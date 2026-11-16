#!/usr/bin/env python3
"""The machine lock of the journal writer (offload spec r2, §3.B5 D1; M3).

`machine_lock(name, timeout, repo=...)` -- a lock file `<git common dir>/forge-journal/<name>.lock`, shared by every
worktree of one clone and by every process of one computer. The common dir is the answer of
`git -C <dir> rev-parse --path-format=absolute --git-common-dir` (`<dir>` = `repo` or the cwd); a relative answer (a git
without `--path-format`) is resolved against `<dir>`, never against the repository root (S-3).

The file is opened `O_RDWR|O_CREAT` and never truncated. The LOCKED thing is one byte at offset 4096 (Windows:
`msvcrt.locking`, polled every 50 ms; elsewhere `fcntl.flock`, chosen by which module imports -- a capability). After
acquiring, the holder writes `pid ts` space-padded to 64 bytes at offset 0, OUTSIDE the locked byte, so another process can
read who holds the lock while it is held (Windows locks are mandatory). The OS releases the lock when the process dies.

Errors are two classes: `LockBusy` (timeout, exit 3 of the writer; its text names the holder) and `LockError` (git missing,
not a repository, the folder unwritable: exit 2). Never a line written without the lock is this module's invariant to the
caller: it raises, it does not fall through."""
from __future__ import annotations

import contextlib
import datetime
import os
import subprocess
import time
from pathlib import Path

try:                                  # a capability, not a platform test: the module that imports decides
    import msvcrt as _msvcrt
    _fcntl = None
except ImportError:                   # pragma: no cover -- the other branch of the same choice
    _msvcrt = None
    import fcntl as _fcntl

LOCK_DIR_NAME = "forge-journal"
LOCK_BYTE_OFFSET = 4096
HOLDER_BYTES = 64
POLL_SECONDS = 0.05
_STEERING_ENV = ("GIT_DIR", "GIT_COMMON_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_PREFIX")


class LockError(Exception):
    """The lock cannot even be attempted (no git, not a repository, the folder cannot be made)."""


class LockBusy(Exception):
    """The timeout ran out while another process held the lock; `str(exc)` is the one line the writer prints."""


def _git_env() -> dict:
    """The environment for a git call that must answer about a DIRECTORY: the variables that steer git to another
    repository (a hook's GIT_DIR / GIT_INDEX_FILE) are dropped, so the answer is the same in a hook and out of one."""
    return {k: v for k, v in os.environ.items() if k not in _STEERING_ENV}


def git_out(directory, *args: str) -> str:
    """The stdout (stripped) of `git -C <directory> <args>`; LockError naming the cause when it cannot be had."""
    try:
        proc = subprocess.run(["git", "-C", str(directory), *args], capture_output=True, timeout=60, env=_git_env())
    except FileNotFoundError:
        raise LockError("git is not installed or not on PATH (the journal lock lives in the git common dir)") from None
    except (OSError, subprocess.SubprocessError) as exc:
        raise LockError(f"git could not be run ({type(exc).__name__})") from None
    if proc.returncode != 0:
        why = proc.stderr.decode("utf-8", errors="replace").strip().splitlines()
        raise LockError(f"{directory} is not inside a git repository, or git refused ({why[-1][:120] if why else 'exit ' + str(proc.returncode)})")
    return proc.stdout.decode("utf-8", errors="replace").strip()


def common_dir(directory) -> Path:
    """The absolute git common dir of `directory` (one path for the root, a subfolder and every linked worktree)."""
    base = Path(directory).resolve()
    try:
        answer = git_out(base, "rev-parse", "--path-format=absolute", "--git-common-dir")
    except LockError:
        answer = git_out(base, "rev-parse", "--git-common-dir")      # a git without --path-format: resolve it ourselves
    lines = [ln.strip() for ln in answer.splitlines() if ln.strip()]
    if not lines:
        raise LockError(f"git gave no common dir for {base}")
    path = Path(lines[-1])                    # an old git echoes the unknown option first; the answer is the last line
    if not path.is_absolute():
        path = base / path                    # relative to <dir>, never to the repository root (S-3)
    path = path.resolve()
    if not path.is_dir():
        raise LockError(f"the git common dir {path} is not a directory")
    return path


def lock_dir(directory) -> Path:
    """`<common>/forge-journal/`, created when absent."""
    path = common_dir(directory) / LOCK_DIR_NAME
    try:
        path.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        raise LockError(f"{path} cannot be created ({type(exc).__name__})") from None
    return path


def lock_path(directory, name: str) -> Path:
    return lock_dir(directory) / f"{name}.lock"


def read_holder(path) -> str:
    """The text of bytes 0-63 of a lock file ("" when unreadable or never held); readable while another process holds it."""
    try:
        with open(path, "rb", buffering=0) as handle:      # unbuffered: a buffered read of 8 KB would cross the locked byte
            return handle.read(HOLDER_BYTES).decode("utf-8", errors="replace").strip()
    except OSError:
        return ""


def _busy_text(path) -> str:
    holder = read_holder(path).split(None, 1)
    if len(holder) == 2 and holder[0].isdigit():
        return f"journal busy: held by pid {holder[0]} since {holder[1]}"
    return "journal busy: held by another process"


def _try_lock(fd: int) -> bool:
    try:
        if _msvcrt is not None:
            os.lseek(fd, LOCK_BYTE_OFFSET, os.SEEK_SET)
            _msvcrt.locking(fd, _msvcrt.LK_NBLCK, 1)
        else:
            _fcntl.flock(fd, _fcntl.LOCK_EX | _fcntl.LOCK_NB)
        return True
    except OSError:
        return False


def _unlock(fd: int) -> None:
    try:
        if _msvcrt is not None:
            os.lseek(fd, LOCK_BYTE_OFFSET, os.SEEK_SET)
            _msvcrt.locking(fd, _msvcrt.LK_UNLCK, 1)
        else:
            _fcntl.flock(fd, _fcntl.LOCK_UN)
    except OSError:
        pass


def _write_holder(fd: int) -> None:
    text = f"{os.getpid()} {datetime.datetime.now().isoformat(timespec='seconds')}"
    os.lseek(fd, 0, os.SEEK_SET)
    os.write(fd, text.encode("ascii", errors="replace")[:HOLDER_BYTES].ljust(HOLDER_BYTES, b" "))


@contextlib.contextmanager
def machine_lock(name: str, timeout: float, *, repo=None):
    """Hold the machine lock `name` for the body. `repo`: a directory of the clone (default: the cwd). Raises LockBusy after
    `timeout` seconds and LockError when the lock file cannot be had; releases on exit and on exception."""
    path = lock_path(repo if repo is not None else Path.cwd(), name)
    try:
        fd = os.open(path, os.O_RDWR | os.O_CREAT | getattr(os, "O_BINARY", 0), 0o644)
    except OSError as exc:
        raise LockError(f"{path} cannot be opened ({type(exc).__name__})") from None
    deadline = time.monotonic() + max(0.0, timeout)
    try:
        while not _try_lock(fd):
            if time.monotonic() >= deadline:
                raise LockBusy(_busy_text(path))
            time.sleep(POLL_SECONDS)
        try:
            _write_holder(fd)
            yield path
        finally:
            with contextlib.suppress(OSError):
                os.lseek(fd, 0, os.SEEK_SET)
                os.write(fd, b" " * HOLDER_BYTES)      # nobody reads a stale holder after the release
            _unlock(fd)
    finally:
        os.close(fd)
