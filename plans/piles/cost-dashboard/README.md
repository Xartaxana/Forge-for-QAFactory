# Деньги, телеметрия, дашборд (`cost-dashboard`)

приоритет: П3 | фичи: F14 | стенд: не нужен (эталонные прогоны) | зона: `ai-packages/qa-factory/scripts/cost_capture.py`, `scripts/retro_numbers.py`, `scripts/factory_dashboard.py`, `scripts/judge.py`, `tools/usage_report.py`, `references/model-rates.json`, `experiments/measurers/context_shape.py`, `experiments/measurers/conductor_families.py`, `experiments/measurers/report_run.py`, `experiments/measurers/compare.py`

## Зачем

Сегодня цена задачи складывается из нескольких источников, которые местами расходятся: сессии драйвера сворачиваются
в строку «(no task)», хвост сессии может не попасть в учёт, у новых моделей нет цены в одной из таблиц, а строка без
стоимости превращается в «$0» как факт. Дашборд не раскрывает задачу по агентам и стадиям, а ретро не делит цену
доработки по причинам. После первой пачки цена задачи одна и истинная (P18), никакой «$0 как факт», дашборд показывает
задачу по стадиям и агентам, а ретро делит цену доработки по причинам.

## Что не так сегодня (факты)

- `cost_capture.collapse_requests` сворачивает сессии драйвера в одну строку «(no task)»: на cmp1 так 35 файлов из 35 (`plans/BACKLOG.md:182`).
- `recapture_session` всегда ставит `usage_complete: True`, импорт Codex из «предварительно» становится «полно» без нового свидетельства (`plans/BACKLOG.md:417`); хвост сессии, записанный в ту же секунду, пропускается (`plans/BACKLOG.md:416`).
- Таблица цен `tools/usage_report.py` расходится с `references/model-rates.json`: нет `claude-fable-5-1` и `claude-sonnet-5-5` (`plans/BACKLOG.md:140`; дайджест `docs/tasks/specs/reports/t-713-scout-piles-b.md` сверил с кодом 13.10).
- Латентный `total_cost_usd or 0` в измерителях превратит строку журнала без стоимости в «$0 как факт» (`plans/BACKLOG.md:142`).
- Ретро не делит цену доработки по причинам: `repair_cause` в `retro_numbers.py` — 0 вхождений на 13.10 (дайджест t-713), `REPAIR_CAUSES` живёт в `controller.py` (`plans/BACKLOG.md:106`).
- Дашборд, записанный через `--out`, несёт абсолютные ссылки `file:///C:/…` (`plans/BACKLOG.md:178`).
- 13 открытых строк в пачке 1 и 16 находок (дайджест t-713, пересчёт 13 из 13 и 16 из 16 на 13.10).

## Пачки

| № | Что изменится для пользователя | Строки | Размер | Статус | Взял | Ветка | MR |
|---|---|---|---|---|---|---|---|
| 1 | цена задачи одна и истинная (P18), дашборд по задачам и стадиям, прогноз по размеру, никаких «$0 как факт» | B-083 | M | закрыта | — | — | `855d4e5c` |
| 2 | измерители не считают служебные строки журнала драйвера вызовами (`compare.driver_report`, `report_run.journal`) | CD2-1 | S | ожидает | — | — | — |

Открытое перенесено 01.11.2026 → release-next/1, execution-report/1, onboarding-forge/1, execution-report/2.

Статусы пачки: `ожидает` → `в работе` → `сдано` → `принято` → `закрыта`. Размер — по узлам: S ≤ 4 узлов,
M 5–9, L 10–15 (больше — две пачки). Взятая пачка заморожена: её файл правит только взявший, новое
по теме — файлом в `findings/`.

## Бриф пачки 1

Начать с CD1-1 (сбор цены: «(no task)», хвост сессии, `usage_complete`) — денежный дифф, критик обязателен; CD1-4 (дашборд)
идёт независимо. Стенд не нужен — свидетель эталонные прогоны (cmp1 и новее). Ждёт слова владельца: CD1-5 (цель по стоимости,
D-03). Подробно — `batch-1-true-price.md`, раздел «Бриф».

## Дороги

Читать по порядку: эта карточка → `batch-1-true-price.md` → находки узла (колонка «id / файл» ниже) → строки
`plans/BACKLOG.md` 106, 110–112, 140, 142, 173, 178, 182, 295, 416, 417, 457 → `PROJECT.md` P18 (цена одна и истинная) →
код зоны по функциям из «Слов» → `ai-packages/qa-factory/references/model-rates.json` → `experiments/measurers/` (эталонные
прогоны и `answers/`) → `BACKLOG.md` §9 (решения D-02, D-03).
Слова: `plans/features.json` F14 (поле `words`) и сверх них: `collapse_requests`, `_written_after`, `recapture_session`,
`usage_complete`, `scan_file_incremental`, `total_cost_usd`, `model-rates.json`, `usage_report`, `repair_cause`,
`REPAIR_CAUSES`, `story_bug_rows`, `bugs_by_case`, `sizing.json`, `external_calls`, `(no task)`, `judge.settings`,
`file:///`; «цена задачи», «$0 как факт», «управляющий слой», «прогноз по размеру».
Не читать: код стадий, зону `live-runs` (находка про CLI testproject1 в `cost_capture` — только как связь), `story_run.py`.

## Содержание

Снимок 13.10.2026; пути — от `ai-packages/qa-factory/scripts/`; суть строк — из `plans/BACKLOG.md`, находок — из дайджеста t-713. При расхождении авторитетны файлы пачек.

| id / файл | вид | суть (≤ 20 слов) | пути | статус | слово владельца | связи |
|---|---|---|---|---|---|---|
| **Сбор цены (пачка 1, CD1-1)** | | | | | | |
| B-219 | строка | `collapse_requests` сворачивает сессии драйвера в одну строку «(no task)»; чинить сбор живым прогоном | `cost_capture.py` | пачка 1, CD1-1; дашборд починен отдельно по тексту | нет | — |
| B-397 | строка | `_written_after` сравнивает по mtime с запасом +1 с: хвост сессии в ту же секунду пропускается | `cost_capture.py` | пачка 1, CD1-1 | нет | — |
| B-398 | строка | `recapture_session` всегда ставит `usage_complete: True`; импорт Codex становится «полно» без нового свидетельства | `cost_capture.py` | пачка 1, CD1-1 | нет | — |
| **Сбор цены: диапазон и транскрипт (пачка 1, CD1-2)** | | | | | | |
| B-439 | строка | заявка на диапазон цены считается по диапазону регулярки, а не по вызову; тихие приведения в `judge.settings` теряют «отключить суждение» | `cost_capture.py`, `retro_numbers.py`, `judge.py` | пачка 1, CD1-2 | нет | `live-runs`, `stand-and-sources`, `execution-probes` (остатки инвентаря) |
| B-121 | строка | дайджест вернувшейся роли брать из её транскрипта, а не из сессии родителя | `cost_capture.py` | пачка 1, CD1-2 | нет | — |
| **Достоверность измерителей (пачка 1, CD1-3)** | | | | | | |
| B-141 | строка | латентный `total_cost_usd or 0` в измерителях: строка журнала без стоимости станет «$0 как факт» | `experiments/measurers/context_shape.py`, `experiments/measurers/conductor_families.py` | пачка 1, CD1-3; номера строк сдвинулись — проверить по коду | нет | — |
| B-138 | строка | таблица цен `usage_report.py` расходится с `model-rates.json`: нет двух новых моделей, `claude-sonnet-5` по $3/$15 | `tools/usage_report.py`, `references/model-rates.json` | пачка 1, CD1-3: актуально на 13.10 (дайджест t-713) | нет | — |
| **Дашборд (пачка 1, CD1-4)** | | | | | | |
| B-084 | строка | дашборд: расход по агентам — вкладка на каждую задачу | `factory_dashboard.py` | пачка 1, CD1-4 | нет | — |
| B-085 | строка | дашборд: задача раскрывается по стадиям S0–S9 со временем каждой стадии | `factory_dashboard.py` | пачка 1, CD1-4 | нет | — |
| B-187 | строка | дашборд: необязательный вид `--task <T>`; по умолчанию дашборд накапливает (решение 30.09) | `factory_dashboard.py` | пачка 1, CD1-4 | дано 30.09 | — |
| B-198 | строка | дашборд через `--out` несёт абсолютные `file:///C:/…`; нужны относительные ссылки или путь простым текстом | `factory_dashboard.py` | пачка 1, CD1-4 | нет | — |
| **Прогноз и ретро (пачка 1, CD1-5 и CD1-6)** | | | | | | |
| B-083 | строка | прогноз стоимости стори по размеру (`sizing.json` и факт) по мере накопления прецедентов | `retro_numbers.py` | пачка 1, CD1-5: зависит от решения D-03 | ждёт: цель по стоимости, D-03 | — |
| B-079 | строка | ретро делит цену доработки по `repair_cause` | `retro_numbers.py` | пачка 1, CD1-6: актуально на 13.10 (0 вхождений в `retro_numbers.py`) | нет | — |
| B-080 | строка | параллельные окна S5 (цепочки окон параллельно, запуски — одной очередью к стенду) | `story_run.py`, `controller.py`, `run_suite.py` | пачка 1, CD1-24 (отдельный релиз 0.11.0, после 0.10.7) | да, 29.10.2026: спека t-1576, развилки решены, отдельный релиз | находка ниже |
| **Сбор и достоверность (кандидаты пачки 2)** | | | | | | |
| `findings/B-238-tsena-vyborki-tiketa-lozhitsya-na-zadachu.md` | находка | цена выборки тикета ложится на задачу: сессия jira-assistant записана в «(no task)» | `cost_capture.py` | открыто (опирается на решение D-06 от 01.10) | дано 01.10 | `forge` |
| `findings/B-130-khuk-metrik-ne-vkladyvaet-recorded-metric.md` | находка | хук метрик вкладывает «Recorded metric signals…» после каждого Write | `telemetry_hook.py` | перенос: speed-cost/1 (SC1-4) | нет | — |
| **Дашборд и аналитика (кандидаты пачки 2)** | | | | | | |
| `findings/B-322-dashbord-pokazyvaet-bagi-obshchego-kataloga-po.md` | находка | дашборд показывает баги общего каталога по одному id кейса | `factory_dashboard.py` | возможно сделано частично: `story_bug_rows` привязывает по `task`, `bugs_by_case` — по id кейса; проверить по коду | нет | — |
| `findings/B-105-nedelnaya-kross-proektnaya-analitika-odin-md.md` | находка | недельная кросс-проектная аналитика одним файлом | — | отложено владельцем | отложено | — |
| **Управляющий слой (кандидат пачки 2)** | | | | | | |
| `findings/B-077-dolya-upravlyayushchego-sloya-porog-0-35-ne.md` | находка | порог доли управляющего слоя 0.35 не подтверждён; замер после прогона против judge-off | — | ждёт слова владельца | да | `live-runs` (прогон против judge-off) |
| **Рычаги расхода контекста и времени (кандидаты пачки 2)** | | | | | | |
| `findings/B-070-mekhanicheskuyu-pochinku-formy-svezhim-uzkim.md` | находка | чинить форму свежим диспатчем, не `--resume`: возобновлённый ход дороже свежего в 1.95 раза | — | перенос: speed-cost/1 (SC1-1) | нет | — |
| `findings/B-071-slaysy-on-demand-mekhanizm-est-vyklyuchen-reshit.md` | находка | слайсы `on_demand`: механизм есть, выключен; решить по `stage_compare` на живой стори (0 из 290 субагентов открыли файл) | — | перенос: speed-cost/1 (SC1-9) | нет | — |
| `findings/B-073-razdelit-s1-na-sborshchikov-po-istochniku.md` | находка | разделить S1 на сборщиков по источнику: пик контекста стратега 746K, цель до 150K | — | перенос: speed-cost/1 (SC1-10) | нет | — |
| `findings/B-074-vozobnovlyat-v-5-minutnom-okne-kesha-zamerit.md` | находка | возобновлять в 5-минутном окне кэша; замерить часовой кэш | — | перенос: speed-cost/1 (SC1-11) | нет | — |
| `findings/B-075-okna-s5-dlya-ne-ui-keysov-4.md` | находка | окна S5 для не-UI кейсов 4 → 8 | `controller.py` | актуально; ссылка на строку устарела, значение по умолчанию в `split_windows` | нет | — |
| `findings/B-078-kriteriy-poleznosti-sobrannogo-esli-material-mr.md` | находка | критерий полезности собранного: материал, нигде ниже S1 не процитированный, сужает сбор | — | перенос: speed-cost/1 (SC1-10) | нет | — |
| `findings/B-080-parallelnye-okna-s5-tolko-posle.md` | находка | параллельные окна S5 — только после замера цены последовательного S5 на большой стори | — | пачка 1, CD1-24 (отдельный релиз 0.11.0, после 0.10.7) | да, 29.10.2026: «да добавь»; спека t-1576 просмотрена, развилки F1–F10 решены, отдельный релиз (F0) | — |
| `findings/B-081-gruppirovka-krasnykh-prob-po-ekvivalentnosti.md` | находка | группировка красных проб по эквивалентности (`covered_by_equivalence`) — рычаг стоимости | `red_sandbox.py` | открыто | нет | — |
| `findings/B-082-selftest-pul-dlya-cmd-selftest-scripts-25-detey.md` | находка | `selftest`: пул для `cmd_selftest_scripts` (25 детей подряд), обновить `SLOW_TESTS` | `selftest.py` | открыто | нет | `package-ci` |
| `findings/B-107-prichina-rosta-chisla-faylov-telemetrii-fayl.md` | находка | причина роста числа файлов телеметрии: 5038 файлов, симптом вылечен, причина нет | — | перенос: speed-cost/1 (SC1-4) | нет | — |
| `findings/B-128-razmer-po-tipu-tiketa-bug-s.md` | находка | размер по типу тикета: Bug с 14 требованиями не должен упираться в потолок 1 | — | открыто | нет | — |
| `findings/20261016-model-rates-paketa-rashoditsya-so-stranitsey-tsen.md` | находка | таблица тарифов пакета расходится со страницей цен: Sonnet 5.5 `cache_read` 0.2 → 0.10, строк 5.x нет | `references/model-rates.json`, `scripts/task_price.py` | пачка 1, CD1-7 | нет | — |
| `findings/20261016-tsena-cli-protiv-tablitsy-tarifov-i-ostatki-cd1-7.md` | находка | цена CLI против таблицы на кэш-чтении Sonnet 5.5 (замер первым ходом); штамп ревизии без читателя; алиасы; загрузчики мимо `read_json` | `scripts/task_price.py`, `scripts/cost_capture.py` | пачка 1, CD1-8 | нет | — |
| `findings/20261016-cost-capture-ne-chitaet-iterations-otkat-modeli-v-tsene-stori.md` | находка | цена стори не читает `usage.iterations` — откат модели считается по одной модели (та же дыра, что F6-23 закрыл в tools) | `scripts/cost_capture.py` | пачка 1, CD1-9 | нет | — |
| `findings/20261016-ostatki-cd1-9-add-usage-split-vyshe-zapisi-count-friction-fixture.md` | находка | остатки CD1-9: `add_usage` на верхнем пути ценит вложенный split выше записи кэша; `_row_usage`/`_count`; аналог `friction.turns_of`; общая фикстура tools/пакет; строка оси 14 (критики t-900/t-902) | `scripts/cost_capture.py`, `scripts/friction.py`, `tools/test_usage_report.py` | пачка 1, CD1-10 | нет | — |
| **Фабричные виды активности (пачка 1, CD1-11)** | | | | | | |
| `findings/20261020-factory-dashboard-chitaet-status-fb-po-pozicii-kolonki.md` | находка | `parse_backlog_section` :357 режет строку FB по `|` и берёт статус по индексу: просьба человека с `\|` в словах показывается закрытой | `scripts/factory_dashboard.py` | пачка 1, CD1-12 | нет | `collect/1` CL1-5, ось 21 |
| `findings/20261019-factory-types-kopii-v-hooklib-i-cost-capture.md` | находка | множество «фабричных» видов активности литералом в `hooklib`, `cost_capture` (×2) и дашборде; расход скилла `collect` — `Unclassified` | `scripts/hooklib.py`, `scripts/cost_capture.py`, `scripts/dashboard_cost_groups.py` | пачка 1, CD1-11 | нет | `collect` (CL1-4: `FACTORY_TYPES`) |
| `findings/20261024-cena-kritika-keysov-ne-uchtena.md` | находка | расход resumed-агента `qa-case-critic` не учтён (`cost: null`), цена истории 12586 занижена на ~$2.24 | `scripts/cost_capture.py`, `scripts/task_price.py` | пачка 1, CD1-13 | слово 24.10.2026 | P18, t-1211 |
| `findings/20261025-cost-capture-zamedlyaet-vyzovy.md` | находка | каждый вызов инструмента вдвое медленнее; подозреваемый — `cost_capture` (177 запусков, до 144 с; Stop держит ход) | `cost_capture.py`, `telemetry_hook.py`, `hooks.json` | CD1-14, ожидает | вопрос 24–25.10.2026 (поведение) | t-1221; CD1-13; DC1-9 |
| `findings/20261026-telemetriya-perepisyvaet-vse-agregaty-kazhdye-40-s.md` | находка | после HF2-9 сбор цены каждые ~40 с переписывает все агрегаты телеметрии (1750 файлов и растёт); правка роли 5–11 с | `cost_capture.py`, `telemetry_capture.py`, `telemetry_hook.py` | перенос: speed-cost/1 (SC1-4) | П1, слово 26.10.2026 | CD1-14 / HF2-9 |
| **Находки прогона 14857 (0.10.2), 27.10.2026** | | | | | | |
| `findings/20261027-aktivnost-doctor-ne-zakryta-cena-istorii-polovina.md` | находка | N-1: активность `doctor` не закрыта, цена истории $13.86 против $27.82 (P18) | `scripts/cost_capture.py`, `scripts/factory_dashboard.py` | пачка 1, CD1-16 | нет | N-2 |
| `findings/20261027-18-rashozhdenij-dashboard-retro-i-istochnikov.md` | находка | N-2: 18 расхождений дашборда и ретро с первичными записями (D1–D18) | `scripts/factory_dashboard.py`, `scripts/metrics_projection.py` | пачка 1, CD1-17 | нет | N-1, FB-13 |
| `findings/20261027-potok-orkestratora-schitaetsya-marafonnym-dispatchem.md` | находка | A1: поток оркестратора считается «марафонным диспатчем»; карточка и F04 расходятся | `scripts/factory_dashboard.py`, `scripts/metrics_projection.py` | пачка 1, CD1-18 | нет | A2 |
| `findings/20261027-stop-pop-istorii-otkryvaet-segment-roditelya.md` | находка | Сторона записи активностей: Stop-выход истории открывает сегмент родителя (остаток SC3-22) | `scripts/activity_capture.py`, `scripts/cost_capture.py` | пачка 1, CD1-19 | нет | N-1 |
| `findings/20261027-chitateli-incomplete-s-odnoj-prichinoj.md` | находка | Три читателя сводят `incomplete` к одной причине | `scripts/retro_numbers.py`, `scripts/story_progress.py`, `scripts/story_budget.py` | пачка 1, CD1-20 | нет | N-1 |
| `findings/20261027-codex-host-binding-roditel-posle-stop.md` | находка | Дочерний процесс Codex наследует активность родителя после Stop | `scripts/cost_capture.py` | пачка 1, CD1-21 | нет | N-1 |
| `findings/20261027-otkrytaya-aktivnost-cherez-granitsu-stadii.md` | находка | Диапазон для названных денег и граница по стадиям журнала | `scripts/task_price.py` | пачка 1, CD1-22 | да (форма диапазона) | N-1 |
| `findings/20261027-avtorekapchur-staryh-cost-po-pravilu-privyazki.md` | находка | Автоперезапись cost-файлов 0.10.2 по версии правила привязки | `scripts/cost_capture.py` | пачка 1, CD1-23 | нет | N-1 |
| `findings/20261029-tarif-chteniya-kesha-ne-tot-chto-u-shlyuza.md` | находка | дашборд считает `cache_read` Sonnet 5.5 по $0.10 (CD1-7), шлюз Test Project 1 берёт $0.20: $28.12 против $40.78 при тех же токенах; второго источника цены у прогона без драйвера нет | `model-rates.json`, `cost_capture.py`, `factory_dashboard.py`, `retro_numbers.py` | пачка 1, CD1-25 | да — владелец 29.10.2026: цена по Anthropic, ставки шлюза не берём; релиз 0.11.0 вместе с CD1-24 | CD1-7; CD1-5; CD1-18 |
| **Находки ночного прогона 14857 (0.10.6), 30.10.2026** | | | | | | |
| `findings/20261030-perenos-sessii-v-arhiv-pereschityvaet-cost-fajl-i-teryaet-privyazku.md` | находка | перенесённая в архив сессия пересоздаётся сбором: $12.35 на задачу и $9.98 на `(no task)` вместо $22.22 и $0.12; хода «архивировать прогон» нет | `scripts/cost_capture.py`, `scripts/factory_dashboard.py` | пачка 1, CD1-26 | нет | P18; t-1605 #17 |
| `findings/20261030-cena-zadachi-razezzhaetsya-po-dvum-strokam-dashborda.md` | находка | цена задачи разнесена по двум строкам дашборда («TP1-14857» только ночь, ручной в «Unclassified») и по `(no task)` | `scripts/factory_dashboard.py`, `scripts/cost_capture.py` | пачка 1, CD1-27 | нет | CD1-26; B-268; t-1605 #18 |
| `findings/20261030-tokeny-na-dashborde-glavnym-obrazom-deshyovoe-chtenie-kesha.md` | находка | токены на дашборде — 92–97 % чтение кэша, не мера цены | `scripts/factory_dashboard.py` | пачка 1, CD1-28 | нет | `speed-cost` (замер токенов 12586); t-1605 #19 |
| `findings/20261030-schetchiki-instrumentov-v-cost-fajle-rastut-pri-kazhdom-sbore.md` | находка | счётчики инструментов субагентов растут при каждом сборе (`Bash` 17 065 против 405) | `scripts/cost_capture.py`, `scripts/factory_dashboard.py` | пачка 1, CD1-29 | нет | t-1605 #20 |
| `findings/20261030-polosy-razmera-bands-obshchie-dlya-strok-i-funkcij.md` | находка | `BANDS` общие для размера в строках и в функциях: один ярлык, две единицы | `scripts/metrics_projection.py`, `scripts/factory_dashboard.py` | пачка 1, CD1-30 | нет | CD1-5; критик SC2-37/CD1-5 п. 3 |
| `findings/20261030-vidzhety-tab-estimates-smeshivayut-edinicy-razmera.md` | находка | виджеты 1–2 `tab_estimates` смешивают единицы в медиане и круге попаданий | `scripts/factory_dashboard.py` | пачка 1, CD1-31 | нет | CD1-30; F-D2 (а) |
| `findings/20261030-nearest-precedents-bez-filtra-edinicy-i-svoej-zapisi.md` | находка | `nearest_precedents` без фильтра единицы и без исключения своей записи | `scripts/sizing.py`, `scripts/retro_numbers.py` | пачка 1, CD1-32 | нет | CD1-5; решение №8 |
| `findings/20261030-u-actual-test-runs-i-function-count-net-chitatelya.md` | находка | у `actual.test_runs` и `forecast.function_count` реестра нет читателя | `scripts/factory_dashboard.py` | пачка 1, CD1-33 | нет | SC2-37, CD1-5; AR-22 |
| `findings/20261030-povrezhdennyj-blok-run-ostanavlivaet-retro.md` | находка | `run_block_metrics` падает на блоке с не-списком `results`, `numbers()` останавливается | `scripts/retro_numbers.py` | пачка 1, CD1-34 | нет | SC2-37 фикс-раунд |
| `findings/20261114-driver-report-schitaet-sluzhebnye-stroki-zhurnala-vyzovami.md` | находка, id — | `compare.driver_report` и `report_run.journal` считают служебные строки журнала драйвера вызовами; один перечень служебных видов | `experiments/measurers/compare.py`, `experiments/measurers/report_run.py` | пачка 2, CD2-1 | нет | критик темы CL4-1 (Q3); P18 |

## Входящие

`findings/` этой кучки; находку, не названную ни в одной пачке, называет `piles.py check --all` (е).

## Вопросы владельцу

- B-077: порог доли управляющего слоя 0.35 (решение D-02 в `plans/BACKLOG.md` §9) — подтвердить или поменять после замера прогона против judge-off? Находка `findings/B-077-dolya-upravlyayushchego-sloya-porog-0-35-ne.md`.
- B-083: цель по стоимости — старая или новая по задаче 13797 (решение D-03 в `plans/BACKLOG.md` §9)? От ответа зависит прогноз по размеру (узел CD1-5).
