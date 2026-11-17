# Дома файла бага: писатель (`qa-bug-reporter`) и читатели читают разные папки

id: — | кучка: `rules-debt` | от: спека карточек фазы 2 (`docs/tasks/specs/20261117-rules-debt-phase2-cards-spec.md`), 17.11.2026 | приоритет: П1 | кандидат наверх: нет

Что не так / что сделать: Репортёр пишет `<корень задачи>/bugs/BUG-n.md`, а `judge_results.run_bugs`, `external_writes` (`bug_file`) и рамка `common-rules.md:116` ищут баг в каталоге состояния проекта. Класс: писатель и его читатели обязаны меняться одним коммитом (AR-22, ось 38 карты — текст оси пишет Lead).

Что именно менять: (1) `bug_records`: одна публичная функция списка файлов багов для проверки дублей — сначала `<корень задачи>/bugs/`, затем `<project>/qa-factory/bugs/`, затем `<корень артефактов>/<T>/bugs/` других стори; строка в таблице `test_bug_records.py`. (2) `judge_results.run_bugs` берёт `existing` оттуда, `_project_bugs_dir` удалён, запись дубля получает `"file"` (относительно каталога состояния). (3) `common-rules.md:116`: `bug_file` — от корня задачи, старый баг в каталоге состояния всё ещё находится; слайсы — `contract_slices.py --write`. (4) `external_writes`: один помощник для `bug_file` в двух местах (корень задачи, затем `state_dir()`); строка в `test_external_writes_bug_refusals.py`, красная до правки. (5) тексты `external-writes.md:44`, `templates/test-report.md:35`, `form_selftest.py:245` — одни и те же слова. (6) докстринг `bug_records.py:10-18`. Края E1-E8 карточки (нечитаемая папка называется, не читается как пустая; потолок режет сначала чужие баги).

Карточка: `docs/tasks/specs/20261117-rules-debt-phase2-cards-spec.md`, карточка C1 — читать там, не копировать сюда.

Свидетель: `docs/tasks/specs/20261117-rules-debt-phase2-cards-spec.md` §0 п. 2 (читатель `external_writes.py:653,893-901`); критик t-942 F8 (`docs/tasks/specs/reviews/t-942-rules-debt-phase1.md`).

Принципы и правила: FR-14, FR-37; AR-13, AR-22.

Решение владельца нужно: нет.
