"""The census of the driver's exits (P1-b spec sections 3.1-3.6, node N1): which routes, joints and question kinds the driver has, and
whether each has a row; the class of each refusal; the state fingerprint and the "same ask" test the dry walk judges with.

A helper next to the tests, not a test (like `scenario_walk.py`). It decides nothing about meaning (P27, AR-29): it reads data -
the driver's own tables by import (`driver_dispatch.KNOWN_REFUSALS`, `no_move.load_question_prices`, the stage-joints file through the
reader its walker uses, `refusal_registry.REGISTRY`, the driver sources through `harness.driver_sources`) - and compares them with the
rows of `fixtures/driver-exits/<group>.json`, in both directions. A route, joint or keyless question kind with no row is red; so is a
row with nothing behind it. The keys of the closed questions are NOT censused here (`test_conductor_doors.py` already does that; the
walk rows join its `driven` set through `driven_keys`). A question kind is "keyless" (a row here) unless its text argument is, or is a name
bound IN THE SAME FUNCTION to, a `closed_question(...)` / `priced_section(...)` call: those texts are the existing census's.

    python -B scripts/tests/dry_exits.py --check [--dir D] [--exits-dir E]   the census: 0 discrepancies or the list, and the numbers
    python -B scripts/tests/dry_exits.py --judge RESULTS.json [--dir D]      judge `{row id: bool}` against the ledger `D/known_red.json`
    python -B scripts/tests/dry_exits.py --selftest                          the table of cases of this file

The label ledger is the ONE helper `known_red.py` (its reconcile, its raise door); this file only names the ledger file. Unknown never
becomes a pass (AR-28): an unreadable or missing data file is red naming the file, never an empty census; a row with no class source
is `class unknown` and RED (E19), never a guessed class and never a pass (FR-59).
"""
import argparse
import ast
import hashlib
import json
import re
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

HERE = Path(__file__).resolve().parent
PACKAGE = HERE.parents[1]
SCRIPTS = PACKAGE / "scripts"
for _path in (str(SCRIPTS), str(HERE)):
    if _path not in sys.path:
        sys.path.insert(0, _path)

EXITS_DIR = HERE / "fixtures" / "driver-exits"
WALK_DIR = HERE / "fixtures" / "stories" / "dry-1" / "exits"
NOT_GROUP = ("classes.json", "known_red.json")          # the two files of the directory that are no group
SECTIONS = ("routes", "joints", "kinds_without_key")
GROUP_KEYS = ("schema", "group", "routes", "joints", "kinds_without_key", "ratchet")
ROW_KEYS = ("reach", "seed", "why_unreached", "class_source", "raised_at")
RATCHET_COUNTS = ("live_only", "after", "unwalked", "hook_layer")
RATCHET_KEYS = RATCHET_COUNTS + ("raised_by",)
REACH_RE = re.compile(r"^(story|seed|live_only|unwalked|hook_layer|after:[A-Z][A-Z0-9]*-[0-9]+[a-z]?)$")
NEEDS_WHY = ("live_only", "unwalked")                    # `after:<finding>` always needs one too
EXECUTABLE = ("story", "seed")                           # the reach values that mean the row is run (E20)
COUNT_ONLY = ("unwalked", "hook_layer")                  # reaches a WALK row never carries: they are counts of the group files
KEYED = ("closed_question", "priced_section")
PERSON_CALLS = ("Person", "site_seam_person")
UNMATCHED, KNOWN_FALSE = "unmatched", "known_false"
CLASS_UNKNOWN, NOT_A_REFUSAL = "class unknown", "n/a"
RAISE_RE = re.compile(r"^(live_only|after|unwalked|hook_layer) \| (\S.*?) \| (\S.*)$")      # "<count> | <row> | <who, where>" (F2)
MATCH_KNOWN = "match_known"                              # the function whose literal `return "<name>", "<action>"` tuples are routes (F4)
# The keys of a state carrier that hold a clock reading. A short closed list kept here on purpose (AR-1 inside the test layer: the
# fingerprint must ignore them and the carriers are the controller's and the driver's own files); a key ending in `_at` is a clock too.
TIME_KEYS = ("at", "ts", "started", "finished", "stage_started", "stage_finished", "started_at", "finished_at", "asked_at")
STATE_DOOR = "add a row to fixtures/driver-exits/<group>.json with reach seed or live_only (or unwalked, counted in that group's ratchet) and a why_unreached"


class ExitsUnreadable(ValueError):
    """A data file of the census cannot be trusted: the message names the file and what was expected (AR-28)."""


class StateUnreadable(ValueError):
    """A carrier of the world state cannot be read: names the file; a fingerprint over a guess is never made (E7)."""


@dataclass(frozen=True)
class Fingerprint:
    digest: str
    notes: tuple = field(default=(), compare=False)


@dataclass
class Report:
    problems: list = field(default_factory=list)
    notes: list = field(default_factory=list)
    numbers: list = field(default_factory=list)


# ---------------------------------------------------------------------------------------------------- reading
def _no_duplicate_keys(pairs: list) -> dict:
    out: dict = {}
    for key, value in pairs:
        if key in out:
            raise ValueError(f"duplicate key {key!r}")
        out[key] = value
    return out


def _read_json(path: Path, expected: str):
    try:
        text = Path(path).read_text(encoding="utf-8-sig")
    except OSError as exc:
        raise ExitsUnreadable(f"{path}: cannot be read ({exc.__class__.__name__}); expected {expected}") from exc
    try:
        return json.loads(text, object_pairs_hook=_no_duplicate_keys)
    except ValueError as exc:
        raise ExitsUnreadable(f"{path}: not valid JSON ({exc}); expected {expected}") from exc


def _directory(path, what: str) -> Path:
    path = Path(path)
    if not path.is_dir():
        raise ExitsUnreadable(f"{path}: the {what} directory does not exist; expected it to hold one <group>.json per group "
                              f"(node N1 creates fixtures/driver-exits/ with classes.json and known_red.json)")
    return path


def _row_problems(where: str, section: str, name: str, row) -> list:
    if not isinstance(row, dict):
        return [f"{where}: {section} row {name!r} is {type(row).__name__}; expected an object"]
    out = [f"{where}: {section} row {name!r} has unknown field {key!r}; expected only {list(ROW_KEYS)} (the key of a priced question and the "
           f"known_red label are not fields of this directory)" for key in sorted(set(row) - set(ROW_KEYS))]
    reach = row.get("reach")
    if not isinstance(reach, str) or not REACH_RE.match(reach):
        out.append(f"{where}: {section} row {name!r} reach {reach!r}; expected story, seed, live_only, unwalked, hook_layer or "
                   f"after:<finding id> (pattern {REACH_RE.pattern})")
        return out
    if reach in NEEDS_WHY or reach.startswith("after:"):
        why = row.get("why_unreached")
        if not isinstance(why, str) or not why.strip():
            out.append(f"{where}: {section} row {name!r} reach {reach} has no why_unreached; expected one line saying why it is not run")
    if section == "kinds_without_key":
        raised = row.get("raised_at")
        if not isinstance(raised, list) or not raised or not all(isinstance(item, str) and item.strip() for item in raised):
            out.append(f"{where}: kind row {name!r} has no raised_at; expected a list of '<module>:<function>' strings")
    return out


def _group_problems(path: Path, data) -> list:
    where = str(path)
    if not isinstance(data, dict):
        return [f"{where}: the top level is {type(data).__name__}; expected an object with {list(GROUP_KEYS)}"]
    out = [f"{where}: unknown top-level key {key!r}; expected only {list(GROUP_KEYS)}" for key in sorted(set(data) - set(GROUP_KEYS))]
    if data.get("schema") != 1:
        out.append(f"{where}: schema is {data.get('schema')!r}; expected 1")
    if not isinstance(data.get("group"), str) or not data.get("group"):
        out.append(f"{where}: group is {data.get('group')!r}; expected the group name")
    for section in SECTIONS:
        body = data.get(section, {})
        if not isinstance(body, dict):
            out.append(f"{where}: {section} is {type(body).__name__}; expected an object of name -> row")
            continue
        for name, row in body.items():
            out.extend(_row_problems(where, section, name, row))
    ratchet = data.get("ratchet")
    if not isinstance(ratchet, dict):
        out.append(f"{where}: ratchet is {type(ratchet).__name__}; expected an object with {list(RATCHET_KEYS)}")
        return out
    out.extend(f"{where}: ratchet has unknown key {key!r}; expected only {list(RATCHET_KEYS)}" for key in sorted(set(ratchet) - set(RATCHET_KEYS)))
    for key in RATCHET_COUNTS:
        value = ratchet.get(key)
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            out.append(f"{where}: ratchet.{key} is {value!r}; expected a whole number of rows, 0 or more")
    raised = ratchet.get("raised_by")
    if not isinstance(raised, list):
        out.append(f"{where}: ratchet.raised_by is {raised!r}; expected a list of '<count> | <row> | <who, where>' strings")
    else:
        out.extend(f"{where}: ratchet.raised_by entry {item!r} does not fit; expected '<count> | <row> | <who, where>' with the count one of "
                   f"{list(RATCHET_COUNTS)} (one entry per raised row, naming the row)" for item in raised if not _raise_entry(item))
    out.extend(_empty_problems(where, data, ratchet))
    return out


def _raise_entry(item):
    """`(count name, row ref, who)` of a `raised_by` entry, or None when it does not fit the form."""
    match = RAISE_RE.match(item) if isinstance(item, str) else None
    return match.groups() if match else None


def _empty_problems(where: str, data: dict, ratchet: dict) -> list:
    """A group file that carries no row and no count says nothing: refused naming the file (AR-28, never a green empty group)."""
    rows = any(isinstance(data.get(section), dict) and data.get(section) for section in SECTIONS)
    counts = any(isinstance(ratchet.get(key), int) and ratchet.get(key) for key in RATCHET_COUNTS)
    return [] if rows or counts else [f"{where}: carries no row and no ratchet count; expected the rows of its group (or delete the file)"]


def load(directory=None) -> dict:
    """The census files glued: `{"routes": {name: row}, "joints": {...}, "kinds_without_key": {...}, "where": {(section, name): path},
    "base": {count name: sum of the bases}, "raised_by": [...], "classes": {...}, "files": [...]}`. Every `*.json` of the directory except
    `classes.json` and `known_red.json` is a group file. The same id in two files, a file that cannot be read, an unknown field, a missing
    directory, no group file at all: `ExitsUnreadable` naming the file(s) - never an empty census (AR-28)."""
    directory = _directory(directory or EXITS_DIR, "driver-exits")
    files = sorted(p for p in directory.glob("*.json") if p.name not in NOT_GROUP)
    if not files:
        raise ExitsUnreadable(f"{directory}: no group file; expected at least one <group>.json beside classes.json")
    census = {section: {} for section in SECTIONS}
    census.update(where={}, base={name: 0 for name in RATCHET_COUNTS}, raised_by=[], files=files, groups=[])
    problems = []
    for path in files:
        data = _read_json(path, "an object with schema, group, routes, joints, kinds_without_key and ratchet")
        found = _group_problems(path, data)
        if found:
            problems.extend(found)
            continue
        census["groups"].append(data["group"])
        for section in SECTIONS:
            for name, row in (data.get(section) or {}).items():
                if name in census[section]:
                    problems.append(f"{section} id {name!r} is in two group files: {census['where'][(section, name)]} and {path}; "
                                    f"expected each id in exactly one group file")
                    continue
                census[section][name] = row
                census["where"][(section, name)] = path
        for name in RATCHET_COUNTS:
            census["base"][name] += data["ratchet"][name]
        census["raised_by"].extend(data["ratchet"]["raised_by"])
    if problems:
        raise ExitsUnreadable("\n".join(problems))
    census["classes"] = load_classes(directory)
    return census


def load_classes(directory=None) -> dict:
    """`classes.json`: `{"by_source": {source id: class}, "default": null | class}` (spec 3.6). Unreadable: `ExitsUnreadable`."""
    path = Path(directory or EXITS_DIR) / "classes.json"
    data = _read_json(path, "an object with schema, by_source and default")
    if not isinstance(data, dict) or data.get("schema") != 1 or not isinstance(data.get("by_source"), dict) or "default" not in data:
        raise ExitsUnreadable(f"{path}: expected an object with schema 1, a by_source object and a default (null or a class)")
    for source, klass in data["by_source"].items():
        if not isinstance(klass, str) or not klass.strip():
            raise ExitsUnreadable(f"{path}: by_source {source!r} is {klass!r}; expected a non-empty class word")
    default = data["default"]
    if default is not None and (not isinstance(default, str) or not default.strip()):
        raise ExitsUnreadable(f"{path}: default is {default!r}; expected null or a non-empty class word")
    return data


def load_walk_rows(walk_dir=None) -> dict:
    """The walk rows of the dry story, `{id: row + {"_path": path}}`, from `fixtures/stories/dry-1/exits/*.json` (`{"schema": 1, "group":
    g, "rows": [...]}`). The directory is created by the walk nodes (N4): while it is absent there are no rows (TEMPORAL; stated in the
    report). Present but unreadable, a row with no id or reach, an id in two files: `ExitsUnreadable`."""
    walk_dir = Path(walk_dir or WALK_DIR)
    if not walk_dir.is_dir():
        return {}
    rows: dict = {}
    for path in sorted(walk_dir.glob("*.json")):
        data = _read_json(path, "an object with schema, group and rows")
        body = data.get("rows") if isinstance(data, dict) else None
        if not isinstance(body, list):
            raise ExitsUnreadable(f"{path}: expected an object with a rows list")
        for index, row in enumerate(body):
            rid = row.get("id") if isinstance(row, dict) else None
            if not isinstance(rid, str) or "/" not in rid or not rid.split("/", 1)[0] or not rid.split("/", 1)[1]:
                raise ExitsUnreadable(f"{path}: row {index} id {rid!r}; expected '<key|route|joint|kind>/<variant>'")
            found = _row_problems(str(path), "walk", rid, {k: v for k, v in row.items() if k in ROW_KEYS})
            if found:
                raise ExitsUnreadable("\n".join(found))
            if rid in rows:
                raise ExitsUnreadable(f"walk row id {rid!r} is in two files: {rows[rid]['_path']} and {path}; expected each id once")
            rows[rid] = {**row, "_path": path}
    return rows


# ---------------------------------------------------------------------------------------------------- the scans
def _callee(node: ast.Call):
    func = node.func
    return func.id if isinstance(func, ast.Name) else func.attr if isinstance(func, ast.Attribute) else None


def _calls_keyed(expr) -> bool:
    return any(isinstance(inner, ast.Call) and _callee(inner) in KEYED for inner in ast.walk(expr))


def _own_nodes(node):
    """The nodes of a function body that belong to THIS function (a nested function or lambda is another scope)."""
    stack = list(ast.iter_child_nodes(node))
    while stack:
        current = stack.pop()
        yield current
        if not isinstance(current, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)):
            stack.extend(ast.iter_child_nodes(current))


MAX_HOPS = 8     # a guard against pathological input: a chain of more than this many bindings is keyless


def _bindings(function) -> dict:
    """`{name: [expression, ...]}` for the names a function binds by a plain assignment, in that function's OWN scope (every binding of a
    name is kept: a name bound twice holds both expressions)."""
    bound: dict = {}
    for node in _own_nodes(function):
        pairs = ([(t, node.value) for t in node.targets] if isinstance(node, ast.Assign)
                 else [(node.target, node.value)] if isinstance(node, ast.AnnAssign) and node.value is not None else [])
        for target, value in pairs:
            if isinstance(target, ast.Name):
                bound.setdefault(target.id, []).append(value)
    return bound


def _bound_names(expr, bound: dict) -> list:
    return [inner.id for inner in ast.walk(expr) if isinstance(inner, ast.Name) and inner.id in bound]


def _name_keyed(name: str, bound: dict, hops: int, seen: frozenset) -> set:
    """The values (`True` keyed / `False` not) a name can hold, following its bindings through names of the same function. A binding
    cycle yields nothing (it terminates keyless); more than MAX_HOPS bindings in a chain is `{False}`."""
    if name in seen:
        return set()
    if hops > MAX_HOPS:
        return {False}
    found: set = set()
    for value in bound[name]:
        if _calls_keyed(value):
            found.add(True)
            continue
        names = _bound_names(value, bound)
        found |= set().union(*(_name_keyed(n, bound, hops + 1, seen | {name}) for n in names)) if names else {False}
    return found


def _text_keyed(text, bound: dict) -> set:
    """`{True}`, `{False}` or both for the text argument of a Person site: keyed when the expression calls a keyed function itself, or
    is built from names whose binding chain IN THIS FUNCTION reaches such a call (spec 3.2 as amended, followed transitively: `text =
    Priced(body, section.priced)` with `section = self.priced_section(...)` is keyed). Never across functions, attributes of `self` or
    parameters. A name bound twice, once reaching a call and once not, holds both (MIXED); a binding cycle ends keyless; a chain of more
    than 8 bindings (MAX_HOPS) is keyless."""
    if text is None:
        return {False}
    if _calls_keyed(text):
        return {True}
    names = _bound_names(text, bound)
    found = set().union(*(_name_keyed(n, bound, 1, frozenset()) for n in names)) if names else set()
    return found or {False}


class _PersonSites(ast.NodeVisitor):
    def __init__(self, module: str):
        self.module, self.stack, self.sites = module, [], []

    def _function(self, node):
        self.stack.append((node.name, _bindings(node)))
        self.generic_visit(node)
        self.stack.pop()

    visit_FunctionDef = visit_AsyncFunctionDef = _function

    def visit_Call(self, node: ast.Call):
        if _callee(node) in PERSON_CALLS and node.args:
            first = node.args[0]
            kind = first.value if isinstance(first, ast.Constant) and isinstance(first.value, str) else None
            text = node.args[1] if len(node.args) > 1 else next((kw.value for kw in node.keywords if kw.arg == "text"), None)
            name, bound = self.stack[-1] if self.stack else ("<module>", {})
            for keyed in sorted(_text_keyed(text, bound)):
                self.sites.append((kind, f"{self.module}:{name}", keyed))
        self.generic_visit(node)


def person_sites(sources=None) -> list:
    """`[(kind or None, "<module>:<function>", keyed)]` for every `Person(...)` / `site_seam_person(...)` call of the driver sources
    (`harness.driver_sources()`: the ONE reader of that set, AR-13). `kind` is the literal first argument, None when it arrives as a value
    (a name, an f-string, an expression). `keyed` is True when the TEXT argument calls `closed_question(...)` / `priced_section(...)` or is built
    from a name bound in the same function to such a call (spec 3.2 as amended; `_text_keyed`). A name bound twice, once keyed and once not,
    gives the site both values (the kind is MIXED). A source that does not parse is an `ExitsUnreadable`, never skipped."""
    if sources is None:
        import harness
        sources = harness.driver_sources()
    found = []
    for path, text in sources:
        try:
            tree = ast.parse(text, filename=str(path))
        except SyntaxError as exc:
            raise ExitsUnreadable(f"{path}: does not parse ({exc}); expected the driver source to be Python") from exc
        visitor = _PersonSites(Path(path).stem)
        visitor.visit(tree)
        found.extend(visitor.sites)
    return found


def scan_kinds_without_key(sources=None, sites=None) -> dict:
    """`{kind: {"raised_at": [sites WITHOUT a key], "keyed_at": [sites with one]}}` for every literal kind that has at least one site that
    does not pass `closed_question(...)` / `priced_section(...)`. A kind with both sorts of site is listed with its own `raised_at` (the
    keyless ones) - its keyed sites are the existing census's."""
    sites = person_sites(sources) if sites is None else sites
    kinds: dict = {}
    for kind, at, keyed in sites:
        if kind is None:
            continue
        entry = kinds.setdefault(kind, {"raised_at": set(), "keyed_at": set()})
        entry["keyed_at" if keyed else "raised_at"].add(at)
    return {kind: {"raised_at": sorted(e["raised_at"]), "keyed_at": sorted(e["keyed_at"])} for kind, e in sorted(kinds.items()) if e["raised_at"]}


def variable_kind_sites(sources=None, sites=None) -> list:
    """The sites whose kind arrives as a value (a name, an f-string): they cannot be listed by kind, so they are printed (NOTE), not rows."""
    sites = person_sites(sources) if sites is None else sites
    return sorted({at for kind, at, _keyed in sites if kind is None})


def minted_routes(source: str) -> dict:
    """`{name: action}` of the literal `return "<name>", "<action>"` tuples of `match_known` read from its SOURCE by AST: the routes the
    function mints itself, before the table is consulted (the marker branches). A new marker branch is a new tuple and so a route with
    no row (red). No such tuple at all - the function was rewritten - is `ExitsUnreadable`, never zero routes as a pass (F4)."""
    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        raise ExitsUnreadable(f"driver_machine.{MATCH_KNOWN}: its source does not parse ({exc}); could not read the routes of {MATCH_KNOWN}") from exc
    functions = [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == MATCH_KNOWN]
    found = {}
    for function in functions[:1]:
        for node in ast.walk(function):
            pair = node.value.elts if isinstance(node, ast.Return) and isinstance(node.value, ast.Tuple) and len(node.value.elts) == 2 else []
            if pair and all(isinstance(e, ast.Constant) and isinstance(e.value, str) for e in pair):
                found[pair[0].value] = pair[1].value
    if not found:
        raise ExitsUnreadable(f"driver_machine.{MATCH_KNOWN}: could not read the routes of {MATCH_KNOWN} (no literal return \"<name>\", "
                              f"\"<action>\" tuple found); update fixtures/driver-exits and this scan to the function's new shape")
    return found


def scan_minted() -> tuple:
    """The names of the routes `match_known` mints itself, read from the source of the module that holds it."""
    import driver_machine
    return tuple(sorted(minted_routes(Path(driver_machine.__file__).read_text(encoding="utf-8"))))


def scan_routes() -> dict:
    """`{name: action}`: the 21 rows of `driver_dispatch.KNOWN_REFUSALS` BY IMPORT, the routes `match_known` mints itself (`minted_routes`:
    the marker branches), plus the two classes that are no row of the table: `unmatched` (a text no row matches goes to the conductor:
    `driver_machine.match_known` returns None) and `known_false` (a refusal a G step raises, `driver_core.gate_refusal`, is never routed
    by the table). Both are checked by calling the function; a function that stopped behaving so is an `ExitsUnreadable`, not a row that
    silently stays."""
    import driver_core
    import driver_dispatch
    import driver_machine
    routes = {name: action for name, _pattern, action in driver_dispatch.KNOWN_REFUSALS}
    routes.update(minted_routes(Path(driver_machine.__file__).read_text(encoding="utf-8")))
    if driver_machine.match_known("\u0001 text no known refusal row matches \u0001") is not None:
        raise ExitsUnreadable("driver_machine.match_known: a text no row matches no longer returns None; the `unmatched` route is not "
                              "what the census says - update fixtures/driver-exits and this scan")
    if getattr(driver_core.gate_refusal("x.py", 1, "", "y"), "known", True) is not False:
        raise ExitsUnreadable("driver_core.gate_refusal: the refusal is no longer marked known = False; the `known_false` route is not "
                              "what the census says - update fixtures/driver-exits and this scan")
    routes[UNMATCHED] = "conductor"
    routes[KNOWN_FALSE] = "conductor"
    return routes


def scan_prices() -> dict:
    """`{key: [row, ...]}` through `no_move.load_question_prices()` (its one loader); `DataUnreadable` becomes `ExitsUnreadable` naming it."""
    import no_move
    try:
        return no_move.load_question_prices()
    except no_move.DataUnreadable as exc:
        raise ExitsUnreadable(f"question-prices.json: {exc}") from exc


def scan_joints() -> list:
    """The `check` of every joint of `references/stage-joints.json`, through the reader the stage-joints walker itself uses
    (`null_outcomes.load_data` over `stage_joints.DATA`; the file's shape is that walker's audit)."""
    import null_outcomes
    import stage_joints
    data, why = null_outcomes.load_data(stage_joints.DATA)
    if data is None:
        raise ExitsUnreadable(f"stage-joints.json: {why}")
    rows = data.get("joints")
    if not isinstance(rows, list) or not rows or not all(isinstance(r, dict) and isinstance(r.get("check"), str) for r in rows):
        raise ExitsUnreadable("stage-joints.json: expected a non-empty joints list whose rows each hold a text `check`")
    return [r["check"] for r in rows]


@dataclass
class Universe:
    """What the code holds today: the routes, joints, keyless kinds, variable-kind sites, priced questions, hook-layer registry."""
    routes: dict
    joints: list
    kinds: dict
    variable: list
    prices: dict
    registry: list
    scanned: tuple
    errors: list = field(default_factory=list)
    kinds_total: int = 0                   # the literal kinds the driver raises, keyed or not
    unpassable: frozenset = frozenset()    # ids of the registry records whose word does not pass: `refusal_registry.unpassable()` (AR-13)
    minted: tuple = ()                     # the routes `match_known` mints itself (a subset of `routes`), for the numbers

    @classmethod
    def real(cls) -> "Universe":
        errors: list = []

        def read(name, make, empty):
            try:
                return make()
            except ExitsUnreadable as exc:
                errors.append(str(exc))
            except Exception as exc:  # an import that fails is a reason, never an empty universe
                errors.append(f"{name}: cannot be read ({exc.__class__.__name__}: {exc})")
            return empty

        import refusal_registry
        sites = read("driver sources", person_sites, [])
        return cls(routes=read("driver_dispatch.KNOWN_REFUSALS", scan_routes, {}), joints=read("stage-joints.json", scan_joints, []),
                   kinds=scan_kinds_without_key(sites=sites), variable=variable_kind_sites(sites=sites),
                   prices=read("question-prices.json", scan_prices, {}), registry=list(refusal_registry.REGISTRY),
                   scanned=tuple(refusal_registry.SCANNED), errors=errors,
                   kinds_total=len({kind for kind, _at, _keyed in sites if kind}),
                   unpassable=frozenset(str(r.get("id")) for r in refusal_registry.unpassable()),
                   minted=read("driver_machine.match_known", scan_minted, ()))


# ---------------------------------------------------------------------------------------------------- classes, doors
def registry_kinds(registry) -> dict:
    return {str(r.get("id")): ("operation" if r.get("kind") == "operation" else "scanned") for r in registry if isinstance(r, dict)}


def class_of(row, classes: dict, *, section: str, action: str = "", joints=(), registry=()) -> str:
    """The class of a census row by its SOURCE (spec 3.6; the rule is data in `classes.json`, not a list here). A joint: source `stage-joints`.
    A route whose move is `ask_person`: the source its `class_source` names - a joint check, a REGISTRY id (operation or scanned), a
    `question:<key>` id, or any other `by_source` key directly. A route with a code move and a kind of question are no refusal text a person
    reads: `n/a`. A source that is not named, not found, or not in `by_source` with no default: `class unknown` - RED in `check` (E19), never a
    guess (FR-59)."""
    if section != "joints" and not (section == "routes" and action == "ask_person"):
        return NOT_A_REFUSAL
    source = "stage-joints" if section == "joints" else None
    if section == "routes":
        named = row.get("class_source") if isinstance(row, dict) else None
        if not isinstance(named, str) or not named.strip():
            return CLASS_UNKNOWN
        if named in set(joints):
            source = "stage-joints"
        elif named in registry_kinds(registry):
            source = f"refusal_registry:{registry_kinds(registry)[named]}"
        elif named.startswith("question:") or named in classes.get("by_source", {}):
            source = named
    klass = classes.get("by_source", {}).get(source) if source else None
    return klass or classes.get("default") or CLASS_UNKNOWN


def _hook_bans(universe: Universe) -> list:
    """The registry records of the hook layer: a scanned file, no operation."""
    return [r for r in universe.registry if r.get("file") in universe.scanned and r.get("kind") != "operation"]


def ban_doors(universe: Universe) -> list:
    """The ids of the hook-layer records whose word does not pass (`universe.unpassable`, read through `refusal_registry.unpassable()`, the
    ONE reader of that fact - AR-13) and whose door is not named (`unpassable_because` empty or blank): FR-57, a ban is never a dead end.
    Only the DATA of the registry is read; the hooks are not run (F11)."""
    out = []
    for record in _hook_bans(universe):
        door = record.get("unpassable_because")
        if str(record.get("id")) in universe.unpassable and (not isinstance(door, str) or not door.strip()):
            out.append(str(record.get("id")))
    return out


def class_counts(universe: Universe, classes: dict) -> dict:
    """The numbers of spec 3.6: hook bans the word does not pass / pass, operations (and of them the word does not pass), joints, and the
    closed questions of `classes.json` (`question:<key>` sources whose key is in the prices)."""
    bans = _hook_bans(universe)
    operations = [r for r in universe.registry if r.get("kind") == "operation"]
    stuck = sum(1 for r in bans if str(r.get("id")) in universe.unpassable)
    questions = [s for s in classes.get("by_source", {}) if s.startswith("question:") and s[len("question:"):] in universe.prices]
    return {"ban_unpassable": stuck, "ban_passable": len(bans) - stuck, "gate_operations": len(operations),
            "gate_operations_unpassable": sum(1 for r in operations if str(r.get("id")) in universe.unpassable),
            "gate_joints": len(universe.joints), "gate_questions": len(questions)}


# ---------------------------------------------------------------------------------------------------- the census
def _side(universe: Universe) -> dict:
    return {"routes": set(universe.routes), "joints": set(universe.joints), "kinds_without_key": set(universe.kinds)}


def _count_reach(census: dict, walk: dict) -> dict:
    counts = {"live_only": 0, "after": 0, "unwalked": 0}
    rows = [row for section in SECTIONS for row in census[section].values()] + list(walk.values())
    for row in rows:
        reach = str(row.get("reach"))
        key = "after" if reach.startswith("after:") else reach
        if key in counts:
            counts[key] += 1
    return counts


def check(directory=None, walk_dir=None, universe: Universe | None = None, ledger_path=None) -> Report:
    """The census of spec 3.2, both directions, with every discrepancy carrying its door. Returns a `Report`; nothing is raised for a
    data fault (a fault is a problem line naming the file)."""
    report = Report()
    red = report.problems.append
    directory = Path(directory or EXITS_DIR)
    try:
        census = load(directory)
    except ExitsUnreadable as exc:
        red(str(exc))
        return report
    try:
        walk = load_walk_rows(walk_dir)
    except ExitsUnreadable as exc:
        red(str(exc))
        return report
    universe = universe or Universe.real()
    report.problems.extend(universe.errors)
    if universe.errors:                        # a census over a carrier that could not be read is no census
        return report
    if not walk:
        report.notes.append(f"walk rows: none ({walk_dir or WALK_DIR} holds no rows yet; the walk nodes N4 write them)")
    _code_rows(census, universe, red)
    _walk_problems(census, walk, universe, red)
    counts = _ratchets(census, walk, universe, report)
    _classes_and_doors(census, universe, red)
    _ledger(Path(ledger_path or directory / "known_red.json"), red)
    report.numbers = _numbers(census, universe, counts)
    return report


def _code_rows(census: dict, universe: Universe, red) -> None:
    """Section 1 of the census: code <-> rows, both directions, and where each keyless kind is raised."""
    labels = {"routes": "route", "joints": "joint", "kinds_without_key": "kind without a key"}
    for section, code_ids in _side(universe).items():
        rows = census[section]
        for name in sorted(code_ids - set(rows)):
            red(f"{labels[section]} {name}: the driver has it and no row names it; {STATE_DOOR}")
        for name in sorted(set(rows) - code_ids):
            red(f"{labels[section]} {name}: stale row in {census['where'][(section, name)]}; the driver no longer has it - remove the row")
    for name, entry in universe.kinds.items():
        row = census["kinds_without_key"].get(name)
        if row and set(row.get("raised_at") or []) != set(entry["raised_at"]):
            red(f"kind without a key {name}: raised_at {sorted(row.get('raised_at') or [])} in {census['where'][('kinds_without_key', name)]} "
                f"differs from the driver's {entry['raised_at']}; make the row say where the question is raised")


def _walk_problems(census: dict, walk: dict, universe: Universe, red) -> None:
    """Section 2: the walk rows against the census, in both directions. A row's subject exists; a walk row never carries a count reach; a
    census row that claims it is run (`seed`/`story`) has a walk row behind it (E1, AR-28)."""
    subjects = set(universe.prices) | set(census["routes"]) | set(census["joints"]) | set(census["kinds_without_key"])
    walked = {rid.split("/", 1)[0] for rid in walk}
    for rid, row in sorted(walk.items()):
        subject, reach = rid.split("/", 1)[0], str(row.get("reach"))
        if subject not in subjects:
            red(f"walk row {rid} ({row['_path']}): {subject!r} is not a key of question-prices.json, a route, a joint or a kind without a key; "
                f"fix the id, or add the key/route to its table")
        if reach in COUNT_ONLY:
            red(f"walk row {rid}: reach {reach} is a count of the group files, not a walk row's reach; give the row story, seed, live_only or "
                f"after:<finding>, or remove it")
    for section in SECTIONS:
        for name, row in sorted(census[section].items()):
            reach = str(row.get("reach"))
            if reach == "hook_layer":
                red(f"{section[:-1]} {name}: reach hook_layer is a count (the hook refusals are not rows of a group file); fix the row")
            if reach in EXECUTABLE and name not in walked:
                red(f"{section[:-1]} {name} ({census['where'][(section, name)]}): claims reach {reach} and no walk row names it; write the row "
                    f"in fixtures/stories/dry-1/exits/<group>.json, or set the row's reach to unwalked and count it in the group's ratchet")


def _raised(census: dict, walk: dict, universe: Universe) -> tuple:
    """`({count name: [valid entry text]}, [problem])`: each `raised_by` entry names its count and ITS row; the row must exist and carry
    that count's reach (a hook_layer entry names a scanned registry id). An entry whose row is gone, or twice for one row, is stale."""
    refs = {"hook_layer": {str(r.get("id")) for r in _hook_bans(universe)}}
    for key in ("live_only", "unwalked"):
        refs[key] = {f"{section}/{name}" for section in SECTIONS for name, row in census[section].items() if row.get("reach") == key}
        refs[key] |= {f"walk/{rid}" for rid, row in walk.items() if row.get("reach") == key}
    refs["after"] = {f"{section}/{name}" for section in SECTIONS for name, row in census[section].items() if str(row.get("reach")).startswith("after:")}
    refs["after"] |= {f"walk/{rid}" for rid, row in walk.items() if str(row.get("reach")).startswith("after:")}
    valid: dict = {key: [] for key in RATCHET_COUNTS}
    problems, seen = [], set()
    for item in census["raised_by"]:
        count, row, _who = _raise_entry(item)
        if row not in refs[count]:
            problems.append(f"ratchet {count}: stale raise {item!r}: its row {row!r} is gone or no longer has that reach; drop the entry")
        elif (count, row) in seen:
            problems.append(f"ratchet {count}: raise {item!r} names a row twice; one entry per row")
        else:
            seen.add((count, row))
            valid[count].append(item)
    return valid, problems


def _ratchets(census: dict, walk: dict, universe: Universe, report: Report) -> dict:
    """Section 3: the sum over the group files against the bases. Each count has its OWN credit: count == base + the entries of `raised_by`
    that name that count and a live row - above it is an unnamed raise, below it a stale credit (AR-20, one stale semantics). Returns the counts."""
    counts = _count_reach(census, walk)
    counts["hook_layer"] = len(_hook_bans(universe))
    valid, problems = _raised(census, walk, universe)
    report.problems.extend(problems)
    for name in RATCHET_COUNTS:
        base, count, named = census["base"][name], counts[name], len(valid[name])
        if count < base:
            report.problems.append(f"ratchet {name}: stale base: {count} rows, below the base {base}; lower the base to {count} in the group files")
        elif count > base + named:
            report.problems.append(f"ratchet {name}: {count} rows, above the base {base}, and ratchet.raised_by names {named} raise(s) of {name}; a "
                                   f"raise needs one entry '{name} | <row> | <who, where>' per row, then the base is lowered back by fixing the rows")
        elif named > max(count - base, 0):
            report.problems.append(f"ratchet {name}: stale raise credit: {named} raised_by entr{'y' if named == 1 else 'ies'} for {name}, "
                                   f"{max(count - base, 0)} row(s) above the base {base}; drop the surplus entry or lower the base")
        elif count > base:
            report.notes.append(f"ratchet {name}: raised {count - base} row(s) above the base {base}, named in raised_by: {valid[name]}")
    return counts


def _classes_and_doors(census: dict, universe: Universe, red) -> None:
    """Section 4: every refusal row has a class (E19: `class unknown` is red), and every hook ban the word does not pass names its door."""
    for section in ("routes", "joints"):
        for name, row in sorted(census[section].items()):
            klass = class_of(row, census["classes"], section=section, action=universe.routes.get(name, ""),
                             joints=universe.joints, registry=universe.registry)
            if klass == CLASS_UNKNOWN:
                red(f"{section[:-1]} {name}: class unknown; name a class_source for the row (a joint check, a REGISTRY id, question:<key> or a "
                    f"by_source key) and its class in fixtures/driver-exits/classes.json - the class is never guessed (FR-59)")
    for rid in ban_doors(universe):
        red(f"hook refusal {rid}: its word does not pass (override '') and unpassable_because names no door (FR-57); name the door in refusal_registry.py")


def _ledger(ledger: Path, red) -> None:
    """Section 5: the label ledger of the helper, read through it."""
    try:
        import known_red
        stale = known_red.pin_problem(ledger, "known_red", len(known_red.load(ledger)))
        if stale:
            red(stale)
    except Exception as exc:  # LedgerError names the file and the row
        red(f"{ledger}: {exc}")


def _numbers(census: dict, universe: Universe, counts: dict) -> list:
    """The NUMBER lines, each with a recount command that prints the figure(s) of its own line."""
    minted = list(universe.minted)
    table = len(universe.routes) - len(minted) - 2
    options = sum(len(rows) for rows in universe.prices.values())
    by: dict = {}
    for check_id in universe.joints:
        by[check_id.split(":", 1)[0]] = by.get(check_id.split(":", 1)[0], 0) + 1
    n = class_counts(universe, census["classes"])
    mixed = sorted(name for name, e in universe.kinds.items() if e["keyed_at"])
    return [
        f"routes: {table} KNOWN_REFUSALS + {len(minted)} minted by match_known ({', '.join(sorted(minted))}) + 2 (unmatched, known_false) = "
        f"{len(universe.routes)}   [recount: python -B -c \"import driver_dispatch as D; print(len(D.KNOWN_REFUSALS))\" in scripts/ prints {table}; "
        f"grep -cE 'return .marked_' driver_machine.py prints {len(minted)}]",
        f"price keys: {len(universe.prices)}, options: {options}   "
        f"[recount: python -B -c \"import no_move as N; p=N.load_question_prices(); print(len(p), sum(map(len, p.values())))\" in scripts/]",
        f"joints: {len(universe.joints)} ({', '.join(f'{k} {v}' for k, v in sorted(by.items()))})   "
        f"[recount: python -B -c \"import null_outcomes as O, stage_joints as J; print(len(O.load_data(J.DATA)[0]['joints']))\" in scripts/]",
        f"kinds without a key: {len(universe.kinds)} of {universe.kinds_total} literal kinds ({len(universe.kinds) - len(mixed)} keyless, "
        f"{len(mixed)} mixed: {', '.join(mixed) or 'none'}); sites with a kind that arrives as a value: {len(universe.variable)} "
        f"({', '.join(universe.variable) or 'none'})   [recount: grep -ohE \"(Person|site_seam_person)\\(\\s*['\\\"][a-z_0-9]+['\\\"]\" "
        f"driver_*.py | sort -u | wc -l prints the literal kinds; the rows are the kinds_without_key keys of the group files]",
        f"classes, bans: word-does-not-pass {n['ban_unpassable']} / word-passes {n['ban_passable']}   [recount: python -B -c \"import "
        f"refusal_registry as R; b=[r for r in R.REGISTRY if r.get('file') in R.SCANNED and r.get('kind')!='operation']; u=R.unpassable(); "
        f"print(sum(r in u for r in b), sum(r not in u for r in b))\" in scripts/]",
        f"classes, gates: operations {n['gate_operations']} (of them override '': {n['gate_operations_unpassable']}) / joints {n['gate_joints']} / "
        f"questions {n['gate_questions']}   [recount: python -B -c \"import refusal_registry as R, no_move as N, json; o=[r for r in R.REGISTRY "
        f"if r.get('kind')=='operation']; c=json.load(open('tests/fixtures/driver-exits/classes.json')); p=N.load_question_prices(); "
        f"print(len(o), sum(r in R.unpassable() for r in o), sum(s[9:] in p for s in c['by_source'] if s.startswith('question:')))\" in scripts/]",
        f"ban_doors without a named door: {len(ban_doors(universe))}   [recount: python -B -c \"import refusal_registry as R; print(sum(1 for r in "
        f"R.unpassable() if r.get('file') in R.SCANNED and r.get('kind')!='operation' and not str(r.get('unpassable_because') or '').strip()))\" in scripts/]",
        "ratchet (rows now / base): " + ", ".join(f"{k} {counts[k]}/{census['base'][k]}" for k in RATCHET_COUNTS)
        + f"; raised_by {len(census['raised_by'])}",
        f"groups: {', '.join(census['groups'])}"]


def judge(results: dict, ledger_path) -> tuple:
    """`(ok, lines)`: the walk's `{row id: bool}` judged against the ledger file by the ONE helper (`known_red.reconcile`); this file adds
    nothing to its reading. A ledger that cannot be read is red naming the file."""
    import known_red
    try:
        ledger = known_red.load(ledger_path)
        verdict = known_red.reconcile(results, ledger, ledger_path=str(ledger_path))
    except known_red.LedgerError as exc:
        return False, [f"{ledger_path}: {exc}"]
    return verdict.ok, [*verdict.problems, *verdict.known]


# ---------------------------------------------------------------------------------------------------- driven keys
def driven_keys(walk_dir=None, prices=None) -> set:
    """The price keys the dry story drives (spec 3.2, E20): a key whose EVERY answer row (`<key>/<answer>`) is a walk row with reach `story`
    or `seed` (a pass and a `known_red` are both driven). A key with one answer row `live_only` / `after:<finding>` / missing is NOT in the
    set: the existing census keeps its `PINNED_ELSEWHERE` entry. Unreadable rows or prices: an error, never an empty set (AR-28)."""
    rows = load_walk_rows(walk_dir)
    prices = scan_prices() if prices is None else prices
    out = set()
    for key, answers in prices.items():
        wanted = [f"{key}/{row['answer']}" for row in answers]
        if wanted and all(rid in rows and str(rows[rid].get("reach")) in EXECUTABLE for rid in wanted):
            out.add(key)
    return out


# ---------------------------------------------------------------------------------------------------- the state fingerprint
def _dispatch_normalized(text: str) -> str:
    from driver_core import DISPATCH_ID_RE
    return DISPATCH_ID_RE.sub("<dispatch>", text)


def _strip_time(value):
    if isinstance(value, dict):
        return {k: _strip_time(v) for k, v in sorted(value.items()) if k not in TIME_KEYS and not str(k).endswith("_at")}
    if isinstance(value, list):
        return [_strip_time(item) for item in value]
    return value


def _file_hash(path: Path) -> str:
    raw = path.read_bytes()
    try:
        text = _dispatch_normalized(raw.decode("utf-8-sig"))
    except UnicodeDecodeError:
        return hashlib.sha256(raw).hexdigest()
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _json_carrier(path: Path, expected: str):
    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, ValueError) as exc:
        raise StateUnreadable(f"{path}: cannot be read as JSON ({exc.__class__.__name__}); expected {expected}") from exc


def _stage_outputs(stages=None) -> dict:
    if stages is None:
        import hooklib
        stages = hooklib.load_ref_json("stages.json")
    if not isinstance(stages, dict) or not isinstance(stages.get("stages"), list):
        raise StateUnreadable("references/stages.json: cannot be read; expected an object with a stages list")
    return {str(s.get("id")): [str(o) for o in s.get("outputs") or [] if not str(o).startswith("project:")]
            for s in stages["stages"] if isinstance(s, dict)}


def state_fingerprint(task_root, stages=None) -> Fingerprint:
    """A hash of the state of the world a driver step leaves (spec 3.4): the stage statuses, the gate decisions and the `acceptance` records
    of `pipeline.json`; the statuses of the controller's dispatches (ids normalised by `DISPATCH_ID_RE`); the ROUND of each dispatch by (stage,
    role) from `retro_numbers.dispatch_rounds`; the hashes of the filled handoff forms `work/handoffs/*.yaml` keyed by (stage, role, round),
    normalised the same way; `asked.kind/stage` of `driver-state.json`; the hashes of the stage outputs `stages.json` declares. No time in
    it. A new legitimate round is a NEW state even when a deterministic stub writes the same bytes. Without `state/controller.json` the rounds
    are unknown: they are left out and the notes say `rounds unknown` (E7) - never read as no rounds. An unreadable carrier raises
    `StateUnreadable` naming it."""
    import retro_numbers
    root, notes = Path(task_root), []
    pipeline = _json_carrier(root / "pipeline.json", "the story's pipeline.json (an object)") or {}
    if not isinstance(pipeline, dict):
        raise StateUnreadable(f"{root / 'pipeline.json'}: is {type(pipeline).__name__}; expected an object")
    controller = _json_carrier(root / "state" / "controller.json", "the controller's projection (an object with dispatches)") or {}
    asked = ((_json_carrier(root / "state" / "driver-state.json", "the driver's state (an object)") or {}).get("asked") or {})
    parts = {"stages": {sid: (s or {}).get("status") for sid, s in sorted((pipeline.get("stages") or {}).items()) if isinstance(s, dict)},
             "gates": _strip_time(pipeline.get("gates") or {}), "acceptance": _strip_time(pipeline.get("acceptance") or {}),
             "asked": {"kind": str(asked.get("kind") or ""), "stage": str(asked.get("stage") or "")}}
    records = controller.get("dispatches") if isinstance(controller, dict) else None
    parts["dispatches"] = sorted((_dispatch_normalized(str(k)), str((v or {}).get("status") or "")) for k, v in (records or {}).items()
                                 if isinstance(v, dict))
    rounds = retro_numbers.dispatch_rounds(root)
    by_id = {row["id"]: row["round"] for row in rounds}
    if rounds:
        parts["rounds"] = sorted((row["stage"], row["role"], row["round"]) for row in rounds)
    else:
        notes.append("rounds unknown: no dispatch records in state/controller.json, so the rounds are not part of this fingerprint")
    forms = {}
    for form in sorted((root / "work" / "handoffs").glob("*.yaml")) if (root / "work" / "handoffs").is_dir() else []:
        match = re.match(r"^(S\d+)-(qa-[a-z-]+)-(\d+)$", form.stem)
        stage, role = (match.group(1), match.group(2)) if match else ("", form.stem)
        circle = by_id.get(form.stem, int(match.group(3)) if match and not rounds else None)
        forms[f"{stage}|{role}|{circle}"] = _file_hash(form)
    parts["forms"] = forms
    outputs = {}
    for stage, names in sorted(_stage_outputs(stages).items()):
        for name in names:
            target = root / name.rstrip("/")
            if name.endswith("/"):
                outputs[f"{stage}:{name}"] = sorted((p.relative_to(target).as_posix(), _file_hash(p)) for p in target.rglob("*") if p.is_file()) \
                    if target.is_dir() else "absent"
            else:
                outputs[f"{stage}:{name}"] = _file_hash(target) if target.is_file() else "absent"
    parts["outputs"] = outputs
    digest = hashlib.sha256(json.dumps(parts, sort_keys=True, ensure_ascii=True).encode("ascii")).hexdigest()
    return Fingerprint(digest=digest, notes=tuple(notes))


def author_input_sha(prompt: str) -> str:
    """The hash of the author's input (the prompt a stub got for a new round) with real dispatch ids replaced (C5): a prompt that differs only
    by the id of its dispatch is the same input."""
    return hashlib.sha256(" ".join(_dispatch_normalized(str(prompt or "")).split()).encode("utf-8")).hexdigest()


def _ask_identity(ask: dict) -> tuple:
    from driver_dialog import DriverDialog
    tokens = ask.get("tokens") if ask.get("tokens") is not None else ask.get("offered") or []
    from driver_core import DISPATCH_ID_RE
    dispatch = DISPATCH_ID_RE.sub(lambda m: m.group(0).rsplit("-", 1)[0] + "-<n>", str(ask.get("dispatch") or ""))    # the number goes, stage and role stay
    return (str(ask.get("key") or ask.get("kind") or ""), str(ask.get("stage") or "").strip(), dispatch,
            frozenset(t for t in (DriverDialog.s0_normalize(token) for token in tokens) if t))


def same_ask(first: dict, second: dict) -> bool:
    """C5: are two asks (a row of `driver-questions.jsonl` or a call of the conductor) the same? They are when (price key or kind, stage,
    dispatch with its number replaced (`DISPATCH_ID_RE` finds the id; stage and role stay), the SET of offered tokens, each normalised by the driver's own `s0_normalize`) agree.
    The text, `asked_at`, and the FR-7 block are not compared. Direction of error: two nearly equal asks merge into one (a false red, one
    review); one ask is never counted as two (that would pass a loop)."""
    return _ask_identity(first) == _ask_identity(second)


# ---------------------------------------------------------------------------------------------------- the selftest
def _write(path: Path, data) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(data if isinstance(data, str) else json.dumps(data), encoding="utf-8")
    return path


def _ratchet(**kw) -> dict:
    base = {"live_only": 0, "after": 0, "unwalked": 0, "hook_layer": 0, "raised_by": []}
    base.update(kw)
    return base


def _group(name="g", **sections) -> dict:
    ratchet = sections.pop("ratchet", _ratchet())
    return {"schema": 1, "group": name, "routes": {}, "joints": {}, "kinds_without_key": {}, "ratchet": ratchet, **sections}


def _row(reach="unwalked", **kw) -> dict:
    return {"reach": reach, "seed": None, "why_unreached": kw.pop("why", "x"), **kw}


def _universe(**kw) -> Universe:
    base = dict(routes={"r1": "continue", UNMATCHED: "conductor"}, joints=["exit:j1"], kinds={"k1": {"raised_at": ["m:f"], "keyed_at": []}},
                variable=[], prices={"p.key": [{"answer": "a"}, {"answer": "b"}]}, registry=[], scanned=("stage_guard.py",))
    base.update(kw)
    return Universe(**base)


def _tree(root: Path, group=None, classes=None, ledger=None) -> Path:
    directory = root / "driver-exits"
    _write(directory / "g.json", group or _group(routes={"r1": _row(), UNMATCHED: _row()}, joints={"exit:j1": _row()},
                                                 kinds_without_key={"k1": _row(raised_at=["m:f"])}, ratchet=_ratchet(unwalked=4)))
    _write(directory / "classes.json", classes or {"schema": 1, "by_source": {"stage-joints": "gate"}, "default": None})
    _write(directory / "known_red.json", ledger or {"known_red": {}, "pins": {"known_red": 0}})
    return directory


def _selftest_cases() -> list:
    """`[(case id, callable returning None for pass or a string for the failure)]` - one row per case, the id names it."""
    cases = []

    def case(name):
        def register(fn):
            cases.append((name, fn))
            return fn
        return register

    def tmp():
        return Path(tempfile.mkdtemp(prefix="dry-exits-"))

    def src(text, name="m.py"):
        return [(Path(name), text)]

    # ---- item 1: the scan of kinds
    @case("scan: a literal kind whose site passes no key is listed with its site")
    def _():
        got = scan_kinds_without_key(src("def f(self):\n    raise Person('alpha', text, 'S1')\n"))
        return None if got == {"alpha": {"raised_at": ["m:f"], "keyed_at": []}} else f"got {got}"

    @case("scan: closed_question inside the call keys it, so it is not listed")
    def _():
        got = scan_kinds_without_key(src("def f(self):\n    raise Person('alpha', self.closed_question('a.key', lead, o), 'S1')\n"))
        return None if got == {} else f"got {got}"

    @case("scan: site_seam_person with priced_section is keyed")
    def _():
        got = scan_kinds_without_key(src("def f(self):\n    return self.site_seam_person('beta', self.priced_section('b.key', o), 'S3')\n"))
        return None if got == {} else f"got {got}"

    @case("scan: a kind with a keyed and a keyless site is listed with the keyless one only")
    def _():
        text = ("def keyed(self):\n    return Person('mix', self.closed_question('m.key', l, o), 'S1')\n"
                "def bare(self):\n    return Person('mix', text, 'S1')\n")
        got = scan_kinds_without_key(src(text))
        return None if got == {"mix": {"raised_at": ["m:bare"], "keyed_at": ["m:keyed"]}} else f"got {got}"

    @case("scan: a text bound in the same function to a closed_question call keys the site (the key one statement earlier)")
    def _():
        text = ("def f(self):\n    text = self.closed_question('a.key', lead, o)\n    raise Person('alpha', text, 'S1')\n"
                "def g(self):\n    body = self.priced_section('b.key', o)\n    return self.site_seam_person('beta', lead + body, 'S1')\n")
        got = scan_kinds_without_key(src(text))
        return None if got == {} else f"got {got}"

    @case("scan: a text bound to a plain string in the same function stays keyless")
    def _():
        got = scan_kinds_without_key(src("def f(self):\n    text = 'no key here'\n    raise Person('alpha', text, 'S1')\n"))
        return None if got == {"alpha": {"raised_at": ["m:f"], "keyed_at": []}} else f"got {got}"

    @case("scan: a name bound twice in one function, once keyed and once not, makes the kind MIXED, not keyed")
    def _():
        text = "def f(self, c):\n    text = self.closed_question('a.key', l, o)\n    if c:\n        text = 'plain'\n    raise Person('alpha', text, 'S1')\n"
        got = scan_kinds_without_key(src(text))
        return None if got == {"alpha": {"raised_at": ["m:f"], "keyed_at": ["m:f"]}} else f"got {got}"

    @case("scan: a key bound in ANOTHER function (or an enclosing one) does not key the site; a text= keyword is the text")
    def _():
        text = ("def other(self):\n    text = self.closed_question('a.key', l, o)\n"
                "def f(self):\n    raise Person('alpha', text, 'S1')\n"
                "def outer(self):\n    text = self.closed_question('b.key', l, o)\n    def inner():\n        raise Person('beta', text, 'S1')\n"
                "def h(self):\n    raise Person('gamma', text=self.closed_question('c.key', l, o), stage='S1')\n")
        got = scan_kinds_without_key(src(text))
        return None if sorted(got) == ["alpha", "beta"] else f"got {sorted(got)}"

    def chain(length, end="self.priced_section('a.key', o)"):
        """A function whose site text is bound through `length` bindings: n1 = Priced(n2) ... n<length> = <end>."""
        lines = [f"    n{i} = Priced(n{i + 1})" for i in range(1, length)] + [f"    n{length} = {end}"]
        return "def f(self):\n" + "\n".join(lines) + "\n    raise Person('alpha', n1, 'S1')\n"

    @case("scan: a two-hop chain (text = Priced(body, section.priced), section = priced_section(..)) keys the site")
    def _():
        text = "def f(self):\n    section = self.priced_section('a.key', o)\n    text = Priced(body, section.priced)\n    raise Person('alpha', text, 'S1')\n"
        got = scan_kinds_without_key(src(text))
        return None if got == {} else f"got {got}"

    @case("scan: a chain through a name bound twice (once reaching a call, once not) is MIXED")
    def _():
        text = ("def f(self, c):\n    section = self.priced_section('a.key', o)\n    if c:\n        section = 'plain'\n"
                "    text = Priced(body, section)\n    raise Person('alpha', text, 'S1')\n")
        got = scan_kinds_without_key(src(text))
        return None if got == {"alpha": {"raised_at": ["m:f"], "keyed_at": ["m:f"]}} else f"got {got}"

    @case("scan: a binding cycle (a = b; b = a) terminates and stays keyless")
    def _():
        got = scan_kinds_without_key(src("def f(self):\n    a = b\n    b = a\n    raise Person('alpha', a, 'S1')\n"))
        return None if got == {"alpha": {"raised_at": ["m:f"], "keyed_at": []}} else f"got {got}"

    @case("scan: a chain of 8 bindings keys the site, a chain of 9 is keyless (the hop limit)")
    def _():
        at8, at9 = scan_kinds_without_key(src(chain(8))), scan_kinds_without_key(src(chain(9)))
        if at8 != {}:
            return f"8 hops: got {at8}"
        return None if at9 == {"alpha": {"raised_at": ["m:f"], "keyed_at": []}} else f"9 hops: got {at9}"

    @case("scan: a chain does not follow a parameter or an attribute of self set elsewhere")
    def _():
        text = ("def f(self, section):\n    text = Priced(body, section)\n    raise Person('alpha', text, 'S1')\n"
                "def g(self):\n    text = Priced(body, self.section)\n    raise Person('beta', text, 'S1')\n")
        got = scan_kinds_without_key(src(text))
        return None if sorted(got) == ["alpha", "beta"] else f"got {sorted(got)}"

    @case("scan: a kind that arrives as a value is no row and is counted as a variable site")
    def _():
        text = "def f(self, kind):\n    raise Person(kind, text, 'S1')\ndef g(self, gate):\n    raise Person(f'gate_{gate}', text)\n"
        sites = person_sites(src(text))
        got = (scan_kinds_without_key(sites=sites), variable_kind_sites(sites=sites))
        return None if got == ({}, ["m:f", "m:g"]) else f"got {got}"

    @case("scan: the text of a docstring that shows Person('x') is no site")
    def _():
        got = person_sites(src('def f(self):\n    """POSITION: Person(gate_X) is never raised; Person(\'x\')"""\n'))
        return None if got == [] else f"got {got}"

    @case("scan: a source that does not parse is refused naming the file, never skipped")
    def _():
        try:
            person_sites(src("def (:\n", "bad.py"))
        except ExitsUnreadable as exc:
            return None if "bad.py" in str(exc) else f"did not name the file: {exc}"
        return "no refusal"

    # ---- item 5: load
    @case("load: the same route id in two group files is red naming both paths")
    def _():
        root = tmp()
        directory = _tree(root)
        _write(directory / "h.json", _group("h", routes={"r1": _row()}))
        try:
            load(directory)
        except ExitsUnreadable as exc:
            text = str(exc)
            return None if str(directory / "g.json") in text and str(directory / "h.json") in text else f"paths missing: {text}"
        return "no refusal"

    @case("load: a missing driver-exits directory is red naming it and what was expected (temporal: before N1)")
    def _():
        missing = tmp() / "driver-exits"
        report = check(missing, universe=_universe())
        text = " ".join(report.problems)
        return None if str(missing) in text and "does not exist" in text and "Traceback" not in text else f"got {report.problems}"

    @case("load: a group file that is not JSON is red naming the file")
    def _():
        directory = _tree(tmp())
        _write(directory / "g.json", "{not json")
        try:
            load(directory)
        except ExitsUnreadable as exc:
            return None if "g.json" in str(exc) else f"got {exc}"
        return "no refusal"

    @case("load: a duplicate key inside one file is refused")
    def _():
        directory = _tree(tmp())
        _write(directory / "g.json", '{"schema": 1, "schema": 1}')
        try:
            load(directory)
        except ExitsUnreadable as exc:
            return None if "duplicate key" in str(exc) else f"got {exc}"
        return "no refusal"

    @case("load: a price_keys field is not a field of the directory")
    def _():
        directory = _tree(tmp())
        data = _group(routes={"r1": {**_row(), "price_keys": ["x"]}})
        _write(directory / "g.json", data)
        try:
            load(directory)
        except ExitsUnreadable as exc:
            return None if "price_keys" in str(exc) else f"got {exc}"
        return "no refusal"

    @case("load: no group file at all is red, not an empty census")
    def _():
        directory = tmp() / "driver-exits"
        _write(directory / "classes.json", {"schema": 1, "by_source": {}, "default": None})
        try:
            load(directory)
        except ExitsUnreadable as exc:
            return None if "no group file" in str(exc) else f"got {exc}"
        return "no refusal"

    @case("load: reach live_only with no why_unreached is refused; an after: reach needs one too")
    def _():
        for reach in ("live_only", "after:FV1-1"):
            directory = _tree(tmp())
            _write(directory / "g.json", _group(routes={"r1": _row(reach, why=None)}))
            try:
                load(directory)
            except ExitsUnreadable as exc:
                if "why_unreached" not in str(exc):
                    return f"{reach}: {exc}"
            else:
                return f"{reach}: no refusal"
        return None

    # ---- item 6: check
    @case("check: a complete table is 0 discrepancies")
    def _():
        report = check(_tree(tmp()), universe=_universe())
        return None if not report.problems else f"got {report.problems}"

    @case("check: a route removed from its group file is red naming the route and the door")
    def _():
        directory = _tree(tmp(), _group(routes={UNMATCHED: _row()}, joints={"exit:j1": _row()}, kinds_without_key={"k1": _row(raised_at=["m:f"])}))
        report = check(directory, universe=_universe())
        text = "\n".join(report.problems)
        return None if "route r1" in text and "fixtures/driver-exits/<group>.json" in text else f"got {report.problems}"

    @case("check: a row the driver does not have is a stale row naming its file")
    def _():
        directory = _tree(tmp(), _group(routes={"r1": _row(), UNMATCHED: _row(), "gone": _row()}, joints={"exit:j1": _row()},
                                        kinds_without_key={"k1": _row(raised_at=["m:f"])}))
        report = check(directory, universe=_universe())
        text = "\n".join(report.problems)
        return None if "route gone" in text and "stale row" in text and "g.json" in text else f"got {report.problems}"

    @case("check: a joint with no row is red")
    def _():
        directory = _tree(tmp())
        report = check(directory, universe=_universe(joints=["exit:j1", "exit:j2"]))
        return None if any("joint exit:j2" in p for p in report.problems) else f"got {report.problems}"

    @case("check: a keyless kind whose raised_at moved is red")
    def _():
        directory = _tree(tmp())
        report = check(directory, universe=_universe(kinds={"k1": {"raised_at": ["m:other"], "keyed_at": []}}))
        return None if any("raised_at" in p and "k1" in p for p in report.problems) else f"got {report.problems}"

    @case("check: a new keyless kind with no row is red")
    def _():
        directory = _tree(tmp())
        kinds = {"k1": {"raised_at": ["m:f"], "keyed_at": []}, "k2": {"raised_at": ["m:g"], "keyed_at": []}}
        report = check(directory, universe=_universe(kinds=kinds))
        return None if any("kind without a key k2" in p for p in report.problems) else f"got {report.problems}"

    # ---- the ratchet at and beyond its base (F2): each count has its own credit, one entry per extra row, naming its row, never stale
    stay = {"joints": {"exit:j1": _row()}, "kinds_without_key": {"k1": _row(raised_at=["m:f"])}}      # two rows, reach unwalked

    def ratchet_run(routes, **ratchet):
        group = _group(routes=routes, ratchet=_ratchet(**ratchet), **stay)
        return check(_tree(tmp(), group), universe=_universe())

    both_unwalked = {"r1": _row(), UNMATCHED: _row()}                  # with `stay`: 4 rows unwalked
    raise_r1 = "unwalked | routes/r1 | Lead, 2026-11-13"

    @case("ratchet: unwalked == base needs no raise and is green")
    def _():
        report = ratchet_run(both_unwalked, unwalked=4)
        return None if not report.problems else f"got {report.problems}"

    @case("ratchet: unwalked base+1 with its named raise is green and a NOTE")
    def _():
        report = ratchet_run(both_unwalked, unwalked=3, raised_by=[raise_r1])
        return None if not report.problems and any("raised 1" in n for n in report.notes) else f"{report.problems} {report.notes}"

    @case("ratchet: unwalked base+1 with no raise is red naming the count and the door")
    def _():
        report = ratchet_run(both_unwalked, unwalked=3)
        return None if any("ratchet unwalked" in p and "raised_by" in p for p in report.problems) else f"got {report.problems}"

    @case("ratchet: unwalked base+2 with ONE raise is red (one entry per extra row)")
    def _():
        report = ratchet_run(both_unwalked, unwalked=2, raised_by=[raise_r1])
        return None if any("ratchet unwalked" in p and "names 1 raise" in p for p in report.problems) else f"got {report.problems}"

    @case("ratchet: a raise entry while the count sits AT its base is a stale credit, red")
    def _():
        report = ratchet_run(both_unwalked, unwalked=4, raised_by=[raise_r1])
        return None if any("stale raise credit" in p for p in report.problems) else f"got {report.problems}"

    @case("ratchet: a raise entry for another count does not cover this count (cross-count credit)")
    def _():
        report = ratchet_run({"r1": _row("live_only"), UNMATCHED: _row()}, unwalked=3, raised_by=[raise_r1])
        text = " ".join(report.problems)
        return None if "ratchet live_only" in text and "ratchet unwalked" in text else f"got {report.problems}"

    @case("ratchet: a raise entry whose row is gone is stale, red naming the entry")
    def _():
        report = ratchet_run(both_unwalked, unwalked=3, raised_by=["unwalked | routes/gone | Lead, 2026-11-13"])
        return None if any("stale raise" in p and "routes/gone" in p for p in report.problems) else f"got {report.problems}"

    @case("ratchet: two entries for one row are refused")
    def _():
        report = ratchet_run(both_unwalked, unwalked=2, raised_by=[raise_r1, raise_r1 + " again"])
        return None if any("names a row twice" in p for p in report.problems) else f"got {report.problems}"

    @case("ratchet: a raise entry that does not fit the form is refused naming the file")
    def _():
        directory = _tree(tmp(), _group(routes=both_unwalked, ratchet=_ratchet(unwalked=4, raised_by=["Lead, 2026-11-13"]), **stay))
        try:
            load(directory)
        except ExitsUnreadable as exc:
            return None if "g.json" in str(exc) and "<count> | <row> | <who, where>" in str(exc) else f"got {exc}"
        return "no refusal"

    # ---- E1 both ways (F3): a row that claims it is run has a walk row behind it
    def walk_with(root: Path, rid: str, reach="seed") -> Path:
        _write(root / "exits" / "g.json", {"schema": 1, "group": "g", "rows": [{"id": rid, "reach": reach, "start": "S1",
                                                                              **({"why_unreached": "x"} if reach != "seed" else {})}]})
        return root / "exits"

    seed_r1 = _group(routes={"r1": _row("seed"), UNMATCHED: _row()}, ratchet=_ratchet(unwalked=3), **stay)

    @case("walk: a route row claiming seed with no walk row behind it is red, with the door")
    def _():
        report = check(_tree(tmp(), seed_r1), universe=_universe())
        return None if any("route r1" in p and "claims reach seed" in p and "unwalked" in p for p in report.problems) else f"got {report.problems}"

    @case("walk: the same seed row with a walk row naming it is green")
    def _():
        root = tmp()
        report = check(_tree(root, seed_r1), walk_with(root, "r1/a"), universe=_universe())
        return None if not report.problems else f"got {report.problems}"

    @case("walk: a walk row with reach unwalked or hook_layer is red (a count, not a walk row's reach)")
    def _():
        for reach in ("unwalked", "hook_layer"):
            root = tmp()
            report = check(_tree(root), walk_with(root, "r1/a", reach), universe=_universe())
            if not any("walk row r1/a" in p and f"reach {reach}" in p for p in report.problems):
                return f"{reach}: {report.problems}"
        return None

    @case("walk: a census row with reach hook_layer is red")
    def _():
        report = check(_tree(tmp(), _group(routes={"r1": _row("hook_layer"), UNMATCHED: _row()}, **stay)), universe=_universe())
        return None if any("route r1" in p and "hook_layer" in p for p in report.problems) else f"got {report.problems}"

    @case("load: a group file with no row and no count is refused naming the file")
    def _():
        directory = _tree(tmp())
        _write(directory / "h.json", _group("h"))
        try:
            load(directory)
        except ExitsUnreadable as exc:
            return None if "h.json" in str(exc) and "carries no row" in str(exc) else f"got {exc}"
        return "no refusal"

    # ---- F4: the routes match_known mints
    mint_source = ("def match_known(text):\n    if A in text:\n        return 'marked_repair', 'resume_repair'\n"
                   "    if B in text:\n        return 'marked_person', 'ask_person'\n    return None\n")

    @case("minted routes: the literal return tuples of match_known are read from its source")
    def _():
        got = minted_routes(mint_source)
        return None if got == {"marked_repair": "resume_repair", "marked_person": "ask_person"} else f"got {got}"

    @case("minted routes: a third marker branch is a route with no row, red until it has one")
    def _():
        third = mint_source.replace("    return None", "    if C in text:\n        return 'marked_third', 'continue'\n    return None")
        routes = {"r1": "continue", UNMATCHED: "conductor", **minted_routes(third)}
        report = check(_tree(tmp()), universe=_universe(routes=routes))
        return None if any("route marked_third" in p and "no row" in p for p in report.problems) else f"got {report.problems}"

    @case("minted routes: a rewritten match_known (no literal tuple) is refused, never zero routes")
    def _():
        for text in ("def match_known(text):\n    return find(text)\n", "def other():\n    return 'a', 'b'\n", "def match_known(:\n"):
            try:
                minted_routes(text)
            except ExitsUnreadable as exc:
                if "could not read the routes of match_known" not in str(exc):
                    return f"{text!r}: {exc}"
            else:
                return f"{text!r}: no refusal"
        return None

    @case("check: a base above the rows is a stale base")
    def _():
        group = _group(routes={"r1": _row(), UNMATCHED: _row()}, joints={"exit:j1": _row()}, kinds_without_key={"k1": _row(raised_at=["m:f"])},
                       ratchet=_ratchet(unwalked=5))
        report = check(_tree(tmp(), group), universe=_universe())
        return None if any("stale base" in p for p in report.problems) else f"got {report.problems}"

    @case("check: a walk row whose subject is no price key, route, joint or kind is red with the subject")
    def _():
        root = tmp()
        directory = _tree(root)
        walk = root / "exits"
        _write(walk / "g.json", {"schema": 1, "group": "g", "rows": [{"id": "no.such.key/a", "reach": "seed", "start": "S1"}]})
        report = check(directory, walk, universe=_universe())
        return None if any("'no.such.key'" in p for p in report.problems) else f"got {report.problems}"

    @case("check: classes.json missing is red naming the file")
    def _():
        directory = _tree(tmp())
        (directory / "classes.json").unlink()
        report = check(directory, universe=_universe())
        return None if any("classes.json" in p for p in report.problems) else f"got {report.problems}"

    @case("check: an unreadable carrier of the code (prices) is red, never a census over nothing")
    def _():
        report = check(_tree(tmp()), universe=_universe(errors=["question-prices.json: it is absent"]))
        return None if any("question-prices.json" in p for p in report.problems) else f"got {report.problems}"

    @case("check: a stale pin of the label ledger is red")
    def _():
        directory = _tree(tmp(), ledger={"known_red": {}, "pins": {"known_red": 4}})
        report = check(directory, universe=_universe())
        return None if any("stale pin" in p for p in report.problems) else f"got {report.problems}"

    # ---- the ledger through the helper
    @case("judge: a variant with a label and its neighbour red with none - the neighbour is red by id")
    def _():
        root = tmp()
        ledger = _write(root / "known_red.json", {"known_red": {"exit.resume_limit/go on": {"node": "FV1-13", "raised_by": "Lead, 2026-11-13"}},
                                                  "pins": {"known_red": 1}})
        ok, lines = judge({"exit.resume_limit/go on": False, "exit.resume_limit/round": False}, ledger)
        text = "\n".join(lines)
        return None if not ok and "new red: exit.resume_limit/round" in text and "known red: exit.resume_limit/go on" in text else f"got {ok} {lines}"

    # ---- item 7: classes
    registry = [{"id": "OP-1", "kind": "operation", "file": "controller.py", "override": "x"},
                {"id": "SG-1", "file": "stage_guard.py", "override": "", "unpassable_because": "door"},
                {"id": "SG-2", "file": "stage_guard.py", "override": "waiver", "unpassable_because": ""}]
    classes = {"schema": 1, "by_source": {"stage-joints": "gate", "refusal_registry:operation": "gate", "refusal_registry:scanned": "ban",
                                         "question:gate_A": "gate"}, "default": None}

    def klass(row, section="routes", action="ask_person", classes=classes):
        return class_of(row, classes, section=section, action=action, joints=["exit:j1"], registry=registry)

    @case("class: a joint is the class of source stage-joints")
    def _():
        return None if klass({}, "joints", "") == "gate" else f"got {klass({}, 'joints', '')}"

    @case("class: an ask_person route naming a registry operation takes the operation class")
    def _():
        return None if klass({"class_source": "OP-1"}) == "gate" else f"got {klass({'class_source': 'OP-1'})}"

    @case("class: an ask_person route naming a scanned hook record is a ban")
    def _():
        return None if klass({"class_source": "SG-1"}) == "ban" else f"got {klass({'class_source': 'SG-1'})}"

    @case("class: an ask_person route naming a joint check and a question id")
    def _():
        got = (klass({"class_source": "exit:j1"}), klass({"class_source": "question:gate_A"}))
        return None if got == ("gate", "gate") else f"got {got}"

    @case("class: an ask_person route with no class_source is class unknown (E19)")
    def _():
        got = (klass({}), klass({"class_source": ""}), klass({"class_source": None}))
        return None if got == (CLASS_UNKNOWN,) * 3 else f"got {got}"

    @case("class: a class_source found nowhere is class unknown, not a guess")
    def _():
        return None if klass({"class_source": "NO-SUCH"}) == CLASS_UNKNOWN else f"got {klass({'class_source': 'NO-SUCH'})}"

    @case("class: a source with no entry in by_source and no default is class unknown; a default is used when present")
    def _():
        bare = {"schema": 1, "by_source": {}, "default": None}
        filled = {"schema": 1, "by_source": {}, "default": "gate"}
        got = (klass({"class_source": "OP-1"}, classes=bare), klass({"class_source": "OP-1"}, classes=filled))
        return None if got == (CLASS_UNKNOWN, "gate") else f"got {got}"

    @case("class: a code-move route and a question kind are no refusal text (n/a)")
    def _():
        got = (klass({}, "routes", "continue"), klass({}, "kinds_without_key", ""))
        return None if got == (NOT_A_REFUSAL, NOT_A_REFUSAL) else f"got {got}"

    unpassable = frozenset({"SG-1"})                 # what `refusal_registry.unpassable()` returns for `registry`: the one reader of the fact
    prices_q = {"gate_A": [], "gate_B": [], "other": []}

    @case("class: the counts split bans (word does not pass / passes), operations and joints; questions are counted in prices only")
    def _():
        got = class_counts(_universe(registry=registry, joints=["exit:j1", "exit:j2"], unpassable=unpassable, prices=prices_q),
                           {"by_source": {"question:gate_A": "gate", "question:gate_B": "gate", "question:gone": "gate", "stage-joints": "gate"}})
        want = {"ban_unpassable": 1, "ban_passable": 1, "gate_operations": 1, "gate_operations_unpassable": 0, "gate_joints": 2, "gate_questions": 2}
        return None if got == want else f"got {got}"

    def unknown_check(routes, universe_routes, classes_data=None):
        group = _group(routes=routes, joints={"exit:j1": _row()}, kinds_without_key={"k1": _row(raised_at=["m:f"])}, ratchet=_ratchet(unwalked=4))
        return check(_tree(tmp(), group, classes_data), universe=_universe(routes=universe_routes))

    @case("class: an ask_person route with no class_source is RED in check, never a NOTE (E19)")
    def _():
        report = unknown_check({"r1": _row(), UNMATCHED: _row()}, {"r1": "ask_person", UNMATCHED: "conductor"})
        return None if any("route r1: class unknown" in p for p in report.problems) else f"got {report.problems} {report.notes}"

    @case("class: an ask_person route naming a by_source key directly takes its class; a key nobody holds is red")
    def _():
        classes_data = {"schema": 1, "by_source": {"stage-joints": "gate", "route:direct": "gate"}, "default": None}
        named = unknown_check({"r1": _row(class_source="route:direct"), UNMATCHED: _row()}, {"r1": "ask_person", UNMATCHED: "conductor"}, classes_data)
        absent = unknown_check({"r1": _row(class_source="route:nobody"), UNMATCHED: _row()}, {"r1": "ask_person", UNMATCHED: "conductor"}, classes_data)
        if named.problems:
            return f"named: {named.problems}"
        return None if any("route r1: class unknown" in p for p in absent.problems) else f"absent: {absent.problems}"

    @case("class: a joint whose stage-joints source has no class and no default is red in check")
    def _():
        classes_data = {"schema": 1, "by_source": {}, "default": None}
        report = unknown_check({"r1": _row(), UNMATCHED: _row()}, {"r1": "continue", UNMATCHED: "conductor"}, classes_data)
        return None if any("joint exit:j1: class unknown" in p for p in report.problems) else f"got {report.problems}"

    # ---- item 8: ban doors (the word-does-not-pass fact is read through `refusal_registry.unpassable()`; this reads the door of the ids it names)
    def doors(records, stuck, scanned=("stage_guard.py",)):
        return ban_doors(_universe(registry=records, scanned=scanned, unpassable=frozenset(stuck)))

    @case("ban_doors: an unpassable record with no door is red with the id")
    def _():
        got = doors([{"id": "X", "file": "stage_guard.py", "unpassable_because": ""}], {"X"})
        return None if got == ["X"] else f"got {got}"

    @case("ban_doors: a blank door counts as no door; a record missing the field counts as no door")
    def _():
        got = doors([{"id": "X", "file": "stage_guard.py", "unpassable_because": "   "}, {"id": "Y", "file": "stage_guard.py"}], {"X", "Y"})
        return None if got == ["X", "Y"] else f"got {got}"

    @case("ban_doors: a named door, a passable word, an operation and an unscanned file are not red")
    def _():
        rows = [{"id": "A", "file": "stage_guard.py", "unpassable_because": "door"},
                {"id": "B", "file": "stage_guard.py", "unpassable_because": ""},
                {"id": "C", "kind": "operation", "file": "stage_guard.py"},
                {"id": "D", "file": "other.py", "unpassable_because": ""}]
        got = doors(rows, {"A", "C", "D"})              # B is passable: not in the unpassable ids
        return None if got == [] else f"got {got}"

    # ---- item 9: the fingerprint and the same ask
    def world(root: Path, rounds=1, form="a: 1\n", status="running", asked_at="t1", controller=True) -> Path:
        _write(root / "pipeline.json", {"stages": {"S5": {"status": status, "started": asked_at}}, "gates": {"A": {"decision": "none", "at": asked_at}}})
        if controller:
            records = {f"S5-qa-automator-{n}": {"id": f"S5-qa-automator-{n}", "stage": "S5", "role": "qa-automator", "status": "accepted",
                                                "dispatched_seq": n} for n in range(1, rounds + 1)}
            _write(root / "state" / "controller.json", {"dispatches": records})
        for n in range(1, rounds + 1):
            _write(root / "work" / "handoffs" / f"S5-qa-automator-{n}.yaml", form.replace("<id>", f"S5-qa-automator-{n}"))
        return root

    stages = {"stages": [{"id": "S5", "outputs": ["work/out.json", "work/dir/"]}]}

    def finger(root, **kw):
        return state_fingerprint(root, stages=stages, **kw)

    @case("fingerprint: only times differ -> the same state")
    def _():
        a, b = finger(world(tmp(), asked_at="t1")), finger(world(tmp(), asked_at="t2"))
        return None if a == b else "digests differ for a clock only"

    @case("fingerprint: a new round with the same form bytes is another state (C3)")
    def _():
        a, b = finger(world(tmp(), rounds=1)), finger(world(tmp(), rounds=2))
        return None if a != b else "a legitimate new round read as the same state"

    @case("fingerprint: a form that differs only by its dispatch id is the same form for the same key")
    def _():
        one, two = tmp(), tmp()
        world(one, form="id: <id>\n")
        world(two, form="id: <id>\n")
        _write(two / "work" / "handoffs" / "S5-qa-automator-1.yaml", "id: S5-qa-automator-9\n")
        return None if finger(one) == finger(two) else "a dispatch id inside the form changed the digest"

    @case("fingerprint: a changed form for the same round is another state")
    def _():
        a, b = finger(world(tmp(), form="a: 1\n")), finger(world(tmp(), form="a: 2\n"))
        return None if a != b else "a changed form read as the same state"

    @case("fingerprint: a stage status change is another state")
    def _():
        a, b = finger(world(tmp(), status="running")), finger(world(tmp(), status="done"))
        return None if a != b else "a stage status change read as the same state"

    @case("fingerprint: no state/controller.json -> notes say rounds unknown (E7), never a quiet pass")
    def _():
        got = finger(world(tmp(), controller=False))
        return None if any("rounds unknown" in n for n in got.notes) else f"notes {got.notes}"

    @case("fingerprint: a corrupt state/controller.json is red naming the file")
    def _():
        root = world(tmp())
        _write(root / "state" / "controller.json", "{broken")
        try:
            finger(root)
        except StateUnreadable as exc:
            return None if "controller.json" in str(exc) else f"got {exc}"
        return "no refusal"

    @case("fingerprint: a stage output that appears changes the state; a directory output counts its files")
    def _():
        root = world(tmp())
        before = finger(root)
        _write(root / "work" / "dir" / "a.txt", "x")
        mid = finger(root)
        _write(root / "work" / "out.json", "{}")
        return None if len({before.digest, mid.digest, finger(root).digest}) == 3 else "output presence not in the state"

    ask = {"key": "exit.resume_limit", "stage": "S5", "dispatch": "S5-qa-automator-4", "tokens": ["go on", "stop"], "asked_at": "t1", "text": "Q"}

    @case("same_ask: dispatch ids that differ only by number are one ask")
    def _():
        return None if same_ask(ask, {**ask, "dispatch": "S5-qa-automator-5"}) else "split by a dispatch number"

    @case("same_ask: the asked_at stamp and the text are not compared")
    def _():
        return None if same_ask(ask, {**ask, "asked_at": "t2", "text": "Q\n\n---\n**You have answered this exact question before**"}) else "split by text"

    @case("same_ask: the same token in another case, in backticks, or with a full stop is the same set")
    def _():
        other = {**ask, "tokens": ["`Go on`.", " STOP "]}
        return None if same_ask(ask, other) else "split by token spelling"

    @case("same_ask: a different stage, key or token set is another ask")
    def _():
        different = [{**ask, "stage": "S6"}, {**ask, "key": "s5.repair_limit"}, {**ask, "tokens": ["go on"]}, {**ask, "dispatch": "S6-qa-runner-4"}]
        return None if not any(same_ask(ask, other) for other in different) else "different asks merged"

    @case("same_ask: a kind and a key never merge, offered works like tokens")
    def _():
        kind = {"kind": "exit_limit", "stage": "S5", "dispatch": ask["dispatch"], "offered": ["go on", "stop"]}
        return None if not same_ask(ask, kind) and same_ask(kind, {**kind, "offered": ["Stop", "go on"]}) else "bad identity"

    @case("author input: a prompt that differs only by the id of its dispatch is the same input; a new sentence is not")
    def _():
        a = "Dispatch: S5-qa-automator-4\nFix it."
        return None if author_input_sha(a) == author_input_sha("Dispatch: S5-qa-automator-5\nFix  it.") \
            and author_input_sha(a) != author_input_sha(a + " New finding.") else "bad input identity"

    # ---- item 10: driven keys
    prices = {"k1": [{"answer": "a"}, {"answer": "b"}], "k2": [{"answer": "x"}]}

    def driven(rows):
        root = tmp()
        _write(root / "g.json", {"schema": 1, "group": "g", "rows": rows})
        return driven_keys(root, prices)

    def walk_row(rid, reach):
        return {"id": rid, "reach": reach, "start": "S1", "why_unreached": "x" if reach != "seed" else None}

    @case("driven: every answer row of a key run -> the key is driven")
    def _():
        got = driven([walk_row("k1/a", "seed"), walk_row("k1/b", "story"), walk_row("k2/x", "seed")])
        return None if got == {"k1", "k2"} else f"got {got}"

    @case("driven: a key with one live_only answer row is not driven (E20)")
    def _():
        got = driven([walk_row("k1/a", "seed"), walk_row("k1/b", "live_only"), walk_row("k2/x", "seed")])
        return None if got == {"k2"} else f"got {got}"

    @case("driven: a key with an after:<finding> answer row or a missing answer row is not driven")
    def _():
        got = driven([walk_row("k1/a", "seed"), walk_row("k1/b", "after:FV1-1")])
        return None if got == set() else f"got {got}"

    @case("driven: free-words and empty variants do not count toward a key, nor do they stop it")
    def _():
        got = driven([walk_row("k2/x", "seed"), walk_row("k2/free words", "live_only")])
        return None if got == {"k2"} else f"got {got}"

    @case("driven: no walk directory yet means no key is driven (temporal), unreadable rows are an error")
    def _():
        if driven_keys(tmp() / "absent", prices) != set():
            return "absent directory drove keys"
        root = tmp()
        _write(root / "g.json", "{bad")
        try:
            driven_keys(root, prices)
        except ExitsUnreadable:
            return None
        return "unreadable rows read as an empty set"

    @case("driven: the same walk row id in two files is refused naming both")
    def _():
        root = tmp()
        for name in ("g.json", "h.json"):
            _write(root / name, {"schema": 1, "group": name, "rows": [walk_row("k2/x", "seed")]})
        try:
            driven_keys(root, prices)
        except ExitsUnreadable as exc:
            return None if "g.json" in str(exc) and "h.json" in str(exc) else f"got {exc}"
        return "no refusal"

    return cases


def selftest() -> int:
    failed, cases = 0, _selftest_cases()
    for name, fn in cases:
        try:
            why = fn()
        except Exception as exc:  # a case that crashes is a failed case naming itself
            why = f"crashed: {exc.__class__.__name__}: {exc}"
        failed += bool(why)
        print(f"{'FAIL' if why else 'PASS'} {name}" + (f": {why}" if why else ""))
    print(f"dry_exits selftest: {len(cases) - failed}/{len(cases)} cases")
    return 1 if failed else 0


# ---------------------------------------------------------------------------------------------------- the CLI
def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="The census of the driver's exits (P1-b N1).")
    parser.add_argument("--check", action="store_true", help="the census; exit 0 with 0 discrepancies")
    parser.add_argument("--selftest", action="store_true", help="the table of cases of this file")
    parser.add_argument("--judge", metavar="RESULTS.json", help="judge {row id: bool} against known_red.json of --dir")
    parser.add_argument("--dir", help="the driver-exits directory (default: the fixture directory)")
    parser.add_argument("--exits-dir", help="the walk rows directory (default: fixtures/stories/dry-1/exits)")
    args = parser.parse_args(argv)
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")       # the helper's door text carries a dash
    if args.selftest:
        return selftest()
    if args.judge:
        try:
            results = _read_json(Path(args.judge), "an object of row id -> true/false")
            ledger = Path(args.dir or EXITS_DIR) / "known_red.json"
            ok, lines = judge(results, ledger)
        except ExitsUnreadable as exc:
            print(f"FAIL {exc}")
            return 1
        for line in lines:
            print(line)
        print("judge: " + ("ok" if ok else f"REJECT - {sum(1 for ln in lines if not ln.startswith('known red'))} problem(s)"))
        return 0 if ok else 1
    if args.check:
        report = check(args.dir, args.exits_dir)
        for line in report.numbers:
            print(f"NUMBER {line}")
        for line in report.notes:
            print(f"NOTE {line}")
        for line in report.problems:
            print(f"FAIL {line}")
        print(f"dry_exits --check: {len(report.problems)} discrepancies")
        return 1 if report.problems else 0
    parser.print_usage()
    return 2


if __name__ == "__main__":
    sys.exit(main())
