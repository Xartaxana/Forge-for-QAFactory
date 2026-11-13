# Читатели «только имена» слепы в таблице одного разбора env-файла: однобуквенные имена не проходят фильтр имён, строк BOM и `export` для них нет (критик t-227 / t-230, OH3-42)

id: — | кучка: `onboarding-forge` | от: билдер t-230 (ветка `wip/oh3-42r`, коммит `b4e0fbc`, добавил строки для `project_inventory.env_file_keys`), 13.11.2026 | приоритет: П3 | кандидат наверх: нет

## Что наблюдалось

`scripts/tests/test_manual_capture.py::of3_1e_one_env_file_parse` (стр. ~1975) гонит одну таблицу строк env-файла (`A=1`, `export A=1`, BOM, кавычки…) через читателей значений. Читатели «только имена» фильтруют имя: `project_inventory.env_file_keys` — `KEY_NAME_RE = ^[A-Za-z_][A-Za-z0-9_]{1,63}$` (имя от 2 знаков; однобуквенные `A`, `B` таблицы не проходят), `brief_pack._env_file_key_names` (`brief_pack.py:2532`) — `env_probe.SECRET_NAME` (имя содержит `pass|secret|token|key|credential|auth`; `A`/`B` тоже нет). Поэтому на строках таблицы они не видят ничего, и сравнение «все читатели дают то же» для них молчит: BOM и `export` у `brief_pack._env_file_key_names` проверены только отдельной вставкой с `ONE_TOKEN_*`, а не строками таблицы. Для `project_inventory.env_file_keys` билдер t-230 добавил отдельные строки `name_rows` с двухбуквенными именами (`AB`, `CD`); для `brief_pack._env_file_key_names` — нет.

## Что именно менять

Направление выбрано координатором (13.11.2026): строки «только имена» для `brief_pack._env_file_key_names`, по образцу t-230 (`wip/oh3-42r`, `b4e0fbc`). Делается после слияния ветки `wip/oh3-42r` (иначе `name_rows` нет в дереве).
1. В `of3_1e_one_env_file_parse` (`scripts/tests/test_manual_capture.py`), после блока `name_rows` t-230: таблица `brief_names_rows` — строки с именами, проходящими фильтр ЭТОГО читателя (двухбуквенных имён у `SECRET_NAME` нет, имя берётся с признаком секрета и длиной ≥ 2): «BOM перед первым ключом» (`﻿A_KEY=1\nB_KEY=2` → `["A_KEY","B_KEY"]`), «`export ` строчными снят» (`export A_KEY=1` → `["A_KEY"]`), «`EXPORT ` заглавными — часть имени» (`EXPORT A_KEY=1` → `[]`, как у `env_file_keys`: считать по `parse_env_file`, ожидание строки сверить с ним), «имя без признака секрета не названо» (`AB=1` → `[]`), «повтор — один раз, на первом месте» (`A_KEY=1\nB_KEY=2\nA_KEY=3`), «пустой файл» (`[]`), «`env_files` из двух файлов, позднейший побеждает по ЗНАЧЕНИЮ, имена — объединение без повторов».
2. Ожидание каждой строки — из ПРАВИЛ узла OH3-42 (BOM снят, `export ` снят, пустое имя пропущено; сам фильтр имён — `SECRET_NAME`), не из вывода читателя (P20).
3. Мутация: вернуть читателю старый `parse_env_file` без BOM/`export` — красит строки «BOM» и «`export`» этой таблицы.

## Принципы и правила

P20, P12; FR-54; AR-13. Связи: `findings/20261031-dva-razbora-env-fajla.md` (OH3-42), `plans/piles/execution-report/findings/20261031-brief-s5-avtomatora-bez-stroki-uchetki.md`, ось 126 карты.

Решение владельца нужно: нет.
