# t-955 — критик на план: «П1-б: довести сухую стори до CI на main» (20261117-p1b-finish-spec.md)

Критик (Opus), 17.11.2026. Предмет: `docs/tasks/specs/20261117-p1b-finish-spec.md` вместе с решениями Lead (:551-556).
Деревья для проверки: `origin/main` = `42f5fcae` (main ушёл вперёд во время ревью: был `ebb0593e`, спека ссылается на `cfe418b6`),
`wip/p1b-n4m` = `9c9d40c2`, merge-base = `e18e622f` (14.11 07:14, t-819). Деревья выгружены в scratchpad через `git archive`
(рабочие деревья не трогал): `main/`, `branch/`, `merged/` (дерево `git merge-tree --write-tree` = `ba076a5d`).

**Вердикт: годится с правками (fit_with_fixes) — 4 блокера, их надо снять ДО диспатча L1; 10 неблокирующих правок.**
Порядок и форма плана верные (посадка → метки → CI/реестр/проба → группы → N4c); но в нынешнем виде L1 не может
выполнить свой DoD, и main краснеет в момент слияния — причина, которую спека не видит (B1).

---

## Блокеры

### B1. Перепись выходов (census) красная на слитом дереве — 227 расхождений; `full` краснеет на main в момент L1 (K2)

- Носитель: `test_scenario_dry_1.py:28-34` (режим по умолчанию зовёт `census()` → `dry_exits.check()` →
  `harness.check("dry-1/census", not report.problems, …)`). Канон и ночь гоняют этот режим (keep-строка
  `test-layers.json:5109-5123` на ветке, `TEST_TIMEOUTS` 900).
- Прогоны (секунды — около 5 с каждый):
  - `merged`: `python -B scripts/tests/dry_exits.py --check` → `dry_exits --check: 227 discrepancies`
    (по видам: joint validate_artifacts 42, role_cli 33, guard_pre_tool 24, execution_request 24, handoff_check 21,
    manifest_put 14, planning_contract 12, s5_precheck 11, first_look 11, stage_guard 8, host_adapter 8, run_suite 7,
    controller 6, exit_gate 4, coverage_contract 2 — все «the driver has it and no row names it»).
  - контроль `branch`: `dry_exits --check: 0 discrepancies`, `NUMBER joints: 40`.
  - контроль `main`: `dry_exits --check: 228 discrepancies` (те же 227 + старая `kind without a key questions`, которую
    чинит N4:s1-s4), `NUMBER joints: 267`.
  - Причина: на main стыки выросли с 40 до 267 (работа «сказано до работы»: `git log e18e622f..origin/main --
    references/stage-joints.json scripts/stage_joints.py scripts/null_outcomes.py` → 900ccc03d T2, 705837d9/7ed7f103 T1r,
    60ddb66d, 1db4ec9f, 8d71532b, 442ae9de). Перепись на main никто не гоняет (`dry_exits.py` — не `test_*`), поэтому дрейф
    накопился молча.
- Следствия: L1 DoD (б) «`dry_exits.py --check` (`0 discrepancies`)» недостижим; owns L1 (non-goals «любая правка поведения
  сверх ветки») не даёт его починить; DoD L2 «`ci_read why` по `full` не называет `test_scenario_dry_1.py`» тоже недостижим
  (owns L2 — только реестры меток). Красный main после L1 — не размеченное состояние (метки `known_red` закрывают только
  строки обхода и `main/S<n>`, не расхождения переписи), а дефект плана.
- Ожидаемая правка: новый узел **L1c «перепись догоняет main»** на той же ветке, после L1, до L2, в той же волне. Owns:
  `fixtures/driver-exits/{gates,hooks,s0,s1-s4,s5,s6-s9}.json` (все шесть). Направление выбирает Lead ДО диспатча
  (это развилка, не задача билдеру): (а) строка переписи на каждый из 227 стыков (`reach: unwalked` с поднятой базой и
  `raised_by`, AR-20, или `live_only` с причиной) и таблица «семейство стыков → группа»; (б) сузить вселенную переписи в
  `dry_exits` (стыки «сказано до работы» не выходы драйвера) — тогда owns += `dry_exits.py` и это правка смысла проверки,
  ей нужен свой край. Края: DoD `--check` = 0 на итоговом дереве, повтор на дереве волны (параллельные потоки rules-debt
  S7/S8 трогают `exit_gate.py`, `gate-registry.json` — любой новый стык/отказ снова красит перепись); группы N4 стоят ПОСЛЕ
  L1c (тот же `driver-exits/<g>.json`).

### B2. 4789 строк уходят в main без единого критика кода (K2, K8; правило 3 CLAUDE.md)

- Все узлы ветки приняты с отказом от критика под условием «критик темы на сходимости»: журнал `logs/journal/*.jsonl`,
  `accepted` t-695 («critic: one per topic P1»), t-721, t-735, t-751 («topic critic at P1-b end»), t-789 («the P1-b topic
  critic covers it at convergence»), t-828 («critic: skipped»). Объём: `git diff --stat e18e622f wip/p1b-n4m` → 47 files,
  4789 insertions, 133 deletions.
- Решение Lead (:555): «критик кода — один на тему после волны групп» — то есть F-P12 (б), хотя строка :553 говорит «(а)».
  Посадка (волна L1+L2 в main) и есть сходимость, которой обещан критик; после неё код уже на main.
- Правка: F-P12 (а) как рекомендовано — один критик темы П1-б на дифф `origin/main...<ветка L1+L1c+L2>` ДО волны (R13-g не
  нарушается: тот же один проход, раньше по времени); критик групп — отдельная тема.

### B3. Строка решений Lead противоречит развилкам, на которых стоят узлы (K8)

- `:553` «F-P1 … F-P13 — берутся рекомендованные варианты (а), как записаны в §7». Но рекомендация F-P4 — (б) (`:406-408`),
  F-P8 — (б) отдельным узлом и (а) для групп сейчас (`:424-425`), F-P12 — текст Lead выбирает (б) (B2).
- L2 край (4) ветвится по F-P4 «(а) метка находки ходока, (б) удаление строки» — билдер L2 не знает, какую ветку исполнять;
  это гарантированный `rejected` с `failure_class: spec`.
- Правка: по строке на развилку: «F-P4 (б) + находка на (в) — пишет Lead в шаге 1 L2», «F-P8: группы по (а), FV3-14 = (б)»,
  «F-P12 (а)».

### B4. Owns L1 не покрывают два файла ветки; четвёртая метка без носителя (K1, K3)

- `git diff --name-only e18e622f wip/p1b-n4m` содержит `scripts/tests/fixtures/form-rounds.json` (+1 строка known_red
  `"obligation_refs <- manifest_row@all -> window_record.row_field_gaps": {"node": "P1B-2f", … "Lead to confirm this row"}`)
  и `scripts/tests/test_field_producers.py` (ожидание `obligation_refs` без хэша, :775-779). Ни того, ни другого нет в §3 и
  в owns L1 (`:172-191`): слияние запишет их вне owns.
- `P1B-2f` — метка без файла находки и строки пачки: Grep `P1B-2f|N4S0-1|N4S14-1|N4W-1` по `plans/` (-i) → 0;
  положительный контроль той же формы `P1B-9|FV1-14` → 74 вхождения в 19 файлах. L2 шаг (1) перечисляет только три метки.
- Правка: оба файла в owns L1 (и в FV3-1 «Пишет в»); `P1B-2f` — в L2 шаг (1): Lead заводит/подтверждает находку
  (D-0044) или убирает строку; `test_field_producers.py` на слитом дереве зелёный — `885/885 ok`, 22 с.

---

## Неблокирующие правки

- **F1 (§3, K1).** Таблица конфликтов неверна. `git merge-tree --write-tree --name-only origin/main wip/p1b-n4m` → дерево
  `ba076a5d`, rc 0, ни одного конфликта. Обе стороны меняли только `scripts/selftest.py`, ханки не пересекаются (main :355-359
  `REFERENCE_MD_MAX_BYTES`, ветка :112-117 `TEST_TIMEOUTS`). Main НЕ трогал после развилки `test-layers.json`,
  `slow_tests.json`, `form_filler.py`, `form-fill-rules.json`, `test_form_selftest.py`, `dry_*.py`, `scenario_walk.py` (пересечение
  списков имён — одна строка). Ветка не несёт журнал (`logs/` в списке нет). Настоящая поверхность — СМЫСЛОВАЯ: 190 коммитов
  main, 562 файла, из них 91 — скрипты и `references/` продукта (`driver_core.py`, `driver_stage_*.py`, `handoff_check.py`,
  `probe_by_code.py`, `brief_pack.py`, `profile_contract.py`, `controller.py`, `stage_guard.py`, слайсы контрактов). Края L1 (2)-(3)
  о текстовых конфликтах — мертвы; переписать §3 и края на «смысловая поверхность, её мерит L1c (B1) и CI L2».
- **F2 (L2, K2, K7).** Место остановки главного прохода после слияния не установлено (медленный файл, не гонял). Если проход
  встанет раньше S5 из-за отставания заглушки от новых обязанностей ролей на main («сказано до работы»), L2 край (1) пометит
  это находкой продукта. Добавить край: причина на стороне заглушки (тестовый слой) чинится узлом заглушки, а не меткой;
  `raised_by` метки называет класс «пробел заглушки / пробел продукта».
- **F3 (N5, K5).** Удаление входа `spike` убирает единственную дверь «только сухая стори». С задачей в `nightly.yml` вердикт
  части `exits:<g>` (группы, N4R, N2h, L2) — это целый канон: `forge-check` + `package-full` (2 шарда, кап 180 мин) +
  `install-smoke` (`nightly.yml:72-145`). Билдер свой вердикт получить может только через координатора — верно по п. 13
  «Командная работа», но каждый круг стоит часа. Правка: оставить булев вход (`dry_only`) в `canon.yml`, зовущий ту же задачу
  (одна задача, два вызова — AR-15), или вынести задачу в переиспользуемый `dry-story.yml` (workflow_call + workflow_dispatch),
  который вызывает ночь. Время задачи против часа канона (D-0059) в спеке не названо: назвать (части параллельно, кап 30 мин на
  часть; главный проход ~385 с до S5 внутри шарда `package-full`).
- **F4 (волна 3, K9).** N2h край (7) снимает метку `main/S5` «тем же коммитом» — это запись в `driver-exits/known_red.json`,
  которым владеет N4R в той же волне; в owns N2h файла нет. Правка: N2h только пишет строку отчёта; метку меняет N4R или
  отдельный последовательный шаг по выводу CI.
- **F5 (N2h, F-P5).** Не названа конфликтующая пара: «потолок 900 не растёт» (F-P5) против N2h, после которого проход идёт
  дальше S5 и запускает `probe_by_code.py` (мутационная проба) на каждый экземпляр окна. Сказать, что делать, когда проход
  подходит к 900 (кап на проход, отдельный кап пробы, или потолок с поднятием по слову Lead).
- **F6 (общая карточка групп, K6).** Класс F-P4 («ответ предлагается условно, у ходока нет условия») встретится в gates/s5/s6-s9,
  а карточка молчит. Добавить край: такой вариант строкой не пишется, строка отчёта + ссылка на находку (в). И: ожидаемо
  красные строки, для которых у Lead уже есть находки (gates — FV1-7/FV1-8), Lead выдаёт в диспатче заранее, иначе край (2)
  делает фикс-раунд у каждой группы.
- **F7 (N4R, K4).** Край (6) оставляет `dry_exits --judge --dir D` читать только общий файл; после N4R он отвечает неверно для
  строк групп. Вызывающих в дереве нет (Grep `--judge` по слитому дереву: только `probe_by_code`-тексты CHANGELOG и agents). Убрать
  ветку или научить её файлу группы — одна дорога (P31). В остальном F-P1 (а) вторую дорогу НЕ создаёт: содержимое реестра читает
  только `known_red.load` (AR-13), каждый id живёт ровно в одном файле (край 7), `dry_world.py:1335` склеивает общий файл
  (`main/*`) и файл группы — после N4R продолжает работать без правки; `dry_world.py:976` (главный проход) читает только общий файл.
- **F8 (§1, K7).** AR-14 отмечен «не тронут», но N4R создаёт файлы реестра по группе с одним писателем на файл — это AR-14,
  назвать и как держится. Механизм синхронизации заглушки с поведением ролей не назван: детектор — перепись (B1) и место
  остановки главного прохода; назвать его в §1 и класс метки (F2).
- **F9 (F-P3, K8).** Задача в ночи — ежедневные минуты CI. Если минуты Actions оплачиваются, это деньги — вопрос владельца
  (PROJECT.md «Что решать самому»). Не проверял, платные ли они; Lead подтверждает или спрашивает.
- **F10 (§2, §11).** §2 N3t «каталог `dry-codemie-14857` — не установлено»: он есть на main
  (`ls scripts/tests/fixtures/stories/` в дереве main → `dry-codemie-14857`, `dry-types.json`). Пункты §11 «хэши, точка
  развилки, журнал в ветке» закрыты этим ревью (см. выше) — Lead вставляет в диспатч L1 эти цифры, а не старые.

---

## Ответы по ключам

- **K1 — отвечено.** Команды и выводы — B1, B4, F1. Чего §3 не видит: `form-rounds.json`, `test_field_producers.py` (B4);
  смысловой поверхности (F1); переписи (B1). Ошибочно названы как вероятные конфликты: `test-layers.json`, `slow_tests.json`,
  `form_filler.py`/`form-fill-rules.json`/`test_form_selftest.py` — main их не менял. Проверка §2 на шести строках (по деревьям
  main=42f5fcae / branch): N1 `dry_exits.py` 1657, `dry_stub.py` 580, `dry_world.py` 651, `known_red.py` 152 — верно; `known_red.json`
  на main `{}` / пин 0 — верно; N2 `form_filler.py` 1135 / 1288, `dry_driver.py` 82 — верно; N3 `scenario_walk.py` двери с
  `"driver"` на ветке (`:40`, `:48`) — верно; N6 `runners/` = только `python-pytest` — верно; ОТРИЦАТЕЛЬНАЯ: `test_scenario_dry`
  на main — `grep -rli` по `scripts/` = 0 файлов, контроль той же формы `test_scenario_cart` = 4 — верно. Ошибка §2 — N3t (F10).
- **K2 — отвечено.** Текстово L1 — один узел и тривиален (merge-tree чистый). Но DoD недостижим без L1c (B1); main краснеет в
  `full` на `dry-1/census` с момента слияния — дефект плана, не размеченное состояние. Зелёный ли режим по умолчанию на ветке
  сегодня: на верхушке ветки — **не установлено** (ни один отчёт не гонял режим по умолчанию после слияния s5stub и s1-s4;
  s5stub гонял `--part main` → `6/6 ok`, 385.1 с, остановка S5 под меткой; на слитом дереве перепись уже красная). Быстрые
  свидетели на слитом дереве зелёные: `dry_exits --selftest` 154/154 (1 с), `dry_stub --selftest` 189/189 (46 с),
  `test_form_selftest` 26/26 (9 с), `test_field_producers` 885/885 (22 с); `--witness-for` называет `test_scenario_dry_1.py`
  для трёх `dry_*.py` и `driver_machine.py` (DoD L1 (а) выполним). Потоки rules-debt S7/S8 (`exit_gate.py`, `gate-registry.json`)
  после L1 будут красить перепись при каждом новом стыке/отказе (F11 ниже по классу).
- **K3 — отвечено.** Носители: L2 шаг (1) — пишет Lead (файл + строка пачки, D-0044) до диспатча — для `main/S5`, `N4S0-1`,
  `N4S14-1` да; пропущена `P1B-2f` (B4); находка на F-P4 (в) не закреплена за исполнителем (B3).
- **K4 — отвечено.** F7: столкновение снимается, вторая дорога одна — `--judge`. Все читатели реестра (`dry_exits.py:654-655,2600`,
  `dry_world.py:715,976,1335`, `test_scenario_dry_1.py` `--ledger`) либо в owns N4R, либо работают без правки (прочитано).
- **K5 — отвечено.** Вердикт без локальных медленных файлов и без CI от билдера — да, через координатора; но только целым
  каноном (F3). Время задачи против часа канона не названо (F3).
- **K6 — отвечено.** L2, N4R, N2h, N4c написаны для слабой модели: файл/функция, края, ВРЕМЕННЫЕ и ПОЗИЦИОННЫЙ (N2h (6)) есть;
  оракулы — из `question-prices.json`, классов и контракта, не из вывода кода. Пробелы: класс F-P4 в карточке групп (F6),
  конфликтующая пара времени (F5), L1/L2 DoD (B1).
- **K7 — отвечено.** AR-28/20/22/15/17/29/13 названы верно и держатся; AR-14 пропущен (F8). Суждение роли код нигде не судит
  (C4г — наличие прохода; C10 — `pending judge`). Синхронизация заглушки с ролями — не названа (F8, F2).
- **K8 — отвечено.** F-P2 — правильно снят вопрос владельцу (действует builder-rules 7b). F-P3 — возможно деньги (F9).
  Остальное — Lead-класс. Строка решений противоречива (B3).
- **K9 — отвечено.** Волна 3 пересекается по `driver-exits/known_red.json` (F4); волна 4 — непересекающаяся, но после L1c (B1).
  Взятых пачек с пересечением нет: `live-run-fvf/2` (FV2-13 пишет `dry_exits.py`, `dry_stub.py`) и `forge/7` — «ожидает»
  (шапки прочитаны). Самоактивирующиеся файлы: хуков в owns нет; `nightly.yml` начинает действовать по расписанию на main сразу
  после волны — его кладёт Lead волной, ок.
- **K10 — отвечено.** F11 ниже.

### F11 — класс по карте (K10)

Новая симметрия, которую приносит L1: «любой стык (`stage_joints`/`null_outcomes`), строка реестра отказов, ключ цены или вид
драйвера в пакете ↔ строка переписи в `driver-exits/<g>.json` в том же коммите — иначе `full` красный». Улика — 228 молча
накопленных расхождений на main. В `docs/SIBLING_MAP.md` такой оси нет (Grep `driver-exits|dry_exits|census|перепис` -i: только
чужие переписи — оси 15, 16, 32, `state_census`; Grep `stage-joints|stage_joints|null_outcome|refusal_registry`: строка 138
(null outcomes ↔ required lists) и 570 — без переписи выходов). Правило 9: новая ось в карте тем же коммитом, что L1 (или L1c).
Оси узлов: 18 (храповики), 34 (одна дорога), 5 (двойники), 17, 30 — названы в спеке верно; ось 32 (judgment census) —
`scripts/tests/` вне её счёта, спека это говорит (`:69`).

---

## Не проверено

- Режим по умолчанию и `--part main` / `--part exits:*` `test_scenario_dry_1.py` на слитом дереве (медленный файл; по DoD ревью
  не гонял) — место остановки после слияния не установлено.
- `test_form_at_stop.py`, `test_form_view.py`, `selftest.py --limits --lang` на слитом дереве.
- Платность минут GitHub Actions (F9).
- Что именно меняют в стыках/отказах текущие потоки rules-debt S7/S8 (их ветки не читал).
- Рекурсивность `dry_exits.load` (N4R край 3 поручает билдеру; по `test_scenario_dry_1.py:51` `groups_found` — `glob("*.json")`,
  нерекурсивно; `load` не читал).
- R-L1…R-L10 (узел Lead) — не проверял.

## След

Прочитано: спека целиком (`:1-557`); `canon.yml` (origin/main, целиком до `clock`); `nightly.yml:17-112` и заголовки задач;
`tools/ci_read.py` (Grep WORKFLOW/start); `test_scenario_dry_1.py` (Grep, слитое дерево); `dry_exits.py:2585-2610` и Grep
читателей реестра; `test-layers.json:5105-5125` (слитое); отчёты ветки s5stub `:28-58`, n4wfix, n4g-s0, n4g-s1s4, n3 (Grep исходов);
`driver-exits/known_red.json` ветки; дифф ветки по `form-rounds.json`, `test_field_producers.py`, `selftest.py`, `slow_tests.json`;
журнал (accepted t-695…t-832); шапки `live-run-fvf/batch-2`, `forge/batch-7`; `docs/SIBLING_MAP.md` (Grep, оси); схема вердикта.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "B1: the dry census is red on the merged tree (dry_exits --check: 227 discrepancies; main 228, branch 0; joints 40 -> 267 on main) so test_scenario_dry_1 default mode turns full red at L1; L1 DoD (b) and L2 DoD unreachable; add node L1c (census catch-up, owns the six driver-exits group files, direction chosen by the Lead) before L2 in the same wave",
    "B2: no code critic before landing 4789 lines: every branch node was accepted with critic skipped for a topic critic at convergence, and the Lead text of F-P12 moves it after the group wave; take F-P12 (a) - one topic critic on origin/main...branch before the wave",
    "B3: the Lead decision line says all forks take (a) while F-P4 and F-P8 recommend (b) and the F-P12 text picks (b); L2 edge 4 branches on F-P4; write one decision line per fork",
    "B4: L1 owns miss two files the branch changes (fixtures/form-rounds.json, test_field_producers.py); form-rounds.json brings a fourth label P1B-2f with no finding file or pile row (grep plans: 0, control P1B-9: 74); add both to L1 owns and P1B-2f to L2 step 1"
  ],
  "fixes": [
    "F1: rewrite section 3 - merge-tree is clean (tree ba076a5d), only selftest.py changed on both sides in disjoint hunks; the real surface is semantic (190 main commits, 91 product scripts and references)",
    "F2: L2 edge - a stop caused by the stub lagging main is fixed in the stub, not labelled as a product finding; raised_by names stub gap vs product gap",
    "F3: N5 - keep a dry-only door (a boolean input in canon.yml or a reusable dry-story.yml) so a group verdict is not a whole canon; state the job time against the canon hour",
    "F4: wave 3 overlap - N2h edge 7 writes driver-exits/known_red.json owned by N4R; N2h reports only",
    "F5: name the conflicting pair F-P5 ceiling 900 vs N2h pushing the pass past S5 with mutation probes",
    "F6: group card - add the F-P4 class edge for conditionally offered options; pre-issue finding ids for expected reds (FV1-7, FV1-8)",
    "F7: N4R edge 6 - dry_exits --judge keeps reading only the common file and answers wrongly for group rows; remove it or teach it the group file",
    "F8: section 1 - name AR-14 (one writer per group ledger) and the stub-vs-role sync detector",
    "F9: F-P3 adds nightly CI minutes; if they are billed it is the owner's money question - Lead confirms",
    "F10: section 2 N3t - dry-codemie-14857 exists on main; section 11 git facts are now measured (merge-base e18e622f, branch 9c9d40c2, no journal lines on the branch)",
    "F11: add a SIBLING_MAP axis - a new joint, refusal row, price key or driver kind needs its census row in driver-exits in the same commit, in the commit of L1 or L1c"
  ],
  "class_completeness": "Not complete: L1 brings a new symmetry (package joints, refusal rows, price keys, driver kinds <-> the dry census rows in driver-exits/<g>.json) with no SIBLING_MAP axis (grep driver-exits|dry_exits|census -i: none for this census); evidence - 228 silent discrepancies on main. Axes 18, 34, 5, 17, 30 named by the spec are right; axis 32 excludes scripts/tests as the spec says. Analogs: four labels need carriers, not three (P1B-2f); the F-P4 class recurs in the remaining groups.",
  "trail": {
    "read": [
      "docs/tasks/specs/20261117-p1b-finish-spec.md:1-557",
      ".github/workflows/canon.yml (origin/main, start to clock)",
      ".github/workflows/nightly.yml:17-112 and job headers",
      "tools/ci_read.py (grep WORKFLOW, start)",
      "tools/critic_verdict.schema.json",
      "wip/p1b-n4m reports 20261114-p1b-{s5stub,n4wfix,n4g-s0,n4g-s1s4,n3}-report.md (grep of outcomes; s5stub 28-58)",
      "wip/p1b-n4m fixtures/driver-exits/known_red.json",
      "merged tree scripts/tests/test_scenario_dry_1.py (grep), dry_exits.py:2585-2610, test-layers.json:5105-5125",
      "logs/journal/*.jsonl accepted events t-695..t-832",
      "plans/piles/live-run-fvf/batch-2 header and FV2-13, plans/piles/forge/batch-7 header",
      "docs/SIBLING_MAP.md (grep, axis list, lines 138 and 153)"
    ],
    "reruns": [
      {"command": "git -C C:/QAFactory/forge-repo merge-base origin/main wip/p1b-n4m", "result": "e18e622f (2026-11-14 07:14, t-819); 190 commits on main, 24 on the branch since"},
      {"command": "git -C C:/QAFactory/forge-repo merge-tree --write-tree --name-only origin/main wip/p1b-n4m", "result": "ba076a5d, rc 0, no conflicted files"},
      {"command": "comm -12 of diff --name-only e18e622f..wip/p1b-n4m and e18e622f..origin/main", "result": "only ai-packages/qa-factory/scripts/selftest.py, disjoint hunks"},
      {"command": "python -B scripts/tests/dry_exits.py --check (merged tree)", "result": "227 discrepancies; branch tree 0 (joints 40); main tree 228 (joints 267)"},
      {"command": "python -B scripts/tests/dry_exits.py --selftest (merged tree)", "result": "154/154 cases, 1 s"},
      {"command": "python -B scripts/tests/dry_stub.py --selftest (merged tree)", "result": "189/189 ok, 46 s"},
      {"command": "python -B scripts/tests/test_form_selftest.py (merged tree)", "result": "26/26 ok, 9 s"},
      {"command": "python -B scripts/tests/test_field_producers.py (merged tree)", "result": "885/885 ok, 22 s"},
      {"command": "python -B scripts/tests/scenario_walk.py --witness-for dry_world.py dry_exits.py dry_stub.py form_filler.py driver_machine.py (merged tree)", "result": "test_scenario_dry_1.py named for the three dry_*.py and driver_machine.py"},
      {"command": "Grep -i P1B-2f|N4S0-1|N4S14-1|N4W-1 in plans/ with control P1B-9|FV1-14", "result": "0 matches; control 74 in 19 files"}
    ]
  }
}
```
