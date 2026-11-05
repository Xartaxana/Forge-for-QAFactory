# Текст отказа гарда цитирует цифры чужого тикета: «20 whole rewrites on TP1-13797 cost 8,284 tokens»

id: — | кучка: `words-gates` | от: прогон CART-1 (MyBooks), 31.10.2026 | приоритет: П2 | кандидат наверх: нет

## Что наблюдалось

Свод п. 7.5; отчёт `docs/tasks/specs/reports/t-1633-cart1-run-problems-transcript.md`, строка 35 (S2, `agent-a07c8f`, 01:02:43 UTC): отказ в полной перезаписи `understanding.md`
сказал «20 whole rewrites on TP1-13797 cost 8,284 tokens» — роль проекта MyBooks читает факты другого проекта как свои. Один отказ в прогоне, ≈ 1 мин; но текст стоит при каждом таком отказе в любом проекте.

Носитель (прочитан 31.10.2026): `references/artifact-writers.json`, поле `rewrite_cost` у трёх артефактов — `work/requirements-register.md` (`:37`, «26 whole rewrites … 22,684 tokens»),
`understanding.md` (`:50`, «20 … 8,284»), третий на `:190` («5 … 32,115 tokens … the report is long»); читает `scripts/guard_pre_tool.py` (`:1186`–`:1198`, `entry.get("rewrite_cost")`) и вставляет в отказ дословно.

## Класс

Текст отказа несёт измерение одного проекта как факт (FR-37, P2; FR-41: цифра без носителя в этом прогоне — не факт этого прогона). Не правило CART-1: любой проект, кроме TP1-13797, получает чужую цифру.

## Что именно менять

Направление выбрано: цифра остаётся как пример с названием источника, а не как факт прогона; самое дешёвое — убрать её из отказа, оставить причину.
1. `references/artifact-writers.json`: у трёх записей поле `rewrite_cost` заменить на `rewrite_why` — причина без чисел («every whole rewrite is re-sent as call arguments and re-read on each later turn; it can also revert what earlier turns put there»; для отчёта — «the report is long, so a rewrite is the most expensive single call a role makes»). Числа и тикет уходят в `plans/MEASUREMENTS.md` (там их место: измеренные факты).
2. `scripts/guard_pre_tool.py` (около `:1198`): читать `rewrite_why`; если в записи ещё стоит `rewrite_cost` (проект со своим дополнением таблицы) — выводить, но с пометкой «measured on <источник> in the factory's own runs»; для этого у поля появляется второй ключ `rewrite_cost_source` (обязателен, если есть `rewrite_cost`).
3. Тесты: `scripts/tests/test_artifact_writers.py` — ни в одном `rewrite_*` значении нет подстроки `TP1-` и цифры с запятой-разделителем тысяч; `rewrite_cost` без `rewrite_cost_source` — ошибка таблицы. Один тест на пункт 2: отказ guard для `understanding.md` не содержит `TP1`.
4. Соседи (перебор в том же файле): остальные записи `artifact-writers.json` без `rewrite_cost` — не применимо (`rewrite_cost` найден поиском по `scripts/*.py` и таблице: три записи, читатель один); поиск `TP1-\d+` по `references/*.json` и `scripts/guard_*.py` на цитаты тикета в текстах отказов — первым шагом узла, находки идут строкой в «Ход» (не проверено: сколько их).

Принципы и правила: P2, P10, FR-37, FR-41, AR-1, AR-9.

Решение владельца нужно: нет.
