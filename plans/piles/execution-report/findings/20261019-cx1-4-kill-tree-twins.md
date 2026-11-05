# Две копии убийства дерева процессов остались рядом с `node_ids.kill_tree`

id: — | кучка: `execution-report` | от: билдер CX1-4 (t-1004) по критику t-965 (Q3), 19.10.2026 | приоритет: П3 | кандидат наверх: нет

Что не так / что сделать: CX1-4 сделала `node_ids.kill_tree` публичной (одна копия для сборки, песочницы и планировщика;
рядом `node_ids.run_bounded`, один ограниченный запуск). Двойники остались: `run_suite.kill_tree`
(`scripts/run_suite.py:734`, вызов :1529) и `tests/driver_golden.py:306` (вызов :338). Свести к `node_ids.kill_tree`
(`run_suite` уже вызывает `node_ids` лениво, полный импорт не нужен); зона `execution-probes` (EP1), `run_suite.py` —
не файл этого узла.

Свидетель: `grep -n kill_tree scripts/*.py scripts/tests/*.py` — `node_ids.py:107`, `run_suite.py:734`,
`tests/driver_golden.py:306`; критик `docs/tasks/specs/reviews/t-965-t-958-cx1-4-plan.md` §6 (F-4), Q3.

Принципы и правила: P10, P12, FR-17, FR-54.

Решение владельца нужно: нет.
