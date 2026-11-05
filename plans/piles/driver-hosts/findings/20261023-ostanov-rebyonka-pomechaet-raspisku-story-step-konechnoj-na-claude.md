# Выпущенная остановка ребёнка помечает расписку `story_step` конечной на Claude, хотя правило говорит «только `story_step finish`»

id: — | кучка: `driver-hosts` | от: Lead пачки hotfix-12586/1 (dev2), 23.10.2026 | приоритет: П2 | кандидат наверх: нет

Что не так: `host_dispatch.record` на событии `SubagentStop` (`scripts/host_dispatch.py:171`), после того как выходной хук выпустил остановку
(`_exit_gate_released`), перебирает `agent_id` и `session_id` и ставит расписке `status = terminal`, `terminal_source = SubagentStop`, если
идентичность совпала с `agent_id` или `task_path` расписки (`host_dispatch.py:176-186`). Правило узла — расписка диспатча `story_step`
(путь привязан к `agent_id` с ведущим `/`) НЕ метится остановкой ребёнка, это делает только `story_step finish`
(докстринг `host_dispatch.py:111-112`; отчёт t-060 называет это исключением оси 20, а сама ось 20 в `docs/SIBLING_MAP.md` называет скан остановки
`host_dispatch.py:183` единственным исключением из правила «один читатель имён»). На Codex расписка привязана
по пути и правило держится; на Claude `agent_id` события остановки равен `agent_id` расписки, значит условие совпадает и расписка
`story_step` метится конечной.

Последствие (из отчёта t-060): ПРЕЖДЕВРЕМЕННАЯ выпущенная остановка (строка `completed` 17:52:58 из инцидента 12586, за четыре минуты до
возврата `SubagentHandback`) может пометить расписку критика конечной; после этого `dispatch_liveness._state` отвечает `returned` по
основанию «расписка диспатча конечна», как только транскрипт молчит `abandoned_after_s`, — без всякого возврата роли. Узел HF1-7 читателем
этого не использует (ключ K-L8 гоняет оба состояния расписки), так что код пачки не опирается на побочную запись; но сама запись остаётся.
Почему она не сработала в инциденте (там расписка критика осталась нетерминальной до `story_step finish`, см. уточнение Lead 22.10 в
`findings/20261022-zavershivshijsya-kritik-schitaetsya-zhivym.md`), не установлено; расписка в `testproject1-sdk-14857-clean` показывает `terminal_source: "SubagentStop"`.

Что сделать: `record` пропускает пометку для расписок, связанных `bound_by == story_step`, на любом хосте (кандидат отчёта); тест: остановка
ребёнка с `agent_id` расписки `story_step` расписку не меняет, `story_step finish` меняет; для расписок других владельцев (`bound_by`
не `story_step`) поведение прежнее. Прежде — одно измерение: на реальной расписке Claude, какие записи делает остановка ребёнка до и
после возврата (PROJECT.md, п. «Спека, меняющая смысл», (а)).

Свидетель: `docs/tasks/handoffs/t-060-hf1-7.md`, раздел «F9 — for a finding (not touched)»: «`host_dispatch.record` ... marks a
`story_step` receipt terminal on a released Claude stop, because on Claude the stop event's `agent_id` equals the receipt's `agent_id`;
axis 20's stated exception ("a child's stop must never mark a `story_step` receipt terminal") holds only on Codex, where the receipt is
path-keyed ... Candidate fix (not mine): skip the terminal mark for `bound_by == story_step` in `record` on every host, with the node in
an untaken batch». Строки `host_dispatch.py` — по дереву пачки, проверены 23.10.2026.

Принципы и правила: P22, FR-41, FR-59, AR-5, AR-25.

Решение владельца нужно: нет.
