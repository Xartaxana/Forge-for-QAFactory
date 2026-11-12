"""The one git runner of the tools that READ, LIST, CLONE or CHECK OUT with git: `git(root, *args)` (B-class "git-top readers",
docs/SIBLING_MAP.md Axis 10, row "the one git runner"). exam_runner clones and checks out, and passes `timeout=None`:
a clone of a network URL has no fixed duration, and one killed at the default leaves a half-made folder behind.

Callers (each keeps its own decoding, error mapping and return shape):
    tools/piles.py                 git, git_show
    tools/compact_snapshot.py      run_git
    tools/forge_metrics.py         _run_git
    tools/r3_integration_check.py  _run_git
    tools/owns_verify.py           _git_repo_root, _run_git_name_only
    tools/exam_runner.py           _git, _git_rev_parse
    tools/install_parity.py        the eighth caller
    tools/ci_read.py               backend_for (origin URL; github-move GM1-4)
    tools/hygiene_gate.py          the rollback measurement (`git status`, timeout 5; imported when present)

NOT callers yet: the wrappers of the enforcement chain (tools/dispatch_gate.py, journal_validator.py, mechanism_gate.py,
journal_echo.py, session_context.py, hook_liveness_probe.py) and two more with their own git code
(tools/wiring_check.py `_run_git`, tools/dup_ratchet.py). They wait for forge batch 2, node F2-11, which decides
whether they move to this runner; gitcmd.py itself is already in MECHANISM_PREFIXES (tools/mechanism_gate.py).

Contract:
    root     the repository (`git -C root`), or None for the current directory (no -C).
    args     the git arguments after `git`; no args is a ValueError before anything runs.
    timeout  seconds, default 120.
    stderr   False (default) -> (returncode, stdout bytes); True -> (returncode, stdout bytes, stderr bytes).
    git missing or the process failing to start or timing out -> returncode -1 and the message as bytes (in stdout when
    stderr is False; in stderr, with empty stdout, when it is True). Never an exception for those.
`-c core.quotepath=false` is always on (a path listing is never octal-quoted); stdin is closed (a hook's stdin is never
read by git); no shell. Output is BYTES: decoding is the caller's -- a caller that wants TEXT the way `text=True` gave it
(UTF-8 with replacement, CRLF and CR read as LF) calls `as_text(raw)`, the one such chain (F-11); a caller with another
reading (utf-8-sig, NUL-split) keeps its own.
"""
from __future__ import annotations

import subprocess

DEFAULT_TIMEOUT = 120


def git(root, *args, timeout=DEFAULT_TIMEOUT, stderr=False):
    """Run `git [-C root] -c core.quotepath=false args...`; see the module docstring for the contract."""
    if not args:
        raise ValueError("gitcmd.git: expected at least one git argument, got none")
    argv = ["git"] + (["-C", str(root)] if root is not None else []) + ["-c", "core.quotepath=false", *args]
    try:
        proc = subprocess.run(argv, capture_output=True, timeout=timeout, stdin=subprocess.DEVNULL)
    except (OSError, subprocess.SubprocessError) as exc:
        message = str(exc).encode("utf-8", "replace")
        return (-1, b"", message) if stderr else (-1, message)
    return (proc.returncode, proc.stdout, proc.stderr) if stderr else (proc.returncode, proc.stdout)


def as_text(raw: bytes) -> str:
    """`raw` as text the way subprocess `text=True` read it: UTF-8 with U+FFFD for bad bytes, CRLF and lone CR as LF."""
    return raw.decode("utf-8", "replace").replace("\r\n", "\n").replace("\r", "\n")
