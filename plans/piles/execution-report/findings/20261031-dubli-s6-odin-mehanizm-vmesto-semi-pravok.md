# Дубли S6 (учёт веток): семь копий одного знания — сначала вопрос «один механизм или семь правок»

id: — | кучка: `execution-report` | от: критик диффа S6 шаги 2, 3, 1d, 1e релиза 0.10.7 (`docs/tasks/specs/reviews/r0107-s6-steps-1d-1e-diff-critic.md`, F-11 и строка DUPLICATION), 31.10.2026 | приоритет: П2 | кандидат наверх: нет

Что не так / что сделать: критик назвал семь дублей в диффе S6 (`BA` = `scripts/branch_accounting.py`, строки на `029c57e6`), все в очередь, кроме тех, что чинятся вместе с F-1:
1. `report_facts._gate_a_decided` (`report_facts.py:1652`) копирует `story_run.py:4724-4727` (назвал билдер): публичный читатель «решён ли гейт A» должен заменить обе (AR-13). Обновление t-414 (31.10.2026): публичный читатель теперь есть, `gate_brief.gate_a_decided` (его зовут `report_facts._attachments`, `branch_accounting._unseen_attachments` и писатель `gate_brief.keep_shown_attachments`); копия в `report_facts` удалена. Остались две копии в `story_run.py` (вложенная `decided` в `no_move_facts`, около `:4783`, и `approved` в `ticket_reopen_gate_a`, около `:6720`) — вне владения t-414; заменить их вызовом `gate_brief.gate_a_decided` или решить иначе. Копия константы `RUN_MODE_ENV` — в находке `20261031-s6-driver-state-na-puti-skilla-svoj-fajl-i-klyuchi-tolko-drajvera.md`, п. 3.
2. `_labels` (`BA:1617`) против `acceptance._slice_values` (`acceptance.py:556`) и `_pair` против `acceptance.row_slice` (`:570`, «THE one reader»): чинится вместе с F-1 фикс-раундом; проверить на вершине, что копии ушли.
3. `project_config` (`BA:156`) добавляет ещё один читатель JSON проекта (ось 16, есть `hooklib.read_json`). На базе релиза `3840246e` у имени `project_config` уже две функции: `factory_dashboard.py:721` и `gate_brief.py:3024`; с S6 их три.
4. `_walk_records` (`BA:1985`) против `_walk_problems`: второе чтение `candidates_walked`.
5. `_running_stage` (`BA:1711`) против `_running` (`BA:1049` на базе; ещё `conductor_stop._running`, `conductor_stop.py:41`).
6. `validate_artifacts`: третий список блоков внутри раздела (cut-list), назвал билдер.
7. `dup_ratchet`: свидетельство на вершине показывает только строку `tools`; по t-381 `scripts` дал 0 нового; критик не перезапускал. Храповик ловит копии одной формы, эти семь — разные формы одного факта.

Вопрос Lead до узлов (механизм первым, правила 9–10 `CLAUDE.md`): семь правок по месту (каждая копия заменяется своим читателем) или ОДИН механизм над ними (например, перечень «факт — его единственный читатель» с тестом, который краснеет на втором читателе того же факта; форма и дом перечня — не решены здесь). Цена по вариантам: семь правок — семь мелких узлов и ноль защиты от восьмой копии; один механизм — один узел и критик, плюс чей-то долг поддерживать перечень (платит билдер каждого нового читателя), детектор утечки — калибровка. Обход по карте `docs/SIBLING_MAP.md` для этих семи здесь не делался (карта не читалась); находка о копиях чтения голов команды и `evidence_ref_issue` (`findings/20261031-kopii-chteniya-golovy-komandy-evidence-ref-issue-i-konstanty-resume-doors.md`) того же класса, решать вместе.

Свидетель: `docs/tasks/specs/reviews/r0107-s6-steps-1d-1e-diff-critic.md` строки 65, 87-94; `git grep` на `029c57e6` находит `_labels` (`BA:1617`), `_running_stage` (`BA:1711`), `_walk_records` (`BA:1985`), `project_config` (`BA:156`), `report_facts._gate_a_decided` (`:1652`); `git grep` на `3840246e` находит `project_config` в `factory_dashboard.py:721` и `gate_brief.py:3024`. Ветка `029c57e6` в базе не влита.

Принципы и правила: P12; FR-54, FR-47; AR-13, AR-15.

Решение владельца нужно: нет (решает Lead: механизм или правки по месту).
