# Code critic CR-L: the P1-b landing (t-998)

Under review: `origin/pile/live-run-fvf/batch-3` (HEAD 6819c66d) against `origin/main` (a6df7fd1), merge base 66a6b264. Spec: `docs/tasks/specs/20261117-p1b-finish-spec.md` (cards L1, L1c, L-ax, L2, CR-L; forks F-P*; Lead decisions). One pass for the topic. The context budget (250K) ran out at the end of the pass. Everything below was checked; the parts left unchecked are listed at the end.

## Verdict

**NEEDS WORK (fit_with_fixes).** There are 3 blocking findings, all about red CI the branch causes itself: B1 lint ratchet, B2 driver-layers L8, B3 the keep-covers row. Most of the other CI-2 reds come from main. K-C1, K-C2 and K-C5 hold. K-C10 holds once one stale comment is fixed. The list of fixes is at the end. Accepting the work is the Lead's decision.

## Keys

- **K-C1 (merge adds no behaviour beyond the branch): holds.** I ran `git show --remerge-diff` on every merge in `origin/main..branch`: 8011b58b (L1), 71d61d33, f3a148e1, 906bdf8a, 4304cd94 and c33dc5de are all empty, so each equals the automatic merge. The only manual resolution is 9c9d40c2 (`driver-exits/known_red.json`: union of rows `kind:halt/free words` and `s1.review/unavailable`, pin 2→3). Its commit message names it, and L2 replaced it later. Re-run: `merge-tree` → `d0bf4528…` with rc 0; `diff --stat` → `57 files changed, 6473 insertions(+), 135 deletions(-)`. Both match the dispatch.
- **K-C2 (L1c rows): holds, checked by script.** The L1 report (bec6c773) has 227 `FAIL joint …` lines, all distinct. The joints added between bec6c773 and 98d8ed58 are the same 227 ids (set equality True). Joint ids can contain spaces, e.g. `role_cli:artifact_producer.py publish`, so the parse cuts at ` [tail]`. All 227 new rows are `reach: unwalked` with the spec's `why_unreached` text. Each group got exactly one `raised_by` per new row (gates 84, s1-s4 33, s5 49, s6-s9 61), all in the form `unwalked | joints/<id> | L1c census catch-up, 2026-11-17`. The `unwalked` bases did not change (21/0/31/6). No other key moved. I ran the group rule over all 267 census joints, with stages read through `null_outcomes.load_data(stage_joints.DATA)`: there is 1 mismatch, `branch_accounting:*` (S2–S5, standing, sits in `s1-s4`, the rule says `gates`). That is the exception named in the Lead decisions for t-978. After L1c the census files did not move, except `known_red.json` (L2).
- **K-C3 (labels): holds partly. See F1 and F2.** `main/S5 → FV3-5` (stub gap), `kind:halt/free words → FV3-16` (product gap, "cause not located": L0 edge 1) and the form-rounds row → FV3-18 all point to batch-3 rows with finding files on main. `s1.review/unavailable` was deleted from both the ledger and `stories/dry-1/exits/s1-s4.json`, and the pin went 3→2 (F-P4 (b)). The selftest ledger N4W-1 is unchanged (edge 9).
- **K-C4 (duplication and code quality): findings D1–D4 and Q1–Q4.** The clone ratchet never ran on this branch (F5).
- **K-C5 (AR lines of §1): hold.**
  - AR-17: `grep -i "driver\.[a-z_]+ = "` over `dry_*.py` and `test_scenario_dry_1.py` finds 0. The same pattern finds 3 hits in `infra_failure_common.py:157` and `no_move_seam_common.py:34,44`. The control the spec named, `test_stage_critic_route.py`, does not exist on the branch. `dry_driver` replaces module functions (`no_move.priced_options`, `driver_machine.match_known`), never a Driver attribute. Its calls inside `driver_machine.py:91,95` look the name up in the module globals, so the spy sees them.
  - AR-13: no `json.load` of a ledger outside `known_red.py` (control: `known_red.py:62`). `_norm` reuses `DriverDialog.s0_normalize`.
  - AR-28: holds by `--check`.
  - AR-20: raises are named (question 9 below).
  - AR-29: holds (K-C8).
- **K-C6 (FR pass): F3.** The n2f and n2g reports have no FR pass at all: grep `FR pass|FR-[0-9]+` finds 0 in each and finds it in the other 11 reports. L1's FR pass covers only "edited by me", and L1c's is one line.
- **K-C7 (class completeness, axes): F4 for axis 18.** Axis 30 holds: the stub reads commands through `PC.profile_commands` / `command_argv` (`dry_stub.py:490-493`). Axes 5 and 17: not applicable, no package code or detector shape changed. Axis 34: one runner row, and N6 is a queued node. Axis 38 was added and its text matches L1c. Axis 18: see F4.
- **K-C8 (judgment): holds.** The stub takes verdicts from the row control (`dry_stub.py:91-93,775`; the default conductor offers every open move). The walker compares recorded facts with `expect.checks` (`judge_row`). No role verdict is computed. `judgment-census` does not scan `scripts/tests/`.
- **K-C9 (which reds are the branch's own):**
  - **Own:**
    - **B1:** forge-check `lint_ratchet --check`: 6 new findings, 5 of them in branch files (`dry_exits.py:1364` (unused `known`), `:2156` (unused `import types`), `dry_stub.py:1342` (unused `moves`), `dry_world.py:894` (f-string with no placeholder), `:949` (unused `import dry_stub`)). Main's run 44002414696 has 1 new finding (`tools/test_hygiene_gate.py:348`), and neither baseline has a `dry_*` row. Because this step fails, steps 8–20 were skipped: `dup_ratchet`, journal, piles check, `pytest tools/` (F5).
    - **B2:** `test_driver_layers.py` 282/283, L8. I re-ran it on fvf3. The 2 problems: `dry_driver.py:70 in main` holds the literal `story_run.py` and has no map row; and the row `dry_world.py`/`drive` in `fixtures/driver-layers.json:1295` is now stale, because `drive` runs `dry_driver.py`. It is not red in main's run.
    - **B3:** `test_selftest_slow_tests.py`. The count is the same as main (110/124), but the FAIL row "every keep row covers the helpers it imports" adds `'test_scenario_dry_1.py: tests/harness.py'` on the branch. Main's list does not have it.
  - **From main, not the branch** (same FAIL in main's run 44002414696): `gate_brief --selftest` (brief cap), `test_story_run_loop_b_loop` 264/270, `test_execution_request`, `test_config_migration` 632/633 (OH3-17), `test_audit_rules`. Main has 371/375; the branch's 1 failure is A22, the qa-automator role load of 25,683 from `references/slices`, which the diff does not touch. Also from main: `test_rc1_14_rule_lines`, `test_selftest_shard`, `test_stage_joints` rows-for (main's package-fast shows the same 114 vs 108), `test_probe_by_code`, `test_story_run_refusals`, `test_red_sandbox_probe`, `test_s7_null_outcome`. **The dispatch said the first six are "not in main's red list". That is wrong for 5 of the 6: they are red in main's run artifact. Only `test_driver_layers` is the branch's.**
- **K-C10 (slow_tests and TEST_TIMEOUTS): consistent, apart from F6.** `slow_tests()` documents its seconds as "the duration the measuring run printed for the file" on CI `--jobs 4`. 138.0 is verbatim from run 44000950573 shard 2 (`PASS tests: scripts/tests/test_scenario_dry_1.py  138.0s`; I re-read it). CI-2 printed 210.8 s. Both are far above `slow_over_s` 10, so the tier is right. 900 is the ceiling: the local main pass alone is 304.8 s, which is ≤ 800 (L2 edge 10). The comment next to it is stale (F6).

## Findings

- **B1 (blocks): lint ratchet red, caused by the branch.** Evidence: K-C9. Mechanism: `forge-check` fails at step 7, so `main` would go red, against the spec's invariant "main does not turn red".
- **B2 (blocks): driver-layers L8 red, caused by the branch.** The same mechanism under the key "L8 rows" of axis 18.
- **B3 (blocks): the keep row of `test_scenario_dry_1.py` lacks `tests/harness.py` in `covers`.** The file imports `harness` at line 21.
- **F1 (fix): the FV3-5 finding names only one of the two fields the S5 critic form cannot fill.** The CI-1 stop (`20261117-p1b-ci1-lines.txt`) also prints `probes.runtime_provenance: … no run block of dispatch S5-qa-code-critic-1 … carries a runtime_provenance record` (`handoff_check.py:551`). `grep -i "runtime_provenance|run_suite"` over the finding file finds 0; the control `probe_by_code` finds 5. `probe_by_code.py:13` runs `run_suite.py --request`, so FV3-5's fix probably also produces the run block. That is an estimate, not measured. The DoD of the node must say so: otherwise FV3-5 can pass its selftest row and the stop stays where it is.
- **F2 (fix): the form-rounds row `obligation_refs <- manifest_row@all -> window_record.row_field_gaps` does not start with `product gap:`.** Spec §1 says every registry row this spec writes starts with its class. Edge 7 only said "append". No code reads the prefix (grep `stub gap|product gap` over `scripts/tests/*.py`: only `test_d1_product_gap.py`, which is unrelated), so adding it is safe.
- **F3 (fix): FR pass missing for the n2f/n2g content** (kit channel, `plan_rows`, `world_list_tokens`, the `test_field_producers` expectation change). These touch C (FR-11/14/38), D (FR-16, FR-58: the new expectation comes from the contract plus `manifest_put.py`, not from the filler's output) and G.
- **F4 (fix, Lead tier): axis 18 and brief question 9 do not name the dry census ratchets.** Missing: `driver-exits/<group>.json` `ratchet` (`unwalked`/`live_only`/`after`/`hook_layer` with `raised_by`), `driver-exits/known_red.json` with `pins.known_red`, and `stories/dry-1/selftest/known_red.json`. `grep -i -c driver-exits` gives 0 for `docs/SIBLING_MAP.md` on main and 2 on the branch (both in axis 38), and 0 for `critic-diff-brief.md`. The control `form-rounds.json` finds 1 in the brief. Calibration check 35(b) therefore never reads this branch's raise of 227 `unwalked` rows.
- **F5 (fix): the mechanical layer is incomplete.** `dup_ratchet --check`, journal, piles and `pytest tools/` were skipped on CI-2 (job 133781715829, steps 8–20 `skipped`). About 3000 new lines of test code have no clone-ratchet verdict. The witness-for row is F7.
- **F6 (fix): stale comment.** `selftest.py:115-116` says "48 s at the first stop, S1". The measured values are 138.0 s / 210.8 s on CI and 304.8 s for the local main pass, and the pass stops at S5.
- **F7 (fix): the keep row's `covers` entry `scripts/tests/fixtures/driver-exits` is dead for files.** `scenario_walk.witness_for:914-916` matches `covers` by exact path only. Re-run: every `driver-exits/*.json` gives "no scenario or keep row covers … run the whole scenario layer" (6 scenario files). L1c's witness passed only because it passed the folder itself. The same folder form exists in the 4 story rows, but those are also matched by story folder.
- **D1 (fix): three copies of one helper.** `dry_exits._cut` (`:958`) and `dry_world.cut` (`:726`) are new copies of `dry_stub.cut` (`:216`, already on main).
- **D2 (fix): two runner functions where one would do.** `dry_stub.run_script` / `run_script_both` (`:197-213`) differ only in the text they return. `:529` picks one by `run is run_script`, an identity test on the test seam.
- **D3 (fix): one block written three times.** "run the script, then `wrote` on exit 0 or `live_only`" appears at `dry_stub.py:501-506, 512-516, 523-527`. `dry_driver.py` writes the same sink append twice (`passing_spy` / `route_spy`).
- **D4 (fix): the error text says "probe record" for any token.** `form_filler._spread_world_rows` uses that wording for any `world_list_tokens` token.
- **Q1 (fix): dead code.** The 5 lint findings of B1.
- **Q2 (fix, Lead instruction "nothing later"): new or rewritten functions over about 80 lines.** `dry_exits.walk_row_problems` 1030-1137 (108), `judge_row` 1226-1325 (100, one `elif` per check); `dry_stub.fill_role` 729-849 (121); `dry_world.drive_main` 845-941 (97), `main_pass` 944-1034 (91), `walk_exits` 1279-1368 (90), `run_exit_row` 1174-1255 (82). Risk to note for the Lead: `walk_exits` and `run_exit_row` run only in `--part exits:*`, which the canon does not run. Their witness is the `dry_exits --selftest` walker table plus a CI run of the parts.
- **Q3 (fix): a local name hides a function.** In `test_scenario_dry_1.exits_part`, the local `census` shadows the module function `census()`.
- **Q4 (fix): formatting.** `driver-exits/known_red.json:5` ends with `"} },`. The JSON is valid, but the line breaks the file's one-row-per-line form.

Question 9 (ratchet raises, row by row):
- `driver-exits/known_red.json` rows 0→2, pin 0→2 (FV3-5, FV3-16).
- `form-rounds.json` `known_red` rows 20→21 (FV3-18; this section has no pin; `not_in_world` 47→47).
- Census `unwalked` 58→285, all 227 named in `raised_by` (L1c).
- `live_only` 31 above base 0, named (t-824, from the branch).
- Lint baseline: not raised (red instead: B1).
- Driver-layers L8 rows: B2 needs one row swapped, the count stays the same.

There is no unnamed raise.

Question 12 (one road): none found. Grep `run_script_both|run is run_script` finds the seam in D2, which is a test seam, not a language or project. One runner row, `python-pytest`, plus N6 queued.

Question 5 / tests (rule 20): the landing adds one scenario file. That is legal under the TESTING.md exception (the dry story's time). L1's merge commit carries no `tests-over:` line, although everything it lands is test code. Not checked: whether the wip node commits carried that line. This is left for the fix-round report to answer (fix 12).

Duplication (item 6): D1–D4. Found with grep `^def (cut|_cut|norm|read_json|jsonl…)` over `dry_*.py`, `form_filler.py`, `harness.py`, `scenario_walk.py`, `known_red.py`. The clone ratchet result is missing (F5).

Code quality (item 7): Q1–Q4. Found by an AST pass over the branch's six files, keeping functions with at least 50 % new lines and either more than 60 lines or deeper than 3 levels. The selftest tables `_walker_cases` (414), `selftest_n2` (225) and `selftest_n2c` (173) are parameter tables and are not counted.

## Fixes: one round, a fresh Sonnet builder, the branch `pile/live-run-fvf/batch-3`

1. **B1 / Q1:**
   - `dry_exits.py` `judge_group`: delete `known: tuple = ()` (`:1360`) and `known = verdict.known` (`:1364`).
   - `dry_exits.py` `_walker_cases`: delete `import types` (`:2156`).
   - `dry_stub.py` `selftest_n2`: delete `moves = NM.move_rows(spec)` (`:1342`).
   - `dry_world.py:894`: drop the `f` prefix.
   - `dry_world.py` `main_pass`: delete `import dry_stub` (`:949`).
   - Witness: `python tools/lint_ratchet.py --check` lists no `dry_*` file. The `tools/test_hygiene_gate.py` finding is main's and is not this round's.
2. **B2:** in `scripts/tests/fixtures/driver-layers.json` `source_mentions`, replace the row `{"file": "dry_world.py", "function": "drive", …}` with `{"file": "dry_driver.py", "function": "main", "count": 1, "why": "message text: the refusal names the arguments of story_run.py, not a read of the source"}`. Witness: `python -B scripts/tests/test_driver_layers.py` → 283/283.
3. **B3:** in `scripts/tests/test-layers.json`, keep row `test_scenario_dry_1.py`, add `"tests/harness.py"` to `covers`. Witness: `python -B scripts/tests/test_selftest_slow_tests.py`; its keep-covers FAIL row must no longer name `test_scenario_dry_1.py`. The file stays red for main's rows.
4. **F7:** in `scenario_walk.witness_for` (`:914-916`), a `covers` entry naming a folder covers every path under it: match when `c == cov or c.startswith(cov.rstrip("/") + "/")`. Add a row to `test_scenario_walk.py` (`witness`, `:61-63`): a keep row whose `covers` lists `fixtures/x` and a changed `scripts/tests/fixtures/x/a.json` → `keep … covers it`; a sibling `fixtures/xy/a.json` → not covered. Witness: `python -B scripts/tests/test_scenario_walk.py`, then `--witness-for ai-packages/qa-factory/scripts/tests/fixtures/driver-exits/s5.json` names `keep test_scenario_dry_1.py`.
5. **D1:** `dry_stub.cut` becomes `" ".join(str(text).split())[:limit]`. Delete `dry_exits._cut` and `dry_world.cut`. Their call sites call `dry_stub.cut(x, 300)`, keeping each call's own limit. There is no import cycle: `dry_stub` imports `dry_world` only inside functions. Witness: `dry_exits.py --selftest` 154/154, `dry_stub.py --selftest` 189/189.
6. **D2:** delete `run_script_both`. `run_script(project, script, args, *, both=False)` returns `stdout + stderr` when `both` is true. `automator_branch:529` becomes `run(project, "run_suite.py", [...], both=True)`. Every stand-in for `run` in the `dry_stub` selftests accepts `**kwargs`. Witness: `dry_stub.py --selftest`.
7. **D3:** add a local helper `_record(out, code, text, output, why_head, case=None)` in `dry_stub.py` and use it at the three sites. Add `_append(sink, record, what)` in `dry_driver.py` and use it in both spies. The behaviour and texts stay byte-identical. Witness: as fix 6.
8. **D4:** add a `"what"` field (for example `"probe record"`) to each `world_list_tokens` row of `form-fill-rules.json`. The `_spread_world_rows` text reads `tokens[found[0]]["what"]`. Witness: `test_form_selftest.py` 26/26 or more, `test_field_producers.py` 885/885.
9. **Q2:** split each function named in Q2 into its steps as private helpers in the same module, with no change in behaviour. `judge_row`: one function per check id, held in a `{check_id: fn}` table. The others: by their existing comment blocks. Witness: `dry_exits.py --selftest` and `dry_stub.py --selftest` unchanged. Then the coordinator runs the canon (default mode) and `--part exits:s0` / `exits:s1-s4` on CI.
10. **Q3:** in `test_scenario_dry_1.exits_part`, rename the local `census` to `census_data`. **Q4:** reformat `driver-exits/known_red.json` to one row per line, closing with `}` alone on its own line, and keep the line endings.
11. **F6:** the comment at `selftest.py:115-116` becomes: "main pass stops at S5 today: 138.0 s (canon 44000950573) / 210.8 s (44006084665) on CI, 304.8 s locally for the main pass alone; the ceiling holds the pass through S9".
12. **F2, F3:**
    - F2: the `raised_by` of the form-rounds row starts with `product gap: `.
    - F3: the L1 report gets a section "FR pass of the landed n2f/n2g content" covering sections C, D and G, one line each, plus the `tests-over:` answer from the Question 5 paragraph above.
13. **F1, F4 (Lead or a builder on pile and map files):**
    - F1: the finding `20261117-p1b-s5-zaglushka-kritika-ne-zapuskaet-probu.md` gets the CI-1 stop under «Что не так» (both fields), and its item 4 gets a second table row: "critic form's `probes.runtime_provenance` is filled after the probe".
    - F4: axis 18 «The members» adds the dry census ratchets and the two `known_red.json` ledgers. `critic-diff-brief.md` question 9 names them in the same commit, with an axis block and a `tier:` line.
14. **F5:** after fixes 1–13, the coordinator gets `forge-check` steps 8–20 of the branch. `dup_ratchet --check` is the one that matters. Main's own `test_hygiene_gate` lint finding blocks those steps on CI, so the coordinator runs `python tools/dup_ratchet.py --check` on the branch tree and attaches the output. A new clone in a `dry_*` file is fixed in the same round.

## Not checked (budget)

- I did not read whether the wip node commits carried `tests-over:` lines.
- Q2 is listed by size and depth only; I did not read every function's body.
- I read the fixtures by sample: s1-s4 walk rows, known_red files, s5 census head.

## Trail

- **Read:** the spec (sections 0-4, Lead decisions, fix table); `critic-diff-brief.md` 8-123; `SIBLING_MAP.md` axis 18 and axis headers; on the branch: the reports for L1 (FR, classification), L1c (DoD, FR), L2 and ci1-lines; on main: findings FV3-5 and FV3-19 and batch-3 rows; `test_scenario_dry_1.py` (whole); `dry_driver.py` (whole); `dry_exits.py` 502-513, 958, 1209, 1226-1418; `dry_stub.py` 197-219, 440-533, 1338-1352; `dry_world.py` 892-895, 946-951; the `form_filler.py` diff; `scenario_walk.py` 886-923; `test_scenario_walk.py` 40-89; `test_driver_layers.py` 965-1020; `selftest.py` 1003-1039 (`slow_tests` rule); the diffs of `known_red.json`, `form-rounds.json`, `test-layers.json`, `selftest.py`, `slow_tests.json`, `test_field_producers.py`, `SIBLING_MAP.md`, `features.json`.
- **CI read:** `ci_read why` for 44006084665 and 44002414696; the shard artifacts of both runs and of 44000950573; the steps of job 133781715829.
- **Re-runs:** listed in the json block.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "B1: forge-check lint_ratchet red by the branch: 5 new pyflakes findings in dry_exits.py:1364,2156, dry_stub.py:1342, dry_world.py:894,949 (main has 1, tools/test_hygiene_gate.py); steps 8-20 incl. dup_ratchet skipped",
    "B2: test_driver_layers.py 282/283 by the branch: L8 dry_driver.py:70 main has no source_mentions row; row dry_world.py/drive in fixtures/driver-layers.json:1295 stale",
    "B3: test_selftest_slow_tests keep-covers row gains 'test_scenario_dry_1.py: tests/harness.py' on the branch (absent from main's run 44002414696)"
  ],
  "fixes": [
    "1 B1/Q1: delete dead lines dry_exits.py:1360,1364,2156; dry_stub.py:1342; dry_world.py:949; drop f-prefix dry_world.py:894; witness lint_ratchet --check names no dry_* file",
    "2 B2: fixtures/driver-layers.json source_mentions: replace row dry_world.py/drive with dry_driver.py/main count 1; witness test_driver_layers 283/283",
    "3 B3: test-layers.json keep test_scenario_dry_1.py covers += tests/harness.py",
    "4 F7: scenario_walk.witness_for:914-916 folder covers entry covers paths beneath it; row in test_scenario_walk.py (x covers x/a.json, not xy/a.json)",
    "5 D1: one cut helper (dry_stub.cut with str(text)); delete dry_exits._cut, dry_world.cut",
    "6 D2: merge run_script_both into run_script(both=False); automator_branch:529 calls run(..., both=True)",
    "7 D3: local helpers for the 3 manifest/run record blocks in dry_stub.automator_branch and the 2 sink appends in dry_driver",
    "8 D4: world_list_tokens rows carry a what field; _spread_world_rows text reads it",
    "9 Q2: split walk_row_problems, judge_row (check table), fill_role, drive_main, main_pass, walk_exits, run_exit_row into helpers, behaviour unchanged; selftests plus a CI run of exits parts",
    "10 Q3/Q4: rename local census in exits_part; one-row-per-line form of driver-exits/known_red.json",
    "11 F6: selftest.py:115-116 comment states the measured 138.0/210.8 s CI, 304.8 s local main pass, stop S5",
    "12 F2/F3: form-rounds row raised_by starts with 'product gap: '; L1 report adds the FR pass of n2f/n2g content (C, D, G) and the tests-over answer",
    "13 F1/F4: FV3-5 finding names probes.runtime_provenance and a second DoD row; axis 18 and brief question 9 name the dry census ratchets and both known_red ledgers",
    "14 F5: coordinator attaches dup_ratchet --check of the branch tree after fixes 1-13"
  ],
  "class_completeness": "Axis 18 is incomplete: the driver-exits ratchets (unwalked/live_only/after/hook_layer) and the driver-exits and selftest known_red ledgers are not members, and brief question 9 does not name them (F4). Axis 38 was added and matches L1c. Axis 30 holds (profile_contract). Axis 34: no exclusion found. Axes 5 and 17: not applicable (no package code or detector shape changed). The F7 folder-covers class: 5 keep rows use the folder form, 1 of them is dead for files (driver-exits); the fix goes in the one matcher.",
  "trail": {
    "read": [
      "docs/tasks/specs/20261117-p1b-finish-spec.md sections 0-4, Lead decisions, fix table",
      "docs/tasks/critic-diff-brief.md 8-123",
      "docs/SIBLING_MAP.md axis 18 and axis headers 5/17/30/34; branch axis 38 diff",
      "branch docs/tasks/specs/reports/20261117-p1b-l1-report.md, -l1c-report.md, -l2-report.md, -ci1-lines.txt",
      "main plans/piles/live-run-fvf/findings/20261117-p1b-s5-zaglushka-kritika-ne-zapuskaet-probu.md, -probes-records-bez-pustogo-ishoda.md; batch-3 rows FV3-5/16/17/18",
      "branch scripts/tests/test_scenario_dry_1.py, dry_driver.py (whole); dry_exits.py 502-513, 958, 1209, 1226-1418; dry_stub.py 197-219, 440-533, 1338-1352; dry_world.py 892-951 samples; form_filler.py diff; scenario_walk.py 886-923; test_scenario_walk.py 40-89; test_driver_layers.py 965-1020; selftest.py 1003-1039",
      "diffs of driver-exits/known_red.json, form-rounds.json, test-layers.json, selftest.py, slow_tests.json, test_field_producers.py, stories/dry-1/exits/s1-s4.json, plans/features.json",
      "CI runs 44006084665 (why, shard artifacts, forge-check steps), 44002414696 (why, shard artifacts), 44000950573 (shard artifacts)"
    ],
    "reruns": [
      {"command": "git merge-tree --write-tree --name-only origin/main origin/pile/live-run-fvf/batch-3", "result": "d0bf45288bbf12c21e5919549b6c6a4cc918e71b, rc 0"},
      {"command": "git diff --stat origin/main...origin/pile/live-run-fvf/batch-3", "result": "57 files changed, 6473 insertions(+), 135 deletions(-)"},
      {"command": "git show --remerge-diff on the 7 merges of origin/main..branch", "result": "empty except 9c9d40c2 (known_red.json union, named in its message)"},
      {"command": "python stdin script: L1 report FAIL joint lines vs joints added bec6c773..98d8ed58, raised_by per row, group rule by stages", "result": "227 = 227 set-equal; raised_by 84/33/49/61 one per row; bases unchanged; 1 group mismatch branch_accounting:* (standing, Lead decision t-978)"},
      {"command": "python -B scripts/tests/dry_exits.py --check (fvf3)", "result": "dry_exits --check: 0 discrepancies, rc 0"},
      {"command": "python -B scripts/tests/scenario_walk.py --witness-for <branch scripts/ files> (fvf3)", "result": "dry_*.py -> keep test_scenario_dry_1.py; driver-exits/*.json -> no scenario or keep row covers, whole scenario layer (F7)"},
      {"command": "python -B scripts/tests/test_driver_layers.py (fvf3)", "result": "282/283; L8: dry_driver.py:70 main no row; row dry_world.py/drive holds no literal"},
      {"command": "python -B scripts/tests/test_audit_rules.py (fvf3)", "result": "374/375; FAIL A22 qa-automator 25,683 (-683 free)"},
      {"command": "ci_read artifact 44002414696 shard 1/2 --grep FAIL", "result": "main red: gate_brief, loop_b_loop, execution_request, config_migration, audit_rules 371/375, stage_joints, role_load; shard 2 as dispatch list"},
      {"command": "ci_read why 44002414696 / 44006084665 (forge-check)", "result": "main lint 1 new (test_hygiene_gate); branch 6 new (5 dry_*); dup_ratchet etc. skipped"},
      {"command": "ci_read artifact keep-covers row main vs branch shard 2", "result": "branch adds 'test_scenario_dry_1.py: tests/harness.py'"},
      {"command": "ci_read artifact 44000950573 / 44006084665 grep test_scenario_dry_1", "result": "PASS 138.0s / PASS 210.8s"},
      {"command": "git grep -i -E 'driver\\.[a-z_]+ = ' dry files vs tests/*.py", "result": "0 in dry files; control 3 hits (infra_failure_common.py:157, no_move_seam_common.py:34,44)"}
    ]
  }
}
```
