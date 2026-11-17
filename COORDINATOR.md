# COORDINATOR.md — QA Factory development

Read by the coordinator at start and after compaction (SessionStart line `COORDINATOR RULES:`); workers do not read it at boot — a role reads only the section its role file names

The coordinator's routing policy of this repository (the worker block — the dispatch form, command hygiene, worker
duties, Язык — is `CLAUDE.md`, auto-loaded), and nothing that not every session needs. History of its clauses:
`docs/CLAUDE_HOST_ADAPTATIONS_FULL.md`. Full state restoration goes through BOOT.md ("Restore context from BOOT.md"), not
here: boot context is expensive (boot-context-is-expensive rule). Without this policy in context (the `COORDINATOR RULES:`
line), Lead ends up doing delegable work itself on a tier above the work's (cheapest-tier-default rule).

The project's own rules, principles and layout live in PROJECT.md, read with this file (the `COORDINATOR RULES:` line).

The factory building rules, one line each (generated from `ai-packages/qa-factory/design/factory-rules.md`; the full
text is read before changing the package), and the factory architecture invariants AR-n, one line each (generated from
`ai-packages/qa-factory/design/architecture.md`; a package change names the AR-n it touches, rule 10).

## Contents — topic → where to read

| Topic | Where |
|---|---|
| Tiers | COORDINATOR.md § Tiers |
| Recon → scout; builder; drafting | COORDINATOR.md § 1 + COORDINATOR.md § 2 + COORDINATOR.md § Rule 2 · drafting → designer |
| Dispatch form: DoD, edges, manifest | CLAUDE.md § 11 |
| Witness; acceptance by witness | COORDINATOR.md § 2 |
| What a builder may run | docs/TESTING.md § Что запускать по своей правке |
| Batch canon | COORDINATOR.md § Rule 4 · witness scope and the BATCH CANON + docs/RUNBOOK.md § 7. CI на GitHub и BATCH CANON |
| Which tests are written | docs/TESTING.md |
| Critic gate | COORDINATOR.md § 3 |
| Critic review content | .claude/agents/critic.md § 21-24 |
| Journal | COORDINATOR.md § Routing log |
| Merge and CI reading | docs/RUNBOOK.md § 7. CI на GitHub и BATCH CANON + PROJECT.md § Командная работа |
| Six writers, queue, merge waves | PROJECT.md § Командная работа |
| Cost gates | COORDINATOR.md § Rule 12 · Cost gates |
| Session hygiene | CLAUDE.md § Command hygiene + PROJECT.md § Сессия форджа |
| Command hygiene | CLAUDE.md § Command hygiene |
| Fix the class | COORDINATOR.md § 9 |
| Mechanisms | COORDINATOR.md § 10 |
| Piles and batches | PROJECT.md § Командная работа + docs/TEAMWORK.md |
| «Бэклог»; findings | PROJECT.md § Бэклог и находки |
| Owner's principles | docs/OWNER_PRINCIPLES.md |
| Package change acceptance | PROJECT.md § Как принимается изменение пакета |
| A new idea of the owner | PROJECT.md § Как разрабатывается новая идея владельца |
| Release | docs/RUNBOOK.md § 4.1. Шаги релиза |
| Language | CLAUDE.md § Язык |
| Decide vs ask; owner away | PROJECT.md § Что решать самому, что спрашивать у владельца + COORDINATOR.md § 11a |
| Links in answers | PROJECT.md § Ссылки на файлы в ответах |
| Hand-back form per role | .claude/agents/<role>.md |
| Readers of every touched file | .claude/agents/designer.md § 7 |
| Boot diet | .claude/skills/boot-diet/SKILL.md |
| How rule text for agents is written | .claude/skills/boot-diet/SKILL.md § Как пишутся правила для агентов |
| Session start/end | PROCESS/SESSION_PROTOCOL.md |
| Degradation; Role ≠ tier | COORDINATOR.md § Role ≠ tier + COORDINATOR.md § Lead degradation |
| Dispatcher duties about workers' runs | PROJECT.md § Как принимается изменение пакета + PROJECT.md § Командная работа |

## Tiers (see DELEGATION_TABLE.md; all assignments are estimates until calibrated)

- **scout** (Sonnet) — reconnaissance: searching the repo, reading files, gathering context. Returns a digest with a
  trail, not dumps. No tier runs on Haiku (D-0002).
- **builder** (Sonnet) — implementation from a written spec, tests, routine edits.
- **critic** (Opus) — code/architecture review, debugging unclear bugs, the acceptance gate.
- **designer** (Opus) — spec DRAFTING from a Lead intent brief; forks are returned, never decided; the draft passes
  Lead acceptance before any dispatch uses it.
- **Lead** (Opus) — decomposition, specs, acceptance, mechanism commits after the critic; only Lead decides what gets
  delegated to whom.
- **architect** (Fable) — ABOVE Lead: the owner's new ideas (PROJECT.md, steps 1–4), process questions the Lead
  escalates, the weekly calibration with its review of mechanism commits, its own `DECISIONS.md` lines. Summoned only
  by the owner switching the session model — never a subagent, never routed to automatically (D-0067); its start
  checklist is `PROCESS/ARCHITECT_START.md`.

scout/builder/critic/designer/Lead/architect are names of FUNCTIONS, not of models: the rules speak only in these names; the
function→model binding is `delegation.config.yaml` (one reader: `tools/tier_ladder.py`); price grades of models (`docs/TWO_VOCABULARIES.md`) never appear in
a rule.

## Routing rules

### Rule 1 · recon → scout

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

### Rule 2 · implementation → builder; acceptance by witness

2. Implementation from a finished spec → builder. Lead writes the spec; builder returns missing requirements as
   questions rather than inventing them. Accepting a builder diff goes by witness (witness rule): the `accepted` event
   carries in its `witness` field the actual output of the verification run (command + result), not a paraphrase; a
   report with no witness → `rejected`. A task with a UI result: the verification run includes DRIVING the UI; the
   witness is a before/after screenshot or recording — a purely textual witness is insufficient
   (enforcement-file review rule: CLAUDE.md § Worker duties).

### Rule 2 · drafting → designer

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

   Before a designer dispatch the Lead MEASURES the brief's load-bearing facts by code (the owner's word 17.11.2026).
   A load-bearing fact is any claim about the CURRENT repo or data that a requirement, an edge or a reader list rests
   on: a file, function, constant, field, CLI flag or hook that exists, and its shape or value; a count (readers,
   hits, sizes, lines); a test pin or anchor text; a data premise (PROJECT.md p.6(а)). Each fact goes into the
   dispatch as a `facts:` header block, one line each: `<claim> | <command> | <verbatim result, at most 200 chars>`.
   When the brief rests on none, the block is `facts: none -- <why>`. Opinions, intent and the owner's words are not
   facts: they go in the brief.

### Rule 3 · the critic gate

3. critic — a MANDATORY acceptance gate: builder diffs over roughly 100 lines, or touching the data schema / core /
   money accounting; unclear bugs — BEFORE Lead starts debugging them itself. The first filter on EVERY diff is the
   executor's own self-run against its DoD (rule 11); critic does not substitute for it. Every diff gate also answers
   DUPLICATION and CODE QUALITY: the rule text is `.claude/agents/critic.md` rule 22, Q6-Q7 (its rule 18 points there); the clone ratchet is the deterministic layer. Acceptance still rests with Lead (flat
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

### Rule 4 · parallel parts

4. Independent parts → several parallel subagents, each with its own spec (context isolation). Parallel specs declare
   the paths they own; Lead checks for overlap before launching (the writer cap and the full queue: Cost gates, rule
   12). Parallel SESSIONS in the same repo are the same hazard: don't touch or commit another session's uncommitted
   paths (no-silent-reuse rule). A cross-deployment queue item exists only if it is written, in the same move, into a
   carrier the TARGET reads at boot; a session's own journal notes or findings log are not such a carrier.

### Rule 4 · witness scope and the BATCH CANON

   SCOPE OF THE WITNESS RUN: for every writing node, solo or parallel, the verification run is what
   `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <owns>` prints
   (`docs/TESTING.md` «Что запускать по своей правке»; an owned path outside the package, where that command has no row: the test file that
   judges the path, named in the DoD) — never its big neighbours, never a quarantined file, and not merely the files
   the worker judges to be its own; another worker's uncommitted state can break a shared full run. The full sets are
   the BATCH CANON: the CI pipeline on the batch branch after the branches converge, never a run on this machine
   (D-0056, D-0059; procedure `docs/RUNBOOK.md` §7) — the coordinator's duty. Its output is APPENDED to the `witness`
   field of the batch's LAST `accepted` event: first the node's own narrowed run, then the canon output labelled BATCH
   CANON; the canon never replaces the node's own proof. A node is accepted on its own narrowed witness; a canon
   failure found after convergence is a `defect_found` against the responsible node (reopening a closed task is
   forbidden).

### Rule 4a · a task DAG; team work

   4a. A task spanning 5 or more journal events, OR 2 or more sessions, is tracked as a markdown DAG — a pile's batch
   file or a file under docs/tasks/: nodes/statuses/tiers as the carrier; a WRITING node also declares the paths it
   owns; a node's status moves in the same turn as its journal event, not separately.
   Team work in piles and batches: the rule text is PROJECT.md «Командная работа» (D-0036; detector: check 33).

### Rule 5 · flat delegation

5. Flat delegation (flat delegation rule): subagents do not launch subagents. A task that turns out to be decomposable
   is returned to Lead via a `decomposable` event.

### Rule 6 · escalation

6. Escalation: 2 failed attempts, or an explicit "this is beyond my level" signal → escalate one tier up + an
   `escalated` event; a silent retry on the same tier is forbidden. A failed attempt = a result REJECTED at
   acceptance; every rejection is a `rejected` event (agent = the worker; fields: the `rejected` row of the Routing
   log; reason in notes). Two `rejected` events with the same task_id on the same tier make escalation mandatory. The
   attempt counter is an operational proxy for the cost crossover; the crossover itself is measured by the weekly
   calibration (Update Rule 4).
   ABOVE the critic's model (Opus, which is also the Lead's) «one tier up» is the architect, which is never a subagent: two `rejected` on critic- or
   designer-class work → an item in `docs/tasks/architect-queue.md` + `escalated` with `agent: architect` (`model` =
   the architect binding); the Lead tells the owner «лучше позвать Архитектора: <вопрос одной строкой>», that work
   waits, unrelated work continues. The same road carries every Architect-class question: a new idea's
   architecture, a process trade-off, a rule conflict or a critic verdict the Lead cannot settle. STAND-IN (the
   owner's word 17.11.2026): a model ranked above a function's binding may stand in for that function while the
   bound model is unavailable; the stand-in dispatch names the outage in its notes.

### Rule 7 · background by default

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

### Rule 8 · the skip rule; small-work batching

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

### Rule 9 · fix the class

9. Fix the class, not the instance (fix-the-class-not-the-instance rule): name the class; walk its siblings by the
   MAP in docs/SIBLING_MAP.md (a targeted lookup, NOT a repo scan; a class wider than the map → scout with a concrete
   question); fix now, in the same round; a sibling leaves the round only when it lies in ANOTHER pile's zone or waits for the owner's word (say which), and only as a node with an executor or a confirmed transfer in the forms of `docs/TEAMWORK.md` § 9 — the rare case, never a way to put off a rule fix while rules are being fixed (the owner's word 17.11.2026); the rule against recurrence goes on the
   highest level that ties the siblings together; a new symmetry is a new axis in the map, same commit. Silently
   leaving a known sibling unfixed is a violation. Workers REPORT analogs they notice (without widening their scope),
   critic checks class-wide completeness against the map, Lead owns the workaround and where the rule lives.

   Having named a class, FIRST apply it to every neighbor inside the SAME artifact — sibling subsections of a check,
   clauses of a rule, entries of a list, branches of a parser — before walking the map and before moving anything out of the round
   (sweep-the-artifact-first rule). The unit is the enclosing structural block, widening to the WHOLE file only when
   this move has already read it; opening a file specially for the sweep is forbidden — move it to another pile's node instead (the rare case). Executed
   means an ENUMERATION with a verdict per neighbor (applied / not applicable — why / moved to another pile's node, with its id); prose
   saying "neighbors checked" is not execution; no neighbors found gets an explicit line "no neighbors: <why>". A unit
   over roughly 150 lines, or with more than 5 neighbors, goes to one scout dispatch carrying the applicability
   question, or carries a `dispatch_skipped` event. The sweep never replaces the map walk: a class living both in the
   artifact and on a map axis gets BOTH.

### Rule 10 · four questions per mechanism

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

### Rule 10 · a change to the package

   A change to the package (D-0055, D-0060; P27): it NAMES the AR-n invariants of
   `ai-packages/qa-factory/design/architecture.md` it touches and keeps them; a producer and its readers change in
   one commit. Where judgment lives: P27 and AR-29. On the path: `tools/architecture_gate.py` in commit-msg
   (`architecture: AR-n -- <how kept>` or `architecture: none -- <reason>`, and the `judgment:` line, on every
   package commit), `tools/architecture_index.py --check` in pre-commit and CI, the judgment census
   `scripts/tests/fixtures/judgment-census.json` with `test_judgment_census.py` (shrink-only ratchets),
   `role-load.json` `process_ratchet_tokens`; the critic's standing questions 10 and 11 (JUDGMENT); the designer
   names the AR-n, and for every check the owner it serves and its census class, in §1 of a package spec. This
   paragraph, critic questions 10-11, designer rule 1 and new-idea step 4 change together (axis 1). Detectors: calibration checks 36, 41.

### Rule 11 · the dispatch form — CLAUDE.md § The dispatch form (rule 11)

### Rule 11a · question routing

11a. Question routing (question-routing rule): questions route UP, work routes DOWN; the apex of the hierarchy is the
   OPERATOR — above Lead itself. An underspecified REQUIREMENT (interpreting intent, choosing the shape of a
   deliverable) is a question for the operator, and the work on that part waits for the answer; deciding it on the
   operator's behalf is out of bounds for every tier, Lead included. The skip concession is downward only: a tier may
   skip a dispatch to a tier below itself (with an event) but may not absorb a question that belongs above its own
   level — only escalate (rule 6; once the tiers up to the Lead are exhausted it queues for the Lead, and above the Lead for the
   architect — an item in `docs/tasks/architect-queue.md` + `escalated` with `agent: architect`). Work the coordinator
   executes itself after a `dispatch_skipped` passes the same acceptance as a builder diff (Role ≠ tier); handing the
   operator something that has not cleared it is a violation. With no operator present, a substitute path exists
   only as an explicit, named clause — here the owner-away paragraph of PROJECT.md «Что решать самому, что
   спрашивать у владельца».

### Rule 12 · the coordinator's cadence

12. The coordinator's cadence runs on LARGE moves, not a series of small ones: accepting workers happens in a BATCH
   at a stage boundary (accepting everything stays mandatory — the cadence changes, not the obligation); one question
   carrying a list instead of a round of clarifications; what code can do, code does — journal lines through
   `tools/journal_write.py`, dispatch headers from `tools/dispatch_new.py`, a merge of accepted branches through
   `tools/wave.py merge`, a red pipeline through `tools/ci_read.py why` (the owner's word 14.11.2026); the boot-budget backlog is worked down as a batch at handoff
   (boot-diet). The target is roughly 15 main-turns per task — a measured goal, not a gate.

### Rule 12 · Cost gates

   Cost gates (D-0035, D-0038, D-0040, D-0054; why: `docs/CLAUDE_HOST_ADAPTATIONS_FULL.md`): a fix round runs in a
   FRESH worker carrying only the diff and the verdict; `tools/agent_budget.py` caps a worker (WARN 250K, STOP 400K; the remainder goes to a fresh worker whole); (worker trimming and the one witness run: CLAUDE.md § Worker duties); ONE critic pass per topic (R13-g); critic on a plan: rule 3; a
   re-review carries only the fix diff and the verdict;
   After a critic verdict `fit_with_fixes` on CODE, the Lead checks the fix round ITSELF only inside this border (the
   owner's word 17.11.2026): the fix diff does exactly what the verdict's `fixes` prescribe and adds no new logic — no
   new function, branch, state or write path. The base is the reviewed head: the bare token `reviewed:<sha>` is the
   first token after the model label in the `description` of the critic's Agent call (for example `opus:
   reviewed:69f6272f re-review …`; the hook builds the `delegated` notes from `description` and cuts them at 300
   characters), written by the Lead from `git -C <tree> rev-parse HEAD` after COMMITTING the reviewed state — the Lead
   commits the reviewed state before each critic dispatch, otherwise the fix round is `nobase`. Measured on `git -C
   <tree> diff -U0 <sha> -- '*.py'` (added lines only; a line whose first non-blank character is `#` is not counted):
   zero lines matching the line-start pattern, zero lines matching the anywhere pattern, zero added lines matching the
   write-call pattern (the three patterns, each on one unbroken line so no wrap changes them, are in the block below),
   zero new files (`git diff --name-only --diff-filter=A <sha>` and `git ls-files --others --exclude-standard`), zero
   added `add_argument(`, no changed file other than `.py` and `.md`, and no line outside the owns the verdict
   reviewed:

```
^\+\s*(def |class |async def |if |elif |else\b|try:|except\b|finally:|for |while |match |case |return\b|raise\b|break\b|continue\b|yield\b|with\b|assert\b|del\b)
\bif\b|\bfor\b|\blambda\b|\band\b|\bor\b
write_text|write_bytes|open\(.*['"][wax]|append_jsonl|\.write\(|json\.dump|\.unlink\(|os\.(remove|replace|rename|makedirs)|shutil\.|subprocess\.|\.mkdir\(|\.touch\(
```

   Inside the border the Lead walks the fix diff by the critic's standing questions —
   `.claude/agents/critic.md` rule 22, Q1-Q12 — one line per question, plus one line per fix (`fixed: <where>` / `not
   fixed` → another fix round); a new dict entry used as a dispatch table is caught only by this walk (Q1, Q3). The
   `accepted` notes carry `fixes checked by Lead: <verdict path>, border 0`. Outside the border (any count above
   zero), with no `reviewed:` token (absent or cut) or a base that is not an ancestor of HEAD, when the verdict was
   `blocker`, when a fix cannot be matched to its verdict line, or when the acceptor is not strictly above the
   builder's tier (Role ≠ tier), a critic re-review carries only the fix diff and the verdict, and its dispatch names
   its case: `re-review: logic|nobase|blocker|unmatched|tier`. Plans keep PROJECT.md new idea, step 6.
   The Lead compacts by PROJECT.md § Сессия форджа, a stage
   commit per 2–3 merges, journal notes ≤ 300 chars, CI through `tools/ci_read.py`; a push before a worktree launch
   (`tools/dispatch_gate.py`). The writers, the FULL queue, the per-topic critic and merge waves: PROJECT.md
   «Командная работа» п. 12. Detector: check 17.

### Rule 13 · leaf routing

13. Leaf routing (leaf-routing rule) — not used in this deployment: no judge is bound (`delegation.config.yaml`,
   role `judge`), so every task, leaf or graph, goes through the acceptance of rules 1-12 and Role ≠ tier; an
   acceptance with `basis: "judge"` is not legal here.

   | R13 | when | duty |
   |---|---|---|
   | g | the parts of one topic | ONE critic pass per TOPIC, not one per part (Cost gates, rule 12); a topic holds at most 4 nodes (the owner's word 17.11.2026); a fifth node opens a new topic, split by disjoint owns or seams |

## Routing log — logs/journal/<dev>.jsonl

One journal file per developer: `<dev>` is the `developer:` slug of the untracked `tools/dev.config.yaml`
(`python tools/journal_keys.py where` names the file). One JSON line per event, written by the one writer
`python -B tools/journal_write.py <event> …` (the machine lock, the clock, the validator BEFORE the write; the owner's
word 14.11.2026): the Task/Agent PostToolUse hook writes `delegated` (and the owed designer `dispatch_skipped`) and the
SubagentStop gate writes `returned` by themselves; the coordinator writes `accepted`, `rejected` and the rest with one
call (`accept --run "<cmd>"` runs the verification under bash and stores its verbatim tail as the witness):

```json
{"ts":"2026-11-11T12:00:00","event":"delegated","agent":"builder","model":"sonnet","task_id":"t-042","category":"implementation","worker_ref":"agent:<id>","feature":"F19","notes":"brief: what was delegated"}
```

The journal is append-only and records ACCOMPLISHED FACTS, not intentions: `delegated` is written by the hook AFTER
the launch returns (a hook line `JOURNAL: … NOT written` is repaired the same turn with the CLI), `escalated` after
the dispatch call returns, same turn; a new `delegated` carries a `worker_ref` — a non-empty handle of the launch (a
background-task id, a job id, `cli:<ts>`, `retro:<...>`) that exists only after launch. Open dispatches are
reconciled at both session boundaries — the SessionStart hook and the session-handoff check — worker alive / result
pending / phantom; a phantom is closed by a bare `closes:<task-id>` token (several allowed in one `notes`) in the
`notes` of any LATER event; the open-dispatch scan reads ONLY this literal token — a prose-only closing note leaves
the task open. An already written order defect (id out of order, non-monotone `ts`, repeated `delegated`) is
declared, never rewritten: a bare `order-known:<ts>` (that line's exact `ts`) in the `notes` of a LATER line of the
same file (validator rule 19; check 13(m)). A task id is read by its IDENTITY `<id>@<label>`, and another clone's journal lines are form-checked
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
unclassified work is a Forge metric, not an error). Old events are never rewritten. A task id is issued by
`journal_write.py next` (or by the writer when no id is given) under the machine lock, from the clone's counter in the
git common directory, shared by every session and worktree of the clone; ids may skip and land out of order, never
repeat (validator rule 9a: never seen, at most 1000 above its letter's max). An id carries the clone's LETTER — none
for the first clone of a developer, `a`, `b`, … for the next ones (`logs/journal-letters.json`, `journal_write.py clone
--claim`; the owner's word 14.11.2026 «Номер 123 и 123А», written in lower case ASCII: `t-123`, `t-123a`). Bands
(`id_band`) are retired for new lines and still read in old ones; `journal_keys.py declare` repairs only collisions
already in history. A collision noticed later is not rewritten — it gets a note on the next event and counts as two
tasks (no-silent-reuse rule). `ts` is read from the system clock by the writer, never taken from the session's
narrative; a wrong `ts` noticed later gets a note on the next event (the reference: usage reports / git log,
calibration check 13(f)). A MISSED event noticed later is repaired by a RETRO pair: append
`delegated`/`accepted` NOW, with the current `ts`, a "retroactive" mark and the event's actual boundaries in
`notes`; inserting lines into the past is forbidden; calibration watches the retro stream.

### Routing log · event SHAPES

Event SHAPES — the typed fields each event adds on top of the five base fields:

| event | adds on top of the base fields |
|---|---|
| `delegated` | `task_id`, `model`, `worker_ref`; optional `node` — the pile node `<slug>/<N>/<id>` (`forge/5/F5-2`; `journal_keys.NODE_RE`; a bare id is never a node); a REPEAT on an open task is legitimate only as: a critic-entry (another tier) / a retry with `attempt`>=2 after `rejected` / a DEAD-WORKER REPLACEMENT: a bare `replaces_worker:<prev worker_ref>` token in `notes` — not a retry, `attempt` does not grow; the handle literally matches the `worker_ref` of a prior `delegated` of the same task; the first non-whitespace token after the colon is read, so trailing punctuation breaks the match; on a closed task it is forbidden |
| `returned` | `task_id`, `worker_ref` (the `delegated` it ends), `model`; written by the SubagentStop gate when a worker's stop passes; never closes a task — the open-dispatch scan shows it as RESULT PENDING until `accepted`/`rejected` |
| `accepted` | `task_id`, `model`, `by` (a bare model-family word — `haiku`/`sonnet`/`opus`/`fable`, see below); + `basis` ("critic" / "queued-to-lead") when the acceptor is not strictly above the executor; + `witness` (the verbatim run output) on builder work |
| `rejected` | `task_id`, `model`, `by`, `attempt` (number), `failure_class` ∈ spec/capability/recon/tooling |
| `escalated` | `task_id` (must already exist earlier in the file, except with `agent: architect`, which may open a task), `model` (the model the work moves to; for `architect`, the architect binding) |
| `calibrated` | optional `reviewed_through` — the sha of the last mechanism commit the Architect reviewed |
| `defect_found` | `task_id`, `ref` (the task_id of the original `accepted`) |
| `dispatch_skipped` | reason inside `notes` (no extra field) |

The `model` field is mandatory where the table names it — a self-declaration of Lead; calibration reconciles it
against transcripts, and a discrepancy is itself a calibration event. NEW lines are validated at TWO points
(`tools/journal_validator.py`): the pre-commit gate on `git commit`, and the WRITE moment — the PostToolUse hook
`journal_echo` re-validates the newest lines as they land and warns before the session ever reaches a commit. Both
share the checks: append-only, typed fields, ts-monotonicity, no ts from the future, task_id novelty (the legal
repeats: the `delegated` row). The `accepted` row encodes the acceptance matrix of Role ≠ tier; work performed by a
non-Claude model still carries a `basis` — the matrix compares FUNCTION tiers, not model ids. `by` and `model` differ
on purpose: `by` is a bare model-family word from `FAMILIES` in `tools/tier_ladder.py`
(`haiku`/`sonnet`/`opus`/`fable`), turned by the validator into a FUNCTION rank through the bindings — an unknown `by`, a full model id (e.g. `"claude-opus-4-8"`) included, FAILS the
matrix outright and no `basis` legalizes it; `model` is free-form, and a full model id there is recommended. The
validator's own failure detector is a pair of calibration checks. Events: the rows of the table — `rejected` is a
failed attempt (rule 6), `defect_found` a late defect in ACCEPTED work (agent = the original tier, notes: what broke
— the false-accept stream), `calibrated` a calibration run — plus `decomposable`, `lead_degraded`, `lead_restored`,
`journal_created`. The journal is the evidence for the weekly calibration
(PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md); DELEGATION_TABLE.md statuses move only on this data (Update Rule 1); a
calibration overdue by more than 7 days shows as a Last Calibration line in the Boot Report.

## Role ≠ tier

Three definitions that are NOT synonyms:

- The TIER of a session = the FUNCTION RANK of its ACTUAL model (verified at entry — tier-verification-at-entry
  rule): the highest function bound to that model in `delegation.config.yaml`, by exact id or by family
  (`tools/tier_ladder.py`). Opus and Fable are a MODEL NAME each; "Lead" and "architect" are tier-FUNCTIONS
  (decomposition, specs, acceptance, mechanisms; ideas, process, calibration), not roles in the conversation.
- The coordinator ROLE = ROUTING, not execution. Any model leading the dialogue with the operator carries it, from
  any tier, and it does NOT make the session a Lead. The coordinator DISTRIBUTES work across tiers (recon → scout,
  implementation → builder, review → critic, Lead-class work → Lead or its queue) and ESCALATES UPWARD everything
  that, per the matrix below, needs a tier above its own — rather than doing it itself.
- Full Lead = a coordinator whose rank is lead or above (the model bound to Lead, or the architect's model doing
  Lead work); only it changes mechanisms, the decision log, table statuses and gates.

Acceptance is only from ABOVE: `accepted` is legitimate when the acceptor's rank is strictly above the executor's
function rank, OR the decision carries input from a tier above (a critic verdict), OR acceptance is explicitly queued
for the full Lead (a note in notes). Acceptance by an equal/higher tier without that input is the session
self-certifying (self-certification violation class). An acceptance is never written from inside a worker: a critic
or designer verdict reaches the coordinator through the worker's handoff file. Matrix by the coordinator's actual
function rank:

- **architect rank** (the model bound to architect; Fable) — unrestricted; it may do any Lead work with no extra
  event (the `model` field of its journal lines records it). Routine coordination and each mechanism commit are the
  Lead's work, not its own.
- **lead rank** (the model bound to Lead; Opus) — full Lead: coordination, dispatches, acceptance of scout, builder,
  critic and designer work, the "critic: skipped" waiver over builder, mechanism commits after the critic (`tier:
  opus`), `DECISIONS.md`, statuses. Architect-class questions go by rule 6; a `Last calibration` line carrying
  `-- overdue:` → tell the owner once per session and put one item into `docs/tasks/architect-queue.md` if none is open.
- **builder rank** (the model bound to builder; a Sonnet coordinator) — coordination, dispatches; accepts scout; a
  builder diff — ONLY with critic input (the skip waiver is unavailable); critic and designer work — `basis:
  queued-to-lead`, cleared later by a Lead-ranked session writing a second `accepted` of the same task with no
  basis (calibration check 6 (iii) lists the uncleared); Lead-class work — `docs/tasks/lead-queue.md`.
- Below builder rank, coordination is not supported.

The tier names resolve through `delegation.config.yaml`. The standard mode — the owner coordinates on the Lead's
model and switches the session to the architect's model for architect work; a session on a model below lead (the mid-tier mode) is the
same matrix, and degradation (below) is an unplanned entry into it.

## Lead degradation

A refusal by the Lead's model (safety/dual-use, subscription limit, unavailability) OR an explicit operator switch
to a model ranked below lead:

1. Drop to builder rank (Sonnet) + a `lead_degraded` event (reason, scope) — ONE step. An outage of the Lead's model
   removes critic and designer with it: builder diffs finished meanwhile WAIT — one line each in
   `docs/tasks/lead-queue.md` («ждёт критика: <task_id>, <ветка>») and no `accepted`; critic and designer dispatches
   are not launched (the stand-in of rule 6 is legal when the wait hurts); recon and builder work under accepted
   specs continue.
2. While degraded: coordination and already-authorized tasks — yes; table statuses, gates — no; new decision-log
   entries are queued for the full Lead; acceptance per Role ≠ tier.
3. Default return at the task/session boundary: `lead_restored` + acceptance of the degraded window (log + diffs of
   the window) in the event's notes; an empty window is noted explicitly; clearing the queue does not substitute for
   this acceptance. Degradation spanning a session boundary is recorded as the journal's last event.
4. Tier verification at BOTH points (tier-verification-at-entry rule) — neither alone is sufficient: entry is skipped
   by self-detection while degraded, and there may be no rise back at all.
   a) ENTRY — before the FIRST Lead action of a session (dispatch, acceptance, a mechanism commit, a status change):
   check your own model by the last visible signal (the SessionStart `MODEL:` line; a switch command) against the
   lead binding; if its rank is below lead and the journal has not opened a window → `lead_degraded` BEFORE the
   action. A model that matches no binding and no known family never reads as Lead.
   b) EXIT — a visible rise from below lead to lead or architect rank is itself PROOF a window existed, independent
   of the journal: in the same turn, a retroactive `lead_degraded` (note + actual boundaries), acceptance of the
   window per point 3, `lead_restored`. A switch between the Lead's and the architect's model is NOT a window: no
   event.
   c) EXTERNAL CROSS-CHECK — check 5 of PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md: the actual model of Lead sessions
   per transcripts vs. window coverage by matched event pairs; it catches failures of both in-session checkpoints,
   including a session that died while degraded.
5. The architect's model unavailable or refusing is NOT a Lead degradation: no event; the items of
   `docs/tasks/architect-queue.md` wait and the owner is told once — the architect's absence never stops Lead work.
