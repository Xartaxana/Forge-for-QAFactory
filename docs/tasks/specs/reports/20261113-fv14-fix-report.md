# t-534 fix report: FV1-4 topic F1-F4 (branch wip/fv14-fix)

- F1 done: `brief_pack.py` build head: the repair reason (was `_short` 200) and the purpose (was `_short` 300) go through new `_head_words` -> `_words_block`. Rows in `test_brief_pack.py` `p4_build`: AT 200/300, +1, 10x (wrapped, lines joined == text), a line break, a text over 1000 characters.
- F2 done: `test_brief_pack_timeout.py` restored to cf4dede bytes (`git diff cf4dede -- <file>` is empty, 0 bytes). K-B5/K-B6 behaviour is already pinned in `test_brief_pack.py` `n2_summaries_name_their_whole` (timeout entry 120/121/1200, timeline 3/4/30 profiles), so no rows moved.
- F3 done: `test_brief_pack.py` main, 4 rows on `answers_of`: 20 000 + marker re-worded; 19 999 + marker kept; marker not at the end kept; 10x re-worded.
- F4 partial: (a) N1 report written, `docs/tasks/specs/reports/20261113-fv14-n1-report.md`, with S5 + 12 ROLE ratchet runs on this tree (all 12 tight, none lowered). (c) N2 fragment reworded (repair reason claim); `fv1-4-no-brief-cut.md` already says `bytes` only. NOT done: `changelog.d/p1v-n3-brief-sizes.md:2` (still announces `{ts, stage, role, dispatch, bytes, budget_bytes, ceiling, over}`) and the N0 report copy (b): neither path is in this dispatch's owns. Question below.

## Decision to confirm (fork the spec leaves open)

`_words_block` marks a wrapped text with a `_Pointer` whose note names `<decisions>`. The head has no side file carrying the dispatch reason/purpose, so a wrapped head text there would name a file never written. `_head_words` therefore drops that note (`WORDS_WRAPPED_NOTE`) for the head: text whole, wrapped at 1000, no pointer. Alternative: add the reason/purpose to the decisions side file. Not done; Lead decides.

## Witness (verbatim, from this tree)

```
python -B .../tests/test_brief_pack.py                 -> === test_brief_pack: 1112/1112 ok ===
python -B .../tests/test_brief_pack_s5_plan.py         -> RATCHET S5_PLAN_BRIEF_BYTES_MAX 9520 / === test_brief_pack_s5_plan: 213/213 ok ===
test_first_look_briefs 204/204; test_fit_targets 116/116; test_walk_plan_fields 123/123; test_whole_identifier 166/166;
test_s5_precheck 983/983; test_readiness 314/314; test_flow_requests 93/93
test_role_load 169/171 (K10-b, K10-c qa-failure-analyst: pre-existing)
git diff cf4dede -- test_brief_pack_timeout.py -> empty
```

Slow files of `scenario_walk.py --witness-for brief_pack.py` (test_story_run_*, etc.) and others left to CI; test_s3_roster/bug_records/codex_tool_guidance/regression_scope/story_step_start not run.

## Siblings

No slice missed beyond the critic's table. Noted: `brief_pack.py:2528` (`_text_whole(reason)`) already whole.
