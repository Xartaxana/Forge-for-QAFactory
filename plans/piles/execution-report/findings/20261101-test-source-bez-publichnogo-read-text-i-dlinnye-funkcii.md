# `test_source` читает чужие байты через четыре закрытых имени; `waiver.run_carry` (~80 строк) и `probe_by_code._judge_detector_rows` (~70 строк) над порогом

id: — | кучка: `execution-report` | от: критик диффа S1 релиза 0.10.8 (`docs/tasks/specs/reviews/t-596-s1-critic.md`, F-11), 01.11.2026 | приоритет: П3 | кандидат наверх: нет

Что не так: (1) `scripts/test_source.py` берёт тест-код от пробы через закрытые имена `_declarations`, `_Call`, `_shape`, `_template_parts` и импортирует `probe_by_code._string_end`; публичного входа, принимающего байты, которые проба уже держит, нет. Критик: сейчас законно и не второй лексер, очередь — публичная `read_text(text, entry, rel)`. Проверено 01.11.2026: в `test_source.py` функции с именем `read_text` нет (`Grep` по `read_text` в файле пуст; контроль: `def read_text` найден в `contract.py:2416`). (2) `waiver.run_carry` (`waiver.py:1121`) — около 80 строк (критик на своём дереве: 74, `waiver.py:1113-1186`), линейная; (3) `probe_by_code._judge_detector_rows` (`probe_by_code.py:2522`) — около 70 строк (критик: 70, `:2531-2600`), линейная. Порог «функция над 60 строк» — вопрос критика диффа (`docs/tasks/critic-diff-brief.md`), храповика на размер нет.

Что именно менять: (1) `ai-packages/qa-factory/scripts/test_source.py`: публичная `read_text(text, entry, rel)` над теми же закрытыми помощниками; `probe_by_code` зовёт её вместо закрытых имён (`git grep -n "test_source\._" -- ai-packages/qa-factory/scripts` даёт места); поведение не меняется, тест `scripts/tests/test_test_source.py`: байты на входе дают то же, что чтение файла по пути. (2) `waiver.run_carry`: вынести проверки источника (`old_key`, корень, чтение `stage_overrides` старой истории) в отдельную функцию, `run_carry` остаётся последовательностью шагов; тест — прежние ключи `test_words_carry.py` зелёные без правок. (3) `_judge_detector_rows`: вынести построение строки отчёта в функцию рядом; прежние ключи `test_probe_by_code*.py` зелёные. Это размер и видимость, не поведение: правка без изменения ожидаемых значений в тестах; изменился ожидаемый вывод — стоп.

Свидетель: `docs/tasks/specs/reviews/t-596-s1-critic.md` F-11, строка 51; `ai-packages/qa-factory/scripts/waiver.py:1121`; `ai-packages/qa-factory/scripts/probe_by_code.py:2522`; `ai-packages/qa-factory/scripts/contract.py:2416` (контроль поиска).

Принципы и правила: P12; FR-54; AR-13.

Решение владельца нужно: нет.
