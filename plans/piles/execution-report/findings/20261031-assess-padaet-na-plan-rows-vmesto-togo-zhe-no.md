# Сломанный `test-plan.json` роняет `assess` исключением вместо того же вердикта `no`; докстринг `branch_records` «`assess` never fails» неверен

id: — | кучка: `execution-report` | от: критик диффа S6 шаги 2, 3, 1d, 1e релиза 0.10.7 (`docs/tasks/specs/reviews/r0107-s6-steps-1d-1e-diff-critic.md`, F-7), 31.10.2026 | приоритет: П2 | кандидат наверх: нет

Что не так / что сделать: проба критика на `029c57e6`: сломанный `test-plan.json` — `check_delivery.assess` поднимает `JSONDecodeError`; тот же файл через `branch_records` напрямую даёт одну запись `branches_unreadable`. Значит `assess` останавливается до новой строки учёта веток, вердикта нет. «Нет вердикта» не проход, но и не тот же `no` с названным владельцем (фабрика), который фабрика обещает на нечитаемое (FR-59, FR-19). Источник падения — чтение плана (`plan_rows`) внутри `assess` до `branch_records`; `coverage_contract.py` в том диффе не менялся, то есть это сосед, живший до S6. Докстринг `check_delivery.branch_records` (`:1910-1914` на `029c57e6`) говорит «`assess` never fails» — неверно, пока читатель плана внутри `assess` не обёрнут; ключ V-8 доказывает только подставленное исключение. Что сделать: падение чтения плана внутри `assess` становится тем же `no` с одной записью-фактом фабрики и именем файла; ключ на настоящем сломанном `test-plan.json` (не на подставленном исключении); докстринг приводится к факту.

Класс (соседи, не обойдены здесь): другие читатели плана внутри `assess` и `report_facts` (`C.parse_plan`, `_case_map`) на сломанном файле — разделяют ли они падение; проверка сканом по карте `docs/SIBLING_MAP.md` (ось читателей плана).

Свидетель: `docs/tasks/specs/reviews/r0107-s6-steps-1d-1e-diff-critic.md` F-7 и «Runs» (P6: `assess raises JSONDecodeError`; `branch_records` direct: `['branches_unreadable']`); `git show 029c57e6:ai-packages/qa-factory/scripts/check_delivery.py` строки 1910-1914 (докстринг), 1964 (вызов `branch_records` в `assess`). Ветка `029c57e6` в базе релиза `3840246e` не влита; номера строк — на её вершине.

Принципы и правила: P21, P22; FR-19, FR-41, FR-59; AR-25, AR-28.

Решение владельца нужно: нет.
