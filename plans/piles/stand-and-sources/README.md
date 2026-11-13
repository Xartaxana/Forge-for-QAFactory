# Стенд, источники, HTTP, Jira (`stand-and-sources`)

приоритет: П2 | фичи: F01, F02, F03 (стенд), F18 | стенд: нужен | зона: `ai-packages/qa-factory/scripts/http_client.py`, `scripts/source_inventory.py`, `scripts/ticket_adapter.py`, `scripts/stand_identity.py`, `scripts/stand_health.py`, `scripts/readiness.py`, `scripts/source_exclusions.py`, `scripts/external_writes.py`, `scripts/execution_request.py`, `scripts/runtime_probe.py`

## Зачем

Сегодня фабрика местами читает ошибки HTTP неверно (чужой 404 на тикете, протухший токен выглядит как «MR не найден»),
хранит несколько описаний «как стенд логинится» и «какая сборка стоит», а свежесть тикета проверяет по-разному на
двух путях. После первой пачки HTTP-ошибки читаются верно и называют лекарство, идентичность стенда одна, тикет и его
источники берутся по API и не расходятся со снимком, а запись в Jira идёт в её разметке.

## Что не так сегодня (факты)

- Протухший токен на пути VCS/MR неотличим от «MR не найден»; для Jira это уже сделано кодом выхода 5 (`plans/BACKLOG.md:198`).
- `ticket_adapter.py freshness` превращает любое исключение в код 3 и при `--json` не печатает объект ошибки (`plans/BACKLOG.md:409`); `check_is_due` вызывается только тестами (`plans/BACKLOG.md:413`).
- Гейт `source_freshness` берёт ответ из голого слова рантайма вместо лестницы проб (`plans/BACKLOG.md:241`).
- Есть два описания «как стенд логинится»: `environment.access` и рецепт ручного захвата (`plans/BACKLOG.md:219`).
- Префикс `env:` у секрета снимает доктор, а клиент Jira — нет (`plans/BACKLOG.md:348`).
- 13 открытых строк в пачке 1 и 10 находок (дайджест `docs/tasks/specs/reports/t-713-scout-piles-b.md`, пересчёт 13 из 13 и 10 из 10 на 13.10).

## Пачки

| № | Что изменится для пользователя | Строки | Размер | Статус | Взял | Ветка | MR |
|---|---|---|---|---|---|---|---|
| 1 | HTTP-ошибки читаются верно, стенд-идентичность одна, тикет и его источники берутся по API и не расходятся со снимком, запись в Jira — в её разметке | B-120, B-163 | M | закрыта | — | — | `855d4e5c` |

Открытое перенесено 01.11.2026 → driver-hosts/1, driver-hosts/2, execution-report/2, onboarding-forge/2.

Статусы пачки: `ожидает` → `в работе` → `сдано` → `принято` → `закрыта`. Размер — по узлам: S ≤ 4 узлов,
M 5–9, L 10–15 (больше — две пачки). Взятая пачка заморожена: её файл правит только взявший, новое
по теме — файлом в `findings/`.

## Бриф пачки 1

Начать с SS1-1 (HTTP и авторизация) и SS1-2 (свежесть тикета) — оба без стенда; SS1-4 и SS1-5 — сверки, их результат
сужает SS1-3. Стенд нужен для SS1-3 (идентичность сборки). Ждёт слова владельца: SS1-5 (какое описание входа главное,
после свежего прогона). Подробно — `batch-1-stand-identity.md`, раздел «Бриф».

## Дороги

Читать по порядку: эта карточка → `batch-1-stand-identity.md` → находки узла (колонка «id / файл» ниже) → строки
`plans/BACKLOG.md` 198, 199, 219, 234, 241, 244, 294, 348, 373, 409, 410, 413, 468 → код зоны по функциям из «Слов» →
`docs/factory-map/qa-factory-paths.md` (S0, S1, стенд).
Слова: `plans/features.json` F01, F02, F03, F18 (поле `words`) и сверх них: `User-Agent`, `HTTP 403`, `auth_gate`,
`ticket_unchecked`, `check_is_due`, `freshness`, `JiraClient`, `env:`, `source_freshness`, `runtime_probe`,
`stand_identity`, `environment.access`, `manual_capture`, `external_writes`, `http-answers.json`, `A26`,
`BUILTIN_TICKET_ADAPTERS`, `COMMAND_ADAPTERS`, `stand_health`; «стенд», «идентичность сборки», «свежесть тикета»,
«источник».
Не читать: зоны `live-runs` (замер Антона по UA — там), `package-ci` (формы тикета и доставки — его находки), `cost_capture.py`.

## Содержание

Снимок 13.10.2026; пути — от `ai-packages/qa-factory/scripts/`; суть строк — из `plans/BACKLOG.md`, находок — из дайджеста t-713. При расхождении авторитетны файлы пачек.

| id / файл | вид | суть (≤ 20 слов) | пути | статус | слово владельца | связи |
|---|---|---|---|---|---|---|
| **HTTP и авторизация (пачка 1, SS1-1)** | | | | | | |
| B-450 | строка | остатки исходящего HTTP: чужой 404 на чтении тикета, исходы «запрещено», четыре копии правила безопасного URL | `http_client.py`, `source_inventory.py`, `stand_health.py` | пачка 1, SS1-1 | нет | `live-runs` (замер UA) |
| B-246 | строка | протухший токен VCS/MR неотличим от «MR не найден»; сделать как для Jira (выход 5) | `source_inventory.py` | пачка 1, SS1-1 | нет | — |
| B-247 | строка | мелочи REST: проба «логин жив» живёт в процессе, `py_stdout` без таймаута, рукописные близнецы правил | `source_inventory.py`, `source_exclusions.py` | пачка 1, SS1-1; пункт (в) отмечен закрытым — проверить по коду | нет | — |
| **Свежесть тикета и Jira-клиент (пачка 1, SS1-2)** | | | | | | |
| B-389 | строка | `ticket_adapter.py freshness` превращает любое исключение в код 3; при `--json` не печатает объект ошибки | `ticket_adapter.py` | пачка 1, SS1-2 | нет | — |
| B-390 | строка | в CHANGELOG `## Unreleased` не названо событие журнала `ticket_unchecked` | — | пачка 1, SS1-2 (фрагмент `changelog.d/` — проверить по коду) | нет | — |
| B-393 | строка | `check_is_due` вызывается только тестами; правило свежести записано дважды: в коде и в `s0.md` | `ticket_adapter.py` | пачка 1, SS1-2 | нет | `driver-controller` (свежесть тикета) |
| B-324 | строка | `env:`-префикс секрета снимает доктор (`readiness.check_jira_direct`), а `JiraClient` — нет | `readiness.py` | пачка 1, SS1-2 | нет | — |
| **Идентичность стенда (пачка 1, SS1-3)** | | | | | | |
| B-276 / `findings/B-276-stend-identichnost-n1a-t-336-dolgi-i.md` | строка + находка-остаток | долги стенд-идентичности N1a, подпункты (а)–(у); описание — в находке | `stand_identity.py`, `guard_pre_tool.py`, `execution_request.py`, `gate_preflight.py` | пачка 1, SS1-3 | нет | — |
| B-290 | строка | гейт `source_freshness` берёт ответ из голого слова рантайма: ходить лестницей `runtime_probe` или уйти | `source_preflight.py`, `runtime_probe.py` | пачка 1, SS1-3 | нет | — |
| B-291 | строка | сканер A26: слепые пятна и читатели вне карты | `audit_factory.py` | пачка 1, SS1-3 | нет | — |
| B-350 | строка | карточка и причина устаревшей строки стенда не говорят, что строка устарела | `stand_gaps.py` | пачка 1, SS1-3 | нет | `gates-and-words` |
| **Сверки (пачка 1, SS1-4 и SS1-5)** | | | | | | |
| B-120 | строка | сверка «текст тикета называет комментарии, а снимок пуст»; в 0.8.1 `ticket_problems` и `check_ticket` не перенесены | проверить по коду | пачка 1, SS1-4: перечитать, родитель переоткрыт 06.10 | нет | — |
| B-254 | строка | два описания «как стенд логинится»: `environment.access` и рецепт `manual_capture` | `manual_capture.py` | пачка 1, SS1-5 | ждёт: после свежего прогона | — |
| **Идентичность стенда и его здоровье (кандидаты пачки 2)** | | | | | | |
| `findings/B-257-versiya-sborki-na-stende-ne-bloker.md` | находка | версия сборки на стенде — не блокер, а вопрос; реестр способов на стенд (5 частей, п. 5 сделан 02.10) | `runtime_probe.py`, `execution_request.py` | направление дано 02.10 | дано 02.10 | — |
| `findings/B-163-stend-konteyner-ui-delit-set-s.md` | находка | контейнер UI делит сеть с бэкендом; `stand_health` должен отличать мёртвый прокси и называть лекарство | `stand_health.py` | пачка 1, SS1-7 (с 26.10) | нет | находка 26.10 (обратный случай, строка ниже) |
| `findings/20261026-stend-zhiv-po-kontejneru-mertv-po-api.md` | находка | контейнер бэкенда «Up», 8080 мёртв, UI отдаёт 502; `stand_health` должен пробовать API через фронтенд и называть мёртвую часть | `stand_health.py`, `env_probe.py` | пачка 1, SS1-7 | дано 26.10 (записать) | B-163 (обратный случай) |
| `findings/B-275-nakhodki-perepisi-t-341-t-304-n0-dlya.md` | находка | находки переписи для N2: токенизированный payload, replay `initialize`, абсолютные пути, слепые зоны детекторов | `telemetry_hook.py`, `case_versions.py`, `controller.py` | открыто | нет | — |
| **Источники и снимок (кандидаты пачки 2)** | | | | | | |
| `findings/B-129-s1-govorit-kakim-marshrutom-prochitan-kazhdyy.md` | находка | S1 должен говорить, каким маршрутом прочитан каждый источник и когда 403 сменился на доступ | — | открыто | нет | — |
| `findings/B-232-fabrika-uznaet-sobstvennyy-prezhniy-vykhod-sredi.md` | находка | фабрика узнаёт свой Draft MR среди источников тикета; нужна разведка маркера | — | открыто | нет | — |
| `findings/B-239-vtoroy-progon-toy-zhe-stori-ne.md` | находка | второй прогон той же стори не дублирует работу; метка «в работе» в Jira — только по конфигу и по слову владельца | `external_writes.py` | ждёт слова владельца | да | — |
| `findings/B-240-politika-vlozheniy-i-kartinok-dannye.md` | находка | политика вложений и картинок — данные, не «всё подряд» | `source_inventory.py` | решение D-06 от 01.10 дано | дано 01.10 | — |
| `findings/B-435-b-405-b-406-formy-tiketa-i-dostavki-v.md` | находка | остатки форм тикета и доставки в данных: адаптеры, `reference-kinds.json`, `hooks.json` | `ticket_adapter.py`, `readiness.py`, `source_exclusions.py`, `hooklib.py` | открыто | нет | `package-ci` (формы), `onboarding-hooks` |
| **Запись в Jira (кандидат пачки 2)** | | | | | | |
| `findings/B-241-razmetka-pri-zapisi-v-jira.md` | находка | разметка при записи в Jira — wiki, а не markdown | `external_writes.py` | открыто | нет | — |
| `findings/20261021-ishodyashchij-tekst-bez-lokalnykh-id-i-putej.md` | находка | исходящий текст внешней записи (Jira, КБ) без локальных id и путей: payload и вложения ≤ 1 MiB проверяются до записи; сначала сверить с аудитом A20 | `external_writes.py`, `audit_factory.py` | SS1-6, ожидает | нет | обзор testing-factory (RELATED_WORK §2 п. 7) |

| **Находки 27.10.2026** | | | | | | |
| `findings/20261027-doctor-proved-na-neudachnom-kode.md` | находка | доктор печатает «вход доказан» по записи `login_probe` с неудачным кодом (HTTP 422) | `stand_health.py` | пачка 1, SS1-8 | нет | t-1365 Q1 |
| `findings/20261028-env-probe-liveness-bez-cepochki-frontenda.md` | находка | `env_probe.liveness` спрашивает только адрес API: при сломанном прокси фронтенда доктор «alive», `stand_health` «down» | `env_probe.py`, `stand_health.py` | пачка 1, SS1-9 | нет | RH1-7 |
| **Отзыв пользователя, 28.10.2026** | | | | | | |
| `findings/20261028-klyuch-chuzhogo-proekta-v-zagolovke-i-roditel.md` | находка | ключ чужого проекта в заголовке (`TP6-n`) читается как тикет и даёт 404; родитель берётся, хотя стори не о нём | `ticket_light.py`, `source_inventory.py`, `agents/qa-scout.md` | пачка 1, SS1-10 | «не в 0.10.5, в пачки» (28.10.2026); правило ключей — решение нужно | отзыв Dev6 (TP2-2702), t-1553; SS1-1 |
| **Находки ночного прогона 14857 (0.10.6), 30.10.2026** | | | | | | |
| `findings/20261030-nauchennoe-o-stende-ne-sohranyaetsya-na-sleduyushchij-progon.md` | находка | выученное человеком о стенде (`files_filter`, `timeout(900)`) не сохраняется в конфиг проекта для следующего прогона | `scripts/gate_preflight.py`, `references/config-keys.json` | пачка 1, SS1-11 | нет | t-1597 sink 2; RH2-9; t-1605 #16 |
| `findings/20261030-fingerprint-kanala-chitaet-channels-bez-proverki-tipa.md` | находка | `tracker_write.fingerprint` и соседи читают `external_writes.channels` без проверки типа | `scripts/tracker_write.py` | пачка 1, SS1-12 | нет | S1b round 2 |
| **Находки 31.10.2026 (прогон CART-1, MyBooks)** | | | | | | |
| `findings/20261031-istoriya-bez-klyucha-trekera-vydumannyj-klyuch-i-povtor-s0-s4.md` | находка | история без ключа трекера: дирижёр выдумал ключ не той формы, S0–S4 выброшены и пройдены заново (≈ 38 мин, 4 роли) | `ticket_adapter.py`, `adapter_forms.py`, `case_versions.py`, `s0.md` | пачка 1, SS1-14 | нет | свод CART-1 2.1; 2.3 — известно: `onboarding-hooks/findings/20261031-istochniki-trebovanij-bez-proizvoditelya-i-chitatelya.md` (OH3-39); SS1-10 |
| `findings/20261031-testirovanie-sushchestvuyushchej-funkcii-bez-mr-vhod-v-halt.md` | находка | проверка существующей функции без MR не имеет пути по умолчанию: S1 встаёт в `halt`, вопрос после диспатча | `story_run.py`, `qa-scout.md`, `s1.md` | пачка 1, SS1-13 | нет | свод CART-1 2.5; `grounding/findings/20261031-trebovanie-iz-tekushchego-koda-stanovitsya-orakulom.md` |
| **Обзор MR !12, 01.11.2026** | | | | | | |
| `findings/20261101-klyuch-bagov-i-istochnikov-v-contract-i-branch-accounting-tolko-jira.md` | находка, id — | форма ключа `bug:`/`rest:` держится вне `adapter_forms` и знает только Jira: `bug:#42` и `rest:#42` отказываются на github/gitlab/ado | `scripts/contract.py`, `scripts/branch_accounting.py`, `scripts/validate_artifacts.py`, `references/adapter-forms.json` | пачка 1, SS1-16 | нет (слово 31.10.2026 «трекер — не Jira» дано) | t-1646 F-1; SS1-14; SS1-15 |

## Входящие

`findings/` этой кучки; находку, не названную ни в одной пачке, называет `piles.py check` (е).

## Вопросы владельцу

- B-239: ставить ли метку «в работе» в Jira, чтобы второй прогон той же стори не дублировал работу (только по конфигу `external_writes` и после вашего слова)? Находка `findings/B-239-vtoroy-progon-toy-zhe-stori-ne.md`.
- B-254: после свежего прогона — какое из двух описаний «как стенд логинится» остаётся главным: `environment.access` или рецепт ручного захвата?
