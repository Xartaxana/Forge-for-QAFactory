# Живые прогоны и новые проекты (`live-runs`)

приоритет: П1 | фичи: — | стенд: нужен (кучка владельца и dev2) | зона: `ai-packages/qa-factory/scripts/hooklib.py`, `scripts/install_smoke.py`, `hooks/run-py.cmd`, `references/http-answers.json`, `references/launch-causes.json`, `experiments/measurers/`

## Зачем

Сегодня часть исправлений поведения роли влита в код, но ни разу не доказана живой ролью на реальном проекте: фабрика
идёт на Python и pytest, на консоли Windows и на проектах, где её писали, а на незнакомом проекте или не на Python
не проверена. Поэтому строка закрыта кодом, но не доказана. После первой пачки каждое такое изменение либо подтверждено
живым прогоном на проекте другого человека, либо честно записано как непроверенное, а гард тестов и кодировка консоли
не привязаны к одному языку и одной ОС.

## Что не так сегодня (факты)

- Проба «проверка живая» для не-Python влита 07.10 по частям, но строка закрывается только после живого доказательства M1/M2/M3 на проекте dev2 (`plans/BACKLOG.md:419`).
- Исходящий HTTP с User-Agent влит 07.10; списки ответов в `http-answers.json` остаются оценкой до замера Антона (`plans/BACKLOG.md:427`).
- Онбординг пишет на диск только на шагах p3 и p4; найденное на остальных шагах теряется при компакции контекста (`plans/BACKLOG.md:430`).
- Гард «тесты только через `run_suite.py`» знает только `pytest` (`plans/BACKLOG.md:423`); кодировка консоли Windows искажает первую строку `install_smoke.py` (`plans/BACKLOG.md:432`).
- Прогон TP1-13797 на исправленном коде против judge-off ($109.00) назначен словом владельца 29.09 (`plans/BACKLOG.md:53`); прогоны cmp1..cmp3 видны в журнале git, закрыт ли этот, проверить по файлам.
- 12 открытых строк в пачке 1 и 10 находок (дайджест `docs/tasks/specs/reports/t-712-scout-piles-a.md`, пересчёт 12 из 12 и 10 из 10 на 13.10).

## Пачки

| № | Что изменится для пользователя | Строки | Размер | Статус | Взял | Ветка | MR |
|---|---|---|---|---|---|---|---|
| 1 | каждое изменение поведения роли доказано живым прогоном; фабрика идёт на незнакомом проекте и не-Python | B-015 | M | закрыта | — | — | `855d4e5c` |
| 2 | живые доказательства закрытых и сданных пачек сняты прогонами на 0.10.5 и позже; эталон стори 14857 | B-373, B-411, B-361, B-414, B-410, B-408, B-092, B-104, B-097 | L (23 узла; D3: одна пачка живых доказательств) | ожидает | — | — | — |

Открытое перенесено 01.11.2026 → onboarding-forge/1, live-runs/2.

Статусы пачки: `ожидает` → `в работе` → `сдано` → `принято` → `закрыта`. Размер — по узлам: S ≤ 4 узлов,
M 5–9, L 10–15 (больше — две пачки). Взятая пачка заморожена: её файл правит только взявший, новое
по теме — файлом в `findings/`.

## Бриф пачки 1

Начать с LR1-6 (сверка B-015: закрыт ли прогон cmp1..cmp3) и LR1-5 (код: гард и кодировка, без стенда); живые узлы
LR1-1, LR1-3, LR1-4 требуют проект dev2 и стенд. Ждёт: ввод Антона (LR1-2); слово владельца не нужно. Подробно —
`batch-1-live-proofs.md`, раздел «Бриф».

## Дороги

Читать по порядку: эта карточка → `batch-1-live-proofs.md` → находки узла (колонка «id / файл» ниже) → строки
`plans/BACKLOG.md` 53, 120, 125, 135, 418, 419, 423, 427, 429, 430, 432, 433 → `docs/tasks/b-408-measurement-for-dev5.md`
(замер для Антона, отправлен владельцем 07.10) → `experiments/measurers/` (`runs/`, `answers/`) → `docs/RUNBOOK.md` §9
(как запустить прогон в фоне) → `PROJECT.md` P8 (эксперименты без следов), FR-33.
Слова: `plans/features.json` F03, F07, F15 (поле `words`) и сверх них: `probe_by_code`, `detectors.json`, `M1`, `M2`,
`M3`, `L1`, `L2`, `User-Agent`, `http-answers.json`, `DIRECT_TEST_RUN`, `PREFILTER_SUBSTRINGS`, `collect_forms`,
`reconfigure`, `PYTHONUTF8`, `run-py.cmd`, `activity_capture`, `ACTIVITY NOT RECORDED`, `precompact_guard`,
`postcompact_reload`, `state/onboarding`, `stage_compare`; «живое доказательство», «незнакомый проект», «проект
dev2».
Не читать: код стадий; зоны `execution-probes` и `onboarding-hooks` (остатки B-373 и B-411 — их строки), `stand-and-sources`.

## Содержание

Снимок 13.10.2026; пути — от `ai-packages/qa-factory/`; суть строк — из `plans/BACKLOG.md`, находок — из дайджеста t-712. При расхождении авторитетна доска `plans/PILES.md`.

| id / файл | вид | суть (≤ 20 слов) | пути | статус | слово владельца | связи |
|---|---|---|---|---|---|---|
| **Живая проба на проекте dev2 (пачка 1, LR1-1)** | | | | | | |
| B-373 / `findings/B-373-pereotkryto-06-10-2026-d-0025.md` | строка + находка-остаток | `probe_by_code` для теста на любом языке; части a, b, c влиты 07.10, остаток M1–M3 лежит в находке | `scripts/probe_by_code.py` | пачка 1, LR1-1: закрывается только живым доказательством | D-0028 (06.10) | `execution-probes` (остатки пробы) |
| **HTTP: замер Антона (пачка 1, LR1-2)** | | | | | | |
| B-408 / `findings/B-408-iskhodyashchiy-http-bez-user-agent-i-chtenie.md` | строка + находка-остаток | исходящий HTTP без User-Agent; влито 07.10; списки `http-answers.json` — оценка до замера (a)(b) | `references/http-answers.json` | пачка 1, LR1-2: ждёт ввод Антона | нет | `stand-and-sources` (остатки HTTP) |
| **Онбординг и компакция (пачка 1, LR1-3)** | | | | | | |
| B-411 / `findings/B-411-onbording-pishet-na-disk-tolko-v.md` | строка + находка-остаток | онбординг пишет на диск только в p3 и p4; живые прогоны L1/L2 (возобновление после компакции) не сделаны | `scripts/precompact_guard.py`, `scripts/postcompact_reload.py` | пачка 1, LR1-3 | нет | `onboarding-hooks` (остатки заметок) |
| **Живые доказательства решений гейтов и сессии (пачка 1, LR1-4)** | | | | | | |
| B-361 | строка | ответ человека на пробел стенда с гейта A переносится на карточку гейта B; гейт B переспрашивает только при изменении | `scripts/gate_brief.py` | пачка 1, LR1-4: половина `s8.md` сделана по тексту — проверить по коду | D-0026 | `package-ci`, `gates-and-words` |
| B-414 | строка | карточка пробела стенда объясняет, речь о кейсе или об уровне, и спрашивает «временно или свойство среды» | `scripts/stand_gaps.py` | пачка 1, LR1-4 | D-0029 | `gates-and-words` |
| B-410 | строка | идентичность сессии для команд, которые роль запускает руками; один носитель id из SessionStart-хука | `scripts/activity_capture.py` | пачка 1, LR1-4 | нет | `onboarding-hooks` (остатки сессии) |
| **Гард тестов и кодировка консоли (пачка 1, LR1-5)** | | | | | | |
| B-404 | строка | гард «тесты только через `run_suite.py`» знает только `pytest`; формы запуска тестов вынести в данные | `scripts/hooklib.py`, `references/launch-causes.json` | пачка 1, LR1-5 | нет | `package-ci` (универсальность форм) |
| B-413 | строка | кодировка консоли Windows: `—` в `install_smoke.py` до `reconfigure`; кодировка в одном месте, в лаунчере | `scripts/install_smoke.py`, `hooks/run-py.cmd` | пачка 1, LR1-5 | нет | `package-ci` (остатки кодировки) |
| **Прогон против judge-off (пачка 1, LR1-6)** | | | | | | |
| B-015 | строка | прогон TP1-13797 на исправленном коде против первого прогона judge-off ($109.00) | `experiments/measurers/` | пачка 1, LR1-6: cmp1..cmp3 закрыты? проверить по файлам | решение 29.09 | `cost-dashboard` (замер порога) |
| **Незнакомый проект и новые сценарии (пачка 1, LR1-7)** | | | | | | |
| B-092 | строка | прогон на незнакомом проекте без онбординга | — | пачка 1, LR1-7 | нет | — |
| B-104 | строка | живые приёмки платформ: Android/iOS-адаптеры, playwright-cli, матрица OS и хоста, multi-repo с неверной базой | — | пачка 1, LR1-7 | нет | — |
| B-097 | строка | несколько стори одновременно в одном проекте: ветка или worktree на стори, task в каждом событии хука | — | пачка 1, LR1-7 | нет | — |
| **Живые доказательства forge** | | | | | | |
| `findings/20261008-forge-pachka-1-zhivye-dokazatelstva.md` | находка, id — | два живых доказательства forge/1 на первой пачке dev2: «взять пачку по README за 10 минут» и «слияние двух журналов без конфликта» | `tools/piles.py`, `tools/dev.config.yaml` | ждёт первой пачки dev2 | дано 08.10 | `forge` |
| `findings/20261017-conductor-2-zhivoe-dokazatelstvo-cmp3.md` | находка, id — | живое доказательство conductor/2: один прогон на копии cmp3 (K1, K2/K9, K4, K5, K8) | `scripts/story_run.py`, `scripts/handoff_check.py`, `scripts/waiver.py` | пачка 1, LR1-8 | дано 17.10 | `conductor` |
| `findings/20261105-github-move-2-zhivoj-progon-mybooks-posle-pereezda.md` | находка, id — | живое доказательство github-move/2: прогон на MyBooks пакетом из нового репозитория после D2/D3, сканер O7 по артефактам `total: 0` | `ai-packages/qa-factory/`, `experiments/measurers/` | пачка 2, строка «Живые доказательства» GM2 | перенос, владелец 05.11.2026 | `github-move` |
| **Универсальность: не-pytest и не-testproject1 (кандидаты пачки 2)** | | | | | | |
| `findings/B-090-sloy-avtomatizatsii-znaet-pytest-kartochka.md` | находка | слой автоматизации знает pytest: маркер зашит в `s5_precheck.py`, вынести за `adapter_id` и `test_marker` | `scripts/s5_precheck.py` | открыто | нет | — |
| `findings/B-091-cost-capture-znaet-cli-testproject1-regex.md` | находка | `cost_capture` знает CLI testproject1 (regex); вынести за адаптер | `scripts/cost_capture.py` | открыто | нет | `cost-dashboard` |
| `findings/B-093-sborka-kak-svidetel-komanda-sborki-proekta.md` | находка | сборка как свидетель: `probe.build`, запрет коммита при красной сборке | — | открыто | нет | — |
| **Незнакомый проект: кейсы и хуки (кандидаты пачки 2)** | | | | | | |
| `findings/B-094-keysy-proekta-v-ego-sobstvennom-formate.md` | находка | кейсы проекта в его формате: экспорт после гейта B вместо `TC-NNN.md` | — | открыто | нет | — |
| `findings/B-095-skaut-kladet-v-manifest-skoup-dokument-nabora.md` | находка | скаут кладёт в манифест скоуп-документ набора тестов; конфликт идёт на гейт A | — | открыто | нет | — |
| `findings/B-096-inventar-deystvuyushchikh-khukov-proekt.md` | находка | инвентарь действующих хуков проекта в онбординге и докторе; «нет доступа» — unknown | — | открыто | нет | `onboarding-hooks` |
| `findings/20261021-stsenarij-otsenki-s-utaennym-faktom.md` | находка | сценарий оценки с утаённым фактом: в оракуле отмечено убранное требование, судья проверяет, что роль спросила (P5, P20), а не выдумала | `experiments/` | LR1-9, ожидает | нет | обзор testing-factory (RELATED_WORK §2 п. 14, K9) |
| `findings/20261028-zhivye-dokazatelstva-zakrytyh-pachek-na-0-10-5.md` | находка | девять живых доказательств семи закрываемых пачек (conductor/1, hotfix-12586/3 и /4, run-honesty/1, speed-cost/1 и /3, onboarding-hooks/2): один прогон на релизе 0.10.5 | `ai-packages/qa-factory/` (прогон, кода нет) | LR1-10…LR1-18, ожидает | перенос подтверждён 28.10.2026 | `conductor`, `hotfix-12586`, `run-honesty`, `speed-cost`, `onboarding-hooks` |
| `findings/20261030-etalon-ruchnogo-progona-14857-dlya-sleduyushchego-progona.md` | находка | тесты ручного прогона 14857 — эталон стори; следующий прогон сверяется с ним по требованиям, оракулам и допускам | `experiments/measurers/` | LR1-19, ожидает | нет | t-1606 §2, §4; LR1-9; TQ1-24, TQ1-25 |
| `findings/20261112-plecho-svobodnogo-agenta-v-sravnitelnom-progone.md` | находка, id — | плечо «свободный агент с одним промтом» в каждом сравнительном прогоне; сверка по исходу; «меньше, чем у свободного агента» — стоп | `experiments/` | пачка 2, LR2-1, ожидает | дано 12.11.2026 (два плеча, без знания онбординга, счёт по корневой причине) | LR1-19, LR1-9; `thinking-roles` 1–3; `speed-cost/4` (FB-13) |
| **Живые доказательства из других кучек (пачка 2, пересборка 01.11.2026)** | | | | | | |
| `findings/20261014-krasnyy-test-bez-proby-zapiraet-s5.md` | находка, id — | красный тест без пробы запирает S5; возобновление живого доказательства гейта B на копии cmp3gb (перенос из `conductor`) | `experiments/measurers/runs/cmp3gb.md` | пачка 2, C3-1, ожидает | нет | `conductor` (C3-1) |
| `findings/20261016-zhivoe-dokazatelstvo-gejta-a-prozoy-ne-zaplanirovano.md` | находка, id — | живое доказательство «гейт A прозой» не запланировано; строка в «Живые доказательства» и прогон до гейта A (перенос из `conductor`) | `experiments/measurers/runs/` | пачка 2, C3-19, ожидает | нет | `conductor` (C3-19) |
| `findings/20261023-oshibka-fabriki-v-bekloge-proekta-so-scope-upstream-candidate-proverit-na-zhivom.md` | находка, id — | ошибка фабрики в беклоге проекта со scope `upstream-candidate`: проверить на живом повторе 12586 (перенос из `onboarding-hooks`) | `skills/qa-story/SKILL.md`, `agents/qa-retro-analyst.md` | пачка 2, OH3-21, ожидает | дано 23.10 | `hotfix-12586` (живое доказательство /1) |

## Входящие

`findings/` этой кучки; их число и дату последней показывает `plans/PILES.md` (собирает `piles.py board`; карточку код не правит).

## Вопросы владельцу

- нет (основание: «Решение владельца нужно: да» — 0 из 10 находок, дайджест t-712 п. 5; ждёт не слова владельца, а ввода Антона по замеру User-Agent и проекта dev2 для живых доказательств).
