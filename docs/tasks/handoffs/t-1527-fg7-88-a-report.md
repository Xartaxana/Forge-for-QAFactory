# t-1527 FG7-88 card A -- report

## Plan items
- `journal_hooks.post_send` + mode `post-send` (2.1): DONE -- tools/journal_hooks.py (docstring line, `post_send`, `_post_send`, `main` branch, silent on the deadline).
- `_find_delegated` resumed rule (2.2): DONE -- tools/journal_hooks.py.
- Validator (2.3): DONE -- tools/journal_validator.py: `EVENTS`, `TASK_ID_REQUIRED_EVENTS`, rule 12 covers `resumed`, `_round_step`, 9f "per round" text (`and no resumed since`), new 9h (`RESUMED_DOOR`), WARN step in `returned_order_warnings` (`returned_refs` replaced by `open_pairs`), docstring (9f, 9h, item 21). `_returned_pair` (dead after the change) removed.
- RESULT PENDING (2.4): DONE -- tools/session_context.py (`resumed_last`), tools/compact_snapshot.py (a `resumed` clears the pair's mark, a later `returned` sets it).
- Tests: DONE -- test_journal_hooks.py `RESUME_ROWS` (7 rows) + payload table (12 rows); test_journal_validator.py `RETURNED_ROWS` +5, `RETURN_ROWS` +2; test_session_context.py +2 rows; test_compact_snapshot.py named test extended (t-003).

## Witness (one run, after all edits)
```
$ python -m pytest tools/test_journal_hooks.py tools/test_journal_validator.py tools/test_session_context.py -q
............................                                             [100%]
820 passed in 111.48s (0:01:51)
$ python -m pytest "tools/test_compact_snapshot.py::test_the_open_list_marks_a_dispatch_whose_worker_returned_and_a_returned_never_closes_it" -q
1 passed in 2.37s
```
Narrow call over the live journal (worktree root, Acceptance 3): `115`. I did not measure main's number (a baseline from `git show` into temp was refused by the hook on the word "journal"); the Lead runs it.
Acceptance 2 Grep `_round_step\(`: def :800 + calls :846 (returned_order_warnings), :1188 (validate_new_lines, HEAD/seed loop), :1400 (validate_new_lines, new-line loop). That is the def + 3 call sites, not 2: validate_new_lines has two (seed and new lines).

## Deviations / findings
1. Rule 2 of the validator requires `category`; the card's field list for `resumed` has none. `post_send` copies `category` from the delegated (else `jw._category(agent)`). Without it every write would be refused.
2. E13 "100000 characters" needs a bound: `AGENT_ID_MAX = 64` (journal_hooks.py, constant after `WARN_LOG`); a longer `to` is no worker, returns `[]` (otherwise the file-name probe raises and the hook prints "NOT checked"). New constant, not a config key.
3. A send outside any git repo (`jw.Refused`) returns `[]` silently (card step 3 is silent on it).
4. `returned_order_warnings`: the owed update on `resumed` is date-gated (`RETURNED_WARN_FROM`), as card 2.3; the round state itself is not gated.
5. `session`: `resumed` copies the DELEGATED's session (F3 (b) makes them equal or one absent).
6. No CHANGELOG fragment: no `ai-packages/qa-factory/` path touched (forge tool), and the fragment path is not in owns.

## Tests not written
- none skipped. `main` mode `post-send` is not driven through `run_main` (the card names the existing F3 deadline test as covering `main`); the `post-send` branch of `main` is untested directly.
- Test lines: +59 +22 +11 +6 = ~98 (hooks 59 incl. helper) against ~165 code lines (hooks 61, validator 85, displays 20 by diff-stat insertions); within budget.

## Noticed (fix the class)
- `calibration_counts.py:85-86` hand-copies the required sets (no `resumed`): the card already names it.
- `hook_liveness_probe` has no `post-send` case (card section 10).
- Mechanism files STAGED, not committed (Lead commits): tools/journal_hooks.py, journal_validator.py, session_context.py, compact_snapshot.py. Committed with the branch: the four test files and this report.
- Needed beyond the manifest: tools/journal_write.py (`write_event`, `_fill_returned`, category rule); validator `_line_form_violations` category check.
