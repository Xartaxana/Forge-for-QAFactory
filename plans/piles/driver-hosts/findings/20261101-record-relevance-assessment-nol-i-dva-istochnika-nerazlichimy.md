# `source_inventory.record_relevance_assessment`: «ноль источников» и «два источника» дают один отказ «source_id must identify exactly one source» — без списка известных id и без двери

id: — | кучка: `driver-hosts` | от: аналог `:2876` из критика диффа HF8-5 (`docs/tasks/specs/reviews/r0107-hf8-5-diff-critic.md`, вопрос 3) и соседи спеки (`docs/tasks/specs/r0107-s6b-a-hf8-5.md`), `docs/tasks/release-0.10.7.md:196`, 01.11.2026 | приоритет: П3 | кандидат наверх: нет

## Что наблюдалось

`scripts/source_inventory.py`, `record_relevance_assessment` (около :3148-3160 в слитом дереве; ~:2867-2876 в дереве критика): `if len(matches) != 1: raise ValueError("source_id must identify exactly one source")`.
Ноль и два неразличимы (тот же класс, что исправил HF8-5 для `inspect`: AK2/AK5 различают «нет источника», «несколько» и дают список). Критик: однострочник через `_sources_hint`.
Спека HF8-5 сознательно оставила функцию вне `owns` и поручила Lead завести находку.

## Что именно менять

1. `record_relevance_assessment`: ноль совпадений — «no source `<id>`; known source_id values: …» через `_sources_hint` (список с пределом `_LIST_LIMIT` и хвостом); пустой список — дверь `collect`
   (как AK3); два и более — «several sources carry this id» с их перечислением.
2. Тест (`scripts/tests/test_source_inventory*.py`): три входа (ноль / один / два) — разные тексты, у «ноль» названа дверь. Мутация: вернуть общий текст — красит тест.

## Принципы и правила

FR-1, FR-2, FR-41; AR-9. Связи: HF8-5, соседи `record_attachment_inspection` (исправлен в HF8-5).

Решение владельца нужно: нет.
