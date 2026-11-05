# `references/role-commands.json` (команда `manual_capture.py ui`) не знает режима `read <selector> state=<name>`, добавленного EP1-32

id: — | кучка: `execution-report` | от: проверка 31.10.2026 после EP1-32 (`changelog.d/execution-probes-1-ep1-32.md`), срез релиза 0.10.8 | приоритет: П3 | кандидат наверх: нет

## Что наблюдалось

`references/role-commands.json:44` (`input` команды «manual_capture.py ui», роль `qa-runner`): шаг `read` описан как `read <selector> [attr=<name>|style=<prop>|text]`. EP1-32 добавил режим `state=<name>` (`manual_capture.py:882`,
:1584: `disabled`, `enabled`, `checked`, `visible`, `editable`; данные — `references/manual-capture-steps.json`: `read.args` уже `[attr=<name> | style=<prop> | state=<name> | text]`, `read_states`). Роль читает карточку команды
(`role-commands.json`) и про `state=` не узнаёт; это второй носитель того же списка шагов (AR-13, FR-14: форма вывода и аргументов — контракт).

## Что именно менять

1. `references/role-commands.json:44`: `read <selector> [attr=<name>|style=<prop>|state=<name>|text]`. Размер файла/карточки роли — проверить лимитом (`selftest.py --limits`).
2. Тест (`scripts/tests/test_role_commands.py`): список режимов `read` в `input` команды `manual_capture.py ui` равен режимам из `manual-capture-steps.json` `steps.read.args` (разбор по форме `[a | b | c]`, не по списку слов), и каждое `read_states` из данных
   достижимо из карточки. Мутация: убрать `state=` из карточки — красит. Класс: тест сверяет карточку с данными, а не литерал с литералом — так следующий режим не отстанет.

## Принципы и правила

P1, P2; FR-14, FR-17; AR-13, AR-22. Связи: EP1-32 (`docs/tasks/specs/t-506-s4-manual-capture.md` §6).

Решение владельца нужно: нет.
