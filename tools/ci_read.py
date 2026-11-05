"""ci_read.py -- read (and start) GitHub Actions runs of this project with a few lines of output, so a session does not
pull a whole job log into its context (B-466, t-575; GitHub backend GM1-4, t-1887).

  python tools/ci_read.py pipelines [--n N]                    N is 1..100 (GitHub returns at most 100 per page)
  python tools/ci_read.py jobs <run_id>
  python tools/ci_read.py log <job_id> [--grep REGEX] [--tail N]             (default: FAIL|===|Error|Traceback)
  python tools/ci_read.py artifact <run_id> <name>/<path> [--grep REGEX] [--tail N]   (no --grep: every line)
(--tail N, default 200, keeps the LAST N lines AFTER the grep filter; the last output line is
"(N of M lines)": N shown, M matched.)
  python tools/ci_read.py start [--ref main]                   dispatches canon.yml with the input ref

WHICH repository: the `origin` remote of this tree. The URL is parsed (scp form `user@host:o/r`, else a URL; host
lower-case, userinfo dropped; the path is exactly `owner/repo`, with `.git` and a trailing `/` removed): host
github.com -> GitHub o/r; the host of tools/ci_read_gitlab.HOST -> that GitLab backend (a module deleted at the move);
anything else, or no such module -> a refusal, exit 2, "this tool reads GitHub only; origin host is <host>" (the host
only, never the URL: it may carry a token). No request is made before the choice. No `origin` -> exit 2. A door for an
environment where `origin` is not github.com (a cloud session whose origin is a local proxy): QA_CI_REPO=owner/repo
selects GitHub owner/repo without reading `origin`; the host is then only api.github.com.

The token comes from an environment variable: the NAME of that variable is `github_token_env` of tools/dev.config.yaml
(read by tools/dev_config.py); with NO such file the name is GITHUB_TOKEN and ONE line on stderr says so; a file that
exists without the key is REFUSED (an old file with only gitlab_token_env included), exit 2. The token goes out only in
`Authorization: Bearer`, set as an UNREDIRECTED header: a 301/302 (a log, an artifact zip, a renamed repository) is
followed WITHOUT it, so the token never leaves api.github.com. The value is never printed or logged. An HTTP error
prints "HTTP <status>: <first 200 chars of the body>".

An artifact is read into memory: the zip may not exceed MAX_ARTIFACT_BYTES, nor any member (the size is checked
before a member is read); one byte over is a refusal, exit 1. Output lines carry REMOTE text and go through
sanitize() (ci_read_common); the tool's own words keep their punctuation. Exit codes: 0 ok, 1 HTTP/network error or a
refused answer, 2 missing token, a refused config, a refused argument or no usable origin."""

import io
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path

_TOOLS = Path(__file__).resolve().parent
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))

import ci_read_common as common  # noqa: E402
import gitcmd  # noqa: E402
from ci_read_common import (  # noqa: E402
    TIMEOUT_SECONDS, Failure, Refusal, _emit_tail, emit, emit_own, sanitize)

ROOT = _TOOLS.parent
API = "https://api.github.com"
API_VERSION = "2022-11-28"
TOKEN_ENV = "GITHUB_TOKEN"      # the FALLBACK name: used when there is no tools/dev.config.yaml
TOKEN_KEY = "github_token_env"
WORKFLOW = "canon.yml"
MAX_PER_PAGE = 100
MAX_ARTIFACT_BYTES = 200 * 1024 * 1024
REPO_DOOR = "QA_CI_REPO"
REPO_RE = re.compile(r"^[\w.-]+/[\w.-]+$", re.ASCII)      # ASCII \w: GitHub names are ASCII, and it goes into a URL
_SCP_RE = re.compile(r"^[^@/]+@([^:/]+):(.+)$")
build_parser = common.build_parser


def _repo_name(text):
    """`owner/repo` when `text` is exactly two segments of [\\w.-] (neither all dots), else None."""
    if not REPO_RE.fullmatch(text) or any(not seg.strip(".") for seg in text.split("/")):
        return None
    return text


def split_origin(url: str):
    """(host lower-case or "", path) of an origin URL: scp form first, else a URL; userinfo and port are dropped."""
    scp = _SCP_RE.match(url)
    if scp:
        return scp.group(1).lower(), scp.group(2)
    try:
        parts = urllib.parse.urlsplit(url)
        return (parts.hostname or ""), parts.path
    except ValueError:
        return "", ""


def _origin_repo_path(path: str):
    path = path.lstrip("/").rstrip("/")
    if path.endswith(".git"):
        path = path[:-4]
    return _repo_name(path)


def origin_url(root) -> str:
    rc, out = gitcmd.git(root, "remote", "get-url", "origin")
    url = gitcmd.as_text(out).strip() if rc == 0 else ""
    if not url:
        raise Refusal("no origin remote: git remote add origin https://github.com/<owner>/<repo>.git "
                      "(or set %s=owner/repo)" % REPO_DOOR)
    return url


def backend_for(root=None):
    """The Backend for the tree at `root`: the door QA_CI_REPO, else the host of `origin`. No request is made here."""
    root = ROOT if root is None else root
    door = os.environ.get(REPO_DOOR, "")
    if door:
        repo = _repo_name(door)
        if repo is None:
            raise Refusal("%s must be owner/repo (letters, digits, '_', '.', '-' on both sides of one '/'), "
                          "not what is set" % REPO_DOOR)
        return github_backend(repo, root)
    host, path = split_origin(origin_url(root))
    if host == "github.com":
        repo = _origin_repo_path(path)
        if repo is None:
            raise Refusal("the origin on github.com does not name exactly owner/repo: expected "
                          "https://github.com/<owner>/<repo>.git or git@github.com:<owner>/<repo>.git")
        return github_backend(repo, root)
    try:
        import ci_read_gitlab
        gitlab_host = urllib.parse.urlsplit(ci_read_gitlab.HOST).hostname
    except ImportError:
        ci_read_gitlab, gitlab_host = None, None
    if ci_read_gitlab is not None and host and host == gitlab_host:
        return ci_read_gitlab.make_backend(root)
    raise Refusal("this tool reads GitHub only; origin host is %s" % (sanitize(host) if host else "(none)"))


def _open(url: str, token: str, method: str = "GET", body=None, limit=None):
    """(status, body bytes). The token rides in an UNREDIRECTED header: a redirect never carries it away."""
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("X-GitHub-Api-Version", API_VERSION)
    req.add_unredirected_header("Authorization", "Bearer " + token)
    if data is not None:
        req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS) as resp:
        raw = resp.read() if limit is None else resp.read(limit + 1)
        return getattr(resp, "status", 200), raw


def _text(raw: bytes) -> str:
    return raw.decode("utf-8", errors="replace")


def _rows(raw: bytes, key: str) -> list:
    data = json.loads(_text(raw))          # empty or not JSON: ValueError -> "request failed: JSONDecodeError"
    rows = data.get(key) if isinstance(data, dict) else None
    if not isinstance(rows, list) or not all(isinstance(r, dict) for r in rows):
        raise Failure("unexpected answer: expected a JSON object with a list '%s'" % key)
    return rows


def _done(row: dict) -> str:
    return str(row.get("conclusion") or row.get("status"))


def make_commands(repo: str) -> dict:
    base = "%s/repos/%s" % (API, repo)

    def cmd_pipelines(args, token):
        rows = _rows(_open("%s/actions/runs?per_page=%d" % (base, args.n), token)[1], "workflow_runs")
        for r in rows:
            emit("%s %s %s %s %s" % (r.get("id"), _done(r), r.get("display_title") or "-",
                                     str(r.get("head_sha") or "")[:8], r.get("event")))
        if not rows:
            emit("(no runs)")

    def cmd_jobs(args, token):
        for j in _rows(_open("%s/actions/runs/%d/jobs?per_page=100" % (base, args.id), token)[1], "jobs"):
            emit("%s %s %s" % (j.get("id"), j.get("name"), _done(j)))

    def cmd_log(args, token):
        _emit_tail(_text(_open("%s/actions/jobs/%d/logs" % (base, args.job_id), token)[1]), args.grep, args.tail)

    def cmd_artifact(args, token):
        name, _, member = args.path.partition("/")
        rows = _rows(_open("%s/actions/runs/%d/artifacts?per_page=100" % (base, args.id), token)[1], "artifacts")
        listed = ", ".join(sanitize("%s%s" % (r.get("name"), " (expired)" if r.get("expired") else ""))
                           for r in rows) or "(none)"
        found = [r for r in rows if r.get("name") == name and not r.get("expired")]
        if not found:
            raise Failure("artifact %s is absent or expired in run %d; names: %s" % (sanitize(name), args.id, listed))
        raw = _open("%s/actions/artifacts/%s/zip" % (base, urllib.parse.quote(str(found[0].get("id")), safe="")),
                    token, limit=MAX_ARTIFACT_BYTES)[1]
        if len(raw) > MAX_ARTIFACT_BYTES:
            raise Failure("the artifact archive is larger than %d bytes: refused" % MAX_ARTIFACT_BYTES)
        try:
            with zipfile.ZipFile(io.BytesIO(raw)) as archive:
                try:
                    info = archive.getinfo(member)
                except KeyError:
                    names = ", ".join(sanitize(n) for n in archive.namelist()[:20]) or "(none)"
                    raise Failure("%s is not in the artifact %s; members: %s" % (sanitize(member), sanitize(name),
                                                                                names)) from None
                if info.file_size > MAX_ARTIFACT_BYTES:
                    raise Failure("the member is larger than %d bytes: refused" % MAX_ARTIFACT_BYTES)
                with archive.open(info) as handle:
                    body = handle.read(MAX_ARTIFACT_BYTES + 1)
        except zipfile.BadZipFile:
            raise Failure("the artifact is not a readable zip") from None
        if len(body) > MAX_ARTIFACT_BYTES:
            raise Failure("the member is larger than %d bytes: refused" % MAX_ARTIFACT_BYTES)
        _emit_tail(_text(body), args.grep, args.tail)

    def cmd_start(args, token):
        try:
            _open("%s/actions/workflows/%s/dispatches" % (base, WORKFLOW), token, method="POST",
                  body={"ref": "main", "inputs": {"ref": args.ref}})
        except urllib.error.HTTPError as exc:
            if exc.code == 404:
                raise Failure("%s is not on the default branch, or the token cannot see this repository"
                              % WORKFLOW) from None
            raise
        emit_own("dispatched %s for %s; find the run: ci_read.py pipelines" % (WORKFLOW, sanitize(args.ref)))

    return {"pipelines": cmd_pipelines, "jobs": cmd_jobs, "log": cmd_log, "artifact": cmd_artifact,
            "start": cmd_start}


def _check(args) -> None:
    """Refuse a bad argument before the token is read and before any request."""
    if args.cmd == "pipelines" and args.n < 1:
        raise Refusal("--n must be 1 or more")
    if args.cmd == "pipelines" and args.n > MAX_PER_PAGE:
        raise Refusal("GitHub returns at most %d per page: --n %d is refused, use %d or less"
                      % (MAX_PER_PAGE, args.n, MAX_PER_PAGE))
    if args.cmd == "artifact":
        name, _, member = args.path.partition("/")
        if not name or not member:
            raise Refusal("artifact needs <name>/<path inside the zip>, e.g. ci-out/report.txt")


def github_backend(repo: str, root) -> common.Backend:
    return common.Backend(
        name="GitHub", token_key=TOKEN_KEY, token_fallback=TOKEN_ENV, token_label="GitHub", root=root, check=_check,
        missing_hint="create a GitHub token that may read Actions (and write Actions to start a run) and export it "
                     "as %s",
        commands=make_commands(repo))


def main(argv=None) -> int:
    return common.run(argv, lambda: backend_for(ROOT))


if __name__ == "__main__":
    sys.exit(main())
