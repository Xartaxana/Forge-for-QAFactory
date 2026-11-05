# `run_suite.py main`: при вызове `--mine` восемь выходов не печатают строку `PHASES` (ответы `reused`/`already_run` и отказы)

id: — | кучка: `execution-report` | от: F7 критика S2b (`docs/tasks/specs/reports/r0107-s2b-fix.md`, строка 47) и отчёт `docs/tasks/specs/reports/r0107-s2b-b1.md` (строка 27), `docs/tasks/release-0.10.7.md:226`, `:254`, 01.11.2026 | приоритет: П3 | кандидат наверх: нет

## Что наблюдалось

`scripts/run_suite.py`: после `mine()` в `main` выходы вызова `--mine` не печатают строку `PHASES` (AK4 SC2-37): ответы `:2494`, `:2517-18`, `:2547-48`; отказы `:2491`, `:2498`, `:2521`, `:2545`;
`refuse_missing_executor` `:2526`; плюс `run` `:1787` (номера критика, дерево до фикс-раунда). Ещё два выхода `store.begin` (повтор/переиспользование) вызывают `print_not_launched(action, job, brief=bool(args.mine))`.
`main` — не-цель SC2-37 (владелец S2.03); строка нужна однострочным вызовом `_say_mine_phases(args.phase_clock)`.

## Что именно менять

1. `scripts/run_suite.py`, `main`: каждый выход `--mine` вызывает `_say_mine_phases(args.phase_clock)` до печати (stderr, как в B1); общая обёртка вместо правки каждого выхода (AR-15).
2. Тест (`scripts/tests/test_run_suite_mine.py`): по ключу на каждый класс выхода (ответ reused, already_run, отказ, missing_executor, `store.begin`) — в stderr есть `PHASES:`, в stdout нет (AK2).
   Мутация: убрать вызов в одном выходе — красит ключ этого класса.
3. Время фаз в тесте не мерить часами (см. `package-ci/findings/20261101-test-run-suite-mine-pin-vremeni-fazy-flake.md`).

## Принципы и правила

FR-4, FR-41, FR-55; AR-12, AR-15. Связи: SC2-37, EP1-23 B1.

Решение владельца нужно: нет.
