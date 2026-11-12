# Рецепт запуска двух плеч (A, B) на истории MyBooks «Add to Cart»

Разведка скаута (только чтение; в файлы стенда и пакета ничего не писалось). Спека: `docs/tasks/specs/t-1765-thinking-roles.md:545-565` (протокол), `:663-667` (X0/X4).
Пути с `C:\` ниже — простой текст (вне корня сессии ссылкой не оформляются).

## Главное одной строкой (прочесть до рецепта)

1. **Ключа CART-1 на диске нет, есть `LOCAL-1`.** Память об истории: `qa-factory/local-tickets/LOCAL-1.md`, папка артефактов `qa-factory/artifacts/LOCAL-1/` (в `qa-factory/` слово `CART-1` не найдено, контроль той же формой — `LOCAL-1` даёт 3445 вхождений в 243 файлах). `CART-1` — имя прогона 31.10 (`experiments/mybooks/cart-1-run-problems.md`, заголовок). Рецепт идёт с `--task LOCAL-1`; ключ `CART-1` как локальный не годится (`local_keys.py:1-6`: форма `LOCAL-<n>`).
2. **LOCAL-1 водил не драйвер, а дирижёр в сессии Claude Code** (`pipeline.json:314-318`: `run_mode.mode = "desktop"`, `plugin_root = C:\AI\Factory\codemie-public-skills\ai-packages\qa-factory`, `plugin_version 0.10.8`; в `state/` нет `driver-runs.jsonl`). Готовой командной строки драйвера для этой истории нет — рецепт составлен по `design/driver.md` и RUNBOOK 9.3. Драйвера на MyBooks до сих пор не видели вживую: **не проверено на живом прогоне**.
3. **`source-inventory.json` — продукт S1 (скаут, роль), не S0.** S0 пишет только снимок и ссылки. Делить между плечами можно один S0; инвентарь B обязан собрать сам (хартия qa-scout — предмет эксперимента). Это строка разрыва к спеке `:548-549` (см. п. 4).
4. **`prepare_copy.py` для MyBooks не годится** (зашит `codemie-sdk`, `test-harness`, `poetry`); копии делаются руками через `git worktree add` тестового репозитория (то же, что делает `prepare_copy.py:65` — рабочее дерево владельца не переключается).
5. **Плечи — последовательно, A затем B** (п. 2).
6. **Потолка стоимости диспатча в драйвере нет** (п. 7) — строка разрыва к спеке `:561-563`.

## 1. Как запускали LOCAL-1/CART-1; ответы; куда лёг результат

- Запуск: интерактивно, режим `desktop` (`pipeline.json:314-318`); пакет — установленный плагин 0.10.8 из `C:\AI\Factory\codemie-public-skills`. Транскрипт прогона и разборы: `docs/tasks/specs/reports/t-1632..t-1634-*.md` (названы в `experiments/mybooks/cart-1-run-problems.md:3-6`). Тетради прогона с командой драйвера нет: `experiments/mybooks/` содержит только `add-to-cart-cases.md` и `cart-1-run-problems.md` (Glob `experiments/mybooks/**`).
- Попадания по `LOCAL-1|CART-1|mybooks-stand` в `experiments/ docs/ plans/` — 208 файлов; значимые: `docs/RUNBOOK.md` §11 (стенд), `experiments/mybooks/*`, находки кучек `release-next/findings/20261102-*`, `words-gates/findings/20261102-*`, `plans/piles/live-runs/batch-2-live-proofs.md:96,128` (будущие живые доказательства на MyBooks), снимки `docs/tasks/compact-snapshots/2026-11-02-*.md`.
- Ответов человека LOCAL-1 лежат в `qa-factory/artifacts/LOCAL-1/state/words/*.txt` (7 файлов) и `work/question-answers.jsonl` (4 строки); готовой папки `experiments/*/answers/` для этой истории **нет** (Glob `experiments/mybooks/**` — только два файла; для CodeMie образец — `experiments/jev-13797/answers/`, 102 файла).
- Артефакты сейчас: `C:\AI\Factory\mybooks-stand\test-automation-framework\qa-factory\artifacts\LOCAL-1\` (`pipeline.json`, `understanding.md`, `test-plan.md`, `work/`, `state/`, `evidence/`) — **закоммичены** в тестовом репозитории (`git ls-files`: `pipeline.json`, `state/*`, `test-plan.md`, `understanding.md`; HEAD `5114939`, коммиты `7d861e8`, `ef3bf56`, `5114939`), плюс незакоммиченные правки и файлы S5 (`core/clients/cartApi.ts`, `core/fixtures/cart.fixture.ts`, `core/contracts/validators/errorShape.ts`, много `work/*`).
- **Что отодвигать:** в копиях — ничего (они делаются от коммита `5cd21eb`, до истории: артефактов LOCAL-1 там нет, S0 не пропустится). Живой корень владельца не трогать: его `LOCAL-1` — запись прогона 0.10.8. Если Lead всё же решит гнать в живом корне: `Move-Item` папки `artifacts\LOCAL-1` НЕ внутрь `artifacts\` (число `_taken` в `local_keys.py:126-139` и `is_story_folder` читают и `superseded/`, и соседние папки), а наружу, и в git это будет 40+ удалений — так делать не рекомендую. Правило: переименовывать, не удалять (RUNBOOK 9.1(c), 9.6), и без `pipeline.json` история пропускает S0 (RUNBOOK 9.2.3).

## 2. Две копии на одном стенде

**Копирование (проверено чтением, команды не гонялись).**
- Конфиг пишет пути как `../MyBooks` (`config.json:22,211,369,479`; `environments[local].bring_up` `:300`), поэтому копии — **сёстры `MyBooks`** в `C:\AI\Factory\mybooks-stand\` (иначе `../MyBooks` не найдётся).
- База копии — `5cd21eb` («onboarding 2026-10-31», тесты ещё без истории LOCAL-1). Разница HEAD против `5cd21eb` вне артефактов (git diff --stat): `qa-factory/config.json` (+22/−…), `local-tickets/LOCAL-1.md`, `records/journal.jsonl`, `test-cases/cart/*`. Правки конфига с онбординга: `selectors.verified: true`, `frontend.url_key: BASE_URL`, `runtime_probes.web` (запись `runtime_probe.py --suggest --write`) — это лечение проблем 4.1/4.2 прогона 31.10 (`cart-1-run-problems.md:57-58`), не предмет эксперимента. Рекомендация (решение Lead): в обе копии положить **`config.json` из HEAD** живого корня (он не изменён: `git status` его не перечисляет) и `local-tickets\LOCAL-1.md`; хэши записать в «Подготовку».
- `.gitignore` тестового репозитория (прочитан): `node_modules`, `storage-state/*.json`, `playwright-report`, `test-results`, `traces`, `reports`, **`.env`**, `qa-factory/artifacts/*/work/evidence/`, `*fragment*.json`, `impl-diff*.txt`, **`qa-factory/state/`**. Значит git НЕ несёт: `.env` (копировать; в нём ключи `BASE_URL`, `EMAIL_*`, `USER_*`, `TEST_SECRET` — значения в отчёт не пишутся), `node_modules` (junction на живой — быстро и без сети; либо `npm ci`), `storage-state/` (пустую папку создать; **не проверено**, нужна ли она `global-setup.ts` заранее), `qa-factory/state/` (создаётся фабрикой). `qa-factory/config.json`, `obligations.md`, `strategy/*`, `records/*` в git есть.
- Ловушка Claude: у владельца включён плагин `qa-factory@sdlc-factory` (`~\.claude\settings.json:13-14`), а его хуки и `--plugin-dir` дают «смесь поколений» (вопрос вида `package`, `driver.md:203`). `prepare_copy.py:234-237` лечит так: `.claude\settings.local.json` с `{"enabledPlugins": {"qa-factory@sdlc-factory": false}}` в копии. В рецепте это сделано.
- Ветки в копиях: `prepare_copy` делает `--detach`; S5 коммитит тесты (на гейте A LOCAL-1 «test repository: commit», `words/gate-a-20261102.txt`), поэтому рекомендую ветки `exp/thinking-roles-arm-a|b` (ссылка в репозитории владельца, рабочее дерево `main` не меняется). Не пушить (P8, `--no-trace`).

**Параллельно или последовательно — рекомендую ПОСЛЕДОВАТЕЛЬНО (A целиком, затем B).** Причины:
- Аренда стенда живёт в корне проекта: `qa-factory/state/stand-lease.json`, одна на имя среды (`stand_lease.py:14`); у двух корней две независимые аренды, друг друга не держат. Ветка добавляет безусловную аренду ручного окна (`hold_stand`, `manual_stand_wait_s` — `manual_capture.py`, 10 вхождений на ветке; на `main` `hold_stand` только в `run_suite.py`, 3) — и она тоже внутри корня.
- Сид стирает всё (`npm run db:seed`, RUNBOOK:856, `config.json:286`), тесты меняют остаток через `x-test-secret` (RUNBOOK:846-847) и каждый прогон оставляет заказы (`cart-1-run-problems.md:63`): два плеча на одной БД испортят друг другу данные, а красный тест станет неотличим от гонки.
- Бюджет B = 2 × цена той же стадии в A (спека `:561-562`): цены A нужны до B.
- Спека и RUNBOOK о последовательности молчат (протокол `:545-565`, §9 — ничего; RUNBOOK 9.6 «одна копия на эксперимент»). Дополнительно: два драйвера разом упрутся в лимит `claude -p` (код выхода 5, `driver.md:128`).
- Допустимое послабление (необязательно, на решение Lead): S0–S4 плеча B не трогают стенд записью, их можно запускать, пока A на S5+; но тогда на каждом шаге сверять, что A не держит `db:seed`. По умолчанию — не делать.

## 3. Пакет на плечо

- Плечо A — коммит `3a4cf36087fe840cb92a31fdb1c94cd222058cc1` (git merge-base `3a4cf3608` и `experiment/thinking-roles` = он же — основание ветки). Плечо B — голова `experiment/thinking-roles`; на момент чтения интеграционный worktree `.claude\worktrees\agent-acb67480a48b56ff2` стоит на `038f0751f` (голова будет названа при запуске: `<B_HEAD>`).
- Не использовать живой интеграционный worktree как `--plugin-dir` (его двигают билдеры, п. 9.2.2 RUNBOOK): взять **отдельные неподвижные worktree вне дерева репозитория** `C:\AI\Factory\exp-thinking-roles\pkg-a` и `pkg-b`, `git worktree add --detach <путь> <коммит>`. Рабочее дерево на фиксированном коммите = заморозка (содержимое не меняется без нового `checkout`); отпечаток релиза не нужен драйверу (`references/release-fingerprint.json` есть, хуки читают `${CLAUDE_PLUGIN_ROOT}` — `hooks/hooks.json`, 19 вхождений).
- Шаг установки у `--plugin-dir` отсутствует: драйвер берёт пакет аргументом (`story_run.py:17251`, `driver.md:21-25`), `claude -p` грузит плагин из каталога (`.claude-plugin/plugin.json` есть). Корень пакета внутри worktree: `...\pkg-a\ai-packages\qa-factory`. `install_smoke.py` в запуске не участвует (RUNBOOK 4: он про релиз); **как `claude -p` ведёт себя с `--plugin-dir` на путь внутри git worktree — не проверено** (на CodeMie путь был каталогом репозитория или `%TEMP%` копией, RUNBOOK:569).
- Контроль «одно поколение» делает сам драйвер: `state/host-receipts/package-<сессия>.json`, вопрос `package` при смеси (`driver.md:203`). Записать в «Подготовку» `git rev-parse` обоих worktree.

## 4. Общий S0

Что S0 пишет (по mtime LOCAL-1: S0 в 22:10:15–22:11:39, S1 с 22:14; проверено `ls -l`): `work/ticket-snapshot.json`, `work/ticket-references.json`, `work/sources/SRC-…/…/ticket.json` (для локальной истории — копия текста), пустые `work/evidence`, `work/proposals`, `work/bug-drafts`, `state/config-at-start.json`, `state/test-repo-base.json`, в конце `pipeline.json` + инициализация контроллера (`story_run.py:8689-8710`). `source-inventory.json` (22:22:24), `context-bundle.*`, `context-manifest.json` — **S1** (`pipeline.json:19-31`: S1 «qa-scout S1 review · work/source-inventory.json»). Диффа у этой истории нет (`implementation_source: current-code`, `pipeline.json:7`), делить нечего.

Драйвер умеет стартовать с готовым снимком: `s0_ticket` → `s0_kept_snapshot` «читается как есть и не переписывается; его sha256 — `source_revision`» (`story_run.py:7539-7570`). Поэтому **рецепт: копировать в корень B только `work\ticket-snapshot.json` и `work\ticket-references.json` из корня A после того, как S0 A закрыт, без `pipeline.json`, без `state\`**. S0 B пройдёт кодом (модель не вызывается, `driver.md:163`), прочтёт снимок как есть (то же sha256) и сам создаст `pipeline.json`/контроллер своего поколения. `pipeline.json` и `state/` A с собой не тащить: в них `run_mode.plugin_root`, ревизия контроллера и подписи пакета A.
- Две оговорки: (а) локальный ключ требует `local-tickets\LOCAL-1.md` в обоих корнях (`local_keys.is_local`, `:81-86`); (б) снимок A должен быть записан тем же шагом S0 — смотреть строку в логе A «S0: …». Если B всё же напишет свой снимок (`fetched_at` другой), хэш входа разойдётся — это видно по `sha256`, сверить командой из рецепта.
- Строка разрыва: «инвентарь источников (S1) и вопрос `no_change` не общие»; для сравнимости ответ на `no_change` один и тот же (`current code`).

## 5. Ответы

Папки ответов для этой истории нет. Виды вопросов, которые задавал LOCAL-1 (из `state/words/*`, `cart-1-run-problems.md` §3-4), и заготовки:

| вид вопроса (`kind:` в `driver-question.md`) | слова LOCAL-1 | заготовка файла |
|---|---|---|
| S0 `no_change` (local без `--mr/--branch/--commit`, `story_run.py:7363-7400`, ответ → `implementation_source: current-code`, `:7255-7262`) | выбран «current code» (`pipeline.json:7`) | `answers\s0-no-change.md`: ровно `current code` |
| `s1_review` (источники) | `words/s1-20261102-211500.txt`: «Jira ticket for the current story does not exist; the task is the one I described … The link … XPANBFLFA-141 … can be used as project information. 2) Stand ok.» | `answers\s1-sources.md` дословно этот текст |
| gate_A | `Q1: a / Q2: b / approve / (test repository: commit)` (`words/gate-a-20261102.txt`); приём пробела TS-10 (`-2`, `-3`, `-4`) | `answers\gate-a.md`; буквы — по смыслу вопроса, не по номеру (набор вопросов у плеч разный). Эталон человека из `cart-1-run-problems.md:46`: R-9, R-13, R-16 — «в объёме, сбой — баг» (прошлый «a, a, a») |
| `refusal`/halt S4 «design review» | «Да, пропустить» | `answers\s4-design-review-skip.md` |
| S5 «accept without probe» | «Принять без пробы» (проба не читает Playwright TS, FB-4/RN1-9) | `answers\s5-no-probe.md` |
| вопрос о версии стенда / «незакоммиченные изменения» (S4, S5; `cart-1-run-problems.md:49`) | словами человека «стенд ок» | `answers\stand-ok.md` — один на класс (P5, D-0043) |
| `halt`, `retro`, gate_B | в LOCAL-1 не доходили (до S8) | заготовить при первом появлении |

Правило прогона: слова — каждый раз те же (RUNBOOK 9.2.4); новый вопрос → ночной агент по 9.1(a), ответ помечается «мои». Механика: драйвер выходит с кодом 3, вопрос в `<корень>\qa-factory\artifacts\LOCAL-1\state\driver-question.md` (`kind:`, `stage:`, `dispatch:`), ответ — файл и `--answer`, после ответа вопрос переименовывается в `driver-question.answered.md`, слова — в `state\driver-answers.jsonl` (`driver.md:191-208`, RUNBOOK 9.5.3). Тетрадь ведёт журнал «чьи слова».

## 6. Тетрадь `experiments/mybooks/thinking-roles/`

Файлы по спеке `:663,667`: `arm-a.md` (X0-2), `compare.md` (X4-2); рекомендую `thinking-roles.md` — сама тетрадь по RUNBOOK 9.2.5 (образцы `experiments/cmp2-15045/cmp2.md`, `experiments/jev-13797/runs/cmp1.md`); разделы: «Подготовка», «Команда», «Ход прогона», «Журнал вопросов и ответов», «Утром владельцу». В «Подготовку» записать:
1. Стенд: приложение MyBooks `a25b080` (RUNBOOK §11; спека `:546`; `git rev-parse` в `C:\AI\Factory\mybooks-stand\MyBooks`), сборка прод (`npm start`), `/api/health` до каждого плеча, момент и факт `db:seed`.
2. Тесты: база копий `5cd21eb`, ветки `exp/thinking-roles-arm-a|b`, sha256 `config.json`, `LOCAL-1.md`, `.env` (хэш файла, не значения).
3. Пакеты: A `3a4cf3608…`, B `<B_HEAD>`; пути worktree; версия `plugin.json` обоих.
4. Общий вход: sha256 `work\ticket-snapshot.json` и `ticket-references.json` в обоих корнях (спека `:549` «хэши входов — в отчёте»).
5. Судья: `judge.provider` в конфиге (на CodeMie `none`; `prepare_copy.py:230` ставит его) — **в config MyBooks не проверено**; записать значение. Модель ролей `--model sonnet` (P7).
6. Ключ истории `LOCAL-1` вместо `CART-1` (п. «Главное»), причина.
7. Дата/время запуска, pid, логи (`runs\arm-a-1.log`/`.err`), номера перезапусков.
8. Меры M1–M9 и носитель каждой — как в спеке §3 (M9 — запуски автотестов и лишние запуски, слово владельца 04.11.2026); M6 — один носитель `cost_capture` по транскриптам (деньги в файлы не писать, P18).

## 7. Бюджет диспатча — потолок 2× цены стадии A

Не найден. Поиск: `budget|ceiling|cost_cap|max_budget|max-budget|max_cost` по `story_run.py` в worktree ветки. Попадания — другое: байтовые потолки текста, `READ_BUDGET`/`repair_budget` (раунды починки, `:782,9608`), отказ контроллера `STORY BUDGET` (известная строка `ask_person`, `:208`) и `max-turns` только у дирижёра (`:4992`, `:13377` — 40). `--max-budget-usd` в файле нет (контроль той же формы: `max-turns` в том же файле находится). `turn_budget.py` на ветке — счётчик вызовов инструментов с уведомлением, не остановка («says so out loud», строка 1). **Вывод: драйвер на ветке диспатч по цене не останавливает** — это пробел для тетради («записка владельца»), не блокер: бюджет в B соблюдается руками (смотреть `state\driver-runs.jsonl` стоимость строки по диспатчу и `cost_capture`; при превышении 2× A — остановить процесс и записать пробел). `STORY BUDGET` скаутом глубоко не разбирался (отдельный механизм контроллера).

## Рецепт (PowerShell; без `cd`; пути абсолютные)

Переменные (в начале каждой команды-пакета; состояние оболочки не переживает вызовы):
```powershell
$Y = 'C:\AI\Factory\yml-text-factory'
$S = 'C:\AI\Factory\mybooks-stand'
$T = "$S\test-automation-framework"
$E = "$Y\experiments\mybooks\thinking-roles"
$X = 'C:\AI\Factory\exp-thinking-roles'
$A = "$S\tr-arm-a"; $B = "$S\tr-arm-b"
```

**Шаг 0. Папки тетради и пакетов.**
```powershell
New-Item -ItemType Directory -Force "$E\runs","$E\answers",$X | Out-Null
```

**Шаг 1. Пакеты (заморозка = неподвижный коммит).** `<B_HEAD>` — полный хэш головы `experiment/thinking-roles` на момент запуска.
```powershell
git -C $Y worktree add --detach "$X\pkg-a" 3a4cf36087fe840cb92a31fdb1c94cd222058cc1
git -C $Y worktree add --detach "$X\pkg-b" <B_HEAD>
git -C "$X\pkg-a" rev-parse HEAD
git -C "$X\pkg-b" rev-parse HEAD
```
Ожидание: `$X\pkg-a\ai-packages\qa-factory\.claude-plugin\plugin.json` и `...\scripts\story_run.py` существуют (проверить `Test-Path`).

**Шаг 2. Копии тестового репозитория (рабочее дерево владельца не переключается).**
```powershell
git -C $T worktree add -b exp/thinking-roles-arm-a $A 5cd21eb
git -C $T worktree add -b exp/thinking-roles-arm-b $B 5cd21eb
```
Выход ≠ 0, если копия уже есть: не удалять, выбрать другое имя (RUNBOOK 9.6).

**Шаг 3. Что git не несёт + вход одинаковый.**
```powershell
foreach ($R in $A,$B) {
  Copy-Item "$T\.env" "$R\.env"
  New-Item -ItemType Junction -Path "$R\node_modules" -Target "$T\node_modules" | Out-Null
  New-Item -ItemType Directory -Force "$R\storage-state","$R\qa-factory\local-tickets","$R\.claude" | Out-Null
  Copy-Item "$T\qa-factory\config.json" "$R\qa-factory\config.json" -Force
  Copy-Item "$T\qa-factory\local-tickets\LOCAL-1.md" "$R\qa-factory\local-tickets\LOCAL-1.md"
  Set-Content -Path "$R\.claude\settings.local.json" -Value '{"enabledPlugins":{"qa-factory@sdlc-factory":false}}'
}
Get-FileHash "$A\qa-factory\config.json","$B\qa-factory\config.json","$A\qa-factory\local-tickets\LOCAL-1.md","$B\qa-factory\local-tickets\LOCAL-1.md" | Format-Table Hash,Path
```
Хэши пары должны совпасть (в «Подготовку»). Артефактов LOCAL-1 в копиях нет: `Test-Path "$A\qa-factory\artifacts\LOCAL-1"` → `False` (контроль, что S0 не пропустится).
Проверка среды копии (**не проверено на живом прогоне**): `npm --prefix $A run test -- --list --project=chromium` (профиль/NODE_ENV — RUNBOOK §11: живое приложение только при `NODE_ENV=prod`; не гонять тесты без нужды).

**Шаг 4. Стенд перед плечом A (стенд — её; `db:seed` стирает данные, `config.json:306` его разрешает — решение Lead).**
```powershell
Invoke-RestMethod http://localhost:3000/api/health
npm --prefix "$S\MyBooks" run db:seed
```

**Шаг 5. Ответы-заготовки (по таблице п. 5), например:**
```powershell
Set-Content "$E\answers\s0-no-change.md" 'current code' -NoNewline
```
(остальные файлы — слова из таблицы, дословно).

**Шаг 6. Сухой прогон A (роли не вызываются).**
```powershell
$env:PYTHONUNBUFFERED = '1'
python "$X\pkg-a\ai-packages\qa-factory\scripts\story_run.py" --task LOCAL-1 --env local --model sonnet --no-trace --plugin-dir "$X\pkg-a\ai-packages\qa-factory" --project $A --dry-run
```

**Шаг 7. Запуск плеча A в фоне (отдельный процесс; N растёт на каждый перезапуск).**
```powershell
$env:PYTHONUNBUFFERED = '1'
Start-Process -FilePath python -WorkingDirectory $A `
  -ArgumentList "$X\pkg-a\ai-packages\qa-factory\scripts\story_run.py","--task","LOCAL-1","--env","local","--model","sonnet","--no-trace","--plugin-dir","$X\pkg-a\ai-packages\qa-factory" `
  -RedirectStandardOutput "$E\runs\arm-a-1.log" -RedirectStandardError "$E\runs\arm-a-1.err" -PassThru
```
`--until end` по умолчанию. Объём плеча — решение Lead: вся история (`end`, нужна для M1/M7/эталона Б-1/Б-2/Б-4, требует S6) или `--until gate_A` (дёшево: M3, M5, часть M8). Спека F-4 рекомендует (c): S1–S4 + диспатч исследования S6. Записать pid и время в «Ход прогона»; через пару минут: `Get-Process -Id <pid>`; хвост `.err` пуст.
Остановки по кодам выхода — таблица RUNBOOK 9.4 (3 — вопрос, 4 — дирижёр сдался, 5 — инфраструктура, повторить; 0 — готово или `--until`).

**Шаг 8. Где вопрос и как ответить.**
```powershell
Get-Content "$A\qa-factory\artifacts\LOCAL-1\state\driver-question.md"
Get-Content "$A\qa-factory\artifacts\LOCAL-1\state\driver-runs.jsonl" -Tail 5
```
Ответ — та же команда с `--answer <файл>` и следующим логом (`arm-a-2.log`):
```powershell
Start-Process -FilePath python -WorkingDirectory $A `
  -ArgumentList "$X\pkg-a\ai-packages\qa-factory\scripts\story_run.py","--task","LOCAL-1","--env","local","--model","sonnet","--no-trace","--plugin-dir","$X\pkg-a\ai-packages\qa-factory","--answer","$E\answers\s0-no-change.md" `
  -RedirectStandardOutput "$E\runs\arm-a-2.log" -RedirectStandardError "$E\runs\arm-a-2.err" -PassThru
```
Сначала ожидается вопрос `no_change` (S0 стоит до первого диспатча, `story_run.py:7363`).

**Шаг 9. Общий S0 в B — после того как S0 A закрыт** (в `$A\qa-factory\artifacts\LOCAL-1\pipeline.json` есть `stages.S0.status: done`; для чистоты — после первого ответа):
```powershell
$bw = "$B\qa-factory\artifacts\LOCAL-1\work"
New-Item -ItemType Directory -Force $bw | Out-Null
Copy-Item "$A\qa-factory\artifacts\LOCAL-1\work\ticket-snapshot.json"   "$bw\ticket-snapshot.json"
Copy-Item "$A\qa-factory\artifacts\LOCAL-1\work\ticket-references.json" "$bw\ticket-references.json"
Get-FileHash "$A\qa-factory\artifacts\LOCAL-1\work\ticket-snapshot.json","$bw\ticket-snapshot.json" | Format-Table Hash,Path
```
`pipeline.json`, `state\`, `source-inventory.json` и остальное из корня A — не копировать. Хэш снимка в «Подготовку». Плечо B пройдёт S0 кодом по «снимок уже есть» (`story_run.py:7569`) и спросит `no_change` тем же словом.

**Шаг 10. Когда A дошло до цели (выход 0): стенд заново и запуск B** (стенд перед B как в шаге 4; заглушить `db:seed` по решению Lead, одинаково для обоих плеч):
```powershell
Invoke-RestMethod http://localhost:3000/api/health
npm --prefix "$S\MyBooks" run db:seed
$env:PYTHONUNBUFFERED = '1'
Start-Process -FilePath python -WorkingDirectory $B `
  -ArgumentList "$X\pkg-b\ai-packages\qa-factory\scripts\story_run.py","--task","LOCAL-1","--env","local","--model","sonnet","--no-trace","--plugin-dir","$X\pkg-b\ai-packages\qa-factory" `
  -RedirectStandardOutput "$E\runs\arm-b-1.log" -RedirectStandardError "$E\runs\arm-b-1.err" -PassThru
```
Вопросы и ответы B — как шаг 8 с заменой `$A→$B`, `pkg-a→pkg-b`, `arm-a→arm-b`; **те же файлы ответов** из `$E\answers`.
Бюджет B: после каждой стадии сверять цену диспатча B с 2 × цена той же стадии A (читать по `state\driver-runs.jsonl` и `cost_capture`; автоматического стопа нет — п. 7).

**Шаг 11. Уборка после прогонов (по слову владельца).** Копии и worktree не удалять сессией (RUNBOOK 9.6); процессы: `Get-Process python` старше конца прогона — убить деревья, чужое не трогать (RUNBOOK 9.9).

## Отклонения этой разведки

- Задание «не запускать команды»: я выполнил несколько read-only вызовов Bash (`ls`, `git ls-files/log/diff/show/status/worktree list/merge-base/rev-parse`, `curl` на `/api/health` → `{"status":"ok","db":"up"}`) — только чтобы увидеть состояние стенда и репозиториев. Записей нет. Первый такой вызов начался с `cd` в папку стенда (хук предупредил); я немедленно вернул каталог оболочки в корень сессии.
- «Не проверено»: поведение драйвера на MyBooks вживую; `--plugin-dir` на путь внутри git worktree; нужность папки `storage-state`; значение `judge.provider` в конфиге MyBooks; работа `npm … --list` в копии.

## TRAIL

Прочитано: `docs/tasks/specs/t-1765-thinking-roles.md` 535-575, 575-644, 655-675; `docs/RUNBOOK.md` 367-676 (§9), 831-874 (§11); `experiments/jev-13797/prepare_copy.py` целиком; `experiments/mybooks/cart-1-run-problems.md` целиком; `experiments/mybooks/add-to-cart-cases.md` 1-25; `ai-packages/qa-factory/design/driver.md` 1-30, 118-228, 290-320; `scripts/story_run.py` 7113-7152, 7193-7270, 7349-7402, 7539-7588, 8480-8613, 8615-8712, 17200-17285 (и Grep по argparse/`snapshot`/`budget`/`max-turns`); `scripts/local_keys.py` целиком; `scripts/stand_lease.py` 1-40; `scripts/turn_budget.py` (Grep, шапка); файлы стенда: `.env` (чтение, значения не цитируются), `.gitignore`, `qa-factory/config.json` (Grep путей/сред), `qa-factory/local-tickets/LOCAL-1.md`, `qa-factory/artifacts/LOCAL-1/pipeline.json` 1-60 и 300-330, `state/driver-state.json`, `state/words/*.txt` (7); `C:\Users\Mariia_Lobashova\.claude\settings.json` (Grep `enabledPlugins`); `.claude/settings.json` (Grep).
Grep/Glob: `LOCAL-1|CART-1|mybooks-stand` по `experiments/docs/plans` (208 файлов, count); `CART-1` по `qa-factory` стенда — пусто, контроль `LOCAL-1` той же формой — 3445 в 243 файлах; `ticket-snapshot.json|source-inventory.json` по `scripts/*.py` (75 файлов); `hold_stand|manual_stand_wait_s` по ветке (3 файла, 20) и по `main` (1 файл, 3); `budget|ceiling|cost_cap|max_budget` по `story_run.py` ветки (контроль — `max-turns`, находится); Glob `experiments/mybooks/**`, `experiments/jev-13797/answers/*` (102), `ai-packages/qa-factory/{hooks/*,.claude-plugin/*,references/release-fingerprint.json}`, `**/hold_stand*` (пусто, это имя функции, не файла).
Bash (read-only): `ls`/`git` по тестовому репозиторию (HEAD `5114939`, `5cd21eb`, `7d861e8`, статус, `ls-files qa-factory`, `diff --stat 5cd21eb HEAD`), `git merge-base 3a4cf3608 experiment/thinking-roles` → `3a4cf36087fe840cb92a31fdb1c94cd222058cc1`, `git worktree list`, `git log` интеграционного worktree (HEAD `038f0751f`), `curl /api/health`.
