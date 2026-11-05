# `story_run_common.driver_for` строит Driver, который делает `os.chdir(project)`, а cleanup теста удаляет проект с процессом внутри — на Linux следующий тест падает в `os.getcwd()`; класс всех `test_story_run_*.py`

id: — | кучка: `conductor` | от: CI 7925296 (package-fast красный после слияния C2-6), билдер t-885 (починка одного теста), записал Lead 16.10.2026 09:3x | приоритет: П2 | кандидат наверх: нет

## Что

`story_run.Driver.__init__` (`story_run.py:729/734`) делает `os.chdir(project)`; тесты строят Driver через
`story_run_common.driver_for` во временном проекте и в `finally` удаляют его. Windows не даёт удалить текущую папку —
тесты зелёные; Linux удаляет, и следующий тест в том же процессе падает на `os.getcwd()` (`FileNotFoundError`). t-885
починил ОДИН тест (`test_person_words.py` c26: `cwd0` и `os.chdir(cwd0)` в `finally`); каждый `test_story_run_*.py`, строящий
Driver через `driver_for`, несёт тот же класс — сегодня зелёные по порядку тестов, не по правилу (FR-31: тест, падающий от
порядка/среды — дефект теста).

Что сделать (класс, не экземпляр — правило 9): `driver_for` регистрирует восстановление cwd (контекст-менеджер или `atexit`-
подобный finally в фикстуре) — одно место; тест-страж в `tests/harness.py`: после каждого теста cwd существует; прогон
набора `test_story_run_*.py` в docker `python:3.12` как доказательство (память `slow-tests-proved-on-ci-image`); пин на
негативный контроль (Driver без восстановления → страж падает).

## Куда

Строка C4-6 пачки `conductor/batch-4-vhodyashchie-2.md` (D-0044).
