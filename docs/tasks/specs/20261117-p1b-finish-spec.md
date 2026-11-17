# П1-б: довести сухую стори до «идёт в CI на main». ЧЕРНОВИК ДИЗАЙНЕРА (t-944), ФИКС-РАУНД ПО КРИТИКУ t-955

Статус: черновик дизайнера (Opus) по брифу Lead 17.11.2026 (слово владельца 17.11: «всё что недоделанно делаем сегодня»),
исправлен фикс-раундом 17.11 по вердикту критика на план t-955 (`docs/tasks/specs/reviews/t-955-p1b-finish-plan.md`,
`fit_with_fixes`: 4 блокера B1–B4, 11 правок F1–F11). Все замечания закрыты в этом раунде, в очередь ничего не отложено;
таблица исправлений — §12. До приёмки Lead — не диспатч. Развилки — §7: три старые развилки открыты заново (B3), новые
F-P14…F-P20; ни одна не закрыта дизайнером. Мелкие решения дизайнера — §8, строки кучки — §9, след чтения — §10,
«не сделано / не перемерено» — §11. Денежных цифр нет.

Обозначения. `PKG` = `ai-packages/qa-factory`; `T` = `PKG/scripts/tests`. `MAIN` = корень клона `C:\QAFactory\forge-repo`.
Перемер фикс-раунда 17.11 (чтением файлов, git-команд у дизайнера нет): `.git/refs/remotes/origin/main` и
`.git/refs/heads/main` оба = `7103829adfdff5c6ac8ad1d5a1a278dd7ccce359` (коммит «architect streams B-F merged; reviews t-955;
…»); рабочее дерево корня — `main` на этом коммите (git status сессии: только неотслеживаемые), поэтому файлы корня читаются
как `origin/main` = `7103829a`. `wip/p1b-n4m` = `9c9d40c2a1bd62f2b999ddd66e25f3073cbf20e3` (`.git/packed-refs:34`; рыхлого
рефа нет — Glob `.git/refs/heads/**` находит только `main` и `worktree-agent-*`). `N4M` =
`C:\QAFactory\forge-repo\.claude\worktrees\p1b-n4m` (HEAD = `ref: refs/heads/wip/p1b-n4m`). Точка ветвления `e18e622f`,
чистый `merge-tree` (дерево `ba076a5d`), 47 файлов / 4789+ / 133− — измерены критиком t-955 против `origin/main` = `42f5fcae`;
против нынешнего `7103829a` — **не перемерено** (команды — §3).

Спеки-основания: P1-b `docs/tasks/specs/20261113-p1b-dry-story-spec.md` (дальше «П1-б»); N4w
`docs/tasks/specs/20261114-p1b-n4w-exit-walker-spec.md` («N4w-спека»); поправка
`docs/tasks/specs/20261113-p1-specs-amendment-owner-words.md` («A1/A2»).

---

## 0. Вердикт коротко

1. На `main` стоит только N0/N1-слой: `dry_exits.py` (1657 строк), `dry_stub.py` (580), `dry_world.py` (651),
   `known_red.py` (152), перепись `fixtures/driver-exits/` (8 файлов, реестр меток пуст), `fixtures/stories/dry-types.json`,
   `fixtures/stories/dry-codemie-14857/`, `fixtures/dry-walk/seeds/probe.json`, задача CI `dry-story-spike`
   (`.github/workflows/canon.yml:64-81`). Ни `test_scenario_dry_1.py`, ни двери `driver`, ни истории `dry-1`, ни строки
   `keep` на `main` нет — сухая стори в каноне сегодня НЕ идёт вообще. (Счёт строк перемерен на `7103829a` — §2.)
2. Всё сделанное после N1 живёт в ОДНОЙ ветке `wip/p1b-n4m` (N2, N3, N4w + фикс, N4:s0, N4:s1-s4, заглушка S5).
3. **Перепись выходов красная на слитом дереве (B1).** На `main` стыков `stage-joints.json` 267 (перемерено: Grep `"check":`
   count = 267 на `7103829a`), на ветке перепись знает 40; `dry_exits.py --check` на слитом дереве t-955 = 227 расхождений
   вида «the driver has it and no row names it». Режим по умолчанию `test_scenario_dry_1.py` зовёт эту перепись, поэтому
   посадка без догоняющего узла красит `full` на `main`. Новый узел **L1c** догоняет перепись на той же ветке, ДО волны.
4. Четыре метки реестров, а не три (B4): `main/S5 -> P1B-9` (устарела), `N4S0-1`, `N4S14-1` (реестр `driver-exits`) и
   `P1B-2f` (реестр П1-а `fixtures/form-rounds.json:70`) — ни у одной нет файла находки и строки пачки. Узел Lead **L0**
   заводит находки и пачку ДО L1; L2 переписывает метки.
5. **Критик кода перед посадкой (B2).** 4789+ строк ветки приняты узлами с отказом от критика «до критика темы на
   сходимости»; посадка и есть сходимость. Узел **CR-L** — один критик темы «посадка П1-б» на дифф
   `origin/main...<ветка посадки>` ДО волны (по рекомендации F-P12 (а); развилка открыта заново — B3, §7).
6. Части обхода `--part exits:<g>` дороже минуты (110-385 с) и по builder-rules 7b локально не гоняются. N5 даёт задачу CI
   и ДВЕРЬ «только сухая стори» (F3), чтобы вердикт группы не стоил целого канона.
7. Реестр меток — файл на группу (F-P1 (а), решение Lead), узел N4R до групп.

Порядок (§5): **L0 → L1 → L1c → L-ax → CI-1 → L2 → CI-2 → CR-L (→ фикс-раунд) → проверка перед волной → волна 1 в `main`** →
{N4R, N5, N2h-а} параллельно; N2h-б после N4R в `main` → {N4:gates, N4:s5, N4:s6-s9} параллельно → критик темы групп → N4c →
{N6, N3t, N3a}. Инвариант всего порядка: **`main` не краснеет ни после одного слияния этого плана** (каждая волна сливается
только с зелёным `dry_exits --check` на дереве волны и зелёным каноном на её ветке; §5).

---

## 1. Инварианты AR-n, владельцы проверок, классы (CLAUDE.md правило 10, роль дизайнера правило 1)

Узлы пишут `PKG/scripts/tests/`, данные расписания тестов (`PKG/scripts/selftest.py` словарь `TEST_TIMEOUTS`,
`PKG/scripts/slow_tests.json`), `PKG/changelog.d/`, `.github/workflows/`, `tools/test_workflows.py`; узлы Lead — ещё
`plans/piles/live-run-fvf/` (L0) и `docs/SIBLING_MAP.md` (L-ax). Код продукта вне `scripts/tests/` не меняется ни одним
узлом. «Держит» = слой становится детектором инварианта или соблюдает его внутри тестового слоя.

| AR | Что делает эта спека | Проверка изменения (в DoD узла) |
|---|---|---|
| AR-28 (неизвестное не проходит) | L2: остановка главного прохода — только на строке реестра с живой находкой; N4R: отсутствующий файл реестра группы = пустой реестр, красная строка без метки = FAIL «new red»; N5: группа без своего файла обхода не выпадает молча; L1c: строка переписи пишется ТОЛЬКО для субъекта, который `--check` назвал «no row names it», — ничего «на всякий случай» | L2: вывод CI `NOTE dry-1/main/known_red: known red: main/S<n> -> <id>` и ни одной FAIL; N4R: строка таблицы `dry_exits.py --selftest` «absent group ledger -> empty -> unlabeled red is FAIL»; L1c: `dry_exits --check: 0 discrepancies` и число добавленных строк = число строк «no row names it» L1 (отчёт) |
| AR-20 (храповики убывают) | L1c поднимает счёт `unwalked` ТОЛЬКО строками `ratchet.raised_by` (одна на строку, по F-P14 (а)); группы N4 понижают базы `unwalked` в СВОЁМ файле; рост `live_only` — только строкой `raised_by`; N4c сжимает `PINNED_ELSEWHERE` | `dry_exits.py --check` = `0 discrepancies` и NOTE `ratchet unwalked: raised N row(s) above the base B, named in raised_by` (L1c); каждая группа — `0 discrepancies`; N4c: из `PINNED_ELSEWHERE` удалены ровно ключи `dry_exits.driven_keys()` |
| AR-22 (поле читается — у него писатель) | N4R: у каждого файла реестра группы один писатель (узел группы) и два читателя (`exits_part`, `_ledger_orphans`) в одном коммите; N2h: запись пробы `work/probes/<IID>.json` пишет настоящий `probe_by_code.py`, читатель — заполнитель `world_list` | N4R: строка таблицы «orphan in group ledger -> red»; N2h: строка `dry_stub.py --selftest` «critic branch ran probe_by_code; record exists» |
| AR-14 (один артефакт — один писатель) (F8) | N4R создаёт `driver-exits/known_red/<g>.json`: писатель файла группы — только узел своей группы; общий `known_red.json` после N4R пишет только узел, меняющий строку `main/*` (L2, затем N2h-б), и никогда два узла одной волны; L1c — единственный писатель строк переписи в волне 1 | N4R: строка таблицы «the same id in two ledger files is red with both paths»; §5: ни одна пара параллельных узлов не делит файл (таблица §5, колонка «общие файлы») |
| AR-15 (один выживший) | одна задача CI сухой стори (N5, `dry-story.yml` по F-P16 (а)) вместо спайка, два вызова (ночь и дверь канона); одна перепись ключей вопросов (`test_conductor_doors.py`, N4c); один помощник меток (`known_red.py`, не меняется); одна дорога суда реестра (`--judge` убирается, F-P17 (а)) | N5: `tools/test_workflows.py` строки «canon has no spike input and no dry-story-spike job», «dry-story.yml is called by nightly and by canon's dry_only door» |
| AR-17 (одна дверь к дирижёру) | ни один узел не присваивает атрибут `Driver`; заглушка — на границе процесса | грep `driver\.[a-z_]+ =` по owns узла пуст; положительный контроль — `PKG/scripts/tests/test_stage_critic_route.py:279` (П1-б `:47`) |
| AR-29 (код судит данные) | исход каждой строки обхода задан строкой (вердикт заглушки, ход дирижёра), не вычислен; N2h запускает настоящий инструмент роли, не придумывает вердикт пробы; L1c пишет строки переписи механически из вывода `--check` по правилу группы (§4 L1c п. 2), без суждения о стыке | грep `result_text|brief` по новым функциям owns пуст (положительный контроль `T/dry_stub.py` `result_text`, N4w-спека §1) |
| AR-13 (факт через свою функцию) | реестр меток читается только `known_red.load/reconcile`; готовность гейта — `dry_world.gate_ready`; стыки — только `null_outcomes.load_data(stage_joints.DATA)` (`dry_exits.scan_joints`, `:502-512`) | N4R: грep `json.load` по путям реестра в owns пуст (кроме `known_red.py`); L1c не читает `stage-joints.json` в обход `scan_joints` (правило группы берёт `stages` строки через тот же загрузчик) |

Не тронуты (по строке): AR-1…AR-12 (кроме AR-1 внутри слоя: группы, файлы реестров, правило группы стыка по `stages` —
данные), AR-16, AR-18 (форма вывода ходока не меняется), AR-19, AR-21, AR-23…AR-27 — продукт не меняется.

**Синхронизация заглушки с поведением ролей (F8).** Заглушка и перепись — тестовый слой, который отстаёт молча, когда `main`
меняет роли, стыки, маршруты или ключи (улика — 228 расхождений, накопленных с 14.11). Детекторы, все на пути `full`:
(1) перепись — строка `dry-1/census` режима по умолчанию (`test_scenario_dry_1.py:28-34` → `dry_exits.check()`); с N5 также
шаг `dry_exits.py --check` задачи `dry-story` (5 с, дверь «только сухая стори»); (2) место остановки главного прохода —
`dry-1/main/stop` против метки `main/S<n>` (`known_red.reconcile`: «stale», когда проход ушёл дальше, «new red», когда встал в
новом месте); (3) таблицы `dry_stub.py --selftest` (шаг задачи `dry-story`, F-P6 (а)). Класс метки: поле `raised_by` каждой
строки реестра, которую пишет эта спека, начинается с `stub gap:` (причина в тестовом слое; чинит узел заглушки) или
`product gap:` (причина в продукте; чинит узел находки) — F2, §8. Новая ось карты (F11) — §4 L-ax.

Строки коммита пакета: форма строк `architecture:` и `judgment:` — ТОЛЬКО по `tools/architecture_gate.py` (грамматику
здесь не копирую). Каждый узел, трогающий `PKG/`, называет в `architecture:` AR-n своей строки таблицы выше;
`judgment: none` пишется только с ` -- <почему>` (например: «тестовый слой, суждений роли не проверяет»).
Коммит `docs/SIBLING_MAP.md` (L-ax) — механизм: блок осей по ВСЕМ осям карты (с новой осью 38) и строка `tier:` уровня Lead
(`tools/mechanism_gate.py`), поэтому его делает Lead, не билдер.

### Проверки, которые спека добавляет или меняет: владелец (P27) и класс (AR-29)

`test_judgment_census.py` не считает `scripts/tests/` (П1-б `:71-73`); классы — для вопроса 11 критика.

| # | Проверка | Узел | Владелец | Класс |
|---|---|---|---|---|
| K-C | Каждый стык/маршрут/вид, который есть у драйвера, назван строкой переписи; рост `unwalked` назван `raised_by` | L1c (данные строк; проверка — существующая `dry_exits.check`) | данные (код); направление F-P14 — Lead | presence + shape |
| K-L | Остановка главного прохода есть строка `main/S<n>` реестра, её `node` — узел пачки с файлом находки; `raised_by` называет класс `stub gap`/`product gap` | L2, N2h-б | данные (код); чья находка и её класс — Lead | presence |
| K-R1 | Строка реестра группы называет id строки из `exits/<g>.json` той же группы | N4R | данные | xref |
| K-R2 | Пин `pins.known_red` равен числу строк файла (существующая проверка `known_red.pin_problem`, теперь на файл) | N4R | данные | shape |
| K-P | Заглушка критика S5 запускает `probe_by_code.py` на каждый экземпляр окна; запись есть до формы | N2h | данные | presence |
| K-CI | Задача CI гоняет каждую группу, у которой есть `exits/<g>.json`, `dry_exits.py --check` и чистые таблицы `dry_exits.py --selftest`, `dry_stub.py --selftest` | N5 | данные | presence |
| K15/driven | Ключи сухой стори входят в `driven` переписи; `PINNED_ELSEWHERE` сжимается | N4c | данные | xref |
| C2…C9 | Проверки строк обхода (как построены N4w) | N4:<g> | как N4w-спека §1 (C4г — замысел владельца P13/FR-4, код проверяет только наличие прохода и записи) | как N4w-спека §1 |
| CR-L | Суждение о диффе посадки (архитектура, смысл, дубли, качество) | CR-L | суждение (роль critic), принимает Lead | не проверка кода — вне счёта |

Суждение (годится ли строка, баг ли красный, хорош ли ход дирижёра, класс метки) кодом не проверяется нигде — П2-г, критик,
живой прогон, Lead.

### Оракул каждой новой строки теста

- Строки обхода N4: ожидаемое — из строки обхода, заданной по `PKG/references/question-prices.json` (варианты ключа), по
  П1-б §3.3/§3.6 (класс ГЕЙТ/ЗАПРЕТ из `fixtures/driver-exits/classes.json`), по `expect.owner_quote` с носителем (E14) —
  никогда не из вывода прогона. Красная строка получает метку только с находкой (файл + строка пачки), не «как сейчас».
- L1c: ожидаемое — множество субъектов, которые `dry_exits.check()` называет «no row names it» (производитель — драйвер и
  `stage-joints.json` через `scan_joints`); группа стыка — по его `stages` (§4 L1c п. 2), не по выводу прогона.
- N4R: ожидание таблицы — правило «id реестра группы ⊂ id строк той же группы» (§4 N4R край 4) и равенство пина
  (`known_red.py` `_about`, `fixtures/driver-exits/known_red.json:2`).
- N2h: ожидание — «запись пробы есть для каждого экземпляра окна» (контракт `s5-critic-to-automator`, поле
  `probes.records`, `T/test_handoff.py:144` его называет; `probe_by_code.py:19` пишет `work/probes/<IID>.json` — по отчёту
  s5stub `N4M/docs/tasks/specs/reports/20261114-p1b-s5stub-report.md:47`).
- N5: ожидание — строки `tools/test_workflows.py` из текста этой спеки (имена задач, `if`, `needs`, вход `dry_only`), не из YAML.
- N4c: ожидание — множество `dry_exits.driven_keys()` (производитель N1/N4w), а не список, собранный из вывода переписи.

---

## 2. Состояние, измеренное 17.11 (по чтению деревьев)

Метод: Glob/Grep по `MAIN` и `N4M`; счёт строк — Grep `^` count; отсутствие — с положительным контролем той же формы (§10).

**Перемер фикс-раунда на `origin/main` = `7103829a`** (после слияния Architect streams B–F и rules-debt фазы 1): счёт строк
совпал со столбцом «main» ниже для `dry_exits.py` 1657, `dry_stub.py` 580, `dry_world.py` 651, `known_red.py` 152,
`harness.py` 535, `form_filler.py` 1135, `form-fill-rules.json` 373, `test_form_selftest.py` 79, `scenario_walk.py` 935,
`test-layers.json` 10718; `selftest.py` 1465 (ветка 1467), `slow_tests.json` 156 (ветка 157), `form-rounds.json` 123
(ветка 124), `test_field_producers.py` 1580 (ветка 1580); `stage-joints.json` — 267 строк `"check":`; `canon.yml` — всё ещё
вход `spike` и задача `dry-story-spike` (прочитан целиком). Совпадение счёта строк — не доказательство неизменности
содержимого: содержимое против `42f5fcae` — **не перемерено**.

| Узел | На `origin/main` (носитель) | Только на ветке (ветка, файлы) | Нет нигде |
|---|---|---|---|
| N0 спайк | `T/dry_world.py` (651 стр., `--spike`), `T/dry_stub.py` (580), `T/fixtures/dry-walk/seeds/probe.json`, `T/fixtures/stories/dry-types.json`, `.github/workflows/canon.yml:35-40,64-81` (вход `spike`, задача `dry-story-spike`); отчёты `docs/tasks/specs/reports/20261113-p1b-n0-*.md` | — | — |
| N1 перепись | `T/dry_exits.py` (1657), `T/known_red.py` (152), `T/fixtures/driver-exits/{classes,gates,hooks,s0,s1-s4,s5,s6-s9,known_red}.json`; `known_red.json:3-4` = `{}` / пин 0; перепись знает 40 стыков из 267 (t-955: `main` 228 расхождений) | — | — |
| N2 заглушка, история (N2…N2g) | — | `wip/p1b-n4m`: `T/dry_driver.py` (82, новый), `T/dry_stub.py` (1627), `T/form_filler.py` (1288 против 1135), `T/fixtures/form-fill-rules.json` (398 против 373), `T/test_form_selftest.py` (126 против 79), `T/fixtures/form-rounds.json` (124 против 123: метка `P1B-2f`, `:70`), `T/test_field_producers.py` (ожидание `obligation_refs` без хэша, t-955 `:775-779`), `T/fixtures/stories/dry-1/{story.json,kit.json,impl.diff,ticket/DRY-1.md,runners/python-pytest/…}`, `PKG/changelog.d/p1b-n2-dry-stub.md`; отчёты `N4M/docs/tasks/specs/reports/20261114-p1b-n2*-report.md` | находка `P1B-2f` (Grep `-i` по `plans/` — 0 на `7103829a`, контроль `P1B-9|FV1-14` — 74 в 19 файлах) |
| N3 дверь, главный проход | на main грep `test_scenario_dry` по `PKG/scripts` — 0 (контроль `test_scenario_cart|test_scenario_local` — 12 строк); `T/scenario_walk.py:40` без `driver` | `wip/p1b-n4m`: `T/test_scenario_dry_1.py` (новый), `T/scenario_walk.py:40,48` (`driver`), `T/test-layers.json:5109-5123` (строка `keep`), `PKG/scripts/selftest.py:115-117` (`TEST_TIMEOUTS` 900), `PKG/scripts/slow_tests.json:119` (51.0), `PKG/changelog.d/p1b-n3-driver-door.md` | — |
| N4w ходок (+ фикс t-828) | — | ходок: `wip/p1b-n4m` (`T/dry_world.py:1279` `walk_exits`, `T/dry_exits.py:1328` `judge_group`, `T/test_scenario_dry_1.py:80` `exits_part`, `T/fixtures/stories/dry-1/selftest/{exits,seeds}/selftest.json`, `.../selftest/known_red.json`, `PKG/changelog.d/p1b-n4w-exit-walker.md`); фикс (изоляция `--selftest`, `alive` под меткой) — ТОЛЬКО `wip/p1b-n4m` | — |
| N4:s0 | — | `wip/p1b-n4m`: `T/fixtures/stories/dry-1/exits/s0.json` (10 строк), `.../seeds/s0.json`, `T/fixtures/driver-exits/s0.json` (83 против 66), строка реестра `kind:halt/free words -> N4S0-1` (`N4M/.../driver-exits/known_red.json:5`) | находка `N4S0-1` |
| N4:s1-s4 | — | `wip/p1b-n4m`: `.../exits/s1-s4.json` (11 строк), `.../seeds/s1-s4.json` (`recipes: {}`), `T/fixtures/driver-exits/s1-s4.json` (93 против 79), строка `s1.review/unavailable -> N4S14-1` (`known_red.json:6`) | находка `N4S14-1` |
| Заглушка S5 (s5stub) | — | `wip/p1b-n4m`: `T/form_filler.py:77,316,447-463` (`task_root`, `world_list`), `T/fixtures/form-fill-rules.json:31`, `T/test_form_selftest.py:79-80`, `T/dry_stub.py` (`kit_context(task_root=…)`) | запуск `probe_by_code.py` заглушкой (отчёт s5stub `:47`) |
| N4:gates | перепись `T/fixtures/driver-exits/gates.json` (101 стр., 21 запись `unwalked`, `:94-100`) | дерево `p1b-n4-gates`: уровень N3 — нет `exits_part`/`walk_exits`/`judge_group` | строки обхода `exits/gates.json` |
| N4:s5 | перепись `driver-exits/s5.json` (149) | — | строки обхода |
| N4:s6-s9 | перепись `driver-exits/s6-s9.json` (55) | — | строки обхода |
| N4c | `T/test_conductor_doors.py:636` `PINNED_ELSEWHERE`, `:670` `census_problems`; `test-layers.json:672` keep | — | правка |
| N5 | только `dry-story-spike` (`canon.yml:64-81`, перечитан на `7103829a`) | — | задача `dry-story` |
| N6 | — | — | `stories/dry-1/runners/ts-playwright/` |
| N3t | `dry-types.json:1-14` (`default: codemie-14857`, вход `dry-codemie-14857`); каталог `T/fixtures/stories/dry-codemie-14857/` ЕСТЬ (`story.json`; Glob на `7103829a`; F10) | — | — |
| N3a | — | — | функция `told_before_work`; поправка A2 называет файл `test_scenario_dry.py`, построен `test_scenario_dry_1.py` |
| N-L (R-L1…R-L10) | R-L3: `PKG/design/architecture.md:192` содержит `NO_MOVE_BASELINE_MAX` (по чтению t-944; на `7103829a` после Architect streams — **не перемерено**) | — | R-L2, R-L4…R-L10 — по t-941 не начаты (не перечитано) |

Пачки: ни один узел П1-б не стоит строкой пачки. В `plans/piles/live-run-fvf/` на `7103829a` — `batch-1`, `batch-2`
(обе «ожидает», README `:23-24`), `batch-3` нет (Glob). Связанные строки: `forge/7` FG7-15, FG7-19, FG7-38 — «ожидает»;
`live-run-fvf/2` FV2-13 (пишет `dry_exits.py`, `known_red.py`, `dry_stub.py`); пачка `package-ci/4` — «ожидает»
(статусы этих строк на `7103829a` — **не перемерены**, по чтению t-944/t-955).

---

## 3. Поверхность посадки (F1: переписано)

**Текстовая поверхность** (t-955 против `42f5fcae`): `git merge-tree --write-tree --name-only origin/main wip/p1b-n4m` →
дерево `ba076a5d`, rc 0, конфликтов нет. Обе стороны после точки ветвления `e18e622f` меняли только
`PKG/scripts/selftest.py`, ханки не пересекаются (main `:355-359` `REFERENCE_MD_MAX_BYTES`, ветка `:112-117` `TEST_TIMEOUTS`).
`main` не трогал `test-layers.json`, `slow_tests.json`, `form_filler.py`, `form-fill-rules.json`, `test_form_selftest.py`,
`dry_*.py`, `scenario_walk.py`, `form-rounds.json`, `test_field_producers.py`. Ветка журнала не несёт (`logs/` в списке
файлов нет).

Против нынешнего `origin/main` = `7103829a` (сегодня слиты Architect streams B–F и rules-debt фаза 1) — **не перемерено**.
Команды Lead до диспатча L1 (вывод вставляется в диспатч дословно):
`git -C C:\QAFactory\forge-repo fetch origin`,
`git -C C:\QAFactory\forge-repo merge-tree --write-tree --name-only origin/main wip/p1b-n4m`,
`git -C C:\QAFactory\forge-repo diff --stat origin/main...wip/p1b-n4m`,
`git -C C:\QAFactory\forge-repo log --oneline e18e622f..origin/main -- ai-packages/qa-factory/references/stage-joints.json ai-packages/qa-factory/scripts/driver_dispatch.py ai-packages/qa-factory/scripts/no_move.py ai-packages/qa-factory/scripts/refusal_registry.py`
(последняя — что ещё сдвинуло вселенную переписи).

**Смысловая поверхность** — настоящая (t-955 F1): 190 коммитов `main` после развилки, 562 файла, из них 91 — скрипты и
`references/` продукта (`driver_core.py`, `driver_stage_*.py`, `handoff_check.py`, `probe_by_code.py`, `brief_pack.py`,
`profile_contract.py`, `controller.py`, `stage_guard.py`, слайсы контрактов) — плюс сегодняшние слияния (не перемерено).
Её меряют: перепись (`dry_exits.py --check`, 5 с, локально — L1/L1c), место остановки главного прохода (CI — CI-1/L2) и
быстрые свидетели L1 на итоговом дереве. Пересечения по смыслу: P1B-9 (C1-C4 + фикс-раунд t-831) слит на `main`, ветка несёт
C1-C4 без фикс-раунда; на `main` есть `PKG/scripts/null_outcomes.py`; место остановки главного прохода после слияния может
сдвинуться — его меряет CI (L2).

---

## 4. Узлы

**Свидетель любого узла** (builder-rules 7b, CLAUDE.md правило 4): `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <owns>`
печатает список; ЛОКАЛЬНО гоняются только файлы до минуты. **Медленные файлы** — `test_scenario_dry_1.py` в любом режиме (по
умолчанию ~385 с, части 110-385 с — отчёты N2g `:43`, s5stub `:40`, N4:s0 `:43`, N4:s1-s4 `:40`) и `test_conductor_doors.py`
(53.0 с, `slow_tests.json:20`): если `--witness-for` их называет, отчёт пишет строку «`<файл>` — судит канон пачки» и НЕ
запускает их локально; их задачу запускает и читает координатор (`python -B tools/ci_read.py start --ref <ветка>`,
`python -B tools/ci_read.py why`), билдер CI не запускает и не ждёт (PROJECT.md «Командная работа» п. 13). Быстрые, но не
мгновенные: `dry_stub.py --selftest` (46 с), `test_field_producers.py` (22 с), `test_form_selftest.py` (9 с) — t-955 на
слитом дереве; любой свидетель дольше минуты на машине билдера — строка отчёта с секундами, без повтора. Новых тестовых
файлов ни один узел не создаёт; новый случай — строка таблицы `--selftest` своего модуля или строка обхода (TESTING.md
«Бюджет / Файлы» `:117`; исключение сухой стори по времени — TESTING.md `:130-132`).

### L0 — находки и пачка (узел Lead; до диспатча L1) (B4)

Исполнитель: Lead (находки и строки пачек — работа Lead по PROJECT.md «Командная работа» п. 2 и D-0044; не диспатч).
owns:
C:\QAFactory\forge-repo\plans\piles\live-run-fvf\batch-3-live-run-fvf.md (новый; шапка и строки §9)
C:\QAFactory\forge-repo\plans\piles\live-run-fvf\README.md (строка таблицы «Пачки» и строки «Содержание» для каждого файла ниже)
C:\QAFactory\forge-repo\plans\piles\live-run-fvf\findings\20261117-p1b-2f-obligation-refs-hesh-trebuet-i-otkazyvaet.md (новый; бывшая метка `P1B-2f`)
C:\QAFactory\forge-repo\plans\piles\live-run-fvf\findings\20261117-p1b-s0-halt-svobodnye-slova-ne-dohodyat.md (новый; бывшая `N4S0-1`)
C:\QAFactory\forge-repo\plans\piles\live-run-fvf\findings\20261117-p1b-uslovnyj-otvet-bez-usloviya-u-hodoka.md (новый; бывшая `N4S14-1`, класс F-P4 — текст по решению F-P4)
C:\QAFactory\forge-repo\plans\piles\live-run-fvf\findings\20261117-p1b-s5-zaglushka-kritika-ne-zapuskaet-probu.md (новый; остановка `main/S5`, `stub gap`, узел FV3-5)
C:\QAFactory\forge-repo\plans\piles\live-run-fvf\findings\20261117-p1b-probes-records-bez-pustogo-ishoda.md (новый; `product gap`: у вложенного списка `probes.records` нет объявленного пустого исхода, `handoff.py:515-533`, отчёт s5stub `:49-50`)
Что пишет: (1) `batch-3-live-run-fvf.md` со статусом «ожидает» и строками §9 (FV3-1…FV3-19); (2) строку «Пачки» и строки
«Содержание» в `README.md` (без них `tools/test_pile_cards_contents.py` красит `forge-check`); (3) пять файлов находок — по
форме соседних `findings/` (класс фабрики, не правило проекта; источник — отчёт с номером строки: n2f gap candidate 8 и
`form-rounds.json:70` note; n4g-s0 `:67`; n4g-s1s4 `:55`; s5stub `:43-50`); (4) id меток, которые отдаёт L2: `main/S5 ->
FV3-5`, `kind:halt/free words -> FV3-16`, `s1.review/unavailable -> FV3-17` (только при F-P4 (а)), `obligation_refs <- … ->
FV3-18` (при F-P19 (а)). Слово «пачка 2 полна» — по решению Lead F-P13 (а).
edges: (1) находка `halt` — причина не установлена (драйвер или стык заглушки, отчёт n4g-s0 `:67`): класс в `raised_by`
метки — `product gap` до разбора, разбор — узел FV3-16; инвариант: метка никогда не утверждает класс, которого никто не
установил — текст находки говорит «причина не установлена»; (2) F-P19 (б) (убрать строку `P1B-2f`) → файл
`…-p1b-2f-…` не пишется, строка FV3-18 не заводится, L2 удаляет строку `form-rounds.json:70` только если CI/свидетель
показывает, что противоречие больше не воспроизводится (иначе `test_field_producers.py` краснеет «new red»);
(3) ВРЕМЕННОЙ: до L0 строк FV3-* нет и `piles.py take live-run-fvf 3` невозможно; L0 — первый ход, взятие пачки — после него.
DoD: `python -B tools/piles.py check --all` — без строк про `live-run-fvf`; `python -m pytest tools/test_pile_cards_contents.py -q` — зелёный.
siblings: ось 12 (носители плана: пачка ↔ карточка ↔ «Содержание»).

### L1 — посадка `wip/p1b-n4m` в `main` (текстовая; без перепись-правок)

given: эта спека §2, §3; вывод четырёх git-команд Lead из §3 (дословно); `N4M/docs/tasks/specs/reports/20261114-p1b-n3-report.md`, `…-n4w-report.md`, `…-n4wfix-report.md`, `…-n4g-s0-report.md`, `…-n4g-s1s4-report.md`, `…-s5stub-report.md`, `…-n2f-report.md`; `C:\QAFactory\forge-repo\plans\builder-rules.md` (7b, 18, 19); `C:\QAFactory\forge-repo\ai-packages\qa-factory\design\factory-rules.md` (целиком); `C:\QAFactory\forge-repo\docs\TESTING.md`
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\dry_exits.py
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\dry_stub.py
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\dry_world.py
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\dry_driver.py (новый на main)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_scenario_dry_1.py (новый на main)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\scenario_walk.py
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test-layers.json (только строка keep `test_scenario_dry_1.py`)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\selftest.py (только строка `TEST_TIMEOUTS["test_scenario_dry_1.py"]`)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\slow_tests.json (только строка `test_scenario_dry_1.py`)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\form_filler.py
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\form-fill-rules.json
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_form_selftest.py
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\form-rounds.json (только строка `obligation_refs <- manifest_row@all -> window_record.row_field_gaps`, как несёт ветка)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_field_producers.py (только изменение ветки: ожидание `obligation_refs` без хэша)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\driver-exits\ (как несёт ветка; перепись-строки сверх ветки — L1c)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\stories\dry-1\ (новый на main)
C:\QAFactory\forge-repo\ai-packages\qa-factory\changelog.d\p1b-n2-dry-stub.md (новый на main)
C:\QAFactory\forge-repo\ai-packages\qa-factory\changelog.d\p1b-n3-driver-door.md (новый на main)
C:\QAFactory\forge-repo\ai-packages\qa-factory\changelog.d\p1b-n4w-exit-walker.md (новый на main)
C:\QAFactory\forge-repo\docs\tasks\specs\reports\ (только файлы `20261114-p1b-n*`, `20261114-p1b-s5stub-report.md` и `p1b9-c*`, приходящие с веткой)
C:\QAFactory\forge-repo\docs\tasks\specs\reports\20261117-p1b-l1-report.md (новый, отчёт узла)
non-goals: любая правка поведения сверх того, что несёт ветка (кроме разрешения конфликта); строки переписи сверх ветки (L1c); строки реестров меток по смыслу (L2); числа `slow_tests.json`/`TEST_TIMEOUTS` по новому замеру (L2 по F-P5 (а)); строки обхода; `canon.yml`/`nightly.yml` (N5); `known_red.py`, `harness.py`; журнал руками; запуск CI, мутаций, медленных файлов
handoff: отчёт билдера `C:\QAFactory\forge-repo\docs\tasks\specs\reports\20261117-p1b-l1-report.md` (правило 7 `.claude/agents/builder.md`): ветка и хэш, вывод `merge-tree`, список конфликтов (если были) и как решён каждый, проход FR по затронутым разделам, дословные выводы прогонов DoD с секундами, полный список строк `--check` (вход L1c)
edges: (1) ветка — `pile/live-run-fvf/batch-3` от `origin/main` (PROJECT.md «Командная работа» п. 1; пачку берёт `piles.py take` после L0), затем `git merge --no-ff wip/p1b-n4m`; (2) КОНФЛИКТ СЛИЯНИЯ с сегодняшним `main` (t-955 мерил чисто против `42f5fcae`; против `7103829a` не перемерено): (2а) конфликт в файле пакета, где стороны меняли РАЗНЫЕ функции/ключи — держатся обе стороны (функции `main` + функции ветки); (2б) одна функция/ключ изменены обеими сторонами по-разному — стоп, вопрос Lead с обоими текстами; инвариант: правка `main` никогда не теряется молча и поведение ветки не переписывается билдером; (2в) `test-layers.json` / `slow_tests.json` / `selftest.py`: сторона `main` целиком + одна строка ветки (`keep` `test_scenario_dry_1.py` с `covers` как `N4M/.../test-layers.json:5112-5121`; 51.0; 900); инвариант: канон не получает `unlisted:` и не теряет ни одной строки `main`; (2г) конфликт в `logs/journal/*.jsonl` или `CURRENT_CONTEXT.md` — НЕ решается: стоп и вопрос Lead (журнал пишет только `tools/journal_write.py`; ветка журнала не несёт по t-955, поэтому такой конфликт — признак чужой правки); (3) ВРЕМЕННОЙ: до L1 `--witness-for` не знает `test_scenario_dry_1.py`; после L1 — знает; DoD гоняет `--witness-for` на итоговом дереве; (4) ВРЕМЕННОЙ, перепись (B1) — ДВА МИРА: (4а) на коммите L1 (до L1c) `dry_exits.py --check` печатает `dry_exits --check: <N> discrepancies` с N > 0 (оценка N = 227 по t-955 на `42f5fcae`; на `7103829a` стыков столько же — 267, остальное не перемерено); билдер НЕ чинит, а копирует все строки в отчёт; каждая строка обязана иметь вид `<route|joint|kind without a key> <id>: the driver has it and no row names it; …` или `… stale row in …`; строка ЛЮБОГО другого вида (ratchet, class unknown, ledger, unreadable) — стоп, вопрос Lead; (4б) после L1c — `0 discrepancies` (DoD L1c); инвариант: коммит L1 никогда не уходит в `main` один — волна 1 сливает L1+L1c+L-ax+L2 вместе (§5); (5) ВРЕМЕННОЙ: после L1 задача `full` гоняет режим по умолчанию `test_scenario_dry_1.py`; метка `main/S5 -> P1B-9` устарела по смыслу — её чинит L2 в той же волне; (6) коммит-хук печатает WARN «`dry_driver.py` matches no feature» (`plans/features.json`; отчёт N3 `:54`) — это WARN, не отказ; правка `plans/features.json` — не этот узел (строка отчёта); (7) `lint_ratchet.py` начнёт сканировать `test_scenario_dry_1.py` (`tools/lint_ratchet.py:11`): рост — строка отчёта, судит канон (`forge-check`); `form-rounds.json` читается им только в части семейств (`tools/lint_ratchet.py:69`), строка `known_red` его не меняет; (8) пустой результат `--witness-for` для пути (`no scenario or keep row covers`) — строка отчёта, не повод писать тест (builder-rules 7b); (9) медленный файл в списке `--witness-for` (`test_scenario_dry_1.py`) — строка «судит канон пачки», не запуск
DoD: (а) `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/tests/dry_world.py ai-packages/qa-factory/scripts/tests/dry_exits.py ai-packages/qa-factory/scripts/tests/dry_stub.py ai-packages/qa-factory/scripts/tests/form_filler.py ai-packages/qa-factory/scripts/tests/fixtures/form-rounds.json ai-packages/qa-factory/scripts/tests/test_field_producers.py ai-packages/qa-factory/scripts/driver_machine.py` — называет `test_scenario_dry_1.py` для трёх `dry_*.py` и `driver_machine.py` (t-955: выполнимо) — строка «судит канон пачки»; (б) быстрые свидетели, каждый отдельно, дословно, с секундами: `python -B ai-packages/qa-factory/scripts/tests/dry_exits.py --selftest` (154/154 на слитом дереве t-955), `python -B ai-packages/qa-factory/scripts/tests/dry_exits.py --check` (мир (4а): `<N> discrepancies`, все строки разрешённого вида — копия в отчёт), `python -B ai-packages/qa-factory/scripts/tests/dry_stub.py --selftest` (189/189), `python -B ai-packages/qa-factory/scripts/tests/test_form_selftest.py` (26/26), `python -B ai-packages/qa-factory/scripts/tests/test_field_producers.py` (885/885), `python -B ai-packages/qa-factory/scripts/tests/test_form_at_stop.py`, `python -B ai-packages/qa-factory/scripts/tests/test_form_view.py`, `( cd ai-packages/qa-factory && python -B scripts/selftest.py --limits --lang )` в subshell worktree — каждый зелёный (кроме `--check`, см. мир 4а); (в) грамматика частей, секунды: `python -B ai-packages/qa-factory/scripts/tests/test_scenario_dry_1.py --part exits:` → rc 2; `--part exits:nosuch` → rc 2 с перечнем групп (обе — разбор аргументов, без мира); (г) отчёт называет строкой: «`test_scenario_dry_1.py` (по умолчанию, `--part main`, `--part exits:*`) — судит канон пачки (CI-1)»; (д) коммит слияния несёт строки `architecture:`/`judgment:` по `tools/architecture_gate.py` (AR-28, AR-20, AR-22, AR-17, AR-29 — как держится — одной строкой)
order: после L0; первый узел ветки посадки; за ним L1c (свежий билдер, та же ветка)
siblings: ось 18 (храповики `driver-exits` приходят на main вместе с базами), ось 34 (одна дорога: дверь `driver` — тот же процесс `story_run`), ось 17 (форма вывода ходока), ось 38 (новая, L-ax); остальные оси — как П1-б §7(b)
designer: C:\QAFactory\forge-repo\docs\tasks\specs\20261117-p1b-finish-spec.md (до приёмки — черновик)

Что ветка НЕ несёт из `wip/p1b-n4w` / `wip/p1b-n4-gates`: ничего — `wip/p1b-n4w` — подмножество (ходок без фикса), дерево
`p1b-n4-gates` — уровень N3 без строк обхода. Lead убирает ветки и деревья `wip/p1b-n4w`, `wip/p1b-n4-gates`, `wip/p1b-n3`,
`wip/p1b-n4g-*`, `wip/p1b-s5stub`, `wip/p1b-n4wfix` после волны 1 (PROJECT.md п. 12) — если `git status` дерева
`p1b-n4-gates` пуст (§11).

### L1c — перепись выходов догоняет `main` (B1; после L1, до L-ax и L2, та же ветка, та же волна)

Направление — развилка F-P14 (решает Lead ДО диспатча). Карточка ниже написана по рекомендации (а); при (б) — §7 F-P14 (б)
называет другую owns и край.

given: отчёт L1 (полный список строк `--check`); эта спека §1, §4 L1c, F-P14, F-P15; `T/dry_exits.py` `load` (`:204-237`), `scan_joints` (`:502-512`), `check` (`:628-657`), `_code_rows` (`:660-673`), `_raised`/`_ratchets` (`:699-741`) — строки по `N4M`; `T/fixtures/driver-exits/gates.json` (образец строки `:67-100`); `PKG/references/stage-joints.json` (поле `stages` строки); `C:\QAFactory\forge-repo\plans\builder-rules.md`; `C:\QAFactory\forge-repo\ai-packages\qa-factory\design\factory-rules.md`
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\driver-exits\gates.json
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\driver-exits\hooks.json
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\driver-exits\s0.json
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\driver-exits\s1-s4.json
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\driver-exits\s5.json
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\driver-exits\s6-s9.json
C:\QAFactory\forge-repo\ai-packages\qa-factory\changelog.d\p1b-l1c-census-catch-up.md (новый)
C:\QAFactory\forge-repo\docs\tasks\specs\reports\20261117-p1b-l1c-report.md (новый)
Что сделать: (1) для КАЖДОЙ строки `joint <id>: the driver has it and no row names it` из вывода `--check` — строка в секции
`joints` файла группы: `{"reach": "unwalked", "why_unreached": "not walked yet: joint added on main after N1 (census catch-up L1c); the group's walk node writes its rows"}`;
(2) группа стыка — по полю `stages` его строки `stage-joints.json`, прочитанному через `null_outcomes.load_data(stage_joints.DATA)`
(тот же загрузчик, что `scan_joints`): все стадии внутри одной группы (`S0` → `s0`; `S1`–`S4` → `s1-s4`; `S5` → `s5`;
`S6`–`S9` → `s6-s9`) → эта группа; стадии из двух и более групп → `gates`; правило проверяется на 40 уже стоящих стыках
(`exit_gate:grounding` `S2` → `s1-s4`, `exit_gate:case_identity` `S4` → `s1-s4`, `exit_gate:scoped`/`digest` S1–S9 → `gates`,
`acceptance:*` `S5` → `s5`) — расхождение хоть на одном стоящем стыке — стоп, вопрос Lead; (3) в `ratchet.raised_by` той же
группы — по одной строке на добавленную строку, формой `unwalked | joints/<id> | L1c census catch-up, 2026-11-17` (формат
`_raise_entry`, `dry_exits.py:734-735`); `ratchet.unwalked` (база) НЕ меняется; (4) строки пишутся механически скриптом из
вывода `--check` (скрипт — в scratchpad, в отчёт целиком, не коммитится); (5) таблица отчёта «семейство стыков → группа →
число строк» (по t-955: validate_artifacts 42, role_cli 33, guard_pre_tool 24, execution_request 24, handoff_check 21,
manifest_put 14, planning_contract 12, s5_precheck 11, first_look 11, stage_guard 8, host_adapter 8, run_suite 7,
controller 6, exit_gate 4, coverage_contract 2).
non-goals: `dry_exits.py` и любой код (при F-P14 (а)); строки обхода (`stories/dry-1/exits/*`); реестры меток; классы (`classes.json`: стыки берут класс по источнику `stage-joints`, `dry_exits.py:561-574`); перенос уже стоящих 40 стыков между группами; суждение, проходим ли стык ходоком (F-P15)
handoff: отчёт билдера `C:\QAFactory\forge-repo\docs\tasks\specs\reports\20261117-p1b-l1c-report.md`: таблица семейств, скрипт целиком, дословные выводы DoD с секундами, NOTE храповика
edges: (1) ПУСТОЙ ДИФФ ПЕРЕПИСИ: L1 (б) уже дал `0 discrepancies` (например, `main` убрал стыки или их строки уже есть) → L1c не пишет ни строки и не коммитит; отчёт — строка «census diff empty: 0 discrepancies at <hash>»; узел закрыт отчётом; инвариант: L1c никогда не пишет строку субъекта, которого `--check` не назвал; (2) строка вида `route …` или `kind without a key …` (маршруты/виды, сдвинутые сегодняшними слияниями; t-955 их не видел) — стоп, вопрос Lead с этими строками: группа маршрута и `raised_at` вида — не механическое правило (`kind` требует `raised_at` = места драйвера, `_code_rows` `:669-673`); инвариант: ни одна строка не пишется по догадке; (3) строка `… stale row in <file>; the driver no longer has it` → строка удаляется из файла, и если у неё была запись `raised_by` — удаляется и запись; если строка входила в базу — база понижается на 1 (иначе `stale base`); (4) стык без `stages` или со стадией вне `S0`–`S9` — стоп, вопрос; (5) ДРЕЙФ ДО ВОЛНЫ: параллельные потоки (rules-debt S7/S8: `exit_gate.py`, `gate-registry.json`) могут добавить стык между L1c и волной — проверка перед волной (§5 шаг 9) снова гоняет `--check` на дереве ветки, слитой с текущим `origin/main`; ненулевой → фикс-раунд L1c (свежий билдер, только дельта) до волны; инвариант: в `main` не уходит дерево с `--check` ≠ 0; (6) медленный файл: `--witness-for` по `driver-exits` называет `test_scenario_dry_1.py` — «судит канон пачки», не запуск; (7) счёт `unwalked` групп s0 и s1-s4, уже обойдённых, вырастет: их части печатают NOTE `unwalked: <n>` > 0 — это не FAIL (строка «unwalked» части — NOTE, `judge_group`), следующий шаг — по F-P15
DoD: `python -B ai-packages/qa-factory/scripts/tests/dry_exits.py --check` → `dry_exits --check: 0 discrepancies` и NOTE `ratchet unwalked: raised <N> row(s) above the base <B>, named in raised_by: …` с N = числу строк «no row names it» из отчёта L1; `python -B ai-packages/qa-factory/scripts/tests/dry_exits.py --selftest` — все случаи (154/154); `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/tests/fixtures/driver-exits` — называет `test_scenario_dry_1.py` («судит канон пачки», CI-1); коммит — строки `architecture:` (AR-20, AR-28, AR-13) и `judgment:` по `tools/architecture_gate.py`
order: после L1 (та же ветка), до L-ax, CI-1 и L2; группы N4 — только после волны 1 (тот же `driver-exits/<g>.json`)
siblings: ось 18 (храповик: подъём `unwalked` назван `raised_by`), ось 38 (новая — L-ax), ось 34 (одна дорога: стыки — один загрузчик)

### L-ax — новая ось карты симметрий (F11; узел Lead, та же ветка, после L1c)

Исполнитель: Lead (`docs/SIBLING_MAP.md` — путь механизмов, `tools/mechanism_gate.py:215-218`; коммит несёт блок по всем
осям и `tier:` уровня Lead — билдер его сделать не может).
owns:
C:\QAFactory\forge-repo\docs\SIBLING_MAP.md (новый раздел `## Axis 38 — …` после `## Axis 37`, `:627`)
Текст оси (черновик, Lead правит): `## Axis 38 — the dry census: a joint of references/stage-joints.json, a route of
driver_dispatch.KNOWN_REFUSALS / match_known, a price key of question-prices.json or a keyless kind of the driver <-> its row
in scripts/tests/fixtures/driver-exits/<group>.json (P1-b L1c, critic t-955 F11, 17.11)`; тело: правило «новый стык, маршрут,
ключ цены или вид драйвера в коммите пакета ↔ строка переписи в том же коммите (`reach` + `why_unreached`, рост — `raised_by`)»;
детектор — строка `dry-1/census` задачи `full` и шаг `dry_exits.py --check` задачи `dry-story` (N5); улика — 228 расхождений,
молча накопленных 14.11–17.11; группа стыка — по `stages` (L1c п. 2).
edges: (1) ВРЕМЕННОЙ: пути оси (`dry_exits.py`, `driver-exits/`) существуют на ветке посадки и на `main` после волны 1;
коммит оси — на ветке посадки, не на `main` раньше волны (иначе проверка живости путей карты, калибровочная проверка 12,
видит мёртвый путь); (2) следующие механизм-коммиты всех сессий перечисляют 38 осей — цена соблюдения (правило 10 (a)),
назвать в тексте оси.
DoD: `python -B tools/mechanism_gate.py --msg-file <сообщение>` на коммите — проходит; `python -m pytest tools/test_mechanism_gate.py -q` — зелёный.
order: после L1c, до CI-1.

### CI-1 и CI-2 — канон на ветке посадки (координатор)

Детерминированный запуск (CLAUDE.md правило 8: носитель — журнал и вывод `ci_read`). CI-1 — после L-ax:
`python -B tools/ci_read.py start --ref pile/live-run-fvf/batch-3`, затем `python -B tools/ci_read.py why`; дословный вывод
строк `dry-1/*` задачи `full` (`dry-1/census`, `dry-1/main/known_red`, `dry-1/main/stop`, `dry-1/main/time`) идёт в given L2.
Ожидание CI-1: `dry-1/census` PASS (после L1c); `dry-1/main/known_red` — FAIL/NOTE по меткам ветки (их чинит L2). CI-2 —
после L2, тем же способом; его вывод — DoD L2 и механический слой CR-L. Край: вывод нечитаем или задача `full` не дошла до
файла (таймаут шарда) — стоп, вопрос владельцу «лог CI не читается» (PROJECT.md «изменение пакета» п. 2); место остановки по
коду не угадывается (FR-59).

### L2 — метки реестров, истинные на момент слияния (после CI-1, та же ветка, та же волна)

Шаги: (1) Lead в L0 уже завёл находки и id; (2) CI-1 дал строки `dry-1/main/*`; (3) билдер L2 (свежий: дифф + вывод CI-1)
пишет метки и числа расписания (F-P5 (а), решение Lead).

given: вывод CI-1 дословно (строки `dry-1/*` задачи `full`, включая `dry-1/main/time`); id меток из L0; `C:\QAFactory\forge-repo\.claude\worktrees\p1b-n4m\ai-packages\qa-factory\scripts\tests\fixtures\driver-exits\known_red.json`; `…\fixtures\form-rounds.json:70`; решения Lead по F-P4, F-P19; эта спека §4 L2
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\driver-exits\known_red.json
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\stories\dry-1\selftest\known_red.json (только при F-P4 (а) с общим id)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\form-rounds.json (только поля `node`/`raised_by` строки `obligation_refs <- manifest_row@all -> window_record.row_field_gaps`)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\stories\dry-1\exits\s1-s4.json (только при F-P4 (б): удаление строки `s1.review/unavailable`)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\slow_tests.json (только число строки `test_scenario_dry_1.py`, F-P5 (а))
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\selftest.py (только `TEST_TIMEOUTS["test_scenario_dry_1.py"]`, не выше 900, F-P5 (а))
C:\QAFactory\forge-repo\docs\tasks\specs\reports\20261117-p1b-l2-report.md (новый)
non-goals: починка причины остановки (N2h, узлы находок); заведение находок (L0, Lead); перепись (L1c); статус FG7-38 в `forge/7` (двигает Lead при приёмке)
handoff: отчёт `C:\QAFactory\forge-repo\docs\tasks\specs\reports\20261117-p1b-l2-report.md`: таблица «строка реестра → было → стало → строка CI, на которой основано → класс (`stub gap`/`product gap`)»
edges: (1) CI говорит `stopped at S<n>` с `n` ≠ 5 → строка `main/S5` удаляется, пишется `main/S<n>` с id, который Lead даёт под ЭТУ причину (не переносится чужой id; инвариант: недостижимое не прячется под чужой меткой, П1-б E15); причина, для которой у Lead id нет, — стоп, вопрос; (2) ПРИЧИНА НА СТОРОНЕ ЗАГЛУШКИ (F2): остановка вызвана отставанием заглушки от новых обязанностей ролей на `main` (заглушка не пишет поле/файл, который роль теперь пишет; признак — отказ называет выход роли, а не поведение продукта) → метка `main/S<n>` с id узла заглушки (FV3-5 для S5 «нет записи пробы»; иной причине Lead выдаёт id узла заглушки) и `raised_by: "stub gap: <строка CI>"`; находкой продукта такая остановка НЕ помечается; инвариант: метка никогда не выдаёт дефект теста за дефект продукта и наоборот; класс неясен — `product gap` не ставится, стоп, вопрос Lead; (3) CI зелёный до S9 → строка `main/S5` удаляется, пин −1 (иначе `known_red` краснеет «stale», `known_red.py` `reconcile`); (4) пин `pins.known_red` = число строк после правки (равенство, `known_red.json:2`); (5) строка `s1.review/unavailable` — ПО РЕШЕНИЮ Lead F-P4 (развилка открыта, B3): (а) → `node` = FV3-17, `raised_by: "stub gap: walker has no condition for a conditionally offered answer (n4g-s1s4 :55)"`; (б) → строка обхода `s1.review/unavailable` удаляется из `stories/dry-1/exits/s1-s4.json` и строка реестра удаляется, пин −1; до решения Lead L2 НЕ диспатчится; (6) строка `kind:halt/free words` переименовывает только `node` (→ FV3-16) и `raised_by` (`product gap: … cause not located, FV3-16`); id строки не меняется (id = строка обхода); (7) строка `P1B-2f` реестра `form-rounds.json` — по F-P19: (а) → `node` = FV3-18, `raised_by` дополняется «finding FV3-18, Lead 2026-11-17»; id и пин файла не меняются; (б) → удаляется вместе с пином −1 ТОЛЬКО если свидетель `test_field_producers.py` на итоговом дереве зелёный без неё (иначе стоп); (8) вывод CI нечитаем / задача `full` не дошла до файла — стоп, вопрос координатору; угадывать место остановки по коду запрещено (FR-59); (9) реестр самопроверки ходока (`selftest/known_red.json:4`, `N4W-1`) остаётся: `N4W-1` — id самопроверки, не находка продукта; меняется только при F-P4 (а) с общим id; (10) числа расписания (F-P5 (а)): `slow_tests.json` — секунды режима по умолчанию из CI-1 (`dry-1/main/time` + перепись), округление вверх до 0.1; `TEST_TIMEOUTS` = 900 не меняется, если измерено ≤ 800 с; измерено > 800 с — стоп, вопрос Lead (потолок 900 не растёт без слова Lead, F-P18); (11) медленный файл `test_scenario_dry_1.py` — локально не гоняется («судит канон пачки», CI-2)
DoD: координатор повторяет канон на итоговой ветке (CI-2); `python -B tools/ci_read.py why` по задаче `full` не называет `test_scenario_dry_1.py`; в выводе файла: `PASS dry-1/census`, `NOTE dry-1/main/known_red: known red: main/S<n> -> <id>` (или зелёный проход до S9) и ни одной `FAIL dry-1/…`; локально билдер L2 гоняет `python -B ai-packages/qa-factory/scripts/tests/dry_exits.py --check` (`0 discrepancies`, проверка сирот реестра) и `python -B ai-packages/qa-factory/scripts/tests/test_field_producers.py` (зелёный, 885/885 или больше)
order: после CI-1; до CI-2 и CR-L; та же ветка и волна 1
siblings: ось 18 (реестр меток — храповик помощника П1-а; `form-rounds.json` — второй реестр того же помощника)

### CR-L — критик кода темы «посадка П1-б» (B2; после CI-2, ДО волны 1)

По рекомендации F-P12 (а) — развилка открыта заново (B3, §7); до решения Lead план исполним по рекомендации. Один проход на
тему (R13-g; CLAUDE.md правило 3: дифф > 100 строк — обязательный гейт); критик групп N4 — отдельная тема после волны 4.

Диспатч критику (tier critic):
given (механический слой — ДОСЛОВНО, приложен ДО вердикта, CLAUDE.md правило 3 «две ступени»): (1) `git -C C:\QAFactory\forge-repo merge-tree --write-tree --name-only origin/main pile/live-run-fvf/batch-3` (rc и список); (2) `git -C C:\QAFactory\forge-repo diff --stat origin/main...pile/live-run-fvf/batch-3`; (3) выводы DoD L1, L1c, L2 из их отчётов (каждый быстрый свидетель с секундами); (4) вывод CI-2 `python -B tools/ci_read.py why` и строки `dry-1/*` задачи `full`; (5) `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <все owns L1+L1c+L2>`. Плюс: эта спека; отчёты L1, L1c, L2; `docs/tasks/critic-diff-brief.md` (пункты 6-7: дубли, качество); `ai-packages/qa-factory/design/architecture.md` (строки AR §1); `docs/SIBLING_MAP.md` (оси 18, 34, 5, 17, 30, 38); журнал `accepted` t-695, t-721, t-735, t-751, t-789, t-828 (отложенные отказы от критика, которые этот проход закрывает)
handoff: C:\QAFactory\forge-repo\docs\tasks\specs\reviews\20261117-p1b-landing-code-critic.md
non-goals: строки обхода групп (тема групп); перепрогон медленных файлов; исследование механики чтением, когда слой приложен
DoD (ключи вердикта, `tools/critic_verdict.schema.json`): K-C1 слияние не внесло поведения сверх ветки, кроме названных разрешений конфликтов; K-C2 строки L1c = ровно множество «no row names it» отчёта L1, правило группы по `stages`, по записи `raised_by` на строку; K-C3 каждая метка L2 имеет узел пачки с файлом находки и верный класс `stub gap`/`product gap`; K-C4 дубли и качество кода (`dry_exits.py`, `dry_stub.py`, `dry_world.py`, `form_filler.py`, `test_scenario_dry_1.py`, `dry_driver.py`) по critic-diff-brief 6-7; K-C5 строки AR §1 держатся; K-C6 проход FR в отчётах билдеров; K-C7 полнота класса по карте, включая ось 38; K-C8 суждение роли код нигде не судит (вопросы 10-11 критика)
edges: (1) `fit_with_fixes` / `unfit` → фикс-раунд свежим билдером (только дифф + вердикт, CLAUDE.md правило 12), повторный проход критика — только по диффу фикса и вердикту; минорные замечания чинятся тем же фикс-раундом, не откладываются (PROJECT.md «Командная работа» п. 9); (2) замечание к другой кучке — анализ и перенос строкой с исполнителем; (3) бюджет: дифф ~4800+ строк (из них сотни строк JSON фикстур) — критик читает фикстуры выборкой по механическому слою; WARN 250K `tools/agent_budget.py` → остаток свежему критику целиком
order: после CI-2; до проверки перед волной и волны 1

### N4R — реестр меток по файлу на группу (после волны 1; параллельно с N5 и N2h-а; до групп и до N2h-б)

given: эта спека §4 N4R, F-P1, F-P17; `T/known_red.py` (целиком, 152 стр.); `T/dry_exits.py` `load` (`:204-237`, `directory.glob("*.json")` — НЕрекурсивно, прочитано), `check` (`:654-655`), `_ledger`, `_ledger_orphans` (`:757-778`), `judge` (`:817-826`), ветка `--judge` (`:2588-2600`), `NOT_GROUP` (`:39`) — строки по `N4M`; `T/test_scenario_dry_1.py:51,130,138`; `T/dry_world.py:715` (`KNOWN_RED_FILE`), `:976`, `:1335`
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\dry_exits.py (функции `check`, `_ledger_orphans`; удаление `judge` и ветки `--judge` по F-P17 (а); константа пути реестров групп; строки `_selftest_cases`)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_scenario_dry_1.py (функция `main`: путь `--ledger` по умолчанию)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\driver-exits\known_red.json (остаются только строки `main/*`)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\driver-exits\known_red\s0.json (новый)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\driver-exits\known_red\s1-s4.json (новый; при F-P4 (б) — не создаётся, если строк нет)
C:\QAFactory\forge-repo\ai-packages\qa-factory\changelog.d\p1b-n4r-group-ledgers.md (новый)
C:\QAFactory\forge-repo\docs\tasks\specs\reports\20261117-p1b-n4r-report.md (новый)
non-goals: `known_red.py` (не меняется: `load(path)` уже берёт путь); `dry_world.py` (главный проход `:976` читает `main/*` из общего файла; `:1335` склеивает общий файл и файл группы — работает без правки, t-955 F7); строки обхода; форма строки реестра; строка `main/*` (её меняет N2h-б)
handoff: отчёт билдера `C:\QAFactory\forge-repo\docs\tasks\specs\reports\20261117-p1b-n4r-report.md`
edges: (1) ВРЕМЕННОЙ: каталог `driver-exits/known_red/` создаёт этот узел; до него каждая группа читает общий файл; после — `exits:<g>` по умолчанию читает `driver-exits/known_red/<g>.json`; (2) файла группы нет → пустой реестр (пин 0): красная строка — FAIL «new red» (безопасная сторона), зелёная — PASS; инвариант: отсутствие файла никогда не делает красное ожидаемым; (3) `dry_exits.load` (`:210`) и `groups_found` (`test_scenario_dry_1.py:51`) читают `driver-exits/*.json` НЕрекурсивно — подкаталог не становится группой (прочитано в фикс-раунде); билдер добавляет строку таблицы «a subdirectory is no group»; (4) `_ledger_orphans`: строка в `known_red/<g>.json`, чей id не строка `exits/<g>.json` ТОЙ ЖЕ группы, — красное (строка чужой группы — сирота); строка `main/*` допустима только в общем файле; инвариант: ни одна метка не висит без строки, которая её может напечатать (N4w I8); (5) явный `--ledger` по-прежнему перекрывает путь по умолчанию (самопроверка ходока); (6) `--judge` (F7, F-P17): по рекомендации (а) функция `judge` и ветка `--judge` удаляются вместе со строкой докстринга `:13`; ПЕРЕД удалением билдер грепает `judge(` и `--judge` по `PKG/scripts/tests/dry_*.py`, `test_scenario_dry_1.py`, `PKG/scripts/selftest.py`, `.github/workflows/` — вызов вне самой CLI и её строк `_selftest_cases` → стоп, вопрос (положительный контроль той же формы: тот же Grep находит `def judge_group`); при F-P17 (б) — ветка читает общий файл плюс `known_red/<g>.json` группы через ту же склейку, что `dry_world.py:1335`; инвариант: у суда «строки против реестра» одна дорога (P31); (7) одинаковый id в двух файлах реестра — красное с обоими путями
DoD: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/tests/dry_exits.py ai-packages/qa-factory/scripts/tests/test_scenario_dry_1.py` (называет `test_scenario_dry_1.py` — «судит канон пачки»); `python -B ai-packages/qa-factory/scripts/tests/dry_exits.py --selftest` — зелёный, с новыми строками таблицы для краёв (2), (3), (4), (7); `python -B ai-packages/qa-factory/scripts/tests/dry_exits.py --check` — `0 discrepancies`; части `exits:s0`, `exits:s1-s4` — CI (дверь `dry_only` N5, если N5 уже в `main`, иначе канон), исход: `known red:` по тем же id, что до узла
order: после волны 1; параллельно с N5, N2h-а; до N2h-б и групп
siblings: ось 18 (храповик меток — пин на файл), ось 34 (одна дорога: все группы — один путь по умолчанию; один суд реестра)

### N5 — задача CI сухой стори и дверь «только сухая стори» (после волны 1; параллельно с N4R, N2h-а; РАНЬШЕ групп — F-P2)

Форма двери — развилка F-P16; карточка по рекомендации (а). Деньги минут CI — F-P20 (F9).

given: эта спека §4 N5, F-P2, F-P3, F-P6, F-P16, F12; `C:\QAFactory\forge-repo\.github\workflows\canon.yml` (целиком); `C:\QAFactory\forge-repo\.github\workflows\nightly.yml:1-110`; `C:\QAFactory\forge-repo\tools\test_workflows.py:20-50,283-309,405-420,470-490`; `C:\QAFactory\forge-repo\tools\ci_read.py:69,229-241` (`--workflow`, `--var`); `C:\QAFactory\forge-repo\docs\RUNBOOK.md` §7
owns:
C:\QAFactory\forge-repo\.github\workflows\dry-story.yml (новый: `on: workflow_call` с входом `ref`; задача-список, матрица частей, шаг таблиц)
C:\QAFactory\forge-repo\.github\workflows\nightly.yml (новая задача `dry-story`: `uses: ./.github/workflows/dry-story.yml`)
C:\QAFactory\forge-repo\.github\workflows\canon.yml (вход `spike` → булев `dry_only`; задача `dry-story-spike` → задача `dry-story`, `uses: ./.github/workflows/dry-story.yml`, `if: ${{ inputs.dry_only }}`; `run-name`)
C:\QAFactory\forge-repo\tools\test_workflows.py (`NAMES` += `dry-story.yml`; строки, которые читают эти три файла)
C:\QAFactory\forge-repo\docs\tasks\specs\reports\20261117-p1b-n5-report.md (новый)
non-goals: код пакета; `test_scenario_dry_1.py`; `tools/ci_read.py` (дверь — `--var dry_only=true`, вход уже поддержан `:231-232`); `forge-check.yml`; кап по замеру, если F12 не решён (тогда край 4)
handoff: отчёт билдера `C:\QAFactory\forge-repo\docs\tasks\specs\reports\20261117-p1b-n5-report.md`
edges: (1) список частей — из файлов `PKG/scripts/tests/fixtures/stories/dry-1/exits/*.json`, найденных задачей-списком (шаг shell, имена — `basename .json`), матрица — `fromJSON` его вывода; группа без своего файла в матрицу не входит (её `unwalked` печатает режим по умолчанию задачи `full`); инвариант: группа с файлом никогда не выпадает молча — задача-список печатает перечень; (2) пустой перечень (`exits/` нет) → задача-список печатает «no walk groups» и матрица пуста; задачи частей не стартуют, задача зелёная только с этой строкой; (3) отдельным шагом одной задачи: `python -B ai-packages/qa-factory/scripts/tests/dry_exits.py --check`, `python -B ai-packages/qa-factory/scripts/tests/dry_exits.py --selftest`, `python -B ai-packages/qa-factory/scripts/tests/dry_stub.py --selftest` и часть самопроверки ходока (`--part exits:selftest --exits-root …/selftest --ledger …/selftest/known_red.json`) — по F-P6 (а); `--check` здесь — детектор оси 38 для двери `dry_only`; (4) кап: `timeout-minutes` на часть = решение Lead по F12/E6; до решения — 30 (как спайк, `canon.yml:68`), строкой комментария «until the Lead's cap»; (5) строки `run:` не подставляют `${{ inputs.* }}`, `${{ github.event.* }}` (`tools/test_workflows.py:300-309`); значение матрицы и `ref` — через `env:`; (6) `clock` канона: `needs` = `{start, checks, full}` и `if: ${{ always() && !inputs.dry_only }}`; задачи `checks`/`full` получают `if: ${{ !inputs.dry_only }}` (как сегодня со `spike`); строки `test_workflows.py:289,294` меняются тем же коммитом; (7) `run-name`: `${{ inputs.dry_only && 'dry-story' || 'canon' }} ${{ inputs.ref }}` — запуск двери никогда не читается в списке как канон; (8) ВРЕМЕННОЙ: на `main` после волны 1 — части `s0`, `s1-s4`; после групп — пять; до волны 1 этот узел не диспатчится; (9) задача по расписанию идёт через `skip-if-unchanged` как соседи (`nightly.yml:57-68`); (10) ВРЕМЯ (F3): дверь `dry_only` — задача-список + части параллельно (кап 30 мин на часть; замер частей 110-385 с) + шаг таблиц (~1 мин) — оценка ≤ 10 мин на запуск, не проверено; в каноне части идут рядом с `package-full` (2 шарда, кап 180 мин), главный проход ~385 с до S5 — внутри шарда `package-full`; час канона (D-0059) задача не удлиняет, если её самая долгая часть короче шарда — отчёт N5 печатает измеренные минуты первого запуска; (11) вход `spike` удаляется: вызов `ci_read.py start --var spike=true` после N5 даёт 422 «refused the inputs» (`ci_read.py:241`) — это и есть отказ с дверью (`--var dry_only=true`); строка RUNBOOK §7 о двери — строка отчёта для Lead
DoD: `python -m pytest tools/test_workflows.py -q` — зелёный, с новыми строками: «canon has no spike input and no dry-story-spike job», «canon's dry_only door calls dry-story.yml and skips checks/full/clock», «nightly calls dry-story.yml», «dry-story matrix comes from the list job», «no run string splices inputs»; координатор запускает `python -B tools/ci_read.py start --ref <ветка N5> --var dry_only=true` и читает `python -B tools/ci_read.py jobs <run>` — задачи частей `dry-story (s0)`, `dry-story (s1-s4)` и шаг таблиц присутствуют, минуты в отчёте
order: после волны 1; параллельно с N4R, N2h-а; до групп и N6
siblings: ось 34 (одна дорога: канон, ночь и дверь гоняют один файл задачи), ось 38 (детектор `--check`); `tools/test_workflows.py` — читатель (§6)

### N2h — заглушка критика S5 запускает пробу (N2h-а после волны 1, параллельно с N4R, N5; N2h-б после N4R в `main`; до N4:s5, N4:s6-s9 — F-P7)

**N2h-а (код заглушки).**
given: отчёт s5stub `N4M/docs/tasks/specs/reports/20261114-p1b-s5stub-report.md` (целиком); `T/dry_stub.py` ветки ролей (`ROLE_STEPS`, ветка автоматора, ветка критика кода); `PKG/scripts/probe_by_code.py:1-40`; `PKG/scripts/brief_pack.py:239`; `PKG/references/handoffs/s5-critic-to-automator.yaml`; `PKG/scripts/profile_contract.py` (`profile_commands`); П1-б §4.2, N2 DoD (6)
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\dry_stub.py (ветка критика кода S5, константа `PROBE_TIMEOUT_S`, строки `--selftest`)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\stories\dry-1\story.json (только строки заглушки `qa-code-critic@S5`, если нужен вердикт пробы)
C:\QAFactory\forge-repo\ai-packages\qa-factory\changelog.d\p1b-n2h-critic-probe.md (новый)
C:\QAFactory\forge-repo\docs\tasks\specs\reports\20261117-p1b-n2h-report.md (новый)
non-goals: контракт `s5-critic-to-automator.yaml` и пустой исход `probes.records` (продукт; находка FV3-19); `form_filler.py`; `probe_by_code.py`; `driver-exits/known_red.json` (F4: метку меняет N2h-б, не N2h-а); числа расписания
handoff: отчёт билдера `C:\QAFactory\forge-repo\docs\tasks\specs\reports\20261117-p1b-n2h-report.md`
edges: (1) заглушка запускает `probe_by_code.py` ПРОЦЕССОМ в мире, той же командой, что роль получает (`brief_pack.py:239`), с `STORY_RUN_CLASS=dry`; инвариант: вердикт пробы пишет настоящий инструмент, заглушка его не сочиняет (AR-29); (2) экземпляров окна нет → проба не запускается, форма идёт без записи — та же остановка, что сегодня; не PASS; (3) проба вернула ≠0 → строка журнала заглушки с `stderr` (обрезка 400) и форма без записи; не маскируется; (4) тест в мире падает/проходит — оба исхода законны: вердикт пробы — данные записи; (5) команда пробы берёт тест-команду из профиля мира (`profile_contract.profile_commands`), не из брифа; профиль без команды → журнал «no command», проба не запускается; (6) ПОЗИЦИОННЫЙ: запуск пробы стоит в ветке критика ДО заполнения формы (`fill_handover`): инвариант — заполнитель `world_list` видит записи, которые есть, и никогда не видит придуманных; (7) проба дольше `PROBE_TIMEOUT_S` (120 с, §8) → процесс убит, та же ветка, что rc≠0 (журнал «probe timeout», формы без записи); инвариант: таймаут никогда не даёт записи; (8) КОНФЛИКТУЮЩАЯ ПАРА (F5): потолок `TEST_TIMEOUTS` 900 (F-P5) против прохода, который после N2h идёт дальше S5 и запускает мутационную пробу на каждый экземпляр: N2h-а не меняет числа; CI ветки (координатор) печатает `dry-1/main/time`; время режима по умолчанию > 800 с или убийство по 900 — узел не сливается, стоп, вопрос Lead по F-P18; инвариант: в `main` не попадает проход, который упирается в потолок (таймаут читается как красное, не как известное красное); (9) ВРЕМЕННОЙ: после узла главный проход может пройти S5 — метка `main/S5` станет «stale»; N2h-а её НЕ трогает (файл не в owns, F4) — отчёт пишет строку «метку меняет N2h-б по CI»
DoD: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/tests/dry_stub.py` (медленный `test_scenario_dry_1.py` — «судит канон пачки»); `python -B ai-packages/qa-factory/scripts/tests/dry_stub.py --selftest` — зелёный с новыми строками: «critic S5 runs probe_by_code per instance; the record exists before the form», «no instance -> no probe, no record», «probe rc!=0 -> journal line, no record», «probe timeout -> journal line, no record», «profile without commands -> 'no command'»; главный проход — CI (координатор, на ветке N2h): строки `dry-1/main/stop` и `dry-1/main/time` — дословно в отчёт
siblings: ось 30 (команды профиля), ось 5 (двойник: автоматор уже зовёт `manifest_from_tests.py` процессом), ось 34

**N2h-б (метка главного прохода; F4).** Последовательный шаг на ветке N2h после того, как N4R слит в `main`
(`git merge origin/main` в ветку N2h), по выводу CI ветки N2h. Свежий билдер (дифф + вывод CI).
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\driver-exits\known_red.json (только строки `main/*` и пин)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\slow_tests.json (только число `test_scenario_dry_1.py`, если CI сдвинул время)
C:\QAFactory\forge-repo\docs\tasks\specs\reports\20261117-p1b-n2h-b-report.md (новый)
edges: те же, что L2 края (1)-(4), (8), (10) — проход ушёл дальше: строка `main/S<n>` с id, выданным Lead под новую причину,
класс `stub gap`/`product gap` (L2 край 2); зелёный до S9 — строка удаляется, пин −1; вывод CI нечитаем — стоп; инвариант:
волна N2h сливает N2h-а и N2h-б вместе, метка `main/*` в `main` никогда не «stale».
DoD: CI на итоговой ветке N2h: `python -B tools/ci_read.py why` по `full` не называет `test_scenario_dry_1.py`; `NOTE dry-1/main/known_red: …` по новой метке; локально `python -B ai-packages/qa-factory/scripts/tests/dry_exits.py --check` — `0 discrepancies`.
order: N2h-а ∥ N4R ∥ N5; N2h-б — после N4R в `main`; волна N2h = а + б.

### N4:gates, N4:s5, N4:s6-s9 — строки обхода (параллельно; после волны 1, N4R, N5; s5 и s6-s9 — после волны N2h по F-P7)

Общая карточка; `<g>` ∈ {`gates`, `s5`, `s6-s9`}; один диспатч на группу, owns не пересекаются.

given: N4w-спека §5.2 (пример), §6 (EW1-EW26), §8 (грамматика строки и рецепта); П1-б §3.3, §3.6, §4.3, §5 (E1-E22), §9.3 (вердикты FV1 своей группы); отчёты `…-n4g-s0-report.md` и `…-n4g-s1s4-report.md` (образец); отчёт L1c (какие стыки группы добавлены); `T/fixtures/driver-exits/<g>.json`; `PKG/references/question-prices.json`, `stage-joints.json`, `conductor-actions.json`, `stages.json`; находки FV1 группы в `plans/piles/live-run-fvf/findings/`; id находок для ожидаемо красных строк, выданные Lead В ДИСПАТЧЕ (F6; gates — FV1-7, FV1-8); решение Lead F-P4, F-P15; `C:\QAFactory\forge-repo\ai-packages\qa-factory\design\factory-rules.md`; `C:\QAFactory\forge-repo\plans\builder-rules.md`
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\stories\dry-1\exits\<g>.json (новый)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\stories\dry-1\seeds\<g>.json (новый)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\driver-exits\<g>.json
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\driver-exits\known_red\<g>.json (новый; по F-P1 (а))
C:\QAFactory\forge-repo\docs\tasks\specs\reports\20261117-p1b-n4-<g>-report.md (новый)
non-goals: починка находок; `dry_world.py`/`dry_exits.py`/`dry_stub.py` (дефект ходока — строка отчёта и вопрос, не правка); `test_conductor_doors.py` (N4c); строки других групп; общий `known_red.json` (только `main/*`)
handoff: отчёт по образцу N4:s0/N4:s1-s4: таблица «id → start → reach → исход», строки, которым нужна метка (id → предложенная находка), `live_only` с причиной, вывод `dry_exits.py --check`, остаток `unwalked` по происхождению (N1 / L1c)
edges: (1) EW11 ВРЕМЕННОЙ: строки со `start` позже места остановки главного прохода печатают `after:<node>` по метке `main/S<n>` и сами исполнятся, когда проход пойдёт дальше; (2) красная строка без метки — FAIL «new red»: метку (`known_red/<g>.json`) группа пишет только с id, выданным Lead под ЭТУ причину — заранее в диспатче (F6) или фикс-раундом; id нет — строка отчёта, узел сдаётся красным; (3) строка, которую мир сухой стори не может поставить, — `reach: live_only` с причиной ИЗМЕРЕННОЙ (рецепт пробован) или с пометкой «estimate, not verified» (образец N4:s0 `:78`); рост `live_only` — каждой строкой `raised_by` (двойной счёт — по решению F-P8, открыто заново); (4) ключ цен без строк — не запись `driver-exits` (П1-б §3.2), `unwalked` его не считает; строки ключа нужны N4c — F-P9; (5) строки гейтов с вопросом владельцу Q1/Q2 — `expect.owner_question: "Q<n>"`, NOTE «owner question Q<n> open» (F-W12 (а)); (6) C4г только на субъекте класса `gate` (`classes.json`); иначе загрузчик отказывает до мира; (7) `gate_B` достижим только после S7 (`PKG/references/stages.json:301-312`) — для группы gates сегодня `after:`; `gate_A` достижим (отчёт N2g `:38`); (8) база `unwalked` группы: строки эпохи N1 (gates: маршруты `driver-exits/gates.json:4-66` (15) и стыки `:67-92` (6), база `:97` = 21) группа обходит, понижая базу в том же файле; стыки, добавленные L1c (их записи `raised_by`), — по F-P15: по рекомендации (б) остаются `unwalked` со своей записью `raised_by`, отчёт печатает их число; обойдённый стык L1c удаляет свою запись `raised_by` (иначе «stale raise», `_raised` `:712-713`); (9) время части — кап на часть (F12), одна строка дольше `ROW_CAP` — красное с id (E6); (10) КЛАСС F-P4 (F6): ответ ключа цен, который продукт предлагает условно, а у ходока нет условия, — по решению Lead F-P4: при (б) строка обхода НЕ пишется, отчёт — строка «conditionally offered: <key>/<answer> → FV3-17»; при (а) — строка с меткой FV3-17; инвариант: метка никогда не скрывает строку, которую мир не может предложить; (11) медленный файл `test_scenario_dry_1.py --part exits:<g>` — «судит канон пачки» / дверь `dry_only`, не локально
DoD: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/tests/fixtures/stories/dry-1 ai-packages/qa-factory/scripts/tests/fixtures/driver-exits` (называет `test_scenario_dry_1.py` — «судит канон пачки»); локально: `python -B ai-packages/qa-factory/scripts/tests/dry_exits.py --check` — `0 discrepancies` (база `unwalked` эпохи N1 понижена до 0; остаток L1c — по F-P15); часть `test_scenario_dry_1.py --part exits:<g>` — CI двери `dry_only` (N5) на ветке группы (запускает и читает координатор: `python -B tools/ci_read.py start --ref <ветка> --var dry_only=true`): `PASS dry-1/exits:<g>/outcomes`, NOTE `unwalked: <n>` (n = остаток L1c по F-P15 (б), иначе 0), FAIL — только строки из списка «нужна метка» отчёта
order: после волны 1, волны N4R, волны N5; s5/s6-s9 — после волны N2h; критик темы групп — один после трёх
siblings: ось 5 (двойники стадий: id одного состояния под двумя субъектами — как `kind:s1_review`/`s1.review`, отчёт N4:s1-s4 `:75`), ось 34, ось 38

Своё у групп (дополнение к общей карточке):
- **gates**: субъекты — маршруты и стыки `gates.json` (с L1c — плюс многостадийные стыки); C6 на каждом вопросе `gate_A` в
  строке; строки FV1-7 (I-gate) и FV1-8 (П1-б §9.3) — `gate_A` × `approve` после `questions` × `go on`: ожидаемо красные,
  метка — id FV1-7/FV1-8, выданные в диспатче (находки есть, `live-run-fvf/1` `:40-41`).
- **s5**: `s5.repair_limit`, `s5.nobody_*`, `exit.resume_limit*`, `s6.walk_*`, `s6.data_change`, `code_close.*` (П1-б `:636`);
  строка C10 `s5.window_finish/ref_without_hash` (FV1-19) — `pending judge C10` (N4w F-W13), не PASS.
- **s6-s9**: `s6.stand_*`, `s7.*`, `s8.*`, `closed.held`; FV1-22 — S7-петля (`after:` до прохода S5).

### N4c — перепись ключей вопросов: строки сухой стори входят в `driven` (после всех N4 — П1-б §6, без изменений)

given: П1-б §6 N4c (`:638-651`); `T/dry_exits.py` `driven_keys` (N4w-спека §2); `T/test_conductor_doors.py:626-679,794-810`; `T/test-layers.json:672` (keep `test_conductor_doors.py`)
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_conductor_doors.py
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test-layers.json (только `covers` строки `test_conductor_doors.py`)
C:\QAFactory\forge-repo\docs\tasks\specs\reports\20261117-p1b-n4c-report.md (новый)
non-goals: смысл и сигнатура `census_problems`; строки обхода
handoff: отчёт билдера `C:\QAFactory\forge-repo\docs\tasks\specs\reports\20261117-p1b-n4c-report.md`
edges: П1-б E17, E20; (1) `driven_keys()` пуст → `PINNED_ELSEWHERE` не меняется, отчёт печатает пустое множество; это NOTE, не PASS «сжатия» (инвариант: перепись не теряет закрепление непройденного ключа); (2) ключ в `driven` И в `PINNED_ELSEWHERE` → существующий отказ «listed as pinned elsewhere, but driven here» (`:679`) — запись удаляется; (3) очередь `test-layers.json` — по решению Lead F-P10 (а): N4c берёт строку `covers` по D-0048 без ожидания; (4) медленный файл `test_conductor_doors.py` (53 с) — «судит канон пачки», не локально
DoD: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/tests/test_conductor_doors.py`; `test_conductor_doors.py` — канон (координатор): зелёный, в выводе K15 `driven` содержит ключи сухой стори; список удалённых из `PINNED_ELSEWHERE` = `dry_exits.driven_keys()` (в отчёте)
order: после волн всех групп N4 и FV3-9
siblings: ось 18 (храповик «pinned elsewhere» сжимается)

### Поздние узлы и чего каждый ждёт

- **N6** (П1-б `:659-661`): вторая строка раннеров `stories/dry-1/runners/ts-playwright/` + Node и браузер в образе задачи
  `dry-story` (теперь — `dry-story.yml`, F-P16 (а)). Ждёт: N5, N4:s5, N2h. Owns: `T/fixtures/stories/dry-1/runners/ts-playwright/`
  (новый), `.github/workflows/dry-story.yml` (только шаги образа), `tools/test_workflows.py` (строки этой задачи).
  Пересечение с N5 — последовательно N5 → N6. Свидетель — часть `exits:s5` через дверь `dry_only`.
- **N3t** (A1 `:161-177`): ОДИН узел на типы сверх `default`. Ждёт: волна 1. Расхождение имён — F-P11 (решение Lead (а)):
  построено `test_scenario_dry_1.py` и `stories/dry-1/` с `DEFAULT_STORY = "dry-1"` при `dry-types.json` `default:
  codemie-14857`; каталог `stories/dry-codemie-14857/` на `main` есть (F10). Owns: `T/fixtures/stories/dry-<type>/` (новые),
  `T/fixtures/stories/dry-types.json`, `T/test_scenario_dry_1.py` (функция `main`, ветка `main:<type>`), строка `covers`
  `keep` `test_scenario_dry_1.py` — `test-layers.json` после N4c или по D-0048.
- **N3a** (A2 `:231-245`): «сказано до работы». Ждёт: волна 1 и П1-в N0. Owns: `T/dry_exits.py` (функция `told_before_work`
  только), `T/test_scenario_dry_1.py` (функция `_print_told` и строка её вызова). Пересечение: FV2-13 пишет `dry_exits.py` —
  по D-0048 функции не пересекаются; N4R раньше N3a.
- **FV3-14** (F-P8 (б), если Lead так решит): `T/dry_exits.py` `_count_reach` — после групп.
- **N-L** (узел Lead): R-L1…R-L9 П1-б `:663-677` + R-L10 A2 `:246`. Ждёт: волна 1. R-L3 (`architecture.md:192`), R-L5 — до N4:gates.

---

## 5. Порядок, параллельность и общие файлы

| Шаг | Узлы | Общие файлы и как разведены | Слияние в `main` |
|---|---|---|---|
| 0 | L0 (Lead) | `plans/piles/live-run-fvf/` — один писатель | коммит Lead на `main` (пачка и находки) |
| 1 | L1 | ветка `pile/live-run-fvf/batch-3`, один писатель | нет |
| 2 | L1c | та же ветка, последовательно; шесть файлов `driver-exits/<g>.json` | нет |
| 3 | L-ax (Lead) | `docs/SIBLING_MAP.md` на той же ветке | нет |
| 4 | CI-1 (координатор) | — | нет |
| 5 | L2 | та же ветка; `known_red.json`, `form-rounds.json`, расписание | нет |
| 6 | CI-2 (координатор) | — | нет |
| 7 | CR-L (critic) | читает только | нет |
| 8 | фикс-раунд CR-L (если нужен) + повторный проход по диффу фикса | та же ветка | нет |
| 9 | проверка перед волной (координатор) | `git merge origin/main` в ветку; `merge-tree` чистый; `python -B ai-packages/qa-factory/scripts/tests/dry_exits.py --check` = `0 discrepancies` (иначе фикс-раунд L1c, L1c край 5); если `main` сдвинул продукт с CI-2 — CI ещё раз | — |
| 10 | **волна 1**: `python -B tools/wave.py merge` | L1+L1c+L-ax+L2(+фикс) одной волной | да |
| 11 | N4R ∥ N5 ∥ N2h-а | `dry_exits.py`+`test_scenario_dry_1.py`+`known_red*` (N4R) / workflows+`tools/test_workflows.py` (N5) / `dry_stub.py`+`story.json` (N2h-а) — не пересекаются | каждая своей волной (N4R, N5) |
| 12 | N2h-б | `known_red.json` строки `main/*` — после волны N4R; ветка N2h сливает `main` | волна N2h = а + б |
| 13 | N4:gates ∥ N4:s5 ∥ N4:s6-s9 (+ FV3-9) | файл на группу в четырёх каталогах; общий `known_red.json` не пишет никто | своими волнами |
| 14 | критик темы групп (один) | — | до волн групп |
| 15 | N4c | `test_conductor_doors.py`, `test-layers.json` | своя волна |
| 16 | N6, N3t, N3a, FV3-14 | N6 после N5; N3t после N4c по `test-layers.json`; N3a после N4R по `dry_exits.py` | свои волны |

Инвариант «`main` не краснеет после слияния этого плана»: волна 1 — только после шага 9 и зелёного CI-2 (ни одной `FAIL
dry-1/…`, `dry-1/census` PASS); каждая следующая волна — только с зелёным `dry_exits --check` на её дереве и зелёным CI
двери `dry_only` / канона на её ветке. Остаточный риск, названный: `main` сдвинул продукт между CI ветки и волной — шаг 9
перемеряет быстрое (перепись) и, при сдвиге продукта, повторяет CI; детектор пропуска — ночной `full`.

Писателей одновременно: шаг 11 — 3, шаг 13 — 3-4 (кап 6, CLAUDE.md правило 12). Критик кода: CR-L (тема посадки) и один
критик темы групп (R13-g).

---

## 6. Читатели каждого затронутого файла (роль дизайнера правило 7)

Команды (Grep tool, режим count):
- `dry_exits|dry_world|dry_stub|dry_driver|test_scenario_dry|known_red|driver-exits|stories/dry` по `tools/` — 0; по
  `.githooks/` — 0; по `.claude/settings.json` — 0 (t-944). Положительные контроли той же формы:
  `test-layers\.json|canon\.yml|slow_tests\.json|scenario_walk|test_conductor_doors|nightly\.yml|TEST_TIMEOUTS` по `tools/` —
  136 вхождений в 20 файлах; `piles\.py|architecture_gate` по `.githooks/` — 2 (`commit-msg`; перемерено в фикс-раунде).
- Фикс-раунд: `form-rounds|test_field_producers|dry-story\.yml` по `tools/` — 16 в 2 файлах (`lint_ratchet.py` 5,
  `test_lint_ratchet.py` 11), по `.githooks/` — 0, по `.claude/agents/` — 0 (контроль той же формы `test-layers\.json` по
  `.claude/agents/` — 1, `designer.md`).
- Фикс-раунд: `SIBLING_MAP` по `tools/` — 44 в 25 файлах; по `.githooks/` — 0; по `.claude/` вне `worktrees/` —
  `agents/designer.md` 1, `agents/critic.md` 1, `skills/boot-diet/SKILL.md` 2, `skills/critic-exam-gen/SKILL.md` 1 (поиск по
  `.claude/` упёрся в лимит времени из-за `worktrees/`; строки вне `worktrees/` выписаны из частичного вывода — полнота
  по `.claude/skills/` **не установлена**).
- Фикс-раунд: `live-run-fvf|plans/piles` по `tools/*.py` — 378 в 27 файлах (`piles.py` 27, `test_pile_cards_contents.py` 5,
  `test_piles_*` …).

| Файл | Читатель (tools/.githooks/.claude) | Вердикт |
|---|---|---|
| `.github/workflows/canon.yml` | `tools/test_workflows.py:29,288-297,410-416,476-490` (пин `run-name` со `spike` `:289`, `clock.if`/`needs` `:294`, F19E `:300-309`) | меняется в N5 |
| то же | `tools/ci_read.py:69` (`WORKFLOW = "canon.yml"`, `start`, `--var` `:231-232`) | неизменен (дверь — `--var dry_only=true`) |
| `.github/workflows/nightly.yml` | `tools/test_workflows.py` (`NAMES :29`) | меняется в N5 (и N6 через `dry-story.yml`) |
| `.github/workflows/dry-story.yml` (новый) | `tools/test_workflows.py` `NAMES :29` и детектор папки `find_workflows :41-44` (все `NAMES` обязаны быть в папке) | меняется в N5 (тем же коммитом) |
| `T/test-layers.json` | `tools/test_quarantine.py`, `tools/lint_ratchet.py:11,70`, `tools/owns_readers.json:6`, `tools/owns_readers.py`, `tools/source-split-carriers.json`, `tools/test_redundancy.py`, `tools/story_capture.py` | неизменны |
| `PKG/scripts/slow_tests.json` | `tools/owns_readers.json:7` | неизменен |
| `T/scenario_walk.py` | `tools/story_capture.py`, `tools/install_parity_anchors.json` | неизменны (L1 добавляет дверь `driver`, имена функций не меняются) |
| `T/test_conductor_doors.py` | в `tools/` вхождения общего набора — не разобраны по файлу | N4c: неизменны (имя файла не меняется) |
| `T/fixtures/form-rounds.json` | `tools/lint_ratchet.py:10,39,69` (`FORM_ROUNDS_REL` — семейства → регулярные выражения), `tools/test_lint_ratchet.py` | неизменны (L1/L2 меняют только строку `known_red`, не семейства) |
| `T/test_field_producers.py` | `tools/lint_ratchet.py:12,72` (`HAND_SELF_FILE` — никогда не сканируется) | неизменен |
| `T/dry_*.py`, `T/test_scenario_dry_1.py`, `T/fixtures/driver-exits/**`, `T/fixtures/stories/dry-1/**` | нет (0, с контролем) | — |
| `tools/test_workflows.py` | сам тест; `.githooks/` — 0 | меняется в N5 |
| `docs/SIBLING_MAP.md` | `tools/mechanism_gate.py:206,409,438` (оси по заголовкам `## Axis N — …`; число осей читается из карты — после L-ax каждый механизм-коммит перечисляет 38), `tools/test_mechanism_gate.py`, `tools/install_parity_anchors.json:411,425,525-526` (пара путей kit/host; «liveness» путей карты — калибровочная проверка 12), `tools/claim_control_gate.py`, `tools/handoff_gate.py`, `tools/dispatch_gate.py`, `tools/session_context.py`, ещё 18 файлов `tools/` (упоминания); `.claude/agents/designer.md`, `critic.md`; `.claude/skills/boot-diet`, `critic-exam-gen` | неизменны (новая ось в той же грамматике заголовка); цена — блок осей +1 строка у всех механизм-коммитов |
| `plans/piles/live-run-fvf/batch-3-…`, `README.md`, `findings/*` | `tools/piles.py` (`check`, `take`, `status`, `close`), `.githooks/commit-msg` (через `piles.py`), `tools/test_pile_cards_contents.py`, `tools/forge_metrics.py`, `tools/collect_intake.py`, `tools/compact_snapshot.py` | неизменны (L0 пишет по их правилам) |

Читатели внутри пакета (для краёв, не по правилу 7): `driver-exits/known_red.json` — `T/dry_exits.py:654-655,2600`,
`T/dry_world.py:715,976,1335`, `T/test_scenario_dry_1.py:130,138`; `known_red.py` — `T/dry_exits.py:760,772`,
`T/test_field_producers.py:32,189` (реестр П1-а `form-rounds.json`).

---

## 7. Развилки (решает Lead; OWNER — вопрос владельцу)

### 7.1. Развилки, открытые заново (B3): строка решений Lead противоречит тексту §7

Строка Lead (раздел «Решения Lead по развилкам», `:553` старой нумерации): «F-P1 … F-P13 — берутся рекомендованные варианты
(а), как записаны в §7». Для трёх развилок рекомендованный вариант — не (а), поэтому строка читается двумя способами.
Дизайнер не выбирает; план ниже исполним по рекомендации до решения, но L2 (край 5) по F-P4 не диспатчится до решения.

**F-P4. Строка `s1.review/unavailable`.** Противоречие: строка Lead — «(а)»; §7 — «Рекомендация: (б) сейчас + находка на (в)».
Чтение 1 (буквально «(а)»): находка ходока «условно предложенный ответ» + метка: L2 пишет `node` = FV3-17; строка остаётся
ожидаемо красной; цена — метка закрывает красное, вызванное миром, а не дефектом `main` (ошибка в сторону «скрыть
неисполнимость»). Чтение 2 (слово «рекомендованные»): (б) — строка обхода и строка реестра удаляются; находка (в) «условие
в грамматике ходока» — FV3-17 (L0 пишет файл); класс повторяется в группах (карточка групп, край 10). Рекомендация: чтение 2.

**F-P8. Двойной счёт `live_only`.** Противоречие: строка Lead — «(а)»; §7 — «(б) отдельным узлом после групп; группы пишут
по (а)». Чтение 1: (а) навсегда — двойные записи `raised_by` остаются нормой, строки FV3-14 в §9 нет. Чтение 2: группы пишут
по (а) сейчас + узел FV3-14 (правка `_count_reach`) после групп. Рекомендация: чтение 2 (две записи на один субъект — шум
храповика, который AR-20 должен читать без двусмысленности).

**F-P12. Критик кода перед посадкой.** Противоречие: та же строка — «(а)» и дальше «критик кода — один на тему после волны
групп» = (б); §7 рекомендует (а). Чтение 1 ((б), текст Lead): волна 1 по свидетелю, критик темы после групп (посадка + группы
одним проходом); цена — 4789+ строк уходят в `main` без критика, хотя каждый узел ветки отложил критика именно «до сходимости»
(t-695, t-721, t-735, t-751, t-789, t-828), а CLAUDE.md правило 3 делает критика обязательным для диффа > 100 строк;
такая приёмка требует явного отказа с причиной. Чтение 2 ((а)): узел CR-L до волны 1, критик групп — отдельная тема.
Рекомендация: чтение 2 (план написан так).

Строка Lead покрывает «F-P1 … F-P13»; развилки F10–F13 (П1-б §9) ею не решены: F11 рекомендует (б), F12 — число капа, F13 (а)
— они открыты (F12 нужен N5 край 4).

### 7.2. Новые развилки фикс-раунда

**F-P14. Как перепись догоняет `main` (B1).** (а) строка переписи на каждый стык «no row names it» (`reach: unwalked`,
`raised_by` на строку, группа по `stages`) — owns: шесть файлов `driver-exits`; цена: ~227 строк JSON и 227 записей
`raised_by`, NOTE храповика длинный; ошибка — в безопасную сторону (стык виден переписи и ждёт обхода); (б) сузить вселенную
переписи в `dry_exits` (стыки «сказано до работы» — не выходы драйвера): owns += `dry_exits.py` (`scan_joints`/`Universe`),
правка СМЫСЛА проверки — по PROJECT.md «изменение пакета» п. 6 нужен критик на план правки и измерение посылки; край: какой
признак отделяет «выход драйвера» (поле `joint` строки? семейство?) — не установлен; ошибка (б) — опасная сторона: стык,
который драйвер на деле отказывает, выпадает из переписи молча. Подвариант (а): (а1) записи `raised_by` (рекомендовано —
подъём назван в дереве, AR-20); (а2) база `unwalked` поднимается числом, подъём назван только в вердикте и строке
`architecture:`. Рекомендация: (а)+(а1).

**F-P15. Цель `unwalked` групп после L1c.** (а) группы обходят и стыки L1c до `unwalked: 0` (цена: до ~227 × 3 варианта
`repair`/`no repair`/`word` строк; ходок читает строку отказа только из ходов после ответа — отчёт n4g-s1s4 `:62`, многие
стыки не исполнимы сегодня); (б) группы доводят до 0 только эпоху N1; стыки L1c остаются `unwalked` с `raised_by`, по узлу
на группу позже (строка пачки на группу при приёмке групп). Рекомендация: (б).

**F-P16. Форма двери «только сухая стори» (F3).** (а) переиспользуемый `dry-story.yml` (`workflow_call`), его зовут ночь
(задача `dry-story`) и канон (вход `dry_only`, без `checks`/`full`/`clock`); `ci_read.py` не меняется (`--var dry_only=true`);
(б) задача в `nightly.yml` + булев вход `dry_only` в `canon.yml`, который зовёт ночь целиком с флагом, пропускающим
`package-full`/`install-smoke` (флаг протаскивается через ночь — больше условий в чужих задачах); (в) двери нет (как в
первом черновике): каждый вердикт части — целый канон, ~час на круг. Рекомендация: (а).

**F-P17. `dry_exits --judge` после N4R (F7).** (а) удалить функцию `judge` и ветку CLI (вызывающих нет, t-955 Grep); (б)
научить её файлу группы той же склейкой, что `dry_world.py:1335`. Рекомендация: (а) — одна дорога (`judge_group`), P31.

**F-P18. Потолок 900 против N2h (F5).** Пара: F-P5 «потолок 900 не растёт» и N2h, после которого проход идёт дальше S5 и
гонит мутационную пробу на каждый экземпляр. (а) потолок держится; кап пробы `PROBE_TIMEOUT_S` = 120 с в заглушке; время
режима по умолчанию > 800 с на CI ветки N2h → стоп, вопрос Lead до слияния (план так написан); (б) Lead заранее поднимает
`TEST_TIMEOUTS` по замеру CI ветки N2h (подъём назван в вердикте, AR-20); (в) режим по умолчанию останавливает главный
проход на S5 (цена: «идёт в CI» не дальше S5). Рекомендация: (а), при превышении — (б) словом Lead с числом CI.

**F-P19. Метка `P1B-2f` (`form-rounds.json:70`, B4).** Строка просит «Lead to confirm this row»: фильтр `row_field_gaps`
требует хэш, а контракт и `manifest_put.py` его отказывают. (а) подтвердить: находка FV3-18 (L0), метка переименовывается
(L2); (б) убрать строку — законно только если противоречие на итоговом дереве больше не воспроизводится (иначе
`test_field_producers.py` краснеет). Рекомендация: (а).

**F-P20. Минуты CI ночной задачи (F9) — возможно OWNER.** F-P3 (а) добавляет задачу `dry-story` в каждую ночь (оценка: 5
частей × 2-6 мин + шаг таблиц, не проверено). Платны ли минуты GitHub Actions этого репозитория — не установлено (ни
критик, ни дизайнер не проверяли). Lead подтверждает; если платны — вопрос владельцу простыми словами: «Сухая стори будет
гоняться каждую ночь, это примерно N минут CI в сутки. Оставляем каждую ночь, только по ручному запуску или раз в неделю?».
Рекомендация: Lead проверяет тариф до слияния N5; до ответа N5 сливается с ночным вызовом только при бесплатных минутах.

### 7.3. Развилки первого черновика, без изменений текста

**F10 (П1-б §9).** Как ходок узнаёт ключ цен. (а) обёртка `dry_driver.py` со шпионом на `no_move.priced_options`; (б) сопоставление
по множеству ответов; (в) драйвер пишет ключ сам. Факт: (а) построено (`dry_driver.py`, 82 стр.; отчёт N3 `:72`).
Рекомендация: (а) — уже на ветке, L1 её сажает; (в) — находкой для П1-в. Направление ошибки (б): неверный ключ у одинаковых
наборов (`s5.nobody_*`, `s8.delivery.*`) — запрещённая сторона.

**F11 (П1-б §9).** Где живёт проверка «у запрета без прохода названа дверь». (а) `dry_exits.ban_doors()` (тестовый слой);
(б) строка `refusal_registry.audit`. Рекомендация: (б), до решения (а) временным читателем с пометкой «перенести»; узел (б) —
отдельный, owns `PKG/scripts/refusal_registry.py` + строка его теста, вне этой спеки.

**F12 (П1-б §9).** Числа ворот N0 / кап задачи. Измерено после N0 (ветка): главный проход 381-385 с до S5 (N2g `:43`, s5stub
`:40`, S3 98.8 с, S4 74.0 с), части 110-343 с. Для N5 нужен кап на часть: рекомендация — 30 мин на часть до решения, затем
число Lead.

**F13 (П1-б §9).** `driven` «целиком» (а) или «хотя бы одна строка» (б). Рекомендация: (а) (E20). Следствие: `driven_keys()`
может оказаться пустым, N4c тогда ничего не сжимает (N4c край 1); см. F-P9.

**F-P1** (решено Lead: (а)) — файл реестра на группу, узел N4R. **F-P2** (решено Lead: (а), вопроса владельцу нет —
builder-rules 7b). **F-P3** (решено Lead: (а)) — задача в ночи; форма двери — F-P16, деньги — F-P20. **F-P5** (решено Lead:
(а)) — L2 пишет число по CI, потолок 900 (пара с N2h — F-P18). **F-P6** (решено Lead: (а)) — шаг задачи `dry-story`.
**F-P7** (решено Lead: (а)) — N2h до групп s5, s6-s9. **F-P9** (решено Lead: (а)) — строки ключей групп шага 4; s0/s1-s4 —
FV3-9. **F-P10** (решено Lead: (а)) — D-0048. **F-P11** (решено Lead: (а)) — построенные имена. **F-P13** (решено Lead: (а))
— `live-run-fvf`, пачка 3. Текст вариантов — как в первом черновике (t-944), не менялся.

Вопросы владельцу (OWNER) простыми словами: только F-P20, и только если минуты платны. Q1/Q2 П1-б §9.2 остаются открытыми.

---

## 8. Мелкие решения дизайнера

- Посадка — слиянием ветки в ветку пачки от `origin/main`, не перебазированием (истории узлов и отчёты сохраняются).
- L1, L1c, L-ax, L2 — одна ветка и одна волна: устаревшая метка и красная перепись не попадают на `main` ни на один коммит.
- Подкаталог `driver-exits/known_red/` (а не `known_red.<g>.json` рядом): файлы рядом читались бы как группы
  (`NOT_GROUP`, `dry_exits.py:39`; `load` `:210` — `glob("*.json")`).
- Список групп для матрицы — из `exits/*.json`, не из `groups_found` (тот добавляет группы переписи без файла обхода → FAIL EW1).
- Имена отчётов узлов: `docs/tasks/specs/reports/20261117-p1b-<узел>-report.md`; отчёт критика —
  `docs/tasks/specs/reviews/20261117-p1b-landing-code-critic.md`.
- Ветка посадки — `pile/live-run-fvf/batch-3` (по F-P13 (а)).
- Правило группы стыка L1c — по `stages`, многостадийный → `gates` (воспроизводит размещение 40 стоящих стыков).
- Класс метки — префикс поля `raised_by`: `stub gap:` / `product gap:` (поле свободное, форма реестра не меняется).
- `PROBE_TIMEOUT_S` = 120 с, таймаут = та же ветка, что rc≠0 (безопасная сторона: нет записи → нет прохода).
- Шаг `dry_exits.py --check` в задаче `dry-story` (5 с): детектор оси 38 в двери `dry_only`, где `full` не идёт.
- Номера узлов находок FV3-15…FV3-19 — предложение; окончательные выдаёт Lead в L0.

---

## 9. Строки кучки (F-P13 (а): `plans/piles/live-run-fvf/batch-3-live-run-fvf.md`, приоритет П1; пишет L0)

Шапка: `кучка: live-run-fvf | статус: ожидает | взял: — | ветка: — | MR: — | стенд: не нужен | приоритет: П1`.
Строки таблицы узлов (колонки как `batch-2-live-run-fvf.md:26`):

| Узел | Приоритет | Что | Исполнитель | Пишет в | Зависит от | Статус |
|---|---|---|---|---|---|---|
| FV3-1 | П1 | Посадка сухой стори: ветка `wip/p1b-n4m` сливается в `main` одной волной с FV3-15 и FV3-2; канон и ночь начинают гонять `test_scenario_dry_1.py` (спека `docs/tasks/specs/20261117-p1b-finish-spec.md` §4 L1, CR-L) | builder → critic | `scripts/tests/dry_*.py`, `scripts/tests/test_scenario_dry_1.py`, `scripts/tests/scenario_walk.py`, `scripts/tests/form_filler.py`, `scripts/tests/test_field_producers.py`, `scripts/tests/fixtures/{driver-exits,stories/dry-1,form-fill-rules.json,form-rounds.json}`, `scripts/tests/test_form_selftest.py`, `scripts/tests/test-layers.json` (строка keep), `scripts/selftest.py`, `scripts/slow_tests.json` | — | ожидает |
| FV3-15 | П1 | Перепись выходов догоняет `main` (стыки 40 → 267) + ось 38 карты (§4 L1c, L-ax; F-P14) | builder (+ Lead: ось) | `scripts/tests/fixtures/driver-exits/{gates,hooks,s0,s1-s4,s5,s6-s9}.json`; `docs/SIBLING_MAP.md` (Lead) | FV3-1 | ожидает |
| FV3-2 | П1 | Метки реестров истинны на слиянии: `main/S5`, `kind:halt/free words`, `s1.review/unavailable`, `P1B-2f` — на узлы с файлом находки; числа расписания по CI (§4 L2; F-P4, F-P5, F-P19) | builder | `scripts/tests/fixtures/driver-exits/known_red.json`, `…/stories/dry-1/selftest/known_red.json`, `…/stories/dry-1/exits/s1-s4.json` (F-P4 (б)), `scripts/tests/fixtures/form-rounds.json`, `scripts/slow_tests.json`, `scripts/selftest.py` | FV3-15 | ожидает |
| FV3-3 | П1 | Реестр меток по файлу на группу; `--judge` убран (§4 N4R; F-P1, F-P17) | builder → critic | `scripts/tests/dry_exits.py` (`check`, `_ledger_orphans`, `judge`), `scripts/tests/test_scenario_dry_1.py` (`main`), `scripts/tests/fixtures/driver-exits/known_red*` | FV3-2 | ожидает |
| FV3-4 | П1 | Задача CI `dry-story` в `dry-story.yml`, вызовы ночи и двери `dry_only`, спайк удалён (§4 N5; F-P2, F-P3, F-P6, F-P16, F-P20) | builder → critic | `.github/workflows/{dry-story,nightly,canon}.yml`, `tools/test_workflows.py` | FV3-2 | ожидает |
| FV3-5 | П1 | Заглушка критика кода S5 запускает `probe_by_code.py` (а) и метка главного прохода по CI (б) (§4 N2h; F-P7, F-P18); находка `findings/20261117-p1b-s5-zaglushka-kritika-ne-zapuskaet-probu.md` | builder → critic | `scripts/tests/dry_stub.py`, `scripts/tests/fixtures/stories/dry-1/story.json`; (б) `…/driver-exits/known_red.json` (`main/*`), `scripts/slow_tests.json` | FV3-2; (б) FV3-3 | ожидает |
| FV3-6 | П1 | Строки обхода группы `gates` (§4 N4) | builder | `scripts/tests/fixtures/stories/dry-1/{exits,seeds}/gates.json`, `scripts/tests/fixtures/driver-exits/gates.json`, `…/driver-exits/known_red/gates.json` | FV3-3, FV3-4 | ожидает |
| FV3-7 | П1 | Строки обхода группы `s5` (§4 N4) | builder | то же для `s5` | FV3-3, FV3-4, FV3-5 | ожидает |
| FV3-8 | П1 | Строки обхода группы `s6-s9` (§4 N4) | builder | то же для `s6-s9` | FV3-3, FV3-4, FV3-5 | ожидает |
| FV3-9 | П1 | Строки ключей цен групп `s0`, `s1-s4` (F-P9) | builder | `…/stories/dry-1/exits/{s0,s1-s4}.json` | FV3-3 | ожидает |
| FV3-10 | П1 | Перепись ключей вопросов: ключи сухой стори в `driven`, `PINNED_ELSEWHERE` сжимается (§4 N4c) | builder → critic | `scripts/tests/test_conductor_doors.py`, `scripts/tests/test-layers.json` (covers) | FV3-6…FV3-9 | ожидает |
| FV3-11 | П2 | Вторая строка раннеров TS/Playwright (§4 N6) | builder → critic | `…/stories/dry-1/runners/ts-playwright/`, `.github/workflows/dry-story.yml`, `tools/test_workflows.py` | FV3-4, FV3-7 | ожидает |
| FV3-12 | П2 | Типы сверх `default` (§4 N3t; A1; F-P11) | designer → builder | `…/stories/dry-<type>/`, `…/stories/dry-types.json`, `scripts/tests/test_scenario_dry_1.py` (`main`) | FV3-1, FV3-10 | ожидает |
| FV3-13 | П2 | «Сказано до работы» в сухой истории (§4 N3a; A2) | builder → critic | `scripts/tests/dry_exits.py` (`told_before_work`), `scripts/tests/test_scenario_dry_1.py` (`_print_told`) | FV3-3, П1-в N0 | ожидает |
| FV3-14 | П2 | Двойной счёт `live_only` (F-P8 (б) — только при чтении 2) | builder | `scripts/tests/dry_exits.py` (`_count_reach`) | FV3-6…FV3-8 | ожидает |
| FV3-16 | П1 | Находка: свободные слова человека на вопросе `halt` не доходят до роли (бывшая `N4S0-1`); причина не установлена — драйвер или стык заглушки | Lead (разбор) → builder | по разбору | — | ожидает |
| FV3-17 | П2 | Находка: ответ ключа цен предлагается условно, у ходока нет условия (бывшая `N4S14-1`; класс F-P4) | builder | `scripts/tests/dry_exits.py` / `dry_world.py` (грамматика условия) — по решению F-P4 | FV3-3 | ожидает |
| FV3-18 | П1 | Находка: `window_record.row_field_gaps` требует `obligation_hash`, а контракт и `manifest_put.py` его отказывают (бывшая `P1B-2f`) — по F-P19 (а) | Lead → builder | продукт: по разбору | — | ожидает |
| FV3-19 | П2 | Находка: у вложенного списка `probes.records` нет объявленного пустого исхода (`handoff.py:515-533`) | builder | продукт: `scripts/handoff.py` / контракт — по разбору | — | ожидает |

Строка «Пачки» карточки `live-run-fvf/README.md`: `| 3 | сухая стори идёт в CI на main: посадка ветки, перепись, метки, задача CI, обход всех групп, перепись ключей | FV3-1…FV3-19 | L | ожидает | — | — | — |`
(19 строк > 15 — размер «больше L»; правило карточки `:26-27` велит две пачки — решает Lead при L0: FV3-16…FV3-19 могут
уйти в пачку 4). Строки «Содержание» — по одной на файл находки L0.
Строка `очередь:` для `scenario_walk.py`/`test-layers.json`: `очередь: live-run-fvf/3 FV3-1 → forge/7 FG7-15 → forge/7 FG7-19`
(F-P10 (а)); для FG7-38 строка не нужна (F-P5 (а): L2 пишет числа). Узлы L0, L-ax, N-L — строками Lead, не билдера.

---

## 10. След чтения

| Что | Где | Результат |
|---|---|---|
| Бриф-носители | П1-б `:480-760`, `:760-959`, `:1-95` | F10-F13 без решения Lead |
| N4w-спека | `:1-287`, `:303-412`; заголовки `:411-645` | F-W1…F-W18 |
| Поправка | `20261113-p1-specs-amendment-owner-words.md:156-255` | N3t/N3a, A1-E*, A2-E* |
| Снимок | `docs/tasks/compact-snapshots/2026-11-14-0800-narrative.md:1-48` | `main/S5 -> P1B-9` устарела |
| Вердикт критика (фикс-раунд) | `docs/tasks/specs/reviews/t-955-p1b-finish-plan.md` целиком | B1–B4, F1–F11, K1–K10 |
| Рефы git (фикс-раунд) | `.git/refs/remotes/origin/main`, `.git/refs/heads/main` (оба `7103829a`); `.git/packed-refs` (Grep: `:34` `wip/p1b-n4m` = `9c9d40c2`); Glob `.git/refs/heads/**` (рыхлого рефа ветки нет; контроль — находит `main`) | §0, шапка |
| Счёт строк (фикс-раунд) | Grep `^` count по `MAIN/PKG/scripts` и `N4M/PKG/scripts` (набор из 15 файлов) | §2 «перемер» |
| Стыки (фикс-раунд) | Grep `"check":` count по `MAIN/PKG/references/stage-joints.json` (267); Grep строк `exit_gate:scoped|acceptance:quality|exit_gate:grounding|case_identity|digest|validate_artifacts:` с контекстом | правило группы L1c |
| Перепись (фикс-раунд) | `N4M/T/dry_exits.py:200-239` (`load`), `:600-741` (`_count_reach`, `check`, `_code_rows`, `_walk_problems`, `_raised`, `_ratchets`), `:757-778` (`_ledger`, `_ledger_orphans`), `:815-827` (`judge`), Grep `joint|def check|…` | L1c, N4R края 3 и 6 |
| Образец строки переписи | `N4M/T/fixtures/driver-exits/gates.json:60-101`; Grep ключей стыков по `N4M/.../driver-exits/*.json` (34 видимых) | L1c п. 1-3 |
| Метки (фикс-раунд) | Grep `P1B-2f` в `N4M/T` (`form-rounds.json:70`); `N4M/.../form-rounds.json:60-74`; Grep `-i` `P1B-2f|N4S0-1|N4S14-1|N4W-1` по `plans/` (0) с контролем `P1B-9|FV1-14` (74 в 19 файлах) | B4, L0, L2 край 7 |
| Отчёты ветки (фикс-раунд) | `N4M/…/20261114-p1b-n4g-s0-report.md:60-84`, `…-n4g-s1s4-report.md:48-62`, `…-s5stub-report.md:40-53` | тексты находок L0, F-P15 |
| Кучка | Glob `plans/piles/live-run-fvf/*.md` (batch-1, batch-2, README); `README.md:1-50` | `batch-3` нет; форма «Пачки»/«Содержание» |
| Карта | Grep `^## Axis` по `docs/SIBLING_MAP.md` (последняя — 37, `:627`); Grep `driver-exits|dry_exits|exits census` `-i` (0) с контролем `record_repeat|state_census` (6) | ось 38 новая |
| Гейт механизмов | `tools/mechanism_gate.py:56-71,206-245`, Grep `SIBLING_MAP|Axis|tier:` | L-ax — Lead |
| CI | `.github/workflows/canon.yml` целиком (на `7103829a`); Grep задач `nightly.yml`; `tools/test_workflows.py:20-50`, Grep `NAMES|spike|dry`; Grep `WORKFLOW|inputs|spike` `tools/ci_read.py` | N5, F-P16 |
| Читатели (правило 7) | §6 — команды и счёт | §6 |
| Тесты ветки | Glob `**/test_form_*.py` в `N4M/T` (`test_form_at_stop.py`, `test_form_view.py`, `test_form_selftest.py`); Glob `**/dry-codemie-14857/*` в `MAIN/T/fixtures/stories` (`story.json`) | L1 DoD, F10 |
| Первый черновик | как в t-944 (деревья, расписание, дверь, заполнитель, перепись ключей, `test-layers.json`, gates, стадии, null_outcomes, пачки, правила, R-L3, память) | §2–§4 |

Промахи вызова (отвергнуты как промах, не как отсутствие): Grep с `glob` вида `{a.py,tests/b.py}` (путь внутри скобок) и
Glob с шаблоном, начинающимся с пути каталога, не находили заведомо существующее; повтор с `**/{…}` нашёл.

Нужно сверх манифеста (прочитано): `.git/refs/*`, `.git/packed-refs`, `.git/worktrees/p1b-n4m/HEAD`, `tools/mechanism_gate.py`,
`tools/test_workflows.py`, `tools/ci_read.py`, `tools/lint_ratchet.py` (Grep), `docs/SIBLING_MAP.md` (Grep),
`plans/piles/live-run-fvf/README.md`, `PKG/references/stage-joints.json` (Grep), отчёты ветки `N4M/docs/tasks/specs/reports/*`.

---

## 11. Не сделано / не перемерено

- Против `origin/main` = `7103829a` (сегодняшние слияния): `merge-tree` (текстовые конфликты), `diff --stat`, точка
  ветвления, число расхождений переписи (оценка 227 — по t-955 на `42f5fcae`; стыков столько же — 267), маршруты/виды драйвера —
  **не перемерено** (у дизайнера нет git и запуска); команды — §3, выполняет Lead до L1.
- Совпадение счёта строк файлов посадки (§2) — не доказательство неизменности содержимого.
- Незакоммиченное в дереве `p1b-n4-gates` — `git -C C:\QAFactory\forge-repo\.claude\worktrees\p1b-n4-gates status --short`.
- Место остановки главного прохода на слитом дереве — меряет CI-1; прогноз «S5, запись пробы» — оценка по отчёту s5stub.
- Режим по умолчанию `test_scenario_dry_1.py` на верхушке ветки — не гонялся ни одним отчётом (t-955 K2).
- `test_form_at_stop.py`, `test_form_view.py`, `selftest.py --limits --lang` на слитом дереве — не гонялись (t-955).
- Платность минут GitHub Actions — не установлена (F-P20).
- Что меняют в стыках/отказах потоки rules-debt S7/S8 — не читано (L1c край 5 ловит последствие).
- Полнота читателей `SIBLING_MAP` в `.claude/skills/` — поиск упёрся в лимит времени (§6).
- R-L1…R-L10, значение `architecture.md:192` после Architect streams — не перечитано.
- Что именно читают `tools/story_capture.py`, `tools/install_parity_anchors.json`, `tools/source-split-carriers.json` в
  `scenario_walk.py`/`test-layers.json` — счёт есть, строки не разобраны.
- Статусы строк `forge/7`, `package-ci/4`, `live-run-fvf/2` на `7103829a` — не перемерены.
- Оси SIBLING_MAP в узлах перечислены выборочно; полный перечень по 38 осям на каждый механизм (правило 10 (b)) пишет коммит
  узла.
- Закрыто фикс-раундом: точка ветвления и хэш ветки (t-955 + `packed-refs`), журнал в ветке (нет, t-955), каталог
  `dry-codemie-14857` (есть), рекурсивность `dry_exits.load` (нет, `:210`).

---

## Решения Lead по развилкам (17.11.2026, Fable)

F-P1 … F-P13 — берутся рекомендованные варианты (а), как записаны в §7; порядок §0 стоит: L1 → L2 → {N5, N4R, N2h} →
{N4:gates, N4:s5, N4:s6-s9} → N4c → поздние узлы. F-P2: части `exits:<g>` локально не гоняются (builder-rules 7b), их
судит CI — вопроса владельцу нет, это действующее правило. F-P12: критик на план этой спеки — до L1 (t-955); критик
кода — один на тему после волны групп. Команды git из §3 перед L1 выполняет Lead заново (main ушёл вперёд от `cfe418b6`).

> Примечание дизайнера фикс-раунда (текст Lead выше не правлен): строка противоречит §7 для F-P4, F-P8, F-P12 — развилки
> открыты заново в §7.1 (B3); порядок §0 дополнен узлами L0, L1c, L-ax, CR-L, N2h-б (B1, B2, B4, F4) — Lead подтверждает
> новый порядок вместе с решениями §7.1 и §7.2.

---

## 12. Таблица исправлений фикс-раунда (t-955)

| # | Замечание | Что изменено | Где |
|---|---|---|---|
| B1 | Перепись красная на слитом дереве (227), DoD L1/L2 недостижимы | Новый узел L1c (owns — шесть `driver-exits/<g>.json`, правило группы по `stages`, `raised_by` на строку, DoD `0 discrepancies` + NOTE храповика, края: пустой дифф, маршруты/виды — стоп, дрейф до волны); порядок L1 → L1c → L-ax → CI-1 → L2; DoD L1 в двух мирах (до L1c — `<N> discrepancies` разрешённого вида, после — 0); проверка перед волной (шаг 9); инвариант «main не краснеет»; развилки F-P14 (направление), F-P15 (цель групп) | §0 п. 3, §1 (AR-28, AR-20, AR-13, K-C), §4 L1 край 4 и DoD, §4 L1c, §5 шаги 2, 9; §7.2 |
| B2 | 4789 строк без критика кода | Узел CR-L: один проход темы до волны 1, механический слой дословно (merge-tree, diff --stat, выводы DoD L1/L1c/L2, CI-2, --witness-for), ключи K-C1…K-C8, фикс-раунд свежим билдером, повтор по диффу фикса | §0 п. 5, §1 (CR-L), §4 CR-L, §5 шаги 7-8 |
| B3 | Строка решений Lead противоречит F-P4, F-P8, F-P12 | Три развилки открыты заново: цитата противоречия, два чтения, рекомендация; L2 край 5 по F-P4 не диспатчится до решения; отмечено, что F10–F13 строкой не решены; текст Lead не правлен, добавлено примечание | §7.1, раздел «Решения Lead» (примечание), §4 L2 край 5, карточка групп край 10 |
| B4 | Owns L1 без `form-rounds.json`, `test_field_producers.py`; `P1B-2f` без находки | Оба файла — в owns L1 (абсолютные пути) и в «Пишет в» FV3-1; узел Lead L0 пишет файлы находок (5 путей в `plans/piles/live-run-fvf/findings/`), пачку `batch-3` и строки README; L2 owns += `form-rounds.json` (край 7); развилка F-P19 | §2 (N2), §4 L0, §4 L1 owns, §4 L2, §9 (FV3-1, FV3-18), §7.2 F-P19 |
| F1 | §3 неверен: merge-tree чистый, поверхность смысловая | §3 переписан: текстовая поверхность (t-955), смысловая (190 коммитов, 91 файл продукта), команды перемера против `7103829a`; края L1 о конфликтах сведены в край 2 с пометкой «не перемерено» | §3, §4 L1 край 2 |
| F2 | Остановка из-за отставания заглушки — не находка продукта | L2 край 2: причина на стороне заглушки → метка с id узла заглушки, `raised_by: "stub gap: …"`; класс неясен — стоп; класс в `raised_by` всех меток | §1 (синхронизация), §4 L2 край 2, §8 |
| F3 | Нет двери «только сухая стори»; время задачи не названо | N5: переиспользуемый `dry-story.yml`, вызовы ночи и входа `dry_only` канона (вход `spike` убран), `ci_read.py --var dry_only=true`; край 10 — время двери и против часа канона; развилка F-P16 | §4 N5, §7.2 F-P16 |
| F4 | N2h пишет `known_red.json`, которым владеет N4R | N2h разделён: N2h-а (код, метку не трогает), N2h-б (метка `main/*` по CI после волны N4R, волна N2h = а + б) | §4 N2h, §5 шаги 11-12, §9 FV3-5 |
| F5 | Не названа пара «потолок 900» против N2h | N2h-а край 8 (конфликтующая пара, стоп при > 800 с), край 7 (`PROBE_TIMEOUT_S`); L2 край 10; развилка F-P18 | §4 N2h-а, §4 L2, §7.2 F-P18 |
| F6 | Класс F-P4 в группах; id ожидаемо красных — заранее | Карточка групп: край 10 (условно предложенный ответ — по F-P4), given — id находок в диспатче (FV1-7, FV1-8 для gates), край 2 | §4 N4 (given, края 2, 10, «Своё у групп») |
| F7 | `--judge` после N4R отвечает неверно | N4R край 6: удаление `judge` и ветки `--judge` с грепом вызывающих и положительным контролем; вариант «научить» — развилка F-P17 | §4 N4R, §7.2 F-P17 |
| F8 | AR-14 не назван; детектор синхронизации заглушки не назван | Строка AR-14 в §1; абзац «синхронизация заглушки с поведением ролей»: три детектора и класс метки | §1 |
| F9 | Ночные минуты CI — возможно деньги | Развилка F-P20: Lead проверяет тариф; при платных — вопрос владельцу простыми словами | §7.2 F-P20, §11 |
| F10 | §2 N3t «не установлено» неверно; факты §11 закрыты | §2 N3t: каталог `dry-codemie-14857` есть (Glob на `7103829a`); шапка и §11: хэш ветки (`packed-refs`), точка ветвления, журнала нет — по t-955, перемер против `7103829a` помечен «не перемерено» | шапка, §2, §11 |
| F11 | Нет оси карты для переписи | Узел Lead L-ax: ось 38 в `docs/SIBLING_MAP.md` на ветке посадки (черновик текста, цена, детектор, временной край); оси 38 в siblings узлов | §4 L-ax, §1, §6 (читатели карты), siblings L1/L1c/N5/N4 |
| — (дополнительно, по обходу артефакта) | L2 по F-P5 (а) пишет числа расписания, но их не было в owns | L2 owns += `slow_tests.json`, `selftest.py` (строки `test_scenario_dry_1.py`), край 10 | §4 L2 |
| — (дополнительно) | N4R край 3 поручал билдеру проверить рекурсивность `load` | Прочитано: `load` нерекурсивен (`dry_exits.py:210`); край переписан как факт + строка таблицы | §4 N4R край 3, §11 |

## Решения Lead по развилкам фикс-раунда (17.11.2026, Fable; черновик t-958 принят)

- F-P4 — чтение 2: (б) строка обхода и строка реестра удаляются; находка (в) «условие в грамматике ходока» — FV3-17.
- F-P8 — чтение 2: группы пишут по (а) сейчас + узел FV3-14 после групп.
- F-P12 — чтение 2: узел CR-L (критик кода посадки) ДО волны 1; критик групп — отдельная тема. Прежняя строка Lead
  «один критик после волны групп» отменена: 4789 строк без критика в main не уходят.
- F-P14 (а)+(а1); F-P15 (б); F-P16 (а); F-P17 (а); F-P18 (а), при превышении — (б) словом Lead с числом CI; F-P19 (а).
- F10–F13 первого черновика: F11 (б), F13 (а), F12 — число капа по рекомендации §7.3.
- F-P20: репозиторий публичный (измерено 17.11: `gh api repos/Xartaxana/Forge-for-QAFactory` -> `private: false,
  visibility: public`), минуты GitHub Actions для публичного репозитория не тарифицируются — вопроса владельцу нет;
  N5 сливается с ночным вызовом, F-P3 (а).
- L0 (находки и пачка) отдан билдеру одним диспатчем: это запись файлов по готовому тексту
  спеки; смысловые решения (классы находок, F-P4, F-P19) приняты выше.

Перемер §3 против нынешнего `origin/main` (17.11, команды §3):
`git merge-tree --write-tree --name-only origin/main wip/p1b-n4m` -> дерево `a4886f41af67bb06d4e92b4b3180e827d9e0d142`,
rc 0, конфликтов нет; `git diff --stat origin/main...wip/p1b-n4m` -> `47 files changed, 4789 insertions(+), 133
deletions(-)`; коммитов main после `e18e622f`, тронувших stage-joints.json / driver_dispatch.py / no_move.py /
refusal_registry.py: 9 (вселенная переписи сдвинута — её догоняет L1c).

## Решения Lead по вопросам билдера L1c (t-978), 17.11.2026 — «решила сама», до слова владельца

- Стоящий стык `branch_accounting:*` (S2–S5) лежит в `s1-s4.json`, правило групп даёт `gates`: НЕ переносится (перенос
  40 стоящих стыков — non-goal L1c); правило групп применяется только к новым строкам; расхождение — строка отчёта,
  решает узел обхода группы.
- Новые стыки со `stages: ['*']` (62: guard_pre_tool 24, handoff_check 19, host_adapter 8, stage_guard 8, exit_gate 3):
  `*` = все стадии = две и более групп → группа `gates` (как стоящие `exit_gate:scoped`/`digest`). Обратимо: строки
  переносит узел обхода группы. Стык без ключа `stages` или со стадией вне S0–S9, кроме `*`, — по-прежнему стоп.
- Факты посадки L1 (t-972): `merge-tree` против `66a6b264` → `a800932c…`, конфликтов нет; коммит слияния `8011b58b`,
  отчёт `bec6c773` на `pile/live-run-fvf/batch-3`; `dry_exits --check` = 227 строк вида «no row names it», 0 stale.
