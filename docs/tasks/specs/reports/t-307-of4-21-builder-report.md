# t-307 OF4-21 builder report (condensed by the coordinator; the builder named no handoff file)

commit e53c163 on wip/of4-21 (pushed). One open item: `test_fit_targets.py` K-BRIEF-CAP-9 red. Fix round t-313 changes the pin to expect `runtime_paths.story_text`.

## Done
- New `runtime_paths.story_text(task_root, rel="")` (spec §3.1). It returns the path relative to `project_for_task` when the project holds the story, and the absolute posix path otherwise. `rel` is text, never resolved. It never raises, including on None and "\0".
- `brief_pack.py`: every §2.1 (#1-#27) and §2.2 site goes through `RP.story_text`. Supporting changes:
  - `_home_text(project)` was added.
  - `S3_ROSTER_FILE` becomes `S3_ROSTER_NAME_OF_FILE` plus `RP.rel_text`.
  - `APPROACH_ONE_LINE` and `APPROACH_POINTER` become `{home}` templates.
  - `_approach_test_data(home=RP.HOME)`.
  - The blast line is no longer cut; the cap applies to the reason (E9).
  - Parser #4 uses `case_versions.read_source_path`, and parser #5 skips more (E17).
- Shape changes, made together with every caller (`user_path_failures.main`, `test_flow_requests`, `test_walk_plan_fields`, `test_refusal_registry:145`): `_rel(task_root, name)`, `command_card_lines(task_root, ...)`, `request_lines(found, task_root)`.
- Tests: `of4_21_paths_follow_the_reader` (T1, T2, T3, T5, T6, T6b x3 worlds, T7, T8, T9) and `k6_story_text`. The H24 pin now expects the absolute posix path.
- Changelog: `changelog.d/onboarding-forge-4-of4-21-brief-pack-paths.md`.

## Deviations
1. `test_refusal_registry.py:145` uses an unmarked temp project, not `harness.mark_project`, because owns allowed only the call. The card prints the absolute path, and the assertion is on the card head.
2. T1 "default" checks key lines. The scout card `<T>` line becomes `<task root>` (C1); `test_refusal_ready_commands` is 154/154.
3. Slow files from `slow_tests.json` were not run; CI judges them.
4. `fit_target_lines` is a bare-folder caller that the spec's `_rel` list missed (the Q1 cause).

## Witness (verbatim summary lines; each `( cd <wt> && python -B scripts/tests/<file> )`)
test_ahead_cards 245/245; test_brief_pack 936/936; test_runtime_paths 118/118; test_flow_requests 94/94; test_walk_plan_fields 128/128; test_refusal_registry 263/263; test_brief_pack_s5_plan 194/194; test_first_look_briefs 204/204; test_story_step_start 169/169; test_judgment_census 22/22; test_codex_tool_guidance 217/217; test_cost_capture_role_gaps 8/8; test_dispatch_liveness 441/441; test_first_look_wiring 103/103; test_gate_ordered_reporter 89/89; test_guard_big_read_sections 248/248; test_quality_demand 84/84; test_regression_scope 93/93; test_role_load 171/171; test_scenario_walk 93/93; test_scenario_world 33/33; test_stand_gaps 182/182; test_story_run_s6_w1_frozen 6/6; test_whole_identifier 166/166; test_brief_s3_roster exit 0; test_refusal_ready_commands 154/154; **test_fit_targets 115/116 FAIL K-BRIEF-CAP-9** (handed to t-313).
`selftest.py --limits --lang`: 4/4 ok.
Grep `-i "qa-factory/(artifacts|strategy)"` over `brief_pack.py` finds nothing. The positive control on `hooklib.py` finds :276.
`test_brief_pack` wall time went from 37 s to 39-40 s (about 25 `project_for_task` calls per brief, no cache; C3).

## Quarantined pins expected red (not run)
`test_brief_pack_roles.py:110`, `test_exploration_perturbations.py:88` and `:340`, and possibly `test_project_approach.py`.

## FR / AR
- FR: A n/a; B n/a; C FR-14/15; D FR-16/58/59; E FR-37; F n/a; G FR-30/32/54.
- AR: AR-13, AR-4, AR-15 (the axis-8 row is queued to Lead), AR-24, AR-20 (census 22/22), AR-29 (no check changed).
