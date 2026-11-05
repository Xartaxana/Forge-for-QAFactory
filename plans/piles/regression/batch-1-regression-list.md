# Починка регрессии — пачка 1: список регрессии верный с первого прогона

кучка: `regression` | статус: закрыта | взял: — | ветка: — | MR: `855d4e5c` | стенд: не нужен (код); живое доказательство — прогон стори | приоритет: П1 | issue: https://git.example.com/dev1/yml-text-factory/-/work_items/51

Правило готовности: пачка закрыта, когда каждый узел «принято», свидетели узлов — в журнале взявшего, живое доказательство (FR-33)
сделано: в отчёте прогона стори блок `facts:regression` соответствует P24.

Решения владельца: P24 (`PROJECT.md`, слово владельца 30.10.2026: регрессию фабрика находит и отдаёт, не гоняет; список не урезается
стендом, у пунктов — требования к стенду; один прогон на стори — список верен с первого раза); слово 30.10.2026: «создавай кучку починки регрессии».
Порядок по общим файлам: `delivery_verdict.py`, `agents/qa-test-strategist.md`: RG1-2 → RG1-1 → RG1-3 → RG1-4 → RG1-5.
Скоуп свидетеля: тестовые файлы изменённых модулей (`test_report_facts.py`, `test_third_verdict.py`, `test_test_repo_base.py`) и ключи DoD узла;
полный канон — интегратор при слиянии.
Общий бриф дизайнерам: карточка («Дороги», «Содержание»); находка узла; `PROJECT.md` P24; фикстура
`scripts/tests/fixtures/investigation-14857/TP1-14857/test-plan.md`; вернуть спеку в `docs/tasks/specs/t-nnn-rg1-n.md` с развилками
наверх. Направление ошибки: пропустить файл допустимо, назвать регрессией тест, которого нет на главной ветке, — нет. Фабрика регрессию
не гоняет; список не режется под наш стенд; «нестабильность между прогонами» дефектом не считается (P24).

## Бриф

Что сделать: список регрессии (`## Recommended regression` плана и блок `facts:regression` отчёта) содержит только существующие тесты на
главной ветке, реальные пути, одну команду без повторов, требования к стенду у каждого пункта, у части разработчиков — пути или строку «теста нет».
НЕ делать: запуск регрессии фабрикой; урезание списка по возможностям нашего стенда; меры «стабильности между прогонами»; путь машины в
командах и маркер приложения (это HF8-17 в `hotfix-12586/8`).
Первые 10 минут: (1) прочитать «Бриф пачки 1» карточки, `PROJECT.md` P24, находки узлов; (2) открыть `plans/PILES.md`, найти активные пачки с теми
же файлами (`report_facts.py`, `check_delivery.py` — `hotfix-12586/9`, `report-delivery`); (3) интегратор берёт пачку
`python tools/piles.py take regression 1 --who <кто>`; (4) первая строка «Хода»; первый диспатч — дизайнер RG1-2 (самая большая потеря).

## Узлы

Исполнитель «designer → builder → critic» — кодовый узел; «builder» — узел-документ. Статусы:
`ожидает` → `в работе` → `сдано` → `принято` / `отклонено`.

| Узел | Приоритет | Что | Исполнитель | Пишет в | Зависит от | Статус |
|---|---|---|---|---|---|---|
| RG1-1 | П1 | **0.10.8 (слово владельца 31.10.2026, docs/tasks/release-0.10.8.md).** Одна команда без повторов: файлы дедуплицированы, файл под перечисленным каталогом убран, подписи `blast:B-n` сохраняются (`findings/20261030-regressiya-dublirovanie-zapuskov-v-odnoy-komande.md`; P24). DoD: на списке 12586 `test_integration_update.py` один раз, `test_edit_integration.py` один раз, файлы под `tests/integrations` и `tests/projects` убраны. Свидетель — 12586 `test-report.md:72-78` | designer → builder → critic | `ai-packages/qa-factory/scripts/delivery_verdict.py`, `ai-packages/qa-factory/scripts/report_facts.py`, `ai-packages/qa-factory/agents/qa-test-strategist.md` | RG1-2 | принято, слито (релиз 0.10.8) |
| RG1-2 | П1 | **0.10.8 (слово владельца 31.10.2026, docs/tasks/release-0.10.8.md).** Регрессия без тестов этой стори и с существующими: код по снимку базы (`state/test-repo-base.json`) выделяет файлы, новые в прогоне, в список «тесты этой стори»; роль S3 ищет существующие тесты по тому, что трогает дифф (page object, утилиты, эндпойнты), и называет их путями (`findings/20261030-regressiya-soderzhit-testy-etogo-zhe-progona-i-propuskaet-sushchestvuyushchie.md`; P24, P17). DoD: на 14857 `test_code_datasource_reindex_last_indexed.py` не в регрессии, `test_git_faq_datasource_reindex.py` и соседние `tests/assistant/datasource/` названы. Свидетель — 14857 `test-report.md:61` | designer → critic на план → builder → critic | `ai-packages/qa-factory/scripts/test_repo_base.py`, `ai-packages/qa-factory/scripts/delivery_verdict.py`, `ai-packages/qa-factory/agents/qa-test-strategist.md`, `ai-packages/qa-factory/references/artifact-contract-plan.md` | — | принято, слито (релиз 0.10.8) |
| RG1-3 | П1 | **0.10.8 (слово владельца 31.10.2026, docs/tasks/release-0.10.8.md).** Тестовый файл, уже лежащий на главной ветке проекта, S1/S3 относят к существующему покрытию, а не к изменению; такие тесты годятся в регрессию (`findings/20261030-smerzhennyy-test-only-mr-chitaetsya-kak-chast-izmeneniya.md`; t-1606 урок 1; P24). DoD: MR 798 (влит в main) не попадает в «изменение»; его тест в регрессии как существующий. Сверка базы с mainline до S3 — не здесь | designer → critic на план → builder → critic | `ai-packages/qa-factory/scripts/brief_pack.py`, `ai-packages/qa-factory/scripts/test_repo_base.py`, `ai-packages/qa-factory/agents/qa-test-strategist.md` | RG1-2 | принято, слито (релиз 0.10.8) |
| RG1-4 | П1 | **0.10.8 (слово владельца 31.10.2026, docs/tasks/release-0.10.8.md).** У каждого пункта регрессии записаны требования к стенду; пункт остаётся в списке (`findings/20261030-punkty-regressii-bez-trebovaniy-k-stendu.md`; P24). DoD: `test_scheduler_service.py` несёт «нужен планировщик, запускающий cron источников данных»; пункт без требований — явная строка «требований нет», не молчание. Свидетель — 14857 `test-report.md:63` | designer → builder → critic | `ai-packages/qa-factory/references/artifact-contract-plan.md`, `ai-packages/qa-factory/references/templates/test-report.md`, `ai-packages/qa-factory/scripts/delivery_verdict.py`, `ai-packages/qa-factory/agents/qa-test-strategist.md` | RG1-3 | принято, слито (релиз 0.10.8) |
| RG1-5 | П2 | Часть разработчиков: каждый пункт — реальный путь существующего теста или явная строка «теста нет» к разработчикам, не пункт регрессии (`findings/20261030-chast-razrabotchikov-v-regressii-bez-putey.md`; P24). DoD: на формулировках 12586 (28.10, 29.10) и 14857 (ручной) пункт без пути отклоняется или превращается в строку «теста нет» | designer → builder → critic | `ai-packages/qa-factory/scripts/report_facts.py`, `ai-packages/qa-factory/scripts/delivery_verdict.py`, `ai-packages/qa-factory/agents/qa-test-strategist.md` | RG1-4 | закрыта: перенесено 01.11.2026 → execution-report/1 |
| RG1-6 | П1 | Указатель, не работа: путь машины в командах регрессии (HF8-17 п. 5) и маркер приложения кейсов внутри блока `facts:regression` ведёт `hotfix-12586/8`, HF8-17. перенос: hotfix-12586/8, HF8-17 \| обоснование: те же строки кода, уже заведены там (`hotfix-12586/findings/20261029-otchyot-ne-zaschityvaet-ruchnye-proverki-trebovaniyu.md`) \| подтвердил: Lead пачки, 30.10.2026 | Lead | нет | — | принято: 2913763a |

## Ход

Журнал передачи Lead пачки, новые записи в конец: `<дата время> — <что сделано, диспатчи t-nnn, хэши>`.

- 30.10 — пачка открыта по слову владельца 30.10.2026 («создавай кучку починки регрессии»); карточка, пять находок, t-1608.
- 31.10 — релиз 0.10.8: узлы RG1-1, RG1-2, RG1-3, RG1-4 отнесены в релиз по слову владельца 31.10.2026 (состав — docs/tasks/release-0.10.8.md); t-1642.
- 01.11 — релизы 0.10.7 и 0.10.8 слиты в одну ветку (`claude/releases-7-8-merge-b1f668`, голова `e67df7dd`): статусы строк проставлены — релиз 0.10.8: RG1-1, RG1-2, RG1-3, RG1-4.
- 01.11 — закрыта по слову владельца 01.11.2026 (пересборка бэклога): открытые узлы → execution-report/1

## Живые доказательства

| Что | Стенд / проект | Кто | Статус |
|---|---|---|---|
| Прогон стори с регрессией в плане: блок `facts:regression` без повторов, без тестов этой же стори, с путями и требованиями к стенду | копия проекта, без следов (P8) | — | перенос: live-runs/2 «Живые доказательства» \| обоснование: пересборка бэклога \| подтвердил: владелец, 01.11.2026 (слово 2 пересборки) |

## Остатки

<!--
Пачка закрывается доделкой, не переносом (слово владельца 08.10.2026): `close` отказывает, пока в этом разделе есть
пункт, у которого нет одной из двух форм (ключи в любом регистре, значения как написано, пары `ключ: значение` через ` | `, текст впереди):
  - <что осталось> | сделано: <хэш 7-40 hex | t-nnn>
  - <что осталось> | перенос: <findings/<файл> | пачка N | <кучка>/findings/<файл>> | обоснование: <почему> | подтвердил: <кто, дата>
Пустой раздел — можно закрывать.
-->
