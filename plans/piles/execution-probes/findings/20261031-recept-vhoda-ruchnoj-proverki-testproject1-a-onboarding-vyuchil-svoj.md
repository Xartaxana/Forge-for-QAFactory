# Рецепт входа ручной проверки (`http` и `ui`) — умолчание Test Project 1; онбординг выучил вход проекта и не передал его

id: — | кучка: `execution-probes` | от: прогон CART-1 (MyBooks), 31.10.2026 (свод `experiments/mybooks/cart-1-run-problems.md`, п. 4.3 и 4.4; вопрос владельца W4) | приоритет: П2 | кандидат наверх: нет

Склейка: 4.3 (дверь `http` входит по маршруту Test Project 1) + 4.4 (вход «логином по коду» в UI не подошёл к странице NextAuth) — один класс
(«рецепт входа ручной проверки — умолчание одного проекта, а выученное онбордингом до него не доходит») и один узел.

Вопрос владельца 31.10.2026 (бриф, W4): «разве это не устанавливается на онбординге?» — владелец, 31.10.2026.
Ответ Lead (бриф): онбординг выучил вход (`environment.access.kind: harness_command`, `login_probe.outcome: ok`), а `manual_capture` для
`http` берёт путь `/v1/local-auth/login` из `ai-packages/qa-factory/references/manual-capture-steps.json:29` (умолчание Test Project 1) и
`environment.access` не читает.

## Что наблюдалось

- 4.3 (отчёт `docs/tasks/specs/reports/t-1632-cart1-run-problems-artifacts.md`, строка 25; цитата в
  `A/work/digests/S6-qa-runner-2.txt` — «api door unusable»): `manual_capture http` на S6 вошёл по
  `http://localhost:3000/v1/local-auth/login` → 404 («did not give a token (status 404) … not shown to be the stand's own (HTML
  "Bookstore")»). Runner вместо двери завёл четыре книги и вишлист через UI админки руками.
- 4.4 (t-1633, п. 31; t-1632, строка 10): после снятия блока пробы вход «логином по коду» в UI не прошёл — 31,6 с, `env_blocked`
  (owner `factory`) «the account user … does not sign in on localhost:3000»; решено повторной попыткой через `fill-account`. Умолчание
  рецепта `ui` (`references/manual-capture-steps.json`, `login.ui`) — поля «Email address» / «Password», кнопка «Sign in to your account»,
  кука `testproject1_access_token`, `landed.url_not` `/auth/sign-in`, `openid-connect`: это страница входа Test Project 1.
- Проверено по коду пакета (31.10.2026): `scripts/manual_capture.py`, `_http_login` берёт адрес из `login_recipe(cfg, spec_data, "http")`
  (`manual_capture.login.http` проекта, иначе умолчание файла данных), а `environment.access` читает только для ИМЁН полей тела
  (`_pairs_login`, `config_contract.body_field_candidates`). Путь входа из `environment.access.url` не берётся нигде в `manual_capture`.
- Что онбординг знает о входе (`scripts/stand_access.py`, docstring и `_harness_command`): запись `environment.access` с `kind` из
  `harness_command | local_login | oidc_password | bearer_env | none`, `url` (для `local_login`/`oidc_password`), `user_field`/`secret_field`
  и `login_probe.outcome`. Для `harness_command` проба только запускает команду проекта и проверяет код выхода 0 — ни адреса, ни токена
  она не получает; у MyBooks, по свидетельству брифа, как раз такой вид. Поэтому «просто взять выученное» работает не для всех видов.
- Не проверено: точное содержимое `qa-factory/config.json` проекта MyBooks (`environment.access`, есть ли `manual_capture.login.*`) —
  читал Lead; в отчётах t-1632/t-1633 ключ `manual_capture.login` не упомянут. Проверить дизайнеру по копии стенда.

## Класс

Дверь ручной проверки (`http`, `ui`) молча берёт рецепт входа проекта, на котором фабрику строили, хотя вход проекта онбординг уже
исследовал и записал. Данные проекта лежат в двух местах (`environment.access`, `manual_capture.login.*`), и читатель одного не
знает о другом (AR-3, AR-13, AR-22; P2; FR-17 — средство, существующее для проблемы, подключено не везде).

## Что именно менять

Направление выбрано: рецепт входа берётся из выученного проектом; умолчание Test Project 1 — только для проекта, у которого нет своего
рецепта, и без попытки вслепую.

1. **`scripts/manual_capture.py`, `login_recipe` + `_http_login`: порядок источников рецепта `http` — один читатель.** (а) ключ
   `manual_capture.login.http` проекта (как сегодня); (б) иначе `environment.access` с `kind` `local_login` или `oidc_password`: путь —
   из `access.url` (если это ИМЯ ключа окружения — разворачивает `stand_access`, не копия), поля тела — как сегодня; (в) иначе умолчание
   файла данных — **только если** `environment.access` пуст/`none`/нет записи (проект без записанного входа: поведение прежнее); (г) вид
   `harness_command` или `bearer_env` без рецепта `http` — дверь `http` НЕ ходит на умолчание Test Project 1: до первого запроса отказ
   `env_blocked` с владельцем `project` и дверью: «у проекта вход выполняет команда (`access.command`); задайте `manual_capture.login.http`
   (путь и `token_field`) либо `null`, если HTTP-входа нет (роль входит через UI: `fill-account`)». Тест: фикстура с `harness_command`
   без рецепта — запрос не отправлен (счётчик вызовов 0), отказ называет ключ; фикстура `local_login` с `url` — запрос идёт на путь из
   `access.url`; фикстура Test Project 1 без `access` — поведение прежнее.
2. **Онбординг (`skills/qa-onboarding/phases/p4-generate.md` и код записи конфига, `scripts/onboard_apply.py`/`scripts/config_contract.py`;
   точное место уточняет спека): запись рецептов из выученного.** Если проба входа нашла рабочий HTTP-вход (вид `local_login`/`oidc_password`
   с принятой парой полей) — `manual_capture.login.http` пишется сразу (путь, `token_field`); если вход идёт командой проекта
   (`harness_command`) и HTTP-входа у проекта нет — записывается `manual_capture.login.http: null` (`login_declared_none` это уже читает) после
   ОДНОГО закрытого вопроса человеку (форма `human-questions.md`): «Приложение входит запросом с токеном? да, адрес … / нет, только через
   страницу входа / не знаю». «Не знаю» — ключ не пишется, дверь отказывает по п. 1 (г). Тест: онбординг на фикстуре `harness_command` не
   оставляет рецепт Test Project 1 «по умолчанию молча»; конфиг после онбординга проходит `config_contract` и читается `login_recipe`.
3. **Рецепт `ui` (4.4).** `login.ui` умолчания (поля, кнопка, кука Test Project 1) используется «входом по коду» только если ключ
   `manual_capture.login.ui` не задан И первый локатор рецепта (поле «Email address») находится на странице входа за малый лимит
   (рекомендация: `ELEMENT_WAIT_S`, как у любого шага); не нашёлся — отказ за секунды, не за 31,6 с, без «ошибки учётки»: «рецепт входа
   по умолчанию — для Test Project 1, на этой странице его полей нет; шаги `fill-account` в файле шагов (готовая форма в `agents/qa-runner.md`)
   или рецепт `manual_capture.login.ui` в конфиге» (дверь, которой владелец отказа — роль, FR-2). Онбординг (`p1-discovery`) уже называет адрес
   страницы входа (`landed.url_not`): записывает его в `manual_capture.login.ui.landed`, если он отличается от умолчания.
   Тест: фикстура-страница входа с другими полями — отказ быстрее лимита, текст называет оба выхода; страница Test Project 1 — вход идёт.
4. **Сообщение отказа обеих дверей** называет, откуда рецепт (проект / `environment.access` / умолчание фабрики), чтобы 404 не выдавался за
   «маршрут сломан» (FR-1, FR-37: путь в тексте — тот, который код использует).

## Принципы и правила

P2, P5, P15, P22; FR-1, FR-2, FR-17, FR-37, FR-59; AR-1, AR-3, AR-9, AR-13, AR-22.

Связи: `forge/findings/B-252-login-by-code-u-manual-capture-ui.md` (там замерено: `environment.access` — рецепт API-доступа readiness/stand_health,
к входу в UI не относится; остаток (3) «onboarding спрашивает ключи» не построен — п. 2 этого узла и есть его продолжение);
`onboarding-hooks/findings/20261022-proba-vhoda-shlet-username-a-stend-zhdyot-email.md` (поля тела входа); EP1-28 (профиль и версия стенда
той же двери); EP1-31 — этот узел.

Решение владельца нужно: нет. Ответ на W4 дан Lead 31.10.2026 (выше); вопрос «да/нет по адресу HTTP-входа» человеку — закрытый, в онбординге.
