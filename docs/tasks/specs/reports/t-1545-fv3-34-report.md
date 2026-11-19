# t-1545 FV3-34 report

DONE: driver_machine.py `take_answer` branch order; test_no_mr_entry.py (new parametrised test, 6 rows); changelog fragment fv3-34-not-built-yet-one-road.md.

Branch order before: ... s0_block -> `halt_free_words and not (S1 + not built yet + no diff)` -> generic `offered` (-> take_seam_answer) -> conductor/refusal -> questions -> `halt S1 not built yet no diff` (_answer_s1_not_built, road 2 only) -> halt stop -> halt/s1_review unread.
After: ... s0_block -> `halt S1 not built yet no diff` (_answer_s1_not_built, both roads) -> `halt_free_words` (carve-out dropped, now redundant) -> generic `offered` -> ... -> questions -> halt stop -> unread. The old late branch was moved up, not duplicated.
Road 2 unaffected by the move: between the old and new positions no branch can match a halt without `offered`.

`_answer_s1_not_built` twice (read from code, not run): stage_done.py --set is issued again with the same keys (only `at` differs) and pending_words[dispatch] is overwritten with the new words. Not changed.
Readers: callers of _answer_s1_not_built: only take_answer (grep).
Siblings noticed: none beyond FV3-37.

Witness:
$ python -m pytest "ai-packages/qa-factory/scripts/tests/test_no_mr_entry.py::test_fv3_34_not_built_yet_one_road" -q
......  [100%]
6 passed in 15.15s

Red-before not run (no stash of old code made).
not run locally: test_no_mr_entry.py (whole), canon judges
