# R4: дверь доработки S7 для `bug_candidate` без кейса

id: — | кучка: `rules-debt` | от: спека карточек фазы 2 (`docs/tasks/specs/20261117-rules-debt-phase2-cards-spec.md`), 17.11.2026 | приоритет: П1 | кандидат наверх: нет

Что не так / что сделать: Маршрут доработки принимает только `--cases` (`controller.py:9908`, `ANSWER_REWORK_OWNERS` :9391), у кандидата в баги без кейса двери нет. Класс: запрет без двери (FR-57).

Что именно менять: `controller.py` (маршрут доработки; `ANSWER_REWORK_OWNERS`; аргумент `--cases` → типизированный аргумент кандидата для этого маршрута), регенерация `design/controller-blocks.md`, строки `test_controller_*`. Файлы `test_controller_*` — канон пачки.

Карточка: `docs/tasks/specs/20261117-rules-debt-phase2-cards-spec.md`, карточка FL4 — читать там, не копировать сюда.

Свидетель: `controller.py:9391,9908`.

Принципы и правила: FR-57, FR-2; AR-9, AR-25.

Решение владельца нужно: нет.
