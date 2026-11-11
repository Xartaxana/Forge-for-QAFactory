"""digest_form.py -- the reader of the scout digest form v1 (t-797 F5-2, node N1). Pure functions, no input or output.

A scout's final message is its digest; form v1 makes it a table "one row per object" plus a table of the trail, which
`.claude/agents/scout.md` teaches and this module reads BACK. The reader only REPORTS (P1, FR-45 in spirit): it changes nothing,
cuts nothing, refuses nothing -- the report file stays the worker's verbatim text (I2). What it must never do is say "no flags"
about a claim without a trail or a negative without a control of the same form (I1): every ambiguity errs towards a flag.

    parse(text) -> Digest | None     None: no `digest: v1` key line (today's prose digest, or no digest at all)
    flags(d)    -> list[str]         rows of the trail first, then the objects, then the markup; [] means "nothing to report"
    trail_backing_flags(d, calls)    the Trail rows against the worker's tool_use calls (t-863, F6-14): [] / trail_unbacked:<n> /
                                     trail_unchecked (no transcript). Pure: the caller (handback_extract) reads the transcript.

The grammar, the flag list and two examples live in docs/tasks/exchange-form.md; the closed `result` grammar is RESULT_* below.
FLAG_NAMES is the ONE list of the names flags(d) can return, TRANSCRIPT_FLAG_NAMES of the two trail_backing_flags can.
Tables are read through tools/md_table.py (a leaf: stdlib `re` only), NEVER through `piles`: this module is imported by
tools/handback_extract.py, which must not break because `piles` pulls six other modules (spec t-797 F9).
"""
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import NamedTuple

_TOOLS_DIR = Path(__file__).resolve().parent
if str(_TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(_TOOLS_DIR))
import md_table  # noqa: E402

OBJECTS_HEADER = ["id", "kind", "gist", "paths", "status", "owner", "links", "ev"]
TRAIL_HEADER = ["tid", "op", "target", "pattern / range", "flags", "result", "control"]
GIST_MAX = 20                                   # words, str.split(); the text is never cut
FORKS_LINE = "this needs a decision from a tier above."
OPS = ("read", "grep", "glob")
BOM = "\N{ZERO WIDTH NO-BREAK SPACE}"           # U+FEFF as a named escape: the source carries no invisible character
NO_VALUE = ("", "—")                        # an empty cell and the em dash both mean "nothing here"
REQUIRED = ("Objects", "Trail")                 # Forks and Not done are optional
KNOWN_SECTIONS = ("Objects", "Trail", "Forks", "Not done")

# The names of the flags (the part before the first colon). The ONE list: the note exchange-form.md must carry every FLAG_NAMES
# entry and the module must emit no other name (tools/test_digest_form.py pins both directions; t-863, F6-14).
FLAG_NAMES = ("zero_no_control", "control_unknown", "control_shape", "zero_case", "bad_result", "dup_tid", "tid_space", "bad_row",
              "no_id", "id_space", "dup_id", "gist_over", "no_ev", "ev_unknown", "zero_uncontrolled", "absent_no_negative",
              "bad_header", "no_section", "dup_section", "forks_no_line", "key_not_first", "key_no_task", "stray_row",
              "unknown_section", "comment_unclosed", "fence_unclosed")
TRAIL_UNBACKED = "trail_unbacked"                # trail_unbacked:<n>: n Trail rows no tool_use of the transcript stands behind
TRAIL_UNCHECKED = "trail_unchecked"              # no transcript to check against (a gateway worker): said, never a pass or a fail
TRANSCRIPT_FLAG_NAMES = (TRAIL_UNBACKED, TRAIL_UNCHECKED)
BACKING_TOOL = {"read": "Read", "grep": "Grep", "glob": "Glob"}     # the tool_use a Trail row of that op must stand behind
ROOT_TARGETS = ("", ".")                         # a target that names "everywhere": any Grep / Glob call, with or without a path

# The closed grammar of the Trail `result` cell (spec section 3.1). Digits are [0-9] on purpose: \d would admit other scripts.
RESULT_ABSENT = "absent"                        # grep without `count`, glob: the zero
RESULT_FOUND = re.compile(r"found ([1-9][0-9]*)(?:; \S.*)?")
RESULT_COUNT = re.compile(r"count (0|[1-9][0-9]*)")      # grep with `count`: `count 0` is the zero
RESULT_READ = re.compile(r"read \S.*:\S.*")              # never a zero


@dataclass
class Digest:
    """What parse() found; flags() derives everything else. Rows are the raw cell lists, one per table line."""
    task_id: object                              # the third word of the key line, None when the key carries none
    object_rows: list = field(default_factory=list)
    trail_rows: list = field(default_factory=list)
    objects_read: bool = False                   # the Objects header is the exact one, so its columns can be trusted
    trail_read: bool = False
    markup: list = field(default_factory=list)   # key, section and header flags, in report order

    @property
    def n_objects(self):
        return len(self.object_rows)

    @property
    def n_trail(self):
        return len(self.trail_rows)


# --------------------------------------------------------------------------------------------------------------------
# parse
# --------------------------------------------------------------------------------------------------------------------

def _find_key(lines):
    """(index, task_id or None, something_precedes) of the first `digest: v1 [<task_id>]` line; None when there is none.
    `lines` come with their HTML comments already blanked. Something precedes the key unless everything before it is blank or a
    CLOSED fenced block; a key INSIDE a fence (a fence around the digest) is found all the same and is preceded by the fence."""
    for i, line in enumerate(lines):
        words = line.strip().lstrip(BOM).split()
        if words[:2] == ["digest:", "v1"]:
            outside = dict(md_table.md_lines_outside_fences(lines[:i + 1]))
            preceded = i not in outside or any(l.strip().lstrip(BOM) for k, l in outside.items() if k < i)
            return i, (words[2] if len(words) > 2 else None), preceded
    return None


def _headings(lines):
    """[(line index, name)] of every `## name` line."""
    return [(i, line[3:].strip()) for i, line in enumerate(lines) if line.startswith("## ")]


def _sections(lines, headings):
    """{name: [lines from the heading to the next heading]} for the FIRST occurrence of each known section, and the names that
    occur more than once."""
    found, dup = {}, []
    for k, (i, name) in enumerate(headings):
        if name not in KNOWN_SECTIONS:
            continue
        if name in found:
            if name not in dup:
                dup.append(name)
            continue
        end = headings[k + 1][0] if k + 1 < len(headings) else len(lines)
        found[name] = lines[i:end]
    return found, dup


def _read_table(section, name, header):
    """(rows, header_ok): the table under the section heading. No table, or a header that is not the exact one, is not read."""
    table = md_table.table_after(section, name)
    if table is None:
        return [], False
    cells, rows = table
    return [r for r, _ in rows], cells == header


def _stray_rows(section, name):
    """stray_row:<name>:<n> for every pipe line of a table section that is NOT the read table's header, its one separator or one
    of its rows (I1: a row nobody reads is a claim nobody checked). The read table is the first one; a second table, a row after
    a prose line or a `###` heading, an indented row, a second separator-like row are all stray. n is the 1-based line number
    inside the section, its `## ` heading being line 1."""
    kinds = [kind for kind, _ in md_table.walk_table(section)]
    header = next((j for j, kind in enumerate(kinds) if kind == "header"), None)
    run, sep = set(), None
    if header is not None:
        end = next((j for j in range(header, len(kinds)) if kinds[j] is None), len(kinds))
        run = set(range(header, end))
        sep = header + 1 if header + 1 < len(kinds) and kinds[header + 1] == "rule" else None
    return ["stray_row:%s:%d" % (name, j + 1) for j, line in enumerate(section)
            if line.lstrip().startswith("|") and not (j in run and (kinds[j] != "rule" or j == sep))]


def _read_tables(d, sections):
    """Fill d from the Objects and Trail sections; -> (bad_header flags, stray_row flags)."""
    bad_header, stray = [], []
    for name, header in (("Objects", OBJECTS_HEADER), ("Trail", TRAIL_HEADER)):
        if name not in sections:
            continue
        rows, ok = _read_table(sections[name], name, header)
        if name == "Objects":
            d.object_rows, d.objects_read = rows, ok
        else:
            d.trail_rows, d.trail_read = rows, ok
        if not ok:
            bad_header.append("bad_header:" + name)
        stray += _stray_rows(sections[name], name)
    return bad_header, stray


def parse(text):
    """Digest, or None when the text carries no `digest: v1` key line. Reading starts at the key line (a preamble before it is
    flagged key_not_first; HTML comments and closed fenced blocks before it are not a preamble). After the key, comment and
    fenced lines are blanked (their indices kept) so a fenced example is never data. CRLF and CR are line ends. Never raises
    on a str."""
    raw = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    lines, unclosed = _unwrap_container(raw, *md_table._blank_comments(raw))
    key = _find_key(lines)
    if key is None:
        return None
    index, task_id, preceded = key
    body, fence_open = _body(lines, index)
    headings = _headings(body)
    sections, dup = _sections(body, headings)
    d = Digest(task_id=task_id)
    bad_header, stray = _read_tables(d, sections)
    unknown = list(dict.fromkeys(name for _, name in headings if name not in KNOWN_SECTIONS))
    d.markup = (bad_header
                + ["no_section:" + n for n in REQUIRED if n not in sections]
                + ["dup_section:" + n for n in dup]
                + stray
                + ["unknown_section:" + n for n in unknown]
                + _forks_flags(sections.get("Forks"))
                + (["key_not_first"] if preceded else [])
                + (["key_no_task"] if task_id is None else [])
                + (["comment_unclosed:%d" % (unclosed + 1)] if unclosed is not None else [])
                + (["fence_unclosed:%d" % fence_open] if fence_open else []))
    return d


def _container_close(lines, container, after):
    """The index of the line that closes the container fence opened at `container`, or None. It is the LAST non-blank line (at or
    after `after`), and it closes by the fence grammar: `md_table.fence_walk` on the pair, so the same mark, a run as long and
    nothing after it -- a shorter run, an info string or the other mark does not close it."""
    last = next((k for k in range(len(lines) - 1, after - 1, -1) if lines[k].strip()), None)
    if last is None:
        return None
    roles = [role for _i, _l, role in md_table.fence_walk([lines[container], lines[last]])]
    return last if roles[1:] == ["close"] else None


def _unwrap_container(raw, lines, unclosed):
    """-> (lines, unclosed) with the comments INSIDE a digest wrapped whole in a fence read as the digest's own. The container is a
    transport envelope, not code: it is unwrapped first (its open and close lines stay, found by `fence_walk`), and only the text
    between them goes through `md_table._blank_comments`, where the first opener wins as everywhere else -- a real code fence
    INSIDE the digest still protects its `<!--`. `lines`, `unclosed` are the first pass over the whole text, good for the part
    BEFORE the key (the envelope's own opener); without a container, or when a comment that never closes sits before the key,
    they come back as they are. The text after the closing line is blanked on its own."""
    key = _find_key(lines)
    if key is None or (unclosed is not None and unclosed < key[0]):
        return lines, unclosed
    container = md_table.unclosed_fence(lines[:key[0]])
    if container is None:
        return lines, unclosed
    end = _container_close(raw, container, key[0] + 1)
    inner, inner_unclosed = md_table._blank_comments(raw[container + 1:end])
    tail, tail_unclosed = md_table._blank_comments(raw[end + 1:]) if end is not None else ([], None)
    closing = [] if end is None else [raw[end]]
    first = inner_unclosed + container + 1 if inner_unclosed is not None else (
        None if tail_unclosed is None else tail_unclosed + end + 1)
    return lines[:container + 1] + inner + closing + tail, first


def _body(lines, index):
    """(the lines after the key with every fenced line blanked and the line count kept, the 1-based line of the message of a fence
    that never closes or None). A fence nothing closes hides every line after it -- a hidden row is a hidden claim -- so the
    caller flags it. The one fence that is not flagged: the container, the fence the key itself sits in (a digest wrapped in a
    fence whole); its closing mark is the LAST non-blank line of the message and is dropped from the body, trailing blank lines
    after it or not. Any other fence mark after the key, the last line included, is the body's own."""
    rest = lines[index + 1:]
    container = md_table.unclosed_fence(lines[:index])
    closing = None if container is None else _container_close(lines, container, index + 1)
    if closing is not None:
        rest = rest[:closing - index - 1] + [""] + rest[closing - index:]
    visible = {k for k, _ in md_table.md_lines_outside_fences(rest)}
    opened = md_table.unclosed_fence(rest)
    return [line if k in visible else "" for k, line in enumerate(rest)], None if opened is None else index + opened + 2


def _forks_flags(section):
    """forks_no_line when a Forks section does not END with the literal line scout.md rule 3 prescribes."""
    if section is None:
        return []
    tail = [line.strip() for line in section[1:] if line.strip()]
    return [] if tail and tail[-1] == FORKS_LINE else ["forks_no_line"]


# --------------------------------------------------------------------------------------------------------------------
# the trail: rows, their result kind, the controls of the zero rows
# --------------------------------------------------------------------------------------------------------------------

@dataclass
class _Row:
    """One Trail row that can be referred to by its tid. kind: zero / found / read / bad (a result outside the grammar) /
    invalid (a malformed row: the tid exists but the row is neither a zero nor a control)."""
    tid: str
    op: str = ""
    target: str = ""
    pattern: str = ""
    flagset: frozenset = frozenset()
    control: str = ""
    kind: str = "invalid"


def _result_kind(op, flagset, result):
    """zero / found / read / bad for a result cell under the closed grammar of its op and flags."""
    if op == "read":
        return "read" if RESULT_READ.fullmatch(result) else "bad"
    if op == "grep" and "count" in flagset:
        m = RESULT_COUNT.fullmatch(result)
        return "bad" if m is None else ("zero" if m.group(1) == "0" else "found")
    if result == RESULT_ABSENT:
        return "zero"
    return "found" if RESULT_FOUND.fullmatch(result) else "bad"


def _trail_rows(rows):
    """(index {tid: _Row} -- the FIRST row of a tid --, ordered [(_Row or None, pre-flags)]) over the raw trail rows. A row with
    the wrong cell count or an empty tid or an unknown op is bad_row: its columns are not trusted, so it is neither zero nor
    control (its tid, when it has one, is still known to the objects). A repeated tid is dup_tid and the row is not read."""
    index, ordered = {}, []
    for n, cells in enumerate(rows, 1):
        tid = cells[0] if cells else ""
        if len(cells) != len(TRAIL_HEADER) or not tid or cells[1] not in OPS:
            if tid and tid not in index:
                index[tid] = _Row(tid=tid)
            ordered.append((None, ["bad_row:Trail:%d" % n]))
            continue
        pre = ["tid_space:%d" % n] if len(tid.split()) != 1 else []
        if tid in index:
            ordered.append((None, ["dup_tid:" + tid] + pre))
            continue
        row = _Row(tid=tid, op=cells[1], target=cells[2], pattern=cells[3], control=cells[6],
                   flagset=frozenset([] if cells[4] in NO_VALUE else cells[4].split()))
        row.kind = _result_kind(row.op, row.flagset, cells[5])
        index[tid] = row
        ordered.append((row, pre))
    return index, ordered


def _same_form(zero, control):
    """A control of a zero row: another row, found something (not a zero, not out of grammar), same op, same target, same flags,
    a different pattern -- the invariant I1: a negative proves nothing without a positive of the SAME call shape."""
    return (control.kind == "found" and control.op == zero.op and control.target == zero.target
            and control.flagset == zero.flagset and control.pattern != zero.pattern)


def _control_flag(zero, index):
    """The flag a zero row earns for its control, or None when the control is good."""
    if zero.control in NO_VALUE:
        return "zero_no_control:" + zero.tid
    control = index.get(zero.control)
    if control is None:
        return "control_unknown:" + zero.tid
    return None if _same_form(zero, control) else "control_shape:" + zero.tid


def _row_flags(row, pre, index):
    """The flags of one readable Trail row, in the order of the spec list; `pre` (dup_tid, tid_space, bad_row) go last."""
    out = []
    if row is not None and row.kind == "zero":
        out.append(_control_flag(row, index))
        if row.op == "grep" and "-i" not in row.flagset:
            out.append("zero_case:" + row.tid)
    if row is not None and row.kind == "bad":
        out.append("bad_result:" + row.tid)
    return [f for f in out if f] + pre


# --------------------------------------------------------------------------------------------------------------------
# the objects: one claim each, with a trail to stand on
# --------------------------------------------------------------------------------------------------------------------

def _ev_tids(cell):
    """The tids a cell names: comma separated, each stripped, an empty element (a trailing comma) dropped, exact case."""
    seen = []
    for part in ("" if cell in NO_VALUE else cell).split(","):
        part = part.strip()
        if part and part not in seen:
            seen.append(part)
    return seen


def _is_absent(status):
    words = status.lower().split()
    return bool(words) and words[0].strip(".,;:") == "absent"


def _evidence_flags(label, status, ev, index):
    """no_ev / ev_unknown / zero_uncontrolled / absent_no_negative of one object (I1): ANY zero row of its `ev` without a good
    control is a flag, and a claim `absent` must stand on at least one zero row."""
    tids = _ev_tids(ev)
    if not tids:
        return ["no_ev:" + label]
    out, zero_seen = [], False
    for tid in tids:
        row = index.get(tid)
        if row is None:
            out.append("ev_unknown:%s:%s" % (label, tid))
        elif row.kind == "zero":
            zero_seen = True
            if _control_flag(row, index):
                out.append("zero_uncontrolled:%s:%s" % (label, tid))
    if _is_absent(status) and not zero_seen:
        out.append("absent_no_negative:" + label)
    return out


def _object_flags(rows, index):
    """The flags of the Objects rows, row by row. A row with the wrong cell count is bad_row and read no further. An object with
    no id is labelled #<row> in the flags that need a name. A repeated id is dup_id; every row is still checked (each is a claim)."""
    out, ids = [], set()
    for n, cells in enumerate(rows, 1):
        if len(cells) != len(OBJECTS_HEADER):
            out.append("bad_row:Objects:%d" % n)
            continue
        oid, gist, status, ev = cells[0], cells[2], cells[4], cells[7]
        label = oid or "#%d" % n
        if not oid:
            out.append("no_id:%d" % n)
        elif len(oid.split()) != 1 or "," in oid:
            out.append("id_space:%d" % n)
        if oid and oid in ids:
            out.append("dup_id:" + oid)
        ids.add(oid)
        if len(gist.split()) > GIST_MAX:
            out.append("gist_over:" + label)
        out.extend(_evidence_flags(label, status, ev, index))
    return out


def flags(d):
    """The flags of a Digest, a list of strings; the order is: Trail rows, objects, markup. Rows and objects are read only when
    the header of their table is the exact one (the columns of any other table cannot be trusted)."""
    index, ordered = _trail_rows(d.trail_rows) if d.trail_read else ({}, [])
    out = []
    for row, pre in ordered:
        out.extend(_row_flags(row, pre, index))
    if d.objects_read:
        out.extend(_object_flags(d.object_rows, index))
    return out + d.markup


# --------------------------------------------------------------------------------------------------------------------
# the trail against the transcript (t-863, F6-14): was the row run? The class "a fabricated trail" (tools/pi_run_guard.py)
# --------------------------------------------------------------------------------------------------------------------

class ToolCall(NamedTuple):
    """One Read / Grep / Glob tool_use of a worker's transcript, as handback_extract reads it: the tool name, the path the call
    named (Read: file_path; Grep, Glob: path -- None when it named none) and the pattern (Grep, Glob; None for Read)."""
    name: str
    path: object = None
    pattern: object = None


def _plain(value):
    """The comparison form of a text: lower case, backslash to slash, runs of white space to one space; "" for a non-str."""
    return " ".join(value.replace("\\", "/").lower().split()) if isinstance(value, str) else ""


def _plain_path(value):
    """_plain, then no `./` in front, no trailing slash, one slash for a run of them (`C:\\Work\\x\\` and `c:/work/x` are the same)."""
    text = re.sub(r"/{2,}", "/", _plain(value))
    return (text[2:] if text.startswith("./") else text).rstrip("/")


def _backed(row, calls):
    """True when some call of the transcript stands behind the Trail row: a `read` row behind a Read whose file_path CONTAINS the
    row's target; a `grep` / `glob` row (a zero one too -- a negative claim needs the search it names) behind a Grep / Glob
    whose pattern contains the row's pattern AND whose path contains the row's target, unless the target is the root. The
    direction is one: what the digest says must lie inside what the tool recorded (an absolute path contains the relative one)."""
    target, pattern = _plain_path(row.target), _plain(row.pattern).strip("` ")
    for call in calls:
        if call.name != BACKING_TOOL[row.op]:
            continue
        where = _plain_path(call.path)
        if row.op == "read":
            if target and target in where:
                return True
        elif pattern and pattern in _plain(call.pattern) and (target in ROOT_TARGETS or target in where):
            return True
    return False


def trail_backing_flags(d, calls):
    """The flags of a Digest's Trail against the worker's tool calls (a list of ToolCall, the WHOLE transcript's): `trail_unbacked:<n>`
    when n readable rows have no matching call, [] when every one has. `calls` None means there is no transcript to check against
    (a gateway worker writes none): the check is skipped and the flag is `trail_unchecked` -- never `trail_unbacked`, an unchecked
    trail is not a fabricated one. Rows the reader does not trust (bad_row, dup_tid) are flagged by flags() and not counted here."""
    if calls is None:
        return [TRAIL_UNCHECKED]
    ordered = _trail_rows(d.trail_rows)[1] if d.trail_read else []
    missing = sum(1 for row, _ in ordered if row is not None and not _backed(row, calls))
    return ["%s:%d" % (TRAIL_UNBACKED, missing)] if missing else []
