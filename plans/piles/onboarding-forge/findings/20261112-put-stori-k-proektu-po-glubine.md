# Проект выводится из папки стори фиксированной глубиной `parents[2]` — при настроенном `artifact_root` это другая папка

id: — | кучка: `onboarding-forge` | от: критик t-172 d-1, `docs/tasks/specs/reviews/t-172-of3-1-bde-diff.md` (предложенный узел OF3-1d3), 12.11.2026 | приоритет: П3 | кандидат наверх: нет

## Что наблюдалось

`scripts/walk_timing.py:172` (`project_root = Path(task_root).parents[2]`) и `:241` (`hooklib.read_json(task_root.parents[2] / "qa-factory/…")`), `scripts/gate_brief.py:2303` (`project = task_root.parents[2]`) — проект берётся глубиной, верной только для `<project>/qa-factory/artifacts/<T>`.
При `artifact_root: "stories"` (настроенном) `parents[2]` — не проект: конфиг читается из чужой папки, тайминги и бриф врут. Узел OF3-1 d сделал это для `vcs_evidence`, `local_keys`, `role_load` (`runtime_paths.project_for_task`); эти три места остались (до d так же вели себя уже на main).
Проверено на main: три строки выше есть (grep `parents\[2\]`).

## Что именно менять

1. `scripts/walk_timing.py` (:172, :241) и `scripts/gate_brief.py` (:2303): `runtime_paths.project_for_task(task_root)` вместо `.parents[2]`; ошибка функции («не нашла проект») — как ловит вызывающий в этом месте (читатель — «неизвестно» / пусто, не traceback).
2. Тест: таблица случаев в тестах этих модулей (`test_walk_timing*.py`, `test_gate_brief*.py` — назвать в спеке) — корень по умолчанию и `artifact_root: stories`: тот же проект, тот же конфиг.
3. `gate_brief.py` — файл потока hooks (взятая пачка `onboarding-hooks/4`): узел идёт после её слияния (`очередь: onboarding-hooks/4 → onboarding-forge/4`).

Принципы и правила: FR-54; AR-4, AR-13, AR-15.

Решение владельца нужно: нет.
