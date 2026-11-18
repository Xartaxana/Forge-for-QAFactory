#!/usr/bin/env python3
"""t667 c21: a part of test_story_run_refusals.py, split by tools/test_split.py (TD-11c). The shared helpers are in story_run_refusals_common."""
import contextlib
import io
import json
import os
import re
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness  # noqa: E402
from harness import check, check_eq, check_in, check_not_in  # noqa: E402
from story_run_common import driver_for, jsonl, run_scenarios, seed, set_control, stub_calls
from story_run_refusals_common import (  # noqa: E402
    RES_DISPATCH, RES_PLAIN, recording_stub, res_driver, res_errors, res_fixture,
)


# --- t-261: the fix wave after the critic of t-225 (spec t-217 section 0d): O1 and O2 --------------------------------------
def refusal_o1_the_handoffs_own_resumes_are_the_saved_result() -> None:
    """O1 (critic t-244): `handoff` resumes the role in its own session (`again`, then `third` when every error is
    mechanical) and used to leave `state/driver-runs/<dispatch>.json` holding the FIRST result. After a conductor
    `continue` on the open dispatch, `wait_existing_job` re-judged that stale result, found its finding set already in
    `refusal_resumes`, and raised a false "came back with the same findings" question. Now each resume's non-empty result
    is the saved one (an empty error result is never written: `resume_with`'s rule) and the second entry judges THAT."""
    import story_run
    task = "QA-9"
    marked = lambda *names: res_errors(*names)
    plain = lambda *names: [f"exit gate said: row {n} has no review receipt" for n in names]
    second = RES_PLAIN.replace("written and run", "written and run: second words")
    third = RES_PLAIN.replace("written and run", "written and run: third words")

    def fixture(results, errors_by_marker):
        root, task_root, env = res_fixture(task)
        set_control(root, {"resume": {"result": results}})
        driver = driver_for(root, env, task)
        driver.state["sessions"][RES_DISPATCH] = "sess-a"
        driver.exit_errors = lambda role, digest, dispatch=None: next((e for m, e in errors_by_marker if m in digest), [])
        driver.form_errors = lambda dispatch: []
        return root, task_root, driver

    def saved_of(task_root):
        return json.loads((task_root / "state" / "driver-runs" / f"{RES_DISPATCH}.json").read_text(encoding="utf-8"))

    def handoff(driver, task_root):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            try:
                return driver.handoff("qa-automator", "S5", RES_DISPATCH, saved_of(task_root)), None
            except story_run.Refusal as refusal:
                return None, refusal

    # (1) one resume that repairs: the saved result is the resumed one, with the session the dispatch had
    root, task_root, driver = fixture([second], [("blocked_by_env", plain("TC-1"))])
    try:
        before = saved_of(task_root)
        digest, refusal = handoff(driver, task_root)
        check_eq("O1: the resume repaired the handoff", (refusal, "second words" in (digest or "")), (None, True))
        saved = saved_of(task_root)
        check_in("O1: the saved result IS the resumed one (the killed mutation: it stayed the first)", "second words", saved["result"])
        check_eq("O1: ...with the session id the dispatch had", saved["session_id"], before["session_id"])
        check_eq("O1: ...and one resume was spent", [c["kind"] for c in stub_calls(root)], ["resume"])
    finally:
        harness.cleanup(root)
    # (2) two resumes (every error is mechanical): the saved result is the LAST one
    root, task_root, driver = fixture([second, third], [("blocked_by_env", marked("TC-1")), ("second words", marked("TC-2"))])
    try:
        digest, refusal = handoff(driver, task_root)
        check_eq("O1: the second resume repaired it", (refusal, "third words" in (digest or "")), (None, True))
        check_in("O1: the saved result is the THIRD words, not the second and not the first", "third words", saved_of(task_root)["result"])
        check_eq("O1: two resumes were spent", [c["kind"] for c in stub_calls(root)], ["resume", "resume"])
    finally:
        harness.cleanup(root)
    # (3) an EMPTY result is never written: the first result stands byte for byte
    root, task_root, driver = fixture([""], [("blocked_by_env", marked("TC-1"))])
    try:
        path = task_root / "state" / "driver-runs" / f"{RES_DISPATCH}.json"
        held = path.read_bytes()
        digest, refusal = handoff(driver, task_root)
        check("O1: nothing repaired it: a refusal", refusal is not None)
        check_eq("O1: an empty resume result is not written - the saved result is byte for byte the first", path.read_bytes(), held)
    finally:
        harness.cleanup(root)
    # (4) the session the resume reports none for stays the dispatch's own
    root, task_root, driver = fixture([second], [])
    try:
        driver.keep_resumed_result(RES_DISPATCH, {"result": "words", "session_id": ""}, {"session_id": "sess-a"})
        check_eq("O1: a resume that reports no session keeps the one before (a result with no session cannot be resumed again)",
                 (saved_of(task_root)["session_id"], saved_of(task_root)["result"]), ("sess-a", "words"))
        driver.keep_resumed_result(RES_DISPATCH, {"result": "  ", "session_id": "sess-b"}, {"session_id": "sess-a"})
        check_eq("O1: a blank result writes nothing", saved_of(task_root)["result"], "words")
    finally:
        harness.cleanup(root)
    # (5) the SECOND entry judges the new result: the resume answered with other findings; a fresh driver (the loop
    # came back after a conductor `continue`) must see THOSE, not the set the record says was already resumed on
    first_set, new_set = plain("TC-1"), plain("TC-2", "TC-3")
    root, task_root, driver = fixture([second], [("blocked_by_env", first_set), ("second words", new_set)])
    try:
        digest, refusal = handoff(driver, task_root)
        check_eq("O1: the resume came back with OTHER findings: the handoff is refused over those", refusal.findings if refusal else None, new_set)
        again = driver_for(root, env_of(root), task)
        again.state["sessions"][RES_DISPATCH] = "sess-a"
        again.exit_errors = driver.exit_errors
        again.form_errors = lambda dispatch: []
        digest, refusal = handoff(again, task_root)
        check_eq("O1: the next entry (a fresh driver over the saved result) judges the NEW result: its findings are the new set, "
                 "not the first set the record already holds (the false `same findings`)",
                 refusal.findings if refusal else None, new_set)
        check("O1: and nothing in that refusal is the first set", not refusal or not any(line in refusal.text for line in first_set))
    finally:
        harness.cleanup(root)


def env_of(root):
    """The environment `driver_for` needs, rebuilt from the project's own stub files."""
    return dict(os.environ, CLAUDE_PROJECT_DIR=str(root), STORY_RUN_CLAUDE=str(root / "fake_claude.py"),
                STUB_CONTROL=str(root / "stub-control.json"), STUB_LOG=str(root / "stub-log.jsonl"))


def refusal_o2_the_text_reading_is_for_the_two_refusal_kinds_only() -> None:
    """O2 (critic t-244): the fallback that reads a dispatch out of an OLDER question's text ran for any kind with no
    `blocks` key. An `environment` question with no dispatch that quotes `--dispatch S6-qa-test-runner-1` in its own
    words then filed the person's answer to that runner (the killed mutation). It now runs only for `conductor` and
    `refusal`, and only when there is no `blocks` key."""
    task = "QA-9"
    root, task_root, env = seed(task)
    try:
        driver = driver_for(root, env, task)
        driver.judged_reply = lambda *a, **k: ""
        driver.conductor = lambda text, *, words="", files=None, words_file=None: {"action": "continue", "did": "stub"}
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

        text = ("# Driver question\n---\nThe stand did not answer. Last run: python x.py --dispatch S6-qa-test-runner-1 "
                "and \"dispatch_id\": \"S6-qa-test-runner-1\".\n")
        for kind, words in (("environment", "go on, I read it"), ("package", "go on")):
            said = answer({"kind": kind, "stage": "S6", "dispatch": ""}, text, words)
            check_eq(f"O2: kind `{kind}`, no dispatch, no `blocks` key: the words are filed to NO dispatch (the quoted runner id is never read)",
                     driver.state["pending_words"], {})
            check_in(f"O2: kind `{kind}`: and it says so", "the answer is filed for no dispatch: the question names none", said)
            check_not_in(f"O2: kind `{kind}`: the old line is gone", "named by the refusal itself", said)
        # the two kinds an older driver raised from a refusal keep the reading (with its shape check), and only with no `blocks` key
        for kind in ("conductor", "refusal"):
            said = answer({"kind": kind, "stage": "S5", "dispatch": ""}, "# q\n---\nrun --dispatch S5-qa-code-critic-7 again\n")
            check_eq(f"O2: kind `{kind}` of an older driver (no `blocks` key) still files by the text",
                     driver.state["pending_words"], {"S5-qa-code-critic-7": "go on, I read it"})
            check_in(f"O2: kind `{kind}`: said as before", "the answer is filed for S5-qa-code-critic-7, named by the refusal itself", said)
            answer({"kind": kind, "stage": "S5", "dispatch": "", "blocks": []}, "# q\n---\nrun --dispatch S5-qa-code-critic-7 again\n")
            check_eq(f"O2: kind `{kind}` WITH the `blocks` key never reads the text", driver.state["pending_words"], {})
    finally:
        harness.cleanup(root)


def refusal_t667_take_answer_branches_no_other_file_reaches() -> None:
    """t-667 D14 (characterisation BEFORE the move, green on the unmodified tree): the branches of `take_answer` whose bodies move
    into helpers and that the rest of the rig never ran in this process - the S0 block, the S1 exit gate (a condition with a side
    effect, a reassigned `dispatch`), the stand and stand-login answers. INVARIANT: each runs exactly when it runs today, with
    its side effects in today's order, and the answer is cleared last."""
    import story_run
    task = "QA-9"
    root, task_root, env = seed(task)
    try:
        driver = driver_for(root, env, task)
        real_py = driver.py
        waiver = {"code": 0}
        seen = []

        def py(script, *args, **kwargs):
            if script == "waiver.py":
                seen.append(list(args))
                return waiver["code"], "waiver said no"
            return real_py(script, *args, **kwargs)
        driver.py = py

        def notes() -> list:
            return [str(e.get("notes")) for e in jsonl(root / "qa-factory" / "records" / "journal.jsonl")
                    if e.get("event") == "human_answer"]

        def answer(kind: str, stage: str, dispatch: str, text: str) -> str:
            driver.state["asked"] = {"kind": kind, "stage": stage, "dispatch": dispatch}
            driver.state["pending_words"] = {}
            driver.state_dir.mkdir(parents=True, exist_ok=True)
            (driver.state_dir / "driver-question.md").write_text("---\nkind: " + kind + "\n---\nQuestion?\n", encoding="utf-8")
            sent = root / "answer.md"
            sent.write_bytes(text.encode("utf-8"))
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                try:
                    driver.take_answer(sent)
                except story_run.Person as held:      # C1-6b: a pass the waiver refused is the seam's held question, raised after the line is printed
                    held_questions.append(held.text)
            return out.getvalue()

        held_questions = []

        # (1) the S0 block: the words wait for the next S0 step, no conductor
        driver.state["s0_block"] = "source_list"
        said = answer("halt", "S0", "", "skip the vendor docs")
        check_eq("t667 S0 block: the words wait under `S0`", driver.state["pending_words"], {"S0": "skip the vendor docs"})
        check_eq("t667 S0 block: the journal note names the block", notes()[-1], "S0 source_list: skip the vendor docs")
        check_in("t667 S0 block: and the line says so", "S0 source_list: the answer is kept and read in the next S0 step", said)
        check_eq("t667 S0 block: the question is cleared last", driver.state["asked"], {})
        driver.state.pop("s0_block")

        # (2) the S1 exit gate: the condition runs `s1_exit_gate`, then `record_s1`, then the branch asks `s1_exit_gate` again for the
        # dispatch (E3/E4); the words are filed to THAT dispatch even when the question named none
        order = []
        driver.s1_exit_gate = lambda qtext: (order.append("s1_exit_gate"), "S1-qa-scout-1")[1]
        driver.record_s1 = lambda qtext, words: (order.append("record_s1"), True)[1]
        said = answer("conductor", "S1", "", "the review is fine")
        check_eq("t667 S1 exit gate: the condition, the recording, then the dispatch", order, ["s1_exit_gate", "record_s1", "s1_exit_gate"])
        check_eq("t667 S1 exit gate: the words are filed to the exit gate's dispatch", driver.state["pending_words"],
                 {"S1-qa-scout-1": "the review is fine"})
        check_eq("t667 S1 exit gate: and the answer row names that dispatch", jsonl(driver.state_dir / "driver-answers.jsonl")[-1]["dispatch"],
                 "S1-qa-scout-1")
        del driver.s1_exit_gate, driver.record_s1
        driver._answer_s1_gap = lambda words, asked, qtext, stage, dispatch: True      # C2-9: the answer's executor (record_gaps stands behind it)
        answer("s1_gap", "S1", "S1-qa-scout-1", "the gaps are as listed")
        check_eq("t667 S1 gap: a recorded gap answer is filed for its dispatch", driver.state["pending_words"],
                 {"S1-qa-scout-1": "the gaps are as listed"})
        del driver._answer_s1_gap

        # (3) the stand question: `go on` whose pass the waiver refuses is said, nothing is journaled, the flag is spent
        waiver["code"] = 1
        driver.state["stand_question"] = "S5"
        before = len(notes())
        said = answer("environment", "S5", "", "go on")
        check_in("t667 stand: a pass that was not recorded is said with the end of the refusal",
                 "S5: the pass was not recorded (waiver said no); the question comes back", said)
        check_eq("t667 stand: the seam journals the person's words once (C1-6b), the held question comes back", (len(notes()) - before, held_questions[-1].startswith("Your word could not be recorded as the pass")), (1, True))
        check("t667 stand: the flag is spent", "stand_question" not in driver.state, str(driver.state.get("stand_question")))

        # (4) the stand-login question: three readings, each with its executor
        waiver["code"] = 0
        driver.state["login_question"] = True
        said = answer("stand_login", "S6", "", "retry")
        check_in("t667 login retry: the line (the seam's `person_does`)", "S6: nothing is passed; the step runs again", said)
        check_eq("t667 login retry: the journal note", notes()[-1], "S6 (retry): retry")
        check("t667 login retry: the flag is spent", "login_question" not in driver.state)
        seen.clear()
        driver.state["login_question"] = True
        said = answer("stand_login", "S6", "", "by hand")
        # RN1-9 B1 (t-767, `Driver.waiver_road`): the call ends `--words-file <path> --by driver` (no `--why-person`: no class was asked
        # here); the path is the one varying element, dropped
        check_eq("t667 login by hand: ONE waiver, stage S6, the login block, the person's words by FILE (C1-6b: no inline --decision), on the driver road",
                 [call[:-3] + call[-2:] for call in seen],
                 [["--task", task, "--stage", "S6", "--block", driver.STAND_LOGIN_BLOCK, "--words-file", "--by", "driver"]])
        check_in("t667 login by hand: the line (the seam's `go_on_as_is`)", "S6: going on on the person's word; recorded", said)
        check_eq("t667 login by hand: the journal note", notes()[-1], "S6 (by hand): by hand")
        waiver["code"] = 1
        before = len(notes())
        driver.state["login_question"] = True
        said = answer("stand_login", "S6", "", "go on")
        check_in("t667 login go on, refused: said with the end of the refusal",
                 "S6: the pass was not recorded (waiver said no); the question comes back", said)
        check_eq("t667 login go on, refused: the seam journals the words once, the pass is not written", len(notes()) - before, 1)
        check_eq("t667: every answer above was cleared but the refused pass: its question is held (C1-6b)", driver.state["asked"],
                 {"kind": "stand_login", "stage": "S6", "dispatch": ""})
        check("t667: the story_run module the check read is the one under test", story_run.Driver is type(driver))
    finally:
        harness.cleanup(root)


def refusal_t667_dispatch_action_branches_no_other_file_reaches() -> None:
    """t-667 D15 (characterisation BEFORE the move): the branches of `dispatch_action` that move into one handler per kind and
    that the rest of the rig never ran in this process - S0, a halt that was asked, the liveness text of a failed read,
    `resolve_return` with the person's words and without them, and a kind the driver has no move for. INVARIANT: every
    path that returns today returns; an action with no move reaches the final `Refusal`."""
    import dispatch_liveness
    import story_run
    task = "QA-9"
    root, task_root, env = seed(task)
    dispatch = "S5-qa-test-runner-1"
    try:
        driver = driver_for(root, env, task)
        driver.controller_state = lambda: {"dispatches": {dispatch: {"stage": "S5", "role": "qa-test-runner"}}}
        driver.completion_for = lambda stage, role, record: "COMPLETE"
        made = []

        # (1) S0: a pipeline.json already there closes S0 by code; none there starts S0
        driver.code_only = lambda *args, **kwargs: made.append(("code_only", args))
        driver.s0 = lambda: made.append(("s0",))
        driver.dispatch_action({"action": "prepare_stage", "stage": "S0"})
        check_eq("t667 S0 with a pipeline.json: closed by code, the boundary is S0",
                 (made, driver.boundary), ([("code_only", ("S0", "preflight green: S0 closed on a task initialized before it", ["pipeline.json"]))], "S0"))
        made.clear()
        pipeline = task_root / "pipeline.json"
        kept = pipeline.read_bytes()
        pipeline.unlink()
        try:
            driver.dispatch_action({"action": "prepare_stage", "stage": "S0"})
        finally:
            pipeline.write_bytes(kept)
        check_eq("t667 S0 without one: S0 runs", made, [("s0",)])

        # (2) a gate whose repair round ran returns: the final Refusal is NOT reached (E10)
        made.clear()
        driver.gate_repair = lambda gate: {"ran": True, "top": ""}
        driver.gate = lambda gate, top="": made.append(("gate", gate))
        check_eq("t667 await_gate, a repair round ran: returns", driver.dispatch_action({"action": "await_gate", "gate": "A"}), None)
        check_eq("t667 await_gate, a repair round ran: the gate is not shown", made, [])

        # (3) wait_existing_job: a halt that was asked is asked again, from its question file
        driver.state["asked"] = {"dispatch": dispatch, "kind": "halt"}
        driver.state_dir.mkdir(parents=True, exist_ok=True)
        (driver.state_dir / "driver-question.md").write_text("a\nb\nc\nd\ne\nf\nTHE QUESTION\n", encoding="utf-8")
        try:
            driver.dispatch_action({"action": "wait_existing_job", "dispatch_id": dispatch})
            raised = None
        except story_run.Person as person:
            raised = person
        check_eq("t667 wait_existing_job, halt asked: a Person of that kind with the question's text, the stage and the dispatch",
                 raised and (raised.kind, raised.text, raised.stage, raised.dispatch), ("halt", "THE QUESTION\n", "S5", dispatch))
        # (4) wait_existing_job: nothing is waiting - the liveness read fails, and the refusal says so in the no-evidence word (FR-41)
        driver.state["asked"] = {}
        driver.state["sessions"][dispatch] = "sess"
        real_state = dispatch_liveness.state

        def broken(*args, **kwargs):
            raise RuntimeError("boom")
        dispatch_liveness.state = broken
        try:
            try:
                driver.dispatch_action({"action": "wait_existing_job", "dispatch_id": dispatch})
                refused = None
            except story_run.Refusal as exc:
                refused = exc
        finally:
            dispatch_liveness.state = real_state
        check_eq("t667 wait_existing_job, liveness unreadable: a Refusal for that dispatch", refused and refused.dispatch, dispatch)
        check_in("t667 wait_existing_job, liveness unreadable: the no-evidence word", f"wait_existing_job {dispatch}: nobody can tell whether "
                 "its agent is running: this host keeps no evidence either way — RuntimeError: boom", refused.text if refused else "")

        # (5) resolve_return: the person's words go back to the role; with none, a Refusal for the dispatch
        resumed = []
        driver.resume_role = lambda *args, **kwargs: resumed.append((args, kwargs))
        driver.state["pending_words"] = {dispatch: "accept it"}
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            result = driver.dispatch_action({"action": "resolve_return", "dispatch_id": dispatch})
        check_eq("t667 resolve_return with words: returns, the role resumed with them",
                 (result, resumed, driver.boundary), (None, [(("S5", "qa-test-runner", dispatch, "accept it"), {"complete": "COMPLETE"})], f"S5:{dispatch}"))
        check_in("t667 resolve_return with words: the line", f"{dispatch}: returned without acceptance", out.getvalue())
        driver.state["pending_words"] = {}
        try:
            driver.dispatch_action({"action": "resolve_return", "dispatch_id": dispatch})
            refused = None
        except story_run.Refusal as exc:
            refused = exc
        check_eq("t667 resolve_return without words: a Refusal for the dispatch", refused and refused.dispatch, dispatch)
        check("t667 resolve_return without words: and its text names the action", bool(refused) and refused.text.startswith("resolve_return: "),
              refused.text if refused else "")

        # (6) a kind with no move is the final Refusal
        try:
            driver.dispatch_action({"action": "bogus"})
            refused = None
        except story_run.Refusal as exc:
            refused = exc
        check("t667 an action with no move: the final Refusal", bool(refused) and refused.text.startswith("the driver has no move for `bogus`: "),
              refused.text if refused else "")
    finally:
        harness.cleanup(root)


# --- C2-1s (t-790; t-720 §3.4, §6): the whole list in the texts, and the route of a refusal that is a list -------------------
C21_STALE = "decision references stale source revision ('rev-1'); current is 'rev-2'"


C21_DONE = ("gate before prerequisite completion: gate must be A (after S4) or B (after S8), got 'B'; S8 is not started. If its last "
            "role was already accepted, this is the factory's own bookkeeping: `controller.py --operation recover` closes it")


C21_IDENTITY = "coverage v2 S5 completion requires distinct accepted author and active critic for the same window"


def c21_composite(*items: str) -> str:
    """The controller's combined refusal, as `Controller._raise_all` writes it (C2-2): the head states the count, the items are
    numbered, a continuation line of an item is indented by three spaces."""
    lines = [f"{len(items)} problems - the request is refused whole, every one is listed:"]
    lines += [f"{number}) " + item.replace("\n", "\n   ") for number, item in enumerate(items, 1)]
    return "\n".join(lines)


def c21_forms(text: str) -> dict:
    """The three shapes a combined refusal reaches the driver in (§L-3 id 3 / N1): the controller's bare text (the positive
    control), `story_step finish` (SR wraps `story_step: refused - {exc}`), and `--operation decision` (SR wraps the CLI's
    `{"error": "..."}` line, newlines JSON-escaped)."""
    return {"bare": text,
            "story_step": f"story_step finish {RES_DISPATCH} (exit 2):\nstory_step: refused - " + text,
            "decision": "controller decision (exit 2):\n" + json.dumps({"error": text})}


def refusal_c2_1_route_known_routes_a_list_item_by_item() -> None:
    """K1 (t-720 §3.4, §6): a refusal that is a LIST is routed by its items, never by one item's phrase or marker.
    INVARIANT: nothing that goes to the conductor alone today becomes `continue`, `retry` or a resume of the role through a
    neighbouring item; a head that is there but does not hold its count is the conductor's, NEVER `match_known` over the text."""
    import story_run
    known, marker = story_run.match_known, story_run.REPAIR_MARKER
    receipt = "code review receipt CR-1 is missing for the window " + marker
    check_eq("control: the item 1 alone is the conductor's (the row looks for `stale revision`, the text says `stale source revision`)",
             known(C21_STALE), None)
    check_eq("control: the item 2 alone is `continue`", known(C21_DONE), ("already_done", "continue"))
    check_eq("control: the marked item alone is a repair of the role", known(receipt), ("marked_repair", "resume_repair"))
    check_eq("control: the identity item alone is the conductor's", known(C21_IDENTITY), None)
    for label, items in (("example 1 (stale revision + prerequisite)", (C21_STALE, C21_DONE)),
                         ("example 2 (a marked receipt + the author's identity)", (receipt, C21_IDENTITY))):
        text = c21_composite(*items)
        check("control: " + label + " - the whole text would be routed by one item's phrase or marker by `match_known`",
              known(text) in (("already_done", "continue"), ("marked_repair", "resume_repair")), str(known(text)))
        for form, shown in c21_forms(text).items():
            check_eq(f"{label}, {form}: the conductor, not the neighbour's route", story_run.route_known(story_run.Refusal(shown)), None)
    # all items agree: that route; the marker travels only when EVERY item carries it
    for form, shown in c21_forms(c21_composite(receipt, receipt + " again")).items():
        check_eq(f"all items marked, {form}: a repair of the role", story_run.route_known(story_run.Refusal(shown)),
                 ("marked_repair", "resume_repair"))
    for form, shown in c21_forms(c21_composite(C21_DONE, C21_DONE + " (once more)")).items():
        check_eq(f"all items the same row, {form}: that row", story_run.route_known(story_run.Refusal(shown)), ("already_done", "continue"))
    for form, shown in c21_forms(c21_composite(C21_STALE, C21_IDENTITY)).items():
        check_eq(f"all items unknown, {form}: the conductor", story_run.route_known(story_run.Refusal(shown)), None)
    # a continuation line of an item stays in the item, not the neighbour (the three-space indent of `_raise_all`)
    tail = c21_composite(C21_STALE + "\n" + marker, C21_IDENTITY)
    check_eq("a marker on a CONTINUATION line of item 1 does not lead item 2", story_run.route_known(story_run.Refusal(tail)), None)
    # a head that does not hold its count is the conductor's, never `match_known` over the text
    mismatched = {"3 problems, two items": c21_composite(C21_STALE, C21_DONE).replace("2 problems", "3 problems", 1),
                  "2 problems, three items": c21_composite(C21_STALE, C21_DONE, C21_IDENTITY).replace("3 problems", "2 problems", 1),
                  "1 problem, one item": c21_composite(C21_DONE)}
    for label, text in mismatched.items():
        check("control: " + label + " - `match_known` of the text WOULD say " + str(known(text)), known(text) is not None)
        for form, shown in c21_forms(text).items():
            check_eq(f"{label}, {form}: the conductor", story_run.route_known(story_run.Refusal(shown)), None)
    # no head, fewer than two findings: `match_known` of the text, byte for byte
    for text in (C21_STALE, C21_DONE, receipt, "the moon is down", "story_step finish S1-qa-scout-1 (exit 3):\nstory_step: left none of the outputs"):
        check_eq(f"one item routes as `match_known` does: {text[:40]!r}", story_run.route_known(story_run.Refusal(text)), known(text))
    check_eq("one finding is the refusal's own text, as before",
             story_run.route_known(story_run.Refusal(receipt, findings=[receipt])), known(receipt))
    # an exit gate's findings: one with the marker and one without (a defect) are not a repair of the role
    mixed = story_run.Refusal("exit gate for S5-qa-automator-1 (qa-automator, S5): 2 finding(s):\n- " + receipt + "\n- " + C21_IDENTITY,
                              dispatch="S5-qa-automator-1", findings=[receipt, C21_IDENTITY])
    check_eq("control: the text of the mixed exit-gate refusal carries the marker", known(mixed.text), ("marked_repair", "resume_repair"))
    check_eq("findings [a marked finding, a defect] go to the conductor", story_run.route_known(mixed), None)
    marked = story_run.Refusal("x", findings=[receipt, receipt + " 2"])
    check_eq("findings that all carry the marker are a repair of the role", story_run.route_known(marked), ("marked_repair", "resume_repair"))


def refusal_c2_1_the_dry_run_routes_by_the_same_function() -> None:
    """The dry run's `would:` line (the old SR:10760) is `route_known` too: a combined refusal of `where` whose item 2 alone is
    `continue` is the conductor's in the dry run, as in the loop."""
    import story_run
    task = "QA-9"
    root, task_root, env = seed(task)
    try:
        driver = driver_for(root, env, task, dry_run=True)

        def where_refuses(text):
            def where():
                raise story_run.Refusal(text)
            driver.where = where
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                driver.describe()
            return out.getvalue()
        shown = where_refuses(c21_composite(C21_STALE, C21_DONE))
        check_in("the dry run says the conductor is called", "would: call the conductor", shown)
        check_not_in("and does not name the neighbour's row", "already_done", shown)
        check_in("a single known refusal is still named", "known refusal already_done -> continue", where_refuses(C21_DONE))
    finally:
        harness.cleanup(root)


def refusal_c2_1_the_texts_carry_the_whole_list() -> None:
    """K1 (t-720 §3.4, §6): the resume text, the mechanical third turn and the `Refusal` of the handoff say `N finding(s)` and carry
    EVERY line; past the byte ceiling they carry the path of the file that holds the whole list, written by that very call
    (FR-37); `Refusal.findings` stays whole and the head `exit gate for <id> (` is unchanged. The form's lines the code filled and
    the material it fetched go through the same renderer."""
    import detector_verdict as DV
    import story_run
    task = "QA-9"
    nine = [f"s5_precheck.py: [obligations] OB-{n} has no test bound - fix: bind it" for n in range(1, 10)]
    root, task_root, env = res_fixture(task, RES_PLAIN)
    try:
        driver, _p = res_driver(root, env, task, nine)
        result = json.loads((task_root / "state/driver-runs" / f"{RES_DISPATCH}.json").read_text(encoding="utf-8"))
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                driver.handoff("qa-automator", "S5", RES_DISPATCH, result)
            check("9 findings: the handoff is refused after its one resume", False)
        except story_run.Refusal as refusal:
            asked = stub_calls(root)[0]["prompt"].replace("\r\n", "\n")
            check_in("the resume text says the count", "The exit gate refused your handoff: 9 finding(s). Repair every one of them in this turn", asked)
            check("and carries all 9 lines, in order", all(f"- {line}" in asked for line in nine)
                  and [asked.index(line) for line in nine] == sorted(asked.index(line) for line in nine))
            check_not_in("and no pointer, no file: everything fits", "the whole list", asked)
            check_not_in("and does not claim a file", "(the rest in the file", asked)
            check("the Refusal is `exit gate for <id> (` + role and stage + the count + all 9 lines",
                  refusal.text.startswith(f"exit gate for {RES_DISPATCH} (qa-automator, S5): 9 finding(s):\n- ")
                  and all(f"- {line}" in refusal.text for line in nine), refusal.text)
            check_eq("its findings are all 9", refusal.findings, nine)
            check_eq("nothing was written where nothing was cut", (task_root / "state" / "findings").exists(), False)
    finally:
        harness.cleanup(root)

    # the mechanical third turn shows the same list: `fix exactly these 9 line(s)` and every line
    marked = res_errors(*[f"TC-{n}" for n in range(1, 10)])
    root, task_root, env = res_fixture(task, RES_PLAIN)
    try:
        driver, _p = res_driver(root, env, task, marked)
        result = json.loads((task_root / "state/driver-runs" / f"{RES_DISPATCH}.json").read_text(encoding="utf-8"))
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                driver.handoff("qa-automator", "S5", RES_DISPATCH, result)
            check("9 marked findings: refused after the third turn", False)
        except story_run.Refusal:
            third = stub_calls(root)[1]["prompt"].replace("\r\n", "\n")
            check_in("the third turn says the count", "Two things and nothing else. 1) Your handoff form: fix exactly these 9 line(s), one field at a time", third)
            check("and carries all 9 lines", all(f"- {line}" in third for line in marked))
    finally:
        harness.cleanup(root)

    # past the ceiling: a count and the path; the file holds every line and is the one the text names
    big = [f"s5_precheck.py: [obligations] OB-{n} " + "x" * 300 + f" END-{n}" for n in range(1, 41)]
    root, task_root, env = res_fixture(task, RES_PLAIN)
    try:
        driver, _p = res_driver(root, env, task, big)
        result = json.loads((task_root / "state/driver-runs" / f"{RES_DISPATCH}.json").read_text(encoding="utf-8"))
        path = driver.state_dir / "findings" / f"{RES_DISPATCH}-handoff.txt"
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                driver.handoff("qa-automator", "S5", RES_DISPATCH, result)
            check("40 long findings: refused after the resume", False)
        except story_run.Refusal as refusal:
            asked = stub_calls(root)[0]["prompt"].replace("\r\n", "\n")
            check_in("the resume text says 40 finding(s)", "The exit gate refused your handoff: 40 finding(s).", asked)
            check_in("and that the rest is in the file named at the end of the list", "(the rest in the file named at the end of the list):", asked)
            check_in("the last line of the list points at the file this very call wrote", f"the whole list: {path}", asked)
            check("the file exists and holds all 40, the last whole",
                  path.is_file() and path.read_text(encoding="utf-8").count("\n- ") == 40 and "END-40" in path.read_text(encoding="utf-8"))
            check("the text shows the ceiling's worth, in whole lines, and not the 40th", "END-1\n" in asked and "END-40" not in asked)
            shown_bytes = len(asked.split("\n- (+")[0].split(":\n", 1)[1].encode("utf-8"))
            check("the shown block is within the byte ceiling", shown_bytes <= DV.FINDINGS_MAX_BYTES + 400, str(shown_bytes))
            check_in("the Refusal names the count and the pointer too", "40 finding(s):", refusal.text)
            check_in("and the same path", f"the whole list: {path}", refusal.text)
            check_eq("its findings stay whole", refusal.findings, big)
        # the dry run names no file it did not write (FR-41)
        path.unlink()
        driver.dry = True
        said = driver.exit_ask("qa-automator", RES_DISPATCH, big)
        check_in("a dry run says the list could not be saved", "the whole list could not be saved", said)
        check_eq("and writes nothing", path.exists(), False)
        driver.dry = False
        # the lines the code filled and the material it fetched: every line, through the same renderer
        driver.state.setdefault("form_filled", {})[RES_DISPATCH] = [f"work.item[{n}].field = value {n}" for n in range(1, 21)]
        driver.state["collected"] = {"S1": [f"fetched material {n}" for n in range(1, 13)]}
        said = driver.exit_ask("qa-scout", RES_DISPATCH, nine)
        check("all 20 filled lines are shown, none cut at 12", all(f"- work.item[{n}].field = value {n}" in said for n in range(1, 21)))
        check("all 12 fetched lines are shown, none cut at 8", all(f"- fetched material {n}" in said for n in range(1, 13)))
        driver.state["form_filled"][RES_DISPATCH] = [f"work.item[{n}].field = " + "y" * 300 for n in range(1, 41)]
        driver.state["collected"] = {"S1": [f"fetched {n} " + "z" * 300 for n in range(1, 41)]}
        said = driver.exit_ask("qa-scout", RES_DISPATCH, nine)
        filled_path = driver.state_dir / "findings" / f"{RES_DISPATCH}-filled.txt"
        got_path = driver.state_dir / "findings" / f"{RES_DISPATCH}-collected.txt"
        check_in("a long filled list names its file", "+", said)
        check_in("filled: the pointer says lines, not findings, and the path", f"line(s) — the whole list: {filled_path}", said)
        check_in("collected: the same", f"line(s) — the whole list: {got_path}", said)
        check("and both files hold all 40", filled_path.read_text(encoding="utf-8").count("\n- ") == 40
              and got_path.read_text(encoding="utf-8").count("\n- ") == 40)
    finally:
        harness.cleanup(root)


def refusal_t809_f1_the_head_promises_a_file_only_when_it_was_written() -> None:
    """t-809 F-1 (critic t-806, FR-10/FR-41): the resume head says `(the rest in the file named at the end of the list)` ONLY when
    `render` wrote that file. A cut list whose file was not written (a dry run, a blank dispatch, a failed write) says so in the
    head - `the list is cut at N; the whole list could not be saved: <reason>` - and never promises a file. Each of the three lists
    (findings, filled, collected) is honest on its own: one save failing leaves the others' pointers as they were.
    INVARIANT: a head and the pointer line at the end of its list never contradict each other; a file left by an earlier call is
    never taken for this call's."""
    task = "QA-9"
    promise = "(the rest in the file named at the end of the list)"
    big = [f"s5_precheck.py: [obligations] OB-{n} " + "x" * 300 + f" END-{n}" for n in range(1, 41)]
    root, task_root, env = res_fixture(task, RES_PLAIN)
    try:
        driver, _p = res_driver(root, env, task, big)
        findings = driver.state_dir / "findings"
        path = findings / f"{RES_DISPATCH}-handoff.txt"

        def head_of(said: str) -> str:
            return said.split(":\n", 1)[0]
        # positive control: the file is written, the head promises it, the pointer names it
        said = driver.exit_ask("qa-automator", RES_DISPATCH, big)
        check_in("control: a written file - the head promises it", promise, head_of(said))
        check("control: and the file is there and the list's last line names it", path.is_file() and f"the whole list: {path}" in said)
        # (a) a dry run: no file is written, none is promised, the head says why
        path.unlink()
        driver.dry = True
        said = driver.exit_ask("qa-automator", RES_DISPATCH, big)
        driver.dry = False
        check_not_in("a dry run: the head does not promise a file", promise, said)
        check_not_in("a dry run: the head does not say everything is listed here", "they are all listed here", head_of(said))
        check("a dry run: the head says the list is cut at N and could not be saved, and why it was not",
              re.search(r"in this turn - the list is cut at \d+; the whole list could not be saved: this is a dry run, which writes no file$",
                        head_of(said)) is not None, head_of(said))
        check_eq("a dry run: nothing was written", path.exists(), False)
        # a blank dispatch has no file to write
        said = driver.exit_ask("qa-automator", "", big)
        check_not_in("a blank dispatch: no promise", promise, said)
        check_in("a blank dispatch: the head says the dispatch has no name", "could not be saved: the dispatch has no name", head_of(said))
        # (b) a failed write: the file's place is taken by a folder, so the write raises an OSError
        path.mkdir(parents=True)
        said = driver.exit_ask("qa-automator", RES_DISPATCH, big)
        check_not_in("a failed write: no promise", promise, said)
        check_in("a failed write: the head says the file could not be written", "could not be saved: the file could not be written", head_of(said))
        check_not_in("a failed write: no pointer to a path", f"the whole list: {path}", said)
        cut_at = re.search(r"the list is cut at (\d+);", head_of(said))
        shown = int(cut_at.group(1)) if cut_at else -1
        check_eq("the N of the head is the count of the whole lines shown", said.count("\n- s5_precheck.py"), shown)
        path.rmdir()
        # (c) the save failing on the SECOND list while the first succeeded: each pointer honest on its own
        driver.state.setdefault("form_filled", {})[RES_DISPATCH] = [f"work.item[{n}].field = " + "y" * 300 for n in range(1, 41)]
        driver.state["collected"] = {"S1": [f"fetched {n} " + "z" * 300 for n in range(1, 41)]}
        filled_path, got_path = findings / f"{RES_DISPATCH}-filled.txt", findings / f"{RES_DISPATCH}-collected.txt"
        filled_path.mkdir(parents=True)
        said = driver.exit_ask("qa-scout", RES_DISPATCH, big)
        check_in("second list fails, first succeeds: the head still promises the findings file", promise, head_of(said))
        check("and that file was written", path.is_file() and f"the whole list: {path}" in said)
        check_not_in("the filled list does not name a path it did not write", f"the whole list: {filled_path}", said)
        check_in("the filled list says it could not be saved", "line(s); the whole list could not be saved:", said)
        check_in("the collected list (third) is untouched by the second's failure", f"line(s) — the whole list: {got_path}", said)
        filled_path.rmdir()
        # and the other way round: the FIRST list fails, the others are written
        path.unlink()
        path.mkdir()
        said = driver.exit_ask("qa-scout", RES_DISPATCH, big)
        check_in("first list fails: the head says so", "could not be saved: the file could not be written", head_of(said))
        check_in("and the filled list's pointer is its own file", f"line(s) — the whole list: {filled_path}", said)
        check("and that file exists", filled_path.is_file())
        path.rmdir()
        # (d) a file of an earlier cut is not this call's: a list that fits removes it
        driver.exit_ask("qa-scout", RES_DISPATCH, big)
        check("the earlier cut's file is there", path.is_file())
        said = driver.exit_ask("qa-scout", RES_DISPATCH, big[:3])
        check_eq("a list that fits leaves no file of an earlier cut behind", path.exists(), False)
        check_not_in("and the head promises nothing", promise, head_of(said))
        # the third value of `listed`: "" when whole or written, the clause when not
        check_eq("listed: whole - nothing cut, no clause", driver.listed(big[:3], RES_DISPATCH, "handoff")[1:], (False, ""))
        check_eq("listed: cut and written - cut, no clause", driver.listed(big, RES_DISPATCH, "handoff")[1:], (True, ""))
    finally:
        harness.cleanup(root)


def refusal_t809_f2_the_s1_stops_are_evaluated_again_on_the_resumed_set() -> None:
    """t-809 F-2 (the Lead's decision: keep the S1 roads; critic t-806). `handoff` runs the scout's S1 person branches on the role's
    own message; the ladder's resume can leave a MIXED set (a source gap beside a review, a gap beside a form line), and the
    `Refusal` made of it reads as a list to `route_known` (C2-1s: the conductor). The branches run AGAIN on the resumed set, so
    the stop keeps its road: gap + review is `s1_review`, gap + a form line is `s1_gap`. POSITION INVARIANT: after the resume's
    recompute and BEFORE the `Refusal`. EDGES: a set the resume emptied raises nothing (the digest is returned); a set with
    neither a gap nor a review stays a `Refusal` with the same findings; another role's set is never an S1 stop."""
    import story_run
    task = "QA-9"
    gap = "source unavailable and not accepted by a person: SRC-1a2b"
    review = "no person has reviewed the source decisions"
    form = "handover form: `work.sources` is empty"
    first = res_errors("TC-1")

    def run(role: str, resumed: list):
        root, task_root, env = res_fixture(task, RES_PLAIN)
        try:
            driver, _p = res_driver(root, env, task, first)
            seen = []

            def exit_errors(r, digest, dispatch=None):
                seen.append(1)
                return list(first) if len(seen) == 1 else list(resumed)
            driver.exit_errors = exit_errors
            result = json.loads((task_root / "state/driver-runs" / f"{RES_DISPATCH}.json").read_text(encoding="utf-8"))
            try:
                with contextlib.redirect_stdout(io.StringIO()):
                    out = driver.handoff(role, "S1", RES_DISPATCH, result)
                return "digest", out, [c["kind"] for c in stub_calls(root)]
            except story_run.Person as person:
                return "person", person.kind, [c["kind"] for c in stub_calls(root)]
            except story_run.Refusal as refusal:
                return "refusal", refusal, [c["kind"] for c in stub_calls(root)]
        finally:
            harness.cleanup(root)
    for label, resumed, kind in (("a gap beside a review", [gap, review], "s1_review"),
                                 ("a gap beside a form line", [gap, form], "s1_gap"),
                                 ("two gaps", [gap, gap + " (2)"], "s1_gap"),
                                 ("a review beside a form line", [review, form], "s1_review")):
        got, what, calls = run("qa-scout", resumed)
        check_eq(f"the scout's resumed set, {label}: the person's stop {kind}, not a Refusal", (got, what), ("person", kind))
        check_eq(f"{label}: the role was resumed first (one resume per finding set), then the stop", calls[:1], ["resume"])
    got, what, _calls = run("qa-scout", [form, form + " 2"])
    check_eq("control: a resumed set with no gap and no review is still the Refusal", got, "refusal")
    if got == "refusal":
        check_eq("and its findings are the whole resumed set", what.findings, [form, form + " 2"])
    got, what, _calls = run("qa-scout", [])
    check_eq("EDGE: a set the resume emptied raises nothing - the digest comes back", got, "digest")
    got, what, _calls = run("qa-automator", [gap, review])
    check_eq("another role's set with the same lines is not an S1 stop", got, "refusal")
    # the route of the Refusal they used to become, for the record (the conductor, whole - the reason the branches run again)
    mixed = story_run.Refusal("exit gate for S1-qa-scout-1 (qa-scout, S1): 2 finding(s):\n- " + gap + "\n- " + review,
                              dispatch="S1-qa-scout-1", findings=[gap, review])
    check_eq("control: as a Refusal the mixed set is routed to the conductor", story_run.route_known(mixed), None)


def main() -> None:
    run_scenarios([], [
        refusal_o1_the_handoffs_own_resumes_are_the_saved_result,
        refusal_o2_the_text_reading_is_for_the_two_refusal_kinds_only,
        refusal_t667_take_answer_branches_no_other_file_reaches,
        refusal_t667_dispatch_action_branches_no_other_file_reaches,
        refusal_c2_1_route_known_routes_a_list_item_by_item,
        refusal_c2_1_the_dry_run_routes_by_the_same_function,
        refusal_c2_1_the_texts_carry_the_whole_list,
        refusal_t809_f1_the_head_promises_a_file_only_when_it_was_written,
        refusal_t809_f2_the_s1_stops_are_evaluated_again_on_the_resumed_set,
    ])
    harness.finish("test_story_run_refusals_t667_c21")


# split: runner piece 1
if __name__ == "__main__":
    main()
