# Очередь спеки OF3-1 §7: узлы OF3-1d2 и N-r1…N-r8 ждут пачки `onboarding-forge/4` (D-0044)

id: — | кучка: `onboarding-forge` | от: спека `docs/tasks/specs/t-129-of3-1-knowledge-catalog.md` §7 «Queue entries» (:581-600) и критик `docs/tasks/specs/reviews/t-190-of3-1c-diff.md` (очередь Q2), 12.11.2026 | приоритет: П2 | кандидат наверх: нет

Спека §7 написана как узлы с `owns` и тестом; §7 «перекрывает §1-4». Места, где указано «P\» — префикс `ai-packages/qa-factory/`. Критик t-190 (Q2): пачки `batch-4` не было (D-0044) — она открыта этим ходом. Спека t-129 лежит в рабочей копии Lead (в этой ветке файла нет); строки ниже — полная копия смысла каждого узла.
Критик t-190 нашёл также `execution_scheduler.py:154` (четвёртое место job-store, игнорирующее `artifact_root`): строка уже есть в другой пачке — узел OH5-12 пачки `onboarding-hooks/5` (B-298, `findings/B-298-klass-put-artefaktov-sobran-ot-proekta-cwd.md` той кучки) называет `execution_scheduler.py:154`, `source_exclusions.py:545,568`, `ticket_adapter.py:759` и направление «через читателя `artifact_root` OF3-1»; здесь не заводится второй раз.

## OF3-1d2 — `dispatch_liveness` читает корень артефактов через `hooklib.artifact_root`

`scripts/dispatch_liveness.py:800` (путь `…/artifacts/<ticket>/state/driver-runs.jsonl`) и `:951` (`driver-state.json`; `in_flight_entry`, там уже ловятся `(OSError, ValueError, AttributeError)`) строят путь литералом `"qa-factory" / "artifacts"` — проверено на main. Направление: оба места читают `hooklib.artifact_root(root=project_root)`, ловят `(OSError, ValueError, AttributeError)` → `unknown` (ничто не закрывается отсутствием, `config-keys.json:465`). Изменение поведения: битый конфиг читается «unknown» (сегодня — папка по умолчанию).
Пишет в: `scripts/dispatch_liveness.py`, `scripts/tests/test_dispatch_liveness.py`. Тест: строки «настроенный корень: driver-runs / driver-state найдены там; битый конфиг → unknown». Порядок: `очередь: OF3-1d2 → N-r4` (оба пишут `dispatch_liveness.py`); см. также узел «артефакт-рут бросает на битом конфиге» (`findings/20261112-artifact-root-brosaet-na-bitom-konfige-a-vyzyvayushchie-lovyat-ne-to.md`) — та же правка у вызывающих.

## N-r1 — `environment` / `environments[]` через `project_knowledge.environment`

Читатели класса `environment`/`environments[]` (строки env-класса переписи узла c; известно: `scripts/stand_gaps.py`, `scripts/env_probe.py` `data_cleanup` — поиск стенда) идут через `project_knowledge.environment` (карточка стенда). Пишет в: эти строки переписи, `scripts/project_knowledge.py`. Тест: `scripts/tests/test_project_knowledge.py` — каждый читатель переписи даёт тот же стенд, что `environment(name)` по рёбрам стенда §4; базовая линия R2 сжимается. Когда: фаза 3.2 (OF3-3). Входит также `project_knowledge._stand_roles` против `_stand_card` (критик t-154, F3) — два пути в одном файле.

## N-r2 — `load_config` у вызывающих через один читатель с объявленным направлением ошибки на класс вызывающих (§7 C16)

Пишет в: `scripts/hooklib.py` (`load_config`) и вызывающие переписи; `scripts/manual_capture.py` (`load_config`, уходит из `OUTSIDE_WALKS`). Тест: `scripts/tests/test_read_json.py` — набор строк на класс вызывающего; `OUTSIDE_WALKS` сжимается. Когда: после слияния потоков «hooklib», «hot» И принятия переписи узла c (`owns` читаются из неё; перепись — `docs/tasks/t-183-of3-1c-config-census.md`, ветка `wip/of3-1c`).

## N-r3 — `contract.registry_sides` через `project_knowledge.state`

Пишет в: `scripts/contract.py`, `scripts/project_knowledge.py`. Тест: `test_project_knowledge.py` — ключи сторон дают равные ответы через оба, до свёртки. Когда: после узла a (OF3-1 a).

## N-r4 — оставшиеся прямые чтения `utf-8-sig` конфига (F-8 + перепись) и `install_smoke.py:414`

Пишет в: `scripts/controller.py`, `branch_accounting.py`, `dashboard_refresh.py`, `dispatch_liveness.py`, `env_probe.py` (:1114), `factory_dashboard.py`, `judge.py`, `install_smoke.py` + строки переписи. Тест: `test_read_json.py` — строки BOM на место; базовая линия R2 сжимается. Когда: после потоков, владеющих файлами; `очередь: OF3-1d2 → N-r4` (`dispatch_liveness.py`); `очередь: OF3-1c, OF3-1e → OF1-1 → N-r4` (`env_probe.py`). Входят места критика t-190 Q4 (см. `findings/20261112-chtenie-config-mimo-chitatelya-app-card-i-scheduler.md`), если перепись узла c не даст им иного вердикта.

## N-r5 — `traceability.py --task-root` и `--task` читают корень багов одним правилом (`hooklib.artifact_root`)

(строка бэклога B-348.) Пишет в: `scripts/traceability.py`. Тест: `test_bug_records.py` (keep, покрывает `traceability.py`) — при `artifact_root: qa-artifacts` обе формы читают одну папку. Когда: после узла d.

## N-r6 — C18: три писателя конфига (F-8b) кончаются в `config_contract._write_config` (AR-14)

Пишет в: `scripts/project_decisions.py`, `scripts/runtime_probe.py`, `scripts/config_contract.py` (сигнатура `_write_config`: требует `approval_ref` / `input_hash`, которых у пробы нет; `recorded_writes`; `_kept_pointers`). Тест: `test_config_migration.py` — запись каждого писателя идёт через `_write_config` (или строка `written_by`, решает спека узла); откат сохраняет указатели каждого писателя как сегодня (`restore_config`). Когда: фаза 2 (F9); после узлов a, f (`test_config_migration.py`) и OF1-2 (`config_contract.py`). Рядом: `findings/20261112-resolve-perepisyvaet-config-pri-neizmennom-znachenii.md` (тот же писатель, `resolve`).

## N-r7 — слово владельца 12.11.2026 (F11): исправленное человеком значение стенда записывается в конфигурацию проекта

Значение стенда, оказавшееся неверным (например адрес), и человек велит фабрике его поменять — пишется в конфигурацию проекта (настроенный env-файл или `config.json`, где лежит ключ), не живёт только в прогоне; следующий прогон читает исправленное. Дизайнер набрасывает сначала (где сегодня принимается поправка человека, какой писатель владеет носителем — AR-14, AR-24). Тест: строка «поправка человека лежит в носителе; второй прогон читает её». Когда: фаза 2 или 3.2 (вместе с N-r1, карточкой стенда).

## N-r8 — слово владельца 12.11.2026 (критик t-154 F2): у `format_changed` нет читателя

`format_changed` (форматировать только затронутые стори файлы; TP2-2520) передаётся автоматору (S5), чтобы роль знала единственную команду форматирования; `format_all` остаётся удалённым. Билдер после слияния OH5-9 (`scripts/brief_pack.py` пишется там): бриф автоматора S5 несёт `format_changed` через `project_knowledge.value()`; строка каталога называет этого читателя в `needed_by`; пустое значение → бриф говорит «узкого форматировщика нет», роль не форматирует (никогда не откатывается к широкой команде). Тест: значение доходит до брифа S5; пустое даёт строку «нет форматирования»; R3 больше не находит пустой `needed_by`. Когда: узел f или эта пачка.

Принципы и правила: FR-54; AR-1, AR-4, AR-13, AR-14, AR-16, AR-22.

Решение владельца нужно: нет (N-r7, N-r8 — слово владельца уже в спеке).
