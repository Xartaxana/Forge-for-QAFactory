# Знания о проекте — пачка 2: условия ответа, замена и конфликт, защита оглавления, шире живое доказательство

кучка: `project-knowledge` | статус: ожидает | взял: — | ветка: — | MR: — | стенд: нужен | приоритет: П2

Правило готовности: пачка закрыта, когда каждый узел «принято», свидетели узлов — в журнале взявшего,
живые доказательства (FR-33) сделаны или переданы строкой в кучку «живые прогоны».

Решения владельца: слово владельца 11.11.2026 — пункты сверки с внешним разбором, не вошедшие в общий план t-2277, идут находкой в фазы 2, 5 и 6 плана знаний.
очередь: project-knowledge/1 → project-knowledge/2 (реестр ответов PK0-1)

## Бриф

Узлы исполняются вместе со спекой своей фазы плана `plans/project-knowledge-plan.md` (фазы 2, 5, 6), не раньше: до спеки фазы это
входящие требования к ней. Всё по теме — в находке `findings/20261111-chego-ne-hvataet-planu-znanij-po-vneshnemu-razboru.md`.

## Узлы

Статусы: `ожидает` → `в работе` → `сдано` → `принято` / `отклонено`.

| Узел | Приоритет | Что | Исполнитель | Пишет в | Зависит от | Статус |
|---|---|---|---|---|---|---|
| PK2-1 | П2 | Поле `condition` у записи ответа: условие словами человека, читает роль. `findings/20261111-chego-ne-hvataet-planu-znanij-po-vneshnemu-razboru.md`, раздел PK2-1 | designer (спека фазы 2) → builder → critic | нет (файлы называет спека фазы 2) | PK0-1, спека фазы 2 | ожидает |
| PK2-2 | П2 | Замена (`supersedes`), конфликт двух действующих ответов, одновременная запись, отмена. `findings/20261111-chego-ne-hvataet-planu-znanij-po-vneshnemu-razboru.md`, раздел PK2-2 | designer (спека фазы 2) → builder → critic | нет (файлы называет спека фазы 2) | PK0-1, спека фазы 2 | ожидает |
| PK2-3 | П2 | Оглавление знаний в защищённой части брифа. `findings/20261111-chego-ne-hvataet-planu-znanij-po-vneshnemu-razboru.md`, раздел PK2-3 | designer (спека фазы 5) → builder → critic | нет (файлы называет спека фазы 5) | спека фазы 5 | ожидает |
| PK2-4 | П2 | Четыре шага к живому доказательству фазы 6. `findings/20261111-chego-ne-hvataet-planu-znanij-po-vneshnemu-razboru.md`, раздел PK2-4 | Lead (строка в `live-runs` при спеке фазы 6) | нет | спека фазы 6 | ожидает |
| PK2-5 | П2 | Разведка: выбор документа проекта по имени файла; правка, если подтвердится. `findings/20261111-chego-ne-hvataet-planu-znanij-po-vneshnemu-razboru.md`, раздел PK2-5 | scout → builder | нет (файлы называет разведка) | — | ожидает |
| PK2-6 | П2 | Учётка `default` не должна доходить до трёх карточек: одна строка «решено один раз» для `_probe_actor`, ключей входа `check_s5_credentials` и пункта `default` кейса (`gate_preflight.py`); тест на каждый путь. `findings/20261111-default-ucherka-tri-karty-vne-invarianta.md` | designer (спека узла) → builder → critic | нет (файлы называет спека узла; находка называет `gate_preflight.py`) | PK0-4 | ожидает |
| PK2-7 | П2 | Строки цены `factory`/`you`/`story` у каждой строки `stand_gap_words` в `question-vocabulary.json`; рекомендация: со следующим проходом по текстам пакетов гейтов, владелец может хотеть сейчас. `findings/20261111-stand-gap-karty-bez-strok-ceny.md` | designer (спека прохода по текстам) → builder → critic | нет (файлы называет спека прохода по текстам) | PK0-4 | ожидает |
| PK2-8 | П3 | Два исключения пункта (f) (карточка роли; все кейсы роли отброшены `level_applied`/`decisions`) не взяты; рекомендация: не брать до живого прогона с лишним вопросом, цену взвешивает владелец. `findings/20261111-dva-isklyucheniya-punkta-f-ne-vzyaty.md` | Lead (слово владельца) → builder | нет (файлы называет спека узла, если владелец решит взять) | PK0-4, слово владельца | ожидает |
| PK2-9 | П2 | Гард `guard_pre_tool.py`: подкоманда в любом месте после имени скрипта, один общий помощник для `project_knowledge.py` и `environment_record.py record\|revoke`; тест `--task T role`. `findings/20261111-guard-globalnaya-opciya-pered-podkomandoj.md` | builder → critic | `ai-packages/qa-factory/scripts/guard_pre_tool.py` | PK0-8 | ожидает |
| PK2-10 | П3 | Указатель для спеки фазы 1: первый взгляд реестр не пишет; маршруты, тест-данные, требования к стенду — кандидаты в каталог по слову владельца (J-5). `findings/20261111-pervyj-vzglyad-ne-pishet-reestr-otvetov.md` | Lead (спека фазы 1) | нет (кодом ничего) | спека фазы 1 | ожидает |
| PK2-11 | П2 | Разведка и один общий отказ для писателей записей, которые не проверяют `no_trace`. `findings/20261111-zapis-v-sleduemyj-sled-bez-proverki-no-trace.md` | scout → builder → critic | нет (файлы называет разведка) | — | ожидает |
| PK2-12 | П3 | Одна функция старшинства «последняя запись» вместо `_latest` и `ER.covering`. `findings/20261111-latest-dublirujet-covering-semejstva-zapisej.md` | builder | `ai-packages/qa-factory/scripts/environment_record.py` | PK0-1 | ожидает |
| PK2-13 | П3 | Один помощник замка записи вместо копии в `project_knowledge`. `findings/20261111-zamok-zapisi-dublirujetsya-v-project-knowledge.md` | builder | `ai-packages/qa-factory/scripts/event_store.py` | PK0-1 | ожидает |
| PK2-14 | П2 | Читатель конфига реестра знаний через `read_config_file`, нечитаемый конфиг — не «пусто». `findings/20261111-chitatel-config-glotaet-nechitaemyj-config.md` | builder | `ai-packages/qa-factory/scripts/project_knowledge.py` | PK0-1 | принято: 7907177 (t-441) |
| PK2-15 | П3 | Спека t-2142 §3 (7): условие (c) и итог о кейсе с одним `env`-аккаунтом противоречат; выбрать одну формулировку. `findings/20261111-spec-protivorechie-akkaunt-env-v-uslovii-vhoda.md` | Lead (правка спеки) → builder | `ai-packages/qa-factory/scripts/gate_preflight.py` | PK0-5 | ожидает |
| PK2-16 | П2 | Отказ «нет выбранного стенда» получает свой вид и свою фразу для человека. `findings/20261111-bez-vybrannogo-stenda-chelovek-slyshit-chto-netu-klyuchej.md` | builder → critic | `ai-packages/qa-factory/scripts/story_run.py` | PK0-5 | ожидает |
| PK2-17 | П3 | Один помощник «аккаунт, который называет кейс» для `default_login_needed` и `_actors_of_manual_cases`. `findings/20261111-akkaunt-kejsa-v-dvuh-mestah-odin-pomoshchnik.md` | builder → critic | `ai-packages/qa-factory/scripts/gate_preflight.py` | PK0-5 | ожидает |
| PK2-18 | П2 | Запись замеченной роли: защита «писать, только если последнее состояние отсутствует или `noticed`» под замком в `record`, чтобы ответ человека не перезаписывался. `findings/20261111-zapis-zamechennoj-roli-gonka-proverki-i-zapisi.md` | builder → critic | `ai-packages/qa-factory/scripts/project_knowledge.py` | PK0-3 | ожидает |
| PK2-19 | П2 | `_refuse_no_trace` читает признак эксперимента и до записи `pipeline.json` (launch-запись `state/driver-state.json`, `launch.no_trace`); нет ни одного носителя — не писать и сказать почему (FR-59); тест-таблица случаев. `findings/20261112-s0-no-trace-komandy-dirizhera-pishut-v-reestr.md` | designer (спека узла) → builder → critic | `ai-packages/qa-factory/scripts/project_knowledge.py (_refuse_no_trace)`, `ai-packages/qa-factory/scripts/tests/test_project_knowledge.py` | PK0-1; вместе с PK2-11 (один класс) | ожидает |

## Живые доказательства

| Что | Статус |
|---|---|

## Ход

## Остатки
