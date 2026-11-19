"""stage_close.py - the closes by code a stage takes when no role is left to run it, for both roads (FV3-22, AR-15, P31).

ONE survivor of three steps the Driver used to hold alone: the consumer rule (a stage judged by its consumer role closes by the consumer's
record or a person's pass, and at an `await_at` site awaits it), the manual-half close of S6 (reducer, consumer step, close) and the code
close (completed check, finalize, `code_only` receipt, passed-over findings, stage record). The Driver's methods of the same names
delegate here; no copy of a body stays in the driver modules.

A ROAD is the object a body runs over: the Driver is one (every member below exists on it). Each free function reaches every step through
the road member of the same name the old body called as `self.<member>`, never through its free twin, so a test stub on a Driver
attribute keeps its effect (E-M6). Road members: `task`, `task_root`, `project`, `dry`, `controller_state()`, `pipeline()`,
`py(script, *args, check, expect)`, `owe_row(...)`, `accepted_at(author)`, `consumer_pending(stage)`, `person_pass(...)`,
`consumer_person_pass(...)`, `consumer_need_record(stage, site)`, `consumer_await(...)`, `close_by_code(...)`, `close_receipt(...)`,
`file_passed_over(...)`, `record_close(...)`, `manual_request_paths(cases)`, and for S7 (FV3-26) `plugin`, `failures_to_triage(awaiting)`,
`s7_close_places(why)`, `s7_investigation_gate()`, `s7_investigation_dispatch(targets, budget)`. The skill road's road is `SkillRoad` (FV3-22-2).

This module imports no `story_step` and no `driver_*` (so no cycle and no `allowed_importers` row, L11); the package modules it needs
are imported inside the functions, as `waiver` is by the driver parts.
"""

import hashlib
import json
import subprocess
import sys
from pathlib import Path

BY_PERSON = "by: person"     # the quote prefix of a driver accept that a person's word made (`person_pass` writes it, `Driver.consumer_close_words` reads it): one definition (AR-13)

# The data of the consumer rule, one definition (E-M9). The Driver adds the two callables `closes_when` and `rework_complete`, which only
# `Driver.consumer_awaits` and the rework code read.
# `await_at`: the close sites where a missing record means AWAIT the consumer, not refuse (B1, t-1128): nothing is left to dispatch
# there, so no other road would ever ask the consumer (S7 keeps its own road `s7_await_scribe`).
CONSUMER_ROUTES = {
    "S6": {"consumer_stage": "S7", "author": "qa-runner", "who": "failure analyst", "what": "the runner's handoff",
           "await_at": ("manual_close",),
           "awaits": "the runner stopped; S6 awaits the acceptance of {consumer}, which judges the run report and the case records from its own form"},
    "S7": {"consumer_stage": "S8", "author": "qa-failure-analyst", "who": "doc scribe", "what": "the analyst's handoff",
           "await_at": (),
           "awaits": "the failure analyst stopped; S7 awaits the acceptance of {consumer}, which judges the triage and the bug drafts from its own form"},
}


class Refused(Exception):
    """The refusal of a close step, shared by every road. NOT a Refusal of the driver and NOT a ValueError: the Driver's delegates convert it
    once (`Refusal(str(exc), title=exc.title)`), the skill road prints it. `title` names a refusal the caller must tell from its neighbours
    (`code_only_evidence`)."""

    def __init__(self, text: str, title: str = ""):
        super().__init__(text)
        self.title = str(title or "")


def s6_automation_settled(state, auto_scope) -> bool:
    """CK2: the automated half of S6 is settled - it has no scope, or an S6 dispatch is accepted whose `execution_kind` is `automation` (or
    empty: a dispatch recorded before the field existed)."""
    done = [d for d in ((state or {}).get("dispatches") or {}).values() if isinstance(d, dict) and d.get("stage") == "S6" and d.get("status") == "accepted"]
    return not list(auto_scope or []) or any(d.get("execution_kind") == "automation" or not d.get("execution_kind") for d in done)


def person_word_door(task: str, stage: str) -> str:
    """The recording command of a person's `stage acceptance` word, with the words by file: the one renderer of this door (`waiver.py`
    refuses `--stage/--block` without `--decision` or `--words-file`, FR-2)."""
    import acceptance
    import person_words
    return person_words.door(f'waiver.py --task {task} --stage {stage} --block "{acceptance.STAGE_ACCEPTANCE_PHRASE}"')


def consumer_pending(road, stage: str) -> bool:
    """True when `stage` has a consumer, is not completed, its author ran, and an `accept` record stands for the author's LAST dispatch of
    the current life: the stage is owed its close (a restart between the consumer's record and the close lands here)."""
    import acceptance
    if not acceptance.consumer_of(stage):
        return False
    state = road.controller_state()
    if ((state.get("stages") or {}).get(stage) or {}).get("status") == "completed":
        return False
    return acceptance.accepted_for(road.pipeline(), stage, acceptance.stage_author_dispatch(state, acceptance.stage_def_of(stage)))


def accepted_at(task_root, author: str) -> str:
    """When the dispatch `author` was last accepted, as `controller.stamp_utc` (the last `accept` event of the controller's store); `""`
    when it cannot be read (no event, no store). The ONE reader of that time (B-20 F1): a word dated before it was said about work the
    person had not yet seen."""
    try:
        from controller import Controller, stamp_utc
        times = [e.get("created_at") for e in Controller(task_root).store.read()
                 if e.get("type") == "accept" and (e.get("payload") or {}).get("id") == author]
        return stamp_utc(times[-1]) if times else ""
    except Exception:  # noqa: BLE001 - an acceptance time that cannot be read is the safe side: the word is not honoured
        return ""


def person_pass(road, stage: str, author: str, line: str, answer: str = "", since: str = "") -> dict:
    """The body of the pass (F3, B-6): the person's word - `answer` (given by the caller) or a live `waiver.py --block` that passes `line`
    (`waiver.split_overridden`, the ONE reader, AR-13) - is RECORDED as the driver accept of `author` for `stage` (the one writer,
    `stage_done.py --acceptance`), and then True. `since` (non-empty): a waiver is honoured only when its `at` is LATER than `since` -
    both read through `controller.stamp_utc`; an `at` or a `since` that cannot be read is not honoured (a word never accepts an author
    dispatch the person never saw, FR-4). Returns the honoured entry (`{"decision": <words>, "at": <when or "">}`) once the pass is
    recorded, `{}` when nothing passes: no `author` -> `{}`, no accept record without an author dispatch."""
    import acceptance
    if not author:
        return {}

    def stamp(value) -> str:
        """One normal form for an `at` / `since`: `controller.stamp_utc` of the epoch second; `""` when it is no time (or has no zone)."""
        import stage_done
        from controller import stamp_utc
        if isinstance(value, str):
            moment = stage_done.iso_with_zone(value)
            try:
                return stamp_utc(moment.timestamp()) if moment is not None else ""
            except (OverflowError, OSError):
                return ""
        return "" if isinstance(value, bool) or value is None else stamp_utc(value)
    words = " ".join(str(answer or "").split())
    heard = {}
    if not words:
        import waiver
        _blocking, passed = waiver.split_overridden([line], road.pipeline(), stage)
        if passed and since and not (stamp(passed[0].get("at")) > stamp(since) > ""):
            passed = []
        heard = dict(passed[0]) if passed else {}
        words = " ".join(str(heard.get("decision") or "").split())
    if not words:
        return {}
    if getattr(road, "dry", False):      # B-20 F2: `--dry-run` runs nothing and writes nothing - the pass is only said
        print(f"{stage}: dry run - a person's word would pass the acceptance of {author}; nothing is recorded")
        return {}
    road.py("stage_done.py", "--task", road.task, "--stage", stage, "--acceptance", f"work/handoffs/{author}.yaml",
            "--acceptor", acceptance.DRIVER_ACCEPTOR, "--verdict", "accept", "--quote", f"{BY_PERSON} - " + words[:500], check=True,
            expect=f"the person's pass recorded as the acceptance of {stage} for {author}")
    print(f"{stage}: a person's word passes the acceptance of {author}; recorded as a driver accept (by: person)")
    return {"decision": words, "at": heard.get("at") or ""}


def consumer_person_pass(road, stage: str, author: str, answer: str = "") -> bool:
    """P13 (M3 of t-1860): the person's word moves the factory. True when an `accept` record stands for `author` already, or when a
    person's word passes the acceptance - `answer` (the words of a recorded `close` answer, given by the caller) or a live
    `waiver.py --block` of the stage-acceptance phrase (`acceptance.STAGE_ACCEPTANCE_PHRASE`) of this stage (`waiver.split_overridden`, the one reader) - and then the pass is RECORDED
    first: `stage_done.py --acceptance <the author's form> --acceptor driver --verdict accept --quote "by: person - <words>"`, the one
    writer, so every reader of the record (the close sites, `awaits_acceptance`, `stage_done`) sees it. False: nothing passes it.
    B-20 F1 (FR-4), at EVERY site: a live waiver is honoured only when its `at` is LATER than the acceptance of `author` (`accepted_at`);
    a time that cannot be read is not honoured. `answer` is a fresh word (given by the caller this turn) and is exempt. The Driver's
    delegate carries the WHOLE pass as the `retry` of a refusal of the recording, so the finding is filed after a retry too (P13)."""
    import acceptance
    if not author:
        return False
    if acceptance.accepted_for(road.pipeline(), stage, author):
        return True
    line = f"{acceptance.STAGE_ACCEPTANCE_PHRASE}: no accept record stands for {author}"
    since = ""
    if not " ".join(str(answer or "").split()):
        since = road.accepted_at(author)
        if not since:
            return False
    heard = road.person_pass(stage, author, line, answer, since=since)
    if not heard:
        return False
    # P13: a pass by the person's word is a finding, filed once per stage and author dispatch (the key makes a second write safe)
    road.owe_row("project_decisions.py", "--root", str(road.project), "add-finding",
                 "--essence", f"{stage} acceptance of {author} passed on the person's word: {str(heard.get('decision') or '')[:500]}",
                 "--scope", "local-calibration", "--witness", f"{stage} person's word at {heard.get('at') or ''}",
                 "--idempotency-key", f"stage-acceptance-pass:{road.task}:{stage}:{author}",
                 what="the finding about the stage acceptance you passed", stage=stage)
    return True


def need_record(road, stage: str, site: str) -> bool:
    """The close sites of a stage with a consumer (S6: `s6_reentry`, `s6_reprobed_close`, `manual_close`; S7: `s7_close`): with an author that
    ran, a close needs the `accept` record of the author's LAST dispatch - or a person's pass (`consumer_person_pass`, M3). A refusal names
    the missing record and the door (FR-1, FR-2: the person's-word door carries its words file, `person_word_door`); with no consumer, no
    author dispatch, or the stage completed already, nothing (False). At a site the route's `await_at` lists (S6 `manual_close`), a missing
    record makes the stage AWAIT the consumer instead of refusing (B1): the marker `pipeline.acceptance_awaits[stage] = author` is written
    only when `awaits_acceptance` (the one reader) would then name exactly `author`, and only over a readable pipeline; otherwise today's
    refusal. True = the stage awaits; nothing is closed. POSITION: after the record and the person's pass (they always win), before the
    raise: a stage with a consumer is never closed without either."""
    import acceptance
    consumer = acceptance.consumer_of(stage)
    if not consumer:
        return False
    state = road.controller_state()
    if ((state.get("stages") or {}).get(stage) or {}).get("status") == "completed":
        return False
    author = acceptance.stage_author_dispatch(state, acceptance.stage_def_of(stage))
    if not author or road.consumer_pending(stage) or road.consumer_person_pass(stage, author):
        return False
    route = CONSUMER_ROUTES.get(stage) or {}
    if site in route.get("await_at", ()) and road.consumer_await(stage, author, state, route):
        return True
    raise Refused(f"{stage} cannot be closed at {site}: no accept record of {consumer} stands for {author}. The consumer judges "
                  f"{route.get('what', 'the handoff')} from its own form (`stage_done.py --task {road.task} "
                  f"--stage {stage} --acceptance work/handoffs/<{consumer} dispatch>.yaml`), or a person's word passes it "
                  f"(`{person_word_door(road.task, stage)}`).")


def mark_awaiting(road, stage: str, author: str, state: dict, route: dict) -> bool:
    """B1: the stage AWAITS the consumer - the marker `pipeline.acceptance_awaits[stage] = author` is written (once, the one `atomic_json` of
    it, AR-14) only when `awaits_acceptance` (the one reader) would then name exactly `author`, and only over a readable pipeline. False on
    an unreadable pipeline or when the wait would not hold (the caller's refusal stays the only raise). Named apart from
    `Driver.consumer_awaits`, which is another thing (E-M8)."""
    import acceptance
    pipeline = road.pipeline()
    if not (isinstance(pipeline, dict) and pipeline):
        return False
    marks = pipeline.get("acceptance_awaits") if isinstance(pipeline.get("acceptance_awaits"), dict) else {}
    marked = dict(pipeline, acceptance_awaits=dict(marks, **{stage: author}))
    if acceptance.awaits_acceptance(state, stage, marked) != author:
        return False
    if acceptance.awaits_acceptance(state, stage, pipeline) != author:
        from event_store import atomic_json
        atomic_json(road.task_root / "pipeline.json", marked)
    print(f"{stage}: nothing is left to dispatch; {stage} awaits the acceptance of {acceptance.consumer_of(stage)} for {author} "
          f"(the {route.get('who', 'consumer')} is let in; its record closes {stage})")
    return True


def manual_half_close(road, done: list, refused: list) -> bool:
    """No block is left to dispatch (every case is done, or none could be prepared): the manual half closes with no runner - the receipt is
    `code_only`, written over a `run-report.json` the reducer has just written, then `stage_done`. The words say how many were checked and
    which were not. A reducer that fails is a refusal: nothing is closed over a report nobody could build. ORDER (FV3-21 K6.c, the S7
    twin's order): the reducer, the consumer step, the close. The consumer step closes by the consumer's record, or - at this site, B1 -
    writes the awaiting marker and returns with nothing closed; the marker is written only over a run report the reducer has just written
    (AR-21), and a reducer failure writes none. `done`: the cases checked by an agent; `refused`: `(case, why)` pairs. True = closed,
    False = S6 awaits the consumer."""
    reason = (f"the manual half of S6: {len(done)} case(s) checked by an agent by hand, {len(refused)} not checked"
              + (": " + ", ".join(case for case, _why in refused) if refused else ""))
    code, out = road.py("finalize_task.py", str(road.task_root))
    if code:
        raise Refused(f"S6 manual half: finalize_task.py exit {code}: " + (out.splitlines()[-1] if out else ""))
    if road.consumer_need_record("S6", "manual_close"):         # X7-6 / B1: the consumer's record closes S6; with none, S6 awaits it
        return False
    road.close_by_code("S6", reason, ["work/run-report.json"] + road.manual_request_paths([case for case, _ in refused]),
                       finalize=False, site="s6.manual_close")
    return True


def close_by_code(road, stage: str, reason: str, evidence: list, *, finalize: bool, site: str = "", digest: str = "", role: str = "",
                  journal: bool = False, tail=(), fresh=None) -> bool:
    """THE helper of "a stage closed by code after its post-role loop" (t-698 §18.5; S7's two closes and the close after its
    repairs, and the three S6 closes, which pass `finalize=False` after their own `finalize_task` call and its own refusal text;
    C2-8 marks every one with its `site`): `finalize_task` when `finalize` (BEFORE the receipt, so the receipt hashes what finalize
    wrote), the `code_only` receipt (`close_receipt`), then the `stage_done` record (`record_close`). A stage the controller holds
    `completed` already is NOT closed again (state is read first, never a refusal's words): no finalize, no second receipt. A
    `stage_done` refused after a successful `code_only` is a refusal whose retry repeats `record_close` - the write AND its tail.
    `fresh`: a precondition checked after finalize, before the receipt; False records nothing and returns False."""
    held = ((road.controller_state().get("stages") or {}).get(stage) or {}).get("status")
    if held == "completed":
        print(f"{stage}: the controller holds it completed already; no second receipt is written")
        return True
    if finalize:
        code, out = road.py("finalize_task.py", str(road.task_root))
        if code:
            raise Refused(f"{stage} close: finalize_task.py exit {code}: " + (out.splitlines()[-1] if out else ""))
    if fresh is not None and not fresh():
        return False
    receipt = road.close_receipt(site, stage, reason, evidence)
    road.file_passed_over(stage, receipt)
    road.record_close(site, stage, "--status", "done", *(["--role", role] if role else []),
                      "--digest", digest or reason, *([] if journal else ["--no-journal"]), tail=tail, receipt=receipt)
    return True


def code_only_request(road, stage: str, reason: str, evidence: list) -> dict:
    """The request of the controller's `code_only` operation for `stage` (the one builder of it, AR-14). Every evidence file that exists is
    hashed with the controller's own form (`hashlib.sha256` of the bytes, judged by its `_ref_issues`: no second judge of the hash, E-M5);
    `Refused(title="code_only_evidence")` when none exists, so `close_receipt` tells it from the controller's own refusal by the field."""
    refs = []
    for rel in evidence:
        path = road.task_root / rel
        if path.is_file():
            refs.append({"path": rel, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
    if not refs:
        raise Refused(f"code-only {stage}: none of {evidence} exists to stand as evidence", title="code_only_evidence")
    state = road.controller_state()
    n = len([e for e in (state.get("dispatches") or {}) if str(e).startswith(f"{stage}-code-only")]) + 1
    return {"id": f"{stage}-code-only-{n}", "stage": stage, "reason": reason,
            "evidence_refs": refs, "expected_revision": state.get("revision", 0),
            "idempotency_key": f"code_only:{stage}:{n}"}


def file_passed_over(road, stage: str, receipt) -> None:
    """TR1-9 B4 (AR-27): the work a code close passed over (`stages[stage].passed_over`, written by the controller's `code_only`
    receipt: `returned, never accepted`, `abandoned`, `stopped, never accepted`) is a FINDING, one per dispatch, idempotent by
    (task, stage, dispatch). Position: right after the receipt, before the stage record, so a refused record cannot lose the name;
    the report reads the same names from the stage entry (`report_facts._passed_over_gap`). An unreadable state files nothing here
    and the stage entry still carries the names."""
    state = road.controller_state()
    stages = state.get("stages") if isinstance(state, dict) else None
    entry = stages.get(stage) if isinstance(stages, dict) else None
    rows = state.get("dispatches") if isinstance(state, dict) and isinstance(state.get("dispatches"), dict) else {}
    named = entry.get("passed_over") if isinstance(entry, dict) else None
    for item in named if isinstance(named, list) else []:
        if not isinstance(item, dict) or not item.get("id"):
            continue
        ident = str(item["id"])
        who = str((rows.get(ident) or {}).get("role") or "a role") if isinstance(rows.get(ident), dict) else "a role"
        road.owe_row("project_decisions.py", "--root", str(road.project), "add-finding",
                     "--essence", f"{stage} was closed by code over the work of {who} ({ident}): {item.get('label') or 'never accepted'}"[:500],
                     "--scope", "local-calibration", "--witness", f"close receipt {receipt}",
                     "--idempotency-key", f"close-passed-over:{road.task}:{stage}:{ident}",
                     what="the finding about work a code close passed over", stage=stage)


def record_door(task: str, stage: str, args) -> str:
    """The `door:` line that completes a stage record a refusal left unwritten (E9): the ONE builder, read by `SkillRoad.record_close` and
    `story_step._s6_reentry`, so the same world prints the same command on both (t-1558 F1)."""
    command = " ".join(f'"{a}"' if any(ch.isspace() for ch in str(a)) else str(a) for a in args)
    return f'door: python "${{CLAUDE_PLUGIN_ROOT}}/scripts/stage_done.py" --task {task} --stage {stage} {command}'


def stage_record_written(task_root, controller, stage: str) -> bool:
    """True when the stage record of `stage` is written after the controller completed it by a `code_only` receipt: `stage_done.stage_finished_at`
    (the one reader of `finished`) is present and NOT EARLIER than the time of the stage's last `code_only` event (equal reads as written). The
    pipeline's `status` is no witness: the projection writes `done` from the controller on every apply (t-1209 F4-1). ERROR DIRECTION: any
    time that cannot be read, a missing event or an unreadable store reads as False (not written), never as written (FR-59, AR-28)."""
    import stage_done
    from datetime import datetime
    from controller import stamp_utc
    try:
        events = [e for e in controller.store.read() if e.get("type") == "code_only" and (e.get("payload") or {}).get("stage") == stage]
        completed = datetime.fromisoformat(stamp_utc(events[-1].get("created_at")))
        finished = stage_done.stage_finished_at(stage_done.read_pipeline(Path(task_root) / "pipeline.json"), stage)
        return finished is not None and finished >= completed
    except Exception:  # noqa: BLE001 - a time that cannot be read is the safe side: the record counts as not written
        return False


def s7_failures_to_triage(task_root, awaiting: str = "") -> str:
    """The reasons S7 has something to triage, `"; "`-joined (`""` = nothing to triage); the ONE body of it (AR-13, FV3-26), the Driver's
    `failures_to_triage` delegates here. Reads only `task_root`. A halted run (`broken_run`, `timeout`, `env_blocked`) or a `not_executed`
    with neither an S6 code-only receipt nor a target a role can triage raises `Refused` before any register write."""
    import hooklib
    task_root = Path(task_root)
    report = hooklib.read_json(task_root / "work/run-report.json", {})
    status = report.get("execution_status")
    if status not in ("passed", "failed"):
        # t-305 N1 (Q19 a): `not_executed` is also what S6 leaves on purpose when it closes on a CODE-ONLY receipt
        # (nothing to execute, or everything handed to a person); S7 reads that report. U7 7a: and what a FINISHED S6
        # leaves over a manual-only story (an `inconclusive` or `unprepared` walk) - `triageable_not_executed`, the one
        # predicate delivery's `run_reasons` reads too. Still refused: an S6 halt, and a `not_executed` with neither
        # receipt nor a target a role can triage; the refusal below stands word for word. Read only on this branch.
        import s7_pretriage
        if not (status == "not_executed" and (s7_pretriage.s6_closed_by_code(task_root)
                                              or s7_pretriage.triageable_not_executed(task_root, awaiting=awaiting))):
            raise Refused(f"S7 entry: run-report.json execution_status is `{status}` — nothing to triage yet; "
                          "the S6 halt that produced it stands")
    totals = report.get("current_totals") or report.get("totals") or {}
    reasons = []
    if int(totals.get("failed") or 0):
        reasons.append(f"failed={totals.get('failed')}")
    # t-309: the one definition of a failure that needs triage (contract.triage_targets), shared with the
    # reducer and the S7 handover check - a manual `inconclusive` or `error` is a failure here as there.
    import contract
    targets = contract.triage_targets(report)
    bad = sorted(targets["manual"]) + sorted(targets["unnamed_manual"])
    if bad:
        reasons.append("manual " + ",".join(bad))
    # P26 / RN1-10 (AR-28): a runner's observation, whatever its check's result, wants the analyst's verdict - a green check
    # with an observation dispatches the analyst; a report with none reads exactly as before
    if targets["observations"]:
        reasons.append("manual observations " + ",".join(sorted(targets["observations"])))
    # t-323 C2: a failed RESULT row with no id sits in `unnamed` beside the nameless manual checks, and was worded
    # "manual" with them - a failure of the automated run named as a manual check; it gets its own words
    nameless = sorted(targets["unnamed"] - targets["unnamed_manual"])
    if nameless:
        reasons.append(f"{len(nameless)} failed result row(s) with no id")
    if targets["results"] and not int(totals.get("failed") or 0):
        reasons.append("failed results " + ",".join(sorted(targets["results"])))
    # U7 7b-A: a coded `report_unread` row is a target the analyst reads from the log; reasons are never "" over one, so
    # the S7 close cannot run over it (an `unread` target is no `s7.no_failures`)
    if targets["unread"]:
        reasons.append("results the run could not read " + ",".join(sorted(targets["unread"])))
    manifest = hooklib.read_json(task_root / "work/automation-manifest.json", {})
    if "contradicts_requirement" in json.dumps(manifest.get("unresolved") or []):
        reasons.append("contradicts_requirement rows")
    return "; ".join(reasons)


def gap_reason_text(name: str) -> str:
    """t-1991 U3a: the text `place_answers.close_unsettled` is given, chosen by NAME from `references/place-answers.json` `gap_reason_names`
    (a reorder of the list cannot give a false text). `""` after one printed line when the texts cannot be read: `close_unsettled` then
    refuses and `s7_close_places` prints one line (E-M4)."""
    try:
        import place_answers
        return place_answers._data()["gap_reason_names"][name]
    except Exception as exc:  # noqa: BLE001 - the same printed line as before the move
        print(f"S7: the reason for the places nobody settled could not be chosen ({type(exc).__name__}: {exc})")
        return ""


def s7_close_places(road, why: str) -> list:
    """t-1991 U3a: ONE call at each S7 code closer, BEFORE `s7_investigation_gate` (INVARIANT: a place is never both a settle
    gap and an investigation gap; `close_unsettled` never writes a plain `open` place, and its `by` is outside the investigation's
    prefix). The ids of the register lines written. The list that could not be read whole is one printed line and the close still runs
    on what was read; an exception is one printed line and S7 goes on - it never reads as "no places" (P1, AR-28)."""
    try:
        import place_answers
        found = place_answers.places(road.task_root)
        if found["unreadable"]:
            print("S7: the places to settle could not be computed whole: " + "; ".join(f"{rec}: {w}" for rec, w in found["unreadable"]))
        printed: list = []
        written = place_answers.close_unsettled(road.task_root, why, printed, found=found)
    except Exception as exc:  # noqa: BLE001
        print(f"S7: the places nobody settled could not be recorded as gaps ({type(exc).__name__}: {exc}); S7 goes on")
        return []
    for line in printed:
        print(f"S7: {line}")
    if written:
        print(f"S7: {len(written)} place(s) nobody settled were recorded as coverage gaps: {why}")
    return written


def s7_investigation_gate(road) -> tuple:
    """What S7 does about the observations the run left open BEFORE it closes by code (P2 M3): `(verdict, suffix)`, verdict
    `proceed` | `dispatched` | `dispatch_owed` | `wait`, suffix the text added to the close reason and digest (`""` when nothing happened).
    Called ONLY at the S7 code closers, never at the stage entry. `wait`: the caller returns WITHOUT a close (a running pass; the next
    `where` resumes it). A stage the controller holds `completed` is never worked on. An exception of the investigation code is one printed
    line and today's close (P1, F-5). The decision itself is `investigation.decision` (pure); the register is written only through
    `investigation.project` / `close_gaps`. What the role still decides: the investigation itself (targets worth a probe, what the probe
    shows, how it is recorded). The pass is started by the road (`s7_investigation_dispatch`): the Driver runs it, the skill road says it is owed."""
    held = ((road.controller_state().get("stages") or {}).get("S7") or {}).get("status")
    if held == "completed":
        return "proceed", ""
    try:
        import investigation
        budget, _ = investigation.load_budget(road.plugin)
    except Exception as exc:  # noqa: BLE001
        print(f"S7: the investigation could not be loaded ({type(exc).__name__}: {exc}); S7 closes as it did without it")
        return "proceed", ""
    try:
        investigation.project(road.task_root, "S7")
    except Exception as exc:  # noqa: BLE001
        print(f"S7: the observations the run left open could not be projected ({type(exc).__name__}: {exc}); "
              "S7 goes on with what the register holds")
    try:
        word, why = investigation.decision(road.task_root, road.controller_state(), road.pipeline(), budget)
        targets = (investigation.open_targets(road.task_root, budget)["unresolved"] if word == "dispatch" else [])
    except Exception as exc:  # noqa: BLE001
        print(f"S7: the investigation could not be decided ({type(exc).__name__}: {exc}); S7 closes as it did without it")
        return "proceed", ""
    if word == "wait":
        print(f"S7: the investigation {why} is running; S7 is not closed over it")
        return "wait", ""
    if word == "none":
        if why:
            print(f"S7: {why}")
        return "proceed", ""
    printed: list = []
    if word == "gaps":
        try:
            if why == investigation.WHY_TEXTS[0]:
                print("S7: the investigation budget cannot be used (" + "; ".join(investigation.budget_problems(budget)) + ")")
            g = len(investigation.close_gaps(road.task_root, why, printed, budget=budget))
        except Exception as exc:  # noqa: BLE001
            print(f"S7: the observations the run left open could not be recorded as gaps ({type(exc).__name__}: {exc}); "
                  "S7 closes as it did without it")
            return "proceed", ""
        for line in printed:
            print(f"S7: {line}")
        return "proceed", (f"; {g} observation(s) the run left open were not investigated: {why}" if g else "")
    return road.s7_investigation_dispatch(targets, budget)


def s7_code_close(road, kind: str) -> str:
    """The shared tail of the S7 close by code at `s7.no_failures` (FV3-26; `kind` is `no_failures` only in this node): the places nobody
    settled become gaps, THEN the investigation gate (a place is never both gaps), then the `code_only` receipt over the run report (and the
    register when it exists) with the stage record and the `dispatch_skipped` journal row. POSITION INVARIANT: after the caller's
    `failures_to_triage` (a halted run raises before any register write) and before the receipt (which hashes the register a pass wrote).
    Returns `wait` (a pass running: nothing closed), `dispatch_owed` (the road owes the pass: nothing closed) or `closed`."""
    road.s7_close_places(gap_reason_text(kind))      # t-1991 U3a: BEFORE the gate (a place is never both gaps)
    verdict, suffix = road.s7_investigation_gate()
    if verdict == "wait":
        return "wait"
    if verdict == "dispatch_owed":
        return "dispatch_owed"
    register = ["work/exploratory-findings.jsonl"] if (road.task_root / "work" / "exploratory-findings.jsonl").is_file() else []
    road.close_by_code("S7", "no failures — nothing to triage" + suffix, ["work/run-report.json"] + register,
                       site="s7.no_failures", finalize=False,
                       tail=[["--event", "dispatch_skipped", "--task", road.task, "--reason", "S7: no failures to triage"]])
    return "closed"


class SkillRoad:
    """The road of the skill's own `story_step.py start` (FV3-22-2, P31): the members the free functions above reach their steps through
    (module docstring), over the story's controller and the scripts run as `story_step._run` runs them (the story_step process's cwd and
    environment). `dry` is always False: the skill road has no dry run. The Driver is the other road; no member is copied from it - each
    free body is the one survivor (AR-15)."""
    dry = False

    def __init__(self, task: str, task_root, controller):
        import hooklib
        self.task = task
        self.task_root = Path(task_root)
        self._ctl = controller
        self.project = hooklib.project_root()

    def controller_state(self) -> dict:
        return self._ctl.state()

    def pipeline(self) -> dict:
        import hooklib
        return hooklib.read_json(self.task_root / "pipeline.json", {}, kind=dict, errors=Exception)

    def controller(self, op: str, *args, input_data=None):
        """The controller's own `apply` (it enriches a `code_only` receipt with the passed-over work, so both roads write the same receipt)."""
        return self._ctl.apply(op, input_data)

    def py(self, script: str, *args, check: bool = False, expect: str = "") -> tuple:
        """Run one factory script; `(exit code, stdout+stderr)`. A script that is not in this build is exit 127, never a skipped success
        (AR-28: a close is not reported over a step that did not run - the opposite error direction from `story_step._run`). `check=True`:
        a non-zero exit raises `Refused`."""
        path = Path(__file__).resolve().parent / script
        if not path.is_file():
            code, out = 127, f"{script} is not in this build"
        else:
            done = subprocess.run([sys.executable, "-B", str(path), *[str(a) for a in args]], capture_output=True, text=True,
                                  encoding="utf-8", errors="replace")
            code, out = done.returncode, (done.stdout + ("\n" + done.stderr if done.stderr.strip() else "")).strip()
        if check and code:
            raise Refused(f"{script} exit {code}: " + (out.splitlines()[-1] if out else "") + (f" ({expect})" if expect else ""))
        return code, out

    def owe_row(self, script: str, *args, what: str, stage: str = "") -> None:
        """A journal row the close owes: a failure is one `note:` line and never a raise (the close is recorded already)."""
        code, out = self.py(script, *args)
        if code:
            print(f"note: {what} was not filed: " + (out.splitlines()[-1] if out else f"{script} exit {code}"))

    def accepted_at(self, author: str) -> str:
        return accepted_at(self.task_root, author)

    def consumer_pending(self, stage: str) -> bool:
        return consumer_pending(self, stage)

    def person_pass(self, stage: str, author: str, line: str, answer: str = "", since: str = "") -> dict:
        return person_pass(self, stage, author, line, answer, since)

    def consumer_person_pass(self, stage: str, author: str, answer: str = "") -> bool:
        return consumer_person_pass(self, stage, author, answer)

    def consumer_need_record(self, stage: str, site: str) -> bool:
        return need_record(self, stage, site)

    def consumer_await(self, stage: str, author: str, state: dict, route: dict) -> bool:
        return mark_awaiting(self, stage, author, state, route)

    def close_by_code(self, stage: str, reason: str, evidence: list, **more) -> bool:
        return close_by_code(self, stage, reason, evidence, **more)

    def close_receipt(self, site: str, stage: str, reason: str, evidence: list) -> str:
        request = code_only_request(self, stage, reason, evidence)
        self.controller("code_only", input_data=request)
        return request["id"]

    def file_passed_over(self, stage: str, receipt) -> None:
        file_passed_over(self, stage, receipt)

    def record_close(self, site: str, stage: str, *args, tail=(), receipt: str = "") -> None:
        """The stage record: `stage_done --stage <stage> <args>`, then each `tail` row through `log_append`. A refused record raises `Refused`
        whose text ENDS with the command that completes it (E9: the receipt is never lost silently)."""
        try:
            self.py("stage_done.py", "--task", self.task, "--stage", stage, *args, check=True)
        except Refused as exc:
            raise Refused(f"{exc}\n{record_door(self.task, stage, args)}", title=exc.title) from None
        for row in tail:  # FV3-29: a failed tail row was dropped silently (q3c); now one note, the loop goes on, never a raise
            self.owe_row("log_append.py", *row, what=f"journal row {row[0] if row else '(empty)'}")

    def manual_request_paths(self, cases) -> list:
        import manual_evidence
        return [manual_evidence.request_path(self.task_root, c).relative_to(self.task_root).as_posix() for c in cases]
