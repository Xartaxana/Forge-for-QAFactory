# Исполнение тестов и пробы (`execution-probes`)

приоритет: П2 | фичи: F11, F03 (пробы), F09 | стенд: нужен (M1–M3 на проекте) | зона: `ai-packages/qa-factory/scripts/run_suite.py`, `scripts/execution_request.py`, `scripts/node_ids.py`, `scripts/probe_by_code.py`, `scripts/red_sandbox.py`, `scripts/reporters.py`, `scripts/acceptance.py`, `scripts/window_record.py`, `scripts/gate_preflight.py`, `scripts/hooklib.py`, `references/launch-causes.json`, `references/gate-registry.json`

## Зачем

Сегодня проверка «тест действительно проверяет утверждение» уверенно работает только для Python и pytest: «какой раннер»
решают больше десяти мест по-разному, а окно, где все тесты переданы человеку, принимается по заявлению, а не по
манифесту. После первой пачки проба «проверка живая» работает на любом языке и раннере, понятие «это pytest»
определено один раз, а гейты не молчат там, где проверить нечем: они говорят «не проверено».

## Что не так сегодня (факты)

- Три предиката «это команда pytest» (`node_ids.is_pytest`, `execution_request.is_pytest_command`, `run_suite.resolve_reporter`) расходятся (`plans/BACKLOG.md:391`); две таблицы идентичности раннера и больше десяти читателей «какой раннер» (`plans/BACKLOG.md:450`).
- Окно, где все тесты переданы человеку, принимается по квитанции, а не по манифесту (`plans/BACKLOG.md:395`).
- Гейт `collected_ids` для не-pytest молчит вместо «не проверено» (`plans/BACKLOG.md:227`); `live_check_demand` без ключа `novelty` проходит как «не требуется» (`plans/BACKLOG.md:228`).
- Конфиги раннера есть в ключе репетиции, но не в отпечатке прогона; развилка Lead, решение после релиза 0.9 (`plans/BACKLOG.md:473`).
- Живое доказательство M1–M3 пробы на не-Python проекте не сделано: строка живёт в кучке `live-runs`.
- 13 открытых строк в пачке 1 и 15 находок (дайджест `docs/tasks/specs/reports/t-714-scout-piles-c.md`, пересчёт 13 из 13 и 15 из 15 на 13.10).

## Пачки

| № | Что изменится для пользователя | Строки | Размер | Статус | Взял | Ветка | MR |
|---|---|---|---|---|---|---|---|
| 1 | проба «проверка живая» работает на любом языке и раннере, один предикат «это pytest», оракул — из требований, не из кода | B-369, B-371, B-432 | M | закрыта | — | — | `855d4e5c` |
| 2 | `config_sha` считается по исполняемой конфигурации профиля: зелёный результат не выбрасывается из-за правки `qa-factory/config.json` там, где запуск теста ничего не читает (прогон TP1-14857 на 0.10.2: 31 запуск на 5 тестов) | `batch-2-config-sha-po-profilyu.md` | S (1 узел) | закрыта | dev2, 28.10.2026 | `pile/execution-probes/batch-2` | `f052c829` |

Открытое перенесено 01.11.2026 → release-next/1, words-gates/1, driver-hosts/1, execution-report/1, execution-report/2, onboarding-forge/2.

Статусы пачки: `ожидает` → `в работе` → `сдано` → `принято` → `закрыта`. Размер — по узлам: S ≤ 4 узлов,
M 5–9, L 10–15 (больше — две пачки). Взятая пачка заморожена: её файл правит только взявший, новое
по теме — файлом в `findings/`.

## Бриф пачки 1

Начать с EP1-1 (один предикат и одна таблица раннера) — на ней стоят остальные узлы; EP1-6 — решение Lead, не код.
Стенд нужен только для живого доказательства M1–M3 (его ведёт `live-runs`). Слово владельца не нужно. Подробно —
`batch-1-one-runner.md`, раздел «Бриф».

## Бриф пачки 2

Один узел EP2-1 по спеке `docs/tasks/specs/t-143-ep2-1-config-sha-per-profile.md` (rev. 3 принята 28.10.2026; rev. 7a после пяти проходов план-критика t-144..t-148; rev. 7b после критика кода t-150; узел EP2-1 сдан 28.10.2026 — 917d57af, 8a49689f): `config_sha` отпечатка прогона считается по проекции `qa-factory/config.json` на профиль запуска по правилам из `references/config-projection.json`, а не по байтам всего файла; отказ только там, где отказывает действующий контракт конфига или проекцию нельзя построить, без отката к хэшу файла. Свидетель — квитанции прогона TP1-14857: одна правка `frontend_url` перезапустила TC-005. Пачка открыта отдельно от пачки 1 по D-0044: в пачке 1 уже 21 узел (EP1-1…EP1-21), больше предела L (15). Релиз: следующий после 0.10.4, включение ждёт слова владельца. Стенд нужен только живому доказательству (§8 спеки, копия проекта TP1-14857 на `local-docker`).

## Дороги

Читать по порядку: эта карточка → `batch-1-one-runner.md` → находки узла (колонка «id / файл» ниже) → строки
`plans/BACKLOG.md` 227, 228, 391, 393, 395, 397, 400, 450, 458–460, 463, 473 → код зоны по функциям из «Слов» →
`ai-packages/qa-factory/references/launch-causes.json`, `references/gate-registry.json` →
`docs/factory-map/qa-factory-paths.md` (S5, S6, окна) → `PROJECT.md` P19, P20.
Слова: `plans/features.json` F11, F03, F09 (поле `words`) и сверх них: `is_pytest`, `is_pytest_command`,
`resolve_reporter`, `collect_forms`, `run_forms`, `instance_shas`, `probe_by_code`, `probe_defect`, `assertion_probes`,
`red_sandbox`, `rehearsal`, `input_fingerprint`, `function_sha`, `validate_window`, `assertion_reason`,
`ERROR_HEAD_PREFIXES`, `probe-copies`, `collected_ids`, `live_check_demand`, `novelty`, `reporters.assertion_site`,
`node_report_id`, `sandbox_run_directory`; «проба», «раннер», «окно», «передано человеку».
Не читать: зону `live-runs` (живые доказательства M1–M3 — там), `package-ci` (его строка про реестр гейтов для `red_sandbox.verify`), тексты ролей.

## Содержание

Снимок 13.10.2026; пути — от `ai-packages/qa-factory/scripts/`; суть строк — из `plans/BACKLOG.md`, находок — из дайджеста t-714. При расхождении авторитетна доска `plans/PILES.md`.

| id / файл | вид | суть (≤ 20 слов) | пути | статус | слово владельца | связи |
|---|---|---|---|---|---|---|
| **Один раннер, один предикат (пачка 1, EP1-1)** | | | | | | |
| B-369 | строка | три предиката «это команда pytest» свести к одному | `node_ids.py`, `execution_request.py`, `run_suite.py` | пачка 1, EP1-1 (по тексту строки входит в соседнюю строку про таблицы раннера) | нет | — |
| B-371 | строка | сверить правило поиска тест-файла в `execution_request.instance_shas` с остальными правилами каталога запуска | `execution_request.py` | пачка 1, EP1-1 | нет | — |
| B-432 | строка | свести две таблицы идентичности раннера и более десяти читателей «какой раннер» в один | `execution_request.py`, `run_suite.py`, `hooklib.py`, `launch-causes.json` | пачка 1, EP1-1 | нет | — |
| **Устройство пробы (пачка 1, EP1-2)** | | | | | | |
| B-441 | строка | остатки копии файла пробы: restore без заметки, седьмая копия блокировки, `_probe` в 206 строк, мёртвые ветки | `probe_by_code.py` | пачка 1, EP1-2 | нет | `live-runs` (M1) |
| B-442 | строка | остатки читателя кадров и таблицы проб: дрейф регистра пути, U+2028, AssertJ/Jest/NUnit, паритет | `reporters.py`, `probe_by_code.py` | пачка 1, EP1-2 | нет | — |
| B-445 | строка | реестр гейтов: строка для вердикта пробы, слова `red_sandbox` в `probe_verdicts`, детектор `probe-copies` | `red_sandbox.py`, `gate-registry.json` | пачка 1, EP1-2 | нет | `package-ci` (реестр гейтов) |
| **Красная проба с несколькими целями (пачка 1, EP1-3)** | | | | | | |
| B-377 | строка | в красной пробе с несколькими целями `probe_defect` одной цели скрывает уцелевшую мутацию другой | `probe_by_code.py`, `red_sandbox.py` | пачка 1, EP1-3 | нет | — |
| B-440 | строка | остатки: прозовые близнецы с вшитыми dotnet/karma/jest, `py.test --junitxml`, `ERROR_HEAD_PREFIXES`, приватные имена hooklib | `run_suite.py`, `hooklib.py`, `stage_guard.py` | пачка 1, EP1-3 | нет | — |
| **Приёмка окна (пачка 1, EP1-4)** | | | | | | |
| B-375 | строка | окно, где все тесты переданы человеку, не принимается по квитанции: «передано» выводить из манифеста | `acceptance.py`, `window_record.py` | пачка 1, EP1-4 | нет | — |
| B-380 | строка | запись окна S5 хранит причины как `reporters.assertion_reason`; для однострочной привязки подробностей нет | `window_record.py`, `reporters.py` | пачка 1, EP1-4 | нет | — |
| **Гейты «не проверено» (пачка 1, EP1-5)** | | | | | | |
| B-278 | строка | гейт `collected_ids`: для не-pytest «не проверено» молчит; первая половина закрыта 07.10 по тексту | `gate_preflight.py`, `node_ids.py` | пачка 1, EP1-5: проверить по коду, что осталось | нет | — |
| B-279 | строка | гейт `live_check_demand`: без ключа `novelty` проходит как «не требуется»; нужно «не проверено» в Left with you | `gate_preflight.py` | пачка 1, EP1-5 | нет | `report-delivery` |
| **Развилка Lead (пачка 1, EP1-6)** | | | | | | |
| B-458 | строка | конфиги раннера есть в ключе репетиции, но не в отпечатке прогона; решение после релиза 0.9 с замером на эталоне | `execution_request.py` | пачка 1, EP1-6 | нет (развилка Lead) | — |
| **Раннер и каталог запуска (кандидаты пачки 2)** | | | | | | |
| `findings/B-345-ne-pytest-zapusk-ostatki-posle-volny-6.md` | находка | `node_report_id` не учитывает rootdir; три правила каталога запуска; склейка `selectors.join` | `run_suite.py`, `probe_by_code.py` | открыто | нет | — |
| `findings/B-180-run-suite-py-reparse-block-beret-mapping.md` | находка | `--reparse-block` берёт `--mapping` руками; нужен режим из манифеста без лишних перегонов (FR-51) | `run_suite.py`, `red_sandbox.py` | открыто | нет | — |
| `findings/B-378-proverka-edge-5-it-shows-both.md` | находка | тест `edge 5: it shows both argvs` падает на длинных путях: upstream режет argv по 160 знакам (FR-31) | `tests/test_run_suite_mine.py` | открыто | нет | `package-ci` |
| **Проба для не-Python (кандидаты пачки 2)** | | | | | | |
| `findings/B-337-ne-pytest-proekty-rezhim-proverka-zhivaya.md` | находка | `probe_by_code` умеет только Python; нужен читатель кадров стека по среде; висящий `--logger` | `probe_by_code.py`, `reporters.py`, `node_ids.py` | основа строки в `live-runs`; часть влита 07.10 по тексту | нет | `live-runs` |
| `findings/B-443-b-373-c-lekser-izvestnye-predely-proby.md` | находка | лексер пробы: `/` в начале строки, JSX с апострофом, вложенные кавычки в `${}`; строка для живого прогона | `probe_by_code.py` | открыто | нет | `live-runs` |
| `findings/B-321-pesochnitsa-krasnykh-prob-vo-vlozhennom-proekte.md` | находка | `red_sandbox.artifact_prefixes` ищет конфиг только в `<repo>/qa-factory/config.json` | `red_sandbox.py` | открыто | нет | `driver-controller` (подпапка git) |
| `findings/B-255-analogi-obeshchannye-priemkami-t-279-t-287-kak-b.md` | находка | аналоги, обещанные приёмками: вторая копия проверки пробы, дубль подготовки ctx, текст `PASTE_SHAPE` (пункты а–ж) | `probe_by_code.py`, `gate_preflight.py` | пункты (а), (е), (ж) переданы в узлы по тексту — проверить по коду | нет | — |
| **Приёмка окна и честность «проверено» (кандидаты пачки 2)** | | | | | | |
| `findings/B-179-progon-cmp1-s5-vse-stroki-blokov.md` | находка | cmp1, S5: окно без терминальных результатов принято; проверить, что окно требует `passed` по строкам блока | `window_record.py`, `acceptance.py` | передано в узел t-302 G10 по тексту — проверить по коду | нет | — |
| `findings/B-217-otpechatok-tela-testa-function-sha-slep-k.md` | находка | `function_sha` слеп к модулю данных проекта: ожидаемое значение меняется после красного прогона незаметно | `execution_fingerprint.py` | передано в узел t-302 T6 по тексту — проверить по коду | нет | — |
| `findings/B-168-exit-gate-py-796-804-esli-khost-prisylaet-input.md` | находка | `exit_gate.py` отпускает расписку «incomplete» без перепроверки при неизменном `input_fingerprint` | `exit_gate.py` | открыто | нет | — |
| `findings/B-323-exit-gate-py-466-469-proveryaet-vse-bagi-proekta.md` | находка | `exit_gate.py` проверяет баги всего проекта: сломанный чужой баг блокирует эту историю | `exit_gate.py` | открыто | нет | — |
| **Бейзлайн и лестница P19 (отложено владельцем «после релиза»)** | | | | | | |
| `findings/B-269-beyzlayn-do-izmeneniya-dlya-ruchnoy-proverki.md` | находка | бейзлайн «до изменения» для ручной проверки: машинерия спит; нужны сценарии A–F и лестница добычи «до» | `skills/qa-story/phases/s6.md` | отложено: «до релиза не делаем» (метка «после релиза» — релиз 0.9 состоялся? проверить) | да, 02.10 17:25: до релиза не делаем | — |
| `findings/B-281-geyt-baseline-identity-t-302-g15-gotovnost.md` | находка | гейт `baseline_identity` «советует, не решает»; сделать `refuse_with_door` вместе с бейзлайном | `baseline_contract.py` | идёт вместе с бейзлайном | нет | — |
| `findings/B-283-geyt-reporter-rehearsal-identity-t-302-f9.md` | находка | `reporter_rehearsal_identity`: при `unknown` идентичности стенда репетиция считается «той же»; должно быть `rerun` | `gate_preflight.py` | открыто (метка «после t-300 N3») | нет | `stand-and-sources` |
| `findings/B-227-lestnitsa-vybora-sposoba-proverki-vladelets-30.md` | находка | лестница выбора способа проверки (P19): у ступеней 3 и 5 есть исполнитель, запись и видимость в отчёте | — | открыто | нет | `report-delivery` |
| `findings/20261021-skrinshot-dokazatelstvo-svezhest-i-png.md` | находка | скриншот-доказательство проверяется: mtime не раньше старта прогона, валидный PNG, папка прогона; байт-дубликат чужого прогона — строка отчёта, не отказ | — | EP1-7, ожидает | нет | обзор testing-factory (K6) |
| `findings/20261022-otpechatok-padaet-na-forme-iz-svoej-spravki.md` | находка | `execution_fingerprint.py` падает с `TypeError` на спеке формы `{path, sha256}` из своей же карточки роли; S5 встал до первого теста | `scripts/execution_fingerprint.py`, `references/role-commands.json` | EP1-8, ожидает | нет | OH3-10 (ошибка фабрики в бэклоге проекта) |
| `findings/20261022-chitatel-node-id-ostanavlivaetsya-na-bannere.md` | находка | читатель node id обрывается на баннере `====` до списка тестов: ноль id, отказ всем тестам; второй парсер того же вывода на гейте A | `scripts/node_ids.py`, `scripts/gate_preflight.py` | EP1-9, ожидает | нет | EP1-8, OH3-10 |
| `findings/20261022-ui-testy-probuyutsya-pod-api-profilem.md` | находка | UI-тесты пробуются под профилем `api`: общий корень у двух профилей, селектор молча берёт первый; закрытие окна не читает слово человека | `execution_request.py`, `probe_by_code.py`, `window_record.py` | EP1-10, ожидает | нет | GW1-14, EP1-9 |
| `findings/20261023-sobstvennyj-collect-gejta-dublirovan-bez-povtorov.md` | находка | собственный запуск collect репетиции гейта дублирует `node_ids.collect` без повторов `-qq` и дерева | `scripts/gate_preflight.py`, `scripts/node_ids.py` | перенос: speed-cost/1 (SC1-12) | нет | EP1-9, t-053 A4 |
| `findings/20261023-koren-testov-profilya-chitaetsya-v-trekh-mestakh-po-svoemu.md` | находка | принадлежность пути корню тестов профиля читается в трёх местах по-своему; безымянная строка под чужим единственным корнем идёт под именованным профилем | `probe_by_code.py`, `gate_preflight.py`, `execution_request.py` | EP1-12, ожидает | нет | EP1-10, t-055 C2/C7 |
| `findings/20261023-ostatki-then-ostatka-dva-chitatelya-nomera-i-tag-v-dvuh-fajlah.md` | находка | номер Then читают два приватных читателя, метка ожидающей находки живёт в двух файлах; `judge_code.py:125` в дереве уже со `try/except` | `contract.py`, `s5_precheck.py`, `judge_code.py`, `exit_gate.py` | EP1-13, ожидает | нет | GW1-14, t-059, t-067 |
| `findings/20261023-sopostavlenie-slova-s-instansom-probela-v-dvuh-mestah-i-dvojnik-v-draivere.md` | находка | сопоставление слова человека с экземпляром пробела пробы написано дважды; двойник `story_run.Driver.window_gap` и `_caller_pair_reason` не знают `probe_gap` | `window_record.py`, `acceptance.py`, `story_run.py`, `story_step.py` | EP1-14, ожидает | нет | EP1-10, t-069, conductor/1 |
| `findings/20261024-net-finalnogo-progona-finalnyh-fajlov.md` | находка | правка общей фикстуры после последнего прогона замечена (D-0017), но пять API-тестов 12586 ушли человеку вместо перепрогона фабрикой | `acceptance.py`, `window_record.py`, `proof_level.py` | EP1-15, ожидает | да (24.10: переименование не косметика, меняет `code_sha`, нужен перепрогон) | t-1207; TQ1-9 |
| `findings/20261024-proba-mutacii-ne-peredaet-profil.md` | находка | мутационная проба не запускается при двух профилях на общем корне: `build_request` не передаёт `profile_id`, отказ называет несуществующую дверь `--profile` | `probe_by_code.py`, `execution_request.py`, `red_sandbox.py` | EP1-16, ожидает | — | t-1220; EP1-10; HF1-14 |
| `findings/20261025-s5-zapusk-testa-20-minut-obvyazki.md` | находка | S5 часами: 20 мин обвязки запуска на 20 с тестов (двойной collect, тройная проба); поля строки манифеста роль узнаёт из отказа | `run_suite.py`, `execution_request.py`, `window_record.py`, `manifest_from_tests.py`, `s5_precheck.py` | EP1-17, EP1-18, ожидает | вопрос 24–25.10.2026 (поведение) | t-1221; GW1-22; DC1-9; CD1-14 |
| **Находки прогона 14857 (0.10.2), 27.10.2026** | | | | | | |
| `findings/20261027-forma-zaprosa-proby-ne-sverena-s-kontraktom-sdk.md` | находка | A3: форма запроса пробы ранера не сверяется с контрактом SDK; снятое утверждение TC-006 (калибровка) | `agents/qa-runner.md` | пачка 1, EP1-19 | нет | FB-13 |
| `findings/20261027-dobavlennyj-test-s-effektom-importa.md` | находка | добавленная тестовая функция с эффектом при импорте прощается идентичностью по функции; сомнение должно читаться «изменилось» | `proof_level.py`, `execution_request.py` | пачка 1, EP1-20 | нет | t-1395 Q-b; EP1-15 |
| `findings/20261027-chetyre-kopii-is-code-file-ili-pol.md` | находка | проверка «`is_code_file`, иначе пол расширений» в четырёх копиях; свести в один помощник `test_files` | `test_files.py`, `arch_check.py`, `gate_preflight.py`, `runtime_probe.py` | пачка 1, EP1-21 | нет | t-1390 D-3, Q-2 |
| **Отзыв пользователя, 28.10.2026** | | | | | | |
| `findings/20261028-playwright-junit-otchet-ne-chitaetsya.md` | находка | Playwright Test (JS): отчёт JUnit не читается — `{report_path}` в команде, путь только из env/конфига, проба сканирует весь каталог; S6 целиком вручную | `execution_request.py`, `onboarding_probe.py`, `run_suite.py`, `gate_preflight.py`, `report-cures.json` | пачка 1, EP1-22 | П1 релиза 0.10.7: «Приоритет 1. Берём в следующий релиз» (28.10.2026) | отзыв Dev6 (TP2-2702), t-1553; B-337, B-345 |
| **Прогон TP1-12586 на 0.10.5, 29.10.2026 (скорость S5)** | | | | | | |
| `findings/20261029-zapusk-mine-vsyo-eshchyo-dve-minuty.md` | находка | `run_suite --mine` после 0.10.2 всё ещё 104–140 с на 5–13 с тестов: collect при известных id, работа после прогона | `run_suite.py`, `execution_request.py` | пачка 1, EP1-23 | П1 0.10.7: «переносим к нам в релиз все пункты… которые ускоряют работу» (29.10.2026) | EP1-17; SC2-37 |
| `findings/20261029-runtime-probes-ne-zapisany-do-s5.md` | находка | `execution.runtime_probes` не записан до S5: первый запуск отказан, автоматор пишет пробу сам, `--write` 180 с | `runtime_probe.py`, `onboard_apply.py`, `gate_preflight.py` | пачка 1, EP1-24 | П1 0.10.7 (то же слово) | HF8-9…HF8-14; OH3-26…31 |
| `findings/20261029-forma-markera-qa-uznayotsya-iz-otkazov.md` | находка | форму маркера `qa` и модуль параметров автоматор узнаёт из отказов по одному; окно 2 повторяет отказ окна 1 | `manifest_from_tests.py`, `brief_pack.py`, `agents/qa-automator.md` | пачка 1, EP1-25 | П1 0.10.7 (то же слово) | HF2-12; SC1-15 |
| **Находки ночного прогона 14857 (0.10.6), 30.10.2026** | | | | | | |
| `findings/20261030-vozmozhnost-stenda-planirovshchik-ne-proveryaetsya-do-s5.md` | находка | возможность стенда (планировщик для cron) не проверяется до S5: S7 узнаёт, что её нет (TC-003) | `scripts/runtime_probe.py`, `scripts/gate_preflight.py`, `scripts/s5_precheck.py` | пачка 1, EP1-26 | нет | EP1-24; `stand-and-sources`; t-1605 #15 |
| `findings/20261030-npx-cmd-subprocess-winerror2.md` | находка | `npx` (`.cmd`) на Windows не запускается без оболочки: проба гейта и `run_suite` дают WinError 2, хотя `shutil.which` запуск находит; нужен один разрешатель на оба вызова (вилка Lead) | `scripts/gate_preflight.py`, `scripts/run_suite.py` | пачка 1, EP1-27 | нет | EP1-22; находка про Playwright (28.10) |
| **Находки 31.10.2026 (вопрос владельца о desktop и mobile)** | | | | | | |
| `findings/20261031-desktop-i-mobile-prilozheniya-bez-ruk-i-bez-gotovnosti-stenda.md` | находка | desktop/mobile: набор запустится командой профиля (не доказано), но готовность стенда только web/API, руки агента только HTTP и браузер | `scripts/manual_capture.py`, `scripts/readiness.py`, `skills/qa-onboarding/` | пачка 1, EP1-41 | да, 31.10.2026: «баг первого приоритета» | XT (`exploratory`): исследование не-web; EP1-25 |
| **Находки 31.10.2026 (прогон CART-1, MyBooks)** | | | | | | |
| `findings/20261031-stend-bez-docker-ruchnaya-proverka-ne-sprashivaet-versiyu.md` | находка | стенд без docker: `manual_capture` ищет зашитые профили `api`/`e2e-ui` и уходит в `env_blocked` вместо вопроса «та ли версия на стенде» | `scripts/manual_capture.py`, `scripts/runtime_probe.py`, `scripts/stand_identity.py` | пачка 1, EP1-28 | да, 31.10.2026: «спросить пользователя, правильная ли версия на стенде» | EP1-24 (тот же `--suggest`); EP1-41 |
| `findings/20261031-vvod-s-klaviatury-po-simvolu-v-keysah-i-ruchnoj-proverke.md` | находка | поле ввода проверяется `fill`, а не набором с клавиатуры: баг «нельзя набрать 12» (Б-1) невидим; слова шага `type`, `press`, `paste` и правило дизайна кейса | `scripts/manual_capture.py`, `references/manual-capture-steps.json`, `agents/qa-case-designer.md` | пачка 1, EP1-29 | да, 31.10.2026 (W3): «чтобы фабрика сама нашла все эти 3 бага» | EP1-30; `exploratory` Н-6 |
| `findings/20261031-otkaz-zavisimosti-v-ruchnoj-proverke-ui.md` | находка | ручная проверка `ui` не умеет «отказ зависимости» (Б-2, Б-4): слово шага `fail_request` подменяет ответ запроса страницы | `scripts/manual_capture.py`, `references/manual-capture-steps.json`, `agents/qa-runner.md` | пачка 1, EP1-30 | да, 31.10.2026 (W3) | EP1-29; `grounding` Н-3; `exploratory` Н-6 |
| `findings/20261031-recept-vhoda-ruchnoj-proverki-testproject1-a-onboarding-vyuchil-svoj.md` | находка | рецепт входа `http` и `ui` — умолчание Test Project 1; вход проекта, выученный онбордингом, до `manual_capture` не доходит (4.3+4.4, ответ на W4) | `scripts/manual_capture.py`, `scripts/config_contract.py`, `skills/qa-onboarding/` | пачка 1, EP1-31 | да, 31.10.2026 (W4): «разве это не устанавливается на онбординге?» | B-252 (`forge`); `onboarding-hooks` (вход по логину); EP1-28 |
| `findings/20261031-chtenie-bulevogo-atributa-ne-razlichaet-sostoyaniya.md` | находка | `read attr=disabled` даёт `""` для включённой и выключенной кнопки; «неактивна» записано `passed` по подписи (4.5) | `scripts/manual_capture.py`, `scripts/manual_evidence.py`, `agents/qa-runner.md` | пачка 1, EP1-32 | нет | EP1-29, EP1-30 |
| `findings/20261031-gard-ne-daet-prochitat-skrinshot-ruchnoj-proverki.md` | находка | гард «большой файл целиком» не даёт роли прочитать собственный PNG (118 КБ > 30 КБ), дверь «диапазоном» к картинке неприменима (4.6) | `scripts/guard_pre_tool.py` | пачка 1, EP1-33 | нет | EP1-7 (скриншот-доказательство) |
| `findings/20261031-stend-zagryaznyaetsya-i-dolg-sredy-zapisan-bez-slova-cheloveka.md` | находка | следы фабрики на стенде нигде не перечислены кодом; `env-debt` OB-6 записан без слова человека вопреки правилу файла (4.7) | `scripts/manual_capture.py`, `scripts/report_facts.py`, `references/templates/obligations.md` | пачка 1, EP1-34 | нет | EP1-31; `report-delivery`; `stand-and-sources` |
| `findings/20261031-raner-ne-zapuskaet-npx-na-windows.md` | находка | раннер запускает `argv` без разрешения `.cmd`: `npx` на Windows даёт `WinError 2` и ложное «нет программы» (4.8, FB-3 проекта) | `scripts/hooklib.py`, `scripts/run_suite.py`, `scripts/gate_preflight.py`, `scripts/onboarding_probe.py` | пачка 1, EP1-35 | нет | EP1-22 (Playwright JUnit); `onboarding-hooks` |
| `findings/20261031-proba-chuvstvitelnosti-ne-chitaet-playwright-ts-18-iz-18.md` | находка | проба «тест умеет падать» не читает Playwright TypeScript: 18 из 18 не пробованы, 16 требований не доказаны, человек трижды принимает пробел (5.1) | `scripts/probe_by_code.py`, `references/detectors.json`, `scripts/onboarding_probe.py` | пачка 1, EP1-36 | нет (П1 по своду Lead) | EP1-37, EP1-22, EP1-12; `hotfix-12586/findings/20261028-proba-ne-nahodit-test-s-parametrom-plagina.md`; `gates-and-words` 3.3 |
| `findings/20261031-playwright-ts-ne-chitaetsya-manifestom-selektorom-i-detektorom.md` | находка | манифест, селектор запуска и детектор «изменено после красного» знают только python; роли строят идентификаторы руками (5.2+5.3+5.6, склейка) | `scripts/manifest_from_tests.py`, `scripts/execution_request.py`, `scripts/run_suite.py`, `scripts/proof_level.py`, `scripts/report_facts.py` | пачка 1, EP1-37 | нет | EP1-1, EP1-22, EP1-25, EP1-36 |
| `findings/20261031-s5-precheck-ne-nahodit-fajly-keysov-i-ne-znaet-myagkih-proverok.md` | находка | `s5_precheck` не находит файлы кейсов (автор копирует и считает хэш сам); Then после красного отвергается даже при мягких проверках (5.4+5.5, склейка) | `scripts/s5_precheck.py`, `scripts/manifest_put.py`, `references/detectors.json` | пачка 1, EP1-38 | нет | EP1-13, EP1-37 |
| `findings/20261031-manifest-put-stiraet-tests-pri-povtornoj-otpravke-unresolved.md` | находка | `manifest_put`: строка `unresolved` с `thens` без `instance_ids` читается «весь кейс» и стирает `tests[]`; 4 лишних диспатча (5.7) | `scripts/manifest_put.py`, `scripts/contract.py` | пачка 1, EP1-39 | нет | `driver-controller` (колпак раундов, квитанция критика); EP1-38 |
| `findings/20261031-pravka-testa-vne-skoupa-okna-ne-perepogonyaetsya-v-okne.md` | находка | `run_suite --mine` отказывает перепрогнать тест другого кейса, который окно само изменило; хэши автор правит рукой (5.8) | `scripts/stage_guard.py`, `scripts/manifest_put.py`, `agents/qa-automator.md` | пачка 1, EP1-40 | нет | EP1-39; `driver-controller` (кап окна) |
| **Очередь релиза 0.10.8 (критики t-555, t-561, t-565; t-567)** | | | | | | |
| `findings/20261031-bearer-env-bez-dveri-zagolovok-avtorizacii-otkazyvaetsya.md` | находка, id — | `bearer_env`: дверь ведёт на `login.http`, заголовок `Authorization` отказывает скан секретов; код ставит заголовок сам (t-561 Ф-9 а) | `scripts/manual_capture.py`, `references/manual-capture-steps.json` | EP1-42, ожидает | нет | EP1-31 |
| `findings/20261031-role-commands-ui-read-bez-state.md` | находка, id — | карточка `manual_capture.py ui` не знает `read … state=<name>` | `references/role-commands.json` | EP1-43, ожидает | нет | EP1-32 |
| `findings/20261031-run-history-function-identity-znaet-tolko-py.md` | находка, id — | `_function_identity` знает только `.py`; TS-тест не подтверждает красный (t-565 E-10) | `scripts/run_history.py`, `scripts/import_test_receipt.py` | EP1-44, ожидает | нет | EP1-37, EP1-36 |
| `findings/20261031-okno-vhoda-zakryvaetsya-rano-na-chuzhom-adrese.md` | находка, id — | окно входа закрывается рано на чужом адресе страницы входа (t-506 §10) | `scripts/manual_capture.py` | EP1-45, ожидает | нет | EP1-31 |
| `findings/20261031-obligation-hash-ustarevshij-posle-patcha-refs.md` | находка, id — | устаревший `obligation_hash` после патча `refs` (t-555 F-9) | `scripts/probe_by_code.py`, `scripts/manifest_put.py` | EP1-46, ожидает | нет | EP1-38, EP1-36 |
| `findings/20261101-test-source-bez-publichnogo-read-text-i-dlinnye-funkcii.md` | находка, id — | нет публичного `test_source.read_text`; `run_carry` (~80 строк) и `_judge_detector_rows` (~70) над порогом (t-596 F-11) | `scripts/test_source.py`, `scripts/probe_by_code.py`, `scripts/waiver.py` | EP1-47, ожидает | нет | EP1-36 |
| `findings/20261101-words-of-appium-svoj-entity-guard-ryadom-s-prolog-state.md` | находка, id — | `AppiumBackend.words_of` держит свою защиту от `<!entity` рядом с `reporters._prolog_state` (t-599 F-13) | `scripts/manual_capture.py`, `scripts/reporters.py` | EP1-48, ожидает | нет | EP1-41 |
| **Обзор MR !12, 01.11.2026** | | | | | | |
| `findings/20261101-zavisimosti-python-testa-chitayutsya-neskolkimi-chitatelyami.md` | находка, id — | зависимости Python-теста (импорты и `conftest`) читаются несколькими читателями с разными границами; одна функция-выживший | `scripts/copy_detector.py`, `scripts/execution_request.py`, `scripts/manifest_from_tests.py`, `scripts/probe_by_code.py`, `scripts/s5_precheck.py` | пачка 1, EP1-49 | нет | t-1644 M2; EP1-48 |

## Входящие

`findings/` этой кучки; их число и дату последней показывает `plans/PILES.md` (собирает `piles.py board`; карточку код не правит).
По теме в других кучках: `live-runs/findings/B-373-pereotkryto-06-10-2026-d-0025.md` (остаток строки M1–M3 лежит там).

## Вопросы владельцу

- нет (основание: «Решение владельца нужно: да» — 0 из 15 находок, дайджест t-714 п. 5; бейзлайн отложен словом 02.10, развилка по конфигам раннера — Lead).
