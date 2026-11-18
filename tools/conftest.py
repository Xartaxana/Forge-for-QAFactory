"""Fixtures of the piles tests (test_piles*.py), built on tools/piles_testkit.py.

Only fixtures that a module does not define itself are used from here (a module-level fixture of the same name wins:
test_piles_split.py keeps its own `session_tree` and `tree`). Nothing is autouse, and the kit is imported lazily, so a test
of another tool never pays for it.
"""
import importlib.abc
import importlib.machinery
import importlib.util
import os
import pathlib
import shutil
import sys

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import under_test  # noqa: E402  (sibling in tools/, found through the path line above; stdlib-only)

NEXT_SUFFIX = ".py.next"


def next_copy_map(environ, tools_dir):
    """{module name: absolute path of its `.py.next` copy} for every variable `<NAME>_PATH` of `environ` whose value ends in
    `.py.next` (FG7-58, spec F5-r): a builder delivers a hook file as a copy beside its live file, and a test run that sets
    `<NAME>_PATH=tools/<name>.py.next` judges the copy. `<name>` is NAME lower-cased. A value that ends in `.py.next` and names
    no existing file, or whose `tools/<name>.py` does not exist, raises RuntimeError naming the variable (a typo must not
    silently test the live file), and so raises a value whose file name starts with `<name>.py` and is neither `<name>.py` nor
    `<name>.py.next` (a `.py.nxt` typo; values such as ORIGINAL_PATH are untouched). Every other value -- a `.py` file (the HYGIENE_GATE_PATH loaders of test_hygiene_gate.py and
    test_permission_audit.py), an empty one, a directory -- is ignored."""
    mapping = {}
    for var, value in environ.items():
        if not var.endswith("_PATH") or len(var) == len("_PATH"):
            continue
        name = var[:-len("_PATH")].lower()
        shown = pathlib.PureWindowsPath(value).name
        if shown.startswith(name + ".py") and shown not in (name + ".py", name + NEXT_SUFFIX):
            raise RuntimeError("%s=%s: a copy is `%s.py.next` (or the live `%s.py`); this looks like a typo of it"
                               % (var, value, name, name))
        if not value.endswith(NEXT_SUFFIX):
            continue
        path = pathlib.Path(value).resolve()
        if not path.is_file():
            raise RuntimeError("%s=%s names no existing file: a `.py.next` value must name the copy to test" % (var, value))
        if not (pathlib.Path(tools_dir) / (name + ".py")).is_file():
            raise RuntimeError("%s=%s: tools/%s.py does not exist, so there is no live module this copy stands in for"
                               % (var, value, name))
        mapping[name] = str(path)
    return mapping


class _NextCopyFinder(importlib.abc.MetaPathFinder):
    """Answers `find_spec(<name>)` with the copy's file for the mapped names and None for every other name, so a test's
    `import dispatch_manifest` and a sibling module's own import both resolve to the copy, in any order. The spec is built by
    under_test.copy_spec, the one spec maker (under_test.load_under_test uses it too); the environment is read in two places:
    here (`<NAME>_PATH`, via next_copy_map) and in load_under_test."""

    def __init__(self, mapping):
        self.mapping = mapping

    def find_spec(self, fullname, path=None, target=None):
        copy = self.mapping.get(fullname)
        if copy is None:
            return None
        return under_test.copy_spec(fullname, copy)


def install_next_copies(environ=None, tools_dir=None):
    """Install the finder for the copies named by `<NAME>_PATH` variables, once, at the FRONT of sys.meta_path; returns the
    mapping. The environment is read here, in test code only."""
    mapping = next_copy_map(os.environ if environ is None else environ,
                            pathlib.Path(__file__).resolve().parent if tools_dir is None else tools_dir)
    if mapping and not any(type(f).__name__ == "_NextCopyFinder" for f in sys.meta_path):
        sys.meta_path.insert(0, _NextCopyFinder(mapping))
    return mapping


install_next_copies()


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
