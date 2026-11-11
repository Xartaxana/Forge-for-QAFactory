# Думающие роли — пачка 4: остатки ревью критиков и скаутов (формы, замки, повторы, реестр тестов)

кучка: `thinking-roles` | статус: ожидает | взял: — | ветка: — | MR: — | стенд: не нужен | приоритет: П2

Правило готовности: пачка закрыта, когда каждый узел «принято», свидетели узлов — в журнале взявшего, живые доказательства (FR-33) не требуются.

Решения владельца: нет; узлы — наблюдения критиков (`docs/tasks/specs/reviews/t-2053`, `t-2055`, `t-2060`) и скаута (`docs/tasks/specs/reports/t-2036-tr1-9-triage.md`), направление только названо.
Порядок по общим файлам: `scripts/story_run.py`: TR4-3; `scripts/controller.py`: TR4-3 → TR4-7 (разные функции); `scripts/manual_capture.py`: TR4-2 → TR4-9; `scripts/stand_lease.py`: TR4-2. TR4-3, TR4-8, TR4-9 исполнимы только после слияния веток TR1-1, TR1-4, TR1-9 (функций на основе `guard/t-2065` нет).
Скоуп свидетеля: тестовый файл каждого своего пути (до минуты); медленные `test_story_run_*`, `test_controller_*` — только CI; канон пачки — пайплайн CI.
Общий бриф: узел исполняется по разделу со своим id в находке.

## Бриф

Цель пачки: закрыть то, что критики и скаут записали строками очереди, чтобы остатки не лежали вне пачек. Начать с TR4-4 и TR4-5 (быстрые, не делят файлы) и TR4-1. Строки очереди, которые уже закрыты или имеют владельца, в пачку не входят: TR3-15 (`settle` длиннее 60 строк), узел N8 = TR3-10 (`fill-new-account` в местах слова входа), `_running_verdict` (есть в `scripts/controller.py:2350`), `test_walk_charter.py` с `main` (есть, строка 121).

## Узлы

Статусы: `ожидает` → `в работе` → `сдано` → `принято` / `отклонено`.

| Узел | Приоритет | Что | Исполнитель | Пишет в | Зависит от | Статус |
|---|---|---|---|---|---|---|
| TR4-1 | П1 | Бриф критика/аналитика стадии несёт путь строки просмотренного диспатча автора; форма без него — отказ с дверью. Находка `findings/20261106-forma-kritika-ne-nazyvaet-prosmotrennyj-dispatch.md` | builder → critic | `scripts/stage_done.py`, `scripts/brief_pack.py`, шаблон формы критика стадии, `scripts/tests/` | — | принято |
| TR4-2 | П2 | Один публичный помощник замка файла с таймаутом вместо девяти копий. Находка `findings/20261106-kopii-zamka-fajla-v-pakete.md` | designer → builder → critic | новый модуль замка, `scripts/stand_lease.py`, `scripts/stand_identity.py`, `scripts/execution_scheduler.py`, `scripts/case_versions.py`, `scripts/event_store.py`, `scripts/manual_capture.py` и остальные копии из перечня спеки | — | принято |
| TR4-3 | П2 | `refuse_case(plan, case, reason, door, by)` и один помощник id строки диспатча. Находка `findings/20261106-povtor-zapisi-otkaza-refuse-case.md` | builder | `scripts/story_run.py`, `scripts/controller.py`, `scripts/tests/` | слияние TR1-4, TR1-9 | принято |
| TR4-4 | П2 | Строка `TEST_TIMEOUTS` 600 для `test_exit_limit_halt_answered.py`; три файла в `slow_tests.json` после канона; разбор, почему файл идёт 238 с. Находка `findings/20261106-medlennye-testy-v-spisok-posle-kanona.md` | builder | `scripts/selftest.py`, `scripts/slow_tests.json` | канон CI пачки | принято |
| TR4-5 | П2 | Фикстура `test_guard_write_owners.py` не берёт `<case>` именем каталога. Находка `findings/20261106-test-guard-write-owners-case-kak-imya-kataloga.md` | builder | `scripts/tests/test_guard_write_owners.py` | — | принято |
| TR4-6 | П2 | `driver_timing` в `B_SCRIPTS`, `CLI_SCRIPTS`, `plans/features.json`. Находка `findings/20261106-novyj-skript-ne-zapisan-v-perechnyah.md` | builder | `scripts/audit_factory.py`, `scripts/tests/test_task_root_parsers.py`, `plans/features.json` | слияние TR3-2 | принято |
| TR4-7 | П2 | Отказы «checkpoint active work» читают живость одним помощником и называют держащий диспатч. Находка `findings/20261106-stroki-running-bez-zhivosti-v-kontrollere.md` | builder → critic | `scripts/controller.py`, `scripts/execution_request.py`, `scripts/tests/test_controller_state.py` | слияние TR1-9 | принято |
| TR4-8 | П3 | Настоящий тест входа вместо закрепления текста «проверка пробела до регистрации диспатча». Находка `findings/20261106-test-prikovan-k-tekstu-a-ne-k-povedeniyu.md` | builder | файл теста `test_the_gap_check_stands_before_the_dispatch_is_registered` (найти по имени) | слияние TR1-4 | принято |
| TR4-9 | П2 | Цепочка ввода: сброс при смене актора и `same_field` для написания селектора. Находка `findings/20261106-vvod-tsepochka-po-tekstu-selektora.md` | builder → critic | `scripts/walk_session.py`, `scripts/manual_capture.py`, `scripts/tests/` | слияние TR1-1 | принято |
| TR4-10 | П1 | Окна S5, остатки критика t-2121 (решения Lead — `docs/tasks/handoffs/20261110-lead-window-acceptance.md`, раздел 3, строки Q1–Q5): (1) захваты файлов отпускаются в момент, когда S5 закрыт, какой бы дорогой он ни закрылся; тест: S5 закрыт ответом человека `debt` на гейте, после него доработка автоматора не получает отказа «until that window closes»; (2) окно, чей последний диспатч `returned_unaccepted`, считается открытым в `s5_open_windows`; тест — сценарий критика: критик принял с `mechanical`, доработка автора вернулась непринятой, другое окно S5 не закрывает; (3) цепочка, ждущая в `session_gate`, не запускает сессию после начала слива; тест; (4) строка о владении файлами даётся автоматору при N != 1 на обоих телах (`s5_auto_extra(..., chain=False)` тоже); тест на текст брифа; (5) состояние «стадия `pending` рядом с остановленным окном» закреплено одним тестом и строкой `design/state-exits.md`, поведение не меняется | builder → critic | `scripts/story_run.py` (`s5_open_windows`, `s5_release*`, `session_gate`, `s5_auto_extra`), `scripts/window_files.py`, `design/state-exits.md`, `scripts/tests/test_story_run_s5_parallel.py`, `scripts/tests/test_guard_window_files.py` | TR3-9 (общий `story_run.py`: после него) | принято |
| TR4-11 | П2 | Мелкие остатки окон и census (тот же файл решений, раздел 3): (1) драйвер по Ctrl-C пишет одну запись «остановлен человеком» (кто: person, когда) в состояние стори, `collect_stall` K3 читает её и отличает остановку от смерти драйвера, на обеих дорогах; тест на K3 с записью и без; (2) свои дописыватели jsonl в `story_run.py` (`_append_jsonl` и прямые) идут через `hooklib.append_jsonl_line` (ось 29 карты); тест оси; (3) слепое пятно census — подкласс `ValueError` / `StateConflict` невидим для `refusal_registry.sites` — напечатано в строке итогов `test_judgment_census.py` и в `about` файла census; сканер не расширяется; (4) правки текста: changelog «31.2 s» — расчётное, не измеренное (t-2095 N1), `s5_precheck.py` «a held name» (N2) | builder | `scripts/story_run.py` (`_interrupt_chains`, `_append_jsonl`), `scripts/collect_stall.py`, `scripts/tests/test_collect_stall.py`, `scripts/tests/test_judgment_census.py`, `scripts/tests/fixtures/judgment-census.json` (`about`), `scripts/s5_precheck.py`, `changelog.d/` | TR4-10 (общий `story_run.py`) | принято |
| TR4-12 | П2 | Мелкие остатки ревью 10.11: `role_stops` по id диспатча, префилл форм S7/S8, `test_brief_pack_sd_head.py` в каноне, быстрая фикстура `brief_pack.build()`, `stand_lease` при занятом замке. Находка `findings/20261110-melkie-ostatki-revyu-10-11.md` | builder | `scripts/dispatch_liveness.py`, `scripts/brief_pack.py`, шаблоны форм S7/S8, `scripts/stand_lease.py`, `scripts/tests/` | слияние TR4-1, TR4-2 (часть A) | принято |
| TR4-13 | П1 | Окно S5, чей последний раунд — принятый раунд автора, открыто в `s5_open_windows`, `todo` читает его оттуда, ход — «критик просматривает»; четыре теста (а)–(г). Находка `findings/20261110-s5-okno-posle-prinyatogo-avtorskogo-raunda-nevidimo.md` | builder → critic | `scripts/story_run.py`, `scripts/tests/test_s5_window_leftovers.py` | — | принято |
| TR4-14 | П2 | Один сборщик действия `resolve_return` в `scripts/controller.py`, все места `story_run.py` зовут его; один тест полей пакета, `test_driver_layers.py` держит вызывающих. Находка `findings/20261110-odin-sborshchik-resolve-return.md` | builder | `scripts/controller.py`, `scripts/story_run.py`, `scripts/tests/` | слияние TR4-10, TR4-13 | ожидает |
| TR4-16 | П3 | Остатки ревью TR3-10 D: одно чтение первого стенда и публичные имена, ключи пулов через `fold_kind`, `walk_assign_step` на три шага, возврат в S6 после ответа `added`. Находка `findings/20261111-uchyotki-obhodov-ostatki-revyu.md` | builder | `scripts/walk_pool.py`, `scripts/project_decisions.py`, `scripts/guard_secrets.py`, `scripts/gate_preflight.py`, `scripts/config_contract.py`, `scripts/story_run.py` (`take_answer`, `walk_gap_role`, `_answer_walk_supply`, `walk_assign_step`), `scripts/tests/` | TR3-10 | ожидает |
| TR4-17 | П3 | Остатки цепочки проб t-2064: одиннадцать пунктов находки `findings/20261111-proby-ostatki-cepochki.md` | builder | `scripts/manifest_put.py`, `scripts/proof_level.py`, `scripts/probe_by_code.py`, `scripts/planning_contract.py`, `scripts/check_witness.py`, `scripts/tests/test_probe_by_code_languages.py`, `scripts/tests/test_brief_pack.py` | слияние цепочки проб (TR2-14) | ожидает |
| TR4-15 | П2 | Необязательное поле черновика `observation` (id наблюдения без закреплённого кейса): в контракте, в срезе для аналитика (срез сгенерирован: пересобрать `python -B scripts/contract_slices.py --write`, руками не править), в `place_of_draft`; `validate_artifacts.py` не меняется; четыре теста (а)–(г). Находка `findings/20261110-tr1-11-chernovik-nablyudeniya-klyuch-svyazi.md` | builder → critic | `references/artifact-contract-run.md`, `references/slices/qa-failure-analyst/artifact-contract-run.md` (генерируется), `scripts/place_answers.py`, `scripts/tests/test_place_answers.py` | слияние TR1-11 | ожидает |

## Ход

Журнал передачи Lead пачки, новые записи в конец: `<дата время> — <что сделано, диспатчи t-nnn, хэши>`.

- 06.11.2026 — пачка открыта диспатчем t-2083: находки из очереди ревью t-2053, t-2055, t-2060 и разбора t-2036 (девять узлов, девять находок по классам).

## Живые доказательства

Живых доказательств нет: узлы не меняют поведение роли на стенде.

## Остатки
