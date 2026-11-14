# Wave 8 integration report (t-700)

Merges (no conflicts in either):
- 379f687 Merge wip/fv1-22r-fix (00cfc1c): FV1-22 N1+N2+N3, fix round, continuation, SIBLING_MAP axis 37.
- 67a6c5d Merge wip/find-fable-sub (34cb7d2): FG7-33, documents only.

Edits by the integrator:
- stage_done.py `record_acceptance` docstring: "built from the form's header verdict word" -> "built from the verdict word read at the path `handoff.acceptance_verdict_path` names and the form's ..." (text only, found at line 961).
- batch-1-live-run-fvf.md: FV1-22 status -> `принято: 379f687 (t-700)`, one «Ход» line.
- NAMED RATCHET RAISES (AR-20), owed by the merged branches (A22 red in test_audit_rules.py after the merge, 375/375 after):
  - `ratchet_tokens` qa-failure-analyst 18426 -> 18769; qa-doc-scribe 17944 -> 17971
  - `process_ratchet_tokens` qa-failure-analyst 16401 -> 16744; qa-doc-scribe 16943 -> 16981
  (slices qa-failure-analyst / qa-doc-scribe grew with the FV1-22 consumer-acceptance form.) qa-runner measured below its row (16,026 vs 16124): not lowered, shrink is the Lead's call.

Witnesses (python -B scripts/tests/<file> from ai-packages/qa-factory):
- scenario_walk --witness-for <37 changed package paths> named 122 files. Run: test_audit_rules.py after raises: `=== audit rules (A1/A9/A11/A13/A14/A17/A20/A21/A22/A27): 375/375 ok ===` (before raises 371/375, red = the ratchet rows above).
- rc=0: test_handoff, test_field_producers, test_probe_gap_door, test_probe_not_proved, test_handoff_init, test_null_outcomes, test_judgment_census, test_s7_rejudge, test_selftest_slow_tests, test_selftest_shard; and (first 25 of an interrupted sweep, 90 s cap) test_ahead_cards ... test_infra_failure_stops all rc=0 except the slow ones below.
- rc=124 (90 s cap hit, not run to completion; judged by the pipeline): test_check_delivery, test_gate_brief_and_retro, test_gate_preflight.
- NOT run locally (slow): test_story_run_*, test_controller_*, test_driver_layers, test_scenario_*. The rest of the 122-file list was not run (sweep stopped for time; the pipeline judges it).
- `selftest.py --limits --lang`: `PASS limits ...` x2, `=== qa-factory selftest: 4/4 ok ===`.
- `piles.py check --all`: `piles check: ok`.
- `pytest tools/test_pile_cards_contents.py -q`: `135 passed in 2.44s`.

Late defects: none beyond the ratchet rows. Pipeline state: see the final section.
