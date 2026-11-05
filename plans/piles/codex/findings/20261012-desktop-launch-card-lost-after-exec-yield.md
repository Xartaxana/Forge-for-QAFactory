# На Codex Desktop карточка запуска роли (`story_step.py start`) теряется за yield exec-ячейки, а `next` отвечает `wait_existing_job` на диспетч, которого никто не запускал

id: — | кучка: `codex` | от: dev2 (расследование ручного прогона TP2-2406 на Codex Desktop), 12.10.2026 | приоритет: П1 | кандидат наверх: нет

Что не так / что сделать: В ручном Desktop-прогоне TP2-2406 (проект `C:\Runway202609\nightwing-2406-codex`, пакет
`0.9.0+codex.20261011.aeb82d7`) S2 три раза получила диспетч контроллера и ни разу — агента: `request_binding: {}`,
`agent_id` нет, квитанции хоста нет, `next` → `wait_existing_job`, `liveness: unknown`. Причина — не гард и не контроллер,
а носитель карточки запуска. На Desktop единственный носитель вызова `spawn_agent` и команды `bind` — stdout
`story_step.py start` («--- Agent prompt, verbatim ---»), который печатается целиком в самом конце команды. Оркестратор
запускает её в exec-ячейке с `yield_time_ms: 30000`; `tools.exec_command` возвращает то, что накопилось к ~30–38 с, и
никто не опрашивает сессию дальше. `start` на этой машине длится 34–112 с: диспетч записан на 6-й секунде, дальше
`stage_done.py --status running` (57 с отдельно — обновление дашборда/метрик после записи стадии), потом `brief_pack.py`
(4 с) и форма передачи. Попытка 2 (34 с) успела — карточка пришла, `spawn_agent` был вызван и отклонён гардом «host
unverified» (пакет сменился e735a1c → aeb82d7, проба хоста привязана к отпечатку пакета; отказ записан, `recover`
закрыл `never_started` — это штатно). Попытки 1 (45 с) и 3 (88 с) не успели: ячейка «completed» с пустым выводом, пока
`start` ещё писал бриф. Без карточки оркестратор спрашивает `next`; у `next` нет действия «запусти»: диспетч `running`
с момента события `dispatch`, квитанции хоста нет (она появляется только после `spawn_agent`), инвентаря транскриптов на
Codex нет (`hooklib.story_subagent_transcripts` читает раскладку Claude Code `…/subagents/agent-*.jsonl`, на Codex —
пусто → всегда `unknown`, `never_started` недостижим без строки отказа) — ответ `wait_existing_job`, `cancel_allowed:
false`, и оркестратор останавливается «ждать». Попутно `next` попытки 3 выполнялся параллельно с ещё идущим `start`.
Что сделать (минимальная правка, без смены режима): (1) `story_step.py start` печатает строку `dispatched <id>` и
путь карточки сразу после `controller.apply("dispatch")` с flush, а саму карточку кладёт файлом рядом с брифом
(`work/briefs/<id>.launch.md`: промпт, `subagent_type`, команда `bind`) — носитель, который не зависит от yield;
(2) `controller next`/`story_step where` для диспетча `running` без `agent_id`, без квитанции хоста, без `returned_at` и
без строки отказа в истории `desktop` возвращают `launch` с путём карточки вместо `wait_existing_job` (инвариант:
диспетч с квитанцией или `agent_id` по-прежнему `wait_existing_job`; дубль по-прежнему режет `worker_lifecycle.guard`;
id диспетча не меняется); (3) в `SKILL.md`/`phases/*.md` строка: вывод `start` приходит из файла карточки, если ячейка
вернула пустой вывод. Отдельно, не в этой правке: `stage_done --status running` тратит ~1 мин на обновление дашборда на
пути запуска роли (P11: код, от которого стадия дороже).

Свидетель: `~/.codex/sessions/2026/10/12/rollout-2026-10-12T08-28-58-01a12ecc-….jsonl`: попытка 1 — ячейка L106
06:36:10Z, «completed» L114 06:36:45Z (только вывод `context_bundle`), бриф `S2-qa-requirements-tester-1.md` 06:36:53Z,
форма 06:36:54Z, `next` L122 → `wait_existing_job`; попытка 2 — L283 08:55:32Z, вывод L291 08:56:07Z с карточкой, бриф
08:56:04Z, `spawn_agent` L296 08:56:20Z, отказ L298; попытка 3 — L566 09:46:57Z, «completed» L574 09:47:35Z пусто,
событие `dispatch` 09:47:14Z, `stage_transition` 09:47:37Z, бриф 09:48:23Z, форма 09:48:25Z, `next` L578–L581 09:47:40–
09:48:04Z → `wait_existing_job`, `liveness: unknown`, evidence «this host recorded no subagent transcript for the project».
Изолированный прогон (копия `qa-factory/` стори в scratchpad, `release` копии -3, `watch_start.py`): события и
pipeline.json на 5,8 с, stdout 0 байт на 30 с, бриф на 110,5 с, форма и первый байт stdout на 112,1 с (1 668 байт,
карточка есть); отдельно `brief_pack.py` 4 с, `controller next` 3 с, `stage_done.py --status running` 57 с.
`tests/test_controller_rework.py` 280/280 ok — текущее поведение «диспетч без квитанции → `wait_existing_job`/`unknown`»
закреплено тестом, действия `launch` в нём нет.

Принципы и правила: P1, P3, P11, FR-2, FR-14, FR-15, FR-37, FR-40, FR-41, FR-42, FR-48.

Решение владельца нужно: нет.
перенесено из ветки dev2/codex-overhead-fixes (plans/piles/driver-controller/findings/20261012-desktop-launch-card-lost-after-exec-yield.md), узел: CX1-13
