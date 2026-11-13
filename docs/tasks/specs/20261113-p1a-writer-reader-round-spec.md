# Черновик спеки: слой П1-а «круг писатель → читатель на сегодняшних формах»

Статус: ЧЕРНОВИК дизайнера для приёмки Lead, ФИКС-РАУНД после критика на план t-401 (13.11.2026). Развилки возвращены
(раздел 8), ни одна не закрыта молча. Что поменялось по каждой находке — раздел «Фикс-раунд t-401» в конце.
Основание: план Lead `docs/tasks/specs/20261113-plan-fabrika-ne-huzhe-agenta.md` §3 «П1-а» (слово владельца 13.11.2026 «Да,
дизайнеру») и §10 (решения Lead по находкам t-401, обязательны); разведка t-356 `docs/tasks/specs/reports/t-356-fvf-net-why-digest.md`;
вердикт `docs/tasks/specs/reviews/t-401-p1-layers-plan-review.md`.

Дерево фактов: RM = `C:\QAFactory\forge-repo\.claude\worktrees\read-main\ai-packages\qa-factory` (origin/main). Все пути пакета
ниже — от корня пакета в RM, с номерами строк, прочитанными в этом дереве. Где номер взят из находки или разведки и мною не
перечитан, стоит пометка «(по находке, не перечитано)».

Скоуп: спека СЛОЯ, его заполнителя и общего помощника `known_red` (владелец — П1-а, решение §10 №3/№8). Починки находок FV1 —
НЕ здесь: каждая идёт после своей красной строки (план §4). Соседние слои П1-б («сухая стори») и П1-в («табло») не
специфицируются; общая часть — интерфейс заполнителя (§3.5), выходы стадий (§3.7) и помощник `known_red` (§3.6).
Документы Lead (`docs/SIBLING_MAP.md`, `design/architecture.md`, калибровочная проверка, вопросы критика) узлы этой спеки НЕ
пишут — требования к узлу Lead «носители П1» собраны в §9 (решение §10 №17/№19).

---

## 1. Инварианты, владельцы проверок, классы переписи (designer rule 1; CLAUDE.md правило 10; P27, AR-29)

### 1.1 Какие AR-n трогает слой и как держит

План §6 называет для всего плана AR-22, AR-24, AR-25, AR-12, AR-29. Сверено с `design/architecture.md`; для П1-а:

| AR | Трогает? | Как держит | Проверка изменения (в DoD) |
|---|---|---|---|
| AR-22 «у читаемого поля есть производитель, у произведённого — читатель» (`design/architecture.md:233-238`) | да, слой — его детектор уровня ЗНАЧЕНИЙ. Сегодня детектор сам говорит, что ходит по именам: `test_field_producers.py` — только контракты передач, `test_stage_joints.py` — производитель и токен (`design/architecture.md:236`; `scripts/tests/test_stage_joints.py:4-8`) | ход в обе стороны: форма → значение → каждый читатель (прямой), требование читателя → названный писатель для каждой строки языков (обратный) | прогон `test_field_producers.py` в DoD N1–N3; правка строки «Detector» AR-22 (`:236`) — требование R1 к узлу Lead (§9), не узел этой спеки |
| AR-10 «требование проверки доходит до роли в её полях» (`design/architecture.md:113-118`) | да: обратный ход ловит ровно его нарушение — читатель требует поле, которого нет в форме роли (FV1-22) | строка «читатель без писателя» красная с парой | строка «Detector» AR-10 (`:116`) — требование R1 к узлу Lead (§9) |
| AR-21 «собранное едет в передаче целиком» (`:226-231`) | да: каждая форма заполняется и проходит своего читателя `handoff_check.check`; в круг входят ВСЕ 24 формы, включая форму помощи `role-to-conductor` под ключом `escalation` (`handoffs/index.yaml:102-108`) | ни одно поле формы не выпадает из заполнения: незаполнимая подсказка — красная строка; множество форм сверяется с листингом `handoffs/*.yaml` в обе стороны (N1 п. 4) | прогон теста |
| AR-13 «факт с функцией-читателем читается только через неё» (`:161-166`) | да | заполнитель читает контракт ТОЛЬКО через `handoff.index`/`handoff.template`/`handoff.spec`/`handoff.is_placeholder`/`handoff.set_value` (`scripts/handoff.py:320,399,644,662,667`); писателя выхода стадии — через `hooklib.load_ref_json("artifact-writers.json")` (так его читают `guard_pre_tool.py:778-784`, `driver_runner.py:1036`) и тем же предикатом «`writer == "<role> (the role)"`», что `Driver.written_outputs` (`scripts/driver_runner.py:1044`); читатели вызываются своей функцией, слой не держит своих копий их регулярок | грep `re.compile` в новых файлах: ни одного шаблона id читателя |
| AR-15 «общая задача решается в одном месте и проводится всюду» (`design/architecture.md`, раздел C) | да: реестр известных красных — ОДИН помощник `scripts/tests/known_red.py` для П1-а и П1-б (решение §10 №3) | одна форма строки, одна функция сверки (§3.6); П1-б импортирует, своей сверки не пишет | N0 DoD; критик П1-б сверяет импорт |
| AR-20 «храповики только сжимаются» (`:210-222`) | да: два храповика — реестр известных красных (помощник N0, §3.6) и строка рукописных входов в `tools/lint_ratchet.py` (N4, решение §10 №5) | оба только сжимаются; рост — строкой с `raised_by` (реестр) или `--update` с причиной в коммите (lint); устаревшая строка — отказ с дверью | «новый храповик входит в ось 18 и вопрос 9 тем же коммитом» (`:222`): строки оси 18 и вопроса 9 пишет узел Lead и сажает ВМЕСТЕ с N0 и N4 (требование R7, §9) |
| AR-23 «у обязательного списка объявлен пустой исход» (`:240-245`) | да: вариант «пустой список» для каждого списка формы; пустой реестр `known_red` — объявленный исход (§3.6) | пустой `scope` принимается только там, где форма объявила `null_outcome`; иначе читатель ОБЯЗАН отказать (отрицательная строка) | прогон теста |
| AR-28 «неизвестное не становится проходом» (`:275-280`) | да | незаполнимая подсказка, исключение читателя, язык без писателя, выход стадии без строки писателя, нечитаемый реестр — красная строка или отказ, никогда не пропуск; выход, который заполнитель не умеет, — названный результат `NotCovered`, не догадка (§3.5) | прогон теста |
| AR-29 «код судит данные» (`:134-157`) | да | слой судит только форму значения, стык и присутствие; суждение роли не судит (см. 1.2) | `judgment: none` у коммитов (тесты вне переписи, `:146`) |
| AR-1 / ось 34 «закрытое разнообразие — строка данных» (`:35-53`) | да: строки языков берутся из таблицы данных по ключу возможности, никогда по имени языка в коде слоя | см. решение F3 (а) | грep имён языков в новых файлах: только в фикстурах-образцах, не в ветвлениях |
| AR-24 «слова человека доходят целиком» | да, по решению F7 (а): строка «значение целиком» для полей со словами человека | строка с `known_red` → RC2-1 | прогон теста |
| AR-25 «у состояния есть выход» | НЕТ: это слой П1-б (план §3 П1-б) | — | — |
| AR-12 «трение меряется» | НЕТ: слой — тест, роли его не вызывают | — | — |

### 1.2 Каждая проверка слоя: владелец и класс переписи

Слой целиком живёт в `scripts/tests/` и одной строкой в `tools/lint_ratchet.py` (фордж): перепись суждений
(`scripts/tests/fixtures/judgment-census.json`) по устройству считает только `scripts/*.py` вне `scripts/tests/`
(`design/architecture.md:146`), поэтому строк переписи слой не добавляет. Класс и владелец всё равно названы (AR-29, change check):

| id | Проверка | Класс | Владелец |
|---|---|---|---|
| C1 | Прямой круг: значение, заполненное по подсказке формы, подано читателю; читатель возвращает то же значение / принимает | xref | данные (код) |
| C2 | Тождество: один логический факт (напр. id строки плана) во всех носителях-формах имеет одну форму id | shape | данные |
| C3 | Обратный ход: каждое поле, которое читатель ТРЕБУЕТ, имеет названного писателя, и писатель производит его для каждой строки таблицы языков | xref | данные |
| C4 | Согласие читателей: все читатели одного поля дают один вердикт на одном заполненном значении | xref | данные |
| C5 | Незаполнимая подсказка формы — красная строка | shape | данные |
| C6 | Реестр известных красных: сверка помощником `known_red.reconcile` (§3.6) — новая красная без строки — отказ с дверью; строка без `raised_by` — отказ; позеленевшая строка, не снятая из реестра, — отказ «удали строку» | ratchet (AR-20) | данные; внесение строки — суждение того, кто назван в `raised_by` (вердикт критика или слово Lead); снятие — узел починки |
| C7 | Рукописные входы читателей в тестах — строка `HandReaderInput` общего храповика `tools/lint_ratchet.py` (N4), только убывает | ratchet (AR-20) | данные; рост базы — `--update` с причиной в коммите, судит критик (вопрос 9) |
| C8 | Выход стадии: каждый выход `references/stages.json` классифицирован (заполняет роль по шаблону / пишет код / `NotCovered` с причиной); заполненный выход проходит своего читателя `validate_artifacts.collect_errors` | xref | данные |

Чего слой НЕ делает (P27): не решает, верна ли форма id `P-n` или `TS-n` (это решение узла FV1-14), не судит, хорош ли кейс,
не читает формулировки ролей. Красная строка говорит «писатель и читатель разошлись на значении X», а не «кто прав».

---

## 2. Место в трёх слоях `docs/TESTING.md`

`docs/TESTING.md:49-50` (слой 2): «**Стыки данных.** Поле, которое одна стадия пишет, а другая читает; … Проверки данных, без
запуска драйвера». П1-а — этот слой, доведённый до значения: строка стыка подаёт читателю то, что произвёл бы писатель по
сегодняшней форме, а не рукописный вход. Драйвер не запускается, модели нет.

Потолок (`docs/TESTING.md:55-58`, `:113-126`): «нового тестового файла на новый скрипт» нет; «случай идёт строкой в сценарий,
стык или таблицу своего слоя»; «новый тестовый файл не создаётся» (`:117`). Отсюда: слой — функции в СУЩЕСТВУЮЩЕМ файле слоя
`data_join` (решение F1 (а): `test_field_producers.py`, строка keep `scripts/tests/test-layers.json:1664-1676`,
`layer: data_join`, `why: AR-21/AR-22 field producer-reader join`), а каждая пара (поле, писатель, читатель) — строка таблицы.
Заполнитель и помощник `known_red` — не тестовые файлы, а помощники рядом (`harness.py`, `story_run_common.py` — тот же вид;
`selftest.py:745-749` проверяет листинг только тестовых файлов). Подсчёт вхождений регулярки в коде — «пин исходника»
(`docs/TESTING.md:94`): своим тестом он не пишется, а идёт «одной строкой в общем храповике (`dup_ratchet`, `lint_ratchet`, …)» —
отсюда N4 (решение §10 №5). Литерал числа форм или вариантов — «пин измеренной константы» (`docs/TESTING.md:95`): пины обхода
считаются от носителя, не литералом (N1 п. 4).

Правило покрытия импортов (факт, на который опираются owns): `test_selftest_slow_tests.py:478-490` на НАСТОЯЩЕМ
`test-layers.json` требует, чтобы строка `keep` перечисляла в `covers` каждый помощник `tests/<m>.py`, который файл импортирует
(`:485-486`), и фикстуру, владельцем которой он назван в `fixture_owners` (`:487-488`, форма пути `scripts/tests/fixtures/<fx>`).
Значит, `covers` строки `test_field_producers.py` получает `tests/form_filler.py` и `tests/known_red.py` в том же коммите, что
первый импорт; то же обязана сделать строка `keep` теста П1-б, импортирующего `known_red.py` (сообщено в §9 R8).

Правка текста `docs/TESTING.md` НЕ нужна для решения F1 (а). Решение F2 — слово владельца; до ответа текст не меняется.

Бюджет (`docs/TESTING.md:115-125`): мир строится ОДИН раз на прогон функции; добавка ко времени файла — до 10 с; строк теста не
больше строк продукта узла — продукт здесь заполнитель и данные, причина превышения (если будет) — одна строка отчёта. Обещание
«до 10 с» на ~24 формы × варианты вызовов `handoff_check.check` не измерено (вердикт №37): замер — обязательная строка отчёта N1
и N3; превышение — строка отчёта с числом, решает Lead (молча варианты не срезаются).

---

## 3. Инвентарь (перечислением; где широко — метод и замер)

### 3.1 Формы, которые пакет даёт роли

| Вид формы | Носитель | Сколько | Как читается слоем |
|---|---|---|---|
| Формы передач | `handoffs/*.yaml`; реестр `handoffs/index.yaml`: ключ `handoffs` (`:39-71`, 23 строки) и ключ `escalation` (`:102-108`, контракт `role-to-conductor`, `kind: help`) | 24 формы = 23 строки `handoffs` + 1 `escalation` (26 файлов минус `index.yaml`, `vocabulary.yaml`); число не пинуется литералом (N1 п. 4). Строк с плейсхолдером `ключ: <…>` — 873 (замер: Grep `^\s*(- )?[A-Za-z_]+:\s*"?<` по `handoffs/`, count = 880 в 25 файлах, из них 7 в `index.yaml`) | `handoff.template(contract)` + `handoff.spec(contract)` (`scripts/handoff.py:399,644`); множество контрактов — `handoff.index()` (`:320`) по двум ключам |
| Ключи передач (страница роли) | `references/slices/<role>/handoff-keys.md`, генерируется `contract_slices.py` из тех же форм (`references/slices/qa-test-strategist/handoff-keys.md:1`) | 11 страниц | НЕ отдельный писатель: производная форм; слой сверяет, что подсказка на странице равна подсказке формы (строка C2, носитель — «текст, который видит роль») |
| Контракты артефактов | `references/artifact-contract*.md` (10 файлов) | шаблоны, которые читают код: кейс (`references/artifact-contract.md:54-69`, тело дословно `Requirements: R-1, R-2` и `Plan row: TS-n`, `:62-64`), план md (`references/artifact-contract-plan.md:40-58`, колонка `TS` = `TS-n`, `:46`), план JSON (`:68-69`), строка манифеста (`references/slices/qa-automator/artifact-contract-automation.md:11-26`) и прочие выходы стадий (§3.7) | прозой; решение F8 (а) — шаблоны как строки данных с якорем на дословный текст контракта |
| Форма строки манифеста, печатаемая кодом | `manifest_from_tests._row_form` / текст находки `s5_precheck._row_fields_text` (`scripts/s5_precheck.py:3768-3795`, плейсхолдеры `"<id>"`, `"<field>": <value>`, `qa(obligations=["<plan obligation id>"])`, `:3786,3791`); поля — `window_record.REQUIRED_ROW_FIELDS` (`scripts/window_record.py:176-189`) | 6 полей строки | заполняется как форма (это текст, который роль получает в отказе — ось 28) |
| Маркер обязательств на тесте | `references/case-markers.json:4-8` — форма маркера только под ключом `pytest` | 1 язык из 4 | строки языков, §3.3 |
| Профиль проекта (форма онбординга) | `references/profile-shape.json:11` (`"<test-file>"` в `argv`) | 1 | не в П1-а (решение F5 (б)) |

### 3.2 Виды плейсхолдеров (грамматика уже есть в `handoff._spec_of_value`, `scripts/handoff.py:429-447`)

| Вид | Признак | Пример с носителем | Правило заполнения |
|---|---|---|---|
| id-префикс | `<X-n…>` | `<P-n, the row's stable id>` `handoffs/s3-strategist-to-designer.yaml:52`; `<C-n>` `gate-a-to-automator.yaml:85` | `X-1` (префикс ДОСЛОВНО из подсказки; нумерация по контексту); для поля, ЦИТИРУЮЩЕГО id другой формы, — §3.5 «приоритет» |
| альтернативы id | `<A-n or B-n>`, `<A-n, B-n or C-n>` | `<P-n or R-n>` `s3-strategist-to-designer.yaml:153`; `<R-n, K-n or B-n>` `:79`; `<case id or P-n>` `s4-designer-to-case-critic.yaml:99` | вариант на каждую альтернативу |
| id + свободный текст | `<R-n, a source id or an area>` `s3-strategist-to-designer.yaml:146` | вариант id и вариант слова |
| путь с id внутри | `<bugs/DEBT-n.md>` `s8-bug-reporter-to-scribe.yaml:72` | `bugs/DEBT-1.md` (правило «голый id» здесь не срабатывает) |
| выбор inline | `<a|b|c>` | `<automate|manual-agent|manual-human|skip|unverifiable>` `s3-…:53`; `<TEST_BUG|TEST_BUG:collection|FLAKY|reorder>` `s7-analyst-to-automator.yaml:84` | первое значение в базовом варианте; для `header.verdict` — вариант на каждое |
| выбор из словаря | `one of vocabulary.X` (`handoff.py:32`) | `<one of vocabulary.header_verdicts>` | словарь важнее inline-списка (`handoff.py:436-441`) |
| булев | `<true|false>` | `s3-…:66` | `true` |
| предел длины | `<= N characters>` (`handoff.py:33,442-446`) | `<= 80 characters>` `s3-…:54` | значение длиной ровно N (AT) и N+1 (BEYOND, отрицательная строка) |
| счёт | `<n>`, `<n of m>`, `<r of 2>` | `s3-…:40`, `s7-analyst-to-automator.yaml:87` | `1`, `1 of 1`, `1 of 2` |
| хэш/версия | `<hash>`, `<hash or revision>`, `<plan_revision>` | `s3-…:36,39` | хэш файла мира (поле с деривером — оставить коду, ниже) |
| токены контракта | `<TICKET>`, `<dispatch>`, `<the author's dispatch>` (`handoff.py:406`) | `s3-…:45` | из контекста мира (§3.5); нет ключа — незаполнимо |
| необязательное | слова `OPTIONAL_WORDS` (`handoff.py:35-36`) | `<the stand this row needs, or a dash>` | два варианта: заполнено и опущено |
| заполняет код | «filled by code, or omit»; поля `DERIVERS`/`BY_LEAF` (`scripts/handoff_check.py:564-609`); предикат `handoff_check._code_fills` (`:2725`) | `grounding.*` `s3-…:85-90`; `plan_row` → `_plan_row_of` (`handoff_check.py:429`) | оставить плейсхолдер; в N1 (мир без артефактов) поле не судится — `check(fix=False)`, проблема `kind == "blank"` при `_code_fills(path)` не красная (тот же мягкий край, что `values_report`, `handoff_check.py:2880-2901`); круг дериверов `check(fix=True)` — в N3 после того, как `fill_artifact` положил артефакты в мир (E11) |
| свободный текст | всё прочее | `<what is being checked, one sentence>` | `filled <leaf>` |

Замер id-видов: 32 строки с плейсхолдером вида `<…X-n…>` в 14 формах (Grep `<[^>]*\b[A-Z]{1,4}-n\b` по `handoffs/`, перечень в
следе). Из них id строки плана `P-n`: `s3-strategist-to-designer.yaml:52,98,153`, `s4-designer-to-case-critic.yaml:50,99`,
`s4-designer-to-runner.yaml:48`; та же форма на странице роли `references/slices/qa-test-strategist/handoff-keys.md:27,51,79`.

### 3.3 Таблица языков и раннеров

Единой таблицы «язык/раннер» в пакете нет. Решение F3 (а): языки — `references/detectors.json` `assertion_probes` {`csharp` :86,
`java` :176, `typescript` :265} и `assertion_probes_ast` {`python` :326} — 4 языка; это «intended road» оси 34
(`docs/SIBLING_MAP.md:587`). (в) `references/launch-causes.json:28-52` `run_forms` — только для писателей с ключом раннера
(сегодня таких в П1-а нет). Прочие кандидаты, НЕ взятые: `references/test-path-markers.json:8` `code_extensions` — 20.

### 3.4 Читатели по полям (начальный реестр; полнота — метод ниже)

| Семейство | Поле (писатель-форма) | Читатели (функция — носитель) |
|---|---|---|
| RR-plan-row | `scope[].id`, `manual_policy[].row`, `unresolved[].id` формы S3 (`s3-…:52,98,153`); `scope[].plan_row` форм S4 (`s4-designer-to-case-critic.yaml:50`, `s4-designer-to-runner.yaml:48`); строка тела кейса `Plan row:` (`artifact-contract.md:63`); колонка `TS` плана md (`artifact-contract-plan.md:46`) | `contract.case_plan_row` / `CASE_PLAN_ROW_RE` `(TS-\d+)` (`scripts/contract.py:3052,3617-3619`); `s5_precheck.case_plan_row` / `PLAN_ROW_RE` `(TS-\d+)` (`scripts/s5_precheck.py:79,3747-3762`); `handoff_check._plan_row_of` `TS-\d+` (`scripts/handoff_check.py:429-440`); `contract.TS_ID_RE` (`contract.py:2765`); `grounding_table.TS_ID` (`scripts/grounding_table.py:1504`); `check_delivery.TS_IN_TEXT` (`scripts/check_delivery.py:371`) и `_case_map` (`:406`); `contract.plan_levels`/`case_levels` (`contract.py:2088-2109`); `traceability` `plan_by_ts` (`scripts/traceability.py:452,564`); `gate_brief.ITEM_ID_RE` (`scripts/gate_brief.py:4393`); `validate_artifacts.check_plan` — строки раздела сценариев только с `r[0].startswith("TS-")`, иначе отказ «has no TS-* rows» (`scripts/validate_artifacts.py:791,806-808`); `factory_dashboard.plan_levels` — ключ `r["ts"]` из `contract.parse_plan` (`scripts/factory_dashboard.py:710-716`); любой формы (контроль): `brief_pack.PLAN_ROW_RE` `(\S+)` (`scripts/brief_pack.py:66`) |
| RR-form | каждое поле каждой из 24 форм × 4 слова `header_verdicts` (`handoffs/vocabulary.yaml:23-27`); у `role-to-conductor` поля `header` нет (верхние ключи `handoffs/role-to-conductor.yaml:16-72`: `schema_version`, `contract`, `kind`, `request`, `answer`, `person_question`, `contract_change`, `claims`) — варианты без слова (E19) | `handoff_check.check(doc, contract, art, fix=..., use_judge=False)` (`handoff_check.py:1446`) |
| RR-accept | форма приёмщика стадии: `stage_acceptance` (`failure_class`, `quote`, `witness_paths`) и последняя строка `inputs_read` с формой автора | `stage_done.reviewed_author_dispatch` (`scripts/stage_done.py:939-955`); `acceptance.stage_acceptance_from_form` и `acceptance.stage_acceptance_errors` (`stage_done.py:1039-1042`; `scripts/acceptance.py:1331-1365,1559-1590` — по вердикту t-401, ключ C, мной не перечитано). Формы-кандидаты — по `references/stages.json` `acceptance_by` и `acceptance.consumer_of(stage)` (`stage_done.py:1020`), контракт формы — через `handoff.contract_of` БЕЗ получателя (`handoff.py:354`; вторичные контракты не возвращаются, `handoffs/index.yaml:22-26`) |
| RR-row-fields | 6 полей `REQUIRED_ROW_FIELDS` (`window_record.py:176-189`), писатель по `filled_by`: `automator` → фрагмент по форме строки; `marker` → `manifest_from_tests.py` по маркеру на тесте | `window_record.row_field_gaps` (`window_record.py:270-292`); `s5_precheck.check_row_fields` (`s5_precheck.py:3798-3834`). Финиш окна (проверка хэша ссылок внутри `Controller._s5_v2_collect`, `scripts/controller.py:7247,7293-7302` по вердикту t-401) — НЕ читатель этого слоя: функцией не вызывается; ловит П1-б (решение §10 №6) |
| RR-artifact | каждый выход стадии, который пишет роль (§3.7), заполненный `fill_artifact` | `validate_artifacts.collect_errors(path, cfg)` (`scripts/validate_artifacts.py:2625-2702`) — ветвится по пути; проверки артефактов истории срабатывают только под `/qa-factory/artifacts/` (`:2631`, E22) |

Метод полноты (команда — чистое чтение, хигиена п. 4b): писатели и требования собираются кодом из носителей, которые
пакет уже держит, без ручного списка:

```
import sys; sys.path.insert(0, r"<RM>\scripts")
import handoff, window_record, null_outcomes, json, hooklib
ix = handoff.index()                                                             # handoff.py:320
forms = [r["contract"] for r in ix["handoffs"]] + [ix["escalation"]["contract"]] # 23 + 1 (index.yaml:39-71, :102-108)
fields = {c: handoff.spec(c) for c in forms}                                     # путь -> FieldSpec (kind, options, optional, max_len, hint)
row_fields = window_record.REQUIRED_ROW_FIELDS                                   # 6, с filled_by
tool_fields = list(null_outcomes.tool_fields())                                  # поля «нужен инструмент» (test_field_producers.py:64)
joints = json.load(open(r"<RM>\references\stage-joints.json", encoding="utf-8")) # 43 ключа обхода (test_stage_joints.py:31,78)
stages = json.load(open(r"<RM>\references\stages.json", encoding="utf-8"))       # выходы стадий, §3.7
writers = hooklib.load_ref_json("artifact-writers.json")["artifacts"]            # писатель каждого выхода (references/artifact-writers.json)
```

Читатели вне этих носителей (регулярка id в произвольном скрипте) кодом не находятся — их перечень держит реестр
`form-rounds.json` (§5, N3) с начальной таблицей выше, а пропуск ловит критик (детектор — требование R5 к узлу Lead, §9).
Архитектурная справка: «738 required handoff fields, 28 tool-made» (`design/architecture.md:235`) — число снято на main
41fb1346, мной не перемерено; N1 печатает фактическое число строкой итога.

### 3.5 Интерфейс заполнителя (общая часть с П1-б) — ЕДИНСТВЕННОЕ место, где он записан

Где: `ai-packages/qa-factory/scripts/tests/form_filler.py` (помощник, не тест); правила и шаблоны —
`scripts/tests/fixtures/form-fill-rules.json`. Только чтение пакета; пишет только во временный корень мира, который ему передали.

```
ABSENT                                                # единственный объект-метка: «поле удалить» (в overrides)
FillContext(task_key: str = "TP1-1", case_id_form: str | None = None,          # case_forms по config; None -> форма по умолчанию пакета
            dispatches: dict[str, dict] = {}, author_dispatch: str = "",         # id -> {stage, role}; для <the author's dispatch>
            minted: dict[str, list[str]] = {}, files: dict[str, str] = {},       # выпущенные id по префиксу; пути мира -> текст
            cases: list[str] = [], bugs: list[str] = [], requirements: list[str] = [])   # id для выходов-каталогов (§3.7)
Fill(path, hint, value, rule)            Unfillable(path, hint, why)
Filled(contract, verdict, variant, text: str, data: dict, fills: list[Fill], unfillable: list[Unfillable], left_for_code: list[str])
FilledArtifact(output, files: dict[str, str], fills: list[Fill], unfillable: list[Unfillable], left_for_code: list[str])
ByCode(output, writer: str)              # выход пишет код (artifact-writers.json); заполнитель его не пишет
NotCovered(output, why: str)             # выход пишет роль, но заполнитель ещё не умеет; причина — строка form-fill-rules.json
class NotFillable(Exception)             # (contract_or_output, path, hint, why) — бросает Filled.require() / FilledArtifact.require()

variants(contract) -> list[tuple[verdict | None, variant]]   # слова header_verdicts (None у формы без header.verdict) x
                                                             # {base, omit_optional, empty_lists, alt:<k>, at_limit, beyond_limit, cite_hint:<path>}
fill_form(contract, ctx, *, verdict=None, variant="base", overrides=None) -> Filled
fill_artifact(output, ctx, *, variant="base", overrides=None) -> FilledArtifact | ByCode | NotCovered
    # output: имя выхода из references/stages.json ("work/triage.json", "work/test-cases/", "project:bugs/" ...)
    #         или подвид: case | plan_md_row | plan_json_row | manifest_row | first_look_rows | test_file:<lang>
classify(output) -> "role" | "code" | "not_covered"           # по artifact-writers.json + form-fill-rules.json, без догадки
stage_outputs() -> list[tuple[stage, output]]                 # outputs + optional_dispatches[].output из references/stages.json
write_dispatch_form(task_root, dispatch_id, contract, ctx, verdict, *, overrides=None) -> Path   # work/handoffs/<dispatch_id>.yaml (для П1-б)
write_outputs(task_root, project_root, result: FilledArtifact) -> list[Path]  # "project:<rel>" -> <project_root>/qa-factory/<rel>
```

`overrides: dict[str, value | ABSENT]` — ключ: путь поля в грамматике путей форм (`section[].key` — ключ в каждой строке секции,
`section[0].key` — в одной строке; так её задаёт `handoffs/index.yaml:78-79`); для артефактов: путь ключа JSON/YAML в той же
грамматике, для md — ключ front matter или `body:<метка строки>` (напр. `body:Plan row`). Значение кладётся ДОСЛОВНО в обход
подсказки и записывается в `fills` с `rule="override"`; `ABSENT` удаляет поле (ключ опущен). Поведение на краях — E20.

Инварианты интерфейса (на них П1-б может опереться):
- значение берётся из подсказки ДОСЛОВНО: префикс id (`P`, `TS`, `C`, `PR`…) не переводится в другой; заполнитель никогда не
  читает регулярки читателей и не подбирает значение «чтобы прошло» (код не оракул, P20/FR-58 по аналогии);
- ПРИОРИТЕТ (вердикт №22): поле, которое ВЫПУСКАЕТ id (первый писатель факта, напр. S3 `scope[].id`), берёт подсказку
  дословно; поле, которое ЦИТИРУЕТ id, выпущенный другой формой (S4 `plan_row`, тело кейса `Plan row:`), в базовом варианте берёт
  выпущенное значение из `ctx.minted` (так пишет живая роль — находка FV1-1: кейс с `Plan row: P-1`), и, если префикс
  выпущенного id расходится с префиксом подсказки цитирующего носителя (`P-1` против шаблона `Plan row: TS-n`,
  `artifact-contract.md:63`), заполнитель ДОБАВЛЯЕТ вариант `cite_hint:<path>` с дословным префиксом подсказки (`TS-1`).
  Ни один из двух видов не выбирается молча: базовый проверяет читателей (C1), вариант — тождество (C2);
- поле, которое заполняет код, остаётся плейсхолдером и попадает в `left_for_code`; его заполняет `handoff_check --fix`, не заполнитель;
- `unfillable` никогда не пуст молча: вызывающий обязан превратить каждую запись в красную строку (П1-а) или вызвать
  `require()`, который бросает `NotFillable` с формой/выходом и полем (требование П1-б §6 N2 «исключение с формой и полем»);
- выход стадии всегда получает ОДИН из трёх названных результатов; `NotCovered` никогда не превращается в рукописный текст
  ни здесь, ни у вызывающего (в П1-б — строка `live_only`, решение §10 №4);
- детерминизм: тот же вход (контракт/выход, контекст, вариант, правки) → те же байты; ни времени, ни случайности, порядок ключей —
  порядок шаблона.

### 3.6 Помощник `known_red` — ЕДИНСТВЕННОЕ место, где записан его интерфейс (решение §10 №3/№8; П1-б цитирует этот раздел)

Где: `ai-packages/qa-factory/scripts/tests/known_red.py` (помощник, не тест). Узел N0, первым.

Форма строки реестра (раздел `known_red` в JSON-фикстуре потребителя; у П1-а — `scripts/tests/fixtures/form-rounds.json`,
у П1-б — файл, который назовёт её спека):

```
"known_red": {
  "<id строки обхода>": {"node": "<FV1-n | id узла пачки>",
                         "raised_by": "<кто и где разрешил рост: путь вердикта критика или «Lead, дата»>",
                         "note": "<необязательно, одна строка>"}
}
```

- `<id строки обхода>` — непрозрачная строка, которую печатает обход потребителя (П1-а: `<family>: <writer-path> -> <reader>`,
  `identity: <group>`, `<field> <- <writer>@<lang> -> <reader>`, `unfillable <contract>:<path>`; П1-б: `(<ключ цен | маршрут>,
  <вариант>)` в своей записи). Помощник id НЕ разбирает и сравнивает только ТОЧНЫМ равенством строк.
- `node` — соответствует `^[A-Z][A-Z0-9]*-[0-9]+[a-z]?$` (`FV1-1`, `RC2-1`, `PC4-15`).
- `raised_by` — непустая строка после `strip()`. Каждая строка несёт свой `raised_by`: рост реестра всегда назван построчно
  (AR-20 «a raise is named», `design/architecture.md:210-211`); отдельного счётчика нет — число строк и есть храповик.

```
Row(node: str, raised_by: str, note: str = "")                # frozen
Verdict(ok: bool, problems: tuple[str, ...], known: tuple[str, ...])
class LedgerError(ValueError)                                 # реестру нельзя верить: файл, id строки, что ожидалось
load(path, section: str = "known_red") -> dict[str, Row]
reconcile(results: Mapping[str, bool], ledger: Mapping[str, Row], *, ledger_path: str) -> Verdict
    # results: id -> True (зелёная) / False (красная) для КАЖДОЙ строки, которую прошёл обход; упавшая с исключением = False
```

Поведение `reconcile` — одна функция сверки, все края:

| Случай | Исход | Строка `problems` / `known` (дверь) | Инвариант |
|---|---|---|---|
| красная, строка в реестре | ожидаемая | `known red: <id> -> <node>` в `known` | известная красная не валит канон, но видна в выводе |
| красная, строки нет | отказ | `new red: <id> — fix it, or add "<id>": {"node": "<FV1-n or node id>", "raised_by": "<verdict or word that names this raise>"} to <ledger_path> known_red` | новая красная без названного разрешения не проходит никогда |
| зелёная, строка в реестре (позеленела без снятия) | отказ | `stale: <id> is green; remove its known_red row (node <node>) in this commit` | метка не переживает починку; сжатие только явное |
| строка реестра, которой нет среди `results` (неизвестный id) | отказ | `unknown row: <id> is not a row of this walk; rename it to the walk's id or remove it` | строка реестра никогда не прикрывает «ничего» и не переживает переименование строки обхода |
| зелёная, строки нет | норма | — | — |
| пустой реестр (`{}` или раздела нет в существующем файле) | объявленный пустой исход (AR-23) | каждая красная — `new red` | пустой реестр — не «всё разрешено» |
| пустые `results` при непустом реестре | отказ | каждая строка — `unknown row` | обход, который ничего не прошёл, не зеленеет (плюс пин размера у потребителя) |

`ok = not problems`. Вывод печатается в порядке: `problems` (отсортированы по id), затем `known`.

Края `load` (каждый — `LedgerError` с файлом, id строки и ожидаемым видом; никогда не «пустой реестр»):
файл отсутствует или не JSON — отказ (неизвестное не проход, AR-28); раздел есть, но не объект; повтор id (загрузка с
`object_pairs_hook`, отвергающим дубли, — `json.loads` молча оставил бы последний); id с ведущими/хвостовыми пробелами или пустой;
строка не объект; `node` нет или не по шаблону; `raised_by` нет, не строка или пустой после `strip()`; ключ строки кроме `node`,
`raised_by`, `note`. Отсутствие РАЗДЕЛА в существующем файле — пустой реестр (объявлено выше).

Направление ошибки (помощник — ГЕЙТ: решает, зелёный ли канон): допустимо ошибаться только в сторону красного. Неудобные входы,
обязанные остаться красными (строки таблицы N0): id, отличающийся регистром или пробелом от строки обхода; строка уровня вида
(`exit_limit`) при красном варианте (`exit_limit/empty`) — префикс НЕ прикрывает (вердикт №8, AR-28); `raised_by: "  "`;
`raised_by: null`; `node: "fv1-1"`; повтор id в файле; строка для зелёного id; пустые `results`.

Тест помощника — N0 (таблица в `test_field_producers.py`). Потребители (`form-rounds.json` П1-а, файл П1-б) зовут ТОЛЬКО `load`
и `reconcile`; своей сверки, своего счётчика и своей двери роста не пишут (AR-15, P31).

### 3.7 Выходы стадий для `fill_artifact` (решение §10 №4 (а))

Перечень снят с `references/stages.json` (ключи `outputs` и `optional_dispatches[].output`); писатель — `references/artifact-writers.json`
(`aw:` ниже). Класс: «роль» — `writer` вида `<role> (the role)` (тот же предикат, что `driver_runner.py:1044`); «код» — иначе.
Выход, названный в нескольких стадиях, классифицируется один раз (по имени). «Шаблона/формы в контрактах нет» ниже означает:
Grep `^#+ ` по `references/artifact-contract*.md` (25 файлов, заголовки прочих выходов в той же выдаче — положительный контроль)
не дал заголовка для этого файла.

| Стадия | Выход (`stages.json:строка`) | Писатель (`aw:строка`) | Класс | Шаблон / контракт | Узел | Начальный исход |
|---|---|---|---|---|---|---|
| S0 | `pipeline.json` (:17) | `stage_done.py` (aw:12-17) | код | — | N2a | `ByCode` |
| S0 | `project:readiness.json` (:18) | `readiness.py` (aw:332-335) | код | — | N2a | `ByCode` |
| S1 | `work/context-manifest.json` (:47) | `qa-scout (the role)` (aw:19-24) | роль | `references/artifact-contract-grounding.md:7` | N2a | `FilledArtifact` |
| S1 | `work/context-bundle.json` (:48) | `context_bundle.py` (aw:25-28) | код | — | N2a | `ByCode` |
| S1 | `work/impl-diff.txt` (:49) | `qa-scout (the role)` (aw:33-36) | роль | заголовка в контрактах нет (это текст диффа) | N2a | `NotCovered` — «no contract shape: a diff text; the story kit supplies it» |
| S1 | `work/reference-snapshot.yaml` (:50; и `optional_dispatches` :43) | `reference_snapshot.py` (aw:85-88) | код | — | N2a | `ByCode` |
| S2 | `work/requirements-register.md` (:76) | `qa-requirements-tester (the role)` (aw:37-45) | роль | `references/artifact-contract-plan.md:7` | N2a | `FilledArtifact` |
| S2 | `work/requirements-readiness.json` (:77) | `qa-requirements-tester (the role)` (aw:46-52) | роль | `references/artifact-contract-json.md:123` | N2a | `FilledArtifact` |
| S2 | `understanding.md` (:78) | `qa-requirements-tester (the role)` (aw:53-58) | роль | `references/artifact-contract-plan.md:30` | N2a | `FilledArtifact` |
| S3 | `test-plan.md` (:124) | `qa-test-strategist (the role)` (aw:63-66) | роль | `references/artifact-contract-plan.md:38`; подвид `plan_md_row` | N2b | `FilledArtifact` |
| S3 | `work/test-plan.json` (:125) | `qa-test-strategist (the role)` (aw:67-75) | роль | `references/artifact-contract-plan.md:68-69` (по прежней редакции, не перечитано); подвид `plan_json_row` | N2b | `FilledArtifact` |
| S3 | `work/grounding.yaml` (:126) | `qa-test-strategist (the role)`, машинерия `grounding_table.py`, `base_slice.py` (aw:76-84) | роль | `references/artifact-contract-plan.md:99`; разделы, которые пишет код (`:104`), — в `left_for_code` | N2b | `FilledArtifact` |
| S3 | `work/first-look.yaml` (`optional_dispatches` :119) | `first_look.py` (aw:227-230) | код; роль шлёт строки | подвид `first_look_rows`: `references/artifact-contract-first-look.md:11` («The rows you send») | N2b | `ByCode` для выхода; `FilledArtifact` для подвида |
| S4 | `work/test-cases/` (:160) | `qa-case-designer (the role)` (aw:133-135) | роль | `references/artifact-contract.md:54`; подвид `case`, файл на каждый `ctx.cases` | N2b | `FilledArtifact` |
| S4 | `state/story-case-links.json` (:161) | `case_versions.py` (aw:137-139) | код | — | N2b | `ByCode` |
| S5 | `work/automation-manifest.json` (:193) | `manifest_put.py`, машинерия `manifest_from_tests.py`, `finalize_task.py` (aw:141-148) | код; роль пишет фрагмент | подвид `manifest_row`: поля `window_record.REQUIRED_ROW_FIELDS` (`window_record.py:176-189`), контракт `references/artifact-contract-automation.md:6` | N2c | `ByCode` для выхода; `FilledArtifact` для подвида |
| S5, S6 | `work/evidence/` (:194, :228) | `run_suite.py` и машинерия (aw:184-193) | код | — | N2c | `ByCode` |
| S5 | `work/s5-plan.json` (:195) | `qa-automator (the role)`, скелет — `s5_plan.py --init` (aw:149-155; `references/artifact-contract.md:51` «fields: the brief») | роль | шаблона в контракте нет | N2c | `NotCovered` — «shape is the skeleton s5_plan.py --init writes; no contract template» |
| S5 | `work/s5-notes/` (:196) | `qa-automator (the role)` (aw:125-132) | роль | заголовка в контрактах нет | N2c | `NotCovered` — «free notes, no contract shape» |
| S5 | подвид `test_file:<lang>` (маркер по `references/case-markers.json`) | роль автоматора | роль | `case-markers.json:4-8` | N2c | `FilledArtifact` для `pytest`; для языка без формы маркера — `Unfillable` (E9, красная строка C3) |
| S6 | `work/run-report.json` (:227) | `finalize_task.py` (aw:180-183) | код | — | N2c | `ByCode` |
| S6 | `work/evidence/manual/<case>/tried.md` (:229) | `qa-runner (the role)` (aw:243-246) | роль | заголовка в контрактах нет | N2c | `NotCovered` — «no contract heading; the recorder's build reads it (aw:245)» |
| S7 | `work/triage.json` (:255) | `qa-failure-analyst (the role)` (aw:247-255) | роль | `references/artifact-contract-run.md:62` | N2d | `FilledArtifact` |
| S7 | `work/bug-drafts/` (:256) | `qa-failure-analyst (the role)` (aw:260-263) | роль | `references/artifact-contract-run.md:106`; файл на каждый `ctx.bugs` | N2d | `FilledArtifact` |
| S8 | `work/ledger.json` (:282) | `ledger.py` (aw:272-275) | код | — | N2d | `ByCode` |
| S8 | `work/ledger.md` (:283) | `ledger.py` (aw:276-279) | код | — | N2d | `ByCode` |
| S8 | `test-report.md` (:284) | `qa-doc-scribe (the role)` (aw:288-296) | роль | `references/artifact-contract-results.md:20` | N2d | `FilledArtifact` |
| S8 | `work/proposals/` (:285) | `external_writes.py` (aw:336-339) | код | — | N2d | `ByCode` |
| S8 | `project:bugs/` (:286) | `qa-bug-reporter (the role)` (aw:268-271) | роль | `references/artifact-contract-run.md:140` | N2d | `FilledArtifact` |
| S8, S9 | `project:obligations.md` (:287, :333) | `qa-retro-analyst (the role)` (aw:324-327) | роль | раздел `references/artifact-contract.md:172` «Project-level files» (форму мною не прочитано) | N2d | `FilledArtifact`, если раздел задаёт форму; иначе `NotCovered` с причиной «no shape in artifact-contract.md:172» |
| S9 | `retro.md` (:332) | `qa-retro-analyst (the role)` (aw:317-323) | роль | `references/artifact-contract-results.md:65` | N2d | `FilledArtifact` |
| S9 | `project:factory-backlog.md` (:334) | `qa-retro-analyst (the role)` (aw:328-331) | роль | как `project:obligations.md` | N2d | как `project:obligations.md` |

Итог перечня (мой счёт по `stages.json`, тест сверяет с носителем, литералом не пинуется): 32 вхождения в `outputs`, 30 разных
имён (`work/evidence/` у S5 и S6, `project:obligations.md` у S8 и S9); плюс `work/first-look.yaml` из `optional_dispatches`
(второе — `work/reference-snapshot.yaml` — совпадает с выходом S1) — 31 имя; из них по `writer` 19 — роль, 12 — код; подвидов 6.
Аналог, замеченный по ходу (скоуп не расширяю): `references/artifact-registry.json` держит второй носитель писателя (`producer`)
для части тех же файлов, с другими именами ролей (`qa-req-tester` :6, `qa-results-writer` :30) и отличием пути
(`work/readiness.json` :126 против `project:readiness.json` в `stages.json:18`); слой читает только `artifact-writers.json`.

---

## 4. Края (rule 11, rule 1 designer) — поведение и инвариант

| # | Край | Поведение | Инвариант (что недостижимо / что обязано отказывать) |
|---|---|---|---|
| E1 | Альтернативы `<P-n or R-n>`, `<R-n, K-n or B-n>`, `<case id or P-n>` | вариант на каждую альтернативу; каждый подаётся всем читателям поля | писатель, следующий форме, НИКОГДА не получает отказ читателя: любая альтернатива формы принимается каждым читателем этого поля |
| E2 | id + свободный текст `<R-n, a source id or an area>` | вариант id и вариант слова (`area-1`) | то же: форма разрешила слово — читатель не требует id |
| E3 | Путь с id `<bugs/DEBT-n.md>` | `bugs/DEBT-1.md` | правило «голый id» не съедает путь |
| E4 | Необязательное поле (`OPTIONAL_WORDS`) | варианты «заполнено» и «опущено» | опущение, разрешённое формой, читатель не отказывает |
| E5 | `required_when` / `rows_owed_when` (`handoff.py:535-574`) | вариант на каждое слово `header.verdict`; секции, должные под словом, заполнены, прочие опущены | секция, должная под словом, отсутствует → читатель ОБЯЗАН отказать (отрицательная строка); недолжная отсутствует → принимается |
| E6 | Пустой список (AR-23) | вариант `[]` для каждого списка; `scope: []` — только у формы с `null_outcome` (`handoff.py:458,514-532`), с миром, где условие истинно | `scope: []` без объявленного `null_outcome` ОБЯЗАН быть отказан; прочие пустые списки принимаются |
| E7 | Поле или выход без читателя | у полей форм читатель всегда есть (`handoff_check.check`); для полей артефактов без строки читателя — строка итога `fields with no registered reader: N`; для выхода стадии, где `collect_errors` не отказал и на сломанном варианте (`overrides` с `ABSENT` на первом поле `required` шаблона), — строка итога `outputs no reader refuses: <список>`, не красная (решено мной, §8.2) | «читатель, который ничего не прочёл» не выдаётся за зелёный круг: он назван в итоге поимённо |
| E8 | Читатель без писателя (обратный ход) | красная строка `(<field>, <none>, <reader>)` | требование читателя никогда не остаётся без названного писателя молча |
| E9 | Язык/раннер, который писатель обслужить не может (нет формы маркера для языка в `case-markers.json`) | красная строка `(<field>, <writer>@<lang>, <reader>)` | язык никогда не исключается слоем и не «пропускается»; уход строки — только реестром `known_red` с узлом (§3.6), P31 |
| E10 | Незаполнимая подсказка (не подошло ни одно правило) | красная строка `unfillable <contract>:<path> «<hint>»` | заполнитель не выдумывает значение и не оставляет плейсхолдер, который читатель прочтёт как пустое (`handoff.is_placeholder`, `handoff.py:662-664`) |
| E11 | Поле, которое заполняет код (DERIVERS/BY_LEAF) | N1: `check(fix=False, use_judge=False)`, проблема `kind == "blank"` при `_code_fills(path)` не красная, путь — в `left_for_code` (`handoff_check.py:2725,2901`). N3: после `fill_artifact` (артефакты в мире) — `check(fix=True, use_judge=False)`; деривер вернул `None` → красная строка, писатель = деривер | в мире без артефактов деривер не судится (иначе каждое поле кода — ложная красная); в мире с артефактами значение кода проверяется тем же кругом, что значение роли |
| E12 | Токен контракта без ключа в контексте | незаполнимо (E10) | — |
| E13 | Предел `<= N characters` | AT (N символов) — принимается; BEYOND (N+1) — обязан быть отказан | предел, объявленный формой, держит читатель |
| E14 | Читатель бросил исключение на заполненном входе | красная строка `crashed: <тип>`; в `known_red.reconcile` — `False` | исключение — не пропуск (AR-28) |
| E15 | Форма двух контрактов одной стадии (вторичный, `index.yaml:51,57,65`) | заполняется каждый контракт отдельно; читатель приёмки получает контракт через `handoff.contract_of` без получателя | имя контракта в слое не пишется руками для читателя приёмки |
| E16 | ВРЕМЕННОЕ (rule 11 (i)): помощника `known_red`, заполнителя, правил, реестра сегодня нет | до N0 — ничего не меняется; N0 создаёт `known_red.py` (П1-б N1 до N0 не стартует); N1 создаёт заполнитель и правила; N2a создаёт таблицу выходов стадий (выходы групп N2b–N2d до своих узлов стоят `NotCovered` с причиной «group N2x not landed»); N3 создаёт `form-rounds.json`, где раздел `known_red` впервые заполняется по ЗАМЕРУ первого прогона и сверяется со списком §4.2; N4 добавляет строку в `lint_ratchet` и базу | после N3 тест зелёный на main ровно при `known_red` = фактические красные; после каждого N2x число `NotCovered` не растёт |
| E17 | ПРОТИВОРЕЧИЕ требований: слой обязан краснеть на дефектах main, канон CI на main обязан быть зелёным (PROJECT.md, «Канон всегда на CI») | разрешается реестром `known_red` через `known_red.reconcile` (§3.6) | красная строка вне реестра — отказ; строка реестра, ставшая зелёной, — отказ «удали строку» (сжатие только явное) |
| E18 | ПОЗИЦИОННОЕ: нет — слой не вставляет ветку в существующую логику пакета; единственная вставка — второй источник находок в `tools/lint_ratchet.py` (N4) | источник `HandReaderInput` подмешивается к НЕфатальным находкам до подсчёта `counts` (`lint_ratchet.py:190-192`) | фатальные классы (`SyntaxError`, `UnexpectedError`, `:48`) по-прежнему никогда не попадают в базу; строка рукописных входов не может прикрыть или сдвинуть находку pyflakes (у неё свой класс в identity) |
| E19 | Форма `role-to-conductor` (`kind: help`, без `header`, `handoffs/role-to-conductor.yaml:16-72`) | варианты без слова (`verdict=None`); читатель — `handoff_check.check` как у прочих форм. Если `check` не читает форму вида `help` (исключение или отказ, не связанный с полем), — красная строка `form-kind-unread: role-to-conductor`, перечисляется в отчёте N1 списком (как `unfillable`), решает Lead | форма помощи не выпадает из круга молча (вердикт №1); её половину `request` в жизни рендерит код (`handoff_help.render`, `scripts/handoff_help.py:93-119`), что записано как наблюдение (§8.1), а не повод исключить |
| E20 | `overrides` | путь не называет ни одного поля формы/шаблона → `Unfillable(path, why="override names no field of <contract|output>")`; `ABSENT` на обязательном поле → поле опущено (читатель обязан отказать — так П1-б сеет отказы); правка поля, которое заполняет код, → значение кладётся, путь уходит из `left_for_code`; `section[].key` → во все строки секции, `section[0].key` → в одну; правка и `cite_hint` на один путь → правка важнее, вариант `cite_hint` для этого пути не строится | правка, промахнувшаяся мимо цели, никогда не даёт «чистую» форму, похожую на засеянную |
| E21 | Выход стадии, который заполнитель не умеет | `fill_artifact` → `NotCovered(output, why)`; причина — строка раздела `not_covered` в `form-fill-rules.json`; тест печатает итог `not covered: <output> — <why>` | вызывающий получает названный результат, никогда догадку или пустой файл; П1-б делает из него строку `live_only` (решение §10 №4) |
| E22 | Раскладка мира для читателя артефактов | мир строится как `<root>/qa-factory/artifacts/<task_key>/…`, проектные выходы — `<root>/qa-factory/<rel>`: проверки `collect_errors` срабатывают только под `/qa-factory/artifacts/` (`validate_artifacts.py:2631`) | неверная раскладка не даёт тихий зелёный: сломанный вариант E7 обязан получить отказ, иначе выход назван в итоге |
| E23 | Выход стадии без строки в `artifact-writers.json` или строка шаблона/`not_covered` для имени, которого нет в `stages.json` | красная строка `output <x>: no writer in artifact-writers.json` / `stale fill row <x>` | классификация не угадывает писателя и не держит строк ни для чего |
| E24 | Выход-каталог (`work/test-cases/`, `work/bug-drafts/`, `project:bugs/`) или путь с плейсхолдером (`work/evidence/manual/<case>/tried.md`) | файл на каждый id из `ctx.cases` / `ctx.bugs`; пустой список id → `Unfillable(output, why="no ids in ctx for a directory output")` | каталог без файлов не выдаётся за заполненный выход |

### 4.1 Направление ошибки взятых функций (rule 1, вторая часть)

`handoff.spec` / `_spec_of_value` (`handoff.py:429-447`) — сегодня советчик для проверки формы — становится генератором
значений слоя (ответственнее: от него зависит, увидит ли слой дефект).

- Допустимое направление: ложная КРАСНАЯ (заполнитель выдал значение, которое роль не выдала бы) — разбирается и чинится
  правилом в `form-fill-rules.json`. Недопустимое: ложная ЗЕЛЁНАЯ — значение, которое прошло читателя только потому, что
  заполнитель «нормализовал» подсказку.
- Неудобные входы, которые обязаны остаться на безопасной стороне (каждый — строка таблицы правил N1):
  `<P-n, the row's stable id>` → `P-1`, не `TS-1`; `<PR-n, or the empty list>` (`s5-automator-to-critic.yaml:86`) → и `PR-1`, и `[]`;
  `<file::function or T-n of the planned test>` (`:96`) → оба варианта; `<bugs/DEBT-n.md>` → путь; `<r of 2>` → `1 of 2`;
  `<= 80 characters>` → AT/BEYOND; `<true|false, or omit when …>` (`s3-…:131`) → `true` и «опущено»;
  `<one of vocabulary.test_levels - unit|integration|…>` (`s3-…:63`) → значение словаря;
  `<TEST_BUG|TEST_BUG:collection|FLAKY|reorder>` → двоеточие внутри варианта не режет его;
  `<the author's dispatch>` → `work/handoffs/<ctx.author_dispatch>.yaml`.
- `OPTIONAL_WORDS` содержит широкие `"when "`, `", or "` (`handoff.py:35-36`): поле, ошибочно признанное необязательным, даёт
  вариант «опущено», и читатель его отказывает — это красная строка (безопасная сторона), а не молчание.

`handoff_check._code_fills` (`handoff_check.py:2725`) — сегодня мягкий край проверки файла значений до записи (`:2880-2901`) —
в N1 решает, какое пустое поле НЕ судить. Допустимая ошибка: поле, ошибочно признанное «заполняет код», не судится в N1, но
судится в N3 кругом дериверов (`fix=True`) — потери нет. Недопустимая: поле роли, признанное полем кода, не судится нигде.
Неудобный вход (строка N3): каждое поле, пропущенное в N1 по `_code_fills`, обязано встретиться в N3 либо заполненным
деривером, либо красной строкой «деривер вернул `None`»; поле, не встреченное в N3, — красная строка `unjudged <contract>:<path>`.

Предикат «писатель — роль» (`writer == "<role> (the role)"`, `driver_runner.py:1044`) — сегодня решает, что показать роли после
обрыва вызова, — в слое решает, писать ли выход заполнителем. Допустимая ошибка: выход роли, признанный выходом кода, получает
`ByCode` и в П1-б пишется настоящим кодом или становится `live_only` — видно в итоге. Недопустимая: выход кода, заполненный
заполнителем вместо настоящего писателя (рукописный текст, причина A плана). Неудобные входы: `"finalize_task/qa-failure-analyst"`
(форма `artifact-registry.json:116`, НЕ этого файла) — этот файл не читается; `writer` с машинерией (`work/triage.json`,
aw:247-255) — класс по `writer`, машинерия не меняет класс.

`validate_artifacts.collect_errors` (`validate_artifacts.py:2625`) — сегодня проверка на записи — в слое становится читателем
круга артефактов. Допустимая ошибка: отказ на заполненном выходе — красная строка, разбирается (форма шаблона или читатель).
Недопустимая: молчание на любом входе (ветка по пути не сработала) — закрыто сломанным вариантом E7 и раскладкой E22.

`known_red.reconcile` — гейт канона; направление и неудобные входы — §3.6.

### 4.2 Что слой обязан показать красным на сегодняшнем origin/main (список для сверки `known_red` в N3)

| Строка | Почему красная (по коду) |
|---|---|
| `plan-row: s3.scope[].id -> contract.case_plan_row` | кейс с `Plan row: P-1` → `CASE_PLAN_ROW_RE` `(TS-\d+)` не находит → `""` ≠ `P-1` (`contract.py:3052,3617-3619`) |
| `plan-row: s3.scope[].id -> s5_precheck.case_plan_row` | `PLAN_ROW_RE` `(TS-\d+)` (`s5_precheck.py:79,3750`) |
| `plan-row: s4.scope[].plan_row -> handoff_check._plan_row_of` | `re.search(r"TS-\d+")` (`handoff_check.py:439`) → деривер `None` |
| `plan-row: … -> grounding_table.TS_ID`, `contract.TS_ID_RE`, `check_delivery.TS_IN_TEXT`, `traceability.plan_by_ts`, `factory_dashboard.plan_levels` | `^TS-\d+$` / `TS-\d+` / ключ по колонке `ts` md-плана (`factory_dashboard.py:713`) |
| `plan-row: test-plan.md TS column -> validate_artifacts.check_plan` | строка плана с `P-1` в первой ячейке отброшена `startswith("TS-")`, раздел без строк → отказ «has no TS-* rows» (`validate_artifacts.py:806-808`) |
| `identity: plan-row id` (C2) | носители дают два вида: `P-n` (6 строк форм §3.2 + `handoff-keys.md:27,51,79`) против `TS-n` (`artifact-contract-plan.md:46`, `artifact-contract.md:63`) |
| `row-fields: obligation_refs <- manifest_from_tests@typescript|java|csharp -> window_record.row_field_gaps` | формы маркера есть только под `pytest` (`references/case-markers.json:5-8`); `manifest_from_tests` читает AST Python (`manifest_from_tests.py:15,311` по разведке t-356) — писателя для трёх языков нет |
| `accept: s7-analyst-to-automator[concerns].stage_acceptance.failure_class -> acceptance.stage_acceptance_errors` | в форме диспатча нет секции `stage_acceptance` (прочитана целиком, `handoffs/s7-analyst-to-automator.yaml:1-136`; Grep `stage_acceptance` по `handoffs/` находит её в 5 других контрактах — положительный контроль); обратный ход: читатель без писателя. СМЫСЛ строки (вердикт №21): секция приёмки S6 есть во ВТОРИЧНОМ контракте аналитика — `handoffs/s7-analyst-to-scribe.yaml:53-57` («Acceptance of the runner's handoff (X7-6), owed on `header.verdict: concerns`»), а читатель получает форму ДИСПАТЧА: `contract_of('S7','qa-failure-analyst')` → `s7-analyst-to-automator` (прогон критика t-401). Красная говорит «читатель смотрит в форму диспатча, секция живёт во вторичной» — от этого зависит направление починки FV1-22 (перенос секции в форму диспатча или чтение вторичной), выбор — узел FV1-22, не слой |
| `accept: s7-analyst-to-automator.inputs_read[-1].path -> stage_done.reviewed_author_dispatch` | строки `inputs_read` формы — `work/run-report.json` и `<the runtime_provenance record>` (`:64-69`), строки формы раннера нет → `""` (`stage_done.py:946-955`) |

Убрано фикс-раундом (вердикт №6, решение §10 №6): строка `agree: obligation_refs … s5_precheck vs controller finish` — проверка
хэша живёт внутри `Controller._s5_v2_collect` (`controller.py:7247,7293-7302` по вердикту t-401), функцией-читателем не
вызывается; её ловит П1-б финишем окна в сухой стори.

Зелёные контроли той же функции (без них «прогон ничего не обошёл»): `brief_pack.PLAN_ROW_RE` на `P-1`; приёмка форм S2/S3/S4
критика (`stage_acceptance` есть: `s2-stage-critic-to-tester.yaml:47`, `s3-stage-critic-to-strategist.yaml:50`,
`s4-case-critic-to-designer.yaml:94`); `obligation_refs@python`.

### 4.3 Вердикт по находкам в скоупе

| Находка | Вердикт |
|---|---|
| FV1-1 | caught by row `plan-row: s3.scope[].id -> contract.case_plan_row` и `… -> s5_precheck.case_plan_row` (C1) и `identity: plan-row id` (C2) |
| FV1-14 | caught by rows семейства RR-plan-row для каждого TS-only читателя (§3.4: `handoff_check._plan_row_of`, `grounding_table.TS_ID`, `check_delivery.TS_IN_TEXT`/`_case_map`, `contract.plan_levels`/`case_levels`, `traceability.plan_by_ts`, `validate_artifacts.check_plan`, `factory_dashboard.plan_levels`) и `identity: plan-row id`. Прежний негатив «`report_facts`, `validate_artifacts` не найдены» снят: шаблон `PLAN_ROW_RE|TS-\\d|TS-\(|\(TS-` не ловил литерал `"TS-"` (вердикт №20); `validate_artifacts.py:806-808` и `factory_dashboard.py:710-716` теперь в реестре. `report_facts` — N3 ищет точки входа Grep `TS-` без учёта регистра по `scripts/report_facts*.py` с положительным контролем `validate_artifacts.py:806` той же формы; не найденный — строка итога `unadapted readers` |
| FV1-19 | caught by row `row-fields: obligation_refs <- manifest_from_tests@{typescript,java,csharp}` (C3, дефект 1). Дефект 2 (ссылка без хэша проходит `s5_precheck`, финиш окна требует хэш) — **П1-б** (финиш окна в сухой стори; решение §10 №6). Дефект 3 (починка доходит до человека через exit_limit) — not caught: ход драйвера, слой П1-б |
| FV1-22 | caught by rows `accept: s7-analyst-to-automator[concerns].stage_acceptance.* -> acceptance.stage_acceptance_errors` и `accept: …inputs_read[-1].path -> stage_done.reviewed_author_dispatch` (поля приёмки); смысл первой строки записан в §4.2 (вердикт №21). Петля дирижёра (`tooling` без траты лимита) — not caught: П1-б |
| FV1-18 | not in П1-а (решение F5 (б)); план Lead §3 и §4 исправлены |
| FV1-12 | not in П1-а (решение F6 (а)); план исправлен |

---

## 5. Узлы для билдера (PROJECT.md «Командная работа» п. 11)

Порядок: **N0 → N1 → N2a → N2b → N2c → N2d → N3 → N4** — последовательно: N0–N3 делят `test_field_producers.py` и строку
`covers` в `test-layers.json`, N2a–N3 — `form_filler.py` и `form-fill-rules.json`; N4 читает раздел `hand_inputs` реестра N3.
Все пути — абсолютные под `C:\QAFactory\forge-repo\`. Перед стартом каждого узла билдер получает в «given» целиком
`ai-packages/qa-factory/design/factory-rules.md` и `plans/builder-rules.md` (PROJECT.md, приёмка пакета п. 1) — для N0–N3; N4 —
`tools/`, вне пакета, FR не проходит.

**Очередь на `test-layers.json` (решение §10 №17).** Строка `очередь:` для пачки:
`очередь: test-layers.json — PC4-15, FG7-15, FG7-19 (их порядок между собой — их пачек) → П1-а N0 → N1 → N2a → N2b → N2c → N2d → N3 → П1-б N3 → П1-в N4`.
Каждый узел П1-а трогает в `test-layers.json` только `covers` строки `test_field_producers.py`. N4 файл не трогает.

### N0 — помощник `known_red` (первым; П1-б N1 его импортирует)

owns:
`C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\known_red.py`
`C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_field_producers.py` (только новая функция `known_red_ledger_cases`)
`C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test-layers.json` (только `covers` строки `test_field_producers.py`: `tests/known_red.py`)

| Пункт | Файл, функция | Ожидаемое поведение | Строка теста |
|---|---|---|---|
| 1 | `known_red.py`: `Row`, `Verdict`, `LedgerError`, `load`, `reconcile` | ровно §3.6: форма строки, таблица исходов, края `load`; печать — `problems` по id, затем `known` | — |
| 2 | `test_field_producers.py`: `known_red_ledger_cases` | одна параметризованная таблица; id строки = имя случая | строки: `known red passes`, `new red refused with door`, `stale green refused`, `unknown row refused`, `green without row ok`, `empty ledger: every red is new`, `empty results with rows: every row unknown`; края `load`: `missing file`, `section absent = empty`, `duplicate id`, `whitespace id`, `blank raised_by`, `null raised_by`, `bad node fv1-1`, `extra key`; неудобные входы §3.6: `case-different id stays red`, `kind-level row does not cover variant` |
| 3 | `test-layers.json` | `covers` += `tests/known_red.py` (правило `test_selftest_slow_tests.py:485-486`) | — |

edges: §3.6 целиком; E14, E16, E17. siblings: ось 18 (новый храповик — строки оси пишет узел Lead, сажается вместе, §9 R7);
ось 34 (одна сверка для двух слоёв).
DoD: `python -B C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\scenario_walk.py --witness-for ai-packages/qa-factory/scripts/tests/known_red.py ai-packages/qa-factory/scripts/tests/test_field_producers.py ai-packages/qa-factory/scripts/tests/test-layers.json`
и каждый файл, который оно напечатает, плюс сам `test_field_producers.py`, если команда его не назвала (строка отчёта). Ожидание:
зелёный; отчёт прикладывает строки таблицы с исходами.

### N1 — заполнитель и круг «форма → своя проверка»

owns:
`C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\form_filler.py`
`C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\form-fill-rules.json`
`C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_field_producers.py`
`C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test-layers.json` (только `covers` строки `test_field_producers.py`)

| Пункт | Файл, функция | Ожидаемое поведение | Строка теста |
|---|---|---|---|
| 1 | `form_filler.py`: `ABSENT`, `FillContext`, `Fill`, `Unfillable`, `Filled`, `NotFillable`, `variants`, `fill_form` (с `overrides`), `write_dispatch_form` (интерфейс §3.5) | контракт читается только через `handoff.index/template/spec/is_placeholder/set_value`; правило выбирается по таблице `form-fill-rules.json` (вид §3.2 → генератор); `left_for_code` = пути, для которых `handoff_check._code_fills(path)` истинно (импорт, не копия; тот же источник, что `DERIVERS`/`LIST_DERIVERS`/`BY_LEAF`); `overrides` — E20; приоритет выпуска/цитаты — §3.5 | строки таблицы «подсказка → значение» для каждого неудобного входа §4.1 (одна параметризованная таблица) и строки E20 (`override missing path`, `ABSENT on required`, `override on code field`, `section[] vs section[0]`) |
| 2 | `form-fill-rules.json` | ключи: `rules` (вид → генератор, порядок применения), `context_tokens` (`<TICKET>`, `<dispatch>`, `<the author's dispatch>` → ключ `FillContext`), `artifact_templates` (пусто в N1; заполняют N2a–N2d), `not_covered` (пусто в N1) | — |
| 3 | `test_field_producers.py`: новая функция `every_form_fills_from_its_own_hints` | для каждого контракта множества §3.4 (`handoffs` ∪ `escalation`) × `variants()`: `fill_form`, мир из `harness.temp_dir` ОДИН раз, `handoff_check.check(doc, contract, Artifacts(root, dispatch=...), fix=False, use_judge=False)`; проблема `kind == "blank"` при `_code_fills(path)` не красная (E11); ожидание по E4–E6, E13 (принять / обязан отказать); каждая `Unfillable` — красная строка; `role-to-conductor` — E19 | id строки = `<contract>[<verdict>/<variant>]`; итог печатает `forms N, variants M, fields F, unfillable U, left_for_code L` |
| 4 | там же: пины размера обхода в обе стороны, без литералов (вердикт №1, `docs/TESTING.md:95`) | множество контрактов обхода = имена `handoffs/*.yaml` минус `index`, `vocabulary` — в обе стороны (лишний файл без строки реестра — красная `form file not in index: <x>`; строка реестра без файла — красная `index names no file: <x>`); число вариантов каждой формы ≥ числа слов `header_verdicts` словаря (у формы без `header.verdict` — ≥ 1) | обход, который ничего не обошёл, красный |
| 5 | `test-layers.json` строка `test_field_producers.py` `covers` += `tests/form_filler.py`, `handoff.py`, `handoffs/*.yaml` (по одному пути на контракт — как принято в файле; включая `handoffs/role-to-conductor.yaml`) | `scenario_walk.py --witness-for` выбирает тест при правке формы или заполнителя; правило импортов `test_selftest_slow_tests.py:485-486` выполнено | — |

edges: §4 E1–E6, E10, E11 (часть N1), E12–E15, E19, E20. siblings: ось 28 (форма строки — текст роли), ось 21 (запись md-строк через
`grammar.escape_cell`).
DoD: `python -B C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\scenario_walk.py --witness-for ai-packages/qa-factory/scripts/tests/form_filler.py ai-packages/qa-factory/scripts/tests/fixtures/form-fill-rules.json ai-packages/qa-factory/scripts/tests/test_field_producers.py`
и каждый файл, который оно напечатает, плюс сам `test_field_producers.py`, если команда его не назвала. Ожидание: зелёный, ИЛИ
красные строки только вида `unfillable …` и `form-kind-unread …`, перечисленные в отчёте билдера списком (это находка формы, а не
дефект заполнителя; Lead решает: правило заполнителя или правка формы). Замер добавки ко времени файла — обязательная строка
отчёта (вердикт №37); больше 10 с — число в отчёте, решает Lead.

### N2a–N2d — `fill_artifact` по группам стадий (решение §10 №4 (а))

Общее для четырёх узлов (каждый — отдельный узел и коммит, последовательно):

owns (каждого из N2a, N2b, N2c, N2d):
`C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\form_filler.py` (только `fill_artifact`, `classify`, `stage_outputs`, `write_outputs` и генераторы своей группы)
`C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\form-fill-rules.json` (только строки `artifact_templates` и `not_covered` своей группы)
`C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_field_producers.py` (только строки своей группы в таблице `every_stage_output_fills_or_is_named`)
`C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test-layers.json` (только `covers` строки `test_field_producers.py`: `validate_artifacts.py`, `references/stages.json`, `references/artifact-writers.json` и контракты своей группы из §3.7)

Строка `artifact_templates`: `{"<выход или подвид>": {"contract": "<references/... путь>", "anchor": "<дословная строка контракта>",
"format": "md|json|yaml", "template": <текст или JSON/YAML-скелет с подсказками <…>>, "required": ["<путь поля>"],
"file_name": "<шаблон имени для выхода-каталога, напр. <area>/<case id>.md>"}}`. Подсказки шаблона заполняются теми же правилами,
что формы (§3.2). Строка `not_covered`: `{"<выход>": "<причина, одна строка>"}`.

Таблица `every_stage_output_fills_or_is_named` (C8; одна параметризованная таблица, строка на ВИД выхода):
- для каждого имени из `stage_outputs()`: `classify` — ровно один из трёх; `роль` без строки шаблона и без строки `not_covered` —
  красная `output <x>: role-written, neither template nor not_covered`; E23;
- `FilledArtifact` → `write_outputs` в мир (E22) → `validate_artifacts.collect_errors(path, cfg)` = `[]`; затем сломанный вариант
  (`overrides` с `ABSENT` на `required[0]`) → хотя бы одна ошибка, иначе имя в итоге `outputs no reader refuses` (E7);
- `ByCode` → строка проверяет только, что писатель назван (`writer` из `artifact-writers.json`); итог `by code: N`;
- `NotCovered` → итог `not covered: <output> — <why>`, не красная (E21);
- подвиды — своя строка каждый (`case`, `plan_md_row`, `plan_json_row`, `manifest_row`, `first_look_rows`, `test_file:<lang>`);
- id строки = `output: <имя>[<variant>]`.

| Узел | Группа (§3.7) | Что добавляет | Особое |
|---|---|---|---|
| N2a | S0–S2 | `ABSENT`-правки артефактов, `FilledArtifact`/`ByCode`/`NotCovered`, `classify`, `stage_outputs`, `write_outputs`, сама таблица C8 со строками ВСЕХ стадий: свои выходы — по §3.7, выходы групп N2b–N2d — временно `not_covered` с причиной «group N2x not landed» (E16); шаблоны `work/context-manifest.json`, `work/requirements-register.md`, `work/requirements-readiness.json`, `understanding.md`; `not_covered`: `work/impl-diff.txt` | пины обхода в обе стороны против `stages.json` (без литерала числа) |
| N2b | S3–S4 | шаблоны `test-plan.md` (+ `plan_md_row`), `work/test-plan.json` (+ `plan_json_row`), `work/grounding.yaml` (разделы кода — `left_for_code`), `work/test-cases/` (`case`, файл на `ctx.cases`), подвид `first_look_rows`; снимает свои строки «group N2b not landed» | приоритет выпуска/цитаты (§3.5): кейс — `Plan row: <ctx.minted P-1>` базой и вариант `cite_hint` с `TS-1` |
| N2c | S5–S6 | подвиды `manifest_row` (форма строки `REQUIRED_ROW_FIELDS`), `test_file:<lang>` (маркер по `case-markers.json`; нет формы — `Unfillable`, E9); `not_covered`: `work/s5-plan.json`, `work/s5-notes/`, `work/evidence/manual/<case>/tried.md`, если правило ниже не дало шаблона | для `work/s5-plan.json`: если вызов скелета `s5_plan` в мире даёт файл с подсказками `<…>` — заполнить их правилами §3.2 и перевести выход в `FilledArtifact`; нет подсказок — остаётся `NotCovered` с причиной из §3.7 |
| N2d | S7–S9 | шаблоны `work/triage.json`, `work/bug-drafts/` (файл на `ctx.bugs`), `test-report.md`, `project:bugs/`, `retro.md`; `project:obligations.md` и `project:factory-backlog.md` — шаблон, если раздел `references/artifact-contract.md:172` задаёт форму, иначе `not_covered` с причиной «no shape in artifact-contract.md:172» | после N2d в таблице нет строк «group N2x not landed» |

edges (все четыре): E7, E9, E16, E20–E24. siblings: ось 21 (md-строки через `grammar.escape_cell`), ось 5 (двойники ролей по
стадиям — одна таблица на все стадии), ось 34 (один путь для всех языков в `test_file:<lang>`).
DoD каждого: `python -B C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\scenario_walk.py --witness-for ai-packages/qa-factory/scripts/tests/form_filler.py ai-packages/qa-factory/scripts/tests/fixtures/form-fill-rules.json ai-packages/qa-factory/scripts/tests/test_field_producers.py`
и напечатанные файлы, плюс сам `test_field_producers.py`. Ожидание: зелёный; итог печатает `by code`, `not covered` (поимённо),
`outputs no reader refuses` (поимённо); число `not covered` после узла не больше, чем до него (строка отчёта «до → после»).

### N3 — круги к читателям, круг дериверов, обратный ход, реестр

owns:
`C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\form-rounds.json`
`C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_field_producers.py`
`C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test-layers.json` (только `covers` той же строки)

| Пункт | Файл, функция | Ожидаемое поведение | Строка теста |
|---|---|---|---|
| 1 | `form-rounds.json` | ключи: `readers` (id, вызываемое `module:function`, семейство, поле-селектор, предикат `returns_value` / `accepts` / `refuses`), `identity_groups` (логический факт → носители: путь формы или якорь контракта), `languages_source` (по F3 (а)), `known_red` (форма строки §3.6), `hand_inputs` (`{"<семейство>": ["<регулярка рукописного входа>"]}` — читает только `tools/lint_ratchet.py`, N4). Начальные `hand_inputs` — только для `RR-plan-row`: `Plan row:\s*TS-\d+` и `"plan_row"\s*:\s*"TS-\d+"` (решено мной, §8.2) | — |
| 2 | `test_field_producers.py`: `every_reader_takes_what_its_writer_writes` (C1) | для каждой строки `readers` подать значение из заполненной формы/артефакта (`fill_form`/`fill_artifact`); предикат как в реестре; читатели §3.4 включая `validate_artifacts.check_plan` и `factory_dashboard.plan_levels` | id = `<family>: <writer-path> -> <reader>`; красная печатает пару и значение |
| 3 | там же: `every_derived_field_meets_its_deriver` (E11, перенесено из N1, решение §10 №1/№2) | мир с артефактами `fill_artifact` (кейсы, план, манифест — то, что читают дериверы); каждая форма × базовый вариант: `check(fix=True, use_judge=False)`; деривер вернул `None` → красная; каждое поле, пропущенное в N1 по `_code_fills`, встречено здесь — иначе красная `unjudged <contract>:<path>` (§4.1) | id = `derive: <contract>:<path>` |
| 4 | там же: `one_fact_one_form_everywhere` (C2) | вид id каждой группы одинаков у всех носителей; вариант `cite_hint` (§3.5) — носитель цитаты по своей подсказке | id = `identity: <group>`; печатает носители по видам |
| 5 | там же: `every_demanded_field_has_a_writer_for_every_language` (C3) | требования из `stage_acceptance` (форма по `acceptance_by`/`consumer_of`), `REQUIRED_ROW_FIELDS`, `tool_fields`; писатель по `filled_by`; `marker` — `manifest_from_tests` на `test_file:<lang>` для каждого языка `languages_source` | id = `<field> <- <writer>@<lang> -> <reader>`; нет писателя → `<none>` |
| 6 | там же: `readers_of_one_field_agree` (C4) | один вход — один вердикт у всех читателей поля, вызываемых функцией (строки `readers`); строки финиша окна контроллера нет (решение §10 №6) | id = `agree: <field>` |
| 7 | там же: `red_rows_equal_the_known_red_ledger` (C6) | собрать `results` всех строк п. 2–6 и строк `unfillable` N1 (id → зелёная/красная; исключение = красная); `known_red.load(form-rounds.json)`, `known_red.reconcile(...)`; печать — вывод помощника | — |
| 8 | `covers` += модули читателей §3.4, `tests/fixtures/form-rounds.json`, `references/case-markers.json`, `references/detectors.json`, `references/artifact-contract.md`, `references/artifact-contract-plan.md` | правка читателя выбирает тест в `--witness-for` | — |

edges: E1, E2, E7–E9, E11, E14, E16, E17. siblings: оси 23, 27, 34, 18.
DoD: `python -B C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\scenario_walk.py --witness-for ai-packages/qa-factory/scripts/tests/fixtures/form-rounds.json ai-packages/qa-factory/scripts/tests/test_field_producers.py`
и напечатанные файлы, плюс сам `test_field_producers.py`. Ожидание: зелёный при `known_red`, равном списку §4.2 (отчёт прикладывает
дословный вывод с красными строками ДО внесения их в реестр — это доказательство, что слой краснеет на дефектах main; у каждой
внесённой строки `raised_by` = «t-401 plan review + N3 first measurement, <дата>»). Отрицательный контроль (вне теста, в DoD):
копия `form-rounds.json` без одной строки `known_red` → тест красный `new red: <id>` (байтовая копия, хэш до/после; живой файл
не портится). Замер добавки ко времени файла — строка отчёта.

### N4 — строка рукописных входов в общем храповике (`tools/`, вне пакета; решение §10 №5)

owns:
`C:\QAFactory\forge-repo\tools\lint_ratchet.py`
`C:\QAFactory\forge-repo\tools\lint-baseline.json`
`C:\QAFactory\forge-repo\tools\test_lint_ratchet.py`

| Пункт | Файл, функция | Ожидаемое поведение | Строка теста |
|---|---|---|---|
| 1 | `lint_ratchet.py`: новый источник `hand_input_findings(repo) -> list[Finding]` | читает `ai-packages/qa-factory/scripts/tests/fixtures/form-rounds.json` раздел `hand_inputs`; сканирует `ai-packages/qa-factory/scripts/tests/test_*.py`, кроме файлов раздела `quarantine` `scripts/tests/test-layers.json` и кроме `test_field_producers.py` (слой сам); каждое совпадение в строке → `Finding(rel, line, "HandReaderInput", (<семейство>,), <совпавший текст>)`; identity = (путь, класс, семейство), без строки — как у pyflakes (`lint_ratchet.py:17-18,66-68`) | — |
| 2 | там же, `run` | находки источника подмешиваются к НЕфатальным до `counts` (`:190-192`, E18); база, двери `DOOR_NEW`/`DOOR_STALE`, `--update` с печатью `added`/`grew` (`:215-220`) — те же; источник работает, только когда `ai-packages/qa-factory/scripts` среди корней; иначе строка вывода `hand-input line: not run (package scripts root not among --root)` | — |
| 3 | края | `form-rounds.json` нет, не JSON или `hand_inputs` не объект → выход 2 «cannot judge» с путём (никогда не пропуск, как прочие случаи выхода 2, `:30-32`); регулярка не компилируется → выход 2 с семейством и текстом; `test-layers.json` не читается → выход 2; pyflakes не установлен → выход 2, как сегодня (`:169-178`) — строка не судится отдельно | — |
| 4 | docstring `lint_ratchet.py` | «что охраняет» дополняется второй строкой: число рукописных входов читателей слоя П1-а только убывает | — |
| 5 | `test_lint_ratchet.py` | строки таблицы (новый случай — строка, не файл): `new hand literal -> exit 1 new finding`, `removed literal -> exit 1 stale`, `quarantined file not counted`, `bad regex -> exit 2`, `missing form-rounds.json -> exit 2`, `package root not among --root -> not run line` | id = имя случая |
| 6 | `lint-baseline.json` | `python tools/lint_ratchet.py --update` после правки; вывод `added:` по каждой строке `HandReaderInput` — в отчёт и коммит (AR-20 «list every row added», `design/architecture.md:222`) | — |

edges: N4 п. 3; E18. siblings: ось 18 (член — строку оси пишет узел Lead, сажается вместе, §9 R7); AR-20 Carriers уже называют
`dev:tools/lint_ratchet.py` (`design/architecture.md:217`).
DoD (путь вне пакета — тест, который его судит): `python -m pytest tools/test_lint_ratchet.py -q` и
`python -B C:\QAFactory\forge-repo\tools\lint_ratchet.py --check` (зелёный после `--update`; вывод `--update` со строками `added:` в
отчёте).

---

## 6. Четыре вопроса (CLAUDE.md правило 10)

(a) Цена и кто платит. CI: до 10 с к `test_field_producers.py` (мир один раз; замер — строка отчёта N1 и N3); `lint_ratchet` —
один проход регулярок по тестовым файлам. Авторы пакета: новая подсказка формы или новый выход стадии, не покрытые правилом,
краснят слой — автор добавляет строку правила/шаблона или `not_covered` с причиной тем же коммитом. Узлы починки FV1: удаляют свою
строку `known_red` тем же коммитом. Новый читатель id: строка в `readers` (и шаблон рукописного входа в `hand_inputs`, если есть).

(b) Оси SIBLING_MAP (`docs/SIBLING_MAP.md`, 36 осей), механизм «слой П1-а» (включая помощник `known_red` и строку `lint_ratchet`):
- axis 1: n/a — правила форджа, ролей и журнала не меняются; вопрос критика и поле находки из плана §6 — узел Lead (§9 R5, R6).
- axis 2: n/a — экзаменов тиров не касается.
- axis 3: covered — файлы в `scripts/tests/` едут в релизной копии, поведение установленного плагина не меняют.
- axis 4: covered — `known_red` указывает узлы пачек, не правила FR и не замороженный BACKLOG.
- axis 5: covered — формы и выходы всех стадий обходятся одной таблицей; приёмка S2/S3/S4 и S6-потребителя — одно семейство.
- axis 6: n/a — не измеритель (П1-в).
- axis 7: n/a.
- axis 8: covered — мир во временном корне через `harness.temp_dir`, раскладка `qa-factory/artifacts/<task_key>/` (E22).
- axis 9: covered — имена тестовых файлов языков такие, что `test_files.is_test_for` их узнаёт (один лист).
- axis 10: n/a. axis 11: n/a.
- axis 12: covered — строки `known_red` цитируют узлы пачек; в `plans/BACKLOG.md` ничего.
- axis 13: n/a. axis 14: n/a. axis 15: n/a.
- axis 16: covered — данные слоя читаются одним читателем JSON; `artifact-writers.json` — через `hooklib.load_ref_json`.
- axis 17: covered — читатели вызываются функцией; если читатель доступен только через CLI, его вывод разбирается только `detector_verdict.parse`.
- axis 18: covered через узел Lead — два храповика (`known_red`, `HandReaderInput`) вносит в таблицу оси узел «носители П1», сажается вместе с N0 и N4 (§9 R7).
- axis 19: n/a. axis 20: n/a.
- axis 21: covered — строка md-плана пишется `grammar.escape_cell`, читается `contract.parse_plan`.
- axis 22: n/a.
- axis 23: covered — обратный ход берёт поля строки только из `REQUIRED_ROW_FIELDS`, третьего списка нет.
- axis 24: n/a. axis 25: n/a. axis 26: n/a.
- axis 27: covered — вариант `profile_id` через `execution_request` (`profiles_owning`, `entry_profile_id`).
- axis 28: covered — форма строки, напечатанная `manifest_from_tests._row_form`/`s5_precheck`, заполняется как форма роли.
- axis 29: n/a — слой ничего не дописывает в jsonl репозитория.
- axis 30: n/a — решение F5 (б): команды профиля не в П1-а.
- axis 31: n/a.
- axis 32: covered — все проверки класса данных; тесты вне переписи.
- axis 33: n/a — заполнитель не выбирает dispatch, id берёт из контекста.
- axis 34: covered — языки из таблицы данных, ни один не исключён; необслуживаемый язык — красная строка (F3 (а)); один помощник `known_red` для двух слоёв.
- axis 35: n/a.
- axis 36: n/a — `ledger.open_placeholder_rows` про строки на подмене, не про плейсхолдеры форм (совпадение слова).

Новая ось — требование R2 к узлу Lead (§9).

(c) Детектор отказа самого механизма: пины размера обхода в обе стороны против носителей (N1 п. 4, N2a — против `stages.json`,
N3 — число строк `readers` и семейств); зелёные контроли §4.2; храповики — калибровочная проверка (номер даёт узел Lead, §9 R4) и
`lint_ratchet --check` в CI `forge-check`. Детектор пропуска читателя, не внесённого в реестр, — «на дисциплине» с двумя
детекторами утечки, которые СОЗДАЁТ узел Lead (решение §10 №19): вопрос критика «подан ли читателю выход сегодняшнего писателя —
приложенный прогон П1-а» (§9 R5) и поле находки живого прогона «какой слой ниже должен был поймать» = П1-а (§9 R6). До посадки
узла Lead этот детектор — пожелание (правило 10 (c)); это записано, не скрыто.

(d) Что не даёт пропустить: строка `keep` → канон CI (`selftest.py` гоняет всё, кроме `quarantine`, `docs/TESTING.md:75`);
`covers` делает тест частью `--witness-for` любого узла, трогающего форму, выход стадии, заполнитель или читателя;
`lint_ratchet --check` — в CI `forge-check` (`design/architecture.md:220`).

---

## 7. Пересечения с работой в ходу

| Пачка | Узел | Конфликт | Что делать |
|---|---|---|---|
| `package-ci/4` | PC4-15 (интегратор пишет `test-layers.json` `covers`, `plans/piles/package-ci/batch-4-dieta-testov-td-11-td-15.md:36`) | тот же файл, что N0–N3 | строка `очередь:` §5 (решение §10 №17): PC4-15 раньше узлов П1-а |
| `forge/7` | FG7-15, FG7-19 (`plans/piles/forge/batch-7-vhodyashchie-4.md:38,42` по вердикту t-401, мной не перечитано; owns `scenario_walk.py`, `test-layers.json`) | тот же `test-layers.json`; FG7-19 меняет обходчик, которым считается свидетель | строка `очередь:` §5: FG7-15, FG7-19 раньше узлов П1-а |
| П1-б, П1-в (параллельные спеки) | П1-б N1 (импорт `known_red`), П1-б N2 (заполнитель), П1-б N3 и П1-в N4 (`test-layers.json`) | П1-б N1 не стартует до N0; П1-б N2 — до N2d (полный перечень выходов) или с `NotCovered` → `live_only`; `test-layers.json` — очередь §5 | порядок §5 и E16 |
| `package-ci/4` | PC4-2/PC4-4/PC4-5 (резка `report_facts`, `gate_brief`, `probe_by_code`, `gate_preflight`, `controller` на части за фасадом) | реестр читателей держит `module:function`; после резки функция живёт в части | фасад сохраняет старые имена (`module_facade.install`); слой вызывает через фасад; ничего не ждёт |
| `package-ci/4` | PC4-17 (фаза 2 детекторов, строки-замены) | `test_field_producers.py` — `data_join`, не `detector` | нет |
| `live-run-fvf/1` | FV1-1, FV1-14, FV1-19, FV1-22 | их починки меняют читателей/формы → строки `known_red` зеленеют | порядок плана §4: слой первым; DoD узла починки называет id своей строки и удаляет её тем же коммитом. Неслитые ветки: FV1-1 t-152/t-162 (`worktree-agent-a02fafab496f0a9f6`), t-180, t-186 (`batch-1-live-run-fvf.md:68-80`) — при слиянии в main строки реестра станут «устаревшими» (отказ C6) |
| `roles-context/2` | RC2-1 (`brief_pack.py (question_answer_lines)`, слова человека целиком) | решение F7 (а): строка «слова → brief_pack» красная до RC2-1 | строка в `known_red` с узлом RC2-1 |
| `roles-context/2` | RC2-6 (`references/artifact-contract-plan.md`), RC2-5 (`references/handoffs.md`) | якоря шаблонов артефактов (F8 (а)) | правка контракта краснит якорь — узел обновляет якорь тем же коммитом |
| (план §6) `thinking-roles/5`, `live-runs/2` | не прочитаны (вне манифеста) | — | — |

---

## 8. Развилки, возвращённые Lead

| id | Вопрос | Варианты и последствия | Рекомендация |
|---|---|---|---|
| F1 | Где живёт тест | (а) функции в `test_field_producers.py` (keep `data_join`, AR-21/22) — по `docs/TESTING.md` без правки, рост файла; (б) в `test_stage_joints.py` (`gate_named`, `selftest --contracts`) — смешивает обход имён и значений; (в) новый файл `test_form_rounds.py` + строка keep — нарушает «новый тестовый файл не создаётся» (`docs/TESTING.md:117`), нужна F2 | (а) — РЕШЕНО Lead |
| F2 | Правка `docs/TESTING.md` | (а) не править: слой 2 уже «поле, которое одна стадия пишет, а другая читает»; (б) одна фраза: «стык проверяется значением, которое производит сегодняшний писатель, не рукописным входом» — делает правило П1-а видимым всем узлам | слово владельца — РЕШЕНО Lead (вопрос задан) |
| F3 | Строки «языков» для обратного хода | (а) `detectors.json` `assertion_probes` ∪ `assertion_probes_ast` — 4 языка, ключ возможности оси 34; (б) `code_extensions` — 20; (в) `run_forms` — 22 раннера | (а); (в) для писателей с ключом раннера — РЕШЕНО Lead |
| F4 | Красный слой на main против зелёного канона | (а) реестр `known_red`; (б) слой садится вместе с починками; (в) слой только в `quarantine-watch` | (а) — РЕШЕНО Lead; форма — один помощник §3.6 (решение §10 №3) |
| F5 | FV1-18 в П1-а | (а) поддельный раннер; (б) не в П1-а | (б) — РЕШЕНО Lead |
| F6 | FV1-12 в П1-а | (а) не П1-а; (б) строка сравнения ролей | (а) — РЕШЕНО Lead |
| F7 | К3 (слова человека) в П1-а | (а) семейство «значение целиком» с `known_red` → RC2-1; (б) оставить П1-б | (а) — РЕШЕНО Lead |
| F8 | Контракты артефактов (проза md) как формы | (а) шаблоны строками данных с дословным якорем; (б) разбор md кодом | (а) — РЕШЕНО Lead |
| F9 | Дом счётчика рукописных входов | (а) база в `form-rounds.json`, свой тест; (б) строка `tools/lint_ratchet.py` | **(б) — РЕШЕНО Lead 13.11 при фикс-раунде (решение §10 №5; прежнее (а) отменено)**; узел N4 |
| F10 | Какая форма id строки плана «правильная» | НЕ решается слоем: слой показывает два вида; выбор — узел FV1-14 | — (указатель) |
| F11 (новая) | Собственная таблица теста помощника `known_red` (N0 п. 2) против `docs/TESTING.md:55` («Чего больше нет: … «мини-батареи» на внутреннюю функцию») | (а) таблица в `test_field_producers.py`, как в N0: помощник — ГЕЙТ канона двух слоёв, его направление ошибки (§3.6) иначе ничем не охранено; цена — ~17 строк таблицы; (б) своих строк нет: помощник проверяется только реальным реестром N3 и отрицательным контролем в DoD N3 — неудобные входы §3.6 (регистр, префикс вида, пустой `raised_by`) остаются без проверки до П1-б | (а); DoD брифа Lead требует «its test», но потолок `docs/TESTING.md` — слово владельца 10.11, поэтому возвращаю: если Lead читает `:55` строго — вопрос владельцу вместе с F2 |
| F12 (новая) | Кто пишет строку вопроса 9 `docs/tasks/critic-diff-brief.md` для двух храповиков | Решение §10 №17 перечисляет для узла Lead SIBLING_MAP, `architecture.md`, калибровку, вопрос критика «подан ли читателю…», поле находки — `critic-diff-brief.md` вопрос 9 не назван, а AR-20 требует его «в коммите, создающем храповик» (`design/architecture.md:222`). (а) узел Lead «носители П1» берёт и его (одна посадка, R7); (б) узел этой спеки получает `critic-diff-brief.md` в owns — противоречит духу №17 (документы Lead не пишутся узлами спек) | (а) — записано как требование R3 (§9) до слова Lead |

### 8.1 Расхождения брифа/плана и наблюдения, замеченные по ходу (не расширяю скоуп)

- (снято) План §3 П1-а «ловит FV1-18, FV1-12» — план исправлен решениями F5, F6.
- План §6 относит к плану AR-24, AR-25; для П1-а AR-25 не затронут, AR-24 — по решению F7 (а).
- Единой таблицы «языки/раннеры», на которую ссылается план, в пакете нет — решение F3 (а).
- `references/artifact-registry.json` — второй носитель писателя (`producer`) для части выходов, с другими именами ролей и
  путём readiness (§3.7, конец) — класс «одна сущность — два носителя» (AR-14/AR-15); слой читает только `artifact-writers.json`.
  Предлагаю находку в `package-ci` (решение — Lead).
- `role-to-conductor`: половину `request` рендерит код из секции `blocked` формы роли (`handoff_help.py:93-119`); существующий тест
  записывает её как «never walked» обходом null-исходов (`scripts/tests/test_null_outcomes.py:366`, Q-N0-8). Круг П1-а теперь
  её обходит (вердикт №1) — это другой обход, противоречия нет, но настоящий писатель `request` (код из `blocked`) этим кругом не
  проверяется; строка «секция `blocked` каждой формы → `handoff_help` → читатель» была бы точнее — не добавляю, предлагаю Lead.
- Правило покрытия импортов (`test_selftest_slow_tests.py:485-486`): строка `keep` теста П1-б, импортирующего `known_red.py`,
  обязана перечислить `tests/known_red.py` в `covers` — сообщено узлу Lead (§9 R8) для спеки П1-б.

### 8.2 Мелкие технические решения, закрытые мной

- Заполнитель — `scripts/tests/form_filler.py`, помощник `known_red` — `scripts/tests/known_red.py` (помощники рядом с
  `harness.py`), не `scripts/` пакета: ими пользуются только тесты (П1-а, П1-б).
- Два файла данных (`form-fill-rules.json` у N1–N2d, `form-rounds.json` у N3).
- Поле или выход без зарегистрированного читателя — строка итога, не красная (E7); выход — с проверкой сломанным вариантом.
- Варианты `header.verdict` — все 4 слова словаря; выбор прочих полей — первое значение (иначе комбинаторный взрыв).
- Приоритет выпуска/цитаты id (вердикт №22): базой — выпущенное значение, плюс вариант `cite_hint` с дословным префиксом
  подсказки; не дизайн-выбор, потому что строятся ОБА вида и каждый судится (§3.5).
- Требование П1-б «незаполнимое — исключение»: интерфейс возвращает записи `Unfillable` и даёт `require()`, который бросает
  `NotFillable` — оба пути из одного результата.
- Шаблон `node` в `known_red`: `^[A-Z][A-Z0-9]*-[0-9]+[a-z]?$`; отсутствие раздела `known_red` в существующем файле — пустой реестр,
  отсутствие файла — отказ.
- Начальные `hand_inputs` — только семейство `RR-plan-row` (два шаблона); расширение — строка реестра и `--update` с причиной.
- `fill_artifact` режется на 4 узла ПОСЛЕДОВАТЕЛЬНО (общие `form_filler.py` и `form-fill-rules.json`); параллель потребовала бы
  файл на группу — не стоит выигрыша на узлах такого размера.
- Классификация выходов — по `artifact-writers.json` (носитель «one artifact, one writer», который держит `test_artifact_writers.py`,
  aw:3), предикатом `driver_runner.py:1044`; своей таблицы писателей у слоя нет.

---

## 9. Требования к узлу Lead «носители П1» (решение §10 №17/№19; узлы этой спеки эти файлы НЕ пишут)

| id | Носитель | Что нужно от П1-а | Когда |
|---|---|---|---|
| R1 | `ai-packages/qa-factory/design/architecture.md` | AR-22 «Detector» (`:236`): назвать круг значений П1-а (`test_field_producers.py`: `every_form_fills_from_its_own_hints`, `every_reader_takes_what_its_writer_writes`, `every_derived_field_meets_its_deriver`, `every_demanded_field_has_a_writer_for_every_language`, `every_stage_output_fills_or_is_named`); AR-10 «Detector» (`:116`): обратный ход П1-а; AR-20 «Carriers» (`:212-219`): `scripts/tests/known_red.py` с реестрами-потребителями и строка `HandReaderInput` в `dev:tools/lint_ratchet.py` | R1 по AR-20 — вместе с N0/N4 (R7); по AR-22/AR-10 — после N3 |
| R2 | `docs/SIBLING_MAP.md` | новая ось «плейсхолдер формы / выход стадии ↔ заполнитель (`form-fill-rules.json`) ↔ реестр читателей (`form-rounds.json`) ↔ писатель (`artifact-writers.json`)»: новое поле формы, новый выход стадии или новый читатель id — строка в реестре тем же коммитом; ось 18 — два члена (`known_red` через помощник; `HandReaderInput`) | ось 18 — вместе с N0/N4 (R7); новая ось — после N3 |
| R3 | `docs/tasks/critic-diff-brief.md` | вопрос 9 (храповики): `known_red` (рост — построчный `raised_by`, сверка `known_red.reconcile`) и `HandReaderInput` (рост — `--update` с `added:` в коммите) | вместе с N0/N4 (R7); развилка F12 |
| R4 | `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md` | ОДНА проверка на три спеки (номер даёт Lead): тренд числа строк `known_red` (П1-а и П1-б) и базы `HandReaderInput`; находки живых прогонов с полем «какой слой ниже должен был поймать» = П1-а | после N3 |
| R5 | вопрос критика (бриф критика диффа) | «подан ли читателю выход сегодняшнего писателя — приложен вывод прогона П1-а (`test_field_producers.py`)?» — для диффов, меняющих форму, выход стадии или читателя id | после N3 |
| R6 | форма находки живого прогона | поле «какой слой ниже должен был поймать» (значения: П1-а, П1-б, П1-в, нет) | после N3 |
| R7 | посадка | строки AR-20 Carriers (R1), оси 18 (R2) и вопроса 9 (R3) сажаются в ТОМ ЖЕ коммите или слиянии пачки, что N0 (`known_red`) и N4 (`HandReaderInput`) — AR-20 change check (`design/architecture.md:222`), вердикт №23 | N0, N4 |
| R8 | спека П1-б (через Lead) | строка `keep` теста П1-б, импортирующего `known_red.py`, перечисляет `tests/known_red.py` в `covers` (`test_selftest_slow_tests.py:485-486`); П1-б зовёт только `known_red.load`/`reconcile` (§3.6) и ключует строки `(<ключ цен или маршрут>, <вариант>)` | при фикс-раунде П1-б |

---

## Решения Lead по развилкам (13.11.2026, при приёмке черновика t-396)

- F1 (а): тест живёт в `test_field_producers.py`.
- F2: правка `docs/TESTING.md` — слово владельца; вопрос задан вместе с F2 спеки П1-б. До ответа — (а), текст не меняется.
- F3 (а): языки — из `detectors.json`; (в) только для писателей с ключом раннера.
- F4 (а): реестр `known_red`. ОДИН механизм с П1-б (её F8): одинаковое имя ключа, одинаковое значение (`FV1-n` или id
  узла) и одинаковый строгий режим — строка, позеленевшая без снятия метки, красная (AR-15, P31). Поведение проверки
  C6 этой спеки приводится к этому при фикс-раунде, если расходится.
- F5 (б): FV1-18 не в П1-а; план Lead §3 и §4 исправлены.
- F6 (а): FV1-12 не в П1-а; план исправлен.
- F7 (а): строка «слова целиком» с `known_red` → RC2-1.
- F8 (а), F9 (а).
- F10: указатель принят, слой показывает оба вида.
- К проверке критиком: §3 называет 24 формы; `handoffs/*.yaml` на origin/main — 26 файлов (счёт Lead, `ls`).

Решения Lead по находкам t-401 — план §10 (`docs/tasks/specs/20261113-plan-fabrika-ne-huzhe-agenta.md:207-230`); F9 (а) отменено
решением №5; применение — раздел ниже.

## Фикс-раунд t-401 (13.11.2026)

| № | Что изменилось и где / почему нет |
|---|---|
| 1 | §1.1 AR-21, §3.1, §3.4 метод: множество форм = `index()["handoffs"]` ∪ `{index()["escalation"]["contract"]}` (23 + 1; `index.yaml:39-71,102-108`); N1 п. 4: сверка в обе стороны с листингом `handoffs/*.yaml` без литерала, «вариантов ≥ 96» заменено правилом от словаря; E19 — форма `role-to-conductor` без `header` |
| 2 | §3.2 строка «заполняет код», E11, §4.1 (`_code_fills`), N1 п. 1, 3: N1 гоняет `check(fix=False, use_judge=False)`, пустое поле кода не судится (мягкий край `handoff_check.py:2880-2901`); круг дериверов — N3 п. 3 после `fill_artifact` (решение §10 №1/№2); строка `unjudged` закрывает потерю |
| 3 | новый §3.6 (интерфейс ОДИН раз), новый узел N0 первым, C6 в §1.2 и N3 п. 7 через `known_red.reconcile`; форма строки `{node, raised_by, note?}`, рост — построчный `raised_by`, позеленевшая — отказ, неизвестный id — отказ; §9 R8 для П1-б |
| 4 | §3.5: `overrides {поле: значение | ABSENT}`, `ByCode`/`NotCovered`, `classify`, `stage_outputs`, `write_outputs`; новый §3.7 — перечень выходов `stages.json` с путями:строками и писателями из `artifact-writers.json`; узлы N2a–N2d по группам стадий, строка теста на вид; E20–E24 (решение §10 №4 (а)) |
| 5 | C7 в §1.2 и §2 — строка `HandReaderInput` в `tools/lint_ratchet.py`, узел N4 (шаблоны — раздел `hand_inputs` реестра N3); прежний N2 п. 8 удалён; F9 помечена (б) (решение §10 №5). Решение исполнимо по коду: источник подмешивается к нефатальным находкам до `counts` (`lint_ratchet.py:190-192`), identity без строки уже такова (`:17-18`) |
| 6 | §3.4 RR-row-fields, §4.2 (строка `agree: obligation_refs` убрана с причиной), §4.3 FV1-19 «дефект 2 — П1-б», N3 п. 6 (решение §10 №6) |
| 3/8 (межспек.) | §3.6: точное равенство id, строка уровня вида не прикрывает вариант — неудобный вход в таблице N0 |
| 17 | §5 строка `очередь:` для `test-layers.json` (PC4-15, FG7-15, FG7-19 → П1-а N0…N3 → П1-б N3 → П1-в N4); §7 строки `forge/7` и П1-б/П1-в; прежний узел N3 (документы) снят, требования — §9 |
| 18 | не адресована П1-а (заглушка `session_id`, `run_counters` — П1-б/П1-в); П1-а ничего не меняет |
| 19 | §6 (c), §9 R5, R6: вопрос критика и поле находки создаёт узел Lead; до посадки детектор назван пожеланием явно |
| 20 | §3.4 RR-plan-row += `validate_artifacts.check_plan` (`:791,806-808`), `factory_dashboard.plan_levels` (`:710-716`); §4.2 новые строки; §4.3 FV1-14 негатив снят; поиск `report_facts` — новой формой с контролем |
| 21 | §4.2 строка `accept: …stage_acceptance…`: смысл записан — секция во вторичном `s7-analyst-to-scribe.yaml:53-57`, читатель получает форму диспатча; направление починки FV1-22 — узла FV1-22 |
| 22 | §3.5 «ПРИОРИТЕТ»: выпуск — дословно подсказка, цитата — `ctx.minted` базой плюс вариант `cite_hint`; N2b, N3 п. 4; §8.2 |
| 23 | §1.1 AR-20, §9 R7: строки оси 18, вопроса 9 и AR-20 Carriers сажаются тем же коммитом/слиянием, что N0 и N4 (пишет узел Lead) |
| 37 | §2 «Бюджет», N1 и N3 DoD: замер времени — обязательная строка отчёта; превышение 10 с — число, решает Lead, молча не срезается |
| E (ключ критика) | N3 п. 1: `literal_shape` заменён разделом `hand_inputs` с начальными шаблонами (что считать рукописным входом — определено); C4 для FV1-19 — снят (№6) |
| 24–36 | не адресованы П1-а (П1-б, П1-в, пересечения других спек); №36 («FG7-15/FG7-19 не названы») для П1-а закрыт строкой §7 |

Новые развилки этого раунда: F11 (тест помощника против `docs/TESTING.md:55`) и F12 (кто пишет вопрос 9 `critic-diff-brief.md`) —
§8. Решения Lead не пересматривались; неисполнимых по коду не найдено.

## След чтения

Прочитано (первый раунд): план Lead (весь); разведка t-356 (весь); `handoffs/index.yaml` (весь), `s3-strategist-to-designer.yaml` (весь),
`s4-designer-to-case-critic.yaml` (весь), `s7-analyst-to-automator.yaml` (весь); `scripts/handoff.py:380-700` и определения
`:30-36,168,316-331`; `scripts/handoff_check.py:399-448,560-610` и список функций; `scripts/contract.py:2085-2110,2758-2770,3045-3056,3600-3630`;
`scripts/s5_precheck.py:70-110,3740-3834`; `scripts/window_record.py:155-304`; `scripts/stage_done.py:925-1049`;
`scripts/profile_contract.py:340-377`; `scripts/onboarding_probe.py:195-224,330-399`; `scripts/launch_check.py:640-750`;
`design/architecture.md:1-60,106-294`; `references/artifact-contract.md:30-109`; `references/artifact-contract-plan.md:20-79`;
`references/slices/qa-test-strategist/handoff-keys.md` (весь); `references/slices/qa-automator/artifact-contract-automation.md:1-80`;
`references/test-path-markers.json`, `case-markers.json`, `profile-shape.json` (целиком); `references/detectors.json:80-110`;
`handoffs/vocabulary.yaml:23-30`; `scripts/tests/test_stage_joints.py:1-80`; `scripts/tests/test_field_producers.py:1-120`;
`scripts/tests/test-layers.json:1-60,1660-1690,5225-5270`; `scripts/selftest.py` (Grep `unlisted|def test_layers`);
`docs/TESTING.md` (весь); `td-15-scenarios-quarantine.md:700-724`; `docs/SIBLING_MAP.md` (заголовки осей, оси 18, 23-28, 32-34);
находки FV1-1, FV1-12, FV1-18, FV1-19, FV1-22 (целиком), `batch-1-live-run-fvf.md` (весь); ревью t-152 (Grep F4);
`plans/piles/package-ci/batch-4-…md`, `plans/piles/roles-context/batch-2-…md` (целиком).

Прочитано в фикс-раунде (RM = read-main): вердикт t-401 (весь); план §10 (`:207-241`); спека П1-б `:140-179`, `:286-325` и Grep
`known_red|П1-а|fill_artifact|overrides|ABSENT|live_only|form_filler`; `references/stages.json` (весь, 364 строки);
`references/artifact-writers.json` (весь, 350 строк); `references/artifact-registry.json` (весь); `scripts/artifact_registry.py` (весь);
`handoffs/index.yaml` (весь, повторно: `handoffs` 23 строки `:40-71`, `escalation` `:102-108`); `handoffs/role-to-conductor.yaml`
(Grep верхних ключей); `handoffs/s7-analyst-to-scribe.yaml:48-57`; `scripts/handoff_help.py:60-119`; `scripts/handoff_check.py:2868-2905`
и Grep определений (`check` `:1446`, `_code_fills` `:2725`, `Artifacts` `:73`, `_plan_row_of` `:429`, `LIST_DERIVERS` `:564`,
`DERIVERS` `:569`, `BY_LEAF` `:605`); `scripts/handoff.py` Grep (`index` `:320`, `contract_of` `:354`, `spec` `:644`, `escalation`
`:454`); `scripts/driver_runner.py:1025-1059`; `scripts/validate_artifacts.py:795-812`, `:2625-2706` и список функций;
`scripts/factory_dashboard.py:700-717`; `references/artifact-contract.md:1-70`; `references/artifact-contract-run.md:1-30`;
`references/artifact-contract-results.md:1-30`; `references/artifact-contract-first-look.md:1-20`; Grep `^#+ ` и `Writer` по
`references/artifact-contract*.md`; `design/architecture.md:208-239`; `scripts/tests/test-layers.json:1-60,1655-1684`;
`scripts/selftest.py` Grep `fixture_owners` (`:577-600,643-658,711-726`); `scripts/tests/test_selftest_slow_tests.py:474-491`;
`docs/TESTING.md:40-129`; `tools/lint_ratchet.py` (весь); Glob `tools/test_lint_ratchet*.py` (есть).

Поиски (с положительным контролем той же формы): `PLAN_ROW_RE|TS-\\d|TS-\(|\(TS-` по `scripts/*.py` (контроль — `contract.py:3052`;
промах на литерале `"TS-"` признан, вердикт №20); `stage_acceptance` по `handoffs/` (17 строк в 6 файлах); `<[^>]*\b[A-Z]{1,4}-n\b`
по `handoffs/` (32 строки); `^\s*(- )?[A-Za-z_]+:\s*"?<` по `handoffs/` (880/25 файлов); `role-to-conductor` по `scripts/*.py`
(2 вхождения: `handoff_help.py:96`, `test_null_outcomes.py:366`); `artifact-writers\.json` по `scripts/` (контроль — сам
`driver_runner.py:1036` в выдаче); Glob `references/artifact-contract*.md` — первый вызов с относительным шаблоном дал пусто
(промах вызова), повтор с шаблоном `**/` нашёл 25 файлов; Grep `^#+ ` по ним — основание строк «заголовка в контрактах нет» §3.7
(контроль — заголовки прочих выходов в той же выдаче).

Не прочитано (вне манифеста или не понадобилось): `acceptance.py:1331-1365,1559-1590` (по вердикту t-401); `controller.py:7247-7302`
(по вердикту t-401); `manifest_from_tests.py` (по разведке t-356); `references/artifact-contract.md:172-206` (форма проектных файлов —
N2d читает); `references/artifact-contract-plan.md:60-110` в этом раунде (строки `:68-69`, `:99`, `:104` — по первому раунду и Grep);
`scripts/s5_plan.py` (N2c читает скелет); `tools/test_lint_ratchet.py` (содержимое; файл есть); `plans/piles/forge/batch-7-*.md`
(строки FG7-15/19 — по вердикту t-401); `plans/builder-rules.md` п. 7b читан по пересказу CLAUDE.md правило 4.
