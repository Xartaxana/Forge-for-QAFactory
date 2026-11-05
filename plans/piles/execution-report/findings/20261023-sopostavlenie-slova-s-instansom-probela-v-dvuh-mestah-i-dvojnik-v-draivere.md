# Сопоставление слова человека с экземпляром пробела пробы написано дважды, а двойник в драйвере `story_run.Driver.window_gap` не знает нового вида

id: — | кучка: `execution-report` | от: Lead пачки hotfix-12586/1 (dev2), 23.10.2026 | приоритет: П3 | кандидат наверх: нет

Хвосты узла HF1-14 (EP1-10, слово человека закрывает окно S5 по пробелу пробы); оба — AR-13 / AR-19, один узел.

(1) Соединение «слово человека → экземпляр» (id экземпляра, иначе ключ кейса из его области) написано в двух местах:
`window_record.probe_gap_block` (`scripts/window_record.py:411`, ключи берёт из `links`) и `acceptance.probe_gap_named`
(`scripts/acceptance.py:512`, ключи берёт из `scope_instances`). Они эквивалентны на собранном окне; билдер ввёл `probe_gap_named` как
публичного помощника, чтобы `validate_window` и ярус 4 контроллера (он записывает проход словами из `pipeline.json` самой истории,
не из окна, которое могла написать роль) пользовались ОДНИМ соединением. Второе соединение осталось в `window_record`. Дедуп —
когда появится третий читатель; сейчас дубль — риск расхождения: слово, которое окно видит, а контроллер нет (или наоборот).

(2) Двойник `story_run.Driver.window_gap` (`scripts/story_run.py:2834`, AR-19): знает `could_not_judge`, `fitted_to_code`, `handed_to_person`
и для остального «проваливается» в `story_step`; `blocked_by_env` он не знает и теперь не знает `probe_gap`. В узле HF1-14 он НЕ менялся
(спека M6: падение вниз проверено по спеке, цикл драйвера билдер не гонял). Родственное: `story_step._caller_pair_reason` растит
пару «вызывающего» для `blocked_by_env` и `handed_to_person`, но не для `probe_gap`; вызывающий, набравший пару без слова, получает
отказ яруса 4 с указанием на `finish`.

Что сделать: `window_record` зовёт `acceptance.probe_gap_named` (или оба — общий помощник в `contract.py`); драйвер читает вид
`probe_gap` и `blocked_by_env` теми же функциями, что `story_step` (узел в `story_run.py` идёт после `conductor/1`, строка очереди
в обеих пачках); тест: окно с `probe_gap` проходит `story_run.Driver.window_gap` тем же ходом, что `story_step`. Живое доказательство —
строка пачки hotfix-12586/1 (UI-пробы под `ui`).

Свидетель: `docs/tasks/handoffs/t-069-hf1-14.md` («Analogs noticed»: «`story_run.Driver.window_gap` lacks `blocked_by_env` and now
`probe_gap` (AR-19 twin; falls through) - queue to conductor/1 (spec Q2)»; «The join "instance id, else a case key of its scope" exists
twice: `window_record.probe_gap_block` (keys from `links`) and `acceptance.probe_gap_named` (keys from `scope_instances`). Equivalent on a
built window; a dedupe candidate if a third reader appears»); номера строк — по дереву пачки, проверены 23.10.2026.

Принципы и правила: FR-17, FR-54, AR-13, AR-19, AR-22.

Решение владельца нужно: нет.
