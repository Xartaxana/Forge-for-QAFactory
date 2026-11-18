"""wait_reaper.py and session_proc.py (bounded-waits spec r2 section 7.2; card K-REAP).

Three tables: the pure selection over process-list fixtures (the real Bash and PowerShell wrapper command lines of harness
2.1.321), the session walk over a fake OS seam, and the runs (stop, log, lock, status, launcher). The lister, the handle
open/terminate and the walk's OS calls are thin seams replaced here: no real process is touched, nothing is killed.
Expected values come from the spec rows (section 5.1, 5.2, 7.2), not from the code's output.
"""
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import time
import types

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import session_proc as sp  # noqa: E402
import wait_reaper as wr  # noqa: E402

NOW = 1_800_000_000.0
H = 3600


def P(pid, ppid, name, age, cmd=""):
    return {"pid": pid, "ppid": ppid, "name": name, "created": NOW - age, "cmd": cmd}


def spliced(cmd):
    return cmd.replace("'", "'\\''")


def bash_cmd(user):
    """The measured Bash wrapper (review t-1131, 17.11.2026): the user command single-quote spliced inside `eval '...'`."""
    return ('"C:\\Program Files\\Git\\bin\\bash.exe" -c "source C:/Users/u/.claude/shell-snapshots/snapshot-bash-1731-ab.sh '
            '2>/dev/null || true && export TEMP=C:/t && shopt -u extglob 2>/dev/null || true && eval \'' + spliced(user) +
            '\' < /dev/null && pwd -P >| C:/t/claude-c701-cwd"')


PS_CMD = ('C:\\WINDOWS\\system32\\cmd.exe /d /s /c ""chcp.com" 65001 >nul & "powershell.exe" -NoProfile -NonInteractive '
          '-Command "& $env:CLAUDE_CODE_SHELL_LAUNCHER_SCRIPT""')
LOOP = "until test -f /nonexistent; do sleep 20; done"
SESSION = {"pid": 100, "created": NOW - 3 * 86400}
BASE = [P(90, 1, "claude.exe", 4 * 86400), P(100, 90, "claude.exe", 3 * 86400), P(101, 100, "conhost.exe", 3 * 86400)]
ROWS = sp.load_rows()


def sel(procs, session=SESSION, **kw):
    return wr.select(BASE + procs, NOW, session, ROWS, self_pid=kw.pop("self_pid", 4242), **kw)


# --------------------------------------------------------------------------------------------------------- selection

SELECT_ROWS = [
    # id, procs, expected roots {pid: shape}, expected extras
    ("R-real-bash", [P(200, 100, "bash.exe", 3 * H, bash_cmd(LOOP)), P(201, 200, "sleep.exe", 15, "sleep 20")], {200: "S1"}, {}),
    ("S3-loop-no-sleep-kid", [P(200, 100, "bash.exe", 3 * H, bash_cmd(LOOP))], {200: "S3"}, {}),
    ("R-real-ps", [P(210, 100, "cmd.exe", 3 * H, PS_CMD), P(211, 210, "powershell.exe", 3 * H - 1, "powershell.exe -NoProfile")],
     {210: "S0"}, {"decoded": {210: None}}),
    ("R-AT", [P(200, 100, "bash.exe", 7200, bash_cmd("echo x"))], {}, {}),
    ("R-BEYOND", [P(200, 100, "bash.exe", 7201, bash_cmd("echo x"))], {200: "S0"}, {}),
    ("R-young", [P(200, 100, "bash.exe", 1800, bash_cmd(LOOP)), P(201, 200, "sleep.exe", 15)], {}, {}),
    ("R-11h", [P(200, 100, "bash.exe", 11 * H, bash_cmd("cat > /dev/null; python - <<'EOF'\nimport time\nEOF")),
               P(201, 200, "bash.exe", 11 * H - 1, "bash"), P(202, 200, "bash.exe", 11 * H - 2, "bash")],
     {200: "S0"}, {"tree": {200: [200, 201, 202]}}),
    ("R-dev", [P(200, 100, "bash.exe", 3 * H, bash_cmd("npm run dev")), P(201, 200, "node.exe", 3 * H - 1, "node dev.js")],
     {200: "S0"}, {}),
    ("R-nearest", [P(95, 90, "claude.exe", 4 * 86400), P(96, 95, "powershell.exe", 3 * 86400, "powershell -NoExit"),
                   P(200, 100, "bash.exe", 3 * H, bash_cmd(LOOP)), P(201, 200, "sleep.exe", 5)],
     {200: "S1"}, {"tree": {200: [200, 201]}}),
    ("R-orphan-reuse", [P(300, 100, "bash.exe", 600, bash_cmd("echo")), P(301, 300, "python.exe", 9 * H, "python story_run.py")],
     {}, {}),
    ("R-dead-session", [P(400, 999, "bash.exe", 5 * H, bash_cmd(LOOP))], {}, {"orphans": [400]}),
    ("R-conhost", [P(500, 100, "conhost.exe", 3 * 86400)], {}, {"unknown": []}),
    ("R-unknown-root", [P(510, 100, "cmd.exe", 3 * H, "cmd.exe /c foo")], {}, {"unknown": [510]}),
    ("R-never-gh", [P(200, 100, "bash.exe", 3 * H, bash_cmd(LOOP)), P(201, 200, "gh.exe", 5, "gh run watch")], {}, {"never": [200]}),
    ("R-never-story", [P(200, 100, "bash.exe", 3 * H, bash_cmd(LOOP)), P(201, 200, "python.exe", 5, "python story_run.py x")],
     {}, {"never": [200]}),
    ("R-never-NoExit", [P(200, 100, "bash.exe", 3 * H, bash_cmd(LOOP)), P(201, 200, "powershell.exe", 5, "powershell -noexit")],
     {}, {"never": [200]}),
    ("R-never-path-high", [P(200, 100, "bash.exe", 3 * H, bash_cmd(LOOP)), P(201, 200, "x.exe", 5, "C:\\tools\\high\\x.exe")],
     {200: "S3"}, {}),
    ("R-self", [P(200, 100, "bash.exe", 3 * H, bash_cmd(LOOP)), P(4242, 200, "python.exe", 5, "python wait_reaper.py")],
     {}, {"never": [200]}),
    ("R-self-ancestor-launcher", [P(200, 100, "bash.exe", 3 * H, bash_cmd(LOOP)), P(4241, 200, "python.exe", 6, "python x")],
     {}, {"never": [200]}),
    ("R-unwrap-unknown-wrapper", [P(200, 100, "bash.exe", 3 * H, '"bash.exe" -c "other-harness eval foo"')], {}, {"unknown": [200]}),
    ("R-unwrap-failed", [P(200, 100, "bash.exe", 3 * H, bash_cmd("echo x").replace("' < /dev/null", "' < /dev/zero"))],
     {200: "S0"}, {"unwrap_failed": 1}),
]


@pytest.mark.parametrize("name,procs,roots,extra", SELECT_ROWS, ids=[r[0] for r in SELECT_ROWS])
def test_select(name, procs, roots, extra):
    s = sel(procs, self_pid=4241 if "ancestor" in name else 4242)
    assert {c.root["pid"]: c.shape for c in s.candidates} == roots
    for pid, decoded in extra.get("decoded", {}).items():
        assert [c.decoded for c in s.candidates if c.root["pid"] == pid] == [decoded]
    for pid, tree in extra.get("tree", {}).items():
        assert [[p["pid"] for p in c.tree] for c in s.candidates if c.root["pid"] == pid] == [tree]
    assert [c.root["pid"] for c in s.orphans] == extra.get("orphans", [])
    assert [p["pid"] for p in s.unknown_roots] == extra.get("unknown", [])
    assert [p["pid"] for p in s.kept_never] == extra.get("never", [])
    assert s.unwrap_failed == extra.get("unwrap_failed", 0)


def test_select_no_session_and_session_gone():
    assert wr.select(BASE, NOW, None, ROWS).reason and not wr.select(BASE, NOW, None, ROWS).candidates
    reused = {"pid": 100, "created": NOW - 100}                           # same pid, another creation time: another process
    gone = wr.select([P(200, 100, "bash.exe", 3 * H, bash_cmd(LOOP))], NOW, reused, ROWS)
    assert gone.reason and not gone.candidates


def test_decoded_command_is_the_users():
    s = sel([P(200, 100, "bash.exe", 3 * H, bash_cmd(LOOP))])
    assert s.candidates[0].decoded == LOOP


ADVERSARIAL = [
    "echo it's",                                   # the splice '\''
    "echo \"it's\"",                               # a double-quoted single quote
    "a 'b \"c 'd' c\" b' a",                       # four deep
    "echo \u043f\u0440\u0438\u0432\u0435\u0442",   # non-ASCII
    "echo a\x00b",                                 # NUL
    "'",                                           # a lone quote
    "x" * 70000,                                   # over the decode cap
]


@pytest.mark.parametrize("user", ADVERSARIAL, ids=["splice", "dq-quote", "four-deep", "non-ascii", "nul", "lone", "64k"])
def test_cmd_adversarial_never_raises_and_log_is_ascii(user):
    cmd = bash_cmd(user)
    got = wr.decode_bash_eval(cmd)
    if len(cmd) > wr.DECODE_CAP:
        assert got is None                                                # cut command line: unwrap_failed, never a wide decode
    else:
        assert got == user.replace('\\"', '"')
    cand = wr.select(BASE + [P(200, 100, "bash.exe", 3 * H, cmd)], NOW, SESSION, ROWS, self_pid=4242).candidates
    line = wr.log_line(NOW, "t", SESSION, "reported", cand[0])
    assert line.isascii() and "\n" not in line and "\x00" not in line
    assert len(line.split(" cmd=", 1)[1].split(" kids=")[0]) <= wr.CMD_LOG_MAX


def test_log_caps_kids_and_cmd():
    kids = [P(1000 + i, 200, "k.exe", 10, "c" * 500) for i in range(25)]
    cand = sel([P(200, 100, "bash.exe", 3 * H, bash_cmd(LOOP))] + kids).candidates[0]
    line = wr.log_line(NOW, "post-merge", SESSION, "stopped", cand)
    kid_text = line.split(" kids=", 1)[1]
    assert kid_text.count("/k.exe") == 0 and kid_text.count("k.exe/") == 20 and kid_text.endswith("+5 more")
    assert all(len(part.split("/", 3)[3]) <= wr.KID_CMD_MAX for part in kid_text.split(";")[:20])


def test_cim_dates_and_list_parsing():
    a = wr.parse_cim_date("20261117150000.000000+180")                    # 15:00 at +3 h
    b = wr.parse_cim_date("20261117070000.000000-300")                    # 07:00 at -5 h
    assert a == b == wr.parse_cim_date("/Date(%d)/" % int(a * 1000)) == wr.parse_cim_date("2026-11-17T12:00:00+00:00")
    text = json.dumps([{"ProcessId": 5, "ParentProcessId": 1, "Name": "a.exe", "CreationDate": "/Date(1000)/", "CommandLine": None},
                       {"Name": "no pid"}])
    assert wr.parse_list(text) == [{"pid": 5, "ppid": 1, "name": "a.exe", "created": 1.0, "cmd": ""}]
    assert wr.parse_list("[]") == []
    with pytest.raises(wr.ListError):
        wr.parse_list("not json")


def test_lister_flags_and_failures(monkeypatch):
    monkeypatch.setattr(wr, "_IS_WINDOWS", True)
    seen = {}

    def ok(argv, **kw):
        seen.update(kw, argv=argv)
        return types.SimpleNamespace(returncode=0, stdout=b"[]", stderr=b"")

    assert wr.list_processes(ok) == [] and seen["creationflags"] & 0x08000000 and seen["timeout"] == 20
    assert seen["argv"][:3] == ["powershell", "-NoProfile", "-NonInteractive"] and "Win32_Process" in seen["argv"][-1]

    def slow(argv, **kw):
        raise subprocess.TimeoutExpired(argv, 20)

    def bad(argv, **kw):
        return types.SimpleNamespace(returncode=1, stdout=b"", stderr=b"CIM error\n")

    for run, word in ((slow, "timed out"), (bad, "CIM error")):
        with pytest.raises(wr.ListError, match=word):
            wr.list_processes(run)


# --------------------------------------------------------------------------------------------------------- the walk

SESS_IMG = "C:\\Users\\u\\AppData\\Local\\Claude-Data\\x\\claude-code\\2.1.321\\h\\claude.exe"
APP_IMG = "C:\\Program Files\\WindowsApps\\Claude_5\\app\\Claude.exe"


class FakeOs:
    """`images` maps pid -> image path; a pid not in it has a session image. fail == ("image", pid) breaks only the image read."""

    def __init__(self, procs, created, fail=None, images=None):
        self.procs, self.c, self.fail, self.images = procs, created, fail, images or {}

    def snapshot(self):
        if self.fail == "snapshot":
            raise OSError(5, "denied")
        return self.procs

    def created(self, pid):
        if self.fail == pid:
            e = OSError(5, "denied")
            e.winerror = 5
            raise e
        return self.c[pid]

    def identity(self, pid):
        if self.fail == ("image", pid):
            e = OSError(5, "denied")
            e.winerror = 5
            raise e
        return self.created(pid), self.images.get(pid, SESS_IMG)


def chain(n_hops, session_name="claude.exe"):
    procs, created = {}, {}
    for k in range(n_hops + 1):
        pid = 1000 + k
        procs[pid] = (pid + 1 if k < n_hops else 1, session_name if k == n_hops else "bash.exe")
        created[pid] = 1e9 - k * 10
    return procs, created


def app_over_session(img2=SESS_IMG, img3=APP_IMG):
    return ({1: (2, "bash.exe"), 2: (3, "claude.exe"), 3: (4, "claude.exe"), 4: (0, "explorer.exe")},
            {1: 300.0, 2: 200.0, 3: 100.0, 4: 50.0}, {2: img2, 3: img3})


def orphan_hop():
    return {1: (2, "bash.exe"), 2: (3, "bash.exe"), 3: (0, "claude.exe")}, {1: 300.0, 2: 200.0, 3: 250.0}


WALKS = [
    ("found", app_over_session, None, 1, {"pid": 2, "created": 200.0}, ""),
    ("hops-32-AT", lambda: chain(32), None, 1000, {"pid": 1032, "created": 1e9 - 320}, ""),
    ("hops-33-BEYOND", lambda: chain(33), None, 1000, None, "hops over 32"),
    ("orphan-hop", orphan_hop, None, 1, None, "orphan at bash.exe"),
    ("no-ancestor", lambda: chain(3, "explorer.exe"), None, 1000, None, "no claude.exe ancestor"),
    ("api-error-snapshot", app_over_session, "snapshot", 1, None, "api error 5"),
    ("api-error-times", app_over_session, 2, 1, None, "api error 5"),
    ("utility-not-session", lambda: app_over_session(APP_IMG), None, 1, None, sp.NOT_SESSION_IMAGE % 2),
    ("image-unreadable", app_over_session, ("image", 2), 1, None, "api error 5"),
    ("nested-other-install", lambda: app_over_session(APP_IMG, SESS_IMG), None, 1, None, sp.NOT_SESSION_IMAGE % 2),
    ("marker-substring", lambda: app_over_session("C:\\Users\\claude-code-fan\\x\\claude.exe"), None, 1, None, sp.NOT_SESSION_IMAGE % 2),
    ("marker-case-slash", lambda: app_over_session("C:/X/CLAUDE-CODE/2/claude.exe"), None, 1, {"pid": 2, "created": 200.0}, ""),
    ("marker-as-file-name", lambda: app_over_session("C:\\bin\\claude-code"), None, 1, None, sp.NOT_SESSION_IMAGE % 2),
    ("image-empty", lambda: app_over_session(""), None, 1, None, sp.NOT_SESSION_IMAGE % 2),
]


@pytest.mark.parametrize("name,make,fail,start,want,reason", WALKS, ids=[w[0] for w in WALKS])
def test_walk(name, make, fail, start, want, reason):
    procs, created, *images = make()
    got = sp.session_process(ROWS, FakeOs(procs, created, fail, *images), start_pid=start, platform="nt")
    assert got == (want, reason)


def test_walk_image_row_empty_is_not_measured():
    rows = dict(ROWS, session_image_dirs={"nt": [], "posix": []})
    assert sp.session_process(rows, FakeOs(*app_over_session()), start_pid=1, platform="nt") == (None, sp.IMAGE_NOT_MEASURED)


def test_walk_posix_empty_row_is_no_session():
    assert sp.session_process(ROWS, FakeOs(*app_over_session()[:2]), start_pid=1, platform="posix") == (None, sp.POSIX_NOT_MEASURED)


def test_broken_rows_file_is_named_never_a_default(tmp_path, monkeypatch):
    bad = tmp_path / "wait-reaper.json"
    bad.write_text("{", encoding="utf-8")
    with pytest.raises(sp.RowsError, match="wait-reaper.json"):
        sp.load_rows(bad)
    bad.write_text(json.dumps({"limit_seconds": 1}), encoding="utf-8")
    with pytest.raises(sp.RowsError, match="lacks a required row"):
        sp.load_rows(bad)
    bad.write_text(json.dumps({k: v for k, v in ROWS.items() if k != "session_image_dirs"}), encoding="utf-8")
    with pytest.raises(sp.RowsError, match="session_image_dirs"):
        sp.load_rows(bad)
    monkeypatch.setattr(sp, "ROWS_PATH", bad)
    out = []
    code = wr.run(wr.build_parser().parse_args(["--apply"]), out=out.append, state_root=tmp_path / "s")
    assert code == 1 and "wait-reaper.json" in out[0] and not (tmp_path / "s").exists()


# --------------------------------------------------------------------------------------------------------- stop and runs

def werr(n):
    e = OSError(n, "x")
    e.winerror = n
    return e


class FakeKill:
    def __init__(self, created, open_fail=None, term_fail=None, exited=()):
        self.created, self.open_fail, self.term_fail, self.exit_set = created, open_fail or {}, term_fail or {}, set(exited)
        self.opened, self.terminated, self.closed = [], [], []

    def open_terminable(self, pid):
        self.opened.append(pid)
        if pid in self.open_fail:
            raise werr(self.open_fail[pid])
        return ("h%d" % pid, self.created[pid])

    def terminate(self, handle):
        self.terminated.append(handle)
        if int(handle[1:]) in self.term_fail:
            raise werr(self.term_fail[int(handle[1:])])

    def exited(self, handle):
        return int(handle[1:]) in self.exit_set

    def close(self, handle):
        self.closed.append(handle)


def cand_tree():
    return sel([P(200, 100, "bash.exe", 3 * H, bash_cmd(LOOP)), P(201, 200, "sleep.exe", 15), P(202, 201, "x.exe", 5)]).candidates[0]


STOPS = [
    ("root-first-all-stopped", {}, {}, {}, (), ["h200", "h201", "h202"], ["stopped"] * 3),
    ("pid-reused-AT-tolerance-ok", {200: 1.0}, {}, {}, (), ["h200", "h201", "h202"], ["stopped"] * 3),
    ("pid-reused-BEYOND", {201: 1.01}, {}, {}, (), ["h200", "h202"], ["stopped", "pid-reused", "stopped"]),
    ("term-fails-error-5", {}, {}, {200: 5}, (), ["h200", "h201", "h202"], ["failed: winerror 5", "stopped", "stopped"]),
    ("term-error-5-on-an-exited-process-is-gone", {}, {}, {201: 5}, (201,), ["h200", "h201", "h202"], ["stopped", "gone", "stopped"]),
    ("term-error-87-is-gone", {}, {}, {201: 87}, (), ["h200", "h201", "h202"], ["stopped", "gone", "stopped"]),
    ("gone", {}, {201: 87}, {}, (), ["h200", "h202"], ["stopped", "gone", "stopped"]),
    ("open-fails-error-5", {}, {200: 5}, {}, (), ["h201", "h202"], ["failed: winerror 5", "stopped", "stopped"]),
]


@pytest.mark.parametrize("name,skew,open_fail,term_fail,exited,terminated,outcomes", STOPS, ids=[s[0] for s in STOPS])
def test_stop_tree(name, skew, open_fail, term_fail, exited, terminated, outcomes):
    cand = cand_tree()
    created = {p["pid"]: p["created"] + skew.get(p["pid"], 0) for p in cand.tree}
    api = FakeKill(created, open_fail, term_fail, exited)
    attempted = set()
    got = wr.stop_tree(cand, api, attempted)
    assert [o for _, o in got] == outcomes and api.terminated == terminated
    assert len(api.closed) == len(api.opened) - len([1 for p in cand.tree if p["pid"] in open_fail])
    wr.stop_tree(cand, api, attempted)                                    # one attempt per pid per run
    assert api.opened.count(200) == 1


def args(*extra):
    return wr.build_parser().parse_args(["--session-pid", "100", "--session-created", wr.ws._iso(SESSION["created"]), *extra])


def lister_of(procs):
    return lambda: BASE + procs


def go(tmp_path, *extra, procs=None, api=None, lister=None, session_pid=100, now=NOW):
    out = []
    a = wr.build_parser().parse_args(["--session-pid", str(session_pid), "--session-created",
                                      wr.ws._iso(NOW - 3 * 86400 if session_pid == 100 else NOW - 9 * 86400), *extra])
    code = wr.run(a, lister=lister or lister_of(procs or []), api=api, now=now, out=out.append, state_root=tmp_path, rows=ROWS)
    return code, out


TREE = [P(200, 100, "bash.exe", 3 * H, bash_cmd(LOOP)), P(201, 200, "sleep.exe", 15, "sleep 20")]


def test_dry_list_touches_nothing(tmp_path):
    api = FakeKill({})
    code, out = go(tmp_path / "s", procs=TREE, api=api)
    assert code == 0 and api.opened == [] and not (tmp_path / "s").exists()
    assert any(" reported root=200 " in l and "shape=S1" in l for l in out)


def test_apply_stops_logs_and_writes_status(tmp_path):
    api = FakeKill({p["pid"]: p["created"] for p in TREE})
    code, out = go(tmp_path, "--apply", "--trigger", "post-merge", procs=TREE, api=api)
    assert code == 0 and api.terminated == ["h200", "h201"]
    log = (tmp_path / "run.log").read_text(encoding="utf-8").splitlines()
    assert len(log) == 1 and " post-merge sess=100 stopped root=200 age=10800 shape=S1 name=bash.exe cmd=%s kids=sleep.exe/201/15/" % LOOP in log[0]
    status = json.loads(next(tmp_path.glob("100-*/status.json")).read_text(encoding="utf-8"))
    assert status["state"] == "finished" and status["trees_stopped"] == 1 and status["trigger"] == "post-merge"
    assert not list(tmp_path.glob("100-*/lock"))                          # the lock is released


def test_kid_failures_are_on_the_line_and_counts_name_their_unit(tmp_path):
    api = FakeKill({p["pid"]: p["created"] for p in TREE}, term_fail={201: 5})
    code, out = go(tmp_path, "--apply", procs=TREE, api=api)
    log = (tmp_path / "run.log").read_text(encoding="utf-8").splitlines()
    assert code == 0 and len(log) == 1 and " stopped root=200 " in log[0] and log[0].endswith(" fails=sleep.exe/201/failed: winerror 5")
    status = json.loads(next(tmp_path.glob("100-*/status.json")).read_text(encoding="utf-8"))
    assert (status["trees_stopped"], status["procs_stopped"], status["procs_failed"]) == (1, 1, 1)
    assert "1 trees stopped (1 processes), 1 processes failed" in out[-1]


def test_a_root_kept_by_never_reap_is_a_kept_line(tmp_path):
    keep = [P(200, 100, "bash.exe", 3 * H, bash_cmd("while pgrep -f story_run.py; do sleep 60; done"))]
    rows = dict(ROWS, never_reap={"names": [], "cmd_substrings": ["story_run.py"]})
    out, api = [], FakeKill({})
    a = wr.build_parser().parse_args(["--session-pid", "100", "--session-created", wr.ws._iso(SESSION["created"]), "--apply"])
    wr.run(a, lister=lister_of(keep), api=api, now=NOW, out=out.append, state_root=tmp_path, rows=rows)
    log = (tmp_path / "run.log").read_text(encoding="utf-8")
    assert api.opened == [] and " kept root=200 " in log


def test_empty_list_finishes_with_zero(tmp_path):
    code, out = go(tmp_path, "--apply", lister=lambda: [])
    status = json.loads(next(tmp_path.glob("100-*/status.json")).read_text(encoding="utf-8"))
    assert code == 0 and status["state"] == "finished" and status["trees_stopped"] == 0


@pytest.mark.parametrize("fault", ["timeout", "not-json", "raises"])
def test_unreadable_list_is_exit_1_no_stop(tmp_path, fault):
    def lister():
        if fault == "raises":
            raise RuntimeError("boom")
        raise wr.ListError("timed out after 20 s" if fault == "timeout" else "process list is not JSON")

    api = FakeKill({})
    code, out = go(tmp_path, "--apply", lister=lister, api=api)
    status = json.loads(next(tmp_path.glob("100-*/status.json")).read_text(encoding="utf-8"))
    assert code == 1 and api.opened == [] and status["state"] == "unreadable" and "unreadable:" in out[0]


def test_no_session_stops_nothing_one_line(tmp_path):
    out = []
    a = wr.build_parser().parse_args(["--apply"])
    code = wr.run(a, lister=lister_of(TREE), api=FakeKill({}), now=NOW, out=out.append, state_root=tmp_path, rows=ROWS,
                  walker=lambda rows: (None, "no claude.exe ancestor"))
    assert code == 0 and len(out) == 1 and "no-session: no claude.exe ancestor" in out[0]


def test_two_sessions_both_run_same_session_twice_is_busy(tmp_path):
    other = [P(300, 110, "bash.exe", 3 * H, bash_cmd(LOOP))]
    procs = TREE + other + [P(110, 90, "claude.exe", 9 * 86400)]
    api = FakeKill({p["pid"]: p["created"] for p in procs})
    c1, _ = go(tmp_path, "--apply", procs=procs, api=api)
    c2, _ = go(tmp_path, "--apply", procs=procs, api=api, session_pid=110)
    assert (c1, c2) == (0, 0) and len(list(tmp_path.glob("*-*/status.json"))) == 2
    assert len((tmp_path / "run.log").read_text(encoding="utf-8").splitlines()) == 2
    real = time.time()                                                    # lock freshness reads real file mtimes
    held, _ = wr.ws.acquire_lock(wr._session_dir(tmp_path, SESSION), "x", real)
    code, out = go(tmp_path, "--apply", procs=TREE, api=FakeKill({}), now=real)
    assert code == 0 and out[0].startswith("busy:")
    held.release()


def test_orphans_reported_and_stopped_only_by_flag(tmp_path):
    dead = [P(400, 999, "bash.exe", 5 * H, bash_cmd(LOOP))]
    api = FakeKill({400: dead[0]["created"]})
    _, out = go(tmp_path, "--apply", procs=dead, api=api)
    assert api.terminated == [] and any(" reported root=400 " in l and "orphan=yes" in l for l in out)
    _, out = go(tmp_path, "--apply", "--orphans", procs=dead, api=api)
    assert api.terminated == ["h400"]
    assert [json.loads(p.read_text())["orphans"] for p in tmp_path.glob("100-*/status.json")] == [1]


def test_unknown_root_is_logged_and_counted(tmp_path):
    _, out = go(tmp_path, "--apply", procs=[P(510, 100, "cmd.exe", 3 * H, "cmd.exe /c foo")], api=FakeKill({}))
    assert any(" unknown-root root=510 " in l for l in out)
    assert json.loads(next(tmp_path.glob("100-*/status.json")).read_text())["unknown_root"] == 1


def test_pid_filter_and_limit(tmp_path):
    procs = TREE + [P(300, 100, "bash.exe", 3 * H, bash_cmd(LOOP))]
    api = FakeKill({p["pid"]: p["created"] for p in procs})
    go(tmp_path, "--apply", "--pid", "300", procs=procs, api=api)
    assert api.terminated == ["h300"]
    young = [P(200, 100, "bash.exe", 61, bash_cmd(LOOP))]
    api2 = FakeKill({200: young[0]["created"]})
    go(tmp_path / "b", "--apply", "--limit", "60", procs=young, api=api2)
    assert api2.terminated == ["h200"]


# --------------------------------------------------------------------------------------------------------- launcher, WAITS

def test_launch_no_session_spawns_nothing_and_never_raises(tmp_path, monkeypatch):
    spawned = []
    line = wr.launch("session-start", walker=lambda: (None, "no claude.exe ancestor"), spawn=lambda *a: spawned.append(a))
    assert line == "WAITS: no session (no claude.exe ancestor) -- nothing stopped" and spawned == []

    def boom():
        raise RuntimeError("x")

    assert wr.launch("t", walker=boom).startswith("WAITS: reaper not started (RuntimeError")
    (tmp_path / "tools").mkdir()
    (tmp_path / "tools" / "wait_reaper.py").write_text("", encoding="utf-8")
    timeouts = []
    monkeypatch.setattr(wr.ws, "repo_context", lambda git, root: timeouts.append(git.timeout) or types.SimpleNamespace(main_path=tmp_path))
    assert wr.launch("subagent-stop", walker=lambda: (SESSION, ""), spawn=lambda argv, cwd, env: spawned.append((argv, cwd))) is None
    argv, cwd = spawned[0]
    assert argv[argv.index("--session-pid") + 1] == "100" and "--apply" in argv and argv[argv.index("--trigger") + 1] == "subagent-stop"
    assert argv[argv.index("--session-created") + 1] == wr.ws._iso(SESSION["created"]) and cwd == tmp_path
    assert str(tmp_path / "tools" / "wait_reaper.py") in argv and timeouts == [5]            # one git call budget: 5 s
    held = types.SimpleNamespace(main_path=tmp_path)                                         # a caller's repo: no second context
    assert wr.launch("t", walker=lambda: (SESSION, ""), spawn=lambda *a: None, repo=held) is None and timeouts == [5]

    def refuse(argv, cwd, env):
        raise OSError("no")

    assert wr.launch("t", walker=lambda: (SESSION, ""), spawn=refuse).startswith("WAITS: reaper not started (OSError")


WAITS = [
    ("silent-at-zero", {"state": "finished", "trees_stopped": 0, "procs_failed": 0, "unknown_root": 0, "orphans": 0}, None),
    ("running-silent", {"state": "running", "trees_stopped": 0}, None),
    ("counts", {"state": "finished", "finished": "2026-11-17T12:00:00.5", "trigger": "post-merge", "trees_stopped": 2, "procs_failed": 1,
                "unknown_root": 3, "orphans": 0},
     "WAITS: last reap 2026-11-17T12:00:00 (post-merge): 2 trees stopped, 1 processes failed, 3 unknown roots"),
    ("orphans", {"state": "finished", "finished": "2026-11-17T12:00:00", "trigger": "t", "trees_stopped": 0, "procs_failed": 0, "unknown_root": 0,
                 "orphans": 2},
     "WAITS: last reap 2026-11-17T12:00:00 (t): 0 trees stopped, 0 processes failed, 0 unknown roots; 2 calls of dead sessions -- "
     "python -B tools/wait_reaper.py --orphans --apply"),
    ("unreadable", {"state": "unreadable", "reason": "timed out after 20 s"},
     "WAITS: process list unreadable (timed out after 20 s) -- python -B tools/wait_reaper.py"),
]


@pytest.mark.parametrize("name,status,want", WAITS, ids=[w[0] for w in WAITS])
def test_waits_line(tmp_path, name, status, want):
    d = wr._session_dir(tmp_path, SESSION)
    d.mkdir(parents=True)
    (d / "status.json").write_text(json.dumps(status), encoding="utf-8")
    got = wr.waits_line(tmp_path, SESSION)
    assert got == want and (got is None or len(got) <= 200)
    assert wr.waits_line(tmp_path / "none", SESSION) is None
