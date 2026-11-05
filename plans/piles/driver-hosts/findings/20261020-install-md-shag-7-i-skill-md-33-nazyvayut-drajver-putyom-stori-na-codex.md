# INSTALL.md шаг 7 и SKILL.md:33 называют драйвер путём стори на Codex, а путь один на обоих хостах — навык вызывает человек

id: — | кучка: `driver-hosts` | от: Lead по слову владельца 20.10.2026 20:1x (чат, пачка kb/2: «У нас есть скилл и его вызывает пользователь. И как Кодексе и на клоде»), 20.10.2026 | приоритет: П2 | кандидат наверх: нет | узел: CX2-26 (`batch-2-leftovers-and-rollout-reader.md`)

Что видно (на `main`): `ai-packages/qa-factory/INSTALL.md:26-29` (шаг 7 раздела Codex) говорит «Run a story through the driver, not
through a desktop orchestrator: `python <plugin>/scripts/story_run.py --task <TICKET> --host codex`…» — текст Lead при слиянии CX1-15;
`skills/qa-story/SKILL.md:33` после абзаца о `hooks/codex.json` и профилях `.codex/agents/*.toml` добавляет «Stories run via the driver:
story_run.py --task <T> --host codex». Обе фразы читаются так, будто на Codex инженер гоняет стори драйвером, а на Claude — навыком.
Слово владельца: путь ОДИН — инженер вызывает навык `qa-story` и на Claude, и на Codex; сессия раздаёт роли (на Codex — через
`hooks/codex.json`, профили `.codex/agents/*.toml` в CLI или desktop `task_name`); драйвер `story_run.py --host claude|codex` —
headless-запуск для ОБОИХ хостов, не путь инженера. Фраза Lead «на Codex стори гоняется через драйвер» отозвана (t-1150 §L-2);
страницы КБ пишутся по одному пути (kb/2, KB2-3).

Что сделать: переформулировать обе фразы нейтрально к хосту — INSTALL.md шаг 7: «Run a story the same way as on Claude: invoke the
`qa-story` skill in a Codex task; headless alternative on both hosts — `python <plugin>/scripts/story_run.py --task <TICKET>
--host codex` (design/driver.md)»; SKILL.md:33: «Headless alternative on both hosts: story_run.py --task <T> --host claude|codex
(design/driver.md)». Проверить соседей по оси 5 (тексты, которые читает человек о пути стори): `README.md` пакета, `kb/`
(KB2-3 правит сам), `design/driver.md` (вступление — «headless runner», не «the way to run on Codex»), `references/codex-host.md`.
Пин: документный ключ в `test_audit_rules.py` или `install_smoke.py` на фразу «Headless alternative on both hosts» с отрицательным
контролем на «not through a desktop orchestrator» (0 попаданий).

Детектор сейчас: нет (слово владельца пришло через вопрос к странице КБ).

Решение владельца нужно: нет — слово дано 20.10.2026 20:1x.
