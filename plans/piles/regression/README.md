# Починка регрессии (`regression`)

приоритет: П1 (владелец, 30.10.2026) | фичи: F13, F08 | стенд: не нужен (код); живое доказательство — прогон стори | зона: `ai-packages/qa-factory/scripts/delivery_verdict.py`, `ai-packages/qa-factory/scripts/check_delivery.py`, `ai-packages/qa-factory/scripts/report_facts.py`, `ai-packages/qa-factory/scripts/test_repo_base.py`, `ai-packages/qa-factory/scripts/brief_pack.py`, `ai-packages/qa-factory/agents/qa-test-strategist.md`, `ai-packages/qa-factory/references/artifact-contract-plan.md`, `ai-packages/qa-factory/references/templates/test-report.md`

## Зачем

Человек получает один верный список регрессии с первого и единственного прогона своей стори. В нём только существующие тесты (не
написанные фабрикой в этом же прогоне), настоящие пути, одна команда без повторов, у каждого пункта названо, что нужно от стенда, а
часть разработчиков — это пути или честная строка «теста нет». Фабрика регрессию не гоняет, а находит и отдаёт (P24).

## Что не так сегодня (факты)

- Один файл стоит в нескольких командах, каталог запущен рядом с его же файлами (12586, 29.10): `.../TP1-12586/test-report.md:72-78`.
- В регрессии лежит тест, написанный в этом же прогоне, а существующий пропущен (14857, ночной): `.../TP1-14857/test-report.md:61`, `test-plan.md:45`.
- Влитый MR только с тестами читается как часть изменения, а не как существующее покрытие: `docs/tasks/specs/reviews/t-1606-14857-tests-vs-mr798.md`, урок 1.
- У пункта нет требований к стенду (`tests/scheduler/test_scheduler_service.py` без указания на планировщик): `.../TP1-14857/test-report.md:63`.
- Часть разработчиков названа словами без путей: `.../TP1-12586/test-report.md:80`.
- Путь машины в командах и маркер приложения кейсов внутри блока регрессии уже заведены в `hotfix-12586/8`, HF8-17 (здесь — указатель, не копия).
- Производители: `delivery_verdict.regression_lines`, `report_facts._regression`, `check_delivery.regression_record`, роль `qa-test-strategist` п. 6 (поиск `Recommended regression`, `facts:regression` по `ai-packages/qa-factory`).

## Пачки

| № | Что изменится для пользователя | Строки | Размер | Статус | Взял | Ветка | MR |
|---|---|---|---|---|---|---|---|
| 1 | список регрессии верный с первого прогона: без повторов, без тестов этой же стори, с путями и требованиями к стенду | — | S | закрыта | — | — | `855d4e5c` |

Открытое перенесено 01.11.2026 → execution-report/1.

Статусы пачки: `ожидает` → `в работе` → `сдано` → `принято` → `закрыта`. Размер — по узлам: S ≤ 4 узлов,
M 5–9, L 10–15 (больше — две пачки). Взятая пачка заморожена: её файл правит только взявший, новое
по теме — файлом в `findings/`.

## Бриф пачки 1

Начать с RG1-2 (факт 2: самая большая потеря — регрессия называет тест этой же стори и не видит существующих); RG1-1 и RG1-3…RG1-5
пишут те же роль и `delivery_verdict.py`, порядок задан в файле пачки. Стенд для кода не нужен. Живое доказательство (FR-33) —
прогон стори и чтение блока `facts:regression` в её отчёте. Принцип — `PROJECT.md` P24. Подробно — `batch-1-regression-list.md`, раздел «Бриф».

## Дороги

Читать по порядку: эта карточка → `batch-1-regression-list.md` → находки узла (колонка «id / файл» ниже) → `PROJECT.md` P24, P17, P20 →
`docs/tasks/specs/reviews/t-1606-14857-tests-vs-mr798.md` (урок 1), `t-1605-14857-night-vs-manual.md` → код зоны по функциям из «Слов».
Слова: `plans/features.json` F13, F08 (поле `words`) и сверх них: `Recommended regression`, `facts:regression`, `regression_lines`,
`_regression`, `_r_regression`, `regression_record`, `run_suite.py`, `test-repo-base.json`, `measure_git`, `blast`, `Developer-owned`,
`Left with you`; «регрессия», «существующие тесты», «требования к стенду».
Не читать: `hotfix-12586` кроме HF8-17 (путь машины и маркер приложения — там), `report-delivery` (триаж, вердикты).

## Содержание

Снимок 30.10.2026; пути — от `ai-packages/qa-factory/`; суть находок — из их файлов. При расхождении авторитетны файлы пачек.

| id / файл | вид | суть (≤ 20 слов) | пути | статус | слово владельца | связи |
|---|---|---|---|---|---|---|
| **Пачка 1** | | | | | | |
| `findings/20261030-regressiya-dublirovanie-zapuskov-v-odnoy-komande.md` | находка | файл в трёх командах, каталог рядом с его файлами; нужна одна команда без повторов | `scripts/delivery_verdict.py`, `scripts/report_facts.py` | пачка 1, RG1-1 | нет | P24 |
| `findings/20261030-regressiya-soderzhit-testy-etogo-zhe-progona-i-propuskaet-sushchestvuyushchie.md` | находка | регрессия называет тест этого же прогона и не видит существующих; нужен список «тесты этой стори» и поиск по диффу | `scripts/test_repo_base.py`, `agents/qa-test-strategist.md` | пачка 1, RG1-2 | нет | P24; P17 |
| `findings/20261030-smerzhennyy-test-only-mr-chitaetsya-kak-chast-izmeneniya.md` | находка | влитый MR с тестами читается как изменение, не как существующее покрытие | `scripts/brief_pack.py`, `agents/qa-test-strategist.md` | пачка 1, RG1-3 | нет | t-1606 урок 1 |
| `findings/20261030-punkty-regressii-bez-trebovaniy-k-stendu.md` | находка | у пункта не названы требования к стенду (планировщик cron); пункт остаётся в списке | `references/artifact-contract-plan.md`, `references/templates/test-report.md` | пачка 1, RG1-4 | нет | P24 |
| `findings/20261030-chast-razrabotchikov-v-regressii-bez-putey.md` | находка | пункты за разработчиками без путей; нужен путь или строка «теста нет» | `agents/qa-test-strategist.md`, `scripts/report_facts.py` | пачка 1, RG1-5 | нет | P24 |
| **Указатель на пачку HF8-17** | | | | | | |
| `hotfix-12586/findings/20261029-otchyot-ne-zaschityvaet-ruchnye-proverki-trebovaniyu.md` | указатель | путь машины в командах (п. 5) и маркер приложения внутри блока (HF8-17); не копия | `scripts/report_facts.py` | пачка 1, RG1-6: перенос в HF8-17 | нет | `hotfix-12586` HF8-17 |

## Входящие

`findings/` этой кучки; находку, не названную ни в одной пачке, называет `piles.py check` (е).
Каждая новая находка тем же ходом получает строку в пачке этой кучки, которую ещё не взяли, или указатель `перенос: <кучка>/…`
(`piles.py check` (е)); нет такой пачки — открывается следующая со статусом «ожидает».

## Вопросы владельцу

- нет
