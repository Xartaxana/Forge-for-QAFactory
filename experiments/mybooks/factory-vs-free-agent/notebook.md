# Тетрадь: фабрика против свободного агента (узел `live-runs/2/LR2-1`)

Стори «Add to Cart» в MyBooks, два плеча параллельно. Как вести прогон — [RUN-INSTRUCTIONS.md](RUN-INSTRUCTIONS.md);
с чем сверять — [factory-vs-free-agent.md](factory-vs-free-agent.md). Деньги и секреты сюда не пишутся.

## Подготовка

### Сделано 12.11.2026 (сессия Lead, машина владельца без Docker)

- Слово владельца 12.11.2026: «перед прогоном надо сделать релиз самой фабрики… пока готовь всё для параллельных прогонов
  плеч (песочницы, промт и т. д.)»; «на этом компьютере вроде бы даже докера нет, ставь всё что тебе нужно»; «напиши
  инструкцию по прогону эксперимента, так как запускать его будет опус в новой сессии».
- **Решила сама (техническое, обратимо): стенд без Docker.** На машине нет Docker и WSL, у сессии нет прав администратора;
  `docker-compose.yml` приложения даёт только PostgreSQL 16 и Mailpit. Поставлено:
  PostgreSQL 16.15 — портативные бинарники с `get.enterprisedb.com` (`postgresql-16.15-5-windows-x64-binaries.zip`,
  sha256 `43BB45F1…AA8281`) в `C:\QAFactory\mybooks-stand\tools\pgsql`, без установки и службы; Mailpit 1.33.0 — `winget`
  (`axllent.mailpit`); Claude Code CLI 2.1.322 — `npm install -g @anthropic-ai/claude-code` (вход — за владельцем);
  браузер Chromium для Playwright. Роль и пароль базы — открытые значения из `docker-compose.yml` проекта.
- **Два независимых стенда** (скрипт `stand/stand.ps1`): общий только процесс PostgreSQL на `:5433`.

  | Плечо | Приложение | База | Почта SMTP / UI | Папка |
  |---|---|---|---|---|
  | `factory` | `http://localhost:3000` | `bookstore` | 1025 / 8025 | `C:\QAFactory\mybooks-stand\arm-factory\` |
  | `free` | `http://localhost:3001` | `bookstore_free` | 1026 / 8026 | `C:\QAFactory\mybooks-stand\arm-free\` |

  В каждой папке — своя копия `MyBooks` (`a25b0801669b97d76f96f5a981fdc9ad4525d63d`, прод-сборка) и
  `test-automation-framework` (`d33d6194e0ad497e12a7a264f1d2e4933d78c712`, `main` апстрима — БЕЗ онбординга фабрики).
  Чистые клоны рядом (`...\MyBooks`, `...\test-automation-framework`) только читаются.
- Свидетель 12.11 13:27: оба `setup` прошли — «All migrations have been successfully applied», «Created 38 books, 8
  categories and 2 user(s)», `/api/health` обоих → `{"status":"ok","db":"up"}`; `-Action status` после возврата вызова —
  всё слушает (процессы пережили вызов инструмента).
- Настройки стенда сгенерированы скриптом, значения не печатались. sha256 (начало): `arm-factory\MyBooks\.env.local`
  `8C9BD6C0992E7BF0`, `arm-free\MyBooks\.env.local` `F09D7947224D6E42`, `arm-factory\test-automation-framework\.env`
  `B83EF232845CF6A4`, `arm-free\...\.env` `F5B1D8CCD41C207F`. Секреты у плеч РАЗНЫЕ (свой `TEST_SECRET`, свой пароль
  пользователя) — плечо не может тронуть чужой стенд даже по ошибке адреса.
- **Решила сама: в `.env` тестового репозитория `NODE_ENV=prod`** у обоих плеч. Остальные профили идут в мок-сервер, а
  не в приложение (RUNBOOK §11, ловушки) — это свойство стенда, а не знание онбординга; одинаково обоим.
- **Решила сама: админ сида — `admin@bookstore.com`** с паролем из `core/fixtures/admin.fixture.ts` тестового репозитория
  (как на прежнем стенде, RUNBOOK §11); обычный пользователь — `user@bookstore.com`, пароль сгенерирован.
- Из связки истории (`C:\QAFactory\qa-forge-history-2026-11-11.bundle`, ветка `main-merged`, распакована в
  `C:\QAFactory\history.git`) возвращено дерево `experiments/mybooks/` без `thinking-roles/runs/`: исходники сравнения
  05–06.11 (`disputed-check-plain-agent/`, `thinking-roles/walker-vs-plain-agent.md`), список 24 спорных мест, заготовки
  ответов владельца, рецепт двух плеч 04.11 — п. 5 находки LR2-1 закрыт.
- Написаны: промт свободного агента (черновик), таблица сверки с правдой и порядком слепой оценки, ответы
  (`answers/README.md`), инструкция оператору.

### Не сделано и почему

- (сделано) Проба существующего теста входа на обоих стендах, 12.11 ≈ 13:44:
  `npm --prefix <копия тестов плеча> run test -- tests/e2e/auth/login.spec.ts --project=chromium --reporter=line` →
  `factory`: «1 passed (11.1s)», `free`: «1 passed (2.8s)». Тест ходит в живое приложение своего плеча под админом сида.
- **Ловушка машины: распаковщик браузеров Playwright зависает на Node 26.** `playwright install chromium` (Playwright
  тестового репозитория, сборка браузера 1194) скачивает архив за секунды и навсегда встаёт на «extracting archive»
  (два раза, 15 и 8 минут, 0 файлов). Обход: архивы скачаны с `cdn.playwright.dev` и распакованы `Expand-Archive` в
  `%LOCALAPPDATA%\ms-playwright\{chromium-1194, chromium_headless_shell-1194, ffmpeg-1011, winldd-1007}` с пустым файлом
  `INSTALLATION_COMPLETE` в каждой; копии архивов — `C:\QAFactory\mybooks-stand\tools\pw-zips`. Тот же зависон ждёт любой
  другой Playwright на этой машине (MCP-браузер свободного агента, рекордер фабрики, если он ставит свой браузер):
  `stand/free-mcp.json` поэтому указывает на уже распакованный `chrome.exe`.
- Форма запуска `free` (`claude -p` с MCP-браузером) и вход `claude` не проверены: нужен вход владельца. Проверяет
  репетиция (инструкция, шаг 3).
- Заморозка пакета: ждёт релиза (инструкция, условие 1). На 12.11 `main` — `688ae28`, пакет 0.10.9.

## Решено владельцем 12.11.2026 (вторым ходом)

1. **Онбординг плеча `factory` — заново здесь, релизной версией** («Да, заново здесь»). Прежний онбординг (0.10.8,
   коммит `5cd21eb` на старой машине) не привозится.
2. **Текст стори** — словами владельца (доступа к Jira на этой машине нет, прежний `LOCAL-1.md` не воспроизвести):

   > Задача: Проверить функционал "Add to Cart" в приложении. Все пути как товар может попасть в корзину и все сценарии
   > где этот функционал используется.
   > Что уже было сделано: стори "C:\QAFactory\XPANBFLFA-44.xml"
   > Код самого приложения: https://github.com/e-semenyuk/MyBooks
   > Стенд: локальный

   **Решила сама (одна правка текста):** путь к выгрузке стори заменён на `task/XPANBFLFA-44.xml` — копия файла лежит
   внутри копии тестов каждого плеча, потому что сессия плеча не читает файлы вне своей папки. Канон текста —
   [story/LOCAL-1.md](story/LOCAL-1.md); в обоих плечах лежит `task\LOCAL-1.md` (sha256 `E407BC4E1C65AC00…`) и
   `task\XPANBFLFA-44.xml` (sha256 `A82CB5D9E8E96896…`, 25 997 байт) — хэши пар совпали. Сама выгрузка в этот
   репозиторий НЕ кладётся (корпоративная Jira, репозиторий публичный); её исходник — `C:\QAFactory\XPANBFLFA-44.xml`.
3. **Трекер — оба плеча без трекера** («оба без трекера»). Письменные требования — текст стори, выгрузка
   `XPANBFLFA-44.xml`, репозитории. Следствие для таблицы правды: баги, стоявшие на кейсах Jira (140, 164, 174, TC-016,
   TC-017), теперь стоят только на словах владельца — плечо получает их, только если спросит (`answers/README.md`).
4. **Промт свободного агента утверждён** с блоком «How your result will be judged» («ок»).

5. **Смысл задачи и что считать багом** (третьим ходом, дословно): «Выгруженный тикет это не от что мы тестируем, это то
   что уже было сделано. Из него можно брать требования, но нельзя ими ограничиваться. Текст задачи это "Проверить
   функционал "Add to Cart" в приложении. Все пути как товар может попасть в корзину и все сценарии где этот функционал
   используется." Мы проверяем что функционал работает, всё что не работает или работает не логично может быть багом.
   Если есть сомнения баг это или допустимое поведение, то надо спросить пользователя». Внесено: ответ
   `answers/no-tracker.md` переписан этими словами; в промте `free` правило «баг стоит на записанном требовании»
   заменено этим; счёт ложных багов в таблице — тоже.
6. **Эти слова внесены в сам текст стори** (четвёртым ходом: «Да, внести») — оба плеча читают их с первой минуты.
   `story/LOCAL-1.md` теперь пять строк: задача; что считать багом и когда спрашивать; что уже сделано и как читать
   выгрузку; код; стенд. Правки Lead в словах владельца: опечатка «не от что» → «не то что» и путь к выгрузке (п. 2).
   Хэш п. 2 для `LOCAL-1.md` устарел: sha256 канона и копий в обоих плечах теперь `7A7FDE710E223B8E…` (три файла
   совпали).

## Условия 4–7 и репетиция — сделано 12.11.2026 17:05–17:40 (слово владельца: «Да, отсюда»)

- **Плагин 0.11.0 поставлен как у нового пользователя** (`claude plugin marketplace add Xartaxana/QAFactory`,
  `claude plugin install qa-factory@qafactory`, scope user). В плече `factory` он был включён на время онбординга, после
  него выключен файлом `.claude\settings.local.json` (драйвер берёт пакет из `--plugin-dir`); в плече `free` выключен
  с самого начала тем же файлом; `claude plugin list` из папки `free` → «disabled». Ветки копий: `exp/fvf-factory`,
  `exp/fvf-free`.
- **`/qa-factory:qa-doctor`** (17:07, 68 с): установка здорова, проект не онбордён — следующий шаг онбординг.
- **Онбординг плеча `factory`** — одна сессия `claude -p` на Sonnet, продолжаемая `--resume` (форма без окна работает);
  17:12–17:27, 15 минут стены, 12 ходов человека: 7 пакетов интервью (≈ 20 вопросов), сводка, одна правка сводки и
  ТРИ «да» (см. находки). Логи ходов — `runs/onboarding-*.json` (в репозиторий не коммитятся: в них цена). Цена названа
  владельцу в чате. Итог: `qa-factory\config.json` (стенд `local`, адаптер задач `file`, VCS «github, no delivery»,
  записи `local_only`), `strategy\` (пять документов), `obligations.md`, `factory-backlog.md`, `records\coverage-map.md`;
  ничего не закоммичено.
  - Ответы **владельца** (через вопрос в этой сессии): рисковые области — «Позже»; шкала багов — стандартная; когда
    стори протестирована — «каждое требование проверено, найденные баги описаны, сомнительные места вынесены вопросом
    владельцу продукта».
  - Ответы **мои** (факты стенда и следствия уже принятых решений): единственный репозиторий приложения `../MyBooks`,
    `main`; библиотеки кейсов нет (следствие «без трекера»); стенд `local` на `http://localhost:3000` уже поднят,
    сброс — `stand.ps1 -Action seed -Arm factory`; вход `local_login`, `EMAIL_USER` — админ, `USER_EMAIL` — обычный
    пользователь; данные синтетические, тест убирает за собой, можно опираться на книги, категории и две учётки сида;
    ветки `feature/<…>`, коммиты `type: summary`, записи `local_only`, без пуша и PR; `npm run lint`, `npm run
    typecheck`, `npm ci`; сборка не общая; **ручной ходок один** (стенд один, учётки две, сброс стирает всё);
    находки и кейсы — `markdown`; свои документы стратегии в `qa-factory/strategy/`, гайд проекта не трогать; правка
    сводки: `src/app/api/test/*` — код продукта, не тесты.
- **Текст стори у фабрики**: `qa-factory\local-tickets\LOCAL-1.md`; четыре файла `LOCAL-1.md` (канон, два `task\`,
  `local-tickets\`) — sha256 `7A7FDE710E223B8E…`, совпали.
- **Сухой прогон драйвера**: `story_run.py --task LOCAL-1 --env local --model sonnet --no-trace --plugin-dir
  C:\QAFactory\exp-fvf\pkg\qa-factory --project <копия factory> --dry-run` → выход 0, «pipeline.json is absent: would
  run S0 by code — ticket_adapter get --raw-dir …».
- **Проба формы запуска `free`** (пустая папка, тот же набор флагов): первая попытка — браузер MCP не стартовал
  (`spawn UNKNOWN`), агент честно сказал, что взял заголовок через curl. Причина — **вторая сторона ловушки
  песочницы**: `chrome.exe` по видимому пути `%LOCALAPPDATA%\ms-playwright\…` не запускается («side-by-side
  configuration is incorrect» / «Sandbox cannot access executable»), по настоящему пути
  `C:\Users\i_mas\AppData\Local\Packages\Claude_pzs8sxrjxfjjc\LocalCache\Local\ms-playwright\…` — запускается.
  `stand/free-mcp.json` переведён на настоящий путь; вторая попытка: выход 0, 13 с, 0 отказов разрешений, «The page
  title is "Bookstore"», `out\title.txt` есть. Продолжение той же сессии (`--resume`) — тот же `session_id`,
  `out\ok.txt` появился. **Обоим плечам при старте задаётся `PLAYWRIGHT_BROWSERS_PATH` = настоящий путь** (с ним
  `login.spec` плеча `free` — «1 passed (9.3s)»).
- **Рекордеру фабрики нужен Python-Playwright** (`manual_capture.py` импортирует `playwright.sync_api`), на машине его
  не было; ни доктор, ни онбординг об этом не сказали (находка). Поставлен (слово владельца: «ставь всё что нужно»):
  `python -m pip install playwright` → 1.65.1, `python -m playwright install chromium` → сборки `chromium-1254` и
  `chromium_headless_shell-1254` в настоящей папке браузеров (распаковщик Python-пакета на этой машине НЕ завис).
  Проба тем же способом, каким запускает рекордер (`chromium.launch(headless=True)` и `launch_persistent_context`),
  на `http://localhost:3000`: «launch: Bookstore», «persistent: Bookstore», выход 0 — и с переменной пути, и без неё.
- `runs/free-prompt-final.md` записан (текст стори дословно, команда сида плеча `free`).

## Открыто — ждёт владельца

1. (сделано 12.11.2026 ≈ 17:05) **Релиз фабрики 0.11.0**: PR `Xartaxana/QAFactory#1` слит владельцем
   (`5e55e30f893b0d086b5f3b04aabd2cfa8d1b685d`), тег `v0.11.0`, GitHub Release. **Пакет заморожен** (решила сама:
   на теге релизного репозитория, а не на `main` форджа — там уже `d3b312d`, которого в релизе нет):
   `C:\QAFactory\exp-fvf\pkg` — рабочее дерево `C:\QAFactory\QAFactory` на `v0.11.0`; `rev-parse HEAD` → `5e55e30…`,
   `release_fingerprint.py --check` → «ok - the tree matches references/release-fingerprint.json (version 0.11.0)».
   Пакет драйвера — `C:\QAFactory\exp-fvf\pkg\qa-factory`. Строка «на 12.11 `main` — `688ae28`, пакет 0.10.9» выше
   устарела. Онбординг и репетиция сделаны (раздел выше). Осталось: сам прогон — новой сессией (слово владельца
   12.11.2026: «сам запуск эксперимента начну с новой сессии когда ты скажешь что всё готово»).
2. (сделано владельцем 12.11.2026 ≈ 14:25) **Вход `claude`**: `claude auth status` → `"loggedIn": true`,
   `"authMethod": "claude.ai"`; проба `claude.cmd -p --model sonnet --output-format json` в пустой папке → выход 0,
   `result=OK`, модель `claude-sonnet-5-5`. Форма запуска с MCP-браузером по-прежнему не проверена (репетиция).
   **Ловушка машины — песочница приложения Claude**: записи сессий приложения в `AppData` ложатся в
   `C:\Users\i_mas\AppData\Local\Packages\Claude_pzs8sxrjxfjjc\LocalCache\…`; `claude.cmd`, браузеры Playwright и
   Mailpit обычный терминал Windows не видит. Прогон запускается только из сессии приложения (инструкция, условие 3).
3. Потолок прогона 8 часов на плечо (инструкция, шаг 5) — оценка Lead; назвать своё, если нужно другое.

## Команда

Оператор — сессия Opus 12.11.2026 (журнал: `lead_degraded` 17:38:45, по замыслу инструкции). Перепроверка 17:38: пакет
`5e55e30f893b0d086b5f3b04aabd2cfa8d1b685d`, `release_fingerprint --check` ok (0.11.0), выход 0; стенд — оба плеча
`{"status":"ok","db":"up"}`, Mailpit :8025/:8026; `claude auth status` → `loggedIn: true`; `config.json` и
`local-tickets\LOCAL-1.md` есть; четыре `LOCAL-1.md` — `7A7FDE710E223B8E…`, два `XPANBFLFA-44.xml` — `A82CB5D9E8E96896…`;
`arm-free\…\qa-factory` → False; оба `settings.local.json` выключают `qa-factory@qafactory`; ветки `exp/fvf-factory`,
`exp/fvf-free`. Сид обоим плечам 17:39:06/08 (38 книг, 8 категорий, 2 пользователя).

Команды старта — дословно шаги 4.1 и 4.2 `RUN-INSTRUCTIONS.md`, с `PYTHONUNBUFFERED=1` и `PLAYWRIGHT_BROWSERS_PATH` =
настоящий путь, логи `runs/factory-1.{log,err}` и `runs/free-1.{log,err}`.

## Ход прогона

(время · плечо · что произошло · pid · лог)

- 17:39:08 · оба · старт в одном вызове · `factory` pid 8072, `free` pid 7840 · `factory-1`, `free-1`
- 17:39:11 · factory · выход 3 на S0 (`kind: halt`): в `local-tickets\LOCAL-1.md` нет строки `# `, первая строка взята
  заголовком · — · `factory-1`. **Кандидат в находку** (запишу после прогона): канонический текст стори, который
  владелец дала без markdown-заголовка, останавливает S0 вопросом человеку — трение двери `file` на первом же шаге.
- 17:41:55 · factory · перезапуск с `--answer answers/ticket-title-go-on.md` · pid 6756 · `factory-2`
- 17:41:59 · factory · выход 3 на S0 (`halt`): нет MR/ветки/коммита у локальной стори · — · `factory-2`
- 17:42:42 · factory · перезапуск с `--answer answers/no-change-current-code.md` · pid 9900 · `factory-3`
- 17:44:5x · factory · выход 3, шлюз источников: оставлен один источник `LOCAL-1`; «стенд `local` не ответил» · — ·
  `factory-3`. **Кандидаты в находки**: (1) строка 3 текста стори называет `task/XPANBFLFA-44.xml` — фабрика его в
  источники не взяла; (2) стенд в ту же минуту отвечал `{"status":"ok","db":"up"}` на `:3000/api/health` — проба
  стенда фабрики дала ложное «не ответил».
- 17:45:27 · factory · перезапуск с `--answer answers/no-tracker.md` · pid 19824 · `factory-4`
- 17:47–17:48 · free · ход 1 закончен: `success`, 47 ходов агента, 526 с; 1 баг (BUG-1 — гость → checkout → вход, страница
  остаётся на `/login?callbackUrl=%2Fcheckout`), 5 вопросов в `out/questions.md`, коммит тестов `db7a6fd` (15 API + 4
  e2e, 18 прошли, 1 красный на BUG-1); снимок текстов хода — `runs/free-out-round1/` · — · `free-1`. Заметка для
  разбора (плечу не сказано): в отчёте «при смене цены админом корзина пересчитывается» записано как «в порядке», а
  слово владельца — цена на момент добавления (Q7: a).
- 17:48 · factory · S1 принят, S2 (requirements tester) идёт · — · `factory-4`
- 17:49:18 · free · продолжение сессии `af326bb4…` с `runs/free-answer-1.md` · pid 16744 · `free-2`
- 17:51:5x · free · **плечо закончило** (ход 2: `success`, 11 ходов, 140 с): 2 бага — BUG-1 (возврат на checkout после
  входа гостя) и BUG-2 (ввод «12» в поле количества корзины даёт 1; плечо само поправило прежнюю запись «12 работает»
  как ошибочную); Q1 закрыт словом владельца «не дефект»; открыты Q2, Q3-остаток, Q4, Q5; коммиты `db7a6fd`, `4687c51`
  (20 тестов: 18 зелёных, 2 красных — на BUG-1 и BUG-2). Неотвеченных вопросов нет, `out/report.md` есть. Стена
  плеча `free`: 17:39:08–17:51:59 ≈ 13 мин; обращений к человеку — 1 (пакет из 5 вопросов) · — · `free-2`
- 17:51 · factory · S2: requirements tester принят (два возврата кодом по R-8 — «implementation-only», «нет
  before/now» в Q4), идёт case critic · — · `factory-4`
- ≈18:10 · factory · выход 3 на S2: критик отклонил тестера требований (не пытался опровергнуть R-12, R-9, R-5, не
  взял R-2; R-1, R-2, R-11 составные), раундов починки не осталось · — · `factory-4`
- 18:10:59 · factory · перезапуск с `--answer answers/s2-critic-restart-as-asked.md` · pid 14024 · `factory-5`
- 18:13 · factory · выход 3 на S2 второй раз на том же месте: `restart` перезапустил КРИТИКА (`S2-qa-case-critic-4`), а
  форма тестера не менялась — тот же вердикт. **Кандидат в находку**: после исчерпания раундов починки двери «вернуть
  работу тестеру со словами критика» нет — есть только принять с дырой, перезапустить критика, починить руками или стоп
  (AR-25: у возвращённого состояния нет хода к исполнителю) · — · `factory-5`
- 18:13:33 · factory · перезапуск с `--answer answers/s2-critic-go-on-with-gap.md` · pid 25124 · `factory-6`
- 18:33:41 · factory · S3 пройден; выход 3 на S4 (`S4-qa-case-designer-2`): 18 открытых вопросов при пороге 6, один пакет.
  **Кандидат в находку**: шесть вопросов — повторы другими словами (Q1=Q10, Q2=Q11, Q3=Q12, Q7=Q16, Q8=Q17,
  Q13≈Q14≈Q18); у вопросов нет ссылки на требования («share … could not be computed»); источники вариантов — «from ?»
  · — · `factory-6`
- 18:35:13 · factory · перезапуск с `--answer answers/s4-questions-batch-1.md` · pid 15600 · `factory-7`
- 18:35–18:44 · factory · «S4: recorded by code — no question answered by a token»: ответ своими словами ушёл роли,
  реестр вопросов его не закрыл («18 open … their answer is the pass»); S4 critic → репетиция гейта A (27 пунктов) →
  дирижёр вернул S3 (`S3-qa-test-strategist-3`) → стратег поднял те же 18 + Q19: «Nothing in your answer settled these
  questions». **Кандидат в находку** (FR-7/FR-8, AR-24): ответ человека по каждому вопросу словами владельца не дошёл до
  реестра, тот же пакет спрошен второй раз тем же текстом · — · `factory-7`
  Разбор (вопрос владельца «почему роль не увидела ответы»): (1) бриф стратега
  `work/briefs/S3-qa-test-strategist-3.md`, строка 49, несёт ответ человека ОБРЕЗАННЫМ до 240 символов — «Q1 … Q2 …
  Q3: T...»; Q3–Q18 стратег не видел; файл целиком (`state/words/…`) бриф не называет, хотя строка 53 обещает «here
  whole or one named file away» (бриф над бюджетом 6144 B, срезка «words at level 1»); (2) отметить вопрос отвеченным
  роль не может: реестр пишет только код по метке, а строка 9 брифа велит держать вопрос открытым «until answered» —
  стратег поднял все 18 заново. **Кандидат в находку** (FR-8, AR-24, AR-21): срезка бюджета брифа режет слова человека.
  **Слова владельца 12.11.2026 ≈ 18:55**: «код не должен урезать бриф, фордж следит за длиной брифа»; «а роль
  адаптировать слова человека для кода и запустить его не может? Дирижёр именно для этого и создавался». Факт по логу
  `runs/factory-7.log`: на ответ своими словами S4 драйвер напечатал «recorded by code — no question answered by a
  token», затем сразу «resume S4-qa-case-designer-2 … their answer is the pass» — строки `conductor:` до репетиции гейта A
  нет: свободный ответ обошёл дирижёра, хотя пакет гейта A сам пишет «Anything else, in your own words, goes to the
  assistant running this story, who turns it into one of these» (P22). Две находки: (а) срезка брифа кодом во время
  прогона (замысел — длину держит фордж при разработке); (б) свободный ответ на пакет вопросов не идёт к дирижёру.
- 18:45:58 · factory · перезапуск с `--answer answers/s3-questions-batch-2-tokens.md` · pid 21528 · `factory-8`
- 18:47 · factory · метки приняты: «recorded by code» 15, «kept open until the report» Q2, Q6, Q11, Q19; выход 3 на гейте A
  (план 10 строк, 10 кейсов, критик `approve_with_concerns`; «S5 cannot start yet: 10 thing(s) the factory still has to
  repair itself — this gate should not have been shown yet»; «the derived scope of S5 is empty»; проба стенда: `POST
  /login` → 405 — **кандидат в находку**: проба входа фабрики ходит не тем методом/путём, стенд жив, `free` входил) ·
  — · `factory-8`
- 18:48:10 · factory · перезапуск с `--answer answers/gate-a-approve.md` · pid 20884 · `factory-9`
- 18:52 · factory · гейт A **второй раз**: `vcs-test-repo` и стенд записаны словом; «the decision did not record by code
  (… `Q19: <letter>` or `Q19: not needed` …)» — хотя Q19 оставлен «until the report» и пакет гейта сам писал «not asked
  again here» (**кандидат в находку**); дирижёр перезапустил критика кейсов (`S4-qa-case-critic-3`, TC-002/004/005/010)
  — снова `reject` по P-2, P-4, P-5, P-10; репетиция: «S5 can start: no», «the derived scope of S5 is empty — … closes
  the stage having tested nothing», вопросы Q2/Q5/Q6 «cannot be answered as it stands». Сама фабрика: «this gate should
  not have been shown yet». Стоп плеча, вопрос владельцу (инструкция п. 0 и 5: блокер). · — · `factory-9`
- 18:56:33 · factory · **слово владельца** (вопрос в этой сессии ≈ 18:55): `approve as is` — пропустить все пункты гейта
  A, дойти до отчёта; перезапуск с `--answer answers/gate-a-approve-as-is.md` · pid 27652 · `factory-10`
- 18:58:58 · factory · гейт A записан (`waiver.py` по «approve as is»); выход 3 на S5 (`kind: conductor`): область S5
  пуста — кейсы пишут строку плана `P-1`, читатель фабрики узнаёт только `TS-1`; дирижёр записал находку FB-5. **Кандидат в
  находку** (AR-22: поле, которое пишет одна роль, не читает код другой) · — · `factory-10`
- 19:02:08 · factory · **слово владельца** (вопрос ≈ 19:00): «скажи фабрике посмотреть список тестов ролью и
  автоматизировать все какие запланированно» → `answers/s5-role-reads-cases-automate-all.md` · pid 23168 · `factory-11`
- 19:03 · factory · выход 3 на S5 второй раз (`kind: conductor`): дирижёр не исполнил слово владельца («the factory cannot
  let the automator pick its own scope»), записал находку FB-6, снова `go on` / `retry` / `stop` · — · `factory-11`
- 19:05:49 · factory · **слово владельца** (вопрос ≈ 19:04): «go on — пустой S5» → `answers/s5-empty-scope-go-on.md`
  (`go on`) · pid 14100 · `factory-12`
- 19:07:18 · factory · выход 3 на S5 **третий раз**: `go on` ушёл дирижёру, не коду; дирижёр судил по прежним словам
  («the person's words ask for automation and not for an empty S5»), записал `go on` замечанием, тот же вопрос с теми же
  вариантами. **Плечо `factory` остановлено** по потолку §5 («стоит третий раз на одном и том же месте»): отчёта нет,
  судится то, что успело (S0–S4, гейт A; S5 без тестов). Находка FV1-13 · — · `factory-12`
- 19:10–19:12 · оператор · по слову владельца открыта кучка `plans/piles/live-run-fvf/` (пачка 1, FV1-1…FV1-13) —
  все кандидаты в находки этого прогона.
- 19:20 · оператор · **слово владельца**: «надо починить блокер и запустить фабрику ещё раз. Плечо свободного агента от
  версии фабрики не зависит»; на вопрос «с нуля или с S5» — «Продолжить с S5». Плечо `free` не перезапускается; плечо
  `factory` после починки FV1-1 продолжает в нынешней копии с S5 ответом `retry` на пакете 0.11.0 + починка (прогон
  смешанных версий: S0–S4 на 0.11.0). Разведка читателя — t-151.
- 19:42:08 · factory · починка FV1-1 (t-152, bb2bd10 в worktree; критик t-152 в работе) наложена на копию
  `C:\QAFactory\exp-fvf\pkg-fix1\qa-factory` = 0.11.0 + две строки (`contract.CASE_PLAN_ROW_RE`,
  `s5_precheck.PLAN_ROW_RE`); сухое чтение: TC-001…TC-010 → P-1…P-10, все есть в плане. Перезапуск с пакета pkg-fix1,
  `--answer answers/s5-retry-after-reader-fix.md` (`retry` — вариант (b) самого дирижёра; **мои** по слову владельца
  «продолжить с S5») · pid 13744 · `factory-13`
- 19:43:36 · factory · область S5 прочиталась (вопроса про пустую область нет); выход 3 `kind: environment`: стенд `local`
  не отвечает. Проверка оператора: верно — весь стенд лежал, PostgreSQL :5433 умер без строки остановки после 17:53
  (`mybooks-stand\logs\postgres.log`), приложение :3000 отвечало 503. Фабрика права, находки нет · — · `factory-13`
- 19:45–19:57 · оператор · `stand.ps1 -Action start -Arm factory`, затем `-Action services`: PostgreSQL поднят (без сида,
  данные целы), `/api/health` → 200.
- 20:01:14 · factory · `answers/s5-stand-up-retry.md` (`retry` — **мои**: стенд поднят, вариант (a) самой фабрики) ·
  pid 10476 · `factory-14`
- 20:03:43 · factory · выход 3 `kind: environment` повторно («did not answer»), но в деталях: `/api/health` → 200, `login:
  failed HTTP 405 — POST /login` — онбординг записал этот отказ как известный (`login_probe: failed`, решение «вход кодом
  невозможен»), S5 всё равно стоит на нём. **Слово владельца** (вопрос ≈ 20:05): «Конфиг проекта». Вопрос владельца: «а как
  делать АПИ тесты если кодом нельзя зайти?» Проверка оператора: вход кодом работает через NextAuth (`/api/auth/csrf` →
  `/api/auth/callback/credentials` → сессия). Находка FV1-15 · — · `factory-14`
- 20:07–20:13 · оператор · в копии плеча `qa-factory\config.json` (копия до правки `config.json.before-harness-login-20261112`):
  `access.kind: harness_command`, команда — собственный тест входа проекта `tests/e2e/auth/login.spec.ts` (выход 0; с неверным
  паролем — 1), `login_probe: ok, seconds 60` (замер 56 с). `env_probe.py --env local` фабрики → `login: ok`, выход 0.
  **Помощь фабрике оператором** — судится в таблице: у `free` такой правки не было.
- 20:14:27 · factory · `answers/s5-login-via-harness-retry.md` (`retry`, **мои** по слову владельца «конфиг проекта») ·
  pid 15460 · `factory-15`
- 20:16:23 · factory · стенд подтверждён («stand `local` answered the check; it is confirmed», проверка 52 с); выход 3
  `kind: stand_identity`: развёрнут ли на `local` коммит `d33d619` репозитория ТЕСТОВ. Находка FV1-16 · — · `factory-15`
- 20:17:19 · factory · `answers/s5-stand-identity-deployed.md` (`deployed` — **мои**: стори проверяет текущий код стенда,
  ответ S0 «current code»; на том же коде шло плечо `free`) · pid 8332 · `factory-16`
- 20:17–20:27 · factory · S5 два окна: W1 (TC-001,002,004,005, API) — отказ проверки манифеста (row-fields-missing), раунд
  отказа у дирижёра; W2 (TC-006,007, UI) — тесты написаны, не запущены: `run_suite` отказал, контракт селекторов профиля
  `playwright-tests` не проверен. Выход 3 `kind: conductor` («declare the selectors in qa-factory/config.json»). Цена к этому
  моменту по строке прогресса драйвера — в чат · — · `factory-16`
- 20:28–20:31 · оператор · проба фабрики `onboarding_probe.py --probe-profiles` → `proven` (тест прошёл, отчёт читается), но
  `selectors_verified` → False (`command_changed`) — находка FV1-18. В копии плеча `selectors: {"verified": true}` (копия
  до правки `config.json.before-selectors-verified-20261112`) → True. **Помощь фабрике оператором** (направление владельца
  «конфиг проекта»).
- 20:31:28 · factory · `answers/s5-selectors-declared-retry.md` (`retry` — **мои**) · pid 24508 · `factory-17`
- ≈20:32 · оператор · **слово владельца**: «не онбординга. Их собирает ранер первого взгляда. Но даже если их нет, то фабрика
  не должна отказывать, раньше фабрика работала и без этого, значит это возможно» → находка FV1-18 переписана: регрессия.
- 20:33:02 · factory · тот же вопрос дирижёра второй раз: `retry` перечитал старую сдачу окна (`halt`, `not_run`), тестов не
  гонял · — · `factory-17`
- 20:33:47 · factory · `answers/s5-selectors-declared-restart.md` (`restart` + слова: селекторы объявлены, проба `proven`,
  прогнать TC-006/007 — **мои**) · pid 22776 · `factory-18`
- 20:34–20:45 · factory · дирижёр освободил окно, `S5-qa-automator-3` (TC-006/007) написал и ПРОГНАЛ тесты (run block
  `20261112T194312786104Z-…json`), но выход 3 `kind: exit_limit`: 8 замечаний проверки — 7 строк манифеста без
  `obligation_refs` и 7 instance id не связаны с id отчёта («not_run (id not in report)»); один resume не помог. Связка id —
  следствие FV1-18 (литерал `verified` без правила join); `obligation_refs` — **кандидат в находку** (роль дважды не
  произвела поле, которого ждёт проверка: FR-38?) · — · `factory-18`
- 20:46:16 · factory · `answers/s5-exit-limit-round-mapping.md` (`round` + два шага: `obligation_refs: [OB-6]/[OB-7]` из
  `work/test-plan.json`, `run_suite --reparse-block … --mapping` — **мои**: подсказка роли из слов самой проверки) ·
  pid 11712 · `factory-19`
- 20:46:51 · factory · `round` со словами не принят («carried extra text… write only the word `round`»), хотя вариант (a)
  обещал «your answer as its instruction»; дирижёр сам перенёс два указания в текст вопроса. Второй экземпляр класса FV1-13
  (дописан в находку). Второй раз на этом месте · — · `factory-19`
- 20:47:41 · factory · `answers/s5-exit-limit-round.md` (`round` — **мои**) · pid 12872 · `factory-20`
- 20:50 · factory · `round` исполнен: «accepted S5-qa-automator-3» (окно 2 TC-006/007 сдано, ушло критику кода
  `S5-qa-code-critic-1`); окно 1 (TC-001/002/004/005) — новый автоматор `S5-qa-automator-4`. Брифы 11 657 B и 13 983 B при
  потолке 6 144 B «after every cut» · — · `factory-20`
- 21:04:03 · factory · выход 3, `exit_limit` S5 окна 1 (`S5-qa-automator-4`): тот же класс, что у окна 2 — 10 строк без
  `obligation_refs`, 14 несвязанных id прогона; проверка сама пишет «This is a repair, not a question for the person».
  Находка **FV1-19**. Первый раз на этом месте (окно 2 на своём месте прошло — решила сама: «место» = окно/диспатч) · — ·
  `factory-20`
- 21:04:43 · factory · `answers/s5-exit-limit-round.md` (`round` — **мои**: тот же ответ, что починил окно 2) · pid 28160 ·
  `factory-21`
- 21:09:06 · factory · выход 3, `exit_limit` окна 1 второй раз (15 мест). Автоматор: «The manifest writer reads no obligation
  marker from TypeScript… needs a person's waiver or a TypeScript marker reader». Проверено: `manifest_from_tests.py` — только
  `ast.parse` (Python). Окно 2 прошло рукописным `obligation_refs: {"obligation_id":"OB-6"}` без хэша — значение из моего
  отклонённого ответа, перенесённого дирижёром: **проход окна 2 = помощь оператора** (в таблицу сравнения). FV1-19 переписана · — ·
  `factory-21`
- 21:10:51 · factory · `answers/s5-exit-limit-go-on.md` (`go on` — **мои**: починка невозможна, `round`/`fresh` упрутся в то же;
  9.1(a) — не останавливающий ход, пробел уходит в гейт B) · pid 24812 · `factory-22`. Роль в окне 1 доложила красные: TC-001
  Then 4, TC-004 Then 1 («merge leaves user cart empty»), TC-005 Then 1
- 21:11:10 · factory · выход 3: `go on` не записан — `waiver.py` отказал блоку из строки проверки с заглушкой
  `<plan obligation id>` («Nothing was recorded»); вопрос вернулся. Живых дверей нет: `round`/`fresh` — нет читателя TS
  (FV1-19), `go on` — заглушка (FV1-13, третий экземпляр), остаётся `stop`. **Третий раз на одном месте** (окно 1 exit_limit:
  21:04, 21:09, 21:11) — плечо остановлено по потолку §5, без отчёта; владельцу · — · `factory-22`
- 21:19–21:23 · владелец: «Чинить и продолжить». Починка t-180 (билдер, 8eb20e4 на ветке `worktree-agent-aaf518a792f694a7e`,
  в main не слита): `_exit_go_on` пишет в `waiver.py` только часть строки до ` — fix: `; та же правка в копии
  `pkg-fix1\qa-factory\scripts\driver_dispatch.py` (diff — идентичны). **Помощь оператора** (починка кода фабрики по ходу) ·
  — · —
- 21:23:15 · factory · `answers/s5-exit-limit-go-on.md` (`go on` — **мои**, тот же ответ после починки) · pid 26196 ·
  `factory-23`
- 21:24:33 · factory · `go on` записан (15 строк `stage_overrides` в `pipeline.json`), автоматор прочёл слова и сдал снова, гейт
  выхода отказал теми же строками, драйвер задал тот же вопрос («already resumed… no second resume»). Неясный баг — диагноз
  критику t-185 (по правилу 3) · — · `factory-23`
- 21:36 · разбор t-185: находку `row-fields-missing` проверка не пропускает ни по какому слову — `go on` здесь не сработает
  никогда; починка есть (фрагмент `obligation_refs` без хэша через `manifest_put.py`), но текст отказа её запрещает. Решила сама
  (в русле «чинить и продолжить»): A1 только на копии прогона — текст отказа называет дверь фрагмента (t-186), затем голый
  `round`, чтобы роль чинила сама без слов оператора. **Помощь оператора** (правка кода по ходу) · — · —
- 21:40:00 · factory · t-186 принят (копия `s5_precheck.py.before-t186` рядом); `answers/s5-exit-limit-round.md` (`round` —
  **мои**) · pid 21512 · `factory-24`
- 21:4x · factory · `round` исполнен: окно 1 **сдано** (`accepted S5-qa-automator-4` — роль починила `obligation_refs` по
  новому тексту отказа, без слов оператора); окно 2 — возврат по F-1/F-2 критика (`S5-qa-automator-5`, принят); критик окна 1
  `S5-qa-code-critic-2`: verdict `concerns`, все 10 `unverified`, проб не запускал, F-1/F-2 механические с `blocking: false` ·
  — · `factory-24`
- 21:49:58 · factory · выход 3, `repair_limit` S5 окна 1: «critic sent the tests back without naming a blocking finding»; варианты
  `round` (раунд 2 из 2) / `debt` / `fixed` / `stop` · — · `factory-24`
- 21:51:10 · factory · `answers/s5-exit-limit-round.md` (`round` — **мои**: F-1/F-2 — настоящие механические правки P29; `debt`
  сразу дал бы «not ready») · pid 24356 · `factory-25`
- 21:52:00 · factory · выход 3, `conductor` S5: `round` ушёл не автору, а дирижёру (финиш критика отказал: нет окна ревью и проб
  чувствительности). Критик-2 — 13 ходов, 70 с, файл модели проб не написан, причины нет. Дирижёр: «The factory cannot produce the
  probes» — неправда (отказ называет `probe_by_code.py`). Находка **FV1-20** · — · `factory-25`
- 21:52:35 · factory · `answers/s5-critic-restart.md` (`restart` — **мои**: новый критик должен записать окно и прогнать пробы;
  `go on` закрыл бы S5 непроверенным) · pid 8780 · `factory-26`
- 21:54:45 · factory · выход 3, `repair_limit` S5 снова: `S5-qa-code-critic-3` тоже без проб («probe models not written; stand
  login probe contradicts itself»), F-1/F-2 те же. Третий раз на месте критика окна 1 — по потолку §5 владельцу · — · `factory-26`
- 21:56 · владелец: «Продолжать через пробел» (`round`, затем `go on` у дирижёра; S5 закрывается с пробелом «окно критика без
  проб»).
- 21:56:56 · factory · `answers/s5-exit-limit-round.md` (`round` — **владельца** по выбранному варианту) · pid 11876 ·
  `factory-27`
- 21:57:11 · factory · выход 3, `refusal` S5: «round 3 came back with the same 1 finding(s) as round 2 — no further rework»;
  `retry / go on / stop` · — · `factory-27`
- 21:57:48 · factory · `answers/s5-exit-limit-go-on.md` (`go on` — **владельца**: «продолжать через пробел») · pid 25424 ·
  `factory-28`
- 21:58:43 · factory · дирижёр записал 3 пропуска (блок = целая строка отказа); строки чувствительности прошли, строка
  `review_receipt_ref` нет — отказ сам называет дверь `--block "not receipted"`, дирижёр её не взял (класс FV1-13/FV1-19: блок из
  целой строки) · — · `factory-28`
- 21:59:32 · factory · `go on` повторно — **владельца** (тот же выбор) · pid 26468 · `factory-29`
- 22:00:19 · factory · дирижёр снова записал блок целой строкой, гейт тот же; «You have answered this exact question before» ·
  — · `factory-29`
- 22:00:59 · factory · `answers/s5-go-on-not-receipted.md` (`go on` — **владельца**; дверь `--block "not receipted"` из текста
  самого отказа — **мои**, **помощь оператора**) · pid 20772 · `factory-30`
- 22:01–22:10 · factory · дирижёр записал `--block "not receipted"` — критик-3 принят; автоматор-6 (F-1/F-2) принят; критик-4
  вернул окно 1: «Then 2 expects [[B,3]] equal to the pre-existing user line, so a no-op merge passes» (TC-004, дефект теста) ·
  — · `factory-30`
- 22:10:44 · factory · выход 3, `repair_limit` (лимит 2 раунда исчерпан) · — · `factory-30`
- 22:11:15 · factory · `answers/s5-exit-limit-round.md` (`round` — **мои**: настоящий дефект теста, `debt` оставил бы
  пустую проверку) · pid 11356 · `factory-31`
- 22:11–22:17 · factory · критик-4 принят, автоматор-7 (дефект TC-004 Then 2) принят; критик-5 — снова без проб («probe_by_code
  needs a per-check model file; not written»), F-1/F-2 неблокирующие; выход 3 `repair_limit` («without naming a blocking
  finding», round 4 при лимите 2) · — · `factory-31`
- 22:18:28 · factory · `answers/s5-critic-debt.md` (`debt` — **мои** в русле слова владельца «продолжать через пробел»: ещё
  `round` — тот же круг без проб; вердикт и так «не готово» из-за найденных багов) · pid 18416 · `factory-32`
- 22:25:37 · factory · окно 1 закрыто долгом; критик-6 окна 2 (TC-006/007): `probe_by_code` → `not_executed` (0 of 8, tooling),
  находок блокирующих нет; выход 3 `repair_limit` · — · `factory-32`
- 22:26:17 · factory · `answers/s5-critic-debt.md` (`debt` — **мои**, та же логика) · pid 20748 · `factory-33`
- 22:28:34 · factory · выход 3, `conductor`: 49 пробелов окна 2 (нет `critic_verdict`, нет проб); дирижёр разобрал сам — инструмент
  проб не выбирает тест Playwright по названию, записал FB-9 · — · `factory-33`
- 22:29:20 · factory · `answers/s5-probe-gap-go-on.md` (`go on` + фраза принятия пробела — **владельца** по классу «продолжать
  через пробел») · pid 28012 · `factory-34`
- 22:29–22:37 · factory · дирижёр записал `probe gap: TC-006/007`, затем отказ финиша → FB-10, rework автоматору-8 (принят),
  критик-7 — снова «without naming a blocking finding»; выход 3 `repair_limit` · — · `factory-34`
- 22:38 · factory · `answers/s5-critic-debt.md` (`debt` — **мои**, та же логика) · `factory-35`
- 22:38–22:45 · factory · `debt` ушёл дирижёру (отказ финиша), FB-11, rework автоматору-9 (принят); выход 3 `conductor`:
  «go on — open findings go to gate B as a named debt» · — · `factory-35`
- 22:46 · factory · `answers/s5-exit-limit-go-on.md` (`go on` — **владельца** по классу «продолжать через пробел») · `factory-36`
  → дирижёр записал заметку вместо долга (писателя долга у него нет), тот же вопрос вернулся в 22:47 (FV1-13, четвёртый
  экземпляр). Долг critic-7 был записан ещё в 22:38, но стадия после него пустила раунд автора `S5-qa-automator-9`.
- 22:50 · factory · `answers/s5-conductor-retry-review-repair.md` (`retry` + строка причины — **мои** слова, помощь оператора:
  единственная исполнимая дверь — обзор критиком уже сделанного ремонта) · `factory-37`
  → критик-8 (22:50–23:01): TC-006/007 `unverified`, статически чисто, проба not_executed (FB-9), вердикт concerns без
  блокирующих находок; вопрос `repair_limit` (review / debt / stop).
- 23:01 · factory · `answers/s5-critic-debt.md` (`debt` — **владельца** по классу «продолжать через пробел») · `factory-38`
  → долг записан; финиш critic-8 отказал ×7: хэши `obligation_refs` TC-006/007, вписанные автором-9 руками, не совпадают
  с планом (FV1-19: дверь t-186 неполна, хэш ссылки строит только путь маркера Python).
- 23:04 · factory · `answers/s5-refusal-hash-go-on.md` (`go on` — **владельца** по классу «продолжать через пробел»; строка
  причины — **мои** слова) · `factory-39`
  → не прошёл: отказ финиша словом не снимается (как R1 разбора t-185); слова ушли критику-8, тот же вопрос вернулся 23:05.
- 23:06 · operator · **помощь оператора**: фрагмент `manifest_put.py` (ревизия 43) с хэшами ссылок OB-6/OB-7 из плана
  (`content_hash` обязательства) для 7 строк TC-006/007; попутно `manifest_put` сам переписал строку «TC-001 Then 4 fresh
  session…» в «current spelling» (не просили). Фрагмент — scratchpad сессии, не в репо.
- 23:06 · factory · `answers/s5-refusal-retry-after-hash-fix.md` (`retry` — **мои**) · `factory-40`
  → 23:07 S5 принята (окно 2 — `probe_gap` в отчёт). S6: раннер-1 (23:07–23:19) автотесты 18 прошли / 1 упал; TC-008, TC-010
  не проверены руками (Q5 гейта A без ответа); раннер-2 ручной TC-009 (72 улики) принят 23:33.
  S7: аналитик-1 — TC-005 TEST_BUG (общая cookie гостей, `cartClient.ts:29`); финиш отказывает приёмке S6 (нет
  `failure_class`/`quote` в форме); дирижёр трижды `rework` аналитика с `--cause tooling` (аналитики 2, 3, 4: 23:53, 00:13,
  00:37), ремонт автору не идёт. 00:57 — вопрос дирижёру S7 (новый отказ: нет строки `inputs_read` раннера). FV1-22.
  Строка прогресса весь S7 пишет «S6 Run» (мелочь).
- 13.11 ≈ 01:00 · **слово владельца** «Остановить плечо» (потолок §5, третий повтор на одном месте). Плечо `factory`
  остановлено: S0–S6 пройдены, S7 не закрыт, гейт B не достигнут; вопрос 00:57 оставлен без ответа.

## Журнал вопросов и ответов

(время · плечо · вопрос одной строкой · файл ответа · чьи слова: владельца / заготовка / «мои» и почему)

- 17:41 · factory · S0: нет заголовка `# ` в тексте стори, взять первую строку? · `answers/ticket-title-go-on.md`
  («go on») · **мои**: заготовки нет; RUNBOOK 9.1(a) — самое консервативное и не останавливающее; правка текста
  (`retry`/вставка) изменила бы стори только одному плечу, а текст обязан быть один на оба.
- 17:42 · factory · S0: нет MR/ветки/коммита — на чём тестировать? · `answers/no-change-current-code.md`
  («current code», рекомендация фабрики) · **мои по смыслу слов владельца** (`no-tracker.md`: «проверяем, что
  функционал работает»; выгрузка — то, что уже сделано) — плечо `free` тестирует тот же текущий код.
- 17:45 · factory · S1 шлюз источников: согласны с таблицей (только LOCAL-1)? стенд не ответил ·
  `answers/no-tracker.md` · **владельца** (12.11.2026; тема «есть ли тикет, где требования» + «Stand ok»).
- 17:49 · free · 5 вопросов `out/questions.md` · `runs/free-answer-1.md`: Q1 (блокированная кнопка Out of Stock вместо
  сообщения) — `answers/out-of-stock-disabled-button.md`, **владельца** («Q5: a»); Q3 (поле количества в корзине) —
  `answers/cart-quantity-multidigit.md`, **владельца** («Q3: a», «12» → 12) + `no-decision-yet.md` на остальное;
  Q2 (остаток ниже количества в корзине), Q4 (нет резерва), Q5 (`sessionId` в `GET /api/cart`) — `no-decision-yet.md`
  (заготовка; в таблице слов владельца этих тем нет). Последняя строка файла — «обновить report/bugs/questions» —
  **мои** (операционная, о продукте ничего).
- 18:10 · factory · S2: критик отклонил, раундов нет — принять с дырой или перезапуск со словами? ·
  `answers/s2-critic-restart-as-asked.md` («restart», слова — пересказ требований самого критика фабрики) · **мои**:
  заготовки на этот смысл нет (`thinking-roles/answers/s2-critic-*` — о плейсхолдере формы); 9.1(a) — не
  останавливает; `go on` унёс бы дыру S2 в отчёт, перезапуск даёт фабрике доделать своё без знания извне. Плечу
  `free` этот смысл не задавался (внутренний гейт фабрики).
- 18:13 · factory · S2 то же место повторно (после `restart` критика) · `answers/s2-critic-go-on-with-gap.md` («go on»,
  дыра — открытым пунктом в отчёт) · **мои**: перезапуск критика доказанно не меняет вердикт; `retry` — работа
  оператора за фабрику (портит сравнение); `stop` — останавливает. Дыра S2 судится в отчёте как есть.
- 18:35 · factory · S4, 18 вопросов · `answers/s4-questions-batch-1.md`. По строкам: **владельца** — Q1/Q10 (кнопка
  Out of Stock, карточка 16, «Q5: a»; тот же текст, что плечу `free` на его Q1), Q3/Q12 (слияние — большее, AUTH.md,
  карточка 10), Q8/Q17 и R-8 в Q5 (0, −1, 1.5, «abc» — отклонять с сообщением, карточка 1, Jira 140); **заготовка
  `no-decision-yet`** — Q2/Q11 (cookie или local storage), Q6 (округление), Q7/Q16 и R-10 (повторное добавление —
  одна строка; карточка 22 из «решать владельцу» соседняя); **мои** (9.1(a), самое консервативное: защитные нормы
  действуют) — Q4 кроме повторного добавления, Q9, Q13, Q14, Q15, Q18, R-11/R-12 в Q5 (изоляция чужой корзины, не
  больше остатка, неудачное добавление ничего не меняет). Плечо `free` эти нормы приняло само, не спрашивая.
- 18:45 · factory · тот же пакет повторно (S3, 19 вопросов) · `answers/s3-questions-batch-2-tokens.md` — закрытые
  метки строкой (`question_register.parse_choices` читает только целую строку `Qn: <буква|not needed|until the
  report>`) + слова владельца ниже для роли. По строкам: Q3/Q12 «a», Q8/Q17/Q5 «a» (отклонять — **владельца**, с
  сообщением — словами ниже); Q1 «b», Q10 «a» — **мои по смыслу слова владельца** (кнопка Out of Stock верна → точный
  текст «Out of stock» не требуется); Q2/Q11/Q6/Q19 «until the report» (= `no-decision-yet`); Q4/Q7/Q16 «a» — **мои**,
  смена против первого ответа («решения нет» на повторное добавление): свободная форма не закрывает, а «until the
  report» на Q4 оставил бы открытыми и нормы остатка; Q9/Q13/Q14/Q15/Q18 «a» — **мои** (защитные нормы).
- 18:48 · factory · гейт A · `answers/gate-a-approve.md`: `approve` — **заготовка** (`thinking-roles/answers/approve.md`);
  `vcs-test-repo: accept go on on this branch` — **мои** (незакоммичены только файлы подготовки прогона; `free` их тоже
  не коммитил); `environment-1: accept Stand ok …` — **владельца** по классу («стенд ок», `stand-ok.md`, P5 — одно
  решение на класс). Свои пункты фабрики (пустая область S5, 10 починок, ревью P-2/P-4/P-5/P-10) словом НЕ пропущены.
- 18:55 · factory · гейт A не записан (Q19 «until the report» + свои пункты) · `answers/gate-a-approve-as-is.md`
  (`approve as is`) · **владельца** (ответ на вопрос оператора).
- 19:02 · factory · S5: область пуста (`P-n` против `TS-n`) · `answers/s5-role-reads-cases-automate-all.md` ·
  **владельца**: «скажи фабрике посмотреть список тестов ролью и автоматизировать все какие запланированно».
- 19:05 · factory · S5 повторно (дирижёр отказал) · `answers/s5-empty-scope-go-on.md` (`go on`) · **владельца**:
  «go on — пустой S5». Не исполнено фабрикой (FV1-13); третьего ответа не было — плечо остановлено по потолку.

## Утром владельцу

(докуда дошло каждое плечо · таблица · что решать · ответы «мои» на подтверждение)

### Итог LR2-1 (13.11.2026 ≈ 02:00, оператор Opus, окно `lead_degraded` с 12.11 17:38:45)

- **Докуда дошли.** `free` — до отчёта за ~12 мин, один раунд вопросов (5), вердикт «не готово к поставке (два бага)».
  `factory` — S0–S6 пройдены, S7 не закрыт (петля FV1-22), гейт B и отчёт не достигнуты; остановлено словом владельца
  13.11 ≈ 01:00; 7 ч 18 мин, 40 вопросов драйвера (30 на S5), помощь оператора не меньше 8 раз.
- **Таблица** — `factory-vs-free-agent.md`, «Таблица» (слепая оценка `runs/blind-eval.md`, ключ `runs/blind-key.txt`:
  X = free, Y = factory). Фабрика хуже в а, б, в, е, ж, з, и, к, л; поровну г; д зависит от версии правды; лучше — ни в одной.
  По правилу стопа — находки FV1-23…FV1-26 (новые классы) и FV1-13…FV1-22 (петли) в кучке `live-run-fvf`; стоп до разбора.
- **Время S5 (обещано 12.11 ≈ 18:00)**, `state/driver-runs.jsonl`: стена S5 248 мин (17:57–22:05 UTC); из них модели —
  108 мин (автоматор 35 вызовов / 60 мин, критик кода 11 / 25 мин, дирижёр 27 / 23 мин). Остальные ~140 мин — ожидание
  ответов, шаги кода и починки оператора t-180/t-186 (по «Ходу прогона»; точнее не разложено — оценка). Стена S2–S4 —
  29/31/32 мин; S7 — 77 мин (петля).
- **Решать владельцу:**
  1. Версия правды: таблица считает карточки 11 и 13 багами, а карточку 20 — «решать владельцу»; `SUMMARY.md` несёт твои слова
     05.11: 11 и 13 — «не баг», 20 — «снята». От этого строки (б) «из 8 или из 6» и (д) «ложный pass 0–2 у free».
  2. Неуверенные места оценщика (карточки 2, 3/23, 22; строка е у фабрики) — руками их проходит Lead владельца, не оператор.
  3. Ответы «мои» на подтверждение: `answers/s5-conductor-retry-review-repair.md`, `s5-refusal-hash-go-on.md` (строка
     причины), `s5-refusal-retry-after-hash-fix.md`, `s5-go-on-not-receipted.md`, `s5-probe-gap-go-on.md`; помощь — хэши
     фрагментом `manifest_put` (23:06).
- Цена — в чате (P18): обе цифры сведены из двух источников.

- Обещано владельцу 12.11 ≈ 18:00 (её вопрос «почему наш автоматор в ~10 раз медленнее»): после S5 разложить время S5
  фабрики по `state/driver-timings.jsonl` и транскриптам ролей на (1) S0–S4 до первого теста, (2) передачи и холодный
  старт сессий, (3) привязку Then, красные пробы, гейт выхода и критика, (4) сам код тестов — против 13 мин `free`.
- Вопрос владельца 12.11 ≈ 18:15: «откуда критик в S2, там же первый взгляд, смоук». Факт пакета 0.11.0: S2 —
  «Understanding and size» (реестр требований, противоречия, размер); `references/stages.json` у S2 —
  `roles: [qa-requirements-tester, qa-case-critic]`, `acceptance_by: qa-case-critic`; карточка `phases/s2.md` —
  «One dispatch», одна роль (**кандидат в находку**: карточка и реестр стадии расходятся). Смоука/первого взгляда на
  стенд в S2 нет ни там, ни там. **Решать владельцу**: если замысел S2 — первый взгляд со смоуком, пакет от него ушёл.
