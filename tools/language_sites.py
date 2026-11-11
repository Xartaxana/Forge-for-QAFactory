"""One-road ratchet -- no new branch on a language, framework, report format or named project in the package's
Python reaches the branch unseen (spec t-2065, node TR2-15, owner's words 06.11.2026: «Нигде не должно быть таких
исключений для каких-то языков, проектов или случаев. Это пораждает баги фабрики»).

INERT until wired (node N3): no hook, no CI line calls it; it runs by hand. A SITE is a place in a package script
(ai-packages/qa-factory/, tests excluded) where code takes a different road for a token, by AST, in one of these forms:
`compare`, `name-call`, `regex`, `parser`, `table-key`, `predicate-call`. Key `<path>|<qualname>|<form>|<token>`, a
count; NO line number in a key. The baseline is tools/language-sites-baseline.json (rows, tokens, predicates, and
`predicate_roots`: the parser-rooted subset a staged run seeds its carrying chain from).
Tokens are DATA: the baseline's `tokens` plus the suffixes and keys of references/detectors.json `assertion_probes`
plus references/test-path-markers.json `code_extensions`, all read in this tool (a second reader of that shape: the
package's own reader cannot be imported from tools/).

Commands (no `--update`: a raise written by a command is the cheap way past):
  --check --staged             the index against HEAD; staged scripts, or the whole scan when a token grows
  --check [--base REF]         the whole package in the working tree; with --base also C3 and C5
  --check --rev REF [--base R] the same, reading the package and the baseline as blobs of REF
  --raises --base REF          row by row: added, raised, moved, relabelled, re-mechanised, reworded, basis changes
  --totals                     rows and counts by kind and mechanism, files scanned, wall time
  --shrink                     drops stale rows and lowers counts; NEVER adds or raises
  --predicates                 writes the recomputed predicate list, prints what grew and fell; NEVER writes a row
  --init                       first fill only: refuses when the baseline exists
  --repo PATH                  the repository root (default: the parent of tools/), for tests and odd checkouts

Checks: C1 new or grown; C2 stale; C3 row vs base (fields of the kind, a new word/reason on a raise, relabel,
MOVE rules); C3b the word (who, quote of 12+ characters, a tracked carrier that is not the baseline, the quote stands
in it); C4 baseline shape; C5 basis (scan, tokens, predicates narrowed vs base, without `basis_word`); C6 stored
predicates vs the fixpoint (whole mode); C7 a script that does not parse. Exit: 0 pass, 1 red, 2 cannot judge
(missing or unreadable input, unresolvable base, empty scan: an unknown is never a pass, AR-28).

Error direction (designer rule 1): it errs toward OVER-reporting. A false stop costs one row with a reason or a data
row; a false pass is the owner's complaint. The tool judges data (shape, joins, presence), never whether a word is the
owner's or a reason is good (AR-29): that is the critic's, accepted by the Lead.

KNOWN MISSES (pinned as tests that assert NOT detected, each has a named owner; check 42 counts findings of the class):
  1. A language SHAPE with no token and no regex: `startswith("#")`. Critic question 12.
  2. A constant imported from another module; a token built at run time. Critic.
  3. A function with non-bool returns that branches on a token and returns no parser result: callers not flagged.
  4. A branch inverted or its body changed in place: same key, same count. Critic question 12.
  5. A road by absence: code that never handles the other language and branches on nothing. Critic; TR2-16.
  6. Text: references/test-code-patterns.md, charters. Critic.
  7. A branch on a project not in the `project` family, or on a case: a case has no code shape. Critic.
  8. A trade inside one file: one road removed, another added, same (form, token, mechanism). Critic question 9.
  9. A bare short form: `ext == "py"`, `"ts"`. Critic.
 10. A predicate called through an object of unknown type, or a module imported dynamically. Critic.
 11. A cross-file road row with an honest-looking `moved_from` over what is really a new road: printed, never red.
 12. A token held by a function-local constant, a class attribute or a local pattern variable (only module constants
     are read). Critic.
 13. A call target through a dotted module path (`import pkg.er; pkg.er.is_p(c)`), `compile(s, "f", "exec",
     ast.PyCF_ONLY_AST)`, `from ast import *`. Critic.
 14. A regex whose shape is a word the `syntax` family does not list. Critic question 12.
Closed in round t-2092 (were misses): `+`/`|` of collections, multi-target and tuple assignment, a conditional's arms;
regex `[.]`, `\\.(a|b)` and `\\.pyi?`; `re.findall/finditer/subn`; `find/count/index/removeprefix`; `case {"k": v}`;
`dict(k=1)`; a predicate named without a call; the words `require using function class func include` in a regex.
"""
from __future__ import annotations

import argparse
import ast
import json
import os
import posixpath
import re
import sys
import time
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import gitcmd

REPO = Path(__file__).resolve().parent.parent
PACKAGE_ROOT = "ai-packages/qa-factory/"
BASELINE_REL = "tools/language-sites-baseline.json"
DETECTORS_NAME = "references/detectors.json"
MARKERS_NAME = "references/test-path-markers.json"
DEFAULT_SCAN = {"root": PACKAGE_ROOT, "exclude": [PACKAGE_ROOT + "scripts/tests/"]}
DEFAULT_TOKENS = {
    "suffix": [".py", ".pyi"],
    "language": ["python", "typescript", "javascript", "java", "csharp"],
    "runner": ["pytest", "unittest", "playwright", "jest", "vitest", "mocha", "cypress", "mvn", "gradle", "dotnet",
               "npx", "xunit", "nunit", "testng", "rspec", "python3"],
    "format": ["trx", "junit-xml"],
    "parser": ["ast.parse", "tokenize", "libcst", "parso", "tree_sitter"],
    "project": ["mybooks", "testproject1", "example"],
    "syntax": ["import", "from", "def", "require", "using", "function", "class", "func", "include"],
}
DEFAULT_MECHANISMS = {
    "M1": "S5 exit gate reads only Python test files", "M2": "judge and repo map", "M3": "live check",
    "M4": "execution", "M5": "cosmetic classifier and code sha", "M6": "manifest writing", "M7": "other readers",
    "M8": "found at first fill, no census row", "OWN": "the factory's own Python",
    "FLOOR": "a declared floor under a data row"}
SINCE_DEFAULT = "t-2065"
LITERAL_FAMILIES = ("suffix", "language", "runner", "format", "project")
KINDS = ("road", "own-code", "floor")
FORMS = ("compare", "name-call", "regex", "parser", "table-key", "predicate-call")
NAME_CALL_ATTRS = {"endswith", "startswith", "removesuffix", "removeprefix", "match", "glob", "rglob", "find", "rfind",
                   "index", "rindex", "count"}
REGEX_FUNCS = {"compile", "match", "search", "fullmatch", "sub", "subn", "split", "findall", "finditer"}
BOOL_CALLS = {"endswith", "startswith", "isinstance", "issubclass", "bool", "any", "all"}
COLLECTION_CTORS = {"frozenset", "set", "tuple", "list", "sorted"}
MIN_QUOTE = 12
MAX_SHOWN = 25

REFUSAL_TAIL = """Why it stops: one action by a different road for a language, project or case is a defect that
breeds factory bugs (PROJECT.md P31, docs/SIBLING_MAP.md axis 33).
Expected: no such branch here, or a row for this key. Doors:
  1. A data row: put the difference in a table and read it by a capability key, not by the
     language's name (references/detectors.json through scripts/assertion_detectors.py, AR-1).
     The site then disappears and no row is owed.
  2. The owner's word: a row in tools/language-sites-baseline.json with kind `road` and
     word {who, date, quote, carrier}; the quote (12 characters or more) must stand in the carrier
     file, and the carrier is not the baseline. A raised row needs a new quote. Only the owner gives
     this word: a coordinator or a builder asks her, in plain words, with the options.
  3. Not a language road (the factory reading its own Python, a declared floor): a row with kind
     `own-code` or `floor` and a `reason`; a raised row needs a new reason; the critic of the merge
     reads it.
If the site moved inside a file: move its row, keep its mechanism and word. Across files: name the
old key in `moved_from` too."""
ROW_DOOR = ("Door: edit the row in tools/language-sites-baseline.json (kind `road` needs the owner's word "
            "{who, date, quote, carrier}, asked in plain words; `own-code` and `floor` need a `reason` the critic reads).")


class CannotJudge(Exception):
    """Exit 2: an input is missing or unreadable, the base does not resolve, the scan is empty (AR-28)."""


class Unread:
    """A blob git failed to give (not an absent one): carries the first line of git's reason."""

    def __init__(self, reason):
        self.reason = reason


# ---------------------------------------------------------------------------------------------- sources
ABSENT_MARKERS = ("does not exist in", "exists on disk, but not in", "fatal: path")


def _git_blob(repo, spec):
    """bytes of `git show <spec>`; None when there is no such blob; an Unread when git failed otherwise."""
    code, raw, err = gitcmd.git(repo, "show", spec, stderr=True)
    if code == 0:
        return raw
    reason = gitcmd.as_text(err).strip().split("\n")[0] if err else ""
    if code == 128 and any(m in reason for m in ABSENT_MARKERS):
        return None
    if spec.startswith("HEAD:"):                  # the first commit: no HEAD, so nothing in it
        vcode, _ = gitcmd.git(repo, "rev-parse", "--verify", "-q", "HEAD")
        if vcode == 1:
            return None
    return Unread(reason or "git show %s exited %d" % (spec, code))


def _git_lines(repo, *args):
    code, raw, err = gitcmd.git(repo, *args, stderr=True)
    if code != 0:
        raise CannotJudge("git %s failed: %s" % (" ".join(args[:2]), (gitcmd.as_text(err).strip().split("\n") or [""])[0]
                                                  or "exit %d" % code))
    return [x for x in raw.decode("utf-8", "replace").split("\0") if x]


class Source:
    """Reads a tree: the file listing under a prefix, the bytes of a file. One reader for the working tree, the
    index and a revision, so that every mode judges through the same scan."""
    threaded = True

    def __init__(self, repo):
        self.repo = Path(repo)

    def tracked(self, rel):
        code, raw = gitcmd.git(self.repo, "ls-files", "-z", "--", rel)
        if code != 0:
            return Unread("git ls-files exited %d" % code)
        return bool(raw.strip(b"\0"))

    def listing(self, prefix):
        raise NotImplementedError

    def read(self, rel):
        raise NotImplementedError


class TreeSource(Source):
    threaded = False

    def listing(self, prefix):
        top = self.repo / prefix.rstrip("/")
        out = []
        for dirpath, dirnames, filenames in os.walk(top):
            dirnames[:] = [d for d in dirnames if d not in (".git", "__pycache__")]
            for name in filenames:
                full = Path(dirpath) / name
                out.append(full.relative_to(self.repo).as_posix())
        return sorted(out)

    def read(self, rel):
        try:
            return (self.repo / rel).read_bytes()
        except (FileNotFoundError, NotADirectoryError):
            return None
        except OSError as exc:
            return Unread(str(exc))


class IndexSource(Source):
    def listing(self, prefix):
        return sorted(_git_lines(self.repo, "ls-files", "-z", "--", prefix))

    def read(self, rel):
        return _git_blob(self.repo, ":" + rel)


class RevSource(Source):
    def __init__(self, repo, ref):
        super().__init__(repo)
        self.ref = ref

    def listing(self, prefix):
        if self.ref == "HEAD" and gitcmd.git(self.repo, "rev-parse", "--verify", "-q", "HEAD")[0] == 1:
            return []
        return sorted(_git_lines(self.repo, "ls-tree", "-r", "--name-only", "-z", self.ref, "--", prefix))

    def read(self, rel):
        return _git_blob(self.repo, "%s:%s" % (self.ref, rel))

    def tracked(self, rel):
        blob = self.read(rel)
        return blob if isinstance(blob, Unread) else blob is not None


def read_many(src, paths):
    """{path: bytes | None | Unread}; threaded for the git-backed sources (one subprocess per blob)."""
    if not src.threaded or len(paths) < 4:
        return {p: src.read(p) for p in paths}
    with ThreadPoolExecutor(max_workers=8) as pool:
        return dict(zip(paths, pool.map(src.read, paths)))


def decode(blob):
    return blob.decode("utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")


# ---------------------------------------------------------------------------------------------- tokens
_SUFFIX_TAIL = re.compile(r"(?:\[[^\]]*\]|[$)?])+$")
_WORD_L, _WORD_R = r"(?<![A-Za-z0-9_])", r"(?![A-Za-z0-9_])"
_DOT_GROUP = re.compile(r"\\\.\((?:\?:)?([^()]*)\)")        # `\.(py|ts)`: group 1 is the alternatives


class Tokens:
    """The token union as data. `literal(s)` is the match for a string compared, passed to endswith/glob or used as
    a key; `regex(p)` is the match inside a regex pattern (the `syntax` family counts only there)."""

    def __init__(self, fams):
        self.fams = {f: sorted({str(t).lower() for t in v}) for f, v in fams.items()}
        self.suffix = [t for t in self.fams.get("suffix", [])]
        words = []
        for fam in LITERAL_FAMILIES:
            if fam != "suffix":
                words += self.fams.get(fam, [])
        words = sorted(set(words))
        self.words = [(w, re.compile(_WORD_L + re.escape(w) + _WORD_R)) for w in words]
        # a syntax word (`def`, `class`, `function`) counts in a regex only when whitespace follows it, directly or after
        # the rest of its alternation and closing `)`/`|` only: `def\s+`, `^function\s`, `(?:def|class)\s+` (both words),
        # `\b(?:def|func)\b` match; `bug-class):`, `|class|`, `^function\(` do not (an English word is not a grammar)
        self.syntax = [(w, re.compile(_WORD_L + re.escape(w) + r"(?=(?:\|[\w-]+)*[)|]*\s)"))
                       for w in self.fams.get("syntax", [])]
        self.suffix_re = [(t, re.compile(re.escape(t) + _WORD_R)) for t in self.suffix]
        self.parser = list(self.fams.get("parser", []))

    def literal(self, s):
        s = s.lower()
        core = _SUFFIX_TAIL.sub("", s)
        out = [t for t in self.suffix if core.endswith(t)]
        out += [w for w, rx in self.words if rx.search(s)]
        return out

    def regex(self, pat):
        pat = pat.replace("[.]", "\\.").replace("[\\.]", "\\.")
        pat = _DOT_GROUP.sub(lambda m: "|".join("\\." + a for a in m.group(1).split("|")), pat)
        n = re.sub(r"\\[A-Za-z]", " ", pat)
        n = re.sub(r"\\(.)", r"\1", n, flags=re.S).lower()
        out = []
        for v in (re.sub(r"(\w)\?", r"\1", n), re.sub(r"\w\?", "", n)):      # `\.pyi?` holds `.pyi` and `.py`
            out += [t for t, rx in self.suffix_re if rx.search(v)]
            out += [w for w, rx in self.words if rx.search(v)]
            out += [w for w, rx in self.syntax if rx.search(v)]
        return list(dict.fromkeys(out))


def data_tokens(src, root, required):  # `root` is the package root: the data files do not move when the scan root is narrowed
    """{'suffix': [...], 'language': [...]} from the two data files. Missing or malformed: CannotJudge when
    `required` (never 'no extra tokens'); an absent file at a base is empty, a malformed one still cannot be judged."""
    fams = {"suffix": set(), "language": set()}
    for name, kind in ((DETECTORS_NAME, "detectors"), (MARKERS_NAME, "markers")):
        rel = root + name
        blob = src.read(rel)
        if isinstance(blob, Unread):
            raise CannotJudge("%s could not be read: %s" % (rel, blob.reason))
        if blob is None:
            if required:
                raise CannotJudge("%s is missing: the token union cannot be built, and an unknown is not 'no extra "
                                  "tokens'" % rel)
            continue
        try:
            data = json.loads(decode(blob))
            if kind == "detectors":
                probes = data["assertion_probes"]
                if not isinstance(probes, dict):
                    raise TypeError("assertion_probes is not an object")
                for lang, row in probes.items():
                    fams["language"].add(str(lang))
                    for suf in row["suffixes"]:
                        if not isinstance(suf, str):
                            raise TypeError("a suffix is not a string")
                        fams["suffix"].add(suf)
            else:
                exts = data["code_extensions"]
                if not isinstance(exts, list) or not all(isinstance(x, str) for x in exts):
                    raise TypeError("code_extensions is not a list of strings")
                fams["suffix"].update(exts)
        except (ValueError, KeyError, TypeError, AttributeError) as exc:
            raise CannotJudge("%s is malformed (%s): the token union cannot be built" % (rel, exc))
    return {k: sorted(v) for k, v in fams.items()}


def effective_tokens(doc, src, required=True):
    """The union: the baseline's tokens plus the two data files'. {family: [tokens]}."""
    union = {f: set(map(str.lower, v)) for f, v in doc["tokens"].items()}
    for fam, toks in data_tokens(src, PACKAGE_ROOT, required).items():
        union.setdefault(fam, set()).update(t.lower() for t in toks)
    return {f: sorted(v) for f, v in union.items()}


def token_pairs(fams):
    return {(f, t) for f, v in fams.items() for t in v}


# ---------------------------------------------------------------------------------------------- analysis
class CollList(list):
    """The values of a collection (a tuple, list or set): `+` and `|` of two of them unite, never concatenate."""


def literals(node, consts, depth=0):
    """The string values an expression can hold, read from the code (constants, collections of them, f-strings with a
    NUL for each hole, `+` and `|` of collections, `+`, `%`, `.format`, a conditional's two arms, same-file module
    constants). A CollList is a collection's values."""
    if depth > 6:
        return []
    t = type(node)
    if t is ast.Constant:
        return [node.value] if isinstance(node.value, str) else []
    if t in (ast.Tuple, ast.List, ast.Set):
        out = CollList()
        for e in node.elts:
            out += literals(e, consts, depth + 1)
        return out
    if t is ast.IfExp:
        return literals(node.body, consts, depth + 1) + literals(node.orelse, consts, depth + 1)
    if t is ast.JoinedStr:
        return ["".join(v.value if isinstance(v, ast.Constant) and isinstance(v.value, str) else "\0"
                        for v in node.values)]
    if t is ast.BinOp:
        if isinstance(node.op, (ast.Add, ast.BitOr)):
            left, right = literals(node.left, consts, depth + 1), literals(node.right, consts, depth + 1)
            if isinstance(left, CollList) or isinstance(right, CollList) or isinstance(node.op, ast.BitOr):
                return CollList(list(left) + list(right))
            return [a + b for a in left[:4] for b in right[:4]] if left and right else []
        if isinstance(node.op, ast.Mod):
            return literals(node.left, consts, depth + 1)
        return []
    if t is ast.Name:
        v = consts.get(node.id, ())
        return CollList(v) if isinstance(v, CollList) else list(v)
    if t is ast.Call:
        f = node.func
        if isinstance(f, ast.Name) and f.id in COLLECTION_CTORS and len(node.args) == 1 and not node.keywords:
            return CollList(literals(node.args[0], consts, depth + 1))
        if (isinstance(f, ast.Attribute) and f.attr == "format" and isinstance(f.value, ast.Constant)
                and isinstance(f.value.value, str)):
            return [f.value.value]
    return []


def _const_pairs(st):
    """[(name, value node)] a module-level statement binds: `A = x`, `A = B = x`, `A, B = x, y`, `A: T = x`."""
    if isinstance(st, ast.AnnAssign):
        return [(st.target.id, st.value)] if isinstance(st.target, ast.Name) and st.value is not None else []
    if not isinstance(st, ast.Assign):
        return []
    pairs = []
    for tgt in st.targets:
        if isinstance(tgt, ast.Name):
            pairs.append((tgt.id, st.value))
        elif (isinstance(tgt, (ast.Tuple, ast.List)) and isinstance(st.value, (ast.Tuple, ast.List))
              and len(tgt.elts) == len(st.value.elts)):
            pairs += [(a.id, b) for a, b in zip(tgt.elts, st.value.elts) if isinstance(a, ast.Name)]
    return pairs


def module_consts(tree):
    consts = {}
    for st in tree.body:
        for name, value in _const_pairs(st):
            vals = literals(value, consts)
            if vals and not isinstance(value, ast.Dict):
                consts[name] = vals
    return consts


class FuncInfo:
    __slots__ = ("qual", "kind", "cls", "sites", "calls", "ret_ok", "carry")

    def __init__(self, qual, kind, cls):
        self.qual, self.kind, self.cls = qual, kind, cls
        self.sites = []                       # (form, token, line) -- everything but a predicate-call
        self.calls = defaultdict(list)        # resolved callee name -> [line]
        self.ret_ok = None                    # None: no return; else a list of bool structures
        self.carry = False                    # a structure: does a return carry a parser result


class FileInfo:
    def __init__(self, path, absent=False):
        self.path = path
        self.stem = posixpath.basename(path)[:-3] if path.endswith(".py") else posixpath.basename(path)
        self.error = None
        self.absent = absent
        self.funcs = {}
        self.parser_classes = set()


class Resolver:
    """Calls resolved through the file's imports only (spec 2.2): a bare name defined in the file or brought by
    `from m import f [as g]`; an attribute on an alias of a module; `self.f` inside the class."""

    def __init__(self, stem, tokens):
        self.stem, self.tokens = stem, tokens
        self.mod, self.frm, self.defs = {}, {}, set()

    def resolve(self, f, cls):
        if isinstance(f, ast.Name):
            n = f.id
            if n in self.defs:
                return "%s.%s" % (self.stem, n)
            if n in self.frm:
                m, orig = self.frm[n]
                return "%s.%s" % (m.rsplit(".", 1)[-1], orig) if m else None
            return None
        if isinstance(f, ast.Attribute) and isinstance(f.value, ast.Name):
            a, x = f.value.id, f.attr
            if a in ("self", "cls") and cls:
                return "%s.%s.%s" % (self.stem, cls, x)
            if a in self.mod:
                return "%s.%s" % (self.mod[a].rsplit(".", 1)[-1], x)
            if a in self.frm:
                return "%s.%s" % (self.frm[a][1], x)
            if a in self.defs:
                return "%s.%s.%s" % (self.stem, a, x)
        return None

    def _chain(self, f):
        attrs = []
        while isinstance(f, ast.Attribute):
            attrs.append(f.attr)
            f = f.value
        attrs.reverse()
        return (f.id if isinstance(f, ast.Name) else None), attrs

    def module_of(self, f):
        """(module dotted name, attrs after it) for a call target, or (None, [])."""
        root, attrs = self._chain(f)
        if root is None:
            return None, []
        if root in self.mod:
            return self.mod[root], attrs
        if root in self.frm:
            m, orig = self.frm[root]
            return m, [orig] + attrs
        return None, []

    def re_func(self, f):
        mod, attrs = self.module_of(f)
        if mod == "re" and len(attrs) == 1 and attrs[0] in REGEX_FUNCS:
            return attrs[0]
        return None

    def parser_tokens(self, call, consts):
        """Tokens of the `parser` family this call is: a module call through any alias, a dynamic import or getattr."""
        ptoks = self.tokens.parser
        if not ptoks:
            return []
        f = call.func
        mod, attrs = self.module_of(f)

        def by_module(modname, first_attr, ignore_attr):
            root = modname.split(".")[0]
            out = []
            for t in ptoks:
                tm, _, ta = t.partition(".")
                if root == tm or root.startswith(tm + "_"):
                    if ta == "" or ignore_attr or first_attr == ta:
                        out.append(t)
            return out

        if isinstance(f, ast.Name) and f.id == "getattr" and len(call.args) >= 2:
            lit = literals(call.args[1], consts)
            base = call.args[0]
            if isinstance(base, ast.Name) and base.id in self.mod and lit:
                got = by_module(self.mod[base.id], lit[0], False)
                if got:
                    return got
            return [t for s in lit for t in self.tokens.literal(s)] if lit else []
        dynamic = (isinstance(f, ast.Name) and f.id == "__import__") or (mod == "importlib" and attrs == ["import_module"])
        if dynamic and call.args:
            lit = literals(call.args[0], consts)
            out = []
            for s in lit:
                got = by_module(s, None, True)
                out += got if got else self.tokens.literal(s)
            return out
        if mod is not None:
            return by_module(mod, attrs[0] if attrs else None, False)
        return []

    def bool_struct(self, e, cls):
        if isinstance(e, ast.Constant):
            return isinstance(e.value, bool)
        if isinstance(e, ast.UnaryOp):
            return isinstance(e.op, ast.Not)
        if isinstance(e, ast.Compare):
            return True
        if isinstance(e, ast.BoolOp):
            return ("all", [self.bool_struct(v, cls) for v in e.values])
        if isinstance(e, ast.IfExp):
            return ("all", [self.bool_struct(e.body, cls), self.bool_struct(e.orelse, cls)])
        if isinstance(e, ast.Call):
            f = e.func
            name = f.attr if isinstance(f, ast.Attribute) else (f.id if isinstance(f, ast.Name) else "")
            if name in BOOL_CALLS or name.startswith("fnmatch"):
                return True
            cand = self.resolve(f, cls)
            return ("pc", cand) if cand else False
        return False

    def carry_struct(self, e, assigns, cls, consts, depth=0):
        if isinstance(e, ast.Tuple):
            return ("any", [self.carry_struct(x, assigns, cls, consts, depth) for x in e.elts])
        if isinstance(e, ast.Call):
            if self.parser_tokens(e, consts):
                return True
            cand = self.resolve(e.func, cls)
            return ("pc", cand) if cand else False
        if isinstance(e, ast.Name) and depth == 0:
            return ("any", [self.carry_struct(v, assigns, cls, consts, 1) for v in assigns.get(e.id, [])])
        return False


class _Scan(ast.NodeVisitor):
    def __init__(self, fi, tokens, consts, res):
        self.fi, self.tokens, self.consts, self.res = fi, tokens, consts, res
        self.chain, self.clsq = [], []
        self.stack = [FuncInfo("<module>", "module", None)]
        fi.funcs["<module>"] = self.stack[0]
        self.deferred_calls = []              # (call node, FuncInfo): classified once every import is known
        self.deferred_refs = []               # (candidate, FuncInfo, line): a name used but not called
        self.call_funcs = set()               # id() of every node that is a call's `func`
        self.deferred_funcs = []              # (FuncInfo, [return exprs], assigns)
        self.rets = [None]
        self.assigns = [None]

    cur = property(lambda self: self.stack[-1])

    def _add(self, form, toks, line):
        seen = set()
        for t in toks:
            if t not in seen:
                seen.add(t)
                self.cur.sites.append((form, t, line))

    def visit_Import(self, node):
        for a in node.names:
            if a.asname:
                self.res.mod[a.asname] = a.name
            else:
                top = a.name.split(".")[0]
                self.res.mod[top] = top

    def visit_ImportFrom(self, node):
        for a in node.names:
            self.res.frm[a.asname or a.name] = (node.module or "", a.name)

    def visit_ClassDef(self, node):
        for part in (*node.decorator_list, *node.bases, *node.keywords):
            self.visit(part)
        self.chain.append(node.name)
        qual = ".".join(self.chain)
        fn = self.fi.funcs.setdefault(qual, FuncInfo(qual, "class", self.clsq[-1] if self.clsq else None))
        fn.kind = "class"                     # the LATER definition wins, as in Python's rebinding (`def X` then `class X`)
        self.stack.append(fn)
        self.clsq.append(qual)
        for st in node.body:
            self.visit(st)
        self.clsq.pop()
        self.stack.pop()
        self.chain.pop()

    def _func(self, node):
        for d in node.decorator_list:
            self.visit(d)
        self.visit(node.args)
        if node.returns is not None:
            self.visit(node.returns)
        self.chain.append(node.name)
        qual = ".".join(self.chain)
        # a redefined qualname (a property's setter, a def under try/else, a duplicate def) MERGES: the earlier
        # definition's sites, calls and returns stay (a false pass of the kind spec 2.6 names)
        fn = self.fi.funcs.setdefault(qual, FuncInfo(qual, "func", self.clsq[-1] if self.clsq else None))
        fn.kind = "func"                      # `class X` then `def X`: the def wins
        self.stack.append(fn)
        self.rets.append([])
        self.assigns.append(defaultdict(list))
        for st in node.body:
            self.visit(st)
        self.deferred_funcs.append((fn, self.rets.pop(), self.assigns.pop()))
        self.stack.pop()
        self.chain.pop()

    visit_FunctionDef = _func
    visit_AsyncFunctionDef = _func

    def visit_Return(self, node):
        if self.rets[-1] is not None:
            self.rets[-1].append(node.value)
        self.generic_visit(node)

    def visit_Assign(self, node):
        if self.assigns[-1] is not None:
            for t in node.targets:
                if isinstance(t, ast.Name):
                    self.assigns[-1][t.id].append(node.value)
        self.generic_visit(node)

    def visit_Compare(self, node):
        lits = []
        for op in [node.left, *node.comparators]:
            lits += literals(op, self.consts)
        self._add("compare", [t for s in lits for t in self.tokens.literal(s)], node.lineno)
        self.generic_visit(node)

    def visit_Match(self, node):
        lits = []
        for case in node.cases:
            for sub in ast.walk(case.pattern):
                if isinstance(sub, ast.MatchValue):
                    lits += literals(sub.value, self.consts)
                elif isinstance(sub, ast.MatchMapping):          # `case {"pytest": y}`: a table key
                    for k in sub.keys:
                        lits += literals(k, self.consts)
        self._add("compare", [t for s in lits for t in self.tokens.literal(s)], node.lineno)
        self.generic_visit(node)

    def visit_Dict(self, node):
        lits = []
        for k in node.keys:
            if k is not None:
                lits += literals(k, self.consts)
        self._add("table-key", [t for s in lits for t in self.tokens.literal(s)], node.lineno)
        self.generic_visit(node)

    def visit_Call(self, node):
        self.deferred_calls.append((node, self.cur))
        self.call_funcs.add(id(node.func))
        if isinstance(node.func, ast.Name) and node.func.id == "dict":     # `dict(pytest=1)`: a table key
            self._add("table-key", [t for k in node.keywords if k.arg for t in self.tokens.literal(k.arg)], node.lineno)
        self.generic_visit(node)

    def _reference(self, node):
        """A predicate named without a call (`filter(er.is_p, xs)`, `chk = er.is_p`) is a use of it, like a call."""
        if id(node) not in self.call_funcs:
            cand = self.res.resolve(node, self.cur.cls)
            if cand:
                self.deferred_refs.append((cand, self.cur, node.lineno))

    def visit_Attribute(self, node):
        if isinstance(node.ctx, ast.Load):
            self._reference(node)
        self.generic_visit(node)

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Load):
            self._reference(node)

    def _call_form(self, call):
        """(form, [tokens]) a call is a site of, or (None, []): a parser call, a regex function, a name-call."""
        res, consts, f = self.res, self.consts, call.func
        ptoks = res.parser_tokens(call, consts)
        if ptoks:
            return "parser", ptoks
        if res.re_func(f) is not None:
            pat = call.args[0] if call.args else next((k.value for k in call.keywords if k.arg == "pattern"), None)
            lits = literals(pat, consts) if pat is not None else []
            return "regex", [t for s in lits for t in self.tokens.regex(s)]
        name = f.attr if isinstance(f, ast.Attribute) else (f.id if isinstance(f, ast.Name) else "")
        if not ((isinstance(f, ast.Attribute) and name in NAME_CALL_ATTRS) or name.startswith("fnmatch")):
            return None, []
        lits = []
        for arg in [*call.args, *(k.value for k in call.keywords)]:
            lits += literals(arg, consts)
        return "name-call", [t for s in lits for t in self.tokens.literal(s)]

    def _finish_call(self, call, fn):
        form, toks = self._call_form(call)
        if form:
            fn.sites += [(form, t, call.lineno) for t in dict.fromkeys(toks)]
        cand = self.res.resolve(call.func, fn.cls)
        if cand:
            fn.calls[cand].append(call.lineno)

    def _finish_returns(self, fn, rets, assigns):
        if not rets:
            return
        res = self.res
        ok = [res.bool_struct(r, fn.cls) if r is not None else False for r in rets]
        carry = ("any", [res.carry_struct(r, assigns, fn.cls, self.consts) for r in rets if r is not None])
        fn.ret_ok = ok if fn.ret_ok is None else fn.ret_ok + ok
        fn.carry = carry if fn.carry is False else ("any", [fn.carry, carry])

    def finish(self):
        for call, fn in self.deferred_calls:
            self._finish_call(call, fn)
        for cand, fn, line in self.deferred_refs:
            fn.calls[cand].append(line)
        for fn, rets, assigns in self.deferred_funcs:
            self._finish_returns(fn, rets, assigns)
        for qual, fn in self.fi.funcs.items():
            if fn.kind == "func" and qual.endswith(".__init__") and any(s[0] == "parser" for s in fn.sites):
                self.fi.parser_classes.add(qual[: -len(".__init__")])


def analyze_text(path, text, tokens):
    """FileInfo for one script; a file that does not parse carries `error` (C7), never rows."""
    fi = FileInfo(path)
    try:
        tree = ast.parse(text)
    except (SyntaxError, ValueError, RecursionError, MemoryError) as exc:
        line = getattr(exc, "lineno", None)
        fi.error = "%s: %s%s" % (type(exc).__name__, getattr(exc, "msg", None) or str(exc)[:100],
                                 " (line %d)" % line if line else "")
        return fi
    res = Resolver(fi.stem, tokens)
    res.defs = {st.name for st in tree.body if isinstance(st, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))}
    try:
        sc = _Scan(fi, tokens, module_consts(tree), res)
        sc.visit(tree)
        sc.finish()
    except (RecursionError, MemoryError) as exc:      # a deep `+` chain parses and then overflows the visitor (C7)
        fi.error = "%s: too deeply nested to read" % type(exc).__name__
        fi.funcs, fi.parser_classes = {}, set()
    return fi


def _ok(s, preds):
    if isinstance(s, bool):
        return s
    if s[0] == "all":
        return all(_ok(x, preds) for x in s[1])
    return s[1] in preds                     # ("pc", cand)


def _carries(s, preds):
    if isinstance(s, bool):
        return s
    if s[0] == "any":
        return any(_carries(x, preds) for x in s[1])
    return s[1] in preds


def compute_predicates(infos, seed=(), roots=()):
    """The fixpoint (spec 2.2): (predicates, parser-rooted predicates). A function is a predicate when every return is
    bool-like and its body holds a site (a call of a predicate is a site, so the chain closes); a parser class's
    constructor and a function returning a parser result (directly, through one local name, or as a tuple element) are
    predicates too. `seed` and `roots` are the stored lists of a staged run: the roots seed ONLY the carrying chain, so
    staged and whole mode follow the same names on the same tree (D1, spec 2.7)."""
    fresh = tuple(fi.stem + "." for fi in infos if not fi.error)         # these files are recomputed, as whole mode does
    seed = {n for n in seed if not n.startswith(fresh)}
    roots = {n for n in roots if not n.startswith(fresh)}
    preds = set(seed) | set(roots)
    proots = set(roots)       # parser-rooted names: what a CARRYING return may follow (spec 2.2, not any predicate)
    cands = []
    for fi in infos:
        if fi.error:
            continue
        preds |= {"%s.%s" % (fi.stem, q) for q in fi.parser_classes}
        proots |= {"%s.%s" % (fi.stem, q) for q in fi.parser_classes}
        for qual, fn in fi.funcs.items():
            if fn.kind == "func" and fn.ret_ok is not None:
                cands.append(("%s.%s" % (fi.stem, qual), fn))
    changed = True
    while changed:
        changed = False
        for name, fn in cands:
            if name in proots:
                continue
            carries = _carries(fn.carry, proots)
            if carries:
                preds.add(name)
                proots.add(name)
                changed = True
                continue
            if name in preds:
                continue
            has_site = bool(fn.sites) or any(c in preds for c in fn.calls)
            if has_site and all(_ok(s, preds) for s in fn.ret_ok):
                preds.add(name)
                changed = True
    return preds, proots


def file_keys(fi, preds):
    out = defaultdict(list)
    for qual, fn in fi.funcs.items():
        for form, tok, line in fn.sites:
            out["%s|%s|%s|%s" % (fi.path, qual, form, tok)].append(line)
        for cand, lines in fn.calls.items():
            if cand in preds:
                out["%s|%s|predicate-call|%s" % (fi.path, qual, cand)] += lines
    return out


def scan_texts(files, tokens=None, seed=(), roots=()):
    """Pure helper for tests: {path: text} -> (keys {key: [lines]}, predicates, errors {path: msg})."""
    tokens = tokens or Tokens(DEFAULT_TOKENS)
    infos = [analyze_text(p, t, tokens) for p, t in files.items()]
    preds, _roots = compute_predicates(infos, seed, roots)
    keys = {}
    for fi in infos:
        if not fi.error:
            keys.update(file_keys(fi, preds))
    return keys, preds, {fi.path: fi.error for fi in infos if fi.error}


class Scanned:
    def __init__(self, infos, preds, roots, live, files):
        self.infos, self.preds, self.roots, self.live, self.files = infos, preds, roots, live, files
        self.errors = {fi.path: fi.error for fi in infos if fi.error}


def scan_paths(src, count_paths, tokens, seed=(), extra_paths=(), roots=()):
    """Reads and analyses `count_paths` (counted) and `extra_paths` (only for the predicate fixpoint)."""
    paths = sorted(set(count_paths) | set(extra_paths))
    blobs = read_many(src, paths)
    infos = []
    for p in paths:
        blob = blobs[p]
        if isinstance(blob, Unread):
            raise CannotJudge("%s could not be read: %s" % (p, blob.reason))
        if blob is None:
            infos.append(FileInfo(p, absent=True))
            continue
        try:
            text = decode(blob)
        except UnicodeDecodeError as exc:
            fi = FileInfo(p)
            fi.error = "UnicodeDecodeError: not valid UTF-8 (%s)" % exc.reason
            infos.append(fi)
            continue
        infos.append(analyze_text(p, text, tokens))
    preds, proots = compute_predicates(infos, seed, roots)
    cset = set(count_paths)
    live = {}
    for fi in infos:
        if fi.path in cset and not fi.error:
            live.update(file_keys(fi, preds))
    return Scanned(infos, preds, proots, live, paths)


# ---------------------------------------------------------------------------------------------- baseline
def parse_key(key):
    parts = key.split("|", 3)
    return parts if len(parts) == 4 else None


def squash(s):
    return " ".join(str(s).split())


def validate_doc(doc):
    """C4: the problems of the baseline's shape (empty list: well-formed)."""
    if not isinstance(doc, dict):
        return ["the baseline is not a JSON object"]
    out = []
    if doc.get("schema") != 1:
        out.append("schema is not 1")
    scan = doc.get("scan")
    if not (isinstance(scan, dict) and isinstance(scan.get("root"), str) and isinstance(scan.get("exclude"), list)):
        out.append("`scan` needs a string `root` and a list `exclude`")
    toks = doc.get("tokens")
    if not (isinstance(toks, dict) and all(isinstance(v, list) and all(isinstance(t, str) for t in v)
                                           for v in toks.values())):
        out.append("`tokens` is not an object of string lists")
    mechs = doc.get("mechanisms")
    if not isinstance(mechs, dict):
        out.append("`mechanisms` is not an object")
        mechs = {}
    if not (isinstance(doc.get("predicates"), list) and all(isinstance(p, str) for p in doc["predicates"])):
        out.append("`predicates` is not a list of strings")
    if not (isinstance(doc.get("predicate_roots"), list) and all(isinstance(p, str) for p in doc["predicate_roots"])):
        out.append("`predicate_roots` is not a list of strings (the parser-rooted subset of `predicates`)")
    rows = doc.get("rows")
    if not isinstance(rows, list):
        return out + ["`rows` is not a list"]
    seen = set()
    for i, r in enumerate(rows):
        if not isinstance(r, dict):
            out.append("row %d is not an object" % i)
            continue
        key = r.get("key")
        label = "row %d (%s)" % (i, key)
        if not isinstance(key, str) or parse_key(key) is None:
            out.append("row %d: `key` is not <path>|<qualname>|<form>|<token>" % i)
            continue
        if key in seen:
            out.append("%s: duplicate key" % label)
        seen.add(key)
        if parse_key(key)[2] not in FORMS:
            out.append("%s: unknown form" % label)
        if not (isinstance(r.get("count"), int) and not isinstance(r.get("count"), bool) and r["count"] >= 1):
            out.append("%s: `count` is not an integer >= 1" % label)
        if r.get("kind") not in KINDS:
            out.append("%s: unknown kind %r (expected one of %s)" % (label, r.get("kind"), ", ".join(KINDS)))
        if r.get("mechanism") not in mechs:
            out.append("%s: mechanism %r is not in `mechanisms`" % (label, r.get("mechanism")))
        if not (isinstance(r.get("since"), str) and r["since"].strip()):
            out.append("%s: `since` is missing" % label)
    if "basis_word" in doc and not isinstance(doc["basis_word"], dict):
        out.append("`basis_word` is not an object")
    return out


def rows_by_key(doc):
    return {r["key"]: r for r in doc["rows"]}


def dumps(doc):
    """LF, sorted, one row per line, so two branches merge by line."""
    order = ("key", "count", "mechanism", "kind", "since", "word", "reason", "moved_from")
    rows = sorted(doc["rows"], key=lambda r: r["key"])

    def one(r):
        keys = [k for k in order if k in r] + sorted(k for k in r if k not in order)
        return json.dumps({k: r[k] for k in keys}, ensure_ascii=False)

    head = [("schema", doc["schema"]), ("scan", doc["scan"]), ("tokens", doc["tokens"]),
            ("mechanisms", doc["mechanisms"]), ("predicates", sorted(doc["predicates"])),
            ("predicate_roots", sorted(doc["predicate_roots"]))]
    if "basis_word" in doc:
        head.append(("basis_word", doc["basis_word"]))
    lines = ['{"%s": %s,' % (k, json.dumps(v, ensure_ascii=False)) if i == 0 else ' "%s": %s,' % (k, json.dumps(v, ensure_ascii=False))
             for i, (k, v) in enumerate(head)]
    body = ['  ' + one(r) + ("," if i < len(rows) - 1 else "") for i, r in enumerate(rows)]
    return "\n".join(lines + [' "rows": ['] + body + [" ]}"]) + "\n"


def new_doc(rows, predicates, roots=()):
    return {"schema": 1, "scan": json.loads(json.dumps(DEFAULT_SCAN)), "tokens": json.loads(json.dumps(DEFAULT_TOKENS)),
            "mechanisms": dict(DEFAULT_MECHANISMS), "predicates": sorted(predicates),
            "predicate_roots": sorted(roots), "rows": rows}


def load_doc(blob, label):
    try:
        doc = json.loads(decode(blob))
    except (ValueError, UnicodeDecodeError) as exc:
        raise CannotJudge("%s is not valid JSON: %s" % (label, exc))
    problems = validate_doc(doc)
    if problems:
        raise CannotJudge("%s is malformed (C4): %s" % (label, "; ".join(problems[:8])))
    return doc


# ---------------------------------------------------------------------------------------------- C3 / C5 / C3b
def _quote(row):
    w = row.get("word")
    return squash(w.get("quote")) if isinstance(w, dict) and w.get("quote") else None


def _reason(row):
    r = row.get("reason")
    return squash(r) if isinstance(r, str) and r.strip() else None


def _field(row, kind):
    return _quote(row) if kind == "road" else _reason(row)


def _travels(b, row):
    return (b.get("kind") == row.get("kind") and b.get("since") == row.get("since")
            and b.get("word") == row.get("word") and b.get("reason") == row.get("reason"))


def _same_triple(key):
    p = parse_key(key)
    return (p[2], p[3])


class _Cmp:
    """One compare of a baseline against its base. Its methods are the branches of C3: an added row, a row in both,
    and the budget per (form, token) that no new key can walk around (F1, F2: a relabel or a raise under a NEW key
    is judged by the totals and by the base's own words and reasons, never by the key alone)."""

    def __init__(self, base, cur):
        self.base, self.cur = base, cur
        self.brows, self.crows = rows_by_key(base), rows_by_key(cur)
        self.items, self.words = [], []
        self.base_by_triple = defaultdict(list)           # (path, form, token, mechanism) -> the base's keys, sorted
        for k in sorted(self.brows):
            p = parse_key(k)
            self.base_by_triple[(p[0], p[2], p[3], self.brows[k]["mechanism"])].append(k)
        self.tot_b, self.tot_c = Counter(), Counter()
        for rows, tot in ((self.brows, self.tot_b), (self.crows, self.tot_c)):
            for k, r in rows.items():
                p = parse_key(k)
                tot[(p[0], p[2], p[3], r["mechanism"])] += r["count"]
        # cap: what a base row has given up (base - current count) and no move has taken yet; a move spends it
        self.cap = {k: r["count"] - self.crows.get(k, {}).get("count", 0) for k, r in self.brows.items()}
        self.moved_out, self.moved_in = Counter(), Counter()      # sites a move took from a base key / brought to a key
        self.base_quotes = {q for q in map(_quote, self.brows.values()) if q}
        self.changed = defaultdict(list)       # (form, token) -> rows added, raised or relabelled (not a move)

    def add(self, typ, key, text, red=False):
        self.items.append({"type": typ, "key": key, "red": red, "text": text})

    # -- an added row
    def _spend(self, src, dst, n):
        self.cap[src] -= n
        self.moved_out[src] += n
        self.moved_in[dst] += n

    def _try_move(self, key, row):
        """True when the added row is a travelling move: inside its file (a whole row, or a PART of a row that gave up
        sites: a count-2 row split 1+1; fork 1), or across files with `moved_from`. Inside a file the move needs the same
        (path, form, token, mechanism), a source whose `cap` covers the new count, fields that travel, and a total that
        does not rise: a copied word 1 -> 1+1 raises the total and stays an added row."""
        path, _qual, form, tok = parse_key(key)
        triple = (path, form, tok, row["mechanism"])
        moved = None
        if self.tot_c[triple] <= self.tot_b[triple]:
            for k in self.base_by_triple.get(triple, ()):
                if self.cap[k] >= row["count"] and _travels(self.brows[k], row):
                    moved = k
                    break
        if moved:
            self._spend(moved, key, row["count"])
            self.add("moved", key, "moved inside %s: %s -> %s (kind %s, mechanism %s)"
                     % (path, moved, key, row["kind"], row["mechanism"]))
            if row["kind"] == "road" and row.get("word"):
                self.words.append(("moved row %s" % key, row.get("word")))
            return True
        mf = row.get("moved_from")
        src_row = self.brows.get(mf) if isinstance(mf, str) else None
        if src_row is None or mf == key:
            return False
        mp = parse_key(mf)
        if not (mp[0] != path and mp[2] == form and mp[3] == tok and src_row["mechanism"] == row["mechanism"]
                and self.cap.get(mf, 0) >= row["count"]):
            return False
        if row["kind"] == "road" and _travels(src_row, row):
            self._spend(mf, key, row["count"])
            self.add("moved", key, "moved across files: %s -> %s (kind road, the word travels; the critic reads "
                     "both bodies, question 9)" % (mf, key))
            if row.get("word"):
                self.words.append(("moved row %s" % key, row.get("word")))
            return True
        if row["kind"] != "road" and _reason(row) is not None and _reason(row) == _reason(src_row):
            self.add("added", key, "cross-file move of an `%s` row %s -> %s with the same reason: a reason "
                     "given for one script does not travel to another. Expected a new `reason` for the new "
                     "file. %s" % (row["kind"], mf, key, ROW_DOOR), True)
            return True
        return False

    def _reuse(self, row, form, tok):
        """The base row whose word's quote (road) or reason (same form and token, otherwise) the added row repeats."""
        if row["kind"] == "road":
            q = _quote(row)
            return next((k for k, r in sorted(self.brows.items()) if q and _quote(r) == q), None)
        rs = _reason(row)
        return next((k for k, r in sorted(self.brows.items())
                     if rs and _same_triple(k) == (form, tok) and _reason(r) == rs), None)

    def added(self, key, row):
        path, _qual, form, tok = parse_key(key)
        if self._try_move(key, row):
            return
        self.changed[(form, tok)].append(row)
        what = "word.quote" if row["kind"] == "road" else "reason"
        reused = self._reuse(row, form, tok)
        if row["kind"] == "road" and not isinstance(row.get("word"), dict):
            self.add("added", key, "added road row %s has no `word` {who, date, quote, carrier}. Expected the owner's "
                     "word. %s" % (key, ROW_DOOR), True)
        elif row["kind"] != "road" and _reason(row) is None:
            self.add("added", key, "added %s row %s has no `reason`. Expected a non-empty reason. %s"
                     % (row["kind"], key, ROW_DOOR), True)
        elif reused:
            self.add("added", key, "added %s row %s repeats the %s of %s: one word or reason never buys another site "
                     "(a key renamed, or `moved_from` left out, is not a move). Expected a new %s. %s"
                     % (row["kind"], key, what, reused, what, ROW_DOOR), True)
        else:
            self.add("added", key, "added %s row %s count %d (mechanism %s)" % (row["kind"], key, row["count"],
                                                                                 row["mechanism"]))
        if row["kind"] == "road" and isinstance(row.get("word"), dict):
            self.words.append(("added row %s" % key, row["word"]))

    # -- a row in both
    def _relabel(self, key, row, b):
        ok = True
        if b["kind"] == "road":
            nq = _quote(row)
            if nq is None or nq == _quote(b):
                ok = False
                self.add("relabelled", key, "relabelled %s: road -> %s without a new owner's word. Expected a `word` "
                         "whose quote differs from the base's. %s" % (key, row["kind"], ROW_DOOR), True)
            elif _reason(row) is None:
                ok = False
                self.add("relabelled", key, "relabelled %s: road -> %s has no `reason`. %s" % (key, row["kind"], ROW_DOOR),
                         True)
        elif row["kind"] == "road" and not isinstance(row.get("word"), dict):
            ok = False
            self.add("relabelled", key, "relabelled %s: %s -> road has no `word`. %s" % (key, b["kind"], ROW_DOOR), True)
        elif row["kind"] != "road" and _reason(row) is None:
            ok = False
            self.add("relabelled", key, "relabelled %s: %s -> %s has no `reason`. %s" % (key, b["kind"], row["kind"],
                                                                                          ROW_DOOR), True)
        if ok:
            self.add("relabelled", key, "relabelled %s: %s -> %s" % (key, b["kind"], row["kind"]))
        if row["kind"] == "road" and isinstance(row.get("word"), dict) or (b["kind"] == "road" and _quote(row)):
            self.words.append(("relabelled row %s" % key, row.get("word")))

    def _raise(self, key, row, b):
        new, old = _field(row, row["kind"]), _field(b, row["kind"])
        what = "word.quote" if row["kind"] == "road" else "reason"
        if new is None or new == old:
            self.add("raised", key, "raised %s: %d -> %d under the same %s as the base. Expected a new %s for the raise "
                     "(one word never buys any number of sites). %s" % (key, b["count"], row["count"], what, what,
                                                                         ROW_DOOR), True)
        else:
            self.add("raised", key, "raised %s: %d -> %d (kind %s, new %s)" % (key, b["count"], row["count"],
                                                                                row["kind"], what))
        if row["kind"] == "road" and isinstance(row.get("word"), dict):
            self.words.append(("raised row %s" % key, row["word"]))

    def both(self, key, row, b):
        if b["mechanism"] != row["mechanism"]:
            self.add("re-mechanised", key, "re-mechanised %s: %s -> %s" % (key, b["mechanism"], row["mechanism"]))
        kind_changed = b["kind"] != row["kind"]
        raised = row["count"] > b["count"]
        if kind_changed:
            self._relabel(key, row, b)
        if kind_changed or raised:
            self.changed[_same_triple(key)].append(row)
        if b.get("word") and not kind_changed and not _quote(row):
            self.add("word-removed", key, "the word of %s was removed or emptied. Expected the row to keep its word. %s"
                     % (key, ROW_DOOR), True)
        if b.get("reason") and row["kind"] != "road" and _reason(row) is None:
            self.add("reason-removed", key, "the reason of %s was removed or emptied. Expected the row to keep a reason. %s"
                     % (key, ROW_DOOR), True)
        if raised:
            self._raise(key, row, b)
        elif not kind_changed:
            if row["kind"] == "road":
                w = row.get("word")
                if isinstance(w, dict) and w != b.get("word"):           # the whole word, not the quote alone
                    self.add("reworded", key, "reworded %s (word)" % key)
                    self.words.append(("reworded row %s" % key, w))
            elif _reason(row) and _reason(row) != _reason(b):
                self.add("reworded", key, "reworded %s (reason)" % key)

    # -- the budget per (form, token), over the whole range
    def _gross(self):
        """Per (form, token): the road sites that fell and the non-road sites that rose, row by row, net of what a
        move carried (D2: a road raise elsewhere in the same commit never hides a road that became own-code)."""
        fall, rise = Counter(), Counter()
        for k, b in self.brows.items():
            c = self.crows.get(k)
            if b["kind"] == "road":
                kept = c["count"] if c and c["kind"] == "road" else 0
                fall[_same_triple(k)] += max(0, b["count"] - kept - self.moved_out[k])
        for k, c in self.crows.items():
            if c["kind"] != "road":
                b = self.brows.get(k)
                had = b["count"] if b and b["kind"] != "road" else 0
                rise[_same_triple(k)] += max(0, c["count"] - had - self.moved_in[k])
        return fall, rise

    def budget(self):
        kinds = defaultdict(lambda: Counter())
        for rows, sign in ((self.brows, -1), (self.crows, 1)):
            for k, r in rows.items():
                kinds[_same_triple(k)]["road" if r["kind"] == "road" else "own"] += sign * r["count"]
        fall, rise = self._gross()
        for triple in sorted(kinds):
            road = kinds[triple]["road"]
            rows = self.changed.get(triple, [])
            keys = sorted(r["key"] for r in rows)
            if any(it["red"] and _same_triple(it["key"]) == triple for it in self.items):
                continue                                                # already refused by its own row
            at = keys[0] if keys else None
            if road > 0 and not any(r["kind"] == "road" and _quote(r) and _quote(r) not in self.base_quotes
                                    for r in rows):
                self.add("budget", at or "|".join(["?", "?", *triple]), "the `road` total of `%s` on `%s` rose by %d "
                         "and no changed road row carries a quote the base does not hold. Expected a new owner's word "
                         "for the excess (one word never buys any number of sites). %s" % (triple[0], triple[1], road,
                                                                                             ROW_DOOR), True)
            elif fall[triple] > 0 and rise[triple] > 0 and not any(
                    r["kind"] != "road" and _quote(r) and _quote(r) not in self.base_quotes for r in rows):
                self.add("budget", at or "|".join(["?", "?", *triple]), "road sites of `%s` on `%s` fell by %d while "
                         "non-road rows rose by %d: a road relabelled through a new key. Expected a `word` with a "
                         "quote the base does not hold on the changed row. The budget is global per (form, token), "
                         "not per file: a road fixed in one script and an unrelated own-code row for the same token "
                         "in another trip it too; the way out is a new word on the changed row, or two commits. %s"
                         % (triple[0], triple[1], fall[triple], rise[triple], ROW_DOOR), True)


def compare_docs(base, cur):
    """The one compare of a baseline against its base (C3, C5 and --raises all print and judge from this result).
    Returns {"items": [{type, key, red, text}], "words": [(label, word)], "basis": [{what, text, kind}],
    "basis_word": (the base's, the current one)}."""
    cmp = _Cmp(base, cur)
    for key in sorted(cmp.crows):
        b = cmp.brows.get(key)
        if b is None:
            cmp.added(key, cmp.crows[key])
        else:
            cmp.both(key, cmp.crows[key], b)
    cmp.budget()
    basis = []
    if base["scan"] != cur["scan"]:
        basis.append({"what": "scan", "text": "`scan` changed: %s -> %s" % (json.dumps(base["scan"]), json.dumps(cur["scan"]))})
    for name in sorted(set(base["predicates"]) - set(cur["predicates"])):
        basis.append({"what": "predicate", "name": name, "text": "predicate `%s` removed from the stored list" % name})
    for name in sorted(set(base["predicate_roots"]) - set(cur["predicate_roots"])):
        basis.append({"what": "predicate_root", "name": name,
                      "text": "parser-rooted predicate `%s` removed from the stored roots" % name})
    return {"items": cmp.items, "words": cmp.words, "basis": basis,
            "basis_word": (base.get("basis_word"), cur.get("basis_word"))}


def check_word(word, src):
    """C3b: the shape of a word and the join to its carrier. None when fine, else the problem."""
    if not isinstance(word, dict):
        return "no word object {who, date, quote, carrier}"
    who, quote, carrier = word.get("who"), word.get("quote"), word.get("carrier")
    if not (isinstance(who, str) and who.strip()):
        return "`who` is missing"
    q = squash(quote) if isinstance(quote, str) else ""
    if len(q) < MIN_QUOTE:
        return "the quote is %d characters after whitespace is squashed; expected %d or more" % (len(q), MIN_QUOTE)
    if not (isinstance(carrier, str) and carrier.strip()):
        return "`carrier` is missing"
    norm = posixpath.normpath(carrier.replace("\\", "/"))
    if norm == BASELINE_REL:
        return "the carrier is the baseline itself; expected another tracked file where the word stands"
    if norm.startswith("/") or norm.startswith("..") or re.match(r"^[A-Za-z]:", norm):
        return "the carrier `%s` is not a path inside the repository" % carrier
    tracked = src.tracked(norm)
    if isinstance(tracked, Unread):
        return "the carrier `%s` could not be checked: %s" % (carrier, tracked.reason)
    if not tracked:
        return "the carrier `%s` is not a tracked file" % carrier
    blob = src.read(norm)
    if blob is None or isinstance(blob, Unread):
        return "the carrier `%s` is unreadable" % carrier
    if q not in squash(blob.decode("utf-8", "replace")):
        return "the quote does not stand in the carrier `%s`" % carrier
    return None


# ---------------------------------------------------------------------------------------------- the judging
def resolve_sha(repo, ref):
    code, raw, err = gitcmd.git(repo, "rev-parse", "--verify", "--quiet", ref + "^{commit}", stderr=True)
    sha = raw.decode().strip()
    if code != 0 or not sha:
        reason = gitcmd.as_text(err).strip().split("\n")[0] if err else ""
        raise CannotJudge("the base `%s` does not resolve to a commit (%s): fetch it or name another; C3 and C5 never "
                          "narrow to HEAD~1" % (ref, reason or "git rev-parse exit %d" % code))
    return sha


def staged_paths(repo):
    code, raw = gitcmd.git(repo, "diff", "--cached", "--name-only", "--no-renames", "-z")
    if code != 0:
        raise CannotJudge("the staged paths could not be listed (git exit %d)" % code)
    return [x for x in raw.decode("utf-8", "replace").split("\0") if x]


def is_py_in_scan(path, root, exclude):
    return path.startswith(root) and path.endswith(".py") and not any(path.startswith(e) for e in exclude)


def row_paths(brows, crows):
    """Files whose rows differ between two baselines (staged mode judges their live counts too)."""
    out = set()
    for k in set(brows) | set(crows):
        b, c = brows.get(k), crows.get(k)
        if b is None or c is None or b["count"] != c["count"] or b.get("moved_from") != c.get("moved_from"):
            out.add(parse_key(k)[0])
            for r in (b, c):
                if r and isinstance(r.get("moved_from"), str) and parse_key(r["moved_from"]):
                    out.add(parse_key(r["moved_from"])[0])
    return out


def fmt_site(key, lines, extra=""):
    path, qual, form, tok = parse_key(key)
    shown = ", ".join(str(n) for n in lines[:3]) if lines else "?"
    return "  %s in %s: %s on `%s` (line %s)%s" % (path, qual, form, tok, shown, extra)


class Judgement:
    def __init__(self):
        self.reds, self.notes = [], []

    def red(self, text):
        self.reds.append(text)


def pick_base(repo, a, head_ref_sha):
    """(base source, baseline blob at it, note). The effective base of W6/F13: when the base holds no baseline, the
    FIRST commit of <base>..<head> that adds it, so a branch that never merges is not silenced for good."""
    if a.staged:
        src = RevSource(repo, "HEAD")
        blob = src.read(BASELINE_REL)
        if isinstance(blob, Unread):
            raise CannotJudge("%s in HEAD could not be read: %s (W5)" % (BASELINE_REL, blob.reason))
        return src, blob, None
    if not a.base:
        return None, None, "no base: C3 and C5 not judged"
    sha = resolve_sha(repo, a.base)
    src = RevSource(repo, sha)
    blob = src.read(BASELINE_REL)
    if isinstance(blob, Unread):
        raise CannotJudge("%s at %s could not be read: %s (W5)" % (BASELINE_REL, a.base, blob.reason))
    if blob is not None:
        return src, blob, None
    head = head_ref_sha or "HEAD"
    code, raw, err = gitcmd.git(repo, "log", "--reverse", "--diff-filter=A", "--format=%H", "%s..%s" % (sha, head), "--",
                                BASELINE_REL, stderr=True)
    if code != 0:
        raise CannotJudge("git log %s..%s failed: %s" % (a.base, head, gitcmd.as_text(err).strip().split("\n")[0]))
    adds = raw.decode().split()
    if adds and adds[0] != resolve_sha(repo, head):
        esrc = RevSource(repo, adds[0])
        eblob = esrc.read(BASELINE_REL)
        if isinstance(eblob, Unread):
            raise CannotJudge("%s at %s could not be read: %s (W5)" % (BASELINE_REL, adds[0][:9], eblob.reason))
        return esrc, eblob, "effective base: %s, the first commit adding the baseline (F13)" % adds[0][:9]
    return src, None, None


def _pick_head(repo, a):
    """(head source, its sha or None): the index (staged), a named commit (--rev), or the working tree."""
    if a.staged:
        return IndexSource(repo), None
    if a.rev:
        sha = resolve_sha(repo, a.rev)
        return RevSource(repo, sha), sha
    return TreeSource(repo), None


def _union_delta(base_union, union):
    """(gone, added): the (family, token) pairs the union lost against the base's, and gained (gained only when the
    base had a union to compare with)."""
    bu = token_pairs(base_union) if base_union else set()
    cu = token_pairs(union)
    return sorted(bu - cu), (sorted(cu - bu) if bu else [])


def _staged_relevant(spaths):
    watched = (BASELINE_REL, DEFAULT_SCAN["root"] + DETECTORS_NAME, DEFAULT_SCAN["root"] + MARKERS_NAME)
    return any(is_py_in_scan(p, DEFAULT_SCAN["root"], DEFAULT_SCAN["exclude"]) or p in watched for p in spaths)


def _missing_baseline(head, base_blob, out):
    """The exit code of a head tree that holds no baseline (W3, W4)."""
    package = any(p.endswith(".py") for p in head.listing(DEFAULT_SCAN["root"]))
    if base_blob is not None:
        out("language_sites: the baseline is deleted by this commit: restore it (deleting a ratchet is a Lead act "
            "with its own commit, hook line and all; no door here) (W4)")
        return 1
    if not package:
        out("language_sites: no package here: nothing to scan")
        return 0
    raise CannotJudge("tools/language-sites-baseline.json is missing: this tree carries the package but not the "
                      "baseline; merge the branch that has it (`--init` is for the first fill only) (W3)")


def _count_paths(a, listing, spaths, cur, base, union, base_union):
    """The files whose live sites are counted: all in whole mode; staged, the staged scripts and the files whose rows
    differ (all of them when there is no base or the token union grew: the red lands on the commit that caused it)."""
    if not a.staged:
        return listing
    grows = base_union is not None and not token_pairs(union) <= token_pairs(base_union)
    if base is None or grows:
        return listing
    root, exclude = cur["scan"]["root"], cur["scan"]["exclude"]
    diff = row_paths(rows_by_key(base), rows_by_key(cur))
    return sorted({p for p in spaths if is_py_in_scan(p, root, exclude)} | diff)


def _scan_head(a, head, cur, base, union, base_union, spaths, listing):
    """(Scanned, set of counted paths). Staged mode seeds the fixpoint from the stored lists (the roots only seed the
    carrying chain, D1); whole mode seeds nothing."""
    whole = not a.staged
    count_paths = _count_paths(a, listing, spaths, cur, base, union, base_union)
    removed = sorted(set(base["predicates"]) - set(cur["predicates"])) if base else []
    stems = {posixpath.basename(p)[:-3]: p for p in listing}
    extra = [stems[n.split(".")[0]] for n in removed if n.split(".")[0] in stems]
    sc = scan_paths(head, count_paths, Tokens(union), seed=() if whole else cur["predicates"], extra_paths=extra,
                    roots=() if whole else cur["predicate_roots"])
    return sc, set(count_paths)


def _live_compare(jd, sc, cset, cur, whole):
    """C7, C1, C2 and (whole mode) C6: the live scan against the current rows. Returns the files counted."""
    crows = rows_by_key(cur)
    n_files = len([fi for fi in sc.infos if fi.path in cset and not fi.absent])
    if whole and not sc.live and crows and not sc.errors:
        raise CannotJudge("the scan read %d files and found 0 sites while the baseline holds %d rows: a dead scanner is "
                          "not a pass" % (n_files, len(crows)))
    for path, msg in sorted(sc.errors.items()):
        if path in cset:
            jd.red("C7 language_sites: %s does not parse: %s\nExpected: a script that parses (a file nobody can read is "
                   "not a pass, and it is never baselined)." % (path, msg))
    new_lines, stale_lines = [], []
    # whole mode judges EVERY row (a ghost row for a path outside the listing counts 0 live: F3); staged judges the
    # rows of the paths it counts
    judged = set(crows) if whole else {k for k in crows if parse_key(k)[0] in cset}
    for key in sorted(set(sc.live) | judged):
        n, row = len(sc.live.get(key, ())), crows.get(key)
        have = row["count"] if row else 0
        if not whole and parse_key(key)[0] not in cset:
            continue
        if n > have:
            new_lines.append(fmt_site(key, sc.live[key], "" if not row else " [row holds %d, code has %d]" % (have, n)))
        elif n < have:
            stale_lines.append("  %s [row holds %d, code has %d]" % (key, have, n))
    if new_lines:
        jd.red("C1 language_sites: a new branch on a language, the baseline holds no row for it:\n%s\n%s"
               % ("\n".join(new_lines[:MAX_SHOWN]) + ("\n  ... and %d more" % (len(new_lines) - MAX_SHOWN)
                                                       if len(new_lines) > MAX_SHOWN else ""), REFUSAL_TAIL))
    if stale_lines:
        jd.red("C2 language_sites: the baseline holds rows the code no longer matches (a stale row is refused, never "
               "shrunk silently):\n%s\nExpected: rows equal to the code. Door: `python tools/language_sites.py --shrink` "
               "(drops stale rows, lowers counts, never adds), or move the row (inside a file as is; across files with "
               "`moved_from`)." % "\n".join(stale_lines[:MAX_SHOWN]))
    if whole:
        _c6(jd, cur, sc)
    return n_files


def _c6(jd, cur, sc):
    """The stored predicate lists (all, and the parser-rooted subset) against the recomputed ones."""
    stored, roots = set(cur["predicates"]), set(cur["predicate_roots"])
    grew = sorted(sc.preds - stored) + sorted("roots: " + n for n in sc.roots - roots)
    fell = sorted(stored - sc.preds) + sorted("roots: " + n for n in roots - sc.roots)
    if grew or fell:
        jd.red("C6 language_sites: the stored predicate list differs from the recomputed one: grew %s, fell %s\n"
               "Expected: the list the code computes. Door: `python tools/language_sites.py --predicates` writes it "
               "(never a row); callers it makes new are rows of that same commit." % (grew, fell))


def _range_compare(jd, head, base, cur, base_union, union, sc):
    """C3, C3b and C5: the current baseline against its base."""
    res = compare_docs(base, cur)
    for it in res["items"]:
        if it["red"]:
            jd.red("C3 language_sites: " + it["text"])
    bw, cw = base.get("basis_word"), cur.get("basis_word")
    word_new = isinstance(cw, dict) and not (isinstance(bw, dict) and _quote({"word": cw}) == _quote({"word": bw}))
    gone = _union_delta(base_union, union)[0] if base_union else []
    basis_red = []
    for b in res["basis"]:
        pool = {"predicate": sc.preds, "predicate_root": sc.roots}.get(b["what"])
        if pool is None:
            basis_red.append(b["text"])
        elif b["name"] in pool:
            basis_red.append(b["text"] + " while its function is still a %s" % b["what"].replace("_", " "))
        else:
            jd.notes.append(b["text"] + ": its function is no longer a %s (green)" % b["what"].replace("_", " "))
    if gone:
        basis_red.append("tokens removed from the union: %s" % ", ".join("%s:%s" % p for p in gone))
    if basis_red and not word_new:
        jd.red("C5 language_sites: the basis was narrowed against the base:\n  %s\nExpected: no narrowing, or a "
               "top-level `basis_word` {who, date, quote, carrier} in the baseline with a quote the base does not "
               "hold (the same shape as a road row's word; only the owner gives it)." % "\n  ".join(basis_red))
    todo = list(res["words"])
    if isinstance(cw, dict) and (cw != bw or (basis_red and word_new)):     # the whole word, never the quote alone
        todo.append(("basis_word", cw))
    for label, w in todo:
        problem = check_word(w, head)
        if problem:
            jd.red("C3b language_sites: the word of %s is no word: %s. Expected {who, date, quote, carrier} with a "
                   "quote of %d+ characters that stands in a tracked carrier that is not the baseline. %s"
                   % (label, problem, MIN_QUOTE, ROW_DOOR))
    jd.notes += [it["text"] for it in res["items"] if not it["red"] and it["type"] != "added"]


def run_check(a, repo, out):
    t0 = time.time()
    if a.staged and (a.base or a.rev):
        raise CannotJudge("--staged judges the index against HEAD: it takes neither --rev nor --base")
    spaths = staged_paths(repo) if a.staged else []
    if a.staged and not _staged_relevant(spaths):
        return 0                                               # silent, before any parse
    head, head_sha = _pick_head(repo, a)
    jd = Judgement()
    base_src, base_blob, note = pick_base(repo, a, head_sha)
    if note:
        jd.notes.append(note)
    cur_blob = head.read(BASELINE_REL)
    if isinstance(cur_blob, Unread):
        raise CannotJudge("%s could not be read: %s (W5)" % (BASELINE_REL, cur_blob.reason))
    if cur_blob is None:
        return _missing_baseline(head, base_blob, out)
    cur = load_doc(cur_blob, BASELINE_REL)
    base = load_doc(base_blob, "the base's " + BASELINE_REL) if base_blob is not None else None
    if base is None and base_src is not None and not note:
        jd.notes.append("the baseline is created here: C3 and C5 not judged; `--init` is its only writer")
    union = effective_tokens(cur, head)
    base_union = effective_tokens(base, base_src, required=False) if base else None
    listing = package_listing(head, cur["scan"]["root"], cur["scan"]["exclude"], must=not a.staged)
    sc, cset = _scan_head(a, head, cur, base, union, base_union, spaths, listing)
    n_files = _live_compare(jd, sc, cset, cur, not a.staged)
    if base is not None:
        _range_compare(jd, head, base, cur, base_union, union, sc)
    for n in jd.notes:
        out("language_sites: " + n)
    for r in jd.reds:
        out(r)
    sys.stderr.write("language_sites: scanned %d files in %.2fs\n" % (n_files, time.time() - t0))
    if not jd.reds:
        out("language_sites: ok (%d rows, %d files scanned%s)%s" % (len(cur["rows"]), n_files,
                                                                    ", staged" if a.staged else "",
                                                                    "; the baseline holds NO rows" if not cur["rows"] else ""))
    return 1 if jd.reds else 0


def run_raises(a, repo, out):
    if not a.base:
        raise CannotJudge("--raises needs --base <ref>")
    if a.staged:
        raise CannotJudge("--raises reads the working tree (or --rev) against --base: --staged would silently judge "
                          "HEAD, so it is refused")
    head, head_sha = _pick_head(repo, a)
    base_src, base_blob, note = pick_base(repo, a, head_sha)
    cur_blob = head.read(BASELINE_REL)
    if isinstance(cur_blob, Unread) or cur_blob is None:
        raise CannotJudge("%s could not be read in the head tree" % BASELINE_REL)
    cur = load_doc(cur_blob, BASELINE_REL)
    if base_blob is None:
        out("language_sites: the baseline is created here: nothing to compare")
        return 0
    base = load_doc(base_blob, "the base's " + BASELINE_REL)
    res = compare_docs(base, cur)
    if note:
        out("language_sites: " + note)
    for it in res["items"]:
        out("%s%s" % ("RED  " if it["red"] else "     ", it["text"]))
    for b in res["basis"]:
        out("     basis: " + b["text"])
    bw, cw = res["basis_word"]
    if cw != bw:
        out("     basis_word: %s -> %s" % (json.dumps(bw, ensure_ascii=False), json.dumps(cw, ensure_ascii=False)))
        problem = check_word(cw, head) if isinstance(cw, dict) else None
        if problem:
            out("RED  C3b basis_word is no word: %s" % problem)
    gone, added = _union_delta(effective_tokens(base, base_src, required=False), effective_tokens(cur, head))
    if gone:
        out("     basis: tokens removed from the union: %s" % ", ".join("%s:%s" % p for p in gone))
    if added:
        out("     basis: tokens added to the union: %s" % ", ".join("%s:%s" % p for p in added))
    if not res["items"] and not res["basis"] and cw == bw:
        out("language_sites: no row differs from the base")
    return 0


def package_listing(head, root, exclude, must=True):
    """The scripts the scan counts under `root`; with `must`, an empty listing cannot be judged (a scan of nothing is
    not green) -- the one place the three modes that need a whole listing get it from."""
    listing = [p for p in head.listing(root) if is_py_in_scan(p, root, exclude)]
    if must and not listing:
        raise CannotJudge("the scan found 0 files under %s: a scan of nothing is not green" % root)
    return listing


def _tree_scan(repo):
    head = TreeSource(repo)
    blob = head.read(BASELINE_REL)
    if isinstance(blob, Unread):
        raise CannotJudge("%s could not be read: %s" % (BASELINE_REL, blob.reason))
    if blob is None:
        raise CannotJudge("%s is missing (W3): nothing to work on" % BASELINE_REL)
    doc = load_doc(blob, BASELINE_REL)
    scan = doc["scan"]
    listing = package_listing(head, scan["root"], scan["exclude"])
    return head, doc, scan_paths(head, listing, Tokens(effective_tokens(doc, head))), listing


def run_totals(a, repo, out):
    t0 = time.time()
    _head, doc, sc, listing = _tree_scan(repo)
    kinds, mechs = Counter(), Counter()
    for r in doc["rows"]:
        kinds[r["kind"]] += r["count"]
        mechs[r["mechanism"]] += r["count"]
    out("rows %d, sum of counts %d; live keys %d, live sum %d" % (len(doc["rows"]), sum(r["count"] for r in doc["rows"]),
                                                                  len(sc.live), sum(len(v) for v in sc.live.values())))
    out("by kind: " + ", ".join("%s %d" % kv for kv in sorted(kinds.items())))
    out("by mechanism: " + ", ".join("%s %d" % kv for kv in sorted(mechs.items())))
    out("predicates stored %d, recomputed %d" % (len(doc["predicates"]), len(sc.preds)))
    out("files scanned %d, parse errors %d, wall time %.2fs" % (len(listing), len(sc.errors), time.time() - t0))
    return 0


def _write(repo, doc):
    (Path(repo) / BASELINE_REL).parent.mkdir(parents=True, exist_ok=True)
    (Path(repo) / BASELINE_REL).write_bytes(dumps(doc).encode("utf-8"))


def run_shrink(a, repo, out):
    _head, doc, sc, _listing = _tree_scan(repo)
    if sc.errors:
        for p, m in sorted(sc.errors.items()):
            out("language_sites: %s does not parse: %s -- refusing to shrink while a file is unread" % (p, m))
        return 1
    rows, dropped, lowered = [], [], []
    for r in doc["rows"]:
        n = len(sc.live.get(r["key"], ()))
        if n == 0:
            dropped.append(r["key"])
        elif n < r["count"]:
            lowered.append("%s %d -> %d" % (r["key"], r["count"], n))
            rows.append(dict(r, count=n))
        else:
            rows.append(r)
    by_key = rows_by_key(doc)
    still_new = len([k for k in sc.live if k not in by_key or len(sc.live[k]) > by_key[k]["count"]])
    _write(repo, dict(doc, rows=rows))
    for k in dropped:
        out("dropped " + k)
    for k in lowered:
        out("lowered " + k)
    out("language_sites: shrunk: %d dropped, %d lowered; %d keys the code holds beyond their rows stay red (--shrink "
        "never adds or raises)" % (len(dropped), len(lowered), still_new))
    return 0


def run_predicates(a, repo, out):
    _head, doc, sc, _listing = _tree_scan(repo)
    old, new = set(doc["predicates"]), sc.preds
    for n in sorted(new - old):
        out("grew " + n)
    for n in sorted(old - new):
        out("fell " + n)
    _write(repo, dict(doc, predicates=sorted(new), predicate_roots=sorted(sc.roots)))
    out("language_sites: predicates written (%d); no row was written -- callers made new by growth are rows of the same "
        "commit" % len(new))
    return 0


def run_init(a, repo, out):
    path = Path(repo) / BASELINE_REL
    if path.exists():
        out("language_sites: %s exists; --init is for the first fill only and never reopens. Expected: edit the rows by "
            "hand under C3, or --shrink." % BASELINE_REL)
        return 1
    head = TreeSource(repo)
    union = effective_tokens({"scan": DEFAULT_SCAN, "tokens": DEFAULT_TOKENS}, head)
    listing = package_listing(head, DEFAULT_SCAN["root"], DEFAULT_SCAN["exclude"])
    sc = scan_paths(head, listing, Tokens(union))
    if sc.errors:
        for p, m in sorted(sc.errors.items()):
            out("language_sites: %s does not parse: %s" % (p, m))
        return 1
    rows = [{"key": k, "count": len(v), "mechanism": "M8", "kind": "road", "since": SINCE_DEFAULT}
            for k, v in sorted(sc.live.items())]
    _write(repo, new_doc(rows, sc.preds, sc.roots))
    out("language_sites: wrote %d rows and %d predicates (mechanism M8, kind road, since %s: grandfathered, not "
        "approved)" % (len(rows), len(sc.preds), SINCE_DEFAULT))
    return 0


def main(argv=None):
    for stream in (sys.stdout, sys.stderr):      # the refusal quotes the committer's own text (a dash, a quote)
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(prog="language_sites", description=__doc__.split("\n")[0])
    cmds = ap.add_mutually_exclusive_group(required=True)
    for name in ("check", "raises", "totals", "shrink", "predicates", "init"):
        cmds.add_argument("--" + name, action="store_true")
    ap.add_argument("--staged", action="store_true")
    ap.add_argument("--base")
    ap.add_argument("--rev")
    ap.add_argument("--repo", default=str(REPO))
    try:
        a = ap.parse_args(sys.argv[1:] if argv is None else argv)
    except SystemExit as exc:
        return 2 if exc.code else 0
    repo = Path(a.repo)
    out = print
    try:
        if a.check:
            return run_check(a, repo, out)
        if a.raises:
            return run_raises(a, repo, out)
        if a.totals:
            return run_totals(a, repo, out)
        if a.shrink:
            return run_shrink(a, repo, out)
        if a.predicates:
            return run_predicates(a, repo, out)
        return run_init(a, repo, out)
    except CannotJudge as exc:
        print("language_sites: cannot judge -- %s" % exc)
        return 2


if __name__ == "__main__":
    sys.exit(main())
