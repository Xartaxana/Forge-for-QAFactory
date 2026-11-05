"""Piles and batches: the parsers, the generated board (plans/PILES.md) and the commit gate `check`.

A pile (plans/piles/<slug>/) is a topic with a card (README.md), batch files (batch-<N>[-name].md) and
findings (findings/*.md). plans/PILES.md is GENERATED from them plus plans/BACKLOG.md: a board of the
piles and ONE table of contents of every B-id. `check` is the gate of a commit.

    python tools/piles.py board [--check] [--if-staged]
    python tools/piles.py check [--msg-file PATH] [--all] [--base REV]
    python tools/piles.py take <slug> <N> --who <name>
    python tools/piles.py close <slug> <N> --hash <h> [--url <https://...>]
    python tools/piles.py close --id B-nnn --word "<who, date>" [--hash <h>]
    python tools/piles.py [--repo DIR] ...        point at another tree (tests); default: the parent of tools/

`release` was renamed `close` (the command closes a batch or a row; it is not a factory release): the old name is a
REFUSED alias -- exit 1, the FR-1 text names `close`, nothing runs, whatever the other arguments are.

Exit codes: 0 done / nothing to do / a deliberate pass; 1 cannot run or cannot judge (no "## Закрыто" in
the backlog, a file that is not UTF-8, git cannot list the staged paths or verify a hash, a usage error, the `release`
alias, a write that failed and was rolled back); 2 RED or REFUSED (a check item is red, plans/PILES.md is missing or
stale, take/close refuse).

`take` (the integrator, on main) fixes a waiting batch to its taker in the card row and the batch header; `close`
(after the merge) moves the whole members of an accepted batch into the Закрыто table with the merge hash, or --id
closes one row by the owner's word. A batch is closed by finishing, not by carrying over: `close <slug> <N>` refuses
while an ITEM of the batch's «## Остатки» (every non-empty line outside an HTML comment; a line indented by 2+ spaces
continues the item above it) carries neither `сделано: <7-40 hex | t-nnn>` nor `перенос:` + `обоснование:` +
`подтвердил: <кто, дата>` (a person's confirmation), or while a `перенос:` target names nothing that exists: a
`findings/` file must be on disk AND staged, `пачка N` a card row of this pile that is open and not this batch. The
section is found on the raw `## ` line, the way (в) finds it. The «## Живые доказательства» tables are read the same way (F5-5,
FR-33): `close` refuses while the «Статус» cell of ANY row of ANY table there is neither `сделано: <7-40 hex | t-nnn | a
log/notebook path>` nor `перенос:` + `обоснование:` + `подтвердил:` (the pairs of a table cell are joined with an escaped
pipe; case is free) -- one reader of the forms, `leftover_problem` with the rule `PROOF_RULE`; a section without a table, or with a header-only
table, passes, unless the readiness rule above the first `## ` names «живые доказательства» and no table exists. The readers (board, check, forge_metrics, compact_snapshot)
load the tree tolerantly: a finding file that is not UTF-8 is named (board WARNING, check (д) red with its door), the
others are still read; take, close and split stay strict. They are the only code writers of a batch's status and of
Закрыто, and they write a file in the form it has (CRLF, BOM) and rebuild plans/PILES.md; a write that fails midway
puts every file back (all or nothing, m-8). The status of a batch lives in TWO places -- the batch header (with the card
row) and plans/PILES.md -- and `take` / `close` are the one code writer, in both, of the two statuses they set (`в работе`,
`закрыта`); `сдано` / `принято` are written by hand and reach no board (queued: a command that writes them). There is no
external board: take / close touch files only, make no network call and read no token. On `git commit --amend` the (г) base is HEAD,
the commit being amended, so a row that commit added is grandfathered (m14).

`check` items: (а) placement, (б) overlap, (в) frozen, (г) backlog, (д) form, (е) findings. (б) knows two doors for a file two
batches «в работе» both write: the `очередь: A → B` line in both preambles, or (D-0048, F6-26) a FUNCTION LIST of each batch for
that file -- `` `scripts/story_run.py (f1, f2)` `` or `` `scripts/story_run.py` (`f1`, `f2`) `` in a node's «Пишет в» cell, or, in a
batch already taken (its cell is frozen, its «Ход» is not), a «Ход» line that STARTS with the key `функции:` (after the list marker
and the date): `- 16.10 09:00 — функции: scripts/story_run.py (take_answer, Driver.last_resort, +new_one)`; any other «Ход» line
declares nothing (D-0044). An item is `name`, `Class.name` (the class must define it) or `+name` (a function the node ADDS: no def
needed yet, red if the file already has it). A file named bare AND with a list in one cell is a whole-file claim. Green when both
lists exist and are disjoint and every name is defined in the working tree's file (a misspelt name is red, never a quiet pass);
red naming the common names when they meet; red as before (the file lock) when only one batch, or neither, carries a list. (д) also judges the row-id
coverage of a batch file's nodes (every id of the card row in the «Что» of exactly one node; the doors are in `_coverage_reds`).
(д) also holds, since F6-28, the card's «## Содержание» (every finding file name of the pile and every card-row id exactly once;
`_contents_reds`, `contents_problems`) and the headings «## Бриф» / «## Узлы» of an UNTAKEN batch file (`_heading_reds`,
`batch_heading_problems`); and, since F6-30, the executor of a «Остатки» item at WRITE time (`_leftover_write_reds`): an item that is
NEW or CHANGED against the file at the base carries `сделано: <hash | t-nnn>`, `узел: <id | slug/N/id>` (a node row of a batch that is
not closed, with an Исполнитель) or `перенос: … | обоснование: … | подтвердил: <кто, дата | —>` (the placeholder passes here, `close`
still refuses it). Old bare items stay legal; `leftovers_unowned` counts them (the board count line, the compact snapshot).
(е) is the D-0044 detector: every readable finding is named in a batch file of its own pile, or carries «перенос: <slug>/…»
and is named in that pile's batch; a finding dated 2026-10-13 or later must be named in a ROW (a table row of «Узлы» /
«Остатки» / «Живые доказательства», or a «перенос:» line of «Остатки» -- not the prose of «Ход»), and is red when it is not;
an older one is read at file level and is one WARN line; it runs in `--all` and, in a commit, only when a finding or a batch
file (a deleted one too) is staged. (в) compares a batch that is taken
on origin/main with its text there (the allowed differences: Р9 and P5/P7); with `--base REV` it compares with REV
instead (CI: the base of the pushed range, so (в) judges what the push changed), and so does (г). The door of a red item is a line "piles-skip: <item> -- <reason>" in the commit
message (--msg-file; the hook is commit-msg, the only hook that sees the message); with `--base REV` the same door is also read
from every commit message of REV..HEAD, for all six items (CI has no message file; t-604). A violation passed by a
door once is not red for later unrelated commits: (а) and (б) judge the whole tree, but a red blocks only
a commit whose staged paths carry it; otherwise it is printed as "carried" (--all blocks everything).

Public parsers (imported by tools/piles_split.py and the F0-2c commands): parse_backlog_rows, parse_card,
parse_batch, parse_finding, parse_zone (the card's `зона:`, read by tools/collect_intake.py), closed_hash, split_cells, header_pairs,
staged_paths, door_lines, load_tree.
"""
from __future__ import annotations

import argparse
import ast
import dataclasses
import datetime
import itertools
import os
import re
import sys
import tempfile
import unicodedata
from pathlib import Path

_TOOLS = Path(__file__).resolve().parent
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))

import gitcmd  # noqa: E402
import md_regions  # noqa: E402
# The table reader and the two line filters live in the leaf tools/md_table.py (t-797 F5-2 N3: digest_form reads tables through
# the same objects); every name below stays an attribute of `piles` (the readers and the tests call `piles.split_cells` etc.).
from md_table import (_blank_comments, md_lines_outside_fences, split_cells, split_pipes,  # noqa: E402
                      table_after, unclosed_fence, walk_table)
from forge_metrics import BaseError, compile_glob, parse_backlog_text, resolve_base  # noqa: E402

REPO = _TOOLS.parent
PILES_REL = "plans/piles"
BACKLOG_REL = "plans/BACKLOG.md"
BOARD_REL = "plans/PILES.md"

BATCH_STATUSES = ("ожидает", "в работе", "сдано", "принято", "закрыта")
NODE_STATUSES = BATCH_STATUSES + ("отклонено",)
STATUS_ORDER = {w: i for i, w in enumerate(BATCH_STATUSES)}
ACTIVE = ("в работе", "сдано")
NOT_WRITING = ("принято", "отклонено")     # a node in these statuses writes nothing any more (P5)

BATCH_NAME_RE = re.compile(r"^batch-(\d{1,3})(?:-[a-z0-9-]+)?\.md$")
# group 1 = the B-id of the name (None for a dated name); `slug` = the rest after the id / date prefix (None when there is none).
# The lookahead keeps the dated form exact: yyyymmdd must be followed by "-" (the original alternation's rule).
FINDING_NAME_RE = re.compile(r"^(?:(B-\d{3,})|\d{8}(?=-))(?:-(?P<slug>[a-z0-9-]*))?\.md$")
FINDING_FILE_DATE_RE = re.compile(r"^(\d{4})(\d{2})(\d{2})-")                                   # yyyymmdd- in the file name
FINDING_FROM_DATE_RE = re.compile(r"(?<![\d.])(\d{2})\.(\d{2})(?:\.(\d{4}))?(?![\d.]*\d)")      # 08.10 / 08.10.2026 in `от:`
FINDING_YEAR = "2026"                                                                           # a header date without a year (the freeze year)
ID_RE = re.compile(r"B-\d{3,}")
SECTION_RE = re.compile(r"^## (\d+)\. (.*)$")
LOCK_RE = re.compile(r"^piles-freeze: (\d{4}-\d{2}-\d{2}) open=(\d+) closed=(\d+)\s*$")
QUEUE_RE = re.compile(r"^очередь:\s*([a-z0-9-]+)/(\d+)\s*(?:→|->)\s*([a-z0-9-]+)/(\d+)\s*$", re.M)
WORD_SUFFIX_RE = re.compile(r"; закрыто \d{2}\.\d{2}\.\d{4} по слову: \S")
STAMP_HASH_RE = re.compile(r"закрыто \d{2}\.\d{2}\.\d{4} пачкой `[^`]+`: влито `([0-9a-f]{7,40})`")
# a row closed by the owner's word (`close --id --word [--hash]`): the hash is the optional trailing "; влито `h`" (m-4)
WORD_STAMP_RE = re.compile(r"закрыто \d{2}\.\d{2}\.\d{4} по слову: [^|]*?(?:; влито `([0-9a-f]{7,40})`)?\s*(?:\||$)")
MARKER_RE = re.compile(r"(?i)\b(?:закрыт[оа]?|closed|влит[оа])\b")
HASH_TICK_RE = re.compile(r"(?<![\w-])`([0-9a-f]{7,12}|[0-9a-f]{40})`(?![\w-])")
HASH_BARE_RE = re.compile(r"(?<![\w`-])([0-9a-f]{7,40})(?![\w`-])")
DOOR_RE = re.compile(r"^[ \t]*(?P<kw>piles-skip)[ \t]*:[ \t]*(?P<items>[^-\n]+?)[ \t]*--[ \t]*(?P<reason>\S.*)$",
                     re.M)
ITEMS = (("а", "placement"), ("б", "overlap"), ("в", "frozen"), ("г", "backlog"), ("д", "form"), ("е", "findings"))
ITEM_NAMES = dict(ITEMS)
ITEM_ALIASES = {"а": "а", "a": "а", "placement": "а", "б": "б", "b": "б", "overlap": "б",
                "в": "в", "v": "в", "frozen": "в", "г": "г", "g": "г", "backlog": "г",
                "д": "д", "d": "д", "form": "д", "е": "е", "e": "е", "findings": "е"}
ITEMS_HELP = "а/placement, б/overlap, в/frozen, г/backlog, д/form, е/findings"
DOOR_HELP = 'add a line "piles-skip: <item> -- <reason>" to the commit message (items: %s)' % ITEMS_HELP
NO_VAL = ("", "—", "-")


class CannotRun(Exception):
    """The tool cannot judge (exit 1): an unreadable file, no '## Закрыто', no git. The text names the door."""


class Unreadable(CannotRun):
    """A file that cannot be read or decoded. `reason` is the short form a tolerant reader (a finding) prints."""

    def __init__(self, message: str, reason: str):
        super().__init__(message)
        self.reason = reason


# ============================================================================================
# text, cells, header pairs
# ============================================================================================

def read_text(path) -> str:
    """UTF-8 (BOM allowed), CRLF/CR -> LF. A file that cannot be read or decoded is CannotRun, never 'clean'."""
    try:
        raw = Path(path).read_bytes().decode("utf-8-sig")
    except OSError as exc:
        raise Unreadable("cannot read %s: %s" % (path, exc), exc.strerror or type(exc).__name__)
    except UnicodeDecodeError as exc:
        raise Unreadable("cannot read %s: %s; save it as UTF-8" % (path, exc),
                         "not valid UTF-8 (byte 0x%02x at position %d)" % (exc.object[exc.start], exc.start))
    return raw.replace("\r\n", "\n").replace("\r", "\n")


def unwrap_ticks(value: str) -> str:
    m = re.fullmatch(r"`([^`]*)`", value.strip())
    return m.group(1).strip() if m else value.strip()


def header_pairs(line: str) -> dict:
    """'key: value | key: value' -> {key(lower): value}. Each segment splits at its FIRST colon (a URL keeps
    its colons); a value that is one backtick span is unwrapped; the first occurrence of a key wins (m2)."""
    pairs = {}
    for seg in split_pipes(line):
        if ":" not in seg:
            continue
        key, val = seg.split(":", 1)
        pairs.setdefault(key.strip().strip("`").strip().lower(), unwrap_ticks(val))
    return pairs


def first_tick(value: str) -> str:
    """The first backtick token of a value (the branch is compared by it), else the first word."""
    m = re.search(r"`([^`]+)`", value)
    if m:
        return m.group(1).strip()
    return value.split()[0] if value.split() else ""


def status_word(raw: str, allowed=BATCH_STATUSES):
    """The known status word a cell starts with ('сдано 08.10' -> 'сдано'), else None. Longest word first."""
    t = raw.strip().strip("`").strip().lower()
    for w in sorted(allowed, key=len, reverse=True):
        if t.startswith(w) and (len(t) == len(w) or not t[len(w)].isalpha()):
            return w
    return None


def column_map(header, wanted: dict) -> dict:
    """{key: index} for the header cells whose lower-cased text STARTS with wanted[key]."""
    out = {}
    for key, prefix in wanted.items():
        for i, name in enumerate(header):
            if name.strip().lower().startswith(prefix):
                out.setdefault(key, i)
                break
    return out


def _cell(cells, idx, default=""):
    return cells[idx] if idx is not None and idx < len(cells) else default


# ============================================================================================
# BACKLOG.md
# ============================================================================================

@dataclasses.dataclass
class Row:
    id: str
    line: int
    section: str
    section_title: str
    columns: list
    cells: list
    fields: dict
    text: str
    closed: bool
    irregular: bool


@dataclasses.dataclass
class Backlog:
    rows: list
    boundary: int
    locks: list              # [(line_no, (date, open, closed) | None)] -- None = a malformed piles-freeze line

    @property
    def open_ids(self):
        return {r.id for r in self.rows if not r.closed}

    @property
    def closed_ids(self):
        return {r.id for r in self.rows if r.closed}

    @property
    def n_open(self):
        return sum(1 for r in self.rows if not r.closed)

    @property
    def n_closed(self):
        return sum(1 for r in self.rows if r.closed)

    def first(self, ident, closed):
        return next((r for r in self.rows if r.id == ident and r.closed == closed), None)


COL_FIELDS = {"что сделать": "what", "что": "what", "почему": "witness", "детали": "witness",
              "свидетель": "witness", "источник": "source", "принципы": "principles"}
POSITIONAL = ("id", "что сделать", "почему", "источник", "принципы")


def row_fields(cells, columns):
    """-> (fields{what,witness,source,principles}, irregular). Extra cells go to what, missing ones read '—' (E11)."""
    names = [c.strip().lower() for c in columns] if columns else list(POSITIONAL)
    fields = {"what": "", "witness": "—", "source": "—", "principles": "—"}
    extra_what = []
    for i, name in enumerate(names[1:], 1):
        val = cells[i] if i < len(cells) else "—"
        key = COL_FIELDS.get(name)
        if key == "what":
            fields["what"] = val
        elif key:
            fields[key] = val
        else:
            extra_what.append("%s: %s" % (name, val))
    extra_what += list(cells[len(names):])
    if extra_what:
        fields["what"] = (fields["what"] + " " + " ".join(extra_what)).strip()
    return fields, len(cells) != len(names)


def _unclosed_fence_error(where: str, lines, hidden: str, expected: str = "after it"):
    """CannotRun naming `<where>:<line of the opener>` when a fenced block in `lines` is never closed (F6-16): such a block hides
    every line after it, and the detector would answer a silent «not placed» / «not frozen» for what `hidden` names. `expected`
    says where the closing line belongs. None when every block closes. The ONE builder of this refusal."""
    opened = unclosed_fence(lines)
    if opened is None:
        return None
    return CannotRun("%s:%d: the fenced block opened here is never closed -- it hides every line after it, so %s; expected a closing "
                     "line of the same kind (``` or ~~~) %s; add it and run again" % (where, opened + 1, hidden, expected))


def backlog_marks(lines):
    """-> ({line_no: (section, title, table header cells)}, boundary line_no or 0, [(line_no, lock | None)])."""
    marks, section, title, columns = {}, "?", "", []
    boundary, first_h2 = 0, None
    for i, line in enumerate(lines, 1):
        if line.rstrip() == "## Закрыто" and not boundary:
            boundary = i
        m = SECTION_RE.match(line)
        if m:
            section, title, columns = m.group(1), m.group(2).strip(), []
        if re.match(r"^\| id \|", line, re.I):
            columns = split_cells(line)
        if line.startswith("## ") and first_h2 is None:
            first_h2 = i
        marks[i] = (section, title, columns)
    locks = []
    head = lines[:(first_h2 - 1)] if first_h2 else lines
    error = _unclosed_fence_error(BACKLOG_REL, head, "every `piles-freeze:` line after it would read as «not frozen»",
                                  "before the first «## » heading")
    if error:                            # a block nothing closes hides every lock after it: «not frozen» would be a silent lie (F6-16)
        raise error
    for i, line in md_lines_outside_fences(head):
        if line.startswith("piles-freeze:"):
            m = LOCK_RE.match(line)
            locks.append((i + 1, (m.group(1), int(m.group(2)), int(m.group(3))) if m else None))
    return marks, boundary, locks


def parse_backlog_rows(text: str) -> Backlog:
    """The rows of BACKLOG.md text (already LF). No '## Закрыто' line -> CannotRun (E12): without the boundary
    an open row cannot be told from a closed one. Cells are cut by split_cells, not by forge_metrics' `cells` (P10)."""
    lines = text.split("\n")
    marks, boundary, locks = backlog_marks(lines)
    if not boundary:
        raise CannotRun('%s has no "## Закрыто" heading -- cannot tell open rows from closed ones; expected one '
                        'line "## Закрыто" above the closed table; restore it and run again' % BACKLOG_REL)
    raw_rows, _ = parse_backlog_text(text.encode("utf-8"))
    rows = []
    for r in raw_rows:
        section, title, columns = marks[r["line"]]
        cells = split_cells(r["line_text"])
        fields, irregular = row_fields(cells, columns)
        rows.append(Row(r["id"], r["line"], section, title, columns, cells, fields, r["line_text"],
                        r["line"] > boundary, irregular))
    return Backlog(rows, boundary, locks)


def closed_hash(text: str):
    """The commit hash a closed row names, or None (P9). A row written by `close` is read by its stamp first (a
    batch stamp, then a word stamp -- which without `--hash` reads None, never a hex token of the word);
    otherwise the first token after the first closing marker: in backticks 7-12 or 40 hex (digits allowed), bare
    7-40 hex with at least one letter a-f. A digits-only bare token (a pipeline number) is never a hash."""
    m = STAMP_HASH_RE.search(text)
    if m:
        return m.group(1)
    w = WORD_STAMP_RE.search(text)
    if w:                                # a close by word names a hash only through its own stamp: the word may hold any hex
        return w.group(1)
    marker = MARKER_RE.search(text)
    if not marker:
        return None
    tail = text[marker.end():]
    best = None
    for rx, need_letter in ((HASH_TICK_RE, False), (HASH_BARE_RE, True)):
        for hit in rx.finditer(tail):
            if need_letter and not re.search(r"[a-f]", hit.group(1)):
                continue
            if best is None or hit.start() < best[0]:
                best = (hit.start(), hit.group(1))
            break
    return best[1] if best else None


# ============================================================================================
# card, batch file, finding
# ============================================================================================

@dataclasses.dataclass
class Member:
    id: str
    qualifier: str
    partial: bool


@dataclasses.dataclass
class CardRow:
    n: int
    n_raw: str
    line: int
    what: str
    rows_cell: str
    size: str
    status_raw: str
    status: object
    who: str
    branch: str
    mr: str
    members: list
    nonid: list


@dataclasses.dataclass
class Card:
    path: str
    title: str
    name: str
    title_slug: object
    priority: str
    features: list
    stand: str
    zone: str
    rows: list
    errors: list
    contents: bool = False     # the card has a «## Содержание» section: the pile is in the t-717 form (check (д) judges its row-id coverage)


def split_top_commas(cell: str) -> list:
    """Pieces of a cell split at commas that are not inside parentheses."""
    out, depth, cur = [], 0, []
    for ch in cell:
        if ch == "(":
            depth += 1
        elif ch == ")" and depth > 0:
            depth -= 1
        if ch == "," and depth == 0:
            out.append("".join(cur))
            cur = []
        else:
            cur.append(ch)
    out.append("".join(cur))
    return out


def parse_members(cell: str):
    """-> (members, nonid). Every B-nnn in the cell is a member (also one inside a qualifier, m11). The qualifier is
    the text from the end of the id up to the next comma, the next id or the cell end, minus spaces and / + ;
    -- non-empty means a PARTIAL member (E10). Pieces without an id ('W7', 'затем') are returned as nonid."""
    members = []
    matches = list(ID_RE.finditer(cell))
    for k, m in enumerate(matches):
        end = len(cell)
        comma = cell.find(",", m.end())
        if comma >= 0:
            end = min(end, comma)
        if k + 1 < len(matches):
            end = min(end, matches[k + 1].start())
        qual = cell[m.end():end].strip(" \t/+;")
        members.append(Member(m.group(0), qual, bool(qual)))
    nonid = [p.strip() for p in split_top_commas(cell)
             if p.strip() and p.strip() not in NO_VAL and not ID_RE.search(p)]
    return members, nonid


CARD_COLS = {"n": "№", "what": "что", "rows": "строки", "size": "размер", "status": "статус",
             "who": "взял", "branch": "ветка", "mr": "mr"}
CARD_REQUIRED = (("n", "№"), ("rows", "Строки"), ("status", "Статус"))


def _card_row(cells, line, cols) -> CardRow:
    n_raw = _cell(cells, cols.get("n")).strip()
    n = int(n_raw) if re.fullmatch(r"\d{1,3}", n_raw) and 1 <= int(n_raw) <= 999 else 0
    rows_cell = _cell(cells, cols.get("rows"))
    members, nonid = parse_members(rows_cell)
    st = _cell(cells, cols.get("status"), "—")
    return CardRow(n, n_raw, line, _cell(cells, cols.get("what"), "—"), rows_cell, _cell(cells, cols.get("size"), "—"),
                   st, status_word(st), _cell(cells, cols.get("who"), "—"), _cell(cells, cols.get("branch"), "—"),
                   _cell(cells, cols.get("mr"), "—"), members, nonid)


def parse_card(text: str, rel: str) -> Card:
    """plans/piles/<slug>/README.md. Problems found while parsing are returned in `errors` (the (д) item)."""
    lines = text.split("\n")
    errors = []
    title = next((l for l in lines if l.startswith("# ")), "")
    m = re.match(r"^#\s+(.*?)\s*\(`([^`]+)`\)\s*$", title)
    name, title_slug = (m.group(1), m.group(2)) if m else (title[2:].strip(), None)
    if title_slug is None:
        errors.append('the heading has no (`<slug>`) at its end -- expected "# <name> (`<slug>`)"')
    props_line = next((l for l in lines if "приоритет:" in l.lower()), None)
    pairs = header_pairs(props_line) if props_line else {}
    if props_line is None:
        errors.append('no properties line -- expected "приоритет: П1 | фичи: F01 | стенд: нужен | зона: `…`" under the heading')
    prio = re.search(r"П\d", pairs.get("приоритет", ""))
    table = table_after(lines, "Пачки")
    rows = []
    if table is None:
        errors.append("no batch table under the heading '## Пачки' -- expected a table with the columns № / Строки / Статус")
    else:
        cols = column_map(table[0], CARD_COLS)
        for key, label in CARD_REQUIRED:
            if key not in cols:
                errors.append("the batch table has no %s column -- expected the columns № / Строки / Статус" % label)
        if all(k in cols for k, _ in CARD_REQUIRED):
            rows = [_card_row(c, ln, cols) for c, ln in table[1]]
    for r in rows:
        if r.n == 0:
            errors.append('batch row with № "%s" -- expected a whole number 1-999' % r.n_raw)
        if r.status is None:
            errors.append('batch %s has status "%s", which starts with no known status word -- expected one of: %s'
                          % (r.n_raw, r.status_raw, ", ".join(BATCH_STATUSES)))
    return Card(rel, title[2:].strip(), name, title_slug, prio.group(0) if prio else "—",
                re.findall(r"F\d\d", pairs.get("фичи", "")), pairs.get("стенд", "—") or "—",
                pairs.get("зона", "—") or "—", rows, errors, any(l.rstrip() == "## Содержание" for l in lines))


FN_NAME = r"[A-Za-z_][A-Za-z0-9_]*"
FN_ITEM_RE = re.compile(r"^\+?(?:%s\.)*%s$" % (FN_NAME, FN_NAME))         # `take_answer`, `Driver.take_answer`, or `+new_one` (a function the node ADDS)
HOD_KEY_RE = re.compile(r"^\s*(?:[-*•]\s+|\d+[.)]\s+)?(?:\d[\d.:/-]*(?:\s+\d{1,2}:\d{2})?\s*[—–:-]\s*)?функции:\s*(.*)$", re.I)
BARE_PY_PATH_RE = re.compile(r"(?<![`\w/.\\-])([\w./-]+\.py)(?![\w`])")      # a .py path written with no backticks (a `функции:` line may)
BACKTICK_RE = re.compile(r"`([^`]+)`")
PATH_WITH_LIST_RE = re.compile(r"^([^()]*?)\s+\(([^()]*)\)\s*$")            # form 1, INSIDE the backticks: `scripts/story_run.py (f1, f2)`
LIST_AFTER_RE = re.compile(r"\s*\(([^()]*)\)")                              # form 2, right AFTER the closing backtick: `scripts/story_run.py` (`f1`, `f2`)


def merge_unique(base: list, more) -> list:
    """`base` followed by the items of `more` it does not hold yet (order kept): the one union idiom of the function lists."""
    out = list(base)
    for x in more:
        if x not in out:
            out.append(x)
    return out


def fn_bare(item: str) -> str:
    """'+Driver.take_answer' -> 'take_answer': the name the disjointness of two lists compares."""
    return item.rsplit(".", 1)[-1].lstrip("+")


def parse_fn_list(raw: str):
    """'take_answer, `Driver.last_resort`, +new_one' -> ['take_answer', 'Driver.last_resort', '+new_one'] (the items as written:
    the `Class.` prefix is kept for the existence check, a leading `+` marks a function the node ADDS); None when the bracket
    is not a function list: it is empty, or any piece is not an identifier / Class.identifier / +identifier (so a prose note like
    (S0–S3) or (тексты `handoff`) is no list, and the cell stays the whole-file claim it was before D-0048). `(new)` alone is
    the new-file marker of the dispatch manifests (live in the cells of batch files), never a one-name list. Names are
    case-sensitive; duplicates collapse."""
    if raw.strip().lower() == "new":
        return None
    items = []
    for piece in raw.split(","):
        item = piece.strip().strip("`").strip()
        if FN_ITEM_RE.match(item) is None:
            return None
        items = merge_unique(items, [item])
    return items


def parse_writers(cell: str):
    """-> (paths, lists): every backticked token of the cell is a writer path (as before); a function list written on it in
    form 1 or form 2 is cut off the path and returned in `lists` {path: [items]}. An unreadable bracket after the path is no
    list (the token still counts as a whole-file writer). A path that ALSO appears bare in the same cell (`a.py (f)`, `a.py`)
    is a whole-file claim: the bare mention wins and the path carries no list (the lock, never a quiet narrowing; t-880 F-2)."""
    paths, lists, bare, in_list = [], {}, set(), -1
    for m in BACKTICK_RE.finditer(cell):
        if m.start() < in_list:                    # a `name` inside a function list just read is a name, not a writer
            continue
        tok, names = m.group(1), None
        m1 = PATH_WITH_LIST_RE.match(tok)
        if m1 and m1.group(1).strip():
            tok, names = m1.group(1).strip(), parse_fn_list(m1.group(2))
        else:
            m2 = LIST_AFTER_RE.match(cell, m.end())
            if m2:
                names = parse_fn_list(m2.group(1))
                in_list = m2.end() if names else in_list
        paths.append(tok)
        if names:
            lists[tok] = merge_unique(lists.get(tok, []), names)
        else:
            bare.add(tok)
    return paths, {t: v for t, v in lists.items() if t not in bare}


@dataclasses.dataclass
class Node:
    id: str
    line: int
    executor: str
    writes_cell: str
    writers: list
    status_raw: str
    status: object
    what: str = ""             # the «Что» cell ("" when the table has no such column): check (д) reads the B-ids it names
    lists: dict = dataclasses.field(default_factory=dict)   # {writer path: [function names]} the «Пишет в» cell declares (D-0048)


@dataclasses.dataclass
class BatchFile:
    path: str
    n: int
    title: str
    header: dict
    status_raw: str
    status: object
    who: str
    branch: str
    mr: str
    queue: list
    nodes: list
    has_nodes_table: bool
    errors: list
    hod_lists: dict = dataclasses.field(default_factory=dict)   # {path: [function names]} the «## Ход» lines declare (D-0048)


NODE_COLS = {"id": "узел", "executor": "исполнитель", "writes": "пишет в", "status": "статус", "what": "что"}
NODE_REQUIRED = (("id", "Узел"), ("executor", "Исполнитель"), ("writes", "Пишет в"), ("status", "Статус"))   # «Что» is optional here


def _parse_nodes(lines, errors):
    table = table_after(lines, "Узлы")
    if table is None:
        errors.append("no node table under '## Узлы' -- expected a table with the columns Узел / Исполнитель / Пишет в / Статус")
        return [], False
    cols = column_map(table[0], NODE_COLS)
    missing = [lbl for k, lbl in NODE_REQUIRED if k not in cols]
    if missing:
        errors.append("the node table has no %s column -- expected Узел / Исполнитель / Пишет в / Статус" % ", ".join(missing))
        return [], True
    nodes = []
    for cells, ln in table[1]:
        w = _cell(cells, cols["writes"])
        st = _cell(cells, cols["status"])
        paths, lists = parse_writers(w)
        nodes.append(Node(_cell(cells, cols["id"]), ln, _cell(cells, cols["executor"]), w, paths, st,
                          status_word(st, NODE_STATUSES), _cell(cells, cols.get("what")), lists))
    return nodes, True


def _hod_lists(lines) -> dict:
    """{path: [items]} of the function lists the «## Ход» section DECLARES (D-0048): a taken batch's node cells are frozen by (в), its
    Ход is not, so this is where a batch already in work declares the functions it writes. A Ход line declares ONLY behind the
    key `функции:` at the start of the line (after the list marker and the date, the place `очередь:` takes): `- 16.10 09:00 —
    функции: scripts/story_run.py (take_answer, +new_one)`, the path with or without backticks. Every other line declares
    NOTHING -- the prose of Ход places nothing (D-0044), so `поправила `a.py` (`f`)` narrows no claim (t-880 F-1). A line inside
    a `<!-- -->` comment is no line (the template shows the form there); an empty bracket is no list."""
    out, inside = {}, False
    for line in _blank_comments(list(lines))[0]:
        if line.startswith("## "):
            inside = line.startswith("## Ход")
            continue
        key = HOD_KEY_RE.match(line) if inside else None
        if key:
            for path, items in parse_writers(BARE_PY_PATH_RE.sub(r"`\1`", key.group(1)))[1].items():
                out[path] = merge_unique(out.get(path, []), items)
    return out


def parse_batch(text: str, rel: str, n=None) -> BatchFile:
    """plans/piles/<slug>/batch-<N>[-name].md. N defaults to the one in the file name."""
    lines = text.split("\n")
    errors = []
    if n is None:
        m = BATCH_NAME_RE.match(rel.rsplit("/", 1)[-1])
        n = int(m.group(1)) if m else 0
    title = next((l[2:].strip() for l in lines if l.startswith("# ")), "")
    head_line = next((l for l in lines if "кучка:" in l.lower()), None)
    header = header_pairs(head_line) if head_line else {}
    if head_line is None:
        errors.append('no header line -- expected "кучка: `<slug>` | статус: … | взял: … | ветка: … | MR: …" under the heading')
    st = header.get("статус", "")
    status = status_word(st)
    if head_line is not None and status is None:
        errors.append('status "%s" starts with no known status word -- expected one of: %s'
                      % (st, ", ".join(BATCH_STATUSES)))
    cut = next((i for i, l in enumerate(lines) if l.startswith("## Узлы")), len(lines))
    queue = [(a, int(b), c, int(d)) for a, b, c, d in QUEUE_RE.findall("\n".join(lines[:cut]))]
    nodes, has_table = _parse_nodes(lines, errors)
    return BatchFile(rel, n, title, header, st or "—", status, header.get("взял", "—"), header.get("ветка", "—"),
                     header.get("mr", "—"), queue, nodes, has_table, errors, _hod_lists(lines))


@dataclasses.dataclass
class Finding:
    path: str
    name: str
    name_id: str
    id: str
    pile: str
    title: str
    errors: list
    date: object = None        # datetime.date | None: the file name's yyyymmdd-, else the DD.MM[.YYYY] of `от:` (None: neither)
    text: str = ""             # the whole file as LF, BOM stripped; "" when it could not be read
    unreadable: str = ""       # why the file could not be read ("" = it was); only a tolerant load makes one
    source: str = ""           # the `от:` pair of the header ("" when there is none): the one reader of it (collect_intake's idempotency key)


def finding_date(name: str, pairs: dict):
    """The one date reader of a finding: the file name's yyyymmdd-, else the DD.MM[.YYYY] of the header's `от:` (no year =
    FINDING_YEAR). A date the name carries but the calendar refuses is None -- it does not fall back to the header."""
    named = FINDING_FILE_DATE_RE.match(name)
    found = FINDING_FROM_DATE_RE.search(pairs.get("от", "")) if not named else None
    if named:
        y, mo, d = named.groups()
    elif found:
        y, mo, d = found.group(3) or FINDING_YEAR, found.group(2), found.group(1)
    else:
        return None
    try:
        return datetime.date(int(y), int(mo), int(d))
    except ValueError:
        return None


def unreadable_finding(rel: str, reason: str) -> Finding:
    """What a tolerant load makes of a finding file it cannot read: no id, no text, ONE error that names the way out."""
    name = rel.rsplit("/", 1)[-1]
    nm = FINDING_NAME_RE.match(name)
    return Finding(rel, name, (nm.group(1) or "") if nm else "", "", "", "",
                   ["cannot read this finding (%s) -- expected a UTF-8 text file; save it as UTF-8 or delete it" % reason],
                   finding_date(name, {}), unreadable=reason)       # the date of the NAME is known without reading the file


def parse_finding(text: str, rel: str) -> Finding:
    """plans/piles/<slug>/findings/<name>.md. `id` is '' for a finding without an id (legal, E22). `text` is kept as LF
    without a BOM, so a CRLF or BOM file reads as its LF twin."""
    text = text.removeprefix("\ufeff").replace("\r\n", "\n").replace("\r", "\n")
    name = rel.rsplit("/", 1)[-1]
    nm = FINDING_NAME_RE.match(name)
    errors = []
    if not nm:
        errors.append("file name does not fit B-nnn[-slug].md or yyyymmdd-<slug>.md")
    name_id = (nm.group(1) or "") if nm else ""
    lines = text.split("\n")
    t_idx = next((i for i, l in enumerate(lines) if l.startswith("# ")), None)
    title = lines[t_idx][2:].strip() if t_idx is not None else ""
    window = lines[(t_idx + 1) if t_idx is not None else 0:][:5]
    head = next((l for l in window if l.lower().startswith("id:")), None)
    if head is None:
        errors.append('no header line -- expected "id: B-nnn | кучка: `<slug>` | от: … | приоритет: … | кандидат наверх: …" '
                      "within 5 lines under the heading")
        return Finding(rel, name, name_id, "", "", title, errors, finding_date(name, {}), text)
    pairs = header_pairs(head)
    ident = pairs.get("id", "")
    if ident in NO_VAL:
        ident = ""
    elif not ID_RE.fullmatch(ident):
        errors.append('id "%s" -- expected B-nnn, or — for a finding without an id' % ident)
        ident = ""
    return Finding(rel, name, name_id, ident, pairs.get("кучка", ""), title, errors, finding_date(name, pairs), text,
                   source=pairs.get("от", ""))


# ============================================================================================
# the tree: piles, views of their batches
# ============================================================================================

@dataclasses.dataclass
class View:
    """One batch as the board and the checks see it: the card row (if any) and the file(s) (if any)."""
    slug: str
    n: int
    row: object
    files: list

    @property
    def file(self):
        return self.files[0] if self.files else None

    @property
    def status(self):
        """Effective status: the file's if the file exists, else the card row's (P7: the file leads)."""
        if self.file is not None:
            return self.file.status
        return self.row.status if self.row else None

    @property
    def members(self):
        return self.row.members if self.row else []


@dataclasses.dataclass
class Pile:
    slug: str
    card: object
    card_rel: str
    batches: list
    findings: list
    errors: list             # [(path, message)] found while loading

    def views(self):
        by_n = {}
        for r in (self.card.rows if self.card else []):
            by_n.setdefault(r.n, View(self.slug, r.n, r, []))
        for b in self.batches:
            by_n.setdefault(b.n, View(self.slug, b.n, None, [])).files.append(b)
        return [by_n[k] for k in sorted(by_n)]


@dataclasses.dataclass
class Tree:
    root: Path
    backlog: Backlog
    piles: dict
    untracked: list

    def all_views(self):
        return [v for p in self.piles.values() for v in p.views()]

    def findings_by_id(self):
        out = {}
        for p in self.piles.values():
            for f in p.findings:
                if f.id:
                    out.setdefault(f.id, []).append(f)
        return out

    def member_rows(self):
        """[(view, member)] over every card row of every pile."""
        return [(v, m) for v in self.all_views() for m in v.members]


def _is_pile_dir(p: Path) -> bool:
    return p.is_dir() and not p.name.startswith(("_", "."))


def load_pile(root: Path, folder: Path, tolerant=False) -> Pile:
    """One pile. `tolerant`: a finding file that cannot be read becomes an `unreadable` Finding and the others are still read
    (the readers: board, check, forge_metrics, compact_snapshot); strict (take, close, split): CannotRun,
    because a writer must not act on a tree it could not read whole."""
    slug = folder.name
    rel = "%s/%s" % (PILES_REL, slug)
    errors, card, batches, findings = [], None, [], []
    readme = folder / "README.md"
    if readme.is_file():
        card = parse_card(read_text(readme), rel + "/README.md")
        errors += [(card.path, e) for e in card.errors]
        if card.title_slug is not None and card.title_slug != slug:
            errors.append((card.path, 'heading says (`%s`) but the folder is "%s" -- the folder name wins; fix the heading'
                           % (card.title_slug, slug)))
    else:
        errors.append((rel + "/README.md", "the pile has no README.md card -- expected plans/piles/%s/README.md "
                       "written from plans/piles/_template/README.md" % slug))
    for f in sorted(folder.glob("batch-*.md")):
        m = BATCH_NAME_RE.match(f.name)
        if not m:
            errors.append(("%s/%s" % (rel, f.name), "batch file name does not fit batch-<N>[-name].md (N 1-999, lower case)"))
            continue
        b = parse_batch(read_text(f), "%s/%s" % (rel, f.name), int(m.group(1)))
        batches.append(b)
        errors += [(b.path, e) for e in b.errors]
    fdir = folder / "findings"
    for f in sorted(fdir.glob("*.md")) if fdir.is_dir() else []:
        frel = "%s/findings/%s" % (rel, f.name)
        try:
            fi = parse_finding(read_text(f), frel)
        except Unreadable as exc:
            if not tolerant:
                raise
            fi = unreadable_finding(frel, exc.reason)
        findings.append(fi)
        if not fi.unreadable:                  # an unreadable finding is judged by check (д) in one line of its own, not here
            errors += [(fi.path, e) for e in fi.errors]
    return Pile(slug, card, rel + "/README.md", batches, findings, errors)


def load_tree(root, with_untracked=False, tolerant=False) -> Tree:
    """Everything the board and the checks read, from the working tree. CannotRun on an unreadable file or no boundary --
    except, with `tolerant`, a finding file (see load_pile). The untracked-file scan costs a git call and only the board warns
    about it, hence the flag."""
    root = Path(root)
    backlog = parse_backlog_rows(read_text(root / BACKLOG_REL))
    base = root / PILES_REL
    piles = {}
    for folder in sorted(base.iterdir()) if base.is_dir() else []:
        if _is_pile_dir(folder):
            piles[folder.name] = load_pile(root, folder, tolerant)
    return Tree(root, backlog, piles, untracked_piles(root) if with_untracked else [])


# ============================================================================================
# git
# ============================================================================================

def git(root, *args):
    """-> (returncode, stdout bytes). returncode -1 when git itself cannot run."""
    return gitcmd.git(root, *args)


def staged_paths(root) -> list:
    """Staged paths (adds, changes, deletions; renames split). CannotRun when git cannot list them."""
    rc, out = git(root, "diff", "--cached", "--name-only", "--no-renames", "-z")
    if rc != 0:
        raise CannotRun("cannot list the staged paths (%s) -- run inside the repository, or with --all to check "
                        "the whole tree" % (out.decode("utf-8", "replace").strip() or "git exited %d" % rc))
    return [p for p in out.decode("utf-8", "replace").split("\0") if p]


def untracked_piles(root) -> list:
    rc, out = git(root, "ls-files", "--others", "--exclude-standard", "-z", "--", PILES_REL)
    if rc != 0:
        return []
    return sorted(p for p in out.decode("utf-8", "replace").split("\0") if p)


def git_show(root, rev, rel):
    """Text of rel at rev (LF), or None when the rev or the path is not there."""
    rc, out = git(root, "show", "%s:%s" % (rev, rel))
    if rc != 0:
        return None
    return out.decode("utf-8-sig", "replace").replace("\r\n", "\n").replace("\r", "\n")


def is_merging(root) -> bool:
    rc, out = git(root, "rev-parse", "--git-path", "MERGE_HEAD")
    if rc != 0:
        return False
    p = Path(out.decode("utf-8", "replace").strip())
    return (p if p.is_absolute() else Path(root) / p).exists()


# ============================================================================================
# board
# ============================================================================================

def _esc(s) -> str:
    return str(s).replace("|", "\\|").replace("\n", " ")


def _shown(file_val, card_val, same) -> str:
    """The file's value; when the card row says something else both are shown (E34, P7: the file is ahead)."""
    if not card_val or same(file_val, card_val):
        return file_val
    return "%s (в карточке: %s)" % (file_val, card_val)


def _same_status(a, b):
    wa, wb = status_word(a), status_word(b)
    return wa == wb if wa and wb else a.strip() == b.strip()


def _same_branch(a, b):
    return first_tick(a) == first_tick(b)


def _incoming(pile: Pile, prose: dict):
    """The «Входящие» cell: the findings of the pile that are NOT placed -- by `finding_placed`, the one predicate (е) judges by."""
    mine = [f for f in pile.findings if not finding_placed(f, pile.slug, prose)]
    dates = [re.match(r"(\d{4})(\d{2})(\d{2})-", f.name) for f in mine]
    dates = sorted(m.groups() for m in dates if m)
    last = "%s.%s.%s" % (dates[-1][2], dates[-1][1], dates[-1][0]) if dates else "—"
    return "%d / %s" % (len(mine), last)


def _board_cells(pile: Pile, v: View):
    row, f = v.row, v.file
    what = row.what if row else (f.title if f else "—")
    if f is not None:
        status = _shown(f.status_raw, row.status_raw if row else "", _same_status)
        who = _shown(f.who, row.who if row else "", lambda a, b: a.strip() == b.strip())
        branch = _shown(f.branch, row.branch if row else "", _same_branch)
        mr = _shown(f.mr, row.mr if row else "", lambda a, b: a.strip() == b.strip())
    else:
        status, who, branch, mr = row.status_raw, row.who, row.branch, row.mr
    return [str(v.n), what, row.size if row else "—", status, who, branch, mr]


def _prio_rank(card):
    m = re.fullmatch(r"П(\d)", card.priority) if card else None
    return int(m.group(1)) if m else 9


def board_table(tree: Tree) -> list:
    out = ["| Кучка | Приоритет | Стенд | № | Что изменится | Размер | Статус | Взял | Ветка | MR | Входящие |",
           "|---|---|---|---|---|---|---|---|---|---|---|"]
    keyed = []
    prose = pile_prose(tree)
    for pile in tree.piles.values():
        card = pile.card
        name = card.name if card else pile.slug
        link = "[%s](piles/%s/README.md) (`%s`)" % (name, pile.slug, pile.slug)
        head = [link, card.priority if card else "—", card.stand if card else "—"]
        inc = _incoming(pile, prose)
        views = pile.views()
        if not views:
            keyed.append(((_prio_rank(card), pile.slug, 0), head + ["—"] * 7 + [inc]))
        for v in views:
            if v.files and len(v.files) > 1:
                parts = [(_board_cells(pile, View(v.slug, v.n, v.row, [f]))) for f in v.files]
            else:
                parts = [_board_cells(pile, v)]
            for cells in parts:
                keyed.append(((_prio_rank(card), pile.slug, v.n), head + cells + [inc]))
    for _, cells in sorted(keyed, key=lambda t: t[0]):
        out.append("| " + " | ".join(_esc(c) for c in cells) + " |")
    return out


def _open_sets(tree: Tree):
    """-> (open_ids, live_members {id: [(slug, n, qualifier)]}). open = open rows | findings not closed | live rows."""
    live = {}
    for v, m in tree.member_rows():
        if v.status != "закрыта":
            live.setdefault(m.id, []).append((v.slug, v.n, m.qualifier))
    finds = tree.findings_by_id()
    closed = tree.backlog.closed_ids
    # a closed id that only a PARTIAL member of a live batch names is closed, not open (m-5: the verdict of (а)5)
    in_batch = {i for i, ms in live.items() if i not in closed or any(not qual for _, _, qual in ms)}
    open_ids = tree.backlog.open_ids | {i for i in finds if i not in closed} | in_batch
    return open_ids, live


def _toc_text(ident, tree, misplaced, live, finds) -> str:
    bl = tree.backlog
    if ident in bl.closed_ids:
        h = closed_hash(bl.first(ident, True).text)
        text = "закрыто `%s`" % h if h else "закрыто (хэша нет)"
        return text + (" (и открыт — ошибка)" if ident in bl.open_ids or ident in misplaced else "")
    parts, covered = [], set()
    for slug, n, qual in live.get(ident, []):
        s = "`%s` → пачка %d" % (slug, n) + (" " + qual if qual else "")
        fnd = next((f for f in finds.get(ident, []) if f.path.split("/")[2] == slug), None)
        if fnd:
            s += ", описание: findings/" + fnd.name
            covered.add(fnd.path)
        parts.append(s)
    for f in finds.get(ident, []):
        if f.path not in covered:
            parts.append("`%s` → findings/%s" % (f.path.split("/")[2], f.name))
    return "; ".join(parts) if parts else "не разложено"


def toc_lines(tree: Tree):
    open_ids, live = _open_sets(tree)
    finds = tree.findings_by_id()
    misplaced = closed_but_placed(tree, finds)
    ids = sorted(open_ids | tree.backlog.closed_ids, key=lambda s: int(s[2:]))
    lines = ["| id | где |", "|---|---|"]
    lines += ["| %s | %s |" % (i, _esc(_toc_text(i, tree, misplaced, live, finds))) for i in ids]
    return lines, ids, open_ids, live


def _count_line(tree: Tree, ids, open_ids, live) -> list:
    views = tree.all_views()
    per_status = {}
    for v in views:
        per_status[v.status or "?"] = per_status.get(v.status or "?", 0) + 1
    batches = ", ".join("%s %d" % (w, per_status[w]) for w in BATCH_STATUSES + ("?",) if w in per_status) or "нет"
    finds = tree.findings_by_id()
    in_batch = sum(1 for i in open_ids if i in live)
    in_find = sum(1 for i in open_ids if i not in live and i in finds)
    all_f = [f for p in tree.piles.values() for f in p.findings]
    top = max([int(i[2:]) for i in ids] + [0])
    line = ("кучек: %d; пачек: %s; открытых id: %d (в пачках %d / в находках %d / не разложено %d); "
            "находок без id: %d; не разобрано находок: %d; закрытых: %d; следующий свободный B-id: B-%03d "
            "(выдаёт только интегратор на main); остатков без исполнителя: %d"
            % (len(tree.piles), batches, len(open_ids), in_batch, in_find, len(open_ids) - in_batch - in_find,
               sum(1 for f in all_f if not f.id and not f.errors), sum(1 for f in all_f if f.errors),
               len(tree.backlog.closed_ids), top + 1, len(leftovers_unowned(tree))))
    nonid = ["%s/%d: %s" % (v.slug, v.n, "; ".join(v.row.nonid)) for v in views if v.row and v.row.nonid]
    return [line] + (["не-id в строках: " + "; ".join(nonid)] if nonid else [])


BOARD_HEAD = ("# Кучки и пачки\n\nГенерирует `python tools/piles.py board` из карточек `plans/piles/*/README.md`, "
              "файлов пачек `plans/piles/*/batch-*.md`, папок `findings/` и раздела «Закрыто» `plans/BACKLOG.md` "
              "— руками не править.")


def render_board(tree: Tree):
    """-> (text, counts). Deterministic: no clock, no mtime, no stamp (P4); LF, ends with one newline."""
    toc, ids, open_ids, live = toc_lines(tree)
    out = [BOARD_HEAD, "", "## 1. Доска", ""] + board_table(tree)
    out += ["", "## 2. Оглавление B-id", ""] + toc
    out += ["", "## 3. Счёт", ""] + _count_line(tree, ids, open_ids, live)
    counts = (len(tree.piles), len(tree.all_views()), len(ids))
    return "\n".join(out) + "\n", counts


def write_atomic(path: Path, text: str) -> None:
    write_bytes_atomic(path, text.encode("utf-8"))


def write_bytes_atomic(path: Path, raw: bytes) -> None:
    """A temp file next to `path`, then os.replace: a reader never sees half a file (also what a rollback writes with)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix=".piles-", suffix=".tmp")
    try:
        with os.fdopen(fd, "wb") as fh:
            fh.write(raw)
        os.replace(tmp, path)
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


def untracked_warning(tree: Tree) -> list:
    if not tree.untracked:
        return []
    return ["piles board: WARNING: untracked file(s) under plans/piles feed plans/PILES.md: %s -- `git add` them, or "
            "the next committer's `board --check` goes stale" % ", ".join(tree.untracked)]


def unreadable_warning(tree: Tree) -> list:
    """One line per finding file the board could not read: the rest of the board is still built, so the way out is named."""
    return ["piles board: WARNING: unreadable finding %s (%s) -- left out of the table of contents; save it as UTF-8 and run "
            "board again" % (f.path, f.unreadable) for p in tree.piles.values() for f in p.findings if f.unreadable]


def board_triggers(staged) -> bool:
    return any(p.startswith(PILES_REL + "/") or p in (BACKLOG_REL, BOARD_REL) for p in staged)


def cmd_board(args, root) -> int:
    if args.if_staged and not board_triggers(staged_paths(root)):
        print("piles board: no plans/piles or BACKLOG path staged -- not checked")
        return 0
    tree = load_tree(root, with_untracked=True, tolerant=True)
    text, (n_piles, n_batches, n_ids) = render_board(tree)
    target = root / BOARD_REL
    warnings = untracked_warning(tree) + unreadable_warning(tree)
    if not args.check:
        write_atomic(target, text)
        print("piles board: wrote %s: %d piles, %d batches, %d ids" % (BOARD_REL, n_piles, n_batches, n_ids))
        return _print_all(warnings, 0)
    fix = "run python tools/piles.py board and stage plans/PILES.md"
    if not target.is_file():
        print("piles board: %s is missing -- %s" % (BOARD_REL, fix))
        return _print_all(warnings, 2)
    if read_text(target) != text:
        print("piles board: %s is stale -- %s" % (BOARD_REL, fix))
        return _print_all(warnings, 2)
    print("piles board: up to date (%d piles, %d batches, %d ids)" % (n_piles, n_batches, n_ids))
    return _print_all(warnings, 0)


def _print_all(lines, code) -> int:
    for line in lines:
        print(line)
    return code


# ============================================================================================
# check: the door
# ============================================================================================

def door_lines(msg: str):
    """-> (doors, notes). A door is a 'piles-skip: <item>[, <item>] -- <reason>' line in PROSE position of the
    message (not in a code fence, not in a quote); a degraded or failed scanner counts NO door (fail-closed)."""
    msg = msg.replace("\r\n", "\n").replace("\r", "\n")
    found = list(DOOR_RE.finditer(msg))
    if not found:
        return [], []
    try:
        scan = md_regions.scan(msg)
        reason = scan.reason if scan.degraded else None
    except Exception as exc:                      # a scanner crash must not open a door
        scan, reason = None, "the message scanner failed (%s)" % exc
    if reason:
        return [], ["piles-skip: not counted -- the commit-message scanner is degraded (%s); fix the message "
                    "(shorten it, balance code fences) and commit again" % reason]
    doors, notes = [], []
    for m in found:
        kinds = md_regions.kind_at(scan, m.start("kw"))
        if not kinds or set(kinds) & {md_regions.KIND_FENCED, md_regions.KIND_BLOCKQUOTE,
                                      md_regions.KIND_INLINE_CODE, md_regions.KIND_NOTES,
                                      md_regions.KIND_EMBEDDED_DOC}:
            continue
        names = [s.strip().lower() for s in m.group("items").split(",") if s.strip()]
        items = [ITEM_ALIASES.get(n) for n in names]
        if not names or None in items:
            bad = names[items.index(None)] if None in items else ""
            notes.append('piles-skip: unknown item "%s" -- items: %s' % (bad, ITEMS_HELP))
            continue
        doors.append((set(items), m.group("reason").strip(), m.group(0).strip()))
    return doors, notes


# ============================================================================================
# check: items
# ============================================================================================

CARDS_AND_FINDINGS = "*cards-and-findings*"       # a carrier: any staged card, finding, batch file or BACKLOG.md (a9, P6, V1)
# V1 (t-593): a freeze commit staging only plans/BACKLOG.md, or a batch file hand-set to "закрыта", creates a9 reds
# as surely as a deleted finding does -- they are carriers too, or the commit passes as "carried (not blocking)".
CARD_OR_FINDING_RE = re.compile(r"^plans/piles/[^/_.][^/]*/(?:README\.md|findings/.+|batch-[^/]+\.md)$")


@dataclasses.dataclass
class Red:
    msg: str
    carriers: tuple


@dataclasses.dataclass
class ItemResult:
    reds: list = dataclasses.field(default_factory=list)
    ok: str = ""
    notes: list = dataclasses.field(default_factory=list)
    not_checked: str = ""


@dataclasses.dataclass
class Ctx:
    tree: Tree
    root: Path
    staged: object            # set of staged paths, or None for --all
    base: str                 # the rev (g) compares with
    frozen_ref: str = "origin/main"   # the rev (v) compares with: ORIGIN, or the --base sha when the flag is given

    def touches(self, carriers) -> bool:
        """True when the red is carried by this commit: --all, or a staged path is one of its carriers."""
        if self.staged is None:
            return True
        if CARDS_AND_FINDINGS in carriers and (BACKLOG_REL in self.staged
                                               or any(CARD_OR_FINDING_RE.match(p) for p in self.staged)):
            return True
        return any(c in self.staged for c in carriers)


def _pile_paths(tree, slug, n=None):
    p = tree.piles.get(slug)
    if p is None:
        return ()
    out = [p.card_rel]
    out += [b.path for b in p.batches if n is None or b.n == n]
    return tuple(out)


def _placement_dupes(tree, finds):
    reds = []
    for ident, fl in sorted(finds.items()):
        if len(fl) > 1:
            paths = [f.path for f in fl]
            reds.append(Red("%s is in %d finding files: %s -- an id has one home; keep one file and delete the others"
                            % (ident, len(fl), ", ".join(paths)), tuple(paths)))
    whole = {}
    for v, m in tree.member_rows():
        if not m.partial and v.status != "закрыта":
            whole.setdefault(m.id, []).append(v)
    for ident, vs in sorted(whole.items()):
        keys = sorted({(v.slug, v.n) for v in vs})
        car = tuple(c for s, n in keys for c in _pile_paths(tree, s, n))
        if len(keys) > 1:
            reds.append(Red("%s is a whole member of %d live batches (%s) -- an id has one home; keep it in one batch row"
                            % (ident, len(keys), ", ".join("%s/%d" % k for k in keys)), car))
        homes = {s for s, _ in keys} | {f.path.split("/")[2] for f in finds.get(ident, [])}
        if len(homes) > 1:
            pile = keys[0][0]
            reds.append(Red("%s has homes in %d piles (%s) -- an id lives in one pile; move the finding to "
                            "plans/piles/%s/findings/ (the pile of the batch)" % (ident, len(homes), ", ".join(sorted(homes)), pile),
                            car + tuple(f.path for f in finds.get(ident, []))))
    return reds


def closed_but_placed(tree: Tree, finds) -> dict:
    """{closed id: the files that still place it}: a finding, or a WHOLE member of a live batch. The one verdict of check
    (а)5 and of the board's «(и открыт — ошибка)» (m-5, t-593). A PARTIAL member of a live batch does not place a closed
    id: `close --id` may close a partial member's id (the owner's word), and the Строки cell of a taken batch is frozen
    by (в), so a red here could not be cleared but by a door."""
    out = {}
    for ident in sorted(tree.backlog.closed_ids):
        homes = [f.path for f in finds.get(ident, [])]
        homes += [p for v, m in tree.member_rows() if m.id == ident and not m.partial and v.status != "закрыта"
                  for p in _pile_paths(tree, v.slug, v.n)]
        if homes:
            out[ident] = homes
    return out


def _placement_known(tree, finds):
    reds = []
    bl = tree.backlog
    known = bl.open_ids | bl.closed_ids | set(finds)
    for v, m in tree.member_rows():
        if m.id not in known:
            reds.append(Red("unknown id %s in the row of batch %s/%d (the card) -- it is in no BACKLOG row, no closed row "
                            "and no finding; fix the id or write its finding" % (m.id, v.slug, v.n), (tree.piles[v.slug].card_rel,)))
    for ident in sorted(bl.open_ids & bl.closed_ids):
        reds.append(Red("%s is both open and closed in plans/BACKLOG.md -- delete the stale row" % ident, (BACKLOG_REL,)))
    for ident, homes in sorted(closed_but_placed(tree, finds).items()):
        reds.append(Red("%s is closed but still placed (%s) -- a closed id is not placed anywhere; remove the "
                        "finding or the batch-row member" % (ident, ", ".join(sorted(set(homes)))), tuple(homes)))
    return reds


def _placement_form(tree):
    reds = []
    for v in tree.all_views():
        if v.row is None or v.file is None:
            continue
        in_row = {m.id for m in v.row.members}
        for node in v.file.nodes:
            if ID_RE.fullmatch(node.id) and node.id not in in_row:
                reds.append(Red("the batch file names %s, the card row does not (%s/%d) -- add %s to the Строки cell of "
                                "the card row" % (node.id, v.slug, v.n, node.id), (v.file.path, tree.piles[v.slug].card_rel)))
    for p in tree.piles.values():
        for f in p.findings:
            if f.errors:
                continue
            if f.name_id and f.name_id != f.id:
                reds.append(Red('finding file name says %s, its header says id "%s" -- make them agree' % (f.name_id, f.id or "—"), (f.path,)))
            if f.pile and f.pile != p.slug:
                reds.append(Red('finding header says кучка "%s" but the file is in pile "%s" -- the folder wins; fix the header '
                                "or move the file" % (f.pile, p.slug), (f.path,)))
    return reds


def _placement_all_placed(tree, finds):
    bl = tree.backlog
    live = {m.id for v, m in tree.member_rows() if v.status != "закрыта"}
    reds = []
    for ident in sorted((bl.open_ids | (set(finds) - bl.closed_ids)), key=lambda s: int(s[2:])):
        if ident not in finds and ident not in live:
            reds.append(Red("%s is open but placed nowhere -- put it in a card batch row or write its finding in "
                            "plans/piles/<pile>/findings/" % ident, ()))
    return reds


def check_placement(ctx: Ctx) -> ItemResult:
    tree, res = ctx.tree, ItemResult()
    finds = tree.findings_by_id()
    res.reds += _placement_dupes(tree, finds) + _placement_known(tree, finds) + _placement_form(tree)
    if tree.backlog.locks:
        for r in _placement_all_placed(tree, finds):
            # a9 is carried by a card, a finding, a batch file or BACKLOG.md, changed or deleted (P6, V1)
            res.reds.append(Red(r.msg, (CARDS_AND_FINDINGS,)))
    else:
        res.notes.append('BACKLOG.md is not frozen yet (no piles-freeze line) -- duplicates and unknown ids checked; '
                         '"every open id placed" starts with the freeze (node F0-3)')
    res.ok = "%d open ids, %d closed, %d findings, %d batch-row members" % (
        len(tree.backlog.open_ids), len(tree.backlog.closed_ids), sum(len(v) for v in finds.values()), len(tree.member_rows()))
    return res


def _norm_token(tok: str) -> str:
    t = tok.strip().replace("\\", "/")
    return t[len("ai-packages/qa-factory/"):] if t.startswith("ai-packages/qa-factory/") else t


def _is_glob(t):
    return "*" in t or "?" in t


def _expand_braces(t: str):
    """'a/{b,c}.py' -> ['a/b.py', 'a/c.py']: ONE level, several groups multiply. None for a nested, unclosed or stray brace --
    the part is unreadable and a zone must then match nothing (a wrong guess of a pile is worse than none)."""
    open_at, close_at = t.find("{"), t.find("}")
    if open_at < 0 and close_at < 0:
        return [t]
    if open_at < 0 or close_at < open_at or "{" in t[open_at + 1:close_at]:
        return None
    tails = _expand_braces(t[close_at + 1:])
    if tails is None:
        return None
    return [t[:open_at] + alt.strip() + tail for alt in t[open_at + 1:close_at].split(",") for tail in tails]


def _split_outside_braces(text: str) -> list:
    out, depth, cur = [], 0, []
    for ch in text:
        depth += (ch == "{") - (ch == "}" and depth > 0)
        if ch == "," and depth == 0:
            out.append("".join(cur).strip())
            cur = []
        else:
            cur.append(ch)
    return out + ["".join(cur).strip()]


def parse_zone(zone: str):
    """The ONE reader of a card's `зона:` (the grammar lives in plans/piles/_template/README.md): -> (patterns, errors).
    A part is a backtick token (a value that was one backtick span reaches us unwrapped by `header_pairs`: then the commas
    outside braces split it); `—`/empty = no zone = ([], []); `{a,b}` expands one level; a trailing `/` or `…` means
    everything under the folder (`/**`); the token is normalised by `_norm_token` (the package prefix is dropped: the same
    space the check (б) compares in). A part that cannot be read is NOT guessed: it is returned in `errors` and matches
    nothing. Matching is `forge_metrics.compile_glob` over these patterns."""
    z = (zone or "").strip()
    if z in NO_VAL:
        return [], []
    tokens = BACKTICK_RE.findall(z) or [p for p in _split_outside_braces(z) if p]
    patterns, errors = [], []
    for tok in tokens:
        t = _norm_token(tok)
        if t.endswith("…"):
            t = t[:-1].rstrip("/") + "/**"
        elif t.endswith("/"):
            t += "**"
        expanded = None if (not t.strip("/*") or any(c.isspace() for c in t)) else _expand_braces(t)
        if expanded is None:
            errors.append("zone part `%s` cannot be read -- expected a path, one level of {a,b}, no spaces; it matches nothing" % tok)
        else:
            patterns += expanded
    return patterns, errors


def tokens_overlap(a: str, b: str) -> bool:
    """Two writer tokens may touch the same file. Errs towards TRUE (a false red has doors; a false green on equal
    literals has none)."""
    if a == b:
        return True
    for x, y in ((a, b), (b, a)):
        if _is_glob(x) and compile_glob(x)[0].match(y):
            return True
        if _is_glob(x) and "/" not in x and compile_glob(x)[0].match(y.rsplit("/", 1)[-1]):
            return True
        if x.endswith("/") and y.startswith(x):
            return True
        if "/" not in x and not _is_glob(x) and y.rsplit("/", 1)[-1] == x:
            return True
    if _is_glob(a) and _is_glob(b):
        pa, pb = re.split(r"[*?]", a, 1)[0], re.split(r"[*?]", b, 1)[0]
        return pa.startswith(pb) or pb.startswith(pa)
    return False


def writers_of(b: BatchFile) -> list:
    """Normalised writer tokens of the nodes that still write (status not принято/отклонено, P5)."""
    out = []
    for n in b.nodes:
        if n.status in NOT_WRITING:
            continue
        out += [_norm_token(t) for t in n.writers]
    return sorted(set(out))


def _queue_dirs(b: BatchFile, k1, k2):
    """The ordered pairs ((slug, N) before (slug, N)) this file's queue lines give for the batches k1 and k2."""
    return {((a, n), (c, m)) for a, n, c, m in b.queue if {(a, n), (c, m)} == {k1, k2}}


def fn_lists_of(b: BatchFile) -> dict:
    """{normalised file token: set of items} the batch declares for a file it writes (D-0048; an item is `name`, `Class.name` or
    `+name`, see parse_fn_list). The `функции:` lines of the batch's «Ход» win where they exist (a taken batch's cells are frozen,
    its Ход is how it narrows the claim; they union with the cells' lists); otherwise the file has a list only when EVERY node that
    still writes it carries one on it -- one node that writes the file bare is a whole-file claim. A Ход list for a file no
    still-writing node writes is not here (hod_ignored names it)."""
    per = {}
    for n in b.nodes:
        if n.status in NOT_WRITING:
            continue
        for t in n.writers:
            per.setdefault(_norm_token(t), []).append(n.lists.get(t))
    hod = {}
    for t, names in b.hod_lists.items():
        hod.setdefault(_norm_token(t), set()).update(names)
    out = {}
    for tok, entries in per.items():
        own = set().union(*[set(e) for e in entries if e])
        if hod.get(tok):
            out[tok] = own | hod[tok]
        elif all(entries):
            out[tok] = own
    return out


def hod_ignored(b: BatchFile) -> list:
    """The files a `функции:` line of the batch's Ход lists but that no still-writing node of the batch writes: such a list narrows
    nothing and is ignored (check_overlap prints one WARN line per batch; never red -- a stale line must not stop the factory)."""
    writes = set(writers_of(b))
    return sorted({_norm_token(t) for t in b.hod_lists} - writes)


def defined_names(root, token):
    """-> (names, why): what a Python file defines -- a set holding the bare name of every `def` at module level or inside a class
    (also under an if / try at those levels; not a nested helper), `Class.name` for each member, and `Class.` (with the dot) for
    each class -- or (None, why) when the file cannot be read as Python. `token` is a path from the repo root or from
    ai-packages/qa-factory/ (the way _norm_token leaves it). The file is read from the WORKING TREE under `root`: the tree the batch
    files are read from and, for `--msg-file` on a branch, the branch's own code; so a function the node ADDS is not there yet --
    it is listed as `+name` (judged by _item_verdict), not as a name."""
    for base in ("", "ai-packages/qa-factory/"):
        p = Path(root) / (base + token)
        if p.is_file():
            break
    else:
        return None, "there is no file %s (or ai-packages/qa-factory/%s) in the checked tree" % (token, token)
    try:
        tree = ast.parse(p.read_bytes().decode("utf-8-sig"))
    except (SyntaxError, ValueError, UnicodeDecodeError, OSError) as e:
        return None, "%s cannot be read as Python (%s)" % (token, type(e).__name__)
    names, todo = set(), [(tree, "")]
    while todo:
        parent, cls = todo.pop()
        for ch in ast.iter_child_nodes(parent):
            if isinstance(ch, (ast.FunctionDef, ast.AsyncFunctionDef)):
                names.add(ch.name)
                if cls:
                    names.add("%s.%s" % (cls, ch.name))
            elif isinstance(ch, ast.ClassDef):
                names.add(ch.name + ".")
                todo.append((ch, ch.name))
            else:
                todo.append((ch, cls))
    return names, ""


def _item_verdict(item, defs):
    """'' (fine) | 'undefined' | 'notnew' for one list item against what the file defines. `name` must be defined anywhere (module
    level or in a class); `Class.name` must be a member of that class (the class must exist and define it). `+name` is a function
    the node ADDS: no existence needed, but it must NOT be defined yet ('notnew': then it is not new -- drop the plus);
    `+Class.name` needs the class to exist."""
    parts = item.lstrip("+").split(".")
    key = ".".join(parts[-2:])
    if item.startswith("+"):
        if len(parts) > 1 and parts[-2] + "." not in defs:
            return "undefined"
        return "notnew" if key in defs else ""
    return "" if key in defs else "undefined"


def _queue_door(k1, k2):
    first, second = sorted([k1, k2], key=lambda k: (k[1], k[0]))
    return 'add the line "очередь: %s/%d → %s/%d" to the preamble of BOTH batch files (the same direction)' % (
        first[0], first[1], second[0], second[1])


def _list_verdicts(k1, k2, l1, l2, pairs, root):
    """For the overlapping pairs that are ONE literal Python file with a function list on BOTH sides: -> (handled pairs, red
    messages). Every named name must be defined in the file (FR-59: a misspelt name is red, not a quiet 'disjoint'); the two
    sets must not meet. A pair whose file cannot be read is red too -- the lists cannot be judged. Any other pair is not handled
    here (the file lock stays)."""
    handled, msgs = set(), []
    both = "%s/%d and %s/%d both write" % (k1[0], k1[1], k2[0], k2[1])
    door = "%s, or piles-skip: б" % _queue_door(k1, k2)
    for x, y in pairs:
        if x != y or x not in l1 or x not in l2 or _is_glob(x) or not x.endswith(".py"):
            continue
        handled.add((x, y))
        names, why = defined_names(root, x)
        if names is None:
            msgs.append("%s %s with function lists, but %s -- the lists cannot be checked; write the path from the repo root "
                        "(e.g. scripts/story_run.py), or %s" % (both, x, why, door))
            continue
        for k, lst in ((k1, l1[x]), (k2, l2[x])):
            msgs += _item_reds(k, x, lst, names, door)
        b1, b2 = {fn_bare(i) for i in l1[x]}, {fn_bare(i) for i in l2[x]}
        common = sorted(b1 & b2)
        if common:
            new_in_both = sorted({fn_bare(i) for i in l1[x] if i[0] == "+"} & {fn_bare(i) for i in l2[x] if i[0] == "+"})
            msgs.append("%s %s and both name %s%s -- the function lists must be disjoint: leave each name to ONE batch, or %s" % (
                both, x, ", ".join(common),
                " (%s: both claim to ADD it)" % ", ".join(new_in_both) if new_in_both else "", door))
    return handled, msgs


def _item_reds(k, x, items, names, door):
    """The red messages for the items one batch lists for file `x` that the file contradicts (see _item_verdict): the first
    door of the refusal is the `функции:` line of the batch's «Ход» (writable in a taken batch), then the cell (a batch not yet
    taken: a taken batch's cell is frozen by (в), and the Ход list unions with the cell's, so it cannot remove a cell's name)."""
    who = "%s/%d" % k
    verdicts = {i: _item_verdict(i, names) for i in items}
    undefined = sorted(i for i, v in verdicts.items() if v == "undefined")
    notnew = sorted(i for i, v in verdicts.items() if v == "notnew")
    msgs = []
    if undefined:
        msgs.append("%s lists %s for %s, which %s defined in the file (a def at module level or inside a class; `Class.name` needs "
                    "that class to define it; `+name` needs no def, `+Class.name` needs the class; names are case-sensitive) -- "
                    "correct the name where it is written: in a `функции:` line of the batch's «Ход» (writable in a taken batch), "
                    "or in its «Пишет в» cell (a batch not yet taken: a taken batch's cell is frozen), or %s" % (
                        who, ", ".join(undefined), x, "is not" if len(undefined) == 1 else "are not", door))
    if notnew:
        msgs.append("%s lists %s as ADDED for %s, but the file already defines %s -- not new: drop the plus (the name then stays "
                    "this batch's and must be disjoint from the other's), or %s" % (
                        who, ", ".join(notnew), x, "it" if len(notnew) == 1 else "them", door))
    return msgs


def _pair_overlap(b1, b2, k1, k2, root):
    """-> the red messages of one pair of active batches ([] = green): the file lock of (б) with its two doors, the `очередь:` line
    in both preambles or (D-0048) a disjoint function list of each batch for the shared file."""
    w1, w2 = writers_of(b1), writers_of(b2)
    pairs = sorted({(x, y) for x in w1 for y in w2 if tokens_overlap(x, y)})
    if not pairs:
        return []
    d1, d2 = _queue_dirs(b1, k1, k2), _queue_dirs(b2, k1, k2)
    if d1 and d1 == d2 and len(d1) == 1:
        return []                        # both files say the same single direction: the legal queue (lists are not read)
    l1, l2 = fn_lists_of(b1), fn_lists_of(b2)
    handled, msgs = _list_verdicts(k1, k2, l1, l2, pairs, root)
    left = [(x, y) for x, y in pairs if (x, y) not in handled]
    if not left:
        return msgs
    hits = sorted({x if x == y else "%s ~ %s" % (x, y) for x, y in left})
    names = "%s/%d and %s/%d both write: %s" % (k1[0], k1[1], k2[0], k2[1], ", ".join(hits[:3]) + (" ..." if len(hits) > 3 else ""))
    if d1 and d2:
        msgs.append("%s -- the two batches disagree on the order (%s vs %s); make both preambles say the same direction" % (
            names, "; ".join(sorted("%s/%d -> %s/%d" % (a[0], a[1], b[0], b[1]) for a, b in d1)),
            "; ".join(sorted("%s/%d -> %s/%d" % (a[0], a[1], b[0], b[1]) for a, b in d2))))
        return msgs
    lacking = [(x, [k for k, lst in ((k1, l1), (k2, l2)) if x not in lst]) for x, y in left
               if x == y and x.endswith(".py") and not _is_glob(x)]
    other = (", or give %s -- add the line `функции: %s (f1, f2)` to its «Ход» (the door of a taken batch: its cell is frozen), or write "
             "`%s (f1, f2)` in its «Пишет в» cell (a batch not yet taken); both batches need a list on the file, disjoint "
             "(`+name` for a function the batch adds)" % ("; and ".join("%s a function list for %s" % (
                 " and ".join("%s/%d" % k for k in ks), x) for x, ks in lacking), lacking[0][0], lacking[0][0])) if lacking else ""
    msgs.append("%s -- %s%s, or piles-skip: б" % (names, _queue_door(k1, k2), other))
    return msgs


def check_overlap(ctx: Ctx) -> ItemResult:
    active = [(v.file, (v.slug, v.n)) for v in ctx.tree.all_views()
              if v.file is not None and v.status in ACTIVE]
    res = ItemResult()
    for b, k in active:
        if hod_ignored(b):
            res.notes.append("WARN: %s/%d: a `функции:` line of its «Ход» lists functions for %s, which no node of the batch that still "
                             "writes names in its «Пишет в» -- ignored (the list narrows nothing; write the file in the cell as the "
                             "node does, or drop the line)" % (k[0], k[1], ", ".join(hod_ignored(b))))
    for i in range(len(active)):
        for j in range(i + 1, len(active)):
            (b1, k1), (b2, k2) = active[i], active[j]
            for msg in _pair_overlap(b1, b2, k1, k2, ctx.root):
                res.reds.append(Red(msg, (b1.path, b2.path)))
    res.ok = "%d active batches" % len(active)
    return res


ORIGIN = "origin/main"
FROZEN = ("в работе", "сдано", "принято")           # a batch in one of these ON origin/main is taken (P7)
ORIGIN_BATCH_RE = re.compile(r"^plans/piles/([^/_.][^/]*)/(batch-\d{1,3}[^/]*\.md)$")
CARD_FROZEN_COLS = (("what", "Что"), ("rows_cell", "Строки"), ("size", "Размер"), ("who", "Взял"), ("branch", "Ветка"))
PAIR_NAMES = {"статус": "статус", "взял": "взял", "ветка": "ветка", "mr": "MR"}
MASK = "·"                                           # what an allowed-to-change value is replaced by before comparing


class NoOrigin(Exception):
    """origin/main cannot be read here: (в) says NOT CHECKED and names the door, it never passes silently."""


def origin_snapshot(root, ref=ORIGIN):
    """-> (sha, {(slug, N): [batch file paths on the ref]}). NoOrigin when the ref or git is not there."""
    rc, out = git(root, "rev-parse", "--verify", "--quiet", ref + "^{commit}")
    if rc != 0:
        raise NoOrigin(out.decode("utf-8", "replace").strip() or "no ref %s" % ref)
    sha = out.decode("utf-8", "replace").strip()
    rc, out = git(root, "ls-tree", "-r", "--name-only", "-z", sha, "--", PILES_REL)
    if rc != 0:
        raise NoOrigin("git ls-tree failed on %s" % ref)
    pairs = {}
    for p in out.decode("utf-8", "replace").split("\0"):
        m = ORIGIN_BATCH_RE.match(p)
        bm = BATCH_NAME_RE.match(m.group(2)) if m else None
        if bm:
            pairs.setdefault((m.group(1), int(bm.group(1))), []).append(p)
    return sha, {k: sorted(v) for k, v in pairs.items()}


def replace_pairs(line: str, edits: dict) -> str:
    """The header line with the value of each key in `edits` ({lower-case key: new text}) replaced; every other segment
    stays byte for byte. A key the line does not have is appended as ' | key: value'."""
    parts, seen = split_pipes(line), set()
    for i, seg in enumerate(parts):
        if ":" not in seg:
            continue
        key, val = seg.split(":", 1)
        k = key.strip().strip("`").strip().lower()
        if k in edits and k not in seen:
            seen.add(k)
            lead = val[:len(val) - len(val.lstrip())] or " "
            parts[i] = key + ":" + lead + edits[k] + val[len(val.rstrip()):]
    out = "|".join(parts)
    for k in edits:
        if k not in seen:
            out = out.rstrip() + " | %s: %s" % (PAIR_NAMES.get(k, k), edits[k])
    return out


def section_name(line: str):
    """The lower-cased name of a section heading, or None when the line is not one. A heading is a RAW column-0 `## ` line --
    no fence or comment awareness: the one locator of (в)'s `_frozen_lines` and of the «Остатки» carry-over gate."""
    return line[3:].strip().lower() if line.startswith("## ") else None


def _frozen_lines(text: str):
    """-> (lines, queue lines). The batch file as (в) compares it: the header's статус/MR, the Статус cells of the node
    and evidence tables and the whole Ход and Остатки sections are masked; очередь: lines are returned apart (they may
    only be added); table rows are compared cell by cell, not by their padding."""
    out, queue, section, status_col = [], set(), "", -1
    pre, header_seen = True, False                       # pre: above '## Узлы', where the header and queue lines live
    lines = text.split("\n")
    for line, (kind, cells) in zip(lines, walk_table(lines)):         # walk_table: the one table boundary, shared with `close`
        name = section_name(line)
        if name is not None:
            section = name
            pre = pre and not section.startswith("узлы")
            out.append(line.rstrip())
            continue
        if section.startswith(("ход", "остатки")):
            continue
        if pre and not header_seen and "кучка:" in line.lower():
            header_seen = True
            # issue: -- old headers, no longer written; the mask stays so a taken batch that carries it never goes red (V3, t-593)
            out.append(replace_pairs(line, {"статус": MASK, "mr": MASK, "issue": MASK}).strip())
            continue
        q = QUEUE_RE.match(line) if pre else None
        if q:
            queue.add((q.group(1), int(q.group(2)), q.group(3), int(q.group(4))))
            continue
        if kind is not None and section.startswith(("узлы", "живые доказательства")):
            if kind == "header":                         # the header row of this table
                status_col = next((i for i, c in enumerate(cells) if c.lower().startswith("статус")), -1)
            elif kind == "row" and 0 <= status_col < len(cells):
                cells[status_col] = MASK
            out.append("|".join(cells))
            continue
        out.append(line.rstrip())
    return out, queue


def _shorten(s, limit=110):
    s = " ".join(str(s).split())
    return s if len(s) <= limit else s[:limit - 1] + "…"


def _compare_batch(sha, tf: BatchFile, ob: BatchFile, otext: str, ttext: str):
    """The reds of one taken batch's file against its text on origin/main (Р9 allowed list, P5, P7)."""
    reds, c = [], (tf.path,)
    if tf.status is not None and ob.status is not None and STATUS_ORDER[tf.status] < STATUS_ORDER[ob.status]:
        reds.append(Red('%s: the status moved back from "%s" (origin/main %s) to "%s" -- a taken batch\'s status only goes forward '
                        "(в работе → сдано → принято → закрыта)" % (tf.path, ob.status, sha[:7], tf.status), c))
    ol, oq = _frozen_lines(otext)
    tl, tq = _frozen_lines(ttext)
    for q in sorted(oq - tq):
        reds.append(Red('%s: the queue line "очередь: %s/%d → %s/%d" of origin/main %s was deleted -- queue lines of a taken '
                        "batch only grow" % ((tf.path,) + q + (sha[:7],)), c))
    for o, t in itertools.zip_longest(ol, tl):
        if o != t:
            reds.append(Red('%s: line "%s" differs from origin/main %s%s; a taken batch changes only its Ход, Остатки, the '
                            "Статус cells, queue lines (added) and the header's статус/MR/issue" % (
                                tf.path, _shorten(t if t is not None else "(the file ends here)"), sha[:7],
                                ' (it was "%s")' % _shorten(o) if o is not None else ""), c))
            break
    return reds


def _compare_card(root, sha, view: View, slug: str, n: int, card_rel: str):
    """The card row of a taken batch: only Статус and MR may change (P7)."""
    ctext = git_show(root, sha, card_rel)
    orow = next((r for r in parse_card(ctext, card_rel).rows if r.n == n), None) if ctext is not None else None
    if orow is None:
        return []
    if view.row is None:
        return [Red("%s: the row %d of a taken batch was removed from the card (origin/main %s) -- the row stays until "
                    "`close` closes the batch" % (card_rel, n, sha[:7]), (card_rel,))]
    for attr, label in CARD_FROZEN_COLS:
        was, now = getattr(orow, attr), getattr(view.row, attr)
        if " ".join(was.split()) != " ".join(now.split()):
            return [Red('%s: row %d, column %s changed from "%s" to "%s" (origin/main %s); the card row of a taken batch '
                        "changes only its Статус and MR" % (card_rel, n, label, _shorten(was, 60), _shorten(now, 60), sha[:7]),
                        (card_rel,))]
    # m-1 (t-593): the Статус cell may change, but only forward -- the batch file's status has the same rule above
    if orow.status is not None and view.row.status is not None and STATUS_ORDER[view.row.status] < STATUS_ORDER[orow.status]:
        return [Red('%s: row %d, column Статус moved back from "%s" (origin/main %s) to "%s" -- the card row of a taken batch '
                    "only goes forward (в работе → сдано → принято → закрыта)"
                    % (card_rel, n, _shorten(orow.status_raw, 60), sha[:7], _shorten(view.row.status_raw, 60)), (card_rel,))]
    return []


def _judge_pair(ctx: "Ctx", sha, slug, n, paths):
    """-> (reds, frozen?). A pair frozen on origin/main is judged whatever its status in the tree says (P7)."""
    otext = git_show(ctx.root, sha, paths[0])
    if otext is None:
        return [], False
    ob = parse_batch(otext, paths[0], n)
    if ob.status not in FROZEN:
        return [], False                                  # new or not yet taken on origin/main: free (E21)
    pile = ctx.tree.piles.get(slug)
    view = next((v for v in pile.views() if v.n == n), None) if pile else None
    tf = view.file if view else None
    if tf is None:
        return [Red("%s: the file of a taken batch was removed (%s/%d is \"%s\" on origin/main %s) -- a taken batch is closed "
                    "with `close`, not deleted or un-taken" % (paths[0], slug, n, ob.status, sha[:7]), (paths[0],))], True
    carriers = (tf.path,) if tf.path == paths[0] else (tf.path, paths[0])
    reds = [Red(r.msg, carriers) for r in _compare_batch(sha, tf, ob, otext, read_text(ctx.root / tf.path))]
    return reds + _compare_card(ctx.root, sha, view, slug, n, pile.card_rel), True


def check_frozen(ctx: Ctx) -> ItemResult:
    res = ItemResult()
    explicit = ctx.frozen_ref != ORIGIN                 # --base was given: that rev stands where origin/main stands
    try:
        sha, pairs = origin_snapshot(ctx.root, ctx.frozen_ref)
    except NoOrigin as exc:
        if explicit:
            res.not_checked = "the --base rev %s cannot be read here (%s); pass --base <rev> naming a commit of this repository" % (ctx.frozen_ref[:12], exc)
        else:
            res.not_checked = ('origin/main is not available here (%s); run "git fetch origin" and commit again to have it '
                               "checked; this commit is not blocked by (в)" % exc)
        return res
    frozen = 0
    for (slug, n), paths in sorted(pairs.items()):
        reds, is_frozen = _judge_pair(ctx, sha, slug, n, paths)
        res.reds += reds
        frozen += is_frozen
    res.notes.append("compared with %s %s" % ("--base" if explicit else "origin/main", sha[:7]))
    if explicit:
        res.reds = [Red(r.msg.replace("origin/main " + sha[:7], "the --base " + sha[:7]), r.carriers) for r in res.reds]
        rc, head = git(ctx.root, "rev-parse", "--verify", "--quiet", "HEAD^{commit}")
        if rc == 0 and head.decode("utf-8", "replace").strip() == sha:
            res.notes.append("the base is HEAD itself: no commit lies between them, only the working tree is compared with it")
    res.ok = "%d taken batch(es) on %s; every other batch is new or not yet taken: free" % (frozen, "the --base rev" if explicit else "origin/main")
    return res


def _lock_state(bl: Backlog):
    reds = []
    if len(bl.locks) > 1:
        reds.append(Red("two piles-freeze lines in %s (lines %s) -- keep one" % (BACKLOG_REL, ", ".join(str(n) for n, _ in bl.locks)),
                        (BACKLOG_REL,)))
    for n, v in bl.locks:
        if v is None:
            reds.append(Red('the piles-freeze line at %s:%d is malformed -- expected "piles-freeze: yyyy-mm-dd open=N closed=M"'
                            % (BACKLOG_REL, n), (BACKLOG_REL,)))
    return reds


def _g_after_freeze(tree, head: Backlog, freeze_commit: bool):
    bl = tree.backlog
    reds = []
    c = (BACKLOG_REL,)
    for ident in sorted(bl.open_ids - head.open_ids, key=lambda s: int(s[2:])):
        reds.append(Red("new open row %s: after the freeze a new item is a file in plans/piles/<pile>/findings/, not a row here" % ident, c))
    for ident in sorted(head.closed_ids - bl.closed_ids):
        reds.append(Red("closed row removed: %s -- the Закрыто table only grows (written by `close`)" % ident, c))
    for ident in sorted((head.open_ids - bl.open_ids) - bl.closed_ids):
        reds.append(Red("row vanished: %s was open and is neither open nor closed now -- an archive row only moves to Закрыто" % ident, c))
    if not freeze_commit:
        whole_closed = {m.id for v, m in tree.member_rows() if not m.partial and v.status == "закрыта"}
        for ident in sorted(bl.closed_ids - head.closed_ids):
            row = bl.first(ident, True)
            if ident not in whole_closed and not WORD_SUFFIX_RE.search(row.text):
                reds.append(Red("closed outside close: %s is a new closed row that is not a whole member of a batch with "
                                'status закрыта, and carries no "; закрыто <dd.mm.yyyy> по слову: <кто, дата>" suffix -- close it '
                                "with the `close` command" % ident, c))
    for ident in sorted(bl.open_ids & head.open_ids):
        if bl.first(ident, False).text.rstrip() != head.first(ident, False).text.rstrip():
            reds.append(Red("the archive row %s was edited -- an open row above Закрыто is read-only after the freeze; "
                            "put the new text in its finding" % ident, c))
    return reds


def check_backlog(ctx: Ctx) -> ItemResult:
    tree = ctx.tree
    bl = tree.backlog
    res = ItemResult()
    res.reds += _lock_state(bl)
    head_text = git_show(ctx.root, ctx.base, BACKLOG_REL)
    if head_text is None:
        res.not_checked = "%s is not available at %s here -- run inside the repository with a commit; this commit is not blocked by (г)" % (BACKLOG_REL, ctx.base)
        return res
    try:
        head = parse_backlog_rows(head_text)
    except CannotRun as exc:
        res.not_checked = "%s at %s cannot be read: %s" % (BACKLOG_REL, ctx.base, exc)
        return res
    locked_before, locked_now = bool(head.locks), bool(bl.locks)
    if not locked_before and not locked_now:
        res.not_checked = "not frozen yet (no piles-freeze line) -- the backlog guard starts with the freeze (node F0-3)"
        return res
    if locked_before and not locked_now:
        res.reds.append(Red("the freeze line was removed -- piles-freeze stays in %s for good; restore it" % BACKLOG_REL, (BACKLOG_REL,)))
        return res
    freeze_commit = not locked_before
    if freeze_commit:
        for n, v in bl.locks:
            if v and (v[1], v[2]) != (bl.n_open, bl.n_closed):
                res.reds.append(Red("the freeze line says open=%d closed=%d but the file has open=%d closed=%d -- write the real counts"
                                    % (v[1], v[2], bl.n_open, bl.n_closed), (BACKLOG_REL,)))
    res.reds += _g_after_freeze(tree, head, freeze_commit)
    res.ok = "%s (%s)" % ("freeze commit" if freeze_commit else "frozen", "compared with " + ctx.base)
    return res


def _node_reds(b: BatchFile):
    reds = []
    for n in b.nodes:
        who = "%s: node %s" % (b.path, n.id or "?")
        if n.executor.strip() in NO_VAL:
            reds.append(Red("%s has no Исполнитель -- name who works it (designer → builder → critic, builder, Lead)" % who, (b.path,)))
        if not n.writers and not re.search(r"\bнет\b", n.writes_cell, re.I):
            reds.append(Red('%s has no path in "Пишет в" -- expected at least one `path` in backticks, or the word "нет" '
                            "for a node that writes no file" % who, (b.path,)))
        if n.status is None:
            reds.append(Red('%s has status "%s", which starts with no known status word -- expected one of: %s '
                            "(a date or a note may follow the word)" % (who, n.status_raw, ", ".join(NODE_STATUSES)), (b.path,)))
    return reds


WHAT_ID_RE = re.compile(r"(?<![\w/-])B-\d{3,}(?![\w-])")     # a B-id in a «Что» cell, not one inside a file name (`findings/B-102-x.md`)
CROSS_CHECK_RE = re.compile(r"^[\s*_`>#-]*(?:сверка|проверить)(?!\w)", re.I)


def _coverage_reds(tree: Tree, v: View, card: str):
    """The row-id coverage of a batch (t-769, finding 20261013-pokrytie-uzlami-id-stroki): every member id of the card row's
    Строки cell stands in the «Что» cell of exactly ONE node of the batch file, and no node's «Что» names a B-id outside the row.
    The doors, each a judgment about what a node or a batch IS:
      - a PARTIAL member (a qualifier after the id in the row: `B-308 (а)`, `B-449 (потоки)`) is split across nodes by its
        parts, so it may stand in several -- but still in at least ONE (a member no node names is work nobody was given);
      - a CROSS-CHECK node (its «Что» starts with «сверка» / «проверить») re-reads ids that other nodes own, so its ids count
        neither toward "exactly one" nor as "outside the row";
      - an id that is a member of ANOTHER row of the same card is a reference to a sibling batch (`триггер — правка в B-419
        (пачка 2)`), not a claim on its work: it is not "outside the row" (an id of no row of this pile, or of another pile, is);
      - a CLOSED batch is history: its file and its row are frozen for good, so a red there could only be passed by a door;
      - a pile whose card has no «## Содержание» section is not in the t-717 form (older cards, and the mini trees of the tests):
        its nodes were never asked to carry row ids in «Что»; the contents test (tools/test_pile_cards_contents.py) refuses a
        real card without the section, and the template carries it, so a new pile is born inside the check.
    A row with no member (`—`) passes with no check. A repeated id inside ONE node's «Что» counts once; two ids of the row in
    one node are fine (one node, several members). Red names the batch, the id and how many nodes carry it."""
    if v.row is None or v.file is None or not v.row.members or v.status == "закрыта" or not tree.piles[v.slug].card.contents:
        return []
    whole = {m.id for m in v.row.members if not m.partial}
    in_row = {m.id for m in v.row.members}
    siblings = {m.id for r in tree.piles[v.slug].card.rows if r is not v.row for m in r.members}
    carry, outside = {}, []
    for node in v.file.nodes:
        if CROSS_CHECK_RE.match(node.what):
            continue
        for ident in dict.fromkeys(WHAT_ID_RE.findall(node.what)):
            if ident in in_row:
                carry.setdefault(ident, []).append(node.id)
            elif ident not in siblings:
                outside.append((node.id, ident))
    where, carriers = "%s/%d" % (v.slug, v.n), (v.file.path, card)
    reds = []
    for ident in sorted(in_row):
        nodes = carry.get(ident, [])
        if len(nodes) == 1 or (nodes and ident not in whole):
            continue
        reds.append(Red("batch %s: the row id %s stands in the «Что» of %d nodes (%s), want exactly 1 -- name it in one node of %s "
                        "(a partial member may stand in several; a cross-check node starting «сверка» / «проверить» does not count)"
                        % (where, ident, len(nodes), ", ".join(nodes) or "none", v.file.path), carriers))
    for node_id, ident in outside:
        reds.append(Red("batch %s: node %s names %s in its «Что», but the Строки cell of the card row does not -- add %s to the row "
                        "or take it out of the node (a cross-check node starting «сверка» / «проверить» may name other ids)"
                        % (where, node_id or "?", ident, ident), carriers))
    return reds


def _view_reds(tree: Tree, v: View):
    reds = []
    card = tree.piles[v.slug].card_rel
    if len(v.files) > 1:
        paths = [f.path for f in v.files]
        reds.append(Red("batch %s/%d has %d files (%s) -- one file per batch number; rename or merge" % (v.slug, v.n, len(paths), ", ".join(paths)),
                        tuple(paths)))
    if v.row is None and v.file is not None:
        reds.append(Red("%s: the batch file has no row %d in the card %s -- add the row to the batch table" % (v.file.path, v.n, card),
                        (v.file.path, card)))
    if v.row is not None and v.file is not None and v.row.status and v.file.status:
        if STATUS_ORDER[v.row.status] > STATUS_ORDER[v.file.status]:
            reds.append(Red('%s/%d: the card says "%s", the batch file says "%s" -- the card is ahead of the file; the file is the '
                            "truth while work runs, so bring the file up (or the card back)" % (v.slug, v.n, v.row.status_raw, v.file.status_raw),
                            (v.file.path, card)))
    if v.file is not None and v.file.has_nodes_table and not v.file.nodes and v.status in ("в работе", "сдано", "принято"):
        reds.append(Red("%s: a %s batch has an empty node table -- nobody works a batch without nodes; fill ## Узлы" % (v.file.path, v.status),
                        (v.file.path,)))
    for f in v.files:
        reds += _node_reds(f)
    return reds + _coverage_reds(tree, v, card)


BATCH_HEADINGS = ("## Бриф", "## Узлы")        # the headings an untaken batch file is born with (plans/piles/_template/batch.md)


def _contents_section(card_text: str):
    """The lines between the card's `## Содержание` line and the next `## ` line; None when the card has no such heading."""
    out, inside, seen = [], False, False
    for line in card_text.split("\n"):
        if line.startswith("## "):
            if inside:
                break
            inside = seen = line.rstrip() == "## Содержание"
        elif inside:
            out.append(line)
    return "\n".join(out) if seen else None


def _contents_counts(contents: str, row_ids, finding_names) -> list:
    """[(kind, key, k)]: every finding file name and every card-row id whose number of occurrences in the «Содержание» text is
    not exactly 1. A name counts as a whole token (`_name_re`: `x.md` inside `ax.md` does not count -- it may only UNDER-count,
    a false red); a B-id by `WHAT_ID_RE`. Fenced blocks and `<!-- -->` comments hide what they cover (`_batch_prose`): a name
    only in an example is not a row. A fence that never closes is ONE ("fence", why, 0) entry, never a pass."""
    try:
        prose = _batch_prose(contents, "the «Содержание» section", "a row after it would not be counted")
    except CannotRun as exc:
        return [("fence", str(exc), 0)]
    ids = WHAT_ID_RE.findall(prose)
    out = [("id", i, ids.count(i)) for i in sorted(set(row_ids)) if ids.count(i) != 1]
    for n in sorted(set(finding_names)):
        k = len(_name_re(n).findall(prose))
        if k != 1:
            out.append(("file", n, k))
    return out


def _contents_msg(kind: str, key: str, k: int) -> str:
    if kind == "fence":
        return key
    if kind == "file":
        return ("«Содержание» names findings/%s %d times, want exactly 1 -- add its row (path, type, суть, файлы, узел, решение "
                "владельца, связи) or remove the duplicate" % (key, k))
    return "«Содержание» names %s %d times, want exactly 1 -- name the id once in a row of «Содержание» (or remove the duplicate)" % (key, k)


def contents_problems(contents_text: str, row_ids, finding_names) -> list:
    """[str]: the reasons a card's «Содержание» text does not hold every finding file name and every card-row id EXACTLY once
    (pure; the one reader -- `check` (д) builds its reds from it and tools/test_pile_cards_contents.py calls it)."""
    return [_contents_msg(*c) for c in _contents_counts(contents_text, row_ids, finding_names)]


def _contents_reds(tree: Tree, pile: Pile) -> list:
    """(д): a pile whose card has `## Содержание` (the t-717 form) names every finding file of the pile and every member id of every
    card row exactly once there. A card without the section is not judged here (older form; the contents test refuses a real
    one in CI). Carriers: the card and the finding (an id: the card alone)."""
    if pile.card is None or not pile.card.contents:
        return []
    contents = _contents_section(read_text(tree.root / pile.card_rel))
    if contents is None:
        return []
    by_name = {f.name: f.path for f in pile.findings}
    row_ids = [m.id for r in pile.card.rows for m in r.members]
    reds = []
    for kind, key, k in _contents_counts(contents, row_ids, list(by_name)):
        carriers = (pile.card_rel, by_name[key]) if kind == "file" else (pile.card_rel,)
        reds.append(Red("%s: %s" % (pile.card_rel, _contents_msg(kind, key, k)), carriers))
    return reds


def batch_heading_problems(text: str) -> list:
    """[str]: one reason per heading of BATCH_HEADINGS that is not a whole line of the batch file (pure; the test and the gate share it)."""
    lines = {l.rstrip() for l in text.split("\n")}
    return ["an untaken batch has no «%s» heading -- write it from plans/piles/_template/batch.md" % h
            for h in BATCH_HEADINGS if h not in lines]


def _heading_reds(tree: Tree, b: BatchFile) -> list:
    """(д): an UNTAKEN batch file («ожидает» or an empty status) carries the template headings. A taken batch is not judged: its
    text is frozen by (в), and a red only a (в) door could pass would ask a frozen text to change."""
    raw = (b.status_raw or "").strip()
    if not (b.status == "ожидает" or raw in NO_VAL):
        return []
    return [Red("%s: %s" % (b.path, why), (b.path,)) for why in batch_heading_problems(read_text(tree.root / b.path))]


def check_form(ctx: Ctx) -> ItemResult:
    tree, res = ctx.tree, ItemResult()
    for pile in tree.piles.values():
        res.reds += [Red("%s: %s" % (path, msg), (path,)) for path, msg in pile.errors]
        res.reds += _contents_reds(tree, pile)
        for b in pile.batches:
            res.reds += _heading_reds(tree, b)
        # a finding the tolerant load could not read: ONE red. Its id is unknown, so it has no home in (а); the commit that
        # carries any card, finding, batch or BACKLOG is the one that must see it (the same carrier (а)5 uses)
        res.reds += [Red("%s: cannot read this finding (%s) -- its id is unknown, so (а) placement did not see it; expected a "
                         "UTF-8 text file; save it as UTF-8 or delete it" % (f.path, f.unreadable), (f.path, CARDS_AND_FINDINGS))
                     for f in pile.findings if f.unreadable]
        for v in pile.views():
            res.reds += _view_reds(tree, v)
    res.reds += _leftover_write_reds(ctx, res.notes)
    res.ok = "%d piles, %d batches" % (len(tree.piles), len(tree.all_views()))
    return res


# ---------------------------------------------------------------- (е) findings: every finding is in a batch (D-0044)

FINDINGS_FROM = datetime.date(2026, 10, 13)       # the day of D-0044: a finding dated from here on is RED when orphaned
FINDINGS_WARN_NAMES = 5                           # the baseline line names this many orphans older than that
FINDING_MOVE_RE = re.compile(r"^[ \t]*перенос:[ \t]*`?([a-z0-9][a-z0-9-]*)(?=[/`]|[ \t]*$)", re.M)
FINDINGS_TRIGGER_RE = re.compile(r"^plans/piles/[^/_.][^/]*/(?:findings/.+|batch-[^/]+\.md)$")
BATCH_FILE_RE = re.compile(r"^plans/piles/([^/_.][^/]*)/batch-[^/]+\.md$")


def _batch_prose(text: str, path: str = "this batch file",
                 hidden: str = "a finding named below it would read as «not placed»") -> str:
    """The text of a batch file (or of a finding) where a name or a `перенос:` line may be READ: no fenced block, no `<!-- … -->`
    comment (the template's «Остатки» comment shows the form with placeholders, a fence shows an example -- neither places
    anything). Comment and fence are read in one walk, the first opener wins (`md_table._blank_comments`). A `<!--` that never
    closes hides the rest of the file, as an HTML reader would show it: the unsafe direction of a detector is a false "placed".
    A fence that never closes is the opposite, a false "not placed", and is CannotRun naming `<path>:<line>` (`path`: the
    repo-relative path the caller read the text from; `hidden`: what the fence would hide, for the message)."""
    lines = text.split("\n")
    blanked, unclosed = _blank_comments(lines)
    if unclosed is not None:
        blanked = blanked[:unclosed] + [blanked[unclosed].split("<!--", 1)[0]]
    error = _unclosed_fence_error(path, blanked, hidden)
    if error:
        raise error
    return "\n".join(line for _, line in md_lines_outside_fences(blanked))


ROW_SECTIONS = ("узлы", "остатки", "живые доказательства")      # the sections of a batch file whose rows PLACE a finding
HEADING_RE = re.compile(r"^#{1,2}\s+(.*)")
LEFTOVER_KEY_RE = re.compile(r"(?:^|\|)[\s\-*•+]*(?:перенос|сделано|узел):", re.I)   # the key of a «Остатки» item (`узел:` since F6-30): first, or a `| `-segment of its own


def _batch_rows(prose: str) -> str:
    """The rows of a batch file's prose (`_batch_prose`: no fence, no comment) where a finding may be PLACED (D-0044: «строка (узел
    или указатель `перенос:`)», not the prose of «Ход»): a line that starts with `|` -- after any indentation, so an indented
    ` | … |` row of the F5-5 leftover is a row -- under «Узлы», «Остатки» or «Живые доказательства», and a line under «Остатки»
    whose `перенос:` or `сделано:` is a key (first on the line or a `| `-segment, the close form of an «Остатки» item: those are
    list items, not table rows; the word inside a sentence is not a key). `сделано:` is for a finding whose work was done INSIDE a
    taken batch: its node table is frozen (в), «Остатки» is the one list such a batch may still write. A paragraph outside those
    sections, the batch header and «Ход» are not rows; a file with no such section has no rows."""
    rows, section = [], None
    for line in prose.split("\n"):
        head = HEADING_RE.match(line)
        if head:
            section = next((s for s in ROW_SECTIONS if head.group(1).strip().lower().startswith(s)), None)
        elif section and (line.lstrip().startswith("|") or (section == "остатки" and LEFTOVER_KEY_RE.search(line))):
            rows.append(line)
    return "\n".join(rows)


@dataclasses.dataclass(frozen=True)
class BatchText:
    prose: str       # the file outside fences and comments: what a finding dated before FINDINGS_FROM may be named in (baseline)
    rows: str        # its placement rows (`_batch_rows`): what a finding dated FINDINGS_FROM or later must be named in


def _name_re(name: str):
    """A finding's file name as a whole token: `findings/` before it and backticks around it are fine, a longer name is not."""
    return re.compile(r"(?<![\w.-])" + re.escape(name) + r"(?![\w-])")


def _finding_moves(f: Finding) -> list:
    """The piles a finding's own `перенос: <slug>/…` lines name (outside fenced blocks and `<!-- -->` comments, the text `_batch_prose` reads); [] when it has none."""
    prose = _batch_prose(f.text, f.path, "a «перенос:» line after it would not be read and the finding would read as an orphan")
    return list(dict.fromkeys(FINDING_MOVE_RE.findall(prose)))


def pile_prose(tree: Tree) -> dict:
    """{pile slug: [BatchText of each of its batch files]} -- what a finding may be named in (see `_batch_prose`, `_batch_rows`)."""
    out = {}
    for slug, p in tree.piles.items():
        texts = [_batch_prose(read_text(tree.root / b.path), b.path) for b in p.batches]
        out[slug] = [BatchText(t, _batch_rows(t)) for t in texts]
    return out


def _rows_only(f: Finding) -> bool:
    """A finding dated FINDINGS_FROM or later is placed by a ROW only; an older or undated one is the file-level baseline."""
    return f.date is not None and f.date >= FINDINGS_FROM


def _named_in(f: Finding, text: str) -> bool:
    """The finding's file name as a whole token, or its header id as a whole B-id token (`WHAT_ID_RE`: B-30 is not B-308), in `text`."""
    return bool(_name_re(f.name).search(text) or (f.id and f.id in WHAT_ID_RE.findall(text)))


def _reads(f: Finding, bt: BatchText) -> str:
    return bt.rows if _rows_only(f) else bt.prose


def finding_placed(f: Finding, slug: str, prose: dict) -> bool:
    """THE predicate «this finding is in a batch» -- (е) and the board's «Входящие» both call it (one reader of where a finding is
    named). Placed = `_named_in` the rows (a finding dated FINDINGS_FROM or later) or the prose (an older one) of a batch file of
    its own pile or of a pile its own `перенос: <slug>/…` line names. A name or id only inside a fence or a comment places nothing;
    for a dated finding the prose of «Ход» places nothing either."""
    found = [h for h in [slug] + _finding_moves(f) if h in prose]
    return any(_named_in(f, _reads(f, bt)) for h in found for bt in prose[h])


def _orphan_why(f: Finding, slug: str, prose: dict):
    """None when the finding is placed, else the sentence that says why not. `prose`: {pile: [BatchText]}."""
    if finding_placed(f, slug, prose):
        return None
    moves = _finding_moves(f)
    elsewhere = sorted(s for s, texts in prose.items() if s != slug and any(_named_in(f, _reads(f, bt)) for bt in texts))
    gone = [m for m in moves if m not in prose]
    if gone:
        return ('its «перенос:» line names the pile "%s", which does not exist -- name an existing pile of plans/piles/'
                % ", ".join(gone))
    if moves:
        return ("its «перенос: %s/…» line is not backed: no batch file of %s names it -- add its row to a batch file of %s "
                "(an untaken «ожидает» batch counts)" % (moves[0], moves[0], moves[0]))
    if _rows_only(f):
        in_prose = any(_named_in(f, bt.prose) for bt in prose.get(slug, ()))
        why = "no ROW of a batch file of its pile %s names it" % slug
        if in_prose:
            why += (" (a batch file names it in prose, e.g. «Ход», which is not a row: D-0044 wants a node row of «Узлы», a row of "
                    "«Остатки» / «Живые доказательства», or a «перенос:» line of «Остатки»)")
    else:
        why = "no batch file of its pile %s names it" % slug
    if elsewhere:
        why += (" (a batch file of %s names it, but a finding stays an orphan of its own pile unless it carries the line "
                "«перенос: %s/…»)" % (", ".join(elsewhere), elsewhere[0]))
    return why + (" -- add a row for it to an untaken («ожидает») batch file of %s (none untaken: write batch-<N+1>-… "
                  "and its row in the card), or write «перенос: <other-slug>/…» in the finding and name it there" % slug)


def _staged_batches(ctx: Ctx, homes) -> tuple:
    """The staged paths that are batch files of the piles `homes` -- the DELETED ones too: `staged_paths` lists a `git rm`
    (`git diff --cached --name-only`), the post-deletion tree no longer holds the file, so it is not among the tree's batch
    paths and must be added by name. Empty under `--all` (every red blocks there)."""
    if ctx.staged is None:
        return ()
    return tuple(sorted(p for p in ctx.staged if (m := BATCH_FILE_RE.match(p)) and m.group(1) in homes))


def check_findings(ctx: Ctx) -> ItemResult:
    """(е): every readable finding file is named in a batch file of its own pile, or carries «перенос: <other-slug>/…» and is
    named in a batch file of THAT pile (D-0044, PROJECT.md «Командная работа» п. 2). A finding dated FINDINGS_FROM or later is RED
    when orphaned; an older one (or one with no date: it cannot be scoped) is the baseline -- ONE WARN line with the count and the
    first names. An unreadable finding is (д)'s one red, not (е)'s. Carriers of a red: the finding and the batch files of the
    piles it may be placed in AND the batch files of those piles that this commit stages as deleted (a `git rm` of the only batch
    that named a finding must carry the red it causes, not print it as «carried»). "Named" is a ROW for a finding dated
    FINDINGS_FROM or later (`finding_placed`), prose for an older one."""
    tree, res = ctx.tree, ItemResult()
    prose = pile_prose(tree)
    n_all = n_red = n_undated = 0
    baseline = []
    for slug, pile in sorted(tree.piles.items()):
        for f in pile.findings:
            if f.unreadable:
                continue
            n_all += 1
            why = _orphan_why(f, slug, prose)
            if why is None:
                continue
            if _rows_only(f):
                n_red += 1
                homes = {slug} | {m for m in _finding_moves(f) if m in tree.piles}
                res.reds.append(Red("%s: pile %s, finding dated %s: %s" % (f.path, slug, f.date.isoformat(), why),
                                    (f.path,) + tuple(b.path for h in sorted(homes) for b in tree.piles[h].batches)
                                    + _staged_batches(ctx, homes)))
            else:
                baseline.append("%s/%s" % (slug, f.name))
                n_undated += f.date is None
    if baseline:
        res.notes.append("WARN: %d finding(s) dated before %s%s are named in no batch file of their pile (the baseline the calibration "
                         "reads; not blocking), first %d: %s" % (
                             len(baseline), FINDINGS_FROM.isoformat(), " or undated (%d)" % n_undated if n_undated else "",
                             min(FINDINGS_WARN_NAMES, len(baseline)), ", ".join(baseline[:FINDINGS_WARN_NAMES])))
    res.ok = "%d findings read, %d dated from %s on are orphans, %d older are the baseline" % (
        n_all, n_red, FINDINGS_FROM.isoformat(), len(baseline))
    return res


# (letter, key, function, scope): scope "tree" -- red blocks only a commit that carries it (P6); "files" -- judged
# only for the staged files; "backlog" -- runs when plans/BACKLOG.md is staged; "findings" -- runs when a finding or a batch
# file is staged, and a red blocks like a "tree" one (a commit that carries none of its files only sees it as "carried").
CHECKS = (("а", "placement", check_placement, "tree"), ("б", "overlap", check_overlap, "tree"),
          ("в", "frozen", check_frozen, "files"), ("г", "backlog", check_backlog, "backlog"),
          ("д", "form", check_form, "files"), ("е", "findings", check_findings, "findings"))


def _relevant(staged) -> bool:
    return any(p.startswith(PILES_REL + "/") or p == BACKLOG_REL for p in staged)


def _split_reds(ctx: Ctx, res: ItemResult, scope: str):
    if scope in ("tree", "findings"):
        mine =[r for r in res.reds if ctx.touches(r.carriers)]
        return mine, [r for r in res.reds if r not in mine]
    return [r for r in res.reds if ctx.touches(r.carriers)], []


def _item_lines(letter, key, res: ItemResult, mine, carried, door):
    tag = "(%s) %s:" % (letter, key)
    lines = []
    for r in mine:
        lines.append("%s RED -- %s" % (tag, r.msg))
    if mine and door:
        lines.append("%s RED, passed by the commit message: %s" % (tag, door[2]))
    lines += ["%s carried from earlier commits (not blocking): %s" % (tag, r.msg) for r in carried]
    if res.not_checked:
        lines.append("(%s) NOT CHECKED %s -- %s" % (letter, key, res.not_checked))
    elif not mine and not carried:
        lines.append("%s ok (%s)" % (tag, res.ok))
    lines += ["%s %s" % (tag, n) for n in res.notes]
    return lines


def run_check(root, all_=False, msg_text="", base="HEAD", frozen_ref=None):
    """-> (exit code, output lines). All the judgement lives here; cmd_check only reads the arguments.
    `base` is the rev (г) compares plans/BACKLOG.md with; `frozen_ref` the rev (в) compares the taken batches with
    (None -> origin/main). `--base <rev>` sets both: CI has no origin/main behind the pushed commit, it has the pushed range."""
    staged = None if all_ else set(staged_paths(root))
    if staged is not None and not _relevant(staged):
        return 0, ["piles check: no plans/piles or BACKLOG path staged -- nothing to check"]
    tree = load_tree(root, tolerant=True)
    ctx = Ctx(tree, Path(root), staged, base, frozen_ref or ORIGIN)
    doors, notes = [], []
    for msg in ([msg_text] if isinstance(msg_text, str) else msg_text):     # one scan per message: a broken fence in one never closes another's door
        if msg:
            found, more = door_lines(msg)
            doors += found
            notes += more
    lines, red_items = [], []
    for letter, key, fn, scope in CHECKS:
        if scope == "backlog" and staged is not None and BACKLOG_REL not in staged:
            lines.append("(%s) %s: %s is not staged -- not checked" % (letter, key, BACKLOG_REL))
            continue
        if scope == "findings" and staged is not None and not any(FINDINGS_TRIGGER_RE.match(p) for p in staged):
            lines.append("(%s) %s: no finding or batch file staged -- not checked" % (letter, key))
            continue
        res = fn(ctx)
        mine, carried = _split_reds(ctx, res, scope)
        door = next((d for d in doors if letter in d[0]), None)
        lines += _item_lines(letter, key, res, mine, carried, door)
        if mine and not door:
            red_items.append(letter)
    lines += notes
    if red_items:
        lines.append("piles check: refused -- red: %s. Fix what is named above, or -- when the commit is deliberate -- %s"
                     % (", ".join("(%s)" % i for i in red_items), DOOR_HELP))
        if is_merging(root):
            lines.append("piles check: a merge is in progress -- add the piles-skip line to the merge message, then run `git commit` again")
        return 2, lines
    lines.append("piles check: ok")
    return 0, lines


def range_messages(root, rev):
    """-> (messages, line). The commit messages of `rev..HEAD` and ONE printed line saying what was found. `--base` judges
    what a push changed, so a door written in the commits of that push (t-604, finding F-1 of t-603) is read from the same
    range: CI has no commit message file. Fail-closed: an empty range or an unreadable log gives NO door, never a crash."""
    rc, out = gitcmd.git(root, "log", "--format=%B%x00", "%s..HEAD" % rev)
    if rc != 0:
        return [], ("piles check: WARN: cannot read the commit messages of %s..HEAD (%s) -- no piles-skip door counted from the "
                    "range" % (rev[:12], out.decode("utf-8", "replace").strip() or "git exited %d" % rc))
    msgs = [m.strip() for m in out.decode("utf-8", "replace").split("\0") if m.strip()]
    if not msgs:
        return [], "piles check: no commit in %s..HEAD (empty range) -- no piles-skip door from the range" % rev[:12]
    return msgs, "piles check: piles-skip doors are read from the %d commit message(s) of %s..HEAD" % (len(msgs), rev[:12])


def cmd_check(args, root) -> int:
    msgs = []
    if args.msg_file:
        try:
            msgs.append(Path(args.msg_file).read_bytes().decode("utf-8", "replace"))
        except OSError as exc:
            raise CannotRun("cannot read --msg-file %s: %s" % (args.msg_file, exc))
    base, frozen_ref = "HEAD", None
    if args.base:
        try:
            base = frozen_ref = resolve_base(root, args.base)
        except BaseError:
            raise CannotRun("--base %r does not resolve to a commit in %s -- pass --base <rev> naming a commit of this repository, "
                            "or no flag (then (в) compares with %s and (г) with HEAD)" % (args.base, root, ORIGIN))
        found, line = range_messages(root, base)
        msgs += found
        print(line)
    code, lines = run_check(root, args.all, msgs, base, frozen_ref)
    for line in lines:
        print(line)
    return code


# ============================================================================================
# take / close: the only code writers of a batch's status and of the Закрыто table
# ============================================================================================

class Refused(Exception):
    """A refusal of take/close (exit 2). The text says what is wrong, what was expected, how to pass; nothing was written."""


SLUG_RE = re.compile(r"[a-z0-9][a-z0-9-]*")
TAKEN_DATE_RE = re.compile(r"\s*,\s*\d{2}\.\d{2}\.\d{4}\s*$")
HASH_RE = re.compile(r"[0-9a-f]{7,40}")
URL_RE = re.compile(r"https://\S{1,292}")
WHO_MAX = 40
WORD_MAX = 120                      # --word lands in a BACKLOG cell: bounded like --who (m-3, t-593)
DEBT_REL = "ai-packages/qa-factory/design/factory-rules-debt.md"
FINDING_LABEL_RE = re.compile(r"^(Что не так(?:\s*/\s*что сделать)?|Свидетель|Принципы и правила|Решение владельца нужно)\s*:\s*(.*)$")
FINDING_KEYS = {"что": "what", "свидетель": "witness", "принципы": "principles", "решение": "owner"}
PARTIAL_NOTE_RE = re.compile(r"^Член пачки `[^`]+` частично\b")      # the line tools/piles_split.py writes for a partial member


def read_form(path):
    """(has BOM, uses CRLF) of a file as it lies on disk: a writer keeps both (E13)."""
    raw = Path(path).read_bytes()
    return raw.startswith(b"\xef\xbb\xbf"), b"\r\n" in raw


def write_like(path, text, form) -> None:
    bom, crlf = form
    write_atomic(Path(path), ("﻿" if bom else "") + (text.replace("\n", "\r\n") if crlf else text))


def replace_cells(line: str, edits: dict) -> str:
    """The table row with the cells {index: new text} replaced; the padding and every other cell stay byte for byte."""
    parts = split_pipes(line)
    if edits and max(edits) + 1 >= len(parts) - 1:
        raise Refused("the row has too few cells to write cell %d -- expected as many cells as the table header has" % (max(edits) + 1))
    for idx, new in edits.items():
        part = parts[idx + 1]                         # parts[0] is the text before the leading pipe
        blank = not part.strip()
        lead = " " if blank else part[:len(part) - len(part.lstrip())]
        parts[idx + 1] = lead + new + (" " if blank else part[len(part.rstrip()):])
    return "|".join(parts)


def edit_card(text: str, row: CardRow, values: dict) -> str:
    """The card text with the cells {key of CARD_COLS: new text} of the batch row replaced."""
    lines = text.split("\n")
    cols = column_map(table_after(lines, "Пачки")[0], CARD_COLS)
    for key in values:
        if key not in cols:
            raise Refused("the card table has no %s column -- expected the columns № / Строки / Статус / Взял / Ветка / MR" % CARD_COLS[key])
    lines[row.line - 1] = replace_cells(lines[row.line - 1], {cols[k]: v for k, v in values.items()})
    return "\n".join(lines)


def edit_header(text: str, edits: dict) -> str:
    lines = text.split("\n")
    i = next((i for i, l in enumerate(lines) if "кучка:" in l.lower()), None)
    if i is None:
        raise Refused('the batch file has no header line -- expected "кучка: `<slug>` | статус: … | взял: … | ветка: … | MR: …"')
    lines[i] = replace_pairs(lines[i], edits)
    return "\n".join(lines)


def _today(args) -> str:
    raw = getattr(args, "today", None)
    try:
        day = datetime.date.fromisoformat(raw) if raw else datetime.date.today()
    except ValueError:
        raise CannotRun('usage: --today "%s": expected YYYY-MM-DD' % raw)
    return day.strftime("%d.%m.%Y")


def _parse_n(raw: str) -> int:
    if not re.fullmatch(r"[0-9]{1,3}", raw) or not 1 <= int(raw) <= 999:
        raise Refused('N must be a whole number 1-999, got "%s"' % raw)
    return int(raw)


def _text_arg_ok(text: str, limit: int) -> bool:
    """--who and --word land in table cells and in backtick-split header pairs: no '|', no backtick (it unbalances the
    cell/pair split and a re-`take` is then refused instead of idempotent -- m-2), no line break or control character."""
    return 1 <= len(text) <= limit and not any(c in "|`" or unicodedata.category(c) in ("Cc", "Zl", "Zp") for c in text)


def _find_view(tree: Tree, slug: str, n: int):
    pile = tree.piles.get(slug) if SLUG_RE.fullmatch(slug) else None
    if pile is None or pile.card is None:
        have = ", ".join(sorted(s for s, p in tree.piles.items() if p.card))
        raise Refused('no pile "%s" (no plans/piles/%s/README.md); piles with a card: %s' % (slug, slug, have or "none"))
    view = next((v for v in pile.views() if v.n == n and v.row is not None), None)
    if view is None:
        raise Refused('no batch row %d in the card %s -- expected a row with № %d in its "## Пачки" table' % (n, pile.card_rel, n))
    return pile, view


def _batch_file(view: View, where: str, what: str) -> BatchFile:
    slug = where.split("/")[0]
    if view.file is None:
        raise Refused("no batch file for %s -- expected plans/piles/%s/batch-%d-<name>.md written from plans/piles/_template/batch.md; %s"
                      % (where, slug, view.n, what))
    if len(view.files) > 1:
        raise Refused("%s has %d batch files (%s) -- one file per batch number; merge them, then run it again"
                      % (where, len(view.files), ", ".join(f.path for f in view.files)))
    return view.file


def _current_branch(root):
    rc, out = git(root, "rev-parse", "--abbrev-ref", "HEAD")
    return out.decode("utf-8", "replace").strip() if rc == 0 and out.strip() else None


def rebuild_board(root) -> tuple:
    text, counts = render_board(load_tree(root))
    write_atomic(Path(root) / BOARD_REL, text)
    return counts


def printable(text: str) -> str:
    """Text with every non-printable character replaced by '?': the sanitizer for lines this tool prints or collects.
    Its sibling is ci_read_common.sanitize_own (the same rule for CI output); the two are kept alike on purpose."""
    return "".join(ch if ch.isprintable() else "?" for ch in text)


def _overlap_refusal(tree: Tree, f: BatchFile, key, root) -> None:
    """take runs (б) for the batch it takes against every active batch first, and names the queue door (P5); the function-list
    door (D-0048) is judged the same way as in `check`."""
    for v in tree.all_views():
        if v.file is not None and v.status in ACTIVE and (v.slug, v.n) != key:
            (b1, k1), (b2, k2) = sorted([(f, key), (v.file, (v.slug, v.n))], key=lambda t: (t[1][1], t[1][0]))
            msgs = _pair_overlap(b1, b2, k1, k2, root)
            if msgs:
                raise Refused("%s; the queue line is an append that (в) allows in a taken batch -- then run take again" % "; ".join(msgs))


def cmd_take(args, root) -> int:
    root = Path(root)
    who = args.who.strip()
    if not _text_arg_ok(who, WHO_MAX):
        raise Refused('--who: expected 1-%d characters without "|", a backtick (`) or a line break, got %r' % (WHO_MAX, args.who))
    n = _parse_n(args.n)
    tree = load_tree(root)
    slug = args.slug
    pile, view = _find_view(tree, slug, n)
    where, branch = "%s/%d" % (slug, n), "pile/%s/batch-%d" % (slug, n)
    f = _batch_file(view, where, "write it (the integrator fixes the batch's content at take), then run take again")
    if not f.nodes:
        raise Refused("%s has no nodes -- a batch is taken with its node table (## Узлы) filled" % where)
    if f.status != "ожидает":
        taker = TAKEN_DATE_RE.sub("", f.who).strip()
        if taker == who and first_tick(f.branch) == branch:
            print("piles take: %s is already taken by %s; nothing changed" % (where, who))
            return 0
        raise Refused('batch %s is already taken by %s (status "%s", branch %s) -- a batch has one taker; to hand it over, the '
                      "integrator edits взял in the card row and the batch header and records it in the batch's Ход (commit with "
                      '"piles-skip: в -- handover")' % (where, f.who, f.status_raw, f.branch))
    if view.row.status != f.status:
        raise Refused('the card and the batch file disagree on %s: card status "%s", batch status "%s" -- make them say the '
                      "same thing, then take" % (where, view.row.status_raw, f.status_raw))
    _overlap_refusal(tree, f, (slug, n), root)
    today = _today(args)
    taken, ticks = "%s, %s" % (who, today), "`%s`" % branch
    card_path, batch_path = root / pile.card_rel, root / f.path
    card = edit_card(read_text(card_path), view.row, {"status": "в работе", "who": taken, "branch": ticks})
    batch = edit_header(read_text(batch_path), {"статус": "в работе", "взял": taken, "ветка": ticks})
    apply_changes(root, [(card_path, card), (batch_path, batch)], [])          # all or nothing: card, batch and the board (t-604 F-3)
    print("piles take: %s taken by %s (%s). Next:" % (where, who, today))
    print("  1. on main: git add %s %s %s; git commit -m \"piles: take %s for %s\"; git push origin main"
          % (pile.card_rel, f.path, BOARD_REL, where, who))
    print("  2. the taker: git fetch origin; git switch -c %s origin/main" % branch)
    here = _current_branch(root)
    if here != "main":
        print("piles take: WARNING: the current branch is %s, not main -- the claim is visible to others only once it reaches main"
              % (here or "unknown (git failed)"))
    return 0


def check_hash(root, h) -> None:
    """A commit hash as the table of contents wants it: 7-40 hex characters that name a commit HERE (P2)."""
    if not HASH_RE.fullmatch(h):
        raise Refused('--hash "%s": expected a commit hash (7-40 hex characters)' % h)
    if git(root, "rev-parse", "--git-dir")[0] != 0:
        raise CannotRun("cannot verify %s (git cannot run in %s) -- run where git works" % (h, root))
    if git(root, "cat-file", "-e", h + "^{commit}")[0] != 0:
        raise Refused("%s is not a commit in this repository -- fetch first or check the hash" % h)


def check_url(u) -> None:
    if not URL_RE.fullmatch(u):
        raise Refused('--url "%s": expected an https:// MR address (at most 300 characters, no spaces)' % u)


def _cell_escape(s: str) -> str:
    return re.sub(r"(?<!\\)\|", r"\\|", s)


def finding_fields(text: str, title: str) -> dict:
    """The five Закрыто columns of a finding (P-form of the spec, 4.5): paragraphs joined by a space, '|' escaped."""
    parts, cur = {}, None
    for line in re.sub(r"<!--.*?-->", "", text, flags=re.S).split("\n"):
        m = FINDING_LABEL_RE.match(line)
        if m:
            cur = FINDING_KEYS[m.group(1).split()[0].lower()]
            parts.setdefault(cur, []).append(m.group(2))
        elif PARTIAL_NOTE_RE.match(line):
            cur = None                                  # m-10: split's own note is not a continuation of the cell above it
        elif cur and line.strip():
            parts[cur].append(line.strip())
    head = next((header_pairs(l) for l in text.split("\n")[:8] if l.lower().startswith("id:")), {})
    got = {k: " ".join(x.strip() for x in v if x.strip()) or "—" for k, v in parts.items()}
    what = got.get("what", "—")
    t = title.strip().rstrip(".:").strip()
    fields = {"what": "**%s.** %s" % (t, what) if t else what, "witness": got.get("witness", "—"),
              "source": head.get("от") or "—", "principles": got.get("principles", "—")}
    return {k: _cell_escape(v) for k, v in fields.items()}


def closing_items(tree: Tree, ids, where="") -> list:
    """[(id, finding files, open BACKLOG row)] for ids that still have text; Refused for an id with none at all."""
    finds, items = tree.findings_by_id(), []
    for ident in ids:
        fl, row = finds.get(ident, []), tree.backlog.first(ident, False)
        if not fl and row is None:
            raise Refused("%s%s has no text anywhere (not open in %s, no finding file) -- nothing was written; fix the card row "
                          "or write its finding" % (ident, " named in " + where if where else "", BACKLOG_REL))
        items.append((ident, fl, row))
    return items


def backlog_with_closed(root: Path, items, suffix: str) -> str:
    """BACKLOG text with the archive rows of `items` removed and their five-column closed rows appended to the Закрыто
    table, after its last '| B-' row. The text of a closed row comes from the finding when there is one."""
    lines = read_text(root / BACKLOG_REL).split("\n")
    drop = {row.line for _, _, row in items if row}
    new_rows = []
    for ident, fl, row in items:
        fields = finding_fields(fl[0].text, fl[0].title) if fl else row.fields
        new_rows.append("| %s | %s | %s | %s%s | %s |" % (ident, fields["what"], fields["witness"], fields["source"], suffix,
                                                          fields["principles"]))
    kept = [l for i, l in enumerate(lines, 1) if i not in drop]
    boundary = next(i for i, l in enumerate(kept) if l.rstrip() == "## Закрыто")
    last = max((i for i in range(boundary + 1, len(kept)) if kept[i].startswith("| B-")), default=None)
    if last is None:
        sep = next((i for i in range(boundary + 1, len(kept)) if kept[i].startswith("|---")), None)
        if sep is None:
            kept[boundary + 1:boundary + 1] = ["", "| id | что сделать | почему | источник | принципы |", "|---|---|---|---|---|"]
            sep = boundary + 3
        last = sep
    kept[last + 1:last + 1] = new_rows
    return "\n".join(kept)


def debt_warnings(root: Path, ids) -> list:
    """P12 / axis 4: debt entries (grep only) that cite a B-id that has just been closed."""
    path = root / DEBT_REL
    if not path.is_file():
        return []
    try:
        lines = read_text(path).split("\n")
    except CannotRun:
        return []
    out = []
    for ident in ids:
        hits = [str(i) for i, l in enumerate(lines, 1) if re.search(r"(?<![\w-])%s(?!\d)" % re.escape(ident), l)]
        if hits:
            out.append("piles close: WARNING: debt entries naming %s: %s:%s -- remove them in this commit"
                       % (ident, DEBT_REL, ", ".join(hits)))
    return out


def _split_members(view: View):
    """-> (whole members, partial members) of the card row, each id once, in row order."""
    whole, partial, seen = [], [], set()
    for m in view.row.members:
        if m.id not in seen:
            seen.add(m.id)
            (partial if m.partial else whole).append(m)
    return whole, partial


def _plan_batch_close(tree: Tree, view: View, where: str):
    """-> (closing items, ids already closed, partial members). Refuses before anything is written (m5, E26)."""
    whole, partial = _split_members(view)
    done = [m.id for m in whole if m.id in tree.backlog.closed_ids]
    finds = tree.findings_by_id()
    for m in partial:
        if m.id not in tree.backlog.closed_ids and not finds.get(m.id):
            raise Refused("%s %s is a partial member of %s and has no finding file -- closing the batch would leave its remainder "
                          "placed nowhere; write plans/piles/%s/findings/%s-<slug>.md for the remainder, then close"
                          % (m.id, m.qualifier, where, where.split("/")[0], m.id))
    return closing_items(tree, [m.id for m in whole if m.id not in done], where), done, partial


CLOSE_FORMS = ('`close <slug> <N> --hash <h> [--url <https://…>]` or '
               '`close --id B-nnn --word "<кто, дата>" [--hash <h>]`')


# ---- the carry-over gate of `close <slug> <N>`: a batch is closed by finishing, not by carrying over (08.10.2026) ----

LEFTOVER_DONE_RE = re.compile(r"[0-9a-f]{7,40}|t-\d+")
LEFTOVER_TARGET_RE = re.compile(r"findings/[^/\s]+\.md|пачка\s+\d{1,3}|[a-z0-9][a-z0-9-]*/findings/[^/\s]+\.md")
# A `подтвердил:` / `обоснование:` value that is only one of these (trimmed, lower case) is EMPTY: the gate exists for a person's
# signature and a reason. A dash with text ("— Иванов, 09.10") is not one of them. Data, not code (FR-13).
LEFTOVER_EMPTY_WORDS = ("—", "–", "-", "n/a", "none", "нет", "tbd", "?")
LEFTOVER_FORMS = ("`сделано: <7-40 hex | t-nnn>` OR all three of `перенос: <findings/<file> | пачка N | <slug>/findings/<file>>`, "
                  "`обоснование: <why>`, `подтвердил: <кто, дата>`")
LEFTOVER_DOOR = ("finish the item and write `сделано:`, or carry it and let a PERSON confirm it with `подтвердил: <кто, дата>` "
                 "(an agent never confirms its own carry-over)")


@dataclasses.dataclass(frozen=True)
class DoneCarryRule:
    """The two closed forms of an item -- `сделано: <done>` OR `перенос: <target> | обоснование: <why> | подтвердил: <кто, дата>` --
    as data: what a `сделано` value and a `перенос` value may be, and the words a refusal uses for them. ONE reader of the
    forms (leftover_problem) serves «Остатки» and «Живые доказательства»; only these two patterns differ (F5-5)."""
    done_re: "re.Pattern"
    done_words: str
    target_re: "re.Pattern"
    target_words: str


LEFTOVER_RULE = DoneCarryRule(LEFTOVER_DONE_RE, "7-40 hex characters nor t-nnn",
                              LEFTOVER_TARGET_RE, "findings/<file> | пачка N | <slug>/findings/<file>")

LEFTOVER_MARKER_RE = re.compile(r"(?:[-*+•]|\d+\.)(?:\s+|$)")        # a list marker at the start of an item / a stripped line


def _sections(text: str, prefix: str) -> list:
    """[[(line number, line)]]: the lines of every section whose heading starts with `prefix` («остатки», «живые доказательства»),
    found on RAW column-0 `## ` lines like (в)'s `_frozen_lines` (section_name) -- a fence or an inline `<!--` in an earlier
    section cannot hide the heading."""
    sections, inside = [], False
    for no, line in enumerate(text.split("\n"), 1):
        name = section_name(line)
        if name is not None:
            inside = name.startswith(prefix)
            if inside:
                sections.append([])
        elif inside:
            sections[-1].append((no, line))
    return sections


def leftover_items(text: str):
    """-> ([(line number, item text)], line number of a `<!--` that never closes | None): the items of the batch's «## Остатки»
    section. Comments go first; then EVERY non-empty line left is an item (prose, a heading, a fenced line too) -- only a
    comment hides a line -- EXCEPT a line indented by 2 or more spaces that does not start a list marker: it continues the item
    above it as one more ' | ' segment, so a wrapped bullet is one item and `  сделано: t-1` on its own line counts for its
    bullet. A sub-bullet, a tab-indented line and an indented line with no item above it are items of their own."""
    items = []
    for section in _sections(text, "остатки"):
        lines, unclosed = _blank_comments([line for _, line in section])
        if unclosed is not None:
            return [], section[unclosed][0]
        first = len(items)
        for (no, _), line in zip(section, lines):
            body = line.strip()
            if not body:
                continue
            if len(items) > first and line.startswith("  ") and not LEFTOVER_MARKER_RE.match(body):
                items[-1] = (items[-1][0], items[-1][1] + " | " + body)
            else:
                items.append((no, body))
    return items, None


def leftover_pairs(line: str) -> dict:
    """The `key: value` pairs of an item, split at ' | ' like the batch header. ONE case policy for «Остатки» and for the proof
    rows: a KEY (`сделано` `перенос` `обоснование` `подтвердил`) is read case-insensitively -- `Сделано:` is the key -- while a
    VALUE stays as written, so the closed forms judge it strictly (a hex hash and `t-nnn` in lower case). The free text may come
    first; the first occurrence of a key wins (a later segment with the same key is a note)."""
    pairs, marker = {}, LEFTOVER_MARKER_RE.match(line)
    for seg in split_pipes(line[marker.end():] if marker else line):
        if ":" in seg:
            key, val = seg.split(":", 1)
            pairs.setdefault(key.strip().strip("`").strip().lower(), unwrap_ticks(val))
    return pairs


def leftover_problem(pairs: dict, rule: DoneCarryRule = LEFTOVER_RULE):
    """Why an item may not stay in a closed batch, or None when it is finished or carried with a person's confirmation. The FORM
    only (pure): whether a carry-over target exists is leftover_target_missing's question, asked after this one passed.
    `rule` says what the two values may be: «Остатки» (the default) or a proof row (PROOF_RULE)."""
    done, carry = "сделано" in pairs, "перенос" in pairs
    if done and carry:
        return "carries both `сделано:` and `перенос:` -- one or the other"
    if done:
        return None if rule.done_re.fullmatch(pairs["сделано"]) else \
            '`сделано: %s` is neither %s' % (_shorten(pairs["сделано"], 30), rule.done_words)
    if not carry:
        return "has neither `сделано:` nor `перенос:`"
    bad = []
    if not rule.target_re.fullmatch(pairs["перенос"]):
        bad.append("`перенос: %s` is none of %s" % (_shorten(pairs["перенос"], 30), rule.target_words))
    for key in ("обоснование", "подтвердил"):
        value = pairs.get(key, "")
        if not value:
            bad.append("`%s:` is %s" % (key, "empty" if key in pairs else "missing"))
        elif value.strip().lower() in LEFTOVER_EMPTY_WORDS:
            bad.append("`%s: %s` is a placeholder, not %s" % (key, _shorten(value, 30), "a reason" if key == "обоснование" else "a person's confirmation"))
    return "; ".join(bad) or None


# ---- the write-time gate of «Остатки» (F6-30): an item is written WITH its executor, not at `close` ----

LEFTOVER_NODE_RE = re.compile(r"(?:([a-z0-9][a-z0-9-]*)/(\d{1,3})/)?([A-Za-z0-9][A-Za-z0-9._-]*)")
LEFTOVER_WRITE_FORMS = ("an item is written with its executor: сделано: <hash | t-nnn>, узел: <node id> (a node row of an untaken "
                        "batch, D-0044), or перенос: <target> | обоснование: <why> | подтвердил: <кто, дата | —>")


def _node_problem(tree: Tree, pile: Pile, value: str):
    """Why `узел: <value>` names no worked node row RIGHT NOW, or None: `<id>` is a node row of a batch file of the item's own pile,
    `<slug>/<N>/<id>` of batch N of pile <slug>; the batch is not «закрыта» and the node's «Исполнитель» is not empty. The value
    stands alone (the rule of `сделано:`): trailing text is not a node id."""
    m = LEFTOVER_NODE_RE.fullmatch(value)
    if not m:
        return "`узел: %s` is not a node id -- expected `<id>` or `<slug>/<N>/<id>` alone in its segment" % _shorten(value, 30)
    slug, n, ident = m.groups()
    if slug:
        other = tree.piles.get(slug)
        if other is None:
            return '`узел: %s` names pile "%s", which does not exist' % (_shorten(value, 30), slug)
        files, where = [b for b in other.batches if b.n == int(n)], "batch %s/%d" % (slug, int(n))
        if not files:
            return "`узел: %s` names batch %s/%d, which has no batch file" % (_shorten(value, 30), slug, int(n))
    else:
        files, where = pile.batches, "the batch files of pile %s" % pile.slug
    found = [(b, nd) for b in files for nd in b.nodes if nd.id == ident]
    if not found:
        return "`узел: %s` names no node row (looked in %s: %s)" % (ident, where, ", ".join(b.path for b in files) or "no batch file")
    live = [(b, nd) for b, nd in found if b.status != "закрыта"]
    if not live:
        return "`узел: %s` stands only in a «закрыта» batch (%s) -- name a node of a batch still open" % (ident, ", ".join(b.path for b, _ in found))
    if all(nd.executor.strip() in NO_VAL for _, nd in live):
        return "`узел: %s` has no Исполнитель in %s -- a node nobody works is no executor" % (ident, ", ".join(b.path for b, _ in live))
    return None


def _item_why(tree: Tree, pile: Pile, pairs: dict):
    """None when the item carries ONE valid executor form (item 5 of F6-30), else why none is valid. The forms are alternatives: a
    `узел:` item later closed by `сделано:` still passes. The `перенос:` form accepts a placeholder `подтвердил:` (a person
    confirms later; `close` still demands a real one -- the unchanged close gate)."""
    reasons = []
    if "сделано" in pairs:
        if LEFTOVER_DONE_RE.fullmatch(pairs["сделано"]):
            return None
        reasons.append("`сделано: %s` is neither 7-40 hex characters nor t-nnn" % _shorten(pairs["сделано"], 30))
    if "узел" in pairs:
        why = _node_problem(tree, pile, pairs["узел"])
        if why is None:
            return None
        reasons.append(why)
    if "перенос" in pairs:
        bad = []
        if not LEFTOVER_TARGET_RE.fullmatch(pairs["перенос"]):
            bad.append("`перенос: %s` is none of %s" % (_shorten(pairs["перенос"], 30), LEFTOVER_RULE.target_words))
        reason = pairs.get("обоснование", "")
        if not reason or reason.strip().lower() in LEFTOVER_EMPTY_WORDS:
            bad.append("`обоснование:` is %s" % ("a placeholder, not a reason" if reason else "empty or missing"))
        if "подтвердил" not in pairs:
            bad.append("`подтвердил:` is missing (a placeholder `—` is accepted until a person confirms)")
        if not bad:
            return None
        reasons.append("; ".join(bad))
    return "; ".join(reasons) or "has none of `сделано:`, `узел:`, `перенос:`"


def _leftover_write_reds(ctx: Ctx, notes=None) -> list:
    """(д), F6-30: the «Остатки» items of every batch file that is not «закрыта», that are NEW or CHANGED against the same file at
    `ctx.base` (staged: HEAD; `--base REV`: REV; `--all`: HEAD), carry an executor form (`_item_why`). An item is old when its
    stripped text equals one of the base file's items, matched as a MULTISET (one old copy does not legalize a second new one);
    a file absent at the base (the rev readable) has only new items. A base that cannot be read (a missing rev, a git failure)
    makes EVERY item new and puts one note in `notes`: an unreadable base never makes a bare item old (FR-59). A closed batch is
    never judged here (its `close` already did)."""
    tree, reds, base_ok = ctx.tree, [], None
    for pile in sorted(tree.piles.values(), key=lambda p: p.slug):
        for b in pile.batches:
            if b.status == "закрыта":
                continue
            items, _ = leftover_items(read_text(tree.root / b.path))
            if not items:
                continue
            if base_ok is None:
                base_ok = git(ctx.root, "rev-parse", "--verify", "-q", ctx.base + "^{commit}")[0] == 0
                if not base_ok and notes is not None:
                    notes.append("WARN: the base %s cannot be read here, so every «Остатки» item of every batch file is judged as new -- "
                                 "run inside the repository, or pass --base <rev> naming a commit of it" % ctx.base)
            old = {}
            base_text = git_show(ctx.root, ctx.base, b.path) if base_ok else None
            for _, it in (leftover_items(base_text)[0] if base_text else []):
                old[it] = old.get(it, 0) + 1
            for no, item in items:
                if old.get(item, 0) > 0:
                    old[item] -= 1
                    continue
                why = _item_why(tree, pile, leftover_pairs(item))
                if why:
                    reds.append(Red('%s: «Остатки» line %d "%s": %s -- %s' % (b.path, no, _shorten(item, 80), why, LEFTOVER_WRITE_FORMS),
                                    (b.path,)))
    return reds


def leftovers_unowned(tree: Tree) -> list:
    """[(batch path, line number, item)]: the «Остатки» items of every batch file that is not «закрыта» that carry no valid executor
    form (`_item_why`) -- no base diff, every item counts (the board's count line and the compact snapshot read it)."""
    out = []
    for pile in sorted(tree.piles.values(), key=lambda p: p.slug):
        for b in pile.batches:
            if b.status == "закрыта":
                continue
            out += [(b.path, no, item) for no, item in leftover_items(read_text(tree.root / b.path))[0]
                    if _item_why(tree, pile, leftover_pairs(item))]
    return out


def piles_index(root) -> set:
    """The paths under plans/piles that the index holds (ONE call): a carry-over target must be staged, or the commit of the
    close would point at a file it does not contain. CannotRun when git cannot list them -- never a guess (FR-59)."""
    rc, out = git(root, "ls-files", "-z", "--cached", "--", PILES_REL)
    if rc != 0:
        raise CannotRun("cannot list the index to verify the carry-over targets (%s) -- run close inside the repository; nothing "
                        "was written" % (out.decode("utf-8", "replace").strip() or "git exited %d" % rc))
    return {p for p in out.decode("utf-8", "replace").split("\0") if p}


def _leftover_target(value: str, own_slug: str):
    """A target that passed LEFTOVER_TARGET_RE -> ("batch", N) | ("file", slug, file name). `findings/<f>` is the own pile's."""
    m = re.fullmatch(r"пачка\s+(\d{1,3})", value)
    if m:
        return "batch", int(m.group(1))
    parts = value.split("/")
    return ("file", own_slug, parts[1]) if len(parts) == 2 else ("file", parts[0], parts[2])


def closing_finding_paths(tree: Tree, view: View) -> dict:
    """{path: id} of the finding files closing this batch deletes: those of its whole members that are not closed yet -- the
    files `_plan_batch_close` hands to apply_changes. Computed on its own so that the gate stays ahead of the plan."""
    finds, whole = tree.findings_by_id(), _split_members(view)[0]
    return {f.path: m.id for m in whole if m.id not in tree.backlog.closed_ids for f in finds.get(m.id, [])}


def leftover_target_missing(value: str, *, root, pile: Pile, view: View, deleted: dict, index):
    """Why a carry-over target (a value that passed the FORM check) names nothing a close may point at, or None. `пачка N` must
    be a card row of this pile, not this batch, not закрыта; a file must be on disk (case-exact) AND in the index (`index`: the
    set of piles_index, None when no file target was seen), and must not be a finding this very close deletes."""
    target = _leftover_target(value, view.slug)
    if target[0] == "batch":
        n = target[1]
        row = next((v for v in pile.views() if v.n == n and v.row is not None), None) if n >= 1 else None
        if row is None:
            return "has no row %d in %s" % (n, pile.card_rel)
        if n == view.n:
            return "names this very batch"
        return ("names batch %d, which is закрыта -- carry to a batch still open" % n) if row.status == "закрыта" else None
    slug, name = target[1:]
    path = "%s/%s/findings/%s" % (PILES_REL, slug, name)
    if not (Path(root) / PILES_REL / slug).is_dir():
        return 'names pile "%s", which has no %s/%s/' % (slug, PILES_REL, slug)
    if path in deleted:
        return "names a finding this close deletes (%s is a whole member of %s/%d) -- carry elsewhere" % (deleted[path], view.slug, view.n)
    try:
        on_disk = name in os.listdir(Path(root) / PILES_REL / slug / "findings")
    except OSError:
        on_disk = False
    if not on_disk:
        return "names %s, which is not in the working tree" % path
    if path not in index:
        return ("names %s, which exists but is not staged -- `git add %s` so it lands in the commit of this close, then run close "
                "again" % (path, path))
    return None


def check_leftovers(text: str, rel: str, *, root=None, pile=None, view=None, deleted=None) -> None:
    """Refused (before anything is written) while an item of «Остатки» is neither finished nor carried with a person's
    confirmation (leftover_items: every non-empty line outside a comment). No «Остатки» section, or an empty one, passes. The
    gate cannot know who typed `подтвердил:`: it checks that the pair is there and neither empty nor a placeholder word
    (LEFTOVER_EMPTY_WORDS); the rule text says a person. With `root`, `pile`, `view` (and `deleted`: closing_finding_paths) a
    carry-over target that passed the form check must also EXIST (leftover_target_missing); without them only the form is judged."""
    items, unclosed = leftover_items(text)
    if unclosed is not None:
        raise Refused('%s: «Остатки» line %d: "<!--" opens a comment that never closes -- the gate cannot tell items from comment '
                      'text; close it with "-->", then run close again. Nothing was written' % (rel, unclosed))
    found, targets = [], []
    for no, item in items:
        pairs = leftover_pairs(item)
        why = leftover_problem(pairs)
        if why is None and root is not None and "перенос" in pairs:
            targets.append((no, item, pairs["перенос"]))
        elif why:
            if "узел" in pairs and "сделано" not in pairs and "перенос" not in pairs:
                why += " -- a «узел:» item is closed by «сделано: <hash | t-nnn>» when the node merges, or carried"
            found.append((no, item, why))
    if targets:
        index = piles_index(root) if any(_leftover_target(v, view.slug)[0] == "file" for _, _, v in targets) else None
        for no, item, value in targets:
            why = leftover_target_missing(value, root=root, pile=pile, view=view, deleted=deleted or {}, index=index)
            if why:
                found.append((no, item, "`перенос: %s` %s" % (_shorten(value, 30), why)))
    if found:
        lines = ['line %d "%s": %s' % (no, _shorten(item, 80), why) for no, item, why in sorted(found, key=lambda t: t[0])]
        raise Refused("%s: «Остатки» is not finished -- %s. Expected on every item of «## Остатки» (a non-empty line outside a "
                      "comment; a line indented by 2+ spaces continues the item above it; keys in any case, values as written, `key: value` "
                      "pairs separated by ' | ', free text first): %s. Door: %s; then run close again. Nothing was written"
                      % (rel, "; ".join(lines[:5]) + ("; and %d more" % (len(lines) - 5) if len(lines) > 5 else ""),
                         LEFTOVER_FORMS, LEFTOVER_DOOR))


# ---- the proofs gate of `close <slug> <N>`: «## Живые доказательства» is done or carried, never waiting (F5-5, FR-33) ----

PROOF_SECTION = "живые доказательства"
# `сделано:` of a proof row: a commit (7-40 hex), a task (t-nnn) or a log / notebook path (a `/` and a file extension; a bare
# "да/нет" is not one). A `перенос:` target is free text -- where the proof goes is for the person who confirms it to judge.
PROOF_DONE_RE = re.compile(r"[0-9a-f]{7,40}|t-\d+|(?:[\w.-]+/)+[\w-]+(?:\.[\w-]+)+(?:[#:][\w.-]+)?")
PROOF_TARGET_RE = re.compile(r"(?!(?:%s)$)\S.*" % "|".join(re.escape(w) for w in LEFTOVER_EMPTY_WORDS))
PROOF_RULE = DoneCarryRule(PROOF_DONE_RE, "7-40 hex characters nor t-nnn nor a log/notebook path (dir/file.ext)",
                           PROOF_TARGET_RE, "a place (text that is not empty or a placeholder word)")
PROOF_FORMS = ("`сделано: <7-40 hex | t-nnn | path/to/log-or-notebook.ext>` OR all three of `перенос: <where>`, "
               "`обоснование: <why>`, `подтвердил: <кто, дата>` (keys in any case, values as written: hex and t-nnn in lower case; "
               "inside a table cell write ` \\| ` between the pairs). The value stands ALONE in its segment -- a note after it "
               "goes in its own ` \\| ` segment: `сделано: abc1234 \\| note: see the log` is accepted, `сделано: abc1234 (see the "
               "log)` is not (the first `сделано:` is the value, every later segment is a note)")
# The two refusals about the SHAPE of the section (not about a row) cannot be cured by a «Статус» cell, and (в) freezes the rest of a
# taken batch's proof table: the door is named in the refusal (FR-2, P15).
PROOF_SHAPE_DOOR = ("a table with only its header row means no proofs are owed; editing a taken batch's proof table (header, "
                    "rows, a new table) is a change of frozen text for (в), so the commit that does it needs the line "
                    "`piles-skip: в -- <reason>` in its message")


def proof_promised(text: str) -> bool:
    """The batch's own text above its first `## ` heading (the readiness rule) names «живые доказательства» -- comments aside."""
    head = re.sub(r"<!--.*?-->", "", re.split(r"(?m)^## ", text, maxsplit=1)[0], flags=re.S)
    return PROOF_SECTION in head.lower()


def _proof_row_problem(cell: str):
    """Why a «Статус» cell is not a closed form, or None. The cell is read as an «Остатки» item is, by the SAME reader and the
    same case policy (leftover_pairs): ` | ` pairs (a table cell escapes the pipe as `\\|`), a cell that is one backtick span
    unwrapped, the keys case-free and the values strict -- `Сделано: abc1234` passes, `сделано: ABC1234` does not."""
    return leftover_problem(leftover_pairs(unwrap_ticks(cell).replace("\\|", "|")), PROOF_RULE)


def proof_problems(text: str) -> list:
    """[str]: every reason the batch's «## Живые доказательства» forbids a close, one per row; [] when it may close. EVERY table
    of EVERY such section counts; the tables are read by walk_table, the walker (в)'s `_frozen_lines` and table_after use (a run
    of `|` lines at column 0 -- a blank, a comment-only or an indented line ends it, so the row after one reads as a new header
    and is refused as "no «Статус» column"; an indented `|` line is no row for either reader). A comment hides what it covers.
    FORM only (pure). No section, or a header-only table, passes -- unless the batch's text promises live proofs and holds no
    table at all."""
    found, tables = [], 0
    for section in _sections(text, PROOF_SECTION):
        lines, unclosed = _blank_comments([line for _, line in section])
        if unclosed is not None:
            return ['line %d: "<!--" opens a comment that never closes -- the gate cannot tell rows from comment text; close it '
                    'with "-->" (%s)' % (section[unclosed][0], PROOF_SHAPE_DOOR)]
        cols = {}
        for (no, _), (kind, cells) in zip(section, walk_table(lines)):
            if kind == "header":
                tables += 1
                cols = column_map(cells, {"what": "что", "status": "статус"})
                if "status" not in cols:
                    found.append('line %d: the table has no «Статус» column (header: %s) -- a table ends at the first line that '
                                 'does not start with `|` at column 0 (a blank or a comment line too), so the first row after '
                                 'one reads as a new header; keep the rows in ONE run of `|` lines under a header that has '
                                 '«Статус»; %s' % (no, _shorten(" | ".join(cells), 60), PROOF_SHAPE_DOOR))
            elif kind == "row" and "status" in cols:
                cell = _cell(cells, cols["status"])
                why = _proof_row_problem(cell)
                if why:
                    found.append('line %d "%s" (status: "%s"): %s' % (no, _shorten(_cell(cells, cols.get("what", 0)) or "(no «Что» text)", 80),
                                                                      _shorten(cell, 60), why))
    if not tables and proof_promised(text):
        found.append("the batch promises live proofs (its readiness rule names «живые доказательства») and has no table in "
                     "«## Живые доказательства» -- add the table; %s" % PROOF_SHAPE_DOOR)
    return found


def check_proofs(text: str, rel: str) -> None:
    """Refused (before anything is written) while a row of «## Живые доказательства» is not finished or carried with a person's
    confirmation -- proof_problems. The forms are read by the «Остатки» reader (leftover_problem, one case policy: keys case-free,
    values strict); the `сделано` value also allows a log / notebook path and the `перенос` target is any place (PROOF_RULE).
    The wording of the door is the «Остатки» one."""
    found = proof_problems(text)
    if found:
        raise Refused("%s: «Живые доказательства» are not finished -- %s. Expected in the «Статус» cell of every row of every "
                      "table in «## Живые доказательства»: %s. Door: %s; then run close again. Nothing was written"
                      % (rel, "; ".join(found[:5]) + ("; and %d more" % (len(found) - 5) if len(found) > 5 else ""),
                         PROOF_FORMS, LEFTOVER_DOOR))


def apply_changes(root: Path, writes, deletions) -> None:
    """All or nothing (m-8, t-593). `writes` = [(path, new text)], each written in the form of the file it replaces;
    `deletions` = [path]; then plans/PILES.md is rebuilt. When any step fails, every file touched is put back from the
    bytes read before the first write and CannotRun (exit 1) says so: the tree is as it was."""
    board = Path(root) / BOARD_REL
    forms = {p: read_form(p) for p, _ in writes}
    before = {p: (p.read_bytes() if p.exists() else None) for p in [p for p, _ in writes] + list(deletions) + [board]}
    try:
        for path, text in writes:
            write_like(path, text, forms[path])
        for path in deletions:
            path.unlink()
        rebuild_board(root)
    except BaseException as exc:
        stuck = []
        for path, raw in before.items():
            try:
                if raw is None:
                    path.unlink(missing_ok=True)
                elif not path.exists() or path.read_bytes() != raw:
                    write_bytes_atomic(path, raw)
            except OSError:
                stuck.append(str(path))
        if not isinstance(exc, Exception):
            raise
        raise CannotRun("writing failed (%s: %s) -- %s" % (type(exc).__name__, exc, (
            "could not put back %s; compare them with git before going on" % ", ".join(stuck)) if stuck else
            "every file touched was put back, nothing changed"))


def worktrees_sweep_line(root):
    """t-1738 (FG7-4, F9 a): after a close, start the same FULL worktree sweep the post-merge hook starts, in the background
    (`worktree_sweep.launch_background`: one lock, so a sweep already running is only named), and print one line about it. A
    launch that did not happen is a line with the door, never silence (the owner asked for visibility); the close is done and
    its exit code stays 0 whatever happens here."""
    try:
        import worktree_sweep
    except Exception as exc:                  # the tool itself cannot be imported: there is no door to name either
        return "  worktrees: background sweep not started (%s: %s)" % (type(exc).__name__, str(exc).strip()[:120])
    try:
        kind, text = worktree_sweep.launch_background(Path(root), "piles-close")
    except Exception as exc:
        kind, text = "failed", "%s: %s" % (type(exc).__name__, worktree_sweep.first_line(str(exc)))
    if kind in ("started", "busy"):
        return "  worktrees: %s" % text
    return "  worktrees: %s" % worktree_sweep.not_started(text)


def _close_batch(args, root: Path, today: str) -> int:
    if args.word or args.id:
        raise Refused("--id and --word close one row by the owner's word and take no slug or N; use "
                      '`close --id B-nnn --word "<кто, дата>" [--hash <h>]`')
    if not args.hash:
        raise Refused("--hash is required -- the table of contents names a closed id by its merge commit; add --url for the MR address")
    check_hash(root, args.hash)
    if args.url:
        check_url(args.url)
    n = _parse_n(args.n)
    tree = load_tree(root)
    pile, view = _find_view(tree, args.slug, n)
    where = "%s/%d" % (args.slug, n)
    f = _batch_file(view, where, "nothing to close")
    mr = "`%s`" % args.hash + (" " + args.url if args.url else "")
    if f.status == "закрыта":
        if first_tick(f.mr) == args.hash:
            print("piles close: %s is already closed (%s); nothing changed" % (where, args.hash))
            return 0
        raise Refused("%s is already closed with %s -- a closed batch is not closed again; nothing changed" % (where, f.mr))
    if f.status != "принято":
        raise Refused('%s is "%s" -- close closes a batch the integrator accepted; expected status "принято" in the batch '
                      "header (close brings the card row along)" % (where, f.status_raw))
    if view.row.status == "закрыта":
        raise Refused('the card and the batch file disagree on %s: card status "%s", batch status "%s" -- make them say the '
                      "same thing, then close" % (where, view.row.status_raw, f.status_raw))
    # the gate comes after the status checks (a closed batch stays an idempotent no-op, a wrong status is named first) and
    # before the plan (the BACKLOG side): every refusal precedes the first write
    batch_path = root / f.path
    text = read_text(batch_path)
    check_leftovers(text, f.path, root=root, pile=pile, view=view, deleted=closing_finding_paths(tree, view))
    check_proofs(text, f.path)
    items, done, partial = _plan_batch_close(tree, view, where)
    suffix = "; закрыто %s пачкой `%s`: влито `%s`%s" % (today, where, args.hash, " (MR %s)" % args.url if args.url else "")
    backlog = backlog_with_closed(root, items, suffix)
    card_path = root / pile.card_rel
    card = edit_card(read_text(card_path), view.row, {"status": "закрыта", "mr": mr})
    batch = edit_header(read_text(batch_path), {"статус": "закрыта", "mr": mr})
    apply_changes(root, [(root / BACKLOG_REL, backlog), (card_path, card), (batch_path, batch)],
                  [root / fnd.path for _, fl, _ in items for fnd in fl])
    ids = [i for i, _, _ in items]
    print("piles close: %s closed with %s on %s: moved to Закрыто: %s" % (where, mr, today, ", ".join(ids) or "nothing"))
    for ident in done:
        print("  already closed: %s" % ident)
    if partial:
        print("  partial, left open: %s" % ", ".join("%s %s" % (m.id, m.qualifier) for m in partial))
    for line in debt_warnings(root, ids):
        print(line)
    print(worktrees_sweep_line(root))
    print("  Next: git add %s %s %s; git commit -m \"piles: close %s (%s)\"" % (BACKLOG_REL, "plans/piles/" + args.slug, BOARD_REL,
                                                                           where, args.hash))
    return 0


def _close_word(args, root: Path, today: str) -> int:
    if args.slug or args.n or args.url:
        raise Refused("--id closes one row and takes no slug, N or --url; use "
                      '`close --id B-nnn --word "<кто, дата>" [--hash <h>]`')
    if not re.fullmatch(r"B-\d{3,}", args.id):
        raise Refused('--id "%s": expected B-nnn' % args.id)
    word = (args.word or "").strip()
    if not _text_arg_ok(word, WORD_MAX):
        raise Refused('--word is required with --id and must be the owner\'s word as text: expected --word "<кто, дата>" of '
                      '1-%d characters without "|", a backtick (`) or a line break, got %r' % (WORD_MAX, args.word))
    if args.hash:
        check_hash(root, args.hash)
    tree = load_tree(root)
    if args.id in tree.backlog.closed_ids:
        print("piles close: %s is already closed; nothing changed" % args.id)
        return 0
    for v, m in tree.member_rows():
        if m.id == args.id and not m.partial and v.status != "закрыта":
            raise Refused("%s is a whole member of the live batch %s/%d -- close it with that batch's close, or take it out of "
                          "the card row first" % (args.id, v.slug, v.n))
    items = closing_items(tree, [args.id])
    suffix = "; закрыто %s по слову: %s%s" % (today, word, "; влито `%s`" % args.hash if args.hash else "")
    backlog = backlog_with_closed(root, items, suffix)
    apply_changes(root, [(root / BACKLOG_REL, backlog)], [root / fnd.path for fnd in items[0][1]])
    print("piles close: %s closed by the owner's word (%s) on %s" % (args.id, word, today))
    for line in debt_warnings(root, [args.id]):
        print(line)
    print("  Next: git add %s plans/piles %s; git commit -m \"piles: close %s by the owner's word\"" % (BACKLOG_REL, BOARD_REL, args.id))
    return 0


def cmd_close(args, root) -> int:
    root, today = Path(root), _today(args)
    if args.id:
        return _close_word(args, root, today)
    if not args.slug or not args.n:
        raise CannotRun("usage: expected %s" % CLOSE_FORMS)
    return _close_batch(args, root, today)


def cmd_release(args, root) -> int:
    """The refused alias: `release` was renamed `close`. Nothing runs, whatever the other arguments are."""
    raise CannotRun("`release` was renamed `close` (the command closes a batch or a row; it is not a factory release) -- "
                    "expected `close` with the same arguments: %s; nothing was run" % CLOSE_FORMS)


# ============================================================================================
# CLI
# ============================================================================================

class _Parser(argparse.ArgumentParser):
    def error(self, message):                     # a usage error is "cannot run" (1), not "red" (2)
        raise CannotRun("usage: %s" % message)


def _board_args(p):
    p.add_argument("--check", action="store_true", help="exit 2 when plans/PILES.md is missing or stale; write nothing")
    p.add_argument("--if-staged", action="store_true", help="do nothing unless plans/piles, BACKLOG or PILES.md is staged")


def _check_args(p):
    p.add_argument("--msg-file", help="the commit message file (the hook passes \"$1\"); without it no door is read")
    p.add_argument("--all", action="store_true", help="the whole tree, every red blocks (tests, calibration, CI)")
    p.add_argument("--base", help="the rev (г) compares plans/BACKLOG.md with (default HEAD) and (в) compares the taken batches "
                                  "with (default origin/main); CI passes the pushed range's base")


def _take_args(p):
    p.add_argument("slug", help="the pile (plans/piles/<slug>/)")
    p.add_argument("n", metavar="N", help="the batch number, 1-999")
    p.add_argument("--who", required=True, help="who takes the batch (1-40 characters, no '|', backtick or line break)")
    p.add_argument("--today", help=argparse.SUPPRESS)


def _release_args(p):
    """The alias takes no arguments of its own: whatever follows `release` is left over and the refusal does not read it."""


def _close_args(p):
    p.add_argument("slug", nargs="?", help="the pile of the accepted batch")
    p.add_argument("n", metavar="N", nargs="?", help="the batch number")
    p.add_argument("--hash", help="the merge commit (7-40 hex characters, must be a commit of this repository)")
    p.add_argument("--url", help="the MR address (https://..., at most 300 characters)")
    p.add_argument("--id", help="close ONE row by the owner's word (B-nnn), outside any batch")
    p.add_argument("--word", help="the owner's word for --id: \"<кто, дата>\" (1-120 characters, no '|', backtick or line break)")
    p.add_argument("--today", help=argparse.SUPPRESS)


# command -> (adds its arguments, runs).
COMMANDS = {"board": (_board_args, cmd_board), "check": (_check_args, cmd_check),
            "take": (_take_args, cmd_take), "close": (_close_args, cmd_close),
            "release": (_release_args, cmd_release)}          # release: the refused alias of close


def build_parser() -> argparse.ArgumentParser:
    ap = _Parser(prog="piles.py", description=__doc__.split("\n")[0])
    ap.add_argument("--repo", help="the repository root (default: the parent of tools/)")
    sub = ap.add_subparsers(dest="cmd", required=True, parser_class=_Parser)
    for name, (add, _) in COMMANDS.items():
        add(sub.add_parser(name, add_help=name != "release"))
    return ap


def main(argv=None) -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass
    cmd = ""
    try:
        parser = build_parser()
        args, extra = parser.parse_known_args(argv)         # `release` takes nothing, so its arguments arrive as `extra`
        if extra and args.cmd != "release":
            parser.error("unrecognized arguments: %s" % " ".join(extra))
        cmd = args.cmd
        return COMMANDS[cmd][1](args, Path(args.repo) if args.repo else REPO)
    except Refused as exc:
        print("piles %s: %s" % (cmd, exc))
        return 2
    except CannotRun as exc:
        print(("piles %s: %s" % (cmd, exc)) if cmd else ("piles: %s" % exc))
        return 1


if __name__ == "__main__":
    sys.exit(main())
