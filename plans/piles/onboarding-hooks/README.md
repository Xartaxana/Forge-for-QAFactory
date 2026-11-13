# Онбординг, установка, хуки и гард (`onboarding-hooks`)

приоритет: П2 | фичи: F04, F16 | стенд: частично (L1/L2) | зона: `ai-packages/qa-factory/scripts/hooklib.py`, `scripts/guard_pre_tool.py`, `scripts/guard_app_under_test.py`, `scripts/stage_guard.py`, `scripts/test_files.py`, `scripts/runtime_paths.py`, `scripts/onboard_apply.py`, `scripts/dispatch_liveness.py`, `scripts/vcs_evidence.py`, `references/detectors.json`, `references/test-path-markers.json`, `hooks/run-py.cmd`

## Зачем

Сегодня гард, который не пускает роль писать в код приложения и гонять тесты мимо фабрики, обходится жёсткой ссылкой и
командами через оболочку (heredoc, `eval`, `python -c`), а решения «что такое тестовый файл» и «где лежат артефакты»
разбросаны по десятку мест, которые читают их по-разному. После первой пачки гард узнаёт эти обходы одним разбором
команды, «тестовый файл» и корень артефактов определены в одном месте и читаются одним кодом, а одинаковые
вспомогательные куски собраны в общие.

## Что не так сегодня (факты)

- Жёсткие ссылки обходят охрану границы приложения: создание ссылки и запись по ссылке проходят без разрешения, серьёзность высокая (`plans/BACKLOG.md:372`).
- Shell-индирекция (heredoc, `echo | bash`, `eval`, `python -c`, git-алиасы) проходит мимо гейтов запуска и доставки (`plans/BACKLOG.md:451`); сегментаторов оболочки три, разбор через `shlex` в пяти местах (`plans/BACKLOG.md:452`).
- Ключ `artifact_root` читается примерно в 20 местах и не описан в шаблоне конфига (`plans/BACKLOG.md:343`); `dispatch_liveness` и `vcs_evidence` зашивают `qa-factory/artifacts` (`plans/BACKLOG.md:392`).
- Идиома `_capped` встроена примерно в 18 местах пакета (`plans/BACKLOG.md:462`); цена разбора JSON-данных измерена около 25 мс на вердикт (`plans/BACKLOG.md:447`).
- Устаревший `coverage-map.receipt` даёт REJECT раньше шага retire при переустановке (находка 01.10, до живой переустановки): переустановка лежит только находками, строки про неё в пачке нет.
- 16 открытых строк в пачке 1 и 16 находок (дайджест `docs/tasks/specs/reports/t-714-scout-piles-c.md`, пересчёт 16 из 16 и 16 из 16 на 13.10).

## Пачки

| № | Что изменится для пользователя | Строки | Размер | Статус | Взял | Ветка | MR |
|---|---|---|---|---|---|---|---|
| 1 | переустановка без потерь, заметки онбординга переживают компакцию, гард узнаёт shell-обходы и жёсткие ссылки, один токенайзер оболочки | — | M | закрыта | — | — | `855d4e5c` |
| 2 | читатели рисковых областей после OH1-10: иголка A13 по строкам DD и статический тест маркеров, три сообщения `sizing` вместо одного, строка discovery о ранжирующем документе, запас A22, помощник в `test_sizing`, `impact_scale` строкой без падения | — (находки 20.10 + вердикты t-1158/t-1166; 6 узлов) | M (6 узлов) | закрыта | dev1, 20.10.2026 | `pile/onboarding-hooks/batch-2` | `7f4a6e27` |
| 3 | срез общего слоя ролей (запас A22 ≥ 3 000 B у каждой роли — OH2-4, остановленный на F-12) и читатели после пачки 2: маркер `application repo paths` без `add`, `sizing` читает `impact_scale` своим читателем | `batch-3-common-layer-and-readers.md` | S (3 узла) | закрыта | — | `pile/onboarding-hooks/batch-3` | `855d4e5c` |
| 4 | имена возможностей хоста в гейте A в одном месте (хвост OH1-11) | — (находка 02.11.2026, узел OH4-1) | S | в работе | dev1 (Opus coord), 12.11.2026 | `pile/onboarding-hooks/batch-4` | — |
| 5 | находки кучки, не лежавшие в пачках: разбор класса `${CLAUDE_PLUGIN_ROOT}`, `readiness` читает `closed_by_run`, один носитель раскладки `state/`, переустановка со старой квитанцией, хвосты native_context и идентичности сессии; два вопроса владельцу | `batch-5-nerazlozhennye-nakhodki.md` (16 находок; 15 узлов) | L (15 узлов) | в работе | dev1 (Opus coord), 12.11.2026 | `pile/onboarding-hooks/batch-5` | — |
| 6 | остатки t-203 и критика t-227: копии проверки «одна компонента пути» зовут одного выжившего, потолок длины компоненты, суффикс временного имени `_publish`, отказы нативного контекста видны отчёту, верный хвост текста при сбое перезаписи | `batch-6-ostatki-t-203-i-t-227.md` (4 находки; 6 узлов) | M (6 узлов) | в работе | Lead dev1 (Opus), 13.11.2026 | `pile/onboarding-hooks/batch-6` | — |
| 7 | остатки t-263: два писателя публикуют через `atomic_text`, отказы `check_override`/`rewritten_input` в реестре A24, pending-файл не-словарь и дверь для не стартовавшего запуска, текст гарда тестовых путей по `s5.md` | `batch-7-ostatki-t-263.md` (5 находок; 5 узлов) | M (5 узлов) | в работе | Lead dev1 (Opus), 13.11.2026 | `pile/onboarding-hooks/batch-7` | — |

Открытое перенесено 01.11.2026 → release-next/1, words-gates/1, driver-hosts/1, execution-report/1, onboarding-forge/1, live-runs/2, driver-hosts/2, execution-report/2, onboarding-forge/2.

Статусы пачки: `ожидает` → `в работе` → `сдано` → `принято` → `закрыта`. Размер — по узлам: S ≤ 4 узлов,
M 5–9, L 10–15 (больше — две пачки). Взятая пачка заморожена: её файл правит только взявший, новое
по теме — файлом в `findings/`.

## Бриф пачки 1

Начать с OH1-1 (жёсткие ссылки и пустой файл через `apply_patch`, серьёзность высокая), затем OH1-2 (один токенайзер);
OH1-3…OH1-6 идут по `hooklib.py` по очереди. Стенд нужен только для живых прогонов L1/L2 (их ведёт `live-runs`).
Ждёт слова владельца: маркеры тестовых путей (находка) — не блокирует пачку. Подробно — `batch-1-guard-and-install.md`, раздел «Бриф».

## Дороги

Читать по порядку: эта карточка → `batch-1-guard-and-install.md` → находки узла (колонка «id / файл» ниже) → строки
`plans/BACKLOG.md` 343, 372, 374, 392, 445–447, 449, 451, 452, 454, 462, 465, 470, 471, 474 → код зоны по функциям из
«Слов» → `ai-packages/qa-factory/references/test-path-markers.json`, `references/detectors.json` →
`docs/SIBLING_MAP.md` (оси «путь артефактов», «тестовый файл») → `PROJECT.md` P2, P14, P15.
Слова: `plans/features.json` F04, F16 (поле `words`) и сверх них: `_scan`, `SHELL_EXPANSION`, `DIRECT_TEST_RUN`,
`_empties_existing_file`, `apply_patch`, `heredoc`, `shlex`, `load_ref_json`, `_table`, `shape_in`, `_capped`,
`artifact_root`, `env_file`, `load_env`, `write_atomic`, `cmd_close`, `project_inventory`, `implementations`,
`CLAUDE_PLUGIN_ROOT`, `install-paths.json`, `session_identity`, `native_context`, `coverage-map.receipt`;
«жёсткая ссылка», «токенайзер», «тестовый файл», «корень артефактов», «переустановка».
Не читать: зоны `live-runs` (живые прогоны L1/L2), `package-ci` (формы тикета и доставки), `driver-controller` (читатель «верха git» — его узел DC1-7).

## Содержание

Снимок 13.10.2026; пути — от `ai-packages/qa-factory/scripts/`; суть строк — из `plans/BACKLOG.md`, находок — из дайджеста t-714. При расхождении авторитетна доска `plans/PILES.md`.

| id / файл | вид | суть (≤ 20 слов) | пути | статус | слово владельца | связи |
|---|---|---|---|---|---|---|
| **Охрана границы приложения (пачка 1, OH1-1)** | | | | | | |
| B-349 | строка | жёсткие ссылки обходят охрану границы: создание ссылки и запись по ссылке проходят без разрешения (серьёзность высокая) | `guard_app_under_test.py`, `guard_pre_tool.py` | пачка 1, OH1-1 | нет | — |
| B-351 | строка | `apply_patch` Codex с `Update File`, после которого файл пуст, не распознаётся как удаление (`_empties_existing_file`) | `guard_app_under_test.py` | пачка 1, OH1-1 | нет | — |
| **Один токенайзер оболочки (пачка 1, OH1-2)** | | | | | | |
| B-433 | строка | shell-индирекция (heredoc, `echo` в `bash`, `eval`, `python -c`, git-алиасы) проходит мимо гейтов запуска и доставки | `hooklib.py`, `stage_guard.py`, `guard_pre_tool.py` | пачка 1, OH1-2 | нет | `stand-and-sources` (остатки форм) |
| B-434 | строка | один токенайзер и сегментатор оболочки для всех гейтов: три сегментатора, `shlex` в пяти местах, разбор `cd` | `hooklib.py`, `stage_guard.py`, `guard_pre_tool.py` | пачка 1, OH1-2 | смена данных — слово Lead | — |
| B-436 | строка | качество кода гарда тестов: `hooklib._scan` 107 строк, `elif`-цепь, мёртвая ветка, не закоммичен скрипт мутантов | `hooklib.py` | пачка 1, OH1-2 | нет | `live-runs` (гард тестов) |
| B-453 | строка | остатки мест тестов: `SHELL_EXPANSION` не знает extglob, `check()` 122 строки, повторный глоб, перезапись эталона | `test_path_grants.py` | пачка 1, OH1-2 | нет | `package-ci` (места тестов) |
| **Ось «тестовый файл»: читатели, данные, кэш (пачка 1, OH1-3 и OH1-4)** | | | | | | |
| B-427 | строка | один читатель вместо копий: `implementations` манифеста (5 читателей), разрешители репозиториев (3), обходчики сегментов | `hooklib.py`, `story_run.py` | пачка 1, OH1-3 | нет | `package-ci` (инвентарь) |
| B-428 | строка | закрытое разнообразие в данные (FR-13); пункты (1)–(3) закрыты 07.10 по тексту, открыт (4): `arch_check` и `//`-комментарии | `test_files.py`, `arch_check.py` | пачка 1, OH1-3: проверить по коду, что открыт только (4) | нет | — |
| B-429 | строка | один кэшированный разбор JSON-данных на вызов (`load_ref_json`, `_table`, `shape_in`); цена ~25 мс на вердикт | `hooklib.py`, `test_files.py` | перенос: speed-cost/1 (SC1-5) | нет | — |
| B-431 | строка | «это тестовый файл» — открытые стороны оси: `arch_check`, `validate_artifacts`, `repo_map`, `gate_preflight`, `judge_code`, `friction`, `test_path_grants` | `test_files.py`, `repo_map.py`, `gate_preflight.py` | пачка 1, OH1-4 | нет | — |
| B-459 | строка | `project_inventory` — потребитель листа «тест-файл?» без строки в таблице потребителей; добавить строку `inventory` | `project_inventory.py` | пачка 1, OH1-4 | нет | — |
| **Общие помощники (пачка 1, OH1-5)** | | | | | | |
| B-444 | строка | идиома `_capped` — около 18 встроенных копий по пакету; свести в один помощник | `gate_preflight.py` | пачка 1, OH1-5 | нет | `forge` (батч 4: повторы) |
| B-447 | строка | один разделитель строк по `\r\n`, `\r`, `\n`: четыре копии в `ticket_light`, `question_register`, `execution_fingerprint`, `onboard_apply` | `ticket_light.py`, `question_register.py`, `execution_fingerprint.py`, `onboard_apply.py` | пачка 1, OH1-5 | нет | — |
| **Корень артефактов (пачка 1, OH1-6)** | | | | | | |
| B-319 | строка | ключ `artifact_root` читается ~20 местами, не описан в шаблоне; разбор `env_file` в четырёх модулях, `load_env` с обратным приоритетом | `hooklib.py`, `gate_preflight.py` | пачка 1, OH1-6 | нет | `report-delivery` (корень багов) |
| B-370 | строка | `dispatch_liveness` и `vcs_evidence` зашивают `qa-factory/artifacts`, не читая `artifact_root` | `dispatch_liveness.py`, `vcs_evidence.py` | пачка 1, OH1-6 | нет | — |
| **Заметки онбординга (пачка 1, OH1-7)** | | | | | | |
| B-452 | строка | остатки заметок онбординга: `write_atomic` как седьмой писатель, дифф без `-z`, `cmd_close` 5 уровней; живые прогоны L1/L2 не сделаны | `runtime_paths.py`, `onboard_apply.py` | пачка 1, OH1-7 | нет | `live-runs` (L1/L2) |
| **Охрана и тестовые пути (кандидаты пачки 2)** | | | | | | |
| `findings/B-166-koren-paketa-vo-vremya-raboty-guard-pre-tool-py.md` | находка | корень пакета во время работы: тексты отказов гарда строятся с буквальным `${CLAUDE_PLUGIN_ROOT}`; нужна ось SIBLING_MAP | `guard_pre_tool.py` | пачка 5, OH5-2 (с B-142) | нет | — |
| `findings/B-355-markery-testovykh-putey-references-test-path.md` | находка | маркеры тестовых путей `__test__`, `testing`, `integration`, `fixtures`, `_tests` предложены и не добавлены | `references/test-path-markers.json` | пачка 5, OH5-14: ждёт слова владельца | да | `package-ci` |
| `findings/B-394-u-native-context-pending-path-okolo-stroki-42.md` | находка | `native_context.pending_path` и копия проверки пути в `worker_lifecycle`; дать `artifacts_dir` параметр `root` | `native_context.py`, `worker_lifecycle.py` | пачка 5, OH5-11 | нет | — |
| **Корень проекта и раскладка state/records (кандидаты пачки 2)** | | | | | | |
| `findings/B-249-raskladka-qa-factory-state-propisana-bukvalno-v.md` | находка | раскладка `qa-factory/state/...` прописана буквально в ~15 местах; нужен один носитель `install-paths.json` и тест-сторож | `host_probe.py`, `run_suite.py`, `onboard_apply.py` | пачка 5, OH5-6 | нет | — |
| `findings/B-298-klass-put-artefaktov-sobran-ot-proekta-cwd.md` | находка | класс «путь артефактов собран от проекта или cwd»: остатки вне N1b, отдельный узел после N2 | `dispatch_liveness.py`, `env_probe.py`, `execution_scheduler.py` | пачка 5, OH5-12 | нет | — |
| `findings/B-176-posle-t-078-v-artifact-writers-json-poyavilis.md` | находка | ключи-пути в `artifact-writers.json`: четыре читателя реестра проверить (FR-17) | `guard_pre_tool.py`, `contract_slices.py`, `artifact_supersede.py` | пачка 5, OH5-4 | нет | — |
| `findings/B-142-desktop-rezhim-komandy-claude-plugin-root.md` | находка | десктоп: `${CLAUDE_PLUGIN_ROOT}` в телах агентов не раскрывается хостом; решить, откуда роль берёт корень | `agents/*.md`, `runtime_paths.py` | пачка 5, OH5-2 (с B-166) | нет | `driver-controller` (две головы) |
| `findings/B-315-put-publikatsii-baga-iz-kornya-istorii.md` | находка | `artifact_producer.py publish` разрешает только `<task>/bugs/`, текст роли называет общий каталог | `artifact_producer.py`, `brief_pack.py` | пачка 5, OH5-9 | нет | `report-delivery` |
| **Установка, онбординг, сессия (кандидаты пачки 2)** | | | | | | |
| `findings/B-248-pereustanovka-poryadok-proverka-pokrytiya-ubrat.md` | находка | переустановка: порядок «проверка покрытия, потом убрать устаревшее» перепутан; устаревший `coverage-map.receipt` даёт REJECT | `onboard_apply.py`, `check_coverage.py` | пачка 5, OH5-7 (живая переустановка — live-runs) | нет | — |
| `findings/B-262-avtoobnovlenie-plagina-vklyuchaetsya-samo-kak-v.md` | находка | автообновление плагина включается само при (пере)установке, не трогая выбор человека | — | пачка 5, OH5-15: отложено: «позже» (владелец 02.10) | отложено 02.10 | — |
| `findings/B-242-zakreplennyy-id-modeli-proveryaetsya-pri-starte.md` | находка | закреплённый id модели проверяется при старте: снятая модель сорвала показ у лектора | — | пачка 5, OH5-5 | нет | — |
| `findings/B-153-progon-bez-sledov-b-003-readiness-py-beret.md` | находка | прогон без следов: `readiness.py` берёт `no_trace` только из CLI; читать `closed_by_run` и там | `readiness.py`, `gate_preflight.py` | пачка 5, OH5-3 | нет | — |
| `findings/B-451-b-410-identichnost-sessii-ostatki.md` | находка | остатки идентичности сессии: длина пути Windows, чужая квитанция `THIS_SESSION`, две проверки безопасного id | `session_identity.py`, `activity_capture.py` | пачка 5, OH5-13 (живые доказательства 1–3 ведёт `live-runs`) | нет | `live-runs` |
| `findings/B-325-nativnyy-kontekst-codex-kogda-khost-ne.md` | находка | нативный контекст Codex без имени дочернего агента; сначала измерить `SubagentStart` на живом Codex | `native_context.py` | пачка 5, OH5-10 | нет | — |
| `findings/B-360-zapuskatel-hooks-run-py-cmd-dobavlyaet-k.md` | находка | запускатель `hooks/run-py.cmd` добавляет около 1,15 с на вызов; выбирать интерпретатор без `where` | `hooks/run-py.cmd` | пачка 5, OH5-1: принято (сделано: 47ca1cf6, speed-cost/1 SC1-5) | нет | — |
| `findings/B-305-payplayn-7864129-na-kommite-paketa-57b65fb.md` | находка | пайплайн 7864129: (а) `test_driver_layers` красный, (б) два теста красные на Linux, (в) живая проверка положительной ветки | `scripts/tests/fixtures/driver-layers.json` | пачка 5, OH5-8 ((а) сделано; (б) в узле; (в) live-runs) | нет | `package-ci` |
| **Сбор данных проекта: секреты и просьбы изменить фабрику (пачка 1, OH1-8 и OH1-9)** | | | | | | |
| `findings/20261019-odna-tablitsa-shablonov-sekretov-dlya-garda-i-redaktora.md` | находка | шаблоны секретов в двух таблицах — гард записи и редактор сбора; нужно решение Lead о направлении ошибки гарда | `scripts/guard_secrets.py`, `references/collect-redaction.json` | пачка 1, OH1-8 | нет | `collect` (CL1-1) |
| `findings/20261019-prosba-izmenit-fabriku-v-onboarding-i-doctor.md` | находка | правило «просьба изменить фабрику оставляет след» не доходит до `qa-onboarding` и `qa-doctor`; оба текста у потолка | `skills/qa-onboarding/SKILL.md`, `skills/qa-doctor/SKILL.md` | пачка 1, OH1-9 | нет | `collect` (CL1-5) |
| `findings/20261020-onboarding-ne-sprashivaet-riskovye-oblasti.md` | находка | тема 4 интервью с `28fc7170` не спрашивает рисковые области; читатели (`sizing.py` P1 areas, `aspect-profile`, стратег) голодают; вернуть вопрос | `phases/p2-interview.md`, `p4-generate.md`, `sizing.py` (чтение) | пачка 1, OH1-10 | да (20.10 18:1x: «вернуть») | перепись t-1148; `kb/2` KB2-1 (строка User Guide) |
| **Читатели рисковых областей после OH1-10 (пачка 2)** | | | | | | |
| `findings/20261020-igolka-a13-po-vsemu-fajlu-bekloga-i-staticheskij-test-temy-4.md` | находка | иголка A13 ищет суть маркера по всему файлу бэклога; пример шаблона совпадает с ней; статический тест маркер ↔ команда DD | `scripts/audit_factory.py`, `references/templates/factory-backlog.md` | пачка 2, OH2-1 | нет | критик t-1166 F-2; t-1163 §L F-3 |
| `findings/20261020-sizing-sopostavlyaet-oblasti-po-slovam-bez-stemminga-fr-12-13.md` | находка | `find_area_match` сопоставляет область по словам без стемминга (FR-12/13); один текст «unavailable» на три состояния (FR-41) | `scripts/sizing.py` | пачка 2, OH2-2 | нет | t-1158 F-11 (b); t-1166 side note |
| `findings/20261020-p1-discovery-ne-ishchet-dokument-ranzhiruyushchij-oblasti.md` | находка | p1-discovery не ищет документ, ранжирующий области; p2:199 обещает его «когда прочитан» | `skills/qa-onboarding/phases/p1-discovery.md`, `p2-interview.md` | пачка 2, OH2-3 | нет | t-1158 F-11 (a) |
| **Пачка 3 (ожидает)** | | | | | | |
| `findings/20261021-marker-application-repo-paths-bez-komandy-add.md` | находка | маркер `[DEFERRED: application repo paths]` в P4 без команды `add`; строка `EXCEPTIONS` теста маркеров ждёт пары | `skills/qa-onboarding/phases/p4-generate.md`, `scripts/tests/test_onboarding_markers.py` | OH3-2, ожидает | — | OH2-1, t-1184 F-3, критик t-1201 Q1/Q12 |
| `findings/20261021-sizing-chitaet-impact-scale-svoim-chitatelem-ar-13.md` | находка | `sizing.py` держит свой читатель `impact_scale` рядом с `grammar.impact_scale`; не-ярусный `priority` → P2 молча | `scripts/sizing.py`, `scripts/tests/test_sizing.py` | OH3-3, ожидает | — | OH2-6 (а), t-1184 F-7, критик t-1201 Q5/Q7/Q11 |
| `findings/20261021-doverie-komandam-progona-po-forme.md` | находка | доверие команде прогона по форме: известный раннер проходит, необычная форма один раз ждёт «да» человека; одобрение по хэшу команды вне репозитория | `references/launch-causes.json` | OH3-4, ожидает | нет | обзор testing-factory (RELATED_WORK §2 п. 1) |
| `findings/20261022-doctor-do-onbordinga-proba-i-huki-v-raznyh-kornyah.md` | находка | доктор до онбординга во вложенном проекте: проба гарда пишет в корень git, хуки смотрят в проект — живые хуки объявлены неактивными | `host_probe.py`, `hooklib.py`, `skills/qa-doctor/SKILL.md` | OH3-5, ожидает | нет | класс TP1-14336; OH3-7 |
| `findings/20261022-doctor-daet-cheloveku-komandy-skriptov.md` | находка | доктор отдаёт человеку шаги роли (скрипты `host_probe.py`, `project_gitignore.py`); человек вызывает только скиллы | `skills/qa-doctor/SKILL.md`, `skills/qa-doctor/evals/evals.json` | OH3-6, ожидает | нет | P3, P9 |
| `findings/20261022-doctor-do-onbordinga-trebuet-gitignore.md` | находка | доктор до онбординга требует блок `.gitignore`, который пишет онбординг, из-за своих же квитанций в `state/` | `skills/qa-doctor/SKILL.md`, `project_gitignore.py` | OH3-7, ожидает | нет | OH3-5 |
| `findings/20261022-onbording-sprashivaet-cheloveka-pro-klyuchi-iz-koda.md` | находка | онбординг спрашивает человека, какой области нужны ключи из кода и кто их владелец; область — факт кода, вопрос о ключе — из стори | `skills/qa-onboarding/phases/p1-discovery.md`, `phases/p2-interview.md`, `project_inventory.py` | OH3-8, ожидает | слово владельца 22.10.2026 | P5, FR-50 |
| `findings/20261022-onbording-sprashivaet-pro-sluzhebnye-fajly-fabriki.md` | находка | онбординг спрашивает, удалить ли служебный файл фабрики; доказательство для gate A классится `regenerated` и идёт под удаление | `references/install-paths.json`, `onboard_apply.py` | OH3-9, ожидает | слово владельца 22.10.2026 | FR-3, AR-14 |
| `findings/20261022-proba-vhoda-shlet-username-a-stend-zhdyot-email.md` | находка | проба входа шлёт литерал `username`, стенд ждёт `email`; форма тела — из места вызова входа проекта или перебором известных форм | `stand_access.py`, `project_inventory.py`, `p1-discovery.md` | OH3-10, ожидает | слово владельца 22.10.2026 | AR-1, AR-22, FR-19 |
| `findings/20261022-doktor-vcs-api-401-ne-govorit-chto-delat.md` | находка | доктор о `vcs_api` 401 не называет хост и шаг: токен есть для git.example.com, проект на githost, `GITLAB_TOKEN` перебивает | `skills/qa-doctor/SKILL.md`, проба `vcs_api` | OH3-11, ожидает | нет | P9, FR-1 |
| `findings/20261022-doktor-rasskazyvaet-cheloveku-o-svoej-kuhne.md` | находка | доктор пересказывает человеку служебное: контекст ролей не подтверждён, `journal.jsonl` не закоммичен, `state/` обновлён | `skills/qa-doctor/SKILL.md` | OH3-12, ожидает | нет | OH3-6, P9 |
| `findings/20261022-proba-konteksta-ne-vidit-otvet-cherez-subagenthandback.md` | находка | проба контекста роли не видит ответ через `SubagentHandback`: контекст доставлен, но проба на этом хосте не проходит никогда | `host_probe.py`, `install_smoke.py` | OH3-13, ожидает | нет | OH3-12, AR-5 |
| `findings/20261022-strateg-ne-mozhet-prochitat-slovar-metok.md` | находка | стратег S3 послан за метками в `vocabulary.yaml` плагина, гард чтение запрещает, бриф списков не несёт — окно разметки «impossible», дирижёр носит списки руками | `brief_pack.py`, `phases/s3.md` | OH3-14, ожидает | нет | FR-15, AR-8; повтор 14857 S5 |
| `findings/20261022-razmer-xxl-u-zadachi-razmera-m.md` | находка | размер стори = сумма строк реестра: задача размера M вышла XXL с советом «разделить» влитый тикет | `sizing.py`, `automation-candidacy.md`, `gate_brief.py` | OH3-15, ожидает | да, дано 22.10.2026 (мерить в функциях; задача = M, начало золотого сета; проверить всё, что зависит от размера) | находки sizing этой кучки, P16 |
| `findings/20261022-zavershivshijsya-kritik-schitaetsya-zhivym.md` | находка | завершившийся критик считается живым: возврат через `SubagentHandback` не виден `dispatch_liveness`, доработка по reject — только словом человека | `dispatch_liveness.py`, `story_step.py`, `install_smoke.py` | OH3-16, ожидает | нет | OH3-13, AR-5 |
| `findings/20261023-polya-vhoda-stenda-zapisany-v-neskolkih-nositelyah.md` | находка | поля тела входа стенда записаны в двух носителях (`access.user_field`, `manual_capture.login.http.body`); две красные фикстуры повторяют шаблон руками | `manual_capture.py`, `config_contract.py`, `tests/test_config_migration.py`, `tests/test_install_retire.py` | OH3-17, ожидает | нет | OH3-10, t-056 D5 |
| `findings/20261023-brief-pereraboty-i-ticket-changed-ne-nesyot-slovar-metok.md` | находка | бриф `ticket_changed`-починки и доработки S3 не несёт списки меток, хотя вложены только в окно 1 | `brief_pack.py`, `handoff.py`, `controller.py`, `phases/s3.md` | OH3-18, ожидает | нет | OH3-14, t-058 |
| `findings/20261023-ostanov-rebyonka-pomechaet-raspisku-story-step-konechnoj-na-claude.md` | находка | остановка ребёнка помечает расписку `story_step` конечной на Claude (`host_dispatch.record`) вопреки правилу «только `story_step finish`» | `host_dispatch.py`, `dispatch_liveness.py` | OH3-19, ожидает | нет | OH3-16, t-060 F9, ось 20 |
| `findings/20261023-schetchiki-tool-use-schitayut-vozvrat-roli-vyzovom-instrumenta.md` | находка | `friction.py:134` и `cost_capture.py:1158` считают возврат `SubagentHandback` вызовом инструмента | `friction.py`, `cost_capture.py` | OH3-20, ожидает | нет | OH3-13, t-057 E5, ось 22 |
| `findings/20261023-oshibka-fabriki-v-bekloge-proekta-so-scope-upstream-candidate-proverit-na-zhivom.md` | находка | FB-3 и FB-5 прогона 12586 должны лежать в `factory-backlog.md` со scope `upstream-candidate`; проверка на живом повторе | `skills/qa-story/SKILL.md`, `agents/qa-retro-analyst.md` | OH3-21, ожидает | нет (слово дано 23.10.2026) | OH3-10, EP1-8 |
| **Находки прогона 14857 (0.10.2), 27.10.2026** | | | | | | |
| `findings/20261027-gard-stadii-lozhno-lovit-dostavku-v-chtenii-shell.md` | находка | N-4: гард стадии ловит команду доставки в чтении shell (`for … in`, `def log(`) | `scripts/stage_guard.py`, `references/adapter-forms.json` | пачка 3, OH3-22 | нет | — |
| `findings/20261029-gard-dostavki-chitaet-telo-heredoc-kak-komandu.md` | находка | гард доставки читает тело heredoc и кавычечный аргумент как команду: текст ответов с `gh pr create` отказан | `scripts/stage_guard.py`, `scripts/guard_pre_tool.py` | пачка 3, OH3-22 | нет | прогон 12586 на 0.10.5; OH3-22 (N-4) |
| `findings/20261029-onbording-pishet-profili-ne-toj-formy.md` | находка | онбординг пишет `profiles[].commands` списком и 60+ ошибок схемы; ничто не проверяет, `readiness.py` падает, S5 не запустит тест | `scripts/onboard_apply.py`, `scripts/profile_contract.py`, `scripts/readiness.py`, `skills/qa-onboarding/` | пачка 3, OH3-26…OH3-31 | да, 29.10.2026 — в следующий релиз | отчёт проекта на Playwright 0.10.2; EP1-22; SC2-36 |
| `findings/20261029-strazh-otkazyvaet-slesh-pered-chertoj-v-kavychkah.md` | находка | страж отказывает `\|` внутри кавычек (альтернатива `grep`) и советует «возьмите в кавычки»: 4 отказа за два окна S5 | `scripts/hooklib.py`, `scripts/guard_pre_tool.py` | пачка 3, OH3-32 | П1 0.10.7: «переносим к нам в релиз все пункты… которые ускоряют работу» (29.10.2026) | прогон 12586 на 0.10.5; OH3-22 |
| `findings/20261029-gitignore-work-evidence-ne-tot-katalog.md` | находка | блок `.gitignore` игнорирует `work/evidence/`, а итоговые доказательства и прогоны лежат в `evidence/`; `install-paths.json` зовёт `artifacts/**` carried; MR 12586 несёт 9 из 44 файлов, на которые ссылается отчёт; владелец: скриншоты в репозиторий не нужны — `evidence/**` игнорируется целиком | `install-paths.json`, `install_paths.py`, `project_gitignore.py`, `delivery_manifest.py`, `check_delivery.py` | пачка 3, OH3-33 | нет (П1 0.10.7 — решение Lead) | HF8-17; HF8-21; B-406 |
| `findings/20261029-preduprezhdenie-ustanovleno-0-10-3-pri-rabote-0-10-5.md` | находка | «installed by 0.10.3 - run the onboarding again» при работающей 0.10.5, `vcs_api`/`host_hooks`/`base_slice` unknown доходят до гейта A как предупреждения | хук `SessionStart`, `host_probe.py`, читатель предупреждений гейта A | пачка 1, OH1-11 | нет (слово владельца дано 29.10.2026) | HF8-9..14, OH3-13 |
| **Находки критика диффа S4a3 релиза 0.10.7, 30.10.2026** | | | | | | |
| `findings/20261030-windows-260-codex-dispatch-bez-konteksta.md` | находка | предел пути 260 знаков на Windows: пакет нативного контекста не пишется при корне длиннее 55 знаков, именной запуск роли в Codex идёт без контекста (журнал, не отказ); и CLI (`install_smoke --report`, `factory_dashboard`, `cost_capture` — последний не установлен), создающие `qa-factory/` до онбординга | `scripts/native_context.py`, `scripts/inject_context.py`, `scripts/hooklib.py`, `scripts/install_smoke.py`, `scripts/factory_dashboard.py`, `scripts/cost_capture.py` | пачка 3, OH3-36, OH3-37 | нет | OH3-5, `docs/tasks/specs/reviews/r0107-s4a3-diff-critic.md` |
| `findings/20261030-guard-pre-tool-ssylaetsya-na-udalyonnyj-heredoc-re-nameerror.md` | находка | `guard_pre_tool.py:1939` использует `_HEREDOC_RE`, которого нет в модуле (определение удалено в `ea9dbf5e`) | `scripts/guard_pre_tool.py` | пачка 3, OH3-38 | нет | OH3-22; `lint_ratchet` |
| `findings/20261030-voprosy-onbordinga-mjortvye-klyuchi-i-dod-bez-chitatelya.md` | находка | 43 вопроса: 6 ключей без читателя, `dod` без кода-читателя, рисковые области не доходят до размера (`sizing.py` читает `requirement` вместо заголовка реестра → `area_match` null везде) и до кейсов; дубли и выводимое кодом | `scripts/sizing.py`, `skills/qa-onboarding/phases/p2-interview.md`, `p4-generate.md`, `references/config-keys.json` | OH3-34 (ключ, П1), OH3-35 (диета интервью, П2 — слово владельца) | да (30.10: «нет ли лишних, все ли используются, все ли не могут быть отвечены фабрикой»); решения по ключам — §4 разбора | t-1621; `docs/tasks/specs/reviews/20261030-voprosy-onbordinga-audit.md`; OH1-10; OH2-2; SC5-6 |
| **Находки 31.10.2026 (предложение `qa-explore`)** | | | | | | |
| `findings/20261031-istochniki-trebovanij-bez-proizvoditelya-i-chitatelya.md` | находка | `requirements_sources` в конфиге без производителя и читателя: требования вне тикета и связей фабрика не видит | `skills/qa-onboarding/phases/p1-discovery.md`, `scripts/source_inventory.py`, `references/config-keys.json` | пачка 3, OH3-39 | да, 31.10.2026: «запиши как баг» | OH3-35 (ключ исключён из «снять»); XT1-2; уточнение по прогону ADD-TO-CART: S1 пишет «unreachable» при `verified` трекере |
| **Находки 31.10.2026 (прогон CART-1, MyBooks)** | | | | | | |
| `findings/20261031-klyuchi-uchyotki-polzovatelya-ne-svedeny-s-slovami-cheloveka.md` | находка | человек назвал `EMAIL_USER/EMAIL_PASS`, роль и вход по коду искали `USER_EMAIL/USER_PASSWORD`; гейт смотрел `.env`, конфиг — `.env.local` | `gate_preflight.py`, `manual_capture.py`, `brief_pack.py`, `p2-interview.md` | пачка 3, OH3-40 | нет | свод CART-1 3.5; OH3-10 (поля тела входа), OH3-17, OH3-35 |
| **Очередь релиза 0.10.8 (критик t-561; t-567)** | | | | | | |
| `findings/20261031-brief-s5-avtomatora-bez-stroki-uchetki.md` | находка, id — | бриф S5 автоматора без строк об учётках стенда (t-561 Ф-9 б, Ф-13) | `scripts/brief_pack.py`, `agents/qa-automator.md` | OH3-41, ожидает | нет | OH3-40 |
| `findings/20261031-dva-razbora-env-fajla.md` | находка, id — | три разбора env-файла читают строку по-разному (t-561 Ф-9 в) | `scripts/env_probe.py`, `scripts/manual_capture.py`, `scripts/stand_health.py` | OH3-42, ожидает | нет | OH3-40 |
| `findings/20261102-oh1-11-imena-vozmozhnostej-v-dvuh-regulyarkah.md` | находка | имена возможностей хоста и префикс строки написаны в двух регулярных выражениях гейта A | `scripts/gate_brief.py` | пачка 4, OH4-1 | нет | t-746 m-3; OH1-11 |
| **Остатки t-203 и критика t-227 (13.11.2026)** | | | | | | |
| `findings/20261113-kopii-proverki-odnoj-komponenty-puti.md` | находка, id — | девять копий проверки «одна компонента пути» (одна — `recover_codex_usage.py:16` без охраны `..`) вместо `hooklib.is_one_component` | `scripts/hooklib.py`, `scripts/host_dispatch.py`, `scripts/exit_gate.py`, `scripts/stage_guard.py`, `scripts/activity_capture.py`, `scripts/cost_capture.py`, `scripts/recover_codex_usage.py` | пачка 6, OH6-1 | нет | OH5-11; t-203 §4; t-227 B-2, B-3 |
| `findings/20261113-komponenty-puti-bez-potolka-dliny.md` | находка, id — | ключ, основа имени и id сессии растят записываемый путь без потолка; одна константа рядом с `PACKET_ROOT_LIMIT` | `scripts/native_context.py` и места скаута | пачка 6, OH6-2 | нет | скаут t-216; OH6-3; OH5-13 |
| `findings/20261113-oh5-11-ostatki-f2-publish-temp-f6-native-valueerror.md` | находка, id — | суффикс временного имени `_publish` 32 → 8 hex (F-2); отказы нативного контекста без `note_denial` и A24 (F-6); F-5 закрыта «оставить» | `scripts/event_store.py`, `scripts/native_context.py`, `scripts/inject_context.py`, `scripts/refusal_registry.py` | пачка 6, OH6-3, OH6-4 | нет | t-203 §5-§6; OH5-10, OH5-13 |
| `findings/20261113-t-227-q5-ochered-tekst-deliver-write-failed-i-razrez-deliver.md` | находка, id — | хвост «a shorter folder» печатается и для перезаписи F-9, где причина не длина; `deliver` ~58 строк — резать при OH5-10 | `scripts/inject_context.py` | пачка 6, OH6-5, OH6-6 | нет | t-227 Q5; OH5-10 |
| **Остатки спеки t-263 (13.11.2026)** | | | | | | |
| `findings/20261113-dva-publikatora-dashboard-i-migrate-coverage-mimo-atomic-text.md` | находка, id — | `factory_dashboard.py:4170` и `migrate_coverage.py:25` публикуют своим 32-hex именем; оба зовут `event_store.atomic_text` | `scripts/factory_dashboard.py`, `scripts/migrate_coverage.py` | пачка 7, OH7-1 | нет | t-263 F-C; OH6-3 |
| `findings/20261113-otkazy-check-override-i-rewritten-input-bez-stroki-a24.md` | находка, id — | `ValueError` из `codex_roles.py`/`host_adapter.py` без строки A24; регистрировать по форме D | `scripts/refusal_registry.py`, `scripts/codex_roles.py`, `scripts/host_adapter.py` | пачка 7, OH7-2 | нет | t-263 F-6; OH6-4 |
| `findings/20261113-native-context-stage-json-spisok-v-pending-padaet-bez-paketa.md` | находка, id — | pending-файл со списком JSON даёт `AttributeError`, запуск идёт без пакета; не-словарь — нечитаемый пакет | `scripts/native_context.py` | пачка 7, OH7-3 | нет | t-263 N-1; AR-28 |
| `findings/20261113-otkaz-pending-ne-nazyvaet-dver-dlya-zapuska-kotoryj-ne-startoval.md` | находка, id — | отказ pending не называет двери для не стартовавшего запуска; добавить «relaunch under a unique task name» | `scripts/native_context.py` | пачка 7, OH7-4 | нет | t-263 N-2; FR-57 |
| `findings/20261113-teksty-otkaza-test-path-how-otstali-ot-pravila-s5.md` | находка, id — | `TEST_PATH_HOW` и `HOW` говорят «inside the application tree», `s5.md` расширен B-355 J; выровнять | `scripts/guard_app_under_test.py`, `scripts/tests/test_protected_test_path.py` | пачка 7, OH7-5 | нет | B-355 |

## Входящие

`findings/` этой кучки; их число и дату последней показывает `plans/PILES.md` (собирает `piles.py board`; карточку код не правит).

## Вопросы владельцу

- B-355: добавить ли в маркеры тестовых путей `__test__`, `testing`, `integration`, `fixtures`, `_tests` (решение за владельцем, находка `findings/B-355-markery-testovykh-putey-references-test-path.md`; узел OH5-14)? Рекомендация: добавить `_tests` и `__test__`, остальные три не добавлять (называют и каталоги продукта).
- B-262: оставить автообновление плагина отложенным (слово владельца 02.10)? Рекомендация: оставить (находка `findings/B-262-avtoobnovlenie-plagina-vklyuchaetsya-samo-kak-v.md`; узел OH5-15).
