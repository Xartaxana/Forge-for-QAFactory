# К B-319 (`artifact_root`): форма `traceability.py --task-root <dir>` берёт корень багов как…

id: B-348 | кучка: `report-delivery` | от: критик t-068 | приоритет: — | кандидат наверх: нет

Что не так / что сделать: К B-319 (`artifact_root`): форма `traceability.py --task-root <dir>` берёт корень багов как `parents[1]`, а форма `--task <T>` — `<project>/qa-factory`; при настроенном `artifact_root` они читают разные папки. Боевых вызовов `--task-root` нет (`story_step`, `s9.md`, текст писца — через `--task`); тесты и один отказ на неё опирались (отказ переведён на `--task` в волне 4). Свести на одно правило. [F08]

Свидетель: Критик W4-R (t-068), проба с `artifact_root: qa-artifacts`: `--task` — 1 confirmed, `--task-root` — none.

Принципы и правила: FR-17, FR-37

Решение владельца нужно: нет (фраза не найдена)

<!-- piles split: plans/BACKLOG.md, раздел 12 «Миграция исправлений из legacy-прогона TP2-2406»; ячейки строки перенесены дословно -->

Строка BACKLOG.md целиком:

```
| B-348 | К B-319 (`artifact_root`): форма `traceability.py --task-root <dir>` берёт корень багов как `parents[1]`, а форма `--task <T>` — `<project>/qa-factory`; при настроенном `artifact_root` они читают разные папки. Боевых вызовов `--task-root` нет (`story_step`, `s9.md`, текст писца — через `--task`); тесты и один отказ на неё опирались (отказ переведён на `--task` в волне 4). Свести на одно правило. [F08] | Критик W4-R (t-068), проба с `artifact_root: qa-artifacts`: `--task` — 1 confirmed, `--task-root` — none. | критик t-068 | FR-17, FR-37 |
```
