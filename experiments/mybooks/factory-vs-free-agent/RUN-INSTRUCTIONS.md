# Инструкция оператору: прогон «фабрика против свободного агента» (узел `live-runs/2/LR2-1`)

Для кого: сессия Claude Code на Opus, открытая в корне этого репозитория, которая ведёт прогон по слову владельца.
Написана Lead 12.11.2026. Всё, что здесь сказано «не проверено на живом прогоне», проверяется репетицией (шаг 3) до
настоящего старта; что репетиция опровергла — исправить здесь же тем же ходом.

## 0. Что это и зачем

Идея владельца (12.11.2026): фабрика делает то же, что свободный агент с одним промтом, или больше, но качественнее и
предсказуемее; делает меньше — работает неправильно. «Лучше» — это вернее отражать положение вещей, а не давать больше
багов. Прогон — детектор этой идеи: одна стори MyBooks («Add to Cart»), **два плеча параллельно**:

| | Плечо `factory` | Плечо `free` |
|---|---|---|
| Кто | фабрика целиком, S0–S9, драйвер `story_run.py`, роли на Sonnet | одна сессия `claude -p` на Sonnet с промтом `free-agent-prompt.md` |
| Знание онбординга | есть (`qa-factory/` в тестовом репозитории) | **нет** — папки `qa-factory/` в его копии нет вовсе |
| Стенд | `http://localhost:3000`, база `bookstore`, почта `:8025` | `http://localhost:3001`, база `bookstore_free`, почта `:8026` |
| Папка | `C:\QAFactory\mybooks-stand\arm-factory\` | `C:\QAFactory\mybooks-stand\arm-free\` |

Читать до начала: `PROJECT.md` («Прогоны и эксперименты», P5, P8, P13, P18, P20), `docs/RUNBOOK.md` §9 (мандат ночного
оператора 9.1, остановки 9.4, правила 9.6) и §11, находку
`plans/piles/live-runs/findings/20261112-plecho-svobodnogo-agenta-v-sravnitelnom-progone.md`, таблицу сверки
`factory-vs-free-agent.md`, `answers/README.md`.

Твой тир — Opus (Role ≠ tier в `CLAUDE.md`): ведёшь прогон, отвечаешь плечам, пишешь тетрадь и журнал; механизмы,
`DECISIONS.md`, статусы и правила не меняешь — предложение идёт находкой. Пакет на время прогона заморожен: дефект
фабрики, найденный прогоном, НЕ чинится на ходу (это испортит сравнение), а записывается находкой в кучку и в тетрадь;
плечо `factory` идёт дальше тем, что есть. Исключение — блокер, без которого плечо не доходит до отчёта: тогда стоп
плеча, запись, вопрос владельцу.

## 1. Жёсткие правила

- Рабочий каталог шелла не менять никогда: `git -C`, `npm --prefix`, `Start-Process -WorkingDirectory`, абсолютные пути.
- Следов нет (P8): никакого push, PR, записи в трекер из копий плеч.
- Ничего не удалять: ненужное переименовывать. Сид (`stand.ps1 -Action seed`) — единственное разрешённое стирание, и
  только базы своего плеча.
- Секреты (`.env`, `.env.local`) не печатать и не писать в тетрадь; в тетрадь — только sha256 файлов.
- Деньги — в чат владельцу, не в файлы (P18).
- Плечам отвечать одними словами (`answers/README.md`); свой ответ помечать «мои» и никогда не выдавать за слово владельца.
- Плечо `free` не получает ничего из `qa-factory/`, из пакета фабрики, из этого репозитория и из `experiments/` — ни
  файлом, ни подсказкой в ответе. Ответ плечу — только слова владельца продукта о поведении продукта.
- Оценщик не знает, чьё плечо (`factory-vs-free-agent.md`, «Как судят»).

## 2. Условия старта — проверить все семь, каждое записать в «Подготовку» тетради

1. **Релиз фабрики вышел, и пакет заморожен.** Владелец называет тег или коммит релиза. Заморозка — неподвижное рабочее
   дерево вне репозитория:
   `git -C C:\QAFactory\forge-repo worktree add --detach C:\QAFactory\exp-fvf\pkg <коммит релиза>`;
   пакет драйвера — `C:\QAFactory\exp-fvf\pkg\ai-packages\qa-factory`. Проверка: `git -C C:\QAFactory\exp-fvf\pkg rev-parse HEAD`
   равен названному коммиту; `Test-Path` на `...\scripts\story_run.py` и `...\.claude-plugin\plugin.json`.
2. **Стенд жив и чист.**
   `powershell -NoProfile -ExecutionPolicy Bypass -File experiments\mybooks\factory-vs-free-agent\stand\stand.ps1 -Action status`
   — PostgreSQL слушает, оба приложения отвечают `{"status":"ok","db":"up"}`, оба Mailpit слушают. Не так —
   `-Action services`, затем `-Action start -Arm factory` и `-Arm free`. Прямо перед стартом — `-Action seed` обоим плечам.
   После перезагрузки машины ничего само не поднимается: те же три команды.
3. **`claude` вошёл в аккаунт.** `claude --version` печатает версию; вход делает ТОЛЬКО владелец (`claude`, затем `/login`).
   Проверка без траты: шаг 3 (репетиция) — она же проверка входа. Отказ входа или лимит — выход 5 драйвера, RUNBOOK 9.4.
4. **Плечо `factory` онбордено здесь релизной версией** (слово владельца 12.11.2026: «Да, заново здесь»). Порядок:
   (а) релизный плагин ставится так, как его ставит новый пользователь (`ai-packages/qa-factory/INSTALL.md`):
   `claude plugin marketplace add Xartaxana/QAFactory`, `claude plugin install qa-factory@qafactory`;
   (б) в папке `C:\QAFactory\mybooks-stand\arm-factory\test-automation-framework` — `/qa-factory:qa-doctor`, затем
   `/qa-factory:qa-onboarding`. Онбординг — разговор с человеком: его ведёт владелец или оператор при ней; ответы по
   фактам стенда — RUNBOOK §11, последний пункт (`tests_root: "."`, `code_repos: [{name: MyBooks, path: ../MyBooks,
   default_branch: main}]`, задачи — адаптер `file`, трекера нет, среда — локальный стенд `http://localhost:3000`).
   Запуск онбординга без человека (`claude -p`) **не проверен на живом прогоне**;
   (в) время и цена онбординга записываются в тетрадь отдельной строкой: это вклад фабрики, которого у плеча `free` нет,
   и в таблице он виден отдельно от прогона стори;
   (г) после онбординга: есть `qa-factory\config.json`; текст стори кладётся фабрике её дверью —
   `Copy-Item <копия>\task\LOCAL-1.md <копия>\qa-factory\local-tickets\LOCAL-1.md` (папку создать, если её нет).
   Без `config.json` драйвер выходит с 3 «no qa-factory/config.json».
5. **Текст стори один на оба плеча, трекера нет ни у кого** (слова владельца 12.11.2026). Канон —
   `experiments/mybooks/factory-vs-free-agent/story/LOCAL-1.md`; в обеих копиях тестов уже лежат `task\LOCAL-1.md` и
   `task\XPANBFLFA-44.xml` (выгрузка прежней стори, на неё ссылается текст). `Get-FileHash` трёх файлов `LOCAL-1.md`
   (два в `task\`, один в `qa-factory\local-tickets\`) совпадает, обоих `XPANBFLFA-44.xml` — тоже; хэши в тетрадь.
   Выгрузку в этот репозиторий не коммитить (корпоративная Jira, репозиторий публичный).
6. **Промт `free`** утверждён владельцем 12.11.2026. Заполненный текст кладётся в `runs/free-prompt-final.md` (только
   текст между линиями `=====` из `free-agent-prompt.md`; подстановки: текст стори дословно из `story/LOCAL-1.md`, команда
   сида
   `powershell -NoProfile -ExecutionPolicy Bypass -File C:\QAFactory\forge-repo\experiments\mybooks\factory-vs-free-agent\stand\stand.ps1 -Action seed -Arm free`).
7. **Плечо `free` чисто от фабрики.** `Test-Path C:\QAFactory\mybooks-stand\arm-free\test-automation-framework\qa-factory`
   → `False`. Если плагин `qa-factory` установлен на машине (`claude plugin list`), в копии плеча лежит
   `.claude\settings.local.json` с `{"enabledPlugins": {"<id плагина>": false}}`. То же — в копии плеча `factory`, если
   плагин установлен: драйвер берёт пакет из `--plugin-dir`, а установленный дал бы смесь поколений (вопрос вида `package`).

Перед стартом в обеих копиях — своя ветка, чтобы коммиты тестов не легли на `main` копии:
`git -C <копия тестов> switch -c exp/fvf-factory` и `exp/fvf-free` (это копии плеч, не чекаут владельца).

## 3. Репетиция (обязательна; ролей фабрики не запускает)

1. Сухой прогон драйвера:
   `python C:\QAFactory\exp-fvf\pkg\ai-packages\qa-factory\scripts\story_run.py --task LOCAL-1 --env <имя среды из config.json> --model sonnet --no-trace --plugin-dir C:\QAFactory\exp-fvf\pkg\ai-packages\qa-factory --project C:\QAFactory\mybooks-stand\arm-factory\test-automation-framework --dry-run`
   — печатает, что сделал бы; ошибок нет.
2. Проба формы запуска `free` на пустой папке `C:\QAFactory\exp-fvf\smoke` (создать): та же команда, что в шаге 4.2, но
   промт — файл с одной строкой `Open http://localhost:3001 in the browser, read the page title, write it to out/title.txt, then stop.`
   Смотреть: процесс завершился, в логе JSON с `session_id` и `result`, файл `out\title.txt` есть, браузер MCP вызвался
   без запроса разрешения. Запрос разрешения или отказ инструмента — поправить флаги (`--allowedTools`,
   `--permission-mode`) здесь и в шаге 4.2 и повторить. Форма запуска `free` **не проверена на живом прогоне** — эта
   проба и есть проверка.
   Известная ловушка этой машины (тетрадь, «Ловушка машины»): распаковщик браузеров Playwright зависает на Node 26 на
   строке «extracting archive». `stand/free-mcp.json` поэтому даёт MCP-браузеру готовый `chrome.exe` через
   `--executable-path`; если проба всё равно висит дольше двух минут без вывода — смотреть процессы `node.exe` с
   `oopDownloadBrowserMain` в командной строке и распаковать нужный архив руками, как описано в тетради. То же проверить
   у плеча `factory` до старта: рекордер фабрики (`manual_capture.py`) должен открыть браузер — один ручной вызов по
   подсказке `--dry-run` или первый же шаг S6 покажет; зависание там — блокер машины, не дефект фабрики.
3. Проба продолжения сессии: `claude -p --resume <session_id из пробы> --model sonnet` с вводом `Now write "ok" to out/ok.txt`
   — файл появился в той же папке.

## 4. Старт — оба плеча в одном окне времени

Оба процесса отцеплены от сессии (`Start-Process`), вывод в файлы; `N` в имени лога растёт на каждый запуск.

**4.1. Плечо `factory`:**

```powershell
$env:PYTHONUNBUFFERED = "1"
Start-Process -FilePath python -WorkingDirectory "C:\QAFactory\mybooks-stand\arm-factory\test-automation-framework" `
  -ArgumentList "C:\QAFactory\exp-fvf\pkg\ai-packages\qa-factory\scripts\story_run.py","--task","LOCAL-1","--env","<имя среды>","--model","sonnet","--no-trace","--plugin-dir","C:\QAFactory\exp-fvf\pkg\ai-packages\qa-factory" `
  -RedirectStandardOutput "C:\QAFactory\forge-repo\experiments\mybooks\factory-vs-free-agent\runs\factory-1.log" `
  -RedirectStandardError "C:\QAFactory\forge-repo\experiments\mybooks\factory-vs-free-agent\runs\factory-1.err" -PassThru
```

**4.2. Плечо `free`** (промт идёт на stdin из файла):

```powershell
Start-Process -FilePath "$env:APPDATA\npm\claude.cmd" -WorkingDirectory "C:\QAFactory\mybooks-stand\arm-free\test-automation-framework" `
  -ArgumentList "-p","--model","sonnet","--output-format","json","--permission-mode","acceptEdits","--allowedTools","Bash,Read,Write,Edit,Glob,Grep,Task,WebFetch,mcp__playwright","--mcp-config","C:\QAFactory\forge-repo\experiments\mybooks\factory-vs-free-agent\stand\free-mcp.json" `
  -RedirectStandardInput "C:\QAFactory\forge-repo\experiments\mybooks\factory-vs-free-agent\runs\free-prompt-final.md" `
  -RedirectStandardOutput "C:\QAFactory\forge-repo\experiments\mybooks\factory-vs-free-agent\runs\free-1.log" `
  -RedirectStandardError "C:\QAFactory\forge-repo\experiments\mybooks\factory-vs-free-agent\runs\free-1.err" -PassThru
```

Одинаковая параллельность: плечу `free` разрешён инструмент `Task` (свои подагенты), фабрика параллелит сама; сколько
каждое плечо шло одновременно — записать в тетрадь по логам, не уравнивать руками.

В тетрадь сразу: время, pid обоих, имена логов, коммит пакета. Через две минуты — `Get-Process -Id <pid>` и хвост `.err`.

## 5. Ведение прогона

**Плечо `factory`** — по RUNBOOK 9.4: драйвер выходит кодом, а не ждёт. Выход 3 — вопрос в
`<копия>\qa-factory\artifacts\LOCAL-1\state\driver-question.md`; ответ — файл из `answers/` и та же команда с
`"--answer","<файл>"` и следующим номером лога. Выход 5 — повтор той же команды (до трёх раз с паузой 5 минут). Выход 4 —
причина в том же файле; блокер фабрики не чинить (п. 0), записать и спросить владельца.

**Плечо `free`** — процесс завершается, когда агент закончил ход. В `free-N.log` — JSON: `session_id`, `result`,
`num_turns`, `total_cost_usd`. Если в копии есть `out\questions.md` с неотвеченными вопросами — ответить теми же словами,
что фабрике (`answers/README.md`), одним файлом `runs\free-answer-N.md`, и продолжить ту же сессию: та же команда 4.2 с
`"--resume","<session_id>"` в аргументах, `-RedirectStandardInput` на файл ответа, лог `free-<N+1>.log`. Вопросов нет и
`out\report.md` есть — плечо закончило.

Вопросы плеч приходят в разное время. Порядок: ответ записывается файлом в `answers/` при первом появлении; второму плечу
на тот же смысл уходит ТОТ ЖЕ файл. Каждая строка — в «Журнал вопросов и ответов» тетради: время, плечо, вопрос одной
строкой, файл ответа, чьи слова (владельца / заготовка / «мои» с причиной).

Ожидание: уведомление harness о завершении или ограниченная проверка (`Get-Process -Id`, хвост лога,
`driver-runs.jsonl`); бесконечных циклов `until` не ставить (RUNBOOK 9.8). Сообщений владельцу во время прогона нет,
кроме трёх случаев: вход в `claude` слетел; стенд упал и `stand.ps1` его не поднимает; плечо остановлено блокером.

Потолок: плечо, которое не дало отчёта за 8 часов стены или стоит третий раз на одном и том же месте, останавливается;
то, что оно успело, судится как есть, причина — в тетрадь. (Число 8 — оценка Lead, не замер; владелец может назвать своё.)

## 6. После прогона

1. Снять исходы: у `factory` — `qa-factory\artifacts\LOCAL-1\test-report.md`, черновики багов, реестр требований,
   `work\exploratory-findings.jsonl`, `state\driver-runs.jsonl`; у `free` — `out\report.md`, `out\bugs\`, `out\questions.md`,
   `out\evidence\`, тесты (`git -C <копия> log --stat main..HEAD`). Скопировать в `runs\factory-out\` и `runs\free-out\`
   (улики-картинки не копировать, только пути).
2. Для строки «потеряно между работой и отчётом»: у `factory` — сверить `work\exploratory-findings.jsonl`, строки
   `surprise:` рекордера и черновики багов с отчётом; у `free` — сверить `out\evidence\` и текст `result` в логах с
   `out\report.md`.
3. Привести исходы к одной форме, ослепить, отдать оценщику — `factory-vs-free-agent.md`, «Как судят». Оценщик — подагент
   `critic` в свежем контексте; в его диспатче — оба файла, таблица правды, правила счёта, DoD «строки (а)–(к) заполнены
   для X и Y, у каждой цифры — место в файле исхода».
4. Заполнить таблицу; строка «у фабрики меньше или хуже» — находка в кучку тем же ходом и стоп (правило стопа там же).
5. Время стены и число обращений к человеку — из тетради; цена — `total_cost_usd` логов `free` против суммы
   `driver-runs.jsonl` и дашборда `factory` (P18: источники сходятся, иначе диапазон) — владельцу в чат.
6. Отчёт владельцу под «Утром владельцу» в тетради: докуда дошло каждое плечо, таблица, что решать ей (спорные строки,
   ответы «мои»). Коммит тетради, таблицы и `runs/` (без секретов; проверить `git diff --cached` на слова `SECRET`,
   `PASSWORD`).
7. Узел LR2-1 в `plans/piles/live-runs/batch-2-live-proofs.md` и фразу в `PROJECT.md` (п. 4 находки) закрывает Lead
   владельца, не оператор.

## 7. Где что лежит

| Что | Где |
|---|---|
| Скрипт стенда | `experiments/mybooks/factory-vs-free-agent/stand/stand.ps1` (шапка — все действия) |
| Чистые клоны (только читать) | `C:\QAFactory\mybooks-stand\MyBooks` (`a25b080`), `...\test-automation-framework` (`d33d619`) |
| PostgreSQL 16 (портативный), данные, логи | `C:\QAFactory\mybooks-stand\tools\pgsql`, `...\pgdata`, `...\logs` |
| Тетрадь | `experiments/mybooks/factory-vs-free-agent/notebook.md` |
| Таблица сверки и правда | `experiments/mybooks/factory-vs-free-agent/factory-vs-free-agent.md` |
| Промт `free` | `experiments/mybooks/factory-vs-free-agent/free-agent-prompt.md` |
| Ответы | `experiments/mybooks/factory-vs-free-agent/answers/`; заготовки прошлого опыта — `experiments/mybooks/thinking-roles/answers/` |
| Прошлый опыт на этой стори | `experiments/mybooks/thinking-roles/launch-recipe.md` (рецепт двух плеч 04.11), `.../thinking-roles.md` (тетрадь), `experiments/mybooks/cart-1-run-problems.md` |
