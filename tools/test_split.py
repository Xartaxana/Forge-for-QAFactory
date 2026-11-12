"""Splits ONE test file of the package into part files by a small map, and proves that no check was lost
(TD-11, node T-3; spec docs/tasks/specs/td-11c-test-split.md sections 2 and 4.3 R-A3).

    python -B tools/test_split.py --map <map.json> (--dry-run | --apply) [--repo DIR]
    python -B tools/test_split.py --draft <test file> [--repo DIR]

The map (JSON; keys and row keys that start with an underscore are comments and are ignored):

    {"source": "<test file name>",            # a file of <repo>/ai-packages/qa-factory/scripts/tests (or a path from the repo root)
     "common": "<stem>_common",               # the source stem without a leading `test_`, plus `_common`
     "shim": true | false,                    # true if and only if another test imports the source (found by the tool)
     "parts": ["<source stem>_<topic>", ...],
     "names": [{"name": "...", "kind": "def|class|assign", "home": "<part stem>|<common stem>"}, ...],
     "statements": [{"line": N, "home": "..."}],   # module-level statements that are not definitions
     "closing": N}                                 # optional: the line of the old file's `finish("<label>")` statement to copy
                                                   # as the closing of every part that finds none (see "The closing")

What it does. Every top-level def / class / assignment of the source has exactly one row in `names`. A definition travels as a
SEGMENT: the definition with its decorators and the comment block directly above it, sliced from the source TEXT line by line
(never re-generated). A comment block that is separated from the next definition by a blank line goes to the part that receives
the first name below it. The runner (a `run_scenarios(...)` call with literal lists, a `main()` of direct calls, a module-level
`for` over a run list, an `if __name__` block, several of them) is GENERATED per part: the source's own runner restricted to the
part's scenarios, in the original order, with the `finish(<label>)` label plus the part suffix. A run list that a runner reads by
NAME (`SCENARIOS`, with an argv filter in the loop) is regenerated restricted and the consumer is copied as written. A source
runner the tool cannot recognise is refused, naming the line - never guessed.

The closing (F2 of node N2). Every generated runner ends with the old runner's closing call (`finish(<label>)`, which prints the
tally line and sets the exit code), with the label plus the part suffix. A part whose blocks hold their own `finish` keeps it; a
part that holds none (the old `main()` spans several parts, its `finish` sits at its end, and the part's scenarios come from the
`if __name__` block that calls `main()` last) gets the closing found in the blocks its scenarios come from: the `finish` of the
guard, else the `finish` of the runner function the guard calls. No closing found, a closing that differs between the blocks the
part's scenarios come from, or no `if __name__` block / runner function to carry it: REFUSED with file:line; the door is the map
key `closing` (an int: the line of the `finish("<label>")` statement of the source to copy, a line the tool lists in the refusal).

Every part imports only what its names use (the source's own import block reduced, `sys.path` lines kept as written) and the
names that live in the common module; parts never import each other. The one addition (F1 of node N2): a file that imports any
non-stdlib module (a part; the common module and the shim only get proof (g)) also keeps every module-level import of the old file that is a LOCAL module of the tests dir (a file beside the
old test, not a `test_*` file) even when it uses no name of it, as `import <module>  # noqa: E402` followed by
`del <module>  # split: imported for its sys.path effect` - the old file reached the scripts directory on `sys.path` through such an
import (story_run_common), a part without it crashed on `import <package module>`; the `del` is what keeps pyflakes (which ignores
`# noqa`) from reporting an unused import. A kept line above that already loads the module makes the extra import needless. Every
import a file does not carry is printed (`DROPPED IMPORT:`), every kept one too (`KEPT FOR ITS sys.path EFFECT:`), and a `test_*`
file the old file imports at module level is printed as `REPORTED:` and is not kept. With `"shim": true` the old file becomes a shim that
re-exports the names other tests import from it (listed in `__all__`); without a shim the old file is deleted and the tool
refuses if ANY other test imports it.

THE PROOF is printed by --dry-run and --apply, is computed from the text of the written files (re-read), and fails with exit 2:
(a) check-call sites before = after, (b) top-level names, (c) the run list, (d) byte identity of every moved segment (sha256),
(e) every written file compiles, (f) every part's runner holds exactly one closing call, (g) every part and the shim is imported
alone in a child process (`python -B -c "import <stem>"`, cwd a temp directory outside the repo, the directory of the would-be files
and the tests dir of the target tree as the only extra path entries, 120 s per file, exit 0 required, the stderr tail quoted on a
failure). (g) runs in --dry-run, and in --apply on the re-read temp files, before any rename: a failed proof leaves the target as it was.

Exit codes: 0 done / nothing to do; 1 cannot run (a bad option, a missing or unparsable file, a map that is not JSON);
2 refused (the reasons are printed; NOTHING was written). --apply writes every file to a temp name first and renames only after
the proof passed over the re-read temp files. The tool writes no registry: it PRINTS the row block the node hands over.
"""
from __future__ import annotations

import argparse
import ast
import dataclasses
import hashlib
import json
import os
import re
import shutil
import subprocess
import symtable
import sys
import tempfile
from pathlib import Path

TESTS_REL = "ai-packages/qa-factory/scripts/tests"
CHECK_NAMES = ("check", "check_eq", "check_in", "check_not_in")
RUN_NAME = "run_scenarios"
GEN_MARK = "split by tools/test_split.py"
SHIM_MARK = "# split-shim: generated by tools/test_split.py"
KEEP_MARK = "# split: imported for its sys.path effect"
IMPORT_TIMEOUT = 120      # seconds, per file, of the import proof (g)
PIECE_RE = re.compile(r"^# split: runner piece (\d+)\s*$")
MARKER_RE = re.compile(r"^#\s*[-=#*~]{3,}")
# calls whose presence in an import-time statement makes it build a world or touch the disk or the process state (WARNING only)
WORLD_HINTS = ("seed", "temp_project", "temp_dir", "mkdtemp", "use_project", "mark_project", "chdir", "getcwd", "mkdir",
               "write_text", "write_bytes", "read_text", "read_bytes", "open", "rmtree", "unlink", "Popen", "run_script",
               "run_capture", "install_artifacts", "rig", "Driver", "Controller", "project_of")
LIST_LIMIT = 25
LINE_WIDTH = 110


class Refusal(Exception):
    """The run is refused; `.problems` are the reasons. Nothing was written."""

    def __init__(self, problems):
        super().__init__("; ".join(problems))
        self.problems = list(problems)


class CannotRun(Exception):
    """The run cannot start (exit 1)."""


# ------------------------------------------------------------------------------------------------------ reading text

def decode_source(raw: bytes, label: str):
    """(text with \\n newlines, newline string). A BOM, bad UTF-8 or mixed newlines are refused."""
    if raw.startswith(b"\xef\xbb\xbf"):
        raise Refusal([f"{label}: the file starts with a BOM; remove it first"])
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as err:
        raise Refusal([f"{label}: not valid UTF-8 ({err.reason} at byte {err.start})"])
    crlf = text.count("\r\n")
    lf = text.count("\n") - crlf
    cr = text.count("\r") - crlf
    if cr or (crlf and lf):
        raise Refusal([f"{label}: mixed newlines (CRLF {crlf}, LF {lf}, bare CR {cr}); make them one style first"])
    return text.replace("\r\n", "\n"), ("\r\n" if crlf else "\n")


def slice_text(lines, start, end, repls=()):
    """lines[start..end] (1-based, inclusive) joined; `repls` = (lineno, col, end_lineno, end_col, new text) in absolute
    coordinates (ast columns are UTF-8 byte offsets)."""
    chunk = lines[start - 1:end]
    offsets = [0]
    for one in chunk:
        offsets.append(offsets[-1] + len(one) + 1)
    joined = "\n".join(chunk)

    def pos(lineno, col):
        line = lines[lineno - 1]
        return offsets[lineno - start] + len(line.encode("utf-8")[:col].decode("utf-8"))

    for l1, c1, l2, c2, new in sorted(repls, key=lambda r: (r[0], r[1]), reverse=True):
        a, b = pos(l1, c1), pos(l2, c2)
        joined = joined[:a] + new + joined[b:]
    return joined


def sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def comment_chunks(lines, a, b):
    out, cur = [], []
    for k in range(a, b + 1):
        if lines[k - 1].strip().startswith("#"):
            cur.append(lines[k - 1])
        elif cur:
            out.append("\n".join(cur))
            cur = []
    if cur:
        out.append("\n".join(cur))
    return out


def count_checks(tree) -> int:
    total = 0
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            f = node.func
            if (isinstance(f, ast.Name) and f.id in CHECK_NAMES) or (isinstance(f, ast.Attribute) and f.attr in CHECK_NAMES):
                total += 1
    return total


def symbols_of(src: str):
    """(defined at module level, referenced free names, names rebound through `global`) of a piece of module-level code."""
    top = symtable.symtable(src, "<piece>", "exec")
    defined, used, gwrites = set(), set(), set()
    for s in top.get_symbols():
        if s.is_assigned() or s.is_imported() or s.is_namespace():
            defined.add(s.get_name())
        if s.is_referenced():
            used.add(s.get_name())
    stack = list(top.get_children())
    while stack:
        table = stack.pop()
        stack.extend(table.get_children())
        for s in table.get_symbols():
            if s.is_global():
                if s.is_referenced():
                    used.add(s.get_name())
                if s.is_assigned():
                    gwrites.add(s.get_name())
    return defined, used - defined, gwrites


def world_calls(node) -> list:
    hits = []
    for sub in ast.walk(node):
        if isinstance(sub, ast.Call):
            f = sub.func
            tail = f.id if isinstance(f, ast.Name) else (f.attr if isinstance(f, ast.Attribute) else "")
            if tail in WORLD_HINTS:
                hits.append(tail)
    return hits


# ------------------------------------------------------------------------------------------------------ the analysis

@dataclasses.dataclass
class Seg:
    kind: str                # def | class | assign | statement
    names: list
    line: int                # the node's own first line
    start: int
    end: int
    text: str
    free: list
    uses: set
    gwrites: set
    world: list
    section: str | None
    sha: str = ""
    checks: int = 0          # check call sites inside the segment (a def's body included)

    @property
    def key(self) -> str:
        return self.names[0] if self.names else "stmt@" + self.sha[:10]


@dataclasses.dataclass
class Block:
    key: str                 # func:<name> | list:<NAME> | u<N>
    kind: str                # func | guard | for | call | run | list
    start: int
    end: int
    first: int
    node: object
    verbatim: bool = False
    entries: list = dataclasses.field(default_factory=list)      # [(kind, name)] in source order
    refs: set = dataclasses.field(default_factory=set)           # run lists this block reads by name
    stmts: list = dataclasses.field(default_factory=list)        # restricted func/guard: [dict]
    doc_end: int = 0
    free: list = dataclasses.field(default_factory=list)
    label_spans: list = dataclasses.field(default_factory=list)  # (node, old label)
    lit: str = "["


@dataclasses.dataclass
class Piece:
    """a module-level `finish(label)`"""
    start: int
    end: int
    node: object
    label: str


class Analysis:
    pass


def _targets(node):
    out = []

    def walk(t):
        if isinstance(t, ast.Name):
            out.append(t.id)
            return True
        if isinstance(t, (ast.Tuple, ast.List)):
            return all(walk(e) for e in t.elts)
        if isinstance(t, ast.Starred):
            return walk(t.value)
        return False

    ok = all(walk(t) for t in node.targets) if isinstance(node, ast.Assign) else walk(node.target)
    return out if ok else None


def _is_finish(call, funcs):
    f = call.func
    if isinstance(f, ast.Name):
        return f.id == "finish" and "finish" not in funcs
    return isinstance(f, ast.Attribute) and f.attr == "finish" and isinstance(f.value, ast.Name) and f.value.id == "harness"


def _is_run(call):
    f = call.func
    return (isinstance(f, ast.Name) and f.id == RUN_NAME) or (isinstance(f, ast.Attribute) and f.attr == RUN_NAME)


def _names_list(node, allowed):
    if isinstance(node, (ast.List, ast.Tuple)) and node.elts and all(isinstance(e, ast.Name) and e.id in allowed for e in node.elts):
        return [e.id for e in node.elts]
    return None


def _is_guard(node):
    if not (isinstance(node, ast.If) and not node.orelse and isinstance(node.test, ast.Compare)):
        return False
    t = node.test
    return (isinstance(t.left, ast.Name) and t.left.id == "__name__" and len(t.ops) == 1 and isinstance(t.ops[0], ast.Eq)
            and isinstance(t.comparators[0], ast.Constant) and t.comparators[0].value == "__main__")


def _is_bare_call_of(st, funcs):
    """`name()` or `sys.exit(name())` of a top-level function, as a statement."""
    if not (isinstance(st, ast.Expr) and isinstance(st.value, ast.Call)):
        return False
    c = st.value
    if isinstance(c.func, ast.Name) and c.func.id in funcs and not c.args and not c.keywords:
        return True
    return (isinstance(c.func, ast.Attribute) and c.func.attr == "exit" and len(c.args) == 1 and isinstance(c.args[0], ast.Call)
            and isinstance(c.args[0].func, ast.Name) and c.args[0].func.id in funcs and not c.args[0].args)


def _literal_for(st, funcs):
    """`for v in (<top-level function names>): v()` -> the names, else None."""
    if not (isinstance(st, ast.For) and not st.orelse and isinstance(st.target, ast.Name)):
        return None
    if len(st.body) != 1 or not (isinstance(st.body[0], ast.Expr) and isinstance(st.body[0].value, ast.Call)):
        return None
    c = st.body[0].value
    if not (isinstance(c.func, ast.Name) and c.func.id == st.target.id and not c.args and not c.keywords):
        return None
    return _names_list(st.iter, funcs)


def _runner_shaped(fn, funcs, cands) -> bool:
    """A guard-called function is a runner when it reads a run list by name, or holds nothing but runner statements
    (finish, run_scenarios, bare calls of top-level functions, a literal `for` of them) and no check of its own."""
    if any(isinstance(x, ast.Name) and x.id in cands for x in ast.walk(fn)):
        return True
    if count_checks(fn):
        return False
    body = fn.body[1:] if (fn.body and isinstance(fn.body[0], ast.Expr) and isinstance(fn.body[0].value, ast.Constant)
                           and isinstance(fn.body[0].value.value, str)) else fn.body
    if not body:
        return False
    for st in body:
        if _is_bare_call_of(st, funcs) or _literal_for(st, funcs) is not None:
            continue
        if isinstance(st, ast.Expr) and isinstance(st.value, ast.Call) and (_is_finish(st.value, funcs) or _is_run(st.value)):
            continue
        return False
    return True


def analyze(text: str) -> Analysis:
    an = Analysis()
    an.text, an.lines, an.problems = text, text.split("\n"), []
    lines = an.lines
    try:
        tree = ast.parse(text)
    except SyntaxError as err:
        raise CannotRun(f"does not parse: line {err.lineno}: {err.msg}")
    an.tree = tree
    an.shebang = lines[0] if lines and lines[0].startswith("#!") else None

    def problem(line, msg):
        an.problems.append((line, msg))

    items = []
    prev_end = 0
    for node in tree.body:
        first = min([node.lineno] + [d.lineno for d in getattr(node, "decorator_list", [])])
        if first <= prev_end:
            problem(first, "two statements share a line; put each on its own line first")
        s = first
        while s - 1 > prev_end and lines[s - 2].strip().startswith("#"):
            s -= 1
        items.append({"node": node, "first": first, "start": s, "end": node.end_lineno,
                      "free": comment_chunks(lines, prev_end + 1, s - 1), "cat": "", "prev_end": prev_end})
        prev_end = node.end_lineno
    an.tail_free = comment_chunks(lines, prev_end + 1, len(lines))

    funcs = {it["node"].name for it in items if isinstance(it["node"], (ast.FunctionDef, ast.AsyncFunctionDef))}
    an.funcs = funcs
    # every `finish("<label>")` statement of the file, wherever it stands: the pool the map key `closing` points into
    an.finishes = {}
    for x in ast.walk(tree):
        if isinstance(x, ast.Expr) and isinstance(x.value, ast.Call) and _is_finish(x.value, funcs):
            c = x.value
            if len(c.args) == 1 and not c.keywords and isinstance(c.args[0], ast.Constant) and isinstance(c.args[0].value, str):
                an.finishes[x.lineno] = {"node": x, "label": c.args[0], "type": "finish"}

    def is_doc(i, node):
        return i == 0 and isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant) and isinstance(node.value.value, str)

    def calls_in(stmts):
        return [st.value for st in stmts if isinstance(st, ast.Expr) and isinstance(st.value, ast.Call)]

    # runner functions: a top-level function with a `finish(...)` / `run_scenarios(...)` statement in its body (definite), or one
    # the `if __name__` block calls AND whose body is runner-shaped (T-B1 a: a guard that calls scenarios directly must not
    # turn each scenario it calls into a runner)
    guard_called = set()
    for it in items:
        if _is_guard(it["node"]):
            for st in it["node"].body:
                if isinstance(st, ast.Expr) and isinstance(st.value, ast.Call):
                    c = st.value
                    if isinstance(c.func, ast.Name) and not c.args:
                        guard_called.add(c.func.id)
                    elif (isinstance(c.func, ast.Attribute) and c.func.attr == "exit" and len(c.args) == 1
                          and isinstance(c.args[0], ast.Call) and isinstance(c.args[0].func, ast.Name)):
                        guard_called.add(c.args[0].func.id)
    defs = {it["node"].name: it["node"] for it in items if isinstance(it["node"], ast.FunctionDef)}
    definite = {nm for nm, n in defs.items() if any(_is_finish(c, funcs) or _is_run(c) for c in calls_in(n.body))}

    def find_cands(scen_names):
        out = {}
        for it in items:
            n = it["node"]
            if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name):
                lst = _names_list(n.value, scen_names)
                if lst:
                    out[n.targets[0].id] = (it, lst)
        return out

    # functions that hold a check, directly or through a top-level function they call
    carriers = {nm for nm, n in defs.items() if count_checks(n)}
    callees = {nm: {x.func.id for x in ast.walk(n) if isinstance(x, ast.Call) and isinstance(x.func, ast.Name) and x.func.id in defs}
               for nm, n in defs.items()}
    grown = True
    while grown:
        grown = False
        for nm, cs in callees.items():
            if nm not in carriers and cs & carriers:
                carriers.add(nm)
                grown = True
    an.check_funcs = carriers

    cands0 = find_cands(funcs - definite)
    shaped = {nm for nm in guard_called - definite if nm in defs and _runner_shaped(defs[nm], funcs, cands0)}
    runners = definite | shaped
    an.runners = runners
    scen = funcs - runners
    cands = find_cands(scen)

    def refs_of(node):
        return {x.id for x in ast.walk(node) if isinstance(x, ast.Name) and x.id in cands}

    blocks, pieces, plain = [], [], []
    consumed = set()     # run lists a consumer reads
    unnamed = 0
    for i, it in enumerate(items):
        n = it["node"]
        attached = lines[it["start"] - 1:it["first"] - 1]
        marker = next((int(m.group(1)) for m in (PIECE_RE.match(l.strip()) for l in attached) if m), None)

        def next_key(marker=marker):
            nonlocal unnamed
            unnamed += 1
            return f"u{marker if marker is not None else unnamed}"

        if is_doc(i, n):
            it["cat"] = "doc"
        elif isinstance(n, (ast.Import, ast.ImportFrom)):
            it["cat"] = "import"
        elif isinstance(n, ast.Delete) and KEEP_MARK in lines[n.end_lineno - 1]:
            it["cat"] = "keepdel"          # the `del` of a path-effect import this tool wrote: header, not a segment
        elif (isinstance(n, ast.Expr) and isinstance(n.value, ast.Call) and isinstance(n.value.func, ast.Attribute)
              and n.value.func.attr in ("insert", "append") and isinstance(n.value.func.value, ast.Attribute)
              and n.value.func.value.attr == "path" and isinstance(n.value.func.value.value, ast.Name)
              and n.value.func.value.value.id == "sys"):
            it["cat"] = "path"
        elif isinstance(n, ast.FunctionDef) and n.name in runners:
            it["cat"] = "block"
            blk = Block(key=f"func:{n.name}", kind="func", start=it["start"], end=it["end"], first=it["first"], node=n)
            _fill_stmt_block(an, blk, n.body, funcs, runners, scen, cands, refs_of, problem, it["prev_end"], def_line=n.lineno)
            blocks.append(blk)
            it["blk"] = blk
        elif _is_guard(n):
            it["cat"] = "block"
            blk = Block(key=next_key(), kind="guard", start=it["start"], end=it["end"], first=it["first"], node=n)
            _fill_stmt_block(an, blk, n.body, funcs, runners, scen, cands, refs_of, problem, it["prev_end"], def_line=n.lineno)
            blocks.append(blk)
            it["blk"] = blk
        elif isinstance(n, ast.For) and not n.orelse and (
                (isinstance(n.iter, ast.Name) and n.iter.id in cands) or _names_list(n.iter, scen)):
            it["cat"] = "block"
            blk = Block(key=next_key(), kind="for", start=it["start"], end=it["end"], first=it["first"], node=n)
            if isinstance(n.iter, ast.Name):
                blk.verbatim = True
                blk.refs = refs_of(n)
                _verbatim_problems(an, n, funcs, runners, problem)
            else:
                blk.entries = [("iter", x) for x in _names_list(n.iter, scen)]
                blk.lit = "(" if isinstance(n.iter, ast.Tuple) else "["
            blocks.append(blk)
            it["blk"] = blk
        elif isinstance(n, ast.Expr) and isinstance(n.value, ast.Call) and _is_finish(n.value, funcs):
            c = n.value
            if len(c.args) == 1 and not c.keywords and isinstance(c.args[0], ast.Constant) and isinstance(c.args[0].value, str):
                it["cat"] = "finish"
                it["piece"] = Piece(it["start"], it["end"], c.args[0], c.args[0].value)
            else:
                it["cat"] = "block"
                problem(n.lineno, "a module-level finish(...) whose label is not one string literal")
        elif isinstance(n, ast.Expr) and isinstance(n.value, ast.Call) and _is_run(n.value):
            c = n.value
            lists = ([_names_list(a, scen) or ([] if isinstance(a, (ast.List, ast.Tuple)) and not a.elts else None)
                      for a in c.args] if len(c.args) == 2 and not c.keywords else None)
            it["cat"] = "block"
            blk = Block(key=next_key(), kind="run", start=it["start"], end=it["end"], first=it["first"], node=n)
            if lists is None or any(x is None for x in lists):
                problem(n.lineno, f"{RUN_NAME}(...) at module level without two literal lists of top-level functions")
            else:
                blk.stmts = [{"type": "run", "node": n, "start": it["start"], "end": it["end"], "lists": lists}]
                blk.entries = [(f"arg{k}", name) for k, x in enumerate(lists) for name in x]
            blocks.append(blk)
            it["blk"] = blk
        elif (isinstance(n, ast.Expr) and isinstance(n.value, ast.Call) and isinstance(n.value.func, ast.Name)
              and n.value.func.id in scen and not n.value.args and not n.value.keywords):
            it["cat"] = "block"
            blk = Block(key=next_key(), kind="call", start=it["start"], end=it["end"], first=it["first"], node=n)
            blk.entries = [("call", n.value.func.id)]
            blocks.append(blk)
            it["blk"] = blk
        elif isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
            it["cat"] = "def"
        elif isinstance(n, ast.ClassDef):
            it["cat"] = "class"
        elif isinstance(n, (ast.Assign, ast.AnnAssign)) and _targets(n) is not None and (
                not isinstance(n, ast.AnnAssign) or isinstance(n.target, ast.Name)):
            it["cat"] = "assign"
        else:
            it["cat"] = "statement"

    for blk in blocks:
        consumed |= blk.refs
    # a run list is a candidate that a consumer reads; the rest are ordinary names
    an.runlists = {}
    for name, (it, lst) in cands.items():
        if name in consumed:
            it["cat"] = "block"
            blk = Block(key=f"list:{name}", kind="list", start=it["start"], end=it["end"], first=it["first"], node=it["node"])
            blk.entries = [("list", x) for x in lst]
            blk.lit = "(" if isinstance(it["node"].value, ast.Tuple) else "["
            blocks.append(blk)
            it["blk"] = blk
            an.runlists[name] = blk
    an.blocks = blocks
    # module-level `finish(label)` statements are emitted with the module-level blocks, in source order
    an.pieces = [it["piece"] for it in items if it["cat"] == "finish"]

    # header and segments
    an.future, an.header, an.doc_text, an.segs, an.free_dropped = [], [], None, [], []
    an.import_bound = {}
    section = None
    for it in items:
        n, cat = it["node"], it["cat"]
        for chunk in it["free"]:
            marks = [l.strip() for l in chunk.split("\n") if MARKER_RE.match(l.strip())]
            if marks:
                section = marks[-1]
        attached = lines[it["start"] - 1:it["first"] - 1]
        for l in attached:
            if MARKER_RE.match(l.strip()):
                section = l.strip()
        if cat == "doc":
            an.doc_text = slice_text(lines, n.lineno, n.end_lineno)
            an.free_dropped += it["free"]
        elif cat == "import":
            if isinstance(n, ast.ImportFrom) and n.module == "__future__" and n.level == 0:
                an.future.append(slice_text(lines, n.lineno, n.end_lineno))
                continue
            if isinstance(n, ast.ImportFrom) and any(a.name == "*" for a in n.names):
                problem(n.lineno, "a star import cannot be reduced to the names a part uses")
            aliases = []
            for a in n.names:
                if isinstance(n, ast.Import):
                    bound = a.asname or a.name.split(".")[0]
                    spec = a.name + (f" as {a.asname}" if a.asname else "")
                else:
                    bound = a.asname or a.name
                    spec = a.name + (f" as {a.asname}" if a.asname else "")
                aliases.append((bound, spec))
                an.import_bound[bound] = n.lineno
            tail = lines[n.end_lineno - 1][len(lines[n.end_lineno - 1].encode("utf-8")[:n.end_col_offset].decode("utf-8")):].strip()
            an.header.append({"kind": "import", "node": n, "aliases": aliases, "text": slice_text(lines, n.lineno, n.end_lineno),
                              "tail": tail if tail.startswith("#") else ""})
            an.free_dropped += it["free"]
        elif cat == "path":
            src = slice_text(lines, n.lineno, n.end_lineno)
            an.header.append({"kind": "path", "node": n, "text": src, "uses": symbols_of(src)[1]})
            an.free_dropped += it["free"]
        elif cat == "keepdel":
            an.free_dropped += it["free"]
        elif cat in ("def", "class", "assign", "statement"):
            src = slice_text(lines, it["start"], it["end"])
            try:
                defined, used, gw = symbols_of(src)
            except SyntaxError:
                defined, used, gw = set(), set(), set()
            if cat in ("def", "class"):
                names = [n.name]
            elif cat == "assign":
                names = _targets(n)
            else:
                names = sorted(defined)
            used = used - set(names) if cat != "statement" else used - defined
            world = world_calls(n) if cat in ("assign", "statement") else []
            an.segs.append(Seg(kind=cat, names=names, line=n.lineno, start=it["start"], end=it["end"], text=src, free=it["free"],
                               uses=used, gwrites=gw, world=world, section=section, sha=sha(src), checks=count_checks(n)))
        else:
            an.free_dropped += it["free"]
    an.import_lines = {}
    for hd in an.header:
        if hd["kind"] == "import":
            for bound, _ in hd["aliases"]:
                an.import_lines.setdefault(bound, []).append(hd["node"].lineno)
    # T-B1 d: a file whose checks run at module level and that has no scenario in any run list is a script, not a test file
    # with scenarios; a per-part runner would have nothing to run, so the shape is refused here (the draft shows it too)
    if not any(blk.entries for blk in blocks) and not an.runlists:
        script = [s for s in an.segs if s.kind in ("assign", "statement") and s.checks]
        if script:
            problem(script[0].line, f"the file is a module-level script: {sum(s.checks for s in script)} check call site(s) in "
                                    f"{len(script)} module-level statement(s) (first here) run at import and no scenario is in a run list; "
                                    "splitting such a file is not supported by this tool (a part would have no runner): do it by hand "
                                    "or ask the Lead for a node")
    return an


def _verbatim_problems(an, node, funcs, runners, problem):
    """A block that reads a run list by name is copied as written into every part that holds a scenario of that list: a
    scenario call anywhere inside it (T-B2 class 2, found by walking every call, not only the top-level statements) would run
    once per copy."""
    loop_vars = {t.id for f in ast.walk(node) if isinstance(f, ast.For) for t in ast.walk(f.target) if isinstance(t, ast.Name)}

    def per_entry(c):
        """the call is handed the loop variable: it is the block's own once-per-entry wrapper, not an extra run"""
        return any(isinstance(y, ast.Name) and y.id in loop_vars for a in list(c.args) + [k.value for k in c.keywords]
                   for y in ast.walk(a))

    for c in (x for x in ast.walk(node) if isinstance(x, ast.Call)):
        if _is_run(c) and any(isinstance(a, (ast.List, ast.Tuple)) and a.elts for a in c.args):
            problem(c.lineno, "a block that reads a run list by name also calls run_scenarios with a non-empty literal list "
                              "(an empty `[]` is allowed)")
        if isinstance(c.func, ast.Name) and c.func.id in funcs and c.func.id not in runners and not c.args and not c.keywords:
            problem(c.lineno, "a block that reads a run list by name also calls a top-level function directly "
                              f"(`{c.func.id}()`); the copy in each part would run it once per part")
        elif isinstance(c.func, ast.Name) and c.func.id in an.check_funcs and not per_entry(c):
            problem(c.lineno, f"a block that reads a run list by name calls `{c.func.id}`, a function that holds checks; "
                              "the copy in each part would run its checks once per part")


def _fill_stmt_block(an, blk, body, funcs, runners, scen, cands, refs_of, problem, prev_end, def_line):
    """Classify the statements of a runner function or an `if __name__` block."""
    lines = an.lines
    doc = body[0] if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant) and \
        isinstance(body[0].value.value, str) and blk.kind == "func" else None
    rest = body[1:] if doc else body
    blk.refs = refs_of(blk.node)
    blk.verbatim = bool(blk.refs)
    labels = [(c.args[0], c.args[0].value) for c in (x for x in ast.walk(blk.node) if isinstance(x, ast.Call))
              if _is_finish(c, funcs) and len(c.args) == 1 and not c.keywords and isinstance(c.args[0], ast.Constant)
              and isinstance(c.args[0].value, str)]
    bad = [c for c in (x for x in ast.walk(blk.node) if isinstance(x, ast.Call)) if _is_finish(c, funcs)
           and not (len(c.args) == 1 and not c.keywords and isinstance(c.args[0], ast.Constant) and isinstance(c.args[0].value, str))]
    for c in bad:
        problem(c.lineno, "finish(...) whose label is not one string literal; the part suffix cannot be added")
    blk.label_spans = labels
    if blk.verbatim:
        _verbatim_problems(an, blk.node, funcs, runners, problem)
        return
    pe = doc.end_lineno if doc else def_line
    if doc:
        blk.doc_end = doc.end_lineno
    for st in rest:
        first = st.lineno
        s = first
        while s - 1 > pe and lines[s - 2].strip().startswith("#"):
            s -= 1
        rec = {"node": st, "start": s, "end": st.end_lineno}
        pe = st.end_lineno
        if isinstance(st, ast.Expr) and isinstance(st.value, ast.Call):
            c = st.value
            if _is_finish(c, funcs):
                rec["type"] = "finish"
                rec["label"] = c.args[0] if (len(c.args) == 1 and isinstance(c.args[0], ast.Constant)) else None
            elif _is_run(c):
                lists = [(_names_list(a, scen) or ([] if isinstance(a, (ast.List, ast.Tuple)) and not a.elts else None))
                         for a in c.args] if len(c.args) == 2 and not c.keywords else None
                if lists is None or any(x is None for x in lists):
                    problem(st.lineno, f"{RUN_NAME}(...) arguments are not two literal lists of top-level functions "
                                       "(and the block reads no run list by name)")
                    continue
                rec["type"] = "run"
                rec["lists"] = lists
                for k, x in enumerate(lists):
                    blk.entries += [(f"arg{k}", name) for name in x]
            elif isinstance(c.func, ast.Name) and c.func.id in funcs and not c.args and not c.keywords:
                rec["type"] = "call"
                rec["name"] = c.func.id
                blk.entries.append(("call", c.func.id))
            elif (isinstance(c.func, ast.Attribute) and c.func.attr == "exit" and len(c.args) == 1 and isinstance(c.args[0], ast.Call)
                  and isinstance(c.args[0].func, ast.Name) and c.args[0].func.id in funcs and not c.args[0].args):
                rec["type"] = "call"
                rec["name"] = c.args[0].func.id
                blk.entries.append(("call", c.args[0].func.id))
            else:
                problem(st.lineno, "runner statement not recognised (supported: a direct call of a top-level function, "
                                   f"{RUN_NAME}(literal lists), finish(label)): " + slice_text(lines, st.lineno, st.lineno).strip()[:60])
                continue
        elif _literal_for(st, scen) is not None:
            names = _literal_for(st, scen)
            rec["type"] = "for"
            rec["names"] = names
            rec["lit"] = "(" if isinstance(st.iter, ast.Tuple) else "["
            blk.entries += [("iter", name) for name in names]
        else:
            problem(st.lineno, "runner statement not recognised (only calls and `for v in (<scenarios>): v()` are supported in a "
                               "runner that reads no run list by name): " + slice_text(lines, st.lineno, st.lineno).strip()[:60])
            continue
        blk.stmts.append(rec)


# ------------------------------------------------------------------------------------------------------ importers

def find_importers(tests_dir: Path, stem: str, exclude: set):
    """{file name: set of names used}, plus problems and warnings. The search of spec 2.6, over the real import nodes."""
    out, problems, warnings = {}, [], []
    rx = re.compile(r"^\s*(import|from)\s+" + re.escape(stem) + r"\b", re.M)
    for path in sorted(tests_dir.glob("*.py")):
        if path.stem == stem or path.stem in exclude:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError as err:
            problems.append(f"{path.name}: cannot be read ({err})")
            continue
        textual = bool(rx.search(text))
        if stem not in text:
            continue
        try:
            tree = ast.parse(text)
        except SyntaxError:
            if textual:
                problems.append(f"{path.name}: imports {stem} but does not parse; its names cannot be read")
            continue
        names, aliases, found = set(), set(), False
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for a in node.names:
                    if a.name == stem:
                        aliases.add(a.asname or a.name)
                        found = True
            elif isinstance(node, ast.ImportFrom) and node.module == stem and node.level == 0:
                found = True
                for a in node.names:
                    if a.name == "*":
                        problems.append(f"{path.name}:{node.lineno}: `from {stem} import *` - the names it uses are unknown")
                    else:
                        names.add(a.name)
        if aliases:
            bases = set()
            for node in ast.walk(tree):
                if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name) and node.value.id in aliases:
                    names.add(node.attr)
                    bases.add(id(node.value))
                    if not isinstance(node.ctx, ast.Load):
                        problems.append(f"{path.name}:{node.lineno}: writes `{node.value.id}.{node.attr}` through the module; after "
                                        "the split the write would reach the shim, not the module that holds the name")
                elif isinstance(node, ast.Call) and node.args and isinstance(node.args[0], ast.Name) and node.args[0].id in aliases:
                    tail = node.func.attr if isinstance(node.func, ast.Attribute) else getattr(node.func, "id", "")
                    if tail in ("object", "setattr", "delattr"):
                        problems.append(f"{path.name}:{node.lineno}: `{tail}({node.args[0].id}, ...)` patches the module; after the "
                                        "split the patch would reach the shim, not the module that holds the name")
            for node in ast.walk(tree):
                if isinstance(node, ast.Name) and node.id in aliases and id(node) not in bases and isinstance(node.ctx, ast.Load):
                    warnings.append(f"{path.name}:{node.lineno}: the module `{node.id}` is used as a value; "
                                    "the names read through it cannot be listed")
                    break
        if found:
            out[path.name] = names
        elif textual:
            warnings.append(f"{path.name}: the import search matches the text but no import node names {stem}")
    return out, problems, warnings


# ------------------------------------------------------------------------------------------------------ the plan

def stem_of(name: str) -> str:
    return name[:-3] if name.endswith(".py") else name


def common_stem_for(src_stem: str) -> str:
    return (src_stem[5:] if src_stem.startswith("test_") else src_stem) + "_common"


class Plan:
    pass


def load_map(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except OSError as err:
        raise CannotRun(f"the map cannot be read: {err}")
    except ValueError as err:
        raise CannotRun(f"the map is not JSON: {err}")
    if not isinstance(data, dict):
        raise CannotRun("the map is not a JSON object")
    return data


def tests_dir_of(repo: Path, source: str):
    if "/" in source or "\\" in source:
        p = (repo / source) if not Path(source).is_absolute() else Path(source)
        return p.parent, p.name
    return repo / TESTS_REL, source


def validate_map(m: dict):
    problems = []

    def need(key, typ):
        if not isinstance(m.get(key), typ):
            problems.append(f"map key `{key}` is missing or not a {typ.__name__}")
            return False
        return True

    need("source", str)
    need("common", str)
    need("parts", list)
    need("names", list)
    if isinstance(m.get("parts"), list) and not all(isinstance(p, str) for p in m["parts"]):
        problems.append("map key `parts` must hold strings only (the part stems)")
    if not isinstance(m.get("shim"), bool):
        problems.append("map key `shim` is missing or not true/false")
    if problems:
        raise Refusal(problems)


def soundness_problems(plan, an, name_home) -> list:
    """T-B2: the shapes in which the cut would change what runs, whatever the proof counts. Every one is a refusal that fires
    before any proof and before any write."""
    out = []
    src = plan.source_name
    common = plan.common
    # 1. a module-level check homed in common runs once per part that imports it, or never
    for seg in an.segs:
        if seg.home == common and seg.kind in ("assign", "statement") and seg.checks:
            out.append(f"{src}:{seg.line}: a module-level {seg.kind} that runs {seg.checks} check call site(s) is homed in common; "
                       "it would run once per part that imports a name of it, or never: home it in a part")
    # 3. a statement (not a definition or a plain assignment) before an import: the cut puts every import above all of them
    header_lines = [hd["node"].lineno for hd in an.header]
    last_header = max(header_lines) if header_lines else 0
    for seg in an.segs:
        if seg.kind == "statement" and seg.line < last_header:
            out.append(f"{src}:{seg.line}: this statement runs before the import/sys.path line at {last_header}; the cut hoists "
                       "every import above all definitions, so their order would change: move it below the imports in the source first")
    # 4. one name bound by segments of two homes: each part would re-bind its own copy
    by_name = {}
    for seg in an.segs:
        for nm in seg.names:
            by_name.setdefault(nm, []).append(seg)
    for nm, segs in sorted(by_name.items()):
        homes = {s.home for s in segs if s.home}
        if len(homes) > 1:
            out.append(f"{src}:{','.join(str(s.line) for s in segs[:6])}: `{nm}` is bound by statements homed apart "
                       f"({', '.join(sorted(homes))}); a part would re-bind its own copy: home every binding of it together")
    # 5. an import after a def/assign of the same name wins in the source, and the hoisted import would lose
    for nm, lns in sorted(an.import_lines.items()):
        for seg in by_name.get(nm, []):
            if any(seg.line < ln for ln in lns):
                out.append(f"{src}:{seg.line}: `{nm}` is defined here and imported again later (line {max(lns)}); the cut hoists the "
                           "import above the definition, which then wins: rename one of them in the source first")
    # 6. `global` rebinding of a common name that a part reads: a part imports the value it had at import time
    readers = {}
    for seg in an.segs:
        for u in seg.uses:
            readers.setdefault(u, set()).add(seg.home)
    for blk in an.blocks:
        for x in ast.walk(blk.node):
            if isinstance(x, ast.Name):
                readers.setdefault(x.id, set()).add("(a generated runner)")
    for seg in an.segs:
        for g in sorted(seg.gwrites):
            if name_home.get(g) == common and readers.get(g, set()) - {common}:
                out.append(f"{src}:{seg.line}: `global {g}` rebinds a name homed in common that a part reads "
                           f"({', '.join(sorted(x for x in readers[g] if x != common))}); the part imports the value it had at "
                           "import time: home the writer and every reader of it in one part")
    # 7. a statement that changes a name homed elsewhere changes the copy it imported, not the one the others see
    for seg in an.segs:
        if seg.kind == "statement" and seg.home:
            for u in sorted(seg.uses):
                if u in name_home and name_home[u] and name_home[u] != seg.home:
                    out.append(f"{src}:{seg.line}: a module-level statement uses `{u}`, homed in `{name_home[u]}`, while it is homed "
                               f"in `{seg.home}`; whatever it does to `{u}` happens to a per-part copy: home it with `{u}`")
    return out


def build_plan(m: dict, repo: Path, tests_dir: Path | None = None) -> Plan:
    validate_map(m)
    plan = Plan()
    plan.map = m
    plan.tests_dir, plan.source_name = tests_dir_of(repo, m["source"]) if tests_dir is None else (tests_dir, m["source"])
    plan.src_stem = stem_of(plan.source_name)
    plan.common = m["common"]
    plan.parts = list(m["parts"])
    plan.shim = m["shim"]
    problems, warnings = [], []
    stem_rx = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
    if plan.common != common_stem_for(plan.src_stem):
        problems.append(f"`common` must be `{common_stem_for(plan.src_stem)}` (the source stem without a leading `test_`, "
                        f"plus `_common`), got `{plan.common}`")
    if not plan.parts:
        problems.append("`parts` is empty")
    seen = set()
    for p in plan.parts:
        if not isinstance(p, str) or not stem_rx.match(p):
            problems.append(f"part `{p}` is not a module name")
        elif not p.startswith(plan.src_stem + "_"):
            problems.append(f"part `{p}` must start with `{plan.src_stem}_` (naming rule 2.1)")
        elif p in seen or p == plan.common:
            problems.append(f"part `{p}` is named twice or equals the common module")
        seen.add(p)
    if problems:
        raise Refusal(problems)

    src_path = plan.tests_dir / plan.source_name
    plan.src_path = src_path
    if not src_path.is_file():
        raise CannotRun(f"{src_path} does not exist")
    raw = src_path.read_bytes()
    plan.raw = raw
    text, plan.nl = decode_source(raw, plan.source_name)
    if SHIM_MARK in text[:800]:
        plan.already_shim = True
        return plan
    plan.already_shim = False
    an = analyze(text)
    plan.an = an
    plan.text = text
    for line, msg in an.problems:
        problems.append(f"{plan.source_name}:{line}: {msg}")
    if "closing" in m and (not isinstance(m["closing"], int) or isinstance(m["closing"], bool) or m["closing"] not in an.finishes):
        problems.append(f"map key `closing` must be the line of a `finish(\"<label>\")` statement of {plan.source_name} "
                        f"(one string literal); got {m['closing']!r}; such statements are at line(s) "
                        f"{', '.join(str(k) for k in sorted(an.finishes)) or '(none)'}")
    plan.tests_names = {p.stem for p in plan.tests_dir.glob("*.py")}
    plan.import_notes, plan.reported_tests, plan.closings = {}, {}, {}

    # -- rows
    homes_ok = set(plan.parts) | {plan.common}
    rows = {}
    for row in m["names"]:
        if not isinstance(row, dict) or not all(isinstance(row.get(k), str) for k in ("name", "kind", "home")):
            problems.append(f"a `names` row without string keys name/kind/home: {row!r}")
            continue
        if row["name"] in rows:
            problems.append(f"name `{row['name']}` has two rows")
        rows[row["name"]] = row
        if row["home"] not in homes_ok:
            problems.append(f"name `{row['name']}`: home `{row['home']}` is not a part or the common module"
                            + (" (the draft leaves `home` empty on purpose)" if not row["home"] else ""))
    runner_names = set(an.runners) | set(an.runlists)
    for blk in an.blocks:
        if blk.kind == "for" and isinstance(blk.node.target, ast.Name):
            runner_names.add(blk.node.target.id)
    an.runner_names = runner_names
    by_name = {}
    for seg in an.segs:
        for nm in seg.names:
            by_name.setdefault(nm, []).append(seg)
    for nm, row in rows.items():
        if nm in runner_names:
            problems.append(f"name `{nm}` is a runner block (generated per part); delete its row")
        elif nm not in by_name:
            problems.append(f"name `{nm}` is not a top-level name of the source")
        else:
            kinds = {s.kind for s in by_name[nm] if s.kind != "statement"}
            if kinds and row["kind"] not in kinds:
                problems.append(f"name `{nm}`: kind `{row['kind']}` but the source has `{'|'.join(sorted(kinds))}` (line {by_name[nm][0].line})")
    missing = [(by_name[nm][0].line, nm) for nm in by_name if nm not in rows and nm not in runner_names
               and any(s.kind != "statement" for s in by_name[nm])]
    for line, nm in sorted(missing)[:LIST_LIMIT]:
        problems.append(f"{plan.source_name}:{line}: name `{nm}` has no row in `names`")
    if len(missing) > LIST_LIMIT:
        problems.append(f"... and {len(missing) - LIST_LIMIT} more names without a row")

    # -- statements
    placed = {}
    for row in m.get("statements") or []:
        if not isinstance(row, dict) or not isinstance(row.get("line"), int) or not isinstance(row.get("home"), str):
            problems.append(f"a `statements` row without int line / string home: {row!r}")
            continue
        placed[row["line"]] = row["home"]
        if row["home"] not in homes_ok:
            problems.append(f"statement at line {row['line']}: home `{row['home']}` is not a part or the common module")
    stmt_lines = {s.line for s in an.segs if s.kind == "statement"}
    for ln in sorted(stmt_lines - set(placed)):
        seg = next(s for s in an.segs if s.line == ln)
        problems.append(f"{plan.source_name}:{ln}: a module-level statement that is not a definition has no place "
                        f"(add it to `statements`): {seg.text.splitlines()[0].strip()[:60]}")
    for ln in sorted(set(placed) - stmt_lines):
        problems.append(f"`statements` names line {ln}, which holds no unplaced module-level statement")

    # -- homes of segments
    for seg in an.segs:
        if seg.kind == "statement":
            seg.home = placed.get(seg.line)
        else:
            hs = {rows[nm]["home"] for nm in seg.names if nm in rows and rows[nm]["home"] in homes_ok}
            if len(hs) > 1:
                problems.append(f"{plan.source_name}:{seg.line}: the targets of one statement ({', '.join(seg.names)}) "
                                f"go to different homes ({', '.join(sorted(hs))})")
            seg.home = sorted(hs)[0] if hs else None
        if seg.world and seg.home:
            warnings.append(f"WARNING: line {seg.line} runs at import and touches the world, the disk or the process "
                            f"({', '.join(sorted(set(seg.world)))}); it now runs once per part ({seg.home}): "
                            + seg.text.splitlines()[0].strip()[:70])
    if problems:
        raise Refusal(problems)

    name_home = {}
    for seg in an.segs:
        for nm in seg.names:
            name_home[nm] = seg.home
    plan.name_home = name_home
    problems += soundness_problems(plan, an, name_home)

    # -- scenarios homed in common, runner names used by segments, parts with no scenario
    for blk in an.blocks:
        for kind, nm in blk.entries:
            if nm in an.runners:
                continue
            if nm not in name_home:
                problems.append(f"run list entry `{nm}` has no home")
            elif name_home[nm] == plan.common:
                problems.append(f"scenario `{nm}` is in a run list but homed in common; home it in a part")
    for seg in an.segs:
        bad = seg.uses & runner_names
        if bad:
            problems.append(f"{plan.source_name}:{seg.line}: `{', '.join(sorted(bad))}` is a runner artifact (generated per part) "
                            "but a definition reads it")
    consumers_read = {r for blk in an.blocks for r in blk.refs}
    # -- uses between homes
    cross = {}
    for seg in an.segs:
        for u in sorted(seg.uses):
            if u in name_home and name_home[u] != seg.home and name_home[u] != plan.common:
                cross.setdefault((u, seg.home), []).append(seg.line)
        for g in sorted(seg.gwrites):
            if g in name_home and name_home[g] != seg.home:
                problems.append(f"{plan.source_name}:{seg.line}: `global {g}` rebinds a name homed in `{name_home[g]}`, not in "
                                f"`{seg.home}`; it would rebind a copy")
    for (u, user), at in sorted(cross.items()):
        where = f"{plan.source_name}:" + ",".join(str(x) for x in at[:6]) + (f" (+{len(at) - 6} more)" if len(at) > 6 else "")
        if user == plan.common:
            problems.append(f"{where}: common uses `{u}`, which is homed in `{name_home[u]}`; home `{u}` in common")
        else:
            problems.append(f"{where}: `{u}` (homed in `{name_home[u]}`) is used by `{user}`: parts never import each other; "
                            f"home `{u}` in common")
    for hd in an.header:
        if hd["kind"] == "path":
            bad = hd["uses"] & set(name_home)
            if bad:
                problems.append(f"{plan.source_name}:{hd['node'].lineno}: a sys.path line uses the top-level name(s) {', '.join(sorted(bad))}")
    if problems:
        raise Refusal(problems)

    # -- importers
    exclude = set(plan.parts) | {plan.common}
    plan.importers, iprob, iwarn = find_importers(plan.tests_dir, plan.src_stem, exclude)
    warnings += [f"WARNING: importer {w}" for w in iwarn]
    problems += [f"importer {p}" for p in iprob]
    if plan.shim and not plan.importers:
        problems.append("`shim` is true but no other test imports the source; the shim exists if and only if some test does "
                        "(spec 2.2): set `shim` to false")
    if not plan.shim and plan.importers:
        problems.append("`shim` is false but other tests import the source: " + ", ".join(
            f"{f} ({', '.join(sorted(n)) or 'the module'})" for f, n in sorted(plan.importers.items())) +
            "; set `shim` to true (spec 2.2) - an importer is never edited by a split")
    plan.shim_names, plan.shim_imports = [], []
    if plan.shim and plan.importers:
        wanted = sorted(set().union(*plan.importers.values()))
        for nm in wanted:
            if nm in name_home:
                if name_home[nm] != plan.common:
                    problems.append(f"an importer uses `{nm}`, homed in `{name_home[nm]}`; home it in common so the shim can "
                                    "re-export it without importing a part (E3)")
                else:
                    plan.shim_names.append(nm)
            elif nm in an.import_bound:
                plan.shim_imports.append(nm)
            elif nm in an.runner_names:
                problems.append(f"an importer uses `{nm}`, a runner name that is generated per part")
            else:
                problems.append(f"an importer uses `{nm}`, which the source does not define or import")
    if problems:
        raise Refusal(problems)

    # -- generate
    plan.files = {}            # file name -> text (with \n)
    plan.part_checks = {}
    plan.unreached = []
    inc_by_part = {}
    for part in plan.parts:
        text_p, entries_n = gen_part(plan, part)
        plan.files[part + ".py"] = text_p
        inc_by_part[part] = entries_n
        if entries_n == 0:
            problems.append(f"part `{part}` holds no scenario (no run list reaches a name homed there)")
    common_segs = [s for s in an.segs if s.home == plan.common]
    plan.common_written = bool(common_segs)
    if plan.common_written:
        plan.files[plan.common + ".py"] = gen_common(plan)
    elif plan.shim_names:
        problems.append("the shim re-exports names but the common module holds none")
    if plan.shim:
        plan.files[plan.source_name] = gen_shim(plan)
    if problems:
        raise Refusal(problems)
    # E8 (parts never import each other) is enforced in gen_part, on the names the generated text uses
    ref = {u for seg in an.segs for u in seg.uses} | {nm for b in an.blocks for _, nm in b.entries}
    for blk in an.blocks:
        ref |= {x.id for x in ast.walk(blk.node) if isinstance(x, ast.Name)}
    for seg in an.segs:
        if seg.kind == "def" and seg.names[0] not in ref and seg.names[0] not in set(plan.shim_names) and \
                not any(seg.names[0] in importer_names for importer_names in plan.importers.values()):
            plan.unreached.append((seg.line, seg.names[0], seg.home))
    plan.warnings = warnings
    return plan


# ------------------------------------------------------------------------------------------------------ generation

def _fmt_list(names, lit, ind=""):
    close = {"[": "]", "(": ")"}[lit]
    if not names:
        return lit + close
    body = "".join(f"\n{ind}    {n}," for n in names)
    return f"{lit}{body}\n{ind}{close}"


def _label_repl(span_node, old, suffix):
    new = '"' + old.replace("\\", "\\\\").replace('"', '\\"') + suffix + '"'
    return (span_node.lineno, span_node.col_offset, span_node.end_lineno, span_node.end_col_offset, new)


def included_blocks(plan, part):
    an = plan.an
    home = plan.name_home

    def kept(nm):
        return nm in inc if nm in an.runners else home.get(nm) == part

    inc = {}
    changed = True
    while changed:
        changed = False
        for blk in an.blocks:
            if blk.kind == "list":
                continue
            if blk.key in inc:
                continue
            if blk.verbatim:
                ok = any(any(home.get(nm) == part for _, nm in an.runlists[r].entries) for r in blk.refs)
            else:
                ok = any((nm in inc) if nm in an.runners else home.get(nm) == part for _, nm in blk.entries)
            if ok:
                inc[blk.key] = True
                if blk.kind == "func":
                    inc[blk.key[5:]] = True
                changed = True
    # `inc` also holds bare function names for the `kept` test above
    return inc


def _has_finish(an, inc) -> bool:
    """Does the runner of a part with the included blocks `inc` end in a closing call of its own?"""
    for blk in an.blocks:
        if blk.kind == "list" or blk.key not in inc:
            continue
        if blk.verbatim and blk.label_spans:
            return True
        if any(r["type"] == "finish" for r in blk.stmts):
            return True
    return bool(an.pieces) and any(blk.key in inc and blk.kind in ("for", "run", "call") for blk in an.blocks)


def _closing_candidates(an, blk, seen=()):
    """The `finish(...)` statements that close the runner block `blk`: its own, else those of the runner functions it calls."""
    if blk.verbatim:
        return []
    own = [r for r in blk.stmts if r["type"] == "finish" and r["label"] is not None]
    if own:
        return own
    out = []
    for r in blk.stmts:
        name = r.get("name")
        if r["type"] == "call" and name in an.runners and name not in seen:
            fn = next((b for b in an.blocks if b.key == "func:" + name), None)
            if fn is not None:
                out += _closing_candidates(an, fn, seen + (name,))
    return out


def pick_closing(plan, part, inc):
    """(closing record, the block that carries it) for a part whose included blocks hold no closing call: the old runner's
    own closing, found in the blocks the scenarios came from (the guard's `main()` leads to the `finish` at the end of
    `main`), or the line named by the map key `closing`. A part with no closing to find, or two different ones, is refused."""
    an = plan.an
    here = [b for b in an.blocks if b.kind != "list" and b.key in inc]
    if not here:
        return None, None            # a part with no scenario is refused by the caller
    where = f"{plan.source_name}:{min(b.first for b in here)}"
    forced = plan.map.get("closing")
    if forced is not None:
        cands = [an.finishes[forced]]
    else:
        pool = {}
        for b in here:
            if b.kind in ("func", "guard"):
                for r in _closing_candidates(an, b):
                    pool.setdefault(slice_text(an.lines, r["node"].lineno, r["node"].end_lineno).strip(), r)
        cands = list(pool.values())
        if not cands:
            raise Refusal([f"{where}: part `{part}` would have no closing call: the runner block(s) its scenarios come from "
                           "end in no `finish(<label>)` that can be found (the old runner's closing, e.g. the end of `main`); "
                           f"door: add the map key `closing` = the line of the `finish(...)` statement of {plan.source_name} to copy "
                           f"(statements at line(s) {', '.join(str(k) for k in sorted(an.finishes)) or 'none'})"])
        if len(cands) > 1:
            raise Refusal([f"{where}: part `{part}` takes its scenarios from blocks with different closings (lines "
                           f"{', '.join(str(r['node'].lineno) for r in cands)}); door: add the map key `closing` = the line of the "
                           "one `finish(...)` statement to copy"])
    carriers = [b for b in here if b.kind in ("guard", "func") and not b.verbatim]
    carriers = [b for b in carriers if b.kind == "guard"] or carriers
    if not carriers:
        raise Refusal([f"{where}: part `{part}`: no `if __name__` block or runner function of the part can carry the closing "
                       f"(line {cands[0]['node'].lineno}); the scenarios come from module-level or by-name blocks that end in no "
                       "closing call: do it by hand or ask the Lead for a node"])
    return cands[0], carriers[-1]


def _closing_text(an, rec, suffix, indent):
    """The statement of `rec` as written (its label plus the part suffix), moved to column `indent`."""
    st, lab = rec["node"], rec["label"]
    text = slice_text(an.lines, st.lineno, st.end_lineno, [_label_repl(lab, lab.value, suffix)])
    cut = st.col_offset
    return "\n".join(" " * indent + (l[cut:] if l[:cut].strip() == "" else l) for l in text.split("\n"))


def render_runner(plan, part):
    """(text, number of scenario entries kept)"""
    an = plan.an
    home = plan.name_home
    suffix = part[len(plan.src_stem):]
    inc = included_blocks(plan, part)
    lines = an.lines

    def entry_kept(nm):
        return inc.get(nm, False) if nm in an.runners else home.get(nm) == part

    closing, target = pick_closing(plan, part, inc) if not _has_finish(an, inc) else (None, None)
    out_lists, out_funcs, out_rest = [], [], []
    emitted_lists = set()
    for blk in an.blocks:
        if blk.kind == "list" or blk.key not in inc:
            continue
        for r in sorted(blk.refs):
            emitted_lists.add(r)
    scen_total = 0
    for blk in an.blocks:
        if blk.kind == "list":
            if blk.key[5:] in emitted_lists:
                names = [nm for _, nm in blk.entries if home.get(nm) == part]
                scen_total += len(names)
                out_lists.append(f"{blk.node.targets[0].id} = {_fmt_list(names, blk.lit)}")
            continue
        if blk.key not in inc:
            continue
        text = None
        if blk.verbatim:
            repls = [_label_repl(sp, old, suffix) for sp, old in blk.label_spans]
            text = slice_text(lines, blk.start, blk.end, repls)
        elif blk.kind in ("func", "guard"):
            node = blk.node
            first_stmt = blk.stmts[0]["start"]
            head = slice_text(lines, blk.start, first_stmt - 1).rstrip("\n")
            parts_t = [head]
            for rec in blk.stmts:
                st = rec["node"]
                if rec["type"] == "call":
                    if not entry_kept(rec["name"]):
                        continue
                    if rec["name"] not in an.runners:
                        scen_total += 1
                    parts_t.append(slice_text(lines, rec["start"], rec["end"]))
                elif rec["type"] == "for":
                    names = [nm for nm in rec["names"] if home.get(nm) == part]
                    if not names:
                        continue
                    scen_total += len(names)
                    it_ = st.iter
                    repl = (it_.lineno, it_.col_offset, it_.end_lineno, it_.end_col_offset,
                            _fmt_list(names, rec["lit"], " " * st.col_offset))
                    parts_t.append(slice_text(lines, rec["start"], rec["end"], [repl]))
                elif rec["type"] == "run":
                    ls = [[nm for nm in x if home.get(nm) == part] for x in rec["lists"]]
                    if not any(ls):
                        continue
                    scen_total += sum(len(x) for x in ls)
                    ind = " " * st.col_offset
                    repls = [(a.lineno, a.col_offset, a.end_lineno, a.end_col_offset, _fmt_list(x, "[", ind))
                             for a, x in zip(st.value.args, ls)]
                    parts_t.append(slice_text(lines, rec["start"], rec["end"], repls))
                else:
                    lab = rec["label"]
                    repls = [_label_repl(lab, lab.value, suffix)] if lab is not None else []
                    parts_t.append(slice_text(lines, rec["start"], rec["end"], repls))
            if blk is target:
                parts_t.append(_closing_text(an, closing, suffix, blk.stmts[0]["node"].col_offset))
                plan.closings[part] = closing["node"].lineno
            text = "\n".join(parts_t)
        elif blk.kind == "for":
            node = blk.node
            names = [nm for _, nm in blk.entries if home.get(nm) == part]
            scen_total += len(names)
            it_ = node.iter
            lit = blk.lit + ", ".join(names) + ("," if len(names) == 1 and blk.lit == "(" else "") + {"[": "]", "(": ")"}[blk.lit]
            text = slice_text(lines, blk.start, blk.end, [(it_.lineno, it_.col_offset, it_.end_lineno, it_.end_col_offset, lit)])
        elif blk.kind == "run":
            rec = blk.stmts[0]
            st = rec["node"]
            ls = [[nm for nm in x if home.get(nm) == part] for x in rec["lists"]]
            scen_total += sum(len(x) for x in ls)
            ind = " " * st.col_offset
            repls = [(a.lineno, a.col_offset, a.end_lineno, a.end_col_offset, _fmt_list(x, "[", ind)) for a, x in zip(st.value.args, ls)]
            text = slice_text(lines, rec["start"], rec["end"], repls)
        elif blk.kind == "call":
            text = slice_text(lines, blk.start, blk.end)
        if text is None:
            continue
        if blk.key.startswith("u"):
            text = f"# split: runner piece {blk.key[1:]}\n" + text
        (out_funcs if blk.kind == "func" else out_rest).append((blk.start, text))
    # module-level finish pieces go with the module-level blocks, in source order
    if any(blk.key in inc and blk.kind in ("for", "run", "call") for blk in an.blocks):
        for pc in an.pieces:
            repls = [_label_repl(pc.node, pc.label, suffix)]
            out_rest.append((pc.start, slice_text(lines, pc.start, pc.end, repls)))
    out_rest.sort(key=lambda t: t[0])
    parts_all = out_lists + [t for _, t in out_funcs] + [t for _, t in out_rest]
    return "\n\n\n".join(parts_all), scen_total


STDLIB = frozenset(getattr(sys, "stdlib_module_names", ()))      # empty before 3.10: then every module counts as non-stdlib


def _root_of(node, spec: str) -> str:
    """the top-level module an alias of an import node loads ('.' for a relative import)"""
    if isinstance(node, ast.ImportFrom):
        return (node.module or "").split(".")[0] if node.level == 0 else "."
    return spec.split(" as ")[0].split(".")[0]


def _import_text(node, spec: str) -> str:
    if isinstance(node, ast.Import):
        return f"import {spec}"
    return "from " + "." * node.level + (node.module or "") + f" import {spec}"


def header_text(plan, used, common_import, part=None, keep_path=False):
    """Imports (reduced to `used`) and sys.path lines in source order, then the common import.

    With `part` (the stem of the file being written) two things more, F1 of node N2: (1) with `keep_path` (a part, not the
    common module or the shim: a failure there is caught by proof (g)) and when the file imports any non-stdlib
    module, an import of the old file that is a LOCAL module of the tests dir (a file beside the old test, not a `test_*` file)
    and that the file uses no name of is kept as `import <module>` + `del <module>` (the module is imported for the `sys.path`
    entry it makes; the `del` leaves pyflakes no unused import), unless a kept line above already loads that module; (2) every
    import dropped is recorded in `plan.import_notes[part]`, a test file the old file imports at module level and the part does
    not use is recorded in `plan.reported_tests` - the report prints both."""
    an = plan.an
    out, dropped, kept_path, loaded = [], [], [], set()
    nonstd = bool(common_import) or any(
        _root_of(hd["node"], s) not in STDLIB for hd in an.header if hd["kind"] == "import" for b, s in hd["aliases"] if b in used)
    for hd in an.header:
        if hd["kind"] == "path":
            out.append(hd["text"])
            continue
        node = hd["node"]
        keep = [(b, s) for b, s in hd["aliases"] if b in used]
        gone = [(b, s) for b, s in hd["aliases"] if b not in used]
        if keep:
            loaded |= {_root_of(node, s) for _, s in keep}
            if len(keep) == len(hd["aliases"]):
                out.append(hd["text"])
            else:
                tail = ("  " + hd["tail"]) if hd["tail"] else ""
                if isinstance(node, ast.Import):
                    out.append("import " + ", ".join(s for _, s in keep) + tail)
                else:
                    out.append("from " + "." * node.level + (node.module or "") + " import " + ", ".join(s for _, s in keep) + tail)
        whole_from = isinstance(node, ast.ImportFrom) and not keep      # one line of the old file, every name unused
        for b, s in ([gone[0]] if whole_from else gone):
            root = _root_of(node, s)
            local = (isinstance(node, ast.ImportFrom) or "." not in s.split(" as ")[0]) and root in plan.tests_names
            if part is not None and local and root.startswith("test_"):
                plan.reported_tests.setdefault((node.lineno, root), _import_text(node, s))      # another test file: never kept
            elif part is not None and keep_path and nonstd and local and root not in loaded:
                out.append(f"import {root}  # noqa: E402")
                out.append(f"del {root}  {KEEP_MARK}")
                loaded.add(root)
                kept_path.append((node.lineno, hd["text"] if whole_from else _import_text(node, s)))
                continue
            dropped.append((node.lineno, hd["text"] if whole_from else _import_text(node, s)))
    # one entry per line of the old file: the names of a partly dropped `from` line are joined
    merged = {}
    for ln, txt in dropped:
        merged.setdefault(ln, []).append(txt)
    splitter = re.compile(r"^(.*?\bimport) (.*)$", re.S)
    dropped = [(ln, txts[0] if len(txts) == 1 else splitter.match(txts[0]).group(1) + " "
                + ", ".join(splitter.match(t).group(2) for t in txts)) for ln, txts in sorted(merged.items())]
    if part is not None:
        plan.import_notes[part] = {"dropped": dropped, "kept_path": kept_path}
    if common_import:
        names = sorted(common_import)
        one = f"from {plan.common} import " + ", ".join(names) + "  # noqa: E402"
        if len(one) <= LINE_WIDTH:
            out.append(one)
        else:
            rows, cur = [], "   "
            for nm in names:
                if len(cur) + len(nm) + 2 > LINE_WIDTH:
                    rows.append(cur)
                    cur = "   "
                cur += f" {nm},"
            rows.append(cur)
            out.append(f"from {plan.common} import (  # noqa: E402\n" + "\n".join(rows) + "\n)")
    return out


def _assemble(plan, doc, extra_comment, header, segs, runner):
    an = plan.an
    pieces = []
    if an.shebang:
        pieces.append(an.shebang)
    pieces.append(doc)
    if extra_comment:
        pieces.append(extra_comment)
    pre = "\n".join(pieces)
    head_parts = list(an.future) + header
    body = []
    for seg in segs:
        chunk = "\n\n".join(seg.free + [seg.text]) if seg.free else seg.text
        body.append(chunk)
    text = pre + "\n" + ("\n".join(head_parts) + "\n" if head_parts else "")
    if body:
        text += "\n\n" + "\n\n\n".join(body) + "\n"
    if runner:
        text += "\n\n" + runner + "\n"
    return text


def _uses_of(plan, home_name, runner_text):
    an = plan.an
    used = set()
    for seg in an.segs:
        if seg.home == home_name:
            used |= seg.uses
    if runner_text:
        used |= symbols_of(runner_text)[1]
    for hd in an.header:
        if hd["kind"] == "path":
            used |= hd["uses"]
    return used


def gen_part(plan, part):
    an = plan.an
    runner, n_scen = render_runner(plan, part)
    used = _uses_of(plan, part, runner)
    common_import = {u for u in used if plan.name_home.get(u) == plan.common}
    for u in used:
        h = plan.name_home.get(u)
        if h and h not in (part, plan.common):
            raise Refusal([f"part `{part}` uses `{u}`, homed in `{h}`: parts never import each other; home `{u}` in common"])
        if u in an.runner_names:
            raise Refusal([f"part `{part}` uses `{u}`, a runner artifact"])
    header = header_text(plan, used, common_import, part=part, keep_path=True)
    segs = [s for s in an.segs if s.home == part]
    topic = part[len(plan.src_stem) + 1:]
    doc = f'"""{topic.replace("_", " ")}: a part of {plan.source_name}, {GEN_MARK} (TD-11c). The shared helpers are in {plan.common}."""'
    plan.part_checks[part] = sum(count_checks(ast.parse(s.text)) for s in segs)
    return _assemble(plan, doc, None, header, segs, runner), n_scen


def gen_common(plan):
    an = plan.an
    segs = [s for s in an.segs if s.home == plan.common]
    used = _uses_of(plan, plan.common, "")
    header = header_text(plan, used, set(), part=plan.common)
    doc = an.doc_text if an.doc_text else f'"""Shared helpers of {plan.source_name}."""'
    plan.part_checks[plan.common] = sum(count_checks(ast.parse(s.text)) for s in segs)
    return _assemble(plan, doc, f"# Shared helpers of {plan.source_name}, {GEN_MARK} (TD-11c).", header, segs, "")


def gen_shim(plan):
    an = plan.an
    names = sorted(set(plan.shim_names) | set(plan.shim_imports))
    out = []
    if an.shebang:
        out.append(an.shebang)
    out.append(f'"""The {plan.src_stem} tests were split (TD-11c): the parts hold the checks and {plan.common} the shared helpers.')
    out.append("This module re-exports the names other tests import under the old name. It holds no check of its own: the canon")
    out.append("runs each part as its own process. `python -B " + plan.source_name + " --all` runs the parts one after the other.")
    out.append('"""')
    out.append(SHIM_MARK)
    out.append("import subprocess")
    out.append("import sys")
    out.append("from pathlib import Path")
    out.append("")
    out.append("sys.path.insert(0, str(Path(__file__).resolve().parent))")
    if plan.shim_imports:
        used = set(plan.shim_imports)
        for hd in an.header:
            if hd["kind"] == "path":
                used |= hd["uses"]
        out += [l for l in header_text(plan, used, set(), part=plan.src_stem)]
    if plan.shim_names:
        row = f"from {plan.common} import " + ", ".join(sorted(plan.shim_names))
        if len(row) + 16 <= LINE_WIDTH:
            out.append(row + "  # noqa: E402,F401")
        else:
            out.append(f"from {plan.common} import (  # noqa: E402,F401")
            out += [f"    {nm}," for nm in sorted(plan.shim_names)]
            out.append(")")
    out.append("")
    out.append("# the re-export is the point of this module: naming it in __all__ keeps it")
    out.append("__all__ = [" + ", ".join(f'"{n}"' for n in names) + "]")
    out.append("")
    out.append("PARTS = (" + ", ".join(f'"{p}"' for p in plan.parts) + ("," if len(plan.parts) == 1 else "") + ")")
    out.append("")
    out.append("")
    out.append("def main() -> int:")
    out.append('    if "--all" not in sys.argv[1:]:')
    out.append(f'        print("{plan.source_name}: no checks of its own; they are in " + ", ".join(p + ".py" for p in PARTS))')
    out.append("        return 0")
    out.append("    here = Path(__file__).resolve().parent")
    out.append("    code = 0")
    out.append("    for part in PARTS:")
    out.append('        code = subprocess.run([sys.executable, "-B", str(here / (part + ".py"))]).returncode or code')
    out.append("    return code")
    out.append("")
    out.append("")
    out.append('if __name__ == "__main__":')
    out.append("    sys.exit(main())")
    return "\n".join(out) + "\n"


# ------------------------------------------------------------------------------------------------------ the proof

def _subseq(small, big):
    it = iter(big)
    return all(x in it for x in small)


def plain_run_sites(tree, names, skip) -> list:
    """The run sites of a module read from its plain AST, without the classifier: a bare call `f()` / `sys.exit(f())` or a name
    in a list/tuple literal, where f is a top-level function of the old file; looked for in module-level code and in the
    bodies of top-level functions that hold no check of their own (the runner-like ones). Runner function names are left out."""
    out = []

    def sites_in(node):
        for x in ast.walk(node):
            if isinstance(x, ast.Expr) and isinstance(x.value, ast.Call):
                c = x.value
                if isinstance(c.func, ast.Name) and c.func.id in names and not c.args and not c.keywords:
                    out.append(c.func.id)
                elif (isinstance(c.func, ast.Attribute) and c.func.attr == "exit" and len(c.args) == 1
                      and isinstance(c.args[0], ast.Call) and isinstance(c.args[0].func, ast.Name) and c.args[0].func.id in names):
                    out.append(c.args[0].func.id)
            elif isinstance(x, (ast.List, ast.Tuple)) and isinstance(x.ctx, ast.Load):
                out.extend(e.id for e in x.elts if isinstance(e, ast.Name) and e.id in names)

    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if not count_checks(node):
                sites_in(node)
        elif not isinstance(node, ast.ClassDef):
            sites_in(node)
    return sorted(x for x in out if x not in skip)


def import_failures(plan, files: dict, names) -> list:
    """Import each of `names` in its own child process: `python -B -c "import <stem>"` with the directory that holds the written
    files and the tests dir of the target tree as the only extra path entries (the stage cannot be the tests dir itself: the
    files are not there before the proof passed), cwd a fresh temp directory outside the repo. Returns the failures, each naming
    the file (stderr tail quoted)."""
    work = Path(tempfile.mkdtemp(prefix="tsplit_import_"))
    stage, cwd = work / "stage", work / "cwd"
    stage.mkdir()
    cwd.mkdir()
    env = {k: v for k, v in os.environ.items() if k != "PYTHONPATH"}
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    bad = []
    try:
        for name, raw in files.items():
            (stage / name).write_bytes(raw)
        code = "import importlib, sys; sys.path[:0] = sys.argv[2:]; importlib.import_module(sys.argv[1])"
        for name in names:
            try:
                done = subprocess.run([sys.executable, "-B", "-c", code, stem_of(name), str(stage), str(plan.tests_dir.resolve())],
                                      cwd=str(cwd), env=env, capture_output=True, text=True, encoding="utf-8", errors="replace",
                                      timeout=IMPORT_TIMEOUT)
            except subprocess.TimeoutExpired:
                bad.append(f"{name}: timed out after {IMPORT_TIMEOUT} s")
                continue
            if done.returncode != 0:
                tail = " | ".join(l.strip() for l in done.stderr.strip().splitlines()[-4:])
                bad.append(f"{name}: exit {done.returncode}: {tail[-500:]}")
    finally:
        shutil.rmtree(work, ignore_errors=True)
    return bad


def prove(plan, files: dict, imports: bool = False):
    """files: file name -> bytes as written. Returns (lines, ok). `imports`: also run proof (g), the child-process imports."""
    an = plan.an
    lines, ok = [], True
    texts, trees, ans = {}, {}, {}
    for name, raw in sorted(files.items()):
        try:
            text, nl = decode_source(raw, name)
        except Refusal as err:
            return [f"(0) {err.problems[0]}", "PROOF: FAILED"], False
        if nl != plan.nl:
            lines.append(f"(0) {name}: newline style differs from the source")
            ok = False
        texts[name] = text
        try:
            trees[name] = ast.parse(text)
        except SyntaxError as err:
            lines.append(f"(e) {name}: does not parse: line {err.lineno}: {err.msg}")
            ok = False
    if not ok and len(trees) != len(texts):
        lines.append("PROOF: FAILED")
        return lines, False
    for name in sorted(files):
        if name == plan.source_name and plan.shim:
            continue
        a = analyze(texts[name])
        ans[name] = a
        for line, msg in a.problems:
            lines.append(f"(0) {name}:{line}: {msg}")
            ok = False

    # (a) check-call sites
    src_n = count_checks(an.tree)
    per = {n: count_checks(trees[n]) for n in sorted(files)}
    parts_n = sum(per.get(p + ".py", 0) for p in plan.parts)
    common_n = per.get(plan.common + ".py", 0)
    shim_n = per.get(plan.source_name, 0) if plan.shim else 0
    good = src_n == parts_n + common_n + shim_n
    ok &= good
    lines.append(f"(a) check call sites (AST sites, not executed checks): source {src_n}, parts {parts_n} + common {common_n} "
                 f"+ shim {shim_n} = {parts_n + common_n + shim_n} -> {'ok' if good else 'FAILED'}")

    # (b) names
    def names_of(a):
        out = []
        for seg in a.segs:
            out += seg.names
        return out

    src_names = sorted(names_of(an))
    # a run list that is empty in a part is a plain assignment when the part is read again: it is a runner name, excepted
    after_names = sorted(n for n in sum((names_of(ans[x]) for x in ans), []) if n not in an.runner_names)
    excepted = sorted(an.runner_names)
    good = src_names == after_names
    dups = sorted({n for n in src_names if src_names.count(n) > 1})
    detail = ""
    if not good:
        miss = sorted(set(src_names) - set(after_names))
        extra = sorted(set(after_names) - set(src_names))
        detail = f" (missing: {miss[:8]}, extra: {extra[:8]}, counts differ: {[n for n in set(src_names) if src_names.count(n) != after_names.count(n)][:8]})"
    for part, file in [(p, p + ".py") for p in plan.parts] + [(plan.common, plan.common + ".py")]:
        if file in ans:
            want = sorted(n for seg in an.segs if seg.home == part for n in seg.names)
            if sorted(n for n in names_of(ans[file]) if n not in an.runner_names) != want:
                good = False
                detail += f" ({file} does not hold exactly the names homed there)"
    ok &= good
    lines.append(f"(b) top-level names: source {len(src_names)}, parts + common {len(after_names)}"
                 f"{', defined twice in the source: ' + str(dups) if dups else ', each exactly once'}; "
                 f"generated runner names excepted: {excepted} -> {'ok' if good else 'FAILED' + detail}")
    if plan.shim:
        shim_text = texts.get(plan.source_name, "")
        try:
            shim_tree = ast.parse(shim_text)
        except SyntaxError:
            shim_tree = None
        bad_shim = []
        if shim_tree is not None:
            exported = set()
            for node in ast.walk(shim_tree):
                if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "__all__" for t in node.targets):
                    exported = {e.value for e in node.value.elts}
            bound = set()
            for node in shim_tree.body:
                if isinstance(node, (ast.Import, ast.ImportFrom)):
                    bound |= {(a.asname or a.name.split(".")[0]) for a in node.names}
                elif isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                    bound.add(node.name)
            bad_shim = sorted(exported - bound)
            test_defs = [n.name for n in ast.walk(shim_tree) if isinstance(n, ast.FunctionDef) and n.name.startswith("test_")]
            want = set(plan.shim_names) | set(plan.shim_imports)
            if exported != want or bad_shim or test_defs:
                bad_shim = bad_shim or ["__all__ differs from the names the importers use"]
        good = not bad_shim and shim_tree is not None
        ok &= good
        lines.append(f"(b) shim: re-exports {len(plan.shim_names) + len(plan.shim_imports)} name(s), all resolvable, no test_* "
                     f"function -> {'ok' if good else 'FAILED ' + str(bad_shim)}")

    # (c) the run list
    src_entries = {b.key: list(b.entries) for b in an.blocks}
    got = {}
    order_bad, ref_bad = [], []
    for name, a in ans.items():
        for b in a.blocks:
            got.setdefault(b.key, []).append((name, list(b.entries)))
            if b.verbatim:
                for r in b.refs:
                    if r not in a.runlists and r not in names_of(a):
                        ref_bad.append(f"{name}: reads run list {r}, which it does not define")
    detail = []
    for key in sorted(set(src_entries) | set(got)):
        want = src_entries.get(key)
        if want is None:
            detail.append(f"block {key} is not in the source")
            continue
        # an entry that names a runner function is a LINK (each part that holds the runner repeats it): only scenarios are summed
        union = sorted(e for _, es in got.get(key, []) for e in es if e[1] not in an.runners)
        scen_want = sorted(e for e in want if e[1] not in an.runners)
        if union != scen_want:
            detail.append(f"{key}: entries differ (source {len(scen_want)}, parts {len(union)}; differing "
                          f"{[e for e in set(scen_want) | set(union) if scen_want.count(e) != union.count(e)][:6]})")
        for fname, e in got.get(key, []):
            if not _subseq(e, want):
                order_bad.append(f"{key} in {fname}")
    total_src = sum(1 for b in an.blocks if b.kind in ("list", "for", "run", "call", "func", "guard") for k, nm in b.entries
                    if nm not in an.runners)
    total_got = sum(1 for name, a in ans.items() for b in a.blocks for k, nm in b.entries if nm not in a.runners)
    bad = detail + [f"order differs: {o}" for o in order_bad] + ref_bad
    ok &= not bad
    lines.append(f"(c) run list: {total_src} scenario entries in the source, {total_got} across the parts, each in its own list, "
                 f"source order kept inside each part -> {'ok' if not bad else 'FAILED ' + '; '.join(bad[:5])}")
    # (c2) the same list read a second, independent way: the plain AST of the old file against the plain AST of the new ones
    # (it shares only the names of the runner functions with the classifier, to leave them out)
    all_defs = {n.name for n in an.tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))}
    old_sites = plain_run_sites(an.tree, all_defs, an.runners)
    new_sites = sorted(x for n, t in trees.items() if not (plan.shim and n == plan.source_name)
                       for x in plain_run_sites(t, all_defs, an.runners))
    good = old_sites == new_sites
    ok &= good
    miss = sorted(set(x for x in old_sites + new_sites if old_sites.count(x) != new_sites.count(x)))
    lines.append(f"(c2) run sites read again from the plain AST of the old file ({len(old_sites)}) against the new files "
                 f"({len(new_sites)}), classifier not used -> "
                 f"{'ok' if good else 'FAILED differing: ' + str(miss[:6])}")

    # (d) byte identity
    src_by_home = {}
    for seg in an.segs:
        src_by_home.setdefault(seg.home, []).append((seg.key, seg.sha))
    bad = []
    count = 0
    for home, rows in sorted(src_by_home.items()):
        file = home + ".py"
        if file not in ans:
            bad.append(f"{file} was not generated")
            continue
        after = [(s.key, s.sha) for s in ans[file].segs]
        count += len(rows)
        for name, h in rows:
            if (name, h) not in after:
                bad.append(f"{name} in {file}")
            else:
                after.remove((name, h))
        if after:
            bad.append(f"{file} holds {len(after)} segment(s) the source does not: {[n for n, _ in after][:4]}")
    ok &= not bad
    lines.append(f"(d) byte identity: sha256 of {count} moved segments before == after -> "
                 f"{'ok' if not bad else 'FAILED ' + '; '.join(bad[:5])}")

    # (e) compile
    bad = []
    for name in sorted(texts):
        try:
            compile(texts[name], name, "exec", dont_inherit=True)
        except (SyntaxError, ValueError) as err:
            bad.append(f"{name}: {err}")
    ok &= not bad
    lines.append(f"(compile) {len(texts)} written file(s) compile -> {'ok' if not bad else 'FAILED ' + '; '.join(bad)}")
    # (f) closing: every part's runner ends with exactly one closing call (F2 of node N2: a part without it prints no tally)
    bad = []
    for p in plan.parts:
        a = ans.get(p + ".py")
        if a is None:
            continue
        n = len(a.pieces) + sum(len(b.label_spans) if b.verbatim else sum(1 for r in b.stmts if r["type"] == "finish")
                                for b in a.blocks if b.kind != "list")
        if n != 1:
            bad.append(f"{p}.py holds {n}")
    ok &= not bad
    lines.append(f"(f) closing: each of {len(plan.parts)} part runner(s) holds exactly one closing call (finish) -> "
                 f"{'ok' if not bad else 'FAILED ' + '; '.join(bad)}")

    # (g) import: each part and the shim is imported alone in a child process (module-level code runs; the runner does not)
    if imports:
        names = [p + ".py" for p in plan.parts] + ([plan.source_name] if plan.shim else [])
        bad = import_failures(plan, files, names)
        ok &= not bad
        lines.append(f"(g) import: {len(names)} written file(s) ({', '.join(names)}) each imported alone in a child process, cwd "
                     f"outside the repo, the written files and the tests dir of the target tree as the only extra path entries, "
                     f"exit 0 required -> {'ok' if not bad else 'FAILED ' + '; '.join(bad)}")
    lines.append("NOT RUN HERE: spec 2.5 (e) (each part run alone, its tally pasted), the executed-check count of the old file "
                 "against the sum of the new ones, and the reverse-order run (brief, item 9) are the node's own runs; (g) "
                 "imports each file but does not run its runner, so it proves that every module a file imports can be found, "
                 "not that a scenario passes")
    lines.append("PROOF: " + ("ok" if ok else "FAILED"))
    return lines, ok


# ------------------------------------------------------------------------------------------------------ output

def to_bytes(plan, text: str) -> bytes:
    return text.replace("\n", plan.nl).encode("utf-8")


def row_block(plan) -> list:
    total = sum(plan.part_checks.get(p, 0) for p in plan.parts) or 1
    out = ["ROW BLOCK (the integrator writes the registries; this tool writes none)"]
    old = plan.source_name
    if plan.shim:
        out.append(f'  test-layers.json keep `{old}`: re-row as the shim: layer "data_join", why "split shim: re-exports for '
                   f'{", ".join(sorted(plan.importers))}; checks live in {", ".join(p + ".py" for p in plan.parts)}", '
                   f'covers ["tests/{plan.common}.py"]')
    else:
        out.append(f"  test-layers.json keep `{old}`: remove the row (the file is deleted); the `keep-split` / split-keep door carries it")
    for p in plan.parts:
        out.append(f'  test-layers.json keep: add `{p}.py` - inherit layer/why(+" (part of {old} split, TD-11c)")/named_by/'
                   f'replaced_by from `{old}`; covers = inherited, then narrowed, plus "tests/{plan.common}.py" '
                   f"(this part: {plan.part_checks.get(p, 0)} of {total} check-call sites)")
    out.append(f"  slow_tests.json: remove `{old}`; add each part, provisional seconds = round(old x part check sites / {total}, 1)")
    out.append(f"  selftest.py TEST_TIMEOUTS: remove the row of `{old}` if it has one (parts get no row)")
    out.append(f"  carrier search (spec 2.7): git grep -n \"{plan.src_stem}.py\" -- ai-packages docs/SIBLING_MAP.md "
               "plans/builder-rules.md .github .gitlab-ci.yml")
    return out


def report(plan, proof_lines, mode):
    out = [f"{mode}: {plan.source_name} -> {len(plan.parts)} part(s)" + (f" + {plan.common}.py" if plan.common_written else "")
           + (" + shim" if plan.shim else " (the source is deleted)")]
    an = plan.an
    for p in plan.parts:
        n = sum(1 for s in an.segs if s.home == p)
        out.append(f"  {p}.py: {n} segment(s), {plan.part_checks.get(p, 0)} check-call site(s)")
    if plan.common_written:
        out.append(f"  {plan.common}.py: {sum(1 for s in an.segs if s.home == plan.common)} segment(s), "
                   f"{plan.part_checks.get(plan.common, 0)} check-call site(s)")
    if plan.importers:
        out.append("IMPORTERS found (spec 2.6): " + "; ".join(f"{f}: {', '.join(sorted(n)) or '(the module)'}"
                                                              for f, n in sorted(plan.importers.items())))
    else:
        out.append("IMPORTERS found (spec 2.6): none")
    for line, nm, home in plan.unreached:
        out.append(f"UNREACHED: `{nm}` (line {line}, home {home}) is run by no list and used by nothing; moved with its section, "
                   "added to no runner (E11)")
    if any("argv" in slice_text(an.lines, b.start, b.end) for b in an.blocks if b.kind != "list"):
        out.append("ARGV: the source selects scenarios by argv; a name given to a part that does not hold it runs nothing there "
                   "(E14). Where each scenario lives:")
        for p in plan.parts:
            held = [nm for b in an.blocks for _, nm in b.entries if nm not in an.runners and plan.name_home.get(nm) == p]
            out.append(f"  ARGV {p}.py: " + (", ".join(held) if held else "(none)"))
    for p in plan.parts:
        if p in plan.closings:
            out.append(f"CLOSING: {p}.py got the old runner's closing (line {plan.closings[p]}: "
                       f"{slice_text(an.lines, plan.closings[p], plan.closings[p]).strip()}), label with the part suffix; "
                       "its own blocks hold none")
    for file, notes in sorted(plan.import_notes.items()):
        one = lambda items: "; ".join(f"line {ln}: `{' '.join(txt.split())}`" for ln, txt in items)
        if notes["kept_path"]:
            out.append(f"KEPT FOR ITS sys.path EFFECT: {file}.py keeps (as `import <module>` + `del <module>`) {one(notes['kept_path'])}")
        if notes["dropped"]:
            out.append(f"DROPPED IMPORT: {file}.py does not use {one(notes['dropped'])}")
    for (ln, root), txt in sorted(plan.reported_tests.items()):
        out.append(f"REPORTED: {plan.source_name}:{ln}: `{' '.join(txt.split())}` imports the test file `{root}` at module level; "
                   "a part imports only harness, story_run_common, its common and package modules (spec 2.8), so a part that "
                   "uses none of its names does not keep it")
    out += plan.warnings
    dropped =len([c for c in an.free_dropped]) + len(an.tail_free)
    if dropped:
        out.append(f"NOTE: {dropped} free comment block(s) above the header, the imports or at the end of the file are not carried")
    out += proof_lines
    out += row_block(plan)
    return out


def targets_state(plan):
    """Refuse a half-written target; returns the list of files already identical."""
    problems, same = [], []
    for name, text in plan.files.items():
        path = plan.tests_dir / name
        if name == plan.source_name:
            continue
        if path.exists():
            if path.read_bytes() == to_bytes(plan, text):
                same.append(name)
            else:
                problems.append(f"{path.name} exists and the map does not fully explain it (a half-written split?); "
                                "remove it or fix the map")
    return problems, same


def done_state(m, tests_dir: Path, source_name: str):
    """The source is a shim or gone: is the split complete? Returns (ok, problems)."""
    problems = []
    for p in m["parts"] + [m["common"]]:
        f = tests_dir / (p + ".py")
        if p == m["common"] and not any(r.get("home") == p for r in m["names"] if isinstance(r, dict)):
            continue
        if not f.is_file():
            problems.append(f"{f.name} is missing while the source is already replaced (a half-written split)")
            continue
        try:
            text, _ = decode_source(f.read_bytes(), f.name)
            tree = ast.parse(text)
        except (Refusal, SyntaxError) as err:
            problems.append(f"{f.name}: {err}")
            continue
        defined = set()
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)):
                defined.add(node.name)
            elif isinstance(node, (ast.Assign, ast.AnnAssign)):
                defined |= set(_targets(node) or [])
        for r in m["names"]:
            if isinstance(r, dict) and r.get("home") == p and r.get("name") not in defined:
                problems.append(f"{f.name} lacks `{r.get('name')}`, which the map homes there (a half-written split?)")
    return not problems, problems


def run_map(args) -> int:
    repo = Path(args.repo).resolve()
    m = load_map(Path(args.map))
    validate_map(m)
    tests_dir, source_name = tests_dir_of(repo, m["source"])
    src_path = tests_dir / source_name
    if not src_path.exists() and not m["shim"]:
        ok, problems = done_state(m, tests_dir, source_name)
        if ok:
            print(f"nothing to do: {source_name} is already split into {len(m['parts'])} part(s)")
            return 0
        raise Refusal(problems)
    plan = build_plan(m, repo)
    if plan.already_shim:
        ok, problems = done_state(m, tests_dir, source_name)
        if not ok:
            raise Refusal(problems)
        print(f"nothing to do: {source_name} is already a shim over {len(m['parts'])} part(s)")
        return 0
    problems, same = targets_state(plan)
    if problems:
        raise Refusal(problems)
    files = {n: to_bytes(plan, t) for n, t in plan.files.items()}
    proof, ok = prove(plan, files, imports=args.dry_run)
    if not ok:
        raise Refusal(["the proof failed (nothing was written):"] + ["  " + l for l in proof])
    if args.dry_run:
        for l in report(plan, proof, "DRY RUN (nothing written)"):
            print(l)
        return 0
    # apply: temp names first, re-read, prove again, rename
    temps = {}
    try:
        for name, data in files.items():
            tmp = plan.tests_dir / ("." + name + ".split-tmp")
            tmp.write_bytes(data)
            temps[name] = tmp
        reread = {n: t.read_bytes() for n, t in temps.items()}
        proof, ok = prove(plan, reread, imports=True)
        if not ok:
            raise Refusal(["the proof over the written temp files failed (the tree is untouched):"] + ["  " + l for l in proof])
        placed = []
        try:
            for name in [n for n in files if n != plan.source_name]:
                os.replace(temps[name], plan.tests_dir / name)
                placed.append(name)
            if plan.shim:
                os.replace(temps[plan.source_name], plan.src_path)
            else:
                os.remove(plan.src_path)
        except OSError as err:
            for name in placed:
                if name in same:       # it was there, byte-identical, before this run: never deleted by the rollback
                    continue
                try:
                    os.remove(plan.tests_dir / name)
                except OSError:
                    pass
            if not plan.src_path.exists():
                plan.src_path.write_bytes(plan.raw)
            raise CannotRun(f"a rename failed ({err}); the split was rolled back")
    finally:
        for t in temps.values():
            try:
                if t.exists():
                    t.unlink()
            except OSError:
                pass
    for l in report(plan, proof, "APPLIED"):
        print(l)
    return 0


def run_draft(args) -> int:
    repo = Path(args.repo).resolve()
    p = Path(args.draft)
    path = p if p.is_absolute() else (repo / p)
    if not path.is_file() and p.is_file():
        path = p.resolve()
    if not path.is_file():
        raise CannotRun(f"{args.draft} does not exist")
    text, nl = decode_source(path.read_bytes(), path.name)
    an = analyze(text)
    stem = stem_of(path.name)
    importers, iprob, iwarn = find_importers(path.parent, stem, set())
    problems = [f"{path.name}:{ln}: {msg}" for ln, msg in an.problems] + [f"importer {x}" for x in iprob]
    runs = {}
    for blk in an.blocks:
        for kind, nm in blk.entries:
            runs.setdefault(nm, []).append(blk.key[5:] if kind == "list" else f"{blk.key}:{kind}")
    runner_names = set(an.runners) | set(an.runlists)
    for blk in an.blocks:
        if blk.kind == "for" and isinstance(blk.node.target, ast.Name):
            runner_names.add(blk.node.target.id)
    out = ["{", f'  "source": {json.dumps(path.name)},', f'  "common": {json.dumps(common_stem_for(stem))},',
           f'  "shim": {json.dumps(bool(importers))},', '  "parts": [],', '  "names": [']
    rows, last_section, stmts = [], None, []
    n_def = n_class = n_assign = 0
    for seg in an.segs:
        if seg.kind == "statement":
            stmts.append({"line": seg.line, "home": "", "_text": seg.text.splitlines()[0].strip()[:70],
                          "_defines": seg.names[:6]})
            continue
        for nm in seg.names:
            row = {"name": nm, "kind": seg.kind, "home": "", "_line": seg.line}
            if seg.section and seg.section != last_section:
                row["_section"] = seg.section[:90]
                last_section = seg.section
            if nm in runs:
                row["_runs"] = runs[nm]
            if seg.world:
                row["_world"] = sorted(set(seg.world))
            rows.append(json.dumps(row, ensure_ascii=True))
            n_def += seg.kind == "def"
            n_class += seg.kind == "class"
            n_assign += seg.kind == "assign"
    out.append(",\n".join("    " + r for r in rows))
    out.append("  ],")
    out.append('  "statements": [' + (("\n" + ",\n".join("    " + json.dumps(s, ensure_ascii=True) for s in stmts) + "\n  ") if stmts else "") + "],")
    notes = {"runner_blocks": [{"key": b.key, "kind": b.kind, "line": b.first, "entries": len(b.entries),
                                "reads_run_lists": sorted(b.refs)} for b in an.blocks],
             "runner_names_not_in_names": sorted(runner_names),
             "run_lists": {k: len(v.entries) for k, v in an.runlists.items()},
             "importers": {f: sorted(n) for f, n in sorted(importers.items())},
             "refused": problems,
             "warnings": iwarn}
    out.append('  "_notes": ' + json.dumps(notes, ensure_ascii=True))
    out.append("}")
    print("\n".join(out))
    print(f"draft: {path.name}: {n_def + n_class + n_assign} names ({n_def} defs, {n_class} classes, {n_assign} assignments), "
          f"{len(stmts)} unplaced statement(s), {len([b for b in an.blocks if b.kind != 'list'])} runner block(s) + "
          f"{len(an.runlists)} run list(s) ({sum(len(v.entries) for v in an.runlists.values())} listed scenarios), "
          f"{len(importers)} importer file(s) ({len(set().union(*importers.values())) if importers else 0} names), "
          f"{len(problems)} refused construct(s)", file=sys.stderr)
    for pr in problems:
        print("REFUSED: " + pr, file=sys.stderr)
    return 2 if problems else 0


class _Parser(argparse.ArgumentParser):
    def error(self, message):
        raise CannotRun(message)


def main(argv=None) -> int:
    ap = _Parser(prog="test_split.py", description=__doc__.split("\n")[0])
    ap.add_argument("--map")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--draft")
    ap.add_argument("--repo", default=".")
    try:
        args = ap.parse_args(argv)
        if args.draft:
            if args.map or args.apply or args.dry_run:
                raise CannotRun("--draft takes no --map / --dry-run / --apply")
            return run_draft(args)
        if not args.map or (args.dry_run == args.apply):
            raise CannotRun("give --map with exactly one of --dry-run / --apply, or --draft <test file>")
        return run_map(args)
    except Refusal as err:
        for p in err.problems:
            print("REFUSED: " + p)
        print("refused: nothing was written")
        return 2
    except CannotRun as err:
        print(f"cannot run: {err}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
