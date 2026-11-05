# `test_brief_pack_roles` красный на базе релиза: K9 (устав называет `branch_accounting.py`, которого нет в карточке) и K6 (хэш `## Commands` у `qa-automator`)

id: — | кучка: `package-ci` | от: билдер GW1-16 и критик S1c релиза 0.10.7 (`docs/tasks/handoffs/r0107-s1c-gw1-16.md:41`, `docs/tasks/specs/reviews/r0107-s1c-diff-critic.md:110-112`), замер на базе `268e7608`, 30.10.2026 | приоритет: П2 | кандидат наверх: нет

Что не так / что сделать: `python -B ai-packages/qa-factory/scripts/tests/test_brief_pack_roles.py` на `268e7608`: `FAIL K6 qa-automator: its ## Commands section is today's text — expected 'c49475e3787857bf', got 'c9b19f04922a1438'`; `FAIL K9 qa-requirements-tester: every script its charter names through the plugin root is on its card — expected [], got ['branch_accounting.py']`; `=== test_brief_pack_roles: 165/167 ok ===`. K9: `agents/qa-requirements-tester.md:48` и `:78` называют `branch_accounting.py` (картинки), а `brief_pack.py` его не знает (0 вхождений); строка пришла с OH3-15 (`fbc9f38b`), до диапазона S1c. K6: хэш раздела `## Commands` карточки роли разошёлся с зафиксированным; кто менял — не прослежено (критик S1c: `brief_pack.py` в диапазоне менял только S4). Красный тест идёт мимо узлов, каждый билдер пишет «до меня» и идёт дальше (FR-34: красный тест против требования — баг, не блокер). Что сделать: K9 — добавить скрипт в карточку роли (если роль вправе его звать, P14) или убрать из устава; K6 — перепинить хэш после прочтения диффа раздела, не по собственному выводу. Пин: оба зелёные; комментарий-дверь у хэша K6 (куда смотреть при правке `## Commands`).

Свидетель: вывод `FAIL K6`/`FAIL K9` выше (прогон на `268e7608`); `git grep branch_accounting HEAD -- agents scripts/brief_pack.py` находит только `agents/qa-requirements-tester.md` (билдер GW1-16).

Принципы и правила: P14; FR-34, FR-56, FR-15; AR-8, AR-11.

Решение владельца нужно: нет.
