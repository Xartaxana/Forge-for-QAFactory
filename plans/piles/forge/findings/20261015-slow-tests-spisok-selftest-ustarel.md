# Список `SLOW_TESTS` в `selftest.py` разошёлся с замером ночного яруса: 18 файлов дольше 10 с не в списке, 14 из списка быстрее 5 с

id: — | кучка: `forge` | от: ночной `package-full` 15.10 (пайплайн 7920685, job 27713550, `ci-out/selftest.txt`), записал Lead 15.10.2026 15:10 | приоритет: П3 | кандидат наверх: нет

## Что

`selftest.py` печатает две строки INFO по замеру прогона: «over 10s but not in SLOW_TESTS (add to selftest.py)» — 18 файлов
(`test_blocked_by_env_window`, `test_cost_capture_tail`, `test_driver_golden`, `test_gate_brief_and_retro`, `test_install_retire`,
`test_manifest_from_tests`, `test_no_move_seam`, `test_person_words`, `test_probe_by_code_languages`, `test_probe_debt`,
`test_s5_precheck`, `test_stand_identity`, `test_story_progress`, `test_story_run_gate_repair`, `test_story_run_repair_limit`,
`test_story_run_s7`, `test_story_run_stand_identity`, `test_third_verdict`) и «in SLOW_TESTS but finished under 5s (drop)» —
14 файлов (`test_codex_host`, `test_controller_release`, `test_controller_rework_scope`, `test_controller_state`,
`test_critic_rollcall_apply_fixes`, `test_dashboard_restore`, `test_doctor_context`, `test_external_writes`, `test_node_ids`,
`test_red_sandbox_node_ids`, `test_resolver`, `test_s5_process`, `test_source_preflight`, `test_story_run_monorepo`). Список
правится руками и отстаёт; две строки INFO никто не читает (самые медленные: `test_infra_failure` 110 с,
`test_story_run_delivery_b` 109 с, `test_story_run_gate_repair` 100 с, `test_story_run_refusals` 87 с, `test_story_run_s0` 85 с).
Следствие: быстрый ярус (`--fast`) гоняет медленные файлы, а медленные пины (как K11 `test_infra_failure` после d2, t-828)
ломаются только ночью.

## Чинить

Список — файл данных рядом с `selftest.py` (FR-13), обновляемый из замера: `selftest.py --slow-tests --update` переписывает его
по последнему прогону (порог 10 с / 5 с), CI `package-full` печатает дифф и краснеет при расхождении больше N файлов (детектор);
дверь — строка в коммите.

## Куда

Строка F6-18 пачки `forge/batch-6-vhodyashchie-2.md` (D-0044).
