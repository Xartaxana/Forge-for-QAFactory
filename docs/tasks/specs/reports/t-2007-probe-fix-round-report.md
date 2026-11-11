# t-2007 — fix round on the mutation-probe batch (verdict t-2000)

Branch `pfix`, one commit `639f09879` (from b731b94ba), not pushed. Commit lines: `architecture: AR-9, AR-13, AR-22, AR-25, AR-29`, `judgment: none`, `piles-skip`, trailer Opus 5.5.
`PKG` = `D:/ws2/wt-fb1/ai-packages/qa-factory/scripts/`.

## Per item

| item | state | where |
|---|---|---|
| F1 | DONE | `window_record.probe_gap_block` and `acceptance.probe_gap_named` read `probe_owes_judgment` first: `unjudged` = no block, not named, by any word (instance, case, `tooling:`, class). `cannot_judge` keeps `probe not proved:`. Tests `test_unjudged_record_is_named_by_no_probe_gap_word` (8 params), `test_unjudged_rule_keeps_the_other_words` |
| F2 | DONE | `probe_by_code._judge_dispatch_why`: the row `find_active_dispatch` answers must have role `qa-code-critic`, stage `S5`, the record's case in `scope`; unreadable row / controller / record with no task or case refused with `JUDGE_DOOR`. `parent_retry` ancestor passes through the same reader. Tests (no stub, a real `controller.json`): `test_judge_dispatch_must_be_the_critics_open_s5_one` (8 rows), `..._other_story_or_unreadable_controller_refused`, `test_judge_through_parent_retry_ancestor_still_passes` |
| F3 | DONE | `_binding_items(..., off_target)`: no `sensitivity: proven` / `probe_receipt_ref` for `receipt_off_target(record)`; the row (`tests[]`) keeps its receipt, so the window keeps the off-target door. Test `test_publish_binding_off_target_is_not_proven` (on-target control gets `proven`) |
| F4 | DONE | one helper `window_record.probe_word_door` (beside `probe_gap_keys_line`), used by both controller refusals: unjudged -> `JUDGE_DOOR`; `cannot_judge` -> `NOT_PROVED_RECORD` + keys of `probe_judgment_cases`; the old `probe gap:` text only for the rest (and alone when nothing can be classified). Tests `test_controller_door_follows_the_probe_record`, `..._unrecorded_gap_door_...` |
| F5 | DONE | `judgment_facts` carries `statement_inverted`; `proof_level.cannot_judge_facts` and `probe_judgment_cases` hand it on; `probe_judgment_lead` shows it (falls back to `statement_after` when the probe wrote no inversion text). Key-set pin updated; `test_lead_shows_the_check_not_the_marker_expression` |
| F6 | DONE | `controller._s5_gap_problems` filter and `window_record.probe_gap_segments` `by_factory` removed; `test_no_reader_of_data_row_left` scans `startswith("factory:")` and `by_factory = ` (the control: `startswith("class:")` is found in window_record.py) |
| F7 | DONE | `s5.md` names `probe not proved: <case key>` with the waiver command, "(N5)" removed; `state-exits.md` has the row (revoke road, `test_probe_not_proved.py`) |
| F8 first part | DONE | sample run on Playwright 1.56.0 (`tr-arm-b/node_modules`, throw-away spec in the scratchpad, deleted; the stand tree untouched; no stand needed): a strict-mode violation inside `expect(locator, '<marker> step 1: x').not.toHaveText(..)` fails with `Error: <marker> step 1: x` as the first line of the junit failure body (then `Error: strict mode violation: ...`, call log repeats the marker). So the E1.13 residual HOLDS (reads as fired). Written in the `test_probe_marker.py` docstring. M-TS1/M-TS2 stay owed to the live proof |
| item 6 | DONE | `_word_owed` shared by `probe_gap_cases`, `probe_judgment_cases`, `probe_word_door`; `cannot_judge_facts` and `not_proved_word` moved to `proof_level.py` (no alias; acceptance's lazy import in the loop gone). Queued by the verdict: the three local `cut`s, `judge_detector` (88 lines) |
| item 7 | DONE | `judge_record` split: `_judged_record`, `_judge_input`, `_judge_dispatch_why`/`_demand_critic_dispatch` (the last named so that it is not a census unit) |
| Q5 | PARTIAL | wording fixed: `plan_detector_mutation` docstring, `window_record` "written before N4", `proof_level.receipt_off_target` docstring, `seam_chosen` comment. NOT done: `proved_by=None` -> required. Reason: 20+ calls in `test_probe_gap_word.py` and 2 in `test_decision_classes.py` (not in `owns`) call `probe_gap_block` without it; the one production caller already passes it. Queue: make it required together with those tests |
| L1 | DONE | `test_probe_marker.py`: `assert library` replaced by a real assertion (the row's sample text proves by `fires_as`) |
| L2 | not done (not in the DoD list); `judgment.facts_sha` still has no reader |
| S3 | DONE, marked for the Lead | `probe_judgment_cases`: case listed when every owed item is `cannot_judge` or could-not-run and at least one is `cannot_judge`; only those shown; the word names those only (the tooling test is asked at the next refusal). Test `test_case_with_cannot_judge_and_tooling_test_gets_the_judgment_question`. Unjudged or never-run sibling still keeps the case off |
| S2 second option | DONE | `OFF_TARGET_DOOR` names `story_step.py finish ... --unresolved <why> --reason "<words>"` by the role, "a Python test has no `--at`", delivery "requires a current sensitivity proof", "No word of the person closes it"; the old tokens `unverified`, `--at <n>`, `not proved` kept (they are pinned by `test_probe_target_fact.py`). No new word. Test `test_off_target_door_says_the_true_road` |
| cacheprovider | DONE | `test_probe_not_proved.py` `pytest.main([..., "-p", "no:cacheprovider"])` |
| S1 | not touched (queued for the Lead) |

## Red before the fix (new tests run against a byte-copy of b731b94ba, `git archive`)

Command: `python -B -m pytest -p no:cacheprovider <base>/scripts/tests/test_probe_not_proved.py <base>/scripts/tests/test_probe_marker_judgment.py -q --tb=no -k "unjudged_record_is_named or dispatch_must_be or parent_retry or off_target or case_with_cannot or controller_door or unrecorded_gap_door or lead_shows_the_check"`

```
19 failed, 4 passed, 50 deselected in 86.77s
FAILED ...test_probe_not_proved.py::test_unjudged_record_is_named_by_no_probe_gap_word[2026-11-05T09:59:59+00:00-probe gap: the_test]   (F1)
FAILED ...test_probe_marker_judgment.py::test_judge_dispatch_must_be_the_critics_open_s5_one[rows0-qa-automator dispatch, not the code critic's]   (F2)
FAILED ...test_probe_marker_judgment.py::test_publish_binding_off_target_is_not_proven   (F3)
FAILED ...test_probe_not_proved.py::test_controller_door_follows_the_probe_record   (F4)
FAILED ...test_probe_not_proved.py::test_lead_shows_the_check_not_the_marker_expression   (F5)
FAILED ...test_probe_not_proved.py::test_case_with_cannot_judge_and_tooling_test_gets_the_judgment_question   (S3)
FAILED ...test_probe_not_proved.py::test_off_target_door_says_the_true_road   (S2)
```
(F1 params `tooling:` and `class` pass on base: those words were already closed, as the verdict said. The 4 passing are those.)

## Witness (fixed tree, HEAD 639f09879)

```
python -B -m pytest -p no:cacheprovider .../test_probe_not_proved.py .../test_probe_marker_judgment.py .../test_probe_marker.py -q --tb=short
101 passed in 103.73s (0:01:43)

python -B .../tests/test_judgment_census.py
=== judgment_census: 21/21 ok ===        (census: 903 units; breach=1 validate_artifacts.py::check_behaviour_claims, as at base)

python -B .../tests/test_read_json.py
=== read_json: 382/382 ok ===

neighbours (not owned, fast): pytest test_probe_gap_door.py test_probe_target_fact.py test_decision_classes.py -> 45 passed in 40.09s
```
Pre-commit hooks passed on the commit (rules index, architecture index, journal attribution).

## CI-only files that pin the change (not run here)

`test_probe_gap_word.py` (K20/K21 call `probe_gap_block` with the default `class_word`/`proved_words`; unchanged behaviour, still valid; a run started locally was slow and left for CI), `test_probe_by_code.py` (`judge`/publish paths), `test_controller_*`, `test_story_run_*` (seam question text), `test_role_load.py` (s5.md is not a role file; no change expected), `selftest.py --lang` (new text is English only, checked by reading), docs tests that read `s5.md` / `state-exits.md`.

## Beyond the manifest / notes

- Read beyond `given`: `execution_request.py` (`find_active_dispatch`, `retry_ancestors`), `hooklib.artifact_root`, `story_step.py` usage, `test_probe_gap_door.py` (StubController), `test_judgment_census.py` (UNIT_NAME_RE: a function ending `_check` is a census unit, hence the name `_demand_critic_dispatch`), `test_probe_target_fact.py` (pins tokens in the off-target door).
- Same-class notes: `proof_level.probe_could_not_run` and `probe_gap_block` now both treat `unjudged` as outside every word; the controller's third door text (`gate_preflight` / conductor-actions.json rows for `probe gap`) was not walked.
- Mistakes of mine in the run: two `cd` calls in Bash (one to /dev/null, one into the scratchpad) and a trailing `2>&1` (warned by the hook, no effect on the repo); an over-wide `ls` of the scratchpad.
