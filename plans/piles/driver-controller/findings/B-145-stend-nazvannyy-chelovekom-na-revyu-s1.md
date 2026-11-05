# Стенд, названный человеком на ревью S1 («name another stand here», story_run.py:1274-1276), в…

id: B-145 | кучка: `driver-controller` | от: новое, 29.09; → t-303 (черновик: «decided at N6») | приоритет: — | кандидат наверх: нет

Что не так / что сделать: Стенд, названный человеком на ревью S1 («name another stand here», story_run.py:1274-1276), в режиме драйвера уходит только в `record_review` → `ticket_adapter review --record` (:1243-1256) и не доходит до `pipeline.environment`; человека спросят снова на S5 (FR-8). Тот же разрыв у старой строки «Which stand do I test on». Было до D2.

Свидетель: Критик t-037, F8.

Принципы и правила: FR-8, FR-7

Решение владельца нужно: нет (фраза не найдена)

<!-- piles split: plans/BACKLOG.md, раздел 7 «Релизы, приёмки, инфраструктура разработки»; ячейки строки перенесены дословно -->

Строка BACKLOG.md целиком:

```
| B-145 | Стенд, названный человеком на ревью S1 («name another stand here», story_run.py:1274-1276), в режиме драйвера уходит только в `record_review` → `ticket_adapter review --record` (:1243-1256) и не доходит до `pipeline.environment`; человека спросят снова на S5 (FR-8). Тот же разрыв у старой строки «Which stand do I test on». Было до D2. | Критик t-037, F8. | новое, 29.09; → t-303 (черновик: «decided at N6») | FR-8, FR-7 |
```
