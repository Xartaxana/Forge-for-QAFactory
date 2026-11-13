# t-531 P1-v fix round (FIX-2, FIX-3) report

- FIX-2 done: `driver_runner.py` `run_claude`, transient in-call retry of a call that worked now sets `how = "service_cut"` (no `checks` key; the `unclassified` fallback for a caller that names no token is unchanged). Test row `(a) FIX-2` in `resume_kind_row_cases`, next to the R-9 row.
- FIX-3 done: `driver_journal.run_record_names(key, path=None) -> (tuple, note)` beside `run_record`; used by `run_class` and `Driver.resume_kind_of`. One strictness: missing key, non-list, `[]`, any non-string or empty name -> `()` + one note; unreadable file -> the loader's note. Table rows: `run_record_names_cases` (valid list, `[]`, list with "", non-list, missing key), plus "empty name" (and "empty list" for run_classes) added to the existing per-reader table cases.
- Class/siblings: no third reader of run-record.json lists seen (Grep of driver_*.py for run_classes/resume_kinds: only these two). Note text of run_class's key note changed to the shared wording (tests count notes, not text).

## Witness
`( cd <worktree>/ai-packages/qa-factory/scripts && python -B tests/test_driver_stop_record.py )`:
```
PASS (a) FIX-2: the in-call transient retry row is resumed and `service_cut`, with no `checks` key (next to the R-9 row)
PASS (c) run_record_names valid list / empty list / empty name / not a list / missing key: the names and whether one note
=== test_driver_stop_record: 253/253 ok ===
=== task_price: 302/302 ok ===   (python -B tests/test_task_price.py)
```
`scenario_walk.py --witness-for` lists for driver_journal.py: test_scenario_cart_1, test_scenario_local_1_0108, test_scenario_local_1_arm_b (run started in background, did not finish within 120 s on this machine; left to CI), test_driver_stop_record, test_task_price; for driver_runner.py a long keep list (test_story_run_*, etc.), slow ones left to CI.

## Mutation
FIX-2 branch back to `how = ""`: `FAIL (a) FIX-2 ... expected [(False, None, False, 0), (True, 'service_cut', False, 1)], got [(False, None, False, 0), (True, 'unclassified', False, 1)]` -> `252/253 ok`.
Restored by byte copy; sha256 of driver_runner.py before mutation and after restore both `daa71b44c3f4f69808e4bc69c2785aa8f07b0a64241f65d045bae6219df7e799`.

Factory rules walk: A-F not touched in text a person reads; C - one reader function for the list (AR-13/AR-15); G - package English.
