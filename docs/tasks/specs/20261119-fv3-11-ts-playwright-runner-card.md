# FV3-11 (П1-б N6) — вторая строка раннеров TS/Playwright: карточка билдера (черновик дизайнера, t-1563)

Статус: ЧЕРНОВИК. Решения — Lead. Развилки §5 не закрыты; заголовок §3 написан под рекомендованные варианты (F1 (а), F2 (а),
F3 (а), F4 (а)) и правится Lead при другом выборе.

---

## 0. Главное за 5 строк

1. Сухая история берёт раннер ПО ИСТОРИИ: одна строка `kit.json` `runner` (сегодня `python-pytest`); вторую строку не
   выбирает ни прогон, ни обход. Своими owns N6 до `exits:s5` с TS-строкой не дотягивается (§1, F1).
2. Добавление папки `runners/ts-playwright/` сразу краснит самопроверку `dry_stub.py --selftest` (пин списка строк
   `dry_stub.py:1394`) — owns надо расширить на `dry_stub.py::selftest_n2` (F2).
3. Продукт не умеет TS-маркер (FV1-19 «в работе»; `test_file:typescript` — известный красный `form-rounds.json:52`):
   обход S5 на TS-строке сегодня встанет на первом выходе автоматора — это ожидаемый улов (§9.3 П1-б), не успех.
4. Рекомендация: N6a (эта карточка) = строка + образ (Node, Playwright, Chromium) + проверка «каждая строка раннеров
   запускается своей командой профиля»; N6b (новый узел) = выбор строки на прогон и `exits:s5` на TS-строке.

---

## 1. Замер состояния (чтение, файл:строка)

### 1.1 Что сухая история делает со второй строкой раннеров сегодня

| Вопрос | Ответ | Носитель |
|---|---|---|
| Кто выбирает строку | история: ключ `runner` её `kit.json` | `T/fixtures/stories/dry-1/kit.json:14` `"runner": "python-pytest"`; проверка формы `T/dry_stub.py:324-325` (`load_kit`) |
| Где выбор применяется | при постройке мира: `install_runner(root, runner_row(kit["runner"], story_id))` | `T/dry_world.py:326` (`build_story_world`; её зовут `:1048`, `:1480`) |
| Где ещё | ветки ролей S5: `critic_branch(..., runner_row(kit["runner"]), ...)`, `automator_branch(...)` | `T/dry_stub.py:1030`, `:1045` |
| Выбор на прогон | НЕТ: `test_scenario_dry_1.py` знает только `--part`, `--exits-root`, `--ledger` | `T/test_scenario_dry_1.py:127-130` |
| Обход всех строк | НЕТ: матрица `dry-story.yml` — по файлам `exits/*.json`, о раннерах не знает | `.github/workflows/dry-story.yml:33-50`, `:57-60`; факт Lead: `grep -c runners` = 0 |
| Кто читает ВСЕ строки | `runner_rows()` — читает и ПРОВЕРЯЕТ каждую папку `runners/<row>/` при каждом `runner_row(...)`; неверная строка = `KitError` для любой истории, в том числе на дороге `python-pytest` | `T/dry_stub.py:361-376`, `:379-384` |
| Пин числа строк | самопроверка: `[r["id"] for r in runner_rows()] == ["python-pytest"]` и `kit["runner"] == "python-pytest"` | `T/dry_stub.py:1392-1394` (функция `selftest_n2`, `:1378`); запускается задачей `tables` `dry-story.yml:106-110` |

Вывод: вторая строка сегодня = данные, которые проверяются по форме при каждой постройке мира, но НЕ обходятся ни одним
прогоном. Ответ на вопрос брифа: «выбирается per story» (не per run, не обход каждой строки).

### 1.2 Что заставит TS-строку споткнуться, если её обойти (для F1, N6b)

| Место | Состояние | Носитель |
|---|---|---|
| Тест-файл автоматора | `fill_output(f"test_file:{runner['lang']}", ...)`: язык — ключ `lang` строки | `T/dry_stub.py:613` |
| Шаблон `test_file:<lang>` | есть только `python` и `pytest` (`like`) | `T/fixtures/form-fill-rules.json:238-255` |
| Маркер случая | только pytest: `decorator_prefix "@pytest.mark."`, ключ `pytest` | `PKG/references/case-markers.json:4-8` (Grep `-i typescript\|playwright` — 0; контроль `pytest` в том же файле — 3 строки) |
| Известный красный | `"unfillable output test_file:typescript:marker «typescript»"` → узел FV1-19 | `T/fixtures/form-rounds.json:52` |
| FV1-19 | «в работе»: `manifest_from_tests.py` читает маркер только из Python | `plans/piles/live-run-fvf/batch-1-live-run-fvf.md:58` |
| Строки обхода `s5` | заточены под pytest: 54 вхождения `pytest\|_test\.py\|\.py::` (`TC-1_test.py:6` и т. п.) | Grep count по `T/fixtures/stories/dry-1/` (`exits/s5.json` 54, `story.json` 5) |
| Уговор П1-б | улов FV1-19 дефект 2 — «на обеих строках» | `docs/tasks/specs/20261113-p1b-dry-story-spec.md:661`, `:939` |

### 1.3 CI сегодня

- `dry-story.yml`: задачи `list` (`:23-50`), `parts` (матрица групп, `setup-python` + `pip install -q pytest`, `:52-76`),
  `tables` (маркер `id: setup` `:90`, четыре проверки под `!cancelled() && steps.setup.conclusion == 'success'`, `:96-115`).
  Ни Node, ни Playwright (факт Lead: одно вхождение — комментарий `:1`; Grep `-i setup-node|playwright` по `.github/` — 0,
  контроль той же формы `dry-story\.yml` — 4 строки в `canon.yml`, `nightly.yml`).
- Вызывают файл: `canon.yml:82` (дверь `dry_only`), `nightly.yml:77`.
- Пины `tools/test_workflows.py`: `NAMES :29`; `hidden_checks :217-248` — до маркера допускает ТОЛЬКО `actions/checkout`,
  `actions/setup-python`, `pip install`, `git config` (`:235-236`); параметр `("dry-story.yml", "tables", "setup")` `:253`;
  `:180-186` (нет `cache: pip`); `:421-430` (матрица из `list`); `:433-440` (pytest до первого python-шага в `parts`,
  `tables`); `:443-447` (F19E: `F19E_FORBIDDEN :381` + запрет `${{ matrix.` в `run:`).
- Следствие (позиционный край): Node/npm/Playwright-шаг, поставленный в `tables` до маркера, краснит пин `:253`; после
  маркера — это «проверка», а не установка.

### 1.4 Зависимости строки пачки

FV3-4 (N5) — `принято: 905e9735 (t-1021)`, FV3-7 (N4:s5) — `принято: 9418c560… (t-1223)`
(`plans/piles/live-run-fvf/batch-3-live-run-fvf.md:34`, `:37`). FV3-11 — «ожидает» (`:41`).

---

## 2. §1 спеки: инварианты, проверки, разнообразие

**AR-n, которые трогает изменение** (`PKG/design/architecture.md`):
- AR-1 (закрытое разнообразие — строка данных): язык — строка `runners/<row>/runner.json`, читается по ключу `lang`; ни
  один шаг CI и ни одна строка кода не ветвится на `id` или `lang` строки. Проверка изменения: в `run:` новой задачи нет
  литерала `ts-playwright`/`python-pytest`/`typescript` в цикле проверки (пин теста, §3 `test:` 2).
- AR-22 (у каждого поля — читатель): ключи новой строки — те же, что у первой (`id`, `lang`, `profile_id`, `command`,
  `profile`, `runtime_probe`), их читатели — `runner_rows` (`dry_stub.py:372-374`), `install_runner` (`:391-401`),
  `world_command` (`:486-497`). Новых ключей нет. Проверка изменения: diff `runner.json` против первой строки — только
  значения.
- AR-28 (неизвестное не становится пропуском): необойдённая TS-строка не считается доказанной; строку оси 3 карты
  разнообразия («Proven on») эта карточка НЕ правит — зелёный прогон проверки образа доказывает образ, не фабрику.
- AR-29: добавляемые проверки — (1) задача CI «каждая строка раннеров запускается командой своего профиля», (2) пин этой
  задачи в `tools/test_workflows.py`, (3) пин списка строк в `selftest_n2`. Владелец всех трёх — данные (код): форма,
  присутствие, код выхода; суждения роли не судят. Класс переписи: ни одного места отказа пакета (`refusal_registry.sites()`)
  не добавляется — проверки dev/CI. Строка коммита `judgment:` — в форме гейта, носитель формы — `tools/architecture_gate.py`
  (пункт 6 докстринга); по смыслу — `none` с причиной «fixture data and a CI job; no judgment moves» (форму печатать по
  гейту, не отсюда).

**Обход разнообразия** (`architecture.md` § A, `:66-72`):
- `axis 1: held by table -- stories/dry-1/runners/<row>/runner.json key lang (F5); unknown value -> test_file:<lang> Unfillable, a live_only row (form_filler._key_of; known_red form-rounds.json:52), never a pass`
- `axis 3: held by table -- the same row (profile.commands, command); unknown value -> no command in the profile: world_command says so, nothing is run (dry_stub.py:495-496)`
- `axes 2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13: n/a -- a test fixture row of the dry story and a CI image; no surface, starting state, tracker, delivery, stand, host, process, text language, size, check kind or project age changes`
- `narrows`: нет. Срез «TS-строка не обходится в `exits:s5`» — не исключение языка только при условии, что остаток — названный
  узел N6b с owns и тестом (designer.md правило 6; развилка F1).

---

## 3. Карточка билдера (заголовок R11-f; под F1 (а), F2 (а), F3 (а), F4 (а))

given: C:/QAFactory/forge-repo/docs/tasks/specs/20261119-fv3-11-ts-playwright-runner-card.md (§1 замер, §4 края); C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/fixtures/stories/dry-1/runners/python-pytest/ (runner.json, project/); `ai-packages/qa-factory/scripts/tests/dry_stub.py::runner_rows`, `::install_runner`, `::world_command`, `::selftest_n2`; `ai-packages/qa-factory/scripts/profile_contract.py::profile_command`, `::command_argv`; C:/QAFactory/forge-repo/.github/workflows/dry-story.yml; `tools/test_workflows.py::hidden_checks`, `::test_every_check_step_runs_after_a_red_neighbour`, `::test_dry_story_matrix_comes_from_the_list_job_and_an_empty_list_says_so`
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\stories\dry-1\runners\ts-playwright\ (новая папка: runner.json, project/package.json, project/package-lock.json, project/playwright.config.ts, project/tests/cart.spec.ts)
C:\QAFactory\forge-repo\.github\workflows\dry-story.yml (новая задача `runners` и строки шапки-комментария о ней; задачи `list`, `parts`, `tables` — байт в байт)
C:\QAFactory\forge-repo\tools\test_workflows.py (`hidden_checks` — виды установки; строка параметра `dry-story.yml`/`runners`; одна новая функция пина задачи `runners`)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\dry_stub.py (только функция `selftest_n2`, строки `:1392-1394`; развилка F2)
C:\QAFactory\forge-repo\docs\tasks\specs\reports\20261119-fv3-11-report.md (новый)
non-goals: выбор строки на прогон и обход `exits:s5` с TS-строкой (N6b, развилка F1); правка строки `python-pytest` и `kit.json` (`runner` остаётся `python-pytest`); маркер случая TS, `form-fill-rules.json`, `case-markers.json`, `manifest_from_tests.py` (FV1-19); новый тип истории (FV3-12); правка строки оси карты разнообразия; кэш npm/браузера; живой прогон
handoff: отчёт билдера C:\QAFactory\forge-repo\docs\tasks\specs\reports\20261119-fv3-11-report.md (вывод DoD, id прогона CI двери `dry_only`, замер времени задачи `runners` по шагам)
edges: §4 этой карточки, строки E1-E12 (каждая с инвариантом); главные — E2 (установка красная → задача красная, никогда «пропущено»), E6 (ВРЕМЕННОЙ: дорога `python-pytest` зелёная, идёт задача `runners` или нет), E1 (неверный `runner.json` второй строки ломает и первую дорогу)
DoD: `python -m pytest tools/test_workflows.py -q` зелёный; `python -B ai-packages/qa-factory/scripts/tests/dry_stub.py --selftest` зелёный (если дольше 5 мин — строка отчёта «not run locally: dry_stub.py --selftest, canon judges» и свидетель — задача `tables`); `python -B ai-packages/qa-factory/scripts/selftest.py --lang` без кириллицы в новых файлах; CI: `python -B tools/ci_read.py start --ref <ветка> --var dry_only=true`, затем `python -B tools/ci_read.py jobs <run>` — задачи `list`, `parts` (все группы, включая `s5`) и `tables` зелёные как до правки, задача `runners` зелёная и печатает строку на каждую строку раннеров (`python-pytest`, `ts-playwright`); в отчёте — `git status --short` без `node_modules/`
test: tools/test_workflows.py::test_every_check_step_runs_after_a_red_neighbour (строка параметра ("dry-story.yml", "runners", "setup")) + отрицательные строки `hidden_checks`: `npx playwright test` и `npm test` до маркера — отказ | expected from: край брифа «install fails -> fail loudly, never silently skip»; FG7-90 (`hidden_checks` докстринг :218-221)
test: tools/test_workflows.py (новая функция рядом с :421, пин задачи `runners`: `needs: list`, нет `if:` на задаче, ни `parts`, ни `tables` не `needs: runners`; цикл проверки читает `dry_stub.runner_rows()`; в `run:` цикла нет литерала id/lang строки) | expected from: П1-б F5 (а) `20261113-p1b-dry-story-spec.md:771-772` (одна дорога, P31); край E6 этой карточки
test: ai-packages/qa-factory/scripts/tests/dry_stub.py::selftest_n2 (строка `:1392-1394`: ids = ["python-pytest", "ts-playwright"], `kit["runner"]` = "python-pytest") | expected from: F5 (а); край E6 (история по-прежнему ходит первой строкой)
siblings: ось 34 SIBLING_MAP (языки — строки таблицы раннеров, одна дорога); ось 30 (`profile_contract.profile_commands`/`command_argv` — один читатель команд, им же пользуется проверка); FG7-90 (`hidden_checks` — проверки после красного соседа)
readers: §6 этой карточки (блок `tools/owns_readers.py` к брифу не приложен — Lead прикладывает до диспатча)
designer: C:\QAFactory\forge-repo\docs\tasks\specs\20261119-fv3-11-ts-playwright-runner-card.md

### 3.1 Что сделать (пункты)

1. **Строка `ts-playwright`** (английский текст, ни одного символа кириллицы):
   - `runner.json`: те же ключи, что у `python-pytest/runner.json:1-13`. `id` = `ts-playwright`; `lang` = `typescript`
     (ровно это слово: так назван язык в `form-rounds.json:52`, край E10); `profile_id` = `dry-playwright`; `command` =
     `one_test`; `profile.commands.one_test` = `{"argv": ["npx", "playwright", "test", "--reporter=line"], "cwd": "."}`;
     `runtime_probe` — та же форма, что у первой строки, с `--profile dry-playwright` (развилка F8; при (б) — ключа нет).
   - `project/package.json`: `private: true`, одна devDependency `@playwright/test` с ТОЧНОЙ версией (без `^`/`~`),
     которую печатает `npm view @playwright/test version` в день сборки; `project/package-lock.json` — из
     `npm install --package-lock-only` (без `node_modules/` в дереве; край E8).
   - `project/playwright.config.ts`: `testDir: "tests"`, один проект `chromium`, `retries: 0`, `workers: 1`,
     `reporter: "line"`, без `webServer`, без сети.
   - `project/tests/cart.spec.ts`: один тест того же предмета, что `python-pytest/project/test_cart.py:4-9` (итог корзины
     с количеством = 13), который ОТКРЫВАЕТ страницу (`page.setContent` с итогом, `expect(locator).toHaveText("13")`) —
     браузер доказывается использованием (F4 (а), край E3). Маркера случая нет (FV1-19).
2. **Задача `runners` в `dry-story.yml`** (после `tables`; `needs: list`, без `if:`, `timeout-minutes: 15  # until the
   Lead's cap`): до маркера — `actions/checkout@v7` (`ref: ${{ inputs.ref || 'main' }}`), `actions/setup-python@v7`
   (3.12), `pip install -q pytest`, `actions/setup-node@v4` (`node-version: "22"`, без `cache:`), `npm ci` в папке
   проекта TS-строки, `npx playwright install --with-deps chromium` там же, `git config` (как в `tables`), `id: setup`.
   После маркера — ОДИН шаг проверки под `${{ !cancelled() && steps.setup.conclusion == 'success' }}`: инлайн-python
   (≤ 15 строк), который берёт `dry_stub.runner_rows()`, для КАЖДОЙ строки копирует `<row>/project` во временную папку
   (как `install_runner`, `shutil.copytree`), берёт слова команды через `profile_contract.profile_command` +
   `command_argv` (ось 30, один читатель), запускает их с `cwd` строки, печатает `runner <id>: exit <n>` и завершается
   ненулём, если хоть одна строка не 0 или строк нет. Значения входов — только через `env:` (F19E).
   Шапка-комментарий файла (`:1-8`) получает одну строку о задаче `runners`.
3. **`tools/test_workflows.py`**: (а) `hidden_checks` до маркера допускает ещё ровно три вида установки: `uses:
   actions/setup-node`, `run:` целиком `npm ci ...` и целиком `npx playwright install ...` (полное совпадение формы, не
   `startswith`; край E12); (б) строка параметра `("dry-story.yml", "runners", "setup")`; (в) новая функция пина задачи
   (`test:` 2); (г) отрицательные строки контроля `hidden_checks` (`test:` 1).
4. **`dry_stub.py::selftest_n2`**: ожидание `:1394` — `["python-pytest", "ts-playwright"]`, `kit["runner"]` без изменений;
   текст метки `:1392` — «names the first runner row of two». Больше в файле ничего.
5. Коммит: строки AR-n и `judgment:` — в форме `tools/architecture_gate.py` (не копировать грамматику отсюда); указатель на
   §2 этой карточки.

---

## 4. Края (каждый с инвариантом)

| # | Край | Поведение | Инвариант |
|---|---|---|---|
| E1 | `runner.json` TS-строки неверной формы (нет `lang`, `profile_id` не совпал) | `runner_rows()` (`dry_stub.py:372-374`) бросает `KitError` при КАЖДОЙ постройке мира — краснеет и дорога `python-pytest`; ловит до слияния `selftest_n2` (задача `tables`) и шаг задачи `runners` | неверная строка никогда не «пропускается»: ни одна история не строится молча без неё |
| E2 | `setup-node`, `npm ci` или `npx playwright install` упали в CI | шаг красный → шаг проверки не стартует (условие маркера) → задача `runners` красная → вызов `dry-story.yml` красный в двери `dry_only` и ночью | красная установка никогда не читается как зелёная или «TS-строка пропущена»: нет `continue-on-error`, `\|\| true`, `if:` до маркера (пин `hidden_checks`) |
| E3 | установка браузера вышла 0, а браузера нет (частичная загрузка) | тест `cart.spec.ts` открывает страницу → красный с текстом Playwright | присутствие браузера доказывает его использование, а не код выхода установщика |
| E4 | `runners/` пуст или исчез | `runner_rows()` → `KitError` → шаг проверки ненулевой | «ноль строк» никогда не зелёный |
| E5 | у строки нет команды `one_test` / `argv` строкой | `command_argv` возвращает проблему → шаг печатает `runner <id>: <проблема>` и ненулевой | ни одна строка не выпадает из проверки молча |
| E6 | ВРЕМЕННОЙ. До: одна строка, пин `["python-pytest"]`, задачи `runners` нет. После (этот коммит создаёт и папку, и задачу, и пин): две строки, `kit.runner` = `python-pytest` | `list`, `parts` (все группы), `tables` — байт в байт, ни одна не `needs: runners`; их результат не зависит от того, запустилась ли `runners` | дорога `python-pytest` зелёная, идёт TS-задача или нет; правка пина — тем же коммитом, что папка (иначе `tables` красная между коммитами) |
| E7 | бюджет времени задачи `runners` | ОЦЕНКА, не замерено: `setup-node` 5-15 с, `npm ci` 10-30 с, `playwright install --with-deps chromium` 60-120 с (apt-зависимости), два прогона строк 10-20 с; итого 2-3 мин; кэша нет. Кап 15 мин до решения Lead. Ночь платит те же 2-3 мин (F7). Билдер пишет в отчёт замер по шагам из `ci_read.py jobs` | кап — не догадка навсегда: замер в отчёте, кап меняет Lead |
| E8 | `node_modules/`, `test-results/` | `npm ci` — только в CI (выкидной checkout); локально — `npm install --package-lock-only` (без `node_modules`). Нет Node локально → билдер пишет это в отчёт, лок-файл не выдумывается рукой; Lead решает (лок на CI-ветке отдельным шагом) | в дерево не попадает ни `node_modules/`, ни отчёт Playwright; `npm ci` без лок-файла отказывает громко, а не ставит «что-то» |
| E9 | язык файлов пакета | все новые файлы под `PKG/` — английские | `selftest.py --lang` чистый (FR-30) |
| E10 | значение `lang` | ровно `typescript` | когда N6b обойдёт строку, отказ автоматора попадёт на существующую метку FV1-19 (`form-rounds.json:52`), а не на новую безымянную |
| E11 | (для N6b, здесь не достижимо) обход S5 TS-строкой | автоматор: `test_file:typescript` → `Unfillable` → строка `live_only`, метка FV1-19 | AR-28: неумение продукта никогда не пропуск; TS-строка не «доказана» до зелёного обхода |
| E12 | расширение `hidden_checks` (существующая функция в роли гейта шире) | ошибается в сторону «допустить»: новые виды — только полным совпадением; `npx playwright test`, `npm test`, `npm ci && npx playwright test`, `npx playwright install; pytest` до маркера — отказ (строки контроля) | проверка до маркера не может спрятаться под видом установки; существующие строки `forge-check`/`package-fast`/`tables` зелёные без изменений |

Пары требований, которые могут спорить: «owns только N6» против «пин `selftest_n2` краснеет» — F2; «свидетель —
`exits:s5`» против «строка выбирается историей» — F1/F5; «браузер в образе» против «тест без браузера» — F4.

---

## 5. Развилки для Lead (каждая с рекомендацией; не решены)

**F1. Как TS-строка доходит до `exits:s5`.** Замер §1.1-1.2: строку выбирает история, строки `s5` под pytest, TS-маркер —
FV1-19 «в работе». (а) Разрезать: N6a = эта карточка (строка + образ + проверка всех строк); N6b — новый узел пачки:
выбор строки на прогон (`--runner <row>` в `test_scenario_dry_1.py::main`/`exits_part`, параметр `build_story_world`
вместо одного `kit["runner"]`, матрица `dry-story.yml` — группа × строка из `list`), строки/метки `s5` по строке раннера
(улов FV1-19 «на обеих строках»), откуда мир берёт `node_modules`; owns N6b — `T/test_scenario_dry_1.py`, `T/dry_world.py`
(`build_story_world`, `walk_exits`), `dry-story.yml` (`list`, `parts`), `T/fixtures/stories/dry-1/exits/s5.json`,
`T/fixtures/driver-exits/known_red/s5.json`, `tools/test_workflows.py`; после FV1-19 или с её метками. (б) Всё одной
карточкой сейчас — выходит за owns N6 втрое, пересекает FV3-13 (`test_scenario_dry_1.py`) и FV3-12. (в) TS-строка
отдельной историей `dry-1-ts` — это новый тип истории, non-goal (FV3-12). **Рекомендация: (а)**; цена — `exits:s5` с
TS-строкой откладывается на узел N6b, который Lead вносит в пачку строкой с owns и тестом (иначе остаток — исключение
языка, правило 6).

**F2. Расширение owns на `dry_stub.py::selftest_n2`.** Любая новая папка под `runners/` краснит пин `:1394` в задаче
`tables`. (а) Расширить owns на эту функцию (правило 2: дефект в досягаемости узла чинит карточка) — **рекомендация**;
(б) оставить N6 owns как есть — `tables` красная после слияния, инвариант «`main` не краснеет» (finish-spec §5 `:512`)
нарушен. Альтернативы без правки `dry_stub.py` нет.

**F3. Куда ставить Node и браузер.** (а) Новая задача `runners` в `dry-story.yml`: установка + проверка «каждая строка
запускается командой профиля» — **рекомендация**: ставится один раз, у образа есть потребитель, обе строки идут одной
дорогой; выходит за «только шаги образа» (finish-spec `:475`) на одну задачу — это и есть решение Lead. (б) Шаги в
`parts`: каждая из 4 групп платит 2-3 мин (оценка), потребителя до N6b нет, плюс риск красного `parts` из-за установки,
не нужной группе. (в) В `tables`: требует того же расширения `hidden_checks`, смешивает установку с четырьмя проверками
таблиц. Для N6b образ всё равно понадобится в `parts` — тогда шаги переносятся туда тем узлом.

**F4. Открывает ли TS-тест браузер.** (а) Да (`page.setContent`, без сети) — **рекомендация**: иначе сломанная установка
браузера невидима (край E3). (б) Нет (чистая функция): браузер не нужен вовсе, установку можно не ставить — но тогда
«браузер в образе» из N6 не выполнен.

**F5. Свидетель.** Finish-spec `:476` называет свидетелем «часть `exits:s5` через дверь `dry_only`». При F1 (а) это
недостижимо в N6a. (а) Свидетель N6a — прогон двери `dry_only`: `runners` зелёная с двумя строками, `parts` (вкл. `s5`)
и `tables` зелёные как до правки; `exits:s5` с TS-строкой — свидетель N6b — **рекомендация**. (б) Оставить свидетель как
в спеке — тогда только F1 (б).

**F6. Старая слабость `hidden_checks`.** До маркера сейчас допускается любой `run:`, начинающийся с `pip install`/`git
config` (`startswith`, `:236`) — `pip install x && <проверка>` прошёл бы. (а) Чинить в этой карточке (файл в owns):
полное совпадение для всех видов — риск задеть строки `forge-check`; (б) новые виды — полным совпадением, старые не
трогать, слабость — строкой находки в пачку `forge/7` — **рекомендация** (зона FG7-90).

**F7. Ночь платит задачу `runners`.** `nightly.yml:77` зовёт тот же файл. (а) Принять 2-3 мин (оценка) — **рекомендация**:
одна дорога для двери и ночи; (б) звать `runners` только из двери — нужен вход, вторая дорога.

**F8. `runtime_probe` у TS-строки.** (а) Та же форма, что у первой строки (`--profile dry-playwright`) — **рекомендация**:
строки отличаются только значениями; что `runtime_probe.py` делает с node-профилем — меряет N6b. (б) Без ключа (данные
по умолчанию «нет записи», `dry_stub.py:399-400`) — строки расходятся по форме.

---

## 6. Читатели каждого затронутого файла (правило 7)

Блок `python -B tools/owns_readers.py --paths <owns §3> --names runner_rows,hidden_checks,selftest_n2` к брифу НЕ
приложен — Lead прикладывает его до диспатча; ниже — ручной поиск дизайнера (Grep tool).

Команды и счёт:
- `runners/|ts-playwright|python-pytest` по `tools/` — 0; контроль той же формы с `|dry-story\.yml` — 7 строк в 1 файле
  (`tools/test_workflows.py`).
- `python-pytest|ts-playwright` по `PKG/scripts` — 3 вхождения: `dry_stub.py` 1, `kit.json` 1, `runner.json` 1.
- `runners` по `T/*.py` — читатели папки: только `dry_stub.py` (`:325`, `:361-384`, `:1394-1427`); прочие совпадения —
  другие значения слова (`scenario_clock` `--runners`, `STAGE_RUNNERS`, `script_runners`, `launch_check.runner_row`).
- `test_workflows|dry-story|runners/` по `.githooks/` — 0 (контроль `piles\.py|architecture_gate` — 2, `commit-msg`); по
  `.claude/settings.json` — 0 (контроль `hygiene_gate|dispatch_gate` — 2).
- `test_workflows` по `tools/` — 2 файла: сам тест и `test_test_quarantine.py:1427` (комментарий).
- `dry-story\.yml|setup-node|playwright` (`-i`) по `.github/` — `canon.yml:49,52,82`, `nightly.yml:77`.

| Файл | Читатель | Вердикт |
|---|---|---|
| `runners/ts-playwright/` (новый) | `dry_stub.runner_rows`/`runner_row` (`:361-384`) | читает вторую строку при каждой постройке мира; поведение для истории неизменно (E1, E6) |
| то же | `dry_stub.selftest_n2` (`:1392-1394`) | меняется в этом потоке (F2) |
| то же | `dry_world.build_story_world :326`, `dry_stub :1030, :1045, :1427, :2107` | неизменны (идут по `kit["runner"]` = `python-pytest`) |
| то же | `form_filler` через `test_file:<lang>` (`dry_stub.py:613`) | не достигается в N6a; в N6b — FV1-19 (E11) |
| `.github/workflows/dry-story.yml` | `canon.yml:82` (дверь `dry_only`), `nightly.yml:77` | неизменны; получают ещё одну задачу в вызове (F7) |
| то же | `tools/test_workflows.py` (`NAMES :29`, `:176-186`, `:253`, `:421-447`, `:558-566`) | меняется в этом потоке (пункт 3) |
| то же | `tools/ci_read.py` (`WORKFLOW = "canon.yml"`, finish-spec §6 `:542`) | неизменен (читает задачи прогона, новая задача — ещё одна строка вывода) |
| `tools/test_workflows.py` | сам тест; `tools/test_test_quarantine.py:1427` (комментарий); `.githooks/` — 0 | неизменны |
| `T/dry_stub.py` (`selftest_n2`) | задача `tables` `dry-story.yml:106-110`; `scenario_walk.py --witness-for` (не перемерено) | неизменны (имя функции и CLI те же) |
| поток FV3-13 | пишет `T/dry_exits.py`, `T/test_scenario_dry_1.py` | не пересекается с этими owns |
| поток FV3-12 | пишет `T/fixtures/stories/dry-<type>/`, `dry-types.json`, `test_scenario_dry_1.py` | не пересекается (папка `dry-1/runners/` не его) |

---

## 7. Свидетель

- CI (главный): дверь `dry_only` на ветке узла — `python -B tools/ci_read.py start --ref <ветка> --var dry_only=true`,
  чтение `python -B tools/ci_read.py jobs <run>`. Зелёные: `list`, все `parts` (в том числе `exits:s5` — на строке
  `python-pytest`, ВРЕМЕННОЙ инвариант E6), `tables` (с новым пином `selftest_n2`), `runners` (две строки `runner <id>:
  exit 0`). `exits:s5` С TS-СТРОКОЙ — свидетель N6b (F1, F5).
- Локально (узко): `python -m pytest tools/test_workflows.py -q`; `python -B ai-packages/qa-factory/scripts/tests/dry_stub.py
  --selftest` (время неизвестно — ОЦЕНКА; дольше 5 мин → «canon judges», свидетель — `tables`); `python -B
  ai-packages/qa-factory/scripts/selftest.py --lang`. TS-проект локально не гоняется (Node на машине не замерен).

---

## 8. Мелкие выборы, закрытые дизайнером

- Node 22 (LTS) в `setup-node`; без `cache:` (лок маленький; `cache: npm` без лок-файла роняет шаг — оценка).
- Версия `@playwright/test` — точная, по `npm view` в день сборки; лок-файл обязателен (`npm ci`).
- Только Chromium (`--with-deps chromium`), не три браузера.
- Проверка строк — инлайн-python в шаге, а не новый скрипт (новый файл вне owns N6).
- `timeout-minutes: 15` с комментарием «until the Lead's cap» (по образцу `tables :81`).
- Фрагмент `changelog.d` не пишется (фикстура тестов и CI; не поведение пакета).

## 9. Замеченное за пределами брифа

- Finish-spec `:474` называет owns N6 «`dry-story.yml` (только шаги образа)», а спека П1-б `:660` — `canon.yml`; актуально
  первое (F-P16 (а)); противоречия для карточки нет.
- `hidden_checks :236` — слабость `startswith` (F6).
- Строки обхода `s5` под pytest (54 вхождения) — их параметризация по строке раннера — работа N6b, не FV3-7.

## 10. След чтения

finish-spec `docs/tasks/specs/20261117-p1b-finish-spec.md:130-189, 455-554`; П1-б `20261113-p1b-dry-story-spec.md:650-665,
771-772` + Grep `F5|раннер|runner`, `9\.3|ref_without_hash`; `plans/piles/live-run-fvf/batch-3-live-run-fvf.md` (Grep FV3-11,
FV3-2/3/4/7), `batch-1…:58` (FV1-19); `.github/workflows/dry-story.yml` целиком; `tools/test_workflows.py:1-99, 170-189,
212-259, 381, 393-462`; `T/dry_stub.py:290-418, 486-595, 1378-1434` + Grep `runner|lang|test_file|def`; `T/dry_world.py:300-335`;
`T/test_scenario_dry_1.py:75-154`; `T/fixtures/stories/dry-1/` (Glob; `kit.json`; `runners/python-pytest/*` целиком);
`T/fixtures/form-fill-rules.json:230-274`; `T/form_filler.py:775-844`; `T/fixtures/form-rounds.json:1-60`;
`PKG/references/case-markers.json` целиком; `PKG/scripts/profile_contract.py:245-281`; `PKG/design/architecture.md:33-74,
173-184` + Grep заголовков; `tools/architecture_gate.py` Grep; `docs/TESTING.md:75-114` + Grep заголовков;
`PKG/scripts/slow_tests.json` Grep `dry` (`test_scenario_dry_1.py` 221.6); `test-layers.json` Grep `canon_only`.
Обозначения: `T` = `ai-packages/qa-factory/scripts/tests`, `PKG` = `ai-packages/qa-factory`.
