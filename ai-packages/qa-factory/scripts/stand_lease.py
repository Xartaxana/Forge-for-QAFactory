"""One run at a time on a stand that cannot take two — a project-level lease on the stand.

Why. TP1-15045, 2026-09-21: the project's config said `run.parallel: false` (one
account on the stand; a second login ends the first session), and the code critic still
started five UI runs within the same two seconds. All five failed — four on
`Locator.fill: Timeout` in setup — and the next automator dispatch ($8.08, 62 minutes) was
spent proving the tests were not to blame. `run.parallel` was a fact every role had to
remember; a fact the factory knows is a fact the factory enforces.

`run_suite.py` wraps the execution of a request in `hold()`. The second request does not
fail and is not refused: it waits in line (`waited_s` lands in its summary), and only after
`wait_s` does it give up with `StandBusy`, having launched nothing.

The lease is a record in `qa-factory/state/stand-lease.json`, one per environment name,
written atomically under the same OS file lock the scheduler's lease registry uses. A lease
whose process is gone is taken over and the takeover is noted in the file: a killed runner
must never close the stand for the rest of the day.

A person's word passes this block: `stand_lease.py --release --env NAME --reason "..."`
removes a lease the person knows to be dead or wrong, and the reason is kept in the file.

Usage:
    stand_lease.py --status [--project-root DIR]
    stand_lease.py --release [--env NAME] --reason "why" [--project-root DIR]
    stand_lease.py --selftest
"""
from __future__ import annotations

import argparse
import contextlib
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

DEFAULT_WAIT_S = 1800
DEFAULT_ENVIRONMENT = "default"
NOTES_KEPT = 20

# Injectable for tests: nothing here may really sleep five seconds in a unit test.
_sleep = time.sleep
_monotonic = time.monotonic


class StandBusy(Exception):
    """The stand stayed leased for the whole allowed wait. `holder` is the lease record."""

    def __init__(self, holder: dict, waited_s: int = 0, environment: str = DEFAULT_ENVIRONMENT):
        self.holder = dict(holder or {})
        self.waited_s = int(waited_s)
        self.environment = environment
        super().__init__(
            f"the stand `{environment}` is still held by run {self.holder.get('job_id') or '?'} "
            f"(pid {self.holder.get('pid') or '?'}, since {self.holder.get('acquired_at') or '?'}) "
            f"after waiting {self.waited_s}s; nothing was launched. Start the run again when that "
            "one finishes. If that run is known to be gone, a person releases the stand: "
            f"stand_lease.py --release --env {environment} --reason \"...\"")


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _paths(project_root) -> tuple[Path, Path]:
    path = Path(project_root) / "qa-factory" / "state" / "stand-lease.json"
    return path, path.with_suffix(".lock")


def _env_name(environment) -> str:
    return str(environment or "").strip() or DEFAULT_ENVIRONMENT


def configured_wait_s(project_root) -> int:
    """`run.stand_wait_s` from qa-factory/config.json; optional, so a 0.7.x project keeps working."""
    try:
        config = json.loads((Path(project_root) / "qa-factory" / "config.json")
                            .read_text(encoding="utf-8-sig"))
        value = (config.get("run") or {}).get("stand_wait_s")
        if isinstance(value, (int, float)) and not isinstance(value, bool) and value >= 0:
            return int(value)
    except (OSError, ValueError, AttributeError, TypeError):
        pass
    return DEFAULT_WAIT_S


def _holder_state(lease: dict) -> str:
    """`alive`, `gone`, or `unknown` — what is actually known about the holder's process.

    The scheduler's identity check (pid + birth time) is proof either way: a recycled pid is not
    the holder. Without a recorded birth time there is nothing to compare, so a pid that answers
    is `unknown` and not `alive` — the run may be long finished and its number reused. The
    DECISION does not change (see `_holder_alive`): an unknown holder keeps the stand, because
    taking it from a live run recreates the incident this module exists for. What changes is the
    report, which no longer states as a fact something nobody measured (FR-41).
    """
    try:
        pid = int(lease.get("pid") or 0)
    except (TypeError, ValueError):
        pid = 0
    if pid <= 0:
        return "gone"
    started = str(lease.get("process_started_at") or "")
    try:
        if started:
            from execution_scheduler import _same_process
            return "alive" if _same_process(pid, started) else "gone"
        import run_suite
        return "unknown" if run_suite.pid_alive(pid) else "gone"
    except Exception:
        return "unknown"


def _holder_alive(lease: dict) -> bool:
    """Does this lease still hold the stand? Anything but proof that the holder is gone does."""
    return _holder_state(lease) != "gone"


def _identity(pid: int) -> str:
    try:
        from execution_scheduler import _started
        return _started(pid)
    except Exception:
        return ""


@contextlib.contextmanager
def _locked(lock_path: Path):
    from execution_scheduler import _file_lock
    with _file_lock(lock_path):
        yield


def _read(path: Path) -> dict:
    """A corrupt file is an empty one: a half-written lease must not close the stand."""
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(value, dict) and isinstance(value.get("leases"), dict):
            value.setdefault("notes", [])
            if not isinstance(value["notes"], list):
                value["notes"] = []
            return value
    except (OSError, ValueError):
        pass
    return {"schema_version": 1, "leases": {}, "notes": []}


def _write(path: Path, state: dict) -> None:
    from event_store import atomic_json
    state["notes"] = list(state.get("notes") or [])[-NOTES_KEPT:]
    state["updated_at"] = _now()
    atomic_json(path, state)


def _try_acquire(project_root, job_id: str, environment: str) -> tuple[str, dict]:
    """One attempt. Returns `(outcome, record)`: acquired | reentered | busy, and the holder
    (busy), the taken-over lease (acquired after a takeover) or `{}`."""
    path, lock_path = _paths(project_root)
    with _locked(lock_path):
        state = _read(path)
        current = state["leases"].get(environment)
        taken_over = {}
        if isinstance(current, dict) and current:
            if str(current.get("job_id") or "") == job_id and int(current.get("pid") or 0) == os.getpid():
                return "reentered", {}
            if _holder_alive(current):
                return "busy", dict(current)
            taken_over = dict(current)
            state["notes"].append({
                "at": _now(), "event": "takeover", "environment": environment, "by": job_id,
                "from": current.get("job_id"), "dead_pid": current.get("pid"),
                "held_since": current.get("acquired_at")})
        state["leases"][environment] = {
            "job_id": job_id, "environment": environment, "pid": os.getpid(),
            "process_started_at": _identity(os.getpid()), "acquired_at": _now()}
        _write(path, state)
        return "acquired", taken_over


def _release(project_root, job_id: str, environment: str) -> None:
    path, lock_path = _paths(project_root)
    with _locked(lock_path):
        state = _read(path)
        current = state["leases"].get(environment)
        # Only our own lease: after a takeover the record belongs to somebody else.
        if (isinstance(current, dict) and str(current.get("job_id") or "") == job_id
                and int(current.get("pid") or 0) == os.getpid()):
            del state["leases"][environment]
            _write(path, state)


@contextlib.contextmanager
def hold(project_root, job_id: str, environment: str = "", wait_s: int = DEFAULT_WAIT_S,
         poll_s: int = 5):
    """Hold the stand for the duration of the block.

    Yields `{"waited_s": int, "queued_behind": job_id|None, "environment": name}` plus
    `took_over` when a dead holder's lease was taken and `lease_error` when the lease file
    itself could not be used. Raises `StandBusy` (with `.holder`) when the stand stayed
    leased for `wait_s` seconds; `wait_s=None` reads `run.stand_wait_s` from the config.

    A broken lease FILE never stops a run: the defect would be the factory's own, and the
    person's tests would be the ones not running. The run proceeds unprotected and says so.
    """
    job_id = str(job_id or "") or f"pid-{os.getpid()}"
    env = _env_name(environment)
    limit = configured_wait_s(project_root) if wait_s is None else max(0, int(wait_s))
    began = _monotonic()
    queued_behind = None
    result = {"waited_s": 0, "queued_behind": None, "environment": env}
    outcome = "unprotected"
    while True:
        try:
            outcome, record = _try_acquire(project_root, job_id, env)
        except Exception as exc:  # lock or disk trouble: the factory's defect, not the run's
            outcome, record = "unprotected", {}
            result["lease_error"] = f"{type(exc).__name__}: {exc}"
        if outcome != "busy":
            if record:
                result["took_over"] = {"job_id": record.get("job_id"), "pid": record.get("pid"),
                                       "acquired_at": record.get("acquired_at")}
            break
        if queued_behind is None:
            queued_behind = str(record.get("job_id") or "") or None
        waited = _monotonic() - began
        if waited >= limit:
            raise StandBusy(record, int(waited), env)
        _sleep(max(0.0, min(float(poll_s), limit - waited)))
    # Only a run that was kept in line has waited; the time a free stand took to be taken (cold
    # imports, a slow disk, a loaded machine) is not waiting and must not read as 1 s.
    result["waited_s"] = int(round(_monotonic() - began)) if queued_behind is not None else 0
    result["queued_behind"] = queued_behind
    try:
        yield result
    finally:
        if outcome == "acquired":
            try:
                _release(project_root, job_id, env)
            except Exception:
                pass  # a dead holder's lease is taken over by the next run; never mask the run's own error


def status(project_root) -> dict:
    """Every lease with a verdict on its holder. Read-only: nothing is taken over here."""
    path, lock_path = _paths(project_root)
    try:
        with _locked(lock_path):
            state = _read(path)
    except Exception as exc:
        return {"leases": [], "notes": [], "error": f"{type(exc).__name__}: {exc}"}
    rows = []
    for name, lease in sorted(state["leases"].items()):
        if isinstance(lease, dict):
            rows.append({**lease, "environment": name, "holder": _holder_state(lease)})
    return {"leases": rows, "notes": state.get("notes") or []}


def release_by_person(project_root, environment: str, reason: str) -> dict:
    """A person's decision to free the stand, kept with its reason."""
    env = _env_name(environment)
    path, lock_path = _paths(project_root)
    with _locked(lock_path):
        state = _read(path)
        lease = state["leases"].pop(env, None)
        if lease is None:
            return {"status": "not_held", "environment": env}
        state["notes"].append({"at": _now(), "event": "released_by_person", "environment": env,
                               "from": lease.get("job_id"), "reason": reason})
        _write(path, state)
    return {"status": "released", "environment": env, "released": lease}


def selftest() -> int:
    import shutil
    import tempfile
    global _sleep
    root = Path(tempfile.mkdtemp(prefix="qa-stand-lease-"))
    failures = 0

    def case(name, ok):
        nonlocal failures
        failures += 0 if ok else 1
        print(("PASS " if ok else "FAIL ") + name)

    real_sleep = _sleep
    try:
        _sleep = lambda _s: None  # noqa: E731
        with hold(root, "job-a", "", wait_s=0) as lease:
            case("a free stand is taken without waiting", lease["waited_s"] == 0 and lease["queued_behind"] is None)
            case("the lease is on disk", status(root)["leases"][0]["job_id"] == "job-a")
            try:
                with hold(root, "job-b", "", wait_s=0, poll_s=0):
                    case("a second run is kept out", False)
            except StandBusy as busy:
                case("a second run is kept out", busy.holder.get("job_id") == "job-a")
            with hold(root, "job-c", "other-stand", wait_s=0):
                case("another environment has its own lease", len(status(root)["leases"]) == 2)
        case("the lease is released", status(root)["leases"] == [])
        path, _ = _paths(root)
        _write(path, {"schema_version": 1, "notes": [], "leases": {DEFAULT_ENVIRONMENT: {
            "job_id": "dead", "pid": 0, "process_started_at": "", "acquired_at": _now()}}})
        with hold(root, "job-d", "", wait_s=0) as lease:
            case("a dead holder is taken over", (lease.get("took_over") or {}).get("job_id") == "dead")
        case("the takeover is noted", any(n.get("event") == "takeover" for n in status(root)["notes"]))
    finally:
        _sleep = real_sleep
        shutil.rmtree(root, ignore_errors=True)
    print(f"\n=== stand_lease selftest: {'ok' if not failures else str(failures) + ' failed'} ===")
    return 1 if failures else 0


def main() -> None:
    parser = argparse.ArgumentParser(description="The project's stand lease")
    parser.add_argument("--project-root", type=Path)
    parser.add_argument("--status", action="store_true")
    parser.add_argument("--release", action="store_true")
    parser.add_argument("--env", default="")
    parser.add_argument("--reason", default="")
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args()
    if args.selftest:
        raise SystemExit(selftest())
    if args.project_root:
        root = args.project_root.resolve()
    else:
        from hooklib import project_root
        root = project_root()
    if args.release:
        if not args.reason.strip():
            parser.error("--release needs --reason: the person's decision is kept with its reason")
        print(json.dumps(release_by_person(root, args.env, args.reason.strip()), ensure_ascii=False))
        return
    if args.status:
        print(json.dumps(status(root), ensure_ascii=False, indent=1))
        return
    parser.error("--status, --release or --selftest is required")


if __name__ == "__main__":
    main()
