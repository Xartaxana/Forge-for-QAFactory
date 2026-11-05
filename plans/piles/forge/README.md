# Forge: система разработки и командная работа (`forge`)

приоритет: П1 | фичи: F19 | стенд: не нужен | зона: `tools/`, `plans/`, `docs/`, `PROCESS/`, `.githooks/`, `.gitlab-ci.yml`, `CLAUDE.md`, `DECISIONS.md`

## Зачем

Два разработчика с их агентами работают над фабрикой одновременно и не мешают друг другу: работа
разложена по кучкам и пачкам, у каждой пачки один взявший и своя ветка, общие файлы (бэклог, журнал,
контекст, CHANGELOG) больше не точка конфликта. Критик проверяет повторы и качество кода, токены
расходуются по мерам D-0035, CI читается скриптом.

## Пачки

| № | Что изменится для пользователя | Строки | Размер | Статус | Взял | Ветка | MR |
|---|---|---|---|---|---|---|---|
| 1 | фундамент командной работы: кучки, пачки, обзор кодом, журнал на разработчика, заморозка бэклога, GitLab-зеркало | B-230, B-454, B-135, B-162 (пути), B-267 (пути) | L | закрыта | владелец (Lead) | `main` (интегратор, узлы в worktree) | `ff353757` https://git.example.com/dev1/yml-text-factory/-/issues/4 |
| 2 | критик сам проверяет повторы и качество кода; измерители дублей и CRAP без остатков; один читатель транскриптов; постановка не уходит с несуществующим путём; билдер коммитит из worktree без обходов | B-419, B-455, B-456, B-449 (потоки, describe_error), B-467, B-204, B-245, B-468, B-469, B-470, B-471, B-472 | L | закрыта | владелец, 09.10.2026 | `pile/forge/batch-2` | `d7f853e0` |
| 3 | долги экзаменов и калибровки (критик, скаут, Lead, судья, недельная калибровка, экзамен экономики) — отложены словом владельца 09.10 до значимого повода | B-457 | S | закрыта | — | — | `855d4e5c` |
| 4 | в пакете без повторов и переростков: один поиск корня проекта, одно чтение JSON, мёртвые вызовы и реэкспорты убраны, длинные функции разбиты по одной | B-309 (г)–(и), B-426 | M | закрыта | владелец, 09.10.2026 | `pile/forge/batch-4` | `4d3cc054` |
| 5 | входящие forge после пачек 2 и 4, копится (D-0044): отчёт воркера — файл, который пишет сам воркер; формат обмена между ролями; детектор «находка без пачки» и дороги в шаблоне; `take`/`close` двигают issue на доске; `close` читает живые доказательства; осевой блок сверяется с картой по подписи; остатки 09–10.10 | — (находки `findings/2026*.md` без B-id; остатки закрытой 454 и B-331 указателем) | M | закрыта | владелец, 14.10.2026 | `pile/forge/batch-5` | `4d28ad32` |
| 6 | входящие forge после взятия пачки 5, копится (слово владельца 14.10: новые находки и починки по ходу работы и калибровки) | — | S | закрыта | — | — | `855d4e5c` |
| 7 | копии и единственные читатели в пакете: одна свёртка строки, один читатель `test_data`, один цикл штампа `waiver` (очередь критиков релиза 0.10.9) | — (находки 02.11.2026, узлы FG7-1…FG7-7) | S | ожидает | — | — | — |

Открытое перенесено 01.11.2026 → release-next/1, driver-hosts/1, execution-report/1, onboarding-forge/1, driver-hosts/2, onboarding-forge/2.

## Дороги

Читать по порядку: эта карточка → файл пачки, которую ведут (`batch-5-vhodyashchie.md`), и копилка (`batch-6-vhodyashchie-2.md`) →
находка узла (колонка «id / файл» ниже) → код зоны по узлу: кучки и пачки — `tools/piles.py` и `tools/test_piles*.py`;
диспатчи и воркеры — `tools/dispatch_gate.py`, `tools/dispatch_manifest.py`, `tools/agent_budget.py`, `tools/transcripts.py`;
журнал и измерения — `tools/journal_validator.py`, `tools/journal_echo.py`, `tools/forge_metrics.py`, `tools/calibration_counts.py`;
осевой блок коммита — `tools/mechanism_gate.py` и `docs/SIBLING_MAP.md` → правила: `PROJECT.md` «Командная работа» и
«Как принимается изменение пакета», `plans/builder-rules.md`, блок хоста в `CLAUDE.md` (пп. 5–7).
Слова: `plans/features.json` F19 (поле `words`) и сверх них: `piles.py check`, `take`, `close`, `board`, `piles-skip`,
`перенос:`, `очередь:`, `Остатки`, `Живые доказательства`, `owns:`, `handoff:`, `dispatch_gate`, `replaces_worker`,
`is_finished`, `calibration_counts`, `mechanism_gate`, `dup_ratchet`, `crap_report`, `hooklib.read_json`; «кучка», «пачка»,
«находка», «входящие», «копилка».
Не читать: `ai-packages/qa-factory/` (кроме узлов, которые правят пакет: F5-7, F5-11), зону `conductor`, журналы
`logs/journal/*.jsonl` вне узла, который их правит.

## Содержание

Снимок 15.10.2026; пути — от корня репозитория; суть строк — из `plans/BACKLOG.md`, находок — из их файлов. При расхождении
авторитетна доска `plans/PILES.md`. Находка без строки в файле пачки — базовая линия детектора (е) `piles.py check`.

| id / файл | вид | суть (≤ 20 слов) | пути | статус | слово владельца | связи |
|---|---|---|---|---|---|---|
| **Пачка 1 (закрыта)** | | | | | | |
| B-230 | строка | организация работы 2–3 разработчиков: кучки, пачки, заморозка бэклога, машинный журнал | `plans/piles/`, `tools/piles.py` | пачка 1, закрыта | нет | — |
| B-454 | строка | остатки слияния журналов: читатели, ключующие голый id задачи, и запасной путь `journal_echo` | `tools/compact_snapshot.py`, `tools/journal_echo.py` | пачка 1, закрыта | нет | находка про остаток 454 ниже |
| B-135 | строка | бюджет загрузки сессии считать вместе с файлами, подключёнными в `CLAUDE.md` через `@` | `tools/session_context.py` | пачка 1, закрыта | нет | — |
| B-162 | строка | таблицы прогонов эксперимента брать из `paths.py` или аргумента (пути) | `experiments/measurers/stage_compare.py`, `experiments/measurers/report_run.py` | пачка 1, закрыта | нет | — |
| B-267 | строка | инструменты сравнения знают копии по словарям в коде (пути) | `experiments/measurers/` | пачка 1, закрыта | нет | — |
| **Пачка 2 (закрыта)** | | | | | | |
| B-419 | строка | критик: повторы и качество кода — постоянная обязанность в файле роли | `.claude/agents/critic.md` | пачка 2, закрыта | нет | экзамен — пачка 3 |
| B-455 | строка | остатки храповика клонов: вердикт зависит от порядка строк базы | `tools/dup_ratchet.py` | пачка 2, закрыта | нет | — |
| B-456 | строка | остатки замера CRAP: `judge()` мутирует имя, `relativise` исполняется дважды | `tools/crap_report.py` | пачка 2, закрыта | нет | — |
| B-449 | строка | настройка потоков (около 25 копий `reconfigure`) и общие куски в `tools/` — один помощник | `tools/` | пачка 2, закрыта | нет | находка про остаток потоков ниже |
| B-467 | строка | один читатель файлов агентов в `tools/`: `_projects_root`, `usage` из хвоста | `tools/transcripts.py`, `tools/dispatch_gate.py` | пачка 2, закрыта | нет | находка про CLI-читатели ниже |
| B-204 | строка | проверка постановки и реестр путей по-разному читают одну и ту же постановку | `tools/dispatch_manifest.py`, `tools/owns_gate.py` | пачка 2, закрыта | нет | — |
| B-245 | строка | пути «given» проверяются до отправки постановки, а не хуком после | `tools/dispatch_manifest.py` | пачка 2, закрыта | нет | — |
| B-468 | строка | остаток работы остановленного по бюджету воркера делает свежий воркер, не Lead | `tools/agent_budget.py` | пачка 2, закрыта | нет | — |
| B-469 | строка | зеркало падает `AttributeError` на кучке с пачками, но без карточки | `tools/piles_gitlab.py` | пачка 2, закрыта | нет | — |
| B-470 | строка | коммит билдера из worktree: проба хуков и AGENTS.md отказывают по чужой вине | `tools/enforcement_probe.py`, `tools/agents_md.py` | пачка 2, закрыта | нет | — |
| B-471 | строка | читатели находок: `piles.Finding` без даты и текста, падение дерева на одном файле | `tools/piles.py`, `tools/forge_metrics.py` | пачка 2, закрыта | нет | — |
| B-472 | строка | гейт переноса «Остатков»: прочерк в подтверждении, цель переноса по форме, проза без маркера | `tools/piles.py` | пачка 2, закрыта | нет | — |
| **Пачка 3 (ожидает)** | | | | | | |
| B-457 | строка | калибровочные случаи пре-релиза 0.9 — вход ближайшей недельной калибровки | `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md` | пачка 3, ожидает | отсрочка 09.10 | — |
| **Пачка 4 (закрыта)** | | | | | | |
| B-309 | строка | измеритель дублирования кода: отчёт, храповик, мерилка длинных функций (пункты г–и) | `tools/dup_report.py`, `tools/dup_ratchet.py` | пачка 4, закрыта | нет | — |
| B-426 | строка | функции, выросшие в диффах 0.9, режутся по списку | `ai-packages/qa-factory/scripts/` | пачка 4, закрыта | нет | — |
| **Находки пачки 5 (взята 14.10)** | | | | | | |
| B-331 | строка (указатель) | перезапуск открытой стадии закрытой истории: дом строки в `driver-controller`, здесь только указатель на находку | `ai-packages/qa-factory/scripts/` | пачка 5, F5-12 | решено 09.10: вопрос человеку перед перезапуском | `driver-controller`, `package-ci` |
| `findings/20261013-pustye-transkripty-subagentov.md` | находка | транскрипты субагентов пустые: отчёт скаута переписывает Lead на самой дорогой модели | `.claude/agents/`, `tools/transcripts.py` | пачка 5, F5-1 | вопрос владельца 13.10 | — |
| `findings/20261013-format-obmena-mezhdu-rolyami.md` | находка | обмен между ролями идёт прозой: дайджесты, брифы, спеки — перерасход токенов на каждом хопе | `.claude/agents/scout.md`, `tools/forge_metrics.py` | пачка 5, F5-2 | вопрос владельца 13.10 | — |
| `findings/20261013-pokrytie-uzlami-id-stroki.md` | находка | покрытие узлами id строки карточки не проверяется кодом | `tools/piles.py`, `tools/test_pile_cards_contents.py` | пачка 5, F5-3 | нет | — |
| `findings/20261013-take-i-close-dvigayut-issue-na-doske.md` | находка | `take` и `close` не двигают issue на доске GitLab: пачка в работе в файлах, на доске её нет | `tools/piles_gitlab.py`, `tools/piles.py` | пачка 5, F5-4 | вопрос владельца 13.10 | — |
| `findings/20261009-close-ne-chitaet-zhivye-dokazatelstva.md` | находка | `close` не читает «Живые доказательства»: правило держится на дисциплине | `tools/piles.py` | пачка 5, F5-5 | нет | — |
| `findings/20261009-osevye-metki-ne-sveryayutsya-s-kartoy.md` | находка | осевой блок коммита сверяется с картой только по номеру оси, подписи «из головы» проходят | `tools/mechanism_gate.py`, `docs/SIBLING_MAP.md` | пачка 5, F5-6 | нет | — |
| `findings/20261009-ci-red-f4-2-fixtures-without-marker.md` | находка | красный CI после F4-2: фикстуры пакетных тестов строят проект без маркера `qa-factory/config.json` | `ai-packages/qa-factory/scripts/tests/` | пачка 5, F5-7 | нет | — |
| `findings/20261009-cap-before-registry.md` | находка | лимит параллельных воркеров живёт в `main()` гейта, реестр owns и снимок критика его не видят | `tools/dispatch_gate.py` | пачка 5, F5-8 | нет | находка про читающий диспатч ниже |
| `findings/20261009-b-454-ostatok-ne-proveren.md` | находка | остатки слияния журналов: три пункта не проверены при закрытии пачки 1 | `tools/journal_validator.py`, `.gitlab-ci.yml` | пачка 5, F5-9 | нет | строка пачки 1 выше |
| `findings/20261009-kritik-t-603-ochered.md` | находка | очередь критика t-603: шесть пунктов остатков пачки 1 | `tools/piles.py`, `tools/journal_validator.py`, `tools/dispatch_gate.py` | пачка 5, F5-10 | нет | — |
| `findings/20261010-puti-ponizheniya-stadii-i-start-pervogo-progona.md` | находка | пути понижения стадии в контроллере не сведены; `started` стадии переживает повторный прогон | `ai-packages/qa-factory/scripts/controller.py` | перенесено: `driver-controller/findings/20261010-puti-ponizheniya-stadii-i-start-pervogo-progona.md` → пачка 1 DC1-8 (подтвердил: владелец, 16.10.2026) | нет | `driver-controller` |
| `findings/20261009-b-331-zakryt-kommentariem.md` | находка | перезапуск открытой стадии закрытой истории «закрыт» только комментарием в коде | `ai-packages/qa-factory/scripts/` | пачка 5, F5-12 (указатель) | решено 09.10: вопрос человеку перед перезапуском | `driver-controller`, `package-ci` |
| **Находки пачки 6 (копится)** | | | | | | |
| `findings/20261014-cap-blokiruet-chitayushchiy-dispatch.md` | находка | гейт параллельных воркеров блокирует читающий диспатч, хотя D-0040 его не считает | `tools/dispatch_gate.py` | пачка 6, F6-1 | нет | — |
| `findings/20261014-pauza-mashiny-bez-sobytiya.md` | находка | пауза машины (сон) ничем не детектируется: журнал молчит 6,5 часов, строки в журнале нет | `tools/journal_echo.py` | пачка 6, F6-2 | нет | — |
| `findings/20261014-calibration-counts-odin-zhurnal-i-zamena-vorkera.md` | находка | `calibration_counts` читает один журнал и не знает ветку `replaces_worker` | `tools/calibration_counts.py` | пачка 6, F6-3 | нет | — |
| `findings/20261014-ledzher-paritata-ustarel-posle-perepisi-proverki-17.md` | находка | леджер паритета ждёт якорь, а проверка 17 переписана под гейты цены | `tools/install_parity.py` | пачка 6, F6-4 | нет | — |
| `findings/20261014-savings-report-bez-bazy-ispolzovaniya.md` | находка | `savings_report.py` падает без таблицы `cc_usage`: проверка 18 неисполнима в подписочном контуре | `tools/savings_report.py` | пачка 6, F6-5 | нет | — |
| `findings/20261014-usage-report-ne-znaet-tsen-claude-5.md` | находка | `usage_report.py` не знает цен семейства Claude 5: все деньги калибровки — нули | `tools/usage_report.py` | пачка 6, F6-6 | нет | — |
| `findings/20261014-is-finished-slep-k-stroke-dlinnee-64-kb.md` | находка | `transcripts.is_finished` слеп к финальной строке длиннее 64 КБ: сдавший воркер считается живым | `tools/transcripts.py` | пачка 6, F6-7 | нет | — |
| `findings/20261014-predikat-limita-dispatch-gate-na-obshchiy-srez.md` | находка | предикат лимита писателей читает диспатч своим построчным сканом, а не общим срезом | `tools/dispatch_gate.py` | пачка 6, F6-8 | нет | — |
| `findings/20261014-import-transcripts-tolko-importerror.md` | находка | импорт `transcripts` в `agent_budget.py` ловит только `ImportError`: `SyntaxError` роняет хук | `tools/agent_budget.py` | пачка 6, F6-9 | нет | — |
| `findings/20261014-kalibrovka-1-slepye-detektory-i-ustarevshaya-navigaciya.md` | находка | калибровка 14.10: слепые детекторы и устаревшая навигация — пять мелких дефектов измерителей | `tools/`, `docs/SIBLING_MAP.md` | пачка 6, F6-10 | нет | — |
| `findings/20261015-detektor-e-ostatki-kritika-t-770.md` | находка | детектор (е): три остатка критика t-770 — носитель «любой статус», удаление пачки, два читателя покрытия | `tools/piles.py` | пачка 6, F6-11 | нет | — |
| `findings/20261015-ostatki-f5-6-okno-audita-i-forma-bloka.md` | находка | остатки F5-6: окно аудита по времени суток, git-раннер гейта, форма блока с ключом в текстах правил | `tools/mechanism_gate.py`, `CLAUDE.md` | пачка 6, F6-12 | нет | — |
| `findings/20261015-ostatki-f5-4-doska-do-pusha-i-ruchnye-statusy.md` | находка | остатки F5-4: зеркало до пуша, команда для `сдано`/`принято`, включение CI-детектора доски | `tools/piles.py`, `tools/piles_gitlab.py` | пачка 6, F6-13 | нет (CI-токен — слово владельца) | — |
| `findings/20261015-forma-daydzhesta-ostatki-kritika-t-808.md` | находка | форма дайджеста v1 — остатки критика t-808: PI_HARNESS учит старой форме, след не сверяется с транскриптом, ручной список имён флагов | `gateway/PI_HARNESS.md`, `tools/digest_form.py` | пачка 6, F6-14 | нет | — |
| `findings/20261015-hop-metrics-ostatki-kritika-t-812.md` | находка | измеритель хопов — остатки критика t-812 (FX-6) и двойники чтения транскриптов (`usage_report`, два glob-цикла, `_manifest_lines`) | `tools/hop_metrics.py`, `tools/transcripts.py`, `tools/usage_report.py` | пачка 6, F6-15 | нет | — |
| `findings/20261015-odin-chitatel-fence-i-karkas-warn-validatora.md` | находка | один читатель fence (`md_table.fence_walk` против сканеров `agents_md`, `md_regions`) и общий каркас WARN валидатора — остатки критика t-815 | `tools/md_table.py`, `tools/journal_validator.py` | пачка 6, F6-16 | нет | — |
| `findings/20261015-f5-7-ostatki-ruchnye-markery-i-tsenzus.md` | находка | F5-7 — остатки: 43 ручных маркера `{}`, четыре локальных помощника, детектор-ценз, m4–m6 критика t-788 | `ai-packages/qa-factory/scripts/tests/harness.py` | пачка 6, F6-17 | нет | — |
| `findings/20261015-slow-tests-spisok-selftest-ustarel.md` | находка | список `SLOW_TESTS` в `selftest.py` разошёлся с замером ночного яруса (18 не в списке, 14 лишних); список — файл данных из замера | `ai-packages/qa-factory/scripts/selftest.py` | пачка 6, F6-18 | нет | — |
| `findings/20261016-is-finished-sdacha-pered-korotkoy-strokoy.md` | находка | `transcripts.is_finished` не видит сдачу, за которой идёт короткая строка: целой гарантирована только последняя строка | `tools/transcripts.py`, `tools/test_transcripts.py`, `tools/test_handback_extract.py` | пачка 6, F6-19 | нет | — |
| `findings/20261016-journal-echo-i-tier-echo-bez-transcripts-lozhatsya-tselikom.md` | находка | `journal_echo`/`tier_echo` без `transcripts` ложатся целиком: валидация журнала гибнет из-за читателя транскриптов | `tools/journal_echo.py`, `tools/tier_echo.py`, `tools/permission_audit.py` | пачка 6, F6-20 | нет | — |
| `findings/20261016-savings-report-ekonomiya-100-pri-nulevyh-tsenah.md` | находка | `savings_report` печатает экономию 100 %, когда фактическая цена ходов не посчитана (нулевые цены Claude 5) | `tools/savings_report.py`, `tools/test_savings_report.py` | пачка 6, F6-21 | нет | — |
| `findings/20261016-yakorya-pariteta-rolevyh-faylov-ustareli-posle-t-754.md` | находка | шесть якорей паритета ролевых файлов устарели после t-754; `install_parity --check` не на пути исполнения | `tools/install_parity_anchors.json`, `.gitlab-ci.yml` | пачка 6, F6-22 | нет | — |
| `findings/20261016-svyortka-usage-report-na-request-usages-tsena-otkata-modeli.md` | находка | свёртка `usage_report` на `request_usages` меняет цену запроса с откатом модели — правила цены нет ни у одного читателя | `tools/transcripts.py`, `tools/usage_report.py` | пачка 6, F6-23 | нет | — |
| `findings/20261016-tseny-claude-5-i-mnozhiteli-kesha-po-modeli.md` | находка | цены Claude 5.x по слову владельца 16.10; множитель чтения кэша — по модели, один общий завышает 5.x | `tools/model_prices.json`, `tools/usage_report.py` | пачка 6, F6-24 | нет | — |
| `findings/20261016-board-check-nochnoy-dzhob-po-slovu-vladeltsa.md` | находка | `board-check` включается ночным джобом (слово владельца 16.10; `GITLAB_TOKEN` создана) | `.gitlab-ci.yml`, `tools/test_ci_layout.py` | пачка 6, F6-25 | нет | — |
| `findings/20261016-parallel-po-story-run-pri-raznyh-funkciyah-d-0048.md` | находка | параллель по `story_run.py` при непересекающихся функциях в `owns` (D-0048): (б) узнаёт форму со списком функций | `tools/piles.py`, `tools/dispatch_manifest.py`, `PROJECT.md` | пачка 6, F6-26 | нет | — |
| `findings/20261019-boot-budget-ne-schitaet-import-claude-md.md` | находка | бут-бюджет не считает `@import` CLAUDE.md: PROJECT.md и индекс правил (45 КБ) грузятся мимо меры | `tools/session_context.py` | пачка 6, F6-27 | нужно: порог слоя с импортами | — |
| `findings/20261020-forge-check-krasnyj-tri-pusha-karta-os-20-pachki-2-session-context.md` | находка | `forge-check` красный три пуша: ключ оси 20 карты, пачки codex/collect 2 без «Бриф» и «Содержания», `session_context` на Linux | `docs/SIBLING_MAP.md`, `plans/piles/`, `tools/session_context.py` | пачка 6, F6-28 | нет | — |
| `findings/20261027-sibling-map-dolgi-osey-posle-relisa-0-10-3.md` | находка | карта `SIBLING_MAP.md` должна семь пунктов по ревью 0.10.3: строки пяти осей и две новые оси | `docs/SIBLING_MAP.md` | пачка 6, F6-41 | нет | t-1277, t-1286, t-1296, t-1310, t-1318, t-1319, t-1320 |
| `findings/20261027-dolya-testov-v-diffah-i-tsena-razrabotki.md` | находка | доля тестов в диффах узлов высока (N-1: оценка ~95/~300 строк, 65 проверок): проверить, почему и насколько это замедляет разработку | `plans/builder-rules.md`, `CLAUDE.md` (правило 11) | пачка 6, F6-42, F6-52 | нет | t-1376, t-1358, t-1359, t-1371…t-1375 |
| **Остатки пачек 2 и 4 (названы в тексте закрытых пачек)** | | | | | | |
| `findings/20261009-b-449-stream-copies-remainder.md` | находка | остаток потоков: 16 копий настройки в звеньях цепи, 14 в `experiments/`, одна в `gateway/` | `tools/`, `experiments/`, `gateway/` | пачка 2, закрыта | нет | строка пачки 2 о потоках выше |
| `findings/20261009-transcripts-cli-readers.md` | находка | читатели транскриптов вне хуков (CLI) и раскладка workflows — очередь после общего читателя | `tools/transcripts.py` | пачка 2, закрыта | нет | строка пачки 2 о читателе транскриптов выше |
| `findings/20261009-f4-2-outside-walks-dashboard-fallback.md` | находка | после F4-2 остаются 11 внешних обходов корня и откат дашборда к маркеру выше стори | `tools/runtime_paths.py` | пачка 4, F4-2 | нет | — |
| `findings/20261009-calibration-counts-null-v-trojke.md` | находка | `calibration_counts`: `rejected` с `agent: null` роняет отчёт `TypeError` в сортировке | `tools/calibration_counts.py` | пачка 4, закрыта | нет | — |
| `findings/20261009-driver-golden-ne-rabotaet-na-main.md` | находка | `driver_golden.py` непригоден на `main`: отказывает на нелитеральном списке и не нормализует штамп | `ai-packages/qa-factory/scripts/tests/driver_golden.py` | пачка 4, закрыта | нет | `driver-controller` (golden драйвера) |
| `findings/20261009-forge-4-ostatok-dlinnye-funktsii.md` | находка | остаток класса «длинные функции»: следующие переростки, контекст-объект, мерилка глубины | `tools/crap_report.py` | пачка 4, закрыта | нет | — |
| `findings/20261009-forge-4-ostatok-klony.md` | находка | остаток клонов: читатели JSON, карта «вариант → слово», строка «the person wrote» | `ai-packages/qa-factory/scripts/` | пачка 4, закрыта | нет | — |
| `findings/20261010-dlinnye-funktsii-posle-volny-1.md` | находка | длинные функции и глубокая вложенность, оставшиеся после волны 1 остатка | `ai-packages/qa-factory/scripts/` | пачка 4, закрыта | нет | — |
| `findings/20261010-json-readers-outside-the-list.md` | находка | читатели JSON вне списка и прочие остатки класса клонов после R1/R2 | `ai-packages/qa-factory/scripts/` | пачка 4, закрыта | нет | — |
| **Старые находки по строкам бэклога (без пачки, базовая линия)** | | | | | | |
| `findings/B-100-raskatka-ustanovlen-0-7-9-v-pakete-0-7-19.md` | находка | раскатка: установлен 0.7.9, в пакете 0.7.19 и ветка драйвера | `ai-packages/qa-factory/` | открыто | нет | — |
| `findings/B-102-protsedura-consistency-review-pered-relizom-kak.md` | находка | процедура consistency-review перед релизом как чек-лист: четыре агента по слайсам | `docs/RUNBOOK.md` | открыто | нет | — |
| `findings/B-106-publikatsiya-stranits-kb-iskhodniki-v-kb.md` | находка | публикация страниц КБ: исходники в `kb/` | `kb/` | открыто | нет | — |
| `findings/B-136-tools-factory-rules-index-py-staged-pre-commit.md` | находка | `factory_rules_index.py --staged`: pre-commit сверяет индекс и правила из индекса git | `tools/factory_rules_index.py` | открыто | нет | — |
| `findings/B-137-tools-factory-rules-index-py-stroka-vida-fr-n-s.md` | находка | `factory_rules_index.py`: строка с дефисом вместо длинного тире не должна молча выпадать | `tools/factory_rules_index.py` | открыто | нет | — |
| `findings/B-140-experiments-bench-13797-check-all-contracts-py.md` | находка | `check_all_contracts.py`: строки-константы и повествования под прогон 13797 | `experiments/measurers/check_all_contracts.py` | открыто | нет | — |
| `findings/B-143-b-011b-experiments-bench-13797-code-friction-py.md` | находка | `code_friction.py` импортирует classify, turns_of и friction из соседнего инструмента | `experiments/measurers/code_friction.py` | открыто | нет | — |
| `findings/B-157-kommitit-prinyatye-temy-po-khodu-a.md` | находка | коммитить принятые темы по ходу, а не всё в конце: масса ломает свидетелей | `docs/`, `plans/builder-rules.md` | открыто | нет | — |
| `findings/B-162-instrumenty-eksperimenta-derzhat-zhestkie.md` | находка | инструменты эксперимента держат жёсткие таблицы прогонов; новый прогон требует правки кода | `experiments/measurers/` | открыто | нет | строка пачки 1 о таблицах прогонов выше |
| `findings/B-173-merilka-stage-compare-py-plan-rows-iz-test-plan.md` | находка | мерилка `stage_compare.py`: `plan_rows` из `test-plan.md` равен None при 14 строках | `experiments/measurers/stage_compare.py` | открыто | нет | — |
| `findings/B-174-progon-cmp1-s1-otvety-na-s1-gap.md` | находка | прогон cmp1, S1: ответы на `s1_gap` дважды ушли дирижёру | `experiments/measurers/` | открыто | нет | `conductor` |
| `findings/B-185-kachestvo-keysov-obzor-t-081-po-trem.md` | находка | качество кейсов: в каждом прогоне 13797 есть Then, чей вход не определён | `experiments/measurers/` | открыто | нет | — |
| `findings/B-200-sistema-razrabotki-khuki-repozitoriya-v-claude.md` | находка | хуки репозитория в `.claude/settings.json` вызываются относительным путём | `.claude/settings.json` | открыто | нет | — |
| `findings/B-202-sistema-razrabotki-bolshaya-pravka-sdaetsya.md` | находка | большая правка сдаётся критику законченными кусками, а не целиком в конце | `plans/builder-rules.md` | открыто | нет | — |
| `findings/B-203-sistema-razrabotki-zamer-khukov-t-087.md` | находка | замер хуков (t-087): задержка Edit и Write, низкий приоритет | `experiments/dev-speed/hook-latency.md` | открыто | нет | — |
| `findings/B-215-reliz-sleduyushchaya-kopiya-paketa-v-testproject1.md` | находка | релиз: следующая копия пакета в `QAFactory` обязана удалить лишнее | `docs/RUNBOOK.md` | открыто | нет | — |
| `findings/B-229-skill-otchet-proekta-o-fabrike-v.md` | находка | скилл «отчёт проекта о фабрике в нашу команду» в формате входящих | `ai-packages/qa-factory/skills/` | открыто | решает владелец | вопросы владельцу ниже |
| `findings/B-234-onbording-vtyagivaet-sushchestvuyushchie-pravila.md` | находка | онбординг втягивает существующие правила проекта (владелец 01.10) | `ai-packages/qa-factory/scripts/onboard_apply.py` | открыто | нет | `onboarding-hooks` |
| `findings/B-236-snimok-s0-i-rest-chtenie-odnogo-tiketa.md` | находка | снимок S0 и REST-чтение одного тикета расходятся, и никто этого не говорит | `ai-packages/qa-factory/scripts/ticket_light.py` | открыто | нет | `stand-and-sources` |
| `findings/B-237-spiski-i-kommentarii-roli-otdayutsya-strochnoy.md` | находка | списки и комментарии роли отдаются строчной формой, не JSON-массивами объектов | `ai-packages/qa-factory/scripts/` | перенос: speed-cost/1 (SC1-3, SC1-9) | нет | — |
| `findings/B-243-sistema-razrabotki-publikatsiya-v-kb-kodom.md` | находка | публикация в КБ кодом по REST с персональным токеном | `tools/kb_publish.py` (removed at the move) | открыто | нет | — |
| `findings/B-244-sistema-razrabotki-fabrika-zapusk-progona.md` | находка | запуск прогона из CI с конкуррентностью по стори, низкий приоритет | `.gitlab-ci.yml` | открыто | нет | — |
| `findings/B-252-login-by-code-u-manual-capture-ui.md` | находка | `login by code` у `manual_capture ui` говорит «ok» до приземления, следующий `goto` обрывает вход | `ai-packages/qa-factory/scripts/manual_capture.py` | открыто | нет | — |
| `findings/B-253-melochi-repetitsii-02-10-spisok-chinit-paketom.md` | находка | мелочи репетиции 02.10: список, чинить пакетом | `ai-packages/qa-factory/scripts/` | открыто | нет | — |
| `findings/B-309-izmeritel-dublirovaniya-koda-vladelets-04-10.md` | находка | измеритель дублирования кода (владелец 04.10: «починим в одном месте, а в другом забудем») | `tools/dup_report.py` | открыто | слово владельца 04.10 | строка пачки 4 выше |
| `findings/B-334-u-tools-controller-blocks-gen-py-net-testa-do.md` | находка | у `controller-blocks-gen.py` нет теста; до миграции в нём был зашит путь чужой машины | `tools/controller-blocks-gen.py` | открыто | нет | — |
| `findings/B-367-tools-journal-echo-py-pri-sliyanii-po-prezhnemu.md` | находка | `journal_echo.py` при слиянии по-прежнему проверяет через `decide()` и печатает хвост | `tools/journal_echo.py` | открыто | нет | — |
| `findings/20261020-opisanie-arhitektury-fabriki-i-pravilo-ne-lomat.md` | находка (слово владельца) | одно описание архитектуры фабрики (четыре цели, носители, детекторы) и правило CLAUDE.md «изменения не ломают архитектуру»; пример — риск-эрии 28fc7170 | `design/architecture.md` (новый), `CLAUDE.md`, критик-бриф, `designer.md`, гейт | пачка 6, F6-29 | да (20.10 18:5x) | `onboarding-hooks` OH1-10; t-1160 |
| `findings/20261021-ostatki-pachki-kopyatsya-strokami-bez-ispolnitelya.md` | находка (решение владельца) | «Остатки» пачки копятся строками без исполнителя: очередь критика при слиянии без узла, «взял» и гейта до `close`; ключ `сделано:`/`узел:`/`перенос:` обязателен при записи (узел F6-30) | `tools/piles.py` | открыто | да | — |
| `findings/B-267-instrumenty-sravneniya-znayut-kopii-po-slovaryam.md` | находка | инструменты сравнения знают копии по словарям; `prepare_copy.py` печатает строку старта с `cd` | `experiments/measurers/` | открыто | нет | строка пачки 1 о копиях выше |
| `findings/20261021-reliz-bot-semver-po-yarlyku-mr.md` | находка | релиз-бот в CI в режиме preview: версия по ярлыку MR, сборка CHANGELOG, заметка релиза, проверка «изменились только релизные файлы»; тег и публикация — по слову владельца | `scripts/release_fingerprint.py`, `scripts/changelog_assemble.py`, `.gitlab-ci.yml` | пачка 6, F6-31 | нет (публикация и тег — по слову владельца при взятии узла) | обзор testing-factory (RELATED_WORK §2 п. 11) |
| `findings/20261021-uroven-proverki-static-simulated-live.md` | находка | уровень проверки изменения static / simulated / live с ограничениями: словарь и пометка уровня в таблице «Живые доказательства» пачки; старые строки без уровня остаются валидными | `plans/piles/_template/batch.md`, `tools/piles.py` | пачка 6, F6-32 | нет | обзор testing-factory (RELATED_WORK §2 п. 13, K11) |
| `findings/20261021-nositeli-roli-odin-vladelec-bez-protivorechij.md` | находка | 31 файл задаёт роли, 4 противоречат D-0056, 9 полных дублей, 22 вне карты: один владелец на аспект роли, остальные указатели, новая ось 22 карты | role-файлы, `plans/builder-rules.md`, `docs/tasks/critic-diff-brief.md`, `CLAUDE.md`, `PROJECT.md`, `docs/SIBLING_MAP.md` | пачка 6, F6-33 | развилка храповиков решена Lead (dup/lint у билдера) | вопрос владельца 21.10; скаут t-1205 |
| `findings/20261021-kanon-pachki-zhivet-tolko-v-proze.md` | находка | BATCH CANON определён только словами: нет скрипта и строки CI, рецепт докера в памяти; `tools/batch_canon.py` со свидетелем формы `accepted.witness` | `tools/batch_canon.py`, `docs/RUNBOOK.md` | пачка 6, F6-34 | нет | скаут t-1205 Q3; D-0056 (3) |
| `findings/20261023-izolirovannyj-worktree-rezhetsya-ot-main-a-ne-ot-vetki-pachki.md` | находка | worktree билдера режется от `main`, а не от ветки пачки: четыре билдера пачки hotfix-12586/1 начинали с чужой базы | `tools/dispatch_gate.py`, `docs/RUNBOOK.md` | пачка 6, F6-35 | нет | F6-1, t-061, t-062, t-064, t-065 |
| `findings/20261023-hooki-sessii-privyazany-k-cwd-cd-v-paket-otbivaet-kazhdyj-vyzov.md` | находка | хуки сессии запускают `python tools/<x>.py` относительно cwd: `cd` в пакет отбивал каждый вызов, пока владелец не вернул папку | `.claude/settings.json`, `tools/` | пачка 6, F6-36 | нет | — |
| `findings/20261023-put-handoff-v-dispatche-ne-sverenyi-s-rolyu-i-izolyatsiej.md` | находка | путь `handoff:` не сверен с ролью и изоляцией: отчёт критика отбит `handoff_gate`, отчёты worktree-билдеров собирает Lead | `tools/dispatch_manifest.py`, `docs/RUNBOOK.md` | пачка 6, F6-37 | нет | R11-f, R11-h, F5-1 |
| `findings/20261024-worktree-ne-udalyayutsya-posle-sliyaniya.md` | находка | worktree билдеров и агентов не удаляются после слияния ветки: 261 копия к 24.10; нужен механизм удаления | `tools/worktree_sweep.py`, `.githooks/post-merge`, `tools/piles.py`, `tools/session_context.py` | пачка 6, F6-38 | слово 24.10.2026 | F6-35, «Kill leftover processes after each merge» |
| `findings/20261026-worktree-sweep-ostatok-posle-f6-38.md` | находка | остаток F6-38: архивные ссылки не чистятся, второй резолвер основной копии, гонка detached, дубль парсера porcelain, итог при пропущенном prune | `tools/worktree_sweep.py`, `tools/wiring_check.py`, `tools/gitcmd.py`, `tools/compact_snapshot.py` | пачка 6, F6-39 | нет | F6-38, ось 10 |
| `findings/20261026-id-sdelan-v-chuzhoj-pachke-net-hoda-zakrytiya.md` | находка | id, сделанный в чужой пачке, нельзя закрыть: `close` и проверка (а) читают указатель по-разному, B-164 сделан в conductor/1, дом — driver-controller | `tools/piles.py`, `tools/test_piles_close.py`, `tools/test_piles.py`, `plans/piles/_template/batch.md` | пачка 6, F6-40 | нет | B-164, F5-12, t-717 Р6 |
| `findings/20261027-docker-kanon-arhiv-crlf-run-py-cmd.md` | находка | исходники docker-канона из `git archive` на Windows пришли с CRLF: `hooks/run-py.cmd` сломан в Linux, первый канон 0.10.3 недействителен | `docs/RUNBOOK.md`, `tools/batch_canon.py` | пачка 6, F6-43 | нет | F6-34, канон 0.10.3 |
| `findings/20261027-a19-nad-realnym-paketom-tolko-v-install-smoke.md` | находка | A19 над реальным пакетом идёт только в ночном `install_smoke`: роль без `## Procedure` прошла все MR, 0.10.3 вышел с этим | `.gitlab-ci.yml`, `scripts/audit_factory.py` | пачка 6, F6-44 | нет | канон 0.10.3; `run-honesty` RH1-2 |
| `findings/20261027-architecture-none-gate-proveryaet-nalichie-stroki-a-ne-pravdu.md` | находка | гейт архитектуры проверяет наличие строки `architecture:`, не правдивость: `none` над коммитом `8a04c661` с изменениями пакета прошёл | `tools/architecture_gate.py` | пачка 6, F6-45 | нет | D-0055, коммит `8a04c661` |
| `findings/20261028-warn-density-dokstring-lzhet-pro-subagentov.md` | находка | докстринг `warn_density.py`: «`hook_additional_context` субагентов не пишется» — замер 28.10 показал, что пишется | `tools/warn_density.py` | пачка 6, F6-46 | нет | speed-cost: класс немого вывода хуков |
| `findings/20261028-padayushchij-kanon-test-pryachet-dalnejshie-krasnye.md` | находка | упавший файл канона обрывает свои ключи: читать stderr целиком, не последнюю строку | `docs/RUNBOOK.md`, `tools/batch_canon.py` | пачка 6, F6-47 | нет | F6-34, F6-43 |
| `findings/20261028-testy-s-pustym-stderr-maskiruet-warn-once.md` | находка | тесты «stderr пуст» зелёные локально из-за маркера `warn_once`, красные в свежем CI (t-1407, t-1411) | `scripts/tests/`, `tools/` | пачка 6, F6-48 | нет | speed-cost 3/SC3-6 |
| `findings/20261028-globy-f04-f05-v-features-json-perekryvayutsya.md` | находка | глобы F04 и F05 в `features.json` перекрываются; чинилось правкой глобов вслепую (t-1411/t-1412) | `plans/features.json`, `tools/forge_metrics.py` | пачка 6, F6-49 | нет | t-1411, t-1412 |
| `findings/20261028-kanon-pachki-ne-dolshe-chasa-v-ci.md` | находка | BATCH CANON шёл часами на локальном докере (bind mount ×5+, 9 ложных таймаутов): норма — не дольше часа, всё возможное в CI | `.gitlab-ci.yml`, `scripts/selftest.py`, `tools/batch_canon.py`, `docs/RUNBOOK.md` | пачка 6, F6-50 | слово 28.10.2026 | F6-34, F6-43, F6-47, F6-18, F6-42 |
| `findings/20261028-testy-ne-derzhat-styki-stadij.md` | находка | тестов много, а стыки стадий не держат: гейт проверяет то, чего роль не ожидает (17 отказов формы дайджеста в 12586) или что никто не пишет (квитанции S5) | `references/`, `scripts/tests/`, `scripts/selftest.py` | пачка 6, F6-51 | слово 28.10.2026 | F6-42, F6-50, hotfix-12586/4 |
| `findings/20261030-strochki-sibling-map-os-7-klyuch-pamyati-i-stroka-120-zhdut-gejta-lead.md` | находка | две правки `docs/SIBLING_MAP.md` (ось 7: ключ памяти сбора; строка `:120`) ждут Lead-гейта | `docs/SIBLING_MAP.md` | пачка 6, F6-53 | нет | EP1-23 B2; GW1-10 |
| `findings/20261031-dubli-s6-odin-mehanizm-vmesto-semi-pravok.md` | находка | семь копий одного знания в диффе S6 (`_gate_a_decided`, `_labels`, `project_config`, `_walk_records`, `_running_stage`, cut-list); вопрос Lead «один механизм или семь правок» | `scripts/branch_accounting.py`, `scripts/report_facts.py`, `scripts/validate_artifacts.py` | пачка 6, F6-54 | нет | критик S6 0.10.7 F-11; F6-55 |
| `findings/20261031-kopii-chteniya-golovy-komandy-evidence-ref-issue-i-konstanty-resume-doors.md` | находка | `NAME=` читается пятью способами, узкий `head_program` не доходит до гарда; код причины подстрокой слов `evidence_ref_issue`; копии статусов в `stage_guard` | `scripts/adapter_forms.py`, `scripts/guard_pre_tool.py`, `scripts/bug_records.py`, `scripts/stage_guard.py` | пачка 6, F6-55 | нет | F6-54 |
| `findings/20261031-s6-driver-state-na-puti-skilla-svoj-fajl-i-klyuchi-tolko-drajvera.md` | находка | путь скилла пишет в `driver-state.json` драйвера (два писателя файла, ключ один); ключи только-драйвера `shown_doors`, `shown_exploratory`, `last_rehearsal_doors`, `delivery` на пути скилла читаются как «нет» (ось 5); константа `RUN_MODE_ENV` в трёх местах | `scripts/gate_brief.py`, `scripts/story_run.py`, `scripts/report_facts.py`, `references/artifact-writers.json` | пачка 6, F6-56 | нет | F6-54 |
| `findings/20261031-s6-predprosmotr-gejta-a-gasit-stroku-new-since.md` | находка | печать гейта A до решения перезаписывает запись «показано», и настоящая цитата теряет строку `new since you last saw this list` | `scripts/gate_brief.py` | пачка 6, F6-57 | нет | F6-56 |
| `findings/20261031-pravilo-zhurnala-9a-net-dveri-dlya-diapazona-id-parallelnoj-vetki.md` | находка, id — | правило журнала 9а (max+1) без двери для диапазона id параллельной ветки; обход строкой `t-499` | `tools/journal_validator.py` | F6-58, ожидает | нет | — |
| `findings/20261101-slovo-vladeltsa-provodit-mr-relizov-cherez-krasnyj-shag-zhurnala-v-ci.md` | находка, id — | два клона писали один файл журнала; CI-валидатор красный на MR релизов, двери нет; слово владельца 01.11.2026 провело MR !12 | `tools/journal_validator.py`, `tools/piles.py` | F6-59, ожидает | да: вариант (а)/(б) | F6-58 |
| `findings/20261102-one-line-devyat-kopij-svertki-stroki.md` | находка, id — | свёртка текста в одну строку с обрезкой написана девять раз; выживший `contract.one_line(text, limit=None)` | `scripts/contract.py`, девять модулей по находке | пачка 7, FG7-1 | нет | t-764 Q5, t-744 |
| `findings/20261102-chitateli-test-data-mimo-odnogo.md` | находка, id — | `env_probe.data_cleanup` и `audit_factory.py:766` читают `test_data` мимо `config_contract.test_data_states` | `scripts/env_probe.py`, `scripts/audit_factory.py`, `scripts/brief_pack.py` | пачка 7, FG7-2 | нет | t-724 m-2, TQ1-11 |
| `findings/20261102-kopii-v-waiver-i-testovyh-strokah-rn1-9-ep1-4.md` | находка, id — | три копии цикла штампов в `waiver.py` и три копии тестовой строки `HANDED_ROW` | `scripts/waiver.py`, `scripts/tests/story_step_common.py` | пачка 7, FG7-3 | нет | t-764 m-6, t-760 |
| `findings/20261103-worktree-sweep-polnaya-uborka-posle-sliyaniya.md` | находка, id — | слитые worktree копятся: хук убирает 5 копий за слияние; полная фоновая уборка после слияния и в `close` | `tools/worktree_sweep.py`, `tools/session_context.py`, `tools/piles.py` | пачка 7, FG7-4 | да, 03.11.2026 | t-1739, t-1210 |
| `findings/20261104-tsena-uzla-s-brakom-v-forge-metrics.md` | находка, id — | журнал не сводит цену узла: все попытки, фикс-раунды, критик, повторные диспатчи по `task_id`; топ-5 дорогих узлов с причиной | `tools/forge_metrics.py`, `tools/test_forge_metrics.py` | пачка 7, FG7-5 | да, 04.11.2026 | FG7-6, FG7-7; P18, FR-51 |
| `findings/20261104-nedelnyj-obzor-raskhoda-skautom-pered-kalibrovkoj.md` | находка, id — | обзор расхода делает Lead руками, калибровка просрочена; один отчёт скаута по журналу за неделю — вход калибровки | `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md` | пачка 7, FG7-6 | да, 04.11.2026 | FG7-5, FG7-7 |
| `findings/20261104-khody-koordinatora-na-uzel-v-tsene.md` | находка, id — | ответы воркерам и повторные диспатчи не входят в цену узла; `forge_metrics` считает ходы координатора по `task_id` | `tools/forge_metrics.py`, `tools/test_forge_metrics.py` | пачка 7, FG7-7 | да, 04.11.2026 | FG7-5; правило 12 `CLAUDE.md` |

## Входящие

`findings/` этой кучки; число и дату последней показывает `plans/PILES.md`.

## Вопросы владельцу

- B-229 (отчёт проекта о фабрике в формате «входящих»): что можно выносить из проекта — решает владелец.
- B-331 (находка `findings/20261009-b-331-zakryt-kommentariem.md`): решено владельцем 09.10 — открыть работу: перед перезапуском открытой стадии закрытой истории фабрика спрашивает человека (причина, доработки, «перезапустить / оставить / сделаю сам»); узел в пачку кучки `package-ci`.
- (отвечено 09.10) недельная калибровка F3-4 — после закрытия пачки 4; приоритет пачки 3 — П3.
