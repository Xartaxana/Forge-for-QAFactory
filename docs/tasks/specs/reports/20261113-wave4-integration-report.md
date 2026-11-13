# Wave 4 integration report (2026-11-13)

Branch `wip/wave4` cut from origin/main 819a31f; four accepted topic branches merged `--no-ff` in the ordered sequence.

## Per branch

| order | branch | merge commit | conflicts |
|---|---|---|---|
| 1 | origin/wip/tbw-t1 | c76e08f | none |
| 2 | origin/wip/tq2-1-k2 | 198638f | `references/role-load.json` (qa-automator, qa-code-critic rows, both ratchet objects): re-measured with `role_load.py --all` |
| 3 | origin/wip/cl4-1-n4 | a6add6c | none |
| 4 | origin/wip/p1b-n1 | 9d17dde | none textual; semantic: tbw-t1 renamed the stage-joints, so the driver-exits census went red (see below) |

### Narrow witnesses (verbatim tails)
- tbw-t1: `test_judgment_census.py` -> `=== judgment_census: 25/25 ok ===`; `contract_slices.py --check` -> `slices: 44 declared, all present and fresh; 11 key pages; 12 charters carry a generated digest line`.
- tq2-1: `test_role_load.py` -> `=== role_load ...: 186/186 ok ===` (after the re-measure; 184/186 before); `test_s5_plan_grouping.py` -> `=== test_s5_plan_grouping: 123/123 ok ===`; `test_brief_pack_s5_plan.py` -> `=== test_brief_pack_s5_plan: 250/250 ok ===`.
- cl4-1: `python -m pytest tools/test_collect_intake.py -q` -> `76 passed in 14.98s`; census 25/25, role_load 186/186.
- p1b-n1: `dry_exits.py --check` -> `dry_exits --check: 0 discrepancies` (83 before the fixture rename); `dry_exits.py --selftest` -> `dry_exits selftest: 87/87 cases`.
- after the last merge: `selftest.py --limits --lang` -> `=== qa-factory selftest: 4/4 ok ===`; `architecture_index.py --check` -> `architecture index: up to date (29 invariants, 2682 bytes)`; `factory_rules_index.py --check` -> `factory rules index: up to date (59 rules)`; `test_stage_joints.py` (run once, after the last merge) -> `=== test_stage_joints: 292/292 ok ===` (291/292 before the told-ratchet raise below); census 25/25 again; contract_slices fresh.

## Numbers that moved

- `role-load.json ratchet_tokens qa-code-critic 19478 -> 19568`, reason: main +58 and tq2-1 +89 over their merge base 19420 (sum 147, measured +148 from base by ceil rounding); both branches added text to the code-critic's start load.
- `role-load.json process_ratchet_tokens qa-code-critic 17655 -> 17745`, same units.
- qa-automator kept at main's 20313 / 18746 (tq2-1 only lowered its own rows 20257/18687, which main had already raised past).
- `told-ratchet.json s5_plan.py::main bare 2 -> 3` and `s5_precheck.py::check_obligations bare 1 -> 2`: the baseline came in with tbw-t1 (T1b) frozen on the older s5 code; tq2-1 changed `s5_plan.py` (+161 lines) and `s5_precheck.py` (5 lines) after, adding one bare refusal each. RAISE, units of tq2-1. (I read the diff of those two files only for the attribution; the baseline names bare units, I did not count them line by line beyond the test's own measure `bare is 3 / bare is 2`.)
- driver-exits fixture ratchets (lowered, shrink-only): `s1-s4.json unwalked 14 -> 12`, `s5.json unwalked 32 -> 31`; total `unwalked 82 -> 79`. Reason: tbw-t1 renamed the 43 stage-joints (`window:X` -> `acceptance:X`, `exit:X_errors` -> `exit_gate:X`, `detector:Sn:role:tool.py` -> `tool:*`, four `branch_accounting.py` rows collapsed to one); the row keys in `scripts/tests/fixtures/driver-exits/{gates,s1-s4,s5,s6-s9}.json` were renamed to follow, every row keeping `reach: unwalked` and its `why_unreached`. Four old rows have no row of their own now because the universe has one joint where it had four.

## Hand-edited files
`ai-packages/qa-factory/references/role-load.json`; `ai-packages/qa-factory/scripts/tests/fixtures/driver-exits/{gates,s1-s4,s5,s6-s9}.json`; `ai-packages/qa-factory/scripts/tests/fixtures/told-ratchet.json`; fix rounds: `scripts/stage_joints.py`, `scripts/tests/dry_world.py`, `scripts/tests/test_refusal_registry.py`, `agents/qa-case-designer.md`, `plans/features.json`; this report.

## Noticed, not fixed
- Commit-gate WARN (not a refusal) on the p1b-n1 merge: 24 offenders `new package file ... matches no feature` (`scripts/tests/dry_exits.py`, `dry_stub.py`, `dry_world.py`, `fixtures/driver-exits/*.json`, `fixtures/dry-walk/seeds/probe.json`). p1b-n1's own `plans/features.json` does not name them either. It turned out to be a RED on CI (test_forge_metrics), fixed in round 2 by rows in F06 (see Canon).
- Analog of the driver-exits rename: any other fixture keyed by joint names (none found by the tests that ran) would break the same way.

## Canon (bare push pipelines on main, read through `tools/ci_read.py`)

| run | head | result |
|---|---|---|
| 43521701137 | 31610de (the four merges + told-ratchet raise) | RED: `forge-check` (lint_ratchet: 3 new findings, 39 vs baseline 36) and `package-fast` 219/220 (`test_charters_s5_s9.py::test_x1_numbers_only_shrink[qa-case-designer]`); runner-facts, changes success |
| 43523646222 | a9d69a5 (fix round 1) | `package-fast` success (qa-factory fast selftest green); `forge-check` RED: `tools/test_forge_metrics.py::test_k1_shipped_registry_has_no_unattributed_tracked_package_file` (12 p1b-n1 files with no feature) |
| 43525161013 | 97ba490 (fix round 2) | `forge-check` success, `changes` success, `runner-facts` success, `package-fast` skipped (the commit touched only `plans/features.json`; the previous run's package-fast on a9d69a5 was green) |

Fix round 1 (a9d69a5): lint findings `stage_joints.py:863` (unused `_text`), `dry_world.py:16` (unused `import os`), `test_refusal_registry.py:661` (f-string without placeholders) fixed in code, lint baseline left at 36; the `(P16)` tag that tq2-1 K1 added to the `qa-case-designer.md` charter removed (the X1 number ratchet allows 0; rule text unchanged; role-load rows unchanged, verified 186/186).
Fix round 2 (97ba490): `plans/features.json` F06 files gain `scripts/tests/dry_exits.py`, `dry_stub.py`, `dry_world.py`, `fixtures/driver-exits/**`, `fixtures/dry-walk/**` (my choice of F06 "driver headless" as the owner is a feature-assignment guess; the Lead may move the rows). `test_forge_metrics.py` locally 81 passed, 3 skipped.

Not run: the `workflow_dispatch` BATCH CANON (`canon <branch>`) -- the dispatch asked for the push pipeline only; run it if the Lead wants the full set. No red in `test_story_run_s6_w1_frozen` was seen. Defects found against accepted branches (for the Lead's log): tq2-1 K1 added `(P16)` to a charter with a 0 number ratchet and p1b-n1 added three lint findings plus 12 unregistered package files; neither branch's own run caught them.
