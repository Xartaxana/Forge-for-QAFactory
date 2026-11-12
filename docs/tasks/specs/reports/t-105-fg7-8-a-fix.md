# t-105 FG7-8 part A, fix round (attempt 2)

Paths relative to `ai-packages/qa-factory/` in the worktree `agent-abf432fb6dd127353`. Not committed.

## Items

- F-1 DONE. `gate_brief.still_open`: `QR.matches` runs over ALL dict rows first; `QR.row_answered` and `QR.driver_owned` filters apply inside the loop. Row 2 of an id behind an answered or driver-owned row 1 is now listed (status None, as it stands).
- F-2 DONE. New `question_register.row_answered(row) -> bool` (non-dict -> False); called at gate_preflight.py (`check_open_questions`) and gate_brief.py (`still_open`). The tuple `("answer","answered","resolution")` now lives once, in question_register.py. In gate_preflight.py `import question_register` moved before the `try` so the later call cannot hit a NameError.
- F-3 DONE. `matches` docstring: "by the id stripped of surrounding whitespace, then exactly and case-sensitively, as `load` keys it".
- F-4 DONE. The `except` of gate A resets `settled_rows = [False] * len(questions)` (error toward asking, FR-59), so "every question is checked as it stands" is true.
- F-5 DONE. The "read with problems" note adds " and N more" when more than two problems exist.
- Changelog fragment: one clause added (the vanishing question is now listed).
- test-layers.json: the row's `covers` gained `gate_brief.py` (the test now imports it).

## Red before the fix (new F-1 rows, `still_open` side; run before editing `still_open`)

```
Traceback ... AttributeError: module 'question_register' has no attribute 'row_answered'   (the row_answered test, helper not yet written)
FAIL B-12 F-1 own-answered first row: still_open lists the second row, with no register status - expected [('Where must a moved node appear?', None)], got []
FAIL B-12 F-1 driver-owned first row: still_open lists the second row, with no register status - expected [('Where must a moved node appear?', None)], got []
```
The gate A side of the same rows (1 finding for row 2) passed already, as the critic's probe said.

## Edges, with the test row that shows each (all in test_gate_preflight_question_status.py)

- non-dict rows, no id, id absent from the register: `test_still_open_keeps_its_other_outputs` ("non-dict rows dropped, no-id and absent-id rows listed as they stand"); gate A: `..._no_id_...`, `..._absent_from_the_register_...` (existing).
- `view` None: same test ("view None -> the row is listed as it stands"), and `matches: no view -> nothing`; rows not a list -> [].
- driver-owned first row + a person's second row, register settling the id: the `driver-owned` variant of `test_both_readers_list_the_second_row...` (second row listed by `still_open`, one finding by gate A).
- `row_answered` on a non-dict -> False: `test_row_answered_is_the_one_own_answer_test`.
- No existing test went red, none was edited.

## FR pass

A - refusal texts unchanged; the new notes say what happened and the safe default (FR-1, FR-59). B - no text to a person changed (notes are rehearsal info; the finding text untouched). C - FR-13 n/a, no phrase lists; FR-14 `matches`/`row_answered` shapes are stated in docstrings. D - FR-41/AR-28: no unknown becomes a pass; F-1 removes the one place where it did. E - n/a. F - n/a. G - FR-30 package stays English (changelog, docstrings); FR-31 tests are deterministic, no load dependence.
AR-n touched: AR-13 (one reader/one rule), AR-28.

## Observation (not fixed, not in scope)

The worktree prints "references/test-path-markers.json is missing, unreadable or empty" from `test_files` during test_gate_preflight / test_brief_pack / test_validators; all rc=0. It is not caused by this diff (no file of that name was touched); not verified whether main has the file.

## Witness

`python -B .../scenario_walk.py --witness-for scripts/gate_brief.py scripts/gate_preflight.py scripts/question_register.py` printed the set (3 scenarios + keeps); every fast one was run, plus the three named. Closing lines, verbatim:

```
test_gate_brief_and_retro rc=0 | === gate brief and retro numbers: 975/975 ok ===
test_gate_preflight rc=0 | === gate rehearsal: 1283/1283 ok ===
test_gate_preflight_question_status rc=0 | === gate A: question status from the register: 25/25 ok ===
test_question_register rc=0 | === question_register: 684/684 ok ===
test_scenario_cart_1 rc=0 | === scenario cart-1: 15/15 ok ===
test_scenario_local_1_0108 rc=0 | === scenario local-1-0108: 15/15 ok ===
test_scenario_local_1_arm_b rc=0 | === scenario local-1-arm-b: 5/5 ok ===
test_validators rc=0 | === test_validators: 343/343 ok ===
test_selftest_slow_tests rc=0 | === test_selftest_slow_tests: 124/124 ok ===
PASS limits: SKILL.md / agents / references within size caps
PASS limits: every mandatory role rule of design/role-rules.json holds in its carrier
=== qa-factory selftest: 4/4 ok ===
```
All 45 files run (the printed set minus test_story_run_s6 and test_controller_gate_decision, plus test_selftest_slow_tests) returned rc=0.

## Siblings noticed

None new beyond the verdict's (claim_projector.py:610 last-wins vs first-wins, `statuses_for` per-row hash): not touched.

Needed beyond the manifest: gate_brief.py `still_open`, test_gate_brief_and_retro.py:2888-2941 (the source-inspection test; still green).
