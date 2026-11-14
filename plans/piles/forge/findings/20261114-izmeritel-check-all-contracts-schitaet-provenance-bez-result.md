# Измеритель `check_all_contracts.py:285-290` считает файлы `runtime-provenance-*.json` и называет их «записями о сверке»: после P1B-9 это неверно

id: — | кучка: `forge` | от: план-критик P1B-9 (`docs/tasks/specs/reviews/20261114-p1b-9-plan-critic.md`, K2 строка 5, поправка S9) | приоритет: П3 | кандидат наверх: нет

## Что не так

Класс фабрики: **подпись меры говорит больше, чем мера считает (FR-25, FR-41; ось 6 карты)**. `experiments/measurers/check_all_contracts.py` (~285-290, строка `note(c, "CATCH", "artifacts.runtime_provenance", …)`) считает
`R.glob("evidence/runtime-provenance-*.json")` и пишет «N provenance records exist (expected_source_revision + observed_runtime_identity)». После развилки F2 (ii) плана P1B-9 в `evidence/` лежат и записи непроверенных ответов
(`result: not_applicable` / `unknown`), поэтому подпись («записи с ожидаемой ревизией и наблюдаемой идентичностью») устареет. Критик: план искал только в `scripts/`; этот читатель найден вне пакета (контроль того же вида: поиск по `experiments/` находит строку).

## Что именно менять

Выбранное направление: фильтр по полю `result` записи, а не только подпись: считаются записи с установленным `result`, остальные названы отдельным числом.

1. `experiments/measurers/check_all_contracts.py` (~285-290): считать `matched` / `mismatched` отдельно от `not_applicable` / `unknown` / нечитаемых (JSON-ошибка — отдельная графа, не «0»); подпись называет то, что посчитано.
   Поле `result` отсутствует (запись старого вида) — графа «result not recorded», не `matched`.
2. Тест — строка таблицы `experiments/measurers/test_measurers.py` (быстрый): папка `evidence/` с четырьмя записями (`matched`, `unknown`, без `result`, нечитаемая) → подпись называет четыре числа, сумма равна числу файлов; пустая папка — «0».
3. Порядок: после слияния плана P1B-9 (появляется поле `result` у не-matched записей); до слияния узел исполним, но графы `not_applicable`/`unknown` пусты.

Принципы и правила: FR-25, FR-41; AR-28.

Связи: `findings/20261114-p1b-9-odin-chitatel-runtime-provenance.md` (кучка `live-run-fvf`, читатели внутри пакета).

Решение владельца нужно: нет.
