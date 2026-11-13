# FV1-6 — the door "one more round to the author with the critic's words" after an exhausted stage review (draft spec)

Status: DRAFT by designer for the Lead of pile `live-run-fvf`, 13.11.2026; FIX ROUND after the critic-on-plan verdict
(`docs/tasks/specs/reviews/20261113-fv1-6-plan-critic.md`, NEEDS WORK, B1-B4, A1-A12) — what changed is listed in §10. Lead
decisions taken as given: F1 (a), F2 (a), F3 (a), F4 (a) with the residual node as a finding text (§10.4), F5 and F6 as findings.
The node stays ONE node (§5). Node row: `plans/piles/live-run-fvf/batch-1-live-run-fvf.md:39`; finding:
`plans/piles/live-run-fvf/findings/20261112-s2-net-dveri-vernut-rabotu-testeru-so-slovami-kritika.md`.

Every file:line below is read on `.claude/worktrees/read-main` = origin/main `e4ba384`, under `ai-packages/qa-factory/scripts/`
unless another path is given. The builder's worktree is `C:\QAFactory\forge-repo\.claude\worktrees\fv1-6` (the Lead creates it from
origin/main); line numbers there are the same until another node merges.

## 1. Frame

- AR-n touched (each with the change check written into the DoD, §5.4):
  - AR-25 (every recorded state has a way out) — the state "stage review rejected, no repair round left" gets a reachable move to
    the author; change check: rows F1/F4/F5 prove `rework_stage` open at that seam, rows R1/R2 prove the chosen round runs.
  - AR-17 (one seam to the conductor) — the round is offered through `no_move`, no new question site; change check: no new
    `Person(` site and no new question key in the diff (B1's edit is inside the existing builder `_person_of`).
  - AR-19 (stage twins change together) — ONE function, `stage_review_exhausted`, serves S2, S3, S4 and the S6/S7 consumer
    reviews; no stage name enters code; change check: R rows at S2 and S4 in the same table.
  - AR-24 / FR-8 / FR-49 (a person's words reach whatever acts on them, whole) — the person's words go by file, the reviewer's
    verdict by its form path, never cut; the code's preface travels as `extra` lines on every length; change check: rows L1/L2 AT
    and BEYOND 1500 characters of the person's words.
  - AR-14 (one artifact, one writer) — `state["seam_rework"]` keeps its one writer `record_seam_rework` (and `drop_record`);
    change check: the re-entry re-records through that writer, no direct dict write (critic reads the diff).
  - AR-13 (a fact with a reader is read through it) and AR-15 (one survivor) — the critic's start through
    `Controller._dispatch_starts` + `stamp_utc` (already read at `driver_stage_plan.py:711-715`); ONE time normaliser
    `DriverStageS6.time_stamp` (hoisted from `person_pass`'s nested `stamp`, `driver_stage_s6.py:273-283`) serves both the pass and
    the choice; the person's pass read through `waiver.split_overridden` (`waiver.py:202`), the ONE reader; change check: R3-R6,
    R15, R16 green and `grep -n "fromisoformat" driver_stage_plan.py` adds no hit.
  - AR-28 / FR-59 / FR-41 / FR-58 (an unknown never becomes a pass, nor a stated fact) — an unreadable time or start honours no
    recorded choice; the preface states only a verdict word the code READ, never "rejected" on the unreadable road; change
    check: R5, R6, R11, R12.
  - AR-1 (closed variety is data) — the `rework_stage` row's `precondition` / `forbidden_when` (`references/conductor-actions.json:73-74`)
    is aligned with the code's one exception, so data and code say the same (FR-10); `FINISHING_WHYS` stays a code constant (code's
    own vocabulary, the `EXCLUDED_KINDS` precedent `no_move.py:36`); change check: row F10 reads the data row's text.
  - AR-12 (friction is measured; code that makes a stage dearer is a defect) — the cause rule reaches the conductor (B4) so the
    predictable refuse-and-re-ask round trip is not the common path; change check: row F11.
  - AR-20 (shrink-only ratchets) — touched ONLY if `test_judgment_census.py` demands a new row (§4); then the raise is named in the
    report and the commit message (axis 18).
  - AR-29 — checks added/altered, their owner and census class: the table in §4.
- SIBLING_MAP axes (rule 10(b), enumerated here per A9; the builder's commit message carries the full axis block):
  - axis 5 (stage twins; the row "Author + critic repair loop", `docs/SIBLING_MAP.md:122`): covered — the row gains the S2/S3
    stage-review loop and the S6/S7 consumer reviews (in owns, §5.1 p.11);
  - axis 18 (in-tree shrink-only ratchets, `:386`): covered — conditional on a census row (§4); a raise is named;
  - axis 32 (where judgment lives, `:557`): covered — §4: no check decides a role's or the person's question;
  - axis 34 (one road for one action, `:582`): covered — one function and one fact for the five review sites; the S5/S7 `round`
    road difference is F4, its residual node written in §10.4.
- Owner principles: FR-57/P15, FR-40/AR-25, P22/FR-48, FR-8/AR-24, P31/AR-19, P18, P13, P27/AR-29.

## 2. Facts (read on read-main e4ba384, 13.11.2026)

### 2.1 What happens at S2 at the limit today

- S2 runs the tester, then the stage critic's route: `driver_stage_plan.py:583-593` (`stage_S2` -> `stage_critic_route`).
- The round limit: `stage_critic_route` reads `budget_or_none` -> `counted`, `cap` (`driver_stage_plan.py:609-611`); the cap the
  controller applies is `policy["repair_cycles"]` (`design_repair_cycles` for a role with "case") (`controller.py:5603-5605`), default
  `2` (`runtime_policy.py:13`). Not a project config key. The S2/S3 authors are in `REPAIR_LOOP_ROLES` (`controller.py:235-237`).
- A `reject` on the last round goes to `stage_review_exhausted` from INSIDE the critic's `complete` callable, BEFORE `finish`
  (`driver_stage_plan.py:653-679`, call at `:678`). So the critic's dispatch is still `running` while the seam asks.
- `stage_review_exhausted` (`driver_stage_plan.py:691-747`): its docstring (`:693-697`) and lead (`:707`) name three moves —
  accept with the gap, "one more round on the person's words (`rework --reason`, a cause that is not `test_defect`)", or ask. The
  cause rule lives ONLY in the docstring (B4). Order: `since` = the critic's journalled start (`:711-715`); the person's `go on`
  pass `person_closes` (`:717-726`), first check `:727-729`; `self.no_move(state)` (`:730`); then facts: a driver accept -> None
  (`:733-734`), the pass -> None (`:735-736`), a new author dispatch after the critic -> `OpenWork("stage_in_repair" |
  "cases_in_repair" at S4)` (`:743-745`), else the priced fallback (`:747`). Note: the local `line` (`:705`) is the
  `STAGE_ACCEPTANCE_PHRASE` line the pass is matched against.
- It is also reached with `unreadable=True` (no dispatch id, or a verdict word the table does not know): `driver_stage_plan.py:666-670`,
  `:806-810`, `driver_stage_s6.py:357-358`. The consumer road with a reject and no round (or none countable):
  `driver_stage_s6.py:333-341` (`consumer_exhausted`), from `consumer_completion` `:343-369`. S4 last round: `:814-821`.
- ROOT CAUSE: the move `rework_stage` is open only when no dispatch runs: `no_move.rework_blockers` (`no_move.py:98-111`; `running`
  must be `False`, `:105-106`); the fact `running` = any controller dispatch with status `running` (`driver_conductor.py:389`); the
  data row says the same (`references/conductor-actions.json:73` "no dispatch running", `:74` "a dispatch is running"). At this seam
  the running dispatch is the critic itself, so `rework` is NEVER open here: the round the docstring promises is unreachable on all
  five sites. `release_and_restart` IS open (`no_move.py:142-143`: the critic's dispatch is live, `attempts == 0`) — that is the
  `restart` the operator got.
- The controller refuses ANY new dispatch while another runs (`controller.py:5465-5486`, `apply` branch `dispatch`: "sequential task
  already has an active dispatch", raised BEFORE any event). `Driver.rework` registers through it (`driver_dispatch.py:2672`). So a
  rework can be RECORDED at this seam but RUN only after the critic's finish (B2).
- The answer roads (`driver_machine.py`): `take_seam_answer` `:2335-2386` — a token not offered -> `unread(...)` `:2370-2372`; an
  offered token -> `seam_chosen` `:2388-2435`: `rework` with `args` -> `record_seam_rework` (`:2426-2427`, writer
  `driver_conductor.py:733-752`); `rework` without `args` (and every other conductor move) -> the `why: chosen` call (`:2428-2435`,
  `no_move` at `:2432`). `unread` builds `why: unread_answer` (`driver_conductor.py:852-870`).
- Every Person the seam raises stores `why = state["why"]` (`_person_of`, `driver_conductor.py:419-438`, the field at `:428`); `ask`
  writes it to `asked.why` (`driver_dialog.py:327`), `held_question` restores it (`driver_dialog.py:622`). These are the ONLY readers
  of `asked.why` / `person.why` in `scripts/*.py` (grep, trail §9). So the origin `stage_review_exhausted` is lost at the first
  re-ask (B1).
- What the conductor reads: `_conductor_text` (`driver_conductor.py:679-687`) = `lead` + `NM.moves_section(...)` + `text` (+ the
  person's choice paragraph `chosen_note` `:706-722` on a `chosen` call). `moves_section` (`no_move.py:257-285`) says "Only these may
  be offered or taken now" (`:264-265`) and prints the `rework` closed list through `rework_args_list` (`:208-225`). "Do not run the
  rework yourself" is said only in `chosen_note` (`:719-721`).
- The cap past which `test_defect` is refused: `controller.py:5639-5663` (needs the person's pass for BOTH roles, `waiver.py --block`,
  the refusal prints the keys); a cause other than `test_defect` spends none of the cap (`controller.py:5608-5610`) and needs a
  `reason` (`:5597-5601`). The data row already says the pass rule (`conductor-actions.json:73`, from "A test_defect round past the
  repair cap first needs the pass ...").
- The chosen rework is run by `seam_rework_step` (`driver_machine.py:578-616`), which waits while any dispatch runs (`owed_rework`,
  `driver_s0.py:550-559`, the test at `:557`). So a recorded choice runs only AFTER the critic's finish.
- The preface is joined in front of the person's words into `reason` (`driver_machine.py:606-607`); `Driver.rework` sends
  `--words-file` instead of `--reason` when a words file is named (`driver_dispatch.py:2659-2660`; `reason[:1500]` only without one),
  and replaces a reason over 1500 characters by a `line` naming the words file (`:2681-2683`); the prompt takes `line` OR `reason`
  (`:637-638`) — a preface on long words is dropped silently today (also on the exploratory road, record at `driver_machine.py:2742`).
  `extra` lines reach the prompt on every length (`driver_dispatch.py:704`).
- After the critic is accepted with `OpenWork` on the last round, neither owed-round helper fires over the person's round:
  `stage_repair_owed` is gated by `not last_round` (`driver_stage_plan.py:612`), `s4_repair_owed` likewise (`:545`).

### 2.2 Real-run evidence (fvf, LR2-1, 12.11.2026)

- `experiments/mybooks/factory-vs-free-agent/runs/factory-4.log:57`: `conductor: ask_person — ... No state-changing command run:
  rework is not an open move, so every way forward needs the person's word.`
- `:59-87`: the question (kind conductor, S2, dispatch `S2-qa-case-critic-3`); options `go on` / `restart` / `retry` / `stop`; no
  round for the tester.
- `experiments/mybooks/factory-vs-free-agent/notebook.md:205-212`: the `restart` answer restarted the CRITIC, same verdict at
  18:13; S2 then accepted with the gap (`answers/s2-critic-go-on-with-gap.md`).

### 2.3 Stage twins: how each leaves "rounds spent" TODAY

| Stage / loop | Site (file:line) | Exit offered today | Door to the author? |
|---|---|---|---|
| S2 stage critic | `driver_stage_plan.py:678` -> `:691` | conductor seam; `rework` closed by `running` | no |
| S3 stage critic | `driver_stage_plan.py:117,122,131` (critic-verified on e4ba384) -> the same `stage_critic_completion` `:678` | same | no |
| S4 case critic | `driver_stage_plan.py:814-821` (`s4_critic_completion`) -> `:691` | same | no |
| S6 consumer (S7 failure analyst judges S6) | `driver_stage_s6.py:343-369` (`consumer_completion`) -> `:333-341` / `:357-358` -> `:691` | same | no |
| S7 consumer (doc scribe judges S7) | the same `consumer_completion` road | same | no |
| S5 test window (code critic) | `driver_dispatch.py:3052` (`repair_limit_gate`), offer `round/debt/fixed/stop` `:3099` | site closed question `s5.repair_limit` (`question-prices.json:155`); `round` records the passes (`driver_dispatch.py:3198-3200`) | yes, another road |
| S7 failing test repair | `driver_stage_s7.py:1122-1131`, offer `round/debt/stop` `:1152` | the same machinery, key `s7.repair_limit` (`question-prices.json:187`) | yes, another road |

Related, not this class: the conductor's own refusal rounds, `WINDOW_ROUND_CAP = 2` (`driver_machine.py:45`), S5 only; the exit
limit `exit.resume_limit` (`question-prices.json:175`) is a separate road.

## 3. Design (on the decided forks F1-F4 (a))

1. The fact `running` stops counting the ONE dispatch whose finish the seam sits inside. A new module constant in `no_move.py`,
   `FINISHING_WHYS = ("stage_review_exhausted",)`. `no_move_facts` computes `finishing` = `state["dispatch"]` when it is non-empty and
   `state["why"]` or `state["asked_why"]` is in `FINISHING_WHYS`, else `""`; `running` counts every `running` dispatch whose id is not
   `finishing`; the new fact `facts["finishing"]` carries that id (`""` when none). Then `rework` is open (with the closed `args`
   list) at the first call, at the `unread` call and at the `chosen` call — and on every later hop (point 2).
2. The question's ORIGIN survives every re-ask (B1): `_person_of` stores `person.why = asked_why or why`; the two answer roads of a
   seam question pass the question's own `asked.why` as `asked_why` (`take_seam_answer` -> `unread(asked_why=)`, `seam_chosen` -> the
   `chosen` state). Since an `unread`/`chosen` question now stores the ORIGIN as its `why`, the next answer carries it again: the chain
   closes for any number of hops.
3. `rework` is OPTION-ONLY while the reviewer finishes (B2): when `facts["finishing"]` is non-empty, `moves_section` prints, right
   under the `rework` closed list, one line: offer it; the driver records the person's choice and runs it after `<id>` finishes;
   running it yourself now is refused. The same line carries the cause rule (B4, point 4). The lead of `stage_review_exhausted` says
   "offer the person one more round for {author}" instead of "one more round on words you ground", its docstring describes the
   offer road, and the data row's `precondition` / `forbidden_when` name the one exception. The moves section is rendered on EVERY
   conductor call (`_conductor_text`), so the line reaches the first, `unread`, `chosen` and args-refused calls through one carrier.
4. The cause rule reaches the conductor (B4) in that same line, in words that are true whether or not the cap is spent (the
   unreadable road may have rounds left): past the author's repair cap the controller takes a `test_defect` round only after the
   person's pass for both roles is recorded (the `rework_stage` row says how); a cause other than `test_defect` needs no pass; which
   cause fits the person's words is the conductor's judgment. `check_args` still checks only the closed list (AR-2).
5. The critic's finish does not ask again once the person chose a round, and the later of two recorded words wins (A1): in
   `stage_review_exhausted`, BEFORE the first `person_closes(author_last)` check, a pending `state["seam_rework"]` whose `at` is later
   than the critic's start is HONOURED unless the person's `go on` pass (read through `waiver.split_overridden`, never recorded here)
   is strictly later than it. An honoured choice re-records itself through `record_seam_rework` with one preface line naming the
   reviewer's form (worded per B3), and the function returns `OpenWork(word, ...)` (the same word as the post-conductor branch). A
   pass that is later wins: the existing `person_closes` closes the stage, and the pending choice is dropped through `drop_record`
   with a printed line.
6. The preface is never dropped (A3): `seam_rework_step` passes `reason` = the person's words and `extra` = the preface lines, on
   every length. No new constant; `Driver.rework` is not edited.
7. Nothing else changes: the moves' other rows, the prices (`rework_stage`: `stages_again` / `answer` / `waits`,
   `conductor-actions.json:75-77`), the fallback block, the controller, `driver_dispatch.py`.

Flow after the change (S2, the run of 12.11): critic rejects on round 2 of 2 -> seam: moves open now include `rework` with the
option-only/cause line -> the conductor offers e.g. `rework` (S2, qa-requirements-tester, a cause it judges), `go on`, `restart`,
`stop`, each with its three price lines -> the person answers `rework` -> `record_seam_rework` (critic still running) -> next
process: `seam_rework_step` waits (`owed_rework`, critic running) -> `where` -> `wait_existing_job` -> `_finish_saved_result`
(`driver_machine.py:1445-1470`, `:1522`) -> `completion_for` (`driver_stage_plan.py:1011`, S2/S3 `:1042`, S4 `:1114`) ->
`stage_review_exhausted` sees the choice -> re-record with the form line -> `OpenWork` -> the critic accepted, stage open -> next turn
`seam_rework_step` -> `Driver.rework` with the words file, preface as `extra` -> tester round -> critic again (last round again) ->
accept closes S2, or reject -> the seam again, the person decides again (F2 (a)).

## 4. Checks added or altered (AR-29)

| Check | Where | Class | Owner it serves | Census |
|---|---|---|---|---|
| `running` excludes the finishing dispatch; `finishing` fact | `driver_conductor.no_move_facts` | shape (state precondition) | data | existing row `judgment-census.json:1005` (shape, data); class unchanged |
| a recorded choice honoured only when recorded after the critic's start and not older than a recorded pass | `driver_stage_plan.stage_review_exhausted` | shape (presence of a person's recorded word + a time join) | intent (whether one more round is worth it is the person's; code only carries the later word) | add a row ONLY if `test_judgment_census.py` names the unit: `{"file": "driver_stage_plan.py", "function": "stage_review_exhausted", "class": "shape", "roles": ["conductor"], "owner": "intent"}` — a raise, named (AR-20, axis 18) |
| the option-only/cause line under `rework` | `no_move.moves_section` | not a check (prompt text) | — | none |
| the origin carried in `person.why` | `driver_conductor._person_of` | not a check (data carried) | — | none |
| preface as `extra` | `driver_machine.seam_rework_step` | not a check | — | none |

Judgment stays where it is: which stage, role, cases and cause the round takes — the conductor (AR-2, `check_args` checks only the
closed list); whether to buy the round — the person; whether the repaired work is good — the stage critic / consumer, accepted by
the driver.

Error direction of the reused filter (advice -> gate: `open_moves` gates what the conductor may offer, `no_move.py:8-11`): the
allowed error stays TOO FEW moves; the forbidden error is a move whose precondition is false. After the change the precondition of
the OFFER form of `rework` (record now, run after the finish) is true at this seam; the RUN form is named refused in the prompt
(point 3). Adversarial inputs that must stay CLOSED (rework not open): `dispatch` empty; `why`/`asked_why` absent or another word
(`refusal`, `threshold`, `chosen` with `asked_why` `""` or `threshold`); another dispatch running beside the critic; the critic
replaced by a `restart` (a new id `C'` running while `dispatch` names `C`); `controller.json` unreadable (`held()` raises, `running`
None, `no_move.py:105`); an `asked` written before the change by an unread hop (its `why` is `unread_answer`, the origin lost).
Input that stays harmless: `asked_why` in the set but `dispatch` names a dispatch that is not running (nothing to exclude). The one
residual direction: a conductor that ignores the option-only line and runs `controller.py --operation rework` itself is refused at
`apply` BEFORE any event (`controller.py:5473-5486`): one paid turn, nothing corrupted.

Error direction of the reused `person_pass` normaliser (`time_stamp`, now also a gate on the choice): it may err only toward "no
time" (`""`): a naive time, a non-string that is not a number, a bool, an unparsable string -> `""` -> the choice is not honoured
(the conductor is asked as today). Adversarial inputs that must stay on that side: `"x"`, `""`, `None`, `True`, a naive
`"2026-11-12T18:10:00"`, an `at` equal to the start (strictly later only).

## 5. The node

node: FV1-6 (builder, Sonnet) — the round to the author at an exhausted stage review, on the one seam

given: this spec (`C:\QAFactory\forge-repo\docs\tasks\specs\20261113-fv1-6-s2-door-back-to-tester-spec.md`) and the verdict
  (`C:\QAFactory\forge-repo\docs\tasks\specs\reviews\20261113-fv1-6-plan-critic.md`); `ai-packages/qa-factory/design/factory-rules.md`
  (whole); `plans/builder-rules.md`; `ai-packages/qa-factory/design/architecture.md` (AR-1, AR-12, AR-13, AR-14, AR-15, AR-17, AR-19,
  AR-20, AR-24, AR-25, AR-28, AR-29); `docs/TESTING.md`; the files of owns as they stand on origin/main;
  `ai-packages/qa-factory/scripts/tests/no_move_seam_common.py` (`rig`, `seam_asked`, `raised`, `FACTS`);
  `ai-packages/qa-factory/scripts/waiver.py` `split_overridden` (`:202`, read only); `ai-packages/qa-factory/scripts/driver_s0.py`
  `owed_rework` / `drop_record` (`:550-564`, read only); `ai-packages/qa-factory/scripts/controller.py` `stamp_utc` (`:1157-1162`, read only)
owns:
C:\QAFactory\forge-repo\.claude\worktrees\fv1-6\ai-packages\qa-factory\scripts\no_move.py (new module constant `FINISHING_WHYS`; `moves_section`: the finishing line only)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-6\ai-packages\qa-factory\scripts\driver_conductor.py (`no_move_facts`, `unread`, `_person_of` (the `why` field only), `record_seam_rework` (docstring sentence about `preface` only))
C:\QAFactory\forge-repo\.claude\worktrees\fv1-6\ai-packages\qa-factory\scripts\driver_machine.py (`take_seam_answer` (the `unread` call `:2371` only), `seam_chosen` (the `chosen` state `:2432-2435` only), `seam_rework_step`)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-6\ai-packages\qa-factory\scripts\driver_stage_plan.py (`stage_review_exhausted` only)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-6\ai-packages\qa-factory\scripts\driver_stage_s6.py (`person_pass`: the nested `stamp` removed and its calls renamed; new `DriverStageS6.time_stamp` staticmethod)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-6\ai-packages\qa-factory\references\conductor-actions.json (`moves[rework_stage].precondition` and `.forbidden_when` strings only)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-6\ai-packages\qa-factory\scripts\tests\test_no_move_seam_n2b_n15.py (rows in `n2b_the_facts_are_read_from_the_project`; new table function `fv16_stage_review_round`, registered in `main()`)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-6\ai-packages\qa-factory\scripts\tests\fixtures\judgment-census.json (only the row the census test names, if any)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-6\ai-packages\qa-factory\changelog.d\fv1-6-stage-review-round.md (new fragment, English)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-6\docs\SIBLING_MAP.md (axis 5, the row "Author + critic repair loop" at line 122, one cell)
non-goals: every other function of the five scripts (`sides_reread`, `window_round_gate`, `handle_refusal`, `take_answer`,
  `_unread_halt_or_review`, `_file_words`, `chosen_note`, `no_move`, `_no_move`, `validate_options`, `stage_verdict_known`,
  `stage_acceptance_write`, `consumer_*`); `driver_dispatch.py` (not edited at all); `driver_dialog.py`; the S5/S7 `repair_limit` road
  and `WINDOW_ROUND_CAP` (F4, F6); every other row and key of `conductor-actions.json` and `question-prices.json`; the fallback block;
  the controller; the quarantined files (`test_stage_review_person_pass.py`, `test_stage_critic_route.py`,
  `test_stage_acceptance_consumer.py`, `test_story_run_repair_limit.py`) — not run, not edited; the consumer OpenWork word (F5); the
  behaviours of A6/A7 (existing roads, findings §10.4); the batch file (the Lead updates row 39, §10.3).
handoff: the diff committed in the worktree; the report per `.claude/agents/builder.md` rule 7 with the FR pass (A, B, C, D, E, G one
  line each; F: "no measurement changed"), the verbatim witness, the axis block (§1 four axes plus the rest of the map by number), the
  AR-20 line if a census row was added, the test-budget line (TESTING.md) if test lines exceed product lines, and any "no scenario or
  keep row covers" line as printed.
edges: §5.2, E1-E18.
DoD: §5.4; verification command: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/no_move.py ai-packages/qa-factory/scripts/driver_conductor.py ai-packages/qa-factory/scripts/driver_machine.py ai-packages/qa-factory/scripts/driver_stage_plan.py ai-packages/qa-factory/scripts/driver_stage_s6.py ai-packages/qa-factory/references/conductor-actions.json ai-packages/qa-factory/scripts/tests/test_no_move_seam_n2b_n15.py`
siblings: S3, S4, S6 consumer, S7 consumer — covered by the same function, R rows at S2 and S4; S5 window and S7 test repair —
  another road, F4 residual node (§10.4); conductor window-round cap — F6, not this class; the exploratory seam record
  (`driver_machine.py:2742`) — covered by A3 (the same runner `seam_rework_step`).
designer: this draft (after Lead acceptance)

### 5.1 What to change, exactly

1. `no_move.py`, next to `EXCLUDED_KINDS` (`:36`): `FINISHING_WHYS = ("stage_review_exhausted",)` with a comment: the seam reasons
   raised inside the finish of the dispatch the question is about; the facts never count that dispatch as running, and `rework` is
   then an option only (FV1-6).
2. `no_move.moves_section` (`:257-285`): inside the loop, in the `args == "rework"` branch, after `lines.append(rework_args_list(facts))`
   and before `continue`, when `str(facts.get("finishing") or "")` is non-empty append ONE line:
   `f"  option only while {finishing} finishes: offer it; the driver records the person's choice and runs it after that finish — running it yourself now is refused (one dispatch runs at a time). Past the author's repair cap the controller takes a `test_defect` round only after the person's pass for both roles is recorded (the `rework_stage` row says how); a cause other than `test_defect` needs no pass. Which cause fits the person's words is your judgment."`
   Nothing else in the function. (`rework_args_list` itself is not changed: the args-refused re-prompt keeps its text.)
3. `driver_conductor.no_move_facts` (`:352-407`): after `facts, dispatch = ...` (`:357`) compute
   `finishing = dispatch if dispatch and (str(state.get("why") or "") in NM.FINISHING_WHYS or str(state.get("asked_why") or "") in NM.FINISHING_WHYS) else ""`
   (do NOT name it `held`: `held()` is the nested reader at `:365`), set `facts["finishing"] = finishing`, and change the `running`
   reader (`:389`) to `any(isinstance(d, dict) and d.get("status") == "running" and str(d.get("id") or key) != finishing for key, d in held()["dispatches"].items())`
   (the key is the dispatch id; `d["id"]` when present). Every other fact unchanged. Extend the docstring with E1's invariant.
4. `driver_conductor._person_of` (`:419-438`): at `:428` the `why` value becomes `str(state.get("asked_why") or state.get("why") or "")`.
   Nothing else; line `:436` keeps reading `state.get("why")`.
5. `driver_conductor.unread` (`:852-870`): new keyword `asked_why: str = ""`; when non-empty, `state["asked_why"] = asked_why` (both
   branches). All existing callers unchanged.
6. `driver_conductor.record_seam_rework` docstring (`:738-739`): "`preface`: lines the CODE gives the role beside the person's words
   (as `extra` lines of the rework's prompt; the finding the words are about, critic t-1592 M-a; the reviewer's form, FV1-6); kept in
   the record, absent when there are none." No code change.
7. `driver_machine.take_seam_answer`: the `unread(...)` call at `:2371` passes `asked_why=str(asked.get("why") or "")`. Nothing else.
8. `driver_machine.seam_chosen`: the `no_move` state at `:2432-2435` gains `"asked_why": str(asked.get("why") or "")`. Nothing else.
9. `driver_machine.seam_rework_step` (`:578-616`): replace `:607` by `reason = given[1]` and pass `extra=preface` to the
   `self.rework(...)` call at `:609-610` (keep every other argument). Update the docstring sentence that says the preface is in the
   reason. No new constant.
10. `driver_stage_s6`: hoist the nested `stamp` (`:273-283`) to `@staticmethod def time_stamp(value) -> str` on `DriverStageS6`, body
    byte-for-byte; `person_pass` calls `self.time_stamp(...)` at `:289`. No behaviour change.
11. `driver_stage_plan.stage_review_exhausted` (`:691-747`):
    a. docstring `:694-697`: the second move reads "an OFFER to the person of one more round for the author (`rework` with `args`;
       the driver records the choice and runs it after this finish; past the cap a cause other than `test_defect`, or the person's
       passes)"; and one sentence: "A choice the person recorded after this critic dispatch started, and not older than a recorded
       `go on` pass, is honoured here without a second conductor call (FV1-6)."
    b. lead `:707`: `text + f". Decide: accept {stage} with the gap, offer the person one more round for {author}, or ask the person."`
    c. hoist `word = "cases_in_repair" if stage == "S4" else "stage_in_repair"` above the new block; the branch at `:743-745` uses it.
    d. the new block, right after `author_last = ...` (`:727`) and BEFORE `if person_closes(author_last)` (`:728`):
       ```
       chosen = self.state.get("seam_rework")
       chosen_at = self.time_stamp(chosen.get("at")) if isinstance(chosen, dict) else ""
       start = self.time_stamp(since) if since else ""
       honoured = bool(start) and chosen_at > start
       if honoured:
           _blocking, passed = waiver.split_overridden([line], self.pipeline(), stage)
           honoured = not (passed and self.time_stamp(passed[0].get("at")) > chosen_at)
       if honoured:
           ... (11e) ... return OpenWork(word, open_work_reason(
               f"the person chose one more round after {who} reviewed {stage}", f"… [list: {form}]"))
       ```
    e. inside the honoured branch: build `form_line` (11f) — name it `form_line`, NOT `line` (`line` at `:705` is the pass phrase);
       `old = [str(x) for x in chosen.get("preface") or []]`; when `getattr(self, "dry", False)`: print
       `f"{stage}: dry run - the round the person chose would start after this review's finish; nothing is recorded"` and return the
       OpenWork without re-recording; else call
       `self.record_seam_rework({k: chosen[k] for k in ("stage", "role", "cases", "rows", "cause") if chosen.get(k)}, str(chosen.get("words_file") or ""), preface=old if form_line in old else [*old, form_line])`,
       print `f"{stage}: the round you chose starts once this review is finished; the conductor is not asked again"`, return the OpenWork.
    f. `form_line` (each a true statement whatever stage the chosen round takes, A4):
       - `form` empty or `(self.task_root / form).is_file()` False:
         `f"The form of {who} on {stage} could not be found ({form or 'the saved result named no dispatch'}). The person chose this round; their words below are its instruction."`
       - else, `verdict = "" if unreadable else str((record or {}).get("verdict") or "")`; with `verdict`:
         `f"{who} gave {stage} the verdict `{verdict}`; its form is {form}: read it whole. The person chose this round; their words below are its instruction."`
       - else: `f"The form of {who} on {stage} is {form}; no verdict word could be read from it, so no verdict is stated here. The person chose this round; their words below are its instruction."`
    g. the existing `if person_closes(author_last): return None` (`:728-729`) becomes: when it closes AND `chosen_at > start` (a pending
       choice recorded after the start, so the later pass beat it): `self.drop_record("seam_rework")` and print
       `f"{stage}: the round chosen earlier is not run: the later word `go on` closed {stage}"`; then `return None`.
       The second `person_closes` at `:735-736` is unchanged.
12. `references/conductor-actions.json` `moves[rework_stage]`: in `precondition` replace "no dispatch running" by "no dispatch running
    other than the reviewer whose finish raised this question (then `rework` is an option only: the driver runs the chosen rework after
    that finish)"; in `forbidden_when` replace "a dispatch is running" by "a dispatch other than that reviewer is running; running it
    yourself while that reviewer finishes". No other key or row.
13. Changelog fragment (English, no Cyrillic): one paragraph — an exhausted stage review (S2, S3, S4, and the S6/S7 consumer reviews)
    now offers the person one more round for the author through the conductor; the round is recorded and runs after the review's
    finish, with the person's words and the reviewer's form path; a long reason no longer drops the code's preface.
14. `docs/SIBLING_MAP.md:122` (axis 5, "Author + critic repair loop"): append to the first cell's list ", S2/S3 author/stage critic and
    the S6/S7 author/consumer reviews (`Driver.stage_critic_route`, `Driver.consumer_completion`; the exhausted review's one seam
    `Driver.stage_review_exhausted`)". No other line.

### 5.2 Edges (each with the invariant it protects)

- E1 (positional, `no_move_facts`): the exclusion applies to exactly one id, the seam's own `dispatch`, and only for a `why` /
  `asked_why` in `FINISHING_WHYS`. Invariant: `rework` is never offered while ANY other dispatch runs; with no `dispatch` or another
  origin the facts are today's, plus `finishing: ""`.
- E2 (positional, `stage_review_exhausted`): the new block sits AFTER `since` and `author_last` are read and BEFORE the first
  `person_closes` and the first `no_move`. Invariant: a choice recorded for THIS review never buys a second paid conductor call; a
  `go on` pass recorded strictly later than the choice still closes the stage first; a choice older than the critic's start (or of
  unknown age) never holds a later review open.
- E3 (empty/absent): `since == ""` (no journalled start), `seam_rework` absent / not a dict, `at` absent / not a time / no zone /
  equal to the start -> not honoured, today's order runs. Invariant (FR-59): an unknown never becomes a held stage.
- E4 (B3, the unreadable road): `unreadable=True` or a record with no verdict word -> the "no verdict word could be read" line; a
  missing form or no dispatch id -> the "could not be found" line; the OpenWork reason says "reviewed", never "rejected". Invariant
  (FR-41, FR-58, AR-28): no verdict is stated that the code did not read; the round is never refused for a missing quote or form.
- E5 (long words, limit AT/BEYOND, outside input): the person's words at 1500 characters and at 1501 -> `reason` is the words whole and
  `extra` is the preface on both (the 1500 cut lives in `Driver.rework`, unchanged, and turns 1501 into the file line). Invariant
  (FR-8, FR-49): neither the person's words nor the reviewer's form path is cut or lost; the verdict travels by path, never pasted.
- E6 (the bought round is also spent): the next reject (counted past cap, `last_round` True) reaches the seam again with `rework`
  open again; the person decides each time (F2 (a)). Invariant: no round starts without a `seam_rework` record written from a
  person's chosen token; no path loops silently or stops silently.
- E7 (free text): words that are no offered token -> `unread` with `asked_why` -> the conductor reads them with `rework` open. Its
  answers: (i) options -> a new question whose `asked.why` is the origin (B1); (ii) `continue`/`retry` -> `take_seam_answer` returns
  False and `_file_words` files the words for the critic (`pending_words[<critic id>]`, `driver_machine.py:4101-4112`), so
  `wait_existing_job` RESUMES THE CRITIC with them (`driver_machine.py:1451-1453`) instead of finishing its saved result — an existing
  road this node does not change (finding text §10.4, A6). Invariant (P22, FR-12): code never reads the words by phrase.
- E8 (`rework` token without `args`, any hop): the chosen call carries `asked_why` = the origin; `rework` stays open; the conductor
  answers with the lone `rework` option (`validate_options` lone rule, `no_move.py:419-422`) and `chosen_rework` records it.
  Invariant: a `rework` choice never meets "no longer open" (`driver_conductor.py:714-715`) because of the reviewer's own running
  dispatch, however many questions came before it.
- E9 (temporal — before/after this commit; the commit creates the new world, no migration): (a) a story asked at the limit before the
  change holds `asked.why: stage_review_exhausted` (`driver_dialog.py:327`), so after the upgrade a word or token answer reaches a
  conductor that sees `rework` open; its old token answers run as before; (b) a story whose `asked` was written by an UNREAD hop
  before the change holds `why: unread_answer` (origin lost) -> no exclusion, `rework` closed, today's behaviour (the safe side);
  (c) no `seam_rework` record can exist for such a review (the move was closed), so E2's block finds none; (d) a record written before
  the change by another road (the exploratory seam, `driver_machine.py:2742`) is honoured only when its `at` is after THIS critic's
  start — impossible for an older record.
- E10 (A1, conflicting pair: a `go on` pass AND a chosen round both recorded after the critic's start): the LATER word wins. Choice
  later (or the same second — the tie goes to the reversible side, the round) -> OpenWork, the pass is not recorded as an accept,
  and on the next review it is older than that critic's start, so it never closes it. Pass later -> the stage closes with its
  finding (existing), the choice record is dropped and the person reads the printed line. Invariant: one finish never both accepts
  the stage and holds it open, and the code never runs a word the person replaced.
- E11 (price line, P18): the option's lines are the conductor's, priced by the `rework_stage` row classes; this change writes no
  money figure. Invariant: no number of dollars in a question, record or report this code writes.
- E12 (the controller refuses the round, e.g. `test_defect` past the cap without passes): `seam_rework_step` -> `ReworkRefused` ->
  `seam_rework_refused` (`driver_machine.py:745-750`) -> the conductor with the person's words, the refusal (its passes door) and the
  closed list. Follow-on (A7): if that conductor answers `continue`, the stage stays open (the OpenWork was accepted) and the next
  `stage_S2` -> `stage_critic_route` runs a NEW paid critic over the unchanged artifact (`stage_repair_owed` is skipped on the last
  round, `driver_stage_plan.py:612`) — reachable now; named here, finding text §10.4. Invariant (FR-57): a refusal is never a dead
  end and the person's words are not lost.
- E13 (A4, the chosen stage differs from the reviewed one): `rework_stages` at S2 holds S1 and S2, at S4 S1-S4, at the S6 consumer
  S5-S8 (`driver_conductor.py:376-382`). The choice is honoured all the same (the person's word); `form_line` names the reviewed stage
  and its form and claims nothing about what the round repairs. Invariant: no text says "this round repairs what it names" for a
  stage the reviewer did not judge.
- E14 (A5, the re-record raises inside the finish): `record_seam_rework` raises `held_question` when `rel` is empty or
  `controller.json` cannot be read (`driver_conductor.py:740-747`). The Person propagates out of `complete`: the critic's finish is not
  done, the record is unchanged, the person's question comes back (the same road the seam's own Person takes from inside
  `complete`). Invariant (FR-59): an unknown never becomes a held stage; nothing is half-written.
- E15 (dry run): the honoured branch writes nothing (no re-record), prints one line and returns the same OpenWork. Invariant (B-20
  F2): `--dry-run` runs nothing and writes nothing.
- E16 (no dispatch id): `critic_dispatch == ""` -> `finishing` is `""` -> `rework` stays closed by the running critic, `since` is ""
  so no choice is honoured; the conductor sees today's moves. Invariant: with no id, code does not guess which dispatch is finishing.
- E17 (B2, the run form): with `finishing` set, the prompt says the run is refused; a conductor that runs it anyway is refused at
  `apply` before any event (`controller.py:5473-5486`). Invariant: the gate never presents the RUN form as available beside a running
  dispatch; nothing is corrupted on the residual path.
- E18 (B1 positional, `_person_of`): `asked_why` outranks `why` only when non-empty. Invariant: a state with no `asked_why` stores its
  own `why` byte-for-byte (every existing reader of `asked.why` — the restore — and every existing test that builds a direct state are
  unchanged).

### 5.3 Test rows (keep file `test_no_move_seam_n2b_n15.py`, `test-layers.json:3165`, layer detector, `covers` names all five scripts; `docs/TESTING.md`: one table, a row per behaviour, ids naming the input)

In `n2b_the_facts_are_read_from_the_project` (existing function), a table `(id, state, dispatches, expected running, expected
finishing, rework_stage open?)` over `driver.controller_state` stubbed to hold accepted S1 and S2 dispatches plus the critic `C`
(`running`) unless the row says otherwise:

| Row | state | other running | running | finishing | `rework_stage` open |
|---|---|---|---|---|---|
| F1 | why `stage_review_exhausted`, dispatch `C` | none | False | `C` | yes |
| F2 | same | `X` running | True | `C` | no |
| F3 | why `refusal`, dispatch `C` | none | True | `""` | no |
| F4 | why `chosen`, asked_why `stage_review_exhausted`, dispatch `C` | none | False | `C` | yes |
| F5 | why `unread_answer`, asked_why `stage_review_exhausted`, dispatch `C` | none | False | `C` | yes |
| F6 | why `stage_review_exhausted`, dispatch `""` | none | True | `""` | no |
| F7 | why `chosen`, asked_why `threshold`, dispatch `C` | none | True | `""` | no |
| F8 (B1) | two hops: `seam_asked(..., why=<_person_of(unread state with asked_why stage_review_exhausted).why>)`, then the `chosen` state `seam_chosen` builds from that `asked` | none | False | `C` | yes |
| F9 (restart) | why `stage_review_exhausted`, dispatch `C`; `C` released, `C'` running | `C'` | True | `C` | no |
| F10 (B2) | F1's facts through `NM.moves_section` | — | — | — | the text holds "option only while C finishes" and "running it yourself now is refused"; F3's facts: neither phrase; `conductor-actions.json` `rework_stage.precondition` holds "other than the reviewer" |
| F11 (B4) | F1's facts through `NM.moves_section` | — | — | — | the text holds "only after the person's pass for both roles" and "Which cause fits the person's words is your judgment" |
| F12 (E18) | `_person_of` of a `refusal` state with no `asked_why` | — | — | — | `person.why == "refusal"` |

New table function `fv16_stage_review_round` (driver from `rig()`; `controller.Controller._dispatch_starts` stubbed to give the
critic's start, restored in `finally`; `no_move`, `record_seam_rework`, `person_pass` (or `py`), `rework` replaced by recording stand-ins
where named; the critic's form written under `task_root/work/handoffs/` where the row needs it):

| Row | input | expected |
|---|---|---|
| R1 | S2, choice `at` = start + 1 s, record verdict `reject` | `OpenWork("stage_in_repair")`; `no_move` not called; `record_seam_rework` once with the "gave S2 the verdict `reject`" line in `preface` |
| R2 | S4, same | `OpenWork("cases_in_repair")` |
| R3 | `at` == start | `no_move` called; no OpenWork from the new block |
| R4 | `at` = start - 1 s | `no_move` called |
| R5 | no journalled start (`since` "") | `no_move` called |
| R6 | `at` = `"x"`, absent, `"2026-11-12T18:10:00"` (no zone), `True` | `no_move` called (one row per value, ids name them) |
| R7 | no `seam_rework` | `no_move` called (today) |
| R8 | the re-entry twice (the first record already carries the form line) | the form line is in `preface` exactly once |
| R9 | `form` "" | the "could not be found" line |
| R10 | a choice at start + 2 s, a `go on` pass at start + 1 s | OpenWork; the pass is NOT recorded (`person_pass` not reached) |
| R11 (B3) | `unreadable=True`, form file present | the "no verdict word could be read" line; the OpenWork reason holds "reviewed", not "rejected" |
| R12 (B3) | record `{}` (no verdict word), not unreadable | the "no verdict word could be read" line |
| R13 (A4) | S2, the choice's stage `S1` | OpenWork; `record_seam_rework` got `stage: S1` |
| R14 (A5) | `record_seam_rework` raises `story_run.Person` | the Person propagates; `state["seam_rework"]` unchanged; no OpenWork |
| R15 (A1) | a pass at start + 2 s, a choice at start + 1 s | returns None (the pass closes); `seam_rework` dropped; the printed line names `go on` |
| R16 (A1 tie) | pass and choice at the same second | OpenWork (the round) |
| R17 (dry) | `driver.dry = True`, an honoured choice | OpenWork; `record_seam_rework` not called; the dry line printed |
| L1 (limit AT) | `seam_rework_step`, preface of 1 line, words of exactly 1500 characters | `rework` got `reason` == the words (1500 characters) and `extra` == the preface |
| L2 (limit BEYOND) | words of 1501 characters | `reason` == the words (1501), `extra` == the preface |
| L3 | no preface | `extra` empty |
| A1 | `take_seam_answer`, free words to an `asked` with why `stage_review_exhausted` | `unread` got `asked_why="stage_review_exhausted"` |
| A2 | `seam_chosen`, `rework` without `args` | the `no_move` state carries `asked_why` |
| A3 | `unread(..., asked_why="stage_review_exhausted")` | the state given to `no_move` carries it; without the keyword it carries no `asked_why` key |

The test lines will likely exceed the product lines (TESTING.md budget): the builder names the reason in one report line (one
table per behaviour class of a seam with five sites and two answer roads).

### 5.4 DoD (inline)

Acceptance criteria:
1. At an exhausted stage review the fact `running` ignores the reviewing dispatch alone, on every hop of the question (rows F1-F9 and
   F12 green).
2. The conductor is told `rework` is option-only while the reviewer finishes, with the cause rule, and the data row says the same
   exception (F10, F11 green).
3. A person's chosen round recorded after the critic's start and not older than a recorded pass makes the critic's finish return the
   existing `OpenWork` word without a second conductor call; the round carries the reviewer's form path in words that state only what
   was read; a later pass wins and drops the choice (R1-R17 green).
4. The preface reaches the role as `extra` on both sides of 1500 (L1-L3 green); the answer roads carry the origin (A1-A3 green).
5. Function scope: `git -C C:\QAFactory\forge-repo\.claude\worktrees\fv1-6 diff origin/main -- ai-packages/qa-factory/scripts/driver_machine.py`
   shows hunks only inside `take_seam_answer`, `seam_chosen`, `seam_rework_step`; the same for each script against its owns line;
   `driver_dispatch.py` and `driver_dialog.py` have no diff.
6. AR change checks: no new `Person(` site and no new question key (grep of the diff); no new `fromisoformat` in
   `driver_stage_plan.py`; `python -m pytest ai-packages/qa-factory/scripts/tests/test_judgment_census.py -q` green, any row it
   demanded added per §4 and named with its AR-20 raise.
7. FR pass in the report (A, B, C, D, E, G one line each; F: "no measurement changed"); `python -B ai-packages/qa-factory/scripts/selftest.py --lang`
   green (the changelog fragment and the new strings carry no Cyrillic).
8. `docs/SIBLING_MAP.md`: doc witness per rule 11 — a key-presence script, attached in full in the report and not committed, checks
   the verbatim keys "S2/S3 author/stage critic" and "`Driver.stage_review_exhausted`" on line 122, with a negative control (a key
   deliberately absent -> the script reports failure); plus the one-hunk `git diff` of that file.

Verification run (the witness), from the worktree root:
`python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/no_move.py ai-packages/qa-factory/scripts/driver_conductor.py ai-packages/qa-factory/scripts/driver_machine.py ai-packages/qa-factory/scripts/driver_stage_plan.py ai-packages/qa-factory/scripts/driver_stage_s6.py ai-packages/qa-factory/references/conductor-actions.json ai-packages/qa-factory/scripts/tests/test_no_move_seam_n2b_n15.py`
then every file it prints that is a keep row or a scenario (never a quarantine file, never a slow file), at least
`python -B ai-packages/qa-factory/scripts/tests/test_no_move_seam_n2b_n15.py`,
`python -B ai-packages/qa-factory/scripts/tests/test_no_move_seam_n1_n9.py` and
`python -m pytest ai-packages/qa-factory/scripts/tests/test_judgment_census.py -q`; output pasted verbatim. A keep row that goes red
because it asserts `asked.why` after an unread hop is an expected change of E18/B1 only if its input carried `asked_why`; anything
else red is a defect of the diff.

Live proof (FR-33): a row in the not-taken batch of pile `live-runs` — "an exhausted S2 review offers `rework` to the tester as an
option, the chosen round runs after the critic's finish with the critic's form path" — moved there at batch close (PROJECT.md
«Командная работа» p. 9).

Axis 34 (P31): covered — one function for the five review sites, no stage name in code; the S5/S7 road difference is F4 (§10.4).

### 5.5 Crossings (other work in flight on the same files; function lists per PROJECT.md «Командная работа» p. 3, D-0048)

- `driver_machine.py`: CL4-1 N1 owns `window_round_gate`; FV1-22 N3 owns `window_round_gate` too; FV1-3 owns `_unread_halt_or_review`
  and the call line `:3510` in `take_answer` (`docs/tasks/specs/20261113-fv1-3-free-answer-to-conductor-spec.md:162`); FV1-17 owns
  `resume_on_refusal` (`:279-287`) and the `stand_probe` docstring; FV1-4 owns the `_answer_note` call sites `:3308-3312`,
  `:3888-3889`. FV1-6 owns `take_seam_answer`, `seam_chosen`, `seam_rework_step`: DISJOINT from all of them — parallel; the later
  branch merges main.
- `driver_stage_plan.py`: FV1-22 N1 owns `stage_verdict_known`, N2 owns `stage_acceptance_write`
  (`docs/tasks/specs/20261113-fv1-22-s7-acceptance-loop-spec.md:147,248`). FV1-6 owns `stage_review_exhausted`: disjoint — parallel.
  Interplay, not a shared function: N1 changes when `stage_verdict_known` is False, i.e. when `unreadable=True` reaches the seam; E4's
  lines are true on both values.
- `driver_conductor.py`: FV1-22 edits none (its non-goal); FV1-3 owns no function of it, and calls `unread` with today's arguments —
  the new keyword has a default, so FV1-3's calls and its test stubs of `driver.unread` stay valid. FV1-13 #4 (no spec yet; named by
  FV1-3's non-goals as owning `no_move`, `validate_options`, `conductor-actions.json`): `no_move` / `_no_move` are not FV1-6's;
  disjoint by function.
- `no_move.py`: FV1-13 #4 may own `validate_options`; FV1-6 owns `moves_section` and one constant at the top: disjoint by function
  (a constant next to `EXCLUDED_KINDS` may meet another constant in a merge: trivial, the later branch resolves).
- `references/conductor-actions.json`: FV1-6 edits two strings of the `rework_stage` row. FV1-13 #4 has no spec yet: if it edits the
  `rework_stage` row, the two are SEQUENTIAL (`очередь: FV1-6 → FV1-13` in both rows, or the reverse by readiness); if it edits other
  rows (e.g. `go_on_as_is`), disjoint. The Lead confirms when FV1-13's spec exists.
- `driver_stage_s6.py`: FV1-22 names `consumer_*` as protected; FV1-6 owns only `person_pass` + the new staticmethod: disjoint.
- `driver_dispatch.py`: FV1-2, FV1-3, FV1-13, FV1-20, FV1-22 N2/N3 write it; FV1-6 does not touch it (A3 keeps it so).

## 6. Forks (returned, with a recommendation)

- F1 — Scope of the fix. DECIDED by the Lead: (a) the shared seam, which fixes S2, S3, S4, S6c, S7c in one move.
- F2 — The bought round is spent too. DECIDED: (a) the person decides each time.
- F3 — The cause of the bought round. DECIDED: (a) the conductor's judgment from the closed list; the rule now reaches the conductor
  (B4, §5.1 p.2).
- F4 — Two roads for one state "rounds spent". DECIDED: (a) keep both now; the residual node is written as a finding text in §10.4;
  the owner has been asked about (b)/(c).
- F5, F6 — DECIDED: findings (texts in §10.4).
- F7 (new, A1) — which word wins when a `go on` pass and a chosen round both stand after the critic's start. (a) the LATER recorded word
  wins (both carry `at`; the pass's `at` read through `waiver.split_overridden` before anything is recorded; a tie goes to the
  round, the reversible side); (b) the pass always wins and the pending choice is dropped with a printed line (the critic's minimal
  alternative). Recommend (a): it is the reading of the person's intent that needs no rule of precedence between two words of the same
  person, and it costs one read of the one reader. The node is written on (a) (§5.1 p.11d/g, R10, R15, R16); (b) would delete the
  `split_overridden` read and R10/R16, nothing else. Which word wins is the person's intent: the Lead confirms or picks (b).
- F8 (new, B2 carrier) — where the option-only note lives. (i) one line in `moves_section` keyed by the `finishing` fact (one carrier,
  every hop, the cause rule rides with it); (ii) one line in the text of the three states (first call, `unread`, `chosen`) — three
  carriers, and the `unread` state has no lead, so a later hop would lose it (the B1 class again). Recommend and written on (i).
  Small weight, returned because it widens owns to `no_move.moves_section`.

## 7. Small choices closed by the designer

- `FINISHING_WHYS` as a module constant in `no_move.py` (the `EXCLUDED_KINDS` precedent), not a data row: the `why` words are written
  by code only (one writer, `driver_stage_plan.py:706`).
- The origin is carried in `person.why` (`asked_why or why`) instead of a separate `asked.asked_why` key: the critic's analysis — a
  separate key would touch `driver_core.Person`, `driver_dialog.ask` and the restore; `asked.why` has no behavioural reader besides the
  restore (grep §9).
- The local of the finishing id is `finishing`, not `held` (`held()` is the nested reader of `no_move_facts`); the preface local is
  `form_line`, not `line` (`line` is the pass phrase). Both were collisions in the first draft.
- `time_stamp` is a staticmethod of `DriverStageS6`, reached as `self.time_stamp` from `DriverStagePlan` (both are mixins of the one
  Driver): no import between the two modules.
- The reviewer's verdict travels by form PATH, never pasted, so no new limit is introduced.
- The fallback block (no conductor answer) is not given a `rework`: stage, role and cause are the conductor's judgment (AR-2); on the
  floor the person's words still reach the conductor through `unread`.
- `record_seam_rework` is re-called (one writer) rather than editing `state["seam_rework"]` in place.
- Test rows go into the keep file `test_no_move_seam_n2b_n15.py` (`test-layers.json:3165`); the natural homes
  (`test_stage_review_person_pass.py` `:9939`, `test_stage_critic_route.py` `:9913`, `test_stage_acceptance_consumer.py` `:9896`) are in
  the `quarantine` section (`:7126` onwards).

## 8. Not verified (estimates)

- What `scenario_walk.py --witness-for` prints for these paths: not run (no shell in this role); the covers lists of
  `test_no_move_seam_n1_n9.py` and `test_no_move_seam_n2b_n15.py` name all five scripts (`test-layers.json:3125-3163`, `:3165-3199`);
  `references/conductor-actions.json` is not in those covers — the walk names its judge or prints "no scenario or keep row covers".
- Whether `test_judgment_census.py` names `stage_review_exhausted`: not run; §4 is conditional.
- The S3 call sites `driver_stage_plan.py:117,122,131` and `driver_stage_plan.py:1036-1043` / `:1108-1114` ranges: taken from the
  critic's trail on e4ba384, with the `completion_for` def `:1011` and the calls `:1042`, `:1114` re-read by grep.
- No keep row was found that asserts `asked.why` after an unread hop through `take_seam_answer`; not exhaustively proved (the grep of
  §9 found only fixtures that BUILD `asked` dicts with `why: unread_answer`).

## 9. Reading trail (fix round, read-main e4ba384)

Read: the verdict (whole); this spec (whole); `driver_stage_plan.py:536-547,575-824`; `driver_conductor.py:340-489,560-889`;
`driver_machine.py:570-619,745-769,1440-1474,2330-2444,4085-4129`; `no_move.py:1-304`; `references/conductor-actions.json:60-84`;
`controller.py:5460-5489,5585-5663`; `driver_dispatch.py:628-707,2630-2704`; `driver_stage_s6.py:255-369`; `driver_s0.py:548-567`;
`scripts/tests/test_no_move_seam_n2b_n15.py:1-45,455-486`; `scripts/tests/no_move_seam_common.py:1-80`;
`scripts/tests/scenario_walk.py:860-889`; `scripts/tests/test-layers.json:3125-3199`; `plans/piles/live-run-fvf/batch-1-live-run-fvf.md`
(whole); FV1-3 spec (owns block `:160-173`, §2 grep); FV1-22 spec (owns blocks `:140-152,245-251,296-300`, §4 `:311-326`).

Searches (each with its positive control):
- `asked\.get\("why"\)|asked\["why"\]|person\.why|\.why = |why=asked|...` over `scripts/*.py` -> `driver_dialog.py:327,622`,
  `driver_conductor.py:428` (the known write/restore lines ARE the control); then `asked.{0,30}why[^_]` -> only `driver_dialog.py:622`
  in product code, tests that assert `asked["why"]` on direct states (`test_story_run_refusals.py:179,202`, `test_no_move_seam_n1_n9.py:48`).
- `"why"\]?.{0,40}(unread_answer|chosen)` over `scripts/tests` -> fixture dicts only (control: the hits themselves).
- `no dispatch running|a dispatch is running` (case-insensitive) over the package -> `conductor-actions.json:73-74` and two test
  comments; no test pins the row text (control: the json lines are the known sample).
- `"stage_review_exhausted"` over `scripts` -> the one writer `driver_stage_plan.py:706` plus three quarantined tests.
- `\bseam_time\b|\btime_stamp\b|def stamp\b` (case-insensitive) over `scripts` -> no `time_stamp`; control: the same call found
  `driver_stage_s6.py:273` `def stamp`.
- `^(REPAIR_LOOP_ROLES|AUTHOR_ROLES|REPAIR_CAUSES)\s*=` in `controller.py` -> `:235,261,270`.
- `repair_limit|def repair_limit_gate|"round"` in `driver_stage_s7.py`, `driver_dispatch.py` -> `:3052,3099,3198-3200`, s7 `:1122-1131,1152`.
- `"(s5|s7)\.repair_limit"|"exit\.resume_limit"` in `question-prices.json` -> `:155,175,187`.
- `lone|len\(options\) == 1|exactly one option` in `no_move.py` -> `:419-422`.
- `repair_cycles` in `runtime_policy.py` -> `:13`; `def split_overridden` in `waiver.py` -> `:202`; `def _now` -> `driver_core.py:289-290`
  (aware UTC ISO); `def stamp_utc` -> `controller.py:1157`.
- `record_seam_rework\(|WINDOW_ROUND_CAP|def seam_rework_refused|def owed_rework|def drop_record|def _file_words|pending_words` in
  `driver_*.py` -> the cited lines (`driver_machine.py:45,745,2427,2742,4085,4111`; `driver_s0.py:550,561`).
- `def completion_for|def _finish_saved_result|stage_critic_completion\(|s4_critic_completion\(` -> `driver_stage_plan.py:1011,1042,1114`,
  `driver_machine.py:1522`.
- `test_no_move_seam_n2b_n15|...|"quarantine"|"keep"` in `test-layers.json` -> `:35,3125,3165,7126,9896,9913,9939`; census grep ->
  `judgment-census.json:1005` only for the five functions.
- SIBLING_MAP headings for axes 5/18/32/34 -> `:111,386,557,582`; "repair loop" -> `:122`.
- Owns lines of the other `20261113-fv1-*` specs for the five scripts and `conductor-actions.json` -> the crossings of §5.5.
- `witness-for` in `plans/builder-rules.md` (read-main) -> 7b `:15-21`; `scenario_walk._relative` accepts `ai-packages/qa-factory/`
  paths (`:862-865`).

Not re-read (taken from the critic's trail): `driver_stage_plan.py:117,122,131`; `driver_dialog.py:300-345` beyond the grep lines.

## 10. Fix round (critic-on-plan verdict, 13.11.2026)

### 10.1 Blockers

- B1 (`asked_why` lost after one re-ask) — applied. `_person_of` stores `asked_why or why` (§3.2, §5.1 p.4); `driver_conductor._person_of`
  added to owns with that reason; positional edge E18; temporal E9(b) (an `asked` already written by an unread hop stays closed — the
  safe side); E7/E8 rewritten for any number of hops; rows F8 (two hops) and F12 (no `asked_why` unchanged).
- B2 (the RUN form opened, the controller refuses it) — applied: the design only RECORDS at the seam and runs after the finish, and the
  conductor is told so on every call: the `finishing` fact + one line in `moves_section` (§3.3, §5.1 p.2-3; fork F8 records the
  carrier choice); the lead `:707` rewritten to "offer the person one more round for {author}" (§5.1 p.11b); the docstring `:694-697`
  (p.11a); the data row `rework_stage.precondition` / `forbidden_when` aligned (p.12; `conductor-actions.json` added to owns, the
  non-goal narrowed to "every other row and key"); §4 error direction rewritten; E17; row F10.
- B3 (the unreadable road states a false reject) — applied: `form_line` has three variants and states only a verdict word READ from the
  record, never on `unreadable` (§5.1 p.11f); the OpenWork reason says "reviewed" (p.11d); E4 rewritten; rows R11, R12.
- B4 (the cause rule never reaches the conductor) — applied: the rule rides the same `moves_section` line (§3.4, §5.1 p.2), worded so it
  is true with and without a spent cap (the unreadable road may have rounds left) and consistent with the data row's pass rule
  (`conductor-actions.json:73`) — the critic's sample sentence "the controller refuses `test_defect` here" was not used as is, because
  the controller takes `test_defect` past the cap once the person's passes are recorded (`controller.py:5639-5663`); AR-12 named in §1;
  row F11.

### 10.2 Amendments

- A1 (E10 double effect) — applied on the recommendation "the later word wins" (§3.5, §5.1 p.11d/g, E10, R10/R15/R16) and returned
  as fork F7 for the Lead's confirmation.
- A2 (second time normaliser) — applied: `person_pass`'s nested `stamp` hoisted to `DriverStageS6.time_stamp` and used by both
  (§5.1 p.10, p.11d); `driver_stage_s6.person_pass` added to owns; AR-13/AR-15 in §1; §4 states its error direction as a gate.
- A3 (third copy of 1500) — applied: no constant, no branch; `reason` = words, `extra` = preface on every length (§3.6, §5.1 p.9); L1-L3
  rewritten as AT/BEYOND on the words' length; the exploratory road `:2742` fixed by the same runner (siblings line).
- A4 (the chosen stage differs) — applied: E13; `form_line` wording true for any stage; row R13.
- A5 (the re-record raises inside the finish) — applied: E14 (corrected: `record_seam_rework` raises for an EMPTY `rel` or an unreadable
  `controller.json`, `driver_conductor.py:740-747`; it does not check that the file exists); row R14.
- A6 (E7 `continue` resumes the critic with the words) — named in E7 as an existing road; finding text in §10.4.
- A7 (E12 follow-on: a fresh paid critic over unchanged work) — named in E12; finding text in §10.4.
- A8 (stale references) — applied: every file:line re-taken on e4ba384. The critic's 12 rows: `seam_rework_step` `:578`, preface
  `:606-607`, `ReworkRefused` `:611-614`; `take_seam_answer` `:2335-2386`, `unread` call `:2371`; `seam_chosen` `record_seam_rework`
  `:2426-2427`, `why: chosen` `:2428-2435` / `no_move` `:2432`; exploratory `:2742`; `WINDOW_ROUND_CAP` `:45`; `driver_dispatch.py`
  cut `:2660`, `line` `:2681-2683`, prompt `:637-638`, `extra` `:704`; `repair_limit_gate` `:3052`, offer `:3099`, passes `:3198-3200`;
  lone rule `no_move.py:419-422`; census `:1005`; `question-prices.json:155,175,187`; the `rerun_after` cite dropped (E10 no longer
  relies on it). Also re-taken beyond the list: `controller.py:5603-5605` (cap), `:5465-5486` (refusal), `s4_repair_owed` gate `:545`
  (the critic wrote `:544`), `_file_words` filing `:4101-4112`, S7 test repair `driver_stage_s7.py:1122-1131,1152`; dropped as
  unverified: `driver_stage_s7.py:133`, `driver_stage_s8s9.py:79`, `controller.py:2190-2202`, `controller.py:3665-3668`.
- A9 (SIBLING_MAP axes) — applied in §1 (axes 5, 18, 32, 34) and owns (`docs/SIBLING_MAP.md:122`, §5.1 p.14, DoD 8); AR-20 named.
- A10 (the pile row) — for the Lead (the batch file is outside this dispatch's single write): row 39 «Пишет в» should read
  `scripts/no_move.py`, `scripts/driver_conductor.py`, `scripts/driver_machine.py`, `scripts/driver_stage_plan.py`,
  `scripts/driver_stage_s6.py`, `references/conductor-actions.json`, `scripts/tests/test_no_move_seam_n2b_n15.py`,
  `scripts/tests/fixtures/judgment-census.json`, `changelog.d/`, `docs/SIBLING_MAP.md`.
- A11 (tests) — applied: F8 (B1), F10 (B2), F11 (B4), F9 (restarted critic id), F12 (E18), R11/R12 (B3), R13-R17, L rows per A3, A3
  row for `unread`; the test-budget line in §5.3 and handoff.
- A12 (the F4 residual must name the exact difference) — applied in the residual node text below.

### 10.3 For the Lead (outside the single write of this dispatch)

- Update batch row 39 «Пишет в» (A10, text above).
- File the four finding texts below (and add their rows per PROJECT.md «Командная работа» p. 2); the F4 residual opens a node.
- When FV1-13's spec exists: confirm the `conductor-actions.json` row crossing (§5.5).

### 10.4 Finding texts (for the Lead to file)

- F4 residual node — "Rounds spent: two roads for one state". Class: the state "the author's repair rounds are spent and a reviewer
  still rejects" has two roads. Stage reviews (S2, S3, S4, S6/S7 consumer; `driver_stage_plan.stage_review_exhausted`) lift the cap by a
  cause LABEL: the conductor offers `rework` with a cause other than `test_defect`, which spends none of the cap
  (`controller.py:5608-5610`), or the person's passes for both roles. The S5 window and the S7 test repair
  (`driver_dispatch.repair_limit_gate` `:3052`, `repair_limit_person` `:3151`, `_answer_repair_limit` `:3202`; `driver_stage_s7.py:1122-1152`)
  lift it by recorded PASSES with the honest `test_defect` (`driver_dispatch.py:3198-3200`, token `round` of a priced site question).
  The label-vs-passes split is what the owner's P31 word settles: (b) the stage reviews take the `repair_limit` road (a priced site
  question with `round`, passes by code) or (c) S5/S7 take the seam (`round` becomes the conductor's `rework`). Owns (estimate):
  `driver_dispatch.repair_limit_*`, `driver_stage_plan.stage_review_exhausted`, `references/question-prices.json` (a key if (b)),
  `no_move.moves_section` (the line of FV1-6 if (c)). Test: one table that asks both sites the same "one more round" shape. Order:
  after FV1-6 and after FV1-20 (`driver_dispatch.py` repair_limit -> conductor). Owner's word needed: yes.
- F5 — "Consumer stages get the author-repair word at the exhausted seam". `stage_review_exhausted` returns `stage_in_repair` for the
  S6/S7 consumer reviews (`driver_stage_plan.py:744`, and FV1-6's new block reuses it), while their round-left road returns
  `acceptance.SUPERSEDED_WORD` (`driver_stage_s6.py:365-366`). Question for the pile's Lead: should the consumers get
  `SUPERSEDED_WORD` at the exhausted seam too (one word per road, AR-19)?
- F6 — "The conductor's window-round cap is S5-only and its question has no round". `WINDOW_ROUND_CAP = 2` (`driver_machine.py:45`)
  is enabled for S5 (FV1-22 N2/N3 widen it to S7 / every stage); its question is the generic fallback (`retry` / `go on` / `stop`)
  with no round option. Report only; not the class of FV1-6.
- A6 — "A free answer the conductor continues on is filed as words for the reviewer". At a seam question about a running reviewer, the
  person's free words that the conductor answers with `continue`/`retry` are filed as `pending_words[<reviewer id>]`
  (`driver_machine.py:4101-4112`), and `wait_existing_job` resumes the REVIEWER with them (`driver_machine.py:1451-1453`) instead of
  finishing its saved result — at the exhausted review the words were usually about the author's round. Class: the words' addressee
  is chosen by `asked.dispatch`, not by what the conductor decided. Direction to choose: the conductor's `continue` after reading the
  words names whether they go to the role (a data column of the verdict) or the seam's `asked_why` marks the question as raised
  inside a finish, so its words are never filed for that dispatch.
- A7 — "After a refused chosen round and a conductor `continue`, a new paid critic runs over unchanged work". The critic was accepted
  with `OpenWork` (the stage open); `stage_critic_route` on the last round skips `stage_repair_owed` (`driver_stage_plan.py:612`), so
  the next `stage_S2` dispatches a fresh critic over the same artifact (the t-919 F-1 invariant of S4, `driver_stage_plan.py:795-798`,
  has no S2/S3 twin on the last round). Reachable after FV1-6 (E12). Direction: the S2/S3 entry derives an owed person's round from
  the record or asks the seam again, never a new critic over unchanged bytes.
