# Читатели времени: в `dispatch_liveness` их два, и дубль `_iso` рядом с `story_progress`

id: — | кучка: `onboarding-forge` | от: билдер t-971 (узел CX1-3), по критикам t-955 / t-969, 19.10.2026 | приоритет: П3 | кандидат наверх: нет

Что не так / что сделать: после CX1-3 в пакете несколько разборщиков времени с РАЗНЫМ смыслом «времени без зоны»:

- `dispatch_liveness._epoch` (без зоны = UTC; число = эпоха; зеркало `story_progress._epoch`);
- `dispatch_liveness._row_time` (новый: строка за охраной `isinstance(str)`, `codex_usage.stamp`, без зоны или число — НЕТ улики);
- `driver_session_end` и `role_stops` (`datetime.fromisoformat(...).timestamp()`, без зоны = ЛОКАЛЬНОЕ время);
- `codex_usage.stamp` (деньги: `scan` берёт им времена ответов; без зоны остаётся наивным).

Расхождение оправдано (строка роллаута Codex всегда несёт зону, а улика о времени, которому нельзя верить, ничего не
решает), но схождение в одну функцию `epoch_of(value, naive=...)` с явным аргументом «что делать с наивным» стоит
отдельного узла. Рядом: `dispatch_liveness._iso` (эпоха → `...Z`) дублирует `story_progress._iso` (эпоха → ISO со смещением) —
оба оправданы разным видом строки, но это второй рендерер; свести вместе с читателями.

Не здесь: `codex_usage.stamp` не менялся (денежный путь `scan`, M-3 критика t-955).

Свидетель: `scripts/dispatch_liveness.py` (`_epoch`, `_row_time`, `_iso`, `driver_session_end`, `role_stops`);
`scripts/story_progress.py` (`_epoch`, `_iso`); `scripts/codex_usage.py` (`stamp`).

Принципы и правила: P10, P12, FR-54.

Решение владельца нужно: нет
