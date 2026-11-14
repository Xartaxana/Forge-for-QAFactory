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
| FV2-2 | П2 | Метка «заполняет код» по имени листа `requirements` (`BY_LEAF`) покрывает поля S3/S8, которых код не заполняет; метка ключуется полным путём поля (`findings/20261113-by-leaf-requirements-pomechaet-polya-kotorye-kod-ne-zapolnyaet.md`) | designer → builder → critic | `scripts/handoff_check.py`, `references/form-rounds.json` | FV2-1 | принято: 4f37213 (t-661) |
| FV2-3 | П2 | Два читателя «раннер выбирает по id узла» расходятся на `py.test`: `is_pytest_command` против `runner_identity.node_id_selection`; единственный ответ — ключ данных (`findings/20261113-py-test-dva-chitatelya-odnogo-voprosa-vybor-po-id-uzla.md`) | designer → builder → critic | `scripts/execution_request.py`, `scripts/run_suite.py`, `references/launch-causes.json` | — | ожидает |
| FV2-4 | П3 | Выходы стадий, которые не отказывает ни один читатель (8) и не покрытые (6): `requirements-readiness.json` без `verdict`, `grounding.yaml` без `rows:` (`findings/20261113-vyhody-stadii-kotorye-ne-otkazyvaet-ni-odin-chitatel.md`; нужна доразведка имён) | designer → builder → critic | `scripts/validate_artifacts.py` | FV2-1, FV2-2 | ожидает |
| FV2-5 | П3 | Проверка реестра красных строк сливает повторный id через И; повторный id — отказ (`findings/20261113-ledger-krasnyh-strok-sklevaet-povtornyj-id-cherez-i.md`) | builder → critic | `scripts/tests/known_red.py`, `scripts/tests/test_field_producers.py` (оценка по ветке `wip/p1a-fix`; уточняется при взятии) | FV2-4 | ожидает |
| FV2-6 | П3 | Частный вызов `runtime_paths._package_fingerprint` из `driver_journal` и двойной гард «строка не создаёт папку стори» в `driver_machine` (`findings/20261113-chastnyj-vyzov-i-dvojnoj-gard-papki-zhurnala-progona.md`) | builder → critic | `scripts/runtime_paths.py`, `scripts/driver_journal.py`, `scripts/driver_machine.py` | — | ожидает |
| FV2-7 | П3 | Текст `s5.md:309-311` называет отказ маркера «не в строке плана кейса», маркер судится по всему плану; указатель очереди `:292-299` расширяется до `:309-311` (`findings/20261113-tekst-s5-md-ob-otkazah-markera-ustarel-posle-fv1-19.md`) | builder → critic | `skills/qa-story/phases/s5.md` | — | ожидает |
| FV2-8 | П3 | `role_load.settings` не проверяет типы `allowances.brief` / `brief_charter_head`: сырой `ValueError` (`findings/20261113-role-load-ne-proveryaet-tipy-allowances-brief.md`) | builder → critic | `scripts/role_load.py` | — | ожидает |
| FV2-9 | П2 | Строки выбора теста для форм jest / vitest / dotnet-test: сейчас навсегда `no_selection_form` (`findings/20261113-formy-vybora-testa-tolko-dlya-pytest-i-playwright.md`; нужна доразведка флагов) | designer → builder → critic | `references/launch-causes.json`, таблица форм запуска | FV2-3 | ожидает |
| FV2-10 | П3 | Три разборщика тега id находки (`waiver`, `s5_precheck._finding_tag`, `exit_gate._finding_tag_of`) — один выживший в модуле, импортируемом без `waiver`; четвёртый читатель строк слова `_record_s5_word_passes` — через того же читателя (`findings/20261113-tri-razbiratelya-id-nahodki-i-chetvyortyj-chitatel-strok-slova.md`; критик темы FV1-30b, F5 и отчёт фикса; FR-17, FR-54; AR-13, AR-15) | designer → builder → critic | `scripts/waiver.py`, `scripts/s5_precheck.py`, `scripts/exit_gate.py`, `scripts/controller.py`, `scripts/contract.py`, их тесты | FV1-30 | ожидает |
| FV2-11 | П3 | «Left with you» под (b) не одна строка данных: поправить фразу F4 спеки (по рекомендации критика) либо перенести выбор `to_check` в таблицу видов (`findings/20261113-left-with-you-pod-b-ne-odna-stroka-dannyh-build-left-items.md`; критик темы FV1-30b, F8; AR-1, FR-13) | builder → critic | `docs/tasks/specs/20261113-fv1-30b-word-fact-downstream-spec.md` | FV1-30 | ожидает |
| FV2-12 | П3 | `controller._record_person_pass` дописывает jsonl через `hooklib.append_jsonl_line` (ось карты 29) (`findings/20261113-record-person-pass-pishet-jsonl-mimo-hooklib-append-jsonl-line.md`; критик темы FV1-30b, Axis 29; FR-17; AR-14, AR-15) | builder → critic | `scripts/controller.py` (`_record_person_pass`), `docs/SIBLING_MAP.md`, их тесты | FV1-30 | ожидает |
| FV2-13 | П3 | Перепись выходов драйвера: строгий читатель JSON `dry_exits._read_json` → `known_red`; `prompt_sha` в `dry_stub` через `dry_exits.author_input_sha` (`findings/20261113-perepis-vyhodov-draivera-dva-klona-chitatel-json-i-hesh-prompta.md`; критик узла P1-b N1, F9, F10; FR-54; AR-13, AR-15) | builder → critic | `scripts/tests/dry_exits.py`, `scripts/tests/known_red.py`, `scripts/tests/dry_stub.py`, их тесты | P1-b N1, N2 (слиты) | ожидает |
| FV2-14 | П2 | Перепись выходов драйвера: долги Lead при слиянии N1 — строки осей 18/34/17 и вопрос 9 брифа критика, путь реестра красных строк в спеке, ключ `keep` N3, перепись на пути CI (`findings/20261113-perepis-vyhodov-draivera-dolgi-lead-n-l-i-put-ci.md`; критик узла P1-b N1, F12; AR-20, FR-44) | builder → critic | `docs/SIBLING_MAP.md`, `docs/tasks/critic-diff-brief.md`, `docs/tasks/specs/20261113-p1b-dry-story-spec.md`, `ai-packages/qa-factory/scripts/tests/test-layers.json` | P1-b N1, N3 | ожидает |
| FV2-15 | П3 | Тексты `run_suite` (`executor_unavailable`) и `story_budget` (`STORY BUDGET`) без записи в реестре отказов: класс строками `route:<name>` в файле классов переписи, пока записи нет (`findings/20261113-run-suite-i-story-budget-bez-zapisi-v-reestre-otkazov-klass-po-route.md`; слово Lead, критик узла P1-b N1, F1/Q1; FR-19; AR-1, AR-13) | builder → critic | `ai-packages/qa-factory/scripts/tests/fixtures/driver-exits/classes.json`, `ai-packages/qa-factory/scripts/tests/dry_exits.py` | P1-b N1 (фикс F1) | ожидает |
| FV2-16 | П2 | Дорога остановки и остальные ветки, где шов дирижёра вернул `Stop`, не пишут строку `driver-answers.jsonl` (повторный вопрос без блока FR-7); `plan_lines` дороги остановки теряются; строка теста «повторный запуск после остановки швом» в `test_story_run_loop_b_threshold.py` (`findings/20261114-doroga-ostanovki-seam-stop-ne-pishet-stroku-otvetov-i-plan-lines-teryayutsya.md`; критик узла FV1-3, Q1, Q3, Q6; FR-7; AR-24, AR-25) | designer → builder → critic | `ai-packages/qa-factory/scripts/driver_machine.py` (`_unread_halt_or_review`), `ai-packages/qa-factory/scripts/driver_dispatch.py` (`record_halt_words`), `ai-packages/qa-factory/scripts/tests/test_story_run_loop_b_threshold.py` | FV1-3 (слияние) | ожидает |
| FV2-17 | П3 | Строки карточек реестра на гейтах A/B идут к дирижёру через `_unread_kept_gate` без инструкции и обратной печати вопросного останова: одна ли дорога (скаут первым) (`findings/20261114-karty-reestra-gate-a-b-idut-k-dirizheru-bez-instrukcii-i-obratnoj-pechati.md`; критик узла FV1-3, Q2; P31, ось 34; AR-15, AR-17) | scout → builder → critic | `ai-packages/qa-factory/scripts/driver_machine.py` (`_unread_kept_gate`), `docs/SIBLING_MAP.md` | FV1-3 (слияние) | ожидает |
| FV2-18 | П3 | Хвост prompt дирижёра (инструкции, `MOVES_RULE`, `OWN_TOKEN_RULE`, `## The question`, срез текста вопроса) собирается в нескольких местах: один строитель (`findings/20261114-hvost-prompta-dirizhera-sobiraetsya-v-pyati-mestah.md`; критик узла FV1-3, Q4; FR-54; AR-13, AR-15) | builder → critic | `ai-packages/qa-factory/scripts/driver_conductor.py`, `ai-packages/qa-factory/scripts/driver_machine.py`, `ai-packages/qa-factory/scripts/driver_stage_build.py` | FV1-3 (слияние) | ожидает |
| FV2-19 | П3 | `record_answers` не включает в `recorded` id, пропущенные как тот же ответ (H6b): «recorded by code: nothing» про уже записанное (`findings/20261114-record-answers-ne-nazyvaet-id-propushchennye-kak-tot-zhe-otvet.md`; критик узла FV1-3, Q5; FR-41; AR-28) | builder → critic | `ai-packages/qa-factory/scripts/question_register.py` (`record_answers`), их тесты | FV1-3 (слияние), FV1-13 | ожидает |
| FV2-20 | П3 | `told_world` в `test_stage_joints.py` дважды сканирует пакет: один общий широкий скан (`findings/20261114-told-world-skaniruet-paket-dvazhdy.md`; критик темы T1, Q-a; FR-55; AR-12) | builder → critic | `ai-packages/qa-factory/scripts/tests/test_stage_joints.py` (`told_world`) | — | ожидает |
| FV2-21 | П2 | `stage_joints.rows_for` возвращает `[]` для нечитаемых строк: неизвестное как «требования нет»; пара `(rows, why)` (`findings/20261114-rows-for-vozvrashchaet-pustoe-kogda-stroki-ne-prochitany.md`; критик темы T1, Q-b, узел T3a; FR-41, FR-59; AR-28) | designer → builder → critic | `ai-packages/qa-factory/scripts/stage_joints.py` (`rows_for`), их тесты | T3a спеки `docs/tasks/specs/20261113-told-before-work-mechanism-spec.md` | ожидает |
| FV2-22 | П3 | Записи сквозных id в `refusal_registry.py:1404` несут `state: "walk_error"`, хотя это не ошибка: состояние-факт скана (`findings/20261114-check-id-zapisi-skvoznyh-vyhodov-nesut-sostoyanie-walk-error.md`; критик темы T1, Q-c, узел T2; FR-14; AR-18, AR-22) | builder → critic | `ai-packages/qa-factory/scripts/refusal_registry.py`, `ai-packages/qa-factory/scripts/tests/test_judgment_census.py` | T2 спеки `docs/tasks/specs/20261113-told-before-work-mechanism-spec.md` | ожидает |
| FV2-23 | П3 | Перепись «told»: копии читателей (`role_set`, `measure_untold`, `_hand_cards`, чтение `own`) и `_row_requirement` на 61 строку (`findings/20261114-told-dublikaty-chitatelej-i-row-requirement-na-60-strok.md`; критик темы T1, Q-d, Q-e; FR-54; AR-13, AR-15) | builder → critic | `ai-packages/qa-factory/scripts/stage_joints.py`, `ai-packages/qa-factory/scripts/tests/test_stage_joints.py` | — | ожидает |
| FV2-24 | П3 | `covered()` засчитывает id покрытым любым `<id>.<часть>`, а правило C14 уже (`findings/20261114-covered-pokryvaet-id-lyubym-pod-id.md`; критик темы T1, Q-f, узел T1r; FR-59; AR-28) | builder → critic | `ai-packages/qa-factory/scripts/tests/test_stage_joints.py` (`covered`) | T1r спеки `docs/tasks/specs/20261113-told-before-work-mechanism-spec.md` | ожидает |
| FV2-25 | П3 | `legacy_legs` и `unsited` переписи «told» — только потолок; вариант (a) равенство по умолчанию, выбор — Lead (`findings/20261114-legacy-legs-i-unsited-tolko-potolok.md`; критик темы T1, Q-g; AR-20) | builder → critic | `ai-packages/qa-factory/scripts/stage_joints.py`, `ai-packages/qa-factory/scripts/tests/test_stage_joints.py` | — | ожидает |
| FV2-26 | П3 | Группа «только дирижёр» читается из `note` строки переписи регулярным выражением `GROUP_RE`: поле строки (`findings/20261114-gruppa-tolko-dirizhera-chitaetsya-iz-note-cherez-regex.md`; критик темы T1, Q-i; AR-1, AR-13) | builder → critic | `ai-packages/qa-factory/scripts/tests/test_stage_joints.py`, `ai-packages/qa-factory/scripts/tests/fixtures/judgment-census.json` | T4, T9a, T9c спеки `docs/tasks/specs/20261113-told-before-work-mechanism-spec.md` | ожидает |
| FV2-27 | П3 | Две записки темы T1: осевой блок коммита T1c не перечисление (строка калибровки); неверный владелец `cmd_archive` в отчёте T1a (`findings/20261114-t1-zametki-osevoj-blok-kommita-i-owner-v-otchyote-t1a.md`; критик темы T1, Q-h, Q-j; FR-37) | builder → critic | `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md` | — | ожидает |

## Ход

Журнал передачи Lead пачки, новые записи в конец: `<дата время> — <что сделано, диспатчи t-nnn, хэши>`.

- 13.11 — пачка открыта (t-545): девять находок очередей критиков P1-a, P1-v, FV1-4, FV1-18, FV1-19.
- 14.11 — FV2-2: принято, ветка `wip/fv2-2` слита в main коммитом 4f37213 (отчёт волны 2 `docs/tasks/specs/reports/20261113-wave2-integration-report.md`); зависимость FV2-1 этим отчётом не названа слитой, статус FV2-1 не тронут.

## Живые доказательства

| Что | Стенд / проект | Кто | Статус |
|---|---|---|---|

## Остатки
