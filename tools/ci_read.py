"""ci_read.py -- read (and start) GitHub Actions runs of this project with a few lines of output, so a session does not
pull a whole job log into its context (B-466, t-575; GitHub backend GM1-4, t-1887).

  python tools/ci_read.py pipelines [--n N]                    N is 1..100 (GitHub returns at most 100 per page)
  python tools/ci_read.py jobs <run_id>                        under each job, every failed step
  python tools/ci_read.py log <job_id> [--grep REGEX] [--tail N]             (default: FAIL|===|Error|Traceback)
  python tools/ci_read.py artifact <run_id> <name>/<path> [--grep REGEX] [--tail N]   (no --grep: every line)
(--tail N, default 200, keeps the LAST N lines AFTER the grep filter; the last output line is
"(N of M lines)": N shown, M matched.)
  python tools/ci_read.py why [<run_id>|latest] [--workflow canon.yml] [--branch B] [--tail N]
      the failing job(s) of a run (latest = newest of the workflow, on --branch when given; --branch and --workflow
      apply to `latest` only) and the last N lines (default 60, 1..500) of each failing step's log section; at most 3
      jobs (+K more); green / unfinished / no failed job / log expired / step section not found each say so.
  python tools/ci_read.py start [--ref main] [--workflow canon.yml] [--var KEY=VALUE ...]
      dispatches the workflow (default canon.yml) with the input ref plus one input per --var (the GitLab reader's
      pipeline variables, same form); e.g. the test-redundancy measurement:
      start --workflow nightly.yml --ref <branch> --var TEST_REDUNDANCY=1 --var REDUNDANCY_SCOPE=keep
      the quarantine watch: start --workflow quarantine-watch.yml --ref <branch>
      A pair without "=", an empty KEY, a KEY twice or --var ref=... is refused (exit 2) before any request; a KEY
      the workflow does not declare is GitHub's 422, printed as a refusal of the inputs (exit 1).

  python tools/ci_read.py main-red [show|refresh]       main's red list (FG7-94): no subcommand = the SessionStart line, or `main green at <sha8>`;
      show = the red jobs with the merges that could have brought them; refresh = read CI of main's last tips now
  python tools/ci_read.py main-red fixer <t-NNN> | fixer --done <t-NNN>      one fixer at a time (refused: another open, or main not red)
  python tools/ci_read.py main-red flaky add "<id>" --why "<text>" | flaky done "<id>" --by <t-NNN>      the known-flaky queue
      Carrier: <git common dir>/main-red/state.json, written only by main_red_write (lock main-red). A bad task id or flaky id
      is refused (exit 2) before the lock; a busy lock is exit 1 `retry`. Push runs of forge-check.yml and canon.yml on main
      are read (a dispatch run or quarantine-watch never counts); cancelled is never red, unknown is never green.

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

import argparse
import calendar
import contextlib
import io
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path
from types import SimpleNamespace

_TOOLS = Path(__file__).resolve().parent
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))

import ascii_line  # noqa: E402
import ci_read_common as common  # noqa: E402
import gitcmd  # noqa: E402
import journal_lock as jl  # noqa: E402
from ci_read_common import (  # noqa: E402
    TIMEOUT_SECONDS, Failure, Refusal, _emit_tail, emit, emit_own, sanitize)

ROOT = _TOOLS.parent
API = "https://api.github.com"
API_VERSION = "2022-11-28"
TOKEN_ENV = "GITHUB_TOKEN"      # the FALLBACK name: used when there is no tools/dev.config.yaml
TOKEN_KEY = "github_token_env"
WORKFLOW = "canon.yml"
MAX_PER_PAGE = 100
FAILED = ("failure", "timed_out")     # the conclusions `why` reads
WHY_MAX_JOBS = 3
MAX_ARTIFACT_BYTES = 200 * 1024 * 1024
REPO_DOOR = "QA_CI_REPO"
WORKFLOW_RE = re.compile(r"^[\w.-]+\.ya?ml$", re.ASCII)   # it goes into a URL path segment
REPO_RE = re.compile(r"^[\w.-]+/[\w.-]+$", re.ASCII)      # ASCII \w: GitHub names are ASCII, and it goes into a URL
_SCP_RE = re.compile(r"^[^@/]+@([^:/]+):(.+)$")
build_parser = common.build_parser
MAIN_WORKFLOWS = ("forge-check.yml", "canon.yml")     # the allow-list of push runs on main (quarantine-watch never counts, E8)
MAIN_WINDOW = 30                  # first-parent tips of origin/main read per refresh
GRACE_NEW_S = 120                 # a tip younger than this is pending whatever CI says
NONE_UNKNOWN_S = 900              # no run at all after this: unknown
PENDING_STALE_S = 5400            # still pending after 90 min (> the measured canon max of 73): unknown
HISTORY_MAX = 50
NAME_MAX = 60                     # a job name / subject / branch from the remote
LINE_MAX = 300                    # the SessionStart line
FLAKY_ID_MAX = 200
LAUNCH_MIN_S = 300                # a detached refresh is not launched twice within this
LOCK_WAIT = 10.0
STATE_DIRNAME = "main-red"
TASK_RE = re.compile(r"t-[0-9]{3,9}[a-z]{0,2}")
FLAKY_RE = re.compile(r"[\x20-\x7e]{1,%d}" % FLAKY_ID_MAX)
_PENDING = ("queued", "in_progress", "waiting", "requested", "pending")
_VERDICT = {"success": "success", "failure": "failure", "timed_out": "failure", "startup_failure": "failure",
            "cancelled": "cancelled", "skipped": "skipped"}
_RANK = ("failure", "pending", "unknown", "cancelled", "skipped", "success")     # the worse verdict wins on one name


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


def failed_steps(job) -> list:
    """The steps of a job (API order) whose conclusion is in FAILED: the ONE predicate `jobs` and `why` both read (FG7-90).
    A job that is not a dict, steps absent / None / not a list, entries that are not dicts: skipped, never raises."""
    steps = job.get("steps") if isinstance(job, dict) else None
    if not isinstance(steps, list):
        return []
    return [s for s in steps if isinstance(s, dict) and s.get("conclusion") in FAILED]


def _done(row: dict) -> str:
    return str(row.get("conclusion") or row.get("status"))


def _state_word(row: dict) -> str:
    """success | failure | in_progress | unknown of one run or job row (conclusion first, else its status)."""
    w = str(row.get("conclusion") or row.get("status") or "")
    return ("success" if w == "success" else "failure" if w in ("failure", "timed_out", "cancelled")
            else "in_progress" if w in ("in_progress", "queued", "waiting", "pending", "requested") else "unknown")


def workflow_note(root, ref: str, workflow: str):
    """One line about a ref that edits workflow files, or None. GitHub runs a workflow_dispatch from the default
    branch's file (t-1223 round 7: a branch edit of the dispatch cap only took effect from main), so a branch's own
    workflow edit is not tested by its own run. GitHub runs the REMOTE ref, so origin/<ref> is diffed first and the
    local <ref> only when origin/<ref> does not resolve. Never raises; a failed git diff is "workflow check skipped"."""
    if ref in ("main", "origin/main"):
        return None
    errors = []
    for rev in ("origin/" + ref, ref):
        rc, out, err = gitcmd.git(root, "diff", "--name-only", "origin/main..." + rev, "--", ".github/workflows/",
                                  stderr=True)
        if rc == 0:
            break
        errors.append(gitcmd.first_line(err or out, 120))
    else:
        return "workflow check skipped: neither origin/%s nor %s resolves (%s)" % (ref, ref, errors[0])
    files = [Path(ln).name for ln in gitcmd.as_text(out).splitlines() if ln.strip()]
    if workflow in files:
        return ("note: %s is changed on %s, but this run uses main's version of it (a dispatch reads the default "
                "branch's workflow file)" % (workflow, ref))
    if files:        # start refuses a numeric --workflow (WORKFLOW_RE), so `workflow` is always a file name here
        return ("note: %s changed on %s, which does not affect the run of %s unless it is reusable/called"
                % (", ".join(files), ref, workflow))
    return None


def _canon_run_exists(base: str, token: str, ref: str) -> bool:
    """FG7-91 E6: a push to worktree-agent-** starts the canon by itself, so a hand start of the same head is a duplicate.
    True (after printing the id and url) when the PUSH run of canon.yml for branch `ref` exists at its head sha, in any
    state (a dispatch run carries main's head_sha and never counts); False
    to start as today, with one note line when the head or the run listing could not be read. Only a start without --var
    asks (a --var start is never a push run). Never raises."""
    try:
        head = json.loads(_text(_open("%s/commits/%s" % (base, urllib.parse.quote(ref, safe="/")), token)[1])).get("sha")
        if not head:
            raise ValueError("no sha")
        rows = _rows(_open("%s/actions/workflows/%s/runs?head_sha=%s&per_page=10"
                           % (base, WORKFLOW, urllib.parse.quote(str(head), safe="")), token)[1], "workflow_runs")
    except Exception as exc:  # noqa: BLE001 -- advisory: whatever fails, the start goes on as before
        emit_own("note: the run listing failed (%s); starting as before" % sanitize(str(exc)[:80] or type(exc).__name__))
        return False
    # only the push run of THIS branch counts: a dispatch run carries main's head_sha whatever it canonises (critic t-1478 F1)
    rows = [r for r in rows if str(r.get("head_sha") or "") == head and r.get("event") == "push" and r.get("head_branch") == ref]
    if not rows:
        return False
    emit_own("%s already has a run for %s at %s: %s %s; nothing started" % (
        WORKFLOW, sanitize(ref), head[:8], sanitize(str(rows[0].get("id"))), sanitize(str(rows[0].get("html_url") or "-"))))
    return True


def _verdict(row: dict) -> str:
    """success | failure | cancelled | skipped | pending | unknown of one run or job row (FG7-94 D2; _state_word stays as it is)."""
    done = row.get("conclusion")
    if not done:
        return "pending" if row.get("status") in _PENDING else "unknown"
    return _VERDICT.get(done, "unknown")


def _key(row: dict):
    return (str(row.get("created_at") or ""), row.get("id") if isinstance(row.get("id"), int) else 0)


def make_commands(repo: str, root=None) -> dict:
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
            bad = failed_steps(j)
            for s in bad:
                emit("  step %s %s %s" % (s.get("number"), s.get("name"), s.get("conclusion")))
            if not bad and j.get("conclusion") in FAILED:      # a red job never prints as if nothing failed (E8)
                emit_own("  no failed step recorded (job %s)" % j.get("conclusion"))

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
        workflow = args.workflow or WORKFLOW
        extra = common.parse_vars(args.var)          # already checked by _check (form, duplicates, no ref)
        inputs = {"ref": args.ref}
        inputs.update(extra)
        if workflow == WORKFLOW and not extra and _canon_run_exists(base, token, args.ref):
            return
        try:
            _open("%s/actions/workflows/%s/dispatches" % (base, workflow), token, method="POST",
                  body={"ref": "main", "inputs": inputs})
        except urllib.error.HTTPError as exc:
            if exc.code == 404:
                raise Failure("%s is not on the default branch, or the token cannot see this repository"
                              % workflow) from None
            if exc.code == 422 and extra:
                raise Failure("HTTP 422: %s refused the inputs; every --var KEY must be an input of its "
                              "workflow_dispatch" % workflow) from None
            raise
        shown = "".join(" %s=%s" % (k, v) for k, v in extra.items())
        emit_own("dispatched %s for %s%s; find the run: ci_read.py pipelines" % (workflow, sanitize(args.ref),
                                                                              sanitize(shown)))
        note = workflow_note(root, args.ref, workflow)       # advisory only: never blocks, never changes the exit
        if note:
            emit_own(sanitize(note))

    def why_run(args, token):
        """The run `why` reads (latest of the workflow, or the explicit id), or None after saying "(no runs)"."""
        if args.run == "latest":
            query = "per_page=1" + ("&branch=" + urllib.parse.quote(args.branch, safe="") if args.branch else "")
            rows = _rows(_open("%s/actions/workflows/%s/runs?%s" % (base, args.workflow or WORKFLOW, query),
                               token)[1], "workflow_runs")
            if not rows:
                emit("(no runs)")
                return None
            return rows[0]
        run = json.loads(_text(_open("%s/actions/runs/%d" % (base, args.run), token)[1]))
        if not isinstance(run, dict):
            raise Failure("unexpected answer: expected a JSON object describing the run")
        return run

    def why_job(job, args, token):
        emit("job %s %s" % (job.get("id"), job.get("name")))
        try:
            log = _text(_open("%s/actions/jobs/%s/logs" % (base, job.get("id")), token)[1])
        except urllib.error.HTTPError as exc:
            if exc.code not in (404, 410):
                raise
            emit_own("log expired")
            return
        steps = [s for s in (job.get("steps") or []) if isinstance(s, dict)]
        whole_shown = False
        for step in failed_steps(job) or [None]:
            section = None
            if step is not None:
                emit("step %s %s %s" % (step.get("number"), step.get("name"), step.get("conclusion")))
                section = common.step_section(log, step, steps)
            if section is not None:
                _emit_tail(section, None, args.tail)
            elif not whole_shown:
                emit_own("step section not found: job log tail")
                _emit_tail(log, None, args.tail)
                whole_shown = True

    def cmd_why(args, token):
        run = why_run(args, token)
        if run is None:
            return
        run_id, conclusion = run.get("id"), run.get("conclusion")
        head = "run %s %s %s %s" % (run_id, _done(run), run.get("display_title") or "-", str(run.get("head_sha") or "")[:8])
        if run.get("status") != "completed":
            emit(head)                                    # in progress / queued: that status, nothing to read yet
            return
        if conclusion == "success":
            emit("run %s success: nothing failed" % run_id)
            return
        emit(head)
        jobs = _rows(_open("%s/actions/runs/%s/jobs?per_page=100" % (base, run_id), token)[1], "jobs")
        failed = sorted((j for j in jobs if j.get("conclusion") in FAILED),
                        key=lambda j: j["id"] if isinstance(j.get("id"), int) else 0)
        if not failed:
            emit_own("%s: no failed job" % sanitize(str(conclusion)))
            return
        for job in failed[:WHY_MAX_JOBS]:
            why_job(job, args, token)
        if len(failed) > WHY_MAX_JOBS:
            emit_own("+%d more failed jobs" % (len(failed) - WHY_MAX_JOBS))

    def cmd_run_state(args, token):
        """DATA, not output: (state, failed job names) of the newest run of the commit `args.sha` (see run_state)."""
        runs = _rows(_open("%s/actions/runs?head_sha=%s&per_page=10" % (base, urllib.parse.quote(args.sha, safe="")),
                           token)[1], "workflow_runs")
        runs = [r for r in runs if str(r.get("head_sha") or "") == args.sha]
        if not runs:
            return "none", []
        state = _state_word(runs[0])
        jobs = _rows(_open("%s/actions/runs/%s/jobs?per_page=100" % (base, urllib.parse.quote(str(runs[0].get("id")),
                                                                                              safe="")), token)[1], "jobs")
        for j in jobs:
            if "forge-check" in str(j.get("name") or ""):
                state = _state_word(j)
        failed = [str(j.get("name")) for j in jobs if _state_word(j) == "failure"] if state == "failure" else []
        return state, failed

    def cmd_push_jobs(args, token):
        """DATA: (word, {workflow: run_id}, {job: verdict}) of the PUSH runs on main at `args.sha` (see main_push_jobs)."""
        q = urllib.parse.quote(args.sha, safe="")
        rows = _rows(_open("%s/actions/runs?head_sha=%s&event=push&branch=main&per_page=20" % (base, q), token)[1],
                     "workflow_runs")
        kept = {}
        for r in rows:       # newest per workflow; a dispatch run, another head, another workflow never counts (E7, E8)
            wf = str(r.get("path") or "").split("@")[0].rsplit("/", 1)[-1]
            if (str(r.get("head_sha") or "") == args.sha and r.get("event") == "push" and r.get("head_branch") == "main"
                    and wf in MAIN_WORKFLOWS and (wf not in kept or _key(r) > _key(kept[wf]))):
                kept[wf] = r
        if not kept:
            return "none", {}, {}
        jobs = {}

        def put(name, verdict):
            name = ascii_line.clip(name, NAME_MAX)
            if name not in jobs or _RANK.index(verdict) < _RANK.index(jobs[name]):
                jobs[name] = verdict
        for wf, r in kept.items():
            if r.get("conclusion") == "startup_failure":          # a broken workflow file on main (E9)
                put("%s: startup_failure" % wf, "failure")
                continue
            listed = _rows(_open("%s/actions/runs/%s/jobs?per_page=100" % (base, urllib.parse.quote(str(r.get("id")), safe="")),
                                 token)[1], "jobs")
            for j in listed:
                put(str(j.get("name")), _verdict(j))
            if r.get("status") != "completed" or not listed:
                put("%s: run" % wf, _verdict(r))
        return "read", {wf: r.get("id") for wf, r in kept.items()}, jobs

    return {"pipelines": cmd_pipelines, "jobs": cmd_jobs, "log": cmd_log, "artifact": cmd_artifact,
            "start": cmd_start, "why": cmd_why, "run_state": cmd_run_state, "push_jobs": cmd_push_jobs}


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
    if args.cmd == "why":
        if args.run != "latest" and (args.branch is not None or args.workflow is not None):
            raise Refusal("--branch/--workflow select `latest` only; with run <id> drop them")
        if not 1 <= args.tail <= common.WHY_MAX_TAIL:
            raise Refusal("why --tail must be 1..%d, got %d" % (common.WHY_MAX_TAIL, args.tail))
        if args.workflow is not None and not WORKFLOW_RE.fullmatch(args.workflow):
            raise Refusal("--workflow expects a file name of .github/workflows, e.g. canon.yml "
                          "(letters, digits, '_', '.', '-', ending .yml or .yaml)")
    if args.cmd == "start":
        if args.workflow is not None and not WORKFLOW_RE.fullmatch(args.workflow):
            raise Refusal("--workflow expects a file name of .github/workflows, e.g. quarantine-watch.yml "
                          "(letters, digits, '_', '.', '-', ending .yml or .yaml)")
        if "ref" in common.parse_vars(args.var):
            raise Refusal("start: the input ref is given by --ref, not by --var ref=...")


def github_backend(repo: str, root) -> common.Backend:
    return common.Backend(
        name="GitHub", token_key=TOKEN_KEY, token_fallback=TOKEN_ENV, token_label="GitHub", root=root, check=_check,
        missing_hint="create a GitHub token that may read Actions (and write Actions to start a run) and export it "
                     "as %s",
        commands=make_commands(repo, root))


def run_state(root, sha):
    """(state, failed_jobs) of the CI run of the commit `sha`, as DATA through the backend of the tree at `root` (the
    same choice, token door and request function as the commands). state: success | failure | in_progress | none (no run
    for that sha) | unknown (no usable backend, token or answer: any transport/parse error; never a pass, never a failure);
    failed_jobs: the names of the failed jobs, empty unless failure. The job named *forge-check* decides the state of a run
    that has one. A backend without a `run_state` command (the old one) answers unknown. Never raises, never prints."""
    try:
        with contextlib.redirect_stderr(io.StringIO()):
            backend = backend_for(root)
            name, _source = backend.token_env_name()
        command, token = backend.commands.get("run_state"), os.environ.get(name)
        if command is None or not token:
            return "unknown", []
        state, failed = command(SimpleNamespace(sha=str(sha)), token)
        return state, list(failed)
    except Exception:  # noqa: BLE001 -- information only: whatever fails is `unknown`
        return "unknown", []


def main_push_jobs(root, sha):
    """(word, {workflow: run_id}, {job: verdict}) of the PUSH runs of MAIN_WORKFLOWS on main at `sha`, as DATA, built like
    run_state (same backend, token door, request function). word: none (no kept run) | read | unknown (any transport, parse
    or token failure). Never raises, never prints. The error direction is toward unknown/pending, never toward green."""
    try:
        with contextlib.redirect_stderr(io.StringIO()):
            backend = backend_for(root)
            name, _source = backend.token_env_name()
        command, token = backend.commands.get("push_jobs"), os.environ.get(name)
        if command is None or not token:
            return "unknown", {}, {}
        word, runs, jobs = command(SimpleNamespace(sha=str(sha)), token)
        return word, dict(runs), dict(jobs)
    except Exception:  # noqa: BLE001 -- information only: whatever fails is `unknown`
        return "unknown", {}, {}


# ---- main's red list (FG7-94): the carrier, its one writer, the fold, the line, the launch, the CLI
class MainRedRefusal(Exception):
    """A mutation refused by its own rule (the carrier stays as it was)."""


def _iso(t):
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(t))


def _epoch(text):
    try:
        return calendar.timegm(time.strptime(str(text), "%Y-%m-%dT%H:%M:%SZ"))
    except (ValueError, OverflowError):
        return 0


def _s8(sha):
    return str(sha or "")[:8]


def _fresh():
    return {"version": 1, "head": None, "read_at": None, "error": None, "tips": {}, "order": [], "red": {},
            "fixer": None, "flaky": [], "history": []}


def _valid(st):
    shape = (("tips", dict), ("order", list), ("red", dict), ("flaky", list), ("history", list))
    return (isinstance(st, dict) and st.get("version") == 1 and all(isinstance(st.get(k), t) for k, t in shape)
            and (st.get("fixer") is None or isinstance(st.get("fixer"), dict))
            and all(isinstance(t, dict) for t in st["tips"].values()) and all(isinstance(r, dict) for r in st["red"].values()))


def _state_path(root):
    return jl.common_dir(root) / STATE_DIRNAME / "state.json"


def main_red_read(root, path=None):
    """(state, None) | (None, why); why is `never read` or `state unreadable (<Exc>)`. No lock: the file is replaced whole."""
    try:
        path = path or _state_path(root)
        state = json.loads(path.read_text(encoding="utf-8"))
        if not _valid(state):
            raise ValueError("wrong shape")
        return state, None
    except FileNotFoundError:
        return None, "never read"
    except Exception as exc:  # noqa: BLE001 -- a corrupt file is never green
        return None, "state unreadable (%s)" % type(exc).__name__


def main_red_write(root, mutate):
    """THE one writer of the carrier: read, `mutate(state)`, replace from a temp file beside it, under lock main-red. A corrupt
    or wrong-shaped file is renamed aside and the mutation starts fresh (E11). Returns (state, notes). Raises LockBusy / LockError
    / whatever `mutate` raises (then nothing is written)."""
    path = _state_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    notes = []
    with jl.machine_lock("main-red", LOCK_WAIT, repo=root):
        state, why = main_red_read(root, path)
        if state is None and path.exists():
            aside = "state.json.corrupt-" + time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
            os.replace(path, path.parent / aside)
            notes.append("state was unreadable (%s); kept as %s, started fresh" % (why, aside))
        state = state or _fresh()
        mutate(state)
        state["history"] = state["history"][-HISTORY_MAX:]
        tmp = path.parent / ("state.json.tmp-%d" % os.getpid())
        tmp.write_text(json.dumps(state, indent=1, sort_keys=True), encoding="utf-8")
        os.replace(tmp, path)
    return state, notes


def _hist(st, text, now=None):
    st["history"].append({"at": _iso(time.time() if now is None else now), "text": ascii_line.clip(text, 200)})


def _new_tip(task, branch, kind, subject, when):
    return {"task": task, "branch": branch, "kind": kind, "subject": ascii_line.clip(subject or "", NAME_MAX),
            "pushed_at": _iso(when), "runs": {}, "jobs": {}, "state": "pending", "final": False}


def main_red_record(root, sha, task=None, branch=None, kind="merge", preflight=None, now=None):
    """wave's call after a push to main: the tip joins the carrier (pending until a refresh reads it). Returns an error text
    or None; never raises. `preflight`: names of FG7-92 registry checks that were red before the merge (a prediction, shown
    by `show`, never opening MAIN RED)."""
    try:
        def mutate(st):
            tip = st["tips"].get(sha) or _new_tip(task, branch, kind, "", time.time() if now is None else now)
            tip.update(task=task, branch=ascii_line.clip(branch or "", NAME_MAX) or None, kind=kind)
            if preflight:
                tip["preflight"] = [ascii_line.clip(p, NAME_MAX) for p in list(preflight)[:10]]
            st["tips"][sha] = tip
            if sha not in st["order"]:
                st["order"].append(sha)
            st["order"] = st["order"][-MAIN_WINDOW:]
        main_red_write(root, mutate)
        return None
    except Exception as exc:  # noqa: BLE001 -- wave never fails on this
        return ascii_line.clip("%s: %s" % (type(exc).__name__, exc), 120)


def main_red_tip_state(word, runs, jobs, age):
    """pending | unknown | red | green | superseded of one tip (D4). Pending outranks red: a red tip is final only when no run is open."""
    if word == "unknown":
        return "unknown"
    if age < GRACE_NEW_S:
        return "pending"
    if word == "none":
        return "unknown" if age > NONE_UNKNOWN_S else "pending"
    if any(v == "pending" for v in jobs.values()):
        return "unknown" if age > PENDING_STALE_S else "pending"
    if any(v == "failure" for v in jobs.values()):
        return "red"
    if "forge-check.yml" in runs and all(v in ("success", "skipped") for v in jobs.values()):
        return "green"
    return "superseded"


def main_red_fold(order, tips, prior_red):
    """(red, events) over `order` (oldest first), pure. Per job: only tips with a FINAL verdict success/failure speak. Latest
    failure opens it (first_red = start of the trailing failure streak, last_green before it, range = tips after last_green up
    to first_red, tips without a verdict named); latest success closes it; no verdict in the window keeps a prior red as it was;
    a prior red whose job is absent at a green head closes as `gone`. events: (job, closed|gone, sha)."""
    red, events = {}, []
    pos = {sha: i for i, sha in enumerate(order)}
    final = [s for s in order if tips.get(s, {}).get("final")]
    for job in sorted(set(prior_red) | {j for s in final for j in tips[s].get("jobs", {})}):
        seq = [(s, tips[s]["jobs"][job]) for s in final if tips[s].get("jobs", {}).get(job) in ("success", "failure")]
        if not seq:
            if job in prior_red:
                red[job] = prior_red[job]
            continue
        if seq[-1][1] == "success":
            if job in prior_red:
                events.append((job, "closed", seq[-1][0]))
            continue
        i = len(seq) - 1
        while i > 0 and seq[i - 1][1] == "failure":
            i -= 1
        first, green = seq[i][0], (seq[i - 1][0] if i else None)
        prior = prior_red.get(job)
        if prior and not green and prior.get("first_red") not in pos:       # the streak began before the window: keep its start
            red[job] = prior
            continue
        span = order[(pos[green] + 1 if green else 0):pos[first] + 1]
        rng = [{"sha": s, "task": tips[s].get("task"), "label": tips[s].get("branch") or tips[s].get("subject") or ""} for s in span]
        red[job] = {"first_red": first, "last_green": green, "range": rng, "opened_at": (prior or {}).get("opened_at")}
    head = tips.get(order[-1]) if order else None
    if head and head.get("state") == "green":
        for job in [j for j in red if j not in head.get("jobs", {})]:
            events.append((job, "gone", order[-1]))
            del red[job]
    return red, events


def main_red_refresh(root, now=None):
    """(exit code, text): fetch origin main (30 s; failure -> the local ref, error recorded), read CI of the window's tips that
    are not final, fold, write. A busy lock is exit 0 `another refresh is running`."""
    now = time.time() if now is None else now
    error = None
    if gitcmd.git(root, "fetch", "origin", "main", timeout=30)[0] != 0:
        error = "fetch failed; the local origin/main was read"
    rc, out = gitcmd.git(root, "log", "--first-parent", "-n", str(MAIN_WINDOW), "--format=%H%x09%ct%x09%s", "origin/main")
    rows = [ln.split("\t", 2) for ln in gitcmd.as_text(out).splitlines() if ln.count("\t") >= 2] if rc == 0 else []
    if not rows:
        return 1, "origin/main does not resolve here"
    prior = main_red_read(root)[0] or _fresh()
    reads = {sha: main_push_jobs(root, sha) for sha, _ct, _s in rows if not prior["tips"].get(sha, {}).get("final")}
    if any(r[0] == "unknown" for r in reads.values()):
        error = error or "CI read failed"

    def mutate(st):
        order, tips = [r[0] for r in reversed(rows)], {}
        newest = int(rows[0][1])
        late = sorted((t["pushed_at"], sha) for sha, t in st["tips"].items()      # recorded by wave while the CI was being read (F1)
                      if sha not in order and _epoch(t.get("pushed_at")) >= newest)
        order += [sha for _at, sha in late]
        for sha, ct, subject in reversed(rows):
            tip = st["tips"].get(sha) or _new_tip(None, None, "direct", subject, int(ct))
            tip["subject"] = tip.get("subject") or ascii_line.clip(subject, NAME_MAX)
            if not tip.get("final") and sha in reads:
                word, runs, jobs = reads[sha]
                age = now - _epoch(tip["pushed_at"])
                tip.update(runs=runs, jobs=jobs, state=main_red_tip_state(word, runs, jobs, age))
                tip["final"] = tip["state"] in ("green", "red", "superseded")
                tip["why"] = ("CI read failed" if word == "unknown" else "no run after 15 min" if word == "none"
                              else "no verdict after 90 min") if tip["state"] == "unknown" else None      # F2: the reason lives on the tip
            tips[sha] = tip
        for sha in order[len(rows):]:
            tips[sha] = st["tips"][sha]
        was = st["red"]
        st["red"], events = main_red_fold(order, tips, was)
        fixer = (st["fixer"] or {}).get("task")
        for job, red in st["red"].items():
            if job not in was:
                red["opened_at"] = _iso(now)
                _hist(st, "opened %s, first red %s" % (job, _s8(red["first_red"])), now)
        for job, kind, sha in events:
            task = tips[sha].get("task")
            by = " (fixed by fixer)" if kind == "closed" and fixer and task == fixer else ""
            _hist(st, "%s %s at %s (%s)%s" % (job, "closed" if kind == "closed" else "gone", _s8(sha), task or "direct", by), now)
        st.update(tips=tips, order=order, head=order[-1], read_at=_iso(now), error=error)
    try:
        state, notes = main_red_write(root, mutate)
    except jl.LockBusy:
        return 0, "another refresh is running"
    except jl.LockError as exc:
        return 1, "cannot write the carrier (%s)" % type(exc).__name__
    head = state["tips"][state["head"]]["state"]
    return 0, "; ".join(notes + ["refreshed: head %s %s, %d red" % (_s8(state["head"]), head, len(state["red"]))])


def _origin(root):
    rc, out = gitcmd.git(root, "rev-parse", "--verify", "-q", "refs/remotes/origin/main", timeout=5)
    return gitcmd.as_text(out).strip() if rc == 0 else ""


def _unknown(sha, why):
    return "MAIN CI unknown at %s: %s; refresh: python -B tools/ci_read.py main-red refresh" % (_s8(sha), why)


def main_red_line(root, now=None):
    """The ONE formatter of main's state (SessionStart and the CLI): a str of at most LINE_MAX ASCII chars, or None (silence
    means green with no fixer, or no origin/main here). One file read and at most two local git calls; no network (D5)."""
    now = time.time() if now is None else now
    origin = _origin(root)
    if not origin:
        return None
    state, why = main_red_read(root)
    if state is None:
        return _unknown(origin, why)
    head, tips = state.get("head"), state["tips"]
    if head not in tips or (head != origin and gitcmd.git(root, "merge-base", "--is-ancestor", origin, head, timeout=5)[0] != 0):
        head = None
    age = 0
    if head is None:
        hs, hsha, hwhy = "unknown", origin, "not read yet"
    else:
        tip = tips[head]
        hs, hsha, hwhy = tip.get("state", "unknown"), head, None
        age = now - _epoch(tip.get("pushed_at"))
        if hs == "pending" and not tip.get("runs") and age > NONE_UNKNOWN_S:
            hs, hwhy = "unknown", "no run after 15 min"
        elif hs == "pending" and age > PENDING_STALE_S:
            hs, hwhy = "unknown", "no verdict after 90 min"
        elif hs == "superseded":
            hs, hwhy = "unknown", "run cancelled"
        elif hs == "unknown":
            hwhy = tip.get("why") or "no verdict after 90 min"
    fixer = ascii_line.clip((state["fixer"] or {}).get("task") or "", 20) if state["fixer"] else ""
    n_flaky, h8 = len(state["flaky"]), _s8(hsha)
    if state["red"]:
        pos = {s: i for i, s in enumerate(state["order"])}
        reds = sorted(state["red"].items(), key=lambda kv: pos.get(kv[1].get("first_red"), -1))
        since = _s8(reds[0][1].get("first_red"))
        for k in (3, 2, 1):
            parts = []
            for job, red in reds[:k]:
                tasks = list(dict.fromkeys(ascii_line.clip(r.get("task") or "direct", 20) for r in red.get("range", [])))   # one wave = one task (F6)
                shown = ", ".join(tasks[:2]) + (" +%d" % (len(tasks) - 2) if len(tasks) > 2 else "")
                parts.append("%s [%s]" % (ascii_line.clip(job, NAME_MAX), shown))
            line = "MAIN RED since %s: %s%s; head %s %s; fixer %s%s" % (
                since, ", ".join(parts), " +%d more" % (len(reds) - k) if len(reds) > k else "", h8, hs, fixer or "none",
                "; flaky %d" % n_flaky if n_flaky else "")
            if len(line) <= LINE_MAX:
                break
        return ascii_line.clip(line, LINE_MAX)
    if hs == "green":
        if fixer:
            base = "MAIN GREEN at %s; fixer %s on the flaky queue" % (h8, fixer)
            return base + (": %d left" % n_flaky if n_flaky else
                           "; nothing left, close: python -B tools/ci_read.py main-red fixer --done %s" % fixer)
        return "MAIN GREEN, flaky queue %d: no fixer" % n_flaky if n_flaky else None
    if hs == "pending":
        last = next((s for s in reversed(state["order"]) if tips.get(s, {}).get("state") == "green"), None)
        return "MAIN CI pending at %s (%d min); last green %s" % (h8, max(0, int(age // 60)), _s8(last) if last else "none")
    return _unknown(hsha, hwhy)


def main_red_launch(root, trigger, spawn=None, now=None):
    """started | throttled | no-origin | failed: a detached `main-red refresh`, never waited for. Skipped when origin/main does
    not resolve or the last launch is younger than LAUNCH_MIN_S. Never raises."""
    now = time.time() if now is None else now
    try:
        if not _origin(root):
            return "no-origin"
        stamp = _state_path(root).parent / "launch"
        stamp.parent.mkdir(parents=True, exist_ok=True)
        try:
            if now - float(stamp.read_text(encoding="utf-8")) < LAUNCH_MIN_S:
                return "throttled"
        except (OSError, ValueError):
            pass
        stamp.write_text(str(now), encoding="utf-8")
        import worktree_sweep  # noqa: PLC0415 -- the ONE place a background process is made
        (spawn or worktree_sweep.spawn_detached)([sys.executable, "-B", str(Path(__file__).resolve()), "main-red", "--repo", str(root), "refresh"],
                                   root, jl._git_env())
        return "started"
    except Exception:  # noqa: BLE001 -- the trigger (SessionStart, wave) must not fail on this
        return "failed"


def _refuse(text, code=1):
    print("main-red: " + text)
    return code


def _show(root):
    state, why = main_red_read(root)
    if state is None:
        return _refuse("no state (%s); refresh: python -B tools/ci_read.py main-red refresh" % why)
    tips, order = state["tips"], state["order"]
    print("head %s %s; fixer %s; flaky %d" % (_s8(state["head"]), tips.get(state["head"], {}).get("state", "unknown"),
                                              (state["fixer"] or {}).get("task", "none"), len(state["flaky"])))
    for job, red in state["red"].items():
        green = red.get("last_green")
        print("RED %s: first red %s, last green %s" % (job, _s8(red["first_red"]),
                                                       _s8(green) if green else "none (before %s)" % _s8(order[0] if order else "")))
        for r in red.get("range", [])[:5]:
            print("  %s %s %s" % (_s8(r["sha"]), r.get("task") or "direct", r.get("label") or "-"))
        if len(red.get("range", [])) > 5:
            print("  +%d more" % (len(red["range"]) - 5))
        first = tips.get(red["first_red"], {})
        print("  runs: %s" % (", ".join("%s=%s" % kv for kv in first.get("runs", {}).items()) or "-"))
        for r in red.get("range", []):
            if tips.get(r["sha"], {}).get("preflight"):
                print("  preflight red before %s: %s" % (_s8(r["sha"]), ", ".join(tips[r["sha"]]["preflight"])))
    for item in state["flaky"]:
        print("flaky %s: %s" % (item.get("id"), item.get("why")))
    for event in state["history"][-5:]:
        print("history %s %s" % (event.get("at"), event.get("text")))
    return 0


def _mutation(root, text, mutate):
    try:
        main_red_write(root, mutate)
    except MainRedRefusal as exc:
        return _refuse(str(exc))
    except jl.LockBusy:
        return _refuse("retry: another writer holds the lock")
    except (jl.LockError, OSError) as exc:
        return _refuse("cannot write the carrier (%s)" % type(exc).__name__)
    print(text)
    return 0


def main_red_cli(argv):
    p = argparse.ArgumentParser(prog="ci_read.py main-red", description="main's red list and its one fixer")
    p.add_argument("--repo", default=str(ROOT))
    sub = p.add_subparsers(dest="sub")
    sub.add_parser("show")
    sub.add_parser("refresh")
    f = sub.add_parser("fixer")
    f.add_argument("task", nargs="?")
    f.add_argument("--done", metavar="TASK")
    fl = sub.add_parser("flaky")
    fl.add_argument("op", choices=("add", "done"))
    fl.add_argument("id")
    fl.add_argument("--why")
    fl.add_argument("--by")
    a = p.parse_args(argv)
    root = a.repo
    if a.sub is None:
        line = main_red_line(root)
        if line is None and _origin(root):
            line = "main green at %s" % _s8(_origin(root))
        print(line or "main-red: no origin/main in this root")
        return 0
    if a.sub == "show":
        return _show(root)
    if a.sub == "refresh":
        code, text = main_red_refresh(root)
        print(text)
        return code
    if a.sub == "fixer":
        return _cmd_fixer(root, a)
    return _cmd_flaky(root, a)


def _cmd_fixer(root, a):
    task = a.done or a.task
    if (a.done is None) == (a.task is None) or not TASK_RE.fullmatch(task or ""):
        return _refuse("fixer expects one task id t-NNN (3-9 digits, optional letters) or --done t-NNN", 2)

    def mutate(st):
        cur = (st["fixer"] or {}).get("task")
        if a.done is None:
            if cur:
                raise MainRedRefusal("fixer %s is open" % cur)
            if not st["red"]:
                raise MainRedRefusal("main is not red")
            st["fixer"] = {"task": task, "since": _iso(time.time())}
        else:
            if cur != task:
                raise MainRedRefusal("fixer %s is open" % cur if cur else "no fixer is open")
            st["fixer"] = None
        _hist(st, "fixer %s %s" % (task, "set" if a.done is None else "done"))
    return _mutation(root, "fixer %s %s" % (task, "set" if a.done is None else "done"), mutate)


def _cmd_flaky(root, a):
    if not FLAKY_RE.fullmatch(a.id) or (a.why is not None and not FLAKY_RE.fullmatch(a.why)):
        return _refuse("flaky id and --why are 1..%d printable ASCII characters, one line" % FLAKY_ID_MAX, 2)
    if (a.op == "add" and a.why is None) or (a.op == "done" and not TASK_RE.fullmatch(a.by or "")):
        return _refuse("flaky add needs --why <text>; flaky done needs --by t-NNN", 2)

    def mutate(st):
        ids = [x.get("id") for x in st["flaky"]]
        if a.op == "add":
            if a.id in ids:
                raise MainRedRefusal("already on the flaky queue")
            st["flaky"].append({"id": a.id, "why": a.why, "added": _iso(time.time())})
        else:
            if a.id not in ids:
                raise MainRedRefusal("not on the flaky queue")
            st["flaky"] = [x for x in st["flaky"] if x.get("id") != a.id]
        _hist(st, "flaky %s %s%s" % (a.op, a.id, " by " + a.by if a.op == "done" else ""))
    return _mutation(root, "flaky %s %s" % (a.op, a.id), mutate)


def main(argv=None) -> int:
    args = sys.argv[1:] if argv is None else list(argv)
    if args and args[0] == "main-red":
        return main_red_cli(args[1:])
    return common.run(argv, lambda: backend_for(ROOT))


if __name__ == "__main__":
    sys.exit(main())
