# t-974 — S7 fix round (original t-950), builder report

## Per finding
- S7-1: `check_witness.py` new `has_contract(name)` (`name == "code-review.md" or name in RULES`), placed right after `NOT_CHECKED_NO_CONTRACT`;
  `check_witness.main` reads it (`if not has_contract(path.name)`, then `rule = RULES[path.name]`; code-review.md keeps its branch
  before it, and the predicate carries the same special case). `exit_gate.py`: `import check_witness as CW`; `witness_errors` now
  tests `if not CW.has_contract(art.name)`; the `startswith("not checked: ...")` text test is gone, the consumer matches no advice text.
  Empty/absent name: `witness_errors` returns before (no name -> `[]`), unchanged.
- S7-2: the check lives in `test_exit_gate_unreadable.py` (D8 witness block, its world already drives `witness_errors`; the
  real check_witness runs, nothing faked for the no-rule row). It asserts stdout has `witness not checked: test-plan.md has no
  evidence contract`, no `witness OK`, `errs == []`, and `_STASH[(ROLE,"T-1","witness")]` kinds == `["advice"]`. Control row: a
  ruled artifact (first key of RULES, run faked clean) prints `witness OK`, no `not checked`, files no advice.
  `test_check_witness.py` docstring cut to what the row checks; the `EG.advice_records` call is replaced by a `has_contract` row
  (ruled name, code-review.md, no-rule name, empty name -> True, True, False, False).

## Which assertion catches which mutation (reasoned, not run)
- consumer reverted to always print OK: "the gate says `not checked`" and "never `witness OK`" go red.
- `"witness"` deleted from the `run_advisers` tuple (second commit, Lead's answer): the row now drives `run_advisers` in the same world
  (`_stage_detectors`, `_ticket_of`, `_live_dispatch`, `write_advice` stubbed, nothing else) and asserts the filed records equal exactly
  `[["not checked: no evidence contract for test-plan.md"]]` and the stash key is gone; with the tuple element deleted the filed list is `[]`... in fact `write_advice` is never called and `filed` stays `[]`, so "files the witness advice exactly once" goes red.
- consumer stops stashing: the stash assertion (`["advice"]`) goes red.

## FR walk
A refusals: n/a (no refusal text changed). B: text to a person unchanged (printed line unchanged). C: FR-14 shape of check_witness output unchanged; FR-13: has_contract reads the RULES data row. D: FR-59 held (no contract = not checked). E, F: n/a. G: FR-30 English only, no control bytes; FR-54 siblings below.

## Witness (all inside the worktree)
`python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ...check_witness.py ...exit_gate.py` printed 43 lines (3 scenario, 40 keep) in 26 s.
Fast files, each separately (exit 0): test_check_witness 34/34 3s; test_exit_gate_unreadable 60/60 3s; test_delivery_ownership 310/310 11s; test_detector_verdict 464/464 17s; test_handed_to_person 58/58 5s; test_owner_role_one_list 15/15 1s; test_question_register 945/945 16s; test_dispatch_identity 114/114 6s; test_dispatch_liveness 441/441 5s; test_exit_gate_digest_source 94/94 2s; test_exit_gate_lock_wait 8/8 3s; test_exit_gate_scope 106/106 3s; test_exit_text_end 50/50 2s; test_exploration_identity 66/66 3s; test_first_look_step 105/105 10s; test_hook_lifecycle 25/25 4s; test_host_adapter 95/95 0s; test_reference_window 85/85 11s; test_role_digest 93/93 2s; test_source_stage_integration 21/21 3s; test_stage_of_dispatch 17/17 2s; test_stages 133/133 8s; test_story_run_first_look 26/26 11s; test_then_remainder 354/354 18s; test_validators 343/343 15s; test_whole_list_sites 292/292 7s.
Slow (slow_tests.json), not run: судит канон пачки — test_scenario_cart_1, test_scenario_local_1_0108, test_scenario_local_1_arm_b, test_console_encoding, test_s7_rejudge, test_branch_accounting, test_judgment_census, test_read_json, test_resolver, test_s5_plan_controller, test_story_run_s3_windows, test_words_doors.
First run of test_exit_gate_unreadable was 59/60: my control row used an unruled name (w.json); fixed to a ruled one, then 60/60.
`python -B scripts/selftest.py --limits --lang`: `=== qa-factory selftest: 4/4 ok === ` (2 s). pyflakes on the four touched files: clean (exit 0).

## Needed beyond the manifest
scripts/slow_tests.json; scenario_walk output.

## Analogs noticed
None new. Note: the pre-existing D8 control row (fake clean run on `w.json`) now prints `witness not checked` to stdout, because w.json has no rule; harmless, the assertion there is only `[]`.

## Second commit (run_advisers row)
Re-run once: test_exit_gate_unreadable 63/63 ok, test_check_witness 34/34 ok, pyflakes clean. No new stub beyond four attributes was needed.
