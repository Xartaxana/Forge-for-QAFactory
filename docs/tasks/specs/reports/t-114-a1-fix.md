# t-114 A1 fix round (attempt 2) -- report

Items 1-8: all DONE.

1. B1: `_compact_age` = max(mtime age, header `written` age); `written` absent/unparsable -> untrusted -> never fresh (shown age = mtime's); future written -> 0. Rows: written_65_min_ago_mtime_refreshed, other_sessions_old_file_mtime_refreshed, written_unparsable, written_absent_from_header, written_in_the_future_mtime_decides.
2. B2: record written via `dod_track._atomic_write_text` (imported). Unreadable/not-list record -> MISSING + `_compact_rebuild` rewrites a valid list of all hook snapshot names; line says "rebuilt now with the N snapshot(s) present; the next compaction reads it"; if the rewrite fails: "could not be rebuilt (...) -- delete .claude/compact_seen.json; the next compaction writes it again". Rows: record_corrupt, record_not_a_list (now rebuilt), record_corrupt_next_compaction_works (mode heal: second call with a new snapshot shows it fresh), record_corrupt_and_not_writable.
3. F1: `.gitignore` line `.claude/compact_seen.json` after `.claude/dod_track/`.
4. F2: `_write_announced` re-reads and merges (union, order kept, last 200) right before the atomic write; test `test_a1_write_announced_merges_what_another_session_wrote`. Residual: two writes in the same instant can still lose an update; errs toward "fresh once more" (stated in the code comment) -- NAMED FOR CALIBRATION CHECK 32 (node P).
5. F3: both unavailable returns (`_compact_unavailable`) carry the AFTER COMPACT line; test `test_a1_outer_failure_also_carries_the_after_line`.
6. F4: REMINDER now: newest file of the folder whose first line is not a hook header, whatever its name; COMPACT NARRATIVE names it when newer. Data-join test unchanged and green.
7. F5: row newer_candidate_unreadable_older_still_named (mode newer_unreadable).
8. F6: split into `_compact_candidates`, `_compact_age`, `_compact_chosen`, `_compact_block`, `_write_announced`, `_compact_rebuild`, `_compact_unavailable`, `_exc_text`; `compact_snapshot_lines` is now ~25 lines.

## Changed expectations
- row `record_corrupt`: record afterwards = rebuilt list `["2026-11-12-1257-manual.md"]` (was: untouched raw text); must also contain "rebuilt".
- row `record_not_a_list`: same (rebuilt list, "rebuilt" in block).
- `test_a1_unreadable_file_is_skipped_and_all_failing_is_unavailable`: result now 2 lines (unavailable + AFTER COMPACT), was 1.
- harness: raw-record-untouched assertion removed (replaced by the uniform `_a1_record == record_after`, corrupt record returned as raw text); `unwritable` mode refuses names starting `compact_seen.json` (the atomic writer's temp file); `_a1_put` accepts an optional 4th item (written minutes-ago / raw text / "absent"). Every other row unchanged and green.

## Red before the fix (B1 rows, new test rows, old code)
```
FAILED test_a1_compact_block[written_65_min_ago_mtime_refreshed]
FAILED test_a1_compact_block[other_sessions_old_file_mtime_refreshed]
FAILED test_a1_compact_block[written_unparsable]
FAILED test_a1_compact_block[written_absent_from_header]
4 failed, 2 passed, 255 deselected in 2.13s
```
(e.g. old code printed `COMPACT SNAPSHOT: .../2026-11-12-1155-manual.md (5 min old, trigger manual)` for the 65-min-written file.) The future-written row and one more already passed, as expected.

## Siblings
`tools/hook_liveness_probe.py:1356` anchor `COMPACT SNAPSHOT: docs/tasks/compact-snapshots/` (the writer's stdout summary prefix) still matches; untouched.

## DoD run
`python -m pytest tools/test_session_context.py tools/test_compact_snapshot.py -q` (worktree files, --rootdir worktree):
```
316 passed in 84.94s (0:01:24)
```
The timing test passed in this run (no re-run needed). Tests write only under tmp_path. Not committed.
