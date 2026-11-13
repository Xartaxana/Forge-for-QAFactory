"""One task key for every journal READER (B-402).

Two clones of this repository issue task ids independently, and `merge=union` joins their
journals without renumbering: the same `t-050` then names two different tasks, and a reader that
keys by the bare id lets an `accepted` of one clone close the other clone's still-open dispatch
(the false close that the 13(i) open-dispatch check and the SessionStart OPEN DISPATCH list
exist to catch). The measured case: 71 ids, t-007..t-077, issued by both the codex-fixes branch
and main (docs/tasks/legacy-2406-sync-081.md, "Nomera").

The remedy is a DECLARATION, `logs/journal-segments.json`: for each foreign instance it lists the
lines (by identity) that belong to it and gives it a label. A reader's task key is then
(label, task_id): the label is "" for every undeclared line, so a journal with no declaration
reads exactly as it always did. The gate (tools/journal_validator.py) stays on BARE ids -- it
over-refuses, which is the allowed direction -- and only READERS key.

Identity of a journal line = (ts, task_id, event, agent, worker_ref), five strings, "" for an
absent worker_ref. It is not guaranteed unique: two lines identical in all five fields are
listed twice, and `check` requires the listed count to equal the matched count, so the listing
determines the matched lines exactly.

Pure functions (no git, no cwd) plus a small CLI:
  python tools/journal_keys.py declare --label L --lines A-B --why TEXT   # write a segment
  python tools/journal_keys.py check                                      # validate the file
Readers that must never fail loudly call load_segments(journal_path): it never raises, and any
failure gives NO_SEGMENTS plus a reason the reader prints (a partial declaration is never applied
-- all or nothing).

ONE FILE PER WRITER (t-581, F0-4). The journal of a clone is logs/journal/<slug>.jsonl, `<slug>` =
the `developer:` key of the untracked tools/dev.config.yaml (developer_slug); logs/routing-log.jsonl
is the HISTORY up to the switch and takes no new lines afterwards. The owner's file continues the
history (its line 1 is a journal_created with `"continues": "logs/routing-log.jsonl"`): its lines
carry the same label "" (alias `main`), so a task delegated in the history and accepted in the
successor is ONE task. Every other writer's lines carry their slug as the label. The one loader of
all of this is load_all(root) (never raises); current_path(root) is the one answer to "where do I
write", for the hooks, the readers and the Lead (CLI: `python tools/journal_keys.py where`).
The label space is {"" / main} + the declared segments + the file slugs. Hooks import this module,
so everything here is stdlib only (the developer config is read by tools/dev_config.py, the one
reader of it: a stdlib line parser, not yaml).
"""
from __future__ import annotations

import argparse
import heapq
import json
import os
import re
import sys
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import NamedTuple

try:
    import dev_config
except ImportError:  # imported by file path, with tools/ not on sys.path
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import dev_config

VERSION = 1
SEGMENTS_NAME = "journal-segments.json"
SEGMENTS_REL = "logs/" + SEGMENTS_NAME
JOURNAL_REL = "logs/routing-log.jsonl"
HISTORY_REL = JOURNAL_REL
JOURNAL_DIR_REL = "logs/journal"
DEV_CONFIG_REL = "tools/dev.config.yaml"
MAIN_LABEL = "main"
RESERVED_LABELS = frozenset({MAIN_LABEL})
CONTINUES_FIELD = "continues"
# a developer slug is a LABEL (LABEL_RE below, 1-24) of 2-24 characters that starts with a letter;
# the one definition lives in dev_config (the one reader of tools/dev.config.yaml)
SLUG_RE = dev_config.SLUG_RE
_TS_SHAPE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?$")
IDENTITY_FIELDS = ("ts", "task_id", "event", "agent", "worker_ref")
LABEL_RE = re.compile(r"^[a-z0-9-]{1,24}$")
REF_RE = re.compile(r"^(t-\d{3,})(?:@([a-z0-9-]{1,24}))?$")
# The `closes:` token of a journal line's notes: `closes:t-NNN` or `closes:t-NNN@label`. The
# `(?<!\w)` boundary keeps `discloses:t-001` out. The label part is captured WIDER than a valid
# label (any run of [A-Za-z0-9_-]) on purpose: a token whose `@...` is not a valid label closes
# NOTHING (closes_tokens drops it) -- reading `closes:t-050@Codex` as the bare `closes:t-050` would
# close the OTHER clone's instance, the false close this module exists to prevent. The readers
# (session_context, calibration_counts) keep a fallback copy of this regex for the case that this
# module cannot be imported; a test in each pins their pattern equal to this one.
CLOSES_RE = re.compile(r"(?<!\w)closes:(t-\d+)(@[A-Za-z0-9_-]*)?")
# The NODE of a `delegated` line (t-797 F5-2, M5): the pile node the work belongs to, ONE form everywhere --
# the `node` field, the hop_metrics `--node` argument and the normalized notes token: `<slug>/<N>/<id>`
# (`forge/5/F5-2`, `conductor/2/C2-1`, `forge/4/D9`). A bare id (`F5-2`) is never a node: ids repeat between
# piles. `\Z`, not `$`: `$` also matches before a trailing newline, and `forge/5/F5-2\n` is not a node.
# The id ends in a letter or a digit, never a dash (`forge/5/F5-` is not a node: the critic's FX-6 of t-812).
NODE_RE = re.compile(r"^[a-z][a-z0-9-]*/[1-9][0-9]*/[A-Za-z](?:[A-Za-z0-9-]*[A-Za-z0-9])?\Z")
# The node as OLD lines wrote it in `notes`: `<slug>/<N> <id>` ("forge/5 F5-2") or already `<slug>/<N>/<id>`.
# Not inside a path or a word (the lookbehind), not followed by more id characters (the lookahead). The id of
# a TOKEN holds a digit (F5-2, C2-1, D9): prose is full of `<word>/<N> <word>` ("conductor/1 node", "3070 passed"
# as failed/3070/passed), measured on the live journal -- NODE_RE itself, for a written field, does not ask for one.
NODE_TOKEN_RE = re.compile(r"(?<![\w/.-])([a-z][a-z0-9-]*)/([1-9][0-9]*)[ /]((?=[A-Za-z0-9-]*\d)[A-Za-z](?:[A-Za-z0-9-]*[A-Za-z0-9])?)(?![\w/-])")
MAX_PROBLEMS_SHOWN = 3
# ID BANDS (rule 9e of journal_validator, F6-58): the optional `id_band` field of ANY journal line, ONE door for a
# parallel branch and for a second writer of the same file. Closed `t-A..t-B` reserves the ids A..B for the writer
# who declares it; open `t-A..` raises the file's own sequence so that its next brand-new id is t-A. Both ends are
# ASCII digits, 3 to 9 of them (`[0-9]`, never `\d`: a fullwidth digit is not the same number; bounded, so int() is
# never reached on a long run). `\Z`, not `$`: `t-500..\n` is not a band. The id regex of the next-id readers
# (ID_NUM_RE) is the same ASCII class, kept here because journal_validator imports this module, not the reverse.
BAND_RE = re.compile(r"^t-([0-9]{3,9})\.\.(?:t-([0-9]{3,9}))?\Z")
ID_NUM_RE = re.compile(r"^t-([0-9]{3,9})$")
BAND_MAX_SIZE = 1000      # ids in a closed band
BAND_JUMP_MAX = 10000     # a band may start at most this far above `top`
BAND_GAP_MIN = 50         # a closed band starts at least this far above `top` (it protects by DISTANCE)
BAND_SHOW_MAX = 3         # band lines printed by `where` / the snapshot / the NOVELTY text


class Segments:
    """A parsed declaration. `segments`: tuple of (label, why, lines) where lines is a tuple of
    identity tuples; `index`: identity -> label (a repeated identity keeps its first label --
    `check` refuses an identity listed by two segments); `listed`: identity -> how many times it
    is listed in all; `ids`: label -> the set of task ids that segment holds."""

    def __init__(self, version=VERSION, segments=()):
        self.version = version
        self.segments = tuple(segments)
        self.index: dict = {}
        self.listed: Counter = Counter()
        self.ids: dict = {}
        for label, _why, lines in self.segments:
            for ident in lines:
                self.index.setdefault(ident, label)
                self.listed[ident] += 1
                self.ids.setdefault(label, set()).add(ident[1])

    def __bool__(self) -> bool:
        return bool(self.segments)

    @property
    def labels(self) -> list:
        return [label for label, _w, _l in self.segments]


NO_SEGMENTS = Segments()


def identity(obj: dict) -> tuple:
    """The five-field identity of a journal line object (non-strings read as "")."""
    return tuple(obj.get(k) if isinstance(obj.get(k), str) else "" for k in IDENTITY_FIELDS)


def split_lines(text: str | None) -> list[str]:
    if not text:
        return []
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    return lines


def closes_tokens(notes) -> list[str]:
    """The `closes:` tokens of a notes field, as the strings ref_key resolves: `t-NNN` or
    `t-NNN@label`. [] for a non-string. A token whose `@...` part is not a valid label (1-24 of
    [a-z0-9-]) is DROPPED: it closes nothing, not even the bare id. Never raises."""
    if not isinstance(notes, str):
        return []
    out = []
    for m in CLOSES_RE.finditer(notes):
        at = m.group(2)
        if at is None:
            out.append(m.group(1))
        elif LABEL_RE.match(at[1:]):
            out.append(m.group(1) + at)
    return out


def node_tokens(notes) -> set:
    """The node tokens of a notes field, each normalized to `<slug>/<N>/<id>`; a set (the same node written
    twice is one). Empty for a non-string. Never raises."""
    if not isinstance(notes, str):
        return set()
    return {"%s/%s/%s" % m.groups() for m in NODE_TOKEN_RE.finditer(notes)}


def node_of(obj):
    """(node | None, reason) of a journal line: the `node` FIELD first, else the notes token.

    A field that is present (not absent, not null) decides alone: a string in NODE_RE is the node; a
    non-string (a list, a dict, a number: E27) is (None, "node_not_string") and a string outside the form is
    (None, "node_not_form") -- never a TypeError, and never a fallback to the notes token, because a line that
    wrote a bad field is a bad line, not an unlinked one. A good field next to a notes token that names ANOTHER
    node is (node, "node_token_differ"): the field wins, the reason is the readers' WARN (E26). With no field:
    one token -> (token, None); two different tokens -> (None, "two_tokens") (the link is not guessed, I4);
    none -> (None, "no_node"). A non-dict is (None, "not_an_object"). Pure, never raises."""
    if not isinstance(obj, dict):
        return None, "not_an_object"
    tokens = node_tokens(obj.get("notes"))
    value = obj.get("node")
    if value is not None:
        if not isinstance(value, str):
            return None, "node_not_string"
        if NODE_RE.match(value) is None:
            return None, "node_not_form"
        return value, ("node_token_differ" if tokens and tokens != {value} else None)
    if len(tokens) == 1:
        return next(iter(tokens)), None
    return None, "two_tokens" if tokens else "no_node"


class Band(NamedTuple):
    """A parsed `id_band`: `lo`, `hi` (None for the open form `t-A..`) and the `raw` text as written."""
    lo: int
    hi: int | None
    raw: str

    @property
    def label(self) -> str:
        """The band in the journal's own width: `t-450..t-499` / `t-450..`."""
        return f"t-{self.lo:03d}.." + (f"t-{self.hi:03d}" if self.hi is not None else "")


def id_band_of(obj):
    """(Band | None, reason | None) of a journal line: the optional `id_band` FIELD (rule 9e).

    Absent or JSON null -> (None, None) (as `node`); a non-dict is (None, None) too. Present and not a str ->
    (None, "band_not_string"); a str outside BAND_RE (fullwidth digits, 10+ digits, spaces, a dash other than
    `..`) -> (None, "band_not_form"); a closed band whose end is below its start -> (None, "band_reversed"); one
    that holds more than BAND_MAX_SIZE ids -> (None, "band_too_big"). Pure, never raises, never reaches int() on
    more than 9 digits."""
    if not isinstance(obj, dict):
        return None, None
    value = obj.get("id_band")
    if value is None:
        return None, None
    if not isinstance(value, str):
        return None, "band_not_string"
    m = BAND_RE.match(value)
    if m is None:
        return None, "band_not_form"
    lo = int(m.group(1))
    hi = int(m.group(2)) if m.group(2) is not None else None
    if hi is not None:
        if hi < lo:
            return None, "band_reversed"
        if hi - lo + 1 > BAND_MAX_SIZE:
            return None, "band_too_big"
    return Band(lo, hi, value), None


def suggested_band(top: int) -> int:
    """The start of the band a second writer is told to open: a round number (a multiple of 50) at least
    BAND_GAP_MIN above `top`. The one function behind `where`, the refusals and the PARALLEL SESSION note."""
    return -(-(top + BAND_GAP_MIN) // 50) * 50


class NextIds(NamedTuple):
    """`main`: the next id of the file's own sequence; `bands`: {Band: next id | None (used up)} of the closed
    bands in declaration order; `top`: the highest id or band end seen (see BandState.top)."""
    main: int
    bands: dict
    top: int


class BandState:
    """The one incremental state of the next-id rule, fed line by line (rule 9a and 9e): every task id seen, the
    closed bands and the open bands. The gate feeds it OLD lines with `add(obj)` (their bands are never judged:
    append-only) and a NEW line through check_band / add."""

    def __init__(self):
        self.ids: set = set()        # ints: the task ids that match ID_NUM_RE
        self.closed: list = []       # closed Bands, declaration order
        self.opens: list = []        # lo of every open band

    def _inside(self, n: int) -> bool:
        return any(b.lo <= n <= b.hi for b in self.closed)

    @property
    def top(self) -> int:
        """The maximum of every id seen, every closed band's end and every open band's `lo - 1` (0 when none)."""
        return max([*self.ids, *(b.hi for b in self.closed), *(lo - 1 for lo in self.opens), 0])

    def check_band(self, band):
        """None when `band` may be declared now, else why not: "below" (`lo <= top`: it reaches back and could
        hand out an id twice), "near" (a closed band under BAND_GAP_MIN above `top`: the other writer's next
        id lands on its first), "jump" (more than BAND_JUMP_MAX above `top`)."""
        top = self.top
        if band.lo <= top:
            return "below"
        if band.hi is not None and band.lo < top + BAND_GAP_MIN:
            return "near"
        if band.lo - top > BAND_JUMP_MAX:
            return "jump"
        return None

    def add_band(self, band) -> None:
        """Take a form-valid band into the state (the same band twice is one)."""
        if band.hi is None:
            if band.lo not in self.opens:
                self.opens.append(band.lo)
        elif all((b.lo, b.hi) != (band.lo, band.hi) for b in self.closed):
            self.closed.append(band)

    def add(self, obj, band_ok: bool = True) -> None:
        """One line: its band first (when `band_ok` and the band is form-valid), then its task id (when it
        matches ID_NUM_RE) -- the band applies before that line's own id is judged."""
        if band_ok:
            band = id_band_of(obj)[0]
            if band is not None:
                self.add_band(band)
        tid = obj.get("task_id") if isinstance(obj, dict) else None
        m = ID_NUM_RE.match(tid) if isinstance(tid, str) else None
        if m:
            self.ids.add(int(m.group(1)))

    def issuable(self):
        """(main, {Band: next id | None}). `main`: one above the max over the ids NOT inside a closed band and
        over every open band's `lo - 1`; while it lies inside a closed band it jumps to that band's end + 1.
        A closed band's next id is the max of the ids inside it + 1, or its `lo` when it has none; None once
        that passes its end (used up)."""
        floor = max([n for n in self.ids if not self._inside(n)] + [lo - 1 for lo in self.opens] + [0])
        main = floor + 1
        moved = True
        while moved:
            moved = False
            for b in self.closed:
                if b.lo <= main <= b.hi:
                    main = b.hi + 1
                    moved = True
        bands = {}
        for b in self.closed:
            inside = [n for n in self.ids if b.lo <= n <= b.hi]
            nxt = max(inside) + 1 if inside else b.lo
            bands[b] = nxt if nxt <= b.hi else None
        return main, bands

    def has_closed(self, band) -> bool:
        """Is `band` (a Band) already one of the declared closed bands? A line that repeats a declared band is a
        REFERENCE to it (the line is issued from that band), not a new declaration: it is never judged BELOW."""
        return band is not None and band.hi is not None and any((b.lo, b.hi) == (band.lo, band.hi) for b in self.closed)

    def band_around(self, n: int):
        """The declared closed band that holds the id `n`, or None (the first one declared)."""
        return next((b for b in self.closed if b.lo <= n <= b.hi), None)

    def may_issue(self, n: int, own_band=None) -> bool:
        """THE one predicate of "who may take which brand-new id" (rule 9a/9e): `n` is the file's own next id, OR it
        is the next id of the closed band that the issuing line carries in ITS OWN `id_band` (`own_band`, a Band
        already in this state) and that band is not used up. The next id of a band the line does not carry is
        never issuable by it: a writer that took max+1 and landed on a band's id does not own the band."""
        main, bands = self.issuable()
        if n == main:
            return True
        if own_band is None or own_band.hi is None:
            return False
        return any(nxt == n for b, nxt in bands.items() if (b.lo, b.hi) == (own_band.lo, own_band.hi) and nxt is not None)

    def suggested(self):
        """(s, s + 49): the band a second writer is told to open, from suggested_band(top)."""
        s = suggested_band(self.top)
        return s, s + 49


def next_ids(objs) -> NextIds:
    """A BandState fed over `objs` (journal line objects, bands taken as written), read once."""
    state = BandState()
    for obj in objs:
        state.add(obj)
    main, bands = state.issuable()
    return NextIds(main, bands, state.top)


def free_bands(state) -> list:
    """[(Band, next id)] of the closed bands that still have a free id, declaration order. `state`: a BandState
    or a NextIds."""
    bands = state.issuable()[1] if isinstance(state, BandState) else state.bands
    return [(b, n) for b, n in bands.items() if n is not None]


def used_up_bands(state) -> list:
    """The closed bands with no free id left, declaration order. `state`: a BandState or a NextIds."""
    bands = state.issuable()[1] if isinstance(state, BandState) else state.bands
    return [b for b, n in bands.items() if n is None]


def band_lines(state) -> list:
    """At most BAND_SHOW_MAX lines `band t-A..t-B: next t-N`: the LATEST-declared closed bands that still have a
    free id, in declaration order. A used-up band is never printed, so the output stays bounded however many
    bands were declared. `state`: a BandState or a NextIds."""
    return [f"band {b.label}: next t-{n:03d}" for b, n in free_bands(state)[-BAND_SHOW_MAX:]]


PEER_CLEAR_SUFFIX = " (possibly this session before /clear)"


def peer_note(peers, state, cleared: bool = False) -> str:
    """The PARALLEL SESSION note (a note, never a refusal): "" with no `peers` ([(stem, age_s)], youngest first,
    transcripts.peer_main_sessions), else one line that tells the session another main session of this project
    is live and how to open a band. At most 3 stems are shown. `state`: a BandState or a NextIds (its `top`).
    `cleared` (SessionStart source "clear"): the youngest file may be this very session's pre-/clear transcript, so
    the note ends with PEER_CLEAR_SUFFIX -- no peer is dropped (an unknown is never hidden)."""
    if not peers:
        return ""
    s = suggested_band(state.top)
    shown = ", ".join(str(stem)[:8] for stem, _age in peers[:3])
    if len(peers) > 3:
        shown += f", +{len(peers) - 3} more"
    return (
        "PARALLEL SESSION (a note, nothing is blocked): another main session of this project wrote its "
        f"transcript {int(peers[0][1]) // 60} min ago ({shown}). Two sessions issuing task ids into one journal "
        "file collide on max+1 (13.11, t-347..t-356); one of you opens a band before its next id: "
        f'id_band: "t-{s:03d}..t-{s + 49:03d}" on every journal line you issue from it (python tools/journal_keys.py '
        "where prints the next ids; CLAUDE.md, Routing log)."
        + (PEER_CLEAR_SUFFIX if cleared else "")
    )


def _objs(lines: list[str]) -> list:
    """[(1-based line number, object)] of the lines that parse into a JSON object."""
    out = []
    for n, line in enumerate(lines, start=1):
        try:
            obj = json.loads(line)
        except (ValueError, TypeError):
            continue
        if isinstance(obj, dict):
            out.append((n, obj))
    return out


def _has_task_id(obj: dict) -> bool:
    tid = obj.get("task_id")
    return isinstance(tid, str) and bool(tid)


# --- keys ----------------------------------------------------------------------------------

class LabeledEvent(dict):
    """A journal event whose FILE is known: `jk_label` is the label its task key carries ("" for
    the history, its declared segments' labels, the successor file; the slug for any other
    writer). An attribute, not a field: a journal line cannot forge it. task_key / ref_key read it
    when present, and fall back to the declaration (segments) for a plain dict -- so a reader that
    holds plain dicts reads exactly as before."""
    __slots__ = ("jk_label",)


def _event_label(obj):
    """The file label a LabeledEvent carries, else None."""
    return getattr(obj, "jk_label", None)


def task_key(obj: dict, segs: Segments):
    """(label, task_id) of a journal event, or None when it carries no task_id. The label is the
    label of the event's file when the event is a LabeledEvent (see load_all), else the declared
    instance the line belongs to, "" for every undeclared line (and always "" under
    NO_SEGMENTS)."""
    if not isinstance(obj, dict) or not _has_task_id(obj):
        return None
    label = _event_label(obj)
    if label is None:
        label = segs.index.get(identity(obj), "")
    return (label, obj["task_id"])


def _carrier_label(carrier_obj, segs: Segments) -> str:
    if not isinstance(carrier_obj, dict):
        return ""
    label = _event_label(carrier_obj)
    if label is not None:
        return label
    ck = task_key(carrier_obj, segs)
    return ck[0] if ck else ""


def ref_key(token: str, carrier_obj, segs: Segments, label_ids=None, aliases=()):
    """The key a `closes:`-style token names, or None when the token is not t-NNN[@label].
    `t-NNN@label` is explicit: (label, t-NNN) -- a label that no segment and no file holds is a key
    that matches nothing, so such a token closes nothing; `main` and the slug of the successor file
    (`aliases`) are other names of the label "". A bare `t-NNN` resolves by the carrier's label
    when that label's segment or file holds the id (`segs.ids`, `label_ids`: label -> the task ids
    of that file), else "" (the carrier with no task_id, or one of the undeclared side, names the
    bare id: a token never serves another writer's task unless it names that writer)."""
    m = REF_RE.match(token) if isinstance(token, str) else None
    if m is None:
        return None
    tid, label = m.group(1), m.group(2)
    if label:
        if label == MAIN_LABEL or label in aliases:
            label = ""
        return (label, tid)
    carrier_label = _carrier_label(carrier_obj, segs)
    if carrier_label and (tid in segs.ids.get(carrier_label, ())
                          or tid in (label_ids or {}).get(carrier_label, ())):
        return (carrier_label, tid)
    return ("", tid)


def display(key) -> str:
    """t-007 for the undeclared instance, t-007@codex-fixes for a declared one."""
    label, tid = key
    return f"{tid}@{label}" if label else tid


# --- the declaration file ------------------------------------------------------------------

def parse_declaration(text: str):
    """(Segments, None) when `text` is a declaration of the right SHAPE, else (None, reason).
    Shape only: the semantic problems (label, version, why, the listing against the journal) are
    check()'s, so there is one place that names them."""
    try:
        data = json.loads(text)
    except (ValueError, TypeError) as e:
        return None, f"not valid JSON ({e})"
    if not isinstance(data, dict):
        return None, "the top level is not an object"
    if "version" not in data or "segments" not in data:
        return None, "the object needs `version` and `segments`"
    raw = data["segments"]
    if not isinstance(raw, list):
        return None, "`segments` is not a list"
    segments = []
    for i, seg in enumerate(raw, start=1):
        if not isinstance(seg, dict):
            return None, f"segment {i} is not an object"
        label, why, lines = seg.get("label"), seg.get("why"), seg.get("lines")
        if not isinstance(label, str) or not isinstance(why, str) or not isinstance(lines, list):
            return None, f"segment {i} needs a string `label`, a string `why` and a list `lines`"
        idents = []
        for j, ident in enumerate(lines, start=1):
            if (not isinstance(ident, list) or len(ident) != len(IDENTITY_FIELDS)
                    or not all(isinstance(x, str) for x in ident)):
                return None, (f"segment {i} line entry {j} is not a list of {len(IDENTITY_FIELDS)} "
                              f"strings ({', '.join(IDENTITY_FIELDS)})")
            idents.append(tuple(ident))
        segments.append((label, why, tuple(idents)))
    version = data["version"]
    if isinstance(version, bool) or not isinstance(version, int):
        return None, f"`version` is {version!r}, expected the integer {VERSION}"
    return Segments(version, segments), None


def check(lines: list[str], segs: Segments) -> list[str]:
    """Every problem of the declaration against the journal `lines` (raw text lines); [] = fine.
    Problems: an unknown version; a bad or duplicate label; an empty `why`; an identity that
    matches 0 journal lines or a different number of lines than it is listed; an identity listed
    by two segments; a declared task id with no undeclared line (nothing would tell the instances
    apart); a declared key (either side) whose first line in file order is not `delegated`."""
    problems: list[str] = []
    if segs.version != VERSION:
        problems.append(f"unknown version {segs.version!r} (this reader knows version {VERSION})")
    seen_labels: set = set()
    for label, why, _lines in segs.segments:
        if not LABEL_RE.match(label):
            problems.append(f"label {label!r} is not 1-24 characters of [a-z0-9-]")
        if label in seen_labels:
            problems.append(f"label {label!r} is declared twice")
        seen_labels.add(label)
        if not why.strip():
            problems.append(f"segment {label!r} has an empty `why`")
    objs = _objs(lines)
    matched = Counter(identity(o) for _n, o in objs if _has_task_id(o))
    for ident, n in segs.listed.items():
        m = matched.get(ident, 0)
        if m == 0:
            problems.append(f"identity {list(ident)} matches 0 journal lines")
        elif m != n:
            problems.append(f"identity {list(ident)} is listed {n} time(s) but matches {m} journal line(s)")
    owners: dict = {}
    for label, _why, idents in segs.segments:
        for ident in set(idents):
            owners.setdefault(ident, []).append(label)
    for ident, labels in owners.items():
        if len(labels) > 1:
            problems.append(f"identity {list(ident)} is listed by more than one segment ({', '.join(labels)})")
    declared_ids = {ident[1] for ident in segs.listed}
    undeclared_ids = {o["task_id"] for _n, o in objs if _has_task_id(o) and identity(o) not in segs.listed}
    for tid in sorted(declared_ids - undeclared_ids):
        problems.append(f"task id {tid} is declared but has no undeclared line -- the declaration "
                        "must leave one instance undeclared, or nothing tells the instances apart")
    first_event: dict = {}
    for _n, o in objs:
        if _has_task_id(o) and o["task_id"] in declared_ids:
            key = task_key(o, segs)
            first_event.setdefault(key, o.get("event"))
    for key in sorted(first_event):
        if first_event[key] != "delegated":
            problems.append(f"the first line of key {display(key)} is {first_event[key]!r}, not 'delegated' -- "
                            "a declared instance must start with its own dispatch")
    return problems


def load_segments(journal_path):
    """(segments, reason): the declaration beside `journal_path` (logs/journal-segments.json next
    to logs/routing-log.jsonl), validated against that journal. NEVER raises: an absent file is
    (NO_SEGMENTS, None); any exception, unreadable bytes, wrong shape or failing check is
    (NO_SEGMENTS, reason) -- all or nothing, a partial declaration is never applied. The fallback
    errs toward glue (colliding ids read as one task), which is today's reading."""
    try:
        jp = Path(journal_path)
        dp = jp.parent / SEGMENTS_NAME
        if not dp.exists():
            return NO_SEGMENTS, None
        text = dp.read_text(encoding="utf-8")
        segs, why = parse_declaration(text)
        if segs is None:
            return NO_SEGMENTS, why
        journal = jp.read_text(encoding="utf-8", errors="replace")
        problems = check(split_lines(journal), segs)
        if problems:
            return NO_SEGMENTS, _problems_text(problems)
        return segs, None
    except Exception as e:  # noqa: BLE001 -- the contract: a reader never fails on this file
        return NO_SEGMENTS, f"{type(e).__name__}: {e}"


def _problems_text(problems: list[str]) -> str:
    shown = "; ".join(problems[:MAX_PROBLEMS_SHOWN])
    more = len(problems) - MAX_PROBLEMS_SHOWN
    return shown + (f"; and {more} more" if more > 0 else "")


def summary(segs: Segments) -> str:
    n_lines = sum(len(lines) for _l, _w, lines in segs.segments)
    ids = {ident[1] for _l, _w, lines in segs.segments for ident in lines}
    names = ", ".join(segs.labels)
    count = len(segs.segments)
    return f"{count} segment{'s' if count != 1 else ''} ({names}), {n_lines} lines, {len(ids)} task ids"


def dumps_declaration(segs: Segments) -> str:
    """The file text: valid JSON, one identity per line (a diff of a declaration is readable)."""
    out = ["{", f'  "version": {json.dumps(segs.version)},', '  "segments": [']
    for si, (label, why, lines) in enumerate(segs.segments):
        out.append("    {")
        out.append(f'      "label": {json.dumps(label, ensure_ascii=False)},')
        out.append(f'      "why": {json.dumps(why, ensure_ascii=False)},')
        out.append('      "lines": [')
        for li, ident in enumerate(lines):
            comma = "," if li < len(lines) - 1 else ""
            out.append("        " + json.dumps(list(ident), ensure_ascii=False) + comma)
        out.append("      ]")
        out.append("    }" + ("," if si < len(segs.segments) - 1 else ""))
    out.append("  ]")
    out.append("}")
    return "\n".join(out) + "\n"


# --- one file per writer (t-581, F0-4) ---------------------------------------------------------

class NameProblem(str):
    """The text of a naming problem; `paths` = the repository paths it is about (so a gate can
    tell a problem of a staged file from one that was already there)."""
    paths: tuple = ()

    def __new__(cls, text, paths=()):
        obj = super().__new__(cls, text)
        obj.paths = tuple(paths)
        return obj


@dataclass
class JournalFile:
    """One journal file: `path` relative to the repository (forward slashes), `slug` and `label`
    (the file's own label; for a successor the label of its ROWS is "" -- see Row.label),
    `successor` = its line 1 is a journal_created with `continues` = the history."""
    path: str
    slug: str
    label: str
    successor: bool = False


def _norm_rel(path) -> str:
    return str(path).replace("\\", "/")


def journal_names(paths, segment_labels=()):
    """(files, problems) of a list of repository paths. PURE: the disk, the git index and a git
    tree all feed it. Only a direct child `logs/journal/<name>.jsonl` is a journal file; anything
    else (nested paths, other extensions, the history) is neither returned nor mentioned. A file
    whose name is not a legal slug (SLUG_RE, lower-case `.jsonl`), is reserved (`main`), equals a
    segment label, or repeats another file's slug after casefold is a PROBLEM and is not returned
    in `files`. problems are NameProblem texts."""
    files, problems = [], []
    labels = {str(l).casefold() for l in segment_labels}
    seen: dict = {}
    for raw in paths:
        p = _norm_rel(raw)
        parts = p.split("/")
        if len(parts) != 3 or parts[0] != "logs" or parts[1] != "journal":
            continue
        name = parts[2]
        if not name.casefold().endswith(".jsonl"):
            continue
        stem = name[:-len(".jsonl")]
        bad = None
        if not name.endswith(".jsonl"):
            bad = "the extension must be lower-case `.jsonl`"
        elif not SLUG_RE.match(stem):
            bad = ("the name is not a legal developer slug (2-24 characters of [a-z0-9-], starting "
                   "with a letter)")
        elif stem.casefold() in RESERVED_LABELS:
            bad = f"`{stem}` is reserved for the history and its successor"
        elif stem.casefold() in labels:
            bad = f"`{stem}` is already the label of a declared segment in {SEGMENTS_REL}"
        if bad:
            problems.append(NameProblem(
                f"journal file {p} cannot be a journal file: {bad} -- rename it to "
                f"{JOURNAL_DIR_REL}/<slug>.jsonl with the writer's slug, or remove it", (p,)))
        key = stem.casefold()
        if key in seen:
            problems.append(NameProblem(
                f"journal files {seen[key]} and {p} have the same slug after case folding -- two "
                "writers cannot share a label; give each clone its own slug", (seen[key], p)))
        else:
            seen[key] = p
        if not bad:
            files.append(JournalFile(p, stem, stem))
    files.sort(key=lambda f: f.path)
    return files, problems


def _declared_labels(root: Path) -> list:
    """The labels in root/logs/journal-segments.json, read leniently (shape-only); [] on any
    failure. A slug that equals one must be refused even when the declaration is otherwise
    broken, so this does not go through check()."""
    try:
        data = json.loads((Path(root) / SEGMENTS_REL).read_text(encoding="utf-8"))
        return [s["label"] for s in data["segments"] if isinstance(s, dict) and isinstance(s.get("label"), str)]
    except Exception:  # noqa: BLE001 -- lenient on purpose
        return []


_DEV_DOOR = ("set `developer: <slug>` in tools/dev.config.yaml (an untracked file, one per clone; "
             "template tools/dev.config.example.yaml; a slug is 2-24 characters of [a-z0-9-], starting "
             "with a letter, not `main`, not a segment label)")


def developer_slug(root):
    """(slug, None) when tools/dev.config.yaml of `root` names a legal developer slug, else
    (None, reason-with-a-door). The file is parsed by tools/dev_config.py, the ONE reader of it
    (grammar, BOM, CRLF, comments, quotes, a duplicate or an indented key, SLUG_RE, the reserved
    `main`); this function adds the one check that is the journal's own, a slug equal to a segment
    label of logs/journal-segments.json. It reads exactly root/tools/dev.config.yaml: the
    QA_DEV_CONFIG door of dev_config is not followed, so a root never answers with another file's
    slug. NEVER raises. Direction of the error (the function is the base of the freeze and
    one-writer refusals): None -- `main`, upper case, a length outside 2-24, a segment label, an
    unreadable or refused file all give None, never a path."""
    try:
        path = Path(root) / DEV_CONFIG_REL
        if not path.is_file():
            return None, f"{DEV_CONFIG_REL} cannot be read (no such file in {root}) -- {_DEV_DOOR}"
        slug, why = dev_config.developer_slug(path=path)
        if slug is None:
            return None, f"{why} -- {_DEV_DOOR}"
        if slug.casefold() in {l.casefold() for l in _declared_labels(Path(root))}:
            return None, f"{DEV_CONFIG_REL}: the slug {slug[:40]!r} is a segment label of {SEGMENTS_REL} -- {_DEV_DOOR}"
        return slug, None
    except Exception as e:  # noqa: BLE001 -- the contract: never raises
        return None, f"{DEV_CONFIG_REL} could not be read ({type(e).__name__}) -- {_DEV_DOOR}"


def disk_journal_files(root) -> list:
    """The JournalFile list (legal names only) of root/logs/journal on DISK. Never raises."""
    try:
        names = [f"{JOURNAL_DIR_REL}/{e.name}" for e in os.scandir(Path(root) / JOURNAL_DIR_REL) if e.is_file()]
    except OSError:
        return []
    return journal_names(names, _declared_labels(root))[0]


def current_path(root):
    """(rel, reason): the one answer to "which file does this clone write its journal lines to".
    BEFORE the switch (no legal journal file on disk, the history file present) it is the
    history, logs/routing-log.jsonl.
    AFTER it: logs/journal/<slug>.jsonl for the clone's developer slug (reason = a note when the
    file does not exist yet), or (None, reason-with-a-door) when the slug is missing or wrong --
    the history takes no new lines after the switch, so there is nowhere else to write.
    A tree with NEITHER a journal file NOR the history file (a fresh repository after the
    github-move, FK-14: the history stays in the old repository's bundle) is on the AFTER side:
    its first line goes to its own file, never into a history that does not exist there (a
    session that wrote it would revive a world that ended before t-581). Never raises."""
    try:
        if not disk_journal_files(root) and (Path(root) / HISTORY_REL).exists():
            return HISTORY_REL, None
        slug, why = developer_slug(root)
        if slug is None:
            return None, why
        rel = f"{JOURNAL_DIR_REL}/{slug}.jsonl"
        if not (Path(root) / rel).exists():
            return rel, f"{rel} does not exist yet -- its first line is a journal_created"
        return rel, None
    except Exception as e:  # noqa: BLE001
        return None, f"cannot decide where to write ({type(e).__name__}) -- {_DEV_DOOR}"


@dataclass
class Row:
    """One non-blank journal line. `path`: the file (repository-relative); `file_label`: the
    file's own label ("" for the history, the slug of a developer file); `label`: the label the
    task key carries ("" for the history's undeclared lines and the successor's lines, a declared
    segment's label, or the slug); `obj`: the parsed object (a LabeledEvent) or None with `error`
    set; `key`: (label, task_id) or None."""
    path: str
    file_label: str
    label: str
    line_no: int
    raw: str
    obj: object
    error: object
    key: object


@dataclass
class Journal:
    """Everything load_all read. rows: all rows in the merged order (see load_all)."""
    root: Path
    rows: list = field(default_factory=list)
    files: list = field(default_factory=list)
    problems: list = field(default_factory=list)
    segments: object = NO_SEGMENTS
    segments_reason: object = None
    successor_slug: object = None
    label_ids: dict = field(default_factory=dict)
    known_labels: set = field(default_factory=set)
    _by_path: dict = field(default_factory=dict)

    @property
    def aliases(self) -> frozenset:
        """The names, other than "", of the label "": `main` and the successor's slug."""
        return frozenset({MAIN_LABEL} | ({self.successor_slug} if self.successor_slug else set()))

    def rows_of(self, path) -> list:
        return list(self._by_path.get(_norm_rel(path), ()))

    def writer_label(self, slug) -> str:
        """The label the task keys of writer `slug` carry: "" for the successor, else the slug."""
        return "" if slug is not None and slug == self.successor_slug else (slug or "")

    def logical(self, label) -> list:
        """The rows of the LOGICAL journal `label`: for "" / `main` / the successor's slug the
        history followed by the successor file; for another slug that writer's file; for a
        declared segment label the rows carrying it."""
        if label in ("", MAIN_LABEL) or (self.successor_slug and label == self.successor_slug):
            out = self.rows_of(HISTORY_REL)
            if self.successor_slug:
                out += self.rows_of(f"{JOURNAL_DIR_REL}/{self.successor_slug}.jsonl")
            return out
        own = self.rows_of(f"{JOURNAL_DIR_REL}/{label}.jsonl")
        return own or [r for r in self.rows if r.label == label]

    def events(self, rows=None) -> list:
        """The LabeledEvent objects of `rows` (default: all), in that order; unparsable rows are
        skipped."""
        return [r.obj for r in (self.rows if rows is None else rows) if r.obj is not None]

    def next_free_id(self, label) -> str:
        """t-NNN = the next id of the file's own sequence of the logical journal `label`, in the journal's own
        width: max(t-NNN) + 1, where an open band raises the max and a closed band is skipped (rule 9e;
        `next_ids`). With no band in the journal it is max + 1, as before."""
        return f"t-{next_ids(r.obj for r in self.logical(label) if r.obj is not None).main:03d}"

    def band_state(self, label) -> BandState:
        """The BandState of the logical journal `label` (what next_free_id reads), for the readers that also
        print the bands (compact_snapshot)."""
        state = BandState()
        for r in self.logical(label):
            if r.obj is not None:
                state.add(r.obj)
        return state

    def last_ts(self, label):
        """The ts of the last row of the logical journal `label` that has a string ts, else None."""
        for r in reversed(self.logical(label)):
            if r.obj is not None and isinstance(r.obj.get("ts"), str):
                return r.obj["ts"]
        return None

    def resolve_ref(self, token, row):
        """The key a `closes:`-style token (or a `ref`) written on `row` names (None for a token
        that is not t-NNN[@label]). `@label` is explicit (`main` and the successor's slug are the
        label ""; a label no file and no segment holds matches nothing); a bare token is the
        carrier file's own task when that file holds the id, else the task of "" (main) -- never
        another writer's. See ref_key."""
        return ref_key(token, row.obj if row.obj is not None else _bare_carrier(row.label),
                       self.segments, self.label_ids, self.aliases)


def _bare_carrier(label):
    ev = LabeledEvent()
    ev.jk_label = label
    return ev


def _row_lines(text: str):
    """[(1-based line number, line)] of the non-blank lines of `text`, one trailing CR stripped."""
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    out = []
    for n, line in enumerate(lines, start=1):
        if line.endswith("\r"):
            line = line[:-1]
        if line.strip():
            out.append((n, line))
    return out


def continues_value(text: str):
    """The `continues` value on physical line 1 of a journal text (None when absent or when line 1
    is not a JSON object)."""
    first = (text or "").split("\n", 1)[0].rstrip("\r")
    try:
        obj = json.loads(first)
    except (ValueError, TypeError):
        return None
    return obj.get(CONTINUES_FIELD) if isinstance(obj, dict) else None


def load_all(root, *, segments=None) -> Journal:
    """Reads the history and every logs/journal/<slug>.jsonl of `root` into one Journal. NEVER
    raises: an unreadable file, a bad name, two successors, a misplaced `continues` are
    Journal.problems; an unparsable line is a Row with obj None and its error. The segment
    declaration is loaded ONCE (`segments` = a Segments to use instead; it applies to the history
    only). One trailing CR is stripped from every line; blank lines are skipped but the line
    numbers count them.
    ORDER of `rows`: a merge by ts (heapq.merge) of the files, each kept in its own order -- the
    key of a row is (its ts, or the last well-formed ts above it in the same file, "" for the
    first; the file's rank: history, successor, then slugs; line number). INVARIANT: for any file
    the rows of that file appear in file order, even when its ts are not monotonic, so a reader
    that counts by position sees no file permuted."""
    root = Path(root)
    j = Journal(root=root)
    try:
        _load_all_into(j, segments)
    except Exception as e:  # noqa: BLE001 -- the contract: never raises
        j.problems.append(f"the journal could not be loaded completely ({type(e).__name__}: {e})")
    return j


def _read_text(root: Path, rel: str, problems: list):
    try:
        return (root / rel).read_bytes().decode("utf-8", errors="replace")
    except OSError as e:
        problems.append(f"{rel} cannot be read ({type(e).__name__}: {e})")
        return None


def _find_successors(j: Journal, kept: list, texts: dict) -> list:
    """The files whose line 1 carries `continues` = the history; every other use of the field is a
    problem of the Journal."""
    successors = []
    for f in kept:
        for n, line in _row_lines(texts[f.path]):
            try:
                obj = json.loads(line)
            except (ValueError, TypeError):
                continue
            if not isinstance(obj, dict) or CONTINUES_FIELD not in obj:
                continue
            if n != 1:
                j.problems.append(f"{f.path} line {n}: `{CONTINUES_FIELD}` is allowed on line 1 only")
            elif obj[CONTINUES_FIELD] != HISTORY_REL:
                j.problems.append(f"{f.path} line 1: `{CONTINUES_FIELD}` is {str(obj[CONTINUES_FIELD])[:60]!r}, "
                                  f"expected {HISTORY_REL!r}")
            else:
                successors.append(f)
    if len(successors) > 1:
        j.problems.append("more than one journal file continues the history ("
                          + ", ".join(f.path for f in successors)
                          + ") -- only one file can; none of them is treated as its continuation")
        return []
    return successors


def _file_rows(rel: str, text: str, file_label: str, label_of, rank_key):
    """([Row], [(merge key, Row)]) of one file. `label_of(parsed_obj)` = the label of a row."""
    rows, stream = [], []
    last_ts = ""
    for n, line in _row_lines(text):
        obj, error = None, None
        try:
            parsed = json.loads(line)
        except (ValueError, TypeError, RecursionError) as e:
            error = f"invalid JSON ({e})"
        else:
            if isinstance(parsed, dict):
                obj = LabeledEvent(parsed)
            else:
                error = "not a JSON object"
        if obj is not None:
            label = label_of(parsed)
            obj.jk_label = label
            key = (label, obj["task_id"]) if _has_task_id(obj) else None
            ts = obj.get("ts")
            if isinstance(ts, str) and _TS_SHAPE_RE.match(ts):
                last_ts = ts
        else:
            label, key = label_of(None), None
        row = Row(rel, file_label, label, n, line, obj, error, key)
        rows.append(row)
        stream.append(((last_ts, rank_key, n), row))
    return rows, stream


def _load_all_into(j: Journal, segments) -> None:
    root = j.root
    history = root / HISTORY_REL
    has_history = history.is_file()
    if segments is not None:
        segs, why = segments, None
    elif has_history:
        segs, why = load_segments(history)
    else:
        segs, why = NO_SEGMENTS, None
    j.segments, j.segments_reason = segs, why
    try:
        listing = [f"{JOURNAL_DIR_REL}/{e.name}" for e in os.scandir(root / JOURNAL_DIR_REL) if e.is_file()]
    except OSError:
        listing = []
    files, name_problems = journal_names(listing, segs.labels)
    j.problems.extend(str(p) for p in name_problems)

    texts: dict = {}
    if has_history:
        t = _read_text(root, HISTORY_REL, j.problems)
        if t is not None:
            texts[HISTORY_REL] = t
    kept = []
    for f in files:
        t = _read_text(root, f.path, j.problems)
        if t is not None:
            texts[f.path] = t
            kept.append(f)
    successors = _find_successors(j, kept, texts)
    if successors:
        successors[0].successor = True
        j.successor_slug = successors[0].slug
    j.files = kept

    streams = []
    if HISTORY_REL in texts:
        rows, stream = _file_rows(HISTORY_REL, texts[HISTORY_REL], "",
                                  lambda p: segs.index.get(identity(p), "") if p is not None else "", (0, ""))
        j._by_path[HISTORY_REL] = rows
        streams.append(stream)
    for f in kept:
        label = "" if f.successor else f.slug
        rows, stream = _file_rows(f.path, texts[f.path], f.slug, lambda _p, label=label: label,
                                  (1 if f.successor else 2, f.slug))
        j._by_path[f.path] = rows
        streams.append(stream)
    j.rows = [row for _k, row in heapq.merge(*streams, key=lambda t: t[0])]

    for r in j.rows:
        if r.key is not None:
            j.label_ids.setdefault(r.key[0], set()).add(r.key[1])
    j.known_labels = {"", MAIN_LABEL} | set(segs.labels) | {f.slug for f in kept}


# --- CLI -----------------------------------------------------------------------------------

def _default_paths(journal: str | None):
    root = Path(__file__).resolve().parent.parent
    jp = Path(journal) if journal else root / JOURNAL_REL
    return jp, jp.parent / SEGMENTS_NAME


def _parse_range(text: str):
    m = re.fullmatch(r"(\d+)-(\d+)", text.strip())
    if not m:
        return None
    return int(m.group(1)), int(m.group(2))


def cmd_declare(journal_path: Path, segments_path: Path, label: str, lines_arg: str, why: str) -> int:
    if not why.strip():
        print("journal_keys declare: --why is empty -- say where the numbering collision comes from", file=sys.stderr)
        return 1
    if not LABEL_RE.match(label):
        print(f"journal_keys declare: label {label!r} is not 1-24 characters of [a-z0-9-]", file=sys.stderr)
        return 1
    rng = _parse_range(lines_arg)
    if rng is None or rng[0] < 1 or rng[1] < rng[0]:
        print(f"journal_keys declare: --lines {lines_arg!r} is not A-B with 1 <= A <= B (1-based journal line numbers)",
              file=sys.stderr)
        return 1
    a, b = rng
    try:
        journal_lines = split_lines(journal_path.read_text(encoding="utf-8", errors="replace"))
    except OSError as e:
        print(f"journal_keys declare: cannot read {journal_path}: {e}", file=sys.stderr)
        return 1
    if b > len(journal_lines):
        print(f"journal_keys declare: the range {a}-{b} runs past the end of the journal ({len(journal_lines)} lines)",
              file=sys.stderr)
        return 1
    existing = NO_SEGMENTS
    if segments_path.exists():
        try:
            existing, why_not = parse_declaration(segments_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError) as e:
            existing, why_not = None, str(e)
        if existing is None:
            print(f"journal_keys declare: the existing {segments_path.name} is unreadable ({why_not}) -- fix or remove it first",
                  file=sys.stderr)
            return 1
    idents = [identity(o) for n, o in _objs(journal_lines) if a <= n <= b and _has_task_id(o)]
    if not idents:
        print(f"journal_keys declare: no line with a task_id in lines {a}-{b} -- nothing to declare", file=sys.stderr)
        return 1
    new = Segments(existing.version, list(existing.segments) + [(label, why, tuple(idents))])
    problems = check(journal_lines, new)
    if problems:
        print("journal_keys declare: the declaration would not pass `check`, nothing was written:", file=sys.stderr)
        for p in problems[:20]:
            print(f"  - {p}", file=sys.stderr)
        return 1
    with open(segments_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(dumps_declaration(new))
    ids = {i[1] for i in idents}
    print(f"journal_keys declare: label {label}: {len(idents)} lines, {len(ids)} task ids -> {segments_path.name}")
    return 0


def cmd_check(journal_path: Path, segments_path: Path) -> int:
    if not segments_path.exists():
        print(f"journal_keys check: ok -- no declaration ({segments_path.name} absent)")
        return 0
    try:
        text = segments_path.read_text(encoding="utf-8")
        journal_lines = split_lines(journal_path.read_text(encoding="utf-8", errors="replace"))
    except (OSError, UnicodeDecodeError) as e:
        print(f"journal_keys check: FAIL -- unreadable: {e}", file=sys.stderr)
        return 1
    segs, why = parse_declaration(text)
    if segs is None:
        print(f"journal_keys check: FAIL -- {why}", file=sys.stderr)
        return 1
    problems = check(journal_lines, segs)
    if problems:
        for p in problems:
            print(f"journal_keys check: FAIL -- {p}", file=sys.stderr)
        return 1
    print(f"journal_keys check: ok -- {summary(segs)}")
    return 0


def cmd_where(root: Path) -> int:
    """Prints the file this clone writes its journal lines to, the next free task id and the last
    ts of that writer's logical journal -- from current_path(), the function the hooks use -- then
    (rule 9e) a line `band t-A..t-B: next t-N` for each of the latest 3 closed bands that still have a
    free id, and LAST, always, the band a second writer would open. Exit 1 with the door when there is
    no path to write."""
    rel, why = current_path(root)
    if rel is None:
        print(f"journal_keys where: there is no file to write to -- {why}", file=sys.stderr)
        return 1
    j = load_all(root)
    label = "" if rel == HISTORY_REL else Path(rel).stem
    print(f"write to: {rel}")
    if rel != HISTORY_REL and not (root / rel).exists():
        print(f"next free id: t-001 (the file does not exist yet; with `continues` on line 1 it continues the history: "
              f"{j.next_free_id('')})")
        print("last ts: -")
        s, e = j.band_state("").suggested()      # the file continues the history: its top is the history's
        print(f"suggested band (for a second writer): t-{s:03d}..t-{e:03d}")
        return 0
    state = j.band_state(label)
    print(f"next free id: t-{state.issuable()[0]:03d}")
    print(f"last ts: {j.last_ts(label) or '-'}")
    for line in band_lines(state):
        print(line)
    s, e = state.suggested()
    print(f"suggested band (for a second writer): t-{s:03d}..t-{e:03d}")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="journal_keys", description=__doc__.split("\n")[0])
    ap.add_argument("--journal", default=None, help="the journal path (default logs/routing-log.jsonl of this repository)")
    ap.add_argument("--root", default=None, help="`where`: the repository root (default: the repository of this file)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("where", help="print the file this clone writes to, the next free id and the last ts")
    d = sub.add_parser("declare", help="declare the lines A-B of the journal as a foreign instance")
    d.add_argument("--label", required=True)
    d.add_argument("--lines", required=True, help="A-B, 1-based, inclusive")
    d.add_argument("--why", required=True)
    sub.add_parser("check", help="validate logs/journal-segments.json against the journal")
    args = ap.parse_args(argv)
    if args.cmd == "where":
        return cmd_where(Path(args.root) if args.root else Path(__file__).resolve().parent.parent)
    jp, sp = _default_paths(args.journal)
    if args.cmd == "declare":
        return cmd_declare(jp, sp, args.label, args.lines, args.why)
    return cmd_check(jp, sp)


if __name__ == "__main__":
    sys.exit(main())
