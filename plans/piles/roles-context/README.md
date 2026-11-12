# Роли, тексты и контекст (`roles-context`)

приоритет: П3 | фичи: F17, F20 | стенд: нужен (трение меряется прогоном) | зона: `ai-packages/qa-factory/agents/qa-code-critic.md`, `agents/qa-doc-scribe.md`, `agents/qa-test-strategist.md`, `agents/qa-case-designer.md`, `references/common-rules.md`, `references/ahead-cards.json`, `handoffs/vocabulary.yaml`, `scripts/handoff_check.py`, `scripts/guard_pre_tool.py`, `scripts/exit_gate.py`

## Зачем

Сегодня роли читают больше, чем им нужно: общая часть промпта велика, уставы двух ролей упёрлись в пороги размера, а
часть полей, которые роли обязаны писать, никто не читает. Принципы P16 и P17 (меньше e2e, кейс и тест — многие ко
многим) ещё не дошли до уставов всех ролей, а словарь вердиктов критика общий для двух стадий. После первой пачки роли
читают меньше и точнее, уставы несут P16 и P17, лишние поля убраны, тексты охраны и гейта выхода не вводят в заблуждение.

## Что не так сегодня (факты)

- Уставы `qa-code-critic` (1006 байт до порога A22 в 1000) и `qa-doc-scribe` (1015) упёрлись в порог; следующая правка потребует сокращений (`plans/BACKLOG.md:371`; числа сняты в t-048/t-060, текущее состояние проверить по коду).
- Общая часть промпта ролей 17.6K, цель 9K и ≤ 25K на роль; пока работает только храповик A22/A25 (`plans/BACKLOG.md:103`).
- Восемь полей `claims.*`, которые роль пишет и никто не читает (`plans/BACKLOG.md:62`); 108 блоков контроллера с маршрутом `command` не проверены на открываемость двери (`plans/BACKLOG.md:63`).
- `critic_verdicts` в `vocabulary.yaml` общий для S4 и S5 (`plans/BACKLOG.md:152`).
- Карточки AHEAD сократили стратега с 176 ходов и $12.83 до 51 хода и $2.53 в одном замере; на остальных ролях эффект не измерен (находка B-022, дайджест `docs/tasks/specs/reports/t-713-scout-piles-b.md`).
- 11 открытых строк в пачке 1 и 17 находок (дайджест t-713, пересчёт 11 из 11 и 17 из 17 на 13.10).

## Пачки

| № | Что изменится для пользователя | Строки | Размер | Статус | Взял | Ветка | MR |
|---|---|---|---|---|---|---|---|
| 1 | роли читают меньше и точнее (диета инъекции, карточки AHEAD), уставы ролей несут P16/P17, джев-суждения достроены | B-023 | M | закрыта | — | — | `855d4e5c` |
| 2 | на самом сильном сжатии брифа слова человека из ответа на вопрос остаются в брифе, а заметка о брифе не теряется за строкой stderr | — (находки 12.11.2026, узлы RC2-1, RC2-2, RC2-3) | S | ожидает | — | — | — |

Открытое перенесено 01.11.2026 → release-next/1, words-gates/1, onboarding-forge/1, driver-hosts/2, onboarding-forge/2.

Статусы пачки: `ожидает` → `в работе` → `сдано` → `принято` → `закрыта`. Размер — по узлам: S ≤ 4 узлов,
M 5–9, L 10–15 (больше — две пачки). Взятая пачка заморожена: её файл правит только взявший, новое
по теме — файлом в `findings/`.

## Бриф пачки 1

Начать с RC1-1 (диета и пороги A22/A25: любая правка устава ролей упирается в них); RC1-2 и RC1-3 идут после неё, они тоже
правят уставы. Стенд нужен для замера трения (FR-55) после правок. Слово владельца не нужно. Подробно — `batch-1-role-texts.md`,
раздел «Бриф».

## Дороги

Читать по порядку: эта карточка → `batch-1-role-texts.md` → находки узла (колонка «id / файл» ниже) → строки
`plans/BACKLOG.md` 62, 63, 99, 103, 152, 160, 174, 300, 305, 307, 371 → `ai-packages/qa-factory/references/common-rules.md`,
`agents/*.md` (только затронутые узлом роли) → `references/ahead-cards.json` → `PROJECT.md` P14, P16, P17, FR-55 →
`docs/tasks/specs/` (спеки t-048, t-060 про числа порогов).
Слова: `plans/features.json` F17, F20 (поле `words`) и сверх них: `A22`, `A25`, `AHEAD`, `claims.*`, `critic_verdicts`,
`vocabulary.yaml`, `unverifiable`, `manual-human`, `TC-n`, `TURN BUDGET`, `exit_gate`, `handoff_check --fix`,
`coverage_projection`, `manifest_from_tests`, `judge_diff`, `seeded-defect`; «диета инъекции», «устав роли», «карточка
AHEAD», «форма передачи».
Не читать: код стадий, зону `conductor` (формы вопроса человеку), `cost_capture.py`.

## Содержание

Снимок 13.10.2026; пути — от `ai-packages/qa-factory/`; суть строк — из `plans/BACKLOG.md`, находок — из дайджеста t-713. При расхождении авторитетна доска `plans/PILES.md`.

| id / файл | вид | суть (≤ 20 слов) | пути | статус | слово владельца | связи |
|---|---|---|---|---|---|---|
| **Диета инъекции и пороги (пачка 1, RC1-1)** | | | | | | |
| B-346 | строка | `qa-code-critic` на 1006 байт до порога A22, `qa-doc-scribe` на 1015; следующая правка потребует сокращений | `agents/qa-code-critic.md`, `agents/qa-doc-scribe.md` | пачка 1, RC1-1: числа сняты в t-048/t-060 по тексту — проверить по коду | нет | — |
| B-076 | строка | диета инъекции: общая часть 17.6K → 9K, роль ≤ 25K; разрезать `common-rules.md`; пока только храповик | `references/common-rules.md` | пачка 1, RC1-1 | нет | — |
| B-072 | строка | урезать постоянную часть промпта ролей — набор инструментов диспатча | `agents/qa-test-strategist.md` | пачка 1, RC1-1 | нет | — |
| **P16 и P17 в уставах (пачка 1, RC1-2)** | | | | | | |
| B-188 | строка | P16 в тексты ролей: стратег, дизайнер, критики | `agents/qa-test-strategist.md`, `agents/qa-case-designer.md`, `agents/qa-code-critic.md` | пачка 1, RC1-2 | P16 дано 30.09 | — |
| B-133 | строка | стратегу: `unverifiable → manual-human` и поверхность API test-harness в уставе | `agents/qa-test-strategist.md` | пачка 1, RC1-2 | нет | — |
| **Словарь и формы (пачка 1, RC1-3 и RC1-4)** | | | | | | |
| B-161 | строка | `critic_verdicts` в `vocabulary.yaml` общий для S4 и S5; развести или запретить `unverified` в S4 | `handoffs/vocabulary.yaml` | пачка 1, RC1-3 | нет | — |
| B-169 | строка | остатки формы `TC-n` в текстах кода, которые роли не читают как образец | `scripts/run_suite.py`, `scripts/execution_request.py`, `references/ahead-cards.json` | пачка 1, RC1-3: тексты ролей переданы в t-043 E / t-070 по тексту — проверить по коду | нет | — |
| B-023 | строка | восемь `claims.*`, которые роль пишет и никто не читает: три дёшево проверить, остальные убрать | `scripts/handoff_check.py` | перенос: speed-cost/1 (SC1-2) | нет | — |
| B-024 | строка | 108 блоков контроллера с маршрутом `command`: проверить, что дверь открывается | `design/controller-blocks.md` | пачка 1, RC1-5 | нет | — |
| **Охрана и гейт выхода (пачка 1, RC1-6)** | | | | | | |
| B-126 | строка | тексты pre-tool guard: лимит Read 30 КБ, истории про чужую стори, TURN BUDGET, запрет git-конфига срабатывает на текст команды целиком | `scripts/guard_pre_tool.py` | пачка 1, RC1-6 | нет | `onboarding-hooks` |
| B-131 | строка | гейт выхода показывает находки целиком, а не последние три строки | `scripts/exit_gate.py` | пачка 1, RC1-6 | нет | — |
| **Цена контекста (кандидаты пачки 2)** | | | | | | |
| `findings/B-021-tsena-formy-peredachi-po-rolyam-skolko.md` | находка | цена формы передачи по ролям: 90 полей у код-критика | — | перенос: speed-cost/1 (SC1-2) | нет | — |
| `findings/B-022-zamerit-effekt-kartochek-ahead-na-vsekh.md` | находка | замерить эффект карточек AHEAD на всех 12 ролях: стратег 51 ход/$2.53 против 176/$12.83 | `references/ahead-cards.json` | открыто | нет | — |
| **Уставы ролей: содержание (кандидаты пачки 2)** | | | | | | |
| `findings/B-175-progon-cmp1-s4-dizayner-bez-bash.md` | находка | S4, cmp1: дизайнер без Bash оставил `claims.*` как шаблонную строку `<true или false>`; слово в уставе и resume роли без дирижёра | `scripts/handoff_check.py` | перенос: speed-cost/1 (SC1-2) | нет | `driver-controller` |
| `findings/B-190-pereispolzovanie-a-brif-avtomatora-neset-iz.md` | находка | бриф автоматора несёт из S1 «переиспользуй это»; подпункт (б) снят владельцем | — | подпункт (б) снят владельцем (P17) | снято 30.09 | — |
| `findings/B-191-p17-glavnaya-logika-keysy.md` | находка | P17: связь кейс и тест многие-ко-многим, проверить и выровнять | `scripts/manifest_from_tests.py` | исходит от владельца 30.09 | дано 30.09 | — |
| **Трение артефактов и охраны (кандидаты пачки 2)** | | | | | | |
| `findings/B-020-tochechnye-redaktory-artefaktov-manifest-set.md` | находка | точечные редакторы артефактов (`manifest_set`, посекционные), `config_view --keys`; 20 % ходов скаута S1 на питон-патчеры | `scripts/manifest_from_tests.py` | перенос: speed-cost/1 (SC1-2) | нет | — |
| `findings/B-025-dve-uzkie-dveri-khuka-chtenie-plagina.md` | находка | две узкие двери хука (чтение плагина, прямой pytest): расширять дверь, не снимать запрет | `scripts/guard_pre_tool.py` | открыто | нет | — |
| `findings/B-027-obligation-bindings-coverage-projection-vyvodit.md` | находка | `coverage_projection` выводит привязку из `tests[].obligation_ids` | — | открыто | нет | — |
| `findings/B-028-stroki-bez-parametrizatsii-report-row-missing.md` | находка | строки без параметризации (`report row missing`) — дефект запроса, а не блок сдачи | `scripts/run_suite.py` | открыто | нет | — |
| `findings/B-029-fragment-manifesta-nabrannyy-rukoy-rezolvitsya.md` | находка | фрагмент манифеста, набранный рукой, резолвится через pytest (`_why_no_row`) | `scripts/s5_precheck.py` | половина (`--collect`) в CHANGELOG, остаток открыт | нет | — |
| `findings/B-030-rol-perepisyvayushchaya-artefakt-fabriki-cherez.md` | находка | роль, переписывающая артефакт через `json.dump`, теряет ключи | — | открыто | нет | — |
| `findings/B-127-komanda-skauta-dlya-verkhnego-inspection-status.md` | находка | команда скаута для верхнего `inspection_status` | — | открыто | нет | — |
| `findings/B-165-prokhod-po-slovu-cheloveka-cherez-vopros.md` | находка | проход по слову человека через вопрос «поколение пакета / режим прогона» пишет только `defect_found` | — | открыто | нет | `gates-and-words` |
| **Джев-суждения (кандидаты пачки 2)** | | | | | | |
| `findings/B-110-nepostroennye-suzhdeniya-ticket-degenerate-env.md` | находка | непостроенные суждения (`ticket_degenerate`, `env_answer_intent`, `answer_covers_topic`) | `scripts/judge.py` | ждёт решения D-04 (BACKLOG §9) | не найдено | — |
| `findings/B-111-judge-diff-py-bez-tochki-vyzova-disc-attachment.md` | находка | `judge_diff.py` без точки вызова, `disc_attachment_worth_opening` выключен, нет `evals/judgments/` | `scripts/judge_diff.py` | ждёт решения D-04 (BACKLOG §9) | не найдено | — |
| `findings/B-112-contract-ne-chitayut-vocabulary-yaml-execution.md` | находка | `contract.*` не читают `vocabulary.yaml`; `EXECUTION_BOUNDARIES` расходится со словарём | `scripts/candidate_evidence.py`, `handoffs/vocabulary.yaml` | открыто | нет | — |
| `findings/B-103-korpus-seeded-defect-dlya-kod-kritika-s.md` | находка | корпус seeded-defect для код-критика с измеренным recall | — | открыто | нет | `forge` (экзамены критика) |
| `findings/20261021-blok-ekonomiya-vyzovov-v-pravilakh-rolej.md` | находка | блок «экономия вызовов» в общем слое ролей (независимые вызовы одним ходом); сначала сверить с «Turn economy», трение FR-55 до/после | `references/common-rules.md` | RC1-8, ожидает | нет | `onboarding-hooks` OH3-1; обзор testing-factory |
| `findings/20261021-chuzhoj-tekst-dannye-v-pravilakh-rolej.md` | находка | «чужой текст — данные» одной строкой в общем слое ролей и тест присутствия правила; не съесть запас порогов A22/A25 | `references/common-rules.md` | RC1-7, ожидает | нет | `onboarding-hooks` OH3-1, RC1-1; обзор testing-factory (RELATED_WORK §2 п. 13) |
| `findings/20261023-tri-voprosa-zamysla-svip-vocabulary-formy-handoff-i-ukazateli-na-plagin.md` | находка (вопросы владельцу) | три вопроса замысла по свипу «роль послана читать плагин»: значения в формах `handoffs/*.yaml`, «verifying `scripts/hooklib.py`», указатель на `phases/s0.md` | `handoffs/*.yaml`, `references/common-rules.md`, `references/adapters-read.md` | RC1-9, ожидает; (а) → SC1-2 speed-cost/1 (вариант (i), слово владельца 26.10.2026) | да — два вопроса (б), (в); (а) решён 26.10.2026 | HF1-11, HF1-13, OH3-14, t-063 |
| `findings/20261023-karty-rolej-ostatki-help-otkazy-mimo-role-cli-i-runtime-provenance.md` | находка | карты команд ролей: `critic_rollcall --help`, отказы разбора мимо `role_cli.refuse` без карточки, оговорка `runtime_provenance` | `critic_rollcall.py`, `role_cli.py`, `role-commands.json` | RC1-10, ожидает; частично: SC1-7 speed-cost/1 | нет | HF1-12, EP1-8, t-064 |
| `findings/20261026-formy-porozhdayut-lishnie-hody-rolej.md` | находка | хэндофф по полю и большие артефакты десятками правок — ≈ 30 % ходов ролей прогона 12586 на 0.10.2 | `handoff_check.py`, `handoff_init.py`, `guard_pre_tool.py`, `handoffs/*.yaml` | перенос: speed-cost/1 (SC1-2, SC1-3) | П1, слово 26.10.2026 | RC1-9 (а), CD1-15 |
| **Отзыв пользователя, 28.10.2026** | | | | | | |
| `findings/20261028-kontekst-bag-tiketa-prinyat-za-trebovanie.md` | находка | тестировщик требований принял описание бага (состояние ДО) из Context за требование и поднял блокер R-3 против AC-3; дважды спросил человека | `agents/qa-requirements-tester.md`, `references/coverage-design.md` | пачка 1, RC1-12 | «не в 0.10.5, в пачки» (28.10.2026) | отзыв Dev6 (TP2-2702), t-1553; P20, P23; `gates-and-words` (FR-7) |
| **Находки прогона 14857 (0.10.5), 29.10.2026** | | | | | | |
| `findings/20261029-skaut-ostanavlivaetsya-na-konflikte-reshyonnom-v-kommentariyah.md` | находка | скаут S1 остановился на `requirement/code conflict`, снятом комментариями источника, который сам читал «полностью» | `phases/s1.md:341`, `agents/qa-scout.md` | RC1-13, ожидает | нет (П1 0.10.7 — решение Lead) | RC1-12, CX1-14 |
| `findings/20261030-potolki-inekcii-ne-tam-gde-rezhetsya.md` | находка | A22/A25 меряют не то, что получает роль (первое сообщение 34–54 КБ); в рантайме режется только бриф (6 144 Б), драйвер при переборе молча отдаёт ноль правил; мера от цены, молчаливые потери — кодом | `scripts/audit_factory.py`, `scripts/brief_pack.py`, `scripts/story_run.py`, `scripts/inject_context.py`, `references/inject-map.json` | RC1-14, ожидает | да (30.10: «не урезать, а решить; либо поднимаем лимиты»); бюджет в $ — решение владельца | t-1619; `docs/tasks/specs/reviews/20261030-obyom-pravil-roli-i-potolki.md`; RC1-1; OH3-1 |
| `findings/20261101-common-rules-i-slajsy-uchat-tolko-path-value.md` | находка, id — | `common-rules.md` и 13 слайсов учат роль только `path: value`, индексную форму строк списка не называют (F-2 (б) HF8-7) | `references/common-rules.md` | RC1-15, ожидает | нет | RC1-9; RC1-11; HF8-28 |
| **Бриф роли: слова человека и заметка о брифе (пачка 2)** | | | | | | |
| `findings/20261112-slova-cheloveka-iz-otveta-na-vopros-uhodyat-iz-brifa-na-urovne-1.md` | находка, id — | на уровне слов 1 ответ на вопрос теряет слова человека (FR-8, AR-24); заметка о брифе — последняя строка stdout+stderr, а не строка `brief: ` | `scripts/brief_pack.py`, `scripts/story_step.py`, `scripts/tests/test_brief_pack.py` | пачка 2, RC2-1, RC2-2, ожидает | нет | критик на план t-051 (B5, N2); PC2-6 `package-ci/2`; `docs/tasks/specs/reviews/t-042-critic-on-plan.md` |
| `findings/20261112-razdely-masterstva-nesut-stroki-procedury-p27.md` | находка, id — | в разделах `kind: craft` `qa-runner` и `qa-case-critic` стоят строки процедуры (`about:`, `first_look.py put`, фиксированные метки): переносятся в `process`, подъём храповика называется | `agents/qa-runner.md`, `agents/qa-case-critic.md`, `references/role-load.json` | пачка 2, RC2-3, ожидает | нет | калибровка 12.11 п. 13 (проверка 41(d)); P27; AR-20 |

## Входящие

`findings/` этой кучки; их число и дату последней показывает `plans/PILES.md` (собирает `piles.py board`; карточку код не правит).

## Вопросы владельцу

- B-110, B-111: решение D-04 в `plans/BACKLOG.md` §9 — можно ли отправлять данные во внешний сервис для джев-суждений; ответа в BACKLOG не найдено (дайджест t-713). Нужно ли оно для пачки 1: нет, узлы джева — кандидаты пачки 2.
- RC1-9 (23.10.2026, Lead пачки hotfix-12586/1): два вопроса замысла по свипу t-063 — (б) «verifying `scripts/hooklib.py`» в `common-rules.md:142`, (в) указатель на `phases/s0.md` в `adapters-read.md`; вопрос (а) — значения в формах `handoffs/*.yaml` — решён 26.10.2026: вариант (i), исполняет узел SC1-2 пачки `speed-cost/1` (слово владельца 26.10.2026); находка `findings/20261023-tri-voprosa-zamysla-svip-vocabulary-formy-handoff-i-ukazateli-na-plagin.md`.
