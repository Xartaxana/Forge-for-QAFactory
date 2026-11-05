# `sorted(<Path iterable>)` в пакете зависит от платформы (Windows без учёта регистра, Linux по кодам): порядок пунктов отказов и отчётов разный на разных ОС — класс ~25 обходов

id: — | кучка: `conductor` | от: CI 7925427 (package-fast красный после слияния C4-5), билдер t-887 (починка одного сайта `contract.case_glob`), записал Lead 16.10.2026 09:5x | приоритет: П2 | кандидат наверх: нет

## Что

`contract.case_glob` сортировал объекты `Path`; их порядок платформенный (`TC-001.md` vs `a/TC-002.md` стоят по-разному на Windows и
Linux), и совместный отказ `case_index` перечислял пункты в разном порядке — красный `package-fast` на `main`. t-887 починил ОДИН
сайт ключом `as_posix()` (порядок по кодам). Класс (перепись билдера, только по grep): `session_handoff.py:36/:50/:58`
(`can_takeover` — порядок glob наполняет списки jobs/unknown_writes в отказе), `exit_gate.py:533/:559` (порядок списка ошибок), и
не прочитанные сайты в audit_factory, brief_pack, controller, delivery_manifest, environment_preparation, execution_request,
factory_dashboard, gate_preflight, guard_pre_tool, host_*, install_smoke, judge_run, metrics_projection, project_decisions,
readiness, run_suite, session_identity, story_run:6584, story_step, tms_publication, window_budget, worker_lifecycle.
Правило: любой `sorted(<Path>)`, чей порядок доходит до отказа, отчёта или файла, сортирует по `as_posix()` (FR-31: тест, падающий
только на одной среде — дефект; P10 — одна логика везде).

Что сделать: первый ход — перепись `grep -n 'sorted(.*\(glob\|iterdir\|listdir\)' scripts/*.py` с вердиктом на сайт (доходит до
текста/файла — да/нет); один помощник порядка (`hooklib.sorted_paths` или рядом с `case_glob`) и перевод сайтов с «да»; пин на
смешанный регистр; доказательство в docker `python:3.12` для тронутых тестов (память `package-tests-proved-in-docker-before-merge`).

## Куда

Строка C4-7 пачки `conductor/batch-4-vhodyashchie-2.md` (D-0044).
