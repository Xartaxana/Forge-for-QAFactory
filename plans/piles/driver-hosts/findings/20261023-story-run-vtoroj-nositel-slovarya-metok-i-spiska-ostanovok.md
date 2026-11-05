# `story_run.py` держит второй носитель двух знаний, которые хотфикс довёл до одного читателя: строку словаря меток (`:7775`) и таблицу остановок `UNTIL_PAST` (`:114`)

id: — | кучка: `driver-hosts` | от: Lead пачки hotfix-12586/1 (dev2), 23.10.2026 | приоритет: П2 | кандидат наверх: нет

Зона `story_run.py` принадлежит `conductor/1` (взята), поэтому узлы hotfix-12586/1 (HF1-6, HF1-8) файл не трогали и оставили обе правки очереди.
Находка — для невзятой пачки conductor; оба места — AR-13 / AR-15 (второй носитель того, что теперь читает один), одна правка файла.

(1) Словарь меток (узел HF1-6, OH3-14). `s3_strategist_lines` → `labelling_lines` строит строку `labels: …; requirement states: ….` сам
(`scripts/story_run.py:7775-7776`), а для брифа окна 1 тот же текст теперь строит `handoff.grounding_vocabulary_line()` (вывод побайтно тот же
для здорового словаря; при нечитаемом словаре пишет `NONE READABLE`, а не пустоту). Точная замена из отчёта t-058:

    f"labels: {', '.join(H.allowed('grounding_labels'))}; requirement states: "
    f"{', '.join(H.allowed('requirement_grounding_states'))}.",
    →
    H.grounding_vocabulary_line(),

Ключ `test_story_run_s3_windows.py:433-436` патчит `H.allowed` и остаётся действительным, потому что помощник зовёт глобальный `allowed` модуля.
Без правки два построителя одного текста расходятся при первом изменении формата.

(2) Список остановок (узел HF1-8, GW1-12). Закрытый список `STOP_VALUES` / `STOP_GATES` и читатель `stop_after()` переехали в `controller.py`
(`scripts/controller.py:5858`, `:5863`); комментарий `scripts/story_run.py:113` всё ещё называет `story_step.STOP_GATES`, а таблица `UNTIL_PAST`
(`scripts/story_run.py:114`, `{"gate_A": {"S5".."S9"}, "gate_B": {"S9"}}`, читается в `:1010` и `:12043`) — ВТОРАЯ копия того же закрытого списка
(AR-1 / AR-15): добавление третьего значения `stop_after` в `controller` не дойдёт до драйвера.

Что сделать: (1) замена выше; (2) `UNTIL_PAST` строится из `controller.STOP_GATES` (или читает его), комментарий называет `controller`;
тест: набор ключей `UNTIL_PAST` равен `controller.STOP_VALUES`; тест `test_story_run_s3_windows.py` (ключи `:425-436`) и `test_story_run_*`,
которые трогают разбор `--until`, — зелёные. Тесты `story_run` большие: свидетель узла — их точечные ключи, полные прогоны — по канону пачки.

Свидетель: `docs/tasks/handoffs/t-058-hf1-6.md`, «Needed from integration (story_run.py is not mine)»; `docs/tasks/handoffs/t-061-hf1-8.md`, «Needed from
integration» («`story_run.py:113` comment says `story_step.STOP_GATES`; now `controller.STOP_GATES`. Its `UNTIL_PAST` table (`story_run.py:114`) is a SECOND
copy of the same closed list (AR-1/AR-15 analog): should import `controller.STOP_GATES`. Not touched (non-goal)»); строки — по дереву пачки, проверены 23.10.2026.

Принципы и правила: FR-13, FR-17, AR-1, AR-13, AR-15, AR-19.

Решение владельца нужно: нет.
