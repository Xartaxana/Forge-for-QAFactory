# После F4-2 остаются 11 внешних обходов корня, две «догадки о форме» вне переписи и откат дашборда к маркеру выше стори

id: — | кучка: `forge` | от: билдер t-622 / Lead, 09.10 | приоритет: П3 | кандидат наверх: нет

Что не так / что сделать: узел F4-2 (B-309 д) свёл восемь обходов маркера `qa-factory/config.json` в один лист
`runtime_paths.nearest_project`; перепись `scripts/tests/test_runtime_paths.py --census` считает оставшиеся обходы
и держит их список-разрешение `OUTSIDE_WALKS` (11 записей, только уменьшается): `contract._config_location`,
`gate_brief.filing_line` / `portable` / `project_config`, `host_probe._not_a_project`, `launch_check._find_project_root`,
`manual_capture.load_config`, `migrate_artifacts._find_project_root`, `question_stop._find_config`,
`stand_gaps.project_of`, `story_progress._project_of`. Каждый — кандидат на тот же лист отдельным диффом (направление
ошибки потребителя — в спеке, как в t-617 §8). Две «догадки о форме», которые перепись не видит (не обход, а
предположение о раскладке `qa-factory/artifacts`): `report_facts._qa_root` :118 и `dispatch_liveness.in_flight_entry`
:371 — слепое пятно переписи, названо здесь. Отдельно, F5(б) спеки: `dashboard_refresh.refresh_for_task` при отказе
`project_for_task` по всем кандидатам всё ещё откатывается к маркеру ВЫШЕ стори и может писать в проект, чей корень
артефактов стори не содержит; поведение сохранено и свёрнуто на лист (F5(а)), смена смысла — новый узел, не F4-2.

Свидетель: отчёт `docs/tasks/specs/reports/t-622-builder-report.md` (перепись до/после: 19 → 12 обходов,
«0 beyond the leaf and the allowlist»); спека `docs/tasks/specs/t-617-f4-2-project-root.md` §8.4, §8.8, F5.

Принципы и правила: FR-17, FR-54, FR-59; ось 8 SIBLING_MAP (строки «The ONE project-marker walk» и «Outside walks»).

Решение владельца нужно: нет.
