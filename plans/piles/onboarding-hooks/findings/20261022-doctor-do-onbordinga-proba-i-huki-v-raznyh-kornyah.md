# Доктор до онбординга во вложенном проекте: проба гарда и хуки смотрят в разные корни, доктор объявляет хуки неактивными

id: — | кучка: `onboarding-hooks` | от: владелец, 22.10.2026 (первый `/qa-factory:qa-doctor` на чистой копии с 0.10.0) | приоритет: П2 | кандидат наверх: нет

Что не так: копия `testproject1-dev-fresh/testproject1-sdk-fresh010` (git worktree свежего `main` testproject1-sdk), проект — подпапка `test-harness`,
онбординга ещё не было (нет `qa-factory/config.json`). Доктор, шаг 1b: `host_probe.py --prepare` → эхо ALLOW и DENY → `--check`;
DENY исполнилось, `--check` вернул `status: unverified`, и доктор сказал человеку «Hooks look inactive in this session». Хуки при этом
работали: в транскрипте той же сессии `stop_hook_summary` с четырьмя хуками плагина, хук стоимости создал
`test-harness/qa-factory/state/cost/.writers/<session>/`.

Причина: `host_probe.py` — CLI без `CLAUDE_PROJECT_DIR`; `hooklib.project_root()` не находит маркер `qa-factory/config.json` (онбординга
нет) и падает на `git rev-parse --show-toplevel` = корень монорепозитория. Проба записала nonce в
`testproject1-sdk-fresh010/qa-factory/state/host-probe.json` (её вывод: `"root": "...testproject1-sdk-fresh010"`), а хуки идут с
`CLAUDE_PROJECT_DIR=test-harness` и nonce не видят: DENY не отказан, квитанций нет. Тот же откат положил `host-probe.json` в
`qa-factory/state/` корня монорепозитория. (Уточнение 22.10: `journal.jsonl` и `factory-dashboard.html` рядом с ним — не от отката, они
закоммичены в testproject1-sdk `main` ещё в TP1-14336, коммит 98f01299, 16.09 — след того самого инцидента.) Класс — TP1-14336
(docstring `hooklib.project_root`) на ветке «ещё не онбордили», где маркера нет ни у кого.

Что сделать (форма — спеке): (1) проба не создаёт хранилище там, куда хуки не посмотрят: корень пробы до онбординга берётся тем же
путём, что у хуков (cwd сессии, где открыт проект), либо проба честно отказывает «до онбординга гард не проверить» — без записи в
корень репозитория; (2) доктор при `root` пробы ≠ корню, который видят хуки, или при отсутствии `config.json` не пишет «хуки неактивны»:
строка `unknown / owner: factory` с фактом (FR-41, FR-59), следующий шаг — онбординг; (3) сиблинги по `docs/SIBLING_MAP.md` — все CLI,
которые резолвят корень до онбординга (`activity_capture.py`, дашборд, `install_smoke --report`), и куда они пишут.

Свидетель: транскрипт `~/.claude/projects/D--ws-testproject1-dev-fresh-testproject1-sdk-fresh010-test-harness/8cc24072-….jsonl`
(вывод `--prepare` с `root`/`store`, вывод `--check`, `stop_hook_summary`); файлы `testproject1-sdk-fresh010/qa-factory/state/` против
`testproject1-sdk-fresh010/test-harness/qa-factory/state/` (22.10 11:34). Код: `scripts/host_probe.py` `main` (`root = args.root or project_root()`),
`scripts/hooklib.py` `project_root` (откат на `--show-toplevel`).

Принципы и правила: FR-41, FR-59, FR-17, AR-4, AR-28, AR-13.

Решение владельца нужно: нет.
