"""hf2 11b: a part of test_story_run_s6.py, split by tools/test_split.py (TD-11c). The shared helpers are in story_run_s6_common."""
import json
import re
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness  # noqa: E402
import story_run_common  # noqa: E402
del story_run_common  # split: imported for its sys.path effect
from story_run_common import run_scenarios, D1Evidence, D1_SAME, check, check_eq, check_in, check_not_in, d1_answer, d1_driver, d1_extras, d2_pipeline, d2_seed, driver_for, eq, seed
from story_run_s6_common import (  # noqa: E402
    ACCEPTED_S6, AWAITS, ManualWorld, REPLAY_A, REPLAY_B, Staleness, WHY_RUN, d1_blocks, enter_manual,
    manual_rig, pin_project, record_failure_analyst_accept, reprobe_rig, row, stale_probe, unpin_project,
)


RUNNING_S6 = {"S6-qa-runner-1": {"id": "S6-qa-runner-1", "stage": "S6", "status": "running", "execution_kind": "automation",
                                  "scope": ["TC-1", "TC-2"]}}


def close_digest(moves) -> str:
    """The `--digest` of the `stage_done` the code close wrote."""
    args = next((m[1] for m in moves if m[0] == "stage_done"), "")
    return args.split("--digest ", 1)[1].rsplit(" --no-journal", 1)[0] if "--digest " in args else ""


def hf2_11b_s6_freshness_reads_the_run_rows_shas() -> None:
    """K1 + P7: a result the evidence function keeps moves from `stand` to `run` when the run row's own shas say it ran other code
    (a helper module `helper_files` does not name: the evidence compares the whole-file fingerprint and keeps it); `probes` holds the
    stale live checks; `unknown` is NOT stale; the keys are today's plus `probes`; an exception is `undecided`, as today.
    MUTATION `s6_freshness leaves a staleness-stale instance in stand` -> the first three checks fail."""
    task = "QA-9"
    two = {"test_a": ("result", "passed", ""), "test_b": ("result", "failed", "")}
    root, task_root, env = d2_seed(task, environment="Local", pending=False)
    pin = pin_project(root)
    try:
        d1_blocks(root, task_root)
        driver, launched, moves, _started = d1_driver(root, env, task)
        answer = {"test_a": row(("stale", WHY_RUN)), "test_b": row(("fresh", ""), stale_probe(REPLAY_B))}
        with D1Evidence(d1_answer(two)), Staleness(answer) as held:
            fresh = driver.s6_freshness(["TC-1", "TC-2"])
        eq("K1 the staleness reader is asked once, for the instances the evidence named", held.calls, [["test_a", "test_b"]])
        eq("K1 the instance whose run row says other code leaves `stand` for `run`, with the reader's words",
           (fresh["stand"], fresh["run"]), (["test_b"], {"test_a": WHY_RUN}))
        eq("K1 and the counts follow the results that stand", (fresh["passed"], fresh["failed"]), (0, 1))
        eq("K1 `probes` holds the stale live check with its replay", fresh["probes"], {"test_b": REPLAY_B})
        eq("K1 the keys are today's plus `probes`", sorted(fresh), sorted(["decided", "why", "stand", "run", "passed", "failed", "probes"]))
        eq("P7 the runner is told the SAME predicate's answer",
           driver.s6_freshness_lines(fresh), [f"Results that stand: test_b; run only: test_a ({WHY_RUN})."])
        with D1Evidence(d1_answer(two)), Staleness({"test_a": row(("unknown", "the run recorded no per-test identity")), "test_b": row()}):
            fresh = driver.s6_freshness(["TC-1", "TC-2"])
        eq("K1 `unknown` is not `stale`: both results stand, no live check is stale",
           (fresh["stand"], fresh["run"], fresh["probes"]), (["test_a", "test_b"], {}, {}))
        with D1Evidence(d1_answer(two)), Staleness(RuntimeError("boom")):
            fresh = driver.s6_freshness(["TC-1", "TC-2"])
        eq("K1 an exception inside the reader is `undecided`, with its words, and the keys are the same",
           (fresh["decided"], fresh["why"], fresh["probes"], fresh["run"]), (False, "RuntimeError: boom", {}, {}))
        with D1Evidence({"instances": {}, "observed": False, "why": "run-budget.json cannot be read"}):
            fresh = driver.s6_freshness(["TC-1", "TC-2"])
        eq("K1 an undecided answer of the evidence carries `probes` too", (fresh["decided"], fresh["probes"]), (False, {}))
    finally:
        unpin_project(pin)
        harness.cleanup(root)


def hf2_11b_stale_live_checks_are_proved_again_before_the_reduction() -> None:
    """K2 + K-P5 + K-P9: every run stands, some live checks are stale, a stand is up -> one `probe_by_code.py` each, BEFORE
    `finalize_task.py`, the close at site `s6.reprobed` with the count and the time in the digest. A failed proof, a verdict other than
    `intended_failure`, a `replay` of None, a refusal of the close context: ONE digest line each, no question, S6 closes.
    HF3-6 (B-K1..B-K4): no running dispatch -> `--s6-close`; a running one -> `--dispatch`; the receipt names each probe record.
    MUTATIONS: `the probe before the runs` -> K3 (next scenario); `no running dispatch and no call (S6_NO_DISPATCH back)` -> B-K1;
    `--s6-close with a running S6 dispatch` -> B-K2; `the records not in the evidence` -> B-K3; `a refusal of the context stops S6`
    -> B-K4; `the empty set changes the digest` -> K5."""
    import story_run
    task = "QA-9"
    two = {"test_a": ("result", "passed", ""), "test_b": ("result", "failed", "")}
    both = {"test_a": row(("fresh", ""), stale_probe(REPLAY_A)), "test_b": row(("fresh", ""), stale_probe(REPLAY_B))}
    root, task_root, env = d2_seed(task, environment="Local", pending=False)
    pin = pin_project(root)
    try:
        d1_blocks(root, task_root)
        # every proof lands: before the reduction, in the order of the instances, under the OPEN dispatch
        driver, launched, moves, probes, sites = reprobe_rig(root, env, task, dispatches=RUNNING_S6)
        with D1Evidence(d1_answer(two)), Staleness(both):
            driver.stage_S6()
        eq("K2 the proofs come BEFORE the reduction, then the receipt, then the close; no runner",
           ([m[0] for m in moves], launched), (["probe", "probe", "finalize", "code_only", "stage_done"], []))
        eq("K2 the first proof is the replay of the record, under the open S6 dispatch",
           probes[0], ["--task", task, "--dispatch", "S6-qa-runner-1", "--test", "tests/t.py::test_a", "--instance", "test_a",
                       "--mutation", "invert", "--json"])
        eq("K2 and the second names its mutation and the oracle the record had (`--oracle`)",
           probes[1][-5:], ["--mutation", "expected", "--json", "--oracle", "tests/helpers.py::expected_total"])
        eq("K2 the close is at its own site", sites, ["s6.reprobed"])
        digest = close_digest(moves)
        check_in("K2 the digest says how many were proved again, with the time", "re-proved 2 probes after the tests changed (", digest)
        check("K2 ...and the time is a number of seconds", re.search(r"\(\d+ s\)", digest) is not None, digest)
        check_in("K2 the receipt's reason carries the same words", "re-proved 2 probes after the tests changed", moves[3][2])
        eq("K2 the receipt stands on the manifest and the jobs", moves[3][3], ["work/automation-manifest.json", "state/execution-jobs"])

        # a proof that fails (exit 2, the tool's refusal) and one that answers another verdict: a line each, no question, S6 closes
        def reply(argv):
            if "test_a" in argv[argv.index("--instance") + 1]:
                return 2, json.dumps({"status": "refused", "error": "no active dispatch in story QA-9"})
            return 0, json.dumps({"verdict": "no_failure", "words": "the inverted assertion did not fail"})
        driver, launched, moves, probes, sites = reprobe_rig(root, env, task, dispatches=RUNNING_S6, reply=reply)
        with D1Evidence(d1_answer(two)), Staleness(both):
            driver.stage_S6()
        digest = close_digest(moves)
        check_in("K2 a failed proof is one line with its exit and the tool's words",
                 "test_a: not proved again (probe_by_code exit 2): no active dispatch in story QA-9", digest)
        check_in("K2 a verdict other than intended_failure is one line with the tool's words",
                 "test_b: the probe gave `no_failure`, not `intended_failure`: the inverted assertion did not fail", digest)
        check_in("K2 and nothing was proved", "re-proved 0 probes after the tests changed (", digest)
        eq("K2 neither failure asks anyone or stops S6: the close is recorded", ([m[0] for m in moves][-2:], sites), (["code_only", "stage_done"], ["s6.reprobed"]))

        # K-P9: a replay of None names the instance, the other is still proved
        driver, launched, moves, probes, sites = reprobe_rig(root, env, task, dispatches=RUNNING_S6)
        with D1Evidence(d1_answer(two)), Staleness({"test_a": row(("fresh", ""), stale_probe(None)), "test_b": both["test_b"]}):
            driver.stage_S6()
        digest = close_digest(moves)
        check_in("K-P9 a probe code cannot replay is named, with why", "test_a: not proved again - the probe cannot be replayed by code", digest)
        check_in("K-P9 ...among the reasons: the line anchor moved with the edit", "the probe's line anchor moved with the edit", digest)
        eq("K-P9 only the replayable one is proved", [p[p.index("--instance") + 1] for p in probes], ["test_b"])
        check_in("K-P9 and counted", "re-proved 1 probes after the tests changed (", digest)

        # B-K1 (was K-P5, HF3-6): no RUNNING dispatch -> the tool IS called, for every replay, in the close context of S6
        # (`--s6-close`, never `--dispatch`); the old line is gone; S6 closes at its site
        for label, table in (("none at all", {}), ("an accepted one only", ACCEPTED_S6)):
            # an accepted automation runner is `auto_done`: that is the re-entry (the mark says the runner was ours), not the first entry
            driver, launched, moves, probes, sites = reprobe_rig(root, env, task, dispatches=table, mark="S6-qa-runner-1" if table else None)
            with D1Evidence(d1_answer(two)), Staleness(both):
                driver.stage_S6()
            digest = close_digest(moves)
            eq(f"B-K1 {label}: the tool is called for each replay, in order", [p[p.index("--instance") + 1] for p in probes], ["test_a", "test_b"])
            eq(f"B-K1 {label}: every call names the close context and no dispatch",
               [("--s6-close" in p, "--dispatch" in p) for p in probes], [(True, False)] * 2)
            check_in(f"B-K1 {label}: the digest says what was proved again", "re-proved 2 probes after the tests changed (", digest)
            check_not_in(f"B-K1 {label}: the old line is nowhere in the digest", "re-probe skipped: no open S6 dispatch", digest)
            eq(f"B-K1 {label}: the stage closes at its site, after the proofs", (sites, [m[0] for m in moves]),
               (["s6.reprobed"], ["probe", "probe", "finalize", "code_only", "stage_done"]))
        eq("B-K1 the constant of the old line is gone", hasattr(story_run.Driver, "S6_NO_DISPATCH"), False)

        # B-K2: a RUNNING S6 dispatch -> `--dispatch <id>`, never `--s6-close` (the tool runs under the role's own dispatch)
        driver, launched, moves, probes, sites = reprobe_rig(root, env, task, dispatches=RUNNING_S6)
        with D1Evidence(d1_answer(two)), Staleness(both):
            driver.stage_S6()
        eq("B-K2 a running S6 dispatch: the call carries it and not the close context",
           [("--dispatch" in p and p[p.index("--dispatch") + 1], "--s6-close" in p) for p in probes], [("S6-qa-runner-1", False)] * 2)

        # B-K3: the receipt names each probe record the tool printed; a refusal printed none
        def reply_records(argv):
            if "test_a" in argv[argv.index("--instance") + 1]:
                return 0, json.dumps({"verdict": "intended_failure", "record": "work/probes/test_a.json"})
            return 2, json.dumps({"status": "refused", "error": "a dispatch is open in this story (S6-x): a probe runs under it"})
        driver, launched, moves, probes, sites = reprobe_rig(root, env, task, dispatches={}, reply=reply_records)
        with D1Evidence(d1_answer(two)), Staleness(both):
            driver.stage_S6()
        eq("B-K3 the receipt stands on the manifest, the jobs and the record of the proof that gave one",
           next(m[3] for m in moves if m[0] == "code_only"), ["work/automation-manifest.json", "state/execution-jobs", "work/probes/test_a.json"])

        # B-K3 + B-K4: a refusal of the context (exit 2, no record) is ONE line with the tool's words, no question, S6 closes
        driver, launched, moves, probes, sites = reprobe_rig(root, env, task, dispatches={}, reply=lambda argv: (
            2, json.dumps({"status": "refused", "error": "a dispatch is open in this story (S6-x): a probe runs under it"})))
        with D1Evidence(d1_answer(two)), Staleness(both):
            driver.stage_S6()
        digest = close_digest(moves)
        check_in("B-K4 the refused context is a digest line with the exit and the tool's words",
                 "test_a: not proved again (probe_by_code exit 2): a dispatch is open in this story (S6-x)", digest)
        eq("B-K4 one line each (one per instance) and nothing was proved", (digest.count("not proved again (probe_by_code exit 2)"), "re-proved 0 probes" in digest), (2, True))
        eq("B-K4 no question, S6 is closed at its site", ([m[0] for m in moves][-2:], sites), (["code_only", "stage_done"], ["s6.reprobed"]))
        eq("B-K3 a refusal printed no record: the evidence is the base", next(m[3] for m in moves if m[0] == "code_only"),
           ["work/automation-manifest.json", "state/execution-jobs"])
        # a record path that is not a probe record of the story is not evidence (never a path out of the story)
        driver, launched, moves, probes, sites = reprobe_rig(root, env, task, dispatches={}, reply=lambda argv: (
            0, json.dumps({"verdict": "intended_failure", "record": "../../etc/x.json"})))
        with D1Evidence(d1_answer(two)), Staleness(both):
            driver.stage_S6()
        eq("B-K3 a record path outside work/probes is not named", next(m[3] for m in moves if m[0] == "code_only"),
           ["work/automation-manifest.json", "state/execution-jobs"])
        # G-2 (t-1277): an `already_probed` answer by a product record prints `work/probes/product/<stem>.json`: it is named,
        # once, like the `probe_record` one; a path that climbs out of that folder, or goes deeper, is still dropped
        for label, printed, named in (
                ("a product record is named", "work/probes/product/test_a.json", ["work/probes/product/test_a.json"]),
                ("a product record deeper down is not", "work/probes/product/x/test_a.json", []),
                ("a climb out of the product folder is not", "work/probes/product/../../x.json", [])):
            driver, launched, moves, probes, sites = reprobe_rig(root, env, task, dispatches={}, reply=lambda argv, p=printed: (
                0, json.dumps({"verdict": "intended_failure", "record": p})))
            with D1Evidence(d1_answer(two)), Staleness(both):
                driver.stage_S6()
            eq(f"G-2 {label} (once for the two instances)", next(m[3] for m in moves if m[0] == "code_only"),
               ["work/automation-manifest.json", "state/execution-jobs"] + named)
    finally:
        unpin_project(pin)
        harness.cleanup(root)


def hf2_11b_the_tool_takes_only_a_running_dispatch() -> None:
    """The fact K-P5 stands on, from the tool itself (`execution_request.find_active_dispatch`, what `probe_by_code.py` reaches
    through `build_mine_request`): an `accepted` dispatch is refused, a `running` one is found. The code-closed S6 path opens no
    dispatch (`close_by_code` -> `code_only` is a receipt, and the controller REFUSES it while any dispatch is running). The road
    without a running dispatch is `--s6-close` (HF3-6)."""
    import tempfile
    import execution_request
    for status, found in (("accepted", False), ("running", True)):
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp) / "QA-9" / "state"
            state.mkdir(parents=True)
            (state / "controller.json").write_text(json.dumps({"dispatches": {"S6-qa-runner-1": {
                "id": "S6-qa-runner-1", "stage": "S6", "status": status, "scope": ["TC-1"]}}}), encoding="utf-8")
            try:
                got = execution_request.find_active_dispatch(Path(tmp), "QA-9", "S6-qa-runner-1", ["TC-1"])[2]["id"]
            except execution_request.MineRefusal:
                got = None
            eq(f"a {status} S6 dispatch is {'found' if found else 'refused'} by the tool the proof goes through", got, "S6-qa-runner-1" if found else None)


def hf2_11b_stale_runs_go_to_the_runner_and_the_proofs_follow() -> None:
    """K3 + invariant (i): stale RUNS -> the runner as today, launched with `complete=False` when stale live checks are owed, no
    probe before it (a probe is never next to code with no run on its current bytes); on its return (`auto_done`) the proofs, the
    reduction and the close at `s6.reprobed`; once per life of S6; the second life (no mark of ours) probes only when every run
    stands. MUTATIONS: `the probe before the runs` -> the first check; `complete=True with stale probes` -> the complete check;
    `the no-consumer window owes nothing` (driver_stage_s6.py `not owed` -> `owed`) -> the no-consumer check; `the consumer's record is
    not written` -> the re-entry key after the record."""
    import story_run
    from unittest import mock
    task = "QA-9"
    two = {"test_a": ("stale", "", D1_SAME), "test_b": ("result", "failed", "")}
    answer = {"test_a": row(("stale", WHY_RUN), stale_probe(REPLAY_A)), "test_b": row(("fresh", ""), stale_probe(REPLAY_B))}
    root, task_root, env = d2_seed(task, environment="Local", pending=False)
    pin = pin_project(root)
    try:
        d1_blocks(root, task_root)
        driver, launched, moves, probes, sites = reprobe_rig(root, env, task, dispatches=RUNNING_S6)
        with D1Evidence(d1_answer(two)), Staleness(answer):
            driver.stage_S6()
        eq("K3 stale runs: the runner is dispatched, whole scope, and NOT closing the stage; no probe, no close before it",
           ([(e["role"], e["scope"], e["complete"]) for e in launched], moves, sites), ([("qa-runner", ["TC-1", "TC-2"], AWAITS)], [], []))         # X7-6c: awaits the consumer (the proofs run at s6_reentry)
        check_in("K3 and it is told what stands and what to run, as today", f"Results that stand: test_b; run only: test_a ({D1_SAME}).",
                 d1_extras(launched))
        eq("K3 the close the runner no longer makes is OWED: the mark is set (before the runner; the dispatch id is filled after it)",
           driver.state.get("s6_probe_after"), "")

        # the runner came back, accepted in this life (the mark names it); the runs stand now; an OPEN dispatch is there
        both_open = dict(ACCEPTED_S6, **{"S6-probe-1": dict(RUNNING_S6["S6-qa-runner-1"], id="S6-probe-1")})
        fresh_runs = {"test_a": row(("fresh", ""), stale_probe(REPLAY_A)), "test_b": row(("unknown", "the run recorded no per-test identity"),
                                                                                            stale_probe(REPLAY_B))}
        # PC2-3: the FIRST re-entry runs with the consumer ON: the runner's entry carries its `role` (a scenario-local copy: `ACCEPTED_S6` is
        # shared with a reader that must not change colour), so `acceptance.stage_author_dispatch` names it as the author. The stage closes only
        # AFTER the consumer's record exists (driver_stage_s6.py X7-6 comment: the proofs run in `s6_reentry` "after the record, whose close
        # site finds it"): before the record the close is REFUSED naming it, nothing proved, nothing closed; after it, the close follows.
        authored = dict(both_open, **{k: dict(v, role="qa-runner") for k, v in ACCEPTED_S6.items()})
        driver, launched, moves, probes, sites = reprobe_rig(root, env, task, dispatches=authored, mark="S6-qa-runner-1")
        refused = ""
        with D1Evidence(d1_answer(two)), Staleness(fresh_runs):
            try:
                driver.stage_S6()
            except story_run.Refusal as refusal:
                refused = refusal.text
        eq("K3 re-entry before the consumer's record: refused, naming the record; no proof, no reduction, no close",
           (refused.startswith("S6 cannot be closed at s6_reentry: no accept record of qa-failure-analyst stands for S6-qa-runner-1"),
            moves, sites), (True, [], []))
        # FV3-22 E-M2 (FR-2): the person's-word door the refusal prints is one `waiver.py` can run - it carries its words file
        # (`waiver.py` refuses `--stage/--block` without `--decision` or `--words-file`), built by `stage_close.person_word_door`, the one renderer
        import acceptance
        import person_words
        door = person_words.door(f'waiver.py --task {driver.task} --stage S6 --block "{acceptance.STAGE_ACCEPTANCE_PHRASE}"')
        eq("K3 the same refusal ends with the person's-word door WITH its words file",
           (refused.endswith(f"(`{door}`)."), " --words-file " in door), (True, True))
        record_failure_analyst_accept(driver, "S6-qa-runner-1")      # the analyst's verdict now stands for the runner's dispatch
        driver, launched, moves, probes, sites = reprobe_rig(root, env, task, dispatches=authored, mark="S6-qa-runner-1")
        with D1Evidence(d1_answer(two)) as evidence, Staleness(fresh_runs):
            driver.stage_S6()
        eq("K3 re-entry: no evidence asked, no runner, the proofs, THEN the reduction, the receipt, the close",
           (evidence.asked, launched, [m[0] for m in moves]), ([], [], ["probe", "probe", "finalize", "code_only", "stage_done"]))
        eq("K3 under the open dispatch, one site", ([p[p.index("--dispatch") + 1] for p in probes], sites), (["S6-probe-1"] * 2, ["s6.reprobed"]))
        check_in("K3 the digest", "re-proved 2 probes after the tests changed (", close_digest(moves))
        check_not_in("K3 the close is the stage's own: the mark is gone", "s6_probe_after", json.dumps(driver.state))

        # The rigs below run with NO consumer for S6 (`acceptance.consumer_of` answers "", the same patch as the no-consumer check at the end):
        # they pin the re-probe logic of a later life, and `both_open` names no author; the consumer-on world is the two re-entry keys above.
        with mock.patch("acceptance.consumer_of", lambda stage, table=None: ""):
            # once per life: the same entry again finds nothing stale and owes nothing
            driver, launched, moves, probes, sites = reprobe_rig(root, env, task, dispatches=both_open)
            with D1Evidence(d1_answer(two)), Staleness({"test_a": row(), "test_b": row()}):
                driver.stage_S6()
            eq("K3 once per life of S6: nothing stale and no mark -> no probe, no close, nothing asked", (moves, sites, launched), ([], [], []))

            # the runner is back but a run STILL has no current bytes (it was not run): no probe next to it; the close is owed all the same
            driver, launched, moves, probes, sites = reprobe_rig(root, env, task, dispatches=both_open, mark="S6-qa-runner-1")
            with D1Evidence(d1_answer(two)), Staleness({"test_a": row(("stale", WHY_RUN), stale_probe(REPLAY_A)), "test_b": row()}):
                driver.stage_S6()
            check_in("invariant (i) a stale run at the return: the proof is skipped and says why",
                     "re-probe skipped: 1 tests have no run on their current bytes (test_a)", close_digest(moves))
            eq("invariant (i) ...no probe, and the stage is still closed by code (the runner was told not to)", (probes, sites), ([], ["s6.reprobed"]))

            # the second life of S6 (`invalidate` leaves earlier dispatches accepted): no mark of ours.
            # `unknown` runs do NOT license a probe there - nothing says the runner ran in this life
            driver, launched, moves, probes, sites = reprobe_rig(root, env, task, dispatches=both_open)
            with D1Evidence(d1_answer(two)), Staleness(fresh_runs):
                driver.stage_S6()
            eq("second life, a run `unknown` and no mark: nothing is probed or closed (invariant (i))", (moves, sites), ([], []))
            # ...while runs that are fresh everywhere do
            driver, launched, moves, probes, sites = reprobe_rig(root, env, task, dispatches=both_open)
            with D1Evidence(d1_answer(two)), Staleness({"test_a": row(("fresh", ""), stale_probe(REPLAY_A)), "test_b": row(("fresh", ""))}):
                driver.stage_S6()
            eq("second life, every run fresh: the stale live check is proved, then the close",
               ([m[0] for m in moves], sites), (["probe", "finalize", "code_only", "stage_done"], ["s6.reprobed"]))

        # a manual half: the runner never closes the stage, so no mark is owed and nothing here changes
        driver, launched, moves, probes, sites = reprobe_rig(root, env, task, dispatches={}, manual=("TC-9",))
        with D1Evidence(d1_answer(two)), Staleness(answer):
            driver.stage_S6()
        eq("a manual half pending: the runner goes as today (complete=False), no mark, no probe",
           ([e["complete"] for e in launched], "s6_probe_after" in driver.state, probes), ([False], False, []))

        # no consumer: a stage table where S6 has no `acceptance_by` (older pipelines). The runner window is the identity of today: it closes
        # S6 itself (`complete` True) unless live checks are owed, which only the driver's own close can prove (`complete` False, the
        # mark set; driver_stage_s6.py "the runner does NOT close the stage" / `consumer_awaits` "the identity with no consumer")
        completes = []
        for stale_rows in (answer, {"test_a": row(("stale", WHY_RUN)), "test_b": row()}):      # owed probes / none owed
            driver, launched, moves, probes, sites = reprobe_rig(root, env, task, dispatches=RUNNING_S6)
            with mock.patch("acceptance.consumer_of", lambda stage, table=None: ""), D1Evidence(d1_answer(two)), Staleness(stale_rows):
                driver.stage_S6()
            completes.append([e["complete"] for e in launched])
        eq("no consumer of S6: the runner window owing live checks is not complete; the control with none owed is", completes, [[False], [True]])
    finally:
        unpin_project(pin)
        harness.cleanup(root)


def hf2_11b_without_a_stand_nothing_is_run_or_proved() -> None:
    """K4 + P11: the carrier of "no stand" is the recorded WORD `stand not confirmed` (not the text of the answer): the stage goes
    on, no probe is launched, and the digest says `N tests changed after their run are left for a run elsewhere` (P19 step 5).
    MUTATION `a probe with the stand not confirmed` -> the first check."""
    task = "QA-9"
    two = {"test_a": ("result", "passed", ""), "test_b": ("result", "failed", "")}
    both = {"test_a": row(("fresh", ""), stale_probe(REPLAY_A)), "test_b": row(("fresh", ""), stale_probe(REPLAY_B))}
    word = [{"stage": "S6", "match": "stand not confirmed", "decision": "carry on, I will run them on staging", "at": "2026-10-26T10:00:00+00:00", "by": "human"}]
    root, task_root, env = d2_seed(task, environment="Local", pending=True)
    pin = pin_project(root)
    try:
        d1_blocks(root, task_root)
        d2_pipeline(task_root, stage_overrides=word)
        driver, launched, moves, probes, sites = reprobe_rig(root, env, task, dispatches=RUNNING_S6)
        eq("P11 the word is recorded: no stand, whatever the answer's own text said", driver.s6_no_stand(), True)
        with D1Evidence(d1_answer(two)), Staleness(both):
            driver.stage_S6()
        eq("K4 every run stands, the live checks are stale, no stand: NO probe (an open dispatch is there)", probes, [])
        check_in("K4 the digest says how many were left for a run elsewhere", "2 tests changed after their run are left for a run elsewhere",
                 close_digest(moves))
        eq("K4 the stage closes as the other code closes do (the reduction first)", ([m[0] for m in moves], sites),
           (["finalize", "code_only", "stage_done"], ["s6.reprobed"]))

        # stale runs with no stand: no new run either - the runner is dispatched as today (the answer is undecided: no stand observed),
        # told the count, and not owed the close
        driver, launched, moves, probes, sites = reprobe_rig(root, env, task, dispatches=RUNNING_S6)
        answer = {"test_a": row(("stale", WHY_RUN)), "test_b": row(("fresh", ""), stale_probe(REPLAY_B))}
        with D1Evidence(d1_answer({"test_a": ("unknown", "", "the stand's version was not observed")}, observed=False)), Staleness(answer):
            driver.stage_S6()
        check_in("K4 stale runs: the runner is told how many are left for a run elsewhere",
                 "2 tests changed after their run are left for a run elsewhere", d1_extras(launched))
        eq("K4 ...is not told to leave the stage open, and no probe was launched",
           ([e["complete"] for e in launched], probes, "s6_probe_after" in driver.state), ([AWAITS], [], False))         # X7-6c

        # P11 negative control: the same pipeline WITHOUT the word is not "no stand"; a confirmed stand never is
        d2_pipeline(task_root, stage_overrides=[])
        eq("P11 control: an unconfirmed stand and NO word is not `no stand` (the stand question comes first)", driver.s6_no_stand(), False)
        d2_pipeline(task_root, stage_overrides=word, environment="Local", environment_pending=False)
        eq("P11 control: a confirmed stand is never `no stand`, whatever words are on file", driver.s6_no_stand(), False)
        driver, launched, moves, probes, sites = reprobe_rig(root, env, task, dispatches=RUNNING_S6)
        with D1Evidence(d1_answer(two)), Staleness(both):
            driver.stage_S6()
        eq("P11 control: with the stand confirmed the same stale live checks ARE proved", len(probes), 2)
    finally:
        unpin_project(pin)
        harness.cleanup(root)


def fv3_21_the_stand_word_reaches_the_manual_half() -> None:
    """FV3-21 K1 + K6 (card r2 section 2): the person's no-stand word reaches the manual half of S6 - no walk is dispatched, no question
    asked, each case is `left_unchecked` in the person's words (W1-W6), a case prepare refused keeps its own record (W14), an accepted record
    is never overwritten (W7), a case a deferred question holds is refused once with its own reason (W8), a live S6 dispatch or an unreadable
    state is today's road (W12*), no word / a confirmed stand / a dead word is today's road (C1-C6); and a close with nothing left to dispatch
    awaits the analyst instead of a Refusal (W13*), never closing without a record or a pass. Expected texts are literals.
    MUTATIONS: the `return self.manual_no_stand(...)` line deleted -> W1; `skip=()` in `manual_no_stand` -> W8; the `await_at` test False -> W13."""
    import contextlib
    import hashlib
    import io
    import manual_evidence as ME
    import story_run
    from controller import stamp_utc
    task = "QA-9"
    reason_of = lambda said: f'not checked by an agent: no stand is confirmed for this story; the person said: "{said}"'
    REASON = reason_of("go on")
    DOOR = "record a stand for this project with the onboarding; the next run checks it by hand"
    WORD = {"stage": "S6", "match": "stand not confirmed", "decision": "go on", "at": "2026-11-17T10:00:00+00:00", "by": "human"}
    ACCEPT_WORD = {"stage": "S6", "match": "stage acceptance", "decision": "accept the run", "at": "2026-11-17T10:00:00+00:00", "by": "human"}
    CASES = ["TC_001", "TC_002"]
    AUTHOR = {"stage": "S6", "role": "qa-runner", "status": "accepted", "execution_kind": "automation", "scope": ["TC_900"]}
    roots = []

    def rig(cases=CASES, environment=None, pending=True, overrides=(WORD,), refused=(), dispatches=None):
        root, task_root, env = d2_seed(task, environment=environment, pending=pending)
        roots.append(root)
        d2_pipeline(task_root, stage_overrides=list(overrides) if isinstance(overrides, (list, tuple)) else overrides)
        world = ManualWorld()
        world.dispatches.update({k: dict(v, id=k) for k, v in (dispatches or {}).items()})     # a controller row carries its own id
        driver, world, launched, moves = manual_rig(root, env, task, cases, refused=refused, world=world)
        sites, prepared = [], []
        real_close, real_prepare, inner_py = driver.close_by_code, driver.manual_prepare, driver.py
        driver.close_by_code = lambda *a, **k: (sites.append(k.get("site")) or real_close(*a, **k))
        driver.manual_prepare = lambda case: (prepared.append(case) or real_prepare(case))
        driver.py = lambda script, *a, **k: (0, "") if script == "project_decisions.py" else inner_py(script, *a, **k)
        driver.accepted_at = lambda author: stamp_utc(1794906000)       # the runner was accepted at 2026-11-17T09:00:00Z, before the pass `at`
        return driver, world, launched, moves, sites, prepared, task_root

    def request(task_root, case):
        path = task_root / "work" / "evidence" / "manual" / case / "request.json"
        return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else None

    def refusals(task_root, cases=CASES):
        return {case: (request(task_root, case) or {}).get("refused") for case in cases}

    def pipeline_of(task_root):
        return json.loads((task_root / "pipeline.json").read_text(encoding="utf-8"))

    try:
        # --- the branch is taken: no walk, no question, every case left unchecked in the person's words (W1-W6)
        long_words = "x" * 2000
        edge = "y" * story_run.Driver.QUOTE_LIMIT
        for label, kwargs, said, console_cut in (
                ("W1 no stand, word on S6", {}, "go on", False),
                ("W2 word on S5", {"overrides": [dict(WORD, stage="S5")]}, "go on", False),
                ("W3 named stand, pending", {"environment": "Local"}, "go on", False),
                ("W4 multi-line, non-ASCII words", {"overrides": [dict(WORD, decision="go on\n  " + chr(0xE9) + " later")]},
                 "go on " + chr(0xE9) + " later", False),
                ("W5 2000 characters", {"overrides": [dict(WORD, decision=long_words)]}, long_words, True),
                ("W5a exactly QUOTE_LIMIT characters", {"overrides": [dict(WORD, decision=edge)]}, edge, False),
                ("W6 `*` pass on S6", {"overrides": [dict(WORD, match="*")]}, "go on", False)):
            driver, world, launched, moves, sites, prepared, task_root = rig(**kwargs)
            text, new = enter_manual(driver, world, CASES, accept=False)
            eq(f"{label}: nothing launched (checked first), no dispatch registered", (launched, new, sorted(world.dispatches)), ([], "", []))
            eq(f"{label}: each case prepared once, no question", prepared, CASES)
            want = {"reason": reason_of(said), "door": DOOR, "by": "left_unchecked"}
            eq(f"{label}: both requests hold the person's words whole, the door and `left_unchecked`", refusals(task_root), {c: want for c in CASES})
            eq(f"{label}: reduced, then closed by code at the manual close", ([m[0] for m in moves], sites),
               (["finalize", "code_only", "stage_done"], ["s6.manual_close"]))
            line = "S6: TC_001: not checked by hand — not checked by an agent: no stand is confirmed for this story; the person said: \""
            check_in(f"{label}: the console says it", line, text)
            if console_cut:
                check("W5 the console quote is cut at the limit and says so", ("x" * story_run.Driver.QUOTE_LIMIT + driver.CUT + '"') in text)
            elif said == edge:
                check_in("W5a the console quote at the limit is whole, not cut", edge + '"', text)
        # --- case-level rows
        done = {"S6-qa-runner-1": {"stage": "S6", "role": "qa-runner", "status": "accepted", "execution_kind": "manual",
                                   "manual_case_ids": ["TC_003"], "scope": ["TC_003"]}}
        driver, world, launched, moves, sites, prepared, task_root = rig(cases=CASES + ["TC_003"], dispatches=done)
        record_failure_analyst_accept(driver, "S6-qa-runner-1")
        enter_manual(driver, world, CASES + ["TC_003"], accept=False)
        eq("W7 an accepted manual record is never overwritten; the close counts it", (request(task_root, "TC_003"), "1 case(s) checked by an agent by hand, 2 not checked" in moves[1][2]),
           (None, True))
        driver, world, launched, moves, sites, prepared, task_root = rig()
        driver.state["deferred"] = [{"n": 1, "kind": "walk_account", "holds": ["TC_002"]}]
        enter_manual(driver, world, CASES, accept=False)
        eq("W8 a case a deferred question holds is refused ONCE with its own reason and never prepared",
           (refusals(task_root, ["TC_002"])["TC_002"]["reason"], prepared),
           ("not checked yet: it waits for your answer to question 1, asked before gate B", ["TC_001"]))
        eq("W8 ...and the other case holds the no-stand reason", refusals(task_root, ["TC_001"])["TC_001"]["reason"], REASON)

        # W14: prepare refuses TC_002 for its OWN reason (the rig's stub writes the record the real prepare writes)
        driver, world, launched, moves, sites, prepared, task_root = rig(refused=["TC_002"])
        own = {"reason": "the check could not be taken: TC_002 stands as not checked by hand", "door": "its own door"}
        ME.atomic_json(ME.request_path(task_root, "TC_002"), {"refused": own})
        text, new = enter_manual(driver, world, CASES, accept=False)
        eq("W14 prepare's own refusal keeps its record (no second write); the other case holds the no-stand reason",
           refusals(task_root), {"TC_001": {"reason": REASON, "door": DOOR, "by": "left_unchecked"}, "TC_002": own})
        check_in("W14 ...and is printed with its reason", "S6: TC_002: not checked by hand — the check could not be taken", text)
        driver, world, launched, moves, sites, prepared, task_root = rig()
        driver.manual_prepare = lambda case: (["OB-x"], "", "factory failed") if case == "TC_002" else ([f"OB-{case}"], "", "")
        text, new = enter_manual(driver, world, CASES, accept=False)
        eq("W14b a case the factory failed to prepare is refused with the no-stand reason; nothing is walked",
           (launched, refusals(task_root)["TC_002"]["reason"]), ([], REASON))

        # --- W12: a live S6 dispatch (any scope) or an unreadable dispatch state at entry = today's road, one line
        running = {"stage": "S6", "role": "qa-runner", "status": "running", "execution_kind": "manual", "scope": ["TC_002"]}
        for label, dispatches, patch in (("W12 a live S6 dispatch", {"S6-qa-runner-5": running}, None),
                                         ("W12b ...with an empty scope", {"S6-qa-runner-5": dict(running, scope=[])}, None),
                                         ("W12c an unreadable dispatch state", None, lambda d: setattr(
                                             d, "s6_live_scopes", lambda: (_ for _ in ()).throw(RuntimeError("state down"))))):
            driver, world, launched, moves, sites, prepared, task_root = rig(dispatches=dispatches)
            if patch:
                patch(driver)
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                driver.manual_lane_plan(CASES)
            check_in(f"{label}: the one line says why the word waits", "an S6 walk is under way or stopped", out.getvalue())
            eq(f"{label}: today's road ran (prepare called), no request holds the no-stand reason",
               (prepared, [r for r in refusals(task_root).values() if r and r.get("reason") == REASON]), (CASES, []))

        # --- W13: an accepted not-complete author, nothing left to dispatch -> the stage awaits the consumer (B1), never a Refusal
        driver, world, launched, moves, sites, prepared, task_root = rig(dispatches={"S6-qa-runner-1": dict(AUTHOR)})
        text, new = enter_manual(driver, world, CASES, accept=False)
        eq("W13 first entry: reduced, NOT closed; the marker stands; both cases refused in the person's words",
           ([m[0] for m in moves], pipeline_of(task_root).get("acceptance_awaits"), [r["reason"] for r in refusals(task_root).values()]),
           (["finalize"], {"S6": "S6-qa-runner-1"}, [REASON, REASON]))
        check_in("W13 ...and says what it waits for", "S6: nothing is left to dispatch; S6 awaits the acceptance of qa-failure-analyst for S6-qa-runner-1", text)
        record_failure_analyst_accept(driver, "S6-qa-runner-1")
        enter_manual(driver, world, CASES, accept=False)
        eq("W13 after the analyst's record S6 closes at the manual close with the full receipt",
           ([m[0] for m in moves][1:], sites, "0 case(s) checked by an agent by hand, 2 not checked" in moves[-2][2]),
           (["finalize", "code_only", "stage_done"], ["s6.manual_close"], True))
        # W13b: the sibling - prepare refused every case, a confirmed stand, no word
        driver, world, launched, moves, sites, prepared, task_root = rig(environment="Local", pending=False, overrides=[], refused=CASES,
                                                                         dispatches={"S6-qa-runner-1": dict(AUTHOR)})
        text, new = enter_manual(driver, world, CASES, accept=False)
        eq("W13b every case refused by prepare after an accepted not-complete runner: the same await",
           ([m[0] for m in moves], pipeline_of(task_root).get("acceptance_awaits")), (["finalize"], {"S6": "S6-qa-runner-1"}))
        check_in("W13b ...each case printed with prepare's reason", "S6: TC_002: not checked by hand — the check could not be taken", text)
        # W13c: a NEWER running author dispatch - the wait would not hold: today's Refusal, no marker
        driver, world, launched, moves, sites, prepared, task_root = rig(dispatches={"S6-qa-runner-1": dict(AUTHOR)})
        world.dispatches["S6-qa-runner-2"] = dict(running, scope=["TC_001"], id="S6-qa-runner-2")
        try:
            driver.manual_close(["TC_001"], [])
            refusal = ""
        except story_run.Refusal as raised:
            refusal = str(raised)
        check_in("W13c a wait that would not hold is today's Refusal", "no accept record of qa-failure-analyst stands for S6-qa-runner-1", refusal)
        check("W13c ...and no marker is written", "acceptance_awaits" not in pipeline_of(task_root))
        # W13d: a person's live pass of the stage acceptance wins - the close goes on, no marker
        driver, world, launched, moves, sites, prepared, task_root = rig(overrides=(WORD, ACCEPT_WORD), dispatches={"S6-qa-runner-1": dict(AUTHOR)})
        enter_manual(driver, world, CASES, accept=False)
        eq("W13d a person's pass is recorded and the close goes on; no marker",
           (moves[-1][0], "code_only" in [m[0] for m in moves], "acceptance_awaits" in pipeline_of(task_root)), ("stage_done", True, False))
        # W13e: an unreadable pipeline.json = today's Refusal, the file is not touched
        driver, world, launched, moves, sites, prepared, task_root = rig(dispatches={"S6-qa-runner-1": dict(AUTHOR)})
        before = hashlib.sha256((task_root / "pipeline.json").read_bytes()).hexdigest()
        driver.pipeline = lambda: {}
        try:
            driver.manual_close(CASES, [])
            refusal = ""
        except story_run.Refusal as raised:
            refusal = str(raised)
        check_in("W13e an unreadable pipeline is today's Refusal", "no accept record of qa-failure-analyst stands for S6-qa-runner-1", refusal)
        eq("W13e ...and pipeline.json is byte-identical", hashlib.sha256((task_root / "pipeline.json").read_bytes()).hexdigest(), before)

        # --- C1-C6: the branch is not taken - exactly one manual dispatch, as today; no request holds the no-stand reason
        for label, kwargs in (("C1 a confirmed stand with the word on file", {"environment": "Local", "pending": False}),
                              ("C2 no stand, no word", {"overrides": []}),
                              ("C3 a revoked word", {"overrides": [dict(WORD, revoked_at="2026-11-17T11:00:00+00:00")]}),
                              ("C4 a word for S4", {"overrides": [dict(WORD, stage="S4")]}),
                              ("C5 stage_overrides is not a list", {"overrides": "broken"}),
                              ("C6 a word for another block", {"overrides": [dict(WORD, match="stand login missing")]})):
            driver, world, launched, moves, sites, prepared, task_root = rig(**kwargs)
            text, new = enter_manual(driver, world, CASES, accept=False)
            eq(f"{label}: one manual dispatch as today, prepared as today, no no-stand record",
               (bool(new), len(launched), prepared, [r for r in refusals(task_root).values() if r and r.get("reason") == REASON]), (True, 1, CASES, []))
    finally:
        for root in roots:
            harness.cleanup(root)


def hf2_11b_nothing_stale_is_byte_identical() -> None:
    """K5: the empty set changes nothing - today's calls, today's receipt text, today's digest, today's runner arguments (the older
    checks of `d1_s6_freshness` go through the real reader on a world whose run rows hold no per-test identity and stay green
    as they were). MUTATION `the empty set changes the digest` -> the digest check."""
    task = "QA-9"
    two = {"test_a": ("result", "passed", ""), "test_b": ("result", "failed", "")}
    root, task_root, env = d2_seed(task, environment="Local", pending=False)
    pin = pin_project(root)
    try:
        d1_blocks(root, task_root)
        driver, launched, moves, probes, sites = reprobe_rig(root, env, task, dispatches=RUNNING_S6)
        with D1Evidence(d1_answer(two)), Staleness({"test_a": row(), "test_b": row()}):
            driver.stage_S6()
        eq("K5 the moves are today's, with no probe", [m[0] for m in moves], ["finalize", "code_only", "stage_done"])
        eq("K5 the receipt's words and the site are today's",
           (moves[1][2], sites), ("every automated test has a result on its current bytes, on the same stand and version: "
                                  "1 passed, 1 failed - reused, nothing re-run", ["s6.results_stand"]))
        eq("K5 the digest is today's", close_digest(moves), "every automated result stands; nothing re-run")
        driver, launched, moves, probes, sites = reprobe_rig(root, env, task, dispatches={})
        with D1Evidence(d1_answer({"test_a": ("stale", "", D1_SAME), "test_b": ("result", "failed", "")})), Staleness({}):
            driver.stage_S6()
        eq("K5 stale runs, no live check: the runner as today (closing the stage), no mark",
           ([(e["scope"], e["complete"]) for e in launched], "s6_probe_after" in driver.state), ([(["TC-1", "TC-2"], AWAITS)], False))         # X7-6c
        check_in("K5 ...with today's line", f"Results that stand: test_b; run only: test_a ({D1_SAME}).", d1_extras(launched))
        check_not_in("K5 ...and no word of the new lines", "left for a run elsewhere", d1_extras(launched))
    finally:
        unpin_project(pin)
        harness.cleanup(root)


def hf2_11b_forty_tests_changed_by_one_fixture() -> None:
    """K6 + F-7 (a): one edit of a fixture makes 40 tests stale -> all 40 in `run only` (no sampling, no ceiling); and, when their
    runs stand, 40 proofs with the time in the digest."""
    task = "QA-9"
    ids = [f"t{n:02d}" for n in range(40)]
    results = {i: ("result", "passed", "") for i in ids + ["keep"]}
    root, task_root, env = d2_seed(task, environment="Local", pending=False)
    pin = pin_project(root)
    try:
        d1_blocks(root, task_root)
        driver, launched, moves, probes, sites = reprobe_rig(root, env, task, dispatches={})
        with D1Evidence(d1_answer(results)), Staleness({i: row(("stale", WHY_RUN)) for i in ids}):
            driver.stage_S6()
        extras = d1_extras(launched)
        eq("K6 the runner is dispatched, not the close", ([e["role"] for e in launched], moves), (["qa-runner"], []))
        check_in("K6 the result that stands is named", "Results that stand: keep; run only: t00 (", extras)
        eq("K6 all 40 are in `run only`", sum(f"{i} ({WHY_RUN})" in extras for i in ids), 40)
        driver, launched, moves, probes, sites = reprobe_rig(root, env, task, dispatches=RUNNING_S6)
        with D1Evidence(d1_answer(results)), Staleness({i: row(("fresh", ""), stale_probe(dict(REPLAY_A, instance=i))) for i in ids}):
            driver.stage_S6()
        eq("K6 40 proofs, none left out", sorted(p[p.index("--instance") + 1] for p in probes), ids)
        check("K6 the time is in the digest", re.search(r"re-proved 40 probes after the tests changed \(\d+ s\)", close_digest(moves)) is not None,
              close_digest(moves))
    finally:
        unpin_project(pin)
        harness.cleanup(root)


def test_consumer_round_cap_is_data() -> None:
    """B1 (E-B1, E-B2, E-B3, E-B12): the S6/S7 consumer round cap is `acceptance_rounds` in the stage row, read by ONE function
    (`runtime_policy.repair_cap`); S4/S5 keep today's caps; a malformed row is ignored; a person's words lift the row; the status
    line reads the same reader (the line never shows a cap the controller does not apply)."""
    import acceptance
    import runtime_policy as RP
    import stage_status as SS

    def cap(stage, role, **kw):
        return RP.repair_cap(role, acceptance.stage_def_of(stage), **kw)

    rows = [("C1 s6-runner-cap-is-1", cap("S6", "qa-runner"), 1),
            ("C2 s7-analyst-cap-is-1", cap("S7", "qa-failure-analyst"), 1),
            ("C3 s5-automator-cap-unchanged", cap("S5", "qa-automator"), RP.DEFAULT_LIMITS["repair_cycles"]),
            ("C4 s4-designer-cap-unchanged", cap("S4", "qa-case-designer"), RP.DEFAULT_LIMITS["design_repair_cycles"]),
            ("C6 person-words-lift-the-row", cap("S6", "qa-runner", person_words=True), RP.DEFAULT_LIMITS["repair_cycles"]),
            ("C1 a project's limits do not lift the row", cap("S6", "qa-runner", limits={"repair_cycles": 5}), 1),
            ("C1 the status line reads the one reader (S6)", SS.round_cap(None, "qa-runner", "S6"), 1),
            ("C1 the status line reads the one reader (S7)", SS.round_cap(None, "qa-failure-analyst", "S7"), 1),
            ("C1 an unknown stage reads today's value", SS.round_cap(None, "qa-runner", "S99"), RP.DEFAULT_LIMITS["repair_cycles"]),
            ("C1 an empty stage reads today's value", SS.round_cap(None, "qa-runner", ""), RP.DEFAULT_LIMITS["repair_cycles"]),
            ("C1 not the stage's author: today's value", RP.repair_cap("qa-code-critic", {"roles": ["qa-runner"], "acceptance_rounds": 1}),
             RP.DEFAULT_LIMITS["repair_cycles"])]
    for label, got, want in rows:
        eq(label, got, want)
    for bad in ("x", -1, True, None, 1.5):             # C5: malformed or absent -> ignored, today's cap
        eq(f"C5 malformed-row-ignored: {bad!r}",
           RP.repair_cap("qa-runner", {"roles": ["qa-runner"], "acceptance_rounds": bad}), RP.DEFAULT_LIMITS["repair_cycles"])
    eq("C5 malformed-row-ignored: key absent", RP.repair_cap("qa-runner", {"roles": ["qa-runner"]}), RP.DEFAULT_LIMITS["repair_cycles"])
    eq("C5 malformed-row-ignored: no row", RP.repair_cap("qa-runner", None), RP.DEFAULT_LIMITS["repair_cycles"])
    eq("C5 a zero is a cap", RP.repair_cap("qa-runner", {"roles": ["qa-runner"], "acceptance_rounds": 0}), 0)


def test_consumer_gap_road() -> None:
    """SC-B2 rows G1-G10 (B2-3, B2-4, B2-5): a consumer-judged stage (S6 by the analyst, S7 by the scribe) gets one repair round and is never
    a barrier - a spent / unreadable / uncountable / unregistrable round is accepted by the driver WITH A GAP (record first, then the
    warning), the consumer's OWN completion goes on, and the seam is never asked. One table of cases for both stages."""
    import acceptance as A
    import brief_pack
    import gate_brief
    from driver_core import GAP_PREFIX, OpenWork, Refusal, ReworkRefused
    root, task_root, env = seed("QA-9")
    try:
        for stage in ("S6", "S7"):
            driver = driver_for(root, env, "QA-9")
            author, who = A.stage_def_of(stage)["roles"][0], driver.CONSUMER_ROUTES[stage]["who"]
            tip, judge = f"{stage}-{author}-1", f"X-{stage}-1"
            dispatches = {tip: {"id": tip, "stage": stage, "role": author, "status": "accepted"}}
            pipeline, calls, seam, ran, counts = {"ticket": "QA-9"}, [], [], [], [(1, 1)]
            driver.controller_state = lambda: {"stages": {stage: {"status": "pending"}}, "dispatches": dispatches}
            driver.pipeline = lambda: pipeline
            driver.stage_review_exhausted = lambda *a, **k: seam.append(a) or "SEAM"
            driver.stage_verdict_known = lambda form: True
            driver.consumer_counts = lambda *a: counts[0]
            driver.consumer_person_pass = lambda *a, **k: False
            driver.rework = lambda *a, **k: ran.append(k) or None
            driver.last_dispatch = judge

            def write(st, dispatch, word="reject", quote="the run report has no row"):
                pipeline.setdefault("acceptance", {}).setdefault(st, []).append(
                    {"stage": st, "acceptor": A.consumer_of(st), "reviewed_dispatch": tip, "verdict": word, "quote": quote})

            def py(script, *args, **kw):
                at = lambda key: args[args.index(key) + 1]
                calls.append("record" if "--acceptor" in args else "warn")
                if "--acceptor" in args:
                    pipeline.setdefault("acceptance", {}).setdefault(stage, []).append(
                        {"stage": stage, "acceptor": at("--acceptor"), "reviewed_dispatch": tip, "verdict": "accept", "quote": at("--quote")})
                    assert at("--acceptance") == f"work/handoffs/{tip}.yaml", args
                else:
                    pipeline.setdefault("warnings", []).append(at("--warn"))
                return 0, ""
            driver.py, driver.stage_acceptance_write = py, write

            def finish(label, word="reject", quote="the run report has no row", counted=(1, 1), known=True, refuse="", inner="INNER", step=""):
                pipeline.pop("acceptance", None), pipeline.pop("warnings", None), calls.clear(), seam.clear(), ran.clear()
                counts[0], driver.stage_verdict_known = counted, lambda form: known

                def written(st, dispatch):
                    if refuse:
                        refusal = Refusal(refuse)
                        refusal.step = step
                        raise refusal
                    write(st, dispatch, word, quote)
                driver.stage_acceptance_write = written
                out = driver.consumer_completion(stage, inner)("digest")
                check_eq(f"{stage} {label}: the seam is never asked", seam, [])
                return out, (pipeline.get("acceptance") or {}).get(stage, [])[-1:], pipeline.get("warnings") or [], list(calls)
            words = lambda why: f"{stage} was accepted with a gap: {why}"
            spent = f"the one repair round of the {author} is spent"
            out, rec, warns, order = finish("G1 accept-unchanged", word="accept", counted=(0, 1))
            check_eq(f"{stage} G1: an accept is the consumer's own completion, no gap record, no warning", (out, order, warns), ("INNER", [], []))
            out, rec, warns, order = finish("G2 reject-round-left-reworks-once", counted=(0, 1))
            check_eq(f"{stage} G2: a reject with a round left sends the stale work back, no gap", (type(out).__name__, out.unresolved, order), ("OpenWork", A.SUPERSEDED_WORD, []))
            out, rec, warns, order = finish("G3 reject-no-round-gap-own-completion", counted=(1, 1))
            check_eq(f"{stage} G3: the driver's accept with a gap quote, then the warning, then the consumer's own completion",
                     (out, rec[0]["acceptor"], rec[0]["verdict"], rec[0]["quote"], warns, order),
                     ("INNER", A.DRIVER_ACCEPTOR, "accept", f"{GAP_PREFIX} {spent}: the run report has no row", [words(spent)], ["record", "warn"]))
            check_eq(f"{stage} G3b gap-own-open-work-passes-through: open work of the stage's own rule is returned as it is",
                     type(finish("G3b", inner=OpenWork("repairs_pending", "rows remain"))[0]).__name__, "OpenWork")
            for label, kw, why, quote in (
                    ("G4 unreadable-word-gap", dict(known=False), f"the {who}'s verdict word could not be read", "(no quote)"),
                    ("G4 form-refused-gap", dict(refuse="the form lacks its quote"), f"the {who}'s acceptance form was refused: the form lacks its quote", "(no quote)"),
                    ("G5 uncountable-gap-no-round", dict(counted=(None, None)), f"the repair rounds of the {author} could not be counted",
                     "the run report has no row"),
                    ("G7 temporal-round-2-of-1-gap", dict(counted=(2, 1)), spent, "the run report has no row"),
                    ("E-B9 long quote cut at 400", dict(quote="q" * 500), spent, "q" * 400 + "...")):
                out, rec, warns, order = finish(label, **kw)
                check_eq(f"{stage} {label}: gap record, then the warning; no round is started; the consumer's own completion",
                         (out, rec[0]["quote"], warns, order, ran), ("INNER", f"{GAP_PREFIX} {why}: {quote}", [words(why)], ["record", "warn"], []))
            # G4c (F4): a refusal of the consumer's questions to the person propagates; no gap record, no warning
            try:
                finish("G4c questions-refused", refuse="the question has no title", step="questions")
                raised = False
            except Refusal:
                raised = True
            check_eq(f"{stage} G4c: a refused question raise is a Refusal, never a gap", (raised, pipeline.get("acceptance"), pipeline.get("warnings"), calls), (True, None, None, []))
            # G8b (F3): a person's word that stands before the verdict is never overwritten by a gap (the finish road)
            driver.consumer_person_pass = lambda *a, **k: True
            out, rec, warns, order = finish("G8b person-pass-beats-gap", counted=(1, 1))
            driver.consumer_person_pass = lambda *a, **k: False
            check_eq(f"{stage} G8b: no gap record, no warning, the consumer's own completion", (out, order, warns), ("INNER", [], []))
            # G10: no author run to judge -> no record, no warning, the consumer goes on
            dispatches.clear()
            out, rec, warns, order = finish("G10 no-author-no-record", known=False)
            check_eq(f"{stage} G10: no author dispatch -> no record, no warning, own completion", (out, rec, warns, order), ("INNER", [], [], []))
            dispatches[tip] = {"id": tip, "stage": stage, "role": author, "status": "accepted"}
            # the settle road (restart recovery): G8 person-pass-wins, G9 rework-refused-gap, a round left reworks once, spent -> gap
            for label, counted, person, refused, want in (("G8 person-pass-wins", (1, 1), True, False, ([], [], [])),
                                                          ("G9 rework-refused-gap", (0, 1), False, True, (["record", "warn"], [], [1])),
                                                          ("G2 settled round left", (0, 1), False, False, ([], [], [1])),
                                                          ("G3 settled spent", (1, 1), False, False, (["record", "warn"], [], []))):
                pipeline.pop("acceptance", None), pipeline.pop("warnings", None), calls.clear(), seam.clear(), ran.clear()
                write(stage, tip)
                counts[0], driver.consumer_person_pass = counted, lambda *a, p=person, **k: p
                driver.rework = (lambda *a, **k: ran.append(1) or (_ for _ in ()).throw(ReworkRefused("the controller will not register a round"))) \
                    if refused else (lambda *a, **k: ran.append(1) or None)
                done = driver.consumer_settled(stage, driver.controller_state(), tip, True, ran=True)
                check_eq(f"{stage} {label}: (calls, seam, rounds started) and the entry's result", (calls, seam, ran, done), (*want, False if person else True))
                if refused:
                    check_in(f"{stage} {label}: the refusal text is in the gap quote", "could not be started: the controller will not register a round",
                             pipeline["acceptance"][stage][-1]["quote"])
            # G4 settled form-refused (F5, P31): the finish died after the consumer's dispatch; its form is refused -> the gap road, True
            route = driver.CONSUMER_ROUTES[stage]
            dispatches[judge] = {"id": judge, "stage": route["consumer_stage"], "role": A.consumer_of(stage), "status": "accepted"}
            pipeline.pop("acceptance", None), pipeline.pop("warnings", None), calls.clear(), seam.clear(), ran.clear()

            def refused_form(st, dispatch):
                raise Refusal("the form lacks its quote")
            driver.stage_acceptance_write, driver.stage_verdict_known = refused_form, lambda form: True
            done = driver.consumer_settled(stage, driver.controller_state(), tip, True, ran=True)
            check_eq(f"{stage} G4 settled form-refused: gap record, then the warning; no seam; the entry is done",
                     (done, calls, seam, ran, [w for w in pipeline.get("warnings") or []]),
                     (True, ["record", "warn"], [], [], [words(f"the {who}'s acceptance form was refused: the form lacks its quote")]))
            driver.stage_acceptance_write = write
            del dispatches[judge]
            pipeline.pop("acceptance", None), pipeline.pop("warnings", None)
            finish("G6 close words", counted=(1, 1))
            check_eq(f"{stage} G6 close-words-say-gap", driver.consumer_close_words(stage),
                     (f"accepted with a gap: {GAP_PREFIX} {spent}: the run report has no row", "accepted with a gap"))
            pipeline["acceptance"][stage][-1]["quote"] = f"by: person - {GAP_PREFIX} said so"
            check_eq(f"{stage} G8 a person's pass is never read as a gap", driver.consumer_close_words(stage)[1], "accepted by a person's word")
            # the round line (B2-2): told before the work; a round left / none left / uncounted
            for counted, head in (((0, 1), f"Your return is the one chance the {author} has to redo this (0 of 1 used)"),
                                  ((1, 1), "No return is left for this handoff: do your own work"),
                                  ((None, None), "No return is left for this handoff: the rounds could not be counted: do your own work")):
                counts[0] = counted
                check_eq(f"{stage} round line {counted}", driver.consumer_round_line(stage, tip).startswith(head), True)
        # G6: the S6 gap reaches the scribe's brief as a `standing:` line; the S7 warning reaches the packet gate_brief reads (`collect`)
        line = "S6 was accepted with a gap: the one repair round of the qa-runner is spent"
        shown = brief_pack.decisions({"warnings": [line]}, "S8", "qa-doc-scribe")[0]
        check_eq("S6 G6 scribe-brief-standing-gap-line", [s for s in shown if "- standing: " + line in str(s)] != [], True)
        packet = Path(root) / "qa-factory" / "artifacts" / "QA-9"
        packet.mkdir(parents=True, exist_ok=True)
        (packet / "pipeline.json").write_text(json.dumps({"ticket": "QA-9", "stages": {}, "warnings": [line.replace("S6", "S7")]}), encoding="utf-8")
        check_in("S7 G6c s7-gap-after-scribe-brief-reaches-gate-b", "S7 was accepted with a gap", gate_brief.render_gate_b("QA-9", packet))
        (packet / "pipeline.json").write_text(json.dumps({"ticket": "QA-9", "stages": {}}), encoding="utf-8")
        check_not_in("S7 G6c no warnings, no block at gate B", "Warnings the factory is carrying", gate_brief.render_gate_b("QA-9", packet))
    finally:
        harness.cleanup(root)


def main() -> None:
    run_scenarios([], [
        test_consumer_round_cap_is_data,
        test_consumer_gap_road,
        hf2_11b_s6_freshness_reads_the_run_rows_shas,
        hf2_11b_stale_live_checks_are_proved_again_before_the_reduction,
        hf2_11b_the_tool_takes_only_a_running_dispatch,
        hf2_11b_stale_runs_go_to_the_runner_and_the_proofs_follow,
        hf2_11b_without_a_stand_nothing_is_run_or_proved,
        fv3_21_the_stand_word_reaches_the_manual_half,
        hf2_11b_nothing_stale_is_byte_identical,
        hf2_11b_forty_tests_changed_by_one_fixture,
    ])
    harness.finish("test_story_run_s6_hf2_11b")


# split: runner piece 1
if __name__ == "__main__":
    main()
