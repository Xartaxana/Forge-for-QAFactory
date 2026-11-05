# Регрессия повторяет запуски: файл в трёх командах, каталог рядом с его файлами

id: — | кучка: `regression` | от: прогон TP1-12586 на 0.10.5, 29.10.2026 (владелец, 30.10.2026: «создавай кучку починки регрессии») | приоритет: П1 | кандидат наверх: нет

Что не так / что сделать: список регрессии прогона 12586 запускает одно и то же несколько раз. `test_integration_update.py` стоит в трёх
командах (blast:B-7, blast:B-9, и внутри каталога B-8), `test_edit_integration.py` — в двух (B-3, B-5). Команда B-8 запускает целые
каталоги `tests/integrations` и `tests/projects`, и они уже покрывают большинство остальных пунктов. Человек, прогоняющий регрессию на
своей машине, ждёт те же тесты по нескольку раз. Нужно: одна исполнимая команда, файлы без повторов, файл, покрытый перечисленным
каталогом, из списка убран (P24 «одна команда без повторов»); подписи пунктов (`blast:B-n`) сохраняются при сжатии.

Свидетель: `testproject1-dev-010/testproject1-sdk/test-harness/qa-factory/artifacts/TP1-12586/test-report.md:72-78` (блок `facts:regression`); те же
блоки в `archive/testproject1-dev-010-run-12586-20261028/worktree-untracked/test-harness/qa-factory/artifacts/TP1-12586/test-report.md`.
Производители: `scripts/delivery_verdict.py` (`regression_lines`), `scripts/report_facts.py` (`_regression`, `_r_regression`),
`scripts/check_delivery.py` (`regression_record`); роль — `agents/qa-test-strategist.md` п. 6.

Принципы и правила: P24; P2; FR-47 (код — инструмент роли), FR-14.

Решение владельца нужно: нет.
