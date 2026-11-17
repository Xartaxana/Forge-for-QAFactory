# t-951 — rules-debt S8 (X9): the finding scopes as one data file

## Done (items 1-4)
1. `ai-packages/qa-factory/references/finding-scopes.json` (new): `{word: {"meaning", "urgent"}}` for the three words, meanings verbatim from the old `project_decisions.py:44-49`; `local-urgent` is `urgent: true`.
2. `project_decisions.FINDING_SCOPES` is now a lazy `Mapping` (`_ScopeTable`): `{word: meaning}` as before (same shape for every importer, same object imported by the dashboard), read at FIRST USE, never at import (E2). `.urgent` names the urgent words. Failed read: `ValueError` naming the file and its door (restore from plugin), not cached, no code fallback (E1). Missing file, broken JSON, non-object, empty object, a row with no string meaning / non-bool urgent: the same refusal. `_scope_arg` turns it into an `ArgumentTypeError` (argparse would hide a bare ValueError); `_build_parser` no longer breaks every action when the table is unreadable (only `add-finding --scope` refuses, with the door). Measured: with `SCOPES_FILE='nope.json'` -> `REFUSED: the finding scopes cannot be read (FileNotFoundError): ... restore it from the plugin ... nothing was recorded`, parser builds, `add-finding` exits 2.
3. Dashboard: legend and `scope_span` iterate `FINDING_SCOPES`; urgent styling (class `warn`) and the render-findings count key on `FINDING_SCOPES.urgent`, no literal `local-urgent` left in `factory_dashboard.py`. `scope_span` moved to the top of the widget block (the legend uses it). Colours stay in `SCOPE_COLOR` with the grey fallback.
4. Template: prose kept; one wording change in the `upstream-candidate` line ("canon; passing it upstream is a human decision") so the data meaning stands whole inside the line. Data-join rows added inside the existing `row_38_names_the_three_scope_words` of `test_conductor_doors.py`: data file words+urgent flags quoted from the spec; `PD.FINDING_SCOPES == data`; template's three `- \`word\` — meaning` lines name the words in order and each holds the data meaning whole.

## FR pass
A (FR-1): refusal text of `scope_refusal` unchanged; new load refusal says what, expected form, door. FR-4/FR-59: no silent empty list, no code fallback. B: text to a person unchanged. C (FR-13): closed variety moved to a data file. D/E/F: not touched. G (FR-30): English, no control bytes. AR-1, AR-13, AR-3 (no project key, owner 17.11.2026).

## Deviations / decisions to check (the spec was silent)
- Item 2 "same dict shape" vs item 1's `{meaning, urgent}` rows: existing keep tests (`test_project_decisions_refs.py:121,134,220`) read `FINDING_SCOPES` as `{word: meaning string}` and require `FD.FINDING_SCOPES is PD.FINDING_SCOPES`; I kept word -> meaning and exposed `urgent` as a property.
- No urgent row in the data: render findings are not lost, they get a grey slice of their own in the donut and a `—` scope cell (spec silent).
- `local-calibration` is now drawn with an inline colour `#FDB022` instead of CSS class `skip` (urgent keeps class `warn`): presentation only.
- Dashboard with an unreadable data file raises the `ValueError` refusal at render (no fallback, per E1).
- Home row (`selftest.py --homes`): passes with no new row.

## DoD output
`scenario_walk.py --witness-for <four owns>` prints the list (scenario_cart_1, local_1_0108, local_1_arm_b, scenario_walk, scenario_world; keep rows below). Scenario tests and `test_gate_preflight`, `test_http_client`, `test_story_run_refusals`, `test_test_locations`, `test_install_retire`... : scenarios, `test_gate_preflight.py`, `test_http_client.py`, `test_story_run_refusals.py`, `test_test_locations.py`, `test_scenario_walk.py`, `test_scenario_world.py` — judged by the batch canon (not run here).
Run here, verbatim last lines:
```
test_conductor_doors: === conductor doors: 225/225 ok ===   (first run 222/225: my own shadowed variable in the new row, fixed)
test_project_decisions_change_request: 142/142 ok
test_project_decisions_refs: 127/127 ok
test_project_decisions_doc_ref_form: 111/111 ok
test_onboarding_notes 328/328; test_dashboard_cost_gap_rows 9/9; test_retro_numbers 316/316; test_ledger 452/452
test_bug_records 409/409; test_guard_write_owners 549/549; test_onboarding_first_reader 130/130; test_onboarding_markers 8/8
test_project_knowledge 157 passed; test_silent_passes 326/326; test_triage_identity OK; test_field_producers 885/885
test_third_verdict 636/636; test_pinned_lifecycle 51/51; test_sides_ledger 120/120; test_manifest_projection 182/182
test_install_retire 357/357; test_cost_capture_settled 159/159; test_case_key_identity_join 154/154
python -m pytest tools/test_collect_intake.py -q  ->  76 passed in 28.51s
selftest.py --homes -> PASS homes ... 1/1 ok
```

## Analogs noticed
Grep of the three words in non-test `scripts/` finds only command doors (driver_*.py, guard_pre_tool.py, onboarding_first_reader.py, ticket_adapter.py:2947) that pass a word as an argument: names not meanings, non-goals. No other tuple or dict of the three words. Docs: `retro.md:53` and `qa-retro-analyst.md:62` name words in prose (non-goals). `factory-rules-debt.md:84` carries the recorded FR-13 debt row for this constant: the row should now be closed (not touched, outside owns). The stale comment `project_decisions.py` "FR-13 debt" line was replaced.

## Commit
See the final message / `git log` of the worktree branch.
