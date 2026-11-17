# G15: головы команд чтения — данными, и `_is_reader` режет `.exe` как символы (`catx` читается как `cat`)

id: — | кучка: `rules-debt` | от: спека карточек фазы 2 (`docs/tasks/specs/20261117-rules-debt-phase2-cards-spec.md`), 17.11.2026 | приоритет: П1 | кандидат наверх: нет

Что не так / что сделать: Списки голов чтения — кодом (`host_adapter.py:452 _READ_HEAD`, `stage_guard.py:2509 READER_COMMANDS`). В `stage_guard._is_reader` найдено: `name.rstrip(".exe")` (:2590) снимает СИМВОЛЫ `.`, `e`, `x`, а не суффикс: `catx` → `cat` считается читателем (ошибка в сторону исключения для читателя). Класс: закрытое разнообразие — строка данных (AR-1, FR-13).

Что именно менять: `launch-causes.json`: новые таблицы для двух списков; `host_adapter.py` (`_READ_HEAD`, `_read_refusal`), `stage_guard.py` (`READER_COMMANDS`, `_is_reader`), `tests/role_replay.py` (`_READ_ALTS` выводится из `_READ_HEAD`). Остаются отказанными / не читателями: `python`, `bash`, `pwsh`, `node`; голова с путём (`/usr/bin/rg`); `.exe` и регистры; `catx`, `lsx`; пустая или нечитаемая таблица → пол в коде (сегодняшние списки), не «любая голова»; строка таблицы, добавляющая писателя в головы чтения. Тесты стражи медленные: канон.

Карточка: `docs/tasks/specs/20261117-rules-debt-phase2-cards-spec.md`, карточка S10 — читать там, не копировать сюда.

Свидетель: `host_adapter.py:452,525`; `stage_guard.py:2509-2512,2589-2590`; `tests/role_replay.py:30-36`.

Принципы и правила: FR-13, FR-17; AR-1, AR-29.

Решение владельца нужно: нет.
