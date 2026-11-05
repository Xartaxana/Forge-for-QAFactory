# `test_state_portability.py` красный с коммита карточки запуска 194af3ea: у `<DISPATCH>.launch.md` нет строки `file_writers`

id: — | кучка: `codex` | от: Dev2 (ветка `dev2/codex-overhead-fixes`), 13.10.2026 | приоритет: П2 | кандидат наверх: нет

Что не так / что сделать: `state_census.build_baseline` отказывает (`BaselineRefused: no file_writers entry … F3
<PROJECT>/qa-factory/artifacts/<TASK>/work/briefs/<DISPATCH>.launch.md (whole file) plugin_root`), и проверка N0-K3
«the stale row is the only complaint» даёт 2 вместо 1. Красно на нетронутой копии HEAD (`git archive 8cb19fd5`,
прогон 13.10 11:5x), то есть дефект принесён `launch_card.py` (194af3ea), а не t-005. Нужно: строка инвентаря
`file_writers` для карточки запуска (кто пишет, какой узел убирает) в `state_census`/базе переписи и зелёный
`python -B scripts/tests/test_state_portability.py`.

Свидетель: вывод прогона на копии HEAD — `state_census.py:1431 BaselineRefused … <DISPATCH>.launch.md … plugin_root`;
`FAIL N0-K3: the stale row is the only complaint … expected 1, got 2`.

Принципы и правила: FR-32, FR-54 (карточка запуска — новый носитель состояния, перепись обязана его знать).

Решение владельца нужно: нет.
перенесено из ветки dev2/codex-overhead-fixes (plans/piles/driver-controller/findings/20261013-state-portability-launch-card-red.md), узел: CX1-13
