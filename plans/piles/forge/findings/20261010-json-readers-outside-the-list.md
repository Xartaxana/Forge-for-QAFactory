# Читатели JSON вне списка t-666 и прочие остатки класса клонов после R1/R2

id: — | кучка: `forge` | от: Lead по вердиктам t-670/t-678 и отчётам t-677/t-674, 10.10 | приоритет: П3 | кандидат наверх: нет

Что не так / что сделать: узлы R1 (t-677, `5fb660a2`) и R2 (t-674, `b38d748b`) свели 15 читателей «объект или `{}`» на
`hooklib.read_json(kind=)` и пять карт «вариант → слово» на `gate_brief.stand_gap_word_of`, пять строк «the person wrote»
на `contract.person_decision`. Перепись G5 в `test_read_json.py` ловит функции формы «try: json.loads(read_text) / except:
константа» (тело ≤ 2 инструкций, try ≤ 2); всё, что она нашла и не переведено, лежит в её `KEPT` со ссылкой сюда (26 строк
`queued`): acceptance._manifest_under, brief_pack._load, config_contract.package_version, contract.load_json (~180 вызовов,
гейты доставки — горячий), controller.Controller._pipeline (горячий, conductor/1), cost_capture._read_pending,
factory_dashboard.is_archived_task / project_config, grammar.load_overrides, inject_context.load_map, judge_form._vocabularies,
judge_sources._read, manual_capture._env_blocked_row, onboard_apply._writer_pid, reachability.load_receipt,
report_facts._risk_words, role_cli.registry, runtime_paths._config_of, session_identity.load_rules,
source_inventory._prefix_cache, stand_health._read, stand_lease._read, story_step._read_pipeline,
test_locations._config_of, ticket_adapter._holds_inventory, window_record._load. Перепись СЛЕПА (t-678 Q3/Q5) к формам
шире: task_price._project_cost_cfg, controller._pipeline_stage_statuses, audit_factory._stage_done, acceptance._instance_test_file
(3 инструкции), читатели с отчётом об ошибке (report_cures.load, story_progress._load, external_writes.load_json,
manual_capture.spec, assertion_detectors._document, metrics_projection.read_json, probe_debt._read_json_file,
onboard_apply._load_json — контракт отказа/отчёта, не класс), к `import json as _json` (сейчас 0 случаев — читателей среди
трёх алиасов нет), к stage_guard.py:1348 (обработчик строит текст — контракт отчёта). Складываемо без потери контракта:
`exit_gate._existing` (`read_json(..., kind=dict, errors=Exception).get(...)`). Класс «конфиг проекта» (runtime_paths,
test_locations, task_price, probe_debt, story_budget, window_budget рядом с `config_contract.read_config_file`) — один
читатель конфига. Остатки групп 2–3: литерал «in your own words» в ЧЕТЫРЁХ местах (stand_gaps:492, gate_brief:1138/1140/1193)
плюс waiver:314; `story_run.py:~9225 canonical` (слово → вариант) — двойник `stand_gap_word_index`; тексты-инструкции,
описывающие форму решения (waiver:358, guard_app_under_test:280, story_run:~9095, conductor.md:26, s4.md:139, s8.md:154) —
не класс. Группа 4 (двойные циклы `_record_gap_lines`/`_record_door_lines`) остаётся намеренно (t-666 F-4, комментарий у
каждого цикла). Мелочь из t-678 Q4/Q6: `story_run.py:~6235` `"; ".join([earlier])` падает TypeError на не-строке в
повреждённом состоянии (единственный писатель кладёт строку); направление `errors=Exception` запинено трижды (`broad_none`
:118, `c5_value_reader`, `test_t674_c_rows`) — сложить в `broad_none`; мёртвая ветка `seen = "bom" in DATA_CASES`
в `c5_stage_guard_facts`; имя `c5_kept_readers` пинит и переведённый `_json_or_none`. Баг (не ход): `archive_task.cmd_archive`
/`cmd_undo` перезаписывают нечитаемый `pipeline.json` только полями архива. Дверь G5 для других узлов: строка `KEPT` с
причиной или вызов `hooklib.read_json`.

Свидетель: отчёты t-677/t-674 (dup_report --min-statements 3: 20 → 16 групп, строки 339 → 255; G1 на 8 копий исчезла);
вердикт t-678 (перепись 32/32 = KEPT, scratch-слияние R1+R2 382/382 без строки `gate_brief.read_json`).

Принципы и правила: FR-17, FR-54, ось 16 карты (`docs/SIBLING_MAP.md`), правило 9 CLAUDE.md.

Решение владельца нужно: нет.
