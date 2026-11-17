# Сказано до работы — пачка 1: доделка (id на отказы, карточки в строки, закрытие счётчиков)

кучка: `told-before-work` | статус: ожидает | взял: — | ветка: — | MR: — | стенд: не нужен | приоритет: П1

Правило готовности: пачка закрыта, когда каждый узел «принято», свидетели узлов — в журнале взявшего,
живые доказательства (FR-33) сделаны или переданы строкой в кучку «живые прогоны».

Решения владельца: слово владельца 17.11.2026 по Q-O1 (предел размера страниц): «не в ущерб правилам. Если не влезет можно поднять» — текст правил не режется ради предела, предел роли поднимается именованной записью (роль, байты, причина); F-6 читается как (b) с записью.
Решения Lead (17.11.2026, спека `docs/tasks/specs/20261117-told-before-work-finish-spec.md`, раздел «Lead decisions on the forks»): F-1 (a), F-2 (b), F-3 (b), F-4 (a) только если T9c п. 0 красен, F-5 (a), F-7 (a), F-8 (a) — эта кучка и есть дом строк, F-9 (a).
Порядок по общим файлам: `judgment-census.json` — слияния последовательно T4b → T7f → T9c → T9a; `scripts/validate_artifacts.py` и `test_validators.py` — T7a-A → T7a-B → T7a-C (списки функций, D-0048); `test_detector_verdict.py` — каждый узел владеет одной новой функцией `tbw_<узел>_sites`; `told_ratchet.unsited` и пин K12 (`test_stage_joints.py:927-932`) двигает только интегратор волны (F-1 (a)).
Скоуп свидетеля: по узлам — то, что печатает `scenario_walk.py --witness-for <owns>`, плюс быстрые файлы карточки, `stage_joints.py --check`, `selftest.py --limits --lang`; медленные файлы судит канон пачки; BATCH CANON на CI — координатор.
Общий бриф дизайнерам: спека `docs/tasks/specs/20261117-told-before-work-finish-spec.md` (§0 замер, §1 архитектура, §6 карточки, §7 строки) и механизм-спека `told before work`; вернуть спеку-ответ по карточке; DoD узла — в общем DoD §6.

Пути «Пишет в»: пакета — от `ai-packages/qa-factory/`; Lead пачки уточняет списки функций при взятии.

## Бриф

Что сделать: строки таблицы ниже — дословно из §7 спеки (метки спеки `TBW1-1 (M9)` … `TBW1-15 (close)`; id узлов — `TBW1-1` … `TBW1-15`: форма `<инициалы><N>-<n>` требует `tools/test_pile_cards_contents.py`); ни T5b, ни T7a-8, T7d, T7e, T8 в пачке нет — поглощены или без работы (спека §0). Волна A (шесть писателей): T4a, T5r, T6, T7a-A, T7b, T7c (T5r после слияния `RD1-22 (FL9)` из `rules-debt/1`); волна B: T4b, T7a-B, T7a-C, T3b (после M9 и порядка по `test_ahead_cards.py`), T9a (работа сейчас, слияние после T9c), K1b (узел FV2-79 в `live-run-fvf/2`); волна C: T7f, T9c, T1r-cards-билдер (после передрафта и критика); волна D: `TBW1-15 (close)`. M9 и передрафт T1rc — Lead и дизайнер, волна 0.
НЕ делать: правок текста отказов (побайтно прежний вывод); новых файлов тестов (одна новая функция на узел в существующем файле); правок `stage-joints.json` вне `TBW1-11 (T9c)`, `TBW1-13 (T1rc)`, `TBW1-15 (close)`; K1b не переносится в эту пачку — Lead добавляет его id в «Зависит от» там, где нужно.

## Узлы

Исполнитель «designer → builder → critic» — кодовый узел; «builder» — узел-документ. Статусы:
`ожидает` → `в работе` → `сдано` → `принято` / `отклонено`.

| Узел | Приоритет | Что | Исполнитель | Пишет в | Зависит от | Статус |
|---|---|---|---|---|---|---|
| TBW1-1 | П1 | метка спеки: TBW-M9; Опыт M9: переживает ли страница из `--append-system-prompt-file` и строка промпта `claude -p --resume` (спека finish §4) (находка: `findings/20261117-tbw-m9-perezhivaet-li-stranitsa-resume.md`) | Lead | `docs/tasks/specs/reports/20261117-tbw-m9.md` | — | ожидает |
| TBW1-2 | П1 | метка спеки: TBW-T4a; id строк §5.3 на отказах `guard_pre_tool`/`host_adapter` (FV1-27 строки 2, 11) (находка: `findings/20261117-tbw-t4a-id-strok-na-otkazah-guard-pre-tool.md`) | builder → critic | `scripts/guard_pre_tool.py` (функции карточки), `scripts/host_adapter.py` (`role_policy`), `scripts/tests/test_detector_verdict.py` (`tbw_t4a_sites`) | — | принято: 71d36190 (t-965) |
| TBW1-3 | П1 | метка спеки: TBW-T4b; id строк §5.3 25-31 на `stage_guard`/`hooklib`; перепись G-dispatch → conductor (находка: `findings/20261117-tbw-t4b-id-strok-na-stage-guard-i-hooklib.md`) | builder → critic | `scripts/stage_guard.py`, `scripts/hooklib.py` (функции карточки), `scripts/tests/fixtures/judgment-census.json`, `test_detector_verdict.py` (`tbw_t4b_sites`) | перепись: первым | принято: 7b095bad (t-1031) |
| TBW1-4 | П1 | метка спеки: TBW-T5r; id строк §5.4 на `s5_precheck` (11) и `manifest_put` (14) (находка: `findings/20261117-tbw-t5r-id-strok-na-s5-precheck-i-manifest-put.md`) | builder → critic | `scripts/s5_precheck.py` (семейства), `scripts/manifest_put.py`, `test_manifest_put_merge.py`, `test_s5_precheck_sides.py` | — | принято: 71d36190 (t-970) |
| TBW1-5 | П1 | метка спеки: TBW-T6; id 21 строки `handoff_check` (находка: `findings/20261117-tbw-t6-id-21-stroki-handoff-check.md`) | builder → critic | `scripts/handoff_check.py` (строители задач; не `_review_receipt`), `test_detector_verdict.py` (`tbw_t6_sites`) | FV2-78 — списки функций | принято: 71d36190 (t-963) |
| TBW1-6 | П1 | метка спеки: TBW-T7a-A/B/C; id 42 строк `validate_artifacts` (три узла по функциям) (находка: `findings/20261117-tbw-t7a-id-42-strok-validate-artifacts.md`) | builder → critic | `scripts/validate_artifacts.py` (списки функций), `test_validators.py` | A → B → C по общему файлу | принято: 7b095bad (t-1024) |
| TBW1-7 | П1 | метка спеки: TBW-T7b; id 12 строк `planning_contract` (находка: `findings/20261117-tbw-t7b-id-12-strok-planning-contract.md`) | builder → critic | `scripts/planning_contract.py`, `test_detector_verdict.py` (`tbw_t7b_sites`) | — | принято: 71d36190 (t-966) |
| TBW1-8 | П1 | метка спеки: TBW-T7c; id 2 строк `coverage_contract` (находка: `findings/20261117-tbw-t7c-id-2-strok-coverage-contract.md`) | builder → critic | `scripts/coverage_contract.py`, `test_detector_verdict.py` (`tbw_t7c_sites`) | — | принято: 71d36190 (t-967) |
| TBW1-9 | П1 | метка спеки: TBW-T7f; перепись единиц `stage_done` → conductor (F-W2 (a)) (находка: `findings/20261117-tbw-t7f-perepis-edinic-stage-done.md`) | builder → critic | `judgment-census.json` | T4b | принято: f216597f (t-1061) |
| TBW1-10 | П1 | метка спеки: TBW-T9a; id 6 строк `controller:*`; перепись ролей (находка: `findings/20261117-tbw-t9a-id-6-strok-controller.md`) | builder → critic | `scripts/controller.py` (функции карточки), `judgment-census.json`, `test_controller_doors.py` | T9c (перепись); FV2-88 | ожидает |
| TBW1-11 | П1 | метка спеки: TBW-T9c; раздел «What code will check in this launch» у дирижёра; строки дирижёра; `_producer_leg` (находка: `findings/20261117-tbw-t9c-razdel-what-code-will-check-u-dirizhera.md`) | builder → critic | `scripts/no_move.py`, `scripts/stage_joints.py` (`_producer_leg`), `references/stage-joints.json` (строки дирижёра), `judgment-census.json`, `test_controller_doors.py` | T7f (перепись) | ожидает |
| TBW1-12 | П1 | метка спеки: TBW-T3b; бриф без карточек, строка групп, `first_look:put` (находка: `findings/20261117-tbw-t3b-brif-bez-kartochek-stroka-grupp.md`) | builder → critic | `scripts/brief_pack.py`, `window_record.py`, `story_step.py` (`_prompt`, `_card_text`), `first_look.py`, `test_first_look.py` | TBW1-1 (M9); T1r-cards по `test_ahead_cards.py` | ожидает |
| TBW1-13 | П1 | метка спеки: TBW-T1rc; карточки → строки: передрафт дизайнера (B2, B3), критик на изменённые части, затем билдер -a/-b (находка: `findings/20261117-tbw-t1rc-kartochki-v-stroki-peredraft.md`) | designer → critic → builder | `docs/tasks/specs/20261117-told-before-work-t1r-cards-spec-r2.md` (по передрафту) | — | в работе |
| TBW1-14 | П1 | метка спеки: TBW-T10; носители Lead: ось 38, AR-10/AR-9, FR-38, critic-brief, калибровка (находка: `findings/20261117-tbw-t10-nositeli-lead-os-38.md`) | Lead | `docs/SIBLING_MAP.md`, `design/architecture.md`, `design/factory-rules.md`, `docs/tasks/critic-diff-brief.md`, `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md` | — | ожидает |
| TBW1-15 | П1 | метка спеки: TBW-close; закрытие: счётчики `told_ratchet` и `told-ratchet.json` по замеру, мёртвый код карточек (находка: `findings/20261117-tbw-close-zakrytie-schetchikov-told-ratchet.md`) | builder | `references/stage-joints.json` (`told_ratchet`), `told-ratchet.json`, `test_stage_joints.py` (пины счётчиков), `contract_slices.py` | все узлы | ожидает |

## Ход

Журнал передачи Lead пачки, новые записи в конец: `<дата время> — <что сделано, диспатчи t-nnn, хэши>`.

- 17.11 (t-980) — пачка открыта строками §7 спеки `docs/tasks/specs/20261117-told-before-work-finish-spec.md` (малый пакет билдеру), по находке на строку.

## Живые доказательства

| Что | Стенд / проект | Кто | Статус |
|---|---|---|---|

## Остатки
