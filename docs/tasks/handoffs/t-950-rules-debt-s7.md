# t-950 — S7 (W3): "no rule" is not "OK"

## Done
- `check_witness.py main`: an artifact name with no RULES entry now prints `ADVICE — 1` / `- not checked: no evidence contract for <name>` (form 1 (e) of `detector_verdict`), exit 0. The old `OK (no rule ...)` line is gone. `code-review.md` path and the RULES paths unchanged (E3). Empty/absent artifact name: unchanged behaviour of `main` (no argv -> usage, exit 1; non-existent path -> REJECT, exit 1; both before the no-rule branch).
- `exit_gate.witness_errors`: parses the advice through `advice_records` (the one shape), stashes it as source `"witness"` (replaced on every call, reset at the top so early returns leave nothing) and `run_advisers` now pops `("detector", "digest", "witness")`, so the advice is filed as the gate files advice. When the advice is `not checked: no evidence contract...` it prints `witness not checked: <art> has no evidence contract` instead of `witness OK`. Returns `[]` (never blocks).
- `gate-registry.json` row `witness_backstop`: `exempt_reason` text only.
- Test: one new scenario row `no_rule_is_not_checked_never_ok` in `test_check_witness.py` (a `test-plan.md` -> ADVICE, exit 0, no "OK", `parse` reads 1 advice and no defects, gate record `kind=advice`).
- E2 (malformed advice -> `defects`) is the existing contract of `parse`; not touched. E4: nothing rewritten.

## red-before
`python -B ai-packages/qa-factory/scripts/tests/test_check_witness.py` -> `FAIL S7: ADVICE block with the not checked line`, `FAIL S7: and is never printed as OK`, `FAIL S7: the contract reads it as one advice, no defect — expected ([...], []), got ([], [])`, `FAIL S7: the gate's record is advice...`; `=== check witness: 30/34 ok ===` (the exit-0 assertion passed, as it did before).

## FR pass
A (FR-1/4): refusal text unchanged, exit unchanged (fail-open kept). B: no text to a person. C (FR-38): no new requirement, ahead-card unchanged. D (FR-59): the unknown is named, never a pass. E: n/a. F (FR-41): an unknown is not reported as a fact. G (FR-30): English, no control bytes (U+2014 written as an escape in code, same as the contract's header).

## DoD output
`python -B .../scenario_walk.py --witness-for check_witness.py exit_gate.py` prints a list of 37 keep/scenario files; ran them (narrow, per-file, 90 s cap), all green:
```
test_check_witness 34/34 ok; test_console_encoding 116/116; test_delivery_ownership 310/310; test_detector_verdict 464/464;
test_dispatch_identity 114/114; test_dispatch_liveness 441/441; test_exit_gate_digest_source 94/94; test_exit_gate_lock_wait 8/8;
test_exit_gate_scope 106/106; test_exit_text_end 50/50; test_exploration_identity 66/66; test_first_look_step 105/105;
test_handed_to_person 58/58; test_hook_lifecycle 25/25; test_host_adapter 95/95; test_owner_role_one_list 15/15;
test_question_register 945/945; test_read_json 500/500; test_reference_window 85/85; test_resolver 1147/1147;
test_role_digest 93/93; test_s5_plan_controller 101/101; test_exit_gate_unreadable 54/54; test_finish_unreadable 21/21;
test_detector_named_story 102/102
python -m pytest test_judgment_census.py -q -> 25 passed in 121.67s
python -B test_gate_registry.py -> === test_gate_registry: 438/438 ok ===
python -B test_check_witness.py -> === check witness: 34/34 ok ===
```
Judged by the batch canon (over the 90 s cap, not finished here): test_branch_accounting, test_story_step_gate, and the tail of the list after test_s5_plan_controller (test_scenario_*, test_source_stage_integration, test_stage_of_dispatch, test_stages, test_story_run_*, test_then_remainder, test_validators, test_whole_list_sites, test_words_doors).

## Siblings / analogs
- Readers of the literal "witness OK": `grep -i "witness OK"` over ai-packages/qa-factory: check_witness.py (print), exit_gate.py (print), driver_dispatch.py:136 (a comment about history), test_check_witness.py (the new negative assert and one check). No second caller depends on the literal; none in *.md/*.json.
- Noticed, not touched: `check_delivery.py:716-724` and `artifact_producer.py:79` unchanged per spec; `driver_dispatch.py:136` comment mentions "witness OK" as history.

## Needed beyond the manifest
`scripts/detector_verdict.py` (parse/advice), `exit_gate.py` advice stash and `run_advisers`, `gate-registry.json`, `test_exit_gate_scope.py` list.

## Owns note
These three paths are listed in the dispatch `owns:` (given there as main-checkout absolute paths; I wrote the same repo-relative paths in my worktree), so the hook's mismatch looks like a path-prefix artifact, not a real overreach.
owns-skip: ai-packages/qa-factory/references/gate-registry.json -- in dispatch owns (row witness_backstop, exempt_reason text only)
owns-skip: ai-packages/qa-factory/scripts/exit_gate.py -- in dispatch owns (witness_errors; one-line source tuple in run_advisers needed for the advice to be filed)
owns-skip: ai-packages/qa-factory/scripts/tests/test_check_witness.py -- in dispatch owns (the new S7 row)

## Commit
see final message / `git log -1` in the worktree.
