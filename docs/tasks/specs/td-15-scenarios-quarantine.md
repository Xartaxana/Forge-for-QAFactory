# TD-15 — слой сценариев, список остающихся, карантин и наблюдатель (ревизия 2, принята Lead 11.11.2026, t-2287)

Статус: черновик дизайнера к приёмке Lead. Ревизия 2 вносит решения владельца O-1…O-5 (10.11.2026, 23:30,
`docs/tasks/test-diet.md` l.128–133), решения Lead по блокирующим находкам критика плана t-2281
(`docs/tasks/specs/reviews/td-15-plan-critic.md`, B1–B7) и ответ на каждую неблокирующую (R1–R9) — раздел «Ответы критику».
Каждый узел §F исполним по рекомендации каждой развилки §G.

Язык: проза по-русски (так велит диспатч ревизии; ревизия 1 была по-английски — расхождение отмечено в сводке Lead).
Всё, что пишет код пакета или форджа (тексты строк, отказов, имена полей), — по-английски и только ASCII (FR-30).

## Ревизия 2 — что изменилось против ревизии 1

1. **B1 — перевод в два шага.** Детектор, названный носителем (SIBLING_MAP, `design/architecture.md`, `design/factory-rules.md`),
   и ещё четыре файла по критериям 2/4 в первом шаге НЕ переводятся: они получают в keep слой `detector` и колонку
   «заменён чем» (`replaced_by`). Фаза 2 — по одному детектору, только когда keep называет строку сценария/стыка, которая
   ловит тот же класс, и носитель правится тем же коммитом. Критерий 1 дополнен (1b: строки DoD п. 7b, детекторы
   архитектуры и правил). Числа §B — замеренные: остаются 69, фаза 2 — 51, фаза 1 — 581 (из 701 файла на диске). L-5
   переписана.
2. **B2 — только синтетические истории.** Корпус Jira (14857, 12586) не история; `12586-gateb`, `12586-redthen`, `14857-s7`
   сняты. Источники — прогоны стенда MyBooks (LOCAL-*) и истории, записанные для этой цели. Захват вычищает людей и всё, что
   называет FK-11. Узел TD-15.0 инвентаризирует синтетические и ПОЛНЫЕ наборы; условие перевода — ≥ 3 зелёные истории,
   вместе покрывающие S0..S9, слова гейта A, слова гейта B и один красный Then. Узел записи истории на стенде TD-15.5r и
   развилка владельца G-1. Грани фасетов отказываются по стадии (`not_walked`).
3. **B3 — условие 5 `enter` заменено** стыком данных: секция `pin_holds` в `test-layers.json`; файл с пином текста роли,
   которого нет в реестре, не переводится. Строки 41–52 (12 удалённых файлов) убраны; область TD-5.3 сужена до
   кандидатов в карантин.
4. **B4 — триггер наблюдателя.** GitLab, расписание пайплайна на ветке-параметре (`plans/test-quarantine/config.json`
   `branch`), строка RUNBOOK §7, два раза в неделю (O-3), плюс прогон после каждого релиза, распознанного по смене версии в
   `.claude-plugin/plugin.json` (push-правило). `pull` читает пайплайны schedule/web/api/push, пишет время вытяжки и время
   последнего прогона наблюдателя раздельно; строка сессии показывает оба возраста; «наблюдатель не идёт» — ALERT.
   `enter` отказывает, пока расписание не видно через API. Остальные задачи `schedule` не едут с переменной.
5. **B5 — маскировка уловов.** Вердикт ключуется (файл, подпись падения, пайплайн); `stale` покрывает только ту же подпись
   (или её подмножество); новая проверка в подписи — новое неразобранное красное; `flaky` — только при красном и зелёном
   того же файла на одном коммите. READY отказан при любом неразобранном красном; печатается число «слепых» файлов.
6. **B6 — охрана K5** судит каждый коммит диапазона от появления `test-layers.json` до HEAD с его собственным сообщением,
   работает на коммитах слияния (комбинированный дифф), охраняет секции `test-layers.json` (keep покидается только командой,
   из истории карантина возврата нет), у прошлого нарушения — дверь `quarantine-accept:`.
7. **B7 — свидетель и честность.** `covers` у каждой строки keep, включая gate_named и detector; `--witness-for` называет тест
   гейта. Новый раздел §G0 «Для владельца»: замеренные числа покрытия (нижняя граница 31,3 % строк за оставшимися,
   крупнейшие уходящие файлы, `delivery_c` 19,4 %), точное число — узел TD-15.6d на CI до перевода, `enter` без него отказывает.
8. **O-1…O-5** — в правилах R (§D.3: два релиза, полный прогон на втором), в CI (два раза в неделю), в порогах (максимальный
   промежуток 4 дня, тревога после 8), в текстах строки сессии; срока нет нигде (O-5). Когорты: файлы фазы 2 входят позже,
   их счёт релизов свой.
9. Неблокирующие R1–R9: применены (двери без побочных эффектов, веса шардов, `expected` в записи, дубли, цена разбора,
   базовая линия красных/мигающих по трём ночным, порядок и владение узлов, `features.json`, тест 2 МБ снят) — «Ответы критику».
10. §F переписан: узлы TD-15.0, 15.0b, 15.1–15.4, 15.5.k, 15.5r, 15.6a–d, 15.7, 15.8, 15.9, 15.10.k; волны с не более чем 6
    пишущими; у каждого узла файл, функция/поле, ожидаемое поведение, строка теста.

---

Замысел (обязывающий, слово владельца 10.11.2026, ночь): «Значит нужно менять сам подход к написанию тестов. Нельзя покрыть
тестами всё, а эта куча тестов всё равно не ловит важное. Надо в принципе по другому писать тесты, так что бы они не проверяли
каждую строчку и мелкую функцию.» О старых тестах: «карантин и запланируй систему оповещения как мы узнаем что всё из
карантина можно удалить». Решения владельца по развилкам (10.11.2026, 23:30): O-1 удалять после ДВУХ опубликованных релизов
с входа — полный прогон наблюдателя на втором, все покраснения разобраны, каждый настоящий улов перенесён; O-2 настоящий
улов — записать, перенести случай в строку сценария/таблицы, сразу сообщить, счёт продолжается; O-3 наблюдатель два раза в
неделю; O-4 оповещение — строка в начале сессии; O-5 предельного срока нет, ждём релизов. Lead: O-6 — три истории до
перевода; L-1…L-12 по рекомендации, кроме изменённых здесь (L-5, L-8, L-11). Правило — `docs/TESTING.md` («Что пишется — три
слоя», «Карантин старых тестов»).

Область: тестовые файлы пакета `ai-packages/qa-factory/scripts/tests/test_*.py` — **701 файл** на дереве `wt-test-diet`
(замер: Grep, `files_with_matches`, шаблон `.`, glob `test_*.py`, страница offset 650 → 51 файл, итого 650 + 51; в
`fixtures/` того же шаблона нет — контроль: тот же вызов с glob `*.json` находит `judgment-census.json`). Тесты форджа
`tools/test_*.py` — вне области (L-12).

---

## §1. Затронутые инварианты (AR-n), проверка изменения каждого, владелец и класс переписи каждой проверки

| AR | Как спека его касается | Проверка изменения в DoD узлов |
|---|---|---|
| AR-3, AR-9, AR-17, AR-24, AR-25 | их единственные детекторы (`test_config_migration`, `test_controller_blocks`, `test_no_move_seam`, `test_words_doors`, `test_state_exits`/`test_controller_state`) остаются в каноне слоем `detector` до замены (фаза 2, §B.4) | `enter` отказывает, если файл, названный носителем, попал в карантин (K4 усл. 3); строка `architecture:` каждого коммита фазы 2 называет AR и строку-замену |
| AR-13 один читатель | `scripts/tests/test-layers.json` читает ТОЛЬКО `selftest.test_layers()`; фордж его импортирует | grep по `tools/` и пакету на `test-layers.json`: открывает только `selftest.py` (контроль: тот же grep находит `slow_tests.json` в `selftest.py`) |
| AR-14 один писатель | секции `quarantine` и `cohorts` пишет только `tools/test_quarantine.py enter/purge`; `keep` и `pin_holds` — ревьюемые ручные коммиты (удаление keep — только командой, K5); `plans/test-quarantine/watch.jsonl` — только `pull`; `verdicts.jsonl` — только `judge`/`land`/`purge`; `plans/test-quarantine/config.json` — Lead руками | отчёт узла называет писателя каждого созданного файла; K5 проверяет секции по истории |
| AR-20 только сжимается | `quarantine` сжимается только `purge`; `pin_holds` только сжимается после `enter`; `purge` сжимает `driver-layers.json`, `slow_tests.json`, `TEST_TIMEOUTS`, `plans/features.json` | каждая добавленная/поднятая/снятая строка перечислена (ключ, было → стало, причина); `quarantine` и `pin_holds` входят в ось 18 SIBLING_MAP и вопрос 9 критика тем же коммитом, что их создаёт |
| AR-21 передача целиком | фасет `handed` сценария (§A.3) | строка таблицы `test_scenario_walk.py` на `handed` |
| AR-22 производитель/читатель | каждое поле, которое пишут `pull`/`judge`, читает `status`; каждое поле, которое читает `status`, имеет производителя | строка таблицы `tools/test_test_quarantine.py` на поле |
| AR-23 пустой исход | пустой keep, пустой карантин, пустая запись наблюдателя, прогон с нулём файлов, история без проходимой стадии — §E2 | по строке таблицы на пустой исход |
| AR-28 неизвестное не проход | неполный прогон, нечитаемый `plugin.json`, недоступный CI на `enter`/`pull`, нечитаемое расписание — никогда не зелёное и не READY | строки таблицы; `enter` отказывает на неизвестном |
| AR-29 суждение | код проверяет данные; вердикт по красному (stale / real_catch / flaky) — суждение роли критического тира, принимает Lead; «ловит ли замена тот же класс» в фазе 2 — суждение критика; удаление — слово владельца | таблица ниже; `test_judgment_census.py` в DoD TD-15.1 |
| AR-4 без привязки к машине | истории без путей машины, людей и внутренних хостов | захват отказывает на остатке (K15) |

FR пройдены: FR-12 (детектор не читает слова человека/роли по списку фраз — правила чистки захвата ищут имена и хосты, не
смысл), FR-13 (закрытые словари — слои, вердикты, статусы, виды дверей, обязательное покрытие историй — в данных),
FR-28 (наблюдатель — измеритель: у него тест), FR-30 (истории английские: транслитерация при захвате), FR-31 (таймаут файла
в наблюдателе судится, не проход), FR-32/FR-33 (настоящий улов становится строкой, падающей до правки), FR-41, FR-57 (у
каждого отказа дверь), FR-58/P20 (ожидаемый исход истории — запись прогона и принятая поправка, не сегодняшний код), FR-59
(`enter` и READY не решают на неизвестном).

Проверки, которые спека добавляет или меняет (AR-29: какому владельцу служит, класс переписи):

| # | Проверка | Где | Владелец | Класс |
|---|---|---|---|---|
| K1 | файл `test_*.py` на диске вне обеих секций (после `enter`) — строка FAIL, файл всё равно идёт | `selftest.cmd_tests` | данные | xref |
| K2 | `--tests` пропускает карантин; `--quarantined` гоняет только его | `selftest.cmd_tests` | данные | не проверка (выбор) |
| K3 | keep содержит каждый файл, названный носителями пакета | `selftest.gate_named_files()` + строка `test_selftest_slow_tests.py` | данные | xref |
| K4 | `enter` отказывает до выполнения §C.2 усл. 1–8 | `tools/test_quarantine.py enter` | данные | presence/xref |
| K5 | коммит диапазона, правящий/удаляющий файл карантина, снимающий строку keep/quarantine руками, возвращающий файл из истории карантина в keep или добавляющий импорт kept → quarantined, без двери своего коммита — отказ | `tools/test_quarantine.py check` (forge-check) | данные | xref |
| K6 | READY TO DELETE = правила R1–R6 §D.3 по когорте | `status` | данные (входы — вердикты роли) | xref/presence |
| K7 | вердикт по красному: stale / real_catch / flaky | роль критического тира по диспатчу Lead, запись `judge` | суждение (принимает Lead) | — (не код) |
| K8 | `purge` без слова владельца — отказ | `purge --owner-word` | замысел | presence |
| K9 | исход фасета = `expected.json` истории | `scripts/tests/scenario_walk.py` | данные (ожидание = запись + принятая поправка) | тестовый код, вне переписи |
| K10 | папка фикстур удаляется на purge, только если её не называет ничто оставшееся | `purge` | данные | xref; ошибается в сторону СОХРАНЕНИЯ |
| K11 | файл из `pin_holds` не переводится | `enter` | данные (что пин — правило, решила роль TD-5.2 и критик TD-5.3) | xref |
| K12 | расписание с `QUARANTINE_WATCH=1` на ветке конфига видно через API | `enter` | данные | presence |
| K13 | истории вместе покрывают `story_coverage_required` | `enter` | данные (годность истории принимает Lead) | xref |
| K14 | `judge --verdict flaky` требует красное и зелёное того же файла на одном sha | `judge` | данные (сам вердикт — суждение) | presence |
| K15 | захват отказывает на совпадении правил чистки / пути / кириллицы | `tools/story_capture.py capture` | данные | presence (регулярки по строке) |
| K16 | наблюдатель не шёл на CI дольше 2 × max_gap — ALERT, `pull` выходит 3 | `status_line`, `pull` | данные | presence |
| K17 | фаза 2: `replaced_by` называет существующую строку keep, носитель файла больше его не называет | `enter --phase2` | данные (ловит ли замена тот же класс — суждение критика, принимает Lead) | xref |

Повторно используемые функции в более ответственной роли (правило 1 дизайнера):
- `selftest.slow_tests_updated(data, measured={}, ...)` в `purge` — снимать строки удалённых файлов. Допустимая ошибка: оставить
  лишнюю строку (её назовёт `package-full-report` как `missing`); недопустимо снять строку существующего файла. Неудобные
  входы: имя, отличающееся регистром от файла на диске (на Linux CI — отсутствует, верно); строка файла карантина, ещё лежащего
  на диске (purge зовёт функцию ПОСЛЕ удаления файлов); пустой `files` (без изменений).
- `install_paths.plugin_version()` + `install_paths._vtuple` как детектор РЕЛИЗА (был советчиком, стал входом гейта R2).
  Допустимая ошибка: НЕ засчитать релиз (тогда READY позже — безопасно); недопустимо засчитать то, чего не было. Неудобные
  входы: версия с суффиксом (`0.11.0-rc1`) — если `_vtuple` её не разбирает, версия «unknown», не считается; четыре копии
  `plugin.json` расходятся — читается только `.claude-plugin/plugin.json` через `plugin_version()`; версия уменьшилась
  (откат) — не новый релиз, считается только строго больше максимума виденных; та же версия повторно — один релиз.
- Строки `FAIL <name> — <detail>` харнесса (`harness.py:94`) как ПОДПИСЬ падения (B5). Допустимая ошибка: счесть подпись новой
  (лишний разбор — безопасно); недопустимо счесть новую проверку старой. Неудобные входы: имя проверки с изменчивыми данными
  (путь, число) — даёт «новую» подпись, разбирается заново (безопасная сторона); падение без строк FAIL (трассировка) — подпись
  `crash:<тип исключения>`; более 50 имён — первые 50 по сортировке и маркер `+N more` (новое имя за пределом 50 не видно —
  поэтому маркер с числом входит в подпись: изменилось число — подпись новая).

---

## §A. Слой сценариев

### A.1 Что такое история (P20 + FK-11/FK-13: ничего не выдумано, ничего из Jira)

ИСТОРИЯ — срез настоящего прогона фабрики на **синтетической** задаче: корень задачи, который записал прогон
(`state/events.jsonl`, `state/words/`, `state/driver-questions.jsonl` где есть, `pipeline.json` или события, из которых он
проецируется, `work/*`, `work/handoffs/*`), вычищенный (пути машины → `<stand>`/`<home>`, AR-4; имена людей, логины,
внутренние хосты и ключи по правилам чистки — K15), транслитерированный (FR-30, как `latin()` в
`fixtures/run-12586-gate-b/rebuild.py`), с пересчитанными хэшами тем же кодом (`event_store.content_hash`, привязки гейта A —
`Controller.gate_inputs()`), без ручной правки.

НЕ история: корпус Jira — всё, чей ключ задачи TP3*/внутренний (FK-13: `investigation-14857`, `TP1-13877`; решение
Lead: и `run-12586-*`); ГИБРИД — состояние из разных моментов (`run-12586-manual`, README: «THIS FIXTURE IS A HYBRID»;
`run-12586-red-then`: строки удалены руками, `controller/` срезан в другой момент, чем `work/`). Существующие оставляемые
тесты на этих фикстурах (`test_stage_joints_12586`, `test_exit_gate_digest_source`, `test_quality_demand`,
`test_s7_investigation_replay`, `test_gate_b_orders`) остаются в keep по своим основаниям (их называет `stage-joints.json`
или они сценарий прежнего вида), но историями слоя сценариев не считаются и в условие перевода не входят; их фикстуры заменит
синтетика при переезде ветки (GM2-7, t-1855:485, 489).

Что есть в репозитории (замер, §H): корней задач с `state/events.jsonl` — 5, все внутренние (`investigation-14857`,
`run-12586-gate-b`, `run-12586-manual`, `run-12586-red-then/controller`, `experiments/TP1-13877`); корней `LOCAL-*` в
репозитории нет (Glob `**/LOCAL-*/**/*.json*` — пусто; контроль той же формы `**/TP1-14857/**/events.json*` находит
файл). В `experiments/mybooks/thinking-roles/` — журналы прогонов и кейсы обходчика, не корни задач. Значит, синтетических
полных историй в репозитории сейчас, по этому замеру, нет; кандидаты — прогоны стенда MyBooks на копиях стенда вне
репозитория (`tools/dev.config.yaml` `stand_copy_root`), их меряет TD-15.0. Если полных синтетических наборов меньше трёх
или они вместе не покрывают требуемое (A.5), нужен узел TD-15.5r — запись истории живым прогоном на стенде (машина и стенд
владельца; развилка G-1).

Захват: `python tools/story_capture.py capture --source <корень задачи> --id <id истории> [--cut-after-seq N] [--drop <glob>]`
пишет `ai-packages/qa-factory/scripts/tests/fixtures/stories/<id>/` (вычищенная копия + `README.txt`: источник, срез, что
изменено, что отброшено) и `python tools/story_capture.py expected --id <id>` извлекает `expected.json` (A.2). Lead сверяет
`expected.json` с записью прогона и его принятым разбором и добавляет ПОПРАВКИ (A.2) — это «принял человек» P20 по
делегированию; поправка, меняющая исход, перечисляется владельцу в сообщении о переводе (§G0, п. 6).

### A.2 Файлы истории

`fixtures/stories/<id>/story.json` (пример — форма, не запись; конкретные стадии и двери берутся из отчёта TD-15.0):
```json
{"id": "local-1", "task": "LOCAL-1", "synthetic": true, "package_version": "0.10.8",
 "walk": [
   {"stage": "S3", "role": "qa-strategist", "door": {"kind": "exit_gate", "digest_file": "handbacks/S3.txt"},
    "facets": ["accepted", "handed"]},
   {"stage": "gateA", "door": {"kind": "gate", "cut_before_seq": 47}, "facets": ["question", "decision"]},
   {"stage": "S8", "door": {"kind": "delivery"}, "facets": ["delivery"]}],
 "not_walked": [{"stage": "S4", "facet": "handed", "why": "the run wrote no handoff form for S4"}]}
```
`synthetic: true` — обязательное поле; `enter` считает только такие истории. `root` (необязательно) — путь к уже лежащей
синтетической фикстуре (без второй копии). `expected.json` (извлечён, потом с поправками):
```json
{"stages": {
   "S3": {"outcome": "accepted", "handed": ["work/test-plan.json"], "source": "events.jsonl seq 32 accept"},
   "gateA": {"question_kind": "gate_a", "options": ["approve", "rework"], "decision": "approve",
             "source": "events seq 47 decision; state/words/gate-a-decision.txt"},
   "S8": {"delivery": "no", "source": "events seq 140; work/run-report.md verdict"}},
 "amendments": [
   {"stage": "S5", "field": "outcome", "recorded": "refused (digest form) x17", "expected": "accepted",
    "why": "the 17 digest refusals were a factory defect", "ref": "<finding path>", "accepted_by": "Lead, <date>"}]}
```
`variants.json` — ОДНА СТРОКА на добавленный случай (из найденного дефекта или враждебного ввода СНАРУЖИ: тикет, слова
человека, конфиг проекта, ответ хоста):
```json
[{"id": "run-witness-missing", "stage": "S5", "file": "work/automation-manifest.json",
  "op": "del", "pointer": "/run_witness", "expect": {"outcome": "refused", "names": "run_witness"}, "source": "<finding>"}]
```
Словарь `op` (закрытый, FR-13): `del`, `set` (с `value`), `replace_file` (с `with`: путь внутри папки истории), `words`
(заменить текст файла слов человека). Вариант применяется к КОПИИ мира и снимается после проверки.

### A.3 Что сценарий утверждает — и что нет (R1: двери без побочных эффектов)

Фасеты на проходимой стадии; виды дверей — закрытый словарь `DOORS` в `scenario_walk.py`:
- `accepted` / `refused` — дверь `exit_gate`: `exit_gate.all_errors(agent, task, digest, facts_text)`
  (`scripts/exit_gate.py:1763`) в процессе, на общем мире, на последнем принятом выходе стадии; `digest` — текст из
  `door.digest_file` истории (захват сохраняет текст сдачи; где он лежит в записи — TD-15.0 (f)); дверь `joint` — чистая
  проверка, которую называет строка `stage-joints.json` (как J1–J3 `test_stage_joints_12586.py`). Для `refused` сверяется
  вид/ключ отказа, никогда текст. `story_step.py finish` НЕ зовётся (он записал бы приёмку в мир, который уже её содержит).
- `handed` — на КОПИИ мира: `story_step.py start` роли следующей стадии проходит, и каждый файл, который называет форма
  передачи (`work/handoffs/<dispatch>.yaml`, `handoff_init.py`), существует и разбирается.
- `question` — на КОПИИ мира, срезанной до открытия гейта (`door.cut_before_seq`): функция, которая строит вопрос гейта (её
  называет TD-15.0 (g) — в пакете нет одной очевидной: кандидаты `controller._gate_questions_view`, `gate_brief.*`),
  даёт записанный `question_kind` и тот же набор закрытых токенов (равенство множеств, не текст).
- `decision` — на КОПИИ мира, срезанной до записанного решения: записанные слова человека (`state/words/*`) через ту же
  дверь (путь решения контроллера; функцию называет TD-15.0 (g)) дают решение с записанными токенами.
- `delivery` — `delivery_verdict.decide(kinds, doc)` (`scripts/delivery_verdict.py:119`); откуда берутся `kinds` и `doc` в
  записи — TD-15.0 (h); даёт записанное слово (yes / after_checks / no).

Фасет без носителя в срезе — `not_walked` со стадией, фасетом и причиной; печатается `NOTE <story>/<stage>/<facet>: not walked -- <why>`,
никогда не зелёный и не считается в покрытие (A.5).

Не утверждается никогда: текст сообщения, вопроса или отказа; порядок строк; время; деньги; промежуточные файлы, не названные
передачей; число событий; хэши, кроме стыков идентичности, которые проверяет сам гейт.

Почему только ПОСЛЕДНИЙ принятый выход: у артефакта один писатель (AR-14), его последний файл — последний принятый выход;
ранние отказанные попытки идут ВАРИАНТАМИ из записанного отказа.

Что слой не ловит по устройству (критик, ответ 1; честно владельцу в §G0): потерю поля в коде, который пишет артефакт между
стадиями (снимок, леджер, сводки) — обход начинается с ЗАПИСАННОГО выхода; состояние без хода (AR-25 — это детекторы фазы 2);
хосты, кроме записанного; онбординг, установку; редкие ветки, которых не прошёл ни один прогон; время и конкуренцию.

### A.4 Один мир на историю

`scripts/tests/scenario_walk.py` (модуль-помощник, не тест):
- `load_story(id) -> Story` читает `story.json`, `expected.json`, `variants.json`; битый файл — исключение `StoryError` с файлом и
  ключом; история без `synthetic: true` — `StoryError("not synthetic")`.
- `build_world(story) -> Path` копирует корень ОДИН раз в `harness.temp_dir()` как `<tmp>/project/qa-factory/artifacts/<task>/`,
  проецирует `pipeline.json` из событий, если его нет (`Controller._project_pipeline`, `controller.py:4624`).
- `copy_world(world, cut_before_seq=None) -> Path` — копия для фасетов с побочными эффектами (`handed`, `question`,
  `decision`), события обрезаются до `cut_before_seq`.
- `walk(story, world) -> list[Result]` — стадии в порядке `walk`, каждая проверка названа `<story>/<stage>/<facet>` (P16: красная
  строка называет историю и стадию), затем варианты `<story>/variant/<id>`.
- `run(story_id)` = load + build + walk + `harness.finish()`.
- `witness_for(paths) -> list[str]` (§A.6).

Тестовые файлы: по одному на историю, `scripts/tests/test_scenario_<id с _>.py`, тело = `scenario_walk.run("<id>")`. Цель по
времени: история ≤ 60 с на образе CI, слой ≤ 5 мин; судит только пайплайн.

### A.5 Покрытие, нужное до перевода (O-6 + B2)

`test-layers.json` `story_coverage_required` (данные, FR-13):
`["S0","S1","S2","S3","S4","S5","S6","S7","S8","S9","gateA.words","gateB.words","red_then"]`.
**Решение Lead 11.11.2026 (до слова владельца, обратимо): `S0` снят из списка в данных.** У S0 в записи прогона только
`stage_transition` — нет роли, диспатча, формы передачи и выхода, который обходчик мог бы пройти; все три захваченные истории
дали `not_walked` с этой причиной, и условие нельзя было выполнить ничем (FR-5). Вернуть `S0` — вместе с дверью обходчика для
предполётной проверки (`stage_done` S0), отдельным узлом.
Засчитывается: стадия `Sn` — хотя бы один фасет этой стадии пройден (не `not_walked`) в зелёной синтетической истории;
`gateA.words`/`gateB.words` — фасет `decision` гейта с записанными словами человека; `red_then` — история, где записанный
исход проверки Then красный и фасет стадии, которая это записала (S6 или S7), пройден. Код считает только пройденные фасеты;
годится ли история как представитель стадии — решает Lead при приёмке TD-15.5.k (AR-29).

### A.6 Как выбирается свидетель билдера (B7)

`python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <path> [<path> ...]` печатает по строке на файл:
- каждый `test_scenario_<id>.py`, у истории которого есть дверь, чей модуль в замыкании импортов содержит изменённый модуль
  (статический обход `ast` по `import X`/`from X import` внутри `scripts/`);
- каждую строку keep ЛЮБОГО слоя (включая gate_named, register, detector), чей `covers` содержит изменённый путь;
- для пути без совпадения — `no scenario or keep row covers <path>: run the whole scenario layer` и все `test_scenario_*.py`.
Путь вне `scripts/` (JSON справочника, текст роли) сверяется с `covers`; удалённый путь считается изменённым.

`covers` каждой строки keep TD-15.2 вычисляет из импортов файла (модули `scripts/`, к которым он обращается напрямую) плюс
файлы данных, которые файл открывает литералом (`references/*.json` и т. п.); ручное дополнение допустимо, снятие — нет.

---

## §B. Список остающихся (keep), фаза 2 и держатели пинов

### B.1 Файл

`ai-packages/qa-factory/scripts/tests/test-layers.json` — ОДИН файл (L-1), английский, читает только `selftest.test_layers()`:
```json
{"schema_version": 1,
 "note": "Which package test files run in the canon (keep) and which sit in quarantine (docs/TESTING.md; spec docs/tasks/specs/td-15-scenarios-quarantine.md). Read only by scripts/selftest.py test_layers(). quarantine and cohorts are written only by tools/test_quarantine.py; a keep row leaves only by that tool.",
 "layers": ["scenario", "data_join", "table", "register", "gate_named", "detector"],
 "enforce_listing": false,
 "story_coverage_required": ["S0","S1","S2","S3","S4","S5","S6","S7","S8","S9","gateA.words","gateB.words","red_then"],
 "keep": {
   "test_gate_preflight.py": {"layer": "gate_named", "why": "gate-registry G13", "covers": ["gate_preflight.py"]},
   "test_words_doors.py": {"layer": "detector", "why": "sole AR-24 detector (architecture.md:249)", "named_by": ["design/architecture.md:249", "docs/SIBLING_MAP.md:141"], "replaced_by": null, "covers": ["..."]}},
 "pin_holds": {"test_gate_brief_and_retro.py": "TD-5.2 inventory: 4 role-text pins not yet in role-rules.json"},
 "cohorts": {},
 "quarantine": {}}
```
Строка карантина (пишет `enter`): `{"cohort": "<pipeline_at_entry>", "entered": "2026-11-20", "release_at_entry": "0.10.9",
"commit_at_entry": "<sha>", "red_at_entry": false, "flaky_at_entry": false, "seconds": 12.4}` (`seconds` — из `slow_tests.json`
до его чистки, вес шарда наблюдателя, R3). Когорта (пишет `enter`): `"cohorts": {"<pipeline_at_entry>": {"entered": "...",
"release_at_entry": "...", "commit_at_entry": "...", "phase": 1, "replaced_by": {}}}` — у когорты фазы 2 `replaced_by`
отображает файл → строку keep.

Читатель `selftest.test_layers(path=None) -> dict`: файла нет — `{"keep": {}, "quarantine": {}, "pin_holds": {}, "cohorts": {},
"enforce_listing": False, "absent": True}` (мир до TD-15.2); битый — `TestLayersError` с одним предложением (main печатает,
выход 2), как `slow_tests()`. Отказываемые формы: ключ не голое имя `test_*.py`; файл в двух секциях (keep и quarantine);
слово слоя не из `layers`; строка keep с пустым `why`; строка `detector` без `named_by` или без ключа `replaced_by`; строка
карантина без `cohort`/`entered`/`release_at_entry` или с `cohort`, которого нет в `cohorts`; `pin_holds` с файлом, которого
нет на диске.

### B.2 Критерии (по порядку; решает первый, который выполнен)

1. gate_named — файл называет носитель, который читает код: `CONTRACT_TESTS`; `selftest --hooks` (`test_hooks_wiring.py`);
   строка `.gitlab-ci.yml`; `install_smoke.py`; `gate-registry.json` `test`; `stage-joints.json` `joint.test`; владелец
   фикстуры храповика AR-20 (`driver-layers.json` → `test_driver_layers.py`); строка DoD `plans/builder-rules.md` п. 7b
   (по типу правки: `test_audit_rules`, `test_hooks_wiring`, `test_null_outcomes`, `test_gate_registry`, `test_console_encoding`)
   и п. 7c (`test_story_run_words`, `test_driver_layers`).
1b. detector — файл называет как детектор/член оси носитель процесса: `design/architecture.md`, `design/factory-rules.md`,
   `docs/SIBLING_MAP.md` (любое упоминание — шире строк «Detector», ошибка в сторону сохранения), владелец члена оси 18
   (`fixtures/env-facts-baseline.json` → `test_state_portability.py`); плюс по критериям 2/4 без носителя: храповик
   «только сжимается» внутри файла и обход «строка реестра ↔ читатель» (их находит TD-15.0b). Слой `detector`, фаза 2.
   Решение Lead 11.11.2026 (критик темы 1, N3; узел t-2520): храповик, который НЕ назван ни одним носителем, остаётся
   строкой слоя `data_join` — слой `detector` требует `named_by` и `replaced_by` (`selftest.layers_problems`), а придумывать
   носитель ради метки нельзя. Оба слоя постоянные, на перевод в карантин метка не влияет. Так стоят пять файлов:
   `test_brief_pack_s5_plan`, `test_charters_s5_s9`, `test_file_lock`, `test_role_load`, `test_walk_plan_fields`.
2. register — обход реестра правил или мест, потеря которых молчалива (перепись AR-29, реестр правил ролей
   `test_role_rules.py`, классы владельца-человека, писатели артефактов).
3. scenario — обход записанных артефактов настоящих прогонов через двери стадий.
4. data_join — поле, которое пишет одна стадия, а читает другая; строка реестра и её читатель; перепись одного читателя/источника.
5. table — настоящая комбинаторика по списку Lead: разбор идентификаторов, ключи и хэши записей на дисках проектов, деньги,
   отказы безопасности (секреты, внешние записи, гарды), сам раннер канона и обходчик сценариев.
6. иначе — КАРАНТИН (фаза 1), если файл не в `pin_holds`.

`selftest.gate_named_files(extra_texts=()) -> set[str]` считает критерий 1 и часть 1b по носителям ПАКЕТА (`CONTRACT_TESTS`,
`gate-registry.json`, `stage-joints.json`, `install_smoke.py`, `driver-layers.json`, `design/architecture.md`,
`design/factory-rules.md` — имена по регулярке `test_[a-z0-9_]+\.py`, только существующие в `scripts/tests/`); носители ФОРДЖА
(`plans/builder-rules.md`, `.gitlab-ci.yml`, `docs/SIBLING_MAP.md`, `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md`) передаёт текстами
`tools/test_quarantine.py` — пакет не читает `docs/` (AR-4).

### B.3 Замеренные числа

| Множество | Файлов | Как замерено |
|---|---|---|
| на диске | **701** | Grep `files_with_matches` `.` glob `test_*.py` по `scripts/tests`, offset 650 → 51 |
| остаются (stay) | **69** | 71 имя проверено Glob по скобочному списку (найдены все 71) минус `test_story_version`, `test_driver_golden` (критик, ответ 2: «мелкая функция» / измеритель не уровня прогонов) |
| фаза 2 (`detector`) | **51** | 52 существующих файла, названных в `docs/SIBLING_MAP.md` (Grep `-o test_[a-z0-9_]+\.py` + Glob существования: 27 + 25), минус 14 уже в stay, минус `test_console_encoding` (строка DoD 7b → stay) = 37; плюс 9 только из `design/architecture.md` (Grep того же вида: `config_migration`, `story_run_s0`, `controller_blocks`, `friction`, `retro_numbers`, `gate_question_form`, `no_move_seam`, `state_exits`, `validators`); плюс 1 из `design/factory-rules.md` (`stand_lease`); плюс 4 по критериям 2/4 без носителя (`stage_cards`, `onboarding_markers`, `silent_passes` — храповики в файле; `role_commands` — реестр ↔ читатель) |
| фаза 1 (кандидаты) | **581** | 701 − 69 − 51 |
| из них держатся пинами до TD-5.3 | неизвестно до TD-5.2; верхняя граница по решету **242** (на всех 701, включая stay и фазу 2) | решето §4.6 TD-5 (обе альтернативы), Grep `files_with_matches` по `test_*.py`: 242; инвентаря TD-5.2 в `docs/tasks/handoffs/` нет (Glob `td-5*` пусто; контроль той же формы находит `t-1467-f6-42-test-volume.md`) |

PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md новых детекторов не добавляет (его имена — `test_story_step.py` как пример утечки,
l.369, остальные уже в stay или тесты форджа); `plans/builder-rules.md` кроме строк DoD называет `test_story_step.py`,
`test_probe_by_code_copy.py`, `test_arch_check.py` как историю/примеры, не как DoD — в критерий 1 не входят.

Импорты kept → quarantined: на старом списке критик насчитал 31 ребро (его AST-прогон); на новом списке не замерено —
печатает `enter --dry-run` («held by import»), его режет TD-15.8. С возвратом `test_controller_state`, `test_words_doors`,
`test_fixes_13797` в фазу 2 часть рёбер исчезает.

### B.4 Остаются (stay, 69) — по слоям

| Слой | Файлы (почему, если не очевидно) |
|---|---|
| gate_named (31) | `test_null_outcomes`, `test_gate_registry`, `test_stage_joints` (`CONTRACT_TESTS`); `test_hooks_wiring` (`--hooks`); `test_audit_rules` (`.gitlab-ci.yml`, 7b); `test_reinstall_equals_fresh` (`install_smoke.py`); `test_driver_layers` (AR-20, 7c); `test_story_run_words` (7c); `test_console_encoding` (7b, SIBLING:348); gate-registry `test`: `test_stand_identity` (G1), `test_execution_request` (G2, G4), `test_proof_level` (G5, G8), `test_node_ids` (G6), `test_s5_precheck` (G9), `test_window_record` (G10), `test_check_delivery` (G11), `test_gate_preflight` (G13), `test_environment_preparation` (G14), `test_baseline_contract` (G15), `test_oracle_provenance`, `test_exploratory_answers`, `test_story_run_s6`, `test_story_run_stand_identity`, `test_environment_record`, `test_probe_by_code_languages`, `test_story_step_start`, `test_branch_accounting`, `test_grounding_table`, `test_regression_scope`, `test_env_evidence`, `test_fit_targets` |
| scenario, прежний вид (5) | `test_stage_joints_12586`, `test_exit_gate_digest_source`, `test_quality_demand` (`stage-joints` `joint.test`); `test_s7_investigation_replay`; `test_gate_b_orders` — в условие историй не входят (A.1) |
| register (6) | `test_judgment_census` (AR-29, ось 18); `test_conductor_investigates_first` (AR-17 `SITES`, FR-48, PROCESS:1071; его K4 — стык данных по TD-5 §4.6, остаётся); `test_person_owned`, `test_person_owned_paths` (AR-17); `test_artifact_writers` (AR-14); `test_role_rules` (реестр правил ролей TD-5.1) |
| data_join (6) | `test_field_producers` (AR-21/22); `test_one_source_per_fact` (FR-10: согласованность пакета — причина исправлена по критику); `test_read_json` (AR-13 ось 16); `test_detector_verdict` (AR-18); `test_handoff` (AR-21); `test_open_list_fields` |
| table (21) | `test_grammar`, `test_case_id_form`, `test_local_keys`, `test_s0_key_form` (формы ключа на S0: разбор + закрытый вопрос; слой уточнён по критику), `test_task_root_parsers`, `test_event_store`, `test_release_fingerprint`, `test_task_price`, `test_cost_capture_tail`, `test_human_questions`, `test_run_forms`, `test_test_files`, `test_http_client`, `test_resolver`, `test_runtime_paths`, `test_stage_guard`, `test_external_writes`, `test_selftest_shard`, `test_selftest_slow_tests`, `test_selftest_ran_nothing`, `test_contract_slices` (генератор; слой уточнён по критику) |
| запланированы | `test_scenario_<id>.py` ×≥3 (scenario); `test_scenario_walk.py` (table: обходчик — часть раннера канона, крит. 5) |

Сомнительные строки ревизии 1 (`?`) — по умолчанию остаются (R8), кроме двух, которые критик отнёс к карантину.

### B.5 Фаза 2 (`detector`, 51) — что держит каждый и чем заменить

Колонка «заменён чем» в начале пуста у всех; файл переводится узлом TD-15.10.k (§C.3). «Носитель» — строка, где файл назван
(замер Grep `-o`, номера строк на дереве `wt-test-diet`).

| Файл | Носитель | Что держит |
|---|---|---|
| `test_controller_state` | SIBLING:125; architecture:256 | AR-25 (один из двух детекторов) |
| `test_state_exits` | architecture:256 | AR-25 (перечисление состояний из `controller.projection([])` в обе стороны) |
| `test_words_doors` | SIBLING:141; architecture:164, 249 | AR-24 единственный детектор |
| `test_no_move_seam` | architecture:192 | AR-17 |
| `test_controller_blocks` | architecture:109 | AR-9 (блоки против исходника в обе стороны) |
| `test_config_migration` | architecture:65, 67 | AR-3 единственный детектор |
| `test_state_portability` | SIBLING:217; ось 18 (`env-facts-baseline.json`, SIBLING:387); architecture:72 | AR-4, AR-20 |
| `test_story_run_monorepo` | SIBLING:259; architecture:72 | AR-4 |
| `test_codex_tool_guidance` | SIBLING:403; architecture:79, 164 | AR-5, ось 19 |
| `test_resume_story_isolation` | SIBLING:409; architecture:79 | AR-5, ось 20 |
| `test_story_run_s0` | architecture:86 | AR-6 (S0 чтение) |
| `test_friction`, `test_retro_numbers` | architecture:130 | AR-12 |
| `test_gate_question_form` | architecture:185 | AR-16 |
| `test_exit_gate_scope` | SIBLING:378; architecture:199 | AR-18 |
| `test_validators` | architecture:263 | AR-26 (правила C0 хука валидатора) |
| `test_bug_records` | SIBLING:154, 221; architecture:164, 270 | AR-27 |
| `test_hooklib_scan` | SIBLING:278; architecture:178 | ось гарда команд |
| `test_adapter_forms`, `test_assertion_detectors` | SIBLING:240, 278 / 148; architecture:51 | AR-1/AR-2 |
| `test_stand_lease` | factory-rules:432 | правило FR (аренда стенда) |
| `test_install_retire` | SIBLING:76 | ось установки |
| `test_sizing`, `test_onboarding_notes` | SIBLING:153 | ось онбординга |
| `test_triage_blocked` | SIBLING:154 | ось сортировки |
| `test_stand_gaps`, `test_protected_test_path`, `test_test_locations` | SIBLING:143, 240, 278 | оси путей тестов |
| `test_critic_rollcall_apply_fixes` | SIBLING:162 | — |
| `test_config_projection`, `test_case_key_identity_join`, `test_line_endings` | SIBLING:188, 189, 190 | — |
| `test_controller_task_flag` | SIBLING:220 | — |
| `test_guard_command_text`, `test_role_policy_reads` | SIBLING:278 | ось гарда |
| `test_cost_capture_role_gaps`, `test_dashboard_cost_gap_rows`, `test_cost_capture_start_turn`, `test_cost_capture_settled` | SIBLING:337–339 | ось денег |
| `test_fixes_13797` | SIBLING:402 («Analogs kept (queued)», не строка Detector — взят по правилу «любое упоминание») | ось 19 |
| `test_project_decisions_change_request` | SIBLING:413 | ось 21 |
| `test_host_adapter`, `test_dispatch_liveness` | SIBLING:425 | ось 22 |
| `test_driver_stop_record`, `test_hooklib_append_jsonl` | SIBLING:455 | — |
| `test_profile_reader` | SIBLING:459; храповик в файле (:565) | AR-20 |
| `test_dispatch_identity` | SIBLING:573, 577 | — |
| `test_stage_cards`, `test_onboarding_markers`, `test_silent_passes` | критерий 2 (храповики `NO_CARD` :39, :36, :1348) | AR-20 |
| `test_role_commands` | критерий 4 (каждая команда `references/role-commands.json` против читателя) | AR-9 |

TD-15.0b может предложить: (а) добавить в фазу 2 найденные обходы реестров без носителя; (б) перенести в фазу 1 упоминание
SIBLING_MAP, которое не детектор (цитируя строку). Решает Lead; по умолчанию файл остаётся в фазе 2 (безопасная сторона).

### B.6 Держатели пинов (`pin_holds`, B3)

Файл фазы 1 или 2 переводится, только когда каждый пин текста роли в нём — строка реестра `design/role-rules.json`
(слово владельца: «Пока реестр не принял правило, его старый пин не удаляется», `docs/TESTING.md:90`). Носитель — секция
`pin_holds` в `test-layers.json`: файл → одна строка причины. Её создаёт TD-15.2 из инвентаря TD-5.2
(`docs/tasks/handoffs/td-5-2-inventory.md`): каждый файл-кандидат (не stay), у которого инвентарь называет хоть один пин вида
«rule»; файл с строкой `none: <why>` в `pin_holds` не попадает. Строку снимает волна TD-5.3 тем же коммитом, что переносит
ключи файла в реестр (область TD-5.3 сужается до файлов `pin_holds`; пины в файлах stay остаются пинами и продолжают идти).
Как волна доказывает снятие: `python -B ai-packages/qa-factory/scripts/role_rules.py --check` без находок и в отчёте список
`<file>: <проверка/функция> -> <id реестра> | dropped:<вид> | red before` по каждому пину, который инвентарь называет в этом
файле; критик TD-5.3 сверяет список с инвентарём. После `enter` строки `pin_holds` только снимаются (K5).

---

## §C. Механика карантина

### C.1 Где живёт факт: манифест, не каталог (L-2)

Секция `quarantine` в `test-layers.json`; файлы остаются в `scripts/tests/<name>`. Причины (ревизия 1, подтверждены критиком):
тесты импортируют друг друга по родительскому каталогу; `slow_tests_diff` назвал бы переехавший файл `missing`; строки
`driver-layers.json` и глобы `plans/features.json` называют пути.

Инварианты (у каждого свой страж):
1. Канон не гоняет файл карантина — `selftest.cmd_tests` отфильтровывает строки `quarantine` ДО шардирования (`--tests`,
   `--fast`, `--shard I/N`, без флагов). Строки `test_selftest_shard.py`.
2. Шарды канона — чистая функция отфильтрованного списка и весов.
3. `slow_tests.json` согласован — `enter` снимает имена карантина из `files` тем же коммитом (сначала копирует секунды в строку
   карантина `seconds`); `slow_tests_updated`/`slow_tests_diff` пропускают имена карантина. Наблюдатель `--slow-tests` не кормит.
4. Носители (`CONTRACT_TESTS`, `gate-registry.json`, `stage-joints.json`, `driver-layers.json`, `install_smoke.py`,
   `.gitlab-ci.yml`, `design/*.md`, SIBLING_MAP, builder-rules) называют только оставшиеся: `enter` отказывает, если
   `gate_named_files(forge texts)` пересекается с переводимыми.
5. `TEST_TIMEOUTS` — `enter` не трогает (нужны наблюдателю); `purge` снимает строки удалённых.
6. Глобы `features.json`, строки `driver-layers.json`, `lint_ratchet`, `dup_ratchet`, перепись суждений — `enter` не трогает
   (файлы на месте); `purge` чистит (§D.6).
7. Помощники (`harness.py`, `story_run_common.py`, ..., все фикстуры) остаются до `purge`, решает K10.
8. Файл карантина не правится — K5 (§C.4).
9. Перевод — один обратимый коммит: `enter` готовит строки `quarantine` и `cohorts`, `enforce_listing: true` (первая когорта),
   чистку `slow_tests.json`; пишет сообщение коммита в `ci-out/quarantine-enter-msg.txt` и печатает строку `git commit -F`;
   коммитит Lead. Правки носителей §E — отдельный коммит Lead; откат = `git revert` обоих.

### C.2 Условия перевода фазы 1 (K4)

`python tools/test_quarantine.py enter --pipeline <id> --coverage-pipeline <id> [--dry-run]` отказывает (выход 1, причина и
дверь), пока не выполнены ВСЕ:
1. `test-layers.json` есть, разбирается, keep ≥ 1. Дверь: TD-15.2.
2. Истории (K13): ≥ `MIN_STORIES` (3, O-6) строк keep слоя `scenario` с именем `test_scenario_*.py`, у чьей истории
   `synthetic: true`; все PASS в пайплайне `<id>`; их пройденные фасеты вместе покрывают `story_coverage_required`. Отказ
   называет непокрытое (`missing coverage: S1, gateB.words`). Дверь: захватить/записать историю (TD-15.5.k / TD-15.5r).
3. `gate_named_files(тексты носителей форджа) ⊆ keep`, и ни один переводимый файл им не назван. Дверь: строка keep.
4. Пайплайн `<id>` шёл ровно на HEAD (`sha == git rev-parse HEAD`); его `ci-out/selftest.txt` (`package-full-report`) несёт
   `PASS tests: scripts/tests/<f>` на каждую строку keep и ни одного `FAIL tests:` строки keep. Чтение — функциями
   `tools/ci_read.py`. CI недоступен, токен отказан, артефакта нет — отказ (FR-59), дверь
   `rerun when CI is reachable: python tools/ci_read.py jobs <id>`.
5. Файл из `pin_holds` не переводится (K11) и перевод остальных не держит: он остаётся в каноне как записанный
   (`_listing_ok`: записанные = `keep` + `quarantine` + `pin_holds`), печать называет число `held by pins: P`. Решение Lead
   11.11.2026 (узел TD-15.6e, t-2357; прежний текст «ни один переводимый файл не в `pin_holds`» ставил весь перевод за
   волной TD-5.3 на 186 правил). Снятая волной TD-5.3 строка `pin_holds` делает файл незаписанным: ему нужна строка keep
   или вход следующей когортой.
6. Расписание (K12): `GET /projects/:id/pipeline_schedules` показывает активное расписание с `ref ==` `config.json` `branch` и
   переменной `QUARANTINE_WATCH=1`. Недоступно — отказ. Дверь: `ask the owner to create it: Settings -> CI/CD -> Schedules,
   cron "0 3 * * 1,4", branch <branch>, variable QUARANTINE_WATCH=1; then record it in docs/RUNBOOK.md section 7`.
7. Замер покрытия (B7): пайплайн `--coverage-pipeline` — задача `test-redundancy` с `REDUNDANCY_SCOPE=keep` (TD-15.6d) на
   коммите, чей набор keep равен набору keep HEAD; `enter` читает из его отчёта «covered lines» и печатает
   `canon after the move covers X of Y product lines (pipeline <id>)`, то же — в сообщение коммита. Нет замера — отказ.
8. Базовая линия (R7): последние 3 пайплайна `package-full-report` ветки (включая `<id>`) читаются; переводимый файл, красный
   хоть в одном, получает `red_at_entry: true`; красный и зелёный вперемежку — `flaky_at_entry: true`. Меньше 3 пайплайнов —
   отказ с дверью «run the full tier N more times».
Дверь по слову владельца (P13; слова владельца 11.11.2026 «не надо ждать, пайплайн после карантина поменяется, а расписание
ставим позже» и «не жди его, делай дальше как будто он зелёный»): `enter --owner-word "<слова>"` проходит РОВНО четыре проверки,
каждая печатается строкой `... -- passed by the owner's word: <слова>` и пишется в когорту (`owner_word`, `owner_word_gates`):
`schedule` (усл. 6); `red_keep` (усл. 4: красные и неизмеренные строки keep — `keep_fail_at_entry`, `keep_absent_at_entry`);
`head` (усл. 4: пайплайн не на HEAD — `pipeline_sha`); `coverage_keep_set` (усл. 7: замер на прежнем наборе keep —
`coverage_measured_on`). Остальное слово не проходит: истории PASS и покрытие стадий (усл. 2), носители (усл. 3), импорты
остающихся файлов, `pin_holds` (усл. 5), базовая линия (усл. 8), недоступный CI.
Печать: `quarantine enter: N files (L lines) to quarantine, K kept (by layer: ...); held by import: H (kept -> quarantined,
listed); held by pins: P; slow_tests.json -R rows; red at entry: A, flaky at entry: F; canon after the move covers X of Y lines;
prose mentions to fix by hand: <file:line>`; затем строка коммита. `--dry-run` печатает то же и ничего не пишет.

Временная грань: до TD-15.1 ничего не меняется. После TD-15.1, до TD-15.2 (файла нет): всё идёт, K1 выключен
(`absent: True`). После TD-15.2, до `enter`: строки keep есть, `enforce_listing: false` — всё идёт, K1 выключен. После
`enter`: карантин пропускается, K1 включён. После `purge` всех когорт: `quarantine: {}`, K1 остаётся включён.

### C.3 Фаза 2 — перевод детектора (K17)

`python tools/test_quarantine.py enter --phase2 <file> --replaced-by <keep row> --pipeline <id> [--dry-run]` отказывает, пока:
(а) `<file>` — строка keep слоя `detector`; (б) `<keep row>` — существующая строка keep другого слоя (сценарий/стык/таблица),
зелёная в пайплайне `<id>` на HEAD; (в) ни один носитель (§B.2, 1–1b) больше не называет `<file>` — то есть тот же
подготовленный коммит правит строку носителя (SIBLING_MAP, architecture.md, ...) на замену; (г) `<file>` не в `pin_holds`.
Пишет: строку `replaced_by` в keep (для истории), новую когорту `{"phase": 2, "replaced_by": {<file>: <keep row>}}`, строку
карантина, сообщение `quarantine-enter: phase2 <file> -> <keep row>`. Ловит ли замена тот же класс дефектов — суждение
критика узла TD-15.10.k, принимает Lead (AR-29); код проверяет только данные (а)–(г).

### C.4 Страж K5 (B6)

`python tools/test_quarantine.py check` в задаче forge-check (после `piles.py check`). Диапазон — от коммита, который ДОБАВИЛ
`ai-packages/qa-factory/scripts/tests/test-layers.json` (`git log --diff-filter=A --format=%H -- <path>`, последний в выводе),
до HEAD: база не зависит от `CI_COMMIT_BEFORE_SHA` и вида пайплайна. Файла нет — `no test-layers.json` и выход 0.

Каждый коммит диапазона судится СВОИМ сообщением (`git log -1 --format=%B <c>`):
- обычный коммит — по своему диффу с родителем; коммит слияния — по комбинированному диффу (`git diff-tree --cc`), то есть
  только по правкам разрешения конфликта; изменения, принесённые вторым родителем, судятся в их собственных коммитах (они в
  диапазоне `rev-list`);
- изменение, переименование или удаление пути, который на родителе (на любом родителе — для слияния) — строка `quarantine`, →
  отказ, если в сообщении коммита нет `quarantine-edit: <file> -- <reason>` или коммит не `quarantine-purge: <cohort>`;
- секции `test-layers.json` на коммите против родителя (для слияния — трёхсторонне, по базе слияния B: строка keep или `quarantine`, что была в B и пропала в результате, снята слиянием, если только хоть один родитель уже её не имел — её снял и судил коммит того родителя; строка, которой нет в B, но которая есть у какого-то родителя, обязана быть в результате, иначе снята слиянием; файл-строка `quarantine`, чей блоб в результате отличается от блоба у родителя, где строка есть, требует `quarantine-edit:` в сообщении слияния, если только другой родитель, имевший строку и в B, не принёс тот же блоб; нет базы слияния — объединение строк родителей): снятая строка
  `quarantine` без `quarantine-purge:` → отказ; добавленная строка `quarantine` без `quarantine-enter:` → отказ; снятая строка
  keep без `quarantine-enter:` (переведена) или без `keep-drop: <file> -- <reason>` с удалением самого файла тем же коммитом →
  отказ; строка keep с именем, которое было в `quarantine` на ЛЮБОМ коммите диапазона (история `git log -p -- test-layers.json`)
  → отказ без двери (из карантина не возвращаются); добавленная строка `pin_holds` после первого `quarantine-enter:` → отказ;
- новое ребро импорта kept → quarantined (статический дифф импортов `ast`) → отказ, дверь
  `quarantine-import: <kept file> -> <quarantined file> -- <reason>`.
Прошлое нарушение, уже в истории: дверь — строка `quarantine-accept: <sha> -- <reason>` в любом ПОЗДНЕЙШЕМ коммите диапазона
(как `merge-accepts:` журнала); без неё нарушение красит каждый следующий прогон.
`commit_at_entry` когорты не предок HEAD (история переписана) → отказ, дверь `python tools/test_quarantine.py enter --rebase-entry
<cohort> <new sha>` (пишет новый `commit_at_entry`, сообщение `quarantine-enter: rebase <cohort>`).
Копия как pre-commit хук — по желанию, ставит Lead (правило файлов принуждения).

---

## §D. Наблюдатель и оповещение

### D.1 Где расписание и как наблюдатель узнаёт о релизе (B4, O-3)

Конфиг форджа `plans/test-quarantine/config.json` (пишет Lead руками; читает только `tools/test_quarantine.py`):
`{"ci": "gitlab", "branch": "<ветка карантина>", "cron": "0 3 * * 1,4", "max_gap_days": 4, "schedule_variable": "QUARANTINE_WATCH"}`.
`branch` — ветка, на которой идёт канон пакета этой работы (рекомендация на момент записи: `experiment/thinking-roles`,
куда сливается `test-diet`; `main` переехал на GitHub). `cron` — понедельник и четверг 03:00 (O-3: два раза в неделю);
промежутки 3 и 4 дня → `max_gap_days: 4`.

Расписание пайплайна GitLab создаёт владелец руками (Settings → CI/CD → Schedules: cron из конфига, ветка `branch`, переменная
`QUARANTINE_WATCH=1`). Запись о нём — строка `docs/RUNBOOK.md` §7 (правка Lead, §E): «Расписание наблюдателя карантина: id <n>,
ветка <branch>, cron `0 3 * * 1,4`, переменная `QUARANTINE_WATCH=1`, создала <кто, дата>». `enter` проверяет его через API
(§C.2 усл. 6).

`.gitlab-ci.yml` (и золото `tools/test_ci_layout.py`, тем же коммитом):
- `quarantine-watch`: stage nightly, `parallel: 2`, `needs: []`, `allow_failure: true`, timeout 3h. Правила:
  `if: $CI_PIPELINE_SOURCE == "schedule" && $QUARANTINE_WATCH == "1"`;
  `if: ($CI_PIPELINE_SOURCE == "web" || $CI_PIPELINE_SOURCE == "api") && $QUARANTINE_WATCH == "1"`;
  `if: $CI_PIPELINE_SOURCE == "push" && $CI_COMMIT_BRANCH == "<branch>"` с `changes: [ai-packages/qa-factory/.claude-plugin/plugin.json]`
  — прогон после каждого релиза (версия пакета меняется в этом файле), без кнопки. Литерал ветки равен `config.json` `branch`
  — строка таблицы `tools/test_test_quarantine.py` сверяет их (стык данных).
  Скрипт: `python -B scripts/selftest.py --quarantined --jobs 4 --shard "$CI_NODE_INDEX/$CI_NODE_TOTAL" --watch-out "$CI_PROJECT_DIR/ci-out/quarantine-watch-$CI_NODE_INDEX-of-$CI_NODE_TOTAL.json" || true` (из каталога пакета, как соседние задачи).
- `quarantine-watch-report`: stage report, `needs: [quarantine-watch]`, `when: always`, `allow_failure: true`, те же правила:
  `python tools/test_quarantine.py ci-summary --from "ci-out/quarantine-watch-*.json" --out ci-out/quarantine-watch.json`;
  артефакт 2 недели.
- Задачи `package-full`, `install-smoke`, `package-full-report`, `board-check` (если есть), `crap-measure` получают в правило
  `schedule` условие `&& $QUARANTINE_WATCH != "1"` — расписание наблюдателя не тянет за собой полный уровень.

`selftest.py --quarantined` (TD-15.1): только строки карантина; веса шардов — поле `seconds` строк карантина (R3), без поля —
вес по умолчанию; `--watch-out <path>` пишет `{"sha", "package_version", "shard": "I/N", "expected": [имена шарда],
"files": {name: {"status": "green|red|timeout|ran_nothing|missing", "seconds": s, "fails": [≤ 50 имён FAIL, по 160 знаков,
+ маркер "+N more"], "crash": "<последняя строка трассировки, 200 знаков>"}}}`. Выход 0 всегда с `--quarantined` (замер); сбой
самого раннера — 2.

`ci-summary`: объединяет шарды; `complete: true` только если есть все шарды, объединение `expected` равно множеству строк
карантина на этом sha (читается из `test-layers.json` чекаута CI через `selftest.test_layers`) и у каждого ожидаемого есть
результат; иначе `complete: false`, недостающие — `not_run`. В записи: `pipeline`, `source` (`$CI_PIPELINE_SOURCE`),
`created_at`, `sha`, `package_version`.

### D.2 `pull` — вытяжка и два возраста (B4)

`python tools/test_quarantine.py pull [--pipeline <id>]` (форж):
- спрашивает CI о пайплайнах ветки `config.branch` любого источника (schedule, web, api, push) с задачей
  `quarantine-watch-report`, новее последнего записанного; по каждому скачивает `ci-out/quarantine-watch.json` и дописывает в
  `plans/test-quarantine/watch.jsonl` строку `{"kind": "run", "pipeline", "source", "created_at", "sha", "package_version",
  "complete", "files"}` (пайплайн уже записан — пропуск; идемпотентно);
- всегда дописывает строку `{"kind": "pull", "at": <сейчас>, "ci": "ok|unreachable|token_refused", "newest_watch_pipeline":
  <id|null>, "newest_watch_at": <created_at|null>}` — время вытяжки и время последнего прогона наблюдателя на CI РАЗДЕЛЬНО;
- коды выхода: 0 — записано или нечего; 3 — наблюдатель не шёл на CI дольше `2 × max_gap_days` (8 дней) от момента вытяжки
  (или ни разу после входа, если вход старше 8 дней): печатает ALERT-строку §D.5; 1 — CI недоступен или токен отказан (строка
  `pull` с `ci: unreachable|token_refused` всё равно пишется); 2 — ошибка вызова.
Lead гоняет `pull` при утреннем чтении ночного (builder-rules 7b) и коммитит строки.

### D.3 Правила удаления как данные (K6; O-1, O-2, O-5)

Наблюдение = пара (файл, подпись) в ПОЛНОМ прогоне, где статус не `green`. Подпись: отсортированные имена FAIL (до 50 + маркер);
красное без строк FAIL — `crash:<тип>`; `timeout`; `ran_nothing`; `missing`. `not_run` — не наблюдение (прогон неполный).

`status` считает READY ПО КОГОРТЕ, если ВСЕ:
- **R1** в когорте ≥ 1 строка карантина;
- **R2 (O-1: два релиза)** пусть V0 = `release_at_entry` когорты; релизы = различные версии `.claude-plugin/plugin.json` на
  первородительской истории ветки после `commit_at_entry`, строго больше V0 и строго больше каждой предыдущей (по `_vtuple`);
  R_2 — вторая такая версия. Нужен ПОЛНЫЙ прогон наблюдателя, чей `package_version ≥ R_2`. (Релиз = смена версии на ветке;
  опубликованность в `QAFactory` код не видит — это приближение, названное владельцу в §G0.)
- **R3** ноль неразобранных наблюдений по файлам когорты во всех полных прогонах после `commit_at_entry` (O-1: «все покраснения
  разобраны»);
- **R4** ноль противоречивых вердиктов (два вердикта на один ключ с разным `verdict` без цепочки `--supersede`; одинаковые
  строки — один вердикт);
- **R5** у каждого `real_catch` есть строка `land` (O-1/O-2: «каждый настоящий улов перенесён»);
- **R6** ни один файл когорты не импортирует оставшийся файл (`held_by_import` пуст).
Срока нет ни в одном правиле (O-5). Настоящий улов не сбрасывает счёт релизов (O-2). Неудачные правила печатаются по одному.
Неизвестное (нечитаемые `watch.jsonl`/`verdicts.jsonl`/`plugin.json`, нечитаемая история ветки) — `unknown (<reason>)`, никогда
READY (AR-28). Дубли строк `run` с тем же `pipeline` (две сессии вытянули одно и то же) — одна (R5 критика).

### D.4 Разбор красного (роль, не код — AR-29; B5)

Неразобранное наблюдение — то, которое не покрыто вердиктом. Вердикт пишется на ключ (файл, подпись, пайплайн первого
наблюдения):
`python tools/test_quarantine.py judge <file> --pipeline <id> --verdict stale|real_catch|flaky --by <tier> --reason "<one line>" [--finding <path>] [--task <t-NNN>] [--supersede "<why>"]`
— подпись берётся из записи этого пайплайна (не вводится руками); строка в `plans/test-quarantine/verdicts.jsonl`
`{ts, file, signature, pipeline, verdict, by, reason, finding, task}`. Отказы: `real_catch` без `--finding` (дверь: файл
находки в кучке, PROJECT.md «Командная работа» п. 2); `flaky` без красного И зелёного этого файла на одном и том же `sha` в
`watch.jsonl` (K14; дверь: `retry the quarantine-watch job of pipeline <id> (GitLab: Retry), then pull`); второй вердикт на тот же
ключ без `--supersede`.

Покрытие позднейших наблюдений: вердикт V покрывает наблюдение (тот же файл, подпись S, пайплайн P), если имена S ⊆ имён
подписи V и: V = `stale` или `real_catch` — без доп. условий; V = `flaky` — только если у файла есть и зелёный результат на
`sha` пайплайна P. Новое имя проверки в подписи — новое неразобранное наблюдение при любом виде вердикта.

`status` печатает `blind: N files` — файлы, у которых все наблюдения покрыты `stale` и которые с момента вердикта ни разу не
были зелёными (их сигнал на настоящий улов ослаблен: новое имя проверки всё ещё видно, падение уже упавшей проверки — нет).
READY это число не блокирует; оно входит в строку READY и в сообщение владельцу.

Цена разбора (R6): один диспатч роли критического тира на одну вытяжку со всеми новыми наблюдениями: сначала массовый проход по
списку (файл, имена проверок, диапазон коммитов `git log --oneline <prev green sha>..<sha> -- ai-packages/qa-factory`), файл
открывается только там, где имён недостаточно; потолок — 30 наблюдений на диспатч, остаток — следующий. Оценка (не замер):
при двух прогонах в неделю и диапазоне 3–4 дня — единицы новых наблюдений на прогон после первой волны; первая волна после
перевода (законные правки уже накопились) может дать десятки.

Настоящий улов (O-2): (1) ALERT-строка каждой сессии до `land`; (2) файл находки в кучке; (3) случай становится строкой
`variants.json` / поправкой `expected.json` / строкой таблицы, падающей до правки (FR-32) — узел записывает
`python tools/test_quarantine.py land <file> --pipeline <id> --commit <sha>`; (4) Lead сообщает владельцу в тот же ход, когда
строка появилась впервые; (5) счёт релизов продолжается; файл в keep не возвращается (K5).

### D.5 Каналы — кто что печатает (ASCII; точные тексты)

1. Хук SessionStart каждой сессии форджа — `tools/session_context.py`, новая `test_quarantine_line(root) -> list[str]`,
   вызывается в `build_context_lines` сразу после `last_calibration_line`; импортирует `tools/test_quarantine.status_line(root)` в
   try; исключение → `TEST QUARANTINE: unavailable (<reason, 120 chars>)`. Строки (по одной на когорту + ALERT отдельными
   строками ПЕРЕД ними; длина ≤ 240):
   - нет `test-layers.json` или карантин пуст: строк нет;
   - ожидание: `TEST QUARANTINE: 581 files since 2026-11-20 (cohort 1, entered at 0.10.9); releases since: 1 of 2 (0.11.0); watch ran 2026-11-24 (1 d ago), pulled 2026-11-24 (1 d ago); 7 red, 2 unexamined, blind 1 -- delete when: complete watch on the 2nd release + 0 unexamined + every catch moved`
   - не вытянуто (вытяжка старше `max_gap_days`): та же строка с `pulled 2026-11-17 (7 d ago) -- run: python tools/test_quarantine.py pull`
   - последняя вытяжка не достучалась: `...; last pull 2026-11-24 could not reach CI (unreachable)`
   - неполные прогоны: `...; last 3 watch runs incomplete (not_run files) -- see the quarantine-watch job`
   - релиз без прогона (версия HEAD ветки > максимума версий полных прогонов): `...; release 0.11.1 has no complete watch run yet -- start it: web pipeline with QUARANTINE_WATCH=1 on <branch>`
   - READY: `TEST QUARANTINE: READY TO DELETE cohort 1 -- 581 files since 2026-11-20; complete watch on 0.11.1 (2nd release since 0.10.9); every red examined (5 stale, 1 flaky, 1 real catch moved); blind 3. Tell the owner; on her word: python tools/test_quarantine.py purge --cohort <id> --owner-word "<who, date>"`
   - ALERT улова: `TEST QUARANTINE ALERT: real catch 2026-11-25 -- test_x.py: <reason, 100 chars> (finding <path>); its case is owed as a scenario/table row -- tell the owner`
   - ALERT наблюдателя (K16; от последней удачной вытяжки до `newest_watch_at` > 8 дней, или прогонов ни разу и вход старше 8 дней): `TEST QUARANTINE ALERT: the watch has not run on CI for 9 d (last 2026-11-15, as of pull 2026-11-24) -- tell the owner: the schedule on <branch> is missing or failing (docs/RUNBOOK.md section 7)`
   - неизвестно: `TEST QUARANTINE: status unknown (<reason>)`
   Lead сообщает владельцу в чате в тот же ход, когда ALERT или READY появились впервые (O-4 + «сообщи мне»); эта обязанность
   — в host-адаптации 12 `CLAUDE.md` (§E). Строки читают только локальные файлы — работают без сети.
2. Сводка задачи CI — `ci-summary` печатает
   `quarantine watch <sha8> (package 0.10.9, pipeline <id>, source schedule): 581 files -- 570 green, 9 red, 2 timeout, 0 ran nothing, 0 missing, 0 not run; complete: yes`,
   затем по строке на незелёный: `  red: test_x.py  <first FAIL name, 160 chars> (+N more)`, затем
   `examine in a forge session: python tools/test_quarantine.py pull, then status`.
3. Чек-лист релиза — `docs/RUNBOOK.md` §4, новый пункт (правка Lead, §E): «**Карантин тестов при релизе**: прогон наблюдателя
   на новой версии запускается сам (push-правило на `plugin.json`); после публикации — `python tools/test_quarantine.py pull`
   и `status`. Неразобранные красные релиз не держат; полный прогон на втором релизе после входа — условие удаления (спека
   td-15 §D.3).»
   `status` (полный) печатает R1–R6 по когорте с pass/fail, наблюдения, вердикты, `blind`.

### D.6 Purge (только по слову владельца)

`python tools/test_quarantine.py purge --cohort <id> --owner-word "<who, date>" [--dry-run]`: отказ, если когорта не READY или
слово пустое (K8; слово копируется в сообщение коммита и в `verdicts.jsonl` строкой `purge`). Затем одним подготовленным
коммитом: удаляет файлы когорты; удаляет папки `scripts/tests/fixtures/`, которых не называет литералом ни оставшийся тест, ни
оставшийся помощник, ни история, ни `stage-joints.json` `fixture`, ни реестр (если оставшийся файл строит путь фикстуры
динамически — удаление фикстур ПРОПУСКАЕТСЯ целиком и кандидаты перечисляются, K10); удаляет помощники, которые больше никто
из оставшихся не импортирует (транзитивно); снимает строки когорты из `quarantine` и саму когорту; `TEST_TIMEOUTS` — снимает
записи удалённых файлов по `ast`-диапазонам (сбой разбора или перекрытие — отказ со списком, дверь: снять руками в том же
изменении, `--registries-done`); `slow_tests.json` — `slow_tests_updated(data, {}, ...)`; `driver-layers.json` — строки
`source_readers`/`source_mentions` удалённых файлов (AR-20, названо); `plans/features.json` — глобы, буквально равные
`scripts/tests/<удалённый файл>`; печатает результат `python tools/lint_ratchet.py --check`. Сообщение несёт
`quarantine-purge: <cohort>` (дверь K5). Печать: `quarantine purge: N test files deleted (L lines), F fixture folders deleted
(S kept: used by ...), H helpers deleted; registries: TEST_TIMEOUTS -a, slow_tests.json -b, driver-layers.json -c, features.json -d;
still named in text: <file:line>; commit: git commit -F ci-out/quarantine-purge-msg.txt`. Откат — `git revert`.

### D.7 Временная грань всего §D

| Мир | строка сессии | наблюдатель | status | purge |
|---|---|---|---|---|
| до `test-layers.json` | нет | задачи нет / `--quarantined` гоняет 0 файлов, пустая запись `complete: true` | `no quarantine` (выход 0) | отказ: нечего |
| keep есть, до `enter` | нет | 0 файлов, `complete: true` (ожидалось 0) | `no quarantine` | отказ |
| до `config.json` | — | — | `enter` отказывает (дверь: записать конфиг) | — |
| после `enter` | ожидание/ALERT/READY | по расписанию и после релиза | R1–R6 по когортам | отказ до READY + слова |
| после purge всех когорт | нет | 0 файлов (задачу может снять Lead) | `no quarantine` | отказ |

---

## §G0. Для владельца — что перестаёт проверяться и что взамен (B7)

Простыми словами, числа замерены, оценки помечены.

1. **Сейчас** канон гоняет все 701 тестовый файл пакета.
2. **После первого шага** канон гоняет 120 файлов: 69 остаются насовсем (их называет гейт или они слой «стык / таблица /
   реестр») и 51 детектор, которые уйдут позже и только по одному, когда для каждого найдётся замена (вторая фаза). Плюс
   истории сценариев (не меньше трёх). В карантин уходит до 581 файла — меньше на те, что держат пины правил ролей до
   переноса в реестр (сколько — скажет инвентарь TD-5.2).
3. **Покрытие кода.** Замер TD-12 (пайплайн 8069240): тесты покрывали 157 856 строк кода пакета. Оставшиеся 120 файлов
   покрывают **не меньше 49 476 строк (31,3 %)** — это нижняя граница (сумма «жадного вклада» этих файлов из таблицы B отчёта;
   на деле больше, потому что вклад засчитан только первому файлу). Файлам первой фазы жадный порядок приписывает 108 362 строки
   (68,7 %) — это ВЕРХНЯЯ граница того, что может потемнеть, не само число. Строк, которые покрывает только один файл, во всём
   наборе 37 929 (`docs/tasks/test-diet.md`, срезы по времени); сколько из них у карантина, отчёт по файлам не говорит. **Точное
   число** — замер на CI до перевода (узел TD-15.6d); без него перевод не начнётся, и Lead покажет это число до перевода.
4. **Крупнейшие уходящие** (жадный вклад, строк): `test_story_run_delivery_c` 30 570 (19,4 % — доставка S8 через драйвер),
   `test_gate_brief_and_retro` 7 217 (держится пинами до переноса в реестр), `test_story_run_s7_live` 5 608, `test_codex_host` 3 196,
   `test_probe_by_code` 2 984, `test_story_run_loop_b` 2 409, `test_collect_pack` 2 238, `test_report_facts` 1 982, `test_brief_pack`
   1 929, `test_run_suite_mine` 1 562.
5. **Какие классы дефектов перестают ловиться в день перевода:** цикл драйвера вне S6, идентичности стенда и слов; доставка S8
   (семейство `delivery_c`); адаптер тикета (`test_ticket_adapter`; чтение S0 через драйвер остаётся во второй фазе); хост Codex
   (`test_codex_host`; правило инструментов Codex остаётся); онбординг вне детекторов; редкие ветки, которых не прошёл ни один
   записанный прогон. Остаются: детекторы инвариантов AR-3, AR-9, AR-17, AR-24, AR-25, AR-26 и все 38 детекторов карты осей,
   ранее попадавших в карантин.
6. **Что дают сценарии взамен:** три и более синтетические истории MyBooks, вместе проходящие S0..S9, слова гейтов A и B и
   один красный Then; каждый будущий дефект — строка в истории, падающая до правки. Не ловят по устройству: потерю поля в коде
   между стадиями, состояние без хода, другой хост, установку. Поправки Lead, меняющие исход истории, перечисляются в сообщении о
   переводе.
7. **Чего стоит ждать:** до удаления 581 мёртвый файл едет в каждом релизе (отпечаток релиза их покрывает). Наблюдатель — два
   раза в неделю; цена прогона — оценка, не замер: ~110 минут счёта раннеров GitLab за прогон (основа: 12 565 с под coverage на
   705 файлов в TD-12; без coverage меньше). Разбор красного — работа роли критического тира, первые недели десятки
   наблюдений (оценка).
8. **Когда вы узнаете:** строка в начале каждой сессии; сразу — если карантин поймал настоящий дефект; сразу — если наблюдатель
   перестал идти больше 8 дней; READY — когда прошёл полный прогон на втором релизе после входа и всё разобрано. «Релиз» код
   видит как смену версии пакета на ветке карантина, а не как публикацию в QAFactory (приближение; см. G-2).

---

## §E. Носители правил, которые Lead правит при посадке (здесь не пишутся)

| Носитель | Сейчас | Изменить на |
|---|---|---|
| `plans/builder-rules.md` 7b | «тестовый файл изменённого модуля (при разделённых файлах — …)» | «файлы, которые печатает `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <пути owns>` (истории и строки keep из `scripts/tests/test-layers.json`, включая тест гейта), и ключи своего DoD. Файл карантина билдер не запускает, не чинит и не правит.»; строка `test_console_encoding.py` по типу правки остаётся (файл в stay) |
| `plans/builder-rules.md` 7d | «новый тестовый файл только у нового скрипта и не дольше 10 с; … Покрасневший пин удаляется, а не чинится.» | «новый тестовый файл не создаётся: случай — строка `variants.json` истории или строка таблицы/стыка своего слоя; файл у нового скрипта — только со строкой keep (слой и причина, их судит критик), не дольше 10 с. Покрасневший пин удаляется, а не чинится. Файл карантина не запускается, не чинится и не правится.» |
| `tools/tests/test_role_carriers_one_owner.py` | якорь `"Покрасневший пин удаляется, а не чинится"` | якорь `"Файл карантина не запускается, не чинится и не правится"` |
| `docs/tasks/critic-diff-brief.md` l.11 (два слоя) и q.5 | «the changed module's test file plus the DoD keys»; q.5 «… A missing pin is NOT a finding.» | l.11: «the files `scenario_walk.py --witness-for <owns>` prints plus the DoD keys»; q.5 + «A new test file with no keep row, or a keep row whose layer/why does not hold — finding; an edit to a quarantined file without a `quarantine-edit:` reason that holds — finding; a phase-2 move whose replacement does not catch the detector's class — finding.» |
| `CLAUDE.md` host adaptation 11 и правило 4 политики («must cover the test FILE that judges each owned path») | — | host adaptation 12 дополняется: «Tests outside the three layers are QUARANTINED (`ai-packages/qa-factory/scripts/tests/test-layers.json`): not run in the canon, not repaired, not edited; the witness of a change is what `scenario_walk.py --witness-for` prints — this overrides host adaptation 11 and rule 4's 'test FILE that judges each owned path' and rule 11's 'AT and BEYOND' and 'SCOPE CEILING' in this repository (the policy block is re-synced whole, never hand-edited): a boundary from OUTSIDE input is a scenario variant row; an internal boundary gets no test. When the SessionStart line says `TEST QUARANTINE ALERT` or `READY TO DELETE`, the Lead tells the owner the same turn (spec td-15).» |
| `.claude/agents/builder.md` правило 4 | «Its scope in this repository: `plans/builder-rules.md` 7b (D-0056).» | «… 7b (D-0056) — the files `scenario_walk.py --witness-for <owns>` prints; a quarantined test file is never run or edited.» |
| `.claude/agents/designer.md` правило 1 | «… verification scope in this repository is `plans/builder-rules.md` 7b.» | «… 7b: the DoD names `scenario_walk.py --witness-for <owns>`; a DoD never asks for a new test file outside the keep rows of `test-layers.json`; a new case is a variant/table row.» |
| `PROJECT.md` «Как принимается изменение пакета» п. 2 | «Объём проверки билдера и канон пачки — D-0056 (…)» | + «Канон гоняет только раздел `keep` из `scripts/tests/test-layers.json`; карантин гоняет задача `quarantine-watch` по расписанию два раза в неделю и после релиза; удаление — по условию спеки td-15 §D.3 и только по слову владельца.» |
| `docs/TESTING.md` «Карантин старых тестов» и «Кто что делает» (l.115 «свидетель — прогон файла области», l.117 вопрос 5) | — | носитель `test-layers.json`, строка `TEST QUARANTINE`, `status`; l.115: «свидетель — то, что печатает `scenario_walk.py --witness-for`»; l.117: «ловит ли строка сценария/таблицы узла тот дефект …» |
| `docs/RUNBOOK.md` §4 | — | пункт §D.5 (3) |
| `docs/RUNBOOK.md` §7 | — | строка о расписании наблюдателя (§D.1) |
| `design/architecture.md` | детекторы фазы 2 — без изменений (они остаются); AR-20 Carriers | + «`scripts/tests/test-layers.json` `quarantine`, `pin_holds` (shrink-only)»; строки детекторов меняются только в коммитах фазы 2 (§C.3) |
| `docs/SIBLING_MAP.md` ось 18 | — | + `quarantine` и `pin_holds` как члены (проверка изменения AR-20); строки детекторов — только в коммитах фазы 2 |
| `references/gate-registry.json` `source_freshness.exempt_reason` | «Pinned by test_source_preflight.py and test_lifecycle_integration.py.» | «… (quarantined, TD-15).» |
| `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md` | — | проверка: возраст наблюдателя на CI ≤ 8 дней, неразобранные наблюдения старше 7 дней, неперенесённые уловы, число `blind` (правило 10 (c): детектор механизма) |
| `docs/tasks/specs/td-5-role-rules-register.md` §7.3 | owns волны: её тестовые файлы и `<REG>` | + строки `pin_holds` своих файлов в `test-layers.json` (снимаются тем же коммитом); область волн — файлы `pin_holds` |

---

## §F. Узлы

Общее для узла-билдера: given — `ai-packages/qa-factory/design/factory-rules.md` целиком, `plans/builder-rules.md`, `docs/TESTING.md`,
эта спека; пакет английский (FR-30); каталог шелла не меняется; без долгих локальных прогонов (не `selftest.py` целиком, не
`test_story_run_*`, не медленные файлы; канон — пайплайн CI ветки); отчёт по правилу 7 `.claude/agents/builder.md` с проходом FR и
строками `architecture:`/`judgment:` для коммитов пакета. Свидетель — только файлы DoD узла. `<wt>` = `D:/ws1/wt-test-diet`,
`<pkg>` = `<wt>\ai-packages\qa-factory`.

| Узел | Тир | Owns (абсолютные) | Зависит | Волна |
|---|---|---|---|---|
| TD-15.0 носители историй | scout (Sonnet) | отчёт `<wt>\docs\tasks\specs\reports\td-15-0-story-carriers.md` | — | 1 |
| TD-15.0b обходы реестров | scout (Sonnet) | отчёт `<wt>\docs\tasks\specs\reports\td-15-0b-registry-walks.md` | — | 1 |
| TD-5.2 инвентарь пинов (спека TD-5) | scout (Sonnet) | `<wt>\docs\tasks\handoffs\td-5-2-inventory.md` | — | 1 |
| TD-15.1 раннер | builder | `<pkg>\scripts\selftest.py`; `<pkg>\scripts\tests\test_selftest_shard.py`; `<pkg>\scripts\tests\test_selftest_slow_tests.py`; `<pkg>\scripts\tests\fixtures\judgment-census.json` (строки) | — | 1 |
| TD-15.2 keep, detector, pin_holds | builder | `<pkg>\scripts\tests\test-layers.json` | 15.1, 15.0b, TD-5.2 | 2 |
| TD-15.3 инструмент захвата | builder | `<wt>\tools\story_capture.py`; `<wt>\tools\test_story_capture.py`; `<wt>\tools\story-scrub-rules.json` | 15.0 | 2 |
| TD-15.4 обходчик | builder | `<pkg>\scripts\tests\scenario_walk.py`; `<pkg>\scripts\tests\test_scenario_walk.py`; `<pkg>\scripts\tests\fixtures\synthetic-scenario\` | 15.0 | 2 |
| TD-15.6a инструмент карантина: данные + заглушки всех подкоманд + features.json | builder | `<wt>\tools\test_quarantine.py`; `<wt>\tools\test_test_quarantine.py`; `<wt>\plans\test-quarantine\README.md`; `<wt>\plans\features.json` | 15.1 | 2 |
| TD-15.5.k захват истории k (k = 1..3, по одной на узел) | builder | `<pkg>\scripts\tests\fixtures\stories\<id>\`; `<pkg>\scripts\tests\test_scenario_<id>.py` | 15.3, 15.4, строка TD-15.0 | 3 |
| TD-15.6b CI: `pull`, `ci_summary`, задачи | builder | `<wt>\tools\test_quarantine.py` (функции `pull`, `ci_summary`, `_ci_pipelines`, `_schedules` только); `<wt>\tools\test_test_quarantine.py` (свои функции теста); `<wt>\.gitlab-ci.yml`; `<wt>\tools\test_ci_layout.py` | 15.6a | 3 |
| TD-15.6c purge | builder | `<wt>\tools\test_quarantine.py` (функция `purge` и её помощники `_purge_*` только); `<wt>\tools\test_test_quarantine.py` (свои функции) | 15.6a | 3 |
| TD-15.7 строка сессии | builder | `<wt>\tools\session_context.py` (функция `test_quarantine_line` + один вызов); `<wt>\tools\test_session_context.py` (свои функции) | 15.6a | 3 |
| TD-15.6d замер покрытия keep | builder | `<wt>\tools\test_redundancy.py`; `<wt>\tools\test_test_redundancy.py`; `<wt>\.gitlab-ci.yml` (строка скрипта задачи `test-redundancy`) | 15.6b (`очередь: TD-15.6b → TD-15.6d` по `.gitlab-ci.yml`), 15.2 | 4 |
| TD-15.8 разрезать импорты | builder | оставшиеся файлы-импортёры из `enter --dry-run` «held by import» (абсолютные пути вставляет Lead в диспатч) + новые `<pkg>\scripts\tests\<area>_common.py` | 15.2, 15.6a | 4 |
| TD-5.3.k волны пинов (спека TD-5, область сужена) | builder | по TD-5 §7.3 + строки `pin_holds` | TD-5.2, 15.2 | 4 (последовательно) |
| TD-15.5r запись истории на стенде | владелец + Lead (живой прогон) | — | G-1; только если TD-15.0 нашёл мало | вне волн |
| TD-15.9 перевод фазы 1 | Lead/интегратор | запускает `enter`, коммитит; правки §E | всё выше зелёное на CI; ≥ 3 истории | 5 |
| TD-15.10.k фаза 2 (по одному детектору) | builder (замена) + Lead (носитель, `enter --phase2`) | строка-замена в своём слое + `test-layers.json` (одна строка keep) | 15.9 | позже |

Волны и потолок пишущих (≤ 6, host adaptation 6; разведчики не считаются): волна 1 — 1 пишущий (15.1) + 3 разведчика;
волна 2 — 4 (15.2, 15.3, 15.4, 15.6a); волна 3 — 6 (15.5.1–3, 15.6b, 15.6c, 15.7); волна 4 — 15.6d, 15.8, волны TD-5.3
(последовательно); 15.5.k сверх трёх ждут слота. 15.6b и 15.6c пишут в один `.py` непересекающимися функциями (D-0048),
`build_parser`/`main` и заглушки всех подкоманд пишет только 15.6a. Строку keep истории (`test_scenario_<id>.py`) узел 15.5.k
НЕ пишет в `test-layers.json`, а сдаёт в отчёте; Lead добавляет строки при слиянии (соседние строки JSON конфликтуют текстом).

Проходы критика (по одному на тему, R13-g): повторный проход по ЭТОЙ ревизии — только дифф ревизии и вердикт t-2281 (host
adaptation 6); тема 1 = 15.1 + 15.2 (раннер канона, ядро); тема 2 = 15.3 + 15.4 + 15.5.* (слой сценариев, одним проходом после
слияния историй); тема 3 = 15.6a–d + 15.7 + 15.8 (инструмент карантина, гейтоподобный). Перевод (15.9) принимает Lead со
свидетелем — id пайплайна, `--coverage-pipeline` и печатью `enter`. Каждый 15.10.k — свой критик (суждение «та же ли защита»).

Доказывает только CI: время историй и слоя; канон «как будет» (условие `enter`); задачи наблюдателя, их объединение и первую
запись; `test_story_run_*` и `SLOW_TESTS`; полный `pytest tools/`; замер покрытия keep.

### TD-15.0 — носители историй (scout)
Вопрос: (а) какие наборы артефактов настоящих прогонов в репозитории и на копиях стенда (`tools/dev.config.yaml`
`stand_copy_root`, только чтение) СИНТЕТИЧЕСКИЕ (задача стенда MyBooks, LOCAL-* или записанная для цели; не ключ TP3*/внутренний)
и ПОЛНЫЕ: есть `state/events.jsonl`, `work/`, `work/handoffs/`, слова гейта A и гейта B в `state/words/`, исход каждой пройденной
стадии; (б) по каждому такому корню: где записана приёмка каждой стадии (тип события, seq), каждый отказ (файл, вид/ключ),
каждый вопрос человеку (файл, `kind`, токены), каждое слово человека, вердикт доставки; какие стадии S0..S9 он покрывает, есть ли
красный Then; (в) какие стадии переделывались; (г) размер в байтах, кириллица, совпадения правил `docs/migration/scrub_rules.json`
(id правила, число); (д) версия пакета; (е) где в записи лежит текст сдачи (digest) и факты, которые принимает
`exit_gate.all_errors`; (ж) какая функция строит вопрос гейта A/B по миру, срезанному до открытия гейта, и какая — записывает решение
по словам, и какие у них побочные эффекты (в пакете нет одной очевидной: кандидаты `controller._gate_questions_view`,
`gate_brief.*`); (з) откуда в записи `kinds` и `doc` для `delivery_verdict.decide`. Критерий полноты: (а)–(з) на каждый корень;
«нет» — только с положительным контролем той же формы на корне, где есть. Итог отчёта: список историй-кандидатов с покрытием
`story_coverage_required` и вывод «трёх хватает / не хватает: непокрыто <…>». Свидетельство пути обязательно.

### TD-15.0b — обходы реестров (scout)
Вопрос: по всем 581 кандидатам фазы 1 (список — 701 минус §B.4 минус §B.5) — какие файлы являются обходом реестра (критерий 2)
или стыком «строка реестра ↔ читатель» / храповиком «только сжимается» (критерий 4/AR-20). Решето (не вердикт):
Grep `-i` `registry|census|ENUMERATED|both directions|one reader|every row|shrink|_MAX\b|baseline` по `scripts/tests/test_*.py`;
чтение головы файла (докстринг, первые 40 строк) — вердикт. Плюс по 37 упоминаниям SIBLING_MAP из §B.5 — является ли строка
карты строкой «Detector»/членом оси или аналогом/примером (цитата строки). Итог: две таблицы (добавить в фазу 2 / можно в фазу 1),
по строке на файл с цитатой. Положительный контроль решета: оно находит `test_state_exits.py` («ENUMERATED»).

### TD-15.1 — раннер (builder)
Given: `<pkg>\scripts\selftest.py` (`cmd_tests`, `shard_files`, `slow_tests`, `slow_tests_diff`, `slow_tests_updated`, `main`,
`CONTRACT_TESTS` l.533), `<pkg>\scripts\install_smoke.py` (l.467–469), `<pkg>\references\gate-registry.json`,
`<pkg>\references\stage-joints.json`, `<pkg>\scripts\tests\fixtures\driver-layers.json`, `<pkg>\design\architecture.md`,
`<pkg>\design\factory-rules.md`, `<pkg>\scripts\install_paths.py` (`plugin_version`), `<pkg>\scripts\tests\harness.py` (l.94 формат
FAIL), эта спека §B.1, §B.2, §C.1, §D.1.
Изменить:
1. `test_layers(path=None) -> dict` и `TestLayersError` — формы §B.1. Тест: таблица в `test_selftest_slow_tests.py` (нет файла /
   битый JSON / файл в двух секциях / слой не из списка / пустой `why` / `detector` без `named_by` / строка карантина с
   неизвестной когортой / `pin_holds` на отсутствующий файл).
2. `gate_named_files(extra_texts=()) -> set[str]` — §B.2 (носители пакета + переданные тексты; только имена, существующие в
   `scripts/tests/`). Тест: строка таблицы на временном мини-пакете (по одному имени в каждом носителе + имя модуля
   `test_files.py`, которого нет в `tests/` → не попадает); строка «на НАСТОЯЩЕМ `test-layers.json` носители пакета ⊆ keep» —
   пропуск с заметкой, пока файла нет.
3. `cmd_tests(..., quarantined=False)`: строки карантина отфильтрованы до шардирования и `--fast`; с `quarantined=True` — только
   они, веса из поля `seconds`; при `enforce_listing` файл вне секций печатает
   `FAIL tests: unlisted: <name> -- add a keep row (layer + why) to scripts/tests/test-layers.json, or put its case as a scenario/table row and remove the file (docs/TESTING.md)`
   и всё равно идёт; строка keep без файла — `FAIL tests: keep row names no file: <name>`; пустой keep при включённом — один
   `FAIL tests: keep list empty` (все файлы идут); при N > 0 — `tests: quarantine: N file(s) not run (scripts/tests/test-layers.json)`.
   Тест: `test_selftest_shard.py` — временный каталог с 4 файлами (keep, detector, quarantine, unlisted): карантин нет ни в одном
   шарде и в `--fast`; объединение шардов = keep + detector + unlisted; `--quarantined` — только карантин; токен `unlisted:`.
4. `slow_tests_diff`/`slow_tests_updated` пропускают имена карантина. Тест: строка в `test_selftest_slow_tests.py`.
5. Флаги `--quarantined` (подразумевает `--tests`; не с `--fast`/`--slow-tests`; с `--shard` можно) и `--watch-out PATH` (только с
   `--quarantined`): запись §D.1 (`expected`, `fails` ≤ 50 + маркер `+N more`, `crash`, статус `missing` для строки без файла);
   выход 0, кроме сбоя раннера. Тест: строка на временном каталоге (красный файл с двумя FAIL, файл с трассировкой, пропавший файл
   → `fails`/`crash`/`missing`).
6. Строки переписи в `fixtures/judgment-census.json` для новых единиц проверки (K1, K3: класс `xref`, владелец данные).
Грани: файла нет — поведение сегодня; битый — выход 2 с предложением; `--quarantined` при нуле строк —
`tests: quarantine: 0 files` и пустая запись с `expected: []` (AR-23); каталог `--watch-out` отсутствует — создаётся.
DoD (из корня `<wt>`): `python -B ai-packages/qa-factory/scripts/tests/test_selftest_shard.py`;
`python -B ai-packages/qa-factory/scripts/tests/test_selftest_slow_tests.py`; `python -B ai-packages/qa-factory/scripts/tests/test_selftest_ran_nothing.py`;
`python -B ai-packages/qa-factory/scripts/selftest.py --limits --lang`; `python -B ai-packages/qa-factory/scripts/tests/test_judgment_census.py`
(на CI 29,5 с; дольше 2 минут локально — стоп, оставить канону строкой отчёта). Non-goals: без CI, без строк keep, без инструмента форджа.

### TD-15.2 — keep, detector, pin_holds (builder)
Given: §B.3–§B.6 (списки дословно), отчёт TD-15.0b с решениями Lead по нему, инвентарь TD-5.2, `selftest.test_layers` (15.1).
Изменить: написать `<pkg>\scripts\tests\test-layers.json`: `enforce_listing: false`, `quarantine: {}`, `cohorts: {}`,
`story_coverage_required` (§A.5); строка keep на каждый файл §B.4 (слой, `why` ≤ 160 знаков) и §B.5 (слой `detector`, `named_by` —
строки «Носитель» §B.5 в форме `<путь>:<строка>`, `replaced_by: null`); `covers` у КАЖДОЙ строки — модули `scripts/`, которые
файл импортирует напрямую, плюс файлы данных, которые он открывает литералом; `pin_holds` — файл → причина, для каждого
не-stay файла, где инвентарь TD-5.2 называет хоть один пин вида «rule».
Грани: файл из списков отсутствует на диске — стоп и отчёт (строку не выдумывать); инвентарь TD-5.2 не готов — узел ждёт
(без `pin_holds` `enter` нельзя было бы доверять: файл с непринятым правилом ушёл бы в карантин).
Тест: строка «носители пакета ⊆ keep» из 15.1 теперь идёт на настоящем файле.
DoD: `python -B ai-packages/qa-factory/scripts/tests/test_selftest_slow_tests.py`; `python -B ai-packages/qa-factory/scripts/selftest.py --limits --lang`;
в отчёте — число строк по слоям (ожидается: gate_named 31, scenario 5, register 6, data_join 6, table 21, detector 51 ± решения по
15.0b) и число `pin_holds`. Non-goals: без строк карантина.

### TD-15.3 — инструмент захвата (builder)
Given: `<pkg>\scripts\tests\fixtures\run-12586-gate-b\rebuild.py` и README (процедура: `latin`, `walk`, `write_chain`,
`rebind_gate_a`), `run-12586-manual\README.txt` (что такое гибрид), `<pkg>\scripts\event_store.py` `content_hash`,
`<pkg>\scripts\controller.py` `gate_inputs` (l.4599), `_project_pipeline` (l.4624), `<wt>\docs\migration\scrub_rules.json`, отчёт
TD-15.0, §A.1–§A.2, FK-11 (`docs/tasks/specs/t-1855-github-move-nodes.md:484`).
Изменить:
1. `<wt>\tools\story-scrub-rules.json` — копия строк `rules` из `docs/migration/scrub_rules.json`, где правило `person` заменено
   шаблоном FK-11 (имена людей), с
   полем `source` («docs/migration/scrub_rules.json + FK-11»). Причина отдельного файла: инструменты `docs/migration/` разовые и не
   переезжают (FK-5).
2. `capture --source DIR --id ID [--cut-after-seq N] [--drop GLOB ...] [--package DIR]`: копирует корень (события до среза),
   транслитерирует кириллицу (`latin()`), заменяет абсолютный префикс источника на `<stand>` и домашний каталог на `<home>`,
   пересчитывает цепочку событий и привязки гейта A функциями пакета, пишет `story.json` с `synthetic: true` и `README.txt`
   (источник, срез, изменено, отброшено). Отказ (выход 1): остаток абсолютного пути, байт кириллицы или совпадение правила
   `story-scrub-rules.json` — с файлом:строкой и id правила (K15; дверь `--drop <glob>` или правка источника вне репозитория);
   ключ задачи совпадает с правилом `jira-tp3` — отказ «not synthetic: internal ticket key» без двери `--drop` (корпус Jira не
   история); результат больше 2 МБ — отказ с пятью крупнейшими файлами (дверь `--drop`, отброшенное в README, стадии, читающие
   отброшенный файл, — `not_walked: trimmed`); цель существует — отказ (дверь: новый id); нет `story-scrub-rules.json` — отказ
   (FR-59).
3. `expected --id ID`: по носителям TD-15.0 извлекает для каждой стадии последнюю приёмку, записанные отказы, вопросы (kind,
   токены), слова, вердикт доставки; пишет `expected.json` с `source` на запись и пустыми `amendments`; стадия без носителя —
   нет в `stages`, есть в `story.json` `not_walked` с причиной.
Тест: `<wt>\tools\test_story_capture.py` (новый скрипт → один файл, ≤ 10 с): синтетический корень на 6 событий во временном
каталоге с одним словом кириллицы, одним абсолютным путём и одним именем из правила `person`: без `--drop` — отказ с id правила;
после правки — выход без всех трёх; цепочка сходится через `event_store`; ключ `TP1-1` — отказ «not synthetic»; цель
существует — отказ; `expected` отображает accept/decision/words. Потолок 2 МБ — внутренняя граница, теста нет (R9).
DoD: `python -m pytest tools/test_story_capture.py -q`. Non-goals: истории здесь не захватываются; файлов пакета нет.

### TD-15.4 — обходчик (builder)
Given: `<pkg>\scripts\tests\test_stage_joints_12586.py` (J1–J3: чистые проверки), `story_run_common.py`, `harness.py`,
`<pkg>\scripts\story_step.py` (`start`), `<pkg>\scripts\exit_gate.py` `all_errors` (l.1763), `<pkg>\scripts\delivery_verdict.py`
`decide` (l.119), `<pkg>\references\stage-joints.json`, `<pkg>\handoffs\index.yaml`, отчёт TD-15.0 (пп. (е)–(з): функции дверей
`gate`/`delivery` — Lead вставляет их имена в диспатч), §A.
Изменить: `scenario_walk.py` — функции §A.4, виды дверей `exit_gate`, `joint`, `start`, `gate`, `delivery` (закрытый `DOORS`),
`--witness-for` (§A.6); `fixtures\synthetic-scenario\` — СИНТЕТИЧЕСКАЯ двухстадийная история ручной сборки, только для таблицы
обходчика (история слоя — никогда; `synthetic: true`, `walker_fixture: true`, `enter` её не считает).
Тест: `test_scenario_walk.py` (≤ 10 с), одна таблица: отказы `load_story` (битый JSON, нет `synthetic`); каждый `op`; фасет без
носителя → NOTE, не PASS; стадия в `walk` без записи `expected` → FAIL `<story>/<stage>/expected-missing`; указатель варианта
отсутствует → FAIL `variant-pointer-absent`; сбой сборки мира → один FAIL и ни одной проверки стадии; фасет `handed` не меняет
общий мир (хэш до/после); `witness_for`: совпадение по импорту / по `covers` строки gate_named / нет совпадения / удалённый путь /
файл данных.
DoD: `python -B ai-packages/qa-factory/scripts/tests/test_scenario_walk.py`; `python -B ai-packages/qa-factory/scripts/selftest.py --limits --lang`.
Non-goals: без правки скриптов продукта; без правки существующих фикстур; без историй.

### TD-15.5.k — захват истории k (builder; k = 1..3+, параллельно)
Given: строка TD-15.0 для прогона, `tools/story_capture.py`, `scenario_walk.py`. Изменить: `capture`, `expected`, `story.json`
`walk` по стадиям, которые носители поддерживают; файл `test_scenario_<id>.py`; строку keep (`{"layer": "scenario", "why": ...,
"covers": [...]}`) — в ОТЧЁТ, не в `test-layers.json`. Поправки билдер НЕ пишет: отчёт перечисляет каждый записанный отказ/исход,
который билдер считает дефектом, со ссылкой на находку; поправки пишет Lead при приёмке. В отчёте — какие элементы
`story_coverage_required` история покрывает (по пройденным фасетам).
Грани: стадия, которую сегодняшний код отказывает там, где прогон принял, — оставить красной и сообщить (регрессия или смена
контракта: решает Lead — поправка или баг); захват отказал по правилу чистки — `--drop` только для файлов, не нужных проходимым
стадиям, иначе стоп и отчёт.
DoD: `python -B ai-packages/qa-factory/scripts/tests/test_scenario_<id>.py`; `python -B ai-packages/qa-factory/scripts/selftest.py --limits --lang`.

### TD-15.5r — запись истории на стенде (владелец + Lead)
Только если TD-15.0 нашёл меньше трёх полных синтетических историй или они не покрывают `story_coverage_required`. Живой прогон
фабрики на стенде MyBooks (машина и стенд владельца, `docs/RUNBOOK.md` §9/§11) на задаче, выбранной под непокрытое (например,
задача с красным Then и решением на гейте B); затем TD-15.5.k над её корнем. Порядок по рекомендации G-1: сначала захватить
то, что есть, и записывать только непокрытое.

### TD-15.6a — инструмент карантина: данные (builder)
Given: §C, §D.2–§D.5 (тексты), `selftest.test_layers`/`gate_named_files`, `<wt>\tools\ci_read.py` (`request`, `token_env_name`,
`cmd_jobs`, `cmd_artifact`), `<pkg>\scripts\install_paths.py` пакета (`plugin_version`, `_vtuple`), `<wt>\plans\features.json`.
Изменить:
1. `<wt>\tools\test_quarantine.py`: `build_parser`/`main` со ВСЕМИ подкомандами (`enter`, `check`, `status`, `judge`, `land`,
   `pull`, `ci-summary`, `purge`, `drop-keep`); тела `pull`, `ci-summary`, `purge` — заглушки, печатающие `not implemented (TD-15.6b/c)`,
   выход 2; функции `status_data(root) -> dict`, `status_line(root) -> list[str]` (тексты §D.5), `held_by_import(root) -> list[tuple]`,
   `signature(file_result) -> tuple`, `covered(observation, verdicts, watch) -> bool`, `releases(root, cohort) -> list[str]`,
   `forge_texts(root) -> list[str]` (тексты носителей форджа для `gate_named_files`).
2. `enter` — §C.2 (усл. 1–5, 7–8; усл. 6 зовёт `_schedules`, которую пишет 15.6b — до неё заглушка, возвращающая «unknown» → отказ),
   `enter --phase2` — §C.3, `enter --rebase-entry` — §C.4; `check` — §C.4; `status` — §D.3; `judge`, `land` — §D.4; `drop-keep FILE
   --reason TEXT` — снимает строку keep и удаляет файл тем же подготовленным коммитом с сообщением `keep-drop: <file> -- <reason>`.
3. `<wt>\plans\test-quarantine\README.md` (по-русски, рабочий документ): файлы `config.json`, `watch.jsonl`, `verdicts.jsonl`, кто пишет.
4. `<wt>\plans\features.json`: глобы новых файлов всей спеки (`scripts/tests/test-layers.json`, `scripts/tests/scenario_walk.py`,
   `scripts/tests/test_scenario_*.py`, `scripts/tests/fixtures/stories/**`, `scripts/tests/fixtures/synthetic-scenario/**`,
   `tools/test_quarantine.py`, `tools/test_test_quarantine.py`, `tools/story_capture.py`, `tools/test_story_capture.py`,
   `tools/story-scrub-rules.json`, `plans/test-quarantine/**`) в фиче, которую называет Lead в диспатче.
Тест: `<wt>\tools\test_test_quarantine.py` (новый скрипт → один файл, ≤ 10 с, временные репозитории git, CI — функция-аргумент):
одна таблица R1–R6 (каждое правило проходит и падает; R2: ноль/один/два релиза, откат версии, версия-суффикс → unknown, полный
прогон на версии ≥ R_2 / только неполный); `enter`: отказ по каждому усл. 1–8, печать при успехе (токены), `--phase2` (а)–(г);
`check`: правка/удаление/переименование файла карантина, дверь в ДРУГОМ коммите не засчитывается, коммит слияния с дверью в
коммите второго родителя проходит, снятая строка keep без двери, возврат имени из истории карантина, добавленный `pin_holds` после
входа, новое ребро импорта, `quarantine-accept:`, `--rebase-entry`; `judge`: дубль и supersede, `real_catch` без находки, `flaky` без
пары красный/зелёный на одном sha; покрытие: `stale` покрывает подмножество подписи, новое имя — не покрыто, `flaky` без зелёного
на sha позднего наблюдения — не покрыто; `status_line` — токены `READY TO DELETE`, `ALERT`, `unknown`, `pulled ... -- run:`,
`has no complete watch run`; дубли строк `run` по `pipeline` — одна; одинаковые вердикты — один, разные — R4.
DoD: `python -m pytest tools/test_test_quarantine.py -q`; `python -m pytest tools/test_forge_metrics.py -q` (глобы фичи).
Non-goals: без CI, без purge, без хука сессии.

### TD-15.6b — CI (builder)
Изменить: `pull` (§D.2), `ci_summary` (§D.1 тексты §D.5 (2)), `_ci_pipelines(branch, sources)` (schedule/web/api/push с задачей
`quarantine-watch-report`), `_schedules(branch)` (`GET /projects/:id/pipeline_schedules` через `ci_read.request`, переменные
расписания); `.gitlab-ci.yml` — задачи `quarantine-watch`, `quarantine-watch-report` (§D.1, карта задач в шапке), условие
`&& $QUARANTINE_WATCH != "1"` в правиле `schedule` задач полного уровня, строка forge-check `python tools/test_quarantine.py check`;
`tools/test_ci_layout.py` — золото.
Тест (свои функции в `tools/test_test_quarantine.py`): шард отсутствует → `complete: false`, `not_run`; объединение `expected` ≠
секции на sha → `complete: false`; `pull` на уже записанном пайплайне — пропуск, строка `pull` всё равно; CI недоступен → выход 1 и
строка `ci: unreachable`; наблюдатель не шёл 9 дней → выход 3 и ALERT-текст; литерал ветки в `.gitlab-ci.yml` = `config.json`
`branch` (стык); `_schedules` без расписания → «missing», с расписанием без переменной → «missing».
DoD: `python -m pytest tools/test_test_quarantine.py tools/test_ci_layout.py -q`. Живое доказательство: один web-пайплайн с
`QUARANTINE_WATCH=1` после перевода (Lead).

### TD-15.6c — purge (builder)
Изменить: `purge` по §D.6. Тест (свои функции): копия мини-пакета во временном каталоге (3 теста в двух когортах, один
оставшийся импортирует помощника, фикстура по литералу, фикстура по динамическому пути, `TEST_TIMEOUTS` с комментариями,
`driver-layers.json`, `features.json`): удаляет ровно нужное и только когорту `--cohort`; динамический путь — фикстуры не
удаляются; отказ без слова и без READY; правка `TEST_TIMEOUTS` по `ast` оставляет файл разбираемым и строки существующих файлов.
DoD: `python -m pytest tools/test_test_quarantine.py -q`. Никогда не гонять против живого дерева в узле.

### TD-15.6d — замер покрытия keep (builder)
Изменить: `tools/test_redundancy.py run` — флаг `--keep-only`: выбор файлов — строки `keep` через `selftest.test_layers()` пакета
(AR-13; импорт по пути `--package`), несовместим с `--only`; отчёт печатает «covered lines» тем же форматом. `.gitlab-ci.yml`
задача `test-redundancy`: при `REDUNDANCY_SCOPE == "keep"` — `--keep-only` вместо прежнего набора. Тест: строка в
`tools/test_test_redundancy.py` (временный пакет с `test-layers.json`: выбраны только keep; нет файла → отказ с дверью «run
TD-15.2 first»). DoD: `python -m pytest tools/test_test_redundancy.py tools/test_ci_layout.py -q`. Живой замер — Lead запускает
web-пайплайн `TEST_REDUNDANCY=1 REDUNDANCY_SCOPE=keep` и передаёт id в `enter --coverage-pipeline`.

### TD-15.7 — строка сессии (builder)
Изменить: `test_quarantine_line(root) -> list[str]` + вызов после `last_calibration_line` в `build_context_lines`; импорт
`tools/test_quarantine` в try. Тест (свои функции в `tools/test_session_context.py`): нет файла → строк нет; миры ожидание / не
вытянуто / READY / ALERT улова / ALERT наблюдателя / unknown → токен присутствует; исключение внутри → строка `unavailable`,
остальной контекст цел. DoD: `python -m pytest tools/test_session_context.py -q`.

### TD-15.8 — разрезать импорты kept → quarantined (builder)
Given: список «held by import» из `enter --dry-run` (Lead вставляет абсолютные пути в owns). Изменить: по каждой паре — имена,
которые оставшийся файл берёт у файла карантина, КОПИРУЮТСЯ в `scripts/tests/<area>_common.py`, импорт оставшегося файла
переводится туда (файл карантина не правится). DoD: прогон каждого тронутого оставшегося файла
(`python -B ai-packages/qa-factory/scripts/tests/<file>`; файл из `SLOW_TESTS` — CI, строкой отчёта);
`python tools/test_quarantine.py enter --dry-run` печатает `held by import: 0`.

### TD-15.10.k — фаза 2: перевод детектора (builder + Lead)
Билдер: строка-замена в своём слое (вариант истории, строка стыка или таблицы), падающая на дефекте класса, который держал
детектор (свидетель — красный прогон на копии с внесённым дефектом, откат копией байт, хэш), и строка keep для неё (в отчёте).
Lead: правит строку носителя (SIBLING_MAP / architecture.md / factory-rules.md) на замену тем же подготовленным коммитом,
запускает `enter --phase2 <file> --replaced-by <row> --pipeline <id>`. Критик узла отвечает на вопрос «ловит ли замена тот же класс».

---

## §E2. Грани (поведение и инвариант, который оно охраняет)

| Грань | Поведение | Инвариант |
|---|---|---|
| файл из карантина «возвращается» | строка keep с именем из истории карантина — отказ K5 без двери; `test_layers` отказывает имени в двух секциях | из карантина тест не возвращается (TESTING.md) |
| пустой keep | `enter` отказывает; при `enforce_listing` и пустом keep — `FAIL tests: keep list empty`, идут все файлы | канон никогда не гоняет ничего |
| пустой карантин | строк сессии нет; `status` — `no quarantine`; R1 падает (READY на пустом не бывает); `purge` — отказ | на пустом не бывает сигнала «можно удалять» |
| пустая запись наблюдателя после `enter` (`watch.jsonl` нет или без строк `run`) | `status`: `no watch run yet (entered N d ago)`; при N > 8 — ALERT наблюдателя; R2/R3 не выполнены | молчание наблюдателя не выглядит как «всё зелено» |
| прогон с нулём файлов | ожидалось 0 (до входа / после purge) → `complete: true`, R2 его не учитывает (в когорте нет файлов на sha); ожидалось > 0 → `complete: false`, `not_run` всем | неизвестное не проход (AR-28) |
| релиз без прогона наблюдателя | версия на HEAD ветки больше версий полных прогонов → строка `release X has no complete watch run yet -- start it`; R2 ждёт полный прогон с версией ≥ R_2 | удаление никогда без прогона на втором релизе |
| релиза на ветке нет (релизы идут из другой ветки) | `releases since: 0 of 2`; READY не наступает; срока нет (O-5); G-2 | версия, которой ветка не видела, не считается |
| красное в файле, удалённом с тех пор | строка `run` для имени, которого нет в секции карантина на sha этой записи, игнорируется (`ci-summary` берёт секцию того же sha); удалённый вне purge файл с ещё живой строкой — статус `missing`, подпись `missing`, наблюдение к разбору; сам коммит удаления уже отказан K5 | набор карантина сжимается только purge; пропажа файла не выглядит зелёной |
| файл карантина импортирован оставшимся | на диске (манифест), импорт работает; R6 падает до TD-15.8; `purge` отказывает | оставшийся тест не теряет импорт |
| оставшемуся нужен помощник из файла карантина | помощник КОПИРУЕТСЯ в не-тестовый модуль; новое ребро импорта — отказ K5 (дверь `quarantine-import:`) | нет новой зависимости от удаляемого; файл карантина не правится |
| фикстура только для карантина | лежит до purge; удаляется, только если её не называет литералом ничто оставшееся и никто не строит путь динамически | purge не удаляет то, что читает оставшийся (ошибка в сторону сохранения) |
| таймаут наблюдателя | таймаут файла → `timeout` (наблюдение к разбору); таймаут задачи/шарда → `complete: false`; три неполных подряд — в строке сессии | неизвестное не зелёное |
| релиз при неразобранных красных | релиз не держится; R3 держит удаление | удаление никогда поверх неразобранного |
| две сессии судят одно красное | второй вердикт на ключ без `--supersede` — отказ; противоречивые строки через слияние — R4, `status` называет конфликт; одинаковые — один | два вердикта не разрешаются молча |
| две сессии вытянули один пайплайн | строки `run` с тем же `pipeline` — одна | дубли не удваивают наблюдения |
| новый файл после перевода вне обеих секций | идёт и печатает `FAIL tests: unlisted:`; добавить в карантин — только `enter --add` (новая когорта, дверь) | файл не пропускается молча; ничто не входит в канон без слоя |
| файл красный на входе (TD-12: `test_telemetry_merge.py`) или мигающий | `red_at_entry`/`flaky_at_entry` по трём прогонам; первое наблюдение всё равно к разбору | старое красное не принимается за улов и не игнорируется |
| подпись меняется от данных в имени проверки | новая подпись → новое наблюдение (лишний разбор) | новая проверка никогда не прячется под старым вердиктом |
| смена контракта делает историю отказанной | поправка `expected.json` с `ref` (судит критик) или свежая история; артефакты истории не правятся | P20 |
| фасет без носителя | `not_walked`, NOTE, не в покрытие | непройденное не выглядит зелёным |
| правка билдера, которую не покрывает ни одна история | `--witness-for` печатает весь слой сценариев | свидетель ошибается в сторону большего |
| `plugin.json` нечитаем / версия неразборчива | `unknown`, никогда READY | FR-59 |
| история переписана (rebase), `commit_at_entry` не предок | `check` отказывает; дверь `enter --rebase-entry` | граница когорты не теряется молча |
| ветка переезжает на GitHub (t-1855:489, «переезд ветки эксперимента») | задачи и `pull` написаны для GitLab; узел переезда ветки переносит их в workflow с `cron` в файле и меняет `config.json` `ci`; до этого строка сессии по-прежнему показывает возраст наблюдателя, и ALERT сработает через 8 дней | наблюдатель никогда не останавливается молча |
| `docs/migration/scrub_rules.json` удалён после переезда | захват его не читает (свой `tools/story-scrub-rules.json`) | чистка историй не зависит от разового инструмента |
| `config.json` отсутствует | `enter`, `pull`, `status` — отказ/`unknown` с дверью «write plans/test-quarantine/config.json» | ветка наблюдателя никогда не угадывается |

---

## §G. Развилки для владельца (только то, что решает владелец; узлы исполнимы по рекомендации)

**G-1 (владелец) — истории, если готовых мало.** По замеру §A.1 в репозитории синтетических полных корней задач нет; кандидаты —
прогоны MyBooks на копиях стенда (меряет TD-15.0). Если трёх с нужным покрытием не наберётся, нужна запись истории живым прогоном
на стенде (ваша машина и стенд). Варианты: (а) начать с того, что есть на копиях стенда, и записывать только непокрытое (стадию,
слова гейта, красный Then) — **рекомендация**: меньше прогонов, перевод быстрее; (б) записать три свежие истории целиком под
цель — чище, но дороже и дольше. До ответа узлы идут по (а): TD-15.0 → TD-15.5.k над найденным; TD-15.5r ждёт вашего прогона.

**G-2 (владелец) — какой релиз считается.** Решение Lead: релиз = смена версии в `.claude-plugin/plugin.json` на ветке карантина
(`config.json` `branch`). Если релизы выходят только из `main` (теперь на GitHub), а карантин живёт на ветке эксперимента, версия
на ветке меняется лишь при слиянии с `main` — до этого условие O-1 не наступит (срока нет, O-5). Варианты: (а) так и ждать — счёт
пойдёт, когда ветка получит релизы (слиянием или переездом) — **рекомендация**: ничего не строим, строка сессии честно пишет
`releases since: 0 of 2`; (б) считать опубликованные релизы `QAFactory` (теги) — нужен доступ к репозиторию релизов и узел чтения
тегов, но тогда наблюдатель гоняет карантин на коде ветки, а не на релизном коде.

Действия владельца (не развилки): создать расписание пайплайна GitLab (Settings → CI/CD → Schedules, cron `0 3 * * 1,4`, ветка из
`config.json`, переменная `QUARANTINE_WATCH=1`) — без него `enter` отказывает; прочитать §G0 перед переводом (Lead покажет точное
число покрытия из TD-15.6d).

## Закрытые развилки (решения, перенесённые в текст)

| Развилка | Решение | Где в тексте |
|---|---|---|
| O-1 | два релиза, полный прогон на втором, всё разобрано, уловы перенесены (владелец) | §D.3 R2, R3, R5 |
| O-2 | записать, перенести, сразу сообщить, счёт продолжается (владелец) | §D.4, R2 |
| O-3 | два раза в неделю (владелец) | §D.1 cron, `max_gap_days`, §G0 п. 7 |
| O-4 | строка в начале сессии (владелец) | §D.5 (1) |
| O-5 | срока нет (владелец) | §D.3, §E2 |
| O-6 | три синтетические истории с покрытием (Lead + B2) | §A.5, §C.2 усл. 2 |
| L-1 | один файл `test-layers.json` | §B.1 |
| L-2 | манифест | §C.1 |
| L-3 | обход дверей стадии на последнем принятом выходе + варианты | §A.3 |
| L-4 | медленные файлы гейтов остаются; перенаправление `test` гейтов — TD-9 | §B.4 |
| L-5 | ПЕРЕПИСАНА (B1): детекторы, названные носителем, остаются слоем `detector` и уходят по одному с заменой и правкой носителя | §B.5, §C.3 |
| L-6 | записи и вердикты — `plans/test-quarantine/` | §D.2, §D.4 |
| L-7 | `pull` руками Lead | §D.2 |
| L-8 | ПЕРЕПИСАНА (B4): GitLab, расписание на ветке-параметре, push-правило релиза; GitHub — при переезде ветки | §D.1, §E2 |
| L-9 | импорты режутся до `enter` (TD-15.8) | §F |
| L-10 | новый файл вне секций идёт + FAIL | §C.2, §E2 |
| L-11 | ЗАМЕНЕНА (B3): `pin_holds` вместо «реестр существует» | §B.6, §C.2 усл. 5 |
| L-12 | тесты `tools/` вне области (TD-8) | Область |

## Ответы критику (t-2281)

| Находка | Ответ |
|---|---|
| B1 | применено: критерий 1b, слой `detector`, фаза 2 с `replaced_by` и правкой носителя тем же коммитом, TD-15.0b; числа замерены (69 / 51 / 581) — §B.2–§B.5, §C.3 |
| B2 | применено: только синтетические истории, 12586/14857 сняты, чистка по правилам + FK-11 (K15), отказ на внутреннем ключе, фасеты `not_walked`, условие покрытия, TD-15.0, TD-15.5r, G-1 — §A, §C.2 усл. 2 |
| B3 | применено: строки 41–52 и «absent today» убраны; усл. 5 — `pin_holds`; область TD-5.3 сужена; доказательство волны — `role_rules.py --check` + список — §B.6, §C.2 |
| B4 | применено по решению Lead: GitLab-расписание на ветке-параметре с записью в RUNBOOK §7, `enter` видит его через API, push-правило релиза, `pull` читает schedule/web/api/push, два возраста, ALERT через 8 дней, `pull` выход 3, полный уровень не едет с переменной — §D.1, §D.2, §D.5; GitHub-cron (а) — при переезде ветки, §E2 |
| B5 | применено: ключ (файл, подпись, пайплайн), покрытие по подмножеству имён, `flaky` по паре на одном sha, READY отказан при любом неразобранном, `blind` — §D.3, §D.4 |
| B6 | применено: диапазон от появления файла, каждый коммит своим сообщением, слияния по комбинированному диффу, охрана секций, запрет возврата по истории, `quarantine-accept:`, `--rebase-entry` — §C.4 |
| B7 | применено: `covers` у каждой строки, `--witness-for` по всем слоям, §G0 с замеренными числами, точное число — TD-15.6d и `enter` усл. 7 |
| R1 | применено: `exit_gate.all_errors` в процессе, копии мира для фасетов с побочными эффектами, срез до решения; функции вопроса/решения и входы `decide` — вопросы TD-15.0 (ж), (з), а не догадка билдера — §A.3 |
| R2 | применено: два различных релиза, полный прогон на втором; «опубликован» — приближение сменой версии, названо владельцу (§G0 п. 8, G-2); O-3 в cron, цене и порогах |
| R3 | применено: `seconds` в строке карантина (из `slow_tests.json` до чистки) — веса шардов наблюдателя; пишет `enter`, не `pull` (пакетный файл — один писатель) |
| R4 | применено: `expected` в записи шарда, сверка с секцией на sha, `missing` — наблюдение к разбору |
| R5 | применено: дубли `run` по `pipeline`; одинаковые вердикты — один, разные — R4 |
| R6 | применено: одна диспатч-партия на вытяжку, массовый проход по именам, потолок 30; оценка помечена — §D.4, §G0 п. 7 |
| R7 | применено: базовая линия по трём `package-full-report` — §C.2 усл. 8 |
| R8 | применено: 15.1 ∥ 15.6a снято (15.6a после 15.1); строки историй — в отчёт, Lead при слиянии; заглушки подкоманд — 15.6a; `features.json` — 15.6a; `?` → остаётся. НЕ применено: владение копиями GitHub-workflow (`docs/migration/forge-repo/.github/workflows/`) — они переносили `main`; ветка эксперимента переезжает отдельным узлом (t-1855:489), он и переносит задачи |
| R9 | применено: тест AT/BEYOND 2 МБ снят; `test_scenario_walk.py` — строка keep слоя table (раннер канона); `tools/test_story_capture.py` — тест форджа, вне списка keep пакета (L-12) |
| ответ 1 (поправки не видит владелец) | применено: поправки, меняющие исход, — в сообщении о переводе (§A.1, §G0 п. 6) |
| ответ 7 (носители правил) | применено: host adaptation 11, правило 4, `critic-diff-brief.md` l.11, `TESTING.md` l.115/117, 7b `test_console_encoding` (теперь stay) — §E |
| риски O-4 (добавить `CURRENT_CONTEXT.md`) | не применено: O-4 решён владельцем — строка сессии; ALERT наблюдателя закрывает «никто не тянет» |
| риски O-3 (минуты GitHub) | не применимо, пока наблюдатель на GitLab; при переезде ветки — строка минут владельцу в том узле |

## Мелкие решения, закрытые дизайнером

- Имена: `scripts/tests/test-layers.json` (секции `keep`, `pin_holds`, `cohorts`, `quarantine`), `scripts/tests/scenario_walk.py`,
  `scripts/tests/fixtures/stories/<id>/`, `tools/test_quarantine.py`, `tools/story_capture.py`, `tools/story-scrub-rules.json`,
  `plans/test-quarantine/{config.json,watch.jsonl,verdicts.jsonl}`.
- Когорты (`cohorts`) — чтобы у файлов фазы 2 был свой счёт релизов; `purge --cohort`.
- Покрытие вердиктом — подмножество имён подписи (не строгое равенство): меньше падающих проверок — это не новая проверка.
- Подпись: до 50 имён по сортировке + маркер `+N more` (маркер входит в подпись).
- Диапазон K5 — от коммита появления `test-layers.json`, а не от базы пайплайна: база не зависит от вида пайплайна.
- `max_gap_days` 4 из cron Пн/Чт; ALERT через 2 × 4 = 8 дней; подсказка «run pull» — вытяжка старше 4 дней.
- Строка вытяжки `kind: pull` в том же `watch.jsonl` (один писатель — `pull`).
- Литерал ветки в `.gitlab-ci.yml` + стык с `config.json` вместо переменной проекта CI (ещё один ручной шаг владельца не нужен).
- Свои правила чистки `tools/story-scrub-rules.json` (FK-5: инструменты `docs/migration/` разовые); `person` — шаблон FK-11.
- `test_s0_key_form` и `test_contract_slices` — слой table; причина `test_one_source_per_fact` — FR-10.
- Строка сессии — после `Last calibration` (переживает срез 25 строк), только ASCII.
- `enter`/`purge`/`drop-keep` готовят коммит и пишут сообщение; коммитит Lead (откат — revert).
- Инструмент захвата — в `tools/` (читает пути стенда вне репозитория; пакет их не называет, AR-4).

## Нужно сверх манифеста

Прочитано сверх given (для замеров и свежести): `ai-packages/qa-factory/scripts/selftest.py` (grep `CONTRACT_TESTS`),
`scripts/tests/harness.py` (grep FAIL), `scripts/` (grep функций `all_errors`, `decide`, `gate_inputs`, `_project_pipeline`,
вопросов в `controller.py`/`gate_brief.py`), `design/architecture.md` (grep имён тестов; l.105–112), `design/factory-rules.md`
(grep), `plans/builder-rules.md` (l.14–73), `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md` (grep; l.366–371), `.gitlab-ci.yml` (grep
правил; l.90–149, l.406–410), `tools/test_redundancy.py` (grep `only`), `docs/migration/scrub_rules.json`,
`docs/tasks/specs/t-1855-github-move-nodes.md` (l.478–491), Glob существования ~140 тестовых файлов, `plugin.json`, `tools/*`.

## §H. Свидетельство чтения

Прочитано: эта спека ревизии 1 (целиком); `docs/tasks/specs/reviews/td-15-plan-critic.md` (целиком); `docs/TESTING.md` (целиком);
`docs/tasks/test-diet.md` (l.100–169); `docs/tasks/specs/td-5-role-rules-register.md` (grep §4.6/TD-5.2/TD-5.3; l.668–707, 813–842);
`docs/SIBLING_MAP.md` (grep имён тестов; l.380–434); `docs/tasks/specs/reports/td-12-redundancy-8069240.md` (l.1–170, 700–734; grep
по 120 именам stay и фазы 2); плюс список «Нужно сверх манифеста».

Замеры и команды (все — инструменты Grep/Glob на дереве `D:/ws1/wt-test-diet`):
- 701 файл: Grep `.` glob `test_*.py` `files_with_matches` в `scripts/tests` с offset 650 → «Found 51 files»; в `fixtures/` того же
  glob нет (контроль: glob `*.json` там находит файлы).
- SIBLING_MAP: Grep `-o` `test_[a-z0-9_]+\.py` → имена; Glob существования в `scripts/tests` двумя скобочными списками → 27 + 25 = 52
  (совпадает с числом критика); 14 из них в stay (`driver_layers`, `http_client`, `null_outcomes`, `resolver`, `runtime_paths`,
  `s5_precheck`, `stage_guard`, `test_files`, `reinstall_equals_fresh`, `detector_verdict`, `read_json`, `run_forms`, `check_delivery`,
  `judgment_census`) → 38, минус `console_encoding` → 37.
- architecture.md / factory-rules.md / builder-rules.md / PROCESS: Grep `-o` того же вида; новые имена проверены Glob (17 найдено из
  21 запрошенных; не найдены — тесты форджа `handoff_rule_anchors`, `compact_snapshot`, `exam_runner`, `digest_form`, они вне пакета).
- stay: Glob двумя скобочными списками — 35 из 35 и 36 из 36.
- Решето пинов §4.6 TD-5 (обе альтернативы): Grep `files_with_matches` → «Found 242 files».
- Инвентарь TD-5.2: Glob `docs/tasks/handoffs/td-5*` — пусто; контроль той же формы `docs/tasks/handoffs/t-1467*` находит файл.
- Корни задач: Glob `**/state/events.jsonl` → 5, все внутренние; `**/LOCAL-*/**/*.json*` — пусто; контроль той же формы
  `**/TP1-14857/**/events.json*` находит файл.
- Покрытие: суммы столбца `adds` таблицы B отчёта TD-12 по строкам, найденным Grep (`| test_(…)\.py |`): stay — 18 591 + 7 913 =
  26 504 (найдено 33 + 33 строк; `test_role_rules` в отчёте нет — моложе замера; `test_driver_layers`, `test_artifact_writers` — не
  измерены; файлы таблицы A — 0); фаза 2 — 7 484 + 15 488 = 22 972 (`test_driver_stop_record` в отчёте нет); всего 49 476 из
  157 856 (31,3 %); фаза 1 = 157 838 (сумма `adds` ok-файлов, строка 6 отчёта) − 49 476 = 108 362 (включает файлы, удалённые после
  замера). Уникальные строки всего набора: 7 299 + 5 254 + 7 338 + 18 038 = 37 929 (`docs/tasks/test-diet.md` l.103–108).
- `--only` у `tools/test_redundancy.py` — один glob (l.114, 285), поэтому TD-15.6d добавляет `--keep-only`.

Замечено, не расширялось: решето TD-5 на сегодня находит 242 файла против 153 при черновике TD-5 (там считалась одна альтернатива);
правило `person` в `docs/migration/scrub_rules.json` у́же, чем FK-11 — GM1-6 расширяет его на `main`, на этой ветке
файл старый; диспатч ревизии называет черновик русским, он был английским.
