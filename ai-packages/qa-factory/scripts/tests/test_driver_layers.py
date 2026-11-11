"""The driver's layer test (t-301 N0): a census of every name the driver defines, and the rules that keep the traffic between
its future modules one-directional (checks L1-L10).

WHY IT IS AN AST TEST ON `self`. The driver is about to be split into modules assembled into one class (mixins), and mixins
never import each other, so an import-direction test is vacuous: the traffic goes through `self.<attr>`, through
`self.state[<key>]`, through ad-hoc attributes of a `Person`, and through `getattr(self, <name chosen at run time>)`. This test
reads the driver set (`scripts/story_run.py` plus every `scripts/driver_*.py`) with `ast` and resolves EVERY such access against
the map `fixtures/driver-layers.json` (FR-44: the map is read by tests only, so it is not under `references/`).

It errs toward refusing: an access it cannot resolve fails; it never passes one. Each check has a bad case, built in a temp
directory below, that must be reported BY NAME (an evergreen layer test is impossible by construction).

    python -B scripts/tests/test_driver_layers.py                 # the checks
    python -B scripts/tests/test_driver_layers.py --draft-missing # one JSON row, `home: null`, per unmapped name (homes are a
                                                                  # judgment by the rules R1-R7 of the t-301 draft; never defaulted)
    python -B scripts/tests/test_driver_layers.py --draft-all     # also the rows the census derives for the other tables

The census counts module-level bindings (def, class, assignments incl. the `HERE` constant) and the members of every class named
`Driver` or `Driver<Suffix>` (methods, static and class methods, class constants), keyed `Driver.<member>` whatever mixin holds
them. Imports, nested functions and the `__main__` block are excluded.
"""

import ast
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness  # noqa: E402
from harness import check, check_eq, finish  # noqa: E402

DRIVER_CLASS = re.compile(r"^Driver[A-Za-z0-9]*$")
MAP_PATH = harness.FIXTURES / "driver-layers.json"
# The golden's own files mention the driver by name on purpose; L8 counts the rig's tests, not the instrument.
# harness.py holds the ONE reader of the driver set (`driver_sources`), which must name story_run.py; it is the instrument too.
L8_SKIP = {"harness.py", "driver_golden.py","driver_trace.py", "test_driver_golden.py", "test_driver_layers.py"}

# The `exceptions` list is SHRINK-ONLY: it may lose rows when a node removes the upward edge, never gain one. These are the rows
# the map held when N0 recorded it (one `from>to>kind` per line). A row in the map that is not here fails L5; a row here that
# the map no longer holds is simply gone (the list shrank).
# t-809 F-2: the four S1 rows moved from `Driver.handoff` to `Driver.s1_person` (the same four edges, extracted so the ladder can run
# the branches again on the set its resume left): four rows out, the same four in - the list did not grow.
PINNED_EXCEPTIONS = """
Driver.__init__>UNTIL_PAST>name
Driver.close_window_series>Driver.window_key>call
Driver.conductor>Driver.boundary_dispatch>call
Driver.conductor_round>Driver.refusal_dispatch>call
Driver.continuation_note>HANDOFF_FORM>name
Driver.finish>Driver.rebuild_report>call
Driver.finish>WINDOW_ROUND_STAGES>name
Driver.handoff>Driver.close_vcs_gaps>call
Driver.s1_person>Driver.s1_gap_text>call
Driver.s1_person>Driver.s1_review_text>call
Driver.s1_person>S1_GAP_RE>name
Driver.s1_person>S1_REVIEW_RE>name
Driver.run_role>Driver.s1_review_text>call
Driver.s0_quote>Driver.QUOTE_LIMIT>call
"""


# --- reading the driver set -----------------------------------------------------------------------------------
def read_modules(root: Path, exempt=()) -> dict:
    """The driver set: story_run.py plus every scripts/driver_*.py that the map does not exempt as `not_driver` (a module
    that merely carries the `driver_` prefix, like `driver_journal.py`, the dashboard's reader of the driver's journal)."""
    return {path.stem: (path, text, ast.parse(text, str(path))) for path, text in harness.driver_sources(root, set(exempt))}


def _targets(node):
    out = []
    for target in (node.targets if isinstance(node, ast.Assign) else [node.target]):
        for n in ast.walk(target):
            if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Store):
                out.append(n.id)
    return out


def definitions(mods: dict) -> dict:
    """{name: [{stem, line, kind}]} for every module-level binding and every member of a Driver class."""
    defs: dict = {}

    def add(name, stem, line, kind):
        defs.setdefault(name, []).append({"stem": stem, "line": line, "kind": kind})

    for stem, (_path, _text, tree) in mods.items():
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                add(node.name, stem, node.lineno, "func")
            elif isinstance(node, ast.ClassDef):
                add(node.name, stem, node.lineno, "class")
                if DRIVER_CLASS.match(node.name):
                    for sub in node.body:
                        if isinstance(sub, (ast.FunctionDef, ast.AsyncFunctionDef)):
                            kind = "method"
                            for deco in sub.decorator_list:
                                if isinstance(deco, ast.Name) and deco.id in ("staticmethod", "classmethod"):
                                    kind = deco.id
                            add("Driver." + sub.name, stem, sub.lineno, kind)
                        elif isinstance(sub, (ast.Assign, ast.AnnAssign)):
                            for name in _targets(sub):
                                add("Driver." + name, stem, sub.lineno, "classconst")
            elif isinstance(node, (ast.Assign, ast.AnnAssign)):
                for name in _targets(node):
                    add(name, stem, node.lineno, "const")
    return defs


# --- one function's traffic -------------------------------------------------------------------------------------
class Scan(ast.NodeVisitor):
    """What one function touches: `self.<attr>`, `getattr(self, ...)`, state keys, Person attributes, module-level names, and
    the forms the test refuses to analyse (an alias of `self` or of `self.state`, `self.__dict__`, `vars(self)`)."""

    def __init__(self, label: str, node, person_names=("person",), driver_member: bool = True):
        self.label, self.node = label, node
        self.driver_member = driver_member
        self.self_use = []          # (attr, ctx 'load'|'store'|'del', line, how)
        self.dynamic_getattr = []   # (expr text, line)
        self.state_keys = []        # (key or None, line)
        self.person_use = []        # (attr, ctx, line)
        self.refused = []           # (message, line)
        self.names = set()
        self.locals = set()
        self.person_names = set(person_names)
        for n in ast.walk(node):
            if isinstance(n, ast.arg):
                self.locals.add(n.arg)
            elif isinstance(n, ast.Name) and isinstance(n.ctx, (ast.Store, ast.Del)):
                self.locals.add(n.id)
            elif isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and n is not node:
                self.locals.add(n.name)
            elif isinstance(n, (ast.Import, ast.ImportFrom)):
                for alias in n.names:
                    self.locals.add((alias.asname or alias.name).split(".")[0])
            elif isinstance(n, ast.ExceptHandler):
                if n.name:
                    self.locals.add(n.name)
                if isinstance(n.type, ast.Name) and n.type.id == "Person" and n.name:
                    self.person_names.add(n.name)
        self.visit(node)

    @staticmethod
    def _is_self(node) -> bool:
        return isinstance(node, ast.Name) and node.id == "self"

    @staticmethod
    def _is_state(node) -> bool:
        return (isinstance(node, ast.Attribute) and node.attr == "state"
                and isinstance(node.value, ast.Name) and node.value.id == "self")

    @staticmethod
    def _ctx(node) -> str:
        return {ast.Load: "load", ast.Store: "store", ast.Del: "del"}.get(type(node.ctx), "load")

    def visit_Attribute(self, node):
        if self._is_self(node.value):
            if node.attr == "__dict__":
                self.refused.append(("`self.__dict__` hides every attribute it touches", node.lineno))
            else:
                self.self_use.append((node.attr, self._ctx(node), node.lineno, "self"))
        elif isinstance(node.value, ast.Name) and DRIVER_CLASS.match(node.value.id):
            # `Driver.<m>` and `DriverCore.<m>` (a mixin) both resolve to the member row `Driver.<m>`; one that does not
            # resolve is refused in L3 below, never passed.
            self.self_use.append((node.attr, "load", node.lineno, "Driver"))
        elif (isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Name) and node.value.func.id == "type"
              and len(node.value.args) == 1 and self._is_self(node.value.args[0])):
            self.self_use.append((node.attr, "load", node.lineno, "type(self)"))
        elif isinstance(node.value, ast.Name) and node.value.id in self.person_names:
            self.person_use.append((node.attr, self._ctx(node), node.lineno))
        self.generic_visit(node)

    def visit_Call(self, node):
        func = node.func
        if isinstance(func, ast.Name) and func.id in ("getattr", "setattr", "hasattr", "delattr") and node.args:
            target = node.args[0]
            if self._is_self(target):
                second = node.args[1] if len(node.args) > 1 else None
                ctx = {"getattr": "load", "hasattr": "load", "setattr": "store", "delattr": "del"}[func.id]
                if isinstance(second, ast.Constant) and isinstance(second.value, str):
                    self.self_use.append((second.value, ctx, node.lineno, func.id))
                else:
                    self.dynamic_getattr.append((ast.unparse(node), node.lineno))
            elif isinstance(target, ast.Name) and target.id in self.person_names and len(node.args) > 1:
                second = node.args[1]
                if isinstance(second, ast.Constant) and isinstance(second.value, str):
                    ctx = {"getattr": "load", "hasattr": "load", "setattr": "store", "delattr": "del"}[func.id]
                    self.person_use.append((second.value, ctx, node.lineno))
        elif isinstance(func, ast.Name) and func.id == "vars" and node.args and self._is_self(node.args[0]):
            self.refused.append(("`vars(self)` hides every attribute it touches", node.lineno))
        elif isinstance(func, ast.Name) and func.id == "once_on" and node.args and self._is_self(node.args[0]):
            # `once_on(self, "<name>", make)` keeps `<name>` on the instance: a touch of that attribute, read like getattr
            second = node.args[1] if len(node.args) > 1 else None
            if isinstance(second, ast.Constant) and isinstance(second.value, str):
                self.self_use.append((second.value, "load", node.lineno, "once_on"))
            else:
                self.refused.append(("`once_on(self, <non-literal>, ...)` hides the attribute it touches", node.lineno))
        if isinstance(func, ast.Attribute) and self._is_state(func.value):
            if func.attr in ("get", "setdefault", "pop", "__contains__", "__getitem__", "__setitem__", "__delitem__"):
                first = node.args[0] if node.args else None
                if isinstance(first, ast.Constant) and isinstance(first.value, str):
                    self.state_keys.append((first.value, node.lineno))
                else:
                    self.state_keys.append((None, node.lineno))
            elif func.attr == "update":
                first = node.args[0] if node.args else None
                if isinstance(first, ast.Dict) and all(isinstance(k, ast.Constant) for k in first.keys):
                    self.state_keys.extend((k.value, node.lineno) for k in first.keys)
                else:
                    self.state_keys.append((None, node.lineno))
        self.generic_visit(node)

    def visit_Subscript(self, node):
        if self._is_state(node.value):
            key = node.slice
            if isinstance(key, ast.Constant) and isinstance(key.value, str):
                self.state_keys.append((key.value, node.lineno))
            else:
                self.state_keys.append((None, node.lineno))
        self.generic_visit(node)

    def visit_Compare(self, node):
        if len(node.ops) == 1 and isinstance(node.ops[0], (ast.In, ast.NotIn)) and self._is_state(node.comparators[0]):
            if isinstance(node.left, ast.Constant) and isinstance(node.left.value, str):
                self.state_keys.append((node.left.value, node.lineno))
            else:
                self.state_keys.append((None, node.lineno))
        self.generic_visit(node)

    def visit_Assign(self, node):
        if self._is_self(node.value):
            self.refused.append(("`x = self` makes an alias, and everything through the alias is invisible", node.lineno))
        elif self._is_state(node.value):
            self.refused.append(("`x = self.state` makes an alias of the state, and its keys are invisible", node.lineno))
        self.generic_visit(node)

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Load) and node.id not in self.locals:
            self.names.add(node.id)


def _driver_classes(tree):
    return [n for n in tree.body if isinstance(n, ast.ClassDef) and DRIVER_CLASS.match(n.name)]


def _python_ids(tree) -> set:
    return {n.name for n in tree.body if isinstance(n, ast.ClassDef) and n.name == "Person"}


def person_defined(mods: dict) -> set:
    """The attribute names the class `Person` itself defines (and the ones every Exception has)."""
    out = set(dir(Exception))
    for _stem, (_p, _t, tree) in mods.items():
        for node in tree.body:
            if isinstance(node, ast.ClassDef) and node.name == "Person":
                for sub in ast.walk(node):
                    if isinstance(sub, ast.Attribute) and isinstance(sub.value, ast.Name) and sub.value.id == "self":
                        out.add(sub.attr)
                for sub in node.body:
                    if isinstance(sub, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        out.add(sub.name)
    return out


def scans(mods: dict) -> list:
    """[(label, stem, Scan)] for every Driver member function, every module-level function and every method of the other
    classes (labelled by the class)."""
    out = []
    for stem, (_path, _text, tree) in mods.items():
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                out.append((node.name, stem, Scan(node.name, node, driver_member=False)))
            elif isinstance(node, ast.ClassDef):
                is_driver = bool(DRIVER_CLASS.match(node.name))
                for sub in node.body:
                    if isinstance(sub, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        label = "Driver." + sub.name if is_driver else node.name
                        out.append((label, stem, Scan(label, sub, driver_member=is_driver)))
    return out


# --- the checks ---------------------------------------------------------------------------------------------------
def rank_of(mp: dict) -> dict:
    return {module: i for i, group in enumerate(mp.get("layers", [])) for module in group}


def analyse(root: Path, mp: dict, tests_dir: Path | None = None) -> dict:
    """{check id: [problem text]} plus `info` (counts). Every problem names the thing, what was expected, and the door."""
    exempt = {row["module"] for row in mp.get("not_driver", [])}
    mods = read_modules(root, exempt)
    defs = definitions(mods)
    probs = {k: [] for k in ("L1", "L2", "L3", "L4", "L5", "L6", "L7", "L8", "L9", "L10")}
    rank = rank_of(mp)
    for path in sorted((root / "scripts").glob("driver_*.py")):
        if path.stem not in rank and path.stem not in exempt:
            probs["L1"].append(f"scripts/{path.name} is a driver_* module with no layer: add `{path.stem}` to `layers` of "
                               f"driver-layers.json (a driver module outside the map is invisible to the golden's stdout "
                               f"filter), or to `not_driver` with a reason if it is not part of the driver.")
    for row in mp.get("not_driver", []):
        if not str(row.get("reason") or "").strip():
            probs["L10"].append(f"not_driver row {row.get('module')!r} has no reason: say why it is not part of the driver.")
    rows = {}
    for row in mp.get("names", []):
        if row["name"] in rows:
            probs["L10"].append(f"driver-layers.json has two rows for `{row['name']}`: a name has one row; delete one.")
        rows[row["name"]] = row
    homes = {name: row.get("home") for name, row in rows.items()}
    modules_present = set(mods)

    # L10 well-formed
    for name, row in rows.items():
        if not row.get("home"):
            probs["L10"].append(f"row `{name}` has no home; homes are a judgment (rules R1-R7 of the t-301 draft), never "
                                f"defaulted: choose one of {sorted(rank)}.")
        elif row["home"] not in rank:
            probs["L10"].append(f"row `{name}` names the home `{row['home']}`, which is not in `layers` {sorted(rank)}: "
                                f"expected a module of the layer list.")
    for table, key in (("attributes", "name"), ("state_keys", "key")):
        seen = set()
        for row in mp.get(table, []):
            if row[key] in seen:
                probs["L10"].append(f"`{table}` has two rows for `{row[key]}`: delete one.")
            seen.add(row[key])
            if row.get("owner") not in rank:
                probs["L10"].append(f"`{table}` row `{row[key]}` has owner {row.get('owner')!r}, not a module of `layers`: "
                                    f"expected one of {sorted(rank)}.")
    for row in mp.get("exceptions", []):
        if not str(row.get("reason") or "").strip():
            probs["L10"].append(f"exceptions row {row.get('from')} -> {row.get('to')} has no reason: say why the upward "
                                f"edge exists and which node removes it.")

    # L1 census, both directions; L2 single definition and placement
    for name, found in sorted(defs.items()):
        first = found[0]
        place = f"{mods[first['stem']][0].name}:{first['line']}"
        if name not in rows:
            kind_hint = first["kind"]
            probs["L1"].append(
                f"{place} defines `{name}`; driver-layers.json has no row for it. Add "
                f"{{\"name\": \"{name}\", \"kind\": \"{kind_hint}\", \"home\": <module>}}, choosing the home by the assignment "
                f"rules R1-R7 (t-301 draft section 3).")
        elif rows[name].get("kind") != first["kind"]:
            probs["L1"].append(f"{place}: `{name}` is a {first['kind']} but its row says {rows[name].get('kind')!r}: "
                               f"fix the row's kind.")
        if len(found) > 1:
            where = ", ".join(f"{mods[f['stem']][0].name}:{f['line']}" for f in found)
            probs["L2"].append(f"`{name}` is defined {len(found)} times ({where}): a name has one home.")
        elif name in rows and rows[name].get("home") in rank:
            home = rows[name]["home"]
            if home in modules_present and home != first["stem"]:
                probs["L2"].append(f"{place} defines `{name}` but its home {home} exists and is the place for it "
                                   f"({mods[home][0].name}): move it there, or change the row's home.")
            if home not in modules_present and first["stem"] != "story_run":
                probs["L2"].append(f"{place} defines `{name}` with home {home}, a module that does not exist: expected the "
                                   f"definition in story_run.py until {home}.py is made.")
    for name in sorted(rows):
        if name not in defs:
            probs["L1"].append(f"row `{name}` names nothing in the driver: delete it, or rename it if the function was "
                               f"renamed.")

    # L3 .. L7 over the scans
    members = {n.split(".", 1)[1] for n in defs if n.startswith("Driver.")}
    attrs = {row["name"]: row for row in mp.get("attributes", [])}
    state_rows = {row["key"]: row for row in mp.get("state_keys", [])}
    dyn_rows = {row["function"]: row for row in mp.get("dynamic_state_keys", [])}
    sd_rows = [row for row in mp.get("string_dispatch", [])]
    adhoc_rows = {(row["on"], row["name"]): row for row in mp.get("adhoc_attributes", [])}
    all_scans = scans(mods)
    person_attrs = person_defined(mods)
    attr_seen: dict = {}
    attr_init: dict = {}
    state_seen: dict = {}
    dyn_sites: dict = {}
    dispatch_sites: dict = {}
    adhoc_seen: dict = {}
    edges = set()
    where = {stem: mods[stem][0].name for stem in mods}
    for label, stem, scan in all_scans:
        site = where[stem]
        caller_home = homes.get(label) if label in rows else None
        for message, line in scan.refused:
            probs["L3"].append(f"{site}:{line} in `{label}`: {message}. Expected plain `self.<name>` accesses; rewrite "
                               f"the line so the access is visible to the map.")
        for attr, ctx, line, how in scan.self_use:
            if not scan.driver_member and how == "self":
                continue
            if attr in members:
                target = "Driver." + attr
                edges.add((label, target, "call", caller_home, homes.get(target), f"{site}:{line}"))
                continue
            if attr.startswith("__") and attr.endswith("__"):
                continue
            if how in ("Driver", "type(self)"):
                probs["L3"].append(f"{site}:{line} in `{label}` reads `{how}.{attr}`; `{attr}` is not a member of the Driver "
                                   f"class. Expected a member in the census.")
                continue
            attr_seen.setdefault(attr, []).append((label, f"{site}:{line}"))
            if label == "Driver.__init__" and ctx == "store":
                attr_init[attr] = True
            if attr not in attrs:
                verb = {"load": "reads", "store": "writes", "del": "deletes"}[ctx]
                probs["L3"].append(
                    f"{site}:{line} in `{label}` {verb} `self.{attr}`; nothing owns `{attr}` (not a member, not in "
                    f"`attributes`). Add {{\"name\": \"{attr}\", \"owner\": <the lowest module that touches it>}}.")
            else:
                owner = attrs[attr].get("owner")
                edges.add((label, "attribute:" + attr, "attr", caller_home, owner, f"{site}:{line}"))
        for expr, line in scan.dynamic_getattr:
            dispatch_sites.setdefault(label, []).append((expr, line))
        for key, line in scan.state_keys:
            if key is None:
                dyn_sites.setdefault(label, []).append(line)
            else:
                state_seen.setdefault(key, []).append((label, f"{site}:{line}"))
                if key in state_rows:
                    edges.add((label, "state:" + key, "state", caller_home, state_rows[key].get("owner"), f"{site}:{line}"))
        for attr, ctx, line in scan.person_use:
            if attr in person_attrs:
                continue
            role = "writers" if ctx in ("store", "del") else "readers"
            adhoc_seen.setdefault(attr, {"writers": set(), "readers": set()})[role].add(label)
        if label in rows or label.startswith("Driver."):
            for name in sorted(scan.names):
                if name in rows and name != label and name != "Driver" and not name.startswith("Driver."):
                    edges.add((label, name, "name", caller_home, homes.get(name), f"{site}"))

    # L3 closing: dispatch tables, stale rows, attributes both directions
    module_literals = {}
    for stem, (_p, _t, tree) in mods.items():
        for node in tree.body:
            if isinstance(node, ast.Assign):
                for name in _targets(node):
                    try:
                        module_literals[name] = ast.literal_eval(node.value)
                    except (ValueError, SyntaxError):
                        pass
    rows_by_function = {}
    for row in sd_rows:
        if "function" in row:
            rows_by_function.setdefault(row["function"], []).append(row)
    for function, sites in sorted(dispatch_sites.items()):
        if function not in rows_by_function:
            expr, line = sites[0]
            probs["L3"].append(f"{where.get('story_run', 'story_run.py')}:{line} in `{function}` calls `{expr}`, a name "
                               f"chosen at run time; add a `string_dispatch` row for `{function}` listing every name it can "
                               f"take.")
    for function, found_rows in sorted(rows_by_function.items()):
        if function not in dispatch_sites:
            probs["L3"].append(f"string_dispatch row for `{function}` matches no getattr(self, <non-literal>) in it: delete "
                               f"the row.")
        for row in found_rows:
            names = list(row.get("candidates") or [])
            for part in re.findall(r"(\w+)\[(\d+)\]", row.get("candidates_from", "")):
                table, column = part[0], int(part[1])
                if table not in module_literals:
                    probs["L3"].append(f"string_dispatch row for `{function}` reads {table}[{column}], and {table} is not "
                                       f"a module-level literal: expected a literal table the test can read.")
                    continue
                names.extend("Driver." + entry[column] for entry in module_literals[table])
            for cand in names:
                if cand not in defs:
                    probs["L3"].append(f"string_dispatch row for `{function}` lists `{cand}`, which is not defined: "
                                       f"delete it from the row, or define it.")
                else:                                       # a name chosen at run time is still a call: it has a direction
                    edges.add((function, cand, "call", homes.get(function), homes.get(cand), f"{where.get('story_run', '')}"))
    for row in sd_rows:
        if "function" not in row and not row.get("planned"):
            probs["L10"].append(f"string_dispatch row {row.get('name')!r} names no function and is not `planned`: "
                                f"expected a function, or planned: <node>.")
    for attr in sorted(attrs):
        if attr not in attr_seen:
            probs["L3"].append(f"`attributes` row `{attr}` is not touched through `self` anywhere: delete it, or rename it "
                               f"if the attribute was renamed.")
        elif bool(attrs[attr].get("set_in_init")) != bool(attr_init.get(attr)):
            probs["L3"].append(f"`attributes` row `{attr}` says set_in_init={bool(attrs[attr].get('set_in_init'))}, but "
                               f"Driver.__init__ {'does' if attr_init.get(attr) else 'does not'} assign it: fix the row "
                               f"(an attribute absent from __init__ is a hazard the row names).")

    # L4 ad-hoc attributes and state keys
    for attr, roles in sorted(adhoc_seen.items()):
        row = adhoc_rows.get(("Person", attr))
        if row is None:
            probs["L4"].append(
                f"`person.{attr}` is used (writers {sorted(roles['writers'])}, readers {sorted(roles['readers'])}) but "
                f"Person does not define it and `adhoc_attributes` has no row: add {{\"on\": \"Person\", \"name\": "
                f"\"{attr}\", \"writers\": [...], \"readers\": [...]}}.")
        else:
            if set(row.get("writers", [])) != roles["writers"] or set(row.get("readers", [])) != roles["readers"]:
                probs["L4"].append(f"adhoc attribute `Person.{attr}`: the row says writers {sorted(row.get('writers', []))} "
                                   f"readers {sorted(row.get('readers', []))}, the source says writers "
                                   f"{sorted(roles['writers'])} readers {sorted(roles['readers'])}: update the row.")
    for (on, attr), row in sorted(adhoc_rows.items()):
        if attr not in adhoc_seen:
            probs["L4"].append(f"`adhoc_attributes` row `{on}.{attr}` is used nowhere: delete it.")
    dyn_keys = set()
    for function, row in dyn_rows.items():
        dyn_keys.update(row.get("keys", []))
        if function not in dyn_sites:
            probs["L4"].append(f"`dynamic_state_keys` row for `{function}` matches no non-literal state key site in it: "
                               f"delete the row.")
    for function, lines in sorted(dyn_sites.items()):
        if function not in dyn_rows:
            probs["L4"].append(f"{where.get('story_run', 'story_run.py')}:{lines[0]} in `{function}` uses a state key chosen "
                               f"at run time; add a `dynamic_state_keys` row for it listing every key it can take.")
    for key, seen_at in sorted(state_seen.items()):
        if key not in state_rows:
            label, place = seen_at[0]
            probs["L4"].append(f"{place} in `{label}` uses state key `{key}`; `state_keys` has no row: add "
                               f"{{\"key\": \"{key}\", \"owner\": <the lowest module that touches it>}}.")
    for key in sorted(state_rows):
        if key not in state_seen and key not in dyn_keys:
            probs["L4"].append(f"`state_keys` row `{key}` is used nowhere in the driver: delete it, or rename it if the key "
                               f"was renamed.")

    # L5 / L7 direction against the exceptions list
    exc = {(r.get("from"), r.get("to"), r.get("kind")) for r in mp.get("exceptions", [])}
    upward = set()
    collapsed = {}
    for caller, target, kind, caller_home, target_home, place in sorted(edges):
        collapsed.setdefault((caller, target, kind), (caller_home, target_home, place))
    for (caller, target, kind), (caller_home, target_home, place) in sorted(collapsed.items()):
        if caller_home not in rank or target_home not in rank:
            continue
        if rank[target_home] > rank[caller_home]:
            upward.add((caller, target, kind))
            if (caller, target, kind) in exc:
                continue
            what = {"call": "calls", "attr": "touches the attribute", "state": "touches the state key", "name": "uses"}[kind]
            if kind in ("attr", "state"):
                probs["L7"].append(
                    f"{place}: `{caller}` ({caller_home}) {what} `{target.split(':', 1)[-1]}` owned by {target_home}: its "
                    f"owner must be at or below every accessor's home. Move the ownership down, or add it to `exceptions` "
                    f"with a reason; the list only shrinks.")
            else:
                probs["L5"].append(
                    f"{place}: `{caller}` ({caller_home}) {what} `{target}` ({target_home}), a higher layer: a lower layer "
                    f"may not call a higher one. Move the call behind a hook (node N4), or add it to `exceptions` with a "
                    f"reason; the list only shrinks.")
    for row in mp.get("exceptions", []):
        key = (row.get("from"), row.get("to"), row.get("kind"))
        if key not in upward:
            probs["L5"].append(f"exceptions row {key[0]} -> {key[1]} ({key[2]}) no longer occurs as an upward edge: delete "
                               f"the row (the list is shrink-only).")
    pinned = {line.strip() for line in PINNED_EXCEPTIONS.strip().split("\n") if line.strip()}
    for row in mp.get("exceptions", []):
        label = f"{row.get('from')}>{row.get('to')}>{row.get('kind')}"
        if label not in pinned:
            probs["L5"].append(f"exceptions row {label} is new: the list is pinned and shrink-only, so an upward edge is "
                               f"never added by an exception. Remove the edge instead (hook, port, or move the name).")

    # L6 import direction
    for stem, (path, _text, tree) in mods.items():
        if stem not in rank:
            continue
        for node in ast.walk(tree):
            imported = []
            if isinstance(node, ast.Import):
                imported = [a.name.split(".")[0] for a in node.names]
            elif isinstance(node, ast.ImportFrom) and node.module and not node.level:
                imported = [node.module.split(".")[0]]
            for module in imported:
                if module in rank and rank[module] > rank[stem]:
                    probs["L6"].append(f"{path.name}:{node.lineno} imports {module}, a higher layer: a lower module never "
                                       f"imports a higher one. Move the shared name down, or pass it in.")

    # L8 source readers: every occurrence of the literal driver file name in the rig's tests
    tests = tests_dir if tests_dir is not None else root / "scripts" / "tests"
    # Every file name of the driver set is a literal L8 counts. TEMPORAL RULE: a row of the map carries no driver file name of
    # its own, so a name other than story_run.py is ENFORCED only once some `source_readers`/`source_mentions` row mentions it
    # (in its targets or note); before the map gains such rows its hits are only collected in `l8_extra` and printed as an
    # informational line, after it they are counted like story_run.py's.
    driver_files = [mods[stem][0].name for stem in mods]
    row_text = json.dumps(mp.get("source_readers", [])) + json.dumps(mp.get("source_mentions", []))
    enforced = [n for n in driver_files if n == "story_run.py" or n in row_text]
    census_l8 = {}
    l8_extra = {}
    if tests.is_dir():
        for path in sorted(tests.glob("*.py")):
            if path.name in L8_SKIP:
                continue
            try:
                tree = ast.parse(path.read_text(encoding="utf-8"))
            except SyntaxError:
                continue
            for fname in driver_files:
                for function, line, count in _literal_mentions(tree, fname):
                    if fname in enforced:
                        census_l8.setdefault((path.name, function), []).append((line, count))
                    else:
                        l8_extra.setdefault(fname, []).append(f"{path.name}:{line}")
    readers = {(r["file"], r["function"]): r for r in mp.get("source_readers", [])}
    mentions = {}
    for r in mp.get("source_mentions", []):
        mentions[(r["file"], r.get("function", ""))] = r
    per_file = {}
    for (file, function), found in census_l8.items():
        per_file.setdefault(file, 0)
        per_file[file] += sum(c for _l, c in found)
    for (file, function), found in sorted(census_l8.items()):
        total = sum(c for _l, c in found)
        key = (file, function)
        declared = 0
        if key in readers:
            declared += readers[key].get("count", 0)
        if key in mentions:
            declared += mentions[key].get("count", 0)
        if declared != total:
            first_line = found[0][0]
            kind = "reads the driver's source" if key not in mentions else "mentions the driver"
            probs["L8"].append(
                f"{file}:{first_line}, in `{function}`, {kind} ({total} occurrence(s) of a driver file name literal) and the "
                f"map declares {declared}: add or fix a row in `source_readers` (a source-text read, with the names it pins, "
                f"so the node that moves them owns this test, t-301 section 0b F3) or in `source_mentions` (command text).")
    for (file, function), row in sorted({**readers, **mentions}.items()):
        if (file, function) not in census_l8:
            probs["L8"].append(f"the map has a row for {file} in `{function}` but that function holds no literal story_run.py: "
                               f"delete the row.")
    for (file, function), row in sorted(readers.items()):
        path = tests / file
        if path.is_file():
            tree = ast.parse(path.read_text(encoding="utf-8"))
            if not _function_reads(tree, function):
                probs["L8"].append(f"source_readers row {file}::{function} names a function with no read_text/read_bytes: "
                                   f"a row for command text belongs in `source_mentions`.")

    # L9 stdout writers
    allowed = {(w["file"], w.get("function", "")) for w in mp.get("stdout_writers", [])}
    for stem, (path, _text, tree) in mods.items():
        for label, line, what in _stdout_writes(tree):
            if (path.name, label) not in allowed:
                probs["L9"].append(f"{path.name}:{line} in `{label}` {what}; the golden records driver output through print() "
                                   f"only, so this line is invisible to it. Use print(), or add the site to `stdout_writers`.")
    for row in mp.get("stdout_writers", []):
        pass
    info = {"names": len(defs), "files": sorted(where.values()), "members": len(members), "attributes": len(attr_seen),
            "state_keys": len(state_seen), "dynamic_state_sites": len(dyn_sites),
            "adhoc": len(adhoc_seen), "edges": len(edges), "upward": len(upward), "l8_sites": sum(
                len(v) for v in census_l8.values()),
            "state_seen": sorted(state_seen), "state_users": {k: sorted({l for l, _ in v}) for k, v in state_seen.items()},
            "attr_seen": {a: sorted({l for l, _ in v}) for a, v in attr_seen.items()},
            "adhoc_seen": {a: {r: sorted(s) for r, s in roles.items()} for a, roles in adhoc_seen.items()},
            "upward_edges": sorted(upward), "defs": defs, "dyn_sites": dyn_sites,
            "dispatch_sites": {k: [e for e, _ in v] for k, v in dispatch_sites.items()}, "census_l8": census_l8,
            "attr_init": attr_init, "l8_extra": l8_extra}
    return {"problems": probs, "info": info}


def _literal_mentions(tree, needle: str):
    """[(enclosing def name, line, occurrences)] for each non-docstring string constant that holds `needle`."""
    docstrings = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            body = node.body
            if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant) and isinstance(
                    body[0].value.value, str):
                docstrings.add(id(body[0].value))
    out = []

    def walk(node, function):
        for child in ast.iter_child_nodes(node):
            fn = function
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                fn = child.name
            if isinstance(child, ast.Constant) and isinstance(child.value, str) and id(child) not in docstrings:
                if needle in child.value:
                    out.append((fn, child.lineno, child.value.count(needle)))
            walk(child, fn)
    walk(tree, "<module>")
    return out


def _function_reads(tree, function: str) -> bool:
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == function:
            for sub in ast.walk(node):
                if isinstance(sub, ast.Attribute) and sub.attr in ("read_text", "read_bytes"):
                    return True
                if isinstance(sub, ast.Name) and sub.id == "open":
                    return True
    return False


def _stdout_writes(tree):
    out = []

    def walk(node, label):
        for child in ast.iter_child_nodes(node):
            lab = label
            if isinstance(child, ast.ClassDef):
                lab = "Driver." if DRIVER_CLASS.match(child.name) else child.name + "."
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                lab = (label + child.name) if label.endswith(".") else child.name
            if isinstance(child, ast.Call):
                func = child.func
                if (isinstance(func, ast.Attribute) and func.attr == "write" and isinstance(func.value, ast.Attribute)
                        and func.value.attr in ("stdout", "stderr") and isinstance(func.value.value, ast.Name)
                        and func.value.value.id == "sys"):
                    out.append((lab, child.lineno, f"writes to sys.{func.value.attr} directly"))
                if isinstance(func, ast.Name) and func.id == "print":
                    for kw in child.keywords:
                        if kw.arg == "file" and not (isinstance(kw.value, ast.Attribute) and kw.value.attr in (
                                "stdout", "stderr") and isinstance(kw.value.value, ast.Name) and kw.value.value.id == "sys"):
                            out.append((lab, child.lineno, "prints to a stream other than sys.stdout/sys.stderr"))
            walk(child, lab)
    walk(tree, "")
    return out


# --- drafting -------------------------------------------------------------------------------------------------
def draft_rows(result: dict, mp: dict) -> dict:
    info = result["info"]
    rows = {n["name"] for n in mp.get("names", [])}
    missing = []
    for name, found in sorted(info["defs"].items(), key=lambda kv: kv[1][0]["line"]):
        if name not in rows:
            missing.append({"name": name, "kind": found[0]["kind"], "home": None, "row": None, "note": ""})
    return {"names": missing}


# --- the test ---------------------------------------------------------------------------------------------------
def _write(root: Path, rel: str, text: str) -> None:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


BASE_SOURCE = '''HERE = 1


class Person(Exception):
    def __init__(self):
        self.kind = "x"


class Driver:
    K = 1

    def __init__(self):
        self.state = {}
        self.boundary = "start"

    def top(self):
        self.low()
        self.boundary = "top"
        return self.state.get("k")

    def low(self):
        person = Person()
        person.stage = "S1"
        return HERE
'''

BASE_MAP = {
    "schema": 1,
    "layers": [["driver_core"], ["driver_dialog"], ["story_run"]],
    "names": [
        {"name": "HERE", "kind": "const", "home": "driver_core"},
        {"name": "Person", "kind": "class", "home": "driver_core"},
        {"name": "Driver", "kind": "class", "home": "story_run"},
        {"name": "Driver.K", "kind": "classconst", "home": "driver_core"},
        {"name": "Driver.__init__", "kind": "method", "home": "driver_core"},
        {"name": "Driver.top", "kind": "method", "home": "driver_dialog"},
        {"name": "Driver.low", "kind": "method", "home": "driver_core"},
    ],
    "attributes": [{"name": "state", "owner": "driver_core", "set_in_init": True},
                   {"name": "boundary", "owner": "driver_core", "set_in_init": True}],
    "adhoc_attributes": [{"on": "Person", "name": "stage", "writers": ["Driver.low"], "readers": []}],
    "state_keys": [{"key": "k", "owner": "driver_core"}],
    "dynamic_state_keys": [],
    "string_dispatch": [],
    "exceptions": [],
    "source_readers": [],
    "source_mentions": [],
    "stdout_writers": [],
}


def fixture(source=BASE_SOURCE, mp=None, extra_files=None, tests_files=None):
    """A temp package root holding `source` as story_run.py, and the map; returns (root, map)."""
    root = harness.temp_dir("qa-layers-")
    _write(root, "scripts/story_run.py", source)
    for rel, text in (extra_files or {}).items():
        _write(root, rel, text)
    for rel, text in (tests_files or {}).items():
        _write(root, "scripts/tests/" + rel, text)
    return root, json.loads(json.dumps(mp if mp is not None else BASE_MAP))


def problems_of(case: str, check_id: str, source=BASE_SOURCE, mp=None, extra_files=None, tests_files=None, edit=None):
    root, the_map = fixture(source, mp, extra_files, tests_files)
    try:
        if edit:
            edit(the_map)
        return analyse(root, the_map)["problems"][check_id]
    finally:
        harness.cleanup(root)


def expect(name: str, check_id: str, needle: str, **kw) -> None:
    found = problems_of(name, check_id, **kw)
    check(f"{name}: {check_id} reports it by name ({needle!r})", any(needle in p for p in found),
          f"expected a {check_id} problem containing {needle!r}; got {found}")


def bad_fixtures() -> None:
    root, the_map = fixture()
    try:
        base = analyse(root, the_map)["problems"]
        check_eq("the base fixture is clean (no problem in any check)", {k: v for k, v in base.items() if v}, {})
    finally:
        harness.cleanup(root)

    expect("L1 a def with no row", "L1", "has no row for it", source=BASE_SOURCE + "\n\ndef extra():\n    return 1\n")
    expect("L1 a row with no def", "L1", "names nothing in the driver",
           edit=lambda m: m["names"].append({"name": "ghost", "kind": "func", "home": "driver_core"}))
    expect("L1 a wrong kind", "L1", "fix the row's kind",
           edit=lambda m: m["names"][0].update(kind="func"))
    expect("L2 one name defined twice", "L2", "defined 2 times",
           source=BASE_SOURCE + "\n\ndef HERE():\n    return 2\n")
    expect("L2 a name defined outside its existing home module", "L2", "move it there",
           extra_files={"scripts/driver_core.py": "FILLER = 1\n"},
           edit=lambda m: m["names"].append({"name": "FILLER", "kind": "const", "home": "driver_dialog"}))
    expect("L3 a read of an unowned attribute", "L3", "nothing owns `ghost_attr`",
           source=BASE_SOURCE.replace("self.low()", "self.ghost_attr\n        self.low()"))
    expect("L3 setattr(self, 'x', v)", "L3", "nothing owns `x`",
           source=BASE_SOURCE.replace("self.low()", "setattr(self, 'x', 1)\n        self.low()"))
    expect("L3 del self.x", "L3", "deletes `self.zz`",
           source=BASE_SOURCE.replace("self.low()", "del self.zz\n        self.low()"))
    expect("L3 a non-literal getattr without a row", "L3", "chosen at run time",
           source=BASE_SOURCE.replace("self.low()", "getattr(self, 'low' + str(1))()"))
    expect("L3 self.__dict__", "L3", "`self.__dict__`", source=BASE_SOURCE.replace("self.low()", "self.__dict__\n        self.low()"))
    expect("L3 once_on(self, 'x', make) is a touch of `x`", "L3", "nothing owns `hidden_lock`",
           source=BASE_SOURCE.replace("self.low()", "once_on(self, 'hidden_lock', dict)\n        self.low()"))
    expect("L3 once_on(self, <non-literal>, make)", "L3", "`once_on(self, <non-literal>, ...)`",
           source=BASE_SOURCE.replace("self.low()", "once_on(self, str(1), dict)\n        self.low()"))
    expect("L3 vars(self)", "L3", "`vars(self)`", source=BASE_SOURCE.replace("self.low()", "vars(self)\n        self.low()"))
    expect("L3 me = self", "L3", "makes an alias", source=BASE_SOURCE.replace("self.low()", "me = self\n        self.low()"))
    expect("L3 a lambda closing over self", "L3", "nothing owns `lam`",
           source=BASE_SOURCE.replace("self.low()", "fn = lambda: self.lam\n        self.low()"))
    expect("L3 self.flags.x resolves `flags` only", "L3", "nothing owns `flags`",
           source=BASE_SOURCE.replace("self.low()", "self.flags.x\n        self.low()"))
    expect("L3 Driver.X", "L3", "not a member of the Driver class", source=BASE_SOURCE.replace("self.low()", "Driver.X\n        self.low()"))
    expect("L3 DriverX.nope (a class-name access that does not resolve)", "L3", "not a member of the Driver class",
           source=BASE_SOURCE.replace("self.low()", "DriverX.nope\n        self.low()"))
    resolved = problems_of("L3 DriverCore.K", "L3", source=BASE_SOURCE.replace("self.low()", "DriverCore.K\n        self.low()"))
    check_eq("L3 DriverCore.K resolves to the member row Driver.K (no problem)", resolved, [])
    expect("L3 type(self).X", "L3", "not a member of the Driver class",
           source=BASE_SOURCE.replace("self.low()", "type(self).Y\n        self.low()"))
    expect("L3 functools.partial(self.m)", "L3", "nothing owns `m`",
           source=BASE_SOURCE.replace("self.low()", "functools.partial(self.m)\n        self.low()"))
    expect("L3 a stale attributes row", "L3", "is not touched through `self` anywhere",
           edit=lambda m: m["attributes"].append({"name": "stale", "owner": "driver_core", "set_in_init": False}))
    expect("L3 a stale string_dispatch row", "L3", "matches no getattr(self, <non-literal>)",
           edit=lambda m: m["string_dispatch"].append({"function": "Driver.low", "expr": "x", "candidates": ["Driver.top"]}))
    expect("L3 a dispatch candidate that does not exist", "L3", "which is not defined",
           source=BASE_SOURCE.replace("self.low()", "getattr(self, 'a' + 'b')()"),
           edit=lambda m: m["string_dispatch"].append({"function": "Driver.top", "expr": "x", "candidates": ["Driver.nope"]}))
    expect("L3 set_in_init says the wrong thing", "L3", "set_in_init",
           edit=lambda m: m["attributes"][1].update(set_in_init=False))
    expect("L4 a state key with no row", "L4", "uses state key `newkey`",
           source=BASE_SOURCE.replace("self.low()", "self.state['newkey'] = 1\n        self.low()"))
    expect("L4 a stale state key row", "L4", "is used nowhere",
           edit=lambda m: m["state_keys"].append({"key": "gone", "owner": "driver_core"}))
    expect("L4 a state key chosen at run time", "L4", "chosen at run time",
           source=BASE_SOURCE.replace("self.low()", "self.state[str(1)] = 1\n        self.low()"))
    expect("L4 x = self.state", "L3", "alias of the state",
           source=BASE_SOURCE.replace("self.low()", "s = self.state\n        self.low()"))
    expect("L4 a Person attribute with no row", "L4", "`person.extra` is used",
           source=BASE_SOURCE.replace('person.stage = "S1"', 'person.stage = "S1"\n        person.extra = 1'))
    expect("L4 a stale adhoc row", "L4", "is used nowhere",
           edit=lambda m: m["adhoc_attributes"].append({"on": "Person", "name": "old", "writers": [], "readers": []}))
    up = BASE_SOURCE.replace("        return HERE\n", "        return self.top()\n")
    expect("L5 a lower layer calls a higher one", "L5", "a lower layer may not call a higher one", source=up)
    root, the_map = fixture(up)
    try:
        the_map["exceptions"].append({"from": "Driver.low", "to": "Driver.top", "kind": "call", "reason": "residue"})
        clean = analyse(root, the_map)["problems"]["L5"]
        check_eq("L5 the same edge listed in `exceptions` passes", [p for p in clean if "may not call" in p], [])
    finally:
        harness.cleanup(root)
    expect("L5 a stale exceptions row", "L5", "no longer occurs",
           edit=lambda m: m["exceptions"].append({"from": "Driver.top", "to": "Driver.low", "kind": "call", "reason": "r"}))
    expect("L7 an owner above its accessor", "L7", "must be at or below",
           edit=lambda m: m["attributes"][1].update(owner="driver_dialog"),
           source=BASE_SOURCE.replace("        self.boundary = \"start\"\n", "        self.boundary = \"start\"\n        self.low()\n"))
    expect("L6 an upward import", "L6", "imports driver_dialog, a higher layer",
           extra_files={"scripts/driver_core.py": "import driver_dialog\n", "scripts/driver_dialog.py": "X = 1\n"},
           edit=lambda m: m["names"].extend([{"name": "X", "kind": "const", "home": "driver_dialog"}]))
    expect("L8 a source read with no row", "L8", "reads the driver's source",
           tests_files={"test_x.py": 'from pathlib import Path\n\n\ndef reader():\n    return Path("scripts/story_run.py").read_text()\n'})
    expect("L8 a source_readers row for a function that reads nothing", "L8", "belongs in `source_mentions`",
           tests_files={"test_x.py": 'def reader():\n    return "run story_run.py now"\n'},
           edit=lambda m: m["source_readers"].append({"file": "test_x.py", "function": "reader", "count": 1, "targets": []}))
    expect("L8 a driver_x.py literal with a row that names the file", "L8", "test_x.py:6",
           extra_files={"scripts/driver_x.py": "X = 1\n"},
           tests_files={"test_x.py": 'def other():\n    return "driver_x.py"\n\n\ndef reader():\n    return "run driver_x.py now"\n'},
           edit=lambda m: (m["names"].append({"name": "X", "kind": "const", "home": "driver_core"}),
                           m["source_mentions"].append({"file": "test_x.py", "function": "other", "count": 1,
                                                        "note": "driver_x.py"})))
    quiet = problems_of("L8 a driver_x.py literal with no row naming the file", "L8",
                        extra_files={"scripts/driver_x.py": "X = 1\n"},
                        tests_files={"test_x.py": 'def reader():\n    return "run driver_x.py now"\n'},
                        edit=lambda m: m["names"].append({"name": "X", "kind": "const", "home": "driver_core"}))
    check_eq("L8 a driver_x.py literal with no row naming the file is informational only (temporal rule)", quiet, [])
    expect("L9 a direct sys.stdout.write", "L9", "writes to sys.stdout directly",
           source=BASE_SOURCE.replace("self.low()", "sys.stdout.write('x')\n        self.low()"))
    expect("L9 print to another stream", "L9", "prints to a stream other than",
           source=BASE_SOURCE.replace("self.low()", "print('x', file=handle)\n        self.low()"))
    expect("L10 a row with no home", "L10", "has no home", edit=lambda m: m["names"][0].update(home=None))
    expect("L10 a home outside the layers", "L10", "not in `layers`", edit=lambda m: m["names"][0].update(home="nowhere"))
    expect("L10 two rows for one name", "L10", "two rows for `HERE`", edit=lambda m: m["names"].append(dict(m["names"][0])))
    expect("L10 an exception with no reason", "L10", "has no reason",
           edit=lambda m: m["exceptions"].append({"from": "a", "to": "b", "kind": "call", "reason": ""}))


def real_map() -> None:
    mp = json.loads(MAP_PATH.read_text(encoding="utf-8"))
    result = analyse(harness.PLUGIN_ROOT, mp)
    info = result["info"]
    names_in_map = len(mp.get("names", []))
    print(f"census: {info['names']} names defined by {', '.join(info['files'])} ({info['members']} Driver members); map rows "
          f"{names_in_map}; attributes {info['attr_seen'].__len__()}; state keys {len(info['state_seen'])}; dynamic state "
          f"sites {info['dynamic_state_sites']}; string-dispatch sites {info['dispatch_sites'] if isinstance(info['dispatch_sites'], int) else len(info['dispatch_sites'])}; "
          f"ad-hoc Person attributes {info['adhoc']}; edges {info['edges']} of which upward {info['upward']} "
          f"(exceptions rows {len(mp.get('exceptions', []))}); source-text sites {info['l8_sites']}")
    for check_id, found in result["problems"].items():
        if check_id == "L6" and not [m for m in read_modules(harness.PLUGIN_ROOT) if m != "story_run"]:
            print("L6 import direction: vacuous at N0 (no driver_* module); the bad fixtures below run the same check")
        check(f"{check_id} holds on the real driver ({len(found)} problem(s))", not found, "\n  " + "\n  ".join(found[:12]))
    readers = mp.get("source_readers", [])
    print(f"L8 source-pinning sites declared as readers: {sum(r['count'] for r in readers)} in "
          f"{len({r['file'] for r in readers})} files: "
          + "; ".join(f"{r['file']}::{r['function']}" for r in readers))
    for fname, hits in sorted(info["l8_extra"].items()):
        print(f"L8 informational: {len(hits)} literal(s) of {fname} in the tests, no row names the file yet: " + ", ".join(hits))
    pinned = {line.strip() for line in PINNED_EXCEPTIONS.strip().split("\n") if line.strip()}
    now = {f"{r['from']}>{r['to']}>{r['kind']}" for r in mp.get("exceptions", [])}
    check("the exceptions list is a subset of the pinned list (shrink-only)", now <= pinned,
          f"new rows: {sorted(now - pinned)}: the list only shrinks; remove the upward edge instead")


def main() -> None:
    if "--draft-missing" in sys.argv or "--draft-all" in sys.argv:
        mp = json.loads(MAP_PATH.read_text(encoding="utf-8")) if MAP_PATH.is_file() else {"names": []}
        result = analyse(harness.PLUGIN_ROOT, mp)
        print(json.dumps(draft_rows(result, mp)["names"], indent=0))
        if "--draft-all" in sys.argv:
            info = result["info"]
            print(json.dumps({"attributes": info["attr_seen"], "attr_init": sorted(info["attr_init"]),
                              "state_keys": info["state_seen"], "dyn_sites": info["dyn_sites"],
                              "dispatch_sites": info["dispatch_sites"], "adhoc": info["adhoc_seen"],
                              "upward_edges": info["upward_edges"],
                              "census_l8": {f"{k[0]}::{k[1]}": v for k, v in info["census_l8"].items()}}, indent=1))
        return
    real_map()
    bad_fixtures()
    finish("test_driver_layers")


if __name__ == "__main__":
    main()
