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
