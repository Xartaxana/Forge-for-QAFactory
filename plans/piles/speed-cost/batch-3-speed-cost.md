# Скорость и цена прогона — пачка 3: остатки и находки релиза 0.10.3 из прогона TP1-14857 (0.10.2) и класс валидаторов

кучка: `speed-cost` | статус: закрыта | взял: dev1, 27.10.2026 | ветка: `pile/speed-cost/batch-3` | MR: `9be91225` | стенд: частично (живые доказательства FB-4, FB-8) | приоритет: П2 | issue: —

очередь: speed-cost/1 → speed-cost/3
очередь: hotfix-12586/3 → speed-cost/3
очередь: conductor/1 → speed-cost/3
очередь: hotfix-12586/2 → speed-cost/3
очередь: onboarding-hooks/2 → speed-cost/3
очередь: speed-cost/3 → run-honesty/1
очередь: speed-cost/3 → hotfix-12586/4
очередь: speed-cost/3 → hotfix-12586/5
очередь: speed-cost/3 → hotfix-12586/7
очередь: speed-cost/3 → execution-probes/2

Открыта Lead 27.10.2026 по D-0044 (t-1362): `speed-cost/1` взята (dev1, 26.10.2026) и заморожена, узлы, которые не могут лечь в неё, и очередь находок идут сюда. Узлы режутся от головы ветки пачки 1 и сливаются после неё (общие горячие файлы `controller.py`, `story_step.py`, `story_run.py`: порядок по `очередь` и по функциям, D-0048).

Правило готовности: пачка закрыта, когда каждый узел «принято», свидетели узлов — в журнале взявшего, живые доказательства (FR-33) сделаны или переданы строкой в кучку «живые прогоны».

Решения владельца: слово владельца 27.10.2026 — FB-4 и FB-8 («правильная починка, в релиз») идут в 0.10.3; по FB-13 слово владельца — правила заведения багов верны и не меняются. Остальные развилки узлов решает Lead пачки.
Порядок по общим файлам: `controller.py`, `story_step.py`, `story_run.py`: SC1-14 → SC3-4 → SC3-6 (по функциям — D-0048). Скоуп свидетеля: у узла — тестовые файлы изменённых модулей и ключи его DoD (D-0056); полный канон, соседи, большие файлы, docker — интегратор один раз на пачку.

## Бриф

Цель: (1) класс валидаторов (VC): отказ роли перечисляет все проблемы и поля сообщаются до работы — спека `docs/tasks/specs/t-1355-validator-class-fields-and-all-problems.md`, три части, билдеры t-1358…t-1360 уже в работе; (2) прогон TP1-14857 на 0.10.2: FB-8 (проба рантайма краснит файлы вне приложения, у `content_mismatch` нет двери человека) — спека t-1350; FB-4 (остановленный диспатч продолжается своим агентом) — спека t-1351, после SC1-14; FB-9 (ручной блок ранера) — спека t-1361 пишется; FB-10 (квитанции пробы привязаны к хэшу файла) ждёт квитанций проекта (владелец просила 27.10); (3) очередь находок: хвосты FB-4, генератор `field_cards.py`, контракт отчёта FB-13, FB-6, остаток FB-3/FB-5, очередь t-1342, N-3. Отчёты проекта: `docs/tasks/specs/reviews/external-14857-0.10.2/QA-Factory-0.10.2-Defects-for-Dev1.md` и `QA-Factory-0.10.2-Marathon-Addendum-for-Dev1.md` (приоритеты по слову владельца: FB-8 П1, FB-3/FB-5 и FB-9 П1, остальное по отчётам и дашборду П2); находки для других кучек (N-1, N-2, A1 → `cost-dashboard`, A2 → `driver-controller`, A3 → `execution-probes`, N-4 → `onboarding-hooks`) лежат в их пачках. Дизайнеру: исходные данные каждого узла — его спека или находка и ревью, названные в строке.

## Узлы

Исполнитель «designer → builder → critic» — кодовый узел; «builder» — узел-документ. Статусы:
`ожидает` → `в работе` → `сдано` → `принято` / `отклонено`. Метки VC / FB-n в «Что» — имена частей спек, не B-id.

| Узел | Приоритет | Что | Исполнитель | Пишет в | Зависит от | Статус |
|---|---|---|---|---|---|---|
| SC3-1 | П2 | VC-N1 (t-1358): закрыт экземпляр класса — `context_bundle` v2 discovery, хук записи, карточка и устав скаута; отказ называет все проблемы и поля (спека t-1355 §3; свип t-1349) | designer → builder → critic (один критик на VC после схождения, R13-g) | `scripts/context_bundle.py`, `scripts/validate_artifacts.py (check_context_manifest_v0)`, `references/ahead-cards.json (cards.qa-scout)`, `scripts/tests/test_context_bundle.py` | — | принято (t-1358, 773b105b) |
| SC3-2 | П2 | VC-N2 (t-1359): сборщики в остальных местах первой ошибки, закрытые списки в сообщениях, поля сообщаются до работы (спека t-1355 §4) | designer → builder → critic | `scripts/detector_verdict.py (one_of)`, `scripts/manual_evidence.py`, `scripts/planning_contract.py`, `references/ahead-cards.json (qa-failure-analyst, qa-retro-analyst)`, их тесты | — | принято (t-1359, e7becee3) |
| SC3-3 | П2 | VC-N3 (t-1360): охранный тест класса `scripts/tests/test_validator_class.py` (спека t-1355 §5) | designer → builder → critic | `scripts/tests/test_validator_class.py`, `scripts/context_bundle.py (_closed)` | SC3-1, SC3-2 | принято (t-1360, 83458476; следы t-1402, t-1412, 9be91225) |
| SC3-4 | П1 | FB8-N1: данные, читатель и проба — файлы вне приложения (Makefile, `.gitleaks.toml`, docs) не сравниваются и не краснят `content_mismatch`; ключ `execution.non_runtime_files` (`also`, `except`) с умолчаниями из данных; строка `matched_not_shipped` (спека t-1350 §N1; FB-8 прогона 14857, P0) | designer → critic на план → builder → critic | `scripts/runtime_probe.py`, `references/`, `references/config-keys.json`, `scripts/story_run.py (Driver.build_outcome)`, их тесты, `changelog.d/` | SC1-14 слит; `очередь: SC1-14 -> FB-8 N1` | принято (t-1384, a42e9942, 6a43d929; слито в пачку b177eac8) |
| SC3-5 | П1 | FB8-N2: дверь человека для `content_mismatch` — слово `content_accepted`, привязка к содержимому, отказы называют `test as is` (спека t-1350 §N2; FB-8, критерий 5 проекта) | designer → critic на план → builder → critic | `scripts/runtime_probe.py`, `scripts/story_run.py`, `scripts/run_suite.py`, тексты отказов, их тесты, `changelog.d/` | SC3-4 | принято (t-1391, 68539227, фикс-раунд cbcbb0b3) |
| SC3-6 | П1 | FB4: остановленный диспатч, который продолжил его же агент, снова бежит — операция `resume`, `dispatch_life_key`, `story_step.py resume`, вызов из `Driver._act_resume_checkpoint`; `next` несёт команду `resume` (F-9 да) (спека t-1351; FB-4 прогона 14857) | designer → critic на план → builder → critic | `scripts/controller.py`, `scripts/story_step.py`, `scripts/story_run.py (Driver._act_resume_checkpoint)`, `skills/qa-story/phases/s1.md`, `references/judge.md`, `references/conductor.md`, `references/controller-api.md`, `design/state-exits.md`, `design/controller-blocks.md`, их тесты, `changelog.d/` | SC1-14 слит; `очередь: SC1-14 -> FB4` | принято (t-1389, 93d2c3d1, фикс-раунд b95781ab; слито в пачку 949fe46c) |
| SC3-7 | П1 | FB9: `story_step.py start --stage S6 --role qa-runner --execution-kind manual` передаёт `manual_case_ids`; отказ называет недостающую опцию; тест на 1 и 4 кейса (спека t-1361 пишется; FB-9 прогона 14857) | designer → builder → critic | `scripts/story_step.py (start)`, `scripts/controller.py (validate_manual_runner_block)`, их тесты | SC1-14 слит (общий `story_step.py`) | принято (t-1385, критик t-1393, 74646d4d; в ветке пачки 4ff0abee) |
| SC3-8 | П2 | FB10: идентичность функции теста прощает только ДОБАВЛЕННУЮ тестовую функцию (прочие изменения скелета — как сегодня «другие байты»); дверь перепробы устаревшей квитанции вне скоупа; метка «comment-only change» после добавления не врёт; спека t-1363 (критик на план t-1368, фикс-раунд принят); свидетельство — `docs/tasks/specs/reviews/external-14857-0.10.2/FB-10-evidence-README.md` | designer → critic на план → builder → critic | `scripts/execution_fingerprint.py (_skeleton, _test_gaps)`, `scripts/execution_request.py (+scope_refusal, +_admitted_outside, build_mine_request)`, `scripts/proof_level.py (reprobe_admitted, code_unchanged_words, words)`, `scripts/probe_debt.py (settle, _scope_word)`, `scripts/window_record.py (_comment_only)`, `references/verification-levels.json`, `skills/qa-story/phases/s5.md`, их тесты, `changelog.d/` | `очередь: SC1-14 -> FB10`; `очередь: hotfix-12586/3 -> FB10` | принято (t-1386, критик t-1395, 0d5ea390) |
| SC3-9 | П2 | FB-7: `gate_preflight` читает вывод collect в обоих форматах (дерево `<Function …>`) | designer → builder → critic | `scripts/gate_preflight.py`, `scripts/node_ids.py` | — | принято (SC1-12, speed-cost/1) |
| SC3-19 | П1 | Остаток FB-3 / FB-5: `p4-generate.md` и `p2-interview.md` — отказ 400/422 на входе есть правка конфига, не проблема стенда; (б) проба форм поля входа — по слову владельца (`findings/20261027-p4-generate-login-failed-vsegda-problema-stenda.md`; FR-50) | builder (а); designer (б) | `skills/qa-onboarding/phases/p4-generate.md`, `skills/qa-onboarding/phases/p2-interview.md`, их тесты | `p4-generate.md` у SC1-14: после слияния | принято (t-1378, 31af3834, ветка wt/sc3-fb35) |
| SC3-22 | П1 | N-1 в релиз 0.10.3 (слово владельца 27.10: «если починка не отдаляет релиз, то бери»): активность стори открывается на каждом ходе открытой задачи, `doctor` закрывается со своим скиллом, открытая через границу стадии активность — находка; один читатель цены (спека t-1366 пишется). Закрывает CD1-16 кучки `cost-dashboard` (`../cost-dashboard/findings/20261027-aktivnost-doctor-ne-zakryta-cena-istorii-polovina.md`; P18, FR-24) | designer → builder → critic | `ai-packages/qa-factory/scripts/` (функции — по спеке t-1366) | — | принято (t-1376, a093ad66, ветка wt/sc3-n1) |

## Ход

Журнал передачи Lead пачки, новые записи в конец: `<дата время> — <что сделано, диспатчи t-nnn, хэши>`.

- 27.10 — пачка открыта Lead по D-0044 (t-1362): узлы, которые не лягут в замороженную `speed-cost/1`, и очередь находок релиза 0.10.3. SC3-1…SC3-3 — билдеры t-1358…t-1360 (в работе), SC3-4/5 — спека t-1350, SC3-6 — t-1351, SC3-7 — спека t-1361 пишется.
- 27.10 14:0x — Lead: квитанции проекта пришли (FB-10) → SC3-8 спека t-1363 пишется; SC3-19 расширен до полного узла FB-3/5 по сверке t-1364 (критерий 1 не выполнен; проба сообщает принятую пару, онбординг пишет её в конфиг — решение Lead, вопрос (б) находки закрыт так) → спека t-1365 пишется; SC3-22 N-1 добавлен по слову владельца. SC3-1 (VC N1) сдан и принят t-1358 (773b105b); SC3-7 спека t-1361 готова, критик на план t-1367.

- 27.10 15:1x — SC3-22 (N-1) принят t-1376: 7afe4c72 + фикс-раунд a093ad66 по критику t-1377; находки CD1-19…23 в кучке `cost-dashboard`. SC3-2 принят t-1359 (e7becee3).
- 27.10 15:4x — очередь держится полной (слово владельца): SC3-4 t-1384, SC3-7 t-1385, SC3-8 t-1386 режутся от головы SC1-14 6c159a2a, параллельно фикс-раундам SC1-14 X/Y по D-0048 (функции не пересекаются); SC3-8 сначала сливает `pile/hotfix-12586/batch-3`. SC3-6 (FB-4) ждёт фикс X: F-3 о продолжении агента. SC3-19 принят t-1378 (31af3834).
- 28.10 — закрытие по слову владельца 28.10.2026: статусы сверены (разведка t-1551), хвосты перенесены (t-1554). SC3-3, SC3-4, SC3-5, SC3-6 приняты (9be91225, a42e9942, 68539227, 93d2c3d1); два живых доказательства — live-runs/1 LR1-16, LR1-17.

## Живые доказательства

| Что | Стенд / проект | Кто | Статус |
|---|---|---|---|
| FB-4 (SC3-6), путь навыка: S1 с источником, ответ на ревью, `story_step.py resume`, SendMessage, `finish` с кодом 0, без `S1-qa-scout-2`; путь драйвера: остановленный диспатч с ожидающими словами продолжен в своей сессии и принят | `testproject1-dev-010` / копия проекта | взявший | перенос: live-runs/1 LR1-16 \| обоснование: живой прогон на релизе 0.10.5 (повтор TP1-12586 на testproject1-dev-010), владелец гоняет после релиза \| подтвердил: владелец, 28.10.2026 |
| FB-8 (SC3-4, SC3-5): проба рантайма на диффе с Makefile даёт `matched` и список «не сравнивалось»; недостающий файл приложения — `mismatched`; дверь человека для `content_mismatch` | `testproject1-dev-010` / копия проекта 14857 | взявший | перенос: live-runs/1 LR1-17 \| обоснование: живой прогон на релизе 0.10.5 (копия проекта 14857 на testproject1-dev-010), владелец гоняет после релиза \| подтвердил: владелец, 28.10.2026 |

## Остатки
