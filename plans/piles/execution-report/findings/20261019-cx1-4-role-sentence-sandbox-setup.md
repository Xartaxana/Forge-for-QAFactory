# Роль не знает `sandbox_setup`: нужна готовая фраза для `execution-lifecycle.md` (после CX1-7)

id: — | кучка: `execution-report` | от: билдер CX1-4 (t-1004) по критику t-965 (Q9, M-8) и Lead (F-6), 19.10.2026 | приоритет: П2 | кандидат наверх: нет

Что не так / что сделать: код CX1-4 умеет ставить зависимости в клон (`sandbox_setup` в запросе красной пробы), но ни
одна роль об этом не сказана (FR-38, FR-15): справочник уровня «catches a broken product»
(`references/execution-lifecycle.md:45–52`, срезы `references/slices/qa-automator/execution-lifecycle.md`) и
`agents/qa-code-critic.md:71` молчат. Файлы принадлежат CX1-7; после неё вписать и перегенерировать срезы.

Готовая фраза для роли (английский, это пакет): «A TS/JS project's clone has no `node_modules`, so a red probe in it stops
at `MODULE_NOT_FOUND` before an assertion. Add `sandbox_setup: [{"kind": "npm_ci", "cwd": "<folder with package.json>",
"package_sha256": "<sha256 of that package.json>", "lock_sha256": "<sha256 of package-lock.json>"}]` to the red-probe
request: the factory installs from the lock inside the throwaway clone, before any mutation. The lock file must be
committed (a git-ignored file is not copied). The installs of one probe call may take up to `sandbox.install_timeout_s`
(540 s by default) and the Bash tool stops a call at 600 s: run `red_sandbox.py --probe` with a Bash timeout of 600000 ms or
in the background, and if the probe was cut off, remove the leftover clone (`<repo>-redprobe-*` next to the repository).
A kind the table does not have (yarn, pnpm) is a factory gap: probe without `sandbox_setup` and file it in
qa-factory/factory-backlog.md.»

Свидетель: `references/execution-lifecycle.md:45–52`; `agents/qa-code-critic.md:71`; критик
`docs/tasks/specs/reviews/t-965-t-958-cx1-4-plan.md` M-8, Q9.

Принципы и правила: FR-38, FR-15, FR-33.

Решение владельца нужно: нет.
