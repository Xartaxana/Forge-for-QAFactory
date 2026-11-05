"""Remove the git worktrees whose work is already in main (F6-38, forge/6; spec docs/tasks/specs/t-1210-f6-38-worktree-sweep.md).

    python tools/worktree_sweep.py [--ref <rev>] [--apply] [--repo <path>]
    python tools/worktree_sweep.py --post-merge [--squash-flag <0|1>]     # called by .githooks/post-merge
    python tools/worktree_sweep.py --count                                  # the cheap estimate (SessionStart: `count_estimate`)

t-1738 (FG7-4): the hook and `piles.py close` start the FULL sweep -- every registered worktree, no count or time limit -- as a
detached background process (`launch_background`, `spawn_detached`). Two sweeps never run at once: one lock file, kept alive by a
heartbeat, in `<git common dir>/worktree-sweep/` (lock, status.json, run.log, prev.log, rerun). SessionStart reads status.json
(`read_status`). The only time limit left is the timeout of ONE git call.

Without --apply it is a dry run: nothing is changed in the repository, in a worktree or in a worktree's admin directory
(`--no-optional-locks`, mtimes read before any git call on a copy, the reflog read as a file). With --apply a candidate loses its
service traces, then its worktree (`git worktree remove`, never `--force`), then -- after an archive ref
`refs/worktree-sweep/<branch>/<sha12>` -- its local branch, then its `<name>-scratch` neighbour.

A candidate: registered, not the main worktree, not locked, branch not protected, HEAD merged into --ref (ancestor, or `git cherry`
prints no `+`), has own commits in ITS OWN HEAD reflog OR has been idle longer than T (the live-agent rule), and no real
uncommitted change (an untracked file listed in tools/worktree-junk.json is a service trace, anything else is work).
Whatever cannot be established is read as "alive / keep" (FR-59): a failure of the data file or of git makes FEWER copies removable.

Exit codes: 0 done (also: nothing to remove); 1 cannot work (no ref, not a git repo, --apply from a linked worktree, main
worktree not identifiable, another sweep running); 3 --apply and at least one FAILED. The hook ignores the code.

This module is a link of the enforcement chain (MECHANISM_PREFIXES): it keeps its own stream setup and never imports `streams`.
"""
from __future__ import annotations

import argparse
import dataclasses
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import threading
import time
import uuid
from datetime import datetime
from pathlib import Path

_TOOLS = Path(__file__).resolve().parent
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))

import gitcmd  # noqa: E402

DEFAULT_REF = "origin/main"          # the manual run and --count judge by the remote ref (F1 c)
BACKGROUND_REF = "main"              # the background run and `close` judge by the LOCAL main (F2 a: they see the merge just made); also the hook's branch
T_SECONDS = 24 * 3600                # T: a copy with no own commits is "possibly alive" for this long (F3 a)
COUNT_TIMEOUT = 5
SHOW_PATHS = 5                       # paths of real changes named in a KEEP line, then "(+N more)"
FALLBACK_PROTECTED = (BACKGROUND_REF,)  # the protected list when the data file is unreadable or has none: never empty (M1)
STATE_DIRNAME = "worktree-sweep"     # <git common dir>/worktree-sweep/ : lock, status.json, run.log, prev.log, rerun (F3 a)
LOG_REL = ".git/" + STATE_DIRNAME + "/run.log"
HEARTBEAT_S = 30                     # the live run touches its lock this often ...
STALE_S = 300                        # ... a lock silent for MORE than this is dead (F4 a; 10 beats)
MAX_RUN_S = 6 * 3600                 # ... and a lock older than this is not trusted even when it beats
MAX_PASSES = 3                       # a merge during a run queues another pass; at most this many passes in one run (F5 a)
STATUS_REASON_MAX = 200
STATUS_RETRY_S = 0.2                 # a status write that meets a reader on Windows is retried 3 times, this far apart
DOOR = "python tools/worktree_sweep.py --apply"
STATES = ("running", "finished", "refused", "crashed", "not-started")
ARCHIVE_PREFIX = "refs/worktree-sweep/"
JUNK_FILE = _TOOLS / "worktree-junk.json"
REPARSE_POINT = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
GLOB_CHARS = set("*?[]{}")


class Refuse(Exception):
    """The tool cannot work here; the message says what is wrong, what is expected and the door (FR-1, P15)."""


# --------------------------------------------------------------------------------------------------------- git

class Git:
    """The one git call of this module: (returncode, stdout bytes, stderr text). The runner is `gitcmd.git` unless a test passes
    another with the same signature. The only time limit of a sweep is the timeout of ONE call: `gitcmd.DEFAULT_TIMEOUT`, or
    the number given (SessionStart passes 5)."""

    def __init__(self, runner=None, timeout=None):
        self.runner = runner or gitcmd.git
        self.timeout = gitcmd.DEFAULT_TIMEOUT if timeout is None else timeout

    def __call__(self, root, *args):
        rc, out, err = self.runner(str(root), *args, timeout=self.timeout, stderr=True)
        return rc, out, gitcmd.as_text(err)


def first_line(text):
    lines = [l for l in (text or "").strip().splitlines() if l.strip()]
    return lines[0].strip() if lines else "no message"


def is_timeout(rc, err):
    return rc == -1 and "timed out" in (err or "")


def _key(path):
    return os.path.normcase(os.path.realpath(str(path)))


# --------------------------------------------------------------------------------------------------------- data

@dataclasses.dataclass
class Junk:
    dirs: list
    names: list
    protected: list
    warnings: list


def _entry_problem(entry, is_dir):
    if not isinstance(entry, str) or not entry.strip():
        return "empty or not a string"
    if entry in ("/", "."):
        return "matches everything"
    if entry.startswith(("/", "\\")) or re.match(r"^[A-Za-z]:", entry):
        return "absolute"
    if "\\" in entry:
        return "backslash (posix form expected)"
    if any(c in GLOB_CHARS for c in entry):
        return "glob character"
    if ".." in entry.split("/"):
        return "contains .."
    if is_dir and not entry.endswith("/"):
        return "a directory prefix ends with /"
    if not is_dir and "/" in entry:
        return "a bare file name has no /"
    return None


def load_junk(path=None):
    """The list of service traces (data, not code: FR-13 by meaning). A missing or broken file, or a forbidden entry, only ever
    shrinks the list: more files then count as real changes, fewer copies are removable."""
    path = Path(path or JUNK_FILE)
    junk = Junk([], [], list(FALLBACK_PROTECTED), [])
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError("the top level is not an object")
    except (OSError, ValueError) as exc:
        junk.warnings.append("WARN %s: unreadable (%s: %s) -- every untracked file counts as a real change" % (
            path.name, type(exc).__name__, first_line(str(exc))))
        return junk
    for key, target, is_dir in (("untracked_dirs", junk.dirs, True), ("untracked_names", junk.names, False)):
        values = data.get(key, [])
        if not isinstance(values, list):
            junk.warnings.append("WARN %s: %s is not a list -- ignored" % (path.name, key))
            continue
        for entry in values:
            why = _entry_problem(entry, is_dir)
            if why:
                junk.warnings.append("WARN %s: %s entry %r ignored (%s)" % (path.name, key, entry, why))
            else:
                target.append(entry)
    protected = data.get("protected_branches")
    if isinstance(protected, list):
        junk.protected = [p for p in protected if isinstance(p, str) and p.strip()]
    elif protected is not None:
        junk.warnings.append("WARN %s: protected_branches is not a list -- ignored" % path.name)
    return junk


def is_junk_path(rel, junk):
    return any(rel.startswith(d) for d in junk.dirs) or rel.rsplit("/", 1)[-1] in junk.names


def parse_status(raw):
    """`status --porcelain=v1 -z` -> [(xy, path)]; a rename or copy carries its source as the next NUL field (skipped)."""
    parts = raw.split(b"\0")
    out, i = [], 0
    while i < len(parts):
        entry = parts[i]
        i += 1
        if len(entry) < 4:
            continue
        xy = entry[:2].decode("ascii", "replace")
        out.append((xy, entry[3:].decode("utf-8", "replace")))
        if "R" in xy or "C" in xy:
            i += 1
    return out


def real_changes(entries, junk):
    """(real paths, junk paths). ONLY an untracked (`??`) path of the list is a trace; a modified, deleted or staged tracked
    file is a real change under any path (E14)."""
    real, traces = [], []
    for xy, path in entries:
        (traces if xy == "??" and is_junk_path(path, junk) else real).append(path)
    return real, traces


# --------------------------------------------------------------------------------------------------------- repo

@dataclasses.dataclass
class Worktree:
    path: str
    head: str = ""
    branch: str = ""            # full ref, empty when detached
    detached: bool = False
    bare: bool = False
    locked: object = None       # None = not locked; a string (maybe empty) = locked with that reason
    prunable: object = None

    @property
    def short(self):
        return self.branch[len("refs/heads/"):] if self.branch.startswith("refs/heads/") else self.branch


def parse_worktrees(raw):
    """`git worktree list --porcelain -z`: NUL-terminated fields, an empty field ends an entry."""
    out, cur = [], None
    for field in raw.split(b"\0"):
        text = field.decode("utf-8", "replace")
        if not text:
            if cur is not None:
                out.append(cur)
                cur = None
            continue
        key, _, value = text.partition(" ")
        if key == "worktree":
            if cur is not None:
                out.append(cur)
            cur = Worktree(path=value)
        elif cur is None:
            continue
        elif key == "HEAD":
            cur.head = value
        elif key == "branch":
            cur.branch = value
        elif key == "detached":
            cur.detached = True
        elif key == "bare":
            cur.bare = True
        elif key == "locked":
            cur.locked = value
        elif key == "prunable":
            cur.prunable = value
    if cur is not None:
        out.append(cur)
    return out


@dataclasses.dataclass
class Repo:
    root: Path
    git_dir: Path
    common: Path
    main_path: Path
    linked: bool


def repo_context(git, root):
    """Where this run stands. The common dir is resolved like wiring_check._main_checkout_githooks (a relative answer is
    relative to root; a common dir not named `.git` has no checkout beside it: cannot tell the main worktree, E29)."""
    root = Path(root)
    rc, out, err = git(root, "rev-parse", "--git-dir", "--git-common-dir")
    lines = gitcmd.as_text(out).split("\n")
    if rc != 0 or len([l for l in lines if l.strip()]) < 2:
        raise Refuse("worktree_sweep: %s is not a git repository or git failed (%s) -- run it inside the repository, or pass "
                     "--repo <path>; nothing removed" % (root, first_line(err or gitcmd.as_text(out))))
    resolved = []
    for line in lines[:2]:
        p = Path(line.strip())
        p = p if p.is_absolute() else root / p
        try:
            resolved.append(p.resolve())
        except OSError:
            raise Refuse("worktree_sweep: git dir %s does not resolve; nothing removed" % line.strip())
    git_dir, common = resolved
    if common.name != ".git":
        raise Refuse("worktree_sweep: cannot tell the main worktree: the git common dir %s is not the .git of a checkout "
                     "-- run it in a normal clone; nothing removed" % common)
    return Repo(root, git_dir, common, common.parent, _key(git_dir) != _key(common))


def list_worktrees(git, repo):
    rc, out, err = git(repo.root, "worktree", "list", "--porcelain", "-z")
    if rc != 0:
        raise Refuse("worktree_sweep: git worktree list failed (%s); nothing removed" % first_line(err))
    wts = parse_worktrees(out)
    if not wts or _key(wts[0].path) != _key(repo.main_path) or wts[0].bare:
        raise Refuse("worktree_sweep: cannot tell the main worktree: the first registered worktree (%s) is not the checkout beside "
                     "%s -- nothing removed" % (wts[0].path if wts else "none", repo.common))
    return wts


def admin_dirs(common):
    """{key of worktree path: its admin dir <common>/worktrees/<id>}, by the `gitdir` file of each admin dir (read as files)."""
    out = {}
    base = Path(common) / "worktrees"
    try:
        entries = list(base.iterdir())
    except OSError:
        return out
    for adm in entries:
        try:
            target = (adm / "gitdir").read_text(encoding="utf-8").strip()
        except OSError:
            continue
        if target:
            out[_key(Path(target).parent)] = adm
    return out


def resolve_ref(git, root, ref):
    rc, out, err = git(root, "log", "-1", "--format=%H%x09%cs", ref)
    text = gitcmd.as_text(out).strip()
    if rc != 0 or "\t" not in text:
        raise Refuse("worktree_sweep: the reference %s does not resolve (%s) -- pass --ref main to judge by the local main; "
                     "nothing removed" % (ref, first_line(err or text)))
    sha, date = text.split("\t", 1)
    return sha, date


# --------------------------------------------------------------------------------------------------------- the live-agent rule

def read_reflog(admin):
    """(created_at, own_commits, why): from <admin>/logs/HEAD, read as a FILE. created_at = the timestamp of the first line when
    its old sha is forty zeros. own_commits: a line whose subject starts `commit`, `cherry-pick` or `revert` (a fast-forward, a
    reset, a checkout, a rebase are NOT authorship). Anything else -- no file, empty, cut by gc, unparseable -- is
    (None, None, why): "cannot establish", read as alive."""
    if admin is None:
        return None, None, "no admin directory"
    try:
        text = (Path(admin) / "logs" / "HEAD").read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        return None, None, "cannot read (%s)" % type(exc).__name__
    lines = [l for l in text.split("\n") if l.strip()]
    if not lines:
        return None, None, "empty"
    own, created = False, None
    for n, line in enumerate(lines):
        head, _, subject = line.partition("\t")
        tokens = head.split()
        if len(tokens) < 5 or not tokens[-2].isdigit() or len(tokens[0]) != 40 or len(tokens[1]) != 40:
            return None, None, "line %d does not parse" % (n + 1)
        if n == 0:
            if set(tokens[0]) != {"0"}:
                return None, None, "cut (the first entry is not the creation)"
            created = int(tokens[-2])
        if subject.startswith(("commit", "cherry-pick", "revert")):
            own = True
    return created, own, ""


def read_activity(admin, wt_path, junk, created_at):
    """The newest mtime of: the creation time, <admin>/{HEAD,index,logs/HEAD}, and the service traces inside the copy (the hooks
    write them while an agent works). ONLY stat calls -- read BEFORE any git call on the copy (M2). (None, why) if nothing."""
    stamps = [created_at] if created_at is not None else []
    paths = []
    if admin is not None:
        paths += [Path(admin) / "HEAD", Path(admin) / "index", Path(admin) / "logs" / "HEAD"]
    wt = Path(wt_path)
    for rel in junk.dirs:
        base = wt / rel.rstrip("/")
        paths.append(base)
        for dirpath, dirnames, filenames in os.walk(base):
            paths += [Path(dirpath) / n for n in dirnames + filenames]
    paths += [wt / name for name in junk.names]
    for p in paths:
        try:
            stamps.append(p.stat().st_mtime)
        except FileNotFoundError:
            continue
        except OSError as exc:
            return None, "cannot stat %s (%s)" % (p.name, type(exc).__name__)
    return (max(stamps), "") if stamps else (None, "no timestamp to read")


# --------------------------------------------------------------------------------------------------------- one copy

@dataclasses.dataclass
class Ctx:
    git: Git
    repo: Repo
    ref: str
    junk: Junk
    admins: dict
    now: float
    T: float
    protected: set
    registered: set


@dataclasses.dataclass
class Eval:
    kind: str                   # candidate | keep | prunable
    text: str = ""              # the reason of a keep
    merged: str = ""
    own: str = "no"
    traces: list = dataclasses.field(default_factory=list)


def merged_verdict(git, repo_root, head, ref):
    """('ancestor' | 'patch-equal' | 'unmerged' | 'unknown', detail). An ancestor cannot err toward "merged". `git cherry` can
    (a commit equal to an old main commit that main later reverted; a branch whose only work is a merge commit, which cherry
    skips) -- that error direction is covered by the archive ref taken before every branch deletion (M4)."""
    rc, _, err = git(repo_root, "merge-base", "--is-ancestor", head, ref)
    if rc == 0:
        return "ancestor", ""
    if rc != 1:
        return "unknown", first_line(err)
    rc, out, err = git(repo_root, "cherry", ref, head)
    if rc != 0:
        return "unknown", first_line(err)
    plus = [l for l in gitcmd.as_text(out).split("\n") if l.startswith("+")]
    return ("unmerged", str(len(plus))) if plus else ("patch-equal", "")


def evaluate(ctx, wt):
    if wt.locked is not None:
        return Eval("keep", "locked (%s)" % (wt.locked or "no reason given"))
    if wt.prunable is not None:
        return Eval("prunable")
    if wt.bare:
        return Eval("keep", "bare repository entry")
    if wt.short and wt.short in ctx.protected:
        return Eval("keep", "protected branch %s" % wt.short)
    admin = ctx.admins.get(_key(wt.path))
    created, own, why = read_reflog(admin)
    # M2: every mtime BEFORE any git call that is about this copy
    last, last_why = read_activity(admin, wt.path, ctx.junk, created)
    merged, detail = merged_verdict(ctx.git, ctx.repo.root, wt.head, ctx.ref)
    if merged == "unmerged":
        return Eval("keep", "unmerged (%s commits not in %s)" % (detail, ctx.ref))
    if merged == "unknown":
        return Eval("keep", "unknown (merge check: %s)" % detail)
    ev = Eval("candidate", merged=merged, own="yes" if own else "no")
    if not own:
        # the live-agent rule: a fresh copy has HEAD = a commit of main, so it always reads as merged
        if last is None:
            return Eval("keep", "unknown (%s)" % (("worktree reflog: " + why) if why else last_why))
        age = ctx.now - last
        if not age > ctx.T:                                              # strictly: age == T is still alive
            if own is None:
                return Eval("keep", "unknown (worktree reflog: %s)" % why)
            return Eval("keep", "no own commits, active %dh ago (< %dh)" % (age // 3600, ctx.T // 3600))
    rc, out, err = ctx.git(wt.path, "--no-optional-locks", "status", "--porcelain=v1", "-z", "--untracked-files=all")
    if rc != 0:
        return Eval("keep", "unknown (status: %s)" % first_line(err or gitcmd.as_text(out)))
    real, traces = real_changes(parse_status(out), ctx.junk)
    if real:
        shown = ", ".join(real[:SHOW_PATHS]) + (" (+%d more)" % (len(real) - SHOW_PATHS) if len(real) > SHOW_PATHS else "")
        return Eval("keep", "real changes: %s -- to let it go: save them (git -C \"%s\" diff; copy the untracked files), then "
                            "git worktree remove --force \"%s\"" % (shown, wt.path, wt.path))
    ev.traces = traces
    return ev


# --------------------------------------------------------------------------------------------------------- apply

def _writable_retry(func, path, exc_info):
    try:
        os.chmod(path, stat.S_IWRITE)
        func(path)
    except OSError:
        raise


def remove_traces(wt_path, traces):
    """Step 1: delete exactly the untracked service traces the status read named, then the directories that became empty
    (bottom-up, only empty ones). Nothing else inside the copy is touched."""
    root = Path(wt_path)
    dirs = set()
    for rel in traces:
        p = root / rel
        try:
            os.chmod(p, stat.S_IWRITE)
            os.remove(p)
        except OSError:
            pass
        d = p.parent
        while d != root and root in d.parents:
            dirs.add(d)
            d = d.parent
    for d in sorted(dirs, key=lambda x: len(x.parts), reverse=True):
        try:
            d.rmdir()
        except OSError:
            pass


def archive_head(git, repo_root, name, head):
    """(ok, archive ref or message): `refs/worktree-sweep/<name>/<sha12>` created and read back. An existing ref equal to `head`
    is not an error and is left alone. Used before a branch is deleted (M4) and before a detached HEAD loses its only
    reference, the worktree admin dir (a removed copy, a pruned registration)."""
    if not head:
        return False, "archive ref failed (no HEAD sha to keep)"
    ref = "%s%s/%s" % (ARCHIVE_PREFIX, name, head[:12])
    rc, out, err = git(repo_root, "rev-parse", "--verify", "--quiet", ref + "^{commit}")
    if not (rc == 0 and gitcmd.as_text(out).strip() == head):
        rc, _, err = git(repo_root, "update-ref", ref, head)
        if rc != 0:
            return False, "archive ref failed (%s)" % first_line(err)
        rc, out, err = git(repo_root, "rev-parse", "--verify", "--quiet", ref + "^{commit}")
        if rc != 0 or gitcmd.as_text(out).strip() != head:
            return False, "archive ref failed (%s does not read back as %s)" % (ref, head[:12])
    return True, ref


def detached_name(ctx, wt):
    """The name part of the archive ref of a detached HEAD: `detached/<admin dir id>` (the copy's folder name when no admin dir)."""
    admin = ctx.admins.get(_key(wt.path))
    return "detached/%s" % (Path(admin).name if admin is not None else Path(wt.path).name)


def archive_and_delete_branch(git, repo_root, branch, head):
    """(ok, archive ref or message). The archive ref comes first, is verified, and only then `branch -D` (M4)."""
    ok, ref = archive_head(git, repo_root, branch, head)
    if not ok:
        return False, ref
    rc, out, err = git(repo_root, "rev-parse", "--verify", "--quiet", "refs/heads/%s^{commit}" % branch)
    if rc == 0 and gitcmd.as_text(out).strip() != head:
        return False, "the branch moved since the worktree was read (archive ref kept: %s)" % ref
    rc, out, err = git(repo_root, "branch", "-D", branch)
    if rc != 0:
        return False, first_line(err or gitcmd.as_text(out))
    return True, ref


def _is_link(path):
    p = str(path)
    if os.path.islink(p):
        return True
    isjunction = getattr(os.path, "isjunction", None)
    if isjunction is not None:
        return bool(isjunction(p))
    try:
        return bool(os.lstat(p).st_file_attributes & REPARSE_POINT)
    except (OSError, AttributeError):
        return False


def _rmtree(path):
    # CPython >= 3.8 rmtree does not descend into a junction or a symlink; the link case is refused before this anyway (E38)
    if sys.version_info >= (3, 12):
        shutil.rmtree(path, onexc=lambda func, p, exc: _writable_retry(func, p, exc))
    else:
        shutil.rmtree(path, onerror=_writable_retry)


def scratch_of(wt_path, registered):
    """(path, state) of `<path>-scratch`: state None = nothing there; 'ok' = may go; 'link' = a link; 'registered' / 'git' = refuse."""
    p = Path(str(wt_path) + "-scratch")
    if not os.path.lexists(str(p)):
        return p, None
    if _is_link(p):
        return p, "link"
    if not p.is_dir():
        return p, None
    if _key(p) in registered:
        return p, "registered"
    if (p / ".git").exists():
        return p, "git"
    return p, "ok"


class Report:
    def __init__(self, out=None):
        self.lines, self.registered, self.done, self.kept, self.failed = [], 0, 0, 0, 0
        self.refused, self.apply, self.sha, self.out = None, False, "", out

    def add(self, line):
        """`out` sees every line the moment it is added: the journal of a long run grows line by line (FR-43 by meaning)."""
        self.lines.append(line)
        if self.out is not None:
            self.out(line)

    @property
    def exit_code(self):
        if self.refused:
            return 1
        return 3 if self.apply and self.failed else 0


def _q(path):
    return '"%s"' % path


def apply_one(ctx, wt, ev, rep):
    git, root = ctx.git, ctx.repo.root
    archive = ""
    if not wt.short:                                                      # a detached HEAD: the admin dir is its only reference (B1)
        ok, info = archive_head(git, root, detached_name(ctx, wt), wt.head)
        if not ok:
            rep.kept += 1
            rep.add("KEEP %s: %s" % (_q(wt.path), info))
            return
        archive = ", archive: " + info
    remove_traces(wt.path, ev.traces)
    rc, out, err = git(root, "worktree", "remove", wt.path)               # never --force: git refuses a file that appeared since the read
    if rc != 0:
        msg = first_line(err or gitcmd.as_text(out))
        if is_timeout(rc, err):
            rep.failed += 1
            rep.add("FAILED %s: timeout (%s)" % (_q(wt.path), msg))
        else:
            rc2, out2, err2 = git(wt.path, "--no-optional-locks", "status", "--porcelain=v1", "-z", "--untracked-files=all")
            real = rc2 == 0 and real_changes(parse_status(out2), ctx.junk)[0]
            if real:
                rep.kept += 1
                rep.add("KEEP %s: changed during sweep (%s)" % (_q(wt.path), msg))
            else:
                rep.failed += 1
                rep.add("FAILED %s: %s" % (_q(wt.path), msg))
        admin = ctx.admins.get(_key(wt.path))
        if os.path.isdir(wt.path) and admin is not None and not Path(admin).exists():
            rep.add("ORPHAN %s" % _q(wt.path))
        return
    if os.path.exists(wt.path):
        rep.failed += 1
        rep.add("FAILED %s: git removed the worktree but the folder is still there" % _q(wt.path))
        return
    extra = []
    if wt.short:
        ok, info = archive_and_delete_branch(git, root, wt.short, wt.head)
        if ok:
            archive = ", archive: " + info
        else:
            extra.append("KEEP branch %s: %s" % (wt.short, info))
    rep.done += 1
    rep.add("REMOVED %s (branch %s, merged: %s, own commits: %s, junk: %d files%s)" % (
        _q(wt.path), wt.short or "(detached)", ev.merged, ev.own, len(ev.traces), archive))
    for line in extra:
        rep.add(line)
    scratch, state = scratch_of(wt.path, ctx.registered)
    if state == "link":
        rep.add("KEEP scratch %s: link" % _q(scratch))
    elif state == "ok":
        try:
            _rmtree(scratch)
            rep.add("SCRATCH %s" % _q(scratch))
        except Exception as exc:                                         # a long path and the like: a line, not a crash
            rep.failed += 1
            rep.add("FAILED scratch %s: %s: %s" % (_q(scratch), type(exc).__name__, first_line(str(exc))))


# --------------------------------------------------------------------------------------------------------- the sweep

def _orphan_scratch(wts, registered):
    parents = {Path(w.path).parent for w in wts}
    found = []
    for parent in sorted(parents, key=str):
        try:
            names = sorted(os.listdir(parent))
        except OSError:
            continue
        for name in names:
            if name.endswith("-scratch") and len(name) > len("-scratch"):
                p = parent / name
                if _key(parent / name[:-len("-scratch")]) not in registered and not _is_link(p) and p.is_dir():
                    found.append(p)
    return found


def prune_registrations(ctx, wts, rep):
    """`git worktree prune` drops EVERY unlocked prunable registration with its admin dir -- and a detached HEAD has no other
    reference (B1). So each such registration whose HEAD is not reachable from ref gets an archive ref first; if one cannot be
    made, nothing is pruned (one line) and the sweep goes on. True when the prune ran and succeeded."""
    git, root = ctx.git, ctx.repo.root
    bad = []
    for w in wts[1:]:
        if w.prunable is None or w.locked is not None:
            continue
        if w.head and git(root, "merge-base", "--is-ancestor", w.head, ctx.ref)[0] == 0:
            continue
        ok, info = archive_head(git, root, w.short or detached_name(ctx, w), w.head)
        if not ok:
            bad.append("%s: %s" % (_q(w.path), info))
    if bad:
        rep.add("KEEP prune: not run, %d registration(s) could not be archived (%s)" % (len(bad), bad[0]))
        return False
    rc, out, err = git(root, "worktree", "prune")
    if rc != 0:
        rep.failed += 1
        rep.add("FAILED worktree prune: %s" % first_line(err or gitcmd.as_text(out)))
    return True


def sweep(root, *, ref=DEFAULT_REF, apply=False, now=None, T=T_SECONDS, runner=None, junk=None, ref_note="", out=None,
          should_stop=None, progress=None):
    """One pass over ALL registered worktrees. Each copy is judged by its state at ITS turn (a fresh `worktree list`), not by
    the snapshot of the start: a commit made in a copy during a long run is not lost, a copy locked since stays. `should_stop()`
    true before a copy ends the pass (the sweep lock was lost); `progress(seen, registered)` follows every copy; `out(line)`
    follows every line. `now` is taken once per pass: a long pass under-states the age of copies, an error toward "keep"."""
    rep = Report(out)
    rep.apply = apply
    git = Git(runner)
    now = time.time() if now is None else now
    junk = junk if junk is not None else load_junk()
    try:
        repo = repo_context(git, root)
        if apply and repo.linked:
            raise Refuse("worktree_sweep: --apply runs from the main checkout %s; this is the linked worktree %s -- run it "
                         "there; nothing removed" % (repo.main_path, repo.root))
        sha, date = resolve_ref(git, repo.root, ref)
        wts = list_worktrees(git, repo)
    except Refuse as exc:
        rep.refused = str(exc)
        rep.add(rep.refused)
        return rep
    linked = wts[1:]
    rep.registered = len(linked)
    rep.sha = sha[:7]
    registered = {_key(w.path) for w in wts}
    protected = set(junk.protected) | {ref.rsplit("/", 1)[-1]}
    if wts[0].short:
        protected.add(wts[0].short)
    ctx = Ctx(git, repo, ref, junk, admin_dirs(repo.common), now, T, protected, registered)
    for w in junk.warnings:
        rep.add(w)
    rep.add("judged against %s at %s (%s)%s" % (ref, sha[:7], date, ref_note))
    prunable, stopped = [], False
    for seen, listed in enumerate(linked, 1):
        if should_stop is not None and should_stop():
            rep.add("STOPPED: the sweep lock was lost -- the rest is left for the next run")
            stopped = True
            break
        try:                                                              # the copy as it is NOW, not as the run began (E20, E21)
            fresh = {_key(w.path): w for w in list_worktrees(git, repo)}
        except Exception as exc:
            rep.kept += 1
            rep.add("KEEP %s: unknown (worktree list: %s)" % (_q(listed.path), first_line(str(exc))))
            if progress is not None:
                progress(seen, rep.registered)
            continue
        wt = fresh.get(_key(listed.path))
        if wt is None:
            rep.add("GONE %s: no longer registered" % _q(listed.path))
            if progress is not None:
                progress(seen, rep.registered)
            continue
        try:
            ev = evaluate(ctx, wt)
        except Exception as exc:                                         # one copy never stops the others (E24)
            ev = Eval("keep", "unknown (%s: %s)" % (type(exc).__name__, first_line(str(exc))))
        if ev.kind == "prunable":
            prunable.append(wt)
            rep.add("PRUNABLE %s" % _q(wt.path))
            rep.done += 1
        elif ev.kind == "keep":
            rep.kept += 1
            rep.add("KEEP %s: %s" % (_q(wt.path), ev.text))
        elif not apply:
            rep.done += 1
            rep.add("CAN REMOVE %s (branch %s, merged: %s, own commits: %s, junk: %d files)" % (
                _q(wt.path), wt.short or "(detached)", ev.merged, ev.own, len(ev.traces)))
            scratch, state = scratch_of(wt.path, registered)
            if state == "link":
                rep.add("KEEP scratch %s: link" % _q(scratch))
            elif state == "ok":
                rep.add("SCRATCH %s" % _q(scratch))
        else:
            try:
                apply_one(ctx, wt, ev, rep)
            except Exception as exc:                                     # one copy never stops the others (M3)
                rep.failed += 1
                rep.add("ERROR %s: %s: %s" % (_q(wt.path), type(exc).__name__, first_line(str(exc))))
        if progress is not None:
            progress(seen, rep.registered)
    if apply and prunable and not stopped:
        try:
            current = list_worktrees(git, repo)                          # a registration that went prunable during the run is archived too (E23)
        except Exception as exc:
            current = None
            rep.add("KEEP prune: not run (worktree list: %s)" % first_line(str(exc)))
        pruned = current is not None and prune_registrations(ctx, current, rep)
        for wt in prunable if pruned else ():                                            # the folder is gone: only the branch is left to judge
            if not wt.short or wt.short in protected or not wt.head:
                continue
            merged, detail = merged_verdict(git, repo.root, wt.head, ref)
            if merged not in ("ancestor", "patch-equal"):
                rep.add("KEEP branch %s: %s" % (wt.short, "unmerged (%s commits not in %s)" % (detail, ref)
                                                 if merged == "unmerged" else "unknown (merge check: %s)" % detail))
                continue
            ok, info = archive_and_delete_branch(git, repo.root, wt.short, wt.head)
            rep.add("REMOVED branch %s (prunable worktree, merged: %s, archive: %s)" % (wt.short, merged, info) if ok
                    else "KEEP branch %s: %s" % (wt.short, info))
    if not stopped:
        for p in _orphan_scratch(wts, registered):
            rep.add("ORPHAN SCRATCH %s" % _q(p))
    rep.add("worktree_sweep: %d registered, %d %s, %d kept, %d failed" % (
        rep.registered, rep.done, "removed" if apply else "can go", rep.kept, rep.failed))
    return rep


# --------------------------------------------------------------------------------------------------------- the state directory

def state_dir(repo):
    """The common .git of the clone: outside every tree, untracked by git, one for all worktrees (F3 a)."""
    return repo.common / STATE_DIRNAME


def _iso(ts=None):
    return datetime.fromtimestamp(time.time() if ts is None else ts).isoformat()


def _iso_epoch(text):
    try:
        return datetime.fromisoformat(str(text)).timestamp()
    except (ValueError, TypeError, OverflowError, OSError):
        return None


def _read_lock(path):
    """(info dict | None, mtime | None): mtime None = no lock file; info None = a file that is not our JSON."""
    try:
        mtime = os.stat(path).st_mtime
    except OSError:
        return None, None
    try:
        info = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None, mtime
    return (info, mtime) if isinstance(info, dict) else (None, mtime)


def _lock_stale(info, mtime, now):
    """The ONE freshness test of a lock (acquire_lock and read_status both call it). Dead = the heartbeat is silent for MORE than
    STALE_S, or the run is older than MAX_RUN_S; an unreadable lock is judged by its mtime only. Strict `>`: exactly at the limit
    the lock is still alive -- the error direction of this test is "busy" (a sweep waits), never two runs at once."""
    if now - mtime > STALE_S:
        return True
    started = _iso_epoch(info.get("started")) if info else None
    return started is not None and now - started > MAX_RUN_S


def _holder(info):
    if info is None:
        return {"token": "unreadable", "pid": None, "started": "unknown", "trigger": "unknown", "unreadable": True}
    return info


class Lock:
    """The right to run a sweep. mtime of the file is the heartbeat; a run that finds the file gone or another token in it has
    LOST the lock (`lost` is set) and removes nothing more."""

    def __init__(self, path, token, pid, started, trigger):
        self.path, self.token, self.pid, self.started, self.trigger = Path(path), token, pid, started, trigger
        self.lost = threading.Event()
        self._stop = threading.Event()

    def _body(self):
        return {"token": self.token, "pid": self.pid, "started": self.started, "trigger": self.trigger}

    def own(self):
        info, _ = _read_lock(self.path)
        return info is not None and info.get("token") == self.token

    def holds(self, retry_s=0.05):
        """Is the lock file ours RIGHT NOW (checked before every copy, E10). A read that fails (a reader on Windows, an empty
        file mid-write) is tried once more after `retry_s`; a second miss, or another token, counts as not ours."""
        for attempt in range(2):
            info, _ = _read_lock(self.path)
            if info is not None:
                return info.get("token") == self.token
            if attempt == 0:
                time.sleep(retry_s)
        return False

    def set_pid(self, pid):
        """The detached child writes its own pid (the parent wrote its own at launch). Informational: a failure is not one."""
        self.pid = pid
        tmp = self.path.with_name(self.path.name + ".tmp")
        try:
            tmp.write_text(json.dumps(self._body()), encoding="utf-8")
            os.replace(tmp, self.path)
        except OSError:
            pass

    def beat(self):
        """One heartbeat: touch the lock when it is still ours, else mark it lost. True = still ours."""
        if not self.own():
            self.lost.set()
            return False
        try:
            os.utime(self.path)
        except OSError:
            self.lost.set()
            return False
        return True

    def heartbeat(self, interval=HEARTBEAT_S):
        def loop():
            while not self._stop.wait(interval):
                if not self.beat():
                    return
        threading.Thread(target=loop, daemon=True, name="worktree-sweep-heartbeat").start()

    def release(self):
        """Delete the lock only when it still carries OUR token."""
        self._stop.set()
        if self.own():
            try:
                os.remove(self.path)
            except OSError:
                pass


def _try_create(path, trigger, now):
    try:
        fd = os.open(str(path), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        return None
    lock = Lock(path, uuid.uuid4().hex, os.getpid(), _iso(now), trigger)
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(json.dumps(lock._body()))
    return lock


def _put_back(moved, path):
    """Return a lock file we moved away by mistake. It never overwrites another lock: on POSIX `os.link` + `os.unlink` (a
    FileExistsError leaves the moved file where it is -- the caller reports busy); Windows `os.rename` already refuses to replace."""
    try:
        if os.name == "nt":
            os.rename(moved, path)
        else:
            os.link(moved, path)
            os.unlink(moved)
    except OSError:
        pass


def acquire_lock(dir, trigger, now=None):
    """(Lock | None, holder | None). OSError of the directory goes out (the caller turns it into "not started")."""
    now = time.time() if now is None else now
    dir = Path(dir)
    dir.mkdir(parents=True, exist_ok=True)
    path = dir / "lock"
    lock = _try_create(path, trigger, now)
    if lock:
        return lock, None
    info, mtime = _read_lock(path)
    if mtime is None:                                                    # it vanished between the two calls
        lock = _try_create(path, trigger, now)
        return (lock, None) if lock else (None, _holder(None))
    if not _lock_stale(info, mtime, now):
        return None, _holder(info)
    seen = (info or {}).get("token")
    moved = path.with_name("lock.stale-%d-%s" % (int(now), str(seen)[:8] if seen else "unreadable"))
    try:
        os.rename(path, moved)
    except OSError:                                                      # somebody else took it first
        return None, _holder(info)
    again, _ = _read_lock(moved)                                         # we may have renamed a NEW lock another run made meanwhile: put it back
    if again is not None and (seen is None or again.get("token") != seen):
        _put_back(moved, path)
        return None, _holder(again)
    lock = _try_create(path, trigger, now)
    return (lock, None) if lock else (None, _holder(None))


@dataclasses.dataclass
class SweepState:
    kind: str                   # none | unreadable | running | died | finished | refused | crashed | not-started
    data: dict = dataclasses.field(default_factory=dict)
    reason: str = ""


def read_status(root, runner=None, timeout=COUNT_TIMEOUT, now=None):
    """What the last background sweep says about itself (SessionStart). One `repo_context` (git, `timeout`) and two small files.
    Raises RuntimeError(reason) when git cannot say where the state directory is."""
    now = time.time() if now is None else now
    try:
        repo = repo_context(Git(runner, timeout), root)
    except Refuse as exc:
        raise RuntimeError(first_line(str(exc)))
    directory = state_dir(repo)
    try:
        raw = (directory / "status.json").read_text(encoding="utf-8")
    except FileNotFoundError:
        return SweepState("none")
    except OSError as exc:
        return SweepState("unreadable", {}, "cannot read status.json (%s)" % type(exc).__name__)
    try:
        data = json.loads(raw)
    except ValueError:
        return SweepState("unreadable", {}, "status.json is %s" % ("empty" if not raw.strip() else "not JSON"))
    if not isinstance(data, dict) or data.get("state") not in STATES:
        return SweepState("unreadable", {}, "status.json has no known state")
    info, mtime = _read_lock(directory / "lock")
    data["heartbeat"] = _iso(mtime) if mtime is not None else None
    state = data["state"]
    if state != "running":
        return SweepState(state, data, str(data.get("reason") or ""))
    alive = info is not None and mtime is not None and info.get("token") == data.get("token") and not _lock_stale(info, mtime, now)
    return SweepState("running" if alive else "died", data)


# --------------------------------------------------------------------------------------------------------- journal and status files

class Journal:
    """run.log: text, one line per Report line, written the moment the line exists (line-buffered). The previous run's log
    becomes prev.log; when that fails the new run appends to run.log after a `----` line (the old text is not lost silently)."""

    def __init__(self, directory):
        self.path = Path(directory) / "run.log"
        self.f = None

    def start(self, header):
        prev = self.path.with_name("prev.log")
        separator = False
        if self.path.exists():
            try:
                os.replace(self.path, prev)
            except OSError:
                separator = True
        self.f = open(self.path, "a", encoding="utf-8", buffering=1)
        if separator:
            self.line("----")
        self.line(header)

    def line(self, text):
        if self.f is not None:
            self.f.write(text + "\n")

    def close(self):
        if self.f is not None:
            try:
                self.f.close()
            finally:
                self.f = None


class StatusFile:
    """status.json, replaced atomically; a failed write is a WARN line in the journal, never a stop of the sweep (P1)."""

    def __init__(self, directory, journal=None):
        self.path = Path(directory) / "status.json"
        self.journal = journal
        self.data = {}
        self.warned = False

    def update(self, **fields):
        self.data.update(fields)
        data = dict(self.data)
        data["reason"] = str(data.get("reason") or "")[:STATUS_REASON_MAX]
        tmp = self.path.with_name("status.json.tmp")
        error = None
        for attempt in range(4):                                         # the first try and up to 3 retries
            try:
                tmp.write_text(json.dumps(data), encoding="utf-8")
                os.replace(tmp, self.path)
                return True
            except PermissionError as exc:
                error = exc
                time.sleep(STATUS_RETRY_S)
            except OSError as exc:
                error = exc
                break
        if self.journal is not None and not self.warned:
            self.warned = True
            self.journal.line("WARN status not written (%s: %s)" % (type(error).__name__, first_line(str(error))))
        return False


def _new_status(lock, ref=None):
    ref = ref or BACKGROUND_REF
    return {"state": "running", "token": lock.token, "trigger": lock.trigger, "pid": lock.pid, "started": lock.started,
            "finished": None, "ref": ref, "sha": "", "registered": 0, "done": 0, "removed": 0, "kept": 0, "failed": 0,
            "passes": 0, "reason": ""}


# --------------------------------------------------------------------------------------------------------- the run

def run_locked(repo, lock, trigger, out=None, *, ref=None, junk=None, runner=None, heartbeat_s=HEARTBEAT_S):
    """The body of a sweep run, one path for the background run and the manual --apply. The caller holds `lock`; it is released
    here. Passes repeat while a merge left `rerun` behind, at most MAX_PASSES. Returns the Report of the last pass."""
    ref = ref or BACKGROUND_REF
    directory = state_dir(repo)
    journal = Journal(directory)
    status = StatusFile(directory, journal)
    status.data = _new_status(lock, ref)
    status.data["pid"] = os.getpid()
    rerun = directory / "rerun"
    rep = Report()
    removed, passes = 0, 0
    try:
        journal.start("worktree_sweep: %s run %s started %s, pid %d" % (trigger, lock.token[:8], lock.started, os.getpid()))
        status.update()
        lock.heartbeat(heartbeat_s)

        def emit(line):
            journal.line(line)
            if out is not None:
                out(line)

        def lost():
            """The lock is no longer ours (heartbeat saw it, or the token check before this copy did): no more removals and
            no more writes of status.json -- it belongs to the new holder (E10)."""
            if lock.lost.is_set():
                return True
            if lock.holds():
                return False
            lock.lost.set()
            return True

        def progress(done, registered):
            if not lost():
                status.update(done=done, registered=registered)

        note = " (local main, may be unpushed)" if ref == BACKGROUND_REF else ""
        while True:
            passes += 1
            try:
                rerun.unlink()
            except FileNotFoundError:
                pass
            if not lost():
                status.update(done=0, passes=passes)
            rep = sweep(repo.main_path, ref=ref, apply=True, out=emit, should_stop=lost, progress=progress,
                        ref_note=note, junk=junk, runner=runner)
            removed += rep.done
            if rep.refused or lost():
                break
            if rerun.exists():
                if passes < MAX_PASSES:
                    continue
                emit("rerun left for the next trigger (%d passes done)" % MAX_PASSES)
            break
        if not lost():
            if rep.refused:
                status.update(state="refused", finished=_iso(), reason=first_line(rep.refused), registered=rep.registered)
            else:
                status.update(state="finished", finished=_iso(), registered=rep.registered, removed=removed, kept=rep.kept,
                              failed=rep.failed, passes=passes, sha=rep.sha, reason="")
    except Exception as exc:
        reason = "%s: %s" % (type(exc).__name__, first_line(str(exc)))
        journal.line("CRASHED %s" % reason)
        if not (lock.lost.is_set() or not lock.holds()):
            status.update(state="crashed", finished=_iso(), reason=reason)
    finally:
        lock.release()
        journal.close()
    return rep


def _env_without_git():
    return {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}


_IS_WINDOWS = os.name == "nt"


def spawn_detached(argv, cwd, env):
    """The ONE place a background process is made (F1 a): no console, its own process group, out of the caller's job object
    (`git merge` and a tool call of a session must not wait for it or take it down), stdio closed. A job that forbids breakaway
    refuses the flag with OSError -- then it is made without it. Returns the pid."""
    kw = dict(cwd=str(cwd), env=env, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, close_fds=True)
    if _IS_WINDOWS:
        flags = 0x00000008 | 0x00000200                                  # DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP
        try:
            proc = subprocess.Popen(argv, creationflags=flags | 0x01000000, **kw)    # | CREATE_BREAKAWAY_FROM_JOB
        except OSError:
            proc = subprocess.Popen(argv, creationflags=flags, **kw)
    else:
        proc = subprocess.Popen(argv, start_new_session=True, **kw)
    return proc.pid


def launch_background(root, trigger, spawn=None, now=None, runner=None):
    """(kind, text), kind in started | busy | refused | failed. Starts the full sweep detached, from the main checkout's own copy
    of this tool. `spawn` is looked up at call time (a test replaces the module attribute)."""
    spawn = spawn or spawn_detached
    now = time.time() if now is None else now
    git = Git(runner)
    try:
        repo = repo_context(git, root)
    except Refuse as exc:
        return "refused", first_line(str(exc))
    if repo.linked:
        return "refused", "background sweep runs from the main checkout %s; this is the linked worktree %s" % (repo.main_path, repo.root)
    tool = repo.main_path / "tools" / "worktree_sweep.py"
    if not tool.is_file():
        return "refused", "tools/worktree_sweep.py not found in %s" % repo.main_path
    directory = state_dir(repo)
    try:
        lock, holder = acquire_lock(directory, trigger, now)
    except OSError as exc:
        return "failed", "background sweep not started (cannot make %s: %s)" % (directory, first_line(str(exc)))
    if lock is None:
        try:
            (directory / "rerun").write_text(_iso(now), encoding="utf-8")
        except OSError:
            pass
        return "busy", "a worktree sweep is already running since %s (%s); a second pass is queued" % (
            holder.get("started", "unknown"), holder.get("trigger", "unknown"))
    status = StatusFile(directory)
    status.data = _new_status(lock)
    status.data["pid"] = None
    status.update()
    try:
        spawn([sys.executable, str(tool), "--background-run", "--token", lock.token, "--repo", str(repo.main_path)],
              repo.main_path, _env_without_git())
    except Exception as exc:
        reason = "%s: %s" % (type(exc).__name__, first_line(str(exc)))
        status.update(state="not-started", finished=_iso(), reason=reason)
        lock.release()
        return "failed", "background sweep not started (%s)" % reason
    return "started", "worktree sweep started in the background (log %s)" % LOG_REL


def not_started(text):
    """The line of a caller (post-merge, close) for a launch that did not start: the reason and the door."""
    reason = text if text.startswith("background sweep not started") else "background sweep not started (%s)" % text
    return "%s -- %s" % (reason, DOOR)


def post_merge(root, squash_flag="0", *, runner=None, spawn=None):
    """The hook body. Second line of the guard (the first is in the sh file): nothing from a linked worktree, nothing off the
    branch the merges land on -- there the tool is the branch's copy, and a builder's merge would sweep its neighbours.
    Whatever the merge was (squash or not, ORIG_HEAD or not), the full sweep does not depend on it: it looks at every copy."""
    rep = Report()
    rep.apply = True
    git = Git(runner)
    try:
        repo = repo_context(git, root)
    except Refuse:
        return rep
    if repo.linked:
        return rep
    rc, out, _ = git(repo.root, "symbolic-ref", "--short", "-q", "HEAD")
    if rc != 0 or gitcmd.as_text(out).strip() != BACKGROUND_REF:
        return rep
    kind, text = launch_background(root, "post-merge", spawn=spawn, runner=runner)
    rep.add("post-merge: %s" % (text if kind in ("started", "busy") else not_started(text)))
    return rep


def count_estimate(root, timeout=COUNT_TIMEOUT, ref=DEFAULT_REF, runner=None):
    """(registered, on merged branches, ref): at most two git calls, no `status`. An ESTIMATE: it includes copies the full run
    keeps (real changes, a live agent). Raises RuntimeError with the reason when git cannot answer."""
    run = runner or gitcmd.git
    rc, out, err = run(str(root), "worktree", "list", "--porcelain", "-z", timeout=timeout, stderr=True)
    if rc != 0:
        raise RuntimeError("worktree list: %s" % first_line(gitcmd.as_text(err)))
    wts = parse_worktrees(out)
    if not wts:
        raise RuntimeError("worktree list: no entries")
    rc, out, err = run(str(root), "branch", "--merged", ref, "--format=%(refname)", timeout=timeout, stderr=True)
    if rc != 0:
        raise RuntimeError("branch --merged %s: %s" % (ref, first_line(gitcmd.as_text(err))))
    merged = set(gitcmd.as_text(out).split("\n"))
    linked = wts[1:]
    return len(linked), sum(1 for w in linked if w.locked is None and w.branch and w.branch in merged), ref


# --------------------------------------------------------------------------------------------------------- CLI

def main(argv=None):
    for stream in (sys.stdout, sys.stderr):                              # a link keeps its own copy of the stream setup (axis 15)
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass
    ap = argparse.ArgumentParser(prog="worktree_sweep", description=__doc__.split("\n")[0])
    ap.add_argument("--ref", default=None, help="what `merged` is judged against (default %s)" % DEFAULT_REF)
    ap.add_argument("--apply", action="store_true", help="remove the candidates (default: a dry run)")
    ap.add_argument("--repo", default=None, help="the repository (default: the current directory)")
    ap.add_argument("--post-merge", action="store_true", help="the hook form: start the full sweep in the background")
    ap.add_argument("--squash-flag", default="0", help="the hook's argument: 1 after merge --squash (the sweep does not depend on it)")
    ap.add_argument("--count", action="store_true", help="print the cheap estimate: the number of copies on merged branches")
    ap.add_argument("--background-run", action="store_true", help="internal: the detached run started by the hook / close")
    ap.add_argument("--token", default=None, help="internal: the token of the lock the detached run was started under")
    args = ap.parse_args(argv)
    root = args.repo or os.getcwd()
    if args.background_run:
        return _background_run(root, args.token or "")
    if args.post_merge:
        try:
            rep = post_merge(root, args.squash_flag)
        except Exception as exc:                                         # git ignores the hook's exit code; say what broke
            print("post-merge: sweep failed (%s: %s)" % (type(exc).__name__, first_line(str(exc))), file=sys.stderr)
            return 0
        for line in rep.lines:
            print(line)
        return 0
    if args.count:
        try:
            print(count_estimate(root, ref=args.ref or DEFAULT_REF)[1])
        except RuntimeError as exc:
            print("worktree_sweep: count unavailable (%s)" % exc, file=sys.stderr)
            return 1
        return 0
    ref = args.ref or DEFAULT_REF
    repo = None
    try:
        repo = repo_context(Git(), root)
    except Refuse:
        pass                                                             # sweep() below says it, with its own refusal text
    if args.apply and repo is not None and not repo.linked:
        return _manual_apply(repo, ref)
    if not args.apply and repo is not None:
        try:
            state = read_status(root)
        except Exception:
            state = None
        if state is not None and state.kind == "running":
            print("NOTE: a sweep is running since %s (%s) -- copies it is removing may still be listed" % (
                state.data.get("started", "unknown"), state.data.get("trigger", "unknown")))
    rep = sweep(root, ref=ref, apply=args.apply)
    for line in rep.lines:
        print(line)
    return rep.exit_code


def _manual_apply(repo, ref):
    """--apply by hand: the same lock and the same run body as the background run; the lines go to the console and the journal."""
    try:
        lock, holder = acquire_lock(state_dir(repo), "manual")
    except OSError as exc:
        print("worktree_sweep: cannot make the state directory %s (%s) -- a sweep never runs without its lock; nothing removed" % (
            state_dir(repo), first_line(str(exc))))
        return 1
    if lock is None:
        print("worktree_sweep: a sweep is already running since %s (%s, pid %s) -- wait for it (log %s), or, if it is dead, run "
              "again after %d min without a heartbeat; nothing removed" % (
                  holder.get("started", "unknown"), holder.get("trigger", "unknown"), holder.get("pid"), LOG_REL, STALE_S // 60))
        return 1
    return run_locked(repo, lock, "manual", print, ref=ref).exit_code


def _background_run(root, token):
    """The detached child: it works only while the lock file still carries the token it was started under (E14)."""
    try:
        repo = repo_context(Git(), root)
    except Refuse as exc:
        print(first_line(str(exc)), file=sys.stderr)
        return 1
    directory = state_dir(repo)
    info, _ = _read_lock(directory / "lock")
    if info is None or not token or info.get("token") != token:
        try:
            directory.mkdir(parents=True, exist_ok=True)
            with open(directory / "run.log", "a", encoding="utf-8") as f:
                f.write("background run %s: the lock is not ours -- nothing done\n" % (token[:8] or "none"))
        except OSError:
            pass
        return 0
    lock = Lock(directory / "lock", token, os.getpid(), info.get("started", _iso()), info.get("trigger", "manual"))
    lock.set_pid(os.getpid())
    return run_locked(repo, lock, lock.trigger).exit_code


if __name__ == "__main__":
    sys.exit(main())
