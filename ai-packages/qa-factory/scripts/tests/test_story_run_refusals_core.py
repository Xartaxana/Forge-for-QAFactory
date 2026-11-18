#!/usr/bin/env python3
"""core: a part of test_story_run_refusals.py, split by tools/test_split.py (TD-11c). The shared helpers are in story_run_refusals_common."""
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
from story_run_common import GOOD_MANIFEST, SCOUT_DIGEST, driver_for, eq, jsonl, run_driver, run_scenarios, seam_control, seed, set_control, stub_calls
from story_run_refusals_common import recording_stub  # noqa: E402


def refusal_round_trip_gate_and_routing() -> None:
    task = "QA-9"
    root, task_root, env = seed(task)
    try:
        out = run_driver(root, env, "--task", task, "--dry-run")
        check_eq("dry-run on a seeded project exits 0", out.returncode, 0)
        check_in("prints where", '"action": "prepare_stage", "stage": "S1"', out.stdout)
        check_in("and the stage it would start", "story_step start S1 qa-scout", out.stdout)
        check_in("and the claude command shape", "--agent qa-factory:<role>", out.stdout)
        check_eq("dry-run calls no stub", stub_calls(root), [])
        check("dry-run registers no dispatch", "S1-qa-scout-1" not in json.dumps(
            json.loads((task_root / "state/controller.json").read_text(encoding="utf-8")).get("dispatches", {})))

        # --- the stage round trip -----------------------------------------------------------
        set_control(root, {"roles": {"qa-scout": {
            "files": {"work/context-manifest.json": json.dumps(GOOD_MANIFEST).replace("{task}", task),
                      "work/context-bundle.json": "{}"},
            "result": SCOUT_DIGEST.replace("{task}", task)}}})
        out = run_driver(root, env, "--task", task, "--max-boundaries", "1")
        eq("one boundary runs and pauses with exit 0", out.returncode, 0, out.stdout[-1500:] + out.stderr[-800:])
        pipeline = json.loads((task_root / "pipeline.json").read_text(encoding="utf-8"))
        check_eq("S1 is done", pipeline["stages"].get("S1", {}).get("status"), "done")
        check_eq("bind wrote the session id as the agent id", pipeline["stages"]["S1"].get("agent_id"), "sess-S1-qa-scout-1")
        calls = stub_calls(root)
        check_eq("exactly one claude -p for the role", [c["kind"] for c in calls], ["role"])
        check_in("the role prompt is the start block", "You are qa-scout. Ticket: QA-9. Dispatch: S1-qa-scout-1.", calls[0]["prompt"])
        check_in("plus the scout's launch lines", "Launch flags: none", calls[0]["prompt"])
        check_in("plus the handoff form", "· ok|concerns|halt|impossible", calls[0]["prompt"])
        check_in("the role is named to claude", "qa-factory:qa-scout", " ".join(calls[0]["argv"]))
        check_in("the tools are the role tools", "Bash,Read,Write,Edit,MultiEdit,Glob,Grep", " ".join(calls[0]["argv"]))
        check_eq("the role's cwd is the project root", Path(calls[0]["cwd"]).resolve(), root.resolve())
        system = Path(calls[0]["sysfile"])
        check("the rule layer travels as the appended system prompt", system.is_file() and "Your factory rules" in system.read_text(encoding="utf-8"))
        check_in("with the resolved task packet", "Resolved task packet", system.read_text(encoding="utf-8"))
        runs = [r for r in jsonl(task_root / "state/driver-runs.jsonl") if r.get("kind") != "process"]  # the role and conductor lines: the `process` rows (P1-v N1) are the run record, counted apart
        check_eq("driver-runs.jsonl has the one role line", len(runs), 1)
        check_eq("with the session id", runs[0].get("session_id"), "sess-S1-qa-scout-1")
        check_eq("the cost", runs[0].get("total_cost_usd"), 0.0123)
        check_eq("the kind, role and dispatch", (runs[0]["kind"], runs[0]["role"], runs[0]["dispatch"]), ("role", "qa-scout", "S1-qa-scout-1"))
        check("the saved result is kept as done", (task_root / "state/driver-runs/S1-qa-scout-1.done.json").is_file())
        check_eq("no refusal, no conductor line", jsonl(task_root / "state/conductor.jsonl"), [])
        out = run_driver(root, env, "--task", task, "--dry-run")
        check_in("the next dry-run is at S2", '"stage": "S2"', out.stdout)

        # --- the gate: a question file and exit 3 ---------------------------------------------
        import story_run
        driver = driver_for(root, env, task)
        driver.where = lambda: {"action": "await_gate", "gate": "A", "revision": 7}
        # t-211: the gate-entry repair rehearses first, and this half-built story's real rehearsal holds
        # factory_fixable findings (no plan rows yet) that would send a round to the conductor. What is proved
        # here is the gate's question file, so the rehearsal is one that finds nothing (the step is test_story_run_gate_repair.py's).
        driver.rehearse = lambda gate: {"findings": []}
        code = driver.run()
        check_eq("await_gate exits 3", code, 3)
        question = task_root / "state/driver-question.md"
        check("the question file exists", question.is_file())
        qtext = question.read_text(encoding="utf-8")
        check_in("its kind is gate_A", "kind: gate_A", qtext)
        check_in("it carries the gate brief", "Gate A", qtext)
        check_in("and how to answer", "--answer", qtext)
        check_eq("driver-state remembers the open question",
                 json.loads((task_root / "state/driver-state.json").read_text(encoding="utf-8"))["asked"]["kind"], "gate_A")

        # --- the answer goes through the conductor ------------------------------------------
        before = len(stub_calls(root))
        answer = root / "answer-a.md"
        answer.write_text("Gate A: approved. Dirty tree: go on.", encoding="utf-8")
        set_control(root, {"conductor": {"action": "continue", "did": "gate-decision recorded", "text": "Recorded."}})
        driver = driver_for(root, env, task, answer=str(answer))
        driver.where = lambda: {"action": "stop", "reason": "test stop"}
        code = driver.run()
        check_eq("the answered loop goes on and stops on `stop`", code, 0)
        calls = stub_calls(root)[before:]
        check_eq("a gate decision the controller refuses still reaches the conductor",
                 [c["kind"] for c in calls], ["conductor"])
        check_in("the conductor got the person's words", "Gate A: approved. Dirty tree: go on.", calls[0]["prompt"])
        check_in("and the question kind", "kind `gate_A`", calls[0]["prompt"])
        check_in("conductor.md is its system prompt", "conductor.md", calls[0]["sysfile"])
        check_in("with the conductor tools", "Bash,Read,Grep", " ".join(calls[0]["argv"]))
        check_in("and a turn cap", "--max-turns", " ".join(calls[0]["argv"]))
        conductor = jsonl(task_root / "state/conductor.jsonl")
        check_eq("conductor.jsonl records the recording call", (conductor[-1]["action"], conductor[-1]["words"]), ("continue", True))

        check("the question is kept as answered", (task_root / "state/driver-question.answered.md").is_file() and not question.exists())
        answers = jsonl(task_root / "state/driver-answers.jsonl")
        check_eq("driver-answers.jsonl carries the words", answers[-1]["words"], "Gate A: approved. Dirty tree: go on.")
        # And when the decision DOES record, the conductor is not called at all: on
        # TP1-13797 the gate-A answer cost $1.05 of conductor to write down words the driver
        # was already holding, plus a 21-turn `ask_person` that recorded nothing.
        quiet = len(stub_calls(root))
        answer_again = root / "answer-a2.md"
        answer_again.write_text("Gate A: approved again, same words.", encoding="utf-8")
        driver = driver_for(root, env, task, answer=str(answer_again))
        driver.where = lambda: {"action": "stop", "reason": "test stop"}
        (task_root / "state" / "driver-question.md").write_text(
            "# Driver question\nkind: gate_A\nstage: S4\n", encoding="utf-8")
        driver.state["asked"] = {"kind": "gate_A", "stage": "S4", "dispatch": ""}
        driver.save_state()
        driver.record_by_code = recording_stub()
        check_eq("the loop goes on", driver.run(), 0)
        check_eq("a recorded gate decision costs no conductor session",
                 len(stub_calls(root)) - quiet, 0)

        runs = [r for r in jsonl(task_root / "state/driver-runs.jsonl") if r.get("kind") != "process"]  # the run record rows (P1-v N1) are counted apart
        check_eq("driver-runs.jsonl has the conductor line", runs[-1]["kind"], "conductor")

        # --- a known refusal never reaches the conductor -------------------------------------
        before = len(stub_calls(root))
        driver = driver_for(root, env, task)

        def budget():
            raise story_run.Refusal("stage_done: STORY BUDGET: QA-9 is past its ceiling — 12 dispatches")
        driver.where = budget
        code = driver.run()
        check_eq("STORY BUDGET is the person's: exit 3", code, 3)
        # The refusal is the factory's own vocabulary, so it goes BESIDE the question, in a file
        # the answer block names - never in place of one (references/human-questions.md).
        qtext = question.read_text(encoding="utf-8")
        check_not_in("the question does not paste the refusal", "STORY BUDGET", qtext)
        # C1-1: the question is the seam's, with no paid call: the three standing answers, each with its three price lines
        for token in ("retry", "go on", "stop"):
            check_in(f"it offers `{token}`", f"`{token}` — ", qtext)
        for label in ("the factory:", "you:", "the story:"):
            check_in(f"and every answer has the line `{label}`", label, qtext)
        check_eq("and `asked` carries the three tokens and why", (driver.state["asked"]["offered"], driver.state["asked"]["why"]),
                 (["retry", "go on", "stop"], "refusal"))
        check_in("and names where our own words are", "driver-question-details.md", qtext)
        check_in("which is where the refusal is", "STORY BUDGET",
                 (task_root / "state/driver-question-details.md").read_text(encoding="utf-8"))
        check_in("with kind refusal", "kind: refusal", qtext)
        check_eq("no conductor was called", len(stub_calls(root)), before)
        check_eq("conductor.jsonl names the table row", jsonl(task_root / "state/conductor.jsonl")[-1]["action"], "known:story_budget")

        # --- an unknown refusal goes to the conductor: ask_person, then stop --------------------
        stand_question = "Which stand should I use? Say `retry` when you have started one, or `stop`."
        set_control(root, {"conductor": seam_control(stand_question)})
        driver = driver_for(root, env, task)

        def unknown():
            raise story_run.Refusal("controller: the moon is down and nobody knows why")
        driver.where = unknown
        code = driver.run()
        check_eq("the conductor's ask_person is exit 3", code, 3)
        qtext = question.read_text(encoding="utf-8")
        check_in("the question is the conductor's", "Which stand should I use?", qtext)
        check_in("and every option carries its three price lines (C1-1)", "the factory: nothing runs now\nyou: work of yours", qtext)
        check_eq("and `asked` carries what the seam offered",
                 (driver.state["asked"]["offered"], driver.state["asked"]["why"]), (["retry", "stop"], "refusal"))
        check_in("with kind conductor", "kind: conductor", qtext)
        check_not_in("without our own words pasted under it", "the moon is down", qtext)
        check_in("which are one file away", "driver-question-details.md", qtext)
        check_in("and are there", "the moon is down",
                 (task_root / "state/driver-question-details.md").read_text(encoding="utf-8"))
        last = jsonl(task_root / "state/conductor.jsonl")[-1]
        check_eq("conductor.jsonl records the verdict", (last["action"], last["question"]), ("ask_person", stand_question))
        check_in("the conductor saw the refusal", "the moon is down", stub_calls(root)[-1]["prompt"])
        check_in("and the stand-remedy authorization", "Stand remedy: NOT authorized", stub_calls(root)[-1]["prompt"])
        check_in("and the moves open here", "## Moves open here", stub_calls(root)[-1]["prompt"])
        set_control(root, {"conductor": seam_control("This violates P-00. Say `retry` or `stop`.", action="stop", did="nothing")})
        driver = driver_for(root, env, task)
        driver.where = unknown
        code = driver.run()
        check_eq("the conductor's stop is exit 4", code, 4)
        check_in("and the reason is in the question file", "This violates P-00.", question.read_text(encoding="utf-8"))

        # --- three conductor calls per boundary, then the person -----------------------------
        set_control(root, {"conductor": {"action": "continue", "did": "nothing changed"}})
        driver = driver_for(root, env, task)
        before = len(stub_calls(root))
        driver.where = unknown
        code = driver.run()
        check_eq("a refusal the conductor keeps 'continuing' ends with the person", code, 3)
        check_eq("after at most three conductor calls", len(stub_calls(root)) - before, 3)
    finally:
        harness.cleanup(root)


def refusal_table() -> None:
    # --- the table itself -------------------------------------------------------------------
    import story_run
    check_eq("STORY BUDGET is a known refusal", story_run.match_known("... STORY BUDGET: x ..."), ("story_budget", "ask_person"))
    check_eq("a stale revision is retried", story_run.match_known("StateConflict: expected_revision 4"), ("stale_revision", "retry"))
    check_eq("an unknown text matches nothing", story_run.match_known("the moon is down"), None)
    check_eq("the S1 source review outranks the handoff-form row (the scout's planned stop is a person question)",
             story_run.match_known("exit gate for S1-qa-scout-1 (qa-scout, S1): source-inventory.json: required "
                                   "sources remain pending: SRC-1; source-inventory.json: no person has reviewed "
                                   "the source decisions yet; digest: your final message is not the handoff form"),
             ("s1_review", "s1_review"))
    gap_text = ("exit gate for S1-qa-scout-1 (qa-scout, S1): source-inventory.json: source material unavailable "
                "and not accepted by a person: SRC-606b160f666899cfb29c — show it to the person; digest: your "
                "final message is not the handoff form")
    check_eq("an unaccepted source gap is the person's word by code", story_run.match_known(gap_text), ("s1_gap", "s1_gap"))
    # A word outside a closed list is the role's repair, whatever the wording: the marker routes it
    # and the table row catches it. TP1-13797, 26.09: `unresolved[0].reason: contradiction`
    # (one word from `contradicts_requirement`) reached the conductor and then the person.
    vocab = ("exit gate for S4-qa-case-designer-1 (qa-case-designer, S4): handover form "
             "S4-qa-case-designer-1.yaml - unresolved[0].reason: `contradiction` is not a value of "
             "this field. Write one of: blocked_by_env, contradicts_requirement, handed_to_person")
    check_eq("a closed-list miss is resumed, never asked", story_run.match_known(vocab)[1], "resume_handoff")
    check_eq("the S1 exit gate names its scout dispatch", story_run.Driver.s1_exit_gate(gap_text), "S1-qa-scout-1")
    check_eq("a gate-A text is not an S1 exit gate", story_run.Driver.s1_exit_gate("gate A waits for words"), "")
    check_eq("the conductor's last JSON line is read", story_run.last_json_line('did things\n{"action": "retry", "did": "x"}'),
             {"action": "retry", "did": "x"})
    check_eq("prose without a verdict is no verdict", story_run.last_json_line("no json here"), {})


def refusal_markers() -> None:
    import story_run
    # P6: the marker in the refusal's own text routes it, so a check added anywhere gets its
    # answer from the right party without a row being added to the table above.
    marked = ("manifest_put: obligation id OB-9 is not in the plan. " + story_run.REPAIR_MARKER
              + "; if they have already decided, the orchestrator records it with waiver.py")
    check_eq("a refusal marked as a repair goes back to the role, not to the conductor",
             story_run.match_known(marked), ("marked_repair", "resume_repair"))
    check_eq("and a refusal marked as the person's question goes to the person",
             story_run.match_known("stand_gaps: " + story_run.PERSON_MARKER + " (three options)"),
             ("marked_person", "ask_person"))
    check("the marker outranks the table it precedes",
          story_run.match_known("required key `run_witness` is missing. " + story_run.REPAIR_MARKER)
          == ("marked_repair", "resume_repair"))


def refusal_dispatch_field() -> None:
    import story_run
    # FR-16: an id travels in a field, not in a sentence the same code just wrote. The regex
    # stays for refusals other scripts raise, where the text is all there is.
    own = story_run.Refusal("exit gate for S1-qa-scout-2 (qa-scout, S1): no inventory",
                            dispatch="S1-qa-scout-2")
    check_eq("the driver's own refusal carries the dispatch as a field", own.dispatch,
             "S1-qa-scout-2")
    other = story_run.Refusal("source_preflight: the S1 review is not accepted")
    check_eq("a refusal that knows no id says so", other.dispatch, "")
    check_eq("and the text reader is still there for those",
             story_run.Driver.s1_exit_gate(own.text), "S1-qa-scout-2")


def refusal_judge_and_source_gaps() -> None:
    import story_run
    # J6: the judge reads the person's words into the option the conductor would have spent its
    # first turns deciding — and records nothing, which is the line plan section 10.6 draws.
    root, _tr, env = seed("QA-J6")
    try:
        driver = driver_for(root, env, "QA-J6")
        import judge_reply
        saved_intent, saved_gap = judge_reply.intent, judge_reply.stand_gap_option
        try:
            judge_reply.intent = lambda q, r, **k: {"status": "ok", "value": "approve_with_edits",
                                                    "leaning": "approve_with_edits",
                                                    "confidence": 0.93, "decided": True,
                                                    "judgment": "gate_reply_intent"}
            judge_reply.stand_gap_option = lambda r, **k: {"status": "ok", "value": "theirs",
                                                           "leaning": "theirs", "confidence": 0.95,
                                                           "decided": True,
                                                           "judgment": "gate_stand_gap_option"}
            read = driver.judged_reply("Approve the plan?", "yes, but drop TC-9", "gate_A")
            check_in("the gate answer is read into a registered option", "approve_with_edits", read)
            check_in("and the reading names the question that made it", "gate_reply_intent", read)
            check_in("with its confidence, so a weak reading is visible", "0.93", read)
            gap = driver.judged_reply("a stand gap card", "I'll do it myself", "stand_gap")
            check_in("a stand-gap card is read by its own question",
                     "gate_stand_gap_option", gap)
            judge_reply.intent = lambda q, r, **k: {"status": "off", "value": None}
            check_eq("with the judge off the conductor gets nothing extra",
                     driver.judged_reply("Approve?", "yes", "gate_A"), "")
            judge_reply.intent = lambda q, r, **k: {"status": "ok", "value": None,
                                                    "leaning": "reject", "confidence": 0.6,
                                                    "judgment": "gate_reply_intent"}
            undecided = driver.judged_reply("Approve?", "hmm", "gate_A")
            check_in("an undecided reading travels as a leaning, never as a decision",
                     "a leaning only", undecided)
        finally:
            judge_reply.intent, judge_reply.stand_gap_option = saved_intent, saved_gap
        check_in("and the prompt says the option decides nothing",
                 "it decides nothing and records nothing", story_run.PRE_FILLED)

        # 26.09: the person is told WHY material is out of reach, and an access failure is not a
        # gap to accept — it is a dropped VPN or an expired login to check.
        inventory = driver.task_root / "work" / "source-inventory.json"
        inventory.parent.mkdir(parents=True, exist_ok=True)
        mr_url = "https://githost.example.invalid/group/app/-/merge_requests/3890"
        inventory.write_text(json.dumps({"schema_version": 1, "sources": [
            {"source_id": "SRC-1", "canonical_ref": "https://jira.example.invalid/browse/APP-8384",
             "status": "read", "materials": {"external_media": {"status": "unavailable", "items": [
                 {"url": mr_url, "status": "unavailable", "error": "auth_required: 302 to the SSO login",
                  "cause": "auth_required", "access_problem": True}]}}}]}), encoding="utf-8")
        gap = driver.s1_gap_text("source material unavailable and not accepted by a person: SRC-1")
        check_in("the gap question carries the cause, not only the URL",
                 "auth_required: 302 to the SSO login", gap)
        check_in("and says that a lost login answers exactly this way",
                 "dropped VPN or an expired login", gap)
        check_in("and warns what accepting it would put on the record",
                 "reachable source on the record as unreachable", gap)

        # What the factory's own authenticated route can collect, code collects before asking.
        calls: list = []
        saved_py = driver.py

        def fake_py(script, *args, **kwargs):
            calls.append((script, args))
            if script == "vcs_evidence.py":
                target = driver.project / args[args.index("--output") + 1]
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(json.dumps({
                    "status": "read", "revision": "c862735b7efe", "complete": True,
                    "url": "https://githost.example.invalid/g/a/-/merge_requests/3890",
                    "discussions": [1, 2],
                    "notes": [{"author": {"name": "Reviewer"}, "body": "the fixture shape was unreal"}],
                    "diffs": [{"new_path": "src/webhook.py"}],
                    "metadata": {"title": "read the action from object_attributes", "state": "merged",
                                 "description": "the filter read the wrong field and 111 tests stayed green"},
                }), encoding="utf-8")
            return 0, ""

        driver.py = fake_py
        try:
            check_eq("a merge request handed in as material is collected by code",
                     driver.close_vcs_gaps(
                         ["source material unavailable and not accepted by a person: SRC-1"]), True)
            # The trigger is any complaint about material, not only a declared gap: "materials not
            # inspected" names no source id, and four merge requests sat `pending` behind exactly
            # that wording while the ladder waited for a gap to be declared first.
            check_eq("a refusal that names no source still runs the ladder over every source",
                     driver.close_vcs_gaps(["source-inventory.json: materials not inspected"]), True)
        finally:
            driver.py = saved_py
        scripts_called = [name for name, _ in calls]
        check_in("through the factory's own collector", "vcs_evidence.py", scripts_called)
        check_in("and recorded as material that was read", "ticket_adapter.py", scripts_called)
        # An API receipt is evidence and it is huge (the precedent's four: 79 KB … 3.8 MB), so code
        # writes the readable part beside it — that is what a brief can hand to a role.
        digest = driver.task_root / "work" / "sources" / "SRC-1" / "mr-3890.md"
        check("a digest is written next to the receipt", digest.is_file())
        body = digest.read_text(encoding="utf-8")
        check_in("with the author's own words", "111 tests stayed green", body)
        check_in("with the review's words", "the fixture shape was unreal", body)
        check_in("with the files it touched", "src/webhook.py", body)
        check_in("and a pointer to the evidence itself", "mr-3890.json", body)
        recorded = next(args for name, args in calls if name == "ticket_adapter.py")
        check_in("as read, because the API route gives description and discussions",
                 "read", list(recorded))

        # Route 2: the API did not answer, the local checkout carries the change — and the change
        # is not the discussion, so what is recorded is `partial`, never `read`.
        calls.clear()
        saved_git = driver.git_route

        def failing_py(script, *args, **kwargs):
            calls.append((script, args))
            return (1, "401 unauthenticated") if script == "vcs_evidence.py" else (0, "")

        driver.py, driver.git_route = failing_py, lambda url, rel: "the local checkout ../../app carries the change as abc123456"
        try:
            check_eq("the local git route still closes the material",
                     driver.close_vcs_gaps(
                         ["source material unavailable and not accepted by a person: SRC-1"]), True)
        finally:
            driver.py, driver.git_route = saved_py, saved_git
        partial = next(args for name, args in calls if name == "ticket_adapter.py")
        check_in("recorded as partial, not as read", "partial", list(partial))
        check_in("naming what the route could not give",
                 "discussions are not in it", " ".join(str(a) for a in partial))

        # The person's own route: they read it and paste what matters. That is material with its
        # own provenance, not an accepted gap.
        calls.clear()
        driver.py = fake_py
        try:
            supplied = driver.record_pasted({"SRC-1"}, "Here is the thread that matters:\n"
                                            "```\nreviewer: the fixture shape was unreal\n```")
        finally:
            driver.py = saved_py
        check_eq("pasted content becomes material of that source", len(supplied), 1)
        pasted_call = next(args for name, args in calls if name == "ticket_adapter.py")
        check_in("with the provenance saying who produced it", "person_pasted", list(pasted_call))
        check_in("and the question offers that route in words",
                 "provenance: person_pasted", gap)

        # FV1-4 L3 (Q5): the note of supplied material names EVERY file, whole, from both fenced-answer callers; the shown text of
        # a kinds acceptance reaches `accept-gap --shown-text` whole (S-1501), as on the other road.
        saved_pasted, saved_row = driver.record_pasted, driver.answer_row
        fenced = "the thread:\n```\nreviewer: the fixture shape was unreal\n```"
        try:
            for label, lines in (
                    ("M-1500", ["x" * 1500]),
                    ("M-1501", ["y" * 1501]),
                    ("M-15000", [f"https://host.example.invalid/{n:02d}/" + "z" * 360 + f" <- work/pasted-{n}.md (pasted by the person)"
                                 for n in range(40)]),
                    ("M-CYR", ["https://" + "".join(chr(c) for c in (0x43f, 0x440, 0x438)) + ".example.invalid/" + chr(0x43f) * 8 + "/x" * 900 + " " + "<- work/p.md (pasted by the person)"])):
                for caller in ("_answer_s1_gap", "record_gaps"):
                    notes = []
                    driver.record_pasted = lambda ids, words, _l=lines: list(_l)
                    driver.answer_row = lambda note, words, **kw: notes.append(note)
                    if caller == "_answer_s1_gap":
                        taken = driver._answer_s1_gap(fenced, {"sources": ["SRC-1"], "classes": []}, "q", "S1", "S1-qa-scout-1")
                    else:
                        taken = driver.record_gaps("q", fenced, ids=["SRC-1"])
                    check_eq(f"{label} {caller}: the fenced answer is taken", taken, True)
                    check_eq(f"{label} {caller}: the note holds every name whole", notes,
                             ["S1 material supplied by the person: " + "; ".join(lines)])
        finally:
            driver.record_pasted, driver.answer_row = saved_pasted, saved_row
        for size in (1500, 1501):
            argv = []
            saved_py = driver.py
            driver.py = lambda *a, **k: (argv.append(list(a)), (1, "stop"))[1]
            try:
                driver._accept_gap_kinds("skip all like these", ["SRC-1"], ["unreachable"],
                                         "- " + "q" * (size - 2), "qa-factory/artifacts/QA-J6/work/source-inventory.json")
            except Exception:  # the refusal of the stub is a held question; the argument is what is checked
                pass
            finally:
                driver.py = saved_py
            shown_arg = argv[0][argv[0].index("--shown-text") + 1]
            check_eq(f"S-{size} the shown text reaches accept-gap whole", len(shown_arg), size)

        # F1: `ask_person` without a question is the conductor failing its own contract.
        driver.pass_to_person({"action": "ask_person", "question": "", "did": ""},
                              "conductor", "S1", "S1-qa-scout-1")
        check("an empty ask_person is not a question for the person", True)
        try:
            driver.pass_to_person({"action": "ask_person", "question": "Which stand?", "why_person": "access", "checked": "the refusal"},
                                  "halt", "S5", "S5-qa-runner-1")
            check("a real question still reaches the person", False)
        except story_run.Person as person:
            check_eq("in the conductor's own words", person.text, "Which stand?")
    finally:
        harness.cleanup(root)


def refusal_every_action_has_a_move() -> None:
    # --- every state the controller can return has a move on this side (FR-42) ---------------
    # Not a list somebody keeps up to date: the actions are read out of the controller's own
    # source, so an action added there fails this check until the driver answers it. Three were
    # missing when this was written - `observe_environment_job` (the controller's FIRST branch),
    # `handoff_ready` and `rollover_pending` - and each of them ended as "the driver has no move
    # for X" -> conductor -> a question to a person.
    controller_src = (harness.SCRIPTS / "controller.py").read_text(encoding="utf-8")
    body = controller_src[controller_src.index("def _next_action_for_state"):]
    body = body[:body.index("\n    @staticmethod")] if "\n    @staticmethod" in body else body
    # an action built in a module-level helper `_<name>_action(` that the body calls (t-1562 F5: `execute_gate_b` is built in
    # `_execute_gate_b_action`) is read too - otherwise it escapes this census in silence
    for helper in sorted(set(re.findall(r'\b(_\w+_action)\(', body))):
        start_helper = controller_src.find(f"\ndef {helper}(")
        if start_helper >= 0:
            body += controller_src[start_helper:].split("\n\n\n")[0]
    # `where` is story_step's answer, so its own action counts too: the controller names
    # twelve (the orders of gate B among them) and story_step adds `stop` when pipeline.stop_after ends the run.
    step_src = (harness.SCRIPTS / "story_step.py").read_text(encoding="utf-8")
    actions = sorted(set(re.findall(r'"action":\s*"(\w+)"', body))
                     | set(re.findall(r'"action":\s*"(\w+)"', step_src)))
    driver_src = harness.driver_text()
    handled = set(re.findall(r'kind == "(\w+)"', driver_src))
    handled |= {name for group in re.findall(r'kind in \(([^)]*)\)', driver_src)
                for name in re.findall(r'"(\w+)"', group)}
    handled |= set(re.findall(r'action\.get\("action"\) == "(\w+)"', driver_src))
    check("the other side's own sources name sixteen actions (`execute_gate_b` read from its helper; the three of the story held for code)",
          len(actions) == 16 and "execute_gate_b" in actions, str(actions))
    missing = [a for a in actions if a not in handled]
    check("and the driver has a branch for every one of them", not missing,
          f"no branch for {missing}")


    # the former tail of this function pinned the literal `kind == "..."` form inside the body of ONE member (`dispatch_action`):
    # a source pin of one named member, deleted by TD-11 phase 0 (F3, docs/TESTING.md l.94); the census above is the form census

def refusal_active_dispatch() -> None:
    import story_run
    # --- the refusal whose whole answer is "ask `where` again" --------------------------------
    # TP1-13797 run 5: four conductor sessions, $0.53, every one of them answering "No
    # command run - where already resolves it: wait_existing_job".
    check_eq("an active sequential dispatch is a known refusal the driver answers itself",
             story_run.match_known("story_step start (exit 2): story_step: refused - sequential "
                                   "task already has an active dispatch S5-qa-code-critic-2"),
             ("active_dispatch", "continue"))


def refusal_structured_artifact() -> None:
    """t-210 / F-cmp2-16: `story_step finish` refusing the role's STRUCTURED artifact resumes the role's OWN session
    once with the refusal verbatim, then `finish` runs again. INVARIANTS: never the conductor, never a fresh
    dispatch; the same refusal a second time (also after a relaunch: the count is in the state file), or no known
    session, is the person's; a refusal of any length is passed whole; a text with a form problem AND a structured
    problem resumes the role once, not twice and not never."""
    import story_run
    Refusal = story_run.Refusal
    task = "QA-9"
    root, task_root, env = seed(task)

    def lf(prompt: str) -> str:
        return prompt.replace(chr(13) + chr(10), chr(10))     # the prompt crosses stdin: Windows text mode adds CR
    try:
        def refused(dispatch: str, body: str = "") -> str:
            return (f"story_step finish {dispatch} (exit 2):\nstory_step: refused - S3 structured test plan invalid: "
                    "OB-1: sufficiency_review required: {author_dispatch_id, input_hash, rationale}, all non-empty; "
                    "OB-1: coverage_links[0] needs candidate_id (CAND-n) or test_ref (a test node id)" + body)

        def driver_at(dispatch: str, session: str = "sess-strategist"):
            driver = driver_for(root, env, task)
            driver.boundary = f"S3:{dispatch}"
            if session:
                driver.state["sessions"][dispatch] = session
            return driver

        def finish_loop(driver, dispatch: str, text: str) -> list:
            """What `guarded` does around `finish`: the move refuses, the retry is `finish` again."""
            ran = []

            def retry():
                ran.append("finish again")
                raise Refusal(text, retry=retry)      # the artifact is still refused

            def move():
                ran.append("finish")
                raise Refusal(text, retry=retry)
            try:
                driver.guarded(move, {"action": "wait_existing_job", "stage": "S3"})
            except story_run.Person as person:
                ran.append(person)
            return ran

        set_control(root, {"resume": {"result": "repaired"}})
        d1 = "S3-qa-test-strategist-1"
        text = refused(d1)
        check_eq("the row: a structured-artifact refusal of `finish` is resumed by the role",
                 story_run.match_known(text), ("structured_artifact", "resume_structured"))
        names = [row[0] for row in story_run.KNOWN_REFUSALS]
        check("POSITION: after form_vocabulary and before missing_output",
              names.index("form_vocabulary") < names.index("structured_artifact") < names.index("missing_output"), str(names))
        check("the S1 source-collection refusal is not this row",
              (story_run.match_known("story_step: refused - S1 source collection pending/invalid: x") or ("",))[0]
              != "structured_artifact")

        # (1) one resume of the role's own session with the refusal verbatim, then `finish` again
        before = len(stub_calls(root))
        driver = driver_at(d1)
        ran = finish_loop(driver, d1, text)
        calls = stub_calls(root)[before:]
        check_eq("(1) the role's own session is resumed once, and nothing else is called",
                 [(c["kind"], c["resume"]) for c in calls], [("resume", "sess-strategist")])
        check_in("(1) the prompt holds the refusal verbatim", text.strip(), lf(calls[0]["prompt"]))
        check_in("(1) and the one sentence", "Repair the named fields in the artifact, change nothing else", calls[0]["prompt"])
        check_eq("(1) `finish` runs again after the resume", ran[:2], ["finish", "finish again"])
        check_eq("(1) the count is in the state file, keyed by dispatch",
                 json.loads((task_root / "state/driver-state.json").read_text(encoding="utf-8")).get("structured_resumes"), {d1: 1})

        # (2) the same refusal again: a Person with the refusal verbatim, no conductor, no new dispatch
        person = ran[-1]
        check("(2) the second refusal is the person's", isinstance(person, story_run.Person), repr(ran))
        check_eq("(2) its details are the refusal, verbatim", person.details, text)
        check_eq("(2) one resume in all, no conductor, no new role", [c["kind"] for c in stub_calls(root)[before:]], ["resume"])
        # the count survives a relaunch (exit 3, a new driver over the same state file)
        before = len(stub_calls(root))
        again = driver_at(d1, session="")
        ran = finish_loop(again, d1, text)
        check("(2) a relaunched driver asks at once", isinstance(ran[-1], story_run.Person), repr(ran))
        check_eq("(2) and calls nothing", len(stub_calls(root)) - before, 0)

        # (3) no known session: the person, nothing is called
        before = len(stub_calls(root))
        d3 = "S3-qa-test-strategist-3"
        ran = finish_loop(driver_at(d3, session=""), d3, refused(d3))
        check("(3) no session known: the person", isinstance(ran[-1], story_run.Person), repr(ran))
        check_eq("(3) nothing is called", len(stub_calls(root)) - before, 0)

        # (4) a refusal of 7,000 characters is passed whole
        d4 = "S3-qa-test-strategist-4"
        big = refused(d4, "".join(f"; OB-{n}: sufficiency_review required: {{author_dispatch_id, input_hash, rationale}}"
                                 for n in range(2, 90)) + "; OB-LAST: the final named field")
        check("(4) fixture: over 7,000 characters", len(big) > 7000, str(len(big)))
        before = len(stub_calls(root))
        driver = driver_at(d4)
        driver.handle_refusal(Refusal(big, retry=lambda: None))
        calls = stub_calls(root)[before:]
        check_in("(4) the prompt holds all of it, down to the last named field", big.strip(), lf(calls[0]["prompt"]))

        # (5) a form problem and a structured problem in ONE text: the role is resumed once, with the whole text
        d5 = "S3-qa-test-strategist-5"
        combined = (f"story_step finish {d5} (exit 2):\nhandoff_check: handover form {d5}.yaml is not ready: "
                    "scope[0] is empty\nstory_step: refused - S3 structured test plan invalid: OB-1: sufficiency_review required")
        check_eq("(5) fixture: the table's first match is the form row",
                 story_run.match_known(combined), ("handover_form", "resume_handoff"))
        before = len(stub_calls(root))
        ran = finish_loop(driver_at(d5), d5, combined)
        calls = stub_calls(root)[before:]
        check_eq("(5) the role is resumed ONCE, in its own session", [(c["kind"], c["resume"]) for c in calls],
                 [("resume", "sess-strategist")])
        check_in("(5) with the whole text", combined.strip(), lf(calls[0]["prompt"]))
        check("(5) and the second refusal is the person's", isinstance(ran[-1], story_run.Person), repr(ran))
    finally:
        harness.cleanup(root)


def refusal_gate_stage_row() -> None:
    """t-211 (F0, C9): `stage_done` refusing to RECORD a stage in front of a gate ("stands in front of gate") is the
    driver's own to go on over - story_step has already had the controller accept the stage, so there is nothing to
    retry and the conductor would only say `continue` ($0.11-0.43, twice per gate stage in cmp2). The row is FIRST in
    the table (the text carries up to four rehearsal findings, whose words can hold a later row's phrase), and
    `handle_refusal` lets it go on ONLY while the controller's stage is `completed`; what the refused finish skipped
    (S4's case appendix, S8's report rebuild) is owed at gate entry."""
    import story_run
    Refusal = story_run.Refusal
    task = "QA-9"
    root, task_root, env = seed(task)

    def refused(stage: str, inside: str = "") -> str:
        gate = {"S4": "A", "S8": "B"}[stage]
        return (f"story_step finish {stage}-qa-case-critic-1 (exit 2):\nstage_done: {stage} stands in front of gate {gate}, and "
                f"the rehearsal (`gate_preflight.py --task QA-9 --gate {gate}`) still has 4 thing(s) the FACTORY has to repair "
                f"before anyone is asked: {inside}one; two; three; four. Repair them, then close the stage. If a person decided "
                f"to go to the gate anyway: `waiver.py --task QA-9 --stage {stage} --block \"gate rehearsal\" --decision "
                f"\"<their words>\"`.\nstory_step: stage_done refused {stage} (exit 2); the refusal above is the halt")

    def set_stage(stage: str, status: str) -> None:
        path = task_root / "state" / "controller.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["stages"][stage] = {"status": status}
        path.write_text(json.dumps(data), encoding="utf-8")
    try:
        check_eq("M11: the stage_done refusal in front of gate A continues, by the new row",
                 story_run.match_known(refused("S4")), ("gate_stage", "continue"))
        check_eq("and the one in front of gate B", story_run.match_known(refused("S8")), ("gate_stage", "continue"))
        check_eq("C9: the row is the first a rehearsal finding's words can match (only `committed_event`, which keys on "
                 "an event already in the journal, stands before it)",
                 [row[0] for row in story_run.KNOWN_REFUSALS][:2], ["committed_event", "gate_stage"])
        for phrase in ("STORY BUDGET: past its ceiling", "expected_revision 4", "executor unavailable", "readiness: stand missing",
                       "report check: damaged", "no person has reviewed the source decisions", "is not in this build",
                       "sequential task already has an active dispatch", "is not the handoff form", "already accepted"):
            check_eq(f"C9: a finding that holds `{phrase}` does not take the refusal to a later row",
                     (story_run.match_known(refused("S4", phrase + "; ")) or ("",))[0], "gate_stage")
        check("the row names nothing but its own phrase: a refusal that is not this one is not caught",
              (story_run.match_known("stage_done: S4 closes without it") or ("",))[0] != "gate_stage")

        # the controller's own stage decides: completed -> the driver goes on, with no conductor
        calls = []
        driver = driver_for(root, env, task)
        driver.conductor = lambda text, *, words="", files=None, words_file=None: calls.append(text) or {"action": "continue", "did": "stub"}
        set_stage("S4", "completed")
        driver.boundary = "S4:S4-qa-case-critic-1"
        with contextlib.redirect_stdout(io.StringIO()):
            outcome = driver.handle_refusal(Refusal(refused("S4"), retry=lambda: None))
        check_eq("a completed S4: `continue`, and the conductor is not called", (outcome, calls), ("continue", []))
        check_in("it is journalled as the known row", "known:gate_stage",
                 json.dumps(jsonl(task_root / "state/conductor.jsonl")))
        check_eq("C10: the case appendix S4's refused finish skipped is owed at gate entry (kept in the state file)",
                 sorted(json.loads((task_root / "state/driver-state.json").read_text(encoding="utf-8"))["gate_entry_owed"]), ["S4"])
        set_stage("S8", "completed")
        driver.boundary = "S8:S8-qa-doc-scribe-1"
        with contextlib.redirect_stdout(io.StringIO()):
            outcome = driver.handle_refusal(Refusal(refused("S8")))
        check_eq("a completed S8: the same, and the report rebuild is owed too",
                 (outcome, calls, sorted(driver.state["gate_entry_owed"])), ("continue", [], ["S4", "S8"]))
        # a stage the controller still holds open is NOT this refusal's case: the conductor, as before the row
        set_stage("S4", "running")
        driver = driver_for(root, env, task)
        driver.conductor = lambda text, *, words="", files=None, words_file=None: calls.append(text) or {"action": "continue", "did": "stub"}
        driver.state["gate_entry_owed"] = {}
        driver.boundary = "S4:S4-qa-case-critic-1"
        with contextlib.redirect_stdout(io.StringIO()):
            outcome = driver.handle_refusal(Refusal(refused("S4")))
        check_eq("an S4 the controller holds open: the conductor is called, nothing is owed",
                 (outcome, len(calls), driver.state["gate_entry_owed"]), ("continue", 1, {}))
        check_in("with the refusal", "stands in front of gate A", calls[0])
        set_stage("S4", "pending")
        driver.boundary = "S4:S4-qa-case-critic-1"
        with contextlib.redirect_stdout(io.StringIO()):
            driver.handle_refusal(Refusal(refused("S4", "S4 pending; ")))
        check_eq("a stage that is not even running: the conductor too", len(calls), 2)
        data = json.loads((task_root / "state" / "controller.json").read_text(encoding="utf-8"))
        data["stages"].pop("S4")
        (task_root / "state" / "controller.json").write_text(json.dumps(data), encoding="utf-8")
        driver.state["window_rounds"] = {}      # the series holds two conductor rounds already (WINDOW_ROUND_CAP): a third distinct text would be capped
        with contextlib.redirect_stdout(io.StringIO()):
            driver.handle_refusal(Refusal(refused("S4", "S4 unknown; ")))
        check_eq("a stage the controller does not know: the conductor too", len(calls), 3)
        # FV1-22 N2: the conductor-round stop covers every stage - the IDENTICAL refusal again is the person's, no conductor
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                again = driver.handle_refusal(Refusal(refused("S4", "S4 unknown; ")))
        except story_run.Person as stop:
            again = stop
        check("N2: the identical repeat of a refusal goes to the person", isinstance(again, story_run.Person), repr(again))
        check_eq("and the conductor is not called a fourth time", len(calls), 3)
    finally:
        os.chdir(harness.PLUGIN_ROOT)
        harness.cleanup(root)


def refusal_committed_event_recovers() -> None:
    """legacy-2406 W2 (M3): `controller.py` refuses with "event committed; ...; do not repeat the action" when the event
    is in the journal and only what comes after it failed. The door is a command code can run (`--operation recover`), so
    the conductor is not asked (FR-48, P3) - and the action is NOT repeated: the answer is `continue`, back to `where`.

    S1 (the table's order, `committed_event` -> `gate_stage` -> `report_check`): a text holding both a committed-event
    phrase and `stands in front of gate` routes to `committed_event`; a rehearsal text holding `STORY BUDGET` /
    `expected_revision` plus `stands in front of gate` still routes to `gate_stage` (`refusal_gate_stage_row` holds the
    rest of that row). S3: `conductor_round` takes `recover_failed` and `committed`; a caller that passes neither
    (`hand_to_conductor`) gets the call it always got."""
    import story_run
    task = "QA-9"
    committed = {
        "derived view": ('controller dispatch (exit 2):\n{"error": "event committed; derived view not '
                         'refreshed (OSError: disk full); do not repeat the action; `controller.py '
                         '--task-root T --operation recover` refreshes it (recorded in '
                         'state/dashboard-deferred.json)"}'),
        "projection": ('controller dispatch (exit 2):\n{"error": "event committed; projection stale; '
                       'recover, do not repeat action"}'),
        "projection on a replay": ('controller dispatch (exit 2):\n{"error": "event already committed; '
                                   'projection stale; recover, do not repeat action"}'),
        # The failure text may itself contain words another row knows: the committed event is the
        # fact that decides.
        "a failure that looks like another row": (
            'controller accept (exit 2):\n{"error": "event committed; derived view not refreshed '
            '(OSError: stage already completed, expected_revision 3); do not repeat the action"}'),
        # The third text the store itself produces (`event_store._run_after_commit`): the step after the commit failed.
        "the step that follows the commit": (
            'controller dispatch (exit 2):\n{"error": "event committed; the step that follows it did not finish '
            '(OSError: disk full); do not repeat the action"}'),
        "the step that follows, with a word of another row": (
            'controller accept (exit 2):\n{"error": "event committed; the step that follows it did not finish '
            '(RuntimeError: expected_revision 3, STORY BUDGET); do not repeat the action"}')}
    for label, text in committed.items():
        check_eq(f"{label}: the refusal is a known row", (story_run.match_known(text) or ("", ""))[1], "recover")

    # S1: the order of the table's head, and the two texts that decide it
    check_eq("S1: the table opens with committed_event, gate_stage, report_check, in this order",
             [row[0] for row in story_run.KNOWN_REFUSALS][:3], ["committed_event", "gate_stage", "report_check"])
    both = ('controller accept (exit 2):\n{"error": "event committed; derived view not refreshed (OSError: S4 stands in '
            'front of gate A); do not repeat the action"}')
    check_eq("S1: a text holding a committed-event phrase AND `stands in front of gate` is the committed event",
             story_run.match_known(both), ("committed_event", "recover"))
    rehearsal = ("story_step finish S4-qa-case-critic-1 (exit 2):\nstage_done: S4 stands in front of gate A, and the "
                 "rehearsal still has 2 thing(s) the FACTORY has to repair: STORY BUDGET: past its ceiling; "
                 "expected_revision 4.")
    check_eq("S1: a rehearsal text holding STORY BUDGET / expected_revision plus `stands in front of gate` is gate_stage",
             story_run.match_known(rehearsal), ("gate_stage", "continue"))

    root, task_root, env = seed(task)
    try:
        driver = driver_for(root, env, task)
        driver.boundary = "S1"
        for label, text in committed.items():
            ran, repeated, before = [], [], len(stub_calls(root))

            def recover(operation, *args, input_data=None, _ran=ran):
                _ran.append(operation)
                return {}
            driver.controller = recover

            def move(_repeated=repeated, _text=text):
                _repeated.append(1)
                raise story_run.Refusal(_text)
            driver.guarded(move, {"action": "prepare_stage", "stage": "S1"})
            check_eq(f"{label}: the driver ran recover once", ran, ["recover"])
            check_eq(f"{label}: and did not repeat the committed action", repeated, [1])
            check_eq(f"{label}: no conductor session was spent", len(stub_calls(root)) - before, 0)
            check_eq(f"{label}: conductor.jsonl names the table row",
                     jsonl(task_root / "state/conductor.jsonl")[-1]["action"], "known:committed_event")

        # recover itself refused: that is a refusal nothing here knows, so it goes where an unknown
        # one goes today - to the conductor - and recover is not run a second time.
        set_control(root, {"conductor": {"action": "ask_person", "question": "recover failed; what now?",
                                         "did": "read where"}})
        ran, before, defects = [], len(stub_calls(root)), []

        def failing_recover(operation, *args, input_data=None):
            ran.append(operation)
            raise story_run.Refusal("controller recover (exit 2):\nthe moon is down and nobody knows why")
        driver.controller = failing_recover
        real_py = driver.py
        driver.py = lambda script, *a, **k: (defects.append(a), (0, ""))[1] if script == "log_append.py" and "defect_found" in a \
            else real_py(script, *a, **k)
        try:
            driver.guarded(lambda: (_ for _ in ()).throw(story_run.Refusal(committed["projection"])),
                           {"action": "prepare_stage", "stage": "S1"})
            check("a second failure reaches the conductor and its answer", False)
        except story_run.Person as person:
            # C1-1: a conductor `ask_person` with NO options is not a usable answer: the priced fallback question is raised
            # instead, and the factory's own defect is journalled once (its words are not shown as a question).
            check_eq("the conductor's ask_person with no options ends the loop in the fallback question",
                     (person.kind, list(person.offered)), ("conductor", ["retry", "go on", "stop"]))
            check_not_in("and the conductor's bare question text is not shown", "recover failed; what now?", person.text)
            for label in ("the factory:", "you:", "the story:"):
                check_in(f"and every answer has the line `{label}`", label, person.text)
            check_eq("and exactly one defect_found is journalled", len(defects), 1)
        driver.py = real_py
        check_eq("recover was run once, not looped on", ran, ["recover"])
        check_eq("and the conductor was asked once", len(stub_calls(root)) - before, 1)
        check_in("with recover's own refusal in front of it", "the moon is down", stub_calls(root)[-1]["prompt"])
        check_in("and the refusal it was run for, so the conductor can judge the pair",
                 "event committed; projection stale", stub_calls(root)[-1]["prompt"])

        # The committed action is NEVER run again by any path: the conductor's `retry` is read as
        # `continue` (back to `where`), because `refusal.retry` would write the event twice.
        set_control(root, {"conductor": {"action": "retry", "did": "looked at recover's refusal"}})
        ran, again, moves, before = [], [], [], len(stub_calls(root))
        driver.boundary = "S2"  # the conductor's allowance is per boundary

        def committed_move():
            moves.append(1)
            raise story_run.Refusal(committed["derived view"], retry=lambda: again.append("re-ran"))
        driver.guarded(committed_move, {"action": "prepare_stage", "stage": "S1"})
        check_eq("recover failed: the conductor was asked, and said retry", len(stub_calls(root)) - before, 1)
        check_eq("the committed action was not run again", again, [])
        check_eq("and the move itself was made once", moves, [1])
        prompt = stub_calls(root)[-1]["prompt"]
        check_in("the conductor was shown the refusal the event came with", "derived view not refreshed", prompt)
        check_in("and recover's refusal beside it", "the moon is down", prompt)

        # What `retry` means for any OTHER row is unchanged: `dead_dispatch` is a refusal of an
        # action that never committed anything, so recover failing and the conductor saying
        # `retry` re-runs that action - there is no event it could write twice.
        ran, again, moves = [], [], []
        driver.boundary = "S5"

        def dead_move():
            moves.append(1)
            raise story_run.Refusal("story_step start (exit 2): wait_existing_job S5-qa-automator-1 returned",
                                    retry=lambda: again.append("re-ran"))
        driver.guarded(dead_move, {"action": "prepare_stage", "stage": "S5"})
        check_eq("dead_dispatch: recover was run once", ran, ["recover"])
        check_eq("and a conductor `retry` still re-runs its refused action", again, ["re-ran"])
        check_in("with both texts in front of the conductor", "wait_existing_job",
                 stub_calls(root)[-1]["prompt"])
        check_in("and recover's", "the moon is down", stub_calls(root)[-1]["prompt"])

        # F1: every committed text is the committed event - the third one too: recover failing and the conductor saying
        # `retry` never repeats the action (today: no row, `committed` stays False, `retry` runs `refusal.retry`).
        for label in ("the step that follows the commit", "the step that follows, with a word of another row"):
            driver.controller = failing_recover
            driver.conductor_calls = {}
            driver.boundary = "S2"
            ran, again, moves = [], [], []

            def third_move(_text=committed[label]):
                moves.append(1)
                raise story_run.Refusal(_text, retry=lambda: again.append("re-ran"))
            driver.guarded(third_move, {"action": "prepare_stage", "stage": "S1"})
            check_eq(f"F1 {label}: recover was run once", ran, ["recover"])
            check_eq(f"F1 {label}: the conductor's `retry` did not run the committed action again", again, [])
            check_eq(f"F1 {label}: and the move was made once", moves, [1])

        # F2: a committed finish over a stage the controller has CLOSED skipped the stage's tail: the same mark
        # `gate_stage` leaves, so the gate entry runs it - once. A stage that is not completed is not marked, and a
        # `recover` that refuses keeps the conductor's path with no mark.
        def set_stage(stage: str, status: str) -> None:
            path = task_root / "state" / "controller.json"
            data = json.loads(path.read_text(encoding="utf-8"))
            data["stages"][stage] = {"status": status}
            path.write_text(json.dumps(data), encoding="utf-8")

        def finish_refused(stage: str, text: str):
            def move():
                raise story_run.Refusal(f"story_step finish {stage}-qa-case-critic-1 (exit 2):\n" + text)
            return move

        for label in ("derived view", "projection", "the step that follows the commit"):
            driver = driver_for(root, env, task)
            driver.state["gate_entry_owed"] = {}
            ran = []
            driver.controller = lambda operation, *args, input_data=None, _ran=ran: _ran.append(operation) or {}
            set_stage("S4", "completed")
            driver.boundary = "S4:S4-qa-case-critic-1"
            with contextlib.redirect_stdout(io.StringIO()):
                driver.guarded(finish_refused("S4", committed[label]), {"action": "prepare_stage", "stage": "S4"})
                driver.guarded(finish_refused("S4", committed[label]), {"action": "prepare_stage", "stage": "S4"})
            check_eq(f"F2 {label}: recovered twice (one per refusal), each time with no conductor", ran, ["recover", "recover"])
            check_eq(f"F2 {label}: a completed S4 is owed to gate A's entry, with one mark",
                     sorted(driver.state["gate_entry_owed"]), ["S4"])
            check_eq(f"F2 {label}: the mark is kept in the state file",
                     sorted(json.loads((task_root / "state/driver-state.json").read_text(encoding="utf-8")).get("gate_entry_owed") or {}),
                     ["S4"])
            rendered = []
            driver.render_appendix = lambda _r=rendered: _r.append(1)
            driver.gate_entry_steps("A")
            driver.gate_entry_steps("A")
            check_eq(f"F2 {label}: the gate entry runs the owed appendix once, not once per recovery", rendered, [1])
        driver = driver_for(root, env, task)
        driver.state["gate_entry_owed"] = {}
        rebuilt = []
        driver.rebuild_report = lambda: rebuilt.append(1)
        driver.controller = lambda operation, *args, input_data=None: {}
        set_stage("S8", "completed")
        driver.boundary = "S8:S8-qa-doc-scribe-1"
        with contextlib.redirect_stdout(io.StringIO()):
            driver.guarded(finish_refused("S8", committed["projection"]), {"action": "prepare_stage", "stage": "S8"})
        driver.gate_entry_steps("B")
        check_eq("F2: a completed S8 owes the report rebuild at gate B's entry", rebuilt, [1])
        for status in ("running", "pending"):
            driver = driver_for(root, env, task)
            driver.state["gate_entry_owed"] = {}
            driver.controller = lambda operation, *args, input_data=None: {}
            set_stage("S4", status)
            driver.boundary = "S4:S4-qa-case-critic-1"
            with contextlib.redirect_stdout(io.StringIO()):
                driver.guarded(finish_refused("S4", committed["derived view"]), {"action": "prepare_stage", "stage": "S4"})
            check_eq(f"F2: a stage that is `{status}` is not marked", driver.state["gate_entry_owed"], {})
        driver = driver_for(root, env, task)
        driver.state["gate_entry_owed"] = {}
        set_stage("S4", "completed")
        set_control(root, {"conductor": {"action": "continue", "did": "read where"}})
        driver.controller = failing_recover
        driver.conductor_calls = {}
        driver.boundary = "S4:S4-qa-case-critic-1"
        with contextlib.redirect_stdout(io.StringIO()):
            driver.guarded(finish_refused("S4", committed["derived view"]), {"action": "prepare_stage", "stage": "S4"})
        check_eq("F2: `recover` refused: the conductor's path, and no mark", driver.state["gate_entry_owed"], {})

        # S3: `conductor_round` itself. The gate-entry caller passes neither argument, and its `retry` stays `retry`.
        driver.conductor_calls = {}
        driver.boundary = "S3"
        calls = []
        driver.conductor = lambda text, *, words="", files=None, words_file=None: calls.append(text) or {"action": "retry", "did": "stub"}
        with contextlib.redirect_stdout(io.StringIO()):
            plain = driver.conductor_round(story_run.Refusal(committed["projection"]), "S3")
            held = driver.conductor_round(story_run.Refusal(committed["projection"]), "S3", committed=True,
                                          recover_failed="the moon is down")
        check_eq("S3: with neither argument a `retry` stays `retry` (the gate-entry caller's call)", plain, "retry")
        check_eq("S3: with `committed` a `retry` is read as `continue`", held, "continue")
        check_not_in("S3: with neither argument the conductor is shown the refusal alone", "was run for it and refused too",
                     calls[0])
        check_in("S3: with `recover_failed` it is shown both texts", "the moon is down", calls[1])
        check_in("S3: and the refusal beside it", "event committed; projection stale", calls[1])
    finally:
        harness.cleanup(root)


def main() -> None:
    run_scenarios([], [
        refusal_round_trip_gate_and_routing,
        refusal_table,
        refusal_markers,
        refusal_dispatch_field,
        refusal_judge_and_source_gaps,
        refusal_every_action_has_a_move,
        refusal_active_dispatch,
        refusal_structured_artifact,
        refusal_gate_stage_row,
        refusal_committed_event_recovers,
    ])
    harness.finish("test_story_run_refusals_core")


# split: runner piece 1
if __name__ == "__main__":
    main()
