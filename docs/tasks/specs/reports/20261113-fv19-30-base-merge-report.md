# FV1-19 / FV1-30 topic base: merge of 84f91d7 (FV1-30a) into b3df35d

Conflict: ai-packages/qa-factory/scripts/tests/test_s5_precheck.py, two hunks. controller.py and s5_precheck.py auto-merged.

Hunk 1 (new test functions, before `main`): HEAD side (b3df35d) added `OB_AUTO`, `OB_MANUAL`, `ROW_FIELDS_DONE`, `refs_story` and `fv1_19_obligation_refs_at_the_precheck` (FV1-19 N2). The 84f91d7 side added `_with_words` and the three FV1-30a functions `a_word_by_tag_passes_every_family_but_the_two_that_wait`, `one_road_selects_the_word_for_the_finding`, `the_result_carries_the_word_passes_and_the_helper_reads_them`. Both kept whole, HEAD block first. The two blocks shared one trailing `finally: cleanup(root)`; the HEAD function got its own copy so each function is complete. No row dropped, no assertion changed, no same-row edit.

Hunk 2 (`main()` call list): HEAD's call `fv1_19_obligation_refs_at_the_precheck()` first, then the three FV1-30a calls.

## Witness (from package dir of the worktree, tails verbatim)
- test_s5_precheck.py: `=== test_s5_precheck: 1144/1144 ok ===`
- test_words_doors.py: `=== test_words_doors: 620/620 ok ===`
- test_manifest_put_merge.py: `=== test_manifest_put_merge: 333/333 ok ===`
- test_obligation_join.py: `=== obligation join (TP2-2553): 48/48 ok ===`
- test_judgment_census.py: `=== judgment_census: 24/24 ok ===`
- selftest.py --lang: `=== qa-factory selftest: 2/2 ok ===`

Reds: none, so no parent comparison was needed.
