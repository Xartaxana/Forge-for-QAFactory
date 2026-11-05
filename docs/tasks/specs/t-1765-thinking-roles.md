# t-1765 — роли думают: страж в фордже (часть A) и план фабрики для экспериментальной ветки (часть B)

Черновик дизайнера (Opus), 03.11.2026, по брифу Lead (Fable). Развилки возвращены (§5), не решены. Решения, принятые дизайнером без
веса замысла, — §8. След чтения — §9. Проза по-русски, идентификаторы и пути по-английски. Числа взяты из носителей, названных в
скобках; лексические счёты скаутов — порядок величины, не замер (как в анализе §1).
Фикс-раунд t-1775 (03.11.2026, свежий дизайнер, по вердикту критика на план t-1774): F-1…F-9 решены владельцем и не перерешаются; что
изменено по каждой находке B-n / F-n / Q-n — §10; новые развилки раунда — F-10, F-11 в §5 (текст написан по рекомендации).

## 1. Цель и затронутые инварианты

**Слово владельца (03.11.2026, дословно):** «Мне надо чтобы роли сами могли думать, а не только следовать инструкциям. Скрипты должны
просто облегчать им работу (например собирать правильный yaml файл), а правила должны являться неким опытом, который тестовая фабрика
переняла у тестировщиков (где лучше искать баги, какие техники тест-дизайна есть, как лучше писать e2e тесты). В результате я хочу,
чтобы роль не теряла гибкость, умение подстраиваться и думать, но получила направление, в котором можно быстрее прийти к правильному
результату (найти все несоответствия, вопросы и баги).» И: «Именно так и было задумано, но выродилось в то, что есть.»

**Принцип (формулировка Lead, сохраняется дословно по смыслу):**
- **код владеет ДАННЫМИ** — читает тикет, дифф, вложения, стенд; собирает YAML; несёт слова человека; проверяет ключи и перекрёстные ссылки;
- **роль владеет СУЖДЕНИЕМ и ИСХОДОМ** — что тестировать, баг ли это, хорош ли кейс; принимает тир выше по смыслу, со свидетелем, как в SD;
- **человек владеет ЗАМЫСЛОМ** — гейты остаются там, где решить может только человек.
Универсальность (P2) сохраняется: роль получает знание, а не правило одного проекта.

**Что спека должна закрыть** (диагноз — анализ `docs/tasks/specs/reports/20261103-pochemu-roli-ne-dumayut.md` §2, §3):
1. приёмка по форме, а не по смыслу → часть B (в): приёмка по смыслу тиром выше, `exit_gate` до «есть и в форме»;
2. роль не владеет исходом → часть B (а), (б): хартия с исходом и DoD, диспатч в форме SD;
3. знание заменено словарём → часть B (а) хартии с ремеслом; развилка F-3 о закрытых словарях;
4. у вопроса нет дороги наверх → часть B (г);
5. нагрузка и трение → часть A (3) храповик нагрузки и доли ремесла; часть B бюджет хартии.
И почему всё это выродилось → часть A целиком.

**AR-n, которые спека трогает** (по протоколу «How a change walks this map», `design/architecture.md:254-265`):

| AR | как трогает | проверка изменения, которую несёт DoD |
|---|---|---|
| AR-2 открытое разнообразие — суждение роли | часть A делает его детектируемым; часть B снимает с кода решения о смысле | для каждого снятого с кода решения назвать, что теперь решает роль и кто это принимает (§3, столбец REWORK) |
| AR-7 код — инструмент роли | AR-29 — его счётная сторона; детектор `none — discipline` получает код (узел A2 правит поле Detector у AR-2 и AR-7) | `stage_compare.py <stage>` до и после на CART-1 (протокол §3.6); расход стадии до/после |
| AR-9 отказ называет дверь | часть B переводит часть отказов в WARN/советы; у оставшихся дверь остаётся; у гейта `judgment:` дверь — форма `none`/`adds data check`/`moves … to code` (§2.4) | `refusal_registry.py --check` (A24) зелёный; удалённый отказ уходит из реестра тем же коммитом |
| AR-10 требование проверки — роли до работы | хартия и бриф SD — новые носители требований | DoD роли стоит в брифе в полях, которые судит приёмщик |
| AR-11 нагрузка роли | бюджет хартии, новые ключи `role-load.json` | `role_load.py --all` до и после; `selftest.py --limits` |
| AR-12 трение | эксперимент меряет трение `friction.py`; гейт называет обе проблемы коммита одним отказом (§2.4, E-A12) | `code_friction` до/после по ролям S1–S4 (и S5–S8 во второй фазе) |
| AR-13 факт с функцией-читателем читается только через неё | приёмка стадии — через `scripts/acceptance.py` (X2-5); число раундов ремонта — только `repair_budget` контроллера (X2-7, §3.5) | второго счётчика раундов и второго читателя записи приёмки нет: `git grep -n "def .*repair_budget\|def .*stage_acceptance" -- ai-packages/qa-factory/scripts` в свидетеле узла |
| AR-18 одна форма выхода детектора | советы стадии — записи `detector_verdict` с признаком совета, не сигнал человеку (X2-2, B-3); перепись читает места отказа через `refusal_registry.sites()`, третьего AST-сканера отказов нет | `test_stage_joints.py` зелёный; второй парсер вывода — находка критика |
| AR-20 храповики только сжимаются | два новых храповика (счёт классов, нагрузка «процесса») | новые храповики входят в ось 18 и в вопрос 9 брифа критика тем же коммитом |
| AR-21, AR-22 передача целиком; у поля есть производитель и читатель | открытие словарей, удаление проверок `c` и полей формы дайджеста; файл советов стадии получает читателя — бриф критика стадии (X2-2) | обход producer→reader и reader→producer с положительным контролем на каждое удаляемое поле (`test_field_producers.py`) |
| AR-24 слова человека доходят целиком | KEEP: `person_words.py`, `waiver.py`, `human_word_check` | `test_words_doors.py` зелёный на ветке |
| AR-26 требования — единица | хартии говорят «требование», не «AC» | перегон переписи `t-928` на тронутых файлах |
| AR-28 неизвестное не становится проходом | приёмка смысла уходит к критику; гейт по-прежнему не пропускает отсутствие; нечитаемая перепись — отказ, не проход (E-A11) | спека называет поведение каждого гейта на пустом/отсутствующем входе (§6); `gate_registry.py --check` (A26) |
| **AR-29 (новый)** | вводится частью A | §2.2 |

**Владелец, которому служит каждая проверка, которую спека добавляет или меняет** (правило 1 дизайнера, AR-29): перепись и её тест —
данные (код; судит форму и счёт, не смысл); гейт `judgment:` — данные (форма строки и рост потолков); советы стадии — суждение (их читает
критик стадии, тир выше); запись приёмки стадии — данные (присутствие, класс `shape`); вердикт приёмщика — суждение; гейты A/B — замысел.

## 2. Часть A — страж в фордже: чтобы принцип не вырождался при мелких изменениях

### 2.0 Почему выродилось

Анализ §1, последний абзац, и §2, «второе следствие»: восемь потерь при передаче (сентябрь — 02.11) лечились одним способом — шаг
забирали у роли и отдавали коду. Для данных это было верно (P5, S0 по коду — это и дало снижение в 5 раз). Тот же рефлекс применили к
шагам суждения (`branch_accounting`, `sizing`, `planning_contract`, `s5_precheck`, закрытие обязательств по закрытому списку), и там код
дал не мысль, а согласие с формой. Принципы, которые говорят обратное (P1, P3, P22, FR-47, AR-2, AR-7), есть, но **на пути исполнения у них
нет кода и нет детектора, который считает, где живёт суждение**: у AR-2 и AR-7 в поле «Detector» записано `none — discipline`
(`design/architecture.md:56`, `:93`). 244 скрипта стоят на пути исполнения, принципы — нет; поэтому каждое мелкое изменение сдвигает
равновесие в одну сторону. Механизм ниже ставит на путь исполнения пять вещей: принцип (P27), инвариант с детектором (AR-29), счётный
тест с храповиком, строку коммита с гейтом и вопрос критика; калибровка читает их раз в неделю.

### 2.1 (1) Принцип P27 для `PROJECT.md`

Вставка после P26, тем же форматом (жирный номер, текст, «Владелец, дата»):

> **P27.** Код владеет данными, роль — суждением и исходом, человек — замыслом. Слово владельца 03.11.2026: «Мне надо чтобы роли сами
> могли думать, а не только следовать инструкциям. Скрипты должны просто облегчать им работу (например собирать правильный yaml файл), а
> правила должны являться неким опытом, который тестовая фабрика переняла у тестировщиков (где лучше искать баги, какие техники
> тест-дизайна есть, как лучше писать e2e тесты)… роль не теряла гибкость, умение подстраиваться и думать, но получила направление, в котором
> можно быстрее прийти к правильному результату (найти все несоответствия, вопросы и баги).» Значит: код читает тикет, дифф, вложения и стенд,
> собирает YAML, несёт слова человека, проверяет ключи и перекрёстные ссылки — и НЕ решает, закрыто ли обязательство, годится ли кейс, баг ли
> красный; это решает роль, и её исход принимает по смыслу тир выше со свидетелем; человек решает на гейтах то, что знает только он. Правило
> роли — опыт тестировщика (где искать баги, техники, как писать стабильный e2e), а не процедура формы. Потерю при передаче лечат кодом только
> тогда, когда потеряны ДАННЫЕ; потерянное суждение лечат хартией, приёмкой и вопросом наверх. Владелец, 03.11.2026 (AR-29; детектор —
> калибровочная проверка 41).

Плюс строка в таблице принципов-правил вводного абзаца раздела («Они же стоят правилами FR-47…FR-57…») не меняется: P27 не новое FR, а
принцип над FR-47/AR-7 (решение дизайнера, §8 S-1).

### 2.2 (2) Инвариант AR-29 для `design/architecture.md`

Раздел B («Low friction with our code»), после AR-12; строка таблицы разделов `| B. … | AR-7 … AR-12 |` получает AR-29; индекс
перегенерируется `python tools/architecture_index.py`. Тем же узлом (A2) поле «Detector» у AR-2 (`:56`) и AR-7 (`:93`) меняется с
`none — discipline` на ссылку `the census (AR-29): test_judgment_census.py; calibration check 41` — иначе §1 «детектор получает код» остаётся
словом без носителя (критик t-1774 F-7).

```
**AR-29 — A code check judges data: shape, joins, presence; a role's judgment is judged by a tier above.**
- Invariant: a check in code judges the SHAPE of an artifact (keys, types, a form), its JOINS (every R-n reached, every Then bound,
  counts equal) or the PRESENCE of an input, a witness or a person's word. A check that classifies a role's judgment (is this a bug,
  is this case good, does this text support the requirement), closes a role's obligation by a closed-list reason, or refuses a role's
  output on its content is a breach. Such a judgment belongs to the role and is accepted on meaning by a tier above (a stage critic or
  the driver) with a witness; code may compute ADVICE for that acceptor and never a refusal. Protection of the application, secrets,
  external writes and the person's words is not judgment and stays a refusal (class `safety`).
- Carriers: P1, P3, P22, P27; FR-12, FR-13, FR-47; AR-2, AR-7; `scripts/tests/fixtures/judgment-census.json` with
  `scripts/tests/test_judgment_census.py`; `scripts/refusal_registry.py` (`sites()`, the one scanner of refusal sites);
  `references/role-load.json` (`process_ratchet_tokens`); `references/stages.json` (`advice`);
  `dev:tools/architecture_gate.py` (the `judgment:` line); `dev:docs/tasks/critic-diff-brief.md` question 11; axis 32 of
  `dev:docs/SIBLING_MAP.md`.
- Detector: `test_judgment_census.py` (every check unit of every `scripts/*.py` outside `scripts/tests/` has a census row with a class;
  whether a unit blocks is computed - refusal sites through `refusal_registry.sites()` and the declared blocking path - never hand-labelled;
  the counts of `word-list`, `meaning-proxy`, `meaning` and `safety` units, of blocking units per role, of `blocks_override` exceptions
  and of breaches only shrink); `role_load.py --all` against `process_ratchet_tokens`; the commit-msg `judgment:` gate; calibration
  check 41. Gap: the class of a unit is a human label; a unit labelled `shape` that reads meaning is caught only by the critic's
  question 11.
- Breakage: LOCAL-1 (0.10.8, 02.11.2026). The automator knew 8.5 hours before S7 that the price was asserted in a field `GET /api/cart`
  does not return, and still recorded 11 reds as `contradicts_requirement`: the gate needed closed obligations, and "the field does not
  exist, the case is defective" was not a move the form accepted (`dev:docs/tasks/specs/reviews/t-1672-local-1-whole-run.md:15-17`).
- Change check: for every check the change adds or alters, name its class (shape / xref / word-list / meaning-proxy / meaning / safety)
  and the owner it serves (data / judgment / intent). A new refusal on a role's content is not added: it becomes advice for the
  acceptor. Run `test_judgment_census.py`; a raised count is named in the verdict (AR-20).
```

Ограничение протокола карты (`design/architecture.md:265`): индекс ≤ 3 КБ, и после 30 записей новый инвариант сливается с ближайшим.
AR-29 — 29-я запись, слияние не требуется; индекс сегодня 2550 Б (замер критика t-1774 §1 (a'')), строка AR-29 ≈ 105 Б — край E-A1 (§6)
не ожидается, но проверяется ключом K2.

### 2.3 (3) Детерминированный детектор: перепись проверочных единиц и храповики

**Что сканируется (переписано по критику t-1774 B-1, F-12).** ВСЕ файлы `ai-packages/qa-factory/scripts/*.py`, кроме каталога
`scripts/tests/`. Набор файлов — НЕ данные переписи: ключа `scan_globs` нет; корень и исключение — константы теста
(`SCAN_ROOT = "scripts"`, `SCAN_EXCLUDE = ("tests",)`). Сузить скан можно только правкой самого теста — её видит дифф, вопрос 11 и проверка
41 (a); правка данных переписи сузить скан не может (прежняя лазейка «сузил образец → счёты упали → C3 требует опустить потолок → коммит
выглядит как улучшение» закрыта). Прежний образец имён файлов (30 у t-1761, 33 у этой спеки — замер критика) терял судей с нейтральным именем
файла: `judge_form.py` (`digest_errors`), `judge.py` (`judged_refusal`), `readiness.py` (15 функций `check_*`), `story_run.py`,
`manual_evidence.py`, `stage_done.py`, `no_move.py` и др. (критик: 336 вхождений функций проверочной формы в 104 файлах). Число сканируемых
файлов на первой переписи — в свидетеле узла A3.

**Что такое проверочная единица (unit).** Функция или метод (AST `FunctionDef`/`AsyncFunctionDef`) в сканируемом файле, если выполнено хотя
бы одно из:
- (u1) имя по константе теста `UNIT_NAME_RE = ^(check_|rule_|judge|judged_)|(_check|_errors)$` — ловит эталоны самой таблицы классов:
  `exit_gate.judge_words`, `judge.judged_refusal`, `judge_form.digest_errors`, `readiness.check_*`;
- (u2) тело вызывает LLM-судью фабрики: вызов атрибута модуля `judge` (`ask`, `ask_one`, `ask_many`, `judged_refusal`) или `judge_form`
  (`digest`, `digest_errors`, `unresolved_reason`, `normalise_unresolved`) — константа теста `JUDGE_CALLS`; так видна функция с
  нейтральным именем, которая отдаёт вердикт модели (семья `judge*.py` — 13 файлов; `import judge` или имя `judge.py` встречаются в 21 файле
  пакета вне `tests/` по grep);
- (u3) в теле есть место отказа, которое видит `refusal_registry.sites()` (вызов `deny`/`block`, `raise StateConflict|ValueError`), — тот же
  сканер, что держит реестр A24, третий AST-обход мест отказа не заводится (критик §6 «ДУБЛИРОВАНИЕ»).
Плюс каждая запись реестра A24 (`refusal_registry.REGISTRY`) и каждая строка `detectors`/`advice` в `references/stages.json` — по правилу
двойного счёта ниже.

**Явные строки классов для файлов, названных критиком** (первая перепись ставит их так; узел A3 читает тело и при несогласии ставит класс
выше по порядку E-A2, не ниже):
- `exit_gate.judge_words` — `word-list` (LLM-судья, сводящий слова к закрытому списку — таблица классов);
- `judge_form.digest_errors`, `judge_form.unresolved_reason`, `judge_form.normalise_unresolved` — `word-list` (шапка `judge_form.py`:
  «Refusals of FORM: a word outside a closed list…»);
- `judge.judged_refusal` — класс по развилке F-10 (рекомендация: `meaning`, если A3 найдёт его на пути отказа, иначе `meaning` с
  вычисленным `blocks: false`); остальные публичные функции `judge.py` попадают в перепись только через u1–u3;
- `readiness.check_*` — `shape` (присутствие исполняемого файла, адаптера, среды, профиля), кроме `check_tracker_write`,
  `check_external_writes` — `safety` (внешние записи, P8); по имени — A3 читает тела.

**Классы (поле `class`, закрытый список — данные переписи):**

| class | что судит | пример (носитель) |
|---|---|---|
| `shape` | ключи, типы, форма, присутствие | `validate_artifacts.check_pipeline`, `exit_gate.required_outputs_errors` |
| `xref` | перекрёстные ссылки, равенство счётов, связки | `s5_precheck.check_bindings`, `branch_accounting` (каждая единица текста имеет дом) |
| `word-list` | слова роли или человека по списку, закрытый список причин закрытия | `stage_guard.rule_manifest` (`closed_unresolved_reasons`), `exit_gate.judge_words`, `judge_form.digest_errors` |
| `meaning-proxy` | качество по шаблону (AST, регэксп по смыслу) | `s5_precheck.check_smells`, `validate_artifacts.check_test_code` |
| `meaning` | хорош ли кейс, баг ли красный | t-1761 §1 насчитал 0; кандидат — `judge.judged_refusal` (F-10) |
| `safety` | защита приложения, секретов, внешних записей, слов человека, git-состояния | `guard_app_under_test`, `guard_secrets`, `guard_pre_tool.human_word_check` |

**Поля строки:** `file`, `function`, `class`, `roles` (на чьём пути стоит: имена ролей или `conductor`), `owner` (`data | judgment | intent` —
кому служит), `ref` (id в A24 / A26 / `stage-joints.json` / строка `stages.json`, если единица там уже зарегистрирована — описание не
повторяется, развилка F-7), `blocks_override` (необязательно; только значение `false`, только вместе с `note`), `note` (одна строка;
обязательна при `blocks_override`).

**`blocks` вычисляется, не размечается (B-1 п. 4; развилка F-11, текст — по рекомендации (b)).** `blocks = true`, если:
- (b1) `refusal_registry.sites(files=<все сканируемые файлы>)` возвращает место отказа с `function` этой единицы; для этого `sites()` получает
  необязательный аргумент `files` (по умолчанию — нынешний `SCANNED`, поведение реестра A24 не меняется; §8 S-7); или
- (b2) файл единицы стоит на объявленном пути отказа: скрипт в `stages.json` `detectors` (после X2-2 — за вычетом `advice` той же стадии и
  роли), либо в константе теста `BLOCKING_ENTRY_FILES` = (`exit_gate.py`, `stage_guard.py`, `guard_pre_tool.py`, `inject_context.py`,
  `stage_done.py`, `validate_artifacts.py`, `s5_precheck.py`, `handoff_check.py`, `judge_form.py`) — это файлы, чьи проверки возвращают список
  ошибок, который вызывающий превращает в отказ, а `sites()` таких отказов не видит; кортеж только растёт (A3 при первой переписи вправе
  убрать файл, которого не нашёл на пути отказа, с `note` в свидетеле; дальше — только добавление);
- иначе `false`.
Ручная метка — только исключение `blocks_override: false` с `note` (например, `raise ValueError` в чистом разборщике, который ловит
вызывающий). Число исключений — потолок `blocks_overrides` в `ratchet` (только вниз); каждое новое исключение читает вопрос 11.
**Нарушение (breach)** вычисляется: вычисленный `blocks == true` (без исключения) и `class ∈ {word-list, meaning-proxy, meaning}`.

**`refusal_registry.sites()` в новой, более ответственной роли (реестр → вход храповика; правило 1 дизайнера).** Направление допустимой ошибки
— в сторону ЛИШНЕГО `blocks: true` (лишний breach виден и снимается исключением с `note`, которое читает критик); недосчёт отказа —
недопустимая ошибка, её закрывает (b2). Неудобные входы, которые обязаны остаться на безопасной стороне (каждый — случай C5):
`raise ValueError` в разборщике (→ `true`, исключение с `note` законно); отказ через обёртку `_deny(...)` или импорт с другим именем
`from hooklib import deny as refuse` (`sites()` не видит — файл обязан быть в (b2), иначе C5 краснеет на синтетическом модуле, не входящем в
путь: тест печатает «отказ через обёртку не виден: добавьте файл в BLOCKING_ENTRY_FILES»); отказ во вложенной функции (`sites()` относит его к
ВНЕШНЕЙ функции — `owner.setdefault` при обходе сверху, `refusal_registry.py:823-827`; единица — внешняя функция); отказ на уровне модуля
(`function: "<module>"` — строка переписи с `function: "<module>"`).

**Правило двойного счёта (критик F-11).** Строка `stages.json` `detectors`/`advice` — единица переписи только для скрипта, у которого нет
функций-единиц; иначе функции-единицы этого скрипта несут `ref: "stages.json:<S>/<role>"`, а строки скрипта нет. Запись A24 с `file`/`function`,
совпадающими с функцией-единицей, — тот же `ref`, не вторая единица. Счёт — по различным парам (`file`, `function`).

**Тест `scripts/tests/test_judgment_census.py` (новый) — что он доказывает:**
- C1 каждая единица сканируемых файлов имеет строку переписи; лишняя строка (функции нет) — отказ «устаревшая строка: удалите или
  перенесите», никогда не тихое сжатие (как A26 F-c и ось 18);
- C2 у каждой строки класс из закрытого списка, `roles` непуст, `owner` из трёх; `blocks_override` — только `false` и только с `note`;
- C3 храповик: `ratchet` в переписи держит потолки `word-list`, `meaning-proxy`, `meaning`, `safety` (принятая F-8 (b)), `breach`,
  `blocks_overrides` и `blocking_per_role.<role>`; счёт выше потолка — красный с именем строк, счёт ниже потолка на величину > 0 — красный
  «опустите потолок до N» (храповик только сжимается и всегда плотный, как `role-load.json` A22-K8). `blocking_per_role` плотный (критик F-10):
  ключ есть у каждой роли из имён файлов `agents/*.md` и у `conductor`; роль без блокирующих единиц — строка `0`, не отсутствие ключа;
  отсутствующий ключ — красный «добавьте строку `<role>: 0`»; ключ роли, которой нет в `agents/`, — красный «устаревшая строка» (переименование
  F-2 (b) — это переименование ключа тем же коммитом, что и файла роли);
- C4 потолок `meaning` — константа теста `MEANING_CEILING`, не данные: правка данных не может её поднять (как `ANCHOR_FLOOR` у A26); значение —
  по развилке F-10 (рекомендация: счёт `meaning` первой переписи, 0 если A3 не нашёл ни одной; дальше константа только опускается, X7-1 доводит
  до 0). **Слепое пятно (критик Q-1), печатается тестом рядом со строкой итогов:** класс `meaning` — ручная метка; единица, которая судит смысл,
  но помечена `word-list` или `shape`, C4 не видна — её ловят вопрос 11 и выборка проверки 41 (d); C4 — гарантия против честного подъёма, не
  против переразметки;
- C5 отрицательные контроли внутри теста (синтетические модули во временном каталоге, `sites(plugin_root=<tmp>, files=…)`):
  `def check_x` без строки переписи → C1; синтетический `def judge_x`, вызывающий `deny(...)`, в файле с нейтральным именем `helpers_x.py`
  → C1 (единица без строки) и вычисленный `blocks: true`; функция с нейтральным именем, вызывающая `judge.ask_one` → C1 (u2); отказ через
  обёртку `_deny` в файле вне `BLOCKING_ENTRY_FILES` → красный «не виден»; строка с классом `opinion` → C2; `blocks_override: false` без
  `note` → C2; поднятый `word-list` и поднятый `safety` → C3; роль без ключа в `blocking_per_role` → C3;
- C6 тест печатает строку итогов: число сканируемых файлов, счёты по классам, `breach`, `blocks_overrides`, `blocking_per_role` (вход
  проверки 41 (a)); `SCAN_ROOT`/`SCAN_EXCLUDE` печатаются в ней же — сужение скана видно в каждом выводе.
Слепое пятно (печатается, как у A26): единица с проверочным смыслом под нейтральным именем, без вызова судьи и без места отказа (`def _ok(...)`,
возвращающая `bool`, по которой вызывающий решает), не видна; её ловит вопрос 11 критика. Направление ошибки переписи: в сторону ЛИШНЕЙ
строки (функция с «проверочным» именем, которая ничего не судит, получает строку `shape` и вычисленный `blocks`) и лишнего `blocks: true` —
это безопасно; недосчёт — слепые пятна выше.

**Храповик нагрузки роли (`references/role-load.json` уже есть, `scripts/role_load.py` его читает).** Сегодня в нём `ratchet_tokens` на роль
(общая нагрузка, только вниз, `ratchet_slack_tokens: 1000`) и непотверждённый `threshold_tokens: 25000`. Изменение:
- разметка «ремесла»: секция исходного текста (хартия роли, `references/*.md`, срезы) с маркером `<!-- kind: craft -->` над заголовком —
  тем же способом, каким уже ставятся `<!-- roles: … -->` (`inject-map.json`, ключ `slices`); неразмеченное считается процессом;
- `role_load.py --all --json` печатает на роль `craft_tokens` и `process_tokens` (сумма = нынешнее число);
- `role-load.json` получает `process_ratchet_tokens` на роль (только вниз, slack 0 — процесс не растёт ни на токен без названного подъёма)
  и `target_tokens` (развилка F-1); `ratchet_tokens` остаётся как был;
- аудит A22 (`selftest.py --limits`) краснеет, если `process_tokens` роли выше её строки или строка не плотная.
Цена: один маркер на секцию; рост ремесла не трогает храповик процесса, но держится общим `ratchet_tokens` и целью F-1.

### 2.4 (4) Строка коммита `judgment:` и её гейт

Каждый коммит, который трогает `ai-packages/qa-factory/`, несёт хотя бы одну собственную строку одной из форм:

```
judgment: none -- <почему изменение не двигает суждение>
judgment: adds data check <unit> -- <почему это проверка данных или защита, а не суждение>
judgment: moves <что> to role -- <почему>
judgment: moves <что> to code -- <почему>
```

Четвёртая форма `adds data check` — по критику t-1774 F-1: рост `blocking_per_role` или `safety` бывает от честной проверки данных (новый
обязательный ключ — `shape`, `blocks: true`); требовать за него `moves … to code` значило бы заставить строку лгать и утопить проверку 41 (c) в
шуме.

Гейт — расширение `tools/architecture_gate.py` вторым видом строки (решение дизайнера §8 S-2, развилка не нужна: одна логика отбора строк —
та, что уже скопирована из `mechanism_gate.py`, второй копии не появляется, вопрос 6 брифа критика). `_prose_matches(msg)` параметризуется
регэкспом — `_prose_matches(msg, line_re=LINE_RE)`, рядом `JUDGMENT_RE = ^[ \t]*judgment[ \t]*:(.*)$` (те же флаги, что `LINE_RE`), —
функция не копируется (критик F-9).

**Форма строки:**
- нет пакетного пути в индексе — молчит (как сейчас);
- пакетный путь есть, строки `judgment:` нет — отказ, называющий четыре формы и дверь `judgment: none -- <reason>`;
- `moves` без `to role|to code`, `adds data check` без `<unit>`, или любая форма без текста после `--` — отказ с образцом;
- строка внутри ограждённого блока или цитаты не считается (как `architecture:`); merge-коммит освобождён (как `architecture:`).

**Перекрёстная проверка переписи (детерминированная).** Путь `P = ai-packages/qa-factory/scripts/tests/fixtures/judgment-census.json`.
`main()` читает ДВА блоба через `gitcmd`: `git show HEAD:<P>` (перепись в HEAD) и `git show :<P>` (перепись в индексе); их тексты (или `None`,
если блоба нет) передаются в `decide()` аргументами — `decide()` остаётся чистой, и тест K4 не требует git (критик §5 п. 2 (г)). Потолки
сравниваются по ключам `ratchet`: новый ключ с числом > 0 — подъём, новый ключ с 0 — не подъём, исчезнувший ключ — не подъём. Миры (каждый —
строка E-A7…E-A11 в §6):
- (i) переписи нет ни в HEAD, ни в индексе (весь `main` до коммита A3 — по F-6 (а) гейт A5 живёт на `main` РАНЬШЕ переписи) — перекрёстная
  проверка молчит; строка `judgment:` по-прежнему требуется по форме;
- (ii) нет в HEAD, есть в индексе (коммит A3 создаёт перепись) — создание не подъём: потолки первой переписи — факт; `judgment: none -- census
  created` проходит; то же, если блоб HEAD есть, но не читается как JSON (тогда — плюс строка WARN «перепись в HEAD не читалась; сравнение с
  пустой»);
- (iii) есть в HEAD, удалена в индексе — удаление стража равно подъёму каждого потолка до неизвестного: `none` и `adds data check`
  отклоняются, проходит только `judgment: moves <что> to code -- <почему>` (дверь всегда открыта, FR-2), отказ называет «перепись удалена этим
  коммитом»;
- (iv) есть в обоих, блобы равны — молчит;
- (v) есть в обоих, различаются: подъём `word-list|meaning-proxy|meaning|breach|blocks_overrides` — `none` и `adds data check` отклоняются, нужна
  `moves <что> to code`; подъём только `blocking_per_role.*` и/или `safety` — `none` отклоняется, проходят `adds data check` или
  `moves … to code`; отказ называет каждый поднятый ключ «<ключ> <старое> → <новое>»;
- блоб в индексе не читается как JSON, в нём нет объекта `ratchet` или потолок не целое ≥ 0 — отказ с путём файла, независимо от
  содержимого строки `judgment:` (AR-28: неизвестное не становится проходом).

**Позиция внутри `decide()` (позиционный край, критик §5 п. 2; E-A12).** Сегодня `decide()` (`tools/architecture_gate.py:130-152`)
возвращается на первом отказе. После A5 порядок такой: (1) нет пакетного пути — `0, ""` до любого чтения (как сейчас); merge-освобождение
остаётся в `main()` до чтения сообщения (`:171-176`) и тоже общее для обеих строк; (2) проблемы `architecture:` (нет индекса, нет строки,
плохая строка) и проблемы `judgment:` (нет строки, плохая форма, нечитаемая перепись, отклонённая форма при подъёме) собираются НЕЗАВИСИМО
в два списка; (3) если хоть один непуст — один отказ, называющий все проблемы обоих видов, с формами обоих видов. Инварианты позиции:
отсутствие `ARCHITECTURE_INDEX.md` не делает `judgment:` непроверенным, а нечитаемая перепись не снимает отказа по `architecture:`
(ни одна проверка не маскирует другую); два круга коммита ради двух проблем не нужны (AR-12); ни один путь не превращает непрочитанное в
проход (AR-28); то, что сегодня отказывается (`architecture:` без индекса, без строки, с неизвестным id), отказывается и после.

Гейт сам судит только форму строки и рост чисел — он не решает, правдива ли `none` (AR-29 к самому стражу); ложную `none` ловят калибровка 41
и вопрос 11.

**Живой путь (критик F-9; правило 2 CLAUDE.md).** `tools/architecture_gate.py` уже вызывается `.githooks/commit-msg` — правка этого файла
и есть правка самоактивирующейся проверки. Билдер A5 сдаёт содержимое соседним файлом `tools/architecture_gate_next.py` с тестом
`tools/test_architecture_gate_next.py` (тест импортирует `architecture_gate_next`); Lead при приёмке переносит его на `tools/architecture_gate.py`,
тест — на `tools/test_architecture_gate.py` (поправив импорт), и гоняет K4 уже на живом имени. До переноса живой гейт не меняется.

### 2.5 (5) Вопрос 11 критика и правило дизайнера

**`docs/tasks/critic-diff-brief.md`**, после вопроса 10:

> 11. **JUDGMENT** (P27, AR-29): does the diff move judgment into code — a check that classifies a role's judgment, closes a role's
>     obligation by a closed-list reason, or refuses a role's output on its content? Does it add text a role must read that is not
>     testing craft (a procedure of keys, scripts and refusals)? Read every census row the diff adds or reclassifies (a class lowered —
>     `word-list` → `shape` — is the cheap way past the ratchet), every `blocks_override: false` it adds (a computed refusal relabelled
>     as non-blocking is the other cheap way), every edit of the census test's scan constants (`SCAN_ROOT`, `SCAN_EXCLUDE`,
>     `BLOCKING_ENTRY_FILES`, `UNIT_NAME_RE`, `JUDGE_CALLS`, `MEANING_CEILING`), and every `<!-- kind: craft -->` marker it adds (a process
>     section marked craft escapes the process ratchet). Each is a finding with a severity; a `judgment: none` or `adds data check` on a diff
>     that does move judgment blocks.

**`.claude/agents/designer.md`, правило 1** — одна фраза в конец абзаца про `ai-packages/qa-factory/`: «…and names, for every check the spec
adds or alters, the owner it serves — data (code), judgment (a role, accepted by a tier above) or intent (the person) — and its census class
(AR-29).» Это правка роли форджа: в `CLAUDE.md` добавляется host adaptation 10 (строка: «designer rule 1 и критик вопрос 11 — P27/AR-29;
детектор — проверка 41»), иначе ось 1 нарушена (правило в CLAUDE.md ↔ файл роли).

### 2.6 (6) Калибровочная проверка 41 (`PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md`)

> 41. **Where judgment lives (P27, AR-29).** Mechanism: the census `scripts/tests/fixtures/judgment-census.json` with
>     `test_judgment_census.py`, the `judgment:` line of `tools/architecture_gate.py`, the critic's question 11, `role-load.json`
>     `process_ratchet_tokens`. Per window:
>     (a) the census totals by class and `breach`, `blocks_overrides` and `blocking_per_role`, against the previous window's, with the command
>     beside the numbers (hygiene 6(b)): `python -B -m pytest ai-packages/qa-factory/scripts/tests/test_judgment_census.py -q` green and the
>     totals line it prints (the scanned-file count included: a fall with no deleted scripts is a narrowed scan); every raise named by a
>     critic verdict, else a finding (axis 18); while the census is not on `main` yet (part A lands forge-first, F-6 (a)), the line says
>     "census not on main" — not a finding, not a zero;
>     (b) every role's start load, `craft_tokens`, `process_tokens` and the craft share (`role_load.py --all --json`), against the
>     previous window's; a process growth with no named raise is a finding; before node A4 lands, the line says "craft split not on main";
>     (c) the `judgment:` lines of package commits (`git log --format=%H%n%B -- ai-packages/qa-factory/`): count `none`, `adds data check`,
>     `moves … to role`, `moves … to code`; the Lead reads every `to code` line, and samples three `none` and three `adds data check` lines
>     against their diffs; a `none` whose diff changed a census row or added a refusal on content is a false `none`;
>     (d) the share of craft in each role's charter — three `kind: craft` sections sampled and read: a procedure marked craft is a finding;
>     and three census rows of class `shape`/`xref` and every `blocks_override` sampled against their function bodies: judgment under a
>     data label is a finding;
>     (e) an empty window gets an explicit line.
>     Detector of this check's own leak: a window with package commits and no line (a)–(c) is itself a finding; the forge metric «findings
>     of the class "role halted on a form" in `plans/piles/*/findings/`» growing while the census counts fall means the census is being
>     relabelled, not the code changed.

Номер: в файле на main последняя проверка — 38 (прочитано; подтверждено критиком t-1774 §0: `527c560f` с проверками 39/40 не предок
`origin/main`); 39 и 40 вносит t-1702 D3 (`docs/tasks/specs/t-1702-d6-forge-ci.md:100,103`). 41 свободен в обоих мирах. Край E-A3 (§6).

### 2.7 (7) Ось SIBLING_MAP

На main 30 осей (`## Axis 30` — последняя, прочитано; положительный контроль того же grep нашёл ось 30; подтверждено критиком t-1774 §0);
ось 31 «Role carriers: one owner per aspect <-> pointers» вносит t-1702 D3 (`t-1702-d6-forge-ci.md:290`). Механизм открывает **новую ось 32**
(или следующую свободную, край E-A3): `## Axis 32 — Where judgment lives: the census <-> the gates that refuse <-> the role charters <-> the
acceptor`. Состав: перепись и её тест; `refusal_registry.sites()` (единственный сканер мест отказа, вход переписи); `exit_gate.py`,
`validate_artifacts.py`, `stage_guard.py`, `guard_pre_tool.py`, `s5_precheck.py`, `handoff_check.py`, `judge.py`, `judge_form.py` (носители
единиц); `agents/*.md` (хартии); `references/stages.json` `advice`; бриф критика вопрос 11. Правило оси: новая проверка в любом файле
`scripts/*.py` получает строку переписи тем же коммитом; перевод проверки в совет меняет `stages.json` `advice` (или `blocks_override` с `note`)
тем же коммитом. Ось 32 ссылается на ось 18 (храповики) и ось 5 (двойники стадий), не дублирует их.

**Перечисление осей (блок для коммита механизма; строки по оси — требование `tools/mechanism_gate.py`).** Семь механизмов: M1 P27, M2 AR-29,
M3 перепись + храповик, M4 храповик нагрузки процесса, M5 строка `judgment:` и гейт, M6 вопрос 11 и правило дизайнера, M7 проверка 41. Строка
оси закрывает каждый механизм по имени (правило 10 (b); критик t-1774 F-8); где механизм не назван — строка говорит «M… — n/a, <почему>».

| ось | вердикт |
|---|---|
| 1 Policy <-> role files <-> journal | covered — M1, M6: host adaptation 10 в CLAUDE.md, правило 1 designer.md и вопрос 11 брифа меняются одним коммитом (A1); M7 — проверка 41 в протоколе тем же коммитом; M2–M5 — n/a (пакет и гейт, не политика ролей) |
| 2 Per-tier exam instruments | queued — M6: правка `designer.md` гасит актуальность экзамена дизайнера (R1 a/b); Lead перегоняет экзамен, строка очереди в узле A1; M1–M5, M7 — n/a (не файлы ролей) |
| 3 Package <-> release copy <-> installed plugin | covered — M2 (`design/architecture.md`), M3 (перепись, её тест, правка `refusal_registry.sites`), M4 (`role-load.json`, `role_load.py`) идут в релизную копию с отпечатком (`release_fingerprint.py --write`); M5 (`tools/`), M1, M6, M7 — n/a (форджа, в релиз не идут) |
| 4 Factory rules <-> debt <-> backlog <-> principles | covered — M1 P27, M2 AR-29; текущие нарушения M3 (`breach` > 0) записываются строками `design/factory-rules-debt.md` под FR-47 (узел A3) |
| 5 Stage twins | covered частью B — §3 по стадиям; двойники S4/S5/S7 (причина ремонта) переписываются вместе; M1–M7 — n/a (часть A стадий не трогает) |
| 6 Measurement tools <-> package | covered — M4: `role_load.py` (новые поля); M3: строка итогов теста (C6) — вход проверки 41; `friction.py`, `stage_compare.py` — в протоколе эксперимента; M5 — n/a (гейт не мерило) |
| 7 Per-test identity | n/a — тождество теста не меняется |
| 8 Where the story is on disk | n/a — пути стори не меняются |
| 9 "is this a test file" | n/a — распознавание тестовых файлов не трогается (M3 исключает `scripts/tests/` константой теста, не распознавателем) |
| 10 git-top readers | covered — M5: гейт читает индекс и два блоба переписи (`git show HEAD:<p>`, `git show :<p>`) через уже существующий `gitcmd`, своего читателя не заводит |
| 11 shell-command recognizers | queued — часть B (узел X5, `guard_pre_tool.runs_check`) трогает распознавание команд; в части A не трогается |
| 12 carriers of the work plan | n/a — кучки и доска не меняются (узлы размещает Lead) |
| 13 the dispatch text | queued — часть B (б), бриф SD через `brief_pack.py`, узел X1; файл советов стадии в `given` брифа критика — X2-2 |
| 14 readers of agent transcripts | n/a — M7 читает перепись и `role_load.py`, не транскрипты |
| 15 console stream setup | n/a |
| 16 one JSON reader `hooklib.read_json` | covered — M3: тест переписи читает JSON через `hooklib.read_json`; M4: `role_load.py` читает `role-load.json` прежним путём; M5 — n/a (гейт в `tools/`, вне пакета: разбор блоба `json.loads` в `decide()`, как прочие гейты форджа) |
| 17 detector verdict shape | queued — X2-2: советы стадии становятся записями `detector_verdict` с признаком совета, а не сигналом человеку (критик B-3); M3 — n/a (тест переписи не детектор стадии; если перепись станет аудитом, её вывод идёт через `detector_verdict`) |
| 18 in-tree shrink-only ratchets | covered — M3 (`ratchet` переписи, `MEANING_CEILING`, `BLOCKING_ENTRY_FILES` — только растёт) и M4 (`process_ratchet_tokens`) входят в таблицу оси и в вопрос 9 тем же коммитом |
| 19 one reader of `tools:` | queued — часть B (хартии) может менять `tools:`; узел X1 читает через `host_adapter.role_tools` |
| 20 host receipt names | n/a |
| 21 markdown table readers | n/a — новых читателей таблиц нет |
| 22 host return form | n/a — форма возврата хоста не меняется (форма дайджеста роли — часть B, ось 13) |
| 23 fields of a `tests[]` row | queued — часть B узел X5 (обязательства S5) |
| 24 record of an execution | n/a |
| 25 freshness of a run | n/a |
| 26 the word `stand not confirmed` | n/a |
| 27 profile of a test row | n/a |
| 28 render site of the row form | queued — часть B узел X5 |
| 29 append-only jsonl writers | n/a — механизм не пишет jsonl |
| 30 commands of a profile | n/a |
| 31 Role carriers (после t-1702 D3) | covered — M1/M6: хартия становится единственным владельцем ремесла роли; M3: перепись — единственным владельцем класса проверки; M2, M4, M5, M7 — n/a (не носители роли); на `main` до D3 этой оси нет — строка пишется, если ось есть в файле на момент коммита (E-A3) |
| 32 Where judgment lives (новая) | covered — создаётся этим механизмом (M1–M7 — её состав) |

### 2.8 Четыре вопроса (правило 10 CLAUDE.md) по каждому из семи механизмов

| механизм | (a) цена и кто платит | (b) оси | (c) детектор | (d) что не даёт пропустить (код на пути) |
|---|---|---|---|---|
| M1 P27 | Lead: один абзац; любая сессия — чтение при работе над пакетом | §2.7 | проверка 41 | импорт PROJECT.md в CLAUDE.md (грузится каждой сессией); на дисциплине — явный выбор, детектор 41 (c) |
| M2 AR-29 | Lead: запись; каждый пакетный коммит — строка `architecture:` уже есть, AR-29 в ней называется при касании | §2.7 | тест переписи (опора); `architecture_index.py --check` и проверка 36 ловят дрейф индекса, не нарушение | `architecture_gate.py` в commit-msg (имя AR-29 в индексе) |
| M3 перепись + храповик | билдер: строка на каждую новую проверку (≈1 мин); CI: один тест на всех `scripts/*.py` (замер времени — в свидетеле узла A3) | §2.7 | сам тест (CI `package-fast`); проверка 41 (a), (d) | `test_judgment_census.py` лежит в `scripts/tests/` и попадает в `selftest.py --fast` / CI `package-fast` без правки `selftest.py` (критик F-7: `cmd_contracts` — явный список, `--contracts` не используется); CI идёт на MR/`main`/расписании |
| M4 храповик нагрузки процесса | автор текста роли: маркер на секцию; аудит A22 — уже идёт | §2.7 | A22 в `selftest.py --limits`; проверка 41 (b), (d) | `selftest.py --limits` в CI |
| M5 строка `judgment:` | каждый пакетный коммит: одна строка; гейт ≈ мс плюс два `git show` | §2.7 | проверка 41 (c) | `.githooks/commit-msg` → `architecture_gate.py` (после переноса Lead с `architecture_gate_next.py`, §2.4); дверь — `judgment: none -- <reason>`; миры переписи — E-A7…E-A11 |
| M6 вопрос 11 критика, правило дизайнера | критик: один вердикт-абзац на дифф; дизайнер: колонка «owner» в спеке | §2.7 | проверка 41 (c), (d); калибровка 15 (повторяющиеся находки критика) | бриф критика прикладывается к каждому диспатчу критика на дифф (host adaptation 5); на дисциплине для дизайнера — явный выбор, детектор 41 (c) |
| M7 проверка 41 | Lead: ≈ 15 мин в неделю | §2.7 | собственный детектор утечки в тексте проверки | расписание калибровки; «последняя калибровка» в Boot Report |

## 3. Часть B — план фабрики для экспериментальной ветки

Ветка режется от `main` после слияния `release-next` (бриф). Всё ниже — для неё. Ссылки на функции прочитаны по `def`-спискам файлов
(след §9); где роль функции выведена только из имени, стоит пометка «по имени — узел читает тело».

### 3.1 KEEP — то, что дало ×5 (не трогать)

| что | носители |
|---|---|
| данные по коду (P5, AR-6) | `ticket_adapter.py`, `source_inventory.py` (S0 по коду), `branch_accounting.py --units / --unhomed / --attachments` (листинг единиц текста и вложений), `blast_radius.py`, `manual_capture.py http\|ui` (руки и улики с хэшами), `exploratory_findings.py` (единственный писатель находок) |
| YAML/JSON-носители передачи (P4, AR-21) | `handoffs/*.yaml` + `handoffs/index.yaml`, `handoff_init.py`, `handoff_check.py --fix` (`DERIVERS`, `apply_values`), `manifest_put.py` (один писатель манифеста, AR-14) |
| слова человека (FR-8, AR-24) | `person_words.py` (`read`, `door`, `write_words`), `waiver.py`, `question_register.py`, `references/person-owned.json` (`why_person`), `guard_pre_tool.human_word_check` |
| ключи и ссылки (классы `shape`, `xref`) | `validate_artifacts.py` классы a и b (36 + 10 проверок, t-1761 §1), `s5_precheck` семьи `manifest`, `bindings`, `run_mapping`, `obligations` (как связка, не как закрытие), `oracle` (P20: литерал при открытом оракуле — это связка данных, не суждение; см. край E-B4), `traceability.py`, `check_traceability`, `check_coverage`, `ledger.py`, `null_outcomes.py` |
| защита (класс `safety`) | P-00 (`guard_app_under_test.py`), `guard_secrets.py`, `stage_guard.rule_pathspec`, `rule_stash`, `rule_tracker_route`, `check_resume`, `guard_pre_tool.git_config_check`, `config_write_check`, `stand_record_write_check`, `owner_check` (один писатель), запрет внешних записей (трекер/TMS — P8) |
| гейты человека (замысел) | `stage_guard.rule_gate_a`, `rule_gate_b`-ветка `rule_delivery`, `rule_gate_ordered`, `rule_order`; `gate_preflight.py` (репетиция гейта — данные) |
| измерения | `friction.py`, `role_load.py`, `turn_budget.py` (уведомление, не отказ), `cost_capture.py`, `retro_numbers.py` |

### 3.2 Таблица по стадиям S0–S9

| стадия | DELETE | KEEP | ADD | REWORK |
|---|---|---|---|---|
| S0 (код, дирижёр) | процедура запуска скриптов в `skills/qa-story/phases/s0.md` (535 строк) — переходит в код драйвера | `ticket_adapter`, `source_inventory`, preflight | — | `phases/s0.md` → строка карты драйвера «S0: данные по коду; вопрос только о доступе, который человек может дать (P5, D-0043)» |
| S1 `qa-scout` | халты хартии как единственный выход (exit_gate `is_halting_handoff` остаётся только для «данных нет»); 5 скриптов как процедура в файле роли | `adapters-read.md` (как читать), `source_inventory`, `grounding` как данные | хартия S1 (§3.3); вопрос наверх вместо халта; DoD «все источники оценены, каждое решение — с причиной» | `exit_gate.grounding_errors`, `awaiting_source_review` → советчик приёмщику (по имени — узел читает тело) |
| S2 `qa-requirements-tester` | проверка закрытой формы вердикта `ready/blocked` по правилу (`qa-requirements-tester:135`) как отказ | `branch_accounting` листинг (каждая единица имеет дом — `xref`), `check_register` ключевая часть | хартия S2 с техниками (§3.3); «требования без AC» (P23) как штатный случай | `stages.json` S2: советы — по стадии и роли, записями детектора (X2-2; `sizing.py` уже совет; у `branch_accounting.py` блокирующей остаётся связка «дом есть», советом — суждение о доме); дом `not_obligation: <why>` судит критик стадии; `validate_artifacts.check_behaviour_claims`, `check_delta_column` — по имени, узел классифицирует |
| S3 `qa-test-strategist` | закрытый `fit` как отказ (развилка F-3) | `planning_contract.py` связки (каждая строка плана ссылается на R-n), `risk-policy.md`, `automation-candidacy.md` | хартия S3: пирамида (P16, P19), риск-ориентированное тестирование, «где прячутся баги в диффе» | `stages.json` S3: советы по стадии и роли (X2-2); `check_plan`/`check_plan_v0` оставить ключи, снять закрытые значения `fit`, `defect_class` |
| S4 `qa-case-designer`, `qa-case-critic` | закрытые `then_oracles` как отказ кроме запрета `code` (F-3); `defect_class` как закрытый список | `check_case` ключи, `check_cell_counts`, `case_identity_errors` (связка), гейт A | хартия S4 с техниками тест-дизайна по имени; `qa-case-critic` перехартирован в критика стадий S2–S4 (F-2) | `critic_rollcall.py` → совет (по имени — узел читает); `check_then_oracles`: оставить «`code` — не оракул» блокирующим, остальное — совет |
| S5 `qa-automator`, `qa-code-critic` | `stage_guard.rule_manifest` — закрытый список `closed_unresolved_reasons` как отказ; `validate_artifacts.check_test_code` (класс c) как отказ | `manifest_put.py`, `s5_precheck` семьи `manifest`, `bindings`, `run_mapping`, `oracle`, `obligations` (связка) | хартия S5: стабильный e2e (ожидания по наблюдаемому каналу, не `sleep`, уникальные данные, изоляция), чтение диффа на риск; дефектный кейс — законный исход («поле не существует — кейс дефектен», вопрос наверх) | `rule_manifest`: `unresolved[]` с причиной свободным текстом, судит `qa-code-critic`; `s5_precheck.check_smells`, `check_copies`, `check_parameterization`, `check_plan_conformance` → советы критику (класс `meaning-proxy`, `blocks: false`) |
| S6 `qa-runner` | процедура 7 скриптов в файле роли | `run_suite`/`execution_request`, `manual_capture`, `proof_level`, `check_run_report_*` ключи | хартия S6 + первый исследовательский чартер (§3.6, F-4) | `phases/s6.md` (152 строки) — в код перехода |
| S7 `qa-failure-analyst` | 25-строчная процедура под валидатором (`qa-failure-analyst:84`) как единственный путь | `check_triage_v0` ключи; классы `APP_BUG/TEST_BUG/ENV/FLAKY` как маршрутизация (кто действует, FR-19) | хартия S7: «сначала пойми, что говорит красный»; дискриминация причины; кейс-дефект — исход | классы триажа — данные маршрута, вердикт роли со свидетелем; приёмщик — драйвер |
| S8 `qa-doc-scribe`, `qa-bug-reporter` | `check_report_forbidden`, `check_report_human_text` (класс c) как отказ; закрытый `confirmation` (F-3) | `check_delivery` (три слова из типизированных записей), `check_report_left_with_you` (связка с леджером, P21), `check_coverage`, гейт B | хартия S8: отчёт говорит «в этих границах, этими техниками»; баг-репорт: шаги, оракул, влияние | `check_report_*` с суждением о тексте → совет; `confirmation` → предложенный список (F-3) |
| S9 `qa-retro-analyst` | — | `retro_numbers.py`, `friction.py` | хартия S9: где фабрика не смотрела; вход — перепись и нагрузка | ретро читает `role_load.py --all` и переписные счёты (вход проверки 41) |

Сквозные строки (все стадии):
- **`exit_gate.py`** — REWORK до «артефакт есть и в форме»: KEEP `required_outputs_errors`, `witness_errors` (есть ли файл свидетеля),
  `answered_question_errors` (связка), `unreadable_record` (AR-28); DELETE как отказ `form_stop_errors` (форма дайджеста: 21 из 26 блоков,
  speed-cost 27.10), `_judged_digest_errors`/`judge_words` (LLM-судья, сводящий слова к закрытому списку — `word-list`); `detector_errors`
  остаётся, но набор детекторов сжимается. **Сегодняшний механизм `advice` для этого НЕ годится** (критик t-1774 B-3, прочитано:
  `advice_detectors()` `exit_gate.py:84-90` собирает `advice` всех стадий в одно множество скриптов; `detector_gates()` `:371-376` сливает
  `detectors` по роли через все стадии; вывод советчика уходит человеку как `person_signal(…, "gate_unreadable", …)` `:404-410`, `:515-516`,
  обрезанным до 200 символов). Перестройка — узел X2-2 (§4): совет по стадии и роли, по записи детектора, в файл советов стадии для приёмщика.
- **`handoff_check.py`** — KEEP `--fix`, `apply_values`, проверку утверждений `CLAIMS` (связка); REWORK «судью» (раздел «the judge» шапки):
  при открытых словарях (F-3) он не нужен; при предложенном списке — печатает соответствие как совет, не заменяет слово роли.
- **`validate_artifacts.py`** — KEEP классы a/b; DROP класс c (3 проверки: `check_report_forbidden`, `check_report_human_text`,
  `check_test_code` — t-1761 §1) как отказ, переносом в советы критику; строки A24/переписи меняются тем же коммитом.
- **`guard_pre_tool.py`** — раздел на два списка (по `def`-списку, тела читает узел X5):
  защита (остаются отказом): `git_config_check`, `human_word_check`, `owner_check`, `config_write_check`, `stand_record_write_check`, `stage_check`,
  запрет внешних записей; форма/содержание (→ WARN или удаление, F-5): `size_check`, `big_read_check`, `plugin_read_check`, `logs_check`,
  `runs_check`, `case_store_check`, `handoff_write_check`, `handoff_values_check`, `artifact_rewrite_check`, `plan_write_check`,
  `manifest_write_check`, `writes_check` (по имени).
- **Закрытые словари** `defect_class` (`validate_artifacts.py:177-181`), `then_oracles` (`check_then_oracles`), `fit`, `confirmation`, вердикт
  `ready/blocked` S2 — по F-3; инвариант при любом выборе: `code` как оракул отклоняется всегда (P20, FR-58).
- **`inject-map.json`** — срезы роли сжимаются до: хартия (вместо файла роли) + манифест тестировщика + одна страница контракта ключей (что
  кладу в YAML, генерируется из `handoffs/*.yaml`) + файлы проекта. Срезы `common-rules` — только строки, нужные для формы передачи;
  процедура исчезает.

### 3.3 ADD (а) — хартия роли (заменяет файл роли)

**Форма хартии** (одна на роль, `agents/<role>.md`, front matter `tools:` как сейчас; секции с маркерами `kind`):

1. `## Исход` (process) — одна фраза: за что роль отвечает целиком.
2. `## Хороший исход` (process) — DoD, по которому принимает тир выше: 3–6 пунктов, каждый со своей формой свидетеля.
3. `## Где на этой стадии прячутся баги` (craft) — опыт: какие места чаще ломаются и почему.
4. `## Техники` (craft) — по имени, с одной строкой «когда применять»: классы эквивалентности, граничные значения, переходы состояний,
   таблицы решений, pairwise, угадывание ошибок, риск-ориентированное тестирование, исследовательские чартеры; для S5 — стабильный e2e;
   для S3/S5 — чтение диффа на риск.
5. `## Инструменты` (process) — список скриптов, которые роль МОЖЕТ вызвать, и что каждый даёт; без «обязан» и без порядка.
6. `## Когда спросить` (process) — дорога вопроса (§3.5 (г)).
Дано / владеет / не цель / handoff — НЕ в хартии: их несёт бриф каждого диспатча (§3.4).

**Бюджет:** хартия ≤ 150 строк, из них craft ≥ 50 % по `role_load.py` (`craft_tokens / (craft+process)` на файле хартии); вся нагрузка роли
без файлов проекта — цель F-1. Мерило — `role_load.py --all --json`, цифры в свидетеле узла.

**Содержание по ролям (скелет ремесла; полный текст — работа узла X1/X5, проверяется критиком на план):**

| роль | исход | хороший исход (DoD приёмщика) | где прячутся баги | техники по имени |
|---|---|---|---|---|
| qa-scout (S1) | все источники требований найдены и оценены | каждый источник: прочитан / недостижим (причина пробы) / не относится (почему); связанные задачи и вложения учтены; список «что не нашёл и где искал» | связанные задачи, комментарии, вложения, родитель; соседние MR | риск-ориентированный отбор, угадывание ошибок по истории багов зоны |
| qa-requirements-tester (S2) | реестр требований полон и проверяем | каждая единица текста имеет дом; каждое требование проверяемо или вопросом; противоречия подняты с цитатами обеих сторон; утверждения из диффа помечены как утверждения (P20) | составные требования, неявные условия, отказы и ошибки, «молчание» требований о граничных случаях | разбиение на классы эквивалентности, таблицы решений, переходы состояний (для требований со статусами) |
| qa-test-strategist (S3) | план находит баги с наименьшей ценой | каждое требование в плане или с причиной «не тестируем»; уровень пирамиды обоснован риском (P16, P19); для каждого риска — гипотеза дефекта | изменённые ветки диффа, швы между фичами, общий изменяемый стейт, права, конкурентность | риск-ориентированное, pairwise для конфигураций, чтение диффа на риск |
| qa-case-designer (S4) | кейсы, которые упадут там, где баг | каждый Then наблюдаем по независимому каналу; оракул назван; граница и негатив на каждое требование с вводом; кейс говорит ЧТО, не КАК (P17) | граница ввода, пусто/много/повтор/порядок, прерванная операция, ввод с клавиатуры по символу | граничные значения, классы эквивалентности, переходы состояний, таблицы решений, угадывание ошибок |
| qa-case-critic → критик стадий S2–S4 (F-2) | принимает или возвращает исход S2–S4 по смыслу | вердикт accept/reject с `failure_class` и свидетелем (цитата артефакта); «где не смотрели» на каждое отклонение; советы стадии (файл X2-2) прочитаны | пропущенные требования, кейсы, которые не могут упасть, оракул из кода | анти-дубль, «может ли этот кейс упасть», проверка оракула |
| qa-automator (S5) | тесты, которые падают на баге и стабильны | красная проба на каждый тест; каждый Then привязан или с причиной; дефект кейса — вопрос наверх, не красный «contradicts_requirement» | поле, которого нет в ответе; ожидание из реализации; общий стейт тестов | стабильный e2e: ожидание наблюдаемого события, уникальные данные, без `sleep`, уровень ниже, где можно |
| qa-code-critic (S5) | принимает тесты по смыслу | вердикт на каждый тест: может ли упасть, тот ли уровень, не дублирует ли; причины `unresolved[]` прочитаны | маскировка, overmocking, проверка ответа того же действия | рубрика `code-review-rubric.md` как знание, не как закрытый список |
| qa-runner (S6) | исполнение с уликами; исследование по чартеру (F-4) | каждая строка: запущено / не запущено (почему); у ручного шага — улика; наблюдения по ходу — все (P26) | ввод по символу, отказ каждой зависимости, перезагрузка посреди операции | исследовательские чартеры, матрица возмущений (`references/perturbations.json`, XT2-2) |
| qa-failure-analyst (S7) | каждый красный объяснён | причина с дискриминирующей уликой; дефект кейса отделён от бага продукта | локатор vs таймаут vs данные; ожидание из кода | анализ первопричины, перепрогон для FLAKY, сверка с оракулом, не с кодом |
| qa-bug-reporter (S8) | баг, который разработчик воспроизведёт | шаги, оракул (требование), фактическое, влияние, улика | — | минимизация воспроизведения |
| qa-doc-scribe (S8) | отчёт, по которому человек решает | «в этих границах, этими техниками»; Left with you полон (P21) | — | — |
| qa-retro-analyst (S9) | где фабрика не смотрела и сколько стоило | данные переписи, трения, нагрузки; одна метрика на сравнение | — | — |
| conductor → driver (Lead) | стори доведена до решения человека | каждое принятие — со свидетелем; вопрос человеку — только класса `why_person`; бюджет держится | — | — |

### 3.4 ADD (б) — диспатч в форме SD для каждой роли

`scripts/brief_pack.py` (единственный писатель брифа) печатает в начале брифа строки-заголовки, как R11-f у форджа:

```
goal: <исход стадии одной фразой из хартии>
DoD: <пункты «Хороший исход» хартии>; witness: <что приложить: пути улик, таблица tried>
given: <пути артефактов прошлых стадий, данные по коду, файлы проекта — именами>
owns: <пути, которые роль пишет>
non-goals: <что не делать на этой стадии>
handoff: <путь формы передачи> (ключи — `handoffs/<form>.yaml`)
questions: question_register.py --raise ... (дорога §3.5 (г)); halt — только когда данных нет и спросить некого
```

Шаблон — правило 11 CLAUDE.md (DoD, манифест, вопрос наверх). Узел пишет шаблон в данные (`references/brief-form.json` или раздел
`handoffs/index.yaml` — решение узла, §8 S-5), `brief_pack.py` его рендерит; тест: бриф каждой роли на фикстуре стори содержит семь строк.
Край: строка, для которой нет данных (нет `given` у S1 кроме тикета) — печатается с `—` и причиной, не опускается (AR-23). Бриф критика
стадии (X2-1) несёт в `given` файл советов стадии (X2-2); файла нет — строка `given` называет его с `—` и причиной (E-A15).

### 3.5 ADD (в) — приёмка по смыслу тиром выше; (г) — дорога вопроса

**(в) Приёмка.** Приёмщик — критик стадии (F-2) или драйвер как Lead. Читает: артефакт, таблицу `tried` (требование × техника × наблюдение ×
путь улики), свидетель (пути `manual_capture`, строки прогона), советы кода (файл советов стадии — записи бывших детекторов, теперь `advice`,
X2-2), хартию (пункты «Хороший исход»). Вердикт: `accept` / `reject` с `failure_class ∈ {spec, capability, data, tooling}` и цитатой.
Отклонение → повтор той же роли в свежем контексте, несущем только артефакт и вердикт (как cost gate 6 форджа); число раундов — ОДНО на
фабрику: `repair_budget` контроллера (`controller.py:1851-1863`, потолок из `runtime_policy.py:13` — сегодня `repair_cycles: 2`,
`design_repair_cycles: 2`), читаемый драйвером через `story_run.Driver.repair_budget` (`story_run.py:9209`); второго счётчика «один повтор»
нет (критик F-3, AR-13; §8 S-8). Потолок исчерпан → эскалация к драйверу (вверх по ФУНКЦИИ, не по модели: FR-52 — правка, держащаяся только на
сильной модели, не правка). Драйвер: повтор с уточнённым брифом, вопрос наверх или принятие с записанным пробелом (AR-27). Где код остаётся:
`exit_gate` — «артефакт есть, ключи на месте, свидетель есть»; вердикт приёмщика — запись приёмки стадии, форма и читатель которой живут в
существующем `scripts/acceptance.py` («Semantic acceptance of a bounded automation window», читатели: `controller.py`, `manifest_put.py`,
`check_delivery.py`, `ledger.py` и др.) — он расширяется с окна автоматизации на стадию (X2-5; §8 S-9); пишет запись в `pipeline.json`
`stage_done.py` (один писатель); код проверяет её только на присутствие и форму (класс `shape`).

**(г) Вопрос.** Открытый вопрос роли — нормальный дешёвый ход: `question_register.py` (уже есть), запись с `asked_by`, текстом и тем, что роль
прочла. Драйвер разбирает сам (P22, «сначала разбирается сам»): ответ из данных на диске → закрывает с `answered_by: driver` и источником.
Человеку — только с классом `why_person` из `references/person-owned.json` (проверка 38) и пачкой на ближайшем гейте или на «человек может
дать доступ». Роль продолжает работу по рекомендации, помечая затронутое «до ответа» — вопрос не останавливает стадию. Это заменяет: халт как
единственный выход (кроме «данных нет»), закрытые списки причин (`closed_unresolved_reasons`) — причина пишется словами и судится приёмщиком.

### 3.6 ADD (д) — первая хартия и протокол эксперимента

**Первая хартия — исследовательский чартер.** Скилл `qa-explore` (предложение `plans/exploratory-charters-proposal.md`) требует 16–19 цепочек
«билдер → критик» и шагов `type`/`fail_request`, которых ещё нет (находка `20261031-qa-explore-…`, раздел «Зависимости»: «узлы … ещё не
названы — не проверено»). Поэтому рекомендация (F-4): первая хартия — **исследовательский диспатч `qa-runner` внутри qa-story на S6** с
чартером qa-explore (гипотезы раньше маршрута, оракул, опровергающее наблюдение, оси возмущений `request_failure` и `keyboard_input` из
XT2-2), руками `manual_capture.py ui|http` (есть), находками через `exploratory_findings.py` (есть). Если шагов `type`/`fail_request` нет на
ветке к моменту прогона, чартер исполняет `page.route`/посимвольный ввод через существующий `manual_capture ui` — узел X3 проверяет, может ли он;
не может — это строка разрыва, а не повод вписать правило MyBooks.

**Протокол (одна метрика на сравнение, MEASUREMENTS п. 6b):**
- Стори: CART-1 (MyBooks `a25b080`, стенд-копия, `docs/RUNBOOK.md` §11); эталон — Б-1, Б-2, Б-4 (обязательные), Б-3 (вопрос человеку, не
  условие); требования R-9, R-13, R-16 (контроль их не проверил, `cart-1-run-problems.md` §3.1).
- Плечи: A — `main` в момент среза ветки, без изменений; B — ветка. Данные по коду одинаковые: снимок S0 (`work/ticket-snapshot.json`,
  `source-inventory.json`, дифф) делается один раз и копируется в оба корня; хэши входов — в отчёте эксперимента.
- Слова человека: один файл ответов на оба плеча (как `experiments/measurers/answers/`), драйвер в фоне (`docs/RUNBOOK.md` §9).
- Меры (каждая — своя строка сравнения, свой носитель):
  M1 эталонные баги найдены (Б-1, Б-2, Б-4: да/нет, с шагами и уликой; судит Lead по оракулам находки);
  M2 прочие подтверждённые Lead находки и ложные баги (два счёта);
  M3 вопросы человеку: всего и избежимых (критерий проверки 38: ответ был на диске);
  M4 трение FR-55: доля ходов, `scripts/friction.py` по транскриптам;
  M5 нагрузка роли: `role_load.py --all --json` (токены, craft/process);
  M6 цена: один носитель — `cost_capture` по транскриптам (цена транскрипта); самоотчёт не смешивается;
  M7 время: метки стадий `pipeline.json`;
  M8 покрытие R-9/R-13/R-16 (есть кейс/проба с вердиктом: да/нет);
  M9 запуски автотестов (слово владельца 04.11.2026: «когда в проекте долгие тесты, запуск лишних становится проблемой»): сколько раз
  за прогон запускались тесты проекта (носитель — `driver-runs.jsonl` / `events.jsonl` S5–S7, команды `npm test`/`pytest`/playwright в
  записях ролей), сколько тестов в каждом запуске, и сколько запусков ЛИШНИХ — повтор без изменения кода, теста или данных между
  запусками, запуск всего набора там, где менялся один файл, прогон того же теста в S5 и снова в S7 без починки. Счёт — по стадиям;
  лишний запуск называется с причиной.
- Сравнение стадий — `stage_compare.py`-образно: по стадии S1–S4 артефакты B против A, «меньше, чем у A» — разбор (PROJECT.md правило 5).
- Бюджет (против блуждания без рельсов): на диспатч роли в B — потолок = 2 × цена той же стадии в A (M6, тот же носитель); `turn_budget.py`
  остаётся уведомлением; на потолке драйвер (не хук) останавливает диспатч и принимает частичный исход с пробелом или отклоняет. Ловит
  блуждание: M4 и M6 по стадиям, плюс «ходов на находку».
- Порог успеха (рекомендация, решает владелец): B находит ≥ 2 из Б-1/Б-2/Б-4 и M3-избежимых ≤ A, при M6 ≤ 1,5 × A; иначе разбор, а не следующая
  фаза.

## 4. Пачки (в порядке исполнения; узел пишется для более слабой модели — PROJECT.md «Командная работа» п. 11)

Каждая строка узла: файл, функция/поле, ожидаемое поведение, тест. Направление выбрано или стоит развилка с рекомендацией (узел исполним по
рекомендации до ответа).

### Пачка A — страж форджа (по F-6 (а): A5 и A1 — на `main` сразу; A2–A4 — первым патчем после слияния `release-next`, до среза ветки)

**Ход (Lead, 03.11.2026 22:3x):** A1 — принято, `main` bcab2866 (тексты P27 / host adaptation 10 / вопрос 11 / правило дизайнера / проверка 41 /
ось 32 / D-0060; док-свидетель `tools/test_a1_judgment_texts.py` 7/7). A5 — принято, `main` 3384384a (билдер t-1778, критик t-1779
fit_with_fixes, фикс-раунд t-1780; K4 на живом имени 97/97; гейт живой — строка `judgment:` требуется с этого коммита, мир (i) до A3).
**Ход (Lead, 04.11.2026 07:50) — итог ночи:** ветка `experiment/thinking-roles` = 4d31b3ac. Все три темы прошли критика и фикс-раунды: X1
(t-1816 → fix-4 t-1819, fix-5 t-1821), X2 (t-1815 → fix-2 t-1818), X3 (t-1811 → fix-2 t-1812); CI-фиксы t-1817, t-1820. **Финальный CI
ветки — 8029407** (канон; читать `python tools/ci_read.py jobs 8029407`): прежние красные (lint, null outcomes, маршрут блока, A27, F11/F17)
закрыты; открыты для чтения CI: A22 qa-case-critic +6…+68 токенов на Linux (не CRLF — `role_load` нормализует; причина не названа),
`test_repair_route` 174/176 (S4 `cases_in_repair OpenWork` на `s4_after_critic`), `test_no_move_seam.py` не прогнан локально. Решения ночи и
очередь — в строке 06:35 ниже; добавлено: `questions[]` поднимаются из формы КРИТИКА (у авторов секции нет), классный вопрос без `why_person`
не в списке гейта A (`gate_brief.still_open`), `stage_done --acceptance` привязан к `inputs_read` критика, `run_advisers` никогда не блокирует,
`stage_review_exhausted` → `no_move(call=False)`, `witness_paths[]`/`inputs_read[].version` необязательны, SD-шапка ≤ 1024 Б видна `role_load`
(слой брифа 6144 → 7168), K6 — путь скриптов в карточке S5 закреплён. Утро: прочитать 8029407, при красном — фикс-раунд; затем X0-1/X4-1 по
слову владельца (стенд её), M1 эксперимента пишет источник находки.

**Ход (Lead, 04.11.2026 06:35):** ветка `experiment/thinking-roles` = 498df887 — ВСЕ узлы X1 (B-A…B-D, fix-1…3), X2 (B0…B4, fix-1, B4-finish)
и X3 (+ fix-1, fix-2) слиты. Критики: X3 — t-1811 принят (fit_with_fixes, фикс-раунд t-1812 слит, тема закрыта); X2 — t-1815 в работе
(`reviews/t-1815-critic-x2.md`); X1 — t-1816 в работе (`reviews/t-1816-critic-x1.md`). CI ветки — 8029089 (канон). После вердиктов: фикс-раунды
свежими билдерами, повторный CI, утренний отчёт. Решения ночи («решила сама»): SD-шапка брифа — форма, вне `budget_of`, свой кап 1024 Б (кап
тела 6144 не поднят); `advice` в `stages.json` — список; `judge_words` → xref/intent; ранг `safety` ниже суждений; тест переписи в быстром CI;
`tried_errors` — adds data check (+1 blocking ×4); `roles` над `kind` законен; вопрос роли без класса `why_person` не держит гейт A; вердикт
критика стадии — `header.verdict`; reject на последнем раунде S4 → шов дирижёра (F-X2-7); ожидание стенда у ручного вызова 120 с; подъёмы
храповиков названы (qa-runner +27, qa-case-critic 15874→17573 хартия). Не достигнуто: F-1 ≤ 6000 токенов (нагрузка 12–16K — слои инъекции, X5);
K11 breach S2–S4 = 0 по счёту переписи не выполнен буквально (16 единиц S5–S9 несут все роли в `roles`; владельцы X5/X7). Очередь: X5-8 (аренда
ручного окна безусловная, `hold_stand` root, ключ `manual_stand_wait_s`, `lease_error`), `s5_precheck` oracle family и `new:` источник (X5),
читатель `tried.md` (X4), K6 S5 waiver inline (критик X1 называет узел), qa-case-critic без записи в `brief-form.json` (X5-1), якоря
`story_run.py:8744`/`sizing.py:4`. Живые прогоны X0-1/X4-1 — утром по слову владельца.

**Ход (Lead, 04.11.2026 04:40):** ветка `experiment/thinking-roles` = 3591cf11 (worktree интеграции `.claude/worktrees/agent-acb67480a48b56ff2`,
слияния веток билдеров `worktree-agent-<id>`; при конфликте в файлах фикс-раунда пачки A — версия ветки). Слиты: X2-2b (t-1799), X1 B-A
(t-1797), B-B (t-1798), B-C (t-1802, хартии 51–53 % ремесла), X1 fix-1 (t-1804), X2 B1 (t-1800, советы стадии), B2 (t-1803, открытые словари),
X3 (t-1801, чартер + `requests-seen` + аренда), X3 fix-1 (t-1807), X2 fix-1 (t-1806). В работе: X1 B-D (t-1805, 150 пинов + тест порядка
маркеров), X2 B3 (t-1808, запись приёмки, дорога вопроса). **Дальше:** (1) X2 B4 после B3 — строка `| B4 |` §5 черновика X2 (маршрут критика
стадии, `qa-case-critic` хартия, `stages.json` roles/acceptance_by, фазы s2–s4, перепись — ЕДИНСТВЕННЫЙ писатель: удалить 4 строки
`exit_gate.form_stop_errors`/`_judged_digest_errors`/`judge_form.digest`/`digest_errors`, `judge_words` → xref/intent, добавить
`contract.open_word_errors` shape, `_ask_judge` override «advice only», потолки к факту); (2) X1 fix-2: `test_role_load` K10-a (ждёт `craft 0`),
`test_handoff_values` K11 (пины B-B), `test_exit_gate_scope.py:270` стенд-ин; (3) X2 fix-2: `test_exit_gate_unreadable` 3 красных (контракт
`run_advisers` после B1 возвращает список записей), `references/judgments.d/form.json` `row_state_vocabularies` без читателя; (4) критик на тему —
три прохода (X1: B-A…B-D + фиксы; X2: B0…B4 + фиксы; X3), фикс-раунды свежими билдерами; (5) CI ветки `python tools/ci_read.py start --ref
experiment/thinking-roles` как канон; (6) утренний отчёт списком «решила сама» (ниже). Очередь из узлов: пять вызовов `_stage_id(agent)` без `task`
(exit_gate :1042/:1099/:1325/:1332/:1642 → B4), `s5_precheck` oracle family блокирует `new:` источник (X5), `exit_gate.py`/`story_run.py`
якоря пинов (B-D отчёт), feature-глобы новых файлов — при каждом слиянии в `plans/features.json`. Живые прогоны X0-1/X4-1 — утром.

**Ход (Lead, 04.11.2026 03:45):** пачка A целиком в `main` ОДНИМ коммитом 3a4cf360 (A2 aeef1232 + A3 38b4c594 + A4 809c0bad + фикс-раунд
t-1796 по критику t-1793, squash: гейт `judgment:` верно отказал `none` на подъёме внутри ветки, на `main` перепись создаётся — мир ii);
первая перепись: 245 файлов, 894 единицы, breach=20, `MEANING_CEILING`=24; канон — пайплайн `main` 8028633 (красный K6
`test_retro_always_full` — фрагмент changelog после релиза 0.10.9, зона соседней сессии). Очередь из критика t-1793: F7 (`audit_factory.py` вне
owns фикса), «kind-строка ложится в срез предыдущей секции» (contract_slices, узел до первого маркера в срезаемом источнике), K7 спеки не
совпадает с заголовком проверки 41. **Ветка эксперимента `experiment/thinking-roles` = 3a4cf360.** Волна 1 (worktree-билдеры, слили
старую историю ветки 96bf4bad — при интеграции конфликты по переписи/role_load/contract_slices решать в пользу ветки): t-1797 X1 B-A
(форма хартии, SD-бриф), t-1798 X1 B-B (срезы, страница ключей, `tried`), t-1799 X2 B0 (X2-2b). Волна 2 после них: X2 B2 (после B-B —
общий `handoff_check.check`), X3 (после B-A — общий `brief_pack.build`; спека `t-1765-x3-explore-charter.md` §6 owns), X1 B-C (хартии, после
B-A и B-B; пишет перепись и `role-load.json`), X2 B1 (после B0); затем B3, B4 (последний писатель переписи X2), B-D (пины), B-E (X1-8).
Критик — один на тему при интеграции (X1, X2, X3), фикс-раунды свежими билдерами. Утренний список «решила сама»: F-X2-7 (reject на
последнем раунде → шов дирижёра, не тихое закрытие), M4 (`judge_words` → `xref`/intent), ранг `safety`, тест переписи в быстром уровне CI,
`tried_errors` как `adds data check` (+1 blocking у четырёх ролей), X3 без критика на план. Прежняя строка хода ниже — история ночи.

**Ход (Lead, ночь 04.11.2026, владелец спит — развилки по рекомендации, утренний отчёт списком):** `local/p1-closeout` слит в `main`
(моё слияние cffe43a37, MR !14 → a2bb4de9e; релиз 0.10.9 соседней сессии — 878641cc9). A2 — сдан aeef12326 (worktree-agent-aa63d7f01f9915118,
t-1788); A4 — сдан 809c0bad0 (worktree-agent-aec4adf805ca64faf, t-1790; pytest-форма K10 не работает из-за `harness.finish()` → канон
`python -B <файл>` 149/149; A22 гоняет `audit_factory.py`, не `selftest --limits`); A3 — билдер t-1789 (worktree, handoff
`docs/tasks/handoffs/t-1788-a3-report.md`) в работе. План интеграции: ветка от `origin/main` → слить три worktree-ветки → узкие свидетели →
ОДИН критик на пакетный патч (R13-g; токен `critic:` закрывает t-1788/t-1790) → фикс-раунд свежим билдером при нужде → push `main` → срез
`experiment/thinking-roles` от этого `main`. Черновики ветки приняты по следу: X1 `docs/tasks/specs/t-1765-x1-charters-s1-s4.md` (t-1784,
3 билдера B-A/B-B/B-C), X2 `docs/tasks/specs/t-1765-x2-meaning-acceptance.md` (t-1785, B1–B4, `очередь: B3 → B4`), X3
`docs/tasks/specs/t-1765-x3-explore-charter.md` (t-1786, один билдер; посылка E-B8 устарела — `fail_request` и ввод по символу уже в дереве);
критик на план X1+X2 — t-1792 (`docs/tasks/specs/reviews/t-1792-critic-plan-x1-x2.md`), после него — билдеры на ветке. Живые прогоны X0-1/X4-1 —
утром по слову владельца (стенд — её; `/api/health` ok). Очередь: D1 (`architecture_gate._show` ↔ `piles.git_show` → `gitcmd`), перегон
экзамена дизайнера (R1 b), узел для S1 exit-gate (X1 F-X8: §3.2 S1 без узла в §4), M1 эксперимента пишет источник находки (строка плана RN1-6
или клетка чартера — X3 §10). Журнальные id: плотно по валидатору (max+1), соседняя сессия пишет в тот же файл — хвост перечитывается перед
каждой записью.

| узел | файл (owns) | что | поведение | тест / свидетель |
|---|---|---|---|---|
| A5 (билдер, форджа) — первым | owns: `D:/ws1/yml-text-factory\tools\architecture_gate_next.py`, `D:/ws1/yml-text-factory\tools\test_architecture_gate_next.py` (соседние имена; живой `tools/architecture_gate.py` переносит Lead, §2.4) | вторая строка `judgment:` §2.4: четыре формы; перекрёстная проверка по двум блобам переписи; миры (i)–(v); позиция в `decide()`; `_prose_matches(msg, line_re=…)` параметризован, не скопирован | на `main` до A3 — мир (i): требуется только форма строки; один отказ называет проблемы обеих строк | K4 (на соседнем имени до переноса, на живом — после) |
| A1 (Lead, док) | `PROJECT.md`; `CLAUDE.md` (host adaptation 10); `docs/tasks/critic-diff-brief.md`; `.claude/agents/designer.md`; `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md`; `docs/SIBLING_MAP.md`; `DECISIONS.md` (строка D-нового) | тексты §2.1, §2.5, §2.6, §2.7 | ключи K1, K5–K9; тексты могут называть файлы A3/A4, которых ещё нет на `main` (имена закреплены этой спекой); проверка 41 (a)/(b) до A3/A4 пишет строку «не на main» (E-A13) | док-свидетель: ключи K1, K5–K9 дословно, скрипт с отрицательным контролем (правило 11, DOC-DISPATCH WITNESS) |
| A2 (билдер, пакет) | `ai-packages/qa-factory/design/architecture.md` (AR-29; поле Detector у AR-2 `:56` и AR-7 `:93`); `docs/ARCHITECTURE_INDEX.md` (генерируется) | AR-29 §2.2; Detector AR-2/AR-7 → ссылка на перепись и проверку 41 | индекс 29 записей, `--check` зелёный | K2 |
| A3 (билдер, пакет; критик t-1779 Q2: тест переписи краснеет на любом ПРОПАВШЕМ верхнем потолке `ratchet` и на пустом `ratchet: {}` — гейт A5 пропускает исчезновение под `none`, страж от снятия стража — этот тест; Q1: база сравнения при `commit --amend` — сам исправляемый коммит, подъём, спрятанный amend-ом, ловит проверка 41 (c), код-гейта нет — на дисциплине) | новый `scripts/tests/test_judgment_census.py`; новый `scripts/tests/fixtures/judgment-census.json`; `scripts/refusal_registry.py` (только функция `sites`: аргумент `files`, по умолчанию `SCANNED`); `design/factory-rules-debt.md` (строки текущих нарушений под FR-47) | перепись §2.3, C1–C6; явные строки классов для `judge_words`, `judge_form`, `judge.py`, `readiness.py` | первая перепись = текущие счёты (потолки по факту); мир (ii) гейта — `judgment: none -- census created`; `refusal_registry.py --check` зелёный (A24 не меняет поведения) | K3; `python -B ai-packages/qa-factory/scripts/refusal_registry.py --check` → exit 0 |
| A4 (билдер, пакет) | `scripts/role_load.py`; `references/role-load.json`; аудит A22 в `audit_factory.py` | `craft_tokens`, `process_tokens`, `process_ratchet_tokens`, `target_tokens` | неразмеченное = процесс; строки плотные | K10; `python -B -m pytest ai-packages/qa-factory/scripts/tests/test_role_load.py -q` (файл есть — критик t-1774 §1 (h)) |

Порядок: **A5 → A1** на `main` сразу (гейт в мире (i) требует только форму строки; тексты A1 называют имена, закреплённые спекой); затем
**A2 ‖ A3 ‖ A4** первым пакетным патчем после слияния `release-next` (коммит A3 — мир (ii)). Прежняя строка «A2 ‖ A3 ‖ A4 → A5 → A1»
противоречила принятой F-6 (а) (критик t-1774 B-2). Живой путь A5 ставит Lead переносом с соседнего имени (правило 2: файл
самоактивирующейся проверки билдер не ставит). Критик: один проход на пачку (R13-g); критик на план — пройден (t-1774), этот фикс-раунд —
его исполнение.

### Ветка эксперимента

| пачка | узлы | содержание | приёмка |
|---|---|---|---|
| X0 базовая линия | X0-1 прогон плеча A на CART-1; X0-2 снимок переписи и `role_load.py --all` на срезе | данные M1–M8 для A | отчёт `experiments/mybooks/thinking-roles/arm-a.md` с носителями чисел |
| X1 хартии S1–S4 + бриф SD | X1-1 форма хартии и маркеры `kind` (шаблон `agents/_charter-template.md`? — §8 S-4); X1-2..X1-5 хартии qa-scout, qa-requirements-tester, qa-test-strategist, qa-case-designer; X1-6 `brief_pack.py` семь строк §3.4; X1-7 `inject-map.json` срезы S1–S4 | хартии ≤ 150 строк, craft ≥ 50 %; нагрузка ≤ цели F-1 | `role_load.py --all --json` до/после; `selftest.py --limits`; тест брифа (семь строк на фикстуре) |
| X2 приёмка по смыслу S2–S4 + вопрос | X2-1 `qa-case-critic` → критик стадий (F-2); X2-2 советы стадии по стадии и роли, записями детектора, в файл для приёмщика (подробно ниже); X2-3 `exit_gate.form_stop_errors`, `judge_words` сняты как отказ; `judge.py` — советчик или судья (критик Q-2, ниже); X2-4 словари S2–S4 по F-3; X2-5 запись приёмки стадии — расширение `scripts/acceptance.py`, писатель `stage_done.py` (ниже); X2-6 `question_register` + драйвер (P22) без халта; X2-7 маршрут критика стадии S2–S4 (ниже) | перепись: `breach` S2–S4 → 0; потолки опущены | `test_judgment_census.py`; `test_stage_joints.py`; `refusal_registry.py --check`; `test_words_doors.py`; K13, K14 |
| X3 первая хартия (исследование) | X3-1 чартер qa-explore для `qa-runner` на S6; X3-2 `references/perturbations.json` (оси `request_failure`, `keyboard_input`, XT2-2 п. 2–3) — или ссылка на узел XT2-2, если он уже слит; X3-3 проверка, умеет ли `manual_capture ui` подмену маршрута и посимвольный ввод | чартер исполним; разрывы — строками | тест на фикстуре потока из трёх запросов (из находки: «чартеры порождены на каждый») |
| X4 прогон плеча B и сравнение | X4-1 прогон; X4-2 отчёт M1–M8 | порог §3.6 | отчёт `experiments/mybooks/thinking-roles/compare.md`; решение владельца |
| — | **стоп: слово владельца по итогам X4** | | |
| X5 S5–S8 | X5-1 хартии qa-automator, qa-code-critic, qa-runner, qa-failure-analyst, qa-bug-reporter, qa-doc-scribe; X5-2 `stage_guard.rule_manifest` — свободная причина; X5-3 `s5_precheck` `check_smells` и др. → советы; X5-4 `validate_artifacts` класс c → советы; X5-5 `guard_pre_tool` форма → WARN (F-5); X5-6 `confirmation`, `fit` (F-3); **X5-7 параллельные окна S5** (слово владельца 03.11.2026; узел CD1-24 / B-080): на ветке исполняются узлы N1–N5 спеки `docs/tasks/specs/t-1576-s5-parallel-windows.md` **ровно по её §9a** (решения владельца 29.10.2026: F1 (б) замок стенда — как сейчас, только при `run.parallel: false`; F7 (а) все окна плана сразу, без потолка; F8 (б) несколько стендов — отдельный узел «стенд окна» после N2; остальные — по рекомендации) — пересказа здесь нет, носитель один (критик t-1774 §3b: прежний пересказ повторял отклонённый F1 (а)). Что X5-7 добавляет сверх t-1576: (i) две строки переписи §2.3 с классом — край E5 t-1576 (красный только при параллели → `environment`/`tooling`: дискриминирующий перепрогон, класс `meaning-proxy`, `ref` на E5) и F5 (а) («S5 закрывает код после проверки свежести»: `xref`), иначе первый коммит N2 поднимет счёт без слова; (ii) `guard_pre_tool.py` общий с N2 t-1576 (охранник пробы, F4 (а)) и X5-5 (форма → WARN): строка `очередь: N2 → X5-5`, и отказ охранника пробы — класс `safety`, в WARN не уходит; **X5-8 параллельный прогон ручных кейсов S6** (слово владельца 03.11.2026; SC2-38 п. 3 и SC2-44; образец — STLC Stage 9, находка `plans/piles/driver-hosts/findings/20261030-chuzhie-fabriki-stlc-i-tcc-rychagi-skorosti-dlya-0-11-0.md`, носители — НАШИ): один `qa-runner` на ручной кейс (или на группу кейсов одного состояния стенда — размер окна по SC2-44), диспатчи параллельно; улики каждого окна пишет `manual_capture.py http|ui|app --case <C> --attempt aN` в `work/evidence/manual/<case>/<attempt>/` (`captures.jsonl`, `steps.jsonl`, `probes.jsonl`), запись кейса собирает `manual_evidence.py build`, находки по ходу — `exploratory_findings.py` (P26); итог S6 код собирает из этих записей (носитель вердикта ручного кейса называет узел после чтения `proof_level.py`/`manual_evidence.py` — критик t-1774 §3c: не проверено); замок стенда — выживший носитель `scripts/stand_lease.py` (его берёт N2 t-1576; аренды `execution_scheduler.py` — второй носитель, сходятся в N2), `manual_capture` подключается к нему; край: при F1 (б) без `run.parallel: false` ручные окна на одном стенде идут без замка, а сидирование состояния (SC2-38) на общем стенде это ломает → ручное окно, которое сидирует состояние, берёт аренду всегда, независимо от `run.parallel` (инвариант: два окна не переписывают одно состояние стенда); чартер исследования X3 — одно из таких окон. Граница P27/AR-29 в обоих узлах: расписание, замок, слияние и сборка — код (данные); что проверять в окне и что увидено — роль; приёмка окна — критик стадии (F-2), по смыслу | `breach` → 0 по всему пакету; X5-7/X5-8: время S5 и S6 на CART-1 против плеча A (одна метрика, п. 6b), манифест после слияния окон проходит `scripts/tests/test_case_key_identity_join.py` (файл приходит с `release-next` / `local/p1-closeout`, на `main` его ещё нет — критик t-1774 Q-3) | те же детекторы + `test_validators.py`, `test_guard_*` по затронутым функциям; X5-7 — ключи приёмки §9a спеки t-1576; X5-8 — тест сборки итога S6 из записей двух окон `work/evidence/manual/<case>/<attempt>/` (`manual_evidence.py build`) под одной арендой `stand_lease.py` |
| X6 дирижёр → драйвер как Lead | X6-1 `skills/qa-story/phases/s*.md` (3 021 строка) → карта драйвера; скрипты переходов — в коде `story_run.Driver`; маршрут критика S2–S4 из X2-7 переносится в карту драйвера, не пишется заново (`очередь: X2-7 → X6-1`); X6-2 `SKILL.md` («You own the process…») → хартия драйвера: маршрутизирует, принимает, эскалирует | на стадию дирижёру названо ≤ 3 скрипта (было 9–26) | счёт скриптов в фазах (grep); прогон драйвера на фикстуре стори |
| X7 закрытие | X7-1 опустить потолки переписи, `MEANING_CEILING` (до 0) и `process_ratchet_tokens` до факта; X7-2 S9 хартия; X7-3 `design/factory-rules-debt.md` строки закрыты | | K3, K10 на ветке |

#### Узлы X2, которые правит фикс-раунд t-1775 (owns и поведение)

Пути — от `ai-packages/qa-factory/` ветки эксперимента; абсолютные пути даёт диспатч узла от корня worktree.

**X2-2 — советы стадии (критик B-3).**
owns: `references/stages.json` (ключ `advice` стадий S2, S3, S4); `scripts/exit_gate.py` (функции `advice_detectors`, `detector_errors`,
`run_advisers`, `_advice_signal`); `scripts/detector_verdict.py` (признак совета в записи — если его нет; узел читает модуль); новый
`scripts/tests/test_exit_gate_advice.py`.
Поведение:
- `advice` в `stages.json` становится картой «роль → скрипты» той же формы, что `detectors` (`{"qa-requirements-tester": ["sizing.py"]}`);
  нынешний список S2 `["sizing.py"]` переписывается в эту форму тем же коммитом;
- `advice_detectors(agent, stage)` возвращает советчиков ТОЛЬКО этой стадии и роли (сегодня — множество по всем стадиям, `exit_gate.py:84-90`);
  `detector_errors`/`run_advisers` передают стадию, которую держит вызывающий (`_HELD_STAGE`, `:413`, или стадия роли из `stages.json`).
  Инвариант: скрипт, объявленный советчиком на S2, остаётся блокирующим детектором на S3–S5, где он стоит в `detectors` (`branch_accounting.py`
  стоит в S2–S5 — критик B-3 п. 1);
- гранулярность — запись детектора, не скрипт: детектор (например `branch_accounting.py`) помечает каждую свою запись `detector_verdict`
  признаком совета; `exit_gate` блокирует только на записях без признака, записи с признаком — советы. Так связка «у единицы текста есть дом»
  (`xref`) остаётся блокирующей, а суждение о доме — советом (критик B-3 п. 2; AR-18 — одна форма вывода);
- носитель для приёмщика: советы пишутся в `<T>/work/advice-<stage>.json` (один писатель — `exit_gate`, AR-14), список записей
  `detector_verdict` с именем скрипта; бриф критика стадии получает этот путь в `given` (§3.4); файла нет — `given` называет его с `—` и причиной
  (AR-23);
- человеку (`person_signal … gate_unreadable`) уходит только советчик, который НЕ запустился (таймаут, не стартовал, вывод не читается) —
  как сейчас для «unreadable»; содержательный вывод советчика человеку не уходит.
Тест: `test_exit_gate_advice.py` — (1) советчик S2 не блокирует S2 и блокирует S3, где стоит в `detectors`; (2) запись с признаком совета не
блокирует, без признака — блокирует; (3) советы попадают в `work/advice-<stage>.json`; (4) упавший советчик даёт один сигнал человеку, а
отработавший — ни одного.

**X2-3 / Q-2 — `judge.py`.** Узел читает вызывающих `judge.judged_refusal` (`judge.py:357`; `import judge` или имя `judge.py` — в 21 файле
пакета вне `tests/`, в том числе `s5_precheck.py`, `handoff_check.py`, `judge_form.py`, `brief_pack.py`) и решает по каждому вызову: советчик
(вывод — запись совета X2-2, класс `meaning`, вычисленный `blocks: false`) или судья на пути отказа (класс `meaning`, breach — снимается в X2
или X5 по стадии). Итог — строки переписи и `MEANING_CEILING` (F-10).

**X2-5 — запись приёмки стадии (критик F-4).**
owns: `scripts/acceptance.py` (новая функция чтения/проверки формы записи стадии рядом с записью окна — имя выбирает узел, например
`stage_acceptance`); `scripts/stage_done.py` (запись `acceptance` в `pipeline.json` — единственный писатель); тест в существующем тестовом
файле `acceptance.py` (узел находит его `git grep -l "import acceptance" -- ai-packages/qa-factory/scripts/tests`).
Поведение: запись `{stage, role, acceptor, verdict: accept|reject, failure_class, quote, witness_paths}`; читатели (`controller.py` при переходе
стадии, отчёт) читают её только через `acceptance.py` (AR-13); код проверяет присутствие и форму (класс `shape`), не смысл. Почему не новый
модуль: `acceptance.py` уже — «semantic acceptance», запись окна S5 — частный случай записи стадии; второй модуль с тем же фактом — второй
читатель (критик §6).

**X2-7 — маршрут критика стадии S2–S4 (критик B-4, рекомендация (а)).**
owns: `skills/qa-story/phases/s2.md`, `skills/qa-story/phases/s3.md`, `skills/qa-story/phases/s4.md`; `scripts/story_run.py` — только функции
класса `Driver`: `s4_repair_owed` (обобщается на S2–S4) и новая функция маршрута критика стадии (имя — узел); `scripts/controller.py` — только
константа `REPAIR_LOOP_ROLES` (`controller.py:202`: сегодня `qa-automator`, `qa-code-critic`, `qa-case-designer`, `qa-case-critic`; добавляются
`qa-requirements-tester`, `qa-test-strategist`). Горячие файлы: по D-0048 — непересекающиеся списки функций в owns; строка `очередь: X2-7 → X6-1`.
Поведение: после остановки роли S2/S3 драйвер диспатчит критика стадии (`qa-case-critic`, перехартированный X2-1) с брифом §3.4 (в `given` —
артефакт, таблица `tried`, файл советов X2-2); вердикт пишет запись X2-5; `reject` → повтор роли в свежем контексте; число раундов — только
`repair_budget` контроллера (§3.5); `budget_or_none` вернул `None` — окно закрывается без раунда, как сегодня (`story_run.py:9220-9241`).
На S4 существующий цикл (`s4_repair_owed`) сохраняет поведение. Сегодня критик в фазах упомянут только в `s4.md`, `s5.md`, `s7.md` (grep
`qa-case-critic|qa-code-critic` по `phases/`; положительный контроль — та же выборка нашла `s4.md`): S2/S3 маршрута нет.
Тест: прогон драйвера на фикстуре стори — после S2 в журнале диспатч критика стадии и запись приёмки; `reject` → второй диспатч роли с
`attempt` 2; исчерпанный потолок → эскалация к драйверу. Ключ K14.

## 5. Развилки (возвращены; F-1…F-11 решены владельцем: F-1…F-9 — 03.11.2026 «согласна со всеми развилками», F-10 и F-11 — 03.11.2026 «Принять», по рекомендации; тем же словом запущена пачка A)

**Слово владельца 03.11.2026: «согласна со всеми развилками» — F-1…F-9 приняты по рекомендации дизайнера** (столбец «рекомендация»
ниже). Тем же словом: в переделку поздних стадий (X5) входят параллельность написания автотестов (S5) и параллельный прогон ручных
кейсов агентом (S6) — узлы X5-7 и X5-8 §4; это та работа, что планировалась в релиз 0.11.0 (CD1-24, SC5-3, SC2-38): ветка эксперимента
несёт её, релиз 0.11.0 собирается из ветки после слова владельца по X4.

| id | вопрос | варианты | рекомендация |
|---|---|---|---|
| F-1 | цель нагрузки роли | (a) ≤ 5 000 ток. факторного текста; (b) ≤ 6 000 (≈ ⅓ сегодняшних 13–18K, как в анализе §4); (c) ≤ 8 000 | (b): ⅓ — цифра анализа; файлы проекта считаются отдельно (они знание проекта, P2); `target_tokens` — информационная строка до подтверждения владельцем, как `threshold_confirmed_by` |
| F-2 | критик стадии — новая роль или перехартирование | (a) новая `qa-stage-critic`; (b) `qa-case-critic` → критик S2–S4, `qa-code-critic` → S5, драйвер — S6–S8 | (b): регистрация новой роли трогает ≈ 44 файла (предложение qa-explore, развилка 4); у обоих критиков уже есть рубрики и права |
| F-3 | закрытые словари | (a) свободный текст + критик; (b) предложенный список, который роль может расширить строкой `new: <слово> -- <почему>` (дверь как P13), критик судит расширение; (c) оставить закрытыми | (b) для `defect_class`, `fit`, `confirmation`, вердикта S2; для `then_oracles` — (b) с неснимаемым запретом `code` (P20, FR-58); классы триажа S7 — (c): это маршрут «кто действует» (FR-19), не суждение о качестве |
| F-4 | объём эксперимента | (a) S1–S4 только (без стенда: эталонные баги не находятся, меряется «кейсы нацелены на Б-n»); (b) вся стори S0–S8; (c) S1–S4 + исследовательский диспатч S6 | (c): S1–S4 дешёво меряют требования и вопросы, S6-чартер — единственное место, где Б-1/Б-2/Б-4 вообще находятся; S5/S7/S8 плеча B работают по-старому |
| F-5 | отказы `guard_pre_tool` по содержанию | (a) удалить целиком; (b) WARN-строки (FR-4: проверка останавливает тихий проход, не осведомлённый) | (b): WARN считает `friction.py`, роль видит предупреждение и решает; после X4 — удалить то, что WARN ни разу не предупредил по делу |
| F-6 | какой релиз несёт часть A | (a) форджевые части (A1, A5) — на `main` сразу, пакетные (A2–A4) — первым патчем после слияния `release-next`, до среза ветки; (b) всё вместе с ветвью эксперимента | (a): ветка наследует перепись и храповик и сжимает их; гейт `judgment:` начинает считать ещё до эксперимента (база для проверки 41). Номер патча — Lead (на main в работе 0.10.9, `docs/tasks/p1-closeout-0-10-9.md`) |
| F-7 | где живёт перепись | (a) новый файл `fixtures/judgment-census.json` целиком; (b) поле `class` в существующих реестрах (A24 `REGISTRY`, A26 `gate-registry.json`, `stage-joints.json`) + новый файл только для непокрытых единиц; (c) (a) со ссылкой `ref` на id существующих реестров, без повтора их описаний | (c): один файл, который видит все единицы (класс — его единственный факт), реестры остаются владельцами своих фактов; (b) разносит один счёт по трём форматам и трём читателям |
| F-8 | класс `safety` | (a) есть, вне храповика; (b) есть, его счёт тоже только вниз или с названным подъёмом; (c) нет — защитные единицы `shape` | (b): без храповика `safety` становится лазейкой («всё назовём защитой»); список защищаемых объектов (приложение, секрет, внешняя запись, слова человека, git-состояние) — данные переписи |
| F-9 | контрольное плечо | (a) новый прогон `main` на срезе; (b) записанный LOCAL-1 (0.10.8) | (a): другая версия — другая метрика (п. 6b); цена — один прогон |
| F-10 | **(новая, t-1775)** противоречие требований: скан всех `scripts/*.py` (B-1) делает видимым LLM-судью `judge.judged_refusal`, а C4 держал `meaning` = 0 жёсткой константой | (a) C4 = 0 константой, LLM-судьи размечаются `word-list` (как `judge_words`); (b) `MEANING_CEILING` — константа теста = счёт `meaning` первой переписи, только опускается, X7-1 доводит до 0; (c) C4 снять, `meaning` — обычный потолок данных | (b): (a) прячет суждение модели под меньший класс — ровно переразметка, которую ловит вопрос 11; (c) отдаёт потолок правке данных; (b) честно считает сегодняшнее и не даёт поднять правкой данных |
| F-11 | **(новая, t-1775)** как вычисляется `blocks` у единиц, которые отказывают не вызовом `deny`/`block`/`raise`, а списком ошибок, который вызывающий превращает в отказ (`validate_artifacts`, `exit_gate`, `judge_form`) — `refusal_registry.sites()` таких не видит | (a) только `sites()` + ручная метка `blocks: true` для валидаторов; (b) `sites()` ИЛИ объявленный путь отказа (`stages.json` `detectors` минус `advice` стадии и роли; константа теста `BLOCKING_ENTRY_FILES`, только растёт), ручная метка — только исключение `blocks_override: false` с `note` под потолком; (c) обход графа вызовов от точек входа хуков | (b): ошибается в сторону лишнего `blocks: true` (безопасно), дешёв, не заводит четвёртого AST-обхода; (a) возвращает ручную метку, через которую новый отказ проходит тихо (критик B-1 п. 4); (c) — новый сканер и хрупкость на динамических вызовах |

## 6. Края (поведение и инвариант, который оно защищает)

| id | край | поведение | инвариант |
|---|---|---|---|
| E-B1 | роль вернула «багов нет, спросить нечего» | приёмщик требует таблицу `tried` (требование × техника × наблюдение × улика) и хотя бы одну попытку опровержения на каждое требование с риском выше низкого; без неё — `reject` (`capability`), повтор, эскалация | «пусто — не чисто» (манифест п. 10): пустой список находок без следа проверки никогда не читается как чистый исход |
| E-B2 | у задачи нет текста требований (P23) | требования выводятся из диффа/кода как утверждения (P20), каждое — вопрос «было/стало» одной пачкой на гейте A; без ответа — пробел в отчёте; утверждение не становится оракулом | код — не оракул (FR-58); требования, не AC, — единица (AR-26) |
| E-B3 | хартия и знание онбординга проекта расходятся | факт проекта (как здесь пишут тесты, где данные, какой уровень принят) — побеждает в КАК; опасение ремесла (например, проект не делает негативных e2e) — находка/вопрос, не молчаливое следование и не молчаливое нарушение | факты проекта — в конфиге (AR-3, P2); замысел — у человека; хартия не отменяет записанного решения человека |
| E-B4 | открытие словарей и снятие отказов задевает P20 | семья `oracle` в `s5_precheck` и запрет `code` в `then_oracles` остаются блокирующими: это связка данных (поле `open` + литерал в assert), не суждение | ожидание из реализации никогда не проходит молча |
| E-B5 | ×5 регрессия цены | потолок на диспатч = 2 × цена стадии в A (тот же носитель); на потолке останавливает драйвер, не хук; M4/M6 по стадиям ловят блуждание | цена одна и истинная (P18); роль не тратит неограниченно без решения приёмщика |
| E-B6 | человек спит | вопросов с остановкой нет; роль идёт по рекомендации, помечая «до ответа»; гейты A/B ждут (это решения человека); драйвер доводит до гейта и пишет утренний список | ни одно решение замысла не принимается за человека; работа не стоит на вопросе, который мог решить драйвер |
| E-B7 | вопрос роли, на который ответ есть на диске | драйвер закрывает его сам с `answered_by: driver` и источником; человеку не уходит | P22: сначала разбирается сам; проверка 38 считает класс |
| E-B8 | исследовательский чартер без шагов `type`/`fail_request` на ветке | чартер исполняется существующим `manual_capture ui`, если умеет; не умеет — строка разрыва в отчёте, Б-n не засчитан | правило проекта не вписывается в хартию (P2); «не нашёл» не равно «нет бага» |
| E-B9 | приёмщик той же модели, что исполнитель | «выше» — по функции и независимому контексту (как дизайнер в форджа), модель по P7/FR-52 | правка, держащаяся только на сильной модели, — не правка |
| E-B10 | X2-7: потолок раундов ремонта на S2/S3 — два кандидата («один повтор» §3.5 прежней редакции и `repair_budget` контроллера) | выживает `repair_budget` контроллера (сегодня 2 раунда, `runtime_policy.py:13`); `budget_or_none` → `None` — окно закрывается без раунда и `defect_found` (как сейчас); исчерпан — эскалация к драйверу | один счётчик раундов на фабрику (AR-13); драйвер не держит своего счёта (B-007) |
| E-B11 | X2-5: запись приёмки стадии отсутствует на переходе | переход стадии отказывает с дверью «диспатчите критика стадии» (класс `shape` — присутствие); запись есть — смысл код не судит | приёмка по смыслу не пропускается молча (AR-28) и не судится кодом (AR-29) |
| E-A1 | индекс AR после AR-29 > 3 КБ | `python tools/architecture_index.py` и проверка длины файла; > 3072 Б — развилка Lead: сократить заголовки или слить AR-29 с AR-7 вторым предложением (протокол карты п. 10) | индекс остаётся ≤ 3 КБ (грузится в каждую сессию) |
| E-A2 | перепись: новая проверка без строки; строка без функции; класс понижен; единица с двумя классами | C1 отказ с дверью «добавьте строку»; устаревшая строка — отказ «удалите/перенесите», не тихое сжатие; понижение класса и новое `blocks_override` — не видно как подъём тесту, видно вопросу 11 и проверке 41 (d); `blocks_overrides` — потолок; две роли — берётся высший по порядку `meaning > meaning-proxy > word-list > xref > shape` | храповик видит рост; ошибка переписи — в сторону лишней строки, лишнего `blocks: true` и высшего класса |
| E-A3 | временной край: t-1702 D3 (ось 31, проверки 39/40) не слит, когда сливается часть A (подтверждено критиком t-1774 §0: `527c560f` не предок `origin/main`) | номер оси и проверки — следующий свободный в файле на момент коммита (41 и 32 свободны в обоих мирах); тексты ссылаются на заголовок, не только на номер; до слияния A5 гейт `judgment:` не существует и ничего не требует, после — требует с первого пакетного коммита | ни одна строка не ссылается на номер, которого нет в файле |
| E-A4 | гейт `judgment:` (сводка) | нет пакетного пути — молчит; нет строки — отказ с четырьмя формами; строка в ограде/цитате — не считается; merge — освобождён; миры переписи — E-A7…E-A11; позиция — E-A12 | ложная `none` на подъёме переписи невозможна; неизвестное не становится проходом (AR-28) |
| E-A5 | разметка `kind: craft` | неразмеченное = процесс; маркер на процедуре виден только критику (вопрос 11) и выборке 41 (d) | процесс не уходит из храповика молча |
| E-A6 | противоречие требований: «код не отказывает по содержанию» и `exit_gate` «один возврат» | один возврат остаётся для отсутствующего артефакта/ключа/свидетеля (класс `shape`); по содержанию — не возвращает | гейт не пропускает отсутствие (AR-28) и не судит смысл (AR-29) |
| E-A7 | ВРЕМЕННОЙ, мир (i): переписи нет ни в HEAD, ни в индексе (весь `main` между A5 и A3 по F-6 (а); любая ветка без A3) | перекрёстная проверка молчит; строка `judgment:` требуется по форме | гейт не требует файла, который ещё ничто не произвело (FR-5), и не выдумывает подъём из отсутствия |
| E-A8 | ВРЕМЕННОЙ, мир (ii): переписи нет в HEAD, есть в индексе (коммит A3); или блоб HEAD не читается как JSON | создание — не подъём; потолки первой переписи — факт; `judgment: none -- census created` проходит; при нечитаемом HEAD — плюс WARN «сравнение с пустой» | первая перепись не заставляет писать ложную `moves … to code`; починка битой переписи не заперта |
| E-A9 | мир (iii): перепись есть в HEAD, удалена в индексе | `none` и `adds data check` отклоняются с текстом «перепись удалена этим коммитом»; проходит только `judgment: moves <что> to code -- <почему>` | снятие стража никогда не проходит молча; дверь есть всегда (FR-2) |
| E-A10 | мир (iv) и (v): перепись есть в обоих; равна / различается | равна — молчит; подъём `word-list|meaning-proxy|meaning|breach|blocks_overrides` — нужна `moves … to code`; подъём только `blocking_per_role.*`/`safety` — `adds data check` или `moves … to code`; новый ключ с 0 и исчезнувший ключ — не подъём | рост суждения в коде не проходит под `none`; честная проверка данных не заставляет строку лгать (критик F-1) |
| E-A11 | мир (v'): блоб переписи в индексе не JSON, без объекта `ratchet` или потолок не целое ≥ 0 | отказ с путём файла, независимо от строки `judgment:` | неизвестное не становится проходом (AR-28) |
| E-A12 | ПОЗИЦИОННЫЙ: место проверки `judgment:` в `decide()` | нет пакетного пути → `0` до любого чтения; merge-освобождение в `main()` до чтения сообщения — общее; проблемы `architecture:` и `judgment:` собираются независимо и называются одним отказом; `decide()` чистая — блобы HEAD/индекса передаются аргументами | отсутствие индекса AR не снимает проверку `judgment:`, битая перепись не снимает отказ `architecture:`; всё, что отказывалось до A5, отказывается после |
| E-A13 | ВРЕМЕННОЙ: A1 (тексты, проверка 41) на `main` раньше A3/A4 | проверка 41 (a) пишет «census not on main», (b) — «craft split not on main» — не находка и не ноль; K9 ищет имена файлов в текстах, не сами файлы | неизвестное не записывается нулём (FR-41); детектор не краснеет на мире, который спека сама создала |
| E-A14 | `refusal_registry.sites()` в новой роли (вход храповика) и вычисление `blocks` | ошибка в сторону лишнего `blocks: true`; обёртка `_deny`, импорт `deny as refuse`, отказ списком ошибок — закрываются путём (b2), вне пути — красный C5 «не виден»; вложенная функция — единица внешней; уровень модуля — `<module>`; `sites()` без `files` ведёт себя как сегодня (A24) | отказ по содержанию роли никогда не считается неблокирующим без названного исключения; реестр A24 не меняет поведения |
| E-A15 | X2-2: советы по стадии | скрипт-советчик S2 остаётся блокирующим детектором S3–S5; запись с признаком совета не блокирует; советы — в `work/advice-<stage>.json` для приёмщика; человеку — только неотработавший советчик; файла советов нет — `given` брифа критика называет его с `—` и причиной | совет никогда не блокирует и не приходит человеку под видом «не прочитан»; блокирующая часть на других стадиях не меняется; у поля советов есть читатель (AR-22) |
| E-A16 | плотность `blocking_per_role` | у каждой роли из `agents/*.md` и у `conductor` — ключ; нет единиц — `0`; ключа нет — красный «добавьте строку 0»; ключ несуществующей роли — красный «устаревшая» | новая или переименованная роль не выпадает из храповика молча |
| E-A17 | двойной счёт: строка `stages.json` и функции того же скрипта, запись A24 и та же функция | строка скрипта — единица только без функций-единиц; иначе `ref` на функциях; счёт по парам (`file`, `function`) | одно действие — один счёт в `blocking_per_role` и `breach` |
| E-A18 | `meaning` (F-10) | `MEANING_CEILING` = счёт первой переписи, только опускается правкой теста; слепое пятно (переразметка `meaning` в меньший класс) печатается тестом | честный подъём суждения модели невозможен без правки теста, которую видит критик |

## 7. Ключи приёмки для Lead (K1…K14)

Дословные команды; «→» — ожидаемый вывод. Док-ключи исполняются скриптом с отрицательным контролем (правило 11 DOC-DISPATCH WITNESS).

- K1 `git grep -n -F "**P27.**" -- PROJECT.md` → одна строка.
- K2 `git grep -n -F "**AR-29 — " -- ai-packages/qa-factory/design/architecture.md` → одна строка; `python tools/architecture_index.py --check` →
  exit 0; `git grep -c "^- AR-" -- docs/ARCHITECTURE_INDEX.md` → `docs/ARCHITECTURE_INDEX.md:29`; длина индекса ≤ 3072 Б (E-A1);
  `git grep -c "none — discipline" -- ai-packages/qa-factory/design/architecture.md` → на 2 меньше, чем до A2 (поля Detector AR-2, AR-7).
- K3 `python -B -m pytest ai-packages/qa-factory/scripts/tests/test_judgment_census.py -q` → passed, включая C5 (отрицательные контроли:
  нейтральное имя файла, вызов судьи, обёртка `_deny`, `blocks_override` без `note`, поднятый `safety`, роль без ключа);
  `git grep -n -F "refusal_registry" -- ai-packages/qa-factory/scripts/tests/test_judgment_census.py` → ≥ 1 строка (импорт `sites`, не свой
  сканер отказов); `git grep -n "scan_globs" -- ai-packages/qa-factory/scripts/tests/fixtures/judgment-census.json` → пусто (положительный
  контроль той же формы: `git grep -n "ratchet" -- ai-packages/qa-factory/scripts/tests/fixtures/judgment-census.json` → ≥ 1).
- K4 `python -m pytest tools/test_architecture_gate_next.py -q` (до переноса Lead), затем `python -m pytest tools/test_architecture_gate.py -q`
  (после) → passed; среди тестов: нет строки → отказ; `judgment: none -- x` → проход; `judgment: moves A to role -- y` → проход;
  `judgment: moves A -- y` → отказ; `judgment: adds data check u -- z` → проход; мир (i) → молчит; мир (ii) + `none` → проход; мир (iii) +
  `none` → отказ, + `moves A to code -- y` → проход; подъём `word-list` + `none` → отказ, + `adds data check` → отказ; подъём только
  `safety` + `none` → отказ, + `adds data check` → проход; битый блоб индекса → отказ с путём; нет индекса AR и нет строки `judgment:` →
  один отказ, называющий обе проблемы; merge → освобождён.
- K5 `git grep -n -F "11. **JUDGMENT**" -- docs/tasks/critic-diff-brief.md` → одна строка.
- K6 `git grep -n -F "the owner it serves" -- .claude/agents/designer.md` → одна строка; `git grep -n "^10\. " -- CLAUDE.md` в блоке host
  adaptations → строка с «P27».
- K7 `git grep -n -F "**Where judgment lives (P27, AR-29).**" -- PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md` → одна строка.
- K8 `git grep -n -F "— Where judgment lives:" -- docs/SIBLING_MAP.md` → одна строка заголовка оси.
- K9 строка оси 18 в `docs/SIBLING_MAP.md` и вопрос 9 брифа называют `judgment-census.json` и `process_ratchet_tokens`:
  `git grep -c -e judgment-census -e process_ratchet_tokens -- docs/SIBLING_MAP.md docs/tasks/critic-diff-brief.md` → ≥ 2 в каждом.
- K10 `python -B ai-packages/qa-factory/scripts/role_load.py --all --json` печатает `craft_tokens` и `process_tokens` на каждую из 12 ролей;
  `git grep -n process_ratchet_tokens -- ai-packages/qa-factory/references/role-load.json` → одна строка.
- K11 (ветка, после X2) перепись: `breach` на ролях S2–S4 = 0 (строка итогов теста K3).
- K12 (ветка, после X4) `experiments/mybooks/thinking-roles/compare.md` содержит строки M1…M8, у каждой — носитель числа.
- K13 (ветка, после X2-2) `python -B -m pytest ai-packages/qa-factory/scripts/tests/test_exit_gate_advice.py -q` → passed (четыре случая X2-2);
  `git grep -n -F "unreadable (advice)" -- ai-packages/qa-factory/scripts/exit_gate.py` → только в ветке «советчик не запустился».
- K14 (ветка, после X2-7) `git grep -c -e qa-case-critic -- ai-packages/qa-factory/skills/qa-story/phases/s2.md ai-packages/qa-factory/skills/qa-story/phases/s3.md`
  → ≥ 1 в каждом; `git grep -n -e qa-requirements-tester -e qa-test-strategist -- ai-packages/qa-factory/scripts/controller.py` → строка
  `REPAIR_LOOP_ROLES`.

## 8. Решения дизайнера без веса замысла (закрыты, Lead может отменить)

- S-1 P27 — принцип над FR-47/AR-7, нового FR не вводится (FR-47 уже говорит то же; не хватало детектора, не правила).
- S-2 Гейт `judgment:` — второй вид строки в `tools/architecture_gate.py`, не новый файл: логика отбора строк одна (вопрос 6 брифа критика).
- S-3 Перепись лежит в `scripts/tests/fixtures/` (как `env-facts-baseline.json`, `driver-layers.json` — члены оси 18): её не читает ни один проект
  в рантайме (FR-44).
- S-4 Форма хартии — шесть секций §3.3; файл-шаблон или раздел в `design/` — решает узел X1-1 по FR-44 (кто его читает).
- S-5 Носитель шаблона брифа — данные (`references/` или `handoffs/index.yaml`), рендер — `brief_pack.py`; выбор между двумя — узел X1-6.
- S-6 Пороги эксперимента (2 × цена, ≥ 2 из 3, ≤ 1,5 × цена) — рекомендации, помечены как таковые в §3.6.
- S-7 (t-1775) `refusal_registry.sites()` получает необязательный аргумент `files` (по умолчанию `SCANNED`), а не копию функции в тесте
  переписи: один сканер мест отказа (AR-15, критик §6); поведение A24 без аргумента не меняется (E-A14).
- S-8 (t-1775) Потолок раундов ремонта на S2–S4 — `repair_budget` контроллера, а не отдельное «один повтор» §3.5 прежней редакции: факт
  с функцией-читателем читается только через неё (AR-13); драйвер своего счётчика не держит (`story_run.py:9211-9212`, B-007).
- S-9 (t-1775) Запись приёмки стадии — расширение `scripts/acceptance.py`, не новый модуль; писатель `pipeline.json` — `stage_done.py` (критик F-4).
- S-10 (t-1775) Носитель советов стадии — `<T>/work/advice-<stage>.json`, писатель `exit_gate` (AR-14); имя — по образцу `work/sizing.json`.
- S-11 (t-1775) A5 сдаётся соседним именем `tools/architecture_gate_next.py` (правило 2 CLAUDE.md о самоактивирующихся файлах; критик F-9).

**Нужно сверх манифеста:** `design/architecture.md:254-265` (протокол, предел индекса 3 КБ); `docs/tasks/specs/t-1702-d6-forge-ci.md` (ось 31 и
проверки 39/40 ещё не на main); `tools/agent_budget.py`, `scripts/turn_budget.py` (образец потолка); `scripts/refusal_registry.py`,
`references/stage-joints.json` (кандидаты на `ref` переписи); `experiments/mybooks/cart-1-run-problems.md`. Фикс-раунд t-1775 сверх
манифеста: `scripts/controller.py:202, 1840-1869` (`REPAIR_LOOP_ROLES`, `repair_budget`), `scripts/runtime_policy.py:13` (потолок раундов),
`scripts/readiness.py` (список `def`), `scripts/judge.py`, `scripts/judge_form.py` (список `def`), grep импортёров `judge`.

**Противоречия в брифе:** (1) бриф называет «axis 31 role carriers» как существующую — на main 30 осей, ось 31 вносит t-1702 D3 (не слита);
новая ось — 32 или следующая свободная. (2) «checks 36–40» — на main последняя 38; 39 и 40 — t-1702. (3) «первая хартия = qa-explore» и
«та же стори CART-1»: скилла qa-explore нет (16–19 цепочек), отсюда рекомендация F-4 (c) — чартер в диспатче `qa-runner`. Противоречия
(1) и (2) подтверждены критиком t-1774 §0 (`git merge-base --is-ancestor 527c560f origin/main` → exit 1) и диспатчем t-1775; утверждение
диспатча t-1774 «ось 31 на main» было неверным — правка журнала/диспатча за Lead (§10 F-13).

## 9. След (прочитано)

- `docs/tasks/specs/reports/20261103-pochemu-roli-ne-dumayut.md` целиком; `docs/tasks/handoffs/t-1760-…`, `t-1761-…`, `t-1762-…` целиком.
- `ai-packages/qa-factory/design/architecture.md:1-60, 85-134, 180-266`; заголовки AR-1…AR-28 (grep `^\*\*AR-`).
- `docs/SIBLING_MAP.md:1-40, 380-482`; grep `^## Axis` (последняя — 30; положительный контроль — та же выборка нашла 1…30); grep `Axis 31`
  по `*.md` → только `t-1702`, ревью `t-1708`, `t-1755`.
- `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md:1037-1066` (проверки 35–38; grep номеров — последняя 38); `t-1702-d6-forge-ci.md:100,103,286-297`.
- `docs/tasks/critic-diff-brief.md` заголовки вопросов 1–10, `:44-63`.
- `tools/architecture_gate.py:1-90`; `tools/agent_budget.py:1-25`.
- пакет: `scripts/gate_registry.py:1-80`; `scripts/refusal_registry.py:1-70`; `references/gate-registry.json` (поля строк, grep);
  `references/role-load.json` целиком; `references/stage-joints.json` (grep ключей); `references/stages.json:60-119` + grep ключей;
  `references/inject-map.json:1-40`; `references/tester-manifesto.md` целиком; `scripts/exit_gate.py:1-80` + список `def`;
  `scripts/stage_guard.py:860-889` + список `rule_*/check_*`; `scripts/guard_pre_tool.py` список `*_check`; `scripts/validate_artifacts.py`
  список `check_*`; `scripts/s5_precheck.py:1-40, 3386-3440` + список `def`; `scripts/branch_accounting.py:1-40`;
  `scripts/handoff_check.py:1-50`; `scripts/turn_budget.py:1-30` (grep `TURN BUDGET` → 4 файла); `agents/qa-case-designer.md:1-70`;
  `agents/qa-runner.md:1-8`; `skills/qa-story/SKILL.md:1-60`; `design/factory-rules.md` FR-12, FR-47, FR-55 (grep с `-A 4`; первая попытка
  по `^### FR-` пуста — неверная форма заголовка, повтор по `FR-47 —` нашёл).
- `plans/exploratory-charters-proposal.md` целиком; `plans/piles/release-next/findings/20261031-qa-explore-dolzhen-nayti-bagi-korziny-mybooks.md`
  целиком; `experiments/mybooks/cart-1-run-problems.md:1-50`; `.claude/agents/builder.md:1-45`.
- Не прочитано (узлы читают сами): тела функций `guard_pre_tool` (классификация защита/форма — по имени), `critic_rollcall.py`,
  `planning_contract.py`, `sizing.py`, `story_run.Driver`, `brief_pack.py`, `question_register.py`, `role_load.py`; `common-rules.md`;
  `phases/s*.md`; `.claude/agents/critic.md`. Размер `docs/ARCHITECTURE_INDEX.md` не измерен (нет оболочки) — край E-A1 (измерен критиком t-1774:
  2550 Б).
- **Фикс-раунд t-1775 (прочитано):** `docs/tasks/specs/reviews/t-1774-critic-plan-thinking-roles.md` целиком; `tools/architecture_gate.py:1-194`
  (`LINE_RE` `:55`, `_prose_matches` `:73-91`, `decide()` `:130-152`, merge-освобождение `:171-176`, чтение индекса `:182-185`);
  `scripts/refusal_registry.py:56-59` (`SCANNED` = `stage_guard.py`, `inject_context.py`, `guard_pre_tool.py`; `REFUSAL_CALLS` = `deny`,
  `block`; `REFUSAL_RAISES` = `StateConflict`, `ValueError`), `:770-839` (`_refusal_calls`, `sites()` — сканирует только `SCANNED`, отсюда
  аргумент `files`, S-7); `scripts/exit_gate.py:78-97` (`advice_detectors`), `:371-376` (`detector_gates`), `:398-413` (`_advice_signal`),
  `:490-524` (`detector_errors`, `run_advisers`); `references/stages.json` grep `"advice"|"detectors"|"id"` (`advice` только у S2 `:80`;
  `detectors` у S2 `:74`, S3 `:110`, S4 `:142` под `qa-case-critic`, S5 `:175`, S8 `:276`; положительный контроль — та же выборка нашла все
  десять `id`); `scripts/acceptance.py:1-40`; `scripts/story_run.py:248` (`GATE_REPAIR_CAP = 2`), `:9209-9248` (`repair_budget`,
  `budget_or_none`), grep `s4_repair_owed` `:9007`, `repair_limit_gate` `:10170`; `scripts/controller.py:202` (`REPAIR_LOOP_ROLES`),
  `:1840-1869` (пакет `repair_budget`); `scripts/runtime_policy.py:13` (grep: `repair_cycles: 2`, `design_repair_cycles: 2`);
  `scripts/judge.py` список `def` (`judged_refusal` `:357`); `scripts/judge_form.py` список `def` (`digest_errors` `:169`);
  `scripts/readiness.py` список `def` (`check_*` — 15); grep `import judge\b|from judge import|judge\.py` по `scripts/*.py` (39 файлов вместе
  с тестами, 21 — вне `tests/`, из них 13 — семья `judge*.py`); Glob `phases/s[2-4].md` (все три есть); grep `qa-case-critic|qa-code-critic`
  по `phases/` → `s4.md` 4, `s5.md` 5, `s7.md` 1 (S2/S3 — нет; положительный контроль — та же выборка нашла `s4.md`).
- Не прочитано в фикс-раунде: тело `judge.judged_refusal` и его вызывающие (узел X2-3 / A3); `scripts/detector_verdict.py` (есть ли признак
  совета — узел X2-2); тела `proof_level.py`/`manual_evidence.py` (X5-8, критик §3c).

## 10. Фикс-раунд t-1775 по критику t-1774

Итог: сделано 17 (B-1…B-4, F-1…F-12, Q-1), оспорено 0, в очереди 3 (F-13, Q-2, Q-3). F-5 и F-6 сделал Lead до раунда (узлы X5-7/X5-8);
их текст этим раундом не трогался.

| id | что изменено (раздел, одна строка) или «не сделано: почему» |
|---|---|
| B-1 | §2.3 переписан: скан всех `scripts/*.py` кроме `tests/` (константы теста, `scan_globs` удалён), единица u1–u3 (`UNIT_NAME_RE` с `judge`, `JUDGE_CALLS`, места отказа через `refusal_registry.sites()`), явные строки классов для `judge_words`, `judge_form`, `judge.py`, `readiness.py`, `blocks` вычисляется (F-11), C5 с нейтральным именем файла; §2.2 Detector, §4 A3 owns, K3, E-A14 |
| B-2 | §4 порядок по F-6 (а): A5 → A1 на `main`, затем A2 ‖ A3 ‖ A4; §2.4 миры (i)–(v) и нечитаемый блоб, позиция в `decide()` с инвариантами; §6 E-A7…E-A13; K4 |
| B-3 | §4 X2-2 (подробный узел): `advice` по стадии и роли, `advice_detectors(agent, stage)`, признак совета на записи `detector_verdict`, файл `work/advice-<stage>.json` в `given` брифа критика, человеку — только неотработавший советчик; §3.2 сквозная строка `exit_gate`, §3.4, §3.5; E-A15; K13 |
| B-4 | §4 новый узел X2-7 с owns (`phases/s2.md`, `s3.md`, `s4.md`; функции `story_run.Driver`; `controller.REPAIR_LOOP_ROLES`), `очередь: X2-7 → X6-1`; X6 строка; K14 |
| F-1 | §2.4 четвёртая форма `judgment: adds data check <unit> -- …`; рост `blocking_per_role`/`safety` не требует `moves … to code`; §2.5, §2.6 (c), E-A10, K4 |
| F-2 | `safety` в C3 (§2.3), в перекрёстной проверке §2.4 (мир (v)), в K3/K4 и E-A10 |
| F-3 | §3.5: выживает `repair_budget` контроллера (`runtime_policy.py:13`, сегодня 2), «один повтор» снят; §8 S-8; E-B10 |
| F-4 | §3.5 и §4 X2-5: запись приёмки стадии — расширение `scripts/acceptance.py`, писатель `stage_done.py`; §8 S-9; §1 строка AR-13; E-B11 |
| F-5 | сделано Lead до раунда (X5-7: ссылка на §9a t-1576, строки переписи E5/F5); не трогалось |
| F-6 | сделано Lead до раунда (X5-8: `work/evidence/manual/…`, `stand_lease.py`, край F1 (б), `очередь: N2 → X5-5`, охранник пробы = `safety`); остаток для Lead: столбец теста X5-8 всё ещё называет «двух `execution-*.json`» — чужой носитель по критику §3c; не правлено (запрет брифа трогать X5-7/X5-8) |
| F-7 | §4 owns: `design/factory-rules-debt.md` — A3; поля Detector AR-2/AR-7 — A2 (§2.2, K2); `selftest.py` не правится — §2.8 M3 «`--fast`/`package-fast`», не `--contracts` |
| F-8 | §2.7 таблица осей: механизмы M1…M7 названы по имени в строках 1, 2, 3, 5, 6, 9, 10, 16, 17, 18, 31; ось 17 → `queued — X2-2`; ось 10 → covered (два `git show`) |
| F-9 | §2.4 «Живой путь»: A5 сдаётся как `tools/architecture_gate_next.py` + тест, переносит Lead; `_prose_matches(msg, line_re=…)` параметризован; §4 A5, §8 S-11, K4 |
| F-10 | §2.3 C3 и E-A16: `blocking_per_role` плотный по `agents/*.md` + `conductor`, роль без единиц — `0`, нет ключа — красный |
| F-11 | §2.3 «Правило двойного счёта» и E-A17: строка `stages.json` — единица только без функций-единиц, иначе `ref`; счёт по (`file`, `function`) |
| F-12 | §2.3: «те же 30 файлов» снято — скан всех `scripts/*.py`; число файлов первой переписи — в свидетеле A3 и строке итогов C6 |
| F-13 | не сделано здесь: утверждение «ось 31 на main» живёт в диспатче/журнале t-1774, не в спеке; спека (§2.6, §2.7, §8, E-A3) уже говорит верно и теперь ссылается на §0 критика; правка журнала — за Lead (очередь: заметка в следующем событии журнала по t-1765) |
| Q-1 | §2.3 C4: слепое пятно `meaning` (ручная метка) названо и печатается тестом; E-A18 |
| Q-2 | в очереди: §4 X2-3 — узел читает вызывающих `judge.judged_refusal` и решает советчик/судья; класс и потолок — развилка F-10 (§5, рекомендация (b)), первая строка переписи — A3 |
| Q-3 | в очереди: уже в X5-7 (текст Lead) — проверка `test_case_key_identity_join.py` на ветке после слияния `release-next` |

Новые развилки раунда: F-10 (`MEANING_CEILING` против видимого LLM-судьи), F-11 (вычисление `blocks` для отказов списком ошибок) — §5, текст
спеки написан по рекомендации (b) обеих, исполним до слова владельца.
