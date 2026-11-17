"""The one no-reaper wrapper for tests that run a hook (session_context.py, dod_gate.py) as a subprocess.

A hook run under a real session would start a real `wait_reaper --apply` against it. The wrapper replaces wait_reaper.launch by
a silent one, then runs the script as __main__. Plain module: imports nothing from conftest."""

import sys
from pathlib import Path

WRAP = ("import runpy, sys; sys.path.insert(0, sys.argv[2])\n"
        "try:\n    import wait_reaper; wait_reaper.launch = lambda *a, **k: None\nexcept ImportError:\n    pass\n"
        "sys.argv = [sys.argv[1]]; runpy.run_path(sys.argv[0], run_name='__main__')")


def hook_argv(script) -> list:
    """The argv that runs `script` as __main__ with no reaper: `python -c WRAP <script> <script's folder>`."""
    script = Path(script).resolve()
    return [sys.executable, "-c", WRAP, str(script), str(script.parent)]


def isolated_hook_argv(script, root, env_name="SESSION_CONTEXT_PATH") -> list:
    """Like hook_argv, but the script runs from a COPY at `<root>/tools/<name>`, so its repo root (parent of its folder) is
    `root`, a tmp dir: the hook never scans the real repo (its quarantine scan alone takes ~20 s). The file copied is the one
    under test: the path in env var `env_name` when set (relative paths against the cwd), else `script`."""
    import os
    import shutil
    cand = os.environ.get(env_name)
    src = Path(cand) if cand else Path(script)
    src = src if src.is_absolute() else Path.cwd() / src
    dst = Path(root) / "tools" / Path(script).name
    dst.parent.mkdir(parents=True, exist_ok=True)
    for sib in Path(__file__).resolve().parent.glob("*.py"):  # the hook's sibling modules; test_*.py stay out (fail-open lines)
        if not sib.name.startswith("test_"):
            shutil.copyfile(sib, dst.parent / sib.name)
    pkg = Path(__file__).resolve().parent.parent / "ai-packages" / "qa-factory" / "scripts"  # journal_write's PACKAGE_SCRIPTS
    if pkg.is_dir():
        (Path(root) / "ai-packages" / "qa-factory" / "scripts").mkdir(parents=True, exist_ok=True)
        for sib in pkg.glob("*.py"):
            shutil.copyfile(sib, Path(root) / "ai-packages" / "qa-factory" / "scripts" / sib.name)
    shutil.copyfile(src, dst)
    return hook_argv(dst)
