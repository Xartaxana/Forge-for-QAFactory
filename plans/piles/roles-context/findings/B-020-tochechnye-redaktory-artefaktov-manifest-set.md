# Точечные редакторы артефактов: `manifest_set` для `context-manifest.json`, посекционные для…

id: B-020 | кучка: `roles-context` | от: PLAN-after-run4 P12, P17 | приоритет: — | кандидат наверх: нет

перенос: speed-cost/batch-1 (узел SC1-2; слово владельца 26.10.2026)

Что не так / что сделать: Точечные редакторы артефактов: `manifest_set` для `context-manifest.json`, посекционные для `requirements-register.md`, `understanding.md`, `test-report.md`, `critic-findings.md`; `config_view --keys`, `source_view --section`. Роль вызывает сама и решает сама. Критерий: у скаута ни одного `_patch*.py`, трейсбека, отказа хука.

Свидетель: Скаут S1: 224 хода, 20 % — питон-патчеры манифеста, 11 самописных скриптов, 12 трейсбеков; около 40 % ходов скаута — подбор формы обращения к нашему коду; tester пишет register 26 раз; стратег переписал test-plan.json 59 раз.

Принципы и правила: P1, P11, P12

Решение владельца нужно: нет (фраза не найдена)

<!-- piles split: plans/BACKLOG.md, раздел 2 «Трение кода о роль»; ячейки строки перенесены дословно -->

Строка BACKLOG.md целиком:

```
| B-020 | Точечные редакторы артефактов: `manifest_set` для `context-manifest.json`, посекционные для `requirements-register.md`, `understanding.md`, `test-report.md`, `critic-findings.md`; `config_view --keys`, `source_view --section`. Роль вызывает сама и решает сама. Критерий: у скаута ни одного `_patch*.py`, трейсбека, отказа хука. | Скаут S1: 224 хода, 20 % — питон-патчеры манифеста, 11 самописных скриптов, 12 трейсбеков; около 40 % ходов скаута — подбор формы обращения к нашему коду; tester пишет register 26 раз; стратег переписал test-plan.json 59 раз. | PLAN-after-run4 P12, P17 | P1, P11, P12 |
```
