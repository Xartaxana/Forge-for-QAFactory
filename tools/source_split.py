#!/usr/bin/env python3
"""The mover: cuts one source file into home modules by a layer map (spec docs/tasks/specs/td-11a-driver-split.md, node T-1).

    python -B tools/source_split.py --map <map.json> --source <PKG-relative .py> [--class <Name>] [--homes a,b]
                                    (--dry-run | --apply) [--repo DIR] [--report FILE]
    python -B tools/source_split.py --selftest

CLASS mode (this node): `--class` names the class that is split into one mixin class per home; every other module-level
name moves as it is. The map gives `names` ({name, kind, home}; a member of the class is `<Class>.<member>`), `layers`
(rank = index of the group), `exceptions`, optionally `module_statements` ({"<first line of a module-level statement>": home})
and `setup_import` (the module whose import sets the console up). Data of the tool itself: tools/source-split-carriers.json
(package root, the checks it runs, the facade module, the carrier registries) - no module or file name of the package is
written in this code (AR-1).

What it does: reads the source as text (UTF-8 strict, one newline style, reused on output), takes the census of names with
`ast`, slices every name's segment from the TEXT (decorators and the comment block directly above travel with it), resolves
the free names of every segment to imports, rewrites only `<Class>.<m>` inside moved code to `<Mixin>.<m>` (W1) and the
path preamble of the facade (W2), writes one module per home and the facade, runs the carrier pass (registries keyed by a
file name) and proves the result (P1-P8). The facade keeps only the import names its own code uses (a deviation from spec
2.4, accepted by the Lead); an import line it keeps whole stays verbatim, comments included; every other comment line no
generated file carries is listed in the report by source line number.

Refusals (exit 2, nothing written; each line says what, what was expected and the door):
  R1 name with no map row            R2 map row whose name the source lacks     R3 name defined twice / two rows
  R4 free name of a HIGHER home      R5 free name that resolves to nothing      R6 same-rank import cycle
  R7 class-body use of a class-body name homed elsewhere                        R8 target module half-written or foreign
  R9 mixed newlines, non-UTF-8, BOM, non-ASCII generated text                    R10 module-level statement with no place
  R11 one statement whose targets go to different homes                          R12 free name of facade code unresolved
  R13 a rewritten `<Class>.<m>` is patched on the assembled class in the tests
  R14 `global` of a module name homed in another file   R15 a name both imported and defined at module level
  R16 a private (mangled) name in class code that is cut
  R17 a name some code rebinds through `global` is read bare from another home (a `from <part> import <name>` would
      read stale: the facade module refuses it at install)
  R18 a carrier of a class-qualified form (reader, py-tuple) that does not declare `class_key` (`assembled`: the row keeps
      the split class's own name and only its file changes; `mixin`: the row names the mixin class that holds the member)
P6 also RUNS the `verify` entries of every tool carrier (package-relative script, or {args, absent}) on the would-be tree:
exit 0, the closing line quoted, a timeout (`verify_timeout`, 120 s) or an `absent` text in the output is a failed proof;
a carrier with no `verify` says so in one line.
The map is a carrier of its own cut (T-1b): the would-be map gets a `names` row for every mixin class, the
`source_readers`/`source_mentions` rows of every test file the carrier pass rewrote are recomputed (a row at zero is
dropped, a missing row is added), and `family.installed` becomes true when the header holds that key (not with --homes);
P5 judges that map, and the map is written with the carriers (the layout of the file is kept line by line). An import no
segment and no facade code uses stays in the facade verbatim and is listed `kept (unused, possible side effect)`.
Proofs: P1 per-name segment sha256 equal (W1 applied before); P2 multiset of every name before == after (parts + facade);
P3 import of the facade in two trees of identical layout (dir(module) before is a subset of after, dir(class) equal);
P4 compile of every written file; P5 the layer test's analyse() on the result tree (with the tests dir) and the would-be map is
empty; P6 carrier pass resolves and no carrier still names the facade file with a moved name; P7 values COMPUTED on both
trees do not grow (pyflakes counts by class, dup groups, judgment-census counts; the pyflakes messages caused by a K7
setup-import line the tool itself added are subtracted, counted and printed); P8 K7 residue empty for every part and the facade.

Write: every file goes to a temp name beside its target and is `os.replace`d (parts first, the facade last, the carriers
after); any failure rolls back what was replaced. Exit: 0 done / nothing to do; 1 cannot run; 2 refused, a proof failed or
did not run on --apply, or the write failed - nothing written (or rolled back). --dry-run writes nothing and prints the
same report as --apply.
"""
from __future__ import annotations

import argparse
import ast
import builtins
import contextlib
import hashlib
import importlib
import importlib.util
import io
import json
import os
import re
import shutil
import subprocess
import symtable
import sys
import tempfile
import tokenize
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent
CARRIERS_FILE = TOOLS_DIR / "source-split-carriers.json"
BUILTINS = set(dir(builtins))
DUNDERS = {"__file__", "__name__", "__doc__", "__spec__", "__package__", "__builtins__", "__loader__", "__path__",
           "__class__", "__module__", "__qualname__"}
TOOL_NAME = "tools/source_split.py"

DOORS = {
    "R1": "add the row (the home is a judgment of the node author or the Lead), then re-run",
    "R2": "delete or rename the row",
    "R3": "keep one row and one definition",
    "R4": "rehome the name down in the map, or remove the edge",
    "R5": "fix the source or the map so the name resolves",
    "R6": "rehome one name of the cycle",
    "R7": "give both names one home",
    "R8": "restore the module (or remove it) and re-run",
    "R9": "fix the source or the generator input",
    "R10": "name the statement in the map's module_statements (statement -> home) or move it into a name",
    "R11": "give the targets of the statement one home",
    "R12": "fix the source, or home the name in a part",
    "R13": "patch the module through its facade, or move the target member to a home the test does not patch",
    "R14": "move the name's row to the same home as the code that rebinds it, or stop rebinding it (return the value)",
    "R15": "rename the module-level definition or the imported name",
    "R16": "use one leading underscore (no name mangling) for the name, or keep every user of it in one class",
    "R17": "move the reader into the name's home, or read the name through the facade module (`<facade>.<name>`)",
    "R18": "declare `class_key` (`assembled` or `mixin`) on the carrier in tools/source-split-carriers.json, from what the carrier's own reader keys by",
}
CLASS_KEYS = ("assembled", "mixin")
CLASS_KEYED_FORMS = ("reader", "py-tuple")     # the carrier forms whose rows name `<Class>.<member>`: they must declare which class


class Cannot(Exception):
    """Exit 1: the tool cannot run (bad arguments, unreadable file, unparsable source)."""


class WriteFailed(Cannot):
    """Exit 2: the write phase failed or the world changed under the plan; what was replaced is rolled back."""


class NotRun(Exception):
    """A proof that cannot be computed here (a tool it needs cannot be imported): reported, never a pass."""


@dataclass
class Refusal:
    code: str
    where: str
    what: str
    expected: str
    door: str = ""

    def line(self) -> str:
        return f"{self.code} {self.where}: {self.what}; expected: {self.expected}; door: {self.door or DOORS[self.code]}"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def camel(home: str) -> str:
    return "".join(p[:1].upper() + p[1:] for p in home.split("_") if p)


def load_cfg() -> dict:
    try:
        return json.loads(CARRIERS_FILE.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise Cannot(f"cannot read {CARRIERS_FILE.name}: {exc}")


# --- scanning one module text -----------------------------------------------------------------------------------------
@dataclass
class Unit:
    names: list
    kinds: list
    level: str                 # module | class | header | stmt | glue
    stmts: list
    ranges: list               # [(first line, last line)] of the segment, attached comments included
    orphan: str = ""
    body_index: int = 0
    home: str = ""
    moves: bool = False
    scope_free: set = field(default_factory=set)
    body_free: set = field(default_factory=set)
    edits: list = field(default_factory=list)        # W1: (line, col0, col1, replacement)
    glue_bound: set = field(default_factory=set)
    parts: list = field(default_factory=list)       # (first, last, orphan, body index) per statement of the unit

    @property
    def start(self) -> int:
        return self.ranges[0][0]

    @property
    def end(self) -> int:
        return self.ranges[-1][1]

    def label(self) -> str:
        return ", ".join(self.names) if self.names else f"statement at line {self.start}"


@dataclass
class Scan:
    tree: ast.Module
    lines: list
    units: list = field(default_factory=list)
    imports: list = field(default_factory=list)
    imp_start: dict = field(default_factory=dict)   # id(import node) -> first line, attached comments included
    doc: object = None
    main_block: object = None        # (node, start, orphan)
    preambles: list = field(default_factory=list)   # (node, start, orphan)
    strays: list = field(default_factory=list)      # Unit(level stmt)
    split_cls: object = None
    cls_doc: object = None           # (node, start, orphan)
    unattached_glue: list = field(default_factory=list)
    spans: list = field(default_factory=list)       # (first, last): source lines no generated file carries by construction
    shared: list = field(default_factory=list)      # lines where a statement starts on the line another one ended


def _targets(node) -> list:
    out = []
    for target in (node.targets if isinstance(node, ast.Assign) else [node.target]):
        for n in ast.walk(target):
            if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Store):
                out.append(n.id)
    return out


def _plain(node) -> bool:
    """Every target is a Name (or a tuple/list/starred of Names): `X[k] = v` and `obj.a = v` are not."""
    def ok(t) -> bool:
        if isinstance(t, ast.Name):
            return True
        if isinstance(t, (ast.Tuple, ast.List)):
            return all(ok(e) for e in t.elts)
        return isinstance(t, ast.Starred) and ok(t.value)
    targets = node.targets if isinstance(node, ast.Assign) else [node.target]
    return all(ok(t) for t in targets) and bool(_targets(node))


def _first_line(node) -> int:
    decos = getattr(node, "decorator_list", None) or []
    return min([node.lineno] + [d.lineno for d in decos])


def _seg_start(lines: list, first: int, indent: int, marker) -> int:
    i = first
    while i > 1:
        prev = lines[i - 2]
        s = prev.strip()
        if s.startswith("#") and (len(prev) - len(prev.lstrip(" "))) == indent and not marker.match(s):
            i -= 1
        else:
            break
    return i


def _orphan_span(lines: list, prev_end: int, start: int):
    """(first, last) source lines between two segments, blank edges trimmed; None when there is nothing."""
    a, b = prev_end + 1, start - 1
    while a <= b and not lines[a - 1].strip():
        a += 1
    while b >= a and not lines[b - 1].strip():
        b -= 1
    return (a, b) if a <= b else None


def _span_text(lines: list, span) -> str:
    return "" if span is None else "\n".join(lines[span[0] - 1:span[1]])


def _drop(sc: Scan, span) -> None:
    if span is None:
        return
    a, b = span
    if a == 1 and sc.lines and sc.lines[0].startswith("#!"):
        a = 2                                        # the shebang is carried by the facade
    if a <= b:
        sc.spans.append((a, b))


def _is_doc(node) -> bool:
    return isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant) and isinstance(node.value.value, str)


def _is_main_block(node) -> bool:
    return (isinstance(node, ast.If) and isinstance(node.test, ast.Compare) and isinstance(node.test.left, ast.Name)
            and node.test.left.id == "__name__")


def _dotted(node) -> str:
    parts = []
    while isinstance(node, ast.Attribute):
        parts.append(node.attr)
        node = node.value
    if isinstance(node, ast.Name):
        parts.append(node.id)
        return ".".join(reversed(parts))
    return ""


def _is_preamble(node, calls) -> bool:
    return (isinstance(node, ast.Expr) and isinstance(node.value, ast.Call) and _dotted(node.value.func) in calls)


def _kind_of(sub) -> str:
    kind = "method"
    for deco in sub.decorator_list:
        if isinstance(deco, ast.Name) and deco.id in ("staticmethod", "classmethod"):
            kind = deco.id
    return kind


def _walk_tables(tables, out: set) -> None:
    for table in tables:
        for sym in table.get_symbols():
            if sym.is_referenced() and sym.is_global() and not sym.is_parameter() and not sym.is_assigned():
                out.add(sym.get_name())
        _walk_tables(table.get_children(), out)


def _rebound_tables(table, out: set, top: bool = True) -> None:
    for sym in ([] if top else table.get_symbols()):
        if sym.is_declared_global() and sym.is_assigned():
            out.add(sym.get_name())
    for child in table.get_children():
        _rebound_tables(child, out, False)


def _rebound_globals(text: str, level: str) -> set:
    """Names a segment rebinds through `global` (declared global and assigned or deleted in a function body)."""
    src = ("class _C:\n" + text) if level in ("class", "glue") else text
    try:
        top = symtable.symtable(src + "\n", "<segment>", "exec")
    except SyntaxError as exc:
        raise Cannot(f"cannot analyse a segment ({exc.msg}, line {exc.lineno}): {text[:60]!r}")
    out: set = set()
    _rebound_tables(top, out)
    return out


def free_names(text: str, level: str) -> tuple:
    """(names read in the segment's own scope, names read inside function/lambda/comprehension bodies): loads not bound
    locally, decorators, default values and annotations included (they are evaluated where the def stands)."""
    src = ("class _C:\n" + text) if level in ("class", "glue") else text
    try:
        top = symtable.symtable(src + "\n", "<segment>", "exec")
    except SyntaxError as exc:
        raise Cannot(f"cannot analyse a segment ({exc.msg}, line {exc.lineno}): {text[:60]!r}")
    scope = top.get_children()[0] if level in ("class", "glue") else top
    own = {s.get_name() for s in scope.get_symbols()
           if s.is_referenced() and not (s.is_assigned() or s.is_imported() or s.is_namespace() or s.is_parameter())}
    body: set = set()
    _walk_tables(scope.get_children(), body)
    return own, body


def render(unit: Unit, lines: list, edits: bool = True) -> str:
    parts = []
    for a, b in unit.ranges:
        seg = list(lines[a - 1:b])
        if edits and unit.edits:
            for line_no, c0, c1, repl in sorted(unit.edits, key=lambda e: (e[0], -e[1])):
                if a <= line_no <= b:
                    idx = line_no - a
                    seg[idx] = seg[idx][:c0] + repl + seg[idx][c1:]
        parts.append("\n".join(seg))
    return "\n".join(parts)


def scan_text(text: str, class_re, prefix: str, marker_re: str, preamble_calls: list) -> Scan:
    tree = ast.parse(text)
    lines = text.split("\n")
    marker = re.compile(marker_re)
    sc = Scan(tree=tree, lines=lines)
    ctx = (class_re, prefix, marker, preamble_calls)
    prev_end = 0
    for i, node in enumerate(tree.body):
        first = _first_line(node)
        start = _seg_start(lines, first, node.col_offset, marker)
        span = _orphan_span(lines, prev_end, start)
        if i and first <= prev_end:
            sc.shared.append(first)
        prev_end = node.end_lineno
        _classify(sc, node, i, start, (_span_text(lines, span), span), ctx)
    _drop(sc, _orphan_span(lines, prev_end, len(lines) + 1))
    for unit in sc.units + sc.strays:
        if unit.level != "header":
            unit.scope_free, unit.body_free = free_names(render(unit, lines, False), "module" if unit.level != "class" else "class")
    return sc


def _classify(sc: Scan, node, i: int, start: int, orph: tuple, ctx: tuple) -> None:
    class_re, prefix, marker, calls = ctx
    orphan, span = orph
    rng = [(start, node.end_lineno)]
    if i == 0 and _is_doc(node):
        sc.doc = node
        _drop(sc, span)
    elif isinstance(node, (ast.Import, ast.ImportFrom)):
        sc.imports.append(node)
        sc.imp_start[id(node)] = start
        _drop(sc, span)
    elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
        sc.units.append(Unit([node.name], ["func"], "module", [node], rng, orphan))
    elif isinstance(node, ast.ClassDef):
        unit = Unit([node.name], ["class"], "header" if class_re.match(node.name) else "module", [node], rng, orphan)
        sc.units.append(unit)
        if class_re.match(node.name):
            sc.split_cls = node
            _scan_class(sc, node, prefix, marker)
    elif isinstance(node, (ast.Assign, ast.AnnAssign)) and _plain(node):
        names = _targets(node)
        sc.units.append(Unit(names, ["const"] * len(names), "module", [node], rng, orphan))
    elif _is_main_block(node):
        sc.main_block = (node, start, orphan)
    elif _is_preamble(node, calls):
        sc.preambles.append((node, start, orphan))
        _drop(sc, span)
        if start < node.lineno:
            _drop(sc, (start, node.lineno - 1))
    else:
        sc.strays.append(Unit([], [], "stmt", [node], rng, orphan))


def _accessor_owner(sub, members: list, prefix: str):
    """The member a `@name.setter` / `.getter` / `.deleter` function belongs to (a property pair is one unit)."""
    for deco in sub.decorator_list:
        if (isinstance(deco, ast.Attribute) and deco.attr in ("setter", "getter", "deleter")
                and isinstance(deco.value, ast.Name) and deco.value.id == sub.name):
            return next((m for m in reversed(members) if m.names == [f"{prefix}.{sub.name}"]), None)
    return None


def _scan_class(sc: Scan, node: ast.ClassDef, prefix: str, marker) -> None:
    lines = sc.lines
    header_end = max([node.lineno] + [getattr(b, "end_lineno", node.lineno) for b in node.bases]
                     + [getattr(k.value, "end_lineno", node.lineno) for k in node.keywords])
    prev_end = header_end
    members, glue, accessors = [], [], []
    for j, sub in enumerate(node.body):
        first = _first_line(sub)
        start = _seg_start(lines, first, sub.col_offset, marker)
        span = _orphan_span(lines, prev_end, start)
        orphan = _span_text(lines, span)
        if j and first <= prev_end:
            sc.shared.append(first)
        prev_end = sub.end_lineno
        rng = [(start, sub.end_lineno)]
        if j == 0 and _is_doc(sub):
            sc.cls_doc = (sub, start, orphan)
            _drop(sc, span)
        elif isinstance(sub, (ast.FunctionDef, ast.AsyncFunctionDef)):
            owner = _accessor_owner(sub, members, prefix)
            if owner is not None:
                accessors.append((owner, sub, (start, sub.end_lineno, orphan, j)))
            else:
                members.append(Unit([f"{prefix}.{sub.name}"], [_kind_of(sub)], "class", [sub], rng, orphan, j))
        elif isinstance(sub, (ast.Assign, ast.AnnAssign)) and _plain(sub):
            names = _targets(sub)
            members.append(Unit([f"{prefix}.{n}" for n in names], ["classconst"] * len(names), "class", [sub], rng, orphan, j))
        else:
            glue.append(Unit([], [], "glue", [sub], rng, orphan, j))
    for unit in members:
        unit.scope_free, unit.body_free = free_names(render(unit, lines, False), "class")
        unit.parts = [(unit.ranges[0][0], unit.ranges[0][1], unit.orphan, unit.body_index)]
    for owner, sub, part in accessors:
        owner.stmts.append(sub)
        owner.parts.append(part)
        own, body = free_names("\n".join(lines[part[0] - 1:part[1]]), "class")
        owner.scope_free |= own
        owner.body_free |= body
    _attach_glue(sc, members, glue)
    for unit in members:
        if len(unit.parts) > 1:
            unit.parts.sort()
            idx = [p[3] for p in unit.parts]
            if idx == list(range(idx[0], idx[0] + len(idx))):      # consecutive in the body: one slice
                unit.ranges = [(unit.parts[0][0], unit.parts[-1][1])]
            else:
                unit.ranges = [(p[0], p[1]) for p in unit.parts]
            unit.orphan = unit.parts[0][2]
        sc.units.append(unit)


def _attach_glue(sc: Scan, members: list, glue: list) -> None:
    """Class-body glue: an import is attached to the first member that reads the name it binds; a `del` to the unit that
    bound the name (spec 2.3). The statements of one unit travel together, in source order."""
    for g in glue:
        stmt = g.stmts[0]
        part = (g.ranges[0][0], g.ranges[0][1], g.orphan, g.body_index)
        if isinstance(stmt, (ast.Import, ast.ImportFrom)):
            bound = {(a.asname or a.name).split(".")[0] for a in stmt.names}
            users = [u for u in members if bound & u.scope_free and u.start > g.start]
            if users:
                owner = users[0]
                owner.stmts.append(stmt)
                owner.parts.append(part)
                owner.glue_bound |= bound
                continue
        elif isinstance(stmt, ast.Delete):
            gone = {t.id for t in stmt.targets if isinstance(t, ast.Name)}
            owner = next((u for u in members if gone & u.glue_bound), None)
            if owner is None:
                owner = next((u for u in members if gone & {n.split(".", 1)[1] for n in u.names}), None)
            if owner is not None:
                owner.stmts.append(stmt)
                owner.parts.append(part)
                continue
        sc.unattached_glue.append(g)


# --- the source ---------------------------------------------------------------------------------------------------------
@dataclass
class Source:
    path: Path
    rel: str
    raw: bytes
    text: str
    nl: str
    sha: str


def read_source(path: Path, rel: str, refusals: list) -> Source | None:
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise Cannot(f"cannot read the source {path}: {exc}")
    where = rel
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        refusals.append(Refusal("R9", where, f"the source is not UTF-8 ({exc.reason} at byte {exc.start})", "UTF-8 text"))
        return None
    if text.startswith("\ufeff"):
        refusals.append(Refusal("R9", where, "the source starts with a byte order mark", "UTF-8 without a BOM"))
        return None
    crlf = text.count("\r\n")
    lf = text.count("\n") - crlf
    cr = text.count("\r") - crlf
    kinds = [k for k, n in (("CRLF", crlf), ("LF", lf), ("CR", cr)) if n]
    if len(kinds) > 1 or kinds == ["CR"]:
        refusals.append(Refusal("R9", where, f"mixed or unsupported newlines ({', '.join(f'{k} {n}' for k, n in (('CRLF', crlf), ('LF', lf), ('CR', cr)) if n)})",
                                "one newline style, LF or CRLF"))
        return None
    nl = "\r\n" if crlf else "\n"
    return Source(path, rel, raw, text.replace("\r\n", "\n"), nl, sha256(raw))


# --- the plan -----------------------------------------------------------------------------------------------------------
@dataclass
class Args:
    map_path: Path
    source: str
    cls: str = ""
    homes: list = field(default_factory=list)
    apply: bool = False
    repo: Path = Path(".")
    report: str = ""


@dataclass
class Plan:
    args: Args
    cfg: dict
    refusals: list = field(default_factory=list)
    lines: list = field(default_factory=list)      # report lines
    warnings: list = field(default_factory=list)
    files: dict = field(default_factory=dict)      # name -> text (LF) of generated modules (rank order) and the facade (last)
    carriers: dict = field(default_factory=dict)   # path -> new text
    carrier_sha: dict = field(default_factory=dict)    # path -> sha256 of the bytes the carrier pass read
    carrier_view: dict = field(default_factory=dict)   # path -> text after the pass (every present tool carrier)
    rewrites: list = field(default_factory=list)
    carrier_rows: list = field(default_factory=list)
    proofs: list = field(default_factory=list)
    done: bool = False
    nothing: bool = False
    src: Source | None = None
    sc: Scan | None = None
    mp: dict = field(default_factory=dict)
    facade: str = ""
    stats: dict = field(default_factory=dict)
    map_new: dict | None = None                    # the would-be map (P5 judges it); None: nothing is generated yet
    map_text: str | None = None                    # its text, written with the carriers
    map_notes: list = field(default_factory=list)  # report lines about the map rewrite

    def refuse(self, code: str, where: str, what: str, expected: str, door: str = "") -> None:
        self.refusals.append(Refusal(code, where, what, expected, door))

    def say(self, line: str = "") -> None:
        self.lines.append(line)


def _import_table(sc: Scan) -> tuple:
    """(nodes, bound name -> (node index, alias))."""
    bound = {}
    for i, node in enumerate(sc.imports):
        for alias in node.names:
            if alias.name == "*":
                continue
            name = alias.asname or (alias.name.split(".")[0] if isinstance(node, ast.Import) else alias.name)
            bound[name] = (i, alias)
    return sc.imports, bound


def _import_line(node, aliases: list, noqa: str = "") -> str:
    def spec(a):
        return a.name + (f" as {a.asname}" if a.asname else "")
    if isinstance(node, ast.Import):
        text = "import " + ", ".join(spec(a) for a in aliases)
    else:
        text = f"from {'.' * node.level}{node.module or ''} import " + ", ".join(spec(a) for a in aliases)
    return text + (f"  # {noqa}" if noqa else "")


def _class_re(cls: str, exact: bool):
    if not cls:
        return re.compile(r"(?!)")
    return re.compile(r"^" + re.escape(cls) + ("$" if exact else r"[A-Za-z0-9]*$"))


def _existing_census(path: Path, cls: str, cfg: dict) -> set | None:
    try:
        text = path.read_text(encoding="utf-8")
        sc = scan_text(text.replace("\r\n", "\n"), _class_re(cls, False), cls, cfg["section_marker"], cfg["preamble_calls"])
    except (OSError, SyntaxError, UnicodeDecodeError, Cannot):
        return None
    names = set()
    for u in sc.units:
        names.update(u.names)
    return names


def make_plan(args: Args) -> Plan:
    cfg = load_cfg()
    plan = Plan(args=args, cfg=cfg)
    repo = Path(args.repo).resolve()
    pkg = repo / cfg["package_root"]
    src_path = pkg / args.source
    plan.facade = Path(args.source).stem
    try:
        mp_raw = Path(args.map_path).read_bytes()
        mp = json.loads(mp_raw.decode("utf-8"))
    except (OSError, ValueError) as exc:
        raise Cannot(f"cannot read the map {args.map_path}: {exc}")
    plan.mp = mp
    src = read_source(src_path, args.source, plan.refusals)
    plan.src = src
    try:
        map_rel = Path(args.map_path).resolve().relative_to(repo).as_posix()
    except ValueError:
        map_rel = Path(args.map_path).name
    plan.stats["map_sha"] = sha256(mp_raw)
    plan.stats["map_raw"] = mp_raw
    plan.stats["map_rel"] = map_rel
    if src is None:
        return plan
    cls = args.cls
    try:
        plan.sc = scan_text(src.text, _class_re(cls, True), cls, cfg["section_marker"], cfg["preamble_calls"])
    except SyntaxError as exc:
        raise Cannot(f"the source does not parse: {exc.msg} at line {exc.lineno}")
    _census_and_rows(plan, pkg, src_path.parent, cls)
    return plan


def _map_rows(plan: Plan) -> dict:
    rows, dups = {}, []
    for row in plan.mp.get("names", []):
        if row["name"] in rows:
            dups.append(row["name"])
        rows[row["name"]] = row
    for name in dups:
        plan.refuse("R3", "map", f"`{name}` has two rows", "one row per name")
    return rows


def _place_strays(plan: Plan) -> None:
    """R10: a module-level statement that is not a name, an import, the docstring, `__main__` or a declared preamble needs
    a place in `module_statements`; one key names one statement; two statements never share a physical line."""
    sc, cfg, rel = plan.sc, plan.cfg, plan.src.rel
    stmt_home = plan.mp.get("module_statements", {}) or {}
    fcall = f"{cfg['facade']['module']}.{cfg['facade']['call']}"
    sc.strays = [u for u in sc.strays if not (isinstance(u.stmts[0], ast.Expr) and isinstance(u.stmts[0].value, ast.Call)
                                              and _dotted(u.stmts[0].value.func) == fcall)]     # the facade's own install call, regenerated
    sc.unattached_glue = [g for g in sc.unattached_glue if not isinstance(g.stmts[0], ast.Pass)]
    used: dict = {}
    for u in sc.strays:
        first = sc.lines[u.start - 1].strip()
        first_stmt = sc.lines[u.stmts[0].lineno - 1].strip()
        key = first_stmt if first_stmt in stmt_home else first if first in stmt_home else None
        home = stmt_home.get(key) if key else None
        if not home:
            plan.refuse("R10", f"{rel}:{u.stmts[0].lineno}", f"module-level statement `{first_stmt[:70]}` is not a name, an import, the docstring, the `__main__` block or a declared preamble and the map has no place for it",
                        "a place in `module_statements`")
        else:
            u.home = home
            used.setdefault(key, []).append(u.stmts[0].lineno)
    for key, at in used.items():
        if len(at) > 1:
            plan.refuse("R10", rel, f"the module_statements key `{key[:60]}` places the statements at lines {at[0]} and {at[1]}"
                        + (f" (and {len(at) - 2} more)" if len(at) > 2 else ""), "one key per statement",
                        "make the first lines of the statements differ, or move one into a name")
    for ln in sc.shared:
        plan.refuse("R10", f"{rel}:{ln}", "a statement starts on the physical line where another one ends (two statements on one line)",
                    "one statement per line", "split the line in the source, then re-run")
    for g in sc.unattached_glue:
        stmt = g.stmts[0]
        text = sc.lines[stmt.lineno - 1].strip()[:70]
        if isinstance(stmt, (ast.Assign, ast.AnnAssign)):
            plan.refuse("R10", f"{rel}:{stmt.lineno}", f"class-body assignment `{text}` has no plain name target, so no member can carry it",
                        "a name target (`x = v`)", "bind a name, or move the effect into a method")
        else:
            plan.refuse("R10", f"{rel}:{stmt.lineno}", f"class-body statement `{text}` is neither a member nor glue of one",
                        "attach it to the member that uses the name it binds")


def _existing_parts(plan: Plan, scripts_dir: Path, cls: str, rank: dict) -> dict:
    existing = {}
    for home in rank:
        if home == plan.facade:
            continue
        path = scripts_dir / f"{home}.py"
        if path.is_file():
            names = _existing_census(path, cls, plan.cfg)
            existing[home] = names if names is not None else set()
            if names is None:
                plan.refuse("R8", f"{path.name}", "the existing target module does not parse", "a readable module")
    return existing


def _row_homes(plan: Plan, u: Unit, rows: dict, rank: dict, existing: dict, collide: dict) -> list:
    rel, homes = plan.src.rel, []
    for n in u.names:
        row = rows.get(n)
        if row is None:
            plan.refuse("R1", f"{rel}:{u.start}", f"`{n}` ({u.kinds[u.names.index(n)]}) has no map row", "a row {name, kind, home}")
            continue
        home = row.get("home")
        if home not in rank:
            plan.refuse("R1", f"{rel}:{u.start}", f"the row of `{n}` has the home {home!r}, which is not in `layers`", "a home of the layer list")
            continue
        homes.append(home)
        for other, names in existing.items():
            if n in names:
                collide.setdefault(other, []).append(n)
    return homes


def _assign_homes(plan: Plan, rows: dict, rank: dict, existing: dict, sel) -> dict:
    sc, rel, facade = plan.sc, plan.src.rel, plan.facade
    collide: dict = {}
    for u in sc.units + sc.strays:
        if u.level == "stmt":
            u.moves = bool(u.home) and u.home != facade and (sel is None or u.home in sel)
            continue
        homes = _row_homes(plan, u, rows, rank, existing, collide)
        if len(set(homes)) > 1:
            plan.refuse("R11", f"{rel}:{u.start}", f"one statement binds {', '.join(u.names)} but their rows are homed in {sorted(set(homes))}",
                        "one home for the targets")
        if homes:
            u.home = homes[0]
        u.moves = u.level != "header" and bool(u.home) and u.home != facade and (sel is None or u.home in sel)
    return collide


def _half_finished(plan: Plan, collide: dict) -> None:
    """R8 once: part files that still define names the source holds are the leftover of a run that did not finish."""
    if not collide:
        return
    files = sorted(f"{h}.py" for h in collide)
    detail = "; ".join(f"{h}.py holds {len(set(n))} of them (e.g. {', '.join(sorted(set(n))[:3])})" for h, n in sorted(collide.items()))
    plan.refuse("R8", ", ".join(files), f"{len(files)} part file(s) exist and still define names the source also defines, so they are the leftover of an earlier run that did not finish ({detail})",
                "no part file for a name the source still holds",
                f"remove {', '.join(files)} (the earlier run's leftovers) and re-run")


def _stale_rows(plan: Plan, rows: dict, rank: dict, existing: dict, half: set) -> None:
    rel = plan.src.rel
    census_names = {n for u in plan.sc.units for n in u.names}
    for n, row in rows.items():
        home = row.get("home")
        if n in census_names or home in existing:
            continue                        # an existing module is judged below (R8) as a whole
        if row.get("kind") == "class" and home in rank and n == camel(home):
            continue                        # the mixin class the cut will create: the layer test asks for its row
        plan.refuse("R2", "map", f"row `{n}` (home {home}) names nothing in {rel}", "a definition")
    for home, have in existing.items():
        want = {n for n, r in rows.items() if r.get("home") == home}
        if have != want and home not in half:
            missing, extra = sorted(want - have), sorted(have - want)
            plan.refuse("R8", f"{home}.py", f"the module exists but is not what the map homes there (missing {missing[:6]}{'...' if len(missing) > 6 else ''}, "
                        f"not homed there {extra[:6]}{'...' if len(extra) > 6 else ''})", "exactly the names the map homes there")


def _census_and_rows(plan: Plan, pkg: Path, scripts_dir: Path, cls: str) -> None:
    a, mp, sc = plan.args, plan.mp, plan.sc
    layers = mp.get("layers", [])
    rank = {m: i for i, group in enumerate(layers) for m in group}
    order = {m: n for n, m in enumerate(m for group in layers for m in group)}
    rows = _map_rows(plan)
    _place_strays(plan)
    seen: dict = {}
    for u in sc.units:
        for n in u.names:
            seen.setdefault(n, []).append(u)
    for n, found in seen.items():
        if len(found) > 1:
            plan.refuse("R3", f"{plan.src.rel}:{', '.join(str(x.start) for x in found)}", f"`{n}` is defined {len(found)} times", "one definition")
    existing = _existing_parts(plan, scripts_dir, cls, rank)
    sel = set(a.homes) if a.homes else None
    collide = _assign_homes(plan, rows, rank, existing, sel)
    _half_finished(plan, collide)
    _stale_rows(plan, rows, rank, existing, set(collide))
    plan.stats.update(rank=rank, order=order, rows=rows, existing=existing, homes={n: r.get("home") for n, r in rows.items()},
                      scripts_dir=scripts_dir, pkg=pkg, sel=sel)
    structural = [r for r in plan.refusals if r.code in ("R1", "R2", "R3", "R8", "R9", "R10", "R11")]
    moving = [u for u in sc.units + sc.strays if u.moves]
    plan.stats["moving"] = moving
    if not moving and not plan.refusals:
        plan.nothing = True
    elif not structural:
        from_generation(plan, cls)


# --- resolution and generation ------------------------------------------------------------------------------------------
@dataclass
class Spec:
    home: str
    src_used: set = field(default_factory=set)
    part_used: dict = field(default_factory=dict)

    def use_part(self, home: str, name: str) -> None:
        self.part_used.setdefault(home, set()).add(name)


class W1Finder(ast.NodeVisitor):
    def __init__(self, cls: str):
        self.cls, self.sites, self.bare = cls, [], []

    def visit_Attribute(self, node):
        if isinstance(node.value, ast.Name) and node.value.id == self.cls and isinstance(node.value.ctx, ast.Load):
            self.sites.append(node)
            return
        self.generic_visit(node)

    def visit_Name(self, node):
        if node.id == self.cls and isinstance(node.ctx, ast.Load):
            self.bare.append(node)


def _char_col(line: str, col: int) -> int:
    return len(line.encode("utf-8")[:col].decode("utf-8", errors="ignore"))


def _bound_name(node, alias) -> str:
    return alias.asname or (alias.name.split(".")[0] if isinstance(node, ast.Import) else alias.name)


def _ascii(plan: Plan, piece: str, where: str) -> None:
    if not piece.isascii():
        plan.refuse("R9", where, f"generated text is not ASCII: {piece[:60]!r}", "ASCII English generated text")


def _mangled(name: str) -> bool:
    return len(name) > 2 and name.startswith("__") and not name.endswith("__")


def _identifiers(stmts: list):
    for stmt in stmts:
        for n in ast.walk(stmt):
            if isinstance(n, ast.Attribute):
                yield n.attr, n.lineno
            elif isinstance(n, ast.Name):
                yield n.id, n.lineno
            elif isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                yield n.name, n.lineno
            elif isinstance(n, ast.arg):
                yield n.arg, n.lineno
            elif isinstance(n, ast.keyword) and n.arg:
                yield n.arg, getattr(n.value, "lineno", 0)


class Resolver:
    """Resolves the free names of every segment to an import, a census name of the same home, a part or a builtin;
    every refusal of the generation phase is raised here, before any text is built."""

    def __init__(self, plan: Plan, cls: str):
        self.plan, self.cls, self.sc = plan, cls, plan.sc
        st = plan.stats
        self.rank, self.order, self.rows = st["rank"], st["order"], st["rows"]
        self.facade, self.lines, self.rel = plan.facade, plan.sc.lines, plan.src.rel
        _nodes, self.bound = _import_table(self.sc)
        self.unit_of = {n: u for u in self.sc.units for n in u.names}
        self.member_names = {n.split(".", 1)[1] for n in self.rows if cls and n.startswith(cls + ".")}
        self.census_home = {n: r["home"] for n, r in self.rows.items() if not (cls and n.startswith(cls + "."))}
        self.specs, self.fac = {}, Spec(self.facade)
        self.exc_names = {(e["from"], e["to"]) for e in plan.mp.get("exceptions", []) if e.get("kind") == "name"}
        self.w1_targets, self.seen_r4 = [], set()
        self.class_moves = any(u.level == "class" and u.moves for u in self.sc.units)
        self.rebound = self.rebound_names()
        self.seen_r17 = set()

    def rebound_names(self) -> set:
        """Census names some unit (moved or staying) rebinds through `global`: no part or facade may import them by name."""
        out = set()
        for u in [x for x in self.sc.units if x.level != "header"] + self.sc.strays:
            out |= _rebound_globals(render(u, self.lines, False), "class" if u.level == "class" else "module")
        return {n for n in out if n in self.unit_of or n in self.census_home}

    def use(self, spec: Spec, g: str, name: str, where: str, label: str) -> None:
        """`from <g> import <name>` into `spec`'s module, except for a name rebound through `global` (R17)."""
        if name not in self.rebound:
            spec.use_part(g, name)
        elif (label, name) not in self.seen_r17:
            self.seen_r17.add((label, name))
            self.plan.refuse("R17", where, f"`{label}` reads `{name}` bare, and `{name}` (home {g}) is rebound through `global` by code of the cut; "
                             f"`from {g} import {name}` would read a stale copy (the facade module refuses it at install)",
                             "the reader and the rebinding code in one home")

    def eff(self, name):
        u = self.unit_of.get(name)
        return (u.home if u.moves else self.facade) if u is not None else self.census_home.get(name)

    def eff_member(self, m):
        u = self.unit_of.get(f"{self.cls}.{m}")
        if u is not None:
            return u.home if u.moves else self.facade
        return self.rows[f"{self.cls}.{m}"]["home"] if f"{self.cls}.{m}" in self.rows else None

    def r4(self, u, h, name, g, extra=""):
        if (u.label(), name) in self.seen_r4:
            return
        self.seen_r4.add((u.label(), name))
        tag = " (a name-kind row of `exceptions`: an import cannot carry it)" if any((lab, name) in self.exc_names for lab in u.names) else ""
        self.plan.refuse("R4", f"{self.rel}:{u.start}", f"{u.label()} (home {h}, rank {self.rank.get(h)}) uses `{name}` (home {g}, rank {self.rank.get(g)}), a higher layer{extra}{tag}",
                         "no upward import")

    def run(self) -> None:
        self.import_clash()
        for u in [x for x in self.sc.units if x.level != "header"] + self.sc.strays:
            self.unit(u)
        self.cycles()
        self.facade_side()

    def import_clash(self) -> None:
        """R15: a name both import-bound and defined at module level resolves to the wrong object in one of the homes."""
        for name in sorted(self.bound):
            u = self.unit_of.get(name)
            if u is not None:
                node = self.sc.imports[self.bound[name][0]]
                self.plan.refuse("R15", f"{self.rel}:{u.start}", f"`{name}` is bound by the import at line {node.lineno} and defined here at module level; "
                                 "the generated modules cannot tell which one a user means", "one meaning per name")

    def unit(self, u: Unit) -> None:
        h = u.home if u.moves else self.facade
        spec = self.specs.setdefault(h, Spec(h)) if u.moves else self.fac
        own = u.scope_free - u.glue_bound
        for name in sorted(own | u.body_free):
            self.name(u, h, spec, name, own)
        if u.moves and self.cls and self.cls in (own | u.body_free):
            self.w1(u, h, spec)
        self.hazards(u, h)

    def name(self, u: Unit, h: str, spec: Spec, name: str, own: set) -> None:
        plan, label = self.plan, u.label()
        if self.cls and name == self.cls:
            return
        if u.level == "class" and name in own and name in self.member_names:
            g = self.eff_member(name)
            if g != h:
                plan.refuse("R7", f"{self.rel}:{u.start}", f"the class-body expression of `{label}` uses the class-body name `{name}` homed in {g} (this one in {h})", "both names in one home")
            return
        if name in self.bound:
            spec.src_used.add(name)
        elif name in self.unit_of or name in self.census_home:
            g = self.eff(name)
            if g == h:
                return
            if not u.moves:
                if g != self.facade:
                    self.use(self.fac, g, name, f"{self.rel}:{u.start}", label)
            elif g is None or self.rank.get(g, 0) > self.rank.get(h, 0):
                self.r4(u, h, name, g)
            else:
                self.use(spec, g, name, f"{self.rel}:{u.start}", label)
        elif name in BUILTINS or name in DUNDERS:
            return
        elif u.moves:
            plan.refuse("R5", f"{self.rel}:{u.start}", f"`{name}` (read by `{label}`) resolves to nothing: no import, no census name, no builtin", "a definition or an import")
        else:
            plan.refuse("R12", f"{self.rel}:{u.start}", f"`{name}` (read by `{label}`, which stays in {self.rel}) does not resolve to a part, an import or a builtin", "a part that homes it")

    def hazards(self, u: Unit, h: str) -> None:
        """R14 `global` of a module name homed elsewhere; R16 a mangled name in class code that is cut."""
        for stmt in u.stmts:
            for n in ast.walk(stmt):
                if isinstance(n, ast.Global):
                    for name in n.names:
                        g = self.eff(name) if (name in self.unit_of or name in self.census_home) else None
                        if g is not None and g != h:
                            self.plan.refuse("R14", f"{self.rel}:{n.lineno}", f"`{u.label()}` (home {h}) declares `global {name}`, and `{name}` is homed in {g}; "
                                             "a module cannot rebind another module's global", "the name and the code that rebinds it in one home")
        if u.level == "class" and self.class_moves:
            seen = set()
            for ident, line in _identifiers(u.stmts):
                if _mangled(ident) and ident not in seen:
                    seen.add(ident)
                    self.plan.refuse("R16", f"{self.rel}:{line or u.start}", f"`{u.label()}` uses the private name `{ident}`: Python mangles it with the class name, "
                                     f"and the class is cut into mixins, so `_{self.cls}{ident}` would split into one name per mixin", "no mangled name in cut class code")

    def w1(self, u: Unit, h: str, spec: Spec) -> None:
        plan, label = self.plan, u.label()
        finder = W1Finder(self.cls)
        for stmt in u.stmts:
            finder.visit(stmt)
        for _n in finder.bare:
            self.r4(u, h, self.cls, self.facade, " (a bare use of the assembled class)")
        for node in finder.sites:
            m = node.attr
            if m not in self.member_names:
                plan.refuse("R5", f"{self.rel}:{node.lineno}", f"`{self.cls}.{m}` (read by `{label}`) names no map row", "a row for the member")
                continue
            g = self.eff_member(m)
            if g in (None, self.facade) or self.rank.get(g, 0) > self.rank.get(h, 0):
                self.r4(u, h, f"{self.cls}.{m}", g, " (a W1 rewrite target)")
                continue
            mixin = camel(g)
            line = self.lines[node.value.lineno - 1]
            u.edits.append((node.value.lineno, _char_col(line, node.value.col_offset), _char_col(line, node.value.end_col_offset), mixin))
            if g != h:
                spec.use_part(g, mixin)
            plan.rewrites.append(f"W1 {self.rel}:{node.lineno} {self.cls}.{m} -> {mixin}.{m} (in {label})")
            self.w1_targets.append((self.cls, m, f"{self.rel}:{node.lineno}"))
        if any(isinstance(n, ast.Name) and n.id == "super" for stmt in u.stmts for n in ast.walk(stmt)):
            plan.warnings.append(f"WARNING {self.rel}:{u.start} `{label}` calls super(): after the cut it names its mixin, not the assembled class")

    def cycles(self) -> None:
        graph = {h: sorted(g for g in s.part_used if g != h and self.rank.get(g) == self.rank.get(h)) for h, s in self.specs.items()}
        state: dict = {}

        def dfs(node, trail):
            state[node] = 1
            for nxt in graph.get(node, []):
                if state.get(nxt) == 1:
                    self.plan.refuse("R6", "homes", f"same-rank import cycle {' -> '.join(trail[trail.index(nxt):] + [nxt])}", "an acyclic import graph")
                elif nxt not in state:
                    dfs(nxt, trail + [nxt])
            state[node] = 2
        for h in sorted(graph):
            if h not in state:
                dfs(h, [h])

    def resolve_text(self, text: str, where: str, label: str) -> None:
        own, body = free_names(text, "module")
        for name in sorted(own | body):
            if name in self.bound:
                self.fac.src_used.add(name)
            elif name in self.unit_of or name in self.census_home:
                g = self.eff(name)
                if g not in (None, self.facade):
                    self.use(self.fac, g, name, where, label)
            elif name not in BUILTINS and name not in DUNDERS:
                self.plan.refuse("R12", where, f"`{name}` (read by {label}, which stays in {self.rel}) does not resolve to a part, an import or a builtin", "a part that homes it")

    def facade_side(self) -> None:
        sc, rel = self.sc, self.rel
        _r13(self.plan, self.w1_targets)
        if sc.main_block:
            node = sc.main_block[0]
            self.resolve_text("\n".join(self.lines[node.lineno - 1:node.end_lineno]), f"{rel}:{node.lineno}", "the `__main__` block")
        if sc.split_cls is not None:
            self.bases()
        self.preambles()

    def bases(self) -> None:
        for expr in list(self.sc.split_cls.bases) + [k.value for k in self.sc.split_cls.keywords]:
            for n in ast.walk(expr):
                if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load):
                    if n.id in self.bound:
                        self.fac.src_used.add(n.id)
                    elif n.id in self.unit_of or n.id in self.census_home:
                        if self.eff(n.id) not in (None, self.facade):
                            self.use(self.fac, self.eff(n.id), n.id, f"{self.rel}:{n.lineno}", f"the bases of `{self.cls}`")
                    elif n.id not in BUILTINS:
                        self.plan.refuse("R12", f"{self.rel}:{n.lineno}", f"the base `{n.id}` of `{self.cls}` does not resolve", "an import or a part that homes it")

    def preambles(self) -> None:
        plan, lines, rel = self.plan, self.lines, self.rel
        out = plan.stats["preamble"] = []
        for node, start, orphan in self.sc.preambles:
            text = "\n".join(lines[node.lineno - 1:node.end_lineno])
            own, body = free_names(text, "module")
            deps = sorted(n for n in (own | body) if n in self.unit_of)
            part_homes = {self.eff(n) for n in deps if self.eff(n) != self.facade}
            if len(part_homes) > 1:
                plan.refuse("R11", f"{rel}:{node.lineno}", f"the preamble `{text[:60]}` reads names homed in {sorted(part_homes)}", "one home for what the preamble reads")
                continue
            new_text, edits = self.w2(node, text, deps)
            if edits:
                plan.rewrites.append(f"W2 {rel}:{node.lineno} preamble `{text.strip()}` -> `{new_text.strip()}` (facade)")
            self.resolve_text(new_text, f"{rel}:{node.lineno}", "the facade's path preamble")
            home = next(iter(part_homes)) if part_homes else None
            if home:
                self.specs.setdefault(home, Spec(home)).src_used |= {n for n in (own | body) if n in self.bound}
            out.append((node, start, orphan, text, new_text, home))

    def w2(self, node, text: str, deps: list) -> tuple:
        edits = []
        for name in deps:
            if self.eff(name) == self.facade:
                continue
            stmt = self.unit_of[name].stmts[0]
            if not (isinstance(stmt, ast.Assign) and len(stmt.targets) == 1 and isinstance(stmt.targets[0], ast.Name)):
                self.plan.refuse("R12", f"{self.rel}:{node.lineno}", f"the preamble reads `{name}`, whose definition is not a simple `name = expr`, so the facade cannot carry it", "a simple definition")
                continue
            expr = ast.get_source_segment(self.plan.src.text, stmt.value)
            edits += [(n.lineno, n.col_offset, n.end_col_offset, expr) for n in ast.walk(node)
                      if isinstance(n, ast.Name) and n.id == name and isinstance(n.ctx, ast.Load)]
        seg = list(self.lines[node.lineno - 1:node.end_lineno])
        for ln, c0, c1, expr in sorted(edits, key=lambda e: (e[0], -e[1])):
            line = seg[ln - node.lineno]
            seg[ln - node.lineno] = line[:_char_col(line, c0)] + expr + line[_char_col(line, c1):]
        return "\n".join(seg), edits


def from_generation(plan: Plan, cls: str) -> None:
    res = Resolver(plan, cls)
    res.run()
    plan.stats.update(specs=res.specs, fac=res.fac, bound=res.bound, unit_of=res.unit_of, eff=res.eff, eff_member=res.eff_member,
                      member_names=res.member_names, census_home=res.census_home)
    _carrier_pass(plan, cls)
    build_texts(plan, cls)
    build_map(plan)


def _r13_patterns(c: str, m: str) -> list:
    c, m = re.escape(c), re.escape(m)
    return [re.compile(r"(?:setattr|patch\.object)\(\s*[\w.]*\b" + c + r"\s*,\s*[\"']" + m + r"[\"']"),
            re.compile(r"\b\w+\." + c + r"\." + m + r"\s*=(?!=)"),
            re.compile(r"patch\(\s*[\"'][\w.]*\b" + c + r"\." + m + r"[\"']"),
            re.compile(r"patch\.multiple\(\s*[^,)]*\b" + c + r"\b[^,)]*,(?:(?!\n\n)[\s\S]){0,600}?\b" + m + r"\s*=(?!=)")]


def _r13(plan: Plan, targets: list) -> None:
    tests = plan.stats["pkg"] / plan.cfg["tests_dir"]
    if not tests.is_dir() or not targets:
        return
    pats = {(c, m): (site, _r13_patterns(c, m)) for c, m, site in targets}
    for path in sorted(tests.rglob("*.py")):
        text = path.read_text(encoding="utf-8", errors="replace")
        for (c, m), (site, found) in pats.items():
            for pat in found:
                for hit in pat.finditer(text):
                    plan.refuse("R13", f"{path.relative_to(plan.stats['pkg']).as_posix()}:{text.count(chr(10), 0, hit.start()) + 1}",
                                f"`{c}.{m}` is patched on the assembled class, and the call at {site} is rewritten to the mixin, so the patch would not reach it",
                                "no patch of a member the cut rewrites")


def _kind_counts(units) -> tuple:
    f = m = c = 0
    for u in units:
        for k in u.kinds:
            if k in ("func", "class"):
                f += 1
            elif k in ("method", "staticmethod", "classmethod"):
                m += 1
            else:
                c += 1
    return f, m, c


def _reduced_imports(sc: Scan, used: set, noqa: str = "") -> list:
    out = []
    for node in sc.imports:
        keep = [a for a in node.names if a.name != "*" and _bound_name(node, a) in used]
        if keep:
            out.append(_import_line(node, keep, noqa))
    return out


def _item_text(unit: Unit, lines: list) -> str:
    body = render(unit, lines)
    return (unit.orphan + "\n\n" + body) if unit.orphan else body


def _join_items(items: list) -> str:
    out, prev = "", None
    for kind, text in items:
        if prev is not None:
            out += "\n\n" if (prev == "const" and kind == "const") else "\n\n\n"
        out += text
        prev = kind
    return out


def _kind_tag(u: Unit) -> str:
    return "const" if (u.kinds and set(u.kinds) == {"const"}) else "def"


def k7_line(setup: str) -> str:
    """The one line the tool adds to a part for the K7 console-setup check; P7 recognises it by this exact text."""
    return f"import {setup}  # noqa: F401 (console setup, K7)"


def _module_level_nodes(body: list):
    for node in body:
        yield node
        if isinstance(node, ast.Try):                 # the K7 check reads a setup import inside a module-level try the same way
            yield from _module_level_nodes(node.body)


def imports_module(text: str, module: str) -> bool:
    """True when the text imports `module` at module level (a module-level `try` body too, never inside a def, a class or an `if`)."""
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return False
    for node in _module_level_nodes(tree.body):
        if isinstance(node, ast.Import) and any(a.name.split(".")[0] == module for a in node.names):
            return True
        if isinstance(node, ast.ImportFrom) and not node.level and node.module and node.module.split(".")[0] == module:
            return True
    return False


def build_part(plan: Plan, home: str, cls: str, setup: str | None) -> str:
    sc, st = plan.sc, plan.stats
    spec = st["specs"].get(home, Spec(home))
    rank, order = st["rank"], st["order"]
    units = [u for u in st["moving"] if u.home == home]
    mod_items, cls_items = [], []
    for u in units:
        if u.level == "class":
            cls_items.append(u)
        else:
            mod_items.append((u.start, _kind_tag(u), _item_text(u, sc.lines)))
    for _n, start, _o, text, _new, phome in st.get("preamble", []):
        if phome == home:
            mod_items.append((start, "def", text))
    mod_items.sort(key=lambda x: x[0])
    what = (f"{cls} members" + (" and names" if mod_items else "")) if cls_items else "names"
    doc = f'"""{home}.py - {what} homed here by {st["map_rel"]} (TD-11 cut by {TOOL_NAME}); no behaviour of its own."""'
    imps = [k7_line(setup)] if setup else []
    imps += _reduced_imports(sc, spec.src_used)
    for g in sorted(spec.part_used, key=lambda g: (rank.get(g, 0), order.get(g, 0))):
        imps.append(f"from {g} import {', '.join(sorted(spec.part_used[g]))}")
    for piece in [doc] + imps + ([f"class {camel(home)}:"] if cls_items else []):
        _ascii(plan, piece, f"{home}.py")
    body = _join_items([(k, t) for _s, k, t in mod_items])
    if cls_items:
        members = "\n\n".join(_item_text(u, sc.lines) for u in sorted(cls_items, key=lambda x: x.start))
        block = f"class {camel(home)}:\n{members}"
        body = (body + "\n\n\n" + block) if body else block
    return doc + "\n\n" + ("\n".join(imps) + "\n\n\n" if imps else "\n") + body + "\n"


def parts_in_rank_order(plan: Plan) -> list:
    """The modules the facade imports and installs: every part of `layers` whose file this run writes or already exists, in
    rank order (L11 (b): the facade imports each part by a literal `import` and installs exactly the parts of the map; a part
    the source imported lazily is imported eagerly by the facade from now on - T-1b item 2)."""
    st = plan.stats
    homes = {r["home"] for r in st["rows"].values() if r.get("home") != plan.facade}
    wanted = {u.home for u in st["moving"] if u.home} | set(st["existing"])
    return sorted((h for h in homes if h in wanted), key=lambda h: (st["rank"].get(h, 0), st["order"].get(h, 0)))


def _inline_comments(lines: list, a: int, b: int) -> dict:
    out = {}
    try:
        for tok in tokenize.generate_tokens(io.StringIO("\n".join(lines[a - 1:b]) + "\n").readline):
            if tok.type == tokenize.COMMENT:
                out[a + tok.start[0] - 1] = tok.string
    except (tokenize.TokenError, SyntaxError):
        pass
    return out


def _facade_bases(plan: Plan) -> tuple:
    sc, src, st = plan.sc, plan.src, plan.stats
    node, rank, order = sc.split_cls, st["rank"], st["order"]
    orig = ([ast.get_source_segment(src.text, b) for b in node.bases] + [ast.get_source_segment(src.text, k) for k in node.keywords]) if node is not None else []
    mixins = []
    for g in sorted({st["eff_member"](m) for m in st["member_names"]} - {None, plan.facade}, key=lambda h: (-rank.get(h, 0), order.get(h, 0))):
        if camel(g) not in orig:
            mixins.append(camel(g))
            st["fac"].use_part(g, camel(g))
    return mixins, orig


def _facade_head(plan: Plan, kept: set) -> list:
    """Shebang, docstring, the import lines the facade keeps (verbatim when whole) and the path preambles, source order."""
    sc, st, lines = plan.sc, plan.stats, plan.sc.lines
    front = [lines[0]] if lines and lines[0].startswith("#!") else []
    if sc.doc is not None:
        front.append("\n".join(lines[sc.doc.lineno - 1:sc.doc.end_lineno]))
    pre = {id(n): new for n, _s, _o, _t, new, _h in st["preamble"]}
    seq = [(n.lineno, "i", n) for n in sc.imports] + [(n.lineno, "p", n) for n in [p[0] for p in st["preamble"]]]
    head, after_pre, dropped, unused = [], False, {}, []
    used_anywhere = set(st["fac"].src_used).union(*[s.src_used for s in st["specs"].values()]) if st["specs"] else set(st["fac"].src_used)
    for _ln, kind, n in sorted(seq, key=lambda x: x[0]):
        if kind == "p":
            head.append(pre[id(n)])
            after_pre = True
            continue
        # a name no segment and no facade code uses is KEPT (it may be there for a side effect); it is never dropped
        idle = [a for a in n.names if a.name != "*" and _bound_name(n, a) not in used_anywhere]
        keep = [a for a in n.names if a.name == "*" or _bound_name(n, a) in kept or a in idle]
        if idle:
            unused.append(f"{plan.src.rel}:{n.lineno} {_import_line(n, idle)}")
        start = sc.imp_start[id(n)]
        if len(keep) == len(n.names):
            head.append("\n".join(sc.lines[start - 1:n.end_lineno]))
            continue
        for ln in range(start, n.lineno):
            if lines[ln - 1].strip():
                dropped[ln] = lines[ln - 1].strip()
        dropped.update(_inline_comments(lines, n.lineno, n.end_lineno))
        if keep:
            head.append(_import_line(n, keep, "noqa: E402" if after_pre else ""))
    st["facade_unused"] = unused
    st["facade_dropped"] = dropped
    return front + [""] * bool(front) + head


def _facade_items(plan: Plan, cls: str, mixins: list, orig_bases: list) -> list:
    sc, lines = plan.sc, plan.sc.lines
    stay = [u for u in sc.units + sc.strays if not u.moves]
    items = []
    for u in stay:
        if u.level == "header":
            bases = ", ".join(mixins + orig_bases)
            _ascii(plan, bases, plan.src.rel)
            block = [f"class {cls}({bases}):"]
            if sc.cls_doc is not None:
                block.append("\n".join(lines[sc.cls_doc[1] - 1:sc.cls_doc[0].end_lineno]))
            block += [_item_text(m, lines) for m in sorted((x for x in stay if x.level == "class"), key=lambda x: x.start)]
            if len(block) == 1:
                block.append("    pass")
            items.append((u.start, "def", (u.orphan + "\n\n" if u.orphan else "") + "\n\n".join(block)))
        elif u.level in ("module", "stmt"):
            items.append((u.start, _kind_tag(u), _item_text(u, lines)))
    items.sort(key=lambda x: x[0])
    return items


def build_facade(plan: Plan, cls: str) -> str:
    sc, src, st = plan.sc, plan.src, plan.stats
    fac, rank, order = st["fac"], st["rank"], st["order"]
    parts = parts_in_rank_order(plan)
    mixins, orig_bases = _facade_bases(plan)
    head = _facade_head(plan, set(fac.src_used))
    cf = plan.cfg["facade"]
    gen = [f"import {cf['module']}  # noqa: E402"] + [f"import {h}  # noqa: E402,F401" for h in parts]
    for g in sorted(fac.part_used, key=lambda g: (rank.get(g, 0), order.get(g, 0))):
        gen.append(f"from {g} import {', '.join(sorted(fac.part_used[g]))}  # noqa: E402")
    install = f"{cf['module']}.{cf['call']}(__name__, [{', '.join(parts)}])"
    for piece in gen + [install]:
        _ascii(plan, piece, src.rel)
    items = _facade_items(plan, cls, mixins, orig_bases)
    chunks = ["\n".join(head + gen), _join_items([(k, t) for _s, k, t in items]), install]
    if sc.main_block:
        n, start, orphan = sc.main_block
        chunks.append((orphan + "\n\n" if orphan else "") + "\n".join(sc.lines[start - 1:n.end_lineno]))
    return "\n\n\n".join(c for c in chunks if c) + "\n"


def _find_check(plan: Plan, rel: str) -> Path | None:
    for base in (plan.stats["pkg"], TOOLS_DIR.parent / plan.cfg["package_root"]):
        if (base / rel).is_file():
            return base / rel
    return None


def _load_module(path: Path, label: str):
    for d in (path.parent, path.parent.parent):
        if str(d) not in sys.path:
            sys.path.insert(0, str(d))
    spec = importlib.util.spec_from_file_location(label, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _k7_run(plan: Plan, texts: dict) -> tuple:
    """({file: lines flagged}, "") or (None, why it was not evaluated)."""
    st = plan.stats
    path = _find_check(plan, plan.cfg["k7"]["file"])
    if path is None:
        return None, "K7 not evaluated: the check file is absent"
    try:
        if st.get("k7_mod") is None:
            st["k7_mod"] = _load_module(path, "_k7_check")
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
            for name, text in texts.items():
                (Path(tmp) / name).write_bytes(text.encode("utf-8"))
            return getattr(st["k7_mod"], plan.cfg["k7"]["entry"])(Path(tmp)), ""
    except Exception as exc:                      # noqa: BLE001 - reported, never silent
        return None, f"WARNING K7 not evaluated: {type(exc).__name__}: {exc}"


def _k7_setup_lines(plan: Plan, texts: dict, cls: str) -> None:
    k7, setup = plan.stats["k7"], plan.mp.get("setup_import")
    flagged, why = _k7_run(plan, texts)
    if flagged is None:
        k7.append(why)
        return
    for name in sorted(texts):
        if name not in flagged:
            k7.append(f"K7 {name}: not flagged")
        elif setup and name != f"{setup}.py" and imports_module(texts[name], setup):
            k7.append(f"K7 {name}: would be flagged at lines {flagged[name]}; it already imports `{setup}` at module level, no line added")
        elif setup and name != f"{setup}.py":
            texts[name] = build_part(plan, name[:-3], cls, setup)
            k7.append(f"K7 {name}: would be flagged at lines {flagged[name]}; adds `{k7_line(setup)}`")
        else:
            k7.append(f"WARNING K7 {name}: would be flagged at lines {flagged[name]}; the map has no `setup_import` key, no line added")


def build_texts(plan: Plan, cls: str) -> None:
    st = plan.stats
    homes = sorted({u.home for u in st["moving"] if u.home}, key=lambda h: (st["rank"].get(h, 0), st["order"].get(h, 0)))
    texts = {f"{h}.py": build_part(plan, h, cls, None) for h in homes}
    st["k7"] = []
    _k7_setup_lines(plan, texts, cls)
    texts[f"{plan.facade}.py"] = build_facade(plan, cls)
    plan.files = texts
    left, why = _k7_run(plan, texts)
    st["k7_left"], st["k7_why"] = left, why


# --- the map as a carrier of its own cut ----------------------------------------------------------------------------------
def _family_file_names(plan: Plan) -> list:
    """The file names the layer test counts as the family's: the facade, the parts this run writes and the parts that exist
    (the map's `family.prefix`, minus the modules `not_driver` exempts)."""
    st, fam = plan.stats, plan.mp.get("family")
    exempt = {r.get("module") for r in plan.mp.get("not_driver", []) if isinstance(r, dict)}
    names = {plan.facade + ".py"} | set(plan.files)
    prefix = fam.get("prefix") if isinstance(fam, dict) else None
    if isinstance(prefix, str) and prefix:
        names |= {p.name for p in st["scripts_dir"].glob(prefix + "*.py") if p.stem not in exempt}
    else:
        names |= {f"{h}.py" for h in st["existing"]}
    return sorted(names)


def _layer_module(plan: Plan):
    """The layer test module (cached); None when its file is absent."""
    st = plan.stats
    if "layer_mod" not in st:
        lt = _find_check(plan, plan.cfg["layer_test"]["file"])
        st["layer_mod"] = _load_module(lt, "_layer_check") if lt is not None else None
    return st["layer_mod"]


def _l8_skip(plan: Plan) -> set:
    try:
        mod = _layer_module(plan)
    except Exception:                             # noqa: BLE001 - P5 reports a layer test that cannot be loaded
        return set()
    if mod is None:
        return set()
    return (set(getattr(mod, "L8_SKIP_ALL", ())) | set(getattr(mod, "L8_SKIP_BY_FACADE", {}).get(plan.facade, ()))
            | {x for x in plan.mp.get("l8_skip", []) if isinstance(x, str)})


def literal_counts(tree: ast.Module, needles: list) -> dict:
    """{enclosing def name (`<module>` at module level): occurrences of any needle in its non-docstring string constants},
    the count the layer test's L8 takes (every family file name counts)."""
    docs = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            body = node.body
            if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant) and isinstance(body[0].value.value, str):
                docs.add(id(body[0].value))
    out: dict = {}

    def walk(node, function):
        for child in ast.iter_child_nodes(node):
            fn = child.name if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)) else function
            if isinstance(child, ast.Constant) and isinstance(child.value, str) and id(child) not in docs:
                n = sum(child.value.count(x) for x in needles)
                if n:
                    out[fn] = out.get(fn, 0) + n
            walk(child, fn)
    walk(tree, "<module>")
    return out


def _function_reads(tree: ast.Module, function: str) -> bool:
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == function:
            if any(isinstance(s, ast.Attribute) and s.attr in ("read_text", "read_bytes") for s in ast.walk(node)):
                return True
    return False


def _shrink(rows: list, total: int) -> int:
    """Cap the counts of `rows` in order so they sum to at most `total`; returns what is left of `total`."""
    for row in rows:
        row["count"] = min(row.get("count", 0), total)
        total -= row["count"]
    return total


def reconcile_rows(obj: dict, file: str, text: str, needles: list) -> list:
    """Make the `source_readers`/`source_mentions` rows of one test file say what the layer test's L8 counts in `text`:
    a count is set to the real one, a row at zero is dropped, a literal with no row gets one. Returns the change lines."""
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return []
    counts = literal_counts(tree, needles)
    out = []
    readers, mentions = obj.get("source_readers", []), obj.get("source_mentions", [])
    funcs = set(counts) | {r.get("function", "") for r in readers + mentions if r.get("file") == file}
    for fn in sorted(funcs):
        total = counts.get(fn, 0)
        rr = [r for r in readers if r.get("file") == file and r.get("function") == fn]
        mm = [r for r in mentions if r.get("file") == file and r.get("function", "") == fn]
        declared = sum(r.get("count", 0) for r in rr + mm)
        if total == declared:
            continue
        if rr or mm:
            left = _shrink(rr + mm, total)
            if left:
                (rr + mm)[0]["count"] += left
            for row in [r for r in rr + mm if r["count"] <= 0]:
                (readers if row in rr else mentions).remove(row)
            out.append(f"map {file}::{fn}: declared {declared}, the would-be file holds {total}: " + ("row dropped" if not total else "count set"))
        else:
            reads = _function_reads(tree, fn)
            new = ({"file": file, "function": fn, "count": total, "targets": ["added by the cut: the carrier pass wrote a family file name here"]} if reads else
                   {"file": file, "function": fn, "count": total, "why": "added by the cut: the carrier pass wrote a family file name here (command text or a key, not a read)"})
            obj.setdefault("source_readers" if reads else "source_mentions", []).append(new)
            out.append(f"map {file}::{fn}: no row, the would-be file holds {total}: row added to {'source_readers' if reads else 'source_mentions'}")
    return out


def _mixin_rows(plan: Plan, obj: dict) -> list:
    st = plan.stats
    homes = sorted({u.home for u in st["moving"] if u.home and u.level == "class"}, key=lambda h: (st["rank"].get(h, 0), st["order"].get(h, 0)))
    added = [h for h in homes if camel(h) not in st["rows"]]
    for h in added:
        obj.setdefault("names", []).append({"name": camel(h), "kind": "class", "home": h})
    return [f"map: names row added for the mixin class {camel(h)} (kind class, home {h})" for h in added]


def _installed_flag(plan: Plan, obj: dict) -> list:
    fam = obj.get("family")
    if not (isinstance(fam, dict) and "installed" in fam):
        return ["map: family.installed not touched (the map has no `family.installed` key)"]
    if plan.stats["sel"]:
        return ["map: family.installed left as it is (--homes cuts only some parts, the facade is not the installed one)"]
    if fam["installed"] is True:
        return ["map: family.installed is already true"]
    fam["installed"] = True
    return ["map: family.installed set to true (the facade installs the parts)"]


def _test_rows(plan: Plan, obj: dict) -> list:
    tests = plan.stats["pkg"] / plan.cfg["tests_dir"]
    skip, needles, out = _l8_skip(plan), _family_file_names(plan), []
    for path, text in sorted(plan.carriers.items(), key=lambda p: str(p[0])):
        if path.parent == tests and path.suffix == ".py" and path.name not in skip:
            out += reconcile_rows(obj, path.name, text, needles)
    return out


def _patch_array(text: str, key: str, old: list | None, new: list | None):
    """Rewrite one top-level array of a map laid out one object per line (` "<key>": [`, `  {...},`, ` ]`), changing only the
    lines of rows that changed; None when the array is not in that layout."""
    if old is None or new is None:
        return None
    pat = re.compile(r'^ "' + re.escape(key) + r'": \[\n((?:  \{.*\},?\n)*) \](,?)$', re.M)
    inline = re.compile(r'^ "' + re.escape(key) + r'": (\[.*\])(,?)$', re.M)
    m, pool = pat.search(text), []
    if m:
        pool = [(json.loads(x.strip().rstrip(",")), x.rstrip(",")) for x in m.group(1).splitlines()]
    else:
        m = inline.search(text)
        if not m:
            return None
        if json.loads(m.group(1)) != old:
            return None
        pool = [(r, "  " + json.dumps(r, ensure_ascii=False)) for r in old]
    if [r for r, _l in pool] != old:
        return None
    body = []
    for row in new:
        at = next((i for i, (r, _l) in enumerate(pool) if r == row), None)
        body.append(pool.pop(at)[1] if at is not None else "  " + json.dumps(row, ensure_ascii=False))
    rep = f' "{key}": [\n' + ",\n".join(body) + f"\n ]{m.group(2)}" if body else f' "{key}": []{m.group(2)}'
    return text[:m.start()] + rep + text[m.end():]


def _patch_map_text(text: str, old: dict, new: dict):
    for key in ("names", "source_readers", "source_mentions"):
        if new.get(key) != old.get(key):
            text = _patch_array(text, key, old.get(key), new.get(key))
            if text is None:
                return None
    if new.get("family") != old.get("family"):
        text, n = re.subn(r'("family"\s*:\s*\{[^{}]*?"installed"\s*:\s*)false', r"\1true", text, count=1)
        if not n:
            return None
    try:
        return text if json.loads(text) == new else None
    except ValueError:
        return None


def map_text_for(raw: bytes, old: dict, new: dict) -> tuple:
    """(the new map text in the file's own newline style, a note or ""): the lines of the changed rows only, else the layout
    json.dumps can reproduce, else the whole file with indent 1 (said in the note)."""
    text = raw.decode("utf-8")
    crlf = "\r\n" in text and text.count("\r\n") == text.count("\n")
    lf = text.replace("\r\n", "\n")
    out, note = _patch_map_text(lf, old, new), ""
    if out is None:
        layout = _json_layout(old, lf)
        if layout is not None:
            out = json.dumps(new, indent=layout[0], ensure_ascii=layout[1]) + layout[2]
        else:
            out, note = json.dumps(new, indent=1, ensure_ascii=False) + "\n", "map: the layout of the file is not one the tool reproduces; the whole file is rewritten with indent 1"
    return (out.replace("\n", "\r\n") if crlf else out), note


def build_map(plan: Plan) -> None:
    """The would-be map: mixin rows, recomputed test rows, family.installed. P5 judges it; write_all writes it."""
    obj = json.loads(json.dumps(plan.mp))
    notes = _mixin_rows(plan, obj) + _test_rows(plan, obj) + _installed_flag(plan, obj)
    plan.map_new = obj
    if obj != plan.mp:
        plan.map_text, note = map_text_for(plan.stats["map_raw"], plan.mp, obj)
        notes += [note] if note else []
    plan.map_notes = notes


# --- carriers -------------------------------------------------------------------------------------------------------------
def _home_of(rows: dict, cls: str, name: str) -> tuple:
    """(home, row key) of a carrier's function name: `<Class>.<name>` before the bare name."""
    for key in ((f"{cls}.{name}" if cls else None), name):
        if key and key in rows:
            return rows[key]["home"], key
    return None, None


@dataclass
class CarrierCtx:
    ffile: str
    facade: str
    cls: str
    rows: dict
    moving: set
    moved_homes: list
    out_rows: list = field(default_factory=list)
    unresolved: list = field(default_factory=list)

    def home_of(self, name: str) -> tuple:
        return _home_of(self.rows, self.cls, name)


def _c_json_file_function(ctx: CarrierCtx, car: dict, text: str) -> str:
    def sub(m):
        obj = m.group(0)
        fm = re.search(r'"file"\s*:\s*"' + re.escape(ctx.ffile) + '"', obj)
        fn = re.search(r'"function"\s*:\s*"([^"]+)"', obj)
        if not (fm and fn):
            return obj
        home, key = ctx.home_of(fn.group(1))
        if home is None:
            ctx.unresolved.append(f"{car['file']}: {ctx.ffile}::{fn.group(1)} names no map row")
            return obj
        if key not in ctx.moving:
            return obj
        ctx.out_rows.append(f"carrier {car['id']} {car['file']}: {ctx.ffile}::{fn.group(1)} -> {home}.py::{fn.group(1)}")
        return obj[:fm.start()] + f'"file": "{home}.py"' + obj[fm.end():]
    return re.sub(r"\{[^{}]*\}", sub, text)


def _c_guard(ctx: CarrierCtx, car: dict, text: str) -> str:
    def sub(m):
        home, key = ctx.home_of(m.group(1))
        if home is None:
            ctx.unresolved.append(f"{car['file']}: {ctx.ffile}::{m.group(1)} names no map row")
            return m.group(0)
        if key not in ctx.moving:
            return m.group(0)
        ctx.out_rows.append(f"carrier {car['id']} {car['file']}: {ctx.ffile}::{m.group(1)} -> {home}.py::{m.group(1)}")
        return f'"{home}.py::{m.group(1)}"'
    return re.sub(r'"' + re.escape(ctx.ffile) + r'::([^"]+)"', sub, text)


def _keyed_class(car: dict, cls: str, home: str) -> str:
    """The class a moved `<Class>.<member>` row names after the cut, by the carrier's declared `class_key`: the split class's
    own name (`assembled`: its reader folds every mixin to it) or the mixin class of the member's home (`mixin`)."""
    return camel(home) if car["class_key"] == "mixin" else cls


def _c_reader(ctx: CarrierCtx, car: dict, text: str) -> str:
    def sub(m):
        key = f"{ctx.cls}.{m.group(1)}"
        if key not in ctx.rows:
            ctx.unresolved.append(f"{car['file']}: {ctx.facade}:{key} names no map row")
            return m.group(0)
        home = ctx.rows[key]["home"]
        if key not in ctx.moving:
            return m.group(0)
        new_cls = _keyed_class(car, ctx.cls, home)
        ctx.out_rows.append(f"carrier {car['id']} {car['file']}: {ctx.facade}:{key} -> {home}:{new_cls}.{m.group(1)}")
        return f'"{home}:{new_cls}.{m.group(1)}"'
    return re.sub(r'"' + re.escape(ctx.facade) + ":" + re.escape(ctx.cls) + r'\.([A-Za-z_]\w*)"', sub, text)


def _py_tuple_key(line: str):
    m = re.match(r"^\s*(\(.*?\))\s*:", line)
    try:
        return ast.literal_eval(m.group(1))
    except Exception:                             # noqa: BLE001
        return None


def _py_tuple_line(ctx: CarrierCtx, car: dict, line: str, pat) -> str:
    m = pat.match(line)
    if not m:
        return line
    qn = m.group(5)
    method = bool(ctx.cls) and qn.startswith(ctx.cls + ".")
    home, key = ctx.home_of(qn.split(".", 1)[1] if method else qn)
    if home is None:
        ctx.unresolved.append(f"{car['file']}: {ctx.ffile} {qn} names no map row")
        return line
    if key not in ctx.moving:
        return line
    new_qn = f"{_keyed_class(car, ctx.cls, home)}.{qn.split('.', 1)[1]}" if method else qn
    ctx.out_rows.append(f"carrier {car['id']} {car['file']}: ({ctx.ffile}, {qn}) -> ({home}.py, {new_qn})")
    return m.group(1) + m.group(2) + home + ".py" + m.group(2) + m.group(3) + m.group(4) + new_qn + m.group(4) + line[m.end():]


def _c_py_tuple(ctx: CarrierCtx, car: dict, text: str) -> str:
    pat = re.compile(r"^(\s*\(\s*)(['\"])" + re.escape(ctx.ffile) + r"\2(\s*,\s*)(['\"])([^'\"]+)\4")
    generic = re.compile(r"^\s*\(\s*['\"][^'\"]*['\"]\s*,.*\)\s*:")
    lines = text.split("\n")
    i = 0
    while i < len(lines):
        if not generic.match(lines[i]):
            i += 1
            continue
        j = i
        while j < len(lines) and generic.match(lines[j]):
            j += 1
        keys = [_py_tuple_key(x) for x in lines[i:j]]
        was_sorted = None not in keys and keys == sorted(keys)
        new_run = [_py_tuple_line(ctx, car, line, pat) for line in lines[i:j]]
        ks = [_py_tuple_key(x) for x in new_run]
        if was_sorted and None not in ks:
            new_run = [x for _k, x in sorted(zip(ks, new_run), key=lambda p: p[0])]
        lines[i:j] = new_run
        i = j
    return "\n".join(lines)


def _json_layout(obj, text: str):
    for indent in (None, 1, 2, 4):
        for ea in (True, False):
            for tail in ("\n", ""):
                if json.dumps(obj, indent=indent, ensure_ascii=ea) + tail == text:
                    return indent, ea, tail
    return None


def _c_covers(ctx: CarrierCtx, car: dict, text: str) -> str:
    obj = json.loads(text)
    layout = _json_layout(obj, text)
    if layout is None:
        ctx.unresolved.append(f"{car['file']}: the file does not round-trip through json, the covers append cannot keep its layout")
        return text
    added = 0
    for row in (obj.get(car["section"]) or {}).values():
        lst = row.get(car["list"]) if isinstance(row, dict) else None
        if isinstance(lst, list) and ctx.ffile in lst:
            at = lst.index(ctx.ffile) + 1
            for h in ctx.moved_homes:
                if f"{h}.py" not in lst:
                    lst.insert(at, f"{h}.py")
                    at += 1
            added += 1
    ctx.out_rows.append(f"carrier {car['id']} {car['file']}: {added} {car['section']} rows gain {len(ctx.moved_homes)} modules each")
    return json.dumps(obj, indent=layout[0], ensure_ascii=layout[1]) + layout[2]


def _c_py_triple(ctx: CarrierCtx, car: dict, text: str) -> str:
    """A list/set-literal row `('<file>', '<function>', '<tag>'),`: the FILE changes. A run of rows (comment-only lines
    between them allowed; a comment block belongs to the row BELOW it and travels with it) that was sorted before is sorted
    after, because a reader may compare it with `sorted(...)`; a run that was not sorted keeps its order."""
    pat = re.compile(r"^(\s*\(\s*)(['\"])" + re.escape(ctx.ffile) + r"\2(\s*,\s*)(['\"])([^'\"]+)\4(\s*,)")
    row = re.compile(r"^\s*\(\s*(['\"])[^'\"]*\1\s*,\s*(['\"])[^'\"]*\2\s*,\s*(['\"])[^'\"]*\3\s*\)\s*,")

    def rewrite(line: str) -> str:
        m = pat.match(line)
        if not m:
            return line
        home, key = ctx.home_of(m.group(5))
        if home is None:
            ctx.unresolved.append(f"{car['file']}: {ctx.ffile} {m.group(5)} names no map row")
            return line
        if key not in ctx.moving:
            return line
        ctx.out_rows.append(f"carrier {car['id']} {car['file']}: ({ctx.ffile}, {m.group(5)}) -> ({home}.py, {m.group(5)})")
        return m.group(1) + m.group(2) + home + ".py" + line[m.end(2) + len(ctx.ffile):]      # the rest starts at the closing quote

    def key_of(line: str):
        try:
            return ast.literal_eval(re.match(r"^\s*(\(.*\))\s*,", line).group(1))
        except Exception:                             # noqa: BLE001
            return None

    lines = text.split("\n")
    out, i = [], 0
    while i < len(lines):
        if not (row.match(lines[i]) or lines[i].lstrip().startswith("#")):
            out.append(lines[i])
            i += 1
            continue
        j = i
        while j < len(lines) and (row.match(lines[j]) or lines[j].lstrip().startswith("#")):
            j += 1
        items, pending = [], []
        for line in lines[i:j]:
            if row.match(line):
                items.append((pending, line))
                pending = []
            else:
                pending.append(line)
        keys = [key_of(x[1]) for x in items]
        was_sorted = None not in keys and keys == sorted(keys)
        new_items = [(c, rewrite(r)) for c, r in items]
        if was_sorted and any(a[1] != b[1] for a, b in zip(items, new_items)):
            new_keys = [key_of(x[1]) for x in new_items]
            if None not in new_keys:
                new_items = [x for _k, x in sorted(zip(new_keys, new_items), key=lambda p: p[0])]
        for c, r in new_items:
            out.extend(c)
            out.append(r)
        out.extend(pending)
        i = j
    return "\n".join(out)


CARRIER_FORMS = {"json-file-function": _c_json_file_function, "guard": _c_guard, "reader": _c_reader,
                 "py-tuple": _c_py_tuple, "py-triple": _c_py_triple, "covers-append": _c_covers}


def _class_key_refusals(plan: Plan) -> bool:
    """R18: a tool carrier of a class-qualified form with no (or an unknown) `class_key` is refused; True when any was."""
    bad = False
    for car in plan.cfg["carriers"]:
        if car.get("who") == "tool" and car.get("form") in CLASS_KEYED_FORMS and car.get("class_key") not in CLASS_KEYS:
            plan.refuse("R18", f"{CARRIERS_FILE.name} carrier {car.get('id')} {car.get('file')}",
                        f"form {car['form']} has class_key {car.get('class_key')!r}", f"one of {list(CLASS_KEYS)}")
            bad = True
    return bad


def _carrier_pass(plan: Plan, cls: str) -> None:
    st, cfg = plan.stats, plan.cfg
    pkg, repo = st["pkg"], Path(plan.args.repo).resolve()
    if _class_key_refusals(plan):
        return
    ctx = CarrierCtx(plan.facade + ".py", plan.facade, cls, st["rows"], {n for u in st["moving"] for n in u.names},
                     sorted({u.home for u in st["moving"]}))
    for car in cfg["carriers"]:
        if car.get("who") != "tool":
            continue
        path = (repo if car.get("root") == "repo" else pkg) / car["file"]
        if not path.is_file():
            ctx.out_rows.append(f"carrier {car['id']} {car['file']}: absent in this tree")
            continue
        raw = path.read_bytes()
        text = raw.decode("utf-8")
        new = CARRIER_FORMS[car["form"]](ctx, car, text) if car["form"] in CARRIER_FORMS else text
        plan.carrier_sha[path] = sha256(raw)
        plan.carrier_view[path] = new
        if new != text:
            plan.carriers[path] = new
    plan.carrier_rows = ctx.out_rows
    st["carrier_unresolved"] = ctx.unresolved


def _record_at(text: str, pos: int, whole_object: bool) -> str:
    """The carrier record around a position: the enclosing json object, or the physical line."""
    a, b = text.rfind("\n", 0, pos) + 1, text.find("\n", pos)
    line = text[a:(b if b >= 0 else len(text))]
    if not whole_object:
        return line
    depth, i = 0, pos
    while i > 0:
        i -= 1
        if text[i] == "}":
            depth += 1
        elif text[i] == "{":
            if depth == 0:
                break
            depth -= 1
    else:
        return line
    depth = 0
    for j in range(pos, len(text)):
        if text[j] == "{":
            depth += 1
        elif text[j] == "}":
            if depth == 0:
                return text[i:j + 1]
            depth -= 1
    return line


def _leftovers(plan: Plan) -> list:
    """P6 second clause: a carrier record that still names the facade file (or `<facade>:`) together with a moved name."""
    st = plan.stats
    moved = {n for u in st["moving"] for n in u.names}
    tokens = moved | {n.split(".", 1)[1] for n in moved if "." in n}
    ffile = plan.facade + ".py"
    out = []
    for path, text in plan.carrier_view.items():
        hits = [m.start() for m in re.finditer(re.escape(ffile) + "|\"" + re.escape(plan.facade) + ":", text)]
        for pos in hits:
            # a json object is the record only where the file name is the VALUE of a key (`"file": "<facade file>"`)
            keyed = path.suffix == ".json" and re.search(r":\s*\"?$", text[max(0, pos - 8):pos]) is not None
            record = _record_at(text, pos, keyed)
            found = sorted({tok for lit in re.findall(r"[\"']([^\"']+)[\"']", record) for tok in re.split(r"[:,\s]+", lit) if tok in tokens})
            if found:
                line = text.count("\n", 0, pos) + 1
                out.append(f"{path.name}:{line} still names {ffile} with the moved name(s) {found[:4]}")
    return sorted(set(out))


# --- proofs ---------------------------------------------------------------------------------------------------------------
P3_CODE = ("import sys, json, importlib\nsys.path.insert(0, sys.argv[1])\nm = importlib.import_module(sys.argv[2])\n"
           "out = {'mod': sorted(dir(m))}\nif sys.argv[3]:\n    out['cls'] = sorted(dir(getattr(m, sys.argv[3])))\nprint(json.dumps(out))\n")


def _p1_p2(plan: Plan, cls: str) -> None:
    st, cfg, sc = plan.stats, plan.cfg, plan.sc
    marker, pre = cfg["section_marker"], cfg["preamble_calls"]
    moving = [u for u in st["moving"] if u.level in ("module", "class")]
    gen, gen_names, bad, total, equal = {}, [], [], 0, 0
    for h in sorted({u.home for u in moving}):
        text = plan.files[f"{h}.py"]
        g = scan_text(text, _class_re(camel(h), True), cls, marker, pre)
        for u in g.units:
            if u.level != "header":
                gen_names.extend(u.names)
                for n in u.names:
                    gen.setdefault(n, (u, g, text))
    for u in moving:
        total += len(u.names)
        got = gen.get(u.names[0])
        if got is None:
            bad.append(u.label())
            continue
        gu, g, text = got
        before, after = render(u, sc.lines, True), render(gu, g.lines, False)
        grow = sum(len(e[3]) - (e[2] - e[1]) for e in u.edits)
        if sha256(after.encode()) == sha256(before.encode()) and before in text and len(after) - len(render(u, sc.lines, False)) == grow:
            equal += len(u.names)
        else:
            bad.append(u.label())
    plan.proofs.append(("P1", not bad, f"P1 segments: {equal}/{total} equal" + (f"; differ: {bad[:5]}" if bad else "")))
    fscan = scan_text(plan.files[f"{plan.facade}.py"], _class_re(cls, True), cls, marker, pre)
    after_names = Counter(gen_names + [n for u in fscan.units for n in u.names])
    before_names = Counter(n for u in sc.units for n in u.names)
    dup = sorted(n for n, c in after_names.items() if c > 1)
    miss = sorted((before_names - after_names).elements())
    extra = sorted((after_names - before_names).elements())
    ok = after_names == before_names
    plan.proofs.append(("P2", ok, f"P2 census (multiset of every name): {sum(before_names.values())} before, {sum(after_names.values())} after, each name once: {ok}"
                        + ("" if ok else f"; lost {miss[:4]}; extra {extra[:4]}; written twice {dup[:4]}")))


def _p4(plan: Plan) -> None:
    bad = []
    for name, text in plan.files.items():
        try:
            compile(text, name, "exec")
        except SyntaxError as exc:
            bad.append(f"{name}:{exc.lineno}")
    plan.proofs.append(("P4", not bad, f"P4 compile of {len(plan.files)} files: {'ok' if not bad else bad}"))


def _p6(plan: Plan) -> None:
    bad = list(plan.stats.get("carrier_unresolved", [])) + _leftovers(plan)
    n = len([x for x in plan.carrier_rows if "absent in this tree" not in x])
    plan.proofs.append(("P6", not bad, f"P6 carrier pass: {n} carrier lines, {len(plan.carrier_view)} carriers rescanned, unresolved or left behind {bad or 0}"))


def _verify_entry(entry) -> tuple:
    """(args, absent text) of one `verify` entry: a package-relative script (a string) or {"args": [...], "absent": "<text>"}."""
    if isinstance(entry, str):
        return [entry], ""
    return list(entry["args"]), entry.get("absent", "")


def _run_verify(plan: Plan, pkg_after: Path, car: dict, entry, cache: dict) -> tuple:
    """(ok, one line) of one verify command on the would-be tree: `python -B <args>` from the package root of the tree."""
    args, absent = _verify_entry(entry)
    limit = (entry.get("verify_timeout") if isinstance(entry, dict) else None) or plan.cfg.get("verify_timeout", 120)
    shown = " ".join(args)[:90]
    head = f"verify carrier {car['id']} {car['file']}: python -B {shown}"
    if not args[0].startswith("-") and not (pkg_after / args[0]).is_file():
        return False, f"{head} -> the script is not in the would-be tree"
    argv = [sys.executable, "-B"] + ([str(pkg_after / args[0])] + args[1:] if not args[0].startswith("-") else args)
    key = tuple(argv)
    if key not in cache:
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONIOENCODING="utf-8")
        try:
            r = subprocess.run(argv, capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=pkg_after, env=env, timeout=limit)
            cache[key] = (r.returncode, (r.stdout or "") + (r.stderr or ""))
        except subprocess.TimeoutExpired:
            cache[key] = (None, "")
        except OSError as exc:
            cache[key] = (-1, f"cannot start: {exc}")
    code, out = cache[key]
    if code is None:
        return False, f"{head} -> timed out after {limit} s (a timeout is a failed proof)"
    tail = [x for x in out.splitlines() if x.strip()]
    closing = tail[-1].strip()[:160] if tail else "(no output)"
    if code != 0:
        fails = [x.strip()[:400] for x in out.splitlines() if x.lstrip().startswith("FAIL")][:3]
        return False, f"{head} -> exit {code}; closing line: {closing}" + "".join(f"\n      {x}" for x in fails)
    if absent and absent in out:
        return False, f"{head} -> exit 0 but the output holds {absent!r}; closing line: {closing}"
    return True, f"{head} -> exit 0; closing line: {closing}"


def _p6_verify(plan: Plan, after: Path) -> None:
    """P6, the proof the carriers still work: every `verify` of a tool carrier is RUN on the would-be tree, and the line of
    each (or of its absence) is appended to P6. A carrier whose file is absent in the tree has nothing to prove."""
    pkg_after, lines, bad, cache = after / plan.cfg["package_root"], [], [], {}
    for car in plan.cfg["carriers"]:
        if car.get("who") != "tool":
            continue
        path = plan.stats["pkg"] / car["file"] if car.get("root") != "repo" else Path(plan.args.repo).resolve() / car["file"]
        if not path.is_file():
            lines.append(f"verify carrier {car['id']} {car['file']}: the carrier file is absent in this tree, nothing to run")
        elif not car.get("verify"):
            lines.append(f"verify carrier {car['id']} {car['file']}: no verify declared")
        else:
            for entry in car["verify"]:
                ok, line = _run_verify(plan, pkg_after, car, entry, cache)
                lines.append(line)
                if not ok:
                    bad.append(line)
    text = "\n    " + "\n    ".join(lines) if lines else ""
    at = next((i for i, p in enumerate(plan.proofs) if p[0] == "P6"), None)
    if at is None:
        plan.proofs.append(("P6", not bad, "P6 carrier verify:" + text))
    else:
        _id, ok, old = plan.proofs[at]
        plan.proofs[at] = ("P6", ok and not bad, old + text)


def _long(path: Path) -> str:
    """An absolute path in the extended-length form on Windows (no 260-character limit), unchanged elsewhere."""
    s = str(Path(path).resolve())
    return "\\\\?\\" + s if os.name == "nt" and not s.startswith("\\\\?\\") else s


def _build_trees(plan: Plan, tmp: Path) -> tuple:
    """Two trees of identical layout: the whole package root before, and the same with the generated files after."""
    st, cfg = plan.stats, plan.cfg
    pkg, scripts_dir, repo = st["pkg"], st["scripts_dir"], Path(plan.args.repo).resolve()
    ignore = shutil.ignore_patterns("__pycache__", "*.pyc", ".git")
    before, after = tmp / "before", tmp / "after"
    try:
        for root in (before, after):
            shutil.copytree(_long(pkg), _long(root / cfg["package_root"]), ignore=ignore)      # deep fixture paths pass MAX_PATH on Windows
        sd = after / cfg["package_root"] / scripts_dir.relative_to(pkg)
        for name, text in plan.files.items():
            (sd / name).write_bytes(text.replace("\n", plan.src.nl).encode("utf-8"))
        for path, text in plan.carriers.items():
            target = after / path.relative_to(repo)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(text.encode("utf-8"))
        if plan.map_text is not None:                  # the would-be map is a carrier of its own cut: a verify command reads it
            try:
                target = after / Path(plan.args.map_path).resolve().relative_to(repo)
            except ValueError:
                target = None
            if target is not None:
                target.write_bytes(plan.map_text.encode("utf-8"))
    except (OSError, shutil.Error) as exc:
        raise Cannot(f"cannot build the proof trees under {tmp}: {exc}")
    return before, after


def _sd(plan: Plan, tree: Path) -> Path:
    return tree / plan.cfg["package_root"] / plan.stats["scripts_dir"].relative_to(plan.stats["pkg"])


def _p3(plan: Plan, cls: str, before: Path, after: Path, tmp: Path) -> None:
    P, fmod, facade = plan.proofs, plan.cfg["facade"]["module"], plan.facade
    fpath = _sd(plan, after) / f"{fmod}.py"
    if not fpath.is_file():
        P.append(("P3", None, f"P3 not run: the facade module {fmod}.py is not in the tree"))
        return
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONIOENCODING="utf-8")
    res = []
    for tree in (before, after):
        r = subprocess.run([sys.executable, "-B", "-I", "-c", P3_CODE, str(_sd(plan, tree)), facade, cls], capture_output=True, text=True,
                           cwd=tmp, env=env, timeout=60)
        res.append(json.loads(r.stdout.strip().splitlines()[-1]) if r.returncode == 0 and r.stdout.strip() else {"err": r.stderr[-300:]})
    if "err" in res[0] or "err" in res[1]:
        P.append(("P3", False, f"P3 import failed: before {res[0].get('err', 'ok')} after {res[1].get('err', 'ok')}"))
        return
    lost = sorted(set(res[0]["mod"]) - set(res[1]["mod"]))
    same = res[0].get("cls") == res[1].get("cls")
    note = " [stand-in module_facade]" if fpath.read_text(encoding="utf-8") == STAND_IN else ""
    P.append(("P3", not lost and same, f"P3 facade import in two trees of identical layout{note}: dir(module) lost {lost[:5] or 'nothing'}; dir({cls}) equal: {same}"))


def _p5(plan: Plan, after: Path) -> None:
    lt = _find_check(plan, plan.cfg["layer_test"]["file"])
    if lt is None:
        plan.proofs.append(("P5", None, "P5 not run: the layer test file is absent"))
        return
    pkg_after = after / plan.cfg["package_root"]
    try:
        mod = _layer_module(plan)
        probs = getattr(mod, plan.cfg["layer_test"]["entry"])(pkg_after, plan.map_new or plan.mp, tests_dir=pkg_after / plan.cfg["tests_dir"])["problems"]
        left = {k: v for k, v in probs.items() if v}
        plan.proofs.append(("P5", not left, f"P5 layer test on the result tree: {'L1-L10 empty' if not left else {k: v[:2] for k, v in left.items()}}"))
    except Exception as exc:                  # noqa: BLE001
        plan.proofs.append(("P5", False, f"P5 layer test failed to run: {type(exc).__name__}: {exc}"))


class _Flakes:
    """A pyflakes reporter that only counts, by message class; a message caused by a K7 setup line the tool added
    (`k7`: file -> line numbers) is counted apart in `exempt`, not in `counts`."""

    def __init__(self, k7: dict | None = None):
        self.counts: dict = {}
        self.exempt = 0
        self.k7 = k7 or {}

    def _bump(self, name: str) -> None:
        self.counts[name] = self.counts.get(name, 0) + 1

    def unexpectedError(self, filename, msg):
        self._bump("UnexpectedError")

    def syntaxError(self, filename, msg, lineno, offset, text):
        self._bump("SyntaxError")

    def _from_k7(self, message) -> bool:
        lines = self.k7.get(getattr(message, "filename", ""), ())
        kind = type(message).__name__
        if kind == "UnusedImport":
            return message.lineno in lines
        if kind == "RedefinedWhileUnused":
            return message.lineno in lines or (len(message.message_args) > 1 and message.message_args[1] in lines)
        return False

    def flake(self, message):
        if self._from_k7(message):
            self.exempt += 1
        else:
            self._bump(type(message).__name__)


def _flake_counts(texts: list, setup: str | None = None) -> tuple:
    """(counts by message class, messages exempt because a K7 setup line the tool added caused them)."""
    try:
        import pyflakes.api
    except ImportError as exc:
        raise NotRun(f"pyflakes cannot be imported ({exc})")
    mark = k7_line(setup) if setup else None
    k7 = {name: {i + 1 for i, ln in enumerate(text.split("\n")) if ln == mark} for name, text in texts} if mark else {}
    rep = _Flakes(k7)
    for name, text in texts:
        pyflakes.api.check(text, name, rep)
    return rep.counts, rep.exempt


def _tool_module(name: str):
    if str(TOOLS_DIR) not in sys.path:
        sys.path.insert(0, str(TOOLS_DIR))
    try:
        return importlib.import_module(name)
    except Exception as exc:                  # noqa: BLE001
        raise NotRun(f"{name} cannot be imported ({type(exc).__name__}: {exc})")


def _dup_groups(tree: Path) -> int:
    mod = _tool_module("dup_ratchet")
    total = 0
    try:
        for name, (paths, exclude) in mod.define_scopes(tree, None).items():
            if mod.dup_report.resolve_files(tree, paths, exclude):
                for run in mod.analyse_scopes(tree, {name: (paths, exclude)}):
                    total += len(run.rep["groups"])
    except Exception as exc:                  # noqa: BLE001
        raise NotRun(f"the dup analysis cannot run ({type(exc).__name__}: {exc})")
    return total


def _census_counts(plan: Plan, tree: Path):
    """(class counts, blocking_per_role) the census test computes on one tree; None when the tree has no census data."""
    cfg = plan.cfg["census_test"]
    data = tree / plan.cfg["package_root"] / cfg["data"]
    if not data.is_file():
        return None
    path = _find_check(plan, cfg["file"])
    if path is None:
        raise NotRun("the census test file is absent")
    try:
        mod = _load_module(path, "_census_check")
        totals = getattr(mod, cfg["entry"])(tree / plan.cfg["package_root"], json.loads(data.read_text(encoding="utf-8")))["totals"]
    except Exception as exc:                  # noqa: BLE001
        raise NotRun(f"the census analysis cannot run ({type(exc).__name__}: {exc})")
    return dict(totals["counts"]), dict(totals["blocking_per_role"])


def _growth(label: str, before, after) -> list:
    if isinstance(before, dict):
        return [f"{label} {k}: {before.get(k, 0)} -> {v}" for k, v in sorted(after.items()) if v > before.get(k, 0)]
    return [f"{label}: {before} -> {after}"] if after > before else []


def _p7(plan: Plan, before: Path, after: Path) -> None:
    try:
        b_src = (before / plan.cfg["package_root"] / plan.src.rel).read_text(encoding="utf-8")
        lint_b, _none = _flake_counts([(plan.src.rel, b_src)])
        lint_a, exempt = _flake_counts(list(plan.files.items()), plan.mp.get("setup_import"))
        lint = (lint_b, lint_a)
        dup =(_dup_groups(before), _dup_groups(after))
        cen = (_census_counts(plan, before), _census_counts(plan, after))
    except NotRun as exc:
        plan.proofs.append(("P7", None, f"P7 not run: {exc}"))
        return
    grown = _growth("pyflakes", *lint) + _growth("dup groups", *dup)
    if cen[0] is not None and cen[1] is not None:
        grown += _growth("census class", cen[0][0], cen[1][0]) + _growth("census blocking_per_role", cen[0][1], cen[1][1])
    cen_note = "census absent in this tree" if cen[0] is None else f"census counts {sum(cen[0][0].values())}={sum(cen[1][0].values())}"
    plan.proofs.append(("P7", not grown, f"P7 computed on both trees: pyflakes {sum(lint[0].values())}->{sum(lint[1].values())}, dup groups {dup[0]}->{dup[1]}, {cen_note}; "
                        f"P7: {exempt} messages from K7 setup lines exempt" + (f"; GREW: {grown[:6]}" if grown else "")))


def _tree_proofs(plan: Plan, cls: str) -> None:
    tmp = Path(tempfile.mkdtemp(prefix="ss"))
    try:
        before, after = _build_trees(plan, tmp)
        _p6_verify(plan, after)
        _p3(plan, cls, before, after, tmp)
        _p5(plan, after)
        _p7(plan, before, after)
    finally:
        shutil.rmtree(_long(tmp), ignore_errors=True)


def _p8(plan: Plan) -> None:
    st = plan.stats
    left = st.get("k7_left")
    if left is None:
        plan.proofs.append(("P8", None, f"P8 not run: {st.get('k7_why') or 'K7 not evaluated'}"))
    else:
        plan.proofs.append(("P8", not left, "P8 K7 residue after the added lines (parts and facade): "
                            + ("empty" if not left else "; ".join(f"{n} {v[:6]}" for n, v in sorted(left.items())))))


def run_proofs(plan: Plan, cls: str) -> None:
    _p1_p2(plan, cls)
    _p4(plan)
    _p6(plan)
    _tree_proofs(plan, cls)
    _p8(plan)
    plan.proofs.sort(key=lambda p: p[0])


# --- report ---------------------------------------------------------------------------------------------------------------
def dropped_comments(plan: Plan) -> dict:
    """{source line: text} of every comment line no generated file carries, from the scan and the facade build."""
    sc, out = plan.sc, {}
    for a, b in sc.spans:
        for ln in range(a, b + 1):
            if sc.lines[ln - 1].strip():
                out[ln] = sc.lines[ln - 1].strip()
    out.update(plan.stats.get("facade_dropped", {}))
    return out


def _report_homes(plan: Plan) -> list:
    st, sc, out = plan.stats, plan.sc, []
    out.append("homes (rank order):")
    homes = sorted({u.home for u in sc.units + sc.strays if u.home}, key=lambda h: (st["rank"].get(h, 0), st["order"].get(h, 0)))
    for h in homes:
        us = [u for u in sc.units + sc.strays if u.home == h and u.level != "header"]
        f, m, c = _kind_counts(us)
        lines = sum(u.end - u.start + 1 for u in us if u.moves)
        imports = len([x for x in plan.files[f"{h}.py"].split("\n") if re.match(r"^(import|from) ", x)]) if f"{h}.py" in plan.files else 0
        tag = "stays" if h == plan.facade else "new" if f"{h}.py" in plan.files else "selected out" if st["sel"] and h not in st["sel"] else "exists"
        out.append(f"  {h}: {sum(len(u.names) for u in us)} names ~{lines} lines ({f} funcs, {m} methods, {c} consts), imports {imports} [{tag}]")
    for h in sorted(st["existing"]):
        out.append(f"  {h}: already out ({len(st['existing'][h])} names in the module)")
    dropped = dropped_comments(plan)
    out.append(f"dropped comment lines (no generated file carries them): {len(dropped)}")
    out += [f"  {plan.src.rel}:{ln}: {dropped[ln][:100]}" for ln in sorted(dropped)]
    return out


def _report_tail(plan: Plan) -> list:
    st, out = plan.stats, []
    out += ["  " + x for x in plan.carrier_rows]
    out += ["  UNRESOLVED " + x for x in st.get("carrier_unresolved", [])]
    tests = st.get("pkg", Path(".")) / plan.cfg["tests_dir"]
    if tests.is_dir():
        pat = re.compile(r"\b" + re.escape(plan.facade) + r"\.(?!py\b)(\w+)")
        hits = {p.name: len(pat.findall(p.read_text(encoding="utf-8", errors="replace"))) for p in tests.rglob("*.py")}
        out.append(f"facade reads `{plan.facade}.<x>` in the tests: {sum(hits.values())} in {sum(1 for v in hits.values() if v)} files")
    out.append("hand/integrator carrier rows: " + "; ".join(f"{c['id']} {c['file']} ({c['who']})" for c in plan.cfg["carriers"] if c["who"] != "tool"))
    out.append("glob censuses over the package scripts:")
    for c in plan.cfg["censuses"]:
        out.append(f"  {c['id']} {c['site']}: keyed by file name: {'yes' if c['keyed_by_file'] else 'no'}; carrier row: {c['carrier_row'] or 'none'}; {c['verdict']}")
    return out


def report(plan: Plan) -> str:
    a, st, out = plan.args, plan.stats, []
    out.append(f"source_split: {a.source} class {a.cls or '-'} mode {'apply' if a.apply else 'dry-run'}")
    if plan.src is not None:
        out.append(f"source sha256: {plan.src.sha} (newline {'CRLF' if plan.src.nl == chr(13) + chr(10) else 'LF'})")
    out.append(f"map sha256: {st.get('map_sha')} ({st.get('map_rel')})")
    if "moving" in st and plan.sc is not None:
        out += _report_homes(plan)
    out.append(f"refusals: {len(plan.refusals)}")
    out += ["  " + r.line() for r in sorted(plan.refusals, key=lambda r: (int(r.code[1:]), r.where))]
    out.append(f"rewrites: {len(plan.rewrites)}")
    out += ["  " + x for x in plan.rewrites]
    out += st.get("k7", []) + plan.warnings
    out += plan.map_notes
    unused = st.get("facade_unused", [])
    out.append(f"kept (unused, possible side effect): {len(unused)}")
    out += ["  " + x for x in unused]
    out += _report_tail(plan)
    for _id, ok, text in plan.proofs:
        out.append(("PASS " if ok else "NOT RUN " if ok is None else "FAIL ") + text)
    out.append(result_line(plan))
    return "\n".join(out)


def _failed_ids(plan: Plan) -> list:
    return [i for i, ok, _t in plan.proofs if ok is False]


def _not_run_ids(plan: Plan) -> list:
    return [i for i, ok, _t in plan.proofs if ok is None]


def failed(plan: Plan) -> bool:
    return bool(_failed_ids(plan)) or (plan.args.apply and bool(_not_run_ids(plan)))


def result_line(plan: Plan) -> str:
    if plan.refusals:
        return f"result: refused ({len(plan.refusals)} refusals), nothing written, exit 2"
    if plan.nothing:
        return "result: nothing to do, exit 0"
    if _failed_ids(plan):
        return f"result: a proof failed ({', '.join(_failed_ids(plan))}), nothing written, exit 2"
    nr = _not_run_ids(plan)
    if nr and plan.args.apply:
        return f"result: {', '.join(nr)} not run, so --apply refuses, nothing written, exit 2"
    tail = f" ({', '.join(nr)} not run)" if nr else ""
    return "result: " + ("applied" if plan.done else f"would apply{tail} (dry-run writes nothing)") + ", exit 0"


# --- the write ------------------------------------------------------------------------------------------------------------
def _unlink(path: Path) -> None:
    try:
        path.unlink()
    except OSError:
        pass


def _rollback(done: list) -> list:
    left = []
    for path, prev in reversed(done):
        try:
            if prev is None:
                path.unlink()
            else:
                path.write_bytes(prev)
        except OSError as exc:
            left.append(f"{path.name} ({exc})")
    return left


def _replace_all(targets: list) -> None:
    """Every file to a temp name beside its target first, then `os.replace` in the given order; any failure undoes the
    replacements already made and ends as WriteFailed."""
    temps, done = [], []
    try:
        for path, data in targets:
            tmp = path.with_name(path.name + f".tmp{os.getpid()}")
            temps.append((tmp, path))
            tmp.write_bytes(data)
        for tmp, path in temps:
            prev = path.read_bytes() if path.exists() else None
            os.replace(tmp, path)
            done.append((path, prev))
    except OSError as exc:
        for tmp, _p in temps:
            _unlink(tmp)
        left = _rollback(done)
        raise WriteFailed(f"the write failed ({exc}); {len(done)} file(s) were replaced and are rolled back"
                          + (f"; could NOT restore {left}" if left else "") + ": nothing is written")


def write_all(plan: Plan) -> None:
    sd, src = plan.stats["scripts_dir"], plan.src
    if sha256(src.path.read_bytes()) != src.sha:
        raise WriteFailed("the source changed while the plan was computed: nothing written; re-run")
    for path in plan.carriers:
        if not path.is_file() or sha256(path.read_bytes()) != plan.carrier_sha[path]:
            raise WriteFailed(f"the carrier {path.name} changed between the plan and the write: nothing written; re-run")
    targets = [(sd / name, text.replace("\n", src.nl).encode("utf-8")) for name, text in plan.files.items()]    # parts, then the facade
    targets += [(path, text.encode("utf-8")) for path, text in plan.carriers.items()]
    if plan.map_text is not None:                  # the map, last: it is part of the same atomic write and of its rollback
        mp = Path(plan.args.map_path)
        if not mp.is_file() or sha256(mp.read_bytes()) != plan.stats["map_sha"]:
            raise WriteFailed(f"the map {mp.name} changed between the plan and the write: nothing written; re-run")
        targets.append((mp, plan.map_text.encode("utf-8")))
    _replace_all(targets)
    plan.done = True


def run(argv: list) -> tuple:
    ap = argparse.ArgumentParser(prog="source_split.py", description=__doc__.split("\n")[0])
    ap.error = lambda message: (_ for _ in ()).throw(Cannot(message))   # exit 1, not argparse's 2
    ap.add_argument("--map")
    ap.add_argument("--source")
    ap.add_argument("--class", dest="cls", default="")
    ap.add_argument("--homes", default="")
    ap.add_argument("--repo", default=".")
    ap.add_argument("--report", default="")
    ap.add_argument("--selftest", action="store_true")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--dry-run", action="store_true")
    g.add_argument("--apply", action="store_true")
    ns = ap.parse_args(argv)
    if ns.selftest:
        return selftest(), ""
    if not (ns.map and ns.source and (ns.dry_run or ns.apply)):
        raise Cannot("--map, --source and one of --dry-run / --apply are required")
    args = Args(Path(ns.map), ns.source, ns.cls, [h for h in ns.homes.split(",") if h], ns.apply, Path(ns.repo), ns.report)
    plan = make_plan(args)
    if not plan.refusals and not plan.nothing and plan.files:
        run_proofs(plan, ns.cls)
    code = 2 if (plan.refusals or failed(plan)) else 0
    if code == 0 and ns.apply and not plan.nothing:
        write_all(plan)
    text = report(plan)
    if ns.report:
        Path(ns.report).write_text(text + "\n", encoding="utf-8")
    return code, text


# --- selftest -------------------------------------------------------------------------------------------------------------
FIXTURE = '''"""Fixture module docstring."""
import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

LIMIT = 3
LABEL = "x"


class Person(Exception):
    pass


def helper(x):
    return json.dumps(x)


class __CLS__:
    # the size of a thing
    SIZE = LIMIT + 1

    def __init__(self):
        pass

    def low(self):
        return os.sep

    @staticmethod
    def pure(x):
        return helper(x) + str(__CLS__.SIZE)

    def top(self):
        return self.low() + LABEL


def main():
    return __CLS__().top()


if __name__ == "__main__":
    sys.exit(main())
'''
STAND_IN = "def install(name, parts):\n    import sys\n    mod = sys.modules[name]\n    for p in parts:\n        for k, v in vars(p).items():\n            mod.__dict__.setdefault(k, v)\n"
EM = "\u2014"


def _fx(tmp: Path, cfg: dict, source=None, edit=None, tests=None, extra=None, raw=None, map_name="map.json", layers=None,
        facade_mod=True, pkg_files=None):
    sf, cls, pre = cfg["selftest"]["source"], cfg["selftest"]["class"], cfg["selftest"]["prefix"]
    facade = Path(sf).stem
    core, dialog = pre + "core", pre + "dialog"
    pkg = tmp / cfg["package_root"]
    sd = pkg / Path(sf).parent
    sd.mkdir(parents=True)
    text = (source or FIXTURE).replace("__CLS__", cls)
    (pkg / sf).write_bytes(raw if raw is not None else text.encode("utf-8"))
    if facade_mod:
        (sd / (cfg["facade"]["module"] + ".py")).write_text(STAND_IN, encoding="utf-8")
    for rel, body in (extra or {}).items():
        (sd / rel).write_bytes(body.encode("utf-8"))
    for rel, body in (pkg_files or {}).items():
        (pkg / rel).parent.mkdir(parents=True, exist_ok=True)
        (pkg / rel).write_bytes(body.replace("__FACADE__", facade).encode("utf-8"))
    for rel, body in (tests or {}).items():
        (pkg / cfg["tests_dir"]).mkdir(parents=True, exist_ok=True)
        (pkg / cfg["tests_dir"] / rel).write_text(body.replace("__CLS__", cls).replace("__FACADE__", facade), encoding="utf-8")
    row = lambda n, k, h: {"name": n, "kind": k, "home": h}   # noqa: E731
    names = [row("HERE", "const", core), row("LIMIT", "const", core), row("LABEL", "const", dialog), row("Person", "class", core),
             row("helper", "func", core), row(cls, "class", facade), row(cls + ".SIZE", "classconst", core), row(cls + ".__init__", "method", core),
             row(cls + ".low", "method", core), row(cls + ".pure", "staticmethod", dialog), row(cls + ".top", "method", dialog),
             row("main", "func", facade), row(camel(core), "class", core), row(camel(dialog), "class", dialog)]
    mp = {"schema": 1, "family": {"facade": facade, "prefix": pre, "class": cls, "cut": "mixins", "installed": False},
          "layers": layers or [[core], [dialog], [facade]], "names": names, "attributes": [], "adhoc_attributes": [],
          "state_keys": [], "dynamic_state_keys": [], "string_dispatch": [], "exceptions": [], "source_readers": [], "source_mentions": [],
          "stdout_writers": [], "not_driver": []}
    if edit:
        edit(mp)
    mpath = tmp / map_name
    mpath.write_text(json.dumps(mp), encoding="utf-8")
    return Args(mpath, sf, cls, [], False, tmp), mp


class T:
    """The selftest's context: one fixture tree per case; results are (label, ok, detail)."""

    def __init__(self):
        self.cfg = load_cfg()
        self.cls, self.pre = self.cfg["selftest"]["class"], self.cfg["selftest"]["prefix"]
        self.facade = Path(self.cfg["selftest"]["source"]).stem
        self.core, self.dialog = self.pre + "core", self.pre + "dialog"
        self.results: list = []

    def ok(self, label: str, cond, detail="") -> None:
        self.results.append((label, bool(cond), str(detail)[:400]))

    @staticmethod
    def tree():
        return tempfile.TemporaryDirectory(ignore_cleanup_errors=True)

    def plan(self, tmp, **kw) -> Plan:
        args, _mp = _fx(Path(tmp), self.cfg, **kw)
        return make_plan(args)

    def proven(self, tmp, **kw) -> Plan:
        plan = self.plan(tmp, **kw)
        if not plan.refusals and not plan.nothing and plan.files:
            run_proofs(plan, self.cls)
        return plan

    def cli_args(self, tmp, mode: str, args: Args, extra=()) -> tuple:
        return run(["--map", str(args.map_path), "--source", args.source, "--class", self.cls, mode, "--repo", str(tmp), *extra])

    def refusal(self, label: str, code: str, needle: str, **kw) -> None:
        with self.tree() as t:
            plan = self.plan(t, **kw)
            hit = [r for r in plan.refusals if r.code == code and needle in r.line()]
            self.ok(f"{code} {label}: reported by name ({needle!r})", hit, "; ".join(r.line()[:150] for r in plan.refusals[:2]))

    def row(self, name, kind, home) -> dict:
        return {"name": name, "kind": kind, "home": home}

    def rows(self, *rows):
        return lambda m: m["names"].extend(self.row(*r) for r in rows)

    def edits(self, *fns):
        return lambda m: [f(m) for f in fns]

    def ins(self, add: str) -> str:
        return FIXTURE.replace("class __CLS__:", add + "\n\n\nclass __CLS__:", 1)

    @staticmethod
    def proof(plan: Plan, pid: str):
        return next((ok for i, ok, _t in plan.proofs if i == pid), "absent")

    @staticmethod
    def snap(root) -> dict:
        return {str(p): sha256(p.read_bytes()) for p in Path(root).rglob("*") if p.is_file()}


def _cases_refusals(t: T) -> None:
    core, dialog, cls, pre = t.core, t.dialog, t.cls, t.pre
    t.refusal("a name with no row", "R1", "extra", source=FIXTURE + "\n\ndef extra():\n    return 1\n")
    t.refusal("a row whose name is gone", "R2", "ghost", edit=t.rows(("ghost", "func", core)))
    t.refusal("a name defined twice", "R3", "helper", source=FIXTURE + "\n\ndef helper(x):\n    return x\n")
    t.refusal("a free name of a higher home", "R4", "LABEL", source=FIXTURE.replace("return os.sep", "return os.sep + LABEL"))
    t.refusal("a free name that resolves to nothing", "R5", "mystery", source=FIXTURE.replace("return os.sep", "return mystery()"))
    t.refusal("a same-rank import cycle", "R6", "->", source=FIXTURE + "\n\ndef fa():\n    return fb()\n\n\ndef fb():\n    return fa()\n",
              edit=t.edits(t.rows(("fa", "func", core), ("fb", "func", pre + "twin")), lambda m: m.update(layers=[[core, pre + "twin"], [dialog], [t.facade]])))
    t.refusal("a class-body use of a name homed elsewhere", "R7", "SIZE", source=FIXTURE.replace("    def __init__", "    BIG = SIZE + 1\n\n    def __init__"),
              edit=t.rows((cls + ".BIG", "classconst", dialog)))
    t.refusal("a target module half-written", "R8", pre + "core.py", extra={pre + "core.py": "FOO = 1\n"})
    t.refusal("mixed newlines", "R9", "newline", raw=FIXTURE.replace("__CLS__", cls).replace("\nLABEL", "\r\nLABEL").encode())
    t.refusal("non-UTF-8 source", "R9", "UTF-8", raw=b"X = '\xff'\n")
    t.refusal("a source with a BOM", "R9", "byte order mark", raw=b"\xef\xbb\xbf" + FIXTURE.replace("__CLS__", cls).encode())
    t.refusal("non-ASCII generated text", "R9", "ASCII", map_name="map-\u00e9.json")
    t.refusal("a module-level statement with no place", "R10", "print", source=FIXTURE.replace("LIMIT = 3", "LIMIT = 3\nprint('x')"))
    t.refusal("targets of one statement in different homes", "R11", "PA", source=FIXTURE.replace("LIMIT = 3", "LIMIT = 3\nPA, PB = 1, 2"),
              edit=t.rows(("PA", "const", core), ("PB", "const", dialog)))
    t.refusal("a free name of facade code", "R12", "mystery", source=FIXTURE.replace("return __CLS__().top()", "return mystery()"))


def _cases_r13(t: T) -> None:
    for label, body in (("setattr", "import __FACADE__ as sr\nsetattr(sr.__CLS__, \"SIZE\", 1)\n"),
                        ("M5 a direct assignment", "import __FACADE__ as sr\nsr.__CLS__.SIZE = 1\n"),
                        ("M5 a patch string target", "from unittest import mock\nmock.patch(\"__FACADE__.__CLS__.SIZE\", 1)\n"),
                        ("M5 patch.multiple", "from unittest import mock\nimport __FACADE__ as sr\nmock.patch.multiple(sr.__CLS__, SIZE=1)\n")):
        t.refusal(f"{label} of a rewritten member on the assembled class", "R13", "SIZE", tests={"test_x.py": body})
    with t.tree() as tmp:
        plan = t.plan(tmp, tests={"test_x.py": "import __FACADE__ as sr\nassert sr.__CLS__.SIZE == 4\n"})
        t.ok("M5 a comparison is not a patch: no R13", not any(r.code == "R13" for r in plan.refusals), [r.line()[:120] for r in plan.refusals])


def _cases_hazards(t: T) -> None:
    core, dialog, cls = t.core, t.dialog, t.cls
    a_src = t.ins("COUNTER = 0\n\n\ndef bump():\n    global COUNTER\n    COUNTER += 1\n    return COUNTER")
    t.refusal("M1 input A: `global` of a name homed in another module", "R14", "COUNTER", source=a_src,
              edit=t.rows(("COUNTER", "const", core), ("bump", "func", dialog)))
    with t.tree() as tmp:
        plan = t.plan(tmp, source=a_src, edit=t.rows(("COUNTER", "const", dialog), ("bump", "func", dialog)))
        t.ok("M1 `global` of a name of the same home is not refused", not any(r.code == "R14" for r in plan.refusals), [r.line()[:120] for r in plan.refusals])
    b_src = t.ins("TABLE = {\"a\": 1}\nTABLE[\"b\"] = 2\nKEYS = sorted(TABLE)")
    t.refusal("M2 input B: a module statement with no name target", "R10", "TABLE[\"b\"] = 2", source=b_src,
              edit=t.rows(("TABLE", "const", core), ("KEYS", "const", core)))
    with t.tree() as tmp:
        plan = t.proven(tmp, source=b_src, edit=t.edits(t.rows(("TABLE", "const", core), ("KEYS", "const", core)),
                                                     lambda m: m.update(module_statements={"TABLE[\"b\"] = 2": core})))
        text = plan.files.get(f"{core}.py", "")
        t.ok("M2 the statement placed by module_statements moves between its names, every proof passes",
             not plan.refusals and text.index("TABLE = ") < text.index("TABLE[\"b\"]") < text.index("KEYS = ") and not [p for p in plan.proofs if p[1] is False],
             [r.line()[:120] for r in plan.refusals] + [p[2][:100] for p in plan.proofs if p[1] is False])
    t.refusal("M3 input E: a name both imported and defined at module level", "R15", "join",
              source=t.ins("def join(a, b):\n    return str(a) + str(b)").replace("import sys\n", "import sys\nfrom os.path import join\n", 1), edit=t.rows(("join", "func", core)))
    t.refusal("M3 input C: a mangled attribute in cut class code", "R16", "__x",
              source=FIXTURE.replace("    def top(self):", "    def put(self):\n        self.__x = 1\n\n    def get(self):\n        return self.__x\n\n    def top(self):"),
              edit=t.rows((cls + ".put", "method", core), (cls + ".get", "method", dialog)))
    t.refusal("R10 two statements on one physical line", "R10", "two statements on one line", source=FIXTURE.replace('LABEL = "x"', 'LABEL = "x"; LIMIT2 = 2'),
              edit=t.rows(("LIMIT2", "const", core)))
    t.refusal("m3 a module_statements key shared by two statements", "R10", "places the statements",
              source=t.ins("if os.name == 'nt':\n    pass\nLATE_ONE = 1\nif os.name == 'nt':\n    pass"), edit=t.edits(t.rows(("LATE_ONE", "const", core)),
              lambda m: m.update(module_statements={"if os.name == 'nt':": core})))
    with t.tree() as tmp:
        plan = t.plan(tmp, extra={t.core + ".py": "def helper(x):\n    return 1\n\nLIMIT = 1\n", t.dialog + ".py": "LABEL = 'x'\n"})
        r8 = [r for r in plan.refusals if r.code == "R8"]
        t.ok("M4 a re-run over leftover parts: ONE R8 naming the part files to remove, no R3 per name",
             len(r8) == 1 and t.core + ".py" in r8[0].line() and t.dialog + ".py" in r8[0].line() and not any(r.code == "R3" for r in plan.refusals),
             [r.line()[:200] for r in plan.refusals[:3]])
    _ = dialog


def _cases_proofs(t: T) -> None:
    core, cls = t.core, t.cls
    with t.tree() as tmp:
        snap = t.snap
        args, _mp = _fx(Path(tmp), t.cfg)
        before = snap(tmp)
        code, text = t.cli_args(tmp, "--dry-run", args)
        t.ok("clean fixture: dry-run exit 0, proofs P1-P8 pass, nothing written", code == 0 and snap(tmp) == before
             and all(f"PASS P{i} " in text for i in range(1, 9)), "\n".join(text.splitlines()[-12:]))
        code2, _t2 = t.cli_args(tmp, "--apply", args)
        code3, text3 = t.cli_args(tmp, "--dry-run", args)
        t.ok("apply writes the parts; the re-run says nothing to do (exit 0)", code2 == 0 and code3 == 0 and "nothing to do" in text3,
             " | ".join(l.strip()[:200] for l in text3.splitlines() if l.startswith("  R")))
        print(text)
    with t.tree() as tmp:
        plan = t.proven(tmp, source=FIXTURE.replace("LIMIT = 3", "LIMIT = 3\nPA, PB = 1, 2"), edit=t.rows(("PA", "const", core), ("PB", "const", core)))
        t.ok("B1 a same-home tuple assignment through the proofs: P1 and P2 pass", t.proof(plan, "P2") is True and t.proof(plan, "P1") is True,
             [p[2][:160] for p in plan.proofs[:2]] + [r.line()[:100] for r in plan.refusals])
    with t.tree() as tmp:
        plan = t.plan(tmp)
        plan.files[f"{core}.py"] += "\nLIMIT = 4\n"
        _p1_p2(plan, cls)
        p2 = [p for p in plan.proofs if p[0] == "P2"][0]
        t.ok("B1 a name written twice on the parts side fails P2", p2[1] is False and "LIMIT" in p2[2], p2[2])


def _cases_trees(t: T) -> None:
    core, cls = t.core, t.cls
    data_src = t.ins("DATA = json.loads((HERE.parent / \"references\" / \"data.json\").read_text(encoding=\"utf-8\"))")
    with t.tree() as tmp:
        plan = t.proven(tmp, source=data_src, edit=t.rows(("DATA", "const", core)), pkg_files={"references/data.json": "{\"k\": 1}"})
        t.ok("B2 a module that reads a sibling data directory at import passes P3 (whole package root in both trees)", t.proof(plan, "P3") is True,
             [p[2][:200] for p in plan.proofs if p[0] == "P3"] + [r.line()[:120] for r in plan.refusals])
    with t.tree() as tmp:
        plan = t.plan(tmp)
        real, raised = shutil.copytree, []

        def boom(*a, **k):
            raise OSError("injected copy failure")
        shutil.copytree = boom
        try:
            try:
                run_proofs(plan, cls)
            except Cannot as exc:
                raised.append(str(exc))
        finally:
            shutil.copytree = real
        t.ok("B2 an OSError during the tree copy is a Cannot line, not a traceback", raised and "injected" in raised[0], raised)
    tests = {"test_x.py": "def f():\n    return '__FACADE__.py'\n"}
    with t.tree() as tmp:
        plan = t.proven(tmp, tests=tests, edit=lambda m: m["source_mentions"].append({"file": "test_x.py", "function": "f", "count": 1}))
        t.ok("B3 P5 passes tests_dir: a declared source mention in the package tests is found on the result tree", t.proof(plan, "P5") is True,
             [p[2][:200] for p in plan.proofs if p[0] == "P5"])


def _cases_p7_p8(t: T) -> None:
    core = t.core
    with t.tree() as tmp:
        plan = t.plan(tmp)
        plan.files[f"{core}.py"] += "\n\ndef broken():\n    return undefined_thing()\n"
        _tree_proofs(plan, t.cls)
        p7 = [p for p in plan.proofs if p[0] == "P7"][0]
        t.ok("B4 P7 fails when a part gains a pyflakes finding (undefined name)", p7[1] is False and "UndefinedName" in p7[2], p7[2])
    with t.tree() as tmp:
        plan = t.plan(tmp)
        real = sys.modules.get("pyflakes")
        sys.modules["pyflakes"] = None
        try:
            _tree_proofs(plan, t.cls)
        finally:
            if real is None:
                sys.modules.pop("pyflakes", None)
            else:
                sys.modules["pyflakes"] = real
        plan.args.apply = True
        t.ok("B4 pyflakes not importable: P7 NOT RUN and --apply refuses naming it", t.proof(plan, "P7") is None and failed(plan) and "P7 not run" in result_line(plan),
             result_line(plan))
    say = t.ins("def say():\n    print('a " + EM + " b')")
    with t.tree() as tmp:
        plan = t.proven(tmp, source=say, edit=t.rows(("say", "func", core)))
        p8 = [p for p in plan.proofs if p[0] == "P8"]
        t.ok("M7 a K7 residue with no setup_import fails P8 and names the part", p8 and p8[0][1] is False and core + ".py" in p8[0][2] and failed(plan),
             [p[2][:160] for p in plan.proofs if p[0] == "P8"])
    with t.tree() as tmp:
        plan = t.proven(tmp, source=say, edit=t.edits(t.rows(("say", "func", core)), lambda m: m.update(setup_import="hooklib")),
                        extra={"hooklib.py": "def utf8_stdio():\n    pass\n"})
        t.ok("M7 with setup_import the added import clears the residue: P8 passes", t.proof(plan, "P8") is True and "import hooklib" in plan.files[f"{core}.py"],
             [p[2][:160] for p in plan.proofs if p[0] == "P8"] + [r.line()[:100] for r in plan.refusals])


def _carrier_files(t: T) -> dict:
    ff = t.facade + ".py"
    return {
        "references/gate-registry.json": json.dumps({"rows": [{"file": ff, "function": "helper"}, {"file": ff, "function": "main"}]}, indent=1) + "\n",
        "references/null-outcomes.json": json.dumps({"guards": [f"{ff}::helper", f"{ff}::main"]}, indent=1) + "\n",
        "references/block-names.json": json.dumps({"names": [f"{t.facade}:{t.cls}.low", f"{t.facade}:{t.cls}.top"]}, indent=1) + "\n",
        "scripts/audit_factory.py": f"NO_MOVE = {{\n    (\"{ff}\", \"{t.cls}.low\"): 1,\n    (\"{ff}\", \"{t.cls}.top\"): 2,\n    (\"{ff}\", \"helper\"): 3,\n}}\n",
        "scripts/tests/test-layers.json": json.dumps({"keep": {"k1": {"covers": [ff]}, "k2": {"covers": ["other.py"]}}}, indent=1) + "\n",
    }


def _cases_carriers(t: T) -> None:
    core, dialog, cls = t.core, t.dialog, t.cls
    with t.tree() as tmp:
        plan = t.proven(tmp, pkg_files=_carrier_files(t))
        got = {p.name: x for p, x in plan.carriers.items()}
        want = {"gate-registry.json": f'"file": "{core}.py"', "null-outcomes.json": f'"{core}.py::helper"', "block-names.json": f'"{dialog}:{camel(dialog)}.top"',
                "audit_factory.py": f'("{core}.py", "{cls}.low")', "test-layers.json": f'"{core}.py"'}
        for name, needle in want.items():
            t.ok(f"carrier form of {name}: the moved row is rewritten ({needle})", needle in got.get(name, ""), got.get(name, "not rewritten")[:200])
        t.ok("carrier pass: unmoved rows stay, P6 passes with every carrier rescanned",
             f'"{t.facade}.py::main"' in plan.carrier_view[next(p for p in plan.carrier_view if p.name == "null-outcomes.json")] and t.proof(plan, "P6") is True,
             [p[2][:200] for p in plan.proofs if p[0] == "P6"])
    nested = json.dumps({"rows": [{"meta": {"k": 1}, "file": t.facade + ".py", "function": "helper"}]}, indent=1) + "\n"
    with t.tree() as tmp:
        plan = t.proven(tmp, pkg_files={"references/gate-registry.json": nested})
        t.ok("M6 P6 fails when a row the regex skips still names the facade file with a moved name", t.proof(plan, "P6") is False,
             [p[2][:200] for p in plan.proofs if p[0] == "P6"])
    rows = {"low": {"home": dialog}, f"{cls}.low": {"home": core}}
    t.ok("M6 home_of tries `<Class>.<name>` before the bare name", _home_of(rows, cls, "low") == (core, f"{cls}.low"), _home_of(rows, cls, "low"))
    with t.tree() as tmp:
        plan = t.proven(tmp)
        t.ok("a tree with no carrier files: P6 reports 0 carriers rescanned and passes", t.proof(plan, "P6") is True and "0 carriers rescanned" in
             [p[2] for p in plan.proofs if p[0] == "P6"][0], [p[2][:200] for p in plan.proofs if p[0] == "P6"])


@contextlib.contextmanager
def _carriers_with(mutate):
    """The tool's carriers file replaced for a block by a copy that `mutate(cfg)` has edited (the selftest's way to ask
    'what if the data said ...'); the file is put back on leaving."""
    global CARRIERS_FILE
    real = CARRIERS_FILE
    cfg = json.loads(real.read_text(encoding="utf-8"))
    mutate(cfg)
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as d:
        CARRIERS_FILE = Path(d) / real.name
        CARRIERS_FILE.write_text(json.dumps(cfg), encoding="utf-8")
        try:
            yield cfg
        finally:
            CARRIERS_FILE = real


def _carrier(cfg: dict, file: str) -> dict:
    return next(c for c in cfg["carriers"] if c["file"] == file)


def _cases_class_key(t: T) -> None:
    core, cls, ff = t.core, t.cls, t.facade + ".py"
    files = {"scripts/audit_factory.py": f'NO_MOVE = {{\n    ("{ff}", "{cls}.low"): 1,\n    ("{ff}", "helper"): 3,\n}}\n',
             "scripts/tests/test_bug_records.py": f'KEPT = {{\n    ("{ff}", "{cls}.low"): 1,\n    ("{ff}", "helper"): 3,\n}}\n',
             "references/block-names.json": json.dumps({"names": [f"{t.facade}:{cls}.low"]}) + "\n",
             "scripts/tests/test_gate_registry.py": f'SITES = [\n    ("other.py", "helper", "g3"),\n    ("{ff}", "helper", "g1"),\n    # the note of main\n    ("{ff}", "main", "g2"),\n]\n'}
    with t.tree() as tmp:
        plan = t.proven(tmp, pkg_files=files)
        got = {p.name: x for p, x in plan.carriers.items()}
        by = _carrier(t.cfg, "scripts/audit_factory.py")["class_key"], _carrier(t.cfg, "scripts/tests/test_bug_records.py")["class_key"]
        t.ok("F1 the shipped carriers declare their keys: audit_factory (A27 folds every mixin to the class) assembled, test_bug_records (the census walks the real class) mixin",
             by == ("assembled", "mixin"), by)
        t.ok("F1 an `assembled` carrier keeps the split class's name and changes only the file", f'("{core}.py", "{cls}.low")' in got.get("audit_factory.py", "") and camel(core) not in got.get("audit_factory.py", ""),
             got.get("audit_factory.py"))
        t.ok("F1 a `mixin` carrier gets the mixin class name of the member's home", f'("{core}.py", "{camel(core)}.low")' in got.get("test_bug_records.py", ""), got.get("test_bug_records.py"))
        t.ok("F1 the reader carrier (block-names, mixin) names `<part>:<Mixin>.<m>`", f'"{core}:{camel(core)}.low"' in got.get("block-names.json", ""), got.get("block-names.json"))
        t.ok("F2 a py-triple row `(<facade file>, <function>, <tag>)` changes its file and, in a sorted run, moves to its sorted place (a reader compares with sorted()); "
             "the comment above the row below it stays with that row; an unmoved name and another file stay",
             got.get("test_gate_registry.py") == f'SITES = [\n    ("{core}.py", "helper", "g1"),\n    ("other.py", "helper", "g3"),\n    # the note of main\n    ("{ff}", "main", "g2"),\n]\n',
             got.get("test_gate_registry.py"))
        ctx = CarrierCtx(ff, t.facade, cls, {"helper": {"home": core}}, {"helper"}, [core])
        unsorted = f'S = [\n    ("{ff}", "helper", "g1"),\n    ("a.py", "x", "g0"),\n]\n'
        t.ok("F2 a py-triple run that was NOT sorted keeps its order: the file is rewritten in place",
             _c_py_triple(ctx, {"id": 0, "file": "x"}, unsorted) == unsorted.replace(f'("{ff}"', f'("{core}.py"'), _c_py_triple(ctx, {"id": 0, "file": "x"}, unsorted))
        t.ok("F1 P6 passes on the cut with both declared keys", t.proof(plan, "P6") is True, [p[2][:300] for p in plan.proofs if p[0] == "P6"])
    with _carriers_with(lambda c: _carrier(c, "scripts/audit_factory.py").pop("class_key")):
        with t.tree() as tmp:
            plan = t.plan(tmp, pkg_files=files)
            hit = [r for r in plan.refusals if r.code == "R18" and "audit_factory.py" in r.line()]
            t.ok("F1 a class-qualified carrier with no class_key is refused (R18, by file), not guessed", hit and not plan.carriers, [r.line()[:200] for r in plan.refusals[:2]])
    with _carriers_with(lambda c: _carrier(c, "scripts/audit_factory.py").update(class_key="both")):
        with t.tree() as tmp:
            plan = t.plan(tmp, pkg_files=files)
            t.ok("F1 a class_key the tool does not know ('both') is refused too", any(r.code == "R18" and "'both'" in r.line() for r in plan.refusals), [r.line()[:200] for r in plan.refusals[:2]])


def _cases_verify(t: T) -> None:
    ok_script = "print('first')\nprint('=== vok: 3/3 ok ===')\n"
    fail_script = "import sys\nprint('=== vbad: 2/3 ok ===')\nsys.exit(1)\n"
    files = {"references/gate-registry.json": json.dumps({"rows": [{"file": t.facade + ".py", "function": "helper"}]}, indent=1) + "\n",
             "references/null-outcomes.json": json.dumps({"guards": [f"{t.facade}.py::main"]}, indent=1) + "\n",
             "scripts/tests/vok.py": ok_script, "scripts/tests/vbad.py": fail_script,
             "scripts/tests/vslow.py": "import time\ntime.sleep(5)\n", "scripts/tests/vtext.py": "print('no scenario or keep row covers x')\n"}

    def verify(*entries, timeout=None):
        def edit(cfg):
            _carrier(cfg, "references/gate-registry.json")["verify"] = list(entries)
            if timeout:
                cfg["verify_timeout"] = timeout
        return edit
    p6 = lambda plan: [p[2] for p in plan.proofs if p[0] == "P6"][0] if any(p[0] == "P6" for p in plan.proofs) else ""    # noqa: E731
    with _carriers_with(verify("scripts/tests/vok.py")), t.tree() as tmp:
        plan = t.proven(tmp, pkg_files=files)
        t.ok("F1b a verify command that exits 0 passes P6 and its closing line is quoted", t.proof(plan, "P6") is True and "=== vok: 3/3 ok ===" in p6(plan) and "exit 0" in p6(plan),
             p6(plan)[-400:])
        t.ok("F1b a present carrier with no verify says so in one line (here the guard carrier, null-outcomes)",
             p6(plan).count("carrier 2 references/null-outcomes.json: no verify declared") == 1, p6(plan)[-400:])
        t.ok("F1b the verify line names the carrier and the command it ran",
             "carrier 1 references/gate-registry.json: python -B scripts/tests/vok.py" in p6(plan), p6(plan)[-300:])
    with _carriers_with(verify("scripts/tests/vbad.py")), t.tree() as tmp:
        plan = t.proven(tmp, pkg_files=files)
        t.ok("F1b a verify command that exits 1 makes P6 FAIL, the exit code and the closing line named, and the run refuses", t.proof(plan, "P6") is False
             and "exit 1" in p6(plan) and "=== vbad: 2/3 ok ===" in p6(plan) and failed(plan), p6(plan)[-300:])
    with _carriers_with(verify("scripts/tests/vslow.py", timeout=1)), t.tree() as tmp:
        plan = t.proven(tmp, pkg_files=files)
        t.ok("F1b a verify command over verify_timeout is a failed proof, named", t.proof(plan, "P6") is False and "timed out after 1 s" in p6(plan), p6(plan)[-300:])
    with _carriers_with(verify({"args": ["scripts/tests/vslow.py"], "verify_timeout": 30}, timeout=1)), t.tree() as tmp:
        plan = t.proven(tmp, pkg_files=dict(files, **{"scripts/tests/vslow.py": "import time\ntime.sleep(2)\nprint('slept')\n"}))
        t.ok("F1b a per-entry verify_timeout overrides the file's (1 s file cap, 30 s entry cap: a 2 s command passes)",
             t.proof(plan, "P6") is True and "slept" in p6(plan), p6(plan)[-300:])
    with _carriers_with(verify({"args": ["scripts/tests/vtext.py"], "absent": "no scenario or keep row covers"})), t.tree() as tmp:
        plan = t.proven(tmp, pkg_files=files)
        t.ok("F1b an `absent` text in the output of an exit-0 command fails P6", t.proof(plan, "P6") is False and "no scenario or keep row covers" in p6(plan), p6(plan)[-300:])
    with _carriers_with(verify("scripts/tests/nothere.py")), t.tree() as tmp:
        plan = t.proven(tmp, pkg_files=files)
        t.ok("F1b a verify script absent from the would-be tree is a failed proof, not a silent skip", t.proof(plan, "P6") is False and "not in the would-be tree" in p6(plan), p6(plan)[-300:])
    unmoved = dict(files, **{"references/gate-registry.json": json.dumps({"rows": [{"file": t.facade + ".py", "function": "main"}]}, indent=1) + "\n"})
    with _carriers_with(verify("scripts/tests/vok.py")), t.tree() as tmp:
        plan = t.proven(tmp, pkg_files=unmoved)
        t.ok("F1b a carrier file with no row for the moved names still has its verify run once (it proves the carrier intact)",
             p6(plan).count("gate-registry.json: python -B scripts/tests/vok.py -> exit 0") == 1 and t.proof(plan, "P6") is True, p6(plan)[-300:])
    with _carriers_with(verify("scripts/tests/vok.py")), t.tree() as tmp:
        plan = t.proven(tmp, pkg_files={"scripts/tests/vok.py": ok_script})
        t.ok("F1b a carrier file absent in the tree has nothing to run: one line says so, no failure",
             "gate-registry.json: the carrier file is absent in this tree" in p6(plan) and t.proof(plan, "P6") is True, p6(plan)[-300:])


def _cases_apply(t: T) -> None:
    with t.tree() as tmp:
        args, _mp = _fx(Path(tmp), t.cfg, pkg_files=_carrier_files(t))
        before = t.snap(tmp)
        real, calls = os.replace, {"n": 0}

        def flaky(a, b):
            calls["n"] += 1
            if calls["n"] == 2:
                raise OSError("injected")
            return real(a, b)
        os.replace = flaky
        out = io.StringIO()
        try:
            with contextlib.redirect_stdout(out):
                code = main(["--map", str(args.map_path), "--source", args.source, "--class", t.cls, "--apply", "--repo", str(tmp)])
        finally:
            os.replace = real
        t.ok("M4 an OSError on the 2nd replace: exit 2, a Cannot line, the tree is exactly as before (rolled back)",
             code == 2 and "cannot run" in out.getvalue() and "Traceback" not in out.getvalue() and t.snap(tmp) == before, [code, out.getvalue()[-200:]])
    with t.tree() as tmp:
        plan = t.plan(tmp, pkg_files=_carrier_files(t))
        run_proofs(plan, t.cls)
        carrier = next(p for p in plan.carriers)
        carrier.write_text(carrier.read_text(encoding="utf-8") + " ", encoding="utf-8")
        refused = []
        try:
            write_all(plan)
        except WriteFailed as exc:
            refused.append(str(exc))
        sd = plan.stats["scripts_dir"]
        t.ok("M4 a carrier changed between the plan and the write is refused, nothing written", refused and not (sd / f"{t.core}.py").exists(), refused)
    with t.tree() as tmp:
        args, _mp = _fx(Path(tmp), t.cfg, facade_mod=False)
        code, text = t.cli_args(tmp, "--dry-run", args)
        code2, text2 = t.cli_args(tmp, "--apply", args)
        t.ok("m3 P3 not run: the dry-run ends `would apply (P3 not run)`, --apply names it and writes nothing",
             code == 0 and "would apply (P3 not run)" in text and code2 == 2 and "P3 not run" in text2.splitlines()[-1] and not (Path(tmp) / t.cfg["package_root"] / "scripts" / f"{t.core}.py").exists(),
             [text.splitlines()[-1], text2.splitlines()[-1]])


def _cases_misc(t: T) -> None:
    core, dialog, cls = t.core, t.dialog, t.cls
    with t.tree() as tmp:
        plan = t.plan(tmp)
        t.ok("W2 the facade's path preamble is rewritten to the expression of the moved name", any(x.startswith("W2 ") for x in plan.rewrites), plan.rewrites)
    with t.tree() as tmp:
        args, _mp = _fx(Path(tmp), t.cfg)
        args.homes = [core]
        plan = make_plan(args)
        run_proofs(plan, cls)
        t.ok("--homes: only the selected home is written, the rest stays in the facade, P1-P4 pass (P5 is red by design: the map still homes the unwritten mixin)",
             sorted(plan.files) == sorted([core + ".py", t.facade + ".py"]) and not plan.refusals and all(t.proof(plan, p) is True for p in ("P1", "P2", "P3", "P4"))
             and 'LABEL = "x"' in plan.files[t.facade + ".py"],
             [sorted(plan.files)] + [p[2][:100] for p in plan.proofs if p[1] is False] + [r.line()[:100] for r in plan.refusals])
    src = FIXTURE.replace("import json\nimport os\nimport sys\n", "import json\n# note about os\nimport os  # trailing os note\nimport sys  # keep sys note\nfrom os import sep, linesep  # why\n", 1)
    src = src.replace("return __CLS__().top()", "return __CLS__().top() + sep").replace("return json.dumps(x)", "return json.dumps(x) + linesep", 1)
    with t.tree() as tmp:
        plan = t.plan(tmp, source=src)
        fac = plan.files.get(t.facade + ".py", "")
        text = report(plan)
        t.ok("m1 an import line kept whole stays verbatim with its comment", "import sys  # keep sys note" in fac, fac[:300])
        t.ok("m1/m2 a line of which the facade uses only some names is regenerated; its comment is listed as dropped",
             "from os import sep\n" in fac and "linesep" not in fac and ":6: # why" in text, text[text.find("dropped"):][:300])
        t.ok("m1 every dropped comment line is listed by source line number and counted; the label is not `(before imports)`",
             "dropped comment lines (no generated file carries them): 3" in text and ":3: # note about os" in text and ":4: # trailing os note" in text
             and "(before imports)" not in text, text[text.find("dropped"):][:300])
        t.ok("m2 the facade imports only the names its own code uses (json lives in the part only)", "import json" not in fac and "import json" in plan.files[core + ".py"], fac[:200])
    late = FIXTURE.replace("def helper(x):\n    return json.dumps(x)\n", "def helper(x):\n    return json.dumps(x)\n\n\ndef lazy():\n    import __PRE__late\n    return __PRE__late.LATE\n").replace("__PRE__", t.pre)
    with t.tree() as tmp:
        plan = t.plan(tmp, source=late, extra={t.pre + "late.py": "LATE = 1\n"}, edit=t.edits(t.rows(("lazy", "func", core), ("LATE", "const", t.pre + "late")),
                      lambda m: m.update(layers=[[t.pre + "late"], [core], [dialog], [t.facade]])))
        fac = plan.files.get(t.facade + ".py", "")
        install = re.search(r"module_facade\.install\(__name__, \[([^\]]*)\]\)", fac)
        t.ok("T-1b 2 a part of `layers` the source imported lazily is imported by the facade by a literal import and installed first (L11 b: every part, rank order)",
             f"import {t.pre}late  # noqa" in fac and install is not None and install.group(1).split(", ")[0] == f"{t.pre}late" and not plan.refusals,
             [r.line()[:150] for r in plan.refusals] + [fac[:400]])
    prop = FIXTURE.replace("    def top(self):", "    @property\n    def size(self):\n        return 1\n\n    @size.setter\n    def size(self, v):\n        pass\n\n    def top(self):")
    with t.tree() as tmp:
        plan = t.plan(tmp, source=prop, edit=t.rows((cls + ".size", "method", core)))
        t.ok("m3 a property getter/setter pair of one name is one unit, not an R3", not any(r.code == "R3" for r in plan.refusals) and "@size.setter" in plan.files.get(core + ".py", ""),
             [r.line()[:150] for r in plan.refusals])


def _hand_layout(obj: dict) -> str:
    """A map laid out the way the real one is: one top-level key per line, a list of objects one object per line."""
    items = []
    for k, v in obj.items():
        if isinstance(v, list) and v and all(isinstance(e, dict) for e in v):
            items.append(f' {json.dumps(k)}: [\n' + ",\n".join("  " + json.dumps(e) for e in v) + "\n ]")
        else:
            items.append(f" {json.dumps(k)}: {json.dumps(v)}")
    return "{" + ",\n".join(items).lstrip(" ") + "}\n"


def _l11_shape(text: str, parts: list, moved: set, module: str) -> list:
    """The shape L11 (b) asks of an installed facade, written from the rule's text: a literal `import <part>` for every part,
    exactly one `<module>.install(__name__, [<parts, low rank first>])`, and no defined name whose home is a part."""
    tree, probs = ast.parse(text), []
    imported = {a.name for n in ast.walk(tree) if isinstance(n, ast.Import) for a in n.names}
    probs += [f"no literal `import {p}`" for p in parts if p not in imported]
    calls = [n for n in ast.walk(tree) if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == "install"
             and isinstance(n.func.value, ast.Name) and n.func.value.id == module]
    if len(calls) != 1:
        return probs + [f"{len(calls)} install calls"]
    args = calls[0].args
    listed = args[1] if len(args) > 1 else None
    if not (len(args) == 2 and isinstance(args[0], ast.Name) and args[0].id == "__name__" and isinstance(listed, ast.List)
            and all(isinstance(e, ast.Name) for e in listed.elts)):
        return probs + ["the install arguments are not (__name__, [names])"]
    if [e.id for e in listed.elts] != parts:
        probs.append(f"installs {[e.id for e in listed.elts]}, expected {parts} in rank order")
    for n in tree.body:
        defined = [n.name] if isinstance(n, (ast.FunctionDef, ast.ClassDef)) else _targets(n) if isinstance(n, (ast.Assign, ast.AnnAssign)) else []
        probs += [f"defines `{d}`, whose home is a part" for d in defined if d in moved]
    return probs


def _cases_t1b_map(t: T) -> None:
    core, dialog, cls = t.core, t.dialog, t.cls
    no_mixin = lambda m: m.update(names=[r for r in m["names"] if r["name"] not in (camel(core), camel(dialog))])    # noqa: E731
    with t.tree() as tmp:
        plan = t.proven(tmp, edit=no_mixin)
        rows = [r for r in plan.map_new["names"] if r["name"] in (camel(core), camel(dialog))]
        t.ok("T-1b 1a the mixin classes get `names` rows in the would-be map, and P5 judges that map", len(rows) == 2 and all(r["kind"] == "class" for r in rows)
             and t.proof(plan, "P5") is True,[r for r in rows] + [p[2][:200] for p in plan.proofs if p[0] == "P5"])
    with t.tree() as tmp:
        plan = t.plan(tmp, edit=no_mixin)
        plan.map_new = None                          # control: the same cut judged against the map as it was
        _tree_proofs(plan, cls)
        t.ok("T-1b 1a control: P5 on the unchanged map (no mixin rows) FAILS", t.proof(plan, "P5") is False, [p[2][:200] for p in plan.proofs if p[0] == "P5"])
    ff = t.facade + ".py"
    bug = (f'KEPT = {{\n    ("{ff}", "{cls}.low"): 1,\n    ("{ff}", "{cls}.top"): 2,\n}}\n\n\ndef build():\n    return {{\n        ("{ff}", "helper"): 3,\n    }}\n\n\n'
           f'def reader(path):\n    text = path.read_text()\n    return {{\n        ("{ff}", "{cls}.pure"): 4,\n    }}\n')
    stale = lambda m: m["source_mentions"].extend([{"file": "test_bug_records.py", "function": "<module>", "count": 5, "why": "x"},     # noqa: E731
                                                   {"file": "test_bug_records.py", "function": "gone", "count": 1, "why": "x"}])
    with t.tree() as tmp:
        plan = t.plan(tmp, pkg_files={"scripts/tests/test_bug_records.py": bug}, edit=stale)
        m, rd = plan.map_new["source_mentions"], plan.map_new["source_readers"]
        got = {(r["function"], r["count"]) for r in m if r["file"] == "test_bug_records.py"}
        t.ok("T-1b 1b the rows of a rewritten test file are recomputed: count lowered, row at zero dropped, missing rows added (mention and reader)",
             got == {("<module>", 2), ("build", 1)} and [(r["function"], r["count"]) for r in rd] == [("reader", 1)] and json.loads(plan.map_text) == plan.map_new,
             [got, rd, plan.map_notes])
    with t.tree() as tmp:
        plan = t.plan(tmp)
        t.ok("T-1b 1b no carrier touches a test file: no row changes", plan.map_new["source_readers"] == [] and plan.map_new["source_mentions"] == [], plan.map_notes)


def _cases_t1b_installed(t: T) -> None:
    core = t.core
    no_mixin = lambda m: m.update(names=[r for r in m["names"] if r["name"] not in (camel(core), camel(t.dialog))])    # noqa: E731
    with t.tree() as tmp:
        args, _mp = _fx(Path(tmp), t.cfg)
        code, text = t.cli_args(tmp, "--apply", args)
        written = json.loads(Path(args.map_path).read_text(encoding="utf-8"))
        t.ok("T-1b 1c --apply writes family.installed true into the map (and the P5 line is PASS)", code == 0 and written["family"]["installed"] is True and "PASS P5 " in text,
             [code, written["family"], text.splitlines()[-1]])
    with t.tree() as tmp:
        args, mp = _fx(Path(tmp), t.cfg, edit=no_mixin)
        before = _hand_layout(mp)
        Path(args.map_path).write_text(before, encoding="utf-8")
        code, _text = t.cli_args(tmp, "--apply", args)
        after = Path(args.map_path).read_text(encoding="utf-8")
        gone, new = set(before.split("\n")) - set(after.split("\n")), set(after.split("\n")) - set(before.split("\n"))
        t.ok("T-1b 1c the layout of the map is kept: only the family line, the comma of the last row and the two new mixin rows differ line by line",
             code == 0 and len(gone) == 2 and len(new) == 4 and '"installed": true' in "".join(new) and sum(camel(x) in "".join(new) for x in (core, t.dialog)) == 2,
             [code, sorted(gone)[:2], sorted(new)[:4]])
    with t.tree() as tmp:
        plan = t.plan(tmp, edit=lambda m: m.pop("family"))
        t.ok("T-1b 1c a map with no family header (or no installed key): nothing set, one line says so",
             "family" not in plan.map_new and sum("family.installed not touched" in x for x in plan.map_notes) == 1, plan.map_notes)


def _cases_t1b_facade_k7(t: T) -> None:
    core, dialog = t.core, t.dialog
    with t.tree() as tmp:
        plan = t.proven(tmp)
        parts = [core, dialog]
        moved = {n for n, r in _fx_rows(t).items() if r in parts}
        fac = plan.files[t.facade + ".py"]
        bad = _l11_shape(fac, parts, moved, t.cfg["facade"]["module"])
        broken = _l11_shape(fac.replace(f"import {dialog}  # noqa: E402,F401\n", ""), parts, moved, t.cfg["facade"]["module"])
        t.ok("T-1b 2 the generated facade of the clean fixture passes the L11 (b) shape (and the check bites: a missing part import is reported)",
             bad == [] and broken == [f"no literal `import {dialog}`"], [bad, broken])
    say = t.ins("def say():\n    print('a " + EM + " b')")
    setup = t.edits(t.rows(("say", "func", core)), lambda m: m.update(setup_import="hooklib"))
    hook = {"hooklib.py": "def utf8_stdio():\n    pass\n"}
    with t.tree() as tmp:
        plan = t.proven(tmp, source=say, edit=setup, extra=hook)
        p7 = [p for p in plan.proofs if p[0] == "P7"][0]
        t.ok("T-1b 3 exempt: the messages caused by the K7 line the tool added are subtracted, counted and printed; P7 passes",
             p7[1] is True and re.search(r"P7: [1-9]\d* messages from K7 setup lines exempt", p7[2]) is not None, p7[2])
    with t.tree() as tmp:
        plan = t.plan(tmp, source=say, edit=setup, extra=hook)
        plan.files[f"{core}.py"] += "\n\ndef broken():\n    return undefined_thing()\n"
        _tree_proofs(plan, t.cls)
        p7 = [p for p in plan.proofs if p[0] == "P7"][0]
        t.ok("T-1b 3 not exempt: any other growth (an undefined name) still fails P7, the exempt count is printed beside it",
             p7[1] is False and "UndefinedName" in p7[2] and "UnusedImport" not in p7[2].split("GREW")[-1] and "messages from K7 setup lines exempt" in p7[2], p7[2])
    hooked = say.replace("import sys\n", "import sys\nimport hooklib\n", 1).replace("print('a " + EM + " b')", "hooklib.utf8_stdio()\n    print('a " + EM + " b')")
    with t.tree() as tmp:
        plan = t.plan(tmp, source=hooked, edit=setup, extra=hook)
        table = [imports_module(x, "hooklib") for x in ("import hooklib\n", "from hooklib import f\n", "try:\n    import hooklib\nexcept ImportError:\n    pass\n",
                                                         "def f():\n    import hooklib\n", "if X:\n    import hooklib\n", "import os\n")]
        t.ok("T-1b 3 a part that already imports the setup module at module level gets no K7 line (the K7 check does not flag it either; the rule is a truth table)",
             plan.files[f"{core}.py"].count("import hooklib") == 1 and table == [True, True, True, False, False, False], [plan.stats["k7"], table])


def _fx_rows(t: T) -> dict:
    """{name: home} of the clean fixture's rows."""
    with t.tree() as tmp:
        _args, mp = _fx(Path(tmp), t.cfg)
    return {r["name"]: r["home"] for r in mp["names"]}


def _cases_t1b_imports_global(t: T) -> None:
    core, dialog = t.core, t.dialog
    idle = FIXTURE.replace("import sys\n", "import sys\nimport zlib  # kept: maybe a side effect\n", 1)
    with t.tree() as tmp:
        plan = t.proven(tmp, source=idle)
        fac = plan.files[t.facade + ".py"]
        text = report(plan)
        t.ok("T-1b 4 an import no segment and no facade code uses is kept in the facade verbatim and listed `kept (unused, possible side effect)`",
             "import zlib  # kept: maybe a side effect" in fac and "zlib" not in plan.files[f"{core}.py"] and "kept (unused, possible side effect): 1" in text
             and ":5 import zlib" in text and t.proof(plan, "P7") is True, [fac[:200], [p[2][:160] for p in plan.proofs if p[0] == "P7"]])
    ctr = t.ins("COUNTER = 0\n\n\ndef bump():\n    global COUNTER\n    COUNTER += 1\n    return COUNTER\n\n\ndef peek():\n    return COUNTER")
    rows = lambda peek_home: t.rows(("COUNTER", "const", core), ("bump", "func", core), ("peek", "func", peek_home))    # noqa: E731
    t.refusal("T-1b 5 a bare reader of a name rebound through `global` in another part", "R17", "COUNTER", source=ctr, edit=rows(dialog))
    t.refusal("T-1b 5 facade code reading a name rebound through `global` in a part", "R17", "COUNTER", source=ctr.replace("return __CLS__().top()", "return COUNTER"),
              edit=rows(core))
    with t.tree() as tmp:
        plan = t.proven(tmp, source=ctr, edit=rows(core))
        t.ok("T-1b 5 control: the reader in the same home as the rebinding code is not refused and the cut proves", not plan.refusals and all(p[1] is True for p in plan.proofs),
             [r.line()[:140] for r in plan.refusals] + [p[2][:100] for p in plan.proofs if p[1] is not True])


def selftest() -> int:
    t = T()
    strip = lambda cfg: [c.pop("verify", None) for c in cfg["carriers"]]      # noqa: E731 - the fixtures hold no test files of the real carriers
    with _carriers_with(strip):
        for group in (_cases_refusals, _cases_r13, _cases_hazards, _cases_proofs, _cases_trees, _cases_p7_p8, _cases_carriers, _cases_class_key,
                      _cases_verify, _cases_apply, _cases_misc, _cases_t1b_map, _cases_t1b_installed, _cases_t1b_facade_k7, _cases_t1b_imports_global):
            try:
                group(t)
            except Exception as exc:                  # noqa: BLE001 - a case group that crashes is a failed case, never silent
                t.ok(f"{group.__name__} ran to the end", False, f"{type(exc).__name__}: {exc}")
    bad = 0
    for label, ok, detail in t.results:
        print(("PASS " if ok else "FAIL ") + label + ("" if ok else f" -- {detail}"))
        bad += 0 if ok else 1
    print(f"selftest: {len(t.results)} checks, {bad} failed")
    return 0 if not bad else 1


def main(argv=None) -> int:
    try:
        code, text = run(sys.argv[1:] if argv is None else argv)
    except WriteFailed as exc:
        print(f"source_split: cannot run: {exc}")
        return 2
    except Cannot as exc:
        print(f"source_split: cannot run: {exc}")
        return 1
    if text:
        print(text)
    return code


if __name__ == "__main__":
    sys.exit(main())
