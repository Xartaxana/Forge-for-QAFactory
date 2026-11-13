# Команды `manual_evidence.py validate` нет в `references/role-commands.json`; тест RC1-10 закрепляет дыру как норму

id: — | кучка: `onboarding-forge` | от: критик t-223 (R3, ревью RC1-10), 13.11.2026 | приоритет: П3 | кандидат наверх: нет

## Что наблюдалось

`references/manual-evidence.md:122` отдаёт роли команду `manual_evidence.py validate --task-root <T> --input <record.json>`, но в реестре `references/role-commands.json` карточки
`manual_evidence.py validate` нет (критик t-223 перечислил ключи реестра). Тест RC1-10 «нет карточки» использует именно эту команду, поэтому проходит из-за отсутствия карточки;
docstring `role_cli.py` обещает обратное («тест называет дыру»). Когда карточку заведут, строка покраснеет не по той причине. Та же форма у `artifact_producer.py validate` (риск ниже: подкоманду не зовёт ни один агент или скилл).

## Что именно менять

Направление выбрано: карточка заводится, строки «нет карточки» переезжают на синтетическую команду.
1. `references/role-commands.json`: карточка `manual_evidence.py validate` с примером (`--task-root`, `--input`). Тест: тест реестра — у каждой команды из `references/manual-evidence.md` есть карточка.
2. Тест RC1-10 «нет карточки» (`scripts/tests/`, файл RC1-10): строка берёт синтетическую незарегистрированную команду (`RefusingParser(command="no_such_command.py")`, `parse_args([])` в процессе), для `manual_evidence.py validate` и `artifact_producer.py validate` — тоже синтетическая строка. Тест: строки зелёные до и после добавления карточки.

Связи: RC1-10. Принципы и правила: FR-11, FR-15; AR-8, AR-22.

Решение владельца нужно: нет.
