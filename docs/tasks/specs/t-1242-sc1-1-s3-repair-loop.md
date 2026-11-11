# t-1242 — SC1-1: петля починки S3 (31,7 % прогона 12586). Черновик спеки (designer, 27.10.2026)

Узел `speed-cost/1` SC1-1, релиз 0.10.3. Исполнитель по строке пачки: designer → **critic на план** → builder → critic.
Пакет P = `D:/ws1/yml-text-factory\ai-packages\qa-factory\`. Спека по-русски, всё, что уходит в пакет, — по-английски (FR-30).

**Главное (несущий факт §0, измерен):** находки приходят «по кусочку» НЕ потому, что гейт выхода останавливается на первой
ветке, и НЕ потому, что дирижёр возобновляет по одной находке. Гейт выхода (`exit_gate.all_errors`) собирает всех производителей
целиком. Режет одна строка: `planning_contract.variant_errors` печатает в находке `invalid_variant` только ПЕРВЫЕ ДВЕ ошибки
контракта плана у ответвления (`'; '.join(new[:2])`, `planning_contract.py:1181`). Во втором случае находку прячет проверка формы:
если в ветке есть плохой ключ, остальные проверки ветки пропускаются (`if not shaped: continue`, :1140). И эти находки — не
отказ, а «замечания» после приёма: `stage_done.s3_branch_line` печатает их ПОСЛЕ того, как S3 уже закрыт. Дирижёр 6 раз заводил
rework и отправлял его через SendMessage в ту же сессию стратега (486k), потому что так велят `SKILL.md:64-66` и `stage_done.py:781`.

---

## 0. Факты, перечитанные на дереве (main 4126e1ae)

### 0.1 Что измерено: транскрипт прогона 12586

Носитель: `C:/Users/dev1/.claude/projects/D--ws-testproject1-dev-010-testproject1-sdk-test-harness/e47e7487-1237-4b24-a0a2-799a8304a425.jsonl`
(путь — `experiments/run-sinks-12586/common.py:2`). Поиск — инструмент Grep, режим `-o`, по этому файлу.

**(a) Замечания по раундам.** Шаблон `S3: \d+ question-branch problem\(s\) the strategist can repair: .{0,170}`. Найдено 6 строк
дирижёра, это строки транскрипта 1029, 1084, 1165, 1270, 1351, 1417. Счёт по раундам: **8, 4, 4, 4, 1, 1** — совпадает с t-1230 §6a.

**(b) Виды находок в каждом раунде.** Шаблон: префиксы сообщений `stale_reason`, `invalid_variant`, `bad_branch`.

| раунд (строка) | находки |
|---|---|
| 1 (1029) | TS-2 a/b и TS-12 a/b: 4 × `stale_reason` («once Qn is answered … reason still names») + 4 × `invalid_variant` |
| 2 (1084) | TS-2 a/b: `bad_branch` (патч ставит `coverage_delta`, этого ключа нет в закрытом списке; ключ внесла починка 1-го раунда); TS-12 a/b: `invalid_variant` |
| 3 (1165) | 4 × `invalid_variant` (TS-2 OB-3; TS-12 OB-17) |
| 4 (1270) | 4 × `invalid_variant` (те же две строки, СЛЕДУЮЩИЕ поля) |
| 5 (1351) | 1 × `invalid_variant` TS-12 b |
| 6 (1417) | 1 × `invalid_variant` TS-12 b (следующие поля) |

**(c) Какие ошибки контракта показаны внутри `invalid_variant`.** Шаблон
`TS-\d+: if Q\d is answered \([a-z]\) the row would break the plan contract: [^;]{0,110}; [^-]{0,110}`. По OB-17 (TS-12) раунды
показывают ровно по две ошибки за раз, по порядку проверок `coverage_contract.validate_obligations`:
- `missing observation_boundary`;
- `applicable_scenarios`;
- `execution_scope`;
- `coverage_links`;
- `surface assertion_ref`;
- `completion_ref`;
- `expectation attribution`.

По OB-3 (TS-2): `coverage delta` → `applicable_scenarios`/`decision` → `execution_scope`/`sufficiency_review`.
**Вывод:** раунды 3–6 целиком и половина раундов 1–2 — это порез `new[:2]`, а не новые дефекты.

**(d) SendMessage к стратегу волны 2 (`a18044c6f5ef680dd`).** Шаблон `"name":"SendMessage","input":\{.{0,300}`. Строки 941, 971,
1002 — починка ДО приёма: форма передачи (4 проблемы, потом «5 more findings») и `missing_branch`. Начиная со строки 1051 — по ДВА
сообщения на раунд:
1. находки («Accepted again, but … 4 more»);
2. «Fill fresh handoff form for formal rework dispatch -N (content already correct)».

Дирижёр сам назвал это в строке 1291: «we've been fixing this schema one or two fields at a time … whack-a-mole» и прочёл
`coverage-design.md` за роль: роли чтение плагина запрещено.

**(e) Rework.** Шаблон `operation rework[^"\\]{0,200}`. Строки 1029–1458: дирижёр каждый раунд запускает
`controller.py --operation rework --stage S3 --role qa-test-strategist --rows TS-2,TS-12 --reason …`, то есть дверь, которую
напечатал `s3_branch_line`. Потом `materialize`, потом SendMessage в старую сессию: новый Agent ни разу не запускался.

### 0.2 Код (файл:строка — каждое место, которое меняется или читается)

| место | факт |
|---|---|
| `P/scripts/planning_contract.py:963-1272` `variant_errors` | чистая проверка, «never raises»; единственный читатель веток для выхода S3 (`stage_done.s3_branch_line`), репетиции S4 (`gate_preflight.check_question_branches` :1428) и драйвера (`story_run.question_branch_findings` :3405) |
| `planning_contract.py:1173-1181` | `new = [e for e in errors if e not in base]`; `message … contract: {'; '.join(new[:2])}` — **порез до двух** |
| `planning_contract.py:1119-1141` | любой плохой ключ ветки (`shaped = False`) → `continue`: `stale_reason` и `invalid_variant` по ВСЕЙ ветке не считаются |
| `planning_contract.py:2329-2350` `missing_branch_findings` | на выходе S3 отказ (через `detector_main` :2353-2418) даёт только вид `missing_branch` |
| `P/scripts/stage_done.py:347-394` `s3_branch_line` | остальные виды веток → ОДНА строка «S3: N question-branch problem(s) the strategist can repair: …» со всеми сообщениями через `; ` и дверью `controller.py … --operation rework … --rows <все where> --reason "<this finding>"`; «REPORTS and never refuses», «writes nothing (FR-45)» |
| `stage_done.py:802-811` (в `run`) | строка печатается после всех отказов и ДО коммита перехода (:860) |
| `stage_done.py:777-787` (в `run`) | отказ `--status running` советует дирижёру: «SendMessage to the role's agent id … reaches the agent that still holds the context» |
| `P/scripts/story_step.py:1753-1756` (в `finish`) | `notes += [строки вывода stage_done][-4:]` — от вывода stage_done остаются **последние 4 непустые строки**; после строки S3 печатаются `pipeline.json: S3 -> done …` (:861) и `print_boundary_notice` (:570-586, текст бывает многострочным) |
| `story_step.py:292-310` `_handoff_check` | проблемы формы режутся: `report["problems"][:4]`, `filled[:3]` / `filled[:2]` — тот же класс «порез → лишний раунд» (0.1 (d): «4 fields», потом «5 more findings») |
| `story_step.py:1470-1512` `_gate_refusal` | дверь отказа `finish`: «the conductor gives … these findings back (resume the same role with the lines above)» |
| `story_step.py:720-737` `_packet_lines` | rework-пакет попадает в промпт карточки строкой `Rework of <parent> (cause …): <reason>` и `Plan rows of this dispatch: …`; отсюда `reason` доходит до роли без изменения схемы |
| `story_step.py:808-812` `IDENTITY_FIELDS` | карточка строится только из полей пакета (`where` и `materialize` сравнивают её побайтно) |
| `P/scripts/controller.py:2402-2504` `build_rework_request` | rework — только для ПРИНЯТОЙ работы; `--rows` проверяются по плану; `--reason` обязателен. Меняться не нужно |
| `P/skills/qa-story/SKILL.md:64-66` | «Back means `controller.py --operation rework …` then `story_step.py materialize`, and launch its card (`SendMessage`: this session only)» — **инструкция возобновлять** |
| `P/skills/qa-story/phases/s3.md` (весь, 120 строк) | о замечаниях выхода S3 и о том, как запускать их починку, — ни слова (Grep `(?i)sendmessage\|resume\|rework\|remark\|question-branch\|if_answered` пуст; контроль той же формы на `SKILL.md` нашёл :65, :66, :91 …) |
| `P/scripts/plan_row.py:63-95` `row_span(text, row_id)` | единственный читатель «где в файле объект строки» (байтовые смещения) |
| `P/scripts/guard_pre_tool.py:681-698` `big_read_cap(cfg)` | «the ONE reader of the limit» на чтение роли целиком (`config.read.max_bytes`, 30000) |
| `P/scripts/detector_verdict.py:333-362` `render` / `_pointer` | общий рендер списка: целиком до 6000 байт, дальше указатель на файл, который пишет этот же вызов |
| `P/scripts/exit_gate.py:1093-1120` `all_errors` | складывает всех производителей; порезов нет (только потолок рендера 6000 байт с файлом). **`exit_gate.py` правки не требует** — отклонение от «Пишет в» строки пачки (§6 F6) |

Где сейчас живут тесты:
- `P/scripts/tests/test_question_branches.py` (`variant_errors`; :147-151 — «каждая ветка — своя находка, если слитые патчи разные»);
- `P/scripts/tests/test_story_closed.py:587-677` (`s3_branch_line`: одна строка, дверь `--rows TS-1, TS-2`, пустые и битые входы);
- `P/scripts/tests/test_s3_s4_chain.py:167-244`.

### 0.3 Чего нет (отрицательные утверждения с контролем)

- В `exit_gate.py` нет остановки «на первой находке»: `all_errors` (:1109-1113) складывает 7 производителей, `main` блокирует
  один раз на всё. Это прочитано целиком (строки 1–1254). Это не поиск, поэтому контроль поиском не нужен.
- `planning_contract.py` и `stage_done.py` во «Пишет в» других пачек, кроме `codex/*`, не найдены. Контроль той же формы:
  шаблон `planning_contract|stage_done\.py|story_step\.py` по `plans/piles/**/batch-*.md` нашёл `codex/batch-1`, `codex/batch-2`.
  Статус этих пачек дизайнер не проверял — это сделает интегратор через `piles.py check` (б) до взятия.

## 1. AR / FR

**AR-n (P/design/architecture.md), которые узел трогает:**

| AR | как держится | change check в DoD |
|---|---|---|
| AR-13 один читатель факта | ветки читает только `variant_errors`, место строки — только `plan_row.row_span`, потолок чтения — только `guard_pre_tool.big_read_cap`, рендер списка — только `detector_verdict.render` | grep `new\[:2\]` и `\[:4\]` по изменённым функциям пуст (с позитивным контролем на другой срез в том же файле); в `stage_done` нет своей копии 30000 / 6000 |
| AR-15 одна выжившая реализация | правка `variant_errors` сразу доходит до выхода S3, репетиции S4 и драйвера | спека называет трёх потребителей (§0.2); точечные тесты A1–A3 зовут `variant_errors` напрямую |
| AR-18 одна форма вывода детектора | `detector_main` печатает те же строки `REJECT …`/`- …`; меняется только текст сообщения `invalid_variant` (длиннее) | `test_s3_s4_chain.py` зелёный (интегратор, канон) |
| AR-21 собранное стадией едет целиком | замечания S3 — пакетом-файлом, ни одно не теряется ни в строке, ни в хвосте `[-4:]` | ключи B2, B5, B7 |
| AR-22 у каждого поля есть читатель | пакет пишет `stage_done`, читает роль через `reason` → `_packet_lines` → карточка; у новой константы-префикса два читателя (`finish`, тест) | B9: пакет назван в карточке rework (сквозной тест) |
| AR-23 пустой исход объявлен | нет замечаний → нет пакета и нет строки (как сейчас, (c)/(d) `test_story_closed`) | B3 |
| AR-24 слово человека доходит целиком | слово, записанное на старый двухошибочный текст, — ребро E7 | A6 |
| AR-28 неизвестное не становится проходом | пакет не записался → все находки печатаются в строке, как раньше (FR-41) | B6 |
| AR-11 роли — только нужный контекст | починка — свежий маленький диспатч: пакет + диапазоны строк, а не контекст 486k | текст SKILL/s3 (C1, C2); мера §7 |
| AR-8 путь даётся, а не ищется | пакет называет диапазоны строк `work/test-plan.json` по каждой строке плана | B4 |
| AR-12 трение меряется | §7: счётчик раундов в тесте A5 + `run_sinks.py` (SC1-0) до и после | A5 |
| AR-19 близнецы стадий | драйвер (`story_run.py`) читает тот же `variant_errors` (выигрывает автоматически); путь возобновления у драйвера — близнец, в очередь (§6 F7) | названо в отчёте |

**FR (P/design/factory-rules.md), разделы:**
- **A.** FR-1: отказ и замечание говорят, чего ждут. FR-2: дверь «новый Agent» дирижёру доступна. FR-4: замечание не отказ — S3 закрывается как сейчас.
- **B.** Текст человеку не меняется. Карточки гейта A показывают тот же `message` — длиннее, но в той же форме (E1).
- **C.** FR-15: путь даётся. FR-38: требование доходит до роли до работы — все ошибки варианта в первом раунде. FR-49: собранное едет целиком.
- **D.** FR-59: неизвестное не проходит (E5, E9).
- **E.** FR-37: путь пакета в тексте = путь, который пишет код.
- **F.** FR-41: «не записан» говорится. FR-51 и FR-55: мера в §7.
- **G.** FR-30: английский. FR-32: корень, а не экземпляр. FR-47: код сообщает, роль чинит. FR-54: соседи по карте (ось 13 — «один порез ↔ N читателей», ось 5 — близнецы стадий, ось 17 — форма вердикта).

## 2. Модель (одна страница)

Сейчас один круг такой:
1. Стратег сдаёт.
2. `finish` → `stage_done` закрывает S3 и печатает замечания. Ошибки контракта показаны по две на вариант; ветка с плохим ключом молчит обо всём остальном.
3. Дирижёр: `rework` → `materialize` → SendMessage находок в сессию 486k → SendMessage «заполни новую форму» → `finish`.
4. Снова замечания — следующие две ошибки.

Раундов было 6, запросов 149, чтения кэша 55,1 млн.

После узла:
1. **Все находки сразу** (часть A). `invalid_variant` называет ВСЕ новые ошибки контракта у варианта. Плохой ключ ветки
   по-прежнему называется (`bad_branch`), но остальная, правильно сформированная часть ветки проверяется дальше: проверяется патч
   без плохих ключей. Одна функция — значит, это получают выход S3, репетиция S4 и драйвер.
2. **Замечания одним пакетом** (часть B). `s3_branch_line` кроме строки пишет ОДИН файл-пакет:
   `state/findings/s3-remarks-<sha12>.md`, имя адресовано содержимым. В пакете:
   - все находки целиком, по строке на находку;
   - для каждой строки плана — её диапазон строк в `work/test-plan.json` (`row_span` → номера строк) и готовые
     `Read offset/limit`, чтобы роль не искала.

   Строка, которую видит дирижёр, короткая: число находок, строки плана, путь пакета и ОДНА готовая команда rework, у которой
   `--reason` называет пакет. Через `reason` пакет попадает в промпт карточки (`_packet_lines`) — без нового поля в схеме
   контроллера.
3. **Починка — свежим диспатчем** (часть B, тексты). Карточка rework запускается НОВЫМ Agent (`bind` к новому agent id).
   SendMessage остаётся для диспатча, который ещё работает и ждёт ответа: ответ на halt, обзор источников S1, вопрос.
   Принятая работа, отправленная назад со списком находок, — всегда свежий диспатч (B-070: возобновлённый ход ×1,95).
   Тексты: `SKILL.md:64-66`, `stage_done.py:781`, абзац в `s3.md`, дверь `_gate_refusal`.
4. **Порезы того же класса на том же пути.**
   - `finish` больше не теряет строку замечаний в хвосте `[-4:]`.
   - `_handoff_check` отдаёт весь список проблем формы: рендер `detector_verdict.render` с файлом
     `state/findings/<dispatch>-form.txt`, а не первые 4.

Что НЕ меняется:
- замечания не становятся отказом (FR-4, FR-7; развилка F1);
- `controller.py` не меняется;
- `exit_gate.py` не меняется;
- форма нового rework-диспатча («заполни свежую форму») — граница с SC1-2 (развилка F5).

## 3. Части по билдерам

Обе части — по ≤ ~250 строк диффа. Владения не пересекаются, и части **можно запускать параллельно**: B читает от A только
текст сообщений. По порядку пачки (`story_step.py`: SC1-1 → SC1-8 → SC1-14) часть B первая на `story_step.py`.

### Часть A — `variant_errors`: все находки за раунд

owns:
D:/ws1/yml-text-factory\ai-packages\qa-factory\scripts\planning_contract.py (variant_errors)
D:/ws1/yml-text-factory\ai-packages\qa-factory\scripts\tests\test_question_branches.py
D:/ws1/yml-text-factory\ai-packages\qa-factory\changelog.d\speed-cost-1-sc1-1a-all-branch-findings.md

Шаги:
1. `:1177-1181`. Сообщение `invalid_variant` несёт ВСЕ ошибки из `new`, в их порядке, через `; `. Начало строки сохраняется
   байт в байт: `"{rid}: if {qid} is answered ({answer}) the row would break the plan contract: "` (E7). Хвост
   ` - the strategist's rework repairs this row` (из `add`) остаётся. Потолка в `variant_errors` нет: функция чистая и не
   пишет файлов. Объём ограничен самим построением — это ошибки одной пропатченной строки (E1). Потолок ставят места печати
   (часть B; `gate_preflight` и драйвер печатают через свои рендеры).
2. `:1119-1141`, проверка формы. Плохой ключ ветки (буква не из чтений, патч — не объект, ключ патча вне закрытого списка)
   по-прежнему даёт `bad_branch` по каждому ключу, как сейчас. Но `continue` больше не пропускает всю ветку. Дальше
   (`groups`, `stale_reason`, `invalid_variant`) считаются для ветки, из которой убраны:
   - ключи-буквы, которых нет среди чтений;
   - не-объектные патчи;
   - в каждом патче — поля вне закрытого списка.

   Ветка, где после очистки не осталось ни одного патча-объекта, дальше не проверяется (нечего применять).
   **Инвариант позиции (E8):** поле вне закрытого списка НИКОГДА не применяется к строке — ни при проверке, ни где-либо ещё.
   `apply_patch` получает только очищенный патч. `touched` и `dependent_pair` считаются, как сейчас, по полям, которые
   встретились (`fields.update` только для патчей-объектов в закрытом списке; без изменений).
3. Ничего больше в `variant_errors` не меняется. Остаются прежними:
   - виды находок и `BRANCH_KINDS`;
   - ключи словаря находки (`kind/owner/where/question/message[/lacking]`; новый ключ не добавляется — AR-22, у него не было бы читателя);
   - порядок находок;
   - `has_branch_fields` и дата O12.
4. Фрагмент `changelog.d` (по-английски, форма — `changelog.d/README.md`):
   ```
   - Question-branch checks name every finding in one round (`planning_contract.py`): a variant that breaks the plan
     contract lists all of its contract errors, not the first two, and a malformed key no longer hides the rest of its
     branch. TP1-12586 spent six S3 repair rounds on two plan rows, two fields at a time (speed-cost SC1-1).
   ```

Тесты (новые функции в `test_question_branches.py`, на `harness.check_eq`):
- **A1** `test_sc1_1_invalid_variant_names_every_contract_error`. Одно обязательство в патче без 7 полей:
  `observation_boundary`, `applicable_scenarios`, `decision`, `execution_scope`, `sufficiency_review`, `coverage_links`, плюс
  `requirement_refs`. Сообщение содержит каждую из ошибок `validate_obligations` для этого обязательства, их число = длине `new`.
  Негативный контроль: обязательство с одним пропуском даёт ровно одну ошибку в сообщении.
- **A2** `test_sc1_1_a_bad_key_hides_nothing_else`. Ветка `{"a": {"coverage_delta": 1, "reason": "per Q1 …"}}` на строке, чей
  `reason` называет Q1. Ожидается два вида находок: `bad_branch` (про `coverage_delta`) И `stale_reason` (`a`). До правки был
  только `bad_branch`.
- **A3** `test_sc1_1_a_key_outside_the_list_is_never_applied`. Шпион на `apply_patch` (подмена в модуле, восстановление
  в `finally`) видит патч без `coverage_delta`. Вариант с одним плохим ключом и правильным остатком даёт `bad_branch` и ничего
  больше.
- **A4** `test_sc1_1_message_head_unchanged`. Начало сообщения до первой ошибки байт в байт равно прежнему шаблону, и хвост
  ` - the strategist's rework repairs this row` на месте.
- **A5** `test_sc1_1_rounds_to_clean` — **мера §7**. Фикстура повторяет 12586:
  - TS-2: одно обязательство OB-3 без 6 полей и с `coverage delta`, ветки a/b;
  - TS-12: OB-17 без 7 полей, ветки a/b, `reason` называет Q.

  Функция-«чинщик» исправляет в плане РОВНО то, что названо в сообщениях текущего раунда: по таблице «текст ошибки → поле →
  годное значение», в тесте. Счётчик раундов до `[]` после правки = **1**. Тот же чинщик на прежнем поведении дал бы ≥ 4 —
  это фиксируется отдельным ключом: подменой `new[:2]` в копии сообщения, без мутации модуля.
- **A6** `test_sc1_1_a_head_word_still_passes` (E7). Слово человека с `match`, равным началу сообщения
  `"TS-2: if Q1 is answered (a)"`, через `waiver.split_overridden` проходит новую, длинную находку.

Существующие ключи, которые обязаны остаться зелёными: `:147-161` (две находки при разных слитых патчах), `:207-238`, `:102-123`.

### Часть B — замечания одним пакетом, свежий диспатч, порезы на пути `finish`

owns:
D:/ws1/yml-text-factory\ai-packages\qa-factory\scripts\stage_done.py (s3_branch_line, +_s3_remark_package, +S3_REMARK_PREFIX, run)
D:/ws1/yml-text-factory\ai-packages\qa-factory\scripts\story_step.py (finish, _handoff_check, _gate_refusal)
D:/ws1/yml-text-factory\ai-packages\qa-factory\skills\qa-story\phases\s3.md
D:/ws1/yml-text-factory\ai-packages\qa-factory\scripts\tests\test_s3_remarks.py (new)
D:/ws1/yml-text-factory\ai-packages\qa-factory\scripts\tests\test_story_closed.py (s3_exit_reports_question_branches_and_never_refuses)
D:/ws1/yml-text-factory\ai-packages\qa-factory\changelog.d\speed-cost-1-sc1-1b-s3-remark-package.md

`SKILL.md` — по builder-rules п. 1 только интегратор. Билдер B пишет точный текст в раздел отчёта «Needed from integration»
(шаг B7), интегратор вносит его тем же коммитом пачки.

`run` в `stage_done.py` меняется только текстом отказа :777-787. SC1-12 тоже пишет `stage_done.py` (`--status running`), и если
его список функций содержит `run`, порядок такой: SC1-1 → SC1-12 (§6 F8).

Шаги:
1. **B1. `stage_done.S3_REMARK_PREFIX = "S3 remarks:"`** — константа-префикс головной строки замечаний. Один производитель
   (`s3_branch_line`), один читатель (`story_step.finish`). Это структурная метка собственного вывода кода, а не список фраз (FR-12).
2. **B2. `s3_branch_line(task_root)`.** Вход и выход те же (одна строка или `""`), и вызывающий её не меняется.
   - Строки «not checked» (нет плана, нет регистра, исключение) остаются прежними, байт в байт — ключи (e)/(f) `test_story_closed`.
   - Если находки есть, функция зовёт `_s3_remark_package` и возвращает ОДНУ строку:
     `S3 remarks: <N> question-branch finding(s) the strategist can repair on <rows> - every one, with where each row is in work/test-plan.json: <package rel path>. One repair round: \`controller.py --task-root <TASK_ROOT> --operation rework --stage S3 --role qa-test-strategist --rows <all rows, comma, no spaces> --reason "repair every finding in <package rel path>"\`, then \`story_step.py materialize\`, and launch the card as a NEW agent (a fresh dispatch: never SendMessage into the author's session). The gate rehearsal at the S4 exit stops on the same facts if they are left.`
   - `<rows>`: через `detector_verdict.named(rows, where=<package rel path>)` (первые 6 и «and K more»). В `--rows` команды —
     ВСЕ строки без пореза: урезанная команда — неверная дверь (FR-2; E2).
   - `<TASK_ROOT>` остаётся заполнителем, как сейчас. Подставить настоящий корень — техническое решение, закрыто (§6 closed-1):
     подставляется `str(task_root)`.
3. **B3. `+_s3_remark_package(task_root, found, rows_doc_text) -> (rel_path | "", reason_not_written)`.** Пишет
   `<task_root>/state/findings/s3-remarks-<sha256(body)[:12]>.md`: через временный файл и `os.replace`, кодировка utf-8.
   Тело пакета:
   - строка-голова: `# <N> S3 question-branch finding(s), plan sha256 <sha12 of plan bytes>, <iso time>`;
     **время — не в теле, по которому считается имя**: имя считается по телу без строки времени, чтобы повтор на тех же байтах
     плана давал то же имя (E6);
   - секция `## Findings` — каждая находка `- <message>`, целиком, в порядке `variant_errors`;
   - секция `## Rows`. Для каждой строки из `where` находок, без повторов, в порядке находок — строка
     `- <rid>: work/test-plan.json lines <a>-<b> (Read offset <a> limit <b-a+1>)`. Номера строк — из `plan_row.row_span(text, rid)`
     (байтовые смещения → номер строки = `text.count("\n", 0, start) + 1`). Если `row_span` дал `(-1, -1)` — строка
     `- <rid>: not located by position; Grep -n "\"<rid>\"" work/test-plan.json` (E15);
   - последняя строка: `Repair every finding above in work/test-plan.json, then return your digest. Each finding names the field and the value it expects; nothing else in the plan needs reading.`

   Кавычки и обратные слэши в `rid` экранируются как в JSON. Пакет — только ASCII-безопасный UTF-8 из текстов находок.
   Запись не удалась (OSError) → `("", "<ExcName>")`: B2 тогда печатает прежнюю строку со ВСЕМИ сообщениями inline и хвостом
   `(the remark package was not written: <ExcName>)` (E5, AR-28).
4. **B4. Потолок чтения (E3).** `cap = guard_pre_tool.big_read_cap(load_config())`, импорт внутри функции; при исключении — 30000
   НЕ подставляется руками, пишется `cap = 0`, то есть «не проверено».
   - Размер пакета ≤ cap или cap ≤ 0 → строка B2 без добавок.
   - Размер > cap → в строке B2 перед `One repair round` добавляется
     `The package is <n> bytes, over the whole-read limit <cap>: read it with Read offset/limit.`

   Пакет НЕ режется: находка никогда не теряется.
5. **B5. `finish` (`story_step.py:1756`).** Строки вывода `stage_done`, которые остаются в `notes`, — это последние 4 непустые
   строки ПЛЮС каждая непустая строка, начинающаяся с `stage_done.S3_REMARK_PREFIX`. Строка, попавшая в обе группы, берётся один
   раз, на своём месте. Порядок — как в выводе.
   **Инвариант позиции (E9):** что бы `stage_done` ни напечатал после строки замечаний (уведомление окна, журнал), она доходит до
   дирижёра. Ветка `if code:` (отказ `stage_done`) не меняется. Больше в `finish` ничего не трогается.
6. **B6. `_handoff_check` (`story_step.py:292-310`).**
   - Проблемы формы: вместо `[:4]` весь список `"<path>: <problem>"` рендерится через
     `detector_verdict.joined(items, noun="form problem", full_path=<task_root>/state/findings/<safe dispatch>-form.txt, max_chars=detector_verdict.FINDINGS_MAX_BYTES, sep="; ")`.
     `joined` — однострочный близнец `render`: `form_note` печатается в одну строку (:1604).
   - `filled[:2]` / `filled[:3]` (что код заполнил сам) остаются: это заметки, а не находки, и их порез не порождает раунд
     (закрыто, §6 closed-3).
   - Форма возврата `(status, note, rel)` та же.
   - Читатель `report["problems"]` терпит лишние ключи в элементе (SC1-2 может их добавить; AR-22): читаются только `path` и
     `problem`, элемент без них — `str(item)`.
7. **B7. Тексты «возобновить → свежий диспатч».**
   - `_gate_refusal` (:1486-1488). Для НЕпринятого диспатча свежей двери без слова человека нет: rework — только для принятой
     работы, `controller.py:2467-2486`. Поэтому дверь остаётся «resume», но текст требует ОДНО сообщение со всем списком:
     `the conductor gives {role} ALL of these findings back in ONE message (the lines above, or the whole-list file they name) - never one finding per message`.
     Свежий диспатч для отказа до приёма — развилка F4.
   - `stage_done.py:780-783` (в `run`): `SendMessage to the role's agent id … reaches the agent that still holds the context, and a fresh dispatch …`
     → `rework it with \`controller.py --task-root <TASK_ROOT> --operation rework …\` and launch its card as a NEW agent - a fresh dispatch reads only the findings and the lines it needs (resuming a long session costs about twice per turn, B-070); SendMessage is for a dispatch still at work that waits for an answer.`
     Остальной текст отказа не меняется.
   - `s3.md`. Новый абзац после «Validate and record S3…» (:93-95), ≤ 600 байт:
     `**Remarks after S3 closes.** \`finish\` may print an \`S3 remarks:\` line: S3 is accepted, and question-branch findings remain. They come ALL at once, in one package file the line names. Run the one rework command it prints, \`materialize\`, and launch the card as a NEW agent (\`bind\` its new id). Never SendMessage the plan's author: its session is the plan's whole history. A remark still standing after that round is the S4 rehearsal's, or a person's word (\`waiver.py --stage S3\`).`
   - `SKILL.md:64-66` («Needed from integration», точный текст):
     `then \`story_step.py materialize\`, and launch its card as a NEW agent (a fresh dispatch; SendMessage only reaches a dispatch still at work that waits for an answer).`
     Байт после правки ≤ байт до (потолок 19000, builder-rules п. 5).
8. **B8. Фрагмент `changelog.d`:**
   ```
   - S3 remarks travel as one package and are repaired by a fresh dispatch (`stage_done.py`, `story_step.py`,
     `phases/s3.md`): the S3 exit writes every question-branch finding and where each plan row sits in
     work/test-plan.json to one file, prints one rework command naming it, and tells the conductor to launch the card as
     a new agent instead of resuming the author's session; `finish` keeps that line whatever follows it, and a
     handover form refusal lists every problem, not the first four. TP1-12586: 6 rounds, 15 messages into a 486k
     session, 55.1M cache-read tokens (speed-cost SC1-1).
   ```

Тесты B (новый узкий файл `test_s3_remarks.py`, `harness.temp_project`; `test_story_step.py` — большой файл, и билдер его не
гоняет, D-0056):
- **B-t1** пакет записан; строка начинается с `S3 remarks:`; в ней путь пакета, `--rows TS-2,TS-12`, `--reason "repair every finding in state/findings/s3-remarks-`, `NEW agent`. Пакет содержит каждое сообщение находок, в каждой строке.
- **B-t2** диапазоны: в плане-фикстуре TS-12 стоит на строках 7–15 → пакет содержит `lines 7-15 (Read offset 7 limit 9)`. Строка
  без позиции (id есть в находке, но не в файле) → `not located by position; Grep -n`.
- **B-t3** идемпотентность: два вызова на тех же байтах плана → то же имя, те же байты, кроме строки времени. Изменили план → другое имя.
- **B-t4** потолок (E3): `config.read.max_bytes` = длина пакета → без добавки (РОВНО на пределе); = длина − 1 → добавка `over the whole-read limit`; = 0 → без добавки.
- **B-t5** OSError при записи (каталог `state/findings` занят файлом с тем же именем) → строка со всеми сообщениями inline и `the remark package was not written: `.
- **B-t6** `finish`, хвост (E9): подмена `story_step._run` на вывод stage_done из 7 строк, где `S3 remarks: …` — вторая. После
  `finish` строка в `notes` ровно одна. Контроль: строка на последнем месте — тоже одна, не две.
- **B-t7** `_handoff_check` с 9 проблемами → все 9 в `note`. При потолке — файл `state/findings/<dispatch>-form.txt` и указатель
  `(+K more form problem(s) — the whole list: …)`. Контроль: 4 проблемы — без указателя.
- **B-t8** тексты: `_gate_refusal` содержит `in ONE message`; отказ `stage_done --status running` по принятому S3 содержит
  `as a NEW agent` и не содержит `still holds the context`; `s3.md` содержит `**Remarks after S3 closes.**`.
- **B-t9** сквозной: план с находками → `stage_done.run(S3 done)` → взять путь из строки → `controller rework` с этой
  командой (собранной из строки) на фикстуре с принятым S3 → `story_step materialize` → текст карточки содержит путь пакета (через `_packet_lines`).
- `test_story_closed.py::s3_exit_reports_question_branches_and_never_refuses` — обновить ключи (a)/(b) под новую голову:
  - `S3 remarks: 1 question-branch finding(s)`;
  - дверь `--rows TS-1` / `--rows TS-1,TS-2` вместо `--rows TS-1, TS-2`;
  - пакет лежит в `state/findings/`;
  - `the plan is not touched` (байты плана те же) остаётся;
  - ключ «writes nothing» превращается в «пишет только `state/findings/s3-remarks-*.md`» (E11).

## 4. Рёбра (правило 11; у каждого — инвариант)

| # | ребро | поведение | инвариант, который держит |
|---|---|---|---|
| E1 | предел: длина `invalid_variant` | без пореза; объём ограничен построением: ошибки `gate_plan_errors` одной пропатченной строки (≈ 25 проверок на обязательство × число обязательств). Места печати режут своим рендером с файлом (B2 — пакет; гейт A — `gate_preflight`, как сейчас) | первый раунд называет всё, что репетиция S4 назвала бы на этих байтах; ни одна ошибка не прячется за счётчиком |
| E2 | конфликт: короткая голова ↔ полная команда | список строк в голове режется `named` (6 и «and K more» с путём); `--rows` в команде — все | дверь, которую печатает код, исполнима как есть (FR-2) |
| E3 | предел: размер пакета ↔ `big_read_cap` | ≤ cap — без добавки (тест РОВНО на пределе); > cap — строка говорит размер и «offset/limit»; cap ≤ 0 или не прочитан — без добавки | находка не режется никогда; роль заранее знает, как читать |
| E4 | пустой вход | нет находок → нет пакета и нет строки; нет плана / регистра / исключение → прежние строки «not checked», пакета нет | пустой исход назван (AR-23); пакет без находок не появляется |
| E5 | запись не удалась | все сообщения inline, как до узла, + `(the remark package was not written: <Exc>)` | неизвестное не становится тишиной (FR-41, AR-28) |
| E6 | временное: пакета нет до узла | до узла — строка inline (старые сборки). После узла пакет пишет `stage_done` при S3 done, если есть замечания. Имя адресовано содержимым (без строки времени); пакеты прошлых раундов не удаляются, строка называет только текущий | `reason` старого rework-пакета указывает на неизменные байты; повтор на тех же байтах — тот же файл |
| E7 | слово человека на старый текст (история в работе) | слово, процитировавшее НАЧАЛО сообщения, проходит (A6). Слово, процитировавшее всё старое сообщение вместе с хвостом ` - the strategist's…` при > 2 ошибках, больше не совпадает подстрокой — находка снова видна как замечание или отказ S4 | слово человека проходит то, что он назвал (P13); утрата возможна только для дословной цитаты целого старого текста, и она названа в отчёте, а не молчит |
| E8 | позиционное: проверка формы ветки | плохой ключ → `bad_branch`, остаток ветки проверяется дальше без плохих ключей | ключ вне закрытого списка никогда не применяется к строке (A3); отсутствие `bad_branch` никогда не наступает |
| E9 | позиционное: хвост `finish` | строка `S3 remarks:` держится независимо от положения; прочие строки — последние 4, как было | что `stage_done` сказал дирижёру о замечаниях, до дирижёра доходит (AR-21) |
| E10 | конфликт требований: B-070 ↔ MEASUREMENTS 1.3 | 1.3: «возврат критика через SendMessage ≈ $0.20 против $0.75–3.89 за новый раунд 2» (пилот, малый контекст). B-070: возобновлённый ход ×1,95. Правило по РОДУ работы: принятая работа со списком находок → свежий диспатч; живой диспатч, ждущий ответа → SendMessage | дорогая сессия не возобновляется ради механической починки; дешёвый ответ живому диспатчу не превращается в холодный старт (порог по размеру контекста — развилка F2) |
| E11 | конфликт: `s3_branch_line` «writes nothing (FR-45)» ↔ пакет | пакет — производный файл в `state/findings/`, как `exit_gate.render_saved` (`exit_gate.py:105-126`); план и регистр не трогаются (B-t1 сравнивает байты плана); docstring переписывается | валидатор не пишет в проверяемое и не пишет в то, что пересобирает проекция (FR-45 в своём смысле) |
| E12 | строки без id | находка с `where` = `row[3]`: в пакете — `row[3]: no id; …`, в `--rows` не попадает. Если id нет ни у одной — команда без `--rows` (S3 его допускает, `controller.py:2411-2413`) | дверь не называет строку, которую `controller` отвергнет как «not in the approved plan» |
| E13 | строка удалена между находкой и командой | `controller rework` откажет со списком строк плана (как сейчас); пакет при этом не врёт — он о байтах плана на момент закрытия | отказ называет дверь, а не молчит |
| E14 | гонка двух `stage_done` одной истории | одно имя, одни байты; запись через временный файл и `os.replace` | файл пакета всегда целый |
| E15 | `row_span` ошибается | она находит первое вхождение `"id": "<rid>"` и ближайшую `{` перед ним (`plan_row.py:68-75`); если id — не первый ключ строки, диапазон может оказаться узким. **Направление ошибки:** диапазон — подсказка; ошибка стоит одного лишнего Read; находка из-за неё не теряется | функция-советчик не становится гейтом: ничего не решается по диапазону |
| E16 | консоль без UTF-8 | существующий `UnicodeEncodeError` → ascii replace (`stage_done.py:808-811`) сохраняется | строка доходит в любой консоли |
| E17 | `variant_errors` на мусорных входах | «never raises» сохраняется: очищенный патч строится в той же защите; тест `:408` (garbage) остаётся | P1: проверка не роняет фабрику |

**Функция в новой, более ответственной роли (designer rule 1).** `plan_row.row_span` — была записью одной строки, стала советом
роли о диапазоне строк. Ошибаться ей разрешено в сторону ЛИШНЕГО чтения (узкий или неверный диапазон, `not located`). Нельзя:
выдать диапазон чужой строки без пометки. Неудобные входы:
- id стоит не первым ключом строки;
- `"id":"TS-2"` в компактной записи;
- id-подстрока (`TS-1` внутри `TS-12`): ищется с закрывающей кавычкой, `row_span` уже так делает;
- строка внутри вложенного объекта.

Тест B-t2 держит первый и третий входы. Если по замеру диапазон окажется чужим, это находка в SC1-3 (владелец `plan_row.py`),
а не правка здесь.

## 5. DoD частей

**Часть A — точечные проверки (из `ai-packages/qa-factory`):**
```
python -B scripts/tests/test_question_branches.py
```
Ключи DoD: A1–A6 зелёные; существующие ключи файла зелёные. Grep `new\[:2\]` по `scripts/planning_contract.py` пуст; позитивный
контроль той же формы — `\[:2\]` находит другие срезы в том же файле.

Мутации и их убийцы:

| мутант | убивает |
|---|---|
| вернуть `new[:2]` | A1 |
| вернуть `continue` при `not shaped` | A2 |
| применять неочищенный патч | A3 |
| изменить голову сообщения | A4 |
| слово человека по голове | A6 |

**Часть B — точечные проверки:**
```
python -B scripts/tests/test_s3_remarks.py
python -B scripts/tests/test_story_closed.py
python -B scripts/selftest.py --limits --lang
```
`--limits --lang` — потому что меняются `s3.md` и текст для `SKILL.md`. Ключи DoD — B-t1…B-t9.

Мутации и их убийцы:

| мутант | убивает |
|---|---|
| строка без пакета | B-t1 |
| `--rows` урезан | B-t1 |
| время в теле имени | B-t3 |
| `>` вместо `>=` на потолке | B-t4 |
| пакет не записан → пустая строка | B-t5 |
| вернуть `[-4:]` без префикса | B-t6 |
| вернуть `[:4]` | B-t7 |
| вернуть «still holds the context» | B-t8 |
| `reason` без пути | B-t9 |

**BATCH CANON (интегратор, один раз на пачку):**
- `test_story_step.py`, `test_story_step_materialize.py`, `test_s3_s4_chain.py`, `test_gate_preflight.py` (check_question_branches), `test_whole_list_sites.py`, `test_story_run_gate_repair.py`;
- `test_story_run_words.py` и `test_driver_layers.py`: драйвер — потребитель `variant_errors`, правило 7c;
- `test_audit_rules.py`, докер python:3.12, храповики (`dup_ratchet`, `lint_ratchet`), мутационный проход по таблицам выше;
- внести текст `SKILL.md` из «Needed from integration» B7;
- `architecture:` строка коммита: `AR-13, AR-15, AR-21, AR-22, AR-23, AR-28 -- one reader each, every finding in one round, the remark package travels whole`.

## 6. Развилки (решает Lead / владелец; у каждой — рекомендация)

- **F1. Замечания — отказ или замечание?**
  - (a) Оставить замечанием после приёма — эта спека.
  - (b) Сделать все виды веток стратега отказом выхода S3 (`missing_branch_findings` → все виды `owner == strategist`). Тогда хук
    блокирует один раз в ТОМ ЖЕ ходе роли, починка обходится без нового диспатча. Двойной остановки нет: S4 уже читает слово S3,
    `gate_preflight.py:1442-1444`.

  Рекомендация: **(a) сейчас**. (b) — после замера SC1-13: после части A раунд обычно один. (b) меняет смысл гейта (PROJECT.md,
  приём п. 6: критик на план), и у отказа на `finish` до приёма свежей двери нет (F4).
- **F2. Когда свежий диспатч, а когда SendMessage.**
  - (a) По роду работы — эта спека (E10).
  - (b) Порог по измеренному контексту сессии автора (транскрипт субагента, ось 14).
  - (c) Решает дирижёр.

  Рекомендация: **(a)**. Детерминированно, без чтения транскриптов. (b) — если SC1-13 покажет дорогие холодные старты.
- **F3. Кто заводит rework замечаний.**
  - (a) `finish` сам строит rework и materialize и печатает готовую карточку (P3: команды запускает код по переходу).
  - (b) Дирижёр запускает две напечатанные команды — эта спека.

  Рекомендация: **(b) сейчас, (a) — в SC1-8** (диета дирижёра). После части A раунд в среднем один, и (a) экономит 2–3 хода
  дирижёра, но делает `finish` писателем второго диспатча (риск: живой rework S3 мешает началу S4 — не проверено).
- **F4. Отказ `finish` ДО приёма** (форма, `missing_branch`; 12586: строки 941/971/1002, три SendMessage).
  - (a) Оставить resume, но одним сообщением со всем списком — эта спека.
  - (b) Новая операция контроллера «repair relaunch» для непринятого диспатча (свежий агент с той же карточкой и списком).

  Рекомендация: **(a) + (b) в очередь** находкой в `speed-cost/findings/` (схема контроллера, критик).
- **F5. Свежая форма передачи для каждого rework** (12586: второе SendMessage каждого раунда — «content already correct»). Форма
  rework могла бы наследовать принятую форму родителя (`handoff_init.py`).

  Рекомендация: **в SC1-2** (владелец `handoff_init.py`, «`--fix` заполняет выводимое»). Строку `очередь:` / узел пишет Lead. В
  SC1-1 это не входит; мера §7 считает раунд без него.
- **F6. Расхождение с «Пишет в» строки SC1-1.**
  - Узел НЕ пишет `exit_gate.py` и `controller.py`: правка не нужна (§0.3).
  - Узел ПИШЕТ `planning_contract.py` (`variant_errors`) и `stage_done.py` (`s3_branch_line`, `+_s3_remark_package`,
    `+S3_REMARK_PREFIX`, `run`) — их в строке нет. Ячейка взятой пачки заморожена.

  Рекомендация: Lead объявляет строкой «Хода» `функции:` для `story_step.py (finish, _handoff_check, _gate_refusal)`,
  `stage_done.py (s3_branch_line, run, +_s3_remark_package)`, `planning_contract.py (variant_errors)` и проверяет
  `piles.py check` (б) против `codex/*` — у них упомянуты `stage_done.py` и `planning_contract`; статус не проверен (§0.3).
- **F7. Близнец драйвера** (ось 5). `story_run.py` тоже возобновляет роль для починки (B-273). Он выигрывает от части A
  автоматически, но его путь возобновления не тронут.

  Рекомендация: находка в `speed-cost/findings/` с узлом в следующей пачке. `story_run.py` — горячий файл, не в этой ячейке.
- **F8. Порядок с SC1-12 на `stage_done.run`.** Если список функций SC1-12 содержит `run` — `очередь: SC1-1 → SC1-12`.
  Рекомендация: так.

**Технические решения, закрытые дизайнером (на остановку Lead):**
1. В команду B2 подставляется настоящий `task_root`, а не `<TASK_ROOT>`: команда исполнима как напечатана.
2. Пакет лежит в `state/findings/`, а не в `work/`: там уже живут «whole list» файлы (`exit_gate.py:105`, `story_step.py:1480`).
3. `filled[:2]`/`[:3]` не трогаются: это заметки, а не находки.
4. Внутри `variant_errors` находки не сливаются по одинаковому набору ошибок (a и b): ключ `:150-151` держит «две находки при
   разных патчах», и слияние сменило бы счёт для слов человека.
5. Фрагменты `changelog.d` — по одному на часть. README говорит «один на пачку»; интегратор при желании сливает их в
   `speed-cost-1-*.md`.
6. Новый узкий тестовый файл вместо `test_story_step.py`: D-0056, большой файл билдер не гоняет.

## 7. Мера (в числах t-1230)

Петля 12586 (t-1230 §6a, 18:48:38–19:30 UTC):

| источник | запросы | чтение кэша |
|---|---|---|
| w2 | 81 | 31 977 974 (≈ 395k на запрос) |
| дирижёр | 68 | 23 121 069 (≈ 340k) |
| **итого** | **149** | **55,1 млн (31,7 %)**, 41 мин, 6 раундов замечаний, 15 SendMessage |

**Ожидание — оценка, не замер:**
- **Раунды: 6 → 1** (A5 доказывает на фикстуре того же устройства), +1, если починка внесёт новый дефект (как `coverage_delta`
  в раунде 2; тогда он виден сразу вместе со всем остальным).
- **Роль:** свежий диспатч вместо сессии 486k. Первое сообщение ≈ 14k токенов (t-1230 §2) + пакет и диапазоны ≈ 5–10k + правки.
  ≈ 15–25 запросов × 30–60k ≈ **0,5–1,5 млн** вместо 32,0 млн.
- **Дирижёр:** на раунд rework, materialize, Agent, bind, finish ≈ 5–8 запросов вместо ≈ 11 (68/6). При его нынешних ≈ 340k
  (контекст дирижёра — SC1-8) ≈ **1,7–5,4 млн** вместо 23,1 млн.
- **Петля целиком:** ≈ **2–7 млн вместо 55,1 млн** (−87…−96 %), то есть **−48…−53 млн = 27–30 % всего прогона**. Запросы:
  149 → ≈ 20–35. SendMessage: 15 → 3 (F4 (a): до приёма) или 0, если позже сделать F4 (b). Минуты: 41 → ≈ 6–10.

**Как увидеть до живого прогона:**
- (1) **A5** — счётчик раундов на фикстуре 12586: 1 против ≥ 4, свидетель узла.
- (2) Повтор раунда 1 по артефактам: `python -I` по копии `work/test-plan.json` и регистра 12586, если интегратор их сохранит.
  `variant_errors` должен дать за один вызов все ошибки OB-3/OB-17 из 0.1 (c): 7+ по OB-17. Копия не в репозитории, поэтому это
  ключ интегратора, а не билдера.
- (3) `run_sinks.py` (SC1-0) до и после на SC1-13: строка «S3 repair loop» — запросы, чтение кэша, SendMessage, раунды.

## 8. След

**Прочитано:**
- бриф `docs/tasks/specs/drafts/20261026-release-0103-designer-brief.md` (весь);
- `plans/piles/speed-cost/batch-1-speed-cost.md` (весь);
- находка `findings/20261026-zamer-stoki-tokenov-12586.md` (вся);
- отчёт `docs/tasks/specs/reports/20261026-run12586-turn-token-sinks.md` (весь);
- `plans/BACKLOG.md` :97 (B-070), :217 (B-273);
- `plans/MEASUREMENTS.md` :20-59 (1.3);
- `plans/builder-rules.md` :8-33;
- `changelog.d/README.md`;
- `experiments/run-sinks-12586/common.py`, `q6.py`;
- `exit_gate.py` 1–1254 (весь);
- `planning_contract.py` 200–280, 820–1300, 2290–2420;
- `coverage_contract.py` 280–369;
- `observation_contract.py` 40–119;
- `stage_done.py` 330–440, 560–590, 740–873;
- `story_step.py` 200–339, 700–960, 1380–1784, 2087–2136;
- `controller.py` 2395–2504, 6130–6166;
- `gate_preflight.py` 1383–1458;
- `story_run.py` 3395–3420;
- `detector_verdict.py` 290–425;
- `plan_row.py` 49–98;
- `guard_pre_tool.py` 676–715;
- `SKILL.md` 50–119;
- `phases/s3.md` (весь);
- `tests/test_question_branches.py` 60–249;
- `tests/test_story_closed.py` 585–677.

**Искалось (Grep):**
- `if_answered` по `scripts/*.py` → 15 файлов;
- `variant_errors|check_question_branches` → 3 потребителя;
- `s3_branch_line` → stage_done:806 и тесты;
- `this session only|still holds the context|resume the same role` → SKILL.md:66, stage_done.py:782, story_step.py:1487, judge.md:27, planning_contract.py:2388, test_s3_s4_chain.py:168;
- `invalid_variant|new\[:2\]|\[:4\]|_handoff_check|s3_branch_line|\[-4:\]` по тестам — пина на текст из двух ошибок и на `[:4]` формы нет;
- `state/findings` → exit_gate, manifest_put, story_step, story_run;
- по транскрипту 12586 — шаблоны 0.1 (a)–(e);
- AR-заголовки и change check в `architecture.md`; оси `SIBLING_MAP.md` (заголовки 1–28).

**Не нашлось — с контролем той же формы:**
- в `phases/s3.md` нет слов о rework, resume и замечаниях (контроль: тот же шаблон по `SKILL.md` нашёл три строки);
- `planning_contract.py` / `stage_done.py` во «Пишет в» пачек — первый поиск с glob `*/batch-*.md` дал пусто: это промах
  glob-формы. Повтор с `**/batch-*.md` нашёл `codex/batch-1`, `codex/batch-2` (§0.3).

**Нужно сверх манифеста** (прочитано вне «given»):
- `planning_contract.py`, `stage_done.py`, `coverage_contract.py`, `observation_contract.py`, `gate_preflight.py`, `story_run.py`,
  `detector_verdict.py`, `plan_row.py`, `guard_pre_tool.py`, `builder-rules.md`, `changelog.d/README.md`;
- транскрипт прогона 12586 (вне репозитория): несущий факт §0 из одного кода не доказывался.

## 10. Решения Lead (27.10.2026 00:2x, координатор Opus, окно `lead_degraded`; технические — «решила сама»)

По рекомендациям дизайнера: F1 (а) — замечания после приёмки остаются, отказ выхода S3 — после замера SC1-13; F2 — свежий диспатч или SendMessage
выбирается по роду работы, не по порогу контекста; F3 — команду доработки запускает дирижёр, запуск из `finish` — в SC1-8; F4 — отказ до приёмки
сохраняет resume с полным списком одним сообщением, операция контроллера «перезапуск починки» — находкой; F5 — свежая форма хэндоффа — SC1-2;
F6 — «Пишет в» взятой пачки заморожена: `planning_contract.py (variant_errors)`, `stage_done.py` и функции `story_step.py (finish, _handoff_check,
_gate_refusal)` объявляются строкой `функции:` «Хода» при запуске билдеров; F7 — двойник в `story_run.py` — находкой с узлом следующей пачки;
F8 — SC1-1 раньше SC1-12 на `stage_done.run`. До билдеров — критик на план (t-1255).

## 11. Правки по вердикту критика t-1255 (Lead, 27.10.2026 00:5x; обязательны для частей A и B, перекрывают §2–§5 там, где расходятся)

Вердикт: NO-GO в целом (B1), часть A — GO с правками M1, M2, m1, m2 (файл `reviews/t-1255-t-1242-plan-review.md`).
- **B1 — одно правило по стадиям, данными (AR-1, ось 5).** Как доработка доходит до роли, задаёт поле стадии `rework_mode` в
  `references/stages.json`: `fresh` — новый агент с пакетом находок (S3, и по умолчанию для стадий, где роль копит большой контекст), `resume` —
  `SendMessage` с дельтой (окна S5, SC1-14). Часть B добавляет поле и его читателя; текст `SKILL.md:64-67` и отказ `stage_done.py:780` говорят
  «по `rework_mode` стадии», без своего правила. SC1-14 (`build_rework_request`, `_packet_lines`) переносит `agent_id` только при `resume` —
  строка в спеку t-1246 §12.
- M1 — `coverage_delta` входит в закрытый список ключей патча или `invalid_variant` перестаёт его требовать — как укажет файл критика (FR-11).
- M2 — §7 и ключ A5: ожидание «1–2 раунда», не «1»; A5 считает раунды ≤ 2 на фикстуре 12586.
- M3, M4, M5 — свежий диспатч сужается в `--reason` (≤ 200 символов: id находок и строки плана); путь пакета — от корня проекта; пакет больше
  потолка чтения — роль получает предупреждение и карту; каждая находка — строка с пределом длины (предел назван ключом).
- M6 — запасная строка E5 несёт префикс и стоит до хвоста `[-4:]`. M7 — строка замечаний идёт ДО указателя (держать при урезании SC1-8; строка в
  спеку t-1251 §12). M8 — правка `SKILL.md` нулевая по байтам: добавленное снимается в том же файле (`--limits` зелёный). M9 — три ключа
  `test_story_closed` переписываются так, чтобы падать на старой голове строки. M10 — раздел Rows не дублирует карту SC1-3: пакет называет id
  строк, роль читает их через карту гарда SC1-3; дефект `row_span` чинит SC1-3 часть 2.
- m1–m10 — по файлу критика, дословно.
Порядок: часть A — билдер сразу; часть B — после слияния SC1-3 части 2 (M10) и с полем `rework_mode` раньше SC1-14.
