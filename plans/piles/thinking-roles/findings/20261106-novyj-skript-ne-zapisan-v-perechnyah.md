# Новый скрипт пакета не записан во все перечни, которые его считают (`driver_timing`)

id: — | кучка: `thinking-roles` | от: ревью критика `docs/tasks/specs/reviews/t-2060-critic-parallel-1.md` (F4 и строка «For the Lead, outside any owns») | приоритет: П2 | кандидат наверх: да (ось: новый скрипт — все перечни)

Решение владельца нужно: нет.

## Что наблюдалось

- Узел TR3-2 добавил `scripts/driver_timing.py`. Критик измерил: перепись `--task-root` красная (`declared-not-expected: ['driver_timing']`; `scripts/tests/test_task_root_parsers.py:157-160` — равенство «новый — красный»); лечение записано как фикс F4: `driver_timing` в `B_SCRIPTS` с рядом батареи `"driver_timing": lambda f, r: [f, r]` (по образцу ряда `walk_timing`) и строка `CLI_SCRIPTS` в `scripts/audit_factory.py` рядом с `walk_timing`.
- Вне этого: `plans/features.json` не содержит `driver_timing.py` — предупреждение коммита; в карту фич скрипт попадает отдельным шагом. На этой основе (`guard/t-2065`) `driver_timing.py` ещё нет (ветка `tr/tr3-2` не слита), поэтому верно ли всё уже сделано фиксом — проверяется после слияния.
- Класс: скрипт, добавленный пакету, должен попасть во все перечни, которые его считают: перепись CLI (`B_SCRIPTS`, `CLI_SCRIPTS`), карту фич (`plans/features.json`), и, если у скрипта есть тест, — перечни тестов. Каждый перечень ловит пропуск красным только если его пишет кто-то заранее; общего списка, откуда они выводились бы, нет.

## Что именно менять

### TR4-6. После слияния TR3-2: все перечни знают `driver_timing`

- Где: `scripts/audit_factory.py` (`CLI_SCRIPTS`), `scripts/tests/test_task_root_parsers.py` (`B_SCRIPTS`, ряд батареи), `plans/features.json` (запись `driver_timing.py` к фиче пачки).
- Поведение: все три места названы в одном коммите узла, а не по предупреждению. Если фикс F4 уже слит — узел сводится к строке `plans/features.json`.
- Тест: `scripts/tests/test_task_root_parsers.py` (быстрый); проверка карты фич — `python tools/piles.py check --all` и предупреждение коммита о `features.json` исчезает.
- Направление класса (не решается здесь): одно место, из которого перечни скриптов выводятся, — вопрос Lead после перечня по оси «новый скрипт».

Принципы и правила: AR-15, AR-22, FR-17, FR-54.
