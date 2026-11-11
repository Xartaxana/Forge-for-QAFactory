# Карантин тестов: файлы состояния

Рабочий документ форджа (в релиз не уходит). Спека — `docs/tasks/specs/td-15-scenarios-quarantine.md` (разделы C и D), правило
о тестах — `docs/TESTING.md`. Читает и пишет эти файлы один инструмент — `tools/test_quarantine.py`; руками правятся только
`config.json` и (в крайнем случае) строки, которые инструмент отказывается написать.

| Файл | Что | Кто пишет | Кто читает |
|---|---|---|---|
| `config.json` | `{"ci": "gitlab", "branch": "<ветка карантина>", "cron": "0 3 * * 1,4", "max_gap_days": 4, "schedule_variable": "QUARANTINE_WATCH"}` — ветка, на которой идёт канон пакета; без файла `enter`, `pull`, `status` отказывают или отвечают `unknown` с дверью «write plans/test-quarantine/config.json» (ветка никогда не угадывается); ключ `ci` читается: кроме `gitlab` инструмент отвечает `unknown` с дверью (читает только GitLab, спека E2), без ключа — `gitlab` | Lead, руками | `tools/test_quarantine.py` |
| `watch.jsonl` | строки `{"kind": "run", "pipeline", "source", "created_at", "sha", "package_version", "complete", "files"}` (прогон наблюдателя) и `{"kind": "pull", "at", "ci": "ok\|unreachable\|token_refused", "newest_watch_pipeline", "newest_watch_at"}` (вытяжка); две строки с одним `pipeline` — одна; исключение — повторное чтение того же pipeline по `pull --pipeline <id>` (после Retry задачи): если запись изменилась, пишется строка `run` с `"retry": N`, и красное с зелёным на одном sha лягут рядом (дверь `judge` flaky); `newest_watch_*` берётся только из записанных `run`, pipeline без записи время наблюдателя не двигает; тревога о наблюдателе горит и когда последняя удачная вытяжка старше 2 × `max_gap_days` или удачной не было вовсе (вытяжки отказаны или CI недоступен) | `pull` (узел TD-15.6b), Lead коммитит | `status`, `judge`, строка сессии |
| `verdicts.jsonl` | вердикты `{"ts", "file", "signature", "pipeline", "verdict": "stale\|real_catch\|flaky", "by", "reason", "finding", "task"}` (+ `"supersede": "<why>"` у заменяющего); строки `{"kind": "land", "file", "pipeline", "commit"}` — настоящий улов перенесён; строка `{"kind": "purge", ...}` — удаление по слову владельца | `judge`, `land`, `purge` | `status`, строка сессии |

Что где лежит в пакете: `ai-packages/qa-factory/scripts/tests/test-layers.json` (секции `keep`, `quarantine`, `cohorts`, `pin_holds`) —
читает только `selftest.test_layers()`; `quarantine` и `cohorts` пишет только `tools/test_quarantine.py enter`, строка keep уходит только им.

Команды: `enter` (перевод в карантин, фаза 1; `--phase2` — перевод детектора; `--rebase-entry` — после переписанной истории),
`check` (страж правок: диапазон от появления `test-layers.json`; двери — строки в сообщении коммита `quarantine-enter:`,
`quarantine-edit:`, `quarantine-purge:`, `keep-drop:`, `quarantine-import:`, прошлое нарушение — `quarantine-accept:`),
`status` (правила R1–R6 по когортам), `judge` / `land` (разбор красного и перенос улова), `drop-keep`; `pull`, `ci-summary`,
`purge` — узлы TD-15.6b и TD-15.6c.
