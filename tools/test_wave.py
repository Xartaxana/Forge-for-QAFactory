"""Tests of tools/wave.py (offload spec r2 §3.C3, F-T1): a temp bare "origin", a root clone and a dev clone; no network.
Row ids carry the E-C3-n of the spec."""
import subprocess
import sys
import threading
import time
from pathlib import Path
from types import SimpleNamespace

import pytest

TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))
import journal_lock as jl  # noqa: E402
import wave  # noqa: E402

REL = "logs/journal/dev.jsonl"
L1, L2, L3 = (b'{"n":1}\n', b'{"n":2}\n', b'{"n":3}\n')
PILES = ("import sys, pathlib\nroot = pathlib.Path(__file__).resolve().parent.parent\n"
         "if (root / 'plans' / 'refuse').exists():\n    print('refused: nope'); sys.exit(1)\n"
         "(root / 'plans').mkdir(exist_ok=True)\n(root / 'plans' / 'node.txt').write_text(' '.join(sys.argv[1:]) + '\\n', encoding='utf-8')\n")


def g(cwd, *args, check=True):
    p = subprocess.run(["git", "-C", str(cwd), *args], capture_output=True, text=True, encoding="utf-8")
    assert p.returncode == 0 or not check, p.stderr
    return p.stdout.strip()


def put(cwd, files, msg="c"):
    for rel, text in files.items():
        f = Path(cwd, rel)
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_bytes(text if isinstance(text, bytes) else text.encode())
        g(cwd, "add", rel)
    g(cwd, "commit", "-q", "-m", msg)


@pytest.fixture
def env(tmp_path, monkeypatch):
    for k in ("NAME", "EMAIL"):
        for who in ("AUTHOR", "COMMITTER"):
            monkeypatch.setenv("GIT_%s_%s" % (who, k), "t" if k == "NAME" else "t@t")
    origin, root, dev = tmp_path / "origin.git", tmp_path / "root", tmp_path / "dev"
    g(tmp_path, "init", "-q", "--bare", "-b", "main", str(origin))
    g(tmp_path, "clone", "-q", str(origin), str(dev))
    g(dev, "checkout", "-q", "-b", "main")
    put(dev, {"README": "a\n", REL: L1, "tools/piles.py": PILES,
              ".gitattributes": "logs/journal/*.jsonl text eol=lf\n"})
    g(dev, "push", "-q", "origin", "main")
    g(tmp_path, "clone", "-q", str(origin), str(root))
    e = SimpleNamespace(origin=origin, root=root, dev=dev, rel=REL, tmp=tmp_path)
    monkeypatch.setattr(wave, "journal_rel", lambda r: e.rel)
    monkeypatch.setattr(wave, "LOCK_WAIT", 1.0)
    return e


def branch(e, name, files, base="origin/main"):
    g(e.dev, "fetch", "-q", "origin")
    g(e.dev, "checkout", "-q", "-B", name, base)
    put(e.dev, files, name)
    g(e.dev, "push", "-q", "origin", name)
    g(e.dev, "checkout", "-q", "--detach")


def push_main(e, files):
    g(e.dev, "fetch", "-q", "origin")
    g(e.dev, "checkout", "-q", "--detach", "origin/main")
    put(e.dev, files, "main moves")
    g(e.dev, "push", "-q", "origin", "HEAD:main")


def go(e, name, node=None, ci=None, task="t-868"):
    out = []
    w = wave.Wave(e.root, name, task, node, ci=ci or (lambda r, s: "success"), out=out.append)
    return w.run(), "\n".join(out), w


def snap(e):
    r = e.root
    return (g(r, "status", "--porcelain"), g(r, "for-each-ref", "refs/heads"), g(r, "worktree", "list"),
            g(r, "stash", "list"), g(r, "rev-parse", "HEAD"), (r / REL).read_bytes())


def origin_main(e):
    return g(e.origin, "rev-parse", "main")


def blob(e, rel, ref="main"):
    p = subprocess.run(["git", "-C", str(e.origin), "show", "%s:%s" % (ref, rel)], capture_output=True)
    return p.stdout if p.returncode == 0 else None


def test_ff_merge_refreshes_root_and_deletes_branch(env):
    branch(env, "b1", {"f.txt": "x\n"})
    rc, out, _ = go(env, "b1")
    assert rc == 0 and "forge-check: success" in out and "branch: deleted" in out and "root: refreshed" in out
    assert g(env.origin, "rev-list", "--merges", "main") == "" and blob(env, "f.txt") == b"x\n"
    assert (env.root / "f.txt").read_text() == "x\n" and g(env.origin, "branch", "--list", "b1") == ""
    assert g(env.root, "worktree", "list").count("\n") == 0 and g(env.root, "rev-parse", "HEAD") == origin_main(env)


def test_no_ff_merge_message(env):
    branch(env, "b2", {"f.txt": "x\n"})
    push_main(env, {"g.txt": "y\n"})
    rc, out, w = go(env, "b2", task="t-901")
    assert rc == 0 and g(env.origin, "log", "-1", "--format=%s", "main") == "wave: merge b2 (t-901)"
    assert len(g(env.origin, "rev-list", "--merges", "main").split()) == 1 and w.sha == origin_main(env)


def test_conflict_refuses_names_paths_and_changes_nothing_E_C3_8(env):
    branch(env, "b3", {"README": "branch\n"})
    push_main(env, {"README": "main\n"})
    before, main_before = snap(env), origin_main(env)
    rc, out, _ = go(env, "b3")
    assert rc == 2 and "README" in out and origin_main(env) == main_before
    assert snap(env) == before and not list((env.root / ".claude" / "worktrees").glob("wave-*"))


def test_unknown_branch_refuses_and_changes_nothing_E_C3_8(env):
    before = snap(env)
    rc, out, _ = go(env, "nope")
    assert rc == 2 and "step 3" in out and snap(env) == before
    assert not list((env.root / ".claude" / "worktrees").glob("wave-*"))


def test_forge_check_is_information_only(env):
    branch(env, "b4", {"f.txt": "x\n"})
    rc, out, _ = go(env, "b4", ci=lambda r, s: "failure")
    assert rc == 0 and "forge-check: failure" in out and blob(env, "f.txt") == b"x\n"


@pytest.mark.parametrize("answer,state", [
    (("101 success t abcd1234 push", "9 forge-check success"), "success"),
    (("101 completed t abcd1234 push", "9 forge-check failure"), "failure"),
    (("101 in_progress t abcd1234 push", "9 other success"), "pending"),
    (("101 success t ffffffff push", ""), "unknown"),
    (None, "unknown")])
def test_forge_check_state_reads_ci_read(monkeypatch, answer, state):
    def fake(argv, **kw):
        if answer is None:
            return subprocess.CompletedProcess(argv, 2, b"", b"no token")
        text = answer[0] if argv[3] == "pipelines" else answer[1]
        return subprocess.CompletedProcess(argv, 0, text.encode(), b"")
    monkeypatch.setattr(wave.subprocess, "run", fake)
    assert wave.forge_check_state(Path("."), "abcd1234" + "0" * 32) == state


def test_forge_check_state_unknown_when_ci_read_raises(monkeypatch):
    def boom(*a, **k):
        raise OSError("no python")
    monkeypatch.setattr(wave.subprocess, "run", boom)
    assert wave.forge_check_state(Path("."), "a" * 40) == "unknown"


def test_non_ff_push_retries_from_the_merge(env, monkeypatch):
    branch(env, "b5", {"f.txt": "x\n"})
    branch(env, "other", {"o.txt": "o\n"})
    real, calls = wave.Wave.push, []

    def moved_once(self, w, step):
        calls.append(step)
        if len(calls) == 1:
            push_main(env, {"g.txt": "y\n"})
        return real(self, w, step)
    monkeypatch.setattr(wave.Wave, "push", moved_once)
    rc, out, _ = go(env, "b5")
    assert rc == 0 and calls[:2] == ["step 7", "step 7"]
    assert blob(env, "f.txt") == b"x\n" and blob(env, "g.txt") == b"y\n"


def test_main_moving_three_times_refuses(env, monkeypatch):
    branch(env, "b6", {"f.txt": "x\n"})
    monkeypatch.setattr(wave.Wave, "push", lambda self, w, step: "moved")
    before = origin_main(env)
    rc, out, _ = go(env, "b6")
    assert rc == 2 and "main moved 3 times during the merge" in out and origin_main(env) == before
    assert not list((env.root / ".claude" / "worktrees").glob("wave-*"))


def test_dirty_root_still_merges_and_is_untouched_E_C3_1(env):
    branch(env, "b7", {"f.txt": "x\n"})
    (env.root / "README").write_text("dirty\n")
    rc, out, _ = go(env, "b7")
    assert rc == 0 and blob(env, "f.txt") == b"x\n"
    assert "root checkout not refreshed: tracked changes beyond the journal: README" in out
    assert (env.root / "README").read_text() == "dirty\n" and not (env.root / "f.txt").exists()
    assert g(env.root, "stash", "list") == ""


def test_journal_is_committed_and_root_bytes_identical(env):
    branch(env, "b8", {"f.txt": "x\n"})
    (env.root / REL).write_bytes(L1 + L2)
    rc, out, _ = go(env, "b8", task="t-870")
    assert rc == 0 and blob(env, REL) == L1 + L2 and "root: refreshed" in out
    assert g(env.origin, "log", "-1", "--format=%s", "main") == "journal: wave b8 (t-870)"
    assert (env.root / REL).read_bytes() == L1 + L2 and g(env.root, "status", "--porcelain") == ""
    assert not list(jl.lock_dir(env.root).glob("wave-copy-*"))


def test_journal_not_prefix_is_not_committed_and_root_not_refreshed(env):
    branch(env, "b9", {"f.txt": "x\n"})
    push_main(env, {REL: L1 + L3})
    (env.root / REL).write_bytes(L1 + L2)
    rc, out, _ = go(env, "b9")
    assert rc == 0 and "journal not committed: origin holds lines the root lacks" in out
    assert blob(env, REL) == L1 + L3 and (env.root / REL).read_bytes() == L1 + L2
    assert "root checkout not refreshed: origin's journal is not a prefix of the root's" in out


def test_already_merged_still_runs_node_and_cleanup_E_C3_5(env):
    branch(env, "b10", {"f.txt": "x\n"})
    g(env.dev, "push", "-q", "origin", "origin/b10:refs/heads/main")
    rc, out, w = go(env, "b10", node=("pile", "2", "N-1"))
    assert rc == 0 and "nothing to merge" in out and "branch: deleted" in out and g(env.origin, "branch", "--list", "b10") == ""
    assert blob(env, "plans/node.txt").decode().split() == ["status", "pile", "2", "N-1", "--set", "принято", "--hash",
                                                            w.sha, "--task", "t-868"]


def test_node_status_is_committed_with_the_merge_hash(env):
    branch(env, "b11", {"f.txt": "x\n"})
    push_main(env, {"g.txt": "y\n"})
    rc, out, w = go(env, "b11", node=("pile", "1", "N-2"))
    assert rc == 0 and "node: pile 1 N-2" in out, out
    assert g(env.origin, "log", "-1", "--format=%s", "main").startswith("piles: pile 1 N-2")
    assert w.sha in blob(env, "plans/node.txt").decode() and w.sha == g(env.origin, "rev-parse", "main~1")


def test_piles_refusal_keeps_the_pushed_merge_and_prints_the_command_E_C3_7(env):
    push_main(env, {"plans/refuse": "x\n"})
    branch(env, "b12", {"f.txt": "x\n"})
    rc, out, w = go(env, "b12", node=("pile", "1", "N-3"))
    assert rc == 1 and "refused: nope" in out and "run by hand: python -B tools/piles.py status pile 1 N-3" in out
    assert blob(env, "f.txt") == b"x\n" and w.pushed
    assert g(env.origin, "branch", "--list", "b12") == ""


def test_two_waves_in_a_row(env):
    branch(env, "w1", {"f1.txt": "1\n"})
    branch(env, "w2", {"f2.txt": "2\n"})
    (env.root / REL).write_bytes(L1 + L2)
    assert go(env, "w1")[0] == 0 and (env.root / REL).read_bytes() == L1 + L2
    (env.root / REL).write_bytes(L1 + L2 + L3)
    rc, out, _ = go(env, "w2")
    assert rc == 0 and "root: refreshed" in out and (env.root / "f1.txt").exists() and (env.root / "f2.txt").exists()
    assert (env.root / REL).read_bytes() == L1 + L2 + L3 and blob(env, REL) == L1 + L2 + L3
    assert g(env.root, "rev-parse", "HEAD") == origin_main(env) and g(env.root, "status", "--porcelain") == ""


def test_concurrent_appender_during_step_9_loses_no_line_E_C3_11(env, monkeypatch):
    branch(env, "b13", {"f.txt": "x\n"})
    (env.root / REL).write_bytes(L1 + L2)
    done = []

    def appender():
        with jl.machine_lock("journal", 10, repo=env.root):
            with open(env.root / REL, "ab") as f:
                f.write(L3)
        done.append(1)

    def hook(name):
        if name == "step9-locked":
            t = threading.Thread(target=appender)
            t.start()
            time.sleep(0.4)
            assert not done                       # it waits on the lock while the dance runs
            hook.thread = t
    monkeypatch.setattr(wave, "_hook", hook)
    rc, out, _ = go(env, "b13")
    hook.thread.join(10)
    assert rc == 0 and "root: refreshed" in out and done
    assert (env.root / REL).read_bytes() == L1 + L2 + L3 and blob(env, REL) == L1 + L2
    assert not list(jl.lock_dir(env.root).glob("wave-copy-*"))


def test_root_on_another_branch_is_not_refreshed_E_C3_9(env):
    branch(env, "b14", {"f.txt": "x\n"})
    g(env.root, "checkout", "-q", "-b", "side")
    rc, out, _ = go(env, "b14")
    assert rc == 0 and "root checkout not refreshed: the root is not on main (side)" in out
    assert g(env.root, "symbolic-ref", "--short", "HEAD") == "side" and not (env.root / "f.txt").exists()
    assert blob(env, "f.txt") == b"x\n"


def test_journal_absent_in_root_head_is_removed_and_restored_E_C3_14(env):
    env.rel = "logs/journal/newdev.jsonl"
    branch(env, "b15", {"f.txt": "x\n"})
    (env.root / env.rel).write_bytes(L1 + L2)
    rc, out, _ = go(env, "b15")
    assert rc == 0 and "root: refreshed" in out
    assert (env.root / env.rel).read_bytes() == L1 + L2 and blob(env, env.rel) == L1 + L2
    assert g(env.root, "status", "--porcelain") == ""


def test_failed_refresh_restores_journal_and_names_git_E_C3_10(env):
    branch(env, "b16", {"f.txt": "x\n"})
    (env.root / "f.txt").write_text("untracked in the way\n")
    (env.root / REL).write_bytes(L1 + L2)
    rc, out, _ = go(env, "b16")
    assert rc == 0 and "root checkout not refreshed:" in out and "f.txt" in out
    assert (env.root / REL).read_bytes() == L1 + L2 and (env.root / "f.txt").read_text() == "untracked in the way\n"
    assert not list(jl.lock_dir(env.root).glob("wave-copy-*"))


def test_restore_mismatch_keeps_the_copy_exit_1(env, monkeypatch):
    branch(env, "b17", {"f.txt": "x\n"})
    (env.root / REL).write_bytes(L1 + L2)
    shas = iter(["before", "after"])
    monkeypatch.setattr(wave, "_sha", lambda d: next(shas))
    rc, out, _ = go(env, "b17")
    assert rc == 1 and "JOURNAL RESTORE MISMATCH: copy kept at" in out
    assert list(jl.lock_dir(env.root).glob("wave-copy-*"))


def test_branch_in_clean_worktree_is_removed_E_C3_12(env):
    branch(env, "b18", {"f.txt": "x\n"})
    g(env.root, "fetch", "-q", "origin")
    g(env.root, "branch", "b18", "origin/b18")
    wt = env.tmp / "wt18"
    g(env.root, "worktree", "add", "-q", str(wt), "b18")
    rc, out, _ = go(env, "b18")
    assert rc == 0 and "branch: deleted" in out and not wt.exists()
    assert g(env.root, "branch", "--list", "b18") == ""


def test_branch_in_dirty_worktree_is_kept_E_C3_12(env):
    branch(env, "b19", {"f.txt": "x\n"})
    g(env.root, "fetch", "-q", "origin")
    g(env.root, "branch", "b19", "origin/b19")
    wt = env.tmp / "wt19"
    g(env.root, "worktree", "add", "-q", str(wt), "b19")
    (wt / "README").write_text("dirty\n")
    rc, out, _ = go(env, "b19")
    assert rc == 0 and "branch: kept, checked out in" in out and "(dirty)" in out and wt.exists()
    assert g(env.root, "branch", "--list", "b19") != "" and blob(env, "f.txt") == b"x\n"


def test_unrefreshed_root_deletes_a_merged_local_branch_by_update_ref(env):
    branch(env, "b20", {"f.txt": "x\n"})
    g(env.root, "fetch", "-q", "origin")
    g(env.root, "branch", "b20", "origin/b20")
    g(env.root, "checkout", "-q", "-b", "side")
    rc, out, _ = go(env, "b20")
    assert rc == 0 and "branch: deleted" in out and g(env.root, "branch", "--list", "b20") == ""


def test_update_ref_old_value_mismatch_keeps_the_branch_E_C3_13(env, monkeypatch):
    branch(env, "b21", {"f.txt": "x\n"})
    g(env.root, "fetch", "-q", "origin")
    g(env.root, "branch", "b21", "origin/b21")
    g(env.root, "checkout", "-q", "-b", "side")
    monkeypatch.setattr(wave, "_hook", lambda name: g(env.root, "update-ref", "refs/heads/b21", "HEAD")
                        if name == "before-update-ref" else None)
    rc, out, _ = go(env, "b21")
    assert rc == 0 and "branch: kept: the branch moved" in out and g(env.root, "branch", "--list", "b21") != ""


def test_lock_held_by_another_wave_refuses_with_the_holder_E_C3_2(env):
    branch(env, "b22", {"f.txt": "x\n"})
    before = origin_main(env)
    with jl.machine_lock("main-merge", 5, repo=env.root):
        rc, out, _ = go(env, "b22")
    assert rc == 2 and "another wave holds main-merge" in out and "pid" in out and origin_main(env) == before


@pytest.mark.parametrize("task", ["t-1", "T-100", "t-100x1", "", "t-1234567890", "100"])
def test_bad_task_is_refused_before_anything_E_C3_3(env, task, capsys):
    assert wave.main(["merge", "b", "--task", task, "--repo", str(env.root)]) == 2
    assert "expected a task id" in capsys.readouterr().out


@pytest.mark.parametrize("name", ["a..b", "a b", "a~1"])
def test_bad_branch_name_is_refused(env, name, capsys):
    assert wave.main(["merge", name, "--task", "t-868", "--repo", str(env.root)]) == 2
    assert "not a branch name" in capsys.readouterr().out


def test_origin_hook_refusal_prints_its_text_E_C3_4(env):
    branch(env, "b23", {"f.txt": "x\n"})
    hook = env.origin / "hooks" / "pre-receive"
    hook.write_bytes(b"#!/bin/sh\necho 'POLICY: no pushes today' >&2\nexit 1\n")
    before = origin_main(env)
    rc, out, _ = go(env, "b23")
    assert rc == 2 and "POLICY: no pushes today" in out and "step 7" in out and origin_main(env) == before
    assert not list((env.root / ".claude" / "worktrees").glob("wave-*"))


def test_network_failure_names_the_step_and_leaves_no_worktree_E_C3_6(env):
    g(env.root, "remote", "set-url", "origin", str(env.tmp / "nowhere.git"))
    rc, out, _ = go(env, "b24")
    assert rc == 2 and "step 2" in out and not list((env.root / ".claude" / "worktrees").glob("wave-*"))
