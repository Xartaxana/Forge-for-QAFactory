# «batch-7 analogs»: другие модули хоста с `json.loads` пакета роли вне `SCANNED` реестра A24 и устаревший абзац SCOPE в `refusal_registry.py`

id: — | кучка: `onboarding-hooks` | от: критик диффа пачки 7 t-287 (Q1, Q5, Q6), очередь аналогов из снимка координатора 13.11.2026 | приоритет: П3 | кандидат наверх: нет

## Что наблюдалось

Класс (AR-18, AR-22, ось 32 карты «перепись ↔ сканер `sites()`»): одна форма отказа — один сканер и одна запись. По дифам пачки 7 (t-287) остались два аналога:

1. Другие модули хоста вне списка `SCANNED` (`refusal_registry.py:56`; в дереве на момент находки — `stage_guard.py`, `inject_context.py`, `guard_pre_tool.py`, `native_context.py`; OH7-2 добавляет `codex_roles.py`, `host_adapter.py`), которые читают пакет роли через `json.loads` и роняют голый `JSONDecodeError`/`AttributeError` без имени файла и двери (как `native_context.stage`, t-287 F34-3: «INJECT: Expecting value: line 1 column 1 (char 0)»). Список таких модулей не составлен — вопрос скауту.
2. Абзац `SCOPE, and its limits` в докстринге `refusal_registry.py` (около :33) перечисляет проверяемые скрипты («`stage_guard.py`, `inject_context.py`, `guard_pre_tool.py`, and `native_context.py`») и устареет, когда `SCANNED` расширится (OH7-2): текст читателя отстаёт от производителя (AR-22).

Источник: в тексте t-287 Q5/Q6 этих двух пунктов буквально нет; они взяты из строки очереди аналогов снимка `docs/tasks/compact-snapshots/2026-11-13-0628-narrative.md` (стр. 38: «Batch-7 analog queue: LaunchIdRowRefused, the refusal_registry SCOPE docstring, and other host modules outside SCANNED (scout)»), `LaunchIdRowRefused` ведёт фикс-раунд OH7-2 (t-287 F2-2) и здесь не повторяется.

## Что именно менять

Направление выбрано (13.11.2026, «по рекомендации, до слова владельца»):
1. Скаут по конкретному вопросу: «какие `scripts/*.py` вне `SCANNED` читают пакет роли или pending/launch-файл через `json.loads` и что роль видит при пустом или сломанном файле». Ответ — перечень с путями строк и ходом отказа каждого; пустой перечень допустим, но с положительным контролем (тот же поиск находит `native_context.py`).
2. Абзац `SCOPE` в `refusal_registry.py` перечисляет скрипты не списком имён, а ссылкой на `SCANNED` (или строится из него), чтобы расширение списка не оставляло устаревшего текста; тем же коммитом, что расширяет `SCANNED`, либо после OH7-2.

Исход отказов, ключи A24 и строки переписи судейства не меняются.

## Тест

Для п. 2: тест сверки — каждое имя из `SCANNED` встречается в докстринге или докстринг ссылается на `SCANNED`; мутация: добавить имя в `SCANNED` без правки текста — красит. Для п. 1: после скаута — таблица по найденным местам (файл с пустым и ломаным JSON → названная `ValueError` с файлом и дверью).

## Принципы и правила

AR-18, AR-22, AR-29; FR-1, FR-14; ось 32 карты. Связи: `docs/tasks/specs/reviews/t-287-batch7-diff-review.md` (Q1, Q5, Q6, F34-3, F2-2); OH7-2, OH7-3; `findings/20261113-otkazy-check-override-i-rewritten-input-bez-stroki-a24.md`.

Решение владельца нужно: нет.
