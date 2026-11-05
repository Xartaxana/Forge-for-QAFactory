# Список git-хуков и его копии в `tools/` (критик t-400 на t-390)

id: B-300 | кучка: `package-ci` | от: новое, 03.10 — малый пакет | приоритет: — | кандидат наверх: нет

Что не так / что сделать: **Список git-хуков и его копии в `tools/` (критик t-400 на t-390):** (а) F1 — `session_context.py:1009` докстринг «both required hook files», их три; (б) F2 — `test_wiring_check.py` читает ожидания из самого `wiring_check._REQUIRED_GITHOOKS`: выпадение `pre-merge-commit` из списка оставит всё зелёным — нужен один пин списка против отслеживаемых файлов `.githooks/`; комментарий у :135 «for each hook in turn» проверяет только последний; (в) F3 — `test_mechanism_gate.py:1252-1253, 1340-1341` знает только `pre-commit` и `commit-msg`; (г) F4 — `agents_md.py:249` текст «pre-commit and commit-msg gates» устарел с 6ba43b6; (д) F5 — стеночные пороги времени в `test_md_regions:564`, `test_witness_echo:652/671`, `test_critic_verdict_check:508` не измерены под нагрузкой; (е) F6 — в `docs/SIBLING_MAP.md` нет оси «набор зарегистрированных хуков ↔ каждый список, который его копирует» (`wiring_check`, `session_context`, CASES пробы, `MECHANISM_PREFIXES`, `test_mechanism_gate`) — решение Lead. Одним малым пакетом билдеру. [F15]

Свидетель: Критик t-400, 03.10.

Принципы и правила: правило 9 `CLAUDE.md`

Решение владельца нужно: нет (фраза не найдена)

<!-- piles split: plans/BACKLOG.md, раздел 7 «Релизы, приёмки, инфраструктура разработки»; ячейки строки перенесены дословно -->

Строка BACKLOG.md целиком:

```
| B-300 | **Список git-хуков и его копии в `tools/` (критик t-400 на t-390):** (а) F1 — `session_context.py:1009` докстринг «both required hook files», их три; (б) F2 — `test_wiring_check.py` читает ожидания из самого `wiring_check._REQUIRED_GITHOOKS`: выпадение `pre-merge-commit` из списка оставит всё зелёным — нужен один пин списка против отслеживаемых файлов `.githooks/`; комментарий у :135 «for each hook in turn» проверяет только последний; (в) F3 — `test_mechanism_gate.py:1252-1253, 1340-1341` знает только `pre-commit` и `commit-msg`; (г) F4 — `agents_md.py:249` текст «pre-commit and commit-msg gates» устарел с 6ba43b6; (д) F5 — стеночные пороги времени в `test_md_regions:564`, `test_witness_echo:652/671`, `test_critic_verdict_check:508` не измерены под нагрузкой; (е) F6 — в `docs/SIBLING_MAP.md` нет оси «набор зарегистрированных хуков ↔ каждый список, который его копирует» (`wiring_check`, `session_context`, CASES пробы, `MECHANISM_PREFIXES`, `test_mechanism_gate`) — решение Lead. Одним малым пакетом билдеру. [F15] | Критик t-400, 03.10. | новое, 03.10 — малый пакет | правило 9 `CLAUDE.md` |
```
