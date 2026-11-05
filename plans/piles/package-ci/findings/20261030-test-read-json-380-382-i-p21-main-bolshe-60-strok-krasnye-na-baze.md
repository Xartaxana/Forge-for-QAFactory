# Два теста красные на базе релиза: `test_read_json` (G5, 380/382) и `test_project_decisions_change_request` (P21: `main()` в 70 строк)

id: — | кучка: `package-ci` | от: билдер OH3-23 и фикс-раунд HF7 релиза 0.10.7 (`docs/tasks/specs/reports/r0107-s4b2-oh3-23-builder.md:71`, `:106`; `docs/tasks/specs/reports/r0107-hf7-round2.md:18`, `:58`), замер на базе `268e7608`, 30.10.2026 | приоритет: П2 | кандидат наверх: нет

Что не так / что сделать: (1) `python -B ai-packages/qa-factory/scripts/tests/test_read_json.py` на `268e7608`: `FAIL G5 no reader-shaped function outside KEPT… — NEW: manual_evidence._read_json (manual_evidence.py:1466)`; `FAIL G5 no stale KEPT row… — STALE: hooklib.load_config`; `=== read_json: 380/382 ok ===`. Второй — следствие GW1-19: `hooklib.load_config` переведён на `read_json`, строка KEPT осталась; первый — новый читатель-двойник `manual_evidence._read_json`. (2) `test_project_decisions_change_request.py`: `FAIL P21: main() is under 60 lines — 70 lines`, `127/128`; `project_decisions.main` вне диффа OH3-23, вырос в HF8-9/HF8-10. Что сделать: (1) убрать строку KEPT `hooklib.load_config` и перевести `manual_evidence._read_json` на `hooklib.read_json(kind=dict)` либо завести строку KEPT с причиной; (2) вынести ветки `main` в функции — до 60 строк. Это красные на релизной базе: их не ловит ни один свидетель узла, и они не от одного узла (FR-34).

Свидетель: `python -B ai-packages/qa-factory/scripts/tests/test_read_json.py` — `=== read_json: 380/382 ok ===`; `python -B ai-packages/qa-factory/scripts/tests/test_project_decisions_change_request.py` — `FAIL P21: main() is under 60 lines — 70 lines`, `=== project_decisions_change_request: 127/128 ok ===` (оба на `268e7608`).

Принципы и правила: FR-34, FR-54, FR-28; AR-13.

Решение владельца нужно: нет.
