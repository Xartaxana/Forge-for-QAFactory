# t-1209 — critic re-review: FV3-22 card r2 against the five blocking findings of t-1195

Reviewed: `docs/tasks/specs/20261117-fv3-21c-skill-road-s6-close-card-r2.md` (§0-§13 and the Lead decisions on the r2 forks, read
by sections), against `docs/tasks/specs/reviews/t-1195-fv3-22-card-plan.md`. Code facts were spot-checked in the FV3-21 worktree
`.claude/worktrees/agent-af279738b46568113` (HEAD 80923ed2 plus the uncommitted t-1186 round). That worktree MOVED while this
review ran: see F5. Scope as dispatched: the five blockers, the Lead decisions, the 11 fixes by the §10 table only, and new defects
only if they block.

**Verdict: NEEDS WORK (fit_with_fixes). 1 blocking finding: F4 is fixed wrongly. F1, F2, F3 fixed. F5 fixed as an instruction, but
t-1186 has already overtaken three of its facts, so it needs amending before dispatch.** The F4 defect comes from my own t-1195
recommendation ("if the pipeline's S6 record is done"). r2 carried it over faithfully, so the fault is in the verdict, not in the
designer's work.

## 1. Per blocking finding

### F1 — Lead F3 = (a) not carried: FIXED

- What r2 now has:
  - K5.k (`story_progress._awaits_position`);
  - `story_progress.py` in §0.2 `owns:`, and node -1's non-goals pass it to FV3-22-2;
  - CK8, the edges E-P1..E-P7 and the rows P1-P5.
- Spot check: `acceptance.awaits_acceptance(state, stage, pipeline=None, table=None)` (WT `acceptance.py:1472`) reads the
  `acceptance_awaits` marker only when `pipeline` is passed (:1497-1498). K5.k passes the pipeline. It returns `""` on a completed
  stage (:1484-1485), which matches E-P6/P5.

### F2 — the live gate checked only `running`: FIXED

- What r2 now has:
  - K5.e step 4 calls `live_s6_scopes(state)`;
  - E4 names running, blocked and paused;
  - rows C11, C11b (paused) and C11c (blocked);
  - probe P3 (a running-only filter turns C11b red).
- Spot check: the predicate counts `("running", "blocked", "paused")`. That holds at both of its WT homes, `driver_stage_s6.py:18-25`
  first and now `controller.py:690-697`.

### F3 — `BY_PERSON` / `_sha` from `driver_core`: FIXED

- What r2 now has:
  - the `BY_PERSON` row in the §2.1 table;
  - K5.b and K5.l (`driver_core.py:411` deleted, `driver-layers.json:82` row deleted);
  - E-M3;
  - `code_only_request` hashes inline in the controller's own form (E-M5), and `_sha` stays for `driver_dispatch.py:2484`.
- Spot check: a whole-word `grep -rnw BY_PERSON` over WT `scripts/` finds exactly `driver_core.py:411`,
  `driver_stage_s6.py:13, 213, 318` and `driver-layers.json:82`. `driver_stage_s6` really is the only importer. A family part
  importing a non-family module is the existing `waiver` precedent.
- r2 departs from my recommendation: `driver_stage_s6` imports `BY_PERSON` directly and there is no re-export from `driver_core`
  (§13). I accept that: it leaves one definition and no stale row.

### F4 — re-entry after the close: FIXED WRONGLY (blocking)

**F4-1. Step 1b's discriminator cannot tell the E9 world from a recorded close.** K5.e step 1b and §2.4 decide "record done" by
`controller._pipeline_stage_statuses().get("S6") == "done"`. But the controller writes that status itself on every apply:
- `_project_pipeline` (WT `controller.py:4885-4935`) runs inside every write (`:4960`, "pipeline.json is written FIRST").
- For each controller stage it sets `entry["status"] = {"completed": "done"}.get(...)` (`:4927`).
- The `code_only` reducer sets S6 to `{"status": "completed", "code_only": True, "reason", "receipt_id"}` (`:1949-1951`).
- So once the receipt exists, pipeline.json's S6 status is `"done"` whether or not `stage_done --status done` ever ran.
- The test world projects too: `real_story` initializes with `source_revision: "src-1"` (WT `test_story_step_manual_block.py:55`),
  and `_project_pipeline` returns early only without it (`:4889`).

The concrete failure is row C9b as the card writes it:
1. The first `start` writes the receipt. The fake `stage_done.py` returns `(1, "refused")`, so the first start exits 2 with the door.
2. The second `start` reaches step 1b. The controller holds S6 `completed` and the pipeline status reads `"done"` (projected), so it
   returns `("done", ["S6 is completed already: nothing is closed again", next where], 0, {})`.
3. Result: exit 0. The stage record (`stage_done.apply_stage`: `finished`, `digest`, `role`, halts resolved, `stage_done.py:801-838`)
   was never written. This is the same false success as t-1195 F4b, only under a different line.
4. E14b is unreachable, and C9b is red against the card's own design. The builder would either STOP or bend the test.

C9 passes only by accident: its fake `stage_done.py` writes nothing, and the projection supplies the `"done"`.

**Fix (in this round):** decide "record written" by a field that only `stage_done` writes and the projection never touches. One
example: S6 `finished` in pipeline.json. `stage_done.py:815-816` writes it on done. It is not in `STAGE_RUN_MARKS`
(`controller.py:1095`) and the projection never sets it. Two conditions apply:
- read it through one named reader, not an inline `json.loads`;
- the card states which earlier write could leave a stale `finished` (an S6 done before a rework), and what then happens.
State the field in §2.4 and step 1b. Make C9's fake `stage_done.py --status done` write the record (or call the real script) so that
C9 is a true positive, and keep C9b as written: it then goes red without the fix. The P4 probe holds.

**F4-2. Step 1b's literal expression crashes in existing green worlds (fix, same item).** It reads
`controller.state()["stages"]["S6"]["status"]`, but:
- `initialize` leaves `stages` empty (`controller.py:1620`; the `initialize` reducer at `:1631-1642` adds only a legacy import);
- an S6 entry appears only once an S6 event exists;
- step 1b runs before steps 2-5, at every X1-X3 call.

So C5 and the existing rows "no automation runner -> E1" (K-R3..K-R5, FV3-21b S1-S10, §5 last paragraph) raise `KeyError` before
they reach E1. **Fix:** write it as a `.get` chain. A missing S6 entry reads as not completed.

The rest of F4 holds:
- The E9 door's digest reads `stages.S6.reason`, which the reducer writes (`:1951`), with a placeholder when it is absent.
- C9 asserts that `finalize_task.py` runs only once.

### F5 — the t-1186 overlap: FIXED as an instruction; facts overtaken, amend before dispatch

r2 §0 is a correct merge instruction:
- start from `origin/main` after the FV3-21 wave merges;
- re-read MF1-MF7 on the merged head;
- a line shift is only reported; any other difference means STOP.

F5 (a)-(d) are each answered:
- (a) `mark_awaiting`, E-M8;
- (b) X2 `spent` comes from `_no_stand_cases`, never from text: E17, C14;
- (c) K5.l, E-M4;
- (d) every line number is marked WT.

But while this review ran, t-1186 moved the code again (WT `git diff --stat` now also touches `controller.py` and
`driver-layers.json`):
- `live_s6_scopes` now lives in `controller.py:690`. `driver_stage_s6.py:10` and `story_step.py:105` import it from `controller`,
  and the `_no_stand_refusal` docstring (`story_step.py:1083`) names `controller.live_s6_scopes`. MF1 and MF2 no longer hold.
- `driver-layers.json` gained the row `Driver.consumer_await` (home `driver_stage_s6`, "FV3-21 F7"). MF4's statement "the WT has no
  row for ... `Driver.consumer_await`" no longer holds.

The STOP clause makes this safe, but as written node -1 is certain to STOP at its first step. The new home also settles F5(c)
better than r2 does: `controller` is not part of the driver family, so the L11 concern is gone, and `stage_close` already imports
`controller` inside its functions.

**Fix (Lead edit before the node -1 dispatch; final once t-1186 is accepted):** rewrite MF1, MF2 and MF4 to the accepted state.
Then:
- drop the move of `live_s6_scopes` from the §2.1 table, K5.a, K5.b, K5.l and E-M4. `stage_close`, `story_step` and step 4 call
  `controller.live_s6_scopes`;
- change the AR-13 DoD grep to "`def live_s6_scopes` exactly 1 hit, in `controller.py`";
- K5.l keeps the `consumer_await` row, whose note gains "delegate of `stage_close.mark_awaiting`", and adds no row.

If t-1186 ends somewhere else, the MF re-read still catches it.

## 2. Lead decisions at the end of r2

- **R2-F1** = one node, two task_ids: agree. No batch rows are needed, so the unread TEAMWORK §2 question does not arise.
- **R2-F2** = A27 reach left as a named residual: acceptable for this dispatch, because node -1's grep covers today's
  `stage_close.py`. But the residual has no node and no executor. CLAUDE.md rule 9 and PROJECT.md «Командная работа» p. 9 let a
  sibling leave the round only as a node with an executor. **Fix:** a node, with its owner and executor, for widening A27 to
  `stage_close.py` / `road.py`. The coordinator of the proper tier opens it (rule 6).
- **R2-F3** = FV3-26: agree. The row exists at `batch-3-live-run-fvf.md:55` with an executor chain and owns.
- **Order** (re-review first, FV3-22-1 after the FV3-21 merge): agree, subject to the F5 amendment.
- §11 "no second plan pass needed": r2 adds homes, not architecture. The F4 fix above changes one predicate and one test world, so a
  Lead check is enough. No further critic pass is needed, per PROJECT.md new-idea step 6.

## 3. The 11 non-blocking fixes (present / absent, by the §10 table)

| item | r2 |
|---|---|
| m1 stub invariant, `manual_request_paths` | present (§2.1 INVARIANT, road members, E-M6) |
| m2 one return shape | present (K5.e 4-tuple, E22) |
| m3 census name | present (`_no_stand_cases`, §1.4 list) |
| m4 print order | present (§2.3 capture, E20, C1 order) |
| m5 the person's-word door | present (`person_word_door`, E21, K5.i; plus E-M2) |
| m6 node ids, covers edit in node -1 | present (§0.1/§0.2, R2-F1, K5.m) |
| m7 A27 reach | present as fork R2-F2 (see §2: a node is owed) |
| axis 26 | present (K5.j, §0.2 siblings) |
| test lines in the DoD | present (§0.1/§0.2 «Test lines», timing tail) |
| positional FB-9 note | present (K5.f, E18, C6) |
| FV3-24 row text | present in r2 as a §7 «Lead action», NOT yet carried out: `batch-3-live-run-fvf.md:53` still names only the re-proof and Q-a3. This is a Lead edit, outside the card |

## 4. Standing questions (scope: the r2 delta)

- **DUPLICATION AND CONSISTENCY:**
  - F5: with t-1186's controller home, a further move to `stage_close` would add churn but no second definition. Adopt the
    controller home.
  - F4-1 must read the record field through one reader.
  - Otherwise none found. Grepped: `BY_PERSON` (whole word), `live_s6_scopes`, `_pipeline_stage_statuses`, `STAGE_RUN_MARKS`.
- **CODE QUALITY:** F4-2 (a literal `[...]` chain on an optional key). Otherwise none found in the r2 delta.
- **ONE ROAD (P31/Q12):** unchanged from t-1195. The close is shared, and FV3-24 and FV3-26 are nodes with executors. No exclusion
  found.
- **TESTS (Q5):** 22 rows in two functions. The volume reason is stated (new behaviour on the skill road, per-edge rows). The C9 and
  C9b worlds need the F4-1 correction to test what they claim.

## 5. Class completeness

Axes 5, 26 and 34 are covered as in t-1195: K5.j, FV3-24 and FV3-26. Analog, not widened and not blocking here: the driver's own
`close_by_code` returns True on a `completed` stage without checking the stage record (WT `driver_stage_s7.py:772-775`). A fresh
driver process after a refused record, with no in-process `Refusal.retry`, would pass over the missing record in the same way.
Whether to open a node for it is the Lead's decision.

## 6. Trail

- Read: r2 §0-§13 and the Lead decisions on the r2 forks (by sections, whole); t-1195 (whole).
- WT, read: `driver_stage_s6.py` 1-30 plus greps; `story_step.py` 1078-1108 plus greps; `controller.py` 685-697, 1095-1101,
  1620, 1631-1644, 1945-1960, 4885-4935, 4950-4962, 6086-6110, 8800-8808; `stage_done.py` 790-845; `driver_stage_s7.py` 763-787;
  `acceptance.py` 1447-1509; `story_progress.py` import and def lines; `driver-layers.json` 1-9, :82 and the diff;
  `test_story_step_manual_block.py` 48-60.
- Main: `plans/piles/live-run-fvf/batch-3-live-run-fvf.md` rows FV3-22, FV3-24, FV3-26.
- Greps, with their controls:
  - `-rnw BY_PERSON` over WT `scripts/`: 5 hits. Control: the definition line itself.
  - `live_s6_scopes` over WT `scripts/*.py`: first run 3 files with the `driver_stage_s6` home; second run the `controller` home.
    That is how the move was detected.
  - `_project_pipeline(`: the definition plus 1 call.
  - `git -C <WT> diff --stat`: 9 files, including `controller.py` and `driver-layers.json`.
- No test runs: this is a plan re-review, so there is no mechanical layer.

The decisions on these findings belong to the Lead (rule 6).

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "F4 fixed wrongly: step 1b and section 2.4 judge the stage record by pipeline S6 status == done, but the controller projects completed -> done into pipeline.json on every apply (controller.py:4927, called at :4960), so after the code_only receipt the status is always done; the E9 world then prints S6 is completed already, exit 0, with the stage_done record never written (the t-1195 F4b false success again); E14b is unreachable and C9b is red against the card's own design"
  ],
  "fixes": [
    "F4-1: judge the record by a field only stage_done writes (e.g. pipeline S6 finished, stage_done.py:815-816, not in STAGE_RUN_MARKS, never projected) through one reader; name the stale-finished case; C9's fake stage_done --status done writes the record (or the real script runs) so C9 is a true positive; C9b unchanged",
    "F4-2: step 1b reads the S6 status with a .get chain; a missing S6 entry (initialize leaves stages empty, controller.py:1620) reads as not completed, else C5 and the existing no-automation-runner rows raise KeyError",
    "F5: t-1186 moved live_s6_scopes to controller.py:690 (imported by driver_stage_s6.py:10 and story_step.py:105) and added the Driver.consumer_await layer row; rewrite MF1, MF2, MF4 to the accepted t-1186 state, drop the live_s6_scopes move (section 2.1 table, K5.a, K5.b, K5.l, E-M4), call controller.live_s6_scopes, AR-13 grep = 1 def in controller.py, K5.l keeps the consumer_await row with an updated note",
    "R2-F2: the A27 reach residual gets a node with owner and executor (rule 9 / PROJECT p.9), opened by the proper-tier coordinator",
    "FV3-24 row text (section 7 Lead action) is not yet applied at batch-3-live-run-fvf.md:53"
  ],
  "class_completeness": "axes 5, 26, 34 covered as in t-1195 (K5.j; FV3-24; FV3-26 at batch-3 row 55); in-artifact: F4 discriminator defect also affects C9 (passes by accident) and E14b; analog noted, not widened: driver close_by_code returns True on a completed stage without checking the stage record (driver_stage_s7.py:772-775) - node is the Lead's call",
  "trail": {
    "read": [
      "docs/tasks/specs/20261117-fv3-21c-skill-road-s6-close-card-r2.md (all sections)",
      "docs/tasks/specs/reviews/t-1195-fv3-22-card-plan.md",
      "WT ai-packages/qa-factory/scripts/controller.py 685-697,1095-1101,1620,1631-1644,1945-1960,4885-4935,4950-4962,6086-6110,8800-8808",
      "WT ai-packages/qa-factory/scripts/stage_done.py 790-845",
      "WT ai-packages/qa-factory/scripts/driver_stage_s7.py 763-787",
      "WT ai-packages/qa-factory/scripts/acceptance.py 1447-1509",
      "WT ai-packages/qa-factory/scripts/driver_stage_s6.py 1-30 + greps",
      "WT ai-packages/qa-factory/scripts/story_step.py 1078-1108 + greps",
      "WT ai-packages/qa-factory/scripts/story_progress.py import/def lines",
      "WT ai-packages/qa-factory/scripts/tests/fixtures/driver-layers.json 1-9, row 82, diff",
      "WT ai-packages/qa-factory/scripts/tests/test_story_step_manual_block.py 48-60",
      "plans/piles/live-run-fvf/batch-3-live-run-fvf.md rows FV3-22, FV3-24, FV3-26"
    ],
    "reruns": []
  }
}
```
