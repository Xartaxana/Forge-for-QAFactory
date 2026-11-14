# Исключение сетевого запроса названо двумя написаниями одного факта: `stand_health.py` и `env_probe.py` («NO ANSWER (<класс>)»)

id: — | кучка: `live-run-fvf` | от: отчёт билдера FV1-15 (`docs/tasks/specs/reports/20261114-fv1-15-report.md`, раздел «Siblings»; то же замечание билдера FV1-17a про `env_probe.py`) | приоритет: П3 | кандидат наверх: нет

## Что не так

Класс фабрики: **один факт записан двумя текстовыми дорогами (P31, AR-13)**. Запрос к стенду не получил ответа (исключение сети), и два места пишут это своими словами:
`ai-packages/qa-factory/scripts/stand_health.py` (~805): `"note": f"NO ANSWER ({type(exc).__name__})"`; `ai-packages/qa-factory/scripts/env_probe.py` (~651):
`"note": f"{shown} -> NO ANSWER ({type(exc).__name__})"`. Рядом в `env_probe.py` уже есть `no_answer_cause(exc)` — одна функция причины; формулировка заметки одной функции нет.

## Что именно менять

Выбранное направление: одна функция формулировки, оба места её зовут; тексты, которые уже читает человек или тест, не меняются без явного решения в спеке.

1. `ai-packages/qa-factory/scripts/env_probe.py`: функция `no_answer_note(exc, shown="") -> str` рядом с `no_answer_cause`: `"NO ANSWER (<класс>)"`, с префиксом `"<shown> -> "`, когда `shown` непуст.
2. `stand_health.py` (~805) и `env_probe.py` (~651) зовут её; `stand_health` берёт `env_probe` внутри функции, как делает сегодня в соседних местах. Какое из двух написаний выживает как каноническое, выбирает дизайнер
   после перечня читателей (grep по `NO ANSWER` в `scripts/`, включая `tests/` и `references/`, контроль того же вида: одна из двух строк находится) — чтобы не сломать читатель текста.
3. Тест — строка таблицы `ai-packages/qa-factory/scripts/tests/test_http_client.py` (keep, быстрый): оба места дают текст функции для `OSError`, `TimeoutError`, `ValueError` (имя класса печатается как есть),
   с `shown` и без.

Принципы и правила: P31, AR-13, FR-54.

Решение владельца нужно: нет.
