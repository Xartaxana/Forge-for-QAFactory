# Остаток B-449: 16 копий настройки потоков в звеньях цепи, 14 в `experiments/`, одна в `gateway/`, и слепые пятна переписи

id: B-449 | кучка: `forge` | от: билдер t-629 / Lead, 09.10 | приоритет: П3 | кандидат наверх: нет

Что не так / что сделать: узел B-449 (t-629) свёл 19 мест `.reconfigure(` в 16 файлах `tools/` вне цепи механизмов на
один помощник `tools/streams.py`; перепись `tools/*.py` после: 17 строк в 16 файлах — 16 копий в 15 звеньях цепи
(`agents_md`, `claim_control_gate`, `dispatch_gate` ×2, `dod_gate`, `dod_track`, `factory_rules_index`, `forge_metrics`,
`hygiene_gate`, `journal_echo`, `main_gate`, `negative_lint`, `owns_gate`, `piles`, `piles_split`, `search_control_gate`;
шесть держат обёртку `_reconfigure_stdout_utf8`) остаются по решению Lead 09.10 (звено не импортирует утилиту — иначе
она входит в сеть через тест замыкания). Вне `tools/`: 14 копий в `experiments/`, одна в `gateway/lead_replay.py`,
`judge_calib_sanitize._write_stdout_utf8` (другая форма). Слепые пятна переписи S3/S4 (названы в тесте):
`getattr(s, "reconfigure")(...)`, перепривязка `sys.stdout`, `importlib`, вызовы инструментов вне цепи из
механизм-путей не-`tools/*.py` (`.claude/skills/permission-audit/SKILL.md:33`, файлы `.claude/agents`). Что сделать:
(а) звенья — только мех-коммитом Lead, если решение 09.10 будет пересмотрено (например, `streams.py` в
`MECHANISM_PREFIXES`); (б) `experiments/` и `gateway/` — отдельный узел по той же спеке t-624 §3–4 (вне ветки CI
`forge-check`? проверить, гоняет ли их `pytest tools/`); (в) очередь по F8(b) спеки t-630 не сюда. Общие куски двух
храповиков (JSON-база, коды выхода, перемаркировка версии, обёртка run/main) — по-прежнему ждут «третьего храповика»
(критик t-534 Q5); член карточки B-449 частичный.

Свидетель: отчёт `docs/tasks/specs/reports/t-629-builder-report.md` (перепись до/после: 35/31 → 17/16; M1–M11 убиты);
спека `docs/tasks/specs/t-624-b-449-streams.md` §2 (таблица переписи), §10.4.

Принципы и правила: FR-17, FR-54; ось 15 SIBLING_MAP; правило 9 CLAUDE.md (класс назван, остаток записан явно).

Решение владельца нужно: нет.
