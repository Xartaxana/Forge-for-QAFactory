Source: pipeline 8069240 (measure/redundancy, f40b0cb6), job test-redundancy 28313602, 10.11.2026; text recovered from the job artifact, table marks restored.

# Test redundancy

- test files: 705 (ok 688, red 1, not-measured 16)
- product lines covered: 157856; by ok files: 157838; under (no context): 0
- ok files with 0 unique lines: 64 (291.55 s of 12565.17 s in all)
- greedy cover: 625 files reach 100% of the lines the ok files cover

## A. Deletion candidates: status ok, 0 unique lines, slowest first

NOTE: line coverage only: a file with zero unique lines may still hold the only assertion on a behaviour - a candidate for a reader, not a verdict.

| file | covered | seconds |
|---|---|---|
| test_state_portability.py | 328 | 42.54 |
| test_judgment_census.py | 931 | 39.35 |
| test_story_run_stand_b.py | 17666 | 29.62 |
| test_gate_decision_manual_pass.py | 14610 | 22.08 |
| test_bind_repair_dispatch.py | 11689 | 20.96 |
| test_halt_resume_door.py | 8457 | 18.95 |
| test_story_step_prompt.py | 4915 | 15.37 |
| test_manual_window.py | 13708 | 7.94 |
| test_story_run_s5_n1_frozen.py | 12892 | 6.42 |
| test_fixes_13797.py | 14111 | 5.98 |
| test_controller_blocks.py | 86 | 4.68 |
| test_gate_vocabulary.py | 8671 | 4.22 |
| test_no_real_claude.py | 8503 | 3.72 |
| test_manual_seed_path.py | 8977 | 3.58 |
| test_resume_packet.py | 8355 | 3.47 |
| test_harness_cwd_guard.py | 10394 | 3.32 |
| test_controller_doors.py | 8166 | 3.27 |
| test_s7_reorder_fixture.py | 9084 | 2.93 |
| test_form_at_stop.py | 6470 | 2.92 |
| test_pinned_lifecycle.py | 9760 | 2.82 |
| test_gate_ordered_reporter.py | 8568 | 2.57 |
| test_cost_capture_nonfactory_summary.py | 4836 | 2.43 |
| test_case_id_texts_sweep.py | 3529 | 2.37 |
| test_coverage_controller_integration.py | 9766 | 2.32 |
| test_field_producers.py | 2655 | 2.32 |
| test_actor_control_rule.py | 1673 | 1.78 |
| test_charters_s5_s9.py | 835 | 1.72 |
| test_ticket_rework_stages.py | 4992 | 1.72 |
| test_cost_capture_subagent_usage.py | 6212 | 1.63 |
| test_bare_calls_live.py | 4748 | 1.57 |
| test_answer_rework_pairs.py | 4658 | 1.47 |
| test_cost_capture_sticky_attribution.py | 6085 | 1.47 |
| test_exit_gate_s7_investigation.py | 4495 | 1.38 |
| test_finalization_flow.py | 5783 | 1.37 |
| test_profile_gate.py | 4792 | 1.32 |
| test_s4_findings_glob.py | 4631 | 1.32 |
| test_reducer_recovery.py | 5402 | 1.22 |
| test_cost_capture_lock_scope.py | 2754 | 1.18 |
| test_codex_host_reference.py | 2851 | 1.17 |
| test_state_exits.py | 3548 | 1.17 |
| test_stage_cards.py | 2878 | 1.04 |
| test_story_step.py | 2675 | 0.92 |
| test_scoped_invalidation.py | 4779 | 0.87 |
| test_instance_records.py | 3506 | 0.77 |
| test_ledger_matching.py | 3151 | 0.77 |
| test_project_root.py | 693 | 0.77 |
| test_dashboard_cost_widgets.py | 3492 | 0.72 |
| test_rc1_14_rule_lines.py | 2625 | 0.72 |
| test_walk_two_actors.py | 1014 | 0.72 |
| test_onboarding_markers.py | 2424 | 0.67 |
| test_tried_table.py | 1905 | 0.62 |
| test_code_critic_probe_rule.py | 2105 | 0.57 |
| test_delivery_visibility.py | 2305 | 0.57 |
| test_stage_joints_12586.py | 2881 | 0.57 |
| test_gate_a_two_documents.py | 1450 | 0.47 |
| test_host_probe_handback.py | 745 | 0.47 |
| test_project_decisions_tables.py | 694 | 0.47 |
| test_conductor_investigates_first.py | 324 | 0.42 |
| test_metrics_already_run.py | 1484 | 0.42 |
| test_remedy_reporter_contract.py | 855 | 0.32 |
| test_postcompact_reload.py | 676 | 0.31 |
| test_report_texts.py | 130 | 0.26 |
| test_task_price_unestimated.py | 1392 | 0.26 |
| test_grammar.py | 204 | 0.21 |

## B. Greedy set cover over the ok files (share of the lines the ok files cover)

| # | file | adds | cumulative lines | cumulative share | seconds |
|---|---|---|---|---|---|
| 1 | test_story_run_delivery_c.py | 30570 | 30570 | 19.37% | 151.65 |
| 2 | test_role_commands.py | 9592 | 40162 | 25.45% | 39.42 |
| 3 | test_gate_brief_and_retro.py | 7217 | 47379 | 30.02% | 60.53 |
| 4 | test_story_run_s7_live.py | 5608 | 52987 | 33.57% | 308.81 |
| 5 | test_s5_precheck.py | 4236 | 57223 | 36.25% | 30.86 |
| 6 | test_story_run_s0.py | 3660 | 60883 | 38.57% | 237.32 |
| 7 | test_codex_host.py | 3196 | 64079 | 40.60% | 14.56 |
| 8 | test_probe_by_code.py | 2984 | 67063 | 42.49% | 116.7 |
| 9 | test_install_retire.py | 2735 | 69798 | 44.22% | 34.68 |
| 10 | test_branch_accounting.py | 2647 | 72445 | 45.90% | 110.94 |
| 11 | test_gate_preflight.py | 2480 | 74925 | 47.47% | 51.41 |
| 12 | test_story_run_loop_b.py | 2409 | 77334 | 49.00% | 99.75 |
| 13 | test_collect_pack.py | 2238 | 79572 | 50.41% | 113.59 |
| 14 | test_report_facts.py | 1982 | 81554 | 51.67% | 43.45 |
| 15 | test_brief_pack.py | 1929 | 83483 | 52.89% | 34.12 |
| 16 | test_stage_guard.py | 1740 | 85223 | 53.99% | 136.03 |
| 17 | test_story_run_s6.py | 1620 | 86843 | 55.02% | 212.77 |
| 18 | test_run_suite_mine.py | 1562 | 88405 | 56.01% | 55.69 |
| 19 | test_words_doors.py | 1520 | 89925 | 56.97% | 120.52 |
| 20 | test_validators.py | 1438 | 91363 | 57.88% | 14.21 |
| 21 | test_task_root_parsers.py | 1369 | 92732 | 58.75% | 123.96 |
| 22 | test_audit_rules.py | 1105 | 93837 | 59.45% | 14.56 |
| 23 | test_ticket_adapter.py | 1091 | 94928 | 60.14% | 18.01 |
| 24 | test_mobile_road.py | 1048 | 95976 | 60.81% | 121.19 |
| 25 | test_blocked_by_env_window.py | 1023 | 96999 | 61.45% | 32.11 |
| 26 | test_story_run_gate_repair.py | 993 | 97992 | 62.08% | 261.19 |
| 27 | test_handoff.py | 966 | 98958 | 62.70% | 64.96 |
| 28 | test_probe_by_code_languages.py | 912 | 99870 | 63.27% | 114.16 |
| 29 | test_factory_dashboard_task_view.py | 891 | 100761 | 63.84% | 6.44 |
| 30 | test_grounding_table.py | 874 | 101635 | 64.39% | 136.73 |
| 31 | test_story_run_refusals.py | 869 | 102504 | 64.94% | 242.87 |
| 32 | test_s7_investigation_replay.py | 787 | 103291 | 65.44% | 37.56 |
| 33 | test_probe_debt.py | 768 | 104059 | 65.93% | 20.61 |
| 34 | test_brief_pack_s5_plan.py | 747 | 104806 | 66.40% | 36.61 |
| 35 | test_question_branches.py | 745 | 105551 | 66.87% | 12.95 |
| 36 | test_console_encoding.py | 692 | 106243 | 67.31% | 25.05 |
| 37 | test_manual_capture.py | 678 | 106921 | 67.74% | 11.72 |
| 38 | test_external_writes.py | 657 | 107578 | 68.16% | 8.14 |
| 39 | test_story_run_codex.py | 657 | 108235 | 68.57% | 56.92 |
| 40 | test_manifest_from_tests.py | 640 | 108875 | 68.98% | 86.14 |
| 41 | test_cost_capture_tail.py | 633 | 109508 | 69.38% | 54.96 |
| 42 | test_exploration.py | 569 | 110077 | 69.74% | 14.29 |
| 43 | test_probe_by_code_alternative.py | 555 | 110632 | 70.09% | 73.52 |
| 44 | test_walk_road.py | 543 | 111175 | 70.44% | 21.85 |
| 45 | test_controller_state.py | 541 | 111716 | 70.78% | 26.43 |
| 46 | test_source_inventory.py | 535 | 112251 | 71.12% | 3.03 |
| 47 | test_check_delivery.py | 528 | 112779 | 71.45% | 107.77 |
| 48 | test_question_register.py | 522 | 113301 | 71.78% | 11.23 |
| 49 | test_judge_run.py | 513 | 113814 | 72.11% | 2.07 |
| 50 | test_reporter_rehearsal.py | 496 | 114310 | 72.42% | 29.94 |
| 51 | test_host_probe_shapes.py | 496 | 114806 | 72.74% | 79.26 |
| 52 | test_launch_check.py | 481 | 115287 | 73.04% | 3.83 |
| 53 | test_source_exclusions.py | 465 | 115752 | 73.34% | 2.12 |
| 54 | test_runtime_probe_onboarding.py | 439 | 116191 | 73.61% | 12.56 |
| 55 | test_driver_chain.py | 438 | 116629 | 73.89% | 8.58 |
| 56 | test_stage_joints.py | 425 | 117054 | 74.16% | 126.39 |
| 57 | test_readiness.py | 424 | 117478 | 74.43% | 31.54 |
| 58 | test_sizing.py | 412 | 117890 | 74.69% | 3.63 |
| 59 | test_hooks_wiring.py | 411 | 118301 | 74.95% | 29.0 |
| 60 | test_red_sandbox_reports.py | 404 | 118705 | 75.21% | 70.93 |
| 61 | test_test_locations.py | 402 | 119107 | 75.46% | 10.29 |
| 62 | test_env_access_onboarding.py | 398 | 119505 | 75.71% | 2.62 |
| 63 | test_story_step_materialize.py | 396 | 119901 | 75.96% | 116.18 |
| 64 | test_base_slice.py | 387 | 120288 | 76.21% | 4.98 |
| 65 | test_bug_reproduction.py | 387 | 120675 | 76.45% | 5.53 |
| 66 | test_execution_scheduler.py | 379 | 121054 | 76.70% | 6.9 |
| 67 | test_story_run_s3_windows.py | 369 | 121423 | 76.93% | 64.97 |
| 68 | test_case_id_form_sites.py | 362 | 121785 | 77.16% | 17.38 |
| 69 | test_flow_requests.py | 337 | 122122 | 77.37% | 3.07 |
| 70 | test_run_forms.py | 333 | 122455 | 77.58% | 27.66 |
| 71 | test_dependency_drift.py | 332 | 122787 | 77.79% | 2.12 |
| 72 | test_stand_health.py | 331 | 123118 | 78.00% | 4.74 |
| 73 | test_post_commit_refresh.py | 320 | 123438 | 78.21% | 8.48 |
| 74 | test_story_run_s7.py | 317 | 123755 | 78.41% | 90.87 |
| 75 | test_stand_gap_carry.py | 302 | 124057 | 78.60% | 13.36 |
| 76 | test_blast_radius.py | 302 | 124359 | 78.79% | 25.09 |
| 77 | test_stand_access.py | 301 | 124660 | 78.98% | 16.44 |
| 78 | test_gate_words_road.py | 300 | 124960 | 79.17% | 70.95 |
| 79 | test_guard_big_read_sections.py | 294 | 125254 | 79.36% | 1.77 |
| 80 | test_place_answers.py | 293 | 125547 | 79.54% | 6.83 |
| 81 | test_stage_acceptance_consumer.py | 289 | 125836 | 79.72% | 29.57 |
| 82 | test_config_revert.py | 279 | 126115 | 79.90% | 7.68 |
| 83 | test_fit_targets.py | 278 | 126393 | 80.08% | 3.52 |
| 84 | test_guard_write_owners.py | 269 | 126662 | 80.25% | 24.32 |
| 85 | test_environment_preparation.py | 266 | 126928 | 80.42% | 3.12 |
| 86 | test_story_run_delivery.py | 263 | 127191 | 80.58% | 137.93 |
| 87 | test_story_closed.py | 261 | 127452 | 80.75% | 35.67 |
| 88 | test_local_keys.py | 258 | 127710 | 80.91% | 4.93 |
| 89 | test_story_run_freshness.py | 258 | 127968 | 81.08% | 142.21 |
| 90 | test_reinstall_equals_fresh.py | 244 | 128212 | 81.23% | 22.37 |
| 91 | test_guard_dispatch_budget_and_logs.py | 244 | 128456 | 81.38% | 214.59 |
| 92 | test_investigation_probe.py | 241 | 128697 | 81.54% | 14.08 |
| 93 | test_ticket_light.py | 240 | 128937 | 81.69% | 1.72 |
| 94 | test_judge.py | 235 | 129172 | 81.84% | 20.92 |
| 95 | test_role_load.py | 233 | 129405 | 81.99% | 2.72 |
| 96 | test_dispatch_liveness.py | 230 | 129635 | 82.13% | 1.32 |
| 97 | test_exploration_perturbations.py | 230 | 129865 | 82.28% | 2.97 |
| 98 | test_walk_session.py | 228 | 130093 | 82.42% | 5.44 |
| 99 | test_judge_results.py | 226 | 130319 | 82.57% | 3.24 |
| 100 | test_onboarding_probe.py | 223 | 130542 | 82.71% | 14.62 |
| 101 | test_account_word.py | 217 | 130759 | 82.84% | 5.04 |
| 102 | test_resume_stopped.py | 212 | 130971 | 82.98% | 33.31 |
| 103 | test_bug_records.py | 211 | 131182 | 83.11% | 60.25 |
| 104 | test_manifest_put_merge.py | 210 | 131392 | 83.24% | 1.57 |
| 105 | test_onboarding_notes.py | 210 | 131602 | 83.38% | 6.19 |
| 106 | test_release_fingerprint.py | 210 | 131812 | 83.51% | 9.34 |
| 107 | test_story_run_repair_limit.py | 210 | 132022 | 83.64% | 171.84 |
| 108 | test_form_selftest.py | 209 | 132231 | 83.78% | 4.58 |
| 109 | test_size_forecast.py | 207 | 132438 | 83.91% | 2.37 |
| 110 | test_probe_one_road.py | 207 | 132645 | 84.04% | 6.54 |
| 111 | test_s5_precheck_plan.py | 206 | 132851 | 84.17% | 2.02 |
| 112 | test_task_price.py | 203 | 133054 | 84.30% | 0.57 |
| 113 | test_manual_evidence.py | 201 | 133255 | 84.43% | 3.48 |
| 114 | test_contract_slices.py | 198 | 133453 | 84.55% | 5.63 |
| 115 | test_import_test_receipt.py | 197 | 133650 | 84.68% | 0.77 |
| 116 | test_claim_projector.py | 197 | 133847 | 84.80% | 41.04 |
| 117 | test_validate_artifacts_report.py | 192 | 134039 | 84.92% | 4.84 |
| 118 | test_story_step_s5_plan.py | 192 | 134231 | 85.04% | 26.35 |
| 119 | test_config_migration.py | 187 | 134418 | 85.16% | 32.35 |
| 120 | test_stand_identity.py | 187 | 134605 | 85.28% | 42.71 |
| 121 | test_selftest_slow_tests.py | 186 | 134791 | 85.40% | 4.23 |
| 122 | test_judge_discovery.py | 185 | 134976 | 85.52% | 0.62 |
| 123 | test_story_resume_migration.py | 182 | 135158 | 85.63% | 3.47 |
| 124 | test_manual_capture_session.py | 181 | 135339 | 85.75% | 2.57 |
| 125 | test_no_move_seam.py | 179 | 135518 | 85.86% | 154.62 |
| 126 | test_red_sandbox_setup.py | 177 | 135695 | 85.97% | 2.92 |
| 127 | test_cost_capture_role_gaps.py | 176 | 135871 | 86.08% | 5.64 |
| 128 | test_execution_request.py | 176 | 136047 | 86.19% | 29.65 |
| 129 | test_friction.py | 173 | 136220 | 86.30% | 1.27 |
| 130 | test_handoff_producers.py | 173 | 136393 | 86.41% | 2.37 |
| 131 | test_window_record.py | 173 | 136566 | 86.52% | 89.4 |
| 132 | test_collect_redact.py | 172 | 136738 | 86.63% | 2.79 |
| 133 | test_config_view.py | 172 | 136910 | 86.74% | 15.97 |
| 134 | test_archive_task.py | 171 | 137081 | 86.85% | 2.02 |
| 135 | test_exit_gate_scope.py | 166 | 137247 | 86.95% | 1.78 |
| 136 | test_judge_code.py | 166 | 137413 | 87.06% | 2.44 |
| 137 | test_walk_supply_config.py | 165 | 137578 | 87.16% | 34.28 |
| 138 | test_story_progress.py | 164 | 137742 | 87.27% | 28.2 |
| 139 | test_window_and_budgets.py | 162 | 137904 | 87.37% | 1.37 |
| 140 | test_s7_null_outcome.py | 161 | 138065 | 87.47% | 53.92 |
| 141 | test_gate_shown.py | 158 | 138223 | 87.57% | 3.22 |
| 142 | test_manual_observe.py | 156 | 138379 | 87.67% | 2.87 |
| 143 | test_s7_reorder.py | 154 | 138533 | 87.77% | 1.87 |
| 144 | test_node_ids.py | 154 | 138687 | 87.87% | 24.83 |
| 145 | test_collect_stall.py | 153 | 138840 | 87.96% | 1.85 |
| 146 | test_exploratory_answers.py | 152 | 138992 | 88.06% | 2.72 |
| 147 | test_probe_not_proved.py | 150 | 139142 | 88.15% | 7.0 |
| 148 | test_gate_registry.py | 150 | 139292 | 88.25% | 21.31 |
| 149 | test_scout_reliability.py | 145 | 139437 | 88.34% | 8.33 |
| 150 | test_grounding_coverage.py | 143 | 139580 | 88.43% | 8.09 |
| 151 | test_needs_author.py | 143 | 139723 | 88.52% | 70.43 |
| 152 | test_run_suite_timeout.py | 142 | 139865 | 88.61% | 1.42 |
| 153 | test_manual_surprise_triage.py | 142 | 140007 | 88.70% | 2.72 |
| 154 | test_ledger.py | 138 | 140145 | 88.79% | 5.08 |
| 155 | test_story_run_stand_identity.py | 138 | 140283 | 88.88% | 209.79 |
| 156 | test_coverage_contract.py | 137 | 140420 | 88.96% | 2.48 |
| 157 | test_raise_reaches_plan_row.py | 136 | 140556 | 89.05% | 2.58 |
| 158 | test_driver_timing.py | 135 | 140691 | 89.14% | 0.87 |
| 159 | test_usage_activity.py | 134 | 140825 | 89.22% | 4.91 |
| 160 | test_baseline_contract.py | 133 | 140958 | 89.31% | 0.62 |
| 161 | test_retro_test_runs.py | 132 | 141090 | 89.39% | 1.22 |
| 162 | test_dashboard_task_binding.py | 129 | 141219 | 89.47% | 2.57 |
| 163 | test_test_novelty.py | 128 | 141347 | 89.55% | 9.62 |
| 164 | test_case_versions_scope.py | 127 | 141474 | 89.63% | 52.3 |
| 165 | test_device_stand.py | 126 | 141600 | 89.71% | 1.82 |
| 166 | test_agent_autobind.py | 126 | 141726 | 89.79% | 45.64 |
| 167 | test_s5_plan_check.py | 124 | 141850 | 89.87% | 13.65 |
| 168 | test_story_run_exit_limit.py | 124 | 141974 | 89.95% | 70.49 |
| 169 | test_telemetry_count.py | 123 | 142097 | 90.03% | 1.62 |
| 170 | test_case_merges.py | 123 | 142220 | 90.11% | 2.17 |
| 171 | test_vcs_evidence.py | 122 | 142342 | 90.18% | 1.32 |
| 172 | test_investigation.py | 121 | 142463 | 90.26% | 15.37 |
| 173 | test_retro_wait_rework.py | 117 | 142580 | 90.33% | 1.52 |
| 174 | test_plan_row.py | 117 | 142697 | 90.41% | 13.34 |
| 175 | test_then_remainder.py | 114 | 142811 | 90.48% | 9.95 |
| 176 | test_s7_rejudge.py | 114 | 142925 | 90.55% | 20.81 |
| 177 | test_exit_gate_digest_fix.py | 113 | 143038 | 90.62% | 1.37 |
| 178 | test_reducer_supersession.py | 113 | 143151 | 90.69% | 1.72 |
| 179 | test_manifest_projection.py | 111 | 143262 | 90.77% | 4.93 |
| 180 | test_command_proposal.py | 111 | 143373 | 90.84% | 32.02 |
| 181 | test_red_sandbox_diagnostic.py | 111 | 143484 | 90.91% | 38.33 |
| 182 | test_protected_test_path.py | 109 | 143593 | 90.97% | 14.21 |
| 183 | test_question_thens_claim_keys.py | 108 | 143701 | 91.04% | 1.93 |
| 184 | test_onboarding_first_reader.py | 107 | 143808 | 91.11% | 12.62 |
| 185 | test_s5_plan_controller.py | 107 | 143915 | 91.18% | 39.93 |
| 186 | test_guard_window_files.py | 106 | 144021 | 91.25% | 1.07 |
| 187 | test_diff_pass.py | 105 | 144126 | 91.31% | 1.92 |
| 188 | test_open_vocabularies.py | 105 | 144231 | 91.38% | 2.97 |
| 189 | test_resolver.py | 105 | 144336 | 91.45% | 12.46 |
| 190 | test_login_body_fields.py | 104 | 144440 | 91.51% | 1.17 |
| 191 | test_claude_host_probe.py | 104 | 144544 | 91.58% | 49.93 |
| 192 | test_silent_passes.py | 102 | 144646 | 91.64% | 58.59 |
| 193 | test_question_stop.py | 101 | 144747 | 91.71% | 6.89 |
| 194 | test_codex_tool_guidance.py | 101 | 144848 | 91.77% | 10.91 |
| 195 | test_managed_dependency.py | 100 | 144948 | 91.83% | 0.52 |
| 196 | test_tms_publication.py | 100 | 145048 | 91.90% | 0.57 |
| 197 | test_walk_places.py | 100 | 145148 | 91.96% | 2.69 |
| 198 | test_s5_process.py | 99 | 145247 | 92.02% | 9.35 |
| 199 | test_manual_app.py | 99 | 145346 | 92.09% | 20.04 |
| 200 | test_arch_check.py | 98 | 145444 | 92.15% | 0.36 |
| 201 | test_story_run_deferred.py | 98 | 145542 | 92.21% | 23.92 |
| 202 | test_launch_card.py | 98 | 145640 | 92.27% | 55.33 |
| 203 | test_app_card.py | 96 | 145736 | 92.33% | 2.32 |
| 204 | test_infra_failure.py | 96 | 145832 | 92.39% | 229.05 |
| 205 | test_report_adapt.py | 94 | 145926 | 92.45% | 14.25 |
| 206 | test_ticket_query.py | 93 | 146019 | 92.51% | 1.27 |
| 207 | test_gap_points.py | 93 | 146112 | 92.57% | 12.85 |
| 208 | test_story_step_manual_block.py | 93 | 146205 | 92.63% | 34.79 |
| 209 | test_d1_product_gap.py | 92 | 146297 | 92.69% | 1.87 |
| 210 | test_environment_record.py | 92 | 146389 | 92.75% | 7.05 |
| 211 | test_sizing_functions.py | 91 | 146480 | 92.80% | 1.52 |
| 212 | test_exploration_identity.py | 91 | 146571 | 92.86% | 1.77 |
| 213 | test_gate_preflight_integrations.py | 91 | 146662 | 92.92% | 4.48 |
| 214 | test_repair_form_carry.py | 91 | 146753 | 92.98% | 21.17 |
| 215 | test_diff_scope.py | 90 | 146843 | 93.03% | 0.62 |
| 216 | test_probe_by_code_copy.py | 90 | 146933 | 93.09% | 19.98 |
| 217 | test_current_audit_contract.py | 88 | 147021 | 93.15% | 0.92 |
| 218 | test_third_verdict.py | 88 | 147109 | 93.20% | 46.52 |
| 219 | test_retro_task_price.py | 87 | 147196 | 93.26% | 2.02 |
| 220 | test_selftest_shard.py | 87 | 147283 | 93.31% | 6.18 |
| 221 | test_tracker_route.py | 86 | 147369 | 93.37% | 3.29 |
| 222 | test_story_root_class.py | 86 | 147455 | 93.42% | 23.78 |
| 223 | test_source_preflight.py | 85 | 147540 | 93.48% | 4.6 |
| 224 | test_controller_gate_decision.py | 85 | 147625 | 93.53% | 79.45 |
| 225 | test_artifact_supersede.py | 84 | 147709 | 93.58% | 8.43 |
| 226 | test_copy_detector.py | 83 | 147792 | 93.64% | 1.13 |
| 227 | test_walk_record.py | 81 | 147873 | 93.69% | 6.37 |
| 228 | test_planning_contract_not_planned.py | 80 | 147953 | 93.74% | 2.68 |
| 229 | test_s5_grown_windows.py | 80 | 148033 | 93.79% | 27.63 |
| 230 | test_run_budget.py | 80 | 148113 | 93.84% | 71.04 |
| 231 | test_tracker_write_and_status.py | 79 | 148192 | 93.89% | 0.97 |
| 232 | test_assertion_detectors.py | 79 | 148271 | 93.94% | 1.12 |
| 233 | test_null_outcomes.py | 79 | 148350 | 93.99% | 14.66 |
| 234 | test_story_closure.py | 78 | 148428 | 94.04% | 3.88 |
| 235 | test_code_close_behind.py | 78 | 148506 | 94.09% | 4.84 |
| 236 | test_price_table_question.py | 77 | 148583 | 94.14% | 1.87 |
| 237 | test_run_suite_reports.py | 77 | 148660 | 94.19% | 3.48 |
| 238 | test_manual_step_errors.py | 76 | 148736 | 94.23% | 2.47 |
| 239 | test_evidence_not_delivered.py | 75 | 148811 | 94.28% | 2.57 |
| 240 | test_rate_precedence.py | 74 | 148885 | 94.33% | 0.47 |
| 241 | test_stand_lease.py | 74 | 148959 | 94.37% | 3.89 |
| 242 | test_s5_parallel_admission.py | 74 | 149033 | 94.42% | 18.56 |
| 243 | test_judge_form.py | 73 | 149106 | 94.47% | 1.32 |
| 244 | test_manual_rejudge.py | 73 | 149179 | 94.51% | 3.58 |
| 245 | test_case_key_identity_join.py | 71 | 149250 | 94.56% | 1.87 |
| 246 | test_exit_gate_unreadable.py | 71 | 149321 | 94.60% | 2.84 |
| 247 | test_user_path_failure_patterns.py | 71 | 149392 | 94.65% | 3.0 |
| 248 | test_waiver_release.py | 71 | 149463 | 94.69% | 43.31 |
| 249 | test_person_owned.py | 70 | 149533 | 94.74% | 3.82 |
| 250 | test_person_words.py | 70 | 149603 | 94.78% | 38.53 |
| 251 | test_run_block_producer.py | 69 | 149672 | 94.83% | 1.02 |
| 252 | test_regression_scope.py | 69 | 149741 | 94.87% | 5.49 |
| 253 | test_red_window.py | 69 | 149810 | 94.91% | 63.73 |
| 254 | test_package_generation.py | 68 | 149878 | 94.96% | 52.26 |
| 255 | test_obligation_join.py | 67 | 149945 | 95.00% | 2.72 |
| 256 | test_storage_visibility.py | 65 | 150010 | 95.04% | 0.72 |
| 257 | test_story_step_card.py | 65 | 150075 | 95.08% | 3.05 |
| 258 | test_carried_concerns.py | 65 | 150140 | 95.12% | 5.12 |
| 259 | test_grounding_section.py | 65 | 150205 | 95.16% | 13.05 |
| 260 | test_project_decisions_stand_facts.py | 64 | 150269 | 95.20% | 48.2 |
| 261 | test_lifecycle_transport.py | 62 | 150331 | 95.24% | 2.67 |
| 262 | test_conductor_stop.py | 62 | 150393 | 95.28% | 4.56 |
| 263 | test_red_sandbox_probe.py | 62 | 150455 | 95.32% | 82.07 |
| 264 | test_cost_capture_settled.py | 60 | 150515 | 95.36% | 1.58 |
| 265 | test_test_repo_base.py | 60 | 150575 | 95.40% | 4.64 |
| 266 | test_critic_rollcall_apply_fixes.py | 59 | 150634 | 95.44% | 1.47 |
| 267 | test_probe_marker_judgment.py | 59 | 150693 | 95.47% | 8.64 |
| 268 | test_install_paths.py | 59 | 150752 | 95.51% | 13.0 |
| 269 | test_quality_demand.py | 58 | 150810 | 95.55% | 1.92 |
| 270 | test_unprepared_outcome.py | 57 | 150867 | 95.58% | 4.43 |
| 271 | test_gate_question_form.py | 57 | 150924 | 95.62% | 7.73 |
| 272 | test_no_mr_entry.py | 57 | 150981 | 95.66% | 56.56 |
| 273 | test_story_step_finish.py | 56 | 151037 | 95.69% | 58.46 |
| 274 | test_controller_rework.py | 56 | 151093 | 95.73% | 123.79 |
| 275 | test_cost_capture_iterations.py | 55 | 151148 | 95.76% | 1.89 |
| 276 | test_place_session.py | 54 | 151202 | 95.80% | 3.32 |
| 277 | test_proof_level.py | 54 | 151256 | 95.83% | 12.5 |
| 278 | test_exit_text_end.py | 53 | 151309 | 95.86% | 1.61 |
| 279 | test_manual_actor.py | 53 | 151362 | 95.90% | 7.19 |
| 280 | test_refusal_ready_commands.py | 53 | 151415 | 95.93% | 24.46 |
| 281 | test_candidate_evidence.py | 52 | 151467 | 95.96% | 0.72 |
| 282 | test_metric_signals.py | 52 | 151519 | 96.00% | 0.82 |
| 283 | test_oracle_provenance.py | 52 | 151571 | 96.03% | 3.62 |
| 284 | test_walk_batch.py | 52 | 151623 | 96.06% | 3.9 |
| 285 | test_story_activity_price.py | 52 | 151675 | 96.10% | 5.49 |
| 286 | test_resume_closed_author.py | 52 | 151727 | 96.13% | 60.77 |
| 287 | test_metric_evidence.py | 51 | 151778 | 96.16% | 1.32 |
| 288 | test_traceability_report.py | 51 | 151829 | 96.19% | 2.54 |
| 289 | test_cost_capture_hot_path.py | 51 | 151880 | 96.23% | 3.77 |
| 290 | test_handoff_values.py | 51 | 151931 | 96.26% | 223.99 |
| 291 | test_reachability.py | 50 | 151981 | 96.29% | 0.47 |
| 292 | test_repo_map.py | 50 | 152031 | 96.32% | 2.37 |
| 293 | test_detector_verdict.py | 49 | 152080 | 96.35% | 8.63 |
| 294 | test_make_fixture_repo.py | 48 | 152128 | 96.38% | 0.32 |
| 295 | test_adapter_forms.py | 48 | 152176 | 96.41% | 0.77 |
| 296 | test_walk_receipt.py | 48 | 152224 | 96.44% | 2.22 |
| 297 | test_window_artifacts.py | 48 | 152272 | 96.47% | 2.68 |
| 298 | test_doctor_access.py | 48 | 152320 | 96.50% | 3.27 |
| 299 | test_controller_scope_expansion.py | 48 | 152368 | 96.53% | 19.21 |
| 300 | test_inject_kinds_packet.py | 47 | 152415 | 96.56% | 0.77 |
| 301 | test_story_run_monorepo.py | 47 | 152462 | 96.59% | 2.78 |
| 302 | test_session_identity.py | 46 | 152508 | 96.62% | 0.62 |
| 303 | test_profile_contract.py | 46 | 152554 | 96.65% | 0.77 |
| 304 | test_triage_blocked.py | 46 | 152600 | 96.68% | 1.22 |
| 305 | test_mixed_then_precheck.py | 46 | 152646 | 96.71% | 1.57 |
| 306 | test_test_source.py | 46 | 152692 | 96.74% | 2.44 |
| 307 | test_project_env.py | 46 | 152738 | 96.77% | 2.52 |
| 308 | test_surfaces.py | 46 | 152784 | 96.80% | 3.92 |
| 309 | test_gate_brief_attachments.py | 46 | 152830 | 96.83% | 28.13 |
| 310 | test_s3_s4_chain.py | 46 | 152876 | 96.86% | 34.87 |
| 311 | test_instance_fingerprint.py | 45 | 152921 | 96.88% | 1.92 |
| 312 | test_exploratory_findings.py | 45 | 152966 | 96.91% | 2.32 |
| 313 | test_cost_capture_start_turn.py | 44 | 153010 | 96.94% | 0.62 |
| 314 | test_brief_pack_manual.py | 44 | 153054 | 96.97% | 2.82 |
| 315 | test_controller_resume.py | 44 | 153098 | 97.00% | 46.15 |
| 316 | test_metrics_contract.py | 43 | 153141 | 97.02% | 5.68 |
| 317 | test_traceability.py | 43 | 153184 | 97.05% | 8.35 |
| 318 | test_story_step_decide.py | 43 | 153227 | 97.08% | 49.83 |
| 319 | test_bug_filing.py | 42 | 153269 | 97.11% | 6.48 |
| 320 | test_changelog_assemble.py | 42 | 153311 | 97.13% | 11.76 |
| 321 | test_line_endings.py | 41 | 153352 | 97.16% | 0.77 |
| 322 | test_manual_look.py | 41 | 153393 | 97.18% | 2.27 |
| 323 | test_context_bundle.py | 41 | 153434 | 97.21% | 3.03 |
| 324 | test_stage_critic_route.py | 41 | 153475 | 97.24% | 43.4 |
| 325 | test_publication_gates.py | 40 | 153515 | 97.26% | 0.57 |
| 326 | test_words_carry.py | 40 | 153555 | 97.29% | 27.59 |
| 327 | test_gate_open_items.py | 39 | 153594 | 97.31% | 1.52 |
| 328 | test_live_audit_contract.py | 39 | 153633 | 97.34% | 1.77 |
| 329 | test_requirement_sources.py | 39 | 153672 | 97.36% | 2.32 |
| 330 | test_login_recipe_apply.py | 39 | 153711 | 97.39% | 7.14 |
| 331 | test_finish_unreadable.py | 38 | 153749 | 97.41% | 1.17 |
| 332 | test_probe_container_answer.py | 38 | 153787 | 97.43% | 1.57 |
| 333 | test_profile_shared_root.py | 37 | 153824 | 97.46% | 2.07 |
| 334 | test_stand_gaps.py | 37 | 153861 | 97.48% | 3.74 |
| 335 | test_delivery_ownership.py | 37 | 153898 | 97.50% | 6.33 |
| 336 | test_activity_session_identity.py | 36 | 153934 | 97.53% | 2.33 |
| 337 | test_place_driver.py | 36 | 153970 | 97.55% | 5.78 |
| 338 | test_install_manifest.py | 35 | 154005 | 97.57% | 0.47 |
| 339 | test_smoke_report.py | 35 | 154040 | 97.59% | 2.32 |
| 340 | test_env_selected_stand.py | 35 | 154075 | 97.62% | 3.93 |
| 341 | test_probe_gap_word.py | 35 | 154110 | 97.64% | 83.52 |
| 342 | test_reporters.py | 34 | 154144 | 97.66% | 0.72 |
| 343 | test_exit_gate_grounding.py | 34 | 154178 | 97.68% | 1.07 |
| 344 | test_walk_brief.py | 34 | 154212 | 97.70% | 3.06 |
| 345 | test_fill_new_account.py | 34 | 154246 | 97.72% | 4.73 |
| 346 | test_refusal_registry.py | 34 | 154280 | 97.75% | 7.14 |
| 347 | test_subagent_journal.py | 34 | 154314 | 97.77% | 19.92 |
| 348 | test_gate_b_orders.py | 33 | 154347 | 97.79% | 44.23 |
| 349 | test_story_run_s5_parallel.py | 33 | 154380 | 97.81% | 77.82 |
| 350 | test_role_permissions.py | 32 | 154412 | 97.83% | 0.31 |
| 351 | test_manual_observations.py | 32 | 154444 | 97.85% | 2.88 |
| 352 | test_report_env.py | 32 | 154476 | 97.87% | 4.53 |
| 353 | test_s3_strategist_rounds.py | 32 | 154508 | 97.89% | 13.8 |
| 354 | test_detector_named_story.py | 32 | 154540 | 97.91% | 28.99 |
| 355 | test_s6_lane_admission.py | 31 | 154571 | 97.93% | 17.48 |
| 356 | test_triage_control.py | 31 | 154602 | 97.95% | 85.02 |
| 357 | test_session_handoff.py | 30 | 154632 | 97.97% | 1.77 |
| 358 | test_inject_notices.py | 30 | 154662 | 97.99% | 1.82 |
| 359 | test_retro_orchestrator_driver.py | 30 | 154692 | 98.01% | 2.22 |
| 360 | test_manual_surprise.py | 30 | 154722 | 98.03% | 2.32 |
| 361 | test_s7_repair_review.py | 30 | 154752 | 98.04% | 34.03 |
| 362 | test_external_writes_bug_refusals.py | 29 | 154781 | 98.06% | 0.47 |
| 363 | test_environment_create.py | 29 | 154810 | 98.08% | 1.62 |
| 364 | test_s6_reprove_manual.py | 29 | 154839 | 98.10% | 8.74 |
| 365 | test_grounding_share.py | 29 | 154868 | 98.12% | 17.26 |
| 366 | test_s0_key_form.py | 29 | 154897 | 98.14% | 25.81 |
| 367 | test_s7_investigation_driver.py | 29 | 154926 | 98.16% | 33.16 |
| 368 | test_exit_gate_digest_source.py | 28 | 154954 | 98.17% | 0.87 |
| 369 | test_frontend_reader.py | 28 | 154982 | 98.19% | 0.87 |
| 370 | test_estimate_record.py | 28 | 155010 | 98.21% | 1.07 |
| 371 | test_source_prefix_probe.py | 28 | 155038 | 98.23% | 1.17 |
| 372 | test_project_gitignore.py | 28 | 155066 | 98.24% | 1.22 |
| 373 | test_question_lines_unread.py | 28 | 155094 | 98.26% | 1.82 |
| 374 | test_event_store.py | 28 | 155122 | 98.28% | 2.92 |
| 375 | test_project_decisions_change_request.py | 28 | 155150 | 98.30% | 4.53 |
| 376 | test_case_gates.py | 28 | 155178 | 98.31% | 7.79 |
| 377 | test_controller_stage_acceptance.py | 28 | 155206 | 98.33% | 12.02 |
| 378 | test_doctor_context.py | 28 | 155234 | 98.35% | 51.79 |
| 379 | test_browser_inventory_policy.py | 27 | 155261 | 98.37% | 0.68 |
| 380 | test_oh3_23_queue.py | 27 | 155288 | 98.38% | 0.92 |
| 381 | test_stuck_facts.py | 27 | 155315 | 98.40% | 7.54 |
| 382 | test_story_step_start.py | 27 | 155342 | 98.42% | 25.4 |
| 383 | test_brief_pack_timeout.py | 26 | 155368 | 98.44% | 1.13 |
| 384 | test_retro_numbers.py | 26 | 155394 | 98.45% | 1.17 |
| 385 | test_dashboard_task_price.py | 26 | 155420 | 98.47% | 2.87 |
| 386 | test_case_stamp.py | 26 | 155446 | 98.48% | 9.54 |
| 387 | test_grounding_schema.py | 26 | 155472 | 98.50% | 10.09 |
| 388 | test_report_hook_signals.py | 25 | 155497 | 98.52% | 0.67 |
| 389 | test_execution_fingerprint_records.py | 25 | 155522 | 98.53% | 1.82 |
| 390 | test_s5_settled_oracle.py | 25 | 155547 | 98.55% | 9.44 |
| 391 | test_launch_path_costs.py | 25 | 155572 | 98.56% | 11.09 |
| 392 | test_acceptance_semantics.py | 24 | 155596 | 98.58% | 2.03 |
| 393 | test_manual_fill_human.py | 24 | 155620 | 98.59% | 2.09 |
| 394 | test_codex_hooks_matchers.py | 24 | 155644 | 98.61% | 35.29 |
| 395 | test_handoff_inline_values.py | 24 | 155668 | 98.63% | 36.5 |
| 396 | test_project_inventory.py | 23 | 155691 | 98.64% | 0.82 |
| 397 | test_dashboard_events.py | 23 | 155714 | 98.65% | 1.37 |
| 398 | test_config_projection.py | 23 | 155737 | 98.67% | 1.62 |
| 399 | test_manifest_put_keep_unsent.py | 23 | 155760 | 98.68% | 1.72 |
| 400 | test_s1_s2_contract.py | 23 | 155783 | 98.70% | 1.83 |
| 401 | test_launch_wrappers.py | 23 | 155806 | 98.71% | 11.75 |
| 402 | test_controller_rework_scope.py | 23 | 155829 | 98.73% | 13.86 |
| 403 | test_environment_lifecycle.py | 22 | 155851 | 98.74% | 0.87 |
| 404 | test_scoped_invalidation.py | 22 | 155873 | 98.76% | 0.87 |
| 405 | test_retro_prior_tried.py | 22 | 155895 | 98.77% | 1.57 |
| 406 | test_stand_gap_remedy.py | 22 | 155917 | 98.78% | 1.92 |
| 407 | test_s8_reporting_regressions.py | 22 | 155939 | 98.80% | 2.68 |
| 408 | test_two_folders.py | 22 | 155961 | 98.81% | 2.82 |
| 409 | test_person_owned_paths.py | 22 | 155983 | 98.82% | 12.65 |
| 410 | test_brief_pack_roles.py | 22 | 156005 | 98.84% | 45.58 |
| 411 | test_planning_policy.py | 21 | 156026 | 98.85% | 0.47 |
| 412 | test_report_manual_counted.py | 21 | 156047 | 98.87% | 1.92 |
| 413 | test_mixed_then_outcomes.py | 21 | 156068 | 98.88% | 2.47 |
| 414 | test_artifact_sections.py | 21 | 156089 | 98.89% | 3.13 |
| 415 | test_guard_window_identity.py | 21 | 156110 | 98.91% | 7.24 |
| 416 | test_profile_reader.py | 21 | 156131 | 98.92% | 13.45 |
| 417 | test_controller_release.py | 21 | 156152 | 98.93% | 14.76 |
| 418 | test_config_fill.py | 21 | 156173 | 98.95% | 39.08 |
| 419 | test_scoped_review_verdict.py | 20 | 156193 | 98.96% | 0.87 |
| 420 | test_stage_of_dispatch.py | 20 | 156213 | 98.97% | 0.87 |
| 421 | test_s5_plan.py | 20 | 156233 | 98.98% | 9.63 |
| 422 | test_s5_kind_readers.py | 20 | 156253 | 99.00% | 21.72 |
| 423 | test_probe_binding.py | 20 | 156273 | 99.01% | 22.59 |
| 424 | test_hook_signal_rows.py | 19 | 156292 | 99.02% | 0.77 |
| 425 | test_execution_metrics_adapter.py | 19 | 156311 | 99.03% | 0.83 |
| 426 | test_resume_story_isolation.py | 19 | 156330 | 99.04% | 1.12 |
| 427 | test_d1_gate_words.py | 19 | 156349 | 99.06% | 1.87 |
| 428 | test_bug_confirmation.py | 19 | 156368 | 99.07% | 2.2 |
| 429 | test_version_coherence.py | 19 | 156387 | 99.08% | 2.27 |
| 430 | test_case_appendix.py | 18 | 156405 | 99.09% | 1.76 |
| 431 | test_story_step_pause.py | 18 | 156423 | 99.10% | 5.49 |
| 432 | test_walk_oracle.py | 17 | 156440 | 99.11% | 1.37 |
| 433 | test_manual_requests_seen.py | 17 | 156457 | 99.13% | 1.77 |
| 434 | test_project_approach.py | 17 | 156474 | 99.14% | 2.62 |
| 435 | test_scheduler_output_drain.py | 17 | 156491 | 99.15% | 3.03 |
| 436 | test_red_sandbox_node_ids.py | 17 | 156508 | 99.16% | 5.49 |
| 437 | test_delivery_owner_case_defect.py | 17 | 156525 | 99.17% | 5.78 |
| 438 | test_decision_classes.py | 17 | 156542 | 99.18% | 17.86 |
| 439 | test_bug_link_s9.py | 17 | 156559 | 99.19% | 20.74 |
| 440 | test_bind_dispatch_list.py | 17 | 156576 | 99.20% | 52.69 |
| 441 | test_charter_form.py | 16 | 156592 | 99.21% | 1.62 |
| 442 | test_candidate_defects.py | 16 | 156608 | 99.22% | 2.1 |
| 443 | test_stage_review_person_pass.py | 16 | 156624 | 99.23% | 2.32 |
| 444 | test_findings_per_dispatch.py | 16 | 156640 | 99.24% | 2.97 |
| 445 | test_run_freshness.py | 16 | 156656 | 99.25% | 3.13 |
| 446 | test_controller_brief.py | 16 | 156672 | 99.26% | 5.03 |
| 447 | test_http_client.py | 16 | 156688 | 99.27% | 5.78 |
| 448 | test_handed_to_person.py | 16 | 156704 | 99.28% | 5.9 |
| 449 | test_case_versions.py | 16 | 156720 | 99.29% | 8.49 |
| 450 | test_env_evidence.py | 15 | 156735 | 99.30% | 0.82 |
| 451 | test_case_id_form.py | 15 | 156750 | 99.31% | 1.07 |
| 452 | test_factory_dashboard_joins.py | 15 | 156765 | 99.32% | 1.22 |
| 453 | test_walk_lanes.py | 15 | 156780 | 99.33% | 3.28 |
| 454 | test_walk_plan_fields.py | 15 | 156795 | 99.34% | 3.9 |
| 455 | test_driver_journal.py | 15 | 156810 | 99.35% | 9.54 |
| 456 | test_story_step_gate.py | 15 | 156825 | 99.36% | 61.04 |
| 457 | test_gate_b_driver.py | 15 | 156840 | 99.37% | 144.94 |
| 458 | test_telemetry_rotation.py | 14 | 156854 | 99.38% | 0.26 |
| 459 | test_variant_shape.py | 14 | 156868 | 99.39% | 0.32 |
| 460 | test_guard_command_text.py | 14 | 156882 | 99.39% | 0.67 |
| 461 | test_contract.py | 14 | 156896 | 99.40% | 0.87 |
| 462 | test_stage_clock.py | 14 | 156910 | 99.41% | 0.97 |
| 463 | test_exit_gate_advice.py | 14 | 156924 | 99.42% | 2.07 |
| 464 | test_human_reading.py | 14 | 156938 | 99.43% | 2.98 |
| 465 | test_launcher_argv.py | 14 | 156952 | 99.44% | 3.43 |
| 466 | test_story_run_stand_c.py | 14 | 156966 | 99.45% | 24.88 |
| 467 | test_driver_gate_unreadable.py | 13 | 156979 | 99.46% | 1.57 |
| 468 | test_probe_marker.py | 13 | 156992 | 99.46% | 2.42 |
| 469 | test_collect_history_sets.py | 13 | 157005 | 99.47% | 8.48 |
| 470 | test_case_alternatives.py | 12 | 157017 | 99.48% | 0.99 |
| 471 | test_walk_rows.py | 12 | 157029 | 99.49% | 1.22 |
| 472 | test_cost_capture_question_wait.py | 12 | 157041 | 99.50% | 1.37 |
| 473 | test_s7_pretriage.py | 12 | 157053 | 99.50% | 1.97 |
| 474 | test_dashboard_restore.py | 12 | 157065 | 99.51% | 2.27 |
| 475 | test_controller_lifecycle_gate.py | 12 | 157077 | 99.52% | 3.34 |
| 476 | test_whole_list_sites.py | 12 | 157089 | 99.53% | 3.83 |
| 477 | test_human_questions.py | 12 | 157101 | 99.53% | 3.98 |
| 478 | test_form_view.py | 12 | 157113 | 99.54% | 20.53 |
| 479 | test_exit_limit_halt_answered.py | 12 | 157125 | 99.55% | 29.8 |
| 480 | test_guard_secrets.py | 11 | 157136 | 99.56% | 0.26 |
| 481 | test_case_identity.py | 11 | 157147 | 99.56% | 1.07 |
| 482 | test_execution_pipeline.py | 11 | 157158 | 99.57% | 1.63 |
| 483 | test_walk_type_chain.py | 11 | 157169 | 99.58% | 1.72 |
| 484 | test_retry_reason.py | 11 | 157180 | 99.58% | 3.33 |
| 485 | test_onboarding_compaction.py | 11 | 157191 | 99.59% | 3.88 |
| 486 | test_stop_after_config.py | 11 | 157202 | 99.60% | 3.88 |
| 487 | test_check_coverage.py | 11 | 157213 | 99.60% | 7.45 |
| 488 | test_project_decisions_refs.py | 11 | 157224 | 99.61% | 9.35 |
| 489 | test_repair_route.py | 11 | 157235 | 99.62% | 47.94 |
| 490 | test_story_run_delivery_b.py | 11 | 157246 | 99.62% | 163.48 |
| 491 | test_obligation_receipt_contract.py | 10 | 157256 | 99.63% | 0.47 |
| 492 | test_dashboard_cost_gap_rows.py | 10 | 157266 | 99.64% | 0.57 |
| 493 | test_row_fields.py | 10 | 157276 | 99.64% | 2.57 |
| 494 | test_resume_doors.py | 10 | 157286 | 99.65% | 52.27 |
| 495 | test_test_files.py | 9 | 157295 | 99.66% | 0.67 |
| 496 | test_file_lock.py | 9 | 157304 | 99.66% | 1.52 |
| 497 | test_one_source_per_fact.py | 9 | 157313 | 99.67% | 1.68 |
| 498 | test_manual_projection.py | 9 | 157322 | 99.67% | 1.92 |
| 499 | test_stage_closure.py | 9 | 157331 | 99.68% | 7.29 |
| 500 | test_handoff_init_author.py | 9 | 157340 | 99.68% | 11.74 |
| 501 | test_conductor_doors.py | 9 | 157349 | 99.69% | 77.58 |
| 502 | test_observation_contract.py | 8 | 157357 | 99.70% | 0.26 |
| 503 | test_run_history_identity.py | 8 | 157365 | 99.70% | 0.37 |
| 504 | test_probe_target_fact.py | 8 | 157373 | 99.71% | 1.47 |
| 505 | test_playwright_identity_local1.py | 8 | 157381 | 99.71% | 2.02 |
| 506 | test_s5_plan_grouping.py | 8 | 157389 | 99.72% | 2.02 |
| 507 | test_receipts_per_function.py | 8 | 157397 | 99.72% | 8.34 |
| 508 | test_story_run_words.py | 8 | 157405 | 99.73% | 26.72 |
| 509 | test_story_step_config.py | 8 | 157413 | 99.73% | 27.86 |
| 510 | test_hooklib_scan.py | 8 | 157421 | 99.74% | 30.36 |
| 511 | test_host_launch_denial.py | 7 | 157428 | 99.74% | 0.57 |
| 512 | test_manual_capture_login_unknown.py | 7 | 157435 | 99.74% | 0.57 |
| 513 | test_s9_summary_refresh.py | 7 | 157442 | 99.75% | 0.62 |
| 514 | test_sizing_impact_scale.py | 7 | 157449 | 99.75% | 0.77 |
| 515 | test_d1_answer_card.py | 7 | 157456 | 99.76% | 0.97 |
| 516 | test_config_discovery.py | 7 | 157463 | 99.76% | 1.83 |
| 517 | test_hook_lifecycle.py | 7 | 157470 | 99.77% | 1.97 |
| 518 | test_stage_done_lock_order.py | 7 | 157477 | 99.77% | 2.49 |
| 519 | test_adapter_matrix.py | 7 | 157484 | 99.78% | 3.58 |
| 520 | test_controller_paths.py | 7 | 157491 | 99.78% | 3.89 |
| 521 | test_s3_remarks.py | 7 | 157498 | 99.78% | 9.52 |
| 522 | test_driver_resume_checkpoint.py | 7 | 157505 | 99.79% | 13.3 |
| 523 | test_fb14_real_state.py | 7 | 157512 | 99.79% | 17.56 |
| 524 | test_worker_lifecycle.py | 6 | 157518 | 99.80% | 0.52 |
| 525 | test_slices_on_demand.py | 6 | 157524 | 99.80% | 0.72 |
| 526 | test_migrate_coverage.py | 6 | 157530 | 99.80% | 0.82 |
| 527 | test_diagnosis_honesty.py | 6 | 157536 | 99.81% | 0.97 |
| 528 | test_driver_reads_answers.py | 6 | 157542 | 99.81% | 1.72 |
| 529 | test_open_list_fields.py | 6 | 157548 | 99.82% | 3.03 |
| 530 | test_s5_window_scope.py | 6 | 157554 | 99.82% | 3.94 |
| 531 | test_repair_marker.py | 6 | 157560 | 99.82% | 4.08 |
| 532 | test_case_id_form_texts.py | 6 | 157566 | 99.83% | 4.43 |
| 533 | test_denial_scope.py | 6 | 157572 | 99.83% | 12.95 |
| 534 | test_profile_shape_gate.py | 6 | 157578 | 99.84% | 24.1 |
| 535 | test_consumer_close_route.py | 6 | 157584 | 99.84% | 35.43 |
| 536 | test_story_run_stand.py | 6 | 157590 | 99.84% | 35.58 |
| 537 | test_window_stage_contract.py | 5 | 157595 | 99.85% | 0.36 |
| 538 | test_host_adapter.py | 5 | 157600 | 99.85% | 0.37 |
| 539 | test_app_boundary_notices.py | 5 | 157605 | 99.85% | 0.62 |
| 540 | test_broad_status.py | 5 | 157610 | 99.86% | 0.67 |
| 541 | test_collect_gaps.py | 5 | 157615 | 99.86% | 0.67 |
| 542 | test_lifecycle_integration.py | 5 | 157620 | 99.86% | 1.07 |
| 543 | test_case_glob_strict.py | 5 | 157625 | 99.87% | 2.02 |
| 544 | test_dashboard_task_row.py | 5 | 157630 | 99.87% | 2.17 |
| 545 | test_validate_notices.py | 5 | 157635 | 99.87% | 2.24 |
| 546 | test_person_word_stages.py | 5 | 157640 | 99.87% | 4.48 |
| 547 | test_reporter_choice.py | 5 | 157645 | 99.88% | 4.83 |
| 548 | test_probe_gap_door.py | 5 | 157650 | 99.88% | 4.88 |
| 549 | test_handoff_check_investigation.py | 5 | 157655 | 99.88% | 9.56 |
| 550 | test_read_json.py | 5 | 157660 | 99.89% | 14.67 |
| 551 | test_gate_lines_over_approval.py | 5 | 157665 | 99.89% | 36.07 |
| 552 | test_controller_task_flag.py | 5 | 157670 | 99.89% | 39.58 |
| 553 | test_case_lifecycle.py | 4 | 157674 | 99.90% | 0.16 |
| 554 | test_record_schema.py | 4 | 157678 | 99.90% | 0.26 |
| 555 | test_traceability_contract.py | 4 | 157682 | 99.90% | 0.38 |
| 556 | test_hook_notices.py | 4 | 157686 | 99.90% | 0.41 |
| 557 | test_role_digest.py | 4 | 157690 | 99.91% | 0.77 |
| 558 | test_orchestrator_share.py | 4 | 157694 | 99.91% | 1.07 |
| 559 | test_reporter_contract_format.py | 4 | 157698 | 99.91% | 1.12 |
| 560 | test_whole_identifier.py | 4 | 157702 | 99.91% | 1.37 |
| 561 | test_role_digest_template.py | 4 | 157706 | 99.92% | 1.42 |
| 562 | test_triage_identity.py | 4 | 157710 | 99.92% | 1.72 |
| 563 | test_exit_gate_lock_wait.py | 4 | 157714 | 99.92% | 2.43 |
| 564 | test_project_decisions_doc_refs.py | 4 | 157718 | 99.92% | 2.77 |
| 565 | test_refuse_case.py | 4 | 157722 | 99.93% | 3.17 |
| 566 | test_s0_close_order.py | 4 | 157726 | 99.93% | 3.28 |
| 567 | test_brief_stand_helpers.py | 4 | 157730 | 99.93% | 3.52 |
| 568 | test_retro_always_full.py | 4 | 157734 | 99.93% | 3.73 |
| 569 | test_detector_unreadable.py | 3 | 157737 | 99.94% | 0.72 |
| 570 | test_probe_plugin_param.py | 3 | 157740 | 99.94% | 0.82 |
| 571 | test_run_execution_metrics.py | 3 | 157743 | 99.94% | 0.87 |
| 572 | test_worker_lifecycle_active.py | 3 | 157746 | 99.94% | 1.02 |
| 573 | test_delivery_manifest_refresh.py | 3 | 157749 | 99.94% | 1.37 |
| 574 | test_identity_proof_contract.py | 3 | 157752 | 99.95% | 1.37 |
| 575 | test_plan_warnings_info.py | 3 | 157755 | 99.95% | 1.77 |
| 576 | test_stand_lease_walk.py | 3 | 157758 | 99.95% | 1.87 |
| 577 | test_case_store.py | 3 | 157761 | 99.95% | 2.02 |
| 578 | test_dispatch_identity.py | 3 | 157764 | 99.95% | 2.42 |
| 579 | test_execution_scheduler_cli.py | 3 | 157767 | 99.96% | 2.82 |
| 580 | test_diff_accounting_readers.py | 3 | 157770 | 99.96% | 22.18 |
| 581 | test_selftest_ran_nothing.py | 3 | 157773 | 99.96% | 41.07 |
| 582 | test_runtime_paths.py | 3 | 157776 | 99.96% | 43.05 |
| 583 | test_telemetry_sweep.py | 2 | 157778 | 99.96% | 0.21 |
| 584 | test_retry_reason_contract.py | 2 | 157780 | 99.96% | 0.37 |
| 585 | test_stand_gap_contract.py | 2 | 157782 | 99.96% | 0.42 |
| 586 | test_evidence_ref_contract.py | 2 | 157784 | 99.97% | 0.47 |
| 587 | test_cost_capture_recapture.py | 2 | 157786 | 99.97% | 0.52 |
| 588 | test_source_peek.py | 2 | 157788 | 99.97% | 0.52 |
| 589 | test_console_plain_and_same_bytes.py | 2 | 157790 | 99.97% | 0.57 |
| 590 | test_install_smoke_layout.py | 2 | 157792 | 99.97% | 0.62 |
| 591 | test_codex_message_semantics.py | 2 | 157794 | 99.97% | 0.82 |
| 592 | test_cost_capture_ownership.py | 2 | 157796 | 99.97% | 1.92 |
| 593 | test_rework_dispatch_files.py | 2 | 157798 | 99.97% | 2.22 |
| 594 | test_stages.py | 2 | 157800 | 99.98% | 3.53 |
| 595 | test_rows_owed.py | 2 | 157802 | 99.98% | 3.82 |
| 596 | test_screenshots_gate_b.py | 2 | 157804 | 99.98% | 4.22 |
| 597 | test_role_policy_reads.py | 2 | 157806 | 99.98% | 4.91 |
| 598 | test_brief_pack_sd_head.py | 2 | 157808 | 99.98% | 6.31 |
| 599 | test_s5_plan_windows.py | 2 | 157810 | 99.98% | 8.29 |
| 600 | test_collect_skill.py | 2 | 157812 | 99.98% | 9.17 |
| 601 | test_story_run_s0_stand_trace.py | 2 | 157814 | 99.98% | 40.02 |
| 602 | test_hooklib_sorted_paths.py | 1 | 157815 | 99.99% | 0.21 |
| 603 | test_story_version.py | 1 | 157816 | 99.99% | 0.21 |
| 604 | test_artifact_registry.py | 1 | 157817 | 99.99% | 0.26 |
| 605 | test_hooklib_append_jsonl.py | 1 | 157818 | 99.99% | 0.26 |
| 606 | test_question_bug_contract.py | 1 | 157819 | 99.99% | 0.31 |
| 607 | test_plan_contract_text.py | 1 | 157820 | 99.99% | 0.46 |
| 608 | test_cost_capture_resumed_agent.py | 1 | 157821 | 99.99% | 0.47 |
| 609 | test_lineage_root.py | 1 | 157822 | 99.99% | 0.57 |
| 610 | test_hooklib_subagent_meta.py | 1 | 157823 | 99.99% | 0.67 |
| 611 | test_dashboard_single_source.py | 1 | 157824 | 99.99% | 0.72 |
| 612 | test_verdict_reason_order.py | 1 | 157825 | 99.99% | 0.72 |
| 613 | test_role_digest_notes.py | 1 | 157826 | 99.99% | 0.97 |
| 614 | test_coverage_targeted_projection.py | 1 | 157827 | 99.99% | 1.02 |
| 615 | test_validator_class.py | 1 | 157828 | 99.99% | 1.32 |
| 616 | test_ahead_cards_rules.py | 1 | 157829 | 99.99% | 1.42 |
| 617 | test_source_stage_integration.py | 1 | 157830 | 99.99% | 1.43 |
| 618 | test_question_register_near.py | 1 | 157831 | 100.00% | 1.47 |
| 619 | test_ahead_cards.py | 1 | 157832 | 100.00% | 3.12 |
| 620 | test_gate_a_settled_forks.py | 1 | 157833 | 100.00% | 3.42 |
| 621 | test_stage_done.py | 1 | 157834 | 100.00% | 14.06 |
| 622 | test_exit_ask_tools.py | 1 | 157835 | 100.00% | 26.49 |
| 623 | test_handoff_rows_prefill.py | 1 | 157836 | 100.00% | 34.89 |
| 624 | test_story_run_loop.py | 1 | 157837 | 100.00% | 65.73 |
| 625 | test_story_run_wait.py | 1 | 157838 | 100.00% | 104.4 |

Ok files the cover never needed (63): test_actor_control_rule.py, test_answer_rework_pairs.py, test_bare_calls_live.py, test_bind_repair_dispatch.py, test_case_id_texts_sweep.py, test_charters_s5_s9.py, test_code_critic_probe_rule.py, test_codex_host_reference.py, test_conductor_investigates_first.py, test_controller_blocks.py, test_controller_doors.py, test_cost_capture_lock_scope.py, test_cost_capture_nonfactory_summary.py, test_cost_capture_sticky_attribution.py, test_cost_capture_subagent_usage.py, test_coverage_controller_integration.py, test_dashboard_cost_widgets.py, test_delivery_visibility.py, test_exit_gate_s7_investigation.py, test_field_producers.py, test_finalization_flow.py, test_fixes_13797.py, test_form_at_stop.py, test_gate_a_two_documents.py, test_gate_decision_manual_pass.py, test_gate_ordered_reporter.py, test_gate_vocabulary.py, test_grammar.py, test_halt_resume_door.py, test_harness_cwd_guard.py, test_host_probe_handback.py, test_instance_records.py, test_judgment_census.py, test_ledger_matching.py, test_manual_seed_path.py, test_manual_window.py, test_metrics_already_run.py, test_no_real_claude.py, test_onboarding_markers.py, test_pinned_lifecycle.py, test_postcompact_reload.py, test_profile_gate.py, test_project_decisions_tables.py, test_project_root.py, test_rc1_14_rule_lines.py, test_reducer_recovery.py, test_remedy_reporter_contract.py, test_report_texts.py, test_resume_packet.py, test_s4_findings_glob.py, test_s7_reorder_fixture.py, test_stage_cards.py, test_stage_joints_12586.py, test_state_exits.py, test_state_portability.py, test_story_run_s5_n1_frozen.py, test_story_run_stand_b.py, test_story_step.py, test_story_step_prompt.py, test_task_price_unestimated.py, test_ticket_rework_stages.py, test_tried_table.py, test_walk_two_actors.py

## C. Not measured and red

| file | status | exit | timed out | seconds |
|---|---|---|---|---|
| test_artifact_writers.py | not-measured | 0 | False | 0.37 |
| test_blocked_by_env_texts.py | not-measured | 0 | False | 0.32 |
| test_case_role_twins.py | not-measured | 0 | False | 0.22 |
| test_case_roles_twin_rules.py | not-measured | 0 | False | 0.22 |
| test_critic_lines_hf2.py | not-measured | 0 | False | 0.21 |
| test_detection_role_texts.py | not-measured | 0 | False | 0.22 |
| test_driver_golden.py | not-measured | 0 | False | 28.63 |
| test_driver_layers.py | not-measured | 1 | False | 33.8 |
| test_gate_continuation_texts.py | not-measured | 0 | False | 0.21 |
| test_mixed_then_texts.py | not-measured | 0 | False | 0.21 |
| test_recommended_rule.py | not-measured | 0 | False | 0.22 |
| test_red_then_texts.py | not-measured | 0 | False | 0.26 |
| test_s7_control_experiment_texts.py | not-measured | 0 | False | 0.37 |
| test_scout_conflict_rule.py | not-measured | 0 | False | 0.21 |
| test_telemetry_merge.py | red | 1 | False | 1.27 |
| test_time_fork_rule.py | not-measured | 0 | False | 0.27 |
| test_walk_charter.py | not-measured | 0 | False | 1.28 |
