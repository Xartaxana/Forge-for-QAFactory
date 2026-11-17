# Сухая стори идёт в CI на main — пачка 3: посадка ветки, перепись, метки, задача CI, обход групп

кучка: `live-run-fvf` | статус: в работе | взял: dev1, 17.11.2026 | ветка: `pile/live-run-fvf/batch-3` | MR: — | стенд: не нужен | приоритет: П1

Правило готовности: пачка закрыта, когда каждый узел «принято», свидетели узлов — в журнале взявшего,
живые доказательства (FR-33) сделаны или переданы строкой в кучку «живые прогоны».

Решения владельца: нет (направление каждого узла выбрано Lead, 17.11.2026, раздел «Решения Lead по развилкам» и «…фикс-раунда» спеки).
Скоуп свидетеля: по узлам, при взятии; свидетель — то, что печатает `scenario_walk.py --witness-for <owns>`; медленные файлы судит канон пачки.
Общий бриф дизайнерам: спека `docs/tasks/specs/20261117-p1b-finish-spec.md` (узлы L1, L1c, L2, N4R, N2h, N5, N4, N4c, N6, N3t, N3a) + вердикт критика на план `docs/tasks/specs/reviews/t-955-p1b-finish-plan.md`.

Пути «Пишет в»: пакета — от `ai-packages/qa-factory/`; Lead пачки уточняет их при взятии.

Пачка открыта 17.11.2026 (Lead пачки): слово владельца 17.11 «всё что недоделанно делаем сегодня»; находки L0 (метки реестров `main/S5`, `N4S0-1`, `N4S14-1`, `P1B-2f`) ложатся сюда (D-0044). Узлы L0, L-ax, N-L спеки — работа Lead, строками пачки не заведены. Размер — больше L (19 строк): Lead при взятии решает, не уходят ли FV3-16…FV3-19 в пачку 4 (правило карточки).

очередь: live-run-fvf/3 FV3-1 → forge/7 FG7-15 → forge/7 FG7-19 (`scenario_walk.py`, `test-layers.json`; F-P10 (а); для FG7-38 строка не нужна — F-P5 (а): числа расписания пишет FV3-2)

## Бриф

Что сделать: узлы таблицы ниже; порядок спеки: FV3-1 → FV3-15 → (ось 38, Lead) → CI → FV3-2 → критик посадки (CR-L) → волна 1 в `main`; затем FV3-3, FV3-4, FV3-5 параллельно; затем группы FV3-6…FV3-9; затем FV3-10; поздние FV3-11…FV3-14. Инвариант всего порядка: `main` не краснеет ни после одного слияния (`dry_exits.py --check` = 0 расхождений на дереве волны).
НЕ делать: правки в замороженном дереве релиза; правки кода продукта вне `scripts/tests/` узлами FV3-1…FV3-15; узлы FV3-16…FV3-19 — находки: причина и направление устанавливаются разбором, не догадкой исполнителя.

## Узлы

Исполнитель «designer → builder → critic» — кодовый узел; «builder» — узел-документ. Статусы:
`ожидает` → `в работе` → `сдано` → `принято` / `отклонено`.

| Узел | Приоритет | Что | Исполнитель | Пишет в | Зависит от | Статус |
|---|---|---|---|---|---|---|
| FV3-1 | П1 | Посадка сухой стори: ветка `wip/p1b-n4m` сливается в `main` одной волной с FV3-15 и FV3-2; канон и ночь начинают гонять `test_scenario_dry_1.py` (спека `docs/tasks/specs/20261117-p1b-finish-spec.md` §4 L1, CR-L) | builder → critic | `scripts/tests/dry_*.py`, `scripts/tests/test_scenario_dry_1.py`, `scripts/tests/scenario_walk.py`, `scripts/tests/form_filler.py`, `scripts/tests/test_field_producers.py`, `scripts/tests/fixtures/{driver-exits,stories/dry-1,form-fill-rules.json,form-rounds.json}`, `scripts/tests/test_form_selftest.py`, `scripts/tests/test-layers.json` (строка keep), `scripts/selftest.py`, `scripts/slow_tests.json` | — | принято: caef09e3 (t-972) |
| FV3-15 | П1 | Перепись выходов догоняет `main` (стыки 40 → 267) + ось 38 карты (§4 L1c, L-ax; F-P14) | builder (+ Lead: ось) | `scripts/tests/fixtures/driver-exits/{gates,hooks,s0,s1-s4,s5,s6-s9}.json`; `docs/SIBLING_MAP.md` (Lead) | FV3-1 | принято: caef09e3 (t-978) |
| FV3-2 | П1 | Метки реестров истинны на слиянии: `main/S5`, `kind:halt/free words`, `s1.review/unavailable`, `P1B-2f` — на узлы с файлом находки; числа расписания по CI (§4 L2; F-P4, F-P5, F-P19) | builder | `scripts/tests/fixtures/driver-exits/known_red.json`, `…/stories/dry-1/selftest/known_red.json`, `…/stories/dry-1/exits/s1-s4.json` (F-P4 (б)), `scripts/tests/fixtures/form-rounds.json`, `scripts/slow_tests.json`, `scripts/selftest.py` | FV3-15 | принято: da9e2354 (t-987) |
| FV3-3 | П1 | Реестр меток по файлу на группу; `--judge` убран (§4 N4R; F-P1, F-P17) | builder → critic | `scripts/tests/dry_exits.py` (`check`, `_ledger_orphans`, `judge`), `scripts/tests/test_scenario_dry_1.py` (`main`), `scripts/tests/fixtures/driver-exits/known_red*` | FV3-2 | принято: f22600df (t-1020) |
| FV3-4 | П1 | Задача CI `dry-story` в `dry-story.yml`, вызовы ночи и двери `dry_only`, спайк удалён (§4 N5; F-P2, F-P3, F-P6, F-P16, F-P20) | builder → critic | `.github/workflows/{dry-story,nightly,canon}.yml`, `tools/test_workflows.py` | FV3-2 | принято: 905e9735 (t-1021) |
| FV3-5 | П1 | Заглушка критика кода S5 запускает `probe_by_code.py` (а) и метка главного прохода по CI (б) (§4 N2h; F-P7, F-P18); находка `findings/20261117-p1b-s5-zaglushka-kritika-ne-zapuskaet-probu.md` | builder → critic | `scripts/tests/dry_stub.py`, `scripts/tests/fixtures/stories/dry-1/story.json`; (б) `…/driver-exits/known_red.json` (`main/*`), `scripts/slow_tests.json` | FV3-2; (б) FV3-3 | принято: b1243561 (t-1022) |
| FV3-6 | П1 | Строки обхода группы `gates` (§4 N4) | builder | `scripts/tests/fixtures/stories/dry-1/{exits,seeds}/gates.json`, `scripts/tests/fixtures/driver-exits/gates.json`, `…/driver-exits/known_red/gates.json` | FV3-3, FV3-4 | принято: b90b73a4 (t-1069) |
| FV3-7 | П1 | Строки обхода группы `s5` (§4 N4) | builder | то же для `s5` | FV3-3, FV3-4, FV3-5 | ожидает |
| FV3-8 | П1 | Строки обхода группы `s6-s9` (§4 N4) | builder | то же для `s6-s9` | FV3-3, FV3-4, FV3-5 | ожидает |
| FV3-9 | П1 | Строки ключей цен групп `s0`, `s1-s4` (F-P9) | builder | `…/stories/dry-1/exits/{s0,s1-s4}.json` | FV3-3 | ожидает |
| FV3-10 | П1 | Перепись ключей вопросов: ключи сухой стори в `driven`, `PINNED_ELSEWHERE` сжимается (§4 N4c) | builder → critic | `scripts/tests/test_conductor_doors.py`, `scripts/tests/test-layers.json` (covers) | FV3-6…FV3-9 | ожидает |
| FV3-11 | П2 | Вторая строка раннеров TS/Playwright (§4 N6) | builder → critic | `…/stories/dry-1/runners/ts-playwright/`, `.github/workflows/dry-story.yml`, `tools/test_workflows.py` | FV3-4, FV3-7 | ожидает |
| FV3-12 | П2 | Типы сверх `default` (§4 N3t; A1; F-P11) | designer → builder | `…/stories/dry-<type>/`, `…/stories/dry-types.json`, `scripts/tests/test_scenario_dry_1.py` (`main`) | FV3-1, FV3-10 | ожидает |
| FV3-13 | П2 | «Сказано до работы» в сухой истории (§4 N3a; A2) | builder → critic | `scripts/tests/dry_exits.py` (`told_before_work`), `scripts/tests/test_scenario_dry_1.py` (`_print_told`) | FV3-3, П1-в N0 | ожидает |
| FV3-14 | П2 | Двойной счёт `live_only` (F-P8 (б) — только при чтении 2) | builder | `scripts/tests/dry_exits.py` (`_count_reach`) | FV3-6…FV3-8 | ожидает |
| FV3-16 | П1 | Находка: свободные слова человека на вопросе `halt` не доходят до роли (бывшая `N4S0-1`); причина не установлена — драйвер или стык заглушки (`findings/20261117-p1b-s0-halt-svobodnye-slova-ne-dohodyat.md`) | Lead (разбор) → builder | по разбору (кандидаты из находки: `scripts/driver_machine.py`, `scripts/tests/dry_stub.py`) | — | ожидает |
| FV3-17 | П2 | Находка: ответ ключа цен предлагается условно, у ходока нет условия (бывшая `N4S14-1`; класс F-P4 (в)) (`findings/20261117-p1b-uslovnyj-otvet-bez-usloviya-u-hodoka.md`) | builder | `scripts/tests/dry_exits.py` / `dry_world.py` (грамматика условия) — по решению F-P4 | FV3-3 | ожидает |
| FV3-18 | П1 | Находка: `window_record.row_field_gaps` требует `obligation_hash`, а контракт и `manifest_put.py` его отказывают (бывшая `P1B-2f`) — по F-P19 (а) (`findings/20261117-p1b-2f-obligation-refs-hesh-trebuet-i-otkazyvaet.md`) | Lead → builder | продукт: по разбору (кандидаты из находки: `scripts/window_record.py`, `scripts/tests/fixtures/form-rounds.json`) | — | ожидает |
| FV3-19 | П2 | Находка: у вложенного списка `probes.records` нет объявленного пустого исхода (`handoff.py:515-533`) (`findings/20261117-p1b-probes-records-bez-pustogo-ishoda.md`) | builder | продукт: `scripts/handoff.py` / контракт — по разбору | — | ожидает |
| FV3-20 | П1 | Находка: после N2h-а главный проход встаёт на S5 по новой причине — заглушка критика кода не пишет запись окна (`window_record.py`) и дайджест; `probes.runtime_provenance` у критика без производителя — кандидат `product gap` (`findings/20261117-p1b-s5-kritik-ne-pishet-okno-i-daidzhest.md`) | designer → builder → critic | `scripts/tests/dry_stub.py` (ветка критика S5), `scripts/tests/fixtures/stories/dry-1/story.json` (строка `qa-code-critic@S5`); метка — `…/driver-exits/known_red.json` (`main/S5`) | FV3-5 | принято: 0bdf33c0 (t-1109) |
| FV3-21 | П1 | Находка: ручная половина S6 уходит в проход без стенда после слова человека «без стенда» — `manual_lane_plan` не читает `s6_no_stand` (`findings/20261117-s6-ruchnaya-polovina-bez-stenda.md`) | designer → builder → critic | продукт: `scripts/driver_stage_s6.py` (`manual_lane_plan`), `scripts/driver_stage_build.py` (`stand_question_text`), `skills/qa-story/phases/s6.md`; метка — `…/driver-exits/known_red.json` (`main/S6`); карточка — `docs/tasks/specs/20261117-s6-manual-half-no-stand-card.md` | FV3-20 | принято: c96d9bc2 (t-1228) |
| FV3-22 | П1 | FV3-21c: путь скилла (`story_step.py`) закрывает ручную половину S6, где каждый ручной кейс отказан словом «без стенда» — сейчас закрытие есть только в методах Driver (`manual_close`, `consumer_need_record`, `close_receipt`); общий код вынести, не копировать (Lead 17.11.2026, вердикт критика t-1173 F6) | designer → builder → critic | продукт: `scripts/story_step.py`, `scripts/driver_stage_s6.py`; карточка — `docs/tasks/specs/20261117-fv3-21c-skill-road-s6-close-card.md` | FV3-21 | ожидает |
| FV3-23 | П1 | Главный проход сухой стори после FV3-21 встаёт на S7: заглушка не держит строку для `qa-failure-analyst@S7` (stub-call S7-qa-failure-analyst-1 wrote=0) — владелец метки `main/S6` в `known_red.json` (Lead 17.11.2026, вердикт критика t-1173 F6) | builder → critic | `scripts/tests/` (заглушка сухого мира, строка S7 аналитика); метка — `…/driver-exits/known_red.json` | FV3-21 | ожидает |
| FV3-24 | П1 | FV3-21d: путь скилла прогоняет остальные кодовые шаги S6 — повторная проба HF8-18 (`s6_reprove_before_manual`) перед ручной половиной и приёмку S6 аналитиком (Q-a3 карточки FV3-21c) (Lead 17.11.2026, развилка F4 карточки FV3-22) | scout → designer → builder → critic | продукт: `scripts/story_step.py`, `scripts/stage_close.py`; карточка — раздел §7 `docs/tasks/specs/20261117-fv3-21c-skill-road-s6-close-card.md` | FV3-22 | ожидает |
| FV3-25 | П2 | Находка: сухой мир не ставит S5 в состояния сбоя — строки девяти ключей S5 стали `live_only` с измеренной причиной (канон 44119861422) (`findings/20261117-p1b-s5-fault-states-unreachable-in-dry-world.md`) | builder → critic | `scripts/tests/dry_world.py`, `dry_stub.py`, `fixtures/stories/dry-1/{exits,seeds}/s5.json` | FV3-7 | ожидает |
| FV3-26 | П2 | Путь скилла закрывает кодовые шаги S7 и S9 так же, как S6 (развилка R2-F3 карточки FV3-22 r2; близнецы оси 5 «Code-only stage closes») (Lead 17.11.2026) | scout → designer → builder → critic | продукт: `scripts/story_step.py`, `scripts/stage_close.py`; карточка — `docs/tasks/specs/20261117-fv3-21c-skill-road-s6-close-card-r2.md` | FV3-22 | ожидает |
| FV3-27 | П2 | Один продуктовый предикат «источник спрошен открыто» (`source_inventory.asked_open(task_root)`): его зовут `driver_sources.py` (~754-762) и `dry_world.WORLD_FACTS` вместо копии в обходчике; край — пропавшая/нечитаемая опись читается как «предложено», как в продукте (F3 вердикта критика t-1217; до слияния сторожем стоит F2) (Lead 17.11.2026) | builder → critic | продукт: `scripts/source_inventory.py`, `scripts/driver_sources.py`; `scripts/tests/dry_world.py` | FV3-17 | ожидает |
| FV3-28 | П2 | Условия 19 ответов, выброшенных из строк обхода «→ FV3-17» (s5: `s5.repair_limit/round\|fixed`, `exit.resume_limit*/round\|fresh\|go on`, `code_close.behind/go on`, `code_close.closed_story/full retro\|retry\|go on`; s6-s9: `s6.stand_confirm/retry\|stand name`, `.login/find the way in\|stand name`, `s7.repair_limit/round`, `s6.gate_a_dry/reapprove`): на каждое условие — читатель факта мира в `WORLD_FACTS` по образцу `inventory_unavailable` или слово Lead, что условие остаётся выброшенным; плюс п. 2 FV3-17 (вернуть `s1.review/unavailable` с `offered_if`) после слияния FV3-9 (F5 вердикта t-1217) (Lead 17.11.2026) | designer → builder → critic | `scripts/tests/dry_world.py`, `stories/dry-1/exits/*.json`, `stories/dry-1/seeds/*.json` | FV3-17, FV3-7, FV3-8, FV3-9 | ожидает |
| FV3-29 | П3 | Остаток R2-F2 карточки FV3-22 r2: охват A27 закрытия S6 на пути скилла, который grep узла -1 не видит сегодня (вердикт t-1209 §2) (Lead 17.11.2026) | scout → builder → critic | `scripts/stage_close.py` (уточнит скаут) | FV3-22 | ожидает |
| FV3-30 | П2 | Живое условие `sibling_in` для пустого `rounds` у S7-автоматора рядом с `fix_result: fixed` (находка: `findings/20261117-rounds-pustoy-pri-fix-result-fixed.md`; вердикт t-1219 R2, карточка FV3-19 r2 приложение A) (Lead 17.11.2026) | builder → critic | `scripts/null_outcomes.py`, `handoffs/s7-automator-to-analyst.yaml`, `scripts/handoff.py`, `scripts/tests/test_s7_null_outcome.py`, `scripts/tests/test_handoff.py` | FV3-19 | ожидает |

## Ход

Журнал передачи Lead пачки, новые записи в конец: `<дата время> — <что сделано, диспатчи t-nnn, хэши>`.

- 17.11 (t-969) — пачка открыта (L0 спеки `docs/tasks/specs/20261117-p1b-finish-spec.md`): строки FV3-1…FV3-19 и пять находок меток реестров. Метки отдают: `main/S5 -> FV3-5`, `kind:halt/free words -> FV3-16`, `s1.review/unavailable -> FV3-17` (строка реестра и строка обхода удаляются по F-P4 чтение 2; метка не ставится), `obligation_refs <- … -> FV3-18` (F-P19 (а)). Взятие пачки (`piles.py take live-run-fvf 3`) — отдельным ходом после этого.
- 17.11 (t-1047) — находка FV3-20 (после N2h-а остановка S5 сменила причину, F10 критика t-1029); метка `main/S5 -> FV3-20`; узел N2h-в — спека `docs/tasks/specs/20261117-p1b-n2h-v-critic-stub-window-card.md`. Строка теста FV3-5 «`probes.runtime_provenance` заполнено после пробы» (находка `…-ne-zapuskaet-probu.md:31`) переносится в FV3-20 (F7, Lead 17.11.2026).
- 17.11 (t-1109) — находка FV3-21 (вердикт критика t-1106, Q1-Q3: ручная половина S6 не читает слово «без стенда», продуктовый дефект); метка `main/S6 -> FV3-21`; карточка узла — `docs/tasks/specs/20261117-s6-manual-half-no-stand-card.md` (дизайнер). Метка с t-1098 (`FV3-20`) исправлена по J2-2 вердикта.
- 17.11 (t-1217, t-1209) — критик групп P1-b: снимок `S<n>` — мир после закрытия `S<n>`; фикс-раунды t-1223 (s5), t-1224 (s6-s9), t-1225 (FV3-17), t-1226 (FV3-9). Новые строки FV3-27 (один предикат asked_open, F3), FV3-28 (условия 19 ответов, F5), FV3-29 (остаток R2-F2 FV3-22). Карточка FV3-22 приняла решения Lead по t-1209 (Lead 17.11.2026).

## Живые доказательства

| Что | Стенд / проект | Кто | Статус |
|---|---|---|---|

## Остатки
