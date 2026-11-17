DoD: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/run_suite.py` + `test_node_ids.py` + `test_console_encoding.py`

## Output
(from the worktree, once at the end; tails)
- scenario_walk --witness-for run_suite.py: tail is the `keep ...` lines (last: `scripts/run_suite.py: keep test_window_record.py (layer gate_named, covers it)`), exit 0
- test_node_ids.py: `=== test_node_ids: 246/246 ok ===`, exit 0
- test_console_encoding.py: `=== console encoding: 116/116 ok ===`, exit 0
- `test_run_suite_*.py`: quarantined, not run -- judged by the batch canon (`test_run_suite_mine.py:1692` M-B1 checks the substring "collect failed: banner" via check_in; still a substring of the new note).

## What changed
- `ai-packages/qa-factory/scripts/run_suite.py:1850` (`verify_node_ids`): note is now `"node ids were not verified: collect failed: " + str(checked["collect_error"])[:400]`. The `[:400]` cut, the `if checked.get("collect_error")` guard (E2: empty/absent -> no note) and all exit codes are unchanged.

## FR walk
- D (FR-59): the collect-error note now says "not verified", names what was not established; the run goes on as before.
- F (FR-41): an unknown is no longer reported as a fact about the ids.
- A, B, C, E, G (FR-30 English, FR-29): not touched / English only, no control bytes.
- AR-28 kept; AR-29: no judgment, a note's words (`judgment: none`).

## Deviations / questions
- Q1: the spec asks for "one row in `test_node_ids.py`'s existing table" (E1: rows AT 400 and beyond). Reality: `test_node_ids.py` never imports or calls `run_suite` / `verify_node_ids` (case-insensitive count 0), has no table over the note, and is not in `owns`. The note is only covered by quarantined `test_run_suite_mine.py` (M-B1). No test row written; I did not invent a harness. Needed from the coordinator: where the row goes (extend owns to test_node_ids.py with an instruction how to reach `verify_node_ids`, or name the test file that does).
- Red-before-change therefore not shown.

## Needed beyond the manifest
- `ai-packages/qa-factory/scripts/tests/test_node_ids.py`, `test_run_suite_mine.py:1692` (read only).
