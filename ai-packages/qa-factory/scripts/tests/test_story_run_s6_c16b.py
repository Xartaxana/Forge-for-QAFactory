"""c16b: a part of test_story_run_s6.py, split by tools/test_split.py (TD-11c). The shared helpers are in story_run_s6_common."""
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness  # noqa: E402
import story_run_common  # noqa: E402
del story_run_common  # split: imported for its sys.path effect
from story_run_common import run_scenarios, check, check_eq, check_in, check_not_in, d2_answer, d2_pipeline, d2_seed, driver_for, eq, human_broken, s0_pipeline, s0_state
import no_move as NM  # noqa: E402
from story_run_s6_common import (  # noqa: E402
    SCREENS, WITH_HTTP, manual_rig, owed_words, t292_config, t292_enter,
)


def t329_b270_g_the_manual_block_size_has_one_source() -> None:
    """t-329 (B-270 g): the driver's window size is the controller's own `MANUAL_WINDOW_CASES`, imported - not a second
    literal that a change on one side would leave behind. The class attribute stays settable per instance (tests do)."""
    import re
    import controller
    import story_run
    eq("T329-g the driver's size is the controller's window constant", story_run.Driver.MANUAL_BLOCK_MAX, controller.MANUAL_WINDOW_CASES)
    source = harness.driver_text()
    check("T329-g and the source holds no literal for it", not re.search(r"(?m)^\s*MANUAL_BLOCK_MAX\s*=\s*\d", source))
    check("T329-g it is read from the controller", "MANUAL_BLOCK_MAX = MANUAL_WINDOW_CASES" in source
          and "from controller import MANUAL_WINDOW_CASES" in source)
    task = "QA-9"
    root, task_root, env = d2_seed(task, environment="Local", pending=False)
    try:
        driver = driver_for(root, env, task)
        driver.MANUAL_BLOCK_MAX = 2
        eq("T329-g control: an instance still overrides it (the size is read where the blocks are cut)",
           driver.MANUAL_BLOCK_MAX, 2)
        eq("T329-g control: the class is unchanged by that", story_run.Driver.MANUAL_BLOCK_MAX, controller.MANUAL_WINDOW_CASES)
    finally:
        harness.cleanup(root)


# ---------------------------------------------------------------------------------------------- C1-6b (t-1212)
# S6 as seam questions (spec t-699 section 3.2-3.3, A5-A7). Every question below carries its three price lines per option, its tokens
# unchanged, and an executor in code for each: `retry` / `go on` are the seam's own (`take_seam_answer`), `by hand` is the same pass plus
# a TYPED record (`refused.by`), `reapprove` is the controller's `semantic_reopen`.
PRICE_LABELS = ("the factory:", "you:", "the story:")


def c16b_price_lines(text: str, options: int) -> bool:
    """Every option has its three labelled lines: each label opens one line per option."""
    return all(sum(1 for line in text.splitlines() if line.startswith(label)) == options for label in PRICE_LABELS)


def c16b_refused_by(task_root, cases) -> list:
    """`refused.by` of the request.json of each case ('' when the key is absent)."""
    return [json.loads((task_root / "work" / "evidence" / "manual" / case / "request.json").read_text(encoding="utf-8"))["refused"].get("by", "")
            for case in cases]


def c16b_stand_login_is_priced_and_its_two_passes_are_two_records() -> None:
    """(§3.2, A5, A6, A7) `s6.stand_login`: three options x three price lines, tokens unchanged; the question carries `offered` and the
    block (a seam question). `by hand` -> `refused.by: person_checks`; `go on` -> `left_unchecked`; a pass recorded for other words (the
    conductor's road) -> `left_unchecked` too, even after a `by hand` (the typed record is bound to ITS pass). The `by hand` line does not
    promise `yes`: it states the verdict measured today (`no`). MUTATION `one executor again`: both tokens -> the same `by`."""
    task = "QA-9"
    root, task_root, env = d2_seed(task, environment="Local", pending=False)
    try:
        t292_config(root)
        cases, screens = list(WITH_HTTP), list(SCREENS)
        driver, world, launched, moves = manual_rig(root, env, task, cases, policy=WITH_HTTP)
        _text, _new, person = t292_enter(driver, world, cases)
        eq("C16b stand_login: the tokens are unchanged, in order", list(person.priced), ["retry", "by hand", "go on"])
        check("C16b stand_login: 3 options x 3 price lines", c16b_price_lines(person.text, 3), person.text[-900:])
        eq("C16b stand_login: it is a seam question - `offered`, the moves, the block code knows",
           (person.offered, [o["move"] for o in person.options], person.block),
           (("retry", "by hand", "go on"), ["person_does", "go_on_as_is", "go_on_as_is"], driver.STAND_LOGIN_BLOCK))
        eq("C16b stand_login: and it obeys human-questions.md", human_broken(person.text), [])
        by_hand_line = next(line for line in person.text.splitlines() if line.startswith("the story:") and "left with you" in line)
        check_not_in("C16b stand_login (P21): `by hand` never promises a ready verdict", "will read: ready", by_hand_line)
        check_in("C16b stand_login (C5-4, P21): ...it states the third outcome, conditional, not `no` (the requirement has its \"Left with you\" line)",
                 "ready after your checks only if nothing else holds it", by_hand_line)
        check_not_in("C16b stand_login (C5-4): ...and no longer says the delivery reads `no`", "not ready to ship as is", by_hand_line)
        check_in("C16b stand_login: the person line of `by hand` is the checks left with them", "checks left with you before release", person.text)
        # B-F1 (t-1228, FR-10/FR-41): `go on` leaves the same cases unchecked and the verdict reads the same measured word: the packet
        # never suggests `go on` is the gentler choice for the delivery
        story_lines = [line for line in person.text.splitlines() if line.startswith("the story:")]
        eq("C16b stand_login (B-F1): one `the story:` line per option", len(story_lines), 3)
        check_in("C16b stand_login (B-F1): the `go on` line states the verdict measured today, as `by hand` does", "not ready to ship as is", story_lines[2])
        eq("C16b stand_login (C5-4): `by hand` holds `not_known` (the cases are the person's line), `go on` holds `no` (nothing is left with them)",
           [row["delivery"] for row in NM.load_question_prices()["s6.stand_login"][1:]], ["not_known", "no"])
        check_eq("C16b stand_login: every token has a data row (the loader reads them)",
                 [row["answer"] for row in NM.load_question_prices()["s6.stand_login"]], list(person.priced))
        for token, words in (("by hand", "By hand."), ("go on", "go on")):
            fresh_root, fresh_task_root, fresh_env = d2_seed(task, environment="Local", pending=False)
            try:
                t292_config(fresh_root)
                driver, world, launched, moves = manual_rig(fresh_root, fresh_env, task, cases, policy=WITH_HTTP)
                _text, _new, person = t292_enter(driver, world, cases)
                driver.ask(person)
                eq(f"C16b `{token}`: `ask()` keeps the seam's fields (offered, block)",
                   ((s0_state(fresh_task_root).get("asked") or {}).get("offered"), (s0_state(fresh_task_root).get("asked") or {}).get("block")),
                   (["retry", "by hand", "go on"], "stand login missing"))
                driver.take_answer(Path(d2_answer(fresh_root, words)))
                got = [o for o in (s0_pipeline(fresh_task_root).get("stage_overrides") or []) if o.get("match") == "stand login missing"]
                eq(f"C16b `{token}`: the pass is `waiver.py --words-file`: the words whole", [(o["stage"], o["decision"]) for o in got], [("S6", words)])
                t292_enter(driver, world, cases)
                eq(f"C16b `{token}`: the typed record in each screen case's request.json",
                   c16b_refused_by(fresh_task_root, screens), ["person_checks" if token == "by hand" else "left_unchecked"] * 2)
            finally:
                harness.cleanup(fresh_root)
        # a pass the conductor recorded from free words: no typed record of ours -> `left_unchecked`; and a stale `by hand` record
        # (the pass was replaced by other words) is not read for the new pass
        fresh_root, fresh_task_root, fresh_env = d2_seed(task, environment="Local", pending=False)
        try:
            t292_config(fresh_root)
            d2_pipeline(fresh_task_root, stage_overrides=[{"stage": "S6", "match": "stand login missing", "decision": "ask Dana, she has it",
                                                            "at": "2026-10-02T10:00:00+00:00", "by": "human"}])
            driver, world, launched, moves = manual_rig(fresh_root, fresh_env, task, cases, policy=WITH_HTTP)
            driver.state["login_choice"] = {"token": "by hand", "words": "by hand"}
            t292_enter(driver, world, cases)
            eq("C16b the conductor's pass (free words) and a stale `by hand` record: `left_unchecked`",
               c16b_refused_by(fresh_task_root, screens), ["left_unchecked"] * 2)
        finally:
            harness.cleanup(fresh_root)
        # free words: the conductor, with the words by FILE, no inline `--decision`
        calls = []
        driver, world, launched, moves = manual_rig(root, env, task, cases, policy=WITH_HTTP)
        _text, _new, person = t292_enter(driver, world, cases)
        driver.ask(person)
        driver.conductor = lambda prompt, words=None, **kw: calls.append((prompt, words)) or {"action": "continue", "did": "read"}
        driver.take_answer(Path(d2_answer(root, "I will think about it")))
        check_in("C16b free words: the conductor is told to record them by file", '--block "stand login missing" --words-file ', calls[0][0])
        check_not_in("C16b free words: no inline `--decision` (axis 5)", "--decision", calls[0][0])
        check("C16b free words: and no typed record is made", "login_choice" not in driver.state)
    finally:
        harness.cleanup(root)


def c16b_stand_confirm_is_priced_and_its_answers_have_executors() -> None:
    """(§3.2) `s6.stand_confirm`: the text is the question plus the priced section (3 options x 3 lines when a stand is named and another
    exists); `retry` / `go on` are the seam's executors (the pass is `waiver.py --words-file`, block `stand not confirmed`); the stand's
    NAME is the site's door; free words go to the conductor with the words by FILE (the S5 class of the inline `--decision`).
    MUTATION `price section dropped`: the count of price lines is 0."""
    import contextlib
    import io
    import story_run
    task = "QA-9"
    root, task_root, env = d2_seed(task, environment="Local", pending=True)
    try:
        driver = driver_for(root, env, task)
        text = driver.stand_question_text("S6", "Local", ["Local", "Staging"], "manual")
        check("C16b stand_confirm: 3 options x 3 price lines", c16b_price_lines(text, 3), text[-700:])
        eq("C16b stand_confirm: the priced tokens", list(text.priced), ["retry", "go on"])
        eq("C16b stand_confirm: it obeys human-questions.md", human_broken(text), [])
        eq("C16b stand_confirm: the answers of the data row = the options of the site (named, another stand)",
           [row["answer"] for row in NM.load_question_prices()["s6.stand_confirm"]], ["stand name", "retry", "go on"])
        eq("C16b stand_confirm: no stand recorded: retry + go on, the answers are a subset of the row",
           list(driver.stand_question_text("S5", "", []).priced), ["retry", "go on"])
        real = driver.py
        driver.py = lambda script, *a, **k: (1, "ENVIRONMENT: down") if script == "env_probe.py" else real(script, *a, **k)
        try:
            driver.stand_check("S6", "manual")
            person = None
        except story_run.Person as raised:
            person = raised
        check("C16b stand_confirm: stand_check raises a Person", person is not None)
        eq("C16b stand_confirm: a seam question - kind `environment`, `offered`, the block",
           (person.kind, person.offered, person.block, person.stand_stage), ("environment", ("retry", "go on"), "stand not confirmed", "S6"))
        # FV3-21 K2: the `go on` option says what it does to the manual cases (T1-T7); every text obeys human-questions.md, the price lines unchanged
        clause, today = "an agent checks no case by hand", "go on without a stand, and the story carries a line saying it was your decision"
        n_of = lambda t: sum(1 for line in t.splitlines() if line.startswith(PRICE_LABELS[0]))
        t1 = driver.stand_question_text("S6", "Local", ["Local"], "manual", manual=True)
        t2 = driver.stand_question_text("S6", "Local", ["Local"], "manual", manual=False)
        t3 = driver.stand_question_text("S5", "", [], manual=True)
        check_in("K2 T1: S6 manual says it", "go on without a stand; " + clause + ", and the story", t1)
        check_in("K2 T2: manual=False is today's text", today, t2)
        eq("K2 T2: ...and equals the call without the keyword", str(t2), str(driver.stand_question_text("S6", "Local", ["Local"], "manual")))
        check_in("K2 T3: S5 keeps its own clause and adds this one", "none is run on a stand; " + clause + ", and the story", t3)
        eq("K2 T1-T3: human-questions.md, price lines", [human_broken(t) for t in (t1, t2, t3)] + [n_of(t) for t in (t1, t2, t3)],
           [[], [], [], 2, 2, 2])
        base_n = n_of(str(person.text))

        def asked(scope_fn):
            driver.stage_scope = scope_fn
            try:
                driver.stand_check("S6", "automation")
            except story_run.Person as raised:
                return str(raised.text)
            finally:
                del driver.stage_scope
            return ""

        def broken_scope(stage, kind=""):
            raise story_run.Refusal("the controller cannot say")
        for label, scope_fn, said in (("T4 a manual case", lambda s, k="": {"scope": ["TC-2"]}, True),
                                      ("T5 an empty manual scope", lambda s, k="": {"scope": []}, False),
                                      ("T6 a scope that cannot be read", broken_scope, True),
                                      ("T7 an answer with no `scope` key", lambda s, k="": {"stage": "S6"}, True)):
            text = asked(scope_fn)
            eq(f"K2 {label}: the clause is said = {said}; human-questions.md; price lines unchanged",
               (clause in text, human_broken(text), n_of(text)), (said, [], base_n))
        driver.ask(person)
        driver.take_answer(Path(d2_answer(root, "go on")))
        got = [(o["stage"], o["match"], o["decision"]) for o in (s0_pipeline(task_root).get("stage_overrides") or [])]
        eq("C16b stand_confirm: `go on` is the seam's pass: `waiver.py --words-file`, the words whole", got, [("S6", "stand not confirmed", "go on")])
        # the stand's name is the site's door; the next entry probes it
        d2_pipeline(task_root, stage_overrides=[])
        driver = driver_for(root, env, task)
        driver.py = lambda script, *a, **k: (1, "ENVIRONMENT: down") if script == "env_probe.py" else real(script, *a, **k)
        driver.config = dict(driver.config, environments=[{"name": "Local"}, {"name": "Staging"}])
        try:
            driver.stand_check("S6", "manual")
        except story_run.Person as raised:
            driver.ask(raised)
        driver.take_answer(Path(d2_answer(root, "Staging")))
        eq("C16b stand_confirm: the name sets the stand (pending until probed)",
           (s0_pipeline(task_root).get("environment"), s0_pipeline(task_root).get("environment_pending")), ("Staging", True))
        # C-F3 (t-1228): the journal row of the stand answer is `answer_row` - a refused write is OWED, the stand is still set (the words
        # reach the executor directly), and the drain writes the row once the journal answers
        d2_pipeline(task_root, stage_overrides=[])
        driver = driver_for(root, env, task)
        driver.config = dict(driver.config, environments=[{"name": "Local"}, {"name": "Staging"}])
        journal_ok = [False]

        def journal_down(script, *a, **k):
            if script == "env_probe.py":
                return 1, "ENVIRONMENT: down"
            if script == "log_append.py" and not journal_ok[0]:
                return 1, "journal busy"
            return real(script, *a, **k)
        driver.py = journal_down
        try:
            driver.stand_check("S6", "manual")
        except story_run.Person as raised:
            driver.ask(raised)
        with contextlib.redirect_stdout(io.StringIO()):
            driver.take_answer(Path(d2_answer(root, "Local")))
        eq("C16b stand_confirm (C-F3): the stand is set whatever the journal does",
           (s0_pipeline(task_root).get("environment"), s0_pipeline(task_root).get("environment_pending")), ("Local", True))
        eq("C16b stand_confirm (C-F3): ...and the refused `human_answer` row of the words is OWED",
           [(r["script"], "human_answer" in r["args"], "stand at S6: Local" in owed_words(r)) for r in driver.state.get("owed_rows") or []],
           [("log_append.py", True, True)])
        journal_ok[0] = True
        with contextlib.redirect_stdout(io.StringIO()):
            driver.owed_rows_step()
        eq("C16b stand_confirm (C-F3): ...and the drain writes it", driver.state.get("owed_rows") or [], [])
        # free words: the conductor, the words by FILE
        calls = []
        driver = driver_for(root, env, task)
        driver.py = lambda script, *a, **k: (1, "ENVIRONMENT: down") if script == "env_probe.py" else real(script, *a, **k)
        driver.state["asked"] = {"kind": "environment", "stage": "S6", "dispatch": ""}
        driver.state["stand_question"] = "S6"
        driver.save_state()
        (task_root / "state" / "driver-question.md").write_text("# q\nkind: environment\n", encoding="utf-8")
        driver.conductor = lambda prompt, words=None, **kw: calls.append((prompt, words)) or {"action": "continue", "did": "read"}
        with contextlib.redirect_stdout(io.StringIO()):
            driver.take_answer(Path(d2_answer(root, "use whatever works")))
        check_in("C16b stand_confirm free words: the command takes the words by file", '--block "stand not confirmed" --words-file ', calls[0][0])
        check_not_in("C16b stand_confirm free words: no inline `--decision` (axis 5)", "--decision", calls[0][0])
    finally:
        harness.cleanup(root)


def c16b_gate_a_dry_is_a_priced_question_with_three_executors() -> None:
    """(§3.3, edges 10, 6, 7) `s6.gate_a_dry`: a Person of kind `gate_a_dry` with `reapprove` / `go on` / `stop`, 3 lines each. `reapprove`
    -> the controller's `semantic_reopen` with the answer words as the reason and the MANUAL cases as the scope (the facts the
    controller is asked with: its revision); `go on` -> `waiver.py --stage S6 --block "gate A recorded dry" --words-file`, and the question
    is not asked again (the note line stays); `stop` -> held. `reapprove` is NOT offered while a dispatch runs, in a run that records
    gates dry (`--dry-run`), with no approved gate A, or with no case the approved scope holds - and a typed `reapprove` then goes to
    the conductor, never to the controller. MUTATION `the dry-gate Person removed`: the first check fails."""
    import contextlib
    import io
    from unittest import mock
    import story_run
    task = "QA-9"
    root, task_root, env = d2_seed(task, environment="Local", pending=False)
    try:
        plan = [{"id": "TS-1", "disposition": "manual-agent", "coverage_obligations": [{"obligation_id": "OB-1", "decision": "new"}]}]
        (task_root / "work" / "test-plan.json").write_text(json.dumps({"rows": plan}), encoding="utf-8")
        index = {"QA-9_TC_001": {"path": task_root / "work" / "test-cases" / "QA-9_TC_001.md", "plan_row": "TS-1"},
                 "QA-9_TC_002": {"path": task_root / "work" / "test-cases" / "QA-9_TC_002.md", "plan_row": "TS-2"}}

        def build(running=False, approved=True, dry=False, scope=("QA-9_TC_001", "QA-9_TC_002")):
            driver = driver_for(root, env, task)
            driver.dry = dry
            ctl = {"dispatches": {"S6-qa-runner-1": {"stage": "S6", "status": "running"}} if running else {},
                   "decisions": {"d1": {"gate": "A", "status": "approved", "source_revision": "r1"}} if approved else {},
                   "scope": list(scope), "source_revision": "r1", "revision": 7}
            driver.controller_state = lambda: ctl
            calls = []
            driver.controller = lambda op, *a, input_data=None, **k: calls.append((op, input_data)) or {}
            return driver, calls

        def raised_person(driver):
            out = io.StringIO()
            try:
                with mock.patch("contract.case_index", lambda _root: index), contextlib.redirect_stdout(out):
                    driver.manual_gate_note()
            except story_run.Person as person:
                return person, out.getvalue()
            return None, out.getvalue()

        driver, calls = build()
        person, said = raised_person(driver)
        check("C16b gate A dry: the manual rows with no executable obligation raise a Person", person is not None)
        eq("C16b gate A dry: kind `gate_a_dry`, at S6, the tokens, the moves, the block",
           (person.kind, person.stage, person.offered, [o["move"] for o in person.options], person.block),
           ("gate_a_dry", "S6", ("reapprove", "go on", "stop"), ["site_door", "go_on_as_is", "stop_here"], "gate A recorded dry"))
        check("C16b gate A dry: 3 options x 3 price lines", c16b_price_lines(person.text, 3), person.text[-900:])
        check_in("C16b gate A dry: `reapprove` states the stages it runs again (measured: the case review, not the designer)",
                 "the case review of S4, gate A and the manual half of S6 run again", person.text)
        check_in("C16b gate A dry: the case named is its id (the other plan row's case is not named)", "QA-9_TC_001", person.text)
        check_not_in("C16b gate A dry: and the case of another row is not", "QA-9_TC_002", person.text)
        eq("C16b gate A dry: it obeys human-questions.md", human_broken(person.text), [])
        eq("C16b gate A dry: every token has a data row, and the set is the site's",
           [row["answer"] for row in NM.load_question_prices()["s6.gate_a_dry"]], list(person.priced))
        check_not_in("C16b gate A dry: no command, no script in anything the person reads", "semantic_reopen", person.text + said)
        # reapprove -> semantic_reopen with the words, the manual cases, the controller's own revision
        driver.ask(person)
        driver.take_answer(Path(d2_answer(root, "reapprove")))
        eq("C16b gate A dry: `reapprove` calls semantic_reopen with the manual cases (and only the controller's op)",
           [(op, d["reason"], d["affected_scope"], d["expected_revision"]) for op, d in calls], [("semantic_reopen", "reapprove", ["QA-9_TC_001"], 7)])
        check("C16b gate A dry: ...with an idempotency key of its own", calls[0][1]["idempotency_key"].startswith("semantic_reopen:gate_a_dry:"))
        eq("C16b gate A dry: ...and no waiver was written", s0_pipeline(task_root).get("stage_overrides") or [], [])
        # C-F3 (t-1228): the journal row of the words is `answer_row` - a refused write is OWED (the drain writes it again, the seam asks
        # after a second failure) and the reopening still runs: the words reach the executor directly (E8 of t-1152)
        driver, calls = build()
        person, _said = raised_person(driver)
        driver.ask(person)
        base_py = driver.py
        driver.py = lambda script, *a, **k: (1, "journal busy") if script == "log_append.py" else base_py(script, *a, **k)
        with contextlib.redirect_stdout(io.StringIO()):
            driver.take_answer(Path(d2_answer(root, "reapprove")))
        eq("C16b gate A dry (C-F3): a refused journal row is owed, as a `human_answer` row of those words",
           [(r["script"], "human_answer" in r["args"], "gate A recorded dry (reapprove): " in owed_words(r)) for r in driver.state.get("owed_rows") or []],
           [("log_append.py", True, True)])
        eq("C16b gate A dry (C-F3): ...and the reopening still ran with the words", [op for op, _data in calls], ["semantic_reopen"])
        driver.py = base_py
        with contextlib.redirect_stdout(io.StringIO()):
            driver.owed_rows_step()
        eq("C16b gate A dry (C-F3): ...and the drain writes it", driver.state.get("owed_rows") or [], [])
        # the controller refuses: said, nothing changed, the question comes back
        driver, calls = build()
        person, _said = raised_person(driver)
        driver.ask(person)
        driver.controller = lambda op, *a, input_data=None, **k: (_ for _ in ()).throw(story_run.Refusal("checkpoint active work before reopening Gate A"))
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                driver.take_answer(Path(d2_answer(root, "reapprove")))
            held = None
        except story_run.Person as raised:
            held = raised
        check("C16b gate A dry: a refusal of the controller comes back as the held question, with its words",
              held is not None and "could not be carried out" in held.text and "checkpoint active work" in (held.details or ""))
        # go on -> the waiver by file, asked once (the note line stays)
        driver, calls = build()
        person, _said = raised_person(driver)
        driver.ask(person)
        with contextlib.redirect_stdout(io.StringIO()):
            driver.take_answer(Path(d2_answer(root, "go on")))
        got = [(o["stage"], o["match"], o["decision"]) for o in (s0_pipeline(task_root).get("stage_overrides") or [])]
        eq("C16b gate A dry: `go on` is `waiver.py --stage S6 --block` with the words by file", got, [("S6", "gate A recorded dry", "go on")])
        again, said = raised_person(build()[0])
        eq("C16b gate A dry: a passed question is not asked again - the line stays", (again, "gate A was recorded dry" in said), (None, True))
        d2_pipeline(task_root, stage_overrides=[])
        # stop -> held
        driver, calls = build()
        person, _said = raised_person(driver)
        driver.ask(person)
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                driver.take_answer(Path(d2_answer(root, "stop")))
            held = None
        except story_run.Person as raised:
            held = raised
        check("C16b gate A dry: `stop` holds the question (nothing runs, nothing is recorded)",
              held is not None and held.text.startswith("You said to stop.") and calls == [] and not s0_pipeline(task_root).get("stage_overrides"))
        # edge 10: reapprove is not offered when its executor would not run
        for label, kwargs, why in (("a dispatch runs", {"running": True}, "a role is still working"),
                                   ("the run records gates dry", {"dry": True}, "this run records gates dry"),
                                   ("no approved gate A", {"approved": False}, "there is no approved gate A"),
                                   ("the approved scope holds none of the cases", {"scope": ()}, "could not name these cases")):
            driver, calls = build(**kwargs)
            person, _said = raised_person(driver)
            eq(f"C16b gate A dry edge 10 ({label}): `reapprove` is not offered; `go on` and `stop` are", person.offered, ("go on", "stop"))
            check_in(f"C16b gate A dry edge 10 ({label}): and ONE line says why", why, person.text)
            check_not_in(f"C16b gate A dry edge 10 ({label}): no `reapprove` option in the text", "`reapprove`", person.text)
            driver.ask(person)
            seen = []
            driver.conductor = lambda prompt, words=None, **kw: seen.append(words) or {"action": "continue", "did": "read"}
            with contextlib.redirect_stdout(io.StringIO()):
                driver.take_answer(Path(d2_answer(root, "reapprove")))
            eq(f"C16b gate A dry edge 10 ({label}): a typed `reapprove` goes to the conductor, never to the controller", (calls, seen), ([], ["reapprove"]))
    finally:
        harness.cleanup(root)


def c16b_fix_round_one_words_door_one_token_table() -> None:
    """(t-1228 B-F2, B-F3) The words door of the stand prompts is `person_words.door` (the file option has ONE text, the path of the
    answer file is its `path` argument); the tokens the seam owns are `NM.TOKEN_MOVES` and a site table adds only its own words.
    MUTATION `the second door text restored`: `_words_door` builds `--words-file` itself -> the first source check fails."""
    import inspect
    import person_words
    import story_run
    door_source = inspect.getsource(story_run.Driver._words_door)
    check("B-F2: `_words_door` renders through person_words.door", "person_words.door(" in door_source)
    check_not_in("B-F2: ...and holds no text of the file option of its own", "--words-file", door_source.split('"""')[2])
    command = 'python waiver.py --task T --stage S6 --block "stand login missing"'
    eq("B-F2: the door with the answer file is the plain door with that path in the place of the placeholder",
       person_words.door(command, path="work/answers/a.md"), command + " --words-file work/answers/a.md")
    eq("B-F2: no path - the placeholder as before (the form a role reads, and a person reads)",
       (person_words.door(command), person_words.door(command, for_person=True)),
       (command + " --words-file <file>", command + " --words-file <file with your words>"))
    eq("B-F3: the seam's own tokens are NM.TOKEN_MOVES, whole", {t: m for t, m in story_run.Driver.SITE_MOVES.items() if t in NM.TOKEN_MOVES}, NM.TOKEN_MOVES)
    eq("B-F3: ...and the site adds only its three words", sorted(set(story_run.Driver.SITE_MOVES) - set(NM.TOKEN_MOVES)), ["by hand", "find the way in", "reapprove"])
    table_lines = [part.split("\n", 1)[0] for part in harness.driver_text().split("SITE_MOVES = ")[1:]]      # every assignment of the table, in the whole driver set
    check("B-F3: the table is built from NM.TOKEN_MOVES, not copied", len(table_lines) >= 1 and all("{**NM.TOKEN_MOVES," in line for line in table_lines), str(table_lines))


def main() -> None:
    run_scenarios([], [
        t329_b270_g_the_manual_block_size_has_one_source,
        c16b_stand_login_is_priced_and_its_two_passes_are_two_records,
        c16b_stand_confirm_is_priced_and_its_answers_have_executors,
        c16b_gate_a_dry_is_a_priced_question_with_three_executors,
        c16b_fix_round_one_words_door_one_token_table,
    ])
    harness.finish("test_story_run_s6_c16b")


# split: runner piece 1
if __name__ == "__main__":
    main()
