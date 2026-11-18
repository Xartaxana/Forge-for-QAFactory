"""The module a test file judges when a candidate is not yet on its live path (a plain module: tests import it by this
name; tools/conftest.py imports it too). Stdlib only: it imports nothing from tools (conftest loads it at module load).

The ONE spec maker of a copy file is `copy_spec`. The environment is read in two places: `load_under_test` (the variable a
test names) and tools/conftest.py (`<NAME>_PATH` variables); both build their spec through `copy_spec`."""
import importlib.machinery
import importlib.util
import pathlib
import sys


def copy_spec(module_name: str, path):
    """The module spec of the copy file `path` under the name `module_name`. SourceFileLoader is given explicitly, so a
    `.py.next` file (no `.py` suffix) loads exactly as a `.py` one."""
    path = str(path)
    return importlib.util.spec_from_file_location(module_name, path, loader=importlib.machinery.SourceFileLoader(module_name, path))


def load_under_test(env_var: str, module_name: str):
    """The module a test file judges: the file named by the environment variable `env_var` (a candidate not yet on its live
    path; a `.py` or a `.py.next` file), loaded under the name `module_name` so a sibling import of that name resolves to it;
    unset or empty, the live tools/<module_name>.py. The spec comes from `copy_spec`, the same maker as the finder of
    tools/conftest.py (the `<NAME>_PATH=tools/<name>.py.next` import closure), so both roads give one file under one name."""
    import importlib
    import os
    path = os.environ.get(env_var)
    if not path:
        return importlib.import_module(module_name)
    path = pathlib.Path(path).resolve()
    loaded = sys.modules.get(module_name)
    if loaded is not None and getattr(loaded, "__file__", None) and pathlib.Path(loaded.__file__).resolve() == path:
        return loaded
    spec = copy_spec(module_name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = mod
    spec.loader.exec_module(mod)
    return mod
