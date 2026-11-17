DoD: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/run_suite.py` + `test_node_ids.py` + `test_console_encoding.py`

## Output
(from the worktree, once at the end; tails)
- scenario_walk --witness-for run_suite.py: last line `scripts/run_suite.py: keep test_window_record.py (layer gate_named, covers it)`, exit 0
- test_node_ids.py: `=== test_node_ids: 251/251 ok ===`, exit 0 (new rows, all PASS: `S5 collect note, short: kept whole` / `AT 400: kept whole` / `401: cut to 400, no cut mark` / `empty: no note` / `absent (None): no note`)
- test_console_encoding.py: `=== console encoding: 116/116 ok ===`, exit 0
- `test_run_suite_*.py`: quarantined, not run -- judged by the batch canon (`test_run_suite_mine.py:1692` M-B1 checks the substring "collect failed: banner", still a substring of the new note).

## What changed
- `scripts/run_suite.py`: new pure helper `collect_failed_note(collect_error)` (just above `verify_node_ids`): `"node ids were not verified: collect failed: " + str(err)[:400]`, "" when empty/absent. `verify_node_ids` calls it under the unchanged `if checked.get("collect_error")` guard. Exit codes unchanged.
- `scripts/tests/test_node_ids.py`: function `collect_failed_note_rows()` (one table of 5 rows, called first in `main`).

## FR walk
- D (FR-59), F (FR-41): the note says "not verified"; an unknown is not reported as a fact. A, B, C, E: untouched. G: English, no control bytes.
- AR-28 kept; judgment: none.

## Deviations / questions
- The Lead's message asked for a 401 row "with its cut mark" and an empty row where "the note still says what was not established". The spec block S5 says: the existing `[:400]` cut stays (no cut mark exists today; none added) and E2: empty/absent -> NO note (unchanged). Expected strings follow the spec; the empty/None rows assert no note. Question: confirm, or the spec block must change (a cut mark / a note on empty would be a design change, not done).
- No red-before run was done for the new rows (the helper did not exist before).

## Needed beyond the manifest
- `test_run_suite_mine.py:1692` (read only).
