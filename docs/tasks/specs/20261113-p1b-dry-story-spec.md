# П1-б. Сухая стори: весь цикл драйвера на заглушках ролей, формы передач включены, обход каждого выхода — ЧЕРНОВИК СПЕКИ

Статус: черновик дизайнера (Opus) по брифу Lead 13.11.2026 (слово владельца на план 13.11.2026: «Да, дизайнеру»);
**фикс-раунд по вердикту критика на план t-401** (13.11.2026, решения Lead — план §10). Что изменено и где — §12
«Фикс-раунд t-401», по строке на находку. До приёмки Lead — не спека для диспатча. Развилки — §9 (новые — F10–F13),
вопросы владельцу — §9.2; ни одна не закрыта молча. Мелкие технические решения — §10. След чтения — §11.

Деревья: `RM` = `C:\QAFactory\forge-repo\.claude\worktrees\read-main\ai-packages\qa-factory` (origin/main, пакет);
`FND` = `C:\QAFactory\forge-repo\.claude\worktrees\findings-1413\plans\piles\live-run-fvf\findings`. Пути `RM/...` ниже
относительно корня пакета; строки прочитаны в RM 13.11.2026 (первый проход и фикс-раунд).

Шапка спеки (R11-f; по узлам — свои шапки в §6):

given: C:\QAFactory\forge-repo\docs\tasks\specs\20261113-plan-fabrika-ne-huzhe-agenta.md (§2 причины B, C, D, E; §3 П1-б; §4 К2, К3; §10 решения Lead по t-401); C:\QAFactory\forge-repo\docs\tasks\specs\reviews\t-401-p1-layers-plan-review.md; C:\QAFactory\forge-repo\docs\tasks\specs\reports\t-356-fvf-net-why-digest.md; C:\QAFactory\forge-repo\docs\tasks\specs\reports\t-357-fvf-time-split.md; C:\QAFactory\forge-repo\docs\TESTING.md; C:\QAFactory\forge-repo\plans\builder-rules.md; C:\QAFactory\forge-repo\ai-packages\qa-factory\design\factory-rules.md; C:\QAFactory\forge-repo\ai-packages\qa-factory\design\architecture.md; спека П1-а C:\QAFactory\forge-repo\docs\tasks\specs\20261113-p1a-writer-reader-round-spec.md (помощник `known_red.py` и `fill_artifact` с `overrides` — её узлы); спека П1-в C:\QAFactory\forge-repo\docs\tasks\specs\20261113-p1v-run-scoreboard-spec.md (`run_counters.counters`)
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\dry_exits.py
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\dry_stub.py
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\dry_world.py
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\dry_driver.py
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\driver-exits\
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\stories\dry-1\
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_scenario_dry_1.py
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_conductor_doors.py
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\scenario_walk.py
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test-layers.json
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\selftest.py
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\slow_tests.json
C:\QAFactory\forge-repo\.github\workflows\canon.yml
non-goals: писать код в этой спеке; менять поведение драйвера, контроллера, гейтов (каждая починка FV1 идёт своим узлом после своей красной строки); живые прогоны; дымовой прогон на модели (П2-г); дизайн заполнителя форм и помощника `known_red.py` (П1-а) и табло (П1-в); писать `docs/SIBLING_MAP.md`, `design/architecture.md`, `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md`, `docs/tasks/critic-diff-brief.md` (узел Lead «носители П1», §6 N-L); решать развилки §9
handoff: C:\QAFactory\forge-repo\docs\tasks\specs\20261113-p1b-dry-story-spec.md
edges: §5 (E1–E22)
DoD: по узлам §6; общий свидетель — `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <owns узла>`; что из названного им гоняется локально, а что только CI — §6 «Свидетель»; канон — CI
siblings: оси 5, 17, 18, 32, 34 SIBLING_MAP (полный перечень — §7); строки осей пишет узел Lead «носители П1» (§6 N-L)
designer: этот файл (черновик после фикс-раунда t-401; путь принятой версии назовёт Lead)

---

## 1. Инварианты AR-n, владельцы проверок, классы переписи суждений

Сверено с `RM/design/architecture.md` (не с памятью плана). План §6 называет AR-22, AR-24, AR-25, AR-12, AR-29;
бриф — AR-17, AR-24, AR-25, AR-28, AR-29. Слой ничего не меняет в коде пакета вне `scripts/tests/` (кроме строки
`TEST_TIMEOUTS` в `scripts/selftest.py` и строки `scripts/slow_tests.json` — данные расписания тестов, §6 N3), поэтому
«держит» здесь значит «становится детектором инварианта, не меняя его носителей».

| AR | Что слой делает с ним | Как держится | Проверка изменения (в DoD узлов) |
|---|---|---|---|
| AR-17 (одна дверь к дирижёру, `architecture.md:189-194`) | Слой утверждает: каждое состояние без хода доходит до вопроса через `Driver.no_move`; заглушка стоит на ГРАНИЦЕ ПРОЦЕССА (`STORY_RUN_CLAUDE`), не на `no_move`/`_ask_conductor` | шов не трогается; ни один метод `Driver` не подменяется (§4); обёртка `dry_driver.py` (если F10 (а)) только записывает ключ цен проходящим вызовом `no_move.priced_options` и зовёт настоящий | N3/N4 DoD: в коде узла нет присваивания атрибута объекту `Driver` и нет in-process `Driver` на пути под тестом — грep по owns с положительным контролем (`driver.stage_review_exhausted =` находится в `RM/scripts/tests/test_stage_critic_route.py:279`) |
| AR-24 (слова человека доходят целиком, `:247-252`) | Строки «длинные слова / слова после жетона / свободные слова» проверяют, что слова дошли до исполнителя (бриф роли, файл слов, вызов дирижёра) | только чтение носителей (`state/words/`, бриф, журнал заглушки) | N4 DoD: строки E9 (величина, кодировка, пустое) зелёные или помечены `known_red` с id находки |
| AR-25 (у каждого возвращённого состояния ход, `:254-259`) | Ядро обхода выходов: предложенный вариант исполним, после исполнения состояние другое | перепись выходов сверяется с кодом в обе стороны (§3) | N1 DoD: перепись маршрутов/стыков против скана кода — 0 расхождений; N4c DoD: перепись ключей вопросов `test_conductor_doors.py` зелёная со строками сухой стори в `driven` |
| AR-28 (неизвестное не проходит границу, `:275-280`) | Инвариант I-gate: гейт не показывается человеку, пока собственная репетиция гейта говорит «нельзя» по пунктам фабрики (FV1-7); нечитаемый носитель в слое — красное, не пропуск; `known_red` — по id СТРОКИ обхода, не по виду (t-401 №8): красная строка без своей метки никогда не «ожидаема» | слой сам следует AR-28: нечитаемый `question-prices.json`/журнал → красная строка с именем файла (E7) | N3 DoD: строка E7 с испорченной КОПИЕЙ носителя краснеет; N1 DoD: соседний вариант того же ключа без метки краснеет, хотя у ключа есть помеченная строка |
| AR-29 (код судит данные, `:134-157`) | Все проверки слоя — форма/стыки/наличие состояний; заглушка роли не имитирует суждение роли, заглушка дирижёра не выбирает по смыслу | исход строки (какой вердикт пишет заглушка критика, какой вариант берёт дирижёр, какое поле роль «чинит» на следующем раунде) задан СТРОКОЙ обхода, а не вычислен; команды автоматора — из профиля и строки таблицы раннеров, не из брифа (t-401 №12) | N2 DoD: в `dry_stub.py` нет ветвления по тексту брифа/формы, кроме чтения закрытых меток (`Dispatch:`, `Artifacts dir:`, `## Moves open here`); грep `brief` по веткам команд автоматора пуст |
| AR-16 (одна форма вопроса, варианты в `question-prices.json`, `:182-187`) | Варианты берутся из `RM/references/question-prices.json`; «свободный ответ идёт дирижёру» (текст AR-16) — проверяемое ожидание строк FV1-3 | только чтение | N4 DoD: строка «свободные слова» на каждом ключе, у которого есть строка цен с `person: "answer"` |
| AR-21 (передача несёт всё, `:226-231`) | Формы передач ВКЛЮЧЕНЫ (`handoffs.required` не трогается; в `story_run_common.py:201` его выключают) | мир строится без `cfg["handoffs"] = {"required": False}` | N3 DoD: грep `"required": False` по owns пуст (положительный контроль — `RM/scripts/tests/story_run_common.py:201`) |
| AR-20 (храповики только убывают, `:210-222`) | Храповики слоя: число строк `reach: live_only`, `after: <находка>`, `unwalked` и `hook_layer` — только убывают; `known_red` — общий храповик помощника П1-а (`raised_by`) | счёт — сумма по файлам групп `fixtures/driver-exits/<group>.json` против базы в тех же файлах; рост — строкой `raised_by` | N1 DoD: тест отказывает, если число выросло без строки `raised_by`. Строка оси 18 и вопроса 9 критика — тем же коммитом, что храповик (t-401 №23): требование к узлу Lead N-L, который сажается ВМЕСТЕ с N1 |
| AR-22 (поле читается — у него писатель, `:233-238`) | Перепись — стык в обе стороны: место вопроса в коде ↔ строка цен (существующая перепись) ↔ строка обхода; маршрут/стык ↔ строка `driver-exits` | см. AR-25 | см. AR-25 |
| AR-15 (общая задача — один выживший, `architecture.md` раздел C) — **добавлен в фикс-раунде (t-401 №7)** | Перепись ключей вопросов НЕ дублируется: выживший — `test_conductor_doors.py` (`QUESTION_SITE_RE :626`, `census_problems :668-679`); сухая стори становится частью его множества `driven`; `driver-exits` держит только то, чего та перепись не знает | один производитель множества ключей, которые гоняет сухая стори (`dry_exits.driven_keys()`), и один читатель-перепись | N4c DoD: в `driver-exits` нет поля `price_keys` и нет строк, ключуемых ключом цен (грep `price_keys` по `fixtures/driver-exits/` пуст; положительный контроль — `price_keys` находится в §3.2 этой спеки) |
| AR-13 (факт с функцией-читателем читается только через неё) — **добавлен (t-401 №25, №18)** | Готовность гейта читается полем `gate_ready` результата `gate_preflight.run` (`RM/scripts/gate_preflight.py:6063-6066`), не текстом «can start» (`:6080-6081`); круги переделок — `retro_numbers.dispatch_rounds` (`RM/scripts/retro_numbers.py:268-307`); счётчики табло — `run_counters.counters(task_root)` П1-в | только чтение через названные функции | N3 DoD: грep `can start` по owns пуст (положительный контроль — `RM/scripts/gate_preflight.py:6081`) |
| AR-12 (трение меряется, `:127-132`) | Только точка подключения счётчиков табло П1-в (§3.5), без дизайна табло | — | — |

Не тронуты (одна строка на каждый, по `architecture.md` «How a change walks», п. 2): AR-1…AR-11, AR-14, AR-18,
AR-19, AR-23, AR-26, AR-27 — слой не добавляет ни таблицы в код пакета, ни нового писателя артефакта; закрытое
разнообразие самого слоя (классы отказов §3.6, группы, правила по умолчанию) — строки его данных `fixtures/driver-exits/`,
не списки в коде (AR-1 соблюдается и внутри тестового слоя).

Замечено расхождение носителя (не чинится здесь; подтверждено критиком t-401 №28): `architecture.md:192` пишет
«`NO_MOVE_BASELINE_MAX = 102`, :1582», а в коде `RM/scripts/audit_factory.py:1715` — `NO_MOVE_BASELINE_MAX = 55`.
Правка — требование к узлу Lead N-L (§6), не этой спеки.

### Проверки слоя: владелец и класс

Все проверки живут в `scripts/tests/`, а перепись суждений (`test_judgment_census.py`, AR-29 «every check unit of every
`scripts/*.py` outside `scripts/tests/`», `architecture.md:146`) тесты не считает. Класс ниже — по словарю AR-29 для
ясности критику (вопрос 11), строка переписи `judgment-census.json` не меняется.

| # | Проверка | Владелец (P27) | Класс (AR-29) |
|---|---|---|---|
| C1 | Перепись маршрутов `KNOWN_REFUSALS` и стыков `stage-joints.json` = скан кода, в обе стороны; ключи вопросов — существующая перепись `test_conductor_doors.py` со строками сухой стори в `driven` (t-401 №7) | данные (код) | xref |
| C2 | У каждого предложенного варианта есть исполнитель | данные | xref |
| C3 | После исполнения варианта отпечаток состояния другой (отпечаток несёт круги и хэши форм, t-401 №11) | данные | shape |
| C4г | ГЕЙТ (t-401 №9, решение Lead): слово человека проводит отказ гейта, и проход записан строкой `state/passed-by-person.jsonl` (`RM/scripts/controller.py:2402-2413`) | замысел (владелец, P13 и FR-4 «A person's word passes any block», `design/factory-rules.md:53`); код проверяет только наличие прохода и записи | presence |
| C4з | ЗАПРЕТ слоя хуков (`refusal_registry`, файлы `SCANNED`): у отказа, который слово не проходит (`override: ""`), названа дверь (FR-57) — проверка ДАННЫХ реестра, хуки в сухой стори не исполняются (F11) | данные (наличие поля двери); годится ли дверь — суждение критика | presence |
| C5 | Тот же вопрос (или вызов дирижёра) в третий раз, когда между вторым и третьим не изменились ни вход автора, ни его выход — красное | данные | xref |
| C6 | I-gate: гейт не показан, пока своя репетиция гейта даёт `gate_ready: false` | данные | xref |
| C7 | Слова человека целиком у исполнителя | данные (защита слов человека — класс `safety` по AR-29, не суждение) | presence |
| C8 | Строка с ожиданием из слова владельца (FV1-2) | замысел (владелец; носитель — цитата в строке обхода) | presence |
| C9 | FV1-6 (t-401 №11): среди предложенных вариантов вопроса `stage_review_exhausted` есть ход, исполнитель которого — роль-автор стадии | данные (поля предложенных вариантов) | xref |
| C10 | FV1-19 дефект 2 (t-401 №6, решение Lead): что одна проверка приняла по полю `obligation_refs`, финиш окна того же поля не отвергает | данные (два читателя одного поля) | xref |

Суждение (годится ли кейс, баг ли красный, хорош ли реестр, годится ли текст двери запрета) слой не проверяет НИГДЕ:
оно остаётся П2-г, критику и живому прогону.

---

## 2. Место слоя среди трёх слоёв `docs/TESTING.md`

**Факты.** TESTING.md:43-53 — ровно три слоя: (1) сценарии на артефактах настоящих прогонов, (2) стыки данных,
(3) таблица случаев; новый случай — строка (`:55-58`); новый тестовый файл не создаётся (`:117`), кроме теста истории
`test_scenario_<id>.py` (`:77-79`: «тест истории `test_scenario_<id>.py`. Новый случай — строка `variants.json`»); новый
файл укладывается в 10 с, драйвер — «мир ОДИН раз на файл» (`:124-125`); части разрезанного — до 60 с в каноне (`:122-123`).
Обходчик сценариев знает пять дверей и не запускает цикл драйвера (`RM/scripts/tests/scenario_walk.py:40`
`DOORS = ("exit_gate", "joint", "start", "gate", "delivery")`). Спека карантина сама называет, что сценарии не ловят:
«потерю поля в коде между стадиями, состояние без хода» (`docs/tasks/specs/td-15-scenarios-quarantine.md:715-716`) и
что в день перевода перестаёт ловиться «цикл драйвера вне S6» (`:709`).

**Место.** Сухая стори — СЛОЙ 1 по форме (история в `fixtures/stories/dry-1/`, тест истории `test_scenario_dry_1.py`,
новый случай — строка), с новой, шестой дверью обходчика `driver` (весь процесс `story_run.py`). Отличие от слоя 1 по
источнику: история синтетическая и собрана кодом из сегодняшних форм, а не записана с прогона. Это меняет текст
TESTING.md:45-47 — развилка **F2** (§9), рекомендация: одна фраза в слой 1. Новый случай — строка
`stories/dry-1/exits/<group>.json` (не новый тест-файл: TESTING.md:117 соблюдён). Ключ `story_coverage_required`
(`RM/scripts/tests/test-layers.json:13-26`, S1…S9, `gateA.words`, `gateB.words`, `red_then`) — сухая стори его НЕ
закрывает за записанные истории (она синтетическая); строка `keep` не заявляет `story_coverage` (E21).

**Что переиспользуется.**
- `scenario_walk.py`: загрузчик истории, `_new_project`, `_pinned`, `--witness-for` (`DOOR_MODULES`, `:46-47`; новой двери
  нужна строка `"driver": ["story_run"]`, чтобы правка любого `driver_*.py` называла сухую стори свидетелем; критик
  t-401 замерил: замыкание `story_run` — 227 из 279 скриптов против 201 у двери `gate`).
- `story_run_common.py` — ТОЛЬКО импортом, без правки (её пишет PC4-12): `RECEIPT` (`:32-52`, квитанция хоста),
  образ `s0_project` (`:405-426`, файловый адаптер тикета), `d2_alive_server` (`:480-496`, стенд «жив»).
- Носители драйвера, которые уже пишет настоящий драйвер: `state/driver-questions.jsonl` (`RM/scripts/driver_dialog.py:410-419`),
  `state/driver-answers.jsonl` с `question_sha` (`:381-392`), `state/driver-state.json` `asked` с `offered`/`options`
  (`:319-333`), `driver-runs.jsonl`.
- **Существующая перепись ключей вопросов** (t-401 №7): `RM/scripts/tests/test_conductor_doors.py` — `QUESTION_SITE_RE`
  (`:626`, литералы `closed_question("<ключ>"`/`priced_section("<ключ>"`), `AWAITING_ITS_SITE` (`:634`),
  `PINNED_ELSEWHERE` (`:636-665`), `census_problems(raised, data_keys, driven, awaiting, pinned)` (`:668-679`); `driven` =
  ключи, которые этот тест гоняет шпионом `NM.priced_options` (`:723-729`, `:802`). Файл в `keep`, слой `register`
  (`test-layers.json:661`), 53.0 с (`RM/scripts/slow_tests.json:20`), в `keep_fail_at_entry` когорты (`test-layers.json:6994`).

**Что заменяется (не удаляется).**
- `story_run_common.STUB` (`:54-181`) с ответами из рукописных `control` и выключенными формами — для сухой стори
  заменён `dry_stub.py` (роли пишут из форм через заполнитель П1-а). Старые файлы на `STUB` остаются как есть.
- 16 файлов `test_story_run_*` в карантине (`RM/scripts/tests/test-layers.json` раздел `quarantine` с `:7022`: codex,
  delivery, delivery_b, delivery_c, exit_limit, gate_repair, loop, repair_limit, s0_stand_trace, s5_n1_frozen,
  s5_parallel, s7_live, stand, stand_b, stand_c, wait) — сухая стори берёт их КЛАСС (цикл драйвера, выходы). Их удаление
  — только `purge` по слову владельца (PC4-18); «переносом улова» здесь будет строка обхода на ключ/маршрут, который файл
  держал. Показатель (критик t-401 №7): `PINNED_ELSEWHERE` указывает на карантинные файлы (`exit.resume_limit` →
  `test_story_run_exit_limit.py`, `:644`; `s5.repair_limit` → `test_story_run_repair_limit.py`, `:642`) — когда строка сухой
  стори гоняет ключ, запись `PINNED_ELSEWHERE` для него удаляется (её требует сама перепись: «listed as pinned elsewhere,
  but driven here», `:677`), §3.2.
  20 файлов `test_story_run_*` в `keep` (`:5426-6662`) не трогаются.
- Аудит A27 (`RM/scripts/audit_factory.py:1641-1715`, считает МЕСТА, причина E) остаётся; перепись выходов — его двойник
  по СОСТОЯНИЯМ. Слияние — не здесь.

**Конфликт с закреплённым поведением (причина B).** Строки FV1-3 и FV1-4 краснеют против тестов, закрепивших дефект:
`RM/scripts/tests/test_story_run_s0.py:1140` («no question answered by a token» как ожидаемое; файл в `keep`) и
`RM/scripts/tests/test_brief_pack.py:2428-2440` (срезка до `DECISION_CHARS_MIN`; `keep`). Строки C4г краснеют против
`RM/scripts/tests/test_row_fields.py:366-374` (запись слова `*`, `row-fields`, `row-fields-missing`, `manifest` «does not lift
the finding»; файл в карантине по плану §7). Слой их не правит; узел починки переписывает или удаляет их тем же коммитом
(TESTING.md:130-131).

---

## 3. Реестр видов отказов, видов вопросов и закрытых вариантов

### 3.1 Что есть в коде сегодня (замеры; команда — инструмент Grep по RM, вывод в §11)

| Множество | Где живёт | Перечисляемо сегодня? | Замер |
|---|---|---|---|
| Виды вопросов, литералом | `Person("<kind>", ...)` в наборе драйвера (`story_run.py`, `driver_*.py`); класс `RM/scripts/driver_core.py:192-233` | частично: AST-скан литералов | **25 разных видов в 36 местах** (Grep `Person\(\s*"[A-Za-z_0-9]+"`, `-o`, glob `{story_run,driver_*}.py`): conductor, halt, ticket_changed, ticket_auth, first_look_dead, package, open_work, report_match, delivery_check, delivery, retro, stand_identity, s1_gap, s1_review, questions, repair_limit, walk_supply, data_change, walk_account, exit_limit, arrival_not_waiting, first_look_same_code, absent_side, closed_held, code_close |
| Виды вопросов, переменной | `Person(kind, ...)` | НЕТ: вид приходит значением | **5 мест** (Grep `Person\(\s*[a-z_]...`): `driver_conductor.py:205`, `driver_s0.py:738`, `driver_runner.py:1220`, `driver_machine.py:469`, `driver_machine.py:1482`; через них идут виды прогона LR2-1 `gate_A`, `environment`, `refusal`, `stand_login`, `gate_a_dry` (t-357 табл. 1/4b) |
| Ветви ответа | `Driver.take_answer`, `RM/scripts/driver_machine.py:3314` и далее (`kind == "repair_limit"` :3382, `exit_limit` :3403, `code_close` :3410, … `report_match/delivery_check/delivery` :3472) | да: AST сравнений `kind` в одном методе | не сосчитано целиком (чтение остановлено на :3473); пересчёт — первый шаг N1 |
| Закрытые варианты | `RM/references/question-prices.json`, один загрузчик `no_move.load_question_prices` (`RM/scripts/no_move.py:589-609`) | да | **61 ключ, 188 строк `"answer":`** (Grep count; подтверждено критиком прогоном) |
| **Место вопроса → ключ цен (исправлено, t-401 №7)** | литерал ключа в месте вопроса: `closed_question("<ключ>", …)` / `priced_section("<ключ>", …)` (`RM/scripts/driver_runner.py:1187,1205`; `RM/scripts/exploration.py:494`); перепись в обе стороны — `RM/scripts/tests/test_conductor_doors.py:626` (`QUESTION_SITE_RE`), `:668-679` (`census_problems`), `:799-805` (скан `scripts/*.py`) | **да, уже есть** | Grep `closed_question\("\|priced_section\("` по `RM/scripts`: 38 мест в пакете, напр. `driver_dispatch.py:3135` (`s5.repair_limit`), `:3127` (`s7.repair_limit`), `:3761-3762` (`exit.resume_limit_halted` / `exit.resume_limit`), `driver_conductor.py:783` (`gate_A`/`gate_B`). Прежний негатив черновика («соответствие не найдено») был промахом формы поиска (искали `Person(`, а ключ стоит в `closed_question(`) — снят |
| Ходы дирижёра | `RM/references/conductor-actions.json` `moves` (`:63-216`: `rework_stage`, `approve_gate`, `resume_with_words`, `release_and_restart`, `go_on_as_is`, `story_fact`, `stand_prepare`, `revoke_exclusion`, `person_does`, `stop_here`); предусловия `MOVE_FACTS` `RM/scripts/no_move.py:161-172` (10 ходов); жетоны кода `TOKEN_MOVES` `:40` (3) | да | 10 / 3 |
| Причины в шве | ключ `"why"` состояния `no_move({...})` | да: литералы | **8 значений** (Grep `"why": "[a-z_]+"`): refusal, threshold, cap, unread_answer, stage_review_exhausted, by_hand, stop, chosen |
| Маршруты отказов драйвера | `KNOWN_REFUSALS`, `RM/scripts/driver_dispatch.py:38-107` (имя, регулярка, ход) + «не совпало» → дирижёр; `gate_refusal` с `known = False` (`RM/scripts/driver_core.py:73-81`) | да (список в коде) | **21 строка** + 2 класса (несовпавший, `known=False`) |
| Источники отказа выходу роли | `RM/references/stage-joints.json` `joints[].check` | да | **43**: `exit:` 8, `detector:` 8, `window:` 27 (строки :9…:1117) |
| Отказы на пути диспатча (хуки) и операции | `RM/scripts/refusal_registry.py` `REGISTRY` (`:72`, A24) | да | **102 записи**: 77 построчных (файлы `SCANNED`, `:57-58`), из них 58 с `"override": ""`; 25 — `kind: operation` (все с непустым `override`). Подсчёт по классам — §3.6 |
| Отказ «слово не проходит» на гейте | один производитель — `RM/scripts/s5_precheck.py:4679` (`DV.refusal_line`), правило `_passable` `:3930-3933` | да | §3.6 |
| Действия контроллера | перепись `RM/scripts/tests/test_story_run_refusals.py:446-476` (регулярка по исходнику) | да | 16 (утверждение самого теста, `:472`) |
| Детектор «петли» | `RM/references/collect-loops.json` L1–L7 (читатель `collect_stall.load_loops`) | да | 7 записей; читает тот же `driver-questions.jsonl` (L7) |
| Писатель каждого выхода стадии | `RM/references/artifact-writers.json` (`:4-347`; «роль» против скрипта) | да | основа таблицы §4.2 |

### 3.2 Что вводится — один производитель, одна перепись на множество (переписано, t-401 №7, №13)

**Ключи вопросов — существующая перепись, не новая.** Строка обхода, у которой есть ключ цен, ключуется ЭТИМ ключом
(вид `Person` в id строки не участвует). Множество ключей, которые гоняет сухая стори, производит одна функция
`dry_exits.driven_keys() -> set[str]`: ключи строк обхода (`stories/dry-1/exits/*.json`) с `reach` ∈ {`story`, `seed`}
(исполняемых; исход PASS или `known_red` — оба «гоняются»), у которых каждая строка цен ключа (каждый `answer`) покрыта
своей строкой обхода (иначе ключ не `driven`: «гоняет часть ответов» не считается). Читатели производителя:
`test_scenario_dry_1.py` (исполняет строки) и `test_conductor_doors.py` (перепись). Изменение переписи (узел N4c, ОДИН
коммит вместе с вычисткой `PINNED_ELSEWHERE`):

```
# test_conductor_doors.py, the_question_prices_are_data(), строка :802 (сегодня):
#   census = lambda raised, data_keys: census_problems(raised, data_keys, set(offered), AWAITING_ITS_SITE, set(PINNED_ELSEWHERE))
# после N4c:
#   import dry_exits
#   driven = set(offered) | dry_exits.driven_keys()
#   census = lambda raised, data_keys: census_problems(raised, data_keys, driven, AWAITING_ITS_SITE, set(PINNED_ELSEWHERE))
# + из PINNED_ELSEWHERE удаляются ключи, вошедшие в driven (иначе :677 «listed as pinned elsewhere, but driven here»)
# + строка keep test_conductor_doors.py: covers += "tests/dry_exits.py", "scripts/tests/fixtures/stories/dry-1"
```

Сравнение «ответы, которые код предлагает на ключе, = строки данных» (`:794-796`, K15) для ключей сухой стори делает сама
сухая стори: на вопросе с ключом k множество предложенных ответов (записанное по F10) равно множеству `answer` строк k
(`question-prices.json`), иначе красное с ключом и разницей — та же проверка K15, исполненная в процессе драйвера.
`census_problems` не меняет сигнатуры и смысла; меняется только аргумент `driven`. Отрицательный контроль N4c: копия
`exits/<group>.json` без строки одного ответа ключа k → `driven_keys()` без k → перепись краснеет «raised, but neither driven
here nor pinned elsewhere: k» (на копии, правило 7 гигиены).

**`fixtures/driver-exits/` держит только то, чего перепись ключей не знает** — файл на группу (t-401 №13), читатель
`dry_exits.load()` склеивает их; одинаковый id в двух файлах — красное с обоими путями:

```
fixtures/driver-exits/<group>.json:
{"schema": 1, "group": "<group>",
 "routes": {"<KNOWN_REFUSALS name>|unmatched|known_false": {"reach": ..., "seed": ..., "why_unreached": ..., "class_source": "<id>"}},
 "joints": {"<stage-joints check>": {"reach": ..., "seed": ..., "why_unreached": ...}},
 "kinds_without_key": {"<Person kind>": {"raised_at": ["<module>:<function>"], "reach": ..., "seed": ..., "why_unreached": ...}},
 "ratchet": {"live_only": <n>, "after": <n>, "unwalked": <n>, "hook_layer": <n>, "raised_by": []}}
fixtures/driver-exits/classes.json  (§3.6: правило класса по источнику отказа, данные)
reach ∈ story | seed | live_only | after:<id находки> | unwalked | hook_layer
```

Поля `price_keys` и `known_red` в `driver-exits` НЕТ: ключ цен — существующая перепись; метка «ожидаемо красная» — реестр
общего помощника `scripts/tests/known_red.py` (владелец — П1-а, решение Lead №3/№8; П1-б только импортирует), строка
реестра = id строки обхода `(<ключ цен | маршрут | стык | вид без ключа>, <вариант>)` → `FV1-n | id узла`, рост — с
`raised_by`, позеленевшая без снятия — красная.

`kinds_without_key` — виды `Person`, чьё место поднимает вопрос без `closed_question`/`priced_section` (сегодня, по табл.
§3.1: `conductor`, `refusal`, `environment`, `retro`, `stand_identity` и др. — точный список первым шагом N1: вид из скана
§3.1, ни одно место которого не стоит рядом с литералом ключа; правило «рядом» — тот же вызов `Person(kind, self.closed_question(...))`
или `site_seam_person(kind, self.closed_question(...))` по AST). Для них строка обхода ключуется видом.

Сверка в обе стороны (C1), красное с дверью «добавь строку в `fixtures/driver-exits/<group>.json` с `seed` или
`live_only` и причиной» при:
- маршрут `KNOWN_REFUSALS`, check `stage-joints.json` или вид без ключа из скана без строки — **новый вид без случая
  падает, а не проходит молча** (E5);
- строка `driver-exits`, которой нет в скане — «устаревшая строка»;
- строка обхода с ключом цен, которого нет в `question-prices.json` — красное с ключом;
- рост `ratchet` любого счёта без `raised_by`.

Ключ цен без строки обхода — не красное этого слоя: его ловит существующая перепись («raised, but neither driven here nor
pinned elsewhere») — одна дорога.

Читатели меняются тем же коммитом (правило 10): читатель `driver-exits` один — `dry_exits.py`; `test_scenario_dry_1.py`,
обходчик и `test_conductor_doors.py` зовут только его. Код пакета перепись не читает (F3 (а), решение Lead).

### 3.3 Строка обхода

Строка = (ключ цен, вариант) для вопроса с ключом; (маршрут, вариант) / (стык, вариант) / (вид без ключа, вариант) иначе.
Id строки — эта пара строкой `"<ключ|маршрут|стык|вид>/<вариант>"`; это и есть id в реестре `known_red` (t-401 №8).
Варианты: каждый `answer` строк цен ключа + «свободные слова» + «пустой ответ»; строки батареи E9 — ТОЛЬКО на ключах, у
которых есть строка цен с `"person": "answer"` (ответ несёт слова роли/дирижёру; напр. `halt.words`, `questions.answers`,
`gate_A.rework` — `RM/references/question-prices.json:126,130,150`) и на видах без ключа, чей вопрос несёт слова
(`conductor`, `refusal`) (t-401 №26, №37). Для маршрутов без вопроса (ход кода: `continue`, `recover`, `retry`, …) вариант один
— «ход кода». Строки `hook_layer` построчно НЕ обходятся: один счёт в храповике (t-401 №37), плюс проверка данных C4з.

Формат файла строк группы `stories/dry-1/exits/<group>.json` (грамматика задана здесь, критик t-401 «E»):

```
{"schema": 1, "group": "<group>",
 "rows": [{"id": "<ключ|маршрут|стык|вид>/<вариант>",
           "start": "<имя снимка мира §4.3: S0|S1|...|S9|after:<id находки>>",
           "seed": [<шаги, §4.3>],
           "answer": {"token": "<жетон>" | null, "words": "<слова>" | null, "words_file": "<путь в истории>" | null},
           "stub": {"verdicts": {"<stage>/<role>": "<вердикт>"}, "conductor": {"action": "...", "options": [...]},
                    "overrides": {"<форма или выход>": {"<поле>": "<значение>" | "ABSENT"}},
                    "repair_on_round": {"<stage>/<role>": {"<поле>": "<значение>"}}},
           "expect": {"checks": ["C2", "C3", ...], "owner_quote": {"text": "...", "carrier": "<путь:строка>"} | null},
           "reach": "story | seed | live_only | after:<id находки>",
           "why_unreached": "<причина>" | null}]}
```

`repair_on_round` — данные строки, а не суждение: «на раунде n+1 роль пишет это поле так» (проверяется, что дверь фабрики
работает, когда роль сделала правильное, — C2/C3). Строка без `repair_on_round` проверяет поведение фабрики, когда роль не
исправила (C5).

### 3.4 Отпечаток состояния (C3, C5) — переписано (t-401 №11)

`state_fingerprint(task_root)` в `dry_exits.py`: хэш от (статусы стадий и решения гейтов `pipeline.json`, записи
`acceptance`; статусы диспатчей контроллера с id, нормализованными правилом `DISPATCH_ID_RE`, `RM/scripts/driver_core.py:47,55-64`;
**номер круга каждого диспатча по (стадия, роль) — `retro_numbers.dispatch_rounds(task_root)` (`RM/scripts/retro_numbers.py:268-307`,
поле `round`)**; **хэши заполненных форм передач `work/handoffs/*.yaml` (писатель `handoff_init.py:421`), нормализованные
`DISPATCH_ID_RE`, ключ — (стадия, роль, круг)**; `asked.kind/stage` и число пропусков слова в `driver-state.json`; хэши
объявленных выходов стадии из `references/stages.json`). Без времени. Следствие: новый законный раунд переделки — НОВОЕ
состояние (C3 зелёная), даже когда детерминированная заглушка пишет те же байты.

«Тот же вопрос» (C5): «спрос» — строка `driver-questions.jsonl` ИЛИ вызов дирижёра в журнале заглушки
(`state/dry-stub.jsonl`, §4.4). Два спроса одинаковы, если совпали (ключ цен или вид, стадия, dispatch по `DISPATCH_ID_RE`,
множество предложенных жетонов). Красное, когда третий одинаковый спрос подряд пришёл, а между вторым и третьим НЕ
изменились (а) нормализованный хэш входа автора — подсказки, которую заглушка получила для нового раунда автора
(`prompt_sha` журнала заглушки, нормализация `DISPATCH_ID_RE`), и (б) нормализованный хэш его формы. Смысл: фабрика третий
раз задаёт тот же вопрос, ничего нового роли не дав. Это и есть петля FV1-13/FV1-22; законный раунд с новыми словами
критика меняет (а) и не краснеет.

**Направление ошибки переиспользованных функций в роли гейта** (`finding_lines`/`DISPATCH_ID_RE`, `question_body_sha`,
`retro_numbers.dispatch_rounds` были советчиками/идентичностью/отчётом, здесь решают красное CI):
- C5: допустимая ошибка — слить два почти одинаковых спроса в один (ложное красное: лишний разбор); запрещённая — считать
  один спрос двумя (пропуск петли FV1-13/FV1-22).
- C3 (обратное направление): допустимая ошибка — счесть два состояния разными (ложное зелёное C3 гасится C5 и C9 для
  известных петель); запрещённая — счесть законно новое состояние тем же (ложное красное без дефекта, которое нельзя
  снять починкой — ровно дефект №11). Поэтому круги и хэши форм входят в отпечаток C3, а в равенство C5 — только вход и
  выход автора.
- Неудобные входы, которые обязаны остаться на безопасной стороне (строки таблицы N1): id диспатча отличается только
  номером (`S5-qa-automator-4` / `-5`) → один спрос; метка `asked_at` в шапке → игнорируется; вопрос отличается только
  дописанным блоком FR-7 «You have answered this exact question before» (`RM/scripts/driver_dialog.py:302-314`) → один
  спрос; тот же жетон в другом регистре/в бэктиках → одно множество жетонов (нормализация драйвера `s0_normalize`);
  подсказка нового раунда отличается только id диспатча → тот же вход (C5); новый круг с той же формой → другое
  состояние (C3); `retro_numbers.dispatch_rounds` возвращает `[]` (нет `state/controller.json`) → круги не входят в
  отпечаток, и строка печатает NOTE «rounds unknown» (не PASS C3, E7).
- `no_move.open_moves` (`RM/scripts/no_move.py:175-187`) кормит заглушку дирижёра; его объявленная ошибка — «слишком мало
  ходов» (`:8-11`). В слое это значит: неоткрытый ход не обходится, и дыра «нет двери» может спрятаться. Поэтому C2
  дополняется: в состоянии отказа хотя бы один предложенный вариант, кроме `stop`, обязан сменить отпечаток (иначе
  красное «жив только `stop`» — третий экземпляр FV1-13), и C9 проверяет ДАННЫЕ предложенного (есть ли исполнитель-автор),
  а не только исход.

### 3.5 Точка подключения табло П1-в (без дизайна табло)

После главного прохода и после каждой строки обхода, ДО уборки мира: каталог `qa-factory/artifacts/<task>/state/` сухой
стори (`driver-runs.jsonl`, `driver-questions.jsonl`, `driver-answers.jsonl`, `driver-state.json`, журнал заглушки) — те же
носители, по которым t-357 мерил LR2-1. Обходчик зовёт **`run_counters.counters(task_root)`** (имя — решение Lead №18,
одно в обеих спеках) и печатает его строки; до появления функции — строка `scoreboard: not wired (П1-в)` (NOTE, не
PASS). Требование к функции: принимает корень задачи, ничего не пишет в мир, печатает счётчики «возвраты по гейту,
вопросы по виду, повтор вопроса» (строку «повтор вопроса» добавляет П1-в, решение Lead №18). Сухая стори кормит её:
строки `driver-runs.jsonl` с `session_id: stub-<dispatch>-<n>` (§4.4), процесс с `STORY_RUN_CLASS=dry` (§4.4).

### 3.6 Классы отказов для C4 (новое, t-401 №9) — данные, источник, замер

Класс строки — поле данных `fixtures/driver-exits/classes.json` (правило по источнику отказа, с умолчанием), не список в
коде:

```
{"schema": 1,
 "by_source": {"stage-joints": "gate",                 // RM/references/stage-joints.json joints[].check
               "refusal_registry:operation": "gate",   // REGISTRY, "kind": "operation"
               "refusal_registry:scanned": "ban",      // REGISTRY, "file" из SCANNED (refusal_registry.py:57-58)
               "question:gate_A": "gate", "question:gate_B": "gate"},
 "default": null}                                      // источник не назван → красное «class unknown» (FR-59), не догадка
```

Строка маршрута `KNOWN_REFUSALS` с ходом `ask_person` (`story_budget`, `executor`, `readiness`, `driver_dispatch.py:97-99`)
называет `class_source` — id источника своего текста (check стыка или id записи реестра); строка без него — красное
«class unknown».

**Замер по классам** (команда — Grep по `RM/scripts/refusal_registry.py`, `-n`: шаблоны `^    \{"id": "` → 102 строки;
`"kind": "operation"` → 25 строк (`:756`, `:812`…`:1034`); `"override": ""` → 58 строк, последняя `:805`; ни одна не
попадает в запись `kind: operation` — сверка номеров строк, вывод в §11):

| Класс | Источник (данные) | Число | Как проверяет слой |
|---|---|---|---|
| ЗАПРЕТ, слово не проходит | `REGISTRY`, файл из `SCANNED`, `"override": ""` | **58** | C4з: проверка данных — у записи непустое `unpassable_because` (дверь, FR-57); хуки не исполняются |
| ЗАПРЕТ, слово проходит | `REGISTRY`, файл из `SCANNED`, `override` непуст | **19** (77 − 58) | счёт `hook_layer` |
| ГЕЙТ, операция | `REGISTRY`, `kind: operation` (контроллер, `stage_done`, `exit_gate`, `waiver`, `planning_contract`…) | **25**, из них с `override: ""` — 0 | C4г в главном проходе/строках, где операция отказывает |
| ГЕЙТ, стык | `stage-joints.json` `joints[].check` | **43** (`exit:` 8, `detector:` 8, `window:` 27) | C4г |
| ГЕЙТ, вопрос гейта | `gate_A`, `gate_B` (`question-prices.json:149-160`) | 2 | C4г |
| ГЕЙТ, сегодня «слово не проходит у источника» | один производитель `s5_precheck.py:4679`; правило `_passable` (`:3930-3933`): семейства `CHECKS` (9, `:72`) вне `PASSABLE` (2, `:82`) = **7 семейств** (`manifest`, `bindings`, `oracle`, `run_mapping`, `smell`, `plan`, `sides`), кроме 3 тегов `WORD_PASSABLE_TAGS` (`:101`) и тега ожидания `then-remainder-unrecorded-*` (`:3945`); читатель класса — `exit_gate.word_class` (`RM/scripts/exit_gate.py:1785-1804`, `"refused"`) | 7 семейств | C4г ожидает проход → строки красные (`known_red` с находкой, R-L5 §6) — кроме вопросов владельцу §9.2 |

Положительный контроль «производитель один»: Grep `refusal_line\(` по `RM/scripts` → определение `detector_verdict.py:116`,
вызов только `s5_precheck.py:4679` (остальное — тесты).

**Проверки гейта, где проход словом противоречит записанному решению владельца** (решение Lead №9: каждая — вопрос
владельцу простыми словами, §9.2). Поиск: Grep `-i` `never by a waiver|no word (passes|opens|lifts)|does not lift|owner's word|владел`
по `exit_gate, s5_precheck, waiver, stage_done, controller, gate_preflight, planning_contract, window_record, contract,
detector_verdict .py` — попадания: `s5_precheck.py:93, :98, :3932`; `exit_gate.py:1788, :1791, :1817`; `contract.py:5355, :5701`;
`window_record.py:111, :875, :957`; `controller.py:3346` (положительный контроль — тот же вызов нашёл `s5_precheck.py:93`).
`DECISIONS.md` — 0 попаданий на `слово человека|word passes|override|waiver` (`-i`; контроль той же формы `D-00` → 23).
Разбор:
- `s5_precheck.py:90-94` `open-oracle-asserted`: «a person settles it only by answering the question … never by a waiver
  (FR-4, FR-58, FR-59)» — FR-58 = P20 (владелец 01.10): ожидание открыто до ответа, проход словом сделал бы код оракулом
  → **вопрос владельцу Q1**.
- Вердикт доставки `no` (`question-prices.json:302-303`: `s8.delivery.no` × `go on` → `"delivery": "no"`): слово проводит шаг,
  вердикт остаётся `no` (P21, владелец 02.10/03.10; FR-35) → ожидание C4г для гейтов с вердиктом — «шаг пройден, вердикт не
  изменён» → **вопрос владельцу Q2** (подтвердить прочтение).
- `exit_gate.py:1791` `unreadable` — «named_only» по слову владельца 27.10 F-5: слово проходит, но только названное — с P13
  не спорит (вопроса нет).
- `contract.py:5355`, `window_record.py:111, :875, :957` (слова владельца 05.11 о словах `probe gap:`/`probe not proved:`) —
  какое слово что проходит, а не запрет прохода (вопроса нет).
- Семейства `manifest`/`bindings`/`oracle`/`run_mapping`/`smell`/`plan`/`sides`: обоснование «a repair the author can make
  without asking anybody» (`s5_precheck.py:80-82`) — правило дизайна, не слово владельца; найденного решения владельца нет
  → по решению Lead №9 строки краснеют (`known_red` с находкой R-L5), вопроса нет.

---

## 4. Как драйвер ставится в состояние

### 4.1 Шов — граница процесса

Драйвер запускается настоящим процессом (`story_run.py --project <мир>`, как `story_run_common.run_driver`, `:333-334`;
при F10 (а) — через обёртку `dry_driver.py`, §4.4); подменяется только исполняемый `claude` через переменную
`STORY_RUN_CLAUDE` (механизм `RM/scripts/tests/story_run_common.py:6-7,235`). Это не лямбда шва под тестом (причина C):
ни один метод `Driver` не заменяется, `no_move`, `_ask_conductor`, `stage_review_exhausted`, `take_answer` идут настоящие;
заглушка отвечает так, как ответил бы хост (JSON `result`), и всё, что после, — код пакета. Каждый процесс, который
запускает обходчик (драйвер, операции рецептов), получает `STORY_RUN_CLASS=dry` в окружении (решение Lead №16; §4.4).

| Что | Настоящее | Заглушка |
|---|---|---|
| Цикл драйвера (`story_run.py`, все `driver_*.py`), шов `no_move`, `ask`, `take_answer` | да | — |
| Контроллер, `story_step.py`, `stage_done.py`, `exit_gate.py`, `handoff_init.py`/`handoff_check.py` (формы ОБЯЗАТЕЛЬНЫ) | да | — |
| `brief_pack.py`, `person_words`, `waiver.py`, `question_register.py`, `gate_preflight.py`, `gate_brief.py`, `s5_precheck.py`, `planning_contract.py`, `acceptance.py`, `check_delivery.py`, `manifest_put.py`, `finalize_task.py`, `ledger.py`, `context_bundle.py`, `case_versions.py` | да (код-писатели выходов по `artifact-writers.json`) | — |
| Адаптер тикета | да (файловый, как `s0_project`) | тикет — синтетический файл истории |
| Стенд | да, внутрипроцессный HTTP «жив» (`d2_alive_server`) | содержимое ответов |
| Запуск тестов автоматора | да: роль-заглушка вызывает команды **профиля** проекта мира (`profile_contract.profile_commands(profile)`, `RM/scripts/profile_contract.py:243-252`; ось 30) на крошечном проекте **строки таблицы раннеров** F5 (`stories/dry-1/runners/<row>/`); бриф НЕ разбирается (t-401 №12) | — |
| Роли (`claude -p --agent ...`) | — | `dry_stub.py`: пишет выходы, чей писатель — роль (`artifact-writers.json`), заполнителем П1-а по сегодняшним формам + наборы истории; выход, который заполнитель ещё не умеет, — строка `live_only` (решение Lead №4), не рукописный текст; вердикт, выбор и правки раунда — из строки обхода |
| Дирижёр (`claude -p` без агента) | — | `dry_stub.py`: детерминированно; действие и вариант — из строки; по умолчанию `ask_person` со ВСЕМИ открытыми предлагаемыми ходами из раздела `## Moves open here` подсказки (`RM/scripts/no_move.py:257-285`) с ценами из строк цен |
| Хуки хоста (`stage_guard`, `guard_pre_tool`, …) | — | не исполняются (хоста нет): класс `hook_layer`, один счёт + проверка данных C4з (E8) |

### 4.2 Выходы стадий, которые пишет заглушка (новое, t-401 №12; источник `RM/references/stages.json` `outputs`, писатель — `RM/references/artifact-writers.json`)

Колонка «П1-а» — вид заполнителя: сегодняшние виды `fill_artifact` (`case`, `plan_md_row`, `plan_json_row`, `manifest_row`,
`test_file:<lang>` — спека П1-а, строка `:166`) или форма передачи (`fill_form`); вид, который П1-а добавит по решению Lead №4
(перечень из `stages.json`), назван здесь как ТРЕБОВАНИЕ `stage_output:<путь>` — точное имя назначает спека П1-а; пока его
нет — `live_only`.

| Стадия | Выход (`stages.json`) | Писатель (`artifact-writers.json`) | Кто пишет в сухой стори | П1-а / иначе |
|---|---|---|---|---|
| S0 | `pipeline.json` (`:17`), `project:readiness.json` (`:18`) | `stage_done.py` (`:12-17`); `readiness.py` (`:332-334`) | код | — |
| S1 | `work/context-manifest.json` (`:47`) | роль `qa-scout` (`:19-24`) | заглушка | требование `stage_output:work/context-manifest.json`, иначе `live_only` |
| S1 | `work/context-bundle.json` (`:48`) | `context_bundle.py` (`:25-28`) | код (команда роли из профиля/данных, §4.3) | — |
| S1 | `work/impl-diff.txt` (`:49`) | роль `qa-scout` (`:33-36`) | заглушка | требование `stage_output:work/impl-diff.txt`, иначе `live_only` |
| S1 | `work/reference-snapshot.yaml` (`:50`) | `reference_snapshot.py` (`:85-88`) | вне главного прохода (S-c история) | `live_only` |
| S2 | `work/requirements-register.md`, `work/requirements-readiness.json`, `understanding.md` (`:76-78`) | роль `qa-requirements-tester` (`:37-58`) | заглушка | требование `stage_output:<каждый>`; иначе `live_only` |
| S2–S9 | форма передачи диспатча `work/handoffs/<dispatch>.yaml` | `handoff_init.py` создаёт, роль заполняет (`:297-304`) | заглушка | `fill_form` (П1-а) |
| S3 | `test-plan.md` (`:124`) | роль `qa-test-strategist` (`:63-66`) | заглушка | `plan_md_row` + требование `stage_output:test-plan.md` (рамка документа) |
| S3 | `work/test-plan.json` (`:125`) | роль (`:67-75`) | заглушка | `plan_json_row` |
| S3 | `work/grounding.yaml` (`:126`) | роль (`:76-84`) | заглушка | требование `stage_output:work/grounding.yaml`, иначе `live_only` |
| S4 | `work/test-cases/` (`:160`) | роль `qa-case-designer` (`:133-136`) | заглушка | `case` |
| S4 | `state/story-case-links.json` (`:161`) | `case_versions.py` (`:137-140`) | код | — |
| S5 | `work/automation-manifest.json` (`:193`) | `manifest_put.py` (`:141-148`) | код по фрагменту роли | `manifest_row` (фрагмент) |
| S5 | тест-файлы проекта | роль `qa-automator` | заглушка | `test_file:<lang>` по строке раннера |
| S5 | `work/s5-plan.json` (`:195`) | роль (`:149-155`) | заглушка | требование `stage_output:work/s5-plan.json`, иначе `live_only` |
| S5 | `work/s5-notes/` (`:196`) | роль (`:121-132`) | заглушка | требование `stage_output:work/s5-notes/`, иначе `live_only` |
| S5 | `work/evidence/` (`:194`) | `run_suite.py` (`:184-193`) | код (команда профиля) | — |
| S6 | `work/run-report.json` (`:227`) | `finalize_task.py` (`:180-183`) | код | — |
| S6 | `work/evidence/manual/<case>/tried.md` (`:229`) | роль `qa-runner` (`:243-246`) | заглушка | требование `stage_output:…/tried.md`, иначе `live_only` |
| S7 | `work/triage.json` (`:255`) | роль `qa-failure-analyst` (`:247-255`) | заглушка | требование `stage_output:work/triage.json`, иначе `live_only` |
| S7 | `work/bug-drafts/` (`:256`) | роль (`:260-263`) | заглушка | требование `stage_output:work/bug-drafts/`, иначе `live_only` |
| S8 | `work/ledger.json`, `work/ledger.md` (`:282-283`) | `ledger.py` (`:272-279`) | код | — |
| S8 | `test-report.md` (`:284`) | роль `qa-doc-scribe` (`:288-296`) | заглушка | требование `stage_output:test-report.md`, иначе `live_only` |
| S8 | `work/proposals/` (`:285`) | `external_writes.py` (`:336-339`) | код | — |
| S8 | `project:bugs/` (`:286`) | роль `qa-bug-reporter` после гейта B (`:268-271`) | заглушка | требование `stage_output:project:bugs/`, иначе `live_only` |
| S8/S9 | `project:obligations.md` (`:287`, `:333`) | роль `qa-retro-analyst` (`:324-327`) | заглушка | требование, иначе `live_only` |
| S9 | `retro.md` (`:332`) | роль (`:317-323`; режим `numbers` — кодом) | заглушка или код (`numbers`) | требование `stage_output:retro.md`, иначе `live_only` |
| S9 | `project:factory-backlog.md` (`:334`) | роль (`:328-331`) | заглушка | требование, иначе `live_only` |

Выход с писателем «роль», для которого нет вида заполнителя, делает недостижимым всё, что ниже его по течению: строки
ниже получают `reach: live_only` с `why_unreached: "filler kind <вид> missing (П1-а)"` (храповик, только убывает); когда П1-а
добавляет вид — строки исполняются (E13).

### 4.3 Состояние для строки обхода — снимки на границах стадий (новое, t-401 №10)

- Главный проход (N3) после закрытия каждой стадии делает **снимок мира** (`dry_world.snapshot(name)`): байтовая копия
  проекта мира и `qa-factory/artifacts/<task>/` в каталог временных файлов теста, имя — `S<n>` по последней закрытой стадии.
  Снимок живёт только в этом прогоне теста и **никогда не коммитится** (закоммиченный мир — рукописный вход, причина A).
- Строка обхода стартует с **копии** снимка `start` (`dry_world.from_snapshot(name)`: копия копии, сам снимок не меняется),
  поднимает свой стенд «жив» и выполняет `seed` — короткую последовательность шагов только настоящими писателями:
  (а) `drive_until: {"stage": "S<n>", "question": "<ключ|вид>"}` — прогон драйвера от снимка до нужного вопроса с управлением
  заглушки из `stub`; (б) `op: ["<скрипт>", "<аргументы>"]` — операция контроллера / `story_step.py` / `stage_done.py` /
  `waiver.py` отдельным процессом. Запрещено в рецепте: писать руками `driver-state.json` `asked`, `pipeline.json` стадий,
  файлы вопросов; создавать `Driver` в процессе теста (F4 (а), решение Lead).
- Снимка, до которого главный проход не дошёл, нет: строка со `start`, которого нет, — `after:<id находки, на которой встал
  проход>` (NOTE, счёт храповика `after`), никогда не PASS (E15).
- Время строки ограничено капом на строку (E6); снимки делают время строки независимым от длины пути от S0.

### 4.4 Окружение, журнал и ответы заглушки (новое, t-401 №16, №18; F10)

- `STORY_RUN_CLASS=dry` — выставляет обходчик в окружение каждого процесса, который запускает (решение Lead №16; читатель —
  П1-в). Отсутствует — читатели считают прогон `live` (так решил Lead); поэтому обходчик проверяет перед первым шагом, что
  переменная видна в окружении процесса заглушки (заглушка пишет её значение первой строкой своего журнала), иначе красное
  «run class not propagated» (E18).
- Ответ заглушки (роль или дирижёр) несёт `session_id: "stub-<dispatch>-<n>"`, где `<n>` — счётчик вызовов заглушки ПО id
  диспатча (для дирижёра — `stub-conductor-<n>`), в поле той квитанции, которую драйвер читает у хоста
  (`story_run_common.RECEIPT`, `:32-52`). Счётчик по id диспатча, не общий индекс (гонка, `story_run_common.py:75-77`).
- Журнал заглушки `state/dry-stub.jsonl` (пишет только `dry_stub.py`, в мир сухой стори): строка на вызов — `ts`, `dispatch`
  (или `conductor`), `n`, `role`, `prompt_sha` (sha256 подсказки, нормализованной `DISPATCH_ID_RE`), `wrote` (пути), `run_class`.
  Читатели: C5 (§3.4), положительный контроль E7, `run_counters` (через `driver-runs.jsonl`, не этот файл).
- **Ключ цен вопроса** (нужен для `driven` и K15 в процессе, §3.2): драйвер не пишет ключ в запись вопроса
  (`driver_dialog.py:410-419` — полей ключа нет). Как его узнать — развилка **F10** (рекомендация (а): обёртка
  `dry_driver.py` ставит проходящий записывающий шпион на `no_move.priced_options` — тот же приём, что `test_conductor_doors.py:723-729`,
  но в процессе драйвера — и пишет `{"key", "answers"}` в `state/dry-priced.jsonl`, затем зовёт `story_run.main()`).

---

## 5. Края (поведение и инвариант каждого)

| # | Край | Поведение | Инвариант, который защищён |
|---|---|---|---|
| E1 | Состояние достижимо только живым ответом роли | строка `reach: live_only` с `why_unreached`; печатается NOTE-строкой с id; счёт в храповике `live_only` (только убывает); П2-г забирает | ни одно неохваченное состояние не считается пройденным молча; рост неохвата виден критику |
| E2 | Отказ без закрытого варианта (маршрут `KNOWN_REFUSALS` с ходом кода) | исполняется ход кода; за ≤ N шагов цикла (N = число маршрутов в цепочке рецепта) отпечаток другой и вопроса без вариантов нет; отказ ни с ходом, ни с вариантами — красное «тупик» | не бывает состояния, из которого нет ни хода кода, ни двери человеку (AR-25, FR-57) |
| E3 | Исполнитель варианта — дирижёр (ход дирижёра `rework_stage`, `story_fact`, …) | заглушка дирижёра исполняет ход ровно существующей командой хода (данные `conductor-actions.json`) с аргументами из строки; затем C3. Ход, который без суждения не заполнить, — строка `executor: conductor_judgment`: проверяется только C5 | вариант без исполнителя никогда не зелёный; суждение дирижёра не имитируется (AR-29) |
| E4 | Параллельные окна | главный проход последовательный (`parallel_windows: 1`, `manual.walkers: 1` — как `seed`, `story_run_common.py:203-211`); отдельная строка «два окна S5» с барьером меток (механизм `:85-145`), каждое ожидание с капом; счётчик вызовов заглушки по id диспатча, не общий индекс (гонка `:75-77`) | параллельная дорога — та же дорога (P31), проверяется, а не исключается; заглушка никогда не виснет |
| E5 | Маршрут/стык/вид без ключа, добавленный позже, без строки | C1 красное с дверью «строка в `fixtures/driver-exits/<group>.json`»; новый ключ цен без строки — красное существующей переписи | новое место выхода не проходит молча |
| E6 | Бюджет времени CI | F6 (а): отдельная задача CI `dry-story`, части по группам; кап на строку и на задачу назначает Lead после замера N0; за капом строки — красное с id строки и секундами; за капом задачи — красное с именами пяти самых долгих строк; локальный свидетель — §6 «Свидетель» | канон не превращается в часы, и строка не выпадает молча по таймауту |
| E7 | Пустой/нечитаемый носитель (`question-prices.json`, журнал вопросов, журнал заглушки, `dry-priced.jsonl`, `state/controller.json`) | красное с именем файла и тем, что ожидалось (FR-59); «вызовов дирижёра 0» утверждается только после положительного контроля (первая строка журнала заглушки записана); `dispatch_rounds` → `[]` — NOTE «rounds unknown», не PASS C3 | неизвестное не становится зелёным (AR-28) |
| E8 | Отказы хуков (`refusal_registry`, 77 построчных) | класс `hook_layer`: один счёт в храповике, построчно не обходятся (t-401 №37); проверка данных C4з по F11 | граница слоя названа, а не подразумевается; запрет без двери виден |
| E9 | Слова человека — вход СНАРУЖИ (адверсарная батарея, правило 11) | строки-варианты — только на ключах с ответом `person: "answer"` и видах `conductor`/`refusal` (§3.3): величина (24 КБ; на и за `DECISION_CHARS_MIN` = 240 — 240 и 241 символ, `RM/scripts/brief_pack.py:60`; на и за `BRIEF_MAX_BYTES` = 6144, `:54`); вложенность (markdown-ограда, цитата); кодировка (кириллица кодовыми точками как `OTHER_SCRIPT`, BOM, CRLF); жетон + строки слов; жетон в бэктиках; другой регистр; пустой файл → ожидаемый `Stop` «is empty» (`RM/scripts/driver_machine.py:3319-3320`), не пропуск | слова доходят целиком; пустой ответ не становится ответом |
| E10 | Конфликт требований C4 (слово проводит гейт, P13/FR-4) ↔ отказы «слово не проходит» (§3.6) — **переписан (t-401 №9; F7 (а) отменено Lead)** | C4 по классу: ГЕЙТ — ожидается проход и строка `passed-by-person.jsonl` (C4г); сегодняшние 7 семейств `s5_precheck` → `known_red` с находкой (R-L5); гейты, где проход противоречит слову владельца (Q1, Q2), — до ответа строка печатает NOTE «owner question Q<n> open», не PASS и не red; ЗАПРЕТ — дверь (C4з) | слово человека проводит любой гейт и проход записан; запрет не обходится, но дверь у него есть; решение владельца не перекрывается кодом молча |
| E11 | Конфликт «красный на main» ↔ «канон зелёный» | F8 (а): реестр общего помощника `known_red.py` (П1-а), строгий режим, id = строка обхода | канон зелёный, красное по известной находке видно |
| E12 | ВРЕМЕННОЙ: файлы, которых сегодня нет (`fixtures/driver-exits/`, `dry_exits.py`, `dry_stub.py`, `dry_world.py`, `dry_driver.py`, `stories/dry-1/`, `test_scenario_dry_1.py`, `known_red.py` П1-а) | до N1 `--witness-for` их не знает: DoD узла называет прогон напрямую; `test-layers.json` `enforce_listing: true` (`:12`) красит канон строкой `unlisted:` — строка `keep` входит тем же коммитом, что новый `test_*.py` (N3); `dry_*.py` — не `test_*` и не листятся (как `scenario_walk.py`); до узла `known_red.py` П1-а узел N1 не стартует (импорт) | канон не краснеет от незаписанного файла; слой не заводит второй реестр меток |
| E13 | ВРЕМЕННОЙ: заполнитель П1-а ещё не умеет вид выхода | строки ниже по течению — `live_only` с причиной «filler kind missing»; когда вид появляется (узел П1-а), строки исполняются тем же прогоном; новые красные получают свою метку с находкой (как E15) | слой не строится на рукописных формах (причина A); не умеющий заполнитель не становится зелёным |
| E14 | Строка с ожиданием от владельца (FV1-2) | ожидание — цитата с носителем в строке обхода (`expect.owner_quote`); без носителя строка запрещена | код не оракул (P20): ожидание из слова владельца, не из реализации |
| E15 | **ВРЕМЕННОЙ (новый, t-401 №10): починка FV1-1** | До починки: главный проход встаёт на S5 (пустая область), строка `main/S5` — `known_red: FV1-1`; снимков S5…S9 нет; строки с таким `start` — `after:FV1-1` (NOTE, храповик `after`). После (коммит узла FV1-1 в `live-run-fvf`): узел снимает свою метку `main/S5`; главный проход идёт дальше, снимки появляются, строки `after:FV1-1` исполняются автоматически в том же прогоне. Новый красный ниже по течению получает **свою** строку реестра `known_red` с **своей** находкой (файл в `findings/` и строка пачки тем же ходом, D-0044) и `raised_by: <узел FV1-1>`; помощник отказывает строке, чья метка равна её же `after` (`after:FV1-1` + `known_red: FV1-1` → красное «a row is never expected red for the defect that made it unreachable»), и любой строке с меткой FV1-1, кроме `main/S5` | недостижимая строка никогда не PASS; дефект ниже по течению не прячется под чужой меткой; узел FV1-1 отвечает только за свою строку |
| E16 | Снимок мира отсутствует, повреждён или от другого прогона | `from_snapshot` проверяет, что снимок сделан главным проходом этого же процесса теста (метка процесса в снимке), иначе красное «snapshot not from this run»; снимок не найден → `after:<находка>` (E15) | строка никогда не стартует с мира, собранного не настоящими писателями |
| E17 | Ключ цен вопроса не записан (F10) или записанный ответ-набор ≠ строкам цен | красное с ключом и разницей (K15 в процессе); вопрос без записи `dry-priced.jsonl` при строке с ключом — красное «key not observed», не догадка по тексту | ключ, который строка «гоняет», действительно поднят и предложен целиком |
| E18 | `STORY_RUN_CLASS` не дошла до процесса заглушки | красное «run class not propagated» до первого шага строки | сухой прогон никогда не считается живым (П1-в §7.9, ось 34) |
| E19 | Строка маршрута с ходом `ask_person` без `class_source`, источник отказа не в `classes.json` | красное «class unknown» | класс не угадывается (FR-59) |
| E20 | Пара требований «ключ `driven` целиком» ↔ «строка ответа `live_only`» | ключ с хотя бы одной строкой ответа не исполняемой (`live_only`/`after`) — НЕ `driven`; запись `PINNED_ELSEWHERE` для него остаётся | перепись не теряет закрепление ключа, который сухая стори гоняет не целиком |
| E21 | Синтетическая история и `story_coverage_required` (`test-layers.json:13-26`) | строка `keep` `test_scenario_dry_1.py` не заявляет покрытие S1…S9 за записанные истории | требование записанных историй не закрывается синтетикой |
| E22 | Строки гейтов с открытым вопросом владельцу (Q1, Q2) | NOTE с номером вопроса до ответа; после ответа — Lead пишет ожидание в строку (`expect.owner_quote` с носителем) | решение владельца не подменяется ни кодом, ни Lead |

Языки: дорога одна (P31) — F5 (а), строки таблицы раннеров; улов FV1-19 дефект 2 — на обеих строках (§9.3).

---

## 6. Узлы для более слабой модели

Горячие файлы (`story_run.py`, `controller.py`, `stage_guard.py`, `hooklib.py`; D-0048) — НЕ пишутся ни одним узлом; все
читаются. Общие файлы с другими пачками и спеками — §8, порядок на `test-layers.json` и `scenario_walk.py` — там же.

Порядок: [П1-а: узел `known_red.py`, узел `fill_form`] → N0 (спайк) → **решение Lead «продолжать / сузить»** → N1 ∥ N2
(N2 после узлов `fill_artifact` П1-а для стадий главного прохода) → N3 → N4:<group> (параллельно, owns не пересекаются) →
N4c (последовательно, после всех N4) → N5. N6 — по F5, после N0 и N5. Узел Lead N-L сажается вместе с N1 (храповик) и до N5.

**Свидетель (t-401 №27).** Для любого узла: `--witness-for <owns>` печатает список; ЛОКАЛЬНО гоняются только быстрые
(до минуты): `dry_exits.py --check` и `dry_stub.py --selftest`, а также `test_scenario_dry_1.py --part <своя часть>`, если
замер N0 дал часть ≤ 60 с; правка `scenario_walk.py` по коду `witness_for` называет все сценарные тесты
(`scenario_walk.py:910-912`): `test_scenario_cart_1.py` 67.4 с, `…_local_1_0108.py` 110.4 с, `…_local_1_arm_b.py` 22.8 с
(`slow_tests.json:118-120`, с потолками `selftest.py:110-115`) — они и `test_conductor_doors.py` (53.0 с) судятся ТОЛЬКО CI
на ветке пачки (`docs/RUNBOOK.md` §7, чтение через `tools/ci_read.py`); отчёт узла прикладывает вывод `--witness-for` и ссылку
на прогон CI. Медленные файлы (`test_story_run_*`) локально не гоняются.

### N0 — спайк: главный проход S0→S3 с формами на заглушках, замер (новое, t-401 №10)
given: эта спека §4; `RM/scripts/tests/story_run_common.py:32-181,199-211,333-334,405-426,480-496`; `RM/references/stages.json:5-138`; `RM/references/artifact-writers.json`; `RM/references/role-commands.json`; спека П1-а (`fill_form`, `fill_artifact` видов S1–S3)
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\dry_stub.py
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\dry_world.py
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\stories\dry-1\
C:\QAFactory\forge-repo\.github\workflows\canon.yml
non-goals: обход выходов; перепись; строки `keep`; оптимизация
handoff: отчёт билдера (правило 7) + таблица секунд (по стадиям S0…S3, на снимок, на одну строку от снимка — три пробные строки: `s1.review/go on`, `questions/answers`, `halt/words`) + ссылка на прогон CI
edges: E7, E13, E16, E18; формы ВКЛЮЧЕНЫ
DoD: задача `dry-story-spike` (ручной запуск `workflow_dispatch`) в `canon.yml` на ветке узла печатает строку `spike: S0..S3 <сек> s; snapshot <сек> s; row median <сек> s; rows 3` и исход по стадиям; прогон через `docs/RUNBOOK.md` §7, вывод — `python tools/ci_read.py`; локально — только `python -B ai-packages/qa-factory/scripts/tests/dry_stub.py --selftest`
siblings: ось 34 (одна дорога: тот же процесс драйвера, что живой)

**Ворота решения Lead (до N2; числа — рекомендация дизайнера, решает Lead, F6 (а) уже назначила кап «после замера»):**
- **продолжать**, если на CI: S0→S3 ≤ 120 с И медиана строки от снимка ≤ 20 с (оценка задачи: 2,5 × (S0→S3) + ~120 строк ×
  медиана ≤ 15 мин — кап F6 (а));
- **сузить**, если S0→S3 ∈ (120, 300] с или медиана ∈ (20, 60] с: строк — по одной на КЛАСС исполнителя ключа (строки цен с
  одинаковым `factory`-классом сливаются в одну строку), батарея E9 — только величина и пустое; новый замер на N3;
- **стоп и возврат Lead** (пересмотр формы слоя), если S0→S3 > 300 с или любая пробная строка > 60 с.

### N1 — перепись маршрутов/стыков, классы, сканер, отпечаток
given: эта спека §3; `RM/scripts/no_move.py`; `RM/scripts/driver_dispatch.py:38-107`; `RM/scripts/driver_core.py:47-81,192-233`; `RM/scripts/driver_machine.py:3314-3600`; `RM/references/question-prices.json`; `RM/references/stage-joints.json`; `RM/scripts/refusal_registry.py:57-72,1105-1180`; `RM/scripts/retro_numbers.py:268-307`; `RM/scripts/tests/harness.py` (`driver_sources`); `RM/scripts/tests/test_conductor_doors.py:626-679,799-805`; помощник `scripts/tests/known_red.py` (узел П1-а — импорт)
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\dry_exits.py
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\driver-exits\
non-goals: исполнение строк; правки драйвера; правка `test_conductor_doors.py` (N4c); второй реестр меток
handoff: отчёт билдера (правило 7) + вывод прогона
edges: E5, E7, E8, E12, E19, E20; неудобные входы §3.4
DoD: `python -B ai-packages/qa-factory/scripts/tests/dry_exits.py --check` печатает 0 расхождений и числа §3.1/§3.6 с командой пересчёта; три отрицательных контроля на байтовых КОПИЯХ (правило 7 гигиены): копия `driver-exits/<group>.json` без одного маршрута → красное с именем маршрута; копия с ростом `unwalked` без `raised_by` → красное; копия реестра меток, где помечена строка `exit.resume_limit/go on`, а строка `exit.resume_limit/round` красна без метки → красное с id `exit.resume_limit/round` (t-401 №8)
siblings: ось 18 (новый храповик — строка оси и вопроса 9 сажает N-L тем же коммитом), ось 34

| Пункт | Файл, функция | Поведение | Проверка |
|---|---|---|---|
| 1 | `dry_exits.scan_kinds_without_key()` | AST набора драйвера через `harness.driver_sources()`: виды `Person` (литерал и места `raised_at`), у которых место НЕ передаёт `closed_question(...)`/`priced_section(...)` | список с числом; вид, у которого есть и места с ключом, и без, — в списке со своими `raised_at` |
| 2 | `scan_routes()` | `driver_dispatch.KNOWN_REFUSALS` импортом (не регуляркой по тексту) + `unmatched`, `known_false` | 21 + 2 |
| 3 | `scan_prices()` | `no_move.load_question_prices()`; `DataUnreadable` → красное с файлом | 61 ключ / 188 вариантов (печать, не пин: TESTING.md:87) |
| 4 | `scan_joints()` | ключи `check` `stage-joints.json` через его читателя (`scripts/stage_joints.py`) | 43 (печать) |
| 5 | `load()` | склейка `fixtures/driver-exits/*.json` кроме `classes.json`; одинаковый id в двух файлах → красное с путями | таблица случаев |
| 6 | `check()` | сверка §3.2 в обе стороны + храповики (сумма по файлам групп против баз в тех же файлах) | каждый случай расхождения — красное с дверью |
| 7 | `class_of(row)` | §3.6 по `classes.json`; нет источника → «class unknown» | 58/19/25/43 печатаются с командой |
| 8 | `ban_doors()` (по F11 (а)) | записи `REGISTRY` с `override: ""` и пустым `unpassable_because` → красное с id | 0 на сегодня (печать); копия с пустым полем → красное |
| 9 | `state_fingerprint()`, `same_ask()` | §3.4 | таблица неудобных входов §3.4 |
| 10 | `driven_keys()` | §3.2 (ключ целиком; `live_only`/`after` не считаются, E20) | таблица: ключ с одной `live_only`-строкой ответа → не в множестве |
| 11 | заполнить `driver-exits/<group>.json` | каждая строка с `reach`; не обойдённое — `unwalked` с группой (счёт храповика) | `--check` зелёный |

### N2 — заглушка ролей и дирижёра, набор истории, обёртка ключа
given: N0, N1; спека П1-а (`fill_form`, `fill_artifact` с `overrides`, виды по §4.2); `RM/scripts/tests/story_run_common.py:32-181`; `RM/scripts/profile_contract.py:243-260`; `RM/references/artifact-writers.json`; `RM/references/role-commands.json`; `RM/scripts/no_move.py:612-630`
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\dry_stub.py
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\dry_driver.py
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\stories\dry-1\story.json
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\stories\dry-1\ticket\
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\stories\dry-1\kit.json
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\stories\dry-1\runners\
non-goals: заполнитель (П1-а); выбор по смыслу; разбор брифа; рукописный текст выходов
handoff: отчёт билдера + вывод прогона
edges: E3, E4, E13, E17, E18
DoD: `python -B ai-packages/qa-factory/scripts/tests/dry_stub.py --selftest` — (1) роль S2 пишет реестр и форму передачи через заполнитель; выход без вида заполнителя → исключение `Unfillable` с формой и полем, не текст; (2) дирижёр на подсказке с `## Moves open here` отвечает `ask_person` со всеми открытыми ходами; (3) одинаковый вход → одинаковые байты; (4) `session_id` ответа = `stub-<dispatch>-<n>`, счётчик по диспатчу; (5) строка журнала несёт `run_class` из окружения; (6) команды автоматора взяты из `profile_contract.profile_commands` профиля мира — копия профиля без `commands` → заглушка пишет в журнал «no command» и НЕ ищет команду в брифе
siblings: ось 5 (двойники ролей по стадиям), ось 30 (команды профиля), ось 34

| Пункт | Что | Поведение | Проверка |
|---|---|---|---|
| 1 | ветка роли | читает `Artifacts dir:`/`Dispatch:` (как `STUB`, `:119-120`), пишет выходы с писателем «роль» по §4.2 заполнителем (+ форма передачи `fill_form`); `overrides` и `repair_on_round` — из строки | выходы S1–S9 без рукописного текста; нет вида → `live_only` строки ниже |
| 2 | ветка автоматора | тест-файлы — `test_file:<lang>` строки раннера; запуск — команды профиля (`profile_commands`), фрагмент манифеста — `manifest_row` через `manifest_put.py` | команда не из брифа (грep) |
| 3 | ветка дирижёра | действие/вариант из строки; по умолчанию все открытые предлагаемые ходы; `why_person`/`checked` из строки (RN1-9) | ответ проходит `no_move.validate_options` |
| 4 | журнал `state/dry-stub.jsonl` | §4.4 | первая строка — `run_class` |
| 5 | `dry_driver.py` (F10 (а)) | проходящий шпион на `no_move.priced_options` пишет `{"key","answers"}` в `state/dry-priced.jsonl`, зовёт настоящий и `story_run.main()` | ни одного присваивания атрибута `Driver` (грep) |
| 6 | `stories/dry-1/` | `story.json` (`synthetic: true`), тикет (2 требования, 1 автокейс, 1 ручной), `kit.json` (ключ, id), `runners/python-pytest/` (строка F5 первая) | `scenario_walk.load_story("dry-1")` читает |

**Требование к спеке П1-а (интерфейс заполнителя)** — сверено с решением Lead №4. Вход: путь формы или шаблона артефакта
(`handoffs/*.yaml`, контракты артефактов, шаблон кейса, выходы стадий по §4.2); набор истории (ключ задачи, id требований,
id кейсов, пути тестов, id диспатча, стадия, роль); `overrides {поле: значение | ABSENT}` для затравки отказов. Выход: байты
заполненной формы и карта «плейсхолдер → значение» (чтобы красная строка называла поле). Детерминизм: тот же вход → те же
байты. Плейсхолдер, который не заполнить, — исключение с формой и полем, никогда не молчаливое значение. Заполняет ТОЛЬКО по
подсказкам формы (`<P-n>` → `P-1`): расхождение сегодняшних форм с читателями сохраняется (в этом смысл). Вызов — функцией в
процессе. Перечень видов, которые П1-б ждёт, — колонка «П1-а» таблицы §4.2.

### N3 — дверь `driver`, главный проход S0…S9, снимки, инварианты
given: N0, N1, N2; `RM/scripts/tests/scenario_walk.py`; `RM/scripts/driver_dialog.py:270-425`; `RM/scripts/gate_preflight.py:6036-6066`
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\scenario_walk.py
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_scenario_dry_1.py
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\dry_world.py
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test-layers.json
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\selftest.py (только словарь `TEST_TIMEOUTS`, `:110-…`)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\slow_tests.json
non-goals: строки обхода (N4); CI (N5); правка `test_conductor_doors.py`
handoff: отчёт билдера + вывод прогона + ссылка на CI
edges: E6, E7, E11, E12, E15, E16, E18, E21
DoD: `python -B ai-packages/qa-factory/scripts/tests/test_scenario_dry_1.py --part main` — проход до S9 или до первой строки `known_red`, каждая отмечена id находки; снимки `S0…S<n>` перечислены; строки за местом остановки напечатаны `after:<находка>`; `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/driver_machine.py` называет `test_scenario_dry_1.py`
siblings: ось 17 (форма вывода обходчика), ось 18

| Пункт | Что | Поведение | Проверка |
|---|---|---|---|
| 1 | `DOORS` += `driver`, `DOOR_MODULES["driver"] = ["story_run"]` | дверь запускает процесс драйвера в КОПИИ мира с `STORY_RUN_CLASS=dry` | `--witness-for` по `driver_*.py` |
| 2 | мир (`dry_world.build`) | `s0_project`-образ без `handoffs.required = False`; стенд «жив» | грep `"required": False` по owns пуст |
| 3 | главный проход | ответы на вопросы — из строк `story.json` `walk`; после каждого ответа C3/C5; снимок на каждой закрытой стадии (§4.3) | исход по стадиям |
| 4 | I-gate (C6) | при каждом вопросе `gate_A`/`gate_B` запустить `gate_preflight.py --task <T> --gate <A|B>` (вывод JSON по умолчанию, `gate_preflight.py:6383-6384`) на КОПИИ мира и читать поле `gate_ready` (`:6064`); `false` → красное; текст «can start» не читается (t-401 №25) | строка FV1-7 |
| 5 | точка табло §3.5 | `run_counters.counters(task_root)`; NOTE до П1-в | строка вывода |
| 6 | строка `keep` | слой `scenario`, `covers` = `tests/dry_exits.py`, `tests/dry_stub.py`, `tests/dry_world.py`, `tests/dry_driver.py`, `scripts/tests/fixtures/driver-exits`, `scripts/tests/fixtures/stories/dry-1` + модули двери; тем же коммитом; без заявки `story_coverage` (E21) | канон без `unlisted:` |
| 7 | `TEST_TIMEOUTS` и `slow_tests.json` | строка `test_scenario_dry_1.py` с потолком по замеру N0 (t-401 №24); режим файла по умолчанию (без `--part`) = перепись + главный проход — его гоняет задача `full`; части обхода `--part exits:<g>` — только задача `dry-story` (§10, двойного прогона нет) | `selftest.py --slow-tests` видит строку |

### N4:<group> — обход выходов (части по группам стадий, параллельно; owns не пересекаются, t-401 №13)
given: N1–N3; спека §3.3 (грамматика), §3.6, §4.3; находки FND (FV1 своей группы)
owns (часть `<group>`; одна часть = один диспатч):
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\stories\dry-1\exits\<group>.json
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\stories\dry-1\seeds\<group>.json
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\driver-exits\<group>.json
non-goals: починка находок; правка `test_conductor_doors.py` (N4c); строки других групп; строки реестра меток (их вносит узел П1-а-помощника по заявке части — §10)
handoff: отчёт билдера + вывод прогона + список строк, которым нужна метка (id → находка)
edges: E1–E4, E8, E9, E13, E15, E17, E19, E20, E22
DoD: `python -B ai-packages/qa-factory/scripts/tests/test_scenario_dry_1.py --part exits:<group>` — каждая строка группы PASS, `known_red` (красная, как ожидается), NOTE `live_only`/`after:<находка>`/«owner question Q<n> open»; ни одной строки без исхода; счёт `unwalked` группы = 0
siblings: ось 5, ось 34

Группы: `s0` (halt, ticket_*, package, arrival, first_look_*), `s1-s4` (s1.gap, s1.review, questions, conductor/stage_review_exhausted, s3.grounding_*), `gates` (gate_A, gate_B, C4г стыков и операций), `s5` (s5.repair_limit, s5.nobody_*, exit.resume_limit*, s6.walk_* , s6.data_change, code_close.*), `s6-s9` (s6.stand_*, s7.*, s8.*, closed.held). Ключи и маршруты — в одной группе ровно один раз (N1 п. 5 ловит дубли). Строки групп `s5` и `s6-s9` на сегодняшнем main — `after:FV1-1` (E15).

### N4c — перепись ключей вопросов: строки сухой стори входят в `driven` (новое, t-401 №7; последовательно после всех N4)
given: N1 (`dry_exits.driven_keys`), все N4; `RM/scripts/tests/test_conductor_doors.py:626-679,794-805`; `RM/scripts/tests/test-layers.json:661`
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_conductor_doors.py
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test-layers.json (строка `keep` `test_conductor_doors.py`, только `covers`)
non-goals: смысл и сигнатура `census_problems`; строки обхода
handoff: отчёт билдера + ссылка на CI (файл 53 с — CI)
edges: E17, E20
DoD: CI на ветке: `test_conductor_doors.py` зелёный; в выводе K15 `driven` содержит ключи сухой стори; из `PINNED_ELSEWHERE` удалены ровно ключи из `dry_exits.driven_keys()` (список в отчёте); отрицательный контроль на копии `exits/<group>.json` без строки одного ответа — перепись краснеет «raised, but neither driven here nor pinned elsewhere: <ключ>»
siblings: ось 18 (перепись ключей — храповик «pinned elsewhere» сжимается)

Производитель (`driven_keys`, N1) и его второй читатель (`test_conductor_doors.py`) — в разных узлах сознательно: до N4c
функция имеет читателя `test_scenario_dry_1.py` (AR-22 держится); изменение ПЕРЕПИСИ (её `driven` и вычистка
`PINNED_ELSEWHERE`) — один коммит N4c.

### N5 — канон, CI
owns:
C:\QAFactory\forge-repo\.github\workflows\canon.yml
non-goals: удаление карантина; документы Lead (N-L)
DoD: задача CI `dry-story` в `canon.yml` (части `--part exits:<g>` матрицей) зелёная на ветке пачки (вывод через `tools/ci_read.py`); задача `dry-story-spike` N0 удалена тем же коммитом

### N6 — вторая строка таблицы раннеров (по F5; после N0 и N5)
owns: `stories/dry-1/runners/ts-playwright/`; `canon.yml` (Node и браузер в образе задачи `dry-story`). Свидетель — часть
`exits:s5` с этой строкой; улов FV1-19 дефект 2 на обеих строках (§9.3).

### N-L — требования к узлу Lead «носители П1» (решение Lead №17/№19; эта спека эти файлы НЕ пишет)
- R-L1 `docs/SIBLING_MAP.md`: ось 18 — храповики `fixtures/driver-exits/` (`live_only`, `after`, `unwalked`, `hook_layer`) и
  перепись ключей вопросов как общий носитель; ось 34 — строка механизма «сухая стори = тот же процесс драйвера; языки —
  строки раннеров»; ось 17 — форма вывода двери `driver`. Сажается ТЕМ ЖЕ коммитом, что N1 (AR-20, t-401 №23).
- R-L2 `docs/tasks/critic-diff-brief.md` вопрос 9 (храповики): называет храповики слоя — тем же коммитом, что N1.
- R-L3 `design/architecture.md`: AR-17 `:192` — `NO_MOVE_BASELINE_MAX = 55` (`audit_factory.py:1715`), не 102; AR-25/AR-22 —
  сухая стори как детектор в строке «Detector»; AR-15 — выживший переписи ключей вопросов `test_conductor_doors.py`.
- R-L4 `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md`: одна проверка на три спеки (один номер): возраст строк `known_red`, тренд
  `live_only`/`after`, находки живых прогонов с пустым полем «какой слой ниже должен был поймать».
- R-L5 находка (файл в `live-run-fvf/findings/` + строка пачки, D-0044): «7 семейств `s5_precheck` отказывают любому слову
  против P13/FR-4 (решение Lead №9)» — её id нужен строкам C4г группы `gates`/`s5` до N4:gates; носитель причины — план §2 B.
- R-L6 поле находки живого прогона «какой слой ниже должен был поймать» (план §6) — шаблон находки.
- R-L7 `docs/TESTING.md` — по F2 после слова владельца.
- R-L8 `docs/RUNBOOK.md` §4: «релиз требует зелёной задачи `dry-story`» (план §6).
- R-L9 узел починки FV1-1 (`live-run-fvf/1`): DoD называет `test_scenario_dry_1.py` (все части) и поведение E15.

---

## 7. Детектор, что мешает пропустить, цена — четыре вопроса (правило 10)

(a) **Цена.** CI: замер N0 (до него — оценка: главный проход + ~120 строк после срезки t-401 №26/№37, по снимкам);
кап — решение Lead после N0. Билдер: каждый новый маршрут `KNOWN_REFUSALS`, стык или вид без ключа требует строку
`driver-exits` (минуты); новый ключ цен — строку обхода или запись `PINNED_ELSEWHERE` в существующей переписи (как сегодня).
Платит фордж (CI) и автор нового места.

(b) **Оси** (36 осей `docs/SIBLING_MAP.md`; строки осей в самой карте пишет N-L, R-L1):
- ось 1: n/a — правила деплоя/ролей не меняются (кроме TESTING.md по F2, это не роль-файл);
- ось 2: n/a — экзамены тиров не трогаются;
- ось 3: covered — файлы в `scripts/tests/` уходят в релиз как все тесты пакета; отпечаток релиза их покрывает;
- ось 4: queued — FR-долг не меняется; находки FV1 уже в пачке `live-run-fvf/1`; новая находка C4г — R-L5;
- ось 5: covered — двойники стадий обходятся одной переписью, группы N4 по стадиям;
- ось 6: n/a — измерители не меняются; табло — П1-в (`run_counters.counters`);
- ось 7: n/a — идентичность теста не меняется;
- ось 8: covered — мир и снимки через `harness.temp_project`/`runtime_paths`, во временном каталоге, путей машины нет;
- оси 9, 10, 11: n/a — распознаватели тест-файла, верха git, слов шелла не трогаются;
- ось 12: covered — узлы §6 ложатся в пачку по правилам кучек (Lead при сборке);
- ось 13: n/a — текст диспатча не трогается (сырые читатели носителей драйвера — вопрос AR-13, §1, не оси 13; та же поправка, что критик t-401 №33 дал П1-в);
- оси 14, 15, 16: n/a — транскрипты, консоль, `read_json` не трогаются;
- ось 17: covered — обходчик печатает свою форму PASS/FAIL/NOTE, как `scenario_walk.Result`;
- ось 18: covered — храповики `driver-exits` и сжатие `PINNED_ELSEWHERE`; строка оси и вопрос 9 — R-L1/R-L2 тем же коммитом, что N1;
- оси 19, 20, 21, 22: n/a — хост не участвует (заглушка), таблицы markdown не читаются;
- оси 23–29: n/a — поля строк `tests[]`, исполнения, свежесть не меняются (читаются настоящим кодом);
- ось 30: covered — команды автоматора из `profile_contract.profile_commands` (t-401 №12);
- ось 31: n/a — носители ролей не меняются;
- ось 32: covered — §1 «Проверки слоя»: владелец и класс каждой; суждение не проверяется;
- ось 33: n/a — выбор диспатча не меняется;
- ось 34: covered/queued — одна дорога: языки — F5 (вторая строка — узел N6), параллельные окна — строка E4, сухой/живой —
  один процесс драйвера и `STORY_RUN_CLASS` (E18), перепись ключей — одна (t-401 №7);
- оси 35, 36: n/a — стороны стори и подстановки не меняются.

(c) **Детектор отказа механизма.** Свой: C1 (перепись против кода) — краснеет, если слой отстал от драйвера; храповики;
существующая перепись ключей. Внешний: калибровочная проверка — требование R-L4 к узлу Lead (один номер на три спеки).
До её записи — механизм с детектором только внутри себя (находка для Lead, t-401 №19).

(d) **Что мешает пропустить.** Задача CI `dry-story` в `canon.yml` на ветке пачки (D-0059: канон на CI); строка `keep`
делает файл частью канона (задача `full` гоняет перепись и главный проход); `--witness-for` называет сухую стори
свидетелем любой правки драйвера; перепись ключей вопросов краснеет на новом ключе без случая; релиз требует зелёной
(R-L8). Смысл красного судит критик (вопрос 5 TESTING.md).

---

## 8. Пересечения с работой в ходу

| Пачка / спека | Что пересекается | Конфликт и предложение |
|---|---|---|
| `package-ci/4` (ожидает) PC4-12 | `story_run_common.py` (`run_scenarios` → `scenario_world`) | N0–N3 только импортируют `story_run_common`; не писать её. Если PC4-12 сольётся раньше — `RECEIPT`/`s0_project` остаются; сверить импорт |
| PC4-10 | режет `test_story_run_refusals.py` (там перепись действий контроллера `:446-476`), `test_story_run_s0.py`, `test_story_run_s6.py` | N1 не зависит от неё; если перепись выносится — сканер N1 может стать её читателем (не сейчас) |
| PC4-5 | режет `controller.py` | слой читает контроллер процессом и через `Controller.apply` — имя класса и операции стабильны; узел резки гоняет сухую стори свидетелем (по `--witness-for`) |
| PC4-15, PC4-17, PC4-18 | пишут `test-layers.json` | порядок — строка ниже |
| PC4-16 (условный, TD-15.5r) | синтетические истории против `story_coverage_required` | сухая стори не заявляет покрытие (E21) — пересечения смысла нет |
| `forge/7` FG7-15 (`plans/piles/forge/batch-7-vhodyashchie-4.md:38`, «ожидает»; owns `scenario_walk.py`, `test-layers.json`) — **добавлено (t-401 №17, №36)** | `--witness-for` для путей вне пакета | тот же файл, что N3; порядок — строка ниже |
| `forge/7` FG7-19 (`:42`, «ожидает»; `--witness-for` печатает тесты читателей и секунды против потолка CI) — **добавлено** | `scenario_walk.py` (`witness_for`) | тот же файл, что N3; FG7-19 сократит список свидетелей двери `driver` (227 скриптов); порядок — строка ниже |
| `live-run-fvf/1` (ожидает) | узлы FV1-1, 2, 3, 4, 6, 7, 8, 13, 19, 20, 22 — починки | порядок плана §4: красная строка слоя (N3/N4) → правка. Узел починки снимает метку своей строки тем же коммитом; FV1-1 — по E15 (R-L9). Узлы FV1 зависят от N4 своей группы |
| `words-gates/1` (ожидает, 41 узел; 16 упоминаний `driver_gates`/`gate_brief`/`question_register`/`brief_pack`/`person_words`/`no_move`) | те же места, что строки гейтов и слов | файлового конфликта нет (слой их не пишет); конфликт смысла: их починки переворачивают метки — тот же порядок, что для FV1 |
| `driver-controller/1`, `gates-and-words/1` | закрыты | нет |
| П1-а (параллельная спека) | `known_red.py` (её первый узел), `fill_form`, `fill_artifact` с `overrides` и видами §4.2 | N1 ждёт `known_red.py`; N0 — `fill_form` и виды S1–S3; N2 — виды главного прохода (E13); П1-б импортирует, не проектирует |
| П1-в (параллельная спека) | `run_counters.counters(task_root)`, строка «повтор вопроса», `STORY_RUN_CLASS` | точка подключения §3.5; заглушка даёт `session_id: stub-…` (§4.4) |

**Строка очереди на общие файлы** (решение Lead №17; пишется в обе пачки при сборке):
`очередь: package-ci/4 PC4-15 → forge/7 FG7-15 → forge/7 FG7-19 → П1-а (узлы, пишущие test-layers.json) → П1-б N3 → П1-б N4c → П1-в N4`
для `ai-packages/qa-factory/scripts/tests/test-layers.json`; для `ai-packages/qa-factory/scripts/tests/scenario_walk.py`:
`очередь: forge/7 FG7-15 → forge/7 FG7-19 → П1-б N3`. PC4-17/PC4-18 (по одному детектору; purge по слову владельца) пишут
другие строки `test-layers.json` — с П1-б по D-0048 (непересекающиеся строки в `owns`) без очереди, если Lead так решит при
сборке; иначе — после N4c.

---

## 9. Развилки, возвращённые Lead

**F1. Форма слоя.** (а) история `dry-1` в слое сценариев с дверью `driver` и тестом истории `test_scenario_dry_1.py`
(форма, разрешённая TESTING.md:77-79); (б) отдельный слой/файл вне трёх; (в) расширить `story_run_common` и квартет
`test_story_run_*`. Последствия: (б) — новый слой правилу владельца; (в) — дорастить то, что ушло в карантин.
Рекомендация: (а). *Решено Lead: (а).*

**F2. Текст TESTING.md.** Слой 1 сегодня — «артефакты настоящих прогонов» (`:45-47`); сухая стори синтетическая.
(а) дописать одну фразу: «и одна сухая история, собранная кодом из сегодняшних форм, проходит настоящий драйвер; новый
вид выхода — строка её переписи»; (б) не менять, считать `dry-1` «синтетической историей» как `story.json synthetic: true`.
Рекомендация: (а) — TESTING.md держит слово владельца 10.11, правку подтверждает владелец. *Вопрос владельцу задан Lead.*

**F3. Где живёт перепись.** (а) тестовая перепись `scripts/tests/fixtures/driver-exits/`, код пакета её не читает;
(б) данные `references/question-kinds.json`, которые читает и драйвер. Рекомендация: (а) сейчас. *Решено Lead: (а).*
После t-401 №7 перепись ключей цен — существующая (`test_conductor_doors.py`), `driver-exits` — только маршруты/стыки/виды
без ключа.

**F4. Как ставить состояние.** (а) только настоящими писателями и процессом драйвера (§4); (б) затравка файлов
состояния руками. Рекомендация: (а). *Решено Lead: (а).* Снимки §4.3 — копии мира, сделанного настоящими писателями в этом же
прогоне; это не (б).

**F5. Языки (P31, ось 34).** (а) параметр — строка таблицы раннеров (данные, не имя языка), первая строка Python/pytest,
вторая TS/Playwright — узел N6; (б) только Python. Рекомендация: (а). *Решено Lead: (а).* После t-401 №37: N6 — после спайка N0.

**F6. Бюджет времени.** (а) отдельная задача CI `dry-story` с капом, части по группам стадий; (б) всё в быстрый уровень.
Рекомендация: (а). *Решено Lead: (а); кап — после замера (N0).*

**F7. «Слово человека снимает ЛЮБОЙ отказ».** *Решение Lead F7 (а) от 13.11 ОТМЕНЕНО решением Lead №9 по t-401*: C4 по классу
отказа — ГЕЙТ (слово проводит, проход в `passed-by-person.jsonl`) против ЗАПРЕТА хуков (дверь, FR-57); §3.6, E10.

**F8. Красное на main.** (а) метки `known_red`, строгий режим. *Решено Lead: (а)*; после t-401 №3/№8 — ОДИН помощник
`known_red.py` (П1-а), id = строка обхода.

**F9. Ожидание из слова владельца в строке (FV1-2).** (а) строка несёт ожидание с цитатой владельца 12.11
(`FND/20261112-dirizher-ne-ispolnil-slovo-vladelca-na-s5.md:7-8`). *Решено Lead: (а).*

**F10 (новая). Как обходчик узнаёт ключ цен вопроса** (нужно для `driven` и K15, §3.2, §4.4). Драйвер ключ в запись вопроса
не пишет (`driver_dialog.py:410-419`).
- (а) обёртка `dry_driver.py`: проходящий записывающий шпион на `no_move.priced_options` (функция модуля, не метод `Driver`;
  зовёт настоящую), пишет `{"key","answers"}` в `state/dry-priced.jsonl`, затем `story_run.main()`. Цена: малая; риск —
  процесс драйвера запущен не командой `story_run.py` (ось 34: дорога та же по коду, другая по точке входа).
- (б) сопоставлять жетоны вопроса со строками цен по множеству ответов. Цена: ноль кода; ошибка в запрещённую сторону —
  у разных ключей одинаковые наборы (`s5.nobody_*`, `s8.delivery.*`) → строка «гоняет» не тот ключ.
- (в) изменение продукта: драйвер пишет ключ в `asked` и `driver-questions.jsonl` (AR-22: поле данных едет дальше). Цена:
  правка `driver_dialog.py`/`Person` вне скоупа слоя (non-goals), новое поле — читатели (`collect_stall` L7, табло).
Рекомендация: (а) сейчас; (в) — находкой для П1-в/табло, если «вопросы по ключу» понадобятся и в живом прогоне.

**F11 (новая). Где живёт проверка «у запрета без прохода названа дверь» (C4з).** `refusal_registry --check` сегодня НЕ требует
`unpassable_because` у не-fail-closed записи («A missing override is NOT a violation on its own», `refusal_registry.py:1147-1148`).
- (а) `dry_exits.ban_doors()` читает `REGISTRY` импортом (тестовый слой; второй читатель правила реестра).
- (б) строка в `refusal_registry.audit` (`--check`; одна дорога; правка аудита пакета — свой узел с owns
  `refusal_registry.py` и строкой его теста).
Рекомендация: (б) — правило реестра живёт в реестре (AR-15); до решения — (а) как временный читатель с пометкой «перенести».

**F12 (новая). Числа ворот N0** (§6 N0): «продолжать» ≤ 120 с S0→S3 и ≤ 20 с медиана строки; «сузить» до 300/60 с;
«стоп» выше. Альтернатива — ворота по одной цифре (оценка задачи ≤ 15 мин). Рекомендация: две цифры (длина прохода и
цена строки — разные рычаги срезки). Решает Lead.

**F13 (новая). Покрытие ключа «целиком» для `driven`** (§3.2, E20). (а) ключ `driven`, только если КАЖДЫЙ ответ ключа
исполнен строкой; (б) достаточно одной исполненной строки ключа. Цена (а): ключи с одним `live_only`-ответом остаются в
`PINNED_ELSEWHERE` (часто — у карантинных файлов); (б) — перепись потеряет закрепление непройденных ответов. Рекомендация: (а).

### 9.2 Вопросы владельцу (решение Lead №9: проход словом против записанного решения владельца) — простыми словами

- **Q1.** «Проверка автотестов отказывает, когда тест проверяет значение, которое требование оставило открытым (ждёт вашего
  ответа). Сегодня это нельзя пропустить словом — только ответить на вопрос о значении; так записано по вашему правилу „код
  не оракул“ (01.10). По новому правилу „слово человека проводит любой гейт“ его пришлось бы пропускать словом. Как быть?
  (а) оставить: это место снимается только ответом о значении; (б) пропускать словом, записывая проход и пробел в отчёте.»
  Рекомендация: (а) — проход словом сделал бы тест с выдуманным ожиданием зелёным (P20). Носитель: `s5_precheck.py:90-94`.
- **Q2.** «Когда фабрика нашла баг и доставка „нет“, на вопросе о доставке есть ответ „go on“. Сейчас он проводит шаг, но
  доставка остаётся „нет“. По правилу „слово проводит любой гейт“ подтвердите: слово проводит ШАГ, а вердикт не меняет?
  (а) да, вердикт остаётся; (б) слово может сделать доставку „да“.» Рекомендация: (а) — так уже записано в данных и в
  ваших правилах о трёх исходах доставки (02.10/03.10). Носитель: `question-prices.json:302-303`, P21, FR-35.

Других проверок гейта, где проход словом спорит с записанным словом владельца, не найдено (поиск и контроль — §3.6).

### 9.3 Вердикты по находкам (переписано по t-401 №10, №11, №6)

| FV1 | Ловит ли слой | Случай | Красное сегодня |
|---|---|---|---|
| FV1-2 | да, только по F9 (а) | строка `window:empty_scope` × слово человека с ожиданием от владельца | **достижимо после FV1-1** (`after:FV1-1`: S5 на main не достигается) |
| FV1-6 | да — **проверкой данных C9** (t-401 №11) | `stage_review_exhausted` на S2 (критик-заглушка `reject` по строке, раунды исчерпаны): среди `asked.options` (`driver-state.json`, писатель `driver_dialog.py:326`) нет хода `rework_stage` (`conductor-actions.json:65-78`), у которого `args.role` = роль-автор стадии (`stages.json:61` `qa-requirements-tester`); вариант без `args.role` — красное «executor not named» (FR-42, безопасная сторона). После починки вариант появляется → строка зелёная независимо от вердикта заглушки | да (ожидается); S2 достижима главным проходом |
| FV1-7 | да | I-gate (C6) в главном проходе: сегодняшние формы S3/S4 пишут `<P-n>` → `gate_ready: false` (`gate_preflight.py:6064`) → гейт A показан | да (ожидается) |
| FV1-8 | да | `questions` × `go on` (отложить до отчёта) → затем `gate_A` × `approve`: решение не записано, гейт показан снова (C3/C5) | да (ожидается) |
| FV1-13 | да, четыре экземпляра | (1) `conductor` × `go on` → исполнено кодом, вызова дирижёра после жетона нет; (2) `exit.resume_limit` × «`round` + строки слов» (E9); (3) `exit.resume_limit` над находкой с заглушкой `<plan obligation id>` × `go on` → C2 «жив только `stop`»; (4) затравка «долг записан → раунд автора → отказ лимита критика» × `go on` → отпечаток тот же | экз. 1 — на S2/S3 (если состояние `conductor` достижимо до S5; иначе `after:FV1-1`); экз. 2–4 — **достижимо после FV1-1** (S5); экз. 3 закрыт t-180 на ветке, не в main — сверить при N4 |
| FV1-19, дефект 2 — **добавлено (t-401 №6, решение Lead)** | да, C10 | строка `s5.window_finish/ref_without_hash`: автоматор-заглушка пишет фрагмент манифеста через `manifest_put.py` с `overrides: {"obligation_refs[].obligation_hash": "ABSENT"}`; `s5_precheck` принимает; финиш окна (`Controller._s5_v2_collect`, `RM/scripts/controller.py:7294-7302`: «coverage v2 instance requires unique obligation_refs with exact hashes»; сверка с `content_hash` плана `:7289-7293`) отказывает → красное «два читателя одного поля разошлись». Зелёное после починки: или запись отказывает с правильным значением, или код строит хэш при записи (оба исхода — C10 зелёная). На обеих строках раннеров (P31; TS — N6) | **достижимо после FV1-1** (S5) |
| FV1-20 | частично | `s5.repair_limit` × `round` → ожидается новый диспатч автора (C3); сегодня уходит дирижёру. НЕ ловится: критик не запускает пробы, ложное «фабрика не может» дирижёра — суждение (AR-29), это П2-г | **достижимо после FV1-1** |
| FV1-22 | да (петля, C5) | главный проход S7: форма аналитика по шаблону без `stage_acceptance` → `stage_done` отказывает → дирижёр-заглушка `rework_stage` → тот же отказ, вход аналитика (подсказка) и его форма между 2-м и 3-м спросом не изменились → C5. Потерю поля формы ловит П1-а; секция живёт во вторичном контракте `s7-analyst-to-scribe.yaml:53` (критик t-401 №21) — от этого зависит направление починки | **достижимо после FV1-1** (S7) — на сегодняшнем main не краснеет (t-401 №10 (б)) |
| FV1-3 | да | `questions` × «свободные слова» без меток → ожидается вызов дирижёра (AR-16 `architecture.md:183`, слово владельца 12.11); сегодня «recorded by code — no question answered by a token» | да (ожидается; S2–S4) |
| FV1-4 | да | вопрос, после которого роль получает раунд, × слова 24 КБ (E9) → бриф следующей роли несёт слова целиком или называет файл слов; сегодня срезка до 240 | да (ожидается; строки до S4) |
| FV1-10 | нет | скаут — заглушка; чтение путей в тексте локальной стори — работа сборщика `context_bundle` и роли. Место — таблица случаев сборщика или П2-г | — |

Вне скоупа, но краснеет естественно: FV1-1 (П1-а держит) — главный проход с сегодняшними формами встаёт на пустой области
S5: строка `main/S5` с `known_red: FV1-1`; всё ниже — `after:FV1-1` (E15).

---

## 10. Мелкие решения, закрытые дизайнером

- Имена файлов: `dry_exits.py`, `dry_stub.py`, `dry_world.py`, `dry_driver.py` (не `test_*`: selftest их не запускает, как `scenario_walk.py`).
- Главный проход последовательный; параллель — отдельной строкой (E4).
- Группы частей обхода — по стадиям (N4); файл на группу в трёх каталогах (`exits/`, `seeds/`, `driver-exits/`).
- Тикет синтетический: 2 требования, 1 автокейс, 1 ручной (минимум, на котором есть S5 и S6).
- (t-401) Режим `test_scenario_dry_1.py` по умолчанию = перепись + главный проход (задача `full` канона), части обхода — только
  `--part exits:<g>` (задача `dry-story`): двойного прогона нет (ответ на t-401 №24).
- (t-401) Изменение переписи `test_conductor_doors.py` — отдельным последовательным узлом N4c после всех частей N4, чтобы
  параллельные части не делили этот файл.
- (t-401) Строки реестра меток для строк части N4 вносит узел-владелец помощника по списку из отчёта части (одна заявка на
  часть) — если помощник П1-а держит реестр в одном файле; если П1-а сделает реестр по файлу на группу — часть пишет свой.
  Окончательно — по форме, которую назначит П1-а.
- (t-401) Снимок мира — во временном каталоге теста, никогда не в репозитории.
- (t-401) Журнал заглушки `state/dry-stub.jsonl` и запись ключей `state/dry-priced.jsonl` — внутри мира сухой стори (не носители пакета).

## 10a. Решения Lead по развилкам (13.11.2026, при приёмке черновика t-397)

- F1 (а): история `dry-1` в слое сценариев, шестая дверь `driver`.
- F2: правка `docs/TESTING.md` — слово владельца; вопрос задан. До ответа узлы исполнимы по рекомендации (а), сама
  правка текста ждёт ответа.
- F3 (а): перепись — тестовая (`fixtures/driver-exits/` после t-401 №13).
- F4 (а): состояние ставится только настоящими писателями; недостижимое — `live_only` (только убывает).
- F5 (а): параметр — строка таблицы раннеров, Python/pytest и TS/Playwright (P31; исключение языка — только словом владельца).
- F6 (а): отдельная задача CI `dry-story`; кап — после первого замера.
- ~~F7 (а)~~ — **отменено решением Lead №9 по t-401** (план §10): C4 по классу отказа, §3.6.
- F8 (а): `known_red`, строгий режим. ОДИН механизм с П1-а — помощник `scripts/tests/known_red.py` (решение Lead №3/№8).
- F9 (а): строка FV1-2 несёт ожидание с цитатой владельца 12.11.

## 11. След чтения

| Что | Где | Результат |
|---|---|---|
| План, разведки | `docs/tasks/specs/20261113-plan-fabrika-ne-huzhe-agenta.md` (в фикс-раунде — §3, §4, §10); `reports/t-356-…`; `reports/t-357-…` | целиком (первый проход) |
| Вердикт критика | `docs/tasks/specs/reviews/t-401-p1-layers-plan-review.md` | целиком |
| Заглушка цикла, формы выключены | `RM/scripts/tests/story_run_common.py` 1-775 | `:201` `handoffs.required = False`; STUB `:54-181` |
| Обходчик | `RM/scripts/tests/scenario_walk.py` 1-140, 880-936 | `DOORS :40`, `DOOR_MODULES :46-47`; `witness_for :887-922` (правка `scenario_walk.py` → все сценарии `:910-912`) |
| Перепись ключей вопросов | `RM/scripts/tests/test_conductor_doors.py` 590-808 | `QUESTION_SITE_RE :626`, `AWAITING_ITS_SITE :634`, `PINNED_ELSEWHERE :636-665`, `census_problems :668-679`, шпион `:723-729`, `census(...)` `:802`, скан `:799-801` |
| Места ключей | Grep `closed_question\("\|priced_section\("` по `RM/scripts` | 38 мест; `driver_dispatch.py:3127,3135,3761-3762`; `driver_conductor.py:783`; определения `driver_runner.py:1187,1205`, `exploration.py:494` |
| Шов | `RM/scripts/no_move.py` 1-649 | `TOKEN_MOVES :40`, `MOVE_FACTS :161-172`, загрузчик цен `:589-609`, `priced_options :612-630` |
| Вопрос / запись | `RM/scripts/driver_dialog.py` 260-440; `RM/scripts/driver_core.py` 30-110, 150-257 | `ask` (`asked` `:319-333`), `already_answered :381-392`, `judge_own_question :394-425` (полей ключа цен нет); `Person`, `GATE_KINDS :52` |
| Ветви ответа | `RM/scripts/driver_machine.py` 3314-3473 | ветви по видам |
| Маршруты отказов | `RM/scripts/driver_dispatch.py` 30-145 | `KNOWN_REFUSALS :38-107` (21) |
| Виды вопросов | Grep `Person\(\s*"[A-Za-z_0-9]+"` -o, glob `{story_run,driver_*}.py` | 36 мест, 25 видов |
| Переменные виды | Grep `Person\(\s*[a-z_][a-zA-Z_.\[\]"']*\s*[,)]` | 5 мест (+ строка докстринга `driver_gates.py:831`) |
| Причины шва | Grep `"why": "[a-z_]+"` -o | 8 значений |
| Цены | Grep `^    "[^"]+": \[` -n (61 ключ, строки :3…:308); чтение `:1-40, 120-160, 280-315` — `RM/references/question-prices.json` | 61 / 188; `person: "answer"` `:126,130,150`; `s8.delivery.no` `:302-307` |
| Реестр отказов | `RM/scripts/refusal_registry.py` 1-110, 1100-1180; Grep `"override": ""\|^    \{"id": "\|"kind": "operation"\|^    # ---` -n | 102 записи (`{"id"` строк), 25 operation, 58 `override: ""` (последняя `:805`; operation-записи `:756`, `:812`…`:1034` без них); `SCANNED :57-58`; `audit` `:1147-1180` |
| Класс слова на гейте | `RM/scripts/exit_gate.py` 1750-1830; `RM/scripts/s5_precheck.py` 70-110, 3912-3960; Grep `refusal_line\(` | `word_class :1785-1804`; `CHECKS :72`, `PASSABLE :82`, `WORD_PASSABLE_TAGS :101`, `_passable :3930-3933`, `refusal_cause :3936-3949`; производитель `s5_precheck.py:4679` |
| Проход словом и запись | `RM/scripts/controller.py` 2395-2430, 7245-7310; `RM/scripts/waiver.py` 150-250 | `passed-by-person.jsonl :2402-2413`, `_passed_by_person :2417-2429`; `_s5_v2_collect :7247`, хэши ссылок `:7289-7302`; `split_overridden :202-222` |
| Слова владельца о проходе | Grep `-i` по 10 файлам гейтов (§3.6); `DECISIONS.md` Grep `-i` (0; контроль `D-00` → 23); `docs/DECISIONS_ARCHIVE.md` Grep (3 длинных строки: D-0046, D-0048 — не о проходе гейта) | §3.6, Q1, Q2 |
| FR-4 | `design/factory-rules.md:53-59` | «A person's word passes any block» |
| Репетиция гейта | `RM/scripts/gate_preflight.py` 6036-6100, 6200-6260, 6373-6390 | `run` → `gate_ready :6064`; текст «can start» `:6081`, `:6237`; JSON по умолчанию `:6384` |
| Круги диспатчей | `RM/scripts/retro_numbers.py` 268-307 | `dispatch_rounds` (`round` по стадии и роли) |
| Формы, брифы | Grep `handoff_init.py`, `brief_pack.py` | `work/handoffs/<dispatch>.yaml` (`handoff_init.py:421`), `work/briefs` (`brief_pack.py:4098`) |
| Команды профиля | `RM/scripts/profile_contract.py` 243-260 | `profile_commands` |
| Выходы стадий, писатели | `RM/references/stages.json` целиком; `RM/references/artifact-writers.json` целиком | табл. §4.2 |
| Ходы дирижёра | `RM/references/conductor-actions.json` 1-125, 195-224; Grep `"id"` | `moves :63-216` (`rework_stage :65-78`, `release_and_restart :111-124`) |
| Список данных пакета | Glob `*.json` в `RM/references` (положительный контроль после пустого Glob с фигурными скобками в шаблоне — промах вызова, не отсутствие) | `role-commands.json`, `artifact-writers.json`, `question-branch-keys.json` (не соответствие вид→ключ: `patch_keys`), `gate-registry.json` (не класс прохода) |
| Стыки | Grep `"check": "` — `RM/references/stage-joints.json` | 43 (8/8/27) |
| A27 | Grep `^NO_MOVE_BASELINE_MAX = \d+` — `RM/scripts/audit_factory.py` | 55 на `:1715` (против `architecture.md:192`) |
| Инварианты | `RM/design/architecture.md` 1-294 | AR-12, 13, 15, 16, 17, 20-29 |
| Перепись действий | `RM/scripts/tests/test_story_run_refusals.py` 420-500 | `:446-476` |
| Выходы состояний | `RM/scripts/tests/test_state_exits.py` 1-40 | перечисление из источника |
| Слой тестов | `RM/scripts/tests/test-layers.json` 1-34, 4938-4962, 6985-7024; Grep разделов | keep `:35`, `test_conductor_doors.py :661`, quarantine `:7022`, `story_coverage_required :13-26`, `keep_fail_at_entry :6994` |
| Время файлов | `RM/scripts/slow_tests.json` Grep; `RM/scripts/selftest.py` 100-120 | `test_conductor_doors.py` 53.0 (`:20`), сценарии 67.4/110.4/22.8 (`:118-120`), `test_story_run_s0.py` 289.8 (`:139`), `_s6.py` 218.8 (`:142`); `TEST_TIMEOUTS :110-116` |
| Бриф | `RM/scripts/brief_pack.py` 4415-4499; Grep констант | `BRIEF_MAX_BYTES :54`, `DECISION_CHARS_MIN :60` |
| Гейт / ревью | `RM/scripts/driver_gates.py` 818-857; `RM/scripts/driver_stage_plan.py` 686-735 | инварианты `gate_repair`; `stage_review_exhausted` |
| Петли | `RM/references/collect-loops.json`; Grep `collect_stall.py` | L1–L7 |
| Находки | `FND/` FV1-2, 3, 4, 6, 7, 8, 10, 13, 19, 20, 22; пачка `batch-1-live-run-fvf.md` (в фикс-раунде — `:58`, `:76-85`) | FV1-6 `:7-23`; FV1-19 дефекты `:12-28`, «дверь t-186 неполна» `:63-75` |
| Пачки | `plans/piles/package-ci/batch-4-…` (строки PC4-10…PC4-18, Grep); `plans/piles/forge/batch-7-vhodyashchie-4.md:38,42` (FG7-15, FG7-19); `driver-controller/batch-1`, `gates-and-words/batch-1`, `words-gates/batch-1` (шапки) | §8 |
| Сиблинг-спеки | `20261113-p1a-writer-reader-round-spec.md` (Grep `known_red\|fill_artifact\|overrides\|live_only\|ABSENT`: виды `:166`, `:289`; редакция ДО её фикс-раунда); `20261113-p1v-run-scoreboard-spec.md` (Grep `run_counters\|STORY_RUN_CLASS\|run_class\|stub-`) | §4.2, §8 |
| Правила | `docs/TESTING.md` целиком (первый проход); `td-15-scenarios-quarantine.md` 708-721; `docs/SIBLING_MAP.md` (Grep заголовков осей: 36) | — |
| CI | `RM/../.github/workflows/canon.yml` (Grep задач) | задачи `start`, `checks`, `full`, `clock` |

Не прочитано (честно): `plans/builder-rules.md` 7b (форма свидетеля взята из правила 4 CLAUDE.md, где она процитирована);
весь `take_answer` после `:3473`; `RM/scripts/stage_joints.py` (читатель назван по `architecture.md:116`);
`RM/references/role-commands.json` (только факт наличия — Glob; N0/N2 читают); поле квитанции хоста, куда кладётся
`session_id`, в `story_run_common.RECEIPT` `:32-52` (прочитано в первом проходе, поле в фикс-раунде не перепроверено — N2 сверяет);
только ли чтение делает `gate_preflight.run` (поэтому I-gate гоняет его на КОПИИ мира); число мест вида `conductor` до S5
(экз. 1 FV1-13 — достижимость решит N4:s1-s4).

---

## 12. Фикс-раунд t-401 (13.11.2026)

Одна строка на находку критика, адресованную П1-б: что изменено и где, или «почему нет».

| № | Что сделано |
|---|---|
| 3 | `known_red` — один помощник `scripts/tests/known_red.py` П1-а; П1-б только импортирует; поле `known_red` и счёт `ratchet.known_red` из `driver-exits` удалены (§3.2, E11, E12, N1 given, §8, §10a F8) |
| 4 | Требование к П1-а сверено с решением Lead №4: виды по `stages.json` + `overrides`; невидимый выход — `live_only`, не рукописный текст (§4.1, §4.2, N2, E13) |
| 6 | FV1-19 дефект 2 принят в П1-б: проверка C10, строка `s5.window_finish/ref_without_hash` на обеих строках раннеров, «достижимо после FV1-1» (§1 C10, §9.3) |
| 7 | Строки обхода ключуются ключом цен существующей переписи `test_conductor_doors.py`; производитель `dry_exits.driven_keys()`, читатели `test_scenario_dry_1.py` и перепись; изменение переписи (`driven` + вычистка `PINNED_ELSEWHERE` + `covers`) — один коммит узла N4c; `driver-exits` держит только маршруты, стыки, виды без ключа, классы; неверный негатив снят с положительным контролем (§1 AR-15, §2, §3.1, §3.2, N4c) |
| 8 | Id строки обхода = `(<ключ|маршрут|стык|вид>, <вариант>)`, метка — по id строки; отрицательный контроль «соседний вариант без метки краснеет» в DoD N1 (§1 AR-28, §3.3, N1) |
| 9 | C4 разделён: C4г (гейт: слово проводит, запись `passed-by-person.jsonl`) и C4з (запрет хуков: дверь); классы — данные `classes.json` с источником; замер 58/19/25/43/7 с командой; вопросы владельцу Q1, Q2; поиск со слов владельца и контроль (§1, §3.6, E10, E19, E22, §9 F7, §9.2) |
| 10 | Узел N0 (спайк S0→S3, замер, ворота Lead с числами — F12); снимки мира на границах стадий, строки стартуют с копии (§4.3, E16); строки за FV1-1 — `after:FV1-1`; ВРЕМЕННОЙ край E15 (новые красные — своя метка со своей находкой, запрет `after:X` + `known_red: X`); вердикты FV1-2/13/19/20/22 переписаны на «достижимо после FV1-1» (§9.3) |
| 11 | FV1-6 — проверка данных C9 по `asked.options` (ход `rework_stage` с `args.role` = автор); отпечаток C3 несёт круги `dispatch_rounds` и хэши форм; C5 переопределён через вход/выход автора; направление ошибки для C3 и C5 (§3.4, §9.3) |
| 12 | Команды автоматора — из `profile_contract.profile_commands` и строки раннеров, не из брифа; таблица выходов по стадиям с писателями и видами П1-а/`live_only` (§4.1, §4.2, N2 DoD (6)) |
| 13 | Файл на группу: `exits/<group>.json`, `seeds/<group>.json`, `driver-exits/<group>.json`; читатель склеивает, дубль id — красное; owns частей не пересекаются; правка переписи — отдельный последовательный N4c (§3.2, N1 п. 5, N4, N4c) |
| 16 | `STORY_RUN_CLASS=dry` выставляет обходчик во всех своих процессах; проверка распространения (E18) (§4.1, §4.4) |
| 17 | Строки очереди на `test-layers.json` и `scenario_walk.py` с PC4-15, FG7-15, FG7-19 и узлами трёх спек; документы Lead — требования R-L1…R-L9 к узлу «носители П1», не owns спеки (§6 N-L, §8, шапка non-goals) |
| 18 | `session_id: stub-<dispatch>-<n>` (счётчик по диспатчу); функция `run_counters.counters(task_root)`; строку «повтор вопроса» добавляет П1-в (§3.5, §4.4, N2 DoD (4)) |
| 19 | Детектор (калибровочная проверка, один номер) и поле находки «какой слой ниже» — требования R-L4, R-L6 к узлу Lead (§6 N-L, §7 (c)) |
| 23 | Строка оси 18 и вопрос 9 критика — R-L1/R-L2, сажаются тем же коммитом, что N1 (§1 AR-20, §6 N-L) |
| 24 | `test_scenario_dry_1.py` в `TEST_TIMEOUTS` и `slow_tests.json` (owns N3); режим по умолчанию — задача `full`, части — только `dry-story`, двойного прогона нет (N3 п. 7, §10) |
| 25 | Носитель I-gate — поле `gate_ready` результата `gate_preflight` (JSON), не текст «can start» (§1 AR-13, N3 п. 4, §9.3 FV1-7) |
| 26 | Батарея E9 — только на ключах с ответом `person: "answer"` и видах `conductor`/`refusal` (§3.3, E9) |
| 27 | Свидетель: что локально (до минуты), что только CI, с секундами из `slow_tests.json` (§6 «Свидетель») |
| 28 | Подтверждено; правка `architecture.md:192` — требование R-L3 к узлу Lead, не этой спеки (§1, §6 N-L) |
| 36 | FG7-15, FG7-19 названы в §8 с путями и строкой очереди |
| 37 | Срезка цены: E9 сужена (№26), `hook_layer` — один счёт без построчного обхода, N6 после спайка N0; ворота N0 «сузить» (§3.3, E8, §6 N0, N6) |
| 21 (П1-а, затрагивает FV1-22 П1-б) | Записано в вердикте FV1-22: секция `stage_acceptance` во вторичном контракте `s7-analyst-to-scribe.yaml:53` (§9.3) |
| 33 (П1-в, тот же класс) | Строка оси 13 в §7 (b) переписана: сырые читатели — AR-13, не ось 13 |
| 20, 22, 29–32, 34, 35 | Почему нет: адресованы П1-а/П1-в, в П1-б аналога нет (П1-б не читает `TS-`, не держит заполнитель, табло, тайминги, `brief_pack`) |
| 1, 2, 5, 14, 15 | Почему нет: блокирующие П1-а/П1-в; П1-б затронута только через №3/№4/№18 (выше) |

**Новые развилки фикс-раунда:** F10 (как узнать ключ цен вопроса; рек. (а) обёртка-шпион `dry_driver.py`), F11 (где живёт
проверка двери запрета; рек. (б) `refusal_registry --check`), F12 (числа ворот N0; рек. две цифры), F13 (`driven` — ключ
целиком; рек. (а)). Последствия и варианты — §9. **Вопросы владельцу:** Q1, Q2 (§9.2).
