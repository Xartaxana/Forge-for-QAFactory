# Находки живого прогона LR2-1 — пачка 2: читатели и носители, найденные критиками 13.11.2026

кучка: `live-run-fvf` | статус: ожидает | взял: — | ветка: — | MR: — | стенд: не нужен | приоритет: П2

Правило готовности: пачка закрыта, когда каждый узел «принято», свидетели узлов — в журнале взявшего,
живые доказательства (FR-33) сделаны или переданы строкой в кучку «живые прогоны».

Решения владельца: нет (направление каждого узла выбрано Lead пачки, 13.11.2026, и записано в находке узла).
Скоуп свидетеля: по узлам, при взятии.
Общий бриф дизайнерам: находка узла + вердикт критика, названный в её строке «от» (`docs/tasks/specs/reviews/20261113-*.md`).

Пути «Пишет в»: пакета — от `ai-packages/qa-factory/`; Lead пачки уточняет их при взятии.

Пачка открыта 13.11.2026 (Lead пачки): `batch-1-live-run-fvf.md` — 30 узлов, находки очередей критиков 13.11 ложатся сюда (D-0044).

## Бриф

Что сделать: узлы таблицы ниже; первыми FV2-1 и FV2-2 (читатели полей, которых нет у носителя или которых код не заполняет). Узлы
FV2-1, FV2-2 имеют фиксированные id от Lead (строки реестра P1-a перепривязаны к ним). НЕ делать: правки в замороженном дереве релиза.

## Узлы

Исполнитель «designer → builder → critic» — кодовый узел; «builder» — узел-документ. Статусы:
`ожидает` → `в работе` → `сдано` → `принято` / `отклонено`.

| Узел | Приоритет | Что | Исполнитель | Пишет в | Зависит от | Статус |
|---|---|---|---|---|---|---|
| FV2-1 | П2 | `handoff_check._plan_row_of` читает ключ шапки `plan_row:`, которого нет в контракте кейса (`artifact-contract.md:59-62`); читать носитель контракта через `contract.case_plan_row`; найти, где роли учили писать `plan_row:` (`findings/20261113-chitatel-plan-row-chitaet-klyuch-kotorogo-net-v-kontrakte.md`) | designer → builder → critic | `scripts/handoff_check.py`, `references/form-rounds.json` | — | ожидает |
| FV2-2 | П2 | Метка «заполняет код» по имени листа `requirements` (`BY_LEAF`) покрывает поля S3/S8, которых код не заполняет; метка ключуется полным путём поля (`findings/20261113-by-leaf-requirements-pomechaet-polya-kotorye-kod-ne-zapolnyaet.md`) | designer → builder → critic | `scripts/handoff_check.py`, `references/form-rounds.json` | FV2-1 | ожидает |
| FV2-3 | П2 | Два читателя «раннер выбирает по id узла» расходятся на `py.test`: `is_pytest_command` против `runner_identity.node_id_selection`; единственный ответ — ключ данных (`findings/20261113-py-test-dva-chitatelya-odnogo-voprosa-vybor-po-id-uzla.md`) | designer → builder → critic | `scripts/execution_request.py`, `scripts/run_suite.py`, `references/launch-causes.json` | — | ожидает |
| FV2-4 | П3 | Выходы стадий, которые не отказывает ни один читатель (8) и не покрытые (6): `requirements-readiness.json` без `verdict`, `grounding.yaml` без `rows:` (`findings/20261113-vyhody-stadii-kotorye-ne-otkazyvaet-ni-odin-chitatel.md`; нужна доразведка имён) | designer → builder → critic | `scripts/validate_artifacts.py` | FV2-1, FV2-2 | ожидает |
| FV2-5 | П3 | Проверка реестра красных строк сливает повторный id через И; повторный id — отказ (`findings/20261113-ledger-krasnyh-strok-sklevaet-povtornyj-id-cherez-i.md`) | builder → critic | `scripts/tests/known_red.py`, `scripts/tests/test_field_producers.py` (оценка по ветке `wip/p1a-fix`; уточняется при взятии) | FV2-4 | ожидает |
| FV2-6 | П3 | Частный вызов `runtime_paths._package_fingerprint` из `driver_journal` и двойной гард «строка не создаёт папку стори» в `driver_machine` (`findings/20261113-chastnyj-vyzov-i-dvojnoj-gard-papki-zhurnala-progona.md`) | builder → critic | `scripts/runtime_paths.py`, `scripts/driver_journal.py`, `scripts/driver_machine.py` | — | ожидает |
| FV2-7 | П3 | Текст `s5.md:309-311` называет отказ маркера «не в строке плана кейса», маркер судится по всему плану; указатель очереди `:292-299` расширяется до `:309-311` (`findings/20261113-tekst-s5-md-ob-otkazah-markera-ustarel-posle-fv1-19.md`) | builder → critic | `skills/qa-story/phases/s5.md` | — | ожидает |
| FV2-8 | П3 | `role_load.settings` не проверяет типы `allowances.brief` / `brief_charter_head`: сырой `ValueError` (`findings/20261113-role-load-ne-proveryaet-tipy-allowances-brief.md`) | builder → critic | `scripts/role_load.py` | — | ожидает |
| FV2-9 | П2 | Строки выбора теста для форм jest / vitest / dotnet-test: сейчас навсегда `no_selection_form` (`findings/20261113-formy-vybora-testa-tolko-dlya-pytest-i-playwright.md`; нужна доразведка флагов) | designer → builder → critic | `references/launch-causes.json`, таблица форм запуска | FV2-3 | ожидает |

## Ход

Журнал передачи Lead пачки, новые записи в конец: `<дата время> — <что сделано, диспатчи t-nnn, хэши>`.

- 13.11 — пачка открыта (t-545): девять находок очередей критиков P1-a, P1-v, FV1-4, FV1-18, FV1-19.

## Живые доказательства

| Что | Стенд / проект | Кто | Статус |
|---|---|---|---|

## Остатки
