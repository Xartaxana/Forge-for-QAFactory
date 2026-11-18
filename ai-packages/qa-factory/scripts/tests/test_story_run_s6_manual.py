"""manual: a part of test_story_run_s6.py, split by tools/test_split.py (TD-11c). The shared helpers are in story_run_s6_common."""
import json
import sys
import types
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness  # noqa: E402
import story_run_common  # noqa: E402
del story_run_common  # split: imported for its sys.path effect
from story_run_common import run_scenarios, D1Evidence, D1_SAME, check, check_eq, check_in, check_not_in, d1_answer, d1_driver, d1_write_blocks, d2_seed, driver_for, eq, seed
from story_run_s6_common import AWAITS, enter_manual, manual_rig  # noqa: E402


def t261_k2_the_blocks_of_five_and_the_refused_are_not_dispatched() -> None:
    """K2: 7 accepted + 4 refused -> blocks [5, 2] and 4 `not checked` lines; 5 -> [5]; 6 -> [5, 1]; 11 -> [5, 5, 1]; and
    the position/stage rules: ONE dispatch per entry, only the LAST block completes (and only when nothing was refused,
    because the controller refuses a completion over a case no accepted dispatch carried); no block left -> the manual
    half closes with no runner (finalize, then the code-only receipt, then stage_done)."""
    import story_run
    task = "QA-9"
    root, task_root, env = d2_seed(task, environment="Local", pending=False)
    try:
        names = lambda n, tag="TC": [f"QA-9_{tag}_{i:03d}" for i in range(1, n + 1)]
        driver, world, launched, moves = manual_rig(root, env, task, [])
        for ready_n, expected in ((0, []), (1, [1]), (4, [4]), (5, [5]), (6, [5, 1]), (10, [5, 5]), (11, [5, 5, 1]), (12, [5, 5, 2])):
            cases = names(ready_n)
            plan = driver.manual_plan(cases)
            check_eq(f"blocks of {ready_n} prepared cases: {expected}", [len(b) for b in plan["blocks"]], expected)
            check_eq(f"{ready_n} prepared cases: the cases are in the given (plan-row) order, none lost",
                     [c for b in plan["blocks"] for c in b], cases)
        # K2 as stated: 7 accepted + 4 refused
        ready, bad = names(7), names(4, "BAD")
        scope = [c for pair in zip(ready[:4], bad) for c in pair] + ready[4:]       # refused cases between the others
        driver, world, launched, moves = manual_rig(root, env, task, scope, refused=bad)
        plan = driver.manual_plan(scope)
        check_eq("K2: 7 accepted + 4 refused -> blocks [5, 2]", [len(b) for b in plan["blocks"]], [5, 2])
        check_eq("K2: and the four refused are named, each with its words", [c for c, _w in plan["refused"]], bad)
        # entry 1: the first block only, and it does NOT complete the stage (a second block and refused cases follow)
        text, first = enter_manual(driver, world, scope)
        check_eq("entry 1: exactly one dispatch, scope the first five prepared cases, in order",
                 [(e["role"], e["scope"], e["complete"]) for e in launched], [("qa-runner", ready[:5], False)])
        check_eq("entry 1: the dispatch is registered as a manual block of those five (the controller's own field)",
                 (world.dispatches[first]["execution_kind"], world.dispatches[first]["manual_case_ids"]), ("manual", ready[:5]))
        check_eq("K2: four `not checked` lines, one per refused case", len([ln for ln in text.splitlines() if "not checked by hand" in ln]), 4)
        for case in bad:
            check_in(f"the line names {case} and its refusal", f"S6: {case}: not checked by hand — the check could not be taken", text)
        check_in("the runner is told the prepared request of each case of the block, by path",
                 f"work/evidence/manual/{ready[0]}/request.json", " ".join(launched[0]["extra"]))
        # entry 2: the second block (two cases) - still not closing: the refused cases are outside any dispatch's cover
        text, second = enter_manual(driver, world, scope)
        check_eq("entry 2: one more dispatch, the two left, `--not-complete` because four were refused",
                 [(e["scope"], e["complete"]) for e in launched[1:]], [(ready[5:], AWAITS)])         # X7-6c: the last block awaits the consumer
        check_eq("entry 2: and the four lines are said again (each entry is a fresh reading of the plan)",
                 len([ln for ln in text.splitlines() if "not checked by hand" in ln]), 4)
        check_eq("no finalize and no receipt yet", moves, [])
        # entry 3: nothing left to dispatch: the manual half closes with no runner
        text, third = enter_manual(driver, world, scope)
        check_eq("entry 3: no new dispatch and no role call", (third, len(launched)), ("", 2))
        check_eq("entry 3: the reduction FIRST, then the code-only receipt, then the close",
                 [m[0] for m in moves], ["finalize", "code_only", "stage_done"])
        check_eq("the receipt names the stage and the evidence: the run report and each refused case's request",
                 (moves[1][1], moves[1][3]) if len(moves) > 1 else None,
                 ("S6", ["work/run-report.json"] + [f"work/evidence/manual/{c}/request.json" for c in bad]))
        check_in("and says how many were checked and which were not", "7 case(s) checked by an agent by hand, 4 not checked: " + ", ".join(bad),
                 moves[1][2] if len(moves) > 1 else "")
        # a refused case is NEVER in any dispatch scope (the mutation: a refused case dispatched anyway)
        check_eq("no refused case appears in any dispatch scope",
                 [c for e in launched for c in e["scope"] if c in bad], [])
        # 5 -> one block that closes the stage; 6 -> [5] then [1] that closes it; 11 -> [5] [5] [1]
        for n, flags in ((5, [AWAITS]), (6, [False, AWAITS]), (11, [False, False, AWAITS])):         # X7-6c: the LAST block awaits the consumer
            driver, world, launched, moves = manual_rig(root, env, task, [])
            cases = names(n)
            for _ in flags:
                enter_manual(driver, world, cases)
            check_eq(f"{n} prepared cases, none refused: the blocks' `complete` flags (only the LAST block closes S6)",
                     [e["complete"] for e in launched], flags)
            check_eq(f"{n} prepared cases: the dispatches' scopes are the blocks, in order",
                     [len(e["scope"]) for e in launched], {5: [5], 6: [5, 1], 11: [5, 5, 1]}[n])
            check_eq(f"{n} prepared cases: nothing is closed by code (the last runner closes it)", moves, [])
        # 0 prepared: no runner, the manual half closes with the lines
        bad = names(3, "BAD")
        driver, world, launched, moves = manual_rig(root, env, task, bad, refused=bad)
        text, new = enter_manual(driver, world, bad)
        check_eq("0 accepted: no runner, no dispatch", (launched, new), ([], ""))
        check_eq("0 accepted: the three lines, then the manual half closes code-only",
                 (len([ln for ln in text.splitlines() if "not checked by hand" in ln]), [m[0] for m in moves]),
                 (3, ["finalize", "code_only", "stage_done"]))
        # the reduction fails: nothing is closed over a report nobody could build
        driver, world, launched, moves = manual_rig(root, env, task, bad, refused=bad)
        real = driver.py
        driver.py = lambda script, *a, **k: (1, "boom: corrupt run block") if script == "finalize_task.py" else real(script, *a, **k)
        try:
            enter_manual(driver, world, bad)
            check("a failing reduction is a refusal", False)
        except story_run.Refusal as refusal:
            check_in("a failing reduction is a refusal that names it", "finalize_task.py exit 1", refusal.text)
        check_eq("...and no receipt was written", [m for m in moves if m[0] != "finalize"], [])
    finally:
        harness.cleanup(root)


def test_manual_block_dispatches_unprepared() -> None:
    """F5(c) (t-1936 N5, B-15; SLOW, CI judges): a case the FACTORY failed to prepare is dispatched in the same block as the
    prepared ones (the factory never stands), the runner is told its reason in one line that forbids a result, and the driver
    prints it; a case the STORY refuses stays out of every scope. Control: a prepared case gets no such line."""
    task = "QA-9"
    root, task_root, env = d2_seed(task, environment="Local", pending=False)
    try:
        ready, walked, refused = f"{task}_TC_001", f"{task}_TC_002", f"{task}_BAD_001"
        reason = "the plan gives TC_002's check an evidence rule that is not one word"
        driver, world, launched, moves = manual_rig(root, env, task, [ready, walked, refused], refused=[refused])
        base = driver.manual_prepare
        driver.manual_prepare = lambda case: ([f"OB-{case}"], "", reason) if case == walked else base(case)
        text, first = enter_manual(driver, world, [ready, walked, refused])
        check_eq("the prepared and the unprepared case share one dispatch; the refused one is outside it",
                 [e["scope"] for e in launched], [[ready, walked]])
        check_in("the driver says the case is walked unprepared, with the reason", f"S6: {walked}: unprepared - {reason}", text)
        lines = [ln for ln in launched[0]["extra"] if "unprepared" in ln]
        check_eq("the runner gets exactly one unprepared line, for the walked case", len(lines), 1)
        check_in("...that names the case and the reason", f"{walked}: unprepared - {reason}", lines[0])
        check_in("...and forbids a result", "record no pass or fail", lines[0])
        check_not_in("the prepared case has no such line", ready + ": unprepared", " ".join(launched[0]["extra"]))
        check_in("the refused case is still named as not checked", f"S6: {refused}: not checked by hand", text)
    finally:
        harness.cleanup(root)


def t261_resume_after_a_crash_between_blocks_and_the_recovery_rule() -> None:
    """C4: the done blocks are the controller's accepted dispatches, so a FRESH driver after a crash dispatches the next
    block and never the first again; a block that crashed (running, never accepted) is judged by `completion_for` on
    recovery with the same rule the dispatch used."""
    task = "QA-9"
    root, task_root, env = d2_seed(task, environment="Local", pending=False)
    try:
        cases = [f"QA-9_TC_{i:03d}" for i in range(1, 12)]
        driver, world, launched, moves = manual_rig(root, env, task, cases)
        enter_manual(driver, world, cases)                              # block 1 accepted
        check_eq("setup: block 1 went", [len(e["scope"]) for e in launched], [5])
        fresh, _w, launched2, moves2 = manual_rig(root, env, task, cases, world=world)     # a relaunch: new driver, same controller
        enter_manual(fresh, world, cases)
        check_eq("after the crash the NEXT block goes (cases 6-10), not block 1 again",
                 [e["scope"] for e in launched2], [cases[5:10]])
        check_eq("...and it does not close the stage (one more block is left)", [e["complete"] for e in launched2], [False])
        # a crash INSIDE a block: registered, never accepted -> not done; the recovery path asks completion_for
        crashed, w2, l3, m3 = manual_rig(root, env, task, cases)
        enter_manual(crashed, w2, cases, accept=False)
        running = next(iter(w2.dispatches.values()))
        check_eq("setup: the crashed block is `running`, so it is not done", (running["status"], crashed.manual_done()), ("running", set()))
        # completion_for on recovery, with the scope and the preparation replaced
        def completion(record, scope, refused=(), done=()):
            d, w, _l, _m = manual_rig(root, env, task, scope, refused=refused)
            for i, ids in enumerate(done, 1):
                w.dispatches[f"S6-qa-runner-{i}"] = {"stage": "S6", "status": "accepted", "execution_kind": "manual", "manual_case_ids": ids}
            d.stage_scope = lambda stage, kind="": {"scope": list(scope)}
            return d.completion_for("S6", "qa-runner", record)
        last = {"execution_kind": "manual", "manual_case_ids": cases[10:], "scope": cases[10:]}
        check_eq("recovery: the LAST block (nothing else left) closes the stage", completion(last, cases, done=[cases[:5], cases[5:10]]), AWAITS)         # X7-6c: the closing window awaits the consumer
        check_eq("recovery: a block with another still to go does not", completion(dict(last, manual_case_ids=cases[5:10], scope=cases[5:10]), cases, done=[cases[:5]]), False)
        check_eq("recovery: the last block awaits the consumer though a case was refused (X7-6; manual_close closes the refused case later)",
                 completion(last, cases, refused=[cases[0]], done=[cases[1:5], cases[5:10]]), AWAITS)
        auto = {"execution_kind": "automation", "scope": ["QA-9_TC_900"]}
        check_eq("recovery: the AUTOMATION runner does not close S6 while a manual half is left", completion(auto, cases), False)
        check_eq("recovery: ...and does when there is none", completion(auto, []), AWAITS)         # X7-6c
        d, w, _l, _m = manual_rig(root, env, task, cases)
        d.stage_scope = lambda *a, **k: (_ for _ in ()).throw(RuntimeError("controller down"))
        check_eq("recovery: a scope that cannot be read closes nothing (a doubt never closes a stage)",
                 d.completion_for("S6", "qa-runner", last), False)
        check_eq("recovery: another stage's roles keep their own rule (a scout is the default)",
                 d.completion_for("S1", "qa-scout", {}), None)
    finally:
        harness.cleanup(root)


def t261_the_real_controller_refuses_a_completion_over_an_undispatched_case_and_takes_the_code_only_receipt() -> None:
    """The premise of C4 against the REAL controller (the helpers of test_fixes_13797.py, F5): a runner dispatch that
    would complete S6 while a manual-agent case of the derived scope was never dispatched (a case `prepare` refused) is
    refused - which is why the driver sends the last block `--not-complete` when anything was refused - and the code-only
    receipt (`finalize_task`, then `code_only`, then `stage_done`: what `manual_close` writes) closes S6 over that case."""
    import test_fixes_13797 as F
    root = harness.temp_dir("qa-t261-controller-")
    try:
        c = F.s6_story(root)
        refused = F.runner(c, root, "S6-auto", "automation", ["TC-1"], True)
        check_in("a completion over a derived manual case nobody dispatched is refused by the controller (C4's premise)",
                 "manual-agent case TC-2 has no accepted S6 dispatch", refused)
        check_eq("...and S6 stays open", c.state()["stages"]["S6"]["status"], "running")
        check_eq("the same acceptance with `--not-complete` goes through", F.runner(c, root, "S6-auto", "automation", ["TC-1"], False), "")
        evidence = F.BASE.evidence_ref(root, "run-report.json", "{}")
        c.apply("code_only", {"id": "S6-code-only-1", "stage": "S6", "reason": "the manual half of S6: 0 case(s) checked, 1 not checked: TC-2",
                              "evidence_refs": [evidence], "expected_revision": c.state().get("revision", 0),
                              "idempotency_key": "code_only:S6:1"})
        check_eq("the code-only receipt closes S6 with TC-2 never dispatched",
                 (c.state()["stages"]["S6"]["status"], c.state()["stages"]["S6"].get("code_only")), ("completed", True))
    finally:
        harness.cleanup(root)
    # FV3-21 K6 (T-RC): the awaiting marker `consumer_need_record` writes at `manual_close` holds against the REAL controller: an accepted
    # not-complete automation author with no record awaits nothing until the marker stands; then `next` names S7 and the analyst is let in
    import acceptance
    root2 = harness.temp_dir("qa-t261-await-")
    try:
        c2 = F.s6_story(root2)
        eq("T-RC the runner is accepted not-complete", F.runner(c2, root2, "S6-auto", "automation", ["TC-1"], False), "")
        path = root2 / "pipeline.json"
        pipeline = json.loads(path.read_text(encoding="utf-8-sig")) if path.is_file() else {}
        eq("T-RC control: with no marker nothing awaits (today the story stops)", acceptance.awaits_acceptance(c2.state(), "S6", pipeline), "")
        path.write_text(json.dumps(dict(pipeline, acceptance_awaits={"S6": "S6-auto"})), encoding="utf-8")
        pipeline = json.loads(path.read_text(encoding="utf-8-sig"))
        eq("T-RC the marker makes S6 await the consumer", acceptance.awaits_acceptance(c2.state(), "S6", pipeline), "S6-auto")
        eq("T-RC `next` names S7", c2.next_action().get("stage"), "S7")
        analyst = {"id": "S7-qa-failure-analyst-1", "stage": "S7", "role": "qa-failure-analyst", "scope": ["TC-1"], "input_hash": "s7",
                   "budget": {}, "known_paths": {}, "idempotency_key": "d-an1"}
        eq("T-RC control: the doc scribe is NOT let in while S6 awaits the analyst",
           "required prior logical stage incomplete" in F.refused(c2.apply, "dispatch", dict(analyst, id="S7-qa-doc-scribe-1", role="qa-doc-scribe",
                                                                                              idempotency_key="d-sc1")), True)
        eq("T-RC the failure analyst's dispatch is admitted", F.refused(c2.apply, "dispatch", analyst), "")
    finally:
        harness.cleanup(root2)


def t261_prepare_by_code_on_the_cmp2_shape_and_the_temporal_door() -> None:
    """The real `manual_evidence.prepare` over the cmp2-shaped task (scaffold of test_manual_capture): a plan approved
    BEFORE the pass keeps `decision: new`, so every case is refused - naming a door the driver can use (FR-57: the case
    stands as not checked, or gate A is approved again); once the pass has run, TS-7 and TS-12 are prepared and TC_015
    (R-19, implementation-only) is still refused as an unconfirmed expectation (C2) - the free negative control."""
    sys.path.insert(0, str(Path(__file__).resolve().parent / "fixtures" / "manual-evidence"))
    import scaffold as S
    import planning_contract as PC
    import story_run
    import manual_evidence as ME
    t = S.make_task(manual=())
    try:
        harness.use_project(t.project)
        shim = types.SimpleNamespace(task_root=t.task)
        manual = [S.CASES["ui"], S.CASES["api"], S.CASES["impl"]]
        words = "\n".join(f"{c}: manual" for c in manual[1:])          # TS-7 is a manual-agent row already; 12 and 15 are the person's words
        # before: the plan as cmp2 approved it - TS-7 is a manual-agent row whose obligation still says `new`
        with t.patched():
            ids, why, _walk = story_run.Driver.manual_prepare(shim, S.CASES["ui"])
        check_eq("temporal: a plan approved before the pass: TC_007 is refused, with no obligation id", (ids, bool(why)), ([], True))
        check_in("...naming what is wrong in words", "the approved plan still has this check as `new`", why)
        check_in("...and a door the driver can use (FR-57): gate A again, or the case stands as not checked", "stands as not checked by hand", why)
        check_in("...and the orchestrator's operation", "semantic_reopen", why)
        written = json.loads(ME.request_path(t.task, S.CASES["ui"]).read_text(encoding="utf-8"))
        check_eq("the refusal is on disk for the report: {refused: {reason, door}} and nothing else",
                 (sorted(written), sorted(written["refused"])), (["refused"], ["door", "reason"]))
        # after: gate A applied the pass (the person said `<TC_012>: manual`, `<TC_015>: manual`)
        PC.apply_gate_answers(t.task, words)
        with t.patched():
            ui = story_run.Driver.manual_prepare(shim, S.CASES["ui"])
            api = story_run.Driver.manual_prepare(shim, S.CASES["api"])
            impl = story_run.Driver.manual_prepare(shim, S.CASES["impl"])
        check_eq("after the pass: TC_007 is prepared (OB-7)", ui, (["OB-7"], "", ""))
        check_eq("after the pass: TC_012 is prepared (OB-12, policy api)", api, (["OB-12"], "", ""))
        check_eq("C2: TC_015 is refused, no obligation id", impl[0], [])
        check_in("C2: as an unconfirmed expectation", "expectation unconfirmed", impl[1])
        check("the prepared case's request.json is the request, the refused one's is the refusal",
              "refused" not in json.loads(ME.request_path(t.task, S.CASES["ui"]).read_text(encoding="utf-8"))
              and "refused" in json.loads(ME.request_path(t.task, S.CASES["impl"]).read_text(encoding="utf-8")))
        # plan-row order: the scope is given in another order; the plan's rows decide (TS-7, TS-12, TS-15)
        check_eq("plan-row order, whatever order the scope names the cases in",
                 story_run.Driver.manual_order(shim, [S.CASES["impl"], S.CASES["api"], S.CASES["ui"]]), manual)
        # an unexpected failure is a refusal too, written for the report - never a dispatch on a doubt
        real = ME.prepare_to_file
        ME.prepare_to_file = lambda *a, **k: (_ for _ in ()).throw(OSError("disk full"))
        try:
            ids, why, _walk = story_run.Driver.manual_prepare(shim, S.CASES["ui"])
        finally:
            ME.prepare_to_file = real
        check_eq("an unexpected failure of prepare: refused (no ids), the failure named", (ids, "OSError: disk full" in why), ([], True))
        check_in("...and written where the report reads it", "OSError: disk full",
                 json.loads(ME.request_path(t.task, S.CASES["ui"]).read_text(encoding="utf-8"))["refused"]["reason"])
    finally:
        S.cleanup(t)


def t289_real_story(root, manual_n):
    """A story in the NEW plan-contract mode through gate A and S5: TC-1 is automated, TC-2..TC-(manual_n+1) are
    manual-agent rows (the shape of `test_fixes_13797.s6_story`, with more manual cases). Returns the real controller."""
    import test_fixes_13797 as F
    import test_controller_state as BASE
    import test_controller_rework_scope as SCOPED
    from controller import Controller
    cases = [f"TC-{i}" for i in range(1, manual_n + 2)]
    (root / "qa-factory").mkdir(parents=True, exist_ok=True)
    (root / "qa-factory" / "config.json").write_text("{}", encoding="utf-8")
    c = Controller(root)
    c.apply("initialize", {"scope": cases, "source_revision": "src-1", "known_paths": {"root": str(root)}, "idempotency_key": "init"})
    for number in range(5):
        BASE.accept_stage(c, root, f"S{number}")
    BASE.seed_plan(root, [SCOPED.plan_row(1, "automate")] + [SCOPED.plan_row(i, "manual-agent") for i in range(2, len(cases) + 1)])
    (root / "state" / "story-case-links.json").write_text(json.dumps({"links": [
        {"case_id": case, "version": f"cv_{i}"} for i, case in enumerate(cases, 1)]}), encoding="utf-8")
    decision = {"id": "gate-a", "gate": "A", "action": "approve", "status": "approved", "authorization_source": "human",
                "source_revision": "src-1", "scope": cases, "input_revision": "src-1", "idempotency_key": "gate-a"}
    c.apply("decision", BASE.bind_gate_a(root, decision))
    BASE.accept_stage(c, root, "S5")
    return c, F


def t289_manual_block_goes_through_the_real_prepare_and_a_refusal_is_a_text() -> None:
    """t-289 (live S6 rehearsal, cmp2r): in `plan_contract_mode: new` the REAL `controller.prepare` demands the
    `execution_kind` of a qa-runner packet and validates a manual block, and the driver added both only after `prepare`:
    it died with a ValueError and a traceback. Here no fake controller stands in: K-PREP (the packet is prepared with the
    kind and the block, the dispatch is registered with them), K-RES (a second block after the first is accepted goes as
    the NEXT dispatch, the first never again; no block left -> the manual half closes), and a block the controller
    refuses is the driver's own `Refusal`, never a traceback."""
    import contextlib
    import io
    from unittest import mock
    import story_run
    task = "QA-9"
    root, task_root, env = d2_seed(task, environment="Local", pending=False)
    ctl_root = harness.temp_dir("qa-t289-controller-")
    try:
        c, F = t289_real_story(ctl_root, 6)
        manual = [f"TC-{i}" for i in range(2, 8)]
        check_eq("setup: the story is in the NEW plan-contract mode (the premise of the failure)", c.state().get("plan_contract_mode"), "new")
        # the premise, against the real controller: without the kind `prepare` itself refuses (the mutation's own symptom)
        try:
            c.prepare({"stage": "S6", "role": "qa-runner", "id": "probe", "scope": manual[:2]})
            check("the real prepare refuses a qa-runner packet with no execution_kind", False)
        except ValueError as exc:
            check_in("the real prepare refuses a qa-runner packet with no execution_kind", "requires execution_kind", str(exc))
        check_eq("setup: the automation half is accepted first (as in the rehearsal), not closing the stage",
                 F.runner(c, ctl_root, "S6-qa-runner-1", "automation", ["TC-1"], False), "")

        def rig(size=2):
            driver, world, launched, moves = manual_rig(root, env, task, manual)
            driver.controller_state = lambda: c.state()           # the REAL dispatch table: what is accepted is what is done
            driver.MANUAL_BLOCK_MAX = size

            def enter():
                out = io.StringIO()
                with mock.patch("controller.Controller", lambda _root, wait_seconds=0.0: c), contextlib.redirect_stdout(out):
                    driver.run_manual_block(list(manual))
                return out.getvalue()
            return driver, launched, moves, enter

        # K-PREP: the first block of two, through the real prepare and the real apply
        driver, launched, moves, enter = rig()
        text = enter()
        first = c.state()["dispatches"].get("S6-qa-runner-2") or {}
        check_eq("K-PREP: the block is registered by the real controller as a manual block of those two cases",
                 (first.get("execution_kind"), first.get("manual_case_ids"), first.get("scope")), ("manual", manual[:2], manual[:2]))
        check_eq("K-PREP: and the runner is launched on that block, not closing the stage (two blocks follow)",
                 [(e["scope"], e["complete"]) for e in launched], [(manual[:2], False)])
        check_in("K-PREP: the block line is said", "S6: manual block of 2 case(s), 2 more block(s) after it: " + ", ".join(manual[:2]), text)
        # K-RES: the first block is accepted; a FRESH driver goes on with the next block, never the first again
        check_eq("setup: the runner finishes the first block", F.runner(c, ctl_root, "S6-qa-runner-2", "manual", manual[:2], False), "")
        driver, launched, moves, enter = rig()
        enter()
        check_eq("K-RES: the second block is the NEXT dispatch with the next two cases",
                 [(e["scope"], e["complete"]) for e in launched], [(manual[2:4], False)])
        check_eq("K-RES: registered as such", (c.state()["dispatches"]["S6-qa-runner-3"]["manual_case_ids"],
                                               c.state()["dispatches"]["S6-qa-runner-3"]["execution_kind"]), (manual[2:4], "manual"))
        check_eq("setup: the second block is accepted", F.runner(c, ctl_root, "S6-qa-runner-3", "manual", manual[2:4], False), "")
        driver, launched, moves, enter = rig()
        enter()
        check_eq("K-RES: the LAST block closes the stage and is the third manual dispatch",
                 [(e["scope"], e["complete"]) for e in launched], [(manual[4:], AWAITS)])         # X7-6c
        check_eq("setup: the last block is accepted, closing S6", F.runner(c, ctl_root, "S6-qa-runner-4", "manual", manual[4:], True), "")
        check_eq("K-RES: S6 is completed by the accepted dispatches", c.state()["stages"]["S6"]["status"], "completed")
        # a block the CONTROLLER refuses (6 cases > the limit of five) is the driver's Refusal with the controller's words
        fresh_root = harness.temp_dir("qa-t289-controller-b-")
        try:
            c2, F2 = t289_real_story(fresh_root, 6)
            F2.runner(c2, fresh_root, "S6-qa-runner-1", "automation", ["TC-1"], False)
            driver, world, launched, moves = manual_rig(root, env, task, manual)
            driver.controller_state = lambda: c2.state()
            driver.MANUAL_BLOCK_MAX = 6
            try:
                with mock.patch("controller.Controller", lambda _root, wait_seconds=0.0: c2), contextlib.redirect_stdout(io.StringIO()):
                    driver.run_manual_block(list(manual))
                check("a block of six is refused", False)
            except story_run.Refusal as refusal:
                check_in("a block the real controller refuses is the driver's Refusal, in the controller's words",
                         "S6 manual block dispatch refused: ", refusal.text)
                check_in("...naming what it expected", "manual runner block must name 1..5 unique in-scope cases", refusal.text)
            check_eq("...and nothing was registered or launched",
                     (sorted(d for d in c2.state()["dispatches"] if d.startswith("S6-qa-runner-")), launched),
                     (["S6-qa-runner-1"], []))
        finally:
            harness.cleanup(fresh_root)
        # a ValueError out of `prepare` (what the live run met) is the same Refusal, not a traceback
        driver, world, launched, moves = manual_rig(root, env, task, manual)

        class Refusing:
            def __init__(self, task_root, wait_seconds=0.0):
                pass

            def state(self):
                return {"dispatches": {}}

            def prepare(self, options):
                raise ValueError("new-task qa-runner packet requires execution_kind manual or automation")
        try:
            with mock.patch("controller.Controller", Refusing), contextlib.redirect_stdout(io.StringIO()):
                driver.run_manual_block(list(manual[:2]))
            check("a ValueError of prepare is refused", False)
        except story_run.Refusal as refusal:
            check_in("a ValueError of prepare is the Refusal, with its words", "S6 manual block dispatch refused: ValueError: new-task qa-runner packet requires", refusal.text)
        check_eq("...and no role was launched on it", launched, [])
    finally:
        harness.cleanup(ctl_root)
        harness.cleanup(root)


def t289_the_automation_half_with_a_manual_half_pending_finishes_not_complete() -> None:
    """The part of K-ACC that already holds (t-289, cause (B) is NOT here: the refusal of the automation half in the live
    run came from the EXIT GATE of `handoff`, before `finish` - see the report): with a manual half pending `stage_S6` hands
    the automation runner `complete=False`, and `finish` then speaks `story_step finish --not-complete` and nothing else,
    with no conductor and no `--complete`; with no manual half the runner closes the stage as today."""
    import contextlib
    import io
    task = "QA-9"
    root, task_root, env = d2_seed(task, environment="Local", pending=False)
    try:
        d1_write_blocks(task_root)
        for manual, flag in ((("TC-9",), False), ((), AWAITS)):         # X7-6c: with no manual half the final window awaits the consumer
            driver, launched, moves, started = d1_driver(root, env, task, manual=manual)
            two = {"test_a": ("stale", "", D1_SAME), "test_b": ("missing", "", "none")}
            with D1Evidence(d1_answer(two)):
                driver.stage_S6()
            check_eq(f"manual half {'pending' if manual else 'absent'}: the automation runner gets complete={flag}",
                     [e["complete"] for e in launched], [flag])
            check_eq(f"manual half {'pending' if manual else 'absent'}: the next entry is the manual block (or nothing)",
                     started, [])
        calls = []
        driver = driver_for(root, env, task)
        driver.py = lambda script, *a, **k: calls.append((script, [str(x) for x in a])) or (0, "accepted S6-qa-runner-1")
        driver.conductor = lambda *a, **k: calls.append(("conductor", []))
        with contextlib.redirect_stdout(io.StringIO()):
            driver.finish("S6-qa-runner-1", "digest", complete=False, role="qa-runner", stage="S6")
        check_eq("the finish of the automation half is ONE story_step call", [c[0] for c in calls], ["story_step.py"])
        check("...with --not-complete and without --complete", "--not-complete" in calls[0][1] and "--complete" not in calls[0][1])
    finally:
        harness.cleanup(root)


def t261_the_dry_gate_note_and_the_gate_b_text_slot() -> None:
    """(6) a plan with manual rows and no executable obligation says so once; (§4) the gate B packet holds the block
    `report_facts.manual_checks_text` renders, whole and before the ledger - and ONE line when it is not there, fails or
    prints nothing."""
    import io
    import contextlib
    import report_facts
    task = "QA-9"
    root, task_root, env = d2_seed(task, environment="Local", pending=False)
    try:
        driver = driver_for(root, env, task)
        plan = [{"id": "TS-1", "disposition": "manual-agent", "coverage_obligations": [{"obligation_id": "OB-1", "decision": "new"}]},
                {"id": "TS-2", "disposition": "automate", "coverage_obligations": [{"obligation_id": "OB-2", "decision": "new"}]}]
        (task_root / "work" / "test-plan.json").write_text(json.dumps({"rows": plan}), encoding="utf-8")

        import story_run

        def said(d):
            """(printed text, the Person raised or None)."""
            out, person = io.StringIO(), None
            with contextlib.redirect_stdout(out):
                try:
                    d.manual_gate_note()
                except story_run.Person as raised:
                    person = raised
            return out.getvalue(), person
        text, person = said(driver)
        check_in("(6) manual rows and no executable obligation: one line, `gate A was recorded dry;`", "S6: gate A was recorded dry; the plan has 1 row(s)", text)
        # C1-6b FLIPS the pins that were here ("...with a door that exists": `semantic_reopen` in the printed line; "...once" as the
        # whole outcome): the door is now a QUESTION (kind `gate_a_dry`), and no command is named in anything the person reads
        check_eq("(6) FLIPPED: the dry gate A is a Person, kind `gate_a_dry`, at S6", (getattr(person, "kind", None), getattr(person, "stage", None)),
                 ("gate_a_dry", "S6"))
        check_not_in("(6) FLIPPED: no command in the printed line", "semantic_reopen", text)
        check_not_in("(6) FLIPPED: ...nor in the question", "semantic_reopen", getattr(person, "text", ""))
        check_eq("(6) ...the line is said once", text.count("gate A was recorded dry"), 1)
        plan[0]["coverage_obligations"][0]["decision"] = "manual-agent"
        (task_root / "work" / "test-plan.json").write_text(json.dumps({"rows": plan}), encoding="utf-8")
        check_eq("(6) one executable obligation: nothing is said, nothing is asked", said(driver), ("", None))
        plan[0]["disposition"] = "automate"
        (task_root / "work" / "test-plan.json").write_text(json.dumps({"rows": plan}), encoding="utf-8")
        check_eq("(6) no manual row at all: nothing is said, nothing is asked", said(driver), ("", None))
        (task_root / "work" / "test-plan.json").unlink()
        check_eq("(6) no plan: nothing is said, nothing raised", said(driver), ("", None))

        # the gate B text slot; gate_brief / gate_preflight / waiver are not under test
        def packet(d):
            real = d.py
            d.py = lambda script, *a, **k: (0, f"<{script}>") if script in ("gate_brief.py", "gate_preflight.py", "waiver.py") else real(script, *a, **k)
            return d.gate_text("B")
        held = getattr(report_facts, "manual_checks_text", None)
        if held is not None:
            del report_facts.manual_checks_text
        try:
            ledger = task_root / "work" / "ledger.md"
            ledger.write_text("LEDGER-START " + "x" * 13000 + "\n", encoding="utf-8")
            text = packet(driver)
            check_in("§4: the renderer is not installed: ONE line says so", "manual checks: renderer not installed", text)
            check_eq("§4: ...once", text.count("manual checks:"), 1)
            big = "## Checked by hand — 2 of 3\n" + "\n".join(f"- case {i}: " + "word " * 40 for i in range(120)) + "\nBLOCK-END"
            seen = []
            report_facts.manual_checks_text = lambda task_root_: seen.append(task_root_) or big
            text = packet(driver)
            check_in("§4: the renderer's block is in the packet, WHOLE (long as it is, never cut)", big, text)
            check("§4: ...and stands BEFORE the ledger", 0 <= text.find("BLOCK-END") < text.find("LEDGER-START"))
            check_eq("§4: ...rendered for the story's own task folder", [Path(p).resolve() for p in seen], [task_root.resolve()])
            report_facts.manual_checks_text = lambda task_root_: (_ for _ in ()).throw(RuntimeError("the ledger is torn"))
            text = packet(driver)
            check_in("§4: a renderer that fails: one line naming it", "manual checks: could not be shown (RuntimeError: the ledger is torn)", text)
            check_in("§4: ...and the rest of the packet is still there", "LEDGER-START", text)
            for label, value in (("prints nothing", ""), ("prints a number", 7)):
                report_facts.manual_checks_text = lambda task_root_, value=value: value
                check_in(f"§4: a renderer that {label}: one line", "manual checks: the renderer printed nothing", packet(driver))
        finally:
            if held is not None:
                report_facts.manual_checks_text = held
            elif hasattr(report_facts, "manual_checks_text"):
                del report_facts.manual_checks_text
    finally:
        harness.cleanup(root)


def t261_the_integration_lines_of_the_driver() -> None:
    """The lines of t-253 / t-256 that land in story_run.py: the journal read through the layout (both worlds and a
    person's own path), the case ids handed to the answer reader, and `--apply-fixes` also for a Then that says `raise`."""
    import contextlib
    import io
    task = "QA-9"
    # (a) the journal the --no-trace line counts external writes in: records/ (new), state/ (old), the person's own path
    line = json.dumps({"ts": "2026-09-29T10:00:00+00:00", "event": "external_write", "task": task, "ref": "bug-1", "notes": "filed"}) + "\n"
    for label, where, config, expected in (
            ("old layout (state/)", "qa-factory/state/journal.jsonl", None, 1),
            ("new layout (records/)", "qa-factory/records/journal.jsonl", None, 1),
            ("the person's own path", "elsewhere/journal.jsonl", "elsewhere/journal.jsonl", 1),
            ("no journal at all", None, None, 0)):
        root, task_root, env = seed(task)
        try:
            if config:
                cfg_path = root / "qa-factory" / "config.json"
                cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
                cfg["journal_path"] = config
                cfg_path.write_text(json.dumps(cfg), encoding="utf-8")
            if where:
                target = root / where
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(line, encoding="utf-8")
            driver = driver_for(root, env, task, no_trace=True)
            driver.where = lambda: {"action": "stop", "reason": "end of test"}
            printed = io.StringIO()
            with contextlib.redirect_stdout(printed):
                driver.run()
            check_eq(f"journal through the layout: {label}: the external write is counted (or not) as the file says",
                     "already holds 1 external_write event(s)" in printed.getvalue(), bool(expected))
        finally:
            harness.cleanup(root)
    # (b) parse_choices gets the story's case ids: a case word at a question stop is read as a CASE word and said back
    root, task_root, env = seed(task)
    try:
        work = task_root / "work"
        (work / "test-cases" / "area").mkdir(parents=True)
        (work / "test-cases" / "area" / "QA-9_TC_001.md").write_text(
            "---\nid: QA-9_TC_001\ntitle: first\nplan_row: TS-1\n---\n\n## Then\n1. x.\n", encoding="utf-8")
        (work / "requirements-readiness.json").write_text(json.dumps({"verdict": "blocked", "open_questions": [
            {"id": "Q1", "question": "Which?", "severity": "major",
             "readings": [{"reading": "r0", "from": "description", "if_chosen": "x"}, {"reading": "r1", "from": "description", "if_chosen": "x"}]}]}),
            encoding="utf-8")
        cfg_path = root / "qa-factory" / "config.json"
        cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
        cfg["case_id_form"] = "{ticket}_TC_{nnn}"
        cfg_path.write_text(json.dumps(cfg), encoding="utf-8")
        driver = driver_for(root, env, task)
        driver.py = lambda script, *a, **k: (0, "")
        driver.unread = lambda *a, **k: "continue"       # FV1-3: words code could not read go to the conductor; this test judges what code prints
        printed = io.StringIO()
        with contextlib.redirect_stdout(printed):
            driver.take_question_answer("S3", "S3-qa-test-strategist-1", "Q1: a\nQA-9_TC_001: accept as blocked\n")
        out = printed.getvalue()
        check_in("a question word is still recorded by code", "S3: recorded by code — Q1: a", out)
        check_in("the case word is said back as a case word, not as an unknown question", "`QA-9_TC_001: accept as blocked` is a word about a case", out)
        check_not_in("it is not listed as an unknown question id either", "not recognised as open questions", out)
        check_in("and says where it is applied", "say it again at gate A", out)
        printed = io.StringIO()
        with contextlib.redirect_stdout(printed):
            driver.take_question_answer("S3", "S3-qa-test-strategist-1", "NOT_A_CASE_1: accept as blocked\nQ77: a\n")
        check_not_in("an id that is no case of the story is no case word (control: the line is printed only for a real case)",
                     "is a word about a case", printed.getvalue())
        check_in("an unknown QUESTION id is still named as not recognised", "not recognised as open questions, so nothing is recorded for them: Q77", printed.getvalue())
    finally:
        harness.cleanup(root)
    # (c) stage_S4: `--apply-fixes` also for a pinned case that says `raise`, with or without a findings file
    for label, findings_text, case_says_raise, expected in (
            ("approve_with_fixes in the findings", "verdict: approve_with_fixes\n", False, True),
            ("a plain approve, no `raise` anywhere", "verdict: approve\n", False, False),
            ("a plain approve, a case says `raise`", "verdict: approve\n", True, True),
            ("no findings file, a case says `raise`", None, True, True),
            ("no findings file, nothing says `raise`", None, False, False)):
        root, task_root, env = seed(task)
        try:
            cases = task_root / "work" / "test-cases" / "area"
            cases.mkdir(parents=True)
            oracle = '[{"then": 1, "source": "unknown", "ref": "raise"}]' if case_says_raise else '[{"then": 1, "source": "ac", "ref": "R-1"}]'
            (cases / "TC-001.md").write_text(
                f"---\nid: TC-001\ntask: QA-9\nplan_row: TS-1\nthen_oracles: {oracle}\n---\n\n## Then\n1. x.\n", encoding="utf-8")
            findings = None
            if findings_text is not None:
                findings = cases / "critic-findings.md"
                findings.write_text(findings_text, encoding="utf-8")
            driver = driver_for(root, env, task)
            calls = []
            driver.py = lambda script, *a, **k: calls.append((script, [str(x) for x in a])) or (0, "")
            driver.run_role = lambda *a, **k: ("", None)
            driver.pin_cases = lambda: None
            driver.revise_plan = lambda: None
            driver.render_appendix = lambda: None
            driver.pinned_cases = lambda: ["QA-9_TC_001"]
            driver.critic_scope = lambda: ["QA-9_TC_001"]
            driver.budget_or_none = lambda *a, **k: {"counted": 0, "cap": 2}
            driver.newest = lambda pattern: findings
            with contextlib.redirect_stdout(io.StringIO()):
                driver.stage_S4()
            ran = [c for c in calls if c[0] == "critic_rollcall.py"]
            check_eq(f"S4 exit, {label}: `critic_rollcall.py --apply-fixes` runs: {expected}", bool(ran), expected)
            if ran:
                check_in(f"S4 exit, {label}: it is the same command", "--apply-fixes", " ".join(ran[0][1]))
                check_eq(f"S4 exit, {label}: the findings file is named only when there is one", str(findings) in ran[0][1], findings is not None)
        finally:
            harness.cleanup(root)


def main() -> None:
    run_scenarios([], [
        t261_k2_the_blocks_of_five_and_the_refused_are_not_dispatched,
        test_manual_block_dispatches_unprepared,
        t261_resume_after_a_crash_between_blocks_and_the_recovery_rule,
        t261_the_real_controller_refuses_a_completion_over_an_undispatched_case_and_takes_the_code_only_receipt,
        t261_prepare_by_code_on_the_cmp2_shape_and_the_temporal_door,
        t289_manual_block_goes_through_the_real_prepare_and_a_refusal_is_a_text,
        t289_the_automation_half_with_a_manual_half_pending_finishes_not_complete,
        t261_the_dry_gate_note_and_the_gate_b_text_slot,
        t261_the_integration_lines_of_the_driver,
    ])
    harness.finish("test_story_run_s6_manual")


# split: runner piece 1
if __name__ == "__main__":
    main()
