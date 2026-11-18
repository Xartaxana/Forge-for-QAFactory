"""d1: a part of test_story_run_s6.py, split by tools/test_split.py (TD-11c). The shared helpers are in story_run_s6_common."""
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness  # noqa: E402
import story_run_common  # noqa: E402
del story_run_common  # split: imported for its sys.path effect
from story_run_common import run_scenarios, D1Evidence, D1_SAME, D2_DEAD, check, check_eq, check_in, check_not_in, d1_answer, d1_driver, d1_extras, d1_write_blocks, d2_enter, d2_seed, driver_for, eq, s0_question, seed
from story_run_s6_common import AWAITS, d1_blocks, pin_project, unpin_project  # noqa: E402


def s5_critic_finish_passes_window() -> None:
    """t-079 (FR-5/FR-48): the last window's critic closes S5 only over a window record; code builds it
    (window_record.py) and passes it to story_step finish. A failed build: finish runs without --window."""
    task = "QA-9"
    root, task_root, env = seed(task)
    try:
        for code in (0, 2):
            driver = driver_for(root, env, task)
            calls = []

            def py(script, *args, **kwargs):
                calls.append((script, [str(a) for a in args]))
                return (code, "record failed: no receipt") if script == "window_record.py" else (0, "accepted x")
            driver.py = py
            driver.finish("S5-qa-code-critic-5", "qa-code-critic S5 W1 ok", complete=True,
                          role="qa-code-critic", stage="S5")
            names = [c[0] for c in calls]
            check_eq(f"S5 critic finish (window_record exit {code}): window_record first, then finish",
                     names, ["window_record.py", "story_step.py"])
            check_eq(f"S5 critic finish (window_record exit {code}): window_record is asked for the dispatch",
                     calls[0][1], ["--task", task, "--dispatch", "S5-qa-code-critic-5"])
            has = "--window" in calls[1][1]
            check_eq(f"S5 critic finish (window_record exit {code}): --window passed only after a built record",
                     has, code == 0)
            if has:
                check_eq("the window path is the record window_record wrote",
                         calls[1][1][calls[1][1].index("--window") + 1], "work/windows/S5-qa-code-critic-5.json")
        driver = driver_for(root, env, task)
        calls = []
        driver.py = lambda script, *args, **kwargs: (calls.append(script) or (0, "accepted x"))
        driver.finish("S5-qa-automator-4", "d", complete=False, role="qa-automator", stage="S5")
        driver.finish("S5-qa-code-critic-4", "d", complete=False, role="qa-code-critic", stage="S5")
        check_eq("no window record for a finish that leaves the stage open", calls, ["story_step.py", "story_step.py"])
    finally:
        harness.cleanup(root)


def d1_s6_freshness() -> None:
    """D1: the automation branch of S6 asks the story's own record what stands, AFTER the stand question and
    BEFORE any runner. In-process, `run_role` recorded, no claude."""
    import story_run
    task = "QA-9"
    two = {"test_a": ("result", "passed", ""), "test_b": ("result", "failed", "")}
    root, task_root, env = d2_seed(task, environment="Local", pending=False)
    pin = pin_project(root)
    try:
        # (i) every result stands: nothing launched, no runner; the receipt, the reduction, the close
        d1_blocks(root, task_root)      # HF2-11b: the test file is on disk - a result of a file that is gone does not stand
        driver, launched, moves, started = d1_driver(root, env, task)
        with D1Evidence(d1_answer(two)) as evidence:
            driver.stage_S6()
        eq("D1(i) the story's record was asked once, for the automated cases, with the run_suite stand probe",
           (len(evidence.calls), evidence.calls[0][0]), (1, ["TC-1", "TC-2"]))
        import run_suite
        check("D1(i) and with the config and the stand probe the runner itself uses",
              evidence.calls[0][1].get("probe") is run_suite.probe_runtime and evidence.calls[0][1].get("cfg") == driver.config)
        eq("D1(i) NO runner is dispatched and nothing is started", (launched, started), ([], []))
        eq("D1(i) the moves are the reduction, the receipt, the close - in that order (the receipt only over a green reduction)",
           [m[0] for m in moves], ["finalize", "code_only", "stage_done"])
        eq("D1(i) the receipt names the stage and the evidence", (moves[1][1], moves[1][3]),
           ("S6", ["work/automation-manifest.json", "state/execution-jobs"]))
        check_in("D1(i) and says what stood, with the counts", "1 passed, 1 failed - reused, nothing re-run", moves[1][2])
        eq("D1(i) finalize_task runs on the task root", Path(moves[0][1]).resolve(), task_root.resolve())
        check_in("D1(i) the close is the S6 stage_done", "--stage S6 --status done", moves[2][1])
        report = json.loads((task_root / "work" / "run-report.json").read_text(encoding="utf-8"))
        eq("D1(i) run-report.json (a real finalize_task) holds the S5 rows of both runs",
           sorted(r["instance_id"] for r in report["current_results"]), ["test_a", "test_b"])
        eq("D1(i) a red result that stands is in the whole-story report as failed",
           (report["execution_status"], report["current_totals"]), ("failed", {"failed": 1, "passed": 1}))
        eq("D1(i) and S7 sees it to triage", driver.failures_to_triage(), "failed=1")

        # (i) but the reduction fails (a corrupt run block): no receipt, no close - the runner as today, with the note
        (task_root / "work" / "run-blocks" / "x.json").write_text("{not json", encoding="utf-8")
        driver, launched, moves, started = d1_driver(root, env, task)
        with D1Evidence(d1_answer(two)):
            driver.stage_S6()
        eq("D1(i) finalize exits non-zero: only the reduction was tried - no receipt, no close",
           [m[0] for m in moves], ["finalize"])
        eq("D1(i) finalize fails: the runner is dispatched as today, whole scope, closing S6",
           [(e["stage"], e["role"], e["scope"], e["complete"]) for e in launched], [("S6", "qa-runner", ["TC-1", "TC-2"], AWAITS)])         # X7-6c: the final window awaits the consumer, it does not close S6
        check_in("D1(i) finalize fails: with the note naming the exit",
                 "The factory could not decide freshness (finalize_task exit 1): decide per instance.", d1_extras(launched))
        (task_root / "work" / "run-blocks" / "x.json").unlink()

        # (ii) one instance is stale: the runner is dispatched, told what stands and what to run
        for label, states, line in (
                ("stale", {"test_a": two["test_a"], "test_b": ("stale", "", D1_SAME)},
                 f"Results that stand: test_a; run only: test_b ({D1_SAME})."),
                ("missing", {"test_a": two["test_a"], "test_b": ("missing", "", "no run of it is on record")},
                 "Results that stand: test_a; run only: test_b (no run of it is on record).")):
            driver, launched, moves, started = d1_driver(root, env, task)
            with D1Evidence(d1_answer(states)):
                driver.stage_S6()
            eq(f"D1(ii) {label}: one qa-runner dispatch, no receipt", ([(e["stage"], e["role"]) for e in launched], moves),
               ([("S6", "qa-runner")], []))
            check_in(f"D1(ii) {label}: the runner is told what stands and what to run", line, d1_extras(launched))
            # OPEN FORK (report): the dispatch keeps the whole automation scope. A dispatch scoped to the stale
            # cases only cannot close S6 - the controller completes S6 over its derived scope by ACCEPTED
            # dispatches (`_s6_completion_problems`) - so narrowing waits for Lead's decision.
            eq(f"D1(ii) {label}: the dispatch scope is the automation scope, and closes S6 (no manual half)",
               (launched[0]["scope"], launched[0]["complete"]), (["TC-1", "TC-2"], AWAITS))         # X7-6c: awaits the consumer
        driver, launched, moves, started = d1_driver(root, env, task)
        with D1Evidence(d1_answer({"test_a": ("stale", "", D1_SAME), "test_b": ("missing", "", "none")})):
            driver.stage_S6()
        check_not_in("D1(ii) nothing stands: no `Results that stand` line, the runner runs as today", "Results that stand", d1_extras(launched))
        check_in("D1(ii) and today's instruction is still the first line", "Execution kind: automation", d1_extras(launched))

        # (iii) the factory cannot decide: the runner as today, with the note (P1)
        long_text = "x" * 200
        for label, answer, why in (
                ("the evidence function raises", RuntimeError("boom"), "RuntimeError: boom"),
                ("a message AT the 200 limit is whole", ValueError(long_text), "ValueError: " + long_text),
                ("a message BEYOND it is cut", ValueError(long_text + "y"), "ValueError: " + long_text + story_run.Driver.CUT),
                ("the stand was not observed", d1_answer({"test_a": ("unknown", "", "the stand's version was not observed")}, observed=False),
                 "the stand's version was not observed"),
                ("no budget data (nothing decided, no instances)", {"instances": {}, "observed": False, "why": "run-budget.json cannot be read"},
                 "run-budget.json cannot be read"),
                ("an empty answer", d1_answer({}), "no test of these cases could be listed"),
                ("a state it does not know", d1_answer({"test_a": ("weird", "", "")}), "test_a: state `weird`"),
                ("a result whose outcome it cannot count", d1_answer({"test_a": ("result", "inconclusive", "")}), "test_a: state `result` with outcome `inconclusive`")):
            driver, launched, moves, started = d1_driver(root, env, task)
            with D1Evidence(answer):
                driver.stage_S6()
            eq(f"D1(iii) {label}: the runner is dispatched as today, no receipt", ([(e["stage"], e["role"]) for e in launched], moves),
               ([("S6", "qa-runner")], []))
            check_in(f"D1(iii) {label}: with the note and its reason", "The factory could not decide freshness (" + why, d1_extras(launched))
            check_in(f"D1(iii) {label}: and the instruction to decide per instance", "): decide per instance.", d1_extras(launched))
            eq(f"D1(iii) {label}: the whole automation scope, awaiting the consumer (X7-6c)", (launched[0]["scope"], launched[0]["complete"]),
               (["TC-1", "TC-2"], AWAITS))

        # a manual half is still to run: the receipt would close the WHOLE stage, so the runner goes as today
        driver, launched, moves, started = d1_driver(root, env, task, manual=("TC-9",))
        with D1Evidence(d1_answer(two)) as evidence:
            driver.stage_S6()
        eq("D1 manual present, every result stands: no receipt (it would close the manual half's stage too)", moves, [])
        eq("D1 manual present: the automation runner goes as today, not closing the stage", (len(launched), launched[0]["complete"]), (1, False))
        check_in("D1 manual present: and is told what stands", "Results that stand: test_a, test_b; run only: nothing.", d1_extras(launched))
        eq("D1 manual present: the manual block is for the loop's next entry", started, [])
        driver, launched, moves, started = d1_driver(root, env, task, manual=("TC-9",), accepted_auto=True)
        with D1Evidence(d1_answer(two)) as evidence:
            driver.stage_S6()
        eq("D1 manual present, the automation half accepted: the manual block still runs, nothing is asked or dispatched",
           (started, launched, moves, evidence.asked), ([("S6", "manual")], [], [], []))

        # the other edges: nothing is asked where nothing is to run
        driver, launched, moves, started = d1_driver(root, env, task, accepted_auto=True)
        with D1Evidence(d1_answer(two)) as evidence:
            driver.stage_S6()
        eq("D1 edge: `auto_done` and no manual half: unchanged - nothing asked, dispatched or closed",
           (evidence.asked, launched, moves, started), ([], [], [], []))
        driver, launched, moves, started = d1_driver(root, env, task, auto=(), manual=("TC-9",))
        with D1Evidence(d1_answer(two)) as evidence:
            driver.stage_S6()
        eq("D1 edge: an empty automation scope (a handed case is out of it already): only the manual block, nothing asked",
           (evidence.asked, launched, moves, started), ([], [], [], [("S6", "manual")]))
        driver, launched, moves, started = d1_driver(root, env, task, auto=(), manual=())
        with D1Evidence(d1_answer(two)) as evidence:
            driver.stage_S6()
        eq("D1 edge: nothing to execute at all is today's code-only close, the record is not asked",
           ([m[:2] for m in moves if m[0] == "code_only"], [m[0] for m in moves], evidence.asked),
           ([("code_only", "S6")], ["finalize", "code_only", "stage_done"], []))
    finally:
        unpin_project(pin)
        harness.cleanup(root)

    # POSITIONAL: the stand question is before the record. An unconfirmed stand asks, and nothing has been
    # asked of the record, dispatched or closed when it does (the invariant `stand_check` documents).
    root, task_root, env = d2_seed(task, environment="Local", pending=True, url=D2_DEAD)
    try:
        d1_write_blocks(task_root)
        driver, launched, moves, started = d1_driver(root, env, task)
        with D1Evidence(d1_answer(two)) as evidence:
            code = d2_enter(driver, "S6")
        eq("D1 position: an unconfirmed stand asks its question first: exit 3", code, 3)
        eq("D1 position: and before it the record was not asked, no runner, no receipt, no close",
           (evidence.asked, launched, moves, started), ([], [], [], []))
        check_in("D1 position: it is the stand question", "kind: environment", s0_question(task_root))
    finally:
        harness.cleanup(root)


def d1_texts() -> None:
    """D2: what the roles are told. The texts sit inside long methods, so they are read from the source as
    the string constants they are (an f-string is its literal parts) - a pin on the words, not on the layout."""
    import ast
    texts, parts = [], set()
    nodes = [node for _path, source in harness.driver_sources() for node in ast.walk(ast.parse(source))]      # every file of the driver set, parsed apart
    for node in nodes:
        if isinstance(node, ast.JoinedStr):
            parts.update(id(p) for p in node.values)      # its literal pieces are counted once, whole
            texts.append("".join(p.value for p in node.values if isinstance(p, ast.Constant)))
    for node in nodes:
        if isinstance(node, ast.Constant) and isinstance(node.value, str) and id(node) not in parts:
            texts.append(node.value)
    whole = "\n".join(texts)
    check_in("D2 critic: probe_by_code once per instance, every check of the test",
             "then probe_by_code.py once per instance, every check of the test: ", whole)
    check_in("D2 critic: red_sandbox only on doubt, proves only the one check it names, the others stay owed",
             "red_sandbox.py --probe (only when you doubt the check looks at the product, with the reason in your findings) proves only the one check it names, the others stay owed", whole)
    check_in("D2 critic: a probe of unchanged bytes and the same entries is answered already_probed", "a probe of unchanged bytes and the same entries is answered `already_probed`", whole)
    check_in("D2 critic: the rest is kept", "write your findings file and the review_receipt_ref on the manifest bindings; `cause:` on each finding.", whole)
    words = "re-run only the instances whose code changed; a comment/docstring/marker-only fix keeps its run (the factory answers `reused`)."
    eq("D2 rework: both S5 repair texts (the test-defect round and the mechanical one) say it", whole.count(words), 2)
    check_not_in("D2 rework: and neither says `files changed` any more", "whose files changed", whole)
    check_in("D2 S7 repair: re-run only the failed test through --mine, node id, repair_verify",
             "--node-id <test> --purpose repair_verify`; FLAKY confirmation per s7.md (at most 3 flaky_diagnostic runs, S7).", whole)
    check_not_in("D2 S7 repair: the old `--request` wording is gone", "run_suite.py --request with purpose repair_verify", whole)


def main() -> None:
    run_scenarios([], [
        s5_critic_finish_passes_window,
        d1_s6_freshness,
        d1_texts,
    ])
    harness.finish("test_story_run_s6_d1")


# split: runner piece 1
if __name__ == "__main__":
    main()
