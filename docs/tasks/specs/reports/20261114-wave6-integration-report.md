# Wave 6 integration report (t-660)

Branch wip/wave6 (cut from origin/main 97ba490), pushed to main by fast-forward.

## Merges
1. `origin/wip/fv1-3` (tip 485db3f) -> merge commit 5f03a39. No conflicts (auto-merge incl. `driver_dispatch.py`).
2. main moved (d5059a5, wave 5: FV1-30b topic, N3, N6, findings) -> `origin/main` merged: commit 2dbd225. No conflicts; `driver_dispatch.py` merged cleanly, both behaviours proven (witnesses below). No ratchet/census file needed a hand move.
3. Added by the Lead mid-wave: `origin/wip/statuses-w4` (10e9fef, t-661, docs only, `plans/piles/**` + one report) -> merged after fv1-3. No conflict, no table-row id collision seen.

Push 1 (first attempt) was refused (main moved d5059a5); re-merged, not forced. Push 2 (fv1-3 + main): d5059a5..2dbd225. `git branch -r --contains 485db3f` -> origin/main, origin/wip/fv1-3.

## Witnesses (verbatim tails), after merge of origin/main
- test_story_run_loop_b_threshold: `=== test_story_run_loop_b_threshold: 204/204 ok ===`
- test_story_run_loop_b_answers: `=== test_story_run_loop_b_answers: 106/106 ok ===`
- test_words_doors: `=== test_words_doors: 710/710 ok ===` (before main merge: 620/620)
- test_window_record: `=== window record: 573/573 ok ===` (before: 487/487)
- `python -B scripts/selftest.py --limits --lang`: `=== qa-factory selftest: 4/4 ok ===`
- statuses-w4: `piles check: ok` (one non-blocking WARN (е): 152 baseline findings), `python -m pytest tools/test_pile_cards_contents.py -q` -> `135 passed in 2.56s`.

## CI
- Canon run on main tip 2dbd225: id 43527732984 (workflow_dispatch). Conclusion and the lines of test_story_run_s0 / test_story_run_s6: see the section "Canon result" below (filled at the end, or "not finished" if the cap ran out).
- Push forge-check run 43527710780 on 2dbd225: failure; jobs forge-check (132237478248) and package-fast (132237541092) failed, runner-facts and changes success. package-fast first failing line: `FAIL tests: scripts/tests/test_controller_blocks.py ... === test_controller_blocks: 368/371 ok ===` ("every block in controller.py has a row in the walk: not walked: _s5_completion_tiers ...; counts agree: expected 351, got 353"). The same two jobs failed identically on wave 5's push d5059a5 (run 43526628004, jobs 132233999533, 132234070718), i.e. before this wave. No file of this wave (driver_*.py, question_stop.py) is on that path; `controller.py` blocks vs walk fixture is wave-5 / S5 completion-tiers territory. Reported, not fixed. The forge-check job log shows only the checkout/cleanup lines through `ci_read log` (first failing step not readable that way).

## Duplicates left by the merge
None noticed.

## Canon result
(see final message; appended after the run)
