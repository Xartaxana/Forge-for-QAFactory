# П1-б: довести сухую стори до «идёт в CI на main». ЧЕРНОВИК ДИЗАЙНЕРА (t-944)

Статус: черновик дизайнера (Opus) по брифу Lead 17.11.2026 (слово владельца 17.11: «всё что недоделанно делаем сегодня»).
До приёмки Lead — не диспатч. Развилки — §7 (ни одна не закрыта), мелкие решения дизайнера — §8, строки кучки — §9,
след чтения — §10, «не сделано / не установлено» — §11. Денежных цифр нет.

Обозначения. `PKG` = `ai-packages/qa-factory`; `T` = `PKG/scripts/tests`. `MAIN` = корень клона `C:\QAFactory\forge-repo`:
его `.git/refs/heads/main` и `.git/refs/remotes/origin/main` оба = `cfe418b6350f3573d37ba6198b6b107dfd13ad02` (прочитано
17.11), рабочее дерево — `main` на этом коммите (git status сессии: только неотслеживаемые файлы), поэтому файлы корня
читаются как `origin/main` на момент последнего fetch. `N4M` = `C:\QAFactory\forge-repo\.claude\worktrees\p1b-n4m`
(HEAD = `ref: refs/heads/wip/p1b-n4m`, `.git/worktrees/p1b-n4m/HEAD`). Хэши веток не прочитаны (refs упакованы): команда
Lead — `git -C C:\QAFactory\forge-repo rev-parse wip/p1b-n4m wip/p1b-n4w wip/p1b-n4-gates wip/p1b-n3`.

Спеки-основания: P1-b `docs/tasks/specs/20261113-p1b-dry-story-spec.md` (дальше «П1-б»); N4w
`docs/tasks/specs/20261114-p1b-n4w-exit-walker-spec.md` («N4w-спека»); поправка
`docs/tasks/specs/20261113-p1-specs-amendment-owner-words.md` («A1/A2»).

---

## 0. Вердикт коротко

1. На `main` стоит только N0/N1-слой: `dry_exits.py` (1657 строк), `dry_stub.py` (580), `dry_world.py` (651),
   `known_red.py` (152), перепись `fixtures/driver-exits/` (8 файлов, реестр меток пуст), `fixtures/stories/dry-types.json`,
   `fixtures/dry-walk/seeds/probe.json`, задача CI `dry-story-spike` (`.github/workflows/canon.yml:64-81`). Ни
   `test_scenario_dry_1.py`, ни двери `driver`, ни истории `dry-1`, ни строки `keep` на `main` нет — сухая стори в каноне
   сегодня НЕ идёт вообще.
2. Всё сделанное после N1 живёт в ОДНОЙ ветке `wip/p1b-n4m` (N2, N3, N4w + фикс, N4:s0, N4:s1-s4, заглушка S5).
   `wip/p1b-n4w` — её подмножество без фикса; дерево `p1b-n4-gates` — уровня N3, без ходока (узел gates не начат).
3. Первый узел — ПОСАДКА (L1): слить `wip/p1b-n4m` в `main`. С ней `full` (ночной `package-full` и канон) начинает гонять
   режим по умолчанию `test_scenario_dry_1.py` (перепись + главный проход) — это уже «идёт в CI на main» для главного прохода.
4. Три метки реестра на ветке не годятся для слияния как есть: `main/S5 -> P1B-9` устарела (P1B-9 слит, причина остановки
   S5 на ветке другая — запись пробы), `N4S0-1` и `N4S14-1` — id без файла находки и строки пачки (D-0044). Их чинит L2.
5. Части обхода `--part exits:<g>` дороже минуты (110-385 с замера) и по builder-rules 7b локально не гоняются; задачи CI для
   них нет. Поэтому N5 (задача CI сухой стори) рекомендован РАНЬШЕ групп (F-P2), а не последним, как в П1-б §6.
6. Общий реестр меток `driver-exits/known_red.json` с пином-равенством `pins.known_red` — точка гарантированного конфликта
   параллельных групп. Рекомендация: файл реестра на группу, отдельным последовательным узлом N4R до групп (F-P1).

Порядок (на рекомендациях): L1 → L2 → {N5, N4R, N2h} параллельно → {N4:gates, N4:s5, N4:s6-s9} параллельно → N4c →
{N6, N3t, N3a} (каждый со своим ожиданием, §5). N-L — узел Lead, требования R-L1…R-L10 П1-б §6 и A2.

---

## 1. Инварианты AR-n, владельцы проверок, классы (CLAUDE.md правило 10, роль дизайнера правило 1)

Все узлы пишут только `PKG/scripts/tests/`, данные расписания тестов (`PKG/scripts/selftest.py` словарь `TEST_TIMEOUTS`,
`PKG/scripts/slow_tests.json`), `PKG/changelog.d/`, `.github/workflows/` и `tools/test_workflows.py`. Код продукта вне
`scripts/tests/` не меняется ни одним узлом этой спеки (кроме строк расписания). «Держит» = слой становится детектором
инварианта или соблюдает его внутри тестового слоя.

| AR | Что делает эта спека | Проверка изменения (в DoD узла) |
|---|---|---|
| AR-28 (неизвестное не проходит) | L2: остановка главного прохода — только на строке реестра с живой находкой; N4R: отсутствующий файл реестра группы = пустой реестр, красная строка без метки = FAIL «new red»; N5: группа без своего файла обхода не выпадает молча (печать списка групп) | L2: вывод CI `NOTE dry-1/main/known_red: known red: main/S<n> -> <id>` и ни одной FAIL; N4R: строка таблицы `dry_exits.py --selftest` «absent group ledger -> empty -> unlabeled red is FAIL» |
| AR-20 (храповики убывают) | группы N4 понижают базы `unwalked` в СВОЁМ файле `driver-exits/<g>.json`; рост `live_only` — только строкой `raised_by`; N4c сжимает `PINNED_ELSEWHERE` | `dry_exits.py --check` = `0 discrepancies` (каждая группа); N4c: из `PINNED_ELSEWHERE` удалены ровно ключи `dry_exits.driven_keys()` |
| AR-22 (поле читается — у него писатель) | N4R: у каждого файла реестра группы один писатель (узел группы) и два читателя (`exits_part`, `_ledger_orphans`) в одном коммите; N2h: запись пробы `work/probes/<IID>.json` пишет настоящий `probe_by_code.py`, читатель — заполнитель `world_list` | N4R: строка таблицы «orphan in group ledger -> red»; N2h: строка `dry_stub.py --selftest` «critic branch ran probe_by_code; record exists» |
| AR-15 (один выживший) | одна задача CI сухой стори (N5) вместо спайка; одна перепись ключей вопросов (`test_conductor_doors.py`, N4c); один помощник меток (`known_red.py`, не меняется) | N5: `tools/test_workflows.py` строка «spike job absent, dry-story job present» |
| AR-17 (одна дверь к дирижёру) | ни один узел не присваивает атрибут `Driver`; заглушка — на границе процесса | грep `driver\.[a-z_]+ =` по owns узла пуст; положительный контроль — `RM/scripts/tests/test_stage_critic_route.py:279` (П1-б `:47`) |
| AR-29 (код судит данные) | исход каждой строки обхода задан строкой (вердикт заглушки, ход дирижёра), не вычислен; N2h запускает настоящий инструмент роли, не придумывает вердикт пробы | грep `result_text|brief` по новым функциям owns пуст (положительный контроль `T/dry_stub.py` `result_text`, N4w-спека §1) |
| AR-13 (факт через свою функцию) | реестр меток читается только `known_red.load/reconcile`; готовность гейта — `dry_world.gate_ready` | N4R: грep `json.load` по путям реестра в owns пуст (кроме `known_red.py`) |

Не тронуты (по строке): AR-1…AR-12 (кроме AR-1 внутри слоя: группы, файлы реестров — данные), AR-14, AR-16, AR-18 (форма
вывода ходока не меняется), AR-19, AR-21, AR-23…AR-27 — продукт не меняется.

Строки коммита пакета: форма строк `architecture:` и `judgment:` — ТОЛЬКО по `tools/architecture_gate.py` (грамматику
здесь не копирую). Каждый узел, трогающий `PKG/`, называет в `architecture:` AR-n своей строки таблицы выше;
`judgment: none` пишется только с ` -- <почему>` (например: «тестовый слой, суждений роли не проверяет»).

### Проверки, которые спека добавляет или меняет: владелец (P27) и класс (AR-29)

`test_judgment_census.py` не считает `scripts/tests/` (П1-б `:71-73`); классы — для вопроса 11 критика.

| # | Проверка | Узел | Владелец | Класс |
|---|---|---|---|---|
| K-L | Остановка главного прохода есть строка `main/S<n>` реестра, её `node` — открытая находка с файлом | L2 | данные (код); чья находка — Lead | presence |
| K-R1 | Строка реестра группы называет id строки из `exits/<g>.json` той же группы | N4R | данные | xref |
| K-R2 | Пин `pins.known_red` равен числу строк файла (существующая проверка `known_red.pin_problem`, теперь на файл) | N4R | данные | shape |
| K-P | Заглушка критика S5 запускает `probe_by_code.py` на каждый экземпляр окна; запись есть до формы | N2h | данные | presence |
| K-CI | Задача CI гоняет каждую группу, у которой есть `exits/<g>.json`, и чистые таблицы `dry_exits.py --selftest`, `dry_stub.py --selftest` | N5 | данные | presence |
| K15/driven | Ключи сухой стори входят в `driven` переписи; `PINNED_ELSEWHERE` сжимается | N4c | данные | xref |
| C2…C9 | Проверки строк обхода (как построены N4w) | N4:<g> | как N4w-спека §1 (C4г — замысел владельца P13/FR-4, код проверяет только наличие прохода и записи) | как N4w-спека §1 |

Суждение (годится ли строка, баг ли красный, хорош ли ход дирижёра) не проверяется нигде — П2-г, критик, живой прогон.

### Оракул каждой новой строки теста

- Строки обхода N4: ожидаемое — из строки обхода, заданной по `RM/references/question-prices.json` (варианты ключа), по
  П1-б §3.3/§3.6 (класс ГЕЙТ/ЗАПРЕТ из `fixtures/driver-exits/classes.json`), по `expect.owner_quote` с носителем (E14) —
  никогда не из вывода прогона. Красная строка получает метку только с находкой (файл + строка пачки), не «как сейчас».
- N4R: ожидание таблицы — правило «id реестра группы ⊂ id строк той же группы» (эта спека §4 N4R п. 3) и равенство пина
  (`known_red.py` `_about`, `fixtures/driver-exits/known_red.json:2`).
- N2h: ожидание — «запись пробы есть для каждого экземпляра окна» (контракт `s5-critic-to-automator`, поле
  `probes.records`, `T/test_handoff.py:144` его называет; `probe_by_code.py:19` пишет `work/probes/<IID>.json` — по отчёту
  s5stub `N4M/docs/tasks/specs/reports/20261114-p1b-s5stub-report.md:47`).
- N5: ожидание — строки `tools/test_workflows.py` из текста этой спеки (имена задач, `if`, `needs`), не из YAML.
- N4c: ожидание — множество `dry_exits.driven_keys()` (производитель N1/N4w), а не список, собранный из вывода переписи.

---

## 2. Состояние, измеренное 17.11 (по чтению деревьев)

Метод: Glob/Grep по `MAIN` и `N4M` (и деревьям `p1b-n4w`, `p1b-n4-gates`, `p1b-n3`); счёт строк — Grep `^` count;
отсутствие — с положительным контролем той же формы (§10). Где нужен git — «не установлено» и команда.

| Узел | На `origin/main` (носитель) | Только на ветке (ветка, файлы) | Нет нигде |
|---|---|---|---|
| N0 спайк | `T/dry_world.py` (651 стр., `--spike`), `T/dry_stub.py` (580), `T/fixtures/dry-walk/seeds/probe.json`, `T/fixtures/stories/dry-types.json`, `.github/workflows/canon.yml:35-40,64-81` (вход `spike`, задача `dry-story-spike`); отчёты `docs/tasks/specs/reports/20261113-p1b-n0-*.md` | — | — |
| N1 перепись | `T/dry_exits.py` (1657), `T/known_red.py` (152), `T/fixtures/driver-exits/{classes,gates,hooks,s0,s1-s4,s5,s6-s9,known_red}.json`; `known_red.json:3-4` = `{}` / пин 0 | — | — |
| N2 заглушка, история (N2…N2g) | — | `wip/p1b-n4m` (через `wip/p1b-n3`): `T/dry_driver.py` (82, новый), `T/dry_stub.py` (1627), `T/form_filler.py` (1288 против 1135 на main), `T/fixtures/form-fill-rules.json` (398 против 373), `T/test_form_selftest.py` (126 против 79), `T/fixtures/stories/dry-1/{story.json,kit.json,impl.diff,ticket/DRY-1.md,runners/python-pytest/…}`, `PKG/changelog.d/p1b-n2-dry-stub.md`; отчёты `N4M/docs/tasks/specs/reports/20261114-p1b-n2*-report.md` | — |
| N3 дверь, главный проход | на main грep `test_scenario_dry` по `PKG/scripts` — 0 (контроль `test_scenario_cart|test_scenario_local` — 12 строк); `T/scenario_walk.py:40` без `driver` | `wip/p1b-n4m`: `T/test_scenario_dry_1.py` (новый), `T/scenario_walk.py:40,48` (`driver`), `T/test-layers.json:5109-5123` (строка `keep`), `PKG/scripts/selftest.py:115-117` (`TEST_TIMEOUTS` 900), `PKG/scripts/slow_tests.json:119` (51.0), `PKG/changelog.d/p1b-n3-driver-door.md` | — |
| N4w ходок (+ фикс t-828) | — | ходок: `wip/p1b-n4w` и `wip/p1b-n4m` (`T/dry_world.py:1279` `walk_exits`, `T/dry_exits.py:1328` `judge_group`, `T/test_scenario_dry_1.py:80` `exits_part`, `T/fixtures/stories/dry-1/selftest/{exits,seeds}/selftest.json`, `.../selftest/known_red.json`, `PKG/changelog.d/p1b-n4w-exit-walker.md`); фикс (изоляция `--selftest`, `alive` под меткой) — ТОЛЬКО `wip/p1b-n4m` (грep `isolation: a real-looking walk file` по деревьям — 1 файл, `N4M/.../dry_exits.py`) | — |
| N4:s0 | — | `wip/p1b-n4m`: `T/fixtures/stories/dry-1/exits/s0.json` (10 строк), `.../seeds/s0.json` (рецепт `to-halt`), `T/fixtures/driver-exits/s0.json` (83 против 66), строка реестра `kind:halt/free words -> N4S0-1` (`N4M/.../driver-exits/known_red.json:5`) | находка `N4S0-1` (грep вне `.claude/` — только журнал и снимки) |
| N4:s1-s4 | — | `wip/p1b-n4m`: `.../exits/s1-s4.json` (11 строк), `.../seeds/s1-s4.json` (`recipes: {}`), `T/fixtures/driver-exits/s1-s4.json` (93 против 79), строка `s1.review/unavailable -> N4S14-1` (`known_red.json:6`) | находка `N4S14-1` (то же) |
| Заглушка S5 (s5stub, t-…; вне списка узлов П1-б) | — | `wip/p1b-n4m` (из `wip/p1b-s5stub` dbf413d9 по отчёту): `T/form_filler.py:77,316,447-463` (`task_root`, `world_list`), `T/fixtures/form-fill-rules.json:31` (`world_list_tokens`), `T/test_form_selftest.py:79-80`, `T/dry_stub.py` (`kit_context(task_root=…)`); на main грep `world_list` — 0 (контроль на main `class FillContext|task_root` — 4 строки) | запуск `probe_by_code.py` заглушкой (отчёт s5stub `:47`) |
| N4:gates | перепись `T/fixtures/driver-exits/gates.json` (101 стр., 21 запись `unwalked`, `:94-100`) | дерево `p1b-n4-gates` (HEAD `wip/p1b-n4-gates`): уровень N3 — нет `exits_part`/`walk_exits`/`judge_group` (грep 0; контроль той же формы в `N4M` — 3 строки), нет `exits/`; незакоммиченное в нём — **не установлено**: `git -C C:\QAFactory\forge-repo\.claude\worktrees\p1b-n4-gates status --short` | строки обхода `exits/gates.json` |
| N4:s5 | перепись `driver-exits/s5.json` (149) | — | строки обхода |
| N4:s6-s9 | перепись `driver-exits/s6-s9.json` (55) | — | строки обхода |
| N4c | `T/test_conductor_doors.py:636` `PINNED_ELSEWHERE`, `:670` `census_problems`; `test-layers.json:672` keep | — | правка |
| N5 | только `dry-story-spike` (`canon.yml:64-81`) | — | задача `dry-story` |
| N6 | — | — | `stories/dry-1/runners/ts-playwright/` (в `N4M/.../runners/` только `python-pytest`) |
| N3t | `dry-types.json:1-14` (`default: codemie-14857`, вход `dry-codemie-14857`) | — | каталог `fixtures/stories/dry-codemie-14857/` — **не установлено** (не искал отдельно): Glob `T/fixtures/stories/dry-codemie-14857/**` |
| N3a | — | — | функция `told_before_work`; поправка A2 называет файл `test_scenario_dry.py`, построен `test_scenario_dry_1.py` |
| N-L (R-L1…R-L10) | R-L3: `PKG/design/architecture.md:192` содержит `NO_MOVE_BASELINE_MAX` (строка подтверждена Grep; значение 102 против 55 в `audit_factory.py` — по дайджесту скаута t-941, мной не перечитано); R-L1 строки `docs/SIBLING_MAP.md` — по t-941, не перечитано | — | R-L2, R-L4…R-L10 — по t-941 не начаты (не перечитано) |

Пачки: ни один узел П1-б не стоит строкой пачки (бриф Lead, t-941). Связанные строки, которые есть: `forge/7` FG7-15 (`:38`),
FG7-19 (`:42`), FG7-38 (`:61`, «числа slow_tests/selftest после N3», зависит от слияния `wip/p1b-n3`) — все «ожидает»;
`live-run-fvf/2` FV2-13 (`:40`, «ожидает», пишет `dry_exits.py`, `known_red.py`, `dry_stub.py`); пачка
`package-ci/4` — «ожидает» (`:3`), PC4-15…PC4-18 (`:36-39`).

---

## 3. Поверхность конфликта посадки

Файлы, которые `wip/p1b-n4m` меняет, против `main` сегодня. Сравнение по чтению (счёт строк, ключевые строки); какие из
них `main` менял ПОСЛЕ точки ветвления — **не установлено**, команда Lead до диспатча:
`git -C C:\QAFactory\forge-repo log --oneline $(git -C C:\QAFactory\forge-repo merge-base origin/main wip/p1b-n4m)..origin/main -- ai-packages/qa-factory/scripts/tests/dry_exits.py ai-packages/qa-factory/scripts/tests/dry_stub.py ai-packages/qa-factory/scripts/tests/dry_world.py ai-packages/qa-factory/scripts/tests/form_filler.py ai-packages/qa-factory/scripts/tests/fixtures/form-fill-rules.json ai-packages/qa-factory/scripts/tests/test_form_selftest.py ai-packages/qa-factory/scripts/tests/scenario_walk.py ai-packages/qa-factory/scripts/tests/test-layers.json ai-packages/qa-factory/scripts/selftest.py ai-packages/qa-factory/scripts/slow_tests.json ai-packages/qa-factory/scripts/tests/fixtures/driver-exits ai-packages/qa-factory/scripts/tests/known_red.py ai-packages/qa-factory/scripts/tests/harness.py logs/journal`
и `git -C C:\QAFactory\forge-repo diff --stat origin/main...wip/p1b-n4m`.

| Файл | main | ветка | Ожидание (оценка, не проверено) |
|---|---|---|---|
| `T/test-layers.json` | 10718 стр. | 10733 | ветка +15 при строке `keep` ~15 стр.; `main` меняется часто (PC4, TD-15) — конфликт вероятен в районе `:5089-5130` (соседи `test_scenario_cart_1`/`local_1_0108`) |
| `PKG/scripts/slow_tests.json` | `:118-120` cart/local | `:119` вставка `dry_1` между cart и local | соседняя вставка — конфликт возможен |
| `PKG/scripts/selftest.py` | `:113-116` | `:115-117` вставка | ханк `main` не менялся — вероятно чисто |
| `T/scenario_walk.py` | 935, `:40` без `driver` | 936, `:40,48` | FG7-15/FG7-19 не слиты — вероятно чисто |
| `T/form_filler.py`, `form-fill-rules.json`, `test_form_selftest.py` | 1135 / 373 / 79 | 1288 / 398 / 126 | файлы П1-а; правки `main` после ветвления не установлены — первый кандидат на конфликт |
| `T/dry_exits.py`, `dry_stub.py`, `dry_world.py` | N0/N1-версии | +967 / +1047 / +730 | если `main` их не трогал после N1 — чисто |
| `T/fixtures/driver-exits/known_red.json` | пусто, пин 0 | 3 строки, пин 3 | чисто по тексту; по смыслу — L2 |
| `T/fixtures/driver-exits/s0.json`, `s1-s4.json` | 66 / 79 | 83 / 93 | чисто, если `main` не менял |
| `T/known_red.py`, `T/harness.py` | 152 / 535 | 152 / 535 | одинаковый счёт строк — вероятно без изменений |
| `PKG/changelog.d/` | есть `p1b-9-fix-round.md` | нет его; есть `p1b-n2-dry-stub.md`, `p1b-n3-driver-door.md`, `p1b-n4w-exit-walker.md` | только добавления — чисто |
| `docs/tasks/specs/reports/20261114-p1b-*`, `docs/tasks/specs/reviews/*` | нет отчётов N2…N4g | есть | добавления — чисто |
| `logs/journal/*.jsonl` | — | содержит ли ветка строки журнала — **не установлено** | конфликт журнала НЕ решается руками (L1 edges) |

Пересечения по смыслу на `main`: P1B-9 (C1-C4 + фикс-раунд t-831) слит — ветка содержит C1-C4 (отчёты `p1b9-c1…c45`) без
фикс-раунда (нет `p1b9-fix-report.md`, нет `p1b-9-fix-round.md`); на `main` есть новый модуль `PKG/scripts/null_outcomes.py`
(`:113`). Отсюда: место остановки главного прохода после слияния может сдвинуться — его меряет CI (L2).

---

## 4. Узлы

**Свидетель любого узла** (builder-rules 7b, CLAUDE.md правило 4): `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <owns>`
печатает список; ЛОКАЛЬНО гоняются только файлы до минуты. `test_scenario_dry_1.py` в любом режиме (по умолчанию ~385 с,
части 110-385 с — отчёты N2g `:43`, s5stub `:40`, N4:s0 `:43`, N4:s1-s4 `:40`) и `test_conductor_doors.py` (53.0 с,
`slow_tests.json:20`) локально НЕ гоняются: их судит CI; задачу запускает и читает координатор
(`python -B tools/ci_read.py start --ref <ветка>`, `python -B tools/ci_read.py why`), билдер CI не запускает и не ждёт
(PROJECT.md «Командная работа» п. 13). Новых тестовых файлов ни один узел не создаёт; новый случай — строка таблицы
`--selftest` своего модуля или строка обхода (TESTING.md «Бюджет / Файлы» `:117`; исключение сухой стори по времени —
TESTING.md `:130-132`).

### L1 — посадка `wip/p1b-n4m` в `main`

given: эта спека §2, §3; `N4M/docs/tasks/specs/reports/20261114-p1b-n3-report.md`, `…-n4w-report.md`, `…-n4wfix-report.md`, `…-n4g-s0-report.md`, `…-n4g-s1s4-report.md`, `…-s5stub-report.md`; `C:\QAFactory\forge-repo\plans\builder-rules.md` (7b, 18, 19); `C:\QAFactory\forge-repo\ai-packages\qa-factory\design\factory-rules.md` (целиком, PROJECT.md «изменение пакета» п. 1); `C:\QAFactory\forge-repo\docs\TESTING.md`; вывод двух git-команд Lead из §3 (вставить в диспатч)
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
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\driver-exits\
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\stories\dry-1\ (новый на main)
C:\QAFactory\forge-repo\ai-packages\qa-factory\changelog.d\p1b-n2-dry-stub.md (новый на main)
C:\QAFactory\forge-repo\ai-packages\qa-factory\changelog.d\p1b-n3-driver-door.md (новый на main)
C:\QAFactory\forge-repo\ai-packages\qa-factory\changelog.d\p1b-n4w-exit-walker.md (новый на main)
C:\QAFactory\forge-repo\docs\tasks\specs\reports\ (только файлы `20261114-p1b-n*` и `20261114-p1b-s5stub-report.md`, приходящие с веткой)
C:\QAFactory\forge-repo\docs\tasks\specs\reports\20261117-p1b-l1-report.md (новый, отчёт узла)
non-goals: любая правка поведения сверх того, что несёт ветка (кроме разрешения конфликта); строки реестра меток по смыслу (L2); числа `slow_tests.json`/`TEST_TIMEOUTS` по новому замеру (F-P5: L2 или FG7-38); строки обхода; `canon.yml`/`nightly.yml` (N5); `known_red.py`, `harness.py`; журнал руками; запуск CI, мутаций, медленных файлов
handoff: отчёт билдера `C:\QAFactory\forge-repo\docs\tasks\specs\reports\20261117-p1b-l1-report.md` (правило 7 `.claude/agents/builder.md`): ветка и хэш, список конфликтов и как решён каждый (сторона и почему), проход FR по затронутым разделам, дословные выводы прогонов DoD с секундами
edges: (1) ветка — `pile/<slug>/batch-<N>` от `origin/main` (PROJECT.md «Командная работа» п. 1), затем `git merge --no-ff wip/p1b-n4m`; (2) конфликт в файле П1-а (`form_filler.py`, `form-fill-rules.json`, `test_form_selftest.py`): обе стороны держатся (функции `main` + `world_list`/`task_root`/`plan_rows` ветки); если две стороны меняют ОДНУ функцию по-разному — стоп, вопрос Lead с обоими текстами (инвариант: правка П1-а с `main` никогда не теряется молча); (3) конфликт `test-layers.json` / `slow_tests.json` / `selftest.py`: сторона `main` целиком + одна строка ветки (`keep` `test_scenario_dry_1.py` с `covers` как `N4M/.../test-layers.json:5112-5121`; 51.0; 900); инвариант: канон не получает `unlisted:` и не теряет ни одной строки `main`; (4) конфликт в `logs/journal/*.jsonl` или `CURRENT_CONTEXT.md` — НЕ решается: стоп и вопрос Lead (журнал пишет только `tools/journal_write.py`, проверка — `tools/journal_validator.py --merge-parent`); (5) ВРЕМЕННОЙ: до L1 `--witness-for` не знает `test_scenario_dry_1.py` (строки `keep` нет); после L1 — знает; DoD гоняет `--witness-for` на итоговом дереве; (6) ВРЕМЕННОЙ: после L1 задача `full` (ночной `package-full`, `.github/workflows/nightly.yml:72-104`, и канон) гоняет режим по умолчанию `test_scenario_dry_1.py`; пока L2 не слит, метка `main/S5 -> P1B-9` устарела по смыслу — поэтому L1 и L2 сливаются в `main` ОДНОЙ волной (`tools/wave.py merge`), L1 отдельно в `main` не идёт; (7) коммит-хук печатает WARN «`dry_driver.py` matches no feature» (`plans/features.json`; отчёт N3 `:54`) — это WARN, не отказ; правка `plans/features.json` — не этот узел (строка отчёта); (8) `lint_ratchet.py` начнёт сканировать `test_scenario_dry_1.py` (`tools/lint_ratchet.py:11`): рост — строка отчёта, судит канон (`forge-check`); (9) пустой результат `--witness-for` для пути (`no scenario or keep row covers`) — строка отчёта, не повод писать тест (builder-rules 7b)
DoD: (а) `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/tests/dry_world.py ai-packages/qa-factory/scripts/tests/dry_exits.py ai-packages/qa-factory/scripts/tests/dry_stub.py ai-packages/qa-factory/scripts/tests/form_filler.py ai-packages/qa-factory/scripts/driver_machine.py` называет `test_scenario_dry_1.py` для четырёх `dry_*`/`driver_machine.py`; (б) быстрые свидетели, каждый отдельно, дословно: `python -B ai-packages/qa-factory/scripts/tests/dry_exits.py --selftest` (все случаи, 154 на ветке по отчёту фикса), `python -B ai-packages/qa-factory/scripts/tests/dry_exits.py --check` (`0 discrepancies`), `python -B ai-packages/qa-factory/scripts/tests/dry_stub.py --selftest` (все строки), `python -B ai-packages/qa-factory/scripts/tests/test_form_selftest.py`, `python -B ai-packages/qa-factory/scripts/tests/test_form_at_stop.py`, `python -B ai-packages/qa-factory/scripts/tests/test_form_view.py`, `( cd ai-packages/qa-factory && python -B scripts/selftest.py --limits --lang )` в subshell worktree — каждый зелёный; любой из них дольше минуты — строка отчёта с секундами, не повтор; (в) грамматика частей, секунды: `python -B ai-packages/qa-factory/scripts/tests/test_scenario_dry_1.py --part exits:` → rc 2; `--part exits:nosuch` → rc 2 с перечнем групп; (г) отчёт называет строкой: «`test_scenario_dry_1.py` (по умолчанию, `--part main`, `--part exits:*`) судит CI — L2»; (д) коммит слияния несёт строки `architecture:`/`judgment:` по `tools/architecture_gate.py` (AR-28, AR-20, AR-22, AR-17, AR-29 — как держится — одной строкой)
siblings: ось 18 (храповики `driver-exits` приходят на main вместе с базами), ось 34 (одна дорога: дверь `driver` — тот же процесс `story_run`), ось 17 (форма вывода ходока); остальные оси — как П1-б §7(b)
designer: C:\QAFactory\forge-repo\docs\tasks\specs\20261117-p1b-finish-spec.md (до приёмки — черновик)

Что ветка НЕ несёт из `wip/p1b-n4w` / `wip/p1b-n4-gates`: ничего — `wip/p1b-n4w` — подмножество (ходок без фикса), дерево
`p1b-n4-gates` — уровень N3 без строк обхода. Узел L1 их не сливает; Lead убирает ветки и деревья `wip/p1b-n4w`,
`wip/p1b-n4-gates`, `wip/p1b-n3`, `wip/p1b-n4g-*`, `wip/p1b-s5stub`, `wip/p1b-n4wfix` после волны (PROJECT.md п. 12) — если
`git status` дерева `p1b-n4-gates` пуст (§2).

### L2 — метки реестра, истинные на момент слияния (последовательно после L1, та же ветка, та же волна)

Шаги: (1) Lead ДО диспатча заводит находки (файл в `findings/` + строка пачки тем же ходом, D-0044) и id: `<S5-стоп>`
(рекомендация текста: «заглушка критика кода не запускает `probe_by_code.py`, записи пробы нет; у контракта нет пустого исхода
вложенного списка `probes.records` (`handoff.py:515-533`)» — отчёт s5stub `:46-50`), `<halt>` (вместо N4S0-1, отчёт N4:s0
`:67`), `<unavailable>` (вместо N4S14-1 — по F-P4); (2) координатор запускает канон на ветке L1
(`python -B tools/ci_read.py start --ref <ветка>`) и читает `python -B tools/ci_read.py why` — строки
`dry-1/main/known_red` и `dry-1/main/stop` задачи `full`; (3) билдер L2 (свежий, по фикс-раунду: дифф + вывод CI) пишет метки.

given: вывод CI шага (2) дословно (строки `dry-1/main/*`); id находок шага (1); `C:\QAFactory\forge-repo\.claude\worktrees\p1b-n4m\ai-packages\qa-factory\scripts\tests\fixtures\driver-exits\known_red.json`; эта спека §4 L2
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\driver-exits\known_red.json
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\stories\dry-1\selftest\known_red.json
C:\QAFactory\forge-repo\docs\tasks\specs\reports\20261117-p1b-l2-report.md (новый)
non-goals: починка причины остановки (N2h, узлы находок); заведение находок (Lead); числа расписания, если F-P5 (б)
handoff: отчёт `C:\QAFactory\forge-repo\docs\tasks\specs\reports\20261117-p1b-l2-report.md`: таблица «строка реестра → было → стало → строка CI, на которой основано»
edges: (1) CI говорит `stopped at S<n>` с `n` ≠ 5 → строка `main/S5` удаляется, пишется `main/S<n>` с id, который Lead даёт под ЭТУ причину (не переносится чужой id; инвариант: недостижимое не прячется под чужой меткой, П1-б E15); причина, для которой у Lead id нет, — стоп, вопрос; (2) CI зелёный до S9 → строка `main/S5` удаляется, пин −1 (иначе `known_red` краснеет «stale», `known_red.py` `reconcile`); (3) пин `pins.known_red` = число строк после правки (равенство, `known_red.json:2`); (4) строка `s1.review/unavailable` — по F-P4: (а) метка находки ходока, (б) удаление строки обхода и строки реестра; (5) строка `kind:halt/free words` переименовывает только `node` и `raised_by` (id строки не меняется: id = строка обхода); (6) вывод CI нечитаем / задача `full` не дошла до файла (таймаут шарда) — стоп, вопрос координатору; угадывать место остановки по коду запрещено (FR-59); (7) реестр самопроверки ходока (`selftest/known_red.json:4`, `N4W-1`) остаётся, если `N4W-1` — id самопроверки, а не находка продукта (его `raised_by` так и говорит) — меняется только при F-P4 (а) с общим id
DoD: координатор повторяет канон на итоговой ветке; `python -B tools/ci_read.py why` по задаче `full` не называет `test_scenario_dry_1.py`; в выводе файла: `NOTE dry-1/main/known_red: known red: main/S<n> -> <id>` (или зелёный проход до S9) и ни одной `FAIL dry-1/…`; локально билдер L2 гоняет только `python -B ai-packages/qa-factory/scripts/tests/dry_exits.py --check` (`0 discrepancies`, проверка сирот реестра)
siblings: ось 18 (реестр меток — храповик помощника П1-а)

### N4R — реестр меток по файлу на группу (после L2; параллельно с N5 и N2h; до групп)

given: эта спека §4 N4R, F-P1; `T/known_red.py` (целиком, 152 стр.); `T/dry_exits.py` `check` (`:654-655`), `_ledger`, `_ledger_orphans` (`:768`), `--judge` (`:2588-2600`), `NOT_GROUP` (`:39`) — строки по `N4M`; `T/test_scenario_dry_1.py:130,138`; `T/dry_world.py:715` (`KNOWN_RED_FILE`)
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\dry_exits.py (функции `check`, `_ledger_orphans`, ветка `--judge`, константа пути реестров групп, строки `_selftest_cases`)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_scenario_dry_1.py (функция `main`: путь `--ledger` по умолчанию)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\driver-exits\known_red.json (остаются только строки `main/*`)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\driver-exits\known_red\s0.json (новый)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\driver-exits\known_red\s1-s4.json (новый)
C:\QAFactory\forge-repo\ai-packages\qa-factory\changelog.d\p1b-n4r-group-ledgers.md (новый)
non-goals: `known_red.py` (не меняется: `load(path)` уже берёт путь); `dry_world.py` (главный проход читает `main/*` из прежнего файла); строки обхода; форма строки реестра
handoff: отчёт билдера `C:\QAFactory\forge-repo\docs\tasks\specs\reports\20261117-p1b-n4r-report.md`
edges: (1) ВРЕМЕННОЙ: каталог `driver-exits/known_red/` создаёт этот узел; до него каждая группа читает общий файл; после — `exits:<g>` по умолчанию читает `driver-exits/known_red/<g>.json`; (2) файла группы нет → пустой реестр (пин 0): красная строка — FAIL «new red» (безопасная сторона), зелёная — PASS; инвариант: отсутствие файла никогда не делает красное ожидаемым; (3) `dry_exits.load` и `groups_found` (`test_scenario_dry_1.py:51`) читают `driver-exits/*.json` НЕрекурсивно — подкаталог не становится группой; билдер подтверждает чтением `load` и строкой таблицы «a subdirectory is no group»; если `load` рекурсивен — стоп, вопрос; (4) `_ledger_orphans`: строка в `known_red/<g>.json`, чей id не строка `exits/<g>.json` ТОЙ ЖЕ группы, — красное (строка чужой группы — сирота); строка `main/*` допустима только в общем файле; инвариант: ни одна метка не висит без строки, которая её может напечатать (N4w I8); (5) явный `--ledger` по-прежнему перекрывает путь по умолчанию (самопроверка ходока); (6) `--judge --dir D` судит общий файл `D/known_red.json` как сегодня — неизменно; (7) одинаковый id в двух файлах реестра — красное с обоими путями
DoD: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/tests/dry_exits.py ai-packages/qa-factory/scripts/tests/test_scenario_dry_1.py`; `python -B ai-packages/qa-factory/scripts/tests/dry_exits.py --selftest` — зелёный, с новыми строками таблицы для краёв (2), (3), (4), (7); `python -B ai-packages/qa-factory/scripts/tests/dry_exits.py --check` — `0 discrepancies`; части `exits:s0`, `exits:s1-s4` — CI (N5 или канон), исход: `known red:` по тем же id, что до узла
siblings: ось 18 (храповик меток — пин на файл), ось 34 (одна дорога: все группы — один путь по умолчанию)

### N5 — задача CI сухой стори (после L1; параллельно с N4R, N2h; РАНЬШЕ групп — F-P2)

given: эта спека §4 N5, F-P2, F-P3, F12; `C:\QAFactory\forge-repo\.github\workflows\canon.yml` (целиком); `C:\QAFactory\forge-repo\.github\workflows\nightly.yml:1-110`; `C:\QAFactory\forge-repo\tools\test_workflows.py:283-309,405-420,470-490`; `C:\QAFactory\forge-repo\docs\RUNBOOK.md` §7
owns:
C:\QAFactory\forge-repo\.github\workflows\nightly.yml (новая задача `dry-story`, по F-P3 (а))
C:\QAFactory\forge-repo\.github\workflows\canon.yml (удалить вход `spike` и задачу `dry-story-spike`, `run-name`)
C:\QAFactory\forge-repo\tools\test_workflows.py (строки, которые читают эти два файла)
non-goals: код пакета; `test_scenario_dry_1.py`; кап по замеру, если F12 не решён (тогда — §4 N5 п. 4); `forge-check.yml`
handoff: отчёт билдера `C:\QAFactory\forge-repo\docs\tasks\specs\reports\20261117-p1b-n5-report.md`
edges: (1) список частей — из файлов `PKG/scripts/tests/fixtures/stories/dry-1/exits/*.json`, найденных задачей-списком (шаг shell, имена — `basename .json`), матрица — `fromJSON` его вывода; группа без своего файла в матрицу не входит (её `unwalked` печатает режим по умолчанию задачи `full`); инвариант: группа с файлом никогда не выпадает молча — задача-список печатает перечень; (2) пустой перечень (`exits/` нет) → задача-список печатает «no walk groups» и матрица пуста; задачи частей не стартуют, задача зелёная только с этой строкой (до L1 это и есть мир `main`); (3) дополнительно, отдельным шагом одной задачи: `python -B ai-packages/qa-factory/scripts/tests/dry_exits.py --selftest` и `python -B ai-packages/qa-factory/scripts/tests/dry_stub.py --selftest` и часть самопроверки ходока (`--part exits:selftest --exits-root …/selftest --ledger …/selftest/known_red.json`) — по F-P6; (4) кап: `timeout-minutes` на часть = решение Lead по F12/E6; до решения — 30 (как спайк, `canon.yml:68`), строкой комментария «until the Lead's cap»; (5) строки `run:` не подставляют `${{ inputs.* }}`, `${{ github.event.* }}` (`tools/test_workflows.py:300-309`); значение матрицы — через `env:`; (6) `clock` канона: `needs` не меняется (`test_workflows.py:294`), если задача живёт в `nightly.yml` (вызов `full`); при F-P3 (б) — `needs` += `dry-story` тем же коммитом; (7) удаление `spike`: `run-name` становится `canon ${{ inputs.ref }}`, строка `test_workflows.py:289` меняется тем же коммитом; задачи `checks`/`full`/`clock` теряют `if: !inputs.spike`; (8) ВРЕМЕННОЙ: до L1 на `main` нет `exits/` — край (2); после L1 — части `s0`, `s1-s4`; после групп — пять; (9) задача по расписанию (`schedule`) идёт через `skip-if-unchanged` как соседи (`nightly.yml:57-68`)
DoD: `python -m pytest tools/test_workflows.py -q` — зелёный, с новыми строками: «canon has no spike input and no dry-story-spike job», «nightly has a dry-story job whose matrix comes from the list job», «no run string splices inputs»; координатор запускает канон на ветке узла и читает `python -B tools/ci_read.py jobs <run>` — задачи частей `dry-story (s0)`, `dry-story (s1-s4)` и шаг таблиц присутствуют (их красное по существу — не дефект N5, если оно то же, что у L2)
siblings: ось 34 (одна дорога: канон и ночь гоняют одну задачу), ось 18 (нет); `tools/test_workflows.py` — читатель (§6)

### N2h — заглушка критика S5 запускает пробу (после L1; параллельно с N4R, N5; до N4:s5, N4:s6-s9 — F-P7)

given: отчёт s5stub `N4M/docs/tasks/specs/reports/20261114-p1b-s5stub-report.md` (целиком); `T/dry_stub.py` ветки ролей (`ROLE_STEPS`, ветка автоматора `automator_branch`, ветка критика кода); `PKG/scripts/probe_by_code.py:1-40`; `PKG/scripts/brief_pack.py:239` (команда, которую получает критик); `PKG/references/handoffs/s5-critic-to-automator.yaml`; П1-б §4.2 (писатели выходов), N2 DoD (6) (команды — из профиля, не из брифа)
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\dry_stub.py (ветка критика кода S5 и строки `--selftest`)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\stories\dry-1\story.json (только строки заглушки `qa-code-critic@S5`, если нужен вердикт пробы)
C:\QAFactory\forge-repo\ai-packages\qa-factory\changelog.d\p1b-n2h-critic-probe.md (новый)
non-goals: контракт `s5-critic-to-automator.yaml` и пустой исход `probes.records` (продукт; находка L2 шага 1); `form_filler.py`; `probe_by_code.py`; метки реестра (L2/узел находки снимает свою `main/S5` тем же коммитом, если проход идёт дальше)
handoff: отчёт билдера `C:\QAFactory\forge-repo\docs\tasks\specs\reports\20261117-p1b-n2h-report.md`
edges: (1) заглушка запускает `probe_by_code.py` ПРОЦЕССОМ в мире, той же командой, что роль получает (`brief_pack.py:239`), с `STORY_RUN_CLASS=dry`; инвариант: вердикт пробы пишет настоящий инструмент, заглушка его не сочиняет (AR-29); (2) экземпляров окна нет → проба не запускается, форма идёт без записи — и это та же остановка, что сегодня (находка контракта); не PASS; (3) проба вернула ≠0 → строка журнала заглушки с `stderr` (обрезка 400) и форма без записи; не маскируется; (4) тест в мире падает/проходит — оба исхода законны: вердикт пробы — данные записи; (5) команда пробы берёт тест-команду из профиля мира (`profile_contract.profile_commands`), не из брифа; профиль без команды → журнал «no command», проба не запускается; (6) ПОЗИЦИОННЫЙ: запуск пробы стоит в ветке критика ДО заполнения формы (`fill_handover`): инвариант — заполнитель `world_list` видит записи, которые есть, и никогда не видит придуманных; (7) ВРЕМЕННОЙ: после узла главный проход может пройти S5 — метка `main/S5` станет «stale»; узел снимает её ТЕМ ЖЕ коммитом только по выводу CI на своей ветке (координатор), иначе пишет в отчёт «метку снимает следующий узел по CI»
DoD: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/tests/dry_stub.py`; `python -B ai-packages/qa-factory/scripts/tests/dry_stub.py --selftest` — зелёный с новыми строками: «critic S5 runs probe_by_code per instance; the record exists before the form», «no instance -> no probe, no record», «probe rc!=0 -> journal line, no record», «profile without commands -> 'no command'»; главный проход — CI (координатор): строка `dry-1/main/stop` называет стадию дальше S5 или новую причину S5 (в отчёт дословно)
siblings: ось 30 (команды профиля), ось 5 (двойник: автоматор уже зовёт `manifest_from_tests.py` процессом — тот же приём), ось 34

### N4:gates, N4:s5, N4:s6-s9 — строки обхода (параллельно; после L2, N4R; s5 и s6-s9 — после N2h по F-P7)

Общая карточка; `<g>` ∈ {`gates`, `s5`, `s6-s9`}; один диспатч на группу, owns не пересекаются.

given: N4w-спека §5.2 (пример), §6 (EW1-EW26), §8 (грамматика строки и рецепта); П1-б §3.3, §3.6, §4.3, §5 (E1-E22), §9.3 (вердикты FV1 своей группы); отчёты `…-n4g-s0-report.md` и `…-n4g-s1s4-report.md` (образец: исходы, `live_only` с причиной, что ходок не умеет); `T/fixtures/driver-exits/<g>.json`; `PKG/references/question-prices.json`, `stage-joints.json`, `conductor-actions.json`, `stages.json`; находки FV1 группы в `plans/piles/live-run-fvf/findings/`; `C:\QAFactory\forge-repo\ai-packages\qa-factory\design\factory-rules.md`; `C:\QAFactory\forge-repo\plans\builder-rules.md`
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\stories\dry-1\exits\<g>.json (новый)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\stories\dry-1\seeds\<g>.json (новый)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\driver-exits\<g>.json
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\driver-exits\known_red\<g>.json (новый; по F-P1 (а))
C:\QAFactory\forge-repo\docs\tasks\specs\reports\20261117-p1b-n4-<g>-report.md (новый)
non-goals: починка находок; `dry_world.py`/`dry_exits.py`/`dry_stub.py` (дефект ходока — строка отчёта и вопрос, не правка); `test_conductor_doors.py` (N4c); строки других групп; общий `known_red.json` (только `main/*`)
handoff: отчёт по образцу N4:s0/N4:s1-s4: таблица «id → start → reach → исход», строки, которым нужна метка (id → предложенная находка), `live_only` с причиной, вывод `dry_exits.py --check`
edges: (1) EW11 ВРЕМЕННОЙ: строки со `start` позже места остановки главного прохода печатают `after:<node>` по метке `main/S<n>` и сами исполнятся, когда проход пойдёт дальше; группа s5/s6-s9 до N2h — почти целиком `after:` (F-P7); (2) красная строка без метки — FAIL «new red»: метку (`known_red/<g>.json`) группа пишет только с id находки, который Lead выдал под ЭТУ причину (не чужой: П1-б E15); id нет — строка отчёта, узел сдаётся красным, Lead выдаёт id фикс-раундом; (3) строка, которую мир сухой стори не может поставить, — `reach: live_only` с причиной ИЗМЕРЕННОЙ (рецепт пробован) или с пометкой «estimate, not verified» (по образцу N4:s0 `:78`); рост `live_only` — каждой строкой `raised_by` (F-P8 о двойном счёте); (4) ключ цен без строк — не запись `driver-exits` (П1-б §3.2), `unwalked` его не считает; строки ключа нужны N4c — F-P9; (5) строки гейтов с вопросом владельцу Q1/Q2 — `expect.owner_question: "Q<n>"`, NOTE «owner question Q<n> open» (F-W12 (а)); (6) C4г только на субъекте класса `gate` (`classes.json`); иначе загрузчик отказывает до мира; (7) `gate_B` достижим только после S7 (порядок `PKG/references/stages.json:301-312`) — для группы gates сегодня `after:`; `gate_A` достижим (отчёт N2g `:38`); (8) группа gates: маршруты `driver-exits/gates.json:4-66` (15) и стыки `:67-92` (6), всё `unwalked`, база `:97` = 21 → итог `unwalked` группы 0, база в том же файле понижена; (9) время части — кап на часть (F12), одна строка дольше `ROW_CAP` — красное с id (E6)
DoD: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/tests/fixtures/stories/dry-1 ai-packages/qa-factory/scripts/tests/fixtures/driver-exits` (называет `test_scenario_dry_1.py`); локально: `python -B ai-packages/qa-factory/scripts/tests/dry_exits.py --check` — `0 discrepancies` (база `unwalked` группы понижена до 0); часть `test_scenario_dry_1.py --part exits:<g>` — CI задачи `dry-story` (N5) на ветке группы (запускает и читает координатор): `PASS dry-1/exits:<g>/outcomes`, NOTE `unwalked: 0`, FAIL — только строки из списка «нужна метка» отчёта
siblings: ось 5 (двойники стадий: id одного состояния под двумя субъектами — как `kind:s1_review`/`s1.review`, отчёт N4:s1-s4 `:75`), ось 34

Своё у групп (дополнение к общей карточке):
- **gates**: субъекты — маршруты и стыки `gates.json`; C6 на каждом вопросе `gate_A` в строке; строки FV1-7 (I-gate) и FV1-8
  (П1-б §9.3) — `gate_A` × `approve` после `questions` × `go on`: ожидаемо красные, метка — id FV1-7/FV1-8 (находки есть,
  `live-run-fvf/1` `:40-41`).
- **s5**: `s5.repair_limit`, `s5.nobody_*`, `exit.resume_limit*`, `s6.walk_*`, `s6.data_change`, `code_close.*` (П1-б `:636`);
  строка C10 `s5.window_finish/ref_without_hash` (FV1-19) — `pending judge C10` (N4w F-W13), не PASS.
- **s6-s9**: `s6.stand_*`, `s7.*`, `s8.*`, `closed.held`; FV1-22 — S7-петля (`after:` до прохода S5).

### N4c — перепись ключей вопросов: строки сухой стори входят в `driven` (после всех N4 — П1-б §6, без изменений)

given: П1-б §6 N4c (`:638-651`); `T/dry_exits.py` `driven_keys` (N4w-спека §2: `:764-775` по дереву n3); `T/test_conductor_doors.py:626-679,794-810`; `T/test-layers.json:672` (keep `test_conductor_doors.py`)
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_conductor_doors.py
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test-layers.json (только `covers` строки `test_conductor_doors.py`)
non-goals: смысл и сигнатура `census_problems`; строки обхода
handoff: отчёт билдера `C:\QAFactory\forge-repo\docs\tasks\specs\reports\20261117-p1b-n4c-report.md`
edges: П1-б E17, E20; (1) `driven_keys()` пуст (ни у одного ключа нет всех ответов строками `story`/`seed`, F13 (а)) → `PINNED_ELSEWHERE` не меняется, отчёт печатает пустое множество; это не PASS «сжатия», а NOTE (инвариант: перепись не теряет закрепление непройденного ключа); (2) ключ в `driven` И в `PINNED_ELSEWHERE` → существующий отказ «listed as pinned elsewhere, but driven here» (`:679`) — запись удаляется; (3) очередь `test-layers.json` (П1-б §8 `:741-746`): PC4-15 → FG7-15 → FG7-19 → П1-а → П1-б N3 (=L1) → N4c; на 17.11 все впереди стоящие «ожидает» (§2) — N4c берёт строку `covers` по D-0048 (непересекающиеся строки) без ожидания, если Lead так решит (F-P10)
DoD: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/tests/test_conductor_doors.py`; `test_conductor_doors.py` — CI (53.0 с): зелёный, в выводе K15 `driven` содержит ключи сухой стори; список удалённых из `PINNED_ELSEWHERE` = `dry_exits.driven_keys()` (в отчёте)
siblings: ось 18 (храповик «pinned elsewhere» сжимается)

### Поздние узлы и чего каждый ждёт

- **N6** (П1-б `:659-661`): вторая строка раннеров `stories/dry-1/runners/ts-playwright/` + Node и браузер в образе задачи
  `dry-story` (по F-P3 — `nightly.yml`, не `canon.yml`). Ждёт: N5 (задача есть), N4:s5 (строка C10 на обеих строках
  раннеров), N2h (без S5 строки `after:`). Owns: `T/fixtures/stories/dry-1/runners/ts-playwright/` (новый),
  `.github/workflows/nightly.yml` (только шаги образа задачи `dry-story`), `tools/test_workflows.py` (строки этой задачи).
  Пересечение с N5 по `nightly.yml` и `test_workflows.py` — последовательно N5 → N6. Свидетель — часть `exits:s5` CI.
- **N3t** (A1 `:161-177`): ОДИН узел на типы сверх `default`. Ждёт: L1. Расхождение имён — F-P11: поправка называет
  `test_scenario_dry.py` и `stories/dry-<default>/`, построено `test_scenario_dry_1.py` и `stories/dry-1/` с
  `DEFAULT_STORY = "dry-1"` при `dry-types.json` `default: codemie-14857` (отчёт N3 Q5). Owns по F-P11 (а):
  `T/fixtures/stories/dry-<type>/` (новые), `T/fixtures/stories/dry-types.json`, `T/test_scenario_dry_1.py` (функция
  `main`, ветка `main:<type>`), строка `covers` `keep` `test_scenario_dry_1.py` — `test-layers.json` в очереди с N4c
  (последовательно N4c → N3t или по D-0048).
- **N3a** (A2 `:231-245`): «сказано до работы». Ждёт: L1 и П1-в N0 (ключ `checks` в `driver-runs.jsonl`). Owns
  (переименование по F-P11): `T/dry_exits.py` (функция `told_before_work` только), `T/test_scenario_dry_1.py` (функция
  `_print_told` и строка её вызова). Пересечение: FV2-13 (`live-run-fvf/2` `:40`) пишет `dry_exits.py` — по D-0048
  функции не пересекаются (`_read_json`/`author_input_sha` против `told_before_work`), строка `очередь:` не нужна, если Lead
  принимает список функций; N4R тоже пишет `dry_exits.py` (`check`, `_ledger_orphans`) — N4R раньше N3a по порядку.
- **N-L** (узел Lead, не диспатч билдеру этой спеки): R-L1…R-L9 П1-б `:663-677` + R-L10 A2 `:246`. Ждёт: L1 (носители
  называют файлы, которых до L1 на main нет). R-L3 (`architecture.md:192`), R-L5 (находка C4г) — до N4:gates.

---

## 5. Параллельность и общие файлы

| Шаг | Узлы | Общие файлы и как разведены |
|---|---|---|
| 1 | L1 | один писатель всех файлов ветки |
| 2 | L2 | та же ветка, последовательно; волна L1+L2 в `main` одна |
| 3 | N4R ∥ N5 ∥ N2h | `dry_exits.py`+`test_scenario_dry_1.py` (N4R) / workflows+`tools/test_workflows.py` (N5) / `dry_stub.py`+`story.json` (N2h) — не пересекаются |
| 4 | N4:gates ∥ N4:s5 ∥ N4:s6-s9 | файл на группу в четырёх каталогах (`exits/`, `seeds/`, `driver-exits/`, `driver-exits/known_red/`); общий `known_red.json` не пишет никто (F-P1 (а)) |
| 5 | N4c | `test_conductor_doors.py`, `test-layers.json` |
| 6 | N6, N3t, N3a | N6 после N5; N3t после N4c по `test-layers.json`; N3a после N4R по `dry_exits.py` |

Писателей одновременно: шаг 3 — 3, шаг 4 — 3 (кап 6, CLAUDE.md правило 12). Критик кода — один на тему (R13-g) после шага 4
(плюс L1+L2 по правилу 3: дифф > 100 строк — критик перед волной; F-P12).

---

## 6. Читатели каждого затронутого файла (роль дизайнера правило 7)

Команды (Grep tool, путь, режим count):
- `dry_exits|dry_world|dry_stub|dry_driver|test_scenario_dry|known_red|driver-exits|stories/dry` по `tools/` — 0; по
  `.githooks/` — 0; по `.claude/settings.json` — 0. Положительные контроли той же формы: `test-layers\.json|canon\.yml|slow_tests\.json|scenario_walk|test_conductor_doors|nightly\.yml|TEST_TIMEOUTS`
  по `tools/` — 136 вхождений в 20 файлах; `piles\.py|architecture_gate` по `.githooks/` — 2 (`commit-msg`).
- Широкий набор по `.claude/agents/` — 3 (`builder.md` 1, `designer.md` 2: упоминания `test-layers.json` в тексте правил) —
  неизменны. `.claude/worktrees/` исключён (деревья других сессий).

| Файл | Читатель (tools/.githooks/.claude) | Вердикт |
|---|---|---|
| `.github/workflows/canon.yml` | `tools/test_workflows.py:29,288-297,410-416,476-490` (пин `run-name` со `spike` `:289`, `clock.if`/`needs` `:294`, F19E `:300-309`) | меняется в N5 |
| то же | `tools/ci_read.py:69` (`WORKFLOW = "canon.yml"`, `start`) | неизменен |
| `.github/workflows/nightly.yml` | `tools/test_workflows.py` (`NAMES :29`, задачи nightly) | меняется в N5 (и N6) |
| `T/test-layers.json` | `tools/test_quarantine.py` (27), `tools/lint_ratchet.py:11,70`, `tools/owns_readers.json:6`, `tools/owns_readers.py`, `tools/source-split-carriers.json`, `tools/test_redundancy.py`, `tools/story_capture.py` | неизменны (L1 добавляет строку `keep` — читатели её видят как любую; N4c/N3t правят только `covers`) |
| `PKG/scripts/slow_tests.json` | `tools/owns_readers.json:7` | неизменен |
| `T/scenario_walk.py` | `tools/story_capture.py`, `tools/install_parity_anchors.json` (по 6/1 вхождений общего набора; что именно — не прочитано) | неизменны (L1 добавляет дверь `driver`, имена функций не меняются) |
| `T/test_conductor_doors.py` | в `tools/` вхождения общего набора — не разобраны по файлу | N4c: неизменны (имя файла не меняется) |
| `T/dry_*.py`, `T/test_scenario_dry_1.py`, `T/fixtures/driver-exits/**`, `T/fixtures/stories/dry-1/**` | нет (0, с контролем) | — |
| `tools/test_workflows.py` | сам тест; `.githooks/` — 0 | меняется в N5 |

Читатели внутри пакета (для краёв, не по правилу 7): `driver-exits/known_red.json` — `T/dry_exits.py:654-655,2600`,
`T/dry_world.py:715` (`KNOWN_RED_FILE`), `T/test_scenario_dry_1.py:130,138`; `known_red.py` — `T/dry_exits.py:707,754`,
`T/test_field_producers.py:32,189` (реестр П1-а `form-rounds.json`, не этот файл — N4R его не трогает).

---

## 7. Развилки (решает Lead; OWNER — вопрос владельцу)

**F10 (П1-б §9).** Как ходок узнаёт ключ цен. (а) обёртка `dry_driver.py` со шпионом на `no_move.priced_options`; (б) сопоставление
по множеству ответов; (в) драйвер пишет ключ сам. Факт: (а) построено (`dry_driver.py`, 82 стр.; N3 перевёл `drive` на неё,
отчёт N3 `:72`). Рекомендация: (а) — уже на ветке, L1 её сажает; (в) — находкой для П1-в, если понадобится в живом прогоне.
Направление ошибки (б): неверный ключ у одинаковых наборов (`s5.nobody_*`, `s8.delivery.*`) — запрещённая сторона.

**F11 (П1-б §9).** Где живёт проверка «у запрета без прохода названа дверь». (а) `dry_exits.ban_doors()` (тестовый слой);
(б) строка `refusal_registry.audit`. Рекомендация: (б), до решения (а) временным читателем с пометкой «перенести»; узел (б) —
отдельный, owns `PKG/scripts/refusal_registry.py` + строка его теста, вне этой спеки.

**F12 (П1-б §9).** Числа ворот N0 / кап задачи. Рекомендация дизайнера П1-б — две цифры (S0→S3 ≤ 120 с, медиана строки ≤ 20 с).
Измерено после N0 (ветка): главный проход 381-385 с до S5 (N2g `:43`, s5stub `:40`, S3 98.8 с, S4 74.0 с), части 110-343 с.
Для N5 нужен кап на часть: рекомендация — 30 мин на часть до решения (как спайк), затем число Lead.

**F13 (П1-б §9).** `driven` «целиком» (а) или «хотя бы одна строка» (б). Рекомендация: (а) (E20). Следствие сегодня: ни одна
группа не писала строк ключей цен (отчёты s0 `:82,88`, s1-s4 `:64-65`) — `driven_keys()` может оказаться пустым, N4c тогда
ничего не сжимает (N4c край 1); см. F-P9.

**F-P1. Реестр меток для параллельных групп.** (а) файл на группу `driver-exits/known_red/<g>.json`, узел N4R до групп
(цена: малая правка `dry_exits.py`/`test_scenario_dry_1.py`, `known_red.py` не меняется; ошибка в безопасную сторону —
отсутствующий файл = пустой реестр); (б) один писатель: группы пишут метки во временный `--ledger`, один узел после всех
групп переносит их в общий файл (цена: свидетель группы опирается на незакоммиченный файл; между слиянием группы и
переносом часть красная в N5); (в) все пишут общий файл, конфликт пина решает волна слияния (цена: гарантированный
конфликт `pins.known_red` на каждой паре). Рекомендация: (а). П1-б §10 (`:857-859`) сам допускал «файл на группу».

**F-P2. Где судятся части `exits:<g>`.** (а) N5 раньше групп; части судит CI на ветке группы (координатор запускает);
(б) билдер гоняет свою часть локально один раз (110-385 с) — против builder-rules 7b «до минуты» (слово владельца 21.10 и
14.11) — **OWNER**: «Можно ли билдеру сухой стори один раз прогнать свою часть на своей машине (2-6 минут), или всё только
через CI?»; (в) N5 последним, как П1-б §6 — группы сдаются без прогона своей части. Рекомендация: (а).

**F-P3. Где живёт задача `dry-story`.** (а) `nightly.yml` (её вызывает и ночь на `main`, и канон через `full`) — «идёт в CI на
main» каждую ночь; (б) `canon.yml` (только ручной канон, как П1-б N5). Рекомендация: (а) — одна задача, два вызова (AR-15);
цена: ночное время +кап частей.

**F-P4. Строка `s1.review/unavailable`.** Отчёт s1-s4 `:55`: ответ `unavailable` предлагается условно, у ходока нет условия;
самопроверка ходока держит тот же случай под `N4W-1`. (а) находка ходока «условно предложенный ответ» + метка; (б) убрать
строку (вариант не предлагается в этом мире — не вариант строки); (в) условие в грамматике (правка ходока). Рекомендация: (б)
сейчас + находка на (в): строка, которую мир не может предложить, не должна быть «ожидаемо красной» (метка скрывала бы
неисполнимость). Ошибка (а) — красное по миру, а не по дефекту `main`.

**F-P5. Числа расписания после слияния** (`slow_tests.json` 51.0 и `TEST_TIMEOUTS` 900 при замере 381-385 с; FG7-38 `forge/7`
`:61`). (а) L2 пишет число по замеру CI в ту же волну и отмечает FG7-38 сделанным (один писатель); (б) FG7-38 остаётся своим
узлом после волны. Рекомендация: (а) — FG7-38 сам зависит от этого слияния; потолок 900 не растёт.

**F-P6. Чистые таблицы `dry_exits.py --selftest` (154) и `dry_stub.py --selftest` (189) не гоняет ни одна задача CI** (не
`test_*`, selftest их не зовёт; грep по `N4M/PKG/scripts` — только сами файлы). (а) шаг задачи `dry-story` (N5 край 3);
(б) вызов из режима по умолчанию `test_scenario_dry_1.py` (задача `full`; цена: правка файла узлом N4R/L1); (в) не гонять.
Рекомендация: (а).

**F-P7. Строки s5/s6-s9 до N2h.** (а) N2h до групп s5, s6-s9 (рецепты и варианты проверяются на настоящем мире);
(б) писать строки сейчас, все `after:` (исполнятся сами, но написаны вслепую). Рекомендация: (а); gates идёт сразу.

**F-P8. Двойной счёт `live_only`** (строка переписи и её строка обхода считаются дважды, `_count_reach`; отчёт s0 Q1).
(а) оставить (две записи `raised_by` на субъект); (б) строка обхода с `reach: live_only` при такой же строке переписи не
считается (правка `dry_exits._count_reach`, свой узел). Рекомендация: (б) отдельным узлом после групп; группы пишут по (а).

**F-P9. Строки ключей цен (`<key>/<answer>`)** нужны N4c, ни одна группа их не писала (s0 Q3). (а) каждая группа пишет строки
своих ключей (`live_only` для недостижимых ответов) — N4c сжимает только полностью исполненные (F13 (а)); (б) ключи — только
существующая перепись, N4c откладывается. Рекомендация: (а) для групп шага 4; s0 и s1-s4 — фикс-раундом их строк после
L1 (новые узлы `N4:s0+`, `N4:s1-s4+`, owns — их файлы обхода).

**F-P10. Очередь `test-layers.json`.** (а) по D-0048 — N4c и L1 пишут разные строки `keep`, очереди нет; (б) очередь П1-б §8.
Рекомендация: (а) (все впереди стоящие — «ожидает», §2).

**F-P11. Имена в поправке A1/A2** (`test_scenario_dry.py`, `stories/dry-<default>/`) против построенного
(`test_scenario_dry_1.py`, `stories/dry-1/`, `DEFAULT_STORY = "dry-1"`, `dry-types.json` `default: codemie-14857`).
(а) поправка читается в построенных именах (`dry-1` = история слоя; тип `default` таблицы = `codemie-14857` — отдельная
история `dry-codemie-14857`); (б) переименовать файл и каталог (правка канона, `keep`, всех ссылок). Рекомендация: (а) —
переименование ничего не даёт; два смысла `default` развести строкой в `dry-types.json` (`_about`) узлом N3t.

**F-P12. Критик перед волной L1+L2.** Дифф ветки — тысячи строк, весь уже прошёл критиков узлов? (Критик темы П1-б «N3 + N4w
+ группы перед слиянием» — долг Lead, снимок `2026-11-14-0800` `:35`.) (а) один критик темы П1-б на дифф `origin/main...` ветки
до волны; (б) волна по witness, критик темы после групп. Рекомендация: (а) — правило 3 (дифф > 100 строк) и снимок прямо
называют этот долг.

**F-P13. Кучка для строк.** (а) `live-run-fvf`, новая пачка 3 П1 (кучка П1, фича F19, тема — слой, ловящий находки
прогона; пачка 2 — П2 и 78 узлов: нужно слово Lead «пачка 2 полна», правило «Командная работа» п. 2); (б) `forge`, пачка 8
(пачка 7 П2, «ожидает», 30+ узлов); (в) новая кучка `dry-story`. Рекомендация: (а).

Вопросы владельцу (OWNER) простыми словами: только F-P2 (б). Остальное — решения Lead. Q1/Q2 П1-б §9.2 остаются открытыми
(строки гейтов печатают NOTE до ответа).

---

## 8. Мелкие решения дизайнера

- Посадка — слиянием ветки в новую ветку пачки от `origin/main`, не перебазированием (истории узлов и отчёты сохраняются).
- L1 и L2 — одна ветка и одна волна: устаревшая метка не попадает на `main` ни на один коммит.
- Подкаталог `driver-exits/known_red/` (а не `known_red.<g>.json` рядом): файлы рядом читались бы как группы
  (`NOT_GROUP`, `dry_exits.py:39`).
- Список групп для матрицы — из `exits/*.json`, не из `groups_found` (тот добавляет группы переписи без файла обхода → FAIL EW1).
- Имена отчётов узлов: `docs/tasks/specs/reports/20261117-p1b-<узел>-report.md`.

---

## 9. Строки кучки (рекомендация F-P13 (а): `plans/piles/live-run-fvf/batch-3-…`, приоритет П1)

Шапка: `кучка: live-run-fvf | статус: ожидает | взял: — | ветка: — | MR: — | стенд: не нужен | приоритет: П1`.
Строки таблицы узлов (колонки как `batch-2-live-run-fvf.md:26`):

| Узел | Приоритет | Что | Исполнитель | Пишет в | Зависит от | Статус |
|---|---|---|---|---|---|---|
| FV3-1 | П1 | Посадка сухой стори: ветка `wip/p1b-n4m` (N2, N3, N4w+фикс, N4:s0, N4:s1-s4, заглушка S5) сливается в `main`; канон и ночь начинают гонять `test_scenario_dry_1.py` (спека `docs/tasks/specs/20261117-p1b-finish-spec.md` §4 L1) | builder → critic | `scripts/tests/dry_*.py`, `scripts/tests/test_scenario_dry_1.py`, `scripts/tests/scenario_walk.py`, `scripts/tests/form_filler.py`, `scripts/tests/fixtures/{driver-exits,stories/dry-1,form-fill-rules.json}`, `scripts/tests/test-layers.json` (строка keep), `scripts/selftest.py`, `scripts/slow_tests.json` | — | ожидает |
| FV3-2 | П1 | Метки реестра истинны на слиянии: `main/S5 -> P1B-9` заменяется находкой измеренной остановки; `N4S0-1`, `N4S14-1` — находками с файлом (§4 L2; F-P4, F-P5) | Lead (находки) → builder | `scripts/tests/fixtures/driver-exits/known_red.json`, `…/stories/dry-1/selftest/known_red.json` | FV3-1 | ожидает |
| FV3-3 | П1 | Реестр меток по файлу на группу, чтобы параллельные группы не делили пин (§4 N4R; F-P1) | builder → critic | `scripts/tests/dry_exits.py` (`check`, `_ledger_orphans`), `scripts/tests/test_scenario_dry_1.py` (`main`), `scripts/tests/fixtures/driver-exits/known_red*` | FV3-2 | ожидает |
| FV3-4 | П1 | Задача CI `dry-story` (части по файлам обхода, таблицы `--selftest`), спайк удалён (§4 N5; F-P2, F-P3, F-P6) | builder → critic | `.github/workflows/nightly.yml`, `.github/workflows/canon.yml`, `tools/test_workflows.py` | FV3-1 | ожидает |
| FV3-5 | П1 | Заглушка критика кода S5 запускает `probe_by_code.py` (§4 N2h; F-P7) | builder → critic | `scripts/tests/dry_stub.py`, `scripts/tests/fixtures/stories/dry-1/story.json` | FV3-2 | ожидает |
| FV3-6 | П1 | Строки обхода группы `gates` (§4 N4) | builder | `scripts/tests/fixtures/stories/dry-1/{exits,seeds}/gates.json`, `scripts/tests/fixtures/driver-exits/gates.json`, `…/driver-exits/known_red/gates.json` | FV3-3, FV3-4 | ожидает |
| FV3-7 | П1 | Строки обхода группы `s5` (§4 N4) | builder | то же для `s5` | FV3-3, FV3-4, FV3-5 | ожидает |
| FV3-8 | П1 | Строки обхода группы `s6-s9` (§4 N4) | builder | то же для `s6-s9` | FV3-3, FV3-4, FV3-5 | ожидает |
| FV3-9 | П1 | Строки ключей цен групп `s0`, `s1-s4` (F-P9) | builder | `…/stories/dry-1/exits/{s0,s1-s4}.json` | FV3-3 | ожидает |
| FV3-10 | П1 | Перепись ключей вопросов: ключи сухой стори в `driven`, `PINNED_ELSEWHERE` сжимается (§4 N4c) | builder → critic | `scripts/tests/test_conductor_doors.py`, `scripts/tests/test-layers.json` (covers) | FV3-6…FV3-9 | ожидает |
| FV3-11 | П2 | Вторая строка раннеров TS/Playwright (§4 N6) | builder → critic | `…/stories/dry-1/runners/ts-playwright/`, `.github/workflows/nightly.yml`, `tools/test_workflows.py` | FV3-4, FV3-7 | ожидает |
| FV3-12 | П2 | Типы сверх `default` (§4 N3t; A1; F-P11) | designer → builder | `…/stories/dry-<type>/`, `…/stories/dry-types.json`, `scripts/tests/test_scenario_dry_1.py` (`main`) | FV3-1, FV3-10 | ожидает |
| FV3-13 | П2 | «Сказано до работы» в сухой истории (§4 N3a; A2) | builder → critic | `scripts/tests/dry_exits.py` (`told_before_work`), `scripts/tests/test_scenario_dry_1.py` (`_print_told`) | FV3-3, П1-в N0 | ожидает |
| FV3-14 | П2 | Двойной счёт `live_only` (F-P8 (б)) | builder | `scripts/tests/dry_exits.py` (`_count_reach`) | FV3-6…FV3-8 | ожидает |

Строка «Пачки» карточки `live-run-fvf/README.md`: `| 3 | сухая стори идёт в CI на main: посадка ветки, метки, задача CI, обход всех групп, перепись ключей | FV3-1…FV3-14 | L | ожидает | — | — | — |`.
Строка `очередь:` для `forge/7`: `очередь: live-run-fvf/3 FV3-1 → forge/7 FG7-38` (если F-P5 (б)) и для
`scenario_walk.py`/`test-layers.json`: `очередь: live-run-fvf/3 FV3-1 → forge/7 FG7-15 → forge/7 FG7-19` (L1 уже несёт
правку `scenario_walk.py`; П1-б §8 ставил FG7-15/19 раньше — но они не начаты, а ветка готова; решает Lead вместе с F-P10).
Узел N-L — строкой Lead, не билдера.

---

## 10. След чтения

| Что | Где | Результат |
|---|---|---|
| Бриф-носители | П1-б `:480-760` (E1-E22, §6 узлы, §8 очередь), `:760-959` (F1-F13, §9.2, §9.3, §10, §10a, §11, §12); `:1-95` (шапка, §1) | F10-F13 без решения Lead (§10a перечисляет F1-F9) |
| N4w-спека | `:1-287`, `:303-412` (DoD, грамматика §8, §9 карточки групп, §10); заголовки `:411-645` | F-W1…F-W18 |
| Поправка | `20261113-p1-specs-amendment-owner-words.md:156-255` | N3t/N3a, A1-E*, A2-E*; имена `test_scenario_dry.py` |
| Снимок | `docs/tasks/compact-snapshots/2026-11-14-0800-narrative.md:1-48` | `main/S5 -> P1B-9` устарела; следующий узел — проба на S5 |
| Рефы git | `.git/refs/heads/main`, `.git/refs/remotes/origin/main` (оба `cfe418b6`); `.git/worktrees/{p1b-n4m,p1b-n4-gates,p1b-n4w,p1b-n3}/HEAD` | ветки по именам; `refs/heads/wip/p1b-n4m` — файла нет (упаковано) |
| Деревья | Glob `**/*` в `N4M/T/fixtures/{stories/dry-1,driver-exits}`, в `MAIN/T/fixtures/{driver-exits,dry-walk}`; Glob `**/*dry*` в `T` обоих; Glob `**/{dry_*.py,test_scenario_dry_1.py,known_red.py}` в трёх деревьях | §2. Промахи вызова: Glob с шаблоном, начинающимся с имени каталога (`p1b-*/…`, `*/BOOT.md`), не находил заведомо существующее — отвергнуты как промах, не как отсутствие |
| Счёт строк | Grep `^` count по `T` main и N4M (glob набора файлов) | таблицы §2, §3 |
| Отчёты ветки | `N4M/docs/tasks/specs/reports/20261114-p1b-{n3,n2g(:1-75),n4wfix,n4g-s0,n4g-s1s4,s5stub}-report.md` | §2, §4 |
| Метки | `N4M/T/fixtures/driver-exits/known_red.json`, `MAIN/…/known_red.json`, `N4M/…/stories/dry-1/selftest/known_red.json`; Grep `N4S0-1|N4S14-1|N4W-1` вне `.claude/` (4 файла: журнал, снимки) и в N4M (6) | находок с этими id нет |
| Тест истории | `N4M/T/test_scenario_dry_1.py:1-156` | режимы, `--ledger` по умолчанию |
| Ходок/реестр | Grep `def exits_part|def walk_exits|def judge_group` в `p1b-n4-gates` (0), `N4M` (3), `p1b-n4w` (3); Grep `isolation: a real-looking walk file` (1, N4M); Grep `known_red\.json|LEDGER|_ledger_orphans|NOT_GROUP` в N4M `*.py` | §2, N4R |
| Расписание | `MAIN` и `N4M` `PKG/scripts/selftest.py:100-124`; Grep `test_scenario_dry` в `MAIN/PKG/scripts` (0; контроль `test_scenario_cart|test_scenario_local` — 12) и в N4M (`slow_tests.json:119`, `selftest.py:117`, `test-layers.json:5109`) | §2, §3 |
| Дверь | Grep `^DOORS|DOOR_MODULES|"driver"` в обоих `scenario_walk.py` | `:40`, `:48` |
| Заполнитель | Grep `def world_list|world_list_tokens` в N4M (есть) и MAIN (0; контроль `class FillContext|task_root` — 4) | §2 |
| CI | `.github/workflows/canon.yml` целиком; Grep триггеров `nightly.yml`, `forge-check.yml`; `tools/test_workflows.py:280-309`; Grep `canon.yml|dry|spike` `tools/ci_read.py` | N5, §6 |
| Перепись ключей | Grep `PINNED_ELSEWHERE|census_problems|driven` `T/test_conductor_doors.py`; Grep `"test_conductor_doors.py"` в `PKG/scripts` | `:636`, `:670`; `test-layers.json:672,7146` (keep_fail_at_entry) |
| `test-layers.json` | `MAIN :1-34`, `:7130-7154`; `N4M :5105-5135`; Grep `fixture_owners` в `selftest.py` | keep, `enforce_listing`, `fixture_owners` |
| Перепись gates | `N4M/T/fixtures/driver-exits/gates.json` целиком | 15 маршрутов, 6 стыков, база 21 |
| Стадии | Grep `gate_B|gate_A|"gate"` `PKG/references/stages.json`; `:285-319` | гейт B — приказы S7/S8 |
| null_outcomes | Grep `def null_outcome|null_outcome_entries|probes\.records` в `MAIN/PKG/scripts` | `handoff.py:472,515`, `null_outcomes.py:113` |
| Пачки | `forge/batch-7…:1-20`; Grep FG7-15/19/38 в `plans/piles/forge`; статусы `batch-7` (Grep хвоста строк); `live-run-fvf/batch-2:1-40`, Grep `P1B|П1-б|p1b|сух`; `batch-1` строки FV1-1,6,7,8,13,19,22; `live-run-fvf/README.md:1-40`; `package-ci/batch-4:1-6`; Grep `P1B-|П1-б|p1b` count по `plans/piles` | §2, §9 |
| Правила | `docs/TESTING.md:36-135`; Grep `7b` `plans/builder-rules.md` (+12 строк) | §4 «Свидетель» |
| Читатели (правило 7) | §6 — команды и счёт | §6 |
| AR-17 R-L3 | Grep `NO_MOVE_BASELINE_MAX` `PKG/design/architecture.md` | строка `:192` есть (текст длинный, значение не прочитано) |
| Память машины | `memory/stale-local-main-checkout.md` | корень отставал 13.11; 17.11 `main` = `origin/main` по рефам |

Нужно сверх манифеста (прочитано): `.git/refs/*`, `.git/worktrees/*/HEAD`, `tools/test_workflows.py`, `tools/ci_read.py`,
`tools/owns_readers.json`, `tools/lint_ratchet.py`, `plans/piles/**` (статусы), `PKG/references/stages.json`, отчёты ветки
`N4M/docs/tasks/specs/reports/*`, `PKG/scripts/handoff.py` (Grep), `nightly.yml`, `forge-check.yml`.

---

## 11. Не сделано / не установлено

- Хэши веток и точка ветвления; какие файлы `main` менял после неё; есть ли в ветке строки журнала — команды §3 (Lead до L1).
- Незакоммиченное в дереве `p1b-n4-gates` — `git -C C:\QAFactory\forge-repo\.claude\worktrees\p1b-n4-gates status --short`.
- Полный список деревьев `p1b-*` — `git -C C:\QAFactory\forge-repo worktree list` (мой Glob по шаблону каталога — промах вызова).
- Место остановки главного прохода на `main` после слияния — меряет CI (L2 шаг 2); прогноз «S5, запись пробы» — оценка по
  отчёту s5stub, не проверено.
- Покрывает ли `null_outcomes.py` (`main`) вложенный `probes.records` — не прочитано (N2h/находка L2).
- Каталог `fixtures/stories/dry-codemie-14857/` — не искал.
- R-L1 (строки `SIBLING_MAP`), значение `architecture.md:192` (102) — по дайджесту t-941, мной не перечитано.
- Рекурсивен ли `dry_exits.load` по `driver-exits/` — не прочитано (N4R край 3 требует от билдера проверить).
- Что именно читают `tools/story_capture.py`, `tools/install_parity_anchors.json`, `tools/source-split-carriers.json` в
  `scenario_walk.py`/`test-layers.json` — счёт есть, строки не разобраны (вердикт «неизменны»: имена функций и формат не
  меняются).
- Время `dry_stub.py --selftest`, `test_field_producers.py` на итоговом дереве — не измерено (L1 DoD печатает секунды).
- Оси SIBLING_MAP в узлах перечислены выборочно (оси групп — как П1-б §7(b)); полный перечень по 36 осям на каждый механизм
  (правило 10 (b)) пишет коммит узла — не эта спека.

---

## Решения Lead по развилкам (17.11.2026, Fable)

F-P1 … F-P13 — берутся рекомендованные варианты (а), как записаны в §7; порядок §0 стоит: L1 → L2 → {N5, N4R, N2h} →
{N4:gates, N4:s5, N4:s6-s9} → N4c → поздние узлы. F-P2: части `exits:<g>` локально не гоняются (builder-rules 7b), их
судит CI — вопроса владельцу нет, это действующее правило. F-P12: критик на план этой спеки — до L1 (t-955); критик
кода — один на тему после волны групп. Команды git из §3 перед L1 выполняет Lead заново (main ушёл вперёд от `cfe418b6`).
