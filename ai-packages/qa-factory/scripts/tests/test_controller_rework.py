#!/usr/bin/env python3
"""A receipt without an agent, and a rework nobody could spell.

TP1-15045 ended its morning like this: `--operation dispatch` wrote the S5 receipt, the
hook on `Agent` then refused the call, and the story was left with a `running` dispatch no
agent was doing. `next` answered `wait_existing_job`, `cancel_allowed: false`, "Polling
timeout ... do not authorize cancellation" — no way forward for the orchestrator and none
for the person either.

Earlier the same morning three attempts to dispatch a rework were refused in a row: a bare
`KeyError` printed as `{"error": "'supported'"}`, then "unsupported purpose; regression is
user-owned" for a free-text purpose, then a `SendMessage` to an agent id from a session that
no longer existed. Rework is an operation here, and every refusal names what it wants.
"""
import copy
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from harness import (SCRIPTS, check, check_eq, check_in, check_not_in, cleanup, finish,  # noqa: E402
                     mark_project, run_script, s5_apply, temp_dir, temp_project)

sys.path.insert(0, str(SCRIPTS))
import person_words  # noqa: E402
import stage_guard  # noqa: E402
from controller import (BINDING_KEYS, DISPATCH_DEFAULTS, Controller, apply_rerun_after,  # noqa: E402
                        projection, repair_ledger)
from event_store import StateConflict  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_controller_state as BASE  # noqa: E402
import test_controller_rework_scope as SCOPED  # noqa: E402  (plan_row/gate_a_task fixtures)
import test_dispatch_liveness as LIFE  # noqa: E402  (transcript/fake_hooklib fixtures)
import test_story_closed as CLOSED  # noqa: E402  (closed_story fixture)

AUTOMATOR = "S5-qa-automator-1"


def at_s5(root):
    """The shape the story was stuck in: gate A approved, an S5 receipt, no agent."""
    controller = SCOPED.gate_a_task(root)
    s5_apply(controller, {"id": AUTOMATOR, "stage": "S5", "role": "qa-automator",
                                  "scope": ["TC-1"], "input_hash": "s5-input", "budget": {},
                                  "known_paths": {"root": str(root)},
                                  "idempotency_key": "dispatch:" + AUTOMATOR})
    return controller


def journal(root, records):
    path = root / "qa-factory" / "records" / "journal.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(r) + "\n" for r in records), encoding="utf-8")


def host_receipt(root, **fields):
    path = root / "qa-factory" / "state" / "host-dispatches" / "one.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(fields), encoding="utf-8")


# --- a dispatch nobody is doing is not a job to wait for -----------------------------------

def next_never_waits_for_an_agent_that_was_never_launched():
    root = temp_project("qa-never-started-")
    try:
        controller = at_s5(root)
        check_eq("the stuck state is the one the person saw",
                 controller._next_action_for_state(controller.state())["action"], "wait_existing_job")
        # What a launch really leaves behind on this host: the OTHER roles' transcripts. The
        # automator's receipt is ten minutes old and no transcript names it.
        LIFE.fake_hooklib([LIFE.transcript(root, "critic", "S4-qa-case-critic-1",
                                           role="qa-case-critic", ticket=root.name, age=30)])
        # The receipt here is seconds old, so the project's own waiting time is the honest way
        # to reach the threshold; a story in flight is never closed before it passes.
        early = Controller(root).next_action()
        check_eq("seconds after the receipt the factory says it cannot tell yet",
                 (early["action"], early["liveness"]), ("wait_existing_job", "unknown"))
        (root / "qa-factory" / "config.json").write_text(
            json.dumps({"dispatch": {"never_started_after_s": 0.01}}), encoding="utf-8")
        action = Controller(root).next_action()
        check_eq("next closes it instead of telling the story to wait",
                 action["action"], "relaunch")
        check_eq("and hands over the packet that starts the work again",
                 action["dispatch_request"]["role"], "qa-automator")
        check_eq("with the scope and inputs of the receipt that never reached an agent",
                 (action["dispatch_request"]["scope"], action["dispatch_request"]["input_hash"]),
                 (["TC-1"], "s5-input"))
        check_eq("under an id that does not collide with it",
                 action["dispatch_request"]["id"], "S5-qa-automator-2")
        state = Controller(root).state()
        check_eq("the receipt is kept, marked for what it was",
                 state["dispatches"][AUTOMATOR]["status"], "never_started")
        check_in("the journalled reason says why the factory believes it",
                 "no subagent transcript names this dispatch",
                 state["dispatches"][AUTOMATOR].get("reason", ""))
        check_eq("and S5 is startable again", state["stages"]["S5"]["status"], "pending")
        check_eq("a second pass has nothing left to close",
                 Controller(root).never_started_fixes(), [])
        check_eq("and recover agrees with next", Controller(root).recover()["journalled_repairs"], [])
        s5_apply(controller, dict(action["dispatch_request"]))
        check_eq("the relaunch packet dispatches as it stands",
                 Controller(root).state()["dispatches"]["S5-qa-automator-2"]["status"], "running")
    finally:
        LIFE.without_hooklib()
        cleanup(root)


def a_working_agent_is_still_waited_for():
    root = temp_project("qa-launched-")
    try:
        controller = at_s5(root)
        LIFE.fake_hooklib([LIFE.transcript(root, "auto", AUTOMATOR, ticket=root.name, age=5)])
        check_eq("a transcript written five seconds ago closes nothing",
                 controller.liveness_fixes(), [])
        action = Controller(root).next_action()
        check_eq("so next still waits for the job", action["action"], "wait_existing_job")
        check_eq("and says on what evidence", action["liveness"], "alive")
    finally:
        LIFE.without_hooklib()
        cleanup(root)


def a_host_receipt_is_evidence_too():
    root = temp_project("qa-host-receipt-")
    try:
        controller = at_s5(root)
        host_receipt(root, agent_id="a1", agent_type="qa-automator", task_id=root.name,
                     dispatch_id=AUTOMATOR, status="running")
        check_eq("a live host binding for this dispatch is evidence of a launch",
                 controller.liveness_fixes(), [])
    finally:
        cleanup(root)


def a_host_that_records_nothing_is_left_alone():
    """Absence of a record is evidence only on a host that keeps records. A bundled runtime
    journals no subagent_stop at all, and a job running there is still a job."""
    root = temp_project("qa-silent-host-")
    try:
        controller = at_s5(root)
        LIFE.without_hooklib()
        check_eq("with nothing recorded for this story nothing is closed",
                 controller.liveness_fixes(), [])
        action = Controller(root).next_action()
        check_eq("and next answers exactly as it did before", action["action"], "wait_existing_job")
        check_eq("saying plainly that it cannot tell", action["liveness"], "unknown")
        check_in("and carrying the one command a person's word needs",
                 "--operation release", action["release"])
    finally:
        cleanup(root)


def a_recorded_denial_closes_it_even_with_a_receipt():
    """A receipt that came BEFORE the refusal does not save the dispatch: it is a launch of
    something else, long silent. (A receipt after the refusal, or a living agent, does: see
    test_denial_scope.py - this test used to pin a receipt with no time and a file written
    seconds ago, which is exactly the live automator the denial must not close.)"""
    root = temp_project("qa-denied-")
    try:
        controller = at_s5(root)
        host_receipt(root, agent_id="a1", agent_type="qa-automator", task_id=root.name,
                     dispatch_id=AUTOMATOR, status="running",
                     bound_at=1_789_969_860.0 - 3600)    # an hour before the refusal below
        denials = root / "state" / "dispatch-denials.jsonl"
        denials.parent.mkdir(parents=True, exist_ok=True)
        denials.write_text(json.dumps({"at": "2026-09-21T05:51:00+00:00", "stage": "S5",
                                       "role": "qa-automator", "dispatch_id": AUTOMATOR,
                                       "reason": "stage guard refused S5"}) + "\n", encoding="utf-8")
        fixes = controller.never_started_fixes()
        check_eq("a recorded denial is the end of the argument", len(fixes), 1)
        check_in("and it says which record proved it", "dispatch-denials.jsonl", fixes[0]["reason"])
    finally:
        cleanup(root)


def a_story_under_no_project_closes_nothing():
    """t-622 (B-309 (d), F-2): `_project_root` is None when no `qa-factory/config.json` stands at or above the story - it used
    to be the task root, so a receipt under `<story>/qa-factory/state/host-dispatches` (a folder that is no project's) was
    read as the project's and could close a dispatch. Now: no project, no host records to prove anything from."""
    root = temp_dir("qa-no-project-")     # NOT temp_project: this fixture models the "unknown" road (t-617 section 8.2) - the marker is removed below
    try:
        controller = at_s5(root)
        (root / "qa-factory" / "config.json").unlink()      # the gate-A fixture made the story its own project: it is none
        LIFE.without_hooklib()
        check_eq("fixture: no marker at or above the story, so the project is None (not the task root)",
                 controller._project_root(), None)
        host_receipt(root, agent_id="a1", agent_type="qa-automator", task_id=root.name,
                     dispatch_id=AUTOMATOR, status="terminal")
        check_eq("a terminal receipt under the story's own qa-factory/state closes nothing (the story is no project)",
                 controller.liveness_fixes(), [])
        check_eq("...and the dispatch is still running", controller.state()["dispatches"][AUTOMATOR]["status"], "running")
        check_eq("_launched_after with no project is True: undecided keeps the veto (it was a TypeError inside "
                 "dispatch_liveness, caught as False)", controller._launched_after({"id": AUTOMATOR}, None, {}), True)
        denials = root / "state" / "dispatch-denials.jsonl"
        denials.parent.mkdir(parents=True, exist_ok=True)
        denials.write_text(json.dumps({"at": "2026-09-21T05:51:00+00:00", "stage": "S5", "role": "qa-automator",
                                       "dispatch_id": AUTOMATOR, "reason": "stage guard refused S5"}) + "\n", encoding="utf-8")
        check_eq("a task-local denial with no project to read a launch from is not a refusal that closes the dispatch",
                 controller._denied(controller.state()["dispatches"][AUTOMATOR]), False)
        check_eq("...so never_started_fixes closes nothing either", controller.never_started_fixes(), [])
        action = Controller(root).next_action()
        check_eq("next still waits for the job", action["action"], "wait_existing_job")
        check_eq("saying plainly that it cannot tell", action["liveness"], "unknown")
        check_in("and names the missing config", "qa-factory/config.json", action["evidence"])
        check_in("and the one command a person's word needs", "--operation release", action["release"])
        check_eq("the config reads fall to their defaults (no TypeError escapes)",
                 (controller._dispatch_setting("api_window_cases"), controller._handed_cases()),
                 (DISPATCH_DEFAULTS["api_window_cases"], {}))
    finally:
        LIFE.without_hooklib()
        cleanup(root)


# --- the stage guard runs BEFORE the receipt ---------------------------------------------

def a_refused_dispatch_leaves_no_receipt():
    root = temp_project("qa-guard-before-")
    original = getattr(stage_guard, "dispatch_errors", None)
    try:
        controller = SCOPED.gate_a_task(root)
        seen = {}

        def refuse(pipeline, stage_id, assume_gate_approved=None, **kwargs):   # kwargs: task_root (C4-1)
            seen["stage"] = stage_id
            return [f"stage {stage_id} is past gate A, and gate A is not approved. "
                    "A person's word passes this: `"
                    + person_words.door(f"waiver.py --task T --stage {stage_id} --block \"gate A\"") + "`"]

        stage_guard.dispatch_errors = refuse
        message = ""
        try:
            s5_apply(controller, {"id": AUTOMATOR, "stage": "S5", "role": "qa-automator",
                                          "scope": ["TC-1"], "input_hash": "s5", "budget": {},
                                          "known_paths": {}, "idempotency_key": "d1"})
        except StateConflict as exc:
            message = str(exc)
        check_eq("the guard is asked about the stage being dispatched", seen.get("stage"), "S5")
        check_in("the refusal is the guard's own words", "past gate A", message)
        check_in("and it ends in the command that passes it", "waiver.py", message)
        check_eq("a refused dispatch leaves no receipt behind",
                 AUTOMATOR in controller.state()["dispatches"], False)
        check_eq("so the story is not waiting for anybody",
                 Controller(root).next_action()["action"], "prepare_stage")

        stage_guard.dispatch_errors = lambda pipeline, stage_id, assume_gate_approved=None, **kwargs: [
            "stage S5 cannot start"]
        message = ""
        try:
            s5_apply(controller, {"id": AUTOMATOR, "stage": "S5", "role": "qa-automator",
                                          "scope": ["TC-1"], "input_hash": "s5", "budget": {},
                                          "known_paths": {}, "idempotency_key": "d2"})
        except StateConflict as exc:
            message = str(exc)
        check_in("a block that forgot the person's word gets it added here", "waiver.py", message)

        del stage_guard.dispatch_errors
        s5_apply(controller, {"id": AUTOMATOR, "stage": "S5", "role": "qa-automator",
                                      "scope": ["TC-1"], "input_hash": "s5", "budget": {},
                                      "known_paths": {}, "idempotency_key": "d3"})
        check_eq("without the guard the controller behaves exactly as before",
                 controller.state()["dispatches"][AUTOMATOR]["status"], "running")
    finally:
        if original is not None:
            stage_guard.dispatch_errors = original
        elif hasattr(stage_guard, "dispatch_errors"):
            del stage_guard.dispatch_errors
        cleanup(root)


# --- rework is an operation -------------------------------------------------------------

def rework_is_built_from_the_accepted_work():
    root = temp_project("qa-rework-op-")
    try:
        controller = Controller(root)
        controller.apply("initialize", {"scope": ["TC-1", "TC-2"], "source_revision": "src-1",
                                        "known_paths": {"root": str(root)}, "idempotency_key": "init"})
        BASE.seed_plan(root, [SCOPED.plan_row(1, "automate")])
        for number in range(4):
            BASE.accept_stage(controller, root, f"S{number}")
        controller.apply("dispatch", {"id": "S4-qa-case-designer-1", "stage": "S4",
                                      "role": "qa-case-designer", "scope": ["TC-1", "TC-2"],
                                      "input_hash": "design-input", "known_paths": {"root": str(root)},
                                      "budget": {"requests": 40}, "idempotency_key": "d-designer"})
        BASE.record_stage_acceptance(root, "S4", "S4-qa-case-designer-1")  # E-B11
        controller.apply("accept", {"id": "S4-qa-case-designer-1", "status": "accepted",
                                    "stage_complete": True,
                                    "evidence_refs": [BASE.evidence_ref(root, "designer.txt")],
                                    "idempotency_key": "a-designer"})
        request = controller.build_rework_request("S4", "qa-case-designer", ["TC-2"],
                                                  "apply the critic's two exact replacements")
        check_eq("the input hash comes from the accepted work, not from a guess",
                 request["input_hash"], "design-input")
        check_eq("so does the budget", request["budget"], {"requests": 40})
        check_eq("and the paths", request["known_paths"], {"root": str(root)})
        check_eq("the scope is the cases the person named", request["scope"], ["TC-2"])
        check_eq("the id does not collide with the work it repeats",
                 request["id"], "S4-qa-case-designer-2")
        check_eq("it says which dispatch it reworks", request["rework_of"], "S4-qa-case-designer-1")
        controller.apply("dispatch", dict(request))
        check_eq("and it dispatches", controller.state()["dispatches"][request["id"]]["status"],
                 "running")

        for args, needle in (
                (("S4", "qa-case-designer", ["TC-9"], "why"), "outside the approved scope"),
                (("S4", "qa-code-critic", ["TC-2"], "why"), "accepted roles on S4"),
                (("S9", "qa-case-designer", ["TC-2"], "why"), "no accepted qa-case-designer"),
                (("S4", "qa-case-designer", [], "why"), "at least one case"),
                (("S4", "qa-case-designer", ["TC-2"], ""), "--reason")):
            message = ""
            try:
                controller.build_rework_request(*args)
            except ValueError as exc:
                message = str(exc)
            check_in(f"a refused rework names what it wants ({needle})", needle, message)
        message = ""
        try:
            controller.build_rework_request("S4", "qa-case-designer", ["TC-2"], "why", "regression")
        except ValueError as exc:
            message = str(exc)
        check_in("an invented purpose is answered with the list of real ones",
                 "must be one of: build, collect", message)
    finally:
        cleanup(root)


# --- a repair carries its binding, and a continuation keeps the original request ---------------
#
# A rework request named cases and a reason, and the role repaired whatever CaseVersion it
# happened to read (a stale link on the accepted receipt). And when such a repair stopped, the
# retry and relaunch packets copied four fields of the dispatch RECORD: the binding, the cause,
# the lineage and the mandatory `reason` were gone - and the record's own `reason` is not the
# request's (a checkpoint and the liveness repair both rewrite it), so copying it from there
# would have carried the wrong sentence.

STALE, CANONICAL = "cv_e791cbef9b7195262a80", "cv_c098ad9b0d4075cde6dc"
DESIGNER = "S4-qa-case-designer-1"
CONTRACT = ("case_version_links", "repair_cause", "repair_cause_source", "rework_of", "reason",
            "purpose", "plan_rows", "limits")


def pin(root, *links):
    path = root / "state" / "story-case-links.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"links": list(links)}), encoding="utf-8")


def accept_prerequisites(controller, root, scope):
    """S0-S3 accepted over THIS fixture's scope. `BASE.accept_stage` dispatches TC-1 whatever the
    story's scope is, so a fixture of other cases had to widen its own scope to carry it."""
    for stage in ("S0", "S1", "S2", "S3"):
        if stage == "S3":
            BASE.seed_plan(root, [SCOPED.plan_row(1, "automate")])
        controller.apply("dispatch", {"id": "d" + stage, "stage": stage, "role": "qa-worker",
                                      "scope": list(scope), "input_hash": stage, "budget": {},
                                      "known_paths": {}, "idempotency_key": "dispatch-" + stage})
        BASE.record_stage_acceptance(root, stage)  # E-B11 (no-op for S0/S1); the qa-worker stub has no author dispatch
        controller.apply("accept", {"id": "d" + stage, "status": "accepted", "stage_complete": True,
                                    "evidence_refs": [BASE.evidence_ref(root, stage + ".txt", stage)],
                                    "idempotency_key": "accept-" + stage})


def designer_story(root, scope=("TC-082", "TC-099"), links=None):
    """A story whose S4 designer was accepted over the scope, the pin file naming the CURRENT
    versions and the accepted receipt still carrying a stale one for TC-082."""
    controller = Controller(root)
    controller.apply("initialize", {"scope": list(scope), "source_revision": "src-1",
                                    "known_paths": {"root": str(root)}, "idempotency_key": "init"})
    accept_prerequisites(controller, root, scope)
    pin(root, *(links if links is not None else (
        {"case_id": "TC-082", "version": CANONICAL}, {"case_id": "TC-099", "version": "cv_other"})))
    controller.apply("dispatch", {"id": DESIGNER, "stage": "S4", "role": "qa-case-designer",
                                  "scope": list(scope), "input_hash": "design-input",
                                  "known_paths": {"root": str(root)}, "budget": {"requests": 40},
                                  "case_version_links": [{"case_id": "TC-082", "version": STALE}],
                                  "idempotency_key": "d-designer"})
    # No `stage_complete`: the designer is not the role that closes S4 (the critic is), so the
    # stage stays open - and only an open stage is startable again after a round never started.
    controller.apply("accept", {"id": DESIGNER, "status": "accepted",
                                "evidence_refs": [BASE.evidence_ref(root, "designer.txt")],
                                "idempotency_key": "a-designer"})
    return controller


def refusal(call):
    try:
        call()
    except (ValueError, StateConflict) as exc:
        return str(exc)
    return ""


def sent(controller, dispatch_id):
    """The payload the journal holds for a dispatch: what the request was, stamps included."""
    return next(event["payload"] for event in controller.store.read()
                if event["type"] == "dispatch" and event["payload"]["id"] == dispatch_id)


def never_started_action(root):
    """What `next` answers when nothing proves an agent ever started: the liveness repair closes
    the dispatch and hands over the relaunch packet."""
    (root / "qa-factory").mkdir(parents=True, exist_ok=True)
    (root / "qa-factory" / "config.json").write_text(
        json.dumps({"dispatch": {"never_started_after_s": 0.01}}), encoding="utf-8")
    LIFE.fake_hooklib([LIFE.transcript(root, "critic", "S4-qa-case-critic-1",
                                       role="qa-case-critic", ticket=root.name, age=30)])
    time.sleep(0.05)
    return Controller(root).next_action()


def a_repair_request_carries_the_current_pinned_versions():
    root = temp_project("qa-rework-canonical-case-version-")
    try:
        controller = designer_story(root)
        request = controller.build_rework_request(
            "S4", "qa-case-designer", ["TC-082"],
            "repair against the current canonical CaseVersion", cause="mechanical")
        check_eq("the request resolves the CURRENT canonical version, not the stale receipt's",
                 request.get("case_version_links"), [{"case_id": "TC-082", "version": CANONICAL}])
        check_not_in("a case outside the repair is not copied in", "TC-099",
                     [link["case_id"] for link in request.get("case_version_links") or []])
        for link in request.get("case_version_links") or []:
            link["version"] = "changed-copy"
        again = controller.build_rework_request("S4", "qa-case-designer", ["TC-082"], "again")
        check_eq("the links are copies: editing the request does not touch the pin file",
                 again.get("case_version_links"), [{"case_id": "TC-082", "version": CANONICAL}])
        check_eq("and the request stays valid for the dispatch operation",
                 refusal(lambda: controller.validate("dispatch", again, controller.state())), "")
    finally:
        cleanup(root)


def the_binding_of_a_repair_follows_the_pins_it_can_find():
    root = temp_project("qa-rework-binding-edges-")
    try:
        scope = ("TC-001", "TC-002", "TC-003")
        controller = designer_story(root, scope, links=(
            {"case_id": "TC-001", "area": "speakers", "version": "cv_speakers"},
            {"case_id": "TC-001", "area": "hosts", "version": "cv_hosts"},
            {"case_id": "TC-002", "version": "cv_two"},
            {"case_id": "TC-003"}))
        ask = lambda *cases: controller.build_rework_request(  # noqa: E731
            "S4", "qa-case-designer", list(cases), "repair", cause="tooling")
        links = lambda *cases: ask(*cases).get("case_version_links")  # noqa: E731
        check_eq("a bare id pinned in two areas brings both pins",
                 [link["version"] for link in links("TC-001") or []], ["cv_speakers", "cv_hosts"])
        check_eq("a scope case with no pin is left out, nothing is invented",
                 [link["case_id"] for link in links("TC-002", "TC-003") or []], ["TC-002"])
        check_eq("and a pin with no version is not a pin", links("TC-003"), [])
        check_eq("the area travels with the link it belongs to",
                 [link.get("area") for link in links("TC-001") or []], ["speakers", "hosts"])
        request = ask("TC-001", "TC-002")
        check_eq("the request is valid for the dispatch operation",
                 refusal(lambda: controller.validate("dispatch", request, controller.state())), "")

        (root / "state" / "story-case-links.json").unlink()
        check_eq("a story with no pin file carries an empty list, not an error",
                 links("TC-001"), [])

        caseless = controller.build_rework_request("S1", "qa-worker", [], "the sources moved",
                                                   cause="environment")
        check_eq("a caseless stage names no pins", caseless.get("case_version_links"), [])
        check_eq("and its request is valid too",
                 refusal(lambda: controller.validate("dispatch", caseless, controller.state())), "")
    finally:
        cleanup(root)


def continuation_matches_the_request(label, controller, packet, state, original, parent_status):
    for key in CONTRACT:
        check_eq(f"{label}: {key} is the request's", packet.get(key), original.get(key))
    check_eq(f"{label}: the whole packet passes the dispatch validator",
             refusal(lambda: controller.validate("dispatch", packet, state)), "")
    check_eq(f"{label}: the parent is the dispatch that stopped", parent_status[0],
             parent_status[1])


def a_paused_repair_resumes_with_its_original_request():
    root = temp_project("qa-rework-paused-")
    try:
        controller = designer_story(root)
        request = controller.build_rework_request(
            "S4", "qa-case-designer", ["TC-082"],
            "repair against the current canonical CaseVersion", cause="mechanical")
        request["limits"] = {"requests": 33}
        controller.apply("dispatch", dict(request))
        original = sent(controller, request["id"])
        pin(root, {"case_id": "TC-082", "version": "cv_moved_since"})
        bound = controller.state()["dispatches"][request["id"]].get("request_binding")
        check("the binding is written at dispatch time, from the request",
              bound and bound.get("reason") == request["reason"], str(bound))
        # A checkpoint that tries to carry a binding of its own (adversarial): written once, so
        # nothing the dispatch goes through afterwards can replace it.
        controller.apply("checkpoint", {"id": request["id"], "status": "paused",
                                        "reason": "waiting on the stand",
                                        "checkpoint": {"remaining": ["TC-082"]},
                                        "request_binding": {"reason": "forged"},
                                        "idempotency_key": "cp-1"})
        state = controller.state()
        record = state["dispatches"][request["id"]]
        check_eq("a checkpoint never rewrites the binding", record.get("request_binding"), bound)
        check("the record's reason is no longer the request's (a checkpoint rewrote it)",
              record["reason"] == "waiting on the stand" and original["reason"] != record["reason"],
              record["reason"])
        for source, packet in (("recover", controller.retry_packets(state)[0]["packet"]),
                               ("next", controller.next_action()["packet"]),
                               ("builder", Controller._retry_packet(state, record))):
            check_eq(f"{source}: the reason is the request's, not the checkpoint's",
                     packet.get("reason"), request["reason"])
            check_eq(f"{source}: the binding is the ORIGINAL one, never re-resolved from the pins",
                     packet.get("case_version_links"), [{"case_id": "TC-082", "version": CANONICAL}])
            continuation_matches_the_request(f"paused {source}", controller, packet, state,
                                             original, (record["status"], "paused"))
        packet = Controller._retry_packet(state, record)
        for link in packet.get("case_version_links") or []:
            link["version"] = "changed-copy"
        (packet.get("limits") or {})["requests"] = 1
        packet["known_paths"]["added"] = "x"
        binding = record.get("request_binding") or {}
        check_eq("the packet is a copy: the record's binding is untouched",
                 [link["version"] for link in binding.get("case_version_links") or []], [CANONICAL])
        check_eq("nor its limits", binding.get("limits"), {"requests": 33})
        check_eq("nor its paths", "added" in record["known_paths"], False)
        fresh = Controller._retry_packet(state, record)
        for link in binding.get("case_version_links") or []:
            link["version"] = "changed-record"
        check_eq("and a later change of the record does not reach a packet already built",
                 [link["version"] for link in fresh.get("case_version_links") or []], [CANONICAL])

        resumed = Controller._retry_packet(controller.state(), controller.state()["dispatches"][request["id"]])
        controller.apply("dispatch", dict(resumed))
        new = controller.state()["dispatches"][resumed["id"]]
        check_eq("the retry dispatches as it stands", new["status"], "running")
        check_eq("and its own binding is the original one again, so a second continuation keeps it",
                 (new.get("request_binding") or {}).get("case_version_links"),
                 [{"case_id": "TC-082", "version": CANONICAL}])
        check_eq("with the original reason", (new.get("request_binding") or {}).get("reason"),
                 request["reason"])
    finally:
        cleanup(root)


def a_never_started_repair_relaunches_with_its_original_request():
    root = temp_project("qa-rework-never-started-")
    try:
        controller = designer_story(root)
        request = controller.build_rework_request(
            "S4", "qa-case-designer", ["TC-082", "TC-099"],
            "repair against the current canonical CaseVersion", cause="mechanical")
        # The stand-signal stamp: a cause the CONTROLLER chose, with its source, which a
        # continuation must carry as it carried the person's.
        controller._window_stand_signal = lambda state, req: {"summary": "evidence/runs/s4/run-1.json"}
        stamped = dict(request)
        stamped.pop("repair_cause")
        controller.apply("dispatch", stamped)
        original = sent(controller, request["id"])
        check_eq("the controller stamped the cause and its source on the request",
                 (original.get("repair_cause"), original.get("repair_cause_source")),
                 ("environment", "stand_signal:evidence/runs/s4/run-1.json"))
        ledger_before = repair_ledger(controller.state()["dispatches"],
                                      controller.state()["dispatches"][request["id"]])
        pin(root, {"case_id": "TC-082", "version": "cv_moved_since"})
        try:
            action = never_started_action(root)
            check_eq("nothing proves an agent started, so `next` closes it and relaunches",
                     action["action"], "relaunch")
            state = Controller(root).state()
            record = state["dispatches"][request["id"]]
            check("the record's reason is the liveness repair's, not the request's",
                  record["status"] == "never_started" and record["reason"] != original["reason"]
                  and "no subagent transcript" in record["reason"], record["reason"])
            check_eq("and the liveness repair left the binding as it was",
                     record.get("request_binding", {}).get("reason"), original["reason"])
            for source, packet in (("next", action["dispatch_request"]),
                                   ("builder", Controller._relaunch_packet(state, record))):
                check_eq(f"{source}: the reason is the request's", packet.get("reason"),
                         original["reason"])
                check_eq(f"{source}: the cause and its source are the controller's stamp",
                         (packet.get("repair_cause"), packet.get("repair_cause_source")),
                         ("environment", "stand_signal:evidence/runs/s4/run-1.json"))
                check_eq(f"{source}: the binding is the original, not the moved pin",
                         packet.get("case_version_links"),
                         [{"case_id": "TC-082", "version": CANONICAL},
                          {"case_id": "TC-099", "version": "cv_other"}])
                check_eq(f"{source}: it names the dispatch it relaunches",
                         (packet.get("relaunch_of"), packet.get("rework_of")), (request["id"], DESIGNER))
                continuation_matches_the_request(f"relaunch {source}", controller, packet, state,
                                                 original, (record["status"], "never_started"))
            packet = Controller._relaunch_packet(state, record)
            for link in packet.get("case_version_links") or []:
                link["version"] = "changed-copy"
            packet["known_paths"]["added"] = "x"
            packet["budget"]["added"] = 1
            binding = record.get("request_binding") or {}
            check_eq("the packet is a copy of the binding",
                     [link["version"] for link in binding.get("case_version_links") or []],
                     [CANONICAL, "cv_other"])
            check_eq("of the paths", "added" in record["known_paths"], False)
            check_eq("and of the budget", "added" in record["budget"], False)

            check_eq("the relaunch dispatches as it stands",
                     refusal(lambda: controller.apply("dispatch", dict(action["dispatch_request"]))), "")
            check_eq("the same packet replayed is the same event, not a refusal (FR-45)",
                     refusal(lambda: controller.apply("dispatch", dict(action["dispatch_request"]))), "")
            after = Controller(root).state()
            new = after["dispatches"][action["dispatch_request"]["id"]]
            check_eq("the new record names the closed one", new.get("relaunch_of"), request["id"])
            check("with the original binding", binding and new.get("request_binding") == binding,
                  str(new.get("request_binding")))
            ledger_after = repair_ledger(after["dispatches"], new)
            check_eq("relaunching a round that never started spends no extra round",
                     (ledger_after["counted"], ledger_after["by_cause"]),
                     (ledger_before["counted"], ledger_before["by_cause"]))
        finally:
            LIFE.without_hooklib()
    finally:
        cleanup(root)


def a_relaunch_of_a_test_defect_round_is_not_a_second_round():
    root = temp_project("qa-rework-relaunch-counted-")
    try:
        controller = designer_story(root)
        request = controller.build_rework_request("S4", "qa-case-designer", ["TC-082", "TC-099"],
                                                  "the critic's two replacements")
        controller.apply("dispatch", dict(request))
        running = controller.state()["dispatches"][request["id"]]
        before = repair_ledger(controller.state()["dispatches"], running)
        check_eq("the round counts while it runs", before["counted"], 1)
        try:
            action = never_started_action(root)
            s5_apply(controller, dict(action["dispatch_request"]))
        finally:
            LIFE.without_hooklib()
        after = controller.state()
        new = after["dispatches"][action["dispatch_request"]["id"]]
        check_eq("its relaunch counts as the same one round",
                 repair_ledger(after["dispatches"], new)["counted"], before["counted"])
    finally:
        cleanup(root)


def a_record_without_a_binding_falls_back_to_the_four_fields():
    root = temp_project("qa-rework-no-binding-")
    try:
        controller = designer_story(root)
        state = controller.state()
        record = {"id": "S4-qa-case-designer-9", "stage": "S4", "role": "qa-case-designer",
                  "scope": ["TC-082"], "input_hash": "design-input", "known_paths": {"root": "r"},
                  "budget": {"requests": 5}, "status": "paused", "purpose": "repair_verify",
                  "limits": {"requests": 9}, "execution_kind": "automation",
                  "manual_case_ids": ["TC-082"], "reason": "written before the binding existed",
                  "repair_cause": "mechanical", "checkpoint": {"remaining": ["TC-082"]}}
        for name, build in (("retry", Controller._retry_packet), ("relaunch", Controller._relaunch_packet)):
            packet = build(state, record)
            check_eq(f"{name}: today's four fields come from the record",
                     (packet["purpose"], packet["limits"], packet["execution_kind"],
                      packet["manual_case_ids"]),
                     ("repair_verify", {"requests": 9}, "automation", ["TC-082"]))
            check_eq(f"{name}: nothing else is invented from a record that cannot say it",
                     [key for key in ("case_version_links", "repair_cause", "reason", "rework_of")
                      if key in packet], [])
        bare = dict(record, request_binding={})
        check_eq("a binding that is empty is a request that carried none of them",
                 "purpose" in Controller._retry_packet(state, bare), False)
    finally:
        cleanup(root)


def a_continuation_packet_takes_its_paths_from_the_stamp_and_its_plan_rows_by_presence():
    """0.8.1 `_stamped_paths` (portable tokens, this package's fingerprint) is the one source of a
    continuation's `known_paths`, binding or not; `plan_rows` is carried by PRESENCE: the binding's
    list wins, else the record's, and `[]` stays `[]` while an absent key stays absent."""
    root = temp_project("qa-rework-packet-sources-")
    try:
        controller = designer_story(root)
        state = controller.state()
        base = {"id": "S4-qa-case-designer-8", "stage": "S4", "role": "qa-case-designer",
                "scope": ["TC-082"], "input_hash": "design-input", "budget": {"requests": 5},
                "status": "paused", "checkpoint": {"remaining": ["TC-082"]}}
        stale = {"root": "r", "package_fingerprint": "stamp-of-another-package", "package_version": "0.0.0"}
        for name, build in (("retry", Controller._retry_packet), ("relaunch", Controller._relaunch_packet)):
            for label, extra in (("no binding", {}), ("a binding", {"request_binding": {"reason": "why"}})):
                record = dict(base, known_paths=dict(stale), **extra)
                packet = build(state, record)
                check_eq(f"{name}, {label}: known_paths is what `_stamped_paths` makes of the record's",
                         packet["known_paths"], Controller._stamped_paths(record["known_paths"]))
                check(f"{name}, {label}: the old package's stamp is not copied",
                      packet["known_paths"].get("package_fingerprint") != "stamp-of-another-package",
                      str(packet["known_paths"]))
                check_eq(f"{name}, {label}: the record's own paths are not aliased",
                         record["known_paths"], stale)
                check_eq(f"{name}, {label}: the budget is a copy", packet["budget"] is record["budget"], False)
            rows = [{"row_id": "TS-1"}]
            for label, record, expected in (
                    ("no binding, absent", dict(base), None),
                    ("no binding, empty", dict(base, plan_rows=[]), []),
                    ("no binding, rows", dict(base, plan_rows=rows), rows),
                    ("a binding without the key falls to the record", dict(
                        base, request_binding={"reason": "why"}, plan_rows=rows), rows),
                    ("a binding with the key wins", dict(
                        base, request_binding={"plan_rows": []}, plan_rows=rows), []),
                    ("a binding with the key and rows", dict(
                        base, request_binding={"plan_rows": rows}), rows),
                    ("a binding without the key, none on the record", dict(
                        base, request_binding={"reason": "why"}), None)):
                packet = build(state, record)
                if expected is None:
                    check_eq(f"{name}, {label}: plan_rows stays absent", "plan_rows" in packet, False)
                else:
                    check_eq(f"{name}, {label}: plan_rows", packet.get("plan_rows"), expected)
                    check_eq(f"{name}, {label}: plan_rows is a copy",
                             any(packet["plan_rows"] is value for value in (rows, record.get("plan_rows"),
                                 (record.get("request_binding") or {}).get("plan_rows"))), False)
    finally:
        cleanup(root)


def a_made_up_relaunch_is_refused_and_a_new_dispatch_is_judged_as_before():
    root = temp_project("qa-rework-relaunch-refused-")
    try:
        controller = designer_story(root)
        request = controller.build_rework_request("S4", "qa-case-designer", ["TC-082"],
                                                  "repair", cause="mechanical")
        controller.apply("dispatch", dict(request))
        try:
            action = never_started_action(root)
        finally:
            LIFE.without_hooklib()
        good = action["dispatch_request"]
        state = controller.state()
        check_eq("the packet `next` printed is accepted", refusal(
            lambda: controller.validate("dispatch", good, state)), "")

        made_up = dict(good, relaunch_of="S4-qa-case-designer-99")
        message = refusal(lambda: controller.apply("dispatch", dict(made_up)))
        check_in("a relaunch of a dispatch that does not exist is refused, naming it",
                 "S4-qa-case-designer-99", message)
        check_in("and the door: the packet next prints", "dispatch_request", message)
        message = refusal(lambda: controller.apply("dispatch", dict(good, relaunch_of=DESIGNER)))
        check_in("a relaunch of an accepted dispatch is refused, naming its state",
                 "accepted", message)
        check_in("and the way on", "--operation rework", message)
        check_eq("neither left a receipt", sorted(controller.state()["dispatches"]),
                 sorted(state["dispatches"]))

        no_reason = dict(good, repair_cause="environment")
        no_reason.pop("reason", None)
        no_reason.pop("repair_cause_source", None)
        check_in("a relaunch is no door past the reason a non-test cause needs",
                 "needs `reason`", refusal(lambda: controller.validate("dispatch", no_reason, state)))
        check_in("nor past the purposes that exist", "must be one of",
                 refusal(lambda: controller.validate("dispatch", dict(good, purpose="regression"), state)))

        # The stand-signal stamp is the continuation's own business only when the packet names
        # a dispatch that exists; a made-up name is a new dispatch and is classified as one.
        controller._window_stand_signal = lambda s, req: {"summary": "evidence/runs/s4/run-2.json"}
        for name, packet, expected in (
                ("a relaunch", dict(good), None),
                ("a made-up relaunch", dict(made_up), "environment"),
                ("a fresh dispatch", {k: v for k, v in good.items() if k != "relaunch_of"}, "environment")):
            packet = dict(packet)  # the cause is not named: the stamp is what decides
            packet.pop("repair_cause", None)
            packet.pop("repair_cause_source", None)
            controller._stamp_dispatch(packet, state)
            check_eq(f"{name} is stamped as the stand says only when it is a new dispatch",
                     packet.get("repair_cause"), expected)
    finally:
        cleanup(root)


def a_continuation_is_tied_to_the_dispatch_it_names():
    """`parent_retry` always had to repeat its parent's stage, role, scope and input hash; a
    `relaunch_of` was only checked for existing and for being in a relaunchable state, so a
    packet could name a never-started dispatch and ask for different work. And a `parent_retry`
    that named nothing was a bare KeyError."""
    root = temp_project("qa-rework-continuation-tied-")
    try:
        controller = designer_story(root)
        request = controller.build_rework_request("S4", "qa-case-designer", ["TC-082", "TC-099"],
                                                  "repair", cause="mechanical")
        controller.apply("dispatch", dict(request))
        try:
            action = never_started_action(root)
        finally:
            LIFE.without_hooklib()
        good = action["dispatch_request"]
        state = controller.state()
        check_eq("the packet `next` printed is accepted as it stands", refusal(
            lambda: controller.validate("dispatch", good, state)), "")
        record = state["dispatches"][request["id"]]
        check_eq("and the record's input hash is what the packet copied",
                 good["input_hash"], record["input_hash"])

        for field, value in (("stage", "S3"), ("role", "qa-worker"),
                             ("scope", ["TC-099"]), ("input_hash", "other-input")):
            message = refusal(lambda: controller.apply("dispatch", dict(good, **{field: value})))
            check_in(f"a relaunch that changes {field} is refused", "relaunch_of", message)
            check_in(f"and says it is {field} that differs", f"differs in {field}", message)
            check_in("and what the dispatch it names has", repr(record[field]), message)
            check_in("and the door: the packet next prints, dispatched as it stands",
                     "dispatch_request", message)
            check_in("and that different work is a dispatch of its own", "new dispatch", message)
        message = refusal(lambda: controller.validate(
            "dispatch", dict(good, role="qa-worker", scope=["TC-099"]), state))
        check_in("every difference is named in the one refusal", "differs in role, scope", message)
        check_eq("none of them left a receipt", sorted(controller.state()["dispatches"]),
                 sorted(state["dispatches"]))
        # A scope that is absent on the record is the same as an empty one.
        bare = dict(record, id="S4-qa-case-designer-8", scope=None)
        bare_state = dict(state, dispatches=dict(state["dispatches"], **{bare["id"]: bare}))
        check_eq("an absent scope on the dispatch is an empty scope, not a difference",
                 refusal(lambda: controller.validate(
                     "dispatch", dict(good, relaunch_of=bare["id"], scope=[]), bare_state)), "")

        # A name that is not even a string: a bare `TypeError: unhashable` from a dict lookup.
        for field in ("relaunch_of", "parent_retry"):
            for value in (["S4-qa-case-designer-2"], {"id": "S4-qa-case-designer-2"}):
                packet = dict(good, **{field: value}, checkpoint={"remaining": ["TC-082"]})
                if field == "parent_retry":
                    packet.pop("relaunch_of")
                try:
                    controller.validate("dispatch", packet, state)
                    message, kind = "", "no refusal"
                except StateConflict as exc:
                    message, kind = str(exc), "refusal"
                except Exception as exc:  # noqa: BLE001 - the point: nothing bare may come out
                    message, kind = str(exc), type(exc).__name__
                check_eq(f"{field} = {type(value).__name__}: a refusal, not {kind}", kind, "refusal")
                check_in(f"{field} = {type(value).__name__}: it says it names no dispatch",
                         "names no dispatch", message)
                check_in(f"{field} = {type(value).__name__}: and the door", "controller.py --operation next",
                         message)

        gone = dict(good, id="S4-qa-case-designer-9", parent_retry="S4-qa-case-designer-99",
                    checkpoint={"remaining": ["TC-082"]}, idempotency_key="dispatch:gone")
        gone.pop("relaunch_of")
        for name, call in (("validate", lambda: controller.validate("dispatch", dict(gone), state)),
                           ("apply", lambda: controller.apply("dispatch", dict(gone)))):
            try:
                call()
                message, bare_key = "", False
            except KeyError:
                message, bare_key = "", True
            except (ValueError, StateConflict) as exc:
                message, bare_key = str(exc), False
            check_eq(f"{name}: a parent_retry that names no dispatch is no bare KeyError", bare_key, False)
            check_in(f"{name}: it is refused, naming it", "S4-qa-case-designer-99", message)
            check_in(f"{name}: and the door: the packet next or recover prints", "controller.py --operation next",
                     message)
        check_eq("and no receipt was left", sorted(controller.state()["dispatches"]),
                 sorted(state["dispatches"]))
        check_eq("a relaunch that repeats the same work is not touched",
                 refusal(lambda: controller.apply("dispatch", dict(good))), "")
    finally:
        cleanup(root)


def a_completion_cannot_bind_a_record_that_has_no_binding():
    """`request_binding` is written once, from the dispatch request. A record with none (imported
    from a pre-controller pipeline) must not be given one by a checkpoint or an accept payload:
    a continuation would then be built from words the request never carried."""
    from controller import projection
    legacy = {"id": "legacy:S1", "stage": "S1", "role": "legacy", "status": "incomplete",
              "checkpoint": {"remaining": ["S1"]}, "reason": "imported", "imported": True}
    start = {"type": "initialize", "sequence": 1, "payload": {
        "scope": [], "source_revision": "s", "known_paths": {},
        "legacy_import": {"stages": {"S1": {"status": "incomplete", "dispatch_id": "legacy:S1",
                                            "imported": True}},
                          "dispatches": {"legacy:S1": legacy}, "decisions": {}}}}
    forged = {"reason": "forged", "rework_of": "S1-x-1", "case_version_links": [{"case_id": "TC-1"}]}
    for kind, payload in (
            ("checkpoint", {"id": "legacy:S1", "status": "paused", "reason": "r",
                            "checkpoint": {"remaining": ["S1"]}, "request_binding": forged}),
            ("accept", {"id": "legacy:S1", "status": "accepted", "stage_complete": True,
                        "evidence_refs": [{"path": "a", "sha256": "0" * 64}],
                        "request_binding": forged})):
        record = projection([start, {"type": kind, "sequence": 2, "payload": payload}]
                            )["dispatches"]["legacy:S1"]
        check_eq(f"{kind}: the rest of the payload still lands", record["status"], payload["status"])
        check_eq(f"{kind}: but no binding is set on a record that had none",
                 "request_binding" in record, False)
        check_eq(f"{kind}: so a continuation of it falls back to the four fields",
                 Controller._original_request(record), {})


def no_bare_key_error_reaches_a_reader():
    root = temp_project("qa-key-error-")
    try:
        controller = SCOPED.gate_a_task(root)
        message = ""
        try:
            s5_apply(controller, {"id": "x", "stage": "S5", "role": "qa-automator",
                                          "scope": ["TC-1"], "input_hash": "s5", "budget": {},
                                          "known_paths": {}, "idempotency_key": "k",
                                          "model_policy": {"parent": {"model": "m"}}})
        except (ValueError, KeyError) as exc:
            message = str(exc)
        check("a missing model_policy field is no longer the bare key the CLI printed",
              message != "'supported'", message)
        check_in("it names the field the request is missing", "model_policy requires", message)
        check_in("and the other one beside it", "'parent'", message)
        check_in("and says what omitting the policy does", "inherit", message)

        result = run_script("controller.py", "--task-root", root, "--operation", "teleport")
        check_in("an unknown operation is answered with the list of operations",
                 "must be one of", result.stderr)
        check_in("which includes the ones a person actually types", "gate-decision", result.stderr)
    finally:
        cleanup(root)


def the_cli_records_a_gate_decision_and_a_rework():
    root = temp_project("qa-cli-ops-")
    try:
        controller = Controller(root)
        controller.apply("initialize", {"scope": ["TC-1"], "source_revision": "src-1",
                                        "known_paths": {"root": str(root)}, "idempotency_key": "init"})
        BASE.seed_plan(root, [SCOPED.plan_row(1, "automate")])
        for number in range(5):
            BASE.accept_stage(controller, root, f"S{number}")
        result = run_script("controller.py", "--task-root", root, "--operation", "gate-decision",
                            "--gate", "A", "--words", "approve, keep all automate")
        check("the CLI records the gate decision in one call", result.returncode == 0,
              result.stderr)
        recorded = json.loads(result.stdout)
        check_eq("and says so", recorded["recorded"], True)
        check_eq("with the next action in the same answer",
                 recorded["next_action"]["stage"], "S5")
        check_eq("the person's words are what was recorded",
                 Controller(root).state()["decisions"]["gateA-" + root.name]["authorization_source"],
                 "approve, keep all automate")
        result = run_script("controller.py", "--task-root", root, "--operation", "rework",
                            "--stage", "S4", "--role", "qa-worker", "--cases", "TC-1",
                            "--reason", "carry the case ids into the plan", "--build-only")
        check("a rework request can be inspected before it is sent", result.returncode == 0,
              result.stderr)
        built = json.loads(result.stdout)
        check_eq("and nothing was dispatched by the inspection", built["dispatched"], False)
        check_eq("the request is complete enough to send as it stands",
                 sorted(k for k in ("id", "stage", "role", "scope", "input_hash", "budget",
                                    "known_paths") if k in built["request"]),
                 ["budget", "id", "input_hash", "known_paths", "role", "scope", "stage"])
    finally:
        cleanup(root)


# --- C1-2 (conductor/1, C4, FR-8): a rework takes the person's words from a file ------------------------------------

def rework_takes_the_persons_words_from_a_file():
    """`rework --words-file` goes through `person_words.read`, so a multi-line reason (CRLF included) is stored whole; both
    `--reason` and `--words-file` are refused (exit 2) before any event; the inline `--reason` is untouched, also under the
    cmd launcher, where `gate-decision --words` inline is refused (the control that proves the marker is on)."""
    import os
    root = temp_project("qa-rework-words-")
    try:
        controller = Controller(root)
        controller.apply("initialize", {"scope": ["TC-1"], "source_revision": "src-1",
                                        "known_paths": {"root": str(root)}, "idempotency_key": "init"})
        BASE.seed_plan(root, [SCOPED.plan_row(1, "automate")])
        for number in range(5):
            BASE.accept_stage(controller, root, f"S{number}")
        words = root / "words.txt"
        raw = b"the export test checks only the status code\r\nplease check the body too\r\n"
        words.write_bytes(raw)
        base = ("--task-root", root, "--operation", "rework", "--stage", "S4", "--role", "qa-worker", "--cases", "TC-1")
        before = Controller(root).state()["revision"]
        result = run_script("controller.py", *base, "--words-file", words, "--build-only")
        check("C4: --words-file alone builds the request", result.returncode == 0, result.stderr)
        check_eq("C4: the request's reason is the file's bytes, CRLF and two lines whole",
                 json.loads(result.stdout)["request"]["reason"].encode("utf-8"), raw)
        result = run_script("controller.py", *base, "--words-file", words)
        check("C4: and it dispatches", result.returncode == 0, result.stderr)
        stored = [d.get("reason") for d in Controller(root).state()["dispatches"].values() if d.get("rework_of")]
        check_eq("C4: the stored receipt keeps the reason whole", [r.encode("utf-8") for r in stored if r], [raw])
        after_one = Controller(root).state()["revision"]
        check("C4: that dispatch is an event", after_one > before)
        result = run_script("controller.py", *base, "--words-file", words, "--reason", "inline words")
        check_eq("C4: both flags are refused with exit 2", result.returncode, 2)
        check_in("C4: ...and the refusal names both options", "--reason and --words-file", result.stderr)
        check_eq("C4: ...and no event was recorded", Controller(root).state()["revision"], after_one)
        result = run_script("controller.py", *base, "--words-file", root / "missing.txt")
        check_eq("C4: a missing file is refused with exit 2", result.returncode, 2)
        check_eq("C4: ...and records no event", Controller(root).state()["revision"], after_one)
        # the inline path is untouched, also under the cmd launcher (the factory's own finding text goes there)
        via_cmd = dict(os.environ, QA_FACTORY_LAUNCHER="cmd")
        refused = run_script("controller.py", "--task-root", root, "--operation", "gate-decision", "--gate", "A",
                             "--words", "approve", "--build-only", env=via_cmd)
        check_eq("C4 control: under the cmd launcher an inline person's words (gate-decision --words) are refused",
                 refused.returncode, 2)
        inline = run_script("controller.py", *base, "--reason", "the refusal, verbatim", "--build-only", env=via_cmd)
        check("C4: inline --reason is still accepted under the cmd launcher", inline.returncode == 0, inline.stderr)
        check_eq("C4: ...and is stored as given", json.loads(inline.stdout)["request"]["reason"], "the refusal, verbatim")
    finally:
        cleanup(root)


# --- a rework is never the opener of a window (B-007, F7-1) ----------------------------------------

def _receipt(identifier, scope=("TC-1",), status="accepted", role="qa-automator", stage="S5", **extra):
    return dict({"id": identifier, "stage": stage, "role": role, "scope": list(scope), "status": status}, **extra)


def a_rework_is_never_the_opener_of_a_window():
    """S7 and S4 register their reworks on a window whose plain opener sits under another key
    (a wider S5 window, the designer's own scope): the first repair was read as the opener and
    cost nothing, so the cap allowed one round more than the round text said."""
    window = _receipt("next")

    def ledger(*receipts):
        return {r["id"]: r for r in receipts}

    s7 = ledger(_receipt("S5-qa-automator-2", rework_of="S5-qa-automator-1", repair_cause="test_defect"),
                _receipt("S5-qa-automator-3", rework_of="S5-qa-automator-2", repair_cause="test_defect"))
    found = repair_ledger(s7, window)
    check_eq("S7-shaped: two reworks on [TC-1] and no plain opener are two rounds", found["counted"], 2)
    check_eq("and the window is opened by them", found["opened"], True)
    check_eq("each round is named", [r["id"] for r in found["rounds"]],
             ["S5-qa-automator-2", "S5-qa-automator-3"])

    s5 = ledger(_receipt("S5-qa-automator-1"),
                _receipt("S5-qa-automator-2", rework_of="S5-qa-automator-1", repair_cause="test_defect"))
    check_eq("S5-shaped: the plain opener and one rework are one round", repair_ledger(s5, window)["counted"], 1)

    later = ledger(_receipt("S5-qa-automator-2", rework_of="S5-qa-automator-1", repair_cause="test_defect"),
                   _receipt("S5-qa-automator-1"))
    check_eq("the plain dispatch is the opener wherever it stands in the journal",
             [r["id"] for r in repair_ledger(later, window)["rounds"]], ["S5-qa-automator-2"])

    resumed = ledger(_receipt("S5-qa-automator-2", status="superseded", rework_of="S5-qa-automator-1",
                              repair_cause="test_defect"),
                     _receipt("S5-qa-automator-3", parent_retry="S5-qa-automator-2"))
    check_eq("a resumed rework is one round, not the opener",
             repair_ledger(resumed, window)["counted"], 1)

    dead_opener = ledger(_receipt("S5-qa-automator-1", status="never_started"),
                         _receipt("S5-qa-automator-2", rework_of="S5-qa-automator-1", repair_cause="test_defect"))
    check_eq("an opener that never started leaves the rework a round", repair_ledger(dead_opener, window)["counted"], 1)

    check_eq("a window with nothing live is not opened",
             (repair_ledger({}, window)["opened"], repair_ledger({}, window)["counted"]), (False, 0))
    other = ledger(_receipt("S5-qa-automator-2", scope=("TC-9",), rework_of="x", repair_cause="test_defect"))
    check_eq("another window's rework spends nobody's cap here", repair_ledger(other, window)["counted"], 0)
    tooling = ledger(_receipt("S5-qa-automator-2", rework_of="x", repair_cause="tooling"))
    check_eq("a rework about the tooling is a round of its own cause and spends no cap",
             (repair_ledger(tooling, window)["by_cause"], repair_ledger(tooling, window)["counted"]),
             ({"tooling": 1}, 0))


def s4_rounds_survive_a_changed_case_list():
    """The S4 designer's rounds are counted for the story, not for one case list: a repair that adds
    or drops a case changes the scope hash, and the count used to start again from 0 (critic t-064:
    5 cases -> 1, 6 cases -> 1, 7 cases -> 0), so the S4 loop could run past its cap."""
    window = _receipt("next", role="qa-case-designer", stage="S4", scope=("TC-1", "TC-2", "TC-3"))

    def ledger(*receipts):
        return {r["id"]: r for r in receipts}

    drift = ledger(_receipt("S4-qa-case-designer-1", role="qa-case-designer", stage="S4", scope=("TC-1", "TC-2", "TC-3")),
                   _receipt("S4-qa-case-designer-2", role="qa-case-designer", stage="S4", scope=("TC-1", "TC-2"),
                            rework_of="S4-qa-case-designer-1", repair_cause="test_defect"),
                   _receipt("S4-qa-case-designer-3", role="qa-case-designer", stage="S4", scope=("TC-1", "TC-2", "TC-3"),
                            rework_of="S4-qa-case-designer-2", repair_cause="test_defect"))
    check_eq("S4: rounds over three different case lists are still two rounds",
             repair_ledger(drift, window)["counted"], 2)
    check_eq("and a fourth case list asks the same ledger",
             repair_ledger(drift, _receipt("x", role="qa-case-designer", stage="S4", scope=("TC-1", "TC-2", "TC-3", "TC-4")))["counted"], 2)
    plain = ledger(_receipt("S5-qa-automator-1", scope=("TC-1", "TC-2")),
                   _receipt("S5-qa-automator-2", scope=("TC-1",), rework_of="S5-qa-automator-1", repair_cause="test_defect"))
    check_eq("S5 keeps its per-window key: another case list is another window",
             repair_ledger(plain, _receipt("x", scope=("TC-1", "TC-2", "TC-3")))["counted"], 0)

    root = temp_project("qa-s4-drift-")
    try:
        cases = ["TC-1", "TC-2", "TC-3"]
        controller = Controller(root)
        controller.apply("initialize", {"scope": cases, "source_revision": "src-1",
                                        "known_paths": {"root": str(root)}, "idempotency_key": "init"})
        BASE.seed_plan(root, [SCOPED.plan_row(1, "automate")])
        for number in range(4):
            BASE.accept_stage(controller, root, f"S{number}")
        controller.apply("dispatch", {"id": "S4-qa-case-designer-1", "stage": "S4", "role": "qa-case-designer",
                                      "scope": cases, "input_hash": "design-input", "known_paths": {"root": str(root)},
                                      "budget": {}, "idempotency_key": "d-designer"})
        BASE.record_stage_acceptance(root, "S4", "S4-qa-case-designer-1")  # E-B11: a closing accept of S4 needs the acceptor's record
        controller.apply("accept", {"id": "S4-qa-case-designer-1", "status": "accepted", "stage_complete": True,
                                    "evidence_refs": [BASE.evidence_ref(root, "designer.txt")],
                                    "idempotency_key": "a-designer"})

        def budget_for(scope):
            return Controller(root).prepare({"stage": "S4", "role": "qa-case-designer", "scope": scope})["repair_budget"]

        check_eq("S4: a fresh story has spent nothing", budget_for(cases)["counted"], 0)
        first = controller.build_rework_request("S4", "qa-case-designer", ["TC-1", "TC-2"], "round one")
        controller.apply("dispatch", dict(first))
        controller.apply("accept", {"id": first["id"], "status": "accepted", "stage_complete": False,
                                    "evidence_refs": [BASE.evidence_ref(root, "designer-2.txt")],
                                    "idempotency_key": "a-" + first["id"]})
        check_eq("S4: after one rework the next round reads 1 of 2", (budget_for(cases)["counted"], budget_for(cases)["cap"]), (1, 2))
        second = controller.build_rework_request("S4", "qa-case-designer", cases, "round two, a case was added")
        controller.apply("dispatch", dict(second))
        controller.apply("accept", {"id": second["id"], "status": "accepted", "stage_complete": False,
                                    "evidence_refs": [BASE.evidence_ref(root, "designer-3.txt")],
                                    "idempotency_key": "a-" + second["id"]})
        check_eq("S4: the second rework, over another case list, is counted: the budget says 2 of 2",
                 (budget_for(["TC-1"])["counted"], budget_for(cases)["counted"], budget_for(cases)["cap"]), (2, 2, 2))
        message = ""
        try:
            controller.apply("dispatch", dict(controller.build_rework_request("S4", "qa-case-designer", ["TC-1", "TC-3"], "round three")))
        except StateConflict as exc:
            message = str(exc)
        check_in("S4: a third rework is refused by the controller's own cap check, on the same key", "repair round(s)", message)
        check_in("and says the cap", "the cap is 2", message)
    finally:
        cleanup(root)


# --- t-675 (C1-4a, F6): a rework that carries a PERSON's words sets aside what runs after it ------------------------
#
# Staying monotonic (`set_stage`) meant a person's "the automation needs changes" re-ran the automator and nothing
# after it: S6-S8 stayed `completed` over code that was about to change, and a gate B decision stayed `approved`.
# The controller now writes `rerun_after` on the rework request - only when the reason IS a person's words
# (`--words-file`) - and its replay lowers the named stages, stales the named reviews and gate decisions. A reason
# typed by code (`--reason`: the driver's repairs, the conductor's refusal repairs) is the factory's own finding and
# never stales a stage it did not name. Every test below runs on the controller alone (the CLI where it matters).

WORDS = "the export test checks only the status code\r\nplease check the body too\r\n"
DROP = object()  # a request field a forged-stamp row removes (R9)


def story_to_s8(root):
    """S0-S8 accepted, gate A approved, gate B not asked: the story as it waits at gate B."""
    controller = SCOPED.gate_a_task(root)
    for number in range(5, 9):
        BASE.accept_stage(controller, root, f"S{number}")
    return controller


def pipeline_of(root):
    return json.loads((root / "pipeline.json").read_text(encoding="utf-8"))


def person_rework(controller, stage="S5", role="qa-automator", **extra):
    """The request of a rework whose reason is the person's own words (what `--words-file` builds)."""
    return controller.build_rework_request(stage, role, ["TC-1"], WORDS, words_given=True, **extra)


def rework_cli(root, *tail, stage="S5", role="qa-automator"):
    return run_script("controller.py", "--task-root", root, "--operation", "rework", "--stage", stage,
                      "--role", role, "--cases", "TC-1", *tail)


def words_file(root):
    path = root / "words.txt"
    path.write_bytes(WORDS.encode("utf-8"))
    return path


def settle(controller, root, request):
    """The rework is accepted the way the stage's non-closing role is: the stage stays open."""
    controller.apply("accept", {"id": request["id"], "status": "accepted", "stage_complete": False,
                                "evidence_refs": [BASE.evidence_ref(root, request["id"] + ".txt", request["id"])],
                                "idempotency_key": "accept-" + request["id"]})


def redo(controller, root, stage, identifier):
    """A stage that runs again: one fresh dispatch of the fixture's worker, accepted as complete."""
    controller.apply("dispatch", {"id": identifier, "stage": stage, "role": "qa-worker", "scope": ["TC-1"],
                                  "input_hash": identifier, "budget": {}, "known_paths": {},
                                  "idempotency_key": "dispatch-" + identifier})
    BASE.record_stage_acceptance(root, stage)  # E-B11 (no-op outside S2-S4); the qa-worker stub has no author dispatch
    controller.apply("accept", {"id": identifier, "status": "accepted", "stage_complete": True,
                                "evidence_refs": [BASE.evidence_ref(root, identifier + ".txt", identifier)],
                                "idempotency_key": "accept-" + identifier})


def dispatch_states(state, *ids):
    return {i: state["dispatches"][i]["status"] for i in ids}


def a_person_rework_carries_the_stamp():
    """R1: the request names the completed stages after S5, the critic's review, and the decisions after it."""
    root = temp_project("qa-rerun-r1-")
    try:
        controller = story_to_s8(root)
        revision = controller.state()["revision"]
        stamp = person_rework(controller).get("rerun_after")
        check_eq("R1: the stamp lists S6-S8, the S5 critic's review, and no decision (gate B is undecided)",
                 stamp, {"stages": ["S6", "S7", "S8"], "reviews": ["dS5"], "decisions": []})
        check_eq("R1: the author's own accepted dispatch is not a review of its own rework",
                 "dS5-author" in (stamp or {}).get("reviews", []), False)
        result = rework_cli(root, "--words-file", words_file(root), "--build-only")
        check("R1: the CLI builds it from --words-file", result.returncode == 0, result.stderr)
        built = json.loads(result.stdout)["request"]
        check_eq("R1: --build-only prints the stamp", built.get("rerun_after"), stamp)
        check_eq("R1: the reason is still the file's bytes, CRLF and both lines whole",
                 built["reason"].encode("utf-8"), WORDS.encode("utf-8"))
        check_eq("R1: building recorded nothing", Controller(root).state()["revision"], revision)
        check_eq("R1: the stamp is a COPY of what the state holds - building it twice gives the same one",
                 person_rework(controller).get("rerun_after"), stamp)
    finally:
        cleanup(root)


def the_replay_sets_aside_what_runs_after_the_rework():
    """R2: the dispatch event lowers S6-S8, stales the critic and their accepted dispatches, and `next` goes back to S5."""
    root = temp_project("qa-rerun-r2-")
    try:
        story_to_s8(root)
        result = rework_cli(root, "--words-file", words_file(root))
        check("R2: the CLI dispatches the stamped rework", result.returncode == 0, result.stderr)
        rework = json.loads(result.stdout)["request"]["id"]
        state = Controller(root).state()
        check_eq("R2: S5 is running again, and says which rework did it",
                 {k: state["stages"]["S5"].get(k) for k in ("status", "dispatch_id", "rerun_after")},
                 {"status": "running", "dispatch_id": rework, "rerun_after": rework})
        for name in ("S6", "S7", "S8"):
            entry = state["stages"][name]
            check_eq(f"R2: {name} is pending again, stamped with the rework",
                     (entry["status"], entry.get("rerun_after")), ("pending", rework))
            check_in(f"R2: {name} says why", f"runs again after the rework {rework} of S5", entry["reason"])
        check_eq("R2: the critic and every later accepted dispatch are stale; the author's work and S0-S4 stand",
                 dispatch_states(state, "dS5", "dS6", "dS7", "dS8", "dS5-author", "dS4", "dS0"),
                 {"dS5": "stale", "dS6": "stale", "dS7": "stale", "dS8": "stale",
                  "dS5-author": "accepted", "dS4": "accepted", "dS0": "accepted"})
        check_eq("R2: and they say which rework staled them",
                 {i: state["dispatches"][i].get("stale_by_rework") for i in ("dS5", "dS6", "dS8")},
                 {"dS5": rework, "dS6": rework, "dS8": rework})
        check_eq("R2: gate A is untouched (it is before S5)", state["decisions"]["gate-a"]["status"], "approved")
        controller = Controller(root)
        settle(controller, root, {"id": rework})
        action = Controller(root).next_action()
        check_eq("R2: the rework is accepted, not complete: next goes back to S5",
                 (action["action"], action.get("stage")), ("prepare_stage", "S5"))
        check_eq("R2: S5 is startable again", Controller(root).state()["stages"]["S5"]["status"], "pending")
    finally:
        cleanup(root)


def a_stage_closed_by_a_code_only_receipt_is_lowered():
    """R3 + H14: S6 closed by a receipt has no accepted dispatch; the stamp lowers it by status, and pipeline.json
    loses the receipt's marks with it."""
    root = temp_project("qa-rerun-r3-")
    try:
        controller = SCOPED.gate_a_task(root)
        BASE.accept_stage(controller, root, "S5")
        controller.apply("code_only", {"id": "zero-s6", "stage": "S6", "reason": "all current checks already have valid evidence",
                                       "evidence_refs": [BASE.evidence_ref(root, "zero-s6.txt")], "idempotency_key": "zero-s6"})
        for number in (7, 8):
            BASE.accept_stage(controller, root, f"S{number}")
        check_eq("R3 fixture: S6 is closed by a receipt and no dispatch ran on it",
                 (controller.state()["stages"]["S6"].get("code_only"),
                  [d for d in controller.state()["dispatches"].values() if d.get("stage") == "S6"]), (True, []))
        check_eq("R3 control: pipeline.json carries the receipt's marks before the rework",
                 (pipeline_of(root)["stages"]["S6"].get("code_only"), pipeline_of(root)["stages"]["S6"].get("receipt_id")),
                 (True, "zero-s6"))
        request = person_rework(controller)
        check_eq("R3: the stamp lowers S6 as well as S7-S8", (request.get("rerun_after") or {}).get("stages"), ["S6", "S7", "S8"])
        controller.apply("dispatch", dict(request))
        state = controller.state()
        check_eq("R3: S6 is pending, with no receipt marks", (state["stages"]["S6"]["status"],
                 "code_only" in state["stages"]["S6"], "receipt_id" in state["stages"]["S6"]), ("pending", False, False))
        pipeline_s6 = pipeline_of(root)["stages"]["S6"]
        check_eq("H14: pipeline.json drops code_only and receipt_id of the lowered stage",
                 (pipeline_s6["status"], "code_only" in pipeline_s6, "receipt_id" in pipeline_s6, pipeline_s6.get("rerun_after")),
                 ("pending", False, False, request["id"]))
    finally:
        cleanup(root)


def a_skipped_stage_is_never_touched():
    """R4: a policy-skipped S5/S6 stays skipped - not named by the stamp, and left alone when a stamp names it."""
    root = temp_project("qa-rerun-r4-")
    try:
        controller = SCOPED.gate_a_task(root)
        controller.apply("policy", {"id": "no-implementation", "mode": "preparatory", "reason": "implementation absent",
                                    "source_revision": "src-1", "scope": ["TC-1"],
                                    "evidence_refs": [BASE.evidence_ref(root, "policy.txt")], "idempotency_key": "no-implementation"})
        controller.apply("code_only", {"id": "prep-s7", "stage": "S7", "reason": "no execution blocks in preparatory mode",
                                       "evidence_refs": [BASE.evidence_ref(root, "s7.txt")], "idempotency_key": "prep-s7"})
        controller.apply("code_only", {"id": "prep-s8", "stage": "S8", "reason": "reduced preparatory report",
                                       "evidence_refs": [BASE.evidence_ref(root, "s8.txt")], "idempotency_key": "prep-s8"})
        request = person_rework(controller, "S4", "qa-worker")
        check_eq("R4: the stamp names S7-S8 and gate A, never the skipped S5-S6",
                 request.get("rerun_after"), {"stages": ["S7", "S8"], "reviews": [], "decisions": ["gate-a"]})
        forged = dict(request, rerun_after={"stages": ["S5", "S6", "S7", "S8"], "reviews": [], "decisions": []})
        controller.apply("dispatch", forged)
        state = controller.state()
        check_eq("R4: a stamp that DOES name a skipped stage leaves it skipped, policy and all",
                 [(state["stages"][s]["status"], state["stages"][s].get("policy_id")) for s in ("S5", "S6")],
                 [("skipped", "no-implementation")] * 2)
        check_eq("R4: while the code-only S7-S8 are lowered by status",
                 [state["stages"][s]["status"] for s in ("S7", "S8")], ["pending", "pending"])
    finally:
        cleanup(root)


def a_ticket_changed_rework_is_not_stamped():
    """R5: the B-364 road re-runs its own stages; two writers of one re-run never."""
    root = temp_project("qa-rerun-r5-")
    try:
        controller = story_to_s8(root)
        check_eq("R5 control: the same call with the default cause carries the stamp",
                 "rerun_after" in person_rework(controller), True)
        check_eq("R5: cause ticket_changed carries none",
                 "rerun_after" in person_rework(controller, cause="ticket_changed"), False)
    finally:
        cleanup(root)


def a_closed_story_is_not_stamped():
    """R6: a closed story's rework is a reopen (C1-6): today's reopen stamp, nothing else lowered."""
    root = temp_project("qa-rerun-r6-")
    try:
        controller = CLOSED.closed_story(root)
        request = person_rework(controller)
        check_eq("R6: no stamp on a closed story", "rerun_after" in request, False)
        check("R6: the reopen stamp is as it was", bool(request.get("reopened_at")), str(request))
        controller.apply("dispatch", dict(request))
        state = controller.state()
        check_eq("R6: nothing after S5 was lowered, nothing staled, gate B stands",
                 ([state["stages"][s]["status"] for s in ("S6", "S7", "S8")], state["dispatches"]["dS5"]["status"],
                  state["decisions"]["B"]["status"]), (["completed"] * 3, "accepted", "approved"))
        check_eq("R6: and the person's words reopened the story as before",
                 pipeline_of(root).get("reopened_by_words"), WORDS)
    finally:
        cleanup(root)


def a_round_inside_an_open_stage_is_not_stamped():
    """R7: S4 is still open (its designer accepted, its critic not yet): the request is byte-equal to today's."""
    root = temp_project("qa-rerun-r7-")
    try:
        controller = designer_story(root)
        check_eq("R7 fixture: S4 is not completed", controller.state()["stages"]["S4"]["status"], "pending")
        with_words = controller.build_rework_request("S4", "qa-case-designer", ["TC-082"], WORDS, words_given=True)
        without = controller.build_rework_request("S4", "qa-case-designer", ["TC-082"], WORDS)
        check_eq("R7: no stamp, and the request is the one it always was (plus the person_words mark, R14)",
                 (with_words, "rerun_after" in with_words), (dict(without, person_words=True), False))
    finally:
        cleanup(root)


def an_approved_gate_decision_after_the_stage_goes_stale():
    """R8: a story a person reopened keeps its approved gate B; a person's rework of S5 stales it, so S9 cannot start on
    a gate nobody asks again. Gate A is before S5 and stands."""
    root = temp_project("qa-rerun-r8-")
    try:
        controller = CLOSED.closed_story(root)
        CLOSED.stray(controller, CLOSED.GHOST)      # C1-6a: `dispatch` refuses work on a closed story; the tail is written past it
        controller.release_dispatch(CLOSED.GHOST, "nobody is doing this, drop it")
        check_eq("R8 fixture: the story is open by a person's word and gate B is still approved",
                 (bool(CLOSED.story_closed(pipeline_of(root))), controller.state()["decisions"]["B"]["status"]),
                 (False, "approved"))
        request = person_rework(controller)
        check_eq("R8: the stamp names gate B's decision", request.get("rerun_after"),
                 {"stages": ["S6", "S7", "S8"], "reviews": ["dS5"], "decisions": ["B"]})
        controller.apply("dispatch", dict(request))
        state = controller.state()
        check_eq("R8: gate B is stale, gate A is approved",
                 (state["decisions"]["B"]["status"], state["decisions"]["A"]["status"]), ("stale", "approved"))
    finally:
        cleanup(root)


def a_forged_stamp_is_refused_whole():
    """R9: the controller refuses a `rerun_after` it did not build, naming the field; no event is written."""
    root = temp_project("qa-rerun-r9-")
    try:
        controller = story_to_s8(root)
        request = person_rework(controller)
        revision = controller.state()["revision"]
        path = root / "forged.json"
        empty = {"stages": [], "reviews": [], "decisions": []}
        # the last column re-roles the request (the reworked role is `qa-code-critic` there) or drops `rework_of`
        critic = {"role": "qa-code-critic"}
        for label, stamp, needle, change in (
                ("a stage that is not after S5", dict(empty, stages=["S3"]), "rerun_after.stages", {}),
                ("S5 itself", dict(empty, stages=["S5"]), "rerun_after.stages", {}),
                ("S9, past the last stage a rework can lower", dict(empty, stages=["S9"]), "rerun_after.stages", {}),
                ("ids that are not strings", dict(empty, stages=[6]), "rerun_after.stages", {}),
                ("a review no dispatch holds", dict(empty, reviews=["no-such-dispatch"]), "rerun_after.reviews", {}),
                ("a review of another stage", dict(empty, reviews=["dS6"]), "rerun_after.reviews", {}),
                ("a review by a role that does not close S5 (the author)", dict(empty, reviews=["dS5-author"]),
                 "rerun_after.reviews", critic),
                ("a review by the very role being reworked", dict(empty, reviews=["dS5"]), "rerun_after.reviews", critic),
                ("a decision nobody recorded", dict(empty, decisions=["gate-z"]), "rerun_after.decisions", {}),
                ("gate A on a rework of S5 (the builder names gate A only up to S4)", dict(empty, decisions=["gate-a"]),
                 "rerun_after.decisions", {}),
                ("a stamp on a request that reworks nothing", empty, "rework_of", {"rework_of": DROP}),
                ("not an object", ["S6"], "rerun_after must be", {}),
                ("a key the controller does not write", dict(empty, everything=True), "rerun_after must be", {})):
            forged = {k: v for k, v in dict(request, rerun_after=stamp, **change).items() if v is not DROP}
            path.write_text(json.dumps(forged), encoding="utf-8")
            result = run_script("controller.py", "--task-root", root, "--operation", "dispatch", "--input", path)
            check_eq(f"R9: {label}: exit 2", result.returncode, 2)
            check_in(f"R9: {label}: the refusal names the field", needle, result.stderr)
        check_eq("R9: nothing was written by any of them", Controller(root).state()["revision"], revision)
        path.write_text(json.dumps(request), encoding="utf-8")
        result = run_script("controller.py", "--task-root", root, "--operation", "dispatch", "--input", path)
        check("R9 control: the unforged request dispatches through the same door", result.returncode == 0, result.stderr)
    finally:
        cleanup(root)


def the_validator_stops_where_the_builder_stops():
    """R9 (bounds): the validator refuses every decision the builder would not name - unapproved, gate A past S4, gate B past
    S8 - and accepts the same decision AT each edge (the positive control). Pure: the validator reads only the state."""
    root = temp_project("qa-rerun-r9b-")
    try:
        controller = CLOSED.closed_story(root)
        state = controller.state()  # gates "A" and "B" approved
        def bound(stage, ids, state=state):
            body = {"stage": stage, "role": "qa-worker", "rework_of": "d", "rerun_after": {"decisions": ids}}
            return refusal(lambda: Controller._validate_rerun_after(body, state, int(stage[1:])))
        # the builder names exactly these decisions at each edge - the validator takes each of them
        for stage, named in (("S4", ["A", "B"]), ("S5", ["B"]), ("S8", ["B"])):
            built = Controller._rerun_stamp(state, stage, "qa-worker", ["TC-1"])
            check_eq(f"R9 control: the builder names {named} on a rework of {stage}", (built or {}).get("decisions"), named)
            check_eq(f"R9 control: so the validator takes {named} there", bound(stage, named), "")
        # and refuses the first decision past each bound
        for stage, ids in (("S5", ["A"]), ("S9", ["B"])):
            check_in(f"R9: {ids} on a rework of {stage} is beyond the builder's bound", "rerun_after.decisions", bound(stage, ids))
        stale = copy.deepcopy(state)
        stale["decisions"]["A"]["status"] = "stale"
        check_in("R9: an unapproved decision is refused although the builder's bound holds", "rerun_after.decisions",
                 bound("S4", ["A"], stale))
        check_eq("R9 control: the same decision approved is taken", bound("S4", ["A"]), "")
    finally:
        cleanup(root)


def the_projection_forgets_the_run_a_lowered_stage_was():
    """R10 + H14: after S7 completes again its pipeline.json entry carries no `rerun_after`, and a lowered stage drops
    the later-work marks of its previous life; S8, still waiting, keeps the stamp."""
    root = temp_project("qa-rerun-r10-")
    try:
        controller = story_to_s8(root)
        # an unstamped rework of S7 first: the completed S7 keeps its completion and grows later-work marks
        first = controller.build_rework_request("S7", "qa-worker", ["TC-1"], "the triage missed a failure")
        controller.apply("dispatch", dict(first))
        settle(controller, root, first)
        marks = pipeline_of(root)["stages"]["S7"]
        check_eq("H14 control: pipeline.json S7 carries the later-work marks before the stamp",
                 ("later_work_status" in marks, marks.get("later_work_settled")), (True, True))
        request = person_rework(controller, "S6", "qa-worker")
        check_eq("R10: a rework of S6 stamps S7 and S8", (request.get("rerun_after") or {}).get("stages"), ["S7", "S8"])
        controller.apply("dispatch", dict(request))
        pipeline = pipeline_of(root)["stages"]
        check_eq("R10: both lowered stages carry the stamp in pipeline.json",
                 (pipeline["S7"]["status"], pipeline["S7"].get("rerun_after"), pipeline["S8"].get("rerun_after")),
                 ("pending", request["id"], request["id"]))
        check_eq("H14: and S7 lost its later-work marks with its old run",
                 [key for key in ("later_work_status", "later_work_settled", "code_only", "receipt_id")
                  if key in pipeline["S7"]], [])
        settle(controller, root, request)
        redo(controller, root, "S7", "dS7-again")
        pipeline = pipeline_of(root)["stages"]
        check_eq("R10: after S7 completes again its entry carries no rerun_after",
                 (pipeline["S7"]["status"], "rerun_after" in pipeline["S7"]), ("done", False))
        check_eq("R10: S8, still waiting for its run, keeps the stamp", pipeline["S8"].get("rerun_after"), request["id"])
        redo(controller, root, "S8", "dS8-again")
        check_eq("R10: and loses it when it completes",
                 "rerun_after" in pipeline_of(root)["stages"]["S8"], False)
    finally:
        cleanup(root)


def the_stamp_is_applied_once_and_never_travels_in_a_continuation():
    """R11 + H6: the journal replayed twice gives one state; the stamp applied on top of its own replay changes nothing;
    `rerun_after` is no binding key, so a relaunch or a retry packet never carries it."""
    root = temp_project("qa-rerun-r11-")
    try:
        controller = story_to_s8(root)
        request = person_rework(controller)
        controller.apply("dispatch", dict(request))
        events = controller.store.read()
        after = projection(events)
        check_eq("R11: replaying the journal twice gives the same state", projection(events), after)
        again = copy.deepcopy(after)
        apply_rerun_after(again, request["id"], "S5", request.get("rerun_after") or {})
        check_eq("R11: the stamp applied again on the state it already made changes nothing", again, after)
        check_eq("H6: rerun_after is no binding key", "rerun_after" in BINDING_KEYS, False)
        record = after["dispatches"][request["id"]]
        check_eq("H6: the dispatch record's binding carries none", "rerun_after" in record["request_binding"], False)
        paused = dict(record, status="paused", checkpoint={"remaining": ["TC-1"]})
        for name, packet in (("relaunch", Controller._relaunch_packet(after, record)),
                             ("retry", Controller._retry_packet(after, paused))):
            check_eq(f"H6: a {name} packet of the stamped rework carries no rerun_after", "rerun_after" in packet, False)
    finally:
        cleanup(root)


def staling_the_critic_does_not_reset_the_repair_cap():
    """R12: the cap the driver reads is the AUTHOR's window (`budget_or_none("S5", "qa-automator", cases)`). A stamped
    rework counts as the one round it is, exactly as the same rework without the stamp does; the critic's staling adds
    nothing and removes nothing from it."""
    counted = {}
    for label, stamped in (("stamped", True), ("unstamped", False)):
        root = temp_project(f"qa-rerun-r12-{label}-")
        try:
            controller = story_to_s8(root)
            request = controller.build_rework_request("S5", "qa-automator", ["TC-1"], WORDS, words_given=stamped)
            controller.apply("dispatch", dict(request))
            state = Controller(root).state()
            window = {"stage": "S5", "role": "qa-automator", "scope": ["TC-1"]}
            ledger = repair_ledger(state["dispatches"], window)
            budget = Controller(root).prepare({"stage": "S5", "role": "qa-automator", "scope": ["TC-1"]})["repair_budget"]
            counted[label] = (ledger["counted"], ledger["by_cause"], budget["counted"], budget["cap"],
                              state["dispatches"]["dS5"]["status"])
        finally:
            cleanup(root)
    check_eq("R12: the critic IS staled by the stamp and not without it (the comparison means something)",
             (counted["stamped"][4], counted["unstamped"][4]), ("stale", "accepted"))
    check_eq("R12: the author window's counted, by_cause and the budget the driver reads are the same either way",
             counted["stamped"][:4], counted["unstamped"][:4])
    check_eq("R12: that count is the one round of the rework (cap 2 is not reset to 0 by the staling)",
             counted["stamped"][:4], (1, {"test_defect": 1}, 1, 2))


def two_window_story(root):
    """S0-S8 accepted over TWO cases: TC-1 is the window the fixture's critic `dS5` reviewed, TC-2 (a manual-human plan row, so
    no S6 dispatch is owed for it) the window of a second critic `dS5-w2`, accepted before the stage closed."""
    scope = ("TC-1", "TC-2")
    mark_project(root)
    controller = Controller(root)
    controller.apply("initialize", {"scope": list(scope), "source_revision": "src-1",
                                    "known_paths": {"root": str(root)}, "idempotency_key": "init"})
    for number in range(5):
        BASE.accept_stage(controller, root, f"S{number}")
    BASE.seed_plan(root, [SCOPED.plan_row(1, "automate"), SCOPED.plan_row(2, "manual-human")])
    pin(root, {"case_id": "TC-1", "version": "cv_1"}, {"case_id": "TC-2", "version": "cv_2"})
    controller.apply("decision", BASE.bind_gate_a(root, {
        "id": "gate-a", "gate": "A", "action": "approve", "status": "approved", "authorization_source": "human",
        "source_revision": "src-1", "scope": list(scope), "input_revision": "src-1", "idempotency_key": "gate-a"}))
    s5_apply(controller, {"id": "dS5-w2", "stage": "S5", "role": "qa-code-critic", "scope": ["TC-2"], "input_hash": "w2",
                                  "budget": {}, "known_paths": {}, "idempotency_key": "d-w2"})
    controller.apply("accept", {"id": "dS5-w2", "status": "accepted", "stage_complete": False,
                                "evidence_refs": [BASE.evidence_ref(root, "w2.txt", "w2")], "idempotency_key": "a-w2"})
    for number in range(5, 9):
        BASE.accept_stage(controller, root, f"S{number}")
    return controller


def a_second_person_rework_of_a_pending_stage_stamps_its_own_window():
    """R13 (spec 12, t-679 queue (d)): two person-word reworks of S5, W1 then W2. After the first one's re-run is accepted S5
    is `pending`, no longer `completed`; the second still sets W2's critic aside, so its acceptance cannot approve work that
    was reworked. Controls: no words -> no stamp (H1); a window the first stamp already staled is not named again; an in-stage
    pending S5 no stamped rework reopened stamps nothing."""
    root = temp_project("qa-rerun-r13-")
    try:
        controller = two_window_story(root)
        first = controller.build_rework_request("S5", "qa-automator", ["TC-1"], WORDS, words_given=True)
        check_eq("R13 fixture: the first stamp names W1's critic only - W2's critic is not a review of TC-1",
                 first.get("rerun_after"), {"stages": ["S6", "S7", "S8"], "reviews": ["dS5"], "decisions": []})
        controller.apply("dispatch", dict(first))
        settle(controller, root, first)
        state = controller.state()
        check_eq("R13 fixture: S5 is pending after the first rework, W2's critic still stands",
                 (state["stages"]["S5"]["status"], state["dispatches"]["dS5"]["status"], state["dispatches"]["dS5-w2"]["status"]),
                 ("pending", "stale", "accepted"))
        check_eq("R13 control: the same rework without a person's words stamps nothing (a driver repair, H1)",
                 "rerun_after" in controller.build_rework_request("S5", "qa-automator", ["TC-2"], "the finding", words_given=False),
                 False)
        check_eq("R13 control: a window the first stamp already staled is not named again - nothing left to stamp",
                 "rerun_after" in controller.build_rework_request("S5", "qa-automator", ["TC-1"], WORDS, words_given=True), False)
        second = controller.build_rework_request("S5", "qa-automator", ["TC-2"], WORDS, words_given=True)
        check_eq("R13: the second person's rework of S5 on W2 stamps W2's critic although S5 is pending, and nothing else",
                 second.get("rerun_after"), {"stages": [], "reviews": ["dS5-w2"], "decisions": []})
        controller.apply("dispatch", dict(second))
        state = controller.state()
        check_eq("R13: W2's critic is staled, and says which rework did it",
                 (state["dispatches"]["dS5-w2"]["status"], state["dispatches"]["dS5-w2"].get("stale_by_rework")),
                 ("stale", second["id"]))
        check_eq("R13: S5 is running for the second rework, stamped with it",
                 {k: state["stages"]["S5"].get(k) for k in ("status", "dispatch_id", "rerun_after")},
                 {"status": "running", "dispatch_id": second["id"], "rerun_after": second["id"]})
        settle(controller, root, second)
        action = Controller(root).next_action()
        check_eq("R13: both reviews are owed again: next goes back to S5", (action["action"], action.get("stage")),
                 ("prepare_stage", "S5"))
        ledger = repair_ledger(Controller(root).state()["dispatches"], {"stage": "S5", "role": "qa-automator", "scope": ["TC-2"]})
        check_eq("R13: the cap still counts the second rework as the one round it is (the staling resets nothing)",
                 (ledger["counted"], ledger["by_cause"]), (1, {"test_defect": 1}))
    finally:
        cleanup(root)
    root = temp_project("qa-rerun-r13-s4-")
    try:
        # R7's fixture: S4 is pending mid-round (its designer accepted, its critic not yet) and no stamped rework opened it
        check_eq("R13 control: a pending stage no stamped rework reopened stamps nothing even with a person's words",
                 "rerun_after" in designer_story(root).build_rework_request("S4", "qa-case-designer", ["TC-082"], WORDS,
                                                                            words_given=True), False)
    finally:
        cleanup(root)


def a_rework_without_words_is_todays_flow():
    """H1: `--reason` (the driver's repairs, the conductor's refusal repairs) gets no stamp and stales nothing it did not
    name - an S5 rework leaves S6-S8 and the critic alone; an S7 repair leaves the S5 critic and S6 untouched."""
    for stage, role in (("S5", "qa-automator"), ("S7", "qa-worker")):
        root = temp_project(f"qa-rerun-h1-{stage}-")
        try:
            story_to_s8(root)
            built = rework_cli(root, "--reason", "the refusal, verbatim", "--build-only", stage=stage, role=role)
            check(f"H1: the {stage} rework builds", built.returncode == 0, built.stderr)
            check_eq(f"H1: --reason only: no stamp on {stage}", "rerun_after" in json.loads(built.stdout)["request"], False)
            result = rework_cli(root, "--reason", "the refusal, verbatim", stage=stage, role=role)
            check(f"H1: the {stage} rework dispatches", result.returncode == 0, result.stderr)
            state = Controller(root).state()
            check_eq(f"H1: {stage} --reason: no stage lowered, no dispatch staled, S5 critic and S6 untouched",
                     ([state["stages"][s]["status"] for s in ("S5", "S6", "S7", "S8")],
                      sorted(i for i, d in state["dispatches"].items() if d["status"] == "stale")),
                     (["completed"] * 4, []))
        finally:
            cleanup(root)


def the_person_words_mark_follows_the_words_file():
    """R14 (t-694, F1): the request and the dispatch record carry `person_words: true` exactly when the reason is a person's words
    (`--words-file`, the same `words_given` input as the stamp) - also when the stamp is empty (an S8 rework) - and never with
    `--reason` (a finding typed by code). The gate note quotes `on your words` only for the mark."""
    root = temp_project("qa-rerun-r14-")
    try:
        controller = story_to_s8(root)
        built = rework_cli(root, "--words-file", words_file(root), "--build-only")
        check_eq("R14: --words-file: the built request carries the mark", json.loads(built.stdout)["request"].get("person_words"), True)
        built = rework_cli(root, "--reason", "the refusal, verbatim", "--build-only")
        check_eq("R14: --reason: no mark on the built request", "person_words" in json.loads(built.stdout)["request"], False)
        check_eq("R14: the library call without words_given: no mark", "person_words" in controller.build_rework_request(
            "S5", "qa-automator", ["TC-1"], WORDS), False)
        check_eq("R14: an empty stamp (S8, nothing after it) still carries the mark",
                 person_rework(controller, "S8", "qa-worker").get("person_words"), True)
        result = rework_cli(root, "--words-file", words_file(root))
        check("R14: the rework dispatches", result.returncode == 0, result.stderr)
        record = Controller(root).state()["dispatches"][json.loads(result.stdout)["request"]["id"]]
        check_eq("R14: the dispatch RECORD keeps the mark (the gate note reads the record)", record.get("person_words"), True)
    finally:
        cleanup(root)
    root = temp_project("qa-rerun-r14b-")
    try:
        story_to_s8(root)
        result = rework_cli(root, "--reason", "the refusal, verbatim", stage="S7", role="qa-worker")
        check("R14: a --reason rework dispatches", result.returncode == 0, result.stderr)
        record = Controller(root).state()["dispatches"][json.loads(result.stdout)["request"]["id"]]
        check_eq("R14: and its record has no mark", "person_words" in record, False)
    finally:
        cleanup(root)


def a_stamp_with_nothing_to_set_aside_is_no_stamp():
    """H1 edge: a person-word rework of the last stage has no completed stage above it, no review of its own and no gate B
    decision: an empty stamp set is no stamp, and the request is the one a `--reason` rework builds."""
    root = temp_project("qa-rerun-empty-")
    try:
        controller = story_to_s8(root)
        with_words = person_rework(controller, "S8", "qa-worker")
        check_eq("empty stamp set: the request carries no rerun_after and equals the unstamped one (plus the person_words mark, R14)",
                 (with_words, "rerun_after" in with_words),
                 (dict(controller.build_rework_request("S8", "qa-worker", ["TC-1"], WORDS), person_words=True), False))
        controller.apply("dispatch", dict(with_words))
        state = controller.state()
        check_eq("empty stamp set: applying it lowers and stales nothing else",
                 ([state["stages"][s]["status"] for s in ("S5", "S6", "S7", "S8")],
                  sorted(i for i, d in state["dispatches"].items() if d["status"] == "stale")),
                 (["completed"] * 4, []))
    finally:
        cleanup(root)


def only_one_dispatch_runs_at_a_time_and_a_second_rework_stamps_again():
    """Edge 3: a second rework while the first runs is refused and writes nothing (the controller's own running-dispatch
    rule). Edge 4: after the stages ran again, a new person's rework stamps them again under ITS id."""
    root = temp_project("qa-rerun-e34-")
    try:
        controller = story_to_s8(root)
        first = person_rework(controller, "S6", "qa-worker")
        controller.apply("dispatch", dict(first))
        revision = controller.state()["revision"]
        second = person_rework(controller, "S6", "qa-worker")
        message = refusal(lambda: controller.apply("dispatch", dict(second)))
        check_in("edge 3: a rework while another dispatch runs is refused", "active dispatch", message)
        check_eq("edge 3: and wrote nothing", controller.state()["revision"], revision)
        settle(controller, root, first)
        redo(controller, root, "S7", "dS7-again")
        redo(controller, root, "S8", "dS8-again")
        later = person_rework(controller, "S6", "qa-worker")
        check_eq("edge 4: the stages that ran again are named again", (later.get("rerun_after") or {}).get("stages"), ["S7", "S8"])
        controller.apply("dispatch", dict(later))
        state = controller.state()
        check_eq("edge 4: and carry the NEW rework's id, so each re-show can say what changed",
                 [state["stages"][s].get("rerun_after") for s in ("S7", "S8")], [later["id"]] * 2)
        check("edge 4: the two reworks have different ids", first["id"] != later["id"], first["id"])
    finally:
        cleanup(root)


def a_designer_rework_after_gate_a_stales_the_critic_and_the_gate():
    """Edge 7 + spec 5.6: no case review after gate A (the controller's CASE_REVIEW_AFTER_GATE_A), until a person's rework
    of the designer stales gate A and the critic's acceptance - then the critic may run again."""
    root = temp_project("qa-rerun-s4-")
    try:
        scope = ("TC-082", "TC-099")
        controller = designer_story(root, scope)
        controller.apply("dispatch", {"id": "S4-qa-case-critic-1", "stage": "S4", "role": "qa-case-critic",
                                      "scope": list(scope), "input_hash": "critic-input", "budget": {}, "known_paths": {},
                                      "idempotency_key": "d-critic"})
        BASE.record_stage_acceptance(root, "S4", DESIGNER)  # E-B11: the critic's closing accept reviews the designer's dispatch
        controller.apply("accept", {"id": "S4-qa-case-critic-1", "status": "accepted", "stage_complete": True,
                                    "evidence_refs": [BASE.evidence_ref(root, "critic.txt")], "idempotency_key": "a-critic"})
        controller.apply("decision", BASE.bind_gate_a(root, {
            "id": "gate-a", "gate": "A", "action": "approve", "status": "approved", "authorization_source": "human",
            "source_revision": "src-1", "scope": list(scope), "input_revision": "src-1", "idempotency_key": "gate-a"}))
        critic = {"id": "S4-qa-case-critic-2", "stage": "S4", "role": "qa-case-critic", "scope": list(scope),
                  "input_hash": "critic-input-2", "budget": {}, "known_paths": {}, "idempotency_key": "d-critic-2"}
        check_in("edge 7: after gate A the controller refuses a new case review", "CASE_REVIEW_AFTER_GATE_A",
                 refusal(lambda: controller.apply("dispatch", dict(critic))))
        request = controller.build_rework_request("S4", "qa-case-designer", ["TC-082"], WORDS, words_given=True)
        check_eq("spec 5.6: the stamp stales the critic's review and gate A, and lowers no stage (S5 never ran)",
                 request.get("rerun_after"),
                 {"stages": [], "reviews": ["S4-qa-case-critic-1"], "decisions": ["gate-a"]})
        controller.apply("dispatch", dict(request))
        settle(controller, root, request)
        state = controller.state()
        check_eq("spec 5.6: the critic's acceptance and gate A are stale, S4 is open again",
                 (state["dispatches"]["S4-qa-case-critic-1"]["status"], state["decisions"]["gate-a"]["status"],
                  state["stages"]["S4"]["status"]), ("stale", "stale", "pending"))
        check_eq("edge 7: now the case review may run again (gate A is no longer current)",
                 refusal(lambda: controller.apply("dispatch", dict(critic))), "")
    finally:
        cleanup(root)


def a_paid_round_stays_paid_when_its_own_stage_sets_it_aside():
    """R15 (C1-5a, A1; named R15 because R13 and R14 are taken above; the finding 20261010-ledger-kritika-sbrasyvaetsya-pri-stale):
    a `stale` dispatch counts as a paid round ONLY when a rework of the SAME stage set it aside (the `reviews` stamp: an S5 rework
    stales the S5 critic - its round was spent). A rework of an EARLIER stage (S3/S4) that stales S5 through the stamp's `stages`
    step opens a NEW window: counted 0, or the re-run window's first dispatch would count as round 1 or be refused. Both directions
    run through the real replay (`apply_rerun_after`) and the real ledger."""
    def state_of(rework_stage):
        def d(identifier, role, stage="S5", **extra):
            return dict({"id": identifier, "stage": stage, "role": role, "scope": ["TC-1"], "status": "accepted"}, **extra)
        return {"dispatches": {"a1": d("a1", "qa-automator"), "a2": d("a2", "qa-automator"),
                               "c1": d("c1", "qa-code-critic"), "c2": d("c2", "qa-code-critic"),
                               "r": d("r", "qa-automator" if rework_stage == "S5" else "qa-case-designer", stage=rework_stage,
                                      status="running", rework_of="x")},
                "stages": {"S5": {"status": "completed"}}, "decisions": {}}
    critic = {"stage": "S5", "role": "qa-code-critic", "scope": ["TC-1"]}
    author = dict(critic, role="qa-automator")
    unstaled = state_of("S5")
    check_eq("R15 fixture: before any rework the critic has had one round (c2), the author two (a2 and the rework r)",
             (repair_ledger(unstaled["dispatches"], critic)["counted"], repair_ledger(unstaled["dispatches"], author)["counted"]), (1, 2))
    own = state_of("S5")
    apply_rerun_after(own, "r", "S5", {"stages": [], "reviews": ["c1", "c2"], "decisions": []})
    check_eq("R15: the S5 rework stales the critic through the `reviews` stamp, with the mark",
             [(own["dispatches"][i]["status"], own["dispatches"][i].get("stale_by_rework")) for i in ("c1", "c2")],
             [("stale", "r"), ("stale", "r")])
    check_eq("R15: its round stays paid - the critic's counted stays 1 (the cap is not reset by the person's word)",
             repair_ledger(own["dispatches"], critic)["counted"], 1)
    earlier = state_of("S4")
    apply_rerun_after(earlier, "r", "S4", {"stages": ["S5"], "reviews": [], "decisions": []})
    check_eq("R15 fixture: the S4 rework stales every accepted S5 dispatch through the stamp's `stages` step",
             sorted(i for i, d in earlier["dispatches"].items() if d["status"] == "stale"), ["a1", "a2", "c1", "c2"])
    check_eq("R15: ...and that opens a NEW window - the critic's and the author's counted are 0, not 1",
             (repair_ledger(earlier["dispatches"], critic)["counted"], repair_ledger(earlier["dispatches"], author)["counted"]), (0, 0))
    check_eq("R15 control: a stale dispatch whose mark names no dispatch (an old record) is not a paid round",
             repair_ledger({"c1": dict(earlier["dispatches"]["c1"], stale_by_rework="gone"),
                            "c2": dict(earlier["dispatches"]["c2"], stale_by_rework="gone")}, critic)["counted"], 0)


def s6_runner_rework_takes_its_half_from_its_cases():
    """FB-9 (spec t-1361 R12, F-4): a new-mode S6 qa-runner rework says which half it runs and carries the block.
    K-W1 kind + ids + the dispatch is accepted; K-W2 mixed halves, two doors; K-W2b kind unknown; K-W3 over five split;
    K-W4 the parent is the same half's; K-W5 the automation half is unbounded; K-W6 the legacy mode is unchanged.
    KILLS (M17) the parent read from `prior[-1]` (K-W4, K-W4b) or the kind from the records alone (K-W1); (M18) a mixed rework
    allowed (K-W2); (M19) the block rule skipped (K-W3); (M20) one automated case deciding the half for cases of neither (K-W7)."""
    import test_story_step_manual_block as MB
    import test_fixes_13797 as F
    from detector_verdict import split_items
    manual_cases = ["TC-2", "TC-3", "TC-4", "TC-5", "TC-6"]
    root = temp_dir("qa-fb9-rework-")
    try:
        c = MB.real_story(root, MB.MIXED_7)
        F.runner(c, root, "S6-qa-runner-1", "manual", manual_cases, False)
        F.runner(c, root, "S6-qa-runner-2", "manual", ["TC-7"], False)
        F.runner(c, root, "S6-qa-runner-3", "automation", ["TC-1"], False)       # the LAST accepted runner is the other half
        request = c.build_rework_request("S6", "qa-runner", ["TC-2"], "recheck TC-2")
        check_eq("K-W1: a manual rework is a manual block of its cases",
                 (request["execution_kind"], request["manual_case_ids"], request["scope"]), ("manual", ["TC-2"], ["TC-2"]))
        check_eq("K-W4: its parent is the manual block that HOLDS TC-2 (E25), not the later block or the automation packet",
                 request["rework_of"], "S6-qa-runner-1")
        joined = c.build_rework_request("S6", "qa-runner", ["TC-6", "TC-7"], "recheck both")
        check_eq("K-W4b: cases of two manual blocks take the later block that holds one (one block of two cases)",
                 (joined["rework_of"], joined["manual_case_ids"]), ("S6-qa-runner-2", ["TC-6", "TC-7"]))
        c.apply("dispatch", dict(request))
        check_eq("K-W1: and the controller dispatches it", c.state()["dispatches"][request["id"]]["manual_case_ids"], ["TC-2"])
        F.runner(c, root, request["id"], "manual", ["TC-2"], False)
        auto = c.build_rework_request("S6", "qa-runner", ["TC-1"], "recheck TC-1")
        check_eq("K-W4: an automation rework resumes the automation packet", (auto["execution_kind"], auto["rework_of"]), ("automation", "S6-qa-runner-3"))
        check_eq("K-W5: ...and carries no block", "manual_case_ids" in auto, False)
        # K-W2: both halves in one call
        try:
            c.build_rework_request("S6", "qa-runner", ["TC-1", "TC-2"], "both")
            check("K-W2: a rework over both halves is refused", False)
        except ValueError as exc:
            text = str(exc)
            check_in("K-W2: ...with the manual door", "--cases TC-2 ", text)
            check_in("K-W2: ...and the automated door", "--cases TC-1`", text)
            check_in("K-W2: ...and the reason (one packet, one half)", "one packet runs one half", text)
        # K-W3: over five splits, whole, with the first block's door
        try:
            c.build_rework_request("S6", "qa-runner", manual_cases + ["TC-7"], "all six", )
            check("K-W3: a manual rework of six cases is refused", False)
        except ValueError as exc:
            text = str(exc)
            check_in("K-W3: the split is said", "it names 6 cases, at most 5: split the block", text)
            check_in("K-W3: ...with the first block's rework command", "--cases TC-2,TC-3,TC-4,TC-5,TC-6 --reason", text)
            check_in("K-W3: ...and the rest counted", "1 more block(s) of at most 5 for: TC-7", text)
        # the block problems join the call's other problems in ONE refusal (class rule 27.10)
        try:
            c.build_rework_request("S6", "qa-runner", manual_cases + ["TC-7"], "", purpose="nonsense")
            check("K-W3: a bad call plus a long block is refused", False)
        except ValueError as exc:
            check_eq("K-W3: ...whole: purpose, reason and the block in one answer", len(split_items(str(exc)) or []) >= 3, True)
        # K-W2b: the kind cannot be established (the plan derives nothing; the records hold both halves / none)
        with __import__("unittest.mock", fromlist=["patch"]).patch.object(
                c, "stage_scope", lambda *a, **k: {"derived": False, "scope": [], "reason": "no dispositions"}):
            try:
                c.build_rework_request("S6", "qa-runner", ["TC-2", "TC-1"], "x")
                check("K-W2b: no disposition and no single half: refused", False)
            except ValueError as exc:
                check_in("K-W2b: no disposition and no single half: refused", "the kind of this S6 qa-runner rework cannot be established", str(exc))
                check_in("K-W2b: ...with the within-one-half door", "--cases <the cases of one half>", str(exc))
            single = c.build_rework_request("S6", "qa-runner", ["TC-1"], "x")
            check_eq("K-W2b control: records that hold the case in ONE half give the kind", single["execution_kind"], "automation")
        # K-W7 (F1): a case of NEITHER half never rides along on the automation half (and not on the manual one)
        root3 = temp_dir("qa-fb9-rework-neither-")
        try:
            c3 = MB.real_story(root3, ["automate", "manual-human", "manual-agent"])
            F.runner(c3, root3, "S6-qa-runner-1", "automation", ["TC-1"], False)
            for label, cases in (("automated + manual-human", ["TC-1", "TC-2"]), ("manual-human alone", ["TC-2"]),
                                 ("manual-agent + manual-human", ["TC-3", "TC-2"])):
                try:
                    c3.build_rework_request("S6", "qa-runner", cases, "probe")
                    check(f"K-W7: {label} is refused", False)
                except ValueError as exc:
                    check_in(f"K-W7: {label} is refused naming TC-2 and the stage-scope door", "TC-2", str(exc))
                    check_in(f"K-W7: ...{label}: the stage-scope door", "--operation stage-scope", str(exc))
            check_eq("K-W7 control: the automated case alone is still reworked",
                     c3.build_rework_request("S6", "qa-runner", ["TC-1"], "probe")["execution_kind"], "automation")
        finally:
            cleanup(root3)
        # K-W5: seven automated cases, no bound
        root2 = temp_dir("qa-fb9-rework-auto-")
        try:
            c2 = MB.real_story(root2, ["automate"] * 7)
            F.runner(c2, root2, "S6-qa-runner-1", "automation", [f"TC-{i}" for i in range(1, 8)], True)
            wide = c2.build_rework_request("S6", "qa-runner", [f"TC-{i}" for i in range(1, 8)], "all")
            check_eq("K-W5: seven automated cases are one packet", (wide["execution_kind"], len(wide["scope"]), "manual_case_ids" in wide), ("automation", 7, False))
        finally:
            cleanup(root2)
        # K-W6: the legacy mode is unchanged (no kind is required there)
        legacy = dict(c.state(), plan_contract_mode="legacy")
        with __import__("unittest.mock", fromlist=["patch"]).patch.object(c, "state", lambda: legacy):
            old = c.build_rework_request("S6", "qa-runner", ["TC-2"], "x")
            check_eq("K-W6: a legacy-mode rework carries neither field", ("execution_kind" in old, "manual_case_ids" in old), (False, False))
    finally:
        cleanup(root)


def rh110_s6_half_membership():
    """RH1-10 (spec t-1421 part B, DC1-13 / DC1-15): ONE membership function, `Controller._half_membership_problems`, for both S6
    halves on every road. Keys B-K1..B-K11 and B-K16, edges B-E1..B-E13.
    KILLS (one test file, this one): the automation call dropped from `validate` (B-K2), from `prepare` (B-K1) or from
    `build_rework_request` (B-K7); `_case_rows` errors read as `[]` (B-K6, B-K6b); `execution_kind:` put back into the empty-cases door
    (B-K8); the `named` cut moved to 19 or 21 (B-K10); an id stripped before it is judged (B-K11); the manual sentences reworded (B-K4)."""
    import unittest.mock as mock
    import waiver
    import test_story_step_manual_block as MB
    import test_fixes_13797 as F
    from no_move import check_args
    from controller import MANUAL_BLOCK_CASES, SCOPE_SHOWN

    def refused_with(call):
        try:
            call()
        except (StateConflict, ValueError) as exc:
            return str(exc)
        return None

    root = temp_dir("qa-rh110-")
    try:
        c = MB.real_story(root, MB.MIXED_7)          # TC-1 automate; TC-2..TC-7 manual-agent
        # B-K1: prepare, automation, over a manual-agent case -> cause 1, with the real manual command as its door
        text = refused_with(lambda: c.prepare({"stage": "S6", "role": "qa-runner", "id": "a1", "scope": ["TC-2"], "execution_kind": "automation"}))
        check_in("B-K1: prepare refuses an automation packet over a manual-agent case (cause 1)", "disposed manual-agent in the plan: TC-2", text or "")
        check_in("B-K1: ...with the real manual command as its door",
                 f"story_step.py start --stage S6 --role qa-runner --execution-kind manual --scope <1..{MANUAL_BLOCK_CASES} ids>", text or "")
        check_in("B-K1: ...and the disposition road", "S3 rework, then gate A", text or "")
        ok = c.prepare({"stage": "S6", "role": "qa-runner", "id": "a1", "scope": ["TC-1"], "execution_kind": "automation"})
        check_eq("B-K1 control: the automated case is prepared", ok["dispatch_request"]["scope"], ["TC-1"])
        default = c.prepare({"stage": "S6", "role": "qa-runner", "id": "a1", "execution_kind": "automation"})
        check_eq("B-K1 control: no scope given: the derived automated scope", default["dispatch_request"]["scope"], ["TC-1"])
        # B-K2: validate (apply "dispatch") over a handed automate case -> cause 2; built BEFORE the hand-over, so only `validate` can stop it
        request = dict(ok["dispatch_request"])
        c._handed_cases = lambda: {"TC-1": "profile-x"}
        text = refused_with(lambda: c.apply("dispatch", dict(request)))
        check_in("B-K2: apply('dispatch') refuses a handed automate case (cause 2)", "handed to the person by their recorded word: TC-1", text or "")
        check_in("B-K2: ...leave it out of the automated run", "leave them out of the automated run", text or "")
        check_eq("B-K2: ...and nothing was registered", "a1" in c.state()["dispatches"], False)
        c._handed_cases = lambda: {}
        # B-K3: a case in neither half (manual-human) -> cause 3 with the stage-scope door and the kind
        root3 = temp_dir("qa-rh110-neither-")
        try:
            c3 = MB.real_story(root3, ["automate", "manual-human", "manual-agent"])
            got = c3._half_membership_problems("S6", c3.state(), ["TC-1", "TC-2"], "automation")
            check_eq("B-K3: a manual-human case on the automation half: ONE sentence", len(got), 1)
            check_in("B-K3: ...cause 3 names the case", "not an automated case of the approved plan: TC-2", got[0])
            check_in("B-K3: ...with the stage-scope door and the kind",
                     "`controller.py --operation stage-scope` with `execution_kind: automation` lists the cases the automated half may name", got[0])
            check_eq("B-E3 / B-K3 (manual twin): the same case on the manual half is cause 3 too",
                     [t.split(":")[0] for t in c3._half_membership_problems("S6", c3.state(), ["TC-2"], "manual")], ["not a manual-agent case of the approved plan"])
        finally:
            cleanup(root3)
        # B-K4: the manual half's sentences are byte for byte today's
        c._handed_cases = lambda: {"TC-3": "profile-x"}
        check_eq("B-K4: the manual half's three sentences, byte for byte",
                 c._half_membership_problems("S6", c.state(), ["TC-1", "TC-3", "TC-99", "TC-2"], "manual"),
                 ["disposed automate in the plan: TC-1 - the automated half runs them (`story_step.py start --stage S6 --role qa-runner "
                  "--execution-kind automation`); to check them by hand, the plan row's disposition changes (S3 rework, then gate A)",
                  "handed to the person by their recorded word: TC-3 - nobody dispatches them; leave them out of the block",
                  "not a manual-agent case of the approved plan: TC-99 - `controller.py --operation stage-scope` with `execution_kind: manual` "
                  "lists the cases a block may name"])
        # B-E4 / m1 (t-1452, FR-2): a HANDED case is judged handed FIRST in both halves, so its door is the handed door and never
        # leads to the other half's refusal of the same case. KILLS: the handed test moved back behind the other half's.
        got = c._half_membership_problems("S6", c.state(), ["TC-3"], "automation")
        check_eq("B-E4/m1: a handed manual-agent case on the automation half is cause 2 (handed), not 'a manual block runs them'",
                 [t.split(":")[0] for t in got], ["handed to the person by their recorded word"])
        check_in("B-E4/m1: ...it names the case", "TC-3", got[0])
        c._handed_cases = lambda: {"TC-1": "profile-x"}
        got = c._half_membership_problems("S6", c.state(), ["TC-1"], "manual")
        check_eq("m1 manual twin: a handed automate case on the manual half is cause 2 (handed), not 'the automated half runs them'",
                 [t.split(":")[0] for t in got], ["handed to the person by their recorded word"])
        c._handed_cases = lambda: {"TC-3": "profile-x"}
        check_eq("m1 control: an unhanded manual-agent case on the automation half still gets the manual-block door",
                 [t.split(":")[0] for t in c._half_membership_problems("S6", c.state(), ["TC-2"], "automation")], ["disposed manual-agent in the plan"])
        c._handed_cases = lambda: {}
        # q1: prepare with a derived EMPTY automated half never falls back to the whole approved scope - it refuses, naming the half
        root1 = temp_dir("qa-rh110-q1-")
        try:
            c1 = MB.real_story(root1, ["manual-agent", "manual-agent"])
            text = refused_with(lambda: c1.prepare({"stage": "S6", "role": "qa-runner", "id": "q1", "execution_kind": "automation"})) or ""
            check_in("q1: an empty derived automated half is named", "the automated half of the approved plan is empty", text)
            check_in("q1: ...with the manual door", "--execution-kind manual --scope", text)
            check_not_in("q1: ...and never the membership prefix over cases nobody named", "must name only cases", text)
            check_eq("q1 control: a given scope is still judged by the membership check",
                     "disposed manual-agent in the plan: TC-1" in (refused_with(lambda: c1.prepare(
                         {"stage": "S6", "role": "qa-runner", "id": "q1", "scope": ["TC-1"], "execution_kind": "automation"})) or ""), True)
        finally:
            cleanup(root1)
        c._handed_cases = lambda: {}
        # B-K5: a readable plan with no dispositions -> the declared skip, both halves
        with mock.patch.object(c, "stage_scope", lambda *a, **k: {"derived": False, "scope": [], "reason": "no dispositions"}):
            check_eq("B-K5: no dispositions -> [] for both halves",
                     (c._half_membership_problems("S6", c.state(), ["TC-1", "TC-99"], "manual"),
                      c._half_membership_problems("S6", c.state(), ["TC-1", "TC-99"], "automation")), ([], []))
        # only S6 has two halves; an unknown kind reads nothing
        check_eq("B-E5: an S5 packet and an unknown kind meet no half check",
                 (c._half_membership_problems("S5", c.state(), ["TC-2"], "automation"), c._half_membership_problems("S6", c.state(), ["TC-2"], "")), ([], []))
        # B-K6: `_case_rows` raises -> the unknown is ONE sentence with the person's-word door, for BOTH halves; the S6 waiver passes it
        real_rows = c._case_rows
        for error in (StateConflict("plan is broken"), ValueError("plan rows are not a list")):
            c._case_rows = lambda s, e=error: (_ for _ in ()).throw(e)
            for kind, ids in (("manual", ["TC-2"]), ("automation", ["TC-1"])):
                got = c._half_membership_problems("S6", c.state(), ids, kind)
                check_eq(f"B-K6: {type(error).__name__} on the {kind} half: ONE sentence (the unknown never reads as a pass)", len(got), 1)
                check_in(f"B-K6: ...{kind}: it names the case, the reason and the S6 block",
                         f"the plan could not be read to judge which half {ids[0]} belong to ({error}) - repair the plan (S3 rework) or record "
                         "the person's word (`waiver.py --stage S6 --block \"S6 half membership: unreadable\"`)", got[0])
        pipeline = json.loads((root / "pipeline.json").read_text(encoding="utf-8-sig"))
        waiver.apply_stage_override(pipeline, "S6", "S6 half membership: unreadable", "accept - the person wrote: go on", "2026-10-28T00:00:00")
        (root / "pipeline.json").write_text(json.dumps(pipeline), encoding="utf-8")
        check_eq("B-K6: with the person's word recorded at S6 the same unknown passes, both halves",
                 (c._half_membership_problems("S6", c.state(), ["TC-2"], "manual"), c._half_membership_problems("S6", c.state(), ["TC-1"], "automation")), ([], []))
        pipeline["stage_overrides"][0]["stage"] = "S5"
        (root / "pipeline.json").write_text(json.dumps(pipeline), encoding="utf-8")
        check_eq("B-K6 negative control: a word recorded at another stage passes nothing",
                 len(c._half_membership_problems("S6", c.state(), ["TC-1"], "automation")), 1)
        pipeline["stage_overrides"] = []
        (root / "pipeline.json").write_text(json.dumps(pipeline), encoding="utf-8")
        c._case_rows = real_rows
        # q3 (AR-28, F-8 sibling): `validate`'s empty-scope check does not pass when the plan cannot be read; same road and block as B-K6
        okq = c.prepare({"stage": "S6", "role": "qa-runner", "id": "q3", "scope": ["TC-1"], "execution_kind": "automation"})
        empty = dict(okq["dispatch_request"], scope=[])
        text = refused_with(lambda: c.apply("dispatch", dict(empty))) or ""
        check_in("q3 control: a READABLE plan refuses the empty scope as before", "has an empty scope while the approved plan expects 1", text)
        c._case_rows = lambda s: (_ for _ in ()).throw(StateConflict("plan is broken"))
        text = refused_with(lambda: c.apply("dispatch", dict(empty))) or ""
        check_in("q3: an UNREADABLE plan does not pass an empty scope (the unknown is not a pass)", "the plan could not be read to judge", text)
        check_in("q3: ...with the S6 person's-word block", "S6 half membership: unreadable", text)
        pipeline = json.loads((root / "pipeline.json").read_text(encoding="utf-8-sig"))
        waiver.apply_stage_override(pipeline, "S6", "S6 half membership: unreadable", "accept - the person wrote: go on", "2026-10-28T00:00:00")
        (root / "pipeline.json").write_text(json.dumps(pipeline), encoding="utf-8")
        check_eq("q3: with the person's word recorded the unreadable-plan sentence is gone (read, not dispatched: a pass would register)",
                 c._unreadable_plan_problems(c.state(), "x"), [])
        pipeline["stage_overrides"] = []
        (root / "pipeline.json").write_text(json.dumps(pipeline), encoding="utf-8")
        c._case_rows = real_rows
        # t-1459 (the S5 twin of q3): `validate`'s empty-scope check at S5 over an unreadable plan refuses with its own block,
        # and only a word recorded AT S5 under THAT block passes it (the S6 block and a word at S6 pass nothing).
        ok5 = c.prepare({"stage": "S5", "role": "qa-automator", "id": "q3-s5", "scope": ["TC-1"]})
        empty5 = dict(ok5["dispatch_request"], scope=[])
        text = refused_with(lambda: c.apply("dispatch", dict(empty5))) or ""
        check_in("q3 S5 control: a READABLE plan refuses the empty S5 scope as before", "has an empty scope while the approved plan expects", text)
        c._case_rows = lambda s: (_ for _ in ()).throw(StateConflict("plan is broken"))
        text = refused_with(lambda: c.apply("dispatch", dict(empty5))) or ""
        check_in("q3 S5: an UNREADABLE plan does not pass an empty scope", "the plan could not be read to judge", text)
        check_in("q3 S5: ...with the S5 person's-word block", "--stage S5 --block \"S5 scope: unreadable\"", text)
        check_not_in("q3 S5: ...and not the S6 block", "S6 half membership", text)
        pipeline = json.loads((root / "pipeline.json").read_text(encoding="utf-8-sig"))
        waiver.apply_stage_override(pipeline, "S6", "S5 scope: unreadable", "accept - the person wrote: go on", "2026-10-28T00:00:00")
        (root / "pipeline.json").write_text(json.dumps(pipeline), encoding="utf-8")
        check_eq("q3 S5 negative control: the S5 block recorded at S6 passes nothing at S5",
                 len(c._unreadable_plan_problems(c.state(), "x", "S5")), 1)
        pipeline["stage_overrides"] = []
        waiver.apply_stage_override(pipeline, "S5", "S5 scope: unreadable", "accept - the person wrote: go on", "2026-10-28T00:00:00")
        (root / "pipeline.json").write_text(json.dumps(pipeline), encoding="utf-8")
        check_eq("q3 S5: with the person's word recorded at S5 the unreadable-plan sentence is gone",
                 c._unreadable_plan_problems(c.state(), "x", "S5"), [])
        pipeline["stage_overrides"] = []
        (root / "pipeline.json").write_text(json.dumps(pipeline), encoding="utf-8")
        c._case_rows = real_rows
        # B-K7: a rework of the automation half over a handed case -> cause 2 joins the call's problems
        F.runner(c, root, "S6-qa-runner-3", "automation", ["TC-1"], False)
        c._handed_cases = lambda: {"TC-1": "profile-x"}
        text = refused_with(lambda: c.build_rework_request("S6", "qa-runner", ["TC-1"], "recheck TC-1"))
        check_in("B-K7: an automation rework over a handed case is refused (cause 2)", "handed to the person by their recorded word: TC-1", text or "")
        c._handed_cases = lambda: {}
        check_eq("B-K7 control: with nothing handed the same rework is built",
                 c.build_rework_request("S6", "qa-runner", ["TC-1"], "recheck TC-1")["execution_kind"], "automation")
        # B-K8 (DC1-13, B-AC4): the S6 empty-cases door names stage-scope and one half per call, and no `rework` parameter it lacks
        text = refused_with(lambda: c.build_rework_request("S6", "qa-runner", [], "x")) or ""
        check_in("B-K8: S6 empty --cases: the refusal", "--cases must name at least one case of the approved scope", text)
        check_in("B-K8: ...the door names stage-scope", "`controller.py --operation stage-scope` lists them", text)
        check_in("B-K8: ...and one half per call", "S6 is reworked one half per call", text)
        check_in("B-K8: ...with the manual bound", f"(at most {MANUAL_BLOCK_CASES})", text)
        check_not_in("B-K8: ...and never `execution_kind:` as a rework parameter", "execution_kind:", text)
        # B-K9: S5 empty --cases: the same door, no S6 tail
        text = refused_with(lambda: c.build_rework_request("S5", "qa-automator", [], "x")) or ""
        check_in("B-K9: S5 empty --cases: the door names stage-scope", "`controller.py --operation stage-scope` lists them", text)
        check_not_in("B-K9: ...with no S6 tail", "one half per call", text)
        legacy = dict(c.state(), plan_contract_mode="legacy")
        with mock.patch.object(c, "state", lambda: legacy):
            text = refused_with(lambda: c.build_rework_request("S6", "qa-runner", [], "x")) or ""
        check_not_in("B-K9: a legacy-mode S6 empty --cases has no half tail either", "one half per call", text)
        # B-K10: the named list AT and BEYOND SCOPE_SHOWN (B-E9)
        rootn = temp_dir("qa-rh110-many-")
        try:
            cn = MB.real_story(rootn, ["manual-agent"] * (SCOPE_SHOWN + 1))
            every = [f"TC-{i}" for i in range(1, SCOPE_SHOWN + 2)]
            at = cn._half_membership_problems("S6", cn.state(), every[:SCOPE_SHOWN], "automation")
            beyond = cn._half_membership_problems("S6", cn.state(), every, "automation")
            check_eq("B-K10: AT the limit the whole list is named, no tail", ("and 1 more" in at[0], every[SCOPE_SHOWN - 1] in at[0]), (False, True))
            check_eq("B-K10: BEYOND it the tail says how many are left out", ("and 1 more" in beyond[0], every[SCOPE_SHOWN] in beyond[0]), (True, False))
        finally:
            cleanup(rootn)
        # B-K11 / B-E13: an unstripped id is judged as given, on the safe side (a refusal with a door), both halves
        text = refused_with(lambda: c.prepare({"stage": "S6", "role": "qa-runner", "id": "u1", "scope": [" TC-2 "], "execution_kind": "manual",
                                               "manual_case_ids": [" TC-2 "]})) or ""
        check_in("B-K11: ` TC-2 ` to prepare (manual) is cause 3", "not a manual-agent case of the approved plan:  TC-2 ", text)
        text = refused_with(lambda: c.prepare({"stage": "S6", "role": "qa-runner", "id": "u1", "scope": [" TC-1 "], "execution_kind": "automation"})) or ""
        check_in("B-K11: ` TC-1 ` to prepare (automation) is cause 3", "not an automated case of the approved plan:  TC-1 ", text)
        # B-E7: malformed members never raise; a duplicate is judged once
        got = c._half_membership_problems("S6", c.state(), ["TC-2", "TC-2", 5, "", None, ["TC-3"], "TC-1"], "automation")
        check_eq("B-E7: non-str / empty members skipped, a duplicate judged once: ONE sentence naming TC-2 once", (len(got), got[0].count("TC-2")), (1, 1))
        check_eq("B-E7: a non-list is the caller's to judge", [c._half_membership_problems("S6", c.state(), bad, "automation") for bad in ("TC-2", None, 7, {"TC-2"})], [[]] * 4)
        # B-E8: a bare id two areas hold, or an area-qualified spelling the plan does not key, is compared as written -> cause 3
        check_in("B-E8: an area-qualified spelling of an automated case is refused with the stage-scope door", "not an automated case of the approved plan: area/TC-1",
                 c._half_membership_problems("S6", c.state(), ["area/TC-1"], "automation")[0])
        # B-E10: a record already running or accepted is not re-judged (the check is on new packets only)
        check_eq("B-E10: the accepted automation record is untouched by a later re-disposition", c.state()["dispatches"]["S6-qa-runner-3"]["status"], "accepted")
        # B-K16 (B-AC5): the S4+ rule of `no_move.check_args` refuses an S6 rework with no cases
        facts = {"rework_roles": {"S6": ["qa-runner"]}, "scope": ["TC-1", "TC-2"], "causes": ["ticket_changed", "test_defect"], "rework_stages": ["S6"]}
        good = {"stage": "S6", "role": "qa-runner", "cases": ["TC-1"], "cause": "test_defect"}
        check_eq("B-K16 control: the same args with a case are accepted", check_args(good, facts)[1], "")
        none, why = check_args(dict(good, cases=[]), facts)
        check_eq("B-K16: an S6 rework with `cases: []` is refused, nothing is read as 'all'", (none, "needs at least one of the approved scope" in why), (None, True))
        none, why = check_args({k: v for k, v in good.items() if k != "cases"}, facts)
        check_eq("B-K16: ...and so is one with no `cases` key", (none, "needs at least one of the approved scope" in why), (None, True))
        # B-K6b: a MISSING plan file is an unknown for both halves, on the real reader
        (root / "work" / "test-plan.json").unlink()
        for kind, ids in (("manual", ["TC-2"]), ("automation", ["TC-1"])):
            got = c._half_membership_problems("S6", c.state(), ids, kind)
            check_eq(f"B-K6b: no work/test-plan.json: the {kind} half has ONE unknown sentence", len(got), 1)
            check_in(f"B-K6b: ...{kind}: the S6 block is the door", "S6 half membership: unreadable", got[0])
    finally:
        cleanup(root)


def main():
    rh110_s6_half_membership()
    s6_runner_rework_takes_its_half_from_its_cases()
    a_paid_round_stays_paid_when_its_own_stage_sets_it_aside()
    a_rework_is_never_the_opener_of_a_window()
    s4_rounds_survive_a_changed_case_list()
    next_never_waits_for_an_agent_that_was_never_launched()
    a_working_agent_is_still_waited_for()
    a_host_receipt_is_evidence_too()
    a_host_that_records_nothing_is_left_alone()
    a_recorded_denial_closes_it_even_with_a_receipt()
    a_story_under_no_project_closes_nothing()
    a_refused_dispatch_leaves_no_receipt()
    rework_is_built_from_the_accepted_work()
    a_repair_request_carries_the_current_pinned_versions()
    the_binding_of_a_repair_follows_the_pins_it_can_find()
    a_paused_repair_resumes_with_its_original_request()
    a_never_started_repair_relaunches_with_its_original_request()
    a_relaunch_of_a_test_defect_round_is_not_a_second_round()
    a_record_without_a_binding_falls_back_to_the_four_fields()
    a_continuation_packet_takes_its_paths_from_the_stamp_and_its_plan_rows_by_presence()
    a_made_up_relaunch_is_refused_and_a_new_dispatch_is_judged_as_before()
    a_continuation_is_tied_to_the_dispatch_it_names()
    a_completion_cannot_bind_a_record_that_has_no_binding()
    no_bare_key_error_reaches_a_reader()
    the_cli_records_a_gate_decision_and_a_rework()
    rework_takes_the_persons_words_from_a_file()
    a_person_rework_carries_the_stamp()
    the_replay_sets_aside_what_runs_after_the_rework()
    a_stage_closed_by_a_code_only_receipt_is_lowered()
    a_skipped_stage_is_never_touched()
    a_ticket_changed_rework_is_not_stamped()
    a_closed_story_is_not_stamped()
    a_round_inside_an_open_stage_is_not_stamped()
    an_approved_gate_decision_after_the_stage_goes_stale()
    a_forged_stamp_is_refused_whole()
    the_validator_stops_where_the_builder_stops()
    the_projection_forgets_the_run_a_lowered_stage_was()
    the_stamp_is_applied_once_and_never_travels_in_a_continuation()
    staling_the_critic_does_not_reset_the_repair_cap()
    a_second_person_rework_of_a_pending_stage_stamps_its_own_window()
    a_rework_without_words_is_todays_flow()
    the_person_words_mark_follows_the_words_file()
    a_stamp_with_nothing_to_set_aside_is_no_stamp()
    only_one_dispatch_runs_at_a_time_and_a_second_rework_stamps_again()
    a_designer_rework_after_gate_a_stales_the_critic_and_the_gate()
    finish("test_controller_rework")


if __name__ == "__main__":
    main()
