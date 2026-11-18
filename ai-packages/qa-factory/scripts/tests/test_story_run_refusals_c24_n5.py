#!/usr/bin/env python3
"""c24 n5: a part of test_story_run_refusals.py, split by tools/test_split.py (TD-11c). The shared helpers are in story_run_refusals_common."""
import contextlib
import io
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness  # noqa: E402
from harness import check, check_eq, check_in, check_not_in  # noqa: E402
from story_run_common import driver_for, jsonl, run_scenarios, seed, stub_calls
from story_run_refusals_common import RES_DISPATCH, RES_PLAIN, res_errors, res_fixture  # noqa: E402


# --- C2-4 (t-917, K9): a role is resumed only for judgement ---------------------------------------------------------------------------
K9_LENGTH = "handover form S5-qa-automator-1.yaml - scope[0].reason: 90 characters, at most 80. This is a repair, not a question for the person."


K9_CUT = {"shortened": [{"field": "scope[0].reason", "kept_len": 80, "written_len": 90}]}


def k9_driver(root, env, task: str, exit_lines, *, form=None):
    """A driver whose exit gate answers `exit_lines()` (a callable) and whose form check is `form(shorten)` -> (report, lines)."""
    driver = driver_for(root, env, task)
    driver.state["sessions"][RES_DISPATCH] = "sess-a"
    driver.exit_errors = lambda role, digest, dispatch=None: list(exit_lines())
    driver.controller_state = lambda: {"dispatches": {RES_DISPATCH: {"stage": "S5", "role": "qa-automator", "scope": ["TC-1"]}}}
    cuts = []
    driver.form_report = lambda dispatch, shorten=False: (cuts.append(shorten) or form(shorten)) if form else (None, [])
    return driver, cuts


def k9_handoff(driver, root, task_root, role="qa-automator", stage="S5"):
    result = json.loads((task_root / "state/driver-runs" / f"{RES_DISPATCH}.json").read_text(encoding="utf-8"))
    with contextlib.redirect_stdout(io.StringIO()):
        return driver.handoff(role, stage, RES_DISPATCH, result)


def refusal_c2_4_a_length_is_cut_by_code_not_resumed_for():
    """C2-4 T15a/T15b/T16 + I5: (a) after the first resume only lengths are left: the form is cut, the digest returned, NO third
    resume (the ladder point); (b) at the first entry only lengths: no paid call at all (the `handoff` point); (c) length beside a
    judgement line: the cut is not asked for and the role is woken (the third turn as today); (d) a scout's S1 gap stands first."""
    import story_run
    task = "QA-9"
    length = [K9_LENGTH]
    root, task_root, env = res_fixture(task, RES_PLAIN)
    try:
        state = {"cut": False}
        driver, cuts = k9_driver(root, env, task, lambda: res_errors("TC-1") if not stub_calls(root) else [],
                                 form=lambda shorten: ((state.update(cut=True) or K9_CUT), []) if shorten else (None, [] if state["cut"] else length))
        out = k9_handoff(driver, root, task_root)
        check_eq("T15a: one resume for the judgement line, none for the length left after it; the digest comes back",
                 ([c["kind"] for c in stub_calls(root)], bool(out)), (["resume"], True))
        check_eq("T15a: the form was cut once, by the driver's flag", cuts.count(True), 1)
    finally:
        harness.cleanup(root)
    root, task_root, env = res_fixture(task, RES_PLAIN)
    try:
        state = {"cut": False}
        driver, cuts = k9_driver(root, env, task, lambda: [],
                                 form=lambda shorten: ((state.update(cut=True) or K9_CUT), []) if shorten else (None, [] if state["cut"] else length))
        out = k9_handoff(driver, root, task_root)
        check_eq("T15b: only a length at the first entry: no paid call, the digest comes back", (stub_calls(root), bool(out)), ([], True))
    finally:
        harness.cleanup(root)
    root, task_root, env = res_fixture(task, RES_PLAIN)
    try:
        driver, cuts = k9_driver(root, env, task, lambda: res_errors("TC-1"), form=lambda shorten: (None, length))
        try:
            k9_handoff(driver, root, task_root)
        except story_run.Refusal:
            pass
        check_eq("T16: a length beside a judgement line: never cut, the role is woken (resume x2 as today)",
                 (cuts.count(True), [c["kind"] for c in stub_calls(root)]), (0, ["resume", "resume"]))
    finally:
        harness.cleanup(root)
    root, task_root, env = res_fixture(task, RES_PLAIN)
    try:
        # t-919 F-2 (T16b): at the ladder point NO assembly follows a cut, so the final-message line left on the exit side after the
        # first resume is the role's to repair with its form's words: nothing is cut, the third resume runs
        import story_run as _sr
        final = "digest: your final message is not the handoff form. " + _sr.REPAIR_MARKER
        driver, cuts = k9_driver(root, env, task, lambda: res_errors("TC-1") if not stub_calls(root) else [final],
                                 form=lambda shorten: (None, length))
        try:
            k9_handoff(driver, root, task_root)
        except story_run.Refusal:
            pass
        check_eq("T16b: a length beside the final-message line after the first resume: not cut, the role is woken (resume x2)",
                 (cuts.count(True), [c["kind"] for c in stub_calls(root)]), (0, ["resume", "resume"]))
    finally:
        harness.cleanup(root)
    root, task_root, env = res_fixture(task, RES_PLAIN)
    try:
        gap = "source unavailable and not accepted by a person: SRC-1a2b"
        driver, cuts = k9_driver(root, env, task, lambda: [gap], form=lambda shorten: (K9_CUT, []) if shorten else (None, length))
        try:
            k9_handoff(driver, root, task_root, role="qa-scout", stage="S1")
            check("I5: a scout's S1 gap is the person's", False)
        except story_run.Person as person:
            check_eq("I5: the S1 stop is raised before any cut or resume", (person.kind, True in cuts, stub_calls(root)), ("s1_gap", False, []))
    finally:
        harness.cleanup(root)


def k9_door_rig(root, env, task: str, role: str, dispatch: str, retry, *, wrote=True):
    """A driver for the code doors: `py` stub (window_record / ticket_adapter) rewrites `target` when `wrote`; claude and the
    seam must not run unless the test allows it. (driver, door log)"""
    driver = driver_for(root, env, task)
    driver.controller_state = lambda: {"dispatches": {dispatch: {"stage": dispatch.split("-")[0], "role": role, "scope": ["TC-1"]}}}
    driver.form_report = lambda d, shorten=False: (None, [])
    log = []
    real_py = driver.py
    target = driver.task_root / "work" / ("automation-manifest.json" if role == "qa-code-critic" else "source-inventory.json")

    def py(script, *args, **kw):
        if script in ("window_record.py", "ticket_adapter.py"):
            log.append(script)
            if wrote:
                target.write_text(target.read_text(encoding="utf-8") + " ", encoding="utf-8")
            return 0, "done"
        return real_py(script, *args, **kw)
    driver.py = py
    driver.exit_limit = lambda *a, **kw: log.append("exit_limit")
    return driver, log


def k9_refusal(dispatch: str, retry, text: str = "the qa-code-critic window is not receipted", role="qa-code-critic", stage="S5"):
    import story_run
    return story_run.Refusal(f"story_step finish {dispatch} (exit 3):\n{text}", dispatch=dispatch, retry=retry)


def refusal_c2_4_the_doors_of_code_run_before_every_resume():
    """C2-4 T17 (a-g) + F-2 + F-6 (t-909): the review receipt, the scout's receipts and the form are written by code BEFORE a
    resume; success closes the refusal with no `note_resume`; a changed key takes the whole road; the same key keeps today's
    road over the original refusal; a record that already holds the key and no session at all are met too (position invariant);
    a gap/stale window writes no receipt (I4); the step is not entered from inside its own retry."""
    import story_run
    task, dispatch = "QA-9", "S5-qa-code-critic-1"
    for label, role, disp in (("review receipt", "qa-code-critic", dispatch), ("source receipts", "qa-scout", "S1-qa-scout-1")):
        root, task_root, env = res_fixture(task, RES_PLAIN)
        try:
            (task_root / "work").mkdir(parents=True, exist_ok=True)
            for name in ("automation-manifest.json", "source-inventory.json"):
                (task_root / "work" / name).write_text("{}", encoding="utf-8")
            (task_root / "work" / "test-code").mkdir(parents=True, exist_ok=True)
            (task_root / "work" / "test-code" / "critic-findings.md").write_text("#", encoding="utf-8")
            calls = []
            driver, log = k9_door_rig(root, env, task, role, disp, None)
            driver.state["sessions"][disp] = "sess-a"
            driver.run_claude = lambda *a, **kw: (_ for _ in ()).throw(AssertionError("a paid call"))
            refusal = k9_refusal(disp, lambda: calls.append("retry"))
            with contextlib.redirect_stdout(io.StringIO()) as out:
                got = driver.resume_on_refusal(refusal, disp.split("-")[0], disp)
            check_eq(f"T17 ({label}): the door wrote, the retry went through: continue, no paid call, no resume on record",
                     (got, log, calls, driver.state.get("refusal_resumes")), ("continue", [log[0]], ["retry"], None))
            check_in(f"T17 ({label}): and the print names the door", "closed by code", out.getvalue())
        finally:
            harness.cleanup(root)
    root, task_root, env = res_fixture(task, RES_PLAIN)
    try:
        (task_root / "work" / "test-code").mkdir(parents=True, exist_ok=True)
        (task_root / "work" / "test-code" / "critic-findings.md").write_text("#", encoding="utf-8")
        (task_root / "work" / "automation-manifest.json").write_text("{}", encoding="utf-8")
        # T17b: a retry that raises ANOTHER refusal -> the whole road; the SAME key -> today's first resume over the original
        driver, log = k9_door_rig(root, env, task, "qa-code-critic", dispatch, None)
        driver.state["sessions"][dispatch] = "sess-a"
        seen = []
        driver.handle_refusal = lambda r2: seen.append(r2.text) or "continue"
        def other():
            raise k9_refusal(dispatch, None, "a different refusal")
        with contextlib.redirect_stdout(io.StringIO()):
            got = driver.resume_on_refusal(k9_refusal(dispatch, other), "S5", dispatch)
        check_eq("T17b: the retry's new refusal (another key) takes handle_refusal", (got, len(seen)), ("continue", 1))
        driver2, log2 = k9_door_rig(root, env, task, "qa-code-critic", dispatch, None)
        driver2.state["sessions"][dispatch] = "sess-a"
        def same():
            raise k9_refusal(dispatch, None)
        before = len(stub_calls(root))
        with contextlib.redirect_stdout(io.StringIO()):
            got = driver2.resume_on_refusal(k9_refusal(dispatch, same), "S5", dispatch)
        check_eq("T17b: the same key: today's first resume (one paid call, on record)",
                 (got, [c["kind"] for c in stub_calls(root)[before:]], len(driver2.state["refusal_resumes"][dispatch]["sess-a"])), ("continue", ["resume"], 1))
        with contextlib.redirect_stdout(io.StringIO()):
            driver2.resume_on_refusal(k9_refusal(dispatch, same), "S5", dispatch)
        check_eq("T17b: the same (dispatch, key) a second time: the doors are not run again (the bound), the seam is met instead",
                 (log2.count("window_record.py"), log2.count("exit_limit")), (1, 1))
        # T17c: the set is already on record ("already resumed"): the door still closes it, exit_limit is not met
        driver3, log3 = k9_door_rig(root, env, task, "qa-code-critic", dispatch, None)
        driver3.state["sessions"][dispatch] = "sess-a"
        refusal = k9_refusal(dispatch, lambda: None)
        driver3.note_resume(dispatch, "sess-a", story_run.finding_key(driver3.refusal_lines(refusal)), "refusal")
        with contextlib.redirect_stdout(io.StringIO()):
            got = driver3.resume_on_refusal(refusal, "S5", dispatch)
        check_eq("T17c: a set already on record, the door closes it: continue, the seam not met", (got, "exit_limit" in log3), ("continue", False))
        # T17g: no session at all: the door is met before the `exit_limit` of the 'no session' branch
        driver4, log4 = k9_door_rig(root, env, task, "qa-code-critic", dispatch, None)
        driver4.state["sessions"].pop(dispatch, None)
        with contextlib.redirect_stdout(io.StringIO()):
            got = driver4.resume_on_refusal(k9_refusal(dispatch, lambda: None), "S5", dispatch)
        check_eq("T17g: no session: the door closes first, exit_limit is not called", (got, "exit_limit" in log4), ("continue", False))
        # T17d/e: window_record wrote nothing (a gap, a stale review, a collision) -> no retry, today's road
        driver5, log5 = k9_door_rig(root, env, task, "qa-code-critic", dispatch, None, wrote=False)
        driver5.state["sessions"][dispatch] = "sess-a"
        retried = []
        before = len(stub_calls(root))
        with contextlib.redirect_stdout(io.StringIO()):
            got = driver5.resume_on_refusal(k9_refusal(dispatch, lambda: retried.append(1), "a window with a gap"), "S5", dispatch)
        check_eq("T17d: a door that writes nothing is no closure: no retry, the first resume as today", (got, retried, [c["kind"] for c in stub_calls(root)[before:]]),
                 ("continue", [], ["resume"]))
        # F-10: no findings file -> the receipt door does not run (a receipt is immutable; the role is woken for the findings)
        (task_root / "work" / "test-code" / "critic-findings.md").unlink()
        driver6, log6 = k9_door_rig(root, env, task, "qa-code-critic", dispatch, None)
        driver6.state["sessions"][dispatch] = "sess-a"
        with contextlib.redirect_stdout(io.StringIO()):
            driver6.resume_on_refusal(k9_refusal(dispatch, lambda: None, "no findings yet"), "S5", dispatch)
        check_eq("F-10: no findings file, no receipt door", log6, [])
        # F-2: a door that writes on every pass + a retry raising a fresh key each time: ONE door run, then today's branches
        (task_root / "work" / "test-code" / "critic-findings.md").write_text("#", encoding="utf-8")
        driver7, log7 = k9_door_rig(root, env, task, "qa-code-critic", dispatch, None)
        driver7.state["sessions"][dispatch] = "sess-a"
        counter = []
        def fresh():
            counter.append(1)
            raise k9_refusal(dispatch, fresh, f"a refusal that changes: {len(counter)}")
        driver7.handle_refusal = lambda r2: driver7.resume_on_refusal(r2, "S5", dispatch)
        before = len(stub_calls(root))
        with contextlib.redirect_stdout(io.StringIO()):
            got = driver7.resume_on_refusal(k9_refusal(dispatch, fresh), "S5", dispatch)
        check_eq("F-2: the step is not entered from inside its own retry: one door run, one retry, one resume (the nested refusal's)",
                 (got, log7, len(counter), [c["kind"] for c in stub_calls(root)[before:]], driver7.in_code_step), ("continue", ["window_record.py"], 1, ["resume"], False))
    finally:
        harness.cleanup(root)


def refusal_c2_4_s4_keeps_open_only_when_the_round_will_run():
    """C2-4 T18/T18b + F-3/F-4/F-6 (t-909): the S4 case critic's finish says `OpenWork` (`--not-complete --unresolved --reason`)
    exactly when the rework branch will run (verdict sends cases back, a round is left, a findings file exists); with no findings
    file the old False stays (one resume of the critic, no new critic); the recovery road (`completion_for`) applies the same rule
    BEFORE `rework_of`; the reason is timeless and at most 300; the D3 pins and the F-6 (b) unknown-window pin."""
    import story_run
    task = "QA-9"
    root, task_root, env = res_fixture(task, RES_PLAIN)
    try:
        driver = driver_for(root, env, task)
        # X2-7: the critic's finish reads its form by the dispatch id and writes the stage acceptance first (a known word, a no-op writer)
        driver.last_dispatch = "S4-qa-case-critic-1"
        driver.stage_verdict_known = lambda form: True
        driver.stage_acceptance_write = lambda stage, dispatch: None
        # X2-7 point 7: a critic that sends cases back on the LAST round (or with a count that is no number) goes to the conductor seam; here the seam
        # answers "no move needed" (a stub, as in test_repair_route), so the T18 expectations of those rows (None) stay what they were
        driver.pipeline = lambda: {}
        seam = []
        driver.stage_review_exhausted = lambda stage, *a, **k: seam.append((stage, bool(k.get("unreadable")), k.get("text") or "")) or None
        digest = "qa-case-critic S4 TC-1 · concerns\nTC-1 · rejected · weak Then\nwork/test-cases/critic-findings.md"
        rule = driver.s4_critic_completion(["TC-1", "TC-2"], 0, 2)
        check_eq("F-3: concerns, a round left, NO findings file: the old False (one resume of the critic, no open stage)", rule(digest), False)
        findings = task_root / "work" / "test-cases" / "critic-findings.md"
        findings.parent.mkdir(parents=True, exist_ok=True)
        findings.write_text("# findings", encoding="utf-8")
        got = rule(digest)
        check_eq("T18: with a findings file the finish is OpenWork cases_in_repair", (type(got).__name__, got.unresolved), ("OpenWork", "cases_in_repair"))
        check_in("F-3 (t-919): the reason names the cases the critic REJECTED (1 of the 2 in scope) and the findings path",
                 "the case critic sent 1 case(s) back for repair; S4 was kept open for the repair round: TC-1; its findings: work/test-cases/critic-findings.md", got.reason)
        no_rows = driver.s4_critic_completion(["TC-1", "TC-2"], 0, 2)("qa-case-critic S4 TC-1 · concerns\nwork/test-cases/critic-findings.md").reason
        check_eq("F-3 (t-919): a rejected set that cannot be read prints no number (FR-41)",
                 (no_rows.startswith("the case critic sent work back for repair; S4 was kept open"), any(ch.isdigit() for ch in no_rows.split(";")[0])), (True, False))
        check_not_in("T18: and is timeless (no 'round k of cap', no present tense)", " is kept", got.reason)
        check_eq("T18: approve -> None (the critic closes S4)", rule(digest.replace("concerns", "approve")), None)
        check_eq("T18: the last round (counted == cap) with an unreadable roll-call -> the conductor seam",
                 (driver.s4_critic_completion(["TC-1"], 2, 2)(digest), seam[-1][:2]), (None, ("S4", True)))
        check_in("T18: the last round (counted == cap) with an unreadable roll-call -> the conductor seam: its text", "roll-call could not be read", seam[-1][2])
        check_eq("T18/edge 15: a count that is no number -> the conductor seam, no number printed",
                 (driver.s4_critic_completion(["TC-1"], None, "x")(digest), seam[-1][:2]), (None, ("S4", True)))
        check_in("T18/edge 15: the seam's text names the repair count", "repair count", seam[-1][2])
        check("T18/edge 15: and prints no digit", not any(ch.isdigit() for ch in seam[-1][2]), seam[-1][2])
        long_scope = [f"TC-{i:04d}" for i in range(80)]
        long_digest = "qa-case-critic S4 TC-0000 · concerns\n" + "".join(f"{c} · rejected · weak Then\n" for c in long_scope) + "work/test-cases/critic-findings.md"
        reason = driver.s4_critic_completion(long_scope, 0, 2)(long_digest).reason
        check_eq("T18: a long list is cut to 300 and ends with the path of the findings", (len(reason), reason.endswith("… [list: work/test-cases/critic-findings.md]")), (300, True))
        driver.controller = lambda *a, **kw: {"repair_budget": {"counted": 0, "cap": 2}}
        recovered = driver.completion_for("S4", "qa-case-critic", {"id": "S4-qa-case-critic-1", "scope": ["TC-1"], "rework_of": "S4-qa-case-critic-1"})
        check_eq("F-4: the recovery road applies the same rule, before rework_of", type(recovered(digest)).__name__, "OpenWork")
        argv = []
        driver.py = lambda script, *args, **kw: argv.extend(str(a) for a in args) or (0, "accepted x")
        driver.finish("S4-qa-case-critic-1", digest, complete=got, role="qa-case-critic", stage="S4")
        check_eq("T18: the pair reaches story_step as --not-complete --unresolved … --reason …",
                 ("--not-complete" in argv, argv[argv.index("--unresolved") + 1] if "--unresolved" in argv else None, "--reason" in argv),
                 (True, "cases_in_repair", True))
        check_eq("T18b (D3 pin): a rework's finish stays False - the designer's repair round is not closed by itself",
                 (driver.completion_for("S4", "qa-case-designer", {"rework_of": "x"}), driver.completion_for("S2", "qa-x", {"purpose": "repair_verify"})),
                 (False, False))
        def broken(*a, **kw):
            raise story_run.Refusal("stage-scope: cannot read")
        driver.stage_scope = broken
        check_eq("F-6 (b) pin: an unreadable window state keeps False (FR-59: unknown is never a pass)",
                 driver.completion_for("S5", "qa-code-critic", {"scope": ["TC-1"]}), False)
    finally:
        harness.cleanup(root)


def refusal_c2_4_an_owed_s4_repair_round_starts_instead_of_a_new_critic():
    """t-919 F-1: a critic accepted with `cases_in_repair` and no designer rework registered (its finish went through the recovery
    road, or a refused finish that came back as `continue`, so `stage_S4`'s tail never ran) is owed its round: the next `stage_S4`
    entry registers the designer rework from the DATA and dispatches NO critic. The carrier is read from the real rule's own
    OpenWork, one case per road; and the entries that must still run a critic (a rework already registered, no findings file, the
    last round, another word, the live road)."""
    task = "QA-9"
    digest = "qa-case-critic S4 TC-1 · concerns\nTC-1 · rejected · weak Then\nwork/test-cases/critic-findings.md"

    def run(label, dispatches, *, findings=True, counted=0, live_digest=None):
        root, task_root, env = seed(task)
        try:
            driver = driver_for(root, env, task)
            findings_file = driver.task_root / "work" / "test-cases" / "critic-findings.md"      # the driver's own spelling of the root
            findings_file.parent.mkdir(parents=True, exist_ok=True)
            findings_file.write_text("verdict: approve_with_fixes\n", encoding="utf-8")
            roles, rework, calls = [], [], []
            driver.py = lambda script, *a, **k: calls.append(script) or (0, "")
            driver.controller_state = lambda: {"dispatches": dispatches}
            driver.run_role = lambda stage, role, **k: roles.append(role) or (live_digest or digest, None)
            driver.rework = lambda stage, role, cases, reason, **k: rework.append((stage, role, list(cases)))
            driver.pin_cases = lambda: None
            driver.revise_plan = lambda: None
            driver.render_appendix = lambda: calls.append("appendix")
            driver.critic_scope = lambda: ["TC-1", "TC-2"]
            driver.budget_or_none = lambda *a, **k: {"counted": counted, "cap": 2}
            driver.newest = lambda pattern: findings_file if findings else None
            driver.unraised_cases = lambda: False
            with contextlib.redirect_stdout(io.StringIO()):
                driver.stage_S4()
            return roles, rework, driver
        finally:
            harness.cleanup(root)

    base = {"S4-qa-case-designer-1": {"stage": "S4", "role": "qa-case-designer", "status": "accepted"}}

    def with_critic(unresolved, status="accepted"):
        return {**base, "S4-qa-case-critic-1": {"stage": "S4", "role": "qa-case-critic", "status": status, "unresolved": unresolved}}

    root, task_root, env = seed(task)
    try:
        probe = driver_for(root, env, task)
        # X2-7: the critic's finish reads its form by the dispatch id and writes the stage acceptance first (a known word, a no-op writer)
        probe.last_dispatch = "S4-qa-case-critic-1"
        probe.stage_verdict_known = lambda form: True
        probe.stage_acceptance_write = lambda stage, dispatch: None
        (task_root / "work" / "test-cases").mkdir(parents=True, exist_ok=True)
        (task_root / "work" / "test-cases" / "critic-findings.md").write_text("#", encoding="utf-8")
        probe.controller = lambda *a, **kw: {"repair_budget": {"counted": 0, "cap": 2}}
        recovery = probe.completion_for("S4", "qa-case-critic", {"id": "S4-qa-case-critic-1", "scope": ["TC-1"], "rework_of": "S4-qa-case-critic-1"})(digest)
        refused_then_continue = probe.s4_critic_completion(["TC-1"], 0, 2)(digest)
    finally:
        harness.cleanup(root)
    for road, open_work in (("recovery road (completion_for via _finish_saved_result)", recovery),
                            ("refused finish returned as continue", refused_then_continue)):
        roles, rework, _driver = run(road, with_critic(open_work.unresolved))
        check_eq(f"F-1, {road}: the owed round is registered from the data and no critic is dispatched",
                 (roles, rework), ([], [("S4", "qa-case-designer", ["TC-1", "TC-2"])]))
    roles, rework, _driver = run("a list-shaped record", with_critic(["cases_in_repair"]))
    check_eq("F-1: the word is found in whatever shape the record keeps it", (roles, len(rework)), ([], 1))
    roles, rework, _driver = run("normal road", base, live_digest=digest)
    check_eq("F-1, normal road: the live critic runs once and ITS tail registers the round once", (roles, len(rework)), (["qa-case-critic"], 1))
    later = {**with_critic("cases_in_repair"), "S4-qa-case-designer-2": {"stage": "S4", "role": "qa-case-designer", "status": "running"}}
    roles, rework, _driver = run("a rework registered", later, live_digest="qa-case-critic S4 TC-1 · ok\nwork/x.md")
    check_eq("F-1: a designer rework already registered after the critic: the pre-check stands down (the next critic is the live one)",
             (roles, rework), (["qa-case-critic"], []))
    roles, rework, _driver = run("no findings", with_critic("cases_in_repair"), findings=False, live_digest="qa-case-critic S4 TC-1 · ok\nx.md")
    check_eq("F-1: no findings file: the round cannot be started, the critic writes them (today's road)", (roles, rework), (["qa-case-critic"], []))
    roles, rework, _driver = run("last round", with_critic("cases_in_repair"), counted=2, live_digest="qa-case-critic S4 TC-1 · ok\nx.md")
    check_eq("F-1: the last round: no repair is owed", (roles, rework), (["qa-case-critic"], []))
    roles, rework, _driver = run("another word", with_critic("repairs_pending"), live_digest="qa-case-critic S4 TC-1 · ok\nx.md")
    check_eq("F-1: another word in the record is not this carrier", (roles, rework), (["qa-case-critic"], []))
    roles, rework, _driver = run("unreadable", with_critic(None), live_digest="qa-case-critic S4 TC-1 · ok\nx.md")
    check_eq("F-1: an absent `unresolved` is not owed: a fresh critic, never a silent close", (roles, rework), (["qa-case-critic"], []))


def refusal_n5_the_driver_refuses_as_the_hook_does_and_uses_the_one_packet() -> None:
    """RC1-14 step 5 (N5): `Driver.system_file` never starts a role with `blocks = []`. Over budget -> the hook's own text as a
    `Refusal` (`injection_over_budget`, `known` False) and the hook's denial line; any other failure, a missing map and an unknown
    role -> `injection_unbuilt` with the dry-run door and a denial line; a built layer -> the packet of `task_packet` with the kind
    of the dispatch's own record."""
    import inject_context
    import story_run
    task = "QA-9"
    root, task_root, env = seed(task)
    saved = {name: getattr(inject_context, name) for name in ("load_map", "collect_blocks")}
    try:
        driver = driver_for(root, env, task)
        denials = task_root / "state" / "dispatch-denials.jsonl"

        def attempt(role="qa-scout", dispatch="S1-qa-scout-1"):
            try:
                return driver.system_file(role, dispatch, ["TC-1"]), None
            except story_run.Refusal as refusal:
                return None, refusal

        # D1 / D2: the budget is read after .strip(), so a body of 26 000 chars is delivered and 26 001 is refused
        big = root / "big-slice.md"
        inject_context.load_map = lambda: {"common": [], "roles": {"qa-scout": ["project:big-slice.md"]}}
        big.write_text("x" * 26001, encoding="utf-8")
        try:
            inject_context.collect_blocks("qa-scout", inject_context.load_map())
            hook_text = ""
        except ValueError as exc:
            hook_text = str(exc)
        check("D1: the fixture is over the budget for collect_blocks", "exceeds budget" in hook_text, hook_text)
        path, refusal = attempt()
        check("D1: a Refusal is raised and no sysfile is written", refusal is not None and path is None)
        if refusal is not None:
            check_eq("D1: its text is the hook's own ValueError text, byte for byte", refusal.text, hook_text)
            check_eq("D1: its title", refusal.title, "injection_over_budget")
            check_eq("D1: its dispatch", refusal.dispatch, "S1-qa-scout-1")
            check_eq("D1: known is False on the instance, so the table never routes it", (refusal.known, story_run.route_known(refusal)), (False, None))
        check("D1: the sysfile of the refused dispatch is not there", not (driver.state_dir / "driver-tmp" / "S1-qa-scout-1.system.md").exists())
        check_eq("D1: no claude call", stub_calls(root), [])
        rows = jsonl(denials)
        check_eq("D1: one denial line `recover` can close", [(r.get("dispatch_id"), r.get("role"), r.get("reason")) for r in rows],
                 [("S1-qa-scout-1", "qa-scout", hook_text)])
        big.write_text("x" * 26000, encoding="utf-8")
        path, refusal = attempt()
        check("D2: 26 000 chars -> the role runs (a sysfile, no refusal)", refusal is None and path is not None and path.is_file())
        check_eq("D2: and no new denial line", len(jsonl(denials)), 1)

        # D3: any other exception, the map missing, the role unknown -> injection_unbuilt with a door and a denial line
        def boom(*args, **kwargs):
            raise RuntimeError("the slice reader broke")
        inject_context.collect_blocks = boom
        inject_context.load_map = saved["load_map"]
        path, refusal = attempt()
        check("D3: RuntimeError -> Refusal injection_unbuilt, no sysfile", refusal is not None and path is None and refusal.title == "injection_unbuilt")
        if refusal is not None:
            check_in("D3: the text names the door", "--dry-run --role qa-scout", refusal.text)
            check_in("D3: and the cause", "RuntimeError: the slice reader broke", refusal.text)
            check_eq("D3: known is False", (refusal.known, story_run.route_known(refusal)), (False, None))
        check_eq("D3: a denial line was written", len(jsonl(denials)), 2)
        inject_context.collect_blocks = saved["collect_blocks"]
        inject_context.load_map = lambda: {}
        path, refusal = attempt()
        check("D3: the map missing -> injection_unbuilt (not an empty rule layer)", refusal is not None and path is None and refusal.title == "injection_unbuilt")
        inject_context.load_map = saved["load_map"]
        path, refusal = attempt(role="qa-nobody")
        check("D3: a role the map does not name -> injection_unbuilt", refusal is not None and path is None and refusal.title == "injection_unbuilt")
        if refusal is not None:
            check_in("D3: naming the role", "qa-nobody", refusal.text)
        check_eq("D3: every refusal left its denial line", len(jsonl(denials)), 4)
        check_eq("D3: and no role was launched", stub_calls(root), [])

        # D4 / D5: the kind comes from THIS dispatch's record; the packet is `task_packet`'s
        state = driver.controller_state()
        records = {"S5-qa-automator-2": {"id": "S5-qa-automator-2", "stage": "S5", "role": "qa-automator", "scope": ["TC-1"],
                                         "rework_of": "S5-qa-automator-1", "repair_cause": "test_defect",
                                         "known_paths": {"package_fingerprint": "fp-1"}},
                   "S5-qa-automator-1": {"id": "S5-qa-automator-1", "stage": "S5", "role": "qa-automator", "scope": ["TC-1"]}}
        driver.controller_state = lambda: dict(state, dispatches=records)
        drop, keep = "### Profiles, leases and build commands", "### After a mechanical fix"
        path, refusal = attempt("qa-automator", "S5-qa-automator-2")
        check("D4: a repair record builds a sysfile", refusal is None and path is not None, getattr(refusal, "text", ""))
        text = path.read_text(encoding="utf-8")
        check("D4: a repair lacks the dropped section and holds the kept one", drop not in text and keep in text)
        path, refusal = attempt("qa-automator", "S5-qa-automator-1")
        first = path.read_text(encoding="utf-8")
        check("D4: a first record holds both", drop in first and keep in first)
        packet = lambda sysfile: json.loads(sysfile.split("# Resolved task packet", 1)[1].split("\n", 1)[1])
        repair_packet = packet(text)
        check_eq("D5: the dispatch projection has kind, role and scope", (repair_packet["dispatch"]["kind"], repair_packet["dispatch"]["role"],
                                                                         repair_packet["dispatch"]["scope"]), ("repair", "qa-automator", ["TC-1"]))
        check("D5: and no known_paths of its own", "known_paths" not in repair_packet["dispatch"])
        check_in("D5/E10: the record's own key is added to the one known_paths", "package_fingerprint", json.dumps(repair_packet["known_paths"]))
        check_in("D5/E10: and every stored value stays", "project_root", json.dumps(repair_packet["known_paths"]))
        first_packet = packet(first)
        check_eq("D5: a first record's kind", first_packet["dispatch"]["kind"], "first")
        path, _ = attempt("qa-automator", "S5-qa-automator-9")          # no record of this id
        none_packet = packet(path.read_text(encoding="utf-8"))
        check_eq("D5: no record -> kind first, role and scope from the arguments",
                 (none_packet["dispatch"]["kind"], none_packet["dispatch"]["role"], none_packet["dispatch"]["scope"], none_packet["dispatch"]["id"]),
                 ("first", "qa-automator", ["TC-1"], "S5-qa-automator-9"))
        check("D5: no record -> no known_paths in the dispatch", "known_paths" not in none_packet["dispatch"])
        driver.controller_state = type(driver).controller_state.__get__(driver)
        # a non-object record or state is kind first, never a crash
        driver.controller_state = lambda: {"dispatches": {"S5-qa-automator-3": "garbage"}}
        path, refusal = attempt("qa-automator", "S5-qa-automator-3")
        check("D5: a record that is not an object -> a sysfile of kind first", refusal is None and drop in path.read_text(encoding="utf-8"))
        driver.controller_state = type(driver).controller_state.__get__(driver)

        # D6: no controller.json -> the role runs with kind first, never a refusal
        (task_root / "state" / "controller.json").unlink()
        path, refusal = attempt("qa-automator", "S5-qa-automator-2")
        check("D6: no controller.json -> a sysfile, no refusal", refusal is None and path is not None, getattr(refusal, "text", ""))
        check_eq("D6: the kind is first", packet(path.read_text(encoding="utf-8"))["dispatch"]["kind"], "first")
    finally:
        for name, value in saved.items():
            setattr(inject_context, name, value)
        harness.cleanup(root)


def refusal_s4_critic_finish_survivors():
    """A1a S-R8 / S-R9 / S-R10: the S4 behaviours of the deleted stage-critic route test (R8, R9 S4 part, R10 through S4's writer), pinned
    on the live S4 code. S-R8: the record is written FIRST from the critic's form, then S4's own rule (`concerns` at 0 of 2 -> OpenWork
    `cases_in_repair`; `ok` -> None; `concerns` at 2 of 2 -> the seam is asked with "S4"). S-R9: the restart road writes the record of the
    RECORD's dispatch id; a record with no id writes nothing and asks the seam with the reason. S-R10: the critic's `questions[]` are
    raised BEFORE its record, `check=True`, by the acceptor, from its form; with no form file only the record is written."""
    for verdict, counted, expect in (("concerns", 0, "OpenWork"), ("ok", 0, "None"), ("concerns", 2, "seam")):
        root, task_root, env = seed("QA-9")
        try:
            driver = driver_for(root, env, "QA-9", max_boundaries=1)
            findings = driver.task_root / "work" / "test-cases" / "critic-findings.md"
            findings.parent.mkdir(parents=True, exist_ok=True)
            findings.write_text("the cases say too little\n", encoding="utf-8")
            log = {"written": [], "seam": [], "events": []}
            driver.last_dispatch = "S4-qa-case-critic-1"
            driver.stage_verdict_known = lambda form: True
            driver.stage_acceptance_write = lambda stage, dispatch: log["written"].append((stage, dispatch)) or log["events"].append("written")
            driver.stage_review_exhausted = lambda *a, **k: log["seam"].append(a[0]) or None
            driver.pipeline = lambda: {}
            got = driver.s4_critic_completion(["TC-1"], counted, 2)(f"qa-case-critic S4 TC-1 · {verdict}\nTC-1 · ok · reviewed\nwork/x.md")
            check_eq(f"S-R8 s4-record-first-then-rule: {verdict} at {counted} of 2: the record is written first, for this dispatch",
                     (log["written"], log["events"][:1]), ([("S4", "S4-qa-case-critic-1")], ["written"]))
            check_eq(f"S-R8 s4-record-first-then-rule: {verdict} at {counted} of 2: the result and the seam calls",
                     (type(got).__name__, getattr(got, "unresolved", None), log["seam"]),
                     {"OpenWork": ("OpenWork", "cases_in_repair", []), "None": ("NoneType", None, []),
                      "seam": ("NoneType", None, ["S4"])}[expect])
        finally:
            harness.cleanup(root)
    root, task_root, env = seed("QA-9")
    try:
        driver = driver_for(root, env, "QA-9", max_boundaries=1)
        log = {"written": [], "seam": []}
        driver.last_dispatch = ""
        driver.stage_verdict_known = lambda form: True
        driver.stage_acceptance_write = lambda stage, dispatch: log["written"].append((stage, dispatch))
        driver.stage_review_exhausted = lambda *a, **k: log["seam"].append(k.get("text") or "verdict") or None
        driver.pipeline = lambda: {}
        got = driver.s4_critic_completion(["TC-1"], 0, 2, dispatch_id="S4-qa-case-critic-7")("qa-case-critic S4 TC-1 · ok\nTC-1 · ok · reviewed\n")
        check_eq("S-R9 s4-restart-reads-record-id: the restart road writes the record of the RECORD's dispatch",
                 (log["written"], got), ([("S4", "S4-qa-case-critic-7")], None))
        log["written"].clear()
        driver.s4_critic_completion(["TC-1"], 0, 2, dispatch_id="")("x")
        check_eq("S-R9 s4-restart-reads-record-id: a record with no id writes nothing and asks the seam once", (log["written"], len(log["seam"])), ([], 1))
        check_in("S-R9 s4-restart-reads-record-id: the seam's reason names the missing id", "no dispatch id", log["seam"][0])
    finally:
        harness.cleanup(root)
    for present in (True, False):
        root, task_root, env = seed("QA-9")
        try:
            driver = driver_for(root, env, "QA-9", max_boundaries=1)
            form = driver.task_root / "work" / "handoffs" / "S4-qa-case-critic-1.yaml"
            if present:
                form.parent.mkdir(parents=True, exist_ok=True)
                form.write_text("header:\n  role: qa-case-critic\n  stage: S4\n  verdict: ok\n", encoding="utf-8")
            calls = []
            driver.py = lambda script, *a, **kw: calls.append((script, [str(x) for x in a], kw.get("check"))) or (0, "")
            driver.stage_acceptance_write("S4", "S4-qa-case-critic-1")
            label = "form present" if present else "form file absent"
            if present:
                raise_args = calls[0][1]
                check_eq(f"S-R10 s4-critic-questions-before-record: {label}: the raise comes first, with check=True, by the acceptor, from the form",
                         (calls[0][0], calls[0][2], raise_args[raise_args.index("--stage") + 1], raise_args[raise_args.index("--asked-by") + 1],
                          raise_args[raise_args.index("--from-handoff") + 1]),
                         ("question_register.py", True, "S4", "qa-case-critic", "work/handoffs/S4-qa-case-critic-1.yaml"))
            check_eq(f"S-R10 s4-critic-questions-before-record: {label}: the record call follows (and is the only call when the form is absent)",
                     [(c[0], c[1][c[1].index("--acceptance") + 1]) for c in calls if c[0] == "stage_done.py"],
                     [("stage_done.py", "work/handoffs/S4-qa-case-critic-1.yaml")])
            check_eq(f"S-R10 s4-critic-questions-before-record: {label}: the order of the scripts",
                     [c[0] for c in calls], ["question_register.py", "stage_done.py"] if present else ["stage_done.py"])
        finally:
            harness.cleanup(root)


def main() -> None:
    run_scenarios([], [
        refusal_c2_4_a_length_is_cut_by_code_not_resumed_for,
        refusal_c2_4_the_doors_of_code_run_before_every_resume,
        refusal_c2_4_s4_keeps_open_only_when_the_round_will_run,
        refusal_s4_critic_finish_survivors,
        refusal_c2_4_an_owed_s4_repair_round_starts_instead_of_a_new_critic,
        refusal_n5_the_driver_refuses_as_the_hook_does_and_uses_the_one_packet,
    ])
    harness.finish("test_story_run_refusals_c24_n5")


# split: runner piece 1
if __name__ == "__main__":
    main()
