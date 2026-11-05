# Читатели «приёмка активна»: статус расписки без записи хоста о завершении, и нет оси в карте

id: — | кучка: `codex` | от: Dev2 (прогон TP2-2406 S4, Codex Desktop), 14.10.2026 | приоритет: П2 | кандидат наверх: да (ось SIBLING_MAP)

Что не так / что сделать: S4 прогона 2406 встал намертво: расписка story_step (`status: running`) не закрывается
`finish` (хэндофф неполон, байты кейсов не запинены), а `worker_lifecycle.active_binding` и `dispatch_liveness._state`
читали только статус расписки — роллаут ребёнка Codex (`task_complete` последней строкой) для них невидим
(`hooklib.story_subagent_transcripts` знает только `subagents/agent-*.jsonl` Claude). Контроллер отказывал в
авторизованном чекпоинте («host worker is still active or cancellation unacknowledged»). Починено в t-009/t-010/t-011:
`dispatch_liveness.native_rollouts`/`native_stop` читают собственную запись хоста о завершении для точного пути
расписки; `_state` и `active_binding` отвечают «вернулся», расписка не пишется, работа не принимается.
Остаток по вердикту критика (`docs/tasks/specs/reviews/t-009-liveness-review.md`, Q5):

- (а) **Ось SIBLING_MAP** «читатели активности расписки»: `dispatch_liveness._state` (ветка waiting),
  `worker_lifecycle.active_binding`, `worker_lifecycle.binding_is_active` (гард спавна; исключение отменено по
  решению Lead — гард читает только terminal/факты контроллера), ветка stop в `worker_lifecycle.guard` (:182),
  `launch_card.py:78`, `story_step.py:763`. Класс: «читатель судит по статусу расписки, которую пишет один
  писатель, и не видит записи хоста». Решение Lead владельца: вносить ось — да/нет.
- (б) Ветка stop гарда (`worker_lifecycle.guard:182`): завершённый простаивающий ребёнок всё ещё требует
  `request_cancel` перед закрытием.
- (в) `hooklib.story_subagent_transcripts` не инвентаризирует роллауты Codex — `transcripts()` в liveness пуст на
  этом хосте; сведение с `native_rollouts`.
- (г) Расписка времени спавна (писатель `host_dispatch.record`), чей выходной гейт отказал, может встать так же:
  `native_stop` принимает только `bound_by: story_step`.
- (д) Четыре читателя `session_meta` (`codex_usage.metadata`, `host_dispatch.child_identity`, `host_probe`,
  `dispatch_liveness.native_rollouts`): свести к одному, расширив `codex_usage.metadata` временем строки.
- (е) Не проверено живьём: пишет ли Codex `task_complete` до блокирующего SubagentStop, который продолжает ход
  (окно в секунды); доказательство — следующий S4-стоп (FR-33).
- (ж) На диске прогона 2406: `TP2-2534` открыта с зависшим `S8: running` — данные проекта (см. находку
  20261013-binding-readers-writers.md (д)).

Свидетель: `qa-factory/state/host-dispatches/<sha256('/root/qa_case_designer__tp2_2406_3')>.json`
(`status: running`, `bound_by: story_step`, без terminal_source); `state/cost/01a135d4-….json` → роллаут
`rollout-2026-10-13T17-14-33-01a135d4-….jsonl`, последняя строка `event_msg task_complete` 15:30:33Z;
`controller.py:2869-2874` отказ чекпоинта; репродукции на копии — `docs/tasks/handoffs/t-009-liveness-report.md`,
`t-010-active-binding-report.md`.

Принципы и правила: P1, P10, P12, FR-17, FR-40, FR-41, FR-54, FR-59.

Решение владельца нужно: да — пункт (а), новая ось карты симметрий.
перенесено из ветки dev2/codex-overhead-fixes (plans/piles/driver-controller/findings/20261014-receipt-active-readers.md), узел: CX1-3
