"""Tests of tools/gitcmd.py, the one git runner: every edge of its contract on a real temporary repository
(piles_testkit.git builds it), plus the argv shape through a recording fake of subprocess.run.

Run from the repo root: python -m pytest tools/test_gitcmd.py -q
"""
import subprocess

import pytest

import gitcmd
import piles_testkit as kit


@pytest.fixture
def repo(tmp_path):
    root = tmp_path / "repo"
    root.mkdir()
    kit.git(root, "init", "-q")
    kit.put(root, "a.txt", "one\n")
    kit.put(root, "папка/файл.txt", "two\n")                 # a non-ASCII path: quotepath would octal-escape it
    kit.git(root, "add", "-A")
    kit.git(root, "commit", "-q", "-m", "first")
    return root


class _Recorder:
    """A subprocess.run that records its call and answers with a canned process."""

    def __init__(self, code=0, out=b"o", err=b"e"):
        self.calls, self.proc = [], subprocess.CompletedProcess([], code, out, err)

    def __call__(self, argv, **kw):
        self.calls.append((argv, kw))
        return self.proc


def test_root_runs_in_that_repo_and_returns_bytes(repo):
    rc, out = gitcmd.git(repo, "rev-parse", "--show-toplevel")
    assert rc == 0 and isinstance(out, bytes)
    assert out.decode().strip().replace("\\", "/").lower() == str(repo).replace("\\", "/").lower()


def test_root_none_means_the_current_directory(repo, monkeypatch):
    monkeypatch.chdir(repo)
    rc, out = gitcmd.git(None, "ls-files")
    assert rc == 0 and b"a.txt" in out
    rec = _Recorder()
    monkeypatch.setattr(gitcmd.subprocess, "run", rec)
    gitcmd.git(None, "status")
    assert rec.calls[0][0] == ["git", "-c", "core.quotepath=false", "status"]      # no -C at all


def test_root_given_is_passed_as_dash_C(monkeypatch, tmp_path):
    rec = _Recorder()
    monkeypatch.setattr(gitcmd.subprocess, "run", rec)
    gitcmd.git(tmp_path, "status", "-s")
    assert rec.calls[0][0] == ["git", "-C", str(tmp_path), "-c", "core.quotepath=false", "status", "-s"]


def test_no_args_is_a_value_error_before_any_subprocess(monkeypatch):
    def never(*a, **k):
        raise AssertionError("a subprocess was started")

    monkeypatch.setattr(gitcmd.subprocess, "run", never)
    for root in (None, "."):
        with pytest.raises(ValueError):
            gitcmd.git(root)
        with pytest.raises(ValueError):
            gitcmd.git(root, stderr=True)


def test_timeout_defaults_to_120_and_a_caller_may_pass_its_own(monkeypatch, tmp_path):
    rec = _Recorder()
    monkeypatch.setattr(gitcmd.subprocess, "run", rec)
    gitcmd.git(tmp_path, "status")
    gitcmd.git(tmp_path, "status", timeout=7)
    assert gitcmd.DEFAULT_TIMEOUT == 120
    assert [kw["timeout"] for _, kw in rec.calls] == [120, 7]


def test_no_shell_captured_output_and_closed_stdin(monkeypatch, tmp_path):
    rec = _Recorder()
    monkeypatch.setattr(gitcmd.subprocess, "run", rec)
    gitcmd.git(tmp_path, "log", "--format=%H; echo hacked")
    argv, kw = rec.calls[0]
    assert isinstance(argv, list) and argv[-1] == "--format=%H; echo hacked"
    assert not kw.get("shell") and kw["capture_output"] is True and kw["stdin"] == subprocess.DEVNULL


def test_git_missing_from_path_is_minus_one_and_bytes_never_an_exception(repo, tmp_path, monkeypatch):
    empty = tmp_path / "empty-path"
    empty.mkdir()
    monkeypatch.setenv("PATH", str(empty))
    rc, out = gitcmd.git(repo, "status")
    assert rc == -1 and isinstance(out, bytes) and out
    rc, out, err = gitcmd.git(repo, "status", stderr=True)
    assert rc == -1 and out == b"" and isinstance(err, bytes) and err


def test_a_timeout_is_minus_one_and_bytes(monkeypatch, tmp_path):
    def slow(argv, **kw):
        raise subprocess.TimeoutExpired(argv, kw["timeout"])

    monkeypatch.setattr(gitcmd.subprocess, "run", slow)
    rc, out = gitcmd.git(tmp_path, "status", timeout=1)
    assert rc == -1 and isinstance(out, bytes) and out


def test_a_nonzero_exit_keeps_its_code_and_stderr_is_asked_for(repo):
    rc, out = gitcmd.git(repo, "rev-parse", "--verify", "--quiet", "no-such-rev^{commit}")
    assert rc == 1 and out == b""
    rc, out, err = gitcmd.git(repo, "show", "no-such-rev:a.txt", stderr=True)
    assert rc != 0 and out == b"" and b"no-such-rev" in err
    rc, out, err = gitcmd.git(repo, "rev-parse", "HEAD", stderr=True)       # the keyword adds a third item, nothing else
    assert rc == 0 and len(out.strip()) == 40 and err == b""


def test_default_return_has_two_items_and_stderr_true_three(repo):
    assert len(gitcmd.git(repo, "status")) == 2
    assert len(gitcmd.git(repo, "status", stderr=True)) == 3


def test_quotepath_is_always_off_so_a_non_ascii_path_is_listed_as_is(repo):
    rc, out = gitcmd.git(repo, "ls-files")
    assert rc == 0 and "папка/файл.txt" in out.decode("utf-8").splitlines()
    assert b'"' not in out and b"\\3" not in out                            # no quoting, no octal escapes


def test_as_text_reads_utf8_with_replacement_and_crlf_and_cr_as_lf():
    """F-11: the one decode chain of the callers that want text (forge_metrics, r3_integration_check, exam_runner)."""
    assert gitcmd.as_text(b"a\r\nb\rc\nd") == "a\nb\nc\nd"
    assert gitcmd.as_text("папка".encode("utf-8")) == "папка"
    assert gitcmd.as_text(b"x\xffy") == "x�y"                            # a bad byte becomes U+FFFD, never an exception
    assert gitcmd.as_text(b"") == ""


def _runner(rc=0, out=b"", err=b"", raises=None):
    def run(root, *args, timeout=gitcmd.DEFAULT_TIMEOUT, stderr=False):
        if raises is not None:
            raise raises
        return rc, out, err
    return run


@pytest.mark.parametrize("name, runner, code, fragment", [
    ("e1_git_missing_rc_minus_one", _runner(-1, b"", b"no git"), "git", "failed to run (no git)"),
    ("rc_128", _runner(128, b"", b"fatal: not a repo\nmore"), "git", "exited 128 (fatal: not a repo)"),
    ("e1a_runner_raises", _runner(raises=OSError("boom")), "git", "raised OSError"),
    ("e2_one_line_only", _runner(0, b".git\n"), "git", "exited 0"),
    ("e2_empty_stdout", _runner(0, b""), "git", "exited 0"),
    ("e3_main_checkout_relative", _runner(0, b".git\n.git\n"), "", ""),
    ("e5_bare_common_dir", _runner(0, b"bare.git\nbare.git\n"), "not-a-checkout", "not a .git directory"),
    ("e5_three_lines_only_two_read", _runner(0, b".git\nbare.git\n.git\n"), "not-a-checkout", "not a .git directory"),
])
def test_main_checkout_rows(tmp_path, name, runner, code, fragment):
    c, got_code, why = gitcmd.main_checkout(tmp_path, runner=runner)
    assert got_code == code and fragment in why, name
    if code == "":
        assert c.path == tmp_path.resolve() and c.linked is False and why == ""
    else:
        assert c is None


def test_main_checkout_resolve_oserror_row(tmp_path, monkeypatch):
    def boom(self, *a, **k):
        raise OSError("no")

    monkeypatch.setattr(gitcmd.Path, "resolve", boom)
    c, code, why = gitcmd.main_checkout(tmp_path, runner=_runner(0, b".git\n.git\n"))
    assert c is None and code == "resolve" and "does not resolve" in why


def test_main_checkout_real_linked_worktree_row(repo, tmp_path):
    wt = tmp_path / "wt"
    kit.git(repo, "worktree", "add", "-q", str(wt), "-b", "side")
    c, code, why = gitcmd.main_checkout(wt)
    assert code == "" and c.linked is True and c.path == repo.resolve()
    c, code, why = gitcmd.main_checkout(repo)
    assert code == "" and c.linked is False and c.path == repo.resolve()


@pytest.mark.parametrize("raw, expected", [
    (b"", []),
    ("", []),
    (b" M a.txt\0", [(" M", "a.txt")]),
    (b"?? new.txt\0", [("??", "new.txt")]),
    (b"R  new.txt\0old.txt\0 M b.txt\0", [("R ", "new.txt"), (" M", "b.txt")]),
    (b"C  copy.txt\0orig.txt\0?? c.txt\0", [("C ", "copy.txt"), ("??", "c.txt")]),
    (b" M a.txt\0\0", [(" M", "a.txt")]),                                 # E9 trailing NUL
    (b"R  new.txt\0", [("R ", "new.txt")]),                               # E10 rename without origin
    (b" M a\xffb.txt\0 M c.txt\0", [(" M", "a�b.txt"), (" M", "c.txt")]),   # E11
    (b" M a\rb.txt\0", [(" M", "a\rb.txt")]),                             # E12 CR kept
    (b" Mx\0 M ab.txt\0", [(" M", "ab.txt")]),                           # 3-char record skipped
    (b"\0", []),                                                          # a lone NUL
    (b"?? ab\0", [("??", "ab")]),                                         # 4-char record kept
    (b"nonulblob", [("no", "ulblob")]),                                   # NUL-free blob: one record
    ("\udcff M a.txt\0", None),                                           # str with a surrogate escape: never raises
])
def test_parse_status_z_rows(raw, expected):
    got = gitcmd.parse_status_z(raw)
    if expected is not None:
        assert got == expected
    assert isinstance(got, list)
    if isinstance(raw, bytes):
        assert gitcmd.parse_status_z(raw.decode("utf-8", "replace")) == got      # bytes and str give equal lists
