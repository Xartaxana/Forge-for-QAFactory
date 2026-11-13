# Отказы `check_override` и `rewritten_input` получают `note_denial` в OH6-4, но без строки реестра A24

id: — | кучка: `onboarding-hooks` | от: спека t-263 (§B, F-6), 13.11.2026 | приоритет: П3 | кандидат наверх: нет

## Что наблюдалось

`inject_context.dispatch` превращает два `ValueError` в отказ без строки реестра:
- `check_override` (броски: `codex_roles.py:49`, `:61`; ловит `inject_context.py:650-652`, только Codex): «Native Codex role missing…» и
  «Native <role> <key> mismatch…»;
- `rewritten_input` (броски: `host_adapter.py:247` и соседние `:80`, `:171`, `:185`; ловит `inject_context.py:716-718`, все хосты).

OH6-4 (спека t-263, F-6 (a)) даёт обоим `note_denial` и строки таблицы B-8/B-9. Строки A24 (`refusal_registry.py`) у них нет: проверка
A24 читает только модули из `SCANNED`, а сами `raise` лежат в `codex_roles.py` и `host_adapter.py` — вне списка.

## Что именно менять

Направление выбрано (форма D спеки t-263 §B.0: регистрировать места броска там, где они есть, не оборачивать). Порядок: после OH6-4.
1. `refusal_registry.SCANNED` получает `codex_roles.py` и `host_adapter.py`. Остальные `ValueError` этих файлов (`codex_roles.py:35`,
   `host_adapter.py:80/171/185/240`) перечисляются в узле: каждый либо получает строку, либо явную пометку «не отказ диспатча — почему».
2. Строки A24 ключуются буквальными текстами `raise` (как три строки `native_context.stage` в OH6-4); ничего не оборачивается.
3. Тест: в `test_doctor_context.py` (как C-B1 спеки) — каждый из двух отказов имеет строку реестра; мутация «убрать строку» красит.

## Принципы и правила

P31, P15; FR-1; AR-18. Связи: t-263 (F-6), OH6-4.

Решение владельца нужно: нет.
