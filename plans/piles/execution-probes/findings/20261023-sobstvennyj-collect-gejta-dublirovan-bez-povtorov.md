# Собственный запуск collect репетиции гейта дублирует `node_ids.collect` без повторов `-qq` и дерева

id: — | кучка: `execution-probes` | от: Lead пачки hotfix-12586/1 (dev2), 23.10.2026 | приоритет: П3 | кандидат наверх: нет

перенос: speed-cost/batch-1 (узел SC1-12; слово владельца 26.10.2026)

Что не так: на шаге `s5_toolchain` репетиция гейта сама запускает pytest `--collect-only` (`subprocess.run(command, ...)` над
`collect_command(config)`, `scripts/gate_preflight.py:215` и `:1625`) и читает вывод через `node_ids.parse_collected`. Полноценный
запуск с повторами живёт в `node_ids.collect` (`scripts/node_ids.py:227`): когда `-q` проекта в `addopts` вместе с нашим даёт `-qq`
и pytest печатает `file.py: 3` вместо id, вызов повторяется с `-v` (`node_ids.py:243-247`); когда `-v` проекта отменяет наш `-q` и
pytest печатает дерево `<Module>/<Function>`, повторяется с лишним `-q` (`node_ids.py:248-255`). У двух запусков одного вывода — два
набора устойчивости к формам: на проекте, чей `addopts` меняет подробность вывода, гейт и S5 читают разное, а гейт повторов не делает.

Свидетель: `docs/tasks/handoffs/t-053-hf1-1.md` («Queue (non-goals, not done)», A4: «the gate's collect runner (`subprocess.run` +
`collect_command`) duplicates `node_ids.collect` without the `-qq`/tree retries — a finding/backlog line for the Lead»). Узел HF1-1
(EP1-9) свёл оба парсера к одному читателю (`parse_collected`) и сделал `unread_count` общим для S5 и гейта, но не сам запуск.
Номера строк — по дереву пачки hotfix-12586/1, проверены 23.10.2026.

Что сделать: репетиция гейта берёт вывод у одного запуска (`node_ids.collect` либо выделенная из него функция, возвращающая код и
текст до решения об исключении), а не у своего `subprocess.run`; отличия гейта (таймаут `gate_rehearsal.collect_timeout_s`,
`FileNotFoundError` → вопрос об исполнителе, `skip_collect`) остаются в обёртке. Тест: проект с `-q` в `addopts` даёт гейту те же
id, что S5; отрицательный контроль — гейт со старым запуском видит `file.py: 3` и «ноль прочитано».

Принципы и правила: FR-17, FR-59, AR-13, AR-15.

Решение владельца нужно: нет.
