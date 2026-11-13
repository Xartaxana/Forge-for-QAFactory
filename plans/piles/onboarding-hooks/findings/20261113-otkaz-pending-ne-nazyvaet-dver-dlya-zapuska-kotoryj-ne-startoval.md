# Отказ «pending» не называет двери для запуска, который так и не стартовал

id: — | кучка: `onboarding-hooks` | от: спека t-263 (§N, N-2), 13.11.2026 | приоритет: П3 | кандидат наверх: нет

## Что наблюдалось

`native_context.py:165`: `raise StateConflict('A factory launch is awaiting SubagentStart; retry after it starts, do not replace it')`. Если запуск
не стартует (сорванный spawn), пакет остаётся pending, и «retry after it starts» ждёт события, которого не будет: двери нет (FR-57, FR-2).
Текст неоднозначности в `deliver` уже называет дверь: `native_context.py:202` — «…relaunch the role under a unique task name.»

## Что именно менять

Направление выбрано: добавить ту же дверь в текст отказа pending.
1. `native_context.py:165`: хвост «; if the launch never starts, relaunch the role under a unique task name» (слова как в :202). Начало
   текста («A factory launch is awaiting SubagentStart») не меняется: оно ключ A24 строки `NC-launch-pending` (спека t-263 §B).
2. Тест: строка таблицы отказов в `test_doctor_context.py` для pending проверяет «unique task name» и сохранённый префикс.

## Принципы и правила

P15; FR-1, FR-2, FR-57; AR-9. Связи: t-263 (N-2, строка NC-launch-pending), OH6-4 (текст отказа в его non-goals — править после слияния).

Решение владельца нужно: нет.
