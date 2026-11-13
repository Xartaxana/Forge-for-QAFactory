"""Tests for tools/worktree_sweep.py (F6-38). Real git on temporary repositories: a bare origin, a clone, `git worktree add`.
The environment has no GIT_* variables (a hook may set them); `now`, T and `spawn` are injected (no sleep, except the end-to-end
poll W19); the git runner is replaced where a failure cannot be produced for real (E7, E36, E37, E39). t-1738 (FG7-4): the tests
of the full background sweep are W1-W26 in the second half of this file (the spec's numbering)."""
from __future__ import annotations

import ast
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import time

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import gitcmd  # noqa: E402
import mechanism_gate as mg  # noqa: E402
import worktree_sweep as ws  # noqa: E402

TOOLS = pathlib.Path(__file__).resolve().parent
T = ws.T_SECONDS
OLD = lambda: time.time() + 2 * T          # noqa: E731  -- "now" a day and more after every copy was made
NEG_CONTROL = os.environ.get("WS_NEG_CONTROL") == "1"
NEG_LOCK = os.environ.get("WS_NEG_LOCK") == "1"     # K4: a proof run in which `_lock_stale` never says "stale" -- W2 must go red

HOOK = """#!/bin/sh
# F6-38/t-1738: after a merge INTO main in the main checkout, start the FULL worktree sweep in the background (tools/worktree_sweep.py).
# Never fails the merge (git ignores this hook's exit code). In a linked worktree it exits before python: the tool there is the branch's copy.
gd=$(git rev-parse --git-dir 2>/dev/null) || exit 0
common=$(git rev-parse --git-common-dir 2>/dev/null) || exit 0
[ -n "$gd" ] && [ "$gd" = "$common" ] || exit 0
[ -f tools/worktree_sweep.py ] || { echo "post-merge: tools/worktree_sweep.py not found; nothing swept" >&2; exit 0; }
python tools/worktree_sweep.py --post-merge --squash-flag "$1" || true
"""


def _clean_env():
    return {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}


PIN = {"GIT_AUTHOR_DATE": "2026-01-01T12:00:00 +0000", "GIT_COMMITTER_DATE": "2026-01-01T12:00:00 +0000"}
PIN_DATES = os.environ.get("WS_PIN_DATES") == "1"      # a proof run: every git() call of this file runs on the "same second" clock


def git(cwd, *args, check=True, env=None):
    """`env`: extra variables for this one call (the dates of one commit); WS_PIN_DATES=1 pins every call (the fast-CI clock).
    Two commits with the same tree, parent, message, identity and the same second are ONE commit (the same sha): CI image git
    makes them within one second, this machine's git does not -- Repo.twin() below exists for that."""
    e = _clean_env()
    if PIN_DATES:
        e.update(PIN)
    e.update(env or {})
    p = subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t", "-c", "core.autocrlf=false", "-C", str(cwd), *args],
                       capture_output=True, text=True, env=e)
    if check and p.returncode != 0:
        raise AssertionError("git %s failed: %s %s" % (" ".join(args), p.stdout, p.stderr))
    return p.stdout.strip()


def build_template(tmp):
    """origin (bare) + a clone with one commit on main, pushed; copied per test (git on this machine is slow: ~0.5 s a call)."""
    origin = tmp / "origin.git"
    subprocess.run(["git", "init", "--bare", "-b", "main", str(origin)], check=True, capture_output=True, env=_clean_env())
    main = tmp / "main"
    subprocess.run(["git", "clone", str(origin), str(main)], check=True, capture_output=True, env=_clean_env())
    for k, v in (("user.name", "t"), ("user.email", "t@t"), ("core.autocrlf", "false")):
        git(main, "config", k, v)
    (main / "logs" / ".search-ledger").mkdir(parents=True)
    (main / "logs" / ".search-ledger" / "keep.txt").write_text("tracked\n")
    (main / "base.txt").write_text("1\n2\n3\n")
    git(main, "add", "-A")
    git(main, "commit", "-m", "base")
    git(main, "push", "-u", "origin", "main")


class Repo:
    def __init__(self, tmp, template):
        self.tmp = tmp
        shutil.copytree(template / "origin.git", tmp / "origin.git")
        self.main = tmp / "main"
        shutil.copytree(template / "main", self.main)
        git(self.main, "remote", "set-url", "origin", str(tmp / "origin.git"))
        (tmp / "nohooks").mkdir()
        git(self.main, "config", "core.hooksPath", str(tmp / "nohooks"))
        self.wts = tmp / "wts"
        self.wts.mkdir()

    def add_wt(self, name, branch=None, base="main", detach=False, existing=False):
        path = self.wts / name
        branch = branch or name
        if detach:
            git(self.main, "worktree", "add", "--detach", str(path), base)
        elif existing:
            git(self.main, "worktree", "add", str(path), branch)
        else:
            git(self.main, "worktree", "add", "-b", branch, str(path), base)
        return path

    def commit(self, path, name, text, msg="c", env=None):
        (pathlib.Path(path) / name).write_text(text)
        git(path, "add", "-A")
        git(path, "commit", "-m", msg, env=env)
        return git(path, "rev-parse", "HEAD")

    def twin(self, sha, env=None):
        """The same patch under ANOTHER sha, committed in main (what `git cherry` calls patch-equal). A plain cherry-pick is the
        SAME commit when the clock second, tree, parent, message and identity coincide (a fast git); `-x` adds the line
        "(cherry picked from commit <sha>)" to the message, so the sha differs by content on every clock, and the patch-id and
        the reflog subject (`cherry-pick: ...`) stay what they were."""
        git(self.main, "cherry-pick", "-x", sha, env=env)
        twin = git(self.main, "rev-parse", "HEAD")
        assert twin != sha, "the cherry-pick collided with its original: the scenario would test 'ancestor', not 'patch-equal'"
        return twin

    def merge(self, *branches, squash=False):
        if squash:
            git(self.main, "merge", "--squash", *branches)
            git(self.main, "commit", "-m", "squash")
        else:
            git(self.main, "merge", "--no-ff", "-m", "merge", *branches)
        git(self.main, "push", "origin", "main")

    def advance_main(self, name="adv.txt", text="a\n"):
        self.commit(self.main, name, text, "advance")
        git(self.main, "push", "origin", "main")

    def merged_wt(self, name, **kw):
        """A worktree with one own commit, merged into main and pushed."""
        path = self.add_wt(name, **kw)
        self.commit(path, name + ".txt", name + "\n")
        self.merge(kw.get("branch") or name)
        return path

    def admin(self, path):
        return ws.admin_dirs(self.main / ".git")[ws._key(path)]

    def sweep(self, root=None, **kw):
        kw.setdefault("junk", ws.load_junk())
        kw.setdefault("now", OLD())
        return ws.sweep(root or self.main, **kw)

    def branches(self):
        return git(self.main, "branch", "--format=%(refname:short)").split()


@pytest.fixture(autouse=True)
def _env(monkeypatch):
    for k in [k for k in os.environ if k.startswith("GIT_")]:
        monkeypatch.delenv(k)
    monkeypatch.setattr(ws, "STATUS_RETRY_S", 0)           # a status write that meets a reader is retried without waiting
    if NEG_CONTROL:
        monkeypatch.setattr(ws, "real_changes", lambda entries, junk: ([], [p for _, p in entries]))
    if NEG_LOCK:
        monkeypatch.setattr(ws, "_lock_stale", lambda info, mtime, now: False)


@pytest.fixture(scope="session")
def template(tmp_path_factory):
    tpl = tmp_path_factory.mktemp("template")
    build_template(tpl)
    return tpl


@pytest.fixture
def repo(tmp_path, template):
    return Repo(tmp_path, template)


def line(rep, start):
    hits = [l for l in rep.lines if l.startswith(start)]
    assert hits, "no line starting %r in %s" % (start, rep.lines)
    return hits[0]


def has(rep, start):
    return any(l.startswith(start) for l in rep.lines)


# ------------------------------------------------------------------------------ the happy paths

def test_merged_clean_dry_run_changes_nothing_then_apply_removes_all(repo):
    wt = repo.merged_wt("a")
    scratch = pathlib.Path(str(wt) + "-scratch")
    scratch.mkdir()
    (scratch / "draft.txt").write_text("x")
    head = git(wt, "rev-parse", "HEAD")
    rep = repo.sweep()
    assert rep.exit_code == 0
    assert line(rep, "CAN REMOVE").endswith("(branch a, merged: ancestor, own commits: yes, junk: 0 files)")
    assert "SCRATCH" in "\n".join(rep.lines) and wt.exists() and scratch.exists() and "a" in repo.branches()
    assert rep.lines[-1] == "worktree_sweep: 1 registered, 1 can go, 0 kept, 0 failed"
    rep = repo.sweep(apply=True)
    assert rep.exit_code == 0 and line(rep, "REMOVED").endswith("archive: refs/worktree-sweep/a/%s)" % head[:12])
    assert not wt.exists() and not scratch.exists() and "a" not in repo.branches()
    assert git(repo.main, "rev-parse", "refs/worktree-sweep/a/" + head[:12]) == head
    assert rep.lines[-1] == "worktree_sweep: 1 registered, 1 removed, 0 kept, 0 failed"
    assert has(rep, "judged against origin/main at ")


def test_merged_junk_only_traces_are_removed_by_the_tool_and_remove_runs_without_force(repo):
    wt = repo.merged_wt("j")
    for rel in (".claude/dod_track/x.json", "logs/.search-ledger/y.log", "bash.exe.stackdump", "deep/critic_snapshot.json"):
        p = wt / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("trace")
    calls = []

    def runner(root, *args, timeout=120, stderr=False):
        calls.append(args)
        return gitcmd.git(root, *args, timeout=timeout, stderr=stderr)

    rep = repo.sweep(apply=True, runner=runner)
    assert line(rep, "REMOVED").count("junk: 4 files") == 1 and not wt.exists()
    removes = [a for a in calls if a[:2] == ("worktree", "remove")]
    assert len(removes) == 1 and "--force" not in removes[0] and "-f" not in removes[0]
    assert (repo.main / "logs" / ".search-ledger" / "keep.txt").exists()


def test_merged_real_change_is_kept_with_the_path_and_the_door(repo):
    wt = repo.merged_wt("r")
    (wt / "notes.txt").write_text("work")
    (wt / "bash.exe.stackdump").write_text("trace")
    rep = repo.sweep(apply=True)
    k = line(rep, "KEEP")
    assert k.startswith('KEEP "%s": real changes: notes.txt -- to let it go: save them' % ws.parse_worktrees(
        gitcmd.git(repo.main, "worktree", "list", "--porcelain", "-z")[1])[1].path)
    assert 'git -C "' in k and "git worktree remove --force" in k and "bash.exe.stackdump" not in k.split(" -- ")[0]
    assert wt.exists() and "r" in repo.branches() and rep.lines[-1].startswith("worktree_sweep: 1 registered, 0 removed, 1 kept")


def test_k7_negative_control_the_real_change_predicate_is_what_keeps_the_copy(repo, monkeypatch):
    wt = repo.merged_wt("n")
    (wt / "notes.txt").write_text("work")
    assert has(repo.sweep(), "KEEP")
    monkeypatch.setattr(ws, "real_changes", lambda entries, junk: ([], []))
    assert has(repo.sweep(), "CAN REMOVE") and not has(repo.sweep(), "KEEP")


def test_tracked_change_under_a_junk_directory_is_a_real_change(repo):
    wt = repo.merged_wt("t")
    (wt / "logs" / ".search-ledger" / "keep.txt").write_text("edited\n")
    k = line(repo.sweep(), "KEEP")
    assert "real changes: logs/.search-ledger/keep.txt" in k


@pytest.mark.parametrize("count,tail", [(5, ""), (6, " (+1 more)")])
def test_real_change_paths_are_cut_at_five_with_a_count(repo, count, tail):
    wt = repo.merged_wt("p")
    names = ["f%d.txt" % i for i in range(count)]
    for n in names:
        (wt / n).write_text("x")
    k = line(repo.sweep(), "KEEP").split(": real changes: ")[1].split(" -- ")[0]
    assert k == ", ".join(names[:5]) + tail


def test_unmerged_is_kept(repo):
    wt = repo.add_wt("u")
    repo.commit(wt, "u.txt", "u")
    rep = repo.sweep(apply=True)
    assert line(rep, "KEEP").endswith(": unmerged (1 commits not in origin/main)") and wt.exists() and "u" in repo.branches()


# ------------------------------------------------------------------------------ the live-agent rule

def test_fresh_zero_commit_young_is_kept_and_old_is_a_candidate(repo):
    wt = repo.add_wt("f")
    young = repo.sweep(now=time.time())
    assert line(young, "KEEP").endswith(": no own commits, active 0h ago (< 24h)") and not has(young, "CAN REMOVE")
    old = repo.sweep(now=OLD())
    assert line(old, "CAN REMOVE").endswith("merged: ancestor, own commits: no, junk: 0 files)") and wt.exists()


@pytest.mark.parametrize("how", ["ff", "reset"])
def test_a_moved_branch_is_not_authorship_young_copy_stays(repo, how):
    wt = repo.add_wt("m")
    repo.advance_main()
    git(wt, "merge", "--ff-only", "origin/main") if how == "ff" else git(wt, "reset", "--hard", "origin/main")
    assert git(wt, "rev-parse", "HEAD") == git(repo.main, "rev-parse", "origin/main")
    rep = repo.sweep(now=time.time())
    assert line(rep, "KEEP").endswith("no own commits, active 0h ago (< 24h)")
    assert has(repo.sweep(now=OLD()), "CAN REMOVE")


def test_existing_branch_young_the_branchs_reflog_is_not_the_copys(repo):
    first = repo.add_wt("e")
    repo.commit(first, "e.txt", "e")
    repo.merge("e")
    git(repo.main, "worktree", "remove", str(first))
    wt = repo.add_wt("e2", branch="e", existing=True)
    assert "commit" in (repo.main / ".git" / "logs" / "refs" / "heads" / "e").read_text()      # the branch has authorship ...
    assert line(repo.sweep(now=time.time()), "KEEP").endswith("no own commits, active 0h ago (< 24h)")   # ... the copy has none
    assert wt.exists()


@pytest.mark.parametrize("damage,why", [("truncated", "cut"), ("empty", "empty"), ("absent", "cannot read"), ("garbage", "line 1 does not parse")])
def test_reflog_that_cannot_be_read_is_alive_when_young_and_a_candidate_when_old(repo, damage, why):
    wt = repo.merged_wt("g")                                               # own commit, merged -- would be removable at once
    log = repo.admin(wt) / "logs" / "HEAD"
    text = log.read_text()
    if damage == "truncated":
        log.write_text("\n".join(text.split("\n")[1:]))
    elif damage == "empty":
        log.write_text("")
    elif damage == "absent":
        log.unlink()
    else:
        log.write_text("not a reflog line\n")
    young = repo.sweep(now=time.time())
    assert "unknown (worktree reflog: %s" % why in line(young, "KEEP") and not has(young, "CAN REMOVE")
    assert has(repo.sweep(now=OLD()), "CAN REMOVE")


X0 = 1_700_000_000


def freeze_at(repo, wt, x=X0):
    """Every timestamp the live-agent rule reads is set to x: the creation line of the copy's reflog, the mtimes of its admin
    files, and the files of the junk directories the checkout wrote (a tracked file there carries the checkout time)."""
    adm = repo.admin(wt)
    log = adm / "logs" / "HEAD"
    first, _, rest = log.read_text().partition("\n")
    log.write_text(re.sub(r" \d+ ([+-]\d{4})", " %d \\1" % x, first, count=1) + "\n" + rest)
    for p in [adm / "HEAD", adm / "index", log, wt / "logs" / ".search-ledger", wt / "logs" / ".search-ledger" / "keep.txt"]:
        os.utime(p, (x, x))
    assert ws.read_activity(adm, wt, ws.load_junk(), ws.read_reflog(adm)[0])[0] == x          # the control: the rule sees exactly x


def test_threshold_is_strict_at_T_alive_at_T_plus_one_second_a_candidate(repo):
    wt = repo.add_wt("b")
    freeze_at(repo, wt)
    at = repo.sweep(now=X0 + T)
    assert line(at, "KEEP").endswith("no own commits, active 24h ago (< 24h)") and not has(at, "CAN REMOVE")
    assert has(repo.sweep(now=X0 + T - 1), "KEEP")
    over = repo.sweep(now=X0 + T + 1)
    assert has(over, "CAN REMOVE"), over.lines


def test_service_traces_count_as_activity(repo):
    wt = repo.add_wt("s")
    freeze_at(repo, wt)
    p = wt / ".claude" / "dod_track" / "t.json"
    p.parent.mkdir(parents=True)
    p.write_text("x")
    for q in (p, p.parent, p.parent.parent):
        os.utime(q, (X0 + T, X0 + T))                                     # a hook wrote a trace T seconds later
    assert has(repo.sweep(now=X0 + T + 5), "KEEP")                        # the copy was active only 5 s ago
    assert has(repo.sweep(now=X0 + 2 * T + 1), "CAN REMOVE")


@pytest.mark.parametrize("subject,own", [
    ("commit: x", True), ("commit (amend): x", True), ("commit (merge): x", True), ("commit (initial): x", True),
    ("cherry-pick: x", True), ("revert: x", True),
    ("merge origin/main: Fast-forward", False), ("reset: moving to origin/main", False), ("checkout: moving from a to b", False),
    ("rebase (finish): returning to refs/heads/a", False), ("pull: Fast-forward", False)])
def test_own_commit_subjects(tmp_path, subject, own):
    z, a, b = "0" * 40, "a" * 40, "b" * 40
    (tmp_path / "logs").mkdir()
    (tmp_path / "logs" / "HEAD").write_text("%s %s t <t@t> 1700000000 +0000\n%s %s t <t@t> 1700000100 +0000\t%s\n" % (z, a, a, b, subject))
    created, got, why = ws.read_reflog(tmp_path)
    assert (created, got, why) == (1700000000, own, "")


# ------------------------------------------------------------------------------ locked, prunable, scratch, detached, paths

def test_locked_is_kept_with_its_reason(repo):
    wt = repo.merged_wt("l")
    git(repo.main, "worktree", "lock", "--reason", "agent running", str(wt))
    rep = repo.sweep(apply=True)
    assert line(rep, "KEEP").endswith(": locked (agent running)") and wt.exists()


def test_scratch_goes_with_its_copy_and_stays_with_a_kept_one_and_orphans_are_only_listed(repo):
    ok = repo.merged_wt("k1")
    kept = repo.merged_wt("k2")
    (kept / "w.txt").write_text("work")
    for w in (ok, kept):
        pathlib.Path(str(w) + "-scratch").mkdir()
    orphan = repo.wts / "gone-scratch"
    orphan.mkdir()
    rep = repo.sweep(apply=True)
    assert not pathlib.Path(str(ok) + "-scratch").exists() and pathlib.Path(str(kept) + "-scratch").exists()
    assert orphan.exists() and 'ORPHAN SCRATCH "%s"' % (str(orphan).replace("\\", "/")) in "\n".join(l.replace("\\", "/") for l in rep.lines)
    assert not any("k2-scratch" in l for l in rep.lines)


def test_scratch_symlink_is_not_followed(repo):
    wt = repo.merged_wt("sl")
    target = repo.tmp / "precious"
    target.mkdir()
    (target / "keep.txt").write_text("k")
    link = pathlib.Path(str(wt) + "-scratch")
    try:
        os.symlink(target, link, target_is_directory=True)
    except (OSError, NotImplementedError):
        pytest.skip("no symlink privilege here")
    rep = repo.sweep(apply=True)
    assert any(l.startswith("KEEP scratch") and l.endswith(": link") for l in rep.lines)
    assert (target / "keep.txt").exists() and os.path.lexists(link) and not wt.exists()


@pytest.mark.skipif(sys.platform != "win32", reason="junction is a Windows object")
def test_scratch_junction_is_not_followed(repo):
    wt = repo.merged_wt("jn")
    target = repo.tmp / "precious2"
    target.mkdir()
    (target / "keep.txt").write_text("k")
    link = pathlib.Path(str(wt) + "-scratch")
    r = subprocess.run(["cmd", "/c", "mklink", "/J", str(link), str(target)], capture_output=True)
    if r.returncode != 0:
        pytest.skip("mklink /J unavailable")
    rep = repo.sweep(apply=True)
    assert any(l.startswith("KEEP scratch") and l.endswith(": link") for l in rep.lines)
    assert (target / "keep.txt").exists() and not wt.exists()


def test_prunable_is_listed_pruned_and_its_branch_archived(repo):
    wt = repo.merged_wt("pr")
    head = git(wt, "rev-parse", "HEAD")
    shutil.rmtree(wt)
    dry = repo.sweep()
    assert has(dry, "PRUNABLE") and "pr" in repo.branches()
    rep = repo.sweep(apply=True)
    assert has(rep, "PRUNABLE") and line(rep, "REMOVED branch pr").endswith("archive: refs/worktree-sweep/pr/%s)" % head[:12])
    assert "pr" not in repo.branches() and "refs/heads/pr" not in git(repo.main, "worktree", "list", "--porcelain")
    assert git(repo.main, "rev-parse", "refs/worktree-sweep/pr/" + head[:12]) == head


def test_prunable_with_an_unmerged_branch_keeps_the_branch(repo):
    wt = repo.add_wt("pu")
    repo.commit(wt, "x.txt", "x")
    shutil.rmtree(wt)
    rep = repo.sweep(apply=True)
    assert has(rep, "KEEP branch pu: unmerged") and "pu" in repo.branches()


def test_detached_head_copy(repo):
    wt = repo.add_wt("d", detach=True)
    young = repo.sweep(now=time.time())
    assert "no own commits" in line(young, "KEEP")
    head = git(wt, "rev-parse", "HEAD")
    rep = repo.sweep(apply=True)
    assert re.search(r"\(branch \(detached\), merged: ancestor, own commits: no, junk: 0 files, archive: refs/worktree-sweep/detached/[^/]+/%s\)$"
                     % head[:12], line(rep, "REMOVED")) and not wt.exists()
    assert git(repo.main, "rev-parse", git(repo.main, "for-each-ref", "--format=%(refname)", "refs/worktree-sweep/")) == head


def _archived(repo, head):
    """The archive refs that hold `head` (positive evidence that the commit survives the removal)."""
    return git(repo.main, "for-each-ref", "--format=%(refname)", "--contains", head, "refs/worktree-sweep/").split()


def _failing_update_ref(calls):
    def runner(root, *args, timeout=120, stderr=False):
        calls.append(args)
        if args[0] == "update-ref":
            return 1, b"", b"fatal: cannot lock ref\n"
        return gitcmd.git(root, *args, timeout=timeout, stderr=stderr)
    return runner


def test_b1_detached_unmerged_prunable_is_archived_before_prune(repo):
    wt = repo.add_wt("dp", detach=True)
    head = repo.commit(wt, "dp.txt", "unmerged detached work")
    shutil.rmtree(wt)
    rep = repo.sweep(apply=True)
    assert has(rep, "PRUNABLE") and not has(rep, "KEEP prune") and rep.exit_code == 0
    assert not (repo.main / ".git" / "worktrees").exists() or not list((repo.main / ".git" / "worktrees").iterdir())   # prune ran
    refs = _archived(repo, head)
    assert len(refs) == 1 and refs[0].startswith("refs/worktree-sweep/detached/") and refs[0].endswith("/" + head[:12])
    git(repo.main, "cat-file", "-e", head + "^{commit}")


def test_the_helpers_never_let_a_patch_equal_twin_collide_with_its_original(repo):
    # t-1238 (CI, pipeline 7979462): a fast git makes the copy's commit and the cherry-pick in ONE second, and two commits with
    # the same tree, parent, message and identity are one sha. The dates are pinned EQUAL here (the fast clock, on any machine).
    wt = repo.add_wt("tw", detach=True)
    head = repo.commit(wt, "tw.txt", "work to be cherry-picked", env=PIN)
    twin = repo.twin(head, env=PIN)
    assert twin != head and git(repo.main, "log", "-1", "--format=%cI", twin) == git(wt, "log", "-1", "--format=%cI", head)   # same second, other sha
    git(repo.main, "push", "origin", "main")
    assert git(repo.main, "cherry", "origin/main", head) == "- " + head                       # patch-equal, not a descendant of the twin
    assert subprocess.run(["git", "-C", str(repo.main), "merge-base", "--is-ancestor", head, "origin/main"], env=_clean_env()).returncode == 1


def test_b1_detached_patch_equal_removed_by_apply_is_archived(repo):
    wt = repo.add_wt("dq", detach=True)
    head = repo.commit(wt, "dq.txt", "detached work cherry-picked into main")
    repo.twin(head)
    git(repo.main, "push", "origin", "main")
    rep = repo.sweep(apply=True)
    assert "merged: patch-equal, own commits: yes" in line(rep, "REMOVED") and not wt.exists()
    assert len(_archived(repo, head)) == 1
    assert repo.sweep(apply=True).exit_code == 0 and len(_archived(repo, head)) == 1         # a second run: the ref exists, no error


@pytest.mark.parametrize("how", ["archive-fails", "prune-rc1"])
def test_b1_archive_failure_skips_the_prune_and_the_sweep_goes_on(repo, how):
    # F-A2: a skipped prune is a FAILED line and exit 3; the prunable copy is "kept", not "removed"; no branch of a prunable is deleted
    calls = []
    if how == "archive-fails":
        wt = repo.add_wt("df", detach=True)
        head = repo.commit(wt, "df.txt", "unmerged detached work")
        shutil.rmtree(wt)
        other = repo.merged_wt("ok1")
        rep = repo.sweep(apply=True, runner=_failing_update_ref(calls))
        assert len([l for l in rep.lines if l.startswith("FAILED prune")]) == 1 and not has(rep, "KEEP prune")
        assert "archive ref failed (fatal: cannot lock ref)" in line(rep, "FAILED prune")
        assert not any(a[:2] == ("worktree", "prune") for a in calls)                       # prune did not run
        assert (repo.main / ".git" / "worktrees").exists() and "dp" not in repo.branches() and _archived(repo, head) == []
        assert has(rep, "KEEP branch ok1: archive ref failed") and not other.exists()
    else:
        gone = repo.merged_wt("pb")
        shutil.rmtree(gone)
        other = repo.merged_wt("ok2")

        def runner(root, *args, timeout=120, stderr=False):
            if args[:2] == ("worktree", "prune"):
                return 1, b"", b"fatal: cannot prune\n"
            return gitcmd.git(root, *args, timeout=timeout, stderr=stderr)

        rep = repo.sweep(apply=True, runner=runner)
        assert line(rep, "FAILED worktree prune").endswith("fatal: cannot prune")
        assert "pb" in repo.branches() and not has(rep, "REMOVED branch pb") and not has(rep, "KEEP branch pb") and not other.exists()
    assert rep.exit_code == 3
    assert rep.lines[-1] == "worktree_sweep: 2 registered, 1 removed, 1 kept, 1 failed"      # the prunable is not in "removed"


@pytest.mark.parametrize("case", ["old-merged-apply", "young", "unmerged", "no-origin-main", "dry-run", "exactly-N"])
def test_r1_archive_refs_expire_only_when_old_and_in_origin_main(repo, case):
    # F-A1: old = committer date more than N days back (strict), AND reachable from origin/main; a dry run only counts
    N = ws.ARCHIVE_KEEP_DAYS
    sha = git(repo.main, "rev-parse", "origin/main")
    if case == "unmerged":
        sha = repo.commit(repo.add_wt("um"), "um.txt", "unmerged work")
    cdate = int(git(repo.main, "log", "-1", "--format=%ct", sha))
    ref = "refs/worktree-sweep/t/" + sha[:12]
    git(repo.main, "update-ref", ref, sha)
    now = {"young": cdate + 86400, "exactly-N": cdate + N * 86400}.get(case, time.time() + (N + 1) * 86400)
    if case == "no-origin-main":
        git(repo.main, "update-ref", "-d", "refs/remotes/origin/main")
    calls = []

    def runner(root, *args, timeout=120, stderr=False):
        calls.append(args)
        return gitcmd.git(root, *args, timeout=timeout, stderr=stderr)

    rep = repo.sweep(apply=case != "dry-run", now=now, runner=runner, ref="main" if case == "no-origin-main" else ws.DEFAULT_REF)
    tail = "(in origin/main, committed more than %d days ago), " % N
    expect = {"old-merged-apply": "archive refs: 1 expired " + tail + "0 kept", "dry-run": "archive refs: 1 can expire " + tail + "0 kept"}
    if case == "no-origin-main":
        assert line(rep, "KEEP archive refs").endswith("origin/main does not resolve -- none expired") and not has(rep, "archive refs:")
    else:
        assert line(rep, "archive refs:") == expect.get(case, "archive refs: 0 expired " + tail + "1 kept")
    assert (git(repo.main, "for-each-ref", "--format=%(refname)", ref) == "") == (case == "old-merged-apply")
    assert not any(a[:2] == ("update-ref", "-d") for a in calls) or case == "old-merged-apply"
    assert rep.exit_code == 0


def test_r1_a_local_branch_named_origin_main_does_not_shadow_the_remote_ref(repo):
    # F1: `git branch origin/main <unpushed commit>` makes the short name resolve to the local branch; the expiry names the full remote ref
    sha = repo.commit(repo.add_wt("um"), "um.txt", "unpushed work")
    git(repo.main, "branch", "origin/main", sha)
    ref = "refs/worktree-sweep/t/" + sha[:12]
    git(repo.main, "update-ref", ref, sha)
    rep = repo.sweep(apply=True, now=time.time() + (ws.ARCHIVE_KEEP_DAYS + 1) * 86400)
    assert line(rep, "archive refs:").startswith("archive refs: 0 expired (") and git(repo.main, "for-each-ref", "--format=%(refname)", ref) == ref


def test_r1_a_symref_under_the_archive_prefix_never_deletes_its_target(repo):
    # F2: `update-ref -d` follows a symbolic ref; --no-deref deletes only the listed ref
    sha = git(repo.main, "rev-parse", "origin/main")
    git(repo.main, "branch", "keepme", sha)
    git(repo.main, "symbolic-ref", "refs/worktree-sweep/x/sym", "refs/heads/keepme")
    repo.sweep(apply=True, now=time.time() + (ws.ARCHIVE_KEEP_DAYS + 1) * 86400)
    assert "keepme" in repo.branches()


def test_r1_no_archive_ref_and_a_ref_that_is_not_a_commit_are_counted_quietly(repo):
    rep = repo.sweep(apply=True, now=time.time() + 40 * 86400)
    assert line(rep, "archive refs:").startswith("archive refs: 0 expired (") and line(rep, "archive refs:").endswith(", 0 kept")
    tree = git(repo.main, "rev-parse", "HEAD^{tree}")
    git(repo.main, "update-ref", "refs/worktree-sweep/tree/x", tree)                         # E20: no committer date -> kept
    rep = repo.sweep(apply=True, now=time.time() + 40 * 86400)
    assert line(rep, "archive refs:").endswith(", 1 kept") and git(repo.main, "for-each-ref", "refs/worktree-sweep/tree/")


@pytest.mark.parametrize("how", ["moved", "rc128"])
def test_q5_detached_head_is_read_again_before_remove(repo, how):
    wt = repo.add_wt("dr", detach=True)
    old = git(wt, "rev-parse", "HEAD")
    seen = []

    def runner(root, *args, timeout=120, stderr=False):
        if args == ("rev-parse", "--verify", "HEAD"):
            seen.append(root)
            if how == "rc128":
                return 128, b"", b"fatal: bad HEAD\n"
            repo.commit(wt, "late.txt", "a commit made after the read")
        return gitcmd.git(root, *args, timeout=timeout, stderr=stderr)

    rep = repo.sweep(apply=True, runner=runner)
    assert len(seen) == 1 and wt.exists() and not has(rep, "REMOVED")
    if how == "rc128":
        assert "unknown (HEAD re-read: fatal: bad HEAD)" in line(rep, "KEEP")
    else:
        new = git(wt, "rev-parse", "HEAD")
        assert new != old and 'HEAD moved since the read (%s -> %s)' % (old[:12], new[:12]) in line(rep, "KEEP")
        git(wt, "cat-file", "-e", new + "^{commit}")                                         # the new commit is reachable from the copy
    assert rep.lines[-1] == "worktree_sweep: 1 registered, 0 removed, 1 kept, 0 failed"


def test_b1_archive_failure_keeps_a_detached_copy_that_exists(repo):
    wt = repo.add_wt("dk", detach=True)
    head = repo.commit(wt, "dk.txt", "detached work")
    repo.twin(head)
    git(repo.main, "push", "origin", "main")
    rep = repo.sweep(apply=True, runner=_failing_update_ref([]))
    assert line(rep, "KEEP").endswith(": archive ref failed (fatal: cannot lock ref)") and wt.exists() and not has(rep, "REMOVED")


def test_m1_broken_junk_file_and_a_sha_ref_keep_main_while_the_main_checkout_is_on_another_branch(repo, tmp_path):
    git(repo.main, "checkout", "-b", "other")
    wt = repo.add_wt("mm", branch="main", existing=True)
    sha = git(repo.main, "rev-parse", "origin/main")
    path = tmp_path / "broken.json"
    path.write_text("{not json")
    junk = ws.load_junk(path)
    assert junk.protected == [ws.BACKGROUND_REF] and junk.warnings
    rep = repo.sweep(ref=sha, apply=True, junk=junk)
    assert line(rep, "KEEP").endswith(": protected branch main") and wt.exists() and "main" in repo.branches()


def test_m3_an_exception_in_apply_one_is_one_line_and_the_next_copy_is_still_processed(repo, monkeypatch):
    first = repo.merged_wt("x1")
    second = repo.merged_wt("x2")
    real = ws.apply_one
    seen = []

    def flaky(ctx, wt, ev, rep):
        seen.append(wt.path)
        if len(seen) == 1:
            raise PermissionError("denied by the OS\nsecond line")
        return real(ctx, wt, ev, rep)

    monkeypatch.setattr(ws, "apply_one", flaky)
    rep = repo.sweep(apply=True)
    errors = [l for l in rep.lines if l.startswith("ERROR ")]
    assert len(errors) == 1 and errors[0].endswith(": PermissionError: denied by the OS") and errors[0].startswith('ERROR "')
    assert has(rep, "REMOVED") and rep.exit_code == 3 and len(seen) == 2
    assert sorted([first.exists(), second.exists()]) == [False, True]


def test_path_with_a_space_is_printed_whole_and_the_form_separates_path_from_reason(repo):
    wt = repo.merged_wt("with space", branch="wspace")
    listed = [w.path for w in ws.parse_worktrees(gitcmd.git(repo.main, "worktree", "list", "--porcelain", "-z")[1])][1]
    assert " " in listed
    l1 = line(repo.sweep(), "CAN REMOVE")
    m = re.match(r'^CAN REMOVE "(.+)" \(branch ', l1)
    assert m and m.group(1) == listed
    (wt / "w.txt").write_text("work")
    l2 = line(repo.sweep(), "KEEP")
    m = re.match(r'^KEEP "(.+?)": real changes: ', l2)
    assert m and m.group(1) == listed
    assert sys.platform != "win32" or re.match(r"^[A-Za-z]:", listed)      # the drive colon sits INSIDE the quoted path


def test_the_main_worktree_and_its_branch_are_never_candidates(repo):
    rep = repo.sweep()
    assert rep.registered == 0 and not any("CAN REMOVE" in l for l in rep.lines)


# ------------------------------------------------------------------------------ the data file (E13)

def test_junk_file_absent_or_broken_makes_traces_real_changes(repo, tmp_path):
    wt = repo.merged_wt("jf")
    (wt / "bash.exe.stackdump").write_text("trace")
    for name, content in (("absent.json", None), ("broken.json", "{not json"), ("empty.json", '{"untracked_dirs": [], "untracked_names": []}')):
        path = tmp_path / name
        if content is not None:
            path.write_text(content)
        junk = ws.load_junk(path)
        rep = repo.sweep(junk=junk)
        assert has(rep, "KEEP") and "real changes: bash.exe.stackdump" in line(rep, "KEEP"), name
        assert bool(junk.warnings) == (name != "empty.json")


@pytest.mark.parametrize("entry", ["", "  ", "/", ".", "/abs/", "C:/x/", "..", "a/../b/", "a*/", "dir[1]/", "nodir", "back\\slash/"])
def test_forbidden_directory_entries_are_ignored_with_a_warning(tmp_path, entry):
    path = tmp_path / "j.json"
    path.write_text(json.dumps({"untracked_dirs": [entry, "ok/"], "untracked_names": [], "protected_branches": ["x"]}))
    junk = ws.load_junk(path)
    assert junk.dirs == ["ok/"] and len(junk.warnings) == 1 and junk.protected == ["x"]


@pytest.mark.parametrize("entry", ["", "/", ".", "a/b", "*", "x?y"])
def test_forbidden_name_entries_are_ignored_with_a_warning(tmp_path, entry):
    path = tmp_path / "j.json"
    path.write_text(json.dumps({"untracked_names": [entry, "ok.txt"]}))
    junk = ws.load_junk(path)
    assert junk.names == ["ok.txt"] and len(junk.warnings) == 1


def test_the_shipped_junk_file_is_clean():
    junk = ws.load_junk()
    assert junk.warnings == [] and ".claude/dod_track/" in junk.dirs and "bash.exe.stackdump" in junk.names


def test_protected_branch_from_the_data_is_kept(repo, tmp_path):
    repo.merged_wt("pb")
    path = tmp_path / "j.json"
    path.write_text(json.dumps({"protected_branches": ["pb"]}))
    assert line(repo.sweep(junk=ws.load_junk(path)), "KEEP").endswith(": protected branch pb")


# ------------------------------------------------------------------------------ M1, M2: no write before the removal

def test_dry_run_and_count_do_not_rewrite_the_copys_index_or_head(repo):
    wt = repo.add_wt("im")
    os.utime(wt / "base.txt", (time.time() + 5, time.time() + 5))         # makes a plain `git status` want to refresh the index
    adm = repo.admin(wt)
    x = 1_700_000_000
    os.utime(adm / "index", (x, x))
    os.utime(adm / "HEAD", (x, x))
    before = ((adm / "index").stat().st_mtime_ns, (adm / "HEAD").stat().st_mtime_ns)
    rep = repo.sweep(now=OLD())
    assert has(rep, "CAN REMOVE") or has(rep, "KEEP")
    ws.count_estimate(repo.main)
    assert ((adm / "index").stat().st_mtime_ns, (adm / "HEAD").stat().st_mtime_ns) == before
    git(wt, "status", "--porcelain")                                      # positive control: the plain status DOES rewrite it
    assert (adm / "index").stat().st_mtime_ns != before[0]


def test_a_file_that_appears_between_status_and_remove_is_not_deleted(repo):
    wt = repo.merged_wt("late")
    scratch = pathlib.Path(str(wt) + "-scratch")
    scratch.mkdir()

    def runner(root, *args, timeout=120, stderr=False):
        if args[:2] == ("worktree", "remove"):
            (wt / "late.txt").write_text("written by an agent after the read")
        return gitcmd.git(root, *args, timeout=timeout, stderr=stderr)

    rep = repo.sweep(apply=True, runner=runner)
    assert line(rep, "KEEP").startswith('KEEP "') and ": changed during sweep (" in line(rep, "KEEP")
    assert rep.exit_code == 0 and (wt / "late.txt").exists() and "late" in repo.branches() and scratch.exists()


def test_a_failing_remove_on_a_clean_tree_is_failed_and_leaves_branch_and_scratch(repo):
    wt = repo.merged_wt("fail")
    scratch = pathlib.Path(str(wt) + "-scratch")
    scratch.mkdir()

    def runner(root, *args, timeout=120, stderr=False):
        if args[:2] == ("worktree", "remove"):
            return 128, b"", b"error: Permission denied: another process uses it\n"
        return gitcmd.git(root, *args, timeout=timeout, stderr=stderr)

    rep = repo.sweep(apply=True, runner=runner)
    assert line(rep, "FAILED").endswith(": error: Permission denied: another process uses it")
    assert rep.exit_code == 3 and wt.exists() and "fail" in repo.branches() and scratch.exists()
    assert rep.lines[-1] == "worktree_sweep: 1 registered, 0 removed, 0 kept, 1 failed"


def test_archive_ref_failure_keeps_the_branch(repo):
    wt = repo.merged_wt("ar")

    def runner(root, *args, timeout=120, stderr=False):
        if args[0] == "update-ref":
            return 1, b"", b"fatal: cannot lock ref\n"
        return gitcmd.git(root, *args, timeout=timeout, stderr=stderr)

    rep = repo.sweep(apply=True, runner=runner)
    assert line(rep, "KEEP branch ar: archive ref failed (fatal: cannot lock ref)") and "ar" in repo.branches() and not wt.exists()


def test_archive_ref_that_reads_back_wrong_keeps_the_branch(repo):
    repo.merged_wt("aw")

    def runner(root, *args, timeout=120, stderr=False):
        if args[0] == "rev-parse" and args[-1].startswith("refs/worktree-sweep/"):
            return 0, b"f" * 40 + b"\n", b""
        return gitcmd.git(root, *args, timeout=timeout, stderr=stderr)

    rep = repo.sweep(apply=True, runner=runner)
    assert "archive ref failed" in line(rep, "KEEP branch aw") and "aw" in repo.branches()


def test_archive_ref_that_already_exists_and_equals_head_is_not_an_error(repo):
    wt = repo.merged_wt("ae")
    head = git(wt, "rev-parse", "HEAD")
    git(repo.main, "update-ref", "refs/worktree-sweep/ae/" + head[:12], head)
    rep = repo.sweep(apply=True)
    assert has(rep, "REMOVED") and not has(rep, "KEEP branch") and "ae" not in repo.branches()


def test_the_same_branch_name_twice_leaves_two_archive_refs(repo):
    for round_ in (1, 2):
        wt = repo.add_wt("w%d" % round_, branch="pile/x/batch-1")
        repo.commit(wt, "r%d.txt" % round_, "r")
        repo.merge("pile/x/batch-1")
        assert has(repo.sweep(apply=True), "REMOVED")
    refs = git(repo.main, "for-each-ref", "--format=%(refname)", "refs/worktree-sweep/pile/x/batch-1/").split()
    assert len(refs) == 2 and len(set(refs)) == 2


# ------------------------------------------------------------------------------ git cherry, the inconvenient inputs

def test_cherry_1_squash_merged_branch_is_not_merged(repo):
    wt = repo.add_wt("c1")
    repo.commit(wt, "a.txt", "a")
    repo.commit(wt, "b.txt", "b")
    repo.merge("c1", squash=True)
    assert line(repo.sweep(), "KEEP").endswith("unmerged (2 commits not in origin/main)")


def test_cherry_2_a_commit_and_its_revert_with_only_the_commit_in_main_stays(repo):
    wt = repo.add_wt("c2")
    a = repo.commit(wt, "a.txt", "a")
    git(wt, "revert", "--no-edit", "HEAD")
    repo.twin(a)
    git(repo.main, "push", "origin", "main")
    assert line(repo.sweep(), "KEEP").endswith("unmerged (1 commits not in origin/main)")


def test_cherry_3_a_commit_main_later_reverted_reads_patch_equal_and_the_archive_ref_keeps_it(repo):
    wt = repo.add_wt("c3")
    h = repo.commit(wt, "f.txt", "x\n")
    repo.commit(repo.main, "f.txt", "x\n", "same change on main")
    git(repo.main, "revert", "--no-edit", "HEAD")
    git(repo.main, "push", "origin", "main")
    assert "f.txt" not in git(repo.main, "ls-tree", "--name-only", "origin/main")       # the change is NOT in main's tree
    assert "merged: patch-equal" in line(repo.sweep(), "CAN REMOVE")
    rep = repo.sweep(apply=True)
    assert "merged: patch-equal" in line(rep, "REMOVED") and "c3" not in repo.branches()
    assert git(repo.main, "rev-parse", "refs/worktree-sweep/c3/" + h[:12]) == h


def test_cherry_4_an_empty_commit_prints_plus_and_the_branch_stays(repo):
    wt = repo.add_wt("c4")
    git(wt, "commit", "--allow-empty", "-m", "empty")
    assert line(repo.sweep(), "KEEP").endswith("unmerged (1 commits not in origin/main)")


def test_cherry_5_a_merge_commit_only_branch_reads_patch_equal_and_the_ref_holds_the_resolution(repo):
    # y1: a branch off base (line 2 -> Y), merged into main with a conflict resolved there; its worktree is gone, the branch stays
    y = repo.add_wt("y1")
    repo.commit(y, "base.txt", "1\nY\n3\n", "Y1")
    git(repo.main, "worktree", "remove", str(y))
    wt = repo.add_wt("c5")
    d = repo.commit(wt, "base.txt", "D\n2\n3\n", "D")                      # line 1 -> D
    repo.twin(d)                                                           # main gets the same patch under another sha
    git(repo.main, "push", "origin", "main")
    git(repo.main, "merge", "--no-ff", "-m", "merge y1", "y1", check=False)
    (repo.main / "base.txt").write_text("D\nY\n3\n")
    git(repo.main, "add", "-A")
    git(repo.main, "commit", "--no-edit")
    git(repo.main, "push", "origin", "main")
    git(wt, "merge", "y1", check=False)                                    # the same conflict inside the copy: adjacent lines
    assert "UU" in git(wt, "status", "--porcelain")
    (wt / "base.txt").write_text("RESOLVED\nY\n3\n")
    git(wt, "add", "-A")
    git(wt, "commit", "--no-edit")
    h = git(wt, "rev-parse", "HEAD")
    assert len(git(wt, "rev-list", "--parents", "-n1", "HEAD").split()) == 3          # the tip IS a merge commit
    # `git cherry` SKIPS a merge commit: measured on git 2.47.3 (the CI image) it prints nothing for `h`. The old assertion
    # (`startswith("- ")`) passed only because `d` and main's twin were two shas on a slow clock; on a fast one they were one sha,
    # the range held `h` alone and the output was empty. Now `d` has its own line (the twin is distinct) and `h` may print nothing
    # or `- h`; what the tool relies on is that nothing is marked `+` (unmerged). The verdict itself is asserted next.
    cherry = git(repo.main, "cherry", "origin/main", h).split("\n")
    assert "- " + d in cherry and all(l.startswith("- ") for l in cherry) and {l[2:] for l in cherry} <= {d, h}
    assert "merged: patch-equal" in line(repo.sweep(), "CAN REMOVE")
    rep = repo.sweep(apply=True)
    assert has(rep, "REMOVED")
    ref = "refs/worktree-sweep/c5/" + h[:12]
    assert git(repo.main, "rev-parse", ref) == h and git(repo.main, "show", ref + ":base.txt").startswith("RESOLVED")


# ------------------------------------------------------------------------------ refusals

def test_apply_from_a_linked_worktree_is_refused_and_a_dry_run_works(repo):
    repo.merged_wt("x1")
    linked = repo.add_wt("x2")
    rep = repo.sweep(root=linked, apply=True)
    assert rep.exit_code == 1 and "--apply runs from the main checkout" in rep.lines[0] and "this is the linked worktree" in rep.lines[0]
    assert "x1" in repo.branches()
    dry = repo.sweep(root=linked)
    assert dry.exit_code == 0 and has(dry, "CAN REMOVE")


def test_missing_ref_refuses_with_the_door_and_removes_nothing(repo):
    wt = repo.merged_wt("nr")
    rep = repo.sweep(ref="nowhere/main", apply=True)
    assert rep.exit_code == 1 and "--ref main" in rep.lines[0] and wt.exists() and "nr" in repo.branches()


def test_not_a_git_repository_refuses(tmp_path):
    rep = ws.sweep(tmp_path / "nothing", ref="main")
    assert rep.exit_code == 1 and "not a git repository" in rep.lines[0]


def test_the_local_main_can_be_the_reference(repo):
    repo.merged_wt("lm")
    rep = repo.sweep(ref="main", apply=True)
    assert rep.exit_code == 0 and has(rep, "REMOVED") and has(rep, "judged against main at ")


def test_an_error_on_one_copy_does_not_stop_the_others(repo):
    repo.merged_wt("e1")
    repo.merged_wt("e2")

    def runner(root, *args, timeout=120, stderr=False):
        if args[0] == "merge-base" and not hasattr(runner, "done"):
            runner.done = True
            raise RuntimeError("boom")
        return gitcmd.git(root, *args, timeout=timeout, stderr=stderr)

    rep = repo.sweep(runner=runner)
    assert sum(1 for l in rep.lines if l.startswith("KEEP") and "unknown (RuntimeError: boom)" in l) == 1 and has(rep, "CAN REMOVE")


# ------------------------------------------------------------------------------ the hook body (--post-merge)

def test_git_call_timeout_is_one_number_the_default_or_the_given_one(repo):
    # t-1738 (§2.1): the budget of S seconds is gone; the only limit left is the timeout of ONE git call
    seen = []

    def runner(root, *args, timeout=120, stderr=False):
        seen.append(timeout)
        return gitcmd.git(root, *args, timeout=timeout, stderr=stderr)

    ws.Git(runner)(repo.main, "status", "--porcelain")
    ws.Git(runner, 5)(repo.main, "status", "--porcelain")
    assert seen == [gitcmd.DEFAULT_TIMEOUT, 5]
    ws.read_status(repo.main, runner=runner, timeout=7)
    assert seen[-1] == 7 and all(t == 7 for t in seen[2:])


def test_timeout_of_a_remove_is_failed_timeout_and_the_next_copy_is_still_processed(repo):
    for nm in ("t1", "t2"):
        wt = repo.add_wt(nm)
        repo.commit(wt, nm + ".txt", nm)
    git(repo.main, "merge", "--no-ff", "-m", "m", "t1", "t2")

    def runner(root, *args, timeout=120, stderr=False):
        if args[:2] == ("worktree", "remove"):
            return -1, b"", b"Command '[git]' timed out after 10 seconds"
        return gitcmd.git(root, *args, timeout=timeout, stderr=stderr)

    rep = repo.sweep(apply=True, runner=runner, ref="main")
    assert len([l for l in rep.lines if l.startswith("FAILED ") and ": timeout (" in l]) == 2     # the second copy was NOT skipped
    assert "t1" in repo.branches() and "t2" in repo.branches() and rep.exit_code == 3


# ------------------------------------------------------------------------------ --count

def test_count_estimate_counts_registered_and_merged_branches(repo):
    repo.merged_wt("n1")
    repo.add_wt("n2")
    repo.commit(repo.wts / "n2", "z.txt", "z")
    locked = repo.merged_wt("n3")
    git(repo.main, "worktree", "lock", str(locked))
    assert ws.count_estimate(repo.main) == (3, 1, "origin/main")


def test_count_makes_at_most_two_git_calls_and_reports_a_failure(repo):
    calls = []

    def runner(root, *args, timeout=120, stderr=False):
        calls.append((args, timeout))
        return gitcmd.git(root, *args, timeout=timeout, stderr=stderr)

    ws.count_estimate(repo.main, runner=runner)
    assert len(calls) == 2 and all(t == 5 for _, t in calls)
    with pytest.raises(RuntimeError, match="branch --merged nowhere/main"):
        ws.count_estimate(repo.main, ref="nowhere/main")
    with pytest.raises(RuntimeError, match="worktree list"):
        ws.count_estimate(repo.tmp / "none")


def test_count_cli_prints_the_number(repo, capsys):
    repo.merged_wt("cc")
    assert ws.main(["--count", "--repo", str(repo.main)]) == 0
    assert capsys.readouterr().out.strip() == "1"


def test_parse_worktrees_locked_prunable_and_detached():
    raw = (b"worktree C:/m\0HEAD " + b"a" * 40 + b"\0branch refs/heads/main\0\0"
           b"worktree C:/x y/l\0HEAD " + b"b" * 40 + b"\0detached\0locked in use\0\0"
           b"worktree C:/p\0HEAD " + b"c" * 40 + b"\0branch refs/heads/p\0prunable gitdir file points to non-existent location\0\0")
    m, l, p = ws.parse_worktrees(raw)
    assert m.short == "main" and l.detached and l.locked == "in use" and l.path == "C:/x y/l" and p.prunable.startswith("gitdir")


# ------------------------------------------------------------------------------ source censuses (K2), the hook (K6, K9)

SOURCE = (TOOLS / "worktree_sweep.py").read_text(encoding="utf-8")


def test_k2_no_trace_names_and_no_protected_main_literal_in_the_code():
    data = (TOOLS / "worktree-junk.json").read_text(encoding="utf-8")
    assert "dod_track" in data and "search-ledger" in data and "stackdump" in data             # positive control: they live in the data
    for needle in ("dod_track", "search-ledger", "stackdump"):
        assert needle not in SOURCE, needle
    assert not re.search(r"protected\w*\s*=\s*[\[\({]\s*[\"']main[\"']", SOURCE)
    assert '["main"]' not in SOURCE and "('main',)" not in SOURCE and '{"main"}' not in SOURCE


def test_k2_no_force_in_the_git_arguments():
    tree = ast.parse(SOURCE)
    constants = [n.value for n in ast.walk(tree) if isinstance(n, ast.Constant) and isinstance(n.value, str)]
    assert not [c for c in constants if c in ("--force", "-f", "--force-delete")]
    remove_calls = [n for n in ast.walk(tree) if isinstance(n, ast.Call) and [a.value for a in n.args if isinstance(a, ast.Constant)][:2] == ["worktree", "remove"]]
    assert len(remove_calls) == 1                                                                   # positive control: the call is found


def test_k6_the_hook_text_names_only_covered_tools_and_the_module_imports_stay_in_the_net(tmp_path):
    (tmp_path / ".githooks").mkdir()
    (tmp_path / ".githooks" / "post-merge").write_text(HOOK, encoding="utf-8")
    pattern = re.compile(r"tools[/\\][A-Za-z0-9_.\\/-]+\.py")
    refs = pattern.findall((tmp_path / ".githooks" / "post-merge").read_text(encoding="utf-8"))
    assert set(refs) == {"tools/worktree_sweep.py"} and all(any(mg._matches(r, p) for p in mg.MECHANISM_PREFIXES) for r in refs)
    assert not any(mg._matches("tools/not_in_the_net.py", p) for p in mg.MECHANISM_PREFIXES)      # negative control
    imported = {a.name.split(".")[0] for n in ast.walk(ast.parse(SOURCE)) if isinstance(n, ast.Import) for a in n.names}
    imported |= {n.module.split(".")[0] for n in ast.walk(ast.parse(SOURCE)) if isinstance(n, ast.ImportFrom) and n.module}
    local = [m for m in imported if (TOOLS / (m + ".py")).exists()]
    assert local == ["gitcmd"] and all(any(mg._matches("tools/%s.py" % m, p) for p in mg.MECHANISM_PREFIXES) for m in local)


needs_sh = pytest.mark.skipif(shutil.which("sh") is None, reason="no sh on this machine (the BATCH CANON docker run executes it)")


def _sh(hook, cwd, tmp, flag="0"):
    env = _clean_env()
    env["PATH"] = str(pathlib.Path(sys.executable).parent) + os.pathsep + env.get("PATH", "")
    return subprocess.run(["sh", pathlib.Path(hook).as_posix(), flag], cwd=str(cwd), capture_output=True, text=True, env=env)


@needs_sh
def test_k9_sh_guard_exits_silently_in_a_linked_worktree_without_the_tool(repo):
    hook = repo.tmp / "post-merge"
    hook.write_text(HOOK, encoding="utf-8", newline="\n")
    linked = repo.add_wt("sh1")
    assert not (linked / "tools" / "worktree_sweep.py").exists()
    p = _sh(hook, linked, repo.tmp)
    assert p.returncode == 0 and p.stderr == "" and p.stdout == ""
    p = _sh(hook, repo.main, repo.tmp)                                     # the main checkout, the tool absent: says so, exit 0
    assert p.returncode == 0 and "tools/worktree_sweep.py not found; nothing swept" in p.stderr


@needs_sh
def test_k9_sh_guard_calls_python_in_the_main_checkout(repo):
    hook = repo.tmp / "post-merge"
    hook.write_text(HOOK, encoding="utf-8", newline="\n")
    (repo.main / "tools").mkdir()
    (repo.main / "tools" / "worktree_sweep.py").write_text(
        "import sys, pathlib\npathlib.Path('marker.txt').write_text(' '.join(sys.argv[1:]))\nsys.exit(5)\n")
    p = _sh(hook, repo.main, repo.tmp, flag="1")
    assert p.returncode == 0                                              # the tool's exit code 5 never fails the hook
    assert (repo.main / "marker.txt").read_text() == "--post-merge --squash-flag 1"


@needs_sh
def test_w19_the_hook_end_to_end_starts_the_background_sweep_that_removes_the_merged_copy(repo):
    (repo.main / "tools").mkdir()
    for name in ("worktree_sweep.py", "gitcmd.py", "worktree-junk.json"):
        shutil.copy(TOOLS / name, repo.main / "tools" / name)
    (repo.main / ".githooks").mkdir()
    hook = repo.main / ".githooks" / "post-merge"
    hook.write_text(HOOK, encoding="utf-8", newline="\n")
    os.chmod(hook, 0o755)          # CI (Linux): git IGNORES a hook without the executable bit ("hook was ignored ... not set as executable");
    #                                Windows: every file is executable and chmod does not change that -- the call is still required
    git(repo.main, "add", "-A")
    git(repo.main, "commit", "-m", "tools and hook")
    git(repo.main, "push", "origin", "main")
    git(repo.main, "config", "core.hooksPath", str(repo.main / ".githooks"))
    wt = repo.add_wt("e2e")
    repo.commit(wt, "e2e.txt", "x")
    env = _clean_env()
    env["PATH"] = str(pathlib.Path(sys.executable).parent) + os.pathsep + env.get("PATH", "")
    p = subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t", "-C", str(repo.main), "merge", "--no-ff", "-m", "m", "e2e"],
                       capture_output=True, text=True, env=env)
    assert p.returncode == 0, p.stderr
    assert "worktree sweep started in the background" in p.stdout + p.stderr           # the merge came back with the launch line
    sd = repo.main / ".git" / "worktree-sweep"
    deadline = time.time() + 120
    while time.time() < deadline:                       # the only sleep of this file: the detached child works on its own
        status = _status(sd)
        if status and status.get("state") != "running" and not (sd / "lock").exists():
            break
        time.sleep(0.5)
    status = _status(sd)
    assert status and status["state"] == "finished" and status["trigger"] == "post-merge", status
    assert not wt.exists() and "e2e" not in repo.branches()
    assert "REMOVED" in (sd / "run.log").read_text(encoding="utf-8")


# ------------------------------------------------------------------------------ t-1738 (FG7-4): the full background sweep (W1-W26)

def _status(sd):
    try:
        return json.loads((sd / "status.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def _sd(repo):
    return repo.main / ".git" / "worktree-sweep"


def _ctx(repo, root=None):
    return ws.repo_context(ws.Git(), root or repo.main)


def with_tool(repo):
    """The main checkout carries tools/worktree_sweep.py (a launch refuses without it, E28); an untracked stub is enough."""
    (repo.main / "tools").mkdir(exist_ok=True)
    (repo.main / "tools" / "worktree_sweep.py").write_text("# stub\n")


class Spawn:
    def __init__(self, error=None):
        self.calls, self.error = [], error

    def __call__(self, argv, cwd, env):
        self.calls.append((argv, cwd, env))
        if self.error:
            raise self.error
        return 4242


def put_lock(sd, token="t" * 32, started=None, mtime=None, text=None, trigger="manual", pid=1):
    sd.mkdir(parents=True, exist_ok=True)
    p = sd / "lock"
    p.write_text(text if text is not None else json.dumps(
        {"token": token, "pid": pid, "started": started or ws._iso(), "trigger": trigger}), encoding="utf-8")
    if mtime is not None:
        os.utime(p, (mtime, mtime))
    return p


def run_body(repo, trigger="manual", out=None, ref="main", **kw):
    lock, holder = ws.acquire_lock(_sd(repo), trigger)
    assert lock is not None, holder
    return ws.run_locked(_ctx(repo), lock, trigger, out, ref=ref, **kw)


def test_w1_a_second_acquire_gets_the_holder_of_the_first(tmp_path):
    a, none = ws.acquire_lock(tmp_path / "sd", "manual")
    assert a is not None and none is None and (tmp_path / "sd" / "lock").exists()
    b, holder = ws.acquire_lock(tmp_path / "sd", "post-merge")
    assert b is None and holder["token"] == a.token and holder["trigger"] == "manual" and holder["pid"] == os.getpid()


def test_w2_a_lock_silent_for_exactly_STALE_S_is_alive_one_second_more_is_taken_over(tmp_path):
    sd = tmp_path / "sd"
    first, _ = ws.acquire_lock(sd, "manual")
    m = int(time.time())
    os.utime(sd / "lock", (m, m))
    busy, holder = ws.acquire_lock(sd, "post-merge", now=m + ws.STALE_S)                       # AT the limit
    assert busy is None and holder["token"] == first.token
    taken, none = ws.acquire_lock(sd, "post-merge", now=m + ws.STALE_S + 1)                    # BEYOND it
    assert taken is not None and none is None and taken.token != first.token
    assert len(list(sd.glob("lock.stale-*"))) == 1 and ws._read_lock(sd / "lock")[0]["token"] == taken.token


def test_w3_a_lock_older_than_MAX_RUN_S_is_not_trusted_even_when_it_beats(tmp_path):
    sd = tmp_path / "sd"
    now = int(time.time())
    put_lock(sd, started=ws._iso(now - ws.MAX_RUN_S), mtime=now)                              # a fresh beat, a run of exactly MAX_RUN_S
    assert ws.acquire_lock(sd, "manual", now=now)[0] is None
    put_lock(sd, started=ws._iso(now - ws.MAX_RUN_S - 1), mtime=now)
    lock, holder = ws.acquire_lock(sd, "manual", now=now)
    assert lock is not None and holder is None


def test_w4_an_unreadable_lock_is_busy_when_fresh_and_dead_when_old(tmp_path):
    sd = tmp_path / "sd"
    now = int(time.time())
    put_lock(sd, text="{not json", mtime=now - 10)
    lock, holder = ws.acquire_lock(sd, "manual", now=now)
    assert lock is None and holder["token"] == "unreadable"
    put_lock(sd, text="{not json", mtime=now - ws.STALE_S - 1)
    lock, holder = ws.acquire_lock(sd, "manual", now=now)
    assert lock is not None and list(sd.glob("lock.stale-*-unreadable"))


def test_w5_losing_the_takeover_race_is_busy_and_the_lock_stays(tmp_path, monkeypatch):
    sd = tmp_path / "sd"
    now = int(time.time())
    put_lock(sd, token="o" * 32, mtime=now - ws.STALE_S - 1)

    def other_was_faster(src, dst):
        raise FileNotFoundError("the other run renamed it first")

    monkeypatch.setattr(ws.os, "rename", other_was_faster)
    lock, holder = ws.acquire_lock(sd, "manual", now=now)
    assert lock is None and holder["token"] == "o" * 32 and (sd / "lock").exists()


def test_w6_a_run_that_lost_its_lock_beats_no_more_removes_nothing_and_never_deletes_the_new_holders_lock(repo, tmp_path):
    sd = tmp_path / "sd"
    mine, _ = ws.acquire_lock(sd, "manual")
    put_lock(sd, token="f" * 32)                                                               # another run took the lock over
    assert mine.beat() is False and mine.lost.is_set()
    mine.release()
    assert ws._read_lock(sd / "lock")[0]["token"] == "f" * 32                                  # a foreign lock is not ours to delete
    again = ws.Lock(sd / "lock", "a" * 32, 1, ws._iso(), "manual")                              # the thread form: one tick, a tiny interval
    again.heartbeat(0.01)
    assert again.lost.wait(10)
    again._stop.set()
    wt = repo.merged_wt("st")
    rep = repo.sweep(apply=True, should_stop=lambda: True)
    assert has(rep, "STOPPED: the sweep lock was lost") and not has(rep, "REMOVED") and wt.exists() and "st" in repo.branches()


def test_w6_takeover_a_lock_taken_over_after_copy_1_stops_the_run_before_copy_2_and_keeps_the_new_holders_status(repo, monkeypatch):
    """F1/F8 (t-1764): the token is checked before EVERY copy by run_locked itself, not only by the heartbeat tick (30 s)."""
    a, b = repo.merged_wt("tk1"), repo.merged_wt("tk2")
    sd, new_holder = _sd(repo), "f" * 32
    original, state = ws.StatusFile.update, {"taken": False}

    def update_then_take_over(self, **fields):
        result = original(self, **fields)
        if fields.get("done") == 1 and not state["taken"]:                  # progress after copy 1: another run takes over now
            state["taken"] = True
            put_lock(sd, token=new_holder)
            (sd / "status.json").write_text(json.dumps({"state": "running", "token": new_holder, "done": 0}), encoding="utf-8")
        return result

    monkeypatch.setattr(ws.StatusFile, "update", update_then_take_over)
    lines = []
    run_body(repo, out=lines.append)
    assert state["taken"]
    assert sum(l.startswith("REMOVED") for l in lines) == 1 and [p.exists() for p in (a, b)].count(True) == 1
    assert any(l.startswith("STOPPED: the sweep lock was lost") for l in lines)
    assert _status(sd)["token"] == new_holder and _status(sd)["state"] == "running"         # no finished/crashed write over the new holder
    assert ws._read_lock(sd / "lock")[0]["token"] == new_holder                              # and its lock is not deleted


def test_w6_lost_lock_read_failure_is_tried_once_more_then_counts_as_not_ours(tmp_path, monkeypatch):
    sd = tmp_path / "sd"
    mine, _ = ws.acquire_lock(sd, "manual")
    real, calls = ws._read_lock, []

    def flaky(path):
        calls.append(1)
        return (None, None) if len(calls) == 1 else real(path)

    monkeypatch.setattr(ws, "_read_lock", flaky)
    assert mine.holds(0) is True and len(calls) == 2                                          # one transient miss does not stop a healthy run
    monkeypatch.setattr(ws, "_read_lock", lambda path: (None, None))
    assert mine.holds(0) is False                                                             # two misses: not ours


def test_w5_takeover_of_an_unreadable_stale_lock_reads_back_and_a_foreign_lock_is_put_back_not_overwritten(tmp_path, monkeypatch):
    sd = tmp_path / "sd"
    now = int(time.time())
    put_lock(sd, text="", mtime=now - ws.STALE_S - 1)                                          # empty: unreadable AND stale
    real_read, state = ws._read_lock, {"readback": 0}

    def another_run_created_it_meanwhile(path):
        if pathlib.Path(path).name.startswith("lock.stale-"):                                          # the read-back of the moved file
            state["readback"] += 1
            return {"token": "n" * 32, "pid": 2, "started": ws._iso(), "trigger": "manual"}, now
        return real_read(path)

    monkeypatch.setattr(ws, "_read_lock", another_run_created_it_meanwhile)
    lock, holder = ws.acquire_lock(sd, "manual", now=now)
    assert state["readback"] == 1 and lock is None and holder["token"] == "n" * 32             # read back although `seen` was None
    assert (sd / "lock").exists() or list(sd.glob("lock.stale-*"))                             # nothing was lost
    other = put_lock(sd, token="z" * 32)                                                       # a third contender's lock is in place
    moved = sd / "lock.stale-1-x"
    moved.write_text("old", encoding="utf-8")
    ws._put_back(moved, other)
    assert ws._read_lock(other)[0]["token"] == "z" * 32                                        # never overwritten


def test_w7_read_status_names_every_state(repo):
    sd, now = _sd(repo), time.time()
    assert ws.read_status(repo.main).kind == "none"
    sd.mkdir()
    for raw in ("", "{not json", json.dumps({"state": "dancing"}), json.dumps([1])):
        (sd / "status.json").write_text(raw)
        assert ws.read_status(repo.main).kind == "unreadable", raw
    base = {"token": "k" * 32, "trigger": "post-merge", "started": ws._iso(), "state": "running"}
    (sd / "status.json").write_text(json.dumps(base))
    put_lock(sd, token="k" * 32, mtime=now)
    assert ws.read_status(repo.main).kind == "running"
    put_lock(sd, token="z" * 32, mtime=now)                                                    # another token
    assert ws.read_status(repo.main).kind == "died"
    put_lock(sd, token="k" * 32, mtime=now - ws.STALE_S - 5)                                   # silent
    assert ws.read_status(repo.main).kind == "died"
    (sd / "lock").unlink()                                                                     # no lock at all
    assert ws.read_status(repo.main).kind == "died"
    for state in ("finished", "refused", "crashed", "not-started"):
        (sd / "status.json").write_text(json.dumps(dict(base, state=state, reason="why")))
        got = ws.read_status(repo.main)
        assert got.kind == state and got.data["trigger"] == "post-merge" and got.reason == "why"
    with pytest.raises(RuntimeError):
        ws.read_status(repo.tmp / "nothing")


def test_w8_launch_hands_the_main_copys_tool_to_spawn_with_the_token_and_an_environment_without_git_variables(repo, monkeypatch):
    with_tool(repo)
    monkeypatch.setenv("GIT_AUTHOR_NAME", "someone")
    assert any(k.startswith("GIT_") for k in os.environ)                                       # the control: the variable IS there
    spawn = Spawn()
    kind, text = ws.launch_background(repo.main, "post-merge", spawn=spawn)
    assert kind == "started" and "worktree sweep started in the background (log .git/worktree-sweep/run.log)" == text
    (argv, cwd, env), = spawn.calls
    token = ws._read_lock(_sd(repo) / "lock")[0]["token"]
    assert argv[0] == sys.executable and argv[2:6] == ["--background-run", "--token", token, "--repo"] and len(argv) == 7
    assert ws._key(argv[1]) == ws._key(repo.main / "tools" / "worktree_sweep.py") and ws._key(argv[6]) == ws._key(repo.main)
    assert ws._key(cwd) == ws._key(repo.main) and not [k for k in env if k.startswith("GIT_")] and "PATH" in env
    status = _status(_sd(repo))
    assert status["state"] == "running" and status["token"] == token and status["pid"] is None and status["trigger"] == "post-merge"


def test_w8_spawn_detached_windows_flags_and_the_retry_without_breakaway(monkeypatch):
    calls = []

    def popen(argv, **kw):
        calls.append(kw)
        if len(calls) == 1:
            raise OSError("[WinError 5] Access is denied")
        return type("P", (), {"pid": 77})()

    monkeypatch.setattr(ws, "_IS_WINDOWS", True)
    monkeypatch.setattr(ws.subprocess, "Popen", popen)
    assert ws.spawn_detached(["x"], "C:/d", {"A": "1"}) == 77
    first, second = calls
    assert first["creationflags"] == 0x8 | 0x200 | 0x01000000 and second["creationflags"] == 0x8 | 0x200
    for kw in calls:
        assert kw["stdin"] == kw["stdout"] == kw["stderr"] == subprocess.DEVNULL and kw["close_fds"] is True and kw["env"] == {"A": "1"}
    calls.clear()
    monkeypatch.setattr(ws, "_IS_WINDOWS", False)
    monkeypatch.setattr(ws.subprocess, "Popen", lambda argv, **kw: calls.append(kw) or type("P", (), {"pid": 5})())
    assert ws.spawn_detached(["x"], "/d", {}) == 5 and calls[0]["start_new_session"] is True and "creationflags" not in calls[0]


def test_w8_when_both_launch_forms_fail_the_status_says_not_started_and_the_lock_is_released(repo, monkeypatch):
    with_tool(repo)

    def popen(argv, **kw):
        raise OSError("no process for you")

    def real_spawn_with_a_dead_popen(argv, cwd, env):                 # Popen is replaced ONLY around the launch: git itself needs it
        with monkeypatch.context() as m:
            m.setattr(ws, "_IS_WINDOWS", True)
            m.setattr(ws.subprocess, "Popen", popen)
            return ws.spawn_detached(argv, cwd, env)

    kind, text = ws.launch_background(repo.main, "piles-close", spawn=real_spawn_with_a_dead_popen)
    assert kind == "failed" and text.startswith("background sweep not started (OSError: no process for you")
    status = _status(_sd(repo))
    assert status["state"] == "not-started" and "no process for you" in status["reason"] and not (_sd(repo) / "lock").exists()
    assert ws.read_status(repo.main).kind == "not-started"
    kind, text = ws.launch_background(repo.main, "piles-close", spawn=Spawn())               # the lock is free again: a launch works
    assert kind == "started"


def test_w8_a_state_directory_that_cannot_be_made_is_failed(repo):
    with_tool(repo)
    (repo.main / ".git" / "worktree-sweep").write_text("a file where the directory should be")
    spawn = Spawn()
    kind, text = ws.launch_background(repo.main, "post-merge", spawn=spawn)
    assert kind == "failed" and text.startswith("background sweep not started (cannot make ") and spawn.calls == []


def test_w9_a_launch_from_a_linked_worktree_a_non_repository_or_a_main_without_the_tool_is_refused(repo, tmp_path):
    spawn = Spawn()
    linked = repo.add_wt("lk")
    with_tool(repo)
    kind, text = ws.launch_background(linked, "piles-close", spawn=spawn)
    assert kind == "refused" and "runs from the main checkout" in text and "this is the linked worktree" in text
    assert not _sd(repo).exists() and spawn.calls == []                                        # no lock was made
    assert ws.launch_background(tmp_path / "nothing", "post-merge", spawn=spawn)[0] == "refused"
    (repo.main / "tools" / "worktree_sweep.py").unlink()
    kind, text = ws.launch_background(repo.main, "post-merge", spawn=spawn)
    assert kind == "refused" and text.startswith("tools/worktree_sweep.py not found in ") and spawn.calls == [] and not _sd(repo).exists()


def test_w10_a_launch_while_a_sweep_runs_is_busy_leaves_rerun_and_starts_nothing(repo):
    with_tool(repo)
    held, _ = ws.acquire_lock(_sd(repo), "manual")
    spawn = Spawn()
    kind, text = ws.launch_background(repo.main, "post-merge", spawn=spawn)
    assert kind == "busy" and text.startswith("a worktree sweep is already running since ") and "(manual); a second pass is queued" in text
    assert (_sd(repo) / "rerun").exists() and spawn.calls == []
    assert ws._read_lock(_sd(repo) / "lock")[0]["token"] == held.token                         # the holder is untouched


def test_w11_the_full_run_removes_every_merged_copy_without_a_limit_and_keeps_the_young_and_the_changed(repo):
    names = ["q%d" % i for i in range(6)]
    for nm in names:
        wt = repo.add_wt(nm)
        repo.commit(wt, nm + ".txt", nm)
    git(repo.main, "merge", "--no-ff", "-m", "octopus", *names)
    older = repo.merged_wt("older")                                                          # merged by an earlier merge, not this one
    young = repo.add_wt("young")                                                             # no commits of its own, made just now
    changed = repo.merged_wt("changed")
    (changed / "work.txt").write_text("real work")
    rep = run_body(repo)
    removed = [l for l in rep.lines if l.startswith("REMOVED ")]
    assert len(removed) == 7 and not has(rep, "deferred") and not older.exists()
    assert all(not (repo.wts / n).exists() for n in names)
    keeps = [l for l in rep.lines if l.startswith("KEEP ")]
    assert any("no own commits, active" in l for l in keeps) and any("real changes: work.txt" in l for l in keeps)
    assert young.exists() and changed.exists()
    status = _status(_sd(repo))
    assert status["state"] == "finished" and status["removed"] == 7 and status["kept"] == 2 and status["registered"] == 9
    assert status["passes"] == 1 and status["pid"] == os.getpid() and "judged against main at" in (_sd(repo) / "run.log").read_text()


@pytest.mark.parametrize("creates_in,passes,left", [({1}, 2, False), ({1, 2}, 3, False), ({1, 2, 3}, 3, True)])
def test_w12_rerun_makes_another_pass_up_to_MAX_PASSES_and_the_rest_is_said(repo, monkeypatch, creates_in, passes, left):
    repo.add_wt("alive")                                                                     # one kept copy: every pass has a copy to see
    real, n = ws.sweep, []

    def wrapped(root, **kw):
        n.append(1)
        inner = kw["progress"]

        def progress(done, registered):
            if len(n) in creates_in:
                (_sd(repo) / "rerun").write_text("x")
            return inner(done, registered)

        kw["progress"] = progress
        return real(root, **kw)

    monkeypatch.setattr(ws, "sweep", wrapped)
    run_body(repo)
    log = (_sd(repo) / "run.log").read_text(encoding="utf-8")
    assert len(n) == passes and _status(_sd(repo))["passes"] == passes
    assert ("rerun left for the next trigger (3 passes done)" in log) == left and (_sd(repo) / "rerun").exists() == left


class Hook:
    """A runner that does something to the repository right BEFORE the n-th `worktree list` of the sweep (n=1 is the start)."""

    def __init__(self, n, action):
        self.n, self.action, self.count = n, action, 0

    def __call__(self, root, *args, timeout=120, stderr=False):
        if args[:2] == ("worktree", "list"):
            self.count += 1
            if self.count == self.n:
                self.action()
        return gitcmd.git(root, *args, timeout=timeout, stderr=stderr)


@pytest.mark.parametrize("detached", [False, True])
def test_w13_a_copy_is_judged_at_its_turn_a_new_commit_a_vanished_and_a_locked_copy(repo, detached):
    a = repo.merged_wt("a1")
    b = repo.add_wt("b1", detach=detached)
    c = repo.merged_wt("c1")
    d = repo.merged_wt("d1")

    def meanwhile():                                                                         # right after the start, before the first copy
        repo.commit(b, "late.txt", "a commit made while the sweep runs")
        git(repo.main, "worktree", "remove", str(c))
        git(repo.main, "worktree", "lock", "--reason", "agent started", str(d))

    rep = repo.sweep(apply=True, runner=Hook(2, meanwhile))
    new_head = git(b, "rev-parse", "HEAD")
    assert not a.exists() and has(rep, "REMOVED")
    assert any(l.startswith('KEEP "') and l.endswith(": unmerged (1 commits not in origin/main)") and "b1" in l for l in rep.lines)
    assert b.exists() and (b / "late.txt").exists()
    git(repo.main, "cat-file", "-e", new_head + "^{commit}")                                 # the commit is reachable: nothing lost
    assert any(l.startswith('GONE "') and l.endswith(": no longer registered") and "c1" in l for l in rep.lines)
    assert any(l.startswith('KEEP "') and l.endswith(": locked (agent started)") for l in rep.lines) and d.exists()
    assert rep.registered == 4 and rep.done == 1 and rep.kept == 2                           # the vanished copy is in NO sum
    assert rep.lines[-1] == "worktree_sweep: 4 registered, 1 removed, 2 kept, 0 failed"


def test_e22_a_copy_made_after_the_start_is_not_this_passes_business(repo):
    repo.merged_wt("a1")
    made = []
    rep = repo.sweep(apply=True, runner=Hook(2, lambda: made.append(repo.add_wt("newborn"))))
    assert made and made[0].exists() and "newborn" in repo.branches()                       # an agent that began during the run is safe
    assert not any("newborn" in l for l in rep.lines) and rep.registered == 1 and has(rep, "REMOVED")


def test_w14_a_registration_that_goes_prunable_during_the_run_is_archived_before_the_prune(repo):
    repo.merged_wt("a1")
    late = repo.add_wt("d1", detach=True)
    head = repo.commit(late, "d.txt", "unmerged detached work")
    gone = repo.merged_wt("p1")
    shutil.rmtree(gone)                                                                      # prunable from the start: the prune will run
    # sweep calls: 1 start, then one per copy (3), then ONE before the prune = the 5th
    rep = repo.sweep(apply=True, runner=Hook(5, lambda: shutil.rmtree(late)))
    assert has(rep, "PRUNABLE") and not has(rep, "KEEP prune")
    assert _archived(repo, head)
    git(repo.main, "cat-file", "-e", head + "^{commit}")
    assert not (repo.main / ".git" / "worktrees").exists() or not list((repo.main / ".git" / "worktrees").iterdir())       # the prune ran


def test_w15_post_merge_starts_the_background_sweep_once_only_on_main_in_the_main_checkout(repo):
    with_tool(repo)
    repo.merged_wt("g1")
    spawn = Spawn()
    rep = ws.post_merge(repo.main, "0", spawn=spawn)
    assert len(spawn.calls) == 1 and rep.lines == ["post-merge: worktree sweep started in the background (log .git/worktree-sweep/run.log)"]
    for flag, orig in (("1", True), ("0", False)):                                           # a squash merge; no ORIG_HEAD at all
        shutil.rmtree(_sd(repo))
        if not orig:
            (repo.main / ".git" / "ORIG_HEAD").unlink(missing_ok=True)
        before = len(spawn.calls)
        assert ws.post_merge(repo.main, flag, spawn=spawn).lines and len(spawn.calls) == before + 1
    shutil.rmtree(_sd(repo))
    linked = repo.add_wt("g2")
    other = Spawn()
    assert ws.post_merge(linked, "0", spawn=other).lines == [] and other.calls == []
    git(repo.main, "checkout", "-b", "other")
    assert ws.post_merge(repo.main, "0", spawn=other).lines == [] and other.calls == [] and not _sd(repo).exists()


def test_w15_post_merge_names_a_launch_that_did_not_happen_with_its_door(repo):
    with_tool(repo)
    rep = ws.post_merge(repo.main, "0", spawn=Spawn(OSError("denied")))
    assert rep.lines == ["post-merge: background sweep not started (OSError: denied) -- python tools/worktree_sweep.py --apply"]
    assert ws.post_merge(repo.main, "0", spawn=Spawn()).lines[0].startswith("post-merge: worktree sweep started")
    assert ws.post_merge(repo.main, "0", spawn=Spawn()).lines[0].startswith("post-merge: a worktree sweep is already running")


def test_w16_a_manual_apply_is_refused_while_a_sweep_runs_and_runs_under_its_own_lock_otherwise(repo, capsys):
    wt = repo.merged_wt("m1")
    held, _ = ws.acquire_lock(_sd(repo), "post-merge")
    assert ws.main(["--apply", "--repo", str(repo.main)]) == 1
    out = capsys.readouterr().out
    assert "a sweep is already running since" in out and "(post-merge, pid %d)" % os.getpid() in out and ".git/worktree-sweep/run.log" in out
    assert "after 5 min without a heartbeat; nothing removed" in out and wt.exists()
    held.release()
    assert ws.main(["--apply", "--repo", str(repo.main)]) == 0
    out = capsys.readouterr().out
    status = _status(_sd(repo))
    assert status["trigger"] == "manual" and status["state"] == "finished" and not wt.exists() and not (_sd(repo) / "lock").exists()
    assert "judged against origin/main at " in out and status["ref"] == "origin/main"
    assert (_sd(repo) / "run.log").read_text(encoding="utf-8").splitlines()[1:] == out.splitlines()   # the journal = the console


def test_w16_a_dry_run_while_a_sweep_runs_says_so_first_and_takes_no_lock(repo, capsys):
    repo.merged_wt("m2")
    now = time.time()
    _sd(repo).mkdir()
    (_sd(repo) / "status.json").write_text(json.dumps({"state": "running", "token": "k" * 32, "trigger": "post-merge", "started": "2026-11-03T10:00:00"}))
    put_lock(_sd(repo), token="k" * 32, mtime=now)
    assert ws.main(["--repo", str(repo.main)]) == 0
    first = capsys.readouterr().out.splitlines()[0]
    assert first == "NOTE: a sweep is running since 2026-11-03T10:00:00 (post-merge) -- copies it is removing may still be listed"
    assert ws._read_lock(_sd(repo) / "lock")[0]["token"] == "k" * 32 and (repo.wts / "m2").exists()


def test_w17_an_exception_in_the_run_is_a_crashed_status_and_the_lock_is_released(repo, monkeypatch):
    def boom(root, **kw):
        raise ValueError("the line\nsecond line")

    monkeypatch.setattr(ws, "sweep", boom)
    run_body(repo)
    status = _status(_sd(repo))
    assert status["state"] == "crashed" and status["reason"] == "ValueError: the line" and not (_sd(repo) / "lock").exists()
    assert ws.read_status(repo.main).kind == "crashed" and "CRASHED ValueError" in (_sd(repo) / "run.log").read_text(encoding="utf-8")


def test_w18_a_reference_that_does_not_resolve_is_a_refused_status_and_nothing_is_removed(repo, monkeypatch):
    wt = repo.merged_wt("r1")
    monkeypatch.setattr(ws, "BACKGROUND_REF", "nowhere")
    lock, _ = ws.acquire_lock(_sd(repo), "post-merge")
    ws.run_locked(_ctx(repo), lock, "post-merge")
    status = _status(_sd(repo))
    assert status["state"] == "refused" and "does not resolve" in status["reason"] and wt.exists() and "r1" in repo.branches()
    assert not (_sd(repo) / "lock").exists()


def test_w20_source_census_no_process_kill_no_limits_no_deferred_line():
    tree = ast.parse(SOURCE)
    funcs = {n.name for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)}
    assert {"spawn_detached", "acquire_lock"} <= funcs                                       # positive control: the parse sees the new code
    attrs = {(n.value.id, n.attr) for n in ast.walk(tree) if isinstance(n, ast.Attribute) and isinstance(n.value, ast.Name)}
    assert ("os", "replace") in attrs and ("os", "kill") not in attrs                        # (control: another os.* call IS found)
    names = {n.id for n in ast.walk(tree) if isinstance(n, ast.Name)} | {n.arg for n in ast.walk(tree) if isinstance(n, ast.arg)}
    names |= {k.arg for n in ast.walk(tree) if isinstance(n, ast.Call) for k in n.keywords} | funcs
    names |= {n.attr for n in ast.walk(tree) if isinstance(n, ast.Attribute)}
    assert "STALE_S" in names                                                                # control: a name of the new code IS found
    for gone in ("N_REMOVALS", "S_SECONDS", "MIN_CALL_TIMEOUT", "max_removals", "only_heads", "budget_s", "POST_MERGE_REF"):
        assert gone not in names, gone
    constants = [n.value for n in ast.walk(tree) if isinstance(n, ast.Constant) and isinstance(n.value, str)]
    assert not [c for c in constants if "deferred:" in c] and any("worktree sweep started" in c for c in constants)
    assert "os.kill" not in SOURCE


def test_w21_the_journal_is_written_line_by_line_while_the_run_goes_on(repo):
    repo.add_wt("alive")
    seen = []

    def out(text):
        seen.append((text, (_sd(repo) / "run.log").read_text(encoding="utf-8")))

    run_body(repo, out=out)
    assert len(seen) >= 3
    first, log_at_first = seen[0]
    assert first.startswith("judged against main at ") and log_at_first.splitlines()[-1] == first    # the line is in the file as `out` hears it
    second, log_at_second = seen[1]
    assert log_at_second.splitlines()[-2:] == [first, second] and "worktree_sweep: 1 registered" not in log_at_second


def test_w22_the_previous_journal_becomes_prev_log_and_a_failed_rotation_appends_after_a_separator(repo, monkeypatch):
    run_body(repo)
    first = (_sd(repo) / "run.log").read_text(encoding="utf-8")
    run_body(repo)
    assert (_sd(repo) / "prev.log").read_text(encoding="utf-8") == first
    second = (_sd(repo) / "run.log").read_text(encoding="utf-8")
    real = os.replace

    def refuse_prev(src, dst):
        if pathlib.Path(dst).name == "prev.log":
            raise PermissionError("prev.log is open")
        return real(src, dst)

    monkeypatch.setattr(ws.os, "replace", refuse_prev)
    run_body(repo)
    third = (_sd(repo) / "run.log").read_text(encoding="utf-8")
    assert third.startswith(second + "----\n") and third.count("worktree_sweep: manual run") == 2


def test_w23_a_status_that_cannot_be_written_is_a_warn_line_and_the_sweep_goes_on(repo, monkeypatch):
    wt = repo.merged_wt("sw")
    real = os.replace

    def refuse_status(src, dst):
        if pathlib.Path(dst).name == "status.json":
            raise PermissionError("a reader holds status.json")
        return real(src, dst)

    monkeypatch.setattr(ws.os, "replace", refuse_status)
    rep = run_body(repo)
    assert "WARN status not written (PermissionError: a reader holds status.json)" in (_sd(repo) / "run.log").read_text(encoding="utf-8")
    assert has(rep, "REMOVED") and not wt.exists() and not (_sd(repo) / "lock").exists()


def test_w24_a_background_child_that_does_not_hold_its_lock_removes_nothing(repo):
    wt = repo.merged_wt("nl")
    held, _ = ws.acquire_lock(_sd(repo), "post-merge")
    assert ws.main(["--background-run", "--token", "x" * 32, "--repo", str(repo.main)]) == 0
    assert "the lock is not ours -- nothing done" in (_sd(repo) / "run.log").read_text(encoding="utf-8")
    assert wt.exists() and "nl" in repo.branches() and ws._read_lock(_sd(repo) / "lock")[0]["token"] == held.token
    held.release()
    assert ws.main(["--background-run", "--token", held.token, "--repo", str(repo.main)]) == 0           # no lock at all: the same
    assert wt.exists() and (_sd(repo) / "run.log").read_text(encoding="utf-8").count("the lock is not ours") == 2


def test_w24_a_background_child_with_its_own_token_runs_and_records_its_own_pid(repo):
    wt = repo.merged_wt("ow")
    lock, _ = ws.acquire_lock(_sd(repo), "post-merge")
    lock_pid_before = ws._read_lock(_sd(repo) / "lock")[0]["pid"]
    assert ws.main(["--background-run", "--token", lock.token, "--repo", str(repo.main)]) == 0
    status = _status(_sd(repo))
    assert status["state"] == "finished" and status["trigger"] == "post-merge" and not wt.exists() and lock_pid_before == os.getpid()


def test_w25_no_copies_is_a_finished_run_with_zero_registered(repo):
    rep = run_body(repo)
    assert rep.exit_code == 0 and rep.lines[-1] == "worktree_sweep: 0 registered, 0 removed, 0 kept, 0 failed"
    status = _status(_sd(repo))
    assert status["state"] == "finished" and status["registered"] == 0 and status["removed"] == 0


def test_w26_a_reason_is_cut_to_200_characters_in_the_status(repo):
    sf = ws.StatusFile(repo.tmp / "sf")
    (repo.tmp / "sf").mkdir()
    assert sf.update(state="crashed", reason="x" * 500) is True
    assert len(_status(repo.tmp / "sf")["reason"]) == ws.STATUS_REASON_MAX == 200


def test_the_lock_is_one_freshness_test_for_the_launcher_and_the_reader():
    callers = [n.name for n in ast.walk(ast.parse(SOURCE)) if isinstance(n, ast.FunctionDef)
               and any(isinstance(c, ast.Call) and getattr(c.func, "id", "") == "_lock_stale" for c in ast.walk(n))]
    assert sorted(callers) == ["acquire_lock", "read_status"]                               # axis 25: one test, two readers
