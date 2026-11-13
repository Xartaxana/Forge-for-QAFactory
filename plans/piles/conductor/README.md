# Дирижёр: принцип P22 (`conductor`)

приоритет: П1 | фичи: F06, F07, F17, F05, F12, F13 | стенд: нужен | зона: `ai-packages/qa-factory/scripts/story_run.py`, `scripts/controller.py`, `scripts/repair_route.py`, `references/conductor*.{md,json}`, `references/human-questions.md`, `skills/qa-story/**`

## Зачем

Сегодня фабрика в непредвиденном состоянии ведёт себя по-разному на каждой стадии: где-то молча идёт дальше, где-то
останавливается и просит человека выполнить команду руками, где-то спрашивает человека без вариантов и без цены, а
дирижёра либо не зовут, либо зовут и запрещают ему действовать. Слово владельца 09.10 (P22, D-0039): если фабрика с
чем-то не справляется, чего-то не понимает или не может — она зовёт дирижёра, он предлагает человеку всё, что
позволяет продолжить (идти дальше как есть, перезапустить нужные стадии, настроить, помочь, получить доступ или
данные) с ценой и последствиями для человека и стори по каждому варианту, исполняет выбранное и пишет находку;
прогон не страдает. Обход всех стадий по коду — отчёт скаута t-621 (`docs/tasks/specs/reports/t-621-scout-p22-walk.md`):
58 мест классов 2–5 на S0–S9, гейтах A/B и доставке; единого шва нет — пять прямых вызовов дирижёра, ~40 прямых
вопросов человеку мимо дирижёра, 42 `Refusal`, 9 `Stop`, 63 молчаливых вызова скриптов без проверки, ~100
`StateConflict` в контроллере; форма вопроса (`human-questions.md`) цены и последствий не требует.

## Пачки

| № | Что изменится для пользователя | Строки | Размер | Статус | Взял | Ветка | MR |
|---|---|---|---|---|---|---|---|
| 1 | фабрика в любом непредвиденном состоянии зовёт дирижёра, он предлагает варианты с ценой и последствиями и исполняет выбранное; ни одного «выполните команду руками» и ни одного молчаливого прохода | — (B-331 остаётся в `driver-controller`, узел C1-6 ссылается на находку) | L | закрыта | владелец, 09.10.2026 | `pile/conductor/batch-1` | `21cf87e6` |
| 2 | находка из прогона чинится классом: отказ показывает весь список за один ход, слово человека ложится во все носители одной дверью, роль возобновляется только ради суждения, пропуск мимо отказа отклоняется, фабрика не спрашивает о заведомо невозможном | — (классы K1–K9 отчёта t-718, слово владельца 13.10.2026 20:58; открытые id подстрочного сравнения остаются в `gates-and-words`, возобновлений — в `driver-controller`) | M | закрыта | владелец, 13.10.2026 | `pile/conductor/batch-2` | `e981cb86` |
| 3 | долги прогона cmp3gb и слияния b1: доказательство гейта B возобновляется после C2-3, записанные раунды последнего окна исполняются или S5 закрывается кодом, шов C2-3s, S5-блок одним решением класса, аналоги K3 и тетрадей cmp3/cmp3gb | — (находка `findings/20261014-krasnyy-test-bez-proby-zapiraet-s5.md`; t-758 находки 1, 6, 8; t-751 m6; t-752 §L N7; t-721 §L-6) | M | закрыта | — | `pile/conductor/batch-3` | `855d4e5c` |
| 4 | входящие после взятия пачки 3: молчаливый проход гейта S6–S8 без манифеста автоматизации, красный медленный тест на `main`, очереди решений Lead из спек C3-x (t-853, t-860, аналоги C3-20) | — | S | закрыта | — | `pile/conductor/batch-4` | `3338f2e7` |
| 5 | входящие после закрытия пачки 4: очереди приёмки C1-6/C1-7 — две другие дороги reopen перезапускают held-работу без вопроса, вопросы `build_check` без цен | `batch-5-vhodyashchie-3.md` | S | закрыта | — | `pile/conductor/batch-5` | `855d4e5c` |

Открытое перенесено 01.11.2026 → words-gates/1, driver-hosts/1, execution-report/1, live-runs/2, driver-hosts/2, execution-report/2, onboarding-forge/2.

## Бриф пачки 2

- В cmp3 каждая из девяти находок оказалась классом (одна ошибка на нескольких стадиях и у нескольких агентов), не местом; пачка чинит классы K1–K9 по таблицам сайтов отчёта t-718.
- Узлы C2-1…C2-9: весь список за один ход, одно решение человека во все носители одной дверью, роль — только ради суждения, блок мимо отказа отклонён, токен и запасной вопрос несут слова, код-закрытие стадии получает ход, никаких вопросов о заведомо невозможном.
- Полный бриф, порядок по файлам и критерий узла — `batch-2-cmp3-classes.md` (преамбула и `## Бриф`).

## Дороги

Читать по порядку: эта карточка → файл пачки, которую ведут (`batch-3-vhodyashchie.md` копится; `batch-2-cmp3-classes.md` и
`batch-1-p22-seams.md` в работе) → находка узла (колонка «id / файл» ниже) → отчёты:
`docs/tasks/specs/reports/t-621-scout-p22-walk.md` (58 мест классов 2–5), `docs/tasks/specs/reports/t-718-class-walk-cmp3.md`
(классы K1–K9 и таблицы сайтов), спеки узлов `docs/tasks/specs/t-721-c2-3-4-one-door.md`,
`docs/tasks/specs/t-745-c2-8-code-close.md`, `docs/tasks/specs/t-752-c2-9-unreachable-once.md` → код зоны по функциям из «Слов»
(`ai-packages/qa-factory/scripts/story_run.py`, `controller.py`, `repair_route.py`, `references/conductor*.{md,json}`,
`references/human-questions.md`, `skills/qa-story/**`) → правила: `PROJECT.md` принцип P22, `ai-packages/qa-factory/design/factory-rules.md`
FR-42, FR-48, FR-57.
Слова: `plans/features.json` F06, F07, F17 (поле `words`) и сверх них: `Refusal`, `Stop`, `Person`, `guarded`, `take_answer`,
`take_seam_answer`, `handle_refusal`, `s0_receipt`, `stage_done`, `rework --reason`, `handed_to_person`,
`window_shape_errors`, `rerun_after`, `record_gaps`, `human-questions`; «шов», «нет хода», «дирижёр», «цена и последствия».
Не читать: код стадий вне узла, зону `driver-controller` (кроме находок, которые узлы называют по имени), журналы
`logs/journal/*.jsonl`.

## Содержание

Снимок 15.10.2026; пути — от `ai-packages/qa-factory/` (вне пакета — от корня репозитория); суть находок — из их файлов. При расхождении авторитетны файлы пачек. Находка без строки в файле пачки — базовая линия детектора (е) `piles.py check`.

| id / файл | вид | суть (≤ 20 слов) | пути | статус | слово владельца | связи |
|---|---|---|---|---|---|---|
| **Пачка 1** | | | | | | |
| B-331 | строка | остаётся в `driver-controller`: перезапуск открытой стадии закрытой истории; узел C1-6 ссылается на находку | `scripts/controller.py` | пачка 1, ссылка из C1-6 | решено 09.10: вопрос человеку перед перезапуском | `driver-controller` |
| `findings/20261009-run-ne-lovit-refusal-vne-guarded.md` | находка | `run()` драйвера не ловил `Refusal` вне `guarded`: отказ заканчивался трассировкой, а не вопросом | `scripts/story_run.py` | пачка 1, C1-1 | нет | — |
| `findings/20261013-gejt-vyhoda-otkazal-dvazhdy-u-dirizhera-net-hoda.md` | находка | гейт выхода отказал после лимита возобновлений: у дирижёра нет хода, человек получает общий вопрос | `scripts/story_run.py`, `scripts/stage_done.py` | пачка 1, «Остатки» (сделано: t-764, C1-5d1/d2) |
| `findings/20261016-gejt-s6-s8-prohodit-molcha-bez-manifesta-avtomatizacii.md` | находка | гейт S6–S8 проходит молча без манифеста автоматизации: `read_json` → `{}`, правило нечего не находит (критик t-874) | `scripts/stage_guard.py`, `scripts/refusal_registry.py` | пачка 4, C4-1 | нет | — |
| `findings/20261016-test-gate-preflight-krasnyj-na-main-s5-profiles.md` | находка | `test_gate_preflight` красный на `main` 982/983 — медленный тест, CI `--fast` не гоняет; диагноз и `defect_found` | `scripts/story_step.py`, `scripts/gate_preflight.py` | пачка 4, C4-2 | нет | — |
| `findings/20261016-waiver-is-own-form-ne-znaet-imen-blokov-chitaemyh-kodom.md` | находка | писатель K4 отвергает имена блоков, которые читает код («keep it local», «executor unavailable:») — скрытый дефект C2-5s (билдер t-875) | `scripts/waiver.py` | пачка 4, C4-3 | нет | — |
| `findings/20261016-c3-11-ostatki-kritika-t-876-generator-i-bratya-klassa.md` | находка | остатки C3-11: генератор карты без двух маршрутов `BY_SEGMENT` (шесть циклов, строка `prepare`); братья класса K1 вне контроллера | `tools/controller-blocks-gen.py`, `scripts/controller.py`, `scripts/session_handoff.py` | пачка 4, C4-4 и C4-5 | нет | — |
| `findings/20261016-driver-for-chdir-v-udalyaemyj-proekt-klass-testov.md` | находка | `driver_for` оставляет процесс в удалённой папке проекта — на Linux следующий тест падает (класс всех `test_story_run_*.py`; CI 7925296) | `scripts/tests/story_run_common.py`, `scripts/tests/harness.py` | пачка 4, C4-6 | нет | — |
| `findings/20261016-sorted-po-path-zavisit-ot-platformy-klass-obhodov-paketa.md` | находка | `sorted(<Path>)` платформенный: порядок отказов/отчётов разный на Windows и Linux — класс ~25 обходов (CI 7925427, t-887) | `scripts/contract.py`, `scripts/session_handoff.py`, `scripts/exit_gate.py` | пачка 4, C4-7 | нет | — | чинить в пачке 1, 13.10 | — |
| `findings/20261016-own-form-blocks-i-block-names-odin-klass-dannyh.md` | находка | `OWN_FORM_BLOCKS` и `block-names.json` — один класс «имена, на которые действует читатель», две таблицы (критик t-894 F-4) | `scripts/waiver.py`, `references/block-names.json` | пачка 4, C4-8 | нет | — |
| `findings/20261016-tri-parsera-prefiksa-executor-unavailable.md` | находка | три парсера префикса `executor unavailable:` читают значение по-разному — один помощник в `contract` (критик t-894 F-5) | `scripts/contract.py`, `scripts/waiver.py` | пачка 4, C4-9 | нет | — |
| `findings/20261016-c4-4-ostatki-kritika-t-893-marshrut-stateconflict-i-shestikratnyj-cikl.md` | находка | остатки критика t-893 по C4-4: маршрут `StateConflict` с двумя хозяевами, шестикратный цикл ниже порога храповика, вложенность, крах `issubset`, цепочка gate-A без `_noted` | `scripts/controller.py`, `tools/controller-blocks-gen.py` | пачка 4, C4-10 | нет | — |
| `findings/20261016-test-story-run-words-krasnyj-na-main-vtoroj-sajt-words.md` | находка | `test_story_run_words` красный на `main` 93/95: второй сайт `"--words"` в `story_run.py`; диагноз `git log -S`, `defect_found`, починка (билдер t-889) | `scripts/story_run.py`, `scripts/tests/test_story_run_words.py` | пачка 4, C4-11 | нет | — |
| `findings/20261016-ostatki-klassa-poryadka-render-case-appendix-selftest-otlozhennye-sajty.md` | находка | остатки класса порядка после C4-7: `render_case_appendix.py:27` без регистра, 8 сайтов `selftest.py`, отложенные `controller.py`/`story_run.py` (критик t-896 F-2/F-4) | `scripts/render_case_appendix.py`, `scripts/selftest.py`, `scripts/controller.py`, `scripts/story_run.py` | пачка 4, C4-12 | нет | — |
| `findings/20261016-glob-na-windows-bez-ucheta-registra-klass-prinadlezhnosti.md` | находка | `Path.glob/rglob` на Windows без учёта регистра: класс принадлежности обхода (критик t-896 F-3) | `scripts/s5_precheck.py`, `scripts/handoff_check.py`, `scripts/judge_results.py`, `scripts/dashboard_refresh.py` | пачка 4, C4-13 | нет | — |
| `findings/20261016-gate-prices-approve-bez-words-file-i-stuby-record-by-code.md` | находка | `gate_prices` ценит `approve` без `asked.words_file`; стабы `record_by_code` с жёсткой сигнатурой (билдер t-884) | `scripts/story_run.py`, `scripts/tests/test_story_run_refusals.py`, `scripts/tests/test_story_run_delivery_b.py` | пачка 4, C4-14 | нет | — |
| `findings/20261010-ci-krasnyj-test-no-real-claude-pin-do-c1-1.md` | находка | CI красный на `main` после C1-1: `test_no_real_claude.py` пинил поведение до шва, теста не было в DoD узла | `scripts/tests/test_no_real_claude.py` | не названа в файле пачки (базовая линия) | нет | — |
| `findings/20261010-flagi-zapuska-teryayutsya-na-kazhdom-voprose.md` | находка | флаги запуска теряются на каждом вопросе человеку; скаут видит «Launch flags: none» после ответа | `scripts/story_run.py` | не названа в файле пачки (базовая линия) | нет | — |
| `findings/20261010-ledger-kritika-sbrasyvaetsya-pri-stale.md` | находка | собственный леджер критика кода обнуляется, когда его диспатч помечен `stale` | `scripts/story_run.py` | не названа в файле пачки (базовая линия) | нет | — |
| `findings/20261010-record-gaps-chitaet-slova-cheloveka-spiskom-fraz.md` | находка | `record_gaps` читает слова человека списком фраз — нарушение FR-12 | `scripts/story_run.py` | не названа в файле пачки (базовая линия) | нет | — |
| **Пачка 3 (ожидает)** | | | | | | |
| `findings/20261014-krasnyy-test-bez-proby-zapiraet-s5.md` | находка | красный тест без пробы запирает S5: у дирижёра нет хода «отдано человеку» | `scripts/story_run.py`, `scripts/controller.py` | пачка 3, C3-1; текст пачки 1 | нет | — |
| `findings/20261014-k1-sosedi-vne-owns.md` | находка | K1-соседи вне owns узла C2-1: `readiness.py:660`, `story_step.py:273`, `story_run.py:1501` режут списки находок | `scripts/readiness.py`, `scripts/story_step.py`, `scripts/story_run.py` | пачка 3, C3-8 | нет | — |
| `findings/20261015-kontroller-stray-po-golomu-id-protiv-klyucha-skoupa.md` | находка | контроллер сверяет ключ скоупа с голыми id `case_ids`: пустой кейс с ключом-областью всегда «stray» (после C2-3 запирает `decide --hand`) | `scripts/controller.py`, `scripts/story_step.py` | пачка 3, C3-12 | нет | — |
| `findings/20261015-c2-3-ostatki-kritika-t-826.md` | находка | C2-3 (ядро) — остатки критика t-826: профильная фикстура `_hand_detail`, вынос дверных тестов в `test_story_decide.py`, F4/F7/F9/F10/F11 | `scripts/story_step.py`, `scripts/tests/test_story_step.py` | пачка 3, C3-13 | нет | — |
| `findings/20261015-stage-done-stiraet-code-only-s6-stoporit-vhod-v-s7.md` | находка | `stage_done` стирает `code_only` со стадии: `s6_closed_by_code` ложен после кодового закрытия S6 — стори без исполнения в S6 встаёт на входе в S7 (на `main`) | `scripts/controller.py`, `scripts/s7_pretriage.py` | пачка 3, C3-14 | да | — |
| `findings/20261016-c1-8-ochered-kritika-t-836.md` | находка | C1-8 (A27) — очередь критика t-836: проглоченные `Refusal`, `subprocess.run` мимо `py`, `except Exception` → None, ускорение A27, T1–T3 | `scripts/audit_factory.py`, `scripts/story_run.py` | пачка 3, C3-15 | нет | — |
| `findings/20261016-tekst-s1-gap-pokazyvaet-imya-skripta.md` | находка | текст вопроса `s1_gap` называет человеку скрипт `vcs_evidence.py` — фабрика сама ловит нарушение и спрашивает «как есть» | `scripts/story_run.py`, `scripts/tests/test_human_questions.py` | пачка 3, C3-16 | нет | — |
| `findings/20261016-gejt-a-pokazan-s-nechinennym-factory-fixable.md` | находка | гейт A показан с «6 вещами, которые фабрика ещё чинит сама» — повтор B-177 в подклассе вне `--apply-fixes` | `scripts/gate_preflight.py`, `scripts/story_run.py`, `scripts/critic_rollcall.py` | пачка 3, C3-17 | нет | — |
| `findings/20261016-testy-s5-ne-zapuskayutsya-bez-zavisimostey-proekta.md` | находка | S5 гоняет тесты проекта Python'ом фабрики без зависимостей проекта: 4 из 4 не собираются, человека просят «установите» | `scripts/run_suite.py`, `scripts/s5_precheck.py`, `scripts/gate_preflight.py`, `references/conductor-actions.json` | пачка 3, C3-18 | нет | — |
| `findings/20261016-zhivoe-dokazatelstvo-gejta-a-prozoy-ne-zaplanirovano.md` | находка | живое доказательство «гейт A прозой» (C1-4) не снято и не стоит ни в одной строке «Живых доказательств» | `experiments/measurers/runs/` | пачка 3, C3-19 | нет | — |
| `findings/20261016-set-stage-zamenyaet-zapis-kodovo-zakrytoy-stadii.md` | находка | `set_stage` заменяет запись кодово закрытой стадии целиком: `accept` со `stage_complete` теряет `code_only`/`receipt_id` | `scripts/controller.py`, `scripts/tests/test_controller_state.py` | пачка 3, C3-20 | нет | — |
| `findings/20261017-approve-tolko-so-slovami-tri-kopii-pravila.md` | находка | правило «`approve` только при файле слов» в трёх местах `story_run.py` (аналог C4-14) | `scripts/story_run.py` | пачка 3, C3-21 | нет | — |
| `findings/20261017-molchalivye-prohody-stage-guard-perepis-osi-16.md` | находка | молчаливые проходы `stage_guard` вне правила манифеста (перепись оси 16 при C4-1) | `scripts/stage_guard.py` | пачка 3, C3-22 | нет | — |
| `findings/20261017-poisk-kejsa-ostatki-c4-13.md` | находка | поиск файла кейса по id — остатки C4-13 (одно имя в двух папках, двойник по регистру, `manifest_from_tests`) | `scripts/manifest_from_tests.py`, `scripts/s5_precheck.py` | пачка 3, C3-23 | нет | — |
| `findings/20261017-controller-ostatki-c4-10.md` | находка | `controller.py` — остатки C4-10: разбить `validate`, молчаливые пропуски Gate A, прочие `issubset`, CRLF генератора | `scripts/controller.py`, `tools/controller-blocks-gen.py` | пачка 3, C3-24 | нет | — |
| `findings/20261017-code-close-ostatki-c2-8.md` | находка | шов `code_close` — мелкие остатки C2-8 (`code_close_lead`, `idle_cap`, пин против настоящего `waiver.py`) | `scripts/story_run.py` | пачка 3, C3-25 | нет | — |
| `findings/20261017-nedostizhimoe-ostatki-c2-9.md` | находка | недостижимое — остатки C2-9 и медленный `resolve_runtime` (перечитывание пакета на каждом `prepare`) | `scripts/context_bundle.py`, `scripts/runtime_paths.py` | пачка 3, C3-26; частично: SC1-12 speed-cost/1 | нет | — |
| `findings/20261017-vozobnovlenie-ostatki-c2-4.md` | находка | возобновление ради суждения — остатки C2-4 (старый читатель вердикта, обрезка причины в `story_step`) | `scripts/story_run.py`, `scripts/story_step.py` | пачка 3, C3-27 | нет | — |
| `findings/20261019-predusloviya-ruchnogo-keisa-cherez-realnyj-interfejs-testera.md` | находка | предусловие ручного кейса должно создаваться через интерфейс тестировщика: нет рецепта и записи среды — отказ с дверью | `scripts/s5_precheck.py`, `scripts/gate_preflight.py`, `scripts/contract.py`, `agents/qa-case-designer.md` | пачка 3, C3-28 | да, 19.10 («класть сейчас») | `grounding` (находка-источник) |
| `findings/20261026-chetyre-parsera-prefiksa-stand-gap.md` | находка | префикс `stand gap:` разбирают четыре парсера (`contract.stand_gap_id`, `waiver`, `story_run` ×2) — один читатель по AR-13 | `scripts/contract.py`, `scripts/waiver.py`, `scripts/story_run.py`, `design/architecture.md` | пачка 3, C3-29 | нет | AR-13, FR-58, ось 16/19 (один читатель) |
| `findings/20261029-s0-karta-ne-nazyvaet-initialize.md` | находка | `start --stage S1` отказывает «initialize task before work», карта S0 команду не называет: дирижёр собрал `init.json` руками (прогон 14857 на 0.10.5) | `scripts/controller.py`, `phases/s0.md` | пачка 3, C3-31 | нет (П2 — решение Lead) | B-336, CX1-10, CX1-11 |
| **Пачка 5 (ожидает)** | | | | | | |
| `findings/20261021-dve-drugie-dorogi-reopen-perezapuskayut-held-rabotu-bez-voprosa.md` | находка | `release` и `rework --reason` перезапускают never-started работу закрытой истории без вопроса; `release_dispatch` обходит `validate` | `scripts/controller.py` | C5-1, ожидает | — | C1-6a, t-699 §12 Q2 |
| `findings/20261021-otkazannyj-ruchnoj-kejs-bez-terminalnogo-ishoda-tretij-verdikt-nedostizhim.md` | находка | отказанный ручной кейс без терминального исхода в трассировке — третий вердикт P21 недостижим для `person_checks` | `scripts/check_traceability.py`, `scripts/delivery_verdict.py` | C5-4, ожидает | — | C1-6b, t-1221, критик t-1228 |
| `findings/20261021-voprosy-build-check-bez-cen.md` | находка | пять вариантов вопроса `build_check` без ценовой секции — ключи в `question-prices.json`, как `s6.stand_confirm` | `scripts/story_run.py`, `references/question-prices.json` | C5-2, ожидает | — | C1-6b, t-699 §9 F10 |
| `findings/20261021-zhurnal-reshenij-progona-odnoj-formy.md` | находка | журнал решений прогона одной формы: `source` script, agent или user, исход accepted, refused, chosen или reported; слово агента не равно принятию; сначала сверить с существующими носителями | `scripts/controller.py` | C5-5, ожидает | — | обзор testing-factory (RELATED_WORK §2 п. 3, K7) |
| `findings/20261023-story-run-vtoroj-nositel-slovarya-metok-i-spiska-ostanovok.md` | находка | `story_run.py` держит второй носитель словаря меток (`:7775`) и списка остановок `UNTIL_PAST` (`:114`), которые hotfix-12586/1 довела до одного читателя | `scripts/story_run.py` | пачка 5, C5-6, ожидает | нет | HF1-6, HF1-8, OH3-18, conductor/1 |
| **Находки ночного прогона 14857 (0.10.6), 30.10.2026** | | | | | | |
| `findings/20261030-perefraz-dirizhyora-menyaet-slova-cheloveka.md` | находка | резюме дирижёра на гейтах A и B меняет слова человека (TC-001 вместо TC-003, «accepted» вместо «the stand has this user») | `scripts/gate_brief.py`, `scripts/story_run.py` | пачка 5, C5-9 | нет | t-1605 #10 |
| `findings/20261030-slova-na-s1-review-ne-perehodyat-v-s1-gap-na-teh-zhe-istochnikah.md` | находка | слова на `s1_review` не доезжают до `s1_gap` об тех же источниках (TP1-10937) | `scripts/story_run.py` | пачка 5, C5-10 | нет | D-0043; t-1605 #12 |

## Входящие

`findings/` этой кучки; находку, не названную ни в одной пачке, называет `piles.py check` (е).
Находки по теме в других кучках: `gates-and-words/findings/20261009-gate-b-pravka-avtomatizacii-bez-ispolnitelya.md`,
`report-delivery/findings/20261009-ischerpannyy-limit-remonta-nedostatki-ne-v-otchete.md`,
`driver-controller/findings/20261009-b-331-vopros-cheloveku-pered-relaunch.md` — узлы пачки 1 ссылаются на них.

## Вопросы владельцу

- нет (слово 09.10 дано трижды: принцип, его широта, цена и последствия в каждом варианте).
