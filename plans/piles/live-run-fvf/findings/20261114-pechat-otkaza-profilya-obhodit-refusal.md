# `window_record.py:267` и `probe_by_code.py:2892` печатают `unknown_profile_refusal` простым текстом, мимо `refusal()`

id: — | кучка: `live-run-fvf` | от: отчёт билдера S-1a, `.claude/worktrees/tbw-t1r/docs/tasks/specs/reports/20261114-t1r-sites-s1a-report.md` («Analogs noticed», второй пункт); спека `docs/tasks/specs/20261114-told-before-work-t1r-sites-spec.md` §6b п. 1 (AR-18) | приоритет: П3 | кандидат наверх: нет

## Что не так

Класс фабрики: **печать отказа роли минует единственный печатающий читатель (AR-18, AR-13)**. Билдер S-1a отметил: `window_record.py:267` и `probe_by_code.py:2892` выводят
`unknown_profile_refusal` обычным текстом и не через `refusal()`. По §6b п. 1 каждый принтер, который отдаёт роли переименованный отказ ER/RS, несёт ту же проекцию `told` (через
`detector_verdict.told_fields`); эти два места в перечне п. 1 не названы, значит строка требования до роли по ним не доходит.

## Что именно менять

1. `ai-packages/qa-factory/scripts/window_record.py` (около `:267`) и `ai-packages/qa-factory/scripts/probe_by_code.py` (около `:2892`): печать `unknown_profile_refusal` идёт через `refusal()`
   (одна JSON-строка с ключом `told`, `error` — те же байты, что сегодня), как у остальных принтеров п. 1.
2. Если у отказа нет строки в таблице 31 id — назвать это в отчёте узла и не придумывать id (§6b п. 6: ни одного литерала вне 31 строки); сайт тогда остаётся в `untold` с причиной.
3. Тест: строка таблицы `T1rs/told/<id>` в `ai-packages/qa-factory/scripts/tests/test_detector_verdict.py` (быстрый файл): печать содержит ровно одну строку `{`, ключ `told` и неизменный `error`.
4. Порядок: после S-1b (там вводится `told_fields` и принтеры п. 1).

Принципы и правила: AR-18, AR-13; FR-14, FR-38.

Решение владельца нужно: нет.
