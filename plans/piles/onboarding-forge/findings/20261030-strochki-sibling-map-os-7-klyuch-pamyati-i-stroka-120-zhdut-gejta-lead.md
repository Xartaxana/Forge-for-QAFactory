# Две правки `docs/SIBLING_MAP.md` релиза 0.10.7 ждут Lead-гейта: строка оси 7 для ключа памяти сбора и переписанная строка `:120` (выход стадии ↔ `finish`)

id: — | кучка: `onboarding-forge` | от: билдеры EP1-23 B2 и GW1-10 релиза 0.10.7 (`docs/tasks/specs/reports/r0107-s2b-b2-fix.md:38`, `:73`; `docs/tasks/specs/reports/r0107-s4b2-gw1-10-fix.md:19`), критик `docs/tasks/specs/reviews/r0107-s2b-b2-diff-critic.md:96`, 30.10.2026 | приоритет: П2 | кандидат наверх: нет

Что не так / что сделать: `docs/SIBLING_MAP.md` — известный дом механизмов (правило 10 `CLAUDE.md`: блок осей и строка `tier:` в коммите), поэтому билдер правит его не сам, а передаёт текст. Две правки ждут. (1) Ось 7 («Per-test identity ↔ every scope a test's behaviour depends on», `SIBLING_MAP.md:175`) не имеет строки для ключа памяти сбора EP1-23 B2: `execution_request._collect_memo_key(argv, run_cwd, test_files, helpers, dependency_files, config_files, provenance, project_root=None)` и читатель `_memo_of_jobs` (память играет через настоящий `build_mine_request`; `request_digest` исключает `collect_memo`). Критик B2: ось называет эту область, строки для ключа нет; пакетные `__init__.py` на пути импорта ключом не прослеживаются (ось 7 называет эту границу); второй каркас `execution_fingerprint.function_sha` с другим контрактом (добавленный тест не входит) повторно не использовать. (2) Строка `SIBLING_MAP.md:120` («Stage exit ↔ its `finish` (GW1-8)») после GW1-10 устарела: «догадка о стори» закрыта GW1-10 для пяти детекторов (`detector_story`), открыты `runtime_probe.py:190` и `exit_gate._ticket_for_stage` (всё ещё угадывают), чтение при падении — GW1-9; фикс-раунд GW1-10 (F-6) переписал строку, но в базу `268e7608` правка не вошла (строка прежняя). Что сделать: Lead кладёт обе строки одним коммитом с блоком осей и `tier:`; `tools/test_sibling_map*.py`, если есть, прогнать по свидетелю.

Свидетель: `docs/SIBLING_MAP.md:120` (прежний текст), `:175` (заголовок оси 7); `r0107-s2b-b2-fix.md:38` («the map row for the key is queued… the Lead adds it»); `r0107-s4b2-gw1-10-fix.md:19`.

Принципы и правила: FR-54; AR-19.

Решение владельца нужно: нет.
