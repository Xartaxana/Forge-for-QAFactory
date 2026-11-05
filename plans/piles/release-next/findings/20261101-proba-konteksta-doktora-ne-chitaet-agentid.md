# Проба контекста доктора остаётся unverified на Claude Code 2.1.309: запись ответа Agent читает не тот ключ id

id: — | кучка: `release-next` | от: прогон доктора на MyBooks, 01.11.2026 | приоритет: П1 | кандидат наверх: нет

Что не так: ребёнок доктора `agent-add467ff79b5988cd` вернул верный вызов
`QA_CONTEXT_RECEIVED_ff289f67f1467a019839ccb9958200f5_END` (контекст доставлен), но
`qa-factory/state/host-probe.json` хранит `injection.status: emitted` без `agent_id`, и `host_probe --check`
судит пробу `unverified`. Ответ хоста на запуск Agent: `{"isAsync":true,"status":"async_launched","agentId":"add467ff…"}`;
`scripts/host_dispatch.py:263` (`record`, ветка PostToolUse) читает только `agent_id` / `id` / `task_path` / `task_name`,
поэтому `agent` = None, `bind_injection` не запускается, `host_probe.check_child:621` выходит на
`if not proof.get('agent_id')`. Новый `scripts/agent_autobind.py:39` уже читает `AGENT_ID_FIELD = "agentId"` (замер):
два читателя одной формы хоста (AR-13, AR-5).

Что сделать (направление выбрано): ключ(и) id запуска в ответе Agent хоста — строка данных в
`references/host-report-forms.json`, её читает одна функция `host_adapter`; её вызывают `host_dispatch.record` (оба места,
:263 и :273) и `agent_autobind`. Соседей подмести: любой другой читатель id из `tool_response` в `scripts/`
(`host_dispatch.record` ветка SubagentStop — узел OH3-19; привязка id агента — DC1-30).
Тесты: (1) проба привязывается и судится `delivered` на ответе `{"agentId": …}`, фоновый и обычный запуск; (2) ответ со
старым ключом `agent_id` по-прежнему привязывается (форма не потеряна); (3) ответ без какого-либо ключа id — проба
`unverified` с названной причиной «ответ хоста без id запуска», не `delivered` (ошибка допустима только в сторону
`unverified`); (4) `install_smoke.py` получает ту же форму ответа, чтобы smoke не был зеленее живого хоста (FR-33).

Свидетель: сессия `1c293fa7-ab85-430a-9bd5-9e7cb36f3ea2`, 01.11.2026 22:10; `scripts/host_dispatch.py:263`,
`scripts/host_probe.py:621`, `scripts/agent_autobind.py:39`.

Принципы и правила: P1, P14; FR-11, FR-16, FR-33, FR-59; AR-5, AR-13.

Решение владельца нужно: нет (слово владельца 01.11.2026 «в пересборку бэклога»; П1).

## Вторая сторона, 02.11.2026

Разбор прогона LOCAL-1 (`docs/tasks/specs/reviews/t-1666-local-1-run-review.md`, П-8): гейт выхода судит детей пробы контекста доктора
как роли. В `records/journal.jsonl` проекта MyBooks J:1-6 — три `subagent_stop` с `task: unknown-task` и три `gate_block` на
`QA_CONTEXT_RECEIVED_*_END`: ребёнок пробы не роль стадии, у него нет формы передачи и дайджеста, гейт требует их и блокирует.
Что менять (тот же узел RN1-1, направление выбрано Lead, 02.11.2026): гейт выхода (`scripts/exit_gate.py`) не судит ребёнка, чей диспатч —
проба доктора (метка пробы в диспатче/`host-probe.json`; одна функция-читатель метки, AR-13), и не пишет для него `gate_block`.
Тест: `subagent_stop` ребёнка пробы с маркером `QA_CONTEXT_RECEIVED_<hex>_END` → нет `gate_block`; тот же стоп роли стадии без формы → блок
по-прежнему (отрицательный контроль).
