# `scoreboard_bar._requests` повторяет сбор запросов `compare.scan`: один читатель транскрипта

id: — | кучка: `forge` | от: черновик носителей P1-v N8 (`docs/tasks/specs/20261114-p1v-n8-carriers-draft.md`, «Noticed, not widened»; повтор назван docstring'ом самой функции: «the same collection `compare.scan` makes (it does not expose it)») | приоритет: П3 | кандидат наверх: нет

## Что не так

Класс фабрики: **один сбор по двум копиям (AR-13, FR-54)**. `experiments/measurers/scoreboard_bar.py::_requests` (~57) читает транскрипт и собирает `{id сообщения: (модель, usage, время)}` из assistant-строк с `usage`, пропуская строки не-JSON и пустые маркеры
(`CMP.is_empty_marker`). `experiments/measurers/compare.py::scan` (~142) делает то же сбор (`seen[id] = (model, usage)`) внутри себя и наружу его не отдаёт. Правило сбора живёт в двух местах; поправка одного (например, новый пустой маркер) разойдётся.

## Что именно менять

Выбранное направление: сбор выносится в одну функцию `compare.py`, обе зовут её.

1. `experiments/measurers/compare.py`: функция `requests_of(path) -> dict` (`{id: (model, usage, timestamp)}`), логика взята из `_requests` как более полная (с временем); `scan` строит `seen` через неё (отбрасывая время) — отдельные части `scan` (роль, tools, `first`/`last` по ВСЕМ строкам с `timestamp`) остаются как есть: `first`/`last` берутся не только с assistant-строк, и это расхождение не стирается.
2. `scoreboard_bar.py::_requests` удаляется, вызовы идут в `CMP.requests_of`; исключения `OSError` / `UnicodeDecodeError` проходят как сегодня.
3. Пустое: файл пуст / нет assistant-строк — `{}`; строка без `id` — ключ по `uuid`, как сегодня; строка не JSON — пропуск.
4. Тесты — строки таблицы в `experiments/measurers/test_measurers.py` (быстрый): один и тот же транскрипт даёт одинаковое число запросов у `scan` и у функции; дубль id считается один раз; пустой маркер пропущен; не-JSON-строка пропущена; пустой файл.

Принципы и правила: AR-13, FR-54; P31.

Связи: `findings/20261114-izmeritel-check-all-contracts-schitaet-provenance-bez-result.md` (тот же каталог `experiments/measurers/`).

Решение владельца нужно: нет.
