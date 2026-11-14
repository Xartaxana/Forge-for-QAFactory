# Wave 5 integration report (t-652)

## Merge order (worktree wip/wave5, cut from origin/main 31610de)
1. origin/wip/fv130b-topic a7c6f06 -> merge 39be4b7 (no conflict)
2. origin/wip/fv130b-n3 9dd9d59 -> merge d01c2a5 (no conflict)
3. origin/wip/fv130b-n6 17915a1 -> merge eb86925 (ONE conflict, below)
4. origin/wip/findings-q 00cd42f -> merge 29991f2 (no conflict; piles rows of wave 4 and findings-q both kept, `piles.py check --all` ok)
5. origin/main moved twice during the work (97ba490, then 586bb7b): merged as d2959b3 and d5059a5 (no conflict, docs / features.json / one charter line).
6. fix round (below) 471ff21, then origin/main (wave 6: FV1-3 etc.) merged, tip 6997034, pushed `wip/wave5:main` as a fast-forward (50d9012..6997034).

Conflict: `fixtures/judgment-census.json`, row `window_record.py::run`. Topic side: roles `qa-code-critic`, class `shape`, owner `data`, note. n6 side: class `xref`, owner `intent`, roles `conductor`. The sides changed disjoint fields, so both kept: class xref, roles [qa-code-critic], owner intent, note (T1a text + "FV1-30b N6: class xref, owner intent"). `test_judgment_census.py`: 25/25 ok after. No other conflict. No ratchet raise by me (role-load, word-passed-facts, contract_slices untouched; `contract_slices.py --check` -> "44 declared, all present and fresh").

Gate notes: the first `git merge -m` stops before committing because the pre-merge-commit hook prints WARN lines (dry-run files unattributed to a feature); `git commit -F` with the trailer lines then passes. My `piles-skip: merge` line is an unknown item to piles.py (items are а-е) - harmless WARN, no rows touched by it.

## Witnesses (verbatim tails)
DoD four (before and after merging main):
```
=== test_words_doors: 710/710 ok ===
=== window record: 573/573 ok ===
=== test_whole_list_sites: 292/292 ok ===
=== test_s5_precheck: 1225/1225 ok ===
```
`scenario_walk.py --witness-for scripts/window_record.py scripts/report_facts.py scripts/waiver.py` printed 61 distinct non-slow files (test_story_run_* and test_controller_* excluded as slow); every one ended `ok` (e.g. `=== scenario cart-1: 15/15 ok ===`, `=== test_third_verdict: 636/636 ok ===`, `=== test_stage_guard: 1683/1683 ok ===`; the four test_probe_* files are pytest-style: 46, 47, 16, 13 passed).
`python -B scripts/selftest.py --limits --lang` -> `=== qa-factory selftest: 4/4 ok ===` (re-run after main merge: same).
`python tools/piles.py check --all` -> `piles check: ok`; `python -m pytest tools/test_pile_cards_contents.py -q` -> `135 passed`.
After the fix round: `=== test_controller_blocks: 373/373 ok ===`; `lint ratchet: 36 findings, 36 in the baseline, 0 new, 0 stale`.
origin/main contains all four tips: `git branch -r --contains origin/wip/<b>` lists origin/main for fv130b-topic, fv130b-n3, fv130b-n6, findings-q.

## CI
Push triggers `forge-check` (run 43526628004 on d5059a5): red on `forge-check` (lint ratchet 1 new: unused `at2`, test_words_doors.py:2118) and `package-fast` (test_controller_blocks: controller walk 351 vs 353, `_s5_completion_problems` -> `_s5_completion_tiers`, `_s5_v2_collect` two duplicated ValueError sites). Both are on this wave's path (controller.py, test_words_doors.py): ONE fix round 471ff21: walk rows renamed/duplicated + header 353, `at2` removed. Pushed with the wave 6 merge, tip 6997034.

Canon (`ci_read.py start --ref main`) on tip 6997034: run **43529668006**, conclusion **failure**. Jobs: start success; full/skip-if-unchanged success; checks/changes success; checks/forge-check success; checks/package-fast success; full/install-smoke success; full/package-full (1) failure; full/package-full (2) failure; test-redundancy, runner-facts, dry-story-spike, quarantine-check, crap-measure, package-full-report skipped.
First failing lines (from artifacts package-full-shard-1/2):
- shard 1: `FAIL tests: scripts/tests/test_driver_layers.py ... 282/283` -> `driver-layers.json L8 holds on the real family (2 problem(s))`: `dry_exits.py:727 in _numbers` and `dry_world.py:326 in drive` each read a family file-name literal (`driver_dispatch`, `story_run.py`) that `source_readers`/`source_mentions` do not declare. Neither file nor driver-layers.json is touched by this wave (both come from wave 4 / p1b-n1) -> NOT on the wave's path as far as I can judge; same failure was in run 43526680756 (before my fix round). Not re-run, not fixed. Not verified whether main before wave 5 was already red here (my scratch worktree of 97ba490 failed to check out).
- shard 2: `FAIL scripts/tests/test_selftest_slow_tests.py 123/124` -> `test-layers.json on the REAL file: every keep row covers the helpers it imports and its owned fixture ['test_stage_joints.py: tests/test_judgment_census.py', 'test_stage_joints.py: told-ratchet.json']`. test-layers.json was changed by this wave's branches (fv130b-topic); judged on the wave's path, but the one fix round is spent and the fix is a layer-map row (a design call about which keep row owns the helper) -> returned, not guessed.
- shard 2: `FAIL scripts/tests/test_story_run_refusals.py 70.9s -> S2: recorded by code ... no question answered by a token` (slow file, not run locally; story_run family; probably on the wave's path via driver_dispatch/story_step). Not diagnosed.
Run 43526680756 (canon on d5059a5, before the fix round) additionally showed the controller-blocks and lint reds above.

## Duplicate helper check (siblings)
Grep for let-go/survivor `def`s in scripts/: one definition (`window_record.py:1217 word_let_go`); no duplicate splitter or filter left by the merge.

## Environment note
The Lead's worktree sweep removed `.claude/worktrees/wave5` twice (and deleted local branch wip/wave5); this report was committed from a fresh worktree on branch `wip/wave5-report` cut from origin/main eb6dd02. Branch tips unchanged.

## Open for the coordinator
1. L8 (driver-layers) red: owner of dry_exits.py / dry_world.py (p1b-n1) or whoever declares them in `source_readers` / `source_mentions`.
2. test-layers.json keep row for test_stage_joints.py must list `tests/test_judgment_census.py` and `told-ratchet.json` (or the import dropped).
3. test_story_run_refusals S2 red: needs a diagnosis (slow file).
Main tip after my push: 6997034 (since moved by others; origin/main at report time eb6dd02).
