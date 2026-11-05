# Установка зависимостей в клон требует `npm` на PATH машины; фабрика Node-инструментарий не определяет

id: — | кучка: `execution-report` | от: билдер CX1-4 (t-1004) по критику t-965 (Q8), 19.10.2026 | приоритет: П3 | кандидат наверх: нет

Что не так / что сделать: `sandbox_setup` вида `npm_ci` запускает `npm` (на Windows `npm.cmd`) из PATH. `project_env.py`
определяет только интерпретатор Python (класс C3-18), Node-инструментарий проекта (версия, менеджер, корень) фабрика не
находит. Если `npm` не стартует, проба получает `SetupFailed` «could not be started» (дефект машины, не свойство стенда,
D-0032) — и дальше нет двери, кроме «поставить npm». Нужно: определение Node-инструментария проекта (по `.nvmrc`,
`engines`, лок-файлу) рядом с `project_env.py`, строки таблицы `sandbox-setup.json` для yarn/pnpm — данные.

Свидетель: `scripts/red_sandbox.py` `_run_install` (`could not be started`); `scripts/project_env.py` (docstring: только
Python); `references/sandbox-setup.json`; критик `docs/tasks/specs/reviews/t-965-t-958-cx1-4-plan.md` Q8.

Принципы и правила: P2, FR-13, FR-15, FR-57.

Решение владельца нужно: нет.
