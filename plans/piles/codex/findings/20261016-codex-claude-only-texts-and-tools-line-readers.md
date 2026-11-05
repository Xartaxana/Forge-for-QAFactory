# Тексты, которые ребёнок на Codex Desktop читает, по-прежнему называют только инструменты Claude; читатели строки `tools:` расходятся в умолчании

id: — | кучка: `codex` | от: Dev2 (критик t-029 на дифф t-028, TP2-2406 S3-4 → S3-5, Codex Desktop), 16.10.2026 | приоритет: П2 | кандидат наверх: нет

Решение владельца нужно: нет (техническое).

## Что найдено

t-028 поставил один блок `host_adapter.CODEX_DESKTOP_TOOLS` в инъекцию ролей без Bash, в `brief_pack.NO_SHELL_HEAD`
и в отказы гарда. Вне этих трёх мест ребёнок на Codex Desktop по-прежнему читает тексты, где есть только Read/Grep/
Glob/Write/Edit:

1. `references/common-rules.md:13` — «Search with Grep/Glob, read with Read, Bash for execution only»; :17-21 — чтение
   среза через `offset`/`limit`, которых на Desktop нет (срез там — `rg -n -A/-B`).
2. `story_step.py:255` (launch card) — «fill it with Edit»; `plan_row`/Edit-тексты карточки.
3. `guard_pre_tool.big_read_check` (~:662) — отказ называет `Read` с `offset`/`limit`; сам чек видит только Read, не
   `Get-Content` (большое чтение на Desktop не ловится).

Второе: три читателя строки `tools:` роли расходятся в умолчании, когда строки нет: `host_adapter.role_policy` и
инъекция t-028 — «нет Bash»; `guard_pre_tool.role_ways` (:906-925) и `story_run.py:1408` — «есть Bash». Для Codex
верно первое. Оси симметрии для читателей `tools:` в `docs/SIBLING_MAP.md` нет (критик проверял оси 5 и 11).

## Что предлагается

- Один читатель строки `tools:` (`host_adapter.role_tools`, появился в t-028 попытка 2) для всех четырёх мест и одно
  умолчание; новая ось в SIBLING_MAP тем же коммитом.
- Тексты 1–3: либо второй хост-вариант от того же блока, либо формулировки без имён инструментов («read the file»),
  там, где текст читают оба хоста.

## Детектор

`scripts/tests/test_codex_tool_guidance.py` держит три места t-028; на остальные теста нет — grep
`Read|Grep|Glob|Edit` по role-facing `.md` и по текстам отказов остаётся ручным до правки.
CX1-6 (t-1003): A25 (`audit_factory._dispatch_weight`, `DISPATCH_CAP_BYTES` 58 000) не считает блок `CODEX_DESKTOP_TOOLS` инъекции Codex (+~856 Б: константа 826 + заголовок); у стратега замер критика t-980 55 421 Б + блок ≈ 56 277 Б, запас до капа ≈ 1,7 КБ — A25 не меняется в узле.
перенесено из ветки dev2/codex-overhead-fixes (plans/piles/roles-context/findings/20261016-codex-claude-only-texts-and-tools-line-readers.md), узел: CX1-6
