# Отказ возобновления роли (агент не привязан к стори) не называет двери: стратег с пустой формой передачи не вернулся, пришлось гонять заново

id: — | кучка: `driver-controller` | от: отзыв пользователя Dev6 (TP2-2702), плагин 0.10.x, 28.10.2026 (разбор t-1553) | приоритет: П2 | кандидат наверх: нет

## Что наблюдалось

Слова пользователя, как написаны: «Issue with the strategist, where I was not able to continue "The strategist left its handover form blank, so I'm sending it back to fill it in. Error: PreToolUse:SendMessage hook error: [… telemetry_hook.py inject_context.py]: STAGE GUARD: TP2-2702: resuming 'a9ecead4c9f68f8aa' is blocked — it is not a dispatch this story ran (it knows ['a4cd8d059099f0433', 'a606876c2465ab9ab', 'a93bffd3857a7856b', 'a97ecebc9aa755135', 'aea4fc544a1ee3e8f']). A resume goes back to an agent that already holds this story's context; anything else is a new dispatch and belongs in Agent, where the stage rules apply." Затем дирижёр предложил два варианта: пройти пустую форму по слову человека (`finish --ignore-handoff`) либо запустить стратега заново («This costs another full dispatch»). Пользователь: «I had to run it again.»

Цена: один полный диспатч стратега. Первый вариант (`--ignore-handoff`) был, но пользователь хотел вернуть форму на доработку тому, кто держит контекст, а возврат закрыт.

## Где в коде

Из разбора t-1553 (пункт 2; пути от `ai-packages/qa-factory/`; номера строк проверить по коду при взятии):
- Пустая форма: `scripts/story_step.py:2013-2027` (`finish`, статус `untouched`, код 3), двери `_FORM_DOORS` (`story_step.py:1553-1556`: `handoffs.required: false` и `finish --ignore-handoff`).
- Отказ возобновления: `scripts/stage_guard.py:856-921` `check_resume` (правило 6, инструмент `SendMessage`). Известные id — `_resumable_agents` (`stage_guard.py:956-983`): `agent_id` стадий `pipeline.json` и записей диспатчей `state/controller.json`.
- Ветка «известных агентов нет» (`stage_guard.py:901-914`) называет дверь (`bind`/`agent_id`, `controller.py --operation recover`). Ветка, на которую попал пользователь (известные есть, `:915-921`), двери не называет: только «anything else is a new dispatch and belongs in Agent». Против FR-1, FR-2, FR-57, P15.
- Откуда берётся id агента: не автоматически из результата вызова Agent; только дирижёр пишет `story_step.py bind --task T --dispatch-id ID --agent-id AID` (`story_step.py:1223`; фазы `skills/qa-story/phases/s3.md:18,24,70,91`) или `controller.py`, `stage_done.py --agent-id`. Если `bind` для этого диспатча не запускали (или связали другой, устаревший id, или хост выдал новый id при возобновлении), охрана знает пять других агентов и отказывает (вывод из кода, прогона нет).

Ограничение вывода: отказ воспроизведён чтением кода, прогона TP2-2702 в руках не было.

## Класс

Отказ без двери (FR-57, FR-2) плюс корень — идентичность диспатча: привязка агента к диспатчу целиком на дисциплине дирижёра. Корень уже заведён: находка `20261027-identichnost-dispatcha-teryaetsya-pri-povtornom-ispolzovanii-sessii-agenta.md` (A2, узел DC1-11, та же пачка): последний `bind` перезаписывает, идентичность диспатча теряется. Родственные: `plans/piles/speed-cost/findings/20261027-resume-hukom-sendmessage-zamer.md` (хук, сам пишущий `resume`; отложен до замера), `plans/piles/codex/findings/20261016-resume-identity-siblings.md`.

## Решения владельца

Владелец, 28.10.2026: «не в 0.10.5, в пачки». Узел DC1-16: (1) текст отказа ветки «известные есть» называет дверь — `story_step.py bind --dispatch-id <диспатч> --agent-id <id>`, когда агент принадлежит этой стори, иначе — дверь «новый диспатч в Agent»; (2) корень — через DC1-11 (автоматическая или проверяемая привязка id). Решение владельца нужно: нет (текст двери и привязка — технические).

Принципы и правила: P15, P22, FR-1, FR-2, FR-57, AR-9, AR-25.
