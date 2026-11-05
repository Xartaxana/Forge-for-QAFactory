"""dispatch_gate.py -- PreToolUse hook for the Task/Agent tool that
checks the SHAPE of a dispatch before it goes out, enforcing two
CLAUDE.md rules in code rather than relying on discipline alone:
rule 11 (DoD-in-every-dispatch / dispatch-context-manifest) and rule 7
(the dispatch label starts with the worker's tier).

B-201 (spec docs/tasks/specs/t-090-dispatch-manifest.md): checks 1 and 2
below are REPLACED in decide() by tools/dispatch_manifest.py's completeness
check; the text of checks 1-2 below is the HISTORY of what decide() did
before. Their WARN companions (write_quoted_warn, dod_quoted_warn,
manifest_quoted_warn, WRITE_INDICATORS_RE, the BLOCK_MESSAGE_NO_* constants)
stay in the file; decide() no longer uses them, so a layer fires only where
a passing or unchecked dispatch still reaches it.

B-204 / B-245 (t-608, Axis 13): ONE cut, N readers, and the paths are checked
before the send. decide_full(payload) -> Decision(code, message, notes, paths,
...) builds the cut of the prompt ONCE (dispatch_manifest.cut_payload ->
section_cut), runs the completeness check on it (dispatch_manifest.check_cut)
and, for a dispatch that check evaluated (a builder or a writing one), the
PATH CHECK on the same cut: every given path must exist under the root
(payload["cwd"], never os.getcwd()), every owns path must exist or carry
`(new)`; a refusal (exit 2) names the missing paths, the root and the doors
(`(new)` for an owns path the worker creates, a merge of the file an earlier
node made, `manifest-skip: given|owns -- <reason>`). Order: completeness ->
paths -> label (3). The path check refuses only from a complete read, a
bare-declaration header, a line outside an unterminated fence and a certain
path; everything else (no cwd, a degraded read, a cap of 200 paths, a header
with prose between key and colon, an exception inside the check) is a NOTE
and the dispatch goes out. decide() = (code, message) of decide_full -- the
form owns_gate and critic_snapshot call, so a dispatch refused on a path leaves
no registry line and no snapshot. main() calls decide_full ONCE and prints the
notes and the path printout (path, bytes, lines) as additionalContext.

An exception out of the completeness check inside decide_full means "not
checked" and the label check (3) still runs; decide_full itself can still raise
on a non-string `description` (the label regex), so its callers guard it: main()
below, owns_gate and critic_snapshot each in a try/except. main() adds the
check's SKIP NOTE / UNCHECKED NOTE to additionalContext; a malformed-JSON or
timed-out stdin, a payload that is not a JSON object, a tool_input that is not
one, or ANY exception out of decide_full gives exit 0 with the UNCHECKED NOTE
(additionalContext and stderr). Empty stdin and a TTY stay silent (exit 0,
no output). A real refusal (exit 2) is never turned into exit 0.

Contract (PreToolUse hook stdin JSON): {"tool_name": str,
"tool_input": {"subagent_type": str, "prompt": str,
"description": str}, "cwd": str, ...}. Only tool_name in
{"Task", "Agent"} is inspected -- any other tool passes silently
(exit 0, no output). Exit 2 with a message on stderr blocks the call;
exit 0 allows it. The completeness gate is stateless: it never reads or
writes any file, it only inspects the payload it was given. The PATH CHECK
(decide_full) stats files and lists the root's top-level names under
payload["cwd"] (existence only; sizes and line counts are computed in
main() alone), and the given-path WARN layer below reads the filesystem the
same way; neither writes anything.
The token-budget layer (t-575, below) is NOT stateless: the parallel cap
reads the session's subagents folder under ~/.claude/projects (file
mtimes, and the tail of each recent transcript to leave finished workers
out -- both through tools/transcripts.py, the one reader of worker
transcripts), and the push-before-launch WARN runs `git rev-list` / `git rev-parse`
in the hook's cwd. It writes nothing; every error there is fail-open.

Cross-reference (a live example of a two-condition detector, see
critic.md's scoping-of-paired-conditions review norm): check 2 below
requires BOTH a given-marker and an owns-marker present in the SAME
prompt to count as a real manifest -- verifying each half in isolation
(a given-marker anywhere, an owns-marker anywhere, even from unrelated
mentions) would be exactly the false cross-match that norm warns
against.

Checks (blocking gate):
 1. subagent_type == "builder": tool_input["prompt"] must contain a
    DoD marker (DOD_MARKERS_RE). None found -> BLOCK
    (BLOCK_MESSAGE_NO_DOD).
 2. subagent_type == "builder" AND the prompt shows a write indicator
    -- a conservative heuristic: block ONLY when a write indicator is
    present AND BOTH manifest markers (MANIFEST_GIVEN_RE and
    MANIFEST_OWNS_RE) are missing -> BLOCK (BLOCK_MESSAGE_NO_MANIFEST).
    No write indicator -> check 2 is skipped entirely (a read-only
    dispatch needs no manifest). The write indicator is EITHER a match
    of WRITE_INDICATORS_RE (four write verbs -- see "Write-indicator
    discriminator" below for why the bare word "owns" is NOT one of
    them any more) OR owns_declaration_has_path_token(prompt) -- an
    owns: HEADER line that actually carries an absolute path, not
    just the bare word (see "One owns predicate" below).
 3. ANY subagent_type (including critic/scout): tool_input["description"],
    IF PRESENT, must start with a leading token followed by a
    separator ([ :-]) -- LABEL_MODEL_PREFIX_RE below. This is a FORM
    check only, on purpose: this template has no fixed list of tier/
    model names (a deployment configures its own bindings in
    delegation.config.yaml), so the hook can only verify that the
    label carries *some* leading tag-like token, not that the token
    names a real tier. description absent from the payload -> check 3
    is skipped.
 4. critic/scout (any subagent_type != "builder") -- checks 1 and 2 do
    not apply to them; their own DoD shape is different (rule 11
    describes it in prose, not as a prompt-text pattern).

Priority when several checks fail at once: 1 -> 2 -> 3, the first one
found is the single stderr message (the hook blocks with one message,
not a list).

Fail-open on a payload that isn't valid JSON -- same principle as
every other hook in this file set: a hook that can't parse its input
must not block an unrelated tool call.

Marker word-boundary hardening: DOD_MARKERS_RE's "DoD"/"witness"
alternatives, and MANIFEST_GIVEN_RE/MANIFEST_OWNS_RE, are \\b-bounded
so a marker only matches as a standalone word, not as a substring
inside an unrelated longer token -- three concrete classes this
closes: a bare filename mentioning "dod" in the given basket (e.g.
"tools/dod_gate.py") no longer counts as a DoD marker; a filename
mentioning "witness" (e.g. "test_witness_echo.py") no longer counts as
a witness marker; an ordinary longer Cyrillic word that merely
CONTAINS the short Cyrillic given-marker root as a substring no longer
counts as a given-marker (same class as the write-indicator fix
below), and a filename merely containing "owns" as a substring no
longer counts as an owns-marker. The multi-word Cyrillic/English
alternatives (an acceptance-criteria phrase, a verification-run
phrase) are not bounded the same way: they are phrases with an
internal space, and no realistic filename/token in this repo's basket
contains that exact sequence of words as a false-positive substring,
so adding \\b there would be an unmotivated widening of the class the
substring bugs above actually belong to.

--- Write-indicator discriminator (owns as a path, not as a word) ---
Earlier, WRITE_INDICATORS_RE carried a bare "\\bowns\\b" alternative:
the WORD "owns" appearing anywhere in the prompt (a read-only recon
dispatch discussing the owns mechanism itself, a quote of rule 11, a
mention of this very file's name) counted as a write indicator. That
is too coarse: the word "owns" as a topic is not the same fact as a
prompt that actually DECLARES an owns path. "\\bowns\\b" is REMOVED
from WRITE_INDICATORS_RE; a writing dispatch is now detected either by
one of the four write verbs, or by owns_declaration_has_path_token()
below finding an absolute path on an "owns:" header line.

is_path_like_token(tok) -- a single, shared predicate for "does this
token look like a real path": a Windows absolute path (drive letter +
":" + slash), a POSIX absolute path (leading "/"), or a glob carrying
BOTH "*" and a slash. A bare "*" with no slash (e.g. markdown
"**bold**") is deliberately NOT a path -- a naive "any token with a
`*`" predicate would treat ordinary bold-text markup in a manifest
paragraph as a path token.

--- One owns predicate (t-855, forge F6-8; SIBLING_MAP axis 13) ---
"Does this dispatch, or this worker, own a path" has ONE answer in tools/,
given by dispatch_manifest.has_owned_paths(text) on the one cut of the text
(section_cut + owned_paths). owns_declaration_has_path_token(prompt) -- the
write predicate of check 2, of is_writing_dispatch (the dispatch side of the
parallel-writer limit, D-0040) and of transcripts.is_writer (the worker
side) -- is a thin call to it; handoff_gate asks the same of its own cut.
There is no second header grammar and no second path rule in this file.
The rule, for every reader of the class:
 * the owns marker counts only as a HEADER line: `owns` is the line's key
   (at line start after an optional bullet / bold / heading mark) with a
   colon within 160 characters, the paths on that line or on the lines
   right under it (the R11-f form). A line that merely SAYS "owns"
   ("owns/non-goals/queue lines", "C3-12 owns /tools/x.py") is prose, not a
   declaration: a reader whose prompt talks about owns stays a reader;
 * a declaration carries an ABSOLUTE path. An owns of relative paths only
   ("owns: tools/x.py", "owns: tools/*.py") is NOT a path declaration --
   the worker is a reader for the limit AND for handoff_gate (locked to its
   one handoff: file), never a writer on one side and a reader on the other;
 * the one pinned widening, the limit's side only: an owns header with an
   absolute path INSIDE a fence or blockquote counts (include_quoted=True),
   the t-847 answer -- the limit counts a worker rather than let a fifth
   writer through on a quoted example. check 2's region-aware twin leaves
   quoted owns out, as it always did.
A worker's kind is the sidecar meta's agentType first ("builder" is a
writer whatever its prompt says); every other kind, and an absent or bad
meta, is decided by this predicate on its first user line; an unknown kind
with no readable first line is counted as a writer (the cap's error
direction).

--- Role-type WARN layer (declared tier vs. loaded agent role) ------
A SEPARATE, informational-only layer, symmetric with the given-path
layer below: it never blocks (never returns exit 2, never adds a
permissionDecision), it only adds text to additionalContext, and only
when decide() has already returned (0, ""). Motivation: the dispatch
label's leading token (LABEL_MODEL_PREFIX_RE) is a self-declared tier
("opus: review the diff"), but the tier ACTUALLY applied to the
worker session is whatever role file loads for tool_input's
subagent_type -- and those two facts can silently diverge (a
subagent_type with no matching role file at all, e.g. "general-
purpose", runs with no role instructions loaded even though its label
claims a specific tier).

role_type_warn(payload) resolves subagent_type against
`.claude/agents/*.md` in THIS repo (AGENTS_DIR, a fixed path relative
to this script's own location, not to payload["cwd"] -- the agent
role files are a fixed asset of this deployment, not something named
in dispatch text): a role file's STEM (filename without ".md") or its
frontmatter `name:` field, matched case-insensitively with surrounding
quotes stripped, identifies the role; filename match takes priority
over a `name:` field match (closer to how the harness itself resolves
subagent_type -> role file). The role file's frontmatter `model:`
field gives its bound model; the same substring family heuristic used
elsewhere in this tool set (haiku/sonnet/opus/fable) reduces it to a
tier family and compares that against the label's declared family.

Edges (all silent, no WARN): description absent/not a string/empty;
a label with the "claude" prefix (no family can be inferred);
subagent_type absent/not a string/blank; the `.claude/agents/`
directory itself missing entirely (a fresh checkout with no role
files yet -- this layer is purely informational, warning on every
single dispatch in that state would be noise with no corresponding
enforcement value); a role file found but with no `model:` line
(a known role with an unstated model -- not the same fact as "role
unknown"); a `model:` value that doesn't resolve to a known family
(e.g. a bare "claude" or a custom id); families that match. A role
file that IS found for the subagent_type, but whose declared family
differs from the label -- WARN (mismatch). No role file found at all
for a real subagent_type -- WARN (unknown role). Any exception inside
this layer is swallowed -- fail-open, the same posture as
given_path_warn().

Two WARNs in one call are joined into ONE additionalContext string
("\\n\\n"-joined, given-path first, role-type second) -- the harness
parses a hook's response as a single JSON object, so two separate
JSON blobs on stdout would not both be read.

--- Given-path WARN layer -------------------------------------------
A WARN layer on top of the blocking gate above: exit-2 branches of
decide() (checks 1/2/3 and the path check) are NOT touched by this layer.
given_path_warn() is a SEPARATE function; decide() never calls it and
its result never participates in the exit code. main() calls it ONLY
when decide_full has not blocked -- if the gate blocks, we don't go
further (no WARN is printed in that case, by design: the blocking
message already tells the dispatcher what to fix). The result is ONLY an
additionalContext JSON on stdout; main()'s exit code stays 0 on this
branch. Scope since B-245: the sections of a checked (builder or writing)
dispatch are covered by the PATH CHECK, so this layer reads only the lines
OUTSIDE them (decision.covered); any other dispatch keeps it over the whole
prompt. Quoted lines (cut.quoted) are not read.

Extraction (extract_given_candidates -> dispatch_manifest.path_candidates):
ONE predicate "is this word a path", shared with the PATH CHECK and the
freshness layer's relative anchors. A candidate is --
 (a) an absolute path (a drive or a leading slash), or
 (b) a backticked span with a slash and no whitespace (a span with
     whitespace only when it is absolute), or
 (c) a word whose first segment is an existing top-level entry of the
     root (top_level_entries(root), listed by the caller: the predicate
     itself does no I/O).
Never a candidate: a URL, a placeholder (`<x>` `{x}` `$X`), prose. An anchor
after an extension (`:12-30`, `~:5`, `::t`, `#L9`) and trailing `. , ) ;`
are stripped, the drive colon kept; a note in brackets is a separate word
and never part of the path. There is no length truncation of a token and no
fixed prefix list (the former repo-relative regexes are gone). The root is
payload["cwd"]; without it the layer is silent (never os.getcwd()).

Known root and foreign trees: an absolute path candidate is checked
ONLY if it lies INSIDE the CURRENT dispatch's own cwd (payload["cwd"],
the same reference point this repo's other sidecar checks already
use) -- `_is_under_root`, a normcase+normpath comparison. An absolute
path OUTSIDE that root (any other drive/tree) is not checked at all,
neither warned about nor treated as an error: a dispatch can
legitimately mention absolute paths belonging to a different
deployment or a sibling repo, and this layer has no way to tell
whether those exist without walking a filesystem it has no business
walking.

Noise threshold (GIVEN_PATH_WARN_SUMMARY_THRESHOLD = 10,
format_given_path_warn): <= 10 missing paths -> the full list; > 10 ->
a summary ("N paths do not exist, first 3: ..."); both branches print
a WARN, only the FORM differs -- a silent no-op above the threshold
would make the summary-format text dead code.

Fail-open: given_path_warn() returns "" on any unrecognized payload/
tool_input/prompt; main() additionally wraps the call in try/except
(belt-and-suspenders) -- an adversarial input must not crash the
BLOCKING hook over a WARN-layer failure.

--- Region-aware filtering (md_regions integration) -------------------
A guard cannot tell an author's own claim from quoted/nested content:
a bare regex match on DoD/given/owns/write markers does not know
whether it landed in the dispatcher's own prose or inside a fenced/
quoted EXAMPLE of someone else's manifest. toolkit/tools/md_regions.py
(imported below, try/except -- ImportError degrades this whole layer
to bare-regex behavior, see I-0 below) splits the prompt into regions
(prose / fenced / blockquote / inline_code); `_is_quoted(region)` is
the single polarity used by every layer in this file: fenced OR
blockquote -> quoted (excluded/flagged), prose and inline code are NOT
quoted (a manifest written in backticks, e.g. "owns: `D:/x.py`", still
counts) -- the same polarity given_path_warn already uses for its own
candidates. An UNTERMINATED fence is read as prose, not a quote (before
any other branch): treating it as a quote would only ever WIDEN the
silent zone, which is the wrong default for an ambiguous case.

I-0 (any md_regions failure -- ImportError, an exception inside
scan(), or a degraded=True result): every region-aware function below
falls back to the exact bare-regex behavior this file had before this
layer existed -- byte for byte. decide()'s check 2 (B2-write) is the
one branch where this file's exit code can legitimately change from
its pre-region-aware behavior: a write verb / owns-declaration whose
ONLY occurrence sits inside a quote no longer counts as a write
signal (`_region_aware_is_write`) -- this can only LOOSEN the block,
never tighten it (checks 1/3 and the given/owns manifest test itself
are untouched). Three new WARN-only layers make that direction
visible instead of silent: dod_quoted_warn/manifest_quoted_warn (the
ONLY marker match found is inside a quote -- decide() still counted
it, by design, this just flags it for a manual look) and
write_quoted_warn (the one case where a write signal WAS quoted-out of
check 2 with no given/owns marker present at all -- the quiet flip
gets a WARN so it is never a silent pass).

freshness_warn() (below) reuses the SAME scan()/_is_quoted() pair for
its own line-anchor check but does NOT get the bare-regex I-0
fallback: with no region info at all, the whole layer stays silent
(a dispatch text with no anchor/check-token candidate never touches
the filesystem or the scanner in the first place -- a cheap
"any candidate at all" prefilter runs before scan() is called).
"""

import bisect
import contextlib
import hashlib
import importlib
import io
import json
import os
import re
import sys
import subprocess
import threading
import time
from datetime import datetime
from pathlib import Path
from typing import NamedTuple

try:
    from tools.md_regions import scan, KIND_FENCED, KIND_BLOCKQUOTE  # package-style
except ImportError:
    try:
        from md_regions import scan, KIND_FENCED, KIND_BLOCKQUOTE  # sibling-module fallback
    except ImportError:
        scan = None
        KIND_FENCED = "fenced"
        KIND_BLOCKQUOTE = "blockquote"


def _transcripts_import_failed(exc: Exception):
    """transcripts present but broken (SyntaxError, an error at import time, a ModuleNotFoundError of ANOTHER
    module inside it) must not kill this hook nor pass in silence: ONE stderr line (class + the message squeezed
    to a line and cut); the parallel cap then counts every fresh file live and says so in its own sentence
    (TRANSCRIPTS_MISSING), t-844. transcripts ITSELF absent (ModuleNotFoundError named transcripts) stays
    silent on stderr, as before -- the cap's sentence still says so."""
    if isinstance(exc, ModuleNotFoundError) and exc.name == "transcripts":
        return None
    detail = " ".join(str(exc).split())[:60]
    print("dispatch_gate: transcripts did not import (%s: %s); the parallel cap counts every fresh worker file "
          "live" % (type(exc).__name__, detail), file=sys.stderr)
    return None


try:
    from tools import transcripts  # package-style
except ImportError:  # absent as a package: the sibling path still gets its try
    try:
        import transcripts  # sibling-module fallback (also what the mechanism net's import walk sees)
    except Exception as _exc:  # absent here too, or present but broken
        transcripts = _transcripts_import_failed(_exc)
except Exception as _exc:  # present as a package but broken
    transcripts = _transcripts_import_failed(_exc)

# Fixed asset of this deployment -- see the module docstring,
# "Role-type WARN layer": the path is relative to this script's own
# location, not to payload["cwd"].
AGENTS_DIR = Path(__file__).resolve().parents[1] / ".claude" / "agents"

DOD_MARKERS_RE = re.compile(
    r"\bDoD\b|acceptance criteria|критери[ия] приёмки|\bwitness\b|"
    r"verification run|проверочн\w+ прогон",
    re.IGNORECASE,
)
# \b-bounded so a marker only matches as a whole word -- otherwise a
# short Cyrillic root (see WRITE_INDICATORS_RE below) would also
# match inside unrelated longer words sharing that root. "owns" is
# deliberately NOT one of these alternatives any more -- see the module
# docstring, "Write-indicator discriminator", for why the bare word is
# too coarse a signal and what replaces it
# (owns_declaration_has_path_token below).
WRITE_INDICATORS_RE = re.compile(
    r"\bwrite file\b|\bcreate file\b|\bedit file\b|\bmodify file\b|"
    r"\bзапиши\b|\bсоздай файл\b|\bправь\b|\bизмени файл\b",
    re.IGNORECASE,
)
# \b-bounded: an ordinary, longer Cyrillic word that merely CONTAINS
# the short given-marker root as a substring (e.g. an unrelated word
# meaning "sold out") must not count as a given-marker, same class as
# the write-indicator fix above.
MANIFEST_GIVEN_RE = re.compile(r"\bgiven\b|\bдано\b", re.IGNORECASE)
# \b-bounded: a filename merely containing "owns" as a substring in the
# given basket must not count as an owns-marker.
MANIFEST_OWNS_RE = re.compile(r"\bowns\b", re.IGNORECASE)
# Portable form check (see module docstring, check 3): a leading
# non-whitespace token followed by a separator. Deliberately NOT a
# fixed list of model/tier names -- this template doesn't know a
# deployment's actual bindings.
LABEL_MODEL_PREFIX_RE = re.compile(r"^\S+[ :-]")

# --- Write-indicator discriminator: a shared "is this a path token"
# predicate -- see the module docstring, "Write-indicator
# discriminator", for the full contract and rationale.
#
# ROOT-ONLY GUARD (route port, node D1, staff twin tools/dispatch_gate.py
# ~:863-884): both absolute regexes require >=1 SEGMENT character
# (not a slash, not whitespace) right after the root slash -- a bare
# root with no segment ("/", "//", "D:\\", "D:/") is not itself a path
# token. Before this guard, "/" and "D:\\" matched as valid path
# tokens: normalize_path("/") self-intersects with any other stray
# "/" in a prompt (a false owns-overlap-shaped positive on nearly any
# text carrying a bare slash), and "D:\\"/"D:/" normalize to "d:" --
# an intersection with the ENTIRE D: drive. A rootless phantom root is
# not an owned path in any practical sense. Only the ROOT-WITHOUT-A-
# SEGMENT class is excluded here -- a doubled root WITH a segment
# ("//foo", "//server/share", "D://x") still counts (the segment is
# present); "/etc" (one segment, no extension) is a token, "/" alone
# is not -- both edges are tested (rule 6a). The glob branch below
# ("*" + a slash) is unaffected -- this guard only narrows the two
# absolute-path regexes, checked first, same order as before.
_PATH_TOKEN_WIN_ABS_RE = re.compile(r"^[A-Za-z]:[\\/]+[^\\/\s]")
_PATH_TOKEN_POSIX_ABS_RE = re.compile(r"^/+[^/\s]")


def is_path_like_token(tok) -> bool:
    """The single, shared predicate for "does this token look like a
    path": a Windows absolute path (drive letter + ":" + slash + a
    segment), a POSIX absolute path (leading "/" + a segment -- see
    "ROOT-ONLY GUARD" above), or a glob carrying BOTH "*" and
    a slash ("/" or "\\"). A bare "*" with no slash (e.g. markdown
    "**bold**") is NOT a path -- see the module docstring for the
    false-positive this excludes."""
    if not isinstance(tok, str) or not tok:
        return False
    if _PATH_TOKEN_WIN_ABS_RE.match(tok) or _PATH_TOKEN_POSIX_ABS_RE.match(tok):
        return True
    return "*" in tok and ("/" in tok or "\\" in tok)


def owns_declaration_has_path_token(prompt: str) -> bool:
    """The write predicate (check 2's signal, the parallel-writer limit through is_writing_dispatch, and
    transcripts.is_writer's injected predicate): a THIN call to the one reader of owned paths,
    dispatch_manifest.has_owned_paths(prompt, include_quoted=True) -- the owns HEADER grammar and the
    absolute-path rule live there and nowhere else (t-855, F6-8; see the module docstring, "One owns
    predicate"). Not a str / empty -> False. A dispatch_manifest that does not import RAISES: is_writer's caller
    (transcripts.live_worker_files) counts such a worker live, and parallel_cap_check's caller is fail-open."""
    if not isinstance(prompt, str) or not prompt:
        return False
    return _load_manifest_module().has_owned_paths(prompt, include_quoted=True)


# =======================================================================
# Region-aware helpers (md_regions integration) -- see the module
# docstring, "Region-aware filtering", for the full design rationale.
# =======================================================================


def _safe_scan(text: str):
    """I-0: None on a missing module / an exception inside scan() /
    degraded=True -- three failure shapes collapse to one "no region
    info" signal, so every caller below has exactly one fallback
    branch to write."""
    if scan is None:
        return None
    try:
        result = scan(text)
    except Exception:
        return None
    if result.degraded:
        return None
    return result


def _region_at(scan_result, offset: int):
    """bisect over scan_result.regions -- mirrors md_regions.kind_at(),
    but returns the WHOLE Region (needed for .unterminated, see
    _is_quoted)."""
    regions = scan_result.regions
    if not regions:
        return None
    starts = [r.start for r in regions]
    idx = bisect.bisect_right(starts, offset) - 1
    if idx < 0:
        return None
    region = regions[idx]
    if region.start <= offset < region.end:
        return region
    return None


def _is_quoted(region) -> bool:
    """The single "quoted" polarity used by every region-aware layer in
    this file -- see the module docstring, "Region-aware filtering".
    region is None (end of text / outside coverage) -> NOT quoted (the
    prose default). An unterminated fence -> NOT quoted (checked
    BEFORE any other branch -- ambiguity must not widen the silent
    zone). Otherwise: fenced OR blockquote in kinds -> quoted; inline
    code and prose are NOT quoted (backticks don't silence a real
    manifest declaration)."""
    if region is None:
        return False
    if KIND_FENCED in region.kinds and region.unterminated:
        return False
    if KIND_FENCED in region.kinds or KIND_BLOCKQUOTE in region.kinds:
        return True
    return False


_QUOTE_TRIGGER_CHARS = "`>~"


def _prompt_has_quote_trigger(prompt: str) -> bool:
    """Cheap prefilter: without one of these characters anywhere in the
    text, no region can possibly be fenced/blockquote -- the same fact
    md_regions._no_markers_whole_text() uses internally."""
    return any(ch in prompt for ch in _QUOTE_TRIGGER_CHARS)


def _region_aware_write_indicator_present(prompt: str, scan_result) -> bool:
    """True when at least one WRITE_INDICATORS_RE match sits OUTSIDE a
    quote. scan_result is None -> I-0 fallback, bare bool(search())."""
    if scan_result is None:
        return bool(WRITE_INDICATORS_RE.search(prompt))
    for m in WRITE_INDICATORS_RE.finditer(prompt):
        if not _is_quoted(_region_at(scan_result, m.start())):
            return True
    return False


def _region_aware_owns_declaration_has_path_token(prompt: str, scan_result) -> bool:
    """Region-aware twin of owns_declaration_has_path_token() above -- the SAME reader
    (dispatch_manifest.has_owned_paths), with ONE difference: a quoted owns declaration does not feed
    check 2 (include_quoted left False). scan_result is None -> I-0 fallback to the bare function above."""
    if scan_result is None:
        return owns_declaration_has_path_token(prompt)
    return _load_manifest_module().has_owned_paths(prompt)


def _region_aware_is_write(prompt: str) -> bool:
    """decide()'s check-2 write signal -- replaces the bare
    `bool(WRITE_INDICATORS_RE.search(prompt)) or
    owns_declaration_has_path_token(prompt)` computation. Two-part cheap
    prefilter before scan() is ever called: (a) a bare marker hit (the
    same pair of predicates decide() already computed) -- nothing found
    -> False, scan() not called; (b) no quote-trigger character
    anywhere in the text -- nothing to filter, the bare True result is
    returned directly. Only when BOTH conditions hold does scan() run,
    exactly once."""
    bare_write = bool(WRITE_INDICATORS_RE.search(prompt))
    bare_owns = owns_declaration_has_path_token(prompt)
    if not (bare_write or bare_owns):
        return False
    if not _prompt_has_quote_trigger(prompt):
        return True
    scan_result = _safe_scan(prompt)
    if scan_result is None:
        return True  # I-0: same bare result that gave True above
    return _region_aware_write_indicator_present(
        prompt, scan_result
    ) or _region_aware_owns_declaration_has_path_token(prompt, scan_result)


BLOCK_MESSAGE_NO_DOD = (
    "A builder dispatch with no DoD does not go out (rule 11): add "
    "acceptance criteria and a verification run whose output becomes "
    "the witness."
)
BLOCK_MESSAGE_NO_MANIFEST = (
    "A writing dispatch with no context manifest (given/owns) does not "
    "go out (rule 11, dispatch-context-manifest rule)."
)
BLOCK_MESSAGE_NO_LABEL = (
    "The dispatch label starts with the worker's tier (rule 7): "
    "e.g. 'sonnet: ...'."
)


def _load_manifest_module():
    """The completeness-check module (tools/dispatch_manifest.py), imported
    LAZILY -- only a Task/Agent call pays for it, and dispatch_manifest
    itself imports this module lazily inside its check(), so no import
    cycle exists at load time. The tools directory (this file's own) is put
    on sys.path first, the same way dispatch_manifest does it, so the
    sibling import resolves under every entry point (a script run, a test,
    critic_snapshot's package-style import). A failed import raises."""
    tools_dir = str(Path(__file__).resolve().parent)
    if tools_dir not in sys.path:
        sys.path.insert(0, tools_dir)
    import dispatch_manifest

    return dispatch_manifest


class PathReport(NamedTuple):
    path: str
    kind: str  # "given" | "owns"
    status: str  # ok | new | glob | outside | missing | unchecked
    full: str


class Decision(NamedTuple):
    code: int
    message: str
    notes: list
    paths: list
    stderr_note: str = ""
    cut: object = None
    covered: object = None  # per-line 1 = inside a checked section (None = no checked sections)


PATH_NOTE = "PATH CHECK: "
PATH_MISSING_TEMPLATE = (
    "DISPATCH PATHS MISSING (CLAUDE.md rule 11): this {kind} dispatch does not go out. "
    "These paths do not exist under the root {root}: {items}. Expected: every given path "
    "exists and every owns path exists or is marked new. Doors: write (new) right after an "
    "owns path this worker creates ((new) is for owns only; a given path must exist); or "
    "merge the file an earlier node created; or add a line: manifest-skip: given|owns -- <reason>."
)
_ABS_PATH_START_RE = re.compile(r"^(?:[A-Za-z]:[\\/]|/)")


def top_level_entries(root):
    """The root's top-level names (both spellings of case) or None when unreadable."""
    try:
        names = os.listdir(root)
    except OSError:
        return None
    return frozenset(names) | frozenset(n.lower() for n in names)


def _covered_lines(cut):
    covered = bytearray(len(cut.lines))
    for secs in cut.sections.values():
        for s in secs:
            covered[s.header_line:s.last_line + 1] = b"\x01" * (s.last_line - s.header_line + 1)
    return covered


def _resolve(path, root):
    full = path if _ABS_PATH_START_RE.match(path) else os.path.join(root, path)
    return os.path.normpath(full)


def _classify_path(kind, path, marked_new, root):
    """(status, full, note) for one path; stats the disk (the only I/O of the check)."""
    full = _resolve(path, root)
    if not _is_under_root(full, root):
        return "outside", full, ""
    if any(c in path for c in "*?["):
        import glob as _glob

        return "glob", full, "%d match(es)" % len(_glob.glob(full))
    if os.path.exists(full):
        note = "%s is marked new but exists" % path if kind == "owns" and marked_new else ""
        return "ok", full, note
    if kind == "owns" and marked_new:
        return "new", full, ""
    return "missing", full, ""


def _path_check(payload, cut, is_builder, dm):
    """(code, message, notes, reports) of the path check (branch A). Exit 2 only from a
    complete read, a bare-declaration header, a line outside an unterminated fence and a
    certain path; every other case is a note or a false pass."""
    root = payload.get("cwd")
    if not isinstance(root, str) or not root.strip():
        return 0, "", [PATH_NOTE + "paths unchecked: no cwd"], []
    top = top_level_entries(root)
    cands = [("owns", o.path, o.is_new, o.line, o.header_line) for o in dm.owned_paths(cut)]
    cands += [("given", g.path, g.marked_new, g.line, g.header_line) for g in dm.given_paths(cut, top)]
    waived = dm.waivers(cut)
    notes, reports, missing, given_new = [], [], [], False
    for item in ("owns", "given"):
        if item in waived and any(c[0] == item for c in cands):
            notes.append(PATH_NOTE + 'the %s paths were not checked on purpose (manifest-skip: %s -- "%s")'
                         % (item, item, waived[item]))
    live = [c for c in cands if c[0] not in waived]
    checked, extra = live[:dm.PATH_CAP], live[dm.PATH_CAP:]
    if extra:
        notes.append(PATH_NOTE + "paths unchecked: %d beyond the first %d" % (len(extra), dm.PATH_CAP))
    for kind, path, marked, line, hline in checked:
        status, full, note = _classify_path(kind, path, marked, root)
        if note:
            notes.append(PATH_NOTE + note)
        if status == "missing":
            why = dm.unsure_reason(cut, hline, line)
            if why:
                notes.append(PATH_NOTE + "paths unchecked: %s: %s" % (why, path))
                status = "unchecked"
            else:
                missing.append("%s: %s" % (kind, path))
                given_new = given_new or (kind == "given" and marked)
        reports.append(PathReport(path, kind, status, full))
    if missing:
        message = PATH_MISSING_TEMPLATE.format(
            kind="builder" if is_builder else "writing", root=root, items="; ".join(missing))
        if given_new:
            message += " ((new) on a given path is ignored: (new) is for owns only.)"
        return 2, message, notes, reports
    return 0, "", notes, reports


def decide_full(payload: dict) -> Decision:
    """The decision with its notes and path reports (main() prints them; owns_gate and
    critic_snapshot keep decide()). Order: completeness check -> path check (branch A,
    B-245) -> label check. The cut is built ONCE (dispatch_manifest.section_cut) and
    shared by the completeness check and the path check. An exception out of the
    completeness check means "not checked"; one out of the path check yields the note
    "paths not checked" and the label check still runs. This function stats files
    (existence only: sizes and line counts are computed in main()). It can still
    raise on a non-string `description` (the label regex); its callers guard it."""
    if not isinstance(payload, dict) or payload.get("tool_name") not in ("Task", "Agent"):
        return Decision(0, "", [], [])
    tool_input = payload.get("tool_input") or {}
    if not isinstance(tool_input, dict):
        return Decision(0, "", [], [])
    description = tool_input.get("description")

    notes, stderr_note, cut, checked, is_builder, dm = [], "", None, False, False, None
    try:
        dm = _load_manifest_module()
        is_builder, cut = dm.cut_payload(payload)
        check_exit, check_message, note, checked = dm.check_cut(cut, is_builder)
        if note:
            notes.append(note)
    except Exception as exc:  # not checked -- fail-open; main() shows the note on stderr too
        check_exit, check_message, checked = 0, "", False
        stderr_note = _unchecked_note("check failed: %s" % type(exc).__name__)
        notes.append(stderr_note)
    if check_exit == 2:
        # The completeness refusal comes first (as old checks 1-2 were).
        return Decision(2, check_message, [], [], stderr_note, cut)

    paths, covered = [], None
    if checked:
        covered = _covered_lines(cut)
        try:
            path_exit, path_message, path_notes, paths = _path_check(payload, cut, is_builder, dm)
            notes.extend(path_notes)
            if path_exit == 2:
                return Decision(2, path_message, notes, paths, stderr_note, cut, covered)
        except Exception as exc:
            notes.append(PATH_NOTE + "paths not checked: %s" % type(exc).__name__)
    elif cut is not None and cut.degraded and (is_builder or dm.owned_paths(cut)):
        notes.append(PATH_NOTE + "paths unchecked: degraded read (%s)" % (cut.reason or "?"))

    if description is not None:
        if not LABEL_MODEL_PREFIX_RE.search(description):
            return Decision(2, BLOCK_MESSAGE_NO_LABEL, notes, paths, stderr_note, cut, covered)
    return Decision(0, "", notes, paths, stderr_note, cut, covered)


def decide(payload: dict) -> tuple[int, str]:
    """(exit_code, stderr_message) of decide_full -- the form owns_gate and
    critic_snapshot call. "" means "write nothing to stderr". Not a pure
    function any more: the path check stats files under payload["cwd"]."""
    decision = decide_full(payload)
    return decision.code, decision.message


_PRINT_LIMIT = 10
_LINE_COUNT_LIMIT = 5 * 1024 * 1024


def _describe(report):
    """One printout line for a path; sizes/lines are computed HERE (main() only)."""
    if report.status == "missing":
        return "%s: %s MISSING" % (report.kind, report.path)
    if report.status in ("outside", "unchecked", "new", "glob"):
        return "%s: %s (%s)" % (report.kind, report.path, report.status)
    try:
        if os.path.isdir(report.full):
            return "%s: %s (directory, %d entries)" % (report.kind, report.path, len(os.listdir(report.full)))
        size = os.path.getsize(report.full)
        if size > _LINE_COUNT_LIMIT:
            return "%s: %s (%d bytes, lines not counted)" % (report.kind, report.path, size)
        with open(report.full, "rb") as fh:
            data = fh.read()
        n = data.count(b"\n") + (1 if data and not data.endswith(b"\n") else 0)
        return "%s: %s (%d bytes, %d lines)" % (report.kind, report.path, size, n)
    except OSError:
        return "%s: %s (unreadable)" % (report.kind, report.path)


def format_path_report(paths):
    """The printout on a pass: one line per path, at most 10 listed, then a summary."""
    if not paths:
        return ""
    lines = [_describe(r) for r in paths[:_PRINT_LIMIT]]
    if len(paths) > _PRINT_LIMIT:
        lines.append("... and %d more path(s) checked" % (len(paths) - _PRINT_LIMIT))
    return PATH_NOTE + "paths checked under the root:\n" + "\n".join(lines)


# --- Given-path WARN layer ------------------------------------------------
# See the module docstring, "Given-path WARN layer", for the full
# design rationale. This layer does NOT participate in decide() and
# does not change the exit code -- a separate function, called ONLY
# from main(), ONLY when decide_full has not blocked; it reads the
# lines outside the checked sections (the PATH CHECK owns those).

GIVEN_PATH_WARN_SUMMARY_THRESHOLD = 10


def extract_given_candidates(prompt: str, top_entries=None, skip=None, quoted=None) -> list:
    """[(path_as_written, is_absolute), ...] -- deduplicated, order of first
    appearance. ONE predicate (dispatch_manifest.path_candidates) line by line;
    lines flagged in `skip` (inside a checked section) or `quoted` are not read."""
    if not isinstance(prompt, str) or not prompt:
        return []
    pc = _load_manifest_module().path_candidates
    seen, out = set(), []
    for i, line in enumerate(prompt.splitlines()):
        if (skip is not None and skip[i]) or (quoted is not None and quoted[i]):
            continue
        for tok in pc(line, top_entries):
            if tok not in seen:
                seen.add(tok)
                out.append((tok, bool(_ABS_PATH_START_RE.match(tok))))
    return out


def _is_under_root(path_str: str, root: str) -> bool:
    """True when path_str lies inside root (root itself included) --
    compared via normcase(normpath(...)) (case-insensitive on Windows,
    separators normalized). See the module docstring, "Known root and
    foreign trees"."""
    try:
        norm_path = os.path.normcase(os.path.normpath(path_str))
        norm_root = os.path.normcase(os.path.normpath(root))
    except Exception:
        return False
    return norm_path == norm_root or norm_path.startswith(norm_root + os.sep)


def _missing_given_paths_from_candidates(candidates: list, repo_root: str) -> list:
    """Existence-check body: absolute candidates outside the root are not checked."""
    missing = []
    for tok, is_abs in candidates:
        full = _resolve(tok, repo_root)
        if is_abs and not _is_under_root(full, repo_root):
            continue
        if not os.path.exists(full):
            missing.append(tok)
    return missing


def find_missing_given_paths(prompt: str, repo_root: str) -> list:
    """The paths of the prompt (any line) that do NOT exist under repo_root."""
    return _missing_given_paths_from_candidates(
        extract_given_candidates(prompt, top_level_entries(repo_root)), repo_root)


def format_given_path_warn(missing: list) -> str:
    """"" on an empty list; otherwise the full form (<=10) or a
    summary (>10) -- see the module docstring, "Noise threshold"."""
    if not missing:
        return ""
    if len(missing) <= GIVEN_PATH_WARN_SUMMARY_THRESHOLD:
        listed = ", ".join(missing)
        return (
            "GIVEN-PATH WARN: the dispatch text names paths that do not "
            f"exist: {listed} -- check the spec's facts against their carrier."
        )
    head = ", ".join(missing[:3])
    return (
        f"GIVEN-PATH WARN: {len(missing)} paths do not exist, first 3: "
        f"{head} -- check the spec's facts against their carrier."
    )


def given_path_warn(payload: dict, decision=None) -> str:
    """"" -- nothing to warn about. Otherwise the WARN text for paths the prompt
    mentions OUTSIDE the checked sections (a builder / writing dispatch's sections
    are checked by the path check in decide_full; any other dispatch keeps this
    layer over the whole prompt). Root = payload["cwd"], never os.getcwd(): without
    a cwd the layer is silent. Quoted lines are not read."""
    if not isinstance(payload, dict) or payload.get("tool_name") not in ("Task", "Agent"):
        return ""
    tool_input = payload.get("tool_input") or {}
    if not isinstance(tool_input, dict):
        return ""
    prompt = tool_input.get("prompt")
    if not isinstance(prompt, str) or not prompt:
        return ""
    repo_root = payload.get("cwd")
    if not isinstance(repo_root, str) or not repo_root:
        return ""
    cut = decision.cut if decision is not None else None
    covered = decision.covered if decision is not None else None
    if cut is None:
        cut = _load_manifest_module().section_cut(prompt)
    candidates = extract_given_candidates(prompt, top_level_entries(repo_root), covered, cut.quoted)
    return format_given_path_warn(_missing_given_paths_from_candidates(candidates, repo_root))


# --- Role-type WARN layer -------------------------------------------
# See the module docstring, "Role-type WARN layer", for the full
# design rationale. Symmetric with the given-path layer above: does
# NOT participate in decide() and does not change the exit code --
# called ONLY from main(), ONLY when decide() has already returned
# (0, "").

ROLE_TYPE_WARN_MISMATCH = (
    "ROLE-TYPE WARN: the dispatch label declares tier '{declared_family}', "
    "but the role file .claude/agents/ for subagent_type='{subagent_type}' "
    "declares model: {bound_model} (family '{bound_family}') -- "
    "a type<->tier mismatch."
)

# Route port, node D1 (staff twin ~:1934/:1943): the single UNKNOWN-ROLE
# message split into two cases with OPPOSITE actions for the reader --
# a project role missing a file is a gap to CLOSE (add the role file),
# a harness built-in type missing a file is EXPECTED (nothing to add;
# just verify the tier separately if it matters). Both share the
# "no role file" substring byte for byte -- same rule-of-three prefix,
# one registry line covers either case, and any test pinning that
# phrase stays green regardless of which branch fires.
ROLE_TYPE_WARN_PROJECT = (
    "ROLE-TYPE WARN: no role file in .claude/agents/ for type "
    "'{subagent_type}' -- the declared tier '{declared_family}' is not "
    "backed by any loaded role, and the worker's actual model can "
    "silently diverge from what's declared -- add a role file with a "
    "model: field for this project role; or, if this is a harness "
    "built-in type not yet in the known list, verify the tier by a "
    "transcript measurement and add the type to the list."
)
ROLE_TYPE_WARN_BUILTIN_TYPE = (
    "ROLE-TYPE WARN: the harness built-in type '{subagent_type}' has no "
    "role file in .claude/agents/ -- expected, not a defect of this "
    "layer, but the declared tier '{declared_family}' stays unconfirmed "
    "and the worker's actual model can diverge from it unnoticed -- "
    "verify the tier by a transcript measurement if the dispatch "
    "decision depends on it."
)

# A CLOSED list of harness built-in subagent types that carry no
# project role file by design (route port, node D1, staff twin's
# _ROLE_TYPE_BUILTIN_HARNESS_TYPES): matched case-insensitively against
# the already-normalized subagent_type_norm. This list can go stale as
# the harness adds types -- that is a finding, not a silent failure:
# a miss falls through to ROLE_TYPE_WARN_PROJECT, whose text literally
# says "or, if this is a harness built-in type not yet in the known
# list ... add the type to the list", not a silent pass.
_ROLE_TYPE_BUILTIN_HARNESS_TYPES = frozenset(
    {"general-purpose", "claude-code-guide", "explore", "plan", "statusline-setup"}
)

_FAMILY_NAMES = ("fable", "opus", "sonnet", "haiku")
# A non-greedy variant of LABEL_MODEL_PREFIX_RE's leading-token check,
# local to this layer: LABEL_MODEL_PREFIX_RE itself (`^\S+[ :-]`,
# greedy) is used unchanged by check 3 above and must not be touched;
# this layer additionally needs the FIRST separator's position (a
# lazy `\S+?` stops at the first match rather than backtracking from
# the end) to read out the leading token itself, not just confirm one
# exists.
_LABEL_LEADING_TOKEN_RE = re.compile(r"^(\S+?)[ :-]")
_FRONTMATTER_BLOCK_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---", re.DOTALL)
_FRONTMATTER_NAME_RE = re.compile(r"^name:\s*(\S+)", re.MULTILINE)
_FRONTMATTER_MODEL_RE = re.compile(r"^model:\s*(\S+)", re.MULTILINE)


def _model_family(model_id) -> str | None:
    """The same substring heuristic used elsewhere in this tool set for
    a bound model's tier family -- implemented locally (this layer
    does not import any other gate module for it)."""
    if not isinstance(model_id, str) or not model_id:
        return None
    low = model_id.lower()
    for fam in _FAMILY_NAMES:
        if fam in low:
            return fam
    return None


def _strip_quotes(token: str) -> str:
    """Strips EXACTLY one pair of surrounding quotes (single or
    double) from a captured token. YAML frontmatter legally writes
    `name: "scout"` / `model: 'sonnet'`; \\S+ captures the quotes
    literally, and an exact comparison against a quoted value would
    otherwise never match. A quote INSIDE the value (not on both edges
    at once) is left untouched -- the condition requires the first and
    last character to match."""
    if len(token) >= 2 and token[0] == token[-1] and token[0] in ("'", '"'):
        return token[1:-1]
    return token


def _read_frontmatter(path: Path):
    """The text of the frontmatter block (between the first and second
    "---" line) of a role file, or None -- the file is unreadable OR
    no frontmatter is anchored there (no opening/closing "---"). Any
    read exception is swallowed here -- see the module docstring,
    "Role-type WARN layer", "Edges"."""
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return None
    m = _FRONTMATTER_BLOCK_RE.match(text)
    return m.group(1) if m else None


def _model_of(frontmatter) -> str | None:
    """The frontmatter's model: value (quotes stripped), None if there
    is no model: line."""
    m2 = _FRONTMATTER_MODEL_RE.search(frontmatter)
    return _strip_quotes(m2.group(1).strip()) if m2 else None


def _find_agent_role_model(subagent_type_norm: str):
    """subagent_type_norm is already .strip().lower(). Returns (True,
    model|None) when a `.claude/agents/*.md` file is found whose
    filename (without ".md") OR frontmatter `name:` field matches
    case-insensitively (surrounding quotes stripped); (False, None) --
    no file matched. model is that file's frontmatter model: value
    (None if the frontmatter is unreadable/unanchored/has no model:
    line) -- "a known role with no stated model" is not the same fact
    as "role unknown".

    PRIORITY: an exact FILENAME match resolves FIRST, before any
    `name:` field match -- closer to how the harness itself resolves
    subagent_type (matched against the FILENAME in the agents
    directory). The `name:` match is tried ONLY if no file in the
    directory matched by filename."""
    candidates = sorted(AGENTS_DIR.glob("*.md"))

    for path in candidates:
        if path.stem.strip().lower() == subagent_type_norm:
            frontmatter = _read_frontmatter(path)
            if frontmatter is None:
                return True, None
            return True, _model_of(frontmatter)

    for path in candidates:
        frontmatter = _read_frontmatter(path)
        if frontmatter is None:
            continue
        m = _FRONTMATTER_NAME_RE.search(frontmatter)
        if m and _strip_quotes(m.group(1).strip()).lower() == subagent_type_norm:
            return True, _model_of(frontmatter)

    return False, None


def role_type_warn(payload: dict) -> str:
    """"" -- nothing to warn about (payload isn't Task/Agent, required
    fields absent/not strings, a "claude:" label, the .claude/agents/
    directory missing, a known role with no model: in its frontmatter,
    or families matching). Otherwise the ready-made WARN text (a
    type<->tier mismatch OR a subagent_type with no role file). See the
    module docstring, "Role-type WARN layer", for the full contract.
    Wrapped entirely in try/except -- fail-open on ANY exception, the
    same posture as the rest of this file's WARN layers."""
    try:
        if not isinstance(payload, dict):
            return ""
        tool_name = payload.get("tool_name")
        if tool_name not in ("Task", "Agent"):
            return ""
        tool_input = payload.get("tool_input") or {}
        if not isinstance(tool_input, dict):
            return ""
        subagent_type = tool_input.get("subagent_type")
        if not isinstance(subagent_type, str) or not subagent_type.strip():
            return ""
        description = tool_input.get("description")
        if not isinstance(description, str) or not description:
            return ""
        if not LABEL_MODEL_PREFIX_RE.search(description):
            return ""
        token_m = _LABEL_LEADING_TOKEN_RE.match(description)
        if not token_m:
            return ""
        declared_family = token_m.group(1).lower()
        if declared_family not in _FAMILY_NAMES:
            # Not a recognized tier family (e.g. "claude:", a custom
            # label token) -- no family to compare, silent.
            return ""
        if not AGENTS_DIR.is_dir():
            # The directory is missing entirely (a fresh checkout) --
            # silent, see the module docstring, "Edges".
            return ""

        subagent_type_norm = subagent_type.strip().lower()
        role_known, bound_model = _find_agent_role_model(subagent_type_norm)
        if not role_known:
            # PROJECT/BUILTIN_TYPE split (route port, node D1): the
            # branching LOGIC (what counts as an unknown role) is
            # untouched -- only the choice of TEXT differs.
            if subagent_type_norm in _ROLE_TYPE_BUILTIN_HARNESS_TYPES:
                return ROLE_TYPE_WARN_BUILTIN_TYPE.format(
                    subagent_type=subagent_type, declared_family=declared_family
                )
            return ROLE_TYPE_WARN_PROJECT.format(
                subagent_type=subagent_type, declared_family=declared_family
            )
        if not bound_model:
            return ""
        bound_family = _model_family(bound_model)
        if bound_family is None or bound_family == declared_family:
            return ""
        return ROLE_TYPE_WARN_MISMATCH.format(
            declared_family=declared_family,
            subagent_type=subagent_type,
            bound_model=bound_model,
            bound_family=bound_family,
        )
    except Exception:
        return ""


# =======================================================================
# "Stricter, WARN-only" layers (route port, node D1): B1 (DoD-marker)
# and B2-manifest (given/owns) checks inside decide() are NOT touched --
# a quoted marker still counts exactly as it does today. These layers
# only INFORM: the sole marker match found sits inside a quote, so
# decide() may have counted a marker that isn't the author's own claim
# -- sanity-check it by hand.
# =======================================================================

_QUOTED_SNIPPET_MAX_LEN = 80

DOD_QUOTED_WARN_MESSAGE = (
    "DOD-QUOTED WARN: the only DoD marker found in this dispatch sits "
    "inside a quote/fence (\"{preview}\") -- check 1 counts it literally "
    "(decide() is untouched), but a quoted marker may be someone else's "
    "text, not the author's own DoD -- verify by hand (rule 11)."
)
MANIFEST_QUOTED_WARN_MESSAGE = (
    "MANIFEST-QUOTED WARN: every occurrence of the manifest marker "
    "'{marker}' found in this dispatch sits inside a quote/fence -- the "
    "declaration may be someone else's example, not the author's own "
    "manifest -- verify by hand (dispatch-context-manifest rule)."
)


def _truncate_snippet(s: str, max_len: int = _QUOTED_SNIPPET_MAX_LEN) -> str:
    s = s.strip()
    if len(s) > max_len:
        return s[:max_len] + "..."
    return s


def dod_quoted_warn(payload: dict) -> str:
    """"" -- nothing to warn about (not Task/Agent, not builder, prompt
    absent/empty, no DoD match at all, no quote-trigger character in
    the text at all, the module is unavailable/degraded, every match
    has at least one UNquoted occurrence). Otherwise -- EVERY
    DOD_MARKERS_RE match sits inside a fenced/blockquote region. Purely
    informational, symmetric with given_path_warn/role_type_warn --
    does not participate in the exit code, called ONLY from main(),
    ONLY when decide() has already returned (0, "")."""
    try:
        if not isinstance(payload, dict):
            return ""
        if payload.get("tool_name") not in ("Task", "Agent"):
            return ""
        tool_input = payload.get("tool_input") or {}
        if not isinstance(tool_input, dict):
            return ""
        if tool_input.get("subagent_type") != "builder":
            return ""
        prompt = tool_input.get("prompt")
        if not isinstance(prompt, str) or not prompt:
            return ""
        matches = list(DOD_MARKERS_RE.finditer(prompt))
        if not matches:
            return ""  # nothing to scan
        if not _prompt_has_quote_trigger(prompt):
            return ""  # no quote-capable character -- nothing can be quoted
        scan_result = _safe_scan(prompt)
        if scan_result is None:
            return ""  # I-0: no region info -- nothing to warn about
        if not all(_is_quoted(_region_at(scan_result, mm.start())) for mm in matches):
            return ""
        preview = _truncate_snippet(matches[0].group(0))
        return DOD_QUOTED_WARN_MESSAGE.format(preview=preview)
    except Exception:
        return ""


def manifest_quoted_warn(payload: dict) -> str:
    """"" -- nothing to warn about (symmetric with dod_quoted_warn
    above). Otherwise -- EVERY MANIFEST_GIVEN_RE match sits inside a
    quote, OR EVERY MANIFEST_OWNS_RE match sits inside a quote (given
    is checked first -- matches decide()'s has_manifest = given AND
    owns order). scan() is called AT MOST once -- computed once, reused
    for both checks."""
    try:
        if not isinstance(payload, dict):
            return ""
        if payload.get("tool_name") not in ("Task", "Agent"):
            return ""
        tool_input = payload.get("tool_input") or {}
        if not isinstance(tool_input, dict):
            return ""
        if tool_input.get("subagent_type") != "builder":
            return ""
        prompt = tool_input.get("prompt")
        if not isinstance(prompt, str) or not prompt:
            return ""
        given_matches = list(MANIFEST_GIVEN_RE.finditer(prompt))
        owns_matches = list(MANIFEST_OWNS_RE.finditer(prompt))
        if not given_matches and not owns_matches:
            return ""  # neither given nor owns -- nothing to scan
        if not _prompt_has_quote_trigger(prompt):
            return ""  # no quote-capable character
        scan_result = _safe_scan(prompt)
        if scan_result is None:
            return ""  # I-0: no region info -- nothing to warn about
        if given_matches and all(
            _is_quoted(_region_at(scan_result, mm.start())) for mm in given_matches
        ):
            return MANIFEST_QUOTED_WARN_MESSAGE.format(marker="given")
        if owns_matches and all(
            _is_quoted(_region_at(scan_result, mm.start())) for mm in owns_matches
        ):
            return MANIFEST_QUOTED_WARN_MESSAGE.format(marker="owns")
        return ""
    except Exception:
        return ""


# --- The one case where the region filter can flip decide()'s exit
# code with no manifest marker present at all -- see the module
# docstring, "Region-aware filtering": a write verb / owns-declaration
# whose ONLY occurrence is quoted, and neither given nor owns appears
# ANYWHERE else in the prompt. dod_quoted_warn/manifest_quoted_warn
# both stay silent in that case (nothing to flag -- no marker match
# exists at all). This layer signals the flip itself, so it is never a
# silent pass: the bare (pre-region) file would have blocked this same
# dispatch.
WRITE_QUOTED_WARN_MESSAGE = (
    "WRITE-QUOTED WARN: the only write signal found in this dispatch "
    "(a write verb / owns-declaration) sits inside a quote/fence -- the "
    "region filter lifted check 2's block, and no given/owns manifest "
    "marker appears anywhere in the text either -- this is not a silent "
    "pass: a bare-regex gate would have blocked this same dispatch -- "
    "verify by hand (dispatch-context-manifest rule)."
)


def write_quoted_warn(payload: dict) -> str:
    """"" -- nothing to warn about (not Task/Agent, not builder, prompt
    absent/empty, the bare write signal was never True -- no flip is
    even possible, ANY manifest marker (given OR owns) is present
    somewhere -- that case is already flagged by manifest_quoted_warn,
    silent here to avoid a duplicate message, the region-aware write
    signal stayed True -- no flip happened). Otherwise -- the bare
    write signal was True, the region-aware one became False, and no
    manifest marker exists at all -- the region filter silently lifted
    the block; this layer signals the flip itself."""
    try:
        if not isinstance(payload, dict):
            return ""
        if payload.get("tool_name") not in ("Task", "Agent"):
            return ""
        tool_input = payload.get("tool_input") or {}
        if not isinstance(tool_input, dict):
            return ""
        if tool_input.get("subagent_type") != "builder":
            return ""
        prompt = tool_input.get("prompt")
        if not isinstance(prompt, str) or not prompt:
            return ""
        bare_is_write = bool(WRITE_INDICATORS_RE.search(prompt)) or owns_declaration_has_path_token(
            prompt
        )
        if not bare_is_write:
            return ""
        if MANIFEST_GIVEN_RE.search(prompt) or MANIFEST_OWNS_RE.search(prompt):
            return ""  # a manifest marker exists -- covered by manifest_quoted_warn
        if _region_aware_is_write(prompt):
            return ""  # no flip -- the region-aware signal is also True
        return WRITE_QUOTED_WARN_MESSAGE
    except Exception:
        return ""


# =======================================================================
# FRESHNESS layer (route port; staff twin's own FRESHNESS node):
# one of the staff twin's two anchor classes is ported -- class (v),
# "a <path>.<ext>:N[-M] anchor points past the end of the real file".
# The staff twin's OTHER class, "check NN(x) references a nonexistent
# calibration-protocol subpoint", is NOT ported this increment: it
# depends on a `<!--CHK NN|-->` machine-anchor convention inside
# WEEKLY_CALIBRATION_PROTOCOL.md that the kit's OWN copy does not carry
# yet (measured: 0 occurrences of "CHK" in
# toolkit/PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md vs. 64 in the staff
# twin) -- adopting that anchor convention is a decision for node C4
# (which owns that file), not this node; porting the check-number class
# now would be machinery for a convention the kit has not adopted. This
# is an honest population narrowing (see the module docstring, "Region-
# aware filtering"), not a silent invention: the layer still degrades
# correctly on a tree with no staff-shaped carriers (class (v) itself
# needs nothing but a path and a line count).
#
# decide() is NOT touched by this layer at all. Region-aware via the
# SAME _safe_scan()/_is_quoted() pair as the layers above -- but with
# NO bare-regex I-0 fallback: with no region info at all, the whole
# layer stays silent (a cheap "any candidate at all" prefilter runs
# BEFORE the filesystem or the scanner are ever touched).
# =======================================================================

FRESHNESS_WARN_PREFIX = "FRESHNESS WARN:"

_FRESHNESS_PATH_BODY_CHAR = r'[^\s"\'<>|?*{}$,;\n]'

FRESHNESS_LINE_ANCHOR_RE = re.compile(
    r"(?<![\w/\\])(?P<path>"
    + r"[\w.\-]+/"
    + _FRESHNESS_PATH_BODY_CHAR
    + r"{0,300}\.[A-Za-z0-9]{1,10})"
    + r":(?P<n>\d{1,7})(?:-(?P<m>\d{1,7}))?\b"
)

FRESHNESS_LINE_ANCHOR_ABS_RE = re.compile(
    r"(?<!\w)(?P<path>[A-Za-z]:[\\/]"
    + _FRESHNESS_PATH_BODY_CHAR
    + r"{0,300}\.[A-Za-z0-9]{1,10})"
    + r":(?P<n>\d{1,7})(?:-(?P<m>\d{1,7}))?\b"
)

_FRESHNESS_SUMMARY_THRESHOLD = 20
_FRESHNESS_MAX_FILE_BYTES = 2 * 1024 * 1024
_FRESHNESS_MAX_FILES_PER_CALL = 8
_FRESHNESS_MAX_PROMPT_CHARS = 300_000


def _freshness_m3_message(token_display: str, line_count: int, bound: int) -> str:
    return (
        f"{FRESHNESS_WARN_PREFIX} anchor {token_display} points past the "
        f"end of the file (it has {line_count} lines) -- the line moved "
        f"or was removed, acceptance will open the wrong place and sign "
        f"off on the wrong content -- re-read the carrier, update the "
        f"line number, or drop it and keep the path."
    )


def _freshness_line_anchor_candidates_region_aware(prompt: str, scan_result) -> list:
    """(path, is_abs, n, m) for anchors with >=1 occurrence OUTSIDE a
    quote -- dedup by (normcase(path), n, m), same polarity/shape as
    extract_given_candidates_region_aware."""
    order = []
    seen = {}
    for pattern, is_abs in (
        (FRESHNESS_LINE_ANCHOR_ABS_RE, True),
        (FRESHNESS_LINE_ANCHOR_RE, False),
    ):
        for m in pattern.finditer(prompt):
            path = m.group("path")
            n = int(m.group("n"))
            m_raw = m.group("m")
            mm = int(m_raw) if m_raw is not None else None
            key = (os.path.normcase(path), n, mm)
            quoted = _is_quoted(_region_at(scan_result, m.start()))
            if key not in seen:
                seen[key] = {
                    "path": path, "is_abs": is_abs, "n": n, "m": mm,
                    "any_unquoted": not quoted,
                }
                order.append(key)
            elif not quoted:
                seen[key]["any_unquoted"] = True
    return [seen[k] for k in order if seen[k]["any_unquoted"]]


def _freshness_class_v_hits(prompt: str, scan_result, repo_root: str) -> list:
    """WARN only when the file exists, is readable, and its line count
    is below max(N, M). _FRESHNESS_MAX_FILE_BYTES / _FRESHNESS_MAX_FILES_
    PER_CALL bound per-call cost; files over the per-call budget are
    silently skipped (never mentioned as "unchecked"). line_count is
    computed EXACTLY once per file within a call -- repeat anchors on
    the same file (different N/M) reuse the cached line count."""
    candidates = _freshness_line_anchor_candidates_region_aware(prompt, scan_result)
    if not candidates:
        return []
    checked_files: set = set()
    line_count_cache: dict = {}
    hits = []
    for cand in candidates:
        path, is_abs, n, m = cand["path"], cand["is_abs"], cand["n"], cand["m"]
        if is_abs:
            if not _is_under_root(path, repo_root):
                continue
            full_path = path
        else:
            # a relative anchor is a path only by the ONE predicate (dispatch_manifest.path_candidates)
            if path not in _load_manifest_module().path_candidates(path, top_level_entries(repo_root)):
                continue
            full_path = os.path.join(repo_root, path)
        file_key = os.path.normcase(os.path.normpath(full_path))

        if file_key in line_count_cache:
            line_count = line_count_cache[file_key]
        else:
            if not os.path.isfile(full_path):
                continue  # silent: does not exist / is a directory
            if file_key not in checked_files:
                if len(checked_files) >= _FRESHNESS_MAX_FILES_PER_CALL:
                    continue  # per-call file budget
                checked_files.add(file_key)
            try:
                if os.path.getsize(full_path) > _FRESHNESS_MAX_FILE_BYTES:
                    continue  # per-file size budget
                with open(full_path, "r", encoding="utf-8", errors="replace") as fh:
                    text = fh.read()
            except OSError:
                continue
            line_count = len(text.splitlines())
            line_count_cache[file_key] = line_count

        bound = max(n, m) if m is not None else n
        if line_count < bound:
            token_display = f"{path}:{n}" + (f"-{m}" if m is not None else "")
            hits.append((token_display, line_count, bound))
    return hits


def _freshness_format_class_v(hits: list) -> str:
    if not hits:
        return ""
    if len(hits) <= _FRESHNESS_SUMMARY_THRESHOLD:
        return "\n\n".join(_freshness_m3_message(*h) for h in hits)
    head = ", ".join(h[0] for h in hits[:3])
    return (
        f"{FRESHNESS_WARN_PREFIX} {len(hits)} file:line anchors point past "
        f"the end of their carrier -- lines moved or were removed, "
        f"acceptance will open the wrong place; first 3: {head} -- "
        f"re-read the carriers, update the line numbers, or drop them "
        f"and keep the paths."
    )


def freshness_warn(payload: dict) -> str:
    """"" -- nothing to warn about; pure, never raises outward. Not
    Task/Agent -- silent without touching the filesystem. No anchor
    candidate at all -> "" BEFORE the filesystem/scanner. Region
    scanner unavailable -> the layer stays silent ENTIRELY (no bare-
    regex I-0 fallback here, unlike given_path_warn -- see the module
    docstring)."""
    if not isinstance(payload, dict):
        return ""
    tool_name = payload.get("tool_name")
    if tool_name not in ("Task", "Agent"):
        return ""
    tool_input = payload.get("tool_input") or {}
    if not isinstance(tool_input, dict):
        return ""
    prompt = tool_input.get("prompt")
    if not isinstance(prompt, str) or not prompt:
        return ""
    if len(prompt) > _FRESHNESS_MAX_PROMPT_CHARS:
        return ""  # stays silent without reading the disk

    has_v = bool(FRESHNESS_LINE_ANCHOR_ABS_RE.search(prompt)) or bool(
        FRESHNESS_LINE_ANCHOR_RE.search(prompt)
    )
    if not has_v:
        return ""

    scan_result = _safe_scan(prompt)
    if scan_result is None:
        return ""  # no region info -- the whole layer stays silent

    repo_root = payload.get("cwd")
    if not isinstance(repo_root, str) or not repo_root:
        return ""  # no root: silent (the same polarity as the path layers; no os.getcwd())

    return _freshness_format_class_v(
        _freshness_class_v_hits(prompt, scan_result, repo_root)
    )


# --- Token-budget layer (t-575, B-462..B-466) ---------------------------------------------
# Two checks beside the completeness gate, both for Task/Agent only:
#  * PARALLEL CAP (blocking, D-0040: WRITING workers only): a dispatch is a WRITING one when
#    is_writing_dispatch says so: subagent_type "builder", or owns_declaration_has_path_token(prompt) --
#    so a reader (scout, critic, designer, Explore, Plan) whose prompt carries an owns line with a path IS
#    a writing dispatch: counted and blockable (door: budget-skip); a dispatch that is not a writing one is
#    neither counted nor blocked (t-847: at >= PARALLEL_CAP live writers it carries one note, "this reader is
#    not counted"; the owns word counts only as a header line carrying an absolute path, dispatch_manifest.has_owned_paths, never as prose). For a writing dispatch: >= PARALLEL_CAP (6, the owner's word 20.10.2026, D-0054; was 4) UNFINISHED agent-*.jsonl
#    files modified within the last PARALLEL_WINDOW_SECONDS in the current session's subagents folder
#    (session_id from the hook input) that are WRITERS (transcripts.is_writer, the predicate injected):
#    the worker's sidecar agent-<id>.meta.json says agentType "builder" (written at launch, decides
#    first), or -- for every other kind, and for an absent or bad meta -- its FIRST user line (the
#    dispatch prompt) satisfies the SAME predicate owns_declaration_has_path_token. -> exit 2 naming
#    the count and the newest files. A transcript whose last assistant
#    line with tool_use calls SubagentHandback is finished and is not counted
#    (transcripts.live_worker_files / is_finished, the one reader of worker transcripts, B-467).
#    Invariant it protects: at most PARALLEL_CAP (six) WRITING workers, each re-reading a
#    large context, at once. Accepted edge: a worker silent for 10 minutes (one long foreground
#    command or a background wait) is not counted. Informed pass: a line `budget-skip: <reason>`
#    in the prompt (the shape of `manifest-skip:`), carried as a note.
#    Error direction, per file: a transcript that cannot be read is COUNTED live (it never lets a
#    (cap+1)-th worker through); a worker of unknown kind (no meta, a bad meta, a missing or non-str
#    agentType) with no readable first user line (empty, malformed, no user line) is COUNTED as a
#    writer; a known non-builder kind with no readable first user line is a reader. Both sides of
#    the line: COUNTED as a writer when unknown or when the meta says builder (the cap never lets a
#    (cap+1)-th through on a missing fact); BLOCKED when its own prompt reads as writing -- a reader's
#    prompt quoting an owns line with a path (door: budget-skip). A file whose stat says
#    FileNotFoundError vanished and is not counted;
#    any other stat error counts the file live. No session_id / an unsafe one / no folder / a glob
#    or home error -> count 0 (fail-open, as before).
#    tools/transcripts.py did not import -> every fresh agent-*.jsonl counts live (an unknown is
#    never a pass) and the message carries TRANSCRIPTS_MISSING; the door stays budget-skip.
#  * PUSH BEFORE LAUNCH (WARN): tool_input.isolation == "worktree" and `git rev-list --count
#    origin/main..main` > 0 (cwd = the hook's cwd): a worktree is cut from origin/main, so local
#    commits missing on origin are missing from the worker's tree. Origin ahead of main, a git
#    error or a missing ref -> silent.

PARALLEL_CAP = 6
PARALLEL_WINDOW_SECONDS = 600
PARALLEL_NAMES_SHOWN = 6
BUDGET_SKIP_RE = re.compile(r"^[ \t]*(?:[-*•][ \t]+)?budget-skip:[ \t]*(\S.*)$", re.IGNORECASE | re.MULTILINE)
TRANSCRIPTS_MISSING = ("tools/transcripts.py did not import -- every fresh worker file counted live; "
                       "door: budget-skip")

# The root of the session folders: the transcripts alias (a module-level name so tests can swap it, and
# recent_subagent_files ALWAYS passes it on as `root`). Without the module there is no alias to take.
if transcripts is not None:
    _projects_root = transcripts.projects_root
else:
    def _projects_root() -> Path:
        return Path.home() / ".claude" / "projects"


def _fresh_files_unfiltered(sid, now) -> list:
    """The count when tools/transcripts.py did not import: every agent-*.jsonl modified within the window,
    finished or not (nothing here can read a transcript), newest first. The error direction of the cap is
    kept: an unknown is never a pass. A stat that fails counts the file live, except a vanished one."""
    if not isinstance(sid, str) or not re.fullmatch(r"[A-Za-z0-9_-]+", sid):
        return []
    found = []
    for f in _projects_root().glob("*/%s/subagents/agent-*.jsonl" % sid):
        try:
            mtime = f.stat().st_mtime
        except FileNotFoundError:
            continue
        except OSError:
            mtime = now
        if now - mtime <= PARALLEL_WINDOW_SECONDS:
            found.append((mtime, f))
    return [f for _m, f in sorted(found, key=lambda t: t[0], reverse=True)]


def is_writing_dispatch(payload: dict) -> bool:
    """D-0040: True when the dispatch is a WRITING one -- subagent_type "builder", or a prompt whose owns
    declaration carries a path token (owns_declaration_has_path_token, the one write predicate, also what
    the cap applies to a live worker's first prompt). A missing tool_input or a non-str prompt: only the
    builder type decides."""
    tool_input = payload.get("tool_input")
    if not isinstance(tool_input, dict):
        return False
    return tool_input.get("subagent_type") == "builder" or owns_declaration_has_path_token(tool_input.get("prompt"))


def recent_subagent_files(payload: dict, now=None) -> list:
    """Paths of unfinished WRITING agent-*.jsonl modified within the window, newest first; [] when unknown.
    A worker is a writer by transcripts.is_writer: its meta says "builder", or its first prompt satisfies
    owns_declaration_has_path_token; an unknown kind and prompt counts as a writer."""
    sid = payload.get("session_id")
    now = time.time() if now is None else now
    if transcripts is None:
        return _fresh_files_unfiltered(sid, now)
    return transcripts.live_worker_files(
        sid, now, PARALLEL_WINDOW_SECONDS, root=_projects_root(),
        writer=lambda f: transcripts.is_writer(f, owns_declaration_has_path_token))


def parallel_cap_check(payload: dict) -> tuple:
    """(exit_code, stderr_message, note) for the parallel cap; (0, "", "") when not a dispatch or under the
    cap. A reading dispatch (D-0040) is neither counted nor blocked; at the full cap it carries ONE note
    "PARALLEL CAP: N writers live (...); this reader is not counted (D-0040)". With
    tools/transcripts.py missing the cap still counts (every fresh file) and every message, refusal or
    pass, carries TRANSCRIPTS_MISSING."""
    if payload.get("tool_name") not in ("Task", "Agent"):
        return 0, "", ""
    files = recent_subagent_files(payload)
    unchecked = (" " + TRANSCRIPTS_MISSING) if transcripts is None else ""
    names = ", ".join(f.name for f in files[:PARALLEL_NAMES_SHOWN])
    if not is_writing_dispatch(payload):
        # t-847: a reader is never blocked; at the full cap it gets ONE note that the writers are there and it
        # is not one of them (under the cap: silence, as before).
        if len(files) < PARALLEL_CAP:
            return 0, "", ""
        return 0, "", "PARALLEL CAP: %d writers live (%s); this reader is not counted (D-0040)%s" % (
            len(files), names, unchecked)
    if len(files) < PARALLEL_CAP:
        return 0, "", ("PARALLEL CAP:" + unchecked) if unchecked else ""
    prompt = (payload.get("tool_input") or {}).get("prompt")
    skip = BUDGET_SKIP_RE.search(prompt) if isinstance(prompt, str) else None
    if skip:
        return 0, "", "BUDGET-SKIP: %d writing workers active in the last 10 minutes (cap %d) -- sent anyway: %s%s" % (
            len(files), PARALLEL_CAP, skip.group(1).strip(), unchecked)
    return 2, (
        "PARALLEL CAP: %d writing-worker transcripts were written in the last 10 minutes (cap %d; newest: %s). "
        "Every running worker re-reads its whole context each turn -- wait for one to hand back, then send "
        "this dispatch. To send it anyway on purpose, add a line: budget-skip: <reason>%s"
        % (len(files), PARALLEL_CAP, names, unchecked)), ""


# --- the verdict carrier and the one-process readers (t-789, forge F5-8; fix round t-796) --------------
# The parallel cap refuses inside main(), and the runtime STARTS ALL hooks of the Task|Agent matcher TOGETHER
# (measured, t-792: the readers began 0-25 ms after the gate and finished before it in 68 of 115 runs), so a
# later hook cannot learn the gate's final verdict from a file. What survives is ONE process: main() judges
# the dispatch and, ONLY on "allow", runs the two trace writers itself -- critic_snapshot, then owns_gate --
# through their run_after_gate(payload) entry points. On "refuse" neither runs: no race, no key, no poll.
# logs/dispatch_verdict.json is the gate's WRITTEN verdict for later readers (session_context, calibration
# 17(g)); no hook reads it. Its key is the runtime's tool_use_id, else a content key with the prompt length.
# Invariant: the carrier and the readers can never change the gate's own decision -- every failure here is one
# stderr line and today's behaviour; the only exit code a reader can add is a refusal it owns (it returns 2).
# BOTH WORLDS: while settings.json still lists critic_snapshot.py / owns_gate.py as hooks of their own they
# run standalone as they always did; claim_trace() keeps the gate's run and the standalone run from both
# writing the trace of one tool_use_id (whoever asks first writes, the other stays silent).
VERDICT_REL_PATH = Path("logs") / "dispatch_verdict.json"
CLAIMS_REL_DIR = Path(".claude") / "dispatch_claims"  # under .claude/: outside the critic's tree hash
CLAIM_MAX_AGE_SECONDS = 3600
VERDICT_REASON_CHARS = 300
TRACE_READERS = ("critic_snapshot", "owns_gate")  # today's settings.json order
_CLAIM_ID_RE = re.compile(r"[A-Za-z0-9_-]{1,128}")


def _sibling_module(name: str):
    """A tools/ module by name, imported LAZILY with this file's directory on sys.path first (the way
    _load_manifest_module does it): only an ALLOWED dispatch pays for the readers."""
    tools_dir = str(Path(__file__).resolve().parent)
    if tools_dir not in sys.path:
        sys.path.insert(0, tools_dir)
    return importlib.import_module(name)


def verdict_key(payload: dict) -> tuple:
    """(key, kind) of this dispatch. The runtime's tool_use_id (kind "tool_use_id") when the payload carries
    a non-empty one; else sha256(prompt + NUL + description)[:16] + ":" + len(prompt) (kind "content": an
    identical resend shares it, which only costs a record nobody reads back, and the length keeps two prompts
    that differ in a tail apart). ("", "") when the payload is not a dispatch dict."""
    if not isinstance(payload, dict):
        return "", ""
    tool_use_id = payload.get("tool_use_id")
    if isinstance(tool_use_id, str) and tool_use_id:
        return tool_use_id, "tool_use_id"
    tool_input = payload.get("tool_input")
    if not isinstance(tool_input, dict):
        return "", ""
    prompt, description = tool_input.get("prompt"), tool_input.get("description")
    prompt = prompt if isinstance(prompt, str) else ""
    text = prompt + "\0" + (description if isinstance(description, str) else "")
    digest = hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()[:16]
    return "%s:%d" % (digest, len(prompt)), "content"


def _verdict_path(payload: dict):
    """<payload cwd>/logs/dispatch_verdict.json; None without a string cwd (the carrier has no home then:
    a payload with no cwd is never written)."""
    cwd = payload.get("cwd") if isinstance(payload, dict) else None
    return Path(cwd) / VERDICT_REL_PATH if isinstance(cwd, str) and cwd else None


def write_verdict(payload: dict, verdict: str, reason: str = "", now: datetime = None) -> None:
    """Record main()'s final verdict ("allow" | "refuse") for this dispatch with the repository's atomic
    writer (dod_track._atomic_write_text: mkstemp beside the file, os.replace, the temp removed on failure).
    An unwritable carrier costs one stderr line and nothing else -- the readers still run."""
    path = _verdict_path(payload)
    key, kind = verdict_key(payload)
    if path is None or not key or payload.get("tool_name") not in ("Task", "Agent"):
        return
    record = {"ts": (now or datetime.now()).isoformat(timespec="seconds"), "verdict": verdict,
              "reason": (reason or "")[:VERDICT_REASON_CHARS], "key": key, "key_kind": kind}
    try:
        _sibling_module("dod_track")._atomic_write_text(path, json.dumps(record, ensure_ascii=False) + "\n")
    except Exception as exc:
        sys.stderr.write("dispatch_gate: verdict carrier %s not written (%s)\n"
                         % (VERDICT_REL_PATH.as_posix(), type(exc).__name__))


def _prune_claims(folder: Path) -> None:
    """Best effort: claim markers older than an hour go (a dispatch lives seconds)."""
    cutoff = time.time() - CLAIM_MAX_AGE_SECONDS
    for marker in folder.iterdir():
        try:
            if marker.stat().st_mtime < cutoff:
                marker.unlink()
        except OSError:
            pass


def claim_trace(payload: dict, reader: str) -> bool:
    """True when `reader` ("critic_snapshot" | "owns_gate") may write its trace for this dispatch: it is the
    FIRST to ask for this tool_use_id (an exclusive create of .claude/dispatch_claims/<id>.<reader>, atomic
    between processes). False only when the marker already exists -- the other run (the gate's, or the
    reader's own hook) has the trace. No usable tool_use_id or cwd (nothing to key on) or any I/O error:
    True -- today's behaviour, a trace is never lost to the guard; a payload with no id may then be written
    twice while both worlds coexist (the hook entry and the gate's call), never zero times."""
    try:
        tool_use_id, cwd = payload.get("tool_use_id"), payload.get("cwd")
        if not (isinstance(tool_use_id, str) and _CLAIM_ID_RE.fullmatch(tool_use_id) and isinstance(cwd, str) and cwd):
            return True
        folder = Path(cwd) / CLAIMS_REL_DIR
        folder.mkdir(parents=True, exist_ok=True)  # FileExistsError here (a file in the way) is an I/O error, not a claim
        _prune_claims(folder)
        marker = str(folder / ("%s.%s" % (tool_use_id, reader)))
    except Exception:
        return True
    try:
        os.close(os.open(marker, os.O_CREAT | os.O_EXCL | os.O_WRONLY))
        return True
    except FileExistsError:
        return False  # only THIS exception means "the other run has the trace"
    except Exception:
        return True


def _context_parts(text: str) -> list:
    """The additionalContext strings of the one-JSON-object lines a reader printed (a line that is not
    that shape is kept as plain text: a reader's words are never dropped)."""
    parts = []
    for line in text.splitlines():
        if not line.strip():
            continue
        try:
            context = json.loads(line)["hookSpecificOutput"]["additionalContext"]
        except Exception:
            context = line
        if isinstance(context, str) and context:
            parts.append(context)
    return parts


def run_trace_readers(payload: dict) -> tuple:
    """Run critic_snapshot then owns_gate (their run_after_gate entry points) for an ALLOWED dispatch.
    Returns (exit_code, context_parts): the highest code a reader returned (a registry refusal is 2 and the
    gate then refuses too; they return 0 in WARN mode) and what they printed, folded into the gate's single
    additionalContext. A payload with no string cwd runs none (they would write into the process cwd).
    A reader that raises costs one stderr line; the other still runs."""
    cwd = payload.get("cwd")
    if not (isinstance(cwd, str) and cwd):
        return 0, []
    sys.modules.setdefault("dispatch_gate", sys.modules[__name__])  # a script run: owns_gate must not load a 2nd copy
    code, parts = 0, []
    for name in TRACE_READERS:
        buffer = io.StringIO()
        try:
            reader = _sibling_module(name)
            with contextlib.redirect_stdout(buffer):
                reader_code = reader.run_after_gate(payload)
        except Exception as exc:
            sys.stderr.write("dispatch_gate: %s did not run (%s) -- its trace for this dispatch is not written "
                             "by the gate\n" % (name, type(exc).__name__))
            continue
        parts.extend(_context_parts(buffer.getvalue()))
        if isinstance(reader_code, int) and reader_code:
            sys.stderr.write("dispatch_gate: %s returned exit %d\n" % (name, reader_code))
            code = max(code, reader_code)
    return code, parts


def _git_out(args: list, cwd):
    """Stripped stdout of `git <args>`; None on a git error, a non-zero exit or empty output."""
    try:
        done = subprocess.run(["git"] + args, cwd=cwd, capture_output=True, text=True, timeout=5)
    except Exception:
        return None
    out = done.stdout.strip()
    return out if done.returncode == 0 and out else None


def push_before_launch_warn(payload: dict) -> str:
    """WARN text when a worktree dispatch would be cut from an origin/main that lacks local commits; else "".

    Only local commits missing on origin count (rev-list origin/main..main > 0); origin ahead is silent."""
    if payload.get("tool_name") not in ("Task", "Agent"):
        return ""
    if (payload.get("tool_input") or {}).get("isolation") != "worktree":
        return ""
    cwd = payload.get("cwd") if isinstance(payload.get("cwd"), str) else None
    ahead = _git_out(["rev-list", "--count", "origin/main..main"], cwd)
    if not ahead or not ahead.isdigit() or int(ahead) < 1:
        return ""
    local, remote = _git_out(["rev-parse", "main"], cwd), _git_out(["rev-parse", "origin/main"], cwd)
    if not local or not remote:
        return ""
    return (
        "PUSH BEFORE LAUNCH: local main is %s, %s commit(s) ahead of origin/main %s; a worktree agent is cut "
        "from origin/main, so those commits are not in its tree. Two exits: push main first, or say "
        "`merge %s first` in the dispatch." % (local, ahead, remote, local))


def _reconfigure_stderr_utf8():
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def _reconfigure_stdout_utf8():
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


# --- stdin deadline (P4 class; a LOCAL copy, no shared module -- the
# same helper toolkit/tools/owns_gate.py/session_context.py already
# carry)
# --------------------------------------------------------------------

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
    thread.join(timeout). A TTY returns b"" without reading anything.
    Any read error degrades to b"" (fail-open)."""
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

# A background reader thread may still be blocked deep in a platform
# read syscall at normal interpreter shutdown, which can crash the
# process ("Fatal Python error: _enter_buffered_busy") instead of
# exiting cleanly. main() itself is UNCHANGED (still a plain
# `return 0`/`return 2`, safe in-process); only the actual __main__
# script-exit path below escalates to os._exit().
_STDIN_DEADLINE_STATE = {"hit": False}

# The UNCHECKED NOTE text (spec "Texts", verbatim) lives in
# dispatch_manifest.UNCHECKED_NOTE_TEMPLATE; this copy is used ONLY when that
# module cannot be imported (a failed import is itself a "check failed"
# case, and the note must still be producible). A test pins the two equal.
_UNCHECKED_NOTE_FALLBACK = (
    "MANIFEST-UNCHECKED: this dispatch was not checked for completeness ({what}) -- it went "
    "out; check given, owns, non-goals, handoff, edges and DoD by eye."
)


def _unchecked_note(what: str) -> str:
    try:
        template = _load_manifest_module().UNCHECKED_NOTE_TEMPLATE
    except Exception:
        template = _UNCHECKED_NOTE_FALLBACK
    return template.format(what=what)


def _unreadable_detail(payload):
    """None -- the payload can be handed to the gate. Otherwise the detail
    for "payload unreadable: <detail>": the payload is not a JSON object, or
    it is a Task/Agent call whose tool_input is not one (an absent tool_input
    is that too). A call that is not Task/Agent is never unreadable here."""
    if not isinstance(payload, dict):
        return "payload is not a JSON object (%s)" % type(payload).__name__
    if payload.get("tool_name") in ("Task", "Agent") and not isinstance(
        payload.get("tool_input"), dict
    ):
        return "tool_input is not a JSON object (%s)" % type(payload.get("tool_input")).__name__
    return None



def _write_hook_output(parts) -> None:
    """One additionalContext JSON on stdout for the non-empty parts."""
    parts = [p for p in parts if p]
    if not parts:
        return
    _reconfigure_stdout_utf8()
    output = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "additionalContext": "\n\n".join(parts),
        }
    }
    sys.stdout.write(json.dumps(output, ensure_ascii=False) + "\n")


def main() -> int:
    _reconfigure_stderr_utf8()

    # Byte-safe read via the stdin-deadline helper (replaces a former
    # direct, unbounded sys.stdin.buffer.read()) -- same decode utf-8/
    # errors="replace" fail-open contract, now bounded by
    # OSLLM_STDIN_TIMEOUT instead of blocking forever with no EOF.
    raw_bytes, timed_out = _read_stdin_bytes_deadline()
    if timed_out:
        # The payload never arrived: fail open, but say so (UNCHECKED NOTE on
        # additionalContext and stderr, next to the old deadline line).
        _STDIN_DEADLINE_STATE["hit"] = True
        sys.stderr.write(f"{Path(__file__).name}: {_STDIN_DEADLINE_MSG}\n")
        note = _unchecked_note("payload unreadable: stdin deadline exceeded")
        sys.stderr.write(note + "\n")
        _write_hook_output([note])
        return 0
    raw = raw_bytes.decode("utf-8", errors="replace")
    if not raw.strip():
        # Empty stdin / a TTY (the reader returns b"" for both): silent exit 0,
        # as before -- test_p4_stdin_deadline.py pins the empty stdout.
        return 0
    try:
        payload = json.loads(raw)
    except Exception as exc:
        # Unparseable input -- fail open (same principle as every other hook
        # in this file set), with the UNCHECKED NOTE so it is visible.
        note = _unchecked_note("payload unreadable: malformed JSON (%s)" % type(exc).__name__)
        sys.stderr.write(note + "\n")
        _write_hook_output([note])
        return 0

    # A payload that is not a JSON object, or an Agent call whose tool_input
    # is not one, cannot be checked: exit 0 with the UNCHECKED NOTE in
    # additionalContext and the same text on stderr (never lock the session).
    detail = _unreadable_detail(payload)
    if detail is not None:
        note = _unchecked_note("payload unreadable: %s" % detail)
        sys.stderr.write(note + "\n")
        _write_hook_output([note])
        return 0

    # ONE call: decide_full holds the completeness check, the path check and the
    # label check and returns the notes too (no second pass over the prompt).
    # Only an EXCEPTION out of it is caught here (fail-open, with the UNCHECKED
    # NOTE); a real refusal (exit 2) is returned as it is.
    decide_note = ""
    try:
        decision = decide_full(payload)
    except Exception as exc:
        decision = Decision(0, "", [], [])
        decide_note = _unchecked_note("check failed: %s" % type(exc).__name__)
        sys.stderr.write(decide_note + "\n")
    if decision.code == 2:
        write_verdict(payload, "refuse", decision.message)
        sys.stderr.write(decision.message + "\n")
        return 2

    # The parallel cap (t-575): a refusal only after the completeness gate passed; fail-open on any error.
    try:
        cap_code, cap_message, cap_note = parallel_cap_check(payload)
    except Exception:
        cap_code, cap_message, cap_note = 0, "", ""
    if cap_code == 2:
        write_verdict(payload, "refuse", cap_message)
        sys.stderr.write(cap_message + "\n")
        return 2
    write_verdict(payload, "allow")  # t-789: the final verdict; the WARN layers below cannot change it
    # t-796: ONE process -- the trace writers run here, after the verdict and only on "allow" (none on a refusal)
    reader_code, reader_parts = run_trace_readers(payload)
    if reader_code == 2:
        write_verdict(payload, "refuse", "a trace writer refused the dispatch")
        return 2

    if decision.stderr_note:
        sys.stderr.write(decision.stderr_note + "\n")
    manifest_note = "\n".join(n for n in [decide_note] + list(decision.notes) if n)
    try:
        path_report = format_path_report(decision.paths)
    except Exception:
        path_report = ""

    # Every WARN layer below is considered only when the gate itself did
    # NOT block (see the module docstrings, "Given-path WARN layer" /
    # "Role-type WARN layer" / "Region-aware filtering" / "FRESHNESS
    # layer"); try/except on EACH is belt-and-suspenders -- no layer
    # must ever crash the blocking hook with a traceback. Fixed order:
    # given-path, role-type (unchanged), then the new region-aware
    # layers in the tail, write-quoted last among those (the newest),
    # freshness at the very end.
    try:
        warn_given = given_path_warn(payload, decision)
    except Exception:
        warn_given = ""
    try:
        warn_role = role_type_warn(payload)
    except Exception:
        warn_role = ""
    try:
        warn_dod_quoted = dod_quoted_warn(payload)
    except Exception:
        warn_dod_quoted = ""
    try:
        warn_manifest_quoted = manifest_quoted_warn(payload)
    except Exception:
        warn_manifest_quoted = ""
    try:
        warn_write_quoted = write_quoted_warn(payload)
    except Exception:
        warn_write_quoted = ""
    try:
        warn_freshness = freshness_warn(payload)
    except Exception:
        warn_freshness = ""

    try:
        warn_push = push_before_launch_warn(payload)
    except Exception:
        warn_push = ""

    warn_parts = [
        w
        for w in (
            manifest_note,
            path_report,
            cap_note,
            warn_push,
            warn_given,
            warn_role,
            warn_dod_quoted,
            warn_manifest_quoted,
            warn_write_quoted,
            warn_freshness,
            *reader_parts,
        )
        if w
    ]
    _write_hook_output(warn_parts)

    return reader_code


if __name__ == "__main__":
    _rc = main()
    if _STDIN_DEADLINE_STATE["hit"]:
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
