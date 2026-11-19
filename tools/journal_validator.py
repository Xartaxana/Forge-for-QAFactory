"""Routing-journal validator -- a pre-commit gate for
logs/routing-log.jsonl that catches, in code, two failure patterns
that have happened for real: a duplicate task_id issued without
re-reading the log's tail, and an event whose ts was written from
narrative rather than read off the clock (a "narrative-future
timestamp"). Calling convention/structure mirror
tools/mechanism_gate.py (the same home in the enforcement chain): a
pure decide(), testable without git, and a thin main() wrapping it in
git plumbing.

Scope: ONLY the staged version of logs/routing-log.jsonl against the
HEAD version (git show :logs/... vs HEAD:logs/...). If the file isn't
staged, main() silently returns 0 (the gate emits nothing at all).
Only deterministically decidable facts are checked -- presence,
shape, typed fields; the meaning of notes is never parsed.

Checks (numbering matches this file's own spec / COORDINATOR.md's "Routing
log" section):
 1. Append-only: staged must start with HEAD as a prefix.
 2. Every NEW line is a valid single-line JSON object with
    ts/event/agent/category/notes (notes non-empty).
 3. event is one of the ENUM values.
 4. model is required for delegated/escalated/accepted/rejected.
 5. task_id is required for delegated/accepted/rejected/escalated/
    defect_found, format t-NNN (3+ digits).
 6. rejected: attempt is an integer >=1; failure_class is one of the
    ENUM values.
 7. accepted with agent=builder: witness is a non-empty string.
 8. defect_found: ref is non-empty.
 9. task_id novelty/reference rules (revised after a live precedent
    showed "strictly max+1" would forbid a legal critic entry into
    acceptance, and a legal retry after rejected). For a NEW
    delegated:
    a) RULE 9a'' (offload B0, owner 14.11.2026 "Number 123 and 123A"; it
       replaces "exactly max+1"): a brand-new id is legal when (i) the full
       id, clone letter included, was NEVER SEEN in the logical journal
       (seed + file), (ii) it is canonical (journal_keys.is_canonical:
       001..999 zero-padded, or 4-9 digits with no leading zero) and (iii)
       its number is at most ID_JUMP_MAX = 1000 above the max number seen
       WITH THE SAME LETTER (none yet: at most 1000, so the first id of a
       new letter is t-001a). Gaps and out-of-order numbers are legal (ids
       reserved by `journal_write.py next --n 3` land in any order). A seen
       id is judged by (b)-(d), keyed by the FULL id: t-123 and t-123a are
       two tasks. "Issued by this clone's counter" is the WRITER's check
       (the validator cannot see the counter);
    b) task_id already exists in the file AND the task is still OPEN
       (no accepted for this task_id earlier in the file) AND the new
       line's agent differs from every earlier delegated agent for
       that task_id -- legal (a continuation dispatch from a
       different tier, e.g. a critic entry into acceptance);
    c) task_id exists, task is open, agent matches one of the earlier
       delegated agents -- legal ONLY with an attempt field (integer
       >=2) AND ONE of (i)/(ii) below (the self/foreign-retry gap: the
       naive form "an attempt field plus ANY rejected on the task_id"
       would legalize a repeat delegated of ANY agent off ANY rejected
       on the task -- a reviewer (e.g. critic) could re-enter a SECOND
       time on an EXECUTOR's rejected with nothing reworked):
       (i) SELF -- an earlier rejected exists for the SAME agent
          (rejected.agent -- the executor whose result was rejected) on
          this task_id -- legalizes the agent's own retry with NO
          extra conditions (the "as before" form, narrowed to exactly
          "its own" rejected -- a self-retry needs no signal between
          the rejected and the repeat delegated);
       (ii) FOREIGN -- a rejected exists on the task_id, but NONE of
          them names an agent matching the incoming one (a "foreign"
          rejected) -- legalizes the entry ONLY if, STRICTLY AFTER that
          agent's own LAST delegated on this task_id (not anywhere
          earlier in the history -- a signal from an earlier round has
          gone stale and does not legalize the next round), at least
          one new-version signal appeared:
            (1) a new delegated by a DIFFERENT agent on this task_id;
            (2) a new rejected with agent=lead on this task_id (a Lead
               fix with no own delegated -- the fix itself is the
               signal);
            (3) a new escalated by a DIFFERENT agent on this task_id
               (an escalated by the SAME agent that is re-entering is a
               self-legalizing loop and does NOT count, symmetric with
               signal (1)).
          Neither (i) nor a valid (ii) signal -> FAIL (see (d));
    c2) (dead-worker replacement) the SAME situation as (c) (agent
       matches, task open) but rejected is NOT required and attempt
       does not need to grow -- this is not a rule-6 retry -- is legal
       if notes contain the literal substring "replaces_worker:" with
       a non-empty handle immediately after it (the first non-
       whitespace token), AND that handle LITERALLY matches the
       worker_ref of some earlier delegated line for this SAME
       task_id (any agent). Guard against a fabricated replacement: a
       handle that appears in no earlier delegated line for this
       task_id -> FAIL (see extract_replaces_worker).
    d) anything else -- FAIL (the duplicate-dispatch pattern: same
       agent, no attempt, no rejected, no valid replaces_worker; and
       delegated on a CLOSED task -- reopening is forbidden, a
       collision counts as two tasks).
    e) RETIRED for NEW lines (offload B0): a new line carrying `id_band` is
       a `band_retired` violation naming `python -B tools/journal_write.py
       next`; old lines' bands still feed BandState.top (read-only). The
       text below is the history of the retired rule.
       ID BANDS (F6-58) -- the door of (a) for a second writer of one file
       (a second session of the same developer) and for a branch whose ids
       will meet another's at a merge. The optional `id_band` field of ANY
       line: closed "t-A..t-B" reserves the ids A..B (at most
       BAND_MAX_SIZE = 1000) for the writer who declares it, issued in
       order A, A+1, ...; open "t-A.." raises the file's own sequence, so
       its next brand-new id is t-A. Both ends are ASCII digits, 3 to 9 of
       them (journal_keys.id_band_of is the one reader). A malformed band
       on a NEW line is a FORM / REVERSED / TOO_BIG violation (field
       `id_band`, clearable in a merge with `merge-accepts:<n>:id_band`); a
       null band is absent; an old line is never judged. `top` = the max of
       every id seen, every closed band's end and every open band's A-1; a
       band needs A > top (BELOW), at most BAND_JUMP_MAX = 10000 above it
       (JUMP), and a CLOSED band at least BAND_GAP_MIN = 50 above it (NEAR:
       a band protects by DISTANCE -- adjacent to `top` its first id is
       where the other writer's next max+1 falls). The band on a line
       applies BEFORE that line's own id is judged (the opening delegated
       of a band is legal); a band refused on a line never makes the same
       line's id legal. A used-up band is a NOVELTY violation that says so;
       a filler line that only raises the max is not needed. A band's next
       id is issuable ONLY by a line that carries that band in its own
       `id_band` (every line issued from a band declares it; repeating a
       declared band is a reference, never BELOW): a line without it that
       lands on the id is judged as a main-sequence id (NOVELTY plus the
       door clause). BandState.may_issue is the one predicate. A band only
       raises or reserves ids above everything issued or reserved: it never
       lowers the counter and never makes an issued id issuable twice. In a
       merge each parent's form-valid bands are in the state of the tail;
       the collision WARN names a band that overlaps ids the other clone
       had issued. The state is journal_keys.BandState: the gate,
       `journal_keys.py where` and compact_snapshot read the next id from
       it.
    f) `returned` (the end of a dispatch): needs task_id, worker_ref, model;
       the task must have an open `delegated` with the SAME worker_ref
       earlier in the logical journal (not closed by an accepted), at most
       one `returned` per (task, worker_ref); it is not novelty-issuing and
       never opens, reopens or closes a task. Optional fields on any event
       (rule 20): `via` (hook|cli), `session` (1-16 of [A-Za-z0-9-]),
       `witness_by` (run|file|text).
    For a new accepted/rejected/escalated/defect_found -- it must
    reference a task_id already seen earlier in the file (in HEAD or
    earlier in this same commit); unchanged otherwise -- except an `escalated` with agent=architect, which may OPEN a
    task under the novelty rule of a new delegated (9a'', F6). A `calibrated` line may carry `reviewed_through`, a git
    sha ^[0-9a-f]{7,40}$ (F9); any other event carrying it, or a bad shape, is a violation.
10. ts of new lines is monotonic relative to HEAD's last line and to
    each other; not later than now+10 minutes (a narrative-future
    timestamp). No lower bound.
11. The role-vs-tier acceptance matrix by FUNCTION RANK (NEW lines only, accepted only -- rejected carries "by" with no
    further check). rank(by) = tools/tier_ladder.py rank_of_model(by, config) over delegation.config.yaml read from the
    root of the repo being validated (absent there -> DEFAULT_BINDINGS; an unreadable one -> one stderr WARN and the
    defaults, never a FAIL); rank(agent) = rank_of_function(agent). agent in {lead, architect} or outside
    FUNCTION_RANKS: the matrix does not apply (presence of "by" is enough). For agent in {scout, builder, critic,
    designer}, in this order:
    (a) `by` outside FAMILIES (exact lowercase key; "lead", "claude-opus-5-5" and "Opus" included) FAILS first, with
        the family list as its door -- no rank arithmetic ever runs on an acceptor that cannot be identified;
    (b) basis=="judge" is REFUSED on every line (no judge is bound in this deployment, COORDINATOR.md rule 13), before
        ok_rank, so no acceptor rank makes it legal;
    (c) ok_rank: rank(by) > rank(agent) -- legal at any basis (a model ranked above a function's binding may stand in
        during an outage: a higher-ranked acceptor is never refused);
    (d) FLOOR: rank(by) < builder rank -- FAIL, before every remaining basis (no basis rescues it);
    (e) basis=="critic": legal iff critic rank > rank(agent);
    (f) basis=="queued-to-lead": legal iff agent in {critic, designer} and builder rank <= rank(by) < lead rank;
    (g) anything else -- FAIL with the generic role-vs-tier message.
    WARNs on a line the matrix passed (matrix_warnings; never a FAIL): `queued to itself` (basis queued-to-lead at
    rank(by) >= lead rank) and `INDEPENDENT CONTEXT` (critic/designer accepted at rank(by) >= lead rank with no
    earlier delegated of that agent on that task whose worker_ref starts `agent:`).
12. Every NEW delegated line carries worker_ref -- a non-empty handle
    by which the next session finds the worker/result; catches a
    phantom delegated whose worker was never launched.

13. Any FAIL -> exit 1, with the line number, event/task_id, and which
    check failed, for every violating line. A validator crash (an
    exception, not a validation FAIL) -> exit 2 with a traceback
    (fail-closed, same as mechanism_gate; see main()).
14. WARN only (never a FAIL, never changes the exit code): a NEW delegated/
    accepted/defect_found dated 2026-10-02 or later with no `feature` field, or
    a `feature` value that is not an id in plans/features.json (see
    feature_warnings / decide_with_warnings). Printed by main() on stderr.
    NOTE: tools/journal_echo.py (the write-moment hook) calls decide() only, so
    this WARN reaches the writer at the commit gate, not at the write moment.
15. MERGE COMMITS (t-430, B-401). A merge commit is validated by decide_merge, not decide: every
    line of both parents is kept (each in its own order, the only change allowed an added
    `feature`), and the lines ONLY the other clone brought get the per-line FORM checks of
    rules 2-8, 11, 12, 18 and the ts shape (the fields in FORM_FIELDS) -- not rule 9, ts order or
    drift, which two clones legitimately collide on. Two paths reach it: a conflicted merge
    concluded with `git commit` (pre-commit: MERGE_HEAD resolves), and a clean merge (the
    pre-merge-commit hook runs `journal_validator.py --merge-parent env`; git names the merged
    parent in GITHEAD_<sha>; none -> exit 0 plus a WARN, several -> exit 1). A defective
    foreign line cannot be edited (append-only, already committed in the other branch): the
    door is a NEW tail line whose notes carry `merge-accepts:<n>:<field>[,<field>]` plus the
    corrected value and the reason; it drops exactly the violations of MERGE_HEAD line n on
    the named fields (PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md 13(l) audits the tokens).
16. DECLARATION (B-402). logs/journal-segments.json tells the READERS (session_context,
    forge_metrics, calibration_counts -- tools/journal_keys.py) which journal lines belong to
    another clone's instance of a colliding task id. THIS gate stays on BARE ids -- rule 9 is
    unchanged and over-refuses, which is the allowed direction; the door for a refused reopen is
    a fresh id. The gate does two things with the file: a STAGED declaration that is unreadable
    or fails `journal_keys.check` against the staged journal is a FAIL (the gate also runs when
    only the declaration is staged); and in merge mode, task ids both clones issued that no
    declaration covers give one WARN (never a violation) with the `declare` door.
    Named limit: tools/journal_echo.py (the write-moment hook) calls decide() only and never
    reads the declaration, so a broken declaration is reported at SessionStart (the readers)
    and at the commit that stages it -- not at the moment a journal line is written.
17. ONE FILE PER WRITER (t-581, F0-4). A clone writes logs/journal/<slug>.jsonl (the slug of
    tools/dev.config.yaml, read by journal_keys.developer_slug); logs/routing-log.jsonl is the
    history. Pre-commit validates EVERY staged journal file separately, the header of the output
    names the path. The rules:
    a) FROZEN HISTORY: once the tree of HEAD holds a legal developer file, a new line of the
       history is a FAIL that names the file to write to (in a merge the other clone's lines are
       form-checked as before, only our own tail is refused);
    b) LINE 1 of a developer file is a journal_created; `continues` is allowed on line 1 only and
       only with the value logs/routing-log.jsonl (the file that continues the history is
       validated with the history as its seed, so its ids go on from the history's max); a second
       file with `continues` is a FAIL; an empty file passes;
    c) ONE WRITER: new lines (not in a merge) in the file of another slug, or with the slug
       unknown, are a FAIL with the door "write into your own file"; a merge that brings lines of
       one developer file from both sides is a WARN (written by two clones);
    d) a file that is deleted or renamed is a FAIL; a bad file name, a reserved or duplicate slug
       (journal_keys.journal_names) is a FAIL when the path is staged, else a WARN; a
       `closes:t-NNN@label` / `ref` naming a label that no file and no segment holds is a WARN
       (the token closes nothing).
    e) `--all --base <ref>` (CI; the old CI line passed a path that was ignored and checked
       nothing): every journal file of HEAD against the tree of the base -- the base text must be
       an unchanged prefix, then decide() over the added lines with the ts drift check OFF (the
       runner's clock is not the writer's), the history frozen by the BASE tree, the names and the
       single successor checked on HEAD; the one-writer rule is not checked (CI does not know the
       writer); a base that is ahead of HEAD, one that does not resolve, no --base, --all with
       --merge-parent, and any unknown argument exit 1.
18. THE NODE OF A LINE (t-797 F5-2, M5). The optional `node` field of a line (a `delegated` writes it; accepted/rejected may
    carry it) names the pile node the work belongs to, ONE form: `<slug>/<N>/<id>` (`forge/5/F5-2`;
    journal_keys.NODE_RE). A NEW line (the same scope as rules 2-8, merge mode included, field name `node` for
    merge-accepts) whose `node` is present and is not a string or not in that form is a FAIL with the text «`node` = <repr>
    is not `<slug>/<N>/<id>`; write e.g. `forge/5/F5-2`»; an ABSENT field (or JSON null, which journal_keys.node_of reads as
    absent) is never a violation, and an old line is never judged (append-only). The reader is journal_keys.node_of. WARN
    only (node_warnings; never a FAIL): a NEW `delegated` dated NODE_WARN_FROM (2026-10-15) or later with no `node` field whose
    `notes` carry a node token (one, or two different: `two_tokens`), or with a good field and a token that names another
    node (the field wins). A line with neither is silent. The same limit as rule 14: the write-moment hook sees decide() only.
19. ORDER-KNOWN DOOR (FG7-32). Three order defects of a NEW line -- a task id issued out of order (rule 9a), a ts not monotone
    against its predecessor (rule 10), a repeated delegated on an open task with no legal reason (rule 9c/d) -- are
    declarable: a LATER line of the SAME file whose `notes` carry `order-known:<ts>` (the exact ts of the defective
    line; the first non-whitespace run after the colon, several tokens allowed) drops the refusal. A line never
    declares itself, a token on an earlier line does not count, two lines with one ts are both covered, lines of
    another file never declare. An undeclared defect is refused with the exact token to append (one refusal per line);
    a token naming no earlier line is refused; one naming a line with no order defect, an empty one, or a value that is not a ts (prose such as `<ts>`; the token is
    ignored, the defect stays refused), is a WARN. Lines
    already in HEAD are never judged (unchanged). The count is the WARN-channel line `order-known: N declared`
    (decide_with_warnings; calibration check 13(m)). tools/journal_echo.py calls decide(), so it shares the door.
21. RETURN ORDER (FG7-22; WARN only, in matrix_warnings; decide() and journal_echo never see it). A NEW accepted or rejected
    line on a task that still has a hook-era worker (a `delegated` dated RETURNED_WARN_FROM or later, worker_ref `agent:<id>`)
    with no `returned` line of that (task_id, worker_ref) earlier in the logical file draws one WARN listing every owed ref.
    Owed = the latest worker of EVERY agent kind on the task; a later delegated of the same (task, agent) or
    `replaces_worker:<h>` supersedes. Producers of `returned` (AR-22): journal_hooks._write_returned (SubagentStop, exit 0)
    and `journal_write.py returned`. A RESUMED worker is owed again from its `resumed` line (FG7-88; producer
    journal_hooks.post_send, PostToolUse SendMessage; hand door `python -B tools/journal_write.py event --json`); a resume
    the hook could not tie (race, a copy beyond the scan) stays silent. A lost end WARNs the same as a running worker.
9f. `returned`: one per ROUND (FG7-88): a round starts at a never-seen `delegated` of (task, worker_ref) or at a `resumed`.
9h. `resumed` (FG7-88): refused on a task closed by an accepted, with a worker_ref no earlier delegated of the task carries,
    or while that pair's round is open (the worker has not returned since its last start). Door: journal_write.py event --json.
"""
from __future__ import annotations

import datetime
import json
import os
import re
import subprocess
import sys
import traceback
from pathlib import Path

try:
    import journal_keys as _jk
except ImportError:  # loaded by path (tests, a hook run from another cwd): tools/ is not on sys.path yet
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import journal_keys as _jk
try:
    import tier_ladder as _tl     # the ladder home (a leaf): the ranks of the acceptance matrix
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import tier_ladder as _tl

JOURNAL_PATH = "logs/routing-log.jsonl"
DECLARATION_PATH = _jk.SEGMENTS_REL            # logs/journal-segments.json (B-402)

# --- the optional `feature` field (WARN-only; Forge metrics, tools/forge_metrics.py) -------
# A NEW delegated/accepted/defect_found without a `feature` field, or with a value that is
# not an id in plans/features.json, is a WARN -- printed by _main(), never a FAIL: the
# journal must not block anyone over a tag. Events dated before FEATURE_WARN_FROM are never
# warned about (append-only, nothing is rewritten). tools/forge_metrics.py imports these
# two constants, so the generator's --check and this WARN ask for the same thing.
FEATURE_WARN_EVENTS = {"delegated", "accepted", "defect_found"}
FEATURE_WARN_FROM = "2026-10-02"
FEATURE_REGISTRY_REL = "plans/features.json"

# --- the optional `node` field (WARN part; t-797 F5-2 M5, F-9 (c)) ----------------------------
# The violation (a `node` that is not `<slug>/<N>/<id>`) is rule 18 of _line_form_violations. The WARN is
# node_warnings: a NEW `delegated` dated NODE_WARN_FROM (the merge day of N3) or later that names its
# node only in `notes` (a token, no field) or whose field and token disagree. Older lines are never warned.
NODE_WARN_FROM = "2026-10-15"
NODE_WARN_EVENTS = {"delegated"}

EVENTS = {
    "delegated", "accepted", "rejected", "escalated", "decomposable",
    "dispatch_skipped", "defect_found", "lead_degraded", "lead_restored",
    "journal_created", "calibrated", "returned", "resumed",
}
MODEL_REQUIRED_EVENTS = {"delegated", "escalated", "accepted", "rejected", "returned"}
TASK_ID_REQUIRED_EVENTS = {"delegated", "accepted", "rejected", "escalated", "defect_found", "returned", "resumed"}
# the optional fields of the offload spec (B0 item 4), judged by VALUE when present: `via` (who wrote the line),
# `session` (a short session id), `witness_by` (how an `accepted` witness was produced)
VIA_VALUES = ("hook", "cli")
WITNESS_BY_VALUES = ("run", "file", "text")
SESSION_RE = re.compile(r"^[A-Za-z0-9-]{1,16}\Z")
RETURNED_DOOR = "python -B tools/journal_write.py returned --task <id> --worker <worker_ref>"
RESUMED_DOOR = "python -B tools/journal_write.py event --json '<the resumed line>'"
FAILURE_CLASSES = {"spec", "capability", "recon", "tooling"}
# The ladder (family order, function ranks, bindings) lives in tools/tier_ladder.py -- no table of its own here.
# The acceptor's rank = rank_of_model(by); the executor's rank = rank_of_function(agent).
# The critic/designer CLASS: basis="queued-to-lead" is keyed on the agent CLASS {critic, designer}, not on a name
# (a data row of the matrix, not a ladder fact); its condition reads ranks (builder rank <= rank(by) < lead rank).
# basis="critic" works by the critic FUNCTION rank against the executor's rank, for any agent.
QUEUED_TO_LEAD_AGENTS = {"critic", "designer"}
# Known non-judge basis string values -- a PLAIN enum/reference (external
# consumers: PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md, log_append.py), no
# longer used as a legality check "basis in BASIS_VALUES" -- legality is
# decided per (by, agent) pair in _matrix_d0058_violation, not bare
# membership (closes a leak where basis=queued-to-lead passed membership
# for ANY by/agent, including builder-class at a sonnet coordinator).
BASIS_VALUES = {"critic", "queued-to-lead"}
# basis="judge" is REFUSED on every line (no judge is bound in this deployment, COORDINATOR.md rule 13; FG7-16).
JUDGE_BASIS_VALUE = "judge"
CONFIG_REL = "delegation.config.yaml"   # read from the root of the repo being validated (S2 of the architect-tier spec)
# reviewed_through of a `calibrated` line: a git sha (the Architect's review marker, ARCHITECT_START step 8)
REVIEWED_THROUGH_RE = re.compile(r"^[0-9a-f]{7,40}\Z")

TASK_ID_RE = _jk.ID_RE      # the ONE read grammar of a task id (journal_keys.ID_RE): t-NNN[a-z]{0,2}, ASCII only


def critic_basis(basis) -> "tuple[bool, str | None]":
    """The ONE grammar of the critic basis (FG7-88 Q2), read by the matrix, the echo R3 and r3_integration_check:
    (True, None) for exactly "critic"; (True, tid) for "critic:" + a task id; (False, None) for anything else (a
    non-str included) -- it may err only toward FAIL. Form only: whether tid names a critic delegated is the echo's."""
    word = "critic"
    if basis == word:
        return (True, None)
    if isinstance(basis, str) and basis.startswith(word + ":"):
        tid = basis[len(word) + 1:]
        if TASK_ID_RE.fullmatch(tid):
            return (True, tid)
    return (False, None)
# Dead-worker replacement marker (rule 9c2): the literal substring
# "replaces_worker:" plus a non-empty handle = the first non-whitespace
# token right after the colon (matches the shape of existing worker_ref
# values -- 'cli:...', 'agent:...' -- no internal whitespace).
REPLACES_WORKER_RE = re.compile(r"replaces_worker:(\S+)")
# ISO without a timezone: 'YYYY-MM-DDTHH:MM:SS' with optional
# microseconds, NO 'Z'/offset -- a timezone is forbidden by the spec
# (otherwise monotonicity between lines of different offsets loses
# its unambiguous ordering).
TS_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?$")
# Rule 19 (FG7-32): the door for ORDER defects of lines already written. `order-known:<ts>` in the `notes` of a
# line that stands LATER in the same file declares the line(s) whose `ts` is exactly <ts>; the first non-whitespace
# run after the colon is read, and it is a ts only when it matches TS_RE (shape-gated like `closes:`); an empty or
# non-ts value (prose such as `<ts>`) is a WARN and ignored: an ignored token never declares anything.
ORDER_KNOWN_RE = re.compile(r"(?<!\w)order-known:(\S*)")


def parse_ts(ts: str):
    if not isinstance(ts, str) or not TS_RE.match(ts):
        return None
    try:
        return datetime.datetime.fromisoformat(ts)
    except ValueError:
        return None


# one implementation of "the lines of a journal text" for the gate and the readers (t-525 F6)
split_lines = _jk.split_lines


def _try_parse_obj(line: str):
    try:
        obj = json.loads(line)
    except (json.JSONDecodeError, TypeError):
        return None
    return obj if isinstance(obj, dict) else None


def extract_task_ids(lines: list[str]) -> set[str]:
    """All task_id values (valid t-NNN format) seen in ANY event of
    these lines -- used both as the "already seen earlier" set and as
    the basis for max(...)+1."""
    ids = set()
    for line in lines:
        obj = _try_parse_obj(line)
        if obj is None:
            continue
        tid = obj.get("task_id")
        if isinstance(tid, str) and TASK_ID_RE.match(tid):
            ids.add(tid)
    return ids


def extract_replaces_worker(notes) -> str | None:
    """Rule 9(c2): pulls the handle out of a "replaces_worker:<handle>"
    marker in notes -- the literal substring plus the first non-
    whitespace token right after the colon. None if there's no marker
    (notes isn't a string, or the substring is absent)."""
    if not isinstance(notes, str):
        return None
    m = REPLACES_WORKER_RE.search(notes)
    return m.group(1) if m else None


def order_known_tokens(notes) -> list[str]:
    """Rule 19: every `order-known:<ts>` value in notes, in order ('' for a token with nothing after the colon).
    notes absent or not a string -> [] (the base-field check owns that refusal)."""
    if not isinstance(notes, str):
        return []
    return ORDER_KNOWN_RE.findall(notes)


def _order_known_door(original: str, ts, task_id, defect: str) -> str:
    return (f"{original} -- ORDER DEFECT ({defect}) on the journal line with ts {ts!r}, task_id {task_id!r}: if the "
            "line is already written and cannot be edited, declare it -- expected: a LATER line of this same file "
            f"whose notes carry the token `order-known:{ts}`; append a new line with that token in its notes, then "
            "commit again (rule 19)")


def _resolve_order_known(violations: list[str], marks: list, file_ts: list, tokens: list, n_head: int,
                         report: dict | None) -> list[str]:
    """Rule 19. `marks` = [(index in violations, file index of the line, ts, task_id, defect)] of the three
    declarable order defects of NEW lines; `file_ts` = the ts of every line of THIS file (HEAD then new; None for a
    line that does not parse); `tokens` = [(file index of the carrier, ts value)] of every token in the file.
    A defect is declared by a token whose ts equals the line's ts and whose carrier stands strictly LATER; the same
    line never declares itself. Returns the violations with declared ones dropped and the door text added to the
    undeclared ones; a token on a NEW line whose ts names no earlier line is a refusal, one that names only lines
    with no order defect is a WARN, an empty or non-ts one is a WARN and ignored (into report['warnings']).
    report['declared'] = the number of distinct defective LINES declared."""
    drop: set = set()
    declared_lines: set = set()
    replace: dict = {}
    good = [(q, tv) for q, tv in tokens if TS_RE.match(tv)]     # a non-ts value never declares anything
    for vi, fi, ts, tid, defect in marks:
        if any(q > fi and tv == ts for q, tv in good):
            drop.add(vi)
            declared_lines.add(fi)
        else:
            replace[vi] = _order_known_door(violations[vi], ts, tid, defect)
    extra: list[str] = []
    defective_idx = {fi for _vi, fi, *_rest in marks}
    for q, tv in tokens:
        if q < n_head:
            continue                                    # a token of an old line is never judged
        carrier = f"line {q + 1}"
        if tv == "":
            if report is not None:
                report.setdefault("warnings", []).append(
                    f"{carrier}: WARN `order-known:` has nothing after the colon -- it declares no line and is ignored "
                    "-- write order-known:<ts> with the exact ts of the defective line (a warning only)")
            continue
        if not TS_RE.match(tv):
            if report is not None:
                report.setdefault("warnings", []).append(
                    f"{carrier}: WARN `order-known:{tv}` is not a ts (YYYY-MM-DDTHH:MM:SS) -- it declares no line and "
                    "is ignored; a defect it meant stays refused -- write order-known:<ts> with the exact ts of the "
                    "defective line (a warning only)")
            continue
        named = [p for p in range(q) if file_ts[p] == tv]
        if not named:
            extra.append(f"{carrier}: `order-known:{tv}` names no line -- no line of this journal that stands before "
                         f"line {q + 1} has the ts {tv!r}, so the token declares nothing and could hide a typo -- copy "
                         "the ts of the defective line exactly (the `ts` value of that line), and put the token on a "
                         "LATER line (rule 19)")
        elif not any(p in defective_idx for p in named) and report is not None:
            if all(p < n_head for p in named):
                why = "names a line already in HEAD; HEAD lines are not judged, so nothing was declared"
            else:
                why = "names a line that carries no order defect, so nothing was declared"
            report.setdefault("warnings", []).append(f"{carrier}: WARN `order-known:{tv}` {why} (a warning only)")
    if report is not None:
        report["declared"] = len(declared_lines)
    return [replace.get(i, v) for i, v in enumerate(violations) if i not in drop] + extra


def _harvest_line_into(idx: int, event, task_id, agent, worker_ref, delegated_agents: dict, closed_tasks: set,
                        rejected_tasks: set, task_worker_refs: dict, rejected_by_agent: dict,
                        last_delegated_idx: dict, signal_log: dict) -> None:
    """Rule 9(b/c/c2) state: updates the per-task_id history by ONE line
    (used both to seed state from HEAD and, line by line, for new
    lines -- call order = line order in the file, so the state at the
    time line N is checked reflects exactly "everything earlier in
    the file"). task_worker_refs accumulates every worker_ref of every
    delegated (any agent) for this task_id -- rule 9(c2) looks for the
    claimed prior worker_ref in this same set, not only among lines by
    the same agent.

    idx -- the 0-based position of the line in the FULL file (HEAD
    lines: 0..len(head)-1 in order; new lines continue the count -- see
    the call in validate_new_lines: len(head_lines)+idx-in-new_lines).
    A self/foreign-retry gap fix (rule 9c): rejected_by_agent (task_id
    -> the set of agents whose result was rejected on that task) and
    signal_log (task_id -> a list of (idx, kind, agent) new-version
    signals: kind="delegated" on EVERY delegated, kind="lead_rejected"
    on a rejected with agent=lead, kind="escalated" on escalated) --
    together with last_delegated_idx[(task_id, agent)] -> the idx of
    that agent's LAST delegated on that task_id -- feed
    _has_new_version_signal(), which tells apart a "self" (i) and a
    "foreign" (ii) rejected under rule 9c."""
    if not (isinstance(task_id, str) and TASK_ID_RE.match(task_id)):
        return
    if event == "delegated" and isinstance(agent, str) and agent:
        delegated_agents.setdefault(task_id, set()).add(agent)
        if isinstance(worker_ref, str) and worker_ref.strip():
            task_worker_refs.setdefault(task_id, set()).add(worker_ref.strip())
        last_delegated_idx[(task_id, agent)] = idx
        signal_log.setdefault(task_id, []).append((idx, "delegated", agent))
    elif event == "accepted":
        closed_tasks.add(task_id)
    elif event == "rejected":
        rejected_tasks.add(task_id)
        if isinstance(agent, str) and agent:
            rejected_by_agent.setdefault(task_id, set()).add(agent)
            if agent == "lead":
                signal_log.setdefault(task_id, []).append((idx, "lead_rejected", agent))
    elif event == "escalated":
        signal_log.setdefault(task_id, []).append((idx, "escalated", agent))


def harvest_task_state(lines: list[str]):
    """Seeds rule 9(b/c/c2) state from the HEAD version (or any prefix
    of lines) -- (delegated_agents, closed_tasks, rejected_tasks,
    task_worker_refs, rejected_by_agent, last_delegated_idx,
    signal_log). idx inside lines is the 0-based position IN THIS LIST
    (for the HEAD seeding this is the position in head_lines, exactly
    0..len(head_lines)-1 -- see _harvest_line_into's docstring on the
    count continuing for new lines)."""
    delegated_agents: dict[str, set] = {}
    closed_tasks: set = set()
    rejected_tasks: set = set()
    task_worker_refs: dict[str, set] = {}
    rejected_by_agent: dict[str, set] = {}
    last_delegated_idx: dict[tuple, int] = {}
    signal_log: dict[str, list] = {}
    for idx, line in enumerate(lines):
        obj = _try_parse_obj(line)
        if obj is None:
            continue
        _harvest_line_into(idx, obj.get("event"), obj.get("task_id"), obj.get("agent"), obj.get("worker_ref"),
                           delegated_agents, closed_tasks, rejected_tasks, task_worker_refs,
                           rejected_by_agent, last_delegated_idx, signal_log)
    return (delegated_agents, closed_tasks, rejected_tasks, task_worker_refs,
            rejected_by_agent, last_delegated_idx, signal_log)


def _has_new_version_signal(task_id: str, agent, after_idx: int, signal_log: dict) -> bool:
    """Rule 9(c-ii), the self/foreign-retry gap: True if signal_log[task_id]
    carries a signal STRICTLY AFTER after_idx (= the idx of this same
    agent's last delegated on this task_id) of one of three kinds --
    (1) a delegated by a DIFFERENT agent (kind_agent != agent), (2) a
    rejected with agent=lead (kind="lead_rejected"), (3) an escalated
    by a DIFFERENT agent (kind="escalated", kind_agent != agent -- with
    no this narrowing, an agent could record its own escalated on its
    own task and use that very move to legalize its own repeat entry --
    a self-legalizing loop; symmetric with signal (1)). idx <= after_idx
    -- a signal from an EARLIER round (before the incoming agent's own
    last delegated) -- is stale, does not count (see the
    test_b3_stale_* tests)."""
    for idx, kind, kind_agent in signal_log.get(task_id, ()):
        if idx <= after_idx:
            continue
        if kind in ("delegated", "escalated") and kind_agent != agent:
            return True
        if kind == "lead_rejected":
            return True
    return False


def _last_head_ts(head_lines: list[str]):
    """ts of the LAST line of the HEAD version (rule 10: monotonicity
    is measured from it, not from the max over the file -- the
    journal is append-only, so HEAD's last line is chronologically the
    last of the old ones)."""
    if not head_lines:
        return None
    obj = _try_parse_obj(head_lines[-1])
    if obj is None:
        return None
    return parse_ts(obj.get("ts"))


def check_append_only(staged_lines: list[str], head_lines: list[str]):
    """Rule 1: staged must start with head as a prefix (existing lines
    are neither changed nor removed). Returns (ok, message)."""
    if len(staged_lines) < len(head_lines):
        return False, (
            f"append-only: staged has FEWER lines ({len(staged_lines)}) than "
            f"HEAD ({len(head_lines)}) -- some already-accepted journal "
            "lines are gone; dispatch history becomes unrecoverable and any "
            "accepted/rejected referencing a removed line loses its anchor "
            "-- restore every HEAD line as an unchanged prefix in staged and "
            "add new events only at the end (rule 1, append-only)"
        )
    for i, head_line in enumerate(head_lines):
        if staged_lines[i] != head_line:
            return False, (
                f"append-only: line {i + 1} diverges from the HEAD version -- "
                "an existing record was edited after the fact; the journal "
                "stops being a trustworthy log of accepted decisions, and "
                "acceptances/escalations that cited it lose their basis -- "
                f"restore line {i + 1} to its HEAD form and record the "
                "correction as a NEW line at the end, leaving the old one "
                "untouched (rule 1, append-only)"
            )
    return True, ""


_CONFIG_UNSET = object()        # config_text default: read delegation.config.yaml of the repo being validated
_CONFIG_ROOTS: dict = {}        # cwd -> repo root (one `git rev-parse` per cwd, not per line)
_CONFIG_WARNED: set = set()     # (root, text) already printed: the WARN is once per run


def _config_warn(root, text: str) -> None:
    key = (str(root), text)
    if key not in _CONFIG_WARNED:
        _CONFIG_WARNED.add(key)
        print(text, file=sys.stderr)


def read_config_text(root=None):
    """The text of delegation.config.yaml at the ROOT of the repo being validated (`root`, default: the git root of the
    cwd), or None when the file is absent there (the ladder then uses DEFAULT_BINDINGS: a repo with no config behaves as
    the repository always did). An unreadable file (not utf-8, an OS error), a config the ladder cannot parse, or a
    config with no lead model is NEVER a FAIL: one stderr WARN per run and the defaults apply (a broken config can only
    make acceptance STRICTER than the live one, spec 2.4)."""
    if root is None:
        cwd = os.getcwd()
        root = _CONFIG_ROOTS.get(cwd)
        if root is None:
            root = _CONFIG_ROOTS[cwd] = _repo_root()
    fallback = f"default bindings (lead={_tl.DEFAULT_BINDINGS['lead']}) used; fix the file"
    try:
        text = (Path(root) / CONFIG_REL).read_text(encoding="utf-8")
    except FileNotFoundError:
        return None
    except (OSError, UnicodeDecodeError) as exc:
        _config_warn(root, f"WARN: {CONFIG_REL} unreadable ({type(exc).__name__}) -- {fallback}")
        return None
    found, note = _tl.bindings(text)
    if "lead" not in found:
        _config_warn(root, f"WARN: {CONFIG_REL} unreadable ({note or 'no lead model'}) -- {fallback}")
    elif note:
        _config_warn(root, f"WARN: {CONFIG_REL}: {note}")
    return text


def _resolve_config(config_text):
    return read_config_text() if config_text is _CONFIG_UNSET else config_text


def _acceptor_rank(by, config_text) -> int:
    """rank_of_model(by); a rank the ladder cannot give counts as the floor (-1): the error direction of a resolver that
    feeds a gate is DOWNWARD."""
    rank = _tl.rank_of_model(by, config_text)
    return -1 if rank is None else rank


def _matrix_d0058_violation(event: str, agent, by: str, obj: dict, config_text=None) -> str | None:
    """Rule 11 (the acceptance matrix by FUNCTION rank, spec 20261116-architect-tier 3.1). Returns the violation text
    or None. Applies ONLY to accepted. rank(by) = tier_ladder.rank_of_model(by, config_text) (config_text None ->
    DEFAULT_BINDINGS); rank(agent) = tier_ladder.rank_of_function(agent). Branch order (the positional invariants):

    0) lead / architect / an agent outside FUNCTION_RANKS -- no matrix.
    1) `by` outside FAMILIES (exact lowercase key) -- FAIL first, so no rank arithmetic runs on an acceptor that
       cannot be identified;
    2) basis == "judge" -- REFUSED on every line, before ok_rank: no acceptor rank makes a judge basis legal;
    3) ok_rank: rank(by) > rank(agent) -- legal at any basis;
    4) FLOOR: rank(by) < builder rank -- FAIL, before every remaining basis: no basis rescues it;
    5) basis == "critic": legal iff critic rank > rank(agent);
    6) basis == "queued-to-lead": agent in QUEUED_TO_LEAD_AGENTS and builder rank <= rank(by) < lead rank;
    7) otherwise -- FAIL with the generic role-vs-tier message."""
    if event != "accepted":
        return None
    if agent in ("lead", "architect"):
        return None  # Lead-tier / Architect-tier work: presence of "by" already checked above
    agent_rank = _tl.rank_of_function(agent)
    if agent_rank is None:
        return None  # unknown agent -- the matrix doesn't define one
    families = list(_tl.FAMILIES)
    if by not in _tl.FAMILIES:
        function_word = ""
        if by in _tl.FUNCTION_RANKS:
            function_word = (f" ({by!r} is a FUNCTION word; `by` is the bare model-family word of the session that "
                             "accepts, not its function)")
        return (
            f"role-vs-tier acceptance matrix: by={by!r} is not a known "
            f"tier ({families}){function_word} -- no basis can legalize an "
            "acceptance from an acceptor whose own tier can't be "
            "identified, and the whole matrix below is unreachable while "
            f"this holds -- set 'by' to one of {families} (an "
            "enum/shape check precedes the matrix's semantics)"
        )
    basis = obj.get("basis")

    if basis == JUDGE_BASIS_VALUE:
        return (
            "role-vs-tier acceptance matrix: basis \"judge\" is not legal here -- no judge is bound in this "
            "deployment (COORDINATOR.md rule 13); accept from a tier above, or use basis 'critic' / 'queued-to-lead' "
            "for the (by, agent) pair"
        )

    by_rank = _acceptor_rank(by, config_text)
    builder_rank = _tl.rank_of_function("builder")
    lead_rank = _tl.rank_of_function("lead")
    critic_rank = _tl.rank_of_function("critic")

    if by_rank > agent_rank:
        return None

    if by_rank < builder_rank:
        return (
            f"role-vs-tier acceptance matrix: by={by!r} -- a tier below "
            f"sonnet, and no basis={basis!r} rescues it ('below Sonnet: no "
            "coordination is provided for') -- an acceptance from a "
            f"non-functioning coordinator would legalize agent={agent!r} "
            "with no real tier oversight -- raise 'by' to at least sonnet"
        )

    if critic_basis(basis)[0]:
        if critic_rank > agent_rank:
            return None
        return (
            f"role-vs-tier acceptance matrix: agent={agent!r} (rank "
            f"{agent_rank}) accepted with basis='critic', but the "
            "critic's rank is not strictly above the executor's own rank "
            "(basis 'critic' or 'critic:<critic task id>') -- this would legalize an acceptance this exact matrix row "
            "forbids, voiding the critic-gate guarantee for the "
            f"critic/designer class -- the legal path for agent={agent!r} is by "
            "a model ranked at or above lead, or basis='queued-to-lead' "
            "at a coordinator ranked below lead"
        )

    if basis == "queued-to-lead":
        if agent in QUEUED_TO_LEAD_AGENTS and builder_rank <= by_rank < lead_rank:
            return None
        return (
            f"role-vs-tier acceptance matrix: agent={agent!r} accepted "
            f"by={by!r} with basis='queued-to-lead' -- this queue is not "
            f"legal for {agent!r}-class at a {by!r} coordinator; accepting "
            "sonnet-class (builder) work through the lead queue would let "
            "the critic gate on that executor's work go unchecked -- the "
            "legal path here is basis='critic'; queued-to-lead is available only "
            f"for the class {sorted(QUEUED_TO_LEAD_AGENTS)} at a coordinator ranked below lead"
        )

    return (
        f"role-vs-tier acceptance matrix: agent={agent!r} accepted by={by!r} "
        "-- by is not strictly above the executor's rank, and no valid "
        "basis rescues it; an acceptance with no coordinator above the "
        "executor's rank and no critic justification bypasses the whole "
        "role-vs-tier acceptance matrix -- set basis='critic' (agent "
        "ranked below critic), or 'queued-to-lead' (agent in {critic,"
        "designer}, by ranked below lead); basis 'critic:<critic task id>' is read as 'critic'"
    )


def matrix_warnings(new_lines: list[str], head_lines: list[str], *, seed_lines=(),
                    config_text=_CONFIG_UNSET) -> list[str]:
    """WARN texts (never violations) for NEW `accepted` lines the matrix PASSED; a WARN never turns a pass into a FAIL:
    (a) `basis: queued-to-lead` at rank(by) >= lead rank -- the line queues work to itself (spec 3.2, F5);
    (b) agent in {critic, designer} accepted at rank(by) >= lead rank when no earlier `delegated` of that agent on that
        task carries a worker_ref starting `agent:` -- a review must come from a separate worker context (spec 2.4
        (ii), the INDEPENDENT CONTEXT detector; calibration check 6 lists these WARNs). Earlier = earlier in the logical
        journal: the seed, HEAD, then the new lines before this one;
    (c) rule 21: returned_order_warnings -- a verdict before the worker's `returned` line. This is now the one channel of
        every accepted-line WARN (the name stays)."""
    config_text = _resolve_config(config_text)
    lead_rank = _tl.rank_of_function("lead")
    isolated: set = set()            # (task_id, agent) with an earlier delegated whose worker_ref starts `agent:`
    warns: list[str] = []

    def _note(obj) -> None:
        ref = obj.get("worker_ref")
        if obj.get("event") == "delegated" and isinstance(ref, str) and ref.strip().startswith("agent:"):
            isolated.add((obj.get("task_id"), obj.get("agent")))

    for line in list(seed_lines) + list(head_lines):
        obj = _try_parse_obj(line)
        if obj is not None:
            _note(obj)
    for idx, line in enumerate(new_lines):
        obj = _try_parse_obj(line)
        if obj is None:
            continue
        agent, by, task_id = obj.get("agent"), obj.get("by"), obj.get("task_id")
        if (obj.get("event") == "accepted" and isinstance(agent, str) and isinstance(by, str)
                and agent not in ("lead", "architect") and agent in _tl.FUNCTION_RANKS and by in _tl.FAMILIES
                and _matrix_d0058_violation("accepted", agent, by, obj, config_text) is None
                and _acceptor_rank(by, config_text) >= lead_rank):
            tag = f"line {len(head_lines) + idx + 1} event='accepted' task_id={task_id!r}"
            if obj.get("basis") == "queued-to-lead":
                warns.append(_warn_line(tag, f"queued to itself: {task_id} by={by} ranks lead or above -- drop the basis"))
            if agent in QUEUED_TO_LEAD_AGENTS and (task_id, agent) not in isolated:
                warns.append(_warn_line(
                    tag, f"INDEPENDENT CONTEXT: {task_id} accepted at by={by} with no agent:<id> delegated of {agent} "
                         "-- a review must come from a separate worker context"))
        _note(obj)
    return warns + returned_order_warnings(new_lines, head_lines, seed_lines=seed_lines)


# FG7-22: a verdict written before the worker's end was journaled (t-057 class; t-1407/t-1410 lost ends). RETURNED_WARN_FROM is
# compared on the DELEGATED line: no `returned` line exists before the hook era (2026-11-16T23:09), so an older worker owes none.
RETURNED_WARN_FROM = "2026-11-17"
RETURN_ORDER_EVENTS = {"accepted", "rejected"}


def _round_step(open_pairs: dict, obj) -> None:
    """FG7-88, the ONE rule of a worker's rounds: `open_pairs[(task_id, worker_ref)]` is True while the round is open. A
    `delegated` opens a pair only when it was never seen; a `returned` closes it; a `resumed` opens it. Refs stripped; a line
    without a str task_id or a non-blank ref changes nothing. A journal with no `resumed` gives one round per pair."""
    if not isinstance(obj, dict) or not isinstance(obj.get("task_id"), str):
        return
    ref = obj.get("worker_ref")
    ref = ref.strip() if isinstance(ref, str) else ""
    if not ref:
        return
    key, event = (obj["task_id"], ref), obj.get("event")
    if event == "delegated":
        open_pairs.setdefault(key, True)
    elif event == "returned":
        open_pairs[key] = False
    elif event == "resumed":
        open_pairs[key] = True


def returned_order_warnings(new_lines: list[str], head_lines: list[str], *, seed_lines=()) -> list[str]:
    """Rule 21 (docstring): WARN texts for NEW accepted/rejected lines whose task still has a hook-era `agent:` worker with no
    `returned` line before the verdict. Pure, never raises. Owed = the LATEST such worker per (task, agent kind); a later
    delegated of the same pair, or `replaces_worker:<h>`, supersedes. Refs compared stripped."""
    warns: list[str] = []
    try:
        owed: dict = {}           # task_id -> {agent: ref}
        open_pairs: dict = {}     # (task_id, ref) -> round open?  (the one rule: _round_step)
        new_from = len(list(seed_lines)) + len(head_lines)
        for pos, line in enumerate(list(seed_lines) + list(head_lines) + list(new_lines)):
            obj = _try_parse_obj(line)
            if obj is None:
                continue
            ev, tid, ref = obj.get("event"), obj.get("task_id"), obj.get("worker_ref")
            if not isinstance(ev, str) or not isinstance(tid, str):
                continue
            ref = ref.strip() if isinstance(ref, str) else None
            if pos >= new_from and ev in RETURN_ORDER_EVENTS and TASK_ID_RE.match(tid):
                due = [(r, a) for a, r in owed.get(tid, {}).items() if open_pairs.get((tid, r)) is not False]
                if due:
                    who = ", ".join(f"{r} ({a})" for r, a in due)
                    tag = f"line {pos - len(list(seed_lines)) + 1} event={ev!r} task_id={tid!r}"
                    warns.append(_warn_line(
                        tag, f"{ev} before the worker returned: {who} has no `returned` line for {tid} -- the verdict was "
                             "written before the worker's end was journaled (after an accepted, rule 9f refuses that worker's "
                             "`returned`) -- wait for the worker's stop line; a worker whose stop was lost gets "
                             f"`python -B tools/journal_write.py returned --task {tid} --worker <ref>` before the verdict"))
            _round_step(open_pairs, obj)
            if ev == "resumed":
                agent, ts = obj.get("agent"), obj.get("ts")
                if (isinstance(agent, str) and ref and parse_ts(ts) is not None and ts[:10] >= RETURNED_WARN_FROM):
                    owed.setdefault(tid, {})[agent] = ref      # FG7-88: a resume is a start: owed again
            elif ev == "delegated":
                agent, ts = obj.get("agent"), obj.get("ts")
                gone = extract_replaces_worker(obj.get("notes"))
                if gone and tid in owed:
                    for a in [a for a, r in owed[tid].items() if r == gone.strip()]:
                        del owed[tid][a]
                if (isinstance(agent, str) and ref and ref.startswith("agent:")
                        and parse_ts(ts) is not None and ts[:10] >= RETURNED_WARN_FROM):
                    owed.setdefault(tid, {})[agent] = ref
    except Exception:  # noqa: BLE001 -- a WARN reader never takes the feature/node WARNs of the same block down
        return warns
    return warns


# TEXT REWRITE: every BLOCK-violation message in this module
# (check_append_only, _matrix_d0058_violation, validate_new_lines) is
# written by the rule of three -- (1) what's wrong, (2) what breaks as a
# consequence (for the journal/gate, not a bare restatement of the
# fact), (3) which action closes it (an imperative verb aimed at the
# line's author); the internal rule-number pointer (this module's own
# docstring numbering) is a tail, never a substitute for the action.
# The meaning of the checks themselves is UNCHANGED -- only the message
# text -- verified by a quantitative control: the old and new text ran
# against the same fixture journal produce the SAME set of violating
# line numbers (see the builder's report / test_journal_validator.py).
# The vocabulary of the FIELD a form violation is about (B-401): the JSON key names the checks
# read, plus "line" for a line that does not parse into one object. `merge-accepts:<n>:<field>`
# (merge mode) names fields from this set; nothing else is accepted as a field.
FORM_FIELDS = ("line", "ts", "event", "agent", "category", "notes", "model", "task_id", "attempt",
               "failure_class", "witness", "worker_ref", "ref", "by", "node", "id_band", "via", "session",
               "witness_by", "reviewed_through")
# the reasons journal_keys.node_of gives to a PRESENT `node` that is not a node (a field that is absent or null is not here)
NODE_BAD_REASONS = ("node_not_string", "node_not_form")


def _line_form_violations(obj: dict, tag: str, config_text=None) -> list[tuple[str, str]]:
    """The per-line FORM checks (rules 2-8, 11, 12, 18) of one parsed object, as (field, text) pairs
    in check order; `text` carries the "{tag}: " prefix. Shared by validate_new_lines (texts
    only, byte-identical to what it appended inline before) and by the merge mode, which applies
    it to the lines the other clone brought. Not here: rule 9 (needs the journal state), rule 10
    (ts order and drift need the neighbors) and the ts SHAPE check (_ts_shape_violation), nor
    the `feature` WARN."""
    out: list[tuple[str, str]] = []
    event = obj.get("event")
    task_id = obj.get("task_id")
    agent = obj.get("agent")
    ts = obj.get("ts")
    category = obj.get("category")
    notes = obj.get("notes")

    if not isinstance(ts, str) or not ts:
        out.append(("ts",
            f"{tag}: field 'ts' is missing/invalid -- without it, "
            "monotonicity (rule 10) and the narrative-future check "
            "cannot run, and the event doesn't slot into the journal's "
            "timeline at all -- set ts to ISO format with no timezone, "
            "read off the system clock at write time (rule 2)"
        ))
    if not isinstance(event, str) or not event:
        out.append(("event",
            f"{tag}: field 'event' is missing/invalid -- without it, "
            "the line matches no ENUM event, and every event-keyed "
            "check below (model/task_id/witness/the role-vs-tier "
            f"matrix) silently skips it -- set event to one of "
            f"{sorted(EVENTS)} (rule 2)"
        ))
    if not isinstance(agent, str) or not agent:
        out.append(("agent",
            f"{tag}: field 'agent' is missing/invalid -- without it, "
            "there's no record of whose result was accepted/rejected, "
            "and the role-vs-tier matrix can't decide whether the "
            "acceptance is legal -- set agent to who did the work "
            "(rule 2)"
        ))
    if not isinstance(category, str) or not category:
        out.append(("category",
            f"{tag}: field 'category' is missing/invalid -- without "
            "it, the kind of work (recon/implementation/review) "
            "is not recorded and the journal cannot be sliced by it "
            "-- set category (rule 2)"
        ))
    if not isinstance(notes, str) or not notes.strip():
        out.append(("notes",
            f"{tag}: field 'notes' is missing/empty -- without it, "
            "the event carries no recorded reason at all (this "
            "journal has no separate 'reason' field), and the "
            "decision stays unexplained on later review -- set a "
            "non-empty notes (rule 2)"
        ))

    if isinstance(event, str) and event and event not in EVENTS:
        out.append(("event",
            f"{tag}: 'event'={event!r} is not in the enum "
            f"({sorted(EVENTS)}) -- an unrecognized event matches "
            "none of the checks in rules 3-11 below, so the gate "
            "silently skips its requirements -- fix event to one of "
            "the listed values (rule 3)"
        ))

    # B-454 item 2: a non-string event (a list/dict) is already a named violation above (field
    # 'event'); it is unhashable, so the event-keyed membership tests below must not see it
    if isinstance(event, str) and event in MODEL_REQUIRED_EVENTS:
        model = obj.get("model")
        if not isinstance(model, str) or not model:
            out.append(("model",
                f"{tag}: 'model' is required for event={event} -- "
                "without it, there's no self-declaration to reconcile "
                "against the actual transcript model, and a tier "
                "mismatch goes undetected -- set model (rule 4)"
            ))

    if isinstance(event, str) and event in TASK_ID_REQUIRED_EVENTS:
        if not isinstance(task_id, str) or not task_id:
            out.append(("task_id",
                f"{tag}: 'task_id' is required for event={event} -- "
                "without it, the event attaches to no task at all, "
                "and a later closes:/defect_found/accepted has nothing "
                "to reference -- set task_id in the t-NNN format "
                "(rule 5)"
            ))
        elif not TASK_ID_RE.match(task_id):
            out.append(("task_id",
                f"{tag}: task_id {task_id!r} does not match the t-NNN "
                "format (3-9 ASCII digits, then an optional clone letter of 0-2 lower-case "
                "ASCII letters, e.g. t-123 or t-123a) -- a non-standard id is invisible "
                "to the novelty check and to the earlier-in-file "
                "existence lookup, inviting numbering collisions -- "
                f"take an id from `{_jk.JOURNAL_WRITE_DOOR}` (rule 5)"
            ))

    if event == "rejected":
        attempt = obj.get("attempt")
        if not isinstance(attempt, int) or isinstance(attempt, bool) or attempt < 1:
            out.append(("attempt",
                f"{tag}: 'attempt' must be an integer >=1 -- without "
                "an attempt number, the escalation rule (two rejected "
                "on one tier makes escalation mandatory) can't count "
                "this task's failures -- set attempt to an integer "
                "starting at 1 (rule 6)"
            ))
        failure_class = obj.get("failure_class")
        if failure_class not in FAILURE_CLASSES:
            out.append(("failure_class",
                f"{tag}: 'failure_class' must be one of "
                f"{sorted(FAILURE_CLASSES)} -- without a failure "
                "class, a later recurrence can't tell a spec defect "
                "apart from a missing capability or a tooling gap -- "
                "set failure_class from the listed values (rule 6)"
            ))

    if event == "accepted" and agent == "builder":
        witness = obj.get("witness")
        if not isinstance(witness, str) or not witness.strip():
            out.append(("witness",
                f"{tag}: 'witness' is required (non-empty string) for "
                "accepted+agent=builder -- without it, acceptance of a "
                "builder diff carries no verbatim verification-run "
                "output, and accepted becomes a retelling instead of "
                "proof -- set witness (rule 7)"
            ))

    if event in ("delegated", "returned", "resumed"):
        worker_ref = obj.get("worker_ref")
        if not isinstance(worker_ref, str) or not worker_ref.strip():
            out.append(("worker_ref",
                f"{tag}: 'worker_ref' is required (non-empty string) "
                f"for {event} -- without it, no handle exists by "
                "which a later session can find the worker or its "
                "result, and a launch that never actually happened "
                "goes undetected -- set worker_ref to the launch's "
                "handle (rule 12)"
            ))

    reviewed_through = obj.get("reviewed_through")
    if reviewed_through is not None:
        # F9: the Architect's review marker -- only a `calibrated` line carries it, and only as a git sha
        if event != "calibrated":
            out.append(("reviewed_through",
                f"{tag}: 'reviewed_through' belongs to a calibrated line only, got event={event!r} -- the field is "
                "the review marker the next Architect session reads, and on another event nothing reads it -- "
                "remove the field, or write it with `python -B tools/journal_write.py calibrated --reviewed-through <sha>`"
            ))
        elif not (isinstance(reviewed_through, str) and REVIEWED_THROUGH_RE.match(reviewed_through)):
            out.append(("reviewed_through",
                f"{tag}: 'reviewed_through' = {str(reviewed_through)[:60]!r} is not a git sha (7-40 lower-case hex "
                "characters, ^[0-9a-f]{7,40}$) -- the next review starts from this commit, and a value that is not a "
                "commit names no start -- write the sha of the last reviewed commit, e.g. from `git rev-parse --short HEAD`"
            ))

    if event == "defect_found":
        ref = obj.get("ref")
        if not isinstance(ref, str) or not ref:
            out.append(("ref",
                f"{tag}: 'ref' is required (non-empty) for "
                "defect_found -- without it, the late defect doesn't "
                "point back to the accepted event it invalidates, and "
                "the false-accept stream loses that link -- set ref "
                "to the original accepted's task_id (rule 8)"
            ))

    if event in ("accepted", "rejected"):
        by = obj.get("by")
        if not isinstance(by, str) or not by:
            out.append(("by",
                f"{tag}: 'by' is required (non-empty) for {event} -- "
                "without it, the role-vs-tier acceptance matrix has no "
                "acceptor tier to check, and a self-certified "
                "acceptance can't be told apart from a legitimate one "
                "-- set by to the accepting tier (rule 11)"
            ))
        else:
            mv = _matrix_d0058_violation(event, agent, by, obj, config_text)
            if mv:
                out.append(("by", f"{tag}: {mv}"))

    # rule 20 (offload B0): the optional `via` / `session` / `witness_by` of any event. Absent or null is never a
    # violation; a PRESENT value outside its set is (the writer and the hooks stamp them, a typo would hide the origin).
    via = obj.get("via")
    if via is not None and via not in VIA_VALUES:
        out.append(("via", f"{tag}: `via` = {via!r} is not one of {list(VIA_VALUES)} -- the field says who wrote the "
                           "line (a hook or the CLI), and calibration check 48 counts by it -- fix the value, or leave "
                           "the field out (it is optional) (rule 20)"))
    session = obj.get("session")
    if session is not None and not (isinstance(session, str) and SESSION_RE.match(session)):
        shown = repr(session)[:60]
        out.append(("session", f"{tag}: `session` = {shown} is not 1-16 characters of [A-Za-z0-9-] -- it is a short "
                               "session id, not prose -- fix the value, or leave the field out (it is optional) "
                               "(rule 20)"))
    witness_by = obj.get("witness_by")
    if witness_by is not None and witness_by not in WITNESS_BY_VALUES:
        out.append(("witness_by", f"{tag}: `witness_by` = {witness_by!r} is not one of {list(WITNESS_BY_VALUES)} -- it "
                                  "says how the witness was produced (a run of the command, a file, a pasted text) "
                                  "-- fix the value, or leave the field out (it is optional) (rule 20)"))
    # rule 18: the optional `node` of any event (delegated writes it; accepted/rejected may carry it too). Absent is never a
    # violation; a PRESENT value is judged by journal_keys.node_of -- the one reader of the form, not a second regex here.
    if "node" in obj and _jk.node_of(obj)[1] in NODE_BAD_REASONS:
        out.append(("node",
            f"{tag}: `node` = {obj['node']!r} is not `<slug>/<N>/<id>`; write e.g. `forge/5/F5-2` -- the pile, the batch "
            "number and the node id; a bare id like F5-2 is never a node (ids repeat between piles) and a list or a "
            "dict is not a string, so hop_metrics and the chain of a node cannot read the line -- fix the value, or leave "
            "the field out (it is optional) (rule 18)"
        ))
    # rule 9e: the optional `id_band` of any event. Absent or null is never a violation; a PRESENT value is judged by
    # journal_keys.id_band_of -- the one reader. Its place against the state (below / near / jump) is judged in
    # validate_new_lines, which has the state; a foreign line in a merge gets the form checks only.
    if "id_band" in obj:
        reason = _jk.id_band_of(obj)[1]
        if reason is not None:
            out.append(("id_band", _band_form_text(tag, obj["id_band"], reason)))
    return out


def _band_form_text(tag: str, value, reason: str) -> str:
    """The refusal text of a malformed `id_band` (rule 9e): FORM (not a string / not the form), REVERSED, TOO_BIG."""
    if reason == "band_reversed":
        return (f"{tag}: id_band = {value!r} ends below its start -- write the lower id first, e.g. "
                '"t-450..t-499" (rule 9e)')
    if reason == "band_too_big":
        m = _jk.BAND_RE.match(value)
        n = int(m.group(2)) - int(m.group(1)) + 1
        return (f"{tag}: id_band = {value!r} holds {n} ids; a band holds at most {_jk.BAND_MAX_SIZE} -- declare a "
                "smaller band, and a new one when it is used up (rule 9e)")
    shown = repr(value)
    if len(shown) > 80:                      # a 5000-digit value must not fill the screen
        shown = shown[:80] + "..."
    return (f'{tag}: id_band = {shown} is not "t-A..t-B" (a closed band: '
            f"at most {_jk.BAND_MAX_SIZE} ids reserved for this writer) or \"t-A..\" (an open band: this journal's ids go "
            "on from t-A), each end 3 to 9 plain digits; write e.g. \"t-450..t-499\" -- fix the value, or leave the field "
            "out (it is optional) (rule 9e)")


def _ts_shape_violation(ts, tag: str):
    """(field, text) when ts is a non-empty string that is not ISO local time without a timezone
    (rule 10's shape part), else None. A missing/empty ts is _line_form_violations' (rule 2).
    The shape check applies to a line from another clone too: ts carries no timezone, so
    monotonicity across clones is only meaningful for shapes that parse."""
    if isinstance(ts, str) and ts and parse_ts(ts) is None:
        return ("ts",
            f"{tag}: ts {ts!r} is not ISO format without a timezone -- "
            "an unparseable ts can't be checked for monotonicity or "
            "future drift, and this line silently escapes both -- "
            "write ts as ISO local time with no timezone suffix "
            "(rule 10)"
        )
    return None


_ANCHOR_FROM_HEAD = object()     # validate_new_lines: "anchor ts order on the last line of head_lines" (the default)


def validate_new_lines(new_lines: list[str], head_lines: list[str],
                        now: datetime.datetime, ts_anchor=_ANCHOR_FROM_HEAD, *,
                        seed_lines: list[str] = (), drift: bool = True,
                        order_report: dict | None = None, config_text=_CONFIG_UNSET) -> list[str]:
    """`ts_anchor`: the ts the first new line is compared with for rule 10's monotonicity. The
    default is the last line of `head_lines`. The merge mode passes HEAD's OWN last ts (or None =
    no lower bound): the lines it validates are OUR side's tail, and the kept part's last line is
    usually the foreign clone's tail, whose clock may be ahead (t-525 F4).
    `seed_lines` (t-581): lines that precede the file in the same LOGICAL journal -- the history,
    for the file that continues it. They seed rule 9 (ids seen, max, the per-task state) and the
    ts anchor when `head_lines` is empty; line numbers in the messages stay those of the file.
    `drift=False` switches off the "later than now+10min" check (the CI run: the runner's clock
    is not the writer's).
    `order_report` (rule 19): a dict the call fills with `declared` (the count of order defects declared by an
    `order-known:<ts>` token) and `warnings` (token WARN texts); None = not wanted.
    `config_text`: the text of delegation.config.yaml the acceptance matrix ranks by (None -> DEFAULT_BINDINGS); the
    default reads it from the root of the repo being validated (read_config_text)."""
    config_text = _resolve_config(config_text)
    violations: list[str] = []
    # rule 19: the ts and the order-known tokens of every line of THIS file (HEAD then new; the seed is another file)
    file_ts: list = []
    tokens: list[tuple[int, str]] = []
    for fi, fl in enumerate(list(head_lines) + list(new_lines)):
        fobj = _try_parse_obj(fl)
        file_ts.append(fobj.get("ts") if fobj is not None and isinstance(fobj.get("ts"), str) else None)
        if fobj is not None:
            tokens.extend((fi, tv) for tv in order_known_tokens(fobj.get("notes")))
    order_marks: list = []

    def _mark(defect: str, fi: int, ts_value, task_id_value) -> None:
        # call right after the append: the mark binds to the LAST violation by position
        if isinstance(ts_value, str) and ts_value:
            order_marks.append((len(violations) - 1, fi, ts_value, task_id_value, defect))

    state_lines = list(seed_lines) + list(head_lines)
    seen_task_ids = extract_task_ids(state_lines)
    # the id state (rule 9a''): HEAD and seed lines contribute their ids (the max number PER LETTER) and, read-only,
    # their old bands (BandState.top, letter ""); none of them is judged. `open_pairs`: (task, worker_ref) -> round open
    # (rule 9f: one `returned` per round; 9h: a `resumed` opens one).
    band_state = _jk.BandState()
    state_objs = []
    open_pairs: dict = {}
    for state_line in state_lines:
        state_obj = _try_parse_obj(state_line)
        if state_obj is not None:
            band_state.add(state_obj)
            state_objs.append(state_obj)
            _round_step(open_pairs, state_obj)
    letter_max = _jk.max_by_letter(state_objs)
    letter_max[""] = max(letter_max.get("", 0), band_state.top)
    if ts_anchor is _ANCHOR_FROM_HEAD:
        last_ts = _last_head_ts(head_lines) if head_lines else _last_head_ts(list(seed_lines))
    else:
        last_ts = ts_anchor
    now_limit = now + datetime.timedelta(minutes=10)
    (delegated_agents, closed_tasks, rejected_tasks, task_worker_refs,
     rejected_by_agent, last_delegated_idx, signal_log) = harvest_task_state(state_lines)

    for idx, line in enumerate(new_lines):
        line_no = len(head_lines) + idx + 1
        try:
            obj = json.loads(line)
        except (json.JSONDecodeError, TypeError) as e:
            violations.append(
                f"line {line_no}: invalid JSON ({e}) -- the line can't be "
                "parsed into any event at all, and none of rules 2-11 "
                "below can run against it -- fix the JSON for this line "
                "(one valid object per line)"
            )
            continue
        if not isinstance(obj, dict):
            violations.append(
                f"line {line_no}: parsed to something other than a JSON "
                "object (dict) -- a list/string/number carries no typed "
                "event/agent/notes fields, so none of rules 2-11 below "
                "apply -- rewrite the line as a JSON object with the "
                "required fields"
            )
            continue

        event = obj.get("event")
        task_id = obj.get("task_id")
        agent = obj.get("agent")
        tag = f"line {line_no} event={event!r} task_id={task_id!r}"

        ts = obj.get("ts")
        notes = obj.get("notes")

        # the per-line FORM checks (rules 2-8, 11, 12, 18) live in _line_form_violations, shared with
        # the merge mode; the texts come back in exactly the order they were appended here before
        violations.extend(text for _field, text in _line_form_violations(obj, tag, config_text))

        # rule 9e is RETIRED for new lines (offload B0): ids come from the clone counter, so a band on a NEW line is a
        # violation naming the writer. Old lines' bands still feed `band_state.top` above (read-only, temporal); a
        # band here never enters the state, so it cannot make this line's own id legal.
        band_retired = obj.get("id_band") is not None
        if band_retired:
            violations.append(
                f"{tag}: band_retired -- `id_band` is retired: ids are issued by the clone counter, so no line "
                f"reserves a range any more, and the field would only confuse every reader of the next id -- take "
                f"ids from `{_jk.JOURNAL_WRITE_DOOR}` and leave `id_band` out (rule 9e retired)")

        valid_tid = isinstance(task_id, str) and TASK_ID_RE.match(task_id)
        if event == "returned" and valid_tid:
            # rule 9f: a `returned` never opens, reopens or closes a task: it needs an OPEN `delegated` with the SAME
            # worker_ref earlier in the logical journal, and is written once per (task, worker_ref)
            wref = obj.get("worker_ref")
            wref = wref.strip() if isinstance(wref, str) else ""
            if task_id in closed_tasks:
                why = f"{task_id} is already closed (an accepted exists above)"
            elif wref and wref not in task_worker_refs.get(task_id, set()):
                why = (f"no earlier open delegated of {task_id} carries worker_ref {wref!r}" if task_id in seen_task_ids
                       else f"{task_id} has no delegated earlier in this journal")
            elif wref and open_pairs.get((task_id, wref)) is False:
                why = f"{task_id} already has a returned for worker_ref {wref!r} and no resumed since"
            else:
                why = None
            if why is not None:
                violations.append(
                    f"{tag}: a returned needs an open delegated with the same worker_ref -- {why}; a returned "
                    "only marks the end of a dispatch and never opens, reopens or closes a task -- write it with "
                    f"`{RETURNED_DOOR}` (rule 9f)")
        elif event == "resumed" and valid_tid:
            # rule 9h (FG7-88): a resume never opens a task, never reopens a closed one, never opens a second round
            wref = obj.get("worker_ref")
            wref = wref.strip() if isinstance(wref, str) else ""
            if task_id in closed_tasks:
                why = f"{task_id} is already closed (an accepted exists above)"
            elif wref and wref not in task_worker_refs.get(task_id, set()):
                why = (f"no earlier open delegated of {task_id} carries worker_ref {wref!r}" if task_id in seen_task_ids
                       else f"{task_id} has no delegated earlier in this journal")
            elif wref and open_pairs.get((task_id, wref)):
                why = (f"the worker {wref!r} has not returned since its last start, so this send is not a new round "
                       "-- drop the line")
            else:
                why = None
            if why is not None:
                violations.append(
                    f"{tag}: a resumed needs a worker that returned and an open task -- {why}; a resumed only marks a new "
                    "round of a worker and never opens, reopens or closes a task -- the hook writes it; by hand: "
                    f"`{RESUMED_DOOR}` (rule 9h)")
        elif event == "delegated" and valid_tid:
            if task_id not in seen_task_ids:
                # (a) a brand-new task -- rule 9a'': the full id (letter included) was never seen, it is canonical,
                # and its number is at most ID_JUMP_MAX above the max number of ITS letter. Gaps and out-of-order
                # numbers are legal (reserved ids land in any order); the clone counter is the writer's check.
                reason = _novelty_reason(task_id, letter_max)
                if reason is not None:
                    violations.append(_novelty_text(tag, task_id, reason))
                    _mark("task id issued out of order", line_no - 1, ts, task_id)
            elif task_id in closed_tasks:
                # (d) reopen forbidden -- a collision counts as two tasks.
                violations.append(
                    f"{tag}: delegated on a CLOSED task {task_id!r} (an "
                    "accepted already exists above) -- reopening a closed "
                    "task silently reuses its id for unrelated new work, "
                    "and the two tasks' history becomes indistinguishable "
                    "-- issue a fresh task_id instead of reopening "
                    f"{task_id!r} (this collision counts as two tasks, the "
                    "no-silent-reuse rule)"
                )
            else:
                prior_agents = delegated_agents.get(task_id, set())
                if isinstance(agent, str) and agent and agent not in prior_agents:
                    pass  # (b) continuation dispatch from a different tier -- legal
                else:
                    attempt = obj.get("attempt")
                    valid_attempt = (isinstance(attempt, int) and not isinstance(attempt, bool)
                                      and attempt >= 2)
                    # The self/foreign-retry gap: a "foreign" rejected
                    # (the agent whose result was rejected DIFFERS from
                    # the incoming agent) legalizes a repeat entry ONLY
                    # with a new-version signal AFTER that agent's own
                    # last delegated (rule 9c-ii) -- see
                    # _has_new_version_signal. The old, unqualified form
                    # ("valid_attempt and task_id in rejected_tasks")
                    # let ANY agent re-enter on ANY rejected of the
                    # task, including a reviewer re-entering on an
                    # EXECUTOR's rejected with nothing redone.
                    own_rejected = isinstance(agent, str) and agent in rejected_by_agent.get(task_id, set())
                    foreign_rejected = task_id in rejected_tasks and not own_rejected
                    if valid_attempt and own_rejected:
                        retry_ok = True  # (c-i) self-retry -- as before, no extra conditions
                    elif valid_attempt and foreign_rejected:
                        last_own_idx = last_delegated_idx.get((task_id, agent))
                        retry_ok = (last_own_idx is not None
                                    and _has_new_version_signal(task_id, agent, last_own_idx, signal_log))
                    else:
                        retry_ok = False
                    replaces_handle = extract_replaces_worker(notes)
                    if retry_ok:
                        pass  # (c) legal retry after rejected
                    elif replaces_handle is not None:
                        prior_refs = task_worker_refs.get(task_id, set())
                        if replaces_handle in prior_refs:
                            pass  # (c2) legal dead-worker replacement
                        else:
                            violations.append(
                                f"{tag}: replaces_worker={replaces_handle!r} does not match any "
                                f"earlier delegated worker_ref for task_id={task_id!r} -- a "
                                "fabricated replacement is forbidden (rule 9c2)"
                            )
                    else:
                        # (c) retry conditions not met, no replaces_worker marker -> (d).
                        # The failure text is branched by valid_attempt FIRST -- if
                        # attempt itself is absent/invalid, the message must say
                        # exactly that, not reason about rejected/signals (even when
                        # foreign_rejected is formally True and a fresh signal
                        # exists -- a missing attempt is on its own sufficient and
                        # the sole reason for the reject here; the text must not
                        # claim the false "no signal" when a signal is in fact
                        # present). This gate's failure text is read by a human at
                        # the moment of rejection -- worth getting exactly right.
                        if not valid_attempt:
                            reason = (
                                "the 'attempt' field is absent or invalid (must be an integer "
                                ">=2 for a repeated delegated on an existing open task_id) -- "
                                "the remaining conditions (a rejected's presence/ownership, a "
                                "new-version signal) are not checked while attempt itself is wrong"
                            )
                        elif foreign_rejected:
                            reason = (
                                "task_id has a rejected, but not of the agent re-entering "
                                "(a \"foreign\" rejected, rule 9c-ii) -- legal only if a "
                                "new-version signal appeared AFTER this agent's own last "
                                "delegated (a new delegated by a different agent / a rejected "
                                "with agent=lead / an escalated on this task_id); no such "
                                "signal exists, or it is from an earlier round and has gone "
                                "stale (the self/foreign-retry gap)"
                            )
                        else:
                            reason = "attempt is valid, but there is no rejected at all for this task_id (neither self nor foreign)"
                        violations.append(
                            f"{tag}: repeated delegated by the same agent={agent!r} on task_id={task_id!r} "
                            f"{reason} -- forbidden duplicate "
                            "(the no-silent-reuse rule); a legal alternative is a "
                            "'replaces_worker:<prior worker_ref>' marker in notes when replacing "
                            "a dead worker with no verdict (rule 9c2)"
                        )
                        _mark("repeated delegated on an open task with no legal reason", line_no - 1, ts, task_id)
        elif event in ("accepted", "rejected", "escalated", "defect_found") and valid_tid:
            if event == "escalated" and agent == "architect" and task_id not in seen_task_ids:
                # F6: an escalation to the Architect may OPEN a task (a fresh idea has no task yet) -- the same novelty
                # rule as a new `delegated` (9a''); any other escalated still needs an earlier event
                reason = _novelty_reason(task_id, letter_max)
                if reason is not None:
                    violations.append(_novelty_text(tag, task_id, reason))
                    _mark("task id issued out of order", line_no - 1, ts, task_id)
            elif task_id not in seen_task_ids:
                violations.append(
                    f"{tag}: task_id {task_id!r} does not reference "
                    "anything existing earlier in the file -- an "
                    f"{event} with no matching delegated leaves this "
                    "event orphaned, and a reader can never find what "
                    f"task it belongs to -- point task_id at a real "
                    "earlier delegated, or issue the missing delegated "
                    "first"
                )

        _round_step(open_pairs, obj)
        _harvest_line_into(len(state_lines) + idx, event, task_id, agent, obj.get("worker_ref"),
                           delegated_agents, closed_tasks, rejected_tasks, task_worker_refs,
                           rejected_by_agent, last_delegated_idx, signal_log)

        parsed_ts = parse_ts(ts) if isinstance(ts, str) else None
        shape = _ts_shape_violation(ts, tag)
        if shape is not None:
            violations.append(shape[1])
        if parsed_ts is not None:
            if last_ts is not None and parsed_ts < last_ts:
                violations.append(
                    f"{tag}: ts is not monotonic -- {parsed_ts.isoformat()} "
                    f"is earlier than the previous {last_ts.isoformat()} -- "
                    "an out-of-order ts means the journal's own event "
                    "order no longer matches wall-clock time, breaking any "
                    "later reconstruction of what happened when -- "
                    "re-read the clock and re-order the batch before "
                    "writing (rule 10)"
                )
                _mark("ts not monotone against its predecessor", line_no - 1, ts, task_id)
            if drift and parsed_ts > now_limit:
                violations.append(
                    f"{tag}: ts {ts!r} is later than now+10min "
                    f"({now_limit.isoformat()}) -- a timestamp this far "
                    "in the future was almost certainly narrated rather "
                    "than read off the clock, and later monotonicity "
                    "checks would then be anchored to a false ts -- read "
                    "ts from the system clock immediately before writing, "
                    "never from the session's narrative (rule 10)"
                )
            last_ts = parsed_ts

        # (iii) the line enters the state: its id (never its band: retired for new lines)
        if valid_tid:
            seen_task_ids.add(task_id)
            n_id, letter_id = int(valid_tid.group(1)), valid_tid.group(2)
            if n_id > letter_max.get(letter_id, 0):
                letter_max[letter_id] = n_id

    return _resolve_order_known(violations, order_marks, file_ts, tokens, len(head_lines), order_report)


def _novelty_reason(task_id: str, letter_max: dict):
    """None when the never-seen id `task_id` (a read-grammar match) may be issued, else why not (rule 9a''): "not
    canonical" (an id a writer never issues: t-0123, t-000), or "jumps" (its number is more than ID_JUMP_MAX above
    the max number of its letter; with no id of that letter yet, above 0). Out-of-order numbers and gaps are legal."""
    if not _jk.is_canonical(task_id):
        return _jk.ID_NOT_CANONICAL_TEXT
    digits, letter = _jk.parse_id(task_id)
    base = letter_max.get(letter, 0)
    if int(digits) > base + _jk.ID_JUMP_MAX:
        which = f"the highest t-NNN{letter} is {base}" if base else f"no id with letter {letter!r} exists yet" if letter \
            else "no id exists yet"
        return f"jumps more than {_jk.ID_JUMP_MAX} above the sequence ({which})"
    return None


def _novelty_text(tag: str, task_id, reason: str) -> str:
    """The refusal of a brand-new delegated (rule 9a''): the id was already used / is not canonical / jumps -- with
    the ONE road that issues ids (the clone counter, `journal_write.py next`); no band advice (bands are retired)."""
    return (f"{tag}: task_id novelty violated -- got {task_id}; it {reason} -- a task id that is not issued by the "
            "counter can collide with another session's id and is read as the same task there -- "
            f"take an id from `{_jk.JOURNAL_WRITE_DOOR}` (rule 9a'')")


def decide(staged_text: str | None, head_text: str | None,
           now: datetime.datetime | None = None, *, seed_text: str | None = None,
           drift: bool = True, order_report: dict | None = None,
           config_text=_CONFIG_UNSET) -> tuple[int, list[str]]:
    """Pure gate decision -- tested without git (see tools/test_journal_validator.py).
    `seed_text` (t-581): the lines that precede this file in its LOGICAL journal (the history, for
    the file that continues it) -- they seed rule 9 and the ts anchor, never the append-only
    comparison. `drift=False`: no "later than now+10min" check (the CI run). Without the two the
    behaviour is exactly the one before them."""
    now = now or datetime.datetime.now()
    staged_lines = split_lines(staged_text)
    head_lines = split_lines(head_text)
    ok, msg = check_append_only(staged_lines, head_lines)
    if not ok:
        return 1, [msg]
    new_lines = staged_lines[len(head_lines):]
    violations = validate_new_lines(new_lines, head_lines, now, seed_lines=split_lines(seed_text), drift=drift,
                                    order_report=order_report, config_text=config_text)
    if violations:
        return 1, violations
    return 0, []


def load_feature_ids(path=None):
    """The set of feature ids in plans/features.json, or None when the registry cannot be
    read (the value check is then skipped; the missing-field WARN still works)."""
    p = Path(path) if path else Path(__file__).resolve().parent.parent / FEATURE_REGISTRY_REL
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
        ids = {f["id"] for f in data["features"] if isinstance(f, dict) and isinstance(f.get("id"), str)}
    except (OSError, ValueError, KeyError, TypeError):
        return None
    return ids or None


def _dated_new_objs(new_lines: list[str], head_lines: list[str], events, since: str):
    """(obj, tag) for every NEW line that parses, whose `event` is a string in `events` and whose `ts` parses and is dated `since`
    (YYYY-MM-DD) or later -- the one skeleton of the dated WARNs (`feature_warnings`, `node_warnings`). `tag` is the head of the
    WARN line: `line <n in the whole file> event=<ev> task_id=<id>`. A list/dict event is skipped, not hashed (B-454 item 2)."""
    for idx, line in enumerate(new_lines):
        obj = _try_parse_obj(line)
        ev = obj.get("event") if obj is not None else None
        if not isinstance(ev, str) or ev not in events:
            continue
        ts = obj.get("ts")
        if parse_ts(ts) is None or ts[:10] < since:
            continue
        yield obj, f"line {len(head_lines) + idx + 1} event={ev!r} task_id={obj.get('task_id')!r}"


def _warn_line(tag: str, text: str) -> str:
    """The one shape of a dated WARN line: `<tag>: WARN <text> (a warning only, the journal is not blocked)`."""
    return f"{tag}: WARN {text} (a warning only, the journal is not blocked)"


def feature_problem(obj: dict, known) -> str | None:
    """FG7-70: the ONE feature predicate of the writer's refusal, this WARN and forge_metrics.run_check (c) -- three copies
    had drifted to two registries (review t-1357 C-3). None = fine; "missing" = no or empty `feature`; "unregistered" = a
    value not in `known` (known None = the registry could not be read: the value is not judged here)."""
    fv = obj.get("feature")
    if fv in (None, ""):
        return "missing"
    return "unregistered" if known is not None and fv not in known else None


def feature_warnings(new_lines: list[str], head_lines: list[str], known=None, registry=None) -> list[str]:
    """WARN texts (never violations) for NEW delegated/accepted/defect_found lines dated
    FEATURE_WARN_FROM or later that carry no `feature` field or a value not in the
    registry. `known` = the registry ids (None -> read `registry`, default this checkout's plans/features.json). Lines
    that do not parse, have no parseable ts, or are older than FEATURE_WARN_FROM are skipped."""
    if known is None:
        known = load_feature_ids(registry)
    warns: list[str] = []
    for obj, tag in _dated_new_objs(new_lines, head_lines, FEATURE_WARN_EVENTS, FEATURE_WARN_FROM):
        fv = obj.get("feature")
        problem = feature_problem(obj, known)
        if problem == "missing":
            warns.append(_warn_line(
                tag,
                f"no 'feature' field -- the event cannot be attributed to a feature in "
                f"the Forge metrics (tools/forge_metrics.py) -- add \"feature\":\"Fnn\" with an id "
                f"from {FEATURE_REGISTRY_REL}"))
        elif problem == "unregistered":
            warns.append(_warn_line(
                tag,
                f"feature={fv!r} is not an id in {FEATURE_REGISTRY_REL} -- the Forge "
                f"metrics count the event as unclassified -- use a registered id, or register the "
                f"feature in {FEATURE_REGISTRY_REL}"))
    return warns


def node_warnings(new_lines: list[str], head_lines: list[str]) -> list[str]:
    """WARN texts (never violations) for NEW `delegated` lines dated NODE_WARN_FROM or later whose node is written only as
    prose: (a) NO `node` field (absent or null) and a node token in `notes` -- one token (journal_keys.node_of finds it) or two
    different ones (`two_tokens`: the link is not guessed); (b) a good `node` field next to a token that names ANOTHER node
    (the field wins, E26). No token and no field is silence (work outside the piles is a metric, not an error); a bad `node` is
    a violation (rule 18), not a WARN. Lines that do not parse, have no parseable ts or are older are skipped. The reader is
    journal_keys.node_of -- this function holds no regex."""
    warns: list[str] = []
    for obj, tag in _dated_new_objs(new_lines, head_lines, NODE_WARN_EVENTS, NODE_WARN_FROM):
        node, why = _jk.node_of(obj)
        if obj.get("node") is None and (node is not None or why == "two_tokens"):
            seen = f"two different node tokens ({why})" if node is None else f"the node token {node!r}"
            warns.append(_warn_line(
                tag,
                f"no 'node' field, but notes carry {seen} -- hop_metrics links the hop by the token only, and "
                f"a hop with the field is linked for good -- add \"node\":\"<slug>/<N>/<id>\" (e.g. \"forge/5/F5-2\")"))
        elif why == "node_token_differ":
            warns.append(_warn_line(
                tag,
                f"'node' = {obj['node']!r} but notes name another node ({why}) -- the field wins, the hop "
                f"is linked to {node!r} -- check which node the work belongs to"))
    return warns


def decide_with_warnings(staged_text: str | None, head_text: str | None,
                         now: datetime.datetime | None = None, known=None, *,
                         seed_text: str | None = None,
                         config_text=_CONFIG_UNSET) -> tuple[int, list[str], list[str]]:
    """decide() plus the WARN list; the exit code is exactly decide()'s -- warnings never
    change it."""
    report: dict = {}
    config_text = _resolve_config(config_text)
    code, violations = decide(staged_text, head_text, now, seed_text=seed_text, order_report=report,
                              config_text=config_text)
    staged_lines = split_lines(staged_text)
    head_lines = split_lines(head_text)
    ok, _msg = check_append_only(staged_lines, head_lines)
    new_lines = staged_lines[len(head_lines):]
    warnings = feature_warnings(new_lines, head_lines, known) + node_warnings(new_lines, head_lines) if ok else []
    if ok:
        warnings = warnings + matrix_warnings(new_lines, head_lines, seed_lines=split_lines(seed_text),
                                              config_text=config_text)
        warnings = warnings + order_known_warnings(report)
    return code, violations, warnings


def order_known_warnings(report: dict) -> list[str]:
    """FG7-34: the ONE producer of the door's WARNs -- the token WARNs of `report["warnings"]` and the line
    `order-known: N declared` (commit, merge and --all paths all call it; before, only the commit path printed
    them and the weekly check 13(m) saw no count from the others). [] for no warnings and count 0."""
    report = report or {}
    out = list(report.get("warnings", []))
    n = report.get("declared")
    if n:
        out.append(f"order-known: {n} declared (summary: the number of distinct defective lines of this journal "
                   "declared by an `order-known:<ts>` token of a later line; calibration check 13(m))")
    return out


# --- MERGE MODE (t-430) ---------------------------------------------------------------------
# A merge commit concluded by hand (`git commit` after conflicts elsewhere) reaches this gate with
# the journal already merged by union (.gitattributes). decide() compares the staged file with
# HEAD (the first parent) only, so every line the OTHER parent brought reads as NEW: ids both
# clones issued independently look like `delegated on a CLOSED task`, and the interleaved tails
# break ts order -- 79 violations on the first real merge (05.10.2026). And the forge-check door
# ("add the feature field") is shut by the append-only rule. Merge mode replaces "staged starts
# with HEAD" by "staged keeps every line of BOTH parents, unchanged and in each parent's own
# order, the only change allowed being an added `feature`"; only lines new to both parents are
# validated by the ordinary rules. Outside a merge nothing here is reached (see _main).
# B-401: the lines the OTHER clone brought are additionally checked for FORM (the per-line rules
# 2-8, 11, 12, 18 and the ts shape) -- they enter this clone's history for the first time through
# this commit, and "validated by the clone that wrote them" is a premise nothing here proved
# (rule sets differ between clones; the first real merge brought 79 lines). Two ways reach it:
# a conflicted merge concluded by `git commit` (pre-commit sees MERGE_HEAD) and a clean merge
# (the pre-merge-commit hook runs `--merge-parent env`: git names the merged parent in
# GITHEAD_<sha>). The door for a defective foreign line is the `merge-accepts:<n>:<field>` token.
MERGE_EXPECTATION = ("every line of both merged journals is kept unchanged and in its order; "
                     "the only change allowed is an added `feature` field")


def _canon(obj) -> str:
    # Compared as canonical JSON text, not with ==: in Python 1 == 1.0 == True, and a changed
    # field value must not slip through as "kept" because of that.
    return json.dumps(obj, sort_keys=True, ensure_ascii=False)


def _reject_duplicate_keys(pairs):
    keys = [k for k, _v in pairs]
    if len(keys) != len(set(keys)):
        raise ValueError("duplicate key")
    return dict(pairs)


def _parse_obj_nodup(line: str):
    """The JSON object of a line, or None when it is not an object OR repeats a key anywhere in
    it. json.loads keeps the LAST of repeated keys, so `"notes":"EVIL","notes":"head"` would
    parse equal to `"notes":"head"` while another reader (or a later edit) sees a reworded line;
    a staged line that differs from its parent as text must not hide a change that way."""
    try:
        obj = json.loads(line, object_pairs_hook=_reject_duplicate_keys)
    except (ValueError, TypeError):
        return None
    return obj if isinstance(obj, dict) else None


def _merge_keeps(staged_line: str, staged_obj, parent_line: str, parent_obj) -> bool:
    """True when the staged line keeps the parent line: the same string, or the same JSON object
    plus an added `feature` (a non-empty string) the parent line did not have. A line that is not
    a JSON object is kept only by string equality; staged_obj must come from _parse_obj_nodup
    (None for a line with a repeated key, which is then kept by string equality only)."""
    if staged_line == parent_line:
        return True
    if staged_obj is None or parent_obj is None or "feature" in parent_obj:
        return False
    fv = staged_obj.get("feature")
    if not isinstance(fv, str) or not fv:
        return False
    rest = {k: v for k, v in staged_obj.items() if k != "feature"}
    return _canon(rest) == _canon(parent_obj)


def _merge_embed(name: str, parent_lines: list[str], staged_lines: list[str], staged_objs: list):
    """Embeds ONE parent into the staged lines: each parent line, in its order, takes the first
    staged line at or after the previous hit that keeps it (one staged line per parent line --
    a line present twice in the parent must be present twice in staged). Returns (indexes of the
    staged lines consumed, violations: one per parent line that found no place, hits: one entry
    per parent line -- the staged index it took, None when it found no place)."""
    consumed: set[int] = set()
    violations: list[str] = []
    hits: list = []
    pos = 0
    for n, pline in enumerate(parent_lines, start=1):
        pobj = _try_parse_obj(pline)
        hit = None
        for i in range(pos, len(staged_lines)):
            if _merge_keeps(staged_lines[i], staged_objs[i], pline, pobj):
                hit = i
                break
        if hit is None:
            violations.append(
                f"merge: {name} line {n} ({pline[:80]!r}) is not in the staged journal at its "
                f"place -- it was dropped, reworded or moved against the order of its own "
                f"journal, and every acceptance or escalation that cites it loses its anchor -- "
                f"expected: {MERGE_EXPECTATION} -- restore this line as it is in {name} "
                "(the merge mode of the append-only rule)"
            )
        else:
            consumed.add(hit)
            pos = hit + 1
        hits.append(hit)
    return consumed, violations, hits


# --- B-401: the form check of the lines the other clone brought, and its door ------------------
# `merge-accepts:<n>:<field>[,<field>]` in the notes of a NEW tail line drops exactly the form
# violations of MERGE_HEAD line n whose field is named. A bare `merge-accepts:<n>` (no field part)
# matches too, so that it can be reported -- and clears nothing.
MERGE_ACK_RE = re.compile(r"(?<!\w)merge-accepts:(\d+)(?::([a-z_]+(?:,[a-z_]+)*))?")

_MERGE_DOOR = (
    "-- this line came with the merged branch, where it is already committed and append-only "
    "forbids editing it there or here: append a new line at the tail of this merge (any legal "
    "event, e.g. dispatch_skipped) whose notes carry merge-accepts:{n}:{field} followed by the "
    "correct value and the reason, then commit again (if the merge is no longer in progress, "
    "start it again with `git merge --no-commit <branch>`)"
)


def _foreign_parse_problem(line: str):
    """None when the line parses into ONE JSON object without a repeated key (the object is
    then _parse_obj_nodup's), else the text of why not (field `line`)."""
    try:
        obj = json.loads(line, object_pairs_hook=_reject_duplicate_keys)
    except json.JSONDecodeError as e:
        return (f"invalid JSON ({e}) -- the line can't be parsed into any event at all, and none "
                "of the per-line checks can run against it")
    except (ValueError, TypeError):
        return ("a key is repeated inside the line -- json.loads keeps the last one, so a reader "
                "can see a different value than the one a check saw, and a value reworded behind "
                "a repeated key would pass unseen")
    if not isinstance(obj, dict):
        return ("parsed to something other than a JSON object (dict) -- a list/string/number "
                "carries no typed event/agent/notes fields, so no per-line check applies")
    return None


def _foreign_line_violations(line: str, staged_obj, n: int, m: int) -> list[tuple[str, str]]:
    """The form violations of ONE line that only the other clone held, as (field, text): the
    parse check, then _line_form_violations, then _ts_shape_violation, on the STAGED object (an
    added `feature` is allowed). Text: `merge: MERGE_HEAD line <n> (staged line <m>)
    event=<e> task_id=<t> [<field>]: <what is wrong>` + the door naming the exact token.
    Excluded by design (A2): rule 9 (id novelty / closed ids), ts order and drift, the
    `feature` WARN -- two clones legitimately collide on those."""
    lenient = _try_parse_obj(line)
    event = lenient.get("event") if lenient is not None else None
    task_id = lenient.get("task_id") if lenient is not None else None
    head = f"merge: MERGE_HEAD line {n} (staged line {m}) event={event!r} task_id={task_id!r}"
    found: list[tuple[str, str]] = []
    problem = _foreign_parse_problem(line)
    if problem is not None:
        found.append(("line", problem))
    else:
        tag = f"staged line {m}"
        prefix = f"{tag}: "
        pairs = list(_line_form_violations(staged_obj, tag, read_config_text()))
        shape = _ts_shape_violation(staged_obj.get("ts"), tag)
        if shape is not None:
            pairs.append(shape)
        for field, text in pairs:
            found.append((field, text[len(prefix):] if text.startswith(prefix) else text))
    return [(field, f"{head} [{field}]: {body} " + _MERGE_DOOR.format(n=n, field=field))
            for field, body in found]


def _merge_acks(tail_lines: list[str], first_staged_no: int) -> list[tuple[int, int, object]]:
    """Every merge-accepts token in the notes of the NEW tail lines: (staged line number of the
    carrier, n, fields tuple -- None for a bare token). A token anywhere else (a kept line, a
    misplaced new line) never reaches here: an acknowledgement is written at the merge it
    acknowledges and is never inherited."""
    acks = []
    for i, line in enumerate(tail_lines):
        obj = _try_parse_obj(line)
        notes = obj.get("notes") if obj is not None else None
        if not isinstance(notes, str):
            continue
        for mt in MERGE_ACK_RE.finditer(notes):
            fields = tuple(mt.group(2).split(",")) if mt.group(2) else None
            acks.append((first_staged_no + i, int(mt.group(1)), fields))
    return acks


def _apply_merge_acks(foreign: dict, acks: list) -> tuple[set, list[str]]:
    """foreign: {n: [(field, text), ...]} of the lines with a form violation. Returns (the set of
    (n, field) pairs that are acknowledged, WARN texts). A token clears exactly the fields it
    names that have a violation on that line; everything else about a token is a WARN that
    changes nothing: a bare token, an unknown field, a field with no violation on that line, an
    n that names no defective MERGE_HEAD-only line."""
    cleared: set = set()
    warns: list[str] = []
    for carrier, n, fields in acks:
        where = f"merge: WARN merge-accepts token in staged line {carrier}"
        if fields is None:
            warns.append(
                f"{where} names no field (merge-accepts:{n}) -- a bare token clears nothing, "
                "because an acknowledgement must never hide a violation it does not name -- "
                f"write merge-accepts:{n}:<field> with the field of the violation "
                f"({', '.join(FORM_FIELDS)}) (a warning only, nothing was cleared)"
            )
            continue
        if n not in foreign:
            warns.append(
                f"{where} names MERGE_HEAD line {n}, which is not a defective line the merged "
                "branch brought (a clean line, a line both parents hold, or a number outside the "
                "branch's journal) -- nothing was cleared -- check the number in the "
                "refusal text (a warning only)"
            )
            continue
        have = {f for f, _t in foreign[n]}
        for field in fields:
            if field not in FORM_FIELDS:
                warns.append(
                    f"{where} names the unknown field {field!r} for MERGE_HEAD line {n} -- "
                    f"nothing was cleared -- use one of {', '.join(FORM_FIELDS)} (a warning only)"
                )
            elif field not in have:
                warns.append(
                    f"{where} names field {field!r} for MERGE_HEAD line {n}, which has no "
                    f"violation on that field (it has: {', '.join(sorted(have))}) -- nothing "
                    "was cleared for it (a warning only)"
                )
            else:
                cleared.add((n, field))
    return cleared, warns


MAX_COLLISION_IDS = 10


def _collision_warning(staged_lines: list[str], consumed_h: set, consumed_o: set, segs, hook_path: bool):
    """The WARN text for task ids BOTH clones issued (an id with HEAD-only lines and MERGE_HEAD-only
    lines) that no declaration covers, or None. An id is covered when all of its lines on one side
    are declared in `segs`. The readers key by (label, id), so an undeclared collision is read as
    one task and one clone's accepted can hide the other's open dispatch; the gate itself stays
    on bare ids and never changes its code for this (a WARN only -- an undeclared collision is
    never silent). Names the declared instances delegated with no accepted line, so that someone
    closes the ones that are not really open."""
    only_h, only_o = consumed_h - consumed_o, consumed_o - consumed_h
    if not only_h or not only_o:
        return None

    def by_id(idxs):
        out: dict = {}
        for i in sorted(idxs):
            obj = _try_parse_obj(staged_lines[i])
            tid = obj.get("task_id") if obj is not None else None
            if isinstance(tid, str) and TASK_ID_RE.match(tid):
                out.setdefault(tid, []).append(obj)
        return out

    ids_h, ids_o = by_id(only_h), by_id(only_o)

    def declared(objs):
        return all(_jk.identity(o) in segs.listed for o in objs)

    uncovered = [tid for tid in sorted(set(ids_h) & set(ids_o))
                 if not (declared(ids_h[tid]) or declared(ids_o[tid]))]
    if not uncovered:
        return None
    shown = ", ".join(uncovered[:MAX_COLLISION_IDS])
    if len(uncovered) > MAX_COLLISION_IDS:
        shown += f" and {len(uncovered) - MAX_COLLISION_IDS} more"
    a, b = min(only_o) + 1, max(only_o) + 1
    where = ("the merge commit is made by the hook before it can hold the file: stage it in the next commit"
             if hook_path else "stage logs/journal-segments.json in this merge commit")
    text = (
        f"merge: WARN {len(uncovered)} task id(s) issued by BOTH clones are not declared: {shown} -- the "
        "readers (session_context, forge_metrics, calibration_counts) key a task by (instance, id), and "
        "with no declaration they read each id as ONE task: an accepted of one clone then hides the other "
        "clone's still-open dispatch -- declare the other clone's side: python tools/journal_keys.py "
        f"declare --label <name> --lines {a}-{b} --why \"<where the collision comes from>\" ({where}) "
        "(a warning only, the code never changes)"
    )
    # rule 9e: an uncovered id inside a closed band declared on THIS side's own lines -- the band overlapped ids the
    # other clone had already issued (a clause on the one WARN, never a violation)
    head_bands = []
    for i in sorted(only_h):
        obj = _try_parse_obj(staged_lines[i])
        band = _jk.id_band_of(obj)[0] if obj is not None else None
        if band is not None and band.hi is not None:
            head_bands.append((band, i + 1))
    for tid in uncovered[:MAX_COLLISION_IDS]:
        num = _jk.id_number(tid) if _jk.parse_id(tid)[1] == "" else None      # a band holds letterless ids only
        for band, n in head_bands:
            if num is not None and band.lo <= num <= band.hi:
                text += (f" -- {tid} lies inside band {band.label} declared on this clone (line {n}): the band "
                         "overlapped ids the other clone had already issued")
                break
    opened: set = set()
    closed: set = set()
    for line in staged_lines:
        obj = _try_parse_obj(line)
        if obj is None:
            continue
        key = _jk.task_key(obj, segs)
        if key is not None:
            if obj.get("event") == "delegated":
                opened.add(key)
            elif obj.get("event") == "accepted":
                closed.add(key)
        for token in _jk.closes_tokens(obj.get("notes")):
            tid, _at, label = token.partition("@")
            if label:
                closed.add((label, tid))
    # What this computes -- and no more: a declared instance with a `delegated` and no `accepted`
    # line and no qualified closes:t-NNN@label. The readers' OPEN DISPATCH rule is wider (an
    # escalated / rejected / decomposable last event also closes it); sharing that lifecycle rule
    # is queued, so the text says what it counted (t-525 F2).
    still_open = sorted(k for k in opened - closed if k[0])
    if still_open:
        names = ", ".join(_jk.display(k) for k in still_open[:MAX_COLLISION_IDS])
        if len(still_open) > MAX_COLLISION_IDS:
            names += f" and {len(still_open) - MAX_COLLISION_IDS} more"
        text += (f" -- declared instances delegated with no accepted line (and no closes:t-NNN@label): {names} "
                 "-- if one is not really open, close it on its clone, or later with closes:t-NNN@<label>")
    return text


def _merge_form(staged_lines: list[str], staged_objs: list, hits_o: list, consumed_h: set,
                tail_lines: list[str], last: int) -> tuple[list[str], list[str]]:
    """Step 2 of decide_merge: the form violations of the lines only MERGE_HEAD held that no
    merge-accepts token of the tail clears, and the WARNs the tokens themselves earn."""
    foreign: dict[int, list[tuple[str, str]]] = {}
    for n, hit in enumerate(hits_o, start=1):
        if hit is None or hit in consumed_h:
            continue
        found = _foreign_line_violations(staged_lines[hit], staged_objs[hit], n, hit + 1)
        if found:
            foreign[n] = found
    acks = _merge_acks(tail_lines, last + 2)
    cleared, ack_warnings = _apply_merge_acks(foreign, acks)
    form_violations = [text for n in sorted(foreign) for field, text in foreign[n]
                       if (n, field) not in cleared]
    return form_violations, ack_warnings


def _merge_segment_warnings(staged_lines: list[str], consumed_h: set, consumed_o: set,
                            segments, hook_path: bool) -> list[str]:
    # the collision WARN (B-402): ids both clones issued that no declaration covers. `segments`
    # None = the declaration of the repository holding this validator, read the way the readers
    # read it (never raises: a broken file is NO_SEGMENTS plus one "unreadable" WARN)
    seg_warnings: list[str] = []
    if segments is None:
        segments, why_unreadable = _jk.load_segments(Path(__file__).resolve().parent.parent / JOURNAL_PATH)
        if why_unreadable:
            seg_warnings.append(
                f"merge: WARN {DECLARATION_PATH} is unreadable ({why_unreadable}) -- colliding task ids "
                "are read as one task by the readers, and this check cannot tell which collisions are "
                "declared -- fix the file (python tools/journal_keys.py check names every problem) "
                "(a warning only)"
            )
    collision = _collision_warning(staged_lines, consumed_h, consumed_o, segments, hook_path)
    if collision:
        seg_warnings.append(collision)
    return seg_warnings


def _merge_placement(staged_lines: list[str], consumed: set, last: int) -> list[str]:
    placement: list[str] = []
    for i in range(last):
        if i not in consumed:
            placement.append(
                f"merge: staged line {i + 1} ({staged_lines[i][:80]!r}) is a new event placed above "
                f"kept line {last + 1} -- an event inserted into the middle of two merged journals "
                "rewrites the past of both and breaks every later id and ts check -- new events go "
                f"at the tail: move this line below line {last + 1}, or remove it if it "
                "duplicates a line one of the merged journals already holds"
            )
    return placement


def decide_merge(staged_text: str | None, head_text: str | None, other_text: str | None,
                 now: datetime.datetime | None = None,
                 known=None, *, segments=None, hook_path: bool = False,
                 seed_text: str | None = None) -> tuple[int, list[str], list[str]]:
    """Pure gate decision for a merge commit (tested without git, see
    tools/test_journal_validator_merge.py). head_text = the first parent (HEAD), other_text =
    the second (MERGE_HEAD -- in the clean-merge hook path the parent named by GITHEAD_<sha>,
    still called MERGE_HEAD in the texts); None/empty reads as no lines. Two paths reach it, see
    _main: a conflicted merge concluded with `git commit` (pre-commit, MERGE_HEAD resolves) and
    a clean merge (the pre-merge-commit hook, `--merge-parent env`).

    1. Every line of both parents must be kept by the staged lines, each parent in its own order
       (`_merge_embed`); one staged line may serve both parents. Else a violation naming the
       parent, the line number in it and the first 80 characters of the line. Invariant: no line
       either clone already recorded is dropped, reordered against its own journal or reworded.
       This violation returns at once (the steps below need a defined kept part).
    2. FORM of the lines only MERGE_HEAD held (consumed by the MERGE_HEAD scan, not by the HEAD
       scan): the parse check, _line_form_violations and _ts_shape_violation on the staged
       object -- the fields in FORM_FIELDS. Invariant: every line that enters this clone's
       history for the first time through a merge commit passes the per-line checks a commit
       here would pass. Not re-checked: HEAD-only and shared lines (each clone validated those
       when it wrote them), rule 9, ts order and drift, the `feature` WARN (two clones
       legitimately collide on those). Door: a NEW tail line whose notes carry
       `merge-accepts:<n>:<field>[,<field>]` drops exactly the violations of MERGE_HEAD line n
       whose field is named; a bare token, an unknown field, a field with no violation, an n
       that names no defective MERGE_HEAD-only line are WARNs and clear nothing. A token in a
       kept or misplaced line does not count.
    3. Staged lines kept by neither parent are NEW; all must sit after the last kept line, else a
       violation (invariant: nothing is inserted into the past). Placement does not stop the run.
    4. The new tail is validated as decide_with_warnings does, with everything above the tail
       (misplaced lines included -- they are reported by step 3 only) as its HEAD; its violations
       and warnings are returned. One difference (t-525 F4): ts MONOTONICITY of the tail is
       anchored on HEAD's OWN last ts, not on the kept part's last line (usually the foreign
       tail, whose clock may be ahead); the now+10min drift check stays. Invariant: no new event
       is dated before the newest event OUR clone already recorded, and a merge-accepts line
       stays writable when the foreign clock is hours ahead.
       Kept lines are not re-validated by the rules of step 4: each clone validated them when it
       wrote them, and two tails cannot satisfy id novelty or ts order against each other.
    5. WARN (B-402, never a violation, the code never changes): task ids BOTH clones issued (an
       id with HEAD-only lines and MERGE_HEAD-only lines) that no declaration covers; an id is
       covered when all of its lines on one side are declared in `segments` (the Segments of
       tools/journal_keys.py; None = the declaration of the repository holding this validator,
       read the way the readers read it; never raises -- a broken file is NO_SEGMENTS plus one
       "unreadable" WARN). `hook_path=True` (the clean-merge hook) words the door as "in the next
       commit": the merge commit does not exist yet when the hook runs. The gate itself keys by
       BARE ids (rule 9 unchanged); only the readers key by (label, id).
    Result: violations in the order form (MERGE_HEAD order), placement (staged order), tail; the
    code is 1 if any unacknowledged violation remains. No new lines and no violation: (0, [], [])
    plus the WARNs."""
    now = now or datetime.datetime.now()
    staged_lines = split_lines(staged_text)
    staged_objs = [_parse_obj_nodup(l) for l in staged_lines]
    head_lines = split_lines(head_text)
    other_lines = split_lines(other_text)
    consumed_h, vh, _hits_h = _merge_embed("HEAD", head_lines, staged_lines, staged_objs)
    consumed_o, vo, hits_o = _merge_embed("MERGE_HEAD", other_lines, staged_lines, staged_objs)
    violations = vh + vo
    if violations:
        # a line that found no place leaves its staged twin (a swapped or reworded line) looking
        # like a "new" one -- reporting that too would only repeat the same fault in other words
        return 1, violations, []
    consumed = consumed_h | consumed_o
    last = max(consumed) if consumed else -1
    tail_lines = staged_lines[last + 1:]

    # step 2: the form of the lines only MERGE_HEAD held
    form_violations, ack_warnings = _merge_form(staged_lines, staged_objs, hits_o, consumed_h,
                                                tail_lines, last)
    ack_warnings = _merge_segment_warnings(staged_lines, consumed_h, consumed_o, segments,
                                           hook_path) + ack_warnings

    # step 3: placement (no early return -- one run reports every independent fault)
    placement = _merge_placement(staged_lines, consumed, last)
    if last + 1 >= len(staged_lines):
        head_part = form_violations + placement
        return (1 if head_part else 0), head_part, ack_warnings
    kept_lines = staged_lines[:last + 1]
    # ts order of the tail (t-525 F4): the tail is OUR side's lines (a merge-accepts carrier, a
    # new event), so monotonicity is anchored on HEAD's OWN last ts, not on the kept part's last
    # line -- in a union that is usually the foreign clone's tail, and a foreign clock that is
    # hours ahead would make the merge-accepts door unusable (a line dated before the foreign
    # tail fails monotonicity, one dated after it fails "later than now+10min"). The drift check
    # (rule 10's now+10min) stays. Invariant: no new event is dated before the newest event OUR
    # clone already recorded; nothing is claimed about the foreign clock.
    seed_lines = split_lines(seed_text)
    anchor = _last_head_ts(head_lines) if head_lines else _last_head_ts(seed_lines)
    order_report: dict = {}
    violations = validate_new_lines(tail_lines, kept_lines, now, ts_anchor=anchor, seed_lines=seed_lines,
                                    order_report=order_report)
    warnings = (feature_warnings(tail_lines, kept_lines, known) + node_warnings(tail_lines, kept_lines)
                + matrix_warnings(tail_lines, kept_lines, seed_lines=seed_lines)
                + order_known_warnings(order_report))
    all_violations = form_violations + placement + violations
    return (1 if all_violations else 0), all_violations, ack_warnings + warnings


def _git(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], capture_output=True, text=True,
                           encoding="utf-8", errors="replace")


# While _main runs, the staged file names are read ONCE (the journal and the declaration both ask);
# outside a run there is no cache, so a direct caller always sees git's current state.
_STAGED_CACHE: dict | None = None


def is_journal_staged(journal_path: str = JOURNAL_PATH) -> bool:
    """`journal_path` is staged (any path may be asked: the declaration uses it too)."""
    if _STAGED_CACHE is not None and "names" in _STAGED_CACHE:
        return journal_path in _STAGED_CACHE["names"]
    names = _git("diff", "--cached", "--name-only").stdout.splitlines()
    if _STAGED_CACHE is not None:
        _STAGED_CACHE["names"] = names
    return journal_path in names


def get_staged_text(journal_path: str = JOURNAL_PATH) -> str:
    """The "./" prefix on the colon-path makes it resolve relative to
    _git's own cwd -- WITHOUT it, bare ":<path>" resolves relative to
    the top of whatever git repo the cwd sits inside, which silently
    diverges from cwd-relative resolution whenever the cwd is a
    subdirectory of a larger repo rather than a repo root itself (see
    gateway/lead_replay.py's git_preimage docstring for the same
    class, verified empirically there)."""
    proc = _git("show", f":./{journal_path}")
    return proc.stdout if proc.returncode == 0 else ""


def get_head_text(journal_path: str = JOURNAL_PATH) -> str:
    """Same "./" prefix rationale as get_staged_text above."""
    proc = _git("show", f"HEAD:./{journal_path}")
    return proc.stdout if proc.returncode == 0 else ""


def is_declaration_staged(declaration_path: str = DECLARATION_PATH) -> bool:
    """logs/journal-segments.json is among the staged files (B-402): the gate then runs even when
    the journal itself is not staged, because a broken declaration must not land."""
    return is_journal_staged(declaration_path)


def get_staged_declaration(declaration_path: str = DECLARATION_PATH):
    """The INDEX version of the declaration, or None when it is not in the index (git failing,
    a deleted or an empty file all read as no declaration)."""
    return get_staged_text(declaration_path) or None


def check_declaration(decl_text: str, journal_text: str | None):
    """(segments, problems): the declaration text read the way the readers read it
    (journal_keys.parse_declaration + journal_keys.check against `journal_text`, the staged
    journal). Problems come back as FAIL texts naming the file and the problem; segments is
    NO_SEGMENTS whenever there is a problem (a partial declaration is never applied). Never
    raises."""
    door = "-- fix the declaration (python tools/journal_keys.py check names every problem) or unstage it"
    try:
        segs, why = _jk.parse_declaration(decl_text)
        if segs is None:
            return _jk.NO_SEGMENTS, [f"{DECLARATION_PATH} is unreadable ({why}) {door}"]
        problems = _jk.check(split_lines(journal_text), segs)
    except Exception as e:  # noqa: BLE001 -- the declaration check must not crash the gate
        return _jk.NO_SEGMENTS, [f"{DECLARATION_PATH} could not be checked ({type(e).__name__}: {e}) {door}"]
    if problems:
        return _jk.NO_SEGMENTS, [f"{DECLARATION_PATH}: {p} {door}" for p in problems]
    return segs, []


def is_merge_in_progress() -> bool:
    """A merge is being concluded: MERGE_HEAD resolves (git commit after a conflicted merge)."""
    return _git("rev-parse", "-q", "--verify", "MERGE_HEAD").returncode == 0


def get_merge_head_text(journal_path: str = JOURNAL_PATH) -> str:
    """The journal of the second parent; the file absent there (or git failing) -> empty, the
    other side then has no lines. Same "./" prefix rationale as get_staged_text above."""
    proc = _git("show", f"MERGE_HEAD:./{journal_path}")
    return proc.stdout if proc.returncode == 0 else ""


# Hex of either case: Python's os.environ upper-cases every name on Windows, so the name the
# validator sees there is GITHEAD_<UPPER-CASE SHA> while git set GITHEAD_<lower-case sha> (measured
# 06.10.2026: a lower-case-only pattern found no parent on Windows). The sha is lower-cased on return.
GITHEAD_RE = re.compile(r"^GITHEAD_([0-9a-fA-F]{7,64})$")
_COMMIT_SHA_RE = re.compile(r"^[0-9a-fA-F]{4,64}$")

_MERGE_ONE_AT_A_TIME = ("merge one branch at a time: `git merge --no-commit <branch>`, then conclude "
                        "with `git commit` (the journal check then runs with MERGE_HEAD)")
_MERGE_PARENT_DOOR = ("to check them, merge with `git merge --no-commit <branch>` and conclude "
                      "with `git commit`")


def merge_parents_from_env(environ) -> list[str]:
    """The shas git names as merged parents of a merge in progress: the names matching
    ^GITHEAD_([0-9a-fA-F]{7,64})$ in `environ` (git sets GITHEAD_<sha>=<branch> for the hooks of
    a merge -- measured on git 2.45.1 for pre-merge-commit; not measured on Linux/macOS git).
    The sha comes back lower-cased (see GITHEAD_RE: os.environ upper-cases names on Windows).
    Sorted; other names are ignored."""
    found = set()
    for name in environ:
        m = GITHEAD_RE.match(name)
        if m:
            found.add(m.group(1).lower())
    return sorted(found)


def get_parent_text(sha: str, journal_path: str = JOURNAL_PATH) -> str:
    """The journal of the commit `sha`; absent there (or git failing) -> empty text, the other
    side then has no lines. Same "./" prefix rationale as get_staged_text above."""
    proc = _git("show", f"{sha}:./{journal_path}")
    return proc.stdout if proc.returncode == 0 else ""


def is_commit(sha: str) -> bool:
    return bool(_COMMIT_SHA_RE.match(sha)) and _git("cat-file", "-e", f"{sha}^{{commit}}").returncode == 0


def _parse_args(argv: list[str]):
    """(options, error): `--merge-parent <sha>|env` / `--merge-parent=...`, `--all`, `--base <ref>` /
    `--base=...`. An argument this gate does not know is a refusal that names it (t-581): the CI line
    used to pass the journal path positionally and the gate silently ignored it, which is how that line
    came to check nothing. options = {"merge_parent", "all", "base"}."""
    opts = {"merge_parent": None, "all": False, "base": None}
    i = 0
    while i < len(argv):
        a = argv[i]
        if a in ("--merge-parent", "--base"):
            key = "merge_parent" if a == "--merge-parent" else "base"
            if i + 1 >= len(argv):
                what = ("a commit sha, or `env` (read GITHEAD_* from the environment)" if key == "merge_parent"
                        else "a git ref the journal files are compared against")
                return opts, f"{a} needs a value: {what}"
            opts[key] = argv[i + 1]
            i += 1
        elif a.startswith("--merge-parent=") or a.startswith("--base="):
            name, _eq, value = a.partition("=")
            opts["merge_parent" if name == "--merge-parent" else "base"] = value
        elif a == "--all":
            opts["all"] = True
        else:
            return opts, (f"unknown argument {a!r} -- this gate takes `--merge-parent <sha>|env`, and `--all --base <ref>` "
                          "(CI); an argument it does not know is refused, not ignored: ignoring one is how the CI line "
                          "that passed the journal path checked nothing")
        i += 1
    if opts["all"] and opts["base"] is None:
        return opts, "--all needs --base <ref>: the files are checked as an append to that ref (CI passes the diff base of the merge request)"
    if opts["all"] and opts["merge_parent"] is not None:
        return opts, "--all and --merge-parent cannot be combined: --all checks a tree against a base, --merge-parent a merge commit being made"
    if opts["base"] is not None and not opts["all"]:
        return opts, "--base is for --all"
    return opts, None


def _parse_argv(argv: list[str]):
    """(merge_parent, error) -- the pre-t-581 view of _parse_args."""
    opts, err = _parse_args(argv)
    return opts["merge_parent"], err


def _resolve_merge_parent(spec: str, environ=None):
    """(sha, exit_code, messages): the merged parent a `--merge-parent` value names. exit_code
    is None when a sha was resolved; 0 with a WARN when `env` finds none (an unknown
    environment never blocks a merge silently, and never passes one silently -- the other
    branch's lines were then NOT checked, and the text says so); 1 with a refusal when `env`
    finds several (an octopus merge is never checked against only one parent) or the sha is not
    a commit."""
    environ = os.environ if environ is None else environ
    if spec == "env":
        shas = merge_parents_from_env(environ)
        if not shas:
            return None, 0, [
                "journal_validator: WARN the merged parent is not in the environment (GITHEAD_*): "
                "the other branch's journal lines were not checked -- " + _MERGE_PARENT_DOOR
                + " (a warning only, the merge is not blocked)"
            ]
        if len(shas) > 1:
            return None, 1, [
                f"journal_validator: more than one merged parent in the environment "
                f"({', '.join(shas)}) -- an octopus merge is never checked against only one of "
                "its parents, and the journal lines of the others would enter unchecked -- "
                + _MERGE_ONE_AT_A_TIME
            ]
        spec = shas[0]
    if not is_commit(spec):
        return None, 1, [
            f"journal_validator: the merged parent {spec!r} is not a commit of this repository -- "
            "the other branch's journal lines cannot be read, so they would enter unchecked -- "
            + _MERGE_PARENT_DOOR
        ]
    return spec, None, []


def _check_history(other_sha, journal_staged: bool, declaration_staged: bool, now):
    """The history file's part of the pre-commit run: (code, violations, warnings, segments, staged
    text of the history). Exactly the check that was the whole of _main before t-581, plus the freeze
    of the history after the switch (see _frozen_history_violation)."""
    staged_text = get_staged_text()
    head_text = get_head_text()
    # the declaration of the colliding task ids (B-402): the INDEX version, in all three paths.
    # A staged one that is unreadable or fails `check` is a FAIL; a committed one that is broken
    # reads as no declaration plus a WARN (the readers say the same on their side).
    decl_text = get_staged_declaration()
    segments, decl_problems = _jk.NO_SEGMENTS, []
    if decl_text is not None:
        segments, decl_problems = check_declaration(decl_text, staged_text)
    decl_violations: list[str] = []
    decl_warnings: list[str] = []
    if decl_problems and declaration_staged:
        decl_violations = decl_problems
    elif decl_problems:
        decl_warnings = [
            f"{DECLARATION_PATH} is unreadable or fails its check ({'; '.join(decl_problems[:3])}) -- colliding "
            "task ids are read as one task by the readers -- fix the file (python tools/journal_keys.py check) "
            "(a warning only)"]
    other_text = None                       # the other parent's journal when this is a merge commit
    if other_sha is not None:
        other_text = get_parent_text(other_sha)
        code, violations, warnings = decide_merge(staged_text, head_text, other_text, now,
                                                  segments=segments, hook_path=True)
    elif journal_staged and is_merge_in_progress():
        other_text = get_merge_head_text()
        code, violations, warnings = decide_merge(staged_text, head_text, other_text, now,
                                                  segments=segments)
    else:
        code, violations, warnings = decide_with_warnings(staged_text, head_text, now)
    if journal_staged:
        head_lines, staged_lines = split_lines(head_text), split_lines(staged_text)
        if other_text is not None:
            n_new = len(set(staged_lines) - set(head_lines) - set(split_lines(other_text)))   # a foreign line is not OUR new line
        else:
            n_new = max(0, len(staged_lines) - len(head_lines))
        if n_new:
            frozen = _frozen_history_violation(n_new, tree_has_developer_file("HEAD"))
            if frozen:
                violations = violations + [frozen]
                code = 1
    if decl_violations:
        violations = violations + decl_violations
        code = 1
    warnings = warnings + decl_warnings
    return code, violations, warnings, segments, staged_text


# --- ONE FILE PER WRITER (t-581, F0-4) -------------------------------------------------------
# logs/journal/<slug>.jsonl is a clone's own journal; logs/routing-log.jsonl is the history and is
# FROZEN once any legal journal file exists in the tree (HEAD for a commit, the base for CI). The file
# that continues the history carries `continues` on its line 1 and is validated with the history as
# its seed. The pure rules live in the helpers below; the git plumbing is _main (pre-commit,
# --merge-parent) and _run_all (CI: --all --base <ref>).

def _repo_root() -> Path:
    proc = _git("rev-parse", "--show-toplevel")
    top = proc.stdout.strip() if proc.returncode == 0 else ""
    return Path(top) if top else Path.cwd()


def _is_journal_dir_path(path: str) -> bool:
    """A path the gate treats as a journal-file candidate: a direct child of logs/journal/ ending in
    .jsonl, in any letter case (a wrong-case name is a naming FAIL, not an invisible file)."""
    parts = path.replace("\\", "/").split("/")
    return (len(parts) == 3 and parts[0].casefold() == "logs" and parts[1].casefold() == "journal"
            and parts[2].casefold().endswith(".jsonl"))


def staged_journal_changes() -> list[tuple[str, str]]:
    """[(status letter, path)] of the staged changes under logs/journal/ (renames are read as a
    deletion plus an addition, so a rename is a FAIL like a deletion)."""
    if _STAGED_CACHE is not None and "changes" in _STAGED_CACHE:
        return list(_STAGED_CACHE["changes"])
    out = _git("diff", "--cached", "--name-status", "--no-renames", "-z", "--", "logs/journal").stdout
    parts = out.split("\0")
    changes = [(parts[i][:1], parts[i + 1]) for i in range(0, len(parts) - 1, 2)
               if parts[i] and _is_journal_dir_path(parts[i + 1])]
    if _STAGED_CACHE is not None:
        _STAGED_CACHE["changes"] = changes
    return list(changes)


def index_journal_names() -> list[str]:
    """The paths under logs/journal/ in the index (what the commit would contain)."""
    proc = _git("ls-files", "-z", "--", "logs/journal")
    return [p for p in proc.stdout.split("\0") if p and _is_journal_dir_path(p)] if proc.returncode == 0 else []


def resolve_commit(ref: str) -> bool:
    return bool(ref) and not ref.startswith("-") and _git("rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}").returncode == 0


def tree_journal_paths(ref: str):
    """The journal paths (the history and logs/journal/*) in the tree of `ref`; None when git cannot
    read it."""
    proc = _git("ls-tree", "-r", "--full-tree", "--name-only", "-z", ref, "--", JOURNAL_PATH, "logs/journal")
    if proc.returncode != 0:
        return None
    return [p for p in proc.stdout.split("\0") if p and (p == JOURNAL_PATH or _is_journal_dir_path(p))]


def tree_has_developer_file(ref: str) -> bool:
    """True when the tree of `ref` holds at least one journal file with a LEGAL name -- the history is
    frozen from then on. A tree git cannot read counts as not frozen (the safe direction here is the
    one that blocks nobody on a git hiccup; CI reads the same tree and fails on its own)."""
    paths = tree_journal_paths(ref) or []
    return bool(_jk.journal_names(paths)[0])


def show_blob(ref: str, path: str):
    """The text of `path` at `ref` (repository-relative path), None when it is not there."""
    proc = _git("show", f"{ref}:{path}")
    return proc.stdout if proc.returncode == 0 else None


def _frozen_history_violation(n_new: int, frozen: bool, door: str | None = None):
    """The refusal text for `n_new` new lines of the history after the switch, else None. `door` =
    where the line goes instead (default: this clone's own file, from journal_keys.current_path)."""
    if not frozen or not n_new:
        return None
    if door is None:
        rel, why = _jk.current_path(_repo_root())
        door = rel if rel else f"your own journal file (there is none to write to yet: {why})"
    return (f"{JOURNAL_PATH} is the history and takes no new lines since the per-developer journal began, "
            f"and {n_new} new line(s) are staged for it -- the history is closed so that two clones never "
            f"append to one file, and a line written here belongs to no writer's file -- write the line "
            f"into {door}")


def developer_file_violations(rel: str, lines: list[str]) -> list[str]:
    """Rule 17.4, the line-1 rules of a developer file: its first line is a journal_created; `continues`
    is allowed on line 1 only and only with the value logs/routing-log.jsonl. An empty file passes."""
    out: list[str] = []
    if not lines:
        return out
    first = _try_parse_obj(lines[0])
    if first is None or first.get("event") != "journal_created":
        out.append(f"{rel} line 1 is not a journal_created event -- a journal file starts with the line that says "
                   "where it comes from, and the readers take `continues` from it -- make line 1 a journal_created "
                   "(add \"continues\":\"logs/routing-log.jsonl\" only if this file continues the history)")
    for n, line in enumerate(lines, start=1):
        obj = _try_parse_obj(line)
        if obj is None or _jk.CONTINUES_FIELD not in obj:
            continue
        if n != 1:
            out.append(f"{rel} line {n}: `continues` is allowed on line 1 only -- anywhere else it would silently "
                       "merge this file's task ids with the history's -- remove it from this line")
        elif obj[_jk.CONTINUES_FIELD] != _jk.HISTORY_REL:
            out.append(f"{rel} line 1: `continues` must be {_jk.HISTORY_REL!r}, got {str(obj[_jk.CONTINUES_FIELD])[:60]!r} "
                       "-- the only thing a journal file can continue is the history -- fix the value or remove the field")
    return out


def _one_writer_violation(rel: str, slug, why, n_new: int):
    """A commit that is not a merge appends only to ITS OWN file (F-10): `slug` = this clone's developer
    slug (None = unknown, `why` = the reason). None when fine."""
    if not n_new:
        return None
    stem = rel.rsplit("/", 1)[-1][:-len(".jsonl")]
    if slug is None:
        return (f"{rel}: {n_new} new line(s) are staged, but this clone's developer slug is unknown ({why}) -- "
                "without it nobody can tell whose file this is, and one file has one writer -- set the slug, then commit again")
    if slug != stem:
        return (f"{rel}: {n_new} new line(s) are staged in the file of writer {stem!r}, and this clone is {slug!r} -- one "
                f"file has one writer, and a line written into another's file reaches a clone that never knew it -- write "
                f"the line into your own file {_jk.JOURNAL_DIR_REL}/{slug}.jsonl; a labelled `closes:t-NNN@{stem}` reaches {stem}'s task")
    return None


def _label_warnings(rel: str, new_lines: list[str], first_no: int, known: set) -> list[str]:
    """WARN texts (F-7) for `closes:t-NNN@label` tokens and `ref` values in NEW lines whose label is not
    a known one (a file in the index, a declared segment, `main`): such a token closes nothing, and
    the file with that label may live on a branch that is not merged yet."""
    warns = []
    for i, line in enumerate(new_lines):
        obj = _try_parse_obj(line)
        if obj is None:
            continue
        tokens = list(_jk.closes_tokens(obj.get("notes")))
        ref = obj.get("ref")
        if isinstance(ref, str):
            tokens.append(ref)
        for tok in tokens:
            m = _jk.REF_RE.match(tok)
            label = m.group(2) if m else None
            if label and label != _jk.MAIN_LABEL and label not in known:
                warns.append(f"{rel} line {first_no + i}: WARN {tok!r} names the label {label!r}, which no journal file or "
                             "declared segment has here -- the token closes nothing (the file may live on a branch "
                             "that is not merged yet) (a warning only)")
    return warns


def _two_clones_warning(rel: str, head_text, other_text):
    """WARN (F-9) when a merge brings lines of one developer file from BOTH sides: one writer per file broke."""
    head, other = split_lines(head_text), split_lines(other_text)
    if set(head) - set(other) and set(other) - set(head):
        return (f"merge: WARN {rel} got lines from both sides of the merge -- it was written by two clones, and one "
                "file has one writer -- give each clone its own slug (developer: in tools/dev.config.yaml) "
                "(a warning only)")
    return None


def _developer_file_result(rel, staged_text, head_text, seed_text, now, *, merge_other=None, hook_path=False,
                           slug=None, slug_why=None, drift=True, one_writer=True, known_labels=None):
    """(violations, warnings) of ONE developer file: line-1 rules, the ordinary decide (or decide_merge),
    the one-writer rule (not in a merge), the label warnings. Pure but for the arguments."""
    lines = split_lines(staged_text)
    head_lines = split_lines(head_text)
    violations = developer_file_violations(rel, lines)
    warnings: list[str] = []
    if merge_other is not None:
        _code, vv, ww = decide_merge(staged_text, head_text, merge_other, now, segments=_jk.NO_SEGMENTS,
                                     hook_path=hook_path, seed_text=seed_text)
        two = _two_clones_warning(rel, head_text, merge_other)
        if two:
            ww = ww + [two]
        known = set(split_lines(head_text)) | set(split_lines(merge_other))
        new_lines = [l for l in lines if l not in known]
    else:
        if drift:
            _code, vv, ww = decide_with_warnings(staged_text, head_text, now, seed_text=seed_text)
        else:                   # --all: no clock, but the matrix WARNs do not depend on it (calibration check 6 (i))
            rep: dict = {}
            _code, vv = decide(staged_text, head_text, now, seed_text=seed_text, drift=False, order_report=rep)
            ww = (matrix_warnings(lines[len(head_lines):], head_lines, seed_lines=split_lines(seed_text))
                  + order_known_warnings(rep))
        ow = _one_writer_violation(rel, slug, slug_why, max(0, len(lines) - len(head_lines))) if one_writer else None
        if ow:
            violations.append(ow)
        new_lines = lines[len(head_lines):]
    warnings.extend(ww)
    if known_labels is not None:
        warnings.extend(_label_warnings(rel, new_lines, len(lines) - len(new_lines) + 1, known_labels))
    return violations + vv, warnings


def _check_developer_files(changes, other_sha, now, segments, history_staged_text):
    """[(path, code, violations, warnings)] for the staged changes under logs/journal/ and the
    cross-file rules (names, a second successor)."""
    root = _repo_root()
    slug, slug_why = _jk.developer_slug(root)
    merging = other_sha is not None or is_merge_in_progress()
    staged_paths = sorted({p for s, p in changes if s != "D"})
    # a NEW file is in the index listing AND in the staged paths: one path once, or it "repeats its own slug"
    files, name_problems = _jk.journal_names(sorted(set(index_journal_names()) | set(staged_paths)), segments.labels)
    known = {_jk.MAIN_LABEL} | set(segments.labels) | {f.slug for f in files}
    results = []
    successors = []
    for status, p in sorted(set(changes), key=lambda c: c[1]):
        if status == "D":
            results.append((p, 1, [f"{p} is removed or renamed by this commit -- a journal file is never removed or "
                                   "renamed: its lines are the record other lines cite, and a reader finds them "
                                   f"by the path -- restore it from HEAD (`git checkout HEAD -- {p}`)"], []))
            continue
        bad = [str(pr) for pr in name_problems if p in pr.paths]
        if bad:
            results.append((p, 1, bad, []))
            continue
        staged_text, head_text = get_staged_text(p), get_head_text(p)
        seed = None
        if _jk.continues_value(staged_text) == _jk.HISTORY_REL:
            seed = history_staged_text if history_staged_text is not None else get_staged_text(JOURNAL_PATH)
            successors.append(p)
        other = None
        if merging:
            other = get_parent_text(other_sha, p) if other_sha is not None else get_merge_head_text(p)
        v, w = _developer_file_result(p, staged_text, head_text, seed, now, merge_other=other,
                                      hook_path=other_sha is not None, slug=slug, slug_why=slug_why,
                                      known_labels=known)
        results.append((p, 1 if v else 0, v, w))
    for f in files:                                       # successors already in the index, not staged now
        if f.path not in staged_paths and _jk.continues_value(get_staged_text(f.path)) == _jk.HISTORY_REL:
            successors.append(f.path)
    if len(set(successors)) > 1:
        results.append((_jk.JOURNAL_DIR_REL + "/", 1, [
            "more than one journal file continues the history (" + ", ".join(sorted(set(successors))) + ") -- "
            "two files with the same task numbers would read as one task each -- keep `continues` in one file"], []))
    staged_set = set(staged_paths)
    other_problems = [str(pr) for pr in name_problems if not (set(pr.paths) & staged_set)]
    if other_problems:
        results.append((_jk.JOURNAL_DIR_REL + "/", 0, [], [p + " (a warning only: not part of this commit)" for p in other_problems]))
    return results


def _emit(path: str, code: int, violations: list[str], warnings: list[str]) -> None:
    if code:
        print(f"journal_validator: {path} FAILED validation:", file=sys.stderr)
        for v in violations:
            print(f"  - {v}", file=sys.stderr)
    if warnings:
        print(f"journal_validator: {path} WARN ({len(warnings)}, does not block):", file=sys.stderr)
        for w in warnings:
            print(f"  - {w}", file=sys.stderr)


def _main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    opts, argv_error = _parse_args(argv)
    if argv_error:
        print(f"journal_validator: {argv_error}", file=sys.stderr)
        return 1
    if opts["all"]:
        return _run_all(opts["base"])
    journal_staged = is_journal_staged()
    declaration_staged = is_declaration_staged()
    changes = staged_journal_changes()
    if not journal_staged and not declaration_staged and not changes:
        return 0  # rule: nothing this gate looks at is staged -> silent exit 0
    other_sha = None
    if opts["merge_parent"] is not None and (journal_staged or changes):
        other_sha, early_code, messages = _resolve_merge_parent(opts["merge_parent"])
        for msg in messages:
            print(msg, file=sys.stderr)
        if early_code is not None:
            return early_code
    now = datetime.datetime.now()
    code, violations, warnings, segments, history_text = _check_history(other_sha, journal_staged,
                                                                        declaration_staged, now)
    results = [(JOURNAL_PATH, code, violations, warnings)]
    if changes:
        results.extend(_check_developer_files(changes, other_sha, now, segments, history_text))
    worst = 0
    for path, c, v, w in results:
        _emit(path, c, v, w)
        worst = worst or c
    return worst


def _run_all(base: str) -> int:
    """CI: every journal file of the tree of HEAD against the tree of `base` (--all --base <ref>). Per
    file: it must still be there; the base text must be an unchanged prefix of the HEAD text; then the
    ordinary rules over the lines added since the base (the file that continues the history, with the
    history of HEAD as its seed). The ts drift check is OFF: the runner's clock is not the writer's.
    The history is frozen by the BASE tree. The one-writer rule is not checked: CI does not know the
    writer. The names and the single successor are checked on the HEAD tree."""
    if not resolve_commit(base):
        print(f"journal_validator: --base {base!r} does not resolve to a commit of this repository -- the files cannot "
              "be compared with a ref that is not there -- pass the diff base of the merge request or `HEAD~1`",
              file=sys.stderr)
        return 1
    if (_git("merge-base", "--is-ancestor", "HEAD", base).returncode == 0
            and _git("rev-parse", "HEAD").stdout.strip() != _git("rev-parse", f"{base}^{{commit}}").stdout.strip()):
        print(f"journal_validator: --all: {base} is ahead of HEAD; fetch or choose the base of this branch -- a base that "
              "is a descendant of the tree being checked would make every journal file look shortened", file=sys.stderr)
        return 1
    head_paths, base_paths = tree_journal_paths("HEAD"), tree_journal_paths(base)
    if head_paths is None or base_paths is None:
        raise RuntimeError("git could not list the journal files of HEAD or of the base")
    now = datetime.datetime.now()
    decl_text = show_blob("HEAD", DECLARATION_PATH)
    segs, decl_problems = _jk.NO_SEGMENTS, []
    history_head = show_blob("HEAD", JOURNAL_PATH) or ""
    if decl_text is not None:
        segs, decl_problems = check_declaration(decl_text, history_head)
    results = []
    if decl_problems:
        results.append((DECLARATION_PATH, 1, decl_problems, []))
    frozen = bool(_jk.journal_names(base_paths, segs.labels)[0])
    files, name_problems = _jk.journal_names(head_paths, segs.labels)
    if name_problems:
        results.append((_jk.JOURNAL_DIR_REL + "/", 1, [str(p) for p in name_problems], []))
    known = {_jk.MAIN_LABEL} | set(segs.labels) | {f.slug for f in files}
    successors = []
    for p in sorted(set(head_paths) | set(base_paths)):
        if p not in head_paths:
            results.append((p, 1, [f"{p} exists in the base and not in the tree -- a journal file is never removed "
                                   "or renamed -- restore it"], []))
            continue
        head_text = show_blob("HEAD", p) or ""
        base_text = show_blob(base, p) if p in base_paths else None
        ok, msg = check_append_only(split_lines(head_text), split_lines(base_text))
        if not ok:
            results.append((p, 1, [msg + " (the tree must hold the base text as an unchanged prefix of this file)"], []))
            continue
        base_lines, head_lines = split_lines(base_text), split_lines(head_text)
        if p == JOURNAL_PATH:
            rep: dict = {}
            v = decide(head_text, base_text, now, drift=False, order_report=rep)[1]
            fz = _frozen_history_violation(len(head_lines) - len(base_lines), frozen,
                                           door=f"your own {_jk.JOURNAL_DIR_REL}/<slug>.jsonl")
            if fz:
                v = v + [fz]
            results.append((p, 1 if v else 0, v, order_known_warnings(rep)))
            continue
        if p not in {f.path for f in files}:
            continue                                      # an illegal name: reported above
        seed = None
        if _jk.continues_value(head_text) == _jk.HISTORY_REL:
            seed = history_head
            successors.append(p)
        v, w = _developer_file_result(p, head_text, base_text, seed, now, one_writer=False, drift=False,
                                      known_labels=known)
        results.append((p, 1 if v else 0, v, w))
    if len(successors) > 1:
        results.append((_jk.JOURNAL_DIR_REL + "/", 1, [
            "more than one journal file continues the history (" + ", ".join(successors) + ") -- keep `continues` in one file"], []))
    worst = 0
    for path, c, v, w in results:
        _emit(path, c, v, w)
        worst = worst or c
    return worst


def main(argv: list[str] | None = None) -> int:
    """Outer boundary: any exception (not a validation FAIL, but a crash
    of the validator itself) -> exit 2 with a traceback, fail-closed,
    same as mechanism_gate."""
    global _STAGED_CACHE
    _STAGED_CACHE = {}          # one `git diff --cached` per run (see is_journal_staged)
    try:
        return _main(argv)
    except Exception:
        traceback.print_exc()
        return 2
    finally:
        _STAGED_CACHE = None


if __name__ == "__main__":
    sys.exit(main())
