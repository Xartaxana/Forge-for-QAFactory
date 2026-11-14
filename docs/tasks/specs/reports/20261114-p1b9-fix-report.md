# P1B-9 fix round report (builder)

Branch wip/p1b9-fix. W = ai-packages/qa-factory.

## Per item
- S-1: `W/scripts/tests/test_handoff.py`, `the_runtime_record_is_the_windows_own`, five rows added before the final check loop
  (`refs-not-a-list`, `ref-not-a-string`, `ref-absolute-other-story`, `block-without-dispatch-id`, `reparse-of-own-is-newest`).
  They go through `H._runtime_provenance` like the existing rows (which calls `window_runtime_record`). Reasons used verbatim:
  "no evidence_refs", "not a file of this story", "carries a runtime_provenance record" (reason d). The reparse row's copied record
  has a different file name than the original, so the row proves the reparse block was picked. All five GREEN on current code; no
  code change. Count: 670/670 after; 661 before (670 minus 9 new checks: 5 path + 4 reason; derived, base not re-run).
- S-2: `W/scripts/handoff_check.py`: new `_form_dispatch(art, doc)` (before `_findings_file`), used in `_findings_file` and
  `_runtime_provenance`. `_review_receipt` untouched.
  DEVIATION/FORK (spec said "byte-identical for every input"): the two old expressions were not identical to each other for a
  WHITESPACE-ONLY value. `_findings_file` took `form_dispatch or header.dispatch or dispatch` and then stripped (so a "  " in the
  first non-empty key won and became ""); `_runtime_provenance` stripped each key before `or` (whitespace falls through). I used the
  `_runtime_provenance` form (strip each). Absent / None / "" behave identically for both callers as before; only `_findings_file` with a
  whitespace-only earlier key changes (now falls through to the next key). Coordinator: confirm or ask for the other form.
- S-3: `W/handoffs/s5-critic-to-automator.yaml:54` (critic cited :53; found by quoted text) now "The stand the probes ran on: the
  record of this review's own probe run."; `W/handoffs/s5-automator-to-runner.yaml:60` now "The record (read its `result`) the
  freshness verdicts above were taken against." Placeholders/keys untouched. No slice rewrite needed.

## Witness (verbatim tails)
- role-load before: `=== role_load (the one measure of a role's start load): 186/186 ok ===`; after: same line.
- `python -B scripts/contract_slices.py --check` before and after: `slices: 44 declared, all present and fresh; 11 key pages; 12 charters carry a generated digest line`
- `python -B scripts/tests/test_handoff.py`: `=== test_handoff: 670/670 ok ===`
- `python -B scripts/selftest.py --limits --lang`: `=== qa-factory selftest: 4/4 ok ===`
- witness-for handoff_check.py, non-slow files each alone: test_artifact_writers 23/23; test_check_witness 29/29; test_field_producers
  885/885; test_knowledge_notice 15 passed; test_null_outcomes 327/327; test_open_list_fields 15 passed; test_triage_blocked 50/50;
  test_triage_identity OK. Slow (in slow_tests.json), judged by the batch canon: test_brief_pack_s5_plan, test_bug_records,
  test_guard_dispatch_budget_and_logs, test_handoff_inline_values, test_handoff_values_keys, test_handoff_values_main_block,
  test_handoff_values_refusal, test_judgment_census, test_s5_plan_controller, test_s7_investigation_replay, test_story_step_start.
  (test_handoff.py is also slow-listed; run alone per the DoD.)

## FR walk
- A: no refusal text changed. B: no person-facing text. C: contract comments only (FR-38: now true for the role); no contract field changed.
- D: FR-16/17 n/a. E: n/a. F: n/a. G: FR-30 English only; FR-54 siblings: `_review_receipt` queued Q-4, untouched.

## Analogs noticed
- `_review_receipt` (L163) still has header-first order (Q-4, untouched).
