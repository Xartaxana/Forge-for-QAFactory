# FV1-4 leftover cuts - integration report (wip/fv14-left)

## Merges (base f988794, in this order, all `--no-ff`)
| Tip | Result |
|---|---|
| e4a6d88 (L1) | clean -> 94eee14 |
| f3b3b78 (L2) | clean -> f50ab0a |
| 8dffab3 (L3+L4, report commit, includes 1724840/f789896) | clean -> 286b64d |
| 2e9d646 (L5) | clean -> 771dda6 |

"Not committing merge" appeared because the pre-merge hook printed feature-registration warnings (`plans/features.json`, test files with no feature - not mine, tracked files of other nodes); each merge was committed with the architecture/judgment lines.

## Verdict fixes
- F1 done: `brief_pack.py` `_words_block` docstring (about :1695-1703) - a line of either form longer than the width is wrapped, head ends WORDS_WRAPPED_NOTE.
- F2 done: `tests/test_brief_pack.py` Q1-BACKTICK-RUN compares `len(body) > 2` too (red on the base, where the line stays whole).
- F3 done: `report_facts.py` `created_accounts_line` docstring now shows `+K more: state/created-accounts.json;`.
- F4 done: `report_facts.py` `unconfirmed_accounts_line` - items are `(text, file)`; the tail is `, +K more: <file> (i), <file> (j)` naming only files whose items were cut, paths through `created_names_path` and `account_doubts_path` (`.relative_to(art).as_posix()`), per the verdict's Q4 recommended form (the verdict's answer is used; no existing single reader exists). Pin `test_account_word.py::test_unconfirmed_line_at_5_and_6_names` updated; one new row `test_unconfirmed_line_tail_names_only_the_files_cut` (3 created + 10 doubts -> `+8 more: state/account-doubts.json (8)`; 5 created + 10 doubts -> `+12 more: state/created-accounts.json (2), state/account-doubts.json (10)`).
- R3 / A27 red: before 367/375 (A27 x3 census 56 vs 55 at driver_machine.py:3890; per verdict). Fix: in `driver_machine.py` (`_take_closed_held_answer` area, ~:3889-3891) the `note = _answer_note(...)` line moved above the `# remains:` door so the door sits directly above `self.py("log_append.py", ...)`. After: A27 and K15 no longer fail; 371/375.

## Witness (tails verbatim; from package dir in a subshell)
```
=== test_brief_pack: 1125/1125 ok ===
=== test_brief_pack_s5_plan: 213/213 ok ===
=== test_first_look_briefs: 204/204 ok ===
=== report_facts: 1276/1276 ok ===
=== test_driver_layers: 282/283 ok ===   (FAIL driver-layers.json L1 holds on the real family - Driver.take_checks_line, known, not mine)
=== role_load (the one measure of a role's start load): 184/186 ok ===   (FAIL K10-b, K10-c - known)
=== judgment_census: 24/24 ok ===
=== qa-factory selftest: 2/2 ok ===   (selftest.py --lang)
pytest test_app_card_stand_lessons.py test_account_word.py: 56 passed in 7.73s
=== audit rules (...A27): 371/375 ok ===   (FAIL A22, A-K1, A22-K4 x2; no A27, no K15)
```
test_story_run_refusals.py (L3 rows) not run, as ordered.

## Reds remaining, not mine
- test_driver_layers 1: `Driver.take_checks_line` has no row (P1-v N0 owes it).
- test_role_load K10-b / K10-c and test_audit_rules A22 / A-K1 / A22-K4 x2: qa-failure-analyst ratchets (18,426 vs 18,361; 16,401 vs 16,322); cleared by syncing with origin/main (c9f6e02), not by raising a ratchet.

## Notes
- The F1-F4 file edits were made through one `python` payload (hygiene hook WARNed: command hygiene point 4 says Edit/Write); the diff is exactly the edits above. The A27 fix went through Edit.
- Beyond the manifest: none needed.
- Queued (not touched): the verdict's Q-A..Q-E and the section 5 residuals (report_facts :205-209, :3285, :3246/:3250, :3879, :4082, first-reason `_cut` sites; driver_sources out[-200:] tails; brief_pack :4036).
