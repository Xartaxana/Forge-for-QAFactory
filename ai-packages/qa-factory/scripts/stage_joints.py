#!/usr/bin/env python3
"""The stage joints: every check the factory makes of a role is produced by something and told to the role (F6-51, FR-5, FR-38).

Run 12586 had 17 `gate_block` "digest: your final message is not the handoff form" and S5 quality receipts nobody
wrote. Both are one class: a gate demanded something of a role that nothing produced, or that the role was never told.
`references/stage-joints.json` is the census of those joints and this module is its reader and its walker. Three
directions, all red when they fail (AR-28: an unreadable input is never green):

  A  code -> registry   every check the walk meets in code has exactly one row. The universe is computed from the
                        package, never copied: the error families `exit_gate.all_errors`/`main` collect (AST), the
                        detectors of `stages.json` (read through `stage_guard.stage_model`, advisers excluded) and
                        the gap kinds `acceptance.validate_window` appends (AST).
  B  registry -> code   every producer entry names a role that exists (`agents/<role>.md`) or a function that is
                        defined (`null_outcomes.unresolved`); every `told` path exists and holds its anchor, and the
                        role RECEIVES it (its agent file, or the file the injection map delivers to it).
  C  demand -> told     every token an entry demands of a role is named in a file that role is told. Tokens come from
                        the existing tables through their readers (`demands_from`), never from a hand-made copy.

A leg that honestly does not exist today is a declared `gap` (ref + reason) under a shrink-only ratchet
(`ratchet[]`, checked by `null_outcomes.ratchet_problems`): an informed pass of the walk, counted, never silent (FR-4).
`told` and `demands` are PER ROLE: an entry lists the roles it speaks for, a `<role>` in a path is expanded for each,
and each role is judged on its own files. A `code:` producer is "told" where it is CALLED on the factory's path.

The file is read ONLY through `load_rows` (schema 2; a file of another schema is `(None, why)`, AR-13, AR-28). Its row keys are
the check ids code writes: `exit_gate:<family>` (an exit family), `<script stem>:*` (a detector script), `acceptance:<kind>` (a
window gap kind). The KIND of a key (exit, detector, window) is the member function's that produced it - `universe()` returns
`{key: {"kind", "where", "stages"}}` - and no reader classifies a key by its text. The lookups (`row_for`, `rows_for`) and the
renderers (`told_text`, `told_line`, `fill`) are the one road a requirement takes from a row to a receiver.

The walker is a measurer (FR-28) and a validator, so it writes nothing (FR-45): `audit()` is pure over what it is
given and the real tree is its default. Heavy imports (`null_outcomes`, `stage_guard`, `inject_context`,
`validate_artifacts`, `acceptance`) are taken inside the functions: the retro reads `threshold()` and must not import
the walker's graph.

CLI: `python -B scripts/stage_joints.py --check [--data <file>]` - exit 0 clean, 1 problems (the detector shape
`REJECT — N finding(s)`), 3 when the data file cannot be read (`detector_verdict.EXIT_UNREADABLE`, the `UNREADABLE:`
line; AR-18), 2 for a usage error (`--data` with no file).
"""
import ast
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PLUGIN = HERE.parent
sys.path.insert(0, str(HERE))

DATA = PLUGIN / "references" / "stage-joints.json"
KEY = "same_class_gate_blocks"
FRICTION_MIN = 2
SCHEMA = 2                                          # the one schema this reader reads; a file of another is `(None, why)`
TOP_KEYS = ("schema_version", "note", "friction", "joints", "ratchet", "when_kinds", "when_exclusive", "told_ratchet")
TOLD_RATCHET_KEYS = ("hand_cards", "legacy_legs", "unsited")   # the counters of the data file; `audit` measures and compares each
KIND_EXIT, KIND_DETECTOR, KIND_WINDOW = "exit", "detector", "window"
KINDS = (KIND_EXIT, KIND_DETECTOR, KIND_WINDOW)     # set by the member function that produced a key, never read from its text
EXIT_NAMESPACE = "exit_gate"                        # the namespace of a family the exit gate names itself
WINDOW_NAMESPACE = "acceptance"
ANY = "*"                                           # a row key `<stem>:*`; a row's stages `*`; a role list `["*"]`
MOVE_PREFIX = "move:"                               # a `when` token naming a move of `conductor-actions.json`
CAPABILITY_TOKENS = ("always", "shell", "no_shell")  # the `when` tokens a role's tools decide; every other token is a dispatch's
PLACEHOLDERS = ("T", "ID", "home")                  # the three words `fill` replaces
FORM_CARRIER = "handoff_form"
ROW_FIELDS_CARRIER = "window_record.REQUIRED_ROW_FIELDS"
COMMANDS_CARRIER = "role-commands.json"
PHASE_KEYS_CARRIER = "validate_artifacts.PHASE_JSON_KEYS"
FORM_TEXT = "every `required` field of your handoff form (section `Handoff form` of this page)"
ROW_KEYS = ("check", "stages", "producers", "joint")
OPTIONAL_ROW_KEYS = ("requirement", "requirement_from", "carrier_key", "door", "door_needs", "when", "role_rule")   # K3, K7
REQUIREMENT_CARRIERS = (FORM_CARRIER, PHASE_KEYS_CARRIER, ROW_FIELDS_CARRIER, COMMANDS_CARRIER)   # the closed `requirement_from`
DOOR_NEEDS = ("shell", "none")
PAGE_ITEM = {"page": True}                          # a told item: the row is on the role's generated key page (K2, gated)
PAGE_RENDERER = "requirement_section"               # the attribute of `contract_slices` whose presence turns the page leg on
KEY_PAGE = "references/slices/{role}/handoff-keys.md"
AHEAD_CARDS = "references/ahead-cards.json"
FALLBACK_NAME = "unlabelled"                        # `<stem>:unlabelled` and `unknown` are the ids code gives a record with no check
FALLBACK_ID = "unknown"
ENTRY_KEYS = ("roles", "code", "field", "told", "demands", "demands_from", "gap", "role_leg")
ENTRY_REQUIRED = ("field", "told")
TOLD_KEYS = ("path", "anchor")
GAP_KEYS = ("leg", "ref", "why")
LEGS = ("producer", "told", "demands")
CARRIERS = ("stages.json:required_outputs", "stages.json:witness", "stages.json:detectors",
            "validate_artifacts.PHASE_JSON_KEYS", "check:script")
GAP_REF = re.compile(r"^(B-\d+|F6-51/\d+)$")
GAP_WHY_MIN = 30
NOTE_MIN = 40
FIELD_MIN = 3
RATCHET_NODE = r"^F6-51$"
EXIT_SKIP = ("list", "all_errors")                  # the aggregator and a copy of the list are not families
EXIT_WRAPPERS = ("own",)                            # `own(family(...), "check")` wraps a family; the walk reads through it
EXIT_FUNCTIONS = ("all_errors", "main")
USAGE_EXIT = 2                                      # `--data` with no file; the unreadable file is the contract's exit 3
ROLE_LEG_KEY = "role_leg"                           # a code row whose role leg the walk does not judge says so in data
ROLE_LEG_NOT_WALKED = "not walked"


# ------------------------------------------------------------------------------------------- the universe
def _leaves(node) -> list:
    """The leaves of a `+` chain at any depth."""
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        return _leaves(node.left) + _leaves(node.right)
    return [node]


def exit_members(src: str, filename: str = "exit_gate.py") -> tuple:
    """`({key: member}, [walk errors])`: the families collected into `errors` by `all_errors` and `main`; a member is
    `{"kind": "exit", "where": str, "stages": None}` (a family is not judged by the stage rule).

    Every `errors = ...` / `errors += ...` in those two bodies (nested statements included: `ast.walk`) has its value
    split at `+`; a leaf that is a call of a bare name in `EXIT_WRAPPERS` (`own(family(...), "check")`) is replaced by its
    first positional argument, repeatedly, BEFORE the next rule runs (a wrapper with no argument is a walk error; the wrapper
    name is never a member). A leaf that is a call of a bare name is a family (the aggregator and `list` are not): its key is
    the id the innermost wrapper gives it - a str literal, else a walk error, never a key made from a name - or, with no
    wrapper, `exit_gate:<callee>`. A call of
    anything else (an attribute, a subscript) is a shape the walk cannot name: a walk error, never skipped (E6). A leaf
    that is no call (a name, a comprehension) is neither a member nor an error."""
    try:
        tree = ast.parse(src)
    except SyntaxError as exc:
        return {}, [f"cannot read the check at {filename}:{exc.lineno} - not Python ({exc.msg})"]
    members, errors = {}, []
    found = {fn.name for fn in tree.body if isinstance(fn, ast.FunctionDef)}
    for name in EXIT_FUNCTIONS:
        if name not in found:
            errors.append(f"cannot read the check at {filename}: no function `{name}`; extend the walk or restore it")
    for fn in (f for f in tree.body if isinstance(f, ast.FunctionDef) and f.name in EXIT_FUNCTIONS):
        for node in ast.walk(fn):
            if isinstance(node, ast.Assign):
                targets, value = node.targets, node.value
            elif isinstance(node, ast.AugAssign):
                targets, value = [node.target], node.value
            else:
                continue
            if not any(isinstance(t, ast.Name) and t.id == "errors" for t in targets):
                continue
            for leaf in _leaves(value):
                bad, wrapper = False, None
                while (isinstance(leaf, ast.Call) and isinstance(leaf.func, ast.Name)
                       and leaf.func.id in EXIT_WRAPPERS):
                    if not leaf.args:
                        errors.append(f"cannot read the check at {filename}:{leaf.lineno} - a call of "
                                      f"`{leaf.func.id}` with no argument in `errors`; extend the walk or simplify the call")
                        bad = True
                        break
                    wrapper, leaf = leaf, leaf.args[0]      # the innermost wrapper names the id (`with_check` keeps the first)
                if bad or not isinstance(leaf, ast.Call):
                    continue
                if isinstance(leaf.func, ast.Name):
                    if leaf.func.id in EXIT_SKIP:
                        continue
                    key = f"{EXIT_NAMESPACE}:{leaf.func.id}"
                    if wrapper is not None:
                        given = wrapper.args[1] if len(wrapper.args) > 1 else None
                        if not (isinstance(given, ast.Constant) and isinstance(given.value, str) and given.value):
                            errors.append(f"cannot read the check at {filename}:{wrapper.lineno} - the check id given to "
                                          f"`{wrapper.func.id}` at line {wrapper.lineno} is not a text; write the id as a literal")
                            continue
                        key = given.value
                    members.setdefault(key, {"kind": KIND_EXIT, "where": f"{filename}::{fn.name}:{leaf.lineno}", "stages": None})
                else:
                    errors.append(f"cannot read the check at {filename}:{leaf.lineno} - a call of a "
                                  f"{type(leaf.func).__name__} in `errors`; extend the walk or simplify the call")
    return members, errors


def detector_members(model: dict, filename: str = "stages.json") -> dict:
    """`{key: member}` for the blocking detectors of the stage model (the advisers - `advice` - never block). One member
    per script: its key is `<script stem>:*` (the stem is the namespace of its check ids), its `stages` the ids of every
    stage whose `detectors` list it, in `stages.json` order, its `where` the first of them."""
    out = {}
    for stage in model.get("stages") or []:
        advisers = {str(s) for s in stage.get("advice") or []}
        for scripts in (stage.get("detectors") or {}).values():
            for script in scripts or []:
                if str(script) in advisers:
                    continue
                member = out.setdefault(f"{Path(str(script)).stem}:{ANY}", {
                    "kind": KIND_DETECTOR, "where": f"{filename} {stage.get('id')}", "stages": []})
                if str(stage.get("id")) not in member["stages"]:
                    member["stages"].append(str(stage.get("id")))
    return out


def _leftmost(node):
    while isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        node = node.left
    return node


def _kinds(leaf, names: dict):
    """The kinds a gap's leading leaf stands for (text before the first `:`), or None when the shape is unreadable."""
    if isinstance(leaf, ast.Constant) and isinstance(leaf.value, str):
        return [leaf.value.split(":", 1)[0]]
    if isinstance(leaf, ast.Name):
        value = names.get(leaf.id)
        return [value.split(":", 1)[0]] if isinstance(value, str) else None
    if isinstance(leaf, ast.IfExp):
        left, right = _kinds(_leftmost(leaf.body), names), _kinds(_leftmost(leaf.orelse), names)
        return left + right if left is not None and right is not None else None
    return None


def window_members(src: str, names: dict, filename: str = "acceptance.py") -> tuple:
    """`({key: member}, [walk errors])`: the gap kinds `validate_window` appends, keyed `acceptance:<kind>`; a member is
    `{"kind": "window", "where": str, "stages": None}`. A `gaps.append(X)` stands for the kind of
    the leftmost leaf of X (a constant, a module name resolved through `names`, or both branches of a conditional);
    a `gaps.extend(<expr>)` stands for `acceptance:<f>` for each call of a bare name `f` inside it. Any other shape is a
    walk error (E6). Many sites of one kind are one member."""
    try:
        tree = ast.parse(src)
    except SyntaxError as exc:
        return {}, [f"cannot read the check at {filename}:{exc.lineno} - not Python ({exc.msg})"]
    fn = next((f for f in tree.body if isinstance(f, ast.FunctionDef) and f.name == "validate_window"), None)
    if fn is None:
        return {}, [f"cannot read the check at {filename}: no function `validate_window`; extend the walk or restore it"]
    members, errors = {}, []
    for call in (n for n in ast.walk(fn) if isinstance(n, ast.Call)):
        func = call.func
        if not (isinstance(func, ast.Attribute) and isinstance(func.value, ast.Name) and func.value.id == "gaps"
                and func.attr in ("append", "extend")):
            continue
        where = f"{filename}::validate_window:{call.lineno}"
        arg = call.args[0] if len(call.args) == 1 else None
        if arg is None:
            errors.append(f"cannot read the check at {filename}:{call.lineno} - gaps.{func.attr} with "
                          f"{len(call.args)} arguments; extend the walk or simplify the call")
        elif func.attr == "append":
            kinds = _kinds(_leftmost(arg), names)
            if kinds is None:
                errors.append(f"cannot read the check at {filename}:{call.lineno} - the leading part of the gap is "
                              f"a {type(_leftmost(arg)).__name__}, not a text, a module text or a conditional of two; "
                              "extend the walk or simplify the call")
            for kind in kinds or []:
                members.setdefault(f"{WINDOW_NAMESPACE}:{kind}", {"kind": KIND_WINDOW, "where": where, "stages": None})
        else:
            called = [n.func.id for n in ast.walk(arg) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)]
            if not called:
                errors.append(f"cannot read the check at {filename}:{call.lineno} - gaps.extend of an expression "
                              "with no call of a named function; extend the walk or simplify the call")
            for name in called:
                members.setdefault(f"{WINDOW_NAMESPACE}:{name}", {"kind": KIND_WINDOW, "where": where, "stages": None})
    return members, errors


def acceptance_names() -> dict:
    """The module-level texts of `acceptance` (the names a gap may start with); read at the call (lazy import)."""
    import acceptance
    return {k: v for k, v in vars(acceptance).items() if isinstance(v, str)}


def universe(exit_src=None, stages=None, acceptance_src=None, names=None) -> tuple:
    """`({key: {"kind", "where", "stages"}}, [walk errors])` of the three kinds. Every argument has the real default. The
    kind of a key is the one its member function gave it (`exit_members`, `detector_members`, `window_members`); no reader
    classifies a key by its text."""
    if exit_src is None:
        exit_src = (HERE / "exit_gate.py").read_text(encoding="utf-8")
    if stages is None:
        import stage_guard
        stages = stage_guard.stage_model()
    if acceptance_src is None:
        acceptance_src = (HERE / "acceptance.py").read_text(encoding="utf-8")
    if names is None:
        names = acceptance_names()
    keys, errors = exit_members(exit_src)
    w_keys, w_errors = window_members(acceptance_src, names)
    out = dict(keys)
    out.update(detector_members(stages))
    out.update(w_keys)
    return out, errors + w_errors


# --------------------------------------------------------------------------- the ids code writes (K1 direction B, K12)
_IDS_CACHE = {}


def is_fallback(check) -> bool:
    """`<stem>:unlabelled` and `unknown`: the ids code gives a record that carries no check. They need no row, and a fallback
    id never stands for coverage of a row (E2)."""
    check = str(check)
    return check == FALLBACK_ID or check.split(":", 1)[-1] == FALLBACK_NAME


def check_ids(plugin=None, records=None, errors=None) -> dict:
    """`{id: (file, function, line)}` of every check id that `refusal(...)` / `with_check(...)` write as a literal, and of every
    literal a listed pass-through def is called with (`refusal_registry.CHECK_PASSTHROUGH`). It reads the RECORDS of the one
    wide scan (`refusal_registry.sites`); this module has no AST walk of its own for ids (AR-13). The scan runs over the files
    whose text names `detector_verdict` and `with_check(` or `refusal(` (the scanner binds those calls to that module; a text
    pre-filter, never a reading of the code), once per plugin root.
    `records` injects the scan's answer; `errors`, a list, receives one sentence per walk error of that scan (a check
    argument that is no literal, a file that does not parse) - an id nobody could read is never silently absent (AR-28)."""
    import refusal_registry
    root = Path(plugin) if plugin else PLUGIN
    if records is None:
        key = str(root)
        if key not in _IDS_CACHE:
            def mentions(name):             # the scanner binds these calls to `detector_verdict`, so a file that never names it has none
                text = (root / "scripts" / name).read_text(encoding="utf-8", errors="replace")
                return "detector_verdict" in text and any(w in text for w in ("with_check(", "refusal("))
            names = [n for n in refusal_registry.package_files(root) if mentions(n)]
            _IDS_CACHE[key] = refusal_registry.sites(root, names, raises=refusal_registry.raise_family(root, names, wide=True))
        records = _IDS_CACHE[key]
    found = {}
    for rec in records:
        if rec.get("transport") in ("check_arg", "parse"):
            if errors is not None:
                errors.append(f"cannot read the check at {rec.get('file')}:{rec.get('line')} - "
                              f"{rec.get('why') or 'the file does not parse'}")
        elif rec.get("check"):
            found.setdefault(str(rec["check"]), (rec.get("file"), rec.get("function"), rec.get("line")))
    return found


def sited_ids(uni, ids=None, errors=None) -> set:
    """Every id a row may be keyed by and still have a site in code: the keys of the v1-derived universe, the check id of every
    A24 entry (`refusal_registry.check_of(e) for e in REGISTRY`), every literal id of the scanner (`check_ids`) and
    `role_cli:<key>` for every key of `references/role-commands.json` (`role_cli.refuse` and `RefusingParser.error` print that id
    as their check line; the keys are read through `role_cli.registry`, the one reader). A registry that yields no commands
    (absent, unreadable, empty) adds nothing and, when `errors` is a list, gets one sentence there - never a crash."""
    import refusal_registry
    import role_cli
    try:
        commands = role_cli.registry()
        commands = commands if isinstance(commands, dict) else {}
    except Exception:  # noqa: BLE001 - a file that is not the expected shape adds nothing, and is named below
        commands = {}
    if not commands and errors is not None:
        errors.append("references/role-commands.json yields no commands (absent, unreadable or empty): no `role_cli:<key>` id is sited")
    return (set(uni) | {refusal_registry.check_of(e) for e in refusal_registry.REGISTRY}
            | set(check_ids() if ids is None else ids) | {f"role_cli:{key}" for key in commands})


def _is_sited(key, sited) -> bool:
    """A key is sited when it is in the set, or is a sub-id `<id>.<part>` of a sited id (C14)."""
    return key in sited or any(str(key).startswith(f"{i}.") for i in sited)


# --------------------------------------------------------------------------------------------- the world
class Env:
    """What the walk reads besides the data: the stage model, the injection map, the tables a demand is read from."""

    def __init__(self, *, model, load_map, phase_keys, phase_writers, stage_of_role, plugin=PLUGIN, scripts=HERE):
        self.model, self.load_map = model, load_map
        self.phase_keys, self.phase_writers = phase_keys, phase_writers
        self.stage_of_role = stage_of_role
        self.plugin, self.scripts = Path(plugin), Path(scripts)
        self._texts, self._trees = {}, {}

    @classmethod
    def real(cls):
        import inject_context
        import stage_guard
        import validate_artifacts
        return cls(model=stage_guard.stage_model(), load_map=inject_context.load_map(),
                   phase_keys=validate_artifacts.PHASE_JSON_KEYS, phase_writers=validate_artifacts.PHASE_JSON_WRITERS,
                   stage_of_role=stage_guard.stage_of_role)

    def text(self, rel: str):
        """The text of a package file, or None when it cannot be read."""
        if rel not in self._texts:
            try:
                self._texts[rel] = (self.plugin / rel).read_text(encoding="utf-8", errors="replace")
            except OSError:
                self._texts[rel] = None
        return self._texts[rel]

    def calls(self, rel: str, function: str):
        """Line numbers of the CALLS of `function` in a package script, outside the function's own body; None when the
        file cannot be parsed. A name in a comment, a docstring or a string is no call (an AST walk)."""
        if rel not in self._trees:
            text = self.text(rel)
            try:
                self._trees[rel] = ast.parse(text) if text is not None else None
            except (SyntaxError, ValueError):
                self._trees[rel] = None
        tree = self._trees[rel]
        if tree is None:
            return None
        spans = [(n.lineno, n.end_lineno) for n in ast.walk(tree)
                 if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == function]
        hits = []
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            called = node.func.id if isinstance(node.func, ast.Name) else getattr(node.func, "attr", None)
            if called == function and not any(a <= node.lineno <= b for a, b in spans):
                hits.append(node.lineno)
        return hits

    def reaches(self, role: str, rel: str) -> bool:
        """True when `role` RECEIVES `rel`: its own agent file, or a file the injection map delivers to it."""
        if rel == f"agents/{role}.md":
            return True
        listed = list(self.load_map.get("common") or []) + list((self.load_map.get("roles") or {}).get(role) or [])
        return f"plugin:{rel}" in listed

    def role_exists(self, role: str) -> bool:
        return (self.plugin / "agents" / f"{role}.md").is_file()


def _base(artifact) -> str:
    text = str(artifact)
    return Path(text[len("project:"):] if text.startswith("project:") else text).name


def demand_tokens(carrier, role: str, check: str, env: Env) -> tuple:
    """`(tokens, why)`: what a carrier says the gate demands of `role`, read through the existing table (B-2)."""
    if carrier == "check:script":
        return [f"{check.split(':', 1)[0]}.py"], ""     # the stem is the id's namespace (`<stem>:*`), not a kind
    if carrier == "stages.json:witness":
        found = (env.model.get("witness") or {}).get(role)
        return ([_base(found)] if found else []), ""
    stage = env.stage_of_role(env.model, role)
    if carrier == "validate_artifacts.PHASE_JSON_KEYS":
        tokens = []
        for artifact, writer in env.phase_writers.items():
            if str(writer).removesuffix(".md") == role:
                tokens += list(env.phase_keys.get(artifact) or [])
        return tokens, ""
    if stage is None:
        return [], f"{role} is in no stage of stages.json"
    if carrier == "stages.json:required_outputs":
        return [_base(o) for o in stage.get("required_outputs") or []], ""
    if carrier == "stages.json:detectors":
        advisers = {str(s) for s in stage.get("advice") or []}
        return [s for s in (stage.get("detectors") or {}).get(role) or [] if s not in advisers], ""
    return [], f"unknown carrier {carrier!r}"


# ------------------------------------------------------------- the rows: the one reader, the lookups, the renderers
def load_rows(path=None) -> tuple:
    """`(data, "")`, or `(None, why)` - THE reader of `stage-joints.json` (AR-13); every code read of the file goes through it.
    `path` None is the module's `DATA`, taken at the call (a caller that re-points `DATA` is read).
    It wraps `null_outcomes.load_data`, so an absent, unreadable or malformed file has the reasons it always had; a file of
    a schema other than `SCHEMA` is `(None, "<name> has schema_version <v>; this reader reads 2")`. An unknown is a reason,
    never a pass and never an empty registry (AR-28)."""
    import null_outcomes
    path = Path(path) if path else DATA
    data, why = null_outcomes.load_data(path)
    if data is None:
        return None, why
    version = data.get("schema_version")
    if type(version) is not int or version != SCHEMA:
        return None, f"{path.name} has schema_version {version}; this reader reads {SCHEMA}"
    return data, ""


def _rows_data(data):
    """`(data, rows, why)`: `data` as given (a rows dict, as `load_rows` returns it) or the real file; `rows` None with a
    reason when there are none to read."""
    if data is None:
        data, why = load_rows()
        if data is None:
            return None, None, why
    rows = data.get("joints") if isinstance(data, dict) else None
    if not isinstance(rows, list):
        return None, None, "stage-joints.json `joints` is not a list"
    return data, [r for r in rows if isinstance(r, dict)], ""


def row_for(check, data=None) -> tuple:
    """`(row | None, why)` of a check id: the row keyed by exactly this id, else the row keyed by its namespace
    `<stem>:*`. Two rows for the id: the first and `why = "two rows"` (the walk is red on it, K5); none: `(None, why)`."""
    _data, rows, why = _rows_data(data)
    if rows is None:
        return None, why
    check = str(check)
    for wanted in (check, f"{check.split(':', 1)[0]}:{ANY}"):
        hit = [r for r in rows if r.get("check") == wanted]
        if hit:
            return hit[0], "two rows" if len(hit) > 1 else ""
    return None, f"no row for {check}"


def _states_requirement(row: dict) -> bool:
    """A row is told to a receiver only with `requirement` XOR `requirement_from` (a row with neither is told by its v1 legs)."""
    own, carrier = row.get("requirement"), row.get("requirement_from")
    has_own = isinstance(own, str) and bool(own.strip())
    has_carrier = isinstance(carrier, str) and bool(carrier.strip())
    return has_own != has_carrier


def _has_shell(role: str) -> bool:
    try:
        import host_adapter
        return bool(host_adapter.role_has_bash(role, PLUGIN))
    except Exception:  # noqa: BLE001 - the one default of every text written to a role: no shell (FR-2)
        return False


def _mapped_roles() -> set:
    """The roles of `inject-map.json` (what `roles: ["*"]` stands for); empty when the map cannot be read."""
    import null_outcomes
    data, _why = null_outcomes.load_data(PLUGIN / "references" / "inject-map.json")
    return set((data or {}).get("roles") or {})


def _row_names(row: dict, role: str, mapped) -> bool:
    for entry in row.get("producers") or []:
        roles = entry.get("roles") if isinstance(entry, dict) else None
        if isinstance(roles, list) and (role in roles or (ANY in roles and role != "conductor" and role in mapped())):
            return True
    return False


def _row_at(row: dict, stages) -> bool:
    mine = row.get("stages")
    mine = [mine] if isinstance(mine, str) else mine
    if not isinstance(mine, list):
        return False
    return ANY in stages or ANY in mine or bool(set(map(str, mine)) & set(map(str, stages)))


def _row_holds(row: dict, role: str, facts) -> bool:
    """Do the `when` tokens of the row hold? ALL must. A capability token is the role's (its tools); with `facts` None every
    dispatch group holds (the page); with a dict the dispatch tokens are read from it - for the conductor `{"moves": [ids]}`.
    An unknown or unstated token holds: the error direction is toward more text, never an omitted row (parent 2.4 (2))."""
    for token in row.get("when") or ["always"]:
        if token == "always":
            continue
        if token in CAPABILITY_TOKENS:
            if (token == "shell") != _has_shell(role):
                return False
        elif facts is None:
            continue
        elif role == "conductor":
            if str(token).startswith(MOVE_PREFIX) and str(token)[len(MOVE_PREFIX):] not in (facts.get("moves") or []):
                return False
        elif token in facts and not facts[token]:
            return False
    return True


def rows_for(role: str, stages, dispatch=None, data=None) -> list:
    """The rows a receiver is told: rows that state a requirement (`_states_requirement`), name `role` in a producer (`["*"]` is
    every role of `inject-map.json`, never the conductor), run at one of `stages` (`["*"]` is every stage), and whose `when`
    holds (`_row_holds`; `dispatch` is None or a facts dict). File order; `[]` when the rows cannot be read."""
    data, rows, _why = _rows_data(data)
    if rows is None:
        return []
    stages, cache = list(stages or []), {}

    def mapped() -> set:                                  # read once, and only when a row says `*`
        if "roles" not in cache:
            cache["roles"] = _mapped_roles()
        return cache["roles"]
    return [r for r in rows if _states_requirement(r) and _row_names(r, role, mapped) and _row_at(r, stages)
            and _row_holds(r, role, dispatch)]


def _carrier_expected(row: dict) -> tuple:
    """`(text, why)` of a `requirement_from` row: the carrier's own words, read at the call (lazy import)."""
    carrier, key = str(row.get("requirement_from")), str(row.get("carrier_key") or "")
    if carrier == FORM_CARRIER:
        return FORM_TEXT, ""
    if carrier == PHASE_KEYS_CARRIER:
        import validate_artifacts
        keys = validate_artifacts.PHASE_JSON_KEYS.get(key)
        return (f"`{key}` carries the keys " + ", ".join(f"`{k}`" for k in keys), "") if keys else ("", f"no keys for `{key}`")
    if carrier == ROW_FIELDS_CARRIER:
        import window_record
        return "; ".join(f"`{name}`: {spec.what}" for name, spec in window_record.REQUIRED_ROW_FIELDS.items()), ""
    if carrier == COMMANDS_CARRIER:
        import role_cli
        found = role_cli.entry(key)
        parts = [str(found["input"])] if found.get("input") else []
        parts += [f"how to prove it: {found['verify']}"] if found.get("verify") else []
        return ("; ".join(parts), "") if parts else ("", f"no command `{key}`")
    return "", f"unknown carrier {carrier!r}"


def told_text(row) -> tuple:
    """`(expected, door)` - THE composer of what a row tells (the page, the conductor section and a refusal all call it).
    `requirement` is the sentence; `requirement_from` is read from its carrier. A row that cannot be read gives a sentence
    saying so, never an exception and never an empty text (a missing row is never a pass, FR-59)."""
    row = row if isinstance(row, dict) else {}
    door = str(row.get("door") or "")
    if isinstance(row.get("requirement"), str) and row["requirement"].strip():
        return row["requirement"].strip(), door
    try:
        text, why = _carrier_expected(row) if row.get("requirement_from") else ("", "the row states no requirement")
    except Exception as exc:  # noqa: BLE001
        text, why = "", f"{type(exc).__name__}"
    return (text or f"(the factory's requirement row {row.get('check')} could not be read: {why}; this is a factory defect)"), door


def fill(text, values) -> str:
    """`text` with exactly `<T>`, `<ID>`, `<home>` replaced from `values`; a value that is missing or empty leaves its placeholder."""
    values = values if isinstance(values, dict) else {}
    return re.sub(r"<(" + "|".join(PLACEHOLDERS) + r")>",
                  lambda m: str(values[m.group(1)]) if values.get(m.group(1)) not in (None, "") else m.group(0), str(text))


def told_line(row, values=None) -> str:
    """THE line renderer: `- [<check>] <expected> Door: <door>.`; `fill` is applied when `values` is given."""
    expected, door = told_text(row)
    line = f"- [{row.get('check') if isinstance(row, dict) else None}] {expected} Door: {door}."
    return line if values is None else fill(line, values)


# ------------------------------------------------------------------------------------- the data's shape
def _shape_problems(data: dict) -> list:
    out = [f"stage-joints.json has an unknown key `{k}`" for k in data if k not in TOP_KEYS]
    out += [f"stage-joints.json lacks `{k}`" for k in TOP_KEYS if k not in data]
    if type(data.get("schema_version")) is not int or data.get("schema_version") != SCHEMA:
        out.append(f"stage-joints.json schema_version is {data.get('schema_version')!r}, this reader reads {SCHEMA}")
    if not isinstance(data.get("note"), str) or len(data.get("note").strip()) < NOTE_MIN:
        out.append(f"stage-joints.json `note` is shorter than {NOTE_MIN} characters - say what the file is")
    friction = data.get("friction")
    if not isinstance(friction, dict) or set(friction) != {KEY}:
        out.append(f"stage-joints.json `friction` is not an object holding exactly `{KEY}`")
    elif not _is_count(friction[KEY], FRICTION_MIN):
        out.append(f"stage-joints.json friction.{KEY} is {friction[KEY]!r}, an integer of at least {FRICTION_MIN} "
                   "is expected (one block of one class is the norm of MAX_BLOCKS, a repeat is the signal)")
    for key in ("joints", "ratchet"):
        if key in data and not isinstance(data[key], list):
            out.append(f"stage-joints.json `{key}` is not a list")
    if isinstance(data.get("joints"), list) and not data["joints"]:
        out.append("stage-joints.json has no joint rows (`joints` is empty): a lost file is not a state - the walk "
                   "meets checks in code")
    kinds = data.get("when_kinds")
    if "when_kinds" in data and (not isinstance(kinds, list) or not kinds
                                 or not all(isinstance(k, str) and k.strip() for k in kinds) or len(set(kinds)) != len(kinds)):
        out.append("stage-joints.json `when_kinds` is not a non-empty list of distinct texts")
    groups = data.get("when_exclusive")
    if "when_exclusive" in data and (not isinstance(groups, list) or not all(
            isinstance(g, list) and len(g) >= 2 and all(isinstance(k, str) for k in g) for g in groups)):
        out.append("stage-joints.json `when_exclusive` is not a list of lists of at least two kinds")
    elif isinstance(groups, list) and isinstance(kinds, list):
        out += [f"stage-joints.json `when_exclusive` names `{k}`, which is not in `when_kinds`"
                for g in groups for k in g if k not in kinds]
    told = data.get("told_ratchet")
    if "told_ratchet" in data:
        if not isinstance(told, dict) or set(told) != set(TOLD_RATCHET_KEYS):
            out.append(f"stage-joints.json `told_ratchet` is not an object holding exactly {', '.join(TOLD_RATCHET_KEYS)}")
        else:
            out += [f"stage-joints.json told_ratchet.{k} is {told[k]!r}, a count (an integer, 0 or more) is expected"
                    for k in TOLD_RATCHET_KEYS if not _is_count(told[k])]
    return out


def _is_count(value, minimum: int = 0) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value >= minimum


def _gap_problems(label: str, gap) -> list:
    if gap is None:
        return []
    if not isinstance(gap, dict) or set(gap) != set(GAP_KEYS):
        return [f"stage-joints: {label}: `gap` is null or an object of exactly {', '.join(GAP_KEYS)}"]
    out = []
    if gap["leg"] not in LEGS:
        out.append(f"stage-joints: {label}: gap leg {gap['leg']!r} is not one of {', '.join(LEGS)}")
    if not isinstance(gap["ref"], str) or not GAP_REF.match(gap["ref"]):
        out.append(f"stage-joints: {label}: gap ref {gap['ref']!r} is not `B-<n>` or `F6-51/<n>` - a gap points at the "
                   "item that closes it")
    if not isinstance(gap["why"], str) or len(gap["why"].strip()) < GAP_WHY_MIN:
        out.append(f"stage-joints: {label}: gap `why` is shorter than {GAP_WHY_MIN} characters - say why the leg is missing")
    return out


# ---------------------------------------------------------------------------------- one producer entry
def _producer_leg(entry: dict, env: Env) -> list:
    """What is wrong with the producer leg of one entry: [] when it names an existing role or a defined function."""
    roles, code = entry.get("roles"), entry.get("code")
    if (roles in (None, [])) and not code:
        return ["the producer leg is missing"]
    if roles and code:
        return ["`roles` and `code` are both given: an entry is a role's or a function's"]
    if roles:
        if not isinstance(roles, list) or not all(isinstance(r, str) for r in roles):
            return ["`roles` is not a list of role names"]
        return [f"role `{r}` has no agents/{r}.md" for r in roles if not env.role_exists(r)]
    import null_outcomes
    why = null_outcomes.unresolved(str(code), env.scripts)
    return [f"`code` {why}"] if why else []


def _expand(rel: str, role: str) -> str:
    return rel.replace("<role>", role)


def _is_page(item) -> bool:
    """`{"page": true}` exactly (`True`, not `1`): the row is told on the role's generated key page."""
    return isinstance(item, dict) and set(item) == set(PAGE_ITEM) and item["page"] is True


def _page_leg(entry: dict, row, env: Env) -> list:
    """K2, GATED (E6): a page item is refused with "the page renderer is not present" while `contract_slices` has no
    `requirement_section`, so no row is green on a page nothing renders. With the renderer present the leg is real: for every
    role the row names, whose capability the row's `when` admits, `rows_for` returns the row and the role's injection list
    holds its key page (for `conductor`: the `when` holds `conductor_answer` or a `move:<id>` token). Prose is never a leg."""
    if entry.get("code"):
        return ["a code producer is told where it is CALLED; a page has no meaning here"]
    import contract_slices
    if getattr(contract_slices, PAGE_RENDERER, None) is None:
        return [f"told by the page: the page renderer is not present (`contract_slices.{PAGE_RENDERER}` does not exist yet), "
                "so this row cannot be told on a page"]
    if not isinstance(row, dict):
        return ["told by the page: the page leg is judged with its row, and none was given"]
    roles = entry.get("roles") if isinstance(entry.get("roles"), list) else []
    if ANY in roles:
        roles = sorted(env.load_map.get("roles") or {})
    whens = [str(t) for t in row.get("when") or ["always"]]
    out = []
    for role in roles:
        if role == "conductor":
            if "conductor_answer" not in whens and not any(t.startswith(MOVE_PREFIX) for t in whens):
                out.append("told by the page: the conductor's section is selected by `conductor_answer` or a `move:<id>` token "
                           "and the row's `when` holds neither")
        elif _row_holds(row, role, None):
            page = KEY_PAGE.format(role=role)
            if not env.reaches(role, page):
                out.append(f"told by the page: {role} does not receive {page} (not in its inject-map.json list)")
            elif row not in rows_for(role, row.get("stages") or [], None, data={"joints": [row]}):
                out.append(f"told by the page: rows_for({role}) does not return this row (state one requirement, name the role "
                           "in a producer, run at a stage)")
    return out


def _told_leg(entry: dict, env: Env, row=None) -> list:
    """What is wrong with the told leg. An empty `told` is its own sentence, so a gap can name it. A page item is the K2 leg
    (`_page_leg`); `row` is the row the entry belongs to (the page leg reads its stages and `when`)."""
    told = entry.get("told")
    if not isinstance(told, list):
        return ["`told` is not a list"]
    if not told:
        return ["the told leg is missing"]
    out = []
    for item in told:
        if _is_page(item):
            out += _page_leg(entry, row, env)
            continue
        if not isinstance(item, dict) or not set(item) <= set(TOLD_KEYS) or "path" not in item:
            out.append(f"a told entry is not an object of path and anchor: {item!r}")
            continue
        if entry.get("code"):
            out += _called_problems(entry, item, env)
        else:
            out += _reach_problems(entry, item, env)
    return out


def _called_problems(entry: dict, item: dict, env: Env) -> list:
    rel, function = str(item["path"]), str(entry["code"]).split("::")[-1]
    if "anchor" in item:
        return [f"told {rel}: a code producer is told where it is CALLED; an anchor has no meaning here"]
    if not re.match(r"^scripts/[A-Za-z0-9_]+\.py$", rel):
        return [f"told {rel}: a code producer is called in a `scripts/*.py` file (not under tests/)"]
    hits = env.calls(rel, function)
    if hits is None:
        return [f"told {rel}: cannot be read or parsed"]
    return [] if hits else [f"told {rel}: no call of `{function}` outside its own definition (a name in a comment "
                            "or a string is no call) - the producer is not run on this path"]


def _reach_problems(entry: dict, item: dict, env: Env) -> list:
    out, anchor = [], item.get("anchor")
    if not isinstance(anchor, str) or not anchor.strip():
        return [f"told {item['path']}: `anchor` is missing - a verbatim phrase of the file proves what it says"]
    for role in entry.get("roles") or []:
        rel = _expand(str(item["path"]), role)
        text = env.text(rel)
        if text is None:
            out.append(f"told {rel}: the file does not exist ({role})")
        elif not env.reaches(role, rel):
            out.append(f"told {rel} is not read by {role} (not its agent file, not injected for it by inject-map.json)")
        elif anchor not in text:
            out.append(f"told {rel}: the anchor {anchor!r} is not in the file ({role})")
    return out


def _demands_leg(check: str, entry: dict, env: Env) -> list:
    """Direction C for one role entry: every demanded token occurs in a told file the role receives. A code producer
    demands nothing of a role."""
    if entry.get("code"):
        return []
    literal, carrier = entry.get("demands"), entry.get("demands_from")
    if not isinstance(literal, list) or not all(isinstance(t, str) and t for t in literal):
        return ["`demands` is not a list of tokens"]
    if carrier is not None and carrier not in CARRIERS:
        return [f"`demands_from` {carrier!r} is not one of {', '.join(CARRIERS)}"]
    out = []
    told = entry.get("told") if isinstance(entry.get("told"), list) else []
    page_only = bool(told) and all(_is_page(t) for t in told)       # the page carries the sentence: no tokens are owed (T1r)
    for role in entry.get("roles") or []:
        tokens, why = list(literal), ""
        if carrier:
            more, why = demand_tokens(carrier, role, check, env)
            tokens += more
        if page_only and not why and not tokens:
            continue
        if why or not tokens:
            out.append(why or f"the demands leg is missing for {role}")
            continue
        paths = [KEY_PAGE.format(role=role) if _is_page(t) else _expand(str(t["path"]), role)
                 for t in told if _is_page(t) or (isinstance(t, dict) and "path" in t)]
        texts = [env.text(p) or "" for p in paths if env.reaches(role, p)]
        out += [f"{role} is not told `{token}` in any of its told files" for token in dict.fromkeys(tokens)
                if not any(token in text for text in texts)]
    return out


def _entry_problems(check: str, index: int, entry, env: Env, row=None) -> tuple:
    """`(problems, has_gap)` of one producer entry: the sentences, and a bool - True when the entry declares a well-formed
    gap on a leg of LEGS (counted against the ratchet). A gap lets its leg be incomplete, once and by name."""
    label = f"{check} producer[{index}]"
    if not isinstance(entry, dict):
        return [f"stage-joints: {label} is not an object"], False
    out = [f"stage-joints: {label} has an unknown key `{k}`" for k in entry if k not in ENTRY_KEYS]
    out += [f"stage-joints: {label} lacks `{k}`" for k in ENTRY_REQUIRED if k not in entry]
    if out:
        return out, False
    if ROLE_LEG_KEY in entry and (entry[ROLE_LEG_KEY] != ROLE_LEG_NOT_WALKED or not entry.get("code")):
        out.append(f"stage-joints: {label}: `{ROLE_LEG_KEY}` is only `{ROLE_LEG_NOT_WALKED}`, on an entry with `code`")
    gap = entry.get("gap")
    out += _gap_problems(label, gap)
    if not isinstance(entry["field"], str) or len(entry["field"].strip()) < FIELD_MIN:
        out.append(f"stage-joints: {label}: `field` is shorter than {FIELD_MIN} characters - say what is produced")
    legs = {"producer": _producer_leg(entry, env)}
    if not legs["producer"]:
        legs["told"] = _told_leg(entry, env, row)
        if entry.get("told"):            # a missing told leg is said once; the tokens are judged against files that exist
            legs["demands"] = _demands_leg(check, entry, env)
    declared = gap.get("leg") if isinstance(gap, dict) else None
    for leg in LEGS:
        found = legs.get(leg)
        if found is None:
            continue
        if leg == declared:
            if not found:
                out.append(f"stage-joints: {label}: gap declared on a complete leg ({leg}) - remove it")
            continue
        for sentence in found:
            hint = (' and no gap is declared - name it, or declare {"leg","ref","why"} (FR-5, FR-38)'
                    if sentence.startswith(f"the {leg} leg is missing") else "")
            out.append(f"stage-joints: {label}: {sentence}{hint}")
    if declared in ("told", "demands") and declared not in legs:
        out.append(f"stage-joints: {label}: gap declared on the {declared} leg, which is not judged "
                   "(the producer leg, or an empty told leg, comes first)")
    return out, isinstance(gap, dict) and declared in LEGS


# --------------------------------------------------------------------------------------- one row, the rows
def _stash(env: Env, name: str, make):
    """One read per `Env` of a table the row checks consult (a cache on the object, never a second reader of the table)."""
    cache = env.__dict__.setdefault("_told_cache", {})
    if name not in cache:
        cache[name] = make()
    return cache[name]


def _row_requirement(check: str, row: dict, env: Env, kinds) -> list:
    """K3, K7, E4: the fields a row tells a receiver by. A row states a requirement one way (`requirement` XOR
    `requirement_from`, closed carriers), names a `door`, keeps `door_needs: "shell"` for a `when` that holds `shell`, takes
    `when` tokens from `when_kinds` or `move:<id>` of a real move, and joins a `role_rule` that exists. A row with neither
    requirement field is told by its v1 legs and is red only when it claims a page (E2). `kinds` None: `when_kinds` is unknown
    and the token list is not judged."""
    out = []
    own, carrier = row.get("requirement"), row.get("requirement_from")
    producers = [e for e in row.get("producers") or [] if isinstance(e, dict)] if isinstance(row.get("producers"), list) else []
    pages = any(_is_page(t) for e in producers for t in (e.get("told") if isinstance(e.get("told"), list) else []))
    for key, value in (("requirement", own), ("requirement_from", carrier), ("door", row.get("door")), ("carrier_key", row.get("carrier_key")),
                       ("role_rule", row.get("role_rule"))):
        if key in row and not isinstance(value, str):
            out.append(f"{key} is not a text")
    if isinstance(own, str) and own.strip() and isinstance(carrier, str) and carrier.strip():
        out.append("states its requirement two ways, `requirement` and `requirement_from`: keep one")
    stated = _states_requirement(row)
    if pages and not stated:
        out.append("is told by the page but states no requirement (`requirement` or `requirement_from`)")
    if stated:
        if isinstance(carrier, str) and carrier.strip():
            if carrier not in REQUIREMENT_CARRIERS:
                out.append(f"`requirement_from` {carrier!r} is not one of {', '.join(REQUIREMENT_CARRIERS)}")
            else:
                try:
                    why = _carrier_expected(row)[1]
                except Exception as exc:  # noqa: BLE001 - a carrier that cannot be read is a finding, not a crash
                    why = f"{type(exc).__name__} while reading it"
                if why:
                    out.append(f"`requirement_from` {carrier}: {why}")
        if not isinstance(row.get("door"), str) or not row["door"].strip():
            out.append("states a requirement and names no `door`: say where the receiver fixes it")
        if not any(isinstance(e.get("roles"), list) and e["roles"] for e in producers) or any(e.get("roles") == [] for e in producers):
            out.append("a requirement nobody is told - name the roles or remove the row")
    whens = row.get("when")
    if "when" in row and (not isinstance(whens, list) or not whens or not all(isinstance(t, str) and t.strip() for t in whens)):
        out.append("`when` is not a non-empty list of tokens")
    else:
        for token in whens or []:
            if token.startswith(MOVE_PREFIX):
                import no_move
                if token[len(MOVE_PREFIX):] not in _stash(env, "moves", lambda: set(no_move.move_ids())):
                    out.append(f"`when` token `{token}` names a move that is not in conductor-actions.json")
            elif kinds is not None and token not in kinds:
                out.append(f"`when` token `{token}` is not in `when_kinds` or a `move:<id>`")
    if "door_needs" in row:
        needs = row["door_needs"]
        if needs not in DOOR_NEEDS:
            out.append(f"`door_needs` {needs!r} is not one of {', '.join(DOOR_NEEDS)}")
        elif needs == "shell" and "shell" not in (whens if isinstance(whens, list) else []):
            out.append("`door_needs` is shell but `when` does not hold `shell`: a door a role without a shell cannot open (FR-2)")
    rule = row.get("role_rule")
    if isinstance(rule, str) and rule.strip():
        import role_rules
        known, why = _stash(env, "role_rules", lambda: (lambda r, p: ({str(x.get("id")) for x in r if isinstance(x, dict)}, p))(*role_rules.load(env.plugin)))
        if why:
            out.append(f"`role_rule` {rule} cannot be checked: design/role-rules.json cannot be read")
        elif rule not in known:
            out.append(f"`role_rule` {rule} is no id of design/role-rules.json")
    return [f"stage-joints: {check}: {text}" for text in out]


def _row_problems(row, env: Env, stage_ids: set, detectors: dict, kinds=None) -> tuple:
    """`(problems, [declared gap legs])` of one row. `detectors` is `detector_members(env.model)`: a row keyed by one of
    its members runs at exactly the stages the model gives that member (the key's text names no stage); `kinds` is the
    file's `when_kinds` (K3)."""
    if not isinstance(row, dict):
        return ["stage-joints: a joint row is not an object"], []
    check = str(row.get("check"))
    unknown = [k for k in row if k not in ROW_KEYS + OPTIONAL_ROW_KEYS]
    lacking = [k for k in ROW_KEYS if k not in row]
    out = [f"stage-joints: {check}: unknown key `{k}`" for k in unknown]
    out += [f"stage-joints: {check}: lacks `{k}`" for k in lacking]
    if unknown or lacking:
        return out, []
    stages = row["stages"]
    if not isinstance(stages, list) or not stages:
        out.append(f"stage-joints: {check}: `stages` is empty - a check that runs at no stage")
    elif stages == [ANY] and check not in detectors:
        pass                                           # the single item `*`: every stage (T1r); a detector row keeps its own stages
    elif ANY in stages and len(stages) > 1:
        out.append(f"stage-joints: {check}: `stages` mixes `{ANY}` with {[s for s in stages if s != ANY]}: `{ANY}` stands alone")
    elif not all(s in stage_ids for s in stages):
        out.append(f"stage-joints: {check}: `stages` names {[s for s in stages if s not in stage_ids]}, "
                   "which are no stage of stages.json")
    elif check in detectors and stages != detectors[check]["stages"]:
        out.append(f"stage-joints: {check}: `stages` is {stages}, a detector row runs at the stages whose detectors list its "
                   f"script: {', '.join(detectors[check]['stages'])}")
    out += _row_requirement(check, row, env, kinds)
    producers, gaps = row["producers"], []
    if not isinstance(producers, list) or not producers:
        out.append(f"stage-joints: {check}: `producers` is empty - an entry for each writer, or an entry whose gap "
                   "declares the producer leg")
        return out, gaps
    for index, entry in enumerate(producers):
        problems, has_gap = _entry_problems(check, index, entry, env, row)
        out += problems
        if has_gap:
            gaps.append(entry["gap"]["leg"])
    out += _joint_problems(check, row["joint"], env)
    return out, gaps


def _joint_problems(check: str, joint, env: Env) -> list:
    """The census of recorded-run tests: `null` is counted, never red; a joint names a test and a fixture that exist and
    the test must mention the fixture folder (the test really reads it)."""
    if joint is None:
        return []
    if not isinstance(joint, dict) or set(joint) != {"test", "fixture"}:
        return [f"stage-joints: {check}: `joint` is null or an object of `test` and `fixture`"]
    test, fixture = str(joint["test"]), str(joint["fixture"])
    out = []
    text = env.text(test)
    if text is None:
        out.append(f"stage-joints: {check}: joint test {test} does not exist")
    if not (env.plugin / fixture).exists():
        out.append(f"stage-joints: {check}: joint fixture {fixture} does not exist")
    elif text is not None and Path(fixture.rstrip("/")).name not in text:
        out.append(f"stage-joints: {check}: joint test {test} never mentions the fixture folder "
                   f"{Path(fixture.rstrip('/')).name} - it does not read it")
    return out


def _direction_a(rows: list, uni: dict, sited=None) -> tuple:    # uni: {key: member}, member = {"kind", "where", "stages"}
    """`(problems, unsited keys)`. Direction A: every check of the v1-derived universe has exactly one row (two rows for one id
    are red, E7: a `<stem>:*` row twice too). Direction B: a row whose key is not sited (`sited_ids`: the universe, the A24
    ids, the scanner's literal ids; or a sub-id of one) is UNSITED - returned, counted and compared to
    `told_ratchet.unsited` by `_ratchet`, never judged here. `sited` None: the universe alone."""
    out, seen, unsited = [], {}, []
    sited = set(uni) if sited is None else sited
    for row in rows:
        key = row.get("check") if isinstance(row, dict) else None
        seen[key] = seen.get(key, 0) + 1
    for key, n in seen.items():
        if n > 1:
            out.append(f"stage-joints: {key} has two rows")
        if not _is_sited(key, sited):
            unsited.append(key)
    for key, member in uni.items():
        if key not in seen:
            out.append(f"stage-joints: {key} is a check in code ({member['where']}) and has no row in references/stage-joints.json - "
                       "add its producer and where the role is told (FR-38, AR-10)")
    return out, unsited


def _pins(uni: dict, pins: dict) -> list:
    out = []
    for kind, pinned in (pins or {}).items():
        got = sum(1 for member in uni.values() if member["kind"] == kind)     # the producer's kind, never the key's text
        if got != pinned:
            out.append(f"{kind} checks: {got}, pinned {pinned}")
    return out


DENSE_COUNTERS = ("hand_cards",)      # a counter that is red BELOW its stored number too (§3.5a: audit (dense <=))
COUNTER_WORDS = {"hand_cards": "hand cards in references/ahead-cards.json",
                 "legacy_legs": "legacy told legs (a role entry told by a path other than its key page)"}


def _told_counters(data: dict, measured: dict) -> list:
    """The told counters of the data file against what `audit` measured (AR-20): measured over the stored number is red
    (named: counter, measured, stored); a dense counter below it is red too ("lower <counter> to N"). `unsited` is a list of row
    keys: with a stored 0 each is a stale row (E11 after the closing), above the stored number it is red as a count. A stored
    number that is absent or no count is the shape check's finding and is never read as 0."""
    told, out = data.get("told_ratchet"), []
    for name, got in measured.items():
        stored = told.get(name) if isinstance(told, dict) else None
        if not _is_count(stored):
            continue
        if name == "unsited":
            if got and stored == 0:
                out += [f"stage-joints: row {key}: stale - the walk does not meet this check; remove the row or fix its key"
                        for key in got]
            elif len(got) > stored:
                out.append(f"stage-joints: told_ratchet.unsited is {stored} but {len(got)} rows have no site in code "
                           f"({', '.join(got)}): a raise is named in the verdict (AR-20); write the site or remove the row")
        elif got > stored:
            out.append(f"stage-joints: told_ratchet.{name} is {stored} but the walk counts {got} {COUNTER_WORDS[name]}: a raise is "
                       "named in the verdict (AR-20); move the leg to a row instead")
        elif got < stored and name in DENSE_COUNTERS:
            out.append(f"stage-joints: lower told_ratchet.{name} to {got}: the walk counts {got} {COUNTER_WORDS[name]}, the "
                       f"ratchet says {stored} (a ratchet falls to what is measured)")
    return out


def _hand_cards(env: Env) -> tuple:
    """`(count | None, why)`: the cards of `references/ahead-cards.json` (`cards` is an object); None with a reason when the
    file cannot be counted (never 0)."""
    import null_outcomes
    data, why = null_outcomes.load_data(env.plugin / AHEAD_CARDS)
    if data is None:
        return None, why
    cards = data.get("cards")
    return (len(cards), "") if isinstance(cards, dict) else (None, f"{Path(AHEAD_CARDS).name} `cards` is not an object")


def _legacy_legs(rows: list) -> int:
    """Told items of role entries (not `code` entries) that name a path other than the role's own key page: the legs a row
    keeps by hand until it is told by `{"page": true}`."""
    return sum(1 for r in rows if isinstance(r, dict) for e in r.get("producers") or [] if isinstance(e, dict) and not e.get("code")
               for t in (e.get("told") if isinstance(e.get("told"), list) else [])
               if isinstance(t, dict) and "path" in t and t["path"] != KEY_PAGE.format(role="<role>"))


def _ratchet(data: dict, gaps: int, measured=None) -> list:
    import null_outcomes
    out = _told_counters(data, measured or {})
    rows = data.get("ratchet")
    if not isinstance(rows, list):
        return out
    return out + [f"stage-joints: {sentence}" for sentence in null_outcomes.ratchet_problems(
        rows, gaps, key="gaps", node_re=RATCHET_NODE, node_words="F6-51 (the node that keeps this ratchet)",
        rise="a raise is named in the verdict (AR-20); close a gap instead, or declare none", noun="gaps",
        unit="declared gaps", drift="a gap declared without raising the ratchet in the open, or closed without lowering it")]


# ------------------------------------------------------------------------------------------- the report
class Report:
    """What `audit` found: `problems` (sentences, [] = green) and `counts` for the summary line."""

    def __init__(self):
        self.problems = []
        self.counts = {"exit": 0, "detector": 0, "window": 0, "rows": 0, "gaps": 0, "producer": 0, "told": 0,
                       "demands": 0, "held": 0, "role_leg": 0, "hand_cards": 0, "legacy_legs": 0, "unsited": 0}
        self.no_detector = []

    @property
    def ok(self) -> bool:
        return not self.problems

    def line(self) -> str:
        c = self.counts
        return (f"stage joints: walked exit {c['exit']}, detector {c['detector']}, window {c['window']} | rows "
                f"{c['rows']}, gaps {c['gaps']} (producer {c['producer']}, told {c['told']}, demands {c['demands']}), "
                f"joints held {c['held']} of {c['rows']} | role leg not walked (code-to-code rows): {c['role_leg']} | "
                f"stages with no detector: "
                f"{', '.join(self.no_detector) or 'none'} | told counters: hand_cards {c['hand_cards']}, "
                f"legacy_legs {c['legacy_legs']}, unsited {c['unsited']}")


def audit(data=None, uni=None, pins=None, env=None, path=None, sited=None) -> Report:
    """Walk the registry against the package and say what has no home. Everything is injectable; the defaults are the
    real tree. `data` may be a str (the reason the file could not be read) - red, never an empty registry (E8).

    uni   `universe()`'s answer: ({key: {"kind", "where", "stages"}}, [walk errors]);  env   an `Env`;  pins  {kind: size}
    (red in both directions);  path  the data file to read when `data` is None (through `load_rows`);  sited  `sited_ids`' answer.
    The counters of `told_ratchet` (`hand_cards`, `legacy_legs`, `unsited`) are measured here from the package and the rows and
    compared in `_ratchet`; this function never opens the census or the told fixture (the census-needing counters are the
    test's, FR-44)."""
    report = Report()
    red = report.problems.append
    if data is None:
        data, why = load_rows(path)
        if data is None:
            red(f"stage-joints: {why}")
            return report
    elif isinstance(data, str):
        red(f"stage-joints: {data}")
        return report
    shape = _shape_problems(data)
    report.problems.extend(shape)
    if not isinstance(data.get("joints"), list) or not data["joints"]:
        return report
    env = env or Env.real()
    uni, walk_errors = universe() if uni is None else uni
    report.problems.extend(f"stage-joints: {e}" for e in walk_errors)
    report.problems.extend(f"stage-joints: {p}" for p in _pins(uni, pins))
    rows = data["joints"]
    if sited is None:
        id_errors = []
        sited = sited_ids(uni, check_ids(env.plugin, errors=id_errors), errors=id_errors)
        report.problems.extend(f"stage-joints: {e}" for e in id_errors)
    problems, unsited = _direction_a(rows, uni, sited)
    report.problems.extend(problems)
    stage_ids = {str(s.get("id")) for s in env.model.get("stages") or [] if isinstance(s, dict)}
    detectors = detector_members(env.model)          # from the model, not from the injectable `uni`
    declared = []
    for row in rows:
        problems, legs = _row_problems(row, env, stage_ids, detectors, data.get("when_kinds"))
        report.problems.extend(problems)
        declared += legs
    measured = {"legacy_legs": _legacy_legs(rows), "unsited": unsited}
    cards, why = _hand_cards(env)
    if cards is None:
        red(f"stage-joints: the hand cards cannot be counted ({why})")
    else:
        measured["hand_cards"] = cards
    report.problems.extend(_ratchet(data, len(declared), measured))
    c = report.counts
    c.update({"hand_cards": cards, "legacy_legs": measured["legacy_legs"], "unsited": len(unsited)})
    c.update({kind: sum(1 for member in uni.values() if member["kind"] == kind) for kind in KINDS})
    c.update({"rows": len(rows), "gaps": len(declared), "held": sum(1 for r in rows if isinstance(r, dict) and r.get("joint")),
              "role_leg": sum(1 for r in rows if isinstance(r, dict) for e in r.get("producers") or []
                              if isinstance(e, dict) and e.get(ROLE_LEG_KEY) == ROLE_LEG_NOT_WALKED)})
    for leg in LEGS:
        c[leg] = declared.count(leg)
    run_at = {stage for member in detectors.values() for stage in member["stages"]}
    report.no_detector = [str(s.get("id")) for s in env.model.get("stages") or [] if str(s.get("id")) not in run_at]
    return report


# ----------------------------------------------------------------------------------------- the threshold
def threshold(path=None):
    """The count of one class of gate block at which the retro says it is a finding, or None when the registry cannot
    say (absent file, bad JSON, no `friction`, not an integer of at least 2). None is "threshold unknown" to the reader,
    never a hidden default (E9)."""
    data, _why = load_rows(path)
    friction = (data or {}).get("friction")
    value = friction.get(KEY) if isinstance(friction, dict) else None
    return value if _is_count(value, FRICTION_MIN) else None


# ---------------------------------------------------------------------------------------------- the CLI
def main(argv=None) -> int:
    try:
        import console_io
        console_io.utf8_stdio()
    except ImportError:
        pass
    args = list(sys.argv[1:] if argv is None else argv)
    path = None
    if "--data" in args:
        at = args.index("--data")
        path = args[at + 1] if at + 1 < len(args) else None
        if path is None:
            print("stage_joints: --data needs a file", file=sys.stderr)
            return USAGE_EXIT
    data, why = load_rows(path)
    if data is None:
        import detector_verdict
        print(detector_verdict.unreadable_line(why))
        return detector_verdict.EXIT_UNREADABLE
    report = audit(data)
    print(report.line())
    if report.problems:
        print(f"REJECT — {len(report.problems)} finding(s):")
        for problem in report.problems:
            print(f"- {problem}")
        return 1
    print("stage joints: clean")
    return 0


if __name__ == "__main__":
    sys.exit(main())
