# Честность прогона — пачка 2: предикат «наследная идентичность» не берёт запись с точным `instance_id`

кучка: `run-honesty` | статус: закрыта | взял: — | ветка: — | MR: `855d4e5c` | стенд: не нужен | приоритет: П3 | issue: https://git.example.com/dev1/yml-text-factory/-/work_items/52

Правило готовности: пачка закрыта, когда каждый узел «принято», свидетели узлов — в журнале взявшего, живые доказательства (FR-33) сделаны или переданы строкой в кучку «живые прогоны».

Решения владельца: нет (слово владельца не требуется: находка `findings/20261027-legacy-identity-ignoriruet-instance-id.md`, «Решение владельца нужно: нет»).
Порядок по общим файлам: `contract.py`: RH2-1 единственный писатель в этой пачке; пачка 1 (`ledger.py`, `check_coverage.py`) `contract.py` по узлам не пишет, кроме возможной правки RH1-1 по вердикту критика — тогда `очередь: run-honesty/1 → run-honesty/2` строкой шапки при взятии.
Скоуп свидетеля: у узла — `scripts/tests/test_case_id_form_sites.py` и ключи DoD; полный канон — интегратор один раз на пачку (D-0056).

## Бриф

Цель: запись с точным `instance_id` не присоединяется к строке чужого теста по кейсу (RH2-1, builder → critic); сверх того пачка собирает остатки узлов пачки 1 (RH2-2…RH2-7, строки таблицы ниже; бриф узлов — находки в колонке «Что»). Читать: находку узла и вердикт `docs/tasks/specs/reviews/t-1416-rh1-1-k11-verdict.md`, раздел «Side observation»; `design/factory-rules.md` (FR-58, FR-59), `design/architecture.md` (AR-13, AR-28).

## Узлы

Исполнитель «designer → builder → critic» — кодовый узел; «builder» — узел-документ. Статусы:
`ожидает` → `в работе` → `сдано` → `принято` / `отклонено`.

| Узел | Приоритет | Что | Исполнитель | Пишет в | Зависит от | Статус |
|---|---|---|---|---|---|---|
| RH2-1 | П3 | `contract.legacy_identity_is_the_case` игнорирует `instance_id`: запись с точным id и маркером = кейсу присоединяется к строке чужого теста по кейсу (зонд критика: `passed_green`). Предикат требует отсутствия `instance_id` (или называет причину, почему нет); счётчик-ключ в тесте (`findings/20261027-legacy-identity-ignoriruet-instance-id.md`; FR-58, FR-59, AR-13, AR-28). Дизайнер не нужен: спека в находке | builder → critic | `scripts/contract.py (legacy_identity_is_the_case)`, `scripts/tests/test_case_id_form_sites.py` | RH1-1 (вердикт критика по K11 и та же область `test_case_id_form_sites.py`) | закрыта: перенесено 01.11.2026 → execution-report/2 |
| RH2-2 | П2 | Актуальность ревью при доставке после правки вне скоупа (бывшая половина `review_stale`, t-1363 R7, E8 RH1-9): вычисляемое чтение при доставке через предикат «тот же тест» (вариант C, предложение; B отклонён — второй носитель, AR-14), неподтверждённое ревью — причина доставки, не пропуск (`findings/20261028-aktualnost-revyu-pri-dostavke-posle-pravki-vne-skoupa-e8.md`; FR-41, FR-58, FR-59, AR-22, AR-28) | designer → builder → critic | `scripts/check_delivery.py`, `scripts/proof_level.py` (чтение), `scripts/tests/` (имена — проверить) | RH1-9 | закрыта: перенесено 01.11.2026 → execution-report/1 |
| RH2-3 | П3 | Принятый риск F5: перенос файла плюс легаси-носитель без идентичности читается `raw` (решение Lead пачки 27.10.2026); запись риска с владельцем, закрытие — подтверждением Lead, что докстринг `same_test` и ключ K-B на месте; код не меняется (`findings/20261028-perenos-fajla-i-legacy-nositel-prinyatyj-risk-f5.md`; FR-41, FR-59, AR-28) | Lead пачки | — (проверка `scripts/proof_level.py`, `scripts/tests/test_proof_level.py`) | RH1-9 | принято: 8fdf9550 |
| RH2-4 | П3 | Остаток AR-13 после RH1-9 (F6): сырые sha файла в `probe_by_code` (:2097, :2227, :2467, :2648), `red_sandbox` (:830), `window_record.probe_gap_block` (:613), путевые близнецы (`execution_request._same_file`, `probe_by_code._same_file`, `sizing._same_path`, `driver_trace._same_path`), `_split_node`, множество `str()` в `run_history._job_contract` — перевод на единый предикат или названная причина; правка осей 7 и 25 `SIBLING_MAP` и перечня K-C — Lead (`findings/20261028-bajtovye-sravneniya-ostalis-v-probe-by-code-red-sandbox-window-record-f6.md`; FR-17, FR-54, FR-58, AR-13, AR-15) | designer → builder → critic | `scripts/probe_by_code.py`, `scripts/red_sandbox.py`, `scripts/window_record.py`, `scripts/execution_request.py`, `scripts/sizing.py`, `scripts/run_history.py` (функции — по спеке) | RH1-9, RH1-3, RH1-8 (горячие файлы — строка `очередь:` при взятии) | закрыта: перенесено 01.11.2026 → execution-report/2 |
| RH2-5 | П1 | **П1 0.10.7, слово владельца 29.10.2026 (соседи релизных узлов, отчёт t-1573).** RH1-11, продолжение: отказ `stage_guard` (~1024) и заметка `host_capabilities` (:87) называют условия `missing` пробы; страж называет и отказ проверенной пробе другой сессии (`findings/20261028-rh1-11-otkaz-strazha-i-zametka-host-capabilities-ne-nazyvayut-missing.md`; FR-1, FR-2, FR-6, AR-9, AR-18) | designer → builder → critic | `scripts/stage_guard.py`, `scripts/host_capabilities.py`, `scripts/tests/` (имена — проверить) | RH1-11; `stage_guard.py` — очередь с codex/2 (CX2-14, CX2-27) | принято, слито (релиз 0.10.7) |
| RH2-6 | П2 | `Driver.s7_round` (`story_run.py:11181`) может отправить доработку S5 без дел — форма открытого пункта гейта A (аналог RH1-6): выяснить, бывает ли `case` пустым, вывести дело из `contract.triage_targets` или дать дела теста; сначала воспроизводящий тест (`findings/20261028-s7-round-mozhet-poslat-rework-s5-bez-del.md`; FR-1, FR-4, FR-42, AR-9, AR-22, AR-28) | designer → builder → critic | `scripts/story_run.py (s7_round, _s7_repair)`, `scripts/tests/` (имена — проверить) | RH1-6 | закрыта: перенесено 01.11.2026 → words-gates/1 |
| RH2-7 | П3 | Аналоги RH1-8: `check_delivery.lifecycle_reasons` читает признаки по точному ключу; `case_stamp.stamp()` → `immutable_proof` вызывает `case_matches` без `cfg`; `check_coverage.collect_cases` `except Exception: continue` скрывает сломанный элемент (`--write` пишет меньший счёт с годной квитанцией) (`findings/20261028-analogi-rh1-8-lifecycle-reasons-immutable-proof-collect-cases.md`; FR-41, FR-59, AR-12, AR-13, AR-28) | designer → builder → critic | `scripts/check_delivery.py (lifecycle_reasons)`, `scripts/case_stamp.py (stamp)`, `scripts/check_coverage.py (collect_cases)`, `scripts/tests/` | RH1-8 | закрыта: перенесено 01.11.2026 → execution-report/2 |
| RH2-8 | П3 | Читатели `uv.lock` и `pdm.lock` по формату, на фикстурах из настоящих lock-файлов (сейчас оба `unknown` «this lock format is not read yet»): uv — маркер на звене зависимости, строки без `version`, одно имя в двух версиях; pdm — ключ `marker` у 15 строк (`findings/20261028-chitateli-uv-lock-pdm-lock-po-formatam.md`; FR-41, FR-59, AR-1, AR-13, AR-28) | designer → builder → critic | `scripts/dependency_drift.py (_read_lock)`, `references/project-dependencies.json`, `scripts/tests/test_dependency_drift.py` | RH1-4 | закрыта: перенесено 01.11.2026 → execution-report/2 |
| RH2-9 | П1 | **П1 0.10.7, слово владельца 29.10.2026.** Тест убит таймаутом pytest проекта (300 с), а автоматор и дирижёр назвали это «индексация на стенде не завершается» — стенд источник проиндексировал (прогон 14857, TC-001): `run_suite` узнаёт убийство pytest-timeout как исход `timeout`; `blocked_by_env` — только со свидетельством среды; бриф автоматора несёт таймаут проекта на тест (`findings/20261029-tajmaut-pytest-prochitan-kak-stend-ne-rabotaet.md`; FR-18, FR-38, FR-41, FR-58, AR-10, AR-28) | designer → builder → critic | `scripts/run_suite.py`, `scripts/brief_pack.py`, `agents/qa-automator.md`, их тесты, `changelog.d/` | — | закрыта: перенесено 01.11.2026 → release-next/1 |

## Ход

Журнал передачи Lead пачки, новые записи в конец: `<дата время> — <что сделано, диспатчи t-nnn, хэши>`.

- 27.10 — пачка открыта находкой критика t-1416 (побочное наблюдение RH1-1), правило 2 «Командной работы»: пачка 1 взята, находка получает следующую (t-1425).
- 28.10 — RH2-2…RH2-7: шесть находок (E8, F5, F6 узла RH1-9; продолжение RH1-11; аналог RH1-6 `s7_round`; аналоги RH1-8) положены тем же ходом, что файлы в `findings/` (правило 2, D-0044; диспатч t-1437). Находка о `s7_round` в черновике спеки названа кучкой `driver-controller`, по слову диспатча лежит здесь (зона пачки 1 включает `story_run.py`).

- 28.10 — RH2-8: читатели `uv.lock`/`pdm.lock` по формату положены находкой критика t-1451 (B1 узла RH1-4) тем же ходом, что файл в `findings/` (правило 2, D-0044; раунд правок t-1454).
- 29.10 — релиз 0.10.6: RH2-5 подняты до П1 (соседи релизных узлов, отчёт t-1573).
- 29.10 — RH2-9 добавлен (П1 0.10.6, слово владельца): прогон 14857, TC-001 убит таймаутом pytest проекта, а фабрика сказала «стенд не индексирует».
- 30.10 — релиз переименован (слово владельца 30.10.2026): «0.10.6» в строках выше — большой релиз, теперь 0.10.7; выпущенный 0.10.6 — коммит 811f31dd; t-1613.
- 01.11 — релизы 0.10.7 и 0.10.8 слиты в одну ветку (`claude/releases-7-8-merge-b1f668`, голова `e67df7dd`): статусы строк проставлены — релиз 0.10.7: RH2-5.
- 01.11 — закрыта по слову владельца 01.11.2026 (пересборка бэклога): открытые узлы → release-next/1, words-gates/1, execution-report/1, execution-report/2

## Живые доказательства

| Что | Стенд / проект | Кто | Статус |
|---|---|---|---|

## Остатки
