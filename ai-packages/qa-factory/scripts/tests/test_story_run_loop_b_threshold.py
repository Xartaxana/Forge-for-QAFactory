"""threshold: a part of test_story_run_loop_b.py, split by tools/test_split.py (TD-11c). The shared helpers are in story_run_loop_b_common."""
import json
import re
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness  # noqa: E402
from harness import check, check_eq, check_in  # noqa: E402
from story_run_common import run_scenarios, check_not_in_text, eq, rules_broken, seed
from story_run_loop_b_common import QStub, Q_TASK, ROLE_OF, q_load  # noqa: E402


def q_register(task_root: Path, ids, total: int = 24, requirements: dict | None = None) -> None:
    """The S2 role's register: each id is one open question with two readings."""
    rows = []
    for qid in ids:
        row = {"id": qid, "question": f"what should happen for {qid}?", "severity": "major",
               "readings": [{"reading": "the first reading", "from": "the ticket", "if_chosen": "x"},
                            {"reading": "the second reading", "from": "the code", "if_chosen": "y"}]}
        if requirements and qid in requirements:
            row["requirements"] = requirements[qid]
        rows.append(row)
    (task_root / "work").mkdir(parents=True, exist_ok=True)
    (task_root / "work" / "requirements-readiness.json").write_text(
        json.dumps({"verdict": "blocked", "register": {"total": total}, "open_questions": rows}), encoding="utf-8")


def question_stop_road() -> None:
    """R15 / R17 / Q8 on one story: the stop, the answer, the resume, the informed pass, the re-stop."""
    import story_run
    root, task_root, env = seed(Q_TASK)
    try:
        q_register(task_root, [f"Q{i}" for i in range(1, 8)])        # 7 open: over the default of 6
        s = QStub(root, env)
        d = s.driver
        person = s.run_role()
        check("stop: seven open questions end a role's handoff in a question", isinstance(person, story_run.Person))
        check_eq("stop: kind, stage, dispatch", (person.kind, person.stage, person.dispatch),
                 ("questions", "S2", s.dispatch))
        check_eq("stop: the stage is halted and was never closed - no finish ran before the stop (B2 row mutation b)",
                 (s.statuses(), s.finishes()), (["halted"], []))
        check_in("stop: the text says how many questions are to be decided", "7 questions to decide", person.text)
        check("stop: every open question is in the text, none cut (the gate's cap was six)",
              all(f"Q{i}" in person.text for i in range(1, 8)))
        check_in("stop: the limit is named as the factory's default, not as the project's", "default threshold", person.text)
        check_not_in_text("stop: no dispatch id and no closed stop-reason code in the words",
                          (s.dispatch, "over_threshold"), person.text)
        stop = d.state["question_stop"]
        check_eq("stop: driver state holds stage, dispatch, count", (stop["stage"], stop["dispatch"], stop["count"]),
                 ("S2", s.dispatch, 7))
        check("stop: and the instant, the share (unknown here) and no answer yet",
              bool(stop["at"]) and stop["share"] is None and "answered" not in stop)
        check("stop: the row hashes the person is shown are kept (a register changed before the answer stays visible)",
              sorted(stop["shown"]) == [f"Q{i}" for i in range(1, 8)] and all(len(h) == 64 for h in stop["shown"].values()))
        disk = json.loads((task_root / "state/driver-state.json").read_text(encoding="utf-8"))
        check_eq("stop: it is on disk, in the driver's state, not in the role's file", disk["question_stop"]["count"], 7)
        check("stop: the role's own readiness file is untouched (no `stop` block written by code)",
              "stop" not in json.loads((task_root / "work/requirements-readiness.json").read_text(encoding="utf-8")))
        check("stop: the role's result is kept for the resume, not consumed",
              (task_root / f"state/driver-runs/{s.dispatch}.json").is_file())

        # --- the console text, once (the question the person reads) ---
        d.ask(person)
        shown = (task_root / "state/driver-question.md").read_text(encoding="utf-8")
        check_in("ask: the question file says which kind it is", "kind: questions", shown)
        check_eq("ask: the text obeys human-questions.md", rules_broken(shown), [])

        # --- the answer: tokens by code, words whole, no conductor --------------------------------
        words = ("Q1: a\nQ2: b\nQ3: not needed\nQ4: c\nQ9: a\nQ5 I do not know yet, ask the owner.\n"
                 "Q6: a, but only for the admin role\n")
        said = s.answer(root, words)
        got = q_load(task_root)
        check_eq("answer: Q1 is answered with reading a, asked at the S2 stop",
                 (got["Q1"]["status"], got["Q1"]["reading"], got["Q1"]["where"]), ("answered", "a", "S2 stop"))
        check_eq("answer: Q2 is answered with reading b", (got["Q2"]["status"], got["Q2"]["reading"]), ("answered", "b"))
        check_eq("answer: Q3 is `not needed`", got["Q3"]["status"], "not_needed")
        check("answer: the words are kept WHOLE in the record (FR-8), not the line", got["Q1"]["words"] == words.strip())
        check_eq("answer: the record stores the hash of the row AS SHOWN", got["Q1"]["record_row_hash"], stop["shown"]["Q1"])
        check("answer: a letter beyond the readings is not recorded - it stays open",
              got["Q4"]["status"] == "open" and "beyond its 2 readings" in said)
        check("answer: prose about a question, and a letter followed by words, are not tokens - they stay open",
              got["Q5"]["status"] == "open" and got["Q6"]["status"] == "open")
        check_in("answer: an id that is not open is printed back as not recognised", "not recognised as open questions", said)
        check_in("answer: and is named", "Q9", said)
        check("answer: nothing is recorded for the unknown id", "Q9" not in got)
        check_eq("answer: the words wait for the role's own session, whole", d.state["pending_words"].get(s.dispatch), words.strip())
        check_eq("answer: the answer is the informed pass - the count and share the person saw are kept",
                 (d.state["question_stop"]["answered"]["count"], d.state["question_stop"]["answered"]["share"]), (7, None))
        check("answer: the question flag is cleared", not d.state.get("asked"))
        check("answer: the words are journalled as a human answer by code",
              any(sc == "log_append.py" and "human_answer" in a for sc, a in s.py_calls))
        check_eq("answer: the conductor was called once, for the lines code could not read", len(s.conductor_calls), 1)
        check_in("answer: and it was told what code recorded first (FR-48)", "recorded by code: Q1: a, Q2: b, Q3: not needed",
                 s.conductor_calls[0][0])

        # --- the resume: the SAME session, its own text, no conductor, halted -> running -> done ------
        check_eq("resume: the role's session is the one the driver stored", d.state["sessions"][s.dispatch], "sess-1")
        s.claude_calls.clear()
        d.resume_role("S2", s.role, s.dispatch, d.state["pending_words"][s.dispatch])
        check_eq("resume: ONE call, in the existing session, never a new dispatch (B2 row mutation c)",
                 [(c["kind"], c["resume"]) for c in s.claude_calls], [("role", "sess-1")])
        prompt = s.claude_calls[0]["prompt"]
        check_in("resume: it has its own text", 'The person answered the open questions: "Q1: a', prompt)
        check_in("resume: and says the answers are recorded and not to ask again",
                 f"Their answers are recorded; continue your dispatch {s.dispatch} on them — do not ask them again.", prompt)
        check_not_in_text("resume: not `from where you stopped`, said to a role that had finished",
                          ("from where you stopped",), prompt)
        check_eq("resume: the stage goes halted -> running, then the finish closes it (E-7)",
                 (s.statuses(), len(s.finishes())), (["halted", "running"], 1))
        check_eq("resume: no conductor on the resume (B2 row mutation a)", len(s.conductor_calls), 1)
        check("resume: the words are consumed and the resume mark is gone",
              s.dispatch not in d.state["pending_words"] and "resume" not in d.state["question_stop"])

        # --- the informed pass (Q8): the same count does not stop again, only a larger one --------------
        q_register(task_root, [f"Q{i}" for i in range(1, 11)])       # Q4..Q10 open = 7, the count answered at
        halts = s.statuses().count("halted")
        try:
            d.question_threshold("S2", s.role, s.dispatch)
            same = None
        except story_run.Person as raised:
            same = raised
        check("informed pass: 7 open after an answer at 7 - NO second stop (the same count)",
              same is None and s.statuses().count("halted") == halts)
        q_register(task_root, [f"Q{i}" for i in range(1, 12)])       # Q4..Q11 open = 8
        try:
            d.question_threshold("S2", s.role, s.dispatch)
            again = None
        except story_run.Person as raised:
            again = raised
        check("informed pass: 8 open, one more than the person answered at - the stop comes back", again is not None)
        if again is not None:
            check_in("re-stop: the changed text says it is still open after the answer, and when",
                     "still open after your answer of ", again.text)
            check_in("re-stop: and what the answer settled (Q1, Q2 answered and Q3 not needed = 3)",
                     "Your answer settled 3 questions", again.text)
            check("re-stop: no answered question is asked again (FR-7)", not re.search(r"\bQ[123]\b", again.text))
            check("re-stop: the still-open ones are all there", all(f"Q{i}" in again.text for i in range(4, 12)))
            check_eq("re-stop: it is recorded at the new count, and the earlier answer is kept",
                     (d.state["question_stop"]["count"], d.state["question_stop"]["answered"]["count"]), (8, 7))
            check_eq("re-stop: the stage is halted again", s.statuses()[-1], "halted")
        check_eq("one conductor call in all of it: the answer's", len(s.conductor_calls), 1)
    finally:
        harness.cleanup(root)


def question_stop_share_and_limits() -> None:
    """Q8 for the SHARE, and the boundaries of `larger_than_answered` (the threshold's own edges are B1's)."""
    import story_run
    larger = story_run.Driver.larger_than_answered
    check("larger: a larger count", larger(8, None, {"count": 7, "share": None}))
    check("larger: the same count is not larger (strictly)", not larger(7, None, {"count": 7, "share": None}))
    check("larger: a smaller count is not larger", not larger(6, None, {"count": 7, "share": None}))
    check("larger: a larger share", larger(3, 0.5, {"count": 3, "share": 0.4}))
    check("larger: the same share is not larger", not larger(3, 0.4, {"count": 3, "share": 0.4}))
    check("larger: an unknown share is never larger (FR-41)", not larger(3, None, {"count": 3, "share": 0.4}))
    check("larger: and is not compared with an unknown one", not larger(3, 0.4, {"count": 3, "share": None}))
    check("larger: a count that was never recorded is not compared", not larger(9, None, {"count": None, "share": None}))
    root, task_root, env = seed(Q_TASK)
    try:
        reqs = {"Q1": ["R-1", "R-2", "R-3"], "Q2": ["R-4", "R-5", "R-6"], "Q3": ["R-7", "R-8", "R-9"]}
        q_register(task_root, ["Q1", "Q2", "Q3"], total=24, requirements=reqs)     # 3 open, 9 of 24 = 0.375 > 1/3
        s = QStub(root, env)
        person = s.run_role()
        check("share: 3 questions are under the count limit but 9 of 24 requirements is over a third - it stops",
              isinstance(person, story_run.Person) and person.kind == "questions")
        check_eq("share: the stop records count and share", (s.driver.state["question_stop"]["count"],
                 round(s.driver.state["question_stop"]["share"], 3)), (3, 0.375))
        s.driver.ask(person)
        s.answer(root, "I will answer all three in words: go with the ticket.")
        try:
            s.driver.question_threshold("S2", s.role, s.dispatch)
            same = None
        except story_run.Person as raised:
            same = raised
        check("share: after a free-word answer the same share does not stop again", same is None)
        q_register(task_root, ["Q1", "Q2", "Q3"], total=24,
                   requirements={"Q1": reqs["Q1"] + ["R-10"], "Q2": reqs["Q2"], "Q3": reqs["Q3"]})   # 10 of 24
        try:
            s.driver.question_threshold("S2", s.role, s.dispatch)
            again = None
        except story_run.Person as raised:
            again = raised
        check("share: a LARGER share (10 of 24) stops again, with the changed text",
              again is not None and "still open after your answer of " in again.text)
    finally:
        harness.cleanup(root)


def question_stop_edges() -> None:
    """The edges of the wiring: (i) a failing count, (ii) the role's own halt, (viii) the person's pass,
    (v) free words, (ix) S3, and the stop at a stage with no stop defined."""
    import question_stop
    root, task_root, env = seed(Q_TASK)
    try:
        q_register(task_root, [f"Q{i}" for i in range(1, 8)])
        s = QStub(root, env)
        # (i) the count itself fails: told, never a stop (P1)
        real = question_stop.over_threshold
        try:
            def broken(*a, **k):
                raise RuntimeError("the thresholds file is gone")
            question_stop.over_threshold = broken
            import contextlib
            import io
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                person = s.run_role()
            check("(i) a count that raises does not stop the factory: the stage closes", person is None and len(s.finishes()) == 1)
            check_in("(i) and the failure is printed as a note", "the question threshold was not checked at S2", out.getvalue())
            check_in("(i) with its cause", "the thresholds file is gone", out.getvalue())
        finally:
            question_stop.over_threshold = real
        # (i) a malformed register is not over: no stop, no crash
        (task_root / "work" / "requirements-readiness.json").write_text("{not json", encoding="utf-8")
        s = QStub(root, env)
        person = s.run_role()
        check("(i) a malformed register is not over: the stage closes", person is None and len(s.finishes()) == 1)
        (task_root / "work" / "requirements-readiness.json").unlink()
        s = QStub(root, env)
        person = s.run_role()
        check("(i) no register at all: nothing to count, the stage closes", person is None and len(s.finishes()) == 1)

        # (ii) the role stopped on its own: the `halt` road only, the threshold does not double-stop
        q_register(task_root, [f"Q{i}" for i in range(1, 8)])
        halting = f"{ROLE_OF['S2']} S2 {Q_TASK} · halt\nR-1 · unresolved · the ticket says two opposite things\n"
        s = QStub(root, env, digest=halting)
        person = s.run_role()
        check_eq("(ii) a role that halted itself is asked by the halt road", getattr(person, "kind", None), "halt")
        check("(ii) and no threshold stop is recorded", "question_stop" not in s.driver.state)
        check_eq("(ii) and the stage is halted once", s.statuses(), ["halted"])

        # (viii) the person's word passes the block, recorded by the waiver itself (FR-4)
        s = QStub(root, env)
        code, out = s.driver.py("waiver.py", "--task", Q_TASK, "--stage", "S3", "--block", "question threshold",
                                "--decision", "go on, I read them")
        eq("(viii) a pass for ANOTHER stage is recorded", code, 0, out)
        person = s.run_role()
        check("(viii) and does not pass this stage", getattr(person, "kind", None) == "questions")
        s.driver.state.pop("question_stop", None)           # the next driver starts without that stop
        s.driver.save_state()
        s = QStub(root, env)
        code, out = s.driver.py("waiver.py", "--task", Q_TASK, "--stage", "S2", "--block", "question threshold",
                                "--decision", "go on, I read them")
        eq("(viii) the pass for this stage is recorded by waiver.py", code, 0, out)
        check_in("(viii) in the story's own file, with the words",
                 "go on, I read them", (task_root / "pipeline.json").read_text(encoding="utf-8"))
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            person = s.run_role()
        check("(viii) with the pass recorded, there is no stop and the stage closes", person is None and len(s.finishes()) == 1)
        check_in("(viii) and the pass is said in the log, with the words", "go on, I read them", out.getvalue())
        check("(viii) no stop was recorded in the driver's state", "question_stop" not in s.driver.state)
    finally:
        harness.cleanup(root)

    # (ix) S3: the strategist's stop; a free-word answer is kept whole and goes to the role
    root, task_root, env = seed(Q_TASK)
    try:
        q_register(task_root, [f"Q{i}" for i in range(1, 9)])
        s = QStub(root, env, stage="S3")
        person = s.run_role()
        check_eq("(ix) S3: the stop is asked at the plan stage", (person.kind, person.stage), ("questions", "S3"))
        check_in("(ix) S3: the batch carries every open question of the register", "8 questions to decide", person.text)
        s.driver.ask(person)
        free = "Go with what the ticket says everywhere, and tell me in the plan what you assumed."
        s.answer(root, free)
        got = q_load(task_root)
        check("(v) free words record nothing by code: no question is marked answered that the person did not name",
              all(q["status"] == "open" for q in got.values()))
        check_eq("(v) the words are kept whole for the role", s.driver.state["pending_words"][s.dispatch], free)
        check_in("(v) and in the driver's answer file, whole", free,
                 (task_root / "state/driver-answers.jsonl").read_text(encoding="utf-8"))
        s.driver.resume_role("S3", s.role, s.dispatch, free)
        check_in("(v) the resume carries them", free, s.claude_calls[-1]["prompt"])
        check_eq("(ix) S3: halted -> running -> done, nothing deleted", (s.statuses(), len(s.finishes())),
                 (["halted", "running"], 1))
    finally:
        harness.cleanup(root)
    root, task_root, env = seed(Q_TASK)
    try:
        q_register(task_root, [f"Q{i}" for i in range(1, 9)])
        s = QStub(root, env, stage="S3")
        s.driver.ask(s.run_role())
        s.answer(root, "Q1: a\nQ2: not needed")
        got = q_load(task_root)
        check_eq("(ix) S3: a token answer is recorded as asked at the S3 stop", (got["Q1"]["where"], got["Q2"]["where"]),
                 ("S3 stop", "S3 stop"))
    finally:
        harness.cleanup(root)


def question_stop_fallbacks() -> None:
    """R17, FR-57, edge (iv): a resume goes to the existing session; with none, or a failed one, the SAME dispatch
    runs again in a new session as a rework whose reason is the words, verbatim. Never both."""
    words = "Q1: a\nand please keep the admin cases apart"
    for label, sid, failing in (("no session id", False, False), ("a session that cannot be resumed", True, True),
                                ("a session that resumes", True, False)):
        root, task_root, env = seed(Q_TASK)
        try:
            q_register(task_root, [f"Q{i}" for i in range(1, 8)])
            s = QStub(root, env)
            d = s.driver
            person = s.run_role()
            d.ask(person)
            s.answer(root, words)
            if not sid:
                d.state["sessions"].pop(s.dispatch, None)
            check_eq(f"{label}: the words wait for the role", d.state["pending_words"][s.dispatch], words)
            reworks, before = [], len(s.claude_calls)
            d.run_role = lambda stage, role, **kw: reworks.append(dict(kw, stage=stage, role=role)) or ("", {})
            if failing:
                s.claude_result = {"result": "", "session_id": "", "stderr": "no such session", "total_cost_usd": 0.0,
                                   "is_error": True, "exit_code": 1}
            d.resume_role("S2", s.role, s.dispatch, words, complete=None)
            if label == "a session that resumes":
                check_eq(f"{label}: no rework, no new dispatch (B2 row mutation c)", reworks, [])
                check_eq(f"{label}: the existing session got the call", [c["resume"] for c in s.claude_calls[before:]], ["sess-1"])
            else:
                check_eq(f"{label}: one rework of the SAME dispatch, reason = the words verbatim",
                         [(r["rework"]["id"], r["rework"]["reason"], r["stage"], r["role"]) for r in reworks],
                         [(s.dispatch, words, "S2", s.role)])
                check_eq(f"{label}: and no resume call reached a session that does not exist",
                         [c["resume"] for c in s.claude_calls[before:]], [] if not sid else ["sess-1"])
                runs = task_root / "state" / "driver-runs"
                check(f"{label}: the saved result is set aside, not deleted, so the role runs again and sees the words",
                      not (runs / f"{s.dispatch}.json").is_file() and (runs / f"{s.dispatch}.stopped.json").is_file())
                check(f"{label}: the words are consumed", s.dispatch not in d.state["pending_words"])
                check_eq(f"{label}: the conductor was called once at the answer, never at the rework or the resume",
                         len(s.conductor_calls), 1)
        finally:
            harness.cleanup(root)


def question_stop_loop_moves() -> None:
    """The loop's moves for a question stop (edge x): an unanswered stop is asked again and never finished
    from the saved result; an answered one is resumed by the loop with the question text."""
    import story_run
    root, task_root, env = seed(Q_TASK)
    try:
        q_register(task_root, [f"Q{i}" for i in range(1, 8)])
        s = QStub(root, env)
        d = s.driver
        person = s.run_role()
        d.ask(person)
        action = {"action": "wait_existing_job", "dispatch_id": s.dispatch}
        before = len(s.finishes())
        try:
            d.dispatch_action(action)
            again = None
        except story_run.Person as raised:
            again = raised
        check("loop: an unanswered stop is asked again", again is not None and again.kind == "questions")
        check_eq("loop: and the saved result is NOT finished over it", len(s.finishes()), before)
        if again is not None:
            check_eq("loop: same stage and dispatch", (again.stage, again.dispatch), ("S2", s.dispatch))
            check_in("loop: the same batch", "7 questions to decide", again.text)
            check_not_in_text("loop: the answer block is not printed twice", ("Answer: write your words",), again.text)
        s.answer(root, "Q1: a\nQ2: a\nQ3: a")
        s.claude_calls.clear()
        d.dispatch_action(action)
        check_eq("loop: an answered stop is resumed by the loop, in the existing session",
                 [(c["kind"], c["resume"]) for c in s.claude_calls], [("role", "sess-1")])
        check_in("loop: with the question text", "The person answered the open questions:", s.claude_calls[0]["prompt"])
        check_eq("loop: halted -> running -> done", (s.statuses(), len(s.finishes())), (["halted", "running"], before + 1))
        check_eq("loop: no conductor", s.conductor_calls, [])
        # a halt answered the old way keeps its own text (the resume mark belongs to a stop only)
        d.state["pending_words"][s.dispatch] = "go on"
        s.claude_calls.clear()
        d.resume_role("S2", s.role, s.dispatch, "go on")
        check_in("loop: an ordinary resume keeps the halt road's text", "from where you stopped", s.claude_calls[0]["prompt"])
    finally:
        harness.cleanup(root)


# --- FV1-3: a free answer to a question pack goes to the conductor -------------------------------------------------------------
# The real answer of the live run (answers/s4-questions-batch-1.md of the factory-vs-free-agent experiment, copied VERBATIM: package tests
# read nothing outside the package). Eighteen lines `Qn: <own words>`, none a token; the driver recorded nothing and said nothing.
FV13_S4_ANSWER = """Q1: A product with zero stock showing a disabled "Out of Stock" button is correct.
Q2: There is no decision on this yet. Record it as an open question for the product owner, with what you saw, and go on.
Q3: The higher quantity wins (this is what the application's AUTH.md says).
Q4: Stock is never exceeded, a failed add changes nothing, and no add touches another owner's cart - these hold. On a repeated add keeping one line there is no decision yet: record it as an open question for the product owner, with what you saw, and go on.
Q5: R-11 and R-12 hold as norms (a failed add leaves the cart unchanged; an add never touches another owner's cart). R-8: a quantity of 0, -1, 1.5 or "abc" on the book page must be refused with a clear message, and nothing is added. R-10: there is no decision on this yet; record it as an open question for the product owner, with what you saw, and go on.
Q6: There is no decision on this yet. Record it as an open question for the product owner, with what you saw, and go on.
Q7: There is no decision on this yet. Record it as an open question for the product owner, with what you saw, and go on.
Q8: A quantity of 0, -1, 1.5 or "abc" on the book page must be refused with a clear message, and nothing is added.
Q9: Yes: a failed add leaves the cart unchanged.
Q10: A product with zero stock showing a disabled "Out of Stock" button is correct.
Q11: There is no decision on this yet. Record it as an open question for the product owner, with what you saw, and go on.
Q12: The higher quantity wins (this is what the application's AUTH.md says).
Q13: Yes: two guests, and a guest and a user, have fully separate carts.
Q14: Yes: an add by one owner leaves other owners' carts unchanged.
Q15: Yes: a signed-in user's cart holds only that user's own adds.
Q16: There is no decision on this yet. Record it as an open question for the product owner, with what you saw, and go on.
Q17: A quantity of 0, -1, 1.5 or "abc" on the book page must be refused with a clear message, and nothing is added.
Q18: Yes: a second guest sees an empty cart, apart from the first guest and the user.
"""
FV13_HALTING = f"{ROLE_OF['S2']} S2 {Q_TASK} · halt\nR-1 · unresolved · the ticket says two opposite things\n"


def fv13_open(mode: str = "stop", ids: int = 7, stage: str = "S2", opened: bool = True):
    """A seeded story with `ids` open questions and the stop (`stop`) or the role's own halt (`halt`) asked. Returns (root, task_root, s)."""
    root, task_root, env = seed(Q_TASK)
    q_register(task_root, [f"Q{i}" for i in range(1, ids + 1)])
    s = QStub(root, env, stage=stage, digest=FV13_HALTING if mode == "halt" else None)
    if opened:
        s.driver.ask(s.run_role())
    return root, task_root, s


def fv13_answer(s, root: Path, words: str):
    """The answer taken as `take_answer` takes it; returns (what the driver printed, the exception it raised or None)."""
    import contextlib
    import io
    path = root / "answer.md"
    path.write_bytes(words.encode("utf-8"))
    out, raised = io.StringIO(), None
    with contextlib.redirect_stdout(out):
        try:
            s.driver.take_answer(path)
        except Exception as exc:  # noqa: BLE001 - the raised Person / Stop is the subject
            raised = exc
    return out.getvalue(), raised


def fv13_watch(s, task_root: Path, then=None) -> list:
    """Wrap the conductor stub: per call the text, the words FILE as it was on disk, the register as the conductor saw it."""
    seen, base = [], s.driver.conductor

    def conductor(*a, **k):
        named = k.get("words_file")
        seen.append({"text": a[0], "file": (task_root / named).read_bytes() if named else b"", "register": q_load(task_root)})
        if then:
            then()
        return base(*a, **k)
    s.driver.conductor = conductor
    return seen


def fv1_3_free_answer_at_a_question_stop() -> None:
    """FV1-3, one table: what code records, what the conductor is called for, and what it is told - per answer shape. Rows already pinned
    elsewhere (the token grammar, `Q1: a or b`, two lines for one id) are not repeated."""
    import story_run
    import driver_conductor
    cyr = "".join(chr(c) for c in (0x0432, 0x044B, 0x0448, 0x0435))                       # a word in another script
    unreadable = lambda ctx: (ctx.task_root / "work" / "requirements-readiness.json").write_text("{not json", encoding="utf-8")  # noqa: E731

    def settle_q1(ctx):                                    # Q1 settled AFTER the person saw it: a different token on it is refused (H6)
        shown = ctx.s.driver.state["question_stop"]["shown"]["Q1"]
        code, out = ctx.s.driver.py("question_register.py", "--task", Q_TASK, "--answer", "Q1", "--reading", "a", "--words", "earlier",
                                    "--where", "S2 stop", "--by", "person", "--register-hash", shown)
        eq("settled-other-answer: the earlier record is written", code, 0, out)

    def seam_raises(ctx):
        def spent(*a, **k):
            raise driver_conductor.ConductorSpent(3, "x")
        ctx.s.driver.conductor = spent
        ctx.s.driver.apply_question_answers = lambda stage: {"opened": False, "plan_lines": ["a plan line"]}

    def seam_raises_after(ctx, out, raised):
        check("seam-raises: the seam's fallback Person comes out of take_answer", isinstance(raised, story_run.Person))
        disk = json.loads((ctx.task_root / "state/driver-state.json").read_text(encoding="utf-8"))
        check_eq("seam-raises: the words are filed and saved BEFORE the seam", disk["pending_words"].get(ctx.s.dispatch), ctx.words)
        check_eq("seam-raises: code's own plan lines are saved BEFORE the seam", disk["question_pass_lines"].get(ctx.s.dispatch),
                 ["a plan line"])
        check_eq("seam-raises: ONE human_answer row", sum(1 for sc, a in ctx.s.py_calls if sc == "log_append.py" and "human_answer" in a), 1)
        log = ctx.s.driver.state_dir / "driver-answers.jsonl"
        rows = [json.loads(ln) for ln in (log.read_text(encoding="utf-8").splitlines() if log.exists() else []) if ln.strip()]
        check_eq("seam-raises: ONE audit row for this answer, on disk before the seam (FR-7)", [(r["dispatch"], r["words"]) for r in rows],
                 [(ctx.s.dispatch, ctx.words)])

    def new_id_after(ctx, out, raised):
        check_in("new-id-in-register: the print-back says nothing was recorded", "recorded nothing", out)
        check("new-id-in-register: and names no Q8 (it was never answered)", "Q8" not in out, out)

    def printback_unreadable_after(ctx, out, raised):
        check_in("printback-unreadable: a register that cannot be read back says so", "could not be read back", out)
        check("printback-unreadable: and never says nothing was recorded", "recorded nothing" not in out)

    def go_on_after(ctx, out, raised):
        check("go-on-not-whole: no pass is written for words that are not the whole `go on`",
              not any(sc == "waiver.py" for sc, a in ctx.s.py_calls))

    def free_after(ctx, out, raised):
        text = ctx.seen[0]["text"]
        check_in(f"{ctx.row}: the text says code recorded nothing", "recorded by code: nothing", text)
        check_in(f"{ctx.row}: and names the stop", '--where "S2 stop"', text)
        check_in(f"{ctx.row}: and who records", "--by conductor", text)

    def mixed_after(ctx, out, raised):
        check_eq("mixed: Q1 was recorded by CODE before the conductor was called (the conductor saw it answered)",
                 ctx.seen[0]["register"]["Q1"]["status"], "answered")
        check_in("mixed: and the conductor is told it is recorded", "recorded by code: Q1: b", ctx.seen[0]["text"])

    def settled_after(ctx, out, raised):
        got = q_load(ctx.task_root)["Q1"]
        check_eq("settled-other-answer: the settled record is not overwritten by code", (got["status"], got["reading"]), ("answered", "a"))
        check_in("settled-other-answer: the refused line is listed with its reason", "Not recorded by code (each line says why)",
                 ctx.seen[0]["text"])
        check("settled-other-answer: and is never called `Not read, still open` (the old label)",
              "Not read, still open" not in ctx.seen[0]["text"])

    def unreadable_after(ctx, out, raised):
        check_in("register-unreadable: the conductor is told nothing was recorded by code", "recorded by code: nothing", ctx.seen[0]["text"])

    def lang_after(ctx, out, raised):
        check_eq("another-language: the words FILE is the answer, byte for byte", ctx.seen[0]["file"], ctx.words.encode("utf-8"))

    def limit_after(ctx, out, raised):
        check_eq(f"{ctx.row}: the words FILE is whole", (len(ctx.seen[0]["file"]), ctx.seen[0]["file"]),
                 (len(ctx.words.encode("utf-8")), ctx.words.encode("utf-8")))

    # id, words, mode, conductor calls, records by code (None: not read), raises, setup (before the answer), in-conductor hook, after
    rows = [
        ("empty-whitespace", "  \n\t \n", "stop", 0, {}, story_run.Stop, None, None, None),
        ("no-question-open", "Q1: a", "closed", 0, {}, story_run.Stop, None, None, None),
        ("all-tokens", "Q1: a\nQ2: not needed", "stop", 0, {"Q1": "answered", "Q2": "not_needed"}, None, None, None, None),
        ("token-word-inside-free-text", "Q1: a because the ticket says so", "stop", 1, {}, None, None, None, free_after),
        ("mixed", "Q1: b\nQ3 go with the ticket", "stop", 1, {"Q1": "answered"}, None, None, None, mixed_after),
        ("another-language", "Q3: " + cyr + "\nQ1: " + chr(0x0430), "stop", 1, {}, None, None, None, lang_after),
        ("words-at-6000", "Q3 " + "w" * 5997, "stop", 1, {}, None, None, None, limit_after),
        ("words-beyond-6001", "Q3 " + "w" * 5998, "stop", 1, {}, None, None, None, limit_after),
        ("settled-other-answer", "Q1: b", "stop", 1, {"Q1": "answered"}, None, settle_q1, None, settled_after),
        ("go-on-not-whole", "go on, but Q3 is the ticket's", "stop", 1, {}, None, None, None, go_on_after),
        ("register-unreadable", "Q1: a", "stop", 1, None, None, unreadable, None, unreadable_after),
        ("printback-unreadable", "Q3 go with the ticket", "stop", 1, None, None, None, unreadable, printback_unreadable_after),
        ("seam-raises", "Q1: a\nQ3 go with the ticket", "stop", 0, {"Q1": "answered"}, story_run.Person, seam_raises, None, seam_raises_after),
        ("new-id-in-register", "Q3 go with the ticket", "stop", 1, {}, None, None,
         lambda ctx: q_register(ctx.task_root, [f"Q{i}" for i in range(1, 9)]), new_id_after),
    ]
    from types import SimpleNamespace
    for row, words, mode, calls, records, raises, setup, in_conductor, after in rows:
        root, task_root, s = fv13_open("stop" if mode == "closed" else mode, opened=mode != "closed")
        try:
            ctx = SimpleNamespace(row=row, s=s, task_root=task_root, words=words, seen=[])
            if setup:
                setup(ctx)
            ctx.seen = fv13_watch(s, task_root, (lambda: in_conductor(ctx)) if in_conductor else None)
            out, raised = fv13_answer(s, root, words)
            check_eq(f"{row}: what the answer raised", type(raised) if raised else None, raises)
            if row != "seam-raises":
                check_eq(f"{row}: the conductor was called {calls} time(s)", len(ctx.seen), calls)
            if records is not None:
                got = {k: v["status"] for k, v in q_load(task_root).items() if v["status"] != "open"}
                check_eq(f"{row}: what code recorded", got, records)
            if after:
                after(ctx, out, raised)
        finally:
            harness.cleanup(root)

    # no-judge-on-register: on both register roads the judge stays uncalled (F-9), the conductor is called once
    for mode in ("stop", "halt"):
        root, task_root, s = fv13_open(mode)
        try:
            judged = []
            s.driver.judged_reply = lambda *a, **k: judged.append(a) or ""
            seen = fv13_watch(s, task_root)
            out, raised = fv13_answer(s, root, "Q1: a\nand please go with the ticket on the rest")
            check_eq(f"no-judge-on-register ({mode}): the judge was not called", judged, [])
            check_eq(f"no-judge-on-register ({mode}): the conductor was called once", len(seen), 1)
            check("no-judge-on-register (%s): and no judge section is in its text" % mode, "judge reads" not in seen[0]["text"])
        finally:
            harness.cleanup(root)

    # halt-road-shares-member: both roads hand over through the ONE member
    for mode, kind in (("stop", "questions"), ("halt", "halt")):
        root, task_root, s = fv13_open(mode)
        try:
            handed = []
            s.driver.register_words_to_conductor = lambda *a, **k: handed.append(a) or []
            seen = fv13_watch(s, task_root)
            fv13_answer(s, root, "Q1: a\nand please go with the ticket on the rest")
            check_eq(f"halt-road-shares-member ({mode}): the member is called once, with kind {kind}", [h[0] for h in handed], [kind])
            check_eq(f"halt-road-shares-member ({mode}): and the conductor only through it", len(seen), 0)
        finally:
            harness.cleanup(root)

    # rerun-other-dispatch: words filed, but the open question is about ANOTHER dispatch -> today's branch, the role resumes
    root, task_root, s = fv13_open()
    try:
        d = s.driver
        d.state["asked"]["dispatch"] = "S3-qa-test-strategist-1"
        d.state["pending_words"][s.dispatch] = "Q1: a"
        q_register(task_root, ["Q1", "Q2"])                  # under the limit: the resumed role is not stopped by the threshold again
        s.claude_calls.clear()
        d.dispatch_action({"action": "wait_existing_job", "dispatch_id": s.dispatch})
        check_eq("rerun-other-dispatch: the role resumes as today", [(c["kind"], c["resume"]) for c in s.claude_calls], [("role", "sess-1")])
    finally:
        harness.cleanup(root)


def fv1_3_the_real_s4_answer() -> None:
    """K2, the finding's own test: the 18 lines of the live run's answer at an S4 stop. Before FV1-3 the conductor was never called and Q3
    stayed open; now the conductor (a stub that runs the register's own command) records Q3 and the person is told so."""
    root, task_root, env = seed(Q_TASK)
    try:
        q_register(task_root, [f"Q{i}" for i in range(1, 19)])
        s = QStub(root, env, stage="S4")
        d = s.driver
        d.ask(s.run_role())
        order = []
        real_apply = d.apply_question_answers
        d.apply_question_answers = lambda stage: order.append("apply") or real_apply(stage)
        base = d.conductor

        def conductor(*a, **k):
            order.append("conductor")
            code, out = d.py("question_register.py", "--task", Q_TASK, "--answer", "Q3", "--reading", "a", "--words-file",
                             str(task_root / d.answer_file()), "--where", "S4 stop", "--by", "conductor",
                             "--register-hash", d.state["question_stop"]["shown"]["Q3"])
            eq("the conductor's own command records", code, 0, out)
            return base(*a, **k)
        d.conductor = conductor
        out, raised = fv13_answer(s, root, FV13_S4_ANSWER)
        check_eq("real s4: nothing is raised", raised, None)
        check_eq("real s4: the conductor was called once", len(s.conductor_calls), 1)
        got = q_load(task_root)["Q3"]
        check_eq("real s4: Q3 is answered with reading a, by the conductor", (got["status"], got["reading"]), ("answered", "a"))
        check_eq("real s4: its words are the answer file's text", got["words"], (task_root / d.answer_file()).read_text(encoding="utf-8"))
        check_eq("real s4: the record keeps the hash the person was SHOWN", got["record_row_hash"], d.state["question_stop"]["shown"]["Q3"])
        check_eq("real s4: the plan is applied by code before the conductor and again after it", order, ["apply", "conductor", "apply"])
        check_in("real s4: the person is told what the assistant recorded", "recorded by the assistant from your own words — Q3: a", out)
        text = s.conductor_calls[0][0]
        check_in("real s4: the conductor is told where the shown hashes are", "question_stop.shown", text)
        check_in("real s4: and how to read the questions whole", "--show", text)
        check("real s4: and no judge reading is put in front of it", "judge reads" not in text)
    finally:
        harness.cleanup(root)


def fv1_3_rerun_with_no_answer() -> None:
    """K4 (B2): a seam question raised over filed words is asked again by a rerun with no `--answer`, with its own tokens, before the role is
    resumed; answering it resumes the role with the ORIGINAL words."""
    import story_run
    root, task_root, s = fv13_open()
    try:
        d = s.driver
        words = "Q1: a\nand please keep the admin cases apart"
        seam = story_run.Person("questions", "The assistant could not settle this; try again or stop?", "S2", s.dispatch)
        seam.offered = ("retry", "stop")
        seam.options = [{"token": "retry", "move": "person_does"}, {"token": "stop", "move": "stop_here"}]

        def unread(*a, **k):
            raise seam
        d.unread = unread
        out, raised = fv13_answer(s, root, words)
        check("rerun: the seam's question comes out of the answer", raised is seam)
        d.ask(raised)
        s.claude_calls.clear()
        try:
            d.dispatch_action({"action": "wait_existing_job", "dispatch_id": s.dispatch})
            again = None
        except story_run.Person as exc:
            again = exc
        check("rerun: a rerun with no answer asks again", again is not None and again.kind == "questions")
        if again is not None:
            check_eq("rerun: with the seam's own tokens", tuple(again.offered), ("retry", "stop"))
            check_in("rerun: and the seam's question", "try again or stop", again.text)
        check_eq("rerun: no role was resumed over the open question", [c for c in s.claude_calls if c["kind"] == "role"], [])
        check_eq("rerun: the words are still filed", d.state["pending_words"].get(s.dispatch), words)
        del d.unread                                        # the real seam again
        s.answer(root, "retry")
        s.claude_calls.clear()
        d.dispatch_action({"action": "wait_existing_job", "dispatch_id": s.dispatch})
        check_eq("rerun: after the answer the role resumes in its own session", [(c["kind"], c["resume"]) for c in s.claude_calls],
                 [("role", "sess-1")])
        check_in("rerun: with the ORIGINAL words in its prompt", "and please keep the admin cases apart", s.claude_calls[0]["prompt"])
    finally:
        harness.cleanup(root)


def fv1_3_the_real_pack_size() -> None:
    """E8: a real S4 pack is over 13 000 characters. Neither cut (the question at 6000 in the member, the refusal text at 6000 in
    `conductor()`) may take an instruction: both the recorded-by-code line and the `--show` pointer stand before character 6000."""
    root, task_root, env = seed(Q_TASK)
    try:
        rows = [{"id": f"Q{i}", "question": f"what should happen for Q{i}? " + ("the ticket and the code disagree about this case. " * 14),
                 "severity": "major",
                 "readings": [{"reading": "the first reading " + "x" * 40, "from": "the ticket", "if_chosen": "x"},
                              {"reading": "the second reading " + "y" * 40, "from": "the code", "if_chosen": "y"}]} for i in range(1, 19)]
        (task_root / "work").mkdir(parents=True, exist_ok=True)
        (task_root / "work" / "requirements-readiness.json").write_text(
            json.dumps({"verdict": "blocked", "register": {"total": 24}, "open_questions": rows}), encoding="utf-8")
        s = QStub(root, env, stage="S4")
        s.driver.ask(s.run_role())
        size = len((task_root / "state/driver-question.md").read_text(encoding="utf-8"))
        check("pack size: the question file is at least 13300 characters", size >= 13300, str(size))
        fv13_answer(s, root, FV13_S4_ANSWER)
        check_eq("pack size: the conductor was called once", len(s.conductor_calls), 1)
        text = s.conductor_calls[0][0]
        check("pack size: `recorded by code:` stands before the cut", 0 <= text.find("recorded by code:") < 6000)
        check("pack size: `--show` stands before the cut", 0 <= text.find("--show") < 6000)
    finally:
        harness.cleanup(root)


def main() -> None:
    run_scenarios([], [
        question_stop_road,
        question_stop_share_and_limits,
        question_stop_edges,
        question_stop_fallbacks,
        question_stop_loop_moves,
        fv1_3_free_answer_at_a_question_stop,
        fv1_3_the_real_s4_answer,
        fv1_3_rerun_with_no_answer,
        fv1_3_the_real_pack_size,
    ])
    harness.finish("test_story_run_loop_b_threshold")


# split: runner piece 1
if __name__ == "__main__":
    main()
