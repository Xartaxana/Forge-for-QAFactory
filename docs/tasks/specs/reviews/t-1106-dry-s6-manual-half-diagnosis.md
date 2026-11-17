# t-1106 — critic: the dry story's stop at the manual half of S6 (diagnosis) + verdict on 5979acb4

Reviewer: critic (opus). Tree: `C:/QAFactory/forge-repo/.claude/worktrees/agent-a5fe6ff90fd3dc296` at `5979acb4`.
All `file:line` below are in that tree, under `ai-packages/qa-factory/`.

## Job 1 — diagnosis

### Q1. What does the factory intend for a manual-agent case after the person says "no stand, go on"?

**Short answer.** The factory says the person's no-stand word is a decision it applies, not a question it asks again
(D-0047). No rule says a manual-agent walk is sent out with no stand. The only roads that exist for a manual case whose
block cannot be walked, when the person has said `go on`, all close the case **before** anything is dispatched: the
request gets `refused` with `by: left_unchecked` and the person's words, it goes into the `manual_skipped` lane, and
`manual_close` closes the half by code. The manual half never reads the no-stand word, so today it dispatches a walk
that can only fail. That is a missing reader. The rules do not intend it.

The texts that decide this:

1. What the person is told `go on` means (`scripts/driver_stage_build.py:129-131`): *"go on without a stand" + (S5) "; the
   tests are still written, but none is run on a stand" + ", and the story carries a line saying it was your decision"*.
   Its price row is `references/question-prices.json` `s6.stand_confirm` `go on`: `factory: record`, `delivery: not_known`,
   `unverified: which stand the tests ran on`. That text was written for automated tests ("none is run on a stand").
   Nothing in it tells the person that a manual-agent case will still be walked.
2. FR-36 (`design/factory-rules.md:350`): *"A capability the run's standing decision forbids is neither probed nor
   advertised."* The standing decision is "no stand". A walk on a stand is that capability.
3. D-0047 (`DECISIONS.md:38`): *"a standing decision is applied WITHOUT a new question but SAID OUT LOUD"*.
4. The sibling gates in the same function already follow this pattern:
   - `stand_login_gate` (`scripts/driver_stage_s6.py:1249-1302`). Its POSITION invariant: *"no block holding a screen case
     exists while the account is missing and no word passes it"*. When a word passes, it calls `refuse_case(..., by)` with
     `left_unchecked` for `go on`, and the half closes code-only through `manual_close`.
   - `walk_refuse_gaps` (`:27-58`): *"a lane that cannot walk costs no role"*. Refused `left_unchecked` before the first
     dispatch.
   - `gate_a_dry_person` `go on` (`:1013-1014`): *"the report carries them as not checked, in your words"*.
5. `skills/qa-story/phases/s6.md:115-119` and `agents/qa-runner.md:74` cover a stand that **exists** but whose probe fails
   or does not match: `env_blocked[]` with the probe line, *"no record"*. That road needs a capture attempt. With no
   `environments[]` there is none: `manual_capture.py:537-541` refuses (*"config.json has no environments[] with a
   base_url ..."*) before any attempt or `env_blocked.json` exists (`manual_capture.py:3370`: *"comes BEFORE an attempt, a
   session or a probe exists: no stand ..."*).

**What happens today, traced step by step** (`driver_stage_s6.py:480-589`):

- `stage_S6` → `stand_check("S6", "both")` returns because the S5 word passes it (`driver_stage_build.py:170-175`).
- `build_check` returns because nothing is named or confirmed (`driver_stage_build.py:305-307`).
- `no_stand = self.s6_no_stand()` is True (`:519`, `:672-681`). The automation half reads it: K4 at `:565` (no probe, an
  `S6_LEFT` line) and `s6_reprove` at `:736`.
- `run_manual_block(manual_scope)` at `:589` → `manual_lane_plan` (`:1304-1336`). This function **never reads `no_stand`**.
  It calls `manual_gate_note`, then `manual_plan` (each case is prepared), then `stand_login_gate`, `walk_refuse_gaps` and
  `walk_assign_*`. Then `run_manual_lane` registers `S6-qa-runner-2`, `walk_before` opens a guest walk, and the role
  starts.
- The role has no tool that can put TC-2 into a lane:
  - every `manual_capture` call is refused with no stand, so no attempt and no `env_blocked`;
  - `manual_evidence.py build` refuses *"nothing was captured"* (`manual_evidence.py:1851-1853`);
  - `manual_evidence.py unprepared` refuses a prepared case (`:1484-1488`).
- `walk_after` → `walk_case_records` → `walk_refusal` (`driver_dispatch.py:1487-1501`): the first refusal is "walked once
  more". Meanwhile this block's exit gate refuses its own handoff, because `validate_artifacts.py:2147-2157` (TC-2 is in
  this block's `manual_case_ids`) finds no lane. The result is the `exit_limit` question to the person: the dry stop.
- If the person answers, the most the current code can reach is a second walk session and then `left_unchecked` with the
  wrong reason (*"the record of its walk was refused twice - nothing was captured"*). That costs two role sessions and one
  question for an outcome the person already decided.

**One road or two (P31)?** One carrier, `Driver.s6_no_stand` (SIBLING_MAP axis 26: the word's one reader is
`waiver.split_overridden`, called from `stand_check`, `s6_no_stand`, `check_delivery.stand_word` and `_take_stand_answer`).
Today the automation half reads it and the manual half does not. It is not two roads for one action. It is one action
(the person's no-stand word) that reaches only one of the two halves it covers (FR-8 / AR-24: *a person's words reach
whatever acts on them*). The road the manual half lacks already exists for its siblings: `refuse_case` → `manual_skipped`
→ `manual_close`. The fix adds a reader. It does not add a road.

### Q2. Classifying the stop

**(a) PRODUCT DEFECT. This is the classification.**

- Function: `S6Mixin.manual_lane_plan` (`scripts/driver_stage_s6.py:1304`). It is reached from `run_manual_block` (`:1580`).
- Missing branch: when `self.s6_no_stand()` is True, the manual-agent cases are not prepared and not dispatched. Each one
  is refused `left_unchecked` in the person's words, and the half closes by `manual_close` (site `s6.manual_close`).
- Expected behaviour:
  - no `S6-qa-runner-<n>` manual dispatch is registered;
  - no walk session is opened;
  - no stand-login or gate-A-dry question is asked;
  - `request.json` of each case holds `{"refused": {"reason": "not checked by an agent: no stand is confirmed for this
    story; the person said: \"<words>\"", "door": ..., "by": "left_unchecked"}}`;
  - `run-report.json` carries the case in `manual_skipped[]`;
  - S6 closes code-only and moves to S7.
- Test row that pins it: `scripts/tests/test_story_run_s6.py`, next to the K4/P11 row (`:2450-2467`, which already builds
  the `word` fixture `{"stage": "S6", "match": "stand not confirmed", ...}`). Same world, manual scope `[<case>]`. Expect:
  no `controller.apply("dispatch", ...)`, no Person, `request.json.refused.by == "left_unchecked"`, its reason quotes the
  word, and the close site `s6.manual_close`. Its control is the same story with the stand confirmed (`environment` named,
  `environment_pending` false), where the block is dispatched as today. The one probe: delete the branch, and the first
  check goes red.
- The finding's class in factory terms (P2, not a rule of one project): *a person's word that passes a stage-entry blocker
  must reach every half of the stage that the blocker covers; a half that cannot work without what the person declined
  sends out no role and closes its cases as not checked, in the person's words* (FR-8, FR-36, AR-24, AR-25; D-0047). It
  holds for any project whose plan has manual-agent cases and whose person declines a stand.

**(b) DRY-WORLD GAP: no.** "Give the dry world a stand" would not be honest for a stub with no product. A stand needs a
host for `manual_capture` to reach, a runtime probe that matches the build, and a page or endpoint that has a Then to
quote. The stub would have to make up every capture its verdict quotes (`agents/qa-runner.md:23` *"Each verdict quotes a
capture of this attempt"*). That is exactly what the builder correctly refused to do. The dry world truthfully has no stand
because S5's answer row says `go on` (`story.json` walk S5 `answers.environment: go on`). That is a real-project state.

**(c) KIT CHOICE: no.** If TC-2 became `manual-human`, dry-1 would lose its only manual-agent case. `kit.json` holds two
cases: TC-1 automate and TC-2 manual-agent. No other dry row would cover the manual half of S6 (scope, prepare, `manual_close`,
the coverage check of the manual lane). It would also hide the defect above rather than pin it.

### Q3. The recommended move (one builder)

**Files and functions:**

1. `scripts/driver_stage_s6.py` `manual_lane_plan`. Right after `waiting = self.deferred_waiting(cases)` and **before**
   `manual_gate_note()`, add:

   > if `self.s6_no_stand()`: for each case of `self.manual_order(cases)` that is not in `self.manual_done()` and not
   > waiting, call `self.refuse_case(plan, case, reason, door, "left_unchecked")` and print
   > `S6: <case>: not checked by hand — <reason>`. Call `self.walk_assign_clear()`. Return
   > `({"blocks": [], "refused": [...], "unprepared": []}, waiting)`.

   - The reason quotes the passed word, read the way `stand_login_gate` reads it (`:1277`, `:1288`), but through the
     block `waiver.stand_block(environment)` that `s6_no_stand` already uses. No second reader of `stage_overrides`
     (axis 26). A small helper that returns the passed decision words beside the bool is the clean form.
   - Door: *"record a stand for the project (onboarding) and confirm it; the manual checks are then run again (retry at
     gate B)"*.
   - `run_manual_block` then reaches `manual_close(cases, plan["refused"])` unchanged.
2. `scripts/driver_stage_build.py` `stand_question_text` (`:129-131`), the ONE site of the `go on` text for both stages.
   When the stage's plan has manual-agent cases (S6 `kind` in manual/both; S5: plan rows with `manual-agent`), the `says`
   adds *"; the cases an agent checks by hand are left unchecked"*. Otherwise the person's price is incomplete (FR-9, B).
   The census tests of question texts (`test_human_questions.py`, `test_story_run_words.py`) follow.
3. `docs/SIBLING_MAP.md` axis 26: add the manual half (`manual_lane_plan` via `s6_no_stand`) to the list of readers, in the
   same commit. This file is outside the package; it is the Lead's to place.
4. `skills/qa-story/phases/s6.md` card line 5 / § "The stand": one sentence for the skill road: *"with the word `stand not
   confirmed` the manual-agent cases are not dispatched; they stand as not checked by hand, in the person's words"*. The
   skill road and the driver road must stay one road (P31).

**Edges (each a row, or one parameterised row):**

| world | expected |
|---|---|
| no stand + `go on` (word recorded on S5 or S6, environment empty) | branch taken: no manual dispatch, cases `left_unchecked` with the words, `manual_close` |
| a stand named but not confirmed (`environment_pending`) + `go on` | the same: `s6_no_stand` is True and the person said *without a stand*. FR-36 says the walk is not tried. This direction is decided here and written into the spec |
| no stand + `stop` | no word is recorded: `stand_check` raises the question / the story stops before `manual_lane_plan`. Nothing changes (control: no `refused` written) |
| a confirmed stand | `s6_no_stand` False: today's road, the block is dispatched (control row) |
| a manual-human case | not in the manual scope (`stage_scope` `manual` returns `manual-agent` only). Untouched, reported with the person as today |
| a case already done by an accepted manual dispatch of an earlier life | stays done, not refused (`manual_done`) |
| a case a deferred question holds | left to `manual_close`'s deferred road (not refused twice) |
| with a consumer (`acceptance.consumer_of("S6")`) | `manual_close` already calls `consumer_need_record`. No new handling |

**Non-goals:**

- The automation half (K4 stays as it is).
- A code-only close of the whole S6 when every automated result stands and all manual cases are refused by no stand.
  `:523` still dispatches the runner because `manual_scope` is non-empty. That is an optimisation, not this defect.
- The walk-retry versus coverage-gate interplay: a first build refusal leaves its case with no lane in its own block, and
  the gate refuses that block. That is reachable with a stand too, and it belongs to the walk-retry design
  (`driver_dispatch.py:1371-1501`, `validate_artifacts.py:2108-2157`). The Lead should look at whether `walk_pending` cases
  are meant to be exempt there. It is outside this move.

**`known_red.json`:** the row `main/S6` leaves (it turns green). The dry pass then stops at the next stage and that stop is
re-measured into a new row by the builder (expected: S7, where the story holds no `qa-failure-analyst@S7` stub row). The
pin stays 1. `test_field_producers.py` "the red rows of the walk are exactly the ledger" follows.

**Designer / plan critic:** the move touches 3+ package files plus tests, so it crosses the designer threshold (CLAUDE.md
rule 2): a designer card, or a `dispatch_skipped` with a reason. It **changes a meaning**: what the person's `go on` on the
stand does to the manual half. So PROJECT.md "package change" item 6 applies: a plan-critic pass on the card before the
builder. It does **not** change what S6 hands on in shape: the same `manual_skipped` lane, the same `refuse_case` writer,
the same `manual_close` site and receipt. The S7 inputs are unchanged in form. Whether to run the plan critic as a short
pass is the Lead's decision.

### Q4. Keying the two S6 dispatches in the story's `stub` table

Key on the **half**, by the existing field `execution_kind` of the dispatch record (`manual` / `automation`). It is read
through the controller's one reader `Controller._record_kind(dispatch)` (`scripts/controller.py:3991-3993`: the committed
request's `execution_kind`, then the record's own field). Do **not** key on the dispatch id. Ids are not stable for a half:

- `walk_next_id` and the walk reservations pick manual ids (`driver_stage_s6.py:1771-1779`, `:17-25`);
- the automation id is `-1` only because it happens to go first;
- a freshness close or a second life of S6 renumbers them.

The grammar: `qa-runner@S6#automation` and `qa-runner@S6#manual`. This widens `STUB_KEY` (`dry_stub.py:749`, today
`#[0-9]` only) to the two half words. `window_of` gets its S6 answer from the dispatch record, not from the brief's prose
(FR-12). A dispatch whose kind is empty (legacy) reads as automation, the way `stage_S6:493` reads it. The guard that keeps
the stub from guessing: when a `#<half>` row exists for (role, stage), the plain `<role>@<stage>` row must not answer
another half. Simplest form: the story moves its row under `#automation` and keeps no plain `qa-runner@S6`. A manual
dispatch with no `#manual` row then gets no form or digest values, which shows up as a `live_only` row, not another half's
text.

With the Q3 move, dry-1 has no manual dispatch at all. The key is still owed now, because the row added by 5979acb4
answers ANY S6 qa-runner dispatch (finding J2-1 below).

## Job 2 — verdict on diff `origin/main...5979acb4`

Files: `scripts/tests/dry_stub.py` (+50), `fixtures/stories/dry-1/story.json` (+40),
`fixtures/driver-exits/known_red.json` (row rewritten), `changelog.d/dry-stub-s6-runner.md`, and the report.

**Values backed by the story's data (checked one by one):**

- `run.environment: "dry-world"` is the `--environment` the dry runner's registered probe is called with
  (`fixtures/stories/dry-1/runners/python-pytest/runner.json:6`), so the probe record says it. Not invented.
- `inputs_read[2].path` / `run.probe_before` / `run.probe_after` = the newest `evidence/runtime-provenance-*.json`. This is
  the same reading the product's own manual form writer makes: `driver_dispatch.walk_run_values` (`:1580`, `:1585`,
  `:1589`) takes `sorted(...)[-1]` and writes the same value for before and after. Consistent.
- `run.application_build: "not established: ..."` is an honest gap.
- `scope[0]` TC-1 `passed_green` / `reused` matches the S5 run that stands.
- The lists set to `[]` / `$absent` remove filler junk rather than claim anything.

Nothing was invented to pass a gate.

**Findings:**

- **J2-1 (NEEDS WORK, fix of this round): the stub answers a dispatch its row was not written for.** The row is keyed
  plain `qa-runner@S6` (`story.json:74`). `stub_control` (`dry_stub.py:764-772`) returns it for EVERY qa-runner dispatch at
  S6. So for `S6-qa-runner-2` (manual, scope TC-2) the stub hands back the digest `qa-runner S6 S6-qa-runner-1 · ok / TC-1
  · green ...` and form overrides `header.window: TC-1`, `scope[0].id: TC-1`, `tried[0]` "TC-2 is not in this window". That
  is a role naming another dispatch and a case outside its scope, which no real role may write. The builder's own report
  says so (§3, "the digest of dispatch 2 repeats the TC-1 line") and calls it moot. It is not moot: it makes up part of the
  refusal text quoted in `known_red.json` (*"TC-2 was in this dispatch's scope and has no line"*). The ledger row therefore
  mixes a stub-made refusal with the product's.
  - Fix: key the row by half (Q4: `qa-runner@S6#automation`, read through `Controller._record_kind`), plus one selftest row
    showing that a manual S6 dispatch gets no values from the automation row.
  - If the Lead prefers not to widen the grammar this round, the smallest honest form is a `KitError` when the dispatch's
    scope (controller record `scope`) does not equal the row's `header.window`. Never a silent answer.
- **J2-2 (NEEDS WORK, fix of this round): the `main/S6` label is not accurate in two places.**
  - (i) It says "classified (b), not a stub gap". By this diagnosis the stop is a PRODUCT DEFECT (Q2 (a)), and part of the
    quoted refusal is the stub's (J2-1).
  - (ii) `raised_by` opens with "Lead t-1098". t-1098 is the builder's task, and no Lead word classified this stop. Axis 18
    admits a row only with a `raised_by` naming a critic verdict path or a Lead word.
  - Fix: `raised_by` names this verdict
    (`docs/tasks/specs/reviews/t-1106-dry-s6-manual-half-diagnosis.md`), states the product defect of Q2 (a), and the
    `node` points to the product node the Lead opens for Q3 (the Lead's decision; FV3-20 stays only if the Lead says so).
    The measured facts in the row (S6-qa-runner-1 accepted, the stop at S6-qa-runner-2, `exit_limit`, the after.json
    words) are true and stay. My re-run confirms them; see the trail.
- **Selftest rows can fail. Checked by reading each assertion:**
  - the resolution row is `check_eq` against a literal dict (mtime order is forced by `os.utime(..., (1, 1))`);
  - the three KitError rows check `startswith("k: override `f.x`")`, so a non-raise gives "no error" and the row goes red;
  - the digest row runs the product's `role_digest.check` and expects `[]`;
  - the fill row asserts specific values.

  An `Unfillable` inside the last row would crash the selftest rather than print FAIL. That is still red (exit != 0), so it
  is acceptable. The builder's negative control (removing `inputs_read[0].path` → E10 Unfillable) was run on the
  form/gate pair, not on the selftest file, but it exercises the same `fill_handover` call. My re-run: 240/240.

**Standing questions:**

- DUPLICATION AND CONSISTENCY: none blocking. Grepped `runtime-provenance` across `scripts/*.py`. The product picks the
  newest by name (`walk_run_values:1580`); `resolve_newest` picks by mtime, then name. The names carry the stamp, so the
  two agree. A shared reader is not required for a test double.
- CODE QUALITY: none found. `resolve_newest` is 15 lines with one closure and named KitErrors; the `pick` closure binds
  `path` by default argument, which is correct.
- ONE ROAD (P31): the diff adds no exclusion of a language, project or case. The product side of the class is in Q1 (one
  carrier, a missing reader).
- TESTS (TESTING.md «Бюджет»): about 27 test lines against about 21 code lines plus 40 lines of story data, so within the
  volume rule and no `tests-over:` owed. The three bad-glob cases are one parameterised table, not a battery.
- IN-TREE RATCHETS: `known_red.json` row `main/S6` is rewritten in place, `pins.known_red` stays 1, no new row, no raise.
  Its label is J2-2.
- ARCHITECTURE: the diff is in the test area only; "AR-n: none (test double)" holds. The Q3 move touches AR-24 and AR-25
  and must name them.
- Hygiene: changelog fragment present, ASCII; `selftest --lang` is in the witness.

**Class completeness (SIBLING_MAP):**

- Axis 26 (the word `stand not confirmed`) is the map axis of the Q2 defect. Its listed readers are `stand_check`,
  `s6_no_stand`, `check_delivery.stand_word` and `_take_stand_answer`. The manual half is the uncovered consumer, and Q3
  item 3 adds it to the axis.
- Axis 5 (stage twins): S5 has no manual half. Its `go on` text is the same site as S6's (Q3 item 2), so it is covered by
  the same edit.
- The stub-key class (J2-1): the builder's own analog note (S7 triage with several windows) is the same class. The key
  grammar in Q4 is per half, and S7 windows would need their own word when their rows are written. That belongs to the
  node that adds S7 stub rows.

## Verdict

- **Job 1:** PRODUCT DEFECT in `manual_lane_plan` (a missing no-stand reader). One builder move as in Q3, after a designer
  card and a plan-critic pass (Lead's decision).
- **Job 2:** NEEDS WORK, 2 findings (J2-1 stub key, J2-2 ledger label), both fixes of this round on the same branch.
  The values are backed by data, the selftest rows can fail, and the witness re-ran.

Accepting the work, and opening the product node, is the coordinator's decision, not this review's.

## Trail

- Read in the tree:
  - `scripts/driver_stage_s6.py` 20-90, 480-880, 880-1060, 1249-1338, 1566-1610, 1737-1905;
  - `scripts/driver_stage_build.py` 100-206, 290-330;
  - `scripts/driver_dispatch.py` 1152-1230, 1365-1510, 1570-1590;
  - `scripts/driver_dialog.py` 220-242;
  - `scripts/manual_evidence.py` 1476-1510, 1810-1870;
  - `scripts/manual_capture.py` (grep of the stand / env_blocked lines);
  - `scripts/validate_artifacts.py` 2092-2162;
  - `scripts/controller.py` 3985-3993 (+ grep of `execution_kind`);
  - `scripts/stand_gaps.py` 148-160;
  - `skills/qa-story/phases/s6.md` (whole);
  - `agents/qa-runner.md` and `references/manual-evidence.md` (grep);
  - `handoffs/s6-runner-to-analyst.yaml` 53-57;
  - `references/question-prices.json` (`s6.stand_confirm`);
  - `design/factory-rules.md` FR-36; `design/architecture.md` AR-25;
  - `scripts/tests/dry_stub.py` 410-440, 740-790;
  - `fixtures/stories/dry-1/kit.json`, `story.json` (walk);
  - `scripts/tests/test_story_run_s6.py` (grep, K4 row 2450-2467).
- Read in the forge: `docs/SIBLING_MAP.md` axis 26 (+ heading grep), `DECISIONS.md` (grep "stand", 4 hits; D-0047),
  `docs/tasks/critic-diff-brief.md` 80-91, `docs/TESTING.md` «Бюджет».
- The diff `git -C <tree> diff origin/main...5979acb4`, whole.
- Negative-claim checks:
  - "the manual half never reads `no_stand`": grep of `no_stand` in `driver_stage_s6.py` lists `:519, 536, 556, 565, 585,
    587, 672-859` and nothing in `:1304-1336` or `:1566-1605`;
  - "no decision keeps manual walking with no stand": grep of `DECISIONS.md` / `DECISIONS_ARCHIVE.md` for "stand not
    confirmed|without a stand|no stand" is empty, with positive control `grep -c -i stand` = 4 / 24, and
    `role-rules.json:330/332` found by the same grep form.
- Re-runs: see the json block. The main-pass re-run reproduces the builder's stop verbatim in its head, and its stub journal line `S6-qa-runner-2 n=1 ... wrote=1 ... work/handoffs/S6-qa-runner-2.yaml` is direct evidence for J2-1: the automation row filled the manual dispatch's form.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "fixes": [
    "J2-1: story.json row qa-runner@S6 answers every S6 qa-runner dispatch (stub_control, dry_stub.py:764-772), so the manual dispatch S6-qa-runner-2 gets the automation digest and TC-1 form rows; key it by half (qa-runner@S6#automation via Controller._record_kind, widen STUB_KEY) or KitError on a scope mismatch, plus one selftest row",
    "J2-2: known_red.json main/S6 label: re-classify from (b) to the product defect of this verdict (manual_lane_plan reads no s6_no_stand), note the stub-made part of the quoted refusal, raised_by names this verdict path instead of 'Lead t-1098', node per the Lead"
  ],
  "class_completeness": "Q2 defect: SIBLING_MAP axis 26 (the word stand not confirmed) - the manual half is the uncovered reader; Q3 item 3 adds it to the axis; axis 5: S5 has no manual half, its go-on text shares the one site of Q3 item 2. Stub-key class (J2-1): S7 multi-window rows are the same class, owed by the node that writes S7 stub rows.",
  "trail": {
    "read": [
      "ai-packages/qa-factory/scripts/driver_stage_s6.py",
      "ai-packages/qa-factory/scripts/driver_stage_build.py",
      "ai-packages/qa-factory/scripts/driver_dispatch.py",
      "ai-packages/qa-factory/scripts/driver_dialog.py",
      "ai-packages/qa-factory/scripts/manual_evidence.py",
      "ai-packages/qa-factory/scripts/manual_capture.py",
      "ai-packages/qa-factory/scripts/validate_artifacts.py",
      "ai-packages/qa-factory/scripts/controller.py",
      "ai-packages/qa-factory/scripts/stand_gaps.py",
      "ai-packages/qa-factory/skills/qa-story/phases/s6.md",
      "ai-packages/qa-factory/agents/qa-runner.md",
      "ai-packages/qa-factory/references/manual-evidence.md",
      "ai-packages/qa-factory/handoffs/s6-runner-to-analyst.yaml",
      "ai-packages/qa-factory/references/question-prices.json",
      "ai-packages/qa-factory/design/factory-rules.md",
      "ai-packages/qa-factory/design/architecture.md",
      "ai-packages/qa-factory/scripts/tests/dry_stub.py",
      "ai-packages/qa-factory/scripts/tests/fixtures/stories/dry-1/kit.json",
      "ai-packages/qa-factory/scripts/tests/fixtures/stories/dry-1/story.json",
      "ai-packages/qa-factory/scripts/tests/test_story_run_s6.py",
      "docs/SIBLING_MAP.md",
      "DECISIONS.md",
      "docs/tasks/critic-diff-brief.md",
      "docs/TESTING.md",
      "git diff origin/main...5979acb4"
    ],
    "reruns": [
      {
        "command": "python -B <tree>/ai-packages/qa-factory/scripts/tests/dry_stub.py --selftest",
        "result": "=== dry_stub --selftest: 240/240 ok === (70 s)"
      },
      {
        "command": "python -B <tree>/ai-packages/qa-factory/scripts/tests/test_scenario_dry_1.py --part main",
        "result": "PASS S0..S5, gate_A; NOTE known red: main/S6 -> FV3-20; NOTE stop: stopped at S6: no answer for exit_limit at S6 ... run-report.json: TC-2 is manual-agent ... appears in no lane; stub-call S6-qa-runner-2 n=1 wrote=1 (work/handoffs/S6-qa-runner-2.yaml, from the automation row: confirms J2-1); === scenario dry-1: 7/7 ok === rc 0 (395 s)"
      }
    ]
  }
}
```
