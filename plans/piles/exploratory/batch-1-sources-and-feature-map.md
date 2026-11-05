# Исследовательское тестирование — пачка 1: требования из всех источников, карта функции по всем репозиториям, матрица покрытия

кучка: `exploratory` | статус: закрыта | взял: — | ветка: — | MR: `855d4e5c` | стенд: нужен (только живое доказательство, MyBooks) | приоритет: П2 | issue: https://git.example.com/dev1/yml-text-factory/-/work_items/42

Правило готовности: пачка закрыта, когда каждый узел «принято», свидетели узлов — в журнале взявшего,
живые доказательства (FR-33) сделаны или переданы строкой в кучку «живые прогоны».

Решения владельца: слово владельца 31.10.2026 — открыть кучку с пачкой 1 («да»); требования — из всех источников онбординга,
не только Jira; карта функции — не на онбординге целиком (10 больших репозиториев); любой проект, не только браузер.
Порядок по общим файлам: `references/config-keys.json`, `skills/qa-onboarding/phases/p1-discovery.md`: onboarding-hooks OH3-35 → OH3-39 → XT1-1.
Скоуп свидетеля: тестовый файл изменённого модуля и ключи DoD узла (D-0056); полный канон — интегратор при слиянии.
Спека пачки: `docs/tasks/specs/t-1630-xt1-exploratory-batch-1.md` (дизайнер t-1630, принята Lead 31.10.2026; развилки F1–F13 — по рекомендации). Общий бриф дизайнерам: `plans/exploratory-charters-proposal.md` (шаги E0–E3, «Уточнения владельца 31.10.2026»); эталон —
`experiments/mybooks/add-to-cart-cases.md`; стенд — `docs/RUNBOOK.md` §11. Каждый узел дизайнер доводит до «Что именно менять»:
файл, функция, поле, ожидаемое поведение и тест на каждый пункт (PROJECT.md «Командная работа», п. 11).

## Бриф

Пачка даёт шаги E0–E3 предложения: из слов «проверь всё, что связано с X» фабрика находит требования во всех источниках
онбординга, код функции во всех репозиториях и сверяет одно с другим и с уже написанными кейсами и тестами. Волны (спека §1): XT1-1 → (XT1-2, XT1-3, XT1-5) → (XT1-4, XT1-6) → XT1-7 → XT1-8.
Грубая карта продукта на онбординге ушла в пачку 2 (XT2-1, F13): она ждёт OH3-39, а тот — слова владельца по OH3-35. Критик — один на тему при
интеграции (R13-g); критик на план — у каждого кодового узла (новая форма данных и новый скилл).

## Узлы

Исполнитель «designer → builder → critic» — кодовый узел; «builder» — узел-документ. Статусы:
`ожидает` → `в работе` → `сдано` → `принято` / `отклонено`.

| Узел | Приоритет | Что | Исполнитель | Пишет в | Зависит от | Статус |
|---|---|---|---|---|---|---|
| XT1-1 | П2 | Ядро исследования: slug из фразы, корень `qa-factory/explorations/<slug>/`, состояние шагов E0–E3, рамка E0 с пробами источников и репозиториев и ОДНИМ пакетом вопросов, `next_step`/`brief`, реестр данных `references/exploration.json` с лимитами (Спека t-1630 §2 XT1-1, п. 1–10) | designer → critic на план → builder → critic | `scripts/exploration.py`, `scripts/tests/test_exploration.py`, `references/exploration.json`, `references/question-prices.json`, `references/install-paths.json`, `scripts/audit_factory.py` | — | закрыта: перенесено 01.11.2026 → release-next/1 |
| XT1-2 | П2 | Личность исследования в гардах: метка `Exploration: <slug>` и `QA_FACTORY_TASK=explore:<slug>` читаются раньше стори; иначе `stage_guard.py:1093-1097` отказывает диспатчу при любой стори в проекте, `:403-407` отдаёт его единственной стори, `exit_gate.py:219-221` судит скаута по чужой S1; отчёт — свип остальных нестори-диспатчей (Спека t-1630 §2 XT1-2; F1, F6) | designer → critic на план → builder → critic | `scripts/stage_guard.py`, `scripts/host_dispatch.py`, `scripts/exit_gate.py`, `scripts/refusal_registry.py`, `scripts/tests/test_exploration_identity.py` | XT1-1 | закрыта: перенесено 01.11.2026 → release-next/1 |
| XT1-3 | П2 | Требования из трекера: `JiraClient.search_issues` (JQL, только чтение, пагинация, лимит), таблица видов источников `references/requirement-source-kinds.json` (F8), найденное читается существующим чтением по ключу (Спека t-1630 §2 XT1-3) | designer → critic на план → builder → critic | `scripts/source_inventory.py` (`+JiraClient.search_issues`), `scripts/requirement_search.py`, `references/requirement-source-kinds.json`, `scripts/exploration.py` (`frame`), `scripts/audit_factory.py`, `scripts/tests/test_requirement_search.py` | XT1-1; OH3-39 по `source_inventory.py` — непересекающиеся функции (D-0048) | закрыта: перенесено 01.11.2026 → release-next/1 |
| XT1-4 | П2 | Требования из Confluence (CQL) и из документов в git (вид `repository` — отбор попаданий XT1-5 по `locator`) (Спека t-1630 §2 XT1-4) | designer → builder → critic | `scripts/requirement_search.py`, `scripts/tests/test_requirement_search_wiki.py` | XT1-3, XT1-5 | закрыта: перенесено 01.11.2026 → execution-report/1 |
| XT1-5 | П2 | Код ищет слова функции по всем репозиториям через `git grep` (F5) поверх `project_inventory.build_inventory` и `test_files.file_kind`; репозиторий без попаданий — строка «не затронут»; кэш по ревизии в `state/features/<slug>/` (Спека t-1630 §2 XT1-5) | designer → critic на план → builder → critic | `scripts/feature_hits.py`, `scripts/tests/test_feature_hits.py`, `scripts/audit_factory.py` | XT1-1 | закрыта: перенесено 01.11.2026 → release-next/1 |
| XT1-6 | П2 | Форма карты функции и её проверка; режимы скаута E1 (требования R-n, F10) и E2 (читать только попадания) в `references/explore-modes.md`, в агенте одна строка (Спека t-1630 §2 XT1-6; F4, F12) | designer → critic на план → builder → critic | `scripts/feature_map.py`, `references/explore-modes.md`, `agents/qa-scout.md`, `references/role-commands.json`, `scripts/audit_factory.py`, `scripts/tests/test_feature_map.py` | XT1-1, XT1-5 | закрыта: перенесено 01.11.2026 → release-next/1 |
| XT1-7 | П2 | Матрица покрытия и режим `qa-requirements-tester` E3: путь или правило × {кейс, автотест, юнит, ничего}; расхождение — вопрос человеку одним пакетом, ответы в пачке 1 не пишутся (P20, F9) (Спека t-1630 §2 XT1-7) | designer → critic на план → builder → critic | `references/explore-modes.md`, `agents/qa-requirements-tester.md`, `references/role-commands.json`, `references/question-prices.json`, `scripts/tests/test_coverage_matrix.py` | XT1-6 | закрыта: перенесено 01.11.2026 → release-next/1 |
| XT1-8 | П2 | Скилл `qa-explore` (E0–E3), `explore_step.py` (сессия ведёт, код печатает следующий шаг, F2) и регистрация по списку §4 спеки (~22 файла; `README.md` и `plugin.json` ×4 — интегратору) (Спека t-1630 §2 XT1-8) | designer → critic на план → builder → critic | `skills/qa-explore/SKILL.md`, `skills/qa-explore/README.md`, `skills/qa-explore/evals/evals.json`, `scripts/explore_step.py`, `scripts/activity_capture.py`, `scripts/factory_dashboard.py`, `scripts/role_permissions.py`, `scripts/audit_factory.py`, `scripts/tests/test_explore_skill.py`, `scripts/tests/test_collect_skill.py` | XT1-2, XT1-3, XT1-5, XT1-6, XT1-7 | закрыта: перенесено 01.11.2026 → release-next/1 |

## Ход

Журнал передачи Lead пачки, новые записи в конец: `<дата время> — <что сделано, диспатчи t-nnn, хэши>`.

- 31.10.2026 — пачка открыта Lead (Opus, деградированное окно) по слову владельца «да»; предложение `plans/exploratory-charters-proposal.md`; разведка t-1629.
- 31.10.2026 01:2x — спека пачки t-1630 принята: 8 узлов, 8 цепочек; XT1-9 → пачка 2 (XT2-1).
- 01.11 — закрыта по слову владельца 01.11.2026 (пересборка бэклога): открытые узлы → release-next/1, execution-report/1

## Живые доказательства

| Что | Стенд / проект | Кто | Статус |
|---|---|---|---|
| `qa-explore "Add to Cart"` находит не меньше эталона `experiments/mybooks/add-to-cart-cases.md`: 4 расхождения (164, 166, 160, 161), точки входа «карточка каталога» и «вишлист», слияние гостевой корзины, удаление книги и последний экземпляр | MyBooks (RUNBOOK §11) | взявший пачку | перенос: live-runs/2 «Живые доказательства» \| обоснование: пересборка бэклога \| подтвердил: владелец, 01.11.2026 (слово 2 пересборки) |

## Остатки
