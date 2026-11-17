"""Fixtures of the piles tests (test_piles*.py), built on tools/piles_testkit.py.

Only fixtures that a module does not define itself are used from here (a module-level fixture of the same name wins:
test_piles_split.py keeps its own `session_tree` and `tree`). Nothing is autouse, and the kit is imported lazily, so a test
of another tool never pays for it.
"""
import pathlib
import shutil
import sys

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))


@pytest.fixture(scope="session")
def session_tree(tmp_path_factory):
    import piles_testkit as kit
    root = tmp_path_factory.mktemp("mini") / "repo"
    root.mkdir()
    kit.build_mini(root)
    return root


@pytest.fixture
def tree(session_tree, tmp_path, request):
    dst = tmp_path / "repo"
    ignore = None if getattr(request.function, "_needs_git", False) else shutil.ignore_patterns(".git")
    shutil.copytree(session_tree, dst, ignore=ignore)
    return dst


@pytest.fixture
def cli(capsys, monkeypatch):
    """`piles.main` on a tree. `close` starts the FULL worktree sweep in the background (t-1738, FG7-4): inside this fixture the
    launcher `worktree_sweep.spawn_detached` is a recorder (`run.spawned` = the argv lists it was given) that NEVER makes a
    process -- a close test on a git tree (a real git on `main`) must not start a real sweep of the machine's worktrees. The
    replacement lives here, not in an autouse fixture: "nothing is autouse" stays true."""
    import piles
    import worktree_sweep

    spawned = []

    def recorder(argv, cwd, env):
        spawned.append(list(argv))
        return 0

    monkeypatch.setattr(worktree_sweep, "spawn_detached", recorder)

    def run(root, *args):
        code = piles.main(["--repo", str(root), *map(str, args)])
        return code, capsys.readouterr().out
    run.spawned = spawned
    return run
