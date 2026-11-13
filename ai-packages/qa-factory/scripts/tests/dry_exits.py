"""The census of the driver's exits (P1-b spec sections 3.1-3.6, node N1): which routes, joints and question kinds the driver has, and
whether each has a row; the class of each refusal; the state fingerprint and the "same ask" test the dry walk judges with.

A helper next to the tests, not a test (like `scenario_walk.py`). It decides nothing about meaning (P27, AR-29): it reads data -
the driver's own tables by import (`driver_dispatch.KNOWN_REFUSALS`, `no_move.load_question_prices`, the stage-joints file through the
reader its walker uses, `refusal_registry.REGISTRY`, the driver sources through `harness.driver_sources`) - and compares them with the
rows of `fixtures/driver-exits/<group>.json`, in both directions. A route, joint or keyless question kind with no row is red; so is a
row with nothing behind it. The keys of the closed questions are NOT censused here (`test_conductor_doors.py` already does that; the
walk rows join its `driven` set through `driven_keys`).

    python -B scripts/tests/dry_exits.py --check [--dir D] [--exits-dir E]   the census: 0 discrepancies or the list, and the numbers
    python -B scripts/tests/dry_exits.py --judge RESULTS.json [--dir D]      judge `{row id: bool}` against the ledger `D/known_red.json`
    python -B scripts/tests/dry_exits.py --selftest                          the table of cases of this file

The label ledger is the ONE helper `known_red.py` (its reconcile, its raise door); this file only names the ledger file. Unknown never
becomes a pass (AR-28): an unreadable or missing data file is red naming the file, never an empty census; a row with no class source
is `class unknown`, printed and counted, never a guessed class.
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
KEYED = ("closed_question", "priced_section")
PERSON_CALLS = ("Person", "site_seam_person")
UNMATCHED, KNOWN_FALSE = "unmatched", "known_false"
CLASS_UNKNOWN, NOT_A_REFUSAL = "class unknown", "n/a"
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
    if not isinstance(raised, list) or not all(isinstance(item, str) and item.strip() for item in raised):
        out.append(f"{where}: ratchet.raised_by is {raised!r}; expected a list of non-empty strings, each naming who allowed one raised row")
    return out


def load(directory=None) -> dict:
    """The census files glued: `{"routes": {name: row}, "joints": {...}, "kinds_without_key": {...}, "where": {(section, name): path},
    "ratchet": {count name: [base sum]}, "raised_by": [...], "classes": {...}, "files": [...]}`. Every `*.json` of the directory except
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


class _PersonSites(ast.NodeVisitor):
    def __init__(self, module: str):
        self.module, self.stack, self.sites = module, [], []

    def _function(self, node):
        self.stack.append(node.name)
        self.generic_visit(node)
        self.stack.pop()

    visit_FunctionDef = visit_AsyncFunctionDef = _function

    def visit_Call(self, node: ast.Call):
        if _callee(node) in PERSON_CALLS and node.args:
            first = node.args[0]
            kind = first.value if isinstance(first, ast.Constant) and isinstance(first.value, str) else None
            rest = [*node.args[1:], *[kw.value for kw in node.keywords]]
            keyed = any(isinstance(inner, ast.Call) and _callee(inner) in KEYED for arg in rest for inner in ast.walk(arg))
            self.sites.append((kind, f"{self.module}:{self.stack[-1] if self.stack else '<module>'}", keyed))
        self.generic_visit(node)


def person_sites(sources=None) -> list:
    """`[(kind or None, "<module>:<function>", keyed)]` for every `Person(...)` / `site_seam_person(...)` call of the driver sources
    (`harness.driver_sources()`: the ONE reader of that set, AR-13). `kind` is the literal first argument, None when it arrives as a value
    (a name, an f-string, an expression). `keyed` is True when `closed_question(...)` / `priced_section(...)` is called INSIDE the call's own
    arguments - the spec's rule "the same call" (3.2). A source that does not parse is an `ExitsUnreadable`, never skipped."""
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


def scan_routes() -> dict:
    """`{name: action}`: the 21 rows of `driver_dispatch.KNOWN_REFUSALS` BY IMPORT, plus the two classes that are no row of it:
    `unmatched` (a text no row matches goes to the conductor: `driver_machine.match_known` returns None) and `known_false` (a refusal a G
    step raises, `driver_core.gate_refusal`, is never routed by the table). Both are checked by calling the function; a function that stopped
    behaving so is an `ExitsUnreadable`, not a row that silently stays."""
    import driver_core
    import driver_dispatch
    import driver_machine
    routes = {name: action for name, _pattern, action in driver_dispatch.KNOWN_REFUSALS}
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
                   kinds_total=len({kind for kind, _at, _keyed in sites if kind}))


# ---------------------------------------------------------------------------------------------------- classes, doors
def registry_kinds(registry) -> dict:
    return {str(r.get("id")): ("operation" if r.get("kind") == "operation" else "scanned") for r in registry if isinstance(r, dict)}


def class_of(row, classes: dict, *, section: str, action: str = "", joints=(), registry=()) -> str:
    """The class of a census row by its SOURCE (spec 3.6; the rule is data in `classes.json`, not a list here). A joint: source `stage-joints`.
    A route whose move is `ask_person`: the source its `class_source` names - a joint check, a REGISTRY id (operation or scanned), or a
    `question:<key>` id. A route with a code move and a kind of question are no refusal text a person reads: `n/a`. A source that is not named,
    not found, or not in `by_source` with no default: `class unknown` - printed and counted, never a guess (FR-59)."""
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
        elif named.startswith("question:"):
            source = named
    klass = classes.get("by_source", {}).get(source) if source else None
    return klass or classes.get("default") or CLASS_UNKNOWN


def ban_doors(registry=None, scanned=None) -> list:
    """The ids of the hook-layer registry records (file in `SCANNED`) whose word does not pass (`override: ""`) and whose door is not named
    (`unpassable_because` empty or blank): FR-57, a ban is never a dead end. Only the DATA of the registry is read; the hooks are not run (F11).
    A record whose `override` is missing or not text counts as not passable (the red direction)."""
    if registry is None or scanned is None:
        import refusal_registry
        registry = refusal_registry.REGISTRY if registry is None else registry
        scanned = refusal_registry.SCANNED if scanned is None else scanned
    out = []
    for record in registry:
        if record.get("file") not in scanned or record.get("kind") == "operation":
            continue
        override = record.get("override")
        if isinstance(override, str) and override.strip():
            continue
        door = record.get("unpassable_because")
        if not isinstance(door, str) or not door.strip():
            out.append(str(record.get("id")))
    return out


def class_counts(universe: Universe) -> dict:
    """The numbers of spec 3.6, recounted from the registry and the joints: hook bans the word does not pass / pass, operations, joints."""
    scanned = [r for r in universe.registry if r.get("file") in universe.scanned and r.get("kind") != "operation"]
    operations = [r for r in universe.registry if r.get("kind") == "operation"]
    blank = lambda r: not (isinstance(r.get("override"), str) and r["override"].strip())     # noqa: E731
    return {"ban_unpassable": sum(1 for r in scanned if blank(r)), "ban_passable": sum(1 for r in scanned if not blank(r)),
            "gate_operations": len(operations), "gate_operations_unpassable": sum(1 for r in operations if blank(r)),
            "gate_joints": len(universe.joints), "gate_questions": 2}


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
    # 1. code <-> rows, both directions
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
    # 2. walk rows: the subject of every row exists
    subjects = set(universe.prices) | set(census["routes"]) | set(census["joints"]) | set(census["kinds_without_key"])
    for rid, row in sorted(walk.items()):
        subject = rid.split("/", 1)[0]
        if subject not in subjects:
            red(f"walk row {rid} ({row['_path']}): {subject!r} is not a key of question-prices.json, a route, a joint or a kind without a key; "
                f"fix the id, or add the key/route to its table")
        if str(row.get("reach")) == "hook_layer":
            red(f"walk row {rid}: reach hook_layer is a count, not a row (the hook refusals are not walked one by one); remove the row")
    # 3. ratchets: the sum over the group files against their bases; a raise is named per row
    counts = _count_reach(census, walk)
    counts["hook_layer"] = sum(1 for r in universe.registry if r.get("file") in universe.scanned and r.get("kind") != "operation")
    for name in RATCHET_COUNTS:
        base, count, named = census["base"][name], counts[name], len(census["raised_by"])
        if count > base + named:
            red(f"ratchet {name}: {count} rows, above the base {base}, and ratchet.raised_by names {named} raise(s); a raise needs one named "
                f"entry per row (who allowed it) and the base lowered back by fixing the rows - the number only shrinks")
        elif count > base:
            report.notes.append(f"ratchet {name}: raised {count - base} row(s) above the base {base}, named in raised_by: {census['raised_by']}")
        elif count < base:
            red(f"ratchet {name}: stale base: {count} rows, below the base {base}; lower the base to {count} in the group files")
    # 4. classes and doors of the bans
    unknown = []
    for section in ("routes", "joints"):
        for name, row in sorted(census[section].items()):
            klass = class_of(row, census["classes"], section=section, action=universe.routes.get(name, ""),
                             joints=universe.joints, registry=universe.registry)
            if klass == CLASS_UNKNOWN:
                unknown.append(f"{section[:-1]} {name}")
    if unknown:
        report.notes.append(f"class unknown: {len(unknown)} ({', '.join(unknown)}); name a class_source for each, or the source in classes.json")
    for rid in ban_doors(universe.registry, universe.scanned):
        red(f"hook refusal {rid}: its word does not pass (override '') and unpassable_because names no door (FR-57); name the door in refusal_registry.py")
    # 5. the label ledger of the helper
    ledger = Path(ledger_path or directory / "known_red.json")
    try:
        import known_red
        rows = known_red.load(ledger)
        stale = known_red.pin_problem(ledger, "known_red", len(rows))
        if stale:
            red(stale)
    except Exception as exc:  # LedgerError names the file and the row
        red(f"{ledger}: {exc}")
    # the numbers
    kept = sorted(set(universe.routes) - {UNMATCHED, KNOWN_FALSE})
    options = sum(len(rows) for rows in universe.prices.values())
    by = {}
    for check_id in universe.joints:
        by[check_id.split(":", 1)[0]] = by.get(check_id.split(":", 1)[0], 0) + 1
    numbers = class_counts(universe)
    report.numbers = [
        f"routes: {len(kept)} KNOWN_REFUSALS + 2 (unmatched, known_false) = {len(universe.routes)}   "
        f"[recount: python -B -c \"import driver_dispatch as D; print(len(D.KNOWN_REFUSALS))\" in scripts/]",
        f"price keys: {len(universe.prices)}, options: {options}   "
        f"[recount: python -B -c \"import no_move as N; p=N.load_question_prices(); print(len(p), sum(map(len, p.values())))\" in scripts/]",
        f"joints: {len(universe.joints)} ({', '.join(f'{k} {v}' for k, v in sorted(by.items()))})   "
        f"[recount: python -B -c \"import null_outcomes as O, stage_joints as J; print(len(O.load_data(J.DATA)[0]['joints']))\" in scripts/]",
        f"kinds without a key: {len(universe.kinds)} of {universe.kinds_total} literal kinds; sites with a kind that arrives as a value: "
        f"{len(universe.variable)} ({', '.join(universe.variable) or 'none'})   [recount: this file, --check]",
        f"classes: ban word-does-not-pass {numbers['ban_unpassable']} / ban word-passes {numbers['ban_passable']} / gate operations "
        f"{numbers['gate_operations']} (of them override '': {numbers['gate_operations_unpassable']}) / gate joints {numbers['gate_joints']} / "
        f"gate questions {numbers['gate_questions']}   [recount: python -B -c \"import refusal_registry as R; "
        f"print(len(R.REGISTRY), sum(1 for r in R.REGISTRY if r.get('kind')=='operation'))\" in scripts/]",
        f"ban_doors without a named door: {len(ban_doors(universe.registry, universe.scanned))}",
        "ratchet (rows now / base): " + ", ".join(f"{n} {counts[n]}/{census['base'][n]}" for n in RATCHET_COUNTS)
        + f"; raised_by {len(census['raised_by'])}",
        f"groups: {', '.join(census['groups'])}"]
    return report


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


def _row(reach="seed", **kw) -> dict:
    return {"reach": reach, "seed": None, "why_unreached": kw.pop("why", None), **kw}


def _universe(**kw) -> Universe:
    base = dict(routes={"r1": "continue", UNMATCHED: "conductor"}, joints=["exit:j1"], kinds={"k1": {"raised_at": ["m:f"], "keyed_at": []}},
                variable=[], prices={"p.key": [{"answer": "a"}, {"answer": "b"}]}, registry=[], scanned=("stage_guard.py",))
    base.update(kw)
    return Universe(**base)


def _tree(root: Path, group=None, classes=None, ledger=None) -> Path:
    directory = root / "driver-exits"
    _write(directory / "g.json", group or _group(routes={"r1": _row(), UNMATCHED: _row()}, joints={"exit:j1": _row()},
                                                 kinds_without_key={"k1": _row(raised_at=["m:f"])}))
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
            _write(directory / "g.json", _group(routes={"r1": _row(reach)}))
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

    @case("check: unwalked rows above the base with no raised_by are red; the base lowered is the same fault")
    def _():
        group = _group(routes={"r1": _row("unwalked", why="x"), UNMATCHED: _row()}, joints={"exit:j1": _row()},
                       kinds_without_key={"k1": _row(raised_at=["m:f"])})
        report = check(_tree(tmp(), group), universe=_universe())
        return None if any("ratchet unwalked" in p and "raised_by" in p for p in report.problems) else f"got {report.problems}"

    @case("check: a raise named in raised_by is a NOTE, one name per row")
    def _():
        group = _group(routes={"r1": _row("unwalked", why="x"), UNMATCHED: _row("unwalked", why="x")}, joints={"exit:j1": _row()},
                       kinds_without_key={"k1": _row(raised_at=["m:f"])}, ratchet=_ratchet(unwalked=1, raised_by=["Lead, 2026-11-13"]))
        report = check(_tree(tmp(), group), universe=_universe())
        two = _group(routes={"r1": _row("unwalked", why="x"), UNMATCHED: _row("unwalked", why="x")}, joints={"exit:j1": _row()},
                     kinds_without_key={"k1": _row(raised_at=["m:f"])}, ratchet=_ratchet(raised_by=["Lead, 2026-11-13"]))
        refused = check(_tree(tmp(), two), universe=_universe())
        if report.problems or not any("raised 1" in n for n in report.notes):
            return f"named raise: {report.problems} {report.notes}"
        return None if any("ratchet unwalked" in p for p in refused.problems) else f"two rows, one name: {refused.problems}"

    @case("check: a base above the rows is a stale base")
    def _():
        group = _group(routes={"r1": _row(), UNMATCHED: _row()}, joints={"exit:j1": _row()}, kinds_without_key={"k1": _row(raised_at=["m:f"])},
                       ratchet=_ratchet(unwalked=3))
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

    @case("class: the counts split bans (word does not pass / passes), operations and joints")
    def _():
        got = class_counts(_universe(registry=registry, joints=["exit:j1", "exit:j2"]))
        want = {"ban_unpassable": 1, "ban_passable": 1, "gate_operations": 1, "gate_operations_unpassable": 0, "gate_joints": 2, "gate_questions": 2}
        return None if got == want else f"got {got}"

    @case("class: an ask_person route with no class_source is counted and printed by check, not hidden")
    def _():
        group = _group(routes={"r1": _row(), UNMATCHED: _row()}, joints={"exit:j1": _row()}, kinds_without_key={"k1": _row(raised_at=["m:f"])})
        report = check(_tree(tmp(), group), universe=_universe(routes={"r1": "ask_person", UNMATCHED: "conductor"}))
        return None if any("class unknown: 1" in n and "route r1" in n for n in report.notes) else f"got {report.notes}"

    # ---- item 8: ban doors
    @case("ban_doors: override '' with no door is red with the id")
    def _():
        got = ban_doors([{"id": "X", "file": "stage_guard.py", "override": "", "unpassable_because": ""}], ("stage_guard.py",))
        return None if got == ["X"] else f"got {got}"

    @case("ban_doors: a blank door counts as no door")
    def _():
        got = ban_doors([{"id": "X", "file": "stage_guard.py", "override": "", "unpassable_because": "   "}], ("stage_guard.py",))
        return None if got == ["X"] else f"got {got}"

    @case("ban_doors: a named door, a passable word, an operation and an unscanned file are not red")
    def _():
        rows = [{"id": "A", "file": "stage_guard.py", "override": "", "unpassable_because": "door"},
                {"id": "B", "file": "stage_guard.py", "override": "waiver", "unpassable_because": ""},
                {"id": "C", "kind": "operation", "file": "stage_guard.py", "override": ""},
                {"id": "D", "file": "other.py", "override": "", "unpassable_because": ""}]
        got = ban_doors(rows, ("stage_guard.py",))
        return None if got == [] else f"got {got}"

    @case("ban_doors: a record with no override field counts as not passable (the red direction)")
    def _():
        got = ban_doors([{"id": "X", "file": "stage_guard.py"}], ("stage_guard.py",))
        return None if got == ["X"] else f"got {got}"

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
