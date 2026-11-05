# Соседи B-194: самодекларации без проверки на других стадиях — `s7-automator-to-analyst.yaml:65`…

id: B-218 | кучка: `report-delivery` | от: новое, 30.09 | приоритет: — | кандидат наверх: нет

Что не так / что сделать: Соседи B-194: самодекларации без проверки на других стадиях — `s7-automator-to-analyst.yaml:65` `then_lines_unchanged`, `s7-analyst-to-scribe.yaml:106` `no_expectation_was_adjusted_to_the_code`, `s5-automator-to-runner.yaml:89`; ещё три claim'а S5 без верификатора (`s5-automator-to-critic.yaml:74,76,78`), при том что комментарий :71-72 обещает «каждый ключ проверяется кодом» (верификаторов 5: `handoff_check.py:403-409`); `tests[].critic_verdict` может записать любая роль; `self_fixes[].why_test_defect` проверяется только на наличие. Красный на S6 → зелёный на S7 должен получить ту же проверку, что B-194 даёт S5.

Свидетель: Проектировщик t-108, раздел «Siblings».

Принципы и правила: FR-17, FR-54, FR-18

Решение владельца нужно: нет (фраза не найдена)

<!-- piles split: plans/BACKLOG.md, раздел 7 «Релизы, приёмки, инфраструктура разработки»; ячейки строки перенесены дословно -->

Строка BACKLOG.md целиком:

```
| B-218 | Соседи B-194: самодекларации без проверки на других стадиях — `s7-automator-to-analyst.yaml:65` `then_lines_unchanged`, `s7-analyst-to-scribe.yaml:106` `no_expectation_was_adjusted_to_the_code`, `s5-automator-to-runner.yaml:89`; ещё три claim'а S5 без верификатора (`s5-automator-to-critic.yaml:74,76,78`), при том что комментарий :71-72 обещает «каждый ключ проверяется кодом» (верификаторов 5: `handoff_check.py:403-409`); `tests[].critic_verdict` может записать любая роль; `self_fixes[].why_test_defect` проверяется только на наличие. Красный на S6 → зелёный на S7 должен получить ту же проверку, что B-194 даёт S5. | Проектировщик t-108, раздел «Siblings». | новое, 30.09 | FR-17, FR-54, FR-18 |
```
