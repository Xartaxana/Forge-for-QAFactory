# Stage critics: S2/S3 removed (Part A); S6/S7 consumer acceptance gets one chance and is never a barrier (Part B) — designer draft, fix round 1

Status: DRAFT by designer for Lead acceptance, 13.11.2026; FIX ROUND after the critic-on-plan verdict
`docs/tasks/specs/reviews/20261113-stage-critics-removed-plan-critic.md` (fit_with_fixes). Every blocker and fix is answered in §R.
Forks are returned in §F; nothing below is accepted until the Lead says so.
Package tree read: `C:\QAFactory\forge-repo\.claude\worktrees\read-main\ai-packages\qa-factory` (origin/main AFTER wave 3, past 12317b6;
every line the verdict corrects was re-read there in this round — §T). Every `file:line` below is on that tree under
`ai-packages/qa-factory/` unless another path is given; a builder finds functions by NAME (lines may drift). Package text English (FR-30).

## §0. The owner's words (13.11.2026, verbatim) and the Lead's readings

- On the stage critics 0.11.0 added (D-0060 part B): «в таком варианте мы только увеличиваем время прохода стори и количество барьеров.
  Убираем лишних кртиков, оставляем как раньше»
- On the S2 critic's checks (units of text nobody turned into a requirement; a compound requirement hiding two behaviours; silence about
  a boundary; a statement lifted from the diff recorded as a requirement (P20); reading the author's `tried` table): «эти проверки
  переносим к критику кейсов когда он смотрит кейсы, если там их ещё нет»
- On the S3 critic's checks (a requirement with no row and no reason for "not tested"; a level higher than the risk needs (P16, P19); a
  row with no defect hypothesis; a branch of the diff no row walks): «это отдать самому автору плану, пусть это будет напоминалка автору»
- On S6/S7 acceptance by the consuming role, first: «это нормально»; then (scope addition, relayed by the Lead): «это не должно быть
  барьером. Но если использовать данные для дальнейшей работы нельзя, то можно даль один шанс их переделать (но все требования должны
  быть у автора изначально)»

**Lead's reading (the owner may correct it):** «не должно быть барьером» = when the one round is spent, or the consumer's verdict cannot
be read, or the rounds cannot be counted, the consumer does NOT go to the conductor seam and no person is asked: the stage is accepted by
the driver with a named GAP, the consumer goes on with what it has, and the gap reaches the report / gate B as a factory defect (Part B,
B2). «один шанс» = one repair round, not two. Marked here as the Lead's reading so the owner can correct it.

Goal. After this work the factory has a critic only on test cases (S4, `qa-case-critic`) and on automation code (S5, `qa-code-critic`);
S2 and S3 close on their author's finish as before 0.11.0; S4 and S5 acceptance do not change; S6/S7 acceptance by the consumer stays as
a mechanism with ONE return and no barrier.

Non-goals (from the brief): S4 and S5 acceptance; the S5/S7 repair-limit road (`repair_limit_gate`, `s7.repair_limit`); restoring any code
refusal; any new question to a person.

## §1. Package header (designer rule 1; CLAUDE.md rule 10, P27, AR-29)

### 1.1 AR-n touched and how each is kept (the change check goes into the node DoDs)

| AR | how it is touched | how it is kept | change check (node) |
|---|---|---|---|
| AR-1 closed variety is data | which stages have an in-stage acceptor; which earlier stages' artifacts the S4 acceptor reads; the consumer round cap | `references/stages.json` rows (`acceptance_by` and the critic leave S2/S3 `roles`; new S4 key `acceptance_reads`; new S6/S7 key `acceptance_rounds`), read by key, never by a stage or role name in code. RESIDUAL: `brief_pack.TRIED_READERS` (`brief_pack.py:112`) is closed variety in code and gains one row (B-1, Lead decision 1); its move into `stages.json` is ONE queue line for the Lead (§Q) | A1a W1 row; B1 rows C1-C6 |
| AR-13 one reader | the cap of a repair loop; "accepted with a gap"; the stage author of a ticket re-run | one new reader `runtime_policy.repair_cap` replaces the four inline `policy.get("design_repair_cycles" if "case" in role ...)` sites; the gap quote prefix `GAP_PREFIX` lives beside `BY_PERSON` in `driver_core.py:411` and is read in `consumer_close_words` like `BY_PERSON` (F-7); `ticket_rework_step` reads the author as `stages.json` `roles[0]` for every stage (B-4a) | B1 grep in DoD; B2 rows; A1a T4 |
| AR-14 one writer | the gap record; the gap warning | the existing writer `stage_done.py --acceptance ... --acceptor driver` (one writer of `pipeline["acceptance"]`) and `stage_done.py --warn` (one writer of `pipeline["warnings"]`, `stage_done.py:178-190`) — see fork F6 for how the two are called | B2 rows |
| AR-15 one survivor | the hand-over of an earlier author's form; the gap to the report | the form travels by the ONE existing table `TRIED_READERS` / reader `tried_reader_names` (`brief_pack.py:3636-3644`) — no `author_form` part (B-1); the gap travels by the ONE existing warnings road (`stage_done.py --warn` -> `brief_pack.py:1819-1824` -> scribe; `gate_brief.py:2362` -> gate B) — no second reader of acceptance records (B-3) | A1a J1; B2 G6 |
| AR-17 one seam | S6/S7 no longer reach `stage_review_exhausted`; S4 still does | the seam is untouched; only its S6/S7 callers stop calling it; its then-dead S6/S7 branches are removed by residual node R1 after FV1-6 (F-3) | B2 row G4; R1 |
| AR-19 stage twins | S2, S3, S4 were one route (X2-7); S6, S7 one consumer table | S2 and S3 leave together (same commit, A1a); S6 and S7 change together through `CONSUMER_ROUTES`; S4 keeps its own route | A1a W-rows; B rows at S6 and S7 |
| AR-20 shrink-only ratchets | `judgment-census.json` (`ratchet` line), `driver-layers.json` rows, `role-load.json` (`ratchet_tokens`, `process_ratchet_tokens` slack 0) | rows leave / ceilings go DOWN to the printed count; any raise is named with key, old -> new, reason in the report and the commit (axis 18). The census and driver-layers tests are SLOW (`scripts/slow_tests.json`): their printed value is read from the branch's CI run (RUNBOOK §7, `tools/ci_read.py`) and written in a fix commit on the same branch before acceptance | A1b, A2, B2, B3 DoDs |
| AR-21 / AR-22 handoff whole; every field produced has a reader | `work/advice-S2.json` and `work/advice-S3.json` (written by `exit_gate.write_advice`) and the S2 tester's / S3 strategist's handoff forms (their `tried` tables) lost their only reader (the S2/S3 critic's brief, `brief_pack.stage_critic_names` `:3565-3579`) | advice files: S4 `acceptance_reads` `{"S2": ["outputs", "advice"], "S3": ["advice"]}` (F2 (a)); both forms: the `TRIED_READERS` row `("S4", "qa-case-critic")` (B-1, B-1b) | A1a J1, J2 in `test_field_producers.py` |
| AR-23 empty outcome | an advice file absent at S4; an author form absent | the advice path is named with the absence line of `file_lines`; an absent form is not named (`tried_reader_names` skips an empty `last_accepted_form`) and the critic's `not_looked` says so | A1a J2 |
| AR-25 every recorded state has a way out | 0.11.0 states in flight (S2/S3 critic dispatch, `stage_in_repair`, an author accepted with the stage open, an S2/S3 completed whose ticket changes later; a second consumer round registered under cap 2) | §A.5 (T1-T4) and §B.5 state each one's road; T1-T4 have test rows | A1a T1, T2, T4; A1b T3 note; B2 G7 |
| AR-27 a gap reaches the report under its owner | the S6/S7 gap | a `pipeline["warnings"]` line `{stage} was accepted with a gap: {why}` -> the scribe's brief (`standing:` label, `brief_pack.py:1822`) -> `## Factory defects - nothing is wanted from you`; the S7 gap recorded at the scribe's own finish reaches gate B's packet through the same warnings (`gate_brief.py:2362`) | B2 G6; B3 scribe line |
| AR-28 an unknown never becomes a pass | an unreadable consumer verdict / uncountable rounds | recorded as a GAP (acceptor `driver`, quote `gap: ...`), never as a plain accept; no round is started on an unknown count | B2 G4, G5 |
| AR-29 a code check judges data; judgment is judged by a tier above | the judgment of the register (S2) moves to the case critic at S4; the plan's four checks become the author's own self-check (no critic judges the plan; the case critic at S4 sees coverage and level through the cases; the person reads the plan at gate A — F-8); consumer return reasons stay the consumer role's judgment | no code check added that reads meaning; AR-29 text updated (node D) | critic question 10/11 on each node |

AR-2, AR-7, AR-10 (FR-38): the consumer's legal return reasons are exactly what the author was told before the work (B3); the round state
reaches the consumer in its brief before its work (B2, the round line). FR-11/FR-38 for the S4 critic: its form and scope rule are changed
with its charter (A2, B-5).

### 1.2 Checks added, altered or removed: owner served and census class

| check | where | change | owner it serves | census class |
|---|---|---|---|---|
| S2/S3 stage acceptance gate (`stage_acceptance_refusal`) | controller / `acceptance.py:1532` | NOT edited; inert for S2/S3 once `acceptance_by` leaves | data | existing row `acceptance.py stage_acceptance_errors` (shape, data) unchanged |
| S3 plan check on a not-closing exit (`author_exit_owes_plan` branch of `_s3_completion_gate`, `controller.py:7533-7537`) | controller + acceptance | removed in A1b (inert after A1a: `acceptance.py:1521` returns False with no acceptor); the plan check runs on the closing exit as before X2-5 | data | no census row (grep, trail §T) |
| the stage critic's verdict at S2/S3 | `driver_stage_plan.stage_critic_completion` | removed (A1b) | judgment (was) | no census row (grep, trail) |
| completion of a dispatch whose role the stage does not declare (T2 rule) | `driver_stage_plan.completion_for` | added (A1a): answers False | data (the stage row) | not a check unit (raises nothing) |
| the ticket re-run's author choice | `driver_s0.ticket_rework_step` | altered (A1a): `roles[0]` for every stage | data | not a check unit |
| the four register checks + `tried` | case critic charter, S4 | moved / added as role text | judgment (the case critic; outcome accepted at gate A by the person and by the driver's shape checks) | none (text) |
| the four plan checks | strategist charter | reminder (self-check) | judgment (the author; nobody reviews the plan by meaning before gate A; the person reads it there) | none (text) |
| repair cap of a loop | `runtime_policy.repair_cap` (new reader) used by `Controller.prepare` (`controller.py:2197`), `Controller.validate` (`:5605`), `runtime_policy.cumulative_budget` (`:94`), `stage_status.round_cap` (`:69`) | altered: a stage row's `acceptance_rounds` caps its author's rounds, except a packet carrying `person_words: true` (F-10) | data | the existing refusal unit in `Controller.validate` `:5639-5663` keeps its class; `repair_cap` raises nothing (not a unit); `runtime_policy.cumulative_budget` row (shape, data) unchanged |
| consumer exhausted -> seam | `driver_stage_s6.consumer_exhausted` | replaced by the gap road (writes records, refuses nothing) | data (carries the consumer's quote) / judgment stays the consumer's | not a check |
| return reasons of the consumer | analyst / scribe charters | narrowed to what the author was told (text) | judgment (consumer), accepted by the tier above at the next stage | none (text) |

### 1.3 SIBLING_MAP axes (rule 10(b)), per mechanism

Mechanism A (S2/S3 stage critic removed; register checks to S4; plan reminder) and mechanism B (consumer one round, gap road). One line
per axis of `docs/SIBLING_MAP.md` (36 axes, read by heading list, trail §T):

- axis 1 (policy/role files/journal): n/a — no forge policy text changes; designer rule 1 and CLAUDE.md rule 10 untouched.
- axis 2 (exam instruments): n/a — no tier exam touched.
- axis 3 (package/release copy/installed plugin): covered — changelog fragments (A1a, B2); release copy is the normal release.
- axis 4 (rules/debt/backlog/principles): covered — D-0060 archive Lead note (§A.6); no FR text changes; `design/factory-rules-debt.md` "stage critic" grep in node D.
- axis 5 (stage twins): covered — A: S2 and S3 leave together, S4 kept; B: S6 and S7 through one table; row "Author + critic repair loop" (`SIBLING_MAP.md:122`) gains the S6/S7 consumer loop in node D (and FV1-6 item 14's S2/S3 addition is dropped, §X).
- axis 6 (measurers): queued — node D greps `experiments/measurers/stage_compare.py` for `qa-case-critic` and reports (no edit outside the package without a node).
- axis 7-11: n/a.
- axis 12 (carriers of the work plan): covered — the Lead's batch rows per §X; findings, not edits here.
- axis 13-16: n/a.
- axis 17 (detector verdict shape): covered A — `advice` records keep one shape; their reader moves to S4. B n/a.
- axis 18 (shrink-only ratchets): covered — census, driver-layers, role-load rows (A1b, A2, B2, B3); raises named; slow-test values read from CI.
- axis 19-30: n/a (no tools line, host receipt, table reader, host form, tests[] row, execution record, freshness, stand word, profile, row form render, jsonl appender, profile commands touched).
- axis 31 (role carriers, one owner per aspect): covered — the register-judgment aspect moves from "stage critic S2" to the case critic charter; the plan self-check lives in the strategist charter only; `role-rules.json` rows follow their carrier (A2).
- axis 32 (where judgment lives): covered — §1.2.
- axis 33 (which dispatch am I): n/a — `reviewed_dispatch` (`brief_pack.py:3582-3597`) keeps S4 and the consumers; S2/S3 drop out by data.
- axis 34 (one road): covered — no stage name in code for either mechanism; S6 and S7 one road; the ticket re-run's author is `roles[0]` for every stage (B-4a: the S1/S3 special cases go); the earlier-author form travels by `TRIED_READERS` only (B-1). The S4 seam vs the S6/S7 gap road is a difference selected by the CONSUMER RELATION (`acceptance.consumer_of(stage)`, `acceptance.py:1490-1494`: `acceptance_by` outside the stage's own roles), a data reading, plus the owner's word «не должно быть барьером» said of consumer acceptance only (§0) — named in §F (F5).
- axis 35, 36: n/a.

Four questions (rule 10): (a) cost — A removes one or more paid critic dispatches per S2 and S3 (and their repair rounds); B removes a
second repair round and every conductor/person call at an exhausted consumer review; paid by nobody new. (c) detector — calibration
check 41 (judgment census) and check 36 (architecture), the role-load audit A22, the keep rows below; the live proof row (FR-33) in
`live-runs`. (d) on the path — data rows read by code (`stages.json`), the controller's cap in `validate`, the brief lines.

---

# PART A — the S2/S3 stage critics removed

## A.1 Facts (read on the carrier)

- The switch: `references/stages.json` S2 `roles: [qa-requirements-tester, qa-case-critic]` (`:62-65`), `acceptance_by: qa-case-critic`
  (`:66`), `advice: ["sizing.py"]` (`:91-93`); S3 `roles: [qa-test-strategist, qa-case-critic]` (`:100-103`), `acceptance_by` (`:104`),
  `optional_dispatches` first_look runner (`:115-122`), no `advice`; S4 `acceptance_by` (`:148`), `inputs` hold the register (`:156`).
  **The `roles` lists must change too**: the critic is the S2/S3 LAST role, and `story_step.start` admits a role only when it is in `roles`
  or has an `optional_dispatches` row for its (role, purpose) (`story_step.py:898-905`).
- `driver_stage_plan.py`: `stage_S3` `:106-137` (critic branches `:115-117`, `:121-122`, `:130-131`); `s3_author_done` `:330-339`;
  `stage_repair_owed` `:557`; `s4_repair_owed` `:572`; `stage_acceptor` `:579-581`; `stage_S2` `:583-593` (no acceptor -> `stage_simple`);
  `stage_raise_questions` `:595`; `stage_critic_route` `:601`; `stage_after_critic` `:621`; `stage_critic_form` `:633`;
  `stage_acceptance_write` `:641`; `stage_critic_completion` `:653`; `stage_verdict_known` `:681`; `stage_review_exhausted` `:691`;
  `settle_role_questions` `:921`; `ticket_rerun_critic` `:962`; `completion_for` `:1011-1143` with the S2/S3 `ticket_changed` branch
  `:1025-1035` (it answers for ANY role at S2/S3) and the S2/S3 acceptor branch `:1036-1043`.
- Shared users kept: `stage_acceptance_write` — S4, S6 `driver_stage_s6.py:359,387`; `stage_verdict_known` — S4, S6 `:357`;
  `stage_review_exhausted` — S4, S6 `:358` and via `consumer_exhausted` `:341`; `stage_acceptor` — S4; `settle_role_questions` — S4.
  After A AND B, `stage_review_exhausted` has S4 as its only caller; its S6/S7 branches (`word = ... "stage_in_repair"` `:744`,
  `who = acceptance.consumer_of(stage) or ...` `:702`) are dead then — residual node R1 (F-3).
- `driver_machine.py`: `_act_prepare_stage` calls `self.stage_S2()` (`:1322-1323`); `wait_existing_job` -> `_wait_then_critic` (`:1290-1291`,
  `:1429-1433`) which calls `ticket_rerun_critic`; `record_running(... retry=lambda: self._wait_then_critic(action) ...)` (`:1496`).
- `driver_s0.ticket_rework_step` (`:483-548`): the author to re-run is `roles[-1]` among the stage's ACCEPTED dispatches, filtered to
  `qa-test-strategist` at S3 and to S1 `roles[0]` at S1, NOT filtered at S2 (`:526-530`); the S3 road `:531-538`, the others `:539-541`
  (`complete=True`). A 0.11.0 S2 completed with the critic accepted last therefore re-runs the CRITIC on a ticket change — refused by
  `story_step.start` after A (live bug on main today, B-4a).
- `driver_dispatch.s3_ticket_completion(closes=True)` `:2635-2642`: `closes=False` is used only by `driver_stage_plan.py:1034`.
- `controller.py`: `REPAIR_LOOP_ROLES` `:235-237` (S2/S3 authors added by X2-7, `:236`); `repair_passes` comment `:758-759` names "the S2/S3
  authors" (still true for the S6/S7 authors); `_s3_completion_gate` `:7516`, X2-5 branch `:7533-7537` calls
  `acceptance.author_exit_owes_plan` (`acceptance.py:1515-1521`), its only caller; `Controller.validate` (`:5336-6084`) holds both the cap
  lines `:5603-5605` and the stage-acceptance comment `:5893-5895`; `Controller.stage_repairs` (static, `:8524-8562`): a stage whose LAST
  role (`contract.stage_closes_with`) was accepted with neither `stage_complete` nor `unresolved` and nothing open gets a `stage_completed`
  fix (`:8554-8561`), applied by `recover` (driver runs it at `driver_machine.py:477`, `:2076`).
- The S2/S3 advice files: `exit_gate.write_advice` writes `work/advice-<stage>.json`; S2 carries the adviser `sizing.py` and the digest
  words outside the form's list; S3 only the digest words (no adviser; no `branch_accounting` record carries the advice kind).
- The S2/S3 critic's brief extras: `brief_pack.stage_critic_names` (`:3565-3579`: the stage's outputs, `work/advice-<stage>.json`, the
  author's last accepted form via `last_accepted_form` `:3625-3633`), gated by `stage_def["acceptance_by"] == role` (`:3570`). The SEPARATE
  existing road for an earlier author's form: `TRIED_READERS` (`:112`, one row `("S9", "qa-retro-analyst")`) read by `tried_reader_names`
  (`:3636-3644`); both are composed into the brief at `:4312-4313` with de-duplication (`if n not in names`).
- `brief_pack.FIRST_LOOK_KIND` (`:4001`) has the row `("S3", "qa-case-critic"): "s3"`.
- `handoffs/s2-stage-critic-to-tester.yaml`, `s3-stage-critic-to-strategist.yaml`; `handoffs/index.yaml:44-47`; `handoff_init.py:152-153`;
  `null-outcomes.json` NE34 `:133` / NE35 `:137` (scope carriers of the two forms); `open-vocabularies.json:3` note ("The stage critic
  judges every extension"); `test-layers.json:1701,1703` (the `covers` list of the keep row `test_field_producers.py` names the two forms).
- `stage_guard.py` `selftest()` (`:3074`): case `:3088-3089` expects `stages_of_role(model, "qa-case-critic") == ["S2", "S3", "S4"]`; run
  by the live keep file `test_stage_guard.py` (slow).
- `stage_done.py` messages naming S2/S3: `:975`, `:1551`.
- The S4 critic's form `handoffs/s4-case-critic-to-designer.yaml`: `inputs` `:17-26` (author's form, cases, plan), `advice_read` `:105`
  — a single placeholder for `work/advice-S4.json`; no code reads `advice_read` (grep over `*.py|*.json|*.yaml`, control: the yaml hit).
- `driver-layers.json` rows: route `:525-538`; `_wait_then_critic` `:784`; consumer `:680-688` (`consumer_exhausted` `:686`).
- `judgment-census.json` `ratchet` (`:4`): `blocking_per_role.qa-case-critic: 164`; rows `runtime_policy.py cumulative_budget` `:881`,
  `stage_status.py line` `:985` (shape, data); none names the S2/S3 route.
- Charter `agents/qa-case-critic.md`: description `:3`, scope `:10`, outcome `:15`, good outcome `:20-25` (item 3 advice `:24`), S2 `:30`,
  S3 `:31`, S4 `:32`, empty list `:33`, technique `:83`, "a finding at S3 and S4" `:86`, Tools scope rule `:95` (S4 scope = rows with
  `design_review_required`; repair review only changed rows), `:121` ("your form ... at every stage").
- Tests that read the S2/S3 route and are NOT quarantined (keep section of `test-layers.json` ends at `:7107`): `test_story_run_s3_windows.py`
  (W1 `:120`, W3 `:175`, W11 `:199-202`, W5 `:285-291`; slow), `test_story_run_freshness_k6_k7.py` (`:344-355`; slow), `test_handoff.py:670`
  (slow), `test_question_register.py:1928`, `test_field_producers.py:562-569` (negative rows fill `s2-stage-critic-to-tester`),
  `test_story_run_first_look.py:44`, `test_first_look_step.py:612-643`, `test_first_look_briefs.py:28`, `test_first_look_wiring.py:126`,
  `test_brief_s3_roster.py:85`, `test_stage_guard.py:2134` (slow, through the selftest). `test_scenario_local_1_arm_b.py` (slow): its walk
  (`fixtures/stories/local-1-arm-b/story.json:7-60`) has no S2/S3 critic step (S2 tester -> next S3 strategist; S4 critic; gate A); its
  recorded S2/S3 critic files are history and stay — judged by CI, no edit.
- `role-load.json`: `qa-case-critic` 18296 / process 15929; `qa-test-strategist` 16925 / 15392; `qa-requirements-tester` 12630 / 11280;
  `process_ratchet_tokens` is slack-0 (A22 red above or below its row).

## A.2 S2 — the acceptor removed; the register checks to the case critic at S4

### A.2.1 What S4 already covers, check by check (quotes from `agents/qa-case-critic.md`)

| S2 check | already at S4? | quote (line) | verdict |
|---|---|---|---|
| units of the text nobody turned into a requirement | technique yes, framed for the S2 stage; dimension 1 counts register coverage, not text units | `:83` "**Register against the units of text.** ..."; `:40` "Coverage — every register `R` covered" | technique stays; ADD one "Where bugs hide" line for S4 (below) |
| a compound requirement hiding two behaviours | no (atomicity `:41-46` is about merging CASES) | — | ADD |
| silence about a boundary (empty, maximum, a second time) | partly, at the case level | `:87` "**Boundaries and classes.** ..." — needs a limit the register states | ADD |
| a statement lifted from the diff recorded as a requirement (P20) | partly, at the oracle level | `:32` "an oracle copied from the code"; `:82` | ADD (register level) |
| reading the author's `tried` table | yes for the S4 author | `:23` item 2; `:84` | ADD: the S2 tester's `tried` is read too when the tester returned no questions |

### A.2.2 The new S4 text (craft voice; replaces `:30-32`)

In "Where bugs hide at this stage", the S2 and S3 bullets (`:30`, `:31`) and the S4 bullet's last sentence (`:32` "The rubric of eight
dimensions follows; hold it for S4 and borrow the dimensions that fit S2 and S3.") become:

- **The register behind the cases.** A sentence, field or branch of the sources that no requirement holds; a requirement that folds two
  behaviours into one row; a boundary the text is silent on (empty, maximum, the second time) with no branch and no question; a
  requirement whose only source is the diff (P20: a claim, never an expected value). A case built on such a row inherits its gap: name
  it, against the register line.
- **The cases.** A case that cannot fail, an oracle copied from the code, a Then with no independent channel, a duplicate of another case.
  The rubric of eight dimensions follows.
- `:33` "An empty list is a claim" gains: "the tester's empty questions list too: look for its attempt in the `tried` table of its form."

Scope rule `:95` (B-5b) gains, after its first sentence: "The register bullet is read once, on the first review round, over the whole
register and its sources, whatever the row scope; a repair round does not repeat it."

Process lines: `:3` description, `:10`, `:15`, `:20-25` lose S2/S3 (the critic is the S4 critic only); item 3 (`:24`) names every advice
file it is given (`work/advice-S4.json`, `work/advice-S2.json`, `work/advice-S3.json`, each named, or a dash and why it was absent).
`:86` "a finding at S3 and S4" -> "a finding". `:121` "at every stage" -> "at S4". Net: the S3 bullet leaves; three craft lines and one
scope sentence come in — A2 measures and names.

The S4 critic's FORM (B-5a, A2 owns it): `handoffs/s4-case-critic-to-designer.yaml` `advice_read` (`:105`) placeholder becomes
`"<each advice file the brief names - work/advice-S4.json, work/advice-S2.json, work/advice-S3.json - read, or a dash and the reason it was
absent>"` (still ONE string: no code reads it); `inputs` (`:17-26`) gain non-required rows (`required: false`) for
`work/requirements-register.md`, `work/requirements-readiness.json`, `understanding.md`, `work/advice-S2.json`, `work/advice-S3.json` and
"the S2 tester's and S3 strategist's last accepted forms (`work/handoffs/<id>.yaml`, named in the brief)". EDGE: a file the brief names
absent -> the critic writes its dash and reason in `advice_read` / `not_looked`; INVARIANT: no form row is `required: true` for a file
the factory may not have produced (FR-5).

### A.2.3 What the case critic is GIVEN at S4 (FR-15/AR-8: handed, not searched)

Data row (AR-1), `stages.json` S4: `"acceptance_reads": {"S2": ["outputs", "advice"], "S3": ["advice"]}` (F2 (a), Lead-decided).
Reader: `brief_pack.stage_critic_names` — after its own-stage names, for each `(earlier stage, parts)` of the acceptor's stage row:
`outputs` -> that stage's `outputs` without `project:` entries (S2: `work/requirements-register.md`, `work/requirements-readiness.json`,
`understanding.md`); `advice` -> `work/advice-<earlier>.json` (named whether or not it exists; absent prints the `file_lines` absence line).
Duplicates are named once (the brief composer de-duplicates, `brief_pack.py:4312-4313`). A key absent = today's behaviour.

The tester's form (which holds `tried`) and the strategist's form reach the S4 case critic through the ONE existing table
`brief_pack.TRIED_READERS` (B-1, B-1b, Lead decision 1): add the row `("S4", "qa-case-critic"): (("S2", "qa-requirements-tester"),
("S3", "qa-test-strategist"))`. Its reader `tried_reader_names` is UNCHANGED in code; only its docstring loses "that is not a stage critic"
(the S4 critic is a stage critic and now reads them) and `last_accepted_form`'s docstring loses "the stage critic's brief" as the S2/S3
reader. No `author_form` part. The S4 author (designer) brief does not change: both readers return `[]` for a role that is not the
acceptor / has no `TRIED_READERS` row. Moving `TRIED_READERS` into `stages.json` is NOT done here (it would change the design): one queue
line for the Lead (§Q, AR-1 residual).

### A.2.4 What a finding against the REGISTER at S4 does (existing mechanisms only)

No road from S4 back to the tester is built (no new loop, no new barrier — the owner's motive). A register finding travels by the two
roads that exist:
1. When the register gap changes what a case must check and the case can carry it, the critic scores the case dimension and the
   designer's ordinary S4 repair round fixes the CASES (`s4_after_critic`, unchanged).
2. When only the person or the product owner can settle it (silence, a diff-only claim P20, a sentence with no home), the critic writes it
   in `questions[]` of its form; `stage_acceptance_write` raises it into the register (`driver_stage_plan.py:646-649`, S4 included) and the
   conductor settles it from files or it goes to the person at gate A with its class (`settle_role_questions`, unchanged). No new
   question site.
The register file itself is not edited at S4 (one writer). Fork F3 (owner's, OPEN) returns the alternative.

## A.3 S3 — the acceptor removed; the four checks become the author's reminder

Strategist charter (`agents/qa-test-strategist.md`):
- `:21` "The acceptor reads each item against its witness; what you tried is the `tried` table of your handoff form." becomes (F-8):
  "Before you stop, read each item against its witness yourself: no critic judges the plan; the person reads it at gate A. What you
  tried is the `tried` table of your handoff form."
- Items 1-3 (`:23-25`) already say three of the four checks. The fourth goes in as one craft line under "Where bugs hide" next to `:32`:
  "**A changed branch no row walks.** Before you stop, lay the diff's changed branches beside the rows: a branch with no row and no
  `not_planned` reason is a hole in the plan, however good the rows read."
- No reference to a critic at S3 anywhere in the charter.
Ratchets: a raise of `qa-test-strategist` `ratchet_tokens` (craft, slack 1000) is expected to fit the slack; `process_ratchet_tokens`
moves to the measured value (slack 0) — named with key, old -> new, reason (AR-20).

`author_exit_owes_plan` and the S3 exit window: the function is deleted with its one caller's branch (A1b); `_s3_completion_gate`'s
`if window != "labelling" and not complete:` returns at once (the pre-X2-5 rule). INVARIANT: every S3 exit that CLAIMS the stage complete
is still judged by `validate_plan` + grounding (the `complete` branch is untouched); a window-1 claim of completeness is still refused
first. `FIRST_LOOK_KIND (S3, qa-case-critic)` goes (A1a); the `(S4, qa-case-critic)` row stays.

## A.4 Dead code and data — function by function, row by row (node in brackets)

| item | verdict | why |
|---|---|---|
| `stages.json` S2/S3 `acceptance_by`, `"qa-case-critic"` in `roles` [A1a] | delete | the switch |
| `stages.json` S2 `advice: ["sizing.py"]` | KEEP | the adviser still runs; its reader becomes S4's acceptor |
| `stages.json` S4 `acceptance_reads` [A1a] | new | A.2.3 |
| `brief_pack.TRIED_READERS` row (S4, qa-case-critic) [A1a] | new row | A.2.3 |
| `Driver.stage_S2` [A1b] | delete; `_act_prepare_stage` S2 goes to `stage_simple` explicitly | no acceptor |
| `stage_S3` critic branches + `critic = ...` [A1b] | delete (window logic untouched) | |
| `s3_author_done` [A1b] | delete | readers: `stage_S3` and tests |
| `stage_raise_questions`, `stage_critic_route`, `stage_after_critic`, `stage_critic_form`, `stage_critic_completion` [A1b] | delete | S2/S3 only |
| `ticket_rerun_critic`; `driver_machine._wait_then_critic` [A1b] | delete; `wait_existing_job` and the `record_running` retry call `_act_wait_existing_job` directly | |
| `completion_for` T2 rule [A1a] | new, BEFORE the S2/S3 `ticket_changed` branch (B-4b) | A.5 T2 |
| `completion_for` `:1033-1034` acceptor sub-branch of `ticket_changed`; `:1036-1043` acceptor branch [A1b] | delete (dead after A1a: `stage_acceptor` is "" at S2/S3) | |
| `s3_ticket_completion(closes=...)` [A1b] | drop the parameter | one caller left passes the default |
| `driver_s0.ticket_rework_step` author filter `:526-530` [A1a] | one generic rule: the author is `stages.json` `roles[0]` | B-4a, P31 |
| `stage_acceptor`, `stage_repair_owed`, `s4_repair_owed`, `stage_acceptance_write`, `stage_verdict_known`, `settle_role_questions` | KEEP | S4, S6, S7 |
| `stage_review_exhausted` S6/S7 branches (`:702`, `:744`) [R1] | simplify after FV1-6 and B2 merge | F-3 |
| `acceptance.py` stage-acceptance block, `stage_done.py --acceptance`, `vocabulary.stage_acceptance_verdicts`, `Reviewed dispatch:` | KEEP; docstrings listing "S2, S3, S4" corrected [A1b] (`acceptance.py:1458-1461,1516-1517,1526`, `stage_done.py:975,1551`) ; `controller.py:5894` comment corrected by B1 (it sits in `validate`, which B1 owns) | text only |
| `acceptance.author_exit_owes_plan` + its branch [A1b] | delete | A.3 |
| `controller.REPAIR_LOOP_ROLES` entries `qa-requirements-tester`, `qa-test-strategist` [A1a] | delete | before X2-7 they were not in the set |
| `controller.repair_passes` comment `:758` [A1a] | "S2/S3 authors ... stage critic's word" -> "S6/S7 authors ... their consumer's word" | text only |
| `brief_pack.stage_critic_names` [A1a] | keep, extended by `acceptance_reads` | |
| `brief_pack` `FIRST_LOOK_KIND` S3 critic row [A1a] | delete | |
| `stage_guard.py` `selftest()` case `:3088-3089` [A1a] | expected `["S4"]`, name "qa-case-critic stands on S4 only" | B-2 |
| `handoffs/s2-stage-critic-to-tester.yaml`, `s3-stage-critic-to-strategist.yaml`, `handoffs/index.yaml:44-47`, `handoff_init.py:152-153` [A1b] | delete (`handoff_init` tuples keep `s4-case-critic-to-designer`) | forms of a dispatch that no longer exists |
| `null-outcomes.json` NE34 `:133`, NE35 `:137` [A1b] | delete (verified: the scope carriers of the two forms) | |
| `open-vocabularies.json:3` note [A1b] | "The stage critic judges every extension" -> "The critic of the stage judges every extension (S4, S5); an extension proposed at S2 or S3 is read by the case critic at S4 through the author's form and by the person at gate A" | |
| `test-layers.json:1701,1703` (`covers` of the keep row `test_field_producers.py`) [A1b] | remove the two entries (a `covers` entry is not a keep row; `quarantine`/`cohorts` are untouched) | the files are deleted |
| `driver-layers.json` `:525-526`, `:529`, `:531-533`, `:535-536`, `:784` [A1b] | delete | methods gone (F-1) |
| `driver-layers.json` `:527-528`, `:530`, `:534`, `:537-538` [A1b] | KEEP; notes "S2 and S3" corrected to "S4/S6/S7" | |
| `driver-layers.json` `:686` (`consumer_exhausted`) [B2] | delete; new rows `consumer_gap`, `consumer_round_line` (home `driver_stage_s6`, row 74) | F-1 |
| `judgment-census.json` `ratchet` [A1b, B2] | no row leaves; `blocking_per_role` values lowered to what `test_judgment_census.py` prints on the branch's CI run when below the ceiling (F-2) | AR-20 |

## A.5 TEMPORAL — a story in flight recorded under 0.11.0, resumed on the new package

Both worlds: before the change S2/S3 carry `acceptance_by` and the critic in `roles`; after, they do not. The move that creates the new
world: A1a's commit to `stages.json`. Old `pipeline["acceptance"]["S2"|"S3"]` records stay on disk and are read by nobody for S2/S3.

| state on disk | road on the new package | cost |
|---|---|---|
| T1: S2/S3 open, the author's last dispatch accepted (finished not-complete under 0.11.0), no critic after it | Which road fires is decided by the record (F-14): (i) the author's record has neither `stage_complete` nor `unresolved` and nothing of the stage is open -> `Controller.stage_repairs` offers `stage_completed` (`controller.py:8554-8561`: the author is now the LAST role) and `recover` closes the stage on the author's finished work, no new dispatch; (ii) otherwise -> `where` -> `prepare_stage`: S2 `stage_simple` runs the tester again; S3 `stage_S3` (`s3_window()`: the newest counting dispatch is an accepted EXIT window -> `"w1"`) runs window 1 then window 2. Code: none. | (i) nothing; (ii) one S2 author dispatch, or two S3 windows (F4 (a)) |
| T1-b (control): S3 between the windows — window 1 (`purpose: s3_labelling`) accepted, window 2 not started | NOT closed by `stage_repairs` (the pre-X2-7 world had the same last-role rule); window 2 runs. Pinned by a row; if the row is red on the node's tree, the node stops with that output as a question to the Lead (a defect older than this spec, not fixed here) | none |
| T2: a `qa-case-critic` dispatch registered or running at S2/S3 | `story_step.start` refuses a NEW one; an existing one comes back through `wait_existing_job`. `completion_for` gets ONE generic rule, placed right after the S1 rules and BEFORE the S2/S3 `ticket_changed` branch (B-4b): a dispatch whose role is neither in its stage's `roles` nor in an `optional_dispatches` row of the stage for its (role, purpose) — the same reading `story_step.start` applies (`_optional_row`, `story_step.py:900`) — returns `False` (no stage or role name in the rule). Then T1. If the controller refuses that not-complete finish, the refusal reaches the conductor through `handle_refusal` (existing road; the conductor's `release` door frees the packet). | the critic's spend is lost; then T1 |
| T3: critic accepted with `stage_in_repair`, the author's round owed, or the author's repair round running | owed: T1 (the critic's form is NOT handed; the fresh author run is the round). Running: its finish recovered through `completion_for` meets the existing `rework_of` rule (False), stage stays open, then T1. | up to two author runs |
| T4: S2/S3 COMPLETED under 0.11.0 (critic accepted last), the ticket changes after the upgrade (B-4a) | `ticket_rework_step` picks the author as `stages.json` `roles[0]` among the stage's accepted dispatches -> the tester / strategist re-runs; never the critic | one author dispatch (as for any ticket change) |

INVARIANT (all four): no 0.11.0 state is a dead end (AR-25/FR-40); no stage closes except on an accepted finish of its author (claiming
it, or closed by the controller's existing last-role repair `stage_repairs`); no critic is dispatched at S2/S3 on the new package; a
dispatch of an undeclared role never closes any stage, whatever its `repair_cause`.

## A.6 Texts

- Charters: A.2.2 (case critic), A.3 (strategist); tester `:21`: "The case critic reads your register at S4, each item against its
  witness; what you tried is the `tried` table of your handoff form." Who is "the acceptor" at S2/S3 now: the driver's code checks only
  (shape: the exit gate, `branch_accounting`, `sizing` advice) — by meaning, the case critic at S4 (the register, through the cases) and
  the person at gate A.
- `skills/qa-story/phases/s2.md:117`, `s3.md:60`: the stage critic sentence removed (node D; FV1-12 crossing §X).
- `design/controller-blocks.md:229`: regenerated by `python tools/controller-blocks-gen.py` after A1b — node D runs the generator and
  commits whatever it prints, never a hand edit.
- `design/architecture.md` AR-29 (`:134-140`): "(a stage critic or the driver)" `:138` becomes "(the critic of the stage at S4 and S5, the
  consumer at S6 and S7, or the driver); the S3 plan is held by its author's self-check — the case critic at S4 sees coverage and level
  through the cases, and the person reads the plan at gate A" (F-8); the index is regenerated (`tools/architecture_index.py`).
- kb pages: searched in this round (`stage critic|qa-case-critic`, case-insensitive, over `kb/`): every hit names the S4 critic
  (`02-architecture.xhtml:86,106`, `01-overview.xhtml:130`, `diagram-pipeline-s0-s9.html:80`, `diagram-three-layers.html:121`,
  `qa-factory-route-en.html:220`, dashboards); no page names an S2/S3 critic or the consumer's rounds — no kb edit (node D repeats the
  search with its control and reports).
- Changelog fragment `changelog.d/stage-critics-s2-s3-removed.md` (English, A1a): "S2 and S3 close on their author's finish again: the
  separate stage critic after the tester and after the strategist is gone. The case critic at S4 now also judges the register behind the
  cases (a sentence no requirement holds, a compound requirement, a silent boundary, a requirement only the diff states) and reads the
  tester's and the strategist's forms and `work/advice-S2.json` / `work/advice-S3.json`. The strategist checks its own plan against four
  reminders before it stops. A ticket re-run always re-runs the stage's author. A story paused under 0.11.0 in S2 or S3 re-runs that
  stage's author once, or is closed on the author's finished work."
- D-0060 archive entry, Lead note (text to append, Russian, the Lead writes it): «Примечание Lead, 13.11.2026: часть B (критики стадий
  S2 и S3) снята словом владельца 13.11.2026 — «в таком варианте мы только увеличиваем время прохода стори и количество барьеров.
  Убираем лишних кртиков, оставляем как раньше». Проверки реестра S2 перенесены к критику кейсов на S4, проверки плана S3 — напоминанием
  в хартию стратега; приёмка S6/S7 потребителем оставлена с одним раундом и без барьера (спека
  `docs/tasks/specs/20261113-stage-critics-s2-s3-removed-spec.md`). P27/AR-29 не меняются: код не судит, суждение у роли.»

---

# PART B — S6/S7 consumer acceptance: one chance, never a barrier

## B.1 Facts

- The consumer table: `driver_stage_s6.py:146-156` `CONSUMER_ROUTES` (S6 judged by the analyst at S7, S7 by the scribe at S8).
- The round count: `consumer_counts` `:323-331` reads `budget_or_none` -> controller `prepare` -> `repair_budget.cap`, which is
  `policy.get("design_repair_cycles" if "case" in role else "repair_cycles")` (`Controller.prepare`, `controller.py:2194-2198`). The same
  inline choice sits at three more sites — four sites in all (F-9): `Controller.validate` (`:5603-5605`, the cap refusal `:5639-5663`),
  `runtime_policy.cumulative_budget` (`:94`, no stage known: passes `stage_def=None`), `stage_status.round_cap` (`:65-72`, reads
  `DEFAULT_LIMITS` only, no stage parameter; one caller, `stage_status.line` `:230`, which knows `stage`). `story_progress.py:357`
  (`DEFAULT_LIMITS["repair_cycles"]`) is the S5 window line (`kind: window`, `round_role` of S5) — NOT a site, not edited. Default
  `repair_cycles: 2` (`runtime_policy.py:13`), shared with the S5 automator/code critic.
- The packet of a rework built from a person's words carries `person_words: True` (`controller.py:3908-3911`, `words_given`); the
  conductor's `seam_rework_step` is such a rework (`driver_machine.py:600-610`, `words_file=rel`) and CAN spend a `test_defect` round of
  the S6 runner (F-10). The S7 re-judge uses `cause="reviewer_error"` (`driver_stage_s7.py:1052`, uncounted).
- The seam today: `consumer_completion` `:343-369` (unreadable word -> `stage_review_exhausted` `:357-358`; reject with no round ->
  `consumer_exhausted` `:367`), `consumer_settled` `:371-401` (no round -> `consumer_exhausted` `:395-397`; a round left -> `self.rework`
  `:398-400`), `consumer_exhausted` `:333-341`.
- The person's pass and its record: `person_pass` `:262-302` writes `stage_done.py --acceptance work/handoffs/<author>.yaml --acceptor driver
  --verdict accept --quote "by: person - ..."`; the prefix `BY_PERSON` lives in `driver_core.py:411`, read at `driver_stage_s6.py:193`.
- `stage_done.py` main: with `--acceptance` it returns `record_acceptance(...)` at `:1549-1553` and IGNORES `--warn`; `--warn` without
  `--stage` goes to `set_facts` (`:1562-1569`, `:911-929`), which appends to `pipeline["warnings"]` (`apply_facts` `:178-190`).
- The consumer's brief lines: S6 judged by the analyst `driver_stage_s7.py:134-137`; S7 judged by the scribe `driver_stage_s8s9.py:76-83`;
  the S7 acceptance is written at the scribe's finish (`driver_stage_s8s9.py:80`, `consumer_completion("S7", True)`) — AFTER its brief.
- The report: the scribe writes `## Factory defects - nothing is wanted from you` from "each `not established:` line of your brief"
  (`agents/qa-doc-scribe.md:64`); brief lines from `pipeline["warnings"]` are labelled `not established` only for an unknown capability
  line, otherwise `standing` (`brief_pack.py:1819-1824`, `gate_brief._not_established` `:2249-2268`). Gate B's packet reads the same
  warnings (`gate_brief.py:2362`).

## B.2 Design

B2-1. The cap is data. `stages.json` S6 and S7 get `"acceptance_rounds": 1` — "the repair rounds a consumer may ask of this stage's
author". One reader `runtime_policy.repair_cap(role, stage_def=None, limits=None, person_words=False) -> int|None`: when `stage_def` carries
an int (not bool) `acceptance_rounds >= 0`, `role == stage_def["roles"][0]` and `person_words` is false, that number; else today's
`policy.get("design_repair_cycles" if "case" in role else "repair_cycles")` over `dict(DEFAULT_LIMITS, **(limits or {}))`. Callers pass the
stage row through `acceptance.stage_def_of(stage)`; `Controller.validate` passes `person_words=bool(p.get("person_words"))`;
`Controller.prepare` passes `bool(options.get("person_words"))` (absent -> False); `stage_status.round_cap(task_root, role, stage="")`
gains the optional `stage` (its caller `line` passes its `stage`) and reads the row inside its existing `try` (any exception ->
`FALLBACK_ROUND_CAP`, as today); `cumulative_budget` passes `stage_def=None` (byte-identical; its local name `repair_cap` is renamed `cap`
to avoid shadowing). S4/S5 rows have no key -> byte-identical caps. A project's `limits.repair_cycles` does NOT lift `acceptance_rounds`
(«один шанс»). A person's words lift it (P13; F-10, decided by rule 2 of the Lead: no new refusal for a person-chosen rework).

B2-2. The round line, before the work (FR-38/AR-10). One helper `Driver.consumer_round_line(stage, awaiting) -> str` in
`driver_stage_s6.py` beside `consumer_counts`, called at both brief sites. Text:
- a round left: "Your return is the one chance the {author} has to redo this ({counted} of {cap} used): return it only if you cannot do
  your own work with it, and only for a reason the {author} was told (your charter lists them)."
- none left, or the count unknown: "No return is left for this handoff{: the rounds could not be counted}: do your own work with what it
  gives, and name what you could not use as a gap in your form's `unresolved` (the report shows it as a factory defect)."

B2-3. The gap road replaces the seam for consumer stages (POSITIONAL: inside `consumer_completion` and `consumer_settled`, in place of
every `stage_review_exhausted` / `consumer_exhausted` call; INVARIANT: `stage_review_exhausted` is still reached from S4 and from nowhere
else changed; an `accept` and a reject WITH a round left behave exactly as today). New `Driver.consumer_gap(stage, why, quote)`:
1. the author dispatch is `acceptance.stage_author_dispatch(state, acceptance.stage_def_of(stage))` (F-6; never `record`, which is None on
   the unreadable path); EMPTY -> no record and no warning, one printed line `"{stage}: no author run to judge; the consumer goes on"`, and
   the caller returns `own()` (a stage with no author run is not judged, cf. `consumer_close_refusal`, `acceptance.py:1500-1502`);
2. writes the record `stage_done.py --task <T> --stage <stage> --acceptance work/handoffs/<author>.yaml --acceptor driver --verdict accept
   --quote "gap: <why>: <quote[:400]>"` (the same writer and form as `person_pass`, `check=True`);
3. writes the warning (B-3, fork F6 recommended (a)): a SECOND call of the same writer, `stage_done.py --task <T> --warn "{stage} was
   accepted with a gap: {why}"` (`set_facts`, `stage_done.py:1562-1569`), right after the record; ORDER INVARIANT: the warning is written
   only after the record is written, so a warning never claims a gap no record holds;
4. prints one line; the caller returns the consumer's OWN completion (`own()` in `consumer_completion`; `True` in `consumer_settled`).
The `why` texts: `the one repair round of the {author} is spent`, `the {who}'s verdict word could not be read`, `the repair rounds of the
{author} could not be counted`, `the {who}'s acceptance form was refused: <refusal text[:200]>` (a Refusal from `stage_acceptance_write`
in `consumer_completion`, caught), `the repair round of the {author} could not be started: <refusal[:200]>` (F-4: `self.rework` in
`consumer_settled` raises `ReworkRefused`/`Refusal`). `consumer_exhausted` is deleted (its one job was the seam). The builder keeps
`consumer_completion` near today's size by routing every branch through `consumer_gap`.

INVARIANT of `own()` on the gap road (F-5): `own()` is the stage's UNCHANGED rule. An analyst that did not triage stays open by
`s7_open_work` / `s7_fresh`; a scribe report that does not hold is caught by `report_facts --check` at the S9 exit. The gap road never
adds a close the stage's own rule refuses.

B2-4. "Accepted with a gap" has one home (AR-13, F-7): `GAP_PREFIX = "gap:"` in `driver_core.py` beside `BY_PERSON` (`:411`), imported by
`driver_stage_s6.py` with it (`:13`). `consumer_close_words` gains a branch: acceptor `driver` and quote starting with `GAP_PREFIX` -> reason
"accepted with a gap: <quote>", digest "accepted with a gap" — POSITION after the `BY_PERSON` branch (INVARIANT: a person's pass is never
read as a gap). No `acceptance.py` change; no second reader of acceptance records in `brief_pack` (B-3: the warnings road carries it).

B2-5. The report (B-3). The S6 gap's warning is in `pipeline["warnings"]` before the scribe's brief is built -> the scribe's brief line
`- standing: S6 was accepted with a gap: <why>` -> the scribe puts it under `## Factory defects - nothing is wanted from you` (B3 charter
line). The S7 gap is written at the scribe's finish (after its brief): (a) on the 1-of-1 path the scribe was told by the round line that no
return is left and names the gap itself; (b) on the unreadable / form-refused / stale-count / rework-refused paths, the warning reaches
gate B's packet (`gate_brief.py:2362`), where the person sees it before deciding. `rebuild_report` and the `report_facts` check are
unchanged; FR-37 kept. Delivery verdict rules are unchanged (P21).

## B.3 All requirements are with the author from the start (FR-38, AR-10)

| consumer -> author | return reason the consumer charter names | where the author is told today | gap / text change |
|---|---|---|---|
| analyst -> runner (S6) | "A run you cannot rely on goes back to the runner with the quote that shows why" (`qa-failure-analyst.md:28`) | unspecific | NARROW: replace with "Return the run only for what the runner was told to give: a verdict no capture of this attempt supports, a doubt the captures show that no observation records, a case or instance that did not run with no reason and owner. Anything else you judge yourself and go on." |
| (same) | a verdict no capture of this attempt supports | `qa-runner.md:23` item 1 | told |
| (same) | a doubt with no observation | `qa-runner.md:24` item 2 | told |
| (same) | not run with no reason/owner | `qa-runner.md:25` item 3, `:16` | told |
| (same) | "A runner whose captures contradict its verdict" (`:39`) | `qa-runner.md:23` | not a return; no change |
| scribe -> analyst (S7) | a red with no verdict (`qa-doc-scribe.md:26`) | `qa-failure-analyst.md:16` | told |
| (same) | a verdict its evidence contradicts (`:26`) | `qa-failure-analyst.md:23` item 1 | told |
| (same) | a bug draft with no requirement (`:26`) | `:27` item 5 names only the red test | GAP: item 5 becomes "A product bug's draft names the requirement it breaks and its red test, or says why there is none." |
| (same) | a merged draft whose manifestations the cause does not explain (`:31`) | `:63` | told |
| (same) | two drafts sharing a code line or seen value and no `distinct_defect` (`:31`) | `:76` code line only | GAP: `:76` "drafts at one `defect_location` merge" -> "drafts at one `defect_location` or one seen value merge" |
| (same) | "A verdict you would have to explain away in the report is the triage's defect" (`:51`) | unspecific | NARROW: "... is the triage's defect when it is one of the returns item 5 lists; anything else you name in the report." |

How "a return for a reason the author was never told is not legal" is kept: TEXT for the consumer role (the narrowed lines and the round
line), judged at acceptance by the tier above; no code reads the meaning of a return (P27, AR-29). Scribe charter also gets one line in
Tools: "No return left (your brief says so): write the report on what you have and name the gap under `## Factory defects - nothing is
wanted from you`; a `standing:` line of your brief that begins `S6 was accepted with a gap` or `S7 was accepted with a gap` goes there too."

## B.4 Edges (each with its invariant)

- E-B1 cap AT and BEYOND: rounds counted 0 of 1 -> one round; 1 of 1 -> gap. INVARIANT: never a second consumer round; never a seam call.
- E-B2 a stage row without `acceptance_rounds` (S4, S5, an older table) -> today's cap. INVARIANT: the S4/S5 cap never changes.
- E-B3 `acceptance_rounds` not an int, negative or a bool -> ignored (today's cap). INVARIANT: a malformed row never removes the one round
  silently and never adds a second one beyond `repair_cycles`.
- E-B4 the brief line said "a round left" but at the verdict none is: the verdict-time count decides; gap. INVARIANT: the decision reads the
  controller's count once, at the verdict; the brief line is advice.
- E-B5 the count unknown (None) -> NO round and a gap. INVARIANT (AR-28): an unknown count is a gap, never a pass and never a round.
- E-B6 the verdict word unreadable / no dispatch id -> gap. INVARIANT: no record is ever `accept` without the `gap:` prefix when the
  consumer's word was not read.
- E-B7 the gap record write, or the warning write, refused (stage_done) -> a Refusal on the standard road (`handle_refusal`); INVARIANT: the
  stage never closes without a record (`consumer_need_record` unchanged). This is the ONE remaining conductor door of Part B: a factory
  defect of the writer, accepted as an FR-1 refusal (K4 i).
- E-B8 a person's pass stands before the verdict -> today's behaviour (the pass wins, `consumer_settled` `:391`). INVARIANT: a person's word
  is never overwritten by a gap.
- E-B9 the quote empty -> `gap: <why>: (no quote)`; longer than 400 characters -> cut at 400 with `...`. INVARIANT: the consumer's full form
  stays on disk and the brief names its path (FR-49).
- E-B10 (F-4) the author's repair round cannot be registered (the controller refuses `rework`) -> `consumer_gap` with why `the repair round
  of the {author} could not be started: <refusal[:200]>`. INVARIANT: no seam, no question.
- E-B11 (F-6) no author dispatch can be named -> no record, no warning, one line, `own()`. INVARIANT: no path is invented; no gap is
  claimed over a run that does not exist.
- E-B12 (F-10) a rework built from a person's words (`person_words: true`) of the S6 runner / S7 analyst -> capped by `repair_cycles`, not by
  `acceptance_rounds`; it still counts in the ledger, so the consumer's next reject after it finds `1 of 1` -> gap. INVARIANT: a person's
  chosen round is never refused by the new cap (P13); the consumer still gets no second round. Residual (named): a conductor's OWN rework
  of the S6 runner with `test_defect` and no person's words is capped at 1 and, past it, meets the existing refusal with its person's-pass
  door (`controller.py:5651-5663`) — an existing refusal, one round earlier.

## B.5 TEMPORAL

Before: cap 2 and the seam; after: cap 1 and the gap road; the move that creates it: B1 (cap) and B2 (road) commits — either alone is
safe (B1 alone: cap 1 with the seam = F1 (b)'s world; B2 alone: the gap road under cap 2). A story in flight with a SECOND consumer round
already registered (counted 1, round 2 running): the round runs; at the next verdict the count is 2 of 1 -> gap (E-B1). A round 2 not yet
registered: none is started. An S6/S7 story parked at the seam: its answer roads are unchanged (`take_seam_answer`); the next consumer
verdict, if any, follows the gap road. INVARIANT: no in-flight state is a dead end; no third round is ever started.

---

## §N. Nodes

Common to every node: given — this spec; `ai-packages/qa-factory/design/factory-rules.md` WHOLE; `plans/builder-rules.md`; `docs/TESTING.md`;
`ai-packages/qa-factory/design/architecture.md` (rows of §1.1); `ai-packages/qa-factory/scripts/slow_tests.json`; the files of owns as they
stand in the node's worktree. non-goals (all): S4, S5 acceptance; the S5/S7 repair-limit road; any code refusal restored; any new question
to a person; any new test FILE (a new parameterised function in an existing keep file is legal); any edit or run of a quarantined test file;
any local run of a file listed in `scripts/slow_tests.json` — such a file is named "judged by CI" and its keys are read from the branch's CI
run (RUNBOOK §7, `tools/ci_read.py`). handoff: builder report per `.claude/agents/builder.md` rule 7 (FR pass A-G, verbatim witness, axis
block, AR-20 line for every ratchet move, `architecture:` and `judgment:` lines, the CI keys of slow files). Worktrees
`C:\QAFactory\forge-repo\.claude\worktrees\sc-<node>\` from origin/main at dispatch (after the prerequisites of §Parallelism).
VERIFICATION FORM (every code node): `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <the node's owned
non-test paths>` and every NON-slow file it prints, run; the slow files it prints are listed as "judged by CI".
OWNER'S FORKS (Lead decision 5): F1, F3, F5 stay open; each node below says which of its lines change if the owner picks the other option.

### A1a — S2/S3 leave in data; temporal rules; the S4 hand-over; live tests  [builder -> critic, topic A]
owns:
C:\QAFactory\forge-repo\.claude\worktrees\sc-a1a\ai-packages\qa-factory\references\stages.json (S2, S3 rows: `roles`, `acceptance_by`; S4 row: new `acceptance_reads`)
C:\QAFactory\forge-repo\.claude\worktrees\sc-a1a\ai-packages\qa-factory\scripts\driver_stage_plan.py (`completion_for`: the new T2 rule only)
C:\QAFactory\forge-repo\.claude\worktrees\sc-a1a\ai-packages\qa-factory\scripts\driver_s0.py (`ticket_rework_step`: the author filter `:526-530` only)
C:\QAFactory\forge-repo\.claude\worktrees\sc-a1a\ai-packages\qa-factory\scripts\controller.py (`REPAIR_LOOP_ROLES` constant; `repair_passes`: the comment `:758-759` only)
C:\QAFactory\forge-repo\.claude\worktrees\sc-a1a\ai-packages\qa-factory\scripts\brief_pack.py (`TRIED_READERS` constant; `stage_critic_names`; docstrings of `tried_reader_names`, `last_accepted_form`; the `FIRST_LOOK_KIND` S3 critic row)
C:\QAFactory\forge-repo\.claude\worktrees\sc-a1a\ai-packages\qa-factory\scripts\stage_guard.py (`selftest()`: the case `:3088-3089` only)
C:\QAFactory\forge-repo\.claude\worktrees\sc-a1a\ai-packages\qa-factory\scripts\tests\test_story_run_s3_windows.py (W1 `:120`, W3 `:175`, W11 `:199-202`, W5 `:285-291`; new rows SC-1..SC-3, T2)
C:\QAFactory\forge-repo\.claude\worktrees\sc-a1a\ai-packages\qa-factory\scripts\tests\test_story_run_freshness_k6_k7.py (`:344-355` rows; new row T4)
C:\QAFactory\forge-repo\.claude\worktrees\sc-a1a\ai-packages\qa-factory\scripts\tests\test_stage_closure.py (new rows T1, T1-b)
C:\QAFactory\forge-repo\.claude\worktrees\sc-a1a\ai-packages\qa-factory\scripts\tests\test_field_producers.py (new rows J1, J2)
C:\QAFactory\forge-repo\.claude\worktrees\sc-a1a\ai-packages\qa-factory\scripts\tests\test_first_look_briefs.py (`PAIRS` `:28`: the `("S3", "qa-case-critic")` entry only)
C:\QAFactory\forge-repo\.claude\worktrees\sc-a1a\ai-packages\qa-factory\scripts\tests\test_first_look_wiring.py (`:126`: the `("S3", "qa-case-critic")` entry only)
C:\QAFactory\forge-repo\.claude\worktrees\sc-a1a\ai-packages\qa-factory\scripts\tests\test_brief_s3_roster.py (`:85`: the S3 roles tuple only)
C:\QAFactory\forge-repo\.claude\worktrees\sc-a1a\ai-packages\qa-factory\changelog.d\stage-critics-s2-s3-removed.md (new)
non-goals: every function A1b deletes (they become inert by data and stay until A1b); S4 functions; every S6/S7 function; `Controller.validate`
and `Controller.prepare` (B1); charters and forms (A2); `story_run_common.py`; the `ticket_changed` acceptor sub-branch (A1b).
edges (each with invariant):
- POSITIONAL `completion_for` T2 rule: right after the two S1 rules (`:1014-1024`), BEFORE the S2/S3 `ticket_changed` branch (`:1025`).
  INVARIANT: a dispatch of an undeclared role never closes any stage, whatever its `repair_cause`; a declared author's ticket re-run still
  closes S2 / re-captures S3 (`ticket_changed` branch untouched); the S1 rules above are untouched; an optional dispatch (first-look runner
  at S3, reference runner at S1) is declared and falls through as today.
- `ticket_rework_step` author filter: `d.get("role") == (self.stages().get(stage, {}).get("roles") or [""])[0]` for every stage, replacing the
  S3 and S1 special cases. INVARIANT: the re-run is always the stage author; a stage whose `roles` is empty re-runs nothing ("no accepted
  work" line, today's road); S1 and S3 behave exactly as today (their `roles[0]` is the same role the special cases named).
- `acceptance_reads` absent / an unknown part word / an earlier stage not in the table / a value that is not a list -> nothing extra for
  that entry, one printed line naming it (never a crash). INVARIANT: the S4 designer brief is byte-identical; the S4 critic brief only grows.
- an advice file absent -> named with the absence line. INVARIANT (AR-23): absence is said, never silent.
- the S2 tester or the S3 strategist has no accepted dispatch -> `tried_reader_names` names nothing for it. INVARIANT: no path is invented.
- `TRIED_READERS` S9 row unchanged. INVARIANT: the retro's brief is byte-identical.
- `REPAIR_LOOP_ROLES` shrink: INVARIANT S4, S5, S6, S7 authors and critics keep their cap.
- TEMPORAL: both worlds A.5 (T1, T1-b, T2, T4). The world is created by this node's `stages.json` commit.
F1/F3/F5 if the owner picks the other option: no line of A1a changes.
test rows (parameterised; ids name the input):
- `test_story_run_s3_windows.py` (keep `test-layers.json:6083`, SLOW — judged by CI): W1 rewritten: S2 roles == [tester], S3 roles ==
  [strategist], neither has `acceptance_by`; S4 has `acceptance_by` and `acceptance_reads == {"S2": ["outputs", "advice"], "S3": ["advice"]}`.
  W3 `:175` / W11 `:199-202` rewritten as SC-2 `s3-closes-without-critic` (diff world and off-diff): window 2 / the one window closes; the
  routed list stays empty. W5 `:285-291`: S3 ticket_changed -> `s3_ticket_completion()` callable returns True (closes); S2 ticket_changed
  with the tester -> True. SC-1 `s2-closes-without-critic`: S2 through `_act_prepare_stage` with the role stub: one dispatch (tester), its
  completion closes. SC-3 `s4-still-runs-its-critic`: `stage_S4` with stubs dispatches the designer then `qa-case-critic` (control). T2
  `undeclared-role-never-closes`: `completion_for("S2", "qa-case-critic", {})` is False; `completion_for("S2", "qa-case-critic",
  {"repair_cause": "ticket_changed"})` is False; `completion_for("S3", "qa-case-critic", {"repair_cause": "ticket_changed"})` is False;
  `completion_for("S3", "qa-runner", {"purpose": "first_look"})` is not False by the T2 rule (control: declared optional).
- `test_story_run_freshness_k6_k7.py` (keep `:5719`, SLOW — judged by CI): `:344-355` S2 ticket re-run with the tester -> True (no acceptor);
  T4 `ticket-rerun-picks-roles0`: accepted S2 dispatches tester then `qa-case-critic` -> `rework("S2", "qa-requirements-tester", ...)`;
  S3 with strategist then first-look runner accepted -> strategist (control, as today); S1 scout then reference runner -> scout (control).
- `test_stage_closure.py` (keep `:5335`, fast): T1 `author-last-closes-by-repair`: `Controller.stage_repairs(state)` for S2 running, newest
  dispatch the tester accepted without `stage_complete`/`unresolved`, nothing open -> one `stage_completed` fix for S2; with `unresolved`
  -> none. T1-b `s3-between-windows-not-closed`: S3 running, newest dispatch window 1 (`purpose: s3_labelling`) accepted -> no fix for S3.
- `test_field_producers.py` (keep `:1682`, fast): J1 `advice-and-forms-reach-s4-critic`: `stage_critic_names(S4 row, "qa-case-critic",
  task)` names `work/advice-S2.json`, `work/advice-S3.json`, `work/requirements-register.md`, `work/requirements-readiness.json`,
  `understanding.md`; `tried_reader_names(S4 row, "qa-case-critic", task)` names the tester's and the strategist's last accepted forms;
  for `qa-case-designer` both return []. J2 `absent-advice-named` / `no-author-form-named-nothing`.
- `test_first_look_briefs.py`, `test_first_look_wiring.py`, `test_brief_s3_roster.py` (fast): the S3 critic entries leave; every other pair
  unchanged.
DoD: keys W1, W3/W11 (SC-2), W5, SC-1, SC-3, T2, T4 green on the branch's CI run (read with `tools/ci_read.py`, quoted verbatim); T1,
T1-b, J1, J2 and the three first-look files green locally; `python -B ai-packages/qa-factory/scripts/stage_guard.py --selftest` prints no
failure (the selftest case of `stage_guard.py`; `test_stage_guard.py` itself is slow — judged by CI); `grep -n "roles\[-1\]"
ai-packages/qa-factory/scripts/driver_s0.py` prints nothing, positive control the same grep on the base tree prints `:535`/`:540`.
Verification: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/references/stages.json ai-packages/qa-factory/scripts/driver_stage_plan.py ai-packages/qa-factory/scripts/driver_s0.py ai-packages/qa-factory/scripts/controller.py ai-packages/qa-factory/scripts/brief_pack.py ai-packages/qa-factory/scripts/stage_guard.py`
and the non-slow files it prints; judged by CI: `test_story_run_s3_windows.py`, `test_story_run_freshness_k6_k7.py`, `test_stage_guard.py`
and every other slow file it prints. `architecture: AR-1, AR-13, AR-15, AR-19, AR-22, AR-23, AR-25 -- data rows; TRIED_READERS row (AR-1
residual queued); one author rule; T2/T4 roads`. judgment: no check reads meaning. Ratchets: none expected (no method added or removed).
siblings: S4 route (control SC-3); S6/S7 consumer (Part B); the census/stage-joints rows of T1 topic (§X).

### A1b — the dead S2/S3 route removed (after A1a)  [builder -> critic, topic A]
owns:
C:\QAFactory\forge-repo\.claude\worktrees\sc-a1b\ai-packages\qa-factory\scripts\driver_stage_plan.py (`stage_S3` critic branches; deleted: `stage_S2`, `s3_author_done`, `stage_raise_questions`, `stage_critic_route`, `stage_after_critic`, `stage_critic_form`, `stage_critic_completion`, `ticket_rerun_critic`; `completion_for`: the acceptor sub-branch `:1033-1034` and the branch `:1036-1043` only; docstrings of `stage_acceptance_write`, `stage_repair_owed` naming S2/S3)
C:\QAFactory\forge-repo\.claude\worktrees\sc-a1b\ai-packages\qa-factory\scripts\driver_machine.py (`_act_prepare_stage` S2 branch; `_wait_then_critic` deleted; the `wait_existing_job` line `:1290-1291`; the `record_running` retry `:1496`)
C:\QAFactory\forge-repo\.claude\worktrees\sc-a1b\ai-packages\qa-factory\scripts\driver_dispatch.py (`s3_ticket_completion` only)
C:\QAFactory\forge-repo\.claude\worktrees\sc-a1b\ai-packages\qa-factory\scripts\controller.py (`_s3_completion_gate`: lines `:7533-7537` only)
C:\QAFactory\forge-repo\.claude\worktrees\sc-a1b\ai-packages\qa-factory\scripts\acceptance.py (`author_exit_owes_plan` deleted; docstrings `:1458-1461`, `:1516-1517`, `:1524-1528`)
C:\QAFactory\forge-repo\.claude\worktrees\sc-a1b\ai-packages\qa-factory\scripts\stage_done.py (the messages `:975`, `:1551` only)
C:\QAFactory\forge-repo\.claude\worktrees\sc-a1b\ai-packages\qa-factory\handoffs\s2-stage-critic-to-tester.yaml (delete)
C:\QAFactory\forge-repo\.claude\worktrees\sc-a1b\ai-packages\qa-factory\handoffs\s3-stage-critic-to-strategist.yaml (delete)
C:\QAFactory\forge-repo\.claude\worktrees\sc-a1b\ai-packages\qa-factory\handoffs\index.yaml (the rows `:44-47`)
C:\QAFactory\forge-repo\.claude\worktrees\sc-a1b\ai-packages\qa-factory\scripts\handoff_init.py (the two contract names in the tuples `:152-153`)
C:\QAFactory\forge-repo\.claude\worktrees\sc-a1b\ai-packages\qa-factory\references\null-outcomes.json (NE34, NE35)
C:\QAFactory\forge-repo\.claude\worktrees\sc-a1b\ai-packages\qa-factory\references\open-vocabularies.json (the `note` `:3`)
C:\QAFactory\forge-repo\.claude\worktrees\sc-a1b\ai-packages\qa-factory\scripts\tests\test-layers.json (the `covers` entries `:1701`, `:1703` of the keep row `test_field_producers.py` only)
C:\QAFactory\forge-repo\.claude\worktrees\sc-a1b\ai-packages\qa-factory\scripts\tests\test_story_run_s3_windows.py (new row W2)
C:\QAFactory\forge-repo\.claude\worktrees\sc-a1b\ai-packages\qa-factory\scripts\tests\test_first_look_step.py (`s3_readers_with_first_look_dispatch_present` `:612-643` only)
C:\QAFactory\forge-repo\.claude\worktrees\sc-a1b\ai-packages\qa-factory\scripts\tests\test_story_run_first_look.py (`:44` only)
C:\QAFactory\forge-repo\.claude\worktrees\sc-a1b\ai-packages\qa-factory\scripts\tests\test_handoff.py (`:670` forms tuple only)
C:\QAFactory\forge-repo\.claude\worktrees\sc-a1b\ai-packages\qa-factory\scripts\tests\test_question_register.py (`:1928` names tuple only)
C:\QAFactory\forge-repo\.claude\worktrees\sc-a1b\ai-packages\qa-factory\scripts\tests\test_field_producers.py (the negative rows `:562-569` only)
C:\QAFactory\forge-repo\.claude\worktrees\sc-a1b\ai-packages\qa-factory\scripts\tests\fixtures\driver-layers.json (rows of A.4 marked [A1b])
C:\QAFactory\forge-repo\.claude\worktrees\sc-a1b\ai-packages\qa-factory\scripts\tests\fixtures\judgment-census.json (the `ratchet` values only, as the CI run of `test_judgment_census.py` prints)
non-goals: everything A1a owns except the listed `completion_for` lines; `Controller.validate` (B1 owns the `:5894` comment); S4 functions;
S6/S7 functions; `stage_review_exhausted` (R1); the recorded fixture story `local-1-arm-b` (history, unchanged).
edges (each with invariant):
- `_s3_completion_gate`: INVARIANT every closing S3 exit is still validated; window 1 claiming completion still refused first.
- `_act_prepare_stage`: S2 joins the explicit `stage_simple` line (never the generic `getattr`, which would look for the deleted method).
  INVARIANT: S1 -> simple, S2 -> simple, S3 -> stage_S3, S4 -> stage_S4.
- `wait_existing_job` and the retry: call `_act_wait_existing_job(action)` directly. INVARIANT: a finished ticket re-run of S2/S3 closes by
  `completion_for` (the `ticket_changed` branch), with no critic route after it.
- a deleted contract still named by a reader outside this owns list -> the node stops with the grep output as a question (the list above is
  the full reader set found in this round: grep `stage-critic-to` over the package, control the two files themselves).
- `test_first_look_step` rows: `at()` returns `s3_window()` only, expected windows `between`, `w1`, `w1`, `w1`, `between`, `w1`, `between`
  (today's first elements); the `stage_S3` tail becomes one check `hasattr(SR.Driver, "stage_critic_route") is False`. INVARIANT: the
  first-look runner record still never counts as a strategist window.
- `test_field_producers` negatives `:562-569`: the contract `s2-stage-critic-to-tester` becomes `s4-case-critic-to-designer` (it owes
  `findings` and `stage_acceptance` on `concerns` too — `handoffs/s4-case-critic-to-designer.yaml:33,92`). INVARIANT: the reader still
  refuses an absent owed row and an owed section left as the template.
- `test_handoff.py:670`, `test_question_register.py:1928`: the tuples keep only `s4-case-critic-to-designer`. INVARIANT: the S4 form keeps
  every assertion it had.
- census / driver-layers values: slow tests — read from the branch CI, written in a fix commit; a raise is named (key, old -> new, reason).
- TEMPORAL: none new (A1a created the world; A1b removes code already inert in it).
F1/F3/F5 if the owner picks the other option: no line of A1b changes.
test rows: W2 (`test_story_run_s3_windows.py`, slow): `_act_prepare_stage` S1 -> simple, S2 -> simple, S3 -> stage_S3, S4 -> stage_S4.
DoD: W2 green on the branch CI; `test_first_look_step.py`, `test_story_run_first_look.py`, `test_question_register.py`,
`test_field_producers.py` green locally; `grep -rn "stage_critic_route\|ticket_rerun_critic\|author_exit_owes_plan\|_wait_then_critic\|s3_author_done\|stage-critic-to" ai-packages/qa-factory/scripts --include=*.py`
outside `tests/fixtures/stories/` prints nothing, positive control `grep -n "stage_review_exhausted" ai-packages/qa-factory/scripts/driver_stage_plan.py`
prints a hit; `test_handoff.py`, `test_driver_layers.py`, `test_judgment_census.py` green on the branch CI.
Verification: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/driver_stage_plan.py ai-packages/qa-factory/scripts/driver_machine.py ai-packages/qa-factory/scripts/driver_dispatch.py ai-packages/qa-factory/scripts/controller.py ai-packages/qa-factory/scripts/acceptance.py ai-packages/qa-factory/scripts/stage_done.py ai-packages/qa-factory/handoffs/index.yaml ai-packages/qa-factory/scripts/handoff_init.py ai-packages/qa-factory/references/null-outcomes.json ai-packages/qa-factory/references/open-vocabularies.json`
and the non-slow files it prints; judged by CI: `test_story_run_s3_windows.py`, `test_handoff.py`, `test_driver_layers.py`,
`test_judgment_census.py` and every other slow file it prints. `architecture: AR-17, AR-19, AR-20, AR-22, AR-25 -- dead route removed,
seam kept for S4; ratchets lowered as printed`. judgment: removed a judgment site (the stage critic); no check added.
siblings: S4 route; `stage_review_exhausted` simplification (R1).

### A2 — charters, the S4 critic's form and ratchets  [builder -> critic, topic A]
owns:
C:\QAFactory\forge-repo\.claude\worktrees\sc-a2\ai-packages\qa-factory\agents\qa-case-critic.md (`:3`, `:10`, `:15`, `:20-25`, `:30-33`, `:86`, `:95`, `:121`; A.2.2)
C:\QAFactory\forge-repo\.claude\worktrees\sc-a2\ai-packages\qa-factory\agents\qa-test-strategist.md (`:21`; one craft line near `:32`; A.3)
C:\QAFactory\forge-repo\.claude\worktrees\sc-a2\ai-packages\qa-factory\agents\qa-requirements-tester.md (`:21` only)
C:\QAFactory\forge-repo\.claude\worktrees\sc-a2\ai-packages\qa-factory\handoffs\s4-case-critic-to-designer.yaml (`advice_read` `:105`; non-required `inputs` rows; A.2.2)
C:\QAFactory\forge-repo\.claude\worktrees\sc-a2\ai-packages\qa-factory\references\role-load.json (the three roles' rows)
C:\QAFactory\forge-repo\.claude\worktrees\sc-a2\ai-packages\qa-factory\design\role-rules.json (only rows whose carrier line A2 changes)
non-goals: any other charter; the rubric dimensions `:38-75`; Tools/When-to-ask sections except the stage words and `:95`; every
`required: true` row of the S4 form.
edges: a `role-rules.json` anchor that stood in a removed S2/S3 line -> the row moves to its new carrier line (the register bullet) or is
removed in the same commit with the reason. INVARIANT: no rule is lost silently. A ratchet row raised -> named key, old -> new, reason;
process rows set to the measured value (slack 0). The S4 form: a brief-named file absent -> dash and reason in `advice_read` /
`not_looked`; INVARIANT: no new `required: true` row (FR-5). Line numbers re-read on the worktree (TQ2-1 K1 edits this charter, §X).
F1/F3/F5 if the owner picks the other option: F3 (b) -> the case critic's register bullet gains "a register gap only the tester can
repair: say so in `questions[]` as a request to re-run S2 (the conductor's `rework_stage`)"; F1/F5: no line of A2 changes.
test rows: none new (role text; TESTING.md); `test_role_rules.py` and `test_role_load.py` (both fast) are the witness.
DoD: `python -B ai-packages/qa-factory/scripts/role_load.py --all --json` before/after attached; DOC-DISPATCH key-presence run (CLAUDE.md
rule 11; script in full in the report, never committed; a negative control with one key deliberately absent reports failure) over
`agents/qa-case-critic.md` with keys present, verbatim: "**The register behind the cases.**", "a requirement that folds two behaviours into
one row", "a boundary the text is silent on", "a requirement whose only source is the diff", "The register bullet is read once, on the first
review round"; keys absent: "**S2: the register.**", "**S3: the plan.**", "The stage critic of S2, S3 and S4"; over
`agents/qa-test-strategist.md` present: "no critic judges the plan", "**A changed branch no row walks.**"; over
`handoffs/s4-case-critic-to-designer.yaml` present: "work/advice-S2.json", "work/advice-S3.json". Verification:
`python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/agents/qa-case-critic.md ai-packages/qa-factory/agents/qa-test-strategist.md ai-packages/qa-factory/agents/qa-requirements-tester.md ai-packages/qa-factory/handoffs/s4-case-critic-to-designer.yaml ai-packages/qa-factory/references/role-load.json ai-packages/qa-factory/design/role-rules.json`
and the non-slow files it prints (`test_role_rules.py`, `test_role_load.py` expected); slow ones judged by CI.
`architecture: AR-10, AR-20, AR-29 -- the S4 critic told before the work in its form; ratchets as measured`. judgment: role text only.
siblings: the consumer charters (B3, another file set).

### B1 — the consumer round cap is data; one reader of a loop's cap  [builder -> critic, topic B]
owns:
C:\QAFactory\forge-repo\.claude\worktrees\sc-b1\ai-packages\qa-factory\references\stages.json (S6, S7 rows: new `acceptance_rounds: 1` only)
C:\QAFactory\forge-repo\.claude\worktrees\sc-b1\ai-packages\qa-factory\scripts\runtime_policy.py (new `repair_cap`; `cumulative_budget`: the line `:94` only)
C:\QAFactory\forge-repo\.claude\worktrees\sc-b1\ai-packages\qa-factory\scripts\controller.py (`Controller.prepare`: the cap lines `:2194-2198` only; `Controller.validate`: the cap lines `:5603-5605` and the comment `:5893-5895` only)
C:\QAFactory\forge-repo\.claude\worktrees\sc-b1\ai-packages\qa-factory\scripts\stage_status.py (`round_cap`; `line`: the call `:230` only)
C:\QAFactory\forge-repo\.claude\worktrees\sc-b1\ai-packages\qa-factory\scripts\tests\test_story_run_s6.py (new function `test_consumer_round_cap_is_data`, rows C1-C6)
non-goals: `DEFAULT_LIMITS` values; `story_progress.py` (the S5 window line, F-9); the S7 re-judge limit (`driver_stage_s7.py:1035`);
`REPAIR_LOOP_ROLES` (A1a); every driver file (B2).
edges: E-B1, E-B2, E-B3, E-B12. `stage_status.round_cap` with an unknown / empty `stage` -> today's value. INVARIANT: the line never shows a
cap the controller does not apply (FR-10: the packet's `repair_budget.cap` and the status line read the one reader). The blast radius
(F-10) is decided in this spec (E-B12): no stop-and-ask for the builder.
F1/F3/F5 if the owner picks the other option: F1 (b) keeps B1 whole (cap 1 is the owner's «один шанс» either way); F3, F5: no line changes.
test rows (in `test_story_run_s6.py`, keep `:6130`, SLOW — judged by CI): C1 `s6-runner-cap-is-1`, C2 `s7-analyst-cap-is-1`, C3
`s5-automator-cap-unchanged` (2), C4 `s4-designer-cap-unchanged` (design_repair_cycles), C5 `malformed-row-ignored` (`"x"`, `-1`, `true`,
absent), C6 `person-words-lift-the-row` (`person_words=True` at S6 runner -> 2).
DoD: rows green on the branch CI; `grep -rn "design_repair_cycles\" if" ai-packages/qa-factory/scripts --include=*.py` outside `tests/` prints
only `runtime_policy.py` (positive control: the same grep on the base tree prints the four sites); a fast local check of the reader:
`python -B -c "import sys; sys.path.insert(0, 'ai-packages/qa-factory/scripts'); import runtime_policy as R; print([R.repair_cap('qa-runner', {'roles': ['qa-runner'], 'acceptance_rounds': 1}), R.repair_cap('qa-automator', {'roles': ['qa-automator']}), R.repair_cap('qa-runner', {'roles': ['qa-runner'], 'acceptance_rounds': True}), R.repair_cap('qa-runner', {'roles': ['qa-runner'], 'acceptance_rounds': 1}, person_words=True)])"`
printing `[1, 2, 2, 2]` (a pure read, hygiene pt. 4b). Verification: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/references/stages.json ai-packages/qa-factory/scripts/runtime_policy.py ai-packages/qa-factory/scripts/controller.py ai-packages/qa-factory/scripts/stage_status.py`
and the non-slow files it prints; judged by CI: `test_story_run_s6.py` and every other slow file it prints. `architecture: AR-1, AR-13, AR-20
-- cap as data, one reader; S4/S5 byte-identical`. judgment: none. Census: `runtime_policy.cumulative_budget` and `stage_status.line` keep
class shape/data; `repair_cap` raises nothing.
siblings: S5 window cap (unchanged, C3); S4 (C4); `story_progress` S5 line (not a site).

### B2 — the gap road replaces the consumer seam; the round line; the gap warning  [builder -> critic, topic B; after FV1-22 N1]
owns:
C:\QAFactory\forge-repo\.claude\worktrees\sc-b2\ai-packages\qa-factory\scripts\driver_stage_s6.py (`consumer_completion`, `consumer_settled`, `consumer_close_words`; `consumer_exhausted` deleted; new `consumer_gap`, new `consumer_round_line`; the import line `:13`)
C:\QAFactory\forge-repo\.claude\worktrees\sc-b2\ai-packages\qa-factory\scripts\driver_core.py (new constant `GAP_PREFIX` beside `BY_PERSON` `:411` only)
C:\QAFactory\forge-repo\.claude\worktrees\sc-b2\ai-packages\qa-factory\scripts\driver_stage_s7.py (the extra list `:134-137` only)
C:\QAFactory\forge-repo\.claude\worktrees\sc-b2\ai-packages\qa-factory\scripts\driver_stage_s8s9.py (the extra lines `:76-83` only)
C:\QAFactory\forge-repo\.claude\worktrees\sc-b2\ai-packages\qa-factory\scripts\tests\test_story_run_s6.py (new function `test_consumer_gap_road`, rows G1-G9)
C:\QAFactory\forge-repo\.claude\worktrees\sc-b2\ai-packages\qa-factory\scripts\tests\fixtures\driver-layers.json (the `driver_stage_s6` rows only: `:686` deleted; `consumer_gap`, `consumer_round_line` added)
C:\QAFactory\forge-repo\.claude\worktrees\sc-b2\ai-packages\qa-factory\scripts\tests\fixtures\judgment-census.json (the `ratchet` values only, as the CI run prints)
C:\QAFactory\forge-repo\.claude\worktrees\sc-b2\ai-packages\qa-factory\changelog.d\consumer-one-round-no-barrier.md (new)
non-goals: `stage_review_exhausted` (S4 keeps it; R1 simplifies it); `person_pass`, `consumer_person_pass`, `consumer_need_record`,
`consumer_word_step`; the controller; `acceptance.py`; `brief_pack.py` (B-3: no second reader); `stage_done.py` (F6 (a): no change);
charters (B3).
edges: E-B4..E-B11; POSITIONAL B2-3 (INVARIANT stated there); B2-4 position after `BY_PERSON`; ORDER record-then-warning (B2-3 step 3);
`own()` invariant (F-5). TEMPORAL: B.5 (both worlds; the move is this node's commit).
F1/F3/F5 if the owner picks the other option: F1 (b) -> B2-3 is not applied: the five `consumer_gap` calls stay `consumer_exhausted` /
`stage_review_exhausted` calls (today's code), `consumer_gap`, `GAP_PREFIX` and the close-words branch are not added, rows G3-G5, G9 expect
the seam; B2-2 (round line, "No return is left ... the conductor decides" variant) stays. F5 (b) -> a new node routes the S4 callers of
`stage_review_exhausted` (`driver_stage_plan.py` `stage_S4`) through `consumer_gap`'s twin; B2 lines unchanged. F3: none.
test rows (in `test_story_run_s6.py`, keep `:6130`, SLOW — judged by CI): G1 `accept-unchanged`; G2 `reject-round-left-reworks-once`; G3
`reject-no-round-gap-own-completion` (record `acceptor: driver`, quote starts `gap: the one repair round`, warning `S6 was accepted with a
gap: ...` in `pipeline["warnings"]` after the record, `own()` returned, no `no_move`); G3b `gap-own-open-work-passes-through` (`own()`
returns open work -> returned as is); G4 `unreadable-word-gap` and `form-refused-gap`; G5 `uncountable-gap-no-round`; G6
`close-words-say-gap`, `scribe-brief-standing-gap-line` (the S6 warning appears in the scribe's brief as `- standing: S6 was accepted with
a gap: ...`) and `s7-gap-after-scribe-brief-reaches-gate-b` (the S7 warning is in the gate B packet's `warnings`); G7
`temporal-round-2-of-1-gap`; G8 `person-pass-wins` (control); G9 `rework-refused-gap` (E-B10); G10 `no-author-no-record` (E-B11). Each
row asserts `stage_review_exhausted` was not called (S6 and S7 each).
DoD: rows green on the branch CI; `grep -n "stage_review_exhausted\|consumer_exhausted" ai-packages/qa-factory/scripts/driver_stage_s6.py`
prints nothing (positive control: the same grep on `driver_stage_plan.py` hits); `test_driver_layers.py` and `test_judgment_census.py` green
on the branch CI with the values written. Verification: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/driver_stage_s6.py ai-packages/qa-factory/scripts/driver_core.py ai-packages/qa-factory/scripts/driver_stage_s7.py ai-packages/qa-factory/scripts/driver_stage_s8s9.py`
and the non-slow files it prints; judged by CI: `test_story_run_s6.py`, `test_driver_layers.py`, `test_judgment_census.py` and every
other slow file it prints. `architecture: AR-13, AR-14, AR-15, AR-17, AR-27, AR-28 -- one prefix home, one writer of records and warnings,
the warnings road to the report; S4 seam untouched`. judgment: a seam call removed (it carried no judgment); no check added.
siblings: S4 seam (kept); FV1-22 N1/N2, FV1-6 (§X); R1.

### B3 — consumer charters: legal returns, round line, gap  [builder -> critic, topic B]
owns:
C:\QAFactory\forge-repo\.claude\worktrees\sc-b3\ai-packages\qa-factory\agents\qa-failure-analyst.md (`:27`, `:28`, `:51`, `:76`)
C:\QAFactory\forge-repo\.claude\worktrees\sc-b3\ai-packages\qa-factory\agents\qa-doc-scribe.md (`:26`, `:51`, one Tools line)
C:\QAFactory\forge-repo\.claude\worktrees\sc-b3\ai-packages\qa-factory\references\role-load.json (the two roles' rows)
C:\QAFactory\forge-repo\.claude\worktrees\sc-b3\ai-packages\qa-factory\design\role-rules.json (rows whose carrier line changes)
non-goals: `qa-runner.md` (nothing missing, B.3); every other line.
edges: as A2. F1 (b) -> the scribe's Tools line loses its gap sentence ("a `standing:` line ... goes there too") and reads "No return
left: write the report on what you have"; F3, F5: none.
DoD: as A2 with these paths; keys present, verbatim: in `qa-failure-analyst.md` "Return the run only for what the runner was told to give",
"names the requirement it breaks and its red test", "or one seen value merge"; in `qa-doc-scribe.md` "S6 was accepted with a gap", "No
return left". Verification: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/agents/qa-failure-analyst.md ai-packages/qa-factory/agents/qa-doc-scribe.md ai-packages/qa-factory/references/role-load.json ai-packages/qa-factory/design/role-rules.json`
and the non-slow files it prints. `architecture: AR-10, AR-27 -- returns told before the work; the gap line's home named`.
siblings: FV1-24, FV1-25 (same analyst charter — §X).

### R1 — `stage_review_exhausted` loses its dead S6/S7 branches (after B2 and FV1-6)  [builder -> critic, topic B residual, F-3]
owns:
C:\QAFactory\forge-repo\.claude\worktrees\sc-r1\ai-packages\qa-factory\scripts\driver_stage_plan.py (`stage_review_exhausted` only)
non-goals: its S4 behaviour; FV1-6's door text.
edges: the `who` (`:702`) and `word` (`:744`) choices collapse to the S4 values (`qa-case-critic`, `cases_in_repair`); INVARIANT: S4's seam
text and open-work word are byte-identical; no caller other than S4 exists (grep `stage_review_exhausted(` over `scripts/*.py` outside
tests prints only `driver_stage_plan.py` S4 lines; control: the definition). If F5 (b) is chosen by the owner, R1 is void.
test rows: the S4 exhausted-review row the FV1-6 node leaves in its keep file stays green (named in R1's dispatch from FV1-6's merged
spec); no new row.
DoD/Verification: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/driver_stage_plan.py`
and the non-slow files it prints. `architecture: AR-17 -- one seam, S4 only`.

### D — docs and generated texts (after A1b, A2, B1, B2)  [builder -> critic or Lead]
owns:
C:\QAFactory\forge-repo\.claude\worktrees\sc-d\ai-packages\qa-factory\skills\qa-story\phases\s2.md (`:117` only)
C:\QAFactory\forge-repo\.claude\worktrees\sc-d\ai-packages\qa-factory\skills\qa-story\phases\s3.md (`:60` only)
C:\QAFactory\forge-repo\.claude\worktrees\sc-d\ai-packages\qa-factory\design\controller-blocks.md (generator output only)
C:\QAFactory\forge-repo\.claude\worktrees\sc-d\ai-packages\qa-factory\design\architecture.md (AR-29 `:138` only)
C:\QAFactory\forge-repo\.claude\worktrees\sc-d\docs\ARCHITECTURE_INDEX.md (generator output only)
C:\QAFactory\forge-repo\.claude\worktrees\sc-d\docs\SIBLING_MAP.md (axis 5 row `:122`, first cell only)
non-goals: kb pages (none needs an edit, A.6); `design/state-exits.md`, `design/driver.md` (no hit in this round's grep of `design/`); the
FV1-12 S2 card rewrite (§X).
edges: `SIBLING_MAP.md:122` first cell gains ", S6 runner / S7 analyst repaired once on their consumer's word (`Driver.consumer_settled`,
`stages.json` `acceptance_rounds`)"; it does NOT gain FV1-6's ", S2/S3 author/stage critic" (§X). A generator that prints nothing new ->
the file is unchanged and the report says so.
DoD: DOC-DISPATCH key-presence run (keys verbatim: absent from `s2.md` and `s3.md` "the driver dispatches `qa-case-critic` for this
stage"; present in `architecture.md` "the consumer at S6 and S7"; present in `SIBLING_MAP.md` "acceptance_rounds"; script in full, a
negative control), plus `python -B ai-packages/qa-factory/scripts/selftest.py --lang` and `python tools/architecture_index.py --check`; the
kb search repeated with its control and reported.

### Parallelism (re-checked against the edited owns; D-0048 function lists on hot files)
Prerequisites: B2 starts after FV1-22 N1 merges (N1 owns `driver_stage_s6.consumer_settled`, the same function as B2 — `очередь: FV1-22/N1
-> B2`); A2 starts after TQ2-1 K1 merges; R1 after B2 and FV1-6; A1b after A1a; D last.
Parallel sets: A1a ∥ B1 ∥ B2 ∥ A2 ∥ B3 (once their prerequisites are met); A1b ∥ B1 ∥ B2.
Function overlaps checked: `stages.json` A1a S2/S3/S4 rows vs B1 S6/S7 rows — disjoint rows. `controller.py`: A1a `REPAIR_LOOP_ROLES` +
`repair_passes`; A1b `_s3_completion_gate`; B1 `Controller.prepare` + `Controller.validate` (incl. the `:5894` comment moved from A1b to B1
for this reason) — disjoint functions. `driver_stage_plan.py`: A1a and A1b both touch `completion_for` — SEQUENTIAL (A1b from main after
A1a); B2 none; R1 `stage_review_exhausted` after B2. `brief_pack.py`: A1a only (B2 no longer edits it). `acceptance.py`: A1b only.
`driver_stage_s6.py`: B2 `consumer_*`; FV1-6 `person_pass` + `time_stamp` — disjoint. `test_story_run_s6.py`: B1
`test_consumer_round_cap_is_data`, B2 `test_consumer_gap_road` — disjoint new functions. `test_story_run_s3_windows.py`,
`test_field_producers.py`: A1a and A1b — sequential. `role-load.json` / `role-rules.json`: A2 three roles, B3 two roles — disjoint rows,
the later merges main. `driver-layers.json`: A1b route rows vs B2 s6 rows — disjoint rows. `judgment-census.json` `ratchet` (one JSON line):
A1b and B2 may both move it — the LATER merge re-reads its CI print after merging main and writes the printed values (D-0048 later-merge
rule). One critic pass per topic (R13-g): topic A (A1a+A1b+A2), topic B (B1+B2+B3+R1).

## §X. Crossings (notes for the Lead; no other file edited)

- TQ2-1: only K1 (`wip/tq2-1-k1`) touches `agents/qa-case-critic.md`, `design/role-rules.json`, `references/role-load.json`; A2 starts AFTER
  K1 merges (F-13: K2 touches `critic_rollcall.py`, `s5_plan.py`, `s5_precheck.py` — no A2 file); line numbers in A.2 are re-read there.
- FV1-6 (`docs/tasks/specs/20261113-fv1-6-s2-door-back-to-tester-spec.md`): its seam survives for S4 ONLY. Changes: title -> "after an
  exhausted S4 case review"; §1 AR-19 line -> S4 only; §2.1/§2.2 become the motive only; §2.3 rows S2, S3, S6, S7 die (S4, S5, S7-test rows
  stay); §5 R rows "at S2 and S4" -> S4 only; the R1 row (`OpenWork("stage_in_repair")` at S2) dies; siblings drop S3/S6/S7; the
  `driver_stage_s6.py` `person_pass`/`time_stamp` owns line stays valid (S4 reads times). ITEM 14 (`docs/SIBLING_MAP.md:122`, "append
  ', S2/S3 author/stage critic'") is the SAME line as node D and is now WRONG: it is dropped from FV1-6 (F-13); node D writes the row.
  FV1-6 also owns `judgment-census.json` (its spec `:222`): the later merge re-reads the CI print. Residual R1 runs after FV1-6. The
  finding's name no longer matches; the Lead re-cuts or closes it as "S4 only".
- FV1-22 (`docs/tasks/specs/20261113-fv1-22-s7-acceptance-loop-spec.md`): N1 SURVIVES and is a PREREQUISITE of B2 twice — in practice
  (without it the analyst's verdict is unreadable and every S6 acceptance becomes a gap) and by owns: N1 item 7 owns
  `driver_stage_s6.consumer_settled` (its spec `:149`, `:188-189`) — `очередь: FV1-22/N1 -> B2`. N1's edges that route an unreadable word
  "to `stage_review_exhausted`" (`:188-189`, `:218`) CHANGE to "to the gap road (B2-3)" — B2 makes that change in `consumer_settled` after
  merging N1. N2: its consumer part (`person_pass` on the `stage_acceptance_write` refusal, rows N2-a/N2-g) DIES for S6/S7 (the refusal now
  takes the gap road); its every-stage same-set stop survives for other refusals; row N2-f must use another stage than S2. N4 unaffected.
  Live proof row "S6 recorded `accept`" stays.
- FV1-24 (S6/S7 charters): same files as B3 -> sequential; recommended B3 first (narrow) or folded into FV1-24.
- FV1-25 (`agents/qa-automator.md`, `agents/qa-failure-analyst.md`; batch `:54`): the same analyst charter as B3 -> `очередь: B3 -> FV1-25`
  (or the reverse; the later merges main and re-measures `role-load.json`).
- FV1-28 (`scripts/brief_pack.py`, `first_look.py`; batch `:61`) and FV1-29 (`agents/qa-automator.md`, `scripts/brief_pack.py`; batch `:62`):
  `brief_pack.py` is shared with A1a (`TRIED_READERS`, `stage_critic_names`, `FIRST_LOOK_KIND` S3 row). Not a hot-file list file; owns must
  name functions: if either node touches `FIRST_LOOK_KIND` or `stage_critic_names`, `очередь: A1a -> FV1-28/FV1-29`.
- FV1-12 (batch `:59`; owns `skills/qa-story/phases/s2.md` and `references/stages.json`, the S2 row): same S2 row as A1a and the same card
  as node D -> `очередь: A1a -> FV1-12` (or fold D's `s2.md:117` edit into FV1-12). The owner's word recorded in the FV1-12 finding
  (`20261112-s2-kartochka-i-reestr-stadij-rashodyatsya.md`, branch `wip/owner-words-1113b`, `f876a5c`) — «нужен ли приёмщик у реестра
  требований — владелец не говорила, стоит как есть в `stages.json`» — is superseded by the owner's word of 13.11 (§0: removed); the Lead
  notes it in the FV1-12 finding.
- T1 topic (census / stage-joints rows): A1a changes `stages.json` roles that `stage_joints.py` reads (`:120`, `:300` read `advice`); A1b
  changes `judgment-census.json` ratchet values; a T1 node editing the same rows goes after A1b (`очередь: A1b -> T1/<node>`).

## §F. Forks (returned; options, cost, recommendation)

- F1 (OWNER, open) — the reading of «не должно быть барьером» (§0). (a) RECOMMENDED the gap road (B2): no seam, no person, a factory-defect
  line in the report / at gate B; cost: a consumer that could not use the data proceeds on less, the report says so. (b) the seam stays at
  an exhausted consumer review (today) with one round instead of two; cost: the barrier the owner named. Nodes written on (a); B1, B2, B3,
  R1 name their (b) lines.
- F2 (Lead) — DECIDED (a): `acceptance_reads` S3 `["advice"]`.
- F3 (OWNER, open) — a register defect found at S4. (a) RECOMMENDED no road back: case-level verdicts + `questions[]` to the register/gate A
  (A.2.4); (b) the conductor's existing `rework_stage` of S2 from S4 — costs a re-run of S2, S3 (two windows) and S4 per use, the barrier
  the owner removed. A2 names its (b) line.
- F4 (Lead) — DECIDED (a): the ordinary road for T1/T3 (F-14: T1 may be closed by `stage_repairs`, cheaper).
- F5 (OWNER, open) — S4's exhausted review keeps the seam while S6/S7 take the gap road. A difference selected by the consumer relation
  (`acceptance.consumer_of`) plus the owner's word said of consumer acceptance only («оставляем как раньше» for the rest). (a) RECOMMENDED
  keep as designed; (b) put S4 on the gap road too — cost: an exhausted case review no longer reaches the person (contradicts the S4
  non-goal). B2 and R1 name their (b) lines.
- F6 (Lead, NEW in this round — returned because the verdict's B-3 text contradicts the code) — how the gap warning is written. The verdict
  says "`consumer_gap` adds `--warn` to the SAME `stage_done.py --acceptance` call"; FACT: `stage_done.py:1549-1553` returns
  `record_acceptance(...)` for `--acceptance` and ignores `--warn` (warns reach `apply_facts` only on the `set_facts` road `:1562-1569` or
  a stage transition `:1571-1573`), so the edit as written would drop the warning silently. (a) RECOMMENDED two calls of the same writer in
  fixed order — the record, then `stage_done.py --task <T> --warn "<line>"` (no `stage_done.py` change; one writer kept; a refused warning
  write takes E-B7's road); (b) teach `record_acceptance` to take `warns` so one call writes both (atomic; costs a `stage_done.py` edit,
  `main` `:1549-1553` and `record_acceptance`, plus a row). B2 is written on (a); (b) changes B2-3 step 3 and adds `stage_done.py`
  (`main`, `record_acceptance`) to B2's owns.

## §S. Small choices closed by the designer

- `acceptance_reads` as a map `{stage: [parts]}` so S3 contributes only its advice.
- `s3_ticket_completion`'s `closes` parameter dropped (dead after A1a).
- `_act_prepare_stage` sends S2 to `stage_simple` explicitly.
- `consumer_exhausted` deleted rather than rewritten.
- Gap quote cut at 400 characters (the form stays on disk).
- Cap reader in `runtime_policy` (where `DEFAULT_LIMITS` lives), stage row passed in by callers.
- Uncountable rounds -> no round, recorded as a gap.
- K10 split of A1 into A1a (behaviour) and A1b (dead code), one critic pass (verdict K10).
- F-7: `GAP_PREFIX` beside `BY_PERSON` in `driver_core.py` (option 1 of F-7: no move, no new `acceptance.py` reader; after B-3 its only
  reader is `consumer_close_words`, the same reader as `BY_PERSON`).
- F-10: `acceptance_rounds` does not bind a packet with `person_words: true` (the option adding no new refusal — Lead decision 2).
- `test-layers.json` `covers` entries of deleted files removed by hand (a `covers` entry is not a keep row; `quarantine`/`cohorts` untouched).
- `controller.py:5894` comment correction moved from A1 to B1 (it sits in `Controller.validate`, which B1 owns).

## §Q. Queue lines for the Lead (not nodes of this spec)

- AR-1 residual: `brief_pack.TRIED_READERS` is closed variety in code; moving it into `stages.json` beside `acceptance_reads` (migrating the
  S9 row) is a design change with its own critic pass (verdict B-1 larger option).

## §O. Owner's notices (the Lead tells the owner)

1. Quarantined tests (never edited here; deletion only by the owner's word, `tools/test_quarantine.py purge`):
   - WHOLLY dead with the S2/S3 route: `scripts/tests/test_stage_critic_route.py` (`test-layers.json:9948`).
   - PARTLY stale (keep S4/S6 rows, judged by `quarantine-watch`): `test_controller_stage_acceptance.py` (`:7712`; S2/S3 rows incl. `:110`),
     `test_brief_pack_roles.py` (`:7294`; X2-1 rows `:405-425`), `test_acceptance_semantics.py` (`:7162`), `test_repair_route.py` (`:9400`),
     `test_handoff_init_author.py` (`:8438`; `:16` tuple keeps S4, `:43`, `:85-89`, `:122-174` name `s2-stage-critic-to-tester`),
     `test_rows_owed.py` (`:9612`; `:46` tuple keeps S4, `:112` S2/S3 only) (F-12).
   - Name-only (not stale): `test_open_vocabularies.py` (`:8984`; a test name says "stage critic").
2. Quarantined tests that go stale under Part B (the consumer seam rows): `test_stage_acceptance_consumer.py` (`:9931`),
   `test_consumer_close_route.py` (`:7670`), `test_stage_review_person_pass.py` (`:9974`, its S6 rows), `test_s7_repair_review.py`
   (`:9786`) and `test_story_run_repair_limit.py` (`:10145`) where they stub the consumer cap.
3. The Lead's reading of «не должно быть барьером» (§0, F1).
4. Forks F1, F3, F5 are the owner's (open); F2, F4 the Lead's (decided); F6 the Lead's (new, recommended (a)).
5. FR-33: one `live-runs` row — a story where S2 and S3 close with no critic, S4's critic reads the register and both forms, and S6 or S7 is
   returned once and then accepted with a gap shown under "Factory defects" (S6) or at gate B (S7).

## §T. Reading trail (searches with positive controls)

Round 0 (draft): as in the draft's trail (charters, `stages.json`, driver/controller/acceptance/brief_pack/exit_gate ranges, FV1-6/FV1-22
specs, SIBLING_MAP axis headings, `test-layers.json` ranges).
Round 1 (this fix round, on read-main after wave 3): the verdict whole; the spec whole; `brief_pack.py:112,1812-1827,3560-3649,4001,4312-4313`;
`driver_stage_plan.py:106-139,1005-1143` + the def list; `driver_s0.py:483-552`; `story_step.py:890-911`; `stage_guard.py:3074-3091`;
`stage_done.py:905-939,1540-1574` + `--warn`/`warns` grep; `gate_brief.py:2249-2268`; `driver_stage_s6.py:323-402` + def list;
`driver_machine.py:578-617` + `_wait_then_critic` grep; `controller.py:235-238,745-768,3744-3759,3905-3941,5590-5664,8516-8562` + def list +
`words_given`/`stage_closes_with`/`.recover()` greps; `runtime_policy.py:85-99`; `stage_status.py:55-79,205-239`; `story_progress.py:345-360`;
`stages.json` rows (grep + `:66-160`); `handoffs/s4-case-critic-to-designer.yaml` grep; `agents/qa-case-critic.md` whole;
`open-vocabularies.json:1-6`; `block-names.json:30-43`; `architecture.md:130-143`; `SIBLING_MAP.md:120-123`; `driver-layers.json` grep
`:525-538,680-688,784`; `judgment-census.json:1-8` + file greps; `slow_tests.json` whole; `test-layers.json` section heads, `:1-30`,
`:970-979`, `:1680-1719`, `:5038-5055` + file-name greps (keep ends `:7107`, quarantine from `:7161`); tests `test_first_look_step.py:608-652`,
`test_question_register.py:1918-1937`, `test_handoff.py:662-681`, `test_field_producers.py:550-579`, `test_open_vocabularies.py:340-364`,
`test_scenario_local_1_arm_b.py` whole, `local-1-arm-b/story.json:1-60`; `plans/piles/live-run-fvf/batch-1-live-run-fvf.md:36-90` (root and
read-main; FV1-28/29 only on read-main); FV1-6 spec greps (`SIBLING_MAP`, `driver_stage_s6`, census); FV1-22 spec grep.
Searches (Grep tool; code tokens case-sensitive, text case-insensitive where marked): S2/S3-only tokens over the package (control: the
definitions and `brief_pack.py:4001`); `stage-critic-to|stage_critic` file list (control: the two yamls); `advice_read` over
`*.py|*.json|*.yaml` (control: the S4 yaml); `design_repair_cycles` (control: `runtime_policy.py:13`); `round_cap\(` (control: definition);
`BY_PERSON` (control: `driver_core.py:411`); `ticket_rework_step` and `consumer_completion|consumer_settled|repair_budget|round_cap` counts
over tests (control: driver-layers hits); kb `stage critic|qa-case-critic` -i (control: hits on S4) and `consumer` -i; `design/` -i for the
route names (control: `controller-blocks.md:229`); phases -i (control: `s2.md:117`).
Not verified (estimates): whether `next` names `recover` on its own for a T1 state (the driver runs it at `driver_machine.py:477`, `:2076`;
not traced further — T1's rows pin `stage_repairs`, the pure function); the exact census count after A1b/B2; the role-load deltas;
`scenario_walk.py --witness-for` outputs (not run: this designer has no shell; each node runs it first).
Needed beyond the manifest: `scripts/slow_tests.json`, `plans/piles/live-run-fvf/batch-1-live-run-fvf.md` (read-main copy).

## §R. Fix round (critic-on-plan verdict, 13.11.2026)

| item | what changed | where |
|---|---|---|
| B-1 | `author_form` dropped; `acceptance_reads` = `{"S2": ["outputs", "advice"], "S3": ["advice"]}`; the tester's form reaches the S4 critic through a new `TRIED_READERS` row, reader unchanged (Lead decision 1); the `stages.json` move queued | A.2.3, A.4, §1.1 AR-1/AR-15/AR-22, A1a owns/J1, §Q |
| B-1b | the S3 strategist is in the same `TRIED_READERS` row; AR-22 row names both forms | A.2.3, §1.1 AR-21/22, A1a J1 |
| B-2 | the seven live checks owned by the node whose change turns them red, with expected values: `stage_guard` selftest -> `["S4"]` (A1a); `test_first_look_briefs` / `_wiring` / `test_brief_s3_roster` S3 critic entries leave (A1a); `test_handoff.py:670`, `test_question_register.py:1928` -> S4 only, `test_story_run_first_look.py:44` -> `s3_window` only (A1b, with the contract deletion / `s3_author_done` removal). Found in this round, same class: `test_field_producers.py:562-569` negatives (A1b), `test_first_look_step.py:612-643` (A1b), `test-layers.json:1701,1703` covers (A1b) | A.1, A1a, A1b |
| B-3 | APPLIED IN GOAL, MECHANISM RETURNED: the gap goes by `pipeline["warnings"]` (one writer `stage_done --warn`), B2-5's second reader deleted, scribe charter names the `standing:` line, G6 `s7-gap-after-scribe-brief-reaches-gate-b` added. The verdict's "same `--acceptance` call" contradicts `stage_done.py:1549-1553` (`--warn` ignored there) -> fork F6, nodes written on F6 (a) | B.1, B2-3, B2-5, B.3, B2 rows, §F F6 |
| B-4 | (a) `ticket_rework_step` author = `roles[0]` for every stage (A1a owns `driver_s0.py`), T4 in A.5 and a T4 row; (b) the T2 rule moved BEFORE the `ticket_changed` branch, T2 rows for `ticket_changed` critic dispatches | A.1, A.4, A.5, A1a |
| B-5 | (a) A2 owns `s4-case-critic-to-designer.yaml`: `advice_read` placeholder names every advice file, non-required `inputs` rows, absence edge; (b) `:95` scope sentence added and owned by A2 | A.2.2, A2 |
| B-6 | slow keep files (`scripts/slow_tests.json`) are never in a verification run; their keys are read from the branch CI; local witness = the non-slow files `--witness-for` prints (Lead decision 4) | §N common, every node DoD |
| B-7 | FV1-12 crossing added (`очередь: A1a -> FV1-12`, superseded owner's line noted) | §X |
| F-1 | `driver-layers.json:784` added to A.4/A1b; B2 owns the `driver_stage_s6` rows (`:686` out, two in) | A.4, A1b, B2 |
| F-2 | census line references the CI print of `test_judgment_census.py`; B2 owns the `ratchet` values; later-merge rule for the shared line | A.4, A1b, B2, §Parallelism |
| F-3 | residual node R1 (owns `stage_review_exhausted`, after B2 and FV1-6); A.1's "the word stays" corrected | A.1, A.4, R1 |
| F-4 | E-B10 + row G9 | B2-3, B.4, B2 rows |
| F-5 | `own()` invariant stated + row G3b | B2-3, B2 rows |
| F-6 | author from `acceptance.stage_author_dispatch`; empty -> no record, one line, `own()` (E-B11, G10) | B2-3, B.4 |
| F-7 | option 1: `GAP_PREFIX` beside `BY_PERSON` in `driver_core.py`; no `acceptance.py` change (named in §S) | B2-4, B2 owns |
| F-8 | strategist line and AR-29 text no longer claim a plan reviewer | A.3, A.6, §1.1 AR-29 |
| F-9 | `stage_status.round_cap` gains optional `stage` from `line`; `story_progress.py` dropped (S5 line); "four sites" made true | B.1, B2-1, B1 |
| F-10 | decided by Lead rule 2 (no new refusal): `acceptance_rounds` does not bind a `person_words` packet (E-B12, row C6); the residual (a conductor's own test_defect rework) named | B.1, B2-1, B.4, B1 |
| F-11 | B1, B2, D owns written as absolute paths with function lists; `--witness-for` not run by this designer (no shell) — each node runs it first | §N |
| F-12 | `test_handoff_init_author.py`, `test_rows_owed.py` added to §O (partly stale) | §O |
| F-13 | crossings FV1-25, FV1-28 (+ FV1-29 found), FV1-6 item 14 (dropped: same line as D and now wrong); TQ2-1 "after K1" | §X, §Parallelism |
| F-14 | T1 states which road fires (`stage_repairs` vs re-run) with rows T1 / T1-b in the fast keep file `test_stage_closure.py`; F4 cost corrected | A.5, A1a, §F F4 |
| F-15 | A2's grep replaced by a verbatim key-presence run with a negative control (B3, D too) | A2, B3, D |
| K10 | A1 split into A1a (data, temporal rules, hand-over, live tests) and A1b (dead code, driver-layers, census); one critic pass for topic A | §N A1a/A1b, §Parallelism |

Found in this round beyond the verdict (applied): FV1-22 N1 owns `consumer_settled` (B2 queued after N1, §X); `controller.py:5894` sits in
`Controller.validate` with B1's cap lines (comment moved to B1); `stage_done.py:1551` message (A1b); `controller.py:758` comment (A1a); the
local-1-arm-b scenario has no S2/S3 critic step (A.1, judged by CI); kb needs no edit (A.6). Counts: 24 items — 23 applied as written or by
the Lead's decisions, 1 (B-3) applied in goal with its mechanism returned as F6.

Forks returned in this round: F1, F3, F5 (owner's, open, nodes on the recommendation, reversible lines named per node); F6 (Lead, new:
how the gap warning is written — B-3's text contradicts `stage_done.py:1549-1553`; recommended (a) two calls of the one writer).
