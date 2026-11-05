# Красный CI после F4-2: фикстуры пакетных тестов строят проект без маркера `qa-factory/config.json`

id: — | кучка: `forge` | от: Lead / билдер t-632, 09.10 | приоритет: П2 | кандидат наверх: нет

Что не так / что сделать: после слияния F4-2 (`3897c6ba`, один обход корня `runtime_paths.nearest_project`, который
находит проект только по ФАЙЛУ `qa-factory/config.json`) пайплайн `package-fast` на `main` покраснел (7893964):
`test_scout_reliability.py` (два теста о вето «host worker is still active» получали `ValueError: checkpoint requires
remaining work and reason`) и `test_post_commit_refresh.py` (`recover` ничего не записал). Причина — не код: фикстуры
строили `root/qa-factory/artifacts/TASK-1` без маркера, и контроллер честно не находил проект (вето :2829-2833
пропускалось, `liveness_fixes` :3605 давал `[]`). Починено в фикстурах (t-632 `c7312607`: маркер `{}` в двух тестах
scout_reliability и в `site_recover`). КЛАСС остаётся: 28 тестовых файлов пакета используют `temp_dir()` как корень
стори вместе с `Controller(`, `at_s3_rework` или `initialized(` (та же форма, что `site_recover`) — они зелёные в CI,
значит, пока не доходят до ветки, зависящей от проекта; измеритель билдера (`def` с `artifacts` + `Controller(` без
маркера) слеп к корням, построенным через помощник. Что сделать: один помощник фикстур (`harness.temp_project` или
`initialized(root)` с маркером), перепись 28 файлов отдельным узлом; до этого любая новая ветка контроллера, зависящая
от `_project_root()`, может покраснеть в тесте, который моделирует проект без маркера. Правило: CI на `main` красный —
строка в бэклог; бэклог заморожен (D-0036) — поэтому находка здесь, B-id выдаст интегратор при сборке пачки.

Свидетель: лог джобы 27603844 (`FAIL tests: scripts/tests/test_post_commit_refresh.py … 155/156`, `test_scout_reliability.py
… FAILED (errors=2)`); отчёт `docs/tasks/specs/reports/t-632-builder-report.md` (негативный контроль: маркер убран —
ошибка вернулась, восстановление байтовой копией, sha256 равен).

Принципы и правила: FR-31, FR-32, FR-59; спека `docs/tasks/specs/t-617-f4-2-project-root.md` §8.2 (без проекта —
`unknown`, не закрытие); ось 8 SIBLING_MAP.

Решение владельца нужно: нет.
