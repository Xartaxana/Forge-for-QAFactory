# `lint_ratchet --check` на базе релиза: 21 новая находка (12 на момент фикс-раунда SC2-37), в том числе `UndefinedName` в страже

id: — | кучка: `package-ci` | от: фикс-раунд SC2-37/CD1-5 релиза 0.10.7 (`docs/tasks/specs/reports/r0107-s4b2-sc2-37-cd1-5-fix.md:58`) и замер на базе `268e7608`, 30.10.2026 | приоритет: П2 | кандидат наверх: нет

Что не так / что сделать: в фикс-раунде SC2-37 `python -B tools/lint_ratchet.py --check --repo .` дал `41 findings, 29 in the baseline, 12 new` — «12 — базовые, в других файлах». На базе `268e7608` тот же инструмент: `50 findings, 29 in the baseline, 21 new, 0 stale (pyflakes 3.2.0)`: счётчик растёт от узла к узлу, потому что каждый билдер не гоняет храповики (builder-rules 7b), а BATCH CANON ещё впереди. Новые: `UnusedImport` в `test_agent_autobind.py` (×2), `test_controller_scope_expansion.py`, `test_copy_detector.py`, `test_cost_capture_role_gaps.py`, `test_cost_capture_settled.py`, `test_dashboard_single_source.py` (×2), `test_proof_level.py:1588`, `test_report_env.py`, `test_report_manual_counted.py` (×2), `test_s6_reprove_manual.py`, `test_s7_rejudge.py:35` (×2); `FStringMissingPlaceholders` в `project_decisions.py:616`, `test_gate_brief_attachments.py:571,576`, `test_run_suite_mine.py:2222`, `test_sizing_impact_scale.py:65`; и `UndefinedName` — `guard_pre_tool.py:1939` (см. отдельную находку в `onboarding-hooks`). Что сделать: убрать все 21 в одном проходе (мелкие правки без смысла), храповик возвращается к `0 new`; в DoD узла, добавляющего тест, — `lint_ratchet.py --check` по своим файлам (одна быстрая команда).

Свидетель: `python -B tools/lint_ratchet.py --check` на `268e7608`: `lint ratchet: 50 findings, 29 in the baseline, 21 new, 0 stale (pyflakes 3.2.0)`.

Принципы и правила: FR-28, FR-32; AR-20.

Решение владельца нужно: нет.
