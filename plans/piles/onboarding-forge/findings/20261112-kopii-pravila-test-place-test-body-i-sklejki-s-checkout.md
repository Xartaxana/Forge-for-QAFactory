# B-355, узел D: правило «записанная область → `test_place`, иначе `test_body`» скопировано в трёх файлах, а склейка «дифф → checkout» — в двух

id: — | кучка: `onboarding-forge` | от: аналоги узла D B-355 (ветка `wip/b355-d`, t-188, коммит 8866d93; спека `docs/tasks/specs/t-155-b355-project-word-for-test-paths.md`), слова Lead 12.11.2026 | приоритет: П3 | кандидат наверх: нет

Изменения узла D живут на ветке `wip/b355-d` и в main ещё не влиты; строки ниже — по ветке.

## Что наблюдалось

1. Правило «если проект записал область файла — `is_test_for("test_place", …)` (папка называет каждый файл), иначе `"test_body"`» повторено: `scripts/arch_check.py` (блок около :115-:129, `test_body = TF.is_test_for("test_place" if recorded else "test_body", …)`),
   `scripts/repo_map.py` `_is_test_file` (:242-248, тот же выбор) и `scripts/project_inventory.py` `_test_area` (:526-541: `test_place` и затем `is_code_file`, затем `names_a_test`). Потребитель-выжившего в `scripts/test_files.py` нет: каждый файл решает «recorded?» сам (AR-13, AR-15).
2. Склейка «дифф → checkout» (`HC.implementation_checkout` / `HC.diff_checkout`) повторена: `scripts/base_slice.py` `_collect_diff` (:416, `HC.diff_checkout`) и `_repo_state` (:201, `HC.implementation_checkout`) и `scripts/blast_radius.py` `_classify` (:176, :185 `HC.implementation_checkout`) — каждый делает свою склейку на каждый дифф; узел B (bb7756b) вынес вычисление «дифф → запись манифеста → коммит» в одного выжившего, а checkout — нет.

## Что именно менять

1. `scripts/test_files.py`: новый потребитель-выживший (например `is_test_in_area(rel, cfg, *, base, root, recorded)`; имя назовёт спека) — выбирает `test_place` или `test_body` по записи области; `arch_check.py`, `repo_map._is_test_file`, `project_inventory._test_area` вызывают его; три копии выбора удаляются тем же коммитом.
2. `scripts/blast_radius.py` `_classify` и `scripts/base_slice.py` `_collect_diff`/`_repo_state` получают checkout дифа через одну функцию (в `hooklib`/`HC`, где живёт `implementation_checkout`); решение «где» — в спеке узла.
3. Тест: таблица случаев в `scripts/tests/test_test_files.py` — запись области есть / нет × файл-тело / место; и строка «все четыре читателя дают один и тот же ответ на одном входе» (строка сценария). Поведение не меняется — свидетель: существующие тесты узла D без правки ключей.

Принципы и правила: FR-47, FR-54; AR-13, AR-15, AR-19.

Решение владельца нужно: нет.
