"""The one place where the measurement tools find the package and the runs.

Before this module every script carried its own literal path - the old worktrees of
the public release repository for the package, the runs folder for the copies, and the Claude
transcript folder spelled out by hand. When the package moved into this repository the
rates and scripts those literals named went stale without a single test noticing (FR-28, and the
measurement axis of docs/SIBLING_MAP.md): a yardstick priced against a catalogue that was not the
one under test reports a number that is not there.

  REPO, PACKAGE, RATES, SCRIPTS, HANDOFFS   derived from this file's own location, never typed
  BASE                                      where the run copies live (outside this repository):
                                            the QA_RUNS_BASE environment variable (a per-process override;
                                            empty = unset), else stand_copy_root of tools/dev.config.yaml
                                            (tools/dev_config.py; a malformed file = its refusal; a relative value
                                            is resolved against REPO, not the cwd). When neither
                                            is set BASE is NO_BASE, <repo>/.no-stand-copy-root, a folder that
                                            must never be created: importing does not fail and any read of it
                                            reports a missing path
  TABLE                                     the runs table of an experiment (QA_RUNS_TABLE = a JSON file, a relative
                                            value is resolved against REPO; unset or empty = {}): task, copy_prefix,
                                            baselines, story_runs, default_left, default_right, story_ticket, caches, runs_dir, sample_task,
                                            live_repo, toolchain, installed_plugins (a list of ids). A table that was asked for and
                                            cannot be read is RunsTableError, never a partial table
  copy_folder(name, known)                  the one place a run name becomes a folder under BASE
  require_base()                          BASE, or a refusal naming what to set; scripts that WRITE under
                                            BASE call it first
  require_args(ap, (flag, value), ...)      the one refusal of an argument that has no default without a table
  transcript_dir(project_path)              the Claude Code projects folder of one project path
"""
import json
import os
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
PACKAGE = REPO / "ai-packages" / "qa-factory"
RATES = PACKAGE / "references" / "model-rates.json"
SCRIPTS = PACKAGE / "scripts"
HANDOFFS = PACKAGE / "handoffs"


def _stand_copy_root() -> str:
    """stand_copy_root from the developer config. dev_config.py is imported under its own name with
    REPO/tools at the FRONT of sys.path for the duration of the import only (sys.path is restored after), so
    another module called dev_config ahead on sys.path cannot shadow it, `python -I` finds it, and a
    DevConfigError IS dev_config.DevConfigError. dev_config reads with the standard library only, so no extra
    package is needed to import this module. A DevConfigError propagates as it is: the script fails with the
    config's own refusal. Returns None when the key is not set; a relative value is resolved against REPO. Called only when QA_RUNS_BASE is unset, and once per process (the module cache keeps
    BASE), so the missing-file WARN prints at most once."""
    saved = list(sys.path)
    sys.path.insert(0, str(REPO / "tools"))
    try:
        import dev_config
    finally:
        sys.path[:] = saved
    value = dev_config.load(REPO)["stand_copy_root"]
    if value is None:
        return None
    # a relative value (the example's `../stand`) is relative to the repository, not to the cwd of whoever
    # imports this: the transcript folder name and the writers' targets must not depend on where they run (F-12)
    return os.path.normpath(value if Path(value).is_absolute() else REPO / value)


NO_BASE = REPO / ".no-stand-copy-root"      # the stand-in for "not set": never created, so a read finds nothing
BASE = Path(os.environ.get("QA_RUNS_BASE") or _stand_copy_root() or NO_BASE)


RUNS_TABLE_ENV = "QA_RUNS_TABLE"
RUN_NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*")
TABLE_KEYS = ("_comment", "task", "copy_prefix", "baselines", "story_runs", "default_left",
              "default_right", "story_ticket", "caches", "runs_dir", "sample_task", "live_repo", "toolchain", "installed_plugins")
_TOOLCHAIN_KEYS = ("import", "tests")
_PREFIX = re.compile(r"[A-Za-z0-9_.-]*")        # a copy prefix is part of ONE folder name: no separator, no drive colon
_DOTTED = re.compile(r"[A-Za-z_][A-Za-z0-9_]*(\.[A-Za-z_][A-Za-z0-9_]*)*")   # `python -c "import <this>"` runs nothing else


class RunsTableError(RuntimeError):
    """QA_RUNS_TABLE names a file that cannot be used as the runs table (it is never read as a partial table)."""


def _folder_name(value) -> bool:
    return isinstance(value, str) and bool(RUN_NAME.fullmatch(value)) and not value.endswith(".")


def _load_table():
    """(path, table) of the runs table the QA_RUNS_TABLE variable names, or (None, {}) when it is unset or empty.
    A table that was asked for and cannot be read is a refusal naming the variable or the key, never an empty or
    partial table (a measurement against half a table is a number that is not there)."""
    raw = os.environ.get(RUNS_TABLE_ENV) or ""
    if not raw:
        return None, {}
    path = Path(raw)
    path = path if path.is_absolute() else REPO / path
    where = f"{RUNS_TABLE_ENV} points to {path}"
    if not path.is_file():
        raise RunsTableError(f"{where}, which is not a file; set it to a runs table or unset it")
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, ValueError) as err:
        raise RunsTableError(f"runs table {path} ({RUNS_TABLE_ENV}) cannot be read as JSON: {err}") from None
    if not isinstance(data, dict):
        raise RunsTableError(f"runs table {path} ({RUNS_TABLE_ENV}): the top level must be a JSON object")
    head = f"runs table {path}"
    for key in data:
        if key not in TABLE_KEYS:
            raise RunsTableError(f"{head}: unknown key {key!r} (known: {', '.join(TABLE_KEYS)})")
    for key in ("_comment", "task", "default_left", "default_right", "story_ticket", "runs_dir", "sample_task"):
        if key in data and not isinstance(data[key], str):
            raise RunsTableError(f"{head}: {key!r} must be a string")
    plugins = data.get("installed_plugins", [])
    if not isinstance(plugins, list) or not all(isinstance(p, str) and p for p in plugins):
        raise RunsTableError(f"{head}: 'installed_plugins' must be a list of plugin ids (an empty list disables nothing)")
    prefix = data.get("copy_prefix", "")
    if not isinstance(prefix, str) or not _PREFIX.fullmatch(prefix) or ".." in prefix:
        raise RunsTableError(f"{head}: 'copy_prefix' must be letters, digits, '.', '-' or '_' only "
                             f"(no separator, no ':', no '..'): it is the front of one folder name")
    for key in ("baselines", "story_runs"):
        value = data.get(key, {})
        if not isinstance(value, dict) or not all(isinstance(k, str) and _folder_name(v) for k, v in value.items()):
            raise RunsTableError(f"{head}: {key!r} must map run names to folder names (one name, no separator)")
    caches = data.get("caches", {})
    if not isinstance(caches, dict) or not all(isinstance(k, str) and isinstance(v, str) for k, v in caches.items()):
        raise RunsTableError(f"{head}: 'caches' must map run names to paths")
    if "live_repo" in data and not _folder_name(data["live_repo"]):
        raise RunsTableError(f"{head}: 'live_repo' must be one folder name under the runs base")
    chain = data.get("toolchain", {})
    if (not isinstance(chain, dict) or any(k not in _TOOLCHAIN_KEYS for k in chain)
            or not all(isinstance(v, str) for v in chain.values())):
        raise RunsTableError(f"{head}: 'toolchain' must be an object with strings under {', '.join(_TOOLCHAIN_KEYS)}")
    if "import" in chain and not _DOTTED.fullmatch(chain["import"]):
        raise RunsTableError(f"{head}: 'toolchain.import' must be a dotted Python name such as pkg or pkg.sub "
                             f"(it is the module the copy's interpreter imports as proof)")
    return path, data


TABLE_FILE, TABLE = _load_table()
BASELINES = dict(TABLE.get("baselines", {}))
STORY_RUNS = dict(TABLE.get("story_runs", {}))
COPY_PREFIX = TABLE.get("copy_prefix", "")
TASK = TABLE.get("task")
DEFAULT_LEFT = TABLE.get("default_left")
DEFAULT_RIGHT = TABLE.get("default_right")
LIVE_REPO = (BASE / TABLE["live_repo"]) if TABLE.get("live_repo") else None


def table_path(key: str, sub: str | None = None):
    """A path the runs table names under `key` (or under `key`[`sub`] for a mapping), resolved against the folder
    of the table file; None when the table does not name it."""
    value = TABLE.get(key)
    if sub is not None:
        value = value.get(sub) if isinstance(value, dict) else None
    if not value or TABLE_FILE is None:
        return None
    return Path(os.path.normpath(TABLE_FILE.parent / value))


def copy_folder(name: str, known: dict) -> str:
    """The folder of a run copy under the runs base: the named baseline's own folder from `known`, else
    COPY_PREFIX + name - the prefix `prepare_copy.py --name <name>` gives every copy it makes (B-267: a new run
    needed an edit of three dicts before any measurer could read it, and the first run that was not there got a
    KeyError instead of a measurement). A name is a folder suffix, never a path: anything that is not letters,
    digits, dot, dash or underscore (a separator, `..`, an empty name) is refused by name. The tools of this
    folder (`stage_compare.py`, `spend_by_dispatch.py`, `report_run.py`) read this one function."""
    if name in known:
        return known[name]
    if not _folder_name(name):
        raise ValueError(f"run name {name!r} is not a copy name: give the suffix `prepare_copy.py --name` was given "
                         f"(letters, digits, `.`, `-`, `_`), which names {BASE}{chr(92)}{COPY_PREFIX}<name>")
    return f"{COPY_PREFIX}{name}"


class BaseNotSet(RuntimeError):
    """Neither QA_RUNS_BASE nor stand_copy_root names the folder of the run copies."""


def require_base() -> Path:
    """BASE, or BaseNotSet naming what to set; a script that writes under BASE calls this first."""
    if BASE == NO_BASE:
        raise BaseNotSet("set stand_copy_root in tools/dev.config.yaml or QA_RUNS_BASE")
    return BASE


def require_args(ap, *pairs) -> None:
    """The one refusal of an argument that has no default without a runs table: `pairs` are (flag, value); the first
    empty value ends the run through `ap.error` (exit 2, the flag named, no traceback)."""
    for flag, value in pairs:
        if not value:
            ap.error(f"{flag} is required: it has no default without a runs table ({RUNS_TABLE_ENV})")


def transcript_key(project_path) -> str:
    """Claude Code names a project's transcript folder after its path: every character that is not
    a letter or a digit becomes a dash."""
    return re.sub(r"[^A-Za-z0-9]", "-", str(project_path))


def transcript_dir(project_path) -> Path:
    return Path.home() / ".claude" / "projects" / transcript_key(project_path)
