# t-013 — CLAUDE.md: the policy rewritten as this project's own text (DRAFT, designer)

Status: DRAFT for Lead acceptance; forks in §7 are returned, not decided. Read with: `CLAUDE.md` (as on disk at 10b6f86,
865 lines; BEGIN marker :73, END marker :864), `docs/tasks/compact-snapshots/2026-11-11-manual.md`.

NOTE ON THE CARRIER. The CLAUDE.md text injected into sessions at the start of this dispatch was OLDER than the file on
disk (it still had «Until the phase-1 move lands…» in adaptation 12 and «Until nodes A3/A4 land…» in 10). Every line
reference below is to the file ON DISK (CLAUDE.md:1-865), which is authoritative.

## §1 Goal, scope, what it touches and crosses

Goal (the owner's words 11.11.2026): rewrite the policy block of `CLAUDE.md` «так как надо нам», without the list of host
adaptations; smaller and easier for agents to read; «из внешнего набора ничего больше не тянем. Номера пунктов оставим.
Правила которые мы не меняли не должны потеряться»; rule 13 (the judge) — text removed, number kept with one line.

Scope: `CLAUDE.md` whole (host intro + three imports + rules); its bindings (§4). No rule demands anything beyond what it
or a host adaptation demands today; no renumbering; no new rule ids; FG7-14 not folded (rule 7's label clause verbatim).

Principles touched:
- P31 (one action, one road): today a reader meets a kit rule and, 600 lines earlier, its cancellation (adaptation 12 over
  rule 4's «test FILE that judges each owned path» and rule 11's «AT and BEYOND» / «SCOPE CEILING»; adaptation 6 over rule
  3's critic-on-plan trigger). The rewrite leaves one operative wording per duty. One residual two-road place is returned
  as fork F5 (witness of a path outside the package).
- The boot-file rule (commit 10b6f86, the owner's word 11.11.2026 «Да, убирай»: a boot file holds only what every session
  needs): provenance, dead conditionals and the judge text leave the boot path; the history goes to
  `docs/CLAUDE_HOST_ADAPTATIONS_FULL.md`.
- P27 / AR-29: the text of host adaptation 10 moves into rule 10 unchanged in meaning.

AR-n: the package (`ai-packages/qa-factory/`) is NOT touched by this spec (the package comment
`scripts/acceptance.py:659` «host adaptation 2» is left and resolves through the map, §5 E1) → `architecture: none --
forge-only change`. Checks this spec alters, their owner and census class: `tools/install_parity.py --check` anchors
(owner: data — code checks the presence of text; census class: outside the package census, none);
`tools/tests/test_role_carriers_one_owner.py` POINTERS (data; none); `tools/session_context.py` `CLAUDE_WARN` (data, a
size threshold; none). No check judges a role's judgment.

Crosses: node FG7-14 of `plans/piles/forge/batch-7-vhodyashchie-4.md:37` (owns `CLAUDE.md`, status «ожидает») — it rewrites
rule 7's label clause later, on the NEW text, directly in rule 7 (there is no adaptation list to append to; its node text
says «хост-адаптация правила 7» — the Lead rewords it to «правка правила 7» when the batch is taken; the batch is not
taken, so it is not frozen). Order: t-013 first, FG7-14 after (§5 E6).

## §2 Inventory (the guard against losing an unchanged rule)

Verdicts: KEEP = duty unchanged (wording may be tightened, provenance removed); FOLD = changed by host adaptation N (how);
DROP = does not apply here (the fact). «§3 anchor» = where the duty stands in §3 (the rule number / section).

Completeness method: the structural units of the block are 7 headings (CLAUDE.md:75,86,110,555,697,748,788), 15 rules
(1-13, 4a, 11a), 4 degradation items, 7 hygiene points, 11 table rows (R1 a,b; R11 m,f,h; R13 g; pt.4 a,b; pt.6 a,b,c) =
44 units, all below; inside the long rules each distinct duty is split. The 81 anchors of unit `routing-policy`
(`tools/install_parity_anchors.json:7-87`) are: 7 headings, 14 rule openers (4a has none), 4 degradation openers, 7
hygiene openers and 49 clause phrases; each of the 49 phrases falls inside a row below (spot map in §4(a)). Host
adaptations 1-12 (CLAUDE.md:18-71): each is the source of at least one FOLD row (list at the end of the table).

| id | duty in one line | verdict | §3 anchor |
|---|---|---|---|
| H0 | title; host intro: PROJECT.md holds the project's rules (CLAUDE.md:1-4) | KEEP (merged with B2) | intro |
| H1 | `@PROJECT.md` import first (:6) | KEEP | intro |
| H2 | `@docs/FACTORY_RULES_INDEX.md`, then `@docs/ARCHITECTURE_INDEX.md` (:13,:15); the FR text is read before a package change | KEEP | intro |
| H3 | host-adaptation list header (:17) | DROP — the list disappears by the owner's word; history → FULL doc | — |
| B0 | BEGIN/END markers (:73-74, :864) | DROP — no code reads them (grep: only `.claude/skills/onboarding/SKILL.md:384,393`, `docs/ADOPTION_LEDGER.md:83`); nothing more is pulled from the kit | — (§4e) |
| B1 | heading «CLAUDE.md — Operating System for LLMs» (:75) | DROP as a second title; the file's title is line 1 | — |
| B2a | full restoration goes through BOOT.md, not here; boot context is expensive (:77-79) | KEEP | intro |
| B2b | only what must be in context always; else Lead self-executes delegable work on the top tier (:79-83) | KEEP (provenance «finding: …» out) | intro |
| B2c | «This repo is a deployment of the supervised-delegation routing method» (:83-84) | FOLD (owner 11.11): the policy is now the project's own, nothing more pulled from the kit | intro |
| TI1 | scout (Sonnet) — recon, digest with trail (:88) | FOLD adaptation 1 (already applied in the line; the clause «no tier runs on Haiku» joins it) | Tiers |
| TI2 | builder (Sonnet) (:90) | KEEP | Tiers |
| TI3 | critic (Opus) (:92) | KEEP | Tiers |
| TI4 | designer (Opus): drafting, forks returned, draft passes Lead acceptance (:94) | KEEP | Tiers |
| TI5 | Lead (Fable): decomposition, specs, acceptance; only Lead decides delegation (:97) | KEEP | Tiers |
| TI6 | role names are FUNCTIONS, rules speak only in them; binding is the deployment's; model grades never in rules, mapping in TWO_VOCABULARIES (:100-108) | KEEP (the «API track» aside out: contour subscription, `delegation.config.yaml:14`) | Tiers |
| 1.1 | recon → scout when >1–2 known files or any repo search; Lead reads one precise target (:112-114) | KEEP | rule 1 |
| 1.2 | up to ~4 known targets only with `dispatch_skipped` (reason) (:115-118) | KEEP | rule 1 |
| 1.3 | recon of unknown scope always scout (:118) | KEEP | rule 1 |
| 1.4 | external repo: two-pass; Lead's second pass trail into RELATED_WORK; no skip event; check 16 (:118-125) | KEEP («RELATED_WORK section» → `docs/RELATED_WORK.md`, which exists) | rule 1 |
| 1.5 | digest accepted by trail; no trail → rejected (:125-130) | KEEP | rule 1 |
| R1-a | lifted verification while the scout holds a current exam pass (:134) | DROP — no scout exam set is registered: `PROCESS/` holds 11 files, none `SCOUT_GOLDEN_SET*` (Glob, positive control `**/*JUDGE_CALIBRATION*` found); the row never fires. Row id kept with one line (fork F4) | R1 table |
| R1-b | strict form: spot-verify one load-bearing claim, negative mandatory, noted in `accepted` (:135) | KEEP — becomes the standing form (it is the only form that can apply) | R1 table |
| 2.1 | implementation → builder; Lead writes spec; builder returns missing requirements as questions (:137-139) | KEEP | rule 2 |
| 2.2 | builder diff accepted by witness in `witness`; no witness → rejected (:139-143) | KEEP | rule 2 |
| 2.3 | UI task: drive the UI, before/after screenshot (:143-145) | KEEP | rule 2 |
| 2.4 | self-activating enforcement file never placed live by builder; Lead places at acceptance (:146-152) | KEEP | rule 2 |
| 2.5 | DRAFTING → designer BY DEFAULT at 3+ numbered items or 3+ files (:154-158) | KEEP + FOLD adaptation 2 (pointer: the draft form incl. edge invariants and a reused function's error direction is designer.md rule 1) | rule 2 |
| 2.6 | Lead self-drafting only with `dispatch_skipped` agent=designer (:158-160) | KEEP | rule 2 |
| 2.7 | motive is CONTEXT ISOLATION, owed regardless of tier relation (:160-165) | KEEP | rule 2 |
| 2.8 | below threshold and intent briefs: no event (:165-166) | KEEP | rule 2 |
| 2.9 | threshold counts PRIMARY draft; RESUBMISSION under same task_id = continuation, Lead edits itself, no event (:166-172) | KEEP | rule 2 |
| 2.10 | NEW task_id = new task; parts after `decomposable` judged on their own (:172-175) | KEEP | rule 2 |
| 3.1 | critic mandatory: diffs >~100 lines or schema/core/money; unclear bugs before Lead debugs (:176-178) | KEEP | rule 3 |
| 3.2 | first filter = executor's own self-run against DoD (:178-180) | KEEP | rule 3 |
| 3.3 | every diff gate answers DUPLICATION and CODE QUALITY (:180-183) | FOLD adaptation 5: rule text `docs/tasks/critic-diff-brief.md` items 6-7, critic rule 18 points there | rule 3 |
| 3.4 | acceptance rests with Lead (:183-184) | KEEP | rule 3 |
| 3.5 | «critic: skipped» waiver only for an acceptor above the executor (:184-187) | KEEP | rule 3 |
| 3.6 | TWO-LAYER CRITIC ENTRY: mechanical layer attached verbatim before the verdict; critic's verdict layer; cheap re-run legal, reading the mechanics not; missing layer → request (:187-196) | KEEP | rule 3 |
| 3.7 | money/numeric: empirics first (:196-198) | KEEP | rule 3 |
| 3.8 | critic-on-plan for a deliverable serving as spec for >30 min work (:198-204) | FOLD adaptation 6 («only for forks or a schema/money change, otherwise critic: skipped») + PROJECT.md mandatory cases (new idea step 6; meaning-changing spec edit p. 6) — fork F10 | rule 3 |
| 4.1 | independent parts → parallel subagents, own specs (:205-206) | KEEP | rule 4 |
| 4.2 | parallel specs declare owns; Lead checks overlap (:206-207) | KEEP | rule 4 |
| 4.3 | parallel sessions: never touch/commit another session's uncommitted paths (:207-210) | KEEP | rule 4 |
| 4.4 | cross-deployment item exists only in a carrier the target reads at boot (:210-214) | KEEP | rule 4 |
| 4.5 | witness run narrowed by owns: the test FILE that judges each owned path (:215-221) | FOLD adaptations 11+12: the run is what `scenario_walk.py --witness-for <owns>` prints (builder-rules 7b), never big neighbours, never a quarantined file; non-package paths: fork F5 | rule 4 |
| 4.6 | FULL canonical run = coordinator's duty after convergence (:221-223) | FOLD D-0056/D-0059 (PROJECT.md p. 2): it is the CI pipeline on the batch branch, never this machine | rule 4 |
| 4.7 | canon output APPENDED to the last `accepted` witness, node's run first, then BATCH CANON (:223-229) | KEEP | rule 4 |
| 4.8 | SOLO writing dispatch keeps the same narrowed witness (:229-231) | FOLD adaptation 11 («solo or parallel» stated once) | rule 4 |
| 4.9 | node accepted on own witness; canon failure → `defect_found`, no reopening (:231-235) | KEEP | rule 4 |
| 4.10 | (adaptation 6) ≤6 parallel WRITING workers, push before worktree launch, queue FULL | FOLD adaptation 6 → Cost gates paragraph of rule 12; rule 4 points there (fork F3) | rule 12 |
| 4a.1 | 5+ events or 2+ sessions → markdown DAG (:236-238) | KEEP + carrier question fork F7 | rule 4a |
| 4a.2 | writing node declares owns (:238-239) | KEEP | rule 4a |
| 4a.3 | node status moves in the same turn as its journal event (:239-240) | KEEP | rule 4a |
| 4a.4 | piles and batches: one taker, frozen batch, frozen BACKLOG, one journal per developer, CURRENT_CONTEXT = main; gates; check 33 (:44-49) | FOLD adaptation 7 | rule 4a |
| 5.1 | subagents never launch subagents (:241-242) | KEEP | rule 5 |
| 5.2 | decomposable task → `decomposable` event (:242-243) | KEEP | rule 5 |
| 6.1 | 2 failed attempts or «beyond my level» → one tier up + `escalated` (:244-246) | KEEP | rule 6 |
| 6.2 | silent same-tier retry forbidden (:246) | KEEP | rule 6 |
| 6.3 | every rejection = `rejected` with task_id, attempt, failure_class (:246-250) | KEEP | rule 6 |
| 6.4 | two `rejected` same task same tier → escalation mandatory (:251-252) | KEEP | rule 6 |
| 6.5 | attempt counter is a proxy; crossover measured by calibration (Update Rule 4) (:252-254) | KEEP | rule 6 |
| 7.1 | background by default; sync only when next step depends AND nothing else pending (:255-258) | KEEP | rule 7 |
| 7.2 | accepting on completion mandatory (:258-259) | KEEP | rule 7 |
| 7.3 | dispatch label starts with the worker's model (:259-263) | KEEP VERBATIM (non-goal; FG7-14 changes it later) | rule 7 |
| 7.4 | tier REQUIREMENT closes by MEASUREMENT: journal_echo measures `agent:<id>`, mismatch resolved before use (:263-270) | KEEP | rule 7 |
| 8.1 | cheap-tier task done by Lead only with `dispatch_skipped` (:271-274) | KEEP | rule 8 |
| 8.2 | follows the ROUTING MOTIVE: context-isolation functions owe the event too (:274-278) | KEEP | rule 8 |
| 8.3 | standing case designer; critic-skip waiver is a note in `accepted` (:278-280) | KEEP | rule 8 |
| 8.4 | SMALL-WORK BATCHING: non-blocking small edits batch to one builder dispatch at a stage boundary, marker in notes (:280-285) | KEEP | rule 8 |
| 8.5 | self-execution with skip only for a blocking edit, reason names the blocker (:285-287) | KEEP | rule 8 |
| 8.6 | «operator waiting» reason legal only on the FIRST move; from the second: non-blocking → batch, blocking → IMMEDIATE SOLO builder dispatch, never self-execution (:287-301) | KEEP (provenance «measured window…» out) | rule 8 |
| 8.7 | Lead-tier work needs no skip event (:301-303) | KEEP | rule 8 |
| 8.8 | DETERMINISTIC SCRIPT RUNS: no skip event, trace in own carrier, doubt → skip event (:303-311) | KEEP | rule 8 |
| 9.1 | name the class; walk siblings by the MAP; wider → scout (:312-315) | KEEP | rule 9 |
| 9.2 | fix now or EXPLICITLY queue (:315-316) | KEEP | rule 9 |
| 9.3 | the rule against recurrence on the highest level tying the siblings (:316-318) | KEEP verbatim (owner key) | rule 9 |
| 9.4 | new symmetry = new axis, same commit (:318) | KEEP | rule 9 |
| 9.5 | silently leaving a known sibling = violation (:319) | KEEP | rule 9 |
| 9.6 | workers report analogs; critic checks by the map; Lead owns the rule's home (:319-322) | KEEP | rule 9 |
| 9.7 | sweep the artifact first; unit = enclosing block; no special opening; enumeration with verdict; «no neighbors» line (:324-334) | KEEP | rule 9 |
| 9.8 | unit >150 lines or >5 neighbors → one scout dispatch or skip event (:334-337) | KEEP | rule 9 |
| 9.9 | sweep never replaces the map walk (:338-339) | KEEP | rule 9 |
| 10.1 | (a) cost of compliance, in writing before the commit (:342-345) | KEEP | rule 10 |
| 10.2 | (b) axis ENUMERATION per axis, per mechanism (:345-354) | KEEP | rule 10 |
| 10.3 | (c) registered detector, for old mechanisms too; a gap is a finding (:354-359) | KEEP | rule 10 |
| 10.4 | (d) what stops skipping; discipline only as an explicit line naming the detector; promotion on evidence (:359-366) | KEEP | rule 10 |
| 10.5 | operator questions exposing a gap → findings (:367-368) | KEEP | rule 10 |
| 10.6 | mechanism_gate in commit-msg; «axes: not a mechanism (<reason>)» (:368-374) | KEEP | rule 10 |
| 10.7 | «tier: <model>» line; gate rejects below the lead binding (:374-379) | KEEP | rule 10 |
| 10.8 | recognition: any duty/check change wherever it lives; doubt → treat; recognition audit (:379-388) | KEEP | rule 10 |
| 10.9 | package change names AR-n; producer+readers one commit; architecture_gate, index check, critic q10, designer §1; check 36 (:52) | FOLD adaptation 9 | rule 10 |
| 10.10 | code owns data, role judgment, person intent; AR-29 breach; census, `judgment:` line, process_ratchet_tokens; critic q11, designer rule 1 change together; check 41 (:53-60) | FOLD adaptation 10 | rule 10 |
| 11.1 | DoD to any tier, in that tier's form (:389-391) | KEEP | rule 11 |
| 11.2 | builder: criteria + verification run → witness (:391-393) | KEEP | rule 11 |
| 11.3 | edge behaviour NAMED (limits, empty, conflicting pairs) or forked; silence = dispatcher defect (:393-399) | KEEP verbatim key | rule 11 |
| 11.4 | (i) TEMPORAL both worlds, (ii) POSITIONAL invariant (:399-409) | KEEP | rule 11 |
| 11.5 | INTERACTIVE surface → mini-battery; every limit AT and BEYOND (:409-412) | FOLD adaptation 12: only input from OUTSIDE; cases are scenario variant rows; an internal boundary gets no test | rule 11 |
| 11.6 | SCOPE CEILING: keys + battery + boundaries (:413-414) | FOLD adaptation 12: ceiling = `docs/TESTING.md` (no new test file outside `keep` rows, register row not pin file, no pin on source/measured constant) | rule 11 |
| 11.6b | three layers, one parameterised test per behaviour; quarantine not run/repaired/edited; `TEST QUARANTINE ALERT`/`READY TO DELETE` → tell the owner same turn; check 33 + test_quarantine.py (:63-71) | FOLD adaptation 12 | rule 11 |
| 11.7 | scout DoD: question + completeness; «nowhere» needs a trail (:414-417) | KEEP | rule 11 |
| 11.8 | critic dispatch attaches the spec/DoD (:417-419) | KEEP | rule 11 |
| 11.9 | DoD-less dispatch returned as questions (:419-420) | KEEP | rule 11 |
| 11.10 | CONTEXT MANIFEST: given; writing: owns, non-goals, handoff; fan-out ownership + maxConcurrent (:421-427) | KEEP | rule 11 |
| 11.11 | DECLARATIVE on reads, NORMATIVE on writes; «needed beyond the manifest» (:428-431) | KEEP | rule 11 |
| 11.12 | targeted read-only: the manifest is the attached enumeration (:431-433) | KEEP | rule 11 |
| 11.13 | manifest-less writing dispatch returned (:433-435) | KEEP | rule 11 |
| 11.14 | FIVE-POINT CHECKLIST by the dispatcher before sending (:435-450) | KEEP; point (4) FOLD adaptation 11: every writing dispatch (solo or parallel) names its witness scope | rule 11 |
| 11.15 | checklist miss = dispatcher spec defect; promotion on recurrence (:450-452) | KEEP | rule 11 |
| 11.16 | DoD INLINE; a pointer is NOT a DoD (:452-455) | KEEP | rule 11 |
| 11.17 | DOC-DISPATCH WITNESS three properties (:455-468) | FOLD adaptation 12 on (ii): attached in FULL in the report, never committed as a test | rule 11 |
| 11.18 | returns are an emergency net; frequent returns flagged (:468-472) | KEEP | rule 11 |
| 11.19 | Lead-tier tasks and the judge covered by own mechanisms (:472-474) | KEEP for Lead (Lead exam, calibration); judge part DROP (no judge, `delegation.config.yaml:80-85` empty) | rule 11 |
| R11-m | given as a marked declaration, one hop; owns always inline (:478) | KEEP | R11 table |
| R11-f | builder / absolute-owns dispatch: header lines, dispatch_manifest.py, manifest-skip door (:479) | FOLD adaptation 3 (applied; «host adaptation» parenthetical out, D-0022 stays) | R11 table |
| R11-h | critic/designer: report on handoff:, handoff_gate (:480) | FOLD adaptation 8 (applied; «D-0045 reserved» out) | R11 table |
| 11a.1 | questions UP, work DOWN; operator is the apex (:482-484) | KEEP | rule 11a |
| 11a.2 | underspecified requirement → operator; work waits; no tier decides it (:484-488) | KEEP | rule 11a |
| 11a.3 | skip concession downward only; escalate (:488-492) | KEEP | rule 11a |
| 11a.4 | self-executed work passes builder-diff acceptance; unaccepted → operator is a violation (:492-495) | KEEP | rule 11a |
| 11a.5 | headless substitute only as a named clause (:495-498) | KEEP + pointer to PROJECT.md's owner-away paragraph as that clause (fork F11) | rule 11a |
| 12.1 | worker acceptance in a BATCH at a stage boundary (:502-505) | KEEP | rule 12 |
| 12.2 | one question with a list (:505-506) | KEEP | rule 12 |
| 12.3 | journal append at the actual TAIL (:506-508) | KEEP | rule 12 |
| 12.4 | boot-diet backlog as a batch at handoff (:508-509) | KEEP | rule 12 |
| 12.5 | ~15 main-turns per task, measured goal (:509-511) | KEEP | rule 12 |
| 12.6 | cost gates: fresh fix-round worker, budget cap WARN 250K/STOP 400K, one critic pass per topic, re-review form, compaction, stage commit, notes ≤300, ci_read, ≤6 writers, push before worktree, slot exemption, queue FULL, check 17 (:33-43) | FOLD adaptation 6 (fork F3 on placement) | rule 12 |
| 13.1 | intake classifies leaf/graph (:512-515) | DROP — without a judge the class changes nothing: the rule's own text :543-545 «with no judge available in either form, the standard acceptance path applies to every task» | rule 13 line |
| 13.2 | leaf runs through the lighter construction, judge acceptance, `basis: judge` (:515-520) | DROP — no judge bound (`delegation.config.yaml:80-85`; `docs/ADOPTION_LEDGER.md:99` deferred) | rule 13 line |
| 13.3 | judge rejection mirrors rule 6 deterministically (:521-523) | DROP — judge loop only | — |
| 13.4 | deviation from the leaf path needs a recorded reason (:523-526) | DROP — no leaf path exists | — |
| 13.5 | recon-leaf DoD carries the negative-form-control criterion (:526-529) | DROP here; the duty still lives in R1-b (negative claims verified), 11.7 and hygiene 6 | R1-b, 11, hygiene 6 |
| 13.6 | two judge forms, equivalence before use (:529-539) | DROP — no judge | — |
| 13.7 | judge only for leaf-class, never mechanisms (:539-542) | DROP — stricter now: no judge acceptance at all | rule 13 line |
| 13.8 | graph tasks and the no-judge case: standard Lead loop for every task (:543-545) | KEEP — the one operative line of rule 13 | rule 13 |
| 13.9 | misclassification recoverable (:545-549) | DROP — no classification | — |
| R13-g | critic at integration for judge-accepted leaves; same topic merged through one pass; cumulative >2 small (:553) | FOLD (fork F2): «same topic merged TOGETHER through ONE critic pass» lives (adaptation 6 cites R13-g, `CLAUDE.md:35`); the judge-only cumulative clause dies (check 2's CUMULATIVE SUBCASE is judge-only, `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md:80-86`) | R13 table |
| J0 | journal heading names `logs/routing-log.jsonl` (:555) | FOLD adaptation 7: `logs/journal/<dev>.jsonl` (the only journal on disk: `logs/journal/dev1.jsonl`; routing-log absent, Glob with positive control) | Routing log |
| J1 | one JSON line per event via Edit/Write; example (:557-561) | KEEP (example gets `feature`, adaptation 4) | Routing log |
| J2 | append-only, facts not intentions; delegated/escalated after the call returns (:563-565) | KEEP | Routing log |
| J3 | `worker_ref` on new delegated, exists only after launch (:565-569) | KEEP | Routing log |
| J4 | open dispatches reconciled at both boundaries; phantom closed by bare `closes:<id>` only (:569-576) | KEEP | Routing log |
| J5a | task id by identity `<id>@<label>`; journal_keys the one loader; readers key by it; `closes:` may carry the label; unknown label closes nothing; GATE on bare ids (:576-583) | KEEP (label = the writer's file slug, `tools/journal_keys.py:28-35`) | Routing log |
| J5b | `logs/journal-segments.json` declaration of foreign lines (:577-579) | DROP — no such file; the declaration «applies to the history only» (`tools/journal_keys.py:688`) and the history file is absent (dev1 line 1: «new repository after github-move; the history stays in the old repository's bundle») | — |
| J6 | merge form-check of foreign lines; `merge-accepts:` door anchored on HEAD's ts (:583-591) | KEEP (`.githooks/pre-merge-commit:18` still runs it) | Routing log |
| J7 | five base fields; ts local ISO without Z; lead_degraded extras (:593-599) | KEEP | Routing log |
| J8 | typed fields list; old events never rewritten (:601-610) | KEEP | Routing log |
| J9 | task_id: re-read tail, max+1, collision note, counts as two (:610-615) | KEEP | Routing log |
| J10 | ts from the clock, not narrative; wrong ts → note; reconciliation reference (:615-621) | KEEP | Routing log |
| J11 | missed event → RETRO pair now; no insertion into the past (:621-628) | KEEP | Routing log |
| J12 | Event SHAPES table (:630-640) | KEEP; `accepted` row FOLD (judge basis DROP); adaptation 4 `feature` FOLD | Routing log |
| J12f | (adaptation 4) every new event carries `feature: Fnn`; WARN; forge_metrics attribution; unclassified = metric (:25-29) | FOLD adaptation 4 | Routing log |
| J13 | `model` mandatory, reconciled, discrepancy = event (:642-645) | KEEP | Routing log |
| J14 | validated at TWO points: pre-commit and journal_echo at write (:646-652) | KEEP | Routing log |
| J15 | shared checks; repeat delegated legal cases incl. DEAD-WORKER REPLACEMENT literal match (:652-662) | KEEP | Routing log |
| J16 | delegated on a closed task forbidden (:662-663) | KEEP | Routing log |
| J17 | `by`; acceptance legal by tier or basis critic/queued-to-lead; non-Claude work carries basis (:663-671) | KEEP; «OR judge» DROP | Routing log |
| J18 | `by` is a bare TIER_ORDER word; unknown/full id FAILS, no basis legalizes; `model` free-form (:671-682) | KEEP («(including judge)», «ported from…» out) | Routing log |
| J19 | validator's detector = a pair of calibration checks (:682-683) | KEEP | Routing log |
| J20 | events list (:683-691) | KEEP | Routing log |
| J21 | the journal is calibration evidence; DELEGATION_TABLE statuses on data; overdue calibration in Boot Report (:691-695) | KEEP | Routing log |
| RT1 | three definitions are not synonyms (:699-702) | KEEP (provenance out) | Role ≠ tier |
| RT2 | tier = actual model; Fable = top; Lead is a function (:704-707) | KEEP | Role ≠ tier |
| RT3 | coordinator role = routing; distributes; escalates upward (:708-714) | KEEP | Role ≠ tier |
| RT4 | only full Lead changes mechanisms, decision log, statuses, gates (:715-716) | KEEP | Role ≠ tier |
| RT5 | acceptance only from above: higher tier / critic input / queued (:718-722) | KEEP; judge condition DROP | Role ≠ tier |
| RT6 | otherwise self-certification (:723-725) | KEEP | Role ≠ tier |
| RT7 | matrix top / upper-mid / mid / below (:728-739) | KEEP | Role ≠ tier |
| RT8 | names resolve through the binding; standard mode; degradation is an unplanned entry (:741-746) | KEEP | Role ≠ tier |
| LD0 | trigger: refusal / limit / unavailability / operator switch (:750-751) | KEEP | degradation |
| LD1 | drop one tier + `lead_degraded` (reason, scope) (:753-755) | KEEP | degradation 1 |
| LD2 | while degraded: allowed/forbidden; queue decisions; acceptance per matrix (:756-760) | KEEP | degradation 2 |
| LD3 | return: `lead_restored` + acceptance of the window; empty window noted; spanning a boundary → last event (:761-765) | KEEP | degradation 3 |
| LD4 | verification at BOTH points; a) ENTRY before the first Lead action; b) EXIT retroactive pair; c) EXTERNAL CROSS-CHECK check 5 (:766-786) | KEEP | degradation 4 |
| CH0 | custom command forms are permission requests (:790-791) | KEEP | hygiene |
| CH1 | canonical test form by contour (:793-797) | FOLD: contour subscription only (`delegation.config.yaml:14`); the full run is CI's (PROJECT.md p. 2, D-0059) | hygiene 1 |
| CH2 | proxy server from gateway/ with keys (:798-800) | DROP — subscription contour; «gateway/ … nothing in it is wired or run» (`docs/ADOPTION_LEDGER.md:112`). Number kept, one line | hygiene 2 |
| CH3 | no `cd <dir> &&` prefix, no ` 2>&1` (:801-802) | KEEP | hygiene 3 |
| CH4 | edits only via Edit/Write; pt.4 a (named committed script legal), b (pure calculation outside scope) (:803-809) | KEEP | hygiene 4 |
| CH5 | log entries via Edit/Write, not printf (:811) | KEEP | hygiene 5 |
| CH6 | env-negative needs a positive canonical check; any env claim measured or labelled; content-search positive control of the same SHAPE; registry status read through (:812-844) | KEEP («points 1–2» → «point 1»; provenance out) | hygiene 6 |
| pt.6 a/b/c | one experiment first; a number carries its carrier, one metric; character claims by Read only (:848-850) | KEEP | hygiene 6 table |
| CH7 | corruption rolled back by BYTE COPY (a)-(d) (:852-863) | KEEP | hygiene 7 |

Host adaptation → row: 1 → TI1; 2 → 2.5; 3 → R11-f; 4 → J12f, J1; 5 → 3.3; 6 → 12.6, 3.8, 4.10, R13-g; 7 → 4a.4, J0;
8 → R11-h; 9 → 10.9 (+H2 «rule 10»); 10 → 10.10; 11 → 4.5, 4.8, 11.14; 12 → 11.5, 11.6, 11.6b, 11.17, 4.5. All twelve placed.

## §3 The new text (paste WHOLE as `CLAUDE.md`)

Byte count: NOT measured (this role has no shell). Estimate, not verified: ~330 lines × ~112 bytes ≈ 37 000 bytes (UTF-8;
arrows and «» count 2-3 bytes). The builder measures `os.path.getsize("CLAUDE.md")` and reports it; if over 40 000, §3
footnote «What else could go» applies. Lines are kept under ~120 chars so every anchor of §4(a) sits on ONE line.

````markdown
# CLAUDE.md — QA Factory development

Auto-loaded into every session: the routing policy of this repository and its command hygiene, and nothing that not
every session needs. It began as the supervised-delegation kit's policy; since the owner's word of 11.11.2026 it is this
project's own text, nothing more is pulled from the kit, and every rule keeps its number (the history of each clause:
`docs/CLAUDE_HOST_ADAPTATIONS_FULL.md`). Full state restoration goes through BOOT.md ("Restore context from BOOT.md"),
not here: boot context is expensive (boot-context-is-expensive rule). Without an auto-loaded policy, Lead ends up doing
delegable work itself on the most expensive tier (cheapest-tier-default rule).

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
   more files, is DRAFTED by the designer from a Lead intent brief (the draft's form, edge invariants and the error
   direction of a reused function included: `.claude/agents/designer.md` rule 1); the Lead self-drafting it anyway
   is legal ONLY with a `dispatch_skipped` event (agent = designer, reason mandatory). The motive is CONTEXT
   ISOLATION — an independent drafting context, not model price — so the event is owed whatever the tiers of designer
   and Lead. Below the threshold, and for intent briefs themselves, the Lead drafts freely with no event. The
   threshold counts the task's PRIMARY draft. A RESUBMISSION after a `rejected` — a retry under the SAME task_id — is
   a CONTINUATION of the existing spec: the Lead edits it ITSELF, with no designer dispatch and no `dispatch_skipped`
   event. Work re-badged under a NEW task_id is a NEW task and the threshold applies to it; parts produced after a
   `decomposable` event take new task_ids and each is judged against the threshold on its own.
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
   forks or a schema/money change, and always for a new idea of the owner and for a spec edit that changes a meaning
   (PROJECT.md: new idea, step 6; package change, p. 6); otherwise `critic: skipped, <reason>`. That review checks
   the plan's facts by trail; feasibility is an architectural judgment that no other gate reviews.
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
   owns; a node's status moves in the same turn as its journal event, not separately. Team work runs in piles and
   batches (D-0036; rule text PROJECT.md «Командная работа»): `plans/piles/<slug>/` with `plans/PILES.md` generated;
   ONE taker per batch, frozen once taken; `plans/BACKLOG.md` frozen (only `piles.py close`); one journal per
   developer; `CURRENT_CONTEXT.md` = the state of `main` only. Gates: `piles.py check --msg-file` in commit-msg (door
   `piles-skip: <item> -- <reason>`), `board --check` in pre-commit, pre-merge-commit and CI. Detector: check 33.
5. Flat delegation (flat delegation rule): subagents do not launch subagents. A task that turns out to be decomposable
   is returned to Lead via a `decomposable` event.
6. Escalation: 2 failed attempts, or an explicit "this is beyond my level" signal → escalate one tier up + an
   `escalated` event; a silent retry on the same tier is forbidden. A failed attempt = a result REJECTED at
   acceptance; every rejection is a `rejected` event (agent = the worker, model mandatory; task_id, attempt,
   failure_class = spec/capability/recon/tooling; reason in notes). Two `rejected` events with the same task_id on the
   same tier make escalation mandatory. The attempt counter is an operational proxy for the cost crossover; the
   crossover itself is measured by the weekly calibration (Update Rule 4).
7. Background execution by default (background-by-default rule): `run_in_background`; synchronous only when the next
   step depends on the result AND there is no other work or operator question pending. Accepting the result on
   completion is mandatory (flat delegation rule). The visible dispatch label (`description`) starts
   with the worker's model: "haiku: …" / "sonnet: …" / "opus: …" (a
   non-standard agent: its actual model) — the operator sees the tier
   in the background-task list, the same self-declaration as the
   journal's `model` field (reconciled by calibration check 4). A tier REQUIREMENT closes by MEASUREMENT, not by
   declaration alone: when a journal line carries a `worker_ref` of the form `agent:<id>`, the `journal_echo` hook
   measures the worker's actual transcript models and warns on a MISMATCH against the declared model; a mismatch is
   resolved — relaunch, an honest record via `basis`, or escalation — before the result is used as that tier's word.
8. Universal skip rule: a task that maps to a cheaper tier, or to a function routed for context isolation, done by
   the Lead itself is legitimate ONLY with a `dispatch_skipped` event (agent = the skipped function, reason
   mandatory) — on any tier: the rule follows the ROUTING MOTIVE, not the price gap. Standing case: designer drafting
   (rule 2). Waiver: skipping critic on a small diff is a note inside `accepted`. Lead-tier work (decomposition,
   specs, acceptance, architecture, policy) needs no skip event. SMALL-WORK BATCHING: a small builder-class edit that
   does NOT block the next step is not self-executed one at a time — it accumulates in a session-scoped list and goes
   to builder as ONE batched dispatch at a stage boundary (rule 12; a "small-work batch" marker in notes);
   self-execution with a skip event stays legitimate only for an edit that blocks the current step, and the reason
   names the blocker. A reason of the class "the operator is waiting / an interactive request blocks the move" is
   legitimate for SELF-EXECUTION ONLY on the FIRST such move in a session; from the SECOND, self-execution is a
   violation even for a blocking edit: a non-blocking edit joins the small-work batch, a blocking one goes out as an
   IMMEDIATE SOLO builder dispatch, never self-execution and never a batch entry. DETERMINISTIC SCRIPT RUNS:
   launching/collecting a deterministic script (an exam runner, a validator, a health check — code with no AI
   judgment in the coordinator's loop) is an environment operation, not a tier task: no `dispatch_skipped`, but the
   result lives in its own carrier (a runs log, journal events, a report) — a run with no carrier trace is a
   violation; in doubt (the run embeds judgment) the skip event is the safe default.
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
   one commit. Code owns DATA (reads, assembles, carries, checks keys and cross-references), a role owns JUDGMENT and
   the OUTCOME (accepted by meaning by a tier above, with a witness), the person owns INTENT: a package check that
   judges a role's judgment, closes a role's obligation by a closed list or refuses a role's output on its content is
   a breach of AR-29. On the path: `tools/architecture_gate.py` in commit-msg (`architecture: AR-n -- <how kept>` or
   `architecture: none -- <reason>`, and the `judgment:` line, on every package commit),
   `tools/architecture_index.py --check` in pre-commit and CI, the judgment census
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
   Which tests a DoD asks for (the owner's word 10.11.2026; rule text `docs/TESTING.md`): behaviour through the
   script's door and the stage junction, one parameterised test per behaviour, cases as rows. Input from OUTSIDE (a
   CLI/UI that accepts user input, a ticket, a person's words, a project config, a host answer) gets an adversarial
   mini-battery — magnitude, nesting, encoding, empty/broken input — and every limit applied to it a case AT and
   BEYOND it, each a scenario variant row; an internal boundary gets no test. SCOPE CEILING: `docs/TESTING.md` — no
   new test file outside the `keep` rows of `ai-packages/qa-factory/scripts/tests/test-layers.json`; a role's rule is
   guarded by one register row, not a pin file; no pin on script source or on a measured constant. Tests outside the
   three layers are QUARANTINED (spec `docs/tasks/specs/td-15-scenarios-quarantine.md`): not run in the canon, not
   repaired, not edited. When the SessionStart line says `TEST QUARANTINE ALERT` or `READY TO DELETE`, the Lead tells
   the owner the same turn (detectors: check 33, `tools/test_quarantine.py check` in `forge-check`).
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
   (1) an explicit question / completeness criterion or acceptance keys; (2) the DoD inline with the exact
   verification run AND the edge behaviors NAMED — limits/truncations, empty/absent inputs, conflicting requirement
   pairs: stated, or explicitly forked up; (3) "given" enumerated AND sufficient — data, fixtures, paths NAMED, not
   implied; (4) a writing dispatch: owns/non-goals/handoff present and its witness scope named (rule 4); (5)
   freshness — the spec's load-bearing facts checked against their carrier, not memory. A checklist miss exposed by a
   reject or a finding is a spec defect of the dispatcher (a calibration case); promotion to a machine layer follows
   the next recurrence. The DoD is written INLINE in the dispatch — named acceptance criteria plus the exact
   verification run; a bare pointer to a spec file or an earlier event is NOT a DoD. DOC-DISPATCH WITNESS: when the
   owns are markdown/config with no test set of their own, a deterministic key-presence run is a legal mechanical
   layer ONLY with three properties: (i) the keys are quoted VERBATIM from the DoD as written BEFORE the run; (ii) the
   script is attached in FULL source with the witness in the report, never committed as a test; (iii) the run
   includes a NEGATIVE control (one key deliberately absent → the script reports failure). Missing any of the three →
   the witness is a retelling, not a run (detector: calibration check 13(k)). A worker returning a DoD-less or
   manifest-less dispatch is an emergency net, not the normal cycle: frequent returns are a coordinator defect,
   flagged at calibration. Lead-tier tasks are covered by their own mechanisms (the Lead exam, weekly calibration).

   | R11 | when | duty |
   |---|---|---|
   | m | a WRITING dispatch's "given" manifest | executed as a MARKED declaration: an inline enumeration, OR a pointer to a persisted spec that itself carries the enumeration, ONE hop away — no marker, no manifest; `owns` itself is always given INLINE, never by pointer |
   | f | a dispatch to builder, or any dispatch whose `owns:` holds an absolute path (D-0022) | carries its manifest as HEADER LINES outside fences and quotes: `given:`, `owns:` (absolute paths, on that line or right under it, no blank line, no heading marks; a path with spaces in backticks), `non-goals:`, `handoff:`, `edges:`, `DoD:` (the verification command in backticks); `tools/dispatch_manifest.py` refuses it otherwise and names what is missing; the informed pass is a line `manifest-skip: <item>[, <item>] -- <reason>` |
   | h | critic/designer dispatch | report path on `handoff:`, never `owns:`; `tools/handoff_gate.py` lets it write only that file |

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
   the remainder goes to a fresh worker whole); ONE critic pass per topic (R13-g); critic-on-plan only as rule 3
   says, otherwise `critic: skipped` with the reason; a re-review carries only the fix diff and the verdict; the Lead
   compacts at ~300K at a stage boundary, a stage commit per 2–3 merges, journal notes ≤ 300 chars, CI through
   `tools/ci_read.py`; at most 6 parallel WRITING workers and a push before a worktree launch
   (`tools/dispatch_gate.py`). The cap counts ONLY builders writing code; designers, critics and scouts are never
   counted and never wait for a slot. The queue is kept FULL: whatever can run in parallel is launched at once — a
   session running 2–3 workers while independent work waits is the failure this line names. Detector: check 17.
13. Leaf routing (leaf-routing rule) — not used in this deployment: no judge is bound (`delegation.config.yaml`,
   role `judge`), so every task, leaf or graph, goes through the acceptance of rules 1-12 and Role ≠ tier; an
   acceptance with `basis: "judge"` is not legal here.

   | R13 | when | duty |
   |---|---|---|
   | g | integration (a merge into `main`) | parts of the SAME topic are merged TOGETHER through ONE critic pass (Cost gates, rule 12); a merge over roughly 100 lines carries that pass (rule 3) |

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
the task open. A task id is read by its IDENTITY `<id>@<label>`, the label being the writer's file slug
(`tools/journal_keys.py` is the one loader; session_context, forge_metrics and calibration_counts key by it); a
`closes:` token may carry the label (`closes:t-050@dev2`), a token with an unknown or malformed label closes nothing;
the GATE stays on bare ids. A merge that brings another clone's journal lines is form-checked at the merge
(`.githooks/pre-merge-commit`, `tools/journal_validator.py --merge-parent env`): a defective foreign line is accepted
only by a tail line of OUR side carrying `merge-accepts:<n>:<field>[,<field>]` (n = the line's number inside the
MERGE_HEAD block, as the refusal names it); the tail lines are anchored on HEAD's own last ts, so a foreign clock
ahead of ours never makes the door unusable.

Every event line — `journal_created` and `lead_degraded` included — carries five base fields checked by
`tools/journal_validator.py`: `ts`, `event`, `agent`, `category` and a non-empty `notes`. `ts` is ISO local time
with NO timezone suffix (a trailing `Z` fails the gate). `lead_degraded`'s `reason`/`scope` are legal extras; they
do not replace `notes`.

Typed fields (typed-fields rule: load-bearing facts go in fields, notes are a human-readable extra): `task_id` on
delegated/accepted/rejected/escalated/defect_found; `attempt` (number) and `failure_class`
(spec/capability/recon/tooling) on `rejected`; `witness` (the actual run output) on `accepted` for builder;
`worker_ref` on `delegated`; `ref` (the task_id of the original `accepted`) on `defect_found`; and on every new event
`feature: Fnn` — the factory feature it belongs to, from `plans/features.json` (`journal_validator` WARNs on a
missing or unknown id for events from 2026-10-02; `tools/forge_metrics.py` attributes by it first and by
tag/files/words only when it is absent; unclassified work is a Forge metric, not an error). Old events are never
rewritten. Issuing a task_id means re-reading the tail of the journal right before writing `delegated`:
max(t-NNN)+1, never an id remembered earlier; a collision noticed later is not rewritten — it gets a note on the next
event and counts as two tasks (no-silent-reuse rule). `ts` comes from the system clock read right before writing
(Get-Date or equivalent), never from the session's narrative; a wrong `ts` noticed later gets a note on the next
event (the reference: usage reports / git log, calibration check 13(f)). A MISSED event noticed later is repaired by
a RETRO pair: append `delegated`/`accepted` NOW, with the current `ts`, a "retroactive" mark and the event's actual
boundaries in `notes`; inserting lines into the past is forbidden; calibration watches the retro stream.

Event SHAPES — the typed fields each event adds on top of the five base fields:

| event | adds on top of the base fields |
|---|---|
| `delegated` | `task_id`, `model`, `worker_ref`; optional `node` — the pile node `<slug>/<N>/<id>` (`forge/5/F5-2`; `journal_keys.NODE_RE`; a bare id is never a node); a REPEAT on an open task is legitimate only as: a critic-entry / a retry with `attempt`>=2 after `rejected` / a `replaces_worker:<prev worker_ref>` bare token in `notes` |
| `accepted` | `task_id`, `model`, `by` (a bare tier word); + `basis` ("critic" / "queued-to-lead") when the acceptor is not strictly above the executor; + `witness` (the verbatim run output) on builder work |
| `rejected` | `task_id`, `model`, `by`, `attempt` (number), `failure_class` ∈ spec/capability/recon/tooling |
| `escalated` | `task_id` (must already exist earlier in the file), `model` |
| `defect_found` | `task_id`, `ref` (the task_id of the original `accepted`) |
| `dispatch_skipped` | reason inside `notes` (no extra field) |

The `model` field is mandatory on delegated/escalated/accepted/rejected — a self-declaration of Lead; calibration
reconciles it against transcripts, and a discrepancy is itself a calibration event. NEW lines are validated at TWO
points (`tools/journal_validator.py`): the pre-commit gate on `git commit`, and the WRITE moment — the PostToolUse
hook `journal_echo` re-validates the newest lines as they land and warns before the session ever reaches a commit.
Both share the checks: append-only, typed fields, ts-monotonicity, no ts from the future, task_id novelty — a repeat
`delegated` on an open task is legitimate only from a different tier (a critic-entry), as a retry with `attempt`>=2
after `rejected`, or as a DEAD-WORKER REPLACEMENT: a `replaces_worker:<previous worker_ref>` marker in notes (not a
retry, `attempt` does not grow; the handle literally matches the `worker_ref` of a prior `delegated` line of the same
task; the validator takes the first non-whitespace token after the colon, so trailing punctuation breaks the match);
`delegated` on a closed task is forbidden. New accepted/rejected carry `by`; `accepted` for
scout/builder/critic/designer is legitimate when tier(`by`) is above the tier of `agent`, OR with a `basis` field
"critic" / "queued-to-lead" (the acceptance matrix of Role ≠ tier, encoded); work performed by a non-Claude model
still carries a `basis` — the matrix compares FUNCTION tiers, not model ids. `by` and `model` differ on purpose: `by`
is a bare tier keyword from `TIER_ORDER` in `tools/journal_validator.py` (`haiku`/`sonnet`/`opus`/`fable`) — an
unknown `by`, a full model id (e.g. `"claude-opus-4-8"`) included, FAILS the matrix outright and no `basis`
legalizes it; `model` is free-form, and a full model id there is recommended. The validator's own failure detector is
a pair of calibration checks. Events: `delegated`, `accepted`, `rejected` (a failed attempt, rule 6), `escalated`,
`decomposable`, `dispatch_skipped` (reason mandatory), `defect_found` (a late defect in ACCEPTED work; agent = the
original tier, `ref` = the task_id of the original `accepted`, notes: what broke — the false-accept stream),
`lead_degraded`, `lead_restored`, `journal_created`, `calibrated` (a calibration run happened). The journal is the
evidence for the weekly calibration (PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md); DELEGATION_TABLE.md statuses move only
on this data (Update Rule 1); a calibration overdue by more than 7 days shows as a Last Calibration line in the Boot
Report.

## Role ≠ tier

Three definitions that are NOT synonyms:

- The TIER of a session = its ACTUAL model (verified at entry — tier-verification-at-entry rule). Fable is the MODEL
  NAME of the top tier; "Lead" is a tier-FUNCTION (decomposition, specs, acceptance, mechanisms), not a role in the
  conversation.
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
   entries are queued for the full Lead; acceptance follows the matrix of Role ≠ tier: equal/higher tier only with
   input from a tier above, or queued.
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

Every "custom" form of a command is a permission request to the operator. For all sessions and subagents here:

1. Tests — the canonical form, from the repo root: `python -m pytest tools/ -q`, or a narrower target; the full sets
   run on CI, not on this machine (PROJECT.md, package change p. 2).
2. The proxy server — not used in this deployment: the contour is subscription and nothing in gateway/ is run.
3. Don't prefix commands with `cd <dir> && ...` and don't append ` 2>&1` — both break the allowlist match.
4. File edits — only via Edit/Write tools (not `python - <<EOF`, not `python -c "...replace..."`).

   | pt.4 | when | duty |
   |---|---|---|
   | a | a NAMED, committed script with its output attached | legitimate: point 4's target is an ad-hoc, unauditable mutation, not a committed, reviewable one |
   | b | a `-c`/heredoc payload that is a pure calculation/read | outside this point's scope, the gate stays silent; a mutation, or an opaque payload, still gets a WARN |

5. Log entries — via an Edit/Write tool, not `printf` with `$(date)`.
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

7. Temporary corruption (a mutation probe, a red-probe, "corrupt and restore") is rolled back by a BYTE COPY, never
   by `git checkout` / `git restore`: (a) take the copy BEFORE corrupting, and restore FROM IT; (b) `git checkout` /
   `git restore` is legal only when `git status --porcelain -- <file>` was EMPTY before the corruption — check it,
   don't assume: skipping the check risks wiping another session's uncommitted changes to that file; (c) the
   rollback's witness is the VERBATIM output of the comparison (a hash or a diff), not the word "restored"; (d) a
   live artifact (a ledger, a registry, a money table) is not corrupted at ALL when a pure function's verdict proves
   the same point — corrupt a COPY of the tree instead.
````

What else could go if the measured size is over 40 000 bytes (each with its cost):
- the journal validator mechanics in «Routing log» (DEAD-WORKER detail, `by` format, merge door detail, ~2.0K) → the
  refusal texts of `tools/journal_validator.py` already name each door (cost: a session meets them only on a refusal);
- Lead degradation 4 a-c compressed to one sentence (~0.6K; cost: the ENTRY procedure becomes a pointer to check 5);
- the package paragraph of rule 10 reduced to a pointer to AR-29 / P27 (~0.8K; cost: `judgment:` line and census
  named only in PROJECT.md P27 and the architecture gate's refusal).

## §4 Bindings

(a) `tools/install_parity_anchors.json`, unit `routing-policy` — CHOSEN: rewrite the anchors (fork F1 lets the Lead
choose removal). Why: the gate's original class (an upgrade restoring old text, `tools/install_parity.py:4-12`) is gone
with the kit, but the class it also catches — a rule silently cut by an edit (a boot diet) — is exactly the owner's
«правила… не должны потеряться»; P31: every other policy carrier (role files, PROCESS) keeps its anchor unit, CLAUDE.md
must not be the one exception; and `tools/test_install_parity.py:1053-1078` (K4b) pins five markers from this unit
(«DRAFTING», «TWO-LAYER CRITIC ENTRY», «SCOPE OF THE WITNESS RUN», «DETERMINISTIC SCRIPT RUNS», «13. Leaf routing»), and
`:643` requires the shipped manifest to be CLEAN on the real tree. Removal would need: deleting K4b and its fixture test
(`:1062-1089`), a ledger row change, and leaves CLAUDE.md the only carrier without a loss guard.
Exact change: keep `unit_id`, `kit_path` ("toolkit/CLAUDE.md" — MUST stay: `test_manifest_covers_all_policy_carriers`
`:1001-1022` reports `missing` when host_path CLAUDE.md is in the manifest under any other kit_path), `host_path`,
`kind`; replace `anchors` with this list (each is a literal substring of ONE line of §3; the fixture
`tools/fixtures/host_pre_delivery_CLAUDE.md` lacks all five K4b markers — grep, positive control «DoD in every dispatch»
found at :266):

```json
["CLAUDE.md — QA Factory development", "Tiers (see DELEGATION_TABLE.md; all assignments are estimates until calibrated)",
 "Routing rules", "1. Recon → scout by default:", "not used here: no scout exam set is registered",
 "spot-verifies at least one load-bearing claim", "2. Implementation from a finished spec → builder.", "DRIVING the UI;",
 "enforcement file (a hook on the active hooks path", "DRAFTING → designer BY DEFAULT", "3 OR MORE numbered items",
 "CONTEXT", "PRIMARY draft. A RESUBMISSION", "NEW task_id is a NEW task", "3. critic — a MANDATORY acceptance gate:",
 "`docs/tasks/critic-diff-brief.md` items 6-7", "TWO-LAYER CRITIC ENTRY", "starts with EMPIRICS", "Critic-on-plan:",
 "4. Independent parts → several parallel subagents,", "SCOPE OF THE WITNESS RUN:", "scenario_walk.py --witness-for <owns>",
 "the BATCH CANON:", "4a. A task spanning 5 or more journal events,", "ONE taker per batch, frozen once taken;",
 "5. Flat delegation (flat delegation rule):", "6. Escalation: 2 failed attempts,", "7. Background execution by default",
 "with the worker's model:", "REQUIREMENT closes by MEASUREMENT,", "8. Universal skip rule:", "ROUTING MOTIVE",
 "SMALL-WORK BATCHING:", "SELF-EXECUTION ONLY on the FIRST", "IMMEDIATE SOLO builder dispatch", "DETERMINISTIC SCRIPT RUNS:",
 "9. Fix the class, not the instance (fix-the-class-not-the-instance", "sweep-the-artifact-first rule",
 "10. Four questions for every mechanism", "axis-enumeration rule", "tier-declaration rule",
 "A change to the package (D-0055, D-0060; P27)", "11. DoD in every dispatch (DoD-in-every-dispatch rule):",
 "the spec NAMES ITS EDGE BEHAVIOR:", "(i) TEMPORAL", "Which tests a DoD asks for", "SCOPE CEILING:", "QUARANTINED",
 "CONTEXT MANIFEST", "DECLARATIVE on reads and", "FIVE-POINT CHECKLIST", "AND the edge behaviors NAMED",
 "DOC-DISPATCH WITNESS:", "a WRITING dispatch's \"given\" manifest", "given INLINE, never by pointer",
 "`tools/handoff_gate.py` lets it write only that file", "11a. Question routing (question-routing rule):",
 "12. The coordinator's cadence runs on LARGE moves,", "Cost gates (D-0035, D-0038, D-0040, D-0054;",
 "13. Leaf routing (leaf-routing rule)", "parts of the SAME topic are merged TOGETHER", "Routing log — logs/journal/<dev>.jsonl",
 "ACCOMPLISHED FACTS,", "ISO local time", "DEAD-WORKER REPLACEMENT:", "Role ≠ tier", "MODEL", "ROLE = ROUTING,",
 "ESCALATES UPWARD", "Lead degradation", "1. Drop one tier (upper-mid, then mid: Opus, then Sonnet)",
 "2. While degraded:", "3. Default return at the task/session boundary:", "4. Tier verification at BOTH points",
 "ENTRY — before the FIRST", "EXTERNAL CROSS-CHECK", "Command hygiene (permission hygiene)",
 "1. Tests — the canonical form, from the repo root:", "2. The proxy server — not used in this deployment",
 "3. Don't prefix commands with `cd <dir> && ...`", "4. File edits — only via Edit/Write tools",
 "a NAMED, committed script with its output attached", "outside this point's scope, the gate stays silent",
 "5. Log entries — via an Edit/Write tool,", "6. An environment-negative claim requires verification:",
 "-E; -P needs a UTF-8", "a project decision rests on an UNKNOWN property of the environment",
 "valid ONLY by reading the carrier directly (the Read tool)", "7. Temporary corruption", "BYTE COPY,", "FROM IT;"]
```

The builder VERIFIES each anchor after pasting: `python tools/install_parity.py --check` → `MISSING (0)` and `UNKNOWN
(0)`; any anchor that a line break split is shortened to its on-line part (a report line names it). Old→new spot map of
the 49 clause anchors: every old CAPS phrase has its new row above except the judge ones («LEAF closes under ONE», «BY
DEFAULT» (rule 13), «CALIBRATED JUDGE», «does NOT replace the critic gate at INTEGRATION») — dropped with rule 13 (§2
13.2, R13-g) — and «OR attached in FULL» (replaced: 11.17 now reads «attached in FULL source … never committed»).
Other units quoting rule numbers (designer.md «the text is CLAUDE.md rule 11», judge.md «(rule 13)»,
JUDGE_CALIBRATION_PROTOCOL «8. … (leaf-routing rule 13)», WEEKLY_CALIBRATION «1. **Rules 1/2/8», «20. **Leaf-routing
judge acceptance (rule 13)»): their anchors are matched against THEIR OWN files, which this spec does not change → no
edit. `docs/ADOPTION_LEDGER.md`: row :83 Basis → «the project's own text since t-013 (the owner's word 11.11.2026): no
BEGIN/END block, host adaptations folded into the rules (map: docs/CLAUDE_HOST_ADAPTATIONS_FULL.md); imports PROJECT.md,
FACTORY_RULES_INDEX, ARCHITECTURE_INDEX; anchors rewritten to the own text» (status stays `adopt`, so a lost anchor stays
red — `install_parity.py:470-485`); row :84 «extended by host adaptation 2» → «extended (D-0021; CLAUDE.md rule 2 points
to it)»; row :86 `logs/routing-log.jsonl` → `logs/journal/<dev>.jsonl`; row :90 «host adaptation 3 (D-0022)» → «D-0022».
No test pins those ledger texts (the K4b fixture ledger is built inline, `test_install_parity.py:1068-1071`).

(b) `tools/tests/test_role_carriers_one_owner.py`. OWNER_KEYS for CLAUDE.md (:45-49) — all survive verbatim in §3
(squashed, case-folded):
- routing:rule-11 → §3 rule 11: «a spec silent on an edge that its / own requirements create is a dispatcher defect» ✓
- routing:hygiene-6 → hygiene 6: «from an INCORRECTLY / invoked tool is a miscall, not proof the object is absent» ✓
- routing:rule-9 → rule 9: «the rule against recurrence goes on the / highest level that ties the siblings together» ✓
- cost:cap → rule 12: «(WARN 250K, STOP 400K;» ✓  - cost:queue → rule 12: «The queue is kept FULL» ✓
POINTERS: anchors HYGIENE_6 «6. An environment-negative claim requires verification: empty output» ✓ (hygiene 6 first
line), «11. DoD in every dispatch (DoD-in-every-dispatch rule)» ✓, «9. Fix the class, not the instance
(fix-the-class-not-the-instance» ✓, CLAUDE.md carrier pointer «`docs/tasks/critic-diff-brief.md` items 6-7» ✓ (rule 3).
MUST change: `COST = "6. Cost gates (D-0035"` (:31) → `COST = "Cost gates (D-0035, D-0038, D-0040, D-0054;"`; POINTERS
:57 and :72 pointer «host-адаптация 6 `CLAUDE.md`» → «`CLAUDE.md` rule 12, Cost gates»; :69 «the rule text is
`CLAUDE.md` host adaptation 6» → «the rule text is `CLAUDE.md` rule 12, Cost gates»; the three carriers change in the
same commit: `plans/builder-rules.md:82` («— host-адаптация 6 `CLAUDE.md` (D-0035, D-0038)» → «— `CLAUDE.md` rule 12, Cost
gates (D-0035, D-0038)»), `docs/RUNBOOK.md:230` (same replacement), `docs/CLAUDE_HOST_ADAPTATIONS_FULL.md` (f).
Constraint: no other scanned file may restate an OWNER key — the new FULL doc must not quote «WARN 250K, STOP 400K» or
«queue is kept FULL».

(c) Imports: §3 keeps the three whole-line `@` imports in the order PROJECT.md, docs/FACTORY_RULES_INDEX.md,
docs/ARCHITECTURE_INDEX.md → `tools/test_session_context.py:1179-1183` stays green unchanged.

(d) `tools/session_context.py:207` `CLAUDE_WARN`: re-derive by its own rule (:203-206): `ceil(size * 1.15 / 100) * 100`
with the size the builder MEASURES after pasting (estimate ~37 000 → ~42 600; not my number). Update the comment block
:194-206 to the new measurement (date, bytes, formula result). Tests pinning the literal 56100:
`tools/test_session_context.py:898, 916, 939, 954, 998` (output strings) → write `{sc.CLAUDE_WARN}` in the f-string
instead of the literal; `:1014` tuple → drop the `sc.CLAUDE_WARN` element (a pin of a measured constant, `docs/TESTING.md`
table «Пин измеренной константы»; the two boot thresholds stay). `BOOT_BUDGET_LIMIT` / `BOOT_BREACH_THRESHOLD` (100000,
:181-182) untouched — the owner's number (fork F9). Expect the boot total ≈ 147 868 − ~21 000 ≈ 127 000: still over
100 000 (snapshot :10; estimate).

(e) Onboarding skill `.claude/skills/onboarding/SKILL.md` «## Upgrade mode» (:331) — add one paragraph right under the
heading: «Not used in this repository: CLAUDE.md is the project's own text since 11.11.2026, there are no BEGIN/END
markers and nothing more is pulled from the kit (the owner's word); do not run this mode here — its step 6.5 would insert
markers and its step 6.2 would overwrite the own text.» Markers: removed from CLAUDE.md (no code reads them, §2 B0).
Fork F6.

(f) Pointers. `docs/CLAUDE_HOST_ADAPTATIONS_FULL.md` rewritten: title «CLAUDE.md — history of its clauses»; a map table
«host adaptation N → where it stands now» (1 Tiers; 2 rule 2 → designer.md rule 1; 3 R11-f; 4 Routing log typed fields;
5 rule 3; 6 rule 12 Cost gates (+ rule 3 critic-on-plan, R13-g); 7 rule 4a; 8 R11-h; 9 and 10 rule 10; 11 and 12 rules 4
and 11); the reasons of 5 and 6 kept as they are (:12-21, with «the rule text is `CLAUDE.md` rule 12, Cost gates»);
adaptation 7 in full kept (the trimmed ↔ full pair now = rule 4a ↔ this text; skill boot-diet step 4); a line: «what was
dropped and why: rule 13 judge text, R1-a, hygiene 2, the journal-segments clause — t-013 §2». Other live carriers:
`.claude/agents/designer.md:33` «host adaptation 10» → «CLAUDE.md rule 10»; `docs/tasks/critic-diff-brief.md:6` «host
adaptation 5» → «CLAUDE.md rule 3»; `docs/TWO_VOCABULARIES.md:11,17` «host adaptation 1» → «CLAUDE.md Tiers»;
`docs/SIBLING_MAP.md:31-32` (journal path → `logs/journal/<dev>.jsonl`; drop «the one reader of
`logs/journal-segments.json`», keep the key `<id>@<label>`), `:468,474,477,479,480,490` («host adaptation 2/6», «host 5/6»,
«host adaptations» → «rule 2 → designer.md 1», «rule 12 Cost gates», «rule 3»); `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md:964`
«CLAUDE.md host adaptation 7» → «CLAUDE.md rule 4a», `:362-366` SECOND SIGNATURE «covering the test FILE that judges each
path in its OWN `owns`» → «covering what `scenario_walk.py --witness-for <its owns>` prints (rule 4)». Left as they are,
resolved by the map: `DECISIONS.md:29` (a record), `tools/forge_metrics.py:16,1150` (comments),
`ai-packages/qa-factory/scripts/acceptance.py:659` (package comment — no package commit for a comment),
`docs/tasks/pre-release-0.9-brief-common.md:42`, `plans/team/team-work-plan.md:254` (historical).

(g) `AGENTS.md`: `python tools/agents_md.py` after every source above is final, then `python tools/agents_md.py --check`
→ exit 0; committed in the same commit (its copy of the BEGIN/END markers disappears with them).

(h) The commit (ONE commit, §5 E5; made by the Lead — CLAUDE.md, designer.md, the skill, SIBLING_MAP, PROCESS and
session_context.py are mechanism paths, `tools/mechanism_gate.py:211-222`, left uncommitted by a builder per
`plans/builder-rules.md` 2). Message lines: `tier: fable`; `architecture: none -- forge-only`; the pile line or
`piles-skip: t-013 -- <reason>`; the four questions — (a) cost: one rewrite and one anchor list now; every session pays
~21K fewer boot bytes; (b) the axis block below; (c) detectors: `install_parity.py --check` in forge-check (a lost rule
anchor is red), `test_role_carriers_one_owner.py` (keys and pointers), the boot-budget line of SessionStart and
calibration check 10; (d) code on the path: forge-check CI, mechanism_gate in commit-msg, agents_md `--check`.
Axis block (one mechanism set: «policy rewrite + anchors + CLAUDE_WARN + Upgrade-mode stop line + pointers»):
axis 1: covered — CLAUDE.md ↔ designer.md pointer ↔ journal path; binding untouched
axis 2: n/a — no exam instrument changes (judge protocol untouched, rule 13 not used)
axis 3: n/a — no package file changes
axis 4: n/a — FR, debt, backlog, principles untouched
axis 5: n/a — package stage twins untouched
axis 6: n/a — measurers untouched
axis 7: n/a — test identity untouched
axis 8: n/a — story-location resolver untouched
axis 9: n/a — test-file recognizer untouched
axis 10: n/a — git-top readers untouched
axis 11: n/a — shell tokenizer untouched
axis 12: covered — rule 4a carries the pile rules unchanged in meaning; carriers untouched
axis 13: n/a — dispatch text form (R11-f) unchanged
axis 14: n/a — transcript readers untouched
axis 15: n/a — console setup untouched
axis 16: n/a — JSON reader untouched
axis 17: n/a — detector verdict shape untouched
axis 18: covered — CLAUDE_WARN lowered (a shrink), not raised
axis 19: n/a — tools: line readers untouched
axis 20: n/a — host receipt names untouched
axis 21: n/a — markdown table readers untouched
axis 22: n/a — host return forms untouched
axis 23: n/a — tests[] row fields untouched
axis 24: n/a — execution record join untouched
axis 25: n/a — freshness predicates untouched
axis 26: n/a — waiver constant untouched
axis 27: n/a — test-row profile untouched
axis 28: n/a — row-form render site untouched
axis 29: n/a — jsonl appenders untouched
axis 30: n/a — profile commands untouched
axis 31: covered — owners keep their keys; three pointers reworded with the POINTERS rows in the same commit
axis 32: n/a — no package check added; rule 10 text of AR-29 unchanged in meaning
axis 33: n/a — dispatch identity untouched
axis 34: covered — the rule/cancellation pairs removed; the remaining two-road place is fork F5 with its residual node
axis 35: n/a — story sides untouched
axis 36: n/a — substitute rows untouched

## §5 Edges (each with the invariant it protects)

E1 — a pointer elsewhere to «host adaptation N» after the list is gone. Behaviour: live rule carriers reworded (§4f);
records, code comments, the package comment and historical docs keep the number and resolve through the map table in
`docs/CLAUDE_HOST_ADAPTATIONS_FULL.md`. Invariant: every pointer resolves in at most one hop; a test-pinned pointer
(POINTERS) and its carrier change in the same commit, so `test_pointer_resolves` never meets one side alone.

E2 — a gate message citing «CLAUDE.md rule 11» / «command hygiene point 6» / «rule 6a» when the wording changed but the
number did not. Behaviour: numbers and the duties under them are unchanged, so messages stay; no gate text quotes the
replaced wording except `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md:362-366` (reworded, §4f) — grep for «test FILE that
judges», «AT and BEYOND», «SCOPE CEILING», «proxy server» outside history found only that line, code comments «rule 6a»
(a dispatch_gate rule, not CLAUDE.md) and `tools/hygiene_gate.py:106` (a comment on gateway/, harmless). Invariant: a
number never points at a different duty than before.

E3 — kit text and adaptation in conflict where the adaptation did not settle it:
(a) critic-on-plan: rule 3 (kit) protects «no plan reaches the build without a feasibility review»; adaptation 6
protects cost («one critic pass»); PROJECT.md (11.11) makes it mandatory for a new idea and for a meaning-changing spec
edit. Behaviour in §3: any of the triggers fires the review; else `critic: skipped, <reason>`. Fork F10.
(b) rule 4 witness for paths outside the package: adaptation 12 says «what scenario_walk prints», but for a forge path
it prints «no scenario or keep row covers … run the whole scenario layer» (`scenario_walk.py:920`), which PROJECT.md p. 2
contradicts («свидетель — тест инструмента»). Invariant: a node's witness judges the paths it owns and never runs the big
neighbours. Behaviour in §3: the test file that judges the path, named in the DoD. Fork F5 (P31).
(c) rule 11a «headless substitute only as a named clause» vs PROJECT.md owner-away paragraph: §3 names that paragraph as
the clause. Invariant: no tier silently decides intent; an absent owner never blocks the night. Fork F11.

E4 — the judge files stay (`.claude/agents/judge.md`, `gateway/`, `PROCESS/JUDGE_CALIBRATION_PROTOCOL.md`, the escape
pin `tools/escape_allowlist.json` judge_role_pin) while rule 13 says «not used». Behaviour: they stay dormant, their
parity units stay green (their anchors are in their own files), ledger row :99 stays `deferred(trigger: calibration
run)`. `tools/journal_validator.py` still accepts `basis: "judge"` — the code over-permits relative to the rule.
Invariant: no acceptance with `basis: judge` counts here — the rule refuses it, and the detector is calibration check 20
(a judge acceptance in the window is a finding). Removal of the files is fork F8.

E5 — temporal: between the CLAUDE.md change and the anchors change CI must not be red. Behaviour: ONE commit carrying
CLAUDE.md, the manifest, the ledger rows, the one-owner test and its three carriers, session_context + its test,
the pointer edits, AGENTS.md. Why: `install_parity.py --check` runs on every push and PR head
(`.github/workflows/forge-check.yml:92,95`) and `test_install_parity.py:643` requires CLEAN on the real tree; a split
would need a `parity-skip:` door on the first commit AND would leave the one-owner test red in between (POINTERS ↔
COST). Before the commit: the old manifest is green on the old text; after: the new manifest on the new text.

E6 — FG7-14 in parallel: it owns `CLAUDE.md` too (`batch-7-vhodyashchie-4.md:37`). Behaviour: FG7-14 waits for t-013's
commit (an `очередь: t-013 → FG7-14` line when its batch is taken); rule 7's label clause is pasted verbatim so its diff
applies. Invariant: one writer of CLAUDE.md at a time.

E7 — empty/absent inputs of the bindings: if `tools/dev.config.yaml` is absent, `journal_keys.py where` already refuses
with its door (unchanged code); if the measured size makes `CLAUDE_WARN` higher than 56100 (size > ~48 700), do NOT
raise it — report the size and the §3 «what else could go» list (raising a ratchet needs the owner's word, axis 18).

E8 — the R1 table row a keeps its id with a «not used» line; if a scout exam set is ever registered, R1-a needs a new
decision (nothing returns from the kit automatically). Invariant: no digest is accepted on trail coverage alone while
no exam pass exists.

## §6 Nodes and acceptance keys

N1 (builder, sonnet) — owns: `C:\QAFactory\forge-repo\CLAUDE.md`, `C:\QAFactory\forge-repo\tools\install_parity_anchors.json`,
`C:\QAFactory\forge-repo\docs\ADOPTION_LEDGER.md`, `C:\QAFactory\forge-repo\tools\tests\test_role_carriers_one_owner.py`,
`C:\QAFactory\forge-repo\plans\builder-rules.md`, `C:\QAFactory\forge-repo\docs\RUNBOOK.md`,
`C:\QAFactory\forge-repo\docs\CLAUDE_HOST_ADAPTATIONS_FULL.md`, `C:\QAFactory\forge-repo\tools\session_context.py`,
`C:\QAFactory\forge-repo\tools\test_session_context.py`. These are bound by tests to one another (anchors, keys,
pointers, size), so one node. Steps: paste §3; measure the size; anchors (§4a); ledger rows; test constants; three
carriers; FULL doc; CLAUDE_WARN. Witness: `python tools/install_parity.py --check` (MISSING 0, UNKNOWN 0);
`python -m pytest tools/tests/test_role_carriers_one_owner.py tools/test_session_context.py tools/test_install_parity.py -q`;
the size line; `scenario_walk.py --witness-for <owns>` prints «no scenario or keep row covers» for these forge paths —
a report line, not a run (builder-rules 7b; fork F5).
N2 (builder, sonnet, parallel to N1, disjoint) — owns: `C:\QAFactory\forge-repo\.claude\agents\designer.md`,
`C:\QAFactory\forge-repo\docs\tasks\critic-diff-brief.md`, `C:\QAFactory\forge-repo\docs\TWO_VOCABULARIES.md`,
`C:\QAFactory\forge-repo\docs\SIBLING_MAP.md`, `C:\QAFactory\forge-repo\PROCESS\WEEKLY_CALIBRATION_PROTOCOL.md`,
`C:\QAFactory\forge-repo\.claude\skills\onboarding\SKILL.md`. Witness: `python tools/install_parity.py --check` (the
designer/PROCESS units' anchors untouched → still present); `python -m pytest tools/tests/test_role_carriers_one_owner.py
-q`; Grep «host adaptation» over the live carriers of §4f → only the «left as they are» residuals.
Lead after both: `python tools/agents_md.py` + `--check`; the one commit (§4h); push; CI forge-check is the batch canon.

Acceptance keys for the critic-on-plan:
K1 every KEEP row of §2 is found in §3 with its duty intact (row by row; the critic samples ≥ 15 rows across all sections
and all FOLD rows).
K2 no DROP row removes a duty this deployment still performs (each DROP's fact is checked on its carrier).
K3 every host adaptation 1-12 stands in §3 in its operative wording; no rule and its cancellation are both present.
K4 every rule number, sub-number and table-row id of the old block is present in §3, in the same order.
K5 every anchor of §4(a) is one-line text of §3 and the five K4b markers are present; kit_path unchanged.
K6 OWNER_KEYS and POINTERS hold as §4(b) says; no other scanned file restates a key.
K7 the forks are open (none silently closed in §3 beyond the marked recommendations F2-F5, F7, F10, F11).
K8 P31: no language/project exception; F5 named with its residual node.
K9 the byte count is measured, and the CLAUDE_WARN value follows the formula and never rises.

## §7 Forks (returned; recommendation; executable before the answer)

F1 — unit `routing-policy`: (A) rewrite anchors to the own text; (B) remove the unit (+ delete K4b tests, ledger row to
native-equivalent). Rec: A (loss guard for unchanged rules; P31 with the other carriers). Executable: A as written.
F2 — R13-g: (A) keep the row as «same topic merged TOGETHER through ONE critic pass at integration» (judge cumulative
clause dies); (B) row «not used», and the one-pass-per-topic duty lives only in Cost gates (reword adaptation-6 text
«(R13-g)»); (C) extend the cumulative clause to critic-skipped merges (adds a demand — outside the non-goals). Rec: A.
F3 — Cost gates placement: (A) one paragraph in rule 12, rules 3/4 point there; (B) split into rules 3, 4, 12. Rec: A
(one owner block; one COST anchor; check 17 reads one place). Executable: A.
F4 — R1-a: (A) id kept, one «not used» line; (B) verbatim, dormant. Rec: A (a dormant condition is what the owner asked
to remove). Executable: A.
F5 (P31) — witness of an owned path outside the package: the one-road option is that `scenario_walk.py --witness-for`
answers for every path (a forge path → its judging test, e.g. a default `tools/x.py → tools/test_x.py` plus data rows);
cost: one node in the package (scenario_walk + test-layers rows or a forge-side map), architecture line, a scenario row.
Until then §3 names «the test file that judges the path, named in the DoD» (PROJECT.md p. 2). Rec: the one road, as a
residual node (owns `ai-packages/qa-factory/scripts/tests/scenario_walk.py`, test: a `witness_for` table row for a
forge path); the Lead takes it to the owner.
F6 — onboarding Upgrade mode: (A) a stop paragraph; (B) delete the section; (C) untouched. Rec: A (cheap, prevents the
marker re-insertion; the skill stays whole). Executable: A.
F7 — rule 4a carrier: (A) a pile's batch file OR docs/tasks/; (B) docs/tasks/ only (duplicate DAGs for pile work).
Rec: A (PROJECT.md: batch files are node graphs). Executable: A.
F8 — judge files: (A) keep dormant (ledger deferred); (B) remove judge.md, gateway/, the protocol, pins, units — a node
of its own. Rec: A now; B only by the owner's word («судью убрать» was said of the text). Executable: A.
F9 — `BOOT_BUDGET_LIMIT` 100000: (A) untouched; (B) the owner sets another number. Rec: A. Executable: A.
F10 — critic-on-plan triggers: (A) union — forks / schema / money OR a new idea OR a meaning-changing spec edit; (B)
adaptation 6 alone. Rec: A (both are the owner's words; the newer 11.11 one adds cases). Executable: A.
F11 — rule 11a's named clause for an absent operator = PROJECT.md owner-away paragraph: (A) name it; (B) leave 11a
unnamed. Rec: A (a reader otherwise meets «work waits» and «no blocking questions» unreconciled). Executable: A.

### Answers to the forks (Lead, 11.11.2026)

- The owner, in chat: F8 = A («Оставить спящими») — the judge's files stay dormant; only the text of rule 13 goes.
- Decided by the Lead on the designer's recommendation (technical; told to the owner the same turn, she may reverse any):
  F1 = A, F2 = A, F3 = A, F4 = A, F6 = A, F7 = A, F10 = A, F11 = A.
- F5 = the one road as a residual node: forge/7 FG7-15
  (`plans/piles/forge/findings/20261111-svidetel-dlya-putej-vne-paketa-odin-put.md`); until it lands §3 stays as drafted.
- F9 — open: `BOOT_BUDGET_LIMIT` is the owner's number; she decides after the final size is measured.
- Measured by the Lead: §3 is 44 340 bytes (the estimate was ~37 000); the 40 000 target is not met — key K7 of the
  critic-on-plan names what else can go.

## Small choices closed by the designer

- Rule 7's «haiku: …» label example kept verbatim beside «No tier runs on Haiku» (non-goal; FG7-14 rewrites it).
- `feature` added to the journal example line (adaptation 4 made visible where the form is taught).
- `docs/RELATED_WORK.md` named instead of «the RELATED_WORK section» (the file exists).
- Class labels kept only where other files cite them (grep: role-vs-tier, trail-based, witness rule, flat delegation,
  dispatch-context-manifest, question-routing, tier-verification-at-entry, background-by-default, no-silent-reuse,
  axis-enumeration, enforcement-file, self-certification, typed-fields, code-gates-execution, four-questions,
  tier-declaration, sweep-the-artifact, two-layer review, boot-context-is-expensive, cheapest-tier-default, two-pass
  external, leaf-routing); dropped: «silent-skip violation class», «large-cadence rule», «facts-not-intentions rule»,
  «mechanism-recognition rule» (no citer outside CLAUDE.md, anchors and history).
- Spelling «neighbor» kept (the literal «no neighbors: <why>» may be matched by a reader).
- The `TIER_ORDER` list keeps `haiku` (a fact of `tools/journal_validator.py:276`).

## Noticed analogs (reported, not widened)

- `docs/ADOPTION_LEDGER.md:125-146` and the skill's step 7 say a «Parity waiver» row makes an absent anchor legitimate,
  but `install_parity.py:470-485` reads only the FIRST matching ledger row's status; waiver rows never decide.
- `logs/routing-log.jsonl` is absent, yet named as a live path by `tools/r3_integration_check.py:4,38`,
  `tools/claim_control_gate.py:265`, `tools/journal_keys.py:61` (default), `.githooks/pre-commit:6` (comment).
- `.claude/agents/scout.md:56-60` requires running `PROCESS/SCOUT_GOLDEN_SET.md`, which does not exist.
- `plans/builder-rules.md:21-22` keeps «Пока перевод в карантин не выполнен…» though `test-layers.json:5379` has
  `quarantine` rows (the clause is dead).
- `docs/SIBLING_MAP.md:481` names «`.gitlab-ci.yml` header» (the CI is GitHub now).
- `tools/journal_validator.py:168` WARNs on `feature` only for delegated/accepted/defect_found, while adaptation 4 says
  «every new event».

## Reading trail

CLAUDE.md:1-865 (whole, on disk); compact snapshot 2026-11-11 (whole); tools/install_parity_anchors.json (whole);
tools/install_parity.py (whole); tools/test_install_parity.py:1-60,340-394,630-652,900-1090; tools/tests/
test_role_carriers_one_owner.py (whole); tools/test_session_context.py:1000-1019,1165-1194; tools/session_context.py:
170-219,1165-1189; Grep CLAUDE_WARN/56100 in tools/; docs/ADOPTION_LEDGER.md (whole); .claude/skills/onboarding/
SKILL.md:360-419 + headings; docs/CLAUDE_HOST_ADAPTATIONS_FULL.md (whole); delegation.config.yaml (whole); docs/
SIBLING_MAP.md:1-45,461-500 + axis headings; docs/TESTING.md (whole); plans/builder-rules.md:1-74 + :82; docs/
RUNBOOK.md:228-231; tools/journal_keys.py:1-58,684-733 + grep; logs/journal/dev1.jsonl:1; Glob logs/*, logs/journal/*,
PROCESS/*, **/routing-log*.jsonl (positive control **/dev1.jsonl), **/*GOLDEN*, **/*CRITIC_EXAM* (positive control
**/*JUDGE_CALIBRATION*); tools/mechanism_gate.py:195-244; tools/agents_md.py:1-60; tools/r3_integration_check.py:1-40;
.github/workflows/forge-check.yml:89-98; tools/test_workflows.py grep; PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md:76-98,
354-373,958-967; .claude/agents/scout.md:50-69; scenario_walk.py grep (:14,:887-931); test-layers.json grep :5379;
tools/journal_validator.py:168,276; tools/escape_allowlist*.json grep; plans/piles/forge/batch-7…:37, README.md:192;
greps: «host adaptation|host-адаптац» (live carriers), class labels, «BEGIN|END supervised», «rule 13|R13», old-wording
phrases, fixture markers (positive control «DoD in every dispatch»).

Needed beyond the manifest: tools/test_install_parity.py (K3/K4b pins), tools/journal_keys.py, scenario_walk.py,
r3_integration_check.py, forge-check.yml, WEEKLY_CALIBRATION_PROTOCOL.md, scout.md, test-layers.json, batch-7 FG7-14 row.
