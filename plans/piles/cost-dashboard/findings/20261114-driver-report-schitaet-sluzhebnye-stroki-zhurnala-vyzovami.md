# Измерители считают служебные строки журнала драйвера вызовами: `compare.driver_report` (и `report_run.journal`)

id: — | кучка: `cost-dashboard` | от: критик темы CL4-1, `docs/tasks/specs/reviews/20261113-cl4-1-topic-code-critic.md` (строка очереди Q3, ось карты 6); кучку выбрал Lead (узла `report_run.journal` в кучках нет: см. `docs/tasks/specs/reports/20261113-findings-queue-report.md`, «NOT FILED» п. 1) | приоритет: П3 | кандидат наверх: нет

## Что не так

Класс фабрики: **служебные строки журнала считаются как вызовы (P18: цена одна и истинная; FR-41; ось карты 6, измерители)**. `experiments/measurers/compare.py:266-284`
(`driver_report`) считает каждую строку журнала вызовом в `by_kind` / `by_role`: `window_round` и `process` попадают в корзины вызовов, как и `launched` и `gate_repair`
(последние две — старше этой находки). Тот же класс у `report_run.journal` (`:141-158`), который спека CL4-1 числит «в очереди»; носителя в кучках у него не было, находка
его создаёт: оба места — один узел. Остальные читатели (`stage_role_table`, `spend_by_dispatch`, `context_shape`, `code_friction`) фильтруют по сессии или виду — критик их прошёл.

## Что именно менять

1. `experiments/measurers/compare.py` (`driver_report`) и `experiments/measurers/report_run.py` (`journal`): служебные виды строк (`window_round`, `process`, `launched`, `gate_repair`)
   не считаются вызовами; перечень служебных видов — один (данные, а не два списка в двух файлах: рядом с прайс-строкой вида из CL4-1 N1), оба измерителя читают его.
2. Строки, не посчитанные как вызовы, печатаются отдельной строкой «bookkeeping rows: N» (не молча: FR-41).
3. Тест измерителя (FR-28, таблица случаев): журнал с вызовом, `window_round`, `process`, `launched`, `gate_repair` — вызовов один, служебных четыре; пустой журнал — ноль и ноль.

Принципы и правила: P18; FR-28, FR-41, FR-54; AR-13.

Решение владельца нужно: нет.
