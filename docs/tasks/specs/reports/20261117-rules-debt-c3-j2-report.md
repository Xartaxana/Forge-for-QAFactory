# Report: node rules-debt/1/RD1-13, C3-j2 (t-1269), builder

Branch worktree-agent-a5dcea7ed81ed1834. Merge of origin/main (93 commits, no conflicts) = 87e86afa; j2 commit = 76a73838 (pushed; the commit-hook said WARN only: TEST VOLUME +13 test lines vs +12 product lines, comment lines of the pin delta).
tests-over: the +13 are comment/pin lines of the delta in test_gate_registry.py; the file loses ~590 lines in all.

## FR pass
A (no refusal text added; one question to a person removed), B (texts removed; the surviving notes are j1's), C (catalogue `needed_by` entries removed with their functions, AR-22), D (FR-59: no gate left on the unknown), G (FR-30 changelog English; FR-32 root cause = deleted with every reader). E, F: not touched.

## Per item
1. DONE gate_preflight.py: deleted `limit_seconds`, `measurement_is_stale`, `_e2e_limit`, `check_s5_stand_limits`, `_stand_limit_card`, the reporter's `over` skip block in `check_s5_reporter`, `r.check_s5_stand_limits` in `run`'s tuple, the two selftest `case(...)` lines of `limit_seconds` / `measurement_is_stale`, the docstring mentions (module head "Four" -> "Three more facts", `profiles_of`-users line, E2E_LEVEL comment reworded: it keeps its reader `_page_load_due`). Also deleted `_kept_page_load` (j1's helper whose only reader was the deleted card) and reworded two j1 comments/docstrings that said "and on the e2e stand card" (check_stand_page_load docstring, kept-text docstring, one comment).
2. DONE gate-registry.json row `s5_stand_limits` deleted; judgment-census row deleted (ceilings unchanged); config-keys.json `needed_by` entries removed from `profiles` and `environments`.
3. DONE test_gate_registry.py: EXPECTED_IDS/EXPECTED_DEBT lose the id; K-T1.2 "1 gate(s) left as debt:" (base measured: 2); K-T1.14 wording + split 25/1/6 (was 25/2/6) + comment lines; F4 unchanged.
4. DONE test_gate_preflight.py deletions (by name): helpers `with_limits`, `limit_cards`, `record_edit`; tests `test_k5_a_page_that_loads_slower_than_the_page_objects_wait_is_one_card`, `test_k5_strict_greater_than_at_and_beyond_the_wait`, `test_k5_nothing_recorded_is_not_measured_and_never_a_card`, `test_k5_a_limit_that_cannot_be_read_is_one_defect_and_no_card`, `test_a_measurement_older_than_the_stand_is_not_a_measurement`, `test_the_other_stand_is_named_only_when_its_own_load_fits`, `test_a_card_a_person_has_answered_is_closed_in_all_the_ways_it_can_still_be`, `test_the_stand_limit_step_can_be_switched_off`, `test_the_reporter_skips_a_profile_whose_e2e_limit_card_is_open`, `test_c2_the_stand_limit_card_offers_only_doors_that_have_an_executor`, `test_q2_a_page_load_with_no_command_or_date_is_the_factorys_defect`; the 11 runner lines of those tests. Edits: `test_the_cmp2_rehearsal_is_the_one_a_person_can_read` (config and the "stand limit" check gone), `scenario_messages` (`record` lambda and five `limits` runs gone), `NEW_CHECK_FUNCTIONS`, the c3 literal-scan list, the `_e2e_limit` entry of the append filter (now `fn.name == "not_asked_line"`). One j1 test edit (owner's correction row): `test_c3_j1_a_kept_reason_gets_one_more_try...` lost its `s5_stand_limits` step and the "e2e stand card carries the kept reason" check (the card is gone; the note still carries the reason, checked there).
5. DONE changelog fragment `ai-packages/qa-factory/changelog.d/rules-debt-c3-j2-stand-limit-removed.md`.

## D13 before / after (GR.analyse, base = git archive of ff7f5b70 in temp; after = worktree)
before: 151 items; after: 151 items; the sorted triple lists are byte-identical (`cmp` of the two outputs: SAME). No triple left.

## K-T1.2 count measured
`gate_registry.py --check` on j2: exit 0, "1 gate(s) left as debt:" (j2's base: 2), `s5_stand_limits` absent (grep of the output: only the "left as debt" line).

## Witness
- `python -B gate_registry.py --check` -> exit 0, `A26 gate registry: no violations`, `1 gate(s) left as debt:`.
- `scenario_walk.py --witness-for <6 owned paths>` printed 36 test files. Slow (slow_tests.json > 10 s) and judged by the batch canon, not run whole: test_gate_preflight, test_judgment_census, test_bug_records, test_config_migration, test_controller_gate_decision, test_detector_verdict, test_gate_brief_and_retro, test_gate_question_form, test_node_ids, test_profile_reader, test_read_json, test_readiness, test_scenario_cart_1, test_scenario_dry_1, test_scenario_local_1_0108, test_selftest_slow_tests, test_stage_joints, test_story_run_s6, test_story_run_stand_identity, test_words_doors. test_gate_registry (19.7 s, owned, pins moved) was run.
- Non-slow files run, tails: question_status `25/25 ok`; gate_role_accounts `44 passed`; gate_vocabulary `141/141 ok`; handed_to_person `58/58 ok`; human_questions `651/651 ok`; login_need `33 passed`; manual_capture `1236/1236 ok`; not_needed_role `22 passed`; one_source_per_fact `21/21 ok`; reference_window `85/85 ok`; scenario_local_1_arm_b `5/5 ok`; scenario_walk `95/95 ok`; scenario_world `33/33 ok`; stand_gaps `182/182 ok`; whole_identifier `166/166 ok`; test_gate_registry (its chain) `523/523 ok` ... `test_field_producers: 891/891 ok`, ALLDONE.
- Slice of the edited tests of test_gate_preflight (render test, c3 scan test, reporter test, the j1 tests, the t-357 sweep): all `OK`; the single FAIL line is the one j1 already reported (`the sweep saw a good many texts`: a slice records too few texts; the rule check itself PASS).
- AST check of test_gate_preflight.py: parses; every `test_*` call of the runner block has a def (missing names: set()). Grep of the file for `e2e_stand_limit|s5_stand_limits|_e2e_limit|page_object_max_wait_s|e2e_page_load_s|with_limits|record_edit|limit_cards|check_s5_stand_limits|_stand_limit_card|e2e stand` -> no output (positive control: the same file holds `check_stand_page_load` hits).
- DoD (2) Grep, case-insensitive, scripts/ non-tests: matches only `cost_capture.py:3364/3403/3415` `_limit_seconds` (another function, name collision with `limit_seconds`) and `tests/test_manual_capture.py:193` (a j1 row that pins "a config `measured` 70 is no longer read -> 180"; a test, not a reader). Positive control `stand_page_load_lines`: brief_pack.py 2. config-keys.json: deleted names 0; `check_stand_page_load` 2.
- Axis 5: Grep of package `.md` for `stand limit|page_object|e2e stand` -> 0 (control: same pattern over `scripts/` finds hits). Reporter `== "over"` left with the skip (A1 class). No other comparison of the deleted word found.

## Deviations / decisions
- Deleted `_kept_page_load` and reworded the j1 "e2e stand card" sentences (the card the kept reason rode on is gone): required by the deletion, the note path stays.
- E24: `test_story_run_delivery_b.py:555`, `test_story_run_delivery_c.py:980, :992` use the id `e2e_stand_limit` as sample data; untouched (no live code reads it).
- The j1 report said the owner's correction was returned as questions; the j1 branch carries it (commit 6aa3c34e); j2 kept it intact in `check_stand_page_load`.

## Needed from integration
- `ai-packages/qa-factory/changelog.d/rules-debt-c3-j1-stand-page-load.md` line 7: "and the reason is carried in the gate note and on the e2e stand card" -> drop " and on the e2e stand card" (the card no longer exists; file outside owns).
- `ai-packages/qa-factory/design/factory-rules-debt.md:111` still lists gate `s5_stand_limits` (Lead's, non-goal).

## Siblings noticed
- `test_manual_capture.py:193` row names the dead key `e2e_page_load_s` as a negative control: fine, but a later grep for the key will show it.
- The reporter `timed_out` card (F-j-reporter) is the reachable successor: still open, Lead's node.
- No config key added.
