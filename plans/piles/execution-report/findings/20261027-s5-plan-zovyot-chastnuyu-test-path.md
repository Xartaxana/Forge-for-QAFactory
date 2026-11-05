# `s5_plan._project_file` зовёт частную `probe_by_code._test_path`

id: — | кучка: `execution-report` | от: критик t-1320 (SC1-14 цепочка, F-8), 27.10.2026 | приоритет: П3 | кандидат наверх: нет

Что не так / что сделать: `s5_plan._project_file` (`s5_plan.py:376`) вызывает приватную функцию другого модуля, `probe_by_code._test_path`. Приватное имя стало межмодульной зависимостью: любая внутренняя правка `probe_by_code.py` ломает `s5_plan.py` молча. Что сделать: сделать функцию публичной (так записано в ревью) и перевести вызов; прочие вызовы `_test_path` вне `probe_by_code.py` найти grep по `_test_path` и перевести вместе. Ключ: тест на публичную функцию; вызов приватного имени вне `probe_by_code.py` не остаётся ни в одном модуле.

Свидетель: `docs/tasks/specs/reviews/t-1320-sc1-14-chain-diff-review.md`, пункт F-8 (`_project_file` зовёт приватный `probe_by_code._test_path` — очередь, «сделать публичным»).

Принципы и правила: FR-54, FR-17, AR-13.

Решение владельца нужно: нет.

## Дописано 02.11.2026 (критик t-751, TQ1-21)

TQ1-21 добавил три НОВЫХ межмодульных вызова закрытых имён: `probe_by_code._test_path`, `probe_by_code._profile_cwd` (в `base_test_file` / `_is_folder`) и `handoff_check._checkout_path` (в `_resolve_candidate`). Узел, делающий `_test_path` публичным (SC2-16), переносит и эти вызовы. Соседи (охранник относительного пути, S5-близнец без защиты) — `20261102-odin-ohrannik-otnositelnogo-puti-i-sosedi-tq1-21.md`.
