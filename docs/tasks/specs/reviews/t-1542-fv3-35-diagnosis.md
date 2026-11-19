# t-1542 critic: diagnosis of FV3-35 (dry-story pile, s5 group, 24 rows)

Tree: `C:/QAFactory/forge-repo`, main at e0ba1ffa (= origin/main, checked with `git rev-parse origin/main`). No repo file was
changed: `git status --porcelain -- ai-packages/` printed nothing after the three runs. Scratch files are only in
`C:/Users/i_mas/AppData/Local/Temp/t1542/`.

**Summary.** The row names two causes. Both are real, but they are not the causes the row assumes, and they do not hit the
same rows. Measured on three families:

| family | rows | measured stop | cause | fix layer |
|---|---|---|---|---|
| A `s5.nobody_{review,environment,tooling}/*` | 14 | conductor at S5 (same as B) | **cause (2) only.** The critic form says `cause: test_defect`, so the route never gives `nobody`. With a per-family cause override, all 3 sampled rows **PASS**, with the product unchanged | fixture (exits/s5.json) |
| B `s5.repair_limit/*` | 4 | conductor at S5 | **product defect.** On the serial road, a critic that sends the LAST (here the only) S5 window back finishes with a bare `--not-complete`. The controller refuses that ("leaves S5 with no role to close it"), and the driver has no move for the refusal. The author round never runs, so the cap is never reached | product (driver S5) |
| C `exit.resume_limit*/*` | 6 | conductor at S5, on `dead_dispatch -> recover -> resolve_return` | **product road, root not pinned.** After three resumes of the automator, re-entering the dispatch finds "no result and no question" and goes to recovery. It never goes to the `exit_limit` seam | trace first, then a product node |

So the class-1 stub did not "fail to fire". It fired exactly as written: the critic rejected and the product refused its
finish. The row text "заглушка critic-reject класса 1 не сработала" is wrong about the layer.

## (a) Measured cause per family

How the conductor's words were made visible: no debug env var exists (grep `environ` in dry_*.py: only `DRY_STUB_CONTROL`,
`CLAUDE_PROJECT_DIR`, `STORY_RUN_CLASS`). I used a scratch wrapper, `Temp/t1542/probe.py`. It imports
`test_scenario_dry_1` from the repo and wraps `dry_world.run_seed`. When the seed is not reached, it prints the pending ask,
`_details_text(copy, 6000)` (the reader the main pass already uses at `dry_world.py:944-947`), `driver-question.md`, the
tails of `dry-stub.jsonl`, `driver-questions.jsonl` and `dry-routes.jsonl`, and the last 60 lines the driver printed. The
exits-root is a scratch copy of `exits/s5.json` filtered to the sampled rows, plus the real `seeds/s5.json`. `--ledger` points
at an absent file (an empty ledger), so the rows print FAIL text instead of "known red".

Commands (each from a `( cd ai-packages/qa-factory && ... )` subshell):
- run1: `python -B Temp/t1542/probe.py --part exits:s5 --exits-root Temp/t1542/root --ledger Temp/t1542/none.json`. Rows:
  s5.repair_limit/debt, s5.nobody_review/review, s5.nobody_environment/fixed, exit.resume_limit/stop,
  exit.resume_limit_halted/stop. Prefix to S4 in 110.2 s, then `1/11 ok`, exit 1, and all 5 rows FAIL with "met the
  conductor at S5" (log lines 581-585, the same text as CI run 44205734909).
- run2: `Temp/t1542/probe2.py`, the same with row s5.nobody_environment/fixed. It reads the critic's form from the copy and
  routes it with `repair_route.route`.
- run3: `probe.py` with root3. The 3 nobody rows, each with ONE override added: `findings[].cause` = environment /
  reviewer_error / tooling.

### Family B (and A as it stands today): the critic's finish is refused

The conductor's own words, verbatim from `state/driver-question-details.md` (the same for the repair_limit, nobody_review and
nobody_environment rows):

```
story_step finish S5-qa-code-critic-1 (exit 2): story_step: refused - accepting S5-qa-code-critic-1 with stage_complete:
false leaves S5 with no role to close it — pass stage_complete: true, name the unresolved work with its reason, or checkpoint
the dispatch if the work is not done (`controller.py ... --operation checkpoint --dispatch S5-qa-code-critic-1 --status
incomplete --reason "<what is left>" --brief`)
```

Driver output tail, run1 row s5.repair_limit/debt (19 lines):
```
answer for environment (S5): go on
S5: going on on the person's word; recorded
S5: stand not confirmed: no stand is confirmed for this story - passed by the person's word "go on"; ...
[S5] qa-automator → S5-qa-automator-1 scope=TC-1
witness OK (re-run by the exit gate): automation-manifest.json - the orchestrator needs no second run
accepted S5-qa-automator-1: 2 evidence files, stage open - next role of this stage
[S5] qa-code-critic → S5-qa-code-critic-1 scope=TC-1
witness OK (re-run by the exit gate): automation-manifest.json - the orchestrator needs no second run
S5 window TC-1: refusal round 1 of 2 goes to the conductor - the refusal is not about the window's tests; the window's own rounds stay 0 of 2
conductor: ask_person — stub: offered every open move
PENDING ASK: {"kind": "conductor", "stage": "S5", "dispatch": "S5-qa-code-critic-1", "why": "refusal", "offered": ["restart", "go on", "retry", "stop"], ...}
TAIL dry-routes.jsonl: (empty: no known route matched)
```

The trace in code:
- `driver_stage_s5.py:458-468` (`s5_review.closes`): returns a **bool**. For a blocking `test_defect` under the cap, the route
  is `action: test_defect`, so `closes` is False.
- `driver_dispatch.py:839-848` (`finish`): `complete is False` gives `--not-complete`. `--open-windows` is added only on a
  chain AND when another window is open (`s5_open_flag`, :3023-3036, returns [] when there is none).
- `controller.py:6003-6011`: `stage_complete is False and not unresolved and "open_windows" not in p and _closes_stage`
  raises `StateConflict`. `_closes_stage` (:7788-7828) is True for the only window.
- `driver_machine.py:430-438` sends the refusal to the conductor ("refusal round 1 of 2"). `s5_author_round`
  (`driver_stage_s5.py:440-442`) is never reached, so `counted` never grows, and `cap` (and so `s5.repair_limit`) is
  unreachable.
- The sibling stages do have this move. S4 returns `OpenWork("cases_in_repair", ...)` (`driver_stage_plan.py:1036`), S2/S3
  return `OpenWork("stage_in_repair")` (:761), S6 `stage_superseded` (`driver_stage_s6.py:344`), S7 `repairs_pending`. The S5
  window critic is the one closing role whose send-back finish has no `OpenWork`. The tests confirm the gap and never hit it:
  `test_story_run_repair_limit.py:96-97` stubs the controller (`return 0, "{}"`), and the comment at :660 says it outright
  ("the real controller refuses a bare `--not-complete` accept of the stage's closing critic").
- This is a **live defect, not only a dry one**: the serial road is the same code in a live run, so every S5 send-back on the
  last window costs a conductor call and a person's question today.

### Family A: cause (2) confirmed, and it is the ONLY cause for these rows

run2 output (verbatim, 14 lines):
```
FORM findings section:
findings:
  - id: F-1
    ...
    cause: test_defect
    blocking: true
findings(): [{"id": "F-1", "problem": "filled problem", "cause": "test_defect", "blocking": true, ...}]
route(concerns, {'counted': 0, 'cap': 2} ) = {"action": "test_defect", "reason": "blocking test_defect finding", ..., "code": ""}
route(concerns, {'counted': 2, 'cap': 2} ) = {"action": "close", "reason": "cap reached", ..., "code": "cap"}
FAIL dry-1/exits:s5/s5.nobody_environment/fixed — seed did not reach s5.nobody_environment: met the conductor at S5: ...
=== scenario dry-1: 1/3 ok ===
```
So the stub can only ever give `cap` -> `s5.repair_limit` (`driver_dispatch.py:3304-3315`). That is t-1331 F2, now measured.

run3 tail (verbatim, the per-family `findings[].cause` override and nothing else changed):
```
NOTE dry-1/exits:s5/prefix: reached S4 in 153.2 s; snapshots S0, S1, S2, S3, S4
PASS dry-1/exits:s5/s5.nobody_review/review
PASS dry-1/exits:s5/s5.nobody_environment/fixed
PASS dry-1/exits:s5/s5.nobody_tooling/debt
PASS dry-1/exits:s5/outcomes
=== scenario dry-1: 4/4 ok ===
exit 0
```
Why cause (1) does not block family A: `repair_limit_gate` sits BEFORE `finish` (`driver_dispatch.py:784-787`, and
:3278-3280 raises the question). A `nobody` route asks the person on the critic's FIRST return, so the refused finish is never
reached. Not measured: the other 11 variants of family A (debt/stop/free words/empty). They share the seed and the stub and
differ only in the answer word, so the builder's run decides them.

### Family C: the resume ladder ends on recovery, not on the `exit_limit` seam

Details at the conductor stop (both rows, verbatim):
```
resolve_return: {"action": "resolve_return", "dispatch_id": "S5-qa-automator-1", "stage": "S5", "role": "qa-automator",
"dispatch_status": "returned_unaccepted", "digest": "", "options": ["accept", "checkpoint", "rework"],
"retry_reason": "subagent_silent", "reason": "recover: S5-qa-automator-1 was recorded as running but its role stopped
without acceptance — the driver recorded this dispatch's session as ended (exit 0) in state/driver-runs.jsonl"}
```
Driver output tail, run1 row exit.resume_limit/stop (13 lines):
```
[S5] qa-automator → S5-qa-automator-1 scope=TC-1
resume S5-qa-automator-1: the role's final message is not the handoff form (not assembled by code: the role's message says `ok` and its form says `concerns`: that is the role's to settle)
resume S5-qa-automator-1: still not repaired after one resume: the role's final message is not the handoff form
note: handoff took 20 s
refusal: known `marked_repair` → resume_repair
refusal: S5-qa-automator-1 is resumed in its own session with the refusal, once
[progress] S5 Automation · ... the automator returned 20:01, its dispatch still open
resume S5-qa-automator-1: the factory refused to close the dispatch: the role's final message is not the handoff form
[progress] S5 Automation · ... the automator returned 20:01, its dispatch still open
refusal: known `dead_dispatch` → recover
conductor: ask_person — stub: offered every open move
```
The halted row is the same, except that line 2 reads "the role's own message halts". So no halt road is taken: t-1331 N3's
risk did not happen. The stub journal shows 3 resumes (n=2,3,4). Each answers the same text and writes nothing, as the stub is
designed to (`dry_stub.py:1085-1088`).

The trace, as far as I read it:
1. `handoff_ladder` resumes once and once more as mechanical (`driver_dispatch.py:580-607`), then raises `Refusal`
   (:612-615).
2. `handle_refusal` routes it as `marked_repair` and spends a third resume, `resume_with` kind `refusal_resume`
   (`driver_machine.py:313-319`).
3. On re-entry the driver should judge that saved result again (`resume_with` docstring, `driver_dispatch.py:2311-2313`:
   "the loop comes back through `where` -> `wait_existing_job` -> `handoff` -> `finish`"). The same findings would then hit
   "already resumed" -> `exit_limit` (`driver_machine.py:325-332`, t-764 E8). Instead `_liveness_refusal`
   (`driver_machine.py:1556-1579`, "The driver holds no result and no question for it") fires. KNOWN_REFUSALS `dead_dispatch`
   (`driver_dispatch.py:108`) sends it to recover, then `_act_resolve_return` (`driver_machine.py:1666-1678`) has no filed
   words, and then the conductor.
- **Not measured: why the saved result is not seen on re-entry.** It may be `state/driver-runs/<dispatch>.json` absent or
  moved, or `where` choosing another branch first. This is a hypothesis only. The stub is not the fault: a live role that
  repeats its message would walk the same road.

## (b) Fix direction per family, with the DoD a builder would get

**A, fixture (14 rows; can land now, with no product change).**
- owns: `.../stories/dry-1/exits/s5.json` and `.../driver-exits/known_red/s5.json`.
- The edit: give each family its own stub override `findings[].cause` (environment / reviewer_error / tooling). This splits
  the 18 byte-identical copies (Q7 of t-1331). Remove the 14 rows from known_red and set `pins.known_red` 57 -> 43, each
  removal named.
- Edges:
  - A variant that reaches its key but fails a check stays labelled with its OWN measured FAIL text and a node. It is never
    left under FV3-35.
  - A cause outside `vocabulary.repair_causes` maps silently to `test_defect` (`repair_route.py:66`). The row's "seed did not
    reach" is the guard, so no new check is owed.
  - Row cap 240 s (`ROW_CAP_EXITS`): measured well inside it.
  - nobody_review: `reviewer_error` is measured (PASS). The `untyped` road (no findings row) is a second door to the same key
    and is unmeasured. This is fork d2.
- DoD: the canon job of the group (`test_scenario_dry_1.py --part exits:s5`; it is slow, so the batch canon judges it). The
  local witness is a scratch exits-root of the 14 rows, all PASS. `dry_exits.py --check`: 0 discrepancies.

**B, product node (4 rows, and live).**
- owns: `scripts/driver_stage_s5.py` (`s5_review.closes`, `s5_mechanical_round`'s complete), `scripts/driver_stage_plan.py`
  (`completion_for` S5 branch, the recovery twin), and a row in `scripts/tests/test_story_run_repair_limit.py` (the
  real-controller part, `rl2_real_controller`).
- The change: when the route owes the author a round (`test_defect` under the cap, a mechanical round owed), the closing
  critic's finish returns `OpenWork(<word>, open_work_reason(...))`, the same move as S4 `cases_in_repair`. Then `finish`
  sends `--not-complete --unresolved --reason`, which the controller accepts.
- Edges:
  - POSITION: `repair_limit_gate` stays BEFORE `finish`. A seam route (cap / nobody / untyped / unknown) is still asked, never
    closed in silence.
  - INVARIANT: the bare silent `--not-complete` on a truly last window is still refused
    (`test_s5_parallel_admission.py:427` stays green).
  - On a chain's non-last window `OpenWork` takes precedence over `--open-windows` (`finish` :841-843). State whether that is
    intended, or keep `open_windows` there.
  - The word must not be read as a window debt or an unresolved window by the S5/S8 readers. Grep the readers of a dispatch's
    `unresolved` and walk producer -> reader both ways (AR walk).
  - The recovery road (`_finish_saved_result` -> `completion_for`) gives the same `OpenWork`. Otherwise recovery still
    refuses.
- red-before: the real-controller row "critic sends back the only window -> author round dispatched, no conductor call" is red
  today with "no role to close it".
- DoD: that row, plus the dry rows `s5.repair_limit/*` PASS in a scratch exits-root run (cap 2 means 3 critic calls and 2
  author rounds; watch the 240 s row cap).

**C, trace first, then a product node (6 rows).**
- Step 1, a scout or critic diagnosis. One scratch run of `exit.resume_limit/stop` that prints, at every driver turn, whether
  `state/driver-runs/S5-qa-automator-1.json` exists, the controller's dispatch status and the `where` action. Question: why
  re-entry after a `refusal_resume` takes `_liveness_refusal` instead of `_finish_saved_result`.
- Step 2, a builder: the road must end at `exit.resume_limit` / `_halted` (t-764 E8: the one seam). The stub and the seeds stay
  as they are.

## (c) Overlap with the other rows

- **FV3-25** (pile :54; finding `plans/piles/live-run-fvf/findings/20261117-p1b-s5-fault-states-unreachable-in-dry-world.md`).
  It covers the SAME keys (repair_limit, nobody_*, resume_limit*, code_close.*). Its item 1 ("why the S5 critic reject does
  not reach repair_limit") is answered here (family B). Its item 2 (seed ops for fault states) is not needed for A (a stub
  cause) or B (a product fix). It may be needed for code_close (FV3-33). Full overlap: fork d1.
- **FV3-33** (code_close.*, 12 rows): a different mechanism. Those rows have no stub and pass S5 with the approving critic, so
  fix B does not touch them. The overlap is files only (`exits/s5.json`, `seeds/s5.json`, `known_red/s5.json`): merge them in
  series. If FV3-33 needs a seed `op` that refuses a stage close, that is FV3-25's grammar item. Do it once.
- **FV3-36** (S6 conditions, 21 rows): no overlap in mechanism. The rows start at S5 with a bare `drive_until` and the
  approving critic (`complete=True`), which fix B does not change. Files only.
- **FV3-28** names `s5.repair_limit/round|fixed` among the dropped answers. These become reachable only after B lands, so
  FV3-28 depends on B for those two.
- The main pass is not affected by A or B (its critic approves). B changes LIVE behaviour (one conductor call less per
  send-back), so a live proof row (FR-33) is owed in the live-runs pile.

## (d) Forks for the Lead

- d1. Is FV3-25 closed into FV3-35 (items 1-2 answered or not needed) plus FV3-33 (code_close)? Or does it stay as the
  seed-op grammar node for FV3-33?
- d2. nobody_review: the `reviewer_error` cause (measured), or the `untyped` road (no findings row; unmeasured), or both
  as separate rows?
- d3. Family B is a live product defect. Is it a node inside this dry pile (FV3-35 b), or a product node in its own pile with
  FV3-35 waiting on it? Which word: reuse `stage_in_repair` (one word with the S2/S3 road and `stage_repair_owed`, Q6), or an
  S5 word such as `tests_in_repair` (S4 keeps its own)?
- d4. Split FV3-35 into A (fixture, now), B (product) and C (trace, then product)? Rewrite the `raised_by` of the 24 rows to
  each family's measured cause (this report)?

## Trail

- Read: the pile row FV3-35 and rows FV3-7/20-28/33/36; t-1331 review (all); `known_red/s5.json` (24 FV3-35 rows listed);
  `known_red.json` main rows; `exits/s5.json` rows repair_limit/debt, nobody_review/review, resume_limit*/stop;
  `seeds/s5.json` :1-100; `test_scenario_dry_1.py` (all); `dry_driver.py` (all); `dry_world.py` :260-300, 388-420, 540-570,
  839-842, 930-960, 1115-1500; `dry_stub.py` :100-140, 1070-1125; `repair_route.py` :19-139; `driver_dispatch.py` :481-616,
  780-900, 3023-3036, 3170-3330, 3851-4040, 2290-2335; `driver_machine.py` :40-80, 285-470, 540-575, 1500-1580, 1655-1678;
  `driver_stage_s5.py` :420-500; `driver_stage_plan.py` :750-765, 1005-1040, 1215-1310; `controller.py` :100-111, 5960-6020,
  7295-7340, 7788-7828; `driver_core.py` :173-187; `s5-critic-to-automator.yaml` :55-100; the FV3-25 finding.
- Runs: run1 (5 rows, `1/11 ok`, exit 1), run2 (1 row plus the form route, `1/3 ok`), run3 (3 rows with the cause
  override, `4/4 ok`, exit 0). Logs: `Temp/t1542/run{1,2,3}.log`.
- Negative searches with a positive control: `environ` in dry_*.py found 9 hits, none of them a debug switch (the control is
  the same grep hitting `DRY_STUB_CONTROL`). "no role to close it" in references/data found 0, while the same grep over
  scripts/*.py found 5 files.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "fixes": [
    "D1: FV3-35's first cause is a product defect, not a stub miss: the serial-road S5 critic that sends the last window back finishes with a bare --not-complete (driver_stage_s5.py s5_review.closes returns bool; driver_dispatch.py:839-848), the controller refuses it (controller.py:6003-6011), and the driver has no move, so it goes to the conductor; 4 repair_limit rows wait on a product node (OpenWork as S4 cases_in_repair)",
    "D2: cause (2) is measured: the critic form gives cause test_defect, route cap; with a per-family findings[].cause override, nobody_review, nobody_environment and nobody_tooling PASS with no product change: 14 rows are a fixture-only fix",
    "D3: the 6 resume_limit rows stop on dead_dispatch, recover, resolve_return after three resumes (driver_machine.py:1556-1579, 1666-1678), never on the exit_limit seam; root not pinned, a trace is owed before a builder"
  ],
  "class_completeness": "Surface: the closing role's send-back finish of a windowed stage. S2/S3 (stage_in_repair), S4 (cases_in_repair), S6 (stage_superseded) and S7 (repairs_pending) return OpenWork; the S5 window critic (serial road and last window of a chain) and its recovery twin completion_for S5 do not. The mechanical-round complete in s5_mechanical_round is the same surface and is named in the B DoD. No scan beyond these files.",
  "trail": {
    "read": [
      "plans/piles/live-run-fvf/batch-3-live-run-fvf.md:37,49-54,64-66",
      "docs/tasks/specs/reviews/t-1331-p1b-s5-dry-code.md",
      "ai-packages/qa-factory/scripts/tests/fixtures/driver-exits/known_red/s5.json",
      "ai-packages/qa-factory/scripts/tests/fixtures/stories/dry-1/exits/s5.json",
      "ai-packages/qa-factory/scripts/tests/fixtures/stories/dry-1/seeds/s5.json",
      "ai-packages/qa-factory/scripts/tests/test_scenario_dry_1.py",
      "ai-packages/qa-factory/scripts/tests/dry_driver.py",
      "ai-packages/qa-factory/scripts/tests/dry_world.py:260-300,540-570,839-960,1115-1500",
      "ai-packages/qa-factory/scripts/tests/dry_stub.py:100-140,1070-1125",
      "ai-packages/qa-factory/scripts/repair_route.py:19-139",
      "ai-packages/qa-factory/scripts/driver_dispatch.py:481-616,780-900,2290-2335,3023-3036,3170-3330,3851-4040",
      "ai-packages/qa-factory/scripts/driver_machine.py:40-80,285-470,1500-1580,1655-1678",
      "ai-packages/qa-factory/scripts/driver_stage_s5.py:420-500",
      "ai-packages/qa-factory/scripts/driver_stage_plan.py:750-765,1005-1040,1215-1310",
      "ai-packages/qa-factory/scripts/controller.py:100-111,5960-6020,7295-7340,7788-7828"
    ],
    "reruns": [
      {"command": "python -B Temp/t1542/probe.py --part exits:s5 --exits-root Temp/t1542/root --ledger Temp/t1542/none.json (5 rows)", "result": "5 FAIL met the conductor at S5; details: story_step finish S5-qa-code-critic-1 refused, no role to close it (3 class-1 rows); resolve_return returned_unaccepted (2 resume rows); 1/11 ok, exit 1"},
      {"command": "python -B Temp/t1542/probe2.py --part exits:s5 --exits-root Temp/t1542/root2 --ledger Temp/t1542/none.json (s5.nobody_environment/fixed)", "result": "form findings cause test_defect; route counted 0 cap 2 = test_defect round; counted 2 cap 2 = close code cap; 1/3 ok"},
      {"command": "python -B Temp/t1542/probe.py --part exits:s5 --exits-root Temp/t1542/root3 --ledger Temp/t1542/none.json (3 nobody rows with findings[].cause override)", "result": "PASS nobody_review/review, nobody_environment/fixed, nobody_tooling/debt; 4/4 ok, exit 0"}
    ]
  },
  "mutants": [],
  "mutants_none": "diagnosis of a pile row, no diff under review"
}
```
