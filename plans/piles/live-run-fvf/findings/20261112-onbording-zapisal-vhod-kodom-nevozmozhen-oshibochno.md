# Онбординг записал «вход кодом невозможен» по POST на страницу `/login`, а проверка стенда S5 останавливает фабрику на этом же записанном отказе

id: — | кучка: `live-run-fvf` | от: живой прогон LR2-1 (плечо `factory`, релиз 0.11.0 + FV1-1), 12.11.2026 | приоритет: П1 | кандидат наверх: да

## Что не так

1. Онбординг (17:23) записал в `config.json` `environment.access.kind: local_login`, `url: /login`, `login_probe: failed 405`, и в
   `records/project-decisions.json` — «local_login by code is not possible: the stand signs in through NextAuth (csrf form)».
   Вывод неверен: `/login` — страница, а не точка входа. Проверка оператора 20:05: `GET /api/auth/csrf` →
   `POST /api/auth/callback/credentials` (csrfToken, email, password) → 200, `/api/auth/session` с пользователем, cookie
   `next-auth.session-token`. Вход кодом работает; у `stand_access` нет вида входа «форма с csrf» (NextAuth credentials), а
   `harness_command` (обвязка проекта входит сама: `tests/e2e/auth/login.spec.ts` проходит, с неверным паролем — падает)
   онбординг не предложил, хотя нашёл рецепт входа UI в `global-setup.ts` (`discovery.yaml:76`).
2. На S5 проверка стенда (`env_probe.py`, слой 1) остановила фабрику на том же входе, который конфиг уже записал как
   `failed`, — дважды (19:43 при упавшем стенде честно, 20:03 при живом). Человеку показан текст «the stand `local` did not
   answer», хотя стенд ответил 200 (это и есть FV1-5); записанное решение класса не применено к экземпляру (P5).

Вопрос владельца на прогоне: «а как делать АПИ тесты если кодом нельзя зайти?» — фабрика с таким выводом онбординга
строит API-проверки без входа или гонит всё через UI.

Обход оператора (по слову владельца «конфиг проекта»): в копии плеча `access.kind: harness_command`, `command: node
node_modules/@playwright/test/cli.js test tests/e2e/auth/login.spec.ts --project=chromium --reporter=line`, `login_probe: ok,
seconds 60` (замер 56 с); копия до правки — `config.json.before-harness-login-20261112`. `env_probe.py --env local` → `login: ok`.

Свидетель: `runs/factory-14.log`; `notebook.md`, «Ход прогона», 20:03–20:15.

## Что сделать (предложение оператора)

(а) Онбординг не пишет «вход кодом невозможен» по одному отказу страницы: пробует точки входа фреймворка (данные — строки
файла вроде `references/login-body-fields.json`: NextAuth `api/auth/csrf` + `callback/credentials`, и т. п.) и предлагает
`harness_command` из найденного рецепта входа обвязки. (б) Вид входа «форма с csrf» в `stand_access` — строкой данных, не кодом
под один фреймворк (AR-1). (в) Проверка стенда не останавливает стадию на отказе входа, уже записанном конфигом как известный
и решённый, а говорит о нём строкой (FR-4, FR-7).

Принципы и правила: P2, P5, P6; FR-4, FR-7, FR-13, FR-50; AR-1, AR-3, AR-6.

Решение владельца нужно: нет (направление «конфиг проекта» дано на прогоне; правка пакета — по пачке).
