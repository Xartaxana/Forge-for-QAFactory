# `stand-login` не передаёт `try_roads` имена ключей из `environment`: проект с `kind: none` и записанными ключами получает «дорог нет»

id: — | кучка: `live-run-fvf` | от: отчёт билдера FV1-15 (`docs/tasks/specs/reports/20261114-fv1-15-report.md`, наблюдение Q4) | приоритет: П2 | кандидат наверх: нет

## Что не так

Класс фабрики: **читатель берёт факт из одного носителя, а он записан в другом (AR-13, AR-22)**. `ai-packages/qa-factory/scripts/stand_access.py::try_roads` пробует дороги
формы (`b:<id>`) только когда имена ключей есть в записанном `environment.access` (`user_key`, `secret_key`) или переданы вызовом (`user_key=`, `secret_key=`); иначе каждая дорога
пропускается («no sign-in key names are recorded or given»). Проект, у которого `environment.access.kind` равен `none`, а имена лежат в `environment.user_key` и `environment.secret_keys`,
получает от `project_decisions.py::record_stand_login` (вызывает `try_roads(config, root, env_name=stand)` без имён) отказ «no way in signed in», хотя дорога формы вошла бы.

## Что именно менять

Выбранное направление: `stand-login` сам передаёт `try_roads` имена ключей из `environment`.

1. `ai-packages/qa-factory/scripts/project_decisions.py::record_stand_login`: перед `try_roads` прочитать из `config["environment"]` имя пользователя (`user_key`) и имя секрета
   (`secret_key`, а при списке `secret_keys` — единственный элемент; два и более — имя не берётся и остаётся прежний отказ «no key names», не угадываем) и передать `user_key=`/`secret_key=`.
   Записанный `access` с ключами по-прежнему первее (как в `try_roads`). Имена, не проходящие `config_contract.KEY_NAME_RE`, не передаются.
2. Тесты — строки таблицы `ai-packages/qa-factory/scripts/tests/test_http_client.py` (`the_stand_login_joins`, keep, быстрый): `kind: none` + `user_key` + один `secret_keys` → дорога формы
   пробуется; два `secret_keys` → «no key names», ничего не пробовалось; пустые / не строки / имя вне `KEY_NAME_RE` → «no key names»; записанный `access` с именами первее `environment`.
3. Изменения текста человеку нет (отказ тот же); `human_text.problems` для него пустой.

Принципы и правила: AR-13, AR-22, AR-9; FR-54.

Связи: `findings/20261114-poisk-vhoda-zamenyaet-ves-access-i-teryaet-klyuchi-ne-pro-vhod.md` (тот же `stand-login`).

Решение владельца нужно: нет.
