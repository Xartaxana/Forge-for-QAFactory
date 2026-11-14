# Поиск входа на стенде («find the way in») заменяет весь `environment.access` и теряет ключи, которые не про вход

id: — | кучка: `live-run-fvf` | от: отчёт билдера FV1-15 (`docs/tasks/specs/reports/20261114-fv1-15-report.md`, вопрос Q3) | приоритет: П2 | кандидат наверх: нет

## Что не так

Класс фабрики: **запись одного факта стирает соседние факты того же носителя (AR-14, AR-28: известное не пропадает молча)**.
`ai-packages/qa-factory/scripts/project_decisions.py::record_stand_login` пишет `environment.access = {**found["access"], "login_probe": record}`
(строка ~709): найденная дорога формы — минимальный объект (`kind`, `form`, `user_key`, `secret_key`), поэтому любой другой ключ прежнего `access`,
не про вход (пример — `unauth_status`, помощник живости, `config_contract.access_errors` читает его на ~389), при поиске пропадает без следа.
Карточка FV1-15 требовала «новое = access дороги + login_probe», билдер построил как написано и вернул вопрос.

Статус: до слова критика темы t-811 (критик на тему FV1-15/FV1-17) узел не берётся; направление ниже выбрано Lead, критик t-811 его проверяет.

## Что именно менять

Выбранное направление: из прежнего `access` переносятся все ключи, которых нет в `access` найденной дороги и которые не являются ключами входа.

1. `ai-packages/qa-factory/scripts/stand_access.py` (рядом с `KINDS`): ОДИН кортеж `SIGN_IN_KEYS` — ключи, которые описывают сам вход (`kind`, `url`, `form`,
   `command`, `user_key`, `secret_key`, `login_probe` и всё, что `config_contract.access_errors` знает как часть дороги). Полный список дизайнер ИЗМЕРЯЕТ чтением
   `access_errors` и `login-roads.json` до спеки (один результат в спеке узла) и не выдумывает.
2. `project_decisions.py::record_stand_login`: `new = {**kept, **found["access"], "login_probe": record}`, где `kept` — ключи прежнего `access`, не входящие в `SIGN_IN_KEYS`
   и не заданные дорогой. Прежний `access` не словарь или пуст — `kept = {}` (как сегодня). Значение, которое `access_errors` не принимает, отказывает как сегодня, ничего не пишется.
3. Тесты — строка на ключ в таблице `ai-packages/qa-factory/scripts/tests/test_http_client.py` (`the_stand_login_joins`, keep, быстрый): `unauth_status` сохранён; ключ не про вход
   сохранён; ключ входа прежней дороги (`command`) НЕ перенесён; прежний `access` отсутствует / не словарь; ключ, который дорога задаёт сама, берётся у дороги.

Принципы и правила: AR-14, AR-28, AR-13; FR-54.

Связи: `findings/20261114-stand-login-ne-peredayot-imena-klyuchej-environment.md` (тот же `stand-login`, другой дефект).

Решение владельца нужно: нет.
