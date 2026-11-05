# `qa-factory/config.json` читают без BOM минимум семь читателей, кроме тех, что поправил GW1-19

id: — | кучка: `onboarding-forge` | от: билдер GW1-19 релиза 0.10.7 (`docs/tasks/specs/reports/r0107-s2a2-gw1-19.md`, «Neighbors»), критик S2a2 p2 (`docs/tasks/specs/reviews/r0107-s2a2-p2-diff-critic.md`, F-5), 30.10.2026 | приоритет: П2 | кандидат наверх: нет

Что не так / что сделать: GW1-19 перевёл `hooklib.load_config` на `read_json` (чтение с BOM; находка `findings/20261023-neizvestnoe-znachenie-stop-after-i-bom-config-molcha-ne-dejstvuyut.md`). Конфиг проекта, сохранённый PowerShell или редактором с BOM, остальные читатели читают как `utf-8` и получают `JSONDecodeError`: либо ловят и тихо берут умолчание (чужие настройки «не действуют», FR-4), либо падают. Список билдера (номера из спеки) пересверен на базе `268e7608` по форме `json.loads(…read_text(encoding="utf-8"))`: `check_coverage.py:99`, `environment_record.py:405`, `import_test_receipt.py:56`, `report_adapt.py:288`, `test_locations.py:745`, `test_novelty.py:320`, `grammar.py:273`. Из списка билдера уже читают с BOM `factory_dashboard.py:725`, `retro_numbers.py:319`, `project_decisions.py:443` — их из узла вычёркивать. Критик p2 не нашёл список в пачке `gates-and-words` по `git grep`; эта находка — его носитель. Что сделать: каждый читатель идёт через `hooklib.read_json` / `config_contract.read_config_file` (один читатель, AR-13), а не правится побуквенно; пин: конфиг с BOM даёт те же значения во всех семи; `grammar.py:273` (билдер не прослеживал) проверить.

Свидетель: `grep -n "json.loads.*config.json.*encoding=\"utf-8\"\)"` по перечисленным файлам на `268e7608` (строки выше); `docs/tasks/specs/reports/r0107-s2a2-gw1-19.md:53-55`; критик p2 `…:73`, `:100`.

Принципы и правила: P1; FR-4, FR-41, FR-54; AR-3, AR-13.

Решение владельца нужно: нет.
