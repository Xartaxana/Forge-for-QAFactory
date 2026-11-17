# FR-59: один предикат `acceptable` для сайтов приёма записи

id: — | кучка: `rules-debt` | от: спека карточек фазы 2 (`docs/tasks/specs/20261117-rules-debt-phase2-cards-spec.md`), 17.11.2026 | приоритет: П1 | кандидат наверх: нет

Что не так / что сделать: Реестр требует, чтобы `accept`-сайт преобразованной строки звал функцию `acceptable` (`gate_registry.py:837-841`), а такой функции нет: `gate_template.py` не существует, есть только `profile_contract.acceptable_provenance`. Класс: общий механизм, без которого строки с сайтом приёма не переводятся в `converted` честно (AR-28).

Что именно менять: `scripts/gate_template.py` (новый): `acceptable(record, consumer)`; неизвестный потребитель, нет записи, слово вне `words`, нечитаемый реестр → False. Входы, которые остаются «не принято»: `person_confirmed` под строкой `promotable: false`; `not_applicable` без кода причины, где `accepts` называет только `not_applicable:<reason>`; слово другого регистра (`Matched`); список или словарь вместо слова. Тест — строки таблицы `test_gate_registry.py` (файл медленный: судит канон). Объём узла (какие сайты ему нужны) — решение плана; не диспатчить без критика на план (новый общий механизм).

Карточка: `docs/tasks/specs/20261117-rules-debt-phase2-cards-spec.md`, карточка C3-0 — читать там, не копировать сюда.

Свидетель: `docs/tasks/specs/20261117-rules-debt-phase2-cards-spec.md` §0 п. 1; `gate_registry.py:234-237,837-841`; `profile_contract.py:895`.

Принципы и правила: FR-59, FR-17; AR-28, AR-29.

Решение владельца нужно: нет.
