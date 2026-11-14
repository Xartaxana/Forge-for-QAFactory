# t-861 B1 fix round: handoff

Worktree `.claude/worktrees/offload-b1`, branch offload/b1, commit 7217de57 (base 3f7760ad), pushed. Only `tools/journal_write.py` and `tools/test_journal_write.py` changed; `journal_lock.py` untouched. B0's unstaged files were not staged.

## Witness

Command: `( cd C:/QAFactory/forge-repo/.claude/worktrees/offload-b1 && python -m pytest tools/test_journal_write.py tools/test_streams.py -q -p no:cacheprovider )`

```
........................................................................ [ 59%]
..................................................                       [100%]
122 passed in 37.88s
```

(test_streams S3, red before, is now green.) Sizes: journal_write.py 850, journal_lock.py 170, test_journal_write.py 560 lines (tests stay under product).

`git show --stat HEAD`:
```
 tools/journal_write.py      | 212 ++++++++++++++++++++++++++------------------
 tools/test_journal_write.py |  64 ++++++++++++-
 2 files changed, 184 insertions(+), 92 deletions(-)
```

## Per finding

- F1 fixed (`test_e_b1_5_a_clone_of_another_developer_scans_only_its_own_journal`): `scan_worktrees(root, rel)` reads only `current_path` + seed per worktree via `read_journal` + `jk.max_by_letter`; `TASK_IN_JSON_RE` dropped. Residual (worktree bases more than 1000 apart; door `event --json`) is in the module docstring.
- F2 fixed (`test_e_b1_6_a_failure_after_the_append_is_still_written_with_a_counter_warn`, `test_save_counter_retries_a_refused_replace_for_a_moment`): (a) a save failure after the append gives written=True plus "WARN counter not updated: ...; the next call takes max(counter, file)"; (b) the out-of-lock counter read is gone: `_locked_counter` reads inside the lock and, when a scan is needed, releases the lock, scans, retakes it (the in-lock file wins if another process wrote it meanwhile); `save_counter` retries `os.replace` on PermissionError for 1 s.
- F3 fixed: private loop replaced by `streams.utf8_stdio()`; test_streams green. B23's DoD must carry the axis-15 chain decision and the hook-notes cap (critic's note).
- F4 fixed (`test_a_linked_worktree_of_the_claiming_clone_copies_the_row_and_keeps_the_letter`): main registry holds this clone "a" and another dev1 clone ""; the linked claim prints 'a'.
- F5 fixed (`test_f5_an_unknown_task_on_accept_gets_the_validators_door_not_the_new_id_door`): `_check_new_task` only for `delegated` / `decomposable` (`NEW_TASK_EVENTS`); other events do not even load the counter.
- F6 fixed: the `returned` lookup is `_fill_returned`, run inside the locked read of `_write_event`; the CLI builds the object with given values only (existing returned test still passes).
- F7 fixed (`test_f7_a_run_for_an_unknown_task_is_refused_before_the_command_runs`): `_precheck_task` (grammar, then seen-or-at-most-counter; unlocked, advisory) runs before `run_witness`; asserted by a touch-file that never appears.
- F8 partly fixed, inside journal_write: one `check_notes` (used by `_accept_obj` and `_prepare`); counter-key and letter-enumeration validation use `jk.parse_id`; `TASK_IN_JSON_RE` gone. F8 remainder for Fable (needs editing journal_keys/piles/validator): move `ID_GRAMMAR_TEXT`, the "not canonical" text (also `journal_validator.py:1352`, `piles.py:3257`), `fmt_id` and `ID_NUMBER_MAX` into journal_keys beside `is_canonical`, and have piles and the validator import the texts; then journal_write imports them (today these four are still local to journal_write).
- F9 fixed: `--period` / `--events-reviewed` removed (parser, `_event_from_args`, EVENTS test row; the period goes in notes).

## Deviations and notes

- The `returned` category warning for an unknown agent ("no category row") is no longer printed (category comes from the matching delegated, else the agent row, else "other").
- The F7 pre-check runs only with `--run` (as the finding states), not for `--witness*`.
- Siblings noticed: none beyond the F8 remainder. Needed beyond the manifest: `tools/streams.py`, `tools/journal_keys.py` (read only).
