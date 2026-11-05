# Тождество черновика бага между двумя домами: `judge_results` ключует по basename, `delivery_summary` глотает старый дом в `known`, `story_bugs.named` — та же коллизия; читатели, видящие нелистаемую папку как `[]`

id: — | кучка: `execution-report` | от: критик t-1076 (`docs/tasks/specs/reviews/t-1100-t-1062-g1-9.md`, Q-1) и билдер фикс-раунда t-1102 (аналоги), записал Lead при слиянии G1-9, 20.10.2026 | приоритет: П3 | кандидат наверх: нет | узел: G2-9 (`batch-2-grounding-measure.md`)

Что видно (на `main` после G1-9): один читатель `bug_records.draft_listing`/`draft_paths` перечисляет черновики двух домов
(`work/bug-drafts/` и старый плоский дом), но ТОЖДЕСТВО черновика у потребителей разное: `judge_results` ключует по basename —
одинаковое имя в двух домах сталкивается; `delivery_summary` относит черновик старого дома к `known`; `story_bugs` `named`
(bug_records.py:509–514) — та же коллизия. Один ключ черновика = дом + путь относительно дома (ось 8: дома артефактов).
Второй класс (билдер t-1102): читатели, которые нелистаемую папку всё ещё читают как `[]` — `gate_preflight.check_bug_drafts`
(`self.unavailable` одной строкой, Q-5 критика), `gate_brief.bug_drafts`, `delivery_summary.build`, `judge_results.run_bugs`
(пишет `drafts=0`), `factory_dashboard` — каждый переводится на `draft_listing` одной строкой (FR-41, FR-59). Фрагмент
`changelog.d/grounding-1-g1-9-bug-draft-glob.md` не называет `draft_listing`.

Детектор сейчас: цензус читателей в `test_bug_records.py` (все читатели названы; на тождество и на `[]`-читателей пина нет).

Решение владельца нужно: нет.
