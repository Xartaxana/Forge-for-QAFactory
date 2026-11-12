# Думающие роли — пачка 3: автоматизация и ручной проход идут параллельно (окна S5 и три ходока)

кучка: `thinking-roles` | статус: ожидает | взял: — | ветка: — | MR: — | стенд: нужен (только живое доказательство) | приоритет: П1

Правило готовности: пачка закрыта, когда каждый узел «принято», свидетели узлов — в журнале взявшего, живые доказательства (FR-33) сделаны или переданы строкой в кучку «живые прогоны».

Решения владельца: «Оба варианта идут очень долго, а должны идти час — время уменьшить в разы»; ходоков по умолчанию — «пусть будет 3»; способ получения учёток — факт проекта, спрашивается один раз (владелец, 05.11.2026). Полные слова — в находке.
Порядок по общим файлам: `scripts/story_run.py`: TR3-2 → TR3-17 → TR3-6 → TR3-18 → TR3-9 → TR3-10 (TR3-13 и TR3-5 — другие функции); `scripts/controller.py`: TR3-4 → TR3-5 → TR3-15; `scripts/probe_debt.py`: TR3-11 → TR3-15; `scripts/brief_pack.py`: TR3-5 → TR3-15; `scripts/guard_pre_tool.py`: TR3-5, TR3-14, TR3-16 — разные функции; `scripts/walk_session.py`: TR3-7 → TR3-10; `scripts/manual_capture.py`: TR3-8 → TR3-10.
Скоуп свидетеля: по разделу 6 спеки t-1937 и узлам §4 «SLICE 2» спеки t-1957; медленные `test_story_run_*`, `test_controller_*` — только CI; канон пачки — пайплайн CI.
Общий бриф дизайнерам: спека t-1937 — черновик, перед первым пишущим узлом один проход критика на план (ядро контроллера); развилки закрыты рекомендациями — список в находке `findings/20261106-parallelnost-okna-s5-i-hodoki.md`. Ручная половина (TR3-7…TR3-10) стартует после узлов TR1-1, TR1-2, TR1-4 пачки 1.

## Бриф

Цель пачки: окна автоматизации S5 идут несколькими сразу, ручной проход — тремя ходоками. Начать с TR3-1 (разведка) и одного прохода критика на план спеки t-1937; одновременно можно вести TR3-2, TR3-3, TR3-7, TR3-8, TR3-11. Узлы TR3-1…TR3-6 и TR3-11 исполняются по разделу 6 спеки `docs/tasks/specs/t-1937-s5-parallel-windows.md`, узлы TR3-7…TR3-10 — по §4 «SLICE 2» спеки `docs/tasks/specs/t-1957-fast-manual-walker.md`; соответствие узлов — в находке.

## Узлы

Статусы: `ожидает` → `в работе` → `сдано` → `принято` / `отклонено`.

| Узел | Приоритет | Что | Исполнитель | Пишет в | Зависит от | Статус |
|---|---|---|---|---|---|---|
| TR3-1 | П1 | Разведка: все места «один работающий диспатч» и все файлы, которые пишет окно S5 (N-P1-0 спеки t-1937). Находка `findings/20261106-parallelnost-okna-s5-i-hodoki.md` | scout | `docs/tasks/specs/reports/t-1937-scout-s5-shared-writers.md` | — | принято |
| TR3-2 | П1 | Носитель времени переходов и ожидание без тишины; первым трогает `launch` (N-P2-1) | builder | `scripts/story_run.py`, `scripts/driver_timing.py`, `scripts/dispatch_liveness.py`, `scripts/story_step.py`, `scripts/audit_factory.py` | — | принято |
| TR3-3 | П1 | Ключ конфига `dispatch.parallel_windows` с умолчанием 3: параллельно по умолчанию, последовательно только если иначе нельзя (N-P1-3; слово владельца 06.11.2026) | builder | `references/templates/config.json`, `references/config-keys.json`, `scripts/config_contract.py` | — | принято |
| TR3-4 | П1 | Контроллер допускает несколько работающих диспатчей стадии (N-P1-1c; ядро) | builder → critic | `scripts/controller.py`, `scripts/story_step.py`, `references/state-exits.md` | TR3-3 | принято |
| TR3-5 | П1 | У каждого окна свой файл находок критика (N-P1-2a) | builder → critic | `agents/qa-code-critic.md`, `handoffs/s5-critic-to-automator.yaml`, `references/artifact-writers.json`, `references/stages.json`, `scripts/handoff_check.py`, `scripts/brief_pack.py`, `scripts/ledger.py`, `scripts/guard_pre_tool.py`, `scripts/story_run.py` | TR3-13 | принято |
| TR3-6 | П1 | Планировщик окон S5 в драйвере: окна, не делящие файлы, идут одновременно; вопрос человеку — после того как окна доработали; здесь начинает действовать умолчание 3 (N-P1-4b) | builder → critic | `scripts/story_run.py`, `scripts/exit_gate.py`, `references/state-exits.md` | TR3-4, TR3-5, TR3-12, TR3-14, TR3-15, TR3-16, TR3-17 | принято |
| TR3-7 | П1 | Общий режим аренды стенда `walk` и все читатели файла аренды (N1b спеки t-1957) | builder → critic | `scripts/stand_lease.py`, `scripts/walk_session.py` | — | принято |
| TR3-8 | П1 | Шаг `fill-new-account` и замок на запись созданных учёток (N1c) | builder → critic | `scripts/manual_capture.py`, `references/manual-capture-steps.json` | — | принято |
| TR3-9 | П1 | Параллельные дорожки ручного прохода на планировщике окон, по умолчанию 3 ходока; `walkers: 1` — как сейчас (N5p) | builder → critic | `scripts/story_run.py` | TR3-6, TR3-7 | сдано |
| TR3-10 | П1 | Способ получения учёток и данных проекта спрашивается один раз и хранится целиком; каждому ходоку свои данные; слово роли для неподтверждённых учёток и строка отчёта о них (F11, F15 критика t-2060) (N8) | builder → critic | `scripts/story_run.py`, `scripts/manual_capture.py`, `scripts/walk_session.py`, `scripts/project_decisions.py`, `scripts/report_facts.py` | TR3-8, TR3-9 | принято |
| TR3-11 | П2 | Расчёт долга проб на входе окна — добавочный, с памятью отказов (N-P2-2; ускоряет каждый переход, к параллельности не обязателен) | builder | `scripts/probe_debt.py`, `scripts/story_step.py` | — | принято |
| TR3-12 | П1 | Вопрос интервью про `dispatch.parallel_windows`, закрепление в заготовке теста (N-P1-3r) | builder | `skills/qa-onboarding/phases/p2-interview.md`, `scripts/tests/story_run_common.py` | TR3-3 | принято |
| TR3-13 | П1 | Замер наследования окружения хуками; один читатель «какой я диспатч»; читатели выхода S5 (N-P1-1a) | builder → critic | `scripts/dispatch_identity.py`, `scripts/story_step.py`, `scripts/story_run.py` | TR3-12 | принято |
| TR3-14 | П1 | Читатели в хуках идут через один читатель личности диспатча (N-P1-1b) | builder → critic | `scripts/guard_pre_tool.py`, `scripts/hooklib.py` | TR3-13 | принято |
| TR3-15 | П1 | Долг проб, память, советы, заметки, судья и размер — на диспатч; settle не трогает работающее окно (N-P1-2b) | builder → critic | `scripts/probe_debt.py`, `scripts/story_step.py`, `scripts/brief_pack.py`, `scripts/exit_gate.py`, `scripts/judge_code.py`, `scripts/sizing.py`, `scripts/controller.py`, `agents/qa-automator.md`, `agents/qa-code-critic.md`, `skills/qa-story/phases/s5.md` | TR3-11, TR3-5, TR3-13 | принято |
| TR3-16 | П1 | Тестовый файл принадлежит окну с первой записи; другое окно получает отказ с дверью «новый файл рядом» (N-P1-5) | builder → critic | `scripts/window_files.py`, `scripts/guard_pre_tool.py`, `agents/qa-automator.md`, `agents/qa-code-critic.md`, `references/state-exits.md` | TR3-13 | принято |
| TR3-17 | П1 | Запись цепочки: значения драйвера по потокам, поток вывода с меткой окна, без смены поведения (N-P1-4a) | builder → critic | `scripts/story_run.py` | TR3-2 | принято |
| TR3-18 | П1 | Набор равносильности и швы при умолчании 3 (N-P1-4c) | builder → critic | `scripts/tests/test_story_run_s5_parallel.py`, `scripts/story_run.py` | TR3-6 | принято |

## Ход

Журнал передачи Lead пачки, новые записи в конец: `<дата время> — <что сделано, диспатчи t-nnn, хэши>`.

- 06.11.2026 — пачка открыта по вопросу владельца 06.11.2026 «сколько узлов надо, чтобы сделать автоматизацию и ручной проход кейсов параллельным»; узлы — из спек t-1937 (раздел 6) и t-1957 (§4, второй срез).
- 12.11.2026 — слово владельца: живые доказательства перенесены в live-runs/2 (t-097).
- 12.11.2026 — TR3-9: критик t-096 (`docs/tasks/specs/reviews/t-096-tr3-9-code.md`) — годится с правками. Сделано раундом t-102 (`7e9f319`): допуск дорожки S6 не закрывает работающие соседние (F1), два теста «по очереди» могут покраснеть (F4), фрагмент changelog (F3); строка оси 5 и ось 33 карты симметрий (F2, Lead). Открыто, узел остаётся «сдано»: (B1) доказательство «один ходок = дорога до дорожек» — карантинный `test_story_run_s6_w1_frozen.py`, красный 4/6 по двум причинам, обе — устаревший снимок, код прав (в промпте новая строка `work/first-look.yaml`; маска подписи `budget B`); нужен пересъём снимка — правка карантинного файла, слово владельца; (F5) известный остаток C.5: `finalize_task`, запущенный ходоком, идёт вне замка драйвера, отчёт может ненадолго не показать блок одной дорожки, закрытие S6 сводит заново; (канон 43208727152) `test_walk_lanes_parallel` «the crashed lane's dispatch stays running for the re-entry» один раз красный на CI, локально зелёный — гонка потоков, разобрать (FR-31); очередь Q1–Q3 критика — завести находкой в пачку 6.

## Живые доказательства

| Что | Стенд / проект | Кто | Статус |
|---|---|---|---|
| перегон S5 стори LOCAL-1 с тремя окнами: время стадии против 4:13 плеча B | MyBooks | — | перенос: live-runs/2 «Живые доказательства» \| обоснование: живые прогоны не держат пачку (PROJECT.md, «Командная работа» п. 9) \| подтвердил: владелец, 12.11.2026 |
| обход 23 карточек тремя ходоками: время набора против 80 минут одного ходока и 21 минуты простого агента | MyBooks, копия `tr-walk` | — | перенос: live-runs/2 «Живые доказательства» \| обоснование: живые прогоны не держат пачку (PROJECT.md, «Командная работа» п. 9) \| подтвердил: владелец, 12.11.2026 |

## Остатки
