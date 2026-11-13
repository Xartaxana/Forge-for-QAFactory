# t-401 — критик на план: три спеки слоёв П1-а / П1-б / П1-в (одна тема, R13-g)

Дата: 13.11.2026. Критик (Opus). Только чтение; вердикт — вход для приёмки Lead, решение за Lead (роль критика, правило 6).

Под ревью: `docs/tasks/specs/20261113-p1a-writer-reader-round-spec.md` (П1-а), `…-p1b-dry-story-spec.md` (П1-б),
`…-p1v-run-scoreboard-spec.md` (П1-в) — в редакции «решений Lead по развилкам» 13.11; план
`docs/tasks/specs/20261113-plan-fabrika-ne-huzhe-agenta.md`.

Дерево фактов: `RM` = `.claude/worktrees/read-main/ai-packages/qa-factory` (HEAD `2830b08`). Свежесть: `origin/main` после
fetch — `596db4e` (волна 14: только onboarding/readiness/`s0.md`, 7 файлов; ни один факт ниже не затронут).

## Вердикты

| Спека | Вердикт | Блокирующих |
|---|---|---|
| П1-а | fit with fixes | 6 (№1–6) |
| П1-б | fit with fixes — направление верно, но узлы N1–N4 в нынешнем виде не исполнимы без придумывания и не дадут заявленных уловов | 7 (№7–13) |
| П1-в | fit with fixes | 3 (№14–16) |

Межспековые находки — №17–19 (неблокирующие, но с фиксом этого раунда). Неблокирующие по спекам — №20–37.

---

## Блокирующие находки

### П1-а

**1. Метод инвентаря теряет форму `role-to-conductor`; пин `forms == 24` противоречит методу и TESTING.md** (§3.1, §3.4 метод, N1 п. 4).
Спор Lead «24 или 26» решён так: 26 файлов `handoffs/*.yaml` = 24 формы роли + `index.yaml` + `vocabulary.yaml` — число 24
верно. Но метод спеки `forms = [r["contract"] for r in handoff.index()["handoffs"]]  # 24` даёт **23**: прогон
`python -B -c "import handoff; ix=handoff.index(); print(len(ix['handoffs']))"` по RM → `23 23`, `role-to-conductor in hs` →
`False`, `handoff.spec('role-to-conductor')` → 35 полей. Форма помощи роли живёт под ключом `escalation`
(`RM/handoffs/index.yaml:101-108`), а не в `handoffs` (строки `:40-71` — 23 записи). Значит, N1 либо упадёт на собственном пине,
либо билдер «починит» пин до 23 и форма, которую роль заполняет при блокировке, выпадет из круга (AR-21, E10 молча не сработает).
Кроме того, литерал `== 24` — «пин измеренной константы», который `docs/TESTING.md:87` запрещает.
Фикс: множество форм = `index()["handoffs"]` ∪ `{index()["escalation"]["contract"]}`; проверка в обе стороны против листинга
`handoffs/*.yaml` минус `index`, `vocabulary` (без литерала числа); строка итога печатает фактическое число.

**2. Мир N1 пуст, а E11 краснит каждое поле деривера** (N1 п. 3, E11, §3.5 `left_for_code`).
N1 строит мир «из `harness.temp_dir` ОДИН раз» и гоняет `handoff_check.check(fix=True)`; поля из `DERIVERS`/`BY_LEAF`
(`RM/scripts/handoff_check.py:564-609`) читают артефакты мира — напр. `_plan_row_of` читает front matter файла кейса
(`handoff_check.py:429-440`). Артефакты мира пишет `fill_artifact`, но это узел N2. В пустом мире каждый деривер вернёт `None`
→ по E11 красная строка «писатель = деривер», а DoD N1 допускает только красные вида `unfillable`. Билдеру N1 придётся
придумать мир. Фикс: в N1 — круг форм с `fix=False` (поля кода остаются в `left_for_code`, не судятся); круг дериверов (E11)
переносится в N2 после `fill_artifact`, или `fill_artifact` переходит в owns N1 — выбрать одно в спеке.

**3. `known_red` — два носителя и два режима, а не один механизм** (§1.2 C6, N2 п. 7; П1-б §3.2, F8; решение Lead F4/F8).
П1-а: реестр `form-rounds.json` `known_red` (id строки → узел), проверка C6 «множество красных = реестр», новая красная —
«почини или ВНЕСИ строку с узлом» (рост без названной причины). П1-б: поле `known_red` в каждой строке `driver-exits.json` +
счётчик `ratchet.known_red` с дверью `raised_by`. Совпадает только имя ключа; дверь роста разная (AR-20: «a raise is named»,
`RM/design/architecture.md:210-222`), читатели разные. Это ровно класс P31/AR-15, который Lead решением F4 хотел закрыть.
Фикс: один помощник `scripts/tests/known_red.py` (одна форма строки: `id` строки обхода → `FV1-n | id узла`, `raised_by`;
одна функция сверки «красные = реестр, рост только с `raised_by`, позеленевшая без снятия — красная»), которым зовут обе
спеки; узел помощника — первым (в П1-а N2), П1-б N1 его импортирует.

**4. Интерфейс заполнителя не покрывает требований П1-б** (§3.5; П1-б §6 N2 «Требование к спеке П1-а»).
П1-б требует: (а) правки `{поле: значение | ABSENT}` для затравки отказов; (б) покрытие «каждого выхода каждой стадии S1–S9, не
только форм передач». У П1-а: `fill_form(contract, ctx, verdict, variant)` без правок; `fill_artifact` — пять видов (`case`,
`plan_md_row`, `plan_json_row`, `manifest_row`, `test_file:<lang>`). Реестр требований, `run-report.json`, черновики багов,
отчёт S8, улики S6 и т. д. не заполняются никем → заглушка П1-б напишет их руками (причина A плана) или билдер придумает
писатель. Фикс: Lead выбирает одно — (а) П1-а N2 расширяет `fill_artifact` перечнем выходов из `references/stages.json` (список
в спеке, по строке теста на вид) и добавляет `overrides`; или (б) П1-б сужает главный проход до стадий, чьи выходы покрыты, а
прочее — `live_only` с храповиком. Без выбора П1-б N2 не стартует.

**5. Счётчик рукописных входов (C7, F9 (а)) — «пин исходника», который TESTING.md запрещает** (§1.2 C7, N2 п. 8, F9).
`docs/TESTING.md:86` (таблица «Что не пишется»): «подсчёт вхождений регулярки в коде … структурный инвариант — одна строка в
общем храповике (`dup_ratchet`, `lint_ratchet`, `test_driver_layers`), не свой тест на узел». C7 считает совпадения
`literal_shape` по `scripts/tests/*.py` своим тестом. Дизайнер назвал это условием (F9 (б)), Lead выбрал (а) без слова
владельца; потолок TESTING.md — слово владельца 10.11 (CLAUDE.md правило 11 «SCOPE CEILING»). Фикс: F9 (б) — строка в
`tools/lint_ratchet.py` (шаблоны `literal_shape` читаются из `form-rounds.json`), либо вопрос владельцу в том же списке, что F2.

**6. Улов FV1-19 «дефект 2» (C4) опирается на читателя, которого нет как функции** (§4.2 строка `agree: obligation_refs`,
§4.3 FV1-19, N2 п. 6). Проверка хэша ссылок живёт внутри метода контроллера: `Controller._s5_v2_collect`
(`RM/scripts/controller.py:7247`), строки `:7293-7302` («coverage v2 instance requires unique obligation_refs with exact
hashes»), на объектах окна `window["instances"]`, построенных из манифеста, с утверждённым планом `_plan_document`. Это не
`module:function` из реестра `readers`: чтобы «подать значение», билдеру нужен контроллер с состоянием или подмена метода —
второе есть класс C плана (лямбда вместо шва). Фикс: назвать вход (публичная операция контроллера в мире N2 с записями плана и
окна — с перечнем, что кладётся в мир) или перенести строку C4 для FV1-19 в П1-б (финиш окна в сухой стори) и поправить
вердикт §4.3 на «дефект 2 — П1-б».

### П1-б

**7. Новая перепись вопросов дублирует существующую и опирается на неверный негатив** (§3.1 строка «Вид вопроса → ключ цен —
соответствие не найдено», §3.2, N1 п. 1, 3, 7).
Перепись ключей вопросов в обе стороны уже есть: `RM/scripts/tests/test_conductor_doors.py:626` `QUESTION_SITE_RE` по литералам
`closed_question("<ключ>")`/`priced_section(...)`, `census_problems` (`:660-673`: «raised by the code, no row in the data», «a row
in the data, no site raises it», «raised, but neither driven here nor pinned elsewhere»), `PINNED_ELSEWHERE` (`:633-659`) — файл в
`keep`, слой `register` (`test-layers.json:661-664`). Соответствие «место → ключ цен» в коде есть литералом:
`driver_dispatch.py:3055,3135` (`s5.repair_limit`), `:3761-3762` (`exit.resume_limit`, `…_halted`); докстринги прямо называют
«the census of question ids reads it» (`driver_dispatch.py:3109,3759`, `driver_machine.py:2133`, `driver_stage_s7.py:480`).
Негатив спеки — не проверка (поиск велся по `Person(`, а не по `closed_question(`). Вторая перепись `driver-exits.json`
с `kinds.price_keys` — две дороги к одному множеству (AR-15, P31, правило 19 роли). Показательно: `PINNED_ELSEWHERE` указывает
на карантинные файлы (`exit.resume_limit` → `test_story_run_exit_limit.py`, который в `quarantine`), — ровно дыра, которую
сухая стори должна закрыть. Фикс: строка обхода ключуется КЛЮЧОМ цен из существующей переписи (вид `Person` — только для
маршрутов без ключа); строки сухой стори становятся множеством `driven`/`PINNED_ELSEWHERE` этой переписи; `driver-exits.json`
держит только `reach`/`seed`/`why_unreached` для того, чего перепись не знает (маршруты `KNOWN_REFUSALS`, стыки).

**8. `known_red` на уровне вида маскирует другие варианты того же вида** (§3.2 схема, §3.3 «строка = (вид, вариант)»).
Схема: `kinds.<kind>.known_red: "<FV1-n>"` — одно значение на вид; обход идёт по паре (вид, вариант). FV1-13 — четыре экземпляра
в видах `conductor` и `exit_limit` с разными вариантами (§9 таблица вердиктов). Пока вид помечен, новый красный в соседнем
варианте того же вида читается «ожидаемым» — неизвестное становится проходом (AR-28). Фикс: `known_red` — по id строки
обхода `(<ключ|маршрут>, <вариант>)`, в общем помощнике №3.

**9. C4 в решении F7 (а) не ловит причину B плана** (§1 C4, E10, F7; план §2 строка B).
План называет дефектом «никакое слово не снимает отказ — `test_row_fields.py:370-378` (против P13)»; на RM:
`test_row_fields.py:366-374` — запись слова `*`, `row-fields`, `row-fields-missing`, `manifest` «does not lift the finding».
C4 (а) засчитывает «перевод в другое состояние с названной дверью»; у `row-fields-missing` дверь есть («допиши поля»,
`window_record.FRAGMENT_DOOR`) → строка зелёная, дефект не пойман. P13 говорит о ГЕЙТЕ («Слово человека проводит фабрику через
любой гейт»), FR-57/P15 — о ЗАПРЕТЕ. Решение F7 слило оба. Фикс: C4 по классу отказа — (i) гейт (проверки `stage-joints.json`
`exit:`/`window:`/`detector:`, вопросы гейтов, отказы выхода стадии): слово проводит и записано в `passed-by-person`; (ii) запрет
слоя хуков (`refusal_registry` `override: ""`, 58 строк): дверь (FR-57). Если Lead считает, что (i) меняет замысел P13 для
каких-то проверок, — это вопрос владельцу (правило 11a), не решение Lead.

**10. Реализуемость не измерена; главный проход заканчивается на FV1-1; посев «от S0 на каждую строку» без снимков**
(§4, §5 E6, F6, N3 DoD, §9 вердикты). (а) Ни один существующий тест не проводит драйвер S0→S9 с формами: квартет
`test_story_run_*` выключает формы (`story_run_common.py:201`) и стоит 15–290 с на часть (`RM/scripts/slow_tests.json`:
`test_story_run_s0.py` 289.8, `…_s6.py` 218.8); реплей готовых историй — 22–110 с. (б) DoD N3: «проход до S9 или до первой
строки `known_red`»; сама спека: «сухая стори … встанет на пустой области S5; `known_red: FV1-1`» (§9, после таблицы) — значит
S6–S9 на main главным проходом недостижимы, а улов FV1-22 («главный проход S7», §9) и группа N4 `s6-s9` на сегодняшнем main не
краснеют по заявленному механизму. (в) Рецепт `seed` = «прогон драйвера до нужной границы» (§4) для ~190 строк без снимка мира на
границах стадий — время не ограничено ничем, кроме будущего капа. (г) ВРЕМЕННОЙ край не назван: когда починка FV1-1 снимет метку,
проход впервые пойдёт дальше S5, и все новые красные S6–S9 лягут на узел FV1-1. Фикс: узел N0 — спайк: главный проход S0→S3 с
формами на заглушках, замер секунд, решение Lead «продолжать / сузить» до N2; снимок мира на каждой границе стадий, строки
обхода стартуют с копии снимка; для строк за FV1-1 — посев снимка через затравку FV1-1-состояния настоящим писателем или
явная пометка «достижимо после FV1-1»; поведение узла починки FV1-1 при новых красных ниже по течению — в §5.

**11. Улов FV1-6 не различает дефект и починку** (§9 строка FV1-6, §3.4).
Механизм: `restart` → критик-заглушка снова `reject` (из строки) → форма тестера та же → отпечаток тот же (C3) → третий раз (C5).
Но дефект FV1-6 — нет ВАРИАНТА «раунд тестеру со словами критика» (находка `…/20261112-s2-net-dveri-vernut-rabotu-testeru-so-slovami-kritika.md:19-22`).
После починки `restart` остаётся (а вердикт критика задан строкой) — строка по-прежнему красная; метку снять нельзя. Шире:
заглушки детерминированы («одинаковый вход → одинаковые байты», N2 DoD), а отпечаток нормализует id диспатча (§3.4) — любой
законный раунд переделки с той же формой выглядит «состояние не изменилось». Фикс: FV1-6 — проверка данных на предложенных
вариантах вопроса `stage_review_exhausted`: есть ли ход с исполнителем = роль-автор (ключ/ход из `question-prices.json`/
`conductor-actions.json`); в отпечаток C3 — счётчики раундов/хэш форм диспатча, чтобы новый раунд был новым состоянием.

**12. Заглушка противоречит своему AR-29 DoD и не имеет перечня выходов** (§1 AR-29 «N2 DoD: нет ветвления по тексту брифа, кроме
закрытых меток», §4 таблица «роль-заглушка вызывает команды, названные её брифом», N2 п. 1 «выходы S1–S9»). Вызвать «команды,
названные брифом», можно только разбирая бриф. Перечня выходов стадий, которые пишет заглушка, нет (см. №4). Фикс: команды
автоматора — из профиля (`profile_contract.profile_commands`, ось 30) и строки таблицы раннеров F5, не из брифа; перечень
выходов по стадиям — таблицей в спеке со ссылкой на `references/stages.json`.

**13. Параллельные части N4 владеют одними файлами** (N4 owns: `seeds.json`, `driver-exits.json` у каждой части).
CLAUDE.md правило 4: параллельные диспатчи объявляют непересекающиеся owns; «разделы внутри файла, интегратор сливает» — это
конфликт JSON-слияния, переложенный на интегратора. Фикс: файл на группу (`stories/dry-1/seeds/<group>.json`,
`driver-exits/<group>.json`, читатель склеивает) или части последовательно.

### П1-в

**14. Поле `gate` (W2) не имеет структурного источника; «каждый вызов передаёт токен, который уже знает» — неверно** (§2 W2,
§0 C-5, N2, норма N-gate, K6). Вызывающие знают только текст отказа: `Refusal` несёт `text`, `findings`, `window_findings`,
`title`, `close` — id проверки нет (`RM/scripts/driver_core.py:117-136`); `resume_with` строит причину из текста
(`driver_dispatch.py:2077-2080`), классифицируя регулярками `RESUME_CLASSES` (`driver_dispatch.py:142-148, 155-175`);
`row-fields-missing` существует только тегом строки находки (`s5_precheck.py:3765` `ROW_FIELDS_TAG`). Норма N-gate («возвраты
одного гейта ≤ 16») и K6 — главный заказ плана (§3 П1-в п. 4: `row-fields-missing`) — без этого не считаются. Фикс: отдельный
узел-производитель структурного id проверки (выход `exit_gate`/`s5_precheck` → поле `Refusal`, owns названы, перечень мест
поднятия) ДО N2; либо явное решение, что `gate` = имя строки `KNOWN_PATTERN`/`RESUME_CLASSES` (код классифицирует СВОЙ текст —
это не FR-12 про слова человека/роли), тогда `s5_precheck:row-fields-missing` недостижим и норма N-gate переформулируется.

**15. Пара требований в конфликте: строка трения = значение `friction.story_friction`, а табло отказывает ключам денег**
(§1.1 AR-12 «N4 DoD: the friction row is the value `friction.story_friction` returns (identity test row)»; §4.2 «refuses to
write a key matching `usd`, `cost`, `price`»). `story_friction` возвращает `priced_cost`, `fric_cost`
(`RM/scripts/friction.py:370-390`) — тождество внесёт в табло деньги (P18) или K1 откажет записи. Фикс: строка = доли и счёты
ходов (`turns`, `fric_turns`, `kinds`), ключи денег отбрасываются поимённо; тест — «в строке нет ключа денег» и «доли равны».

**16. Источник `run_class` (W1) не назван** (§2 W1 `"run_class":"live|dry|smoke"`, §7.9 «a dry scoreboard is never compared with a
live one»). В пакете сигнала нет: Grep `run_class|STORY_RUN_DRY` по `RM/scripts` без учёта регистра — 0; положительный
контроль той же формы `STORY_RUN_CLAUDE` — 41 вхождение в 23 файлах. Билдер N1 будет угадывать (по `STORY_RUN_CLAUDE`?), а на
этом стоит инвариант §7.9 и ось 34 (одна дорога dry/live). Фикс: назвать источник (ключ конфига или переменная, которую
выставляет обходчик П1-б и дымовой прогон П2-г), в обеих спеках, с поведением при отсутствии (`live` или `unknown` — выбрать).

---

## Межспековые находки (фикс этого раунда)

**17. Общие файлы трёх спек без порядка** (D). `test-layers.json`: П1-а N1, N2; П1-б N3; П1-в N4; плюс `package-ci/4`
PC4-15/17/18 и `forge/7` FG7-15/FG7-19 (`plans/piles/forge/batch-7-vhodyashchie-4.md:38,42`, обе «ожидает», owns
`scenario_walk.py`, `test-layers.json` — П1-б §8 их не называет). Документы Lead: `docs/SIBLING_MAP.md` (П1-а N3, П1-б N5,
П1-в N8), `design/architecture.md` (П1-а N3 AR-10/20/22; П1-б N5 `:192`; П1-в N8 AR-12), `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md`
(П1-б предлагает новую проверку, П1-в N8 — «check 45»: два кандидата на один номер). Фикс: один узел Lead «носители П1» на
три спеки; строка `очередь:` для `test-layers.json` между узлами трёх спек и с PC4-15/FG7-15/FG7-19.

**18. Счётчики, которых П1-в ждёт от сухой стори, П1-б не производит** (D). П1-в §7.9: строки `journal_run` с `session_id`
`stub-…`, `resume_kind`, `gate`, строки `process` с `run_class: dry`. П1-б: о префиксе `stub-` в ответе заглушки молчит; `run_class`
— №16; П1-б §3.5 просит у функции табло «повторы», в таблице строк П1-в §2 такой строки нет. Фикс: П1-б N2 — заглушка отдаёт
`session_id: stub-<dispatch>-<n>`; П1-в §2 — строка «повтор вопроса» или П1-б убирает требование; имя функции —
`run_counters.counters(task_root)` в обеих.

**19. Чего план просит, а не покрывает ни одна спека** (D). План §6: (а) вопрос критика «подан ли читателю выход сегодняшнего
писателя — приложенный прогон П1-а»; (б) поле находки живого прогона «какой слой ниже должен был поймать». Обе вещи П1-а §6 (c) и
П1-б §7 (c) называют СВОИМ детектором утечки, но узла, который их создаёт, нет ни в одной спеке (П1-а axis 1: «отдельный узел
Lead»). Механизм с незарегистрированным детектором — «пожелание» (CLAUDE.md правило 10 (c)). Фикс: оба пункта — в узел №17.

---

## Неблокирующие находки

П1-а:
20. Негатив «читатели `report_facts`, `validate_artifacts` не найдены по шаблону `TS-`» (§4.3 FV1-14, §8.1) — промах шаблона:
`validate_artifacts.py:806-808` — `r[0].startswith("TS-")` и отказ «has no TS-* rows»; ещё `factory_dashboard.py:711` («TS-n ->
level»). Шаблон `PLAN_ROW_RE|TS-\\d|TS-\(|\(TS-` не ловит литерал `"TS-"`. Фикс: оба — в начальный реестр `readers`.
21. FV1-22: секция `stage_acceptance` для приёмки S6 есть во ВТОРИЧНОМ контракте аналитика (`handoffs/s7-analyst-to-scribe.yaml:53`
«Acceptance of the runner's handoff (X7-6), owed on concerns»), а `contract_of('S7','qa-failure-analyst')` → `s7-analyst-to-automator`
(прогон). Красная строка верна, но её смысл — «читатель получает форму диспатча, секция живёт во вторичной» — стоит записать: от
этого зависит направление починки FV1-22.
22. Пара требований заполнителя не разрешена: «значение из подсказки ДОСЛОВНО» против «id, выпущенный одной формой, цитируется
тем же значением» (§3.5). Шаблон кейса велит `Plan row: TS-n` (`references/artifact-contract.md:63`), `ctx.minted` даёт `P-1`.
N2 п. 1 молча выбирает minted. Назвать приоритет (правило 11).
23. AR-20 «новый храповик входит в ось 18 и вопрос 9 тем же коммитом» (`architecture.md:222`): `known_red` и счётчик создаёт N2,
ось и вопрос — N3 «сажается после N2». Тот же класс в П1-б (ось 18 «в N1», но owns N1 без SIBLING_MAP/critic-diff-brief) и П1-в
(`norms.json` в N6, ось 18 — N8). Фикс класса: коммит, создающий храповик, несёт строку оси и вопроса (Lead сажает вместе).

П1-б:
24. `test_scenario_dry_1.py` нужен в `TEST_TIMEOUTS` (`RM/scripts/selftest.py:110-115`) и `slow_tests.json`; `selftest.py` не в owns.
Не сказано, идёт ли строка `keep` в задачу `full` канона (двойной прогон с задачей `dry-story`) — выбрать.
25. Носитель I-gate (C6) не назван: «запись репетиции гейта на диске». Репетиция печатает текст «… can start: yes/no»
(`gate_preflight.py:6081, 6237`); чтение этого текста — разбор своей прозы. Назвать структурный носитель или поле результата.
26. Батарея E9 приложена к каждому виду (§3.3) — строк сотни; нужна только на ответах, несущих слова к роли/дирижёру (цена, №37).
27. Свидетель N3 не «до минуты»: правка `scenario_walk.py` по коду `witness_for` называет все сценарные тесты
(`scenario_walk.py:914-915`, ~200 с по `slow_tests.json`) плюс сухую стори; назвать, что гоняется локально, что только CI.
28. Факт `architecture.md:192` «`NO_MOVE_BASELINE_MAX = 102`» против `audit_factory.py:1715` `= 55` — подтверждён; правка в N5 верна.

П1-в:
29. Негатив «`resume_reason` text stays for people; no code reads it» (§2 W2) неверен: `retro_numbers.py:1721-1725` группирует по
тексту причины (`resume_metrics`). Сказать прямо: до узла делегирования (F3) это второе определение переделок (AR-15), с указателем.
30. Дубль читателя: `driver_timing.report(task_root)` (`driver_timing.py:241-287`) уже считает шаги кода, «unattributed» по хопам и
битые строки через `_rows` (`:201-219`). T4/T5 и R1 «`read_timings`» — брать `report`, не второй разбор.
31. Добавка Lead (время учётных и отказанных вызовов по сессии) §2 НЕ покрыта: `friction` считает ходы-трения, не время, и не
считает успешные учётные вызовы (`friction.py:7-15`). Пункт фикс-раунда: строка, источник (транскрипт, время `tool_use`→
`tool_result`), классификация скриптов — данными (FR-13).
32. C-8 устанавливается: копия `experiments/mybooks/factory-vs-free-agent/runs/factory-out/state/driver-runs.jsonl` закоммичена
(`git ls-files`; коммит `4e00ed7`), в ней 120 вхождений `total_cost_usd` — деньги в файле репозитория сегодня (P18). Находка
вне спеки, но спека должна писать «установлено», не «не установлено».
33. Ось 13 в §9 (b) — «текст диспатча»; сырые читатели `driver-questions/answers` — это AR-13, не ось 13. Переписать строку.

Пересечения (G), пропущенные спеками:
34. П1-в N3 `brief_pack.py (build)` + `test_brief_pack.py` — те же файлы, что `roles-context/2` RC2-1/RC2-2 (owns
`brief_pack.py`, `test_brief_pack.py`, «ожидает») и `live-run-fvf/1` FV1-4 (`brief_pack.py`). П1-в §10 их не называет.
35. П1-в N2 правит места вызова `resume_reason=` в `driver_dispatch.py` (`:548, 577, 1035, 2079, 3625`) и `driver_machine.py:549` —
файлы узлов `live-run-fvf/1` FV1-2/3/13/20/22 (`driver_dispatch.py`) и FV1-6 (`driver_machine.py`); П1-в N1 — `Driver.run` в
`driver_machine.py`. Нужны строки `очередь:` (план §4: починки FV1 идут после краснения слоёв — порядок совместим, но не записан).
36. П1-б §8 не называет `forge/7` FG7-15/FG7-19 (см. №17).

Цена (F):
37. Повторяющаяся цена: П1-б — главная (≈190 строк × процесс драйвера + батарея E9 + Node/браузер в образе CI для N6). Что можно
срезать без потери заявленного улова: батарею E9 — до ответов, несущих слова (FV1-3/4/13 экз. 2 остаются); строки `hook_layer`
(102) не обходить построчно — один счётчик; N6 (TS/Playwright) сохранить, но после спайка №10. П1-а — дёшево (до 10 с, без
процессов), но обещание «≤ 10 с» не измерено на ~23×4×6 вызовах `handoff_check.check` — замер в отчёте N1 обязателен. П1-в —
дёшево в CI; правка Lead `norms.json` на каждый прогон (F6 (а)) — приемлема; ничего лишнего не вижу, кроме дубля №30.

---

## Ответы по ключам

**A. Факты по следу.** Проверено по RM (≥ 6 на спеку, из них ≥ 2 негатива с контролем):
- П1-а: `s3-strategist-to-designer.yaml:52` `<P-n, …>` — да; `contract.py:3052` `(TS-\d+)` — да; `s5_precheck.py:79` — да;
  `handoff_check.py:439` — да; `brief_pack.py:66` `(\S+)` — да; `case-markers.json` только `pytest` — да; `artifact-contract.md:63`,
  `artifact-contract-plan.md:46` `TS-n` — да; `window_record.py:226-244` ссылка без хэша проходит — да; финиш требует хэш —
  да, но в `controller.py:7293-7302` (№6); негатив «`stage_acceptance` нет в `s7-analyst-to-automator.yaml`» — верен (Grep -i,
  контроль: 5 других контрактов, `vocabulary.yaml`); `contract_of('S7','qa-failure-analyst')` = `s7-analyst-to-automator` (прогон);
  `test_field_producers.py` — keep `data_join` (`test-layers.json:1664-1676`) — да; языки `detectors.json` {csharp, java,
  typescript}+{python} — да. Неверно: метод «24» (№1); негатив про `validate_artifacts` (№20). 24 vs 26 — ответ в №1.
- П1-б: `story_run_common.py:201` — да; `scenario_walk.py:40` — да; 25 литеральных видов `Person("…")` — да (`grep -ohE`, `sort -u`);
  `KNOWN_REFUSALS` 21 — да (импорт); `question-prices.json` 61 ключ / 188 ответов — да; `stage-joints.json` 43 — да;
  `refusal_registry` 102 / 58 `override: ""` — да; `audit_factory.py:1715` = 55 — да; `DECISION_CHARS_MIN = 240` — да; 16/20
  `test_story_run_*` quarantine/keep — да; `test_story_run_s0.py:1140` — да. Неверно: негатив «соответствие вид → ключ цен не
  найдено» (№7; контроль — `closed_question("s5.repair_limit"` найден Grep той же формы).
- П1-в: `driver_runner.py:728-747` единственный писатель таймингов — да; `driver-timings.jsonl` в живой папке плеча — да (292 строки);
  `brief_pack.py:54`, `:4535` `bytes`/`budget_bytes` — да; `driver_journal.read_rows` молча пропускает битые строки
  (`:356-377`) — да; `driver_machine.py:1784-1790` форма `stopped_by_person` — да; `driver_runner.py:901-910` строка исхода — да;
  `retro_numbers.py:20-28` — да. Неверно: негатив «код не читает `resume_reason`» (№29; контроль: Grep `resume_reason` нашёл писателя
  `driver_runner.py:910` и читателя `retro_numbers.py:1721`); W2 «токен уже известен» (№14). Негатив «`run_class` нет» — мой, с
  контролем (№16).

**B. Архитектура и принципы.** П1-а держит AR-22/AR-10/AR-13/AR-29; ломает AR-20-порядок (№23), AR-15/P31 по `known_red`
(№3), потолок TESTING.md (№5, №1). П1-б: AR-17 держит (шов — граница процесса, без подмены методов); AR-15/P31 ломает вторая перепись
(№7) и `known_red` (№3, №8); AR-28 — маскировка вида (№8); P13/FR-57/FR-4 — C4 (№9); AR-29 — противоречие заглушки (№12);
заглушки и суждение: вердикт критика и выбор дирижёра заданы строкой — это корректно по AR-29, но делает FV1-6 неразличимым (№11).
П1-в: P27/AR-29 по строкам качества — держит (суждение в `judgment.yaml`, K1 — форма, K6 — только по строкам Lead); P18 —
схема без денег держит, но конфликт №15; FR-12 — держит, если №14 решён без разбора текста; AR-13 — дубль №30; AR-15 — второе
определение переделок до делегирования (№29); FR-28 — строки вариантов есть (N4, N6); AR-20 — K5 с `raised_by`+`word` согласно,
порядок — №23. FR-12 нигде не нарушено фразовыми списками по словам человека/роли.

**C. Реализуемость.** П1-а FV1-1/14: прямой круг `Plan row: P-1` → `CASE_PLAN_ROW_RE`/`PLAN_ROW_RE`/`_plan_row_of` → `""`/`None`
— покраснеет механически, механизм верен (при №2 и №22). FV1-19 дефект 1: `test_file:<lang>` без формы маркера → `Unfillable` →
красная — верно и различает починку. FV1-19 дефект 2 — не реализуем как описан (№6). FV1-22 поля приёмки: заполненная
`s7-analyst-to-automator` с `concerns` → `stage_acceptance_from_form` берёт секцию `stage_acceptance` (`acceptance.py:1559-1590`)
→ `failure_class` None → отказ в `stage_acceptance_errors` (`:1331-1365`) — покраснеет; `inputs_read[-1]` → `reviewed_author_dispatch`
`""` (`stage_done.py:939-955`) — покраснеет при состоянии с диспатчем S6 в мире. П1-б: FV1-6 — неразличим (№11); FV1-13 экз. 1
(жетон → вызов дирижёра после жетона) — механика верна, но состояние достижимо только при FV1-1-пустом S5 (№10); FV1-22 петля —
различима, но на main главным проходом недостижима (№10). Сухая стори «минуты в CI» — не установлено ничем; аналоги — сотни
секунд на часть (№10). Зависимость от живого суждения: FV1-20 — честно помечен частичным; FV1-2 — по цитате владельца (F9), не
суждение. П1-в: время шагов кода — измеримо (писатель на main, данные плеча есть); возвраты по гейту из структурного поля — нет
источника (№14).

**D. Согласованность.** Интерфейс заполнителя — №4; счётчики для табло — №18; общие файлы и порядок — №17; непокрытое из плана —
№19. Противоречий в решениях Lead между спеками, кроме `known_red` (№3), не нашёл; F2 (TESTING.md) задан владельцу один раз на
обе спеки — согласно.

**E. Узлы для более слабой модели.** «Придумать подход» придётся в: П1-а N1 (мир для дериверов, №2), N2 п. 6 (C4, №6), N2 п. 8
(`literal_shape` по каждому читателю — что считать рукописным входом, не определено; плюс №5); П1-б N2 п. 1 (выходы S1–S9, №4/№12),
N3 п. 4 (носитель I-gate, №25), N4 (грамматика `seeds.json` не задана — формат рецепта, шаги, как ссылаться на снимок; №10, №13),
N1 п. 7 (если не принять №7); П1-в N1 (`run_class`, №16), N2 (`gate`, №14), N4 (строки добавки Lead, №31). ВРЕМЕННЫЕ края:
П1-а E16 — назван; П1-б E12/E13 — названы, но не назван край «после снятия FV1-1» (№10); П1-в §7.6 — назван. ПОЗИЦИОННЫЕ: П1-в W1
(конец в `finally`, инвариант формы строки) — назван хорошо; П1-в W3 (в `build`, не `main`) — назван. Свидетели узких путей: П1-а —
да; П1-б N3/N4 — не до минуты (№27); П1-в — команда верна, но `--witness-for driver_machine.py` печатает десятки keep-файлов
(свойство обходчика сегодня, FG7-19 его чинит — не дефект спеки).

**F. Цена и трение.** №37; плюс №7 (лишняя перепись) и №30 (лишний читатель) — срезать.

**G. Пересечения.** №34, №35, №36, №17. Проверено: `package-ci/4` PC4-12 (П1-б только импортирует — верно), PC4-2/PC4-5 (резка за
фасадом — верно у П1-а, П1-б), PC4-15/17/18 (`test-layers.json` — названо П1-а/П1-б, но без порядка между тремя спеками);
`execution-report/2` DC1-24 и CD1-* — П1-в назвал верно; `speed-cost/6` SC6-2 — назван; `cost-dashboard/1` закрыта (`batch-1…:3`).

## Полнота класса (правило 5)

Класс «одна сущность — два носителя/два режима» найден трижды: `known_red` (№3, №8), перепись вопросов (№7), чтение таймингов
(№30); плюс «AR-20 порядок оси 18» во всех трёх спеках (№23). Оси карты: 18 (храповики — №3, №5, №23), 34 (одна дорога — №7,
№16), 13 → AR-13 (№33). Поиск шире карты не делал.

## Дублирование и согласованность (вопрос 6 брифа)

Найдено: №7 (вторая перепись ключей вопросов против `test_conductor_doors.py`), №3 (два `known_red`), №30
(`driver_timing.report` против `read_timings`/`read_rows_counted`), №29 (второе определение переделок). Искал: Grep
`closed_question`, `resume_reason`, `run_class`, `TS-`, чтение `driver_timing.py`, `test_conductor_doors.py:600-673`.

## Качество кода (вопрос 7 брифа)

Кода нет (план). По спекам: пины литералом (№1), счётчик вхождений (№5) — против TESTING.md; прочее — none found.

## Одно действие — одна дорога (вопрос 12 брифа, P31)

Исключений языка/проекта без строки данных нет: П1-а языки из `detectors.json`, П1-б F5 (а) TS и Python одной дорогой, П1-в одна
дорога двух плеч. Два носителя одного действия — №3, №7 (фикс этого раунда, не очередь).

## След

Прочитано: план (целиком); три спеки (целиком); `RM/handoffs/index.yaml:1-120`, `s3-strategist-to-designer.yaml:52`,
`s4-designer-to-case-critic.yaml:48-50`, `s7-analyst-to-automator.yaml:60-72`, `vocabulary.yaml:20-30`; `RM/scripts/handoff.py:30-36`
+ def-список; `handoff_check.py:429-441` + def-список; `contract.py:3052,3615-3620`; `s5_precheck.py:79,3745-3762`; `brief_pack.py:54,
60,66,4530-4570`; `window_record.py:176-190,222-246`; `controller.py:7270-7325`; `stage_done.py:935-1050`; `acceptance.py:1331-1365,
1559-1590`; `references/stages.json:205-220`, `case-markers.json`, `artifact-contract.md:60-65`, `artifact-contract-plan.md:44-47`,
`detectors.json` (ключи); `scripts/tests/scenario_walk.py:1-80,833-935`; `test-layers.json:1660-1680` + разделы; `slow_tests.json`;
`selftest.py:103-115`; `story_run_common.py:5-8,54-75,199-203,233-236`; `test_conductor_doors.py:615-673`; `test_row_fields.py:366-380`;
`test_story_run_s0.py:1138-1141`; `test_brief_pack.py:2428-2440`; `no_move.py:40,161,175,255-290,589`; `driver_machine.py:1765-1792,
3314-3321`; `driver_core.py:100-140`; `driver_dispatch.py:142-175,2065-2085` + Grep `resume_reason`; `driver_runner.py:722-750,895-912`;
`driver_timing.py:1-35,193-290`; `driver_journal.py:356-377` + def-список; `retro_numbers.py:20-28,1712-1735`; `friction.py:1-40,
337-400`; `audit_factory.py:1715`; `design/architecture.md:140-157,192,210-222`; `docs/TESTING.md:40-130`; `docs/SIBLING_MAP.md`
(заголовки осей); находки FV1-1, FV1-6, FV1-13, FV1-22 (выдержки), `batch-1-live-run-fvf.md` (таблица узлов, «Ход»); шапки пачек
`package-ci/4`, `roles-context/2`, `execution-report/2`, `speed-cost/6`, `cost-dashboard/1`, `live-runs/2`, `thinking-roles/5`,
`forge/7` (строки FG7-15, FG7-19); папка состояния плеча (листинг, счёт строк); `git ls-files` копии прогона.

Прогоны (контрольные, чтение): `handoff.index()` → 23 записи `handoffs`, `role-to-conductor` вне их, 35 полей; сумма полей 23
контрактов — 1215; `contract_of('S7','qa-failure-analyst')` → `s7-analyst-to-automator`; `consumer_of('S6')` → `qa-failure-analyst`;
`KNOWN_REFUSALS` 21; цены 61/188; стыки 43; реестр отказов 102/58; `_closure(['story_run'])` — 227 из 279 скриптов (против 201 у двери
`gate`); `scenario_walk.py --witness-for test_field_producers.py test-layers.json` и `--witness-for driver_machine.py brief_pack.py`;
`git merge-base --is-ancestor` для `8eb20e4`, `bb2bd10`, `5971ac0` → не в main (дефекты FV1-1/FV1-13 экз. 3 на дереве на месте).

Не проверено: время одного прохода `handoff_check.check` (обещание П1-а «≤ 10 с»); `references/slices/*/handoff-keys.md` (11 страниц);
`runs/blind-eval.md`; `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md` (номер последней проверки — со слов П1-в); `plans/builder-rules.md` 7b
(форма свидетеля — по CLAUDE.md правило 4).

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "1 P1a: inventory method handoff.index()['handoffs'] yields 23, misses role-to-conductor (escalation key, index.yaml:101-108); pin forms==24 contradicts method and TESTING.md measured-constant row",
    "2 P1a: N1 world is empty while E11 reds every deriver field; fill_artifact is in N2",
    "3 P1a+P1b: known_red is two carriers with two raise doors (set equality with free add vs count ratchet with raised_by) - one helper required (AR-15, P31, AR-20)",
    "4 P1a/P1b: filler interface lacks overrides and stage outputs S1-S9 that P1b N2 requires",
    "5 P1a: own hand-input counter C7 (F9 a) is the source-pin TESTING.md forbids; needs lint_ratchet line or owner word",
    "6 P1a: FV1-19 defect 2 reader is inline in Controller._s5_v2_collect (controller.py:7247,7293-7302), not a callable reader",
    "7 P1b: driver-exits census duplicates test_conductor_doors.py census (QUESTION_SITE_RE :626, census_problems, PINNED_ELSEWHERE); negative 'kind to price key mapping not found' is wrong (closed_question literals driver_dispatch.py:3055,3761)",
    "8 P1b: known_red per kind masks sibling variants of the same kind (AR-28)",
    "9 P1b: C4 as decided (F7 a) passes row-fields-missing (test_row_fields.py:366-374) because a door counts; P13 gates vs FR-57 bans must be split",
    "10 P1b: feasibility unmeasured; main pass stops at FV1-1 at S5 so S6-S9 rows incl. FV1-22 loop unreachable on main; per-row seeding from S0 without snapshots; temporal edge after FV1-1 fix unnamed",
    "11 P1b: FV1-6 catch is non-discriminating (scripted verdict + deterministic stub + id-normalized fingerprint)",
    "12 P1b: stub must call commands named by its brief while its AR-29 DoD forbids branching on brief text; no enumerated stage outputs",
    "13 P1b: parallel N4 parts own the same files seeds.json and driver-exits.json",
    "14 P1v: W2 gate field has no structured source; Refusal has no check id (driver_core.py:117-136), resume_reason built by RESUME_CLASSES regex (driver_dispatch.py:142-175)",
    "15 P1v: friction row identity with friction.story_friction (returns priced_cost, fric_cost) conflicts with the no-money key refusal",
    "16 P1v: run_class source unnamed (no signal in package; grep 0, control STORY_RUN_CLAUDE 41)"
  ],
  "fixes": [
    "forms = index handoffs plus escalation contract, two-way against handoffs/*.yaml listing, no literal count",
    "N1 rounds forms with fix=False; deriver round moves to N2 after fill_artifact (or fill_artifact joins N1)",
    "one scripts/tests/known_red.py helper and one ledger row shape keyed by walk-row id with raised_by, used by P1a and P1b",
    "Lead picks: extend fill_artifact to the enumerated stages.json outputs plus overrides, or narrow the dry main pass with live_only ratchet",
    "C7 as a lint_ratchet line, or owner question with F2",
    "name the public controller entry and world for the C4 FV1-19 row, or move it to P1b and correct the 4.3 verdict",
    "key exit rows by question-prices keys from the existing census; dry rows become its driven/pinned set; driver-exits keeps only routes and joints",
    "known_red per (key or route, variant) row",
    "C4 by refusal class: gate passes on the word and is recorded in passed-by-person; hook-layer ban needs a door; owner question if Lead reads P13 otherwise",
    "add spike node N0 (S0-S3 with forms on, measured), stage-boundary snapshots reused by rows, state FV1-1-after behaviour and FV1-22 reachability",
    "FV1-6 as a data check on offered options (an executor equal to the author role); fingerprint carries round counters or form hashes",
    "automator stub commands from profile_contract and the runner row, not from the brief; table of outputs per stage",
    "one file per N4 group or sequential parts",
    "a producer node for a structured check id on Refusal before N2, or define gate as the RESUME_CLASSES/KNOWN_PATTERN class name and restate norm N-gate",
    "friction row carries turn shares only; money keys dropped by name; test for absence",
    "name run_class source and the default when absent, in both P1b and P1v",
    "one Lead node for SIBLING_MAP, architecture.md, calibration checks, the critic question and the finding field of plan section 6; queue lines for test-layers.json across the three specs, PC4-15/17/18 and FG7-15/19",
    "stub session_id prefix stub-, and a repeats row or drop the requirement",
    "non-blocking items 20-37 in the same fix round (readers validate_artifacts.py:806 and factory_dashboard.py:711; driver_timing.report reuse; retro_numbers.py:1721 reader named; Lead bookkeeping-time row; C-8 settled as committed; missed overlaps RC2-1/RC2-2, FV1-4, FV1-2/3/6/13/20/22, FG7-15/19)"
  ],
  "class_completeness": "Class 'one entity, two carriers or two modes' found in known_red (P1a/P1b), the question-key census (P1b vs test_conductor_doors.py), timing readers (P1v vs driver_timing.report), rework definition (P1v vs retro_numbers.resume_metrics); AR-20 same-commit ordering defect in all three specs. Map axes walked: 18, 34, 13 (relabelled to AR-13). No search beyond the map.",
  "trail": {
    "read": [
      "docs/tasks/specs/20261113-plan-fabrika-ne-huzhe-agenta.md",
      "docs/tasks/specs/20261113-p1a-writer-reader-round-spec.md",
      "docs/tasks/specs/20261113-p1b-dry-story-spec.md",
      "docs/tasks/specs/20261113-p1v-run-scoreboard-spec.md",
      "read-main handoffs/index.yaml, s3-strategist-to-designer.yaml, s4-designer-to-case-critic.yaml, s7-analyst-to-automator.yaml, s7-analyst-to-scribe.yaml, vocabulary.yaml",
      "read-main scripts: handoff.py, handoff_check.py, contract.py, s5_precheck.py, brief_pack.py, window_record.py, controller.py:7247-7325, stage_done.py, acceptance.py, no_move.py, driver_machine.py, driver_core.py, driver_dispatch.py, driver_runner.py, driver_timing.py, driver_journal.py, retro_numbers.py, friction.py, audit_factory.py:1715, gate_preflight.py:6081,6237, validate_artifacts.py:806",
      "read-main scripts/tests: scenario_walk.py, test-layers.json, slow_tests.json, selftest.py:103-115, story_run_common.py, test_conductor_doors.py:615-673, test_row_fields.py:366-380, test_story_run_s0.py:1138, test_brief_pack.py:2428",
      "read-main design/architecture.md:140-157,192,210-222; references stages.json, case-markers.json, detectors.json, artifact-contract.md, artifact-contract-plan.md",
      "docs/TESTING.md:40-130; docs/SIBLING_MAP.md headings",
      "findings-1413 live-run-fvf: batch-1, FV1-1, FV1-6, FV1-13, FV1-22",
      "plans/piles heads: package-ci/4, roles-context/2, execution-report/2, speed-cost/6, cost-dashboard/1, live-runs/2, thinking-roles/5, forge/7"
    ],
    "reruns": [
      {"command": "python -B -c handoff.index() count, role-to-conductor membership, spec size", "result": "23 handoffs, role-to-conductor not among them, 35 fields"},
      {"command": "python -B -c handoff.contract_of('S7','qa-failure-analyst'); acceptance.consumer_of('S6')", "result": "s7-analyst-to-automator; qa-failure-analyst"},
      {"command": "python -B -c len(KNOWN_REFUSALS); question-prices keys/answers; stage-joints; refusal_registry", "result": "21; 61/188; 43; 102 with 58 override empty"},
      {"command": "scenario_walk._closure(['story_run'])", "result": "227 of 279 scripts (gate door 201)"},
      {"command": "scenario_walk.py --witness-for test_field_producers.py test-layers.json", "result": "test_null_outcomes, test_selftest_shard, test_selftest_slow_tests"},
      {"command": "Grep -i run_class|STORY_RUN_DRY in read-main scripts; control STORY_RUN_CLAUDE", "result": "0; control 41 in 23 files"},
      {"command": "git merge-base --is-ancestor 8eb20e4/bb2bd10/5971ac0 2830b08", "result": "none in main"},
      {"command": "git ls-files runs; grep -c total_cost_usd driver-runs.jsonl", "result": "committed (4e00ed7), 120"}
    ]
  }
}
```
