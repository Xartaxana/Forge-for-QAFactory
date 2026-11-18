#!/usr/bin/env python3
"""The driver's refusals, with `claude` replaced by a stub (STORY_RUN_CLAUDE) and a temp project.

Nothing here reaches the network or a real model. What is proved:
  * a stage round trip and the gate: start -> role -> bind -> handoff check -> finish, the question file
    and exit 3, the person's answer recorded by code, and a refusal the known table handles never
    reaching the conductor while an unknown one goes to it;
  * the known-refusal table, its markers and the dispatch field a refusal carries;
  * the judge's reading of the person's words, and how a source gap is asked and closed;
  * every action the controller can return has a move on the driver's side;
  * an active sequential dispatch is a known refusal the driver answers itself;
  * the stage in front of a gate that `stage_done` refuses to record (t-211 F0, mutation M11) is gone over by
    the driver itself, and only while the controller holds that stage `completed`.
The shared scaffolding lives in `story_run_common.py`.
"""
# Shared helpers of test_story_run_refusals.py, split by tools/test_split.py (TD-11c).
import contextlib
import io
import json
import os
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from harness import check_eq  # noqa: E402
from story_run_common import d2_pipeline, driver_for, seed, set_control


def recording_stub(result=True, calls=None):
    """A stand-in for `Driver.record_by_code` that takes ANY call (`*args, **kwargs`) and returns `result`: a signature the real
    method grows (C2-7 added `apply_words`) never breaks the test or silently drops an argument (FR-31, C4-14). The call is kept
    in `calls` (when given) as `{kind, stage, words, <the keywords given>}`."""
    def fake(*args, **kwargs):
        if calls is not None:
            calls.append({**dict(zip(("kind", "stage", "words"), args)), **kwargs})
        return result
    return fake


def git_fixture(root: Path):
    """A local bare 'remote' and a checkout of it under the temp project (nothing reaches a network):
    main holds A (TP1-100, an older commit of the ticket prefix) and B; `feat` adds C (TP1-15045),
    and the remote lists C as refs/merge-requests/1924/head. Returns (checkout, {"A","B","C"} full ids)."""
    import subprocess
    env = dict(os.environ, GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t", GIT_COMMITTER_NAME="t",
               GIT_COMMITTER_EMAIL="t@t")

    def git(cwd, *args):
        done = subprocess.run(["git", "-C", str(cwd), *args], capture_output=True, text=True, env=env, timeout=60)
        check_eq(f"fixture: git {' '.join(args[:2])}", done.returncode, 0)
        return done.stdout.strip()

    remote, app = root / "remote.git", root / "app"
    subprocess.run(["git", "init", "-q", "--bare", str(remote)], check=True, capture_output=True)
    subprocess.run(["git", "init", "-q", str(app)], check=True, capture_output=True)
    git(app, "checkout", "-q", "-b", "main")
    (app / "a.txt").write_text("a", encoding="utf-8")
    git(app, "add", "-A")
    git(app, "commit", "-q", "-m", "TP1-100 an older change of the ticket prefix")
    a = git(app, "rev-parse", "HEAD")
    (app / "b.txt").write_text("b", encoding="utf-8")
    git(app, "add", "-A")
    git(app, "commit", "-q", "-m", "an unrelated change")
    b = git(app, "rev-parse", "HEAD")
    git(app, "checkout", "-q", "-b", "feat")
    (app / "c.txt").write_text("c", encoding="utf-8")
    git(app, "add", "-A")
    git(app, "commit", "-q", "-m", "TP1-15045 draft evaluation tests")
    c = git(app, "rev-parse", "HEAD")
    git(app, "remote", "add", "origin", str(remote))
    git(app, "push", "-q", "origin", "main", "feat", f"{c}:refs/merge-requests/1924/head")
    return app, {"A": a, "B": b, "C": c}


# --- t-217 / F-cmp2-23: the role is resumed once per finding set, then the stand, then the person -----------------------
RES_DISPATCH = "S5-qa-automator-1"


# What cmp2's S5 automator answered with (cmp2-19): every case "blocked_by_env", the stand was down while it worked.
RES_DIGEST = ("qa-automator S5 TC-1 · concerns\nTC-1 · blocked_by_env · tests written, not run: stand down\n"
              "work/automation-manifest.json")


RES_PLAIN = "qa-automator S5 TC-1 · concerns\nTC-1 · ok · written and run\nwork/automation-manifest.json"


def res_errors(*names: str) -> list:
    """Exit-gate errors that carry the repair marker, the way s5_precheck words them (cmp2-19)."""
    import story_run
    return [f"s5_precheck.py: {name}: the review receipt is missing. {story_run.REPAIR_MARKER}" for name in names]


def res_fixture(task: str = "QA-9", digest: str = RES_DIGEST, *, environment="local"):
    """A seeded project with the role's saved result on disk, as `wait_existing_job` meets it on every entry."""
    root, task_root, env = seed(task)
    saved = task_root / "state" / "driver-runs" / f"{RES_DISPATCH}.json"
    saved.parent.mkdir(parents=True, exist_ok=True)
    saved.write_text(json.dumps({"session_id": "sess-a", "result": digest, "is_error": False, "exit_code": 0,
                                 "stderr": "", "num_turns": 3}), encoding="utf-8")
    d2_pipeline(task_root, environment=environment)
    set_control(root, {"resume": {"result": digest}})
    return root, task_root, env


def res_driver(root, env, task: str, errors: list, probe=(0, "liveness: alive - http://localhost:5173 -> HTTP 200")):
    """A driver over the same project whose exit gate answers `errors` and whose stand probe answers `probe`.
    (driver, the probe calls). `claude` is the stub: a resume is a `resume` line in the stub's log."""
    driver = driver_for(root, env, task)
    driver.state["sessions"][RES_DISPATCH] = "sess-a"
    driver.exit_errors = lambda role, digest, dispatch=None: list(errors)
    driver.form_errors = lambda dispatch: []
    driver.controller_state = lambda: {"dispatches": {RES_DISPATCH: {"stage": "S5", "role": "qa-automator",
                                                                      "scope": ["TC-1"]}}}
    real_py, probes = driver.py, []

    def py(script, *args, **kwargs):
        if script == "env_probe.py":
            probes.append([str(a) for a in args])
            return probe
        return real_py(script, *args, **kwargs)
    driver.py = py
    return driver, probes


def res_entry(driver):
    """One entry the way the loop makes it: `where` says wait_existing_job, the move runs under `guarded`.
    The Person it raised, or None."""
    import story_run
    action = {"action": "wait_existing_job", "dispatch_id": RES_DISPATCH, "stage": "S5"}
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            driver.guarded(lambda: driver.dispatch_action(action), action)
    except story_run.Person as person:
        return person
    return None
