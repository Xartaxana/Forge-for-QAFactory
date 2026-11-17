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


def load_under_test(env_var: str, module_name: str):
    """The module a test file judges: the file named by the environment variable `env_var` (a candidate not yet on its live
    path), loaded under the name `module_name` so a sibling import of that name resolves to it; unset, the live
    tools/<module_name>.py. Used by every test module of a candidate-gate card; the environment read lives only here."""
    import importlib
    import importlib.util
    import os
    path = os.environ.get(env_var)
    if not path:
        return importlib.import_module(module_name)
    path = pathlib.Path(path).resolve()
    loaded = sys.modules.get(module_name)
    if loaded is not None and getattr(loaded, "__file__", None) and pathlib.Path(loaded.__file__).resolve() == path:
        return loaded
    spec = importlib.util.spec_from_file_location(module_name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = mod
    spec.loader.exec_module(mod)
    return mod


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
