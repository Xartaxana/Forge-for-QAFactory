# Один публичный `runtime_paths.project_relative` вместо частных относителей пути в шести местах

id: — | кучка: `driver-hosts` | от: критик t-1308 (SC1-9/10, F9), решение Lead 27.10.2026 | приоритет: П3 | кандидат наверх: нет

Что не так / что сделать: пачка SC1-9/10 добавила ещё два частных относителя пути: `ticket_adapter._summary_path` (`ticket_adapter.py:1984`, резолвит по живой файловой системе) и `context_bundle._show_path` (то же плюс семантика указателя). В пакете уже есть: `runtime_paths._rest_under` / `contained` (`runtime_paths.py:386-424`, ось 8 «один предикат вложенности»), `case_versions.portable_source_path` (:56), `probe_by_code._rel_project` (:2020), `repo_map._rel` (:193), `project_env._rel` (:104). Что сделать: один публичный `runtime_paths.project_relative(path, project) -> str | None` на основе `_rest_under`, близнецы сводятся в него (направление ошибки сегодня «как дано», не блокирует). До сведения ось 8 требует записать `_summary_path` как близнеца по живой файловой системе. Ключ: один тест на `project_relative` (внутри, снаружи, симлинк, не существует), мутант в любом из свёрнутых мест краснеет.

Свидетель: `docs/tasks/specs/reviews/t-1308-sc1-9-10-diff-review.md`, раздел F9; решение Lead — «F9 ... находками» в конце спеки `docs/tasks/specs/t-1252-sc1-9-10-role-diet.md`; `docs/tasks/handoffs/t-1313-sc1-9-10-fix-round.md` («Other private relativisers (F9) ... queued by the Lead»).

Принципы и правила: FR-54, FR-17, AR-4, AR-13, AR-15.

Решение владельца нужно: нет.
