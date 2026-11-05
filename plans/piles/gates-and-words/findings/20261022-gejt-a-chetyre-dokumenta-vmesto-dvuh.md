# Гейт A называет человеку четыре документа вместо двух одобряемых: правило говорит «understanding + план», код гейта раздаёт четыре

id: — | кучка: `gates-and-words` | от: владелец, 22.10.2026 (гейт A TP1-12586 на `testproject1-dev-010`, 0.10.0) | приоритет: П2 | кандидат наверх: нет

Слово владельца 22.10.2026: вариант (а) — «кейсы — часть плана: отдельным документом их не называть, `test-plan.md` ссылается на них сам».

Что не так: сообщение гейта A: «The full brief is gate-a-brief.md. Read `understanding.md`, `test-plan.md` and `case-appendix.md` …
before you answer» — человеку названы четыре документа. Правило фабрики — два: шаблон `references/templates/understanding.md` («One of
the two documents the human gets at gate A (the other is test-plan.md)»), `skills/qa-story/phases/s4.md:77` («The working appendix is
an internal projection, not a third approval document»). А код гейта держит свой список из четырёх: `scripts/gate_brief.py:1414`
`GATE_A_DOCUMENTS = (plan test-plan.md, cases case-appendix.md, understanding understanding.md, register requirements-register.md)`,
отдаёт его дирижёру полем `documents` (`gate_brief.py:1633`), а `SKILL.md:197` «Paths first» велит начать сообщение с путей — дирижёр
перечислил что дали, добавив бриф и отбросив реестр сам. Один факт — три носителя, и человек не знает, что он одобряет.

Почему это дефект: AR-14 / AR-13 (один факт — один носитель и один читатель), AR-16 и FR-6 (текст человеку — через одну форму, P9),
FR-10 (один пакет человеку не противоречит себе: «два документа» в правиле и четыре в сообщении).

Что сделать (вариант (а) владельца): (1) одобряемых документов два — `understanding.md` и `test-plan.md`; закреплённые кейсы — часть
плана: `test-plan.md` сам ссылается на кейсы (строка плана → id кейса со ссылкой на файл кейса), `case-appendix.md` остаётся внутренней
проекцией для ролей и критика и человеку отдельным документом не называется; (2) список одобряемых документов — один носитель (данные,
не кортеж в `gate_brief.py`; его читают `gate_brief.py`, шаблоны, `s4.md`, `SKILL.md`), `requirements-register.md` и `case-appendix.md` —
не в нём; бриф гейта — сводка, не документ на одобрение; (3) первая строка сообщения гейта A — «одобрите: understanding.md, test-plan.md»
и ссылка на бриф; строит её код, не дирижёр (AR-16); (4) тест: сообщение гейта A называет ровно два документа на одобрение, а в
`test-plan.md` у каждой строки с кейсами есть ссылка на кейс; (5) сиблинг — гейт B (`phases/s8.md`, `gate_brief.py:2902` «the two
documents behind it»): тот же вопрос «что человек одобряет», тот же носитель.

Свидетель: скриншот владельца 22.10 (сообщение гейта A TP1-12586); `scripts/gate_brief.py:1414-1435`, `:1633`;
`skills/qa-story/phases/s4.md:77`; `references/templates/understanding.md:3-5`; `skills/qa-story/SKILL.md:197`.

Принципы и правила: P9, FR-6, FR-10, AR-13, AR-14, AR-16.

Решение владельца нужно: нет (дано 22.10.2026, вариант (а)).
