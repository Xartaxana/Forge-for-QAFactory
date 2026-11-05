"""Tests for tools/ci_read.py (GitHub Actions reader, GM1-4): urlopen is stubbed (no network, except the redirect test,
which talks to a throw-away server on 127.0.0.1), the token is a dummy, `origin` is stubbed unless a test says otherwise.

Run from the repo root: python -m pytest tools/test_ci_read.py -q
"""

import http.server
import io
import json
import sys
import threading
import urllib.error
import urllib.request
import zipfile
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))

import ci_read  # noqa: E402
import gitcmd  # noqa: E402

TOKEN = "ghp_secretvalue123"
BASE = "https://api.github.com/repos/o/r"
GITHUB_ORIGIN = "https://github.com/o/r.git"
try:
    import ci_read_gitlab    # the module that is deleted at the move: tests that need it are skipped without it
    OLD_HOST_URL = ci_read_gitlab.HOST + "/group/project.git"
    OLD_HOST_NAME = ci_read_gitlab.HOST.split("//", 1)[1]
except ImportError:
    ci_read_gitlab = None
    OLD_HOST_URL = OLD_HOST_NAME = None
needs_old_backend = pytest.mark.skipif(ci_read_gitlab is None, reason="the old backend module is deleted")


class _Resp:
    def __init__(self, body, status=200):
        self._body = body if isinstance(body, bytes) else body.encode("utf-8")
        self.status = status

    def read(self, n=None):
        return self._body if n is None else self._body[:n]

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


def http_error(code, body=""):
    return urllib.error.HTTPError("u", code, "x", {}, io.BytesIO(body.encode()))


def make_zip(members, deflate=False):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED if deflate else zipfile.ZIP_STORED) as archive:
        for name, data in members.items():
            archive.writestr(name, data)
    return buf.getvalue()


@pytest.fixture(autouse=True)
def no_real_config(monkeypatch, tmp_path):
    """Every test reads an EMPTY tmp root (no tools/dev.config.yaml), never the real one, and not the doors."""
    monkeypatch.delenv("QA_DEV_CONFIG", raising=False)
    monkeypatch.delenv("QA_CI_REPO", raising=False)
    monkeypatch.setattr(ci_read, "ROOT", tmp_path)
    return tmp_path


def write_config(root, text):
    (root / "tools").mkdir(exist_ok=True)
    (root / "tools" / "dev.config.yaml").write_text(text, encoding="utf-8")


@pytest.fixture
def set_origin(monkeypatch):
    """set_origin(url) makes `git remote get-url origin` answer url; set_origin(None) = there is no origin."""
    def setter(url):
        def fake_git(root, *args, **kwargs):
            assert args == ("remote", "get-url", "origin")
            return (1, b"") if url is None else (0, url.encode("utf-8") + b"\n")
        monkeypatch.setattr(ci_read.gitcmd, "git", fake_git)
    setter(GITHUB_ORIGIN)
    return setter


@pytest.fixture
def net(monkeypatch, set_origin):
    """Stub urlopen: records requests; answers with the first route whose needle is in the URL, else net.body."""
    class Net:
        body = "{}"
        error = None
        routes = []

    state = Net()
    state.requests = []
    state.routes = []

    def fake_urlopen(req, timeout=None):
        state.requests.append(req)
        if state.error:
            raise state.error
        for needle, answer in state.routes:
            if needle in req.full_url:
                if isinstance(answer, Exception):
                    raise answer
                return answer if isinstance(answer, _Resp) else _Resp(answer)
        return _Resp(state.body)

    monkeypatch.setattr(urllib.request, "urlopen", fake_urlopen)
    monkeypatch.setenv("GITHUB_TOKEN", TOKEN)
    return state


def runs_json(*runs):
    return json.dumps({"workflow_runs": list(runs)})


# ---- the choice of the backend: by `origin`, before any request --------------------------------------------------

GITHUB_FORMS = [
    "git@github.com:o/r.git",
    "https://github.com/o/r",
    "ssh://git@github.com/o/r.git",
    "HTTPS://GitHub.com/o/r/",
    "https://user:tok@github.com/o/r",
]
REFUSED_FORMS = [
    ("https://github.com@evil.example/o/r", "this tool reads GitHub only; origin host is evil.example"),
    ("https://github.com.evil/x/y", "this tool reads GitHub only; origin host is github.com.evil"),
    ("git@github.com:o/r/extra", "the origin on github.com does not name exactly owner/repo"),
]


@pytest.fixture
def no_request(monkeypatch):
    def boom(*args, **kwargs):
        raise AssertionError("a request was made before the backend was chosen")
    monkeypatch.setattr(urllib.request, "urlopen", boom)


@pytest.mark.parametrize("url", GITHUB_FORMS + [u for u, _ in REFUSED_FORMS] + [None, "/some/local/path"])
def test_choosing_the_backend_makes_no_request(url, no_request, set_origin):
    set_origin(url)
    try:
        ci_read.backend_for(ci_read.ROOT)
    except ci_read.Refusal:
        pass


@pytest.mark.parametrize("url", GITHUB_FORMS)
def test_github_origin_forms_select_github_owner_repo(url, net, set_origin, capsys):
    set_origin(url)
    net.body = runs_json()
    assert ci_read.main(["pipelines"]) == 0
    assert net.requests[0].full_url == BASE + "/actions/runs?per_page=5"
    assert "tok" not in capsys.readouterr().out          # the userinfo of the URL is never printed


@pytest.mark.parametrize("url, text", REFUSED_FORMS)
def test_a_wrong_host_or_path_is_refused_by_name_without_the_url(url, text, net, set_origin, capsys):
    set_origin(url)
    assert ci_read.main(["start"]) == 2
    out = capsys.readouterr().out
    assert out == text + "\n" or out.startswith(text)
    assert "extra" not in out and "/x/y" not in out and "/o/r" not in out and net.requests == []


@needs_old_backend
def test_the_host_of_the_old_backend_selects_it_and_the_request_goes_there(net, set_origin, monkeypatch):
    set_origin(OLD_HOST_URL)
    monkeypatch.setenv("GITLAB_TOKEN", TOKEN)
    monkeypatch.setattr(ci_read_gitlab, "ROOT", ci_read.ROOT)
    net.body = "[]"
    assert ci_read.main(["pipelines"]) == 0
    assert net.requests[0].full_url.startswith(ci_read_gitlab.HOST + "/")        # the old host, not api.github.com
    assert not net.requests[0].full_url.startswith(ci_read.API)
    assert net.requests[0].get_header("Private-token") == TOKEN


@needs_old_backend
def test_the_old_backend_module_absent_means_a_refusal_naming_only_the_host(net, set_origin, monkeypatch, capsys):
    set_origin(OLD_HOST_URL)
    monkeypatch.setitem(sys.modules, "ci_read_gitlab", None)
    assert ci_read.main(["pipelines"]) == 2
    assert capsys.readouterr().out == "this tool reads GitHub only; origin host is %s\n" % OLD_HOST_NAME
    assert net.requests == []
    set_origin(GITHUB_ORIGIN)                             # and GitHub works with the module gone
    net.body = runs_json()
    assert ci_read.main(["pipelines"]) == 0


def test_no_origin_is_a_refusal_with_the_command_to_run(net, set_origin, capsys):
    set_origin(None)
    assert ci_read.main(["pipelines"]) == 2
    out = capsys.readouterr().out
    assert out.startswith("no origin remote: git remote add origin ") and net.requests == []


def test_a_real_git_tree_is_read_through_gitcmd(tmp_path):
    assert gitcmd.git(tmp_path, "init", "-q")[0] == 0
    with pytest.raises(ci_read.Refusal, match="no origin remote"):
        ci_read.backend_for(tmp_path)
    assert gitcmd.git(tmp_path, "remote", "add", "origin", "git@github.com:o/r.git")[0] == 0
    assert ci_read.backend_for(tmp_path).name == "GitHub"


@pytest.mark.parametrize("repo", ["a/b", "My_Org/repo.name-2"])
def test_the_door_QA_CI_REPO_selects_github_without_reading_origin(repo, net, monkeypatch, capsys):
    def never(*args, **kwargs):
        raise AssertionError("origin was read although QA_CI_REPO is set")
    monkeypatch.setattr(ci_read.gitcmd, "git", never)
    monkeypatch.setenv("QA_CI_REPO", repo)
    net.body = runs_json()
    assert ci_read.main(["pipelines"]) == 0
    assert net.requests[0].full_url.startswith("https://api.github.com/repos/%s/" % repo)


@pytest.mark.parametrize("bad", ["o", "o/r/x", "o r/x", "../x", "o/..", "/r", "o/", "о/р"])
def test_the_door_with_a_bad_form_is_refused_naming_the_form(bad, net, monkeypatch, capsys):
    monkeypatch.setenv("QA_CI_REPO", bad)
    assert ci_read.main(["pipelines"]) == 2
    out = capsys.readouterr().out
    assert out.startswith("QA_CI_REPO must be owner/repo") and net.requests == []


# ---- the token ----------------------------------------------------------------------------------------------------

def test_no_config_uses_GITHUB_TOKEN_with_one_stderr_line(net, capsys):
    net.body = runs_json()
    assert ci_read.main(["pipelines"]) == 0
    err = capsys.readouterr().err.splitlines()
    assert [ln for ln in err if ln.startswith("ci_read:")] == ["ci_read: no tools/dev.config.yaml, token variable GITHUB_TOKEN"]


def test_missing_token_prints_one_line_exits_2_and_makes_no_request(net, monkeypatch, capsys):
    monkeypatch.delenv("GITHUB_TOKEN")
    assert ci_read.main(["pipelines"]) == 2
    lines = capsys.readouterr().out.splitlines()
    assert len(lines) == 1 and lines[0].startswith("GITHUB_TOKEN is not set (its name comes from ")
    assert lines[0].endswith("export it as GITHUB_TOKEN") and net.requests == []


def test_the_name_comes_from_github_token_env_of_the_config(net, monkeypatch, capsys, no_real_config):
    write_config(no_real_config, "github_token_env: MY_GH_TOKEN\n")
    monkeypatch.delenv("MY_GH_TOKEN", raising=False)
    assert ci_read.main(["pipelines"]) == 2
    assert capsys.readouterr().out.startswith("MY_GH_TOKEN is not set (its name comes from the token variable named by "
                                              "github_token_env")
    monkeypatch.setenv("MY_GH_TOKEN", TOKEN)
    net.body = runs_json()
    assert ci_read.main(["pipelines"]) == 0
    assert net.requests[0].get_header("Authorization") == "Bearer " + TOKEN


@pytest.mark.parametrize("text", ["gitlab_token_env: MY_GL_TOKEN\n", "developer: some-dev\n", "# nothing\n"],
                         ids=["old-config", "key-absent", "empty-file"])
def test_a_file_without_github_token_env_is_refused_naming_the_key(text, net, capsys, no_real_config):
    """An old config (only gitlab_token_env) is refused, not silently given GITHUB_TOKEN; GITHUB_TOKEN IS set here."""
    write_config(no_real_config, text)
    assert ci_read.main(["start"]) == 2
    out = capsys.readouterr().out.strip().splitlines()
    assert len(out) == 1 and "github_token_env" in out[0] and "dev.config.yaml" in out[0]
    assert "GitHub token" in out[0] and net.requests == []


# ---- the commands -------------------------------------------------------------------------------------------------

def test_every_request_carries_the_three_headers_and_the_token_only_unredirected(net):
    net.body = runs_json()
    ci_read.main(["pipelines"])
    req = net.requests[0]
    assert req.get_header("Authorization") == "Bearer " + TOKEN
    assert "Authorization" in req.unredirected_hdrs and "Authorization" not in req.headers
    assert req.get_header("Accept") == "application/vnd.github+json"
    assert req.get_header("X-github-api-version") == "2022-11-28"


def test_pipelines_request_and_output(net, capsys):
    net.body = runs_json(
        {"id": 7, "status": "completed", "conclusion": "success", "display_title": "canon feature/x",
         "head_sha": "7883565abcdef", "event": "workflow_dispatch"},
        {"id": 8, "status": "in_progress", "conclusion": None, "display_title": "ci", "head_sha": "abc",
         "event": "push"})
    assert ci_read.main(["pipelines", "--n", "3"]) == 0
    req = net.requests[0]
    assert req.full_url == BASE + "/actions/runs?per_page=3" and req.get_method() == "GET"
    assert capsys.readouterr().out == "7 success canon feature/x 7883565a workflow_dispatch\n8 in_progress ci abc push\n"


def test_pipelines_with_no_runs_says_so_and_exits_0(net, capsys):
    net.body = runs_json()
    assert ci_read.main(["pipelines"]) == 0
    assert capsys.readouterr().out == "(no runs)\n"


def test_jobs_path_and_output(net, capsys):
    net.body = json.dumps({"jobs": [{"id": 11, "name": "package-full", "status": "completed", "conclusion": "failure"},
                                    {"id": 12, "name": "lint", "status": "queued", "conclusion": None}]})
    assert ci_read.main(["jobs", "555"]) == 0
    assert net.requests[0].full_url == BASE + "/actions/runs/555/jobs?per_page=100"
    assert capsys.readouterr().out == "11 package-full failure\n12 lint queued\n"


def test_log_default_grep_keeps_only_matching_lines(net, capsys):
    net.body = "ok line\nFAILED test_x\n=== 1 failed ===\nTraceback (most recent call last)\nboring\nValueError: x\n"
    assert ci_read.main(["log", "42"]) == 0
    assert net.requests[0].full_url == BASE + "/actions/jobs/42/logs"
    assert capsys.readouterr().out.splitlines() == [
        "FAILED test_x", "=== 1 failed ===", "Traceback (most recent call last)", "ValueError: x", "(4 of 4 lines)"]


def test_log_zero_matches_and_empty_log(net, capsys):
    net.body = "lint ratchet: 17 new\nsomething\n"
    ci_read.main(["log", "42"])
    assert capsys.readouterr().out.splitlines() == [
        "(0 of 0 lines)", "(the text has 2 lines and none matched the grep, --grep '' prints them all)"]
    net.body = ""
    ci_read.main(["log", "42"])
    assert capsys.readouterr().out == "(0 of 0 lines)\n"


def artifact_routes(net, zipped, rows=None):
    net.routes = [("/artifacts?per_page=100", json.dumps({"artifacts": rows or [
        {"id": 77, "name": "ci-out", "expired": False}, {"id": 78, "name": "old", "expired": True}]})),
                  ("/artifacts/77/zip", zipped)]


def test_artifact_reads_a_member_of_the_zip_and_every_line_without_grep(net, capsys):
    artifact_routes(net, make_zip({"report.txt": "one\ntwo\n"}))
    assert ci_read.main(["artifact", "9", "ci-out/report.txt"]) == 0
    assert [r.full_url for r in net.requests] == [BASE + "/actions/runs/9/artifacts?per_page=100",
                                                  BASE + "/actions/artifacts/77/zip"]
    assert capsys.readouterr().out == "one\ntwo\n(2 of 2 lines)\n"
    assert ci_read.main(["artifact", "9", "ci-out/report.txt", "--grep", "tw"]) == 0
    assert capsys.readouterr().out == "two\n(1 of 1 lines)\n"


def test_artifact_member_path_may_be_nested(net, capsys):
    artifact_routes(net, make_zip({"a/b/c": "deep\n"}))
    assert ci_read.main(["artifact", "9", "ci-out/a/b/c"]) == 0
    assert capsys.readouterr().out == "deep\n(1 of 1 lines)\n"


@pytest.mark.parametrize("name", ["old", "missing"], ids=["expired", "absent"])
def test_artifact_expired_or_absent_lists_the_names_exit_1(name, net, capsys):
    artifact_routes(net, make_zip({"x": "y"}))
    assert ci_read.main(["artifact", "9", name + "/x"]) == 1
    out = capsys.readouterr().out
    assert "ci-out, old (expired)" in out and len(net.requests) == 1


def test_artifact_member_absent_exit_1_and_not_a_zip_exit_1(net, capsys):
    artifact_routes(net, make_zip({"x": "y"}))
    assert ci_read.main(["artifact", "9", "ci-out/nope.txt"]) == 1
    assert "nope.txt is not in the artifact ci-out; members: x" in capsys.readouterr().out
    artifact_routes(net, b"this is not a zip")
    assert ci_read.main(["artifact", "9", "ci-out/x"]) == 1
    assert capsys.readouterr().out == "the artifact is not a readable zip\n"


@pytest.mark.parametrize("path", ["noslash", "name/", "/member"])
def test_artifact_without_a_name_and_a_member_is_refused_exit_2_before_any_request(path, net, capsys):
    assert ci_read.main(["artifact", "9", path]) == 2
    assert "artifact needs <name>/<path inside the zip>" in capsys.readouterr().out and net.requests == []


def test_the_archive_size_limit_passes_at_the_limit_and_refuses_one_byte_over(net, monkeypatch, capsys):
    zipped = make_zip({"report.txt": "hello\n"})
    artifact_routes(net, zipped)
    monkeypatch.setattr(ci_read, "MAX_ARTIFACT_BYTES", len(zipped))
    assert ci_read.main(["artifact", "9", "ci-out/report.txt"]) == 0
    assert capsys.readouterr().out == "hello\n(1 of 1 lines)\n"
    monkeypatch.setattr(ci_read, "MAX_ARTIFACT_BYTES", len(zipped) - 1)
    assert ci_read.main(["artifact", "9", "ci-out/report.txt"]) == 1
    assert "larger than %d bytes" % (len(zipped) - 1) in capsys.readouterr().out


def test_the_member_size_limit_is_checked_before_the_member_is_read(net, monkeypatch, capsys):
    """A small archive can hold a huge member: the limit is on the member too, at the limit passes, over refuses."""
    at = make_zip({"big.txt": "a" * 5000}, deflate=True)
    artifact_routes(net, at)
    monkeypatch.setattr(ci_read, "MAX_ARTIFACT_BYTES", 5000)
    assert len(at) < 5000
    assert ci_read.main(["artifact", "9", "ci-out/big.txt", "--tail", "1"]) == 0
    assert capsys.readouterr().out.splitlines()[-1] == "(1 of 1 lines)"
    artifact_routes(net, make_zip({"big.txt": "a" * 5001}, deflate=True))
    assert ci_read.main(["artifact", "9", "ci-out/big.txt"]) == 1
    assert "the member is larger than 5000 bytes" in capsys.readouterr().out


def test_start_dispatches_canon_with_the_ref_input(net, capsys):
    net.routes = [("/dispatches", _Resp(b"", status=204))]
    assert ci_read.main(["start", "--ref", "release"]) == 0
    req = net.requests[0]
    assert req.full_url == BASE + "/actions/workflows/canon.yml/dispatches" and req.get_method() == "POST"
    assert json.loads(req.data) == {"ref": "main", "inputs": {"ref": "release"}}
    assert req.get_header("Content-type") == "application/json"
    assert capsys.readouterr().out == "dispatched canon.yml for release; find the run: ci_read.py pipelines\n"
    ci_read.main(["start"])
    assert json.loads(net.requests[1].data)["inputs"] == {"ref": "main"}


def test_start_with_a_non_ascii_ref_and_a_slash_goes_into_the_json_as_is_and_out_sanitized(net, capsys):
    net.routes = [("/dispatches", _Resp(b"", status=204))]
    assert ci_read.main(["start", "--ref", "фича/x\x1b[31m"]) == 0
    assert json.loads(net.requests[0].data)["inputs"]["ref"] == "фича/x\x1b[31m"
    out = capsys.readouterr().out
    assert out == "dispatched canon.yml for ????/x?[31m; find the run: ci_read.py pipelines\n"


def test_start_404_says_canon_is_not_on_the_default_branch_and_403_prints_the_status(net, capsys):
    net.error = http_error(404, '{"message":"Not Found"}')
    assert ci_read.main(["start"]) == 1
    assert capsys.readouterr().out == ("canon.yml is not on the default branch, or the token cannot see this repository\n")
    net.error = http_error(403, '{"message":"API rate limit exceeded"}')
    assert ci_read.main(["start"]) == 1
    out = capsys.readouterr().out
    assert out.startswith("HTTP 403: ") and "API rate limit exceeded" in out and TOKEN not in out


def test_a_403_prints_http_403_with_the_first_200_sanitized_chars(net, capsys):
    net.error = http_error(403, "<html>\x1b[1m" + "A" * 400)
    assert ci_read.main(["jobs", "1"]) == 1
    line = capsys.readouterr().out.rstrip("\n")
    assert line.startswith("HTTP 403: ?html??[1mAAA") and len(line) == len("HTTP 403: ") + 200


# ---- the token never leaves api.github.com (a real redirect) ----------------------------------------------------

class _Server:
    """A throw-away server on 127.0.0.1: /api/... redirects to /storage/..., both record the Authorization header."""

    def __init__(self):
        seen = self.seen = []
        outer = self

        class Handler(http.server.BaseHTTPRequestHandler):
            def do_GET(self):
                seen.append((self.path, self.headers.get("Authorization")))
                if self.path.startswith("/repos/o/r/actions/jobs/5/logs") or self.path.startswith("/control"):
                    self.send_response(302)
                    self.send_header("Location", "http://127.0.0.1:%d/storage/log" % outer.port)
                    self.end_headers()
                    return
                body = b"FAILED stored\n"
                self.send_response(200)
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def log_message(self, *args):
                pass

        self.httpd = http.server.HTTPServer(("127.0.0.1", 0), Handler)
        self.port = self.httpd.server_address[1]
        self.thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        self.thread.start()

    def close(self):
        self.httpd.shutdown()
        self.httpd.server_close()


def test_a_redirect_is_followed_without_the_authorization_header(monkeypatch, set_origin, capsys):
    server = _Server()
    try:
        monkeypatch.setattr(ci_read, "API", "http://127.0.0.1:%d" % server.port)
        monkeypatch.setenv("GITHUB_TOKEN", TOKEN)
        assert ci_read.main(["log", "5"]) == 0
        assert capsys.readouterr().out == "FAILED stored\n(1 of 1 lines)\n"
        assert server.seen[0] == ("/repos/o/r/actions/jobs/5/logs", "Bearer " + TOKEN)
        assert server.seen[1] == ("/storage/log", None)                   # the second request carries no token
        # control: the same redirect with an ordinary header DOES carry it, so the assertion above can fail
        ordinary = urllib.request.Request("http://127.0.0.1:%d/control" % server.port)
        ordinary.add_header("Authorization", "Bearer " + TOKEN)
        urllib.request.urlopen(ordinary, timeout=10).read()
        assert server.seen[-1] == ("/storage/log", "Bearer " + TOKEN)
    finally:
        server.close()


# ---- the token value and the interactive battery ------------------------------------------------------------------

@pytest.mark.parametrize("argv", [["pipelines"], ["jobs", "1"], ["log", "1"], ["artifact", "1", "n/x"], ["start"]])
def test_the_token_is_never_printed_on_any_road(argv, net, capsys):
    for error in (http_error(401, "bad credentials"), urllib.error.URLError("no route"), None):
        net.error = error
        net.routes = []
        net.body = "{}"
        ci_read.main(argv)
    seen = capsys.readouterr()
    assert TOKEN not in seen.out and TOKEN not in seen.err


def test_n_above_the_page_cap_is_refused_naming_the_cap_and_makes_no_request(net, capsys):
    assert ci_read.main(["pipelines", "--n", "1000"]) == 2
    assert capsys.readouterr().out == "GitHub returns at most 100 per page: --n 1000 is refused, use 100 or less\n"
    assert net.requests == []
    assert ci_read.main(["pipelines", "--n", "0"]) == 2 and net.requests == []
    net.body = runs_json()
    assert ci_read.main(["pipelines", "--n", "100"]) == 0                  # AT the cap passes
    assert net.requests[0].full_url.endswith("per_page=100")
    assert ci_read.main(["pipelines", "--n", "101"]) == 2                  # one beyond does not


def test_the_n_refusal_comes_before_the_token_is_read(net, monkeypatch, capsys):
    monkeypatch.delenv("GITHUB_TOKEN")
    assert ci_read.main(["pipelines", "--n", "1000"]) == 2
    assert "GitHub returns at most 100 per page" in capsys.readouterr().out


def test_tail_is_applied_after_the_grep_a_huge_tail_is_fine_and_less_than_one_is_rejected(net, capsys):
    net.body = "\n".join(["keep %d" % i if i % 2 == 0 else "drop %d" % i for i in range(10)]) + "\n"
    assert ci_read.main(["log", "1", "--grep", "keep", "--tail", "2"]) == 0
    assert capsys.readouterr().out.splitlines() == ["keep 6", "keep 8", "(2 of 5 lines)"]
    assert ci_read.main(["log", "1", "--grep", "", "--tail", str(10 ** 12)]) == 0
    assert capsys.readouterr().out.splitlines()[-1] == "(10 of 10 lines)"
    for bad in ("0", "-3", "x"):
        with pytest.raises(SystemExit):
            ci_read.main(["log", "1", "--tail", bad])


def test_cyrillic_and_control_bytes_in_a_log_become_question_marks(net, capsys):
    net.body = "ошибка Error: \x1b[31mred\x1b[0m\tтест\n".encode("utf-8")
    assert ci_read.main(["log", "1"]) == 0
    out = capsys.readouterr().out
    assert out == "?????? Error: ?[31mred?[0m" + "?" + "????" + "\n(1 of 1 lines)\n"


def test_a_log_that_is_not_utf8_does_not_crash(net, capsys):
    net.body = b"\xff\xfe Error: bad bytes\n"
    assert ci_read.main(["log", "1"]) == 0
    assert capsys.readouterr().out.endswith("(1 of 1 lines)\n")


@pytest.mark.parametrize("argv", [["pipelines"], ["jobs", "1"], ["artifact", "1", "ci-out/x"]])
@pytest.mark.parametrize("body", ["", "not json at all", "<html>", "[]", "{}", '{"workflow_runs": 5}',
                                  '{"jobs": [1, 2]}', "null", '"text"'])
def test_an_empty_or_broken_answer_is_a_named_failure_not_a_traceback(argv, body, net, capsys):
    net.body = body
    code = ci_read.main(argv)
    seen = capsys.readouterr()
    assert "Traceback" not in seen.out + seen.err
    if code == 0:
        assert seen.out                            # the one clean case: an empty list prints "(no runs)" or nothing wrong
    else:
        assert code == 1 and (seen.out.startswith("request failed: ") or seen.out.startswith("unexpected answer: ")
                              or "is absent or expired" in seen.out)


def test_network_failure_and_a_bad_regex_exit_1_without_a_traceback(net, capsys):
    net.error = urllib.error.URLError("no route")
    assert ci_read.main(["pipelines"]) == 1
    assert "request failed: URLError" in capsys.readouterr().out
    net.error = None
    net.body = "x"
    assert ci_read.main(["log", "1", "--grep", "("]) == 1
    assert capsys.readouterr().out.startswith("request failed: error")


def test_constants():
    assert ci_read.API == "https://api.github.com" and ci_read.MAX_ARTIFACT_BYTES == 200 * 1024 * 1024
    assert ci_read.common.DEFAULT_GREP == r"FAIL|===|Error|Traceback" and ci_read.TOKEN_ENV == "GITHUB_TOKEN"
