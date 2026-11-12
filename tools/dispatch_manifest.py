"""dispatch_manifest.py -- the dispatch completeness check (B-201, piece A) and
THE ONE CUT of a dispatch text (B-204, t-608 / Axis 13).

A PURE module: no I/O of any kind (no print, no stderr, no file access, no
directory listing): it returns or raises. Exit 2 = the dispatch does not go out
(`message` says what is missing); exit 0 = it goes out, `note` (possibly "") is
a visible remark for the coordinator.

THE CUT. `section_cut(prompt) -> DispatchCut` is the ONE md_regions scan per
prompt and the one place the header grammar is applied: lines, offsets, a
per-line `quoted` flag (dispatch_gate._is_quoted at the line start; an
unterminated fence is prose), the sections (item -> [Section]), the skip lines,
the owns-shaped headers inside quoted lines and the block. Every reader of a
dispatch's sections reads the cut, never a private line scan:
 * `check_cut(cut, is_builder)` -- the completeness check (`check(payload)` is
   its payload wrapper and keeps the pinned 3-tuple);
 * `owned_paths(cut)` -- the one reader of owned paths (union of the owns
   sections; owns_gate registers exactly these);
 * `has_owned_paths(text, include_quoted=False)` -- the one yes/no "does this dispatch text declare an
   owned path" on that reader: handoff_gate asks the same thing of its own cut, the parallel-writer limit of dispatch_gate asks
   it with include_quoted=True (t-855, F6-8: one header grammar, one answer for a relative-only owns);
 * `given_paths(cut, top_entries)` -- the paths of the given sections;
 * `handoff_paths(cut)` -- the absolute paths of the handoff sections (same loop as given_paths);
 * `path_candidates(line, top_entries)` -- the one predicate "is this word a
   path" (absolute, OR backticked with a slash and no whitespace, OR a first
   segment that is a top-level entry of the root). The caller lists the root
   (`top_entries`): this module stays I/O-free.
A scan that raises, or a degraded scan (text over md_regions.MAX_TEXT_CHARS,
too many regions or inline spans), gives a DEGRADED cut: every line is prose,
`degraded` is True, `reason` is kept. The checker then returns the UNCHECKED
note (exit 2 only from a complete read); the registry reads the same all-prose
cut (the allowed direction: more).

WHAT IS CHECKED. `subagent_type.strip().lower() == "builder"` always; any
other type only when its prompt has an owns section with at least one owned
(absolute) path -- a "writing" dispatch. Everything else: (0, "", "").

THE FORM a checked dispatch must carry (each header line OUTSIDE a fenced or
blockquote region, see _HEADER_RE): given:, owns: (absolute paths), non-goals:,
handoff:, edges:, DoD: (with a command: an inline-code span or a fenced line
of 2 or more whitespace-separated tokens), siblings: (entries, or `none -- <why>` with the reason on the
same line; FORM only, never sufficiency) and, from DESIGNER_THRESHOLD owned paths or numbered items
(designer_threshold), designer: (an absolute path, `skip -- <why>` or `resubmission t-<id>`).
A section's extent for these two (section_extent) ends at the first blank line. For these two NEW keys only, a
line is a header only when nothing but markup or a parenthetical stands between the key word and the colon
(`Siblings (axis 13):` is a header, `neighbours once at the end:` is prose and cuts nothing; t-113 F1).

QUOTED TEXT NEVER COUNTS. A header or skip line inside a fence or blockquote
(dispatch_gate._is_quoted decides; an unterminated fence counts as prose, for
the checker AND the registry -- one polarity) is not a header. The one place
quoted text is looked at on purpose: a line inside a terminated fence (not
inside a blockquote) under the DoD section counts as a command.

IMPORTS. md_regions, dispatch_gate (only `_is_quoted`, `is_path_like_token`)
and owns_gate (only the token helpers) are imported LAZILY inside the
functions: a failed import raises out (piece B turns it into an UNCHECKED
note), and no import cycle can arise when dispatch_gate imports this module.

Named open limits, pinned by tests as current behaviour: an absolute path
merely mentioned in the owns section counts; a bullet path with spaces and
no backticks is cut at the first space; a prose line like "Given the above,
...:" counts as a given header (the PATH check treats such a header as "not a
bare declaration" and only notes); two owns sections are a union; a
deliberate degraded read lets a dispatch out (with the UNCHECKED note).
"""

import bisect
import itertools
import re
import sys
from pathlib import Path
from typing import NamedTuple

# --- texts (verbatim from the spec, "Texts") ----------------------------


# --- the one KEY constant -----------------------------------------------

# (item, display name in messages, header-key alternation)
KEY_GROUPS = (
    ("given", "given", r"given|дано"),
    ("owns", "owns", r"owns"),
    ("non-goals", "non-goals", r"non-goals?"),
    ("handoff", "handoff", r"hand-?off"),
    ("edges", "edges", r"edges?|edge behaviou?r"),
    ("dod", "DoD", r"dod|witness|verification"),
    ("siblings", "siblings", r"siblings?|neighbou?rs"),
    ("designer", "designer", r"designer"),
)
ITEMS = tuple(k[0] for k in KEY_GROUPS)
_DISPLAY = {k[0]: k[1] for k in KEY_GROUPS}
_GROUP_TO_ITEM = {"g%d" % i: k[0] for i, k in enumerate(KEY_GROUPS)}

# The form switch (F-E4): True = a missing/ill-formed siblings line, and a missing designer line over the
# threshold, REFUSE the dispatch; False = both are still checked and a miss goes out as a NOTE
# (FORM_NOT_ENFORCED_NOTE_TEMPLATE), never silently (t-113 F3, FR-4).
DISPATCH_FORM_REFUSES = True
# The manifest sections whose extent does not count numbered lines towards the designer threshold (F-E7: `dod`
# is NOT in the set -- numbered acceptance criteria are spec items; `edges` is).
ITEM_EXCLUDED_SECTIONS = ("given", "owns", "non-goals", "handoff", "edges", "siblings", "designer")
DESIGNER_THRESHOLD = 3  # owned paths or numbered items: at or over it, a designer line is required

# What each item's expected form says in the INCOMPLETE text (item -> text after the "name:"; "" = none).
_FORM_HINTS = {
    "given": "(files/data the worker gets; a pointer to a persisted spec is allowed)",
    "owns": ("(the absolute paths the worker may write, never by pointer; on the owns line itself or on the "
             "lines right under it, with no blank line and no heading marks; a path with spaces in backticks)"),
    "non-goals": "",
    "handoff": "",
    "edges": "(the behavior at each limit, empty input and conflicting pair, or 'edges: none -- <why>')",
    "dod": "(with the exact verification command in backticks, two words or more)",
    "siblings": ("(the neighbours the change must also touch or check: paths or 'axis N', or "
                 "'siblings: none -- <why>' with the reason on the same line)"),
    "designer": ("(required only from %d owned paths or %d numbered items: the absolute path of the accepted "
                 "draft, 'designer: skip -- <reason>' or 'designer: resubmission t-<id>')"
                 % (DESIGNER_THRESHOLD, DESIGNER_THRESHOLD)),
}
# The two items whose form DISPATCH_FORM_REFUSES switches between a refusal and a note (F3).
_FORM_ITEMS = ("siblings", "designer")
# The two NEW keys whose header must be a bare declaration: only markup or a parenthetical between the key word
# and the colon (t-113 F1); the six older keys keep the wide grammar of _HEADER_RE.
_BARE_HEADER_ITEMS = ("siblings", "designer")


def _expected_forms() -> str:
    parts = []
    for item, display, _alt in KEY_GROUPS:
        hint = _FORM_HINTS.get(item, "")
        parts.append("%s:%s" % (display, " " + hint if hint else ""))
    return ", ".join(parts)


INCOMPLETE_TEMPLATE = (
    "DISPATCH INCOMPLETE (CLAUDE.md rule 11): this {kind} dispatch does not go out. "
    "Missing: {items}. Expected, each as its own line outside code fences and quotes, "
    "starting with its name and a colon: " + _expected_forms() + ". "
    "To send it anyway on purpose, add a line: manifest-skip: <item>[, <item>] -- <reason>"
)
SKIP_REFUSED_TEMPLATE = (
    "MANIFEST-SKIP REFUSED: '{line}' -- {why}. Expected: manifest-skip: <item>[, <item>] "
    "-- <reason>; items: " + ", ".join(ITEMS) + "; the reason is not empty."
)
SKIP_NOTE_TEMPLATE = (
    'MANIFEST-SKIP: dispatch sent without {items} on purpose: "{reason}" -- '
    "the line stays in the prompt as the record."
)
UNCHECKED_NOTE_TEMPLATE = (
    "MANIFEST-UNCHECKED: this dispatch was not checked for completeness ({what}) -- it went "
    "out; check " + ", ".join(k[1] for k in KEY_GROUPS[:-1]) + " and " + KEY_GROUPS[-1][1] + " by eye."
)
DESIGNER_SKIP_NOTE_TEMPLATE = (
    'DESIGNER-SKIP: this dispatch is over the designer threshold and carries "designer: skip -- {reason}" -- '
    "a dispatch_skipped(agent=designer) event is owed (CLAUDE.md rule 2)."
)
FORM_NOT_ENFORCED_NOTE_TEMPLATE = (
    "SIBLINGS/DESIGNER NOT ENFORCED (DISPATCH_FORM_REFUSES is off): this dispatch went out missing {items}; "
    "add the line(s) in the form the INCOMPLETE text names."
)
WHAT_DEGRADED = "quoted regions could not be read reliably"

HEADER_KEY_LIMIT = 160  # characters between the key and the colon

_HEADER_RE = re.compile(
    r"^[ \t]*(?:[-*•][ \t]+)?(?:\*\*|#{1,6}[ \t]+)?"
    r"(?:" + "|".join("(?P<g%d>%s)" % (i, k[2]) for i, k in enumerate(KEY_GROUPS)) + r")"
    r"\b[^\n:]{0,%d}:" % HEADER_KEY_LIMIT,
    re.IGNORECASE,
)
_SKIP_PREFIX_RE = re.compile(r"^[ \t]*(?:[-*•][ \t]+)?manifest-skip:", re.IGNORECASE)
_SEP = r"--|—"  # THE reason separator: manifest-skip, siblings 'none -- <why>', designer 'skip -- <why>'
_SKIP_SEP_RE = re.compile(_SEP)
_OWNS_WORD_RE = re.compile(r"\bowns\b", re.IGNORECASE)
_INLINE_SPAN_RE = re.compile(r"(?<!`)(`+)(?!`)(.+?)(?<!`)\1(?!`)")
_ABS_TOKEN_RE = re.compile(r"^(?:[A-Za-z]:[\\/]|/)")
_TOKEN_STRIP = "`'\""
# THE section-stop regex (owns_gate and dispatch_gate import it): the closed set
# of manifest sections that ends an owns continuation line.
SECTION_STOP_RE = re.compile(
    r"^\s*(?:\*\*)?(given|дано|owns|non-goals|handoff|siblings?|neighbou?rs|designer)\b", re.IGNORECASE)
_QUOTE_PREFIX_RE = re.compile(r"^(?: {0,3}>[ \t]?)+")
# a header is a "bare declaration" when only a parenthetical / markup sits between key and colon
_GAP_RE = re.compile(r"(?:[ \t]*\([^)]*\))?[ \t*_]*")

PATH_CAP = 200  # candidate paths checked per dispatch (the caller applies it)

# The folder of a role's hand-back report file (t-744 F-3), as the LAST path segments (compared by
# trailing segments, never from a cwd). Data, not code (FR-13): tools/handoff_gate.py gates the reading
# kinds by it, tools/agent_budget.py lets a worker at the STOP cap write into these folders.
HANDOFF_DIRS = {
    "critic": "docs/tasks/specs/reviews",
    "designer": "docs/tasks/specs",
    "builder": "docs/tasks/handoffs",
    "scout": "docs/tasks/specs/reports",
}


class Section(NamedTuple):
    item: str
    header_line: int
    last_line: int
    tail_start: int
    body: str
    full: str


class DispatchCut(NamedTuple):
    text: str
    lines: list
    offsets: list
    quoted: bytearray  # per line: 1 = inside a fence/blockquote (an unterminated fence is prose)
    regions: list
    degraded: bool
    reason: str
    sections: dict  # item -> [Section]
    skips: list  # line indexes of manifest-skip lines (outside quoted lines)
    quoted_owns_headers: list  # line indexes: owns-shaped headers INSIDE quoted lines
    block: object  # (first header line, last line of the last section) | None
    unterminated: list  # (first line, last line) of every unterminated fence


class OwnedPath(NamedTuple):
    path: str
    is_new: bool
    line: int
    header_line: int


class GivenPath(NamedTuple):
    path: str
    line: int
    header_line: int
    marked_new: bool


def _import_siblings():
    """Lazy sibling imports (see the module docstring, IMPORTS). Any failure
    propagates."""
    tools_dir = str(Path(__file__).resolve().parent)
    if tools_dir not in sys.path:
        sys.path.insert(0, tools_dir)
    import md_regions
    import dispatch_gate
    import owns_gate

    return md_regions, dispatch_gate, owns_gate


def _unchecked(what: str) -> str:
    return UNCHECKED_NOTE_TEMPLATE.format(what=what)


def _parse_skip_line(line: str):
    """(items, reason, None) for a valid skip line, (None, None, why) for a
    malformed one. `line` starts (after whitespace and one bullet) with
    'manifest-skip:'."""
    rest = line[_SKIP_PREFIX_RE.match(line).end():]
    sep = _SKIP_SEP_RE.search(rest)
    if sep is None:
        # no separator at all: decided BEFORE the items are looked at
        return None, None, "no reason after --"
    items_part, reason = rest[: sep.start()], rest[sep.end():]
    items = []
    for raw in items_part.split(","):
        name = raw.strip().lower()
        if name not in ITEMS:
            return None, None, "unknown item '%s'" % raw.strip()
        items.append(name)
    if not reason.strip():
        return None, None, "no reason after --"
    return items, reason.strip(), None


def _tokens_ok(text: str) -> bool:
    return len(text.split()) >= 2


# --- the cut ---------------------------------------------------------------


def _scan(md_regions, text):
    """(regions, degraded, reason). A scan that raises is a degraded read (the
    module-failure contract): every line is prose, the reason is kept."""
    try:
        result = md_regions.scan(text)
    except Exception as exc:
        return [], True, "scan raised: %s" % type(exc).__name__
    return result.regions, result.degraded, result.reason


def _mark_quoted(dispatch_gate, md_regions, regions, n_lines):
    """(quoted bytearray, unterminated fences). One pass over the regions (a
    fenced/blockquote region covers whole lines), polarity = _is_quoted."""
    quoted = bytearray(n_lines)
    unterminated = []
    for r in regions:
        if dispatch_gate._is_quoted(r):
            lo, hi = r.line_start, min(r.line_end, n_lines - 1)
            if hi >= lo:
                quoted[lo:hi + 1] = b"\x01" * (hi - lo + 1)
        elif md_regions.KIND_FENCED in r.kinds and r.unterminated:
            unterminated.append((r.line_start, r.line_end))
    return quoted, unterminated


def _is_header(line: str, m) -> bool:
    """False for a line of a NEW key (_BARE_HEADER_ITEMS) whose gap between the key word and the colon is not a
    bare declaration (`neighbours once at the end: ...`, `Siblings of X: ...` are prose, never a header and never
    the end of the section above them); True for every match of the six older keys (their grammar unchanged)."""
    if _GROUP_TO_ITEM[m.lastgroup] not in _BARE_HEADER_ITEMS:
        return True
    return bool(_GAP_RE.fullmatch(line[m.end(m.lastgroup):m.end() - 1]))


def section_cut(prompt: str) -> DispatchCut:
    """The ONE cut of a dispatch text: pure, one md_regions scan, built once per
    prompt. See the module docstring."""
    md_regions, dispatch_gate, _owns_gate = _import_siblings()
    if not isinstance(prompt, str):
        prompt = ""
    regions, degraded, reason = _scan(md_regions, prompt)
    lines = prompt.splitlines()
    n = len(lines)
    offsets = [0]
    offsets.extend(itertools.accumulate(map(len, prompt.splitlines(True))))
    offsets.pop()
    if degraded:
        quoted, unterminated = bytearray(n), []
    else:
        quoted, unterminated = _mark_quoted(dispatch_gate, md_regions, regions, n)

    events = []  # (line_index, "header", item, tail_start) | (line_index, "skip", None, None)
    skips = []
    quoted_owns = []
    for li, line in enumerate(lines):
        if not line or line[0] == "`":
            continue
        header = _HEADER_RE.match(line)
        if header is not None and not _is_header(line, header):
            header = None
        skip = None if header else _SKIP_PREFIX_RE.match(line)
        if header is None and skip is None:
            if quoted[li] and _OWNS_WORD_RE.search(line):
                dequoted = _QUOTE_PREFIX_RE.sub("", line)
                qh = _HEADER_RE.match(dequoted)
                if qh is not None and _GROUP_TO_ITEM[qh.lastgroup] == "owns":
                    quoted_owns.append(li)
            continue
        if quoted[li]:
            if header is not None and _GROUP_TO_ITEM[header.lastgroup] == "owns":
                quoted_owns.append(li)
            continue
        if header is not None:
            events.append((li, "header", _GROUP_TO_ITEM[header.lastgroup], header.end()))
        else:
            events.append((li, "skip", None, None))
            skips.append(li)

    sections = {item: [] for item in ITEMS}
    for k, (li, kind, item, tail) in enumerate(events):
        if kind != "header":
            continue
        end = events[k + 1][0] if k + 1 < len(events) else n
        body = lines[li][tail:] + "\n" + "\n".join(lines[li + 1:end])
        sections[item].append(Section(item, li, end - 1, tail, body, "\n".join(lines[li:end])))
    headers = [e for e in events if e[1] == "header"]
    last_end = max((s.last_line for secs in sections.values() for s in secs), default=None)
    block = (headers[0][0], last_end) if headers else None
    return DispatchCut(prompt, lines, offsets, quoted, regions, degraded, reason,
                       sections, skips, quoted_owns, block, unterminated)


def fence_start(cut: DispatchCut, line: int):
    """The 0-based line of the unterminated fence that holds `line`, or None."""
    for lo, hi in cut.unterminated:
        if lo <= line <= hi:
            return lo
    return None


def waivers(cut: DispatchCut) -> dict:
    """item -> reason of the first VALID manifest-skip line naming it (a
    malformed line waives nothing; the completeness check refuses it)."""
    out = {}
    for li in cut.skips:
        items, reason, why = _parse_skip_line(cut.lines[li])
        if why is None:
            for i in items:
                out.setdefault(i, reason)
    return out


def unsure_reason(cut: DispatchCut, header_line: int, line: int):
    """None when the PATH check may refuse on a path read from `line` of the
    section headed at `header_line`; otherwise the reason the path is only
    noted (P20: the header is prose between key and colon; P21: the line sits
    in an unterminated fence -- exit 2 only from a line whose quoting is certain)."""
    text = cut.lines[header_line]
    m = _HEADER_RE.match(text)
    if m is not None:
        gap = text[m.end(m.lastgroup):m.end() - 1]
        if not _GAP_RE.fullmatch(gap):
            return "header `%s` is not a bare declaration" % text[:m.end()].strip()
    opened = fence_start(cut, line)
    if opened is None:
        opened = fence_start(cut, header_line)
    if opened is not None:
        return "inside an unterminated fence opened at line %d" % (opened + 1)
    return None


# --- (new) marker, owned paths, given paths ---------------------------------

_NEW_RE = re.compile(r"[ \t]*\(new\)", re.IGNORECASE)
_PATH_START_RE = re.compile(r"(?:^|(?<=[\s`\"'«:*(\[]))(?:[A-Za-z]:[\\/]|/)")
_NOTE_TRIM = "`\"'»).,;: \t"


def split_new_marker(line: str):
    """(line_without_markers, new_paths). `(new)` is read PER PATH at line
    level: new_paths holds the path text that immediately precedes each marker
    (`owns: A (new), B` -> {A}). Every other bracket is a note, not a marker."""
    marks = list(_NEW_RE.finditer(line))
    if not marks:
        return line, set()
    new = set()
    for m in marks:
        before = re.split(r"[;,]", line[:m.start()])[-1]
        starts = [s.start() for s in _PATH_START_RE.finditer(before)]
        text = (before[starts[-1]:] if starts else before).strip().strip(_NOTE_TRIM)
        if text:
            new.add(text)
    return _NEW_RE.sub("", line), new


def _cut_note(raw: str) -> str:
    """P19: a note in brackets after a path is cut at the first ' (' -- unless
    the token is an explicit span in quotes/backticks. A span that is CLOSED and followed by ' (' is cut after
    the closing mark (t-877, D-0048: `C:\\x\\story_run.py` (take_answer, last_resort) names the path, not the
    path with its function list); a span with no closing mark, or with no bracket after it, stays whole."""
    s = raw.strip()
    if s[:1] in ("`", '"', "'"):
        close = s.find(s[0], 1)
        if close > 0 and s[close + 1:].lstrip().startswith("(") and s[close + 1:close + 2].isspace():
            return s[:close + 1]
        return s
    idx = s.find(" (")
    return s[:idx].rstrip() if idx > 0 else s


_SPAN_FN_LIST_RE = re.compile(r"`([^`\n]*?\S)\s+\(\s*[+\w.]+(?:\s*,\s*[+\w.]+)*\s*\)`")


def _cut_span_lists(remainder: str) -> str:
    """t-880 F-5 (D-0048, form 1 of a function list): `C:\\x\\y.py (f1, f2)` INSIDE one backtick span is cut to `C:\\x\\y.py`
    BEFORE the token split (the comma of the list would split the span). Only a bracket of function names ([+]name[.name],
    comma-separated) that closes the span is cut; a span with any other bracket (a path with parentheses) stays whole."""
    return _SPAN_FN_LIST_RE.sub(r"`\1`", remainder)


def _header_paths(og, line: str, new: set):
    """[(path, is_new)] from the tail of an owns header line (marker-line
    priority: the caller reads a continuation only when this is empty)."""
    m = _OWNS_WORD_RE.search(line)
    if m is None:
        return [], None
    remainder = _cut_span_lists(og._strip_owns_marker_junk(line[m.end():]))
    found = []
    for raw in og._TOKEN_SEPARATOR_RE.split(remainder):
        toks = og.split_and_clean_tokens(_cut_note(raw))
        tok = toks[0] if toks else ""
        if tok and og.is_path_token(tok):
            found.append((tok, tok in new))
    return found, m


def _continuation(og, cut: DispatchCut, header_line: int, last_line: int, in_quote: bool = False):
    """[(path, is_new, line)] -- the lines under the header; [] at the
    CONTINUATION_LINE_LIMIT (an explicit blindness, not a truncation). `in_quote`: the header itself sits
    inside a fence or blockquote, so the lines under it are read with the quote mark stripped and a quoted
    line does not end the run."""
    found = []
    for idx in range(header_line + 1, last_line + 1):
        line = _QUOTE_PREFIX_RE.sub("", cut.lines[idx]) if in_quote else cut.lines[idx]
        if line.strip() == "" or SECTION_STOP_RE.match(line) or (cut.quoted[idx] and not in_quote):
            break
        line2, new = split_new_marker(line)
        tok = og._first_token_path(_cut_span_lists(line2))
        if tok is None:
            break
        if len(found) >= og.CONTINUATION_LINE_LIMIT:
            return []
        found.append((tok, tok in new, idx))
    return found


def _owns_items(og, cut: DispatchCut, header_line: int, last_line: int, text: str, in_quote: bool = False):
    """[(path token, is_new, line)] of one owns header (`text` is its line, quote mark already stripped for a
    quoted one): the header line itself (marker-line priority) or, when that line is a bare declaration
    without a path, the lines under it. Tokens are not yet filtered to absolute."""
    line, new = split_new_marker(text)
    found, m = _header_paths(og, line, new)
    items = [(p, n, header_line) for p, n in found]
    if not items and m is not None and og._is_owns_declaration_line(line, m.start(), m.end()):
        items = _continuation(og, cut, header_line, last_line, in_quote)
    return items


def owned_paths(cut: DispatchCut) -> list:
    """THE one reader of owned paths: the union over every owns section of the
    absolute paths of its header line (marker-line priority) or, when that line
    is a bare declaration without a path, of the lines under it. Relative
    paths and relative globs are dropped (R11-f demands absolute)."""
    og = _import_siblings()[2]
    out, seen = [], set()
    for sec in cut.sections["owns"]:
        for tok, is_new, li in _owns_items(og, cut, sec.header_line, sec.last_line, cut.lines[sec.header_line]):
            tok = tok.strip().strip(_TOKEN_STRIP)
            if _ABS_TOKEN_RE.match(tok) and tok not in seen:
                seen.add(tok)
                out.append(OwnedPath(tok, is_new, li, sec.header_line))
    return out


def has_owned_paths(text, include_quoted: bool = False) -> bool:
    """THE one answer to "does this dispatch text declare an owned path" -- a writing dispatch or worker.
    Default: exactly the question tools/handoff_gate.py asks, bool(owned_paths(section_cut(text))): an owns
    HEADER line outside a fence and a blockquote with at least one ABSOLUTE path; prose that says "owns" is
    not a declaration, and an owns of relative paths only is not one either (the class's one rule: a relative
    path is no declaration, for the parallel-writer limit and handoff_gate alike). Not a str / empty -> False.
    `include_quoted` (the parallel-writer limit, D-0040, passes True): an owns header with an absolute path
    INSIDE a fence or blockquote counts too -- the pinned answer of t-847, the safe side of the limit (it
    counts a worker, it never lets a fifth through on a quoted example); handoff_gate does not pass it."""
    if not isinstance(text, str) or not text:
        return False
    cut = section_cut(text)
    if owned_paths(cut):
        return True
    if not include_quoted:
        return False
    og = _import_siblings()[2]
    last = len(cut.lines) - 1
    for li in cut.quoted_owns_headers:
        items = _owns_items(og, cut, li, last, _QUOTE_PREFIX_RE.sub("", cut.lines[li]), in_quote=True)
        if any(_ABS_TOKEN_RE.match(tok.strip().strip(_TOKEN_STRIP)) for tok, _new, _line in items):
            return True
    return False


_PLACEHOLDER_RE = re.compile(r"[<>{}$|]")
_ABS_PATH_RE = re.compile(r"^(?:[A-Za-z]:[\\/]+[^\\/\s]|/+[^/\s])")
_ANCHOR_RE = re.compile(r"^(.*\.[A-Za-z0-9_]{1,10})(?:~?:\d[\w\-:,]*|::\S+|#\S*)$")
_WORD_RE = re.compile(r"[^\s,;]+")
_WORD_EDGE = "\"'()[]«»"
_WORD_TAIL = ".,;:!?"
_SEG_SPLIT_RE = re.compile(r"[\\/]")


def _clean_word(w: str) -> str:
    w = w.strip(_WORD_EDGE).rstrip(_WORD_TAIL)
    m = _ANCHOR_RE.match(w)
    if m:
        w = m.group(1)
    return w.rstrip(_WORD_TAIL + _WORD_EDGE)


def path_candidates(line: str, top_entries=None) -> list:
    """THE one predicate "is this a path" for a line of dispatch text, in order
    of appearance, deduplicated. A candidate is: an absolute path (drive or
    slash start); OR a backticked span with a slash and no whitespace (P22: a
    span with whitespace only when it is absolute, `C:\\a b\\x.py` stays one
    token); OR a word whose first segment is an entry of `top_entries` (the
    root's top-level names, supplied by the caller; None switches the rule
    off). Never a candidate: a URL, a placeholder (<x> {x} $X), prose. An
    anchor after an extension (`:12-30`, `~:5`, `::t`, `#L9`) and trailing
    `. , ) ;` are stripped, the drive colon kept; a note in brackets is a
    separate word and never part of the path (P19)."""
    found = []
    spans = []
    for m in _INLINE_SPAN_RE.finditer(line):
        spans.append(m)
        s = m.group(2).strip()
        if _PLACEHOLDER_RE.search(s) or "://" in s:
            continue
        s = _clean_word(s)
        if _ABS_PATH_RE.match(s) or (s and not any(c.isspace() for c in s) and _SEG_SPLIT_RE.search(s)):
            found.append((m.start(), s))
    rest = _INLINE_SPAN_RE.sub(lambda mm: " " * len(mm.group(0)), line) if spans else line
    entries = top_entries if top_entries is not None else ()
    low = sys.platform == "win32"
    for m in _WORD_RE.finditer(rest):
        w = _clean_word(m.group(0))
        if not w or "://" in w or _PLACEHOLDER_RE.search(w):
            continue
        if _ABS_PATH_RE.match(w):
            found.append((m.start(), w))
        elif entries and _SEG_SPLIT_RE.search(w):
            first = _SEG_SPLIT_RE.split(w, 1)[0]
            if first in entries or (low and first.lower() in entries):
                found.append((m.start(), w))
    out, seen = [], set()
    for _pos, p in sorted(found, key=lambda t: t[0]):
        if p not in seen:
            seen.add(p)
            out.append(p)
    return out


def section_extent(cut: DispatchCut, sec: Section) -> int:
    """THE one definition of a section's extent for the siblings form, the designer line and the item count
    (t-098 B3): the header line plus its continuation lines up to (excluding) the FIRST BLANK LINE, never past
    the section's last line (the next header). Returns the index of the last line of the extent (quoted lines
    inside it are part of the extent; the readers skip them). `Section.body` stays the wide read to the next header."""
    idx = sec.header_line
    while idx < sec.last_line and cut.lines[idx + 1].strip():
        idx += 1
    return idx


def _section_paths(cut: DispatchCut, item: str, top_entries=None) -> list:
    """[GivenPath] of every section of `item`: the header tail and the lines under it
    up to the FIRST BLANK LINE, never past the section's last line (P23: a
    continuation never crosses a header); quoted lines are not read (P10). The ONE
    loop of given_paths and handoff_paths."""
    out, seen = [], set()
    for sec in cut.sections[item]:
        for idx, text in _extent_lines(cut, sec):
            text2, new = split_new_marker(text)
            for p in path_candidates(text2, top_entries):
                if p not in seen:
                    seen.add(p)
                    out.append(GivenPath(p, idx, sec.header_line,
                                         p in new))
    return out


def given_paths(cut: DispatchCut, top_entries=None) -> list:
    """The paths of the given sections (see _section_paths)."""
    return _section_paths(cut, "given", top_entries)


def handoff_paths(cut: DispatchCut) -> list:
    """The ABSOLUTE paths (str, in order of appearance, deduplicated) of the handoff sections, read by the
    same loop as given_paths: a relative path, a placeholder (`<t>`) and a quoted line are never a path. The
    caller (tools/handoff_gate.py) decides which of them lies in a role's folder (HANDOFF_DIRS)."""
    return [g.path for g in _section_paths(cut, "handoff") if _ABS_PATH_RE.match(g.path)]


# --- the completeness check --------------------------------------------------


def _command_lines(cut: DispatchCut):
    """Sorted line indexes holding an inline span / a fenced line of >= 2 tokens."""
    md_regions = _import_siblings()[0]
    lines, text = cut.lines, cut.text
    command_lines = set()
    for r in cut.regions:
        kinds = r.kinds
        if kinds == (md_regions.KIND_INLINE_CODE,):
            if _tokens_ok(text[r.start:r.end].strip("`")):
                command_lines.add(r.line_start)
        elif kinds == (md_regions.KIND_FENCED,):
            if r.unterminated:
                # an unterminated fence counts as prose: look for spans by hand
                for li in range(r.line_start, r.line_end + 1):
                    for m in _INLINE_SPAN_RE.finditer(lines[li]):
                        if _tokens_ok(m.group(2)):
                            command_lines.add(li)
            else:
                for li in range(r.line_start + 1, r.line_end):  # not the two delimiter lines
                    if _tokens_ok(lines[li]):
                        command_lines.add(li)
    return sorted(command_lines)


def cut_payload(payload):
    """(is_builder, cut | None) for a payload; None = not a checked kind by the
    cheap exit (a non-builder whose prompt lacks the word 'owns'). Raises
    TypeError on a payload / tool_input that is not a dict."""
    if not isinstance(payload, dict):
        raise TypeError("payload is not a dict: %s" % type(payload).__name__)
    tool_input = payload.get("tool_input")
    if not isinstance(tool_input, dict):
        raise TypeError("tool_input is not a dict: %s" % type(tool_input).__name__)
    subagent_type = tool_input.get("subagent_type")
    is_builder = isinstance(subagent_type, str) and subagent_type.strip().lower() == "builder"
    prompt = tool_input.get("prompt")
    if not isinstance(prompt, str):
        prompt = ""
    if not is_builder and not _OWNS_WORD_RE.search(prompt):
        return is_builder, None  # no owns header is possible without the word
    return is_builder, section_cut(prompt)


_NUMBERED_RE = re.compile(r"^\s*\d+[.)]\s")
_BULLET_OR_NUMBER_RE = re.compile(r"^\s*(?:[-*•]\s+\S|\d+[.)]\s+\S)")
_AXIS_RE = re.compile(r"\baxis\s+\d+", re.IGNORECASE)
_TAIL_JUNK = "*_ \t"
# A siblings tail that is one of these words alone (trailing punctuation allowed) says "no siblings" with no
# reason: refused like a bare `none` (t-113 F6). Data, not regex branches.
_BARE_NONE_WORDS = ("none", "n/a", "-", "–", "—")
_BARE_NONE_RE = re.compile(
    r"(?:" + "|".join(re.escape(w) for w in _BARE_NONE_WORDS) + r")[\s.:;,\-–—]*", re.IGNORECASE)
# The no-siblings answer: `none` + a separator of the spec's four forms; it passes only when the reason after the
# separator holds at least one word character (t-113 F6: `none -- -` is a bare none).
_NONE_ANSWER_RE = re.compile(r"none\s*(?:" + _SEP + r"|\.|\()(?P<reason>.*)$", re.IGNORECASE)
_WORD_CHAR_RE = re.compile(r"\w")
# A repo-relative path token on a siblings continuation line (t-113 B2): segments, a slash, and a last segment
# with an extension -- or a trailing slash for a folder. Pure: no root listing. `and/or`, `tools/x` are not paths.
_REL_PATH_RE = re.compile(
    r"(?<![\w./\\-])(?:[\w.-]+/)+(?:[\w-][\w.-]*\.[A-Za-z0-9]{1,10}(?![\w/])|(?![\w.-]))")
_DESIGNER_SKIP_RE = re.compile(r"\s*skip\s*(?:" + _SEP + r")\s*(\S.*)$", re.IGNORECASE)
_DESIGNER_RESUBMISSION_RE = re.compile(r"\s*resubmission\s+t-\d+\b", re.IGNORECASE)


def _extent_lines(cut: DispatchCut, sec: Section):
    """[(index, text)] of the extent of `sec`: the header TAIL, then the unquoted continuation lines."""
    out = [(sec.header_line, cut.lines[sec.header_line][sec.tail_start:])]
    for idx in range(sec.header_line + 1, section_extent(cut, sec) + 1):
        if not cut.quoted[idx]:
            out.append((idx, cut.lines[idx]))
    return out


def _siblings_state(cut: DispatchCut):
    """None when a siblings section passes; otherwise the label of what is missing ('no line', 'empty',
    'bare none'). FORM only: whether the list is sufficient is never judged (P27)."""
    secs = cut.sections["siblings"]
    if not secs:
        return "no line"
    state = "empty"
    for sec in secs:
        lines = _extent_lines(cut, sec)
        tail = lines[0][1].strip(_TAIL_JUNK)
        if tail:
            answer = _NONE_ANSWER_RE.match(tail)
            if answer is not None and _WORD_CHAR_RE.search(answer.group("reason")):
                return None
            if answer is not None or _BARE_NONE_RE.fullmatch(tail):
                state = "bare none"  # the reason must sit on the header line, whatever follows
                continue
            return None
        for _idx, line in lines[1:]:
            if (_BULLET_OR_NUMBER_RE.match(line) or path_candidates(line) or _REL_PATH_RE.search(line)
                    or _AXIS_RE.search(line)):
                return None
    return state


def _designer_state(cut: DispatchCut):
    """(missing label | None, skip reason | None) of the designer line, read over its extent."""
    secs = cut.sections["designer"]
    if not secs:
        return "no line", None
    state = "empty"
    for sec in secs:
        for _idx, text in _extent_lines(cut, sec):
            body = text.strip(_TAIL_JUNK)
            if not body:
                continue
            state = "no absolute path, 'skip -- <reason>' or 'resubmission t-<id>'"
            m = _DESIGNER_SKIP_RE.match(body)
            if m:
                return None, m.group(1).strip()
            if _DESIGNER_RESUBMISSION_RE.match(body):
                return None, None
            if any(_ABS_PATH_RE.match(p) for p in path_candidates(body)):
                return None, None
    return state, None


def designer_threshold(cut: DispatchCut):
    """(owns_count, items_count): the owned paths (the one reader) and the unquoted numbered lines
    (`^\\s*\\d+[.)]\\s`) lying in no extent of a section of ITEM_EXCLUDED_SECTIONS. Because extents end at
    the first blank line, a spec body written after the header block IS counted (t-098 B3)."""
    spans = [(s.header_line, section_extent(cut, s))
             for item in ITEM_EXCLUDED_SECTIONS for s in cut.sections[item]]
    items = 0
    for li, line in enumerate(cut.lines):
        if cut.quoted[li] or not _NUMBERED_RE.match(line):
            continue
        if not any(lo <= li <= hi for lo, hi in spans):
            items += 1
    return len(owned_paths(cut)), items


def _designer_trigger(counts) -> str:
    """Which count put the dispatch over the designer threshold (t-113 F5): '3 owned paths', '5 numbered items'
    or both."""
    owns_count, items_count = counts
    parts = []
    if owns_count >= DESIGNER_THRESHOLD:
        parts.append("%d owned paths" % owns_count)
    if items_count >= DESIGNER_THRESHOLD:
        parts.append("%d numbered items" % items_count)
    return " and ".join(parts)


def _form_missing(cut: DispatchCut, missing: dict):
    """Adds the siblings and designer labels to `missing` (always computed: DISPATCH_FORM_REFUSES only decides
    refusal vs note, F3); returns the designer skip reason (or None)."""
    state = _siblings_state(cut)
    if state:
        missing["siblings"] = state
    counts = designer_threshold(cut)
    if max(counts) < DESIGNER_THRESHOLD:
        return None
    state, skip_reason = _designer_state(cut)
    if state:
        missing["designer"] = "%s; over the threshold by %s" % (state, _designer_trigger(counts))
    return skip_reason


def _items_text(items, missing) -> str:
    return ", ".join("%s (%s)" % (_DISPLAY[i], missing[i]) for i in items)


def check_cut(cut, is_builder: bool):
    """The completeness check on a cut: (exit_code, message, note, checked).
    `checked` is True when the dispatch was evaluated as a builder / writing one
    (the path check runs only then)."""
    if cut is None:
        return 0, "", "", False
    if cut.degraded:
        return 0, "", _unchecked(WHAT_DEGRADED), False
    sections = cut.sections
    has_owned_path = bool(owned_paths(cut))
    if not is_builder and not has_owned_path:
        return 0, "", "", False
    kind_word = "builder" if is_builder else "writing"

    command_sorted = _command_lines(cut) if sections["dod"] else []

    def has_command(i0, i1):
        pos = bisect.bisect_left(command_sorted, i0)
        return pos < len(command_sorted) and command_sorted[pos] <= i1

    missing = {}
    for item in ITEMS:
        if item in _FORM_ITEMS:
            continue  # checked below by their own form readers
        secs = sections[item]
        if not secs:
            missing[item] = "no line"
            continue
        nonblank = [s for s in secs if s.body.strip()]
        if not nonblank:
            missing[item] = "empty"
            continue
        if item == "owns":
            if not has_owned_path:
                missing[item] = "no absolute path could be read"
        elif item == "dod":
            if not any(has_command(s.header_line, s.last_line) for s in nonblank):
                missing[item] = "no command in backticks"
    designer_skip_reason = _form_missing(cut, missing)

    waived = {}  # item -> reason of the first skip line naming it
    skip_notes = []
    for li in cut.skips:
        items, reason, why = _parse_skip_line(cut.lines[li])
        if why is not None:
            message = SKIP_REFUSED_TEMPLATE.format(line=cut.lines[li].strip(), why=why)
            return 2, message, "", True
        newly = [i for i in ITEMS if i in items and i in missing and i not in waived]
        for i in newly:
            waived[i] = reason
        if newly:
            skip_notes.append(
                SKIP_NOTE_TEMPLATE.format(items=", ".join(_DISPLAY[i] for i in newly), reason=reason)
            )

    still = [i for i in ITEMS if i in missing and i not in waived]
    # F3: with the switch off the two form items are still checked, and reported as a note, never refused
    unenforced = [] if DISPATCH_FORM_REFUSES else [i for i in still if i in _FORM_ITEMS]
    still = [i for i in still if i not in unenforced]
    if still:
        return 2, INCOMPLETE_TEMPLATE.format(kind=kind_word, items=_items_text(still, missing)), "", True
    if unenforced:
        skip_notes.append(FORM_NOT_ENFORCED_NOTE_TEMPLATE.format(items=_items_text(unenforced, missing)))
    if designer_skip_reason is not None:
        skip_notes.append(DESIGNER_SKIP_NOTE_TEMPLATE.format(reason=designer_skip_reason))
    return 0, "", "\n".join(skip_notes), True


def check(payload):
    """The completeness check. Returns (exit_code, message, note); raises on
    a payload that is not a dict, a `tool_input` that is not a dict, an
    internal error or a failed sibling import (piece B guards those)."""
    is_builder, cut = cut_payload(payload)
    if cut is None:
        return 0, "", ""
    code, message, note, _checked = check_cut(cut, is_builder)
    return code, message, note
