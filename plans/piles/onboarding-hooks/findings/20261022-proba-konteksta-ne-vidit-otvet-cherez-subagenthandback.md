# Проба доставки контекста роли не видит ответ ребёнка: хост теперь отдаёт отчёт субагента вызовом `SubagentHandback`, а проба читает только текст

id: — | кучка: `onboarding-hooks` | от: владелец, 22.10.2026 («почему не получилось проверить доставку контекста роли?») | приоритет: П1 | кандидат наверх: нет

перенос: hotfix-12586/batch-1 (узел HF1-5; слово владельца 23.10.2026 — срочная отдельная пачка; узел OH3-13 здесь закрывается её хэшем)

Что не так: доктор 0.10.0 на `testproject1-dev-010/testproject1-sdk/test-harness` (сессия `bfffa363-…`, 22.10 12:26) сделал всё по шагу 1b: гард
`verified` (ALLOW прошёл, DENY отказан), диспетчеризация `qa-factory:qa-scout` с `task_name: qa_factory_context_probe` и промптом
`QA_FACTORY_CONTEXT_PROBE`, затем `--check` → `injection: unverified`, и человеку ушло «Подтвердить доставку контекста роли не удалось».

Измерено по транскрипту ребёнка (`…/bfffa363-…/subagents/agent-a672cd1077d7968c3.jsonl`): **контекст доставлен** — инъекция в первом
сообщении ребёнка (манифест тестировщика «delivered by injection at dispatch») и вызов-вызов, и ребёнок ответил ровно тем, что требуется:
`QA_CONTEXT_RECEIVED_027e35281f5df5b27b88dd9d6abd9e3b_END`. Но ответил он **вызовом инструмента** `SubagentHandback({message: …})`: хост
(Claude Code этой версии) говорит каждому субагенту системной вставкой «Your final report is delivered through SubagentHandback … plain
text you write at the end is not delivered».

`scripts/host_probe.py` `check_child` → `_assistant_texts` (строки ~480–550) ищет префикс `QA_CONTEXT_RECEIVED_` только в текстовых блоках
assistant, а любой блок `tool_use` ставит `used_tool = True` (защита от ребёнка, который ПРОЧИТАЛ вызов из файла). Ответ в `input.message`
блока `tool_use` не виден → `answers` пуст → ничего не записано → `unverified`. Даже если бы он был найден, вердикт стал бы `tool_used`.
То есть на текущем хосте проба **не может пройти никогда**, а доктор каждый раз пишет человеку о неудаче, которой нет. Смежно — смок
(`install_smoke.py`: «PASS injection delivers to 'qa-factory:qa-scout'») зелёный, потому что он синтетический и SubagentHandback не знает.

Что сделать: (1) `_assistant_texts` признаёт отчёт ребёнка через `SubagentHandback` как его ответ (`tool_use` с `name ==
'SubagentHandback'` и строковым `input.message`) и не считает этот вызов «использованием инструмента»; любой ДРУГОЙ вызов по-прежнему
`tool_used` (инвариант: ребёнок не мог прочитать вызов сам); (2) форма отчёта хоста — данные, не литерал в коде (имя инструмента отчёта в
`references/`, рядом с прочими формами хоста: Codex `response_item`, Claude `assistant`), AR-5 — хост читается через один адаптер;
(3) тест на транскрипт с `SubagentHandback` (зелёный) и с `Read` + `SubagentHandback` (`tool_used`); (4) смок `install_smoke.py`
получает тот же случай, чтобы синтетика не была зеленее живого хоста (FR-33); (5) пока не исправлено — доктор не пишет человеку
«не удалось» (это OH3-12), а строка в служебном хвосте говорит факт: «проба контекста не умеет читать ответ этой версии хоста».

Свидетель: транскрипт доктора `~/.claude/projects/D--ws-testproject1-dev-010-testproject1-sdk-test-harness/bfffa363-d807-4b17-af92-d9399f3eb6d8.jsonl`
(`--check` 12:26:38: `status: verified`, `injection: unverified`, `next_action: dispatch_context_probe`; после пробы — то же) и транскрипт
ребёнка `…/subagents/agent-a672cd1077d7968c3.jsonl` (последний блок: `tool_use` SubagentHandback с вызовом); `scripts/host_probe.py:480-550`.

Принципы и правила: FR-33, FR-41, FR-59, FR-17, AR-5, AR-28.

Решение владельца нужно: нет.
