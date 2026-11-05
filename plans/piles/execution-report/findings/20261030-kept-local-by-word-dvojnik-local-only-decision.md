# Отчёт и исполнитель читают слова «баги остаются в репозитории» двумя функциями: `bug_records._kept_local_by_word` — двойник `external_writes.local_only_decision`

id: — | кучка: `execution-report` | от: критик диффа S5b rest релиза 0.10.7 (`docs/tasks/specs/reviews/r0107-s5b-rest-diff-critic.md`, F-4) и фикс-раунд (`docs/tasks/specs/reports/r0107-s5b-rest-fix.md`, «Не сделано»), 30.10.2026 | приоритет: П3 | кандидат наверх: нет

Что не так / что сделать: исполнитель решает «оставить локально» в `external_writes.local_only_decision` (`external_writes.py:297`), отчёт — в `bug_records._kept_local_by_word` (`bug_records.py:721`, использование `:762`). Критик (F-4, AR-13) требовал одну функцию над строками `pipeline.json` в `external_writes.py` и обоих вызывающих на ней; фикс-раунд не сделал: `external_writes.py` не входил в `owns`. Вместо этого двойник приведён к исполнителю по пустым словам и по паре markdown-каналов (`("", "markdown")`) внутри `bug_records`. Остаётся второе место, где слова гейта B читаются, и константа `MARKDOWN_BUG_CHANNELS` в `external_writes.py` (не существует). Класс: исполнитель и отчёт читают один факт разными функциями — расхождение даёт отчёту «вы сказали держать локально» над записью, которую исполнитель пробует отправить. Что сделать: одна функция над строками `gate_waivers` / `stage_overrides` и одна константа каналов в `external_writes.py`, `bug_records` вызывает её; пин: пустые слова, канал `none`/`file`, этап S8/S9/пусто — оба вызывающих дают одно.

Свидетель: `ai-packages/qa-factory/scripts/bug_records.py:721-735`; `scripts/external_writes.py:297`; `r0107-s5b-rest-fix.md:36`, `:86`; критик `r0107-s5b-rest-diff-critic.md:22-24`.

Принципы и правила: FR-35, FR-54; AR-13, AR-14.

Решение владельца нужно: нет.
