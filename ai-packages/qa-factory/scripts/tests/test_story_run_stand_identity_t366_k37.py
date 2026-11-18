#!/usr/bin/env python3
"""t366 k37: a part of test_story_run_stand_identity.py, split by tools/test_split.py (TD-11c). The shared helpers are in story_run_stand_identity_common."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness  # noqa: E402
from harness import check, check_in, check_not_in  # noqa: E402
from story_run_common import run_scenarios, d2_answer, d2_conductor_calls, d2_pipeline, eq, human_broken, s0_question, set_control
from story_run_stand_identity_common import (  # noqa: E402
    HEAD, Rig, asked, flag, journal_answers, matched, run_entry, unknown, use_plan,
)


# --- t-366: the fix pass after critic t-361 ----------------------------------------------------------------------------

def t366_f2_f3_f5_partly_recorded_prose_label_and_console() -> None:
    # F2 (the critic's D3): `always confirm` where `record` is written and `confirm` fails
    rig = Rig(profiles=("api",), real=True)
    try:
        use_plan({"TC-1": ("api", "automate")})
        run_entry(rig, s5=("TC-1",))
        blocker = rig.task_root / "state" / "stand-confirmations.jsonl"
        blocker.mkdir(parents=True)               # the confirmation cannot be appended to a folder: the second step fails
        code, out, started, _ = run_entry(rig, "always confirm", s5=("TC-1",))
        eq("F2: the decision IS written (a person_confirms row) and the word for this story is not", (code, [(r["method"], r["source"]) for r in rig.rows()], rig.confirmations()),
           (3, [("person_confirms", "person")], []))
        eq("F2: the question is the partly-recorded one, offering deployed / retry / stop", (flag(rig).get("variant"), flag(rig).get("answers")),
           ("partly_recorded", ["deployed", "retry", "stop"]))
        text = s0_question(rig.task_root).split("\n---\nAnswer:")[0]
        check_in("F2: it says what is written", "is written: you check the build on that stand yourself", text)
        check_in("F2: ... and what is not", "What is not written is your word that this story's build is there now", text)
        check_not_in("F2 (FR-10): it does NOT say nothing was recorded", "nothing was recorded", text)
        check("F2: no state path, no exception name in it", not any(bad in text for bad in (".jsonl", "Error", "Traceback", "stand_identity.py")), text)
        eq("F2: the text obeys human-questions.md", human_broken(text.split("\n", 6)[-1]), [])
        check_in("F2: the factory's own words are in the details file", "stand-confirmations.jsonl", (rig.task_root / "state" / "driver-question-details.md").read_text(encoding="utf-8"))
        check("F2 (FR-10): the console prints ONE outcome line - not `recorded` and then `not recorded`",
              "your decision for stand `localhost` (api tests) is written but your word for this story is not" in out
              and "is recorded" not in out and "was not recorded" not in out and "Recorded the decision" not in out, out[:700])
        check("F2: the journal says it was partly recorded, with the words", any("partly recorded" in n and n.endswith(": always confirm") for n in journal_answers(rig)))
        blocker.rmdir()
        code, out, started, _ = run_entry(rig, "deployed", s5=("TC-1",))
        eq("F2: `deployed` then completes it: the word is written and the stage goes on (exit 0)", (code, [r["kind"] for r in rig.confirmations()], len(rig.rows())), (0, ["deployed"], 1))
    finally:
        rig.done()
    rig = Rig(profiles=("api",), real=True)
    try:
        use_plan({"TC-1": ("api", "automate")})
        run_entry(rig, s5=("TC-1",))
        (rig.task_root / "state" / "stand-confirmations.jsonl").mkdir(parents=True)
        run_entry(rig, "always confirm", s5=("TC-1",))
        code, out, started, _ = run_entry(rig, "stop", s5=("TC-1",))
        eq("F2: `stop` after a partly-recorded answer is held like any stop (exit 3, nothing passed)", (code, started, rig.confirmations()), (3, [], []))
        check_in("F2: ... with the held text", "You said to stop the story here", s0_question(rig.task_root))
    finally:
        rig.done()
    # F2 CONTROL: `record` itself failing is still the plain not-recorded question (nothing IS written)
    rig = Rig(profiles=("api",), real=True)
    try:
        use_plan({"TC-1": ("api", "automate")})
        run_entry(rig, s5=("TC-1",))
        rig.registry().parent.mkdir(parents=True, exist_ok=True)
        rig.registry().write_text("{ not json", encoding="utf-8")
        run_entry(rig, "always confirm", s5=("TC-1",))
        check_in("F2 CONTROL: when the FIRST step fails, nothing is written and the text says so", "so nothing was recorded for this stand", s0_question(rig.task_root))
        eq("F2 CONTROL: ... and it is the how question, not the partly one", flag(rig).get("variant"), "how")
    finally:
        rig.done()
    # F3 (the critic's D4): prose after `label` or `file` is NOT a value - the conductor reads it, no registry row
    rig = Rig(profiles=("api",), real=True)
    try:
        use_plan({"TC-1": ("api", "automate")})
        set_control(rig.root, {"conductor": {"action": "continue", "did": "read it", "text": "Read."}})
        run_entry(rig, s5=("TC-1",))
        for said in ("label i do not know which one, use the default", "file my notes about the build", "label a b"):
            before = len(d2_conductor_calls(rig.root))
            run_entry(rig, said, s5=("TC-1",))
            eq(f"F3: `{said[:30]}...` goes whole to the conductor, and no registry row was written", (len(d2_conductor_calls(rig.root)) - before, rig.rows()), (1, []))
        check_in("F3: the conductor was given the person's words", "use the default", d2_conductor_calls(rig.root)[0]["prompt"])
        # CONTROL: the same forms with a value of the right shape ARE recorded
        run_entry(rig, "label example.org/revision", s5=("TC-1",))
        eq("F3 CONTROL: a one-word label is recorded as a row", [(r["method"], r["label"]) for r in rig.rows()], [("oci_label", "example.org/revision")])
    finally:
        rig.done()


def t366_o1_a_person_label_does_not_outrank_the_sources() -> None:
    """The critic's P3: a stale label a person recorded, equal to HEAD, on a container whose files differ. AE2 holds for every
    row: the label row joins the ladder AT the label rung, AFTER the sources. The ladder is `runtime_probe.main` driven the way
    test_runtime_probe_onboarding does (its fake docker): the container is the one thing a real run cannot be given here."""
    import test_runtime_probe_onboarding as ONB
    w = ONB.World(git=True)
    try:
        c1, c2 = w.commits
        w.row("oci_label", label=ONB.LABEL)
        stand = ONB.Stand(app=True, labels={ONB.LABEL: c2}, sha=lambda container, path: "f" * 64)
        code, rec, _said = w.probe(stand, "--no-evidence", expected=c2)
        eq("O1/P3: a stale person label == HEAD, the container's content differs: MISMATCHED by content, never matched",
           (rec["result"], rec.get("provenance", {}).get("deployed_source_revision"), rec.get("differing_files")),
           ("mismatched", "content_mismatch", ["src/Page.vue"]))
        # FB-8 N2 (68539227): a content mismatch reads the container's image digest once (`docker inspect`, `observed_image`: what a
        # `test as is` word binds to), so `inspect` is expected; the label rung is `image inspect` and it must still not run
        eq("O1/P3: the label was never consulted (the `/app` check, the compare and the one digest read ran; no `image inspect`)",
           ONB.calls_of(stand), ["test -d", "inspect"])
        eq("O1/P3: the person's row was not rewritten or replaced", [(r["method"], r["source"]) for r in w.rows()], [("oci_label", "person")])
        # CONTROL: the sources cannot be compared (no /app in the container): the person's label decides, as before
        stand = ONB.Stand(app=False, labels={ONB.LABEL: c2})
        code, rec, _said = w.probe(stand, "--no-evidence", expected=c2)
        eq("O1 CONTROL: no /app in the container: the person's label answers - matched by the label",
           (rec["result"], rec["provenance"].get("identity_kind"), ONB.calls_of(stand)), ("matched", "oci_label", ["test -d", "inspect", "image inspect"]))
        # CONTROL: the sources match: matched by content, the label is still not needed
        same = ONB.R.sha_local(w.ui / "src" / "Page.vue")
        stand = ONB.Stand(app=True, labels={ONB.LABEL: c1}, sha=lambda container, path: same)
        code, rec, _said = w.probe(stand, "--no-evidence", expected=c2)
        eq("O1 CONTROL: the files match: matched by content even though the person's label says another commit", (rec["result"], ONB.calls_of(stand)), ("matched", ["test -d"]))
    finally:
        w.close()
    # the texts say it (the decided sentence)
    import stand_identity as SI
    for variant in ("how", "confirm"):
        body = " ".join("\n".join(SI.data()["question"]["variants"][variant]["text"]).split())
        check_in(f"O1: the `{variant}` text says a label tells which image the stand runs and the files are compared whatever it says",
                 "a label tells which image the stand runs, and when the files of this story can be compared with the files inside the container they are, whatever the label says", body)


# --- K37: positions, and the flag ----------------------------------------------------------------------------------

def k37_positions_and_the_flag() -> None:
    import story_run
    rig = Rig(profiles=("api",))
    try:
        use_plan({"TC-1": ("api", "automate")})
        rig.records(api=unknown("api"))
        # a stage with nothing to run never asks: S5 with no window refuses first, S6 with nothing to run closes
        driver, started, steps, probes = rig.driver(s5=())
        try:
            driver.stage_S5()
            check("K37 S5 with nothing to run refuses before any probe", False)
        except story_run.Refusal:
            check("K37 S5 with nothing to run refuses before any probe", True)
        except story_run.Person:
            check("K37 S5 with nothing to run refuses before any probe", False)
        driver, started, steps, probes = rig.driver(auto=(), manual=())
        driver.code_only = lambda stage, reason, evidence: None
        real_py = driver.py
        driver.py = lambda script, *a, **k: (0, "") if script in ("stage_done.py", "finalize_task.py") else real_py(script, *a, **k)
        try:
            driver.stage_S6()
            check("K37 S6 with nothing to execute closes without a question", True)
        except story_run.Person:
            check("K37 S6 with nothing to execute closes without a question", False)
        eq("K37 ... and no probe was run for either", rig.calls(), [])
        # a dispatch already begun and resumed with the person's words is not gated
        driver, started, steps, probes = rig.driver()
        driver.controller_state = lambda: {"dispatches": {"S5-qa-automator-1": {"stage": "S5", "role": "qa-automator", "scope": ["TC-1"]}}}
        resumed = []
        driver.resume_role = lambda stage, role, dispatch, words, **kw: resumed.append(dispatch)
        driver.state["pending_words"]["S5-qa-automator-1"] = "the person's words"
        driver.dispatch_action({"action": "resume_checkpoint", "dispatch_id": "S5-qa-automator-1"})
        driver.dispatch_action({"action": "wait_existing_job", "dispatch_id": "S5-qa-automator-1"})
        eq("K37 resume_checkpoint and wait_existing_job (begun) resume the role: no build check, no probe", (len(resumed), rig.calls()), (2, []))
        # the flag is not taken by another question's answer (mirror of D2 R1), and ask() clears it for every other Person
        set_control(rig.root, {"conductor": {"action": "continue", "did": "read it", "text": "Read."}})
        for label, kind, packet in (("kind conductor with a stale flag", "conductor", {"environment": "localhost", "profile": "api", "answers": ["deployed"], "revision": HEAD}),
                                    ("kind stand_identity with NO flag", "stand_identity", None)):
            before = len(d2_conductor_calls(rig.root))
            driver = rig.driver()[0]
            driver.state["asked"] = {"kind": kind, "stage": "S5", "dispatch": ""}
            driver.state.pop("build_question", None)
            if packet:
                driver.state["build_question"] = packet
            driver.save_state()
            (rig.task_root / "state" / "driver-question.md").write_text(f"# q\nkind: {kind}\n", encoding="utf-8")
            driver.take_answer(Path(d2_answer(rig.root, "deployed")))
            eq(f"K37 answer: {label} keeps its own branch - the conductor is called once, as before", len(d2_conductor_calls(rig.root)) - before, 1)
            eq(f"K37 answer: {label} - no confirmation was recorded", rig.confirmations(), [])
        driver = rig.driver()[0]
        driver.state["build_question"] = {"environment": "localhost"}
        driver.ask(story_run.Person("conductor", "A question that is not the build's, with enough words in it to be a question for the person."))
        check("K37 ask(): a Person that carries no packet clears the flag (it never outlives its question)", "build_question" not in driver.state)
    finally:
        rig.done()
    # an unconfirmed stand asks the STAND question first, never the build question; a stand passed by word returns at once
    rig = Rig(profiles=("api",))
    try:
        use_plan({"TC-1": ("api", "automate")})
        rig.records(api=unknown("api"))
        d2_pipeline(rig.task_root, environment="localhost", environment_pending=True)
        code, out, started, driver = run_entry(rig, s5=("TC-1",))
        eq("K37 an unconfirmed stand asks the stand question first (kind environment); no build probe ran", (code, asked(rig).get("kind"), rig.calls()), (3, "environment", []))
        d2_pipeline(rig.task_root, environment=None, environment_pending=True,
                    stage_overrides=[{"stage": "S5", "match": "stand not confirmed", "decision": "go on", "at": "2026-10-03T10:00:00+00:00", "by": "human"}])
        code, out, started, driver = run_entry(rig, s5=("TC-1",))
        eq("K37 a stand passed by the person's word: build_check returns at once (no probe, no question), the role starts", (code, rig.calls(), ("S5", "qa-automator") in started), (0, [], True))
        # M8's neighbour: the same unconfirmed pair but matched, with the stand confirmed: no question either
        d2_pipeline(rig.task_root, environment="localhost", environment_pending=False, stage_overrides=[])
        rig.records(api=matched("api"))
        code, out, started, driver = run_entry(rig, s5=("TC-1",))
        eq("K37 (M8) a MATCHED record asks nothing (exit 0, no question open)", (code, asked(rig)), (0, {}))
        rig.records(api=unknown("api"))
        code, out, started, driver = run_entry(rig, s5=("TC-1",))
        eq("K37 (M8 CONTROL) the same stand with an `unknown` record DOES ask", (code, asked(rig).get("kind")), (3, "stand_identity"))
    finally:
        rig.done()
    # the dispatch sites: a relaunch and a never-launched dispatch ask before the role starts
    rig = Rig(profiles=("api", "e2e-ui"))
    try:
        use_plan({"TC-1": ("api", "automate"), "TC-2": ("e2e-ui", "manual-agent")})
        rig.records(api=unknown("api"), **{"e2e-ui": unknown("e2e-ui")})
        for stage, role, kind, scope, profile in (("S5", "qa-automator", "", ["TC-1"], "api"), ("S6", "qa-runner", "automation", ["TC-1"], "api"),
                                                  ("S6", "qa-runner", "manual", ["TC-2"], "e2e-ui")):
            driver, started, steps, probes = rig.driver()
            relaunch = {"action": "relaunch", "stage": stage, "role": role, "dispatch_request": {"scope": scope, "execution_kind": kind}}
            try:
                driver.dispatch_action(relaunch)
                check(f"K37 a relaunch on {stage} ({kind or 'no kind'}) asks first", False)
            except story_run.Person as person:
                eq(f"K37 a relaunch on {stage} ({kind or 'no kind'}) asks about the build of {profile} (kind stand_identity)", (person.kind, person.build_question["profile"]), ("stand_identity", profile))
            eq("K37 ... and no role started", started, [])
            driver, started, steps, probes = rig.driver()
            driver.controller_state = lambda stage=stage, role=role, scope=scope, kind=kind: {
                "dispatches": {f"{stage}-{role}-3": {"stage": stage, "role": role, "scope": scope, "execution_kind": kind}}}
            try:
                driver.dispatch_action({"action": "wait_existing_job", "dispatch_id": f"{stage}-{role}-3"})
                check(f"K37 a never-launched {stage} dispatch asks first", False)
            except story_run.Person as person:
                eq(f"K37 a never-launched {stage} dispatch asks about {profile}", (person.kind, person.build_question["profile"]), ("stand_identity", profile))
            eq("K37 ... and no role started", started, [])
        # a dispatch with no scope names no profile: nothing is probed, nothing is asked ("never all")
        before = len(rig.calls())
        driver, started, steps, probes = rig.driver()
        driver.dispatch_action({"action": "relaunch", "stage": "S6", "role": "qa-runner", "dispatch_request": {"scope": [], "execution_kind": ""}})
        eq("K37 a dispatch with an EMPTY scope probes nothing and asks nothing: the role starts", (len(rig.calls()) - before, started), (0, [("S6", "qa-runner")]))
    finally:
        rig.done()


def main() -> None:
    run_scenarios([], [
        t366_f2_f3_f5_partly_recorded_prose_label_and_console,
        t366_o1_a_person_label_does_not_outrank_the_sources,
        k37_positions_and_the_flag,
    ])
    harness.finish("test_story_run_stand_identity_t366_k37")


# split: runner piece 1
if __name__ == "__main__":
    main()
