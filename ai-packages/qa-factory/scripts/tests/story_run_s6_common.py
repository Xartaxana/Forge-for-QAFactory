"""Story-runner tests, S5 critic finish and S6 freshness (t-079, D1): the last window's critic closes S5 only
over a window record code builds; the automation branch of S6 asks the story's own record what stands, after the
stand question and before any runner; and the words the roles are told are pinned in the driver's source.

Nothing here reaches the network or a real model. The stub and the helpers live in `story_run_common`, which
imports `harness` before anything from scripts/ (harness points STORY_RUN_CLAUDE at no_claude.py).
"""
# Shared helpers of test_story_run_s6.py, split by tools/test_split.py (TD-11c).
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import story_run_common  # noqa: E402
from story_run_common import d1_driver, d1_write_blocks, driver_for


class _Awaits:
    """X7-6c: the `complete` of a final S6 runner window under a consumer is the open-work word `stage_awaits_acceptance` (the runner never closes
    S6 by its own finish); this compares equal to that word, whatever its reason text."""

    def __eq__(self, other):
        return type(other).__name__ == "OpenWork" and story_run_common.awaits(other) == "stage_awaits_acceptance"

    def __repr__(self):
        return "<awaits the consumer>"


AWAITS = _Awaits()


def owed_words(row) -> str:
    """The text of an owed journal row: its arguments, and the file `--notes-file` names (FV1-4 N0: a person's words travel by a file)."""
    args = [str(a) for a in row["args"]]
    text = " ".join(args)
    if "--notes-file" in args:
        text += "\n" + Path(args[args.index("--notes-file") + 1]).read_text(encoding="utf-8")
    return text


# --- t-261: the manual half of S6 (t-250 §1, C2, C4) --------------------------------------------------------------
# TP1-15045 (cmp2): `run_manual_block` sent all eleven manual cases in one dispatch (the controller refuses a block
# of more than five), and `manual_evidence.prepare` refused every one. The driver now prepares each case by code, never
# dispatches a refused one, and dispatches the rest in blocks of at most five, ONE per entry, in plan-row order.

class ManualWorld:
    """The controller's dispatch table as the driver reads it, and a stand-in for `Controller` that registers a manual
    dispatch into it. `accept(id)` is the controller accepting what a runner finished."""

    def __init__(self):
        self.dispatches = {}
        self.waits = []          # the `wait_seconds` of every Controller the driver built (M8: a lifecycle command waits)

    def accept(self, dispatch_id):
        self.dispatches[dispatch_id]["status"] = "accepted"

    def controller_class(self):
        world = self

        class FakeController:
            def __init__(self, task_root, wait_seconds=0.0):
                world.waits.append(wait_seconds)

            def state(self):
                return {"dispatches": world.dispatches}

            def prepare(self, options):
                return {"dispatch_request": {"id": options["id"], "stage": options["stage"], "role": options["role"],
                                             "scope": list(options["scope"])}}

            def apply(self, operation, request):
                assert operation == "dispatch"
                world.dispatches[request["id"]] = dict(request, status="running")
        return FakeController


def manual_rig(root, env, task, cases, refused=(), world=None, auto_dispatches=(), policy="api"):
    """(driver, world, launched role calls, moves, printed text getter) with `cases` the manual scope: `refused` names the
    cases `prepare` refuses; every seam that would start a process or a model is replaced. `policy` is what
    `manual_policy` answers (t-292): one word for every case, a {case: word} map (an absent case is `api`), or a
    function - the default `api` keeps every older check away from the stand-login question."""
    world = world or ManualWorld()
    driver = driver_for(root, env, task)
    launched, moves = [], []
    # a story at the manual half has its run report from the automated half: `walk_before` (t-1957) finalizes only when it is absent, so
    # the pins below on WHERE the reduction sits count the close's own finalize, not the walker's
    report = Path(driver.task_root) / "work" / "run-report.json"
    report.parent.mkdir(parents=True, exist_ok=True)
    if not report.is_file():
        report.write_text("{}", encoding="utf-8")
    driver.controller_state = lambda: {"dispatches": world.dispatches}
    driver.manual_order = lambda given: list(given)
    driver.MANUAL_BLOCK_MAX = 5     # SC2-38 item 3: the default window is one case; the older checks here keep their blocks of five
    driver.manual_prepare = lambda case: ([], f"the check could not be taken: {case} stands as not checked by hand", "") \
        if case in refused else ([f"OB-{case}"], "", "")
    driver.manual_policy = policy if callable(policy) else (
        (lambda case: policy.get(case, "api")) if isinstance(policy, dict) else (lambda case: policy))
    driver.manual_gate_note = lambda: None
    driver.manual_request_paths = lambda block: [f"work/evidence/manual/{c}/request.json" for c in block]
    driver.run_role = lambda stage, role, **kw: launched.append(dict(kw, stage=stage, role=role)) or ("", None)
    driver.code_only = lambda stage, reason, evidence: moves.append(("code_only", stage, reason, list(evidence)))
    real_py = driver.py

    def py(script, *args, **kwargs):
        if script == "stage_done.py":
            if "running" in args:          # the block's own `--status running` is not a closing move
                return 0, ""
            moves.append(("stage_done", " ".join(str(a) for a in args)))
            return 0, ""
        if script == "finalize_task.py":
            moves.append(("finalize", str(args[0])))
            return 0, ""
        return real_py(script, *args, **kwargs)
    driver.py = py
    return driver, world, launched, moves


def record_failure_analyst_accept(driver, dispatch_id):
    """X7-6c: S6 closes only over the consumer's (failure analyst's) `accept` record for the author's last dispatch, never on the runner's own
    word; the rig's accepted runner dispatch has been judged by the analyst (the record written the way `stage_done.py --acceptance` writes it)."""
    story_run_common.accept_record(driver.task_root, "S6", dispatch_id)


def enter_manual(driver, world, cases, accept=True):
    """One entry: `run_manual_block` with the controller replaced; the new dispatch is ACCEPTED afterwards when asked to
    be (the runner finished). (the printed text, the dispatch id registered or "")."""
    import contextlib
    import io
    from unittest import mock
    before = set(world.dispatches)
    out = io.StringIO()
    with mock.patch("controller.Controller", world.controller_class()), contextlib.redirect_stdout(out):
        driver.run_manual_block(list(cases))
    new = sorted(set(world.dispatches) - before)
    if accept:
        for dispatch_id in new:
            world.accept(dispatch_id)
            record_failure_analyst_accept(driver, dispatch_id)
    return out.getvalue(), (new[0] if new else "")


# --- t-292: the stand's sign-in account, asked BEFORE a block with a screen case is dispatched ------------------------
# TP1-15045 (cmp2r rehearsal, 02.10): screen cases were dispatched with no usable test account and every capture
# photographed the sign-in page. `d2_seed` records `environment.env_file = qa.env` (an env file with no account in it),
# so the DEFAULT of these scenarios is "the file is there, the account is not"; each scenario writes the config it needs.

def t292_config(root, manual_capture=None, **environment):
    """The project's config with exactly this `environment` (no env_file at all when none is given) and, when given,
    `manual_capture`."""
    path = root / "qa-factory" / "config.json"
    cfg = json.loads(path.read_text(encoding="utf-8"))
    cfg["environment"] = dict(environment)
    cfg.pop("manual_capture", None)
    if manual_capture is not None:
        cfg["manual_capture"] = manual_capture
    path.write_text(json.dumps(cfg, indent=2), encoding="utf-8")


SCREENS = {"QA-9_TC_001": "ui", "QA-9_TC_002": "ui"}


WITH_HTTP = dict(SCREENS, **{"QA-9_TC_003": "api"})


def t292_enter(driver, world, cases, accept=True):
    """`enter_manual`, but a raised `Person` is the result: (printed text, new dispatch id, the Person or None)."""
    import story_run
    import contextlib
    import io
    from unittest import mock
    before, out, person = set(world.dispatches), io.StringIO(), None
    try:
        with mock.patch("controller.Controller", world.controller_class()), contextlib.redirect_stdout(out):
            driver.run_manual_block(list(cases))
    except story_run.Person as raised:
        person = raised
    new = sorted(set(world.dispatches) - before)
    if accept:
        for dispatch_id in new:
            world.accept(dispatch_id)
            record_failure_analyst_accept(driver, dispatch_id)
    return out.getvalue(), (new[0] if new else ""), person


# --- HF2-11b: the live checks of the tests that changed after their run are proved again by code, before S6 closes -------
# The keys (spec t-120 section 3 "11b" as amended by section 10): K1 `s6_freshness` reads `proof_level.staleness` (the run rows'
# own shas move a result from `stand` to `run`; `probes` carries the stale live checks); K2 stale probes + every run standing +
# a stand -> one `probe_by_code.py` each BEFORE the reduction; K3 stale runs -> the runner with `complete=False`, the proofs on its
# return; K4 no stand (the WORD) -> no probe, a digest line; K5 nothing stale -> today's calls and digest; K6 40 tests from one
# fixture -> 40 in "run only", 40 probes, the time in the digest; K-P5 -> B-K1 (HF3-6): no running dispatch -> `--s6-close`,
# the tool is called; K-P9 a `replay` of None -> a digest line naming the instance. `staleness` itself is 11a's (test_run_freshness).

def pin_project(root):
    """`hooklib.project_root()` caches its answer for the life of the process and `proof_level` reads the test files under it; a
    driver test pins it to its own project and gives the old value back with `unpin_project`."""
    import hooklib
    saved = hooklib._PROJECT_ROOT_CACHE
    hooklib._PROJECT_ROOT_CACHE = Path(root).resolve()
    return saved


def unpin_project(saved) -> None:
    import hooklib
    hooklib._PROJECT_ROOT_CACHE = saved


def d1_blocks(root, task_root) -> None:
    """`d1_write_blocks` plus the test file the manifest names: since HF2-11b a result of a test whose file is gone does not
    stand (`run_freshness` rule 1), so the world of a result that stands has the file on disk."""
    d1_write_blocks(task_root)
    (Path(root) / "tests").mkdir(parents=True, exist_ok=True)
    (Path(root) / "tests" / "t.py").write_text("def test_a():\n    assert 1 == 1\n\n\ndef test_b():\n    assert 1 == 2\n", encoding="utf-8")


WHY_RUN = "the test, or a fixture or helper it uses, changed since run a1"


REPLAY_A = {"test": "tests/t.py::test_a", "instance": "test_a", "mutation": "invert", "oracle": ""}


REPLAY_B = {"test": "tests/t.py::test_b", "instance": "test_b", "mutation": "expected", "oracle": "tests/helpers.py::expected_total"}


ACCEPTED_S6 = {"S6-qa-runner-1": {"id": "S6-qa-runner-1", "stage": "S6", "status": "accepted", "execution_kind": "automation",
                                   "scope": ["TC-1", "TC-2"]}}


def row(run=("fresh", ""), probe=None) -> dict:
    """One instance of what `proof_level.staleness` answers."""
    return {"run": run, "probe": probe if probe is not None else {"state": "not_required", "why": "", "replay": None}}


def stale_probe(replay) -> dict:
    return {"state": "stale", "why": "the live check was measured on other code than the test holds now", "replay": replay}


class Staleness:
    """`proof_level.staleness` replaced for a block: `answer` is `{instance id: row}` (an id it does not name reads fresh and
    needs no live check) or the exception it raises; `calls` are the id lists the driver asked about."""

    def __init__(self, answer):
        self.answer, self.calls = answer, []

    def __enter__(self):
        import proof_level
        self.module, self.saved = proof_level, proof_level.staleness

        def fake(task_root, manifest, ids):
            self.calls.append(list(ids))
            if isinstance(self.answer, Exception):
                raise self.answer
            return {i: self.answer.get(i, row()) for i in ids}
        proof_level.staleness = fake
        return self

    def __exit__(self, *_exc):
        self.module.staleness = self.saved


def reprobe_rig(root, env, task, *, dispatches=None, mark=None, reply=None, manual=()):
    """`d1_driver` plus: the controller's dispatch table as given, the mark `s6_probe_after` as given (None = absent), every
    `probe_by_code.py` call recorded IN ORDER among the moves (`("probe", argv)`) and answered by `reply(argv)` (default: exit 0,
    `intended_failure`), and the `site` of every close by code. (driver, launched roles, moves, probe argvs, sites)."""
    driver, launched, moves, _started = d1_driver(root, env, task, manual=manual)
    probes, sites = [], []
    driver.controller_state = lambda: {"dispatches": dict(dispatches or {})}
    if mark is not None:
        driver.state["s6_probe_after"] = mark
    spied, real_close = driver.py, driver.close_by_code

    def py(script, *args, **kwargs):
        if script != "probe_by_code.py":
            return spied(script, *args, **kwargs)
        argv = [str(a) for a in args]
        probes.append(argv)
        moves.append(("probe", argv))
        return reply(argv) if reply else (0, json.dumps({"verdict": "intended_failure"}))
    driver.py = py
    driver.close_by_code = lambda *a, **k: (sites.append(k.get("site")) or real_close(*a, **k))
    return driver, launched, moves, probes, sites
