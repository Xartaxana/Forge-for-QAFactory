# Завершившийся критик считается живым: возврат через `SubagentHandback` не виден `dispatch_liveness`, и обычная доработка по вердикту требует слова человека

id: — | кучка: `onboarding-hooks` | от: владелец, 22.10.2026 (S5 окно 1 TP1-12586 на `testproject1-dev-010`, 0.10.0) | приоритет: П1 | кандидат наверх: нет

перенос: hotfix-12586/batch-1 (узел HF1-7; слово владельца 23.10.2026 — срочная отдельная пачка; узел OH3-16 здесь закрывается её хэшем)

Что не так: критик кода S5 (`S5-qa-code-critic-1`) закончил ревью и вернул вердикт (TC-001/003/004 приняты, TC-002 — дефект теста, у
автора пусты поля манифеста). Транскрипт ребёнка (`…/e0be59d0-…/subagents/agent-a5e3e542e73023f05.jsonl`) кончается вызовом
`SubagentHandback` в 17:56:58, `meta.json` хоста говорит `"finished": true`. Но фабрика держала диспатч открытым:
- `controller.py --operation recover` → `wait_existing_job`, `cancel_allowed: false`, `liveness: alive` («transcript was written 81s ago»),
  через 10 минут `liveness: unknown` («silent for 650s», «the host receipt of this dispatch is not terminal»);
- `story_step pause` → «host worker is still active or cancellation unacknowledged; preserve progress and wait»;
- `story_step finish` → отказ (окно критика не «receipted»: у автора нет `review_receipt_ref`, пробы чувствительности) — ровно то, что
  критик и нашёл.
Тупик: закрыть нельзя (вердикт «доработать»), поставить на паузу нельзя («живой»), отменить нельзя. Дирижёр ждал ~10 минут, затем попросил
у человека слово; `--operation release` со словами человека освободил диспатч, и `S5-qa-automator-2` ушёл на доработку.

Уточнение Lead 22.10 (проверено по `qa-factory/records/journal.jsonl` проекта): хук SubagentStop на этом хосте СРАБОТАЛ — журнал несёт
`subagent_stop` критика `S5-qa-code-critic-1` со `status: completed` в 17:52:58 и 17:57:01 (второй — после возврата хостом), но с
`return_owner: story_step`: для диспатча, привязанного к `story_step`, хук не пишет `returned_at` в контроллер, а квитанция остаётся
нетерминальной до `story_step finish`. Цена и время роли при этом сняты: `state/cost/<сессия>.json` несёт 19 запросов критика до 17:56:58,
`subagent_stop` — время возврата.

Почему это дефект: возврат роли — факт хоста, и хук его записал, а `dispatch_liveness` для story_step-диспатча его не читает: признаёт только
`task_complete` раннера Codex (`native_stop`, прецедент TP2-2406 — тот же тупик, исправленный только для Codex) или `returned_at`,
которого у story_step-диспатча нет; `SubagentHandback` и флаг `finished` в `meta.json` субагента тоже не читаются — смежно с OH3-13. Отсюда
liveness по свежести файла транскрипта (FR-41: «жив» не измерен), и обычный ход стадии «вердикт → доработка» требует слова человека
(FR-4, P22: слово человека — для решений, а не для того, чтобы протолкнуть фабрику через её же невидимость; AR-25 — у состояния «вернулся с
reject» нет хода без человека). Время окна и деньги дирижёра на ожидание — на каждом reject.

Что сделать: (1) `dispatch_liveness` признаёт возврат Claude Code: последний блок транскрипта — `tool_use` `SubagentHandback` и/или
`meta.json` `finished: true` для этого `toolUseId` → `RETURNED` (не принятие работы: принять или вернуть решает дирижёр); форма
признака — данные адаптера хоста рядом с OH3-13 (AR-5); (2) `subagent_stop` хука со `status: completed` для story_step-диспатча — такой же
признак `RETURNED`, как `task_complete` Codex (один предикат для обоих хостов, AR-5, AR-15); (3) `story_step pause` и доработка по вердикту критика идут без слова человека, если
диспатч `RETURNED`; слово человека остаётся для `alive`/`unknown`; (4) тест на транскрипт с `SubagentHandback` и `meta.finished` → `RETURNED`,
и на транскрипт без них → прежнее поведение; (5) смок `install_smoke.py` получает тот же случай (как OH3-13, FR-33).

Свидетель: сообщения дирижёра владельцу 22.10 («the factory still counts its dispatch as alive because its transcript was written minutes
ago … The factory won't let me cancel it»); транскрипт дирижёра `e0be59d0-9c80-4cde-bbce-55280ba3ee8b.jsonl` (ответы `recover`, отказ
`pause`, `release` по словам `state/words/s5-20261022-4.txt`); `subagents/agent-a5e3e542e73023f05.jsonl` и `.meta.json`;
`scripts/dispatch_liveness.py` (`native_stop`, строки ~375-400; `returned_at`, ~696; non-terminal receipt, ~740-795).

Принципы и правила: P22, FR-4, FR-33, FR-41, AR-5, AR-25.

Решение владельца нужно: нет.
