# Отказы «checkpoint active work» читают `running` без живости: мёртвая сессия держит правку плана, возврат, откат

id: — | кучка: `thinking-roles` | от: ревью критика `docs/tasks/specs/reviews/t-2055-critic-manual-walk.md` (раздел «Judged edges», строка очереди 2); разбор скаута `docs/tasks/specs/reports/t-2036-tr1-9-triage.md` (b), (c) | приоритет: П2 | кандидат наверх: нет

Решение владельца нужно: нет.

## Что наблюдалось

- Узел TR1-9 (`5f573e4ae`) научил закрытие кодом (`code_close_facts`) не считать работающим диспатч, чья сессия мертва, и называть держащий диспатч. Критик отметил: класс шире, остальные места читают статус `running` так же, без живости; ошибка в безопасную сторону (отказ), поэтому не блокировало слияние.
- На этой основе (`scripts/controller.py`) отказ без проверки живости остаётся в: «checkpoint active work before revising scope» (5008, правка плана), «… before reopening Gate A» (5051), «… before invalidation» (5622, `invalidate`); критик назвал также `revise_plan`, `semantic_reopen`, `dispatch`, `invalidate`, возобновление и `s6_close_dispatch` (`scripts/execution_request.py`). Читатель живости уже есть: `Controller._liveness` (2206) и `_running_verdict` (2350); `dispatch_liveness.state` отдаёт `returned|abandoned|never_started|alive|unknown`.
- Следствие: после гибели сессии роли человек получает отказ «checkpoint active work» и не знает, какой диспатч держит и что с ним делать (FR-1, FR-2, FR-40).

## Что именно менять

### TR4-7. Один помощник «что держит и жив ли», дверь в каждом тексте

- Где: `scripts/controller.py` — места 5008, 5051, 5622 и операции `dispatch`, `resume`, `semantic_reopen`, `revise_plan` (найти по `checkpoint active work`); `scripts/execution_request.py` (`s6_close_dispatch`).
- Поведение: диспатч с вердиктом «мёртв» (`returned`, `abandoned`, `never_started`) не считается активной работой; неясный (`unknown`) и живой — остаются отказом, и текст называет диспатч по id и дверь (дождаться или `release`). Нечитаемый вердикт держит отказ (FR-59). Читатель один — `_running_verdict` или его обёртка, который уже использует TR1-9.
- Тест: на каждый отказ — мёртвый диспатч не мешает (находка в журнал), живой — отказ называет его и дверь; контроль: старые тексты отказа в `scripts/tests/test_controller_state.py` не ломаются без причины (текст отказа закреплён намеренно; менять вместе).
- Свидетель: файлы тестов контроллера — медленные, их судит CI.

Принципы и правила: FR-1, FR-2, FR-40, FR-59, AR-13, AR-25.
