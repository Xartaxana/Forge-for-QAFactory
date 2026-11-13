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

Checks (numbering matches this file's own spec / CLAUDE.md's "Routing
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
    a) task_id == max(all t-NNN in the file so far)+1 -- always legal
       (a brand-new task); with ID BANDS (rule 9e) the legal new ids are the
       file's own next id (max+1, past every closed band) and the next id
       of each closed band that is not used up;
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
    e) ID BANDS (F6-58) -- the door of (a) for a second writer of one file
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
    For a new accepted/rejected/escalated/defect_found -- it must
    reference a task_id already seen earlier in the file (in HEAD or
    earlier in this same commit); unchanged otherwise.
10. ts of new lines is monotonic relative to HEAD's last line and to
    each other; not later than now+10 minutes (a narrative-future
    timestamp). No lower bound.
11. The role-vs-tier acceptance matrix (NEW lines only, accepted
    only -- rejected carries "by" with no further check, a literal
    reading of the spec). For agent=lead the matrix doesn't apply --
    presence of "by" is enough. For agent in {scout, builder, critic,
    designer} (a revision after a live leak: two different sonnet-tier
    coordinators independently accepted a sonnet-class (builder) result
    via basis=queued-to-lead -- a bare "basis in BASIS_VALUES" set
    membership check passed that basis regardless of WHICH by/agent
    pair it was attached to; the check is now legality PER (by, agent)
    PAIR instead of bare membership).
    An enum check PRECEDES branches (a)-(f): "is by even in
    TIER_ORDER" -- an unknown by FAILS unconditionally, BEFORE the
    judge branch too -- judge's by-independence (branch b below)
    applies only to LEGAL tier words; no basis of any kind legalizes an
    acceptance from an unknown acceptor:

    a) ok_tier -- tier(by) > tier(agent) (haiku<sonnet<opus<fable by
       agent: scout=haiku, builder=sonnet, critic=opus, designer=opus
       (designer's deployment binding, same tier as critic; see
       .claude/agents/designer.md)) -- legal at
       ANY basis (or none).
    b) basis=="judge" -- legal ONLY when the line's OWN "category" is
       ∈ {"recon", "implementation"} (a leaf-class dispatch per this
       toolkit's own CLAUDE.md, "Leaf routing": "Judge acceptance is
       legitimate ONLY for leaf-class dispatches (recon, or
       implementation to a written spec)"); unchanged from before this
       batch. CHECKED FIRST, independent of tier(by) -- a calibrated
       judge is not a coordinator-tier resolution, so it is not
       subject to the floor in (c).
    c) FLOOR "below sonnet: no coordination provided for": if tier(by)
       is KNOWN and strictly below sonnet's tier (i.e. by=="haiku")
       AND ok_tier does not hold AND basis is not "judge" -- FAIL
       unconditionally, no basis rescues it (this toolkit's own
       CLAUDE.md "Role != tier" matrix: "below Sonnet | no
       coordination is provided for | --"). Decision fork (documented
       deliberately): the core rule's literal text ("OR the decision
       carries a higher tier's input (a critic verdict)") would read
       basis="critic" as rescuing ANY by, including haiku -- but the
       matrix's "below Sonnet" row states, without exception, "no
       coordination is provided for"; a haiku-tier session is not a
       functioning coordinator at all in this structure. The floor
       wins over the general "carries higher tier's input" allowance
       for basis="critic"/"queued-to-lead" (but NOT for basis="judge"
       -- see (b), a separate non-coordinator path).
    d) basis=="critic" -- legal ONLY when the critic tier (opus,
       fixed) is strictly above tier(agent), i.e. agent is
       scout/builder-class: a critic verdict on top of the critic's
       own class (agent=="critic") is not meaningful and NOT legal.
    e) basis=="queued-to-lead" -- legal ONLY for agent=="critic"
       (critic-class, tier opus) AND by ∈ {"sonnet", "opus"} (for
       by="sonnet" the queue is legal specifically for critic-class --
       NOT builder-class: at a sonnet coordinator, builder-class
       acceptance is legal only via basis="critic"; for by="opus" the
       queue is legal for critic-class as an equal-tier concession).
    f) any other basis (including none) -- FAIL with the generic
       role-vs-tier message.

    SURFACE NARROWING (a later revision, on a critic verdict): the
    by-shape enum gate applies ONLY to accepted with agent ∈ {scout,
    builder, critic, designer} (designer added to AGENT_TIER, same
    class); OUTSIDE the gate (recorded DECISIONS, not oversights):
    rejected -- by carries no matrix check at all (a literal reading
    of the spec, see the top of rule 11); agent=lead -- a non-tier by
    is legal (a live precedent, by="operator", in
    logs/routing-log.jsonl -- the operator sits at the apex of the
    hierarchy, rule 11a); agent outside AGENT_TIER -- the matrix is
    simply undefined by the spec (an early return before any branch).
    Form-validation candidates for these three neighbors are queued
    for a future calibration pass.
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
    "journal_created", "calibrated",
}
MODEL_REQUIRED_EVENTS = {"delegated", "escalated", "accepted", "rejected"}
TASK_ID_REQUIRED_EVENTS = {"delegated", "accepted", "rejected", "escalated", "defect_found"}
FAILURE_CLASSES = {"spec", "capability", "recon", "tooling"}
TIER_ORDER = {"haiku": 0, "sonnet": 1, "opus": 2, "fable": 3}
AGENT_TIER = {
    "scout": "haiku", "builder": "sonnet", "critic": "opus",
    # designer added: designer's deployment binding is opus (see
    # .claude/agents/designer.md, model: opus) -- the same tier as
    # critic. Class of the gap before this line existed: agent=
    # "designer" was outside AGENT_TIER, so the role-vs-tier
    # acceptance matrix silently did not apply to its accepted lines
    # (see the "agent not in AGENT_TIER" early return below).
    "designer": "opus",
}
# The upper-mid-tier CLASS (decision, after a critic finding): branch
# (5) basis="queued-to-lead" used to be keyed on the literal name
# agent=="critic" -- a narrowing by NAME, not by CLASS. designer
# carries the same tier (opus) and the same coordinator-facing
# semantics for branch (5) -- the queue to Lead is legal for BOTH when
# the coordinator is not strictly above. basis="critic" is NOT
# extended to designer the same way -- branch (4) already works by a
# NUMERIC tier comparison, not by name, so a same-tier critic input
# already fails to legalize designer's acceptance too, without any
# separate change (same as it already fails for agent=="critic" itself).
QUEUED_TO_LEAD_AGENTS = {"critic", "designer"}
# Known non-judge basis string values -- a PLAIN enum/reference (external
# consumers: PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md, log_append.py), no
# longer used as a legality check "basis in BASIS_VALUES" -- legality is
# decided per (by, agent) pair in _matrix_d0058_violation, not bare
# membership (closes a leak where basis=queued-to-lead passed membership
# for ANY by/agent, including builder-class at a sonnet coordinator).
BASIS_VALUES = {"critic", "queued-to-lead"}
JUDGE_BASIS_VALUE = "judge"
# Leaf-class categories a "judge" basis is legal for (rule 11 / this
# toolkit's own CLAUDE.md "Leaf routing" section): "recon, or
# implementation to a written spec".
LEAF_CATEGORIES = {"recon", "implementation"}

TASK_ID_RE = re.compile(r"^t-(\d{3,})$")
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


def _matrix_d0058_violation(event: str, agent, by: str, obj: dict) -> str | None:
    """Rule 11 (the pair-legality rewrite, 2026-07-24: pair-legality
    replaces membership-in-set). Returns the violation text or None. Applies
    ONLY to accepted (a literal reading of the spec: "accepted is
    legal when..."; rejected carries "by" with no further tier/basis
    check).

    Check order is deliberately NOT a "first match wins, unexplained"
    if-cascade -- each branch reads against one row of the CLAUDE.md
    "Role != tier" table (see the module docstring's rule 11 for the
    full pair table and quotes):

    1) basis=="judge" -- a separate, non-coordinator acceptance path
       (a calibrated judge, rule 13/leaf routing): legal ONLY on a
       leaf-class category, INDEPENDENT of tier(by) -- checked first so
       the floor in (3) never intercepts it.
    2) ok_tier: tier(by) > tier(agent) -- legal at any basis.
    3) FLOOR: tier(by) is known and strictly below sonnet (i.e.
       by=="haiku") -- FAIL unconditionally, no basis (other than the
       already-handled "judge") rescues it ("below Sonnet: no
       coordination is provided for").
    4) basis=="critic": legal only if tier("opus") is strictly above
       tier(agent) -- i.e. agent is scout/builder-class, not critic.
    5) basis=="queued-to-lead": legal ONLY for agent=="critic" AND
       by ∈ {"sonnet", "opus"}.
    6) otherwise -- FAIL with the generic role-vs-tier message."""
    if event != "accepted":
        return None
    if agent == "lead":
        return None  # Lead-tier work: presence of "by" already checked above
    if agent not in AGENT_TIER:
        return None  # unknown agent -- the matrix doesn't define one
    if by not in TIER_ORDER:
        # An enum/shape check ("is by even a known tier") precedes ANY
        # matrix semantics, including judge -- no basis legalizes an
        # acceptance from an unknown acceptor; ok_tier/floor stayed
        # silent at by_tier=None, and basis="critic"/"judge" never
        # looked at by at all -- this check closes that hole.
        return (
            f"role-vs-tier acceptance matrix: by={by!r} is not a known "
            f"tier ({sorted(TIER_ORDER)}) -- no basis can legalize an "
            "acceptance from an acceptor whose own tier can't be "
            "identified, and the whole matrix below is unreachable while "
            f"this holds -- set 'by' to one of {sorted(TIER_ORDER)} (an "
            "enum/shape check precedes the matrix's semantics)"
        )
    agent_tier_name = AGENT_TIER[agent]
    agent_tier = TIER_ORDER[agent_tier_name]
    by_tier = TIER_ORDER.get(by)
    basis = obj.get("basis")

    # (1) judge -- separate path, not a coordinator resolution; category
    # decides everything, checked before tier/floor. NARROWED (a
    # critic finding): the judge accepts ONLY leaf-class EXECUTORS
    # (agent ∈ {scout,builder}) -- specs (designer) and reviews
    # (critic) stay outside the judge's remit by policy, regardless of
    # category (before this fix, agent="designer" + basis="judge" +
    # category="implementation" wrongly passed, since only category
    # was checked, never agent). Order: the category gate runs FIRST
    # (a non-leaf category fails for ANY agent, including scout/
    # builder -- a regression pin for the pre-existing tests), the
    # agent gate runs SECOND, only once category is already leaf-class.
    if basis == JUDGE_BASIS_VALUE:
        if obj.get("category") not in LEAF_CATEGORIES:
            return (
                f"role-vs-tier acceptance matrix: basis \"judge\" is legal "
                "only for a leaf-class dispatch (category recon/"
                f"implementation), got category={obj.get('category')!r} -- "
                "a judge is not calibrated to evaluate non-executor work, "
                "and this acceptance would go through with no critic "
                "judgment over architecture or spec -- switch basis to "
                "'critic'/'queued-to-lead' for the (by, agent) pair, or fix "
                "category if the work is genuinely leaf-class"
            )
        if agent not in ("scout", "builder"):
            return (
                f"role-vs-tier acceptance matrix: basis \"judge\" is legal "
                f"only for agent∈{{scout,builder}} (leaf-class EXECUTORS) -- "
                f"agent={agent!r} is not eligible; a judge accepting "
                "designer/critic-class output would bypass the mandatory "
                "critic gate on specs and reviews -- switch basis to "
                "'critic'/'queued-to-lead' for the (by, agent) pair, judge "
                "is not legal for this agent regardless of category"
            )
        return None

    # (2) ok_tier -- strictly above, legal at any basis (or none).
    if by_tier is not None and by_tier > agent_tier:
        return None

    # (3) FLOOR: by of a known tier strictly below sonnet -- no
    # coordination provided for, no basis rescues it ("Role != tier"
    # matrix: "below Sonnet: no coordination is provided for"). The
    # fork against the core rule's literal "carries a higher tier's
    # input" text is documented and resolved in the floor's favor --
    # see the module docstring's rule 11.
    if by_tier is not None and by_tier < TIER_ORDER["sonnet"]:
        return (
            f"role-vs-tier acceptance matrix: by={by!r} -- a tier below "
            f"sonnet, and no basis={basis!r} rescues it ('below Sonnet: no "
            "coordination is provided for') -- an acceptance from a "
            f"non-functioning coordinator would legalize agent={agent!r} "
            "with no real tier oversight -- raise 'by' to at least sonnet, "
            "or route the acceptance through a judge on a leaf-class "
            "dispatch"
        )

    # (4) basis=="critic" -- legal if the critic (opus) is strictly
    # above agent (agent is scout/builder-class). A NUMERIC tier
    # comparison (not a name check) -- this already covers designer
    # correctly with no separate change: designer is also opus-tier,
    # tier("opus") > tier("opus") is false, the same rejection as for
    # agent=="critic" itself today.
    if basis == "critic":
        if TIER_ORDER["opus"] > agent_tier:
            return None
        return (
            f"role-vs-tier acceptance matrix: agent={agent!r} (tier "
            f"{agent_tier_name}) accepted with basis='critic', but the "
            "critic (opus) is not strictly above the executor's own tier "
            "-- this would legalize an acceptance this exact matrix row "
            "forbids, voiding the critic-gate guarantee for the "
            f"upper-mid tier -- the legal path for agent={agent!r} is by "
            "strictly above opus (by='fable'), or basis='queued-to-lead' "
            "at by∈{sonnet,opus}"
        )

    # (5) basis=="queued-to-lead" -- legal for the upper-mid-tier CLASS
    # (QUEUED_TO_LEAD_AGENTS = {critic, designer}, see its own comment
    # above) at by∈{sonnet,opus} (builder-class at a sonnet coordinator
    # does NOT pass -- legal only via basis='critic').
    if basis == "queued-to-lead":
        if agent in QUEUED_TO_LEAD_AGENTS and by in ("sonnet", "opus"):
            return None
        return (
            f"role-vs-tier acceptance matrix: agent={agent!r} accepted "
            f"by={by!r} with basis='queued-to-lead' -- this queue is not "
            f"legal for {agent!r}-class at a {by!r} coordinator; accepting "
            "sonnet-class (builder) work through the lead queue would let "
            "the critic gate on that executor's work go unchecked -- the "
            f"legal path here is basis='critic' (or judge on a leaf "
            f"implementation, if category is leaf-class AND "
            f"agent∈{{scout,builder}}); queued-to-lead is available only "
            f"for the class {sorted(QUEUED_TO_LEAD_AGENTS)}"
        )

    # (6) anything else -- generic role-vs-tier rejection.
    return (
        f"role-vs-tier acceptance matrix: agent={agent!r} accepted by={by!r} "
        "-- by is not strictly above the executor's tier, and no valid "
        "basis rescues it; an acceptance with no coordinator above the "
        "executor's tier and no critic justification bypasses the whole "
        "role-vs-tier acceptance matrix -- set basis='critic' (agent "
        "strictly below opus), or 'queued-to-lead' (agent∈{critic,"
        "designer}, by∈{sonnet,opus}), or judge on category∈{recon,"
        "implementation} with agent∈{scout,builder}"
    )


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
               "failure_class", "witness", "worker_ref", "ref", "by", "node", "id_band")
# the reasons journal_keys.node_of gives to a PRESENT `node` that is not a node (a field that is absent or null is not here)
NODE_BAD_REASONS = ("node_not_string", "node_not_form")


def _line_form_violations(obj: dict, tag: str) -> list[tuple[str, str]]:
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
            "it, leaf-class dispatches (recon/implementation) can't "
            "be told apart from the rest, and basis='judge' becomes "
            "unverifiable -- set category (rule 2)"
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
                "format (3+ digits) -- a non-standard id is invisible "
                "to the novelty/max+1 check and to the earlier-in-file "
                "existence lookup, inviting numbering collisions -- "
                "set an id shaped like t-NNN (rule 5)"
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

    if event == "delegated":
        worker_ref = obj.get("worker_ref")
        if not isinstance(worker_ref, str) or not worker_ref.strip():
            out.append(("worker_ref",
                f"{tag}: 'worker_ref' is required (non-empty string) "
                "for delegated -- without it, no handle exists by "
                "which a later session can find the worker or its "
                "result, and a launch that never actually happened "
                "goes undetected -- set worker_ref to the launch's "
                "handle (rule 12)"
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
            mv = _matrix_d0058_violation(event, agent, by, obj)
            if mv:
                out.append(("by", f"{tag}: {mv}"))

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
                        seed_lines: list[str] = (), drift: bool = True) -> list[str]:
    """`ts_anchor`: the ts the first new line is compared with for rule 10's monotonicity. The
    default is the last line of `head_lines`. The merge mode passes HEAD's OWN last ts (or None =
    no lower bound): the lines it validates are OUR side's tail, and the kept part's last line is
    usually the foreign clone's tail, whose clock may be ahead (t-525 F4).
    `seed_lines` (t-581): lines that precede the file in the same LOGICAL journal -- the history,
    for the file that continues it. They seed rule 9 (ids seen, max, the per-task state) and the
    ts anchor when `head_lines` is empty; line numbers in the messages stay those of the file.
    `drift=False` switches off the "later than now+10min" check (the CI run: the runner's clock
    is not the writer's)."""
    violations: list[str] = []
    state_lines = list(seed_lines) + list(head_lines)
    seen_task_ids = extract_task_ids(state_lines)
    # the next-id state (rule 9a/9e): HEAD and seed lines contribute their ids and their form-valid bands, never judged
    band_state = _jk.BandState()
    for state_line in state_lines:
        state_obj = _try_parse_obj(state_line)
        if state_obj is not None:
            band_state.add(state_obj)
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
        violations.extend(text for _field, text in _line_form_violations(obj, tag))

        # rule 9e (i): the PLACE of a form-valid band on this line, against everything issued or reserved before it.
        # A refused band does not enter the state, so it can never make this line's own id legal (position invariant).
        band, _band_reason = _jk.id_band_of(obj)
        band_kind = None
        if band is not None and not band_state.has_closed(band):     # a repeated declared band is a reference
            band_kind = band_state.check_band(band)
            if band_kind is None:
                band_state.add_band(band)
            else:
                violations.append(_band_place_text(tag, band, band_kind, band_state.top))

        valid_tid = isinstance(task_id, str) and TASK_ID_RE.match(task_id)
        if event == "delegated" and valid_tid:
            if task_id not in seen_task_ids:
                # (a) a brand-new task -- (ii) the file's own next id, or the next id of a closed band that is not
                # used up (rule 9e). The band of THIS line, when accepted above, is already in the state.
                # the band counts only when it is in the state (a refused band never entered it)
                own_band = band if band is not None and band_kind is None else None
                m_id = _jk.ID_NUM_RE.match(task_id)      # more than 9 digits: never issuable
                if m_id is None or not band_state.may_issue(int(m_id.group(1)), own_band):
                    violations.append(_novelty_text(tag, task_id, band_state, own_band))
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
        elif event in ("accepted", "rejected", "escalated", "defect_found") and valid_tid:
            if task_id not in seen_task_ids:
                violations.append(
                    f"{tag}: task_id {task_id!r} does not reference "
                    "anything existing earlier in the file -- an "
                    f"{event} with no matching delegated leaves this "
                    "event orphaned, and a reader can never find what "
                    f"task it belongs to -- point task_id at a real "
                    "earlier delegated, or issue the missing delegated "
                    "first"
                )

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

        # (iii) the line enters the state: its band only when it was not refused, then its id
        band_state.add(obj, band_ok=(band_kind is None))
        if valid_tid:
            seen_task_ids.add(task_id)

    return violations


def _band_place_text(tag: str, band, kind: str, top: int) -> str:
    """The refusal of a band that is well formed but placed wrong: BELOW, NEAR or JUMP (rule 9e)."""
    s = _jk.suggested_band(top)
    gap = band.lo - top
    if kind == "below":
        return (f"{tag}: id_band {band.raw} starts at or below t-{top:03d}, the highest id or band already in this "
                "journal -- a band may only start above everything issued or reserved, or it could hand out an id "
                f"twice; start it at t-{s:03d} (rule 9e)")
    if kind == "near":
        return (f"{tag}: id_band {band.raw} starts {gap} ids above t-{top:03d}; a closed band starts at least "
                f"{_jk.BAND_GAP_MIN} ids above, or the other writer's next id can land on its first id before this "
                f"line is written -- start it at t-{s:03d} (rule 9e)")
    return (f"{tag}: id_band {band.raw} starts {gap} ids above t-{top:03d}; at most {_jk.BAND_JUMP_MAX} -- start it "
            f"nearer, at t-{s:03d} (rule 9e)")


def _novelty_text(tag: str, task_id, state, own_band=None) -> str:
    """The refusal of a brand-new delegated whose id is neither the file's next id nor the next of the band the
    line carries (rules 9a, 9e): names every next id the writer may use, the door when the id lies inside a band
    the line does not carry, and a used-up band with the door."""
    main, _bands = state.issuable()
    s = _jk.suggested_band(state.top)
    text = f"{tag}: task_id novelty violated -- got {task_id}; the next new id is t-{main:03d} (this journal's sequence)"
    for band, nxt in _jk.free_bands(state)[-_jk.BAND_SHOW_MAX:]:
        text += f" or t-{nxt:03d} (band {band.label})"
    m_id = _jk.ID_NUM_RE.match(task_id) if isinstance(task_id, str) else None
    around = state.band_around(int(m_id.group(1))) if m_id else None
    if around is not None and (own_band is None or (own_band.lo, own_band.hi) != (around.lo, around.hi)):
        text += (f"; {task_id} lies in the id band {around.label} of another writer; a line issued from a band "
                 f'carries "id_band":"{around.label}"')
    used = _jk.used_up_bands(state)[-_jk.BAND_SHOW_MAX:]
    for band in used:
        text += f"; band {band.label} is used up"
    if used:
        text += f" -- open a new band at t-{s:03d}"
    return (text + " -- re-read the tail right before writing (python tools/journal_keys.py where prints every next "
            "id); a second writer of this file opens its own band: "
            f'id_band: "t-{s:03d}..t-{s + 49:03d}" on its first line (rules 9a, 9e)')


def decide(staged_text: str | None, head_text: str | None,
           now: datetime.datetime | None = None, *, seed_text: str | None = None,
           drift: bool = True) -> tuple[int, list[str]]:
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
    violations = validate_new_lines(new_lines, head_lines, now, seed_lines=split_lines(seed_text), drift=drift)
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


def feature_warnings(new_lines: list[str], head_lines: list[str], known=None) -> list[str]:
    """WARN texts (never violations) for NEW delegated/accepted/defect_found lines dated
    FEATURE_WARN_FROM or later that carry no `feature` field or a value not in the
    registry. `known` = the registry ids (None -> read plans/features.json). Lines that
    do not parse, have no parseable ts, or are older than FEATURE_WARN_FROM are skipped."""
    if known is None:
        known = load_feature_ids()
    warns: list[str] = []
    for obj, tag in _dated_new_objs(new_lines, head_lines, FEATURE_WARN_EVENTS, FEATURE_WARN_FROM):
        fv = obj.get("feature")
        if fv in (None, ""):
            warns.append(_warn_line(
                tag,
                f"no 'feature' field -- the event cannot be attributed to a feature in "
                f"the Forge metrics (tools/forge_metrics.py) -- add \"feature\":\"Fnn\" with an id "
                f"from {FEATURE_REGISTRY_REL}"))
        elif known is not None and fv not in known:
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
                         seed_text: str | None = None) -> tuple[int, list[str], list[str]]:
    """decide() plus the WARN list; the exit code is exactly decide()'s -- warnings never
    change it."""
    code, violations = decide(staged_text, head_text, now, seed_text=seed_text)
    staged_lines = split_lines(staged_text)
    head_lines = split_lines(head_text)
    ok, _msg = check_append_only(staged_lines, head_lines)
    new_lines = staged_lines[len(head_lines):]
    warnings = feature_warnings(new_lines, head_lines, known) + node_warnings(new_lines, head_lines) if ok else []
    return code, violations, warnings


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
        pairs = list(_line_form_violations(staged_obj, tag))
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
        num = int(tid[2:]) if _jk.ID_NUM_RE.match(tid) else None
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
    violations = validate_new_lines(tail_lines, kept_lines, now, ts_anchor=anchor, seed_lines=seed_lines)
    warnings = feature_warnings(tail_lines, kept_lines, known) + node_warnings(tail_lines, kept_lines)
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
        _code, vv, ww = decide_with_warnings(staged_text, head_text, now, seed_text=seed_text) if drift else (
            *decide(staged_text, head_text, now, seed_text=seed_text, drift=False), [])
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
            v = decide(head_text, base_text, now, drift=False)[1]
            fz = _frozen_history_violation(len(head_lines) - len(base_lines), frozen,
                                           door=f"your own {_jk.JOURNAL_DIR_REL}/<slug>.jsonl")
            if fz:
                v = v + [fz]
            results.append((p, 1 if v else 0, v, []))
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
