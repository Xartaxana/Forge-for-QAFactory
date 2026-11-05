# Остатки t-613 (карточка запуска на Codex Desktop): слова свидетельств не показываются, безадресные отказы проекта не читаются, `start` длиннее 60 строк, живой прогон FR-33 не сделан

id: — | кучка: `codex` | от: критик t-001/t-002@dev2 и Lead, 12.10.2026 | приоритет: П2 | кандидат наверх: нет

Что не так / что сделать: после правки t-613 (`scripts/launch_card.py`, `story_step.py start/where`, `controller.next`
→ действие `launch`/`wait_start`) остались: (1) `launch_action` читает список свидетельств только как «да/нет»: битая
квитанция ЛЮБОЙ стори молча выключает `launch` на весь проект, и никто не видит её имени (FR-59); форма
`wait_existing_job` закреплена тестами, поэтому словам нужно своё поле или строка `evidence`; (2) безадресные отказы
уровня проекта (`qa-factory/state/dispatch-denials.jsonl`, `inject_context.note_ticketless_denial`) ни один читатель
`launch` не смотрит; (3) `story_step.start` ~84 строки (был длинным до правки), `dict(launch, liveness=…, evidence=…)`
повторён в `controller.next_action` и `story_step.where` — перенести в `launch_answer`; (4) `story_run.py:747` называет
`QA_FACTORY_RUN_MODE` второй строкой-литералом (теперь одно определение в `launch_card.RUN_MODE_ENV`); (5) FR-33: правка
доказана только тестами, живой прогон роли на Desktop с новым пакетом не сделан — первый прогон S2 TP2-2406 и
есть доказательство; (6) `stage_done.py --status running` тратит ~57 с на обновление дашборда/метрик на пути запуска
роли (замер 12.10 на копии стори) — P11, отдельная правка, не в t-613. После повторного критика (R1–R6): (7) R1 —
`launch_card._unbound_evidence` переиспользует правило времени `dispatch_liveness._may_be_this_dispatch`, обнуляя
`status` строки (функция по докстрингу только для незавершённых квитанций); вынести предикат времени в один помощник
для обоих вызовов — трогает `dispatch_liveness.py`, вне t-613; тесты N03/N04b держат опасное направление; (8) R3 —
`_settle_probe_debt` по-прежнему возвращает extras, которые `start` отбрасывает (файл долга читается дважды): вернуть
только notes и обновить пин `test_story_step.py:488`; (9) R4 — из «Dispatch protocol» SKILL.md ушёл указатель на
`handoffs/README.md` (остался только в `references/handoffs.md`); (10) R5 — строка реестра с отсутствующим файлом
контракта: `handoff_init` падает, формы нет, `where` отвечает `wait_start` для умершего `start`; дверь — `release`;
(11) R6 — `dict(launch, liveness=…, evidence=…)` в `controller.py` и `story_step.py` — перенести в `launch_answer`;
(12) R2 — строки отказов, которые `_denial_times` не может отнести (битая строка, без `at`, неизвестный старт), не
запрещают `launch` — решение Lead 12.10 записано в спеке t-613 (направление: лишний отказанный вызов, не дубль роли).

Свидетель: `docs/tasks/specs/reviews/t-613-launch-card.md` (F5, класс, качество, ось 4); замер `stage_done` — находка
`20261012-desktop-launch-card-lost-after-exec-yield.md`.

Принципы и правила: P11, FR-33, FR-41, FR-59.

Решение владельца нужно: нет.
перенесено из ветки dev2/codex-overhead-fixes (plans/piles/driver-controller/findings/20261012-launch-card-leftovers.md), узел: CX1-13
