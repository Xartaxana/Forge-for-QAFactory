# Поля тела входа на стенд записаны в нескольких носителях: `access.user_field` и `manual_capture.login.http.body`; две красные фикстуры повторяют шаблон руками

id: — | кучка: `onboarding-forge` | от: Lead пачки hotfix-12586/1 (dev2), 23.10.2026 | приоритет: П3 | кандидат наверх: нет

Хвосты узла HF1-4 (OH3-10, проба входа шлёт имена полей из данных `environment.access`). Оба — «одна запись, несколько ручных копий»,
чинятся делом одного класса: носитель читают, а не повторяют.

(1) Вторая запись тела входа. `environment.access.user_field` / `secret_field` (читатель — `config_contract.body_fields`,
`scripts/config_contract.py:86-87`, умолчания `username` / `password`) и `manual_capture.login.http.body` (`references/manual-capture-steps.json:29`,
`{"email": "{username}", "password": "{password}"}`, проектом заменяется через `manual_capture.login.http`) описывают ОДИН факт — поля тела входа
стенда — в двух местах. Исправление одной записи (онбординг узнал, что стенд ждёт `email`, и записал `user_field`) не меняет другую:
ручной захват берёт имена из своего файла данных; обе записи надо помнить править вместе (AR-13, AR-15). Записи сверяет таблица D5 отчёта t-056: UI-вход и OIDC — не
этого класса (UI — роль и доступное имя, OIDC — поля RFC 6749), другие литералы тел входа в `scripts/*.py` не найдены.

(2) Две красные фикстуры. Шаблон `references/templates/config.json` получил два ключа `environment.access` (`user_field`, `secret_field`),
а фикстуры `ACCESS` в `scripts/tests/test_config_migration.py:972` и `scripts/tests/test_install_retire.py:119` повторяют старый шаблон
руками и краснеют на каждом новом ключе (отчёт t-056, отклонение 1; та же поломка у хотфикса `1cda1745`). Lead пачки поправил обе
фикстуры одной строкой каждая (435/435, 302/302), но причина — рукописная копия — осталась.

Что сделать: (1) `manual_capture` берёт поля тела входа из `environment.access` через `config_contract.body_fields` (или наоборот — одна запись,
второй читатель), `manual_capture.login.http.body` остаётся переопределением проекта, а не вторым источником правды; тест: `user_field: email`
даёт ручному захвату тело с `email`. (2) фикстуры `ACCESS` строятся из `TEMPLATE["environment"]["access"]`, а не руками; тест красный
только на смысловое изменение, не на новый ключ.

Свидетель: `docs/tasks/handoffs/t-056-hf1-4.md` («D5 enumeration»: «`manual_capture.py` HTTP login ... is a SECOND record of the same fact
(the stand's login body fields) next to `access.user_field`: AR-13/AR-15 duplicate. QUEUED to the Lead (one should read the other)»; «Noticed
analogs»: «The two red fixtures mirror the template by hand; deriving `ACCESS` from `TEMPLATE["environment"]["access"]` would stop the
recurrence»). Строки — по дереву пачки, проверены 23.10.2026.

Принципы и правила: FR-13, FR-17, AR-1, AR-13, AR-15, AR-22.

Решение владельца нужно: нет.
