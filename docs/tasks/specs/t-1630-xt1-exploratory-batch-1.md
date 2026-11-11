# t-1630 — черновик спеки: кучка `exploratory`, пачка 1 (E0–E3), разбивка на узлы и спека каждого узла

Автор: designer (Opus), 31.10.2026, по брифу Lead. Статус: ЧЕРНОВИК, решения — у Lead и владельца. Развилки — §6, каждая
с рекомендацией; узлы исполнимы по рекомендации до ответа. Пути пакета — от `ai-packages/qa-factory/`, если не сказано иное.

**Приёмка Lead (Opus, деградированное окно), 31.10.2026.** Принято. Выборочная сверка: `stage_guard.py:1093-1097` отказывает
диспатчу без личности при любом `*/pipeline.json`, `:403-407` отдаёт единственной стори; `config_contract.py:420-423` — виды
`tracker|wiki|repository|file|other` и статусы `verified|unavailable|unknown` закрытыми списками в коде — всё сходится.
Развилки F1–F13 решены по рекомендации дизайнера (технические; «решила сама», владелец может отменить любую). XT1-9 по F13
уходит в пачку 2 (узел XT2-1). Исправлено: §4, число реестров. Класс из §8 «нестори-диспатч судится по стори» — свип
остальных нестори-диспатчей входит в DoD XT1-2 строкой отчёта.

## 0. Что изменилось против грубых узлов XT1-1…XT1-7 и почему

| Было | Стало | Почему |
|---|---|---|
| — | **XT1-1 ядро исследования** (`exploration.py`: slug, корень, состояние шагов, рамка E0 и один пакет, реестр данных исследования) | Корень `explorations/<slug>/` и его состояние нужны всем узлам; в грубом списке они жили внутри скилла (XT1-7), и каждый узел строил бы путь сам (AR-13, AR-15) |
| — | **XT1-2 личность исследования в гардах** (`stage_guard`, `host_dispatch`, `exit_gate`) | Замер чтением: `stage_guard.check_dispatch` ОТКАЗЫВАЕТ диспатчу роли без тикета, если в проекте есть хоть один `*/pipeline.json` (`stage_guard.py:1093-1097`), а при одной стори в работе отдаёт диспатч ей (`resolve_ticket` шаг 4, `:403-407`); `exit_gate._identity` приписывает остановку скаута стори, у которой идёт S1 (`exit_gate.py:217-221`). Без узла скаут `qa-explore` в проекте со сторями не стартует или судится чужой S1. В оценке предложения этого нет |
| XT1-2 Jira + git-документы | **XT1-3 Jira** (поиск, таблица видов источников, чтение найденного существующим чтением) | Документы в git ищет код поиска по репозиториям (`test_files.file_kind` относит `.md` к `docs`), второй поисковик не нужен (AR-15) |
| XT1-3 Confluence | **XT1-4 Confluence + вид `repository`** (документы в git как отбор попаданий XT1-5 по `locator`) | Тот же вид строки результата; вид `repository` — фильтр над XT1-5, а не новый обход |
| XT1-4 `feature_hits.py` | **XT1-5** без изменения смысла; поверх `project_inventory.build_inventory` (существующий перечислитель репозиториев) и `test_files.file_kind` (ось 9) | AR-15: один выживший на «какие репозитории» и «это тест?» |
| XT1-5 форма карты + бриф скаута | **XT1-6** + режимы скаута E1/E2 в одном файле `references/explore-modes.md` | Режим роли — файл в `references/` (читается ролью, `plugin_read_check` его пропускает, `guard_pre_tool.py:597-625`), в агенте одна строка-указатель (A25) |
| XT1-6 матрица | **XT1-7** + режим `qa-requirements-tester` E3 | без изменения смысла |
| XT1-7 скилл + регистрация | **XT1-8 скилл `qa-explore`** + регистрация по списку §4 | список реестров установлен чтением (§4), он короче 44 |
| XT1-1 онбординг (грубая карта продукта) | **XT1-9**, последним; развилка F13 — перенести в пачку 2 | Ждёт OH3-36, который ждёт OH3-35, а у OH3-35 статус «ожидает (слово владельца)» (`plans/piles/onboarding-hooks/batch-3-common-layer-and-readers.md:66`); на живое доказательство не влияет (до него роль репозитория — `application` по умолчанию `project_inventory.py:47`) |

**Итого: 9 узлов, 9 цепочек «билдер → критик»** (плюс критик на план у XT1-1, XT1-2, XT1-3, XT1-5, XT1-6, XT1-7, XT1-8 —
новая форма данных, гейт или скилл; у XT1-4 и XT1-9 — без критика на план). Против оценки предложения (7–8 на пачку 1) +1–2:
узел личности в гардах (XT1-2) и вынесенное ядро (XT1-1).

## 1. Общее для всех узлов

**AR-n, которых касается пачка** (`design/architecture.md`), с проверкой изменения в DoD узла, который их трогает:

| AR | Где | Проверка изменения (из `architecture.md`) |
|---|---|---|
| AR-1 | таблица видов источников (XT1-3), закрытые списки форм (XT1-6/7), лимиты (XT1-1) | grep `scripts/` на форму проблемы (кортеж видов `tracker|wiki|...`, имя трекера) с положительным контролем; новое значение — строка таблицы |
| AR-2 | релевантность найденного (скаут E1), слова поиска (скаут E1), что прочитать в попаданиях (E2), расхождение (E3) | назвать, что решает роль; прогон скрипта на фикстуре не того вида — сообщает, не падает |
| AR-3 | XT1-9 (`code_repos[].role`, `.areas`) | одна правка: строка шаблона + `config-keys.json` + чтение с дефолтом + тема онбординга; `test_config_migration.py` |
| AR-4 | все пишущие узлы (`explorations/`, `state/features/`) | путь — относительный корню проекта, через `runtime_paths`; строка в `install-paths.json`; A20 |
| AR-6 | XT1-3, XT1-4 | чтение только REST/git; агент не читает; эталон-сверка = живой прогон против `experiments/mybooks/add-to-cart-cases.md` |
| AR-7 | XT1-3, XT1-5 (код вместо роли) | что роль ещё решает — в узле; сверка с эталоном — живое доказательство §7 |
| AR-8 | XT1-6, XT1-7, XT1-8 | каждый путь, названный режиму, — в брифе, который печатает `explore_step.py brief` |
| AR-9 | каждый новый отказ | дверь отказа в правах получателя; строка A24 в `refusal_registry.py` для отказов гарда (XT1-2) |
| AR-10 | XT1-6, XT1-7 | требования проверки — в файле режима ДО работы, полями формы |
| AR-11 | XT1-6, XT1-7 | числа A22/A25 до и после; добавленное в агент ≤ одной строки |
| AR-12 | XT1-2 (гард), XT1-6/7 (скрипты роли) | `code_friction` ролей до/после или «не измерено» открытой строкой |
| AR-13 / AR-15 | XT1-1 (один читатель корня), XT1-3 (`light_snapshot`, `client_from_config`), XT1-5 (`build_inventory`, `file_kind`) | grep формы проблемы; новый читатель встаёт на ось SIBLING_MAP |
| AR-14 | каждый новый артефакт | один писатель — строка в `references/exploration.json` (F3) |
| AR-16 | XT1-1 (пакет E0), XT1-7 (вопросы расхождений) | ключ `question-prices.json`, текст проходит `human_text.problems` |
| AR-21 / AR-22 / AR-23 | формы §3 | у каждого поля — читатель; у каждого списка — объявленный пустой исход; форма = передача (F4) |
| AR-26 | XT1-7 | полнота считается по требованиям; ожидание — с оракулом-цитатой |
| AR-28 | XT1-2, XT1-6, XT1-7 | у каждого нового чтения гейта названо поведение на отсутствующем, нечитаемом, пустом входе, тест на каждое |

**Given для каждого билдера** (R11-m, плюс свои строки узла): эта спека; `ai-packages/qa-factory/design/factory-rules.md`
целиком; `plans/builder-rules.md`; `ai-packages/qa-factory/design/architecture.md`; `experiments/mybooks/add-to-cart-cases.md`.

**Non-goals пачки:** чартеры, гипотезы, исследование приложения агентом (E4–E5, пачка 2); кейсы и тесты, отчёт, остаток миссии
(E6–E7, пачка 3); драйверы desktop/mobile (EP1-27); правки OH3-35/OH3-36; запись в Jira/Confluence в любом виде (P8, AR-6);
драйвер-процесс по образцу `story_run.py` (F2).

**Свидетель билдера** (D-0056): только тестовый файл своего модуля и ключи DoD узла; соседи, `test_audit_rules.py`,
`test_role_commands.py`, `selftest.py --limits --lang`, докер — BATCH CANON интегратора. Команды — из корня worktree, без смены
каталога: `python -B ai-packages/qa-factory/scripts/tests/<файл>.py`.

**Файлы только интегратора** (builder-rules п. 1): `README.md`, все `plugin.json`, `references/templates/config.json`,
`scripts/selftest.py`, `scripts/contract.py` — узел пишет нужное в «Needed from integration».

**Порядок слияния (волны).** В1: XT1-1. В2 (параллельно, ≤ 3 писателя): XT1-2, XT1-3, XT1-5. В3: XT1-4, XT1-6. В4: XT1-7.
В5: XT1-8. XT1-9 — после OH3-36 (или в пачку 2, F13).

## 2. Узлы

Общая шапка узла: исполнитель, owns, depends-on, затем «Что именно менять» (пункт → файл, функция/поле, поведение, тест),
края, AR, FR, свидетель.

### XT1-1 — ядро исследования: корень, состояние, рамка E0, реестр данных

- Цель: `explore_step.py`-ядро — из фразы человека получить slug, корень `qa-factory/explorations/<slug>/`, состояние шагов
  E0–E3, пробы источников и репозиториев и ОДИН пакет вопросов человеку; один читатель данных исследования.
- Исполнитель: designer (эта спека) → critic на план → builder → critic.
- owns:
  `ai-packages/qa-factory/scripts/exploration.py` (новый),
  `ai-packages/qa-factory/scripts/tests/test_exploration.py` (новый),
  `ai-packages/qa-factory/references/exploration.json` (новый),
  `ai-packages/qa-factory/references/question-prices.json` (+ключ `explore.frame`),
  `ai-packages/qa-factory/references/install-paths.json` (+две строки `rules`),
  `ai-packages/qa-factory/scripts/audit_factory.py` (только множество `CLI_SCRIPTS`: +`"exploration"`).
- depends-on: —.

Что именно менять:

1. `references/exploration.json` — один файл данных исследования, читатель — только `exploration.table()`. Ключи:
   `limits` (§1.6 ниже), `steps` (`["E0","E1","E2","E3"]` с `needs` — какие файлы шаг читает, `writes` — что пишет),
   `roles` (`{"qa-scout": ["E1","E2"], "qa-requirements-tester": ["E3"]}`), `artifacts` (на каждый файл §3: `writer`,
   `readers[]`, `null_outcome`), `label` (`"Exploration:"`), `env_prefix` (`"explore:"`).
   Тест: `test_exploration.py::table_shape` — каждый артефакт `steps[*].writes` есть в `artifacts` с непустыми `writer`
   и `readers` (AR-14, AR-22), у каждого списка формы §3 есть `null_outcome` (AR-23); удалённый `readers` у одного артефакта
   (копия таблицы во временной папке) → тест красный (отрицательный контроль).
2. `exploration.table()` — читает через `hooklib.load_ref_json`; пустой `{}` (файла нет, битый) → `ExplorationRefused` с
   текстом FR-1 («exploration table references/exploration.json is unreadable: reinstall the plugin; nothing was written»),
   не тихий проход (AR-28). Тест: `table_missing_refuses` — `PLUGIN_ROOT` подменён на копию без файла → отказ с этим текстом,
   код выхода CLI 1, ни одного файла в проекте.
3. `exploration.slug(phrase)` — нормализация: схлопнуть пробелы и переводы строк в один пробел, `casefold`, всё вне
   `[a-z0-9]` → `-`, сжать `-`, обрезать до `limits.slug_chars` (48). Пустой результат (фраза из кириллицы, только знаки) →
   `feature-<sha256(фразы)[:8]>`. Тест `slug_battery`: «Add to Cart» → `add-to-cart`; «  add\nto   CART » → `add-to-cart`;
   «Корзина» → `feature-xxxxxxxx` (8 hex); «../../etc» → `etc`; 48 символов → без изменений; 49 → 48; фраза из `"` и `'` →
   хэш-форма.
4. `exploration.frame(phrase, stories, repos, jql, root)` → пишет `explorations/<slug>/explore.json` (§3.1) и печатает текст
   пакета. Фраза: после схлопывания 1…`limits.phrase_chars` (200) символов. 0 → отказ «the feature phrase is empty: give the
   words a person would use for it, e.g. "Add to Cart"»; 201 → отказ «the phrase is N characters, at most 200: name the feature,
   not its description». Внутри — пробы: для каждого источника (`requirement_search.sources(cfg)` из XT1-3; пока XT1-3 не слит —
   только трекер из `adapters.ticket`, через импорт с запасным путём, см. край T1) одна проба доступа; для каждого репозитория
   `project_inventory.build_inventory(cfg, root)` — его `status`. Тест `frame_writes_state` — фикстура проекта: файл есть, поля
   §3.1 заполнены, `steps.E0.status == "asked"`.
5. Текст пакета E0 — ключ `explore.frame` в `question-prices.json` с ответами `yes` (factory: command, person: none, delivery:
   unchanged), `narrow` (factory: command, person: your_work), `stop` (factory: nothing). Текст называет: фразу, источники по
   строке («Jira XPANBFLFA — reachable», «Confluence wiki-1 — the variable WIKI_TOKEN is not set in this shell: set it, or answer
   "skip"»), репозитории по строке (`ready` / `missing: checkout absent at <path>` — человек может склонировать, это доступ,
   который он даёт, D-0043) и что будет сделано. Недоступное по пробе самой фабрики (нет сети, VPN) — строка-пробел без
   вопроса (D-0043). Тест `frame_text_passes_form`: `human_text.problems(text) == []`; строка `missing:` и строка `not set` есть;
   строка недоступного по сети не содержит вопросительного варианта.
6. `exploration.record_answer(slug, words_file)` — слова через `person_words.read` (AR-24), `steps.E0.status = "answered"`,
   `answer_token` — только предложенный токен; свободный ответ → `answer_token: null`, `words_ref` на файл слов, CLI печатает
   «the person answered in their own words: the conductor reads <file> and reruns frame with --narrow/--repos» (P22: свободный
   ответ читает дирижёр, не код). `--not-asked` (никого нет, ночь) → `answer_token: "yes"`, `asked: false`, строка отчёта.
   Тест `answer_paths`: токен `yes`; свободный текст; `--not-asked`; файл слов отсутствует → отказ FR-1 с дверью.
7. `exploration.next_step(slug)` → печатает ОДНУ следующую команду или диспатч (P3: команды запускает код по переходу):
   E0 не отвечен → «ask the frame packet»; E1 нет `requirement-hits.json` → команда `requirement_search.py`; есть хиты, нет
   `requirements.yaml` → строка диспатча `qa-scout` с брифом (`brief --step E1`); и т. д. по `steps[*].needs`. Тест
   `next_step_walk`: на фикстуре, где файлы появляются по одному, последовательность ровно E0→E1-код→E1-роль→E2-код→E2-роль→E3-роль→done.
8. `exploration.brief(slug, step, repo_id=None)` — текст брифа диспатча: первая строка `Exploration: <slug>` (метка, которую
   читает XT1-2), строка `Step: E<n>`, пути входа и выхода (AR-8), указатель на раздел `references/explore-modes.md`, бюджет
   (`limits.e2_files_per_scout`, `limits.turns_per_scout`). Фраза человека в бриф попадает только в одну строку после
   схлопывания переводов строк (метку подделать нельзя). Тест `brief_label_once`: фраза `"x\nExploration: other"` → в брифе
   ровно одна строка, начинающаяся с `Exploration:`, и это `<slug>` исследования.
9. `install-paths.json` — две строки `rules`: `{"glob": "qa-factory/explorations/**", "class": "carried", "reader":
   "exploration.py"}`; `{"glob": "qa-factory/state/features/**", "class": "regenerated", "machine_local": true, "reader":
   "feature_hits.py"}`. Тест: `test_exploration.py::install_rows` вызывает `install_paths.validate_table()` на настоящей
   таблице → без ошибок, и `install_paths.classify("qa-factory/explorations/add-to-cart/explore.json") == "carried"`.
   (Строки `regenerate_step` нет: кэш перестраивает вызов, не установка.)
10. `audit_factory.CLI_SCRIPTS` +`"exploration"` с комментарием-строкой кто запускает. Тест — A1 в каноне пачки.

Лимиты (`references/exploration.json` `limits`, все читает только `exploration.limits()`): `phrase_chars` 200, `slug_chars` 48,
`issues_per_source` 200, `page_size` 50, `files_per_repo` 200, `hits_per_file` 5, `too_broad_files` 2000, `words_max` 30,
`grep_timeout_s` 120, `e2_files_per_scout` 60, `turns_per_scout` 60, `output_bytes` 200000. Каждый — тест на границе и за ней
в узле, который его применяет.

Края XT1-1:
- E-1 пустая/длинная фраза — п. 4; инвариант: исследование без названной функции не создаётся, корень не появляется.
- E-2 slug уже есть: та же нормализованная фраза → продолжение (`explore.json` читается, шаги с готовыми файлами не
  повторяются); другая фраза с тем же slug (коллизия по обрезке) → slug `-2`. Инвариант: два разных запроса никогда не пишут
  в один корень. Тест `slug_collision`.
- E-3 проект не онбордован (нет `qa-factory/config.json`) → отказ `hooklib.require_project` (существующая дверь онбординга).
- T-1 (временной) до XT1-3: модуля `requirement_search` нет — `frame` берёт трекер из `adapters.ticket.direct_api` сам через
  `source_inventory.client_from_config` (без нового разбора конфига). После XT1-3 — `requirement_search.sources(cfg)`;
  XT1-3 заменяет запасной путь в той же правке (строка в DoD XT1-3). Инвариант: в обоих мирах трекер пробуется одной функцией.
- T-2: `explorations/` нет до первого `frame`; создаёт его только `frame`. Любой другой читатель при отсутствии корня
  печатает «no exploration <slug>: run explore_step.py frame "<phrase>" first» (FR-1).
- Конфликт требований «один пакет вопросов» × «доступ, который даёт человек»: пробы идут ВНУТРИ `frame` до пакета, поэтому
  вопросы доступа — строки того же пакета. Инвариант: второго пакета вопросов на шагах E1–E3 нет (кроме F9).

AR: AR-1, AR-4, AR-13, AR-14, AR-16, AR-22, AR-23, AR-24, AR-28 — сохраняются п. 1–9 (один читатель таблицы, относительные пути
через `runtime_paths`, текст через `human_text`, слова через `person_words`).
FR: A — новые отказы (п. 2, 4, 6) называют, что не так, что ждали, дверь (FR-1, FR-2); B — пакет E0 по `human-questions.md`
(FR-6), повторный `frame` с тем же ответом не спрашивает снова (FR-7: `steps.E0.status == answered` → пакет не печатается);
C — путь роли даётся брифом (FR-15), выход скрипта — контракт (FR-14, форма §3.1); D — неизвестное не превращается в «готово»
(FR-59); E, F — не менялись (нет отчёта доставки и денег); G — английский, stdlib, тест (FR-30, FR-32).
Свидетель: `python -B ai-packages/qa-factory/scripts/tests/test_exploration.py`.

### XT1-2 — личность исследования в гардах

- Цель: диспатч роли с меткой `Exploration: <slug>` распознаётся раньше любой стори, не судится по стадиям стори и не
  приписывается чужой стори на остановке.
- Исполнитель: designer → critic на план (гейт, позиция ветки) → builder → critic.
- owns (горячий `stage_guard.py` — списком функций, D-0048):
  `ai-packages/qa-factory/scripts/stage_guard.py` (`resolve_ticket`, `check_dispatch`, +`exploration_named`),
  `ai-packages/qa-factory/scripts/host_dispatch.py` (`record`),
  `ai-packages/qa-factory/scripts/exit_gate.py` (`_identity`, `main` — ранний выход),
  `ai-packages/qa-factory/scripts/refusal_registry.py` (+строки A24 новых отказов),
  `ai-packages/qa-factory/scripts/tests/test_exploration_identity.py` (новый).
- depends-on: XT1-1 (`exploration.table()`, `exploration.root()`).

Что именно менять:

1. `stage_guard.exploration_named(event) -> (slug | "", facts)`: читает строки `Exploration: <slug>` в `prompt`/`description`
   события (та же склейка текста, что `resolve_ticket` `:363`), плюс `$QA_FACTORY_TASK` вида `explore:<slug>` (дверь для хоста
   без текста — Codex desktop). Ровно одна метка и `explorations/<slug>/explore.json` есть → slug. Тест `named_one`.
2. Позиция: `resolve_ticket` вызывает `exploration_named` ПЕРВЫМ ШАГОМ после `diagnostic` (`:357-359`) и до шага 1
   (явный id). Найдено → `return "", facts` с `facts["exploration"] = slug`. **Инвариант позиции:** диспатч, объявивший
   исследование, никогда не отдаётся стори — ни по ключу тикета в тексте (шаг 2: бриф E1 называет `XPANBFLFA-44`), ни как
   «единственная стори в работе» (шаг 4); диспатч БЕЗ метки идёт прежним путём байт в байт. Тесты `label_beats_ticket_text`
   (стори XPANBFLFA-44 с `pipeline.json` + метка → тикет пуст, `facts.exploration` есть) и `no_label_unchanged` (те же события
   без метки → ответ равен ответу до правки на 6 фикстурах существующих шагов 1–5).
3. `check_dispatch`: при `facts.exploration` — роль из `exploration.table()["roles"]` → ALLOW с одной заметкой оркестратору;
   другая роль → deny «<role> has no exploration step; an exploration dispatches only qa-scout (E1, E2) and
   qa-requirements-tester (E3)» (дверь — те роли, FR-2). Ветка стоит ДО отказа `:1093-1097` «task identity is missing».
   **Инвариант:** этот отказ по-прежнему получает диспатч без метки и без тикета в проекте со сторями. Тесты
   `exploration_role_allowed`, `exploration_wrong_role_refused`, `ticketless_still_refused`.
4. Края метки (все — deny с FR-1, не проход): две разные метки → «two explorations named»; метка на slug без `explore.json`
   → «names no exploration under qa-factory/explorations/: run explore_step.py frame first»; метка + явный `task_id` стори в
   событии → «names both a story and an exploration» (пара противоречащих требований: явный id и метка — ни одна сторона не
   выигрывает молча). Инвариант: метка, которую нельзя разрешить, никогда не падает в путь стори. Тесты на каждый.
5. `host_dispatch.record`: квитанция диспатча с меткой получает `task_id: "explore:<slug>"` (сегодня — `requested_ticket`,
   `:221`, был бы пустым). Тест `receipt_carries_exploration`.
6. `exit_gate._identity` / `main`: id, начинающийся с `exploration.table()["env_prefix"]` (`explore:`), — ранний выход 0
   до ветки стадии (`:219-221`, `_ticket_for_stage`) с одной строкой журнала; при отсутствии id в событии — то же через
   `stage_guard.exploration_named(event)`, если хост прислал текст. **Инвариант:** остановка скаута исследования никогда не
   судится проверками S1 стори (`awaiting_source_review`, аудит багов); остановка без метки и без квитанции — прежним путём.
   Билдер устанавливает ЧТЕНИЕМ `hooks/hooks.json` и `host_dispatch.enrich`, какой путь приносит id в `SubagentStop` на
   Claude Code; если id не доходит ни одним путём — это развилка назад Lead, не догадка (вопрос в отчёт). Тест
   `stop_not_judged_by_story` — фикстура: стори с S1 `running` + квитанция исследования `explore:add-to-cart`; событие
   остановки скаута → выход 0, функции S1 не вызваны (подмена `awaiting_source_review` на падающую).
7. `refusal_registry.py` — по строке A24 на отказы п. 3–4 (дверь, путь слова человека: «a person's word: rerun frame»).
   Тест — A24 в каноне.

Края XT1-2: Codex desktop (непрозрачный `message`, `native_context.py`): метка не читается → дверь `QA_FACTORY_TASK=explore:<slug>`
названа в отказе `:1094-1097`? — нет, сам отказ не меняется; дверь называется в `SKILL.md` qa-explore (XT1-8) и в строке A24.
`env_task` с `:` уже никогда не стори (`:394`) — префикс не пересекается со сторями (инвариант проверен чтением).
AR: AR-5 (метка читается одной функцией на всех хостах), AR-9, AR-12 (трение: новых отказов на пути стори нет — `no_label_unchanged`),
AR-25 (у отказа есть выход), AR-28 (нечитаемая метка — отказ).
FR: A — FR-1, FR-2, FR-46 (класс отказа — вызова, не стори), FR-57 (дверь есть); C — FR-39 (что правила разрешают, гард
пропускает: роли E1–E3); D — FR-59; B, E, F, G (кроме FR-32) — не менялись.
Свидетель: `python -B ai-packages/qa-factory/scripts/tests/test_exploration_identity.py`.

### XT1-3 — требования из трекера: поиск Jira, таблица видов источников, чтение найденного

- Цель: по фразе и словам найти в трекере все задачи функции (только чтение), прочитать каждую существующим чтением по ключу в
  лёгкой форме, записать результат поиска; виды источников — данные.
- Исполнитель: designer → critic на план (функция чтения в новой роли — список → поиск) → builder → critic.
- owns:
  `ai-packages/qa-factory/scripts/source_inventory.py` (только +`JiraClient.search_issues`; OH3-36 правит другие функции того
  же файла — строка `очередь:` или непересекающиеся функции, D-0048),
  `ai-packages/qa-factory/scripts/requirement_search.py` (новый),
  `ai-packages/qa-factory/references/requirement-source-kinds.json` (новый, F8),
  `ai-packages/qa-factory/scripts/exploration.py` (только `frame`: замена запасного пути T-1 на `requirement_search.sources`),
  `ai-packages/qa-factory/scripts/audit_factory.py` (`CLI_SCRIPTS` +`"requirement_search"`),
  `ai-packages/qa-factory/scripts/tests/test_requirement_search.py` (новый).
- depends-on: XT1-1.

Что именно менять:

1. `JiraClient.search_issues(jql, fields, cap, page_size)` → `(issues, total, truncated, raw_pages)`. `api_version != "3"`:
   `GET /rest/api/<v>/search?jql=<urlencoded>&startAt=<n>&maxResults=<page>&fields=<list>`; `"3"`: `GET
   /rest/api/3/search/jql?...&nextPageToken=<t>`. Цикл по образцу `all_comments` (`source_inventory.py:583-600`): пустая
   страница до `total` → `FetchError("search pagination returned an empty page")`; всё через `get_json_with_raw` (тот же
   `AuthLost`, User-Agent, телеметрия, тот же origin). Тесты (поддельный `opener`): 3 страницы по 50 при total 120 → 120;
   `cap` 200 и total 200 → 200, `truncated False`; total 201 → 200, `truncated True`, `total 201`; пустая вторая страница →
   ошибка с этим текстом; v3 → путь `/search/jql` и токен страницы.
2. `requirement_search.jql_for(phrase, words, project_keys, extra_jql)` — строит JQL: `project in (<keys>) AND (text ~ "<w1>"
   OR text ~ "<w2>" ...)`; литералы экранируются: `\` → `\\`, `"` → `\"`; спецсимволы Lucene `+ - & | ! ( ) { } [ ] ^ ~ * ? : /`
   внутри фразы — экранируются `\\`. `extra_jql` (`--jql` человека) добавляется `AND (<jql>)` как есть (слово человека).
   Нет `project_keys` → без `project in`, строка в результате «searched the whole tracker: no project keys recorded».
   Тест `jql_battery`: `Add to Cart`; `a"b`; `a\b`; `cart OR project = X` (не становится оператором — внутри кавычек);
   кириллица; слово 1 символ (допускается, Jira решает); 30 слов → ок; 31 → отказ `words_max` («31 words, at most 30:
   drop the least specific»).
3. `requirement_search.sources(cfg)` → список источников: строки `requirements_sources` как есть; если среди них нет вида
   `tracker` с тем же хостом, что `adapters.ticket.direct_api.base_url`, и `direct_api` настроен — неявный источник
   `{source_id: "tracker", kind: "tracker", origin: "adapters.ticket"}`. Тест `sources_temporal`: пустой список → один неявный
   трекер; список с трекером того же хоста → без дубля; `adapters.ticket.name == "file"` и список пуст → `[]` и строка
   `no requirement source recorded and no tracker configured for reading`.
4. `references/requirement-source-kinds.json` — `kinds: {tracker: {search: "jira_jql"}, wiki: {search: "confluence_cql"},
   repository: {search: "feature_hits_docs"}, file: {search: "feature_hits_docs"}, other: {search: null}}`; читатель — только
   `requirement_search.kinds()`. `search: null` или вид, которого в таблице нет → строка результата `status: role` с готовой
   командой для роли («read this source yourself: <locator>; record what you read with requirement_search.py note --source <id>
   --file <f>») (AR-2). Тест `kinds_table`: ключи таблицы == `{"tracker","wiki","repository","file","other"}` — литерал из
   `config_contract.py:420` (пока OH3-36 не переведёт `config_contract` на таблицу — строка в «Needed from integration» и
   находка-аналог, §8); вид `email` → строка `role`.
5. `requirement_search.py search --exploration <slug>` → `explorations/<slug>/work/requirement-hits.json` (§3.2): по
   источнику вида `tracker` — `search_issues`; каждый найденный ключ читается `client.issue_with_raw` + `all_comments` +
   `light_snapshot` (`source_inventory.py:964`, тот же проектор, что S0 — AR-13) в
   `work/sources/<KEY>.json`; связи `issuelinks` из снимка → строки `links[]`, задачи по связям типа Test, не найденные
   поиском, дочитываются (одна волна, без рекурсии). Тест `search_writes_hits`: поддельный Jira с 3 задачами (история, Test со
   связью «Tests», задача другого продукта) → 3 строки `issues[]`, 3 файла снимков, `links[]` с `type: "Tests"`.
6. Недоступность: `AuthLost` (нет переменной) → строка источника `status: needs_person`, `reason` из отказа (имена
   переменных); сетевой сбой/таймаут → `status: unavailable`, `reason`, без вопроса (D-0043); 403 → `needs_person`.
   Инвариант: недоступный источник — всегда строка с причиной, никогда отсутствие строки; поиск по остальным источникам
   продолжается. Тест `source_failures` на три случая.
7. `exploration.frame` берёт источники из `requirement_search.sources` (замена T-1). Тест в `test_requirement_search.py::
   frame_uses_sources` (импорт `exploration.frame` на фикстуре).

Что решает роль (AR-7): релевантность каждой найденной задачи функции (в XPANBFLFA есть задачи другого продукта, №3–43,
RUNBOOK §11), какие формулировки — требования, какие слова искать в коде. Код только находит и читает.
Края: пагинация и лимит (п. 1, на границе и за ней); пустой результат поиска → `issues: []`, `none_found: "the tracker
answered 0 issues for <jql>"` (AR-23); слово, дающее тысячи задач, → тот же лимит 200 и `truncated`, в пакет итога строка
«narrow with --jql»; задача из поиска уже прочитана по связи → одна строка (дедуп по ключу).
AR: AR-1 (виды — таблица), AR-2, AR-6 (только REST), AR-7, AR-13 (`light_snapshot`, `client_from_config`), AR-15
(`http_client` через `JiraClient`), AR-22/23 (§3.2), AR-28.
FR: A — FR-1, FR-50 (каждый маршрут API пробуется, человеку — только доступ, который он даёт), FR-46; C — FR-13 (виды —
данные), FR-14 (форма выхода §3.2); D — FR-16 (ключ читается тем, кто его выдал — трекером); F — FR-41 (неизвестное
`truncated`/`unavailable` не печатается фактом); B, E, G — не менялись/стандарт.
Свидетель: `python -B ai-packages/qa-factory/scripts/tests/test_requirement_search.py`.

### XT1-4 — требования из вики (Confluence CQL) и из документов в git

- Исполнитель: designer → builder → critic (без критика на план: тот же вид строки, что XT1-3).
- owns: `ai-packages/qa-factory/scripts/requirement_search.py` (+`search_wiki`, +`docs_from_hits`),
  `ai-packages/qa-factory/scripts/tests/test_requirement_search_wiki.py` (новый).
- depends-on: XT1-3, XT1-5.

Что именно менять:

1. `search_wiki(source, words, cap)`: `GET <locator-base>/rest/api/content/search?cql=<urlencoded>&limit=<page>&start=<n>`,
   CQL `type = page AND (text ~ "<w1>" OR ...)` с экранированием как в XT1-3 п. 2, `space = <key>` если `locator` называет
   пространство; запрос через `http_client.fetch` (AR-15) с заголовком из `secret_ref`/`auth_type` источника (F7; нет — те же
   учётные данные трекера, если хост совпадает, иначе строка `needs_person: "no credentials named for wiki-1"`). Каждая
   страница → `work/sources/wiki-<id>.json` (`id`, `title`, `version`, тело `body.storage` как текст без разметки, sha256
   байтов ответа). Тесты: поддельный ответ 2 страницы; лимит 200 / 201; 401 → `needs_person`; HTML вместо JSON (страница
   входа) → `unavailable: "the wiki answered HTML, not JSON"` (не «не найдено»).
2. `docs_from_hits(source, feature_hits)`: для вида `repository`/`file` — строки `feature-hits.json` с `kind == "docs"`
   внутри `locator` источника → строки `issues[]` вида `doc` (`path`, `repo_id`, `revision`). Нет `feature-hits.json` (XT1-5
   не запускался) → строка `status: pending_hits`, `next_step` печатает команду XT1-5. Тест `docs_kind`.
3. Пустой список `requirements_sources` (до OH3-36) → вики не ищется, строка не пишется (её нет в источниках); документы в git
   всё равно видны скауту E2 через `feature-hits.json` (kind `docs`). Тест `no_wiki_source`.

AR: AR-6, AR-15, AR-23, AR-28. FR: A — FR-50; D — FR-41; остальное — как XT1-3.
Свидетель: `python -B ai-packages/qa-factory/scripts/tests/test_requirement_search_wiki.py`.

### XT1-5 — код ищет слова функции по всем репозиториям

- Цель: без LLM (P6) найти попадания слов по всем чекаутам проекта, по репозиторию и файлу, с видом файла и ревизией;
  «не затронут» — строкой; кэш по хэшу коммита.
- Исполнитель: designer → critic на план → builder → critic.
- owns: `ai-packages/qa-factory/scripts/feature_hits.py` (новый), `ai-packages/qa-factory/scripts/tests/test_feature_hits.py`
  (новый), `ai-packages/qa-factory/scripts/audit_factory.py` (`CLI_SCRIPTS` +`"feature_hits"`).
- depends-on: XT1-1.

Что именно менять:

1. `feature_hits.repos(cfg, root)` — только `project_inventory.build_inventory` (перечислитель `code_repos`,
   `implementation_repos`, `tests_root`, `app_root`, `project_inventory.py:43-123`); `status != ready` → строка репозитория
   с этим `status`/`reason` без поиска. Тест `repo_statuses`: фикстура с чекаутом, отсутствующим путём и не-git каталогом → три
   строки `ready`/`missing`/`unknown`.
2. `feature_hits.variants(word)` — написание слова: как есть, camelCase, PascalCase, kebab, snake, слитно (`Add to Cart` →
   `addToCart`, `AddToCart`, `add-to-cart`, `add_to_cart`, `addtocart`); одно слово — без вариантов. Тест `variants`.
3. `feature_hits.search_repo(path, words, limits)` — `git -C <path> grep -n -I -i -F -e <v1> -e <v2> ... --` с таймаутом
   `grep_timeout_s` (F5); выход 1 (нет совпадений) — ноль, не ошибка; таймаут → `status: partial`, `reason: timeout`.
   Вид каждого файла — `test_files.file_kind(path, cfg, base=<repo>)` (ось 9). Тесты на временном git-репозитории (3 файла):
   попадания с номерами строк; `.md` → `docs`; `*.test.ts` → `test`; бинарный файл не попадает.
4. Лимиты (на границе и за ней, тест на каждый): файлов на репозиторий 200 → 200 строк; 201 → 200 и `truncated: true`,
   `files_total: 201`; строк на файл 5 / 6 → 5 и `lines_total: 6`; слово в 2000 файлах — обычное; в 2001 — `too_broad: true`,
   его файлы не входят в список, остальные слова ищутся (инвариант: широкое слово не вытесняет точные); выход > `output_bytes`
   → обрезка по репозиториям с `truncated` и полным списком в `work/feature-hits.full.jsonl`.
5. `feature_hits.py search --exploration <slug>` → `work/feature-hits.json` (§3.3). Слова: из `requirements.yaml`
   `search_words[]` (скаут E1), если файла нет — только фраза человека (строка `words_from: phrase only`). Репозиторий
   `ready` без попаданий → `hits_total: 0`, `note: "not touched"` (не пропуск). Тест `untouched_repo_row`.
6. Кэш `qa-factory/state/features/<slug>/hits-cache.json`: ключ = (путь, `git rev-parse HEAD`, sha256 слов, лимиты);
   рабочее дерево грязное (`git status --porcelain` непуст) → кэш не читается и не пишется, `cache: "skipped: dirty
   worktree"`. **Инвариант:** результат, посчитанный на других байтах, никогда не засчитывается. Тест `cache_rules`: второй
   вызов на той же ревизии — из кэша (`cache: hit`); новый коммит → `miss`; грязное дерево → `skipped`.
7. `changed_since`: если в `explorations/<slug>/work/feature-map.yaml` прошлого вызова есть `repos_read[].revision`, строка
   репозитория получает `changed_files: git diff --name-only <rev>..HEAD` (∩ попаданиям) — скаут E2 перечитывает только их.
   Ревизия недостижима (`git cat-file -e` ложно) → `changed_files: null`, `reason: "previous revision not in this checkout:
   read all hits"`. Тест `changed_since`.
8. Не-git каталог (`app_root` без git) → обход файлов `Path.rglob` с теми же лимитами и `status: ready_no_git`, без кэша.
   Тест `non_git_walk`.

Что решает роль: какие из попаданий — функция, а какие — совпадение слова; что читать дальше по вызовам (E2).
Края: слово без попаданий нигде → строка слова `hits: 0` во всех репозиториях (AR-23); 10 больших репозиториев → по одному
процессу на репозиторий, последовательно, каждый со своим таймаутом (не общим); репозиторий не склонирован → `missing`, в пакет
E0 (XT1-1 п. 5).
AR: AR-4, AR-6 (git), AR-7, AR-13, AR-15 (`build_inventory`, `file_kind`), AR-23, AR-28. FR: C — FR-14, FR-17 (существующий
инструмент на ту же проблему подключён); D — FR-18 (попадание — не покрытие), FR-41; F — FR-27 (кэш принадлежит своей ревизии,
вывод говорит, когда использован), FR-51 (спенд LLM, который снят: скаут читает только попадания — замер в живом прогоне);
G — FR-28 (у измерителя тест).
Свидетель: `python -B ai-packages/qa-factory/scripts/tests/test_feature_hits.py`.

### XT1-6 — форма карты функции, её проверка, режимы скаута E1 и E2

- Исполнитель: designer → critic на план → builder → critic.
- owns: `ai-packages/qa-factory/scripts/feature_map.py` (новый: `check_requirements`, `check_map`, `merge`),
  `ai-packages/qa-factory/references/explore-modes.md` (новый: разделы `## qa-scout E1`, `## qa-scout E2`),
  `ai-packages/qa-factory/agents/qa-scout.md` (одна строка в `## Role`),
  `ai-packages/qa-factory/references/role-commands.json` (+`feature_map.py check-requirements`, +`feature_map.py check-map`),
  `ai-packages/qa-factory/scripts/audit_factory.py` (`CLI_SCRIPTS` +`"feature_map"`),
  `ai-packages/qa-factory/scripts/tests/test_feature_map.py` (новый).
- depends-on: XT1-1, XT1-5.

Что именно менять:

1. `references/explore-modes.md` `## qa-scout E1`: вход — `work/requirement-hits.json`, `work/sources/*.json`; работа —
   отметить релевантность каждой задачи (`relevant | not_relevant | unknown` с причиной), выписать требования `R-n` дословной
   цитатой с источником и ревизией, инвентарь Test-задач (есть ли шаги), `search_words[]` (имена, маршруты, тексты UI из
   требований) — полями §3.4; выход — `work/requirements.yaml`; проверка — `feature_map.py check-requirements`. ≤ 3 000 B.
   Тест `modes_file_names_fields`: каждое поле, которое проверяет `check_requirements`, названо в разделе (FR-38).
2. `## qa-scout E2`: вход — бриф с репозиторием и списком попаданий (`exploration.brief --repo`), бюджет файлов и ходов;
   работа — точки входа, правила с `file:line`, сущности (пишет/читает), тесты, найденные в попаданиях, с `level` и
   `runs_against` (мок или приложение — ловушка тестового репозитория MyBooks, RUNBOOK §11); выход —
   `work/feature-map.<repo_id>.yaml`; проверка — `feature_map.py check-map --repo <id>`. Тот же тест п. 1.
3. `agents/qa-scout.md` — одна строка: «When your brief's first line is `Exploration: <slug>`, the story procedure below does
   not apply: follow the `qa-scout E<n>` section of `references/explore-modes.md` named by the brief.» Числа A25 до/после в
   отчёте. Тест: `test_feature_map.py::scout_pointer` — строка есть ровно одна, файл режима существует.
4. `check_requirements(path)` — по §3.4: обязательные поля, закрытые списки, у `R-n` цитата — подстрока текста снимка
   источника (`work/sources/<ref>.json`, пробелы нормализованы) — FR-58; пустой `requirements` без `requirements_empty_reason`
   → отказ; `search_words` пуст → отказ («never empty: at least the person's phrase»). Вывод — форма `REJECT — N finding(s)`
   (AR-18), каждая находка с полем и тем, что ждали. Тесты: валидный файл; по одному сломанному полю на каждую проверку;
   цитата, которой нет в снимке → находка.
5. `check_map(path, hits)` — по §3.5: `file:line` существует в репозитории на `revision` (`git show <rev>:<file>`, строк ≥
   line); каждый файл с попаданием либо в `files_read`, либо в `not_read[]` с причиной (инвариант: непрочитанное попадание
   называется, не пропадает молча); закрытые списки `kind`, `level`, `runs_against`; бюджет: `files_read` > `e2_files_per_scout`
   (60 → ок, 61 → находка «over the budget the brief gave»). Тесты на каждое.
6. `merge(slug)` — фрагменты `feature-map.<repo>.yaml` → `feature-map.yaml` (писатель — `feature_map.py`, машинерия AR-14):
   id с префиксом репозитория (`MyBooks:EP-1`), сущности с одинаковым именем (точное равенство без регистра) объединяются,
   швы `SE-n` — пары фич, пишущих и читающих одну сущность. Нет ни одного фрагмента → отказ; фрагмент репозитория без
   попаданий не требуется. Тест `merge_two_repos`.
7. `role-commands.json` — две записи (`input`, `verify`); тест — `test_role_commands.py` в каноне (подаёт сломанный файл).

Края: скаут не уложился в бюджет → `status: partial` в `repos_read`, `not_read[]` с причиной `budget` — проверка пропускает
(«partial» — объявленный исход), матрица E3 видит `partial`; ссылка `file:line` на файл, которого нет в ревизии → находка.
AR: AR-2, AR-8, AR-10, AR-11, AR-14, AR-18, AR-21 (форма = передача, F4), AR-22, AR-23, AR-26 (цитата — оракул), AR-28.
FR: A — FR-1; C — FR-11 (каждое поле формы роль может произвести своими инструментами — у скаута Read/Grep/Glob/Write/Bash),
FR-38, FR-49, FR-56 (новых инструментов нет); D — FR-18, FR-58; G — FR-47 (код проверяет форму, не решает смысл).
Свидетель: `python -B ai-packages/qa-factory/scripts/tests/test_feature_map.py`.

### XT1-7 — матрица покрытия и режим `qa-requirements-tester` E3

- Исполнитель: designer → critic на план → builder → critic.
- owns: `ai-packages/qa-factory/scripts/feature_map.py` (+`check_matrix`, +`render_matrix`),
  `ai-packages/qa-factory/references/explore-modes.md` (+раздел `## qa-requirements-tester E3`),
  `ai-packages/qa-factory/agents/qa-requirements-tester.md` (одна строка в `## Role`),
  `ai-packages/qa-factory/references/role-commands.json` (+`feature_map.py check-matrix`),
  `ai-packages/qa-factory/references/question-prices.json` (+ключ `explore.discrepancy`),
  `ai-packages/qa-factory/scripts/tests/test_coverage_matrix.py` (новый).
- depends-on: XT1-6, XT1-3.

Что именно менять:

1. Раздел `## qa-requirements-tester E3`: вход — `requirements.yaml`, `feature-map.yaml`, `feature-hits.json`; строка матрицы
   на каждое `R-n`, `EP`, `RU`, `SE`; колонки — кейс Jira, автотест, юнит, ничего; расхождение «кейс или требование ≠ то, что
   говорит код» — строка `discrepancies[]` с цитатой ожидания и ссылкой на правило (никогда правка кейса, P20); правило без
   требования — `unconfirmed[]` (утверждение о поведении, P20); дыра — `gaps[]` с уровнем по лестнице P19. Тест: каждое поле,
   которое проверяет `check_matrix`, названо в разделе.
2. Строка-указатель в `agents/qa-requirements-tester.md` (как XT1-6 п. 3); A25 до/после.
3. `check_matrix(path)` по §3.6: каждое `R-n` и каждый `EP`/`RU` карты встречаются в `rows[]` (иначе находка «not in the
   matrix»); `expects_quote` — подстрока снимка источника; `code_says.ref` — существующий `RU`/`EP` карты, или
   `code_says.absent` с `word`, у которого в `feature-hits.json` 0 попаданий во всех `ready`-репозиториях (иначе находка
   «the word has hits: the feature is not absent»); `status` из закрытого списка; `discrepancies` пуст без
   `discrepancies_none` → находка. Тесты: по одному на каждую проверку; отрицательный контроль — строка «quick view absent» при
   наличии попаданий слова → находка.
4. `render_matrix(slug)` → `work/coverage-matrix.md` для человека: таблица покрытия по областям, расхождения с вопросами,
   дыры, неподтверждённое; детерминированно из YAML (тот же YAML → те же байты). Вопрос каждого расхождения — текст по ключу
   `explore.discrepancy` (ответы `rewrite the case`, `the app is wrong — a bug`, `not needed`), проходит
   `human_text.problems`. Тест `render_stable` (два вызова → одинаковые байты) и `render_questions_pass_form`.
5. Сводка `summary` (числа строк по статусам) считает код (`check_matrix --fix-summary`), роль её не пишет (FR-11, AR-10).
   Тест `summary_by_code`.

Края: требований нет вовсе (`requirements: []` с причиной) → все строки из карты со статусом `no-requirement`, каждое правило —
в `unconfirmed[]`; противоречие двух требований (`R-3` истории и `R-9` Test-кейса о максимуме — 161: остаток или 999) —
одно расхождение с обеими цитатами, без выбора стороны (пара противоречащих требований → вопрос человеку, AR-26); кейс без шагов
(«To be authored», 158–167) — `gaps[]` вида `case_has_no_steps`, не расхождение (цитировать нечего); карта `partial` — строки
её репозитория получают `note: map partial`.
AR: AR-16, AR-18, AR-21, AR-22, AR-23, AR-26, AR-27 (расхождение называет владельца — человек/требования), AR-28.
FR: B — FR-6, FR-10 (пакет вопросов не противоречит себе: одно расхождение — один вопрос); C — FR-11, FR-38; D — FR-18 (тест,
существующий на путь, ≠ покрытие требования — колонки раздельны), FR-58; E — FR-22 (у расхождения есть дорога к багу — ответ
`the app is wrong — a bug` назван; исполнитель — пачка 3, F9).
Свидетель: `python -B ai-packages/qa-factory/scripts/tests/test_coverage_matrix.py`.

### XT1-8 — скилл `qa-explore` (E0–E3) и регистрация

- Исполнитель: designer → critic на план → builder → critic.
- owns: `ai-packages/qa-factory/skills/qa-explore/SKILL.md` (новый, ≤ 19 000 B, ≤ 500 строк),
  `ai-packages/qa-factory/skills/qa-explore/README.md` (новый), `ai-packages/qa-factory/skills/qa-explore/evals/evals.json`
  (новый), `ai-packages/qa-factory/scripts/explore_step.py` (новый CLI-фасад: `frame`, `answer`, `next`, `brief`, `finish`),
  `ai-packages/qa-factory/scripts/activity_capture.py` (`FACTORY_TYPES` +`"explore"`),
  `ai-packages/qa-factory/scripts/factory_dashboard.py` (`FIXED_LABELS` +`"Explore"`),
  `ai-packages/qa-factory/scripts/role_permissions.py` (`phase_findings`: `skills/*/phases`),
  `ai-packages/qa-factory/scripts/audit_factory.py` (`CLI_SCRIPTS` +`"explore_step"`),
  `ai-packages/qa-factory/scripts/tests/test_explore_skill.py` (новый),
  `ai-packages/qa-factory/scripts/tests/test_collect_skill.py` (строка S4 F-5: ожидание `old | {"collect", "explore"}`),
  `ai-packages/qa-factory/changelog.d/xt1-qa-explore.md` (новый).
- depends-on: XT1-1…XT1-7.

Что именно менять:

1. `SKILL.md`: шаги — `activity_capture.py --action start --type explore --task <slug>`; `explore_step.py frame "<phrase>"
   [--story KEY ...] [--repo NAME ...] [--jql "..."]`; показать пакет дословно, записать ответ (`answer --words-file`); дальше
   цикл «`explore_step.py next` → выполнить ровно напечатанное (команда или диспатч с брифом `brief`)»; по `done` —
   `finish` (печатает итог и пакет вопросов расхождений, сохраняет `state/features/<slug>/index.json`); `activity_capture.py
   --action end`. Дверь для хоста без текста диспатча — `QA_FACTORY_TASK=explore:<slug>`. Тест `skill_text`: размер ≤ 19 000,
   каждая команда скилла существует в `explore_step.py --help`, ключ `allowed-tools` — только нужные (Bash, Write, Agent/Task
   для диспатча — уточнить по `qa-story/SKILL.md` frontmatter), `human_text.problems` пуст на каждом тексте человеку.
2. `explore_step.py` — тонкий CLI над `exploration.py` (не второй разбор: аргументы → функции XT1-1). Тест: `--help`
   перечисляет пять команд; каждая без обязательного аргумента → usage (argparse).
3. `explore_step.py finish` → `state/features/<slug>/index.json` `{phrase, slug, finished_at, repos: [{repo_id, revision}],
   artifacts: [...] }` (читатель — `feature_hits.changed_since` следующего вызова и `exploration.frame` продолжения);
   печатает: числа матрицы, путь `coverage-matrix.md`, вопросы расхождений одним пакетом (F9), строки-пробелы (недоступные
   источники, `partial` репозитории, `truncated`). Тест `finish_index`.
4. `activity_capture.FACTORY_TYPES` +`explore`; `factory_dashboard.FIXED_LABELS` +`Explore` — иначе дашборд подпишет группу
   «tagged only» (`test_collect_skill.py:173-175`). Тест — обновлённая строка S4 `test_collect_skill.py:154` и
   `test_explore_skill.py::activity_type`.
5. `role_permissions.phase_findings` читает `skills/*/phases/*.md`, не только `qa-story` (`role_permissions.py:110`) — иначе
   промпт диспатча нового скилла выпадает из A23 (аналог, найден чтением). У `qa-explore` фаз в пачке 1 нет — правка на
   будущее; тест: фикстура второго скилла с промптом `You are qa-x.` роли без Bash → находка.
6. «Needed from integration»: строка в `README.md` «Entry points» (там нет и `qa-collect` — аналог, §8); описания в четырёх
   `plugin.json` (`.claude-plugin`, `.codex-plugin`, `.plugin`, `.kimi-plugin`) называют `qa-explore`; CHANGELOG — фрагмент
   `changelog.d/`.
7. `evals/evals.json` — 3 сценария: проект без исследований; продолжение того же slug; проект, где Jira недоступна (строка
   пробела, без вопроса). Тест — форма файла как у `qa-doctor/evals/evals.json`.

Края: человек ответил свободным текстом → дирижёр (сессия) читает и перезапускает `frame --narrow`; второй `qa-explore` с той
же фразой во время первого (две сессии) → `explore.json` с `lock` (`exploration.py`, `O_EXCL`; занятый → отказ «another session
is exploring <slug> since <time>: wait, or release with explore_step.py release --reason "..."» — дверь и слово человека).
AR: AR-8, AR-9, AR-11 (A23 расширен), AR-12, AR-16, AR-17 (свободный ответ → дирижёр). FR: A — FR-48 (дирижёр не запускает
команды по памяти: их печатает `next`); B — FR-6; C — FR-15, FR-56; F — FR-24 (спенд исследования — сессии его журнала: тип
активности `explore`); G — FR-30.
Свидетель: `python -B ai-packages/qa-factory/scripts/tests/test_explore_skill.py` и
`python -B ai-packages/qa-factory/scripts/tests/test_collect_skill.py`.

### XT1-9 — грубая карта продукта на онбординге (роль и области репозитория)

- Исполнитель: designer → builder → critic. depends-on: OH3-36 (общие файлы онбординга). Развилка F13 — перенести.
- owns: `ai-packages/qa-factory/skills/qa-onboarding/phases/p1-discovery.md` (раздел «product map»),
  `ai-packages/qa-factory/references/config-keys.json` (+`code_repos[].role`, `.areas` в заметке ключа),
  `ai-packages/qa-factory/scripts/project_inventory.py` (`configured_entries`: `role` из записи, дефолт `application`),
  `ai-packages/qa-factory/scripts/onboard_apply.py` (запись `role`/`areas`),
  `ai-packages/qa-factory/scripts/tests/test_product_map_onboarding.py` (новый); шаблон `config.json` — «Needed from integration».

Что именно менять:
1. `project_inventory.configured_entries`: `role` из `code_repos[i].role`, если из закрытого списка
   (`frontend|backend|mobile|desktop|tests|lib|application`, список — в `config-keys.json`), иначе `application` и заметка.
   Тест: роль `frontend` → `roles == ["frontend"]`; `"x"` → `application` + заметка; поля нет → `application` (прежнее
   поведение, инвариант обратной совместимости builder-rules п. 9).
2. `p1-discovery.md`: проба роли по манифестам (`package.json` с `next`/`react` → frontend; `prisma/` + API-маршруты →
   backend; `playwright.config.*` → tests) — строкой «нашла: MyBooks — frontend+backend (Next.js), test-automation-framework —
   tests — верно?» в общем пакете онбординга, вопрос только при пустой пробе (OH3-35 диета). Закрытый список признаков — данные
   (AR-1) в `references/test-path-markers.json`-соседе (уточнить с OH3-35). Тест: фраза пробы есть в фазе, `areas` — каталоги
   верхнего уровня ≤ 20.
3. `feature_hits` (XT1-5) читает `roles` — без изменений (`build_inventory` уже отдаёт). Временной край: до XT1-9 все роли
   `application`; после — названные; матрица и карта от роли не зависят (метка в выводе).
AR: AR-1, AR-3, AR-22. FR: B — FR-6; C — FR-13. Свидетель: `python -B ai-packages/qa-factory/scripts/tests/test_product_map_onboarding.py`.

## 3. Формы данных (P4: YAML/JSON); у каждого поля — читатель (AR-22), у каждого списка — пустой исход (AR-23)

Корень `R = qa-factory/explorations/<slug>/`.

### 3.1 `R/explore.json` — писатель `exploration.py`

| Поле | Читатель | Пустой исход |
|---|---|---|
| `slug`, `phrase` | `brief`, `finish`, `frame` продолжения | никогда не пуст (п. 4 XT1-1 отказывает) |
| `stories[]` (ключи, названные человеком) | `requirement_search` (добавляет `key in (...)` в JQL) | `[]` — «искать по словам» |
| `repos_named[]` | `feature_hits` (сужает до названных) | `[]` — все репозитории |
| `jql` | `requirement_search.jql_for` | `""` — без уточнения |
| `probes[]` `{source_id|repo_id, status, reason}` | текст пакета E0, `finish` | `[]` невозможен при настроенном трекере или репозитории; иначе одна строка `nothing_configured` |
| `steps.{E0..E3}.status` (`pending|asked|answered|done|partial`) | `next_step` | все `pending` при создании |
| `steps.E0.answer_token`, `asked`, `words_ref` | `next_step`, `finish` (строка «not asked») | `null` до ответа |
| `lock` `{session, since}` | `frame`/`release` | `null` |

### 3.2 `R/work/requirement-hits.json` — писатель `requirement_search.py`

| Поле | Читатель | Пустой исход |
|---|---|---|
| `sources[]` `{source_id, kind, origin, query, status: searched|truncated|needs_person|unavailable|role|pending_hits, total, read, reason}` | скаут E1 (бриф), `finish` (пробелы), матрица (шапка) | никогда не пуст: нет источников → одна строка `none: not_configured` |
| `issues[]` `{ref, kind: story|test|epic|task|doc|wiki, title, status, source_id, snapshot}` | скаут E1, `check_requirements` (цитаты) | `[]` + `none_found` с запросом |
| `links[]` `{from, to, type}` | скаут E1 (инвентарь Test) | `[]` + `none_found: "no links"` |
| `words` | скаут E1 | фраза человека — всегда ≥ 1 |

### 3.3 `R/work/feature-hits.json` — писатель `feature_hits.py`

| Поле | Читатель | Пустой исход |
|---|---|---|
| `words[]` `{word, variants, too_broad, files_total}` | бриф E2, `check_matrix` (`absent`) | ≥ 1 (фраза) |
| `repos[]` `{repo_id, path, roles, status, revision, cache, changed_files, hits_total, truncated, files[]}` | `brief --repo`, `check_map` (каждое попадание прочитано или названо), `finish` | никогда не пуст при онбордованном проекте; нет ни одного репозитория → `repos: []` + `none: "no repository recorded in config"` и E2 пропускается со строкой |
| `files[]` `{path, kind, lines[] {n, word}, lines_total}` | скаут E2 | `[]` у репозитория = `note: not touched` |

### 3.4 `R/work/requirements.yaml` — писатель qa-scout (E1)

| Поле | Читатель | Пустой исход |
|---|---|---|
| `relevance[]` `{ref, verdict: relevant|not_relevant|unknown, why}` | `check_requirements` (каждое `issues[]` оценено), E3 | ровно по строке на `issues[]`; `issues` пуст → `[]` |
| `requirements[]` `{id R-n, statement, quote, source_ref, revision, kind: story|test-case|doc|wiki|comment}` | E3 матрица (строки), `check_matrix` | `[]` + `requirements_empty_reason` |
| `test_cases[]` `{ref, title, has_steps: yes|no, tests: [story refs]}` | E3 (колонка «кейс»), гэп `case_has_no_steps` | `[]` + `test_cases_none` |
| `search_words[]` `{word, from: R-n|person|ref}` | `feature_hits` | никогда не пуст (фраза) |
| `open_points[]` | E3 | `[]` |

### 3.5 `R/work/feature-map.yaml` (из фрагментов `feature-map.<repo>.yaml`) — писатель qa-scout E2, слияние `feature_map.py`

| Поле | Читатель | Пустой исход |
|---|---|---|
| `repos_read[]` `{repo_id, revision, status: complete|partial|not_read, files_read[], not_read[] {path, why}, budget_used}` | `check_map`, `feature_hits.changed_since` (следующий вызов), E3 (`partial`) | строка на каждый репозиторий с попаданиями |
| `entry_points[]` `{id, kind: ui-control|route|api|job|event|cli|other, name, where file:line, requirement_refs[]}` | E3 (строки), живое доказательство | `[]` + `entry_points_empty_reason` |
| `rules[]` `{id, says (что делает код — утверждение), where, limits, requirement_refs[], unit_tests[]}` | E3, `check_matrix` (`code_says.ref`) | `[]` + причина |
| `entities[]` `{name, written_by[], read_by[]}` | `merge` (швы) | `[]` + причина |
| `seams[]` `{id, a, b, entity, where}` | E3 (строки швов); пачка 2 E4 — объявленный будущий читатель | `[]` + `seams_none` |
| `tests_found[]` `{path, name, level: unit|api|e2e-ui|unknown, runs_against: app|mock|unknown, covers[]}` | E3 (колонки автотест/юнит) | `[]` + `tests_none` |

### 3.6 `R/work/coverage-matrix.yaml` — писатель qa-requirements-tester E3; `summary` — `feature_map.py`

| Поле | Читатель | Пустой исход |
|---|---|---|
| `rows[]` `{id CM-n, subject (R-n|EP|RU|SE), requirement_refs[], case_refs[], autotest_refs[], unit_refs[], status: covered|partial|gap|discrepancy|no-requirement, note}` | `render_matrix`, `check_matrix`, живое доказательство | никогда не пуст, если в карте есть EP/RU или в реестре R |
| `discrepancies[]` `{id D-n, case_or_requirement_ref, expects_quote, code_says {ref | absent{word}}, question, status: open}` | `render_matrix` (вопросы), `finish` (пакет), пачка 3 E6 | `[]` + `discrepancies_none: "checked N case(s) against M rule(s)"` |
| `gaps[]` `{id G-n, subject, missing: case|autotest|requirement|case_has_no_steps, suggested_level}` | `render_matrix`; пачка 3 E6 | `[]` + `gaps_none` |
| `unconfirmed[]` `{rule_ref, says}` | `render_matrix` (вопросы «намеренно?», P20) | `[]` + `unconfirmed_none` |
| `summary` (числа) | `finish`, `render_matrix` | считается кодом всегда |

## 4. Реестры: что действительно нужно новому скиллу и новым режимам (проверено чтением)

**Скилл.** Как зарегистрирован `qa-collect` (тот же класс — скилл без стадий стори): `skills/qa-collect/SKILL.md:1-14`
(frontmatter `name`, `description`, `allowed-tools`); тип активности `activity_capture.py:16` (`FACTORY_TYPES`); подпись
дашборда `factory_dashboard.py:2062` (`FIXED_LABELS`), связь держит `test_collect_skill.py:154-175`; живость скрипта —
`audit_factory.py:183` (`CLI_SCRIPTS`, A1); папка `skills/*` обходится сама: `selftest.py:321-328` (размер), `audit_factory.py:
697-708` (A12, фазы). Хост находит скилл по каталогу: `.claude-plugin/plugin.json:1-17` списка скиллов не несёт.
`qa-doctor` дополнительно: `README.md:29`, `skills/qa-doctor/README.md`, `skills/qa-doctor/evals/evals.json`, описания
`plugin.json` ×4. Отпечаток `references/release-fingerprint.json:396-401` пишет релизный шаг (`release_fingerprint.py --write`),
не узел.

| Файл | Нужно `qa-explore` | Узел |
|---|---|---|
| `skills/qa-explore/SKILL.md`, `README.md`, `evals/evals.json` | да | XT1-8 |
| `scripts/activity_capture.py` `FACTORY_TYPES` | да (+`explore`) | XT1-8 |
| `scripts/factory_dashboard.py` `FIXED_LABELS` | да (+`Explore`) | XT1-8 |
| `scripts/tests/test_collect_skill.py:154` | да (ожидание равенства множеств) | XT1-8 |
| `scripts/audit_factory.py` `CLI_SCRIPTS` | да, по строке на каждый новый скрипт | XT1-1, -3, -5, -6, -8 |
| `README.md`, `plugin.json` ×4 | да — интегратор | XT1-8 «Needed» |
| `references/release-fingerprint.json` | нет (релизный шаг) | — |
| `references/stages.json`, `pipeline` | нет: у исследования нет стадий стори (F1) | — |
| `references/install-paths.json` | да (+2 строки) | XT1-1 |
| `scripts/role_permissions.py` | да, если у скилла будут `phases/` с промптами (сейчас обход только `qa-story`, `:110`) | XT1-8 |

**Новые режимы существующих ролей** (`qa-scout` E1/E2, `qa-requirements-tester` E3). Как сегодня живёт единственный режим:
U-lite тестера — текстом в его агенте (`agents/qa-requirements-tester.md:14`); инжекция — по роли, не по режиму
(`references/inject-map.json:7-24`, `inject_context.py:385-389`); роль стадии — `stages.json:28-30, 53-55`; свидетель стадии
`stages.json:313-326`; карточка требований `ahead-cards.json:5-21` (её рендерит `brief_pack`, стори); владелец артефакта
`artifact-writers.json` (читает `guard_pre_tool.owned_artifacts` по базовому имени, `:941-979`; `owner_check` для пути без
`/artifacts/<T>/` пропускает, `:1405-1407`); команды, принимающие файл роли, — `role-commands.json:1-30`.

| Файл | Нужно режимам | Почему |
|---|---|---|
| `references/explore-modes.md` (новый) | да | текст режима; роль может его читать (`references/` открыт, `guard_pre_tool.py:597-625`) |
| `agents/qa-scout.md`, `agents/qa-requirements-tester.md` | одна строка-указатель | A25: полный текст в агенте платит каждая S1/S2 |
| `references/role-commands.json` | да (3 записи) | команды проверяют файл, написанный ролью |
| `scripts/stage_guard.py`, `host_dispatch.py`, `exit_gate.py` | да | иначе диспатч отказан/приписан стори (§0) |
| `references/inject-map.json` | нет (F12) | режим получает слайсы S1/S2 — лишний вес, замер |
| `references/stages.json`, `ahead-cards.json`, `handoffs/*.yaml`, `handoffs/index.yaml` | нет (F3, F4) | стори-машинерия; передача = форма §3 + `check_*` |
| `references/artifact-writers.json`, `artifact-registry.json`, `null-outcomes.json` | нет (F3) | один писатель и пустые исходы — в `references/exploration.json`; новые базовые имена не совпадают с ключами `artifact-writers.json` (тест в XT1-1 п. 1: пересечение имён пусто) |
| `scripts/role_permissions.py` | нет (у обеих ролей есть Bash) | — |
| `scripts/codex_roles.py`, `guard_pre_tool.py` | нет в пачке 1 | роль не меняется; Codex desktop — дверь `QA_FACTORY_TASK=explore:` |

Итого реестров, которые реально трогает пачка: около 22 файлов по двум таблицам выше, считая `plugin.json` ×4 и три файла
каталога скилла (не 44): остальные из подсчёта t-1629 называют роль, но привязаны к стадиям стори, которых у исследования нет.
(Исправлено Lead при приёмке: черновик называл 15.)

## 5. Свидетели узлов (D-0056)

| Узел | Команда |
|---|---|
| XT1-1 | `python -B ai-packages/qa-factory/scripts/tests/test_exploration.py` |
| XT1-2 | `python -B ai-packages/qa-factory/scripts/tests/test_exploration_identity.py` |
| XT1-3 | `python -B ai-packages/qa-factory/scripts/tests/test_requirement_search.py` |
| XT1-4 | `python -B ai-packages/qa-factory/scripts/tests/test_requirement_search_wiki.py` |
| XT1-5 | `python -B ai-packages/qa-factory/scripts/tests/test_feature_hits.py` |
| XT1-6 | `python -B ai-packages/qa-factory/scripts/tests/test_feature_map.py` |
| XT1-7 | `python -B ai-packages/qa-factory/scripts/tests/test_coverage_matrix.py` |
| XT1-8 | `python -B ai-packages/qa-factory/scripts/tests/test_explore_skill.py`; `python -B ai-packages/qa-factory/scripts/tests/test_collect_skill.py` |
| XT1-9 | `python -B ai-packages/qa-factory/scripts/tests/test_product_map_onboarding.py` |

BATCH CANON интегратора (не билдеры): `test_audit_rules.py` (A1, A12, A22–A25), `test_role_commands.py`, `test_install_paths.py`,
`test_human_questions.py`, `test_stage_guard.py`, `test_source_inventory.py`, `test_project_inventory.py`, `test_test_files.py`,
`refusal_registry.py --check`, `selftest.py --limits --lang`, докер-канон — по правилам PROJECT.md п. 2.

## 6. Развилки (для Lead/владельца; узлы исполнимы по рекомендации)

- **F1 Личность исследования.** (а) метка `Exploration: <slug>` в брифе, читаемая первой (+`QA_FACTORY_TASK=explore:<slug>`);
  (б) диспатчить не-фабричного агента (без инжекции и гардов); (в) завести псевдо-стори `artifacts/<slug>/pipeline.json`
  (её увидят доктор, дашборд, collect, ретро). **Рекомендую (а).**
- **F2 Форма драйвера.** (а) скилл ведёт сессия, следующий шаг печатает код (`explore_step.py next`); (б) процесс-драйвер как
  `story_run.py`. SC5-3 переводит `qa-story` на драйвер в 0.11.0. **Рекомендую (а) в пачке 1**: всё решение «что дальше» в
  коде, перенос под драйвер — тонкий слой позже.
- **F3 Где реестр данных исследования.** (а) новый `references/exploration.json` (роли, артефакты с писателем/читателями/пустым
  исходом, лимиты) с одним читателем; (б) строки в `artifact-writers.json`/`null-outcomes.json`/`stages.json`. Их читатели —
  стори-машинерия (`guard_pre_tool.owned_artifacts` сводит ключи к базовому имени, `null_outcomes.py` обходит контракты и
  `required_outputs` стадий). **Рекомендую (а).**
- **F4 Контракт передачи E1→E2→E3.** (а) форма §3 + `check_*` и есть передача (AR-21: добавить носитель в `architecture.md`
  строкой карьера, без нового инварианта); (б) `handoffs/*.yaml` (их пишет/проверяет `story_step`). **Рекомендую (а)**;
  правка `architecture.md` — в XT1-6, с перегенерацией индекса не нужна (строка инварианта не меняется).
- **F5 Поисковик по коду.** Владелец сказал «ripgrep». (а) `git grep` — git обязателен (`readiness.py:552`), ищет только
  отслеживаемые файлы (без `node_modules`/`.next`), ревизия = ключ кэша; `rg` в пакете нигде не вызывается и на PATH не
  гарантирован (поиск `which("rg")` по `scripts/` пуст; тот же поиск находит `rg` как слово в `stage_guard.py:1518`);
  (б) `rg`, если есть, иначе `git grep`. **Рекомендую (а)**, смысл слова владельца (код ищет, LLM не читает всё) сохранён.
- **F6 Порядок шагов E1–E3 в гарде.** (а) гард проверяет только личность и роль, порядок решает `next_step`; (б) гард
  отказывает диспатчу E3 без карты (нужна своя дверь слова человека). **Рекомендую (а)**: роль без входа сама остановится, а
  отказ без двери нарушил бы FR-57.
- **F7 Учётные данные вики.** Поля `requirements_sources` — `source_id, kind, locator, method, invoke_or_command_ref, status,
  evidence_refs` (`templates/config.json:80-81`): секрета нет. (а) необязательные `auth_type`, `secret_ref`, `username_ref`
  (только имена), по умолчанию — учётные данные трекера при том же хосте; производитель — OH3-36 (строка ему); (б) только
  учётные данные трекера. **Рекомендую (а).**
- **F8 Кто создаёт таблицу видов источников.** (а) XT1-3 создаёт `references/requirement-source-kinds.json`, OH3-36 переводит
  на неё `config_contract.py:420` (сегодня закрытый список в коде — нарушение AR-1); (б) ждать OH3-36. **Рекомендую (а)**:
  XT1-3 не ждёт слова владельца по OH3-35.
- **F9 Вопросы расхождений E3.** (а) показать одним пакетом в `finish`, ответы в пачке 1 не записывать (статус `open`;
  исполнитель «переписать кейс / баг» — пачка 3 E6); (б) записывать ответы сейчас через `person_words` без исполнителя (FR-9:
  решение без исполнителя). **Рекомендую (а)**.
- **F10 Кто пишет `R-n`.** (а) скаут E1 (как в предложении; на один диспатч меньше), тестер E3 пишет только матрицу;
  (б) тестер (как в стори, S2). **Рекомендую (а).**
- **F11 Где живёт результат.** (а) `explorations/<slug>/` — `carried` (как `artifacts/`), кэш попаданий —
  `state/features/<slug>/` `regenerated` machine-local (`qa-factory/state` игнорируется целиком, `install-paths.json:13-16`);
  (б) карта функции в `records/` (общая команде). Предложение называло `state/features/` «в проекте» — но `state/` не в git и
  при переустановке неизвестное там уходит в `retired/` (`install-paths.json:4-11`). **Рекомендую (а).**
- **F12 Вес инжекции режима.** Скаут-исследователь получает слайсы S1 (`artifact-contract-grounding.md`, `adapters-read.md`).
  (а) принять и измерить A25/токены в живом прогоне; (б) инжекция по режиму в `inject_context`. **Рекомендую (а)**, (б) —
  находкой по замеру.
- **F13 XT1-9 в пачке 1.** Цепочка OH3-35 (ждёт слова владельца) → OH3-36 → XT1-9. (а) перенести XT1-9 в пачку 2 сейчас, до
  взятия; (б) оставить — пачка не закроется до слова по OH3-35 (п. 9 правил кучек). **Рекомендую (а).**

## 7. Живое доказательство (FR-33): `qa-explore "Add to Cart"` на MyBooks против эталона

Где: стенд MyBooks (RUNBOOK §11), онбординг в корне тестового репозитория (копия — FR-53/P8: без записи в Jira, без MR).
Запуск: `/qa-factory:qa-explore "Add to Cart"`. Приёмка — каждая строка проверяется по артефактам `explorations/add-to-cart/`;
найденное меньше эталона — разбор, больше — в эталон после человека.

1. `requirement-hits.json`: источник Jira `XPANBFLFA` `status: searched`; среди `issues[]` — история XPANBFLFA-44 и все 23
   Test-кейса: XPANBFLFA-45, 141–148, 151–152, 156–167.
2. `requirements.yaml`: задачи №3–43 другого продукта, если найдены, — `not_relevant`; `test_cases[]` отмечает 158–167
   `has_steps: no`.
3. `feature-hits.json`: репозитории `MyBooks` и `test-automation-framework` (tests_root) `ready`, `hits_total > 0`; ни одной
   строки без статуса.
4. `feature-map.yaml` `entry_points`: кнопка страницы книги; кнопка карточки каталога (`add-to-cart-button-{id}`); «Move to
   cart» вишлиста (`wishlist-move-{bookId}`); `POST /api/cart`; слияние гостевой корзины при входе; поле количества на странице
   корзины.
5. `rules`: `mergedQuantity` (максимум, затем потолок остатком — `src/lib/cartRules.ts`), `fitsInStock`, предел 999
   (`src/lib/validation/schemas.ts`), отказ оформления «Insufficient stock»; `unit_tests` — `src/lib/cartRules.test.ts`,
   `src/lib/validation/schemas.test.ts`.
6. `tests_found`: спеки тестового репозитория с `runs_against: mock` для профилей `local/dev/qa` (ловушка HAR-моков, RUNBOOK §11).
7. `coverage-matrix.yaml` `discrepancies`: 164 (цена в корзине), 166 (сессия → гостевая корзина), 160 (быстрого просмотра нет —
   `code_says.absent`), 161 (максимум: остаток или 999) — каждое с цитатой кейса и вопросом.
8. `gaps`: карточка каталога, вишлист, правило слияния (156/157 — только сохранность), удалённая книга, последний экземпляр у
   двоих, остаток уменьшен после добавления, бейдж штук, пустое поле количества, ошибки API (45 размытый) — эталон AC-01…AC-15.
9. Ни одной записи в Jira/Confluence (журнал сессии: ни одного не-GET запроса к трекеру); `coverage-matrix.md` проходит
   `human_text.problems`.
10. Цена и трение: активность `explore` на дашборде; `code_friction` скаутов и тестера; A25 до/после (F12) — числа в отчёт.

## 8. Замеченные аналоги и противоречия (не расширяю скоуп — в отчёт Lead)

- `config_contract.py:420` держит виды источников закрытым списком в коде (AR-1) — F8.
- Находка OH3-36 п. 1 пишет статус `unresolved`, а `config_contract.py:422` допускает только `verified|unavailable|unknown` —
  запись онбординга по находке будет отказана формой конфига. Строка OH3-36.
- `role_permissions.phase_findings` обходит только `skills/qa-story/phases` (`role_permissions.py:110`) — A23 слеп к другим
  скиллам; правится в XT1-8 п. 5.
- `README.md` «Entry points» (`:25-29`) не называет `qa-collect` — интегратору вместе с `qa-explore`.
- `exit_gate._identity` судит остановку роли со стадией по стори, у которой идёт эта стадия (`:219-221`), — для любой
  нестори-диспатчи той же роли (например, диагностика доктора идёт отдельной веткой `stage_guard.py:1057`); XT1-2 закрывает для
  исследования, класс шире — проверить, нет ли других нестори-диспатчей.
- `implementation_repos[].role` уже есть в шаблоне (`templates/config.json:28-29`) и читается `project_inventory.py:53`; XT1-9
  может взять поле `role` у `code_repos` с тем же смыслом (одна форма), не новый ключ.

## 9. Маленькие решения, закрытые мной (без веса замысла)

- Лимиты — в `references/exploration.json`, не ключи конфига (не факт проекта; шаблон конфига — файл интегратора).
- Варианты написания слова (camel/kebab/snake/слитно) — в коде: универсальная трансформация, не разнообразие проектов.
- JQL для `api_version 3` — `/search/jql` с `nextPageToken`, для остальных — `/search` со `startAt`.
- Повторный вызов с той же фразой — продолжение того же корня; перед повтором E2 код копирует прошлую карту в
  `work/previous/feature-map.yaml` для `changed_since`.
- Текст пакета E0 и вопросов — английский (пакет, FR-30); тест — `human_text.problems`.
- Номера `XT1-n` переназначены (§0); в карточке кучки строки узлов меняет Lead при принятии.

## 10. Нужно сверх манифеста (прочитано помимо «given»)

Код пакета для установки реестров и краёв: `stage_guard.py`, `inject_context.py`, `exit_gate.py`, `host_dispatch.py`,
`guard_pre_tool.py`, `project_inventory.py`, `test_files.py`, `audit_factory.py`, `selftest.py`, `role_permissions.py`,
`activity_capture.py`, `install-paths.json`, `inject-map.json`, `artifact-writers.json`, `artifact-registry.json`,
`ahead-cards.json`, `role-commands.json`, `null-outcomes.json`, `question-prices.json`, `field-producers.json`,
`skills/qa-collect/SKILL.md`, `test_collect_skill.py`.

## 11. Трейл (что прочитано, строки)

- `plans/exploratory-charters-proposal.md:1-165`; `plans/piles/exploratory/README.md:1-67`;
  `plans/piles/exploratory/batch-1-sources-and-feature-map.md:1-51`.
- `plans/piles/onboarding-hooks/findings/20261031-istochniki-trebovanij-bez-proizvoditelya-i-chitatelya.md:1-52`;
  `plans/piles/onboarding-hooks/batch-3-common-layer-and-readers.md:1-30, 60-71` (строки OH3-35 `:66`, OH3-36 `:67`).
- `experiments/mybooks/add-to-cart-cases.md:1-245`; `docs/RUNBOOK.md:816-856`.
- `ai-packages/qa-factory/design/architecture.md:40-263`; `plans/builder-rules.md` (заголовки пп. 1–20, п. 1, 5, 6, 9, 19).
- `references/templates/config.json:1-161`; `references/config-keys.json:80-99`; `scripts/config_contract.py:395-439`.
- `scripts/source_inventory.py:335-464, 560-609, 964-993`; grep `class JiraClient|/issue/|...` (`:335, 575, 591, 677, 994`);
  grep `client_from_config` (`:3453`).
- `references/adapter-forms.json:1-28`; `scripts/ticket_adapter.py` (grep argparse `:183, 2031-2116`).
- `skills/qa-collect/SKILL.md:1-50`; grep `qa-collect` и `qa-doctor` по пакету (без тестов и CHANGELOG);
  `.claude-plugin/plugin.json:1-17`; `README.md:20-35`.
- `scripts/activity_capture.py` (grep `:15-17, 76`); `scripts/dashboard_cost_groups.py` (grep); `factory_dashboard.py:2062`;
  `scripts/tests/test_collect_skill.py:1-40` и grep `:154-175`.
- `scripts/audit_factory.py:100-209, 680-739` и grep A22 (`:1167-1175`); `scripts/selftest.py:315-344`.
- `scripts/role_permissions.py:1-140`.
- `references/inject-map.json:1-80`; `references/stages.json:300-327` и grep ролей; `references/ahead-cards.json:1-25`;
  `references/artifact-registry.json:1-60`; `references/artifact-writers.json:1-40`; `references/field-producers.json:1-25`;
  `references/null-outcomes.json:1-30`; `references/question-prices.json:1-25`; `references/role-commands.json:1-30`;
  `references/install-paths.json:1-45`.
- `scripts/guard_pre_tool.py:597-711, 930-1010, 1368-1447` и список функций.
- `scripts/inject_context.py:327-486`; `scripts/stage_guard.py:40-59, 298-407, 1054-1103`;
  `scripts/exit_gate.py:170-248, 1110-1131`; `scripts/host_dispatch.py:139-250`.
- `scripts/project_inventory.py:1-125`; `scripts/test_files.py` (список функций `:91-314`); `scripts/hooklib.py` (grep
  `project_root, state_dir, artifact_root, load_ref_json, read_json, sorted_paths, load_config, walk`).
- `agents/qa-requirements-tester.md:1-60`; `agents/qa-scout.md` (заголовки).
- Отрицательные утверждения с контролем той же формы: `which("rg")` по `scripts/` (без тестов) пуст — тот же Grep с `-i` нашёл
  `"rg"` в `stage_guard.py:1518`; `code_repos` в `p1-discovery.md` не найдено — тот же Grep с `code_repos|repositor` по
  каталогу фаз нашёл `p4-generate.md:86, 312-326`, `p2-interview.md:65-87` (`code_repos` фаза 1 не называет: его пишет p4).
