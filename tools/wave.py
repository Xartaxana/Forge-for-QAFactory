#!/usr/bin/env python3
"""wave.py -- the one merge road of a wave (offload spec r2, §3.C3; mechanism M6).

  python -B tools/wave.py merge <branch> --task t-NNN [--node <slug> <N> <id>] [--repo DIR]

One call: take the machine lock `main-merge` (60 s), fetch, refuse a branch unknown on origin, print the last known
`forge-check` state of the branch head (information only: it never waits, never refuses), merge `origin/<branch>` into a
temporary detached worktree W at `origin/main` (ff, else no-ff; a conflict aborts and refuses naming the paths), with
`--node` record the node through `piles.py status`, push `HEAD:main` (a non-fast-forward push is redone from the merge,
three attempts), commit the root's journal through a second temporary worktree (only when origin's journal is a byte-prefix
of the root's), refresh the root checkout when that is safe, delete the branch, print a 4-line summary.

THE ROOT: wave never stashes, resets, checks out or discards anything in the root. The merge never touches it. The refresh
is `git merge --ff-only origin/main` there, done only when the root is on `main`, its tracked changes are at most its own
journal, its HEAD is an ancestor of origin/main and origin's journal is a byte-prefix of the root's; under the journal lock
the root's journal bytes are copied aside (sha256 H), the file is put to its HEAD state (or removed when HEAD lacks it),
the merge runs, and WHATEVER its result the bytes are written back and checked against H. A mismatch keeps the copy and is
exit 1. Exit codes: 0 done, 1 done but something named must be fixed by hand (piles refusal, journal restore mismatch),
2 refused before any push."""
from __future__ import annotations

import argparse
import hashlib
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

_TOOLS = Path(__file__).resolve().parent
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))

import journal_keys as jk  # noqa: E402
import journal_lock as jl  # noqa: E402
import streams  # noqa: E402
import worktree_sweep as ws  # noqa: E402

LOCK_WAIT = 60.0                  # seconds on another wave's merge (module constant: a test moves it)
JOURNAL_WAIT = 15.0
ATTEMPTS = 3
MAIN = "main"
TASK_RE = re.compile(r"t-\d{3,9}[a-z]?")
CI_TIMEOUT = 60
_NONFF = ("non-fast-forward", "fetch first", "failed to update ref", "(stale info)")


class Refuse(Exception):
    def __init__(self, text, code=2):
        super().__init__(text)
        self.code = code


def _hook(name):          # a seam for tests: called inside the critical sections
    return None


def git(cwd, *args):
    """(rc, stdout text stripped, stderr text stripped)."""
    try:
        p = subprocess.run(["git", "-C", str(cwd), *args], capture_output=True, timeout=300, env=jl._git_env())
    except (OSError, subprocess.SubprocessError) as exc:
        return 255, "", type(exc).__name__
    return (p.returncode, p.stdout.decode("utf-8", "replace").rstrip(), p.stderr.decode("utf-8", "replace").strip())


def git_bytes(cwd, *args):
    p = subprocess.run(["git", "-C", str(cwd), *args], capture_output=True, timeout=300, env=jl._git_env())
    return p.returncode, p.stdout


def forge_check_state(root, sha):
    """`success | failure | pending | unknown` for the commit `sha`, from tools/ci_read.py; any failure is `unknown`."""
    def ci(*args):
        p = subprocess.run([sys.executable, "-B", str(_TOOLS / "ci_read.py"), *args], capture_output=True,
                           timeout=CI_TIMEOUT, cwd=str(root))
        if p.returncode != 0:
            raise OSError("ci_read exit %d" % p.returncode)
        return p.stdout.decode("utf-8", "replace").splitlines()

    def word(w):
        w = (w or "").strip()
        return ("success" if w == "success" else "failure" if w in ("failure", "timed_out", "cancelled")
                else "pending" if w in ("in_progress", "queued", "waiting", "pending", "None") else "unknown")
    try:
        for line in ci("pipelines", "--n", "30"):
            tok = line.split()
            if len(tok) >= 5 and tok[-2] == sha[:8] and tok[0].isdigit():
                state = word(tok[1])
                for job in ci("jobs", tok[0]):
                    parts = job.split()
                    if len(parts) >= 3 and "forge-check" in parts[1:-1]:
                        state = word(parts[-1])
                return state
    except Exception:  # noqa: BLE001 -- information only: whatever fails is `unknown`
        pass
    return "unknown"


def journal_rel(root):
    rel, _why = jk.current_path(root)
    return rel


def _sha(data):
    return hashlib.sha256(data or b"").hexdigest()


class Wave:
    def __init__(self, repo, branch, task, node=None, ci=forge_check_state, out=print):
        self.branch, self.task, self.node, self.ci, self.out = branch, task, node, ci, out
        self.root = jl.common_dir(repo).parent
        self.sha = None
        self.piles_text = None
        self.seq = 0
        self.pushed = False

    # ---- helpers
    def say(self, text):
        self.out(text)

    def fetch(self, step="step 2"):
        rc, _o, err = git(self.root, "fetch", "origin")
        if rc != 0:
            raise Refuse("%s: git fetch origin failed: %s" % (step, err))

    def add_worktree(self):
        self.seq += 1
        path = self.root / ".claude" / "worktrees" / ("wave-%s-%d" % (time.strftime("%Y%m%d-%H%M%S"), self.seq))
        rc, _o, err = git(self.root, "worktree", "add", "--detach", str(path), "origin/" + MAIN)
        if rc != 0:
            raise Refuse("cannot make the temporary worktree: %s" % err)
        return path

    def drop(self, path):
        git(self.root, "worktree", "remove", "--force", str(path))
        if Path(path).exists():
            shutil.rmtree(path, ignore_errors=True)
        git(self.root, "worktree", "prune")

    def push(self, w, step):
        """'ok' | 'moved' (non-fast-forward); a refusal names the text of the hook / network."""
        rc, _o, err = git(w, "push", "origin", "HEAD:" + MAIN)
        if rc == 0:
            return "ok"
        if any(m in err for m in _NONFF):
            return "moved"
        raise Refuse("%s: push refused: %s" % (step, err))

    def origin_blob(self, rel):
        rc, data = git_bytes(self.root, "show", "origin/%s:%s" % (MAIN, rel))
        return data if rc == 0 else b""

    # ---- steps
    def locked(self):
        self.fetch()
        rc, sha, _e = git(self.root, "rev-parse", "--verify", "-q", "refs/remotes/origin/" + self.branch)
        if rc != 0 or self.branch == MAIN:
            raise Refuse("step 3: branch %s is not on origin (expected an existing branch other than main)" % self.branch)
        self.say("forge-check: %s" % self.ci(self.root, sha))
        self.merge_and_push(sha)
        self.commit_journal()
        why = self.refresh()
        self.finish(why)

    def merge_and_push(self, branch_sha):
        for attempt in range(ATTEMPTS):
            if attempt:
                self.fetch("step 7")
            w = self.add_worktree()
            try:
                if git(w, "merge-base", "--is-ancestor", branch_sha, "HEAD")[0] == 0:
                    self.say("nothing to merge")
                    self.sha = branch_sha
                else:
                    self.merge(w)
                    self.sha = git(w, "rev-parse", "HEAD")[1]
                if self.node:
                    self.record_node(w)
                if git(w, "rev-parse", "HEAD")[1] == git(w, "rev-parse", "origin/" + MAIN)[1]:
                    return
                if self.push(w, "step 7") == "ok":
                    self.pushed = True
                    return
            finally:
                self.drop(w)
        raise Refuse("main moved %d times during the merge" % ATTEMPTS)

    def merge(self, w):
        target = "origin/" + self.branch
        if git(w, "merge", "--ff-only", target)[0] == 0:
            return
        rc, _o, err = git(w, "merge", "--no-ff", "-m", "wave: merge %s (%s)" % (self.branch, self.task), target)
        if rc == 0:
            return
        paths = git(w, "diff", "--name-only", "--diff-filter=U")[1].split()
        git(w, "merge", "--abort")
        if paths:
            raise Refuse("step 5: conflict in %s -- nothing was merged" % ", ".join(paths))
        raise Refuse("step 5: the merge was refused: %s" % err)

    def record_node(self, w):
        slug, n, ident = self.node
        argv = [sys.executable, "-B", str(Path(w) / "tools" / "piles.py"), "status", slug, n, ident, "--set", "принято",
                "--hash", self.sha, "--task", self.task]
        p = subprocess.run(argv, capture_output=True, cwd=str(w), timeout=120)
        if p.returncode != 0:
            text = (p.stdout + p.stderr).decode("utf-8", "replace").strip()
            self.piles_text = "%s\nrun by hand: python -B tools/piles.py status %s %s %s --set принято --hash %s --task %s" % (
                text, slug, n, ident, self.sha, self.task)
            return
        changed = [ln[3:] for ln in git(w, "status", "--porcelain")[1].splitlines()]
        if changed:
            git(w, "add", "--", *changed)
            rc, o, err = git(w, "commit", "-m", "piles: %s %s %s принято (%s)" % (slug, n, ident, self.task))
            if rc != 0:
                raise Refuse("step 6: the commit was refused: %s" % (err or o))

    def commit_journal(self):
        rel = journal_rel(self.root)
        if rel is None:
            self.say("journal not committed: this clone has no journal path")
            return
        path = self.root / rel
        try:
            with jl.machine_lock("journal", JOURNAL_WAIT, repo=self.root):
                data = path.read_bytes() if path.exists() else None
        except jl.LockBusy as exc:
            self.say("journal not committed: %s" % exc)
            return
        if data is None:
            return
        for attempt in range(ATTEMPTS):
            if attempt:
                self.fetch("step 8")
            w = self.add_worktree()
            try:
                orig = self.origin_blob(rel)
                if not data.startswith(orig):
                    self.say("journal not committed: origin holds lines the root lacks -- commit it from %s" % self.root)
                    return
                if data == orig:
                    return
                (Path(w) / rel).parent.mkdir(parents=True, exist_ok=True)
                (Path(w) / rel).write_bytes(data)
                git(w, "add", "--", rel)
                rc, o, err = git(w, "commit", "-m", "journal: wave %s (%s)" % (self.branch, self.task))
                if rc != 0:
                    self.say("journal not committed: %s" % (err or o))
                    return
                if self.push(w, "step 8") == "ok":
                    return
            except Refuse as exc:
                self.say("journal not committed: %s" % exc)
                return
            finally:
                self.drop(w)
        self.say("journal not committed: main moved %d times" % ATTEMPTS)

    def refresh(self):
        """None when the root was refreshed, else the reason it was not."""
        root = self.root
        self.fetch("step 9")
        rc, cur_branch, _e = git(root, "symbolic-ref", "-q", "--short", "HEAD")
        if rc != 0 or cur_branch != MAIN:
            return "the root is not on %s (%s)" % (MAIN, cur_branch or "detached")
        rel = journal_rel(root)
        if rel is None:
            return "this clone has no journal path"
        for line in git(root, "status", "--porcelain", "--untracked-files=no")[1].splitlines():
            if line[3:] != rel:
                return "tracked changes beyond the journal: %s" % line[3:]
            if line[0] != " ":
                return "the journal has staged changes"
        if git(root, "merge-base", "--is-ancestor", "HEAD", "origin/" + MAIN)[0] != 0:
            return "the root HEAD is not an ancestor of origin/%s" % MAIN
        path = root / rel
        orig = self.origin_blob(rel)
        cur = path.read_bytes() if path.exists() else None
        if not (cur or b"").startswith(orig) or (cur is None and orig):
            return "origin's journal is not a prefix of the root's"
        try:
            with jl.machine_lock("journal", JOURNAL_WAIT, repo=root):
                return self.swap(rel)
        except jl.LockBusy as exc:
            return "the journal lock is busy (%s)" % exc

    def swap(self, rel):
        """Under the journal lock: copy aside, journal to its HEAD state, ff merge, bytes back, verify. None = refreshed."""
        root = self.root
        path = root / rel
        cur = path.read_bytes() if path.exists() else None
        copy = jl.lock_dir(root) / ("wave-copy-" + time.strftime("%Y%m%d-%H%M%S"))
        copy.write_bytes(cur or b"")
        digest = _sha(cur)
        rc, head_bytes = git_bytes(root, "show", "HEAD:" + rel)
        if rc != 0:
            path.unlink(missing_ok=True)
        else:
            path.write_bytes(head_bytes)
        _hook("step9-locked")
        rc, o, err = git(root, "merge", "--ff-only", "origin/" + MAIN)
        if cur is None:
            path.unlink(missing_ok=True)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(cur)
        now = path.read_bytes() if path.exists() else None
        if _sha(now) != digest or (now is None) != (cur is None):
            raise Refuse("JOURNAL RESTORE MISMATCH: copy kept at %s" % copy, 1)
        copy.unlink()
        return None if rc == 0 else (err or o)

    def worktree_of(self):
        out = git(self.root, "worktree", "list", "--porcelain")[1]
        path = None
        for line in out.splitlines():
            if line.startswith("worktree "):
                path = line[9:]
            elif line == "branch refs/heads/" + self.branch:
                return path
        return None

    def delete_branch(self, refreshed):
        """(deleted?, text)."""
        root, br = self.root, self.branch
        wt = self.worktree_of()
        if wt is not None:
            same_as_root = Path(wt).resolve() == root.resolve()
            entries = [(ln[:2], ln[3:]) for ln in git(wt, "status", "--porcelain")[1].splitlines()]
            real, _traces = ws.real_changes(entries, ws.load_junk())
            if same_as_root or real:
                self.delete_remote()
                return False, "kept, checked out in %s%s" % (wt, " (dirty)" if real else "")
            git(root, "worktree", "remove", "--force", wt)
        rc, local, _e = git(root, "rev-parse", "--verify", "-q", "refs/heads/" + br)
        ok, text = True, "deleted"
        if rc == 0:
            if refreshed:
                rc, o, err = git(root, "branch", "-d", br)
                ok = rc == 0
                text = "deleted" if ok else "kept: %s" % (err or o)
            elif git(root, "merge-base", "--is-ancestor", "refs/heads/" + br, "origin/" + MAIN)[0] != 0:
                ok, text = False, "kept: not merged into origin/%s" % MAIN
            else:
                _hook("before-update-ref")
                rc, o, err = git(root, "update-ref", "-d", "refs/heads/" + br, local)
                ok = rc == 0
                text = "deleted" if ok else "kept: the branch moved (%s)" % (err or o)
        self.delete_remote()
        return ok, text

    def delete_remote(self):
        rc, _o, err = git(self.root, "push", "origin", "--delete", self.branch)
        if rc != 0:
            self.say("remote branch not deleted: %s" % err)

    def finish(self, why):
        _deleted, btext = self.delete_branch(why is None)
        self.say("merge: %s" % self.sha)
        self.say("node: %s" % (" ".join(self.node) if self.node else "none"))
        self.say("branch: %s" % btext)
        self.say("root: refreshed" if why is None else "root checkout not refreshed: %s" % why)
        if self.piles_text:
            self.say("piles status refused (the merge is pushed and stays): %s" % self.piles_text)
            raise Refuse("", 1)

    def run(self):
        try:
            with jl.machine_lock("main-merge", LOCK_WAIT, repo=self.root):
                self.locked()
            return 0
        except jl.LockBusy as exc:
            return self.refuse(Refuse("another wave holds main-merge: %s" % exc))
        except jl.LockError as exc:
            return self.refuse(Refuse("the main-merge lock cannot be taken: %s" % exc))
        except Refuse as exc:
            return self.refuse(exc)

    def refuse(self, exc):
        if str(exc):
            self.say("refused: %s" % exc)
        return exc.code


def build_parser():
    p = argparse.ArgumentParser(prog="wave.py", description="the merge road of a wave")
    sub = p.add_subparsers(dest="cmd", required=True)
    m = sub.add_parser("merge", help="merge one ready branch into main")
    m.add_argument("branch")
    m.add_argument("--task", required=True, help="t-NNN")
    m.add_argument("--node", nargs=3, metavar=("SLUG", "N", "ID"))
    m.add_argument("--repo", default=str(_TOOLS.parent))
    return p


def main(argv=None):
    streams.utf8_stdio()
    a = build_parser().parse_args(argv)
    if not TASK_RE.fullmatch(a.task):
        print("refused: --task %r: expected a task id t-NNN (3-9 digits, optional lower-case letter)" % a.task)
        return 2
    if not a.branch or a.branch.startswith("-") or git(a.repo, "check-ref-format", "--branch", a.branch)[0] != 0:
        print("refused: %r is not a branch name" % a.branch)
        return 2
    if a.node and not a.node[1].isdigit():
        print("refused: --node N must be a number, not %r" % a.node[1])
        return 2
    try:
        wave = Wave(a.repo, a.branch, a.task, a.node)
    except jl.LockError as exc:
        print("refused: %s" % exc)
        return 2
    return wave.run()


if __name__ == "__main__":
    sys.exit(main())
