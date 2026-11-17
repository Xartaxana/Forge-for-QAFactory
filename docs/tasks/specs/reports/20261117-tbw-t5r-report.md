# T5r report (t-970, F19): s5_precheck + manifest_put sites

## Done
- s5_precheck.py: 58 refusal sites now build their finding with `_sited(...)` (a literal-id `DV.refusal` text plus `DV.told_fields`); `told` is a key appended LAST. Form-1 text line unchanged; `--json` gains `told` as the last key (EC-6).
- manifest_put.py: 45 sites wrapped with `DV.refusal("manifest_put:<id>", ...)`; problems stay str subclasses (`Record`), joins and JSON text identical. `_MergeRefused.records` mirrors `RequestError.records`.
- OWNS WIDENED BY THE LEAD'S ANSWER (E-T5r-1 option a): exactly two non-owned places, `_judge_words` and `passed_by_judge`, only to keep `told` last (`_told_last`). No other place found that breaks "told last" (grep over s5_precheck copies; `run`, `report`, `main` do not re-serialise findings).
- E-T5r-2: family label unchanged; a row asserts `_names` returns today's value (whole id, tag True; row id, "fix" False). E-T5r-3: recorded-word passing unchanged.
- Changelog fragment: `ai-packages/qa-factory/changelog.d/tbw-t5r.md`.
- Unsited 119 -> 94 (-25). Row ids: manifest, row_fields, bindings, oracle, run_mapping, environment, obligations, plan, sides.declared, sides.settled, sides.placeholders (11) + colliding_ids, novelty, base_outcome, obligation_hash, helper_rows, provisional, unknown_obligation, then_remainder, retract, critic_approval, assertion_line, ghost_rows, revision, expectation_changes (14).

## Site table (function | fragment | id | test row | proof)
| function | sites | id | test row | proof |
|---|---|---|---|---|
| check_manifest | 9 | manifest | tbw_t5r_sites (sides test) | F |
| check_row_fields | 1 | row_fields | same | F |
| check_bindings, check_then_remainders | 9+6 | bindings | same | F |
| check_open_oracle_asserted, check_case_is_oracle | 1+2 | oracle | same | F |
| check_expectation_changes | 2 | oracle family, `_told_last` after pair_at | same | F |
| check_run_mapping | 2 | run_mapping | same | F |
| check_environment (record closure), check_env_evidence | 1+1 | environment | same | F |
| check_obligations | 2 | obligations | same | F |
| check_plan_conformance | 4 | plan | same | F |
| _sides_declared / _sides_settled / _sides_placeholders | 5/7/6 | sides.declared / .settled / .placeholders | same | F |
| _judge_words, passed_by_judge | copies | none (keep told last) | same, key order | F |
| manifest_put 13 ids (45 sites) + revision raise | see summary | manifest_put:<id> | tbw_t5r_sites (merge test) | F |
Proof F = old text start asserted + told_fields check id + non-empty expected. Old/new byte identity of all 11 s5 findings (dict equal modulo told, same key order) and 14 manifest_put texts compared via scratchpad capture before/after.

E6 (code) residuals, left bare, no row listed: unlisted helper sites in manifest_put; `_Window.add` and `plan_result` plan findings in s5_precheck; the printing transport of manifest_put refusals in `run()` (not owned). No design decision needed. Over-claiming rows (EC-8): none found.

## FR walk
A: texts unchanged, expected/door added (FR-1, FR-59 factory-defect sentence for unreadable row). B: not touched. C: FR-14 output additive only. D: FR-16 literal ids. E, F: not touched. G: FR-30 English ASCII, FR-32 tests, FR-54 siblings reported.
Census: no new blocking unit (test_judgment_census 25/25 ok run locally).

## Witness (verbatim)
```
$ python -B scripts/stage_joints.py --check
stage joints: walked exit 8, detector 5, window 27 | rows 267, gaps 4 (producer 2, told 1, demands 1), joints held 4 of 267 | role leg not walked (code-to-code rows): 26 | stages with no detector: S0, S1, S6, S7, S9 | told counters: hand_cards 12, legacy_legs 0, unsited 94
stage joints: clean
(before: unsited 119)
$ python -B scripts/selftest.py --limits --lang
=== qa-factory selftest: 4/4 ok ===
$ python -B scripts/tests/test_judgment_census.py
=== judgment_census: 25/25 ok ===
scenario_walk --witness-for <4 owns>: printed 48, slow 23, quarantined 0, fast 25 (each alone, rc=0):
test_ahead_cards 253/253; test_artifact_supersede 71/71; test_detector_verdict 464/464; test_dispatch_identity 114/114; test_env_evidence 42/42; test_field_producers 885/885; test_handed_to_person 58/58; test_ledger 452/452; test_manifest_projection 182/182; test_manifest_put_assertion_line 20 passed; test_manifest_put_keep_unsent 91/91; test_manifest_put_merge 421/421; test_obligation_join 87/87; test_probe_every_check 319 passed; test_provisional 76/76; test_s5_precheck_sides 200/200; test_scenario_walk 93/93; test_scenario_world 33/33; test_sides_ledger 120/120; test_stand_gap_remedy 34/34; test_state_exits 142/142; test_then_remainder 354/354; test_validator_class 51/51; test_whole_identifier 166/166; test_whole_list_sites 292/292
```
Judged by the batch canon (slow, not run): test_blocked_by_env_window, test_branch_accounting, test_brief_pack, test_brief_pack_s5_plan, test_execution_request, test_gate_registry, test_handoff, test_manifest_from_tests, test_read_json, test_red_window, test_role_commands, test_s5_precheck, test_scenario_cart_1, test_scenario_local_1_0108, test_scenario_local_1_arm_b, test_stage_guard, test_story_run_loop_b_answers, test_story_run_loop_b_loop, test_story_run_loop_b_threshold, test_task_root_parsers, test_window_record, test_words_doors (test_judgment_census was also run, 25/25).

Negative control (byte copy of s5_precheck.py, both run_mapping sites unwrapped): stage_joints unsited 95 and test_s5_precheck_sides 1 FAIL; restored by cp, sha256 equal before/after: 79de2db29b059dc904a30a7a324636e373b21b32d1deedb77ccbc27ce8654859 (both).

tests-over: tests add ~209 lines vs product rewrites of existing lines (two row batteries, one per file).

## Needed beyond the manifest
stage_joints.py, refusal_registry.py, detector_verdict.py, slow_tests.json, scenario_walk.py, test-layers.json, contract.py, tests/test_row_fields.py, test_obligation_join.py, test_s5_precheck_plan.py.
