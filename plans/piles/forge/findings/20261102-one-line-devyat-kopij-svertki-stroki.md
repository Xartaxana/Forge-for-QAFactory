# Свёртка текста в одну строку с обрезкой написана девять раз: нужен один выживший `contract.one_line`

id: — | кучка: `forge` | от: критик t-764 (RN1-9, Q5 и B-2 ii), `docs/tasks/handoffs/t-744-rn1-9-a.md:17-21` (расхождение 1), 02.11.2026 | приоритет: П2 | кандидат наверх: нет

## Что наблюдалось

Носитель — `ai-packages/qa-factory/scripts/`; поиск `def one_line|_one_line` (с контролем: тот же поиск находит `window_record._gap_why`). Девять членов класса:

- `window_record._gap_why` и `person_owned._one_line` — точные близнецы (обрезка по знакам, `…` входит в предел);
- `gate_brief._one_line`, `brief_pack._one_line`, `bug_records._one_line`, `blast_radius._one_line` — свёртка и обрезка;
- `traceability._one_line` — обрезка по границе слова (иное поведение);
- `detector_verdict.one_line` и `project_decisions.one_line` — только свёртка без предела (`project_decisions` ещё режет управляющие байты).

`tools/dup_ratchet.py` их не видит (каждая копия короче пяти операторов). Строки очереди в `plans/` до сих пор не было (поиск `fold-and-cut|one_line` по `plans/piles/release-next/` и `plans/BACKLOG.md` — 0 попаданий). Расхождение 1 билдера RN1-9: `contract.one_line` на дереве не существовала, билдер взял локальную копию.

## Класс

Свёртка пробелов и обрезка длины текста для строки отчёта написана в каждом модуле заново (FR-17, FR-54; AR-13, AR-15): правка предела или кодировки обязана обойти девять мест. Не правило одного модуля.

## Что именно менять

Направление выбрано (Lead пачки release-next/1, 02.11.2026): выживший — НОВАЯ `contract.one_line(text, limit=None)` с поведением `window_record._gap_why`.

1. `scripts/contract.py`: `one_line(text, limit=None)` — свернуть пробельные последовательности в один пробел, `strip`; при заданном `limit` обрезать по знакам так, чтобы `…` входило в предел (как `_gap_why`); `limit=None` — только свёртка; не-строка → `""`. Тест: `scripts/tests/` рядом с тестом `contract` — предел AT (`len == limit`, без `…`) и BEYOND (`limit + 1` → заканчивается `…`, длина `limit`), `None`, пустая строка, перевод строки и табуляция внутри.
2. Заменить вызовами `contract.one_line`: `window_record._gap_why`, `person_owned._one_line`, `gate_brief._one_line`, `brief_pack._one_line`, `bug_records._one_line`, `blast_radius._one_line`, `detector_verdict.one_line`, `project_decisions.one_line` (после `one_line` — отдельная строка про управляющие байты, она остаётся в `project_decisions`). Тест на каждую замену — существующий тест модуля без правки ожиданий (байт-в-байт тот же вывод); если вывод изменился — это расхождение, его называет билдер, а не прячет.
3. `traceability._one_line` (обрезка по границе слова) — НЕ в классе: остаётся своим поведением, но получает имя `_one_line_at_word` и ссылку на `contract.one_line` в докстринге (одна строка), чтобы поиск следующей сессии различал два поведения.
4. `tools/dup_ratchet.py --check` — 0 новых, 0 выросших; `docs/SIBLING_MAP.md`: строку оси «свёртка строки» вносит Lead.

## Принципы и правила

FR-17, FR-54; AR-13, AR-15.

## Связи

- `docs/tasks/specs/reviews/t-764-rn1-9-integration-critic.md` (Q5, B-2 ii); `docs/tasks/handoffs/t-744-rn1-9-a.md`.

Решение владельца нужно: нет.
