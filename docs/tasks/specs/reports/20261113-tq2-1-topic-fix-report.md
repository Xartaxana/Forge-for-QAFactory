# TQ2-1 topic fix round (F1-F5) - builder report

Branch `wip/tq2-1-k2`. Step 0 merge commit 0d4f777; fix commit follows it (see `git log`).

## Step 0 - merge
`git merge --no-ff origin/wip/tq2-1-n5` -> auto-merged `critic_rollcall.py`, no conflict (K2 hunks :911-925, N5 :95-140, :801-842). K2 hand-rolls no
column lookup, so no K2 line needed to move to `md_column`. `plans/features.json`: taken from origin/main (`git checkout origin/main -- plans/features.json`),
no row added - the commit hooks reported "new rows 0, new package files 1 (all classified)". The branch's copy had lacked one line (the
`probe_by_code_languages_common.py` entry) that origin/main holds; taking main's file restores it.

## Findings -> what changed
- F1 `brief_pack.py` `case_concern_lines`: `asked` is now a SET of `frozenset(group)` -> `k` counts distinct groups. Rows (test_brief_pack_s5_plan.py): B1 fixture now
  carries the token on TC-1 AND TC-2 (still "1 ask", beside the critic's "1 merge hint(s)" in B2); B1b two pairs sharing TC-2 -> 2; B1c group of three -> 1;
  B1d two concerns with no token -> "0 ask", both concerns listed (none dropped).
- F2 `s5_plan.concern_report`: `rounds` counts only rounds of files that are NOT `silent`; `brief_pack`: "none carried" only when no readable round AND no silent
  file; "none raised in N" only when N>0; B6 prints neither (the silent head + files lines say it). B6 `unwanted` gained `none raised`. The three lines stay distinct.
- F3 `brief_pack.held` (removed with the nested def: `elsewhere` now calls `C.names_case(scope, i, cfg)`) and `s5_plan.merge_hints.matches` -> `C.names_case([key], ident, cfg)`.
  G7/B7a green; new row G7b (`TC-10` is not `TC-1`).
- F4 `critic_rollcall.parse_rollcall`: `verdict_at`, `fix_at` via `C.md_column(raw[0], ...)`. Absent column -> None as before (verdict None, fix ""); `case` (startswith)
  and `reviewed` (in) untouched. New table `VERDICT_FIX_COLUMN_CASES` (4 rows: plain, backticks+spaces+case, absent, prefix-not-matched) in test_critic_rollcall_apply_fixes.py.
- F5 `s5_plan.concerns_for_scope`: `not scope` -> every concern `unplaced`, why `"the dispatch names no scope"` (checked before the controller is asked). Rows G10a/G10b
  (empty list, None; plus no concerns) in test_s5_plan_grouping.py. A brief-level row is impossible: the controller refuses to SEND an S5 dispatch with empty scope
  (`StateConflict`, controller.py:5586), so the row calls the function directly.
- Incidental (Q3 trivial, inside the edited lines): `elsewhere` is computed only for the legacy author branch that reads it.

## Ratchets
`S5_PLAN_BRIEF_BYTES_MAX` 9559 before and after (K7 rows green); `role_load` / `role-rules` / charters untouched, `test_role_load.py` 186/186 and `test_role_rules.py` 57/57
green. No ratchet moved.

## Witness (verbatim tails; run from the package dir after the last edit)
`python -B .../scenario_walk.py --witness-for brief_pack.py s5_plan.py critic_rollcall.py` printed 42 files (3 scenario files + keeps). NON-slow ones (slow_tests.json
excluded; the 3 scenario files, `test_story_run_s6_w1_frozen` known red not run) were run in an earlier pass after the F-edits, all ok:
test_ahead_cards 269/269, test_codex_tool_guidance 217/217, test_detector_verdict 209/209, exit gate digest source 94/94, test_field_producers 912/912, test_first_look_briefs 204/204,
test_first_look_wiring 103/103, test_fit_targets 116/116, flow requests 93/93, test_one_source_per_fact 21/21, oracle provenance 296/296, question_register 713/713,
test_regression_scope 93/93, test_s5_plan_windows 104/104, test_walk_plan_fields 123/123, whole identifier 166/166, test_whole_list_sites 292/292, test_brief_s3_roster 12 passed.
Final run after the last edit:
```
## test_brief_pack_s5_plan.py   === test_brief_pack_s5_plan: 250/250 ok ===
## test_s5_plan_grouping.py     === test_s5_plan_grouping: 123/123 ok ===
## test_critic_rollcall_apply_fixes.py   === critic_rollcall_apply_fixes: 51/51 ok ===
## test_role_rules.py           === role rules: 57/57 ok ===
## test_role_load.py            === role_load (the one measure of a role's start load): 186/186 ok ===
## selftest --lang             === qa-factory selftest: 2/2 ok ===
```
Control: the first pass of test_brief_pack_s5_plan.py failed on my own B7c row (the controller refuses empty scope) - the row was replaced by G10; the final run is above.
(test_brief_pack_s5_plan.py is slow-listed, 20 s; run as the DoD names it.)

## FR walk
A - no refusal added (advice only). B - text a person reads: only brief lines of the roles, wording unchanged except counts. C - contracts: `concern_report["rounds"]`
meaning narrowed (readable rounds), sole reader brief_pack updated in the same commit; `names_case` is the one matcher (FR-54/AR-13). D - n/a. E - n/a. F - n/a. G - ASCII, `--lang` green.

## Deviations / questions
1. F1 "a concern with no group tag -> counted as its own group": read as "a concern that does not ask to parametrise is not an ask" (count 0, concern still listed and carried);
   counting it as an ask would print "ask to parametrise" for concerns that ask nothing. Lead to confirm or amend.
2. F2 changed the meaning of `concern_report["rounds"]` (readable rounds only) instead of adding a key; only reader is brief_pack.
## Analogs
Hand-rolled case-key matchers: `git grep -E "ident in C\.case_ids\(|== ident or .*case_ids"` over scripts/*.py -> none left. Queue (verdict Q1-Q3 minus the trivial `elsewhere`) untouched.
