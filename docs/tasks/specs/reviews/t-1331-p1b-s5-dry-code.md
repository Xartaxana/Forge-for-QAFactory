# t-1331 critic: P1-b N4:s5 dry group (t-1223 rounds 1-8), "is green honest?"

Branch `origin/worktree-agent-a7d6e0ca5e89bf763` (head 705282bb, CI head 384e2ed4), base origin/main 25ff21f5.
Pile rows read: batch-3-live-run-fvf.md:52 (FV3-23), :62 (FV3-33), :64 (FV3-35); also FV3-17 (:46), FV2-95 (batch-2 :122).

**Verdict: NEEDS WORK** -- 1 blocking finding (F1), 1 fix-in-round (F2), 3 notes. The JSON block below says `blocker`
because rule 23 maps "any finding blocks" to `blocker`; it is not a REJECT of the work. Accepting the node, and opening or
widening nodes, is the Lead's decision.

Context the Lead should keep in view: in CI job 134490000550 the s5 part reports `=== scenario dry-1: 1/1 ok ===`. Of the
60 rows, 57 are known_red, 3 are `after:FV3-23`, and **0 rows ran green**. So "green" here means only that every row has a
label. Whether that is honest depends entirely on the labels being true.

## Findings

**F1 (blocker): 21 rows are labelled FV3-23, but FV3-23 does not describe why they are red. This is a hidden red.**
The rows: `driver-exits/known_red/s5.json:4` onward, i.e. `s6.walk_supply/*`, `s6.walk_account/*`, `s6.data_change/*`
and `kind:{data_change,walk_account,walk_supply}/*`.
- FV3-23 (pile :52) is about the main pass stopping at S7 because the stub has no `qa-failure-analyst@S7` row. These
  rows ask at S6 and start at S5. Their own `raised_by` says they "meet that stop first", which means S6 has already
  passed without asking. The real cause is that the seed never reaches the question, not the S7 stop.
- Read in the code, all three S6 asks need a world condition that no seed or stub here creates:
  - `walk_supply` and `data_change` are raised only inside `walk_assign_step`. That step runs only on the parallel road:
    `driver_stage_s6.py:1262` `if self.s6_walkers_cap() != 1 and len(plan["blocks"]) >= 2`. It also needs a pool
    shortage (`:1480`) or a lane left alone for lack of data (`:1485`).
  - `walk_account` is raised only from `walk_refuse_gaps` (`:28-60`), for a lane whose stand account has no pair.
  - The dry story has one manual-agent case (story.json:61, TC-2) and touches no sign-in (story.json:146). Since
    FV3-21, S6 with no stand dispatches no walk at all (known_red.json `main/S6` raised_by).
  - The seeds for these rows (`seeds/s5.json` `to-s6-*`, `to-kind-*`) are a bare `drive_until`. They make no move.
- Failure scenario: FV3-23 lands, the S7 stop goes away, and all 21 rows stay red ("seed did not reach s6.walk_supply").
  `known_red.reconcile` (known_red.py:130-144) only checks red or green, so the label stays valid. It then points at a
  closed node whose cause has gone, which is exactly the hidden-red edge of the dispatch.
- The builder's own round-6 argument for class 2 ("an answer row for S7 would only move the stop to S8/S9; it would not
  make any of the nine asks appear") applies word for word to these rows. They were relabelled to FV3-23 anyway in the
  same round.
- No CI log has ever printed a failure reason for these rows. They were labelled FV3-21 from round 4 and FV3-23 from
  round 6, and runs 44155530413, 44189095637 and 44205734909 print them only as known red.
- Fix (the label and node decision is the Lead's): relabel the 21 rows to a node that describes this cause: "no dry seed
  move creates the S6 precondition (parallel road with 2+ lanes and walkers != 1, a pool or data shortage, a stand
  account with no pair)". That means widening FV3-33, which is the same class ("unreachable by any seed move ... give a
  seed or a product node") but whose text names only `code_close.*`, or opening a sibling node. Rewrite `raised_by` to
  match.

**F2 (fix-in-round): the shared class-1 stub can never reach `s5.nobody_*`. FV3-35 leaves a second cause unnamed for 14 of
its 24 rows.** The stub text is in `stories/dry-1/exits/s5.json`, e.g. the overrides at :58, :125, :192, :259, :325, :392.
- All 18 class-1 rows carry one byte-identical stub (rows grouped by `json.dumps(stub)`: a single group covering
  s5.repair_limit and s5.nobody_{review,environment,tooling}).
- Its form overrides set only `review.outcome` and `scope[].state`. The filler fills the finding's `cause:
  <one of vocabulary.repair_causes>` with rule `closed-list` -> `first_option` (form-fill-rules.json:6, form_filler.py:177).
  That gives `test_defect`, the first item of `repair_causes: [test_defect, mechanical, environment, tooling,
  reviewer_error]` (vocabulary.yaml:127).
- `repair_route.route` (repair_route.py:79-139) turns a blocking `test_defect` into a round until the cap, and then
  `code="cap"`. `driver_dispatch.repair_limit_facts` (:3304-3315) maps `cap` to `s5.repair_limit`. It picks
  `s5.nobody_environment|review|tooling` only for `code=="nobody"` (blocking causes in NOT_ROUNDS) or `untyped` (no typed
  finding). This stub produces neither.
- Failure scenario: FV3-35 fixes the S5 conductor stop. The 4 repair_limit rows can then turn green, but the 14 nobody_*
  rows go on failing as "seed did not reach s5.nobody_*", for a cause that FV3-35's row does not name.
- Fix (either is enough): (a) give each family its own stub override, `findings[].cause: environment` /
  `reviewer_error` / `tooling`. For nobody_review, the `untyped` road (no findings row) is the other way in. Or (b), if
  the Lead keeps "no blind stub rounds", the Lead adds this second cause to FV3-35's row, so its builder fixes it in the
  same round.
- The repair_limit stub itself is honest: a coherent reject (`concerns`, `critic_verdict: rejected`, a findings file
  with a roll-call, a probe model) using vocabulary words only, never clean, with no forced pass.

**N1 (note): the labels are trusted, never checked against a measured cause.** `reconcile` is boolean, and CI prints
`known red: <id> -? <node>` with no reason. The FV3-33 and FV3-23 `raised_by` cite run 44189095637 (fd715e65). Two
merges of main came after it. The current stop of those 33 rows on 384e2ed4 has not been measured. For FV3-33 the label
still fits, because its pile row names the root cause ("no seed move reaches no_move.code_close_offer"), which does not
depend on where the stop is. Before any of the three nodes closes, its critic should read the rows' FAIL text with the
label removed in a scratch run.

**N2 (note): 30 census joints went `unwalked` -> `live_only` on an estimate.** `driver-exits/s5.json` changes 28
`acceptance:*`, `s5_precheck:*` and `manifest_put:probe_owed`, with cause "estimate, not verified: post-answer turn is
one driver boundary". Each has a `raised_by` entry, and the cause class is the open node FV2-95, so nothing is silent.
The estimate is still unmeasured.

**N3 (note): `exit.resume_limit_halted` carries a risk the builder declared and nobody has measured.** A halting digest
may be exempt from required outputs, which would take the halt road instead of the ask. The rows are inside FV3-35
("6 exit.resume_limit*"), so the label fits. The resume_limit stub (a digest with no artifact path or scope line) is a
real role move, not a forced pass.

## Per DoD item
1. Seeds (`seeds/s5.json`, 16 recipes). Every recipe is a bare `drive_until {stage, question}`. None forces a pass, but
   none makes a move either. The S6 and code_close rows therefore depend on world conditions that nothing creates (F1;
   FV3-33 for code_close). The only real moves are the row stubs (F2, N3).
2. Labels (57). FV3-35 has 24 rows, all read: the pile row describes exactly these 24 rows, with F2 as the partial
   exception. FV3-33 has 12 rows, all read (cheap): they fit pile :62. FV3-23 has 21 rows, all read: they do not fit
   (F1). Pins: `pins.known_red` is 57, which equals the row count.
3. `driver-exits/s5.json`. Comparing main with the branch by key, no key is removed and none is added. Changes: 30
   joints `unwalked` -> `live_only` (N2) and 3 kinds_without_key `unwalked` -> `story` (their walk rows are the
   `kind:*` rows, F1). The ratchet goes from `unwalked` 33 to 0. The `live_only` rows are carried by 30 named
   `raised_by` entries. No exit is silently dropped. The 12 answer variants deleted in round 2 are written to FV3-17
   (pile :46, class F-P4) in the report, round 2.
4. Class-1 stubs. The reject is honest (F2, last bullet), but it is the wrong stub for the 14 nobody_* rows (F2).

No exit is red in CI without a label or a fix. The job 134490000550 grep `FAIL` gives 0 lines. Positive control: the same
grep on job 134413579643 printed 36 FAIL lines.

## Standing questions (short; a fixture-only diff)
- Q4 class: F1 is the sibling class of FV3-33 (a seed that reaches nothing). Siblings by the map: other groups' seeds use
  `drive_until` only for asks the main pass already makes; I did not scan further. A wider scan is a scout task for the
  coordinator.
- Q5 tests: the walk rows are the test. Their killing power is nil while every row is labelled (0/60 green).
- Q6 duplication and consistency: none found. The new ledger follows the form of known_red/{s0,gates}.json (ls-tree).
- Q7 code quality: none found. JSON data only. The 18 copies of the stub are a copy-paste block (F2 asks for them to be
  split anyway).
- Q9 ratchets: `known_red/s5.json` is new, with pin 0 -> 57 (FV3-23 21, FV3-33 12, FV3-35 24, each with a raised_by
  and an open node). `driver-exits/s5.json` `unwalked` goes 33 -> 0, and `live_only` gains 30 rows, named. Re-run
  `dry_exits --check`: 0 discrepancies.
- Q10, Q11, Q12: none found. No package code changed and no language branch was added (the diff stat shows 5 files:
  fixtures and the report; the workflow is unchanged against main).

## Trail
- `git diff --stat origin/main...origin/worktree-agent-a7d6e0ca5e89bf763`: 5 files, +2551/-68.
- Read on the branch: the report (rounds 1-8); known_red/s5.json (all 57 rows, grouped by node); seeds/s5.json (whole
  file); exits/s5.json (stubs grouped by key; raw bytes checked: 66 x `C2 B7` and 0 Cyrillic. An earlier "В·" was my
  console's cp1251 decoding, not the file); driver-exits/s5.json main vs head (scripted key comparison);
  known_red.py:130-144; known_red.json `main/S6`; story.json; driver_stage_s6.py:28-125, 1240-1263, 1472-1490;
  driver_dispatch.py:3285-3320, 3535-3735; repair_route.py:79-139; form_filler.py:160-200; form-fill-rules.json;
  vocabulary.yaml:127; the pile rows listed in the header.
- `ci_read.py log 134490000550 --grep "known red"`: 57 of 57 lines (FV3-35 24, FV3-33 12, FV3-23 21).
- `ci_read.py log 134490000550 --grep "ok ===|PASS|after:|prefix|FAIL|stopped|reached"`: the prefix reached S5 in
  144.9 s, 3 x `after:FV3-23`, `PASS dry-1/exits:s5/outcomes`, `1/1 ok`, 0 FAIL.
- `ci_read.py log 134413579643 --grep FAIL` (run 44189095637): 18 class-1 rows "conductor at S5", 18 class-2 rows
  "conductor at S7", and no s6 row printed with a reason.
- `python -B <worktree>/ai-packages/qa-factory/scripts/tests/dry_exits.py --check`: `dry_exits --check: 0 discrepancies`.
- Negative searches, each with a positive control: `cause|findings|test_defect` in form_filler.py gave 0 hits (control
  `def fill_form` gave 1); `cause|closed-list` in form-fill-rules.json gave only the closed-list rule at :6.

```json
{
  "verdict": "blocker",
  "blockers": [
    "F1: 21 known_red rows (s6.walk_supply/walk_account/data_change and kind:* in driver-exits/known_red/s5.json) are labelled FV3-23 (S7 stub row), but their asks need a parallel S6 road / pool shortage / stand account gap that no seed creates (driver_stage_s6.py:1262, :1480, :1485, :28-60); fixing FV3-23 leaves them red under a stale label - hidden red; relabel to a node naming that cause (widen FV3-33 or a sibling node, Lead's call)"
  ],
  "fixes": [
    "F2: the class-1 stub (exits/s5.json, 18 identical copies) leaves findings[].cause to the filler's first option test_defect, so the route is cap -> s5.repair_limit and never nobody; give s5.nobody_environment/review/tooling their own cause override, or the Lead names this second cause in FV3-35's pile row"
  ],
  "class_completeness": "F1 is the same class as FV3-33 (a bare drive_until with no move that creates the ask's precondition); 33 of the 57 labels share it; a scan beyond group s5 is left to a scout",
  "trail": {
    "read": [
      "docs/tasks/specs/reports/20261117-p1b-n4-s5-report.md",
      "ai-packages/qa-factory/scripts/tests/fixtures/driver-exits/known_red/s5.json",
      "ai-packages/qa-factory/scripts/tests/fixtures/stories/dry-1/seeds/s5.json",
      "ai-packages/qa-factory/scripts/tests/fixtures/stories/dry-1/exits/s5.json",
      "ai-packages/qa-factory/scripts/tests/fixtures/driver-exits/s5.json",
      "ai-packages/qa-factory/scripts/tests/known_red.py:130-144",
      "ai-packages/qa-factory/scripts/driver_stage_s6.py:28-125,1240-1263,1472-1490",
      "ai-packages/qa-factory/scripts/driver_dispatch.py:3285-3320",
      "ai-packages/qa-factory/scripts/repair_route.py:79-139",
      "ai-packages/qa-factory/scripts/tests/form_filler.py:160-200",
      "ai-packages/qa-factory/handoffs/vocabulary.yaml:127",
      "plans/piles/live-run-fvf/batch-3-live-run-fvf.md:46,52,62,64"
    ],
    "reruns": [
      {"command": "python -B <worktree>/ai-packages/qa-factory/scripts/tests/dry_exits.py --check", "result": "dry_exits --check: 0 discrepancies"},
      {"command": "ci_read.py log 134490000550 --grep known red", "result": "57 of 57 lines: FV3-35 24, FV3-33 12, FV3-23 21"},
      {"command": "ci_read.py log 134490000550 --grep FAIL|ok ===", "result": "0 FAIL; scenario dry-1: 1/1 ok; 3 after:FV3-23"}
    ]
  }
}
```
