# `test_triage_control` A-K9 красный на базе: перечень файлов с вердиктами не знает `traceability.py` и `s7_pretriage.py`

id: — | кучка: `package-ci` | от: билдер HF8-19 N1b и критик S5b rest релиза 0.10.7 (`docs/tasks/specs/reports/r0107-s5b-n1b-hf8-19.md:28-34`, `docs/tasks/specs/reviews/r0107-s5b-rest-diff-critic.md:84`, `:121`), замер на базе `268e7608`, 30.10.2026 | приоритет: П3 | кандидат наверх: нет

Что не так / что сделать: `python -B ai-packages/qa-factory/scripts/tests/test_triage_control.py` на `268e7608`: `FAIL A-K9 the word lives in the vocabulary and the delivery owner table, nowhere else in code — expected ['check_delivery.py', 'contract.py'], got ['check_delivery.py', 'contract.py', 'traceability.py']`; `FAIL A-K9 control: the same search finds the older word in the same two files`; `175/177`. Причина: слова `ASSERT_STRICTER` (docstring `traceability.py:632`) и `CASE_DEFECT` (docstring `s7_pretriage.py:30`; в отчёте — `:13`, критик поправил) встречаются в docstring, а перепись A-K9 ждёт ровно два файла. Красное не от узла: база уже падала (`a85c7f69`). Билдер N1b передал исправление переписи в BATCH CANON (файл вне его `owns`). Что сделать: либо перепись допускает docstring (считать только код через `ast`), либо список содержит два файла с причиной; контрольная проба (старое слово в тех же файлах) обновляется вместе. Пин: слово, добавленное в код третьего модуля, роняет тест; слово в docstring — нет.

Свидетель: вывод `FAIL A-K9` выше; `git grep ASSERT_STRICTER e404d6ea` находит `traceability.py` (критик S5b rest, `…:121`). Связанная находка про исполнителя вердикта: `driver-controller/findings/20261030-case-defect-net-v-drajvere-verdikt-bez-ispolnitelya.md`.

Принципы и правила: FR-34, FR-28; AR-19.

Решение владельца нужно: нет.
