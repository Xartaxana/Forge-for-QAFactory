"""Claude Code transcript telemetry (Delegated Task 5): the operator's
real Lead is the Claude Code subscription, and Claude Code session
transcripts are a first-class real-traffic telemetry source alongside
any gateway log; subscription usage is accounted at API list prices
(a subscription is a cash discount, not a cost of zero).

Reads Claude Code session transcripts (~/.claude/projects/*/*.jsonl --
one file per session; the directory name encodes the project path),
normalizes each assistant API turn into a row in a NEW `cc_usage`
table in the gateway SQLite database (the existing `requests` table,
used by the API-contour gateway, is untouched), and prints a Ledger-
style usage report (tokens, accounted cost, cache economics) roughly
matching gateway/metrics.py's style.

PRIVACY (unified plan section 5): this script reads only
`message.model` / `message.usage` and session/turn metadata. It never
reads message content, tool inputs/outputs, or any prompt text, and
writes none to the database or to reports.

Empirical findings (observed empirically across real transcripts, see
CURRENT_CONTEXT.md "Delegated Task 5" for detail):

- One assistant API turn can appear as MULTIPLE JSONL lines sharing
  the same `requestId` (each with an identical `message.usage` block)
  -- observed when a single response contains several content blocks
  (e.g. multiple tool_use calls). `uuid` is unique per LINE, not per
  turn, so it is the wrong dedupe key: dedupe by `requestId` (first
  occurrence wins) or the API's true row identity would be inflated
  by a large factor (hundreds of duplicate-requestId groups found in
  a single project's transcripts alone).
- `message.model == "<synthetic>"` rows are harness-internal
  rate-limit notices ("You've hit your session limit..."), always
  carrying all-zero usage. Skipped per spec.
- No `isSidechain: true` assistant rows exist anywhere among the
  TOP-LEVEL `<project>/*.jsonl` transcripts observed in a live
  deployment (0 of tens of thousands checked), but the column is
  populated regardless since subagent traffic is real traffic that
  must stay distinguishable (Lead clarification, item 2 of the spec).
  Sidechain traffic DOES exist, just not in that glob -- see Delegated
  Task 6 below.
- Non-assistant line `type`s observed: user, ai-title, last-prompt,
  queue-operation, system, mode, permission-mode, file-history-
  snapshot, pr-link, attachment. None carry a `usage` field; all are
  skipped (only `type == "assistant"` is read).

Delegated Task 6 (follow-up): subagent/sidechain transcripts live at
a SECOND, deeper path --
`<project>/<session-id>/subagents/agent-*.jsonl` -- one file per
dispatched subagent, invisible to the original single glob above.
Re-verified empirically across dozens of such files (thousands of
assistant lines total) before wiring in the second glob:
- every line's `sessionId` JSON field equals the PARENT session's
  UUID (the `<session-id>` directory name one level above
  `subagents/`), 0 mismatches -- so these files' turns correctly
  attach to their parent session, not a synthetic "subagents"
  session.
- `isSidechain` is true on all of them.
- `requestId` is present on all of them (0 missing; the uuid
  fallback below remains untested on real data but is kept for the
  same defensive reason as the top-level case).
- `agentId` is present on all of them. `promptId` was NOT found on
  any of the lines checked, despite being listed as an expected extra
  field in the spec -- noted here since it contradicts that
  assumption; harmless either way since neither field is read.
- No `dedupe_key` (session_id + requestId) collisions were found
  between a parent session's own turns and its subagents' turns, nor
  between sibling subagent files of the same session (checked across
  every session observed that has a subagents/ directory).

Delegated Task 7 (follow-up): agent attribution + haiku pricing gaps
closed. Re-verified empirically across dozens of subagent files
(thousands of lines total, thousands of assistant lines) before
wiring in the two new columns:
- `agentId` is a per-line top-level field on EVERY line of a subagent
  file (assistant and non-assistant alike; all lines checked) --
  confirms the module docstring's earlier claim and gives a stable
  per-row agent identity key.
- `agentType` (the human-readable subagent slug, e.g.
  "test-maintainer") does NOT appear anywhere as a literal JSON key on
  any of the lines checked -- contradicts the Task 6 report's
  phrasing ("agentType: test-maintainer"), which turns out to have
  been describing a value, not a literal key. The literal key holding
  that exact value is `attributionAgent`, present as a TOP-LEVEL field
  on nearly all assistant lines (the handful missing are all
  `model == "<synthetic>"` harness stop-sequence lines, already
  skipped by SKIP_MODELS regardless). Every agentId maps to exactly
  one attributionAgent value across all files checked (0 files with a
  varying value) -- confirmed identical to the *sidecar*
  `agent-<id>.meta.json` file's own `agentType` field (spot-checked:
  an example agent's meta.json says `"agentType":"example-agent"`,
  and every assistant line in that same agent's .jsonl carries
  `"attributionAgent":"example-agent"`) -- so `attributionAgent` is
  the reliable, per-line, no-extra-file-read source used for the new
  `agent_type` column below. The .meta.json sidecars (one per
  subagent file, holding agentType/description/toolUseId/spawnDepth)
  are session-level metadata files, NOT matched by any existing
  transcript glob, and are intentionally left unread --
  `attributionAgent` already gives the same value per-line.
- Top-level (non-subagent) transcript lines carry neither `agentId`
  nor `attributionAgent`; both new columns are NULL there, as
  expected.
- A model id may appear in the gateway log but never in transcripts
  -- its rows fall back to NULL pricing (observed empirically with a
  haiku-tier model id's accounted_cost_usd before this task's pricing
  fix).

Recursive subagent transcript depth (regression follow-up): subagent
transcripts can also appear NESTED further below subagents/ -- e.g. a
workflow tool that groups its agent transcripts under an extra
subagents/workflows/wf_*/ layer. The original one-directory-deep glob
(subagents/*.jsonl) and the "immediate parent == subagents" check in
iter_assistant_turns() both silently miss any such deeper nesting -- a
silent undercount, not an error, since a file the glob never matches
simply contributes zero rows without complaint. Fixed by widening the
glob to subagents/**/*.jsonl (glob.glob(..., recursive=True)) and by
walking UP the path's parents in iter_assistant_turns() to find the
nearest ancestor literally named "subagents", instead of checking only
the immediate parent -- both changes are depth-agnostic, so any future
nesting under subagents/ is covered automatically, not just one extra
level. Any sidecar file the wider glob also matches (e.g. a workflow
tool's own journal/metadata file) stays inert: iter_assistant_turns()
already skips every line whose `type` isn't "assistant" before it ever
looks at `usage`, so a file with no assistant/usage lines simply
yields zero rows, not an error.

Split-turn output_tokens correction (regression follow-up): the
earlier claim above that split lines sharing one requestId always
carry an IDENTICAL `message.usage` block turns out to hold only for
MAIN-CHAIN turns (first line byte-identical to last). For SUBAGENT/
SIDECHAIN turns, input/cache token counts still match across the split
lines, but `output_tokens` is a small PLACEHOLDER value on every line
except the one that carries the real total -- so deduping by
first-occurrence systematically threw away most of the real output
token count for subagent traffic.

Fixed first by switching the importer's dedupe from first-occurrence-
wins to last-occurrence-wins. That fix was itself wrong: the same
dedupe_key (session_id + requestId) can also collide BETWEEN two
sibling subagent files under one session's subagents/ directory, not
only between split lines of a single file. Since import_transcripts()
visits files in `sorted(paths)` order, "last occurrence" tracks glob/
filename sort order, not which file actually holds the real value --
so last-wins can pick a later-sorting file's placeholder over an
earlier file's real number, an outright regression versus even
first-wins for that specific collision shape.

Fixed instead by tie-breaking on VALUE rather than visit order: for a
given dedupe_key, `output_tokens` (and `accounted_cost_usd`,
recomputed from it together with the row's input/cache tokens, which
are identical across colliding lines/files) is only ever UPDATEd when
the newly-seen line's `output_tokens` is STRICTLY GREATER than what is
already stored (MAX-wins). Because a placeholder is always small and
the real value is always the largest number seen for a given
dedupe_key -- true both for split lines within one file and for
cross-file collisions -- taking the max is correct regardless of file
iteration order, line order within a file, or how many times the
importer is re-run: the outcome for a given dedupe_key becomes a pure
function of the SET of lines sharing it, not of the order they are
visited in. `agent_id`/`agent_type` keep their original COALESCE
(fill-if-still-NULL) semantics, unaffected by this change -- those
fields have no placeholder-vs-real split, so a max/order-independent
rule would be pointless for them.

RE-RUNNING the importer over history (no separate migration script) is
how already-persisted rows with a too-low `output_tokens` get
corrected -- the same mechanism that already backfills agent_id/
agent_type for older rows now also backfills correct output_tokens/
cost for rows imported before this fix.
"""

import argparse
import glob
import json
import math
import os
import sqlite3
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import NamedTuple

# A DIRECT sibling import (the reason is written in savings_report.py): the join of the lines of one request is
# transcripts.request_parts, the one reader of it (forge/6 F6-15, F6-23).
_TOOLS_DIR = Path(__file__).resolve().parent
if str(_TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(_TOOLS_DIR))
import transcripts  # noqa: E402

SCHEMA = """
CREATE TABLE IF NOT EXISTS cc_usage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ts TEXT NOT NULL,
    project TEXT NOT NULL,
    session_id TEXT NOT NULL,
    turn_index INTEGER NOT NULL,
    model TEXT NOT NULL,
    input_tokens INTEGER NOT NULL,
    output_tokens INTEGER NOT NULL,
    cache_creation_tokens INTEGER NOT NULL,
    cache_read_tokens INTEGER NOT NULL,
    accounted_cost_usd REAL,
    traffic_kind TEXT NOT NULL DEFAULT 'real',
    is_sidechain INTEGER NOT NULL DEFAULT 0,
    agent_id TEXT,
    agent_type TEXT,
    cache_creation_1h_tokens INTEGER,
    dedupe_key TEXT NOT NULL UNIQUE
);
"""

# F6-24: the part of cache_creation_tokens written with the 1-hour TTL
# (transcript usage.cache_creation.ephemeral_1h_input_tokens); the rest is
# the 5-minute write. NULL = the transcript line carried no split (priced
# as a 5-minute write). A FRESH database gets the column from SCHEMA; an
# EXISTING one gets it from _connect()'s additive ALTER loop (_ADDED_COLUMNS),
# the one schema migrator, on the next import -- which also fills the old rows
# by request id from the transcripts. A database never imported since then
# (read by build_report / token_usage_stats) has no column: `_has_1h_column`.
_CACHE_1H_COLUMN = "cache_creation_1h_tokens"
ESTIMATE_CACHE_WRITES_LINE = (
    "estimate: cache writes priced as 5-minute writes for {n} turn(s) with no 1-hour/5-minute split"
    " in the usage data (a 1-hour write costs more)"
)

# agent_id / agent_type (Delegated Task 7): nullable, populated only for
# subagent/sidechain rows (see module docstring for the empirical
# source of each -- `agentId` and `attributionAgent` respectively,
# both top-level JSONL fields). NULL on every top-level/non-subagent
# row, which is the correct "not applicable" value, not a missing-data
# bug.

# Columns added after the first schema, with their SQLite types, for the
# ALTER TABLE migration in _connect() (existing databases predate them;
# SCHEMA above is CREATE TABLE IF NOT EXISTS so it never retrofits an
# already-existing table): agent_id / agent_type (Delegated Task 7) and the
# 1-hour cache-write split (F6-24). A nullable ADD COLUMN with no default
# only changes the table's metadata -- no row is rewritten.
_ADDED_COLUMNS = (("agent_id", "TEXT"), ("agent_type", "TEXT"), (_CACHE_1H_COLUMN, "INTEGER"))

# dedupe_key convention: session_id + ":" + requestId. Verified empirically
# that a single API turn can be split across multiple JSONL lines
# (distinct `uuid` per line, shared `requestId`) -- requestId (scoped
# to its session; request IDs are not guaranteed globally unique
# across sessions) is the correct one-row-per-API-turn key, not uuid.
# The split lines' `message.usage` blocks are NOT always identical
# (see module docstring's "Split-turn output_tokens correction"):
# identical for main-chain turns, but for subagent/sidechain turns
# only input/cache tokens match across lines -- output_tokens is a
# placeholder except on the line that carries the real value. A
# dedupe_key can also collide BETWEEN two sibling subagent files of
# the same session, not just between split lines of one file -- see
# module docstring. Because which file/line is "first" or "last" is an
# artifact of `sorted(paths)` glob order, not a signal of which value
# is real, import_transcripts() dedupes by MAX(output_tokens), not by
# occurrence order: a stored row's output_tokens/accounted_cost_usd is
# only overwritten when a newly-seen line's output_tokens is strictly
# greater. See module docstring.

# Accounted API list prices, USD per token -- accounting prices, not
# cash prices: a free/subscription tier is a cash discount, not a cost
# of zero (Rule #1: supervision must cost less than the savings it
# produces, verified against accounting prices).
# Source: Anthropic pricing, as cached in the claude-api skill
# (SKILL.md "Current Models", cache date 2026-06-24) and cross-checked
# against gateway/config.yaml's own anthropic/claude-fable-5 and
# anthropic/claude-sonnet-5 aliases in this repo -- cross-checked empirically.
# Cache multipliers (F6-24): cache writes cost 1.25x base input price at
# the 5-minute TTL and 2x at the 1-hour TTL; cache reads cost 0.1x, but
# the Claude 5.x rows carry their own read multiplier (Fable 5.1 0.025x,
# Opus/Sonnet 5.5 0.05x). The file-level multipliers are the defaults, a
# model row MAY override the read/write ones; the transcript usage carries
# the 5m/1h write split (usage.cache_creation), stored in the
# cache_creation_1h_tokens column. Sonnet 5's introductory price ($2/$10
# through 2026-08-31) is NOT used here -- we price at the standard list
# rate per Rule #1 ("list prices"), not a time-limited promotion; note
# this as a caveat in the report if it matters later.
#
# Unknown models get cost=None (Rule #1: never a silent $0). Do NOT
# add a price to tools/model_prices.json without a verified source --
# guessing is exactly what Rule #1 forbids. Prices and the cache
# multipliers live in that file (opus-5 is priced like opus-4-8; both
# haiku-4-5 ids, dated and bare, are keyed to the same price).
#
# Reconciliation with gateway/config.yaml: if a gateway alias ever
# gains an explicit litellm_params.input_cost_per_token /
# output_cost_per_token override there, that becomes a SECOND numeric
# price for the same model id -- re-diff this table against
# gateway/config.yaml whenever such an override appears, since two
# independently-maintained numbers for one model is exactly the kind
# of silent divergence this table exists to avoid.
# The price table is DATA, not code (FR-13: closed variety lives in data
# files): tools/model_prices.json, read by load_prices() -- the one
# reader. A model absent from the file, or present with a null input or
# output price, is "unknown price" (cost=None, never $0); the owner
# fills the price in from the price list in the file, nobody edits code.
PRICES_FILE = Path(__file__).parent / "model_prices.json"


class PricesError(Exception):
    """The price file is missing, unreadable or malformed."""


def _number(value, allow_null=False):
    """True for a finite, non-negative real number (bool is not one)."""
    if value is None:
        return allow_null
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return False
    return math.isfinite(value) and value >= 0


class ModelPrice(NamedTuple):
    """One fully priced model: USD per token and the cache multipliers
    that apply to THIS model (its own row's override, else the file's)."""
    input: float
    output: float
    cache_write_multiplier: float      # 5-minute cache write
    cache_write_1h_multiplier: float   # 1-hour cache write
    cache_read_multiplier: float


_MODEL_OVERRIDE_KEYS = ("cache_read_multiplier", "cache_write_multiplier")
_MODEL_ROW_KEYS = frozenset(("input", "output", "note") + _MODEL_OVERRIDE_KEYS)


def load_prices(path=None) -> dict:
    """Reads and validates the price file (default: model_prices.json
    next to this module). Returns {"as_of", "cache_write_multiplier",
    "cache_write_1h_multiplier", "cache_read_multiplier" (the FILE-level
    defaults), "models": {model_id: ModelPrice}}; every consumer takes a
    model's multipliers from its ModelPrice, never from the file level.
    "models" holds ONLY fully priced models -- a null input or output
    makes a model unknown (both prices are needed; a per-model multiplier
    on such a row is ignored), so it is left out.

    Raises PricesError with ONE message naming the file and what is
    wrong (FR-41: an unreadable table must stop the tool, never read as
    a silent $0); a malformed per-model multiplier names the model and
    the key."""
    p = Path(path) if path is not None else PRICES_FILE
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except OSError as e:
        raise PricesError(f"price file {p}: cannot be read ({e.strerror or e})")
    except (ValueError, UnicodeDecodeError) as e:
        raise PricesError(f"price file {p}: malformed JSON ({e})")
    if not isinstance(data, dict):
        raise PricesError(f"price file {p}: top level must be a JSON object")
    multipliers = {}
    for key in ("cache_write_multiplier", "cache_write_1h_multiplier", "cache_read_multiplier"):
        if not _number(data.get(key)):
            raise PricesError(f"price file {p}: '{key}' is missing or not a number")
        multipliers[key] = data[key]
    models = data.get("models")
    if not isinstance(models, dict):
        raise PricesError(f"price file {p}: 'models' is missing or not an object")
    priced = {}
    for model_id, entry in models.items():
        if not isinstance(entry, dict):
            raise PricesError(f"price file {p}: model '{model_id}' must be an object")
        unknown = sorted(set(entry) - _MODEL_ROW_KEYS)
        if unknown:  # a typo'd key must not price silently at the file default (FR-41); beats a null price
            raise PricesError(
                f"price file {p}: model '{model_id}': unknown key '{unknown[0]}'"
                f" (allowed: {', '.join(sorted(_MODEL_ROW_KEYS))})"
            )
        for key in ("input", "output"):
            if key not in entry or not _number(entry[key], allow_null=True):
                raise PricesError(
                    f"price file {p}: model '{model_id}': '{key}' must be a number or null"
                )
        for key in _MODEL_OVERRIDE_KEYS:
            if key in entry and not _number(entry[key]):
                raise PricesError(
                    f"price file {p}: model '{model_id}': '{key}' must be a non-negative number"
                )
        if entry["input"] is not None and entry["output"] is not None:
            priced[model_id] = ModelPrice(
                entry["input"], entry["output"],
                entry.get("cache_write_multiplier", multipliers["cache_write_multiplier"]),
                multipliers["cache_write_1h_multiplier"],
                entry.get("cache_read_multiplier", multipliers["cache_read_multiplier"]),
            )
    return {
        "as_of": data.get("as_of"),
        "cache_write_multiplier": multipliers["cache_write_multiplier"],
        "cache_write_1h_multiplier": multipliers["cache_write_1h_multiplier"],
        "cache_read_multiplier": multipliers["cache_read_multiplier"],
        "models": priced,
    }


_DEFAULT_PRICES = None


def get_prices(prices=None) -> dict:
    """The prices a caller passed, else the default file, loaded ONCE
    per process."""
    global _DEFAULT_PRICES
    if prices is not None:
        return prices
    if _DEFAULT_PRICES is None:
        _DEFAULT_PRICES = load_prices()
    return _DEFAULT_PRICES


SKIP_MODELS = transcripts.SKIP_MODELS  # the one place of the set (t-886 F-6); the skip itself is transcripts.read_requests'


def transcript_glob(base_dir: Path = None) -> list:
    """Returns the default glob PATTERNS (plural -- a list, not a
    single string) for Claude Code transcripts:

    1. top-level session transcripts: <project>/<session>.jsonl
    2. subagent/sidechain transcripts, ANY depth under subagents/
       (Delegated Task 6, extended by a later regression fix):
       <project>/<session>/subagents/agent-*.jsonl (flat, Task 6) AND
       any further nesting below subagents/ (observed from a workflow
       tool that groups its agent transcripts under an extra
       subagents/workflows/wf_*/ layer). The `**` component matches
       zero or more directories, so this single pattern covers both
       the flat and any deeper layout; import_transcripts() passes
       recursive=True to glob.glob() so `**` is honored.

    The two top-level layouts (session vs. subagent) do not share a
    single glob pattern, hence the list. import_transcripts() accepts
    either this list or a single pattern string (the latter for
    CLI-override / backward-compat with existing callers/tests that
    pass one path)."""
    base = base_dir or (Path.home() / ".claude" / "projects")
    return [
        str(base / "*" / "*.jsonl"),
        str(base / "*" / "*" / "subagents" / "**" / "*.jsonl"),
    ]


# A request with no usage anywhere: its row is zeros, as before F6-15 (the 1-hour split is unknown).
_NO_PART = {**{k: 0 for k in transcripts.REQUEST_USAGE_KEYS}, "cache_creation_1h_tokens": None}


def _turn_meta(obj) -> dict:
    """The per-line metadata of a turn that the usage reader does not carry; read in the same pass.
    agent_id / agent_type (Delegated Task 7, GAP 1): both None on top-level (non-subagent) lines, which never
    carry either field -- verified empirically, see module docstring. `attributionAgent` (not a made-up
    "agentType" key -- that literal key was NOT found anywhere in real data) is the per-line field that matches
    the subagent's sidecar meta.json `agentType` value exactly."""
    return {"ts": obj.get("timestamp"), "session_id": obj.get("sessionId"),
            "is_sidechain": 1 if obj.get("isSidechain") else 0,
            "agent_id": obj.get("agentId"), "agent_type": obj.get("attributionAgent")}


def _part_suffixes(parts) -> list:
    """The dedupe_key suffix of each part of a request, aligned with `parts`: the anchor (the first part with a
    model, else the first) keeps the request's key (the one every single-model request has) and the others add
    `|<model>`; a second part of a model that already has a suffix adds `#<position>` (two iterations of one
    model are two rows, never one)."""
    anchor = next((i for i, q in enumerate(parts) if q["model"] is not None), 0)
    used, suffixes = set(), []
    for i, q in enumerate(parts):
        suffix = "" if i == anchor else f"|{q['model']}"
        suffix = suffix + f"#{i}" if suffix in used else suffix
        used.add(suffix)
        suffixes.append(suffix)
    return suffixes


def iter_assistant_turns(path: str, counts=None):
    """Yields one dict per JSONL line with type == 'assistant', skipping
    every other line type (none of which carry a usage field) and
    <synthetic> rows (harness-internal, always zero usage).

    session_id: the JSON "sessionId" field is preferred when present
    (defensive / test-fixture friendly); the fallback depends on the
    transcript's directory layout (see below).

    project / fallback session_id derivation handles BOTH transcript
    layouts (Delegated Task 6, extended by a later regression fix):
    - top-level: <project>/<session>.jsonl -- verified empirically
      that every real transcript's per-line "sessionId" always equals
      its own filename stem, so the filename stem is both the
      project's session and the fallback.
    - subagent/sidechain, ANY depth under subagents/ --
      <project>/<session>/subagents/agent-*.jsonl (flat, Task 6) or
      nested further below subagents/ (e.g. a workflow tool's extra
      subagents/workflows/wf_x/... layer) -- the file's OWN stem is
      the sub-agent id (e.g. "agent-a6d8..."), not a session id, so it
      would be wrong as a session_id fallback; the real parent session
      id is the directory name one level ABOVE the nearest ancestor
      directory literally named "subagents", regardless of how many
      extra directories sit between "subagents" and the file itself.
      Detected by walking up the path's parents to find that
      "subagents" ancestor, instead of checking only the immediate
      parent (which silently misses any nesting deeper than one
      level).

    Tokens (forge/6 F6-23, t-886): the file is read ONCE, by
    transcripts.read_requests; a request is a list of parts (one per model
    message of it: the provider's own `usage.iterations` when the request
    carries two or more, else the MAX over the lines of each model -- the
    rule is transcripts.request_parts'). A request with several parts (a
    model fallback inside one request) is several turns, one per part,
    priced by accounted_cost each by ITS OWN model and summed by the
    reports; the first part (the model the lines are labelled with) keeps
    the request's dedupe_key, the others add `|<model>`. A part no line is
    labelled with is yielded by the first line of the request. A
    single-model request is unchanged. Real fallback figures: a request of
    fable-5 (2 in, 869 out, 625 5m-write, 102517 read) and opus-4-8 (2, 390,
    0, 98101) is 0.21261 -- the provider's own figure; the lines alone
    (MAX per model) would give 0.17542425.

    `counts`: an optional Counter that receives "bad_usage" (a usage that
    is not an object, or holds a mistyped value: the line is skipped, never
    a traceback), "keyless" (a line with neither requestId nor uuid: its
    own turn, keyed by its position in the file), "bad_iterations" (a
    malformed `usage.iterations`, ignored) and "split_missing" (an
    iterations part with no 1-hour split, priced as a 5-minute write)."""
    p = Path(path)
    subagents_dir = next((a for a in p.parents if a.name == "subagents"), None)
    if subagents_dir is not None:
        session_dir = subagents_dir.parent
        project = session_dir.parent.name
        filename_session_id = session_dir.name
    else:
        project = p.parent.name
        filename_session_id = p.stem
    counts = Counter() if counts is None else counts
    skipped = []
    # ONE pass over the file (t-886 F-2: a second pass over a live transcript meets lines the first never saw,
    # which would be stored as zero rows): the tokens come from the one reader (transcripts.read_requests), the
    # per-line metadata from the same pass. A request is a list of parts, one per model message of it.
    requests, lines = transcripts.read_requests(path, skipped, counts, _turn_meta)
    counts["bad_usage"] += len(skipped)
    parts_of = {rec["key"]: rec["parts"] for rec in requests}
    labelled = {}  # request key -> the models its lines are labelled with
    for _line_no, key, model, _meta in lines:
        labelled.setdefault(key, set()).add(model)
    seen = set()  # requests whose first line has been through the loop
    for index, (line_no, key, model, meta) in enumerate(lines):
        kind, request_id = key
        parts = parts_of.get("%s:%s" % key, [])
        is_first = key not in seen
        seen.add(key)
        # A line yields the parts of ITS model; a part no line is labelled with (the iterations name a model the
        # lines do not) is yielded once, by the first line of the request.
        chosen = [(q, s) for q, s in zip(parts, _part_suffixes(parts))
                  if q["model"] == model or (is_first and q["model"] not in labelled[key])]
        if not parts:
            chosen = [({"model": model, **_NO_PART}, "")]  # a request with no usage anywhere: a zero row, as before F6-15
        session_id = meta["session_id"] or filename_session_id
        dedupe_key = f"{session_id}:{request_id}"
        if kind == "line":
            # Neither a requestId nor a uuid: its own request, keyed by its position in the file (before F6-23 every
            # such line of a session was ONE row, `<session>:None`: an under-count).
            counts["keyless"] += 1
            dedupe_key = f"{session_id}:line:{p.stem}:{line_no}"
        for part, suffix in chosen:
            yield {
                "ts": meta["ts"],
                "project": project,
                "session_id": session_id,
                "turn_index": index,
                "model": part["model"],
                "input_tokens": part["input_tokens"],
                "output_tokens": part["output_tokens"],
                "cache_creation_tokens": part["cache_creation_input_tokens"],
                "cache_read_tokens": part["cache_read_input_tokens"],
                "cache_creation_1h_tokens": part["cache_creation_1h_tokens"],
                "is_sidechain": meta["is_sidechain"],
                "agent_id": meta["agent_id"],
                "agent_type": meta["agent_type"],
                "dedupe_key": dedupe_key + suffix,
            }


def accounted_cost(model: str, input_tokens: int, output_tokens: int,
                    cache_creation_tokens: int, cache_read_tokens: int,
                    prices: dict = None, cache_creation_1h_tokens: int = None):
    """Returns (cost_usd_or_None, warning_or_None). Never a silent $0
    for an unknown price (Rule #1): the cost is None. The warning slot
    is kept for the callers that unpack the pair but is always None --
    an unknown price is no longer a per-turn warning; the report prints
    ONE "unknown price: <model>: N turn(s)" line per model, counted from
    the stored rows with a NULL cost.

    The multipliers are the MODEL's (its ModelPrice). Cache writes are
    split by cache_creation_1h_tokens: that part at the 1-hour rate, the
    rest at the 5-minute rate; None = the split is unknown, the whole
    write is a 5-minute write. A split outside 0..cache_creation_tokens is
    clamped into it (the 1-hour part never exceeds the write)."""
    table = get_prices(prices)
    model_prices = table["models"].get(model)
    if model_prices is None:
        return None, None
    write_1h = 0 if cache_creation_1h_tokens is None else min(max(cache_creation_1h_tokens, 0), cache_creation_tokens)
    cost = (
        input_tokens * model_prices.input
        + output_tokens * model_prices.output
        + (cache_creation_tokens - write_1h) * model_prices.input * model_prices.cache_write_multiplier
        + write_1h * model_prices.input * model_prices.cache_write_1h_multiplier
        + cache_read_tokens * model_prices.input * model_prices.cache_read_multiplier
    )
    return cost, None


def db_path() -> Path:
    return Path(os.environ.get("GATEWAY_DB_PATH", Path(__file__).parent.parent / "gateway" / "requests.db"))


def _connect(path: Path) -> sqlite3.Connection:
    """Opens the DB and ensures the schema is current.

    SCHEMA above is CREATE TABLE IF NOT EXISTS, so it only creates the
    table with the NEW columns on a fresh DB -- it never adds a column
    to a table that already exists from before Delegated Task 7. The
    ALTER TABLE loop below is the idempotent migration for EXISTING
    databases: it checks PRAGMA table_info first and only adds a
    column that is actually missing, so re-running this function
    (i.e. every normal import) is always a safe no-op once the columns
    exist."""
    conn = sqlite3.connect(path)
    conn.execute(SCHEMA)
    existing_cols = {row[1] for row in conn.execute("PRAGMA table_info(cc_usage)")}
    for col, sql_type in _ADDED_COLUMNS:
        if col not in existing_cols:
            conn.execute(f"ALTER TABLE cc_usage ADD COLUMN {col} {sql_type}")
    conn.commit()
    return conn


def _has_1h_column(conn: sqlite3.Connection) -> bool:
    """True when cc_usage stores the 1-hour cache-write split. The importer's
    _connect() always adds it; a database read WITHOUT an import since the
    column was introduced (build_report, token_usage_stats.aggregate) may
    lack it -- the readers say so as an estimate."""
    return _CACHE_1H_COLUMN in {row[1] for row in conn.execute("PRAGMA table_info(cc_usage)")}


def backfill_costs(conn: sqlite3.Connection, prices: dict = None) -> int:
    """Recomputes accounted_cost_usd for rows where it is currently
    NULL, using the CURRENT price file (model_prices.json) and each row's
    already-stored token counts (no transcript re-read needed).

    Exists so that adding a new model's price (e.g. haiku, Delegated
    Task 7 GAP 2) retroactively prices rows imported before that price
    existed, instead of leaving them permanently NULL. Idempotent: a
    row only qualifies while its cost is NULL, so a second call with
    no newly-priced models updates 0 rows. Returns the number of rows
    updated."""
    rows = conn.execute(
        f"""
        SELECT id, model, input_tokens, output_tokens,
               cache_creation_tokens, cache_read_tokens, {_CACHE_1H_COLUMN}
        FROM cc_usage WHERE accounted_cost_usd IS NULL
        """
    ).fetchall()
    updated = 0
    for row_id, model, input_tokens, output_tokens, cache_creation_tokens, cache_read_tokens, write_1h in rows:
        cost, _warning = accounted_cost(
            model, input_tokens, output_tokens, cache_creation_tokens, cache_read_tokens,
            prices, write_1h,
        )
        if cost is not None:
            conn.execute(
                "UPDATE cc_usage SET accounted_cost_usd = ? WHERE id = ?",
                (cost, row_id),
            )
            updated += 1
    return updated


def _max_wins_update(conn: sqlite3.Connection, turn: dict, cost, prices: dict = None) -> None:
    """MAX-wins for an existing row: only a line whose output_tokens is
    strictly greater than the stored value overwrites output_tokens and the
    cost. A line with NO 1-hour split keeps the stored split (it never
    reprices the row as all-5-minute writes, F-5): the cost is then
    recomputed with the stored split, which stays."""
    stored = conn.execute(
        f"SELECT {_CACHE_1H_COLUMN} FROM cc_usage WHERE dedupe_key = ? AND output_tokens < ?",
        (turn["dedupe_key"], turn["output_tokens"])).fetchone()
    if stored is None:
        return
    split = turn["cache_creation_1h_tokens"]
    if split is None and stored[0] is not None:
        split = stored[0]
        cost, _warning = accounted_cost(
            turn["model"], turn["input_tokens"], turn["output_tokens"],
            turn["cache_creation_tokens"], turn["cache_read_tokens"], prices, split)
    conn.execute(
        f"UPDATE cc_usage SET output_tokens = ?, accounted_cost_usd = ?, {_CACHE_1H_COLUMN} = ?"
        " WHERE dedupe_key = ?", (turn["output_tokens"], cost, split, turn["dedupe_key"]))


def _fill_1h_split(conn: sqlite3.Connection, turn: dict, prices: dict = None) -> None:
    """A row that already exists with no stored 1-hour split (imported
    before the column was added) gets the split from this line, and its
    cost is recomputed from the row's OWN stored tokens (never from this
    line's output_tokens, which may be a split-turn placeholder). A row
    that has a split, or a line that has none, is left as it is."""
    if turn["cache_creation_1h_tokens"] is None:
        return
    cur = conn.execute(
        f"UPDATE cc_usage SET {_CACHE_1H_COLUMN} = ? WHERE dedupe_key = ? AND {_CACHE_1H_COLUMN} IS NULL",
        (turn["cache_creation_1h_tokens"], turn["dedupe_key"]),
    )
    if cur.rowcount == 0:
        return
    row = conn.execute(
        "SELECT id, model, input_tokens, output_tokens, cache_creation_tokens, cache_read_tokens"
        " FROM cc_usage WHERE dedupe_key = ?", (turn["dedupe_key"],)).fetchone()
    cost, _warning = accounted_cost(*row[1:], prices, turn["cache_creation_1h_tokens"])
    if cost is not None:
        conn.execute("UPDATE cc_usage SET accounted_cost_usd = ? WHERE id = ?", (cost, row[0]))


def import_transcripts(glob_pattern, db_file: Path, prices: dict = None):
    """Idempotent import: re-running over the same transcripts does not
    duplicate rows, enforced by the UNIQUE constraint on dedupe_key
    (INSERT OR IGNORE). Returns (rows_imported, sessions_seen, warnings).

    glob_pattern accepts either a single glob string (backward
    compatible with existing callers/tests and the CLI override) or a
    list/tuple of glob strings, as returned by transcript_glob()'s
    default (one pattern per transcript directory layout, Delegated
    Task 6). Paths matched by more than one pattern are processed only
    once.

    Backfill (Delegated Task 7, extended by a later regression fix):
    this function ALSO backfills rows that were already imported
    before agent_id/agent_type existed as columns, before their model
    had a price, or with a too-low output_tokens because an earlier
    import run kept a placeholder value instead of the real one --
    whether that placeholder came from an earlier line of the same
    split subagent turn, or from a SIBLING subagent file sharing the
    same dedupe_key (see module docstring for why occurrence-order
    tie-breaks, first OR last, are both wrong for that case). There is
    no separate --backfill flag -- backfilling runs automatically as
    part of every normal import, since all of it is naturally
    idempotent (re-running over unchanged data touches 0 NEWLY-
    imported rows, though see the note below on why the backfill
    UPDATE itself always runs regardless):
    - output_tokens / accounted_cost_usd: when INSERT OR IGNORE finds
      a dedupe_key already present (rowcount == 0) -- whether from an
      earlier line/file processed earlier in THIS run, or from a row a
      PREVIOUS run already inserted -- a CONDITIONAL UPDATE overwrites
      output_tokens and accounted_cost_usd with this line's values
      ONLY IF this line's output_tokens is STRICTLY GREATER than what
      is currently stored (MAX-wins). This makes the final value for a
      given dedupe_key depend only on the SET of lines/files that
      share it, not on the order they are visited in -- unlike either
      first- or last-occurrence-wins.
    - agent fields: a separate, unconditional UPDATE fills
      agent_id/agent_type via COALESCE (keep-existing-if-already-set,
      fill-if-NULL) -- unlike output_tokens these don't have a
      placeholder-vs-real split, so a max/order-independent rule would
      be pointless; COALESCE is what Task 7 shipped and stays
      unchanged.
    - costs for rows this run's transcripts don't touch at all:
      backfill_costs() still runs once at the end over the whole
      table, recomputing accounted_cost_usd for any row still NULL
      (covers rows whose model has since been added to
      model_prices.json, e.g. haiku, GAP 2, when the transcript
      that produced that row is no longer being re-scanned)."""
    patterns = [glob_pattern] if isinstance(glob_pattern, str) else list(glob_pattern)
    warnings = []
    modelless = set()  # dedupe keys of turns with no `model` field
    counts = Counter()  # iter_assistant_turns: "bad_usage", "keyless", "bad_iterations", "split_missing" (each reported as ONE warning line, FR-41)
    sessions_seen = set()
    rows_imported = 0
    conn = _connect(db_file)  # also adds the 1-hour split column to a database that predates it
    paths = set()
    for pattern in patterns:
        # recursive=True so a `**` component (the subagents/**/*.jsonl
        # default pattern) matches any depth, including zero extra
        # directories (the flat Task-6 layout); it is a no-op for
        # patterns without `**` (the top-level session pattern), so
        # this is safe for both defaults and any custom
        # --transcripts-glob override.
        paths.update(glob.glob(pattern, recursive=True))
    try:
        for path in sorted(paths):
            for turn in iter_assistant_turns(path, counts):
                sessions_seen.add(turn["session_id"])
                if turn["model"] is None:
                    # cc_usage.model is NOT NULL (the INSERT OR IGNORE
                    # below would drop the row without a trace): count
                    # it, report ONE summary line at the end (FR-41).
                    modelless.add(turn["dedupe_key"])
                    continue
                cost, warning = accounted_cost(
                    turn["model"], turn["input_tokens"], turn["output_tokens"],
                    turn["cache_creation_tokens"], turn["cache_read_tokens"],
                    prices, turn["cache_creation_1h_tokens"],
                )
                if warning and warning not in warnings:
                    warnings.append(warning)
                cur = conn.execute(
                    f"""
                    INSERT OR IGNORE INTO cc_usage
                        (ts, project, session_id, turn_index, model,
                         input_tokens, output_tokens, cache_creation_tokens,
                         cache_read_tokens, accounted_cost_usd, traffic_kind,
                         is_sidechain, agent_id, agent_type, dedupe_key, {_CACHE_1H_COLUMN})
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'real', ?, ?, ?, ?, ?)
                    """,
                    (
                        turn["ts"], turn["project"], turn["session_id"],
                        turn["turn_index"], turn["model"],
                        turn["input_tokens"], turn["output_tokens"],
                        turn["cache_creation_tokens"], turn["cache_read_tokens"],
                        cost, turn["is_sidechain"],
                        turn["agent_id"], turn["agent_type"], turn["dedupe_key"],
                        turn["cache_creation_1h_tokens"],
                    ),
                )
                rows_imported += cur.rowcount
                if cur.rowcount == 0:
                    # Row already existed -- either a dedupe_key seen
                    # earlier in THIS run (an earlier line of a split
                    # subagent turn, possibly from a DIFFERENT sibling
                    # file) or a row left over from a PREVIOUS import
                    # run. Re-running the importer is how history gets
                    # corrected, but occurrence order (first or last)
                    # is the WRONG tie-break -- it tracks
                    # `sorted(paths)` glob order, not which line holds
                    # the real value. Tie-break on VALUE instead: only
                    # overwrite output_tokens/accounted_cost_usd when
                    # THIS line's output_tokens is strictly greater
                    # than what is already stored (MAX-wins) --
                    # order-independent, a no-op in value for
                    # main-chain turns (whose duplicate lines are
                    # byte-identical, so never strictly greater).
                    _max_wins_update(conn, turn, cost, prices)
                    # agent fields keep their original COALESCE
                    # (fill-if-still-NULL) semantics from Task 7,
                    # unconditionally (independent of the
                    # output_tokens comparison above) -- unlike
                    # output_tokens they have no placeholder-vs-real
                    # split, so there is nothing for a max rule to fix
                    # there.
                    conn.execute(
                        """
                        UPDATE cc_usage
                        SET agent_id = COALESCE(agent_id, ?),
                            agent_type = COALESCE(agent_type, ?)
                        WHERE dedupe_key = ?
                        """,
                        (
                            turn["agent_id"], turn["agent_type"],
                            turn["dedupe_key"],
                        ),
                    )
                    _fill_1h_split(conn, turn, prices)
        backfill_costs(conn, prices)
        conn.commit()
    finally:
        conn.close()
    if modelless:
        warnings.append(f"turns without a model field: {len(modelless)}")
    if counts["bad_usage"]:
        warnings.append(f"usage blocks skipped (not an object, or a mistyped value): {counts['bad_usage']}")
    if counts["bad_iterations"]:
        warnings.append(f"usage.iterations ignored (not a list, or an entry without a model or usage): {counts['bad_iterations']} line(s); the per-model MAX of the lines was used")
    if counts["split_missing"]:
        warnings.append(f"split missing on an iterations entry: {counts['split_missing']} (its cache writes are priced as 5-minute writes)")
    if counts["keyless"]:
        warnings.append(f"turns without a requestId and a uuid: {counts['keyless']} (each its own row, keyed by its line position)")
    return rows_imported, sessions_seen, warnings


def unpriced_turns(conn: sqlite3.Connection, cond: str = "1=1", params: tuple = ()) -> dict:
    """model -> the number of cc_usage turns, under the SQL condition `cond`, whose stored cost is NULL (the
    model has no full price: FR-41, never a $0). THE one counting of unpriced turns: the usage report's
    «unknown price» lines and «partial» mark and the savings report's «not measurable» mark both read it."""
    rows = conn.execute(
        "SELECT model, COUNT(*) FROM cc_usage WHERE (" + cond + ") AND accounted_cost_usd IS NULL"
        " GROUP BY model ORDER BY model", params).fetchall()
    return {model: n for model, n in rows}


def estimated_cache_write_turns(conn: sqlite3.Connection, cond: str = "1=1", params: tuple = ()) -> int:
    """The number of priced cc_usage turns, under the SQL condition `cond`,
    that wrote to the cache with no stored 1-hour/5-minute split (the column
    is absent, or NULL on the row): their writes were priced as 5-minute
    writes -- an estimate the report says out loud (FR-41)."""
    no_split = (f" AND {_CACHE_1H_COLUMN} IS NULL" if _has_1h_column(conn) else "")  # no column: every write is one
    return conn.execute(
        "SELECT COUNT(*) FROM cc_usage WHERE (" + cond + ") AND cache_creation_tokens > 0"
        " AND accounted_cost_usd IS NOT NULL" + no_split, params).fetchone()[0]


def build_report(db_file: Path, days: int, prices: dict = None) -> dict:
    table = get_prices(prices)
    conn = sqlite3.connect(db_file)
    conn.row_factory = sqlite3.Row
    since = f"-{days} days"

    where_days = "substr(ts, 1, 10) >= date('now', ?)" if days is not None else "1=1"
    params = (since,) if days is not None else ()

    rows = conn.execute(
        f"SELECT * FROM cc_usage WHERE {where_days} ORDER BY ts", params
    ).fetchall()

    totals = {
        "rows": len(rows),
        "input_tokens": 0,
        "output_tokens": 0,
        "cache_creation_tokens": 0,
        "cache_read_tokens": 0,
        "accounted_cost_usd": 0.0,
        "unknown_cost_rows": 0,
    }
    unknown_price_turns = unpriced_turns(conn, where_days, params)  # model -> turns with a NULL cost
    totals["unknown_cost_rows"] = sum(unknown_price_turns.values())
    cache_write_estimate = {"turns": estimated_cache_write_turns(conn, where_days, params)}
    per_day = defaultdict(lambda: _empty_bucket())
    per_model = defaultdict(lambda: _empty_bucket())
    per_project = defaultdict(lambda: _empty_bucket())
    per_session = defaultdict(lambda: _empty_bucket())
    sidechain_tokens = 0
    sidechain_cost = 0.0
    total_tokens_all = 0

    for r in rows:
        totals["input_tokens"] += r["input_tokens"]
        totals["output_tokens"] += r["output_tokens"]
        totals["cache_creation_tokens"] += r["cache_creation_tokens"]
        totals["cache_read_tokens"] += r["cache_read_tokens"]
        if r["accounted_cost_usd"] is not None:
            totals["accounted_cost_usd"] += r["accounted_cost_usd"]

        row_total_tokens = (
            r["input_tokens"] + r["output_tokens"]
            + r["cache_creation_tokens"] + r["cache_read_tokens"]
        )
        total_tokens_all += row_total_tokens
        if r["is_sidechain"]:
            sidechain_tokens += row_total_tokens
            sidechain_cost += r["accounted_cost_usd"] or 0.0

        day = r["ts"][:10] if r["ts"] else "unknown"
        _accumulate(per_day[day], r)
        _accumulate(per_model[r["model"]], r)
        _accumulate(per_project[r["project"]], r)
        _accumulate(per_session[(r["project"], r["session_id"])], r)

    cache_read_share_of_input = None
    total_input_side = (
        totals["input_tokens"] + totals["cache_creation_tokens"] + totals["cache_read_tokens"]
    )
    if total_input_side:
        cache_read_share_of_input = totals["cache_read_tokens"] / total_input_side

    # Accounted savings vs. what the same cache_read tokens would have
    # cost if sent as fresh (uncached) input tokens, per model.
    uncached_equivalent_cost = 0.0
    for r in rows:
        model_prices = table["models"].get(r["model"])
        if model_prices is None:
            continue
        uncached_equivalent_cost += r["cache_read_tokens"] * model_prices.input
    cache_accounted_savings_usd = None
    if uncached_equivalent_cost or totals["cache_read_tokens"]:
        actual_cache_read_cost = sum(
            r["cache_read_tokens"] * table["models"][r["model"]].input
            * table["models"][r["model"]].cache_read_multiplier
            for r in rows if r["model"] in table["models"]
        )
        cache_accounted_savings_usd = uncached_equivalent_cost - actual_cache_read_cost

    top_sessions = sorted(
        (
            {"project": proj, "session_id": sid, **bucket}
            for (proj, sid), bucket in per_session.items()
        ),
        key=lambda b: b["accounted_cost_usd"],
        reverse=True,
    )[:5]

    sidechain_share_of_tokens = (
        sidechain_tokens / total_tokens_all if total_tokens_all else None
    )

    return {
        "days": days,
        "totals": totals,
        "unknown_price_turns": unknown_price_turns,
        "cache_write_estimate": cache_write_estimate,
        "per_day": dict(sorted(per_day.items())),
        "per_model": dict(per_model),
        "per_project": dict(per_project),
        "top_sessions_by_cost": top_sessions,
        "cache_read_share_of_input": cache_read_share_of_input,
        "cache_accounted_savings_usd": cache_accounted_savings_usd,
        "sidechain_tokens": sidechain_tokens,
        "sidechain_accounted_cost_usd": sidechain_cost,
        "sidechain_share_of_tokens": sidechain_share_of_tokens,
    }


def _empty_bucket():
    return {
        "rows": 0,
        "input_tokens": 0,
        "output_tokens": 0,
        "cache_creation_tokens": 0,
        "cache_read_tokens": 0,
        "accounted_cost_usd": 0.0,
    }


def _accumulate(bucket, row):
    bucket["rows"] += 1
    bucket["input_tokens"] += row["input_tokens"]
    bucket["output_tokens"] += row["output_tokens"]
    bucket["cache_creation_tokens"] += row["cache_creation_tokens"]
    bucket["cache_read_tokens"] += row["cache_read_tokens"]
    bucket["accounted_cost_usd"] += row["accounted_cost_usd"] or 0.0


def format_report(report: dict, warnings: list) -> str:
    lines = [f"CLAUDE CODE USAGE REPORT (last {report['days']} day(s))" if report["days"] is not None
             else "CLAUDE CODE USAGE REPORT (all time)", ""]

    t = report["totals"]
    lines.append("Totals:")
    partial = (
        f" (partial: {t['unknown_cost_rows']} turn(s) without a price)"
        if t["unknown_cost_rows"] else ""
    )
    lines.append(
        f"  {t['rows']} turns, {t['input_tokens']}+{t['output_tokens']} tok"
        f" (+{t['cache_creation_tokens']} cache-write, +{t['cache_read_tokens']} cache-read),"
        f" ${t['accounted_cost_usd']:.4f} accounted{partial}"
    )
    for model, n in report["unknown_price_turns"].items():
        lines.append(f"  unknown price: {model}: {n} turn(s)")
    estimate = report["cache_write_estimate"]
    if estimate["turns"]:
        lines.append("  " + ESTIMATE_CACHE_WRITES_LINE.format(n=estimate["turns"]))

    lines.append("")
    lines.append("Per day:")
    if not report["per_day"]:
        lines.append("  no turns")
    for day, b in report["per_day"].items():
        lines.append(
            f"  {day}: {b['rows']} turns, {b['input_tokens']}+{b['output_tokens']} tok, ${b['accounted_cost_usd']:.4f}"
        )

    lines.append("")
    lines.append("Per model:")
    for model, b in sorted(report["per_model"].items()):
        lines.append(
            f"  {model}: {b['rows']} turns, {b['input_tokens']}+{b['output_tokens']} tok"
            f" (+{b['cache_creation_tokens']} cache-write, +{b['cache_read_tokens']} cache-read),"
            f" ${b['accounted_cost_usd']:.4f}"
        )

    lines.append("")
    lines.append("Per project:")
    for project, b in sorted(report["per_project"].items()):
        lines.append(
            f"  {project}: {b['rows']} turns, {b['input_tokens']}+{b['output_tokens']} tok, ${b['accounted_cost_usd']:.4f}"
        )

    lines.append("")
    lines.append("Top 5 sessions by accounted cost:")
    if not report["top_sessions_by_cost"]:
        lines.append("  none")
    for s in report["top_sessions_by_cost"]:
        lines.append(
            f"  {s['project']} / {s['session_id']}: {s['rows']} turns, ${s['accounted_cost_usd']:.4f}"
        )

    lines.append("")
    lines.append("Cache economics:")
    share = report["cache_read_share_of_input"]
    lines.append(f"  cache_read share of input: {share:.1%}" if share is not None else "  cache_read share of input: n/a (no input tokens)")
    savings = report["cache_accounted_savings_usd"]
    lines.append(
        f"  accounted savings vs. uncached: ${savings:.4f}" if savings is not None
        else "  accounted savings vs. uncached: n/a"
    )

    lines.append("")
    lines.append("Sidechain (subagent) traffic:")
    lines.append(
        f"  {report['sidechain_tokens']} tok, ${report['sidechain_accounted_cost_usd']:.4f} accounted"
    )
    sc_share = report["sidechain_share_of_tokens"]
    lines.append(
        f"  share of total tokens: {sc_share:.1%}" if sc_share is not None else "  share of total tokens: n/a"
    )

    if warnings:
        lines.append("")
        lines.append("Warnings:")
        for w in warnings:
            lines.append(f"  {w}")

    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Claude Code transcript usage report")
    parser.add_argument(
        "--transcripts-glob",
        default=None,
        help=(
            "Override the transcript glob with a SINGLE custom pattern "
            "(default, with no override: TWO patterns are scanned -- "
            "~/.claude/projects/*/*.jsonl for session transcripts and "
            "~/.claude/projects/*/*/subagents/**/*.jsonl (recursive, "
            "any depth) for subagent/sidechain transcripts, Delegated "
            "Task 6). Passing this flag replaces both default patterns "
            "with just this one."
        ),
    )
    parser.add_argument(
        "--db",
        default=None,
        help="Gateway SQLite DB path (default: $GATEWAY_DB_PATH or gateway/requests.db)",
    )
    parser.add_argument("--days", type=int, default=7, help="Report window in days; use --all for no limit")
    parser.add_argument("--all", action="store_true", help="Report over all imported history, ignoring --days")
    parser.add_argument("--json", action="store_true")
    parser.add_argument(
        "--prices",
        default=None,
        help="Price file (default: model_prices.json next to this script); for tests",
    )
    args = parser.parse_args(argv)

    # The price file is read first, before any import: an unreadable
    # table stops the tool (exit 2), it never reads as a silent $0.
    try:
        prices = load_prices(args.prices)
    except PricesError as e:
        print(f"usage_report: {e}", file=sys.stderr)
        return 2

    db_file = Path(args.db) if args.db else db_path()
    pattern = args.transcripts_glob or transcript_glob()

    rows_imported, sessions_seen, warnings = import_transcripts(pattern, db_file, prices)

    days = None if args.all else args.days
    report = build_report(db_file, days, prices)
    report["import_summary"] = {
        "rows_imported_this_run": rows_imported,
        "sessions_seen_this_run": len(sessions_seen),
    }

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(format_report(report, warnings))
        print("")
        pattern_desc = pattern if isinstance(pattern, str) else " + ".join(pattern)
        print(
            f"(this run: {rows_imported} new row(s) imported from"
            f" {len(sessions_seen)} session file(s) matching {pattern_desc})"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
