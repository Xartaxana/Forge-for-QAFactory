# Тексты `run_suite` (`executor_unavailable`) и `story_budget` (`STORY BUDGET`) без записи в реестре отказов: класс — строками `route:<name>`

id: — | кучка: `live-run-fvf` | от: слово Lead к критику узла P1-b N1, `docs/tasks/specs/reviews/20261113-p1b-n1-code-critic.md` (F1 и Q1 — маршруты без источника класса); строка Lead: «the refusal registry has no record for the texts of run_suite (executor_unavailable) and story_budget (STORY BUDGET); their routes are classed through route:<name> rows in the driver-exits classes data file until a record exists» | приоритет: П3 | кандидат наверх: нет

## Что не так

Класс фабрики: **текст отказа, у которого нет записи в реестре отказов, получает класс в ДРУГОМ месте (данные переписи) — второй носитель одного факта
(FR-19: у причины блокировки есть владелец; AR-1, AR-13)**. Перепись выходов драйвера (`dry_exits.py`) классифицирует маршруты `ask_person`
по `class_source`; у маршрутов `run_suite` (`executor_unavailable`) и `story_budget` (текст `STORY BUDGET`, `controller.py:6217-6219`) записи
реестра нет, поэтому E19 («class unknown» — красное) без строки данных не достигается. Критик называл кандидатов: `executor` берётся из префикса
контракта (`contract.py:117`), `readiness` — возможно `SG-tracker-route` (`refusal_registry.py:254`).

## Что именно менять

Направление выбрано Lead: **пока записи нет — класс этих двух маршрутов задают строки `route:<name>` в файле классов переписи выходов драйвера**; цель — запись реестра.

1. `ai-packages/qa-factory/scripts/tests/fixtures/driver-exits/classes.json` (данные): строки `route:run_suite` (причина `executor_unavailable`) и
   `route:story_budget` (текст `STORY BUDGET`) с классовым словом и источником. Слово класса выбирает Lead (вердикт: для маршрута, где отвечает
   человек, «gate» — естественное прочтение, но решение Lead; P13); исполнимо по этой рекомендации, Lead подтвердит. Требует, чтобы `class_of`
   в `dry_exits.py` принимал такой источник (рекомендация критика F1: `class_source` может называть любой ключ `by_source`) — делается тем же
   узлом после слияния фикс-раунда N1.
2. Тест (`dry_exits --selftest`, таблица): маршрут с строкой → класс известен; строка удалена → красное «class unknown» с именем маршрута и
   дверью (E19); `0 discrepancies` достигается именами источников, а не заметкой.
3. Конец пути — записи реестра: `scripts/refusal_registry.py`, записи для текстов `executor_unavailable` и `STORY BUDGET`; когда запись есть, строки
   `route:<name>` удаляются, тест п. 2 переносится на источник «реестр». Узел поэтому открыт до появления записи; запись реестра — отдельная
   работа владельца реестра (выбор класса и текстов не делается здесь).

Принципы и правила: FR-19, FR-13; AR-1, AR-13, AR-28.

Решение владельца нужно: нет (слово класса — Lead пачки).
