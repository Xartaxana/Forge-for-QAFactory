# t-932 rules-debt S4 (R9) report

DoD: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/driver_stage_s8s9.py` + `python -B ai-packages/qa-factory/scripts/tests/test_driver_layers.py`

## Output
```
$ scenario_walk.py --witness-for .../driver_stage_s8s9.py   -> exit=0, 78 lines (head / tail)
scripts/driver_stage_s8s9.py: scenario test_scenario_cart_1.py (story cart-1)
scripts/driver_stage_s8s9.py: scenario test_scenario_local_1_0108.py (story local-1-0108)
scripts/driver_stage_s8s9.py: scenario test_scenario_local_1_arm_b.py (story local-1-arm-b)
 ...
scripts/driver_stage_s8s9.py: keep test_window_record.py (layer gate_named, covers it)
scripts/driver_stage_s8s9.py: keep test_words_doors.py (layer detector, covers it)

$ test_driver_layers.py (tail)
PASS [gizmo] L12 the assembled class at module level of the FACADE is legal: L12 has no problem
PASS [gizmo] class null: one line says the class clauses of L3 and L12 are not run

=== test_driver_layers: 283/283 ok ===
```
The witness command lists the covering tests (it does not run them). No scenario or keep row prints the reporter's dispatch prompt (a grep of the tests for the old sentence finds only bench fixtures with a person's words, unrelated): "no scenario or keep row covers" the prompt wording; no new test (spec S4).
`test_story_run_delivery*.py`: judged by the batch canon.

## What changed
driver_stage_s8s9.py:278 (`Driver.run_bug_reporter`): "proposal under qa-factory/bugs" -> "proposal under <task root>/bugs/" (charter agents/qa-bug-reporter.md:57 spelling). Nothing else; the experiment line (:272-273) is untouched (E1).

## FR walk
- E (FR-37): the prompt now names the path the charter and brief_pack name.
- B: no text to a person changed (a role prompt). A, C, D, F, G: not touched (G: English, no Cyrillic).
- AR-13: path taken from the charter's one spelling. E2/F-O6: built on (a); revert together with OH5-9 on (b).

## Deviations
none.
## Questions
none.
## Siblings noticed
`common-rules.md:116` + 11 slices and the `bug_records.py:10` docstring: F-O6, untouched as the spec says.
## Needed beyond the manifest
none.
