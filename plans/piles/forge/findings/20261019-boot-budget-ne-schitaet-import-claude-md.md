# Бут-бюджет не считает `@import` CLAUDE.md: PROJECT.md и индекс правил (45 КБ) грузятся в каждую сессию мимо меры

id: — | кучка: `forge` | от: Lead, диета бут-бюджета 19.10 | приоритет: П2 | кандидат наверх: нет

Что не так / что сделать: `tools/session_context.py` меряет бут-набор из шести файлов (CLAUDE.md, DECISIONS.md,
CURRENT_CONTEXT.md, README.md, DELEGATION_TABLE.md, SYSTEM_PROMPT.md; порог 100 000 байт, `CLAUDE_WARN` 56 100), но
CLAUDE.md тянет `@PROJECT.md` (39 910 байт) и `@docs/FACTORY_RULES_INDEX.md` (5 530 байт) — Claude Code вставляет их в
контекст каждой сессии. Реальная цена бута 19.10 после диеты ≈ 104 847 + 45 440 ≈ 150 КБ, а мера показывает 104 847:
порог «рост — решение, а не дрейф» не видит около трети контекста. Что сделать: мерить импорты CLAUDE.md (строки
`@<путь>`, один уровень) той же меркой и печатать их отдельной строкой («CLAUDE layer incl. imports»); порог для слоя
с импортами — решение владельца (поднять 56 100 или считать импорты в тех же 100 000).

Свидетель: `tools/session_context.py:180-206` (константы бюджета), `CLAUDE.md:7,12` (`@PROJECT.md`,
`@docs/FACTORY_RULES_INDEX.md`), `stat` 19.10: PROJECT.md 39 910, docs/FACTORY_RULES_INDEX.md 5 530; вывод
`python tools/session_context.py` 19.10 12:2x: «BOOT BUDGET: 104847 bytes / 100000 (6 files)».

Принципы и правила: CLAUDE.md «boot-context-is-expensive», скилл `boot-diet` шаг 1 (мерить и назвать, что выросло),
FR-41 (неизвестное не выдаётся за факт — здесь мера выдаёт неполное число за полное).

Решение владельца нужно: да — как считать слой CLAUDE с импортами (порог).
