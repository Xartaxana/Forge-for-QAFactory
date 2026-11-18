"""A pointer in a rule text resolves (FG7-52, t-1437 card; finding 20261112 class "a pointer outlives its object").

Scanned: the MAIN documents of the axis-31 register of docs/SIBLING_MAP.md (`main_documents`, the one reader; the test of role
carriers imports it), minus AGENTS.md (a generated copy: its sources are scanned) and minus ai-packages/ (Card B). Four kinds:
  P path     a backticked token with a file suffix or a slash, or an unbackticked `<top-level entry>/...<suffix>` token;
             `:N`, `:N-M`, `::symbol` are cut off and NOT judged (named miss).
  R range    `FR-1...FR-N`; `P1...PN` on a line naming the P home; `<file> rule(s) A[-B][, C]` and `rule N of <file>`.
             A range from 1 is a full-set claim: the enumeration must reach the home maximum; every named item must exist.
  N number   NUMBER_PAIRS: a sentence of a text against a constant read by `ast` (no import); digits, `250K`, EN/RU words.
  A anchor   the cells of the two TOC tables (TOC_TABLES) and prose `<file> § N` / `<file> § Tiers`; a heading starts with the
             anchor, or a numbered item / `Rule N` heading exists.
  X          a row of tools/pointer-lint-exempt.json that is stale (never used) or has no `why`.
Exemptions: `{"rows": {"<carrier>|<token>": {"why": "..."}}}`, written by hand under review; NO writer command (the cheap way
past). A row is red when it suppressed nothing: its token left the carrier, or the path now resolves.
Exit: 0 pass, 1 red, 2 cannot judge (register or control document missing, a home with no openers, a constant not found, git
unavailable, malformed JSON: an unknown is never a pass, AR-28). No timeout and no skip flag; the wall time goes to stderr.
Error direction: a rooted path errs to FALSE RED (door: an exemption row); a bare name errs to FALSE PASS.
KNOWN MISSES (pinned as tests that assert NOT detected): 1 a bare name rescued by a namesake; 2 a range or rule pointer with no home
named on its line; 3 a `:line` or `::symbol` that moved; 4 a gate number with no NUMBER_PAIRS row; 5 an anchor in prose outside the
TOC tables and the listed forms; 6 partially staged text (the hook reads the working tree).
Run: python -B tools/pointer_lint.py --check [--repo PATH]
"""
from __future__ import annotations

import argparse
import ast
import json
import posixpath
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gitcmd  # noqa: E402
import md_table  # noqa: E402

SIBLING_MAP = "docs/SIBLING_MAP.md"
EXEMPT_FILE = "tools/pointer-lint-exempt.json"
CONTROL_DOCS = ("CLAUDE.md", "COORDINATOR.md", "docs/TESTING.md", ".claude/agents/critic.md")
SKIP_CARRIERS = ("AGENTS.md", "ai-packages/")
REPO_PREFIXES = ("C:/QAFactory/forge-repo/",)
DOOR = 'fix the pointer, or add "%s|%s" with a why to ' + EXEMPT_FILE

FR_HOME = ("ai-packages/qa-factory/design/factory-rules.md", re.compile(r"^\*\*FR-(\d+) "))
P_HOME = ("docs/OWNER_PRINCIPLES.md", re.compile(r"^- \*\*P(\d+)\.\*\*"))
COORD = "COORDINATOR.md"
COORD_RULE_HEAD = re.compile(r"^### Rule (\d+)")
ITEM_RE = re.compile(r"^\s*(\d+[a-z]?)\.\s")
NOT_RULE_SECTIONS = ("command hygiene",)       # numbered points that are not rules: `CLAUDE.md rule 3` stays stale (K-STALE)

# (the TOC file, the heading of its table, the column that holds the pointer)
TOC_TABLES = [("COORDINATOR.md", "Contents", "Where"), ("PROJECT.md", "Оглавление", "Раздел")]
PROSE_ANCHORS = r"Rule\s+\d+|\d+(?:\.\d+)*[a-z]?|Tiers|Routing log|Routing rules|Role\s*≠\s*tier|Lead degradation|Contents|Cost gates"

# (constant "path::NAME", carrier, regex with ONE group: a digit, a number word or `250K`)
NUMBER_PAIRS = [
    ("tools/dispatch_manifest.py::DESIGNER_THRESHOLD", "COORDINATOR.md", r"carries (\w+) OR MORE numbered items"),
    ("tools/dispatch_manifest.py::DESIGNER_THRESHOLD", "PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md", r"carries (\w+) OR MORE numbered items"),
    ("tools/dispatch_gate.py::PARALLEL_CAP", "COORDINATOR.md", r"\| (\w+) writers, queue"),
    ("tools/dispatch_gate.py::PARALLEL_CAP", "PROJECT.md", r"держать (\w+) пишущих"),
    ("tools/dispatch_gate.py::PARALLEL_CAP", "docs/RUNBOOK.md", r"не больше (\w+) пишущих"),
    ("tools/dispatch_gate.py::PARALLEL_CAP", "PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md", r"more than (\w+) WRITING workers"),
    ("tools/agent_budget.py::WORKER_WARN", "COORDINATOR.md", r"WARN (\d+K)"),
    ("tools/agent_budget.py::WORKER_STOP", "COORDINATOR.md", r"STOP (\d+K)"),
]
WORDS = dict(zip("one two three four five six seven eight nine ten eleven twelve".split(), range(1, 13)))
WORDS.update(zip("один два три четыре пять шесть семь восемь девять десять одиннадцать двенадцать".split(), range(1, 13)))

SUFFIX_RE = re.compile(r"\.(?:md|py|json|jsonl|ya?ml|txt|sh|toml|cfg|ini|ps1|csv|html|js|ts)$", re.I)
SPAN_RE = re.compile(r"`([^`\n]+)`")
TOKEN_OK = re.compile(r"[\w.@+\-/<>*{}$%]+")
SEP = r"\s*(?:…|\.\.\.?|–|—)\s*"        # a plain hyphen joins a range only where the form is unambiguous (`FR-4-FR-9`, rules)


def rest(mark):
    return r"(?P<rest>(?:\s*,\s*(?:and\s+)?" + mark + r"\d+[a-z]?)*)"


FR_RE = re.compile(r"\bFR-(?P<a>\d+)(?:" + SEP + r"(?:FR-)?|\s*-\s*FR-)(?P<b>\d+)" + rest("(?:FR-)?"))
P_RE = re.compile(r"(?<![\w-])P(?P<a>\d+)(?:" + SEP + r"P?|\s*-\s*P)(?P<b>\d+)" + rest("P?"))
RULE_RE = re.compile(r"(?P<f>[\w./-]+\.md)[`'s]{0,3}\s+(?:routing\s+)?rules?\s+(?P<a>\d+[a-z]?)(?:" + SEP.replace("—)", "—|-)") + r"(?P<b>\d+[a-z]?))?" + rest(""), re.I)
RULE_OF_RE = re.compile(r"\b(?:rule (?P<a>\d+[a-z]?)|R(?P<c>\d+)-\w)\s+of\s+(?P<f>[\w./-]+\.md)"
                        r"|правил\w*\s+(?P<d>\d+\w?)\s+(?:в\s+)?`?(?P<g>[\w./-]+\.md)")
ANCHOR_RE = re.compile(r"(?P<f>[\w./-]+\.md)`?\s*§\s*(?P<a>" + PROSE_ANCHORS + r")")
NUM_ANCHOR = re.compile(r"(?:Rule\s+)?(\d+(?:\.\d+)*[a-z]?)(?:\s*[-–]\s*(\d+))?")


class CannotJudge(Exception):
    pass


def main_documents(root, absent=None):
    """MAIN = the files of axis 31 whose Owner / pointer cell starts with owner or procedure (E13: a missing table or a
    malformed row yields fewer documents, never a pass: `run` exits 2 on a missing control document). `absent`, when a list,
    collects (path, line) of register rows whose file is gone."""
    lines = (root / SIBLING_MAP).read_text(encoding="utf-8").splitlines()
    table = md_table.table_after(lines, "Axis 31")
    if table is None:
        return []
    header, rows = table
    names = [h.casefold() for h in header]
    if "file" not in names or "owner / pointer" not in names:
        return []
    fi, oi = names.index("file"), names.index("owner / pointer")
    out = set()
    for cells, line_no in rows:
        if len(cells) <= max(fi, oi) or not cells[oi].casefold().startswith(("owner", "procedure")):
            continue
        m = re.match(r"`([^`]+\.md)`", cells[fi])
        if not m:
            continue
        path = m.group(1)
        if "*" in path:
            out.update(q.relative_to(root).as_posix() for q in root.glob(path))
        elif (root / path).is_file():
            out.add(path)
        elif absent is not None:
            absent.append((path, line_no))
    return sorted(out)


class Tree:
    """The tracked paths (`git ls-files -z`: NUL-separated, so a non-ASCII name is not octal-quoted) and their lookups."""

    def __init__(self, root):
        rc, out = gitcmd.git(root, "ls-files", "-z")
        if rc != 0:
            raise CannotJudge("git ls-files failed (rc %s): %s" % (rc, out[:120].decode("utf-8", "replace")))
        self.root = root
        self.paths = sorted(p for p in out.decode("utf-8", "replace").split("\0") if p)
        self.set = set(self.paths)
        self.tops = {p.split("/")[0] for p in self.paths}
        self.dirs = set()
        self.suffixes = set()
        for p in self.paths:
            parts = p.split("/")
            for i in range(1, len(parts)):
                self.dirs.add("/".join(parts[:i]))
            for i in range(len(parts)):
                self.suffixes.add("/".join(parts[i:]))
        for d in list(self.dirs):
            parts = d.split("/")
            for i in range(len(parts)):
                self.suffixes.add("/".join(parts[i:]))

    def rooted(self, tok):
        return tok.split("/")[0] in self.tops

    def exact(self, tok):
        tok = tok.rstrip("/")
        return tok in self.set or tok in self.dirs

    def file(self, tok):
        """The tracked path a named file means: the exact path, else the first one ending with /tok; None when absent."""
        if tok in self.set:
            return tok
        return next((p for p in self.paths if p.endswith("/" + tok)), None)


def clean(tok):
    """A raw token as a repo path candidate, or None (a URL, another absolute path, not a path at all)."""
    tok = tok.strip().strip("'\"").replace("\\", "/")
    for pre in REPO_PREFIXES:
        if tok.startswith(pre):
            tok = tok[len(pre):]
    if "://" in tok or tok.startswith(("/", "~", "-")) or re.match(r"[A-Za-z]:", tok):
        return None
    tok = tok.rstrip(".,;:)")
    tok = re.sub(r"(?:::\w[\w.]*|:\d+(?:-\d+)?)$", "", tok).rstrip(".,;:)")
    tok = tok.split("#")[0]
    if not tok or not TOKEN_OK.fullmatch(tok) or re.fullmatch(r"\.\w+", tok):      # a bare suffix (`.md`) names no file
        return None
    return tok


def is_placeholder(tok):
    return any(c in tok for c in "<*{$") or "/.../" in tok


def candidate(tok, tree):
    suffixed = bool(SUFFIX_RE.search(tok.rstrip("/")))
    if "/" in tok:
        return suffixed or tree.rooted(tok)
    return suffixed and not is_placeholder(tok)


def path_tokens(line, tree):
    """The cleaned path candidates of one line: every word of a backtick span, and bare `top/...suffix` tokens outside spans."""
    out = []
    for m in SPAN_RE.finditer(line):
        words = re.sub(r"<[^>]*>", lambda g: g.group(0).replace(" ", "_"), m.group(1)).split()
        whole = clean(m.group(1)) if len(words) > 1 and SUFFIX_RE.search(m.group(1).strip()) else None
        if whole and tree.exact(whole):
            continue
        for w in words:
            tok = clean(w)
            if tok and candidate(tok, tree):
                out.append(tok)
    bare = SPAN_RE.sub(lambda m: " " * len(m.group(0)), line)
    tops = sorted((re.escape(t) for t in tree.tops), key=len, reverse=True)
    for m in re.finditer(r"(?<![\w/.:~$-])(?:" + "|".join(tops) + r")/[^\s`|()\[\]\"',;]*", bare):
        tok = clean(m.group(0))
        if tok and SUFFIX_RE.search(tok.rstrip("/")):
            out.append(tok)
    return out


def resolve(tok, carrier, tree):
    """Steps 1-4 of D3: True resolved, False red (step 5, git check-ignore, and the exemption are the caller's), None skipped."""
    if tok.startswith(("./", "../")):
        joined = posixpath.normpath(posixpath.join(posixpath.dirname(carrier), tok))
        return not joined.startswith("..") and tree.exact(joined)
    if is_placeholder(tok):
        segs = tok.split("/")
        fixed = []
        for s in segs[:-1]:
            if is_placeholder(s):
                break
            fixed.append(s)
        if not fixed:
            return None
        prefix = "/".join(fixed)
        if tree.rooted(prefix):
            return prefix in tree.dirs
        return prefix in tree.suffixes
    if tree.rooted(tok):
        # `tools/mod.symbol` names a function of tools/mod.py: the module is judged, the symbol is a named miss
        return tree.exact(tok) or (not SUFFIX_RE.search(tok) and tok.split(".")[0] + ".py" in tree.set)
    return tok.rstrip("/") in tree.suffixes


def ignored(tokens, root):
    """The subset of repo-relative `tokens` a .gitignore rule matches (one batched call; a missing file still matches)."""
    if not tokens:
        return set()
    rc, out, err = gitcmd.git(root, "check-ignore", "--no-index", "--", *sorted(tokens), stderr=True)
    if rc not in (0, 1):
        raise CannotJudge("git check-ignore failed (rc %s): %s" % (rc, err[:200].decode("utf-8", "replace")))
    return {p for p in out.decode("utf-8", "replace").splitlines() if p}


def home_max(root, home):
    rel, rx = home
    p = root / rel
    if not p.is_file():
        raise CannotJudge("home %s is absent" % rel)
    nums = [int(m.group(1)) for line in p.read_text(encoding="utf-8").splitlines() for m in [rx.match(line)] if m]
    if not nums:
        raise CannotJudge("home %s has no openers (%s)" % (rel, rx.pattern))
    return max(nums)


class Home:
    """Headings and numbered items of one named file, outside fences; the numbered points of NOT_RULE_SECTIONS are not rules."""

    def __init__(self, text):
        self.heads, self.items, self.rule_heads = [], set(), set()
        self.lines = []
        section = ""
        for _, line in md_table.md_lines_outside_fences(text.splitlines()):
            if line.startswith("#"):
                head = " ".join(line.lstrip("#").split()).replace("«", "").replace("»", "").casefold()
                self.heads.append(head)
                if line.startswith("## "):
                    section = head
                m = COORD_RULE_HEAD.match(line)
                if m:
                    self.rule_heads.add(m.group(1))
                self.lines.append((line, True))
                continue
            m = ITEM_RE.match(line)
            if m and not section.startswith(NOT_RULE_SECTIONS):
                self.items.add(m.group(1))
                self.lines.append((line, False))
        self.nums = {re.match(r"\d+", i).group(0) for i in self.items} | self.rule_heads
        self.max = max(map(int, self.rule_heads)) if self.rule_heads else max(map(int, self.nums), default=0)

    def has_item(self, n):
        return n in self.items or n in self.nums

    def has_anchor(self, anchor):
        m = NUM_ANCHOR.fullmatch(anchor)
        if m:
            first, last = m.group(1), m.group(2)
            ns = [str(i) for i in range(int(first), int(last) + 1)] if last else [first]
            return all(self.numbered(n) for n in ns)
        norm = " ".join(anchor.replace("«", "").replace("»", "").split()).casefold()
        return any(h.startswith(norm) for h in self.heads)

    def numbered(self, n):
        rx = re.compile(r"^\s*(?:#{1,6}\s+)?(?:Rule\s+)?" + re.escape(n) + (r"[a-z]?\.?(?:\s|$)" if "." in n else r"[a-z]?\.(?:\s|$)"))
        head = re.compile(r"^#{1,6}\s+Rule\s+" + re.escape(n) + r"(?![\w.])")
        return any(rx.match(line) or head.match(line) for line, _ in self.lines)


def lead(x):
    return int(re.match(r"\d+", x).group(0))


def items_of(a, b, rest):
    """The item names a range pointer claims: `a`, the integers a..b, and every item of the trailing enumeration."""
    names = {a} if not b else {str(i) for i in range(lead(a), lead(b) + 1)}
    return names | set(re.findall(r"\d+[a-z]?", rest or ""))


def number_value(raw):
    raw = raw.casefold()
    if raw.isdigit():
        return int(raw)
    m = re.fullmatch(r"(\d+)k", raw)
    if m:
        return int(m.group(1)) * 1000
    return WORDS.get(raw)


def read_constant(root, spec):
    rel, name = spec.split("::")
    p = root / rel
    if not p.is_file():
        raise CannotJudge("constant %s: file %s is absent" % (spec, rel))
    for node in ast.parse(p.read_text(encoding="utf-8")).body:
        targets = node.targets if isinstance(node, ast.Assign) else [node.target] if isinstance(node, ast.AnnAssign) else []
        if any(isinstance(t, ast.Name) and t.id == name for t in targets) and node.value is not None:
            try:
                return ast.literal_eval(node.value)
            except ValueError:
                break
    raise CannotJudge("constant %s not found as a literal assignment in %s" % (spec, rel))


def load_exempt(root):
    p = root / EXEMPT_FILE
    if not p.is_file():
        return {}
    try:
        rows = json.loads(p.read_text(encoding="utf-8"))["rows"]
        assert isinstance(rows, dict) and all(isinstance(v, dict) for v in rows.values())
    except (ValueError, KeyError, AssertionError, TypeError) as exc:
        raise CannotJudge("%s is malformed (%s)" % (EXEMPT_FILE, exc))
    return rows


class Lint:
    def __init__(self, root):
        self.root = root
        self.tree = Tree(root)
        self.exempt = load_exempt(root)
        self.used = set()
        self.finds = []                 # (carrier, line, kind, pointer, what, home, exempt key or None)
        self.pending = []               # (carrier, line, token): a path that failed D3 steps 1-4
        self.pointers = 0
        self._homes = {}

    def home(self, rel):
        if rel not in self._homes:
            self._homes[rel] = Home((self.root / rel).read_text(encoding="utf-8", errors="replace"))
        return self._homes[rel]

    def add(self, carrier, line, kind, pointer, what, home="-", key=None):
        self.finds.append((carrier, line, kind, pointer, what, home, key))

    def scan(self, carrier, text, fr_max, p_max):
        for n, line in enumerate(text.splitlines(), 1):
            for tok in path_tokens(line, self.tree):
                self.pointers += 1
                if resolve(tok, carrier, self.tree) is False:
                    self.pending.append((carrier, n, tok))
            heading = line.startswith("#")
            for m in FR_RE.finditer(line):
                self.range(carrier, n, m, "FR-", fr_max, FR_HOME[0], heading)
            if re.search(r"OWNER_PRINCIPLES|principle|принцип", line, re.I) and carrier != P_HOME[0]:
                for m in P_RE.finditer(line):
                    self.range(carrier, n, m, "P", p_max, P_HOME[0], heading)
            for m in RULE_RE.finditer(line):
                self.rule(carrier, n, m.group("f"), m, heading)
            for m in RULE_OF_RE.finditer(line):
                a = m.group("a") or m.group("c") or m.group("d")
                self.rule(carrier, n, m.group("f") or m.group("g"), None, heading, single=a)
            for m in ANCHOR_RE.finditer(line):
                self.anchor(carrier, n, m.group("f"), m.group("a"))

    def range(self, carrier, n, m, mark, home_max_, home_rel, heading):
        if heading or carrier == home_rel:                       # a heading is not a claim; a home is not checked against itself
            return
        a, b = int(m.group("a")), int(m.group("b"))
        self.pointers += 1
        top = max(lead(x) for x in items_of(m.group("a"), m.group("b"), m.group("rest")))
        text = m.group(0).strip()
        if top > home_max_:
            self.add(carrier, n, "R", text, "the home holds %s1..%s%d" % (mark, mark, home_max_), home_rel)
        elif a == 1 and top < home_max_:
            self.add(carrier, n, "R", text, "a range from 1 is a full-set claim; the home holds %s1..%s%d" % (mark, mark, home_max_), home_rel)

    def rule(self, carrier, n, fname, m, heading, single=None):
        home_rel = self.tree.file(clean(fname) or "")
        if heading or home_rel is None or home_rel == carrier or home_rel.startswith(SKIP_CARRIERS):
            return
        self.pointers += 1
        home = self.home(home_rel)
        if single is not None:
            nums, text, full = [single], single, False
        else:
            nums = sorted(items_of(m.group("a"), m.group("b"), m.group("rest")), key=lambda x: (lead(x), x))
            text, full = m.group(0).strip(), m.group("b") is not None and re.match(r"1\b", m.group("a")) is not None
        missing = [x for x in nums if not home.has_item(x)]
        if missing:
            self.add(carrier, n, "R", text, "item %s absent; the home holds rules up to %d" % (",".join(missing), home.max), home_rel)
        elif full and max(lead(x) for x in nums) < home.max:
            self.add(carrier, n, "R", text, "a range from 1 is a full-set claim; the home holds rules up to %d" % home.max, home_rel)

    def anchor(self, carrier, n, fname, anchor):
        self.pointers += 1
        home_rel = self.tree.file(clean(fname) or "")
        if home_rel is None:
            self.add(carrier, n, "A", "%s § %s" % (fname, anchor), "the file is not tracked", fname)
        elif not self.home(home_rel).has_anchor(anchor):
            self.add(carrier, n, "A", "%s § %s" % (fname, anchor), "no such heading or item", home_rel)

    def toc(self, carrier, text):
        lines = text.splitlines()
        for _, heading, column in [t for t in TOC_TABLES if t[0] == carrier]:
            table = md_table.table_after(lines, heading)
            if table is None or column not in table[0]:
                raise CannotJudge("%s: table under '%s' with column '%s' not found" % (carrier, heading, column))
            ci = table[0].index(column)
            for cells, n in table[1]:
                for part in cells[ci].replace("`", "").split(" + "):
                    self.toc_part(carrier, n, part.strip())

    def toc_part(self, carrier, n, part):
        self.pointers += 1
        if "§" in part:
            left, anchor = (s.strip() for s in part.split("§", 1))
            fname = left.split("→")[-1].strip() or carrier
        elif SUFFIX_RE.search(part):
            return                                           # a bare file: the path kind judges it
        else:
            fname, anchor = carrier, part.split("→")[0].strip()
        home_rel = self.tree.file(fname)
        if home_rel is None:
            if not is_placeholder(fname):
                self.add(carrier, n, "A", part, "the file is not tracked", fname)
        elif not self.home(home_rel).has_anchor(anchor):
            self.add(carrier, n, "A", part, "no such heading or item", home_rel)

    def numbers(self):
        for spec, carrier, rx in NUMBER_PAIRS:
            want = read_constant(self.root, spec)
            p = self.root / carrier
            self.pointers += 1
            m = re.search(rx, p.read_text(encoding="utf-8")) if p.is_file() else None
            if m is None:
                self.add(carrier, 1, "N", rx, "the sentence is gone (a pair never passes silently); %s = %s" % (spec, want), spec)
                continue
            got = number_value(m.group(1))
            line = p.read_text(encoding="utf-8")[:m.start()].count("\n") + 1
            if got is None:
                self.add(carrier, line, "N", m.group(1), "not a number or a known number word; %s = %s" % (spec, want), spec)
            elif got != want:
                self.add(carrier, line, "N", m.group(0), "%s = %s, the text says %s" % (spec, want, got), spec)

    def finish(self, texts):
        """D3 step 5 (git check-ignore) and step 6 (exemption rows) for the pending paths; then the stale rows."""
        local = ignored({t for _, _, t in self.pending if not is_placeholder(t) and not t.startswith(("./", "../"))}, self.root)
        for carrier, n, tok in self.pending:
            if tok in local:
                continue
            key = "%s|%s" % (carrier, tok)
            if key in self.exempt:
                self.used.add(key)
                continue
            self.add(carrier, n, "P", tok, "not a tracked path", "-", key)
        for key, row in sorted(self.exempt.items()):
            carrier, _, tok = key.partition("|")
            if not str(row.get("why", "")).strip():
                self.add(EXEMPT_FILE, 1, "X", key, "the row has no why", "-")
            if key in self.used:
                continue
            gone = tok not in texts.get(carrier, "").replace("\\", "/")
            self.add(EXEMPT_FILE, 1, "X", key, "stale: the token left the carrier" if gone else "stale: the pointer resolves without the row", "-")


def run(root):
    absent = []
    main = [m for m in main_documents(root, absent) if not m.startswith(SKIP_CARRIERS)]
    missing = [c for c in CONTROL_DOCS if c not in main]
    if missing:
        raise CannotJudge("register of %s: control documents not parsed: %s" % (SIBLING_MAP, ", ".join(missing)))
    fr_max, p_max = home_max(root, FR_HOME), home_max(root, P_HOME)
    lint = Lint(root)
    texts = {}
    for rel in main + [c for c in {t[0] for t in TOC_TABLES} | {c for _, c, _ in NUMBER_PAIRS} if c not in main]:
        texts[rel] = (root / rel).read_text(encoding="utf-8", errors="replace")
    for rel in main:
        lint.scan(rel, texts[rel], fr_max, p_max)
    for rel, text in texts.items():
        lint.toc(rel, text)
    for path, n in absent:
        lint.add(SIBLING_MAP, n, "P", path, "the register row names a file that is not in the tree", "-", "%s|%s" % (SIBLING_MAP, path))
    lint.numbers()
    lint.finish(texts)
    return lint, len(main)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true", required=True)
    ap.add_argument("--repo", default=str(Path(__file__).resolve().parents[1]))
    args = ap.parse_args(argv)
    sys.stdout.reconfigure(encoding="utf-8")
    start = time.perf_counter()
    root = Path(args.repo)
    try:
        lint, files = run(root)
    except (CannotJudge, OSError, UnicodeError, SyntaxError) as exc:
        print("pointer_lint: cannot judge: %s" % exc)
        return 2
    seen, finds = set(), []
    for f in lint.finds:
        if f[:4] not in seen:
            seen.add(f[:4])
            finds.append(f)
    if finds:
        print("pointer_lint: %d finding(s)" % len(finds))
        for carrier, n, kind, ptr, what, home, key in sorted(finds, key=lambda f: (f[0], f[1], f[3])):
            door = DOOR % tuple((key or "%s|%s" % (carrier, ptr)).split("|", 1)) if key else "fix the pointer or the home"
            print("%s:%d: [%s] %s -> %s (home: %s) -- door: %s" % (carrier, n, kind, ptr, what, home, door))
    else:
        print("pointer_lint: ok (%d files, %d pointers)" % (files, lint.pointers))
    print("pointer_lint: %.2fs" % (time.perf_counter() - start), file=sys.stderr)
    return 1 if finds else 0


if __name__ == "__main__":
    sys.exit(main())
