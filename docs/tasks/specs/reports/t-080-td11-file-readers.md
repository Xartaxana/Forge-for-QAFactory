# t-080 report: driver-source readers via `story_run.__file__`

| file:line | layer | what the read was for | done |
|---|---|---|---|
| test_person_owned_paths.py:270 (k1) | keep | census: 7 `self.py("waiver.py"` recording sites in the whole driver | `harness.driver_sources()`, bare lines reported as `file:line`; negative control still on `harness.driver_text()`. Count still 7, no new site in driver_*.py |
| test_story_step_manual_block.py:659 (K-T2) | keep | pattern absent anywhere in the driver (`i:i + size`, `_case_obligation_mapping(`) | `harness.driver_text()` |
| test_walk_account.py:121 | keep | count: one `\nWALK_ACCOUNT_TRIGGERS = ` definition | `harness.driver_text()` (added `import harness`); count is still 1; check label "in the module" -> "in the driver" |
| test_no_move_seam.py:1382 | keep | a PATH: `AF.a27_scan(plugin_root)` takes the plugin root and itself scans entry + `driver_*.py` | left |
| test_no_move_seam.py:275 | keep | a path to a doc, not a source read | left |
| test_place_session.py:382, :391 | QUARANTINE | census of one call site in the driver | not edited; for the Lead |
| test_story_run_delivery_c.py:872, :948 | QUARANTINE | source read | not edited; for the Lead |
| test_code_close_behind.py:343 | QUARANTINE | sentence presence in the driver | not edited; for the Lead |
| test_silent_passes.py:922, test_driver_golden.py:887 | keep | non-reads (path to halts.md; sha256 of the entry file) | left |

driver-layers.json: no row changed (L8 stayed 283/283).

## Witness (each file alone, closing line)
- test_person_owned_paths.py: `=== person_owned_paths: 96/96 ok ===`
- test_story_step_manual_block.py: `=== test_story_step_manual_block: 191/191 ok ===`
- test_walk_account.py: `=== test_walk_account: 190/190 ok ===`
- test_no_move_seam.py: `=== no_move seam: 894/894 ok ===` (unchanged file; run to confirm)
- test_driver_layers.py: `=== 283/283 ok` (`[gizmo] L12 ...` lines above it)
- `python -m pyflakes` on the three edited files: exit 0, no output.
- Repeat of the case-insensitive search (`(story_run|SR|sr).__file__`, `getsource(file)?(story_run|SR|sr)`): the remaining hits are only the quarantined files above plus the non-reads (no_move_seam:275/1382, silent_passes:922, driver_golden:887). The control found all given hits.

## Questions
None. The edge cases (new counts over the set, missing pattern) did not occur.
