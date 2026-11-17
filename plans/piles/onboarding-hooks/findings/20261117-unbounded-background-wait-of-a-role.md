# Неограниченное фоновое ожидание роли переживает роль: у гарда онбординга нет проверки цикла ожидания (спека t-1122, r2 §10 K-FIND)

id: — | кучка: `onboarding-hooks` | от: Lead, спека `docs/tasks/specs/20261117-bounded-waits-mechanism-spec-r2.md` (§10 K-FIND, F11), 17.11.2026 | приоритет: П3 | кандидат наверх: нет

## Что наблюдалось

Class: an unbounded background wait (or any background call) of a factory role outlives the role. `guard_pre_tool.py` has no wait-loop check (estimate, not read). Forge answer: t-1122 — a refusal with a paste-in capped form, and a reaper selecting by session ancestry and age. Решение владельца нужно: нет. id: —.

## Что именно менять

Направление выбрано Lead (17.11.2026, до слова владельца): прочитать `guard_pre_tool.py` (утверждение «проверки цикла ожидания нет» — оценка, не проверено чтением); если проверки нет, взять ответ кузницы t-1122 — отказ со вставляемой ограниченной формой и остановку по предку сессии и возрасту (`tools/hygiene_gate.py`, `tools/wait_reaper.py`; правило `docs/RUNBOOK.md` §9.8).

Связи: `docs/tasks/specs/20261117-bounded-waits-mechanism-spec-r2.md`, узел OH9-9 в `batch-9-perepis-podklassov-oh8-7b-h.md`.

Решение владельца нужно: нет.
