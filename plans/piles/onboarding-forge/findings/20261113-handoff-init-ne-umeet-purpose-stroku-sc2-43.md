# Строка контракта с `purpose` не получается через `handoff_init`: у него нет аргумента `--purpose` (хвост SC2-43)

id: — | кучка: `onboarding-forge` | от: Lead, хвост SC2-43 (t-253), 13.11.2026 | приоритет: П3 | кандидат наверх: нет

Кучка выбрана потому, что `scripts/handoff_init.py` и узел SC2-43 (та же дверь `handoff_init`, перенесён в `onboarding-forge/1`) живут здесь. Дубль не найден: единственная находка про `handoff_init` — `findings/20261030-dver-handoff-init-pechataet-flagi-bez-to-dlya-stadii-s-dvumya-kontraktami.md` (про `--to`, не про `purpose`).

## Что наблюдалось

1. `handoff.contract_of(stage, role, to_role="", purpose="")` (`scripts/handoff.py:354`) умеет искать строку контракта по `purpose` (строка S5-плана, `s5_plan`; совпадает ТОЛЬКО с запросом с тем же purpose, `handoff.py:362-372`).
2. `scripts/handoff_init.py` аргумента `--purpose` не имеет: аргументы — `handoff_init.py:381-398` (`--task --stage --role --to --dispatch --scope --contract --task-root --out --force --carry-from --rows --author-dispatch`); вызов поиска — `handoff_init.py:407`: `handoff.contract_of(args.stage, args.role, args.to)` — без purpose. Проверка: `grep -ni purpose scripts/handoff_init.py` — 0 строк.
3. Итог: форму для контракта со строкой `purpose` можно получить только обходом `--contract <имя>` (его вызывают тесты, `test_story_step_s5_plan.py:112`); поиск по стадии/роли/`--to` такую строку никогда не вернёт. Поле контракта (`purpose` строки) без инструмента, который его производит (FR-11); роли, которой дали «используй `handoff_init`», нечем сказать «это план S5».

## Что именно менять

Направление выбрано (по рекомендации, до слова владельца): добавить `--purpose` (по умолчанию пусто, значение — строка без пробелов) в `handoff_init.main` и передать его `handoff.contract_of(args.stage, args.role, args.to, args.purpose)`.

1. Пусто — поведение не меняется: обычная строка стадии, строка с `purpose` НЕ возвращается (инвариант `handoff.py:362-364`).
2. Неизвестный purpose (нет строки, называющей его) — отказ в духе «no contract for …» с названием запрошенного purpose и списком известных (FR-1, FR-2): не молчаливый откат на обычную строку.
3. `--contract` по-прежнему главнее поиска (переопределение).
4. Дверь отказа `handoff_init` (SC2-43/SC2-42) печатает `--purpose`, когда нужная строка найдена по нему, так же как `--to`.

## Тест

`scripts/tests/test_handoff_init.py`, таблица: (stage S5, role, purpose `s5_plan`) → контракт плана; (то же без purpose) → обычный контракт стадии; (purpose `no_such`) → отказ с именем; (`--contract` + purpose) → побеждает `--contract`; (purpose с пробелом) → отказ. Мутация: убрать передачу `args.purpose` в `contract_of` — красит первую строку.

## Принципы и правила

FR-11, FR-1, FR-2, FR-15; AR-9, AR-22 (поле читается — должен быть производитель). Связи: SC2-43 (`findings/20261030-dver-handoff-init-pechataet-flagi-bez-to-dlya-stadii-s-dvumya-kontraktami.md`), `scripts/handoff.py`, `scripts/tests/test_story_step_s5_plan.py`.

Решение владельца нужно: нет.
