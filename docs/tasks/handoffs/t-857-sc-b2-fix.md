# t-857 report: SC-B2 fix round (wip/sc-b2, commit 2c0a6ac7, pushed)

Done (all in worktree agent-a98af5a726eebee89):
- F3: `driver_stage_s6.consumer_gap` checks `consumer_person_pass(stage, author)` right after resolving the author; True -> prints "a person's word passes it; no gap", returns False (no record, no warning).
- F4: `driver_stage_plan.stage_acceptance_write` tags only the `question_register.py --raise` Refusal with `step = "questions"` (attribute only, re-raised). `consumer_form_write` re-raises a tagged refusal.
- F5: `consumer_form_write(stage, dispatch) -> str` used by `consumer_completion` and `consumer_settled` (settled: gap, return True).
- F6: `consumer_no_round_why(stage, counted, cap) -> str` replaces both copies.
- F1 (B2g): `gate_brief._pipeline_warnings(task_root, pipeline)` (the one reader, extracted from `collect`), `_warning_lines(warnings)` (extracted from `_tail_sections`; gate A text unchanged), `render_gate_b` adds the block before `filing_line`; no warnings -> no block.
- driver-layers.json rows for the two helpers; changelog fragment updated.
- Rows: G8b, G4c, G4 "settled form-refused", G6c re-pointed to `render_gate_b("QA-9", packet)` (+ a no-warnings no-block check).

## Witness
New function alone (scratch call of `test_consumer_gap_road` via run_scenarios; the file has no selector and is slow, 218 s, so the whole file was not run):
`=== s6 gap road alone: 73/73 ok ===`

Fails on the old code (byte-copied old product files in, then restored; sha256 of restored files equals the saved new ones):
- all three old: `FAIL S6 G4c ... got (False, {... 'quote': "gap: the failure analyst's acceptance form was refused: the question has no title: (no quote)"} ...)`; `FAIL S6 G8b ... got ('INNER', ['record', 'warn'], ['S6 was accepted with a gap: ...'])`
- old gate_brief only: `FAIL S7 G6c s7-gap-after-scribe-brief-reaches-gate-b — 'S7 was accepted with a gap' not found in:` -> `=== OLD gate_brief: 72/73 ok ===`
- old driver_stage_s6 only: G4 settled form-refused raises `driver_core.Refusal: the form lacks its quote` (Traceback).

Other runs (cwd in a subshell, `scripts/tests`):
- `test_gate_brief_and_retro.py`: `=== gate brief and retro numbers: 1090/1090 ok ===`
- `test_gate_brief_attachments.py`: `=== test_gate_brief_attachments: 203/203 ok ===`
- `test_driver_layers.py`: `=== test_driver_layers: 282/283 ok ===`; the one FAIL is `L11 ... scripts/retro_numbers.py:2843 imports the family part driver_dialog` - a file this round did not touch (git status: only my 4 files plus the 3 scripts and fixtures); the new rows pass. Not verified on the base commit.
- `selftest.py --lang`: `=== qa-factory selftest: 2/2 ok ===` ; `--limits`: `=== qa-factory selftest: 2/2 ok ===`
- commit hooks: factory rules index, architecture index, AGENTS.md up to date; WARN ok.
- `scenario_walk.py --witness-for` lists many files for driver_stage_s6.py (all "keep", detector/gate_named); I ran the fast relevant ones above, not the slow ones (test_story_run_s6.py, per slow_tests.json; judged by the batch canon).

## FR pass
A - no refusal text changed except the new gap why (names what was refused). B - no person-facing question form changed; gate B gains the existing warnings block. C - FR-12: no text filter; FR-14: gate A text byte-identical (`_warning_lines` same lines, `str(w)` cast only). D - n/a. E - FR-10: the S7 gap now reaches gate B. F - n/a. G - FR-30 English (selftest --lang ok), FR-54 siblings below.

architecture: AR-13, AR-14, AR-15, AR-24, AR-27 (as in the commit). judgment: none.

## Test vs product lines
Product: driver_stage_s6.py +~27/-12, gate_brief.py +~22/-12, driver_stage_plan.py +4/-1. Tests: +~35 in test_story_run_s6.py.

## Siblings / notes
- Quarantined `test_stage_acceptance_consumer.py` (Rig.BOUND uses `consumer_exhausted`) will error at Rig construction - not run, not edited.
- Queue (critic): `driver_accept_write` duplication with `person_pass`; refusal-flatten idiom now has more copies in `driver_*.py` (consumer_form_write adds one); named function instead of `(_ for _ in ()).throw` in the test; F9.
- Needed beyond the manifest: `acceptance.py` (consumer_dispatch), `driver_core.py` (Refusal), `tests/test_driver_layers.py`, slow_tests.json.
- Deviation: `render_gate_b` takes `(task, root)`, so the test's `packet` is the root path (same as the old collect call).
