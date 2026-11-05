# Живость роли под драйвером недоказуема: строка прогресса всегда говорит «not proven alive»

id: B-268 | кучка: `driver-controller` | от: новое, 02.10 — следующий пакетный батч | приоритет: — | кандидат наверх: нет

Что не так / что сделать: **Живость роли под драйвером недоказуема: строка прогресса всегда говорит «not proven alive».** `dispatch_liveness` ищет транскрипт сабагента, а роль `claude -p` его не оставляет — на любой живой роли драйвера строка (t-310) читает «recorded running since HH:MM, not proven alive» (честно, но ложная тревога на каждом прогоне). Сделать: драйвер пишет `in_flight {dispatch_id, pid, started_at}` ДО запуска роли (кусок driver-state из t-294) и `story_progress`/`dispatch_liveness` доказывают живость по pid; `driver_session_end` тоже без доказательства in-flight (аналог билдера). Туда же: литерал «5 кейсов на блок» в `controller.validate_manual_runner_block` без имени — `story_progress` повторяет число; назвать константу и читать её. Четыре читателя «где стори» (`story_progress`, `story_step where`, `next_actions` дашборда, `retro_numbers`) — строка оси 5. [F06]

Свидетель: Билдер t-310 Q3/Q4 + аналоги.

Принципы и правила: FR-41, FR-17, P10

Решение владельца нужно: нет (фраза не найдена)

<!-- piles split: plans/BACKLOG.md, раздел 7 «Релизы, приёмки, инфраструктура разработки»; ячейки строки перенесены дословно -->

Строка BACKLOG.md целиком:

```
| B-268 | **Живость роли под драйвером недоказуема: строка прогресса всегда говорит «not proven alive».** `dispatch_liveness` ищет транскрипт сабагента, а роль `claude -p` его не оставляет — на любой живой роли драйвера строка (t-310) читает «recorded running since HH:MM, not proven alive» (честно, но ложная тревога на каждом прогоне). Сделать: драйвер пишет `in_flight {dispatch_id, pid, started_at}` ДО запуска роли (кусок driver-state из t-294) и `story_progress`/`dispatch_liveness` доказывают живость по pid; `driver_session_end` тоже без доказательства in-flight (аналог билдера). Туда же: литерал «5 кейсов на блок» в `controller.validate_manual_runner_block` без имени — `story_progress` повторяет число; назвать константу и читать её. Четыре читателя «где стори» (`story_progress`, `story_step where`, `next_actions` дашборда, `retro_numbers`) — строка оси 5. [F06] | Билдер t-310 Q3/Q4 + аналоги. | новое, 02.10 — следующий пакетный батч | FR-41, FR-17, P10 |
```
