# Docker-канон релиза 0.10.3 красный не только на среде: K11 `ledger.test_state` и ещё шесть наборов, плюс A19 над реальным пакетом

id: — | кучка: `run-honesty` | от: docker-канон релиза 0.10.3 (`8bfbccfc`), разведка t-1414, 27.10.2026 | приоритет: П1 | кандидат наверх: нет

Что не так / что сделать: канон 0.10.3 на docker `python:3.12` (вывод — `D:/ws1/canon-release-0103\out\selftest.txt` и `install_smoke.txt`, вне репозитория) закончился `456/468 ok` и `INSTALL SMOKE: FAILED`. Красные делятся на два класса.

(1) Регрессия или устаревший тест, узел RH1-1: `scripts/tests/test_case_id_form_sites.py` (216/220), ключ K11 «a result row naming only the project id joins the manifest test» — ожидался `passed_green`, получен `not_executed:no result for this test in run-report.json`. Строка результата с другим `instance_id`, но с тем же кейсом, теперь не засчитывается тесту манифеста. Либо тест устарел после намеренного ужесточения узла VC (instance_id / attempt_id), либо `ledger.test_state` потерял совпадение по проектному id: решает критик ДО билдера (читать узел VC, `scripts/ledger.py`, сам тест); ни одну из сторон не «чинить по тесту» (FR-58, P20).

(2) Остальные красные, узел RH1-2 (по файлам `selftest.txt`):
- `test_driver_layers.py` (51/52): L1 «holds on the real driver (1 problem(s))» — текст проблемы в выводе обрезан;
- `test_s0_close_order.py` (27/28): «and the accept route for a stage a role DID run — '--operation accept' not found»;
- `test_state_portability.py` (93/98): N0-K1, N0-K3 — новый файл `<PROJECT>/qa-factory/artifacts/<TASK>/work/briefs/<DISPATCH>.md` не в эталоне (поток F3, писатель `brief_pack.py :63`); N0-K3 «the stale row is the only complaint» — 2 вместо 1;
- `test_story_run_stand_identity.py`: O1/P3 «the label was never consulted» — ожидалось `['test -d']`, получено `['test -d', 'inspect']` (лишний вызов `inspect`);
- `test_words_doors.py` (470/471): B-387 «no inline door outside the exemption and the pending list» — в `skills/qa-story/phases/s5.md` инлайн-дверь `waiver.py --task <TICKET> --stage S5 --block "<that word>" --decision "`;
- `test_judge.py`: выход 1, деталь строки обрезана в выводе канона;
- A19 над реальным пакетом (только в `install_smoke`): `agents/qa-code-critic.md` — `missing section(s) ['## Procedure']`; раздел разделён на «On the plan» / «On the code (a window)». Починка: вернуть `## Procedure`, оба раздела — подразделы `###`; запас A25 у qa-code-critic 1 457 B (`A25 (info): heaviest dispatch — qa-code-critic 56,543 B`), значит правка не должна расти в размере.

НЕ входит сюда (только среда контейнера): нет `.git` в контейнере — K10/K15 positive control (`git grep over 941a948 / 8637374`: «unable to resolve revision») и `tools/test_enforcement_probe.py` ×2; четыре таймаута 300 с (`test_story_run_delivery_b`, `test_story_run_refusals`, `test_story_run_s7_live`, `test_story_step`) и PERF 240 в K-наборе — нагрузка/время, не поведение (канон ветки в CI — `hotfix-12586/findings/20261026-kanon-vetki-v-ci-i-koroche.md`).

Свидетель: `D:/ws1/canon-release-0103\out\selftest.txt` (строки с `FAIL`), `D:/ws1/canon-release-0103\out\install_smoke.txt` (хвост: `A19 agents contract: VIOLATIONS (1)`, `=== INSTALL SMOKE: FAILED ===`); разведка `docs/tasks/handoffs/t-1414-next-release-urgent-survey.md`, раздел 0.

Принципы и правила: FR-32 (чинить корень, не тест), FR-33, FR-58, AR-20, AR-28; процессные находки канона — `forge/findings/20261027-docker-kanon-arhiv-crlf-run-py-cmd.md`, `…-a19-nad-realnym-paketom-tolko-v-install-smoke.md`.

Решение владельца нужно: нет (RH1-1 — решение критика: устарел тест или регрессия).
