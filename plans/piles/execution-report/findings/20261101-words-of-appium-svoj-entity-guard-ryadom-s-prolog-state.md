# `AppiumBackend.words_of` держит собственную защиту от `<!entity` рядом с `reporters._prolog_state`, который принимает только путь

id: — | кучка: `execution-report` | от: критик диффа S4 релиза 0.10.8 (`docs/tasks/specs/reviews/t-599-s4-critic.md`, вопрос 6 (c) = F-13), 01.11.2026 | приоритет: П3 | кандидат наверх: нет

Что не так: два места отказываются читать XML с объявлением сущности (защита от «взрыва сущностей»). `reporters._prolog_state(path, scan_limit)` (`reporters.py:92`) читает пролог до корневого элемента, различает `entity` / `noroot` и учитывает регистр и комментарии DOCTYPE (тесты `test_reporters.py:874-888`). `manual_capture.AppiumBackend.words_of(xml_text)` (`manual_capture.py:1919-1923`, прочитано на `1afda33f`) для XML, который уже лежит в памяти (ответ сервера Appium), проверяет грубее: `"<!entity" in lowered or "<!doctype" in lowered` — отказывает на любой DOCTYPE, читает всю строку, не знает про предел сканирования (дубль защиты, AR-13: две разные границы одного правила). Критик: `_prolog_state` принимает путь; небольшое расширение до текста — очередь строкой.

Что именно менять: `ai-packages/qa-factory/scripts/reporters.py`: добавить вход, принимающий текст (`_prolog_state_of_text(text, scan_limit)` — новое имя; `_prolog_state(path)` читает первые байты файла и зовёт его), `manual_capture.AppiumBackend.words_of` зовёт его вместо своего `lowered`-сравнения. Направление ошибки сохраняется: «сущность или нет корня» → пусто (ничего не прочитано), как сейчас; DOCTYPE без сущности больше не отказ, если так сказано в `_prolog_state` (проверить: `test_reporters.py:884` `tricky`). Тесты: `scripts/tests/test_manual_app.py:506` (сущность → пусто) остаётся зелёным; новая строка — DOCTYPE без сущности даёт слова (если решение «не отказ» принято Lead пачки; по рекомендации — да, как у `_prolog_state`), `<!ENTITY` в комментарии DOCTYPE и в другом регистре → пусто; текст длиннее `scan_limit` без корня → пусто.

Свидетель: `docs/tasks/specs/reviews/t-599-s4-critic.md` вопрос 6 (c); `ai-packages/qa-factory/scripts/manual_capture.py:1919-1923`; `ai-packages/qa-factory/scripts/reporters.py:92-136`; `ai-packages/qa-factory/scripts/tests/test_manual_app.py:506`; `ai-packages/qa-factory/scripts/tests/test_reporters.py:874-888`.

Принципы и правила: P12; FR-54; AR-13, AR-15.

Решение владельца нужно: нет.
