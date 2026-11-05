# Проект с `environment.access.kind: bearer_env` не получает входа в ручной проверке: дверь ведёт на `login.http`, которого такому проекту не нужно, а заголовок `Authorization` отказывает собственный скан секретов (t-561/t-562 Ф-9 a)

id: — | кучка: `execution-report` | от: критик t-561 (Ф-9 а, `docs/tasks/specs/reviews/t-561-s4-critic.md`), t-516 Н-11, спека t-524 («`bearer_env` (Н-11)»), 31.10.2026 | приоритет: П2 | кандидат наверх: нет

## Что наблюдалось

- `manual_capture.http_login_source` (`manual_capture.py:2498`): любой `kind`, кроме `local_login` и пустого, — `harness_command`, `bearer_env`, `oidc_password` — даёт `EnvBlocked(not_known_line, not_known_door)`; дверь
  (`references/manual-capture-steps.json:63`): «record manual_capture.login.http … (path and token_field)». Для `bearer_env` это неверная дверь: токен такому проекту не выдаёт POST, он лежит в ключе `environment.access.token_key` (`stand_access._bearer_env`, :412).
- Спека t-524 велела отдельную дверь `login.door_bearer`: «pass it with --header "Authorization: Bearer <the value>"». Но `manual_capture.run_http` (:2640) проверяет каждый заголовок через `secret_pattern_hit` (:501), и
  `Authorization: Bearer …` отказывается («A credential never goes in a request you write»). S11 пинит этот отказ. Дверь, которой нельзя воспользоваться (FR-2); билдер оставил общую дверь и спека велела завести находку (Ф-9 а: записи нет).
- Класс: дверь, названная отказом, ведёт туда, где отказ повторится (FR-2, FR-57; AR-9).

## Что именно менять (направление выбрано: код ставит заголовок сам, человек и роль токен не пишут)

1. `manual_capture.py`, `http_login_source`: вид `bearer_env` с непустым `token_key` возвращает `({}, "access_bearer")` (запрос не нужен), как `access` возвращает адрес; вид `bearer_env` без ключа — прежний `EnvBlocked`.
2. `run_http` (:2605) после скана секретов (:2640–2645, он охраняет то, что НАПИСАЛА роль) и перед отправкой: источник `access_bearer` добавляет заголовок `Authorization: Bearer <значение ключа из env-файлов проекта>` самим кодом
   (значение берётся `gate_preflight.env_values(configured_env_files(…))`, ключ отсутствует — `EnvBlocked` с именем ключа, значение не печатается); в сохранённый запрос заголовок попадает как `[redacted]` (`redact`, :514, `redact_headers` уже содержит `Authorization`). Роль, написавшая свой `Authorization`, по-прежнему отказана.
3. `references/manual-capture-steps.json` `login.words`: строка `source_access_bearer` и дверь `door_bearer` («this project's sign-in is a token in the key environment.access.token_key; the factory sends it as a header itself: make the request without --header Authorization»); `qa-runner.md` — одна фраза (лимит байт: проверить).
4. Тесты (`scripts/tests/test_manual_capture.py` / `test_login_body_fields.py`): `bearer_env` + ключ в `.env`: запрос ушёл с заголовком, сохранённый запрос `[redacted]`, значение нигде в выводе; ключа нет — `EnvBlocked` называет ключ; роль передала `--header "Authorization: Bearer x"` — отказ как прежде (S11 зелёный). Мутация: не скрывать заголовок в сохранённом запросе — красит.

## Принципы и правила

P5, P14, P15; FR-2, FR-57, FR-11; AR-3, AR-6, AR-9, AR-22. Связи: EP1-31, `docs/tasks/specs/t-524-s4-appium-amendment.md` (Н-11).

Решение владельца нужно: нет.
