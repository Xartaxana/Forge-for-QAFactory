# Счётчики `tool_use` в `friction.py` и `cost_capture.py` считают возврат роли (`SubagentHandback`) вызовом инструмента

id: — | кучка: `execution-report` | от: Lead пачки hotfix-12586/1 (dev2), 23.10.2026 | приоритет: П3 | кандидат наверх: нет

Что не так: на Claude Code роль отдаёт ответ вызовом инструмента `SubagentHandback` (форма — данные `references/host-report-forms.json`, ось 22
`docs/SIBLING_MAP.md`). Две меры, считающие блоки `tool_use`, принимают его за обычный вызов:

- `scripts/friction.py:134` — каждый `tool_use` становится вызовом роли (имя, аргумент из `command|file_path|pattern`, для возврата `""`). Один
  возврат прибавляет один вызов к числу вызовов роли и завышает знаменатель отношений трения (FR-55: «трение с нашим кодом мерится на каждом
  прогоне»); маркеров трения на возврате нет.
- `scripts/cost_capture.py:1158-1161` — `tools[name] = tools.get(name, 0) + 1` для каждого `tool_use`, поэтому возврат виден в посессионной
  сводке как имя инструмента. Денег не касается (чтение внешних записей смотрит `command` у Bash/PowerShell), число косметическое.

Третий счётчик (`activity_capture.py:141`) возврат не затрагивает: он проигрывает только блоки с `input.command`, подходящим под
`BACKFILL_CMD` (отчёт t-057, E5).

Что сделать: оба счётчика узнают возврат через `host_adapter.report_forms` (один читатель формы возврата, ось 22) и не считают его вызовом
инструмента; имя возврата в код не вводится (AR-1). Тест: транскрипт с одним возвратом даёт на один вызов меньше, чем сырой подсчёт
блоков; отрицательный контроль — подсчёт без различения возврата. Ось 22 уже перечисляет оба счётчика в строке «Counters of `tool_use` blocks»;
узел исполняет эту очередь.

Свидетель: `docs/tasks/handoffs/t-057-hf1-5.md`, «E5 enumeration — tool_use counters (no change)» (`friction.py:134`: «A handback adds one
call per role return to a role's call count; no friction marker fires on it. Queued; it inflates the denominator of friction ratios by one
call per return»; `cost_capture.py:1158`: «the handback shows as a tool name in the per-session tally (a count, no money effect ...).
Queued; cosmetic»); строки — по дереву пачки, проверены 23.10.2026.

Принципы и правила: FR-17, FR-55, AR-1, AR-5, AR-12.

Решение владельца нужно: нет.
