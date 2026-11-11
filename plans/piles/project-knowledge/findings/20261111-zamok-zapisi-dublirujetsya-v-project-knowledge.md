# Замок записи реестра знаний — копия замка решений проекта

id: — | кучка: `project-knowledge` | от: критик t-2349 на PK0-1 (Q3) | приоритет: П3 | кандидат наверх: нет

Решение владельца нужно: нет.

## Что наблюдалось

Класс фабрики: «общая проблема решается в одном месте и подключается везде» (AR-15). `project_knowledge.lock` — копия `project_decisions.lock`
на 12 строк: байтовый замок `event_store.take_file_lock`, перевод `LockBusy` и `LockBroken` в `TimeoutError`. Различие — файл замка и
слова назначения. Следующий писатель записей получит третью копию.

## Что именно менять

В `ai-packages/qa-factory/scripts/event_store.py` — помощник контекстного менеджера, который принимает путь замка, таймаут и слова
назначения и сам делает перевод в `TimeoutError`; `project_decisions.lock` и `project_knowledge.lock` становятся его тонкими вызовами.
Тесты: `test_lock_busy_refused`, `test_account_lock_that_cannot_be_made_has_its_own_sentence` (`test_project_knowledge.py`) и замковые
тесты `test_project_decisions.py` проходят без изменения ожиданий.

Принципы и правила: AR-15, AR-9, P12.
