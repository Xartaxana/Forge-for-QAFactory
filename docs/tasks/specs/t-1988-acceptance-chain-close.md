# t-1988 — B-20: a stage closed by its consumer is not closed from where the driver stands — SPEC (designer draft)

Draft for the Lead. Forks are in §7 and are NOT decided here. Package read at `D:/ws1/wt-fbfix` (branch head); the run used
`D:/ws1/exp-thinking-roles\pkg-b` (0.10.9, `driver-state.json:72-76`). Every code fact below was checked in BOTH trees where it is
load-bearing (marked "both").

## §0 Short answer (what the evidence shows)

The loop was not a chain of acceptances. The analyst's `accept` record for S6 **was written** at 19:31:08 local
(`pipeline.json:790-802`, acceptor `qa-failure-analyst`, `reviewed_dispatch: S6-qa-runner-5`). From that moment the two readers of
"what is next" disagreed: the controller (`next`, `recover`, `checkpoint.json`) said `prepare_stage S6`, while the driver's own
reader `story_step where` said `prepare_stage S7`, because `where` calls `Controller._next_action_for_state(state)` **without the
pipeline**, and `acceptance.awaits_acceptance(..., pipeline=None)` skips the accept-record check. So the driver never entered
`stage_S6` again, and only `stage_S6` closes S6. It kept entering `stage_S7`, which closes nothing of S6, until the
"same step four times" stop. The person's `stage acceptance` word for S6 was not needed (the record already stood). The S7 word was
read and recorded, and then the S7 close was refused by the controller because S6 was still pending. That question
(`code_close`) has no door.

## §1 Goal, AR-n / FR touched, owner and census class of every check

**Goal.** A stage judged by its consumer role (S6 by the failure analyst, S7 by the doc scribe; `references/stages.json:195,221`)
closes as soon as its accept record stands, or as soon as a person's word passes it, whatever stage the driver is at. The driver
never asks the person about a state it can move itself, and when it must ask, it names the stage that holds and a door that opens.

**AR-n touched (host adaptation 9), with the change check each demands (copied into the node DoDs):**

| AR | how it is touched | change check written into the DoD |
|---|---|---|
| AR-13 (one reader) | `where` and `next` must read "S6 awaits" through one call, with the same inputs | N1 test: `where` == `next` on the B-20 state |
| AR-17 (one seam, settle before asking) | stuck loop and `code_close` behind-stage refusal | N3/N5: the driver's own move first; one question, through `no_move` |
| AR-24 (the person's words reach whatever acts) | `stage acceptance` word read from any driver position | N2 test: the S6 word is recorded while the driver is at S7 |
| AR-25 (every recorded state has a way out) | `code_close` S7 with `retry`/`stop` only | N3 test: the behind-stage case offers a door that moves the story |
| AR-28 (an unknown never becomes a pass) | `awaits_acceptance(pipeline=None)` reads "awaits" from an unread record | N1: no production caller passes `None`; error direction stated |
| AR-9 (refusal names a door) | `required prior logical stage incomplete` names no stage | N3: the lead names the stage and its door |
| AR-16 (one question form) | new closed question id `code_close.behind` | N3: `closed_question` literal, census of question ids green |
| AR-19 (stage twins) | S6 and S7 change together (`CONSUMER_ROUTES`) | every node test runs the S6 row AND the S7 row |
| AR-22 (producer/reader) | new state field `stuck_asked` (N5) | producer and reader in one commit, a test reads it |
| AR-27 (owner in the report) | close digest says "the doc scribe accepted" when the person did | N4 test: the digest names the person's word |
| AR-29 (where judgment lives) | no node judges a role's verdict | census rows (below) |
| AR-20 (shrink-only ratchets) | census `blocking_per_role` may rise by the new check units | a raise is named in the commit (`architecture:` line) |

**FR / principles:** FR-2, FR-7, FR-8, FR-9, FR-10, FR-35, FR-40, FR-42, FR-48, FR-57, FR-59; P13 (a pass by the person's word is
recorded in findings), P22 (the factory settles first), P27.

**Every check this spec adds or alters: owner and census class** (classes from
`scripts/tests/fixtures/judgment-census.json:3`: shape, xref, word-list, meaning-proxy, meaning, safety; owner data / judgment / intent):

| check (function) | node | what it decides | owner | class |
|---|---|---|---|---|
| `story_step._next` (read-only) passes the pipeline | N1 | which stage is next (record ↔ dispatch join) | data | xref (unchanged function, its input fixed) |
| `Driver.consumer_word_step` | N2 | does a recorded waiver `stage acceptance` exist for a stage that awaits its consumer | intent (it carries the person's word; it never reads the word's meaning) | shape (a match through `waiver.split_overridden`, the one reader) |
| `Driver.consumer_person_pass` (+ finding) | N2 | unchanged decision; adds the finding row | intent | shape (unchanged) |
| `Driver.code_close` behind branch | N3 | is the refusal the `behind` conflict, which stage is behind, does it await its consumer | data | xref (reads `controller.code_close_facts`, the one reading) |
| `NM.code_close_offer` row `code_close.behind` | N3 | which tokens are offered | data | shape |
| `Driver.consumer_close_words` | N4 | who accepted (record's `acceptor` and quote prefix `by: person`) | data | shape |
| `stuck_facts` + `stuck_asked` | N5 | facts for the lead; was this signature asked and answered | data | shape |

None of them reads what a role's verdict means. The consumer's verdict (`header.verdict` of its form) stays the role's judgment, and
the record is still written by the one writer `stage_done.py --acceptance` (AR-14).

## §2 Facts (file:line; logs and state files)

Line numbers are `D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\` unless named. Times: `driver-state.json`,
`driver-answers.jsonl` and `conductor.jsonl` are UTC (`+00:00`); the `at` of a `pipeline.json` acceptance record has no zone and
reads as local (UTC+1). Log progress lines are local.

### 2.1 Where the evidence is (claim correction)
- The driver logs are NOT in the tree. They are in `D:/ws1/yml-text-factory\experiments\mybooks\thinking-roles\runs\`
  (`arm-b-30.log` … `arm-b-34.log`). `runs/arm-b-3*.log` under `D:/ws1/mybooks-stand` gave no match; the same Glob under
  `experiments` found them (positive control).
- State: `D:/ws1/mybooks-stand\tr-arm-b\qa-factory\artifacts\LOCAL-1\` (`pipeline.json`, `state\*.json*`). Read only.

### 2.2 The sequence, from log and state lines
1. `arm-b-32.log:18-20` — `S6-qa-runner-5` (TC_016) accepted, "stage open". The runner's finish carries `stage_awaits_acceptance`
   (`run_manual_block` `complete = self.consumer_awaits("S6", True)`, `story_run.py:12256-12259`). `pipeline.json:106-119`: S6
   `pending`, reason "S6 awaits the acceptance of qa-failure-analyst".
2. `arm-b-32.log:23-24` — the next action is S7; analyst `S7-qa-failure-analyst-3` dispatched (S7 is let in while S6 awaits,
   `controller.py:4994-4998`, `8162-8168`).
3. `arm-b-32.log:28-33` — analyst-3's form is incomplete (`inputs_read` lacks the runner's form); the conductor reworks S7 →
   `S7-qa-failure-analyst-4` (`:33-39`), then again → `S7-qa-failure-analyst-5` (`:42-48`, cause `test_defect`). These are S7
   reworks by the conductor, not acceptance rounds of S6. Why analyst-3's finish wrote no S6 record: **could not establish** (its
   form and the `consumer_completion` branch it took were not read; consistent with `stage_verdict_known` false →
   `stage_review_exhausted(unreadable=True)`, `story_run.py:9472-9473`).
4. `events.jsonl` line 313 — accept of analyst-5 (`created_at` 1793903433). `pipeline.json:790-802` — the S6 accept record by
   `qa-failure-analyst` for `S6-qa-runner-5`, `at 2026-11-05T19:31:08` (local), `quote: ""`, `witness_paths: []`. Its author is
   most likely `consumer_settled` on the next `stage_S7` entry ("no record but an accepted consumer dispatch created after the
   awaited one: the record is written from its form", `story_run.py:9498-9503`): acceptor is the analyst, not `driver`, and the
   person's waiver came later (`pipeline.json:723-728`, 18:52:20Z). The exact call site is **inferred, not traced**.
5. From then on: `awaits_acceptance(state, "S6", pipeline)` is `""` (record stands, `acceptance.py:1341-1342`), so the controller's
   `next` says S6: `state/checkpoint.json:28-32` `next_action: prepare_stage S6, revision 313`. But `story_step where`
   (`story_step.py:147-149`, both trees) calls `controller._next_action_for_state(state)` with no pipeline
   (`controller.py:7982` default `pipeline=None`), so `awaits_acceptance` skips the record check (`acceptance.py:1341`
   `if pipeline is not None and …`, both trees: pkg-b `acceptance.py:1338`) and S6 still "awaits" by the runner's open-work word →
   `where` says S7. Witness: the conductor was handed `{"action": "prepare_stage", "revision": 313, "stage": "S7"}`
   (`state/conductor.jsonl:51`, end of `refusal`) and wrote "where still says prepare_stage S7; recover reported S6 as the next
   stage" (`conductor.jsonl:53`, `did`).
6. The driver loop asks `where` (`story_run.py:15663`), enters `stage_S7`: `awaiting` is `""` (pipeline given there,
   `story_run.py:12358`), so `consumer_settled("S6")` is not called; the analyst is done → `s7_repairs` → `s7_close` →
   `s7_await_scribe` prints "S7: the repairs ended; S7 awaits the acceptance of qa-doc-scribe for S7-qa-failure-analyst-5"
   (`arm-b-32.log:51-53`, three times, `story_run.py:12499`) and sets `pipeline.acceptance_awaits.S7` (`pipeline.json:822-824`).
   The scribe is never let in: the controller still says S6 (S6 not completed and not awaiting, `controller.py:8163-8174`).
7. Fourth identical `where` → `repeats >= 4` (`story_run.py:15668-15680`) → `no_move` → conductor 21 turns, $0.51, 501 s, answer
   `_unreadable` (`conductor.jsonl:51-52`) → question kind `refusal` "I cannot tell from here what is holding it"
   (`arm-b-32.log:54-90`, `stuck_text`, `story_run.py:2763-2772`).
8. Person (Lead) wrote `waiver.py --stage S6 --block "stage acceptance"` and the same for S7, then `retry`
   (`pipeline.json:716-729`; `driver-answers.jsonl:32`).
9. `arm-b-33.log:7` — "S7: a person's word passes the acceptance of S7-qa-failure-analyst-5; recorded as a driver accept (by:
   person)": `s7_await_scribe` → `consumer_person_pass("S7", …)` (`story_run.py:12483`) → `person_pass` → `stage_done.py
   --acceptance … --acceptor driver` (`story_run.py:9413-9416`); record `pipeline.json:803-817`.
10. Then `s7_closed_by_scribe` / `s7_close` → `close_by_code("S7", "the doc scribe accepted the failure analyst's triage", …)`
    (`story_run.py:12449-12451`) → controller `code_only` refused `{"error": "required prior logical stage incomplete"}`
    (`state/driver-question-details.md:5-8`; `controller.py:764-765`, `code_close_conflicts`, `behind` = S6 pending).
11. `code_close` question (`arm-b-33.log:9-38`, `arm-b-34.log:6-35`): offer `retry`, `stop`; "no word of yours passes what
    refused"; `driver-state.json:427-449` (`site: s7.accepted`, `step: receipt`, `offer: [retry, stop]`, two filed defects).
    `retry` gives the same (`arm-b-34.log:2-35`). The S6 waiver was never read anywhere (no S6 close site ran).
12. `standing-refusal.json:1-7`: `{"stage": "S7", "lines": ["required prior logical stage incomplete"], "doors": []}` — no door.

### 2.3 Where the person's `stage acceptance` word is stored and who reads it
- Stored: `pipeline.json` `stage_overrides[]` rows `{stage, match: "stage acceptance", decision, at, by}` (`pipeline.json:716-729`),
  written by `waiver.py --block`. The phrase is `acceptance.STAGE_ACCEPTANCE_PHRASE` (used at `acceptance.py:1402`,
  `story_run.py:9377,9436`).
- One matcher: `waiver.split_overridden` (`story_run.py:9406`). Readers that call it for a consumer stage:
  `consumer_person_pass` (`story_run.py:9366-9378`) ← called by `consumer_need_record` (the S6 sites `s6_reprobed_close` 11741,
  `s6_reentry` 11770, `manual_close` 11974; S7 `s7_close` 12815), by `consumer_settled` (9506 — ONLY after a record for the awaited
  dispatch exists: 9504 returns False first), and by `s7_await_scribe` (12483). The controller's author-finish gate reads it
  through `_passed_by_person` (`acceptance.py:1380-1412`).
- Not a reader: the router `awaits_acceptance` (records only, by design) and `story_step where`.

### 2.4 Lead's claims — verdicts
| claim | verdict |
|---|---|
| S6 stayed `pending` because it awaits the analyst's acceptance; the analyst ran three times; the chain looped | **corrected.** S6 awaited until 19:31:08 local; then the analyst's accept record stood (`pipeline.json:790-802`) and S6 stayed pending because no S6 close ran. The three analyst runs were conductor reworks of S7 (`arm-b-32.log:33,42`). The loop was `where` → S7 four times (§2.2 steps 5-7). The notebook line "запись приёмки S6 аналитиком так и не появилась" (`thinking-roles.md:155`) is wrong. |
| the S6 word is read only at the S6 close sites; at S7 it is not read, so the driver loops at S7 | **partly confirmed.** True that the S6 word is read only at the three S6 close sites and, at S7, only when a record for the awaited dispatch already exists (§2.3). But in this run the word was not needed; the root is the reader drift `where` ≠ `next` (§2.2 step 5). Both defects are real; the first one stopped the run. |
| `code_close` state with no door | **confirmed** (`driver-state.json:427-449`, `standing-refusal.json`). Also: its lead says "the doc scribe accepted the failure analyst's triage" while the record is a driver accept by the person's word (`pipeline.json:803-816`, `CODE_CLOSE_SITES["s7.accepted"]`, `story_run.py:621`) — FR-10/FR-35. |
| the run was stopped by the Lead; the tree is kept | **confirmed** as far as the files go: `driver-state.json:60-65` `asked: code_close S7 at 18:55:22Z`, `arm-b-34.log` ends with the question; notebook `:156`. That no driver process is alive: **could not establish** (not measured). |
| the logs are in `tr-arm-b\runs` | **corrected** (§2.1). |

### 2.5 Neighbours noticed (reported, not widened)
- `[progress] S6 Run … done S0–S5, S9` while the driver is at S7 (`arm-b-32.log:25,46`; S9 `done` from the first pass,
  `pipeline.json:150-163`). The progress line reads `pipeline.json` stage order; a stale S9 `done` after a reopen is shown as done.
- `events.jsonl` line 312 carries `acceptance_awaits: {"S7": "S7-qa-failure-analyst-1"}` (first pass) until the marker is rewritten.
  Harmless here (marker bound to a dispatch), noted.
- `code_close` filed the factory defect twice for one cause (`driver-state.json:431-434`, two sites). Not in scope.
- The S6 record from the analyst has `quote: ""` and `witness_paths: []` (`pipeline.json:798-799`); whether the writer should
  accept an `accept` with no quote is a separate question (the S3/S4 records carry template text as quote,
  `pipeline.json:755-757,783-785`). Not in scope; queue candidate.

## §3 The class walk (rule 9; `docs/SIBLING_MAP.md` axis 5 "stage twins", axis 32 "where judgment lives")

Class: **the close of a stage that its consumer role (a later stage) accepts must be reachable from wherever the driver stands, and
every reader of "does this stage still await its consumer" must give the same answer.** Consumers are exactly the stages whose
`acceptance_by` is outside their own roles (`acceptance.consumer_of`, `acceptance.py:1346-1350`). Positive control for the
negative lines below: the Grep for `acceptance_by` in `references/stages.json` matched lines 58, 95, 130, 195, 221 and nothing in
the S0, S1, S5, S8, S9 blocks.

| boundary | verdict |
|---|---|
| S0→S1 | n/a — no `acceptance_by`; S0 closes by code. |
| S1→S2 | n/a — S1 has no `acceptance_by`. |
| S2 (critic inside S2) | n/a for the consumer defect — `acceptance_by` is the stage's own `qa-case-critic`, so `consumer_of` is `""` and `awaits_acceptance` is `""` (`acceptance.py:1321`); the close is inside `stage_critic_route`. The word is read by `stage_acceptance_refusal` → `_passed_by_person` at the author's finish (covered). |
| S3 | n/a, same as S2. |
| S4 | n/a, same as S2. |
| S5→S6 | n/a — S5 has no `acceptance_by` (window critics inside S5). |
| **S6→S7** | **the defect, live** (§2.2). Covered by N1 (routing) + N2 (word from any position) + N3 (behind-stage close). |
| **S7→S8** | **same defect possible, by reading** (no live case). When the analyst's last S7 finish carries `stage_awaits_acceptance` (the repair rework, `CONSUMER_ROUTES["S7"]["rework_complete"]`, `story_run.py:9342`), `where` without the pipeline keeps saying S8 after the scribe's record stands; the scribe's second dispatch is then refused by the controller (`controller.py:4995-4998`). When S7 awaits only by the marker `acceptance_awaits` (`s7_await_scribe`), `where` without the pipeline reads no marker and says S7 — consistent by accident. Covered by the same N1/N2/N3; tests run the S7 row. |
| S8→S9 | n/a — S8 has no `acceptance_by`; S9's code close has its own recover (`code_close` S9 branch, `story_run.py:15774-15783`). |
| any code-closed stage with an earlier stage incomplete (`behind`) | **same no-door question possible** at every `CODE_CLOSE_SITES` site (`story_run.py:615-628`): S6 sites behind S5, S7 sites behind S6, S9 behind S8 (this tree has S8 `pending`, `pipeline.json:134-148`). Covered by N3 (one branch in `code_close`, not per site). |

**One mechanism at the seam, not a patch per site:** (1) one reading of "next" for both `where` and `next` (N1); (2) one loop step
that turns a person's `stage acceptance` word into the record for ANY consumer stage, before `where` (N2) — the same place
`code_close_step` already holds (`story_run.py:15656-15661`); (3) one branch in `code_close` for the `behind` conflict (N3).

## §4 Design

**D1 — one reading of "next" (N1).** `story_step._next(read_only=True)` passes `controller._pipeline()` to
`_next_action_for_state`. After it, `where` and `next` differ only by `close_settled` (the reason the read-only path exists,
`story_step.py:145-146`), never by the pipeline. `_pipeline()` reads only (`controller.py:4338-4344`).
- **Reused function in a more consequential role:** `awaits_acceptance` is the ROUTER that sends the driver past a stage. Direction
  of permitted error: when it cannot read the record (pipeline unreadable → `{}`), it says "awaits" and the driver goes to the
  consumer's stage, whose host writes the record from the consumer's form (`consumer_settled`) — the safe side, because the
  consumer's stage closes nothing of the awaited stage and the controller still refuses any later stage. It must NEVER say "not
  awaiting" for a stage that has no record (that would route to the author's stage and could close it by its own finish — the
  thing X7-6 forbids). Adversarial inputs that must stay on the safe side: record for an EARLIER author dispatch (→ awaits), a
  `reject` record (→ awaits), record with `acceptor` other than the consumer and not `driver` (→ `accepted_for` checks only
  `reviewed_dispatch` and verdict when `acceptor` is None — unchanged, stated), `pipeline=None` (→ must not occur in production
  after N1; test pins the production caller), `pipeline={}` (→ awaits).

**D2 — the person's word reaches the stage from any position (N2).** A new loop step `consumer_word_step()`, placed right after
`code_close_step` and before `where` (`story_run.py:15656-15663`). For each stage of `CONSUMER_ROUTES` (S6, S7 — the table is the
one list): `did = acceptance.awaits_acceptance(controller_state, stage, pipeline)`; if `did`, call
`consumer_person_pass(stage, did)` (unchanged matcher and writer). True (turn spent) when a pass was recorded. The pass itself
writes nothing new: it is the existing driver accept `by: person`. What is new: `consumer_person_pass` files ONE finding per pass
(P13) through the same row `code_close` uses for `go on` (`owe_row("project_decisions.py", … "add-finding", …)`,
`story_run.py:15892-15895`), idempotency key `stage-acceptance-pass:<task>:<stage>:<author>`; every site that passes by word gets
it (one place). After the record, N1's routing sends the driver to the awaited stage, whose own close site runs and finds the record
(`consumer_need_record` passes, `story_run.py:9431`).

**D3 — a code close behind an incomplete stage (N3).** In `code_close` (`story_run.py:15763`), when the refusal is the controller's
`required prior logical stage incomplete`, read `controller.code_close_facts(controller_state, stage)["behind"]` (the one reading,
`controller.py:716-745`) — never the refusal's words. Two cases:
- (a) the behind stage does NOT await its consumer (`awaits_acceptance` is `""`): the driver's own move — print one line
  ("<stage> is closed after <behind>, which is not closed yet; the factory goes back to it"), file nothing, return `retry`; `where`
  (N1) now routes to the behind stage. Bounded: the same `(stage, behind, controller revision)` seen a second time without the
  revision moving → case (b) wording with `retry`/`stop` and the facts, through `code_close_ask`.
- (b) the behind stage awaits its consumer: the question key `code_close.behind`; lead names the behind stage (`stage_place`), its
  author dispatch, and that it waits for `<consumer>`'s acceptance; offer `go on` (= the person's word passes the acceptance of the
  BEHIND stage: `consumer_person_pass(behind, did, answer=words)`, then `retry`), `retry`, `stop`. Never "no word of yours passes"
  when a word would pass the behind stage.

**D4 — the close says who accepted (N4).** `s7.accepted` / `s6.accepted` digests and the `code_close` lead are built from the
record: acceptor `driver` with quote starting `by: person` → "your word passed the acceptance of <stage>"; consumer role → as today.
One helper `consumer_close_words(stage)`; `CODE_CLOSE_SITES` keeps the consumer text as the default.

**D5 — the stuck seam says what code can read and asks once (N5).** `repeats >= 4` becomes the named constant `STUCK_REPEATS = 4`
(module data, next to `CODE_CLOSE_IDLE_CAP`). `stuck_facts(controller_state, pipeline, stage)` (pure) returns lines for every stage
before `stage` that is not completed: status, `reason`, `awaits_acceptance` result, whether an accept record stands and for which
dispatch. `stuck_text` puts them under the lead instead of "I cannot tell from here" when there is at least one. `state["stuck_asked"]
[signature] = answered_at` is written when the person answers a stuck question; a second stuck with the same signature after an
answer goes to the conductor with "you answered <token> at <time>; the same step still comes back" — new text, never the same
question again (FR-7).

**What the report says.** The stage digest (pipeline `stages.<S>.digest`, read by progress and the S8 report renderers) carries D4's
words. Whether `test-report.md` renders stage digests at all: **could not establish** (not read) → fork F4.

**No compatibility** with stories written by an older package version (owner, notebook `:154`): no migration of `driver-state.json`
`code_close` records, no reading of old `stuck` state.

## §5 Nodes (for a weaker model; owns are absolute; witness = the fast file of each node, run from the builder's worktree package root; `test_story_run_*`, `test_controller_*` are CI only)

Common `given` for every node: this spec; `D:/ws1/wt-fbfix\ai-packages\qa-factory\design\factory-rules.md` (whole);
`D:/ws1/yml-text-factory\plans\builder-rules.md` (7b: witness scope and the SLOW_TESTS list);
`D:/ws1/wt-fbfix\ai-packages\qa-factory\design\architecture.md` (AR-13, AR-17, AR-24, AR-25, AR-28, AR-29);
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_stage_acceptance_consumer.py` (the fixture style to copy:
`consumer_state`, `T.write_pipeline`, `A.awaits_acceptance`).

### N1 — `where` reads the pipeline (the root of B-20)
- owns: `D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\story_step.py` (function `_next` only);
  `D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_consumer_close_route.py` (new).
- change: `story_step.py:147-149` → `controller._next_action_for_state(state, controller._pipeline())`. Docstring of
  `controller._next_action_for_state` NOT changed (controller.py is not owned; F1).
- tests (new file, fast, no subprocess driver):
  1. B-20 state, S6 row: runner's last dispatch accepted with `stage_awaits_acceptance`, accept record for it stands → `where`'s
     action stage == `next`'s == `S6`.
  2. Same, no record → both `S7`.
  3. S7 row: analyst's last dispatch carries the awaits word, scribe's accept record stands → both `S7`; no record → both `S8`.
  4. Record for an EARLIER runner dispatch → both say the consumer's stage (S7).
  5. `reject` record → both S7.
  6. Unreadable `pipeline.json` (bad JSON) → both S7 (stated direction, D1).
- edges + invariants: TEMPORAL — before the record exists `where` says the consumer's stage, after it the author's stage; the move
  that creates it is the consumer's finish or N2. Invariant: `where` never names a stage past one whose record stands and that is
  not completed. POSITIONAL — none (one call).
- DoD: the six tests green; `python -B scripts/tests/test_consumer_close_route.py` output is the witness; `architecture: AR-13,
  AR-28 -- where and next read the same pipeline`.

### N2 — the `stage acceptance` word is read from any driver position, and filed
- owns: `D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\story_run.py` — functions `consumer_word_step` (new, beside
  `consumer_person_pass`), `consumer_person_pass` (adds the finding), and the loop body of the method holding
  `story_run.py:15634-15710` (ONE inserted step after `code_close_step`); `…\scripts\tests\test_consumer_close_route.py` (adds
  tests; same file as N1 → N2 runs after N1 or N1+N2 is one builder, F5).
- behaviour: §4 D2. `consumer_word_step` returns False when no stage awaits or no word passes; True after a recorded pass.
- tests:
  1. S6 awaits (no record), waiver `stage acceptance` for S6 recorded, driver "at S7" (no stage host called) → after one
     `consumer_word_step`: driver accept for the runner's dispatch stands; `where` says S6.
  2. Same for S7 (scribe's stage S8).
  3. No waiver → False, nothing written.
  4. Waiver for S6 while a NEWER runner dispatch is running (awaits is `""` because the last author row is not accepted) → False,
     nothing written.
  5. Two passes of the same stage/author → one finding row (idempotency key).
  6. The finding text quotes the person's words (first 500 chars, as `person_pass`).
- edges + invariants: POSITIONAL — after `code_close_step` and the person's chosen reworks (a rework may open the stage again and
  change its author: the word then binds to the author `awaits_acceptance` names now) and BEFORE `where` (so the router sees the
  record this turn). Invariant: a word never accepts a dispatch that is running or was superseded; the record is written only by
  `stage_done.py --acceptance` (AR-14). TEMPORAL — the waiver may exist before the author ran (an early word): F2 decides whether
  it counts. Empty/absent: no pipeline → no stage awaits → False.
- DoD: tests green on the fast file; `test_judgment_census.py` green with the new row (`consumer_word_step`, class shape, owner
  intent); a `blocking_per_role` raise, if the census test demands one, named in the commit; `architecture: AR-24, AR-25, AR-14 --
  the word is recorded by the one writer from any position`.

### N3 — a code close refused because an earlier stage is open
- owns: `story_run.py` functions `code_close`, `code_close_lead`, `code_close_person`, `_answer_code_close` (the `go on` branch for
  key `code_close.behind`); `D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\no_move.py` function `code_close_offer`;
  `…\scripts\tests\test_code_close_behind.py` (new).
- behaviour: §4 D3. The behind facts come only from `controller.code_close_facts`.
- tests:
  1. S7 close refused, S6 pending with a standing record → `code_close` returns `retry`, no question, one printed line.
  2. Same refusal twice at the same controller revision → the question `code_close.behind` with `retry`/`stop`, lead names S6.
  3. S6 awaits its consumer (no record) → question `code_close.behind` offers `go on`, `retry`, `stop`; the lead names S6, the
     runner's dispatch and the failure analyst.
  4. `go on` answer → driver accept recorded for S6's author (through `consumer_person_pass`) and `retry` follows; the finding
     row exists (N2).
  5. The refusal is another conflict (`checkpoint active work…`) → today's behaviour unchanged.
  6. S9 behind S8 → case (a)/(b) by the same branch (no S9-specific code).
- edges + invariants: POSITIONAL — the behind branch runs before `file_defect` (a behind stage is not the factory's defect) and
  after the S9 `recover` branch (`story_run.py:15774-15783`, unchanged). Invariant: the driver never closes a stage over an open
  earlier stage, and never asks "no word of yours passes" when the earlier stage accepts a word. LIMIT — the bound in case (a) is one
  silent retry per controller revision (F3). Unreadable controller state → today's question (FR-59).
- DoD: tests green; the question-id census green with the literal `code_close.behind`; `architecture: AR-25, AR-9, AR-17, AR-16 --
  the behind stage is named with a door`.

### N4 — the close says who accepted
- owns: `story_run.py` — `CODE_CLOSE_SITES` (texts only), new `consumer_close_words`, the `close_by_code` call lines inside
  `s7_closed_by_scribe` and inside `stage_S6` (the `s6.accepted` call at `story_run.py:11452-11453` only);
  `…\scripts\tests\test_code_close_behind.py` (adds tests; after N3).
- tests: record acceptor `driver` + quote `by: person - …` → digest and lead say the person's word; acceptor the consumer role →
  today's words; no record → the default text (the close is refused upstream anyway).
- edges + invariants: the words come from the record, never from the refusal text; a person's pass is never reported as a role's
  verdict (FR-35).
- DoD: tests green; `architecture: AR-27 -- the report names the person's pass`.

### N5 — the stuck seam carries facts and asks once
- owns: `story_run.py` — `stuck_text`, new `stuck_facts`, the `repeats` block of the loop (`story_run.py:15668-15680`), the place
  the stuck answer is taken (the `refusal` kind answer road; builder finds it by `stuck_text` callers — F6), new constant
  `STUCK_REPEATS`; `…\scripts\tests\test_stuck_facts.py` (new).
- tests: B-20 state → facts name "S6 pending; acceptance by the failure analyst stands for S6-qa-runner-5"; no earlier stage open →
  today's lead; second stuck with an answered signature → the conductor text names the earlier answer, not the same question.
- edges + invariants: `stuck_asked` producer and reader in one commit (AR-22); an unreadable pipeline → no facts lines, today's lead
  (FR-41: an unknown is not reported as a fact).
- DoD: tests green; `architecture: AR-17, AR-22, FR-7`.

### Order and overlap with work in flight (hot file `story_run.py`, D-0048 disjoint function lists)
- t-1968 N5 (`Person.__init__`, `_person_of`, `ask`, `held_question`, `window_round_gate` S5 branch, `seam_chosen`,
  `probe_judgment_lead`): **disjoint** from N1–N5. N5 here touches the stuck answer road — if that road is `ask`, N5 waits for
  t-1968 N5 (F6).
- t-1957 N5s (`run_manual_block`, `run_role` walk lanes): **disjoint**; this spec only relies on `run_manual_block` → `manual_close`
  closing S6 when no block is left (§6 proves it live).
- t-1986 U3 (`stage_S7`, `s7_close`): **disjoint** — N4 touches `s7_closed_by_scribe` (a sibling method), not `stage_S7`/`s7_close`.
- Order: N1 first (it alone fixes the live run); N2 and N3 in parallel after N1 (different functions; N2's tests go into N1's file,
  N3 has its own); N4 after N3 (same test file); N5 independent.

## §6 Questions for the owner

None. Everything here is the factory's own routing and wording; no product, money or outward decision.

## §7 Forks for the Lead

- **F1 — make `pipeline` required in `_next_action_for_state`.** (a) keep the default `None`, fix the one production caller (N1),
  pin by test; (b) make it required — ~20 test call sites change (`test_launch_card.py`, `test_diagnosis_honesty.py`,
  `test_resume_packet.py`, …; Grep `_next_action_for_state\(`). Recommendation: (a) now, (b) as a queued item.
- **F2 — a word recorded before the author dispatch ran.** `person_pass` has a `since` rule that is not used by
  `consumer_person_pass` (`story_run.py:9378`, `since` empty). (a) as today: any live `stage acceptance` waiver for the stage passes
  the author's last dispatch; (b) honour it only when its `at` is later than the author dispatch's acceptance (FR-4: a word never
  accepts work the person never saw). Recommendation: (b); the builder reads the acceptance time from the controller dispatch row,
  and an unreadable time is "not honoured" (the existing `person_pass` rule). Note: (b) also changes the three existing S6 sites.
- **F3 — the bound of the silent retry in N3 (a), "declared as data".** (a) reuse `CODE_CLOSE_IDLE_CAP` (one bound for the code-close
  seam); (b) a new row in `references/driver-infra.json`. Recommendation: (a) — a bound is not project variety (AR-1).
- **F4 — the report line.** Whether `test-report.md` shows a stage closed by the person's word beyond the digest and the finding:
  (a) digest + finding only (N4, N2); (b) a code-owned report line. Recommendation: (a) now; (b) queued after reading the renderers.
- **F5 — N1 and N2 as one builder.** Same new test file. Recommendation: one builder for N1+N2 (both small), N3 parallel.
- **F6 — N5's answer road.** If the stuck answer is taken in `ask`/`take_answer` (shared with t-1968 N5), N5 waits for t-1968 N5.
  Recommendation: schedule N5 after t-1968 N5 merges.

### Small choices I closed (no design weight)
- New test files are separate from `test_stage_acceptance_consumer.py` (its SLOW status: could not establish; a new fast file keeps
  the witness narrow).
- Helper names `consumer_word_step`, `consumer_close_words`, `stuck_facts`, constant `STUCK_REPEATS`.
- The finding row reuses `project_decisions.py add-finding` with `--scope local-calibration` (as `code_close` `go on`).

### Live proof (FR-33)
On a COPY of the kept tree (the tree stays evidence; P8): copy `D:/ws1/mybooks-stand\tr-arm-b` to a new stand copy, run the
driver of the new package with `--answer` = `retry` to the open `code_close` question. Expected log lines, in order: no
`code_close` question; `where` says S6 (`--dry-run` first: "where: {…"stage": "S6"…}"); `stage_S6` → `manual_close` → S6
closed (site `s6.manual_close`, `CODE_CLOSE_SITES` text); S7 closes by the standing person's record with N4's words; S8 is let in.
What this does NOT prove: N2 on a story with no record (needs a fresh short run where the analyst's form is unreadable — F-run
queued) and N3 (b). Cost estimate (not measured): the copy run to gate B ≈ one scribe + one bug reporter session.

## Reading trail
- Notebook `experiments/mybooks/thinking-roles/thinking-roles.md:125-180`.
- Logs `experiments/mybooks/thinking-roles/runs/arm-b-32.log` (whole), `arm-b-33.log` (whole), `arm-b-34.log` (whole).
- Tree `…\tr-arm-b\qa-factory\artifacts\LOCAL-1\`: `pipeline.json:91-163, 690-843`; `state\driver-state.json` (whole);
  `state\checkpoint.json:1-110`; `state\events.jsonl` lines 281-313 (heads) and 312 (whole); `state\conductor.jsonl:1-5, 51-53`;
  `state\driver-answers.jsonl` (grep: lines 32-33); `state\passed-by-person.jsonl`; `state\standing-refusal.json`;
  `state\driver-question-details.md`. `state\controller.json` not read (470 KB; `events.jsonl:312` carries the projection).
- Package `wt-fbfix`: `story_run.py:593, 615-630, 1490-1530, 2730-2790, 9325-9615, 11440-11560, 11735-11870, 11969-12000,
  12230-12510, 13355-13420, 14936-15033, 15630-15760, 15763-15962, 17880-17922`; `acceptance.py:1230-1430`;
  `controller.py:700-790, 4338-4360, 4975-5004, 7665-7735, 7982-7994, 8130-8175`; `story_step.py:144-152, 3173-3191`;
  `references/stages.json:50-300`; `scripts/tests/fixtures/judgment-census.json:1-6`.
- Package `pkg-b` (the run): Grep `controller._next_action_for_state\(state\)|if pipeline is not None and accepted_for` →
  `story_step.py:149`, `acceptance.py:1338` (the same Grep on `wt-fbfix` found `story_step.py:149`, `acceptance.py:1341`: positive
  control).
- Negative claims and their controls: "only `story_step.py:149` calls `_next_action_for_state` without the pipeline in production" —
  Grep `_next_action_for_state\(` over `scripts/*.py` found the with-pipeline calls `controller.py:1792, 4415, 7698, 7807, 8940` in
  the same output; "no `acceptance_by` on S0/S1/S5/S8/S9" — Grep matched S2/S3/S4/S6/S7.
- Spec `docs/tasks/specs/t-1955-manual-lane-doors.md` (headings only: N1–N4 = B-16..B-19; it does not touch the consumer close or
  `where`; nothing of B-20 is in it). Review t-1971: **not read** (budget). `docs/SIBLING_MAP.md`: axis headings only (axes 5, 32
  named). `docs/factory-map/`: **not read**. `design/architecture.md`, `design/factory-rules.md`: the one-line indexes loaded in
  CLAUDE.md only, full text not read.
- Needed beyond the manifest: `story_step.py`, `no_move.py`, `references/stages.json`, `judgment-census.json`, the `pkg-b` tree.
