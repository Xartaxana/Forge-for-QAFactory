"""The process of THIS session, found in-process (bounded-waits spec r2 section 5.0; K-REAP).

    session_process() -> (dict | None, reason)       dict = {"pid": int, "created": epoch seconds (float)}

Walks from `os.getpid()` up the parent links with no child process (Windows: ctypes over kernel32 -- a snapshot for the parent
links and names, `GetProcessTimes` for the creation time; POSIX: /proc). A hop counts only when the parent was created BEFORE
the child (F-R3: Windows does not re-parent orphans, a dead parent's pid can be reused); otherwise the walk stops. The FIRST
ancestor whose executable name (case-insensitive) is in the data row `session_process_names` of `wait-reaper.json` is the
session; the app above it is never reached. Cap: HOP_CAP hops.

Invariant: the session is known by pid AND creation time only; with no session nothing is stopped. Error direction: this
function may fail to find a session, it never names a wrong process. `load_rows` is the ONE reader of `wait-reaper.json`
(read once per run, loud when broken: RowsError names the file and the fault); it lives here so the narrative stamp can import
the walk without importing the reaper.

The OS calls are the thin seam `Api` (snapshot / created / open_terminable / terminate / close): tests pass a fake.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

_TOOLS = Path(__file__).resolve().parent
ROWS_PATH = _TOOLS / "wait-reaper.json"
HOP_CAP = 32
NO_CLAUDE = "no claude.exe ancestor"
POSIX_NOT_MEASURED = "posix session name not measured"
_IS_WINDOWS = os.name == "nt"


class RowsError(Exception):
    """wait-reaper.json is missing, not JSON, or lacks a row the code needs; the message names the file and the fault."""


def load_rows(path=None):
    """The data rows, validated for shape. Never a default selection: a broken file raises RowsError."""
    path = Path(path or ROWS_PATH)
    try:
        rows = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise RowsError("%s is unreadable (%s: %s) -- fix the file; nothing stopped" % (path.name, type(exc).__name__, str(exc)[:80]))
    ok = isinstance(rows, dict)
    ok = ok and isinstance(rows.get("limit_seconds"), (int, float)) and not isinstance(rows.get("limit_seconds"), bool)
    ok = ok and isinstance(rows.get("session_process_names"), dict)
    ok = ok and all(isinstance(rows["session_process_names"].get(k), list) for k in ("nt", "posix"))
    ok = ok and isinstance(rows.get("tool_call_roots"), list) and isinstance(rows.get("wrapper_forms"), list)
    ok = ok and isinstance(rows.get("never_reap"), dict)
    ok = ok and isinstance(rows["never_reap"].get("names"), list) and isinstance(rows["never_reap"].get("cmd_substrings"), list)
    if not ok:
        raise RowsError("%s lacks a required row (limit_seconds, session_process_names{nt,posix}, tool_call_roots, wrapper_forms, "
                        "never_reap{names,cmd_substrings}) -- fix the file; nothing stopped" % path.name)
    return rows


def error_code(exc):
    return getattr(exc, "winerror", None) or getattr(exc, "errno", None) or 0


# --------------------------------------------------------------------------------------------------------- the OS seam

class WinApi:
    """kernel32 through ctypes, in-process. Every failure is an OSError carrying `winerror`."""

    PROCESS_TERMINATE = 0x0001
    PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
    _EPOCH_DELTA = 116444736000000000            # 100 ns ticks from 1601-01-01 to 1970-01-01

    def __init__(self):
        import ctypes
        from ctypes import wintypes
        self.ct, self.wt = ctypes, wintypes
        k = ctypes.WinDLL("kernel32", use_last_error=True)
        self.k = k
        vp = ctypes.c_void_p
        k.CreateToolhelp32Snapshot.restype = vp
        k.CreateToolhelp32Snapshot.argtypes = [wintypes.DWORD, wintypes.DWORD]
        k.OpenProcess.restype = vp
        k.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
        k.CloseHandle.argtypes = [vp]
        k.GetProcessTimes.argtypes = [vp] + [ctypes.POINTER(wintypes.FILETIME)] * 4
        k.TerminateProcess.argtypes = [vp, wintypes.UINT]

        class Entry(ctypes.Structure):
            _fields_ = [("dwSize", wintypes.DWORD), ("cntUsage", wintypes.DWORD), ("th32ProcessID", wintypes.DWORD),
                        ("th32DefaultHeapID", ctypes.c_size_t), ("th32ModuleID", wintypes.DWORD),
                        ("cntThreads", wintypes.DWORD), ("th32ParentProcessID", wintypes.DWORD),
                        ("pcPriClassBase", wintypes.LONG), ("dwFlags", wintypes.DWORD), ("szExeFile", wintypes.WCHAR * 260)]
        self.Entry = Entry
        k.Process32FirstW.argtypes = [vp, ctypes.POINTER(Entry)]
        k.Process32NextW.argtypes = [vp, ctypes.POINTER(Entry)]

    def _fail(self):
        raise self.ct.WinError(self.ct.get_last_error())

    def snapshot(self):
        """{pid: (ppid, exe name)}"""
        snap = self.k.CreateToolhelp32Snapshot(0x2, 0)                   # TH32CS_SNAPPROCESS
        if not snap or snap == self.ct.c_void_p(-1).value:
            self._fail()
        out = {}
        try:
            entry = self.Entry()
            entry.dwSize = self.ct.sizeof(entry)
            ok = self.k.Process32FirstW(snap, self.ct.byref(entry))
            while ok:
                out[int(entry.th32ProcessID)] = (int(entry.th32ParentProcessID), entry.szExeFile)
                ok = self.k.Process32NextW(snap, self.ct.byref(entry))
        finally:
            self.k.CloseHandle(snap)
        return out

    def _times(self, handle):
        c, e, kt, ut = (self.wt.FILETIME() for _ in range(4))
        if not self.k.GetProcessTimes(handle, self.ct.byref(c), self.ct.byref(e), self.ct.byref(kt), self.ct.byref(ut)):
            self._fail()
        return (((c.dwHighDateTime << 32) | c.dwLowDateTime) - self._EPOCH_DELTA) / 1e7

    def created(self, pid):
        handle = self.k.OpenProcess(self.PROCESS_QUERY_LIMITED_INFORMATION, False, pid)
        if not handle:
            self._fail()
        try:
            return self._times(handle)
        finally:
            self.k.CloseHandle(handle)

    def open_terminable(self, pid):
        """(handle, creation time read ON THAT HANDLE): the creation check and the terminate use the same handle."""
        handle = self.k.OpenProcess(self.PROCESS_TERMINATE | self.PROCESS_QUERY_LIMITED_INFORMATION, False, pid)
        if not handle:
            self._fail()
        try:
            return handle, self._times(handle)
        except OSError:
            self.k.CloseHandle(handle)
            raise

    def terminate(self, handle):
        if not self.k.TerminateProcess(handle, 1):
            self._fail()

    def close(self, handle):
        self.k.CloseHandle(handle)


class PosixApi:
    """/proc. Reads only; POSIX stopping is off until the session process name is measured on a POSIX seat (fork FP)."""

    def snapshot(self):
        out = {}
        for entry in os.listdir("/proc"):
            if not entry.isdigit():
                continue
            try:
                text = Path("/proc/%s/stat" % entry).read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            left, right = text.find("("), text.rfind(")")
            if left < 0 or right < left:
                continue
            fields = text[right + 2:].split()
            if len(fields) > 1 and fields[1].isdigit():
                out[int(entry)] = (int(fields[1]), text[left + 1:right])
        return out

    def created(self, pid):
        text = Path("/proc/%d/stat" % pid).read_text(encoding="utf-8", errors="replace")
        fields = text[text.rfind(")") + 2:].split()
        ticks = int(fields[19])
        btime = next(int(l.split()[1]) for l in Path("/proc/stat").read_text().splitlines() if l.startswith("btime"))
        return btime + ticks / os.sysconf("SC_CLK_TCK")

    def open_terminable(self, pid):
        return pid, self.created(pid)

    def terminate(self, handle):
        import signal
        os.kill(handle, signal.SIGTERM)

    def close(self, handle):
        pass


def default_api():
    return WinApi() if _IS_WINDOWS else PosixApi()


# --------------------------------------------------------------------------------------------------------- the walk

def walk(api, start_pid, names, hop_cap=HOP_CAP):
    """(session dict | None, reason). `names` are lower-case executable names. One snapshot, one creation read per hop."""
    try:
        procs = api.snapshot()
    except OSError as exc:
        return None, "api error %s" % error_code(exc)
    if start_pid not in procs:
        return None, NO_CLAUDE
    cur, hops = start_pid, 0
    try:
        cur_created = api.created(cur)
        while True:
            ppid = procs[cur][0]
            if ppid == 0 or ppid == cur or ppid not in procs:
                return None, NO_CLAUDE
            parent_created = api.created(ppid)
            if not parent_created < cur_created:                         # F-R3: the parent must be OLDER than the child
                return None, "orphan at %s" % procs[cur][1]
            hops += 1
            if hops > hop_cap:
                return None, "hops over %d" % hop_cap
            if procs[ppid][1].lower() in names:
                return {"pid": ppid, "created": parent_created}, ""
            cur, cur_created = ppid, parent_created
    except OSError as exc:
        return None, "api error %s" % error_code(exc)


def session_process(rows=None, api=None, start_pid=None, platform=None):
    """The session process of the caller, or (None, reason). Reasons: `no claude.exe ancestor`, `orphan at <name>`,
    `hops over 32`, `api error <n>`, `posix session name not measured`, `<rows fault>`."""
    platform = platform or os.name
    try:
        rows = rows or load_rows()
    except RowsError as exc:
        return None, str(exc)
    names = [str(n).lower() for n in rows["session_process_names"]["nt" if platform == "nt" else "posix"]]
    if not names:
        return None, POSIX_NOT_MEASURED if platform != "nt" else NO_CLAUDE
    try:
        api = api or default_api()
    except Exception as exc:                                              # a ctypes that cannot load: not a session, not a raise
        return None, "api error %s" % (error_code(exc) or type(exc).__name__)
    return walk(api, os.getpid() if start_pid is None else start_pid, set(names))


def main(argv=None):
    session, reason = session_process()
    print(("session pid=%d created=%.3f" % (session["pid"], session["created"])) if session else "no session: %s" % reason)
    return 0 if session else 1


if __name__ == "__main__":
    sys.exit(main())
