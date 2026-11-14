# Wave 7 integration report (t-672, 14.11.2026)

Worktree `.claude/worktrees/wave7`, branch `wip/wave7`, cut from origin/main 6997034, pushed to `main` as fast-forwards (no force). The six branches of the list are merged; none left out.

## Merges (each `git merge --no-ff origin/<branch>`)

| # | branch (tip) | merge commit | conflicts |
|---|---|---|---|
| 1 | `wip/statuses-fv1` (22b5e2f) | a59c116 | none |
| 2 | `wip/fv118-fix` (27a6cf4; contains topic and n1..n4) | 7aee0ca | one, below |
| 3 | `wip/of3-2-k6` (e02ee1f) | 665fb82 | two, below |
| 4 | `wip/of4-3b` (70636a7) | d264a3c | none |
| 5 | `wip/of5-8` (c51b7e6) | 8120503 | none |
| 6 | `wip/p1a-n4` (fe9256a) | 466e12b | none |

`git cherry origin/main origin/wip/<b>` before merging showed every branch's commits as new (`+`), so no merge was empty.

Conflict 2 (`test_probe_by_code_languages.py`, modify/delete): main cut the file into plan/cli/ts_playwright + common (PC3-2); the branch added two `check_in` lines and `fv1_18_two_sites_one_table()`. Resolved: the old file stays deleted, the three additions are ported to `test_probe_by_code_languages_ts_playwright.py` (after the `selector contract` check of `ep1_36_shape`, the function before `tool_refusal_record`, one call in `main`, `check_not_in` added to the import). The gate-registry / launch-causes json and `role-load.json` auto-merged (no conflict; both valid json).

Conflict 3 (`guard_pre_tool.py`, `test_guard_project_knowledge.py`): main moved the `project_knowledge.py` door to `registry_write_call` (PK2-9), the branch widened the old regex with `remember|kind`. Resolved: `registry_write_call(low, "project_knowledge.py", (... "lesson", "remember", "kind"))`; the old regex line dropped; the branch's `config_contract.py` / `onboard_apply.py` lines kept; both sides' tests kept (PK2-9 tests and `test_role_running_remember_and_kind_is_blocked`).

## Numbers that moved (AR-20, all named)

1. `tools/lint-baseline.json` total 66 -> 76 (commit 59cbf64, `lint_ratchet.py --update`): UnusedImport `execution_request as er` in `test_execution_request.py` 0 -> 1 (from `wip/fv118-fix` e9ab582, a defect of that branch alone: `import execution_request as er` in `fv1_18_no_stop_one_note` is unused); HandReaderInput (the P1-a N4 line, new with `wip/p1a-n4`) `test_check_delivery.py` 3 -> 7, `test_report_facts.py` 1 -> 3, `test_s5_precheck.py` 0 -> 2, `test_handoff.py` 0 -> 1: hand-written `plan_row` inputs that came to main (FV1-30b dc8edef, 6a92521 and others) after the branch measured its baseline. Before the update `python -m pytest tools/test_lint_ratchet.py -q` had 1 failed (`test_k12_shipped_baseline_matches_the_real_tree`), after: 26 passed.
2. `ai-packages/qa-factory/scripts/tests/fixtures/told-ratchet.json` `check_coverage.py::main` bare 12 -> 13 (commit 32f9c3e): `wip/of4-3b` adds one bare site. Found by CI on my first push: run 43533215100 job package-fast, `FAIL tests: scripts/tests/test_stage_joints.py ... K4/at-baseline: ... ['check_coverage.py::main: bare is 13, baseline 12']`. `test_stage_joints.py` is a slow file, so it was not run locally; the next pipeline judges the fix (below). A defect of `wip/of4-3b` alone (its baseline row was not raised in the branch).

## Witnesses (verbatim, run from `ai-packages/qa-factory/scripts/tests` unless noted)

After merge 2 (non-slow files of `scenario_walk.py --witness-for` for the changed package files `execution_request.py launch_check.py probe_by_code.py profile_contract.py run_suite.py gate-registry.json launch-causes.json test_probe_by_code_languages_ts_playwright.py`, plus the three the spec names): 33 commands, 33 exit 0. Summary lines:
```
=== test_run_forms: 305/305 ok ===
=== test_execution_request: 650/650 ok ===
=== test_config_projection: 223/223 ok ===
=== test_delivery_ownership: 310/310 ok ===
=== test_field_producers: 915/915 ok ===
=== test_fit_targets: 116/116 ok ===
=== test_guard_big_read_sections: 248/248 ok ===
=== test_handed_to_person: 58/58 ok ===
=== test_ledger: 452/452 ok ===
=== test_manual_evidence: 248/248 ok ===
=== test_probe_by_code_languages_plan: 502/502 ok ===
=== test_probe_by_code_languages_ts_playwright: 189/189 ok ===
=== stand gaps: 182/182 ok ===
20 passed in 2.65s (test_manifest_put_assertion_line) | 19 passed (test_probe_aggregate) | 24 passed (test_probe_alternative_road) | 27 passed (test_probe_check_records) | 319 passed in 10.86s (test_probe_every_check) | 46 passed (test_probe_joint_judge) | 7 passed (test_probe_judge_languages) | 46 passed in 16.42s (test_probe_marker_judgment) | 47 passed (test_probe_not_proved) | 16 (test_probe_readers) | 14 (test_probe_replay) | 13 (test_probe_target_fact) | 32 (test_probe_walk) ...
python -m pytest test_probe_fix_round.py -q  ->  38 passed in 11.57s
```
(the remaining files of that list — test_probe_walk_edges, test_probe_word_repeat, test_reducer_supersession, test_reference_window, test_s5_window_leftovers, test_scenario_walk, test_scenario_world — all ended `exit=0`; the full log of 33 `exit=0` lines was grepped: `grep -c "exit=0"` printed 33, `grep -B4 "exit=[1-9]"` printed nothing.)

After merge 3: `test_artifact_supersede 71/71`, `test_codex_tool_guidance 217/217`, `test_controller_rework_scope 171/171`, `test_fixes_13797 70/70`, `test_guard_big_read_sections 248/248`, `test_guard_command_text 197/197`, `test_guard_window_files 103/103`, `test_refusal_registry 504/504`, `test_s5_window_leftovers 148/148`, `test_source_stage_integration 21/21`, `test_test_locations 506/506`, `test_guard_write_owners 549/549`, `test_judgment_census 25/25`, `python -m pytest test_guard_project_knowledge.py -q` -> `10 passed in 0.76s`, `test_codex_host` and `test_doctor_access` `OK`.

After merges 4 and 5: `test_check_coverage 38/38`, `test_case_store 14/14`, `test_detector_verdict 209/209`, `test_pinned_lifecycle 51/51`, `test_arch_check 42/42`, `test_test_files 190/190`, `test_test_locations 506/506`, `test_validators 343/343` (slow files of the print — test_console_encoding, test_install_paths, test_install_retire, test_read_json, test_protected_test_path — not run locally).

After merge 6 (repo root): `python -m pytest tools/test_lint_ratchet.py -q` (the file that judges `lint_ratchet.py`): first `1 failed, 25 passed in 58.86s` (the baseline row above), after the named re-measure `26 passed in 66.01s`; `python -B tools/lint_ratchet.py --check` printed the 10 new findings before, none after.

Gates: `( cd .../wave7/ai-packages/qa-factory && python -B scripts/selftest.py --limits --lang )`: `PASS limits: every mandatory role rule of design/role-rules.json holds in its carrier` ... `=== qa-factory selftest: 4/4 ok ===`. `( cd .../wave7 && python -B tools/piles.py check --all )`: `piles check: ok`.

## Pile statuses (`python -B tools/piles.py status ... --task t-672`, as in the statuses-fv1 report)

```
piles status: live-run-fvf/1 FV1-18 set to принято: 7aee0ca (t-672).
piles status: onboarding-forge/4 OF4-3 set to принято: d264a3c (t-672).
piles status: onboarding-forge/5 OF5-8 set to принято: 8120503 (t-672).
```
One «Ход» line each in `live-run-fvf/batch-1`, `onboarding-forge/batch-3` (OF3-2), `-batch-4`, `-batch-5`. OF3-2: the node row exists, but K6 is one part of a phase node whose K1..K5, K7, K8 are not in main; status left «ожидает», a «Ход» line says what K6 covers (same reading as OF3-1 in the statuses-fv1 report). P1-a N4: no node row found by id in any batch file (`grep -n "P1-a\|P1A\|lint_ratchet" plans/piles/*/batch-*.md` finds only mentions of the tool and registry rows), no line written. OF4-3's row says "after OH3-9 and OH5-7" merge; I did not check those two, the status follows the spec's instruction.

## Pipelines

- Run 43533215100 (push of 1517fe9, the first push): `cancelled` as a whole (main moved: a newer push came in), jobs: forge-check cancelled, runner-facts success, changes success, package-fast failure (the `test_stage_joints` K4 line above).
- Pre-existing reds on main named by id: run 43530728622 (eb6dd02, forge-check: `journal_validator.py --all --base` 9 violations in old lines of `logs/journal/dev1.jsonl` since ef0bdf4; t-678 report) and canon 43529668006 (main 6997034). Not from this wave.
- t-678 (another builder) fixed main-red items meanwhile (2c4ee8d, e1fcfdf, report `20261114-main-red-report.md`); I merged origin/main into the branch (aab9933) before pushing the told-ratchet row, no conflict.
- Run 43533986369 (push of 32f9c3e, the last code commit): `success`, read to its end once: changes 132258473928 success, runner-facts 132258474148 success, forge-check 132258474264 success, package-fast 132258546275 success (the `test_stage_joints` K4 row is green with the raise). The commit that adds this report is docs-only; its own run was not waited for. The BATCH CANON (full sets) was not run by me; it is the coordinator's.

## Defects found against accepted branches

- `wip/fv118-fix`: unused import `execution_request as er` at `test_execution_request.py:2063` (FV1-18 N2 round). Baselined, not repaired; remove it in a fix round and lower the baseline (UnusedImport 1 -> 0).
- `wip/of4-3b`: `check_coverage.py::main` bare 12 -> 13 without its told-ratchet row.
- `wip/p1a-n4`: its HandReaderInput baseline was measured on a tree older than main; main's own newer `plan_row` hand inputs were 9 over it. The line's purpose is "only goes down": the 9 raised rows are the debt to pay down (FV1-30b tests among them).

## Analogs noticed (report only)

- `docs`/`test_probe_by_code_languages.py`: main's PC3-2 split leaves branches cut before it with a modify/delete conflict on this file; other old `wip/fv1*` branches that touched it will hit the same one.
- Slow files that judge a ratchet (`test_stage_joints` K4) show up only on CI; a branch that adds a bare site to a role-reachable unit cannot know locally. No scenario_walk row warns about it.

## Not merged

Nothing from the list. Branches outside it (`wip/fv1-22r-*`, `wip/sc-*`) untouched.

## Needed beyond the manifest

`tools/lint_ratchet.py --help`, `tools/test_lint_ratchet.py`, `tools/piles.py status --help`, `ai-packages/qa-factory/scripts/slow_tests.json`, `ai-packages/qa-factory/scripts/tests/fixtures/told-ratchet.json`, `docs/tasks/specs/reports/20261114-main-red-report.md`, `plans/piles/onboarding-forge/batch-{3,4,5}-*.md`.
