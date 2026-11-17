"""The module a test file judges when a candidate is not yet on its live path (a plain module: tests import it by this
name, never through conftest)."""
import pathlib
import sys


def load_under_test(env_var: str, module_name: str):
    """The module a test file judges: the file named by the environment variable `env_var` (a candidate not yet on its live
    path), loaded under the name `module_name` so a sibling import of that name resolves to it; unset, the live
    tools/<module_name>.py. Used by every test module of a candidate-gate card for a `.py` candidate. The `<NAME>_PATH=tools/<name>.py.next` form (a copy
    delivered beside its live file; its whole import closure) is read by tools/conftest.py's finder instead: the environment is
    read in those two places only."""
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
