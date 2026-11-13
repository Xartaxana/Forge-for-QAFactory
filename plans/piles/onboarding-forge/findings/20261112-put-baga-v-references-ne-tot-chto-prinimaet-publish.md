# Класс «путь бага»: общие правила, срезы, `external-writes` и `driver_stage_s8s9` называют `qa-factory/bugs/`, а `publish` принимает только папки стори

id: — | кучка: `onboarding-forge` | от: приёмка OH5-9 (журнал `logs/journal/dev1.jsonl`, t-156 accepted 78f2a8c; слова Lead 12.11.2026, снимок `docs/tasks/compact-snapshots/2026-11-12-2003-narrative.md`, строка «класс путь бага»), 12.11.2026 | приоритет: П3 | кандидат наверх: нет

Критика на OH5-9 как файла в `docs/tasks/specs/reviews/` нет (принято Lead без критика, малый текстовый дифф): источник — журнал и снимок; пути правки OH5-9 — ветка `pile/onboarding-hooks/batch-5`, в main нет.

## Что наблюдалось

OH5-9 (B-315) поправил хартию `agents/qa-bug-reporter.md` и бриф (`brief_pack.py:167`): путь бага — `<task root>/bugs/` и обе папки, которые принимает `publish` (`work/` и `bugs/` стори), а не общий `qa-factory/bugs/`.
Тот же устаревший путь остался в `references/` и в одном скрипте (на main те же строки, поиск `qa-factory/bugs`):
- `references/common-rules.md:111` — «`bugs/BUG-1.md` is `<project>/qa-factory/bugs/BUG-1.md`» и копии-срезы, генерируемые из него: `references/slices/<роль>/common-rules.md` у qa-automator (:90), qa-bug-reporter (:85), qa-case-designer (:48), qa-code-critic (:103), qa-doc-scribe (:85), qa-failure-analyst (:103), qa-retro-analyst (:85), qa-runner (:103), qa-scout (:61), qa-test-strategist (:48);
- `references/external-writes.md:44` — «a bug always gets `qa-factory/bugs/BUG-n.md` regardless of channel»;
- `references/templates/test-report.md:35` — «BUG-n — a bug file in `qa-factory/bugs/`»;
- `scripts/driver_stage_s8s9.py:275` — «proposal under qa-factory/bugs» (текст роли);
- журнал-контракт `contract_slices` (digest): срезы пересобираются командой `python -B scripts/contract_slices.py --write`.
Но `qa-factory/bugs/` — не просто опечатка: `scripts/bug_records.py:134-137` и строка `references/install-paths.json:40` (`qa-factory/bugs/**`, `carried`, читатель `bug_records.py`) называют проектный дом багов настоящим. Поэтому сводить нельзя вслепую.

## Что именно менять

**Вопрос владельцу.** Какие два пути бага у фабрики: проектный дом `<project>/qa-factory/bugs/` (читатель `bug_records.py`) и папка стори `<task root>/bugs/` (то, что принимает `publish`)? Если оба настоящие — тексты называют оба и говорят, какой для чего; если проектный дом — остаток, `bug_records.py` и `install-paths.json:40` тоже сводятся. Рекомендация, до слова владельца: тексты называют ровно ту пару, что OH5-9 дал хартии (`<task root>/bugs/` для публикации, проектный дом — только как место чтения `bug_records.py`).

Исполнимо по рекомендации: 1. `references/common-rules.md` строка 111 и `references/external-writes.md:44`, `references/templates/test-report.md:35`, `scripts/driver_stage_s8s9.py:275` — формулировка OH5-9. 2. `python -B scripts/contract_slices.py --write` (одна правка источника, срезы пересобраны, `--check` зелёный). 3. Тест: существующие `test_contract_slices.py` (`--check`), `test_audit_rules.py`, `test_role_load.py`; строка «путь бага из текста роли — тот, что `publish` принимает» (как в тесте OH5-9). Ограничение: храповики длины (`process_ratchet_tokens`, поправки OH5-9) — формулировка не длиннее прежней.

Зависит от слияния OH5-9 (`pile/onboarding-hooks/batch-5`). Принципы и правила: FR-37, FR-54; AR-13, AR-19, AR-22.

Решение владельца нужно: да (какие пути настоящие).
