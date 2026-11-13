"""The one git runner of the tools, and the two readers built on it: `git(root, *args)` runs git for tools that read, list, clone,
check out OR CHANGE a repository (worktree_sweep removes worktrees, writes and deletes refs); `main_checkout(root)` is the one
resolver of the main checkout; `parse_status_z(raw)` is the one reader of `status --porcelain=v1 -z`
(docs/SIBLING_MAP.md Axis 10, row "the one git runner"). exam_runner clones and checks out, and passes `timeout=None`:
a clone of a network URL has no fixed duration, and one killed at the default leaves a half-made folder behind.

Callers: `grep -l "import gitcmd" tools/*.py`; the enumeration with each caller's function lives in docs/SIBLING_MAP.md axis 10.
Each caller keeps its own decoding, error mapping and return shape.
Git wrappers left on their own code are named on axis 10 (the decision of forge node F2-11, accepted 6fe68a64).
gitcmd.py itself is in MECHANISM_PREFIXES (tools/mechanism_gate.py).

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
    main_checkout(root, *, runner=None, timeout=DEFAULT_TIMEOUT) -> (Checkout | None, code, why); never raises (a runner that
    raises included). code is "" on success, else "git" (failed to run, rc != 0, fewer than two lines), "resolve" (a git dir
    does not resolve) or "not-a-checkout" (the common dir is not named `.git`: no guessed main worktree).
    parse_status_z(raw) -> [(xy, path)]; raw is bytes or str; never raises; errs only toward MORE entries.
"""
from __future__ import annotations

import os
import subprocess
from pathlib import Path
from typing import NamedTuple

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


class Checkout(NamedTuple):
    git_dir: Path
    common: Path
    path: Path
    linked: bool


def _first_line(text: str) -> str:
    lines = [l.strip() for l in (text or "").strip().splitlines() if l.strip()]
    return lines[0] if lines else "no message"


def main_checkout(root, *, runner=None, timeout=DEFAULT_TIMEOUT):
    """The main checkout of the repository `root` belongs to: (Checkout | None, code, why). Never raises. A relative answer of
    git is relative to root; a common dir not named `.git` has no checkout beside it (not guessed). `linked` is True when
    `root` is a linked worktree (git dir differs from the common dir)."""
    run = runner or git
    try:
        rc, out, err = run(root, "rev-parse", "--git-dir", "--git-common-dir", timeout=timeout, stderr=True)
        text = as_text(out)
        err_text = as_text(err)
    except Exception as exc:
        return None, "git", "git rev-parse raised %s" % type(exc).__name__
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    if rc != 0 or len(lines) < 2:
        if rc == -1:
            return None, "git", "git rev-parse failed to run (%s)" % _first_line(err_text)
        return None, "git", "git rev-parse exited %s (%s)" % (rc, _first_line(err_text or text))
    base = Path(str(root)) if root is not None else Path(".")
    resolved = []
    for line in lines[:2]:
        p = Path(line)
        p = p if p.is_absolute() else base / p
        try:
            resolved.append(p.resolve())
        except (OSError, ValueError):     # ValueError: a NUL in the path
            return None, "resolve", "git dir %s does not resolve" % line
    git_dir, common = resolved
    if common.name != ".git":
        return None, "not-a-checkout", "git common dir %s is not a .git directory of a checkout" % common
    linked = os.path.normcase(os.path.realpath(str(git_dir))) != os.path.normcase(os.path.realpath(str(common)))
    return Checkout(git_dir, common, common.parent, linked), "", ""


def parse_status_z(raw):
    """`git status --porcelain=v1 -z` output -> [(xy, path)]; bytes or str. A rename or copy carries its origin as the next NUL
    field (consumed). Plain UTF-8 replace, not `as_text`: a CR inside a path survives. Never raises."""
    text = raw.decode("utf-8", "replace") if isinstance(raw, (bytes, bytearray)) else str(raw)
    parts = text.split("\0")
    out, i = [], 0
    while i < len(parts):
        rec = parts[i]
        i += 1
        if len(rec) < 4:
            continue
        xy, path = rec[:2], rec[3:]
        out.append((xy, path))
        if "R" in xy or "C" in xy:
            i += 1
    return out
