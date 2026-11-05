# Патч новых `obligation_refs` без хэша оставляет прежний `obligation_hash`; `probe_by_code` читает хранимый первым (t-555 F-9)

id: — | кучка: `execution-report` | от: критик t-555, F-9 (`docs/tasks/specs/reviews/t-555-s3-wave1-critic.md:138`), 31.10.2026 | приоритет: П2 | кандидат наверх: нет

## Что наблюдалось

Замер критика: после патча записи манифеста новыми `obligation_refs` без `obligation_hash` хэш остаётся прежним (`stale hash after refs patch: OLD`). `probe_by_code.obligation_fields` (`probe_by_code.py:1288`, строка :1297):
`"obligation_hash": entry.get("obligation_hash") or (content_hash(refs) if refs else None)` — хранимый хэш берётся первым, пересчёт от `refs` только когда его нет. Окно `probe` повторяет из записи четыре поля; устаревший хэш не совпадёт с
`window_record.py:886` / ссылками и даст отказ или, хуже, прикрепит доказательство к прежнему обязательству (направление — «другое/старое»). Закон EP1-38: дверь `obligation_hash` законна, пока код строит хэш от `refs`.

## Что именно менять

1. `probe_by_code.py:1297`: `"obligation_hash": (content_hash(refs) if refs else (entry.get("obligation_hash") or None))` — при наличии `refs` хэш всегда считается от них (один способ, AR-13), хранимый берётся только для записи без `refs`.
2. Писатель: `manifest_put.py` при патче `obligation_refs` пересчитывает и пишет `obligation_hash` в той же записи (один писатель, AR-14), так что хранимый хэш не расходится с `refs` и до чтения.
3. Тесты (`scripts/tests/test_probe_by_code.py`, `test_manifest_put_merge.py`): запись с `refs=A` и хэшем `hash(A)`, патч `refs=B` без хэша: `obligation_fields` отдаёт `hash(B)`; `manifest_put` после патча хранит `hash(B)`; запись без `refs` с хранимым хэшем — хэш из записи (контроль). Мутация: вернуть порядок «хранимый первым» — красит первый.
4. Узел идёт вместе с EP1-36 (он пишет `probe_by_code`); `очередь:` по общему файлу.

## Принципы и правила

P20; FR-16, FR-59; AR-13, AR-14, AR-22. Связи: EP1-38, EP1-36, t-555 F-2.

Решение владельца нужно: нет.
