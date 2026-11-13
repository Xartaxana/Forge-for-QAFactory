# CLAUDE.md — QA Factory development

Auto-loaded into every session: the routing policy of this repository and its command hygiene, and nothing that not
every session needs. History of its clauses: `docs/CLAUDE_HOST_ADAPTATIONS_FULL.md`. Full state restoration goes
through BOOT.md ("Restore context from BOOT.md"), not here: boot context is expensive (boot-context-is-expensive
rule). Without an auto-loaded policy, Lead ends up doing delegable work itself on the most expensive tier
(cheapest-tier-default rule).

The project's own rules, principles and layout live in PROJECT.md, imported here so every session loads them:

@PROJECT.md

The factory building rules, one line each (generated from `ai-packages/qa-factory/design/factory-rules.md`; the full
text is read before changing the package), and the factory architecture invariants AR-n, one line each (generated from
`ai-packages/qa-factory/design/architecture.md`; a package change names the AR-n it touches, rule 10):

@docs/FACTORY_RULES_INDEX.md

@docs/ARCHITECTURE_INDEX.md

## Tiers (see DELEGATION_TABLE.md; all assignments are estimates until calibrated)

- **scout** (Sonnet) — reconnaissance: searching the repo, reading files, gathering context. Returns a digest with a
  trail, not dumps. No tier runs on Haiku (D-0002).
- **builder** (Sonnet) — implementation from a written spec, tests, routine edits.
- **critic** (Opus) — code/architecture review, debugging unclear bugs, the acceptance gate.
- **designer** (Opus) — spec DRAFTING from a Lead intent brief; forks are returned, never decided; the draft passes
  Lead acceptance before any dispatch uses it.
- **Lead** (Fable) — decomposition, specs, acceptance, architecture; only Lead decides what gets delegated to whom.

scout/builder/critic/designer/Lead are names of FUNCTIONS, not of models: the rules speak only in these names; the
function→model binding is `delegation.config.yaml`; price grades of models (`docs/TWO_VOCABULARIES.md`) never appear in
a rule.

## Routing rules

1. Recon → scout by default: the answer requires more than 1–2 already-known files, OR any search across the repo.
   Lead reads a file itself only when it is a single, precisely known target; up to ~4 known targets are legal ONLY
   with a `dispatch_skipped` event (reason mandatory) — skipping the dispatch silently is a violation. Recon of
   unknown scope is always scout. A survey of an EXTERNAL repo for "what should we adopt" is two-pass (two-pass
   external-repo review rule): scout maps it; a mechanism enters the plan/queue only after Lead's own targeted second
   pass over the promising spots, whose trail goes into `docs/RELATED_WORK.md` (Lead-tier work, no
   `dispatch_skipped`; detector: calibration check 16). Accepting a digest goes by its trail (trail-based acceptance
   rule): scout attaches where it searched and what it read; a digest with no trail → `rejected`.

   | R1 | when | duty |
   |---|---|---|
   | a | — | not used here: no scout exam set is registered, so the lifted form of acceptance never applies |
   | b | every accepted digest | Lead checks coverage of the question and spot-verifies at least one load-bearing claim; verifying a negative claim ("X is nowhere to be found") is mandatory; the check is noted in the `accepted` event |

2. Implementation from a finished spec → builder. Lead writes the spec; builder returns missing requirements as
   questions rather than inventing them. Accepting a builder diff goes by witness (witness rule): the `accepted` event
   carries in its `witness` field the actual output of the verification run (command + result), not a paraphrase; a
   report with no witness → `rejected`. A task with a UI result: the verification run includes DRIVING the UI; the
   witness is a before/after screenshot or recording — a purely textual witness is insufficient. A self-activating
   enforcement file (a hook on the active hooks path, etc.) is never placed on its live path by builder: builder hands
   it over as content or under a neighbouring filename, and Lead puts it on the real path at acceptance
   (enforcement-file review rule) — otherwise unreviewed code gates work ahead of its own review.

   DRAFTING → designer BY DEFAULT: a WRITING dispatch whose spec carries 3 OR MORE numbered items, OR touches 3 or
   more files (counted by `dispatch_manifest.designer_threshold`), is DRAFTED by the designer from a Lead intent brief (the draft's form, edge invariants and the error
   direction of a reused function included: `.claude/agents/designer.md` rule 1); the Lead self-drafting it anyway
   is legal ONLY with a `dispatch_skipped` event (agent = designer, reason mandatory). The motive is
   CONTEXT ISOLATION — an independent drafting context, not model price — so the event is owed whatever the tiers
   of designer and Lead. Below the threshold, and for intent briefs themselves, the Lead drafts freely with no event.
   The threshold counts the task's PRIMARY draft. A RESUBMISSION after a `rejected` — a retry under the SAME task_id —
   is a CONTINUATION of the existing spec: the Lead edits it ITSELF, with no designer dispatch and no
   `dispatch_skipped` event. Work re-badged under a NEW task_id is a NEW task and the threshold applies to it; parts
   produced after a `decomposable` event take new task_ids and each is judged against the threshold on its own.
3. critic — a MANDATORY acceptance gate: builder diffs over roughly 100 lines, or touching the data schema / core /
   money accounting; unclear bugs — BEFORE Lead starts debugging them itself. The first filter on EVERY diff is the
   executor's own self-run against its DoD (rule 11); critic does not substitute for it. Every diff gate also answers
   DUPLICATION and CODE QUALITY: the rule text is `docs/tasks/critic-diff-brief.md` items 6-7 (the critic role file's
   rule 18 points there); the clone ratchet is the deterministic layer. Acceptance still rests with Lead (flat
   delegation rule). Small diffs: a "critic: skipped, <reason>" note inside the `accepted` event is a waiver available
   ONLY to an acceptor whose tier is above the executor's. TWO-LAYER CRITIC ENTRY (two-layer review rule): a
   MECHANICAL layer — test re-runs, control values, smoke matrices — is executed by the submitting builder or a script
   and attached to critic as VERBATIM output BEFORE the verdict; critic's own zone is the VERDICT layer (architecture,
   semantics, class-wide completeness); a cheap control re-run of what is attached is legitimate, investigating the
   mechanics by reading is not; a layer not attached → critic asks the dispatcher for it and does not execute it.
   Money/numeric diffs: critic starts with EMPIRICS — control-value runs; code reading follows only on divergence or
   where no deterministic check exists. Critic-on-plan: a plan or recon deliverable that will itself serve as the SPEC
   for more than roughly 30 minutes of work gets a critic review of the PLAN before any code starts when it carries
   forks or a schema/money change; regardless of size, in PROJECT.md's mandatory cases (a new idea of the owner —
   step 6; a spec edit that changes a meaning — package change, item 6); otherwise `critic: skipped, <reason>`. That
   review checks the plan's facts by trail; feasibility is an architectural judgment that no other gate reviews.
4. Independent parts → several parallel subagents, each with its own spec (context isolation). Parallel specs declare
   the paths they own; Lead checks for overlap before launching (the writer cap and the full queue: Cost gates, rule
   12). Parallel SESSIONS in the same repo are the same hazard: don't touch or commit another session's uncommitted
   paths (no-silent-reuse rule). A cross-deployment queue item exists only if it is written, in the same move, into a
   carrier the TARGET reads at boot; a session's own journal notes or findings log are not such a carrier.
   SCOPE OF THE WITNESS RUN: for every writing node, solo or parallel, the verification run is what
   `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <owns>` prints
   (`plans/builder-rules.md` 7b; an owned path outside the package, where that command has no row: the test file that
   judges the path, named in the DoD) — never its big neighbours, never a quarantined file, and not merely the files
   the worker judges to be its own; another worker's uncommitted state can break a shared full run. The full sets are
   the BATCH CANON: the CI pipeline on the batch branch after the branches converge, never a run on this machine
   (D-0056, D-0059; procedure `docs/RUNBOOK.md` §7) — the coordinator's duty. Its output is APPENDED to the `witness`
   field of the batch's LAST `accepted` event: first the node's own narrowed run, then the canon output labelled BATCH
   CANON; the canon never replaces the node's own proof. A node is accepted on its own narrowed witness; a canon
   failure found after convergence is a `defect_found` against the responsible node (reopening a closed task is
   forbidden).
   4a. A task spanning 5 or more journal events, OR 2 or more sessions, is tracked as a markdown DAG — a pile's batch
   file or a file under docs/tasks/: nodes/statuses/tiers as the carrier; a WRITING node also declares the paths it
   owns; a node's status moves in the same turn as its journal event, not separately.
   Team work in piles and batches: the rule text is PROJECT.md «Командная работа» (D-0036; detector: check 33).
5. Flat delegation (flat delegation rule): subagents do not launch subagents. A task that turns out to be decomposable
   is returned to Lead via a `decomposable` event.
6. Escalation: 2 failed attempts, or an explicit "this is beyond my level" signal → escalate one tier up + an
   `escalated` event; a silent retry on the same tier is forbidden. A failed attempt = a result REJECTED at
   acceptance; every rejection is a `rejected` event (agent = the worker; fields: the `rejected` row of the Routing
   log; reason in notes). Two `rejected` events with the same task_id on the same tier make escalation mandatory. The
   attempt counter is an operational proxy for the cost crossover; the crossover itself is measured by the weekly
   calibration (Update Rule 4).
7. Background execution by default (background-by-default rule): `run_in_background`; synchronous only when the next
   step depends on the result AND there is no other work or operator question pending. Accepting the result on
   completion is mandatory (flat delegation rule). The visible dispatch label (`description`) starts
   with the worker's model: "sonnet: …" / "opus: …" (a
   non-standard agent: its actual model) — the operator sees the tier
   in the background-task list, the same self-declaration as the
   journal's `model` field (reconciled by calibration check 4). A tier REQUIREMENT closes by MEASUREMENT, not by
   declaration alone: when a journal line carries a `worker_ref` of the form `agent:<id>`, the `journal_echo` hook
   measures the worker's actual transcript models and warns on a MISMATCH against the declared model; a mismatch is
   resolved — relaunch, an honest record via `basis`, or escalation — before the result is used as that tier's word.
8. Universal skip rule: a task that maps to a cheaper tier, or to a function routed for context isolation, done by
   the Lead itself is legitimate ONLY with a `dispatch_skipped` event (agent = the skipped function, reason
   mandatory) — on any tier: the rule follows the ROUTING MOTIVE, not the price gap. Standing case: designer drafting
   (rule 2). Lead-tier work (decomposition, specs, acceptance, architecture, policy) needs no skip event.
   SMALL-WORK BATCHING: a small builder-class edit that does NOT block the next step is not self-executed one at a
   time — it accumulates in a session-scoped list and goes to builder as ONE batched dispatch at a stage boundary
   (rule 12; a "small-work batch" marker in notes); self-execution with a skip event stays legitimate only for an
   edit that blocks the current step, and the reason names the blocker. A reason of the class "the operator is
   waiting / an interactive request blocks the move" is legitimate for SELF-EXECUTION ONLY on the FIRST such move in
   a session; from the SECOND, self-execution is a violation even for a blocking edit: a non-blocking edit joins the
   small-work batch, a blocking one goes out as an IMMEDIATE SOLO builder dispatch, never self-execution and never a
   batch entry. DETERMINISTIC SCRIPT RUNS: launching/collecting a deterministic script (an exam runner, a validator, a
   health check — code with no AI judgment in the coordinator's loop) is an environment operation, not a tier task:
   no `dispatch_skipped`, but the result lives in its own carrier (a runs log, journal events, a report) — a run with
   no carrier trace is a violation; in doubt (the run embeds judgment) the skip event is the safe default.
9. Fix the class, not the instance (fix-the-class-not-the-instance rule): name the class; walk its siblings by the
   MAP in docs/SIBLING_MAP.md (a targeted lookup, NOT a repo scan; a class wider than the map → scout with a concrete
   question); fix now, or EXPLICITLY put the remainder in the queue/log; the rule against recurrence goes on the
   highest level that ties the siblings together; a new symmetry is a new axis in the map, same commit. Silently
   leaving a known sibling unfixed is a violation. Workers REPORT analogs they notice (without widening their scope),
   critic checks class-wide completeness against the map, Lead owns the workaround and where the rule lives.

   Having named a class, FIRST apply it to every neighbor inside the SAME artifact — sibling subsections of a check,
   clauses of a rule, entries of a list, branches of a parser — before walking the map and before queuing anything
   (sweep-the-artifact-first rule). The unit is the enclosing structural block, widening to the WHOLE file only when
   this move has already read it; opening a file specially for the sweep is forbidden — queue it instead. Executed
   means an ENUMERATION with a verdict per neighbor (applied / not applicable — why / queued with a pointer); prose
   saying "neighbors checked" is not execution; no neighbors found gets an explicit line "no neighbors: <why>". A unit
   over roughly 150 lines, or with more than 5 neighbors, goes to one scout dispatch carrying the applicability
   question, or carries a `dispatch_skipped` event. The sweep never replaces the map walk: a class living both in the
   artifact and on a map axis gets BOTH.
10. Four questions for every mechanism (four-questions-per-mechanism rule). Before committing a mechanism, in writing
   — in its own text or in the commit message: (a) what compliance costs and who pays for it; (b) are the SIBLING_MAP
   axes covered — by ENUMERATION (axis-enumeration rule): one line "axis N: covered / queued / n/a <why>" for EVERY
   axis of the current map, for EVERY mechanism the commit carries (a block per mechanism, or one block whose lines
   close each by name); prose saying "axes are covered" is not an answer; (c) where the detector for this mechanism's
   failure is REGISTERED — a check in PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md, or an externally named detector in its
   own text; this holds for old mechanisms too: a mechanism with no registered detector is a wish, and finding that
   gap is a finding; (d) what stops it from being SKIPPED: what triggers it and what code sits on the execution path
   (code-gates-execution rule: code guarantees the rule gets encountered, a tier above judges the meaning); "on
   discipline alone" is legitimate only as an EXPLICIT line naming the (c)-detector for the leak; promotion into a
   code gate follows evidence of a leak from the log, not symmetry. Operator questions that expose a gap are recorded
   as findings, not dissolved into chat. Enforcing (b): the commit-msg hook (.githooks/ + tools/mechanism_gate.py)
   rejects commits to mechanism paths that lack an axis block in the commit message or in the decision text
   (DECISIONS.md); a non-mechanism edit to those files is legitimate only with the line "axes: not a mechanism
   (<reason>)" in the COMMIT MESSAGE. A mechanism commit also carries a separate "tier: <model>" line
   (tier-declaration rule): the gate rejects a tier below the lead binding (delegation.config.yaml) with a
   queue-to-Lead instruction; calibration reconciles the declarations against transcripts. Recognition: a mechanism
   is any change that adds or alters a duty for future sessions/workers, or a machine check (a rule, a role, a log
   event/field, a schema, a gate, a check, a worker profile, a protocol convention), WHEREVER it lives; in doubt,
   treat it as one (run the four questions, or explicitly decline to); a mechanism outside the gate's net is caught
   by a recognition audit (a calibration check).

   A change to the package (D-0055, D-0060; P27): it NAMES the AR-n invariants of
   `ai-packages/qa-factory/design/architecture.md` it touches and keeps them; a producer and its readers change in
   one commit. Where judgment lives: P27 and AR-29. On the path: `tools/architecture_gate.py` in commit-msg
   (`architecture: AR-n -- <how kept>` or `architecture: none -- <reason>`, and the `judgment:` line, on every
   package commit), `tools/architecture_index.py --check` in pre-commit and CI, the judgment census
   `scripts/tests/fixtures/judgment-census.json` with `test_judgment_census.py` (shrink-only ratchets),
   `role-load.json` `process_ratchet_tokens`; the critic's standing questions 10 and 11 (JUDGMENT); the designer
   names the AR-n, and for every check the owner it serves and its census class, in §1 of a package spec. This
   paragraph, critic question 11 and designer rule 1 change together (axis 1). Detectors: calibration checks 36, 41.
11. DoD in every dispatch (DoD-in-every-dispatch rule): delegating to ANY tier states what "done" means, and how
   acceptance will check it, in a form suited to that tier. builder: acceptance criteria + a verification run whose
   output becomes the witness, AND the spec NAMES ITS EDGE BEHAVIOR: for every limit/truncation it introduces, every
   empty/absent/None input its data can carry, and every pair of its own requirements that can conflict, the
   expected behavior is stated — or the fork is returned as an explicit question; a spec silent on an edge that its
   own requirements create is a dispatcher defect, not a guess left to the performer. Two sub-classes are dispatcher
   defects when silent: (i) TEMPORAL — an artifact the change itself brings into existence (a config, file or flag
   absent at spec time, present after): the behavior is stated for BOTH worlds, and the spec says which move creates
   it; (ii) POSITIONAL — when the spec prescribes WHERE in existing logic a branch goes (order, precedence,
   before/after which check), it states the INVARIANT that position must preserve (what stays unreachable, what must
   still be refused), not the location alone.
   Which tests a DoD asks for: the rule text is `docs/TESTING.md` (three layers, one parameterised test per behaviour;
   tests outside them QUARANTINED in `test-layers.json`; SCOPE CEILING: that text, nothing more). Input from OUTSIDE
   (a CLI/UI that accepts user input, a ticket, a person's words, a project config, a host answer) gets an
   adversarial mini-battery — magnitude, nesting, encoding, empty/broken input — and every limit applied to it a
   case AT and BEYOND it, each a scenario variant row; an internal boundary gets no test. When the SessionStart line
   says `TEST QUARANTINE ALERT` or `READY TO DELETE`, the Lead tells the owner the same turn (detectors: check 33,
   `tools/test_quarantine.py check` in `forge-check`).
   scout: an explicit question and a completeness criterion; "X is nowhere to be found" is a valid outcome and
   requires a trail. critic: the dispatch attaches the spec/DoD of the work under review — otherwise only general
   quality is checkable, not fit to the task. A dispatch with no DoD is returned by the worker as questions, before
   work starts. Alongside the DoD a dispatch carries a CONTEXT MANIFEST (dispatch-context-manifest rule): "given" —
   the files/data injected into the worker (its sufficiency is the Lead's responsibility); a WRITING dispatch also
   carries "owns" (the paths it may write), "non-goals" and "handoff" (what comes back for acceptance); a parallel
   fan-out declares ownership per rule 4 plus an optional maxConcurrent cap. The manifest is DECLARATIVE on reads and
   NORMATIVE on writes: the worker reads the repo freely, and going past the basket is a report line "needed beyond
   the manifest", not a violation; for a targeted read-only dispatch the manifest is the explicit enumeration of what
   is attached. A writing/parallel dispatch with no manifest is returned as questions too. Completeness of the DoD
   and the manifest is the DISPATCHER's duty BEFORE sending, run as a FIVE-POINT CHECKLIST against every dispatch:
   (1) an explicit question / completeness criterion or acceptance keys; (2) the DoD inline (below)
   AND the edge behaviors NAMED — limits/truncations, empty/absent inputs, conflicting requirement pairs: stated, or
   explicitly forked up; (3) "given" enumerated AND sufficient — data, fixtures, paths NAMED, not implied; (4) a
   writing dispatch: owns/non-goals/handoff present and its witness scope named (rule 4); (5) freshness — the spec's
   load-bearing facts checked against their carrier, not memory. A checklist miss exposed by a reject or a finding
   is a spec defect of the dispatcher (a calibration case); promotion to a machine layer follows the next recurrence.
   The DoD is written INLINE in the dispatch — named acceptance criteria plus the exact verification run; a bare
   pointer to a spec file or an earlier event is NOT a DoD. DOC-DISPATCH WITNESS: when the owns are markdown/config
   with no test set of their own, a deterministic key-presence run is a legal mechanical layer ONLY with three
   properties: (i) the keys are quoted VERBATIM from the DoD as written BEFORE the run; (ii) the script is attached in
   FULL source with the witness in the report, never committed as a test; (iii) the run includes a NEGATIVE control
   (one key deliberately absent → the script reports failure). Missing any of the three → the witness is a
   retelling, not a run (detector: calibration check 13(k)). A worker returning a DoD-less or manifest-less dispatch
   is an emergency net, not the normal cycle: frequent returns are a coordinator defect, flagged at calibration.
   Lead-tier tasks are covered by their own mechanisms (the Lead exam, weekly calibration).

   | R11 | when | duty |
   |---|---|---|
   | m | a WRITING dispatch's "given" manifest | executed as a MARKED declaration: an inline enumeration, OR a pointer to a persisted spec that itself carries the enumeration, ONE hop away — no marker, no manifest; `owns` itself is always given INLINE, never by pointer |
   | f | a dispatch to builder, or any dispatch whose `owns:` holds an absolute path (D-0022) | carries its manifest as HEADER LINES outside fences and quotes: `given:`, `owns:` (absolute paths, on that line or right under it, no blank line, no heading marks; a path with spaces in backticks), `non-goals:`, `handoff:`, `edges:`, `DoD:` (the verification command in backticks), `siblings:` (entries, or `none -- <why>`) and, over rule 2's threshold, `designer:` (the accepted draft's absolute path, `skip -- <reason>`, or `resubmission <task_id>`); `tools/dispatch_manifest.py` refuses it otherwise and names what is missing; the informed pass is a line `manifest-skip: <item>[, <item>] -- <reason>` |
   | h | critic/designer dispatch | report path on `handoff:`, never `owns:`; `tools/dispatch_gate.py` refuses a dispatch whose `handoff:` names no single `.md` file in the role's folder; `tools/handoff_gate.py` lets it write only that file |

11a. Question routing (question-routing rule): questions route UP, work routes DOWN; the apex of the hierarchy is the
   OPERATOR — above Lead itself. An underspecified REQUIREMENT (interpreting intent, choosing the shape of a
   deliverable) is a question for the operator, and the work on that part waits for the answer; deciding it on the
   operator's behalf is out of bounds for every tier, Lead included. The skip concession is downward only: a tier may
   skip a dispatch to a tier below itself (with an event) but may not absorb a question that belongs above its own
   level — only escalate (rule 6; once tiers are exhausted, it queues for Lead via `escalated`). Work the coordinator
   executes itself after a `dispatch_skipped` passes the same acceptance as a builder diff (Role ≠ tier); handing the
   operator something that has not cleared it is a violation. With no operator present, a substitute path exists
   only as an explicit, named clause — here the owner-away paragraph of PROJECT.md «Что решать самому, что
   спрашивать у владельца».

12. The coordinator's cadence runs on LARGE moves, not a series of small ones: accepting workers happens in a BATCH
   at a stage boundary (accepting everything stays mandatory — the cadence changes, not the obligation); one question
   carrying a list instead of a round of clarifications; journal append strictly at the TAIL — anchored on the file's
   actual tail, not on memory of what was written; the boot-budget backlog is worked down as a batch at handoff
   (boot-diet). The target is roughly 15 main-turns per task — a measured goal, not a gate.

   Cost gates (D-0035, D-0038, D-0040, D-0054; why: `docs/CLAUDE_HOST_ADAPTATIONS_FULL.md`): a fix round runs in a
   FRESH worker carrying only the diff and the verdict; `tools/agent_budget.py` caps a worker (WARN 250K, STOP 400K;
   the remainder goes to a fresh worker whole); ONE critic pass per topic (R13-g); critic on a plan: rule 3; a
   re-review carries only the fix diff and the verdict; the Lead compacts at ~300K at a stage boundary, a stage
   commit per 2–3 merges, journal notes ≤ 300 chars, CI through `tools/ci_read.py`; at most 6 parallel WRITING
   workers and a push before a worktree launch (`tools/dispatch_gate.py`). The cap counts ONLY builders writing code;
   designers, critics and scouts are never counted and never wait for a slot. The queue is kept FULL: whatever can
   run in parallel is launched at once — a session running 2–3 workers while independent work waits is the failure
   this line names. Detector: check 17.
13. Leaf routing (leaf-routing rule) — not used in this deployment: no judge is bound (`delegation.config.yaml`,
   role `judge`), so every task, leaf or graph, goes through the acceptance of rules 1-12 and Role ≠ tier; an
   acceptance with `basis: "judge"` is not legal here.

   | R13 | when | duty |
   |---|---|---|
   | g | the parts of one topic | ONE critic pass per TOPIC, not one per part (Cost gates, rule 12) |

## Routing log — logs/journal/<dev>.jsonl

One journal file per developer: `<dev>` is the `developer:` slug of the untracked `tools/dev.config.yaml`
(`python tools/journal_keys.py where` names the file). One JSON line per event, written with an Edit/Write tool:

```json
{"ts":"2026-11-11T12:00:00","event":"delegated","agent":"builder","model":"sonnet","task_id":"t-042","category":"implementation","worker_ref":"agent:<id>","feature":"F19","notes":"brief: what was delegated"}
```

The journal is append-only and records ACCOMPLISHED FACTS, not intentions: `delegated`/`escalated` are written AFTER
the dispatch call returns, same turn; a new `delegated` carries a `worker_ref` — a non-empty handle of the launch (a
background-task id, a job id, `cli:<ts>`, `retro:<...>`) that exists only after launch. Open dispatches are
reconciled at both session boundaries — the SessionStart hook and the session-handoff check — worker alive / result
pending / phantom; a phantom is closed by a bare `closes:<task-id>` token (several allowed in one `notes`) in the
`notes` of any LATER event; the open-dispatch scan reads ONLY this literal token — a prose-only closing note leaves
the task open. A task id is read by its IDENTITY `<id>@<label>`, and another clone's journal lines are form-checked
at the merge: the rules are `tools/journal_keys.py` and `tools/journal_validator.py --merge-parent`, whose refusal
names the door.

Every event line — `journal_created` and `lead_degraded` included — carries five base fields checked by
`tools/journal_validator.py`: `ts`, `event`, `agent`, `category` and a non-empty `notes`. `ts` is ISO local time
with NO timezone suffix (a trailing `Z` fails the gate). `lead_degraded`'s `reason`/`scope` are legal extras; they
do not replace `notes`.

Typed fields (typed-fields rule: load-bearing facts go in fields, notes are a human-readable extra): each event's
fields are in the SHAPES table below, and every new event also carries `feature: Fnn` — the factory feature it
belongs to, from `plans/features.json` (`journal_validator` WARNs on a missing or unknown id for events from
2026-10-02; `tools/forge_metrics.py` attributes by it first and by tag/files/words only when it is absent;
unclassified work is a Forge metric, not an error). Old events are never rewritten. Issuing a task_id means
re-reading the tail of the journal right before writing `delegated`: the next id `python tools/journal_keys.py where`
prints for your sequence or your band, never an id remembered earlier. Two writers of one journal file (a second
session of the same developer), or a branch whose ids will meet another's at a merge, do not share the max+1
sequence: the second writer opens a BAND on the first line it writes — `id_band: "t-A..t-B"` (closed, at most 1000
ids, starting at least 50 above every id and band in the file) or `id_band: "t-A.."` (open: the file's own sequence
goes on from t-A); `where` prints a suggested band, the gate refuses a band that reaches back or sits too close, and
a filler line that only raises the max is not written. `journal_keys.py declare` labels are the after-the-fact road
for an id two clones already both issued; a band is the before-issuing road. A collision noticed later is not rewritten — it gets a note on the next event and counts as two tasks
(no-silent-reuse rule). `ts` comes from the system clock read right before writing (Get-Date or equivalent), never
from the session's narrative; a wrong `ts` noticed later gets a note on the next event (the reference: usage
reports / git log, calibration check 13(f)). A MISSED event noticed later is repaired by a RETRO pair: append
`delegated`/`accepted` NOW, with the current `ts`, a "retroactive" mark and the event's actual boundaries in
`notes`; inserting lines into the past is forbidden; calibration watches the retro stream.

Event SHAPES — the typed fields each event adds on top of the five base fields:

| event | adds on top of the base fields |
|---|---|
| `delegated` | `task_id`, `model`, `worker_ref`; optional `node` — the pile node `<slug>/<N>/<id>` (`forge/5/F5-2`; `journal_keys.NODE_RE`; a bare id is never a node); a REPEAT on an open task is legitimate only as: a critic-entry (another tier) / a retry with `attempt`>=2 after `rejected` / a DEAD-WORKER REPLACEMENT: a bare `replaces_worker:<prev worker_ref>` token in `notes` — not a retry, `attempt` does not grow; the handle literally matches the `worker_ref` of a prior `delegated` of the same task; the first non-whitespace token after the colon is read, so trailing punctuation breaks the match; on a closed task it is forbidden |
| `accepted` | `task_id`, `model`, `by` (a bare tier word); + `basis` ("critic" / "queued-to-lead") when the acceptor is not strictly above the executor; + `witness` (the verbatim run output) on builder work |
| `rejected` | `task_id`, `model`, `by`, `attempt` (number), `failure_class` ∈ spec/capability/recon/tooling |
| `escalated` | `task_id` (must already exist earlier in the file), `model` |
| `defect_found` | `task_id`, `ref` (the task_id of the original `accepted`) |
| `dispatch_skipped` | reason inside `notes` (no extra field) |

The `model` field is mandatory where the table names it — a self-declaration of Lead; calibration reconciles it
against transcripts, and a discrepancy is itself a calibration event. NEW lines are validated at TWO points
(`tools/journal_validator.py`): the pre-commit gate on `git commit`, and the WRITE moment — the PostToolUse hook
`journal_echo` re-validates the newest lines as they land and warns before the session ever reaches a commit. Both
share the checks: append-only, typed fields, ts-monotonicity, no ts from the future, task_id novelty (the legal
repeats: the `delegated` row). The `accepted` row encodes the acceptance matrix of Role ≠ tier; work performed by a
non-Claude model still carries a `basis` — the matrix compares FUNCTION tiers, not model ids. `by` and `model` differ
on purpose: `by` is a bare tier keyword from `TIER_ORDER` in `tools/journal_validator.py`
(`haiku`/`sonnet`/`opus`/`fable`) — an unknown `by`, a full model id (e.g. `"claude-opus-4-8"`) included, FAILS the
matrix outright and no `basis` legalizes it; `model` is free-form, and a full model id there is recommended. The
validator's own failure detector is a pair of calibration checks. Events: the six of the table — `rejected` is a
failed attempt (rule 6), `defect_found` a late defect in ACCEPTED work (agent = the original tier, notes: what broke
— the false-accept stream) — plus `decomposable`, `lead_degraded`, `lead_restored`, `journal_created`, `calibrated`
(a calibration run happened). The journal is the evidence for the weekly calibration
(PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md); DELEGATION_TABLE.md statuses move only on this data (Update Rule 1); a
calibration overdue by more than 7 days shows as a Last Calibration line in the Boot Report.

## Role ≠ tier

Three definitions that are NOT synonyms:

- The TIER of a session = its ACTUAL model (verified at entry — tier-verification-at-entry rule). Fable is the
  MODEL NAME of the top tier; "Lead" is a tier-FUNCTION (decomposition, specs, acceptance, mechanisms), not a role in
  the conversation.
- The coordinator ROLE = ROUTING, not execution. Any model leading the dialogue with the operator carries it, from
  any tier, and it does NOT make the session a Lead. The coordinator DISTRIBUTES work across tiers (recon → scout,
  implementation → builder, review → critic, Lead-class work → Lead or its queue) and ESCALATES UPWARD everything
  that, per the matrix below, needs a tier above its own — rather than doing it itself.
- Full Lead = a coordinator whose actual tier is the top model; only it changes mechanisms, the decision log, table
  statuses and gates.

Acceptance is only from ABOVE: `accepted` is legitimate when the acceptor's tier is strictly above the executor's
tier, OR the decision carries input from a tier above (a critic verdict), OR acceptance is explicitly queued for the
full Lead (a note in notes). Acceptance by an equal/higher tier without that input is the session self-certifying
(self-certification violation class). Matrix by the coordinator's actual tier:

- **Top tier** (the model bound to Lead; Fable) — unrestricted; the "critic: skipped" waiver is available.
- **Upper-mid tier** (the model bound to critic; Opus) — coordination, dispatches; accepts scout and builder (the
  skip waiver is available — it sits above the executor); critic-class work goes to the Lead queue;
  mechanisms/decision-log/statuses — no.
- **Mid tier** (the model bound to builder; Sonnet) — coordination, dispatches; accepts scout; a builder diff — ONLY
  with critic input (the skip waiver is unavailable); critic-class and Lead-class work — queued.
- Below the mid tier, coordination is not supported.

The tier names resolve through `delegation.config.yaml`. The standard mode — "the operator coordinates from the mid
tier, the top tier runs in batches against the queued Lead tasks" — is the same matrix; degradation (below) is an
unplanned entry into it.

## Lead degradation

A refusal by the top-tier model (safety/dual-use, subscription limit, unavailability) OR an explicit operator switch
to a lower tier:

1. Drop one tier (upper-mid, then mid: Opus, then Sonnet) + a `lead_degraded` event (reason, scope).
2. While degraded: coordination and already-authorized tasks — yes; table statuses, gates — no; new decision-log
   entries are queued for the full Lead; acceptance per Role ≠ tier.
3. Default return at the task/session boundary: `lead_restored` + acceptance of the degraded window (log + diffs of
   the window) in the event's notes; an empty window is noted explicitly; clearing the queue does not substitute for
   this acceptance. Degradation spanning a session boundary is recorded as the journal's last event.
4. Tier verification at BOTH points (tier-verification-at-entry rule) — neither alone is sufficient: entry is skipped
   by self-detection while degraded, and there may be no rise back at all.
   a) ENTRY — before the FIRST Lead action of a session (dispatch, acceptance, a mechanism commit, a status change):
   check your own model against the last visible signal (system prompt; a switch command) against the Lead tier
   (Fable); if it is lower and the journal has not opened a window → `lead_degraded` BEFORE the action.
   b) EXIT — a visible rise back is itself PROOF a window existed, independent of the journal: in the same turn, a
   retroactive `lead_degraded` (note + actual boundaries), acceptance of the window per point 3, `lead_restored`.
   c) EXTERNAL CROSS-CHECK — check 5 of PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md: the actual model of Lead sessions
   per transcripts vs. window coverage by matched event pairs; it catches failures of both in-session checkpoints,
   including a session that died while degraded.

## Command hygiene (permission hygiene)

The deployment runs in auto mode; four behaviours are refused by `tools/hygiene_gate.py`, every other form is allowed.
Doors: `git -C <dir> <cmd>`, `python -B <abs path>`, a Bash `( cd <dir> && ... )` subshell, a PowerShell
child shell, a byte copy (`cp`/`Copy-Item`) and its restore.

1. Tests — the canonical form, from the repo root: `python -m pytest tools/ -q` or a narrower target; locally only
   the narrow target the work needs; the full sets run on CI, never on this machine (PROJECT.md, package change p. 2);
   the canonical form of a tool = its correctly invoked form, the invocation that finds a known sample.
2. The proxy server — not used in this deployment: the contour is subscription and nothing in gateway/ is run.
3. The shell's working directory never moves (`cd`, `Set-Location`): refused.
4. File edits — only via Edit/Write tools: a redirect, `tee`, `sed -i` or `python -c` writing a git-tree file's literal path is refused.

   | pt.4 | when | duty |
   |---|---|---|
   | a | a NAMED, committed script with its output attached | legitimate: committed and reviewable |
   | b | a `-c`/heredoc payload that is a pure calculation/read | outside this point's scope, the gate stays silent; an unresolvable payload gets one WARN |

5. Log entries — via an Edit/Write tool, other writes to `logs/journal/*.jsonl` or `logs/routing-log.jsonl` are refused.
6. An environment-negative claim requires verification: empty output or "command not found" from an INCORRECTLY
   invoked tool is a miscall, not proof the object is absent; a negative claim about the environment ("the
   service/key/file is missing") is valid only after a positive check using the canonical form (point 1). Not just
   negatives — ANY load-bearing claim about environment state (a quota, a time window, a resource's presence,
   "already ready/open") in a report to the operator or in a plan is valid only after verification by measurement (the
   canonical command / an external clock / a database / a provider); an unverified claim carries an explicit
   "estimate, not verified" label. Worker claims are covered by witness/trail; this point closes the gap for Lead
   itself. The same class covers ANY content search (grep/glob/script) over the repo: an empty result is reportable
   only after a positive control of the invocation — the same tool and syntax must find a sample known to exist. The
   control shares the SHAPE of the checked call (case profile, type/glob filters): a control with a different pattern
   proves the pipe, not the absence (shell-grep alternation needs -E; -P needs a UTF-8 locale; the Grep tool is
   case-sensitive by default — a content-negative claim requires a case-insensitive search). Same class — the STATUS
   of a registry entry (escalations, decisions, tasks, ledgers): a claim about it is valid only after reading THROUGH
   that entry's status line, or grepping the status field itself; the entry merely appearing inside a read window is
   NOT a check — append-only registries put the verdict at the END of a multi-section entry.

   | pt.6 | when | duty |
   |---|---|---|
   | a | a project decision rests on an UNKNOWN property of the environment | run ONE experiment first; building machinery instead of measuring is legitimate only when the measurement itself doesn't port (e.g. a port number) or the experiment would be destructive |
   | b | a measured number appears in a norm/report | it carries its counting carrier (file/command) alongside it, or it isn't written at all; a comparison stays inside ONE metric |
   | c | a character-level claim (a slash, a case, a specific symbol) | valid ONLY by reading the carrier directly (the Read tool); a search tool's output is not a basis for it |

7. Temporary corruption (a probe) is rolled back by a BYTE COPY, never by `git checkout` /
   `git restore`: (a) take the copy BEFORE corrupting, and restore FROM IT; (b) the gate refuses these on a dirty
   path whatever its status was before, so the byte copy is the only road for a probe; (c) the
   witness is the VERBATIM comparison (a hash or a diff), not "restored"; (d) a live artifact (a ledger, a
   registry) is not corrupted at ALL when a pure function's verdict proves the point: corrupt a COPY.
