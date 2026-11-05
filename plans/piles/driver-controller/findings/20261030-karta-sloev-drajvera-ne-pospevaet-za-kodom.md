# Карта слоёв драйвера (`driver-layers.json`) отстаёт от кода: нет строк для четырёх методов, ключа состояния и читателя исходника — `test_driver_layers` красный на базе релиза

id: — | кучка: `driver-controller` | от: критик диффа HF8-18 релиза 0.10.7 (`docs/tasks/specs/reviews/r0107-hf8-18-diff-critic.md`, L8) и замер на базе `268e7608`, 30.10.2026 | приоритет: П2 | кандидат наверх: нет

Что не так / что сделать: на базе `268e7608` `python -B ai-packages/qa-factory/scripts/tests/test_driver_layers.py` даёт `49/52`: L1 — нет строк карты для `Driver.refresh_after_reporter`, `Driver.s7_listed_rows`, `Driver.s7_rejudge_round`, `Driver.s7_rejudge_rows` (S5b N1b); L4 — ключ состояния `s7_rejudge` без строки в `state_keys`; L8 — `test_stage_guard.py:1428` (модульный `OH3_22_TEXT`) читает исходник драйвера (два вхождения литерала `story_run.py`), а карта объявляет 0 читателей (`source_readers` / `source_mentions`). Критик HF8-18 назвал L8 красным «не от диффа», требующим строки очереди у Lead; в этот раз красных три, и каждый новый узел драйвера добавляет четвёртый. Класс: узел, добавляющий метод, ключ состояния или тест-читатель исходника драйвера, не трогает карту — её ловит только полный тест. Что сделать: добавить строки (дом выбирать по правилам R1–R7 t-301); решить, читатель ли `test_stage_guard.py:1428` (`source_mentions` — текст команды, не имя); узлы драйвера в DoD гоняют `test_driver_layers.py` (один файл, быстрый) вместе со своим свидетелем.

Свидетель: `python -B ai-packages/qa-factory/scripts/tests/test_driver_layers.py` на `268e7608`: `FAIL L1 (4 problem(s))`, `FAIL L4 (1)`, `FAIL L8 (1)`, `=== test_driver_layers: 49/52 ok ===`; `r0107-hf8-18-diff-critic.md:75`.

Принципы и правила: FR-17, FR-54, FR-28; AR-13, AR-19.

Решение владельца нужно: нет.
