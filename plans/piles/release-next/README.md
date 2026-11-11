# Релиз 0.10.9 (`release-next`)

приоритет: П1 | фичи: F02, F04, F07, F08, F11, F13, F14, F15, F16, F17, F19, F22, F23 | стенд: не нужен (CI + эталоны) | зона: `ai-packages/qa-factory/scripts/**`, `ai-packages/qa-factory/agents/*`, `ai-packages/qa-factory/references/**`, `ai-packages/qa-factory/skills/**`

## Зачем

Это очередь следующего релиза: все пункты высшего приоритета, которые остались открытыми после релизов 0.10.7 и 0.10.8. Они
собраны из прежних кучек пересборкой бэклога 01.11.2026 (слово владельца), чтобы на релиз смотреть в одном месте. После пачки
проба доктора судит доставку контекста верно, сборщик данных упаковывает всю историю прогона, ложные предупреждения сессии и
остановки скаута на решённом конфликте уходят, критик кейсов ищет дубли, а исследовательский прогон находит баги корзины.

## Что не так сегодня (факты)

- Проба контекста доктора остаётся `unverified`: запись ответа Agent читает не тот ключ id (`scripts/host_dispatch.py:263`, `scripts/agent_autobind.py:39`).
- Таблица наборов сборщика пропускает папку истории (`ai-packages/qa-factory/references/collect-sets.json`).
- Лимит чтения стража 30 000 байт ниже вложений реального тикета (`scripts/guard_pre_tool.py`, `DEFAULT_BIG_READ_BYTES`).
- Мера потолков инъекции A22/A25 не равна тому, что получает роль (`scripts/audit_factory.py`).
- Цепочка исследовательского прогона XT1-1…XT2-2 не начата: нет `scripts/exploration.py` (`ls ai-packages/qa-factory/scripts/`).

## Пачки

| № | Что изменится для пользователя | Строки | Размер | Статус | Взял | Ветка | MR |
|---|---|---|---|---|---|---|---|
| 1 | релиз 0.10.9: проба доктора, сбор истории, ложные предупреждения, диета инъекции, тесты различают, исследовательский прогон | B-375, B-380, B-272, B-271, B-353, B-304, B-306, B-346, B-076, B-072 | L | закрыта | dev2, 02.11.2026 | `claude/release-10-9-706cee` | `a2bb4de9e` https://git.example.com/dev1/yml-text-factory/-/merge_requests/14 |
| 2 | один баг и его проявления: узлы N1–N8 спеки t-2187 и три хвоста критика (RN2-9…RN2-11) сделаны и слиты в `experiment/thinking-roles`; ждёт только живой перепрогон N9 (слово владельца) | — (находка 10.11.2026, узлы RN2-1…RN2-11) | L | ожидает | — | — | — |

Статусы пачки: `ожидает` → `в работе` → `сдано` → `принято` → `закрыта`. Размер — по узлам: S ≤ 4 узлов,
M 5–9, L 10–15 (больше — две пачки). Здесь 69 узлов (36 при сборке 01.11, RN1-2…RN1-10 по прогону LOCAL-1, 02.11, и RN1-11…RN1-33 по двум разборам законченного LOCAL-1, 02.11): пачка собрана пересборкой бэклога, а не по формуле. Взятая пачка
заморожена: её файл правит только взявший, новое по теме — файлом в `findings/`.

## Бриф пачки 1

Узлы с пометкой «перепроверить» начинаются со сверки по коду. Стенд не нужен — CI и эталоны. Слово владельца нужно только там, где
узел его называет. CD1-24 и CD1-25 в пачку не входят (0.11.0 по слову владельца 29.10). Подробно — `batch-1-release-0-10-9.md`, раздел «Бриф».

## Дороги

Читать по порядку: эта карточка → `batch-1-release-0-10-9.md` → находки узла (колонка «id / файл» ниже) → строки
`plans/BACKLOG.md` узла → код зоны по функциям из «Слов» → `docs/tasks/specs/reports/backlog-audit-20261101/` (строка аудита узла).
Слова: `plans/features.json` F04, F11, F14, F17, F22, F23 (поле `words`) и сверх них: `host_dispatch.record`, `agent_autobind`,
`host_probe`, `collect_pack`, `collect-sets.json`, `names_whole`, `sizing`, `area_match`, `role_load`, `inject-map.json`.
Не читать: соседние кучки и пачки `words-gates`, `driver-hosts`, `execution-report`, `onboarding-forge`, `live-runs`: их узлы в эту пачку не входят.

## Содержание

Снимок 01.11.2026; пути — от `ai-packages/qa-factory/`; суть строк — из `plans/BACKLOG.md`, находок — из их файлов. При расхождении
авторитетна доска `plans/PILES.md`. Каждый id строки карточки и каждый файл из `findings/` стоит здесь ровно один раз
(`tools/test_pile_cards_contents.py`); id строки стоит и в «Что» ровно одного узла файла своей пачки (`piles.py check` (д)).

| id / файл | вид | суть (≤ 20 слов) | пути | статус | слово владельца | связи |
|---|---|---|---|---|---|---|
| **Пачка 1: гейты и слова** | | | | | | |
| B-272 | строка | гейт B принимает слова человека из закрытого списка в данных, а не команду `waiver.py` | `scripts/story_run.py`, `scripts/waiver.py` | пачка 1, GW1-3 | нет | — |
| B-271 | строка | ретро всегда полное; из текста гейта убрано «можно пропустить или урезать» | `scripts/controller.py` | пачка 1, GW1-3 | нет | — |
| `findings/20261031-names-whole-pravyj-kraj-vrazhdebnyj-variant-prohodit.md` | находка | правый край `names_whole` пропускает враждебный вариант (`test_x[-1]`, `PC-1@TC_002`) | `scripts/contract.py` | пачка 1, GW1-52 | нет | — |
| `findings/20261031-case-versions-unpinned-pustoj-spisok-na-istorii-bez-kejsov.md` | находка | `unpinned()` на истории без файлов кейсов отдаёт `[]`: репетиция гейта A молчит | `scripts/case_versions.py`, `scripts/gate_preflight.py` | пачка 1, SC5-15 | нет | — |
| **Пачка 1: планирование и кейсы** | | | | | | |
| `findings/20261030-voprosy-onbordinga-mjortvye-klyuchi-i-dod-bez-chitatelya.md` | находка | `sizing.py` читает мёртвый ключ: `area_match` пуст у всех требований; пункты интервью — в OH3-35 | `scripts/sizing.py`, `scripts/brief_pack.py` | пачка 1, OH3-34 | нет | OH3-35 (`onboarding-forge/1`) называет файл по пути |
| `findings/20261029-extend-cel-plana-ne-sushchestvuet-na-baze.md` | находка | цель `extend` плана S3 не проверяется по дереву базы; дизайнер S4 ищет файл по всему диску | `scripts/planning_contract.py`, `scripts/brief_pack.py` | пачка 1, TQ1-21 | нет | — |
| `findings/20261030-vilka-vremeni-cherez-asinhronnuyu-zapis-bez-dopuska-i-ishoda-nelzya-razlichit.md` | находка | вилка времени идёт без допуска и без исхода «нельзя различить» | `agents/qa-case-designer.md`, `references/test-code-patterns.md` | пачка 1, TQ1-24 | нет | — |
| `findings/20261030-kritik-kejsov-ne-ishchet-dubli-i-sliyaniya-p16.md` | находка | критик кейсов S4 принял 12 кейсов без находок о дублях и слиянии | `agents/qa-case-critic.md` | пачка 1, TQ1-27 | нет | — |
| **Пачка 1: источники и сбор** | | | | | | |
| `findings/20261029-limit-chteniya-nizhe-vlozhenij-realnogo-tiketa.md` | находка | лимит чтения 30 000 байт ниже вложений реального тикета | `scripts/guard_pre_tool.py`, `scripts/ticket_adapter.py` | пачка 1, SC2-41 | слово 29.10.2026 | — |
| `findings/20261029-skaut-ostanavlivaetsya-na-konflikte-reshyonnom-v-kommentariyah.md` | находка | скаут S1 остановился на конфликте, уже решённом в комментариях источника | `skills/qa-story/phases/s1.md`, `agents/qa-scout.md` | пачка 1, RC1-13 | нет | — |
| `findings/20261030-sbor-tablica-naborov-ne-pokryvaet-papku-istorii.md` | находка | таблица наборов не покрывает папку истории: 707 файлов пропущены | `references/collect-sets.json`, `scripts/collect_pack.py` | пачка 1, CL3-3 | слово 30.10.2026 | — |
| `findings/20261030-sbor-plugin-version-istorii-ne-tam-chitaetsya.md` | находка | сборщик читает `plugin_version` не из `run_mode` | `scripts/collect_pack.py` | пачка 1, CL3-5 | нет | — |
| `findings/20261030-sbor-transkripty-tolko-zavisshih-petli-ne-vidny.md` | находка | транскрипты уходят только с зависшей историей; петли не видны | `scripts/collect_stall.py`, `scripts/collect_pack.py` | пачка 1, CL3-9 | слово 30.10.2026 | — |
| **Пачка 1: скорость и окно** | | | | | | |
| `findings/20261029-zaderzhka-odnoj-komandy-story-step-40-200-sekund.md` | находка | одна команда фабрики занимает 40–200 с; нужен профиль | `scripts/story_step.py`, `scripts/controller.py` | пачка 1, SC2-40 | слово 29.10.2026 | — |
| `findings/20261030-posle-0-10-2-medlennee-ne-vyzovy-a-vozvraty-i-dirizhyor.md` | находка | после 0.10.2 медленнее стал ход прогона, а не вызовы; метрика считается на ход | `scripts/story_step.py` | пачка 1, SC2-40 | нет | SC5-7 (`driver-hosts/1`) называет файл по пути |
| B-375 | строка | окно «все тесты переданы человеку» принимается по манифесту, а не по заявлению | `scripts/acceptance.py`, `scripts/window_record.py` | пачка 1, EP1-4 | нет | — |
| B-380 | строка | запись окна S5 хранит подробности причин для однострочной привязки | `scripts/reporters.py` | пачка 1, EP1-4 | нет | — |
| `findings/20261030-kap-okna-tratitsya-na-otkaz-samoj-fabriki-bez-kvitancii.md` | находка | кап доработок окна тратится на отказ самой фабрики (нет квитанции) | `scripts/story_run.py` | пачка 1, DC1-21 | нет | — |
| `findings/20261028-testy-ne-derzhat-styki-stadij.md` | находка | тестов много, а стыки стадий не держат; нужен реестр стыков | `scripts/selftest.py`, `references/` | пачка 1, F6-51 | слово 28.10.2026 | — |
| `findings/20261029-tajmaut-pytest-prochitan-kak-stend-ne-rabotaet.md` | находка | таймаут pytest проекта прочитан как «индексация на стенде не завершается» | `scripts/run_suite.py`, `scripts/brief_pack.py` | пачка 1, RH2-9 | слово 29.10.2026 | — |
| **Пачка 1: автоматизация и тесты фабрики** | | | | | | |
| `findings/20261024-avtomator-beret-dannye-stenda-vmesto-fikstur-harnessa.md` | находка | подходы проекта записаны при онбординге, но план, гейт A и автоматор их не применили | `agents/qa-automator.md`, `agents/qa-test-strategist.md` | пачка 1, TQ1-11 | слово 24.10.2026 | — |
| `findings/20261030-then-razlichayushchij-traktovki-dolzhen-past-pri-drugoj-proba-modeliruet-ee.md` | находка | различающий Then должен падать при второй трактовке; красная проба моделирует альтернативу | `scripts/probe_by_code.py`, `references/code-review-rubric.md` | пачка 1, TQ1-25 | нет | — |
| `findings/20261021-test-story-step-chas-pod-nagruzkoj-razdelit.md` | находка | `test_story_step.py` идёт час под нагрузкой; разделить по командам | `scripts/tests/test_story_step.py` | пачка 1, TQ1-10 | слово 21.10.2026 | — |
| **Пачка 1: исследовательский прогон** | | | | | | |
| `findings/20261031-qa-explore-dolzhen-nayti-bagi-korziny-mybooks.md` | находка | `qa-explore` на MyBooks обязан сам найти три бага корзины, пропущенные прогоном CART-1 | `references/perturbations.json`, `skills/qa-explore/` | пачка 1, XT2-2 | слово 31.10.2026 | цепочка XT1-1…XT1-8 |
| **Пачка 1: деньги, отчёт, онбординг, роли** | | | | | | |
| `findings/20261024-cena-kritika-keysov-ne-uchtena.md` | находка | расход критика кейсов не учтён: `by_model: {}`, цена истории занижена на ~$2.24 | `scripts/cost_capture.py`, `scripts/task_price.py` | пачка 1, CD1-13 | нет | — |
| `findings/20261030-cena-zadachi-razezzhaetsya-po-dvum-strokam-dashborda.md` | находка | цена задачи на дашборде расходится по двум строкам; 12 из 36 сессий на `(no task)` | `scripts/factory_dashboard.py`, `scripts/cost_capture.py` | пачка 1, CD1-27 | нет | — |
| B-353 | строка | причина «blocked on the stand» принадлежит `environment`, не `product` | `references/delivery-reason-owners.json` | пачка 1, RD1-4 | нет | — |
| B-304 | строка | хвосты N8 в `stage_guard` и тексте писаря | `scripts/stage_guard.py`, `agents/qa-doc-scribe.md` | пачка 1, RD1-4 | нет | — |
| B-306 | строка | хвосты карточки отчёта гейта A: сырой stderr в `missing:`, блокировка кейса после `accept` | `scripts/stand_gaps.py`, `scripts/story_run.py` | пачка 1, RD1-4 | нет | — |
| `findings/20261029-preduprezhdenie-ustanovleno-0-10-3-pri-rabote-0-10-5.md` | находка | ложное «установлено 0.10.3» при работающей 0.10.5; unknown-пробы доходят до гейта A | `scripts/hooklib.py`, `scripts/host_probe.py` | пачка 1, OH1-11 | слово 29.10.2026 | HF8-9…14 (`hotfix-12586/8`) |
| `findings/20261101-proba-konteksta-doktora-ne-chitaet-agentid.md` | находка | проба доктора `unverified`: запись ответа Agent читает не тот ключ id | `scripts/host_adapter.py`, `scripts/host_dispatch.py`, `scripts/agent_autobind.py` | пачка 1, RN1-1 | слово 01.11.2026 | OH3-19; DC1-30 |
| `findings/20261102-strateg-sdaet-nezapolnennoe-i-krugi-dorabotki.md` | находка | стратег S3 сдаёт незаполненное: 4 круга доработки в LOCAL-1, три формальные | `scripts/planning_contract.py`, `scripts/stage_done.py`, `scripts/handoff_init.py`, `scripts/question_register.py`, `agents/qa-test-strategist.md` | пачка 1, RN1-2 | слово 02.11.2026 | S4 дизайнер (тот же класс) |
| `findings/20261102-dirizhyor-pereskazyvaet-paket-gejta-a.md` | находка | дирижёр пересказал гейт A таблицей из букв, склеил Q4/Q7–Q9, вернул список документов | `scripts/gate_brief.py`, хук `Stop`, `skills/qa-story/SKILL.md`, `phases/s4.md` | пачка 1, RN1-4 | слово 02.11.2026 | GW1-11; C5-9 |
| `findings/20261102-adres-ui-ne-uznan-kogda-ui-i-api-na-odnom-adrese.md` | находка | вопрос об адресе UI при UI и API на одном адресе, хотя UI-проба входа прошла | `scripts/env_probe.py`, `skills/qa-onboarding/` | пачка 1, RN1-3 | — | W-2 hotfix-12586 |
| `findings/20261102-p1-user-path-failures-no-code.md` | находка | детектор G2-14 на «текущем коде» без диффа печатает «no code»: места из `context-bundle facts[].path` ему не отданы | `scripts/user_path_failures.py`, `scripts/brief_pack.py` | пачка 1, RN1-5 | нет | G2-14, G2-15, SS1-13; разбор t-1666 П-1 |
| `findings/20261102-p2-otkaz-kazhdogo-zaprosa-potoka.md` | находка | отказ запроса проверен только на `POST /api/cart`, а не на каждом запросе потока; один механизм с `qa-explore` | `scripts/brief_pack.py`, `agents/qa-test-strategist.md`, `references/perturbations.json` | пачка 1, RN1-6 | нет | XT2-2; разбор t-1666 П-2 |
| `findings/20261102-p3-kritik-kejsov-vycherkivaet-fokus.md` | находка | критик кейсов вычёркивает Then «фокус сохранён», которого требует правило 5a дизайнера: нет близнеца в уставе критика | `agents/qa-case-critic.md`, `agents/qa-case-designer.md` | пачка 1, RN1-7 | нет | EP1-29; TQ1-24, TQ1-27; разбор t-1666 П-3 |
| `findings/20261102-proba-ts-ubita-no-soobshchenie-playwright-ne-prochitano.md` | находка | проба TypeScript падает на мутированной строке, но вердикт `incomplete`: сообщение JUnit Playwright не читается (`fires_on`), E15 записан как «инструмент не читает язык», человеку задан ложный вопрос | `scripts/probe_by_code.py`, `skills/qa-story/phases/s5.md`, `agents/qa-code-critic.md` | пачка 1, RN1-8 | нет | EP1-36, EP1-37, EP1-22; GW1-43 |
| `findings/20261102-dirizhyor-sprashivaet-cheloveka-ne-razobravshis-sam.md` | находка | дирижёр спрашивает человека по состоянию кода, не прочитав улики: общего правила «сначала разберись сам» нет, фазы учат рефлексу, код вопроса не проверяет | `design/factory-rules.md`, `skills/qa-story/SKILL.md`, `phases/s*.md`, `references/conductor.md`, `scripts/story_run.py`, `scripts/waiver.py` | пачка 1, RN1-9 | да, 02.11.2026: «всегда, в любом месте, дирижёр разбирается в проблеме сам и только если не может, то спрашивает человека» | RN1-8, RN1-3, RN1-4; `words-gates`, `driver-hosts` |
| `findings/20261102-ruchnaya-proverka-ne-vhodit-kak-proekt.md` | находка | ручная проверка не входит на стенд и идёт по шагам вслепую: кейс проходит агент вживую, улики за ним пишет код, всё сомнительное по ходу — аналитику | `scripts/manual_capture.py`, `agents/qa-runner.md`, `agents/qa-failure-analyst.md` | пачка 1, RN1-10 | да, 02.11.2026 (P26): «агент смотрел, что получается по ходу прогона, и записывал все сомнительные места… всё это должно идти аналитику» | EP1-31, EP1-28; RN1-3, RN1-9 |
| `findings/20261102-otvet-gejta-a-bukvoj-na-kartochku-do-seychas-ne-primenyaetsya.md` | находка | ответ «Q9 b» на карточку «до / сейчас» молча не применён (`not_applied: changed_since_answer`), вопрос задан на гейте B ещё дважды | `scripts/contract.py`, `scripts/question_register.py`, `scripts/planning_contract.py`, `scripts/gate_brief.py` | пачка 1, RN1-11 | нет | GW1-43 (регрессия); t-1671 Н-1, t-1672 П-3 |
| `findings/20261102-kandidaty-v-bagi-iz-otvetov-i-koda-ne-dohodyat-do-gejta-b.md` | находка | три кандидата в баги (R-24, R-25, R-26) из ответов гейта A и кода не доходят до гейта B | `agents/qa-failure-analyst.md`, `scripts/gate_brief.py`, `scripts/bug_records.py` | пачка 1, RN1-12 | нет | RN1-11, RN1-17; t-1671 Н-3 |
| `findings/20261102-lestnica-p19-ne-izmerena-ruchnaya-stupen-po-not-measured.md` | находка | деньги (TS-24, P0) и TS-25 отданы ручной ступени по `rung_basis: not_measured`, хотя автоматизируются | `scripts/branch_accounting.py`, `scripts/validate_artifacts.py`, `agents/qa-test-strategist.md` | пачка 1, RN1-13 | нет | RN1-10, RN1-2; t-1671 Н-4 |
| `findings/20261102-gejt-a-sprashivaet-reshyonnoe-na-s1.md` | находка | гейт A снова спросил решённое на S1: Q1 + R-8/R-9/R-10 (4 карточки), Q2, Q3, quick view | `scripts/gate_brief.py`, `scripts/question_register.py`, `agents/qa-requirements-tester.md` | пачка 1, RN1-14 | нет | GW1-43 (регрессия); t-1671 Н-5 |
| `findings/20261102-net-funkcii-slovo-cheloveka-zapisano-propuskom-a-ne-probelom-produkta.md` | находка | слово «нет функции — пробел» записано как waiver окружения и «Skipped by the plan», не пробел продукта (FR-21) | `scripts/gate_brief.py`, `scripts/stage_done.py`, `scripts/report_facts.py`, `references/delivery-reason-owners.json` | пачка 1, RN1-15 | нет | RN1-16; t-1671 Н-7, t-1672 П-19 |
| `findings/20261102-prichina-verdikta-nazvana-po-defektu-kejsa-a-ne-baga-produkta.md` | находка | причина вердикта «не готово» названа по дефекту кейса фабрики, баг продукта не назван | `scripts/delivery_verdict.py`, `scripts/check_delivery.py`, `scripts/delivery_summary.py` | пачка 1, RN1-16 | нет | RD1-21; t-1671 Н-8, t-1672 П-1 |
| `findings/20261102-case-defect-izvesten-na-s5-i-ne-vozvrashchaetsya-na-s4.md` | находка | 11 из 19 красных — дефект кейсов (цена в `GET /api/cart`, поля нет): известен с S5, не возвращён на S4; спорно: дефект кейса или пробел продукта | `agents/qa-case-critic.md`, `agents/qa-automator.md`, `agents/qa-code-critic.md`, `scripts/story_run.py` | пачка 1, RN1-17 | да: дефект кейса или пробел продукта (рекомендация Lead: пробел продукта) | DC1-25; t-1671 Н-9, t-1672 П-2 |
| `findings/20261102-bag-dublikat-otkrytogo-i-chernoviki-po-trebovaniyu-a-ne-po-prichine.md` | находка | BUG-1 дубль открытого XPANBFLFA-140, три черновика на одну причину склеил человек | `scripts/bug_records.py`, `scripts/gate_brief.py`, `agents/qa-failure-analyst.md` | пачка 1, RN1-18 | нет | t-1671 Н-10, t-1672 П-5, П-6 |
| `findings/20261102-bag-vosproizvedyon-no-neopredelyon-povtor-hf8-16.md` | находка | при 8 красных с `repair_verify` отчёт пишет «unconfirmed — nobody has reproduced it» | `scripts/bug_records.py`, `scripts/contract.py` | пачка 1, RN1-19 | нет | HF8-16 (регрессия); t-1671 Н-11 |
| `findings/20261102-kvitanciya-recenzii-perezhivaet-novuyu-versiyu-avtora.md` | находка | рецензия гейта A приписана критику кейсов, не видевшему переписанные TC_021/022/024 | `scripts/controller.py`, `scripts/gate_brief.py`, `scripts/case_versions.py` | пачка 1, RN1-20 | нет | HF8-27; t-1672 П-4 |
| `findings/20261102-playwright-ts-manifest-selektor-id-ekzemplyara-povtor-ep1-37.md` | находка | Playwright TS: манифест вручную, селектор с одним `--grep`, расходятся id экземпляров (43 против 34), квитанции только для pytest | `scripts/manifest_from_tests.py`, `scripts/run_suite.py`, `scripts/manifest_put.py`, `scripts/window_record.py` | пачка 1, RN1-21 | нет | EP1-37 (регрессия); RN1-8; t-1672 П-7, П-8, П-10 |
| `findings/20261102-manifest-put-stiraet-then-bindings-povtor-ep1-39.md` | находка | повторная отправка манифеста стёрла `then_bindings` прошлых окон | `scripts/manifest_put.py` | пачка 1, RN1-22 | нет | EP1-39 (регрессия); t-1672 П-9 |
| `findings/20261102-probely-fabriki-v-bloke-produkta-povtor-rd1-21.md` | находка | в блоке «product side» итоговой сводки 13 `CASE_DEFECT`, пробел стенда и «coverage red — none» | `scripts/delivery_summary.py`, `scripts/check_delivery.py`, `references/delivery-reason-owners.json` | пачка 1, RN1-23 | нет | RD1-21 (регрессия), RD1-19; t-1672 П-11 |
| `findings/20261102-vopros-po-odnomu-kejsu-ostanavlivaet-nezavisimye-stadii.md` | находка | вопрос по одному ручному кейсу держал конвейер 3 ч 50 мин, S7 ждал без зависимости | `scripts/story_run.py` | пачка 1, RN1-24 | нет | RN1-10, RN1-9; t-1672 П-13 |
| `findings/20261102-retro-neverno-meryaet-ozhidanie-i-pererabotku.md` | находка | ретро: «Human wait 2h 46m» при ≈ 7 ч 11 мин, «28 repair rounds» при ≈ 10 возвратах, «no recorded usage» рядом со строкой цены | `scripts/retro_numbers.py`, `references/metrics/catalogue.json` | пачка 1, RN1-25 | нет | CD1-13, CD1-27; t-1672 П-14 |
| `findings/20261102-vyhodnoj-kontrol-okna-s5-proveril-ves-plan.md` | находка | выходной контроль окна S5 судит весь план при ремонте `returned_unaccepted`, дефект фабрики выдан человеку на «да» | `scripts/branch_accounting.py`, `scripts/window_record.py`, `scripts/story_run.py` | пачка 1, RN1-26 | нет | DC1-21, RN1-9; t-1672 П-16 |
| `findings/20261102-kritik-kejsov-ne-proveryaet-razlichaet-li-znachenie-ishody.md` | находка | критик кейсов не проверяет, что значение теста не равно результату коэрсии (Then 1 TC_021 с количеством 1) | `agents/qa-case-critic.md`, `agents/qa-case-designer.md` | пачка 1, RN1-27 | нет | RN1-7, TQ1-25; t-1671 Н-16 |
| `findings/20261102-tickets-you-kept-no-requirement-taken-ne-dokazano.md` | находка | «Tickets you kept: no requirement taken (10)» против 23 упоминаний этих тикетов в реестре (не доказано) | `scripts/gate_brief.py`, `scripts/contract.py` | пачка 1, RN1-28 | нет | RN1-14; t-1671 Н-18 |
| `findings/20261102-rol-pravit-konfig-proekta-v-obhod-hozyaina.md` | находка | роль S5 и дирижёр правили онбординговый `config.json`, откат без двери | `scripts/guard_pre_tool.py`, `scripts/stage_guard.py` | пачка 1, RN1-29 | нет | RN1-3; t-1672 П-21 |
| `findings/20261102-katalog-dubl-qa-factory-qa-factory-ot-s9.md` | находка | S9 создал каталог-дубль `qa-factory/qa-factory/`: путь записи от неверного корня | `scripts/project_decisions.py` | пачка 1, RN1-30 | нет | t-1672 П-22 |
| `findings/20261102-dirizhyor-pereskazyvaet-gipotezu-s5-kak-fakt.md` | находка | дирижёр до триажа назвал красные цены дефектом продукта и отозвал | `skills/qa-story/phases/s5.md`, `references/conductor.md` | пачка 1, RN1-31 | нет | RN1-17, RN1-4; t-1672 П-23 |
| `findings/20261102-kontekst-dirizhyora-perepolnyaetsya-na-oknah-s5.md` | находка | контекст дирижёра растёт с числом окон S5: компакт посреди S5, 82 млн токенов | `scripts/story_run.py`, `scripts/retro_numbers.py` | пачка 1, RN1-32 | нет | SC2-40; t-1672 П-25 |
| `findings/20261102-svodka-dostavki-ne-peresobrana-posle-gejta-b-povtor-rd1-20.md` | находка | `delivery-summary.md` и `ledger.md` не пересобраны после гейта B: «1 с багом» против «4 с багом» | `scripts/story_run.py`, `scripts/delivery_summary.py` | пачка 1, RN1-33 | нет | RD1-20 (регрессия); RN1-23; t-1672 П-17 |
| `findings/20261102-p11-isklyuchenie-pripisano-slovu-cheloveka.md` | находка | исключение скоупа подписано «решение человека», хотя человек правку в корзине не называл; ушла территория Б-1/Б-3 | `scripts/branch_accounting.py`, `agents/qa-requirements-tester.md`, `scripts/question_register.py` | пачка 1, WG1-1 | да, 02.11.2026: поднять до П1 | перенесена из words-gates; RN1-7, RN1-14; t-1666 П-11 |
| B-346 | строка | диета инъекции: постоянная часть промпта ролей урезана (поглощено из дубля RC1-1) | `references/common-rules.md` | пачка 1, RC1-14 | нет | — |
| B-076 | строка | запас до порогов A22/A25 у `qa-code-critic` и `qa-doc-scribe` (поглощено из дубля RC1-1) | `agents/qa-code-critic.md`, `agents/qa-doc-scribe.md` | пачка 1, RC1-14 | нет | — |
| B-072 | строка | набор инструментов диспатча — шаг 1 узла RC1-14 (поглощено из дубля RC1-1) | `scripts/inject_context.py` | пачка 1, RC1-14 | нет | — |
| `findings/20261030-potolki-inekcii-ne-tam-gde-rezhetsya.md` | находка | потолки инъекции A22/A25 меряют не то, что получает роль; мера одна и в сумме | `scripts/audit_factory.py`, `scripts/inject_context.py` | пачка 1, RC1-14 | слово 30.10.2026 | — |
| **Пачка 2: один баг и его проявления** | | | | | | |
| `findings/20261110-odin-bag-mnogo-proyavlenij-bagi-odnoj-prichiny-ne-drobyatsya.md` | находка | баги одной причины заводились по числу падений, не по причине; N1–N8 сделаны кодом, живого прогона N9 нет | `scripts/bug_records.py`, `scripts/gate_brief.py`, `scripts/place_answers.py`, `agents/qa-failure-analyst.md` | пачка 2, RN2-1 | слово 10.11.2026: «живой перепрогон отложи» | RN1-18; t-2187 |

## Входящие

`findings/` этой кучки; их число и дату последней показывает `plans/PILES.md` (собирает `piles.py board`; карточку код не правит).
Каждая новая находка тем же ходом получает строку в пачке этой кучки, которую ещё не взяли, или указатель `перенос: <кучка>/…`
(`piles.py check` (е)); нет такой пачки — открывается следующая со статусом «ожидает».

## Вопросы владельцу

- Слов владельца в пачке нет: исполнение узлов идёт по направлению, выбранному Lead (см. «Что именно менять» в находках).
