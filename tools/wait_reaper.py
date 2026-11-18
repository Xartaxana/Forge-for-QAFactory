"""Stop the tool-call trees of THIS session that have outlived the limit (bounded-waits spec r2 section 5; card K-REAP).

    python -B tools/wait_reaper.py [--apply] [--limit <s>] [--trigger <t>] [--session-pid <p> --session-created <iso>]
                                   [--orphans] [--pid <root>] [--repo <path>]

Default: a dry list (nothing locked, logged or stopped). `--apply` stops. A CANDIDATE is a tree whose root is a direct child of
this session's process (`tools/session_proc.py`: pid AND creation time), created after it, a harness tool-call wrapper (data
rows of `tools/wait-reaper.json`), older than `limit_seconds` strictly; no process of the tree is a `never_reap` row, and the
reaper and its ancestors are never in one. A parent link counts only when the parent was created BEFORE the child (F-R3), so an
orphan never joins a tree. Stop = per pid `OpenProcess` + creation time read on THAT handle (1 s tolerance) +
`TerminateProcess`, root first (the loop shell cannot start the next `sleep`), one attempt per pid per run, no child process.
With no session nothing is stopped. The process list is read by one detached PowerShell CIM call (CREATE_NO_WINDOW, 20 s) --
never on the hook path: hooks call `launch`, which walks in-process and spawns this tool detached.

Files (`<git common dir>/wait-reaper/`): `run.log` shared; per session `<pid>-<yyyymmddHHMMSS>/{lock,status.json}`.
Exit: 0 done / no session / busy; 1 cannot work (broken wait-reaper.json, unreadable process list, no repository); 2 bad arguments.
"""
from __future__ import annotations

import argparse
import calendar
import dataclasses
import functools
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

_TOOLS = Path(__file__).resolve().parent
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))

import session_proc  # noqa: E402
import worktree_sweep as ws  # noqa: E402
import ascii_line  # noqa: E402  the one ASCII line helper (FG7-56), a stdlib leaf; plain sibling import (card F2 b)

STATE_DIRNAME = "wait-reaper"
DECODE_CAP = 65536                   # a command line over this is cut before decoding (the cut makes the decode fail, never widen)
CMD_LOG_MAX = 2000
KID_CMD_MAX = 200
KIDS_MAX = 20
PID_TOLERANCE_S = 1.0                # creation read on the handle vs the listed one; a candidate is > limit old, a reused pid is younger
LIST_TIMEOUT_S = 20
REASON_MAX = 120
CREATE_NO_WINDOW = 0x08000000
_IS_WINDOWS = os.name == "nt"
PS_LIST = ("Get-CimInstance Win32_Process | Select-Object ProcessId,ParentProcessId,Name,CreationDate,CommandLine "
           "| ConvertTo-Json -Compress")
ACCESS_DENIED = 5                    # TerminateProcess on a process that is exiting reads this
GONE_CODES = (87, 2, 3)              # ERROR_INVALID_PARAMETER (no such pid), ENOENT, ESRCH


class ListError(Exception):
    """The process list could not be read; the message is the reason (ASCII, clipped by the caller)."""


ascii_clip = functools.partial(ascii_line.clip, control=" ", strip=False, none="")  # the reaper profile; n is required


# --------------------------------------------------------------------------------------------------------- the process list

_MS_DATE = re.compile(r"^\\?/Date\((-?\d+)(?:[+-]\d{4})?\)\\?/$")
_CIM_DATE = re.compile(r"^(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})\.(\d{6})([+-])(\d{3})$")


def parse_cim_date(value):
    """Epoch seconds (UTC) or None. Three shapes: Windows PowerShell JSON `/Date(ms)/` (ms are UTC, an offset suffix is not
    applied), the raw CIM string `yyyymmddHHMMSS.ffffff+mmm` (local time, offset in MINUTES: UTC = local - offset), ISO text."""
    if isinstance(value, dict):
        value = value.get("value")
    if not isinstance(value, str):
        return None
    value = value.strip()
    m = _MS_DATE.match(value)
    if m:
        return int(m.group(1)) / 1000.0
    m = _CIM_DATE.match(value)
    if m:
        y, mo, d, h, mi, s, us = (int(g) for g in m.groups()[:7])
        offset = int(m.group(9)) * (1 if m.group(8) == "+" else -1)
        try:
            return calendar.timegm((y, mo, d, h, mi, s)) - offset * 60 + us / 1e6
        except (ValueError, OverflowError):
            return None
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return dt.timestamp()
    except (ValueError, OverflowError, OSError):
        return None


def parse_list(text):
    """The CIM JSON as a list of {pid, ppid, name, created, cmd}; ListError when it is not one."""
    try:
        data = json.loads((text or "").lstrip("﻿"))
    except ValueError:
        raise ListError("process list is not JSON")
    if isinstance(data, dict):
        data = [data]
    if not isinstance(data, list):
        raise ListError("process list is not a JSON list")
    procs = []
    for item in data:
        if not isinstance(item, dict):
            continue
        try:
            pid, ppid = int(item["ProcessId"]), int(item.get("ParentProcessId") or 0)
        except (KeyError, TypeError, ValueError):
            continue
        procs.append({"pid": pid, "ppid": ppid, "name": str(item.get("Name") or ""),
                      "created": parse_cim_date(item.get("CreationDate")), "cmd": str(item.get("CommandLine") or "")})
    return procs


def list_processes(run=subprocess.run):
    """One CIM read, hidden console, 20 s. `run` is the seam (a test passes a fake with subprocess.run's shape)."""
    kw = {"capture_output": True, "timeout": LIST_TIMEOUT_S}
    if _IS_WINDOWS:
        kw["creationflags"] = CREATE_NO_WINDOW
    try:
        res = run(["powershell", "-NoProfile", "-NonInteractive", "-Command", PS_LIST], **kw)
    except subprocess.TimeoutExpired:
        raise ListError("timed out after %d s" % LIST_TIMEOUT_S)
    except OSError as exc:
        raise ListError("cannot start powershell (%s)" % type(exc).__name__)
    if res.returncode != 0:
        err = (res.stderr or b"").decode("utf-8", errors="replace").strip().splitlines()
        raise ListError("powershell exit %d: %s" % (res.returncode, err[0] if err else "no message"))
    return parse_list((res.stdout or b"").decode("utf-8", errors="replace"))


# --------------------------------------------------------------------------------------------------------- wrappers

def decode_bash_eval(cmd):
    """The user command inside the Bash wrapper `... eval '<cmd>' < /dev/null && pwd -P >| ...`: the single-quoted word, with the
    splices `'\\''` and `'"'"'` re-joined, a Windows-escaped `\\"` restored. None when the shape is not exactly that (a log aid and
    a shape label only: a failed decode never widens a stop)."""
    text = (cmd or "")[:DECODE_CAP]
    snap = text.find("snapshot-bash-")
    start = text.find("eval '", snap if snap >= 0 else 0)
    end = text.rfind("' < /dev/null")
    if start < 0 or end <= start + 5:
        return None
    body, out, i = text[start + 6:end], [], 0
    while True:
        j = body.find("'", i)
        if j < 0:
            out.append(body[i:])
            break
        out.append(body[i:j])
        if body[j + 1:j + 4] == "\\''":
            out.append("'")
            i = j + 4
        elif body[j + 1:j + 5] == "\"'\"'":
            out.append("'")
            i = j + 5
        else:
            return None
    return "".join(out).replace('\\"', '"')


_DECODERS = {"bash-eval": decode_bash_eval}


def match_wrapper(proc, rows):
    """The `wrapper_forms` row the process matches, or None. Name and every `contains` text (case-insensitive)."""
    name, cmd = proc["name"].lower(), proc["cmd"].lower()
    if name not in [str(n).lower() for n in rows["tool_call_roots"]]:
        return None
    for row in rows["wrapper_forms"]:
        if str(row.get("name", "")).lower() == name and all(str(t).lower() in cmd for t in row.get("contains", [])):
            return row
    return None


# --------------------------------------------------------------------------------------------------------- selection (pure)

@dataclasses.dataclass
class Candidate:
    root: dict
    tree: list                       # root first, then descendants breadth-first
    shape: str                       # S0 | S1 | S3 (a log label)
    decoded: object                  # the user command, or None
    age: float
    orphan: bool = False


@dataclasses.dataclass
class Selection:
    candidates: list = dataclasses.field(default_factory=list)
    orphans: list = dataclasses.field(default_factory=list)
    unknown_roots: list = dataclasses.field(default_factory=list)      # procs
    unwrap_failed: int = 0
    kept_never: list = dataclasses.field(default_factory=list)         # root procs kept by never_reap / self-protection
    reason: str = ""                                                     # why nothing could be selected ("" = judged)


def _wait_loops(decoded):
    try:
        import hygiene_gate
        return bool(hygiene_gate.wait_loop_forms(decoded, "Bash"))
    except Exception:
        return False


def _never(tree, rows, protect):
    names = {str(n).lower() for n in rows["never_reap"]["names"]}
    subs = [str(s).lower() for s in rows["never_reap"]["cmd_substrings"]]
    for p in tree:
        if p["pid"] in protect or p["name"].lower() in names or any(s in p["cmd"].lower() for s in subs):
            return True
    return False


class _Index:
    """The process list indexed once: by pid, the older-parent child links, and the reaper's own ancestors (never stopped)."""

    def __init__(self, procs, self_pid=None):
        self.by_pid = {p["pid"]: p for p in procs}
        self.children = {}
        for p in procs:                                                  # F-R3: a link counts only from an OLDER parent
            par = self.by_pid.get(p["ppid"])
            if (p["created"] is not None and par is not None and par["created"] is not None and par is not p
                    and par["created"] < p["created"]):
                self.children.setdefault(par["pid"], []).append(p)
        for kids in self.children.values():
            kids.sort(key=lambda k: (k["created"], k["pid"]))
        self.protect, cur = set(), os.getpid() if self_pid is None else self_pid
        while cur in self.by_pid and cur not in self.protect:            # the reaper and its ancestors, by any link
            self.protect.add(cur)
            cur = self.by_pid[cur]["ppid"]

    def tree_of(self, root):
        tree, queue = [root], [root]
        while queue:
            for k in self.children.get(queue.pop(0)["pid"], []):
                tree.append(k)
                queue.append(k)
        return tree


def _build(root, row, orphan, idx, rows, now, sel):
    tree = idx.tree_of(root)
    if _never(tree, rows, idx.protect):
        sel.kept_never.append(root)
        return None
    decode = _DECODERS.get(row.get("decode"))
    decoded = decode(root["cmd"]) if decode else None
    if decode and decoded is None:
        sel.unwrap_failed += 1
    if any(p["name"].lower().removesuffix(".exe") == "sleep" for p in tree):
        shape = "S1"
    elif decoded is not None and _wait_loops(decoded):
        shape = "S3"
    else:
        shape = "S0"
    return Candidate(root, tree, shape, decoded, now - root["created"], orphan)


def _candidate_pass(procs, idx, session, rows, now, limit, sel, taken):
    """Direct children of the session process, older than the limit: a known wrapper is a candidate, any other root is reported."""
    for p in sorted(procs, key=lambda q: q["pid"]):
        if p["ppid"] != session["pid"] or p["created"] is None or not p["created"] > session["created"]:
            continue
        if p["name"].lower() == "conhost.exe" or not now - p["created"] > limit:
            continue
        row = match_wrapper(p, rows)
        if row is None:
            sel.unknown_roots.append(p)
            continue
        cand = _build(p, row, False, idx, rows, now, sel)
        if cand:
            sel.candidates.append(cand)
            taken.update(q["pid"] for q in cand.tree)


def _orphan_pass(procs, idx, session, rows, now, limit, sel, taken):
    """A dead session's call: a wrapper root older than the limit whose parent is absent or younger."""
    for p in sorted(procs, key=lambda q: q["pid"]):
        if p["pid"] in taken or p["ppid"] == session["pid"] or p["created"] is None or not now - p["created"] > limit:
            continue
        par = idx.by_pid.get(p["ppid"])
        if par is not None and par["created"] is not None and par["created"] < p["created"]:
            continue
        row = match_wrapper(p, rows)
        if row is None or p["name"].lower() == "conhost.exe":
            continue
        cand = _build(p, row, True, idx, rows, now, sel)
        if cand:
            sel.orphans.append(cand)
            taken.update(q["pid"] for q in cand.tree)


def select(procs, now, session, rows, *, limit=None, self_pid=None):
    """Pure: the trees to stop, the orphans, the roots no row knows. `session` = {"pid", "created"} or None (nothing selected)."""
    limit = rows["limit_seconds"] if limit is None else limit
    sel = Selection()
    if not session:
        sel.reason = "no session"
        return sel
    idx = _Index(procs, self_pid)
    sp = idx.by_pid.get(session["pid"])
    if sp is None or sp["created"] is None or abs(sp["created"] - session["created"]) > PID_TOLERANCE_S:
        sel.reason = "session process not in the list (or another process now holds its pid)"
        return sel
    taken = set()
    _candidate_pass(procs, idx, session, rows, now, limit, sel, taken)
    _orphan_pass(procs, idx, session, rows, now, limit, sel, taken)
    return sel


# --------------------------------------------------------------------------------------------------------- stop

def _exited(api, handle):
    """True only when the OS says the process has ended; any doubt reads False (the failure stays a failure)."""
    try:
        return bool(api.exited(handle))
    except Exception:
        return False


def stop_tree(cand, api, attempted):
    """[(proc, outcome)] root first. outcome: stopped | gone | pid-reused | failed: winerror <n>. One attempt per pid per run
    (`attempted` is shared across the run); never raises."""
    results = []
    for p in cand.tree:
        if p["pid"] in attempted:
            continue
        attempted.add(p["pid"])
        handle = None
        try:
            try:
                handle, created = api.open_terminable(p["pid"])
            except OSError as exc:
                code = session_proc.error_code(exc)
                results.append((p, "gone" if code in GONE_CODES else "failed: winerror %s" % code))
                continue
            if p["created"] is None or abs(created - p["created"]) > PID_TOLERANCE_S:
                results.append((p, "pid-reused"))
                continue
            try:
                api.terminate(handle)
                results.append((p, "stopped"))
            except OSError as exc:
                code = session_proc.error_code(exc)
                # a process already gone: its code says so, or access denied on a process that has already exited
                gone = code in GONE_CODES or (code == ACCESS_DENIED and _exited(api, handle))
                results.append((p, "gone" if gone else "failed: winerror %s" % code))
        except Exception as exc:                                         # never a raise out of a stop
            results.append((p, "failed: %s" % type(exc).__name__))
        finally:
            if handle is not None:
                try:
                    api.close(handle)
                except Exception:
                    pass
    return results


# --------------------------------------------------------------------------------------------------------- the log

def _ts(now):
    return datetime.fromtimestamp(now).strftime("%Y-%m-%dT%H:%M:%S")


def kids_field(cand, now):
    kids = cand.tree[1:]
    parts = ["%s/%d/%d/%s" % (ascii_clip(k["name"], 60), k["pid"], max(0, int(now - (k["created"] or now))),
                              ascii_clip(k["cmd"], KID_CMD_MAX)) for k in kids[:KIDS_MAX]]
    if len(kids) > KIDS_MAX:
        parts.append("+%d more" % (len(kids) - KIDS_MAX))
    return ";".join(parts)


def fails_field(results):
    """`<name>/<pid>/<outcome>;...` of every process whose stop failed (the roots and the kids alike), capped like the kids."""
    bad = [(p, o) for p, o in results if o.startswith("failed")]
    parts = ["%s/%d/%s" % (ascii_clip(p["name"], 60), p["pid"], ascii_clip(o, 60)) for p, o in bad[:KIDS_MAX]]
    if len(bad) > KIDS_MAX:
        parts.append("+%d more" % (len(bad) - KIDS_MAX))
    return ";".join(parts)


def log_line(now, trigger, session, label, cand=None, proc=None, fails=""):
    """`<ts> <trigger> sess=<pid> <label> root=<pid> age=<s> shape=<S> name=<n> [orphan=yes] cmd=<...> kids=<...> [fails=<...>]`.
    cmd = the decoded user command, else the raw command line (ASCII, at most 2000)."""
    sess = session["pid"] if session else "-"
    if cand is None and proc is None:
        return "%s %s sess=%s %s" % (_ts(now), trigger, sess, label)
    root = cand.root if cand else proc
    cmd = cand.decoded if cand is not None and cand.decoded is not None else root["cmd"]
    return "%s %s sess=%s %s root=%d age=%d shape=%s name=%s%s cmd=%s kids=%s%s" % (
        _ts(now), trigger, sess, label, root["pid"], max(0, int(now - (root["created"] or now))), cand.shape if cand else "-",
        ascii_clip(root["name"], 60), " orphan=yes" if cand is not None and cand.orphan else "",
        ascii_clip(cmd, CMD_LOG_MAX), kids_field(cand, now) if cand else "", " fails=" + fails if fails else "")


# --------------------------------------------------------------------------------------------------------- the run

def _session_dir(state, session):
    stamp = datetime.fromtimestamp(session["created"]).strftime("%Y%m%d%H%M%S")
    return Path(state) / ("%d-%s" % (session["pid"], stamp))


def _append(path, line):
    try:
        with open(path, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except OSError:
        pass


def run(args, *, lister=None, api=None, now=None, walker=None, out=print, state_root=None, rows=None):
    """One reaper run; returns the exit code. The OS seams (lister, api, walker) and `state_root` are parameters for the tests."""
    now = time.time() if now is None else now
    trigger = ascii_clip(args.trigger, 40)
    try:
        rows = rows or session_proc.load_rows()
    except session_proc.RowsError as exc:
        out("wait_reaper: %s" % exc)
        return 1
    limit = rows["limit_seconds"] if args.limit is None else args.limit
    state = state_root
    if state is None:
        try:
            repo = ws.repo_context(ws.Git(), args.repo or os.getcwd())
        except ws.Refuse as exc:
            out("wait_reaper: %s" % ws.first_line(str(exc)))
            return 1
        state = repo.common / STATE_DIRNAME
    log = Path(state) / "run.log"
    if args.session_pid is not None:
        session = {"pid": args.session_pid, "created": ws._iso_epoch(args.session_created)}
        reason = "" if session["created"] is not None else "--session-created is not an ISO time"
        session = session if session["created"] is not None else None
    else:
        session, reason = (walker or session_proc.session_process)(rows)
    if session is None:
        line = log_line(now, trigger, None, "no-session: %s" % ascii_clip(reason, REASON_MAX))
        out(line)
        if args.apply:
            _try_mkdir(state)
            _append(log, line)
        return 0
    lock, status, sdir = None, None, None
    if args.apply:
        sdir = _session_dir(state, session)
        try:
            lock, holder = ws.acquire_lock(sdir, trigger, now)
        except OSError as exc:
            out("wait_reaper: cannot make %s (%s)" % (sdir, ws.first_line(str(exc))))
            return 1
        if lock is None:
            out("busy: a reaper of this session is already running since %s (%s)" % (holder.get("started", "unknown"),
                                                                                       holder.get("trigger", "unknown")))
            return 0
        status = ws.StatusFile(sdir)
        status.update(state="running", started=ws._iso(now), finished=None, trigger=trigger, trees_stopped=0, procs_stopped=0, procs_failed=0, reported=0,
                      unknown_root=0, orphans=0, unwrap_failed=0, reason="")
    try:
        return _run_locked(args, session, rows, limit, now, trigger, lister, api, out, log, status)
    finally:
        if lock is not None:
            lock.release()


def _try_mkdir(path):
    try:
        Path(path).mkdir(parents=True, exist_ok=True)
    except OSError:
        pass


def _run_locked(args, session, rows, limit, now, trigger, lister, api, out, log, status):
    lines = []

    def emit(line):
        out(line)
        lines.append(line)
        if args.apply:
            _append(log, line)

    try:
        procs = (lister or list_processes)()
    except ListError as exc:
        reason = ascii_clip(exc, REASON_MAX)
        emit(log_line(now, trigger, session, "unreadable: %s" % reason))
        if status:
            status.update(state="unreadable", finished=ws._iso(), reason=reason)
        return 1
    except Exception as exc:                                             # a lister that raises anything else is the same fault
        reason = ascii_clip("%s: %s" % (type(exc).__name__, exc), REASON_MAX)
        emit(log_line(now, trigger, session, "unreadable: %s" % reason))
        if status:
            status.update(state="unreadable", finished=ws._iso(), reason=reason)
        return 1
    sel = select(procs, now, session, rows, limit=limit)
    if sel.reason:
        emit(log_line(now, trigger, session, "no-session: %s" % sel.reason))
        if status:
            status.update(state="finished", finished=ws._iso(), reason=sel.reason)
        return 0
    only = args.pid
    todo = [c for c in sel.candidates if only is None or c.root["pid"] == only]
    orphans = [c for c in sel.orphans if only is None or c.root["pid"] == only]
    unknown = [p for p in sel.unknown_roots if only is None or p["pid"] == only]
    counts = {"trees_stopped": 0, "procs_stopped": 0, "procs_failed": 0, "reported": 0}
    attempted = set()
    for cand in todo + (orphans if args.orphans else []):
        if not args.apply:
            counts["reported"] += 1
            emit(log_line(now, trigger, session, "reported", cand))
            continue
        results = stop_tree(cand, api or session_proc.default_api(), attempted)
        label = results[0][1] if results and results[0][0] is cand.root else "gone"
        counts["trees_stopped"] += 1 if label == "stopped" else 0
        counts["procs_stopped"] += sum(1 for _, o in results if o == "stopped")
        counts["procs_failed"] += sum(1 for _, o in results if o.startswith("failed"))
        emit(log_line(now, trigger, session, label, cand, fails=fails_field(results)))
    if not args.orphans:
        for cand in orphans:
            counts["reported"] += 1
            emit(log_line(now, trigger, session, "reported", cand))
    for p in sel.kept_never:                                             # kept by never_reap / self-protection: said, not silent
        if only is None or p["pid"] == only:
            emit(log_line(now, trigger, session, "kept", proc=p))
    for p in unknown:
        emit(log_line(now, trigger, session, "unknown-root", proc=p))
    out("wait_reaper: finished: %d trees stopped (%d processes), %d processes failed, %d reported, %d unknown roots, %d orphans" % (
        counts["trees_stopped"], counts["procs_stopped"], counts["procs_failed"], counts["reported"], len(unknown), len(orphans)))
    if status:
        status.update(state="finished", finished=ws._iso(), trees_stopped=counts["trees_stopped"],
                      procs_stopped=counts["procs_stopped"], procs_failed=counts["procs_failed"], reported=counts["reported"], unknown_root=len(unknown), orphans=len(orphans),
                      unwrap_failed=sel.unwrap_failed, reason="")
    return 0


# --------------------------------------------------------------------------------------------------------- launcher, WAITS

def launch(trigger, root=None, *, walker=None, spawn=None, runner=None, timeout=5, repo=None):
    """The hook's entry: str | None. The session is resolved IN-PROCESS first (no session: the WAITS line, nothing spawned);
    else this tool of the MAIN checkout is spawned detached with the session's pid and creation time. At most `timeout` (5 s) per
    git call; a caller that already holds the `repo` context passes it. Never raises, never waits."""
    try:
        session, reason = (walker or session_proc.session_process)()
        if session is None:
            return "WAITS: no session (%s) -- nothing stopped" % ascii_clip(reason, REASON_MAX)
        try:
            repo = repo or ws.repo_context(ws.Git(runner, timeout=timeout), root or os.getcwd())
        except ws.Refuse as exc:
            return "WAITS: reaper not started (%s)" % ascii_clip(ws.first_line(str(exc)), REASON_MAX)
        tool = repo.main_path / "tools" / "wait_reaper.py"
        if not tool.is_file():
            return "WAITS: reaper not started (tools/wait_reaper.py not found in %s)" % ascii_clip(repo.main_path, REASON_MAX)
        (spawn or ws.spawn_detached)(
            [sys.executable, "-B", str(tool), "--apply", "--trigger", ascii_clip(trigger, 40), "--session-pid", str(session["pid"]),
             "--session-created", ws._iso(session["created"]), "--repo", str(repo.main_path)],
            repo.main_path, ws._env_without_git())
        return None
    except Exception as exc:
        return "WAITS: reaper not started (%s)" % ascii_clip("%s: %s" % (type(exc).__name__, exc), REASON_MAX)


def waits_line(state_root, session, now=None):
    """The SessionStart line from THIS session's status.json, or None (silent at zero, nothing read, a run in flight)."""
    try:
        data = json.loads((_session_dir(state_root, session) / "status.json").read_text(encoding="utf-8"))
    except (OSError, ValueError, KeyError, TypeError):
        return None
    if not isinstance(data, dict):
        return None
    state = data.get("state")
    if state == "unreadable":
        return ascii_clip("WAITS: process list unreadable (%s) -- python -B tools/wait_reaper.py" % ascii_clip(data.get("reason"), 80),
                          200)
    n, m, u, o = (int(data.get(k) or 0) for k in ("trees_stopped", "procs_failed", "unknown_root", "orphans"))
    if state != "finished" or not (n or m or u or o):
        return None
    when = str(data.get("finished") or data.get("started") or "")[:19]
    line = "WAITS: last reap %s (%s): %d trees stopped, %d processes failed, %d unknown roots" % (when, ascii_clip(data.get("trigger"), 20), n, m, u)
    if o:
        line += "; %d calls of dead sessions -- python -B tools/wait_reaper.py --orphans --apply" % o
    return ascii_clip(line, 200)


def build_parser():
    p = argparse.ArgumentParser(prog="wait_reaper.py", description="Stop this session's tool-call trees older than the limit.")
    p.add_argument("--apply", action="store_true", help="stop (default: a dry list)")
    p.add_argument("--limit", type=float, default=None, help="seconds; default: limit_seconds of wait-reaper.json")
    p.add_argument("--trigger", default="manual")
    p.add_argument("--session-pid", type=int, default=None)
    p.add_argument("--session-created", default=None, help="ISO local time of the session process")
    p.add_argument("--orphans", action="store_true", help="with --apply: also stop the calls of dead sessions")
    p.add_argument("--pid", type=int, default=None, help="only the tree with this root pid")
    p.add_argument("--repo", default=None)
    return p


def main(argv=None):
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(errors="replace", line_buffering=True)
        except (AttributeError, ValueError):
            pass
    parser = build_parser()
    args = parser.parse_args(argv)
    if (args.session_pid is None) != (args.session_created is None):
        parser.error("--session-pid and --session-created go together")
    return run(args)


if __name__ == "__main__":
    sys.exit(main())
