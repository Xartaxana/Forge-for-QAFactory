"""registry_preflight (FG7-92): the rule table, the `run` door with a fake runner, the `command_for` round trip."""
import shlex
import subprocess
import sys
from pathlib import Path

import pytest

TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))
import registry_preflight as RP  # noqa: E402

R = Path("C:/repo") if sys.platform == "win32" else Path("/repo")
S = RP.SCRIPTS
T = RP.TESTS


@pytest.mark.parametrize("path, want", [
    (S + "/x.py", ["census", "driver-layers", "read-json", "lint"]),
    (T + "/fixtures/judgment-census.json", ["census"]),
    (T + "/test-layers.json", ["test-layers"]),
    (S + "/slow_tests.json", ["test-layers"]),
    (T + "/fixtures/driver-layers.json", ["driver-layers"]),
    (T + "/test_x.py (new)", ["test-layers", "lint"]),
    (T + "/test_x.py", ["lint"]),                                  # a content edit lists nothing new
    (RP.PKG + "/agents/new.md (new)", ["census"]),
    (RP.PKG + "/agents/old.md", []),
    ("tools/x.py", ["lint"]),
    ("docs/x.md", []),
    (str(R / "tools" / "x.py"), ["lint"]),                         # absolute
    ("tools\\x.py", ["lint"]),                                     # backslash
    ("tools", ["lint"]),                                           # a directory selects every row with a sign under it
    (RP.PKG, ["census", "driver-layers", "read-json", "test-layers", "lint"]),
    (str(R.parent / "elsewhere" / "tools" / "x.py"), []),          # outside the repo
    ("", ["census", "driver-layers", "read-json", "test-layers", "lint"]),
])
def test_rules_for_table(path, want):
    assert RP.rules_for([path], repo=R) == want


def test_rules_for_forms_and_deleted(monkeypatch):
    assert RP.rules_for([]) == [] and RP.command_for([]) is None
    monkeypatch.setattr(RP, "_normcase", str.lower)                 # the Windows fold, whatever the host
    assert RP.rules_for([str(R).upper().replace("\\", "/") + "/tools/x.py (new)"], repo=R) == ["lint"]
    assert RP.select([("tools/x.py", "D")]) == ["lint"]             # a deleted file keeps its baseline rows to be judged
    assert RP.select([(T + "/test_x.py", "D")]) == ["test-layers", "lint"]


def mkrepo(tmp_path, files):
    def g(*a):
        subprocess.run(["git", "-C", str(tmp_path), "-c", "user.name=t", "-c", "user.email=t@t", *a], check=True,
                       capture_output=True)
    g("init", "-q", "-b", "main")
    (tmp_path / "README").write_text("a\n")
    g("add", "-A"), g("commit", "-q", "-m", "base")
    g("checkout", "-q", "-b", "feat")
    for rel, text in files.items():
        f = tmp_path / rel
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(text)
    g("add", "-A"), g("commit", "-q", "-m", "feat", "--allow-empty")
    return tmp_path


def run_pf(repo, runner):
    out = []
    rep = RP.preflight(repo, "main", "feat", out=out.append, runner=runner)
    return rep, out


def never(argv, timeout):
    raise AssertionError("the runner must not be called")


def test_empty_diff_and_git_failure(tmp_path):
    repo = mkrepo(tmp_path, {})
    rep, out = run_pf(repo, never)
    assert out == ["registry preflight: no change against main"] and rep.empty and rep.code() == 0
    out = []
    rep = RP.preflight(repo, "nobase", "feat", out=out.append, runner=never)
    assert rep.rows == [] and rep.code() == 2 and out[0].startswith("registry preflight: cannot judge (git diff: ")


@pytest.mark.parametrize("n, tail", [(10, ""), (11, " +1 more")])
def test_no_rule_list_is_cut_at_ten(tmp_path, n, tail):
    repo = mkrepo(tmp_path, {f"docs/f{i:02d}.md": "x" for i in range(n)})
    rep, out = run_pf(repo, never)
    names = ", ".join(f"docs/f{i:02d}.md" for i in range(10))
    assert out[0] == f"registry preflight: no rule for {n} file(s): {names}{tail}" and len(rep.no_rule) == n
    assert out[-1].startswith("registry preflight: 0 run, 0 red, 0 cannot judge -- the merge goes on")


@pytest.mark.parametrize("case", ["ok-red", "crash", "timeout", "budget"])
def test_rows_never_read_ok_when_unjudged(tmp_path, monkeypatch, case):
    repo = mkrepo(tmp_path, {S + "/x.py": "x = 1\n"})
    calls = []
    clock = [0.0]
    monkeypatch.setattr(RP, "_clock", lambda: clock[0])

    def runner(argv, timeout):
        rid = argv[argv.index("check") + 1]
        calls.append(rid)
        assert argv[argv.index("--root") + 1] != str(repo) and Path(argv[argv.index("--root") + 1]).name.startswith("preflight-")
        if case == "ok-red":
            return (1, f"{RP.MARK} {rid} RED\n  C1: a\n  +3 more\n", "") if rid == "census" else (0, "", "")
        if case == "crash":
            return 3, "", "Traceback\nImportError: no x"
        if case == "timeout":
            raise subprocess.TimeoutExpired(argv, timeout)
        clock[0] += 61.0
        return 0, "", ""
    rep, out = run_pf(repo, runner)
    text = "\n".join(out)
    states = {r[0]: r[1] for r in rep.rows}
    if case == "ok-red":
        assert states == {"census": "red", "driver-layers": "ok", "read-json": "ok", "lint": "ok"} and rep.code() == 1
        assert "census RED (0.0 s)\n  C1: a\n  +3 more\nregistry preflight: driver-layers ok" in text
    elif case == "crash":
        assert set(states.values()) == {"cannot"} and "exit 3: ImportError: no x" in text and " ok (" not in text
    elif case == "timeout":
        assert set(states.values()) == {"cannot"} and "timeout after 30 s" in text and len(calls) == 4
    else:
        assert calls == ["census"] and "driver-layers cannot judge (budget spent)" in text and states["lint"] == "cannot"
    assert out[-1].startswith("registry preflight: ") and "the merge goes on" in out[-1] and rep.code() in (1, 2)
    assert not list((repo / ".claude" / "worktrees").glob("preflight-*"))        # the tree is gone, the runner crashed or not


@pytest.mark.parametrize("n, lines", [(5, 5), (6, 6)])
def test_red_problem_lines_are_cut_at_five(n, lines):
    got = RP.row_lines("census", "red", 1.0, [f"p{i}" for i in range(n)])
    assert got[0] == "registry preflight: census RED (1.0 s)" and len(got) == 1 + 5 + (n > 5)
    assert (got[-1] == "  +1 more") == (n == 6)


@pytest.mark.parametrize("paths, lint", [
    ([], None), ([S + "/x.py"], [S + "/x.py"]), (["tools/a.py", "tools/b b.py (new)"], ["tools/a.py", "tools/b b.py"]),
    ([str(R / "tools" / "a.py")], ["tools/a.py"]), (["docs/x.md"], None), (["tools"], None),
    ([T + "/test_x.py (new)"], [T + "/test_x.py"]),
])
def test_command_for_round_trips_through_the_check_parser(paths, lint):
    cmd = RP.command_for(paths, repo=R)
    want = [i for i in RP.rules_for(paths, repo=R) if i != "lint" or lint]          # a lint with no file to narrow to is dropped
    if not want:
        assert cmd is None
        return
    assert "`" not in cmd and chr(10) not in cmd and "test_" not in cmd.split("--paths")[0]
    a = RP._parser().parse_args(shlex.split(cmd)[3:])
    assert a.cmd == "check" and a.ids == want and (a.paths or None) == lint
