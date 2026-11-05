"""probe_by_code.py — the critic's red probe done by code, one instance per call.

The critic used to write a mutation request by hand, prepare two sandboxes, run both, read
tracebacks with `--detail` and retype what it saw into a `probe` record (S5-122; on
TP1-13797 every attempt ended `probe_defect` before a test ran). Here the whole probe is
one command and nothing in the record is typed by a role:

  1. the test function is located by AST (`<file>::[Class::]<func>[<param>]`, class methods too);
  2. its FIRST assert is mutated — `invert`: `assert not (<expr>)`; `expected`: the expected
     literal of an `==` / `in` comparison is replaced by a distinct literal of the same type
     (hamcrest `assert_that(actual, matcher)` gets `is_not(matcher)` / the matcher's first
     literal replaced). The mutated assert carries a marker message `probe-<IID> ...` so the
     failure that fires is attributable, and the statement keeps its line count;
  3. exactly that node runs through `run_suite.py --request` with a typed `red_probe` request
     this script writes under `work/probe-requests/probe-<IID>.json` (built by the same code
     `--mine` uses; `red_probe` writes no run block, so the mutated red never reaches the
     ledger as a product result);
  4. the original bytes are restored in a `finally` FROM A BYTE COPY ON DISK (see below) — verified
     by sha256, mtime put back, the module's `__pycache__` entries dropped so no rewritten
     bytecode of the mutated source outlives it — and `work/probes/<IID>.json` is written in the
     `probe` shape `acceptance.validate_window` checks.

  0. BEFORE anything is mutated a test that was already probed over the same bytes is ANSWERED, not
     probed again (`proof_level.already_probed`, D-0018: one probe per test, only a person's word
     repeats it): exit 0, `{"verdict": "already_probed", ...}`, and nothing is mutated, launched
     or written. "The same bytes" is the per-test identity `--mine` writes into the run's
     `instance_contracts` (`proof_level.same_test`), so an edit of ANOTHER test of the file, or a
     comment, keeps the answer; a code edit of this test, or of a fixture or helper it uses, does not.
  5. an `intended_failure` with a verified restore also writes the IMMUTABLE live receipt
     `work/sensitivity-receipts/<stem>-live-<hash>.json` (level `live`: "the check is live") and
     publishes it in `tests[]` and the obligation bindings through one `manifest_put.py` fragment;
     a receipt of a higher level (`red_sandbox.py --probe`) already there is never replaced.

  probe_by_code.py --task T --dispatch ID --test "<file>::<func>[<param>]" --instance IID
                   [--mutation invert|expected] [--oracle [<file>::]<func>] [--at <line>] [--json] [--timeout S]
  probe_by_code.py --task T --s6-close --test "<file>::<func>[<param>]" --instance IID  [same options]
  probe_by_code.py --release-copy <file> [--json]
  probe_by_code.py --task T --dispatch ID --test "<file>::<func>" --instance IID --mutation alternative
                   --alternative <case>:ALT-n --model work/probe-models/<name>.json [--supersede "<reason>"]   (TQ1-25)
  probe_by_code.py --task T --alternatives [--instance IID] [--json]     (the report: what is owed, stale, proven)

  `--mutation alternative` models the reading B a case declares for a Then (`alternatives`): the critic's model file says where
  the test reads the product's value; the tool applies it under the byte copy, runs the one node and reads the run
  (`judge_alternative`). Its record lives under `work/probes/alternative/` and is never a live receipt; the sections after
  `plan_mutation` ("the alternative reading") say the rest.

  The `--s6-close` form is the DRIVER's, in the code close of S6 when no dispatch is open (HF3-6): `--s6-close` takes
  the place of `--dispatch`, and the context is allowed exactly when the controller would take the S6 code-only
  receipt (`execution_request.s6_close_dispatch`, one predicate with `controller.code_close_conflicts`). It is
  asked before anything is read or mutated, and refused (exit 2, nothing changed) while any dispatch is running,
  before S6 has started, after S6 closed, for a case outside the story's scope, or when the state cannot be read.
  The record then carries `dispatch_id` `S6-close-r<revision>`, and a repeat is looked up under the stage S6.

A test in ANY other language gets the same probe (B-373, D-0028: the proof that the check is live is an
assertion change, and it does not depend on the language of the test). `references/detectors.json`
`assertion_probes` says, per language (read ONLY through `assertion_detectors.py`), how to find the test, its
first assertion and the one inverted form of it, and which failure that inverted form must show. The source is
read by the language's lexer (comments and strings never hold a head), the test is found by its declaration
(exactly one match, or `--at <line>` picks), the first head of its body is inverted by one `find -> replace`
pair at one position (`--mutation invert` only), and the run's own report decides: the inverted statement
failed AT its lines AND with its `fires_as` message is `intended_failure`; anything the tool cannot read - a
frame it cannot resolve, a message the row does not know, an error row, a launcher that may not rebuild, a
`--at` among two candidates that passed - is `incomplete` (exit 1, no receipt, `cause: tooling`): a factory gap
is never a verdict on the test (FR-59). A language with no entry, or a table that cannot be read, is a
refusal that says it is a gap of the factory's data and names the row to add (exit 2, nothing changed in the
author's tree). A refusal of the TOOL (`ToolRefusal`) leaves one record, `refused: tool`, when the manifest proves the test is
the instance's (`_record_tool_refusal`); a refusal of the CALL leaves none. A record that says `incomplete`, or that no row of
the report could be bound to the test, also says `language` and `cause: tooling` (`proof_level.tooling_gap_key` reads it); the one
exception is a failure AT the mutated statement whose message the detector row does not know (E15): `cause: data_row`, the row is the
factory's data to correct and no word of the tool's gap is asked of a person.

The author's file is never mutated without a verified byte copy on disk, and the copy is the only
way back that survives the process. `RUN_TIMEOUT_S` is 31 minutes and a role's shell call is killed
long before it: a killed process never runs its `finally`, and the original bytes lived only in its
memory, so the author's file stayed mutated for good. So, per file (keyed by a hash of its
project-relative path, in the project's `qa-factory/state/probe-copies/`, one folder for every
story of the project):

  * `<k>.lock` - an OS lock (the convention of `event_store.lock`), taken BEFORE the file is first
    read and held to the end of the probe; process death releases it. `OSError` EACCES / EAGAIN /
    EWOULDBLOCK / EDEADLK means HELD; any other errno or an ImportError means the primitive itself
    failed, and only then does the fallback deadline `started_at + timeout_s + 120 s` stand in for
    it. Liveness is never tested by a pid;
  * `<k>.orig` - the original bytes; `<k>.meta` - JSON with a non-`.json` suffix (the json scans of
    the story folders skip it): path, original and mutated sha256, original mtime, start, timeout,
    the statement before and after, its line.
  The order: write `.orig` and `.meta`, re-read `.orig` and check its sha, mutate, restore FROM
  `.orig`, check the sha, put the mtime back (a `.py` keeps its own and loses its bytecode; any other
  file gets "now", so the next incremental build rebuilds), and only then delete the copy. A restore
  that cannot be verified keeps both files and says `copy <.orig> over <file>`.

  When a probe starts it first restores what a dead probe left: every copy whose lock is free is
  restored if the file still holds the probe's mutated bytes, dropped if it already holds the
  original, and otherwise left alone (the author's newer edit wins): a copy of another file is a
  note, a copy of THIS probe's own test or oracle is a refusal that goes back to the test's author
  as a tooling finding. `--release-copy <file>` drops such a copy once the author has dealt with it.

The oracle is not always in the test. A suite whose expectations live in shared helpers - the
common idiom - left this script with nothing to mutate, and it refused: nine of the twelve
critic findings of TP1-13797 were that one tooling defect. So the expectation is followed
ONE hop out of the test, into the helpers and fixtures it calls, looked for in the test file,
the conftest chain and the modules it imports; the mutation then lives in that file for the
length of the probe and is restored with it, and the record says where it went. Deeper than one
hop is named by hand with `--oracle`.

Verdicts: `intended_failure` (the run failed by assertion at the mutated statement with the
marker reason), `no_failure` (the mutated test passed — the assert never fired), `wrong_location`
(it failed elsewhere, or for another reason; `actual_location`/`actual_reason` say where),
`not_executed` (nothing ran; `notes` say why), `incomplete` (the run happened but the tool could not read
it well enough to judge the test: `notes` say what it could not read; a tooling finding). Exit 0 for the
first three, 1 for `not_executed`, `incomplete` or a restore that could not be verified, 2 for a refusal
before any file was touched (no such test, no assert, an instance the manifest does not name, a language
with no `assertion_probes` entry: that one names the row to add and `red_sandbox.py --probe`, the probe
that breaks the product in a throwaway copy and works for any language).

The run directory is the profile's own, passed to the request builder as `--cwd` on the first
call (this probe mutates the author's tree in place, so it has no clone to pass as
`--sandbox-root`). The run's report is read by `reporters.read_rows` with the reporter the run's
summary names (JUnit when it names none).

The run itself is `run_suite.py`; `PROBE_RUN_SUITE=<script>` replaces it (tests), and the
script never launches pytest by itself.
"""
import argparse
import ast
import bisect
import errno
import hashlib
import json
import os
import pathlib
import posixpath
import re
import shutil
import subprocess
import sys
import tempfile
import uuid
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from functools import partial
from pathlib import Path
from typing import Callable, NamedTuple

sys.path.insert(0, str(Path(__file__).resolve().parent))

import assertion_detectors as AD  # noqa: E402
import contract as C  # noqa: E402
import proof_level  # noqa: E402
import reporters  # noqa: E402
from red_sandbox import held_ids, matching_rows  # noqa: E402,F401  (the one matcher, HF4-12; red_sandbox never imports this module)
import runtime_paths  # noqa: E402
import test_source  # noqa: E402  (the one reader of a non-Python test file, EP1-37; it imports this module only inside its functions)
from event_store import atomic_json, content_hash  # noqa: E402
from hooklib import artifacts_dir, load_config, project_root, story_root  # noqa: E402
from hooklib import read_json, sorted_paths  # noqa: E402

MUTATIONS = ("invert", "expected")
# This tool mutates the ASSERTION of a test and never the product, so what it proves is that the
# check is live (level `live`), not that it catches a broken product. It used to claim
# "real_behavior", a product mutation it never makes, and the window then accepted an assertion
# probe as if the product had been broken (D-0010, D-0012).
MUTATION_KIND = "assertion"
# TQ1-25: the probe kind `alternative` models a case's declared reading B and is NOT in MUTATIONS (`probe_debt` replays only
# the two invert kinds: a third there would make it try to replay a kind it cannot).
ALTERNATIVE = "alternative"
ALTERNATIVE_KIND = "alternative_model"
MODEL_TEXT_MAX = 2000       # characters of a model's `find` / `replace`
MODEL_FILE_MAX = 16384      # bytes of a model file
MODEL_GAP_MAX = 300         # characters of a model's `gap`
SUPERSEDE_REASON_MAX = 300  # characters of `--supersede "<reason>"`
ASSERT_THAT = "assert_that"
MANIFEST_FIELDS = ("obligation_ids", "obligation_hash", "defect_location", "assertion_id")
RUN_TIMEOUT_S = 1860
_TRACE_TAIL = re.compile(r"^(?P<loc>\S.*:\d+):\s*(?P<exc>\S+)\s*$")
_FRAME = re.compile(r"^(?P<path>[^\s:]+?\.py):(?P<line>\d+)(?::|\s|$)")


class Refusal(ValueError):
    """A problem with what was asked — answered before any file is touched."""


class ToolRefusal(Refusal):
    """A refusal whose cause is the factory's tool, not the call: the language has no entry, the data is broken, the lexer cannot
    read the file, no declaration or assertion form of the entry fits, or the run cannot be selected on this profile. `main` prints
    it as any refusal (one JSON, exit 2) and also leaves the record `refused: tool` (`_record_tool_refusal`), so that "the tool
    cannot read this" is a fact on disk and not only a line in a chat. `name_unproved` says the refusal does not prove the
    `--test` name is the instance's (no declaration was found for it): the record is then written only when the manifest row
    proves the name. A refusal of the CALL (a wrong --test, an unknown instance, a lock) stays a plain `Refusal`: the role does not
    write itself a gap by a wrong call (AR-22)."""

    def __init__(self, message: str = "", name_unproved: bool = False):
        super().__init__(message)
        self.name_unproved = name_unproved


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def fold(text: str, limit: int = 160) -> str:
    text = " ".join(str(text or "").split())
    return text if len(text) <= limit else text[:limit - 1] + "…"


# --- the test ----------------------------------------------------------------------------------

def parse_node(spec: str, root=None) -> dict:
    """`tests/t.py::TestX::test_y[p]` -> file, class chain, function, param. `root` (the project
    root) only lets a refusal call a directory a directory."""
    text = str(spec or "").strip().replace("\\", "/")
    if "::" not in text:
        raise Refusal(f"--test wants <file>::<function>[<param>], got {spec!r}")
    file, tail = text.split("::", 1)
    parts = tail.split("::")
    last = parts[-1]
    function, _, param = last.partition("[")
    if not file.endswith(".py"):
        return parse_detector_node(text, file, tail, root)
    if not function.isidentifier():
        raise Refusal(f"--test wants a .py file and a function name, got {spec!r}")
    return {"file": file, "chain": parts[:-1], "function": function,
            "param": param[:-1] if param.endswith("]") else param, "node": text}


def _defs(body, chain: list, at: list):
    for node in body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            yield list(at), node
        elif isinstance(node, ast.ClassDef):
            yield from _defs(node.body, chain, at + [node.name])
        elif isinstance(node, (ast.If, ast.Try)):  # a def under a guard is still a def
            for sub in ("body", "orelse", "finalbody"):
                yield from _defs(getattr(node, sub, []) or [], chain, at)


def locate(tree: ast.Module, chain: list, function: str):
    """The one FunctionDef named — the class chain decides when a name repeats."""
    found = [(at, node) for at, node in _defs(tree.body, chain, []) if node.name == function]
    if chain:
        found = [(at, node) for at, node in found if at == chain]
    if not found:
        raise Refusal(f"no test function {'::'.join(chain + [function])} in this file")
    if len(found) > 1:
        names = ", ".join("::".join(at + [function]) for at, _ in found)
        raise Refusal(f"{function} is defined more than once ({names}); name the class in --test")
    return found[0][1]


def _statements(body):
    """Every statement of a body in source order, into compound statements, never into a
    nested def/class (that is another function's assert)."""
    for node in body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            continue
        yield node
        for field in ("body", "orelse", "finalbody", "handlers"):
            children = getattr(node, field, None)
            if isinstance(children, list):
                for child in children:
                    if isinstance(child, ast.ExceptHandler):
                        yield from _statements(child.body)
                    elif isinstance(child, ast.stmt):
                        yield from _statements([child])


def _is_assert_that(node) -> bool:
    if not (isinstance(node, ast.Expr) and isinstance(node.value, ast.Call)):
        return False
    func = node.value.func
    name = func.id if isinstance(func, ast.Name) else func.attr if isinstance(func, ast.Attribute) else ""
    return name == ASSERT_THAT and len(node.value.args) >= 2


def first_assert(function_node):
    for node in _statements(function_node.body):
        if isinstance(node, ast.Assert) or _is_assert_that(node):
            return node
    return None


# --- where the oracle lives ----------------------------------------------------------------------
# A probe mutates the ORACLE, and this script only ever looked in the test function's own body.
# A suite whose expectations live in shared helpers - the common idiom, and the one TP1-13797's
# suite used - therefore had no oracle to mutate, and the probe refused: nine of the critic's
# twelve findings that run were this one tooling defect returned to the author in four windows,
# plus seven registry rows that went to the person. The critic of runs 1 and 2 did the red probe by
# hand and never met it, which is the shape of the rule in plan section 2: code that replaces a
# role must name the class of cases where it steps back, and this was not one - it was a gap.
#
# So the oracle is followed one hop out of the test: into the helpers and fixtures the test body
# calls, looked for in the test's own file, then its conftest chain, then the project modules it
# imports from. One hop, and in call order, because the FIRST expectation the test asserts is the
# one the probe is about; anything deeper is a chain the reader cannot follow either, and gets the
# refusal with `--oracle` named in it.

def _called_names(function_node) -> list:
    """The names the body calls, in source order, plus the fixture parameters — a fixture that
    asserts is as much this test's oracle as a helper it calls."""
    names, seen = [], set()
    for arg in function_node.args.args:
        if arg.arg not in seen and arg.arg not in ("self", "cls"):
            seen.add(arg.arg)
            names.append(arg.arg)
    for node in ast.walk(function_node):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        name = (func.id if isinstance(func, ast.Name)
                else func.attr if isinstance(func, ast.Attribute) else "")
        if name and name not in seen:
            seen.add(name)
            names.append(name)
    return names


def _defs_by_name(text: str) -> dict:
    """{name: FunctionDef} of one module's top-level and class-level defs."""
    try:
        tree = ast.parse(text)
    except (SyntaxError, ValueError):
        return {}
    return {node.name: node for _at, node in _defs(tree.body, [], [])}


def _imported_modules(tree: ast.Module, path: Path, root: Path) -> list:
    """Project files this module imports from, as paths that exist."""
    out = []
    for node in ast.walk(tree):
        parts = []
        if isinstance(node, ast.ImportFrom) and node.module and not node.level:
            parts = node.module.split(".")
        elif isinstance(node, ast.Import):
            parts = (node.names[0].name.split(".") if node.names else [])
        if not parts:
            continue
        for base in (path.parent, root):
            candidate = base.joinpath(*parts).with_suffix(".py")
            package = base.joinpath(*parts) / "__init__.py"
            for file in (candidate, package):
                if file.is_file() and file not in out:
                    out.append(file)
    return out


def find_oracle(text: str, spec: dict, path: Path, root: Path, helpers: list) -> tuple:
    """((file, function name, its node), note) for the assert this probe must mutate.

    The test's own body first. Then, one hop out, the helpers and fixtures it calls, searched in
    the test file, the conftest chain and the modules it imports - the first one that asserts.
    `note` is empty when the oracle is the test's own; otherwise it says where it went and that
    the file is shared, because a mutation there is visible to every test using that helper for
    the length of one probe."""
    tree = ast.parse(text)
    function = locate(tree, spec["chain"], spec["function"])
    own = first_assert(function)
    if own is not None:
        return (path, spec["function"], function, own), ""
    sources = [(path, text)]
    for helper in helpers + [str(p) for p in _imported_modules(tree, path, root)]:
        file = Path(helper)
        if file.resolve() == path.resolve():
            continue
        try:
            sources.append((file, file.read_text(encoding="utf-8", errors="replace")))
        except OSError:
            continue
    tables = [(file, _defs_by_name(body)) for file, body in sources]
    for name in _called_names(function):
        for file, table in tables:
            node = table.get(name)
            if node is None:
                continue
            target = first_assert(node)
            if target is None:
                continue
            where = file.name if file.resolve() != path.resolve() else "this file"
            return ((file, name, node, target),
                    f"the test body asserts nothing; its oracle is `{name}` in {where} "
                    f"(line {target.lineno}), which other tests share — the mutation lives "
                    "there for the length of this probe and is restored with it")
    return (None, "")


# --- the mutation --------------------------------------------------------------------------------

def _line_starts(data: bytes) -> list:
    starts, pos = [0], 0
    while True:
        pos = data.find(b"\n", pos)
        if pos < 0:
            return starts
        pos += 1
        starts.append(pos)


def _span(starts: list, node) -> tuple:
    return (starts[node.lineno - 1] + node.col_offset,
            starts[node.end_lineno - 1] + node.end_col_offset)


def distinct(value):
    """A literal of the same type that is not this one."""
    if isinstance(value, bool):
        return not value
    if isinstance(value, int):
        return value + 1
    if isinstance(value, float):
        return value + 1.0
    if isinstance(value, str):
        return value + "-probe" if value else "probe"
    if isinstance(value, bytes):
        return value + b"-probe" if value else b"probe"
    raise Refusal(f"no distinct literal of type {type(value).__name__} ({value!r}); use --mutation invert")


def _literal_node(compare: ast.Compare):
    """The expected literal of `a == <lit>` / `<lit> == a` / `a in <lit>` / `a in [lits]`."""
    if len(compare.ops) != 1 or not isinstance(compare.ops[0], (ast.Eq, ast.In)):
        raise Refusal("--mutation expected wants a single `==` or `in` comparison; use --mutation invert")
    right, left = compare.comparators[0], compare.left
    if isinstance(right, ast.Constant):
        return right
    if isinstance(compare.ops[0], ast.Eq) and isinstance(left, ast.Constant):
        return left
    if isinstance(right, (ast.List, ast.Tuple, ast.Set)) and right.elts and all(
            isinstance(e, ast.Constant) for e in right.elts):
        return right
    raise Refusal("the comparison has no literal to replace (the expected side is not a constant); "
                  "use --mutation invert")


def _first_constant(node):
    found = [n for n in ast.walk(node) if isinstance(n, ast.Constant) and n.value is not None]
    if not found:
        raise Refusal("the matcher carries no literal to replace; use --mutation invert")
    return min(found, key=lambda n: (n.lineno, n.col_offset))


def _replacement_literal(node) -> tuple:
    """(source of the new literal, before, after) for a Constant or a container of Constants."""
    if isinstance(node, ast.Constant):
        before = node.value
        after = distinct(before)
        return repr(after), repr(before), repr(after)
    values = [e.value for e in node.elts]
    if values and all(isinstance(v, int) and not isinstance(v, bool) for v in values):
        shift = max(values) - min(values) + 1  # every member leaves the old set
        news = [v + shift for v in values]
    else:
        news = [distinct(v) for v in values]
    open_, close = {ast.List: ("[", "]"), ast.Tuple: ("(", ")"), ast.Set: ("{", "}")}[type(node)]
    body = ", ".join(repr(v) for v in news) + ("," if isinstance(node, ast.Tuple) and len(news) == 1 else "")
    return open_ + body + close, repr(values), repr(news)


def _padded(text: bytes, wanted_newlines: int) -> bytes:
    """`text` with newlines added inside its last parenthesis so a statement keeps its line
    count — every line after the mutated assert stays where the author's run reported it."""
    missing = wanted_newlines - text.count(b"\n")
    return text if missing <= 0 else text + b"\n" * missing


class Replacement(NamedTuple):
    """What `plan_mutation` has fixed about the one statement it replaces, handed to the builder of the
    replacement text: the statement's node, the source (BOM stripped) with its line starts, `seg` (the
    source of a node of it) and the statement's newline count, which the replacement must keep."""
    target: ast.AST
    text: bytes
    starts: list
    seg: Callable
    newlines: int


def _assert_replacement(rep: Replacement, mutation: str, instance_id: str, detail: dict) -> tuple:
    """(the replacement of an `assert` statement, the marker it carries). `expected` adds the literal pair
    to `detail`. Every line the statement spanned is still there (`_padded`)."""
    target, text, starts, seg, newlines = rep
    if mutation == "invert":
        marker = f"probe-{instance_id} invert: {fold(seg(target.test).decode('utf-8', 'replace'))}"
        body = _padded(b"assert not (" + seg(target.test), newlines) + b")"
        return body + b", " + json.dumps(marker).encode("utf-8"), marker
    if not isinstance(target.test, ast.Compare):
        raise Refusal("--mutation expected wants `assert <a> == <literal>` or `assert <a> in "
                      "<literal>`; use --mutation invert")
    literal = _literal_node(target.test)
    new_src, before, after = _replacement_literal(literal)
    marker = f"probe-{instance_id} expected: {before} -> {after}"
    lit_start, lit_end = _span(starts, literal)
    lit_text = text[lit_start:lit_end]
    new_lit = new_src.encode("utf-8")
    if lit_text.count(b"\n"):
        new_lit = b"(" + _padded(new_lit, lit_text.count(b"\n")) + b")"
    test_start, test_end = _span(starts, target.test)
    new_test = text[test_start:lit_start] + new_lit + text[lit_end:test_end]
    replaced = (b"assert " + _padded(b"(" + new_test, newlines) + b"), "
                + json.dumps(marker).encode("utf-8"))
    detail.update({"literal_before": before, "literal_after": after})
    return replaced, marker


def _assert_that_replacement(rep: Replacement, mutation: str, instance_id: str, detail: dict) -> tuple:
    """(the replacement of an `assert_that(actual, matcher)` statement, the marker it carries). `expected`
    adds the literal pair to `detail`."""
    target, text, starts, seg, newlines = rep
    call = target.value
    func, actual, matcher = seg(call.func), seg(call.args[0]), seg(call.args[1])
    if mutation == "invert":
        marker = f"probe-{instance_id} invert: {fold(matcher.decode('utf-8', 'replace'))}"
        inner = b"__import__(\"hamcrest\").is_not(" + matcher + b")"
    else:
        literal = _first_constant(call.args[1])
        new_src, before, after = _replacement_literal(literal)
        marker = f"probe-{instance_id} expected: {before} -> {after}"
        lit_start, lit_end = _span(starts, literal)
        m_start, m_end = _span(starts, call.args[1])
        inner = text[m_start:lit_start] + new_src.encode("utf-8") + text[lit_end:m_end]
        detail.update({"literal_before": before, "literal_after": after})
    replaced = (func + b"(" + _padded(actual + b", " + inner, newlines) + b", "
                + json.dumps(marker).encode("utf-8") + b")")
    return replaced, marker


def plan_mutation(data: bytes, spec: dict, mutation: str, instance_id: str,
                  oracle_function: str = "", oracle_note: str = "") -> tuple:
    """(mutated bytes, detail) — nothing is written here.

    `oracle_function` names a function in THESE bytes instead of the test itself: the helper or
    fixture `find_oracle` followed the expectation into."""
    if mutation not in MUTATIONS:
        raise Refusal(f"--mutation is one of {', '.join(MUTATIONS)}")
    bom = data.startswith(b"\xef\xbb\xbf")
    text = data[3:] if bom else data
    try:
        tree = ast.parse(text.decode("utf-8"))
    except (SyntaxError, UnicodeDecodeError) as exc:
        raise Refusal(f"{spec['file']} does not parse: {exc}") from exc
    function = (locate(tree, [], oracle_function) if oracle_function
                else locate(tree, spec["chain"], spec["function"]))
    target = first_assert(function)
    if target is None:
        raise Refusal(f"{spec['node']}: the function body has no assert and no {ASSERT_THAT}() "
                      "call, and neither has any helper or fixture it calls — nothing to mutate. "
                      "If the expectation lives further out than one hop, name it: "
                      "`--oracle [<file>::]<function>`")
    starts = _line_starts(text)
    seg = lambda node: text[slice(*_span(starts, node))]  # noqa: E731
    stmt_start, stmt_end = _span(starts, target)
    original = text[stmt_start:stmt_end]
    newlines = original.count(b"\n")
    detail = {"line": target.lineno, "end_line": target.end_lineno, "mutation": mutation,
              "style": "assert" if isinstance(target, ast.Assert) else ASSERT_THAT,
              "statement_before": original.decode("utf-8", "replace")}
    if oracle_function:
        # The reader must see that the mutated line is not in the test: a probe of a shared
        # oracle proves the expectation fires, and says where that expectation lives.
        detail["oracle_function"] = oracle_function
        detail["oracle_note"] = oracle_note

    rep = Replacement(target, text, starts, seg, newlines)
    if isinstance(target, ast.Assert):
        replaced, marker = _assert_replacement(rep, mutation, instance_id, detail)
    else:
        replaced, marker = _assert_that_replacement(rep, mutation, instance_id, detail)
    detail.update({"statement_after": replaced.decode("utf-8", "replace"), "marker": marker})
    if replaced.count(b"\n") != newlines:
        raise Refusal("internal: the mutated statement would change the file's line count")
    mutated = text[:stmt_start] + replaced + text[stmt_end:]
    try:
        ast.parse(mutated.decode("utf-8"))
    except SyntaxError as exc:
        raise Refusal(f"the mutated statement does not parse ({exc}); report it as tooling") from exc
    return (b"\xef\xbb\xbf" + mutated if bom else mutated), detail


# --- a test in another language: the detector path (B-373 c) ---------------------------------------------
# The Python path above mutates one `assert` found by the AST. For any other language the same proof - "the
# check is live" - needs a way to find the test, its first assertion and the one inverted form of it, and
# that is DATA (`references/detectors.json` `assertion_probes`, FR-13, read only by `assertion_detectors`).
# What is code here is what no table can say: reading the source with the entry's lexer, matching brackets,
# and deciding from the run's report. Every function on this path errs one way: toward a refusal before a
# byte is written, or toward `incomplete` after the run - never toward a verdict on the author's test that
# the tool did not actually read (FR-59, E26).

RED_SANDBOX_DOOR = ("red_sandbox.py --probe --repo <project root> --request <mutations.json> "
                    "--task-root <task root>")
OPEN_BRACKETS, CLOSE_BRACKETS = "([{", ")]}"
BRACKET = re.compile(r"[()\[\]{}]")
LINE_BREAK = re.compile(r"\r\n|\r|\n")
IDENTIFIER = re.compile(r"[A-Za-z_$][\w$]*")
# A line break inside a statement that may end at one (`semicolon_or_newline`): the statement goes on when the
# last code character before the break, or the first one after it, only a continuation can have.
CONTINUES_BEFORE = ".,+-*/%|&=?:<>!"
CONTINUES_AFTER = ".?:,+-*/%|&=<>([`"
OPERAND = "<operand>"  # what the lexer remembers after a string or a regex literal: a `/` after it divides
CANDIDATE_CAP = 5   # candidate declarations a refusal lists, then "and N more"
OFFENDER_CAP = 5    # manifest rows a refusal lists, then "and N more"
NAME_BOUNDARY = ".  /:"   # what may stand right before the tail inside a report id (or nothing: its start)


def _blank(chunk: str) -> str:
    """The chunk with every character but a line break turned into a space: offsets and lines survive."""
    return re.sub(r"[^\r\n]", " ", chunk)


def _string_end(text: str, pos: int, spec: dict) -> int:
    """The index after the closing delimiter of the string whose body starts at `pos`, or -1."""
    close, escape = spec["close"], spec["escape"]
    if escape == "backslash":
        scan = re.compile(r"\\.|" + re.escape(close), re.S)
        while True:
            hit = scan.search(text, pos)
            if hit is None:
                return -1
            if hit.group(0) == close:
                return hit.end()
            pos = hit.end()
    while True:
        found = text.find(close, pos)
        if found < 0:
            return -1
        if escape == "double" and text.startswith(close, found + len(close)):
            pos = found + 2 * len(close)  # a doubled delimiter is one escaped character
            continue
        return found + len(close)


def _line_end(text: str, pos: int) -> int:
    """The index of the line break that ends the line `pos` is on (the end of the text when there is none)."""
    return re.compile(r"[^\r\n]*").match(text, pos).end()


def _regex_opens(text: str, pos: int, spec: dict, prev_char: str, prev_word: str) -> bool:
    """Does the `/` at `pos` open a regular-expression literal rather than divide? By the entry's `after` data: the
    last code character before it is one of `after.chars`, or the word it ends is one of `after.words`, or the
    `/` is the first thing on its line or in the file. After an operand - an identifier, a number, `)`, `]`, a
    string, another literal - it divides (`a / b`, `x = y /g/ 2`)."""
    start = max(text.rfind("\n", 0, pos), text.rfind("\r", 0, pos)) + 1
    after = spec["after"]
    return (not text[start:pos].strip() or (bool(prev_char) and prev_char in after["chars"])
            or prev_word in after["words"] or not prev_char)


def _regex_end(text: str, pos: int, spec: dict) -> int:
    """The index after the closing `/` of the regex literal whose body starts at `pos`, or -1. A backslash escapes
    one character; inside a class `[...]` a `/` does not close; a line break before the close is -1 (unless the
    spec allows lines to be crossed)."""
    escape, close, class_open, class_close = spec["escape"], spec["close"], spec["class_open"], spec["class_close"]
    in_class, index = False, pos
    while index < len(text):
        char = text[index]
        if char == escape:
            index += 2
            continue
        if char in "\r\n" and not spec.get("multiline", False):
            return -1
        if in_class:
            in_class = char != class_close
        elif char == class_open:
            in_class = True
        elif char == close:
            return index + 1
        index += 1
    return -1


def lex(text: str, lexer: dict) -> tuple:
    """(code, skeleton, state). `code` is the text with comments blanked and strings kept (a declaration and
    its title are matched there); `skeleton` is the same with strings blanked too (brackets, heads and
    statement ends are read there: a head inside a string or a comment is never the first assertion, E8).
    Both keep every offset and every line break. `state` is `code`, or what the text ends inside."""
    line_comments = list(lexer.get("line_comments") or [])
    blocks = {opener: closer for opener, closer in lexer.get("block_comments") or []}
    strings = {spec["open"]: spec for spec in lexer["strings"]}
    openers = sorted(set(line_comments) | set(blocks) | set(strings), key=len, reverse=True)
    finder = re.compile("|".join(re.escape(o) for o in openers))
    regex = lexer.get("regex_literal")
    if regex:
        openers = sorted(set(openers) | {regex["open"]}, key=len, reverse=True)
        finder = re.compile("|".join(re.escape(o) for o in openers))
    code, skeleton, at, state = [], [], 0, "code"
    prev_char, prev_word = "", ""  # the last code character before a `/`, and the word it ends (a regex is told from a division by them)
    while at < len(text):
        hit = finder.search(text, at)
        stop = len(text) if hit is None else hit.start()
        code.append(text[at:stop])
        skeleton.append(text[at:stop])
        if hit is None:
            break
        seen = text[at:stop].rstrip()
        if seen:
            prev_char = seen[-1]
            word = re.search(r"[A-Za-z_$][\w$]*$", seen)
            prev_word = word.group(0) if word else ""
        opener = hit.group(0)
        if regex and opener == regex["open"] and not _regex_opens(text, stop, regex, prev_char, prev_word):
            code.append(opener)  # a division sign: code
            skeleton.append(opener)
            prev_char, prev_word, at = opener, "", stop + len(opener)
            continue
        if regex and opener == regex["open"]:
            end = _regex_end(text, stop + 1, regex)
            comment = False
            if end < 0:
                end = _line_end(text, stop)
                state = (f"a regex literal that opens at line {1 + len(LINE_BREAK.findall(text[:stop]))} "
                         "and does not close on its line")
            prev_char, prev_word = OPERAND, ""
        elif opener in line_comments:
            end = re.compile(r"[^\r\n]*").match(text, stop).end()
            comment = True
        elif opener in blocks:
            closed = text.find(blocks[opener], stop + len(opener))
            end, comment = (len(text), True) if closed < 0 else (closed + len(blocks[opener]), True)
            if closed < 0:
                state = "a block comment"
        else:
            end, comment = _string_end(text, stop + len(opener), strings[opener]), False
            prev_char, prev_word = OPERAND, ""  # after a string a `/` is a division
            if end < 0:
                end, state = len(text), "a string literal"
            elif strings[opener].get("multiline", True) is False and LINE_BREAK.search(
                    re.sub(r"\\(?:\r\n|.)", "", text[stop:end], flags=re.S)):
                # A string the language ends at the line break, read across one: the lexer took a quote that
                # is not one (a regex literal `/can't/`, an apostrophe in text it does not know) for an
                # opener, so everything up to the next quote is misread - a head can sit "in code" that is
                # really a string. Only a backslash-newline continuation may cross a line.
                state = ("a single-line string that crosses a line break (it opens at line "
                         f"{1 + len(LINE_BREAK.findall(text[:stop]))})")
        piece = text[stop:end]
        code.append(_blank(piece) if comment else piece)
        skeleton.append(_blank(piece))
        at = end
    return "".join(code), "".join(skeleton), state


def _text_line_starts(text: str) -> list:
    """Where each line of `text` starts, a line ending at `\\r\\n`, `\\r` or `\\n` (axis 7). The Python path
    slices BYTES by `\\n` (`_line_starts`); this reads the decoded text of another language."""
    return [0] + [m.end() for m in LINE_BREAK.finditer(text)]


def lexical_shape(text: str, lexer: dict) -> tuple:
    """What a one-statement edit must leave alone: the count of each bracket outside strings and comments,
    and where the lexer ends."""
    _code, skeleton, state = lex(text, lexer)
    return {char: skeleton.count(char) for char in OPEN_BRACKETS + CLOSE_BRACKETS}, state


class Source:
    """One file as an entry's lexer reads it (see `lex`), with the matching bracket of every opener and
    where each line starts. A file the lexer cannot read to its end, or whose brackets do not balance, is
    refused: a regex literal, an interpolated string with quotes in it or a preprocessor branch can do both,
    and a body found in text that is not certainly read could be the wrong one (E4: never a guess)."""

    def __init__(self, text: str, lexer: dict, file: str = ""):
        self.text = text
        self.code, self.skeleton, state = lex(text, lexer)
        self.starts = _text_line_starts(text)
        if state != "code":
            raise ToolRefusal(f"probe_by_code: the lexer reads {file or 'the file'} to its end inside {state}; a "
                          "construct it does not know (a regex literal, an apostrophe, an interpolated string with "
                          "quotes in it) is in the way, so what is code and what is a string cannot be told with "
                          "certainty, and a mutation could land inside a string. Nothing was changed.")
        self.pairs: dict = {}
        stack = []
        for hit in BRACKET.finditer(self.skeleton):
            index, char = hit.start(), hit.group(0)
            if char in OPEN_BRACKETS:
                stack.append(index)
            elif not stack or OPEN_BRACKETS.index(self.skeleton[stack[-1]]) != CLOSE_BRACKETS.index(char):
                raise self._unbalanced(index, file)
            else:
                self.pairs[stack.pop()] = index
        if stack:
            raise self._unbalanced(stack[-1], file)

    def line(self, index: int) -> int:
        return bisect.bisect_right(self.starts, index)

    def _unbalanced(self, index: int, file: str) -> Refusal:
        return ToolRefusal(f"probe_by_code: the brackets of {file or 'the file'} do not balance at line {self.line(index)} "
                       "as the lexer reads it (a regex literal or a preprocessor branch can do that), so no body "
                       "can be told with certainty. Nothing was changed.")


def _strip_call(value: str) -> str:
    """`Adds(a: 1)` -> `Adds`: a trailing balanced `(...)` is the report's way of showing parameters."""
    value = value.rstrip()
    depth = 0
    for index in range(len(value) - 1, -1, -1):
        if value[index] == ")":
            depth += 1
        elif value[index] == "(":
            depth -= 1
            if depth == 0:
                return value[:index].rstrip()
    return value


def _no_entry(file: str, suffix: str, root, doc: dict) -> Refusal:
    known = "; ".join(f"{language}: {' '.join(entry['suffixes'])}" for language, entry in doc.items())
    directory = root is not None and (Path(root) / file).is_dir()
    what = (f"{file} is a directory, not a test file" if directory
            else f"no assertion probe for {suffix or 'a file with no suffix'} ({file})")
    return (Refusal if directory else ToolRefusal)(     # a directory is the call's fault, a missing row the tool's
        f"probe_by_code: {what} - factory data gap: references/detectors.json `assertion_probes` has entries for "
        f"({known}) and none for this suffix, so this probe reads no test of it (it never guesses a grammar). The "
        f"row to add is one entry in that file, the factory's data and not the author's test: {AD.ENTRY_SHAPE}. "
        f"Return it as a tooling finding. Until the row exists the probe that breaks the product in a throwaway "
        f"copy works for any language: {RED_SANDBOX_DOOR}. Nothing was changed.")


def parse_detector_node(text: str, file: str, tail: str, root=None) -> dict:
    """`tests/CalcTests.cs::CalcTests.Adds` -> the spec of a test in a language with an `assertion_probes`
    entry (E1: the grammar is the one declared for the suffix, never another). The tail is everything after
    the first `::`, split on the entry's `name_separators`; the name is the last segment, the tail is the
    segments joined with the entry's `tail_join` (the form the report id is compared with, R6 c)."""
    try:
        doc = AD.assertion_detectors()
    except AD.DetectorsError as exc:
        raise ToolRefusal(f"probe_by_code: factory data gap - {exc}. Return it as a tooling finding (the table is the "
                      f"factory's); the product-breaking probe does not read it: {RED_SANDBOX_DOOR}. "
                      "Nothing was changed.") from exc
    suffix = Path(file).suffix.lower()
    language, entry = AD.entry_for_suffix(doc, suffix)
    if entry is None:
        raise _no_entry(file, suffix, root, doc)
    method = entry["declaration_style"] == "method"
    separators = sorted(entry["name_separators"], key=len, reverse=True)
    body = _strip_call(tail) if method else tail
    parts = re.split("|".join(re.escape(s) for s in separators), body) if separators else [body]
    segments = [" ".join(part.split()) for part in parts if part.strip()]
    if not segments:
        raise Refusal(f"probe_by_code: --test wants <file>::<test name>, got {text!r} (nothing follows `::`)")
    name = segments[-1]
    if method and not IDENTIFIER.fullmatch(name):
        raise Refusal(f"probe_by_code: the test name {name!r} of --test is not an identifier, and a {language} test is "
                      "found by the name of its method: give the method name (after the class, separated by "
                      f"{' '.join(repr(s) for s in entry['name_separators'])}); parameters belong to the report id. "
                      "Nothing was changed.")
    spec = {"file": file, "chain": segments[:-1], "function": name, "param": "", "node": text,
            "language": language, "entry": entry, "tail": entry["tail_join"].join(segments)}
    template = entry.get("title_template")
    if "${" in name and not template:
        raise Refusal(f"probe_by_code: the title {name!r} holds a template substitution `${{`; a title the runner "
                      "builds at run time cannot be matched against the source, so no test is guessed. Name a test "
                      "with a literal title. Nothing was changed.")
    if template and str(template.get("open") or "") in name:
        # the entry reads templated titles (`title_template`): the title is a pattern, the declaration is found by it. Only a
        # title that keeps too few literal characters binds any row to it, and that is refused (EP1-36).
        literal = "".join(p for kind, p in test_source._template_parts(name, template) if kind == "lit")
        tag = re.compile(entry["title_tag"]) if entry.get("title_tag") else None
        kept = len("".join((tag.sub("", literal) if tag else literal).split()))
        if kept < test_source.MIN_LITERAL:
            raise Refusal(f"probe_by_code: the title {name!r} keeps {kept} literal character(s) around its template "
                          f"substitution (fewer than {test_source.MIN_LITERAL}): a pattern that loose would bind any report "
                          "row to it, so no test is guessed. Name the test by a title with more literal text. "
                          "Nothing was changed.")
        spec["template"] = True
    return spec


# --- locating the body and the first assertion ---------------------------------------------------------

def _titled_declarations(src: Source, entry: dict, name: str, file: str, taken: set) -> list:
    """The declarations of a call-style entry that read their titles as DATA (`title_tag`, `title_template`) and are the test
    `name` names, though the entry's regex with the name escaped in did not match them: a title with a tag the name leaves out,
    a templated title whose pattern fits the name (EP1-36). Each is a match-like (`test_source._Call`: start, end, group) of the
    call, found by the ONE reader of the file (`test_source.matches`, the same predicate a report row is tied by). An `each`
    declaration is not one: its first parenthesis is the table's. Never raises: a file the reader cannot read gives none."""
    try:
        state = {"entry": entry, "src": src, "text": src.text}
        test_source._declarations(state, file)
        decls = state["declarations"]
    except Exception:
        return []
    bare = _untagged(name, entry)
    each = re.compile(entry["each_declaration"]) if entry.get("each_declaration") else None
    out = []
    for decl in decls:
        start = decl["span"][0]
        if start in taken or (each and each.match(src.code, start)):
            continue
        if not (test_source.matches(decl, name) or (decl.get("tags") and decl.get("bare_title") == bare)):
            continue
        opener = src.code.find("(", start)
        if opener < 0 or opener not in src.pairs:
            continue
        out.append(test_source._Call(src.text, start, opener + 1))
    return out


def declaration_candidates(src: Source, entry: dict, name: str, helper: bool = False, file: str = "") -> list:
    """Every match of the declaration pattern that starts in CODE (not inside a string or a comment). For a call-style entry
    that reads titles as data (`title_tag`, `title_template`) the declarations `test_source.matches` ties to the name are
    candidates too (a templated declaration is one), so a tagged or templated test is found by the title the report shows."""
    pattern = AD.declaration_regex(entry, name, helper=helper)
    found = [m for m in pattern.finditer(src.code)
             if src.skeleton[m.start()] == src.code[m.start()] and not src.code[m.start()].isspace()]
    if helper or entry["declaration_style"] != "call" or not (entry.get("title_tag") or entry.get("title_template")):
        return found
    extra = _titled_declarations(src, entry, name, file, {m.start() for m in found})
    return sorted(found + extra, key=lambda m: m.start())


def _direct_children(src: Source, opener: int) -> list:
    """(open, close) of every bracket group standing directly inside the one that opens at `opener`."""
    out, index = [], opener + 1
    while index < src.pairs[opener]:
        close = src.pairs.get(index)
        if close is None:
            index += 1
        else:
            out.append((index, close))
            index = close + 1
    return out


def body_span(src: Source, entry: dict, match, helper: bool = False, file: str = "") -> tuple:
    """(index of `{`, index of its `}`) of the body the declaration `match` opens, or a refusal that names the
    shape (A4). `method`: right after the balanced parameter list `body_open` must match, anchored there, and
    its last `{` opens the body. `call`: inside the call's own argument list, after the title, the first
    `body_open` match that stands directly in that list opens it - not one nested deeper. Invariant: a body
    that is not certainly the named test's is never mutated."""
    style = "method" if helper else entry["declaration_style"]
    line = src.line(match.start())
    shape = ("a concise arrow `() => expr`, a C# `=>` expression body, a declaration with no block (abstract, "
             "interface), or a parameter list with no block after it")
    refusal = Refusal(f"probe_by_code: no block opens where the body of the test declared at line {line} of "
                      f"{file or 'the file'} should ({shape}); a body that is not certainly the named test's is "
                      "never mutated. Nothing was changed.")
    if style == "method":
        opener = match.end() - 1
        if src.skeleton[opener] != "(":
            raise Refusal("probe_by_code: the declaration pattern of the entry must end at the opening parenthesis "
                          "of the parameter list (factory data gap: references/detectors.json). Nothing was changed.")
        pattern = re.compile((helper and entry.get("helper_body_open")) or entry["body_open"])
        found = pattern.match(src.skeleton, src.pairs[opener] + 1)
        if found is None or "{" not in found.group(0):
            raise refusal
        brace = found.start() + found.group(0).rindex("{")
        return brace, src.pairs[brace]
    if "(" not in match.group(0):
        raise Refusal("probe_by_code: the declaration pattern of a call-style entry must contain the opening "
                      "parenthesis of the call (factory data gap: references/detectors.json). Nothing was changed.")
    opener = match.start() + match.group(0).index("(")
    nested = _direct_children(src, opener)
    for found in re.compile(entry["body_open"]).finditer(src.skeleton, match.end(), src.pairs[opener]):
        if "{" in found.group(0) and not any(o <= found.start() <= c for o, c in nested):
            brace = found.start() + found.group(0).rindex("{")
            return brace, src.pairs[brace]
    raise refusal


def _lines_of(src: Source, matches: list) -> list:
    return [src.line(m.start()) for m in matches]


def locate_target(src: Source, entry: dict, name: str, at, helper: bool = False, file: str = "",
                  language: str = "") -> dict:
    """The declaration, its body and the first head in it. Exactly one declaration must match; two or more are
    refused with the candidate lines and the door `--at <line>`, which picks the candidate whose body holds
    that line (and, among the body's heads, the one whose statement starts there). No head, or the first one
    not invertible, is a refusal too (E6, E7): this never skips to a later assertion."""
    matches = declaration_candidates(src, entry, name, helper, file)
    where = f"{file or 'the file'}"
    if not matches:
        raise ToolRefusal(f"probe_by_code: no declaration of {name!r} in {where} matches the {language} entry's "
                          f"`{'helper_declaration' if helper else 'test_declaration'}`. The name is the last segment of "
                          "--test; if the test is declared in a shape the entry does not know, the shape is a row of "
                          f"references/detectors.json assertion_probes.{language} (the factory's data). Nothing was changed.",
                          name_unproved=True)
    lines = _lines_of(src, matches)
    if len(matches) > 1 and at is None:
        raise Refusal(f"probe_by_code: {name!r} is declared {len(matches)} times in {where} "
                      f"({_capped([f'line {n}' for n in lines], CANDIDATE_CAP)}); "
                      "which one is the test is not told by the name. Door: --at <line> (a line inside the body "
                      "you mean). Nothing was changed.")
    chosen = matches[0]
    if len(matches) > 1:
        holding = []
        for match in matches:
            try:
                opener, closer = body_span(src, entry, match, helper, file)
            except Refusal:
                continue
            if src.line(opener) <= at <= src.line(closer):
                holding.append(match)
        if len(holding) != 1:
            raise Refusal(f"probe_by_code: --at {at} lies in {len(holding)} of the {len(matches)} bodies of "
                          f"{name!r} in {where} ({_capped([f'line {n}' for n in lines], CANDIDATE_CAP)}); "
                          "it must lie in exactly one. Nothing was changed.")
        chosen = holding[0]
    opener, closer = body_span(src, entry, chosen, helper, file)
    forms = [re.compile(form["head"]) for form in entry["assertions"]]
    heads = sorted(((m.start(), index, m) for index, rx in enumerate(forms)
                    for m in rx.finditer(src.skeleton, opener + 1, closer)), key=lambda h: (h[0], h[1]))
    if at is not None:
        heads = [h for h in heads if src.line(h[0]) == at]
    if not heads:
        # the tool's gap only when the role did not point at a line: a wrong `--at` is the call's fault (no record for it)
        raise (Refusal if at is not None else ToolRefusal)(
            f"probe_by_code: no recognised assertion {'starts on line ' + str(at) + ' of' if at else 'in'} "
            f"the body of {name!r} (lines {src.line(opener)}-{src.line(closer)} of {where}); this probe "
            "inverts the first assertion form its table knows. Doors: `--oracle [<file>::]<helper>` when "
            "the expectation lives in a helper, or add the assertion's head as a form of "
            f"references/detectors.json assertion_probes.{language} (the factory's data). Nothing was changed.")
    start, index, head = heads[0]
    return {"declaration": chosen, "candidates": lines, "body": (opener, closer), "head_start": start,
            "form": index, "head": head}


def _statement_span(src: Source, start: int, mode: str, limit: int, file: str) -> tuple:
    """(start, end) of the statement that begins at `start`: through the first `;` outside any bracket, or - for
    `semicolon_or_newline` - at a line break outside any bracket that no continuation covers (the next
    non-blank character, or the last one before the break, is an operator that only a continuation can
    carry). A statement not certainly delimited is refused."""
    index = start
    while index < limit:
        char = src.skeleton[index]
        if char in OPEN_BRACKETS:
            index = src.pairs[index] + 1
            continue
        if char in CLOSE_BRACKETS:
            break
        if char == ";":
            return start, index + 1
        if mode == "semicolon_or_newline" and char in "\r\n" and not _continues(src, index, start, limit):
            return start, _trimmed(src, start, index)
        index += 1
    if mode == "semicolon_or_newline":
        return start, _trimmed(src, start, min(index, limit))
    raise Refusal(f"probe_by_code: the statement at line {src.line(start)} of {file or 'the file'} is not ended by "
                  "`;` before its block closes, so its extent is not certain. Nothing was changed.")


def _trimmed(src: Source, start: int, end: int) -> int:
    while end > start and src.code[end - 1].isspace():
        end -= 1
    return end


def _continues(src: Source, brk: int, start: int, limit: int) -> bool:
    before = _trimmed(src, start, brk)
    if before > start and src.code[before - 1] in CONTINUES_BEFORE:
        return True
    after = brk
    while after < limit and src.code[after].isspace():
        after += 1
    return after < limit and src.code[after] in CONTINUES_AFTER


def _matcher_position(src: Source, kind: str, head, stmt_end: int, file: str) -> int:
    """Where the pair's `find` is matched: `head` the start of the head, `after_args` the end of the head's
    balanced `(...)`, `second_arg` the start of the second top-level argument (A3). One position, nowhere
    else in the statement."""
    line = src.line(head.start())
    if kind == "head":
        return head.start()
    shown = f"the assertion at line {line} of {file or 'the file'}"
    if kind == "after_args":
        opener = head.end() - 1
        if src.skeleton[opener] != "(" or src.pairs[opener] >= stmt_end:
            raise Refusal(f"probe_by_code: {shown} is matched by a head that does not end at the opening parenthesis "
                          "of its arguments, so `after_args` has no position (factory data gap). Nothing was changed.")
        return src.pairs[opener] + 1
    opener = head.end()
    while opener < stmt_end and src.skeleton[opener].isspace():
        opener += 1
    if opener >= stmt_end or src.skeleton[opener] != "(":
        raise Refusal(f"probe_by_code: {shown} has no parenthesised argument list right after its head, so its "
                      "second argument cannot be found. Nothing was changed.")
    close, index = src.pairs[opener], opener + 1
    while index < close:
        if src.pairs.get(index) is not None:
            index = src.pairs[index] + 1
        elif src.skeleton[index] == ",":
            index += 1
            while index < close and src.code[index].isspace():
                index += 1
            if index >= close:
                break
            return index
        else:
            index += 1
    raise Refusal(f"probe_by_code: {shown} has no second argument. Nothing was changed.")


def _refuse_conditional_compilation(src: Source, entry: dict, shown: str, language: str) -> None:
    """A file that holds a conditional-compilation directive (the entry's `conditional_directive`, a regex matched
    per line: C# `#if` / `#elif` / `#else` / `#endif`) is refused: the lexer reads every branch as code, but only
    one is compiled, and which one is not knowable here - a mutation could land in the inactive branch, the run
    would pass, and the author's live check would be called dead. `--at` is no door (the inactive branch stays
    unknowable); the doors are a row for that file's shape and the product-level probe."""
    pattern = entry.get("conditional_directive")
    hit = re.compile(pattern, re.M).search(src.skeleton) if pattern else None
    if hit:
        line = src.line(hit.start())
        directive = fold(LINE_BREAK.split(src.text[src.starts[line - 1]:], 1)[0].strip(), 60)
        raise Refusal(f"probe_by_code: {shown} holds the conditional-compilation directive `{directive}` at "
                      f"line {line}: which branch is compiled is not knowable here, so a mutation "
                      "could land in the inactive one and the run would pass for it. This is not a verdict on the "
                      f"test (a gap of the factory's: references/detectors.json assertion_probes.{language}); the "
                      f"probe that breaks the product in a throwaway copy does not read the source: {RED_SANDBOX_DOOR}. "
                      "Nothing was changed.")


def _inverted(src: Source, text: str, entry: dict, language: str, form: dict, head, start: int, end: int,
              shown: str) -> tuple:
    """(pair index, pair, the statement after, the whole mutated text). The first pair of the form whose `find`
    matches AT the form's one position (`re.match`, never a search over the statement) is applied once. Every
    guard of the plan lives here, and each is a refusal with nothing written: no pair matches (the form is known,
    this shape is not), `fires_as` matches the mutated statement itself (a failure text that merely echoes it
    could pass for the intended one - A2), a line break would change (count AND kind, so CRLF stays CRLF), the
    brackets' balance or the lexer's end state would change, a byte outside the statement would change (E7, E9)."""
    line = src.line(start)
    position = _matcher_position(src, form["matcher_at"], head, end, shown)
    chosen = next(((index, pair, hit) for index, pair in enumerate(form["invert"])
                   for hit in [re.match(pair["find"], text[position:end])] if hit and hit.end() > 0), None)
    if chosen is None:
        raise Refusal(f"probe_by_code: no inversion pair of the {language} table matches at the {form['matcher_at']} "
                      f"position of the assertion at line {line} of {shown} (`{fold(text[position:end], 80)}`); the "
                      "form is recognised but this shape of it is not (Hamcrest `assertThat(x, is(y))`, Chai "
                      "`.to.equal`, a chain on the next line): nothing is skipped to a later assertion. Doors: "
                      "`--at <line>` or a row for this shape in references/detectors.json. Nothing was changed.")
    index, pair, hit = chosen
    which = pair.get("id") or index
    try:
        replacement = hit.expand(pair["replace"])
    except (re.error, IndexError) as exc:
        raise Refusal(f"probe_by_code: the `replace` of pair {which} of assertion_probes.{language} "
                      f"cannot be expanded ({exc}) - factory data gap. Nothing was changed.") from exc
    before = text[start:end]
    after = text[start:position + hit.start()] + replacement + text[position + hit.end():end]
    if AD.fires_in(pair["fires_as"], after):
        raise Refusal(f"probe_by_code: the failure this inverted form must show (pair {which}) would "
                      f"also match the mutated statement's own text (`{fold(after, 100)}`), so a failure text that "
                      "merely echoes the statement could pass for the intended one. Nothing was changed.")
    if LINE_BREAK.findall(before) != LINE_BREAK.findall(after):
        raise Refusal(f"probe_by_code: the inversion (pair {which} of assertion_probes.{language}) would "
                      f"change the line breaks of the statement at line {line} of {shown}: an edit may not move a "
                      "line or turn CRLF into LF, and a `find` that matches the whitespace of a chain split over "
                      "lines consumes its break. Nothing was changed. The assertion can be inverted by a pair whose "
                      "`find` captures that whitespace (a row of references/detectors.json, the factory's data).")
    mutated = text[:start] + after + text[end:]
    if lexical_shape(mutated, entry["lexer"]) != lexical_shape(text, entry["lexer"]):
        raise Refusal(f"probe_by_code: the inversion would change the bracket balance or the lexical state of "
                      f"{shown}. Nothing was changed.")
    # `mutated` is built from `text[:start]` and `text[end:]` verbatim, so no byte outside the statement can
    # change; the assertion states that invariant (it cannot fire unless this function is edited wrongly).
    assert mutated.startswith(text[:start]) and mutated.endswith(text[end:])
    return index, pair, after, mutated


def plan_detector_mutation(data: bytes, spec: dict, instance_id: str, at=None, oracle_function: str = "",
                           oracle_note: str = "", file: str = "") -> tuple:
    """(mutated bytes, detail, context) - nothing is written here; `context` is the code between the end of the
    previous statement or block and the declaration (where an annotation such as a display name stands). The
    first head of the body is the target; a form with `invert: null` is a refusal (it never skips to a later
    assertion, E7), any other form is inverted by `_inverted`, whose guards are refusals too. A BOM and CRLF
    line ends are kept; a file that is not UTF-8 is refused (E21)."""
    entry, language, shown = spec["entry"], spec["language"], file or spec["file"]
    bom = data.startswith(b"\xef\xbb\xbf")
    try:
        text = (data[3:] if bom else data).decode("utf-8")
    except UnicodeDecodeError as exc:
        raise Refusal(f"probe_by_code: {shown} is not UTF-8 ({exc.reason} at byte {exc.start}); a file read in the "
                      "wrong encoding is never mutated. Nothing was changed.") from exc
    src = Source(text, entry["lexer"], shown)
    _refuse_conditional_compilation(src, entry, shown, language)
    name = oracle_function or spec["function"]
    found = locate_target(src, entry, name, at, bool(oracle_function), shown, language)
    head, form = found["head"], entry["assertions"][found["form"]]
    start, end = _statement_span(src, found["head_start"], entry["statement_end"], found["body"][1], shown)
    line, end_line = src.line(start), src.line(max(start, end - 1))
    if form["invert"] is None:
        raise Refusal(f"probe_by_code: the first assertion of {name!r}, `{fold(head.group(0))}` at line {line} of {shown}, "
                      f"is a form the {language} table does not invert (assertion_probes.{language}.assertions"
                      f"[{found['form']}].invert is null); it never skips to a later assertion, because what is "
                      "mutated must be what the record says. Doors: `--at <line>` names another assertion of the "
                      "body, `--oracle [<file>::]<helper>` another place. Nothing was changed.")
    index, pair, after, mutated = _inverted(src, text, entry, language, form, head, start, end, shown)
    before = text[start:end]
    marker = f"probe-{instance_id} invert: {fold(before)} fires as /{pair['fires_as']}/"
    detail = {"line": line, "end_line": end_line, "mutation": "invert", "style": "detector", "language": language,
              "head": head.group(0), "form": found["form"], "pair": index, "pair_id": pair.get("id"),
              "at": at, "candidates": found["candidates"], "statement_before": before, "statement_after": after,
              "fires_as": pair["fires_as"], "marker": marker, "matcher_at": form["matcher_at"],
              "declaration_line": src.line(found["declaration"].start()), "file": shown}
    if oracle_function:
        detail["oracle_function"], detail["oracle_note"] = oracle_function, oracle_note
    return (b"\xef\xbb\xbf" if bom else b"") + mutated.encode("utf-8"), detail, _context(src, found["declaration"])


def _context(src: Source, declaration) -> str:
    """The code just before a declaration: from the last `;`, `{` or `}` before it."""
    index = declaration.start()
    while index > 0 and src.skeleton[index - 1] not in ";{}":
        index -= 1
    return src.code[index:declaration.start()]


# --- the checks that stand before the first write (R6, E10) ----------------------------------------------

def _in_test_root(cfg: dict, rel: str) -> bool:
    """E10, the interim rule: `rel` (project-relative, POSIX) lies under a profile's `roots.test` (or the
    config's `tests_root`) and under no `protected_app_paths` entry (those are relative to `app_root`). The
    seam B-415 widens: `test_locations.is_test_path(rel, cfg).by == "config"` will also pass; `markers` alone
    never does. Invariant: the product tree is never touched knowingly.

    EP1-12 (AR-13, AR-15): every path here is spelled by `execution_request._path_key` and compared by
    `execution_request.path_under` - the pair `profiles_owning` uses - so `./tests`, `tests\\x` and `tests/a/../x`
    are one spelling. The direction of error is only toward False (the edit is refused): an empty path, an absolute
    path (`/x`, `\\x`, `C:...`: `_path_key` would cut the outer slash and read `/tests/x.py` as `tests/x.py`) and a
    path that climbs out of the project (`..`) are False before any compare; the protected paths are checked after
    the roots and win over them."""
    import execution_request as ER
    text = str(rel or "").replace("\\", "/").strip()     # stripped ONCE, before every absolute check: ` /x` is `/x`, as `_path_key` reads it
    if not text or text.startswith("/") or re.match(r"^[A-Za-z]:", text):
        return False
    key = ER._path_key(text)
    if not key or key == ".." or key.startswith("../"):
        return False
    roots = [ER._path_key((p.get("roots") or {}).get("test")) for p in cfg.get("profiles") or [] if isinstance(p, dict)]
    roots.append(ER._path_key(cfg.get("tests_root")))
    if not any(r and not (r == ".." or r.startswith("../")) and ER.path_under(key, r) for r in roots):
        return False
    app = str(cfg.get("app_root") or ".").replace("\\", "/")
    for protected in cfg.get("protected_app_paths") or []:
        base = ER._path_key(posixpath.join(app, str(protected).replace("\\", "/")))
        if not base or ER.path_under(key, base):
            return False
    return True


def _capped(items: list, cap: int = OFFENDER_CAP) -> str:
    return ", ".join(items[:cap]) + (f" and {len(items) - cap} more" if len(items) > cap else "")


def _normalised_id(report_id: str, entry: dict) -> list:
    """The report id as it is compared with the --test tail: a trailing `(...)` stripped (parameters), `::` and
    the entry's `report_separators` turned into `tail_join`, whitespace folded. Both spellings (with and
    without the parentheses) come back: a title that really ends in `)` must not be lost to the strip."""
    out = []
    for raw in (_strip_call(report_id), report_id):
        text = raw.replace("::", entry["tail_join"])
        for separator in entry.get("report_separators") or []:
            text = text.replace(separator, entry["tail_join"])
        out.append(_untagged(text, entry))
    return out


def _untagged(text: str, entry: dict) -> str:
    """`text` with the entry's own tags (`title_tag`: a `@smoke` in a title) taken out and the whitespace folded; both sides of
    every title comparison go through here, so a tag the report keeps and the --test leaves out (or the reverse) is no mismatch.
    An entry without `title_tag` gets the whitespace fold alone, as before."""
    if entry.get("title_tag"):
        text = re.sub(entry["title_tag"], "", text)
    return " ".join(text.split())


def _tail_matches(report_id: str, tail: str, entry: dict) -> bool:
    folded = _untagged(tail, entry)
    for candidate in _normalised_id(report_id, entry):
        if candidate.endswith(folded) and (len(candidate) == len(folded) or candidate[-len(folded) - 1] in NAME_BOUNDARY):
            return True
    return False


def _profile_of(cfg: dict, rows: list, case: str) -> dict:
    """The profile `build_mine_request` will pick for these rows (its own selector, `_profile_for`: one reading
    of "which profile runs this", FR-17), or a refusal."""
    import execution_request as ER
    files = sorted({str(r["node"]).split("::")[0] for r in rows})
    try:
        # This tool takes no `--profile`: the refusal names only the manifest-row door (FR-2).
        wanted = ER._profile_for(cfg, files, "", [r["entry"] for r in rows], [], [case], profile_door=False)
    except ER.MineRefusal as exc:
        raise Refusal(f"probe_by_code: {str(exc).rstrip('. ')}. Nothing was changed.") from exc
    return next((p for p in cfg.get("profiles") or [] if isinstance(p, dict) and p.get("profile_id") == wanted), {})


def _longer_title(text: str, entry: dict, tail: str, report_id: str) -> tuple:
    """(title, line) of ANOTHER test of the file whose title ends with `tail` at a boundary and that the report
    id ends with too, else ("", 0). For a call-style entry the join and the boundary are both a space, so the
    id of the test titled `calc does not adds` also "ends with" `adds`: `--test x.ts::adds` against that row
    would pass R6(c), and the pass of the OTHER test would be read as a dead check for this one."""
    try:
        src = Source(text, entry["lexer"])
        pattern = re.compile(entry["test_declaration"].replace(AD.NAME, "(?P<_title>[^\r\n]+?)"))
    except (Refusal, re.error) as exc:
        raise Refusal("probe_by_code: the titles of the other tests of the file cannot be listed to tell them from "
                      f"this one ({str(exc)[:120]}), and a report id that ends with several titles is ambiguous. "
                      "Nothing was changed.") from exc
    for found in pattern.finditer(src.code):
        if src.skeleton[found.start()] != src.code[found.start()]:
            continue
        # the other test's title as written (a templated one with its `${...}`; tags out on BOTH sides, so the same test with
        # a tag the --test leaves out is not "another test")
        title = _untagged(found.group("_title"), entry)
        if title != _untagged(tail, entry) and _tail_matches(title, tail, entry) and _tail_matches(report_id, title, entry):
            return title, src.line(found.start())
    return "", 0


def _pattern_ends(pattern: str, report_id: str, entry: dict) -> bool:
    """Does the report id END with a title the `pattern` (a templated title's, `test_source` shape) fits, at a name boundary?
    A pattern that does not compile fits nothing."""
    for candidate in _normalised_id(report_id, entry):
        try:
            if re.search("(?:^|[" + re.escape(NAME_BOUNDARY) + "])(?:" + pattern + ")$", candidate):
                return True
        except re.error:
            return False
    return False


def _report_id_fits(report_id: str, spec: dict, entry: dict) -> bool:
    """R6 (c): the row's report id ends with the --test tail. A templated --test title also fits a report id that is the title
    RENDERED (a role wrote what the runner printed): the id then ends with a string the title's own pattern fits."""
    if _tail_matches(report_id, spec["tail"], entry):
        return True
    if not spec.get("template"):
        return False
    pattern = test_source._shape(spec["function"], entry, False)[1]
    return bool(pattern) and _pattern_ends(pattern, report_id, entry)


def _code_built(cfg: dict, row_entry: dict, argv, root):
    """The selector and report identity the CODE builds for a manifest row that carries none of its own
    (`execution_request.code_selection`, the ONE builder: `--mine` calls it for the same row, EP1-37), or None. The row's profile
    directory is `_profile_cwd`'s; with no project `root` nothing is built (a caller that has none keeps the hand-written rule)."""
    if root is None:
        return None
    import execution_request as ER
    run_cwd = Path(root) / _profile_cwd(cfg, str(row_entry.get("file") or ""), ER.entry_profile_id(row_entry))
    return ER.code_selection(row_entry, argv, run_cwd, Path(root))


def run_shape_checks(cfg: dict, manifest: dict, case: str, entry_row: dict, spec: dict, instance_id: str,
                     context: str, text: str, root=None) -> None:
    """R6: what must hold before one byte is written, because the whole CASE runs (a non-pytest runner
    selects by the manifest's own arguments, not by a node id) and only the row whose report id equals the
    instance's is read. Exit 2, "Nothing was changed". (a) every row of the case has `selector_args` and a
    `report_test_id` - its own, or the ones the code builds for it (`_code_built`; the role's own win, as in `--mine`) - no file
    of it is bare, and the profile's selectors are verified (`profile_contract.selectors_verified`); (b) --test names the
    manifest row's file; (c) the row's report id ends with the --test tail; (d) a compiled entry's launch does
    not forbid a rebuild. Invariant: the mutated test is the test the run selects, and a mutation that never
    reached the build never yields `no_failure` (E11, E12, E14). A row nothing selects on a profile whose command is the
    project's own script is refused BY NAME (`no_direct_form`) and never passes (FR-41, AR-28); `root` is the project, not a clone."""
    import execution_request as ER
    import launch_check
    import profile_contract as PC   # the ONE reader of the `commands` shape (OH3-27, AR-13)
    entry = spec["entry"]
    rows, bare = ER.manifest_rows(manifest, case)
    profile = _profile_of(cfg, rows, case) if rows else {}
    argv = PC.one_test_argv(profile)[0]
    offenders = []
    for row in rows:
        lacks = [name for name, ok in (("selector_args", isinstance(row["entry"].get("selector_args"), list)
                                        and bool(row["entry"]["selector_args"])),
                                       ("report_test_id", bool(str(row["entry"].get("report_test_id") or "").strip())))
                 if not ok]
        if lacks and _code_built(cfg, row["entry"], argv, root) is None:
            offenders += [f"{row['instance_id']} (no `{name}`)" for name in lacks]
    offenders += [f"{file} (names no test)" for file in bare]
    verified = PC.selectors_verified(profile, root)
    if offenders or not verified:
        no_form = str(launch_check.runner_identity(argv)["no_direct_form"] or "") if offenders else ""
        if no_form:
            raise ToolRefusal(f"probe_by_code: {no_form}; the probe is not run on this profile; onboarding offers the "
                              f"direct form. {len(offenders)} instance(s) of {case} that the run would select have no selector "
                              f"of their own: {_capped(offenders)}. Nothing was changed.")
        problems = []
        if offenders:
            problems.append(f"{len(offenders)} instance(s) of {case} that the run would select have no selector of "
                            f"their own: {_capped(offenders)}")
        if not verified:
            problems.append(f"profile {profile.get('profile_id') or '(none found)'} does not say its selector contract "
                            "is verified (selectors.verified in qa-factory/config.json: the onboarding's gap)")
        raise ToolRefusal("probe_by_code: " + "; ".join(problems) + ". A non-pytest runner runs the whole case, and the "
                          "factory binds one report row by the report id the manifest records; the automator records "
                          "them once through `manifest_put.py --task <TICKET> --fragment <file>` "
                          '(`{"tests": [{"instance_id": "<id>", "selector_args": ["<the framework\'s own arguments>"], '
                          '"report_test_id": "<the runner\'s name>"}]}`), then probe again. Nothing was changed.')
    row_file = str(entry_row.get("file") or "").replace("\\", "/")
    if not _same_file(row_file, spec["file"]):
        raise Refusal(f"probe_by_code: --test names {spec['file']}, but the manifest row of {instance_id!r} names "
                      f"{row_file or 'no file'}: the mutated file must be the one the run selects. Nothing was changed.")
    report_id = str(entry_row.get("report_test_id") or "").strip()
    if not report_id:       # the row carries none: the id the code builds for it is the one the run reports under
        report_id = str((_code_built(cfg, entry_row, argv, root) or {}).get("report_test_id") or "")
    if not _report_id_fits(report_id, spec, entry):
        shown = (f"the report id of {instance_id!r} is {report_id!r}; it does not end with {spec['tail']!r} (the --test "
                 f"tail, segments joined by {entry['tail_join']!r}, after the same normalisation), so the test named "
                 "here is not certainly the test the run reports under that id.")
        if entry.get("display_name") and re.search(entry["display_name"], context):
            shown += (" The declaration carries a display name, and the report may name this test by it: the "
                      "manifest's `report_test_id` must be the runner's id for the method.")
        raise Refusal(f"probe_by_code: {shown} Fix --test or the row's `report_test_id` (manifest_put.py --fragment). "
                      "Nothing was changed.")
    longer, where = _longer_title(text, entry, spec["tail"], report_id) if entry["declaration_style"] == "call" else ("", 0)
    if longer:
        raise Refusal(f"probe_by_code: the report id of {instance_id!r} ({report_id!r}) ends with {spec['tail']!r}, but it "
                      f"also ends with the longer title {longer!r} of another test declared at line {where} of "
                      f"{spec['file']}: the row may belong to that test, and its pass would be read as a dead check of "
                      f"{spec['tail']!r}. Give --test the full title, or fix the row's `report_test_id` "
                      "(manifest_put.py --fragment). Nothing was changed.")
    if entry["compiled"]:
        argv, problem = PC.one_test_argv(profile)
        if problem:
            # no words, no proof that the build is the one that rebuilds: reading "no flag found" here would let a dead
            # check pass as a live one - the very thing this refusal guards
            raise Refusal(f"probe_by_code: profile {profile.get('profile_id') or '(none found)'}: {problem}. Nothing was changed.")
        stop = [a for a in argv if a in entry["no_rebuild_flags"]]
        if stop:
            raise Refusal(f"probe_by_code: the profile's one-test command carries {', '.join(stop)}, which stops the "
                          f"{spec['language']} build from picking up the mutated source, so the run would execute the "
                          "author's compiled test and report a pass for a check that never ran. Run the probe on a "
                          "profile whose command builds (the onboarding's `commands.one_test`). Nothing was changed.")


def manifest_entry(task_root: Path, instance_id: str) -> dict:
    path = task_root / "work" / "automation-manifest.json"
    manifest = C.load_json(path) if path.is_file() else {}
    for entry in C.manifest_tests(manifest):
        if not isinstance(entry, dict):
            continue
        ids = {str(entry.get("instance_id") or "")} | set(C.instance_id_aliases(entry))
        if instance_id in ids:
            return entry
    raise Refusal(f"the manifest names no instance {instance_id!r} (work/automation-manifest.json) — "
                  "the automator records it through manifest_put.py first")


def obligation_fields(entry: dict) -> tuple:
    """The four fields the window's `probe` must repeat from its instance, and what is missing."""
    refs = entry.get("obligation_refs") if isinstance(entry.get("obligation_refs"), list) else []
    ids = entry.get("obligation_ids") if isinstance(entry.get("obligation_ids"), list) else None
    if ids is None and refs:
        ids = [str(r.get("obligation_id")) for r in refs if isinstance(r, dict) and r.get("obligation_id")]
    if ids is None and entry.get("obligation_id"):
        ids = [str(entry["obligation_id"])]
    fields = {"obligation_ids": ids or [],
              "obligation_hash": entry.get("obligation_hash") or (content_hash(refs) if refs else None),
              "defect_location": entry.get("defect_location") or None,
              "assertion_id": entry.get("assertion_id") or None}
    if refs:
        fields["obligation_refs"] = refs
    missing = [k for k in MANIFEST_FIELDS if not fields.get(k)]
    return fields, missing


# --- the run ---------------------------------------------------------------------------------------

def probe_runtime(spec: dict) -> dict:
    """The read-only runtime probe `--mine` runs before a first typed run of a profile - `run_suite.probe_runtime`, the
    ONE strict reader (t-300 N2 S8, FR-17). This function used to hold a copy of it that took `matched` only: a person's
    word reached the role's own `--mine` and not the critic's red probe, and a probe that compared nothing
    (`no_changed_file`) was refused here and taken there (B-255 a). One function, one exception class
    (`ProvenanceRefused`), one message; the delegate is imported on use (run_suite imports this package's modules)."""
    import run_suite
    return run_suite.probe_runtime(spec)


def _profile_cwd(cfg: dict, file: str, profile_id: str = "") -> str:
    """The run directory of the profile that owns this file ('.' when none does). The owners are asked of the one
    predicate `_profile_for` asks (`execution_request.profiles_owning`); `profile_id` is the profile the manifest
    row NAMES (`execution_request.entry_profile_id`), which settles a shared root. Invariant: a root several
    profiles share never gives the first profile's directory: when they run in one directory that directory is
    the answer (no guess is made), when they run in different ones the tie is refused with its door. A profile the
    row names that the config does not hold is refused too (EP1-16, A-E4): it is not read as a path, which would run
    the test under whichever profile owns the file - the same predicate and words as `_profile_for`
    (`execution_request.known_profile`, AR-13)."""
    import execution_request as ER
    profiles = {str(p.get("profile_id")): p for p in cfg.get("profiles") or [] if isinstance(p, dict)}
    if profile_id and not ER.known_profile(cfg, profile_id):
        raise Refusal("probe_by_code: " + ER.unknown_profile_refusal(cfg, profile_id, ER.NAMED_BY_ROW)
                      + ". Nothing was changed.")
    owners = [profile_id] if profile_id else ER.profiles_owning(cfg, file)
    import profile_contract as PC     # the ONE reader of the `commands` shape (OH3-27, AR-13)
    # a profile whose commands cannot be read names no directory (as one with no `cwd`): the run is refused earlier, where the
    # command is built from it, with the shape problem
    cwds = {str(PC.profile_command(profiles[o], "one_test")[0].get("cwd") or ".")
            for o in owners if o in profiles}
    if len(cwds) > 1:
        raise Refusal(f"probe_by_code: profiles {', '.join(owners)} share the test root of {file} and run in "
                      "different directories, so the path cannot tell where this test runs; name the profile on "
                      "the manifest row of the instance (`profile_id`). Nothing was changed.")
    return cwds.pop() if cwds else "."


def build_request(root: Path, cfg: dict, task: str, dispatch: str, case: str, spec: dict,
                  instance_id: str, mutation: str, reason: str, profile_id: str = "", s6_close: bool = False,
                  mutation_kind: str = MUTATION_KIND) -> tuple:
    """The typed red_probe request of this one node, built by the code `--mine` uses. With `s6_close` the dispatch
    is the S6 close context (`execution_request.s6_close_dispatch`, read afresh): `dispatch` is then only the
    name the idempotency key starts with, and no dispatch id goes to the builder. A test that is not
    Python (`spec["language"]`) is selected the way L9 of the sandbox probe selects one: the request is built
    for the whole case (a non-pytest runner takes the manifest's own `selector_args`, never a node id built
    here), and the instance must be one of the instances it selects (R7)."""
    from execution_request import JobStore, build_mine_request
    detector = bool(spec.get("language"))
    # A red probe is always told where to run (the request builder refuses one that is not). This
    # probe mutates the author's tree in place - there is no clone - so the directory is passed
    # as `--cwd`, and it is the profile's own: the one the call used to be retried with after a
    # refusal whose WORDING it matched on. The profile the row names goes to the builder too (EP1-16): it used to
    # settle only the directory, and the builder then refused a root two profiles share for want of the name it had
    # been given one line above. This tool has no `--profile`: the builder's refusal names the row door only.
    cwd = (root / _profile_cwd(cfg, spec["file"], profile_id)).resolve()
    request, notes, _reusable, _verified = build_mine_request(
        root, [case], cfg=cfg, task=task, dispatch_id="" if s6_close else dispatch, purpose="red_probe",
        node_ids=None if detector else [spec["node"]], again=True, reason=reason, probe=probe_runtime,
        cwd=str(cwd), profile_id=profile_id, profile_door=False, s6_close=s6_close)
    selected = list(request.get("selected_instance_ids") or [])
    if detector:
        if instance_id not in selected:
            raise Refusal(f"the request for {case} selects {selected}, which does not include {instance_id!r}")
    elif selected != [instance_id]:
        raise Refusal(f"--test {spec['node']} names instance {selected}, not {instance_id!r}")
    jobs = JobStore(artifacts_dir(task) / "state" / "execution-jobs").jobs()
    taken = {str(j.get("idempotency_key")) for j in jobs}
    base = f"{dispatch}:red_probe:probe-{instance_id}:{mutation}:{request['input_fingerprint'][:12]}"
    key, attempt = base, 1
    while key in taken:
        attempt += 1
        key = f"{base}:again-{attempt}"
    request["idempotency_key"] = key
    request["reason"] = reason
    request["built_by"] = {"tool": "probe_by_code.py", "cases": [case], "instance_id": instance_id,
                           "mutation": mutation, "mutation_kind": mutation_kind}
    return request, notes


def run_request(root: Path, request_path: Path, timeout: int) -> tuple:
    """`run_suite.py --request <file>` as a subprocess (or `PROBE_RUN_SUITE`); (proc, summary)."""
    runner = os.environ.get("PROBE_RUN_SUITE") or str(Path(__file__).resolve().parent / "run_suite.py")
    argv = [sys.executable, "-B", runner, "--request", str(request_path)]
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", QA_FACTORY_SKIP_DASHBOARD_REFRESH="1")
    proc = subprocess.run(argv, cwd=str(root), capture_output=True, text=True, encoding="utf-8",
                          errors="replace", timeout=timeout, env=env)
    lines = [ln for ln in (proc.stdout or "").splitlines() if ln.strip().startswith("{")]
    try:
        summary = json.loads(lines[-1]) if lines else {}
    except ValueError:
        summary = {}
    return proc, summary if isinstance(summary, dict) else {}


# --- reading the result ------------------------------------------------------------------------

DEFAULT_REPORTER = "junit-xml"


def report_rows(path: Path, reporter: str, raw: bool = False) -> list:
    """`raw`: the shared reader's own rows (`{test_id, status, problems}`), for the path that binds a row
    by the runner's report id and reads its frames (a test that is not Python). Otherwise:

    The run's report as `{test_id, status, message, text}` rows, read by the shared reader
    (`reporters.read_rows`, dispatched on the TYPED `reporter` of the run's summary).

    `observe` below wants one status and one message/stack per row, as this script's private
    JUnit reader gave them: the FAILURE's own message and stack when the testcase has one, else
    the ERROR's, and then the status is `failed` / `error` — even beside a `<skipped>` child. The
    shared reader keeps every problem of the row in document order and lets a skip outrank a
    failure in `status`; this picks from `problems` what the private reader picked. A row with
    neither keeps the shared reader's status (`passed`, `skipped`, TRX `not_run`)."""
    if raw:
        return reporters.read_rows(path, reporter)
    rows = []
    for row in reporters.read_rows(path, reporter):
        problems = row.get("problems") or []
        chosen = next((p for p in problems if p.get("kind") == "failure"),
                      next((p for p in problems if p.get("kind") == "error"), None))
        status = row.get("status")
        if chosen is not None:
            status = "failed" if chosen["kind"] == "failure" else "error"
        rows.append({"test_id": row["test_id"], "status": status,
                     "message": (chosen or {}).get("message", ""), "text": (chosen or {}).get("text", "")})
    return rows


def _tail(node_id: str) -> str:
    return str(node_id or "").replace("\\", "/").rsplit("::", 1)[-1]


def _same_file(observed: str, expected_file: str) -> bool:
    observed = observed.replace("\\", "/")
    expected_file = expected_file.replace("\\", "/")
    return observed == expected_file or observed.endswith("/" + expected_file) or \
        expected_file.endswith("/" + observed)


def observe(row: dict, spec: dict, detail: dict) -> dict:
    """What the report says: the last traceback line (pytest's own `path:line: Exception`),
    and, when that line is inside a helper (hamcrest, a page object), the deepest frame of the
    test file itself."""
    out = {"status": row.get("status"), "message_head": fold((row.get("message") or "").splitlines()[0]
                                                            if row.get("message") else "", 300)}
    lines = [ln.strip() for ln in (row.get("text") or "").splitlines() if ln.strip()]
    last = _TRACE_TAIL.match(lines[-1]) if lines else None
    if last:
        exc = last.group("exc").split(".")[-1]
        out["location"] = last.group("loc")
        out["failure_kind"] = ("assertion" if exc == "AssertionError" else
                               "error" if row.get("status") == "error" else "exception")
    elif row.get("status") in {"failed", "error"}:
        out["failure_kind"] = "error" if row.get("status") == "error" else "exception"
        head = (row.get("message") or "").split(":", 1)[0].strip()
        if head == "AssertionError":
            out["failure_kind"] = "assertion"
    frames = []
    for line in lines:
        match = _FRAME.match(line)
        if match and _same_file(match.group("path"), spec["file"]):
            frames.append((match.group("path"), int(match.group("line"))))
    if frames:
        out["test_file_frame"] = f"{frames[-1][0]}:{frames[-1][1]}"
    return out


def _location_hits(location: str, spec: dict, detail: dict) -> bool:
    if not location:
        return False
    path, _, line = location.replace("\\", "/").rpartition(":")
    return line.isdigit() and _same_file(path, detail.get("file") or spec["file"]) and \
        detail["line"] <= int(line) <= detail["end_line"]


def verdict_of(observed: dict, spec: dict, detail: dict) -> tuple:
    """(verdict, actual_location, actual_reason, mismatches)."""
    marker = detail["marker"]
    expected_location = f"{spec['file']}:{detail['line']}"
    status = observed.get("status")
    if status == "passed":
        return "no_failure", None, None, ["the mutated assert never fired"]
    if status not in {"failed", "error"}:
        return "not_executed", None, None, [f"report status {status!r}"]
    location = observed.get("location") or observed.get("test_file_frame") or ""
    hit = _location_hits(observed.get("location") or "", spec, detail) or \
        _location_hits(observed.get("test_file_frame") or "", spec, detail)
    head = observed.get("message_head") or ""
    head = head[len("AssertionError:"):].strip() if head.startswith("AssertionError:") else head
    reason_hit = fold(head, 10_000) == fold(marker, 10_000) or marker in head
    mismatches = []
    if not hit:
        mismatches.append("location")
    if not reason_hit:
        mismatches.append("reason")
    if observed.get("failure_kind") != "assertion":
        mismatches.append("failure_kind")
    if not mismatches:
        return "intended_failure", expected_location, marker, []
    return "wrong_location", location or None, head or None, mismatches


# --- reading the run of a test in another language (R8) ------------------------------------------------
# Python's `observe` / `verdict_of` read pytest's own traceback. Here the site comes from
# `reporters.assertion_site` with the entry's frame grammar, and the verdict table is the one place that
# decides what the tool may say about the AUTHOR's test. Only a failure at the mutated statement, with the
# message the inverted form must show, is `intended_failure`; anything the tool did not read well enough
# (an error row, an unresolvable frame, a message the row does not know, a launcher that may not rebuild) is
# `incomplete`, never a verdict on the test (FR-59, E15, E26).

def text_head(text: str, entry: dict) -> str:
    """The failure's text above its first stack frame or skipped line."""
    frames, skip, _path = AD.grammar_of(entry)
    stops = [re.compile(pattern) for pattern in frames + skip]
    lines = []
    for line in str(text or "").splitlines():
        if any(stop.search(line) for stop in stops):
            break
        lines.append(line)
    return "\n".join(lines)


def failure_problem(row: dict) -> dict:
    problems = row.get("problems") or []
    return next((p for p in problems if p.get("kind") == "failure"),
                next((p for p in problems if p.get("kind") == "error"), {}))


def fires_on(row: dict, entry: dict, fires_as: str) -> bool:
    """Does the failure show the message the inverted form must? The `message` first; the text above the first
    frame when the message is empty OR does not match (a Playwright junit message may be `file:line title`).

    RN1-8: the runner's failure body (`text_head`) is read through `AD.fires_in`: the whole text and EACH LINE of it, leading
    whitespace cut, so a `^` in the row's sample binds to the start of a line and not of the whole text (a Playwright report
    opens with a header and its own `Error: <msg>` line; the library's `expect(received)...` line comes after, indented). The
    `message` attribute stays matched WHOLE, as before (`by_line=False`). What this does NOT bound: a line of the failure body
    that is the author's own assertion message can fire a row, as it could when it opened the body; the caller's location
    check bounds WHERE the failure is, not WHOSE words it shows. A blank line is skipped."""
    problem = failure_problem(row)
    message = str(problem.get("message") or "")
    head = text_head(problem.get("text"), entry)
    return AD.fires_in(fires_as, message, by_line=False) or AD.fires_in(fires_as, head)


def launcher_words(argv) -> str:
    """The launch as argv basenames joined by spaces, `.exe` / `.cmd` / `.bat` stripped."""
    words = []
    for token in argv or []:
        name = posixpath.basename(str(token).strip("\"'").replace("\\", "/"))
        for suffix in (".exe", ".cmd", ".bat"):
            if name.lower().endswith(suffix):
                name = name[:-len(suffix)]
        words.append(name)
    return " ".join(words)


def builds_by_default(argv, entry: dict) -> str:
    """The `builds_by_default` prefix this launch starts with (at a token boundary), or ""."""
    words = launcher_words(argv)
    return next((prefix for prefix in entry["builds_by_default"] if words == prefix or words.startswith(prefix + " ")), "")


def judge_detector(row: dict, site: dict, entry: dict, detail: dict, *, among: bool, argv) -> dict:
    """The R8 table. {verdict, actual_location, actual_reason, mismatches, observed, note}; `note` is the one
    sentence a reader needs when the verdict is not `intended_failure`.

      passed   + `--at` chose among 2+ candidates     -> incomplete  (a pass says nothing about WHICH body ran)
      passed   + compiled, launcher may not rebuild   -> incomplete  (the mutation may never have been built)
      passed   otherwise                              -> no_failure
      error                                           -> incomplete
      failed, site unread                             -> incomplete
      failed, at the statement, `fires_as` matches    -> intended_failure
      failed, at the statement, no `fires_as` match   -> incomplete  (the library's wording drifted)
      failed, read, outside the statement             -> wrong_location
      anything else / no row                          -> not_executed"""
    status = row.get("status")
    problem = failure_problem(row)
    shown = (str(problem.get("message") or "").strip() or text_head(problem.get("text"), entry)).strip()
    observed = {"status": status, "message_head": fold(shown.splitlines()[0] if shown else "", 300)}
    for key in ("frame", "location", "failure_kind", "site_unread"):
        if site.get(key):
            observed[key] = site[key]
    language = detail["language"]

    def answer(verdict, note="", location=None, reason=None, mismatches=(), cause=None):
        got = {"verdict": verdict, "actual_location": location, "actual_reason": reason,
               "mismatches": list(mismatches), "observed": observed, "note": note}
        if cause:    # only E15 names one (RN1-8): the other `incomplete` answers are the tool's gap, and the caller writes that
            got["cause"] = cause
        return got

    if status == "passed":
        prefix = builds_by_default(argv, entry)
        if among:
            return answer("incomplete", f"--at chose among {len(detail['candidates'])} declarations of the name and the "
                                        "inverted run passed: a pass does not say which body ran, so the check is not "
                                        "called dead (E5)")
        if entry["compiled"] and not prefix:
            return answer("incomplete", f"the {language} entry is compiled and the launcher `{launcher_words(argv)[:80]}` "
                                        "is not one that rebuilds by default "
                                        f"({', '.join(entry['builds_by_default']) or 'none listed'}): the inverted "
                                        "source may never have reached the build, and a pass then proves nothing (E14)")
        if entry["compiled"]:
            return answer("no_failure", f"the launcher builds by default (`{prefix}`)", mismatches=["the mutated assert never fired"])
        observed["residual"] = ("the entry is not compiled: a project that runs its compiled output through a wrapper "
                                "of its own would have run the author's build, not the mutated source (E14)")
        return answer("no_failure", mismatches=["the mutated assert never fired"])
    if status == "error":
        return answer("incomplete", f"the run's row is an error (an exception outside an assertion, a timeout or a "
                                    f"setup failure): {observed['message_head'] or 'no message'}; the inverted form did "
                                    "not get to assert, so nothing is said about the test")
    if status != "failed":
        return answer("not_executed", f"report status {status!r}", mismatches=[f"report status {status!r}"])
    if "site_unread" in site or not site.get("location"):
        return answer("incomplete", f"the failing row's site was not read ({site.get('reason') or 'no frame'}); the "
                                    f"frame grammar is assertion_probes.{language}.frames in references/detectors.json "
                                    "(the factory's data): a tooling gap, not a verdict on the test")
    line = site["location"].rpartition(":")[2]
    inside = site.get("failure_kind") == "assertion" and line.isdigit() \
        and detail["line"] <= int(line) <= detail["end_line"]
    if not inside:
        return answer("wrong_location", location=site["location"], reason=observed["message_head"] or None,
                      mismatches=["location"])
    if fires_on(row, entry, detail["fires_as"]):
        return answer("intended_failure")
    return answer("incomplete", f"the run failed at the mutated statement, but its message (`{observed['message_head'][:120]}`) "
                                f"does not match the failure this inverted form must show (assertion_probes.{language}, "
                                f"pair {detail.get('pair_id') or detail['pair']}): the library's wording differs from the "
                                "row's, so the row is the factory's to correct, and nothing is said about the test (E15)",
                  cause="data_row")   # the tool read the run; the factory's detector row did not know the text it produced (FR-3, FR-41)


# --- restore -----------------------------------------------------------------------------------

def put_back(path: Path, data: bytes, sha: str, atime_ns, mtime_ns) -> dict:
    """Write the author's bytes into `path` and prove it: the ONE restore, used by the probe's own
    `finally` and by the recovery of a dead probe's copy, so the two cannot drift.

    mtime (E20): a `.py` gets the mtime it had, and its module's bytecode caches are dropped so no
    rewritten bytecode of the mutated source outlives it; any other file gets "now" - an
    incremental build (MSBuild, Maven) that saw the old mtime on a file whose build output was made
    from the MUTATED bytes would call that output up to date, and the author's next ordinary run
    would then execute the mutation."""
    result = {"verified": False}
    try:
        path.write_bytes(data)
        if path.suffix == ".py" and mtime_ns is not None:
            os.utime(path, ns=(mtime_ns if atime_ns is None else atime_ns, mtime_ns))
        else:
            os.utime(path, None)
        result["verified"] = sha256(path.read_bytes()) == sha
        if path.suffix == ".py":
            dropped = []
            for cached in sorted_paths((path.parent / "__pycache__").glob(path.stem + ".*.pyc")):
                try:
                    cached.unlink()
                    dropped.append(cached.name)
                except OSError:
                    pass
            result["bytecode_dropped"] = dropped
    except OSError as exc:
        result["error"] = f"{type(exc).__name__}: {exc}"
    return result


def restore(path: Path, original: bytes, original_sha: str, stat, copy=None) -> dict:
    """Put the author's bytes back FROM THE COPY ON DISK when there is one, and prove it by sha256.

    The copy is the bytes a killed probe could still be put back from; `original` (the same bytes in
    this process's memory) is only the way back when the copy cannot be read or no longer matches the
    sha256 it was made with (writing a damaged copy over the author's file would lose what the probe
    still holds), and the result says which one it used (`restored_from`) - a restore that silently
    used memory would make the copy decoration."""
    data, source, why = original, "memory", ""
    if copy is not None:
        try:
            data, source = Path(copy).read_bytes(), "copy"
            if sha256(data) != original_sha:
                data, source, why = original, "memory", "the copy's sha256 differs from the original's"
        except OSError as exc:
            why = f"{type(exc).__name__}: {exc}"
    result = put_back(path, data, original_sha, stat.st_atime_ns, stat.st_mtime_ns)
    result["sha256"] = original_sha
    if copy is not None:
        result["restored_from"] = source
        if why:
            result["copy_unreadable"] = why
    return result


# --- the durable copy, the lock and the recovery (R9) ----------------------------------------------
# The shape of the failure: the probe holds the author's original bytes in memory, mutates the file,
# and runs for up to RUN_TIMEOUT_S (31 minutes). A role's shell call is killed long before that, and a
# killed process never reaches its `finally`: the author's file stayed mutated and the only copy of the
# original died with the process. So the bytes go to disk BEFORE the mutation, keyed per file (a
# `conftest.py` exists in many folders, so a name is no key), under one lock per file that process
# death releases, and the next probe restores what a dead one left BEFORE it reads a single byte as
# "the author's".

COPY_DIR = "probe-copies"
FALLBACK_GRACE_S = 120
# The convention of `event_store.lock`: an OSError from the non-blocking lock call IS how a HELD lock
# reports itself (msvcrt LK_NBLCK: EACCES; fcntl.flock: EAGAIN/EWOULDBLOCK, EACCES on some systems).
HELD_ERRNOS = frozenset({errno.EACCES, errno.EAGAIN, errno.EWOULDBLOCK, errno.EDEADLK})
META_FIELDS = ("path", "original_sha", "mutated_sha", "original_mtime_ns", "started_at", "timeout_s",
               "statement_before", "statement_after", "line")
_KEY = re.compile(r"^[0-9a-f]{16}$")


def copy_dir(root: Path) -> Path:
    """The project's `state/probe-copies/`: one folder for every story, because a probe killed in
    story A must be visible to the probe of story B. Resolved through `runtime_paths` (FR-37), never
    spelled by hand."""
    return runtime_paths.state_file(root, COPY_DIR)


def copy_key(path: Path, root: Path) -> tuple:
    """(key, project-relative POSIX path): the key is the first 16 hex of sha256 of that path, case-
    folded on Windows where `Tests/A.py` and `tests/a.py` are one file."""
    shown = _rel_project(Path(path), Path(root))
    folded = shown.casefold() if os.name == "nt" else shown
    return sha256(folded.encode("utf-8"))[:16], shown


def copy_files(directory: Path, key: str) -> tuple:
    """(`<k>.orig`, `<k>.meta`). `.meta` is JSON content under a name that is deliberately not
    `.json`: the story folders' json scans (exit_gate, finalize_task, handoff_check, probe_debt) must
    not read it as one of theirs."""
    return directory / f"{key}.orig", directory / f"{key}.meta"


def _os_lock(handle) -> None:
    """One non-blocking exclusive lock on the first byte. Raises OSError when it is held, ImportError
    when the platform module is missing."""
    handle.seek(0)
    if os.name == "nt":
        import msvcrt
        msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
    else:
        import fcntl
        fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)


def _os_unlock(handle) -> None:
    try:
        handle.seek(0)
        if os.name == "nt":
            import msvcrt
            msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
        else:
            import fcntl
            fcntl.flock(handle, fcntl.LOCK_UN)
    except (ImportError, OSError):
        pass  # closing the handle releases it anyway


def try_lock(directory: Path, key: str) -> tuple:
    """("locked", handle) | ("held", None) | ("broken", None).

    "held" is ONLY an OSError whose errno says the lock is taken (`HELD_ERRNOS`); any other errno, an
    ImportError, or a lock file that cannot be made means the PRIMITIVE failed ("broken"), and only
    then does the fallback deadline apply (a lock reported as broken when it was merely held would
    let a second probe take a live probe's mutated bytes for the original). The lock file is only
    ever opened, never deleted or truncated (event_store.lock)."""
    try:
        directory.mkdir(parents=True, exist_ok=True)
        handle = (directory / f"{key}.lock").open("a+b")
    except OSError:
        return "broken", None
    try:
        handle.seek(0, 2)
        if not handle.tell():
            handle.write(b"0")
            handle.flush()
        _os_lock(handle)
    except ImportError:
        handle.close()
        return "broken", None
    except OSError as exc:
        handle.close()
        return ("held" if exc.errno in HELD_ERRNOS else "broken"), None
    return "locked", handle


def release_locks(locks: list) -> None:
    while locks:
        handle = locks.pop()
        _os_unlock(handle)
        try:
            handle.close()
        except OSError:
            pass


def read_meta(meta_path: Path) -> tuple:
    """(meta dict, "") or (None, why). Never raises: a copy record that cannot be read is a state to
    report, not a crash (P1)."""
    try:
        data = json.loads(meta_path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return None, f"its record {meta_path.name} cannot be read ({type(exc).__name__})"
    if not isinstance(data, dict):
        return None, f"its record {meta_path.name} is not a JSON object"
    missing = [k for k in META_FIELDS if k not in data]
    if missing:
        return None, f"its record {meta_path.name} lacks {', '.join(missing)}"
    return data, ""


def copy_deadline(meta) -> "datetime | None":
    """`started_at + timeout_s + FALLBACK_GRACE_S`: when a probe that holds no OS lock must be dead."""
    try:
        started = datetime.fromisoformat(str(meta["started_at"]))
        if started.tzinfo is None:
            started = started.replace(tzinfo=timezone.utc)
        return started + timedelta(seconds=float(meta["timeout_s"]) + FALLBACK_GRACE_S)
    except (KeyError, TypeError, ValueError, OverflowError):
        return None


def _meta_target(root: Path, meta: dict) -> Path:
    path = Path(str(meta["path"]))
    return path if path.is_absolute() else Path(root) / path


def _door(shown: str) -> str:
    return f"probe_by_code.py --release-copy {shown}"


def _unresolved_text(shown: str, why: str, meta, current_sha, orig: Path) -> str:
    """What a copy that cannot be applied says (E19): the file, the shas, the copy, the line, the
    door. The addressee is the test's AUTHOR through a tooling finding - the critic never edits test
    code (FR-2) - and the author's newer edit always wins."""
    parts = [f"a probe that was killed left a byte copy of {shown} ({orig}) that cannot be applied: {why}."]
    if meta:
        parts.append(f"The file holds sha256 {current_sha or 'unreadable'}; the probe's mutated version was "
                     f"{meta['mutated_sha']}, the original {meta['original_sha']}.")
        parts.append(f"If line {meta['line']} still reads `{meta['statement_after']}`, the probe's mutation is "
                     f"still in the file: put back `{meta['statement_before']}`, or copy {orig} over the file "
                     "if nothing else changed there.")
    parts.append(f"Once that is settled, `{_door(shown)}` drops the copy. Nothing was overwritten.")
    return " ".join(parts)


def settle(root: Path, key: str, *, fallback_deadline_needed: bool = False, shown_hint: str = "") -> tuple:
    """Deal with the copy of a probe that is NOT running. -> (state, text), state one of `none` (no
    copy), `dropped` (the file already holds the original: only the copy goes), `recovered` (the file
    held the mutated bytes and the original is back, verified; `text` is the note) or `unresolved`
    (`text` says why; nothing was overwritten).

    Anything the copy does not explain - the author edited the file after the crash, deleted it, or
    the copy itself no longer matches its own sha - is left alone: the author's newer edit wins and
    the way out is `--release-copy` (FR-57)."""
    directory = copy_dir(root)
    orig, meta_path = copy_files(directory, key)
    if not meta_path.is_file():
        return "none", ""  # an orphan `.orig`: the probe died before its record, and nothing was mutated yet
    meta, why = read_meta(meta_path)
    if meta is None:
        # The record is unreadable, so the file it was about is unknown unless the caller knows it (its
        # own test or oracle): the door then takes the 16-hex key, which is the copy's own name.
        return "unresolved", _unresolved_text(shown_hint or key, why, None, None, orig)
    shown = str(meta["path"])
    if fallback_deadline_needed and copy_deadline(meta) is None:
        return "unresolved", _unresolved_text(shown, "the OS lock cannot say whether that probe is alive and its "
                                              "record has no readable started_at / timeout_s", meta, None, orig)
    target = _meta_target(root, meta)
    try:
        current = target.read_bytes()
    except OSError as exc:
        return "unresolved", _unresolved_text(shown, f"the file cannot be read now ({type(exc).__name__})",
                                              meta, None, orig)
    current_sha = sha256(current)
    if current_sha == meta["original_sha"]:
        for stale in (meta_path, orig):
            stale.unlink(missing_ok=True)
        return "dropped", ""
    if current_sha != meta["mutated_sha"]:
        return "unresolved", _unresolved_text(shown, "the file was changed after the probe's mutation (its "
                                              "sha256 is neither the mutated nor the original one)",
                                              meta, current_sha, orig)
    try:
        data = orig.read_bytes()
    except OSError as exc:
        return "unresolved", _unresolved_text(shown, f"the copy cannot be read ({type(exc).__name__})",
                                              meta, current_sha, orig)
    if sha256(data) != meta["original_sha"]:
        return "unresolved", _unresolved_text(shown, "the copy's own bytes no longer match the sha256 its record "
                                              "gives, so it is not written over the file", meta, current_sha, orig)
    mtime = meta.get("original_mtime_ns")
    done = put_back(target, data, meta["original_sha"], None, mtime if isinstance(mtime, int) else None)
    if not done["verified"]:
        return "unresolved", _unresolved_text(shown, "the recovery was written but could not be verified"
                                              + (f" ({done['error']})" if done.get("error") else ""),
                                              meta, current_sha, orig)
    for stale in (meta_path, orig):
        stale.unlink(missing_ok=True)
    return "recovered", (f"recovered {shown}: a probe that was killed before it restored left line {meta['line']} "
                         f"reading `{meta['statement_after']}`; its byte copy put the author's bytes back "
                         f"(sha256 {meta['original_sha']}, verified) and was deleted")


def claim_key(root: Path, key: str, shown: str, *, own: bool, notes: list, now=None):
    """Take the lock of one file, settling the copy a dead probe left there first. -> the lock handle
    (None when the primitive failed: the fallback deadline then stands in for it).

    `own` = this probe's own test or oracle: a probe running there, or a copy that cannot be applied,
    is a refusal (exit 2, nothing changed). For any OTHER file it is a note and the probe goes on - a
    stale copy of file X left in story A must not stop story B's probe of file Y (P1: code reports,
    it does not stop the factory)."""
    now = now or datetime.now(timezone.utc)
    directory = copy_dir(root)
    meta_path = copy_files(directory, key)[1]
    state, handle = try_lock(directory, key)

    def blocked(until):
        if handle is not None:
            release_locks([handle])
        if not own:
            return None
        raise Refusal(f"probe_by_code: a probe of {shown} is running"
                      + (f" until {until.isoformat(timespec='seconds')}" if until else "")
                      + " - it holds the copy of that file, and the lock ends with the probe (a killed one "
                        "releases it). Probe again when it has ended. Nothing was changed.")

    if state == "held":
        return blocked(None)
    broken = state == "broken"
    if broken and meta_path.is_file():
        meta, _why = read_meta(meta_path)
        until = copy_deadline(meta) if meta else None
        if until is not None and until >= now:
            return blocked(until)
    try:
        outcome, text = settle(root, key, fallback_deadline_needed=broken, shown_hint=shown if own else "")
    except Exception as exc:  # the copy is examined, never trusted to be well formed
        outcome, text = "unresolved", _unresolved_text(
            shown, f"it could not be examined ({type(exc).__name__}: {str(exc)[:160]})", None, None,
            copy_files(directory, key)[0])
    if outcome == "unresolved" and own:
        if handle is not None:
            release_locks([handle])
        raise Refusal("probe_by_code: " + text + " This is a tooling finding to return to the test's author, "
                      "not an edit for the critic to make. Nothing was changed.")
    if outcome in ("recovered", "unresolved"):
        notes.append(text)
    if not own and handle is not None:
        release_locks([handle])
        return None
    return handle


def scan_copies(root: Path, *, skip_keys, notes: list, now=None) -> None:
    """R9 step 1: every copy in the folder whose probe is not running is settled - the OTHER files'
    first; this probe's own file goes through `claim_key`. Reads no byte of any project file that
    does not have a copy; makes nothing when there is no folder."""
    directory = copy_dir(root)
    if not directory.is_dir():
        return
    for meta_path in sorted_paths(directory.glob("*.meta")):
        key = meta_path.stem
        if key in skip_keys or not _KEY.match(key):
            continue
        claim_key(root, key, key, own=False, notes=notes, now=now)


def begin_copy(root: Path, path: Path, original: bytes, original_sha: str, stat, mutated_sha: str,
               detail: dict, timeout: int) -> dict:
    """R9 write order 1-2: `.orig`, then `.meta`, then the copy read back and its sha checked. The file
    is NOT mutated yet, so a copy that cannot be written and verified is a refusal with nothing
    changed (invariant: never a mutation without a verified copy on disk)."""
    key, shown = copy_key(path, root)
    directory = copy_dir(root)
    orig, meta = copy_files(directory, key)
    try:
        directory.mkdir(parents=True, exist_ok=True)
        orig.write_bytes(original)  # `.orig` first: a record always has its copy behind it
        atomic_json(meta, {
            "path": shown, "original_sha": original_sha, "mutated_sha": mutated_sha,
            "original_mtime_ns": stat.st_mtime_ns,
            "started_at": datetime.now(timezone.utc).isoformat(timespec="seconds"), "timeout_s": timeout,
            "statement_before": detail.get("statement_before"), "statement_after": detail.get("statement_after"),
            "line": detail.get("line")})
        if sha256(orig.read_bytes()) != original_sha:
            raise OSError("the copy read back does not match the original's sha256")
    except OSError as exc:
        for stale in (meta, orig):
            try:
                stale.unlink(missing_ok=True)
            except OSError:  # the folder is a file or unwritable: `missing_ok` swallows only ENOENT, and Linux
                pass  # answers ENOTDIR under a file (Windows: ENOENT); nothing of ours is there to remove
        raise Refusal(f"probe_by_code: the byte copy of {shown} could not be written and verified under {directory} "
                      f"({type(exc).__name__}: {exc}) - the file is not mutated without one. Fix the folder "
                      "(space, permissions) and probe again. Nothing was changed.") from exc
    return {"orig": orig, "meta": meta, "key": key, "path": shown}


def finish_copy(copy: dict, result: dict, root: Path) -> None:
    """R9 write order 6-7: the copy goes only after the restore is VERIFIED; otherwise both files stay
    (the recovery and the stderr line need them)."""
    result["copy"] = _rel_project(copy["orig"], root)
    if result.get("verified"):
        for stale in (copy["meta"], copy["orig"]):
            stale.unlink(missing_ok=True)
        result["copy_kept"] = False
    else:
        result["copy_kept"] = True


def release_copy(root: Path, file: str, now=None) -> dict:
    """`--release-copy <file>`: take the file's lock, print the copy's record, delete `.orig` and
    `.meta`. Nothing else runs. A held lock (a probe running there) refuses - the author's edit is the
    reason for a release, never a probe's live copy."""
    now = now or datetime.now(timezone.utc)
    if _KEY.match(str(file)):  # a copy whose record is unreadable names no file: its own name is the door
        key, shown = str(file), str(file)
    else:
        target = Path(file)
        target = target if target.is_absolute() else Path(root) / target
        key, shown = copy_key(target, root)
    directory = copy_dir(root)
    orig, meta_path = copy_files(directory, key)
    if not (orig.exists() or meta_path.exists()):
        return {"status": "no_copy", "file": shown,
                "message": f"no byte copy of {shown} is held under {directory}: nothing to release"}
    state, handle = try_lock(directory, key)
    try:
        meta, why = read_meta(meta_path) if meta_path.exists() else (None, "it has no record file")
        until = copy_deadline(meta) if meta else None
        if state == "held" or (state == "broken" and until is not None and until >= now):
            raise Refusal(f"probe_by_code: a probe of {shown} is running"
                          + (f" until {until.isoformat(timespec='seconds')}" if until else "")
                          + " - its copy is not released while it runs. Release it again once that probe has "
                            "ended (a killed probe frees the lock). Nothing was changed.")
        for stale in (meta_path, orig):
            stale.unlink(missing_ok=True)
    finally:
        release_locks([handle] if handle is not None else [])
    return {"status": "released", "file": shown, "copy": _rel_project(orig, root),
            "record": meta if meta else {"unreadable": why}}


# --- binding to the author's bytes -----------------------------------------------------------

def _rel_root(path: Path, root: Path, run_cwd: Path) -> str:
    """The mutated file as the report will name it: relative to the run directory when it
    lies under it, else to the project root."""
    for base in (run_cwd, root):
        try:
            return path.resolve().relative_to(base.resolve()).as_posix()
        except ValueError:
            continue
    return path.as_posix()


def _rel_project(path: Path, root: Path) -> str:
    """The mutated file relative to the project root, POSIX - the one spelling `already_probed`
    resolves it from later, whatever directory the run itself was made in."""
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def _rel_task(path: str, root: Path, task_root: Path) -> str:
    candidate = Path(path)
    candidate = candidate if candidate.is_absolute() else root / candidate
    try:
        return candidate.resolve().relative_to(task_root.resolve()).as_posix()
    except ValueError:
        return str(path).replace("\\", "/")


def original_input_hash(request: dict, mutated_path: Path, mutated_sha: str, original_sha: str) -> str:
    """`test_content_sha` as `execution_fingerprint.build` computes it — the same records in
    the same order, with this file's mutated sha replaced by the author's."""
    records = request.get("fingerprint_files") or []
    groups = {}
    for record in records:
        if not isinstance(record, dict) or record.get("kind") not in ("test_files", "helper_files"):
            continue
        row = dict(record)
        if row.get("sha256") == mutated_sha and Path(str(row.get("path"))).resolve() == mutated_path.resolve():
            row["sha256"] = original_sha
        groups.setdefault(record["kind"], []).append(row)
    ordered = (sorted(groups.get("test_files", []), key=lambda x: x["path"])
               + sorted(groups.get("helper_files", []), key=lambda x: x["path"]))
    return content_hash(ordered) if ordered else original_sha


def _helper_chain(path: Path, run_cwd: Path) -> list:
    """The conftest chain of a test file, nearest first, up to the run directory: where `find_oracle`
    looks for a helper or fixture that asserts. It is NOT the test's identity: that list is the run's
    own (the other test files and the helpers earlier runs declared), and the identity is measured
    by `proof_level.instance_identity`, from the author's request."""
    helpers, directory = [], path.resolve().parent
    while directory == run_cwd or directory.is_relative_to(run_cwd):
        candidate = directory / "conftest.py"
        if candidate.is_file():
            helpers.append(str(candidate))
        if directory == run_cwd:
            break
        directory = directory.parent
    return helpers


def author_binding(task_root: Path, instance_id: str, function_sha: str) -> dict | None:
    """The latest author run block whose row for this instance ran exactly this function
    (`instance_content_sha` equal): its `test_content_sha` is the hash the window carries.
    An empty sha binds nothing: two unmeasured tests are not "the same function".

    "Latest" is the story's ONE block order (`run_history.read_run_blocks`: the block's own clock, a
    reparse right after the block it supersedes), not file-name order, which puts a reparse of an
    attempt whose id starts with a low digit before every `2026...` block (t-149, F-order)."""
    if not function_sha:
        return None
    import run_history
    blocks, _unreadable = run_history.read_run_blocks(task_root)
    for item in reversed(blocks):
        block = item["data"]
        for row in block.get("results") or []:
            if (isinstance(row, dict) and row.get("instance_id") == instance_id
                    and row.get("instance_content_sha") == function_sha
                    and (row.get("source_fingerprint") or {}).get("test_content_sha")):
                return {"run_block": "work/run-blocks/" + item["name"],
                        "test_content_sha": row["source_fingerprint"]["test_content_sha"],
                        "dispatch_id": block.get("dispatch_id"), "status": row.get("status")}
    return None


# --- main ----------------------------------------------------------------------------------------

WINDOW_PROBE_FIELDS = ("verdict", "input_hash", "expected_location", "actual_location", "expected_reason",
                       "actual_reason", "failure_kind", "mutation_kind", "proof_level", "obligation_ids",
                       "obligation_hash", "defect_location", "assertion_id", "evidence_ref")


def window_probe(record: dict) -> dict:
    """The `probe` object of the window instance, exactly as `acceptance.validate_window`
    reads it — the critic copies this, never retypes it."""
    return {key: record.get(key) for key in WINDOW_PROBE_FIELDS}


def record_path(task_root: Path, instance_id: str) -> Path:
    """The probe's own record. The naming lives in `proof_level.probe_record_path`, where
    `already_probed` (which reads it back) and `red_sandbox.py` (which writes the product record beside
    it) find it too: one naming, three users."""
    return proof_level.probe_record_path(task_root, instance_id)


# --- the live receipt ----------------------------------------------------------------------------

RECEIPT_DIR = "work/sensitivity-receipts"
FACT_KEYS = ("case_version", "test_content_hash", "source_revision", "build_id")


def _receipt_core(record: dict, iid: str, facts: dict, restoration: str) -> dict:
    """Everything a live receipt says except the run evidence and its own hash."""
    core = {
        "instance_id": iid, **{key: facts[key] for key in FACT_KEYS},
        "mutation": record["mutation"], "expected_assertion_failure": record["expected_reason"],
        "actual_failure": record["actual_reason"], "assertion_location": record["expected_location"],
        "restoration_evidence": restoration, "failure_kind": record["failure_kind"],
        "proof_level": proof_level.LIVE, "probe_tool": "probe_by_code.py",
        "mutation_kind": MUTATION_KIND, "probe_record": record["record"],
        "obligation_ids": list(record.get("obligation_ids") or []),
        "obligation_hash": record.get("obligation_hash"),
        "defect_location": record.get("defect_location"), "assertion_id": record.get("assertion_id"),
        "immutable": True}
    if record.get("obligation_refs"):
        core["obligation_refs"] = record["obligation_refs"]
    if record.get("test_code_sha"):
        # What can execute in the measured bytes (diff_scope.executable_sha): the receipt still
        # counts after a comment-only edit of its test. Absent for bytes that are not UTF-8 - then
        # only raw equality holds (D-0017, the safe direction).
        core["test_code_sha"] = record["test_code_sha"]
    if record.get("mutated_file"):
        # What this probe mutated travels with the receipt, not only with the record that the next probe
        # overwrites: a repeat is answered by the receipt only while that file still holds these bytes.
        core["mutated_file"] = record["mutated_file"]
    if record.get("instance_identity"):
        # The per-test identity measured BEFORE the mutation, over the same bytes as the raw sha above
        # (the receipt is written only when that raw sha equals what the manifest binds): a neighbour's
        # edit, or a comment, keeps this receipt (D5). Absent when the test had no measurable identity.
        core["instance_identity"] = record["instance_identity"]
    return core


def _hash_of(receipt: dict) -> str:
    """The receipt's identity: everything but itself and the run evidence. The evidence (a job
    summary, a junit file with its timings) differs on EVERY run, so a hash that covered it would
    make a rerun on the same bytes a new receipt each time; what the receipt proves is the same."""
    return content_hash({k: v for k, v in receipt.items() if k not in ("receipt_hash", "evidence_refs")})


def write_receipt(task_root: Path, receipt: dict, instance_id: str) -> tuple:
    """(`{path, sha256}` or None, note). The receipt is IMMUTABLE: written once, never over
    another. Same facts again -> the file already there (same path, same bytes); a different file
    under this very name -> nothing is overwritten and the note says so."""
    receipt = dict(receipt)
    receipt["receipt_hash"] = _hash_of(receipt)
    directory = Path(task_root) / RECEIPT_DIR
    path = directory / f"{C.instance_file_stem(instance_id)}-live-{receipt['receipt_hash'][:16]}.json"
    rel = path.relative_to(task_root).as_posix()
    try:
        if path.exists():
            try:
                found = json.loads(path.read_text(encoding="utf-8"))
            except ValueError:
                found = None
            if not (isinstance(found, dict) and found.get("receipt_hash") == receipt["receipt_hash"]
                    and _hash_of(found) == receipt["receipt_hash"]):
                return None, (f"{rel} already exists with different content; an immutable receipt is "
                              "never overwritten, so no live receipt was written")
            return {"path": rel, "sha256": sha256(path.read_bytes())}, f"{rel} already holds this proof"
        # `atomic_json` names its scratch file `<name>.<32 hex>.tmp`, 37 characters on top of a
        # name that is already 156 for the longest stem `contract.instance_file_stem` allows: on a
        # Windows path limited to 260 that one file failed for a long id while the receipt itself
        # would have fitted. The scratch file here has a short name of its own; the receipt is put
        # in place by one rename, so nobody ever reads it half written.
        directory.mkdir(parents=True, exist_ok=True)
        scratch = directory / (uuid.uuid4().hex[:8] + ".tmp")
        try:
            scratch.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            os.replace(scratch, path)
        finally:
            scratch.unlink(missing_ok=True)
        return {"path": rel, "sha256": sha256(path.read_bytes())}, ""
    except OSError as exc:
        return None, f"the live receipt could not be written ({type(exc).__name__}: {exc})"


def attach_receipt(record: dict, entry: dict, task_root: Path) -> None:
    """Write the live receipt of an `intended_failure` whose restore was verified, and say in the
    record what happened — the receipt, or every fact that was missing for it."""
    record["receipt"], record["receipt_missing"] = None, []
    iid = C.test_instance_id(entry) or record["instance_id"]
    try:
        facts = proof_level.binding_facts(task_root, iid)
    except Exception as exc:  # the record says why there is no receipt; it never crashes the probe
        facts = {}
        record["notes"].append(f"no live receipt: the binding facts could not be read "
                               f"({type(exc).__name__}: {exc})")
    missing = [key for key in FACT_KEYS if not facts.get(key)]
    # The receipt claims the bytes the manifest binds; this probe MEASURED the test file it ran,
    # before mutating anything (`test_file_sha256`, the raw sha256 of the file). A claim nobody
    # compared with the measurement makes the window's byte check circular (the window reads the
    # hash from the receipt), so a receipt is written only when the two agree. Both sides are the
    # raw file hash: `input_hash` is the run's fingerprint over the test AND helper files, a
    # different quantity, and comparing it refused every row of TP1-13797 (driver3) whose
    # binding was right (critic t-035). The door: the manifest's trace_binding is stale.
    measured = str(record.get("test_file_sha256") or "")
    stale = bool(facts.get("test_content_hash")) and bool(measured) and measured != facts["test_content_hash"]
    if stale:
        missing.append("test_content_hash")
        record["notes"].append(
            f"no live receipt: the test file this probe measured (sha256 {measured}) is not the bytes the "
            f"manifest binds (trace_binding.test_content_sha {facts['test_content_hash']}) - the "
            "manifest's trace_binding is stale. It is the author's to rebind, through `manifest_put.py` "
            "(no run needed): trace_binding.test_content_sha is the sha256 of the file's bytes, as "
            "manifest_from_tests.py writes it - never a run block's source_fingerprint.test_content_sha, "
            "which is a fingerprint over several files; then the critic probes again")
        record["receipt_missing"] = missing
        return
    if missing:
        record["receipt_missing"] = missing
        record["notes"].append(
            "no live receipt: the manifest and run blocks carry no " + ", ".join(missing)
            + " for this instance — the author's record, not yours to type: the case version and "
              "test bytes belong in the instance's tests[] row (case_version_links, "
              "trace_binding.test_content_sha), the source and build identity in the run block "
              "that executed it")
        return
    shown = (record.get("mutation_detail") or {}).get("file") or record["test_node"].split("::")[0]
    restoration = f"probe_by_code: {shown} sha256 {record['restore']['sha256']} verified restored"
    receipt = _receipt_core(record, iid, facts, restoration)
    receipt["evidence_refs"] = list(record.get("evidence_refs") or [])
    ref, note = write_receipt(task_root, receipt, iid)
    if note:
        record["notes"].append(note)
    record["receipt"] = ref


def _judge_run(root: Path, task_root: Path, record: dict, summary: dict, spec: dict, detail: dict, request: dict,
               oracle_path: Path, keys: list, *, judge_row: Callable = None) -> None:
    """What the run's summary and its report say, written into the record: the evidence, then the verdict
    (Python: pytest's own traceback; any other language: the R8 table over the bound row and the entry's
    frame grammar)."""
    judge_row = judge_row or _judge_row     # the Python branch's row judge; the alternative probe injects its own (TQ1-25)
    notes = record["notes"]
    record["run"] = {k: summary.get(k) for k in ("label", "exit_code", "execution_status",
                                                 "error_head", "stand_signal") if k in summary}
    evidence = []
    for candidate in (summary.get("summary_path"), (summary.get("report_evidence") or {}).get("path")):
        if not candidate:
            continue
        for base in (root, task_root):
            file = (base / str(candidate))
            if file.is_file():
                rel = _rel_task(str(file), root, task_root)
                if rel not in [e["path"] for e in evidence]:
                    evidence.append({"path": rel, "sha256": sha256(file.read_bytes())})
                break
    record["evidence_refs"] = evidence
    record["evidence_ref"] = evidence[0]["path"] if evidence else None
    report = (summary.get("report_evidence") or {}).get("path")
    # The run says which reporter wrote the report; a summary that names none is
    # what every summary was before it did, and was always read as JUnit.
    reporter = str(summary.get("reporter") or "").strip() or DEFAULT_REPORTER
    detector = bool(spec.get("language"))
    rows = []
    report_read = False     # a report that was read: only then is "no row of it is this test" a fact about the tool, not the stand
    if report and (task_root / report).is_file():
        try:
            rows = report_rows(task_root / report, reporter, raw=detector)
            report_read = True
        except ET.ParseError as exc:
            notes.append(f"the report is not valid XML: {exc}")
        except ValueError as exc:  # a reporter the reader does not know: no rows, said why
            notes.append(f"the run's report was not read (its summary names the reporter): {exc}")
    else:
        notes.append("no report evidence: " + str(summary.get("error_head") or
                                                   summary.get("no_junitxml") or
                                                   summary.get("execution_status") or "unknown cause"))
    if detector:
        _judge_detector_rows(root, record, rows, reporter, spec, detail, request, oracle_path, keys, report_read)
        return
    matches = matching_rows(rows, spec["node"])
    if len(matches) == 1:
        judge_row(record, matches[0], spec, detail)
        if _tail(matches[0]["test_id"]) != _tail(spec["node"]):
            record["matched_report_id"] = matches[0]["test_id"]
    elif matches:
        _judge_param_rows(record, matches, spec, detail, judge_row=judge_row)
    elif rows:
        notes.append(f"no report row is named {_tail(spec['node'])!r}; the report held {held_ids(rows)}")


# Which verdict speaks for a node whose several parametrised rows disagree: the one that says the most
# about a test that did NOT kill the mutation. A mutated assert that never fired outranks a failure at the
# wrong place, and BOTH are judged verdicts that outrank a row that did not run: `not_executed` as the
# headline would let `keep_standing_record` keep an old `intended_failure` over a row that was judged and
# survived (B1, t-1482).
_SURVIVOR_ORDER = ("no_failure", "wrong_location", "not_executed")


def _judge_row(record: dict, row: dict, spec: dict, detail: dict) -> None:
    observed = observe(row, spec, detail)
    record["observed"] = observed
    verdict, actual_location, actual_reason, mismatches = verdict_of(observed, spec, detail)
    record.update(verdict=verdict, actual_location=actual_location,
                  actual_reason=actual_reason, failure_kind=observed.get("failure_kind"))
    if mismatches:
        record["mismatches"] = mismatches


def _judge_param_rows(record: dict, rows: list, spec: dict, detail: dict, *, judge_row: Callable = None) -> None:
    """Several rows `func[p1]`, `func[p2]` stand for one requested node: every row is judged, the verdict is
    `intended_failure` only if EVERY row is, otherwise the surviving rows are named in the record and in a
    note (a row never picked silently: the mutated assert must fire for each parameter)."""
    judged = []
    for row in rows:
        probe: dict = {}
        (judge_row or _judge_row)(probe, row, spec, detail)
        judged.append((row, probe))
    _worst_of_rows(judged, spec, record)


def _worst_of_rows(judged: list, spec: dict, record: dict) -> dict:
    """The ONE aggregator of several judged report rows of one requested test (AR-15; a parametrised Python node and a
    templated or looped test of another language both come here). `judged` is [(report row, its judged fields)], never empty
    (a caller with no row has nothing to judge and says so before it comes here). The verdict is `intended_failure` only if
    EVERY row is; otherwise the survivors are named in `param_rows` and in a note, and the survivor that says the most speaks
    (`_SURVIVOR_ORDER`). The error is allowed only toward NOT `intended_failure` (a row never picked silently: the mutated
    assert must fire for each). Returns the fields that were copied into the record."""
    survivors = [(row, probe) for row, probe in judged if probe["verdict"] != "intended_failure"]
    if len(judged) > 1:     # one row is the plain case: no `param_rows`, no note (as every single-row record always was)
        record["param_rows"] = [{"test_id": row["test_id"], "verdict": probe["verdict"]} for row, probe in judged]
    if len(judged) == 1 or not survivors:
        first = judged[0][1]
    else:
        first = next((p for v in _SURVIVOR_ORDER for _r, p in survivors if p["verdict"] == v), survivors[0][1])
        names = ", ".join(repr(row["test_id"]) for row, _p in survivors)
        record["notes"].append(f"{len(judged)} report rows are named {_tail(spec['node'])!r}[...]; the mutation "
                               f"survived in {len(survivors)}: {names}")
    for key in ("observed", "verdict", "actual_location", "actual_reason", "failure_kind", "mismatches"):
        if key in first:
            record[key] = first[key]
    return first


def _tooling_gap(record: dict, detail: dict) -> None:
    """The record says the TOOL could not judge: the language and `cause: tooling` (the module docstring's `incomplete` and
    an unbound report row). The reader is `proof_level.tooling_gap_key`, which takes the class word only from a record that says
    this and nothing else (a stand that did not run writes no cause)."""
    record["language"], record["cause"] = detail["language"], "tooling"


def _judge_detector_rows(root: Path, record: dict, rows: list, reporter: str, spec: dict, detail: dict,
                         request: dict, oracle_path: Path, keys: list, report_read: bool = True) -> None:
    """R7, R8: the rows of THIS instance are the ones the request's `report_test_id` names for it. A contract with a `file`
    (the code built the selection, or the role's own id is judged by the same table, EP1-37) is read by
    `red_sandbox.selection_rows`: one row, or several of ONE file (a templated or looped test, or a run of several projects),
    each judged and the worst speaks (`_worst_of_rows`); a contract without a file is bound by `red_sandbox.bind_row` as before.
    No row, rows of different files, or no binding leaves the record `not_executed` with the reason BEFORE any aggregate (a
    verdict of "nothing" is none), and says it is the tool that could not bind (`cause: tooling`) - only when the report HELD
    rows (`rows` empty: a stand that wrote an empty report, or none, did not run the suite, and nothing is said about the tool;
    `report_read` is a parameter of the caller's, the rows are the fact, F-1 of t-596). Then the frame of each failed row is
    read with the entry's grammar. `among` is true only for a `--at` that chose among several candidates (E5, M-4)."""
    import red_sandbox
    entry, notes = spec["entry"], record["notes"]
    contracts = request.get("instance_contracts") or {}
    key = next((k for k in keys if k in contracts), keys[0])
    own = contracts.get(key)
    if isinstance(own, dict) and own.get("file"):
        matched = red_sandbox.selection_rows(rows, own)
        if not matched:
            if report_read and rows:
                _tooling_gap(record, detail)
            notes.append(f"no row of the {reporter} report is the test the request selected for {key} "
                         f"({own.get('report_test_id')!r} in {own.get('file')}); the report held {held_ids(rows)}")
            return
        if len(matched) > 1 and not (own.get("report_match") or own.get("classname_match")):
            # a hand-written id names ONE row: several are ambiguous (`bind_row`'s text). Only a selection the CODE built
            # (a pattern, or the file-suffix rule of the run form) can be several rows of one test
            row, why = red_sandbox.bind_row({"instance_id": key}, contracts, rows, reporter, record["task"], pytest_command=False)
            _tooling_gap(record, detail)
            notes.append(why or f"{len(matched)} rows of the {reporter} report are named {own.get('report_test_id')!r}; ambiguous")
            return
        if red_sandbox.classnames_differ(matched):
            _tooling_gap(record, detail)
            notes.append(f"{len(matched)} rows of the {reporter} report are named like {own.get('report_test_id')!r} but belong "
                         "to different files, so which test ran cannot be told; nothing is said about the test")
            return
    else:
        row, why = red_sandbox.bind_row({"instance_id": key}, contracts, rows, reporter, record["task"], pytest_command=False)
        if row is None:
            if report_read and rows:
                _tooling_gap(record, detail)
            notes.append(why or "no row of the report could be bound to this instance")
            return
        matched = [row]
    frames, skip, frame_path = AD.grammar_of(entry)
    among = len(detail["candidates"]) > 1 and detail.get("at") is not None
    argv = (request.get("command") or {}).get("argv")
    judged, row_notes = [], {}
    for row in matched:
        if reporter in ("trx", "junit-xml"):
            site = reporters.assertion_site(row, reporter, root, oracle_path, pytest_command=False,
                                            runtime=detail["language"], frames=frames, skip_frames=skip,
                                            frame_path=frame_path)
        else:
            site = {"site_unread": f"{reporter}/{detail['language']}",
                    "reason": f"the run's reporter is {reporter!r}; stack frames are read only from trx and junit-xml"}
        result = judge_detector(row, site, entry, detail, among=among, argv=argv)
        fields = {"observed": result["observed"], "verdict": result["verdict"],
                  "actual_location": result["actual_location"], "actual_reason": result["actual_reason"],
                  "failure_kind": site.get("failure_kind")}
        if result.get("cause"):
            fields["cause"] = result["cause"]
        if result["verdict"] == "intended_failure":
            fields.update(actual_location=record["expected_location"], actual_reason=record["expected_reason"],
                          failure_kind="assertion")
        if result["mismatches"]:
            fields["mismatches"] = result["mismatches"]
        judged.append((row, fields))
        row_notes[id(fields)] = result["note"]
    first = _worst_of_rows(judged, spec, record)
    if record.get("verdict") == "incomplete":   # the module docstring's gap of the factory (a frame it cannot resolve, a launcher that may not rebuild): the tool's
        incomplete = [f for _r, f in judged if f["verdict"] == "incomplete"]   # ALL of them decide: one tooling gap among data rows is still a gap
        if incomplete and all(f.get("cause") == "data_row" for f in incomplete):   # E15 (RN1-8): the run was read and failed at the statement; the detector row's wording is the factory's
            record["language"], record["cause"] = detail["language"], "data_row"   # data to correct - never `tooling`, so no `probe gap: tooling:<language>` question
        else:
            _tooling_gap(record, detail)
    if row_notes.get(id(first)):
        notes.append(row_notes[id(first)])


def _detector_oracle(root: Path, run_cwd: Path, cfg: dict, spec: dict, oracle: str, path: Path) -> tuple:
    """(file the mutation lands in, the helper's name or "", the note) for a test that is not Python. With no
    `--oracle` the test itself holds its assertion (a body with none is refused, E6). `--oracle
    [<file>::]<name>` names a helper of the same language; its file must lie in the test tree and in no
    protected product path (E10) - the product is never touched knowingly - and a file that is not there is
    a refusal, never a silent fall back to the test."""
    if not oracle:
        return path, "", ""
    file_hint, _, name = str(oracle).rpartition("::")
    target = path
    if file_hint:
        target = next((p for p in (root / file_hint, run_cwd / file_hint) if p.is_file()), None)
        if target is None:
            raise Refusal(f"probe_by_code: --oracle names the file {file_hint!r}, and no such file is under the "
                          "project root. Nothing was changed.")
    if target.suffix.lower() not in spec["entry"]["suffixes"]:
        raise Refusal(f"probe_by_code: the oracle file {file_hint} is not a {spec['language']} file "
                      f"({' '.join(spec['entry']['suffixes'])}): a helper is read with the grammar of the test's own "
                      "language. Nothing was changed.")
    if target.resolve() != path.resolve() and not _in_test_root(cfg, _rel_project(target, root)):
        raise Refusal(f"probe_by_code: the oracle file {_rel_project(target, root)} is not under a test root "
                      "(roots.test of a profile), or lies under a protected_app_paths entry: this probe never "
                      "touches the product tree knowingly. Name a helper inside the test tree, or use the probe that "
                      f"breaks the product in a throwaway copy: {RED_SANDBOX_DOOR}. Nothing was changed.")
    return target, name or str(oracle), f"the oracle was named by hand: {oracle}"


def probe(task: str, dispatch: str, test: str, instance_id: str, mutation: str,
          timeout: int = RUN_TIMEOUT_S, oracle: str = "", at=None, *, s6_close: bool = False,
          alternative: str = "", model: str = "", supersede=None) -> dict:
    """One probe. The per-file locks it takes live exactly as long as this call: released on every
    way out (an answer, a refusal, a crash), and by the OS if the process is killed.

    `s6_close` (keyword only) is the `--s6-close` form of the call (HF3-6): the probe of the code close of S6, with no
    dispatch open (`dispatch` is then ""; the context's own id is taken from the story's state)."""
    locks: list = []
    try:
        return _probe(task, dispatch, test, instance_id, mutation, timeout, oracle, locks, at, s6_close=s6_close,
                      alternative=alternative, model=model, supersede=supersede)
    finally:
        release_locks(locks)


def _refuse_flags(spec: dict, detector: bool, mutation: str, at, model=None) -> None:
    """Refuse a flag that means something only for the other kind of test, before anything is read. An `alternative` probe of a
    test that is not Python goes on to its `gap` record (no model is needed or read there); of a Python test it needs `--model`."""
    if mutation == ALTERNATIVE and not detector and not model:
        raise Refusal("--model <file under work/probe-models/> is required for a Python test: the model says where reading B "
                      "is modelled (`probe_by_code.py --task <TICKET> --alternatives` prints the skeleton). "
                      "Nothing was changed.")
    if detector and mutation not in ("invert", ALTERNATIVE):
        raise Refusal(f"--mutation {mutation} is Python's: a {spec['language']} test has `invert` pairs only "
                      f"(references/detectors.json assertion_probes.{spec['language']}.assertions[].invert); use "
                      "--mutation invert. Nothing was changed.")
    if at is not None and not detector:
        raise Refusal("--at <line> picks among the declarations or assertions of a test that is not Python; a Python "
                      "test is found by its AST node (`<file>::[Class::]<function>`), and the oracle by `--oracle`. "
                      "Nothing was changed.")


def _test_path(root: Path, cfg: dict, spec: dict, entry: dict | None = None) -> tuple:
    """(the test file, the directory its profile runs in); a refusal when no such file is under the root.
    `entry` is the instance's manifest row: the profile it names settles a test root several profiles share.
    Reads no byte of the file: what is read, and when, is the caller's (R9)."""
    import execution_request as ER
    cwd = root / _profile_cwd(cfg, spec["file"], ER.entry_profile_id(entry))
    path = next((p for p in (root / spec["file"], cwd / spec["file"]) if p.is_file()), None)
    if path is None:
        raise Refusal(f"no file {spec['file']} under the project root")
    return path, cwd.resolve()


def _resolve_oracle(root: Path, run_cwd: Path, cfg: dict, spec: dict, detector: bool, oracle: str,
                    path: Path, test_text: bytes) -> tuple:
    """(the file the mutation lands in, the function whose assert is mutated, the note saying how it was
    found). Which FILE the mutation lands in is decided here: the test's own, or the one holding the
    helper or fixture its expectation lives in. Everything after it - the restore, the sha in the
    fingerprint - follows that file, while the test file stays the probe's identity. The test's bytes
    are the caller's argument, read after the test's lock (R9): this function reads none of them."""
    if detector:
        return _detector_oracle(root, run_cwd, cfg, spec, oracle, path)
    if oracle:
        file_hint, _, name = str(oracle).rpartition("::")
        oracle_path = next((p for p in (root / file_hint, run_cwd / file_hint)
                            if file_hint and p.is_file()), path)
        return oracle_path, name or str(oracle), f"the oracle was named by hand: {oracle}"
    found, oracle_note = find_oracle(test_text.decode("utf-8", "replace"), spec, path, root,
                                     _helper_chain(path, run_cwd))
    if found is None:
        return path, "", oracle_note       # plan_mutation refuses with the shape
    return found[0], (found[1] if oracle_note else ""), oracle_note


class ProbeCtx(NamedTuple):
    """What one probe launch has fixed BEFORE it reads a byte of the test (R9): the arguments of `probe()`
    that are values, and what `_test_path` and the manifest give without opening the file. Immutable, and
    it holds nothing a helper changes and no bytes (E11): `record`, `notes`, `locks`, the bytes, their shas
    and the oracle stay arguments, so the lock still comes before the first read of each file and no helper
    can read the test or the oracle from here. `path` is the test file's PATH."""
    task: str
    dispatch: str
    instance_id: str
    case: str
    spec: dict
    entry: dict
    root: Path
    cfg: dict
    task_root: Path
    detector: bool
    mutation: str
    manifest_path: Path
    path: Path
    # The stage the probe belongs to when it has no dispatch to name it ("S6" in the close context, HF3-6); "" = the
    # stage of the dispatch, read by `proof_level` as before. Last and defaulted: a positional build stays valid.
    stage: str = ""


def _repeat_check(ctx: ProbeCtx, now: dict, test_sha: str, copy_notes: list) -> tuple:
    """(the answer to give, or None; the notes the new record starts with). The identity of the test is
    measured by the caller BEFORE the mutation is written: a mutated file is never measured as the
    author's bytes. The same measure answers a repeat (D-0018): a test already probed over these very
    bytes is reported and nothing runs after it - no mutation, no request file, no job, no record
    overwritten. It errs only toward running: a check that fails says so in a note and the probe goes
    on (P1: code tells, never stops)."""
    pre_notes: list = list(copy_notes)
    if now["input_hash"] != test_sha:
        pre_notes.append(f"--test names {ctx.spec['file']}, which is not the file the manifest row of "
                         f"{ctx.instance_id!r} names ({proof_level.test_file_of(ctx.entry) or 'none'}), or that "
                         "file cannot be read: the repeat check is not made, and the record binds the "
                         "bytes measured here")
        return None, pre_notes
    try:
        answer = proof_level.already_probed(ctx.entry,
                                            C.load_json(ctx.manifest_path) if ctx.manifest_path.is_file() else {},
                                            ctx.task_root, now=now, project=ctx.root, dispatch=ctx.dispatch,
                                            stage=ctx.stage)
    except Exception as exc:
        answer = {"probed": False, "notes": [f"the repeat check failed ({type(exc).__name__}: "
                                             f"{str(exc)[:160]}); the probe runs"]}
    if answer.get("probed"):
        return {"verdict": "already_probed", "instance_id": ctx.instance_id, "by": answer["by"],
                "level": answer["level"], "receipt_ref": answer["receipt_ref"],
                "record": answer["record"], "prior_verdict": answer["prior_verdict"],
                "recorded_at": answer["recorded_at"], "holds": answer["holds"],
                "words": answer["words"], "block": answer["block"],
                "notes": copy_notes + list(answer["notes"] or [])}, pre_notes
    pre_notes.extend(answer.get("notes") or [])
    return None, pre_notes


def _plan(ctx: ProbeCtx, at, original: bytes, oracle_path: Path, oracle_function: str, oracle_note: str) -> tuple:
    """(the mutated bytes, the detail of the mutation). For a test that is not Python, everything the
    run needs is checked BEFORE the first write (R6): the whole case runs, and one row of its report
    is read."""
    if not ctx.detector:
        return plan_mutation(original, ctx.spec, ctx.mutation, ctx.instance_id, oracle_function, oracle_note)
    mutated, detail, context = plan_detector_mutation(original, ctx.spec, ctx.instance_id, at, oracle_function,
                                                      oracle_note, _rel_project(oracle_path, ctx.root))
    run_shape_checks(ctx.cfg, C.load_json(ctx.manifest_path) if ctx.manifest_path.is_file() else {}, ctx.case,
                     ctx.entry, ctx.spec, ctx.instance_id, context, original.decode("utf-8-sig", "replace"), ctx.root)
    return mutated, detail


def _new_record(ctx: ProbeCtx, detail: dict, identity: dict, test_bytes: bytes, original: bytes,
                oracle_path: Path) -> dict:
    """The record of a probe that has not run yet: verdict `not_executed`, every field the run fills in
    later empty. `notes` is a fresh list the caller extends."""
    spec, path = ctx.spec, ctx.path
    fields, missing = obligation_fields(ctx.entry)
    expected_location = f"{detail.get('file') or spec['file']}:{detail['line']}"
    return {
        "schema_version": 1, "probe_tool": "probe_by_code.py", "task": ctx.task, "dispatch_id": ctx.dispatch,
        "instance_id": ctx.instance_id, "case": ctx.case, "test_node": spec["node"],
        "verdict": "not_executed", "mutation": ctx.mutation, "mutation_kind": MUTATION_KIND,
        "proof_level": proof_level.LIVE, "failure_kind": None, "expected_location": expected_location, "actual_location": None,
        "expected_reason": detail["marker"], "actual_reason": None, "observed": {},
        "input_hash": None, "input_hash_source": None, "test_file_sha256": sha256(test_bytes),
        # the same measured bytes without comments, docstring lines and blank lines: a later
        # comment-only edit of the test keeps this probe's receipt (D-0017, proof_level)
        "test_code_sha": proof_level.code_sha(test_bytes, path.name),
        # The per-test identity (`--mine`'s `instance_contracts` shas, re-measured by their producer) and
        # the flat sha beside it that says the same thing under the name the run blocks use: ONE
        # derivation per field name. "" when the test has no measurable identity (never a stand-in).
        "instance_identity": identity, "instance_content_sha": identity.get("instance_content_sha", ""),
        # What this probe mutated, so a later repeat is answered only while that file still holds
        # these bytes: the oracle may be a helper or the product, not the test (`already_probed`).
        "mutated_file": {"path": _rel_project(oracle_path, ctx.root), "sha256": sha256(original),
                         "code_sha": proof_level.code_sha(original, oracle_path.name)},
        **fields, "manifest_fields_missing": missing,
        "evidence_ref": None, "evidence_refs": [], "request": None,
        "mutation_detail": detail, "restore": None, "notes": [],
        "recorded_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }


_READ_BOUND = object()   # `_run_and_judge`: the caller did not read the author's binding, read it here


def _run_and_judge(ctx: ProbeCtx, record: dict, oracle_path: Path, mutated_sha: str, original_sha: str,
                   timeout: int, *, judge_row: Callable = None, request_stem: str = None, reason: str = None,
                   mutation_kind: str = MUTATION_KIND, bound=_READ_BOUND) -> None:
    """Build the request, run it, judge the run - filling `record` and its `notes` in place (it is the
    contract of `_judge_run` too). Nothing in here may stop the caller: the record says what happened,
    and the author's bytes go back regardless (the caller's `finally`). The task, dispatch, case,
    instance and mutation are read from `ctx`; the detail and the expected location from the record
    they were written into.

    The keywords are the alternative probe's (TQ1-25): its row judge, its own request file stem (`probe-alt-...`, never the
    invert probe's), its reason, the `mutation_kind` the request names, and the author's binding it already read (one read,
    one id). Their defaults are the invert probe's, unchanged."""
    root, task_root, spec, entry = ctx.root, ctx.task_root, ctx.spec, ctx.entry
    notes, instance_id = record["notes"], ctx.instance_id
    reason = reason or (f"probe-{instance_id}: {ctx.mutation} of the first assert at {record['expected_location']} "
                        f"({ctx.dispatch})")
    try:
        import execution_request as ER
        request, build_notes = build_request(root, ctx.cfg, ctx.task, ctx.dispatch, ctx.case, spec, instance_id,
                                             ctx.mutation, reason, ER.entry_profile_id(entry),
                                             s6_close=ctx.stage == "S6",   # only the close context sets `stage`
                                             mutation_kind=mutation_kind)
        notes.extend(build_notes)
        request_path = (task_root / "work" / "probe-requests"
                        / f"{request_stem or 'probe-' + record_path(task_root, instance_id).stem}.json")
        atomic_json(request_path, request)
        record["request"] = request_path.relative_to(task_root).as_posix()
        record["input_hash"] = original_input_hash(request, oracle_path, mutated_sha, original_sha)
        record["input_hash_source"] = "fingerprint:test_content_sha over the author's bytes"
        if bound is _READ_BOUND:
            bound = author_binding(task_root, instance_id, record["instance_content_sha"])
        if bound:
            record["input_hash"] = bound["test_content_sha"]
            record["input_hash_source"] = f"run_block:{bound['run_block']} ({bound['dispatch_id']})"
            record["author_run_block"] = bound["run_block"]
        proc, summary = run_request(root, request_path, timeout)
        if not summary:
            notes.append(f"run_suite printed no summary (exit {proc.returncode}): "
                         + fold((proc.stderr or proc.stdout or "").strip()[-600:], 600))
        else:
            _judge_run(root, task_root, record, summary, spec, record["mutation_detail"], request, oracle_path,
                       [instance_id, C.test_instance_id(entry) or instance_id], judge_row=judge_row)
    except Exception as exc:  # the record says what happened; the bytes go back regardless
        notes.append(f"{type(exc).__name__}: {exc}")


def _finish_record(record: dict, entry: dict, task_root: Path, instance_id: str) -> None:
    """Window probe, receipt and the write of the record - after the author's bytes are back."""
    record["window_probe"] = window_probe(record)
    out = record_path(task_root, instance_id)
    record["record"] = out.relative_to(task_root).as_posix()
    record["receipt"], record["receipt_missing"] = None, []
    # Only a probe that showed the intended failure AND put the author's bytes back proves
    # anything: an unverified restore is the tool's own failure, and a receipt would vouch for it.
    if record["verdict"] == "intended_failure" and (record.get("restore") or {}).get("verified"):
        attach_receipt(record, entry, task_root)
    if not keep_standing_record(out, record):
        atomic_json(out, record)


def _dispatch_context(root: Path, task: str, task_root: Path, dispatch: str, case: str, s6_close: bool) -> tuple:
    """(dispatch, stage) of the context this probe runs under, asked BEFORE `_test_path`, `scan_copies`, any lock or
    any read of the test (HF3-6 for `--s6-close`, RH1-8 B3 for `--dispatch`). Invariant: a refused context restores
    nobody's copy, takes no lock, reads and mutates no byte, and writes no request, job or record.

    `--s6-close`: the S6 close context, `(id, "S6")`. `--dispatch`: the answer of `find_active_dispatch` is only
    "there is one / refusal"; the PASSED id is kept unchanged (a `parent_retry` ancestor id stays the id the request
    and its `idempotency_key` carry), with no stage. The late question in `build_mine_request` stays (a race)."""
    import execution_request as ER
    if s6_close:
        try:
            got = ER.s6_close_dispatch(task_root, [case])
        except ER.MineRefusal as exc:
            raise Refusal(f"probe_by_code: {exc}") from exc
        return got["id"], "S6"
    from hooklib import artifact_root
    try:
        ER.find_active_dispatch(artifact_root(root=root), task, dispatch, [case], None)
    except ER.MineRefusal as exc:
        detail = str(exc)
        # keep the REASON only: the doors `find_active_dispatch` appends (`--dispatch ID`, `controller.py --operation prepare`,
        # `--task/--label`) belong to the `--mine` caller, not to the critic who reads this refusal (FR-2, RH1-8 F5)
        reason = detail
        for door in (". Inside a story", "; say which one is yours"):
            reason = reason.split(door)[0]
        head =(f"several dispatches are open in story {task}; " if detail.startswith("several dispatches are open")
                else f"no open dispatch {dispatch} in story {task}: ")
        raise Refusal(
            f"probe_by_code: {head}the probe runs only under the dispatch your brief names. Nothing was read or "
            f"changed. Check the id in your brief; if it is that one, report the probe as cause: tooling "
            f"(dispatch not open), repeated under tooling_findings; the instance stays unverified. "
            f"Detail: {reason}.") from exc
    return dispatch, ""


def _lock_test(ctx: ProbeCtx, locks: list) -> tuple:
    """(the test file's copy key, the notes of what a dead probe left). POSITION (R9): everything before this call read no
    byte of the test. Before the FIRST read of it - and so before any byte can be taken as "the author's original", as
    `test_file_sha256` or as the identity - (1) what a dead probe left is restored, (2) this file's lock is taken.
    Invariant: no byte is read as the author's until every dead probe's copy has been put back, and none is read while another
    probe may be mutating the file. The ONE copy of this order: `_probe` and `_probe_alternative` both call it."""
    copy_notes: list = []
    test_key, test_shown = copy_key(ctx.path, ctx.root)
    scan_copies(ctx.root, skip_keys={test_key}, notes=copy_notes)
    held = claim_key(ctx.root, test_key, test_shown, own=True, notes=copy_notes)
    if held is not None:
        locks.append(held)
    return test_key, copy_notes


def _require_cover(task_root: Path, manifest_path: Path, entry: dict, instance_id: str, case: str) -> None:
    """The instance must prove the case the alternative token names (`instances_of_case`, the one reader): else the CALL is
    wrong (exit 2, FR-46). Invariant: a record is only ever keyed by a (case, ALT) the instance proves. Reads the manifest only."""
    import s5_precheck as S5
    cfg = C.case_config()
    manifest = C.load_json(manifest_path) if manifest_path.is_file() else {}
    aliases = {a for row in S5.instances_of_case(manifest, case, cfg) for a in C.instance_id_aliases(row, cfg)}
    if instance_id not in aliases and (C.test_instance_id(entry) or instance_id) not in aliases:
        raise Refusal(f"instance {instance_id!r} does not cover case {case}: an alternative is probed on an instance that "
                      "proves its case (`probe_by_code.py --task <TICKET> --alternatives` lists each instance with its "
                      "cases). Nothing was changed.")


def _probe(task: str, dispatch: str, test: str, instance_id: str, mutation: str, timeout: int,
           oracle: str, locks: list, at=None, *, s6_close: bool = False, alternative: str = "", model: str = "",
           supersede=None) -> dict:
    root = project_root().resolve()
    task_root = artifacts_dir(task).resolve()
    cfg = load_config()
    spec = parse_node(test, root)
    detector = bool(spec.get("language"))
    _refuse_flags(spec, detector, mutation, at, model=model)
    alt_case = parse_alternative_token(alternative)[0] if mutation == ALTERNATIVE else ""
    entry = manifest_entry(task_root, instance_id)
    if alt_case:
        # The case of an alternative probe is the TOKEN's, not the instance's first: the dispatch scope and the request name it
        # (an instance covering TC-001 and TC-002 is probed for TC-002 under the window that holds TC-002).
        _require_cover(task_root, task_root / "work" / "automation-manifest.json", entry, instance_id, alt_case)
    case = alt_case or str(entry.get("case") or next(iter(entry.get("covers") or []), "") or "")
    if not case:
        raise Refusal(f"the manifest entry of {instance_id!r} names no case")
    dispatch, stage = _dispatch_context(root, task, task_root, dispatch, case, s6_close)
    path, run_cwd = _test_path(root, cfg, spec, entry)
    ctx = ProbeCtx(task, dispatch, instance_id, case, spec, entry, root, cfg, task_root, detector, mutation,
                   task_root / "work" / "automation-manifest.json", path, stage)
    if mutation == ALTERNATIVE:
        return _probe_alternative(ctx, locks, alternative, model, supersede, timeout)
    test_key, copy_notes = _lock_test(ctx, locks)
    test_bytes = path.read_bytes()
    test_text = test_bytes[3:] if test_bytes.startswith(b"\xef\xbb\xbf") else test_bytes
    oracle_path, oracle_function, oracle_note = _resolve_oracle(root, run_cwd, cfg, spec, detector, oracle, path,
                                                                test_text)
    # The oracle is another file when the expectation lives in a helper: its lock (and the recovery of a
    # copy a dead probe left of it) comes BEFORE its bytes are read as the original, for the same reason.
    oracle_key, oracle_shown = copy_key(oracle_path, root)
    if oracle_key != test_key:
        held = claim_key(root, oracle_key, oracle_shown, own=True, notes=copy_notes)
        if held is not None:
            locks.append(held)
    original = oracle_path.read_bytes()
    original_sha = sha256(original)
    stat = oracle_path.stat()
    # The identity of the test is measured HERE, before the mutation is written; the same call answers a
    # repeat (D-0018) - the check and its reasons are `_repeat_check`'s.
    test_sha = sha256(test_bytes)
    now = proof_level.instance_identity(entry, task_root, root)
    answer, pre_notes = _repeat_check(ctx, now, test_sha, copy_notes)
    if answer is not None:
        return answer
    identity = now["instance_identity"] if now["input_hash"] == test_sha else {}
    mutated, detail = _plan(ctx, at, original, oracle_path, oracle_function, oracle_note)
    mutated_sha = sha256(mutated)
    if oracle_function and not detector:
        detail["file"] = _rel_root(oracle_path, root, run_cwd)
    record = _new_record(ctx, detail, identity, test_bytes, original, oracle_path)
    missing = record["manifest_fields_missing"]
    notes = record["notes"]
    notes.extend(pre_notes)
    if missing:
        notes.append("the manifest entry carries no " + ", ".join(missing)
                     + ": fill them in the window instance AND here, identically, before the window")
    # The byte copy goes to disk and is verified BEFORE the first write to the author's file: a probe
    # killed from here on leaves the way back behind it (R9 write order 1-2).
    copy = begin_copy(root, oracle_path, original, original_sha, stat, mutated_sha, detail, timeout)
    try:
        oracle_path.write_bytes(mutated)
        _run_and_judge(ctx, record, oracle_path, mutated_sha, original_sha, timeout)
    finally:
        # FROM the copy, verified; the copy is deleted only after the verification (write order 4-7).
        record["restore"] = restore(oracle_path, original, original_sha, stat, copy=copy["orig"])
        finish_copy(copy, record["restore"], root)
    _finish_record(record, entry, task_root, instance_id)
    return record


# --- the alternative reading: the red probe models reading B (TQ1-25) -------------------------------------------------
# A Then its case lists in `alternatives` must FAIL when the product behaves per reading B. The critic writes a MODEL (a
# file under `work/probe-models/`: one `find -> replace` inside the test function, where the test reads the product's
# value); this tool applies it to the author's bytes under the byte copy, runs the one node, and reads the run. The
# verdict is `intended_failure` (the Then's own assert failed under B, and the test was green under A), `no_failure` (it
# passed under B: the Then separates nothing), `wrong_location`, or `incomplete` / `not_executed` / `gap` / `unknown`. Every
# function here errs one way: toward NOT `intended_failure` and never toward blaming the author for the critic's model.
# The record is keyed `<IID>--<CASE>--<ALT>` under `work/probes/alternative/`; it is never a live receipt, never published.

def parse_alternative_token(value) -> tuple:
    """`<case>:ALT-<n>` -> (case, alt). One form only: the case is part of the identity (a bare `ALT-1` of an instance that
    covers two cases would answer for both). `rpartition`: an ALT id never holds a colon."""
    case, _, alt = str(value or "").strip().rpartition(":")
    case = case.strip()
    if not case or not C.ALTERNATIVE_ID.fullmatch(alt):
        raise Refusal(f"--alternative wants <case>:ALT-<n> (for example TC-001:ALT-1), got {value!r}; `probe_by_code.py "
                      "--task <TICKET> --alternatives` prints the token of every declared reading. Nothing was changed.")
    return case, alt


def _model_refusal(path, what: str) -> Refusal:
    return Refusal(f"--model {path}: {what}. A model is ONE JSON object under work/probe-models/ (any file name): "
                   '{"alternative": "<case>:ALT-n", "find": "<the line where the test reads the product\'s value>", '
                   '"replace": "<that line under reading B>"} or {"alternative": "<case>:ALT-n", "gap": "<why B cannot be '
                   'modelled in the test>"}; `function` (optional) names [<file>.py::]<function>. Nothing was changed.')


def model_function_parts(model: dict) -> tuple:
    """(the file hint, the function name) of a model's optional `function`: `("", "")` = the test's own function."""
    hint, _, name = str(model.get("function") or "").rpartition("::")
    return hint, name


def load_model(task_root: Path, path, token: str) -> dict:
    """The critic's model file, validated: under `<task>/work/probe-models/` after `resolve()` (a symlink out is refused),
    <= MODEL_FILE_MAX bytes, UTF-8 (a BOM is tolerated), one JSON object whose `alternative` equals the token EXACTLY and that
    carries EXACTLY ONE of (`find` + `replace`) or `gap`. Every violation is a Refusal naming the field, the limit and the shape;
    nothing is mutated or written."""
    base = (Path(task_root) / "work" / "probe-models").resolve()
    raw = Path(str(path))
    target = raw if raw.is_absolute() else Path(task_root) / raw
    try:
        resolved = target.resolve()
        resolved.relative_to(base)
    except (ValueError, OSError):
        raise _model_refusal(path, f"the file is not under {base.as_posix()} (a link out of it counts as out)") from None
    if not resolved.is_file():
        raise _model_refusal(path, "no such file")
    size = resolved.stat().st_size
    if size > MODEL_FILE_MAX:
        raise _model_refusal(path, f"the file is {size} bytes, at most {MODEL_FILE_MAX} are read")
    data = resolved.read_bytes()
    try:
        doc = json.loads(data.decode("utf-8-sig"))
    except UnicodeDecodeError:
        raise _model_refusal(path, "the file is not UTF-8") from None
    except (ValueError, RecursionError):
        raise _model_refusal(path, "the file is empty or not valid JSON") from None
    if not isinstance(doc, dict):
        raise _model_refusal(path, "the JSON is not one object")
    if doc.get("alternative") != token:
        raise _model_refusal(path, f"`alternative` is {doc.get('alternative')!r}, it must be exactly {token!r}")
    has_pair, has_gap = "find" in doc or "replace" in doc, "gap" in doc
    if has_pair == has_gap:
        raise _model_refusal(path, "it must carry EXACTLY ONE of (`find` and `replace`) or `gap`")
    out = {"alternative": token, "find": "", "replace": "", "gap": "", "function": "", "sha256": sha256(data), "content": doc,
           "file": _rel_task(str(resolved), Path(task_root), Path(task_root))}
    if has_gap:
        gap = doc["gap"]
        if not isinstance(gap, str) or not 1 <= len(gap.strip()) <= MODEL_GAP_MAX:
            raise _model_refusal(path, f"`gap` must be a string of 1 to {MODEL_GAP_MAX} characters")
        out["gap"] = gap.strip()
        return out
    find, replace = doc.get("find"), doc.get("replace")
    if not isinstance(find, str) or not 1 <= len(find) <= MODEL_TEXT_MAX:
        raise _model_refusal(path, f"`find` must be a string of 1 to {MODEL_TEXT_MAX} characters")
    if not isinstance(replace, str) or len(replace) > MODEL_TEXT_MAX:
        raise _model_refusal(path, f"`replace` must be a string of at most {MODEL_TEXT_MAX} characters")
    function = doc.get("function", "")
    if function:
        hint, _, name = str(function).rpartition("::")
        if not isinstance(function, str) or not name.isidentifier() or (hint and not hint.endswith(".py")):
            raise _model_refusal(path, "`function` must be [<file>.py::]<function>")
    out.update(find=find, replace=replace, function=str(function or ""))
    return out


def declared_alternative(task_root: Path, case: str, alt: str, cfg) -> tuple:
    """(the declared item | None, why not). The case file is the contract's (`s5_precheck._case_file_of`: a qualified key is that
    area's file), the key is read by `contract.alternatives_from_text`, and the Then must be one of the case's."""
    import s5_precheck as S5
    file = S5._case_file_of(task_root, case, cfg)
    if file is None:
        return None, f"case file of {case} not found"
    try:
        text = Path(file).read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        return None, f"case file of {case} cannot be read ({type(exc).__name__})"
    entries, problem = C.alternatives_from_text(text)
    if entries is None:
        return None, (f"the key is malformed: {problem}" if problem else "the `alternatives` key is absent")
    errors = C.alternatives_errors(case, entries, [n for n, _ in S5.then_clauses(text)])     # ONE validity rule, the report's too
    if errors:
        return None, f"the key is malformed: {errors[0]}"
    item = next((e for e in entries if e.get("id") == alt), None)
    if item is None:
        return None, f"{alt} is not declared in {case}"
    return item, ""


def then_assertions(manifest: dict, case: str, then, entry: dict, cfg) -> list:
    """[(file, line)] of the covered `then_bindings` rows of THIS instance for this Then, read through `bindings_of_case` (the one
    reader: area-qualified and instance-only rows included). [] = no covered binding."""
    import s5_precheck as S5
    aliases = set(C.instance_id_aliases(entry, cfg))
    out: list = []
    for row in S5.bindings_of_case(manifest, case, cfg):
        number = row.get("then")
        if row.get("status") != "covered" or isinstance(number, bool) or str(number).strip() != str(then):
            continue
        if str(row.get("instance_id") or "") not in aliases:
            continue
        file, _, line = str(row.get("assertion_ref") or "").rpartition(":")
        if file and line.isdigit() and int(line) > 0 and (file, int(line)) not in out:
            out.append((file, int(line)))
    return out


def _deepest_statement(func, line: int):
    """The innermost statement of `func` (its own def excluded) that holds `line`; None when none does."""
    best = None
    for node in ast.walk(func):
        if node is func or not isinstance(node, ast.stmt) or not node.lineno <= line <= node.end_lineno:
            continue
        if best is None or (node.end_lineno - node.lineno, -node.lineno) < (best.end_lineno - best.lineno, -best.lineno):
            best = node
    return best


def assert_spans(test_bytes: bytes, spec: dict, refs: list, path: Path, root: Path, run_cwd: Path) -> tuple:
    """(the asserting statements as [(first line, last line)] | None, why). Every bound assertion must lie in the TEST file: an
    assert in a helper cannot be told apart from a failure the model caused there (`red_sandbox.py --probe` models the product).
    The spans come from the test bytes already read under the lock (no second read)."""
    for file, line in refs:
        named = _same_file(file, spec["file"]) or any(
            candidate.is_file() and candidate.resolve() == path.resolve() for candidate in (root / file, run_cwd / file))
        if not named:
            return None, (f"the Then's assertion lives in {file}:{line}, a helper: the probe cannot check that the failure is "
                          "the Then's own (red_sandbox.py --probe models the product)")
    text = test_bytes[3:] if test_bytes.startswith(b"\xef\xbb\xbf") else test_bytes
    try:
        func = locate(ast.parse(text.decode("utf-8")), spec["chain"], spec["function"])
    except (SyntaxError, UnicodeDecodeError, Refusal) as exc:
        return None, f"the test file cannot be read as the test {spec['function']}: {exc}"
    spans: list = []
    for file, line in refs:
        node = _deepest_statement(func, line)
        if node is None:
            return None, f"the bound assertion {file}:{line} is not a statement of {spec['function']}"
        if (node.lineno, node.end_lineno) not in spans:
            spans.append((node.lineno, node.end_lineno))
    return spans, ""


_NESTED = (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)
_BRANCH_HOLDERS = tuple(t for t in (ast.ExceptHandler, getattr(ast, "match_case", None)) if t)
_SCOPES = (ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp, ast.Lambda)


def _walk_statements(body, chain: tuple, nested: bool):
    """(statement, its chain of (enclosing node, field) pairs, whether it lies in a nested def/class) in source order. The chain
    tells `If.body` from `If.orelse`, `Try.body` from a handler's body, so "the same path" is a prefix compare."""
    for node in body:
        yield node, chain, nested
        deeper = nested or isinstance(node, _NESTED)
        for field in ("body", "orelse", "finalbody", "handlers", "cases"):
            children = getattr(node, field, None)
            if not isinstance(children, list):
                continue
            for child in children:
                if isinstance(child, _BRANCH_HOLDERS):
                    yield from _walk_statements(child.body, chain + ((id(node), field), (id(child), "body")), deeper)
                elif isinstance(child, ast.stmt):
                    yield from _walk_statements([child], chain + ((id(node), field),), deeper)


def model_reach(func_node, region: tuple, spans: list, starts: list, targets_test: bool = True) -> tuple:
    """(True, "") only when the model's replaced region RUNS BEFORE every asserting statement on the way into it (B-3): the model
    targets the TEST function in the test file; the innermost statement S holding the region ends before the first line of
    every asserting span; S is not inside a nested def/lambda/class or a comprehension; and S's chain of enclosing branches is a
    PREFIX of each asserting statement's (the same path: an `if` body is not its `else`). S itself may be compound: its header
    runs whenever S is reached. Otherwise (False, why). A pass that cannot be shown to have reached its model is `incomplete`,
    never `no_failure` (the error goes toward not blaming the author). Pure."""
    if not targets_test:
        return False, "the model targets a helper, not the test function: its reach cannot be shown"
    start, end = region
    rows = list(_walk_statements(func_node.body, (), False))
    holding = [(node, chain, nested) for node, chain, nested in rows
               if _span(starts, node)[0] <= start and end <= _span(starts, node)[1]]
    if not holding:
        return False, "the model's region is not inside a statement of the test function"
    node, chain, nested = min(holding, key=lambda r: _span(starts, r[0])[1] - _span(starts, r[0])[0])
    if nested:
        return False, "the model is inside a nested function"
    for sub in ast.walk(node):
        if isinstance(sub, _SCOPES) and _span(starts, sub)[0] <= start and end <= _span(starts, sub)[1]:
            return False, "the model is inside a comprehension or a lambda"
    for first, last in spans:
        if node.end_lineno >= first:
            return False, "the model is after the assert (or on its line)"
        asserting = [(c, n) for s, c, n in rows if (s.lineno, s.end_lineno) == (first, last)]
        if not asserting:
            return False, "the asserting statement is not a statement of the test function"
        if not any(chain == c[:len(chain)] for c, _n in asserting):
            return False, "the model sits in a branch the assert is not in"
    return True, ""


class _Identities(ast.NodeTransformer):
    """Drops the arithmetic identities (`x + 0`, `0 + x`, `x - 0`, `x * 1`, `1 * x`, `x / 1`, `x // 1`, `x ** 1`, `+x`): the one
    class of "changes code, not the value" that syntax alone can prove (a bool is no number here)."""

    @staticmethod
    def _is(node, number) -> bool:
        return isinstance(node, ast.Constant) and not isinstance(node.value, bool) and node.value == number \
            and isinstance(node.value, (int, float))

    def visit_BinOp(self, node):
        self.generic_visit(node)
        if isinstance(node.op, (ast.Add, ast.Sub)) and self._is(node.right, 0):
            return node.left
        if isinstance(node.op, ast.Add) and self._is(node.left, 0):
            return node.right
        if isinstance(node.op, (ast.Mult, ast.Div, ast.FloorDiv, ast.Pow)) and self._is(node.right, 1):
            return node.left
        if isinstance(node.op, ast.Mult) and self._is(node.left, 1):
            return node.right
        return node

    def visit_UnaryOp(self, node):
        self.generic_visit(node)
        return node.operand if isinstance(node.op, ast.UAdd) else node


def model_changes_value(model: dict) -> tuple:
    """(False, why) when the model PROVABLY changes no value: `find` and `replace` are the same code once the arithmetic
    identities are dropped (`read_stamp()` -> `read_stamp() + 0`). (True, "") otherwise, including every pair that does not parse
    on its own: code cannot judge value equivalence beyond syntax (AR-2); what is left (a constant that equals what A gives) is the
    critic's, by the rubric's "B's value is one A cannot give", and the report prints the model beside `not_separated`."""
    try:
        before = ast.dump(_Identities().visit(ast.parse(model["find"].strip())))
        after = ast.dump(_Identities().visit(ast.parse(model["replace"].strip())))
    except (SyntaxError, ValueError):
        return True, ""
    if before == after:
        return False, f"the model `{fold(model['find'], 80)}` -> `{fold(model['replace'], 80)}` changes no value"
    return True, ""


def _occurrences(hay: bytes, needle: bytes) -> list:
    found, pos = [], hay.find(needle)
    while pos >= 0:
        found.append(pos)
        pos = hay.find(needle, pos + 1)
    return found


def plan_alternative(data: bytes, spec: dict, model: dict, spans: list, target_is_test: bool, name: str = "x.py") -> tuple:
    """(mutated bytes, detail) - nothing is written here. The Python twin of `plan_mutation` for the model's `find -> replace`:
    BOM kept; `find` must occur EXACTLY once inside the model's function (module-level text is outside it); on the test file the
    replaced lines must not touch an asserting statement (that is an inversion: `--mutation invert`); `find` and `replace` carry the
    same number of line breaks (the author's line numbers stay where the run reported them); the result parses and its
    `code_sha` differs (a comment-only or no-op model cannot tell A from B). Every violation is a Refusal with its door."""
    bom = data.startswith(b"\xef\xbb\xbf")
    text = data[3:] if bom else data
    try:
        tree = ast.parse(text.decode("utf-8"))
    except (SyntaxError, UnicodeDecodeError) as exc:
        raise Refusal(f"{name} does not parse: {exc}") from exc
    _hint, wanted = model_function_parts(model)
    func = (locate(tree, spec["chain"], spec["function"]) if target_is_test and wanted in ("", spec["function"])
            else locate(tree, [], wanted))
    starts = _line_starts(text)
    f_start, f_end = _span(starts, func)
    find, replace = model["find"].encode("utf-8"), model["replace"].encode("utf-8")
    hits = _occurrences(text[f_start:f_end], find)
    if len(hits) != 1:
        crlf = (" The file uses CRLF line ends: write `find` with them (\\r\\n)."
                if b"\r\n" in text[f_start:f_end] and b"\n" in find and b"\r\n" not in find else "")
        raise Refusal(f"the model's `find` occurs {len(hits)} times inside {func.name} (exactly once is required; text outside "
                      f"the function, a module constant among it, is not searched): make `find` longer so it is unique.{crlf} "
                      "Nothing was changed.")
    start = f_start + hits[0]
    end = start + len(find)
    first, last = bisect.bisect_right(starts, start), bisect.bisect_right(starts, max(start, end - 1))
    if target_is_test and any(first <= b and a <= last for a, b in spans):
        raise Refusal("the model's `find` touches the asserting statement of the Then: editing the assertion is an inversion, "
                      "use --mutation invert; a model changes the value the test READS. Nothing was changed.")
    if find.count(b"\n") != replace.count(b"\n"):
        raise Refusal("the model's `find` and `replace` must carry the same number of line breaks (the line numbers of the "
                      "author's run must stay where they are). Nothing was changed.")
    mutated = text[:start] + replace + text[end:]
    try:
        ast.parse(mutated.decode("utf-8"))
    except (SyntaxError, UnicodeDecodeError) as exc:
        raise Refusal(f"the model's `replace` makes the file not parse ({exc}). Nothing was changed.") from exc
    before, after = proof_level.code_sha(text, name), proof_level.code_sha(mutated, name)
    if (before == after) if (before or after) else (text == mutated):
        raise Refusal("the model changes no code (only a comment, a blank line or nothing): it cannot tell reading A from B. "
                      "Nothing was changed.")
    shown = lambda blob: blob[starts[first - 1]:(starts[last] if last < len(starts) else len(blob))].decode("utf-8", "replace").strip()  # noqa: E731
    detail = {"line": spans[0][0] if spans else first, "end_line": spans[0][1] if spans else last, "file": spec["file"],
              "mutation": ALTERNATIVE, "model_find": model["find"], "model_replace": model["replace"], "model_line": first,
              "model_region": [start, end], "statement_before": shown(text),
              "statement_after": shown(mutated), "marker": ""}
    return (b"\xef\xbb\xbf" + mutated if bom else mutated), detail


def _in_span(location: str, spec: dict, spans: list) -> bool:
    return any(_location_hits(str(location or ""), spec, {"file": spec["file"], "line": a, "end_line": b}) for a, b in spans)


def judge_alternative(observed: dict, spans: list, author_green, reach: tuple, spec: dict = None) -> tuple:
    """(verdict, actual_location, mismatches, note) - pure, the ONLY decider of an alternative verdict (the table of the spec):

        passed:  author green under A and the model's reach shown   -> no_failure
                 author green, reach not shown                      -> incomplete (the model's reach is not proven)
                 author red or unknown                              -> incomplete (no green under A on these bytes)
        failed:  an assertion failure AT an asserting statement of the test file, author green -> intended_failure
                 the same with author red or unknown                -> incomplete
                 a location read outside every span, or not an assertion -> wrong_location
                 no location read                                   -> incomplete
        error (setup, teardown, collection)                         -> incomplete
        any other status                                            -> not_executed

    `author_green` is True / False / None (never True by default). Error direction: only toward NOT `intended_failure`."""
    spec = spec or {"file": ""}
    status = observed.get("status")
    if status == "passed":
        if author_green is not True:
            return "incomplete", None, [], "no green under A on these bytes: a pass under B proves nothing without it"
        if not reach[0]:
            return "incomplete", None, [], f"the model's reach is not proven: {reach[1]}"
        return "no_failure", None, ["the Then passed under reading B: its assert does not separate A from B"], ""
    if status == "error":
        return "incomplete", None, [], "the run errored in setup, teardown or collection, not at the Then's assert"
    if status != "failed":
        return "not_executed", None, [f"report status {status!r}"], ""
    tail, frame = observed.get("location") or "", observed.get("test_file_frame") or ""
    if not (tail or frame):
        return "incomplete", None, [], "no failure location could be read from the report"
    hit = _in_span(tail, spec, spans) or _in_span(frame, spec, spans)
    if hit and observed.get("failure_kind") == "assertion":
        if author_green is True:
            return "intended_failure", tail if _in_span(tail, spec, spans) else frame, [], ""
        return "incomplete", None, [], "red under A too, or A unknown: a red under both readings separates nothing"
    return "wrong_location", frame or tail, ["location" if not hit else "failure_kind"], ""


def _judge_alternative_row(record: dict, row: dict, spec: dict, detail: dict, *, spans: list, author_green, reach: tuple) -> None:
    observed = observe(row, spec, detail)
    record["observed"] = observed
    verdict, actual_location, mismatches, note = judge_alternative(observed, spans, author_green, reach, spec)
    record.update(verdict=verdict, actual_location=actual_location, actual_reason=observed.get("message_head") or None,
                  failure_kind=observed.get("failure_kind"), mismatches=mismatches + ([note] if note else []))
    if not record["mismatches"]:
        record.pop("mismatches")


# --- identity, freshness, naming -----------------------------------------------------------------------------

def alternative_record_path(task_root: Path, iid: str, case: str, alt: str) -> Path:
    """`work/probes/alternative/<IID>--<CASE>--<ALT>.json`: one naming (`proof_level.probe_record_path`), the CANONICAL instance id
    (an alias at probe time and the canonical id in the report find one file), the case in the key (an instance that covers two
    cases, both with an ALT-1, keeps two records)."""
    return proof_level.probe_record_path(task_root, f"{iid}--{case}--{alt}", kind="alternative")


def _reading_sha(item: dict) -> str:
    """The ONE formula of an alternative's reading hash (the run, the gap record and `alternative_now` all read it here)."""
    return sha256(json.dumps({"then": item.get("then"), "reading": str(item.get("reading") or "").strip()},
                             sort_keys=True).encode("utf-8"))


def alternative_now(entry: dict, task_root: Path, root: Path, item: dict, refs, target_rel: str = "") -> dict:
    """What the world says NOW, for `alternative_fresh`: the reading's hash, the test's raw sha and per-test identity (ONE read,
    `proof_level.instance_identity`), the Then's bound assertions (None when not asked) and the raw sha of the model's target file."""
    ident = proof_level.instance_identity(entry, task_root, root)
    target_sha = ""
    if target_rel:
        try:
            target_sha = sha256((Path(root) / target_rel).read_bytes())
        except OSError:
            target_sha = ""
    identity = ident.get("instance_identity") or {}
    return {"reading_sha": _reading_sha(item), "test_file_sha256": ident.get("input_hash") or "",
            "instance_content_sha": identity.get("instance_content_sha") or "", "instance_identity": identity,
            "assertion_refs": None if refs is None else [[f, n] for f, n in refs],
            "test_file": proof_level.test_file_of(entry), "target_sha": target_sha}


def alternative_fresh(record: dict, now: dict) -> tuple:
    """(True, "") or (False, "stale: <which>"). ONE predicate for the repeat check AND the report. Fresh iff the reading and its
    Then are the same, the test is (the raw sha, or a non-empty equal per-test identity: a neighbour's comment edit keeps it),
    the model's target file (when it is not the test) holds the bytes the model ran on, and the Then is bound to the same
    assertions. A record that never read the test (a tooling gap) is held to the reading alone. Any miss is stale: an old proof
    never stands for new bytes or a new reading."""
    if not isinstance(record, dict):
        return False, "stale: the record is unreadable"
    if record.get("reading_sha") != now.get("reading_sha"):
        return False, "stale: the case's reading of this Then changed"
    rec_raw, rec_id = record.get("test_file_sha256") or "", record.get("instance_content_sha") or ""
    if rec_raw or rec_id:
        cur_raw, cur_id = now.get("test_file_sha256") or "", now.get("instance_content_sha") or ""
        if not ((rec_raw and cur_raw and rec_raw == cur_raw) or (rec_id and cur_id and rec_id == cur_id)):
            return False, "stale: the test's bytes changed since this record"
    target = record.get("mutated_file") or {}
    if target.get("path") and target.get("sha256") and not _same_file(str(target["path"]), now.get("test_file") or ""):
        if target["sha256"] != now.get("target_sha"):
            return False, "stale: the file the model ran on changed since this record"
    if record.get("assertion_refs") is not None and now.get("assertion_refs") is not None \
            and [list(r) for r in record["assertion_refs"]] != now["assertion_refs"]:
        return False, "stale: the Then is bound to another assertion now"
    return True, ""


def _read_alt_record(path: Path) -> tuple:
    """(the record | None, why none). Missing is (None, ""): an unreadable file is said, never read as a proof."""
    if not path.is_file():
        return None, ""
    data = read_json(path, kind=dict)       # the package's one JSON reader (dup ratchet: no private copy)
    return (data, "") if data is not None else (None, "the record file cannot be read as one JSON object")


def _alt_answer(verdict: str, iid: str, token: str, why: str, notes=()) -> dict:
    """An ANSWER, not a record: nothing was mutated, launched or written (exit 1 for `unknown`, 0 for `already_probed`)."""
    return {"verdict": verdict, "instance_id": iid, "alternative": token, "why": why, "words": why, "notes": list(notes)}


def _store_alternative(out: Path, record: dict, old, reason: str) -> None:
    """Write the record atomically; the record it replaces (any verdict) is folded into `superseded[]` with its reason, so the
    old verdict stays visible (no model shopping)."""
    if isinstance(old, dict):
        record["superseded"] = list(old.get("superseded") or []) + [
            {"verdict": old.get("verdict"), "recorded_at": old.get("recorded_at"), "model_sha": old.get("model_sha"),
             "reason": reason}]
    atomic_json(out, record)


def _alt_base(ctx: ProbeCtx, iid: str, token: str, item: dict, out: Path, now: dict) -> dict:
    """The fields every alternative record carries (a gap or a run), under the names the exit and print paths of `main` read."""
    return {"schema_version": 1, "probe_tool": "probe_by_code.py", "task": ctx.task, "dispatch_id": ctx.dispatch,
            "instance_id": iid, "case": ctx.case, "alternative": token, "then": item["then"], "reading": item["reading"],
            "reading_sha": now["reading_sha"], "test_node": ctx.spec["node"], "verdict": "gap", "mutation": ALTERNATIVE,
            "mutation_kind": ALTERNATIVE_KIND, "proof_level": None, "expected_location": None,
            "expected_reason": f"alternative {token}", "actual_location": None, "actual_reason": None, "failure_kind": None,
            "observed": {}, "test_file_sha256": None, "instance_content_sha": "", "mutated_file": None,
            "assertion_refs": None, "evidence_ref": None, "evidence_refs": [], "request": None, "restore": None,
            "superseded": [], "notes": [], "record": out.relative_to(ctx.task_root).as_posix(),
            "recorded_at": datetime.now(timezone.utc).isoformat(timespec="seconds")}


def _alternative_gap_record(ctx: ProbeCtx, iid: str, token: str, item: dict, out: Path, old, *, cause: str, why: str,
                            now: dict, door: str = "", model: dict = None, copy_notes=()) -> dict:
    """The record `gap`: the probe could not model B, and says who owns that (`cause: model` the critic's own gap, `tooling` the
    factory's: a language with no substitution). It is the critic's citable word and never a verdict on the test."""
    record = _alt_base(ctx, iid, token, item, out, now)
    record.update(cause=cause, why=why, door=door, notes=list(copy_notes))
    if ctx.detector:
        _tooling_gap(record, {"language": ctx.spec["language"]})
        record["notes"].append("--model is not read for a test that is not Python: nothing is mutated")
    if now.get("test_file_sha256") and cause == "model":
        record.update(test_file_sha256=now["test_file_sha256"], instance_content_sha=now["instance_content_sha"])
    if model:
        record.update(model=model["content"], model_sha=model["sha256"])
    _store_alternative(out, record, old, f"rerun after {old.get('verdict')}" if isinstance(old, dict) else "")
    return record


def _model_target(ctx: ProbeCtx, model: dict, run_cwd: Path, locks: list, copy_notes: list) -> tuple:
    """(the file the model lands in, whether it is the test file). A named other file must lie under a test root: a product file
    is `red_sandbox.py --probe`'s (it breaks the product in a throwaway copy). Its lock, and the recovery of a copy a dead probe
    left of it, come BEFORE its bytes are read as the original (R9)."""
    hint, _name = model_function_parts(model)
    if not hint:
        return ctx.path, True
    target = next((p for p in (ctx.root / hint, run_cwd / hint) if p.is_file()), None)
    if target is None:
        raise Refusal(f"the model's `function` names {hint}, which is no file under the project. Nothing was changed.")
    if target.resolve() == ctx.path.resolve():
        return ctx.path, True
    if not _in_test_root(ctx.cfg, _rel_project(target, ctx.root)):
        raise Refusal(f"the model's `function` names {hint}, which is not under a test root: a model in product code is "
                      f"`{RED_SANDBOX_DOOR}`, which breaks the product in a throwaway copy. Nothing was changed.")
    key, shown = copy_key(target, ctx.root)
    held = claim_key(ctx.root, key, shown, own=True, notes=copy_notes)
    if held is not None:
        locks.append(held)
    return target, False


def _reach_of(ctx: ProbeCtx, original: bytes, detail: dict, spans: list, model: dict, target_is_test: bool) -> tuple:
    """`model_reach` over the test's own bytes: (ok, why). A model in a helper function or file never has its reach shown."""
    _hint, wanted = model_function_parts(model)
    if not (target_is_test and wanted in ("", ctx.spec["function"])):
        return model_reach(None, (0, 0), spans, [], False)
    text = original[3:] if original.startswith(b"\xef\xbb\xbf") else original
    func = locate(ast.parse(text.decode("utf-8")), ctx.spec["chain"], ctx.spec["function"])
    return model_reach(func, tuple(detail["model_region"]), spans, _line_starts(text), True)


def _alternative_run_record(ctx: ProbeCtx, iid: str, token: str, item: dict, out: Path, now: dict, model: dict, refs: list,
                            detail: dict, test_bytes: bytes, original: bytes, target: Path) -> dict:
    """The record of a run that has not happened yet: `_new_record`'s (the fields `main`'s exit and print paths read keep their
    names: `mutated_file`, `test_file_sha256`, `expected_reason`, `record`), then the alternative's own."""
    record = _new_record(ctx, detail, now["instance_identity"], test_bytes, original, target)
    record.update(instance_id=iid, alternative=token, then=item["then"], reading=item["reading"],
                  reading_sha=now["reading_sha"], mutation_kind=ALTERNATIVE_KIND, proof_level=None,
                  expected_reason=f"alternative {token}", model=model["content"], model_sha=model["sha256"],
                  model_find=detail["model_find"], model_replace=detail["model_replace"], model_line=detail["model_line"],
                  assertion_refs=[[f, n] for f, n in refs], superseded=[], author_run_block=None,
                  record=out.relative_to(ctx.task_root).as_posix())
    return record


def _probe_alternative(ctx: ProbeCtx, locks: list, token: str, model_path: str, supersede, timeout: int) -> dict:
    """One alternative probe (`--mutation alternative`), called by `_probe` once the context is checked. Order and the invariant of
    each position: the declaration is read first and an undeclared ALT yields an ANSWER, never a record; a test that is not
    Python gets its `gap` before any byte is read; the model is validated before any lock; then the test's lock BEFORE its first
    read (R9), the target's lock before ITS first read; bindings and spans before the repeat check; the repeat check before any
    write; the byte copy before the mutation; the restore FROM the copy. Never a live receipt, never `publish_binding`."""
    case, alt = parse_alternative_token(token)
    task_root, root, case_cfg = ctx.task_root, ctx.root, C.case_config()
    iid = C.test_instance_id(ctx.entry) or ctx.instance_id
    item, why = declared_alternative(task_root, case, alt, case_cfg)
    if item is None:
        return _alt_answer("unknown", iid, token, why)
    out = alternative_record_path(task_root, iid, case, alt)
    old, _problem = _read_alt_record(out)
    if ctx.detector:
        language = ctx.spec["language"]
        return _alternative_gap_record(ctx, iid, token, item, out, old, cause="tooling", door=RED_SANDBOX_DOOR,
                                       why=f"substitution is Python-only: a {language} test cannot be modelled here",
                                       now={"reading_sha": _reading_sha(item)})
    model = load_model(task_root, model_path, token)
    _path, run_cwd = _test_path(root, ctx.cfg, ctx.spec, ctx.entry)
    _key, copy_notes = _lock_test(ctx, locks)
    if model["gap"]:
        now = alternative_now(ctx.entry, task_root, root, item, None)
        return _alternative_gap_record(ctx, iid, token, item, out, old, cause="model", why=model["gap"], now=now, model=model,
                                       copy_notes=copy_notes)
    target, target_is_test = _model_target(ctx, model, run_cwd, locks, copy_notes)
    test_bytes = ctx.path.read_bytes()
    manifest = C.load_json(ctx.manifest_path) if ctx.manifest_path.is_file() else {}
    refs = then_assertions(manifest, case, item["then"], ctx.entry, case_cfg)
    if not refs:
        return _alt_answer("unknown", iid, token, f"Then {item['then']} of {case} has no covered binding on {iid}")
    spans, why = assert_spans(test_bytes, ctx.spec, refs, ctx.path, root, run_cwd)
    if spans is None:
        return _alt_answer("unknown", iid, token, why)
    old_target = ((old or {}).get("mutated_file") or {}).get("path")     # the file the standing record ran on, if any
    now = alternative_now(ctx.entry, task_root, root, item, refs, str(old_target or _rel_project(target, root)))
    if now["test_file_sha256"] != sha256(test_bytes):
        raise Refusal(f"--test names {ctx.spec['file']}, which is not the file the manifest row of {iid!r} names "
                      f"({proof_level.test_file_of(ctx.entry) or 'none'}), or that file cannot be read: the probe binds its "
                      "record to the row's test. Nothing was changed.")
    fresh, stale_why = alternative_fresh(old, now) if old is not None else (False, "")
    if old is not None and fresh and supersede is None and old.get("verdict") in proof_level.PROBE_JUDGED_VERDICTS:
        return _already_probed(old, iid, token, copy_notes)
    reason = (str(supersede).strip() if supersede is not None else stale_why if old is not None and not fresh
              else f"rerun after {old.get('verdict')}" if old is not None else "")
    return _run_alternative(ctx, iid, token, item, out, old, now, model, refs, spans, target, target_is_test, test_bytes,
                            copy_notes, reason, timeout)


def _already_probed(old: dict, iid: str, token: str, copy_notes: list) -> dict:
    """The ANSWER of a repeat over the same bytes and reading: nothing runs, nothing is written."""
    return dict(_alt_answer("already_probed", iid, token,
                            f"{token} was already probed over these bytes and this reading: {old.get('verdict')} "
                            f"(record {old.get('record')}); --supersede \"<reason>\" runs it again with another model",
                            copy_notes), record=old.get("record"), prior_verdict=old.get("verdict"),
                recorded_at=old.get("recorded_at"))


def _run_alternative(ctx: ProbeCtx, iid: str, token: str, item: dict, out: Path, old, now: dict, model: dict, refs: list,
                     spans: list, target: Path, target_is_test: bool, test_bytes: bytes, copy_notes: list, reason: str,
                     timeout: int) -> dict:
    """The run half of `_probe_alternative`, entered only after the repeat check: the byte copy before the mutation, the restore
    FROM the copy, the record stored last."""
    task_root, root = ctx.task_root, ctx.root
    original = test_bytes if target_is_test else target.read_bytes()
    original_sha, stat = sha256(original), target.stat()
    mutated, detail = plan_alternative(original, ctx.spec, model, spans, target_is_test, name=target.name)
    changes, no_change_why = model_changes_value(model)
    if not changes:       # B-3: a model that changes code but not the value is the critic's non-model, never the author's defect
        return _alt_answer("unknown", iid, token, no_change_why + ": the Then cannot be shown to separate A from B by it",
                           copy_notes)
    reach = _reach_of(ctx, original, detail, spans, model, target_is_test)
    record = _alternative_run_record(ctx, iid, token, item, out, now, model, refs, detail, test_bytes, original, target)
    bound = author_binding(task_root, ctx.instance_id, record["instance_content_sha"])   # read ONCE, with the id the run uses
    author_green = None if bound is None else bound.get("status") == "passed"
    record.update(author_green=author_green, reach={"ok": reach[0], "why": reach[1]})
    record["notes"].extend(copy_notes)
    mutated_sha = sha256(mutated)
    judge = partial(_judge_alternative_row, spans=spans, author_green=author_green, reach=reach)
    copy = begin_copy(root, target, original, original_sha, stat, mutated_sha, detail, timeout)
    try:
        target.write_bytes(mutated)
        _run_and_judge(ctx, record, target, mutated_sha, original_sha, timeout, judge_row=judge,
                       request_stem="probe-alt-" + out.stem, mutation_kind=ALTERNATIVE_KIND, bound=bound,
                       reason=f"probe-{iid}: alternative {token} at {ctx.spec['file']}:{spans[0][0]} ({ctx.dispatch})")
    finally:
        # FROM the copy, verified; the copy is deleted only after the verification - the SAME path as `_probe`'s, never a second one
        record["restore"] = restore(target, original, original_sha, stat, copy=copy["orig"])
        finish_copy(copy, record["restore"], root)
    record["why"] = "; ".join(record.get("mismatches") or [])
    _store_alternative(out, record, old, reason)
    return record


# --- the report: what is owed, stale or proven ---------------------------------------------------------------------

def alternatives_report(task_root: Path, root: Path, instance=None) -> list:
    """[row]: one per declared alternative of every (instance, case) of the manifest, read-only. `state` is `proven`,
    `not_separated`, `wrong_location`, `gap`, `stale` (a fresher bytes/reading/binding than the record: never `proven`), `unknown`
    (no record, an unreadable one, one that names another case, instance or alternative, or an unjudged run), or `case_unreadable`
    (the case file is missing or its key is malformed: never read as "nothing owed", AR-28). A case with no key or `[]` has no row."""
    import s5_precheck as S5
    case_cfg = C.case_config()
    manifest_path = Path(task_root) / "work" / "automation-manifest.json"
    if not manifest_path.is_file():
        return [{"instance": "-", "case": "-", "then": None, "alternative": "-", "reading": "", "state": "case_unreadable",
                 "why": "the automation manifest is missing: no instance is listed", "record": None, "model_find": None,
                 "model_replace": None, "superseded": [], "flags": ""}]
    manifest = C.load_json(manifest_path)
    rows: list = []
    for entry in C.manifest_tests(manifest):
        aliases = C.instance_id_aliases(entry, case_cfg)
        if instance and instance not in aliases:
            continue
        iid = C.test_instance_id(entry) or (aliases[0] if aliases else "")
        for case in C.manifest_test_keys(entry, case_cfg):
            rows.extend(_case_rows(task_root, root, manifest, entry, iid, case, case_cfg, S5))
    return rows


def _case_rows(task_root: Path, root: Path, manifest: dict, entry: dict, iid: str, case: str, case_cfg, S5) -> list:
    def unreadable(why: str) -> list:
        return [{"instance": iid, "case": case, "then": None, "alternative": "-", "reading": "", "state": "case_unreadable",
                 "why": why, "record": None, "model_find": None, "model_replace": None, "superseded": [], "flags": ""}]
    file = S5._case_file_of(task_root, case, case_cfg)
    if file is None:
        return unreadable(f"case file of {case} not found")
    try:
        text = Path(file).read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        return unreadable(f"case file of {case} cannot be read ({type(exc).__name__})")
    entries, problem = C.alternatives_from_text(text)
    if entries is None:
        return unreadable(f"the `alternatives` key of {case} is malformed: {problem}") if problem else []
    shape = C.alternatives_errors(case, entries and json.dumps(entries), [n for n, _ in S5.then_clauses(text)])
    if shape:
        return unreadable(f"the `alternatives` key of {case} is malformed: {shape[0]}")
    return [_alt_row(task_root, root, manifest, entry, iid, case, item, case_cfg) for item in entries]


def _alt_row(task_root: Path, root: Path, manifest: dict, entry: dict, iid: str, case: str, item: dict, case_cfg) -> dict:
    token = f"{case}:{item['id']}"
    out = alternative_record_path(task_root, iid, case, item["id"])
    row = {"instance": iid, "case": case, "then": item["then"], "alternative": token, "reading": item["reading"],
           "state": "unknown", "verdict": None, "why": "", "record": None, "model_find": None, "model_replace": None,
           "superseded": [], "flags": ""}
    record, problem = _read_alt_record(out)
    if record is None:
        row["why"] = problem or "never probed"
    elif (record.get("instance_id"), record.get("case"), record.get("alternative")) != (iid, case, token):
        row["why"] = (f"the record names another case, instance or alternative ({record.get('case')}, "
                      f"{record.get('instance_id')}, {record.get('alternative')}), not this one")
    else:
        _judge_alt_row(row, record, task_root, root, manifest, entry, item, case, case_cfg, out)
    if row["state"] in ("unknown", "stale"):
        needs_model = str(proof_level.test_file_of(entry)).endswith(".py")
        row["flags"] = (f"--mutation alternative --alternative {token}"
                        + (" --model work/probe-models/<any name>.json" if needs_model else ""))
        if needs_model:
            row["skeleton"] = json.dumps({"alternative": token, "find": "<the line where the test reads the product's value>",
                                          "replace": "<that line under reading B>"}, ensure_ascii=False)
            row["skeleton_gap"] = json.dumps({"alternative": token, "gap": "<why B cannot be modelled in the test>"},
                                             ensure_ascii=False)
    return row


def _judge_alt_row(row: dict, record: dict, task_root: Path, root: Path, manifest: dict, entry: dict, item: dict, case: str,
                   case_cfg, out: Path) -> None:
    verdict = record.get("verdict")
    row.update(verdict=verdict, record=out.relative_to(task_root).as_posix(), model_find=record.get("model_find"),
               model_replace=record.get("model_replace"),
               superseded=[s.get("verdict") for s in record.get("superseded") or [] if isinstance(s, dict)])
    if verdict in ("not_executed", "incomplete"):
        row["why"] = f"the last probe was {verdict}: " + str(record.get("why") or (record.get("notes") or ["no reason recorded"])[0])
        return
    refs = then_assertions(manifest, case, item["then"], entry, case_cfg)
    mutated = record.get("mutated_file") if isinstance(record.get("mutated_file"), dict) else {}
    fresh, why = alternative_fresh(record, alternative_now(entry, task_root, root, item, refs, str(mutated.get("path") or "")))
    if not fresh:
        row.update(state="stale", why=why)
    elif verdict == "intended_failure":
        row.update(state="proven", why="the Then's own assert failed under reading B")
    elif verdict == "no_failure":
        row.update(state="not_separated", why="the Then passed under reading B: its assert does not separate A from B")
    elif verdict == "wrong_location":
        row.update(state="wrong_location", why=f"it failed elsewhere: {record.get('actual_location')}")
    elif verdict == "gap":
        row.update(state="gap", why=f"{record.get('cause')}: {record.get('why')}")
    else:
        row["why"] = f"the record's verdict {verdict!r} is not one this report knows"


def _print_alternatives(rows: list, json_mode: bool) -> None:
    if json_mode:
        print(json.dumps(rows, ensure_ascii=False, indent=1))
        return
    if not rows:
        print("no case of this story declares `alternatives`: nothing is owed")
    for row in rows:
        print(f"{row['instance']} {row['alternative'] if row['alternative'] != '-' else row['case']}"
              f"{' Then ' + str(row['then']) if row.get('then') is not None else ''}: {row['state']} - {row['why']}")
        if row["state"] in ("proven", "not_separated") and row.get("model_find") is not None:
            print(f"  model: {row['model_find']} -> {row['model_replace']}")
        if row.get("superseded"):
            print(f"  superseded: {len(row['superseded'])} (prior: {', '.join(str(v) for v in row['superseded'])})")
        if row.get("flags"):
            print(f"  add to the probe command: {row['flags']}")
        if row.get("skeleton"):
            print(f"  model file: {row['skeleton']}  or, when B cannot be modelled: {row['skeleton_gap']}")


def keep_standing_record(path: Path, record: dict) -> bool:
    """True when `record` is a run that judged NOTHING about the test (`not_executed`, or `incomplete`: the
    tool could not read the run well enough) and `path` holds an `intended_failure`: that stored record is
    kept, and only `last_attempt {at, verdict, why}` is added to it - `verdict` and `test_file_sha256` stay as
    they were. Invariant: an `intended_failure` record is replaced only by the record of a run that judged
    the test. A probe that never ran (a refused request, a stand that was down) used to overwrite it with
    `not_executed`, and the evidence that a probe had passed - the very thing `probe_debt.py` settles -
    vanished (t-177); an `incomplete` answer is a gap of the factory's, and costs the same. Any judged verdict
    (`no_failure`, `wrong_location`, `intended_failure`) replaces the record as before (E23)."""
    if record.get("verdict") not in ("not_executed", "incomplete"):
        return False
    try:
        stored = json.loads(Path(path).read_text(encoding="utf-8-sig"))
    except (OSError, ValueError):
        return False
    if not isinstance(stored, dict) or stored.get("verdict") != "intended_failure":
        return False
    notes = [str(n) for n in record.get("notes") or []]
    stored["last_attempt"] = {"at": record.get("recorded_at"), "verdict": record["verdict"],
                              "why": fold(notes[-1] if notes else "nothing ran", 300)}
    atomic_json(path, stored)
    return True


def _row_publish(entry: dict, ref: dict, task_root, iid: str, new_rank: int) -> tuple:
    """(what the row got: `kept: ...`, `replaced` or `added`; the `tests[]` fragment it needs, or None).
    Never a downgrade: a row ref that already resolves to a VALID receipt of a higher level is kept."""
    row_ref = (entry.get("sensitivity_proof") or {}).get("receipt_ref") \
        if isinstance(entry.get("sensitivity_proof"), dict) else None
    row_level = proof_level.valid_level(entry, row_ref, task_root)
    if proof_level.rank(row_level) > new_rank:
        return f"kept: the row already names a valid receipt that {proof_level.words(row_level)}", None
    return "replaced" if row_ref else "added", [{"instance_id": iid, "sensitivity_proof": {"receipt_ref": ref}}]


def _held_action(existing: dict, entry: dict, task_root, new_rank: int) -> str:
    """`set`, or `kept: ...` when the binding's receipt is a VALID one of a higher level (a file that is
    gone, another instance's receipt or bytes that moved hold nothing)."""
    held = str(existing.get("probe_receipt_ref") or "")
    held_file = task_root / held if held and not pathlib.Path(held).is_absolute() else None
    if existing.get("sensitivity") == "proven" and held_file is not None and held_file.is_file():
        held_level = proof_level.valid_level(
            entry, {"path": held, "sha256": sha256(held_file.read_bytes())}, task_root)
        if proof_level.rank(held_level) > new_rank:
            return f"kept: the binding already names a valid receipt that {proof_level.words(held_level)}"
    return "set"


def _binding_items(obligations: list, manifest: dict, entry: dict, task_root, iid: str, ref_path: str,
                   new_rank: int) -> tuple:
    """(the `obligation_bindings[]` items for the fragment, the rows `record["publish"]["bindings"]` gets).
    A binding's `instance_ids` is the union of what it lists and this instance, because `manifest_put.py`
    REPLACES that list and a second instance of one obligation would otherwise erase the first."""
    aliases = set(C.instance_id_aliases(entry)) | {iid}
    by_id = {str(b.get("obligation_id")): b for b in manifest.get("obligation_bindings") or []
             if isinstance(b, dict)}
    bindings, rows = [], []
    for oid in obligations:
        existing = by_id.get(oid) or {}
        # what the binding lists minus the rows a retraction took out on purpose
        ids = proof_level.without_retracted(existing.get("instance_ids"), manifest)
        if not aliases & set(ids):
            ids.append(iid)
        item = {"obligation_id": oid, "instance_ids": ids}
        action = _held_action(existing, entry, task_root, new_rank)
        if action == "set":
            item.update(sensitivity="proven", proof_kind="executed_red_probe", probe_receipt_ref=ref_path)
        bindings.append(item)
        rows.append({"obligation_id": oid, "instance_ids": ids, "receipt": action})
    return bindings, rows


def _put_fragment(task: str, fragment: dict) -> subprocess.CompletedProcess:
    """Run `manifest_put.py` over `fragment`. The fragment is scratch, not an artifact: it never lands in
    the story's own folder, where a guard and every later reader would treat it as one."""
    scratch = pathlib.Path(tempfile.mkdtemp(prefix="qa-probe-binding-"))
    try:
        path = scratch / "manifest-fragment.json"
        atomic_json(path, fragment)
        return subprocess.run([sys.executable, "-B", str(pathlib.Path(__file__).with_name("manifest_put.py")),
                               "--task", task, "--fragment", str(path)],
                              capture_output=True, text=True, encoding="utf-8", errors="replace")
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


def publish_binding(task: str, task_root, record: dict) -> str:
    """Publish this probe's live receipt in the two places it is read, through ONE
    `manifest_put.py` fragment: `tests[]` (`sensitivity_proof.receipt_ref`, which delivery and
    the ledger read) and the obligation bindings (`probe_receipt_ref`, which the review receipt and
    the coverage map read).

    `window_record.py` publishes a review receipt only when every instance of the window is
    reached by `obligation_bindings[].probe_receipt_ref`, and `red_sandbox.py --probe` writes that
    row itself. This script did not - it wrote `work/probes/<IID>.json` and stopped - while the
    code critic's brief names it as the ONLY probe the role may run. So a critic that obeyed its
    brief could never receipt its window: live TP1-13797, run 5, seven critic dispatches and
    $13.64 on a receipt that was unreachable by construction, with both probes already on disk and
    both `intended_failure`.

    Never a downgrade: a row ref or a binding ref that already resolves to a VALID receipt of a
    higher level (a `red_sandbox.py --probe` receipt) is kept; the same level is replaced (the new
    bytes' proof). A binding's `instance_ids` is the union of what it lists and this instance,
    because `manifest_put.py` REPLACES that list and a second instance of one obligation would
    otherwise erase the first. Everything the publish did goes into `record["publish"]` (FR-14).
    Only a probe that showed the intended failure and restored the author's bytes has a receipt, so
    nothing is published for any other. Returns what it did, for the caller's own output.
    """
    if record.get("verdict") != "intended_failure":
        return ""
    receipt = record.get("receipt")
    if not isinstance(receipt, dict) or not receipt.get("path"):
        why = ("the restore was not verified" if not (record.get("restore") or {}).get("verified")
               else "the facts a receipt binds are missing: " + ", ".join(record.get("receipt_missing") or [])
               if record.get("receipt_missing") else "the receipt could not be written")
        record["publish"] = {"published": False, "why": why}
        return f"no live receipt, nothing published ({why})"
    task_root = pathlib.Path(task_root)
    manifest_path = task_root / "work" / "automation-manifest.json"
    manifest = C.load_json(manifest_path) if manifest_path.is_file() else {}
    try:
        entry = manifest_entry(task_root, record["instance_id"])
    except Refusal as exc:
        record["publish"] = {"published": False, "why": str(exc)}
        return f"nothing published: {exc}"
    iid = C.test_instance_id(entry) or record["instance_id"]
    new_rank = proof_level.rank(proof_level.LIVE)
    ref = {"path": receipt["path"], "sha256": receipt["sha256"]}
    fragment: dict = {}

    row, tests = _row_publish(entry, ref, task_root, iid, new_rank)
    if tests:
        fragment["tests"] = tests
    obligations = [str(oid) for oid in (record.get("obligation_ids") or []) if oid]
    bindings, rows = _binding_items(obligations, manifest, entry, task_root, iid, ref["path"], new_rank)
    done: dict = {"published": True, "receipt": ref, "row": row, "bindings": rows}
    if bindings:
        fragment["obligation_bindings"] = bindings
    else:
        done["bindings_note"] = "no obligation_ids on this probe — the row is published, no binding"
    record["publish"] = done
    if not fragment:
        done["manifest_put"] = "nothing to put: a receipt of a higher level is already published"
        return done["manifest_put"]
    put = _put_fragment(task, fragment)
    from manifest_put import outcome
    put_kind, move = outcome(put.returncode, task)
    if put_kind == "stale":     # exit 4: the fragment IS in the journal, only the manifest's projection failed
        done["published"] = False
        done["manifest_put"] = f"committed, projection stale: {(put.stderr or put.stdout).strip()[-300:]}"
        return (f"manifest_put committed the publish but the manifest's projection is stale - run `{move}`; "
                f"the receipt stays at {ref['path']}")
    if put_kind == "refused":
        done["published"] = False
        done["manifest_put"] = f"refused: {(put.stderr or put.stdout).strip()[-300:]}"
        return f"manifest_put refused the publish, the receipt stays at {ref['path']}: {done['manifest_put']}"
    done["manifest_put"] = ((put.stdout or "").strip().splitlines() or ["ok"])[0]
    return (f"published {ref['path']}: row {done['row']}"
            + (f"; bound {', '.join(obligations)}" if obligations else "; no obligation ids to bind"))


def _tool_refusal_record(args, task_root: Path, exc: "ToolRefusal"):
    """The record `refused: tool` for this refusal, or None when it must not exist. Written only when everything proves the
    refusal is the tool's and the test is the instance's: the manifest names the instance, the `--test` file is the file of
    its row and is under the project, and - when the refusal does not prove the name (`name_unproved`: no declaration was found
    for it) - the row's `report_test_id` ends with the `--test` tail, as `run_shape_checks` reads it. A wrong call (a missing
    file, another instance's file, a name that is not the row's) gives None: the role does not write itself a gap by a wrong
    call (AR-22). Reads, writes nothing."""
    text = str(args.test or "").replace("\\", "/")
    if "::" not in text:
        return None
    file = text.split("::", 1)[0]
    try:
        entry = manifest_entry(task_root, args.instance)
    except Refusal:
        return None
    project = project_root().resolve()
    row_file = str(entry.get("file") or "").replace("\\", "/")
    if not row_file or not _same_file(row_file, file):
        return None
    try:
        path, _cwd = _test_path(project, load_config(), {"file": file}, entry)
    except Refusal:
        return None
    if exc.name_unproved:
        try:
            spec = parse_node(text, project)
        except Refusal:
            return None
        report_id = str(entry.get("report_test_id") or "").strip()
        if not report_id or not _tail_matches(report_id, spec["tail"], spec["entry"]):
            return None
    record = {"schema_version": 1, "probe_tool": "probe_by_code.py", "task": args.task, "instance_id": args.instance,
              "verdict": "not_executed", "refused": "tool", "test_file_sha256": sha256(path.read_bytes()),
              "recorded_at": datetime.now(timezone.utc).isoformat(timespec="seconds"), "notes": [str(exc)]}
    try:    # the tool's gap names its language the way `_tooling_gap` does (F-2 of t-596: ONE reader, `tooling_gap_key`); no entry: neither
        language, _entry = AD.entry_for_suffix(AD.assertion_detectors(), Path(file).suffix)
    except AD.DetectorsError:
        language = None
    if language:
        record["language"], record["cause"] = language, "tooling"
    return record


def _record_tool_refusal(args, task_root: Path, exc: "ToolRefusal") -> None:
    """Write the record of a tool refusal (`_tool_refusal_record`) at the probe's own path. An `intended_failure` stands
    (`keep_standing_record`). Any failure here is ONE line on stderr: the refusal's answer (one JSON, exit 2) never changes."""
    try:
        record = _tool_refusal_record(args, task_root, exc)
        if record is None:
            return
        out = record_path(task_root, args.instance)
        if not keep_standing_record(out, record):
            atomic_json(out, record)
    except Exception as err:    # noqa: BLE001 - the answer is already printed; the record is a convenience of the next reader
        print(f"probe_by_code: the record of this refusal was not written ({type(err).__name__}: {str(err)[:160]})",
              file=sys.stderr)


def _release_copy_cli(args) -> None:
    """`--release-copy`: nothing else runs. Exits 2 on a refusal (one JSON line), 0 once it printed what it
    released."""
    try:
        released = release_copy(project_root().resolve(), args.release_copy)
    except Refusal as exc:
        print(json.dumps({"status": "refused", "error": str(exc)}, ensure_ascii=False))
        sys.exit(2)
    if args.json:
        print(json.dumps(released, ensure_ascii=False, indent=1))
    else:
        print(released.get("message") or f"released the byte copy of {released['file']} ({released['copy']}); "
              f"its record was {json.dumps(released['record'], ensure_ascii=False)}")
    sys.exit(0)


def _print_record(record: dict, restored: bool, json_mode: bool) -> None:
    """What the CLI prints for a probe that ran: the whole record as one object with `--json`, else the
    two lines, the binding and the notes."""
    if json_mode:
        print(json.dumps(record, ensure_ascii=False, indent=1))
        return
    print(f"probe {record['instance_id']}: {record['verdict']} — expected {record['expected_location']} "
          f"/ {record['expected_reason']!r}; actual {record.get('actual_location')} / "
          f"{fold(record.get('actual_reason') or '', 120)!r}")
    print(f"record {record['record']}; evidence {record.get('evidence_ref')}; "
          f"restore {'verified' if restored else 'NOT VERIFIED'}")
    if record.get("binding"):
        print(f"binding: {record['binding']}")
    for note in record.get("notes") or []:
        print(f"note: {note}")


def _unrestored_exit(record: dict) -> None:
    """The author's bytes could not be verified restored: say so on stderr and exit 1, whatever the verdict."""
    # The copy is KEPT when the restore cannot be verified (R9 write order 7), and the line names
    # the one move that undoes the mutation: the file that was mutated is the oracle's when the
    # expectation lives in a helper, not always the test's.
    mutated_file = record.get("mutated_file") or {}
    file_rel = mutated_file.get("path") or record["test_node"].split("::")[0]
    copy_rel = (record.get("restore") or {}).get("copy")
    base = project_root().resolve()
    undo = (f"copy {(base / copy_rel)} over {(base / file_rel)}" if copy_rel
            else f"restore {file_rel} by hand")
    print(f"PROBE: the author's bytes of {file_rel} could not be verified restored "
          f"(sha256 {mutated_file.get('sha256') or record['test_file_sha256']}) — stop and {undo}",
          file=sys.stderr)
    sys.exit(1)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="the critic's red probe by code: mutate the first "
                                                 "assert of ONE test, run that node, restore, record")
    parser.add_argument("--task", help="the ticket id")
    parser.add_argument("--dispatch", help="the open qa-code-critic dispatch id")
    parser.add_argument("--s6-close", action="store_true", dest="s6_close",
                        help="driver only: the probe of the code close of S6, when no dispatch is open "
                             "(refused otherwise)")
    parser.add_argument("--test", help='"<file>::[Class::]<func>[<param>]" — the pytest node; for another '
                                       'language "<file>::<test name>" (the method, or the title)')
    parser.add_argument("--instance", help="the manifest instance id (contract.instance_id)")
    parser.add_argument("--release-copy", default="", metavar="FILE",
                        help="drop the byte copy a killed probe left of FILE (after its author settled the "
                             "file); nothing else runs. A copy whose record is unreadable is named by its "
                             "16-hex key instead of a file")
    parser.add_argument("--mutation", choices=MUTATIONS + (ALTERNATIVE,), default="invert",
                        help="invert: `assert not (<expr>)`; expected: a distinct literal of the same type; alternative: "
                             "the critic's model of a case's declared reading B (--alternative, --model)")
    parser.add_argument("--alternative", default=None, metavar="CASE:ALT-n",
                        help="with --mutation alternative: the declared reading to model, e.g. TC-001:ALT-1 "
                             "(`--alternatives` prints the token of every one)")
    parser.add_argument("--model", default=None, metavar="FILE",
                        help="with --mutation alternative: the model file under work/probe-models/ (a Python test)")
    parser.add_argument("--supersede", default=None, metavar="REASON",
                        help="with --mutation alternative: run again over a judged, fresh record with a new model; the "
                             "old verdict stays in `superseded[]` with this reason")
    parser.add_argument("--alternatives", action="store_true",
                        help="report only (needs --task; optional --instance, --json): every declared alternative with "
                             "its state and the flags to add; reads, writes nothing, exits 0")
    parser.add_argument("--oracle", default="",
                        help="[<file>::]<function> — the helper whose assert is this test's "
                             "expectation, when it lies further out than one hop")
    parser.add_argument("--at", type=int, default=None, metavar="LINE",
                        help="a test that is not Python: the line of the assertion to invert (the head whose "
                             "statement starts there) and, when the name is declared more than once, the "
                             "declaration whose body holds it")
    parser.add_argument("--timeout", type=int, default=RUN_TIMEOUT_S, help="seconds for the run")
    parser.add_argument("--json", action="store_true", help="print the probe record as JSON")
    return parser


def _refuse_alternative_args(args) -> None:
    """The flags of the alternative probe, checked in `main` before anything is read (exit 2): they mean something only together."""
    if args.mutation != ALTERNATIVE:
        for flag, value in (("--alternative", args.alternative), ("--model", args.model), ("--supersede", args.supersede)):
            if value is not None:
                raise Refusal(f"{flag} belongs to --mutation alternative: add it, or drop {flag}. Nothing was changed.")
        return
    if not args.alternative:
        raise Refusal("--mutation alternative needs --alternative <case>:ALT-n (`probe_by_code.py --task <TICKET> "
                      "--alternatives` prints the token of every declared reading). Nothing was changed.")
    if args.oracle or args.at is not None:
        raise Refusal("an alternative is modelled by --model, not found by --oracle or --at: drop them. Nothing was changed.")
    if args.supersede is not None and not 1 <= len(args.supersede.strip()) <= SUPERSEDE_REASON_MAX:
        raise Refusal(f"--supersede wants a reason of 1 to {SUPERSEDE_REASON_MAX} characters (the old verdict stays visible "
                      "beside it). Nothing was changed.")


def _alternatives_cli(args) -> None:
    """`--alternatives`: the report, read-only, exit 0 (P1: code tells, never stops). A story that does not exist is refused as
    everywhere else (CX1-18)."""
    try:
        task_root = story_root(args.task, "probe_by_code.py --task")
    except ValueError as exc:
        print(json.dumps({"status": "refused", "error": str(exc)}, ensure_ascii=False))
        sys.exit(2)
    _print_alternatives(alternatives_report(Path(task_root), project_root().resolve(), args.instance), args.json)
    sys.exit(0)


def _finish_alternative(args, record: dict) -> None:
    """Print what an alternative probe answered and exit. Never `publish_binding` (an alternative record is never a live receipt).
    An unverified restore of the author's file is the loudest alarm and is reported first (`_unrestored_exit`); a `gap` or an
    `unknown` answer ran nothing, has no restore and is not an unrestored file."""
    verdict = record.get("verdict")
    if record.get("restore") is not None:
        restored = bool((record.get("restore") or {}).get("verified"))
        _print_record(record, restored, args.json)
        if not args.json:
            print(f"alternative {record['alternative']}: {record.get('why') or 'see the notes'}")
        if not restored:
            _unrestored_exit(record)
    elif args.json:
        print(json.dumps(record, ensure_ascii=False, indent=1))
    else:
        print(f"probe {record['instance_id']} {record['alternative']}: {verdict} — {record.get('why')}")
        if record.get("record"):
            print(f"record {record['record']}")
        if record.get("door"):
            print(f"door: {record['door']}")
        for note in record.get("notes") or []:
            print(f"note: {note}")
    sys.exit(0 if verdict in {"intended_failure", "no_failure", "wrong_location"} else 1)


def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()
    if args.release_copy:
        _release_copy_cli(args)
    if args.alternatives:
        if not args.task:
            parser.error("the following arguments are required: --task")
        _alternatives_cli(args)
    if args.s6_close and args.dispatch:
        parser.error("use one: --dispatch <id> (an open dispatch) or --s6-close (the code close of S6)")
    # the role's text names `--dispatch` alone: the driver's door (`--s6-close`) is not shown to the critic
    absent = [name for name in ("task", "dispatch", "test", "instance")
              if not getattr(args, name) and not (name == "dispatch" and args.s6_close)]
    if absent:
        parser.error("the following arguments are required: " + ", ".join("--" + name for name in absent))
    try:
        _refuse_alternative_args(args)     # a misuse of the alternative flags is refused before even the story is looked at
        # FIRST, before the probe reads or mutates anything: the story must EXIST (CX1-18), else the person would be
        # sent to a manifest door of a story that is not there. The same root serves the two writes below.
        try:
            root = story_root(args.task, "probe_by_code.py --task")
        except ValueError as exc:
            raise Refusal(str(exc)) from exc
        # the alternative probe's own values go to `probe()` only for that probe: every other call is the call it always was
        extra = ({"alternative": args.alternative, "model": args.model or "", "supersede": args.supersede}
                 if args.mutation == ALTERNATIVE else {})
        record = probe(args.task, args.dispatch or "", args.test, args.instance, args.mutation,
                       args.timeout, args.oracle, args.at, s6_close=args.s6_close, **extra)
    except ToolRefusal as exc:
        # BEFORE `Refusal`: the same one JSON and exit 2, and the record `refused: tool` beside them (the producer of the field);
        # an alternative probe leaves none: that record's path is the INVERT probe's
        print(json.dumps({"status": "refused", "error": str(exc)}, ensure_ascii=False))
        if args.mutation != ALTERNATIVE:
            _record_tool_refusal(args, root, exc)
        sys.exit(2)
    except Refusal as exc:
        print(json.dumps({"status": "refused", "error": str(exc)}, ensure_ascii=False))
        sys.exit(2)
    if record.get("verdict") == "already_probed":
        # Answered, not probed: before `publish_binding` and before the restore check, because nothing
        # was mutated, launched or written - there is nothing to publish and nothing to restore. Exit 0:
        # the test HAS a probe; asking again is not a failure of anyone.
        if args.json:
            print(json.dumps(record, ensure_ascii=False, indent=1))
        else:
            print(f"probe {record['instance_id']}: already_probed — {record['words']}")
            for note in record.get("notes") or []:
                print(f"note: {note}")
        sys.exit(0)
    if args.mutation == ALTERNATIVE:
        _finish_alternative(args, record)
    restored = bool((record.get("restore") or {}).get("verified"))
    # Inside the record, never as an extra line: with `--json` the whole of stdout is one
    # object, and a human-readable line after it turned every field of the parsed record
    # into None for the caller (caught by test_probe_by_code the same minute).
    bound = publish_binding(args.task, root, record)
    if bound:
        record["binding"] = bound
    if record.get("publish"):
        try:  # what the publish did belongs in the probe's own record too (FR-14)
            atomic_json(root / record["record"], record)
        except OSError as exc:
            record["notes"].append(f"the publish could not be written into the record: {exc}")
    _print_record(record, restored, args.json)
    if not restored:
        _unrestored_exit(record)
    sys.exit(0 if record["verdict"] in {"intended_failure", "no_failure", "wrong_location"} else 1)


if __name__ == "__main__":
    main()
