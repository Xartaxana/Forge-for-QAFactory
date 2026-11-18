"""Tests of tools/wave.py (offload spec r2 §3.C3, F-T1): a temp bare "origin", a root clone and a dev clone; no network.
Row ids carry the E-C3-n of the spec."""
import os
import shutil
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
import worktree_sweep as ws  # noqa: E402

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


def go(e, name, node=None, ci=None, task="t-868", piles_skip=None, leftover_ok=None):
    out = []
    w = wave.Wave(e.root, name, task, node, ci=ci or (lambda r, s: "success"), out=out.append, piles_skip=piles_skip,
                  leftover_ok=leftover_ok)
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
    assert rc == 0 and "forge-check: success" in out and "branch: deleted" in out and "root: refreshed to " in out
    assert "pushed to origin" not in out                       # up to date on origin: silent (A)
    assert g(env.origin, "rev-list", "--merges", "main") == "" and blob(env, "f.txt") == b"x\n"
    assert (env.root / "f.txt").read_text() == "x\n" and g(env.origin, "branch", "--list", "b1") == ""
    assert g(env.root, "worktree", "list").count("\n") == 0 and g(env.root, "rev-parse", "HEAD") == origin_main(env)


def test_no_ff_merge_message(env):
    branch(env, "b2", {"f.txt": "x\n"})
    push_main(env, {"g.txt": "y\n"})
    rc, out, w = go(env, "b2", task="t-901")
    assert rc == 0 and g(env.origin, "log", "-1", "--format=%s", "main") == "wave: merge b2 (t-901)"
    assert len(g(env.origin, "rev-list", "--merges", "main").split()) == 1 and w.sha == origin_main(env)


@pytest.mark.parametrize("moved", [False, True])
def test_piles_skip_door_is_the_third_line_of_a_no_ff_merge(env, moved):
    branch(env, "b2d", {"f.txt": "x\n"})
    if moved:
        push_main(env, {"g.txt": "y\n"})
    rc, out, w = go(env, "b2d", task="t-902", piles_skip="б, frozen -- reason here")
    assert rc == 0 and len(g(env.origin, "rev-list", "--parents", "-1", "main").split()) == 3
    assert g(env.origin, "log", "-1", "--format=%B", "main").splitlines() == [
        "wave: merge b2d (t-902)", "", "piles-skip: б, frozen -- reason here"]


@pytest.mark.parametrize("value", ["a -- r", "placement", "placement -- ", "bogus -- r", "", "placement -- r\nx"])
def test_piles_skip_malformed_is_refused_before_anything(env, value, capsys):
    branch(env, "b2e", {"f.txt": "x\n"})
    before, tip = origin_main(env), g(env.origin, "rev-parse", "b2e")
    assert wave.main(["merge", "b2e", "--task", "t-868", "--piles-skip", value, "--repo", str(env.root)]) == 2
    out = capsys.readouterr().out
    assert "expected" in out and "piles-skip: <item> -- <reason>" in out and "placement" in out
    assert origin_main(env) == before and g(env.origin, "rev-parse", "b2e") == tip


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


SHA = "abcd1234" + "0" * 32


@pytest.mark.parametrize("answer,state", [
    (("success", []), "success"),
    (("failure", ["forge-check", "unit"]), "failure (failed: forge-check, unit)"),
    (("failure", []), "failure"),
    (("in_progress", []), "pending"),
    (("none", []), "unknown"),
    (("unknown", []), "unknown")], ids=["green", "red-names", "red-no-names", "pending", "no-run", "unknown"])
def test_forge_check_state_prints_the_run_state_of_ci_read_C3_6(monkeypatch, answer, state):
    import ci_read
    monkeypatch.setattr(ci_read, "run_state", lambda root, sha: answer)
    assert wave.forge_check_state(Path("."), SHA) == state


class _Resp:
    def __init__(self, body):
        self._body = body.encode()
        self.status = 200

    def read(self, n=None):
        return self._body

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


@pytest.mark.parametrize("routes,state", [
    ({"/actions/runs?": {"workflow_runs": [{"id": 1, "head_sha": SHA, "status": "completed", "conclusion": "failure"}]},
      "/actions/runs/1/jobs": {"jobs": [{"name": "forge-check", "conclusion": "failure"}, {"name": "unit", "conclusion": "failure"}]}},
     "failure (failed: forge-check, unit)"),
    ({"/actions/runs?": {"workflow_runs": [{"id": 1, "head_sha": SHA, "status": "completed", "conclusion": "success"}]},
      "/actions/runs/1/jobs": {"jobs": [{"name": "forge-check", "conclusion": "success"}]}}, "success"),
    ({"/actions/runs?": "not json"}, "unknown")], ids=["red", "green", "bad-answer"])
def test_forge_check_state_goes_through_the_real_ci_read_with_a_faked_opener_C3_6(monkeypatch, tmp_path, routes, state):
    """The junction: a rename in ci_read turns this red instead of turning the state into a silent unknown."""
    import json
    import urllib.request
    monkeypatch.setenv("QA_CI_REPO", "o/r")
    monkeypatch.setenv("GITHUB_TOKEN", "dummy-token")
    monkeypatch.delenv("QA_DEV_CONFIG", raising=False)

    def fake_urlopen(req, timeout=None):
        for needle, answer in routes.items():
            if needle in req.full_url:
                return _Resp(answer if isinstance(answer, str) else json.dumps(answer))
        raise AssertionError("unexpected request " + req.full_url)
    monkeypatch.setattr(urllib.request, "urlopen", fake_urlopen)
    assert wave.forge_check_state(tmp_path, SHA) == state


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


def test_foreign_change_does_not_stop_the_ff_refresh_C(env):
    branch(env, "b7", {"f.txt": "x\n"})
    (env.root / "README").write_text("dirty\n")
    rc, out, _ = go(env, "b7")
    assert rc == 0 and blob(env, "f.txt") == b"x\n"
    assert "root: refreshed to %s" % origin_main(env) in out
    assert (env.root / "README").read_text() == "dirty\n" and (env.root / "f.txt").read_text() == "x\n"
    assert g(env.root, "stash", "list") == ""


def test_ff_refused_by_git_names_its_reason_and_paths_C(env):
    branch(env, "b7r", {"README": "branch\n"})
    (env.root / "README").write_text("dirty\n")
    rc, out, _ = go(env, "b7r")
    line = [ln for ln in out.splitlines() if ln.startswith("root not refreshed:")]
    assert rc == 0 and len(line) == 1 and "would be overwritten" in line[0] and line[0].endswith("paths: README")
    assert (env.root / "README").read_text() == "dirty\n" and g(env.root, "stash", "list") == ""
    assert blob(env, "README") == b"branch\n"


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
    assert rc == 1 and "refused: nope" in out and "run by hand, from " in out and "tools/piles.py status pile 1 N-3" in out
    assert "then commit and push the batch file" in out
    assert blob(env, "f.txt") == b"x\n" and w.pushed
    assert g(env.origin, "branch", "--list", "b12") == ""


def test_status_commit_refusal_takes_the_same_road_C3_5(env):
    branch(env, "b12c", {"f.txt": "x\n"})
    pre_commit = env.root / ".git" / "hooks" / "pre-commit"
    pre_commit.write_bytes(
        b"#!/bin/sh\ngit diff --cached --name-only | grep -q node.txt && { echo 'HOOK: no node' >&2; exit 1; }\nexit 0\n")
    pre_commit.chmod(0o755)    # a hook fires only when executable (Linux); Windows ignores the bit
    rc, out, w = go(env, "b12c", node=("pile", "1", "N-4"))
    assert rc == 1 and "the status commit was refused" in out and "HOOK: no node" in out and w.pushed
    assert blob(env, "f.txt") == b"x\n" and blob(env, "plans/node.txt") is None


def test_piles_refusal_on_attempt_1_then_success_exits_0_C3_5(env, monkeypatch):
    push_main(env, {"plans/refuse": "x\n"})
    branch(env, "b12r", {"f.txt": "x\n"})
    real, calls = wave.Wave.push, []

    def moved_once(self, w, step):
        calls.append(step)
        if len(calls) == 1:
            g(env.dev, "fetch", "-q", "origin")
            g(env.dev, "checkout", "-q", "--detach", "origin/main")
            g(env.dev, "rm", "-q", "plans/refuse")
            g(env.dev, "commit", "-q", "-m", "drop the refusal")
            g(env.dev, "push", "-q", "origin", "HEAD:main")
        return real(self, w, step)
    monkeypatch.setattr(wave.Wave, "push", moved_once)
    rc, out, _ = go(env, "b12r", node=("pile", "1", "N-5"))
    assert rc == 0 and "piles status not recorded" not in out and blob(env, "plans/node.txt") is not None


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
    assert rc == 0 and "root not refreshed: " in out and out.splitlines()[-1].endswith("paths: f.txt")
    assert (env.root / REL).read_bytes() == L1 + L2 and (env.root / "f.txt").read_text() == "untracked in the way\n"
    assert not list(jl.lock_dir(env.root).glob("wave-copy-*"))


def test_restore_mismatch_keeps_the_copy_and_the_summary_exit_1_C3_1(env, monkeypatch):
    branch(env, "b17", {"f.txt": "x\n"})
    (env.root / REL).write_bytes(L1 + L2)
    monkeypatch.setattr(wave, "_hook", lambda n: (env.root / REL).write_bytes(b"garbage\n") if n == "step9-locked" else None)
    rc, out, _ = go(env, "b17")
    assert rc == 1 and "JOURNAL RESTORE MISMATCH: the journal changed inside the window; copy kept at" in out
    assert "merge: " in out and "branch: deleted" in out
    assert list(jl.lock_dir(env.root).glob("wave-copy-*"))[0].read_bytes() == L1 + L2


def test_unlocked_appender_in_the_window_is_carried_over_Q5a(env, monkeypatch):
    branch(env, "b17a", {"f.txt": "x\n"})
    (env.root / REL).write_bytes(L1 + L2)

    def hook(n):
        if n == "step9-locked":
            with open(env.root / REL, "ab") as f:      # a by-hand Edit that takes no lock
                f.write(L3)
    monkeypatch.setattr(wave, "_hook", hook)
    rc, out, _ = go(env, "b17a")
    assert rc == 0 and "a line written during the window was appended" in out
    assert (env.root / REL).read_bytes() == L1 + L2 + L3
    assert list(jl.lock_dir(env.root).glob("wave-copy-*"))[0].read_bytes() == L1 + L2


@pytest.mark.parametrize("case", ["equal", "differs", "off_main"])   # FG7-82 E6 + FG7-85: auto refresh only for an equal copy on main
def test_restore_oserror_in_the_window_names_the_copy_Q5c(env, monkeypatch, case):
    branch(env, "b17b", {"f.txt": "x\n", **({REL: L1 + L2} if case != "differs" else {})})
    (env.root / REL).write_bytes(L1 + L2)

    def hook(n):
        if n == "step9-locked":
            if case == "differs":        # the wave commits the root journal into main, so the copy is made to differ
                with open(next(jl.lock_dir(env.root).glob("wave-copy-*")), "ab") as f:
                    f.write(L3)
            if case == "off_main":
                g(env.root, "checkout", "-q", "-b", "side")
            raise OSError("disk says no")
    monkeypatch.setattr(wave, "_hook", hook)
    rc, out, _ = go(env, "b17b")
    copies = list(jl.lock_dir(env.root).glob("wave-copy-*"))
    if case == "equal":
        assert rc == 0 and "the root was staged and fast-forwarded by wave" in out and "RESTORE FAILED" not in out
        assert not copies and (env.root / REL).read_bytes() == L1 + L2 and g(env.root, "status", "--porcelain") == ""
        return
    assert rc == 1 and "JOURNAL RESTORE FAILED (disk says no): copy kept at" in out and "merge: " in out
    assert copies[0].read_bytes() == L1 + L2 + (L3 if case == "differs" else b"")
    assert ("fast-forward the root by hand" in out) == (case == "off_main")
    assert ("auto refresh refused: the root is not on main" in out) == (case == "off_main")


@pytest.mark.parametrize("errs,exc,retried,ok", [          # FG7-82: t-1414 WinError 5 on os.replace
    ([PermissionError(5, "denied")], None, True, True),                    # E1: once, then works
    ([PermissionError(32, "busy")] * 9999, PermissionError, True, False),     # E2: always fails -> raised, tmp gone
    ([OSError("disk")] * 9999, OSError, False, False),                         # E3: other OSError, no retry
])
def test_atomic_write_retries_permission_error_only(tmp_path, monkeypatch, errs, exc, retried, ok):
    real, seen = os.replace, []

    def rep(a, b):
        seen.append(1)
        if len(seen) <= len(errs):
            raise errs[len(seen) - 1]
        real(a, b)
    monkeypatch.setattr(wave.os, "replace", rep)
    monkeypatch.setattr(jl, "REPLACE_RETRY_SECONDS", 0.05)       # the shared rule, shortened
    monkeypatch.setattr(jl, "REPLACE_PAUSE", 0.005)
    p = tmp_path / "j.jsonl"
    if exc:
        with pytest.raises(exc):
            wave._atomic_write(p, b"new")
    else:
        wave._atomic_write(p, b"new")
    assert (len(seen) > 1) == retried and p.exists() == ok and not (tmp_path / "j.jsonl.wave-tmp").exists()


def test_fetch_failure_in_step_9_after_the_push_still_finishes_C3_1(env, monkeypatch):
    branch(env, "b17c", {"f.txt": "x\n"})
    real = wave.Wave.fetch

    def fetch(self, step="step 2"):
        if step == "step 9":
            raise wave.Refuse("step 9: git fetch origin failed: network")
        return real(self, step)
    monkeypatch.setattr(wave.Wave, "fetch", fetch)
    rc, out, w = go(env, "b17c")
    assert rc == 0 and w.pushed and "refused" not in out and "merge: " in out
    assert "root checkout not refreshed: git fetch origin failed" in out and blob(env, "f.txt") == b"x\n"


def test_sweep_deleting_the_branch_first_is_not_reported_as_kept_C3_7(env, monkeypatch):
    branch(env, "b17d", {"f.txt": "x\n"})
    g(env.root, "fetch", "-q", "origin")
    g(env.root, "branch", "b17d", "origin/b17d")
    monkeypatch.setattr(wave, "_hook", lambda n: g(env.root, "branch", "-D", "b17d") if n == "before-branch-delete" else None)
    rc, out, _ = go(env, "b17d")
    assert rc == 0 and "branch: deleted (by the post-merge sweep" in out


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
    rc, out, _ = go(env, "b19", leftover_ok="test")      # a dirty worktree is a leftover now (FG7-67): the door is needed
    assert rc == 0 and "branch: kept, checked out in" in out and "(dirty)" in out and wt.exists()
    assert g(env.root, "branch", "--list", "b19") != "" and blob(env, "f.txt") == b"x\n"
    assert "remote kept: " in out and g(env.origin, "branch", "--list", "b19") != ""      # Q4


def test_remote_branch_that_moved_is_kept_by_the_lease_C3_3(env, monkeypatch):
    branch(env, "b19m", {"f.txt": "x\n"})

    def hook(n):
        if n == "before-delete-remote":                # a live worker pushes after step 3
            g(env.dev, "checkout", "-q", "-B", "b19m", "origin/b19m")
            put(env.dev, {"late.txt": "late\n"}, "late")
            g(env.dev, "push", "-q", "origin", "b19m")
    monkeypatch.setattr(wave, "_hook", hook)
    rc, out, _ = go(env, "b19m")
    assert rc == 0 and "remote branch kept: it moved" in out
    assert g(env.origin, "show", "b19m:late.txt") == "late"


@pytest.mark.parametrize("rc,err,want", [
    (1, "fatal: unable to access 'x': The requested URL returned error: 403", "remote branch kept: the host refused the delete (HTTP 403"),
    (1, "error: RPC failed; HTTP 403 curl 22", "delete bz locally with git push origin --delete bz, or in the GitHub UI"),
    (128, "fatal: could not resolve host\nsecond line " + "x" * 200, "remote branch not deleted: fatal: could not resolve host\n"),
    (128, "y" * 300, "remote branch not deleted: " + "y" * 120 + "\n"),
    (1, "! [rejected] bz (stale info)", "remote branch kept: it moved\n"),
    (0, "", ""),
])
def test_delete_remote_message_per_git_answer(monkeypatch, rc, err, want):      # FG7-68
    said = []
    monkeypatch.setattr(wave, "_hook", lambda n: None)
    monkeypatch.setattr(wave, "git", lambda *a, **k: (rc, "", err))
    wave.Wave.delete_remote(SimpleNamespace(branch="bz", branch_sha="s", root=".", say=lambda t: said.append(t + "\n")))
    text = "".join(said)
    assert (want in text) if want else text == ""
    assert "second line" not in text and "y" * 121 not in text


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


def test_clone_letters_pass_the_task_check_and_bad_nodes_are_refused_C3_4(env, capsys):
    argv = ["merge", "nope", "--repo", str(env.root)]
    assert wave.main(argv + ["--task", "t-123ab"]) == 2 and "expected a task id" not in capsys.readouterr().out
    for node in (["Pile", "1", "N-1"], ["pile", "0", "N-1"], ["pile", "x", "N-1"], ["pile", "1", "-"]):
        assert wave.main(argv + ["--task", "t-123", "--node", *node]) == 2
        assert "node grammar" in capsys.readouterr().out


@pytest.mark.parametrize("name", ["a..b", "a b", "a~1"])
def test_bad_branch_name_is_refused(env, name, capsys):
    assert wave.main(["merge", name, "--task", "t-868", "--repo", str(env.root)]) == 2
    assert "not a branch name" in capsys.readouterr().out


def test_origin_hook_refusal_prints_its_text_E_C3_4(env):
    branch(env, "b23", {"f.txt": "x\n"})
    hook = env.origin / "hooks" / "pre-receive"
    hook.write_bytes(b"#!/bin/sh\necho 'POLICY: no pushes today' >&2\nexit 1\n")
    hook.chmod(0o755)    # a hook fires only when executable (Linux); Windows ignores the bit
    before = origin_main(env)
    rc, out, _ = go(env, "b23")
    assert rc == 2 and "POLICY: no pushes today" in out and "step 7" in out and origin_main(env) == before
    assert not list((env.root / ".claude" / "worktrees").glob("wave-*"))


def test_network_failure_names_the_step_and_leaves_no_worktree_E_C3_6(env):
    g(env.root, "remote", "set-url", "origin", str(env.tmp / "nowhere.git"))
    rc, out, _ = go(env, "b24")
    assert rc == 2 and "step 2" in out and not list((env.root / ".claude" / "worktrees").glob("wave-*"))


def local_branch(e, name, files):
    """A branch that exists only in the root clone (not on origin), as a worker leaves it."""
    g(e.root, "checkout", "-q", "-b", name, "origin/main")
    put(e.root, files, name)
    g(e.root, "checkout", "-q", "main")


def test_branch_only_local_is_pushed_by_wave_then_merged_A(env):
    local_branch(env, "a1", {"f.txt": "x\n"})
    rc, out, _ = go(env, "a1")
    assert rc == 0 and "branch a1 pushed to origin" in out and blob(env, "f.txt") == b"x\n"
    assert g(env.origin, "branch", "--list", "a1") == "" and g(env.root, "branch", "--list", "a1") == ""


def test_push_of_the_branch_refused_names_origin_text_and_merges_nothing_A(env):
    local_branch(env, "a2", {"f.txt": "x\n"})
    hook = env.origin / "hooks" / "pre-receive"
    hook.write_bytes(b"#!/bin/sh\necho 'POLICY: no pushes today' >&2\nexit 1\n")
    hook.chmod(0o755)    # a hook fires only when executable (Linux); Windows ignores the bit
    before = origin_main(env)
    rc, out, _ = go(env, "a2")
    assert rc == 2 and "POLICY: no pushes today" in out and "step 3" in out and origin_main(env) == before
    assert g(env.origin, "branch", "--list", "a2") == "" and not list((env.root / ".claude" / "worktrees").glob("wave-*"))


def test_branch_behind_local_is_pushed_and_diverged_is_refused_not_forced_A(env):
    branch(env, "a3", {"f.txt": "x\n"})
    g(env.root, "fetch", "-q", "origin")
    g(env.root, "checkout", "-q", "-b", "a3", "origin/a3")
    put(env.root, {"g.txt": "y\n"}, "local ahead")
    g(env.root, "checkout", "-q", "main")
    rc, out, _ = go(env, "a3")
    assert rc == 0 and "branch a3 pushed to origin" in out and blob(env, "g.txt") == b"y\n"
    branch(env, "a4", {"f4.txt": "x\n"})
    g(env.root, "fetch", "-q", "origin")
    g(env.root, "checkout", "-q", "-b", "a4", "origin/a4~1")
    put(env.root, {"other.txt": "o\n"}, "diverged")
    g(env.root, "checkout", "-q", "main")
    before = origin_main(env)
    rc, out, _ = go(env, "a4")
    assert rc == 2 and "step 3" in out and "non-fast-forward" in out and origin_main(env) == before
    assert g(env.origin, "show", "a4:f4.txt") == "x"


DEV_HOOK = (b"#!/bin/sh\n[ -f tools/dev.config.yaml ] || { echo 'tools/dev.config.yaml cannot be read (no such file)' >&2; exit 1; }\n"
            b"exit 0\n")


def validator_hook(e):
    hook = e.root / ".git" / "hooks" / "pre-commit"
    hook.write_bytes(DEV_HOOK)
    hook.chmod(0o755)    # a hook fires only when executable (Linux); Windows ignores the bit


def test_journal_commit_gets_the_slug_from_the_main_tree_B(env):
    branch(env, "j1", {"f.txt": "x\n"})
    validator_hook(env)
    (env.root / "tools").mkdir(exist_ok=True)
    (env.root / "tools" / "dev.config.yaml").write_text("developer: dev\n")      # untracked, main tree only
    (env.root / REL).write_bytes(L1 + L2)
    rc, out, _ = go(env, "j1", task="t-890")
    assert rc == 0 and blob(env, REL) == L1 + L2 and "journal not committed" not in out
    assert blob(env, "tools/dev.config.yaml") is None and not list((env.root / ".claude" / "worktrees").glob("wave-*"))


def test_journal_not_committed_when_the_slug_is_unknown_in_the_main_tree_too_B(env):
    branch(env, "j2", {"f.txt": "x\n"})
    validator_hook(env)
    (env.root / REL).write_bytes(L1 + L2)
    rc, out, _ = go(env, "j2")
    assert rc == 0 and blob(env, "f.txt") == b"x\n" and blob(env, REL) == L1
    assert "journal not committed: developer slug unknown (tools/dev.config.yaml)" in out


def test_step_9_writes_are_atomic_a_reader_sees_a_whole_journal_Q5b(env, monkeypatch):
    branch(env, "q1", {"f.txt": "x\n"})
    (env.root / REL).write_bytes(L1 + L2)
    seen, real = [], os.replace

    def spy(src, dst):
        seen.append((Path(dst).read_bytes() if Path(dst).exists() else None, Path(src).read_bytes()))
        return real(src, dst)
    monkeypatch.setattr(wave.os, "replace", spy)
    rc, out, _ = go(env, "q1")
    assert rc == 0 and (env.root / REL).read_bytes() == L1 + L2
    # each replace: the destination still held a whole journal (never a truncated one), the new bytes were already complete
    assert seen == [(L1 + L2, L1), (L1 + L2, L1 + L2)] and not list(env.root.glob("logs/journal/*.wave-tmp"))


def test_worktree_already_gone_is_a_report_line_and_the_lock_is_released_C3_7(env, monkeypatch):
    branch(env, "s1", {"f.txt": "x\n"})
    g(env.root, "fetch", "-q", "origin")
    g(env.root, "branch", "s1", "origin/s1")
    wt = env.tmp / "wt-s1"
    g(env.root, "worktree", "add", "-q", str(wt), "s1")
    held = []

    def hook(n):
        if n == "before-worktree-remove":
            held.append((jl.common_dir(env.root) / ws.STATE_DIRNAME / "lock").exists())   # the sweep's lock is ours now
            shutil.rmtree(wt)                                                           # the sweep got there first
    monkeypatch.setattr(wave, "_hook", hook)
    rc, out, _ = go(env, "s1")
    assert rc == 0 and held == [True] and "folder already gone" in out and "branch: deleted" in out
    assert g(env.root, "branch", "--list", "s1") == "" and not (jl.common_dir(env.root) / ws.STATE_DIRNAME / "lock").exists()


def test_worktree_left_to_a_running_sweep_when_its_lock_stays_busy_C3_7(env, monkeypatch):
    branch(env, "s2", {"f.txt": "x\n"})
    g(env.root, "fetch", "-q", "origin")
    g(env.root, "branch", "s2", "origin/s2")
    wt = env.tmp / "wt-s2"
    g(env.root, "worktree", "add", "-q", str(wt), "s2")
    monkeypatch.setattr(wave, "SWEEP_WAIT", 0.3)
    lock, _ = ws.acquire_lock(jl.common_dir(env.root) / ws.STATE_DIRNAME, "test-sweep")
    try:
        rc, out, _ = go(env, "s2")
    finally:
        lock.release()
    assert rc == 0 and wt.exists() and "a worktree sweep holds its lock" in out and blob(env, "f.txt") == b"x\n"
    assert g(env.root, "branch", "--list", "s2") != ""


def test_worktree_that_git_cannot_remove_keeps_the_branch_P4_F1(env):
    branch(env, "s3", {"f.txt": "x\n"})
    g(env.root, "fetch", "-q", "origin")
    g(env.root, "branch", "s3", "origin/s3")
    wt = env.tmp / "wt-s3"
    g(env.root, "worktree", "add", "-q", str(wt), "s3")
    g(env.root, "worktree", "lock", str(wt))                  # `remove --force` (once) refuses a locked worktree
    rc, out, _ = go(env, "s3")
    assert rc == 0 and wt.exists() and "kept: git worktree remove failed:" in out and "(the worktree is not removed)" in out
    assert g(env.root, "branch", "--list", "s3") != "" and blob(env, "f.txt") == b"x\n"


@pytest.mark.parametrize("pin,ok", [
    ("full", True), ("prefix7", True), ("upper", True),
    ("other", False), ("short", False), ("nothex", False), ("empty", False)],
    ids=["full", "prefix7", "upper-case", "other-tip", "6-chars", "not-hex", "empty"])
def test_sha_pin_is_checked_before_any_push_P4_Q2(env, pin, ok):
    branch(env, "p1", {"f.txt": "x\n"})
    tip = g(env.origin, "rev-parse", "p1")
    main_before = origin_main(env)
    value = {"full": tip, "prefix7": tip[:7], "upper": tip[:12].upper(), "other": "0" * 40, "short": tip[:6],
             "nothex": "zzzzzzzz", "empty": ""}[pin]
    out = []
    rc = wave.Wave(env.root, "p1", "t-868", None, ci=lambda r, s: "success", out=out.append, pin=value).run()
    text = "\n".join(out)
    if ok:
        assert rc == 0 and "pushed: %s" % tip in text and blob(env, "f.txt") == b"x\n"
    else:
        assert rc == 2 and origin_main(env) == main_before and blob(env, "f.txt") is None and "pushed:" not in text
        assert ("!= accepted" in text and "re-accept the new tip" in text) if pin == "other" else "expected 7 to 40 hex" in text


def vol_branch(e, name, t, p):
    branch(e, name, {"tools/tests/t.py": "t\n" * t, "tools/p.py": "p\n" * p})


@pytest.mark.parametrize("t,p,door,merged,where", [
    (5, 2, None, False, "origin"), (5, 2, "why", True, "origin"), (3, 3, None, True, "origin"),
    (0, 2, None, True, "origin"), (2, 0, None, False, "origin"), (0, 2, "why", True, "origin"),
    (5, 2, None, False, "local"), (9, 2, None, False, "ahead"), (3, 9, None, True, "pe")],
    ids="over no-door,over door,equal,zero tests,zero product,door within budget,over local-only,"
        "origin ahead of local,non-ascii product path".split(","))
def test_test_volume_budget_and_door(env, t, p, door, merged, where):
    files = {"tools/tests/t.py": "t\n" * t, "tools/p.py": "p\n" * p}
    if where == "local":                    # committed in the root, never pushed: a refusal leaves origin untouched
        g(env.root, "checkout", "-q", "-B", "v1", "origin/main")
        put(env.root, files)
        g(env.root, "checkout", "-q", "main")
    elif where == "ahead":                  # origin's tip is past the local one and is the over-budget one
        vol_branch(env, "v1", 0, p)
        g(env.root, "fetch", "-q", "origin")
        g(env.root, "branch", "v1", "origin/v1")
        branch(env, "v1", {"tools/tests/t2.py": "t\n" * t}, base="origin/v1")
    else:
        branch(env, "v1", {"tools/tests/t.py": "t\n" * t, ("tools/pé.py" if where == "pe" else "tools/p.py"): "p\n" * p})
    main0, refs0 = origin_main(env), g(env.origin, "for-each-ref", "refs/heads")
    out = []
    w = wave.Wave(env.root, "v1", "t-868", None, ci=lambda r, s: "x", out=out.append, tests_over=door)
    rc, text = w.run(), "\n".join(out)
    assert (rc == 0) == merged and (origin_main(env) != main0) == merged
    if not merged:
        assert rc == 2 and "TEST VOLUME: the branch adds +%d test lines vs +%d product lines" % (t, p) in text
        assert g(env.origin, "for-each-ref", "refs/heads") == refs0 and "pushed:" not in text
    elif door:
        assert g(env.origin, "log", "-1", "--format=%B", "main").splitlines()[-1] == "tests-over: why" and "tests-over: why" in text
        assert len(g(env.origin, "rev-list", "--merges", "main").split()) == 1


FLAGS = ["--tests-over", "--leftover-ok"]


@pytest.mark.parametrize("flag", FLAGS)
@pytest.mark.parametrize("reason", ["", "  ", "a\nb", "x" * 301])
def test_reason_flags_refused_input_needs_no_git_world(tmp_path, flag, reason, capsys):
    rc = wave.main(["merge", "v2", "--task", "t-868", flag, reason, "--repo", str(tmp_path)])
    assert rc == 2 and "refused: " + flag in capsys.readouterr().out


@pytest.mark.parametrize("flag", FLAGS)
@pytest.mark.parametrize("reason", ["x", "x" * 300, " " + "x" * 300])
def test_reason_flags_accepted_input_merges(env, flag, reason):
    vol_branch(env, "v2", 5, 2)
    extra = ["--tests-over", "w"] if flag == "--leftover-ok" else []     # the volume door the branch needs anyway
    rc = wave.main(["merge", "v2", "--task", "t-868", flag, reason, *extra, "--repo", str(env.root)])
    assert rc == 0 and g(env.origin, "log", "-1", "--format=%B", "main").splitlines()[-1] == "tests-over: " + (
        reason.strip() if flag == "--tests-over" else "w")


def test_a_numstat_that_cannot_be_computed_is_one_line_and_the_merge_goes_on(env, monkeypatch):
    vol_branch(env, "v3", 5, 2)
    real = wave.git
    monkeypatch.setattr(wave, "git", lambda cwd, *a: (1, "", "boom") if "--numstat" in a else real(cwd, *a))
    out = []
    rc = wave.Wave(env.root, "v3", "t-868", None, ci=lambda r, s: "x", out=out.append, tests_over="why").run()
    text = "\n".join(out)
    assert rc == 0 and text.count("test volume: not checked (") == 1 and blob(env, "tools/p.py") is not None
    assert g(env.origin, "log", "-1", "--format=%B", "main").splitlines()[-1] == "tests-over: why"


def test_a_local_tip_that_is_not_the_pin_is_not_pushed_P4_Q2(env):
    branch(env, "p2", {"f.txt": "x\n"})
    g(env.root, "fetch", "-q", "origin")
    g(env.root, "branch", "p2", "origin/p2")
    accepted = g(env.root, "rev-parse", "p2")
    g(env.root, "checkout", "-q", "p2")
    put(env.root, {"late.txt": "late\n"}, "late commit")      # a commit the worker added after acceptance
    g(env.root, "checkout", "-q", "main")
    out = []
    rc = wave.Wave(env.root, "p2", "t-868", None, ci=lambda r, s: "success", out=out.append, pin=accepted).run()
    assert rc == 2 and "!= accepted" in "\n".join(out) and g(env.origin, "rev-parse", "p2") == accepted


def leftover_world(e, name, kind):
    branch(e, name, {"f.txt": "x\n"})
    if kind == "absent":
        return None
    g(e.root, "fetch", "-q", "origin")
    g(e.root, "branch", name, "origin/" + name)
    wt = e.tmp / ("wt-" + name)
    g(e.root, "worktree", "add", "-q", str(wt), name)
    if kind == "prunable":
        shutil.rmtree(wt)
    if kind == "nested":
        g(e.tmp, "init", "-q", str(wt / "sub"))
        (wt / "sub" / "a.txt").write_text("a")
    dirty = {"junk": {"critic_snapshot.json": "{}"}, "cr": {"README": "a\r\n"}, "real": {"README": "mine\n"},
             "untracked": {"new.txt": "n\n"}, "many": {"n%02d.txt" % i: "n" for i in range(25)}}
    for rel, text in dirty.get(kind.split("+")[0], {}).items():
        (wt / rel).write_bytes(text.encode())
    return wt


@pytest.mark.parametrize("kind, flag, rc, shows", [
    ("clean", None, 0, "leftover: none"), ("absent", None, 0, "leftover: none"), ("junk", None, 0, "leftover: none"),
    ("cr", None, 0, "leftover: none"), ("real", None, 2, "door 2: --leftover-ok"), ("untracked", None, 2, "  new.txt"),
    ("many", None, 2, "+5 more"), ("prunable", None, 0, "leftover: none"), ("nested", None, 2, "nested repositor"),
    ("nested", "why", 2, "does not pass it"), ("real", None, 2, "origin/main as last fetched"), ("clean", "why", 0, "no leftover; --leftover-ok unused"),
    ("real", "why", 0, "leftover: salvaged refs/worktree-sweep/salvage/lo/"), ("real+fail", "why", 2, "could not be saved")])
def test_leftover_of_the_branch_worktree_refuses_or_is_salvaged_FG7_67(env, monkeypatch, kind, flag, rc, shows):
    wt = leftover_world(env, "lo", kind)
    if kind.endswith("+fail"):
        monkeypatch.setattr(ws, "salvage_leftover", lambda *a: (False, "boom"))
    before = origin_main(env)
    status = g(wt, "status", "--porcelain") if wt and wt.exists() else ""
    got, out, _ = go(env, "lo", leftover_ok=flag)
    assert got == rc and shows in out
    if wt and wt.exists():
        assert g(wt, "status", "--porcelain") == status                       # the worktree is never written
    if rc:
        assert origin_main(env) == before and "pushed:" not in out and out.count("\n  n") <= 20   # nothing before fetch/push
    if flag and "salvaged" in out:
        assert g(env.root, "for-each-ref", "refs/worktree-sweep/salvage/lo") != ""
