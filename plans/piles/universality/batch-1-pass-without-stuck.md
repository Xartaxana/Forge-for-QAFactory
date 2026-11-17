# Универсальность — пачка 1: фабрика проходит все стадии, не застряв

кучка: `universality` | статус: ожидает | взял: — | ветка: — | MR: — | стенд: нужен

Правило готовности: пачка закрыта, когда каждый узел «принято», свидетели узлов — в журнале взявшего,
живые доказательства (FR-33) сделаны или переданы строкой в кучку «живые прогоны».

Решения владельца: слово владельца 17.11.2026 по плану U7 — «да»; развилки F-1…F-17 решены в шапке спеки `docs/tasks/specs/20261117-u7-pass-without-stuck-spec-r3.md` (указатель, не копия); F-5 открыта, ждёт слова владельца — от неё зависит только U1-11.
Порядок по общим файлам: `check_delivery.py`: узел U1-8 → узел U1-9; `s7_pretriage.py`, `test_s7_pretriage.py`, `test_check_delivery.py`: U1-8 → U1-9; `run_suite.py`: U1-5 → U1-9 (разные функции); `check_traceability.py`, `delivery-verdict-kinds.json`, `test_third_verdict.py`: U1-9 → U1-10; `planning_contract.py`, `test_question_branches.py`: U1-1 → U1-2 (после U1-8).
Скоуп свидетеля: по узлам — то, что печатает `scenario_walk.py --witness-for <owns>`; медленные файлы судит канон пачки; BATCH CANON на CI — координатор.
Общий бриф дизайнерам: спека `docs/tasks/specs/20261117-u7-pass-without-stuck-spec-r3.md` (§1 архитектура, §2 места, §6 потоки и шаблоны диспатча, §11 развилки); кодовые узлы уже написаны этой спекой, дизайнер не нужен; DoD узла — в её §6.

Пути «Пишет в»: пакета — от `ai-packages/qa-factory/`.

## Бриф

Что сделать: узлы ниже — потоки спеки `docs/tasks/specs/20261117-u7-pass-without-stuck-spec-r3.md` §6, по одному узлу на поток. Шаблон диспатча каждого — в §6 спеки; DoD узла — там же.
НЕ делать: поток 6 спеки (вопрос о стенде) — узел OF5-5 пачки `onboarding-forge/5`; правки других пачек; узел U1-11 до слова владельца по F-5.

## Узлы

Исполнитель «designer → builder → critic» — кодовый узел; «builder» — узел-документ. Статусы:
`ожидает` → `в работе` → `сдано` → `принято` / `отклонено`.

| Узел | Приоритет | Что | Исполнитель | Пишет в | Зависит от | Статус |
|---|---|---|---|---|---|---|
| U1-1 | П1 | Конфиг без объявленной поверхности вслух называется «не объявлено», неизвестная поверхность идёт по пути «роль пробует первой», строка стенда без адреса говорит, что принята как «внутри процесса». Спека `docs/tasks/specs/20261117-u7-pass-without-stuck-spec-r3.md` §6, поток 1 «surfaces and readiness» (пункты 1–3, 5, 6) | designer → builder → critic | `scripts/surfaces.py`, `references/surfaces.json`, `scripts/readiness.py`, `scripts/planning_contract.py`, `scripts/tests/test_readiness.py`, `scripts/tests/test_question_branches.py`, `design/architecture.md` (только ячейки осей 2 и 7 раздела A) | — | ожидает |
| U1-2 | П1 | Строка плана без исполнителя (`hands: none`) превращается в ручной кейс агента: агент пробует сам и записывает `unprepared` с тем, что пробовал. Спека `docs/tasks/specs/20261117-u7-pass-without-stuck-spec-r3.md` §6, узел 1b — пункт 4 потока 1 «surfaces and readiness» (`_row_of_nobody`) | designer → builder → critic | `scripts/planning_contract.py`, `scripts/tests/test_question_branches.py` | U1-8 (пункт 4 только после слияния 7a) | ожидает |
| U1-3 | П1 | Разведка онбординга спрашивает про продукт на устройстве или нативный, называет «драйвер, который знает фабрика», и говорит, что агент попробует сам, а человеку отдаст только то, чего не может. Спека `docs/tasks/specs/20261117-u7-pass-without-stuck-spec-r3.md` §6, поток 2 «onboarding discovery» | builder | `skills/qa-onboarding/phases/p1-discovery.md`, `skills/qa-onboarding/phases/p2-interview.md` | — | принято: 56addbf7 (t-1261) |
| U1-4 | П1 | Пин: отсутствующая возможность на S0 даёт вопрос `s0.readiness`, вызовов дирижёра 0; код 2 даёт отказ без Person. Спека `docs/tasks/specs/20261117-u7-pass-without-stuck-spec-r3.md` §6, поток 3 «S0 pin» | builder | `scripts/tests/test_no_move_seam_sites.py` | — | принято: 48fb860e (t-1260) |
| U1-5 | П1 | Текст пробы по коду называет дверь «красная песочница» раньше предложения про инструменты. Спека `docs/tasks/specs/20261117-u7-pass-without-stuck-spec-r3.md` §6, поток 4a «probe text» | builder | `scripts/probe_by_code.py`, `scripts/tests/test_probe_by_code.py` | RD1-24 (`rules-debt/1`) | ожидает |
| U1-6 | П1 | Недостающий запускатель с известной командой установки получает один ход дирижёра на все три дороги, затем один вопрос человеку; тихие возвраты проверки говорят вслух. Спека `docs/tasks/specs/20261117-u7-pass-without-stuck-spec-r3.md` §6, поток 5a «gate A» | designer → builder → critic | `scripts/gate_preflight.py` (`check_s5_executor`, `check_s5_toolchain`, `check_s5_dependencies`, `+executor_install`, `executor_turn_had`, `run`), `scripts/driver_gates.py`, `scripts/run_suite.py` (`refuse_missing_executor`), `references/halts.md` (строка `run_suite: executor_unavailable`), `skills/qa-story/phases/s5.md` (предложение на строке 144), `scripts/tests/test_gate_preflight.py`, `scripts/tests/fixtures/driver-layers.json`, `scripts/tests/fixtures/driver-exits/gates.json` | RD1-13, RD1-14 (`rules-debt/1`, тот же файл `gate_preflight.py`) | ожидает |
| U1-7 | П1 | План целиком из ручных кейсов закрывает S5 кодом с пустым манифестом и не требует свидетельства прогона под квитанцией этого закрытия. Спека `docs/tasks/specs/20261117-u7-pass-without-stuck-spec-r3.md` §6, поток 5b «S5 close» | designer → builder → critic | `scripts/driver_stage_s5.py` (`stage_S5`), `scripts/controller.py` (операция `code_only`, ключ `undisposed` в `stage_scope`), `scripts/driver_core.py` (строка `CODE_CLOSE_SITES`), `scripts/driver_dispatch.py` (комментарий на строках 47–50), `scripts/acceptance.py` (`run_witness_excused`), `scripts/check_witness.py` (`_excused` и правило манифеста), `scripts/validate_artifacts.py` (вызов исключения на строках 1731–1737), `scripts/tests/test_s5_window_leftovers.py`, `scripts/tests/test_controller_state.py`, `scripts/tests/test_check_witness.py`, `scripts/tests/fixtures/driver-exits/s5.json`, `design/controller-blocks.md` | — | ожидает |
| U1-8 | П1 | S7 принимает прогон `not_executed` законченного S6, если у роли есть что разобрать, и доставка не называет такой прогон `run_not_deliverable`; смешанная история со сломанной автоматической половиной сохраняет честное `no`. Спека `docs/tasks/specs/20261117-u7-pass-without-stuck-spec-r3.md` §6, поток 7a «S7 entry and its delivery twin» | designer → builder → critic | `scripts/s7_pretriage.py` (`+triageable_not_executed`), `scripts/driver_stage_s7.py` (`failures_to_triage`, вызов в `stage_S7`, комментарии на строках 14–16 и 87–93), `scripts/check_delivery.py` (`run_reasons`), `scripts/tests/test_s7_pretriage.py`, `scripts/tests/test_story_run_s7.py`, `scripts/tests/test_check_delivery.py` | — | ожидает |
| U1-9 | П1 | Каждый экземпляр прогона без отчёта становится целью разбора аналитика; доставка говорит `after_checks` с пунктом `run_unread` на экземпляр или краснотой аналитика. Спека `docs/tasks/specs/20261117-u7-pass-without-stuck-spec-r3.md` §6, поток 7b «the no-report half» | designer → builder → critic | `scripts/run_suite.py` (`build_run_block` и константа), `scripts/contract.py` (`triage_targets`, `triage_failures`), `scripts/s7_pretriage.py` (`triageable_not_executed`), `scripts/ledger.py` (`test_state`, `plan_row_state`, константа состояния), `scripts/check_traceability.py` (ветка разрыва результата), `references/delivery-verdict-kinds.json`, `agents/qa-failure-analyst.md` (один абзац), `design/architecture.md` (только ячейка оси 3 раздела A), `scripts/tests/test_s7_pretriage.py`, `scripts/tests/test_ledger.py`, `scripts/tests/test_third_verdict.py`, `scripts/tests/test_check_delivery.py` | U1-8; U1-6 (если обе открыты — общий файл `run_suite.py`) | ожидает |
| U1-10 | П1 | Непройденный ручной обход доходит до доставки отдельным пунктом `unprepared_walk` (`after_checks`), а не `chain_broken` `no`; покрытие по-прежнему не считается проверенным. Спека `docs/tasks/specs/20261117-u7-pass-without-stuck-spec-r3.md` §6, узел 7c (развилка F-16 (a), §11; список файлов — F-16, Lead пишет в диспатче) | designer → builder → critic | `scripts/check_traceability.py`, `references/delivery-verdict-kinds.json`, `scripts/tests/test_third_verdict.py` | U1-9 | ожидает |
| U1-11 | П1 | Текст исполнителя ручных прогонов говорит, что другой экземпляр стенда или устройства поднимается только действиями, которые проект разрешил; остальное уходит человеку с описанием попытки. Спека `docs/tasks/specs/20261117-u7-pass-without-stuck-spec-r3.md` §6, узел E7 «runner preparation text» | builder | `agents/qa-runner.md` | слово владельца по развилке F-5 | ожидает |

## Ход

Журнал передачи Lead пачки, новые записи в конец: `<дата время> — <что сделано, диспатчи t-nnn, хэши>`.

- 17.11.2026 — состояние потоков: U1-3 принято (56addbf7, t-1261), U1-4 принято (48fb860e, t-1260); в работе U1-1 (t-1263), U1-6 (t-1264), U1-7 (t-1265), U1-8 (t-1266); остальное ожидает. Статусы в таблице оставлены «ожидает», пока пачку не взяли (`piles.py check`), реальное состояние — здесь.
- 17.11.2026 — поток 6 спеки (вопрос о стенде, r10) в эту пачку не входит: это узел OF5-5 пачки `onboarding-forge/5`.

## Живые доказательства

| Что | Стенд / проект | Кто | Статус |
|---|---|---|---|
| L1: онбординг нативного проекта без известного драйвера записывает поверхность и говорит умолчание (спека r3 §7) | стенд | — | ждёт |
| L2: готовность и doctor печатают «не объявлено» или роль-первой слова; непройденный кейс обходит агент и записывает `unprepared` с тем, что пробовал; S7 разбирает его; вердикт доставки и его виды записаны (спека r3 §7) | стенд | — | ждёт |
| L3: неподтверждённый стенд с разрешённым ремонтом получает один ход дирижёра; недостающий запускатель с известной командой установки получает один; вопрос человеку — только после, один раз (спека r3 §7) | стенд | — | ждёт |
| L4: план из одних ручных кейсов проходит S5 кодом (пустой манифест, свидетельство не требуется) и S6, S7, S8 до вердикта доставки без видов `factory_record` и `run_not_deliverable` (спека r3 §7) | стенд | — | ждёт |
| L5: S0 со строкой стенда без адреса говорит умолчание (спека r3 §7) | стенд | — | ждёт |
| L6: прогон с `reporter: none`: аналитик разбирает каждый экземпляр по логу на S7; доставка говорит `after_checks` с одним пунктом `run_unread` на экземпляр или краснотой аналитика (спека r3 §7) | стенд | — | ждёт |
| E-7: второй экземпляр стенда или устройства поднимается только разрешёнными проектом действиями; строка ждёт слова владельца по F-5 (спека r3 §7) | стенд | — | ждёт |

## Остатки

