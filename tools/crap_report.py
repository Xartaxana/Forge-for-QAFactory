"""CRAP report -- complex AND uncovered functions, a MEASUREMENT (BACKLOG B-418 = B-299, t-519).

A report, not a gate: it reads, it prints, it exits 0 when the run completes. No threshold that turns red.
What it is for: a person (or the Lead) sees which functions are both branchy and weakly covered, before the
next change lands in them. CRAP(f) = c^2 x (1 - cov)^3 + c, with c the complexity and cov the line coverage of
the function (a function of cov 1 costs c, a function nobody runs costs c^2 + c).

Usage:
  python tools/crap_report.py [--repo PATH] [--paths GLOB ...] [--coverage FILE] [--coverage-hashes FILE]
                              [--top N] [--measured-only] [--require-coverage] [--json] [--lines] [--depth]
    --repo PATH           the repository root (default: the parent of tools/); every path in the output is
                           relative to it, with forward slashes: no machine-specific text
    --paths GLOB ...       what to read, globs relative to --repo (default: the product scripts, the scope
                           dup_report uses; other trees go through --paths)
    --coverage FILE        the coverage record: a coverage.py JSON (`coverage json`), or the driver golden's
                           `coverage-n0.json` (its executed lines are read from `coverage-hits/*.json` next
                           to it). The shape is recognised, the source path is never guessed; without the flag
                           every function is unmeasured
    --coverage-hashes FILE `sha256sum` lines (`<hex>  <path>` or `<hex> *<path>`) of the files the record
                           measured; a file whose bytes differ from its hash is refused
    --top N                rows to print (default 40); the head still counts all of them
    --measured-only        leave the unmeasured functions out of the table (the head still counts them)
    --require-coverage     CI flag: exit 1 when no file of the scope was measured (see "Exit codes")
    --json                 the same data as JSON instead of markdown
    --lines, --depth       opt-in: one more column each (markdown) and one integer key each (JSON), after
                           `complexity`, always in the order lines, depth; the head gets one line defining
                           them. Off, every byte of the output is what it was without these flags. A report
                           only: no threshold, no change of rank or exit code

What is measured
  Every `def` / `async def` at any depth is one row; its name is dotted (`Class.method`, `outer.inner`).
  Lambdas, class bodies and module code are not rows.
  Complexity c = 1 + decision points of the unit, nested def bodies NOT counted (they are rows of their own).
    +1  each `if` (so `elif` counts), `for`, `while`, `except` / `except*` handler, ternary, comprehension
        generator, comprehension `if`, `match` case (a trailing `case _:` / `case name:` with no guard is
        irrefutable: no branch); +(n-1) for a boolean operator with n operands.
     0  `with`, `assert`, `else`, `finally`, return / raise / break / continue.
    A lambda body, the statements of a class nested in the unit, and the decorators / default values of a
    nested def count to the enclosing unit.
  Lines of a unit L(f): from the first body line to the last line; a nested def body (its first body line to
  its end) is taken out, its decorators and `def` line stay; a nested CLASS body is not (it runs when the unit
  runs, and its branch points are charged to the unit; its methods' bodies are cut out as nested defs); the
  unit's own decorators and `def` line
  are outside (they run at import). A body that starts on the `def` line leaves that line out too. E(f) =
  L(f) intersected with the lines the record knows (executed or missing); cov = executed in E(f) / |E(f)|. A
  line the record lists as both executed and missing counts as missing.
  `--lines` = |L(f)| minus the docstring's lines that fall inside L(f) (a body on the `def` line, or a
  docstring-only body, gives 0). `--depth` = the deepest nesting of if / for / while / try / with / match inside
  the unit (an `elif` adds none, a `case` body adds none, a nested def is its own row and is not entered, a
  nested class body counts toward `lines` but not toward `depth`); both come from the one iterative walk.

Coverage sources, and what refuses a file (a refused file is unmeasured, never partly counted)
  - an entry is attributed to the ONE scanned path its key ends with at a `/` boundary (an absolute key under
    --repo is made relative first; the golden's basename key `story_run.py` is attributed to the one scanned
    path that ends with it). No candidate: unmatched. Several: ambiguous. A file claimed by two entries:
    both ambiguous.
  - a recorded line beyond the file's last line; (golden) `story_run_sha256` not the sha256 of the file's bytes
    as read, with CRLF turned into LF, or with every lone LF turned into CRLF; (hashes file) the same test
    against the file's hash, and a scanned file with no hash line ("no hash").
  - the golden itself: the hits file names (`.json` removed) must equal the `test_files_in_the_record`
    entries (`.py` removed), and the distinct lines of every hits file must number `covered_lines`.
  Without --coverage-hashes a coverage.py record is not checked against bytes (the head says "bytes not
  verified"): a stale JSON whose lines all fit reads as current, which errs toward LESS CRAP -- the one hole.
  Everything else errs toward more CRAP.

Edges
  An unmeasured function (no source, unreadable source, unknown shape, a file the record does not name, a
  refused file) is counted at coverage 0: its CRAP is an upper bound and is printed `<=N`, its coverage `none`.
  A function with no executable line in the record (a stub, a one-line def) prints coverage `n/a`, CRAP = c.
  An unparsable file (SyntaxError, ValueError, RecursionError, OSError) is listed under "Unreadable files" and
  skipped; one file never aborts the run. Two functions with one qualified name are two rows (told apart by
  `line`). Rank: CRAP descending, complexity descending, path, line.

Output: markdown -- a head (paths, formula, coverage source, record counts with the first 5 names of each
non-empty group, totals), the unreadable files, then the table `| # | path:line | function | complexity |
coverage | CRAP |`; coverage is a percentage and CRAP a number, both to 1 decimal. `--json` carries the same
data (coverage as a 0..1 float or null, `crap_is_bound`), rounded to 4 places. ASCII, sorted, no timestamps,
no absolute paths. The wall time goes to stderr only.

Exit codes: 0 the run completed (no source, an unreadable source and 0 files matched are reports too: the head
names the reason); 2 a usage error (an unknown option, --top below 1, --repo not a directory, a --paths glob
that is absolute outside --repo); 1 only under --require-coverage when no file was measured.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import posixpath
import re
import sys
import time
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))
from dup_report import (DEFAULT_PATHS, RECURSION_LIMIT, REPO, UsageError, describe_error,  # noqa: E402
                        normalise_patterns, physical_lines, resolve_files)
import streams  # noqa: E402

DEFAULT_TOP = 40
HITS_DIR = "coverage-hits"
GOLDEN_KEYS = ("schema", "never_run", "story_run_sha256")
GOLDEN_FILE = "story_run.py"
NAMES_SHOWN = 5
FORMULA = ("CRAP = c^2 x (1 - cov)^3 + c; c = 1 + if/elif, for, while, except, ternary, comprehension "
           "generator and its ifs, match case (not a final bare `case _`), boolean operand after the first; "
           "cov = line coverage of the function's own lines")
NO_SOURCE_SENTENCE = ("every function counted at coverage 0: CRAP is its upper bound, the order is by "
                      "complexity")
_SCOPES = (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)
_DEFS = (ast.FunctionDef, ast.AsyncFunctionDef)
_ONE_EACH = (ast.If, ast.For, ast.AsyncFor, ast.While, ast.ExceptHandler, ast.IfExp)
# the statements that open a nesting level for `--depth` (t-625's M snippet); `elif` and a `case` body open none
_LEVELS = (ast.If, ast.For, ast.AsyncFor, ast.While, ast.Try, ast.With, ast.AsyncWith, ast.Match,
           *((ast.TryStar,) if hasattr(ast, "TryStar") else ()))
MEASURES = ("lines", "depth")                  # the opt-in columns, always printed in this order
MEASURE_TEXT = {
    "lines": "lines: the function's own lines (L(f), the CRAP rule) minus its docstring",
    "depth": "depth: nested if/for/while/try/with/match (an elif adds none; nested def, class and lambda bodies "
             "are not counted)"}
_LONE_LF = re.compile(rb"(?<!\r)\n")
_SHA_LINE = re.compile(r"^([0-9a-fA-F]{64}) [ *](.+)$")


# ---------------------------------------------------------------- complexity and lines of a unit

class Unit:
    """One function: where it is, its complexity so far, and the line ranges nested defs / classes take out."""
    __slots__ = ("path", "name", "line", "complexity", "first", "last", "holes", "doc", "depth")

    def __init__(self, path, name, node):
        self.path, self.name, self.line, self.complexity = path, name, node.lineno, 1
        self.first, self.last, self.holes = body_start(node), node.end_lineno, []
        self.doc, self.depth = docstring_span(node), 0

    def lines(self) -> set:
        span = set(range(self.first, self.last + 1))
        for start, end in self.holes:
            span.difference_update(range(start, end + 1))
        return span

    def code_lines(self) -> int:
        """|L(f)| minus the docstring lines that fall inside L(f): never negative, a docstring on the `def`
        line or a body on it is outside L(f) already."""
        span = self.lines()
        if self.doc:
            span.difference_update(range(self.doc[0], self.doc[1] + 1))
        return len(span)


def docstring_span(node):
    """(first line, last line) of the docstring of a def, or None."""
    first = node.body[0]
    if isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant) and isinstance(first.value.value, str):
        return first.lineno, first.end_lineno
    return None


def body_start(node) -> int:
    """The first line of a def / class body that is not its `def` line (a body on the `def` line is outside)."""
    first = node.body[0].lineno
    return first if first > node.lineno else node.lineno + 1


def irrefutable(case) -> bool:
    return isinstance(case.pattern, ast.MatchAs) and case.pattern.pattern is None and case.guard is None


def decision_weight(node) -> int:
    """How many decision points this ONE node adds to its unit (see "What is measured")."""
    if isinstance(node, _ONE_EACH):
        return 1
    if isinstance(node, ast.comprehension):
        return 1 + len(node.ifs)
    if isinstance(node, ast.BoolOp):
        return len(node.values) - 1
    if isinstance(node, ast.Match):
        return len(node.cases) - (1 if node.cases and irrefutable(node.cases[-1]) else 0)
    return 0


def header_nodes(node) -> list:
    """What a def / class evaluates in the scope that holds it: decorators and defaults / bases."""
    if isinstance(node, ast.ClassDef):
        return [*node.decorator_list, *node.bases, *(k.value for k in node.keywords)]
    args = node.args
    return [*node.decorator_list, *args.defaults, *(d for d in args.kw_defaults if d is not None)]


def level_of(node, base):
    """The nesting level a node sits at: its context's level, one more for a statement that opens a level.
    None inside a nested class body, which counts toward `lines` but not toward `depth`."""
    if base is None:
        return None
    return base + 1 if isinstance(node, _LEVELS) else base


def child_base(node, child, own):
    """The context level a child inherits. An `elif` is the lone `If` of its parent's `orelse`: it opens no level
    of its own, so it starts one below the parent's (it adds the level back when it is read)."""
    if own is not None and isinstance(node, ast.If) and isinstance(child, ast.If) and node.orelse == [child]:
        return own - 1
    return own


def charge(owner, node, own) -> None:
    """Add what this ONE node of a unit's own code costs: decision points, and the deepest level seen so far."""
    owner.complexity += decision_weight(node)
    if own is not None and own > owner.depth:
        owner.depth = own


def collect_units(rel: str, tree) -> list:
    """Every function of a parsed module, as Units. Iterative: a deep expression cannot overflow this walk."""
    units = []
    stack = [(n, "", None, 0) for n in reversed(tree.body)]   # (node, qualified prefix, owner unit, nesting level)
    while stack:
        node, prefix, owner, base = stack.pop()
        if isinstance(node, _SCOPES):
            qual = f"{prefix}.{node.name}" if prefix else node.name
            unit = Unit(rel, qual, node) if isinstance(node, _DEFS) else None
            if unit:
                units.append(unit)
            if owner is not None and unit is not None:     # a nested def's body is its own row; a nested class body
                owner.holes.append((body_start(node), node.end_lineno))   # RUNS with the owner, so its lines stay
            stack.extend((h, prefix, owner, base) for h in reversed(header_nodes(node)))
            stack.extend((s, qual, unit or owner, 0 if unit else None) for s in reversed(node.body))
            continue
        own = level_of(node, base)
        if owner is not None:
            charge(owner, node, own)
        stack.extend((c, prefix, owner, child_base(node, c, own)) for c in reversed(list(ast.iter_child_nodes(node))))
    return units


def crap(complexity: int, cov: float) -> float:
    return complexity * complexity * (1.0 - cov) ** 3 + complexity


# ---------------------------------------------------------------- the coverage record

class Entry:
    """One file of a record: executed lines, missing lines as (first, last) runs, what must hold for it."""
    __slots__ = ("name", "executed", "missing", "sha", "basename_key", "error")

    def __init__(self, name, executed=(), missing=(), sha=None, basename_key=False, error=None):
        self.name, self.executed, self.missing = name.replace("\\", "/"), set(executed), list(missing)
        self.sha, self.basename_key, self.error = sha, basename_key, error

    def max_line(self) -> int:
        return max(max(self.executed, default=0), max((b for _, b in self.missing), default=0))

    def line_sets(self) -> tuple:
        missing = set()
        for first, last in self.missing:
            missing.update(range(first, last + 1))
        return self.executed - missing, missing


class Source:
    """The coverage source as read: kind, a printable label, the entries, or the reason it cannot be used."""

    def __init__(self, label, kind=None, entries=(), error=None):
        self.label, self.kind, self.entries, self.error = label, kind, list(entries), error


def label_of(path: Path, repo: Path) -> str:
    resolved = path.resolve()
    try:
        return resolved.relative_to(repo).as_posix()
    except ValueError:
        return resolved.name


def lines_ok(value) -> bool:
    return isinstance(value, list) and all(type(v) is int and v >= 1 for v in value)


def coverage_entries(files: dict) -> list:
    out = []
    for key, val in files.items():
        executed = val.get("executed_lines") if isinstance(val, dict) else None
        missing = val.get("missing_lines") if isinstance(val, dict) else None
        if lines_ok(executed) and lines_ok(missing):
            out.append(Entry(key, executed, [(n, n) for n in sorted(set(missing))]))
        else:
            out.append(Entry(key, error="executed_lines / missing_lines are not lists of line numbers"))
    return out


def never_run_runs(rows) -> list:
    if not isinstance(rows, list):
        raise ValueError("`never_run` is not a list")
    runs = []
    for i, row in enumerate(rows):
        span = row.get("lines") if isinstance(row, dict) else None
        if not (isinstance(span, list) and len(span) == 2 and lines_ok(span) and span[0] <= span[1]):
            raise ValueError(f"`never_run` entry {i} has no valid `lines` [first, last]")
        runs.append((span[0], span[1]))
    return runs


def stems_of(names, suffix) -> set:
    return {n[:-len(suffix)] if n.endswith(suffix) else n for n in names}


def hits_union(directory: Path, doc: dict) -> set:
    """The executed lines of the golden: the union of `<dir>/coverage-hits/*.json`, accepted only when the
    hits file names match the record's test files and the union has `covered_lines` lines (the recorder
    writes `run.name[:-3] + ".json"`, driver_golden.py:744)."""
    tests = doc.get("test_files_in_the_record")
    if not (isinstance(tests, list) and all(isinstance(t, str) for t in tests)):
        raise ValueError("`test_files_in_the_record` is not a list of names")
    try:
        files = sorted((directory / HITS_DIR).glob("*.json"))
    except OSError as exc:
        raise ValueError(f"the {HITS_DIR} directory cannot be read ({describe_error(exc)})") from exc
    want, have = stems_of(tests, ".py"), {p.stem for p in files}
    if want != have:
        raise ValueError(f"the {HITS_DIR} files do not match test_files_in_the_record "
                         f"(only in the record: {', '.join(sorted(want - have)[:3]) or '-'}; "
                         f"only in {HITS_DIR}: {', '.join(sorted(have - want)[:3]) or '-'})")
    union = set()
    for path in files:
        union.update(read_hits_file(path))
    if len(union) != doc.get("covered_lines"):
        raise ValueError(f"the {HITS_DIR} files hold {len(union)} distinct lines, the record says "
                         f"covered_lines {doc.get('covered_lines')}")
    return union


def read_hits_file(path: Path) -> list:
    """The `story_run.py` line numbers of one hits file; ValueError with a sentence when it cannot be read."""
    try:
        lines = json.loads(path.read_text(encoding="utf-8")).get(GOLDEN_FILE, [])
    except (OSError, ValueError, RecursionError, AttributeError) as exc:
        raise ValueError(f"{path.name} cannot be read ({describe_error(exc)})") from exc
    if not lines_ok(lines):
        raise ValueError(f"{path.name} holds no list of line numbers for {GOLDEN_FILE}")
    return lines


def golden_entry(doc: dict, directory: Path) -> Entry:
    sha = doc.get("story_run_sha256")
    try:
        if not isinstance(sha, str):
            raise ValueError("`story_run_sha256` is not a string")
        return Entry(GOLDEN_FILE, hits_union(directory, doc), never_run_runs(doc["never_run"]), sha, True)
    except ValueError as exc:
        return Entry(GOLDEN_FILE, sha=sha if isinstance(sha, str) else None, basename_key=True, error=str(exc))


def read_source(path: Path, repo: Path) -> Source:
    label = label_of(path, repo)
    try:
        doc = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, RecursionError, MemoryError) as exc:
        return Source(label, error=describe_error(exc))
    if not isinstance(doc, dict):
        return Source(label, error="the JSON is not an object")
    if all(k in doc for k in GOLDEN_KEYS):
        return Source(label, "driver golden", [golden_entry(doc, path.resolve().parent)])
    if isinstance(doc.get("files"), dict):
        return Source(label, "coverage.py", coverage_entries(doc["files"]))
    return Source(label, error="unknown shape: neither a coverage.py JSON (`files`) nor a driver golden "
                               "record (`schema`, `never_run`, `story_run_sha256`)")


def read_hashes(path: Path, repo: Path) -> dict:
    """{label, by_name: {path: [hex]}, lines, ignored, error} for a `sha256sum` file."""
    out = {"label": label_of(path, repo), "by_name": {}, "lines": 0, "ignored": 0, "error": None}
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, ValueError) as exc:
        out["error"] = describe_error(exc)
        return out
    for raw in text.splitlines():
        mo = _SHA_LINE.match(raw.rstrip("\r"))
        if mo:
            out["lines"] += 1
            out["by_name"].setdefault(mo.group(2), []).append(mo.group(1).lower())
        elif raw.strip():
            out["ignored"] += 1
    return out


def sha_forms(data: bytes) -> set:
    """The sha256 of the bytes as read, with CRLF turned into LF, and with every lone LF turned into CRLF:
    a line-ending conversion moves no line, a changed byte inside a line moves every form."""
    return {hashlib.sha256(b).hexdigest()
            for b in (data, data.replace(b"\r\n", b"\n"), _LONE_LF.sub(b"\r\n", data))}


# ---------------------------------------------------------------- attributing entries to files

def relativise(key: str, repo: Path) -> str:
    key = key.replace("\\", "/")
    if Path(key).is_absolute():
        try:
            return Path(key).relative_to(repo).as_posix()
        except ValueError:
            pass
    return key


def machine_free(key: str) -> str:
    """A record key as the output may show it: an absolute key (another tree's, a user's home) is cut to its
    last two segments, `.../pkg/zz.py`; a relative one is shown whole."""
    if not (key.startswith("/") or re.match(r"^[A-Za-z]:/", key)):
        return key
    return ".../" + "/".join(key.rstrip("/").split("/")[-2:])


def attribute(key: str, by_base: dict, repo: Path, basename_key: bool) -> list:
    """The scanned paths a record key belongs to: the key ends with the path at a `/` boundary (a golden
    basename key is the other way round: the path ends with it)."""
    return attribute_relative(relativise(key, repo), by_base, basename_key)


def attribute_relative(key: str, by_base: dict, basename_key: bool) -> list:
    """`attribute` for a key that is already relativised (judge relativises each entry once)."""
    out = []
    for path in by_base.get(posixpath.basename(key), ()):
        if path == key or (path.endswith("/" + key) if basename_key else key.endswith("/" + path)):
            out.append(path)
    return out


def index_by_base(scanned) -> dict:
    by_base: dict = {}
    for path in scanned:
        by_base.setdefault(posixpath.basename(path), []).append(path)
    return by_base


def hashes_by_file(hashes, by_base, repo) -> tuple:
    """({scanned path: [hex]}, number of hash lines that name no single scanned file)."""
    found, lost = {}, 0
    for name, hexes in sorted(hashes["by_name"].items()):
        cands = attribute(name, by_base, repo, False)
        if len(cands) == 1:
            found.setdefault(cands[0], []).extend(hexes)
        else:
            lost += len(hexes)
    return found, lost


def refusal(entry, data, hexes, hashes_given):
    """Why this entry cannot count for the file `data`, or None. Every reason says the record measured
    other bytes (or could not be trusted); none is a guess."""
    if entry.error:
        return entry.error
    if data is None:
        return "the file is unreadable"
    nlines, top = physical_lines(data), entry.max_line()
    if top > nlines:
        return f"a recorded line ({top}) is beyond the file's {nlines} lines: the record measured other bytes"
    if hashes_given and not hexes:
        return "no hash: the hashes file has no line for this file"
    if entry.sha is None and not hexes:
        return None
    forms = sha_forms(data)
    if entry.sha is not None and entry.sha.lower() not in forms:
        return (f"story_run_sha256 {entry.sha[:8]} is not the sha256 of the file "
                f"({hashlib.sha256(data).hexdigest()[:8]}): the record measured other bytes")
    if hexes and not all(h in forms for h in hexes):
        return "the sha256 differs from the hashes file: the record measured other bytes"
    return None


def judge(source, hashes, parsed, scanned, repo) -> tuple:
    """-> ({path: (executed, missing)} of the accepted files, the record counts)."""
    by_base = index_by_base(scanned)
    hexes, lost = ({}, 0) if hashes is None else hashes_by_file(hashes, by_base, repo)
    counts = {"matched": [], "unmatched": [], "ambiguous": [], "refused": []}
    claims: dict = {}
    # an absolute key under --repo is shown relative; the entry itself is never changed (one relativise each)
    named = sorted(((relativise(e.name, repo), e) for e in source.entries), key=lambda pair: pair[0])
    for name, entry in named:
        cands = attribute_relative(name, by_base, entry.basename_key)
        if len(cands) == 1:
            claims.setdefault(cands[0], []).append((name, entry))
        else:
            counts["ambiguous" if cands else "unmatched"].append(machine_free(name))
    accepted = {}
    for path, claimed in sorted(claims.items()):
        if len(claimed) > 1:
            counts["ambiguous"].extend(machine_free(name) for name, _ in claimed)
            continue
        entry = claimed[0][1]
        why_not = refusal(entry, parsed[path].data if path in parsed else None, hexes.get(path), hashes is not None)
        if why_not:
            counts["refused"].append((path, why_not))          # the scanned repo path, never the record's own key
        else:
            accepted[path] = entry.line_sets()
            counts["matched"].append(path)
    counts["hash_lines_unattributed"] = lost
    return accepted, counts


# ---------------------------------------------------------------- the report

class Parsed:
    __slots__ = ("data", "units")

    def __init__(self, data, units):
        self.data, self.units = data, units


def parse_files(repo: Path, scanned) -> tuple:
    parsed, unreadable = {}, []
    for rel in scanned:
        try:
            data = (repo / rel).read_bytes()
            parsed[rel] = Parsed(data, collect_units(rel, ast.parse(data, filename=rel)))
        except (SyntaxError, ValueError, RecursionError, MemoryError, OSError) as exc:
            unreadable.append({"path": rel, "error": describe_error(exc)})
    return parsed, unreadable


def coverage_of(unit, record):
    """The line coverage of a unit in an accepted record, or None when the record knows none of its lines."""
    executed, missing = record
    lines = unit.lines()
    ran, absent = len(lines & executed), len(lines & missing)
    return ran / (ran + absent) if ran + absent else None


def make_row(unit, record, measures=()) -> dict:
    """One row. `measures` names the opt-in columns (`MEASURES`): each adds its integer key after `complexity`."""
    c = unit.complexity
    cov = None if record is None else coverage_of(unit, record)
    if record is None:                                   # unmeasured: counted at coverage 0, an upper bound
        value, bound = crap(c, 0.0), True
    else:
        value, bound = (c, False) if cov is None else (crap(c, cov), False)
    row = {"path": unit.path, "line": unit.line, "function": unit.name, "complexity": c}
    if "lines" in measures:
        row["lines"] = unit.code_lines()
    if "depth" in measures:
        row["depth"] = unit.depth
    row.update(coverage=cov, crap=float(value), crap_is_bound=bound)
    return row


def names_of(counts: dict, key: str) -> list:
    items = counts[key]
    return [{"name": n, "reason": r} for n, r in items[:NAMES_SHOWN]] if key == "refused" else items[:NAMES_SHOWN]


def analyse(repo: Path, patterns, source, hashes, top, measured_only=False, measures=()) -> dict:
    sys.setrecursionlimit(max(sys.getrecursionlimit(), RECURSION_LIMIT))
    scanned = resolve_files(repo, patterns)
    parsed, unreadable = parse_files(repo, scanned)
    accepted, counts = ({}, {"matched": [], "unmatched": [], "ambiguous": [], "refused": []}) \
        if source is None or source.error else judge(source, hashes, parsed, scanned, repo)
    rows = []
    for rel, info in parsed.items():
        record = accepted.get(rel)
        rows.extend(make_row(u, record, measures) for u in info.units)
    measured = sum(1 for r in rows if r["path"] in accepted)
    rows.sort(key=lambda r: (-r["crap"], -r["complexity"], r["path"], r["line"]))
    shown_rows = [r for r in rows if r["path"] in accepted] if measured_only else rows
    shown_rows = shown_rows[:top]
    entries = len(source.entries) if source is not None and not source.error else 0
    return {
        "options": {"paths": list(patterns), "top": top, "measured_only": measured_only,
                    **{m: True for m in MEASURES if m in measures}},
        "coverage": {"source": source.label if source else None, "kind": source.kind if source else None,
                     "error": source.error if source else None,
                     "bytes_verified": hashes is not None and not hashes["error"],
                     "hashes": None if hashes is None else {k: hashes[k] for k in ("label", "lines", "ignored", "error")},
                     "hash_lines_unattributed": counts.get("hash_lines_unattributed", 0),
                     "entries": entries,
                     "counts": {k: len(counts[k]) for k in ("matched", "unmatched", "ambiguous", "refused")},
                     "names": {k: names_of(counts, k) for k in ("matched", "unmatched", "ambiguous", "refused")}},
        "totals": {"files_read": len(parsed), "files_unreadable": len(unreadable),
                   "files_measured": len(accepted), "functions": len(rows), "measured": measured,
                   "unmeasured": len(rows) - measured, "shown": len(shown_rows)},
        "unreadable": unreadable,
        "rows": [dict(r, rank=i) for i, r in enumerate(shown_rows, 1)],
    }


# ---------------------------------------------------------------- output

def ascii_text(text) -> str:
    return str(text).encode("ascii", "backslashreplace").decode("ascii")


def source_lines(cov: dict) -> list:
    if cov["source"] is None:
        return [f"- coverage source: none -- {NO_SOURCE_SENTENCE}"]
    if cov["error"]:
        return [f"- coverage source: `{ascii_text(cov['source'])}` unusable ({ascii_text(cov['error'])}) -- "
                f"{NO_SOURCE_SENTENCE}"]
    out = [f"- coverage source: `{ascii_text(cov['source'])}` ({cov['kind']})"]
    if cov["kind"] == "coverage.py" and cov["hashes"] is None:
        out.append("- bytes not verified: no --coverage-hashes, a record of other bytes whose lines all fit "
                   "reads as current")
    return out


def hashes_lines(cov: dict) -> list:
    h = cov["hashes"]
    if h is None:
        return []
    if h["error"]:
        return [f"- hashes: `{ascii_text(h['label'])}` unusable ({ascii_text(h['error'])}): every file is "
                f"unmeasured (no hash)"]
    return [f"- hashes: `{ascii_text(h['label'])}`, {h['lines']} lines, {h['ignored']} ignored, "
            f"{cov['hash_lines_unattributed']} naming no single scanned file"]


def record_lines(cov: dict) -> list:
    if cov["source"] is None or cov["error"]:
        return []
    c = cov["counts"]
    out = [f"- record entries: {cov['entries']}; matched {c['matched']}; unmatched {c['unmatched']}; "
           f"ambiguous {c['ambiguous']}; refused {c['refused']}"]
    for group in ("matched", "unmatched", "ambiguous", "refused"):
        if not c[group]:
            continue
        shown = [f"`{ascii_text(n['name'])}` ({ascii_text(n['reason'])})" if group == "refused"
                 else f"`{ascii_text(n)}`" for n in cov["names"][group]]
        more = f", ... {c[group] - len(shown)} more" if c[group] > len(shown) else ""
        out.append(f"  - {group}: {', '.join(shown)}{more}")
    return out


def cell(text) -> str:
    return ascii_text(text).replace("|", "\\|")


def render_row(r: dict, columns=()) -> str:
    """One table row; `columns` are the opt-in measures (`MEASURES`) printed between complexity and coverage."""
    cov = "none" if r["coverage"] is None and r["crap_is_bound"] else "n/a" if r["coverage"] is None \
        else f"{100.0 * r['coverage']:.1f}%"
    value = ("<=" if r["crap_is_bound"] else "") + f"{r['crap']:.1f}"
    measured = "".join(f" {r[m]} |" for m in columns)
    return (f"| {r['rank']} | {cell(r['path'])}:{r['line']} | {cell(r['function'])} | {r['complexity']} |"
            f"{measured} {cov} | {value} |")


def render_markdown(rep: dict) -> str:
    o, t, cov = rep["options"], rep["totals"], rep["coverage"]
    columns = [m for m in MEASURES if o.get(m)]
    out = ["# CRAP report", "", f"- paths: {', '.join('`' + ascii_text(p) + '`' for p in o['paths'])}",
           f"- formula: {FORMULA}"]
    if columns:
        out.append("- " + "; ".join(MEASURE_TEXT[m] for m in columns))
    out += source_lines(cov) + hashes_lines(cov) + record_lines(cov)
    if t["unmeasured"] and cov["source"] is not None and not cov["error"]:
        out.append("- functions in files with no usable record are counted at coverage 0: their CRAP is an "
                   "upper bound (printed `<=N`)")
    out += [f"- files read: {t['files_read']}", f"- files unreadable: {t['files_unreadable']}",
            f"- functions: {t['functions']}", f"- measured: {t['measured']}", f"- unmeasured: {t['unmeasured']}",
            f"- shown: {t['shown']}" + (" (measured only)" if o["measured_only"] else ""), ""]
    if rep["unreadable"]:
        out += ["## Unreadable files", ""]
        out += [f"- `{ascii_text(u['path'])}`: {ascii_text(u['error'])}" for u in rep["unreadable"]]
        out.append("")
    if not t["functions"]:
        out += ["No functions found: nothing was read or no file matched the paths.", ""]
        return "\n".join(out)
    out += ["| # | path:line | function | complexity |" + "".join(f" {m} |" for m in columns) + " coverage | CRAP |",
            "|---|---|---|---|" + "---|" * len(columns) + "---|---|"]
    out += [render_row(r, columns) for r in rep["rows"]]
    out.append("")
    return "\n".join(out)


def rounded(rep: dict) -> dict:
    rows = [dict(r, coverage=None if r["coverage"] is None else round(r["coverage"], 4), crap=round(r["crap"], 4))
            for r in rep["rows"]]
    return dict(rep, rows=rows)


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description="rank functions by CRAP (complexity x line coverage); a report, "
                                             "not a gate")
    ap.add_argument("--repo", default=str(REPO), help="repository root; output paths are relative to it")
    ap.add_argument("--paths", nargs="+", default=None, metavar="GLOB",
                    help="globs relative to --repo (default: " + ", ".join(DEFAULT_PATHS) + ")")
    ap.add_argument("--coverage", default=None, metavar="FILE",
                    help="a coverage.py JSON or the driver golden's coverage-n0.json (default: none)")
    ap.add_argument("--coverage-hashes", default=None, dest="coverage_hashes", metavar="FILE",
                    help="sha256sum lines of the files the record measured")
    ap.add_argument("--top", type=int, default=DEFAULT_TOP, metavar="N", help="rows to print (default %(default)s)")
    ap.add_argument("--measured-only", action="store_true", dest="measured_only",
                    help="leave the unmeasured functions out of the table")
    ap.add_argument("--require-coverage", action="store_true", dest="require_coverage",
                    help="exit 1 when no file of the scope was measured")
    ap.add_argument("--json", action="store_true", help="print JSON instead of markdown")
    ap.add_argument("--lines", action="store_true",
                    help="add a `lines` column (JSON key): the function's own lines minus its docstring")
    ap.add_argument("--depth", action="store_true",
                    help="add a `depth` column (JSON key): the deepest nesting of if/for/while/try/with/match")
    return ap


def run(argv=None) -> int:
    try:
        args = build_parser().parse_args(argv)
    except SystemExit as exc:                  # argparse: 2 on a usage error, 0 on --help
        return int(exc.code or 0)
    try:
        if args.top < 1:
            raise UsageError(f"--top must be at least 1, got {args.top}")
        repo = Path(args.repo).resolve()
        if not repo.is_dir():
            raise UsageError("--repo is not a directory")
        patterns = normalise_patterns(repo, args.paths if args.paths else DEFAULT_PATHS)
        started = time.monotonic()
        source = read_source(Path(args.coverage), repo) if args.coverage else None
        hashes = read_hashes(Path(args.coverage_hashes), repo) if args.coverage_hashes else None
        rep = analyse(repo, patterns, source, hashes, args.top, args.measured_only,
                      [m for m in MEASURES if getattr(args, m)])
    except UsageError as exc:
        print(f"crap_report: usage error: {exc}", file=sys.stderr)
        return 2
    sys.stdout.write((json.dumps(rounded(rep), indent=2) if args.json else render_markdown(rep)) + "\n")
    print(f"crap_report: {rep['totals']['files_read']} files read in {time.monotonic() - started:.1f}s",
          file=sys.stderr)
    if args.require_coverage and not rep["coverage"]["counts"]["matched"]:
        print("crap_report: --require-coverage: no file of the scope was measured (see the head)", file=sys.stderr)
        return 1
    return 0


def main(argv=None) -> int:
    streams.utf8_stdio(newline="\n")
    return run(argv)


if __name__ == "__main__":
    sys.exit(main())
