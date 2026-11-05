# `guard_pre_tool._shell_write_shape` ссылается на `_HEREDOC_RE`, которого нет в модуле: `NameError` на пути гарда

id: — | кучка: `onboarding-hooks` | от: замер `lint_ratchet --check` на базе `268e7608` (при разборе находки про 21 новый замечание храповика), 30.10.2026 | приоритет: П1 | кандидат наверх: да

Что не так / что сделать: `python -B tools/lint_ratchet.py --check` на `268e7608` называет `ai-packages/qa-factory/scripts/guard_pre_tool.py:1939: undefined name '_HEREDOC_RE' [UndefinedName]`. Прочитано: в `_shell_write_shape` (`:1916`) после цикла по сегментам идёт `for m in _HEREDOC_RE.finditer(command):` (`:1939`); определения `_HEREDOC_RE` в модуле нет (`grep -n _HEREDOC_RE guard_pre_tool.py` — одно вхождение; определение не найдено и в других модулях). Определение удалил коммит `ea9dbf5e` (30.10, «a heredoc or here-string body the shell only stores is text to the gate; one body scan in hooklib»: в его диффе строка `-_HEREDOC_RE = re.compile(…)`), использование осталось. Если путь достижим (команда, не вернувшая раньше `shape`), гард падает `NameError` на каждой такой команде — чем он закрыт (fail-open или сбой хука), не прослежено; тест не поймал. Не выполнялось: найдено статически (pyflakes). Что сделать: сначала один запуск `_shell_write_shape` на простой команде (подтвердить), затем перевести цикл на общий скан тела из `hooklib` (как задумывал `ea9dbf5e`) или вернуть определение; пин: команда с heredoc, исполняемым интерпретатором, и команда с heredoc, который оболочка только хранит. Тот же класс: удалённое определение — оставшееся использование (весь список lint_ratchet: `package-ci/findings/20261030-lint-ratchet-check-21-novyj-na-baze-reliza.md`).

Свидетель: `python -B tools/lint_ratchet.py --check` на `268e7608`; `ai-packages/qa-factory/scripts/guard_pre_tool.py:1939`; `git log -S_HEREDOC_RE -- ai-packages/qa-factory/scripts/guard_pre_tool.py` → `ea9dbf5e`.

Принципы и правила: P15; FR-32, FR-39; AR-9.

Решение владельца нужно: нет.
