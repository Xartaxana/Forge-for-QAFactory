"""Duplicate-code report -- a MEASUREMENT of copied logic in Python sources (BACKLOG B-309, t-420).

A report, not a gate: it reads, it prints, it exits 0 when the run completes. No baseline, no threshold
that turns red. What it is for: a person (or the Lead) sees where the same logic lives in two places
before the third copy is written. (The gate built on its JSON is tools/dup_ratchet.py, B-417: the
`fingerprint` of every group and `fingerprint_basis.normalisation` exist for it.)

Usage:
  python tools/dup_report.py [--repo PATH] [--paths GLOB ...] [--exclude GLOB ...] [--min-statements N]
                             [--window N] [--top N] [--strict] [--with-imports] [--json]
    --repo PATH          the repository root (default: the parent of tools/); every path in the output is
                         relative to it, with forward slashes, so the output carries no machine-specific text
    --paths GLOB ...     what to read, globs relative to --repo (default: ai-packages/qa-factory/scripts/*.py,
                         the product scripts; tests and tools are separate runs: --paths
                         "ai-packages/qa-factory/scripts/tests/*.py", --paths "tools/*.py")
    --exclude GLOB ...   files to drop from that set: every path matching one of these globs (fnmatch on the
                         repo-relative POSIX path, e.g. "tools/test_*.py"); the options of the JSON carry `exclude`
                         only when something is excluded
    --min-statements N   function clones: the smallest body that counts (default 5)
    --window N           fragment clones: consecutive statements per window (default 6)
    --top N              how many groups to print (default 40); the head still counts all of them
    --strict             keep literal values too (see "Normalisation")
    --with-imports       let import statements and `sys.path.insert/append(...)` count in fragment windows (by
                         default they break a window, so a block of imports is never a clone)
    --json               the same data as JSON instead of markdown

What is measured
  (A) FUNCTION CLONES: every function and method body (nested ones included) is normalised and hashed;
      functions with the same hash and at least --min-statements statements form a group.
  (B) FRAGMENT CLONES: inside every statement list (a module, a class body, a function body, the body of
      an if/for/while/try/with/match branch) a sliding window of --window consecutive statements is
      normalised and hashed; the same window in two places is a clone. Windows over adjacent positions
      that are copied together are merged into ONE maximal run, reported once. A window never contains a
      `def` or `class` statement, so it never spans two functions (a function body is its own list); unless
      --with-imports is given it never contains an `import` / `from ... import` statement or a
      `sys.path.insert(...)` / `sys.path.append(...)` bootstrap line either (they break a window the same
      way; the options line says `imports excluded`). A repeated block inside ONE function is a fragment with every range listed; copies of a group that
      overlap each other in one statement list are thinned to non-overlapping ones (a table of identical
      calls reports every non-overlapping stretch, not every start position).
  A fragment group that lies wholly inside the members of ONE larger function-clone group is dropped (it
  would say the same thing twice); the head counts those. A function group wholly inside the members of
  a larger function group is dropped the same way.

Normalisation (what is abstracted, what is NOT -- the claim is "same logic", so the tool must not make
different logic equal):
  abstracted : names of LOCAL variables and parameters (including loop variables, `with ... as` names,
               `except ... as` names, names of nested defs), renamed by order of first appearance, so
               `a + b` and `c + d` are equal but `a + b` and `a + a` are not; literal values (a string,
               an int, a float ... become a placeholder carrying only the literal's TYPE); docstrings and
               comments (a docstring is only the first statement of a body); annotations.
  KEPT       : operators, the shape of every call, attribute names (`x.status` is not `x.verdict`),
               keyword-argument names, global / imported / builtin names (`json.dumps` is not `yaml.dump`),
               import statements, None / True / False / ..., statement kinds and nesting.
  --strict   : keeps literal values as well, so two functions that differ only in a constant are different.
  Windows number local names from the window's own first appearance, so the position of a fragment inside
  its function does not change its fingerprint. Module-level and class-level names are not local: kept.

Output: markdown -- a head (options, files read, functions, clone groups, duplicated lines and their share),
the unreadable files, then the groups sorted by (statements x copies) descending; each group names its
kind, statements, lines (the longest copy), copies, and every location as `path:first-last` with the
function (or class, or <module>) it sits in. "Duplicated lines" is the union of the line ranges of every
copy of every kept group (each physical line once), over the physical lines of the files read.
Determinism: the output is a pure function of the tree -- sorted, no timestamps, no absolute paths. The wall
time goes to stderr only.

Known limit: when three or more copies share a stretch and only some of them continue it further, the
stretch is reported as separate runs per distinct set of copies (they overlap in the shared part); a pair
is always merged into its maximal run when the copies of the stretch are exactly that pair.

Exit codes: 0 the run completed (a clone-free tree and an empty set are reports too); 2 a usage error
(an unknown option, a value that is not a number or is out of range, --repo not a directory, a --paths glob
that is absolute outside --repo).
"""
from __future__ import annotations

import argparse
import ast
import fnmatch
import hashlib
import json
import re
import sys
import time
from pathlib import Path

import streams

REPO = Path(__file__).resolve().parent.parent
DEFAULT_PATHS = ("ai-packages/qa-factory/scripts/*.py",)
# Bump whenever `ser` / `renumber` / `digest` / the grouping changes: every group fingerprint below moves with
# them, and tools/dup-baseline.json (tools/dup_ratchet.py) must be regenerated in the same commit.
NORMALISATION = 1
DEFAULT_MIN_STATEMENTS = 5
DEFAULT_WINDOW = 6
DEFAULT_TOP = 40
RECURSION_LIMIT = 6000          # a long `a + b + ...` chain is a deep tree; a file that still overflows is "unreadable"

_DEFS = (ast.FunctionDef, ast.AsyncFunctionDef)
_BREAKERS = (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)
_SKIP_FIELDS = frozenset({"ctx", "type_comment", "kind", "type_params", "annotation", "returns"})
_BINDING_STRINGS = frozenset({("FunctionDef", "name"), ("AsyncFunctionDef", "name"), ("ClassDef", "name"),
                              ("ExceptHandler", "name"), ("alias", "asname"), ("MatchAs", "name"),
                              ("MatchStar", "name"), ("MatchMapping", "rest")})
_MARK = re.compile("\x00([^\x00]*)\x00")


class UsageError(Exception):
    """The command line cannot be served; main() prints the sentence and returns 2."""


# ---------------------------------------------------------------- normalisation

def strip_doc(body):
    """The body without its docstring (the first statement, when it is a bare string)."""
    if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant) \
            and isinstance(body[0].value.value, str):
        return body[1:]
    return body


def is_import_statement(stmt) -> bool:
    """`import x`, `from x import y`, and the `sys.path.insert(...)` / `sys.path.append(...)` bootstrap line:
    the statements every module of a package starts with, which say nothing about shared logic."""
    if isinstance(stmt, (ast.Import, ast.ImportFrom)):
        return True
    if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Call):
        fn = stmt.value.func
        return (isinstance(fn, ast.Attribute) and fn.attr in ("insert", "append")
                and isinstance(fn.value, ast.Attribute) and fn.value.attr == "path"
                and isinstance(fn.value.value, ast.Name) and fn.value.value.id == "sys")
    return False


def child_blocks(stmt):
    """The statement lists directly inside a statement (a def/class body has its docstring stripped)."""
    if isinstance(stmt, _BREAKERS):
        return [strip_doc(stmt.body)]
    blocks = []
    for _, value in ast.iter_fields(stmt):
        if isinstance(value, list) and value:
            if all(isinstance(v, ast.stmt) for v in value):
                blocks.append(value)
            else:
                for v in value:
                    if isinstance(v, (ast.ExceptHandler, ast.match_case)):
                        blocks.append(v.body)
    return blocks


def count_stmts(stmts) -> int:
    """Statements in a list, nested ones included (docstrings are not statements)."""
    n = 0
    for s in stmts:
        n += 1
        for blk in child_blocks(s):
            n += count_stmts(blk)
    return n


def collect_locals(fn) -> frozenset:
    """Names bound inside a function: parameters, assignment / loop / with / walrus targets, `except ... as`
    names, nested def and class names; minus whatever the function declares global or nonlocal. Imports are
    NOT local on purpose: `json` and `yaml` stay different."""
    names, declared = set(), set()
    for n in ast.walk(fn):
        t = type(n)
        if t is ast.Name:
            if isinstance(n.ctx, (ast.Store, ast.Del)):
                names.add(n.id)
        elif t is ast.arg:
            names.add(n.arg)
        elif t in _BREAKERS:
            if n is not fn:
                names.add(n.name)
        elif t is ast.ExceptHandler:
            if n.name:
                names.add(n.name)
        elif t is ast.Global or t is ast.Nonlocal:
            declared.update(n.names)
        elif t.__name__ in ("MatchAs", "MatchStar"):
            if n.name:
                names.add(n.name)
        elif t.__name__ == "MatchMapping":
            if n.rest:
                names.add(n.rest)
    return frozenset(names - declared)


def _name(identifier, locs) -> str:
    return "\x00" + identifier + "\x00" if identifier in locs else "N:" + identifier


def ser(node, locs, strict) -> str:
    """The canonical text of an AST node: see "Normalisation" in the module docstring. A local name is
    emitted between NUL marks and numbered later by renumber(), so the numbering starts where the
    fingerprinted text starts."""
    if isinstance(node, list):
        return "[" + ",".join(ser(v, locs, strict) for v in node) + "]"
    if not isinstance(node, ast.AST):
        return repr(node)
    cls = type(node)
    if cls is ast.Name:
        return _name(node.id, locs)
    if cls is ast.Constant:
        v = node.value
        if strict:
            return "K" + repr(v)
        if v is None or v is True or v is False or v is Ellipsis:
            return repr(v)
        return "K:" + type(v).__name__
    if cls is ast.arg:
        return "arg " + _name(node.arg, locs)
    is_breaker = isinstance(node, _BREAKERS)
    parts = [cls.__name__]
    for fname, value in ast.iter_fields(node):
        if fname in _SKIP_FIELDS:
            continue
        if is_breaker and fname == "body":
            value = strip_doc(value)
        if (cls.__name__, fname) in _BINDING_STRINGS:
            parts.append(fname + "=" + (_name(value, locs) if isinstance(value, str) else "None"))
        else:
            parts.append(fname + "=" + ser(value, locs, strict))
    return "(" + " ".join(parts) + ")"


def renumber(text: str) -> str:
    """Local-name marks -> numbers by order of first appearance in this text."""
    seen: dict = {}

    def sub(mo):
        return "\x01%d" % seen.setdefault(mo.group(1), len(seen))

    return _MARK.sub(sub, text)


def digest(text: str) -> str:
    return hashlib.sha1(text.encode("utf-8", "backslashreplace")).hexdigest()


def function_hash(fn, locs, strict) -> str:
    """Fingerprint of a function: its parameters and its body (docstring dropped); the name and the
    decorators are not part of it."""
    kind = "async" if isinstance(fn, ast.AsyncFunctionDef) else "def"
    return digest(renumber(kind + ser(fn.args, locs, strict) + ser(strip_doc(fn.body), locs, strict)))


# ---------------------------------------------------------------- one file

class FuncRec:
    __slots__ = ("path", "name", "start", "end", "size", "hash")

    def __init__(self, path, name, start, end, size, h):
        self.path, self.name, self.start, self.end, self.size, self.hash = path, name, start, end, size, h


class ListRec:
    """One statement list with the fingerprint of the window that STARTS at each position (None where a
    window would not fit or would contain a def/class)."""
    __slots__ = ("path", "scope", "starts", "ends", "counts", "hashes")

    def __init__(self, path, scope, starts, ends, counts, hashes):
        self.path, self.scope, self.starts, self.ends, self.counts, self.hashes = path, scope, starts, ends, counts, hashes


def _qual(scope: str, name: str) -> str:
    return name if scope == "<module>" else scope + "." + name


class FileAnalysis:
    def __init__(self, rel, tree, strict, window, min_statements, with_imports=False):
        self.rel, self.strict, self.window, self.min_statements = rel, strict, window, min_statements
        self.with_imports = with_imports
        self.funcs: list = []
        self.lists: list = []
        self.n_functions = 0
        self._walk_block(strip_doc(tree.body), "<module>", frozenset())

    def _walk_block(self, stmts, scope, locs):
        self._add_list(stmts, scope, locs)
        for s in stmts:
            if isinstance(s, _DEFS):
                inner = collect_locals(s)
                qual = _qual(scope, s.name)
                body = strip_doc(s.body)
                size = count_stmts(body)
                self.n_functions += 1
                if size >= self.min_statements:
                    self.funcs.append(FuncRec(self.rel, qual, s.lineno, s.end_lineno, size,
                                              function_hash(s, inner, self.strict)))
                self._walk_block(body, qual, inner)
            elif isinstance(s, ast.ClassDef):
                self._walk_block(strip_doc(s.body), _qual(scope, s.name), locs)
            else:
                for blk in child_blocks(s):
                    self._walk_block(blk, scope, locs)

    def _add_list(self, stmts, scope, locs):
        w, n = self.window, len(stmts)
        if n < w:
            return
        breaker = [isinstance(s, _BREAKERS) or (not self.with_imports and is_import_statement(s)) for s in stmts]
        strs = [None if b else ser(s, locs, self.strict) for s, b in zip(stmts, breaker)]
        prefix = [0]
        for b in breaker:
            prefix.append(prefix[-1] + (1 if b else 0))
        hashes = []
        for pos in range(n - w + 1):
            if prefix[pos + w] - prefix[pos]:
                hashes.append(None)
            else:
                hashes.append(digest(renumber("\x1f".join(strs[pos:pos + w]))))
        if not any(h is not None for h in hashes):
            return
        counts = [0 if b else count_stmts([s]) for s, b in zip(stmts, breaker)]
        self.lists.append(ListRec(self.rel, scope, [s.lineno for s in stmts], [s.end_lineno for s in stmts],
                                  counts, hashes))


def physical_lines(data: bytes) -> int:
    return data.count(b"\n") + (1 if data and not data.endswith(b"\n") else 0)


def describe_error(exc) -> str:
    if isinstance(exc, SyntaxError):
        return f"SyntaxError: {exc.msg} (line {exc.lineno})"
    if isinstance(exc, OSError):  # str(exc) carries filename/filename2 -- an absolute path; never printed
        reason = (str(exc.strerror or "").splitlines() or [""])[0][:200]
        return f"{type(exc).__name__}: {reason or 'cannot be read'}"
    first = (str(exc).splitlines() or [""])[0][:200]
    return f"{type(exc).__name__}: {first}" if first else type(exc).__name__


# ---------------------------------------------------------------- the set

def normalise_patterns(repo: Path, patterns) -> tuple:
    """Forward slashes; an absolute glob inside --repo becomes relative (the output must carry no
    machine-specific path, the options line included); one outside --repo is a usage error."""
    out = []
    for pat in patterns:
        pat = pat.replace("\\", "/")
        if Path(pat).is_absolute():
            try:
                pat = Path(pat).relative_to(repo).as_posix()
            except ValueError as exc:
                raise UsageError(f"the glob `{pat}` is absolute and outside --repo; "
                                 f"give --paths globs relative to --repo") from exc
        out.append(pat)
    return tuple(out)


def resolve_files(repo: Path, patterns, exclude=()) -> list:
    """The files the (normalised) globs match, as repo-relative POSIX paths, sorted, once each; a file whose
    path matches an `exclude` glob (fnmatch on the repo-relative POSIX path) is dropped."""
    found = set()
    for pat in patterns:
        try:
            matches = list(repo.glob(pat))
        except (ValueError, NotImplementedError) as exc:
            raise UsageError(f"the glob `{pat}` cannot be used: {exc}") from exc
        for f in matches:
            if f.is_file():
                try:
                    found.add(f.relative_to(repo).as_posix())
                except ValueError as exc:
                    raise UsageError(f"the glob `{pat}` reaches outside --repo") from exc
    return sorted(p for p in found if not any(fnmatch.fnmatchcase(p, ex) for ex in exclude))


class Group:
    __slots__ = ("kind", "size", "locs", "key")

    def __init__(self, kind, size, locs, key):
        self.kind, self.size = kind, size
        self.locs = sorted(locs)            # (path, start, end, name)
        self.key = key                      # what the grouping keyed on: a function hash, or a fragment's (hash, windows)

    @property
    def fingerprint(self) -> str:
        """The group's identity: the normalised code, no path and no line -- a rename, a move or an edit
        elsewhere in the file leaves it unchanged. Changing how it is made bumps NORMALISATION."""
        if self.kind == "function":
            return digest("function\x1f" + self.key)
        return digest("fragment\x1f%s\x1f%d" % self.key)

    @property
    def copies(self):
        return len(self.locs)

    @property
    def lines(self):
        return max(e - s + 1 for _, s, e, _ in self.locs)


def function_groups(funcs) -> list:
    by_hash: dict = {}
    for f in funcs:
        by_hash.setdefault(f.hash, []).append(f)
    return [Group("function", fs[0].size, [(f.path, f.start, f.end, f.name) for f in fs], h)
            for h, fs in by_hash.items() if len(fs) >= 2]


def fragment_groups(lists, window) -> list:
    occ: dict = {}
    for li, rec in enumerate(lists):
        for pos, h in enumerate(rec.hashes):
            if h is not None:
                occ.setdefault(h, []).append((li, pos))
    grouped = {h: o for h, o in occ.items() if len(o) >= 2}
    memo: dict = {}

    def linked(h1, h2) -> bool:
        """The windows h1 and h2 (h2 one position later) always travel together: every copy of h1 is
        followed by h2 and every copy of h2 is preceded by h1."""
        key = (h1, h2)
        if key not in memo:
            o1, o2 = grouped.get(h1), grouped.get(h2)
            memo[key] = (o1 is not None and o2 is not None and len(o1) == len(o2)
                         and {(li, p + 1) for li, p in o1} == set(o2))
        return memo[key]

    runs: dict = {}
    for li, rec in enumerate(lists):
        hs, n = rec.hashes, len(rec.hashes)
        for pos in range(n):
            h = hs[pos]
            if h is None or h not in grouped:
                continue
            if pos > 0 and hs[pos - 1] is not None and linked(hs[pos - 1], h):
                continue                      # not the start of a run
            k = 1
            while pos + k < n and hs[pos + k] is not None and linked(hs[pos + k - 1], hs[pos + k]):
                k += 1
            runs.setdefault((h, k), []).append((li, pos))

    groups = []
    for (h, k), starts in runs.items():
        length = k + window - 1
        kept, last_li, last_end = [], -1, -1
        for li, pos in sorted(starts):
            if li == last_li and pos < last_end:
                continue                      # overlaps the previous copy in the same statement list
            kept.append((li, pos))
            last_li, last_end = li, pos + length
        if len(kept) < 2:
            continue
        locs, size = [], 0
        for li, pos in kept:
            rec = lists[li]
            size = sum(rec.counts[pos:pos + length])
            locs.append((rec.path, rec.starts[pos], rec.ends[pos + length - 1], rec.scope))
        groups.append(Group("fragment", size, locs, (h, k)))
    return groups


def drop_covered(groups) -> tuple:
    """Remove groups that lie wholly inside the members of ONE larger function group. -> (kept, dropped count)."""
    fgroups = [g for g in groups if g.kind == "function"]
    members: dict = {}                        # path -> [(start, end, group index)]
    for gi, g in enumerate(fgroups):
        for path, s, e, _ in g.locs:
            members.setdefault(path, []).append((s, e, gi))
    kept, dropped = [], 0
    for g in groups:
        candidates = None
        for path, s, e, _ in g.locs:
            here = {gi for ms, me, gi in members.get(path, ()) if ms <= s and e <= me}
            candidates = here if candidates is None else candidates & here
            if not candidates:
                break
        covered = any(fgroups[gi] is not g and (g.kind == "fragment" or fgroups[gi].size > g.size)
                      for gi in (candidates or ()))
        if covered:
            dropped += 1
        else:
            kept.append(g)
    return kept, dropped


def union_lines(groups) -> int:
    by_path: dict = {}
    for g in groups:
        for path, s, e, _ in g.locs:
            by_path.setdefault(path, []).append((s, e))
    total = 0
    for spans in by_path.values():
        spans.sort()
        cur_s, cur_e = spans[0]
        for s, e in spans[1:]:
            if s <= cur_e + 1:
                cur_e = max(cur_e, e)
            else:
                total += cur_e - cur_s + 1
                cur_s, cur_e = s, e
        total += cur_e - cur_s + 1
    return total


def group_dict(gid, g) -> dict:
    return {"id": gid, "kind": g.kind, "fingerprint": g.fingerprint, "statements": g.size, "lines": g.lines,
            "copies": g.copies,
            "locations": [{"path": p, "first": s, "last": e, "in": n} for p, s, e, n in g.locs]}


def analyse(repo: Path, patterns, min_statements, window, strict, top, with_imports=False, exclude=(), files=None) -> dict:
    """`files`: the list `resolve_files(repo, patterns, exclude)` already returned (a caller that needs it too passes it, so
    the globs run once per scope); None = resolved here. It is the caller's to keep in step with `patterns` and `exclude`."""
    sys.setrecursionlimit(max(sys.getrecursionlimit(), RECURSION_LIMIT))
    if files is None:
        files = resolve_files(repo, patterns, exclude)
    funcs, lists, unreadable = [], [], []
    n_read = n_functions = total_lines = 0
    for rel in files:
        try:
            data = (repo / rel).read_bytes()
            fa = FileAnalysis(rel, ast.parse(data, filename=rel), strict, window, min_statements, with_imports)
        except (SyntaxError, ValueError, RecursionError, MemoryError, OSError) as exc:
            unreadable.append({"path": rel, "error": describe_error(exc)})
            continue
        n_read += 1
        n_functions += fa.n_functions
        total_lines += physical_lines(data)
        funcs.extend(fa.funcs)
        lists.extend(fa.lists)
    found = function_groups(funcs) + fragment_groups(lists, window)
    kept, dropped = drop_covered(found)
    kept.sort(key=lambda g: (-(g.size * g.copies), -g.size, -g.copies, g.kind, g.locs))
    dup = union_lines(kept) if kept else 0
    options = {"paths": list(patterns), "min_statements": min_statements, "window": window,
               "strict": strict, "top": top}
    if with_imports:
        options["with_imports"] = True         # absent = the default (imports excluded): JSON of a default run is unchanged
    if exclude:
        options["exclude"] = list(exclude)     # absent = nothing excluded, for the same reason
    return {
        "options": options,
        "fingerprint_basis": {"normalisation": NORMALISATION},
        "totals": {"files_read": n_read, "files_unreadable": len(unreadable), "functions": n_functions,
                   "groups": len(kept), "function_groups": sum(1 for g in kept if g.kind == "function"),
                   "fragment_groups": sum(1 for g in kept if g.kind == "fragment"),
                   "groups_shown": min(top, len(kept)), "groups_dropped_as_covered": dropped,
                   "duplicated_lines": dup, "lines_read": total_lines,
                   "duplicated_share_percent": round(100.0 * dup / total_lines, 1) if total_lines else 0.0},
        "unreadable": unreadable,
        "groups": [group_dict(f"G{i}", g) for i, g in enumerate(kept[:top], 1)],
    }


# ---------------------------------------------------------------- output

def render_markdown(rep: dict) -> str:
    o, t = rep["options"], rep["totals"]
    out = ["# Duplicate code report", "",
           f"- paths: {', '.join('`' + p + '`' for p in o['paths'])}"]
    if o.get("exclude"):                        # only a run that excludes something says so: the default output is unchanged
        out.append(f"- exclude: {', '.join('`' + p + '`' for p in o['exclude'])}")
    out += [f"- options: min-statements {o['min_statements']}, window {o['window']}, "
            f"strict {'yes' if o['strict'] else 'no'}, imports {'included' if o.get('with_imports') else 'excluded'}, "
            f"top {o['top']}",
            f"- files read: {t['files_read']}",
            f"- files unreadable: {t['files_unreadable']}",
            f"- functions: {t['functions']}",
            f"- clone groups: {t['groups']} ({t['function_groups']} function, {t['fragment_groups']} fragment), "
            f"shown {t['groups_shown']}",
            f"- groups dropped as lying inside a larger function clone: {t['groups_dropped_as_covered']}",
            f"- duplicated lines: {t['duplicated_lines']} of {t['lines_read']} "
            f"({t['duplicated_share_percent']:.1f}%)", ""]
    if rep["unreadable"]:
        out += ["## Unreadable files", ""]
        out += [f"- `{u['path']}`: {u['error']}" for u in rep["unreadable"]]
        out.append("")
    if t["files_read"] == 0 and not rep["unreadable"]:
        out += ["No Python files matched the paths: nothing was read.", ""]
    elif not t["groups"]:
        out += ["No clone groups found.", ""]
    for g in rep["groups"]:
        out += [f"## {g['id']} {g['kind']}: {g['statements']} statements, {g['lines']} lines, {g['copies']} copies", ""]
        out += [f"- `{loc['path']}:{loc['first']}-{loc['last']}` {loc['in']}" for loc in g["locations"]]
        out.append("")
    return "\n".join(out)


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description="report duplicated code (function and fragment clones); a report, not a gate")
    ap.add_argument("--repo", default=str(REPO), help="repository root; output paths are relative to it")
    ap.add_argument("--paths", nargs="+", default=None, metavar="GLOB",
                    help="globs relative to --repo (default: " + ", ".join(DEFAULT_PATHS) + ")")
    ap.add_argument("--exclude", nargs="+", default=None, metavar="GLOB",
                    help="drop every file whose repo-relative path matches one of these globs (fnmatch; default: none)")
    ap.add_argument("--min-statements", type=int, default=DEFAULT_MIN_STATEMENTS, metavar="N",
                    help="smallest function body that counts (default %(default)s)")
    ap.add_argument("--window", type=int, default=DEFAULT_WINDOW, metavar="N",
                    help="consecutive statements per fragment window (default %(default)s)")
    ap.add_argument("--top", type=int, default=DEFAULT_TOP, metavar="N", help="groups to print (default %(default)s)")
    ap.add_argument("--strict", action="store_true", help="keep literal values in the comparison")
    ap.add_argument("--with-imports", action="store_true", dest="with_imports",
                    help="let import statements and the sys.path bootstrap line count in fragment windows "
                         "(default: they break a window like a def does)")
    ap.add_argument("--json", action="store_true", help="print JSON instead of markdown")
    return ap


def run(argv=None) -> int:
    ap = build_parser()
    try:
        args = ap.parse_args(argv)
    except SystemExit as exc:                  # argparse: 2 on a usage error, 0 on --help
        return int(exc.code or 0)
    try:
        for name, value, low in (("--min-statements", args.min_statements, 1), ("--window", args.window, 2),
                                 ("--top", args.top, 1)):
            if value < low:
                raise UsageError(f"{name} must be at least {low}, got {value}")
        repo = Path(args.repo).resolve()
        if not repo.is_dir():
            raise UsageError("--repo is not a directory")
        patterns = normalise_patterns(repo, args.paths if args.paths else DEFAULT_PATHS)
        exclude = normalise_patterns(repo, args.exclude) if args.exclude else ()
        started = time.monotonic()
        rep = analyse(repo, patterns, args.min_statements, args.window, args.strict, args.top, args.with_imports,
                      exclude)
    except UsageError as exc:
        print(f"dup_report: usage error: {exc}", file=sys.stderr)
        return 2
    text = json.dumps(rep, indent=2) if args.json else render_markdown(rep)
    sys.stdout.write(text + "\n")
    print(f"dup_report: {rep['totals']['files_read']} files read in {time.monotonic() - started:.1f}s", file=sys.stderr)
    return 0


def main(argv=None) -> int:
    streams.utf8_stdio(newline="\n")
    return run(argv)


if __name__ == "__main__":
    sys.exit(main())
