# Прогон без кода и с одной стороной — пачка 1: стороны, реестр допущений, ожидание кода, приход кода, старая версия

кучка: `pre-code` | статус: закрыта | взял: dev1, 11.11.2026 | ветка: `pile/pre-code/batch-1` | MR: `5498318` | стенд: нужен | приоритет: П2 | issue: https://git.example.com/dev1/yml-text-factory/-/work_items/72

Правило готовности: пачка закрыта, когда каждый узел «принято», свидетели узлов — в журнале взявшего,
живые доказательства (FR-33) сделаны или переданы строкой в кучку «живые прогоны».

Решения владельца: слово владельца 10.11.2026 — одна архитектура на три случая; контракт локаторов для разработчика не делаем; бага «не выполнено» у стори без кода нет, строка «ждёт кода»; гейт A в режиме «как раньше» показывает только расхождения и пробелы; постоянный факт о сторонах хранится в хранилище знаний (спека t-2142), не в конфиге; чужая подменённая сторона даёт вердикт «готово после проверок человеком»; вопрос «чья сторона» — один, при запуске; ждущая стори ждёт бессрочно и закрывается словом «перестать ждать»; пачка выпускается целиком.
очередь: project-knowledge/1 → pre-code/1 (`scripts/project_knowledge.py`, `scripts/guard_pre_tool.py`: PK0-1, PK0-8 → PC1-2; `docs/SIBLING_MAP.md` ось 34: PK0-6 → PC1-14)
очередь: project-knowledge/1 → pre-code/1
Порядок по общим файлам: `scripts/story_run.py`: PC1-3 → PC1-9 → PC1-12, PC1-2 — другие функции; `scripts/run_suite.py`: PC1-5 → PC1-7 → PC1-12; `scripts/contract.py`: PC1-1 → PC1-4, PC1-11, PC1-2 — разные функции; `references/question-prices.json`: PC1-3 → PC1-9; `skills/qa-story/phases/s5.md`: PC1-9 → PC1-10; `agents/qa-requirements-tester.md`: PC1-10 → PC1-11; `scripts/tests/test_human_reading.py`: PC1-9 → PC1-13; `scripts/controller.py`, `scripts/stage_guard.py`: только PC1-8, после окончания параллельной сессии `thinking-roles`.
Скоуп свидетеля: тестовые файлы, названные в строке узла §7 спеки (быстрые, до минуты каждый); `test_story_run_*`, `test_controller_*`, список медленных — только CI; канон пачки — пайплайн CI.
Общий бриф: узел исполняется по своей строке §7 спеки `docs/tasks/specs/t-2181-pre-code-and-one-side-runs.md` (файлы, функции, тесты, команда свидетеля — там); поведение — §2–§5, решения развилок — блок решений в начале спеки и §6. Спека ссылается на `controller.py` и `story_run.py` по именам функций: номера строк перемеряются перед диспатчем. Повышение храповика без строки в спеке — стоп и возврат.

## Бриф

Цель пачки — одна модель на три случая. Первый срез доказывает «кода нет» на стенде без хранилища знаний: PC1-1; затем параллельно PC1-3,
PC1-4, PC1-8; затем PC1-5; PC1-9; PC1-10; живое доказательство S-a. Второй срез: PC1-7 → PC1-6 (доказательство на подмене), PC1-2 (факты о
сторонах в реестре знаний; после PK0-1, PK0-8 и PC1-3), PC1-11 → PC1-12, PC1-13 (старая версия; PC1-11 можно вести рядом с первым срезом),
PC1-14 последним. Между срезами релиза нет. **До первого диспатча:** параллельная сессия `thinking-roles` закончила; каждая ссылка
`путь:строка` спеки перемерена по ветке; список «согласовать с сессией хранилища знаний» из спеки передан Lead кучки `project-knowledge`.

## Узлы

Статусы: `ожидает` → `в работе` → `сдано` → `принято` / `отклонено`.

| Узел | Приоритет | Что | Исполнитель | Пишет в | Зависит от | Статус |
|---|---|---|---|---|---|---|
| PC1-1 | П1 | Данные о сторонах и один читатель по записи стори: по умолчанию одна настоящая сторона, как сегодня. Спека §2.1, §7 PC1-1 | builder → critic | `references/side-realities.json`, `scripts/contract.py`, `scripts/stage_done.py`, `scripts/tests/test_story_sides.py` | — | принято |
| PC1-2 | П2 | Постоянные факты о сторонах в реестре знаний: три ключа, сравнение `exact`, проверка значения, `subjects`, команда `side`, закрытая от ролей. Спека §2.1, §7 PC1-2 | builder → critic | `scripts/project_knowledge.py`, `references/conductor-actions.json`, `scripts/guard_pre_tool.py`, `scripts/contract.py`, `scripts/story_run.py`, `scripts/tests/test_project_knowledge.py`, `scripts/tests/test_guard_project_knowledge.py`, `scripts/tests/test_story_sides.py` | PK0-1, PK0-8 (`project-knowledge`), PC1-1, PC1-3 | принято |
| PC1-3 | П1 | Запуск: флаги `--side`, `--reference`, ответ «код ещё не написан» в обоих вопросах-близнецах, текст без бага «не выполнено», вопрос «чья сторона». Спека §3.1, §7 PC1-3 | builder → critic | `scripts/story_run.py`, `references/question-prices.json`, `skills/qa-story/phases/s1.md`, `agents/qa-scout.md`, `scripts/tests/test_no_mr_entry.py` | PC1-1 | принято |
| PC1-4 | П1 | Поля манифеста автоматизации: реестр допущений `provisional[]`, стороны теста, «о чём проверка», вид записи прогона. Спека §2.2, §7 PC1-4 | builder → critic | `references/provisional-kinds.json`, `references/artifact-contract-automation.md`, `scripts/manifest_put.py`, `scripts/contract.py`, `scripts/manifest_from_tests.py`, `references/null-outcomes.json`, `design/state-exits.md`, `scripts/tests/test_provisional.py` | PC1-1 | принято |
| PC1-5 | П1 | Проверки выхода S5 (C1–C6), один читатель «тест ждёт кода», «тест собирается» как свидетель, исключение «все тесты ждут кода». Спека §1.3, §5, §7 PC1-5 | builder → critic | `scripts/acceptance.py`, `scripts/s5_precheck.py`, `scripts/window_record.py`, `scripts/run_suite.py`, `scripts/check_witness.py`, `scripts/tests/test_s5_precheck_sides.py`, `scripts/tests/test_check_witness.py` | PC1-4 | принято |
| PC1-7 | П2 | Отметка «какие стороны встретил прогон» на каждом блоке исполнения — автотеста и ручного прохода. Спека §2.3, §7 PC1-7 | builder → critic | `scripts/run_suite.py`, `scripts/manual_evidence.py`, `scripts/finalize_task.py`, `references/artifact-contract-run.md`, `agents/qa-runner.md`, `scripts/tests/test_proof_stamp.py` | PC1-5, PC1-1 | принято |
| PC1-6 | П2 | Леджер и вердикт: «зелёный на подмене» не проход, «ждёт кода», пункты перепрохода в отчёте. Спека §2.3, §2.4, §7 PC1-6 | builder → critic | `scripts/ledger.py`, `references/delivery-verdict-kinds.json`, `scripts/check_delivery.py`, `scripts/factory_dashboard.py`, `scripts/tests/test_sides_ledger.py` | PC1-7, PC1-4 | принято |
| PC1-8 | П1 | Контроллер и страж: стори ждёт кода, приход кода, «перестать ждать», новые слова доработки; ждущая стори не уходит в S6. Спека §2.4, §7 PC1-8 | builder → critic | `scripts/controller.py`, `scripts/stage_guard.py`, `scripts/archive_task.py`, `design/state-exits.md`, `scripts/tests/test_awaiting_state.py` | PC1-1 | принято |
| PC1-9 | П1 | Драйвер: стоп после S5 с пакетом «что написано и чего не хватает», дорога прихода кода после проверки свежести тикета. Спека §3.1, §3.2, §7 PC1-9 | builder → critic | `scripts/story_run.py`, `scripts/interim_packet.py`, `references/question-prices.json`, `skills/qa-story/phases/s5.md`, `scripts/audit_factory.py`, `scripts/tests/test_interim_packet.py`, `scripts/tests/test_story_run_arrival.py` | PC1-3, PC1-5, PC1-8 | принято |
| PC1-10 | П1 | Хартии автоматора, критика кода и тестировщика требований; бриф S5 со сторонами и бриф привязки. Спека §3, §7 PC1-10 | builder → critic | `agents/qa-automator.md`, `agents/qa-code-critic.md`, `agents/qa-requirements-tester.md`, `scripts/brief_pack.py`, `skills/qa-story/phases/s2.md`, `skills/qa-story/phases/s5.md` | PC1-5; `s5.md` после PC1-9 | принято |
| PC1-11 | П2 | Старая версия: форма снимка поведения, его писатель, оракул «прецедент» со ссылкой на снимок, колонка `parity`. Спека §3.3, §7 PC1-11 | builder → critic | `references/artifact-contract-reference.md`, `scripts/reference_snapshot.py`, `scripts/contract.py`, `references/vocabularies.md`, `agents/qa-requirements-tester.md`, `scripts/tests/test_reference_snapshot.py` | PC1-1; хартия после PC1-10 | принято |
| PC1-12 | П2 | Старая версия: проход раннером на S1, стенд-образец без проверки сборки, запрет гонять тесты стори по образцу. Спека §3.3, §7 PC1-12 | builder → critic | `references/stages.json`, `scripts/story_run.py`, `scripts/stand_identity.py`, `scripts/runtime_probe.py`, `scripts/run_suite.py`, `scripts/execution_request.py`, `references/role-commands.json` | PC1-9, PC1-7, PC1-11, PC1-8 | принято |
| PC1-13 | П2 | Гейт A для стори с образцом показывает расхождения, пробелы и одну строку «N поведений переносятся как есть». Спека §3.1 (4), §7 PC1-13 | builder → critic | `scripts/gate_brief.py`, `scripts/tests/test_gate_brief_and_retro.py`, `scripts/tests/test_human_reading.py` | PC1-11; `test_human_reading.py` после PC1-9 | принято |
| PC1-14 | П2 | Замеры (доля допущений, закрытых без правки; цена второй фазы), детекторы в архитектуре, члены оси 34, проверка калибровки. Спека §8, §7 PC1-14 | builder → critic | `scripts/report_facts.py`, `design/architecture.md`, `docs/SIBLING_MAP.md`, `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md` | PC1-6, PC1-9, PK0-6 (`project-knowledge`) | принято |

Пути узлов — от `ai-packages/qa-factory/`, кроме `docs/` и `PROCESS/`. Полный список файлов и функций узла — строка §7 спеки; при расхождении верна спека.

## Ход

Журнал передачи Lead пачки, новые записи в конец: `<дата время> — <что сделано, диспатчи t-nnn, хэши>`.

- 10.11.2026 — пачка открыта: спека t-2181 в третьей редакции (дизайнер t-2181, критик на план t-2186, правки t-2187; слово владельца по развилкам). Кода нет; старт — после окончания параллельной сессии.
- 11.11.2026 — все 14 узлов приняты: код слит в ветке эксперимента 11.11 по общему плану t-2277 (его §3.2 режет пачку на PC-1a…PC-10) и пришёл в `main` коммитом слияния `5498318`. Соответствие и свидетели (журнал сессии общего плана — бандл истории, `docs/tasks/compact-snapshots/journal-root-copy-2026-11-11.jsonl` ветки `exp-final`; в `main` этого файла нет): PC1-1 = PC-1a (t-2332, фикс t-2344, критик t-2339); PC1-2 = PC-1b (фикс t-2480, критик t-2475); PC1-3 = PC-2 (t-2347, фикс t-2378, критик t-2368); PC1-4 = PC-3 (t-2343, фикс t-2366, критик t-2356); PC1-5 = PC-4 (t-2357, фикс t-2382, критик t-2376); PC1-7 = PC-5a (t-2390, критик t-2401); PC1-6 = PC-5 (t-2402, критик t-2423); PC1-8 = PC-6 (t-2380, критик t-2369); PC1-9 = PC-7 (t-2384, фикс t-2403, критик t-2399); PC1-10 = PC-8 (t-2447, критик t-2465); PC1-11 = PC-9a (t-2406, критик t-2429); PC1-12 = PC-9b (фикс t-2524, критик t-2513); PC1-13 = PC-9c (t-2545, критик t-2549); PC1-14 = PC-10 (t-2478, фикс t-2497, критик t-2486). Статусы проставлены 11.11 при сверке бэклога с историей слияния. Три живых доказательства перенесены в `live-runs/2` (слово владельца 11.11.2026: живые прогоны пачку не держат); пачка закрыта.

## Живые доказательства

| Что | Стенд / проект | Кто | Статус |
|---|---|---|---|
| Кода нет: стори на фичу, которой в MyBooks нет, встаёт в ожидание с пакетом «чего не хватает»; фича сделана на ветке; повторный запуск с веткой доходит до вердикта, хотя бы одна строка допущений закрыта без правки | MyBooks | Lead пачки | перенос: live-runs/2 «Живые доказательства» \| обоснование: живые прогоны собираются в одну пачку и закрываются одним прогоном на несколько узлов, пачку они не держат \| подтвердил: владелец, 11.11.2026 |
| Одна сторона: UI-стори с замоканным API идёт до конца, вердикт «готово после проверок человеком», отчёт называет тесты для перепрохода; перепроход на настоящем бэкенде делает их зелёными | MyBooks | Lead пачки | перенос: live-runs/2 «Живые доказательства» \| обоснование: живые прогоны собираются в одну пачку и закрываются одним прогоном на несколько узлов, пачку они не держат \| подтвердил: владелец, 11.11.2026 |
| Как раньше: старый тег MyBooks вторым стендом-образцом; гейт A показывает только расхождения и пробелы | MyBooks + второй деплой (стенд — за владельцем) | Lead пачки | перенос: live-runs/2 «Живые доказательства» \| обоснование: живые прогоны собираются в одну пачку и закрываются одним прогоном на несколько узлов, пачку они не держат \| подтвердил: владелец, 11.11.2026 |

## Остатки
