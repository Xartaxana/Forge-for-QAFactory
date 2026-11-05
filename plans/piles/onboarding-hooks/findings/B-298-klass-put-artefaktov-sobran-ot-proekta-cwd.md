# Класс «путь артефактов собран от проекта/cwd» (ось 8, критик t-387 F5)

id: B-298 | кучка: `onboarding-hooks` | от: новое, 03.10 | приоритет: — | кандидат наверх: нет

Что не так / что сделать: **Класс «путь артефактов собран от проекта/cwd» (ось 8, критик t-387 F5):** производственные места вне owns N1b — `dispatch_liveness.py:146/:295`, `env_probe.py:291`, `execution_scheduler.py:177` (форма `parents[1]`), строки `f"qa-factory/artifacts/{task}/…"` как расположение: `story_run.py:2383/:2630`, `ticket_adapter.py:645`, `source_exclusions.py:528`; плюс `hooklib.artifacts_dir` (35 вызовов, fallback на git toplevel/cwd — хуки обязаны оставаться fail-open). N1b фиксирует четыре названных писателя и ставит K-B8 как shrink-only список известных мест; остальное — свой узел после N2. [F04]

Свидетель: Критик t-387 F5/Q11.

Принципы и правила: FR-15, FR-54

Решение владельца нужно: нет (фраза не найдена)

<!-- piles split: plans/BACKLOG.md, раздел 7 «Релизы, приёмки, инфраструктура разработки»; ячейки строки перенесены дословно -->

Строка BACKLOG.md целиком:

```
| B-298 | **Класс «путь артефактов собран от проекта/cwd» (ось 8, критик t-387 F5):** производственные места вне owns N1b — `dispatch_liveness.py:146/:295`, `env_probe.py:291`, `execution_scheduler.py:177` (форма `parents[1]`), строки `f"qa-factory/artifacts/{task}/…"` как расположение: `story_run.py:2383/:2630`, `ticket_adapter.py:645`, `source_exclusions.py:528`; плюс `hooklib.artifacts_dir` (35 вызовов, fallback на git toplevel/cwd — хуки обязаны оставаться fail-open). N1b фиксирует четыре названных писателя и ставит K-B8 как shrink-only список известных мест; остальное — свой узел после N2. [F04] | Критик t-387 F5/Q11. | новое, 03.10 | FR-15, FR-54 |
```
