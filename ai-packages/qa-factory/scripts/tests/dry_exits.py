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
# The grammar of a walk row (node N4w; spec docs/tasks/specs/20261114-p1b-n4w-exit-walker-spec.md section 8). Closed vocabularies are data
# tuples HERE and nowhere else (AR-1 inside the test layer): the loader, the judge and the self-test read these names.
WALK_FILE_KEYS = ("schema", "group", "rows")
WALK_ROW_KEYS = ("id", "start", "seed", "answer", "stub", "expect", "reach", "why_unreached")
ANSWER_KEYS = ("token", "words", "words_file")
EXPECT_KEYS = ("checks", "owner_quote", "owner_question")
OWNER_QUOTE_KEYS = ("text", "carrier")
SEED_FILE_KEYS = ("schema", "group", "recipes")
SEED_STEP_KEYS = ("drive_until", "op")
DRIVE_UNTIL_KEYS = ("stage", "question")
CHECKS_JUDGED = ("C2", "C3", "C4", "C5", "C6", "C9", "empty")          # implemented by `judge_row`
CHECKS_PENDING = ("C7", "C8", "C10")                                   # listed, not judged here: the row is a NOTE `pending judge` (F-W13)
CHECK_IDS = CHECKS_JUDGED + CHECKS_PENDING
STARTS = ("fresh",) + tuple(f"S{n}" for n in range(10))
NAMESPACES = {"route": "routes", "joint": "joints", "kind": "kinds_without_key"}      # a bare subject is a price key (F-W2 (a))
V_FREE, V_EMPTY, V_CODE = "free words", "empty", "code move"
JOINT_VARIANTS = ("repair", "no repair", "word")                        # F-W3 (a)
WHY_VALUES = ("refusal", "threshold", "cap", "unread_answer", "stage_review_exhausted", "by_hand", "stop", "chosen")    # the seam's closed `why` (P1-b section 3)
OP_SCRIPTS = ("story_step.py", "stage_done.py", "waiver.py", "controller.py")     # the closed list of a seed `op` (P1-b 4.3)
CASE_VARIANT_RE = re.compile(r"^words:[A-Za-z0-9_.-]+$")                # the E9 battery rows
WHY_VARIANT_RE = re.compile(r"^([a-z_]+):(\S.*)$")                      # `<why>:<token>` (F-W15 (a))
QUESTION_RE = re.compile(r"^Q[0-9]+$")
CARRIER_RE = re.compile(r"^(.+):([0-9]+)$")
GATE_CLASSES = ("gate",)
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


def load_group_file(path, *, strict: bool = False, universe=None, seeds=None, class_of_subject=None, story_dir=None) -> list:
    """The rows of ONE walk file (`{"schema": 1, "group": g, "rows": [...]}`), the one reader both the census (`strict=False`) and the walker
    (`strict=True`) go through. Refused in both modes: an unreadable file, a `rows` list that is absent or EMPTY (an empty group says nothing,
    EW2), a row with no id or with a field of the census row grammar that is wrong, an unknown top-level field of a row (EW4). `strict` adds
    the grammar of `walk_row_problems` and the file's own keys; every refusal comes BEFORE any world is built (E-R3)."""
    path = Path(path)
    data = _read_json(path, "an object with schema, group and rows")
    body = data.get("rows") if isinstance(data, dict) else None
    if not isinstance(body, list):
        raise ExitsUnreadable(f"{path}: expected an object with a rows list")
    if not body:
        raise ExitsUnreadable(f"{path}: `rows` is empty; an empty group says nothing - expected the walk rows of the group (or delete the file)")
    problems: list = []
    if strict:
        problems += [f"{path}: unknown top-level key {key!r}; expected only {list(WALK_FILE_KEYS)}" for key in sorted(set(data) - set(WALK_FILE_KEYS))]
        if data.get("schema") != 1:
            problems.append(f"{path}: schema is {data.get('schema')!r}; expected 1")
        if data.get("group") != path.stem:
            problems.append(f"{path}: group is {data.get('group')!r}; expected the file stem {path.stem!r}")
    rows: list = []
    for index, row in enumerate(body):
        rid = row.get("id") if isinstance(row, dict) else None
        if not isinstance(rid, str) or "/" not in rid or not rid.split("/", 1)[0] or not rid.split("/", 1)[1]:
            raise ExitsUnreadable(f"{path}: row {index} id {rid!r}; expected '<key|route:..|joint:..|kind:..>/<variant>'")
        found = _row_problems(str(path), "walk", rid, {k: v for k, v in row.items() if k in ROW_KEYS})
        found += [f"{path}: row {rid!r} has unknown field {key!r}; expected only {list(WALK_ROW_KEYS)}" for key in sorted(set(row) - set(WALK_ROW_KEYS))]
        if strict and not found:
            found = walk_row_problems(path, row, universe=universe, seeds=seeds or {}, class_of_subject=class_of_subject, story_dir=story_dir)
        problems.extend(found)
        rows.append(row)
    if problems:
        raise ExitsUnreadable("\n".join(problems))
    return rows


def load_walk_rows(walk_dir=None, *, strict: bool = False, universe=None, seeds_dir=None, class_of_subject=None, story_dir=None) -> dict:
    """The walk rows of the dry story, `{id: row + {"_path": path}}`, from `fixtures/stories/dry-1/exits/*.json`. The directory is created
    by the walk nodes (N4): while it is absent there are no rows (TEMPORAL; stated in the report). Present but unreadable, a row with no id
    or reach, an unknown field, an empty `rows` list, an id in two files: `ExitsUnreadable`. `strict=True` (the walker's call) is the whole
    grammar; the census and `driven_keys` call it non-strict - one reader, the same files."""
    walk_dir = Path(walk_dir or WALK_DIR)
    if not walk_dir.is_dir():
        return {}
    rows: dict = {}
    for path in sorted(walk_dir.glob("*.json")):
        seeds = load_seeds(Path(seeds_dir) / path.name) if strict and seeds_dir else {}
        for row in load_group_file(path, strict=strict, universe=universe, seeds=seeds, class_of_subject=class_of_subject, story_dir=story_dir):
            rid = row["id"]
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
    _ledger_orphans(Path(ledger_path or directory / "known_red.json"), walk, red)
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
    walked = {_subject_of(rid)[:2] for rid in walk}
    for rid, row in sorted(walk.items()):
        section, subject = _subject_of(rid)[:2]
        reach = str(row.get("reach"))
        if (subject not in universe.prices) if section == "key" else (subject not in census[section]):
            red(f"walk row {rid} ({row['_path']}): {subject!r} is not a key of question-prices.json, a route, a joint or a kind without a key "
                f"(a route, joint or kind id carries its namespace `route:`/`joint:`/`kind:`); fix the id, or add the key/route to its table")
        if reach in COUNT_ONLY:
            red(f"walk row {rid}: reach {reach} is a count of the group files, not a walk row's reach; give the row story, seed, live_only or "
                f"after:<finding>, or remove it")
    for section in SECTIONS:
        for name, row in sorted(census[section].items()):
            reach = str(row.get("reach"))
            if reach == "hook_layer":
                red(f"{section[:-1]} {name}: reach hook_layer is a count (the hook refusals are not rows of a group file); fix the row")
            if reach in EXECUTABLE and (section, name) not in walked:
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


def _ledger_orphans(ledger: Path, walk: dict, red) -> None:
    """I8: a ledger id that is neither a `main...` stage row nor the id of a written walk row can never be reported by any part - red naming it.
    (A part's ledger of its own, like the self-test's, is another file and is never read here.) An unreadable ledger is `_ledger`'s line."""
    try:
        import known_red
        ids = list(known_red.load(ledger))
    except Exception:
        return
    for rid in ids:
        if not (rid.startswith("main/") or rid.startswith("main:") or rid in walk):
            red(f"label ledger row {rid} names no walk row and no main stage; no part can ever report it - rename or remove it ({ledger})")


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


# ---------------------------------------------------------------------------------------------------- the walk rows (node N4w)
def _cut(text, n: int = 300) -> str:
    return " ".join(str(text).split())[:n]


def _subject_of(rid: str) -> tuple:
    """`(section, name, variant)` of a walk row id (F-W2 (a)): a bare subject is a price key (`section` "key"); `route:`, `joint:`, `kind:` name the
    section of the census. Never raises: an id with no `/` gives an empty variant, the caller refuses it."""
    subject, _, variant = str(rid).partition("/")
    prefix, sep, rest = subject.partition(":")
    if sep and prefix in NAMESPACES and rest:
        return NAMESPACES[prefix], rest, variant
    return "key", subject, variant


def _prefix_of(section: str) -> str:
    return next((f"{prefix}:" for prefix, name in NAMESPACES.items() if name == section), "")


def variant_problem(section: str, name: str, variant: str, universe) -> str:
    """"" when `variant` is in the vocabulary of the subject, else the sentence naming what it may be (EW10): a key - its price answers, `free words`,
    `empty`, `words:<case>`; a code route - `code move`; a joint - `repair`, `no repair`, `word` (F-W3 (a)); a route that asks a person and a kind -
    `free words`, `empty`, `words:<case>` and `<why>:<token>` with a `why` of the seam's closed list (F-W15 (a))."""
    cases = why = False
    if section == "key":
        fixed, cases = [str(r.get("answer")) for r in universe.prices.get(name, [])] + [V_FREE, V_EMPTY], True
    elif section == "joints":
        fixed = list(JOINT_VARIANTS)
    elif section == "routes" and universe.routes.get(name) != "ask_person":
        fixed = [V_CODE]
    else:
        fixed, cases, why = [V_FREE, V_EMPTY], True, True
    if variant in fixed or (cases and CASE_VARIANT_RE.match(variant)):
        return ""
    found = WHY_VARIANT_RE.match(variant)
    if why and found and found.group(1) in WHY_VALUES:
        return ""
    allowed = fixed + (["words:<case>"] if cases else []) + ([f"<why>:<token> with why one of {list(WHY_VALUES)}"] if why else [])
    return f"variant {variant!r} is outside the vocabulary of {name!r}; expected one of {allowed}"


def resolve_words_file(story_dir, name) -> tuple:
    """`(path, problem)` of a row's `words_file` (EW14): relative to the story folder, no `..`, resolving INSIDE it, and a file that exists. One
    reader for the loader and for `dry_world.answer_bytes` (AR-13)."""
    if not isinstance(name, str) or not name.strip():
        return None, "words_file is not a path; expected a file name inside the story folder"
    given = Path(name)
    if given.anchor or ".." in given.parts:
        return None, f"words_file {name!r} must be relative to the story folder and hold no `..`"
    base = Path(story_dir).resolve()
    path = (base / given).resolve()
    try:
        path.relative_to(base)
    except ValueError:
        return None, f"words_file {name!r} resolves outside the story folder {base}"
    if not path.is_file():
        return None, f"words_file {name!r} is not a file in the story folder {base}"
    return path, ""


def _carrier_problem(carrier) -> str:
    """"" when `carrier` is `<path>:<line>` and the path (absolute, or relative to the repository root) is a file with that many lines."""
    found = CARRIER_RE.match(carrier) if isinstance(carrier, str) else None
    if not found:
        return f"carrier {carrier!r} is not `<path>:<line>`"
    path = Path(found.group(1))
    path = path if path.is_absolute() else PACKAGE.parents[1] / path
    if not path.is_file():
        return f"carrier {carrier!r}: {path} is not a file"
    lines = len(path.read_text(encoding="utf-8", errors="replace").splitlines())
    return "" if 1 <= int(found.group(2)) <= lines else f"carrier {carrier!r}: the file has {lines} line(s)"


def walk_row_problems(path, row, *, universe, seeds, class_of_subject=None, story_dir=None) -> list:
    """The grammar of ONE walk row (spec section 8), every refusal naming the row id and the field (EW4-EW10, EW14-EW16, I2, I3). `seeds` is the
    `recipes` mapping of `seeds/<group>.json` ({} when the file is absent); `class_of_subject(section, name) -> class word` is what C4 needs (a
    row listing C4 with none given is refused: the class is never guessed, FR-59); `story_dir` lets `words_file` be resolved. Nothing here runs
    a world."""
    where = str(path)
    rid = row.get("id") if isinstance(row, dict) else None
    if not isinstance(rid, str):
        return [f"{where}: a row has no id; expected a string '<subject>/<variant>'"]
    out: list = []

    def bad(text: str) -> None:
        out.append(f"{where}: row {rid!r}: {text}")

    for key in sorted(set(row) - set(WALK_ROW_KEYS)):
        bad(f"unknown field {key!r}; expected only {list(WALK_ROW_KEYS)}")
    section, name, variant = _subject_of(rid)
    known = {"key": universe.prices, "routes": universe.routes, "joints": universe.joints, "kinds_without_key": universe.kinds}[section]
    if name not in known:
        bad(f"{name!r} is not a key of question-prices.json" if section == "key" else f"{name!r} is not a {section[:-1]} of the driver")
        if section == "key":
            out[-1] += "; a route, joint or kind id needs its namespace `route:`/`joint:`/`kind:`"
    else:
        found = variant_problem(section, name, variant, universe)
        if found:
            bad(found)
    if row.get("start") not in STARTS:
        bad(f"start {row.get('start')!r}; expected one of {list(STARTS)} (a static `after:` belongs to `reach`, F-W14)")
    expect = row.get("expect")
    if expect is None:
        expect = {}
    elif not isinstance(expect, dict):
        bad(f"`expect` is {type(expect).__name__}; expected an object with {list(EXPECT_KEYS)}")
        expect = {}
    for key in sorted(set(expect) - set(EXPECT_KEYS)):
        bad(f"unknown field {key!r} in `expect`; expected only {list(EXPECT_KEYS)}")
    question = expect.get("owner_question")
    if question is not None and not (isinstance(question, str) and QUESTION_RE.match(question)):
        bad(f"expect.owner_question {question!r}; expected null or 'Q<number>'")
    runnable = row.get("reach") in EXECUTABLE and question is None
    checks = expect.get("checks")
    if checks is None:
        checks = []
    if not isinstance(checks, list) or not all(isinstance(c, str) for c in checks):
        bad("expect.checks is not a list of check ids")
        checks = []
    for check_id in checks:
        if check_id not in CHECK_IDS:
            bad(f"unknown check {check_id!r}; expected one of {list(CHECK_IDS)}")
    if len(set(checks)) != len(checks):
        bad("expect.checks names a check twice")
    if runnable and not checks:
        bad("a row that runs has an empty or absent expect.checks; a row with no check never passes (name the checks it judges)")
    if "C4" in checks:
        if class_of_subject is None:
            bad("C4 is listed and no class source was given; C4 is the gate check and the class is never guessed")
        elif name in known and class_of_subject(section, name) not in GATE_CLASSES:
            bad(f"C4 is the gate check; the class of {name!r} is {class_of_subject(section, name)!r}")
    quote = expect.get("owner_quote")
    if quote is not None:
        if not isinstance(quote, dict):
            bad("expect.owner_quote is not an object with `text` and `carrier`")
        else:
            for key in sorted(set(quote) - set(OWNER_QUOTE_KEYS)):
                bad(f"unknown field {key!r} in `expect.owner_quote`; expected only {list(OWNER_QUOTE_KEYS)}")
            if not isinstance(quote.get("text"), str) or not quote["text"].strip():
                bad("expect.owner_quote has no `text`; expected the owner's words")
            problem = _carrier_problem(quote.get("carrier"))
            if problem:
                bad(f"expect.owner_quote {problem}")
    answer = row.get("answer")
    if answer is None:
        answer = {}
    elif not isinstance(answer, dict):
        bad(f"`answer` is {type(answer).__name__}; expected an object with {list(ANSWER_KEYS)}")
        answer = {}
    for key in sorted(set(answer) - set(ANSWER_KEYS)):
        bad(f"unknown field {key!r} in `answer`; expected only {list(ANSWER_KEYS)}")
    for key in ANSWER_KEYS:
        value = answer.get(key)
        if value is not None and not isinstance(value, str):
            bad(f"answer.{key} is {type(value).__name__}; expected text or null")
        elif isinstance(value, str) and not value.strip() and variant != V_EMPTY:
            bad(f"answer.{key} is blank; an empty answer is only the `{V_EMPTY}` variant")
    if answer.get("words") is not None and answer.get("words_file") is not None:
        bad("`answer.words` and `answer.words_file` are both set; one answer, one source")
    given = any(answer.get(key) is not None for key in ANSWER_KEYS)
    if runnable and variant == V_EMPTY and given:
        bad(f"variant `{V_EMPTY}` carries an answer field; expected token, words and words_file all null")
    if runnable and variant != V_EMPTY and not given:
        bad(f"all answer fields are null on variant {variant!r}; an empty answer is only the `{V_EMPTY}` variant")
    if story_dir is not None and isinstance(answer.get("words_file"), str):
        problem = resolve_words_file(story_dir, answer["words_file"])[1]
        if problem:
            bad(problem)
    seed = row.get("seed")
    if seed is not None and (not isinstance(seed, str) or not seed.strip()):
        bad(f"seed {seed!r}; expected null or the id of a recipe of seeds/<group>.json")
    elif seed is not None and seed not in seeds:
        bad(f"seed {seed!r} is not a recipe of seeds/{Path(where).stem}.json ({len(seeds)} recipe(s): {sorted(seeds)}); write the recipe, or set seed to null")
    if runnable and row.get("why_unreached") not in (None, ""):
        bad("why_unreached on a row that runs; the field says why a row is NOT run (one meaning per field)")
    stub = row.get("stub")
    if stub is not None and not isinstance(stub, dict):
        bad(f"`stub` is {type(stub).__name__}; expected the control grammar of the story's `stub` (an object)")
    elif isinstance(stub, dict) and "conductor" in stub and not isinstance(stub["conductor"], dict):
        bad("stub.conductor is not an object")
    return out


def _seed_problems(where: str, recipes) -> list:
    out: list = []
    if not isinstance(recipes, dict):
        return [f"{where}: `recipes` is {type(recipes).__name__}; expected an object of recipe id -> list of steps"]
    for rid, steps in recipes.items():
        if not isinstance(steps, list) or not steps:
            out.append(f"{where}: recipe {rid!r} is not a non-empty list of steps (a row that needs no seed says `seed: null`)")
            continue
        for index, step in enumerate(steps):
            at = f"{where}: recipe {rid!r} step {index}"
            if not isinstance(step, dict) or len(step) != 1 or next(iter(step)) not in SEED_STEP_KEYS:
                out.append(f"{at} is not an object with exactly one of {list(SEED_STEP_KEYS)}")
            elif "drive_until" in step:
                until = step["drive_until"]
                if not isinstance(until, dict) or set(until) != set(DRIVE_UNTIL_KEYS) or not all(isinstance(v, str) and v.strip() for v in until.values()):
                    out.append(f"{at}: drive_until must be an object with exactly {list(DRIVE_UNTIL_KEYS)}, both text")
                elif not re.match(r"^S[0-9]$", until["stage"]):
                    out.append(f"{at}: drive_until.stage {until['stage']!r}; expected S0..S9")
            else:
                op = step["op"]
                if not isinstance(op, list) or not op or not all(isinstance(a, str) for a in op):
                    out.append(f"{at}: op must be a non-empty list of text ([script, args...])")
                elif op[0] not in OP_SCRIPTS:
                    out.append(f"{at}: op script {op[0]!r} is not on the closed list {list(OP_SCRIPTS)} (a seed never writes a file by hand, P1-b 4.3)")
    return out


def load_seeds(path) -> dict:
    """The `recipes` of `seeds/<group>.json` (`{"schema": 1, "group": g, "recipes": {id: [step, ...]}}`); an ABSENT file is `{}` (a row that names a
    recipe is then refused naming the file, EW5). Unreadable, an unknown key, a group that is not the file stem, a recipe that is not a non-empty
    list of closed steps: `ExitsUnreadable` naming the file (before any world)."""
    path = Path(path)
    if not path.is_file():
        return {}
    data = _read_json(path, "an object with schema, group and recipes")
    if not isinstance(data, dict):
        raise ExitsUnreadable(f"{path}: the top level is {type(data).__name__}; expected an object with {list(SEED_FILE_KEYS)}")
    problems = [f"{path}: unknown top-level key {key!r}; expected only {list(SEED_FILE_KEYS)}" for key in sorted(set(data) - set(SEED_FILE_KEYS))]
    if data.get("schema") != 1:
        problems.append(f"{path}: schema is {data.get('schema')!r}; expected 1")
    if data.get("group") != path.stem:
        problems.append(f"{path}: group is {data.get('group')!r}; expected the file stem {path.stem!r}")
    problems += _seed_problems(str(path), data.get("recipes"))
    if problems:
        raise ExitsUnreadable("\n".join(problems))
    return data["recipes"]


def subject_class(section: str, name: str, census: dict, universe) -> str:
    """The class word of a walk subject for C4 (the rule is data in `classes.json`, read through `class_of`, AR-13): a key by its `question:<key>`
    source, a route or joint by its census row, a kind has none (`n/a`)."""
    classes = census["classes"]
    if section == "key":
        return classes.get("by_source", {}).get(f"question:{name}") or classes.get("default") or CLASS_UNKNOWN
    return class_of(census[section].get(name, {}), classes, section=section, action=universe.routes.get(name, ""), joints=universe.joints,
                    registry=universe.registry)


@dataclass(frozen=True)
class Outcome:
    """The one outcome of a row: `kind` pass / fail / note; a note carries its `tag` (live_only, after, owner_question, pending_judge, rounds_unknown),
    an `after` note its `node`; `changed` is whether the answer changed the state fingerprint (None: not measured)."""
    kind: str
    detail: str = ""
    tag: str = ""
    node: str = ""
    changed: object = None


def _norm(token) -> str:
    from driver_dialog import DriverDialog
    return DriverDialog.s0_normalize(str(token))


def rework_problem(options, author: str) -> str:
    """C9 (FV1-6): "" when among `options` there is a move `rework_stage` whose `args.role` is the stage's author; else the sentence. An option with no
    `args.role` counts as missing (the executor is not named, FR-42)."""
    moves = [o for o in options or [] if isinstance(o, dict) and (o.get("move") or o.get("action")) == "rework_stage"]
    if not moves:
        return "none of the offered options is a `rework_stage` move"
    roles = [str(((o.get("args") or {}) if isinstance(o.get("args"), dict) else {}).get("role") or "") for o in moves]
    if author not in roles:
        return f"no `rework_stage` option names the author {author!r} in args.role (found {roles}); executor not named"
    return ""


def judge_row(row: dict, facts: dict, *, prices: dict, class_of_subject: str = "", classes=GATE_CLASSES) -> Outcome:
    """The ONE outcome of a row that ran, from `facts` alone (it opens no file: AR-13, AR-29 - the data is compared, the expectation is SET by the
    row's `expect.checks`). It judges exactly the listed checks in order, then the always-checks (K15/E17 for a key subject, E18, the route record).
    A failing check is a FAIL naming the check and the evidence (cut at 300); a listed C7/C8/C10 is a NOTE `pending judge` (EW26), never green; a C3
    that cannot be established (`rounds unknown`, EW19) is a NOTE; every listed check passing is a PASS. `facts` keys: see `dry_world.row_facts`."""
    rid = row["id"]
    section, name, variant = _subject_of(rid)
    checks = list((row.get("expect") or {}).get("checks") or [])
    seed = facts.get("seed") or {"reached": True}
    if facts.get("over_cap"):
        return Outcome("fail", f"{rid}: over the cap {facts.get('cap')} s at {facts['over_cap']}")
    if not seed.get("reached"):
        return Outcome("fail", f"seed did not reach {name}: {_cut(seed.get('detail', ''))}")
    ask, token = facts.get("ask"), (row.get("answer") or {}).get("token")
    fp_ask, fp_after = facts.get("fp_ask"), facts.get("fp_after")
    changed = None if fp_ask is None or fp_after is None else fp_ask != fp_after
    results: list = []        # (check, "ok" | "fail" | "note", detail)

    def put(check_id, status, detail=""):
        results.append((check_id, status, _cut(detail)))

    for check_id in checks:
        if check_id == "C2":
            offered = list((ask or {}).get("offered") or []) or [a for a in (facts.get("priced_at_ask") or {}).get("answers") or []]
            records = [r for r in facts.get("answer_records") or [] if r.get("question_sha") == facts.get("ask_sha")]
            whys, calls = list(facts.get("conductor_whys") or []), int(facts.get("conductor_calls") or 0)
            if not ask:
                put(check_id, "fail", "no question was pending at the target, so no variant was offered")
            elif token and not offered:
                put(check_id, "fail", f"the ask {ask.get('kind')!r} carries no offered set and no priced record names one; C2 cannot be established")
            elif token and _norm(token) not in {_norm(o) for o in offered}:
                put(check_id, "fail", f"the token {token!r} was not offered at {ask.get('kind')!r} (offered {sorted(map(str, offered))})")
            elif not records:
                put(check_id, "fail", f"the driver recorded no answer for this ask (no driver-answers.jsonl row with its question_sha; {len(facts.get('answer_records') or [])} row(s) added)")
            elif "unread_answer" in whys or (calls and not whys):
                put(check_id, "fail", "a conductor call followed the answer" + (" with why unread_answer" if "unread_answer" in whys else " and its why is not on record"))
            else:
                put(check_id, "ok")
        elif check_id == "C3":
            if fp_ask is None or fp_after is None:
                put(check_id, "fail", "no state fingerprint was taken at the ask and after the answer")
            elif any("rounds unknown" in str(n) for n in facts.get("fp_notes") or ()):
                put(check_id, "note", "rounds unknown: no dispatch records, so the fingerprint cannot tell a new round with the same bytes")
            elif not changed:
                put(check_id, "fail", "the answer changed nothing: the state fingerprint is the one it was asked at (C3)")
            else:
                put(check_id, "ok")
        elif check_id == "C4":
            if class_of_subject not in classes:
                put(check_id, "fail", f"C4 is the gate check; the class of {name!r} is {class_of_subject!r}")
            elif int(facts.get("passed_lines") or 0) < 1:
                put(check_id, "fail", "no new line in state/passed-by-person.jsonl: the person's word did not pass the block")
            else:
                put(check_id, "ok")
        elif check_id == "C5":
            put(check_id, "fail" if facts.get("loop") else "ok", facts.get("loop") or "")
        elif check_id == "C6":
            gates = facts.get("gates") or []
            wrong = [g for g in gates if g.get("ready") is not True]
            put(check_id, "fail" if wrong or not gates else "ok",
                "no gate question was met by the row" if not gates else "; ".join(f"{g.get('kind')}: gate_ready {g.get('ready')!r} {g.get('detail', '')}" for g in wrong))
        elif check_id == "C9":
            rework = facts.get("rework")
            problem = "no stage_review_exhausted ask with options was observed" if not rework else rework_problem(rework.get("options"), rework.get("author", ""))
            put(check_id, "fail" if problem else "ok", problem)
        elif check_id == V_EMPTY:
            after = facts.get("asked_after") or {}
            if not facts.get("empty_refused"):
                put(check_id, "fail", "the driver did not refuse the empty answer (no `is empty` line); an empty answer silently taken is red")
            elif not ask or (after.get("kind"), after.get("stage")) != (ask.get("kind"), ask.get("stage")):
                put(check_id, "fail", f"the ask is no longer pending after the empty answer (was {ask and ask.get('kind')!r}, now {after.get('kind')!r})")
            else:
                put(check_id, "ok")
    if section == "key":
        priced, rows = facts.get("priced_at_ask"), {str(r.get("answer")) for r in prices.get(name, [])}
        if not priced or priced.get("key") != name:
            put("K15", "fail", f"key not observed: expected {name}, observed {priced.get('key') if priced else 'none'}")
        elif not priced.get("answers") or not set(map(str, priced["answers"])) <= rows:
            put("K15", "fail", f"the answers the question offered {sorted(map(str, priced.get('answers') or []))} are not all price rows of {name} ({sorted(rows)})")
    if section == "routes" and name not in (facts.get("routes_added") or []):
        put("route", "fail", f"route not observed: {name!r} was not matched by the driver during the row (state/dry-routes.jsonl)")
    if section == "joints":
        needle = name.rstrip("*")
        if needle not in str(facts.get("refusal_text") or ""):
            put("joint", "fail", f"joint not observed: no refusal line of the driver names {needle!r}")
    if any(str(line.get("run_class") or "") != "dry" for line in facts.get("stub_added") or []):
        put("E18", "fail", "a stub journal line the row added does not carry run_class dry")
    if facts.get("exhausted"):
        put("turns", "fail", f"{rid}: {facts.get('post_turns')} post-answer turns with no new ask and no loop")
    fails = [f"{c}: {d}" if d else c for c, s, d in results if s == "fail"]
    pending = [c for c in checks if c in CHECKS_PENDING]
    if fails:
        return Outcome("fail", "; ".join(fails), changed=changed)
    if pending:
        done = ", ".join(f"{c} {s}" for c, s, _d in results)
        return Outcome("note", f"pending judge {', '.join(pending)}" + (f" (judged: {done})" if done else ""), tag="pending_judge", changed=changed)
    notes = [f"{c}: {d}" for c, s, d in results if s == "note"]
    if notes:
        return Outcome("note", "; ".join(notes), tag="rounds_unknown", changed=changed)
    return Outcome("pass", changed=changed)


def judge_group(outcomes: list, ledger_path, ids: list) -> list:
    """The lines of a part, `[(name, kind, detail)]` (kind pass / fail / note; the name is a row id, `known_red`, `alive` or `outcomes`), from the
    `[(row id, Outcome)]` the rows produced. Rows that RAN (pass / fail) go to `known_red.reconcile` with the ledger FILTERED to the ids of this group's
    file (a ledger row of another group is no `unknown row` here, I6); rows that did not run are NOTEs and are never in the results. E15 (F-W16 (a)):
    a ledger row for a row whose outcome is `after:<node>` with the SAME node is red. The check `outcomes` is PASS only when every id of the file has
    exactly one outcome (I1). `alive`: a subject whose rows all ran and whose every variant but `stop` and `empty` left the fingerprint unchanged is red."""
    import known_red
    wanted = list(ids)
    by_id: dict = {}
    for rid, outcome in outcomes:
        by_id.setdefault(rid, []).append(outcome)
    lines: list = []
    try:
        ledger_all = known_red.load(ledger_path)
    except known_red.LedgerError as exc:
        ledger_all = None
        lines.append(("known_red", "fail", str(exc)))
    ledger = {rid: row for rid, row in (ledger_all or {}).items() if rid in set(wanted)}
    single = {rid: found[0] for rid, found in by_id.items() if len(found) == 1}
    for rid, outcome in single.items():
        if outcome.tag == "after" and rid in ledger and ledger[rid].node == outcome.node:
            lines.append(("known_red", "fail", f"a row is never expected red for the defect that made it unreachable: {rid} is after:{outcome.node} and the ledger names {outcome.node} for it"))
            del ledger[rid]
    results = {rid: o.kind == "pass" for rid, o in single.items() if o.kind in ("pass", "fail")}
    for rid in wanted:
        for outcome in by_id.get(rid, []):
            if outcome.kind == "pass":
                lines.append((rid, "pass", ""))
            elif outcome.kind == "fail":
                lines.append((rid, "note" if rid in ledger else "fail", f"red evidence: {outcome.detail}" if rid in ledger else outcome.detail))
            else:
                lines.append((rid, "note", outcome.detail))
    known: tuple = ()
    if ledger_all is not None:
        verdict = known_red.reconcile(results, ledger, ledger_path=str(ledger_path))
        lines += [("known_red", "fail", problem) for problem in verdict.problems] + [("known_red", "note", text) for text in verdict.known]
        known = verdict.known
    subjects: dict = {}
    for rid in wanted:
        section, name, variant = _subject_of(rid)
        if len(by_id.get(rid, [])) == 1:
            subjects.setdefault((section, name), []).append((variant, by_id[rid][0], rid))
    for (section, name), rows in subjects.items():
        if any(o.kind not in ("pass", "fail") or o.changed is None for _v, o, _r in rows):
            continue
        moving = [(v, o, r) for v, o, r in rows if v != "stop" and not v.endswith(":stop") and v != V_EMPTY]
        if moving and all(o.changed is False for _v, o, _r in moving):
            text = f"alive only stop: {_prefix_of(section)}{name}: every variant but stop left the state fingerprint unchanged ({', '.join(v for v, _o, _r in moving)})"
            # applied AFTER the rows were judged and reconciled: softened only when EVERY contributing variant is red AND still labelled in the ledger
            if all(o.kind == "fail" and r in ledger for _v, o, r in moving):
                lines.append(("alive", "note", f"{text}; known red: " + "; ".join(f"{r} -> {ledger[r].node}" for _v, _o, r in moving)))
            else:
                lines.append(("alive", "fail", text))
    problems = [f"{rid}: {len(by_id.get(rid, []))} outcome(s)" for rid in wanted if len(by_id.get(rid, [])) != 1]
    problems += [f"{rid}: an outcome for a row the file does not hold" for rid in by_id if rid not in set(wanted)]
    tally: dict = {}
    for rid in wanted:
        for o in by_id.get(rid, []):
            word = "known red" if o.kind == "fail" and rid in ledger else {"pass": "pass", "fail": "fail"}.get(o.kind) or (o.tag or "note").replace("_", " ")
            tally[word] = tally.get(word, 0) + 1
    detail = f"{len(wanted)} rows: " + ", ".join(f"{n} {word}" for word, n in sorted(tally.items())) if not problems else "; ".join(problems)
    lines.append(("outcomes", "fail" if problems else "pass", detail))
    return lines


def group_unwalked(group: str, census, walk_rows: list, prices: dict, *, routes=None) -> tuple:
    """`(count, [text])` of the `unwalked` NOTE of a group (F-W9 (a)): the census entries of `driver-exits/<group>.json` whose reach is `unwalked`, plus
    the variants §3.3 demands of the subjects the group's walk rows name and no row writes (a key: each price answer + `free words` + `empty`; a code
    route: `code move`; a joint: `repair`, `no repair`, `word`; a kind and an asking route have open options and demand none). Price keys with no row
    at all stay with the census (P1-b section 3.2). No census file for the group (`census` None, or the group is not in it): 0 and the NOTE saying so."""
    if not census or group not in census.get("groups", []):
        return 0, [f"no census file for group {group}: unwalked not counted"]
    names = [f"{_prefix_of(section)}{name}" for section in SECTIONS for name, row in census[section].items()
             if row.get("reach") == "unwalked" and Path(census["where"][(section, name)]).stem == group]
    have: dict = {}
    for row in walk_rows:
        section, name, variant = _subject_of(row["id"])
        have.setdefault((section, name), []).append(variant)
    missing: list = []
    for (section, name), variants in have.items():
        if section == "key":
            demanded = [str(r.get("answer")) for r in prices.get(name, [])] + [V_FREE, V_EMPTY]
        elif section == "joints":
            demanded = list(JOINT_VARIANTS)
        elif section == "routes" and routes is not None and routes.get(name) not in (None, "ask_person"):
            demanded = [V_CODE]
        else:
            demanded = []
        missing += [f"{_prefix_of(section)}{name}/{v}" for v in demanded if v not in variants]
    total = len(names) + len(missing)
    return total, [f"{total} (census unwalked {len(names)}: {', '.join(names) or 'none'}; variants without a row {len(missing)}: {', '.join(missing) or 'none'})"]


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

    def check(directory=None, walk_dir=None, universe=None, ledger_path=None):
        """ISOLATION (t-828): every selftest case builds its own tree against a fake universe, so a call that names no `walk_dir` gets its own EMPTY
        temp one - never the real `fixtures/stories/dry-1/exits/` (a real group file would turn the cases red: the result must not depend on which
        real group files exist). The real module-level `check` is called, nothing else changes."""
        return globals()["check"](directory, walk_dir if walk_dir is not None else tmp(), universe, ledger_path)

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

    @case("isolation: a real-looking walk file where the DEFAULT walk_dir points does not change a fake-universe case's verdict")
    def _():
        mod = globals()
        planted = tmp()
        _write(planted / "s0.json", {"schema": 1, "group": "s0", "rows": [{"id": "kind:halt/free words", "reach": "seed", "start": "S1"}]})
        saved = mod["WALK_DIR"]
        mod["WALK_DIR"] = planted
        try:
            isolated = check(_tree(tmp()), universe=_universe())
            leaking = mod["check"](_tree(tmp()), None, _universe())          # control: the real check with the default directory does read it
        finally:
            mod["WALK_DIR"] = saved
        return None if not isolated.problems and leaking.problems else f"isolated {isolated.problems}; control (default dir) {leaking.problems}"

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
        report = check(_tree(root, seed_r1), walk_with(root, "route:r1/a"), universe=_universe())
        return None if not report.problems else f"got {report.problems}"

    @case("walk: a walk row with reach unwalked or hook_layer is red (a count, not a walk row's reach)")
    def _():
        for reach in ("unwalked", "hook_layer"):
            root = tmp()
            report = check(_tree(root), walk_with(root, "route:r1/a", reach), universe=_universe())
            if not any("walk row route:r1/a" in p and f"reach {reach}" in p for p in report.problems):
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

    _walker_cases(case, tmp)
    return cases


def _walker_cases(case, tmp) -> None:
    """The table of node N4w (spec 5.1: the pure functions get synthetic facts and files in a temp dir; `run_seed` / `drive_main` get a fake driver)."""
    import types
    uni = _universe(routes={"r1": "continue", "r2": "ask_person", UNMATCHED: "conductor"}, joints=["exit:j1", "exit:g:*"])

    def wrow(rid="p.key/a", **kw):
        row = {"id": rid, "start": "S1", "seed": None, "answer": {"token": "a", "words": None, "words_file": None}, "reach": "story",
               "expect": {"checks": ["C3"]}}
        row.update(kw)
        return row

    def probs(row, seeds=None, **kw):
        return walk_row_problems("g.json", row, universe=uni, seeds=seeds or {}, **kw)

    refusals = [
        ("EW4 unknown field of a row", wrow(extra=1), "unknown field 'extra'"),
        ("EW4 unknown field of the answer", wrow(answer={"token": "a", "tokens": 1}), "unknown field 'tokens' in `answer`"),
        ("EW4 unknown field of expect", wrow(expect={"checks": ["C3"], "check": []}), "unknown field 'check' in `expect`"),
        ("EW5 a seed recipe that the seeds file does not hold", wrow(seed="nope"), "seed 'nope' is not a recipe"),
        ("EW8 a bare id that is no price key needs its namespace", wrow("r1/code move"), "needs its namespace"),
        ("EW9 a subject the driver does not have", wrow("route:gone/code move"), "'gone' is not a route"),
        ("EW10 a variant outside the key's vocabulary", wrow("p.key/zzz"), "variant 'zzz' is outside"),
        ("a route with a code move has one variant", wrow("route:r1/free words"), "variant 'free words' is outside"),
        ("an asking route takes a `<why>:<token>` variant of the closed list only", wrow("route:r2/nonsense:x"), "variant 'nonsense:x' is outside"),
        ("start outside S0..S9 and fresh", wrow(start="S10"), "start 'S10'"),
        ("I2 a row that runs with no check", wrow(expect={"checks": []}), "empty or absent expect.checks"),
        ("an unknown check id", wrow(expect={"checks": ["C99"]}), "unknown check 'C99'"),
        ("EW15 words and words_file together", wrow(answer={"token": None, "words": "x", "words_file": "f.txt"}), "both set"),
        ("EW16 all answer fields null on a variant other than empty", wrow(answer={"token": None, "words": None, "words_file": None}), "all answer fields are null"),
        ("EW16 a field set on the empty variant", wrow("p.key/empty", answer={"token": "a"}, expect={"checks": ["empty"]}), "carries an answer field"),
        ("a blank token is not an answer", wrow(answer={"token": "  "}), "is blank"),
        ("why_unreached on a row that runs", wrow(why_unreached="x"), "why_unreached on a row that runs"),
        ("an owner_quote whose carrier is no file", wrow(expect={"checks": ["C3"], "owner_quote": {"text": "t", "carrier": "no/such/file.md:3"}}), "is not a file"),
        ("an owner_question that is no Q<n>", wrow(expect={"checks": ["C3"], "owner_question": "first"}), "owner_question"),
        ("C4 with no class source", wrow(expect={"checks": ["C4"]}), "no class source"),
    ]
    for label, row, needle in refusals:
        @case(f"walk grammar: {label} is refused naming the row and the field")
        def _(row=row, needle=needle):
            got = "\n".join(probs(row))
            return None if needle in got and repr(row["id"]) in got else f"got {got!r}"

    @case("walk grammar: C4 on a subject that is not of the gate class is refused naming the class")
    def _():
        got = "\n".join(probs(wrow(expect={"checks": ["C4"]}), class_of_subject=lambda s, n: "ban"))
        ok = probs(wrow(expect={"checks": ["C4"]}), class_of_subject=lambda s, n: "gate")
        return None if "gate check; the class of 'p.key' is 'ban'" in got and not ok else f"got {got!r} / {ok}"

    @case("walk grammar: EW14 a words_file that is absolute, climbs, is absent or is a real file in the folder")
    def _():
        folder = tmp()
        (folder / "w.txt").write_bytes(b"a\r\nb")
        bad = ["../x.txt", str(folder / "w.txt"), "absent.txt", "/rooted.txt"]
        for name in bad:
            if "words_file" not in "\n".join(probs(wrow(answer={"words_file": name}), story_dir=folder)):
                return f"{name!r} not refused"
        return None if not probs(wrow(answer={"words_file": "w.txt"}), story_dir=folder) else "a file inside the folder was refused"

    @case("walk grammar: a complete row and a live_only row with no checks pass; `*` joints and `<why>:<token>` are in vocabulary")
    def _():
        rows = [wrow(), wrow("p.key/empty", answer={}, expect={"checks": ["empty"]}), wrow("p.key/free words", answer={"words": "w"}),
                wrow("p.key/words:long", answer={"words": "w"}), wrow("joint:exit:g:*/word", answer={"token": "x"}, expect={"checks": ["C3"]}),
                wrow("route:r1/code move", answer={"token": "x"}), wrow("kind:k1/stage_review_exhausted:rework_stage", answer={"token": "x"}),
                wrow("p.key/b", reach="live_only", why_unreached="needs a live dispatch", expect={"checks": []}, answer=None)]
        got = [p for row in rows for p in probs(row)]
        return None if not got else f"got {got}"

    def group_file(rows, group="g", **extra):
        root = tmp()
        _write(root / f"{group}.json", {"schema": 1, "group": group, "rows": rows, **extra})
        return root / f"{group}.json"

    @case("walk loader: EW2 an empty rows list is refused in both modes, naming the file")
    def _():
        path = group_file([])
        for strict in (False, True):
            try:
                load_group_file(path, strict=strict, universe=uni)
            except ExitsUnreadable as exc:
                if "g.json" not in str(exc):
                    return f"{strict}: {exc}"
                continue
            return f"{strict}: no refusal"
        return None

    @case("walk loader: EW3/EW4 broken JSON names the file; an unknown row field is refused in the census mode too")
    def _():
        broken = tmp() / "g.json"
        broken.write_text("{bad", encoding="utf-8")
        for path, needle in ((broken, "g.json"), (group_file([{"id": "p.key/a", "reach": "seed", "start": "S1", "bogus": 1}]), "'bogus'")):
            try:
                load_group_file(path, universe=uni)
            except ExitsUnreadable as exc:
                if needle not in str(exc):
                    return f"{needle}: {exc}"
                continue
            return f"{needle}: no refusal"
        return None

    @case("walk loader: strict mode wants the group to be the file stem and refuses the unknown top-level key of the file")
    def _():
        path = group_file([wrow()], group="g", extra=1)
        try:
            load_group_file(path, strict=True, universe=uni)
        except ExitsUnreadable as exc:
            return None if "'extra'" in str(exc) else f"got {exc}"
        return "no refusal"

    @case("seeds: an absent file is no recipes; an op script off the closed list, an empty recipe and a bad step are refused naming the file")
    def _():
        root = tmp()
        if load_seeds(root / "seeds" / "g.json") != {}:
            return "absent file read as recipes"
        path = root / "seeds" / "g.json"
        for recipes, needle in (({"r": [{"op": ["rm", "-rf"]}]}, "closed list"), ({"r": []}, "non-empty list"), ({"r": [{"drive_until": {"stage": "S1"}}]}, "drive_until"),
                                ({"r": [{"op": ["story_step.py"], "drive_until": {}}]}, "exactly one")):
            _write(path, {"schema": 1, "group": "g", "recipes": recipes})
            try:
                load_seeds(path)
            except ExitsUnreadable as exc:
                if needle not in str(exc) or "g.json" not in str(exc):
                    return f"{needle}: {exc}"
                continue
            return f"{needle}: no refusal"
        _write(path, {"schema": 1, "group": "g", "recipes": {"r": [{"drive_until": {"stage": "S8", "question": "q"}}, {"op": ["story_step.py", "--task", "{task}"]}]}})
        return None if list(load_seeds(path)) == ["r"] else "a good recipe was refused"

    @case("census: a ledger row that names no walk row and no main stage is an orphan, red; main/ and a written walk row are not")
    def _():
        out = {}
        for rid, expect_red in (("p.key/zzz", True), ("main/S5", False), ("route:r1/a", False)):
            root = tmp()
            ledger = {"known_red": {rid: {"node": "P1B-9", "raised_by": "x"}}, "pins": {"known_red": 1}}
            directory = _tree(root, ledger=ledger)
            walk = {"route:r1/a": {"reach": "seed"}}
            red = []
            _ledger_orphans(directory / "known_red.json", walk, red.append)
            out[rid] = bool(red)
            if bool(red) != expect_red:
                return f"{rid}: red={red}"
        return None

    # ---- answer bytes, the control, the part grammar
    @case("answer bytes: token+newline, words as given, token and words, the file's raw bytes (CRLF and BOM kept), none -> b''")
    def _():
        import dry_world as W
        folder = tmp()
        (folder / "w.txt").write_bytes(b"\xef\xbb\xbfone\r\ntwo")
        rows = [({"token": "go on"}, b"go on\n"), ({"words": "free\ntext"}, b"free\ntext"), ({"token": "agree", "words": "and more"}, b"agree\nand more"),
                ({"words_file": "w.txt"}, b"\xef\xbb\xbfone\r\ntwo"), ({}, b"")]
        for answer, want in rows:
            got = W.answer_bytes({"id": "k/a", "answer": answer}, folder)
            if got != want:
                return f"{answer}: {got!r} != {want!r}"
        try:
            W.answer_bytes({"id": "k/a", "answer": {"words_file": "../w.txt"}}, folder)
        except W.MainPassError as exc:
            return None if "words_file" in str(exc) else f"got {exc}"
        return "a words_file outside the folder was read"

    @case("control: a row `stub` with a conductor lifts it to the control's top level; a row with no stub writes the story's control unchanged")
    def _():
        import dry_world as W
        root = tmp()
        world = W.World({"id": "dry-1", "task": "T", "stub": {"qa-scout": {"verdict": "ok"}}}, root, {}, None, root / "snaps", "dry-1")
        world.control()
        plain = (root / "dry-stub-control.json").read_text(encoding="utf-8")
        want = json.dumps({"task": "T", "story": "dry-1", "stub": {"qa-scout": {"verdict": "ok"}}})
        world.control({"conductor": {"variant": "go on"}, "qa-scout": {"verdict": "bad"}})
        steered = json.loads((root / "dry-stub-control.json").read_text(encoding="utf-8"))
        ok = steered.get("conductor") == {"variant": "go on"} and "conductor" not in steered["stub"] and steered["stub"]["qa-scout"] == {"verdict": "bad"}
        return None if plain == want and ok else f"plain {plain} / steered {steered}"

    @case("parts: main, main:<type>, exits:<group> parse; an empty or malformed group, an unknown group and any other text exit 2 naming the groups")
    def _():
        import test_scenario_dry_1 as S
        root = tmp()
        _write(root / "exits" / "grp.json", {})
        if [S.parse_part(t, root) for t in ("main", "main:x", "exits:grp")] != [("main", "default"), ("main", "x"), ("exits", "grp")]:
            return "a good part was misread"
        for text in ("exits:", "exits:Bad_Name", "exits:nosuch", "walk", "exit:grp"):
            try:
                S.parse_part(text, root)
            except SystemExit as exc:
                if exc.code != 2:
                    return f"{text!r}: exit {exc.code}"
                continue
            return f"{text!r}: no refusal"
        return None

    @case("route spy: returns exactly what the real function returns and records only after a non-None result")
    def _():
        import dry_driver
        sink = tmp() / "state" / "dry-routes.jsonl"
        spy = dry_driver.route_spy(lambda text: ("marked_x", "continue") if "x" in text else None, sink)
        first, second = spy("nothing"), spy("a x b")
        lines = sink.read_text(encoding="utf-8").splitlines() if sink.is_file() else []
        return None if first is None and second == ("marked_x", "continue") and lines == ['{"route": "marked_x"}'] else f"{first} {second} {lines}"

    # ---- drive_main and run_seed with a fake driver
    def fake_world():
        import dry_world as W
        root = tmp()
        world = W.World({"id": "dry-1", "task": "T"}, root, {}, None, root / "snaps", "dry-1")
        world.task_root.mkdir(parents=True)
        (world.task_root / "state").mkdir()
        return W, world

    def put_state(world, kind, stage, n_questions):
        state = world.task_root / "state"
        _write(state / "driver-state.json", {"asked": {"kind": kind, "stage": stage} if kind else {}})
        _write(state / "driver-questions.jsonl", "".join(json.dumps({"kind": kind or "x", "stage": stage}) + "\n" for _ in range(n_questions)))

    @case("drive_main: returns at once, with no driver run, when the stop_after snapshot already exists")
    def _():
        W, world = fake_world()
        (world.snaps / "dry-1" / "S2").mkdir(parents=True)

        def never(*a, **k):
            raise AssertionError("the driver ran")
        got = W.drive_main(world, {}, line=lambda *a: None, stop_after="S2", drive_fn=never)
        return None if got["turns"] == 0 and got["stop"] == "" else f"got {got['turns']} {got['stop']!r}"

    @case("run_seed: the question already pending is reached with zero driver runs (EW12)")
    def _():
        W, world = fake_world()
        put_state(world, "s1_review", "S1", 1)
        runs = []
        got = W.run_seed(world, [{"drive_until": {"stage": "S1", "question": "s1_review"}}], {}, drive_fn=lambda *a, **k: runs.append(a))
        return None if got == (True, "") and not runs else f"got {got} {runs}"

    @case("run_seed: an intermediate question is answered with the story's closed words; one with no words is not reached and named (EW17)")
    def _():
        W, world = fake_world()
        put_state(world, "halt", "S0", 1)

        def turn(w, *args, timeout):
            put_state(w, "s1_review", "S1", 2)
            return W.Run(0, "", 1.0, [])
        step = [{"drive_until": {"stage": "S1", "question": "s1_review"}}]
        got = W.run_seed(world, step, {("S0", "halt"): "go on"}, drive_fn=turn)
        written = (world.root / "answer.md").read_bytes() if (world.root / "answer.md").is_file() else b""
        put_state(world, "halt", "S0", 1)
        none = W.run_seed(world, step, {}, drive_fn=turn)
        return None if got == (True, "") and written == b"go on" and not none[0] and "halt" in none[1] else f"got {got} {written!r} {none}"

    @case("run_seed: the cap AT the value still runs, BEYOND it (cap + 1 s) is not reached; a driver exit with no new question is named")
    def _():
        W, world = fake_world()
        step = [{"drive_until": {"stage": "S1", "question": "s1_review"}}]
        outs = []
        for seconds in (10.0, 11.0):
            put_state(world, "halt", "S0", 1)
            outs.append(W.run_seed(world, step, {("S0", "halt"): "go"}, cap=10,
                                   drive_fn=lambda w, *a, timeout, s=seconds: (put_state(w, "s1_review", "S1", 2), W.Run(0, "", s, []))[1]))
        put_state(world, "halt", "S0", 1)
        stuck = W.run_seed(world, step, {("S0", "halt"): "go"}, drive_fn=lambda w, *a, timeout: W.Run(0, "", 1.0, []))
        return None if outs[0] == (True, "") and not outs[1][0] and "over the cap" in outs[1][1] and not stuck[0] and "no new question" in stuck[1] else f"{outs} {stuck}"

    # ---- judge_row, one row per check and branch
    ask = {"kind": "s1_review", "stage": "S1", "offered": ["agree", "flip"]}
    good = {"seed": {"reached": True}, "ask": ask, "ask_sha": "q1", "priced_at_ask": {"key": "p.key", "answers": ["a", "b"]}, "fp_ask": "x", "fp_after": "y",
            "fp_notes": [], "answer_records": [{"question_sha": "q1"}], "conductor_calls": 0, "conductor_whys": [], "gates": [], "passed_lines": 0, "loop": "",
            "stub_added": [{"run_class": "dry"}], "routes_added": [], "cap": 240}
    jrow = wrow("p.key/a", answer={"token": "agree"}, expect={"checks": ["C2", "C3"]})

    def judged(row=jrow, klass="", **facts):
        return judge_row(row, {**good, **facts}, prices={"p.key": [{"answer": "a"}, {"answer": "b"}, {"answer": "c"}]}, class_of_subject=klass)

    table = [
        ("a row whose checks hold is PASS", {}, "pass", ""),
        ("C2: a token the ask did not offer is FAIL", {"ask": {**ask, "offered": ["flip"]}}, "fail", "was not offered"),
        ("C2: no answer record for the ask is FAIL", {"answer_records": [{"question_sha": "other"}]}, "fail", "no answer"),
        ("C2: an unread_answer conductor call is FAIL", {"conductor_whys": ["unread_answer"]}, "fail", "unread_answer"),
        ("C3: a fingerprint that did not change is FAIL naming the check", {"fp_after": "x"}, "fail", "changed nothing"),
        ("C3: rounds unknown is a NOTE, never PASS (EW19)", {"fp_notes": ["rounds unknown: x"]}, "note", "rounds unknown"),
        ("K15/E17: a priced record of another key is FAIL (EW18)", {"priced_at_ask": {"key": "q.key", "answers": ["a"]}}, "fail", "key not observed: expected p.key, observed q.key"),
        ("K15/E17: no priced record is FAIL", {"priced_at_ask": None}, "fail", "key not observed"),
        ("K15/E17: an offered answer with no price row is FAIL", {"priced_at_ask": {"key": "p.key", "answers": ["a", "zzz"]}}, "fail", "price rows"),
        ("E18: a stub line with run_class '' is FAIL", {"stub_added": [{"run_class": ""}]}, "fail", "run_class"),
        ("EW17: a seed that did not reach is FAIL naming the subject", {"seed": {"reached": False, "detail": "met halt"}}, "fail", "seed did not reach p.key"),
        ("EW23: over the cap is FAIL naming the phase", {"over_cap": "answer turn 1"}, "fail", "over the cap 240 s at answer turn 1"),
        ("EW24: POST_TURNS with no new ask and no loop is FAIL", {"exhausted": True, "post_turns": 4}, "fail", "4 post-answer turns"),
    ]
    for label, facts, kind, needle in table:
        @case(f"judge_row: {label}")
        def _(facts=facts, kind=kind, needle=needle):
            got = judged(**facts)
            return None if got.kind == kind and needle in got.detail else f"got {got}"

    @case("judge_row: C4 passes on a gate subject with a new passed-by-person line, fails without one or off the gate class")
    def _():
        row = wrow("p.key/a", answer={"token": "agree"}, expect={"checks": ["C4"]})
        a, b, c = judged(row, "gate", passed_lines=1), judged(row, "gate"), judged(row, "ban", passed_lines=1)
        return None if (a.kind, b.kind, c.kind) == ("pass", "fail", "fail") else f"got {a} {b} {c}"

    @case("judge_row: C5 follows the loop fact; C6 needs every gate rehearsal true and at least one gate met")
    def _():
        c5 = wrow("p.key/a", expect={"checks": ["C5"]})
        c6 = wrow("p.key/a", expect={"checks": ["C6"]})
        got = [judged(c5).kind, judged(c5, loop="third ask").kind, judged(c6).kind, judged(c6, gates=[{"kind": "gate_A", "ready": True}]).kind,
               judged(c6, gates=[{"kind": "gate_A", "ready": None, "detail": "no json"}]).kind]
        return None if got == ["pass", "fail", "fail", "pass", "fail"] else f"got {got}"

    @case("judge_row: C9 wants a rework_stage option whose args.role is the author; no role counts as missing")
    def _():
        row = wrow("p.key/a", expect={"checks": ["C9"]})
        opts = lambda role: {"options": [{"move": "rework_stage", "args": {"role": role}}] if role else [{"move": "rework_stage"}], "author": "qa-case-designer"}   # noqa: E731
        got = [judged(row, rework=opts("qa-case-designer")).kind, judged(row, rework=opts("qa-scout")).kind, judged(row, rework=opts("")).kind, judged(row).kind]
        return None if got == ["pass", "fail", "fail", "fail"] else f"got {got}"

    @case("judge_row: `empty` is PASS only when the driver refused it and the same ask is still pending")
    def _():
        row = wrow("p.key/empty", answer={}, expect={"checks": ["empty"]})
        pending = {"kind": "s1_review", "stage": "S1"}
        got = [judged(row, empty_refused=True, asked_after=pending).kind, judged(row, empty_refused=False, asked_after=pending).kind,
               judged(row, empty_refused=True, asked_after={}).kind]
        return None if got == ["pass", "fail", "fail"] else f"got {got}"

    @case("judge_row: EW26 a listed C7/C8/C10 is a NOTE `pending judge` naming it, while a failing check among the others is still FAIL")
    def _():
        row = wrow("p.key/a", answer={"token": "agree"}, expect={"checks": ["C2", "C7", "C10"]})
        note, red = judged(row), judged(row, answer_records=[])
        return None if note.kind == "note" and note.tag == "pending_judge" and "C7, C10" in note.detail and red.kind == "fail" else f"got {note} {red}"

    @case("judge_row: a route subject needs its route in the recorded routes (F-W4)")
    def _():
        row = wrow("route:r1/code move", answer={"token": "agree"}, expect={"checks": ["C3"]})
        seen, missing = judged(row, routes_added=["r1"]), judged(row, routes_added=[])
        return None if seen.kind == "pass" and missing.kind == "fail" and "route not observed" in missing.detail else f"got {seen} {missing}"

    # ---- judge_group
    def ledger_file(rows):
        root = tmp()
        return _write(root / "known_red.json", {"known_red": {rid: {"node": node, "raised_by": "x"} for rid, node in rows.items()}, "pins": {"known_red": len(rows)}})

    def group_lines(outcomes, ledger, ids=None):
        return judge_group(outcomes, ledger_file(ledger), ids or [rid for rid, _o in outcomes])

    P, F = Outcome("pass", changed=True), Outcome("fail", "no", changed=False)

    @case("judge_group: a ledger row of another group is not an unknown row; a red row with a ledger row is known red; a green one is stale")
    def _():
        got = group_lines([("p.key/a", F), ("p.key/b", P)], {"p.key/a": "P1B-9", "other/x": "P1B-9", "p.key/b": "P1B-9"})
        text = "\n".join(f"{n} {k} {d}" for n, k, d in got)
        return None if "known red: p.key/a -> P1B-9" in text and "stale: p.key/b" in text and "other/x" not in text else f"got {text}"

    @case("judge_group: a red row with no ledger row is new red")
    def _():
        text = "\n".join(f"{n} {k} {d}" for n, k, d in group_lines([("p.key/a", F)], {}))
        return None if "fail" in text and "new red: p.key/a" in text else f"got {text}"

    @case("judge_group: E15 a ledger row naming the node of the row's own after: label is red")
    def _():
        gone = Outcome("note", "after:P1B-9: x", tag="after", node="P1B-9")
        text = "\n".join(f"{n} {k} {d}" for n, k, d in group_lines([("p.key/a", gone)], {"p.key/a": "P1B-9"}))
        return None if "never expected red for the defect that made it unreachable" in text else f"got {text}"

    @case("judge_group: alive only stop - every variant but stop unchanged is red; one that moved is not")
    def _():
        stop = Outcome("pass", changed=False)
        dead = group_lines([("p.key/a", Outcome("pass", changed=False)), ("p.key/stop", stop)], {})
        live = group_lines([("p.key/a", P), ("p.key/stop", stop)], {})
        return None if any(n == "alive" and "alive only stop" in d for n, _k, d in dead) and not any(n == "alive" for n, _k, _d in live) else f"got {dead} {live}"

    def alive_lines(outcomes, ledger):
        return [(k, d) for n, k, d in group_lines(outcomes, ledger) if n == "alive"]

    stop0 = ("p.key/stop", Outcome("pass", changed=False))

    @case("judge_group: alive - every moving-less variant red AND ledgered is a NOTE naming the row and node, never a fail")
    def _():
        got = alive_lines([("p.key/a", F), ("p.key/b", F), stop0], {"p.key/a": "N4S0-1", "p.key/b": "N4S0-1"})
        return None if len(got) == 1 and got[0][0] == "note" and "known red: p.key/a -> N4S0-1" in got[0][1] and "p.key/b -> N4S0-1" in got[0][1] else f"got {got}"

    @case("judge_group: alive - one ledgered red and one unledgered red variant stays FAIL")
    def _():
        got = alive_lines([("p.key/a", F), ("p.key/b", F), stop0], {"p.key/a": "N4S0-1"})
        return None if [k for k, _d in got] == ["fail"] else f"got {got}"

    @case("judge_group: alive - a ledgered red variant plus a variant that passed yet left the state unchanged stays FAIL")
    def _():
        got = alive_lines([("p.key/a", F), ("p.key/b", Outcome("pass", changed=False)), stop0], {"p.key/a": "N4S0-1"})
        return None if [k for k, _d in got] == ["fail"] else f"got {got}"

    @case("judge_group: alive - no red rows (all passed, state unchanged) is the FAIL of today")
    def _():
        got = alive_lines([("p.key/a", Outcome("pass", changed=False)), stop0], {})
        return None if [k for k, _d in got] == ["fail"] else f"got {got}"

    @case("judge_group: alive - an unreadable ledger file keeps alive FAIL (the ledger problem is printed by its own line)")
    def _():
        bad = tmp() / "known_red.json"
        bad.write_text("{not json", encoding="utf-8")
        got = judge_group([("p.key/a", F), stop0], bad, ["p.key/a", "p.key/stop"])
        return None if any(n == "alive" and k == "fail" for n, k, _d in got) and any(n == "known_red" and k == "fail" for n, k, _d in got) else f"got {got}"

    @case("judge_group: `outcomes` is PASS with the count per kind; a row with two outcomes or none is FAIL")
    def _():
        notes = [("p.key/a", P), ("p.key/b", Outcome("note", "live_only: x", tag="live_only"))]
        ok = [(n, k, d) for n, k, d in group_lines(notes, {}) if n == "outcomes"][0]
        two = [(n, k) for n, k, d in group_lines([("p.key/a", P), ("p.key/a", P)], {}, ["p.key/a"]) if n == "outcomes"][0]
        none = [(n, k) for n, k, d in group_lines([("p.key/a", P)], {}, ["p.key/a", "p.key/b"]) if n == "outcomes"][0]
        return None if ok[1] == "pass" and "1 pass" in ok[2] and "1 live only" in ok[2] and two[1] == "fail" and none[1] == "fail" else f"got {ok} {two} {none}"

    # ---- group_unwalked
    @case("group_unwalked: a key with answers a, b and only `a` written -> b, free words, empty are missing; a census unwalked row counts; no census file is a NOTE")
    def _():
        directory = _tree(tmp())
        census = load(directory)
        count, texts = group_unwalked("g", census, [wrow("p.key/a")], {"p.key": [{"answer": "a"}, {"answer": "b"}]}, routes=uni.routes)
        none = group_unwalked("selftest", census, [], {})
        return (None if count == 7 and "variants without a row 3: p.key/b, p.key/free words, p.key/empty" in texts[0] and "route:r1" in texts[0]
                and none == (0, ["no census file for group selftest: unwalked not counted"]) else f"got {count} {texts} {none}")


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
