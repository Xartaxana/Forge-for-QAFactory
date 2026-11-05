# Строка данных `image/` печатает для `image/svg+xml` вызов `Read <путь> limit 1`: SVG вернётся одной строкой текста, а не картинкой

id: — | кучка: `execution-report` | от: критик диффа S6 шаги 2, 3, 1d, 1e релиза 0.10.7 (`docs/tasks/specs/reviews/r0107-s6-steps-1d-1e-diff-critic.md`, F-12), 31.10.2026 | приоритет: П3 | кандидат наверх: нет

Что не так / что сделать: данные `references/branch-accounting.json` (строка 11 на `029c57e6`) задают для медиатипа с префиксом `image/` вызов `limit_1`, и `branch_accounting` печатает роли `Read <путь> limit 1` (`by_media`, `branch_accounting.py:152`: `media.startswith(row["prefix"])`). По описанию инструмента Read картинками читаются только PNG, JPG, GIF и WEBP; `image/svg+xml` под префикс `image/` попадает, а Read вернёт его как одну строку текста (не прогонялось, выведено из текста описания инструмента, оценка критика, не замер). `.svg` по суффиксу формы вообще не имеет. Фабрика называет вызов «открытием» картинки, которого не было: направление ошибки к ложному «открыто» (FR-59; AR-28). Что сделать: сузить строку данных (закрытый список медиатипов-картинок вместо префикса `image/`, либо отдельная строка для `image/svg+xml` с формой текста), строку для `.svg` по суффиксу; закрытое разнообразие — в данных (FR-13; AR-1). Пин: `image/svg+xml` и `a.svg` не получают `limit 1`; перед правкой — один замер на настоящем Read (неизвестное свойство среды сначала меряется: `CLAUDE.md`, Command hygiene, pt. 6a).

Свидетель: `docs/tasks/specs/reviews/r0107-s6-steps-1d-1e-diff-critic.md` F-12; `git show 029c57e6:ai-packages/qa-factory/references/branch-accounting.json` строки 11-20 (`by_media`); `git grep` на `029c57e6` для `startswith(row["prefix"])` — `branch_accounting.py:152`. Ветка `029c57e6` в базе релиза не влита (на базе `3840246e` в `branch_accounting.py` есть только `startswith("image/")` в `:710`, `:801`).

Принципы и правила: P2; FR-13, FR-41, FR-59; AR-1, AR-28.

Решение владельца нужно: нет.
