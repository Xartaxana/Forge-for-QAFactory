#!/usr/bin/env python3
"""resume: a part of test_story_run_refusals.py, split by tools/test_split.py (TD-11c). The shared helpers are in story_run_refusals_common."""
import contextlib
import io
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness  # noqa: E402
from harness import check, check_eq, check_in, check_not_in  # noqa: E402
from story_run_common import d2_conductor_calls, driver_for, run_scenarios, seam_control, seed, set_control, stub_calls
from story_run_refusals_common import (  # noqa: E402
    RES_DIGEST, RES_DISPATCH, RES_PLAIN, recording_stub, res_driver, res_entry, res_errors, res_fixture,
)


def refusal_resume_once_per_finding_set() -> None:
    """K1 (cmp2-19 replay): marked exit-gate errors over a saved result whose digest holds a `blocked_by_env` row,
    the stand probe answering. The handoff resumes the role (twice: every error is mechanical), the refusal that
    follows is answered by ONE stand resume, then the PERSON - never the conductor - and a second entry on a FRESH
    driver over the same saved result makes no role call at all. INVARIANTS: a role is never resumed twice for the
    same finding set on one dispatch+session, across entries and relaunches; the record is written BEFORE the paid
    call; the stand is looked at once per dispatch+session; a refusal of the CALL class never resumes a role."""
    import story_run
    task = "QA-9"
    errors = res_errors("TC-1", "TC-2")
    root, task_root, env = res_fixture(task)
    try:
        driver, probes = res_driver(root, env, task, errors)
        check_eq("entry 1: the handoff's resumes and the stand's end in a pass back to the loop", res_entry(driver), None)
        calls = stub_calls(root)
        check_eq("K1: handoff resumes twice (every error is mechanical) and one resume for the stand, nothing else",
                 [c["kind"] for c in calls], ["resume", "resume", "resume"])
        check_eq("the stand was probed once, with `--env` and `--task` (the tool stand_check uses)",
                 probes, [["--env", "local", "--task", task]])
        check_in("the third resume carries the probe's own words whole", "liveness: alive - http://localhost:5173 -> HTTP 200",
                 calls[2]["prompt"])
        check_in("and the refusal, whole", errors[0], calls[2]["prompt"])
        check_in("and the one sentence", "Repair the named fields in the artifact, change nothing else", calls[2]["prompt"])
        check_eq("and every resume is in the role's OWN session", {c["resume"] for c in calls}, {"sess-a"})
        record = json.loads((task_root / "state/driver-state.json").read_text(encoding="utf-8"))["refusal_resumes"]
        check_eq("the record is keyed by dispatch, then session, then the finding set; the stand is its last word",
                 (list(record), list(record[RES_DISPATCH]), sorted(set(record[RES_DISPATCH]["sess-a"].values()))),
                 ([RES_DISPATCH], ["sess-a"], ["stand"]))
        person = res_entry(driver)
        check("K1: the next pass over the same findings is the PERSON's", isinstance(person, story_run.Person), repr(person))
        if person:
            check_eq("it is the ONE seam's question (t-764: kind exit_limit) about the dispatch the refusal names", (person.kind, person.dispatch),
                     ("exit_limit", RES_DISPATCH))
            check_in("and the check's lines, whole, are beside it", errors[0], person.details)
            check_in("the closed answers are offered (t-764): the paid round", "`round`", person.text)
            check_in("the pass over the check", "`go on`", person.text)
            check_in("and the stop", "`stop`", person.text)
        check_eq("K1: no conductor call at all (cmp2-19.log:6 `conductor: retry - stand_health.py` is gone)",
                 d2_conductor_calls(root), [])
        before = len(stub_calls(root))
        fresh, fresh_probes = res_driver(root, env, task, errors)
        again = res_entry(fresh)
        check("K1: a second entry on a FRESH driver over the same saved result is the person's again",
              isinstance(again, story_run.Person), repr(again))
        check_eq("and makes no role call and no probe (the record is in the state file, not in memory)",
                 (len(stub_calls(root)) - before, fresh_probes), (0, []))

        # (d) the probe's answer is a fact, not a guess: it fails, or prints nothing -> the stand does not answer
        for label, probe in (("fails", (1, "connection refused")), ("crashes", None), ("prints nothing", (0, ""))):
            root2, task_root2, env2 = res_fixture(task)
            try:
                d2, p2 = res_driver(root2, env2, task, errors, probe=probe or (0, ""))
                if probe is None:
                    real = d2.py
                    d2.py = lambda script, *a, **k: (_ for _ in ()).throw(OSError("no such executable")) \
                        if script == "env_probe.py" else real(script, *a, **k)
                # C1-1: a stand that does not answer is a state the conductor has moves for (the stand, a restart), so the seam CALLS it
                # once (D11) - and its question, with options, is the person's; the probe's words travel in the details
                set_control(root2, {"resume": {"result": RES_DIGEST}, "conductor": seam_control()})
                person = res_entry(d2)
                check(f"a probe that {label}: the person, the conductor asked once, and the stand is not resumed on",
                      isinstance(person, story_run.Person)
                      and [c["kind"] for c in stub_calls(root2)] == ["resume", "resume", "conductor"], repr(person))
                if person:
                    check_in(f"a probe that {label}: its words are beside the refusal", "What the probe of the stand printed",
                             person.details)
                    check_in(f"a probe that {label}: and the conductor was shown them", "What the probe of the stand printed",
                             stub_calls(root2)[-1]["prompt"])
                state = json.loads((task_root2 / "state/driver-state.json").read_text(encoding="utf-8"))
                check(f"a probe that {label}: nothing is recorded as a stand resume",
                      "stand" not in set(state["refusal_resumes"][RES_DISPATCH]["sess-a"].values()))
            finally:
                harness.cleanup(root2)

        # no `blocked_by_env` row, or no stand: no probe at all (the clause needs the closed state word AND a stand)
        for label, digest, environment in (("no blocked row", RES_PLAIN, "local"), ("no environment", RES_DIGEST, None)):
            root2, task_root2, env2 = res_fixture(task, digest, environment=environment)
            try:
                d2, p2 = res_driver(root2, env2, task, errors)
                person = res_entry(d2)
                check(f"{label}: the person after the handoff's own resumes, and no probe was run",
                      isinstance(person, story_run.Person) and p2 == [], repr((person, p2)))
            finally:
                harness.cleanup(root2)
        # the saved result is gone (the stand clause reads it): no stand clause, the person
        root2, task_root2, env2 = res_fixture(task)
        try:
            d2, p2 = res_driver(root2, env2, task, errors)
            refusal = story_run.Refusal("exit gate for " + RES_DISPATCH + " (qa-automator, S5): " + errors[0],
                                        dispatch=RES_DISPATCH, findings=errors)
            d2.note_resume(RES_DISPATCH, "sess-a", story_run.finding_key(errors), "handoff")
            (task_root2 / "state/driver-runs" / f"{RES_DISPATCH}.json").unlink()
            try:
                d2.resume_on_refusal(refusal, "S5", RES_DISPATCH)
                check("an absent saved result: the person", False)
            except story_run.Person:
                check("an absent saved result: the person, and no probe", p2 == [] and stub_calls(root2) == [], repr(p2))
        finally:
            harness.cleanup(root2)
    finally:
        harness.cleanup(root)


def refusal_resume_record_edges() -> None:
    """The record's own edges (t-217 §1, C3): written BEFORE the paid call; keyed by dispatch AND session; an alternation
    A, B, A ends at the second A; no dispatch or no session is the person's with nothing called; an accepted finish
    drops the record; a refusal's finding key ignores an order, a repeated line and the dispatch id."""
    import story_run
    task = "QA-9"
    root, task_root, env = res_fixture(task, RES_PLAIN)
    refused = lambda lines: story_run.Refusal("exit gate for " + RES_DISPATCH + " (qa-automator, S5): " + "; ".join(lines),
                                              dispatch=RES_DISPATCH, findings=lines)
    a, b = res_errors("TC-1"), res_errors("TC-2")
    try:
        # the key is a set: order, repeats, whitespace and the dispatch id do not make a new finding
        k = story_run.finding_key
        check_eq("key: the same lines in another order, with a repeat and other whitespace, are one set",
                 k(["x  y", "a"]), k(["a", "x y", "a", "  "]))
        check_eq("key: a dispatch id inside a line is `<dispatch>` - the next dispatch's same finding is the same",
                 k(["S5-qa-code-critic-2 has gaps"]), k(["S5-qa-code-critic-3 has gaps"]))
        check("key: another line is another key", k(["a"]) != k(["b"]))
        check_eq("key: no lines, no key (an empty set is never equal to anything)", (k([]), k(["", "  "])), ("", ""))

        # the record is written BEFORE the paid call: a call that dies still counts as the one resume
        driver, _p = res_driver(root, env, task, a)
        calls = []
        driver.run_claude = lambda *args, **kw: calls.append(args) or (_ for _ in ()).throw(RuntimeError("the call died"))
        try:
            driver.resume_on_refusal(refused(a), "S5", RES_DISPATCH)
            check("(c) a dying call raises", False)
        except RuntimeError:
            pass
        fresh, _p = res_driver(root, env, task, a)
        check("the record was on disk before the call: a FRESH driver reads it", story_run.finding_key(a) in
              fresh.resume_record(RES_DISPATCH, "sess-a"), json.dumps(fresh.state.get("refusal_resumes")))
        check_eq("(c) record-before-call: why = refusal", fresh.resume_record(RES_DISPATCH, "sess-a").get(story_run.finding_key(a)),
                 "refusal")
        fresh.run_claude = lambda *args, **kw: calls.append(args) or {"result": "x"}
        try:
            fresh.resume_on_refusal(refused(a), "S5", RES_DISPATCH)
            check("record-before-call: the second try is the person's", False)
        except story_run.Person:
            check_eq("record-before-call: and no second call was made", len(calls), 1)
        # handoff's own resume: the same
        root2, task_root2, env2 = res_fixture(task, RES_PLAIN)
        try:
            driver, _p = res_driver(root2, env2, task, a)
            driver.run_claude = lambda *args, **kw: (_ for _ in ()).throw(RuntimeError("the call died"))
            result = json.loads((task_root2 / "state/driver-runs" / f"{RES_DISPATCH}.json").read_text(encoding="utf-8"))
            try:
                driver.handoff("qa-automator", "S5", RES_DISPATCH, result)
                check("(b) a dying handoff resume raises", False)
            except RuntimeError:
                pass
            fresh, _p = res_driver(root2, env2, task, a)
            fresh.run_claude = lambda *args, **kw: (_ for _ in ()).throw(AssertionError("a second resume"))
            try:
                fresh.handoff("qa-automator", "S5", RES_DISPATCH, result)
                check("(b) the findings are still refused", False)
            except story_run.Person as person:
                check_eq("(b) record-before-call: a fresh handoff over the same findings resumes nothing and goes to the ONE seam (t-764)",
                         (person.kind, person.dispatch, a[0] in person.details), ("exit_limit", RES_DISPATCH, True))
        finally:
            harness.cleanup(root2)

        # C3: a NEW session of the same dispatch gets its own one resume; the old session's record is untouched
        root3, task_root3, env3 = res_fixture(task, RES_PLAIN)
        try:
            driver, _p = res_driver(root3, env3, task, a)
            check_eq("C3: a first resume in session A returns to the loop", driver.resume_on_refusal(refused(a), "S5", RES_DISPATCH), "continue")
            try:
                driver.resume_on_refusal(refused(a), "S5", RES_DISPATCH)
                check("C3: the same findings in the same session are the person's", False)
            except story_run.Person:
                pass
            driver.state["sessions"][RES_DISPATCH] = "sess-b"      # question_rework, an interrupted call, ...: a new session
            before = len(stub_calls(root3))
            check_eq("C3: a new session of the same dispatch gets its own one resume",
                     driver.resume_on_refusal(refused(a), "S5", RES_DISPATCH), "continue")
            check_eq("C3: one call, in the new session", [c["resume"] for c in stub_calls(root3)[before:]], ["sess-b"])
            try:
                driver.resume_on_refusal(refused(a), "S5", RES_DISPATCH)
                check("C3: and only one", False)
            except story_run.Person:
                check_eq("C3: both sessions are on record, keyed apart", sorted(driver.state["refusal_resumes"][RES_DISPATCH]),
                         ["sess-a", "sess-b"])
            # alternation A, B, A ends at the second A (the saved result stays the plain digest: no stand clause here)
            driver, _p = res_driver(root3, env3, task, a)
            driver.state["sessions"][RES_DISPATCH] = "sess-c"
            calls = len(stub_calls(root3))
            outcomes = []
            for lines in (a, b, a):
                try:
                    outcomes.append(driver.resume_on_refusal(refused(lines), "S5", RES_DISPATCH))
                except story_run.Person:
                    outcomes.append("person")
            check_eq("alternation A, B, A: the role is resumed on A and on B, and the second A is the person's",
                     (outcomes, len(stub_calls(root3)) - calls), (["continue", "continue", "person"], 2))
            # a resume that answers with an error and no words: spent, and the person's
            driver, _p = res_driver(root3, env3, task, b)
            driver.state["sessions"][RES_DISPATCH] = "sess-d"
            driver.run_claude = lambda *args, **kw: {"result": "", "is_error": True, "stderr": "no such session", "session_id": ""}
            try:
                driver.resume_on_refusal(refused(b), "S5", RES_DISPATCH)
                check("a resume that returns an error and no words is the person's", False)
            except story_run.Person as person:
                check_in("it says the session could not be asked", "its session no longer answers", person.text)
                check_in("and keeps the resume's own error beside the refusal", "no such session", person.details)
                check("and the resume is on record as spent", story_run.finding_key(b) in driver.resume_record(RES_DISPATCH, "sess-d"))

            # no dispatch, or no session: the seam CALLS the conductor once (C1-1, D11: it has a restart for them) and its
            # question with options is the person's
            set_control(root3, {"resume": {"result": RES_PLAIN}, "conductor": seam_control()})
            before = len(stub_calls(root3))
            driver, _p = res_driver(root3, env3, task, a)
            driver.state["sessions"].pop(RES_DISPATCH)
            for label, refusal, want in (("no session", refused(a), ("exit_limit", 0)),      # t-764 E9: the dispatch is known - the one seam, no call
                                         ("no dispatch", story_run.Refusal("exit gate for X (qa-automator, S5): " + a[0], findings=a), ("refusal", 1))):
                try:
                    driver.resume_on_refusal(refusal, "S5", RES_DISPATCH if label == "no session" else "")
                    check(f"{label}: the person", False)
                except story_run.Person as person:
                    check_eq(f"{label}: the person, and the conductor was called {want[1]} time(s)",
                             (person.kind, len(stub_calls(root3)) - before), want)
                    before = len(stub_calls(root3))
                    driver.conductor_calls.clear()
        finally:
            harness.cleanup(root3)

        # an accepted finish drops the dispatch's record (state-exits.md); a refused one keeps it
        root4, task_root4, env4 = res_fixture(task, RES_PLAIN)
        try:
            driver, _p = res_driver(root4, env4, task, a)
            driver.note_resume(RES_DISPATCH, "sess-a", story_run.finding_key(a), "handoff")
            driver.py = lambda script, *args, **kw: (3, "story_step: refused") if script == "story_step.py" else (0, "")
            try:
                with contextlib.redirect_stdout(io.StringIO()):
                    driver.finish(RES_DISPATCH, RES_PLAIN, complete=False, role="qa-automator", stage="S5")
            except story_run.Refusal as refusal:
                check_eq("a finish that is refused names its dispatch in the field (FR-16)", refusal.dispatch, RES_DISPATCH)
            check("a refused finish keeps the record", RES_DISPATCH in driver.state["refusal_resumes"])
            driver.py = lambda script, *args, **kw: (0, "accepted x")
            with contextlib.redirect_stdout(io.StringIO()):
                driver.finish(RES_DISPATCH, RES_PLAIN, complete=False, role="qa-automator", stage="S5")
            check("an accepted finish drops it", RES_DISPATCH not in driver.state["refusal_resumes"]
                  and RES_DISPATCH not in json.loads((task_root4 / "state/driver-state.json").read_text(encoding="utf-8"))["refusal_resumes"])
        finally:
            harness.cleanup(root4)
    finally:
        harness.cleanup(root)


def refusal_exit_limit_routes() -> None:
    """EL9 / EL11 (t-764, C1-5d2): a NEW finding set after nothing was resumed is still resumed once and then a `Refusal`, as today (the
    seam is only for a set the role has already seen); the NEXT entry over the same set is the person's, through the one seam (kind
    `exit_limit`), asked once - no conductor call - and a finish refusal that survived the resume (E8) reaches the same seam."""
    import story_run
    task, lines = "QA-9", ["plain unmarked finding of the check"]
    root, task_root, env = res_fixture(task, RES_PLAIN)
    try:
        driver, _p = res_driver(root, env, task, lines)
        result = json.loads((task_root / "state/driver-runs" / f"{RES_DISPATCH}.json").read_text(encoding="utf-8"))
        before = len(stub_calls(root))
        try:
            driver.handoff("qa-automator", "S5", RES_DISPATCH, result)
            check("EL9: a new set is refused", False)
        except story_run.Refusal as refusal:
            check_eq("EL9: a NEW set gets its one free resume and is a Refusal as today", (refusal.findings, len(stub_calls(root)) - before), (lines, 1))
        except story_run.Person:
            check("EL9: a new set is NOT the seam's yet", False)
        try:
            driver.handoff("qa-automator", "S5", RES_DISPATCH, result)
            check("EL9: the same set the next entry is asked", False)
        except story_run.Person as person:
            check_eq("EL9: the next entry over the same set is the ONE seam's, with no further call",
                     (person.kind, len(stub_calls(root)) - before, d2_conductor_calls(root)), ("exit_limit", 1, []))
        refusal = story_run.Refusal(f"story_step finish {RES_DISPATCH} (exit 3):\nstory_step: left none of the outputs", dispatch=RES_DISPATCH,
                                    findings=["story_step: left none of the outputs"])
        driver.note_resume(RES_DISPATCH, "sess-a", story_run.finding_key(refusal.findings), "refusal")
        try:
            driver.resume_on_refusal(refusal, "S5", RES_DISPATCH)
            check("EL11/E8: a finish refusal that survived its resume is asked", False)
        except story_run.Person as person:
            check_eq("EL11/E8: it reaches the same seam, the refusal whole beside it", (person.kind, refusal.text in person.details), ("exit_limit", True))
    finally:
        harness.cleanup(root)


def refusal_exit_limit_order_the_mechanical_third_turn_runs_before_the_seam() -> None:
    """EL8 (t-764, t-698 §12.1 E5 / positional invariant P1): a NEW set whose every error is mechanical (carries the repair marker) gets its free
    resume AND the one more cheap turn that SHOWS the lines, and only then is a `Refusal` as today; the NEXT entry over the same set is the
    seam's, with no further call. The seam stands AFTER the third turn: a seam placed before it would ask the person while a cheap turn at the role
    was still owed."""
    import story_run
    task = "QA-9"
    errors = res_errors("TC-1", "TC-2")
    root, task_root, env = res_fixture(task, RES_PLAIN)
    try:
        driver, _p = res_driver(root, env, task, errors)
        result = json.loads((task_root / "state/driver-runs" / f"{RES_DISPATCH}.json").read_text(encoding="utf-8"))
        before = len(stub_calls(root))
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                driver.handoff("qa-automator", "S5", RES_DISPATCH, result)
            check("EL8: a new mechanical set is refused", False)
        except story_run.Refusal as refusal:
            calls = stub_calls(root)[before:]
            check_eq("EL8: the free resume AND the third cheap turn ran, then a Refusal as today", ([c["kind"] for c in calls], refusal.findings),
                     (["resume", "resume"], errors))
            check_in("EL8: the second turn is the one that SHOWS the lines", "Two things and nothing else", calls[1]["prompt"])
        except story_run.Person:
            check("EL8: the seam is NOT reached before the third turn", False)
        after = len(stub_calls(root))
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                driver.handoff("qa-automator", "S5", RES_DISPATCH, result)
            check("EL8: the same set the next entry is asked", False)
        except story_run.Person as person:
            check_eq("EL8: THEN the seam, with no further call", (person.kind, len(stub_calls(root)) - after), ("exit_limit", 0))
    finally:
        harness.cleanup(root)


def refusal_call_class_stays_with_the_conductor() -> None:
    """C10 (FR-46): a refusal of the CALL class carries the marker too, but it is the driver's own mistake - the role is
    never resumed for it - and the head is matched ANCHORED: a text that only quotes `exit gate for <id>` further down
    is not that refusal. Only `exit gate for <id>` and `story_step finish <id> (exit 3)` take the role's own resume."""
    import story_run
    task = "QA-9"
    root, task_root, env = res_fixture(task, RES_PLAIN)
    marker = story_run.REPAIR_MARKER
    try:
        heads = [
            ("finish exit 2, --unresolved without --reason",
             "story_step finish " + RES_DISPATCH + " (exit 2):\nstory_step: finish got --unresolved without --reason. "
             + marker + ": repeat the call with both.", False),
            ("finish exit 2, no dispatch",
             "story_step finish " + RES_DISPATCH + " (exit 2):\nstory_step: no dispatch " + RES_DISPATCH
             + " in this story. " + marker + ": name one of them.", False),
            ("a text that only quotes the exit-gate head",
             "conductor note: exit gate for " + RES_DISPATCH + " (qa-automator, S5): " + marker, False),
            ("a text that quotes the finish head on its second line",
             "controller: refused\nstory_step finish " + RES_DISPATCH + " (exit 3): " + marker, False),
            ("the exit gate of a dispatch", "exit gate for " + RES_DISPATCH + " (qa-automator, S5): x. " + marker, True),
            ("finish exit 3 (the handover form)",
             "story_step finish " + RES_DISPATCH + " (exit 3):\nstory_step: the handover form is not complete - x\n  "
             + marker + ".", True),
        ]
        for number, (label, text, resumes) in enumerate(heads, 1):
            check_eq(f"{label}: the anchored head reads {'a dispatch' if resumes else 'nothing'}",
                     bool(story_run.Driver.resumable_head(text)), resumes)
            set_control(root, {"resume": {"result": RES_PLAIN}, "conductor": {"action": "continue", "did": "stub"}})
            before = len(stub_calls(root))
            driver, _p = res_driver(root, env, task, [])
            driver.state["sessions"][RES_DISPATCH] = f"sess-{number}"      # a session of its own: a clean record
            driver.state.pop("window_rounds", None)       # the cap of a window's rounds is not what is under test here
            driver.boundary = "S5:" + RES_DISPATCH
            with contextlib.redirect_stdout(io.StringIO()):
                outcome = driver.handle_refusal(story_run.Refusal(text, dispatch=RES_DISPATCH))
            kinds = [c["kind"] for c in stub_calls(root)[before:]]
            check_eq(f"{label}: {'the role is resumed, not the conductor' if resumes else 'the conductor, never a resume'}",
                     (outcome, kinds), ("continue", ["resume"]) if resumes else ("continue", ["conductor"]))
    finally:
        harness.cleanup(root)


def refusal_resumed_halt_is_heard() -> None:
    """The role's answer to a refusal-resume may be a halt (it cannot go on). `wait_existing_job` finishes the saved result,
    and `finish` would close the dispatch over a halt: the halt is heard first, as `run_role` hears it."""
    import story_run
    task = "QA-9"
    halting = "qa-automator S5 TC-1 · halt\nTC-1 · unresolved · cannot go on without the stand\nwork/automation-manifest.json"
    root, task_root, env = res_fixture(task, halting)
    try:
        driver, _p = res_driver(root, env, task, [])
        finished, done = [], []
        driver.finish = lambda *a, **k: finished.append(a)
        real = driver.py
        driver.py = lambda script, *a, **k: done.append(a) or (0, "") if script == "stage_done.py" else real(script, *a, **k)
        person = res_entry(driver)
        check("a halting saved result is the person's, not finished", isinstance(person, story_run.Person) and finished == [],
              repr((person, finished)))
        if person:
            check_eq("as a halt about the dispatch", (person.kind, person.dispatch), ("halt", RES_DISPATCH))
        check("and the stage is recorded halted", any("halted" in a for a in done), repr(done))
        # a result that does not halt is finished as before
        root2, task_root2, env2 = res_fixture(task, RES_PLAIN)
        try:
            driver, _p = res_driver(root2, env2, task, [])
            finished = []
            driver.finish = lambda *a, **k: finished.append(a)
            check_eq("a plain result is finished", (res_entry(driver), len(finished)), (None, 1))
        finally:
            harness.cleanup(root2)
    finally:
        harness.cleanup(root)


# --- t-217 / F-cmp2-22: whose answer it is - the field, never an id quoted in the text -----------------------------------
def refusal_answer_filed_by_the_field() -> None:
    """K3: cmp2-18.log:9 ("the answer is filed for S2-qa-requirements-tester-1, named by the refusal itself" - a gate-A
    packet quoting the S2 handoff) and cmp2-26.log:4 ("filed for <critic, named by the refusal itself" - a placeholder in a
    probe's hint). INVARIANTS: a gate answer is never filed to a dispatch; for the questions a refusal raises the field
    (`asked.dispatch`) decides and the text is never read; a question an OLDER driver asked (no `blocks` key) keeps the
    text reading, but a capture counts only when it is a dispatch id by shape and the only one; when unsure the words are
    filed to NO dispatch."""
    task = "QA-9"
    root, task_root, env = seed(task)
    try:
        driver = driver_for(root, env, task)
        driver.judged_reply = lambda *a, **k: ""
        conductor = []
        driver.conductor = lambda text, *, words="", files=None, words_file=None: conductor.append(words) or {"action": "continue", "did": "stub"}
        driver.record_by_code = recording_stub()

        def answer(asked: dict, qtext: str, words: str = "go on, I read it") -> str:
            driver.state["asked"] = dict(asked)
            driver.state["pending_words"] = {}
            driver.state.pop("gate_answer_kept", None)
            driver.state_dir.mkdir(parents=True, exist_ok=True)
            (driver.state_dir / "driver-question.md").write_text(qtext, encoding="utf-8")
            sent = root / "answer.md"
            sent.write_bytes(words.encode("utf-8"))
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                driver.take_answer(sent)
            return out.getvalue()

        quoted = ("# Driver question\nkind: gate_A\n---\nGate A. Accept the S2 handoff of S2-qa-requirements-tester-1 "
                  "and run --dispatch S2-qa-requirements-tester-1 now.\n")      # a spelling the legacy text reading WOULD file
        said = answer({"kind": "gate_A", "stage": "S4", "dispatch": ""}, quoted, "approve\ngo on, I read it")     # C1-4b: an approval is its first-line word
        check_eq("K3: a gate-A answer files nothing (cmp2-18.log:9)", driver.state["pending_words"], {})
        check_in("and says so", "gate A: the answer is recorded by code and filed for no dispatch", said)
        check_not_in("the old line is gone", "named by the refusal itself", said)
        driver.record_by_code = recording_stub(False)       # the decision did not record
        said = answer({"kind": "gate_B", "stage": "S8", "dispatch": ""}, quoted.replace("gate_A", "gate_B"), "approve\ngo on, I read it")
        check_eq("a gate answer the controller did not record is kept for the gate and still filed nowhere",
                 (driver.state["pending_words"], bool(driver.state.get("gate_answer_kept"))), ({}, True))
        check_in("said as it is", "gate B: the answer is kept for the gate and filed for no dispatch", said)
        driver.record_by_code = recording_stub()

        question = "# Driver question\nkind: refusal\n---\nrun `--dispatch S5-qa-code-critic-9` or see \"dispatch_id\": \"S5-qa-automator-4\"\n"
        said = answer({"kind": "refusal", "stage": "S5", "dispatch": "S5-qa-code-critic-2", "blocks": []}, question)
        check_eq("the field decides, and a text with two other ids is never read",
                 driver.state["pending_words"], {"S5-qa-code-critic-2": "go on, I read it"})
        check_in("said as it is", "the answer is filed for S5-qa-code-critic-2, the dispatch the question is about", said)
        for kind in ("conductor", "refusal"):
            answer({"kind": kind, "stage": "S5", "dispatch": "S5-qa-code-critic-2", "blocks": []}, question)
            check_eq(f"kind {kind} files by the field", list(driver.state["pending_words"]), ["S5-qa-code-critic-2"])
        # cmp2-26.log:4: the body of the question holds a REAL `--dispatch S5-qa-code-critic-2` (the controller's text), the
        # field is empty and the key is there: nothing is filed
        said = answer({"kind": "conductor", "stage": "S5", "dispatch": "", "blocks": []},
                      "# q\n---\nLast refusal: use `--dispatch S5-qa-code-critic-2` to rebuild\n")
        check_eq("K3: a question of this driver that names no dispatch files nothing, whatever its text quotes (cmp2-26.log:4)",
                 driver.state["pending_words"], {})
        check_in("and says so", "the answer is filed for no dispatch: the question names none", said)
        # an OLDER driver's question: the text, with the shape check
        for label, text, expected in (
                ("a placeholder", "run `--dispatch <critic id>` first", {}),
                ("the `dispatch_id` key with an id", 'the packet {"dispatch_id": "S5-qa-code-critic-7"}', {"S5-qa-code-critic-7": "go on, I read it"}),
                ("the command with an id", "run --dispatch S5-qa-code-critic-7 again", {"S5-qa-code-critic-7": "go on, I read it"}),
                ("two different ids", '"dispatch_id": "S5-qa-code-critic-7" and --dispatch S5-qa-automator-2', {}),
                ("the same id twice", '"dispatch_id": "S5-qa-code-critic-7" and --dispatch S5-qa-code-critic-7',
                 {"S5-qa-code-critic-7": "go on, I read it"}),
                ("an id only in the body (the bare third spelling is gone)", "the refusal is about S5-qa-code-critic-7 only", {})):
            answer({"kind": "refusal", "stage": "S5", "dispatch": ""}, "# q\n---\n" + text + "\n")
            check_eq(f"older driver, {label}", driver.state["pending_words"], expected)
        # boundaries that name no dispatch by shape
        for boundary in ("S0:ticket", "gate_A", "S5:TC-1,TC-2", "S5:environment:job-1", "where", "start"):
            driver.boundary = boundary
            check_eq(f"boundary `{boundary}` names no dispatch", driver.boundary_dispatch(), "")
        for boundary in ("S5:S5-qa-code-critic-2", "S5:S5-qa-code-critic-2:resume", "S5:S5-qa-code-critic-2:answer"):
            driver.boundary = boundary
            check_eq(f"boundary `{boundary}` names one", driver.boundary_dispatch(), "S5-qa-code-critic-2")
    finally:
        harness.cleanup(root)


def refusal_persons_carry_their_dispatch() -> None:
    """C9: every Person raised from a refusal carries the dispatch as a field - the refusal's own, else the boundary's - and
    every raise site that knows its dispatch passes it; `ask()` writes it, and writes `blocks` for the kinds that carry
    named blocks (an empty list until the parser of t-228 lands)."""
    import story_run
    task = "QA-9"
    root, task_root, env = seed(task)
    try:
        driver = driver_for(root, env, task)
        budget = "stage_done: STORY BUDGET: QA-9 is past its ceiling"
        for label, refusal, boundary, expected in (
                ("the refusal's field", story_run.Refusal(budget, dispatch="S5-qa-code-critic-2"), "S5:TC-1", "S5-qa-code-critic-2"),
                ("the field outranks the boundary", story_run.Refusal(budget, dispatch="S5-qa-code-critic-2"),
                 "S5:S5-qa-automator-1", "S5-qa-code-critic-2"),
                ("the boundary when there is no field", story_run.Refusal(budget), "S5:S5-qa-automator-1", "S5-qa-automator-1"),
                ("neither", story_run.Refusal(budget), "S5:TC-1,TC-2", "")):
            driver.boundary = boundary
            try:
                driver.handle_refusal(refusal)
                check(f"{label}: a known `ask_person` row raises", False)
            except story_run.Person as person:
                check_eq(f"{label}: the Person carries it", person.dispatch, expected)
        # the conductor's cap
        driver.boundary = "S5:S5-qa-code-critic-2"
        driver.conductor_calls[driver.boundary] = story_run.CONDUCTOR_CALLS_PER_BOUNDARY
        # (C1-1: `conductor()` raises ConductorSpent, which only the seam catches; the seam's answer at the cap is the priced
        # fallback question, never the old "What should happen?" text)
        try:
            driver.conductor("some refusal")
            check("the cap raises", False)
        except story_run.ConductorSpent as spent:
            check_eq("the cap is a ConductorSpent that counts the calls", spent.count, story_run.CONDUCTOR_CALLS_PER_BOUNDARY)
        try:
            driver.no_move({"why": "refusal", "kind": "conductor", "stage": "S5", "dispatch": driver.boundary_dispatch(),
                            "text": "some refusal"})
            check("the cap raises", False)
        except story_run.Person as person:
            check_eq("the cap's Person carries the boundary's dispatch", person.dispatch, "S5-qa-code-critic-2")
            check_eq("and offers the three standing answers", list(person.offered), ["retry", "go on", "stop"])
            check_not_in("and not the old text", "What should happen?", person.text)
            check_in("with their price lines", "the factory:", person.text)
        # ask() writes the field, and the blocks key for the two kinds
        driver.ask(story_run.Person("refusal", "A question that is long enough to be a real question for a person, with "
                                    "words in it.", "S5", "S5-qa-code-critic-2"))
        check_eq("ask(): asked carries the dispatch and an empty `blocks` list (refusal)",
                 (driver.state["asked"]["dispatch"], driver.state["asked"]["blocks"]), ("S5-qa-code-critic-2", []))
        driver.ask(story_run.Person("conductor", "A question that is long enough to be a real question for a person, with "
                                    "words in it.", "S5", "S5-qa-code-critic-2"))
        check_eq("ask(): the same for conductor", driver.state["asked"]["blocks"], [])
        driver.ask(story_run.Person("retro", "A question that is long enough to be a real question for a person, with "
                                    "words in it.", "S9"))
        check("ask(): no `blocks` key for a kind that carries none", "blocks" not in driver.state["asked"])
        # raise sites that know their dispatch pass it
        action = {"action": "resume_checkpoint", "dispatch_id": "S5-qa-code-critic-2"}
        driver.state["sessions"]["S5-qa-code-critic-2"] = "sess-x"      # a dispatch this driver launched: wait_existing_job refuses
        driver.py = lambda script, *a, **k: (0, "")                      # (and resume_role's `stage_done` is not what is under test)
        for kind in ("resume_checkpoint", "resolve_return", "wait_existing_job"):
            try:
                driver.dispatch_action(dict(action, action=kind))
                check(f"{kind}: refuses", False)
            except story_run.Refusal as refusal:
                check_eq(f"{kind}: the Refusal carries its dispatch", refusal.dispatch, "S5-qa-code-critic-2")
        try:
            driver.resume_role("S5", "qa-code-critic", "S5-qa-code-critic-8", "go on")
            check("resume_role with no session refuses", False)
        except story_run.Refusal as refusal:
            check_eq("resume_role: the Refusal carries its dispatch", refusal.dispatch, "S5-qa-code-critic-8")
    finally:
        harness.cleanup(root)


def main() -> None:
    run_scenarios([], [
        refusal_resume_once_per_finding_set,
        refusal_resume_record_edges,
        refusal_exit_limit_routes,
        refusal_exit_limit_order_the_mechanical_third_turn_runs_before_the_seam,
        refusal_call_class_stays_with_the_conductor,
        refusal_resumed_halt_is_heard,
        refusal_answer_filed_by_the_field,
        refusal_persons_carry_their_dispatch,
    ])
    harness.finish("test_story_run_refusals_resume")


# split: runner piece 1
if __name__ == "__main__":
    main()
