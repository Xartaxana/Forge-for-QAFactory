# `pipeline.json` показывает S3/S4 `done`, пока их доработка идёт (`later_work_status: running`)

id: — | кучка: `driver-hosts` | от: прогон LOCAL-1, разбор t-1666, 02.11.2026 | приоритет: П2 | кандидат наверх: нет

## Что наблюдалось

Носитель — `mybooks-stand/test-automation-framework/qa-factory/artifacts/LOCAL-1`; разбор t-1666, П-10.

- В `pipeline.json` у S3 и S4: `status: done` вместе с `later_work_status: running`; в `checkpoint.json` `task_id: null`.
- Читатель видит «готово до S4», хотя гейт A ещё не собран; впечатление «S5 в работе» при том, что ключа S5 в `pipeline.json` нет и `git status --short tests` пуст.

## Класс

Состояние стадии читается из двух полей разными читателями, и ни один не называет «доработка идёт» (FR-41: неизвестное/неполное не выдаётся за факт; AR-13: факт с функцией-читателем читается только через неё; AR-22). Не правило MyBooks.

## Что именно менять

Направление выбрано (Lead, 02.11.2026); узел DH1-2.

1. **Один читатель статуса стадии.** Функция в `scripts/controller.py` (запись `later_work_status` — `:785`, `STAGE_RUN_MARKS` — `:845`) выдаёт составной статус: `status: done` + `later_work_status: running` → «доработка идёт»; все показывающие статус места (`scripts/story_step.py` describe, `scripts/factory_dashboard.py`, текст дирижёру) вызывают её. Тест: состояние `done` + `running` → «доработка идёт», `done` без метки → «готово».
2. **Что видит человек.** Сводка прогона не пишет «готово до S4», пока у S3/S4 доработка идёт; строка называет стадию и то, что гейт A не собран. Тест: сводка на `pipeline.json` из фикстуры LOCAL-1 не содержит «готово» для S3/S4.
3. **`checkpoint.json`.** `task_id: null` при идущей доработке — `task_id` берётся из записи доработки или состояние называется «нет активной задачи» явно. Тест: чекпоинт при `running` несёт id задачи.

## Принципы и правила

P1, P3, P22; FR-41; AR-13, AR-22.

## Связи

- Разбор прогона: `docs/tasks/specs/reviews/t-1666-local-1-run-review.md` (П-10).
- Соседи: узлы driver-controller по `later_work_status` (DC1-*), HF5-20 (повторное открытие работы).

Решение владельца нужно: нет.

## Повтор LOCAL-1 (02.11.2026)

Прогон LOCAL-1 (t-1672 П-24): `pipeline.json` — у всех стадий `wall_seconds: null`; у S4 `finished: null` и пустой digest; `later_work_status: running` у S3/S7/S8 после `done`; `closed_at` (10:10:42) раньше `finished` S8 (10:10:53). Тест узла дополняется: проекция pipeline закрывает поля стадии (`wall_seconds`, `finished`) и не оставляет `later_work_status: running` после закрытия.
