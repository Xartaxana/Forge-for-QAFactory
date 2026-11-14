# Думающие роли — пачка 6: хвосты пачек 1, 2 и 4 приоритета П3

кучка: `thinking-roles` | статус: ожидает | взял: — | ветка: — | MR: — | стенд: не нужен | приоритет: П3

Правило готовности: пачка закрыта, когда каждый узел «принято», свидетели узлов — в журнале взявшего, живые доказательства (FR-33) не требуются.

Решения владельца: хвосты пачек 1, 2 и 4 собраны по приоритету словом владельца 12.11.2026.
Порядок по общим файлам: `scripts/story_run.py`: TR2-10 → TR4-16 (функции не пересекаются, списки в «Пишет в»); TR2-10 идёт после TR2-5 пачки 5 (общий `story_run.py`).
Скоуп свидетеля: тестовый файл каждого своего пути (до минуты); медленные `test_story_run_*`, `test_controller_*` — только CI; канон пачки — пайплайн CI.
Общий бриф: узел исполняется по разделу со своим id в находке, названной в ячейке «Что».

## Бриф

Цель пачки: хвосты пачек 1, 2 и 4 приоритета П3 — узлы, которые остались ожидать после того, как приняты узлы П1 этих пачек; каждый узел исполняется по разделу со своим id в находке, названной в «Что». Начать с узлов, у которых в «Зависит от» стоит «—» или только принятые узлы: TR2-13, TR4-16, TR4-17; TR1-7 ждёт TR1-6 пачки 5, TR2-10 — TR2-5 пачки 5.

## Узлы

Статусы: `ожидает` → `в работе` → `сдано` → `принято` / `отклонено`.

| Узел | Приоритет | Что | Исполнитель | Пишет в | Зависит от | Статус |
|---|---|---|---|---|---|---|
| TR1-7 | П3 | Остатки ревью ходока: пин настоящей пересборки записи, непокрытые края, тест двух учёток исполняется в CI, повторы кода. Раздел TR1-7 той же находки | builder | `scripts/tests/test_walk_road.py`, `scripts/tests/test_walk_two_actors.py`, `scripts/walk_session.py` | TR1-6 | ожидает |
| TR2-10 | П3 | Лишний вопрос `s1_gap`: ответ на таблицу источников записан решением класса и читается перед вопросом о недостижимом источнике. Раздел TR2-10 той же находки | scout → builder | `scripts/story_run.py` | TR2-5 | ожидает |
| TR2-13 | П3 | Спеки t-1957, t-1991, t-1988, хартия аналитика и `docs/SIBLING_MAP.md` приведены к коду ночных пачек (узел-документ). Раздел TR2-13 той же находки | builder | `docs/tasks/specs/t-1957-fast-manual-walker.md`, `docs/tasks/specs/t-1991-analyst-settles-places.md`, `docs/tasks/specs/t-1988-acceptance-chain-close.md`, `agents/qa-failure-analyst.md`, `docs/SIBLING_MAP.md` | — | ожидает |
| TR4-16 | П3 | Остатки ревью TR3-10 D: одно чтение первого стенда и публичные имена, ключи пулов через `fold_kind`, `walk_assign_step` на три шага, возврат в S6 после ответа `added`. Находка `findings/20261111-uchyotki-obhodov-ostatki-revyu.md` | builder | `scripts/walk_pool.py`, `scripts/project_decisions.py`, `scripts/guard_secrets.py`, `scripts/gate_preflight.py`, `scripts/config_contract.py`, `scripts/story_run.py` (`take_answer`, `walk_gap_role`, `_answer_walk_supply`, `walk_assign_step`), `scripts/tests/` | TR3-10 | ожидает |
| TR4-17 | П3 | Остатки цепочки проб t-2064: одиннадцать пунктов находки `findings/20261111-proby-ostatki-cepochki.md` | builder | `scripts/manifest_put.py`, `scripts/proof_level.py`, `scripts/probe_by_code.py`, `scripts/planning_contract.py`, `scripts/check_witness.py`, `scripts/tests/test_probe_by_code_languages.py`, `scripts/tests/test_brief_pack.py` | слияние цепочки проб (TR2-14) | ожидает |
| TR6-1 | П3 | Остатки TR3-9 (критик t-096, канон 43208727152): сборка строк промпта вынесена из `run_manual_lane`; одно тело для `_window_beside_running` / `_lane_beside_running` и для `parallel_windows` / `walkers`; мёртвое слагаемое в `run_complete`; строка об известном остатке отчёта; причина одного нестабильного пина `test_walk_lanes_parallel` разобрана. Пять пунктов раздела «Что именно менять» находки `findings/20261112-tr3-9-ostatki-dorozhek-ruchnogo-prohoda.md` | scout (п. 5) → builder → critic | `scripts/driver_stage_s6.py (run_manual_lane, run_complete)`, `scripts/controller.py (_window_beside_running, _lane_beside_running)`, `scripts/config_contract.py (parallel_windows, walkers)`, `design/state-exits.md`, `scripts/tests/test_walk_lanes_parallel.py` | — | ожидает |
| TR6-2 | П3 | Нестабильный тест `test_controller_rework_repair_binding` (FR-31, красный один раз на каноне 43342086225, не воспроизведён): первый шаг — печатать `repr` исключения в падающей проверке «a recorded id under a fresh key is refused» (`findings/20261113-test-controller-rework-repair-binding-krasnyj-odin-raz-fr-31.md`; t-247 Red 2) | builder | `scripts/tests/test_controller_rework_repair_binding.py` | — | принято: 7da38c2 (t-436) |
| TR6-3 | П3 | CL-NS: детектор «роль без shell перечислена на карточке команды, которую никто ей не велит запускать» — соединение данных в быстром тесте (кандидат `test_ahead_cards.py`): каждая роль записи `role-commands.json` имеет `host_adapter.role_has_bash` истинным, кроме записи с явным ключом данных `no_shell_road`; четыре строки дрейфа исправляются в том же узле (`findings/20261114-cl-ns-detektor-roli-bez-shell-na-karte-komand.md`; критик кода A2/A3/F7-пересборки, Q5; FR-56, FR-12; AR-11, AR-29) | designer → builder → critic | `ai-packages/qa-factory/scripts/tests/test_ahead_cards.py`, `ai-packages/qa-factory/references/role-commands.json`, `ai-packages/qa-factory/scripts/host_adapter.py` | — | ожидает |

## Ход

Журнал передачи Lead пачки, новые записи в конец: `<дата время> — <что сделано, диспатчи t-nnn, хэши>`.

- 12.11.2026 — пачка открыта словом владельца: хвосты П3 пачек 1, 2 и 4 вынесены из них, чтобы те закрывались по узлам П1 и П2 (t-097).

- 14.11 — TR6-2: второе наблюдение той же красной строки (канон 43515748054 волны 3, первая попытка shard 1, зелёный на перезапуске) дописано в находку `findings/20261113-test-controller-rework-repair-binding-krasnyj-odin-raz-fr-31.md`; отдельной находки в `live-run-fvf` нет (дубль не заводился).

## Живые доказательства

Живые доказательства узлов этой пачки ведутся в `live-runs` (слово владельца 11.11.2026).

| Что | Стенд / проект | Кто | Статус |
|---|---|---|---|

## Остатки
