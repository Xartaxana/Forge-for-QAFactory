# Раскладка `qa-factory/state/...` прописана буквально в хуках и скриптах, а не через `runtime_paths`

id: B-249 | кучка: `onboarding-hooks` | от: новое, 01.10 — после живой переустановки; → t-304 N1/N5, FR-60; половина путей пакетов — t-329 п. 3 (02.10) | приоритет: — | кандидат наверх: нет

Что не так / что сделать: **Раскладка `qa-factory/state/...` прописана буквально в хуках и скриптах, а не через `runtime_paths`.** Скаут t-283: все вхождения присоединены к корню проекта (`host_probe.py:33,38,208,265,322,342,357,371,407`, `metric_signals`, `metrics_projection`, `bug_snapshot`, `run_suite:1975`, `guard_pre_tool:2431`, `telemetry_hook:119`, `dashboard_refresh`, `host_dispatch`, `native_context`, `readiness`; константы `onboard_apply.py:85,94`, `red_sandbox.py:77`), то есть работают, но каждое — вторая копия раскладки (FR-13): переезд папки (как `journal.jsonl` state/ → records/) чинится в десятке мест. Относительные к cwd только артефакты: `handoff_init.py:34`, `plan_row.py:177`, `runtime_probe.py:509`. Сделать после живой переустановки: один носитель раскладки (`install-paths.json` + `runtime_paths.record()/state()`), хуки берут путь оттуда; тест-сторож — grep буквальных `qa-factory/state/` вне `runtime_paths`/`install-paths.json` пуст, с контролем.

Свидетель: Скаут t-283 п. 10.

Принципы и правила: FR-13, FR-17

Решение владельца нужно: нет (фраза не найдена)

<!-- piles split: plans/BACKLOG.md, раздел 7 «Релизы, приёмки, инфраструктура разработки»; ячейки строки перенесены дословно -->

Строка BACKLOG.md целиком:

```
| B-249 | **Раскладка `qa-factory/state/...` прописана буквально в хуках и скриптах, а не через `runtime_paths`.** Скаут t-283: все вхождения присоединены к корню проекта (`host_probe.py:33,38,208,265,322,342,357,371,407`, `metric_signals`, `metrics_projection`, `bug_snapshot`, `run_suite:1975`, `guard_pre_tool:2431`, `telemetry_hook:119`, `dashboard_refresh`, `host_dispatch`, `native_context`, `readiness`; константы `onboard_apply.py:85,94`, `red_sandbox.py:77`), то есть работают, но каждое — вторая копия раскладки (FR-13): переезд папки (как `journal.jsonl` state/ → records/) чинится в десятке мест. Относительные к cwd только артефакты: `handoff_init.py:34`, `plan_row.py:177`, `runtime_probe.py:509`. Сделать после живой переустановки: один носитель раскладки (`install-paths.json` + `runtime_paths.record()/state()`), хуки берут путь оттуда; тест-сторож — grep буквальных `qa-factory/state/` вне `runtime_paths`/`install-paths.json` пуст, с контролем. | Скаут t-283 п. 10. | новое, 01.10 — после живой переустановки; → t-304 N1/N5, FR-60; половина путей пакетов — t-329 п. 3 (02.10) | FR-13, FR-17 |
```
