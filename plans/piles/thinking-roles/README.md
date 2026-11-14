# Думающие роли: остатки прогона плеча B и ходока, параллельность (`thinking-roles`)

приоритет: П1 | фичи: F17, F10 | стенд: нужен (только живые доказательства, MyBooks) | зона: —

## Зачем

Эксперимент «думающие роли» прогнал стори на MyBooks целиком (плечо B) и отдельно — ручной проход 23 спорных карточек ходоком и
обход неподтверждённых мест аналитиком. Прогоны показали, что роли думают верно, а мешает им наш код: ходок дважды поставил «прошло»
там, где человек видит баг, часть карточек осталась без вердикта из-за правила рекордера, пробы целятся не в ту проверку, стадия не
закрылась после работы аналитика, и всё идёт по одному — 80 минут на 21 карточку и больше четырёх часов на автоматизацию. После этой
кучки ручной проход даёт верные вердикты, пробы закрывают окно без слова человека, а автоматизация и ручной проход идут параллельно.

## Что не так сегодня (факты)

- Ходок: ложный pass на карточках 3 и 23; 9, 15, 16 без вердикта; 14 невыполнима; 18, 19 не пройдены — `experiments/mybooks/thinking-roles/walker-vs-plain-agent.md`, разделы 4 и 6.
- Пробы: окно TC_001, TC_002 не закрылось `approved`; 30 из 44 проб не в цель — `docs/tasks/specs/reports/t-2031-probe-live-proof-report.md`, `docs/tasks/specs/reviews/t-2000-critic-probe-diff.md`.
- Плечо B: из двадцати дефектов B-1…B-20 пять не взяты ни одной пачкой починок (B-4, B-8, B-9, B-12, B-13) — `docs/tasks/specs/t-1936-fix-batch-arm-b.md`, раздел «Deferred».
- Скорость: параллельность обоих плеч — 1; S5 плеча B 4:13 — `experiments/mybooks/thinking-roles/time-analysis.md`; ходок 80 минут на 21 карточку — `experiments/mybooks/thinking-roles/morning-report-2026-11-06.md`.
- Тесты пакета в стиле pytest (13 файлов) невидимы для `selftest` — `docs/tasks/specs/reports/t-1996-walker-integration-report.md`, строки 34–35.

## Пачки

| № | Что изменится для пользователя | Строки | Размер | Статус | Взял | Ветка | MR |
|---|---|---|---|---|---|---|---|
| 1 | ручной проход кейсов и мест даёт верные вердикты: ввод как у человека, правило сбоя не мешает соседним кейсам, незнакомая учётка не останавливает прогон, стадия закрывается после аналитика | находки ходока и аналитика 06.11.2026 | L | закрыта | — | — | `5498318` |
| 2 | пробы целятся в проверку требования и закрывают окно без слова человека; драйвер не теряет ответ скрипта из-за предупреждения; швы первого прохода плеча B закрыты; тест, который ничего не исполнил, — красный | находки проб, драйвера, плеча B, тестов 06.11.2026 | L | закрыта | — | — | `5498318` |
| 3 | автоматизация идёт несколькими окнами сразу, ручной проход — тремя ходоками | находка параллельности 06.11.2026 | L | закрыта | — | — | `506e5e1` |
| 4 | остатки ревью критиков и скаутов: форма критика называет просмотренный диспатч, один замок файла, один помощник отказа, реестр медленных тестов, перечни знают новый скрипт | находки остатков 06.11.2026 | M | закрыта | — | — | `5498318` |
| 5 | хвосты П2 пачек 1, 2 и 4: быстрый отказ входа и остатки ревью ходока, запись обхода принимается по смыслу, повтор пробы с другой целью, один читатель ответов драйвера, статус вопроса гейта A из реестра, один сборщик `resolve_return`, поле `observation` черновика | находки пачек 1, 2 и 4 | M | ожидает | — | — | — |
| 6 | хвосты П3 пачек 1, 2 и 4: остатки ревью ходока и обходов, спеки приведены к коду ночных пачек, остатки цепочки проб, лишний вопрос `s1_gap` | находки пачек 1, 2 и 4 | S | ожидает | — | — | — |

Статусы пачки: `ожидает` → `в работе` → `сдано` → `принято` → `закрыта`.

## Бриф пачки 1

Начать с TR1-1, TR1-4, TR1-11 (не делят файлы): TR1-1 и TR1-4 снимают ложные и потерянные вердикты, без них параллельные ходоки
(пачка 3) только ускорят ошибку. Стенд нужен лишь для живого доказательства в конце. Слова владельца не нужно. Подробно —
`batch-1-ruchnoj-prohod.md`.

## Бриф пачки 2

Начать с TR2-1 (пробы в цель) и TR2-12 (невидимые тесты) — оба П1 и ни с чем не делят файлы; TR2-3 открывает цепочку узлов по
`story_run.py`. Подробно — `batch-2-proby-drajver-shvy.md`.

## Бриф пачки 3

Начать с TR3-1 (разведка) и одного прохода критика на план спеки t-1937; параллельно — TR3-2, TR3-3, TR3-7, TR3-8, TR3-11.
Подробно — `batch-3-parallelnost.md`.

## Бриф пачки 4

Начать с TR4-4, TR4-5 и TR4-1 (быстрые, файлы не делят); TR4-3, TR4-6…TR4-9 ждут слияния веток своих узлов (функций на основе нет).
Подробно — `batch-4-ostatki.md`.

## Бриф пачки 5

Хвосты П2 пачек 1, 2 и 4, собранные словом владельца 12.11.2026, чтобы эти пачки закрывались по узлам П1. Начать с TR1-5, TR1-6, TR2-2, TR2-3,
TR2-6, TR2-9, TR2-11, TR2-16, TR4-14, TR4-15 (у них «—» или только принятые узлы в «Зависит от»); остальные идут цепочками общих файлов.
Подробно — `batch-5-hvosty-p2.md`.

## Бриф пачки 6

Хвосты П3 пачек 1, 2 и 4, собранные словом владельца 12.11.2026. Начать с TR2-13, TR4-16, TR4-17; TR1-7 и TR2-10 ждут узлов пачки 5.
Подробно — `batch-6-hvosty-p3.md`.

## Дороги

Читать по порядку: эта карточка → файл пачки → находка узла (раздел с id узла) → спека, названная находкой → код по функциям из находки.
Слова: `plans/features.json` F17, F10 и сверх них: `walk_session`, `manual_capture`, `walk_actors`, `restore_request`, `probe_by_code`,
`assertion_id`, `already_probed`, `_read_answer`, `read_document`, `question_from_refusal`, `S5Scheduler`, `parallel_windows`, `walk` lease.
Не читать: кучки `execution-probes`, `exploratory`, `driver-controller` — их узлы написаны для пакета другого репозитория; всё, что
нужно узлу этой кучки, собрано в его находке.

## Содержание

Снимок 06.11.2026; пути — от корня репозитория, пути пакета — от `ai-packages/qa-factory/`. При расхождении авторитетны файлы пачек.

| id / файл | вид | суть (≤ 20 слов) | пути | статус | слово владельца | связи |
|---|---|---|---|---|---|---|
| **Пачка 1** | | | | | | |
| `findings/20261106-hodok-lozhnyj-pass-i-pravila-sboya.md` | находка, id — | набор по одной цифре прячет баг; снятое правило сбоя мешает следующим кейсам; нет шага «закончить сессию» | `scripts/manual_capture.py`, `scripts/walk_session.py` | в пачке 1, TR1-1, TR1-2, TR1-3 | нет | t-1957 |
| `findings/20261106-hodok-uchyotki-i-vhod.md` | находка, id — | дорожка с незнакомой учёткой уходит на старую дорогу и останавливает прогон; отказ входа ждёт минутами | `scripts/story_run.py`, `scripts/manual_capture.py` | в пачке 1, TR1-4; в пачке 5, TR1-5 | нет | t-1955, t-1957 |
| `findings/20261106-hodok-ostatki-kritika-i-priyomka-zapisi.md` | находка, id — | открытые замечания двух ревью ходока; запись обхода принимается по наличию цитаты, не по смыслу | `scripts/walk_session.py`, `scripts/manual_evidence.py`, `references/walk-charter.md` | в пачке 5, TR1-6, TR1-8; в пачке 6, TR1-7 | нет | t-2013, t-2018 |
| `findings/20261106-analitik-prohodit-mesta-ostatki.md` | находка, id — | S7 не закрылась после обхода мест; место за входом недоступно; черновик без подтверждения читается подтверждённым | `scripts/controller.py`, `scripts/story_run.py`, `scripts/place_answers.py` | в пачке 1, TR1-9, TR1-11; в пачке 5, TR1-10 | нет | t-1991, t-2010, t-2027 |
| **Пачка 2** | | | | | | |
| `findings/20261106-proby-cel-proby-i-ostatki.md` | находка, id — | проба не в цель: `assertion_id` на строку мимо Then; повтор пробы запирает цель; старое слово как вейвер | `scripts/probe_by_code.py`, `scripts/manifest_put.py`, `scripts/window_record.py` | в пачке 2, TR2-1; в пачке 5, TR2-2 | нет | t-1968, t-2000, t-2031 |
| `findings/20261106-drajver-chtenie-otvetov-i-ostatki-b20.md` | находка, id — | ответы дочерних скриптов читаются целым текстом; остатки цепочки приёмок; шапка над текстом дирижёра | `scripts/story_run.py`, `scripts/no_move.py` | в пачке 5, TR2-3, TR2-4, TR2-5 | нет | t-1988, t-2015, t-2020 |
| `findings/20261106-plecho-b-shvy-pervogo-prohoda.md` | находка, id — | пять невзятых дефектов плеча B, лишний вопрос S1, расхождение цены из двух источников | `scripts/handoff_check.py`, `scripts/gate_preflight.py`, `scripts/coverage_contract.py`, `scripts/stage_done.py` | в пачке 2, TR2-7, TR2-8; в пачке 5, TR2-6, TR2-9, TR2-11; в пачке 6, TR2-10 | нет | t-1936 |
| `findings/20261106-testy-pytest-nevidimy-i-sverka-spek.md` | находка, id — | тесты в стиле pytest невидимы для selftest; спеки и хартии отстали от кода ночных пачек | `scripts/selftest.py`, `docs/tasks/specs/`, `docs/SIBLING_MAP.md` | в пачке 2, TR2-12; в пачке 6, TR2-13 | нет | t-1996, t-2028 |
| `findings/20261106-odna-doroga-proby-na-vse-yazyki.md` | находка, id — | Python-путь пробы ломает первый assert, нет `--at`; исключение языка из спеки — дефект форджа | `scripts/probe_by_code.py`, `references/detectors.json`, `.claude/agents/designer.md`, `docs/SIBLING_MAP.md` | в пачке 2, TR2-14, TR2-15; в пачке 5, TR2-16 | да: 06.11.2026 («надо что бы всё было единообразно») | t-1968, t-2000, t-2045 |
| **Пачка 3** | | | | | | |
| `findings/20261106-parallelnost-okna-s5-i-hodoki.md` | находка, id — | окна автоматизации и ручной проход идут по одному; узлы параллельности из спек t-1937 и t-1957 | `scripts/controller.py`, `scripts/story_run.py`, `scripts/stand_lease.py` | в пачке 3, TR3-1…TR3-11 | да: 05.11.2026 («время уменьшить в разы», «пусть будет 3») | t-1937, t-1957 |
| **Пачка 4** | | | | | | |
| `findings/20261106-forma-kritika-ne-nazyvaet-prosmotrennyj-dispatch.md` | находка, id — | форма критика стадии не называет просмотренный диспатч автора; отказ приходит после работы и держит закрытие S7 | `scripts/stage_done.py`, `scripts/brief_pack.py` | в пачке 4, TR4-1 | нет | t-2036, t-2055 |
| `findings/20261106-kopii-zamka-fajla-v-pakete.md` | находка, id — | девять копий замка файла на msvcrt/fcntl; нужен один помощник с таймаутом | `scripts/stand_lease.py`, `scripts/manual_capture.py`, `scripts/case_versions.py` | в пачке 4, TR4-2 | нет | t-2060 |
| `findings/20261106-povtor-zapisi-otkaza-refuse-case.md` | находка, id — | запись отказа кейса в трёх местах и три чтения id строки; нужны `refuse_case` и один помощник | `scripts/story_run.py`, `scripts/controller.py` | в пачке 4, TR4-3 | нет | t-2055 |
| `findings/20261106-medlennye-testy-v-spisok-posle-kanona.md` | находка, id — | три файла дольше 10 с не в `slow_tests.json`; у одного нет потолка 600 | `scripts/selftest.py`, `scripts/slow_tests.json` | в пачке 4, TR4-4 | нет | t-2053 |
| `findings/20261106-test-guard-write-owners-case-kak-imya-kataloga.md` | находка, id — | фикстура берёт `<case>` именем каталога и падает на Windows (WinError 123) | `scripts/tests/test_guard_write_owners.py` | в пачке 4, TR4-5 | нет | t-2083 |
| `findings/20261106-novyj-skript-ne-zapisan-v-perechnyah.md` | находка, id — | `driver_timing` не во всех перечнях: перепись CLI, `audit_factory`, карта фич | `scripts/audit_factory.py`, `scripts/tests/test_task_root_parsers.py`, `plans/features.json` | в пачке 4, TR4-6 | нет | t-2060 |
| `findings/20261106-stroki-running-bez-zhivosti-v-kontrollere.md` | находка, id — | отказы «checkpoint active work» читают `running` без живости: мёртвая сессия держит правку, откат, возврат | `scripts/controller.py`, `scripts/execution_request.py` | в пачке 4, TR4-7 | нет | t-2036, t-2055 |
| `findings/20261106-test-prikovan-k-tekstu-a-ne-k-povedeniyu.md` | находка, id — | тест порядка проверки пробела читает исходник вместо входа | файл теста порядка проверки пробела | в пачке 4, TR4-8 | нет | t-2055 |
| `findings/20261106-vvod-tsepochka-po-tekstu-selektora.md` | находка, id — | цепочка ввода различает поле по написанию селектора и делится между акторами | `scripts/walk_session.py`, `scripts/manual_capture.py` | в пачке 4, TR4-9 | нет | t-2055 |
| `findings/20261110-melkie-ostatki-revyu-10-11.md` | находка, id — | живость по роли, а не по диспатчу; формы S7/S8 без префилла; медленная фикстура brief pack; аренда стенда без замка | `scripts/dispatch_liveness.py`, `scripts/brief_pack.py`, `scripts/stand_lease.py` | в пачке 4, TR4-12 | нет | t-2145, t-2153, t-2166 |
| `findings/20261110-s5-okno-posle-prinyatogo-avtorskogo-raunda-nevidimo.md` | находка, id — | окно S5 после принятого раунда автора не видно читателям открытых окон; стадия кончается отказом вместо просмотра критика | `scripts/story_run.py`, `scripts/tests/test_s5_window_leftovers.py` | в пачке 4, TR4-13 | нет | t-2263 |
| `findings/20261110-odin-sborshchik-resolve-return.md` | находка, id — | пакет `resolve_return` собирается в нескольких местах `story_run.py`; нужен один сборщик в контроллере | `scripts/controller.py`, `scripts/story_run.py` | в пачке 5, TR4-14 | нет | t-2263 |
| `findings/20261111-uchyotki-obhodov-ostatki-revyu.md` | находка, id — | остатки ревью TR3-10 D: стенд читается в нескольких местах, ключи пулов и `fold_kind` расходятся, `walk_assign_step` длинный, ответ `added` не возвращает S6 | `scripts/walk_pool.py`, `scripts/story_run.py`, `scripts/config_contract.py` | в пачке 6, TR4-16 | нет | t-2331 |
| `findings/20261111-proby-ostatki-cepochki.md` | находка, id — | остатки цепочки проб (t-2064) после приёмки: проверка строки у привязок, один предикат устаревания, мёртвый `--supersede`, один читатель строки агрегата, остатки старой дороги, `except Exception` ходьбы, пустой список строк, ранний снимок дерева в тесте, запас байт пина K7, `owner_role` с двумя правилами, остаток слова | `scripts/manifest_put.py`, `scripts/proof_level.py`, `scripts/probe_by_code.py`, `scripts/planning_contract.py`, `scripts/check_witness.py` | в пачке 6, TR4-17 | нет | t-2064, t-2400, t-2490 |
| `findings/20261112-tr3-9-ostatki-dorozhek-ruchnogo-prohoda.md` | находка, id — | остатки TR3-9: длинная функция дорожки, два повтора, мёртвое слагаемое, известный остаток отчёта, один нестабильный пин | `scripts/driver_stage_s6.py`, `scripts/controller.py`, `scripts/config_contract.py`, `scripts/tests/test_walk_lanes_parallel.py` | в пачке 6, TR6-1 | нет | t-096, t-102, t-107 |
| `findings/20261110-tr1-11-chernovik-nablyudeniya-klyuch-svyazi.md` | находка, id — | черновик непривязанного наблюдения не называет его: нужно одно необязательное поле контракта, которое читает `place_of_draft` | `scripts/place_answers.py`, `references/artifact-contract-run.md`, `scripts/validate_artifacts.py` | в пачке 5, TR4-15 | нет | t-2306, t-2299 |
| `findings/20261113-test-controller-rework-repair-binding-krasnyj-odin-raz-fr-31.md` | находка, id — | тест красный один раз на каноне, не воспроизвёлся (FR-31); первый шаг — печатать `repr` исключения в падающем assert | `scripts/tests/test_controller_rework_repair_binding.py` | в пачке 6, TR6-2 | нет | t-247 Red 2; TR4-7, t-2183 |
| `findings/20261114-skill-doroga-ne-pishet-register-gaps.md` | находка, id — | дорога скилла не записывает строки `register_gaps` критика S4: драйвер, который их записывает, там не бежит (край R18) | `skills/qa-story/phases/s4.md`, `scripts/driver_stage_plan.py` | в пачке 5, TR5-4 | нет | критик кода A2/A3/F7-пересборки (Q1); P31, ось 5 |
| `findings/20261114-f-r0-dve-dorogi-k-odnomu-registru-vopros-vladeltsu.md` | находка, id — | F-R0: две дороги к одному реестру наблюдений (роли с shell и критик S4 без Bash) — вопрос владельцу по P31, рекомендация (а) | `scripts/exploratory_findings.py`, `scripts/driver_stage_plan.py` | в пачке 5, TR5-5 | да (P31) | критик кода A2/A3/F7-пересборки (Q6) |
| `findings/20261114-cl-ns-detektor-roli-bez-shell-na-karte-komand.md` | находка, id — | CL-NS: роль без shell на карточке команды без носителя, который велит её запускать; четыре строки дрейфа | `references/role-commands.json`, `scripts/tests/test_ahead_cards.py` | в пачке 6, TR6-3 | нет | критик кода A2/A3/F7-пересборки (Q5); FR-56 |

## Входящие

`findings/` этой кучки; находку, не названную ни в одной пачке, называет `piles.py check --all` (е). Каждая новая находка тем же ходом получает строку в
пачке этой кучки, которую ещё не взяли, или указатель `перенос: <кучка>/…`.

## Вопросы владельцу

- TR5-5 (находка `findings/20261114-f-r0-dve-dorogi-k-odnomu-registru-vopros-vladeltsu.md`, P31): роли с командной строкой записывают наблюдения сами, а проверяющий кейсы без неё — строкой формы, которую записывает код; оставить две дороги (рекомендация, действует до слова владельца) или перевести всех на одну (отдельная тема, около шести узлов).

- Закрыто 06.11.2026. `dispatch.parallel_windows`: 3, и это умолчание пакета: «По умолчанию запускаем в параллели и только если это не возможно, то последовательно».
- Закрыто 06.11.2026. Восемь карточек Add to Cart: ответы владельца — `experiments/mybooks/thinking-roles/walker-vs-plain-agent.md`, раздел 5.
