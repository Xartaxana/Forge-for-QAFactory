# `tools/test_quarantine.py`: в тексте отказа «or or», а дверь `quarantine-edit:` принимает только голое имя файла и отказ этого не говорит

id: — | кучка: `onboarding-forge` | от: наблюдение Lead 12.11.2026 (снимок `docs/tasks/compact-snapshots/2026-11-12-2032-narrative.md`, строка «test_quarantine: «or or»…») | приоритет: П3 | кандидат наверх: нет

## Что наблюдалось (проверено чтением main)

1. `tools/test_quarantine.py` :1753 — `_say(f"quarantine check: {sha[:8]}: {text}; or {_ACCEPT}")`, а `_ACCEPT` (:1522) = `'or a later commit line "quarantine-accept: <sha> -- <reason>"'` уже начинается с «or»: в выводе «…; or or a later commit line…».
2. Дверь `quarantine-edit:` — `_DOORS["edit"]` :1515 = `^quarantine-edit:\s*(\S+)\s*--\s*\S`, сверка `n in _DOORS["edit"].findall(msg)` (:1631, :1692) — `n` это ГОЛОЕ имя файла из раздела `quarantine` (без `scripts/tests/`). Строка с путём (`scripts/tests/test_x.py`) не совпадёт, а отказ (:1632, :1694) пишет только «expected a line 'quarantine-edit: {n} -- <reason>'» с самим `n` и не говорит, что нужно голое имя без папки — человек, поправивший путь «для ясности», получает тот же отказ (FR-1: ожидаемое названо не полностью).

## Что именно менять

1. `tools/test_quarantine.py` :1753 — убрать лишнее «or»: `f"…: {text}; {_ACCEPT}"` (константа несёт союз).
2. Тексты отказа :1632 и :1694 (общая константа, одно написание): «…expected a line 'quarantine-edit: {n} -- <reason>' (the bare file name, no folder) in this commit message».
3. Тест: `tools/test_test_quarantine.py` — строка таблицы: вывод `check` не содержит «or or»; отказ про изменённый файл содержит «bare file name».

Принципы и правила: FR-1, FR-2; AR-9.

Решение владельца нужно: нет.
