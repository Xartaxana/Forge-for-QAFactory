#!/usr/bin/env python3
"""wave.py -- the one merge road of a wave (offload spec r2, §3.C3; mechanism M6).

  python -B tools/wave.py merge <branch> --task t-NNN [--node <slug> <N> <id>] [--sha <tip>] [--piles-skip "<items> -- <reason>"] [--tests-over "<reason>"] [--leftover-ok "<reason>"] [--repo DIR]

Before anything (even the fetch) the branch's own worktree, if one is checked out, is read for a real leftover (uncommitted
or untracked files that are not junk and differ from origin/main ignoring CR): found, the merge is refused (exit 2) with the
files and two doors -- commit them, or --leftover-ok "<reason>" (saved to a salvage ref; the summary line `leftover:`).

--tests-over names the Lead's reason for a branch whose added test lines exceed its product lines (test_volume.py's
classifier over `git diff --numstat origin/main...<tip>`); without it such a branch is refused before any push. With it
the merge is always --no-ff and its message carries `tests-over: <reason>`. Reason: one line, 1 to 300 characters.

--sha pins the accepted branch tip (full or a prefix of 7+ hex digits): another tip is refused before any push. The tool
prints `pushed: <sha>` (the tip it merges) before the merge.

--piles-skip puts the door line `piles-skip: <items> -- <reason>` (tools/piles.py DOOR_RE, ITEMS) into the merge commit
message, after an empty line; the fast-forward is then skipped (a fast-forward has no commit to carry the line) and the
merge is always --no-ff. The piles check still runs and reads the line itself: the door never switches it off. A
malformed value is refused with exit 2 before the lock is taken.

One call: take the machine lock `main-merge` (60 s), fetch, push the branch to origin itself when origin lacks it or is
behind it (fast-forward only, never forced; a refusal prints origin's text and nothing is merged), refuse a branch known
nowhere, print the last known
`forge-check` state of the branch head (information only: it never waits, never refuses), merge `origin/<branch>` into a
temporary detached worktree W at `origin/main` (ff, else no-ff; a conflict aborts and refuses naming the paths), with
`--node` record the node through `piles.py status`, push `HEAD:main` (a non-fast-forward push is redone from the merge,
three attempts), commit the root's journal through a second temporary worktree (only when origin's journal is a byte-prefix
of the root's), refresh the root checkout when that is safe, delete the branch, print a 4-line summary.

THE ROOT: wave never stashes, resets, checks out or discards anything in the root. The merge never touches it. The refresh
is `git merge --ff-only origin/main` there, tried whenever the root is on `main`, its journal has no staged change, its HEAD
is an ancestor of origin/main and origin's journal is a byte-prefix of the root's (foreign tracked changes do not stop the
try: git refuses on overlap and the line names its reason and up to 5 paths); under the journal lock
the root's journal bytes are copied aside (sha256 H), the file is put to its HEAD state (or removed when HEAD lacks it),
the merge runs, and WHATEVER its result the bytes are written back and checked against H. A mismatch keeps the copy and is
exit 1. Exit codes: 0 done, 1 done but something named must be fixed by hand (piles refusal, journal restore mismatch),
2 refused before any push. A step-9 failure after the push never turns into "refused": the summary is printed and a
restore mismatch is exit 1 after it."""
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
import piles  # noqa: E402
import streams  # noqa: E402
import test_volume as tv  # noqa: E402  (the ONE definition of test vs product lines)
import worktree_sweep as ws  # noqa: E402

LOCK_WAIT = 60.0                  # seconds on another wave's merge (module constant: a test moves it)
JOURNAL_WAIT = 15.0
SWEEP_WAIT = 20.0                 # seconds on a running worktree sweep before a worktree is left to it (C3-7)
SHOW_PATHS = 5
ATTEMPTS = 3
MAIN = "main"
REASON_MAX = 300                  # the longest --tests-over / --leftover-ok reason
LEFTOVER_SHOW = 20                # leftover files named in a refusal, then "+N more"
PIN_RE = re.compile(r"[0-9a-fA-F]{7,40}", re.ASCII)
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
    """`success | failure | pending | unknown` for the commit `sha` from ci_read.run_state (the one road to the CI state:
    its backend, its token door, its request function); a red state carries the names of its failed jobs:
    `failure (failed: a, b)`. No run or any failure to know is `unknown`, never a guessed reason."""
    import ci_read  # noqa: PLC0415
    state, failed = ci_read.run_state(root, sha)
    if state == "failure" and failed:
        return "failure (failed: %s)" % ", ".join(failed[:3])
    return {"success": "success", "failure": "failure", "in_progress": "pending"}.get(state, "unknown")


def journal_rel(root):
    rel, _why = jk.current_path(root)
    return rel


def _atomic_write(path, data):
    """Temp file beside it, then `os.replace`: a reader without the lock sees the old whole file or the new whole file,
    never a truncated one (Q5b)."""
    tmp = path.with_name(path.name + ".wave-tmp")
    try:
        tmp.write_bytes(data)
        jl.replace_retrying(tmp, path)       # t-1414: another process held the journal for a moment (WinError 5/32)
    except OSError:
        tmp.unlink(missing_ok=True)
        raise


def _sha(data):
    return hashlib.sha256(data or b"").hexdigest()


class Wave:
    def __init__(self, repo, branch, task, node=None, ci=forge_check_state, out=print, pin=None, piles_skip=None,
                 tests_over=None, leftover_ok=None):
        self.leftover_ok = leftover_ok    # the validated reason, or None
        self.leftover_line = "leftover: none"
        self.branch, self.task, self.node, self.ci, self.out = branch, task, node, ci, out
        self.pin = pin
        self.tests_over = tests_over      # the validated reason, or None
        self.over_line = None             # set by check_volume: the reason, whenever --tests-over is given and a merge is due
        self.volume_tip = None            # the last tip judged (memo by tip, not by flag)
        self.piles_skip = piles_skip      # the validated text after "piles-skip:", or None
        self.root = jl.common_dir(repo).parent
        self.sha = None
        self.branch_sha = None
        self.piles_text = None
        self.mismatch = None
        self.seq = 0
        self.pushed = False
        self.ff_text = None
        self.foreign = []

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
    def check_leftover(self):
        """Uncommitted files in the branch's own worktree never go silently missing from main (owner, 18.11). Before any fetch
        or push: a worktree with a REAL leftover (not junk by worktree_sweep's list, not equal to origin/main ignoring CR; an
        untracked file counts) refuses with its files and two doors -- the builder commits (a new tip, a new canon), or
        --leftover-ok "<reason>" saves the files to a salvage archive ref (worktree_sweep.salvage_leftover) and merges. The
        worktree itself is never written. Sets self.leftover_line."""
        self.leftover_line = "leftover: none"
        try:
            git_ = ws.Git()
            repo = ws.repo_context(git_, self.root)
            wt = next((w for w in ws.list_worktrees(git_, repo) if w.branch == "refs/heads/" + self.branch
                       and w.prunable is None and Path(w.path).exists()), None)     # a prunable or missing one is E2
            ctx = ws.Ctx(git_, repo, ws.DEFAULT_REF, ws.load_junk(), {}, time.time(), 0, set(), set())
            entries, diff, nested = ws.read_leftover(ctx, wt) if wt is not None else ([], [], "")
            if not diff:
                if self.leftover_ok is not None:
                    self.say("note: no leftover; --leftover-ok unused")
                return
            if nested:                                  # the sweep never saves or removes a nested repo: no door (F4)
                raise Refuse("step 1: %s holds a nested repository (%s) among its uncommitted files; the sweep never saves or "
                             "removes nested repositories, so --leftover-ok does not pass it: commit or move it away, then "
                             "merge again" % (wt.path, nested))
            if self.leftover_ok is None:
                shown = "".join("\n  %s" % p for p in diff[:LEFTOVER_SHOW])
                more = "\n  +%d more" % (len(diff) - LEFTOVER_SHOW) if len(diff) > LEFTOVER_SHOW else ""
                raise Refuse('step 1: %s holds %d uncommitted file(s) differing from origin/main as last fetched, which the merge '
                             'would leave out of main:%s%s\n'
                             '  door 1: the builder commits them (a new tip, a new canon), then merge again\n'
                             '  door 2: --leftover-ok "<reason>" saves them to a salvage archive ref, merges, and the sweep '
                             'cleans the worktree' % (wt.path, len(diff), shown, more))
            ev = ws.Eval("candidate", leftover=diff, entries=entries, cls="merged-leftover-salvage")
            ok, ref = ws.salvage_leftover(ctx, wt, ev)
            if not ok:
                raise Refuse("step 1: the leftover of %s could not be saved (%s); nothing merged, the worktree is untouched"
                             % (wt.path, ref))
            self.leftover_line = "leftover: salvaged %s (%s)" % (ref, self.leftover_ok)
        except (ws.Refuse, RuntimeError, OSError) as exc:
            raise Refuse("step 1: the worktree of %s cannot be checked for a leftover (%s); nothing merged" % (self.branch, exc))

    def locked(self):
        if self.branch != MAIN:
            self.check_leftover()
        self.fetch()
        if self.branch != MAIN:
            self.check_pin_local()
            self.check_volume_local()
            self.publish_branch()
        rc, sha, _e = git(self.root, "rev-parse", "--verify", "-q", "refs/remotes/origin/" + self.branch)
        if rc != 0 or self.branch == MAIN:
            raise Refuse("step 3: branch %s is not on origin (expected an existing branch other than main)" % self.branch)
        self.check_pin(sha)
        self.check_volume(sha)
        self.branch_sha = sha
        self.say("pushed: %s" % sha)
        self.say("forge-check: %s" % self.ci(self.root, sha))
        self.merge_and_push(sha)
        self.commit_journal()
        why = self.refresh()
        self.finish(why)

    def pin_problem(self):
        """None, or the text that refuses a malformed --sha before anything runs."""
        if self.pin is not None and not PIN_RE.fullmatch(self.pin):
            return "--sha %r: expected 7 to 40 hex digits (a full sha or a prefix of at least 7)" % self.pin
        return None

    def check_pin(self, tip):
        """The branch tip that is pushed and merged is the accepted one: a mismatch refuses before any push."""
        if self.pin is not None and not tip.lower().startswith(self.pin.lower()):
            raise Refuse("step 3: tip %s != accepted %s; expected the tip you accepted -- re-accept the new tip, "
                         "or pass the new sha with --sha" % (tip, self.pin))

    def check_pin_local(self):
        rc, tip, _e = git(self.root, "rev-parse", "--verify", "-q", "refs/heads/" + self.branch)
        if rc == 0:
            self.check_pin(tip)

    def check_volume_local(self):
        """Same check on the local tip BEFORE publish_branch pushes it: a refusal leaves origin untouched."""
        rc, tip, _e = git(self.root, "rev-parse", "--verify", "-q", "refs/heads/" + self.branch)
        if rc == 0:
            self.check_volume(tip)

    def check_volume(self, tip):
        """Test lines of the branch vs product lines (tools/test_volume.py's classifier and summer). Over the budget and
        no --tests-over: refused before any push. Cannot be computed: one line, the merge goes on."""
        if self.volume_tip == tip or self.branch == MAIN:      # a tip is judged once; the local and the origin tip may differ
            return
        self.volume_tip = tip
        root = self.root
        if git(root, "merge-base", "--is-ancestor", tip, "origin/" + MAIN)[0] == 0:
            return                                                  # nothing to merge: no check, no merge commit
        self.over_line = self.tests_over                            # the Lead's reason is written whenever a merge commit is made
        # quotepath off: a non-ASCII path stays a path (octal-quoted it would read as excluded; tools/gitcmd.py does the same)
        rc, text, err = git(root, "-c", "core.quotepath=false", "diff", "--numstat", "-M", "origin/%s...%s" % (MAIN, tip))
        if rc != 0:
            self.say("test volume: not checked (git diff --numstat failed: %s)" % (err[:200] or "no message"))
            return

        def has_tests(path):
            r, blob_text, _e = git(root, "show", "%s:%s" % (tip, path))
            return r == 0 and tv.TEST_DEF_RE.search(blob_text) is not None
        try:
            t, p = tv.sum_numstat(text, has_tests)
        except Exception as exc:
            self.say("test volume: not checked (%s: %s)" % (type(exc).__name__, exc))
            return
        if t <= p:
            return
        if self.tests_over is None:
            raise Refuse(
                "TEST VOLUME: the branch adds +%d test lines vs +%d product lines (docs/TESTING.md, budget / volume). "
                'Way on: the builder cuts rows to the budget, weakest first, and reports them as "tests not written: '
                '<row> -- over budget"; or the Lead names the reason: --tests-over "<reason>" (written into the merge '
                "commit)." % (t, p))

    def publish_branch(self):
        """Step 3a: the accepted branch reaches origin by this road. Nothing local -> step 3 judges; origin equal to or
        ahead of the local branch -> nothing to push (silent); else a plain fast-forward push, never forced."""
        root, br = self.root, self.branch
        lrc, local, _e = git(root, "rev-parse", "--verify", "-q", "refs/heads/" + br)
        if lrc != 0:
            return
        rrc, remote, _e = git(root, "rev-parse", "--verify", "-q", "refs/remotes/origin/" + br)
        if rrc == 0 and (remote == local or git(root, "merge-base", "--is-ancestor", local, remote)[0] == 0):
            return
        rc, _o, err = git(root, "push", "origin", "refs/heads/%s:refs/heads/%s" % (br, br))
        if rc != 0:
            kind = "non-fast-forward, not forced" if any(m in err for m in _NONFF) else "refused"
            raise Refuse("step 3: push of %s to origin %s: %s" % (br, kind, err))
        self.say("branch %s pushed to origin" % br)

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
        if self.piles_skip is None and self.over_line is None and git(w, "merge", "--ff-only", target)[0] == 0:
            return
        msg = "wave: merge %s (%s)" % (self.branch, self.task)
        lines = []
        if self.piles_skip is not None:
            lines.append("piles-skip: " + self.piles_skip)
        if self.over_line is not None:
            lines.append("tests-over: " + self.over_line)
        if lines:
            msg += "\n\n" + "\n".join(lines)
        rc, _o, err = git(w, "merge", "--no-ff", "-m", msg, target)
        if rc == 0:
            return
        paths = git(w, "diff", "--name-only", "--diff-filter=U")[1].split()
        git(w, "merge", "--abort")
        if paths:
            raise Refuse("step 5: conflict in %s -- nothing was merged" % ", ".join(paths))
        raise Refuse("step 5: the merge was refused: %s" % err)

    def record_node(self, w):
        slug, n, ident = self.node
        self.piles_text = None                      # one attempt's refusal never outlives the attempt (C3-5)
        argv = [sys.executable, "-B", str(Path(w) / "tools" / "piles.py"), "status", slug, n, ident, "--set", "принято",
                "--hash", self.sha, "--task", self.task]
        p = subprocess.run(argv, capture_output=True, cwd=str(w), timeout=120)
        if p.returncode != 0:
            text = (p.stdout + p.stderr).decode("utf-8", "replace").strip()
            self.piles_text = self.by_hand(text)
            return
        changed = [ln[3:] for ln in git(w, "status", "--porcelain")[1].splitlines()]
        if changed:
            git(w, "add", "--", *changed)
            rc, o, err = git(w, "commit", "-m", "piles: %s %s %s принято (%s)" % (slug, n, ident, self.task))
            if rc != 0:
                self.piles_text = self.by_hand("the status commit was refused: %s" % (err or o))

    def by_hand(self, text):
        slug, n, ident = self.node
        return ("%s\nrun by hand, from %s: python -B tools/piles.py status %s %s %s --set принято --hash %s --task %s"
                " -- then commit and push the batch file" % (text, self.root, slug, n, ident, self.sha, self.task))

    def main_tree(self):
        """The clone's MAIN working tree: the first entry of `git worktree list` (the root when git cannot say)."""
        for line in git(self.root, "worktree", "list", "--porcelain")[1].splitlines():
            if line.startswith("worktree "):
                return Path(line[9:])
        return self.root

    def place_dev_config(self, w):
        """The validator reads tools/dev.config.yaml of the tree it runs in; the file is untracked and lives in the main
        tree only. The smallest legal move: a copy into the temporary worktree, gone with it. True = a copy was placed."""
        src = self.main_tree() / jk.DEV_CONFIG_REL
        if not src.is_file():
            return False
        dst = Path(w) / jk.DEV_CONFIG_REL
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dst)
        return True

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
                placed = self.place_dev_config(w)
                git(w, "add", "--", rel)
                rc, o, err = git(w, "commit", "-m", "journal: wave %s (%s)" % (self.branch, self.task))
                if rc != 0:
                    text = err or o
                    if not placed and jk.DEV_CONFIG_REL in text:
                        text = "developer slug unknown (%s)" % jk.DEV_CONFIG_REL
                    self.say("journal not committed: %s" % text)
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
        try:
            self.fetch("step 9")
        except Refuse:
            return "git fetch origin failed"       # after the push: never "refused" (C3-1)
        rc, cur_branch, _e = git(root, "symbolic-ref", "-q", "--short", "HEAD")
        if rc != 0 or cur_branch != MAIN:
            return "the root is not on %s (%s)" % (MAIN, cur_branch or "detached")
        rel = journal_rel(root)
        if rel is None:
            return "this clone has no journal path"
        self.foreign = []
        for line in git(root, "status", "--porcelain", "--untracked-files=no")[1].splitlines():
            if line[3:] != rel:
                self.foreign.append(line[3:])        # foreign changes never stop the ff attempt; git judges overlap
            elif line[0] != " ":
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
        """Under the journal lock: copy aside, journal to its HEAD state, ff merge, bytes back, verify. None = refreshed.
        A line an unlocked writer appended inside the window rides on top of the copy (copy kept, named); anything else
        found in the file keeps the copy and is the mismatch; an OSError names the copy (Q5)."""
        root = self.root
        path = root / rel
        cur = path.read_bytes() if path.exists() else None
        copy = jl.lock_dir(root) / ("wave-copy-" + time.strftime("%Y%m%d-%H%M%S"))
        copy.write_bytes(cur or b"")
        try:
            rc, head_bytes = git_bytes(root, "show", "HEAD:" + rel)
            head_bytes = head_bytes if rc == 0 else None
            if head_bytes is None:
                path.unlink(missing_ok=True)
            else:
                _atomic_write(path, head_bytes)
            _hook("step9-locked")
            rc, o, err = git(root, "merge", "--ff-only", "origin/" + MAIN)
            left = path.read_bytes() if path.exists() else None
            expected = head_bytes
            if rc == 0:
                orc, ob = git_bytes(root, "show", "origin/%s:%s" % (MAIN, rel))
                expected = ob if orc == 0 else None
            target, kept = cur, False
            if left != expected:
                if left is not None and expected is not None and left.startswith(expected):
                    target, kept = (cur or b"") + left[len(expected):], True
                else:
                    self.mismatch = "JOURNAL RESTORE MISMATCH: the journal changed inside the window; copy kept at %s" % copy
                    return "journal restore mismatch"
            if target is None:
                path.unlink(missing_ok=True)
            else:
                path.parent.mkdir(parents=True, exist_ok=True)
                _atomic_write(path, target)
            now = path.read_bytes() if path.exists() else None
            if _sha(now) != _sha(target) or (now is None) != (target is None):
                self.mismatch = "JOURNAL RESTORE MISMATCH: copy kept at %s" % copy
                return "journal restore mismatch"
        except OSError as exc:
            self.mismatch = "JOURNAL RESTORE FAILED (%s): copy kept at %s" % (exc, copy)
            self.mismatch += self._recovery_clause(rel, copy)
            return "journal restore failed"
        if kept:
            self.say("a line written during the window was appended to the journal; the copy is kept at %s" % copy)
        else:
            copy.unlink()
        if rc == 0:
            return None
        self.ff_text = err or o
        return self.ff_text

    def _recovery_clause(self, rel, copy):
        """E6: the kept copy equals origin/main's journal -> name the manual recovery; any failure -> no clause."""
        try:
            rc, ob = git_bytes(self.root, "show", "origin/%s:%s" % (MAIN, rel))
            if rc == 0 and copy.read_bytes() == ob:
                return "; the copy equals origin/%s: stage %s and fast-forward the root by hand" % (MAIN, rel)
        except Exception:
            pass
        return ""

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
            if real:                                  # a dirty tree is a live worker: keep the remote too (Q4)
                self.say("remote kept: %s is dirty" % wt)
                return False, "kept, checked out in %s (dirty)" % wt
            if same_as_root:
                self.delete_remote()
                return False, "kept, checked out in %s" % wt
            if not self.remove_worktree(wt):
                self.delete_remote()
                return False, "kept, checked out in %s (the worktree is not removed)" % wt
        rc, local, _e = git(root, "rev-parse", "--verify", "-q", "refs/heads/" + br)
        ok, text = True, "deleted"
        if rc == 0:
            _hook("before-branch-delete")
            if refreshed:
                rc, o, err = git(root, "branch", "-d", br)
                ok = rc == 0
                text = "deleted" if ok else "kept: %s" % (err or o)
                if not ok and git(root, "rev-parse", "--verify", "-q", "refs/heads/" + br)[0] != 0:
                    ok, text = True, "deleted (by the post-merge sweep that the root refresh started)"   # C3-7
            elif git(root, "merge-base", "--is-ancestor", "refs/heads/" + br, "origin/" + MAIN)[0] != 0:
                ok, text = False, "kept: not merged into origin/%s" % MAIN
            else:
                _hook("before-update-ref")
                rc, o, err = git(root, "update-ref", "-d", "refs/heads/" + br, local)
                ok = rc == 0
                text = "deleted" if ok else "kept: the branch moved (%s)" % (err or o)
        self.delete_remote()
        return ok, text

    def remove_worktree(self, wt):
        """Under the SAME lock the background worktree sweep takes (one lock, not two): remove the folder; a folder that is
        already gone is a report line, not an error. False = the worktree stays (the lock stayed busy for SWEEP_WAIT and it
        is left to the sweep, or git could not remove it): the caller never deletes its branch then."""
        sweep_dir = jl.common_dir(self.root) / ws.STATE_DIRNAME
        deadline = time.monotonic() + SWEEP_WAIT
        while True:
            try:
                lock, holder = ws.acquire_lock(sweep_dir, "wave-merge")
            except OSError as exc:
                self.say("worktree %s kept: the sweep lock cannot be taken (%s)" % (wt, exc))
                return False
            if lock is not None:
                break
            if time.monotonic() >= deadline:
                self.say("worktree %s kept: a worktree sweep holds its lock since %s; the sweep removes it"
                         % (wt, (holder or {}).get("started", "unknown")))
                return False
            time.sleep(0.1)
        try:
            _hook("before-worktree-remove")
            gone = not Path(wt).exists()
            if not gone:
                rc, o, err = git(self.root, "worktree", "remove", "--force", wt)
                if rc != 0 and Path(wt).exists():          # git could not remove it: the branch stays checked out there
                    self.say("worktree %s kept: git worktree remove failed: %s" % (wt, err or o or "no text"))
                    return False
                gone = rc != 0
            if gone:
                git(self.root, "worktree", "prune")
                self.say("worktree %s: folder already gone (removed by the sweep); registration pruned" % wt)
        finally:
            lock.release()
        return True

    def delete_remote(self):
        _hook("before-delete-remote")
        lease = "--force-with-lease=refs/heads/%s:%s" % (self.branch, self.branch_sha)
        rc, _o, err = git(self.root, "push", lease, "origin", "--delete", self.branch)
        if rc != 0:
            if "stale info" in err or "rejected" in err:
                self.say("remote branch kept: it moved")
            elif re.search(r"\b403\b", err):
                # the cloud git proxy answers a remote delete with HTTP 403 (trial t-1281): say what to do, not the raw stderr
                self.say("remote branch kept: the host refused the delete (HTTP 403, e.g. the cloud git proxy); "
                         "delete %s locally with git push origin --delete %s, or in the GitHub UI" % (self.branch, self.branch))
            else:
                first = next((ln.strip() for ln in err.splitlines() if ln.strip()), "no message")
                self.say("remote branch not deleted: %s" % first[:120])

    def root_line(self, why):
        if why is None:
            return "root: refreshed to %s" % git(self.root, "rev-parse", "HEAD")[1]
        if self.ff_text is None or why != self.ff_text:
            return "root checkout not refreshed: %s" % why
        lines = [ln.strip() for ln in self.ff_text.splitlines() if ln.strip()]
        paths = list(self.foreign)
        paths += [ln.strip() for ln in self.ff_text.splitlines() if ln.startswith(("\t", "    ")) and ln.strip()]
        paths = list(dict.fromkeys(paths))[:SHOW_PATHS]
        return "root not refreshed: %s; paths: %s" % (lines[0] if lines else "git refused", ", ".join(paths) or "(none named)")

    def finish(self, why):
        _deleted, btext = self.delete_branch(why is None)
        self.say("merge: %s" % self.sha)
        self.say("node: %s" % (" ".join(self.node) if self.node else "none"))
        self.say("branch: %s" % btext)
        if self.over_line is not None:
            self.say("tests-over: %s" % self.over_line)
        self.say(self.leftover_line)
        self.say(self.root_line(why))
        if self.piles_text:
            self.say("piles status not recorded (the merge is pushed without the status commit): %s" % self.piles_text)
        if self.mismatch:
            self.say(self.mismatch)
        if self.piles_text or self.mismatch:
            raise Refuse("", 1)

    def run(self):
        bad = self.pin_problem()
        if bad:
            return self.refuse(Refuse(bad))
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
    m.add_argument("--sha", default=None, metavar="SHA",
                   help="the accepted branch tip (full or a prefix of 7+ hex digits); a different tip is refused before any push")
    m.add_argument("--piles-skip", default=None, metavar="TEXT",
                   help='the door for the commit-time piles check: "<items> -- <reason>" becomes the line '
                        '"piles-skip: <items> -- <reason>" in the merge commit message (the merge is then always --no-ff; '
                        'items: %s)' % piles.ITEMS_HELP)
    m.add_argument("--tests-over", default=None, metavar="REASON",
                   help='the Lead\'s reason for a branch with more test lines than product lines (one line, up to '
                        '%d characters); written as "tests-over: <reason>" in the merge commit (always --no-ff)' % REASON_MAX)
    m.add_argument("--leftover-ok", default=None, metavar="REASON",
                   help='the door for uncommitted files in the branch\'s worktree: they are saved to a salvage archive ref, '
                        'then the merge goes on (one line, up to %d characters)' % REASON_MAX)
    m.add_argument("--repo", default=str(_TOOLS.parent))
    return p


def door_problem(text):
    """None when `text` makes a well-formed door line by piles' own reader, else what was expected."""
    line = "piles-skip: " + text
    m = None if ("\n" in text or "\r" in text) else piles.DOOR_RE.match(line)
    if m:
        known = {w for pair in piles.ITEMS for w in pair}
        names = [x.strip().lower() for x in m.group("items").split(",")]
        if names and all(n in known for n in names):
            return None
    return '--piles-skip %r: expected "<item>[, <item>] -- <reason>" on one line (items: %s); %s' % (
        text, piles.ITEMS_HELP, piles.DOOR_HELP)


def _one_line_reason(flag, value):
    """The stripped reason, or None after printing the refusal: one non-empty line of at most REASON_MAX characters."""
    text = value.strip()
    if not text or "\n" in text or "\r" in text or len(text) > REASON_MAX:
        print("refused: %s %r: expected one non-empty line of at most %d characters" % (flag, text[:60], REASON_MAX))
        return None
    return text


def main(argv=None):
    streams.utf8_stdio()
    a = build_parser().parse_args(argv)
    if jk.parse_id(a.task) is None:
        print("refused: --task %r: expected a task id t-NNN (3-9 digits, optional clone letters aa..zz)" % a.task)
        return 2
    if not a.branch or a.branch.startswith("-") or git(a.repo, "check-ref-format", "--branch", a.branch)[0] != 0:
        print("refused: %r is not a branch name" % a.branch)
        return 2
    if a.node and not jk.NODE_RE.match("/".join(a.node)):
        print("refused: --node %s: expected <slug> <N> <id> in the node grammar (slug/N/id, N from 1)" % " ".join(a.node))
        return 2
    skip = None
    if a.piles_skip is not None:
        skip = a.piles_skip.strip()
        bad = door_problem(skip)
        if bad:
            print("refused: " + bad)
            return 2
    over, left = a.tests_over, a.leftover_ok
    for flag, value in (("--tests-over", over), ("--leftover-ok", left)):
        if value is not None and _one_line_reason(flag, value) is None:
            return 2
    over = over.strip() if over is not None else None
    left = left.strip() if left is not None else None
    try:
        wave = Wave(a.repo, a.branch, a.task, a.node, pin=a.sha, piles_skip=skip, tests_over=over, leftover_ok=left)
    except jl.LockError as exc:
        print("refused: %s" % exc)
        return 2
    return wave.run()


if __name__ == "__main__":
    sys.exit(main())
