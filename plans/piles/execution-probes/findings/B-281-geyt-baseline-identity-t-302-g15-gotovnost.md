# Гейт `baseline_identity` (t-302 G15) — готовность бейзлайна «советует», не решает

id: B-281 | кучка: `execution-probes` | от: новое, 03.10 — после релиза, с B-269 | приоритет: — | кандидат наверх: нет

Что не так / что сделать: **Гейт `baseline_identity` (t-302 G15) — готовность бейзлайна «советует», не решает.** `baseline_contract.validate_baseline_request`, `deployment_readiness` (advisory), ручной бейзлайн: идентичность СТАРОЙ сборки обязана быть `matched` кодом (слово человека `person_confirmed` тут не поднимает — t-300 §4, `promotable: false`), а readiness лишь советует. Сделать вместе с B-269 (бейзлайн после релиза): `refuse_with_door`. `debt_ref`. [F03]

Свидетель: t-302 R-2 G15; B-269.

Принципы и правила: FR-18, FR-58

Решение владельца нужно: нет (фраза не найдена)

<!-- piles split: plans/BACKLOG.md, раздел 7 «Релизы, приёмки, инфраструктура разработки»; ячейки строки перенесены дословно -->

Строка BACKLOG.md целиком:

```
| B-281 | **Гейт `baseline_identity` (t-302 G15) — готовность бейзлайна «советует», не решает.** `baseline_contract.validate_baseline_request`, `deployment_readiness` (advisory), ручной бейзлайн: идентичность СТАРОЙ сборки обязана быть `matched` кодом (слово человека `person_confirmed` тут не поднимает — t-300 §4, `promotable: false`), а readiness лишь советует. Сделать вместе с B-269 (бейзлайн после релиза): `refuse_with_door`. `debt_ref`. [F03] | t-302 R-2 G15; B-269. | новое, 03.10 — после релиза, с B-269 | FR-18, FR-58 |
```
