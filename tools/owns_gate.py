r"""owns_gate.py -- a Claude Code PreToolUse hook on Task/Agent, WARN-ONLY
(measure first, decide whether to block later). Mechanizes a machine
check that a NEW writing dispatch's owns paths don't collide with the
owns paths of currently LIVE dispatches -- one layer of protection
against parallel-dispatch collisions (CLAUDE.md rule 4: "parallel
specs declare path ownership; the Lead checks overlap before
launching" -- a manual check decays with the coordinator's memory,
this is a machine backstop on top of it, not a replacement for it).

Why NOT logs/routing-log.jsonl: `delegated` events are written AFTER
the dispatch call returns and are legitimately BATCHED to a stage
boundary (rule 12 -- "events accumulate and are written as a batch at
the stage boundary"). That means the journal lags exactly in the
window where two simultaneous dispatches collide: if the coordinator
dispatches two writing tasks back to back with no journal write in
between, the second dispatch goes out BEFORE the first ever appears in
routing-log -- a journal-based check would see nothing. PreToolUse is
the one point where code is guaranteed to meet EVERY dispatch before
it starts -- so the carrier for live owns state is a SEPARATE sidecar,
logs/owns_registry.jsonl (append-only, one JSON line per writing
dispatch), not the routing journal.

Payload contract: the same one tools/dispatch_gate.py already uses
(payload["tool_name"] in {"Task", "Agent"}, tool_input.prompt /
tool_input.description, payload["cwd"]).

--- Extracting owns paths from the prompt (extract_owns_paths) ------
extract_owns_paths(prompt) is a thin wrapper over the ONE reader
(dispatch_manifest.owned_paths on dispatch_manifest.section_cut, see "One
cut, one reader" below); the token helpers it uses (_strip_owns_marker_junk,
split_and_clean_tokens, is_path_token, _first_token_path,
_is_owns_declaration_line, CONTINUATION_LINE_LIMIT) live in this file and are
described here. A marker line is read as follows.
 1. Owns MARKER. This kit's tools/dispatch_gate.py already exports a
    single, WORD-BOUNDED owns marker (MANIFEST_OWNS_RE = r"\bowns\b",
    case-insensitive) -- this file imports it rather than keeping a
    local copy (shared point of truth: dispatch_gate.py's own check 2
    and this file's extraction must never drift apart). ADAPTATION
    FROM THE PORTED SOURCE: the source deployment's dispatch_gate.py
    carries TWO owns regexes -- a word-bounded primary one and a
    separate, bare (unbounded) fallback used ONLY when no line in the
    prompt matches the bounded form at all (tolerance for a mangled
    prompt where "owns" appears only as a substring of another word).
    This kit's dispatch_gate.py does not carry that second, unbounded
    regex (MANIFEST_OWNS_RE here is ALREADY the bounded form) -- there
    is nothing to fall back to, so this port runs a SINGLE pass over
    MANIFEST_OWNS_RE and has no substring-fallback pass. A prompt whose
    only mention of "owns" is embedded inside another word (e.g. a
    filename) is treated the same as a prompt with no owns marker at
    all: extract_owns_paths returns [] with no diagnostic. This is a
    conscious behavioral narrowing, not a partial port -- see the
    handoff report for the exact discrepancy this creates against the
    ported source.
 2. The header line of EVERY owns section (not just the first) is read:
    the text after the marker match has its "declaration junk" trimmed
    (_strip_owns_marker_junk) -- an optional parenthetical
    clarification `\([^)]*\)` (covers `owns (ABSOLUTE write paths):`)
    and leading punctuation `[\s*:\-\u2014\u00ab\u00bb"']` (covers
    markdown `**owns**:` and a plain `owns:`), iteratively, until the
    remainder stabilizes. What's left is tokenized
    (split_and_clean_tokens) and filtered by is_path_token. The paths
    of ALL owns sections are united (a section whose header carries no
    path contributes only its continuation, see "Multi-line owns
    block"); a marker line that is prose ("Attempt 1 owns: ...") is not
    a header and is never read.

--- Line selection is declaration-aware, not "any line with the word"
The scan above only tries the MULTI-LINE continuation form (see below)
when the marker's OWN line is itself a genuine owns DECLARATION, not
prose that merely happens to contain the word "owns" ("don't go beyond
the owns of this task" is prose, not a declaration). A line qualifies
as a declaration line (_is_owns_declaration_line) when: (a) everything
BEFORE the marker match is only whitespace + an optional bullet
(`- `/`* `/`\u2022 `) + optional markdown `**`; (b) everything AFTER
the marker match, once junk-trimmed, is EMPTY. Both conditions are
required together -- a line that already yielded a path on its own
never reaches this check at all (the marker line's own paths win
first, unconditionally).

--- One cut, one reader (B-204, t-608) ---------------------------------
The prompt is cut ONCE by dispatch_manifest.section_cut (one md_regions
scan, header grammar = dispatch_manifest._HEADER_RE, one quoted polarity:
dispatch_gate._is_quoted, an UNTERMINATED fence is prose) and owned paths
are read ONCE by dispatch_manifest.owned_paths(cut): the union of every
owns section (a header line outside a fence/blockquote), marker-line
priority, the continuation stops at a blank line / a section header / a
quoted line, and only ABSOLUTE paths are kept. This hook registers exactly
those paths -- what the completeness check counts. A prose line that merely
contains the word ("Attempt 1 owns: D:/old/a.py was wrong.") is not a header
and registers nothing; a relative glob (`owns: tools/*.py`) is dropped by
the absolute filter (R11-f makes it illegal anyway). `(new)` after a path is
read per path and not registered.

QUOTED_OWNS_WARN (a third diagnostic outcome): decide() distinguishes
THREE outcomes when owns_paths == []:
  1. No marker anywhere -- a read-only dispatch, silence (unchanged).
  2. A marker is found, no owns header in quoted text -- BLIND_OWNS_WARN
     (MANIFEST_OWNS_RE + WRITE_INDICATORS_RE on the raw prompt).
  3. No owns header in prose, but one in a fence/blockquote
     (cut.quoted_owns_headers) -- QUOTED_OWNS_WARN. Priority 3 BEFORE 2.
Neither writes to the sidecar. QUOTED_OWNS_WARN is printed ONLY when an
INDEPENDENT write indicator is present elsewhere in the prompt.

POLARITY (F8): one polarity for the checker and the registry -- an
unterminated fence is PROSE. This hook is WARN-only, so the allowed error
direction is "register more": a false overlap WARN, never a block (this hook
always returns 0). The old "unclear stays silent" asymmetry is gone.

MODULE FAILURE: md_regions raising inside section_cut gives a DEGRADED cut
(every line prose, degraded=True, the reason kept) -- the registry registers
from the all-prose cut (more, the allowed direction); the completeness check
returns the UNCHECKED note for the same cut. One scan per prompt: a prompt
without the owns word is not cut at all.

--- "Declaration, not prose" gate: a regression this port pins ------
A marker line qualifies for continuation ONLY when it is itself a
genuine declaration, not ordinary prose that happens to contain the
standalone word "owns" (e.g. "don't go beyond the owns of this task.
D:/repo/readme.md -- read before starting\n\nowns: D:/repo/
real_target.py" -- the prose line must NOT hijack the real `owns:`
declaration two lines below it, stealing "D:/repo/readme.md" as if it
were the continuation's first path and never reaching the real
declaration). _is_owns_declaration_line() and the strict
_is_continuation_path_token() (requiring a real absolute path or a
`*`+slash glob, not a bare "any token with a `*`" match) both exist
specifically to prevent this.

--- Known extraction limits (documented, not fixed; both pinned) ----
 - A LEADING GLOB STAR IS EATEN BY THE STRIPPER: `*` is one of the
   junk leading characters (_JUNK_PREFIX_RE, there for markdown
   `**owns**:`), so extract_owns_paths("owns: */tools/*") yields
   ["/tools/*"], not ["*/tools/*"] -- the leading star is lost. Known,
   not fixed: a glob with a leading star is not an absolute path and
   so falls outside this kit's rule 11 norm ("owns (ABSOLUTE write
   paths)") anyway; the cost is a coarser check on a non-canonical
   form, WARN-only.
 - _strip_owns_marker_junk IS QUADRATIC IN THE NUMBER OF JUNK
   PARENTHETICAL GROUPS: each loop iteration strips ONE `([^)]*)`
   group via a slice-copy of the remainder, so cost is roughly O(n^2)
   in the number of groups. Immaterial at any realistic prompt size; a
   pathological input degrades in time but never crashes the hook
   (main() always returns exit 0) -- not preemptively optimized, the
   price of simplicity in a WARN-only tool.
 3. The remainder is split on `;`, `,`, newline (_TOKEN_SEPARATOR_RE).
    Each raw token, before edge-trimming, has its prose tail cut at
    the FIRST "space-emdash-space" sequence (_PROSE_TAIL_SEP = " \u2014
    ") -- covers "D:/a.py \u2014 a new file": the tail "\u2014 a new
    file" is dropped, the path survives. Deliberately NOT split on a
    bare space -- a legal path containing spaces must survive whole.
 4. After the tail cut, each token is edge-trimmed: whitespace, then
    LEADING quotes/brackets/guillemets (_EDGE_TRIM_CHARS), then
    TRAILING quotes/brackets/guillemets/sentence-ending dot
    (_TRAILING_TRIM_CHARS) -- iteratively (see _clean_token).
 5. Only tokens that LOOK LIKE A PATH survive: a Windows absolute path
    (drive letter, `:`, slash), a POSIX absolute path (leading `/`,
    covers a git-bash `/d/...` form), or a glob carrying BOTH `*` and
    a slash -- is_path_token(), a thin wrapper over
    dispatch_gate.is_path_like_token() (the single shared predicate --
    see dispatch_gate.py's own docstring). RELATIVE paths are NOT
    recognized as paths -- not an oversight: this kit's rule 11
    explicitly requires "owns (ABSOLUTE write paths)".
 No owns marker on any line -- a read-only dispatch, extract_owns_paths
 returns [] -- decide() writes nothing to the sidecar and exits quietly
 (0, None).

ROOT-ONLY PATH TOKENS -- a live cross-dependency, not fixed here: the
staff sibling's is_path_like_token() carries a "root without a segment
is not a path" guard (bare "/", "D:\", "D:/" etc. are rejected) that
this kit's tools/dispatch_gate.py may or may not carry yet at any
given moment (a parallel port node owns that fix). is_path_token()
below is a THIN WRAPPER with no local logic of its own -- it therefore
behaves correctly under EITHER state of dispatch_gate.is_path_like_token
automatically, with no duplicate guard to keep in sync. The battery
below pins this at the boundary through owns_gate's OWN public entry
point (is_path_token / extract_owns_paths), asserting consistency with
whatever dispatch_gate.is_path_like_token currently returns, rather
than hard-coding the guard's post-fix verdict -- see the handoff
report for the current landing state of that dependency.

--- Diagnosing an empty owns ("silence -> noise") --------------------
If extract_owns_paths returned [] (no line yielded any path) BUT the
prompt carries an owns marker (MANIFEST_OWNS_RE) AND a write indicator
(WRITE_INDICATORS_RE, imported from dispatch_gate.py -- the same
shared point of truth) -- decide() returns an additionalContext WARN
("an owns marker is present but no paths could be parsed out of it --
the overlap check is blind on this dispatch; check the owns line's
form", see BLIND_OWNS_WARN_MESSAGE) and does NOT write to the sidecar
(a check that's known to be blind gains nothing from registering an
empty/meaningless owns set). A genuinely read-only dispatch (no marker
at all, OR an owns marker with no OTHER write verb present -- see
WRITE_INDICATORS_RE in dispatch_gate.py, which no longer carries a
bare "owns" alternative) stays silent, same as before.

--- Registration does not depend on WRITE_INDICATORS_RE -------------
The MAIN sidecar-registration path (decide() -> owned_paths(cut))
does NOT consult WRITE_INDICATORS_RE at all -- it is unconditional on
"is this dispatch writing": the decision rests entirely on whether
REAL path tokens were found in an owns declaration. This is a
deliberate architectural choice: manifest correctness must not depend
on whether one of the four write verbs happens to appear elsewhere in
the prompt -- an owns declaration with real paths must register and be
checked regardless of the surrounding prose (same "code guarantees the
encounter" logic as the "Why NOT logs/routing-log.jsonl" section
above). The ONLY place this file consults WRITE_INDICATORS_RE at all
is the two diagnostic branches above (owns declared with no paths --
blind or quoted).

--- Multi-line owns block --------------------------------------------
The canonical form ("paths on the marker's own line") remains the
priority; the reader EXTENDS it: if an owns header is a bare declaration
(_is_owns_declaration_line) and its OWN line yields no valid path,
dispatch_manifest.owned_paths reads the FOLLOWING lines of that section as
a continuation of the block, until the first line that doesn't parse as a
path (a bulleted list `- path` / `* path` / `\u2022 path`, a numbered list
`1. path` / `2) path`, and/or bare path lines; each line is tokenized and
filtered by this file's token helpers: _first_token_path, is_path_token).

MARKER-LINE PRIORITY (mandatory): if the header's OWN line already yielded
>=1 valid path, the continuation is never read at all -- a block below,
even if present, is never merged into the header line's own paths (an
owns line + a list below it as an ADDITION, not an alternative, would
silently change already-accepted dispatches' semantics -- not done here).

Stop conditions for the continuation block (owned_paths; ALL FOUR end the
block, they don't "skip and continue"):
 1. A blank line (line.strip() == "") -- including immediately after
    the marker (a zero-length block -> []).
 2. A new manifest section header -- given/\u0434\u0430\u043d\u043e,
    owns, non-goals, handoff (dispatch_manifest.SECTION_STOP_RE, the one
    regex; a CLOSED set of manifest sections from this kit's rule 11 --
    not an open guess) at the start of the line (after an optional
    markdown `**`) -- its content never joins owns, even if it formally
    contains something path-like (e.g. `non-goals: toolkit/**` contains
    `*`, which by itself would match is_path_token -- the section stop is
    checked FIRST, before tokenizing the line).
 3. The line is quoted (cut.quoted: inside a fence or blockquote; an
    unterminated fence is prose) -- checked BEFORE tokenizing the line.
 4. The first line that yields NO path-like token at all, after
    stripping an optional bullet prefix (`- `/`* `/`\u2022 `) and the
    same junk-trimming the single-line form uses
    (_strip_owns_marker_junk + split_and_clean_tokens + is_path_token).

CONTINUATION-LINE LIMIT (protection against parsing the whole prompt,
boundary-tested BOTH sides): exactly 40 valid continuation lines,
naturally ended by a stop condition on line 41 (or the prompt's end) --
the 40 collected paths are returned as-is. If the block would STILL be
continuing at line 41 (that line too would yield >=1 path token) -- the
limit is hit: [] is returned (the same "blind owns" diagnostic then
fires through decide()), NOT a silent truncation to the first 40 --
a silently truncated owns set would be WORSE than explicit blindness
(the same principle behind the rest of this WARN-only tool: a silent
partial check is more dangerous than an explicitly flagged empty one).

--- Fenced code blocks ------------------------------------------------
A marker+path inside a TERMINATED triple-backtick fence (or a blockquote)
is excluded BY POSITION: the cut marks the line quoted, so it is not a
header (see "One cut, one reader") and stop condition 3 ends a continuation
there. The pinned regression (a bold marker line, then a path inside a
following fenced block) gives an empty result for TWO independent
reasons at once: (a) the "```" delimiter line is not path-like,
tokenization ends the block there; (b) the "```" line itself is quoted,
stop condition 3 ends the block there first, before (a) would even run.
An UNTERMINATED fence is not a quote (one polarity, "POLARITY (F8)").

--- Sidecar -------------------------------------------------------
logs/owns_registry.jsonl, relative to payload["cwd"] (the same
convention tools/dod_track.py already uses for its own track).
Append-only (except for compaction, below), one JSON line per WRITING
dispatch (read-only dispatches AND dispatches with an unparseable owns
-- see "Diagnosing an empty owns" -- produce no record):
  {"ts": "YYYY-MM-DDTHH:MM:SS" (local time, no timezone),
   "session_key": str,
   "cwd": str or None,
   "description": str (tool_input.description or ""),
   "owns": [str, ...]}
A missing file / a malformed JSON line inside it -- fail-open (the
line is silently skipped, the rest read normally; a missing file is an
empty list of live records).

ORDER: a new dispatch is checked against already-existing live records
FIRST, and only THEN (after the check, regardless of its outcome)
appended to the sidecar itself -- self-overlap of a dispatch with its
own record is structurally excluded by this order.

--- Same-session retry exclusion (SAME_SESSION_RETRY) -----------------
FINDING: the sidecar records the START of a writing dispatch and never
learns of its COMPLETION -- there is no wired-up carrier for that yet.
Consequence: ANY resubmission after a `rejected` (this kit's rule 6
PRESCRIBES exactly that -- same task_id, same or WIDER owns) collides
with ITSELF by construction: attempt 1 registered {a.py, b.py};
attempt 2 (the SAME coordinator session, after `rejected`) declares the
same set, or a superset -- the live-records scan finds attempt 1's own
now-dead record and warns the coordinator about its own already-dead
retry, noise the reader cannot act on (owns cannot be split apart --
the retry is rewriting the SAME files by definition; nothing to
serialize -- the earlier dispatch is already dead).

FIX -- K1 (a literal design decision, named here so the risk it
accepts is visible, not buried): a live record is excluded from the
WARN check ENTIRELY (not path-by-path -- the WHOLE record), when BOTH:
 (a) it belongs to the SAME session as the new dispatch (same_session);
 (b) its owns set (each path normalize_path()-normalized -- the SAME
     normalization paths_overlap() already applies, not raw string
     equality) is a SUBSET OF, including EQUAL TO, the new dispatch's
     owns set.

RATIONALE: a genuine parallel conflict (this kit's rule 4) is TWO
workers with DIFFERENT, partially overlapping ownership (that's the
whole point of declaring paths -- each worker declares its OWN slice).
A retry RE-DECLARES the same ownership set or WIDENS it. The signal is
NOT perfect, and the risk is named here explicitly: two LIVE workers
where one's owns is STRICTLY NESTED inside the other's (worker A owns
{x.py}, worker B owns {x.py, y.py}, both alive AT THE SAME TIME in the
SAME session) would LOSE their warn -- the signal misreads B as a
"retry" of A. Such a launch is ALREADY a rule-4 violation on the
dispatcher's part (overlapping parallel owners must be declared
disjoint, the Lead checks overlap before launching) -- skipping the
warn here does not create a NEW hole, it inherits an existing one (the
dispatcher was already required not to launch that pair); this layer
is not the only defense against that mistake.

K2 (the battery's MAIN test): a PARTIAL overlap (the sets intersect,
but NEITHER is nested in the other) remains a conflict -- the WARN
STAYS. This proves the fix does not switch the whole layer off.

K3: a DIFFERENT session ALWAYS warns, regardless of nesting -- a
parallel writer from a different context can never be "this session's
retry" by definition.

FAIL-CLOSED ON AN UNKNOWN SESSION (edge case, spelled out): a record
with a missing or None session_key is treated as a FOREIGN session
(never excluded), even when the NEW dispatch's own session_key also
happens to be missing/None -- a protective default: an unknown
record's author gets no retry leniency.

EMPTY OWNS ON THE RECORD (edge case, spelled out): `[]` or a missing
field is NOT a subset of anything (a deliberate departure from the
set-theoretic convention "the empty set is a subset of everything" --
the filter deliberately does not treat such a record as a retry). In
practice this changes nothing observable in _find_overlaps -- a record
with empty owns, even WITHOUT this rule, never produces a match in the
per-path check below (any() over an empty iterable is always False) --
the rule exists purely for EXPLICIT behavior, covered by its own test
separate from the per-path effect.

NESTING NORMALIZATION (edge case): the owns-set comparison is BY
ELEMENT, each normalize_path()-normalized (.lower(), `\` -> `/`,
trailing `/` sliced) -- the SAME normalization paths_overlap() already
applies for the overlap outcome itself; NOT bare string equality of
raw paths (closes case/separator mismatches), and NOT full fnmatch/
prefix semantics (two DIFFERENT paths that merely "glob-overlap" are
NOT the same element for a subset comparison) -- a deliberate, narrower
engineering choice, documented rather than silently assumed.

RESIDUAL GAP 1 -- NARROWING RETRY (known, left open on purpose): a
legal case where attempt 2 SHRINKS scope after `rejected` (attempt 2's
owns is a STRICT SUBSET of attempt 1's, not a superset or equal). Then
the RECORD's owns (attempt 1) is NOT a subset of the NEW dispatch's
owns (attempt 2) -- K1's issubset() check does not fire, the record
stays a candidate, and the WARN fires falsely (the same noise class as
the original finding above -- a same-session retry the signal doesn't
catch). Left AS-IS, on purpose: widening K1 to "the record's owns and
the new dispatch's owns overlap by superset IN EITHER DIRECTION" would
make it indistinguishable from K2 (a genuine partial-overlap conflict,
the battery's main test) -- {a,b} vs {b,c} (a real conflict, K2) and
{a,b} vs {a} (a narrowing retry, this gap) would BOTH read as "the
record's owns overlaps, but neither is a subset nor equal" -- the same
signal could not tell a real conflict between two DIFFERENT workers
from a legal narrowing retry of ONE worker without an additional
carrier this sidecar doesn't have (e.g. knowing a path was DROPPED from
the declaration, rather than a NEW path appearing under a different
owner). Closes only with a dispatch-completion carrier or a separate
"path REMOVED from owns" signal -- neither exists today.

RESIDUAL GAP 2 -- CROSS-SESSION RETRY (known, same nature): a retry
routinely outlives the DEATH of the coordinator SESSION that sent
attempt 1 (the session compacts/exits, a NEW coordinator session
continues the same logical task and sends attempt 2) -- its
session_key is DIFFERENT. _is_own_session() returns False by
construction (the record's session_key != the new dispatch's) -- K3
("a different session always warns") fires literally, but here its
firing is the SAME false noise: a retry, not a parallel conflict, its
session simply changed legitimately. PARTIALLY damped by the 24h
liveness window (WINDOW_SECONDS) -- if attempt 1 is older than the
window at attempt 2's time, its record is no longer "live" at all and
never reaches this check; WITHIN the window the gap is live. Left
AS-IS -- K3 requires this literally ("a different session ALWAYS
warns"), and telling "a new session of the SAME coordinator,
continuing the same task" apart from "a genuinely different, parallel
session" from a single session_key alone is structurally impossible
(both forms give "a different session_key").
------------------------------------------------------------------------

--- Shared code with tools/owns_verify.py -----------------------------
normalize_path/paths_overlap/split_and_clean_tokens are defined HERE
(owns_gate.py) and imported by owns_verify.py -- owns_gate.py is the
active PreToolUse hook (registered by the harness, must be able to run
standalone with no CLI scaffolding), while owns_verify.py is a plain
CLI, for which an extra dependency on owns_gate.py's own module
carries no reverse-direction problem.

--- Known sidecar limitations (a documented list, not preemptively
fixed) -------------------------------------------------------------
 - WARN-FIRST ACCURACY: the sidecar does not know when a worker
   FINISHES -- a record lives in the liveness window regardless of
   whether the dispatch has already completed; a WARN on an already-
   fully-completed dispatch is possible. Judging actual liveness is
   left to the coordinator.
 - CONCURRENT APPEND FROM TWO SESSIONS: two processes can write to the
   sidecar at once; on most OSes `open(..., "a")` is atomic for a
   short line, but not guaranteed -- a torn (interleaved) line is
   possible in the limit. The reading side (_load_live_records)
   fail-open skips such a line as malformed JSON -- acceptable for a
   WARN-ONLY tool (a missed WARN is cheaper than a crashed hook).
 - COMPACTION AS A LOSS POINT: compaction (below) rewrites the file
   whole -- if a SECOND process appends a line BETWEEN this process's
   read of the existing lines and its final rewrite, that line is lost
   (the rewrite never saw it). A rare case (requires compaction to
   coincide with a concurrent write in a narrow window), accepted as
   the price of simplicity for a WARN-only tool, not preemptively
   fixed.

--- stdin deadline (P4 class) ------------------------------------------
main() reads stdin through a bounded, cross-platform deadline
(_read_stdin_bytes_deadline / _stdin_deadline_seconds, env override
OSLLM_STDIN_TIMEOUT, default 10s, max 600s -- the SAME names and
contract this kit's tools/session_context.py already carries for the
same class of hazard) instead of a bare, unbounded
sys.stdin.buffer.read(): a non-draining consumer on the other end of
the pipe used to hang this hook forever. A LOCAL copy on purpose (no
shared helper module) -- each hook in this kit owns its own copy, same
as the staff sibling. On a timeout the hook DEGRADES to a no-payload
run (returns exit 0 with no output, the same as an empty/malformed
payload) rather than crashing or hanging; a background reader thread
may still be blocked deep in a platform read syscall when main()
returns, so the `if __name__ == "__main__":` guard escalates to
os._exit() after a timeout instead of falling through to normal
interpreter shutdown (a blocked buffered-reader thread can otherwise
crash the process at shutdown with "Fatal Python error:
_enter_buffered_busy").

ONE PROCESS (t-789/t-796, forge F5-8): the parallel cap refuses inside dispatch_gate.main(), which decide()
below cannot see, and the runtime starts the hooks of the Task|Agent matcher TOGETHER, so no hook can read the
gate's verdict in time. dispatch_gate.main() therefore calls run_after_gate(payload) HERE itself, only on
"allow" -- a cap-refused dispatch never reaches this module: no registry row, no warning. run_after_gate() is
main() minus the stdin read and minus decide()'s own dispatch_gate.decide() question (the gate has just
answered it); main() (this file as a hook of its own, settings.json today) reads no carrier and behaves as it
always did. Both runs ask dispatch_gate.claim_trace(payload, "owns_gate") first: of the two runs for one
tool_use_id the first does the work (row, warning), the other returns (0, None) -- nothing is written twice.

FAIL-OPEN: payload not a dict / tool_name not Task|Agent / tool_input
not a dict / prompt not a string / no owns block found -- all of these
return (0, None), no side effects. main() wraps decide() in one more
try/except (belt-and-suspenders, the same principle as this tool set's
other WARN layers) -- an adversarial input (malformed JSON, non-UTF-8
bytes, a payload that isn't a dict, a huge owns string) must not crash
the hook with a traceback; the exit code is ALWAYS 0 (WARN mode -- this
layer never blocks)."""

import fnmatch
import json
import os
import re
import sys
import threading
from datetime import datetime
from pathlib import Path

_TOOLS_DIR = Path(__file__).resolve().parent
if str(_TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(_TOOLS_DIR))

# A DIRECT sibling-module import only (no package-style guess: a bare
# `import tools.dispatch_gate` can resolve "tools" at the CURRENT WORKING
# DIRECTORY as a PEP 420 namespace package and pick up the WRONG module).
from dispatch_gate import (
    MANIFEST_OWNS_RE,
    WRITE_INDICATORS_RE,
    is_path_like_token,
)

# decide() calls dispatch_gate.decide(payload) VERBATIM before it registers
# (see its comment, "M2-1-analog").
import dispatch_gate

# The one cut of the dispatch text and the one reader of owned paths
# (B-204): pure module, no import cycle (its sibling imports are lazy).
import dispatch_manifest


# --- extracting owns paths from the prompt ----------------------------
# The word-bounded owns marker (MANIFEST_OWNS_RE = r"\bowns\b") is
# imported from tools/dispatch_gate.py rather than kept as a local
# copy -- a single shared point of truth between the blocking check
# (dispatch_gate.py's check 2) and this file's extraction. See the
# module docstring, "Owns MARKER", for why this port carries no
# separate unbounded fallback regex.

_PAREN_PREFIX_RE = re.compile(r"^\s*\([^)]*\)")
_JUNK_PREFIX_RE = re.compile(r"^[\s*:\-\u2014\u00ab\u00bb\"']+")
_TOKEN_SEPARATOR_RE = re.compile(r"[;,\n]")
_PROSE_TAIL_SEP = " \u2014 "  # space-emdash-space -- see the module docstring, point 3.

# Backtick "`" is included -- the same class of markdown decoration
# that quotes/guillemets already strip here.
_EDGE_TRIM_CHARS = "\"'`()[]{}\u00ab\u00bb\u201e\u201c\u201d"
# Trailing sentence-ending punctuation (`.`) -- this kit's real
# manifests write an owns bullet as a complete sentence, so ONLY the
# trailing dot (rstrip, not lstrip -- a leading dot is protected, in
# case of a hypothetical relative dot-path) joins the trimmed set, on
# top of quotes/brackets/guillemets.
_TRAILING_TRIM_CHARS = _EDGE_TRIM_CHARS + "."

_WINDOWS_ABS_RE = re.compile(r"^[A-Za-z]:[\\/]")
_POSIX_ABS_RE = re.compile(r"^/")

# Multi-line owns block.
_BULLET_PREFIX_RE = re.compile(r"^\s*[-*\u2022]\s+")
# A numbered list ("1. path" / "2) path") is also recognized as a
# bullet-continuation form.
_NUMBERED_PREFIX_RE = re.compile(r"^\s*\d+[.)]\s+")
# Everything BEFORE the start of the owns-marker match must be only
# whitespace + an optional bullet + optional markdown `**` -- otherwise
# the marker's line is not a declaration, but prose that merely
# contains the word "owns" (see the module docstring, "Declaration, not
# prose").
_DECLARATION_PREFIX_RE = re.compile(r"^\s*(?:[-*\u2022]\s+)?(?:\*\*)?$")
CONTINUATION_LINE_LIMIT = 40


def _strip_owns_marker_junk(remainder: str) -> str:
    """Iteratively strips, from the START of remainder, an optional
    parenthetical clarification `\\([^)]*\\)` and leading characters of
    the class `[\\s*:\\-\\u2014\\u00ab\\u00bb"']` -- IN EITHER ORDER (the
    parenthetical may come before or after the colon; markdown
    `**owns**:` puts stars before the colon) -- until the string
    stabilizes. Both patterns always consume >=1 character on a match,
    so remainder strictly shortens on every successful iteration --
    termination is guaranteed with no separate iteration counter."""
    prev = None
    while remainder != prev:
        prev = remainder
        m = _PAREN_PREFIX_RE.match(remainder)
        if m:
            remainder = remainder[m.end():]
            continue
        m2 = _JUNK_PREFIX_RE.match(remainder)
        if m2:
            remainder = remainder[m2.end():]
            continue
    return remainder


def _cut_prose_tail(raw: str) -> str:
    """Cuts a token's tail at the FIRST "space-emdash-space" sequence
    (_PROSE_TAIL_SEP) -- see the module docstring, point 3. Does NOT
    split on a bare space -- a path containing spaces (e.g.
    "D:/AI CRM/x/AGENTS.md") stays whole."""
    if not raw:
        return raw
    idx = raw.find(_PROSE_TAIL_SEP)
    if idx == -1:
        return raw
    return raw[:idx]


def _clean_token(raw: str) -> str:
    """Strips whitespace, then LEADING quotes/brackets/guillemets
    (_EDGE_TRIM_CHARS) and TRAILING quotes/brackets/guillemets/dot
    (_TRAILING_TRIM_CHARS) -- ITERATIVELY (until stable), so nested
    combinations like "(logs/owns_registry.jsonl)." (a bracket then a
    sentence-ending dot) collapse to a clean path in one loop, not a
    single strip() call."""
    tok = raw.strip()
    prev = None
    while tok != prev:
        prev = tok
        tok = tok.lstrip(_EDGE_TRIM_CHARS)
        tok = tok.rstrip(_TRAILING_TRIM_CHARS)
        tok = tok.strip()
    return tok


def split_and_clean_tokens(text: str) -> list:
    """Splits text on `;`/`,`/newline, cuts each raw token's prose tail
    (_cut_prose_tail) and edge-trims whitespace/quotes/brackets/
    guillemets (+ a trailing dot, see _clean_token). A shared function
    -- see the module docstring, "Shared code with
    tools/owns_verify.py"."""
    if not isinstance(text, str) or not text:
        return []
    cleaned = []
    for raw in _TOKEN_SEPARATOR_RE.split(text):
        raw = _cut_prose_tail(raw)
        tok = _clean_token(raw)
        if tok:
            cleaned.append(tok)
    return cleaned


# A thin wrapper over dispatch_gate.is_path_like_token() -- a single
# shared point of truth, not a local copy. The name is_path_token is
# kept for readability at this file's call sites; behavior is
# identical to is_path_like_token. See the module docstring,
# "Root-only path tokens" -- this wrapper carries no local logic, so it
# tracks whatever dispatch_gate.is_path_like_token() currently does.
def is_path_token(tok: str) -> bool:
    """Windows-absolute / POSIX-absolute / a glob with BOTH `*` and a
    slash -- see the module docstring, point 5, "Extracting owns paths
    from the prompt". Delegates to dispatch_gate.is_path_like_token()
    -- not independent logic."""
    return is_path_like_token(tok)


BLIND_OWNS_WARN_MESSAGE = (
    "an owns marker is present but no paths could be parsed out of it "
    "-- the overlap check is blind on this dispatch; check the owns line's form"
)

# See the module docstring, "QUOTED_OWNS_WARN": all found owns markers
# sit in fenced/blockquote/inline_code, none in prose.
QUOTED_OWNS_WARN_MESSAGE = (
    "owns is declared only inside a quote/fence/inline code \u2014 not a "
    "declaration of ownership; a path-owning conflict with another "
    "dispatch will not be detected; move the owns line into ordinary prose"
)



def _is_owns_declaration_line(line: str, marker_start: int, marker_end: int) -> bool:
    """True only when the marker's own line is itself an owns
    DECLARATION, not prose that merely contains the word "owns" inside
    a sentence -- see the module docstring, "Declaration, not prose",
    for the full rationale. Called by dispatch_manifest.owned_paths ONLY
    when the header line itself yielded no paths -- decides whether
    reading a continuation below is worth it (prose must not hijack a
    real declaration that may be further down)."""
    prefix = line[:marker_start]
    if not _DECLARATION_PREFIX_RE.match(prefix):
        return False
    remainder_after_junk = _strip_owns_marker_junk(line[marker_end:])
    return remainder_after_junk.strip() == ""


# This check already requires "*" AND a slash together -- the same
# strictness dispatch_gate.is_path_like_token() applies as the shared
# point of truth (is_path_token() above simply matches it). Delegating
# removes duplication between two otherwise-identical implementations
# -- the name is kept for readability at this file's call sites.
def _is_continuation_path_token(tok: str) -> bool:
    """A continuation-block token must be a Windows/POSIX absolute path
    OR a glob carrying BOTH "*" and a slash -- see the module
    docstring, "A regression this port pins". Delegates to
    dispatch_gate.is_path_like_token()."""
    return is_path_like_token(tok)


# Open-to-close quote pairs: _first_raw_token looks for a matching
# closing character instead of splitting on the first space, so a
# continuation-line path WITH spaces inside quotes survives whole --
# the single-line form already tolerates spaces inside a path (it
# never splits on a bare space at all, see the module docstring,
# "Extracting owns paths", points 3-4), but a continuation line's ONLY
# token separator is whitespace, so an explicit quote/backtick/
# guillemet delimiter is needed here.
_QUOTE_OPEN_TO_CLOSE = {"\"": "\"", "'": "'", "`": "`", "\u00ab": "\u00bb"}


def _first_raw_token(body: str) -> str:
    """The raw (untrimmed) first token of body -- NORMALLY the first
    whitespace-delimited token (body.split(None, 1)[0]), BUT if body
    starts with an opening character from _QUOTE_OPEN_TO_CLOSE, the
    matching closing character is searched for further in the line --
    if found, everything between them (inclusive) is returned
    (quotes/backtick are stripped later by _clean_token, already
    included in _EDGE_TRIM_CHARS) -- spaces INSIDE are preserved. No
    closing character found -- falls back to a plain space split (does
    not regress behavior on an unclosed quote)."""
    if body and body[0] in _QUOTE_OPEN_TO_CLOSE:
        close_char = _QUOTE_OPEN_TO_CLOSE[body[0]]
        close_idx = body.find(close_char, 1)
        if close_idx != -1:
            return body[: close_idx + 1]
    return body.split(None, 1)[0]


def _first_token_path(line: str):
    """The FIRST token of a continuation line (after stripping a bullet
    `- `/`* `/`\u2022 ` OR a list number `1.`/`2)`), if it is valid per
    _is_continuation_path_token -- any prose tail after the first token
    is IGNORED entirely (it is not glued to the path through a missing
    comma separator). "First token" is found via _first_raw_token --
    normally the first whitespace-delimited one, but if the token opens
    with a quote/backtick/guillemet, everything up to the matching
    close is taken (spaces inside quotes no longer split the path in
    two). None -- the line does not parse as a continuation path (end
    of the block)."""
    body = _BULLET_PREFIX_RE.sub("", line, count=1)
    body = _NUMBERED_PREFIX_RE.sub("", body, count=1)
    body = body.strip()
    if not body:
        return None
    first_raw = _first_raw_token(body)
    tok = _clean_token(first_raw)
    if tok and _is_continuation_path_token(tok):
        return tok
    return None


def extract_owns_paths(prompt: str) -> list:
    """The absolute owns paths of the prompt, in order -- a thin wrapper over
    the ONE reader (dispatch_manifest.owned_paths on dispatch_manifest.
    section_cut). [] -- no owns header outside a fence/blockquote, or none
    yielded an absolute path. Kept for direct callers and the battery."""
    if not isinstance(prompt, str) or not prompt:
        return []
    return [p.path for p in dispatch_manifest.owned_paths(dispatch_manifest.section_cut(prompt))]


# --- path normalization and overlap (shared with owns_verify.py) ------


def normalize_path(p: str) -> str:
    """.lower(), `\\` -> `/`, trailing `/` sliced off -- see the module
    docstring, "Path overlap semantics"."""
    if not isinstance(p, str):
        return ""
    p = p.strip().lower().replace("\\", "/")
    while len(p) > 1 and p.endswith("/"):
        p = p[:-1]
    return p


def paths_overlap(a: str, b: str) -> bool:
    """Equality / a directory-prefix relationship at a segment boundary
    / an fnmatch in either direction when at least one path carries a
    glob -- fnmatch.fnmatchcase (not fnmatch.fnmatch) is used on
    purpose, for identical behavior regardless of the OS the tests
    happen to run on."""
    na, nb = normalize_path(a), normalize_path(b)
    if not na or not nb:
        return False
    if na == nb:
        return True
    if na.startswith(nb + "/") or nb.startswith(na + "/"):
        return True
    if "*" in na or "*" in nb:
        if fnmatch.fnmatchcase(nb, na) or fnmatch.fnmatchcase(na, nb):
            return True
    return False


# --- sidecar: reading live records + writing a new one -----------------

WINDOW_SECONDS = 24 * 60 * 60
_TS_FORMAT = "%Y-%m-%dT%H:%M:%S"
_DESC_TRUNC_LEN = 200
REGISTRY_COMPACT_THRESHOLD_LINES = 500


def _now_iso(now: datetime) -> str:
    return now.strftime(_TS_FORMAT)


def _registry_path_from_cwd(cwd) -> Path:
    return Path(cwd or ".") / "logs" / "owns_registry.jsonl"


def _load_live_records(registry_path: Path, cwd, now: datetime) -> list:
    """Fail-open: a missing file / a malformed line / a wrong-typed
    field -- the record/line is silently skipped, the rest read
    normally. The scope is the SAME cwd (a literal string comparison),
    NOT session_key -- session_key inside a record is only a LABEL for
    the WARN message, see _find_overlaps."""
    if registry_path is None or not registry_path.exists():
        return []
    try:
        raw = registry_path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return []

    records = []
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rec = json.loads(line)
        except Exception:
            continue
        if not isinstance(rec, dict):
            continue
        if rec.get("cwd") != cwd:
            continue
        ts_str = rec.get("ts")
        if not isinstance(ts_str, str):
            continue
        try:
            rec_ts = datetime.strptime(ts_str, _TS_FORMAT)
        except Exception:
            continue
        delta = (now - rec_ts).total_seconds()
        if delta < 0 or delta > WINDOW_SECONDS:
            continue
        owns = rec.get("owns")
        if not isinstance(owns, list):
            continue
        records.append(rec)
    return records


def _compact_live_lines(existing_lines: list, now: datetime) -> list:
    """Compaction: keeps only the RAW lines (str) whose ts falls inside
    the liveness window -- GLOBALLY, with no cwd/session filter
    (compaction serves the whole file, not one specific dispatch). A
    malformed JSON line -- fail-open, silently dropped during
    compaction (see the module docstring, "Known sidecar limitations"
    -- compaction as a possible loss point for a concurrent write)."""
    live = []
    for line in existing_lines:
        line = line.strip()
        if not line:
            continue
        try:
            rec = json.loads(line)
        except Exception:
            continue
        if not isinstance(rec, dict):
            continue
        ts_str = rec.get("ts")
        if not isinstance(ts_str, str):
            continue
        try:
            rec_ts = datetime.strptime(ts_str, _TS_FORMAT)
        except Exception:
            continue
        delta = (now - rec_ts).total_seconds()
        if delta < 0 or delta > WINDOW_SECONDS:
            continue
        live.append(line)
    return live


def _append_registry(
    registry_path: Path, now: datetime, session_key, cwd, description: str, owns_paths: list
) -> None:
    try:
        registry_path.parent.mkdir(parents=True, exist_ok=True)
        entry = {
            "ts": _now_iso(now),
            "session_key": session_key,
            "cwd": cwd,
            "description": description or "",
            "owns": owns_paths,
        }
        entry_line = json.dumps(entry, ensure_ascii=False)

        existing_lines = []
        if registry_path.exists():
            try:
                raw = registry_path.read_text(encoding="utf-8", errors="replace")
                existing_lines = [ln for ln in raw.splitlines() if ln.strip()]
            except Exception:
                existing_lines = []

        # Compaction ONLY when the number of lines is STRICTLY GREATER
        # than the threshold (500 -> a plain append; 501 -> compaction),
        # see the module docstring.
        if len(existing_lines) > REGISTRY_COMPACT_THRESHOLD_LINES:
            live_lines = _compact_live_lines(existing_lines, now)
            live_lines.append(entry_line)
            registry_path.write_text("\n".join(live_lines) + "\n", encoding="utf-8")
        else:
            with registry_path.open("a", encoding="utf-8") as f:
                f.write(entry_line + "\n")
    except Exception:
        # fail-open: being unable to append to the sidecar (e.g. a
        # read-only disk) must not crash the hook.
        pass


def _truncate(s: str, max_len: int = _DESC_TRUNC_LEN) -> str:
    s = (s or "").strip()
    if len(s) > max_len:
        return s[:max_len] + "\u2026"
    return s


# --- Same-session retry exclusion -- see the module docstring,
# "Same-session retry exclusion (SAME_SESSION_RETRY)", for the full
# rationale, the named risk, and the two residual gaps (D1/D2) left
# open on purpose. -------------------------------------------------


def _normalize_owns_set(owns) -> set:
    """The set of normalize_path()-normalized paths of a record/new
    dispatch -- see "Same-session retry exclusion" above, "Nesting
    normalization". Non-string elements and elements that normalize to
    an empty string are dropped silently (fail-open, the same
    principle as the rest of this module)."""
    if not isinstance(owns, list):
        return set()
    result = set()
    for p in owns:
        if not isinstance(p, str):
            continue
        norm = normalize_path(p)
        if norm:
            result.add(norm)
    return result


def _is_own_session(rec: dict, session_key) -> bool:
    """K3/fail-closed (see "Same-session retry exclusion" above): a
    record's session_key must be non-empty AND literally equal to the
    new dispatch's session_key -- a missing/None record session_key is
    ALWAYS a foreign session (never "own"), see "Fail-closed on an
    unknown session" above."""
    rec_session = rec.get("session_key")
    if rec_session is None:
        return False
    return rec_session == session_key


def _is_self_retry_record(rec: dict, session_key, new_owns_normalized: set) -> bool:
    """K1: True -- the record is excluded from the WARN check entirely
    (a same-session retry, not a parallel conflict) -- see "Same-
    session retry exclusion" above for the full rationale, the named
    risk, and the edge cases (empty owns, a missing session_key)."""
    if not _is_own_session(rec, session_key):
        return False
    rec_owns_normalized = _normalize_owns_set(rec.get("owns"))
    if not rec_owns_normalized:
        return False  # EDGE: an empty record owns is not a subset of anything (see above)
    return rec_owns_normalized.issubset(new_owns_normalized)


def _find_overlaps(new_paths: list, records: list, session_key) -> list:
    """Groups overlaps BY NEW PATH, not by (path, record) pair -- a
    single new path that collides with several live records gives ONE
    entry in the result. Returns
    [(path, [(ts, description, same_session_bool), ...]), ...] -- paths
    in the order of new_paths, matched records inside in the order of
    records. same_session_bool compares a record's session_key against
    the CURRENT dispatch's session_key (a label, not a scope filter).

    Records recognized by _is_self_retry_record() as a SAME-SESSION
    RETRY are excluded from the check ENTIRELY, BEFORE the per-path
    overlap check below -- see "Same-session retry exclusion" above.
    A partial overlap (K2) and a foreign session (K3) do NOT pass
    through this filter -- they remain candidates for the ordinary
    per-path check."""
    new_owns_normalized = _normalize_owns_set(new_paths)
    candidate_records = [
        rec for rec in records
        if not _is_self_retry_record(rec, session_key, new_owns_normalized)
    ]
    grouped = []
    for p in new_paths:
        matches = []
        for rec in candidate_records:
            rec_owns = rec.get("owns") or []
            if any(paths_overlap(p, existing) for existing in rec_owns):
                same_session = rec.get("session_key") == session_key
                matches.append((rec.get("ts"), rec.get("description") or "", same_session))
        if matches:
            grouped.append((p, matches))
    return grouped


def _format_mention(ts, desc, same_session: bool) -> str:
    tag = (
        "a parallel dispatch of this same session"
        if same_session
        else "a different session (a parallel-session collision)"
    )
    return f"{ts} \u00ab{_truncate(desc)}\u00bb ({tag})"


def _format_path_line(p: str, matches: list) -> str:
    shown = matches[:2]
    mentions = "; ".join(_format_mention(ts, desc, same) for ts, desc, same in shown)
    extra = len(matches) - len(shown)
    if extra > 0:
        mentions += f"; and {extra} more"
    return f"path {p} overlaps with {mentions}"


def _format_overlap_context(grouped: list) -> str:
    head = grouped[:3]
    parts = [_format_path_line(p, matches) for p, matches in head]
    return (
        "OWNS OVERLAP (warn): " + "; ".join(parts) + "; a parallel write to "
        "shared paths -- serialize the work or split up the owns paths"
    )


# --- decide() ----------------------------------------------------------


def decide(payload: dict, registry_path: Path = None, now: datetime = None, gate_allowed: bool = False) -> tuple:
    """Nearly-pure logic (with sidecar I/O inside -- checking live owns
    unavoidably requires a read before the decision and a write after,
    see the module docstring, "ORDER") -- directly testable by passing
    its own registry_path/now. exit_code is ALWAYS 0 (WARN mode).
    Returns (0, None) on a quiet skip, (0, dict) -- a dict already
    ready for json.dumps on stdout, on a found owns overlap OR on
    either of the two owns_paths == [] diagnostics (quoted-only takes
    priority over blind, see the module docstring, "QUOTED_OWNS_WARN").
    gate_allowed=True: the caller is dispatch_gate.main() on its own "allow" -- the "M2-1-analog" question below
    is already answered and is not asked again."""
    if not isinstance(payload, dict):
        return 0, None

    tool_name = payload.get("tool_name")
    if tool_name not in ("Task", "Agent"):
        return 0, None

    tool_input = payload.get("tool_input") or {}
    if not isinstance(tool_input, dict):
        return 0, None

    # t-796: of the gate's run and this hook's own run for one tool_use_id, the FIRST does the work. No id (or
    # an I/O error) -> True: this run proceeds, as before the claim existed.
    if not dispatch_gate.claim_trace(payload, "owns_gate"):
        return 0, None

    prompt = tool_input.get("prompt")
    if not isinstance(prompt, str):
        prompt = ""

    cut = None
    owns_paths = []
    if MANIFEST_OWNS_RE.search(prompt):
        # ONE cut (dispatch_manifest.section_cut) and ONE reader of owned paths
        # (owned_paths): the registry holds exactly what the completeness
        # checker counts, plus what an unterminated fence leaves as prose.
        cut = dispatch_manifest.section_cut(prompt)
        owns_paths = [p.path for p in dispatch_manifest.owned_paths(cut)]
    if not owns_paths:
        # Every owns header is quoted (fenced/blockquote) -- QUOTED_OWNS_WARN,
        # the sidecar does NOT grow, printed ONLY with an independent write
        # indicator elsewhere in the prompt.
        if cut is not None and cut.quoted_owns_headers and not cut.sections["owns"] \
                and WRITE_INDICATORS_RE.search(prompt):
            return 0, {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "additionalContext": QUOTED_OWNS_WARN_MESSAGE,
                }
            }
        # An owns marker is declared, but no line yielded any path-like
        # tokens -- the check is blind, WARN about the blindness
        # instead of a quiet skip, the sidecar does NOT grow. A
        # genuine read-only dispatch (no marker / no write indicator)
        # stays silent.
        if MANIFEST_OWNS_RE.search(prompt) and WRITE_INDICATORS_RE.search(prompt):
            return 0, {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "additionalContext": BLIND_OWNS_WARN_MESSAGE,
                }
            }
        return 0, None

    if now is None:
        now = datetime.now()
    cwd = payload.get("cwd")
    if registry_path is None:
        registry_path = _registry_path_from_cwd(cwd)

    session_id = payload.get("session_id")
    session_key = session_id if isinstance(session_id, str) and session_id else cwd

    description = tool_input.get("description")
    if not isinstance(description, str):
        description = ""

    records = _load_live_records(registry_path, cwd, now)
    grouped = _find_overlaps(owns_paths, records, session_key)

    output = None
    if grouped:
        output = {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "additionalContext": _format_overlap_context(grouped),
            }
        }

    # Order: the check runs FIRST, the write happens AFTER (self-overlap
    # is excluded structurally, see the module docstring, "ORDER").
    #
    # M2-1-analog (the same class the reference deployment's
    # owns_gate.py:1882-1905 fixes): the runtime executes PreToolUse
    # hooks INDEPENDENTLY of each other -- a dispatch that dispatch_gate
    # itself would block (exit 2) never actually runs, but this hook
    # (WARN-mode, its own exit code is ALWAYS 0) would still register a
    # sidecar record for a dispatch that never happened. Fix: BEFORE the
    # write, ask dispatch_gate.decide() for a verdict on the SAME
    # payload -- exit 2 (blocked) skips the registration (the overlap
    # check above has already run and its output is returned as usual --
    # only the WRITE is skipped, not the decision). An exception out of
    # dispatch_gate.decide() -> register anyway (fail-open, the same
    # philosophy this hook's own WARN mode already carries for its own
    # failures). exit 0 (even with non-empty warn text) -> register as
    # before. Existing registry lines predating this fix are untouched
    # (append-only) -- this check only concerns NEW records. Invariant:
    # this hook's own exit_code stays 0 always -- this branch decides
    # only the registration, never the return value.
    try:
        gate_exit_code = 0 if gate_allowed else dispatch_gate.decide(payload)[0]
    except Exception:
        gate_exit_code = 0  # fail-open: register, as before this fix
    if gate_exit_code != 2:
        _append_registry(registry_path, now, session_key, cwd, description, owns_paths)

    return 0, output


def _reconfigure_stdout_utf8():
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


# --- stdin deadline (P4 class; a LOCAL copy, no shared module -- see
# the module docstring, "stdin deadline (P4 class)") -----------------

_STDIN_DEADLINE_DEFAULT = 10.0
_STDIN_DEADLINE_MAX = 600.0
_STDIN_DEADLINE_ENV = "OSLLM_STDIN_TIMEOUT"


def _stdin_deadline_seconds():
    """Seconds to wait for stdin: env override, else the default.
    Invalid, non-numeric, <=0, or > _STDIN_DEADLINE_MAX all fall back to
    the default -- there is deliberately NO "0 = wait forever" mode (that
    would resurrect the exact hang this helper exists to close)."""
    try:
        value = float(os.environ.get(_STDIN_DEADLINE_ENV, ""))
    except (TypeError, ValueError):
        return _STDIN_DEADLINE_DEFAULT
    if not (0.0 < value <= _STDIN_DEADLINE_MAX):
        return _STDIN_DEADLINE_DEFAULT
    return value


def _read_stdin_bytes_deadline():
    """Returns (bytes, timed_out). Reads stdin to EOF, but no longer
    than the deadline. Cross-platform by construction: select/poll do
    not work on pipes on Windows, so a background daemon thread does
    the actual blocking read and the deadline is enforced via
    thread.join(timeout). A TTY returns b"" without reading anything
    (the same guard this kit's other hooks already carry). Any read
    error degrades to b"" (fail-open, the same discipline as the rest
    of this hook)."""
    stdin = getattr(sys, "stdin", None)
    if stdin is None:
        return b"", False
    try:
        if stdin.isatty():
            return b"", False
    except Exception:
        pass
    stream = getattr(stdin, "buffer", stdin)
    box = {}

    def _reader():
        try:
            box["data"] = stream.read()
        except Exception:
            box["data"] = b""

    thread = threading.Thread(target=_reader, name="stdin-deadline", daemon=True)
    thread.start()
    thread.join(_stdin_deadline_seconds())
    if thread.is_alive():
        return b"", True
    data = box.get("data") or b""
    if not isinstance(data, bytes):
        data = str(data).encode("utf-8", "replace")
    return data, False


_STDIN_DEADLINE_MSG = "stdin deadline exceeded -- fail-open, payload discarded"

# Set when a stdin read actually timed out. A background reader thread
# may still be blocked deep in a platform read syscall at normal
# interpreter shutdown, which can crash the process ("Fatal Python
# error: _enter_buffered_busy") instead of exiting cleanly. main()
# itself is UNCHANGED (still a plain `return 0`, safe in-process); only
# the actual __main__ script-exit path below escalates to os._exit().
_STDIN_DEADLINE_STATE = {"hit": False}


def main() -> int:
    _reconfigure_stdout_utf8()

    # Byte-safe read via the stdin-deadline helper (replaces a former
    # direct, unbounded sys.stdin.buffer.read()) -- same decode utf-8/
    # errors="replace" fail-open contract, now bounded by
    # OSLLM_STDIN_TIMEOUT instead of blocking forever with no EOF.
    raw_bytes, timed_out = _read_stdin_bytes_deadline()
    if timed_out:
        _STDIN_DEADLINE_STATE["hit"] = True
        try:
            sys.stderr.write(f"{Path(__file__).name}: {_STDIN_DEADLINE_MSG}\n")
        except Exception:
            pass
        return 0
    raw = raw_bytes.decode("utf-8", errors="replace")
    try:
        payload = json.loads(raw)
    except Exception:
        return 0

    return _decide_and_print(payload, gate_allowed=False)


def _decide_and_print(payload, gate_allowed: bool) -> int:
    try:
        exit_code, output = decide(payload, gate_allowed=gate_allowed)
    except Exception:
        # belt-and-suspenders: decide() is already defensively typed,
        # but an adversarial input (e.g. an unexpected shape somewhere
        # deeper) must not crash the hook with a traceback out.
        return 0

    if output is not None:
        sys.stdout.write(json.dumps(output, ensure_ascii=False) + "\n")
    return exit_code


def run_after_gate(payload: dict) -> int:
    """Called by dispatch_gate.main() for a dispatch it ALLOWED: the registry row and the overlap warning
    (printed on stdout as main() prints it; the gate folds it into its own output). Returns the exit code."""
    return _decide_and_print(payload, gate_allowed=True)


if __name__ == "__main__":
    _rc = main()
    if _STDIN_DEADLINE_STATE["hit"]:
        # A stdin-reader thread may still be blocked deep inside a
        # platform read syscall -- normal interpreter shutdown can
        # crash on that. Flush both streams defensively, then exit
        # immediately without running the normal shutdown sequence.
        try:
            sys.stdout.flush()
        except Exception:
            pass
        try:
            sys.stderr.flush()
        except Exception:
            pass
        os._exit(_rc)
    sys.exit(_rc)
