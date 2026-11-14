# t-678 main-red report (14.11.2026)

Worktree `.claude/worktrees/main-red`, cut from origin/main eb6dd02. Package paths are under `ai-packages/qa-factory/scripts/tests/`.

## Item 1 test_controller_blocks - already green, no change
Wave 5 fixed it in 471ff21. At eb6dd02: `=== test_controller_blocks: 373/373 ok ===` (run before any edit).

## Item 2 test_driver_layers L8 - fixed
Cause: `dry_exits.py:727-728` (`_numbers`) names `driver_machine.py` only inside a recount command string printed for a person; `dry_world.py:326` (`drive`) builds the path of `story_run.py` for `Popen`. Neither reads the family's source, so no declared reader (AR-13) applies and `source_readers` would be wrong. Declared both in `fixtures/driver-layers.json` `source_mentions` (command text), with the reason per row.
After: `=== test_driver_layers: 283/283 ok ===`.
Siblings: grep of `story_run.py|driver_*.py` in `dry_*.py` finds only these two sites. `dry_stub.py` has none.

## Item 3 test_story_run_refusals - fixed in the test, no code defect
Cause: `refusal_person_words_kept_whole` (test_story_run_refusals.py, scenario (2)+(3)) calls `driver.take_answer` four times on ONE driver at the same boundary `S2:S2-qa-case-designer-1`: the stop answer plus sizes 20000, 21000 and 40000. Each runs a conductor call (`driver_conductor.py:21 CONDUCTOR_CALLS_PER_BOUNDARY = 3`, count in `driver.conductor_calls`, in memory). The 4th call (40000) hits the cap, raising `driver_core.Person` ("the conductor cap was reached") and the run dies mid-file. That is the "S2: recorded by code - no question answered by a token" log lines in the CI log: the last conductor line before the crash. Everything after the crash row is not run, so the following rows appear red. At eb6dd02 locally J-1 20000 and 21000 PASSed and the 40000 call crashed; I could not reproduce "expected 1, got 0" for 20000/21000 on this tree, so I cannot say the CI row text had a different carrier. No claim by FV1-3 or FV1-30b N6 about a different note carrier came up, so no question to return.
AR-24 invariant is kept in the code: all three sized answers are in their note whole and once (PASS lines below). The row itself is stale: it judges the note, not the cap. Fix: in the scenario's local `answer()` helper, `driver.conductor_calls = {}` before each answer, so each answer is its own session. No test row weakened; no code changed. The cap (3) is unchanged and tested elsewhere.
After: `=== test_story_run_refusals: 849/849 ok ===` (full file, about 3 minutes locally, so it is a slow file by wall time: it is judged by the pipeline too; I did not check `slow_tests.json` membership because the file is not at `tests/slow_tests.json`).
Class (not fixed, reported): any scenario answering more than 3 times on one driver and boundary hits the same cap; I found no other.

## Item 4 test_selftest_slow_tests - fixed
Cause: `test-layers.json` keep row `test_stage_joints.py` did not cover `tests/test_judgment_census.py` (imported at test_stage_joints.py:785) nor the owned fixture `told-ratchet.json`. Added `scripts/tests/fixtures/told-ratchet.json` and `tests/test_judgment_census.py` to its `covers`.
After: `=== test_selftest_slow_tests: 124/124 ok ===`.

## Item 5 forge-check - cause found, heals with the next push
First failing step (run 43530728622, job forge-check): `python tools/journal_validator.py --all --base $BASE` -> `logs/journal/dev1.jsonl FAILED validation`. Reproduced with `--base 6997034`: 9 violations in old lines (novelty at lines 903, 958, 1269, 1273, 1275, 1645; ts order at 1113, 1190; repeated delegated at 1191). They entered with ef0bdf4 ("one-time bypass of the journal gate"); the validator judges the lines new since BASE. With `--base ef0bdf4` it passes (no output). The journal is append-only, so I did not touch it. After a push whose BASE is eb6dd02 the step is green.
Later steps checked locally: lint_ratchet (0 new), dup_ratchet (0 new), escape_check, factory_rules_index, architecture_index, agents_md (all up to date), piles check (empty range), install_parity (UNKNOWN 0). `forge_metrics --check` is ok with bases d5059a5, 50d9012, 6997034, HEAD~1: no featureless package file (the twelve candidates are not red at eb6dd02). `python -m pytest tools/test_forge_metrics.py -q`: `81 passed, 3 skipped in 64.75s`. `python -m pytest tools/ -q` (the whole suite) not run locally (CI).
Verdict for the sixth class: none found.

## Witness
- `python -B scripts/selftest.py --limits --lang` (from ai-packages/qa-factory): `PASS limits: SKILL.md / agents / references within size caps` ... `=== qa-factory selftest: 4/4 ok ===`.
- The four test-file outputs are quoted in the item sections above.

## Commits, push, pipeline
See the final lines appended below after the push.
