# Знания о проекте (`project-knowledge`)

приоритет: П1 | фичи: F04 | стенд: нужен | зона: `ai-packages/qa-factory/scripts/project_knowledge.py`, `ai-packages/qa-factory/scripts/tests/test_project_knowledge.py`

## Зачем

Сегодня онбординг спрашивает обо всём сразу, а стори переспрашивает то, что ей не нужно или что человек уже говорил. Здесь строится одна
схема для всего, что фабрика узнаёт о проекте: основное спрашивается на онбординге, остальное — когда стори это впервые понадобилось;
ответ, который касается проекта или стенда, запоминается и больше не спрашивается. Новый вид знания добавляется строкой, а не новым
механизмом.

## Что не так сегодня (факты)

- План и разбор «как сейчас»: `plans/project-knowledge-plan.md` (разделы 1 и 7; раздел 7 главнее разделов 1–4).
- Гейт A спрашивает ключи входа на стенд у любой стори: `ai-packages/qa-factory/scripts/gate_preflight.py`, `check_s5_credentials`.
- Ответ человека запоминается пятью разными способами, общего нет: таблица раздела 1 плана и замечание C3 отчёта
  `docs/tasks/specs/reviews/20261110-project-knowledge-plan-critic.md`.

## Пачки

| № | Что изменится для пользователя | Строки | Размер | Статус | Взял | Ветка | MR |
|---|---|---|---|---|---|---|---|
| 1 | Фабрика помнит роли продукта и учётки по ролям на стенде: спрашивает учётку только когда она нужна кейсам стори и только один раз | — | M | закрыта | dev1, 11.11.2026 | `pile/project-knowledge/batch-1` | `5498318` |
| 2 | Ответ можно дать с условием и заменить без потери истории; противоречащие ответы видны, а не решаются последней записью; оглавление знаний не пропадает из брифа | — | M | ожидает | — | — | — |

## Бриф пачки 1

Начать с PK0-1 (реестр ответов) — от него зависят все остальные узлы. **Порядок, ворота и общие файлы — по общему плану
`docs/tasks/specs/t-2277-joint-plan-knowledge-pre-code-first-look.md` §4** (слово владельца 10–11.11.2026 заменяет прежнее «разработка не
начинается, пока не закончит сессия `thinking-roles`»: её ждут только узлы на её файлах; PK0-1 стартует сразу); перед диспатчем ссылки спеки на строки кода перемеряются.
Стенд нужен только для живого доказательства. Слово владельца не требуется: развилки спеки решены. Подробно — `batch-1-odin-fakt-naskvoz.md`.

## Дороги

Читать по порядку: эта карточка → `batch-1-odin-fakt-naskvoz.md` → спека `docs/tasks/specs/t-2142-project-knowledge-phase0.md` (узел
исполняется по разделу §5 со своим id; блок «Lead acceptance» — решения развилок) → отчёты критика
`docs/tasks/specs/reviews/20261110-t-2142-phase0-spec-critic.md` и `…-critic-r2.md` только при вопросе «почему так».
Слова: `plans/features.json` F04 и сверх них: `project_knowledge`, `roster`, `product_roles`, `check_role_accounts`,
`default_login_needed`, `credentials_by_role`, `record_stand_account`, `stand_gap_card_lines`, `card_door`, `covered_gaps`.
Не читать: разделы 1–4 плана как задание (их правит раздел 7); спеку t-1957 целиком (соседняя работа, нужны только §3.6–3.7).

## Содержание

Снимок 10.11.2026; пути — от корня репозитория. При расхождении авторитетна доска `plans/PILES.md`.

| id / файл | вид | суть (≤ 20 слов) | пути | статус | слово владельца | связи |
|---|---|---|---|---|---|---|
| **Пачка 1** | | | | | | |
| **Пачка 2** | | | | | | |
| `findings/20261111-chego-ne-hvataet-planu-znanij-po-vneshnemu-razboru.md` | находка | Условие ответа словами, замена и конфликт, защита оглавления в брифе, шире живое доказательство, выбор документа по имени | `plans/piles/project-knowledge/batch-2-usloviya-zamena-oglavlenie.md` | PK2-1…PK2-5, ожидает | владелец, 11.11.2026: «Да, так» | план знаний, фазы 2, 5, 6; t-2277 |
| `findings/20261111-default-ucherka-tri-karty-vne-invarianta.md` | находка | Неудовлетворённая учётка `default` всё ещё доходит до трёх карточек, вне инварианта PK0-4 (F-13) | `plans/piles/project-knowledge/batch-2-usloviya-zamena-oglavlenie.md` | PK2-6, ожидает | нет | остаток R-2 (i) t-2142; PK0-4 |
| `findings/20261111-stand-gap-karty-bez-strok-ceny.md` | находка | Карточки пробелов стенда без строк цены; `stand_gap_words` получают factory/you/story (FK-9 b) | `plans/piles/project-knowledge/batch-2-usloviya-zamena-oglavlenie.md` | PK2-7, ожидает | нужно: да (текст человеку) | остаток R-2 (ii) t-2142 |
| `findings/20261111-dva-isklyucheniya-punkta-f-ne-vzyaty.md` | находка | Два исключения пункта (f) не взяты; цена — лишний вопрос про вход по умолчанию | `plans/piles/project-knowledge/batch-2-usloviya-zamena-oglavlenie.md` | PK2-8, ожидает | нужно: да (взвесить цену) | остаток R-2 (iii) t-2142 |
| `findings/20261111-guard-globalnaya-opciya-pered-podkomandoj.md` | находка | Гард не видит глобальную опцию перед подкомандой у двух соседей; одна общая правка | `plans/piles/project-knowledge/batch-2-usloviya-zamena-oglavlenie.md` | PK2-9, ожидает | нет | остаток R-2 (iv) t-2142; PK0-8 |
| `findings/20261111-pervyj-vzglyad-ne-pishet-reestr-otvetov.md` | находка | Указатель: первый взгляд реестр не пишет, кандидаты в каталог фазы 1 — по слову владельца | `plans/piles/project-knowledge/batch-2-usloviya-zamena-oglavlenie.md` | PK2-10, ожидает | J-5: кодом ничего | t-2277 §6.1; фаза 1 плана |
| `findings/20261111-zapis-v-sleduemyj-sled-bez-proverki-no-trace.md` | находка | Писатели записей семейства не проверяют `no_trace`: эксперимент оставляет след; нужен один общий отказ | `plans/piles/project-knowledge/batch-2-usloviya-zamena-oglavlenie.md` | PK2-11, ожидает | нет | критик t-2349 (Q1); FR-53 |
| `findings/20261111-latest-dublirujet-covering-semejstva-zapisej.md` | находка | Правило «последняя запись» в двух местах: `_latest` и `ER.covering`; вынести в одну функцию | `plans/piles/project-knowledge/batch-2-usloviya-zamena-oglavlenie.md` | PK2-12, ожидает | нет | критик t-2349 (Q2) |
| `findings/20261111-zamok-zapisi-dublirujetsya-v-project-knowledge.md` | находка | Замок записи реестра знаний — копия замка решений; один помощник в `event_store` | `plans/piles/project-knowledge/batch-2-usloviya-zamena-oglavlenie.md` | PK2-13, ожидает | нет | критик t-2349 (Q3); AR-15 |
| `findings/20261111-chitatel-config-glotaet-nechitaemyj-config.md` | находка | Читатель `config.json` реестра знаний прячет нечитаемый конфиг как «пусто»; читать через `read_config_file` | `plans/piles/project-knowledge/batch-2-usloviya-zamena-oglavlenie.md` | PK2-14, ожидает | нет | критик t-2349 (Q4); FR-41 |
| `findings/20261111-spec-protivorechie-akkaunt-env-v-uslovii-vhoda.md` | находка | Спека t-2142 §3 (7): условие (c) и итог о кейсе с одним `env`-аккаунтом противоречат друг другу | `plans/piles/project-knowledge/batch-2-usloviya-zamena-oglavlenie.md` | PK2-15, ожидает | — | PK0-5; t-2361 |
| `findings/20261111-bez-vybrannogo-stenda-chelovek-slyshit-chto-netu-klyuchej.md` | находка | Без выбранного стенда вопрос о входе говорит «нет ключей», а не «стенд не выбран» | `plans/piles/project-knowledge/batch-2-usloviya-zamena-oglavlenie.md` | PK2-16, ожидает | — | PK0-5; t-2361 |
| `findings/20261111-akkaunt-kejsa-v-dvuh-mestah-odin-pomoshchnik.md` | находка | Аккаунт, который называет ручной кейс, определён в двух местах; нужен один помощник | `plans/piles/project-knowledge/batch-2-usloviya-zamena-oglavlenie.md` | PK2-17, ожидает | — | PK0-5; t-2361 |
| `findings/20261111-zapis-zamechennoj-roli-gonka-proverki-i-zapisi.md` | находка | Замеченная роль: проверка реестра без замка и запись под замком; ответ человека может быть перезаписан | `plans/piles/project-knowledge/batch-2-usloviya-zamena-oglavlenie.md` | PK2-18, ожидает | нет | критик t-2370 (PK0-3); AR-28 |
| `findings/20261112-s0-no-trace-komandy-dirizhera-pishut-v-reestr.md` | находка | В S0 прогона `--no-trace` `side`/`account`/`revoke` пишут строку в реестр: `pipeline.json` ещё нет, признак живёт в `launch.no_trace` | `plans/piles/project-knowledge/batch-2-usloviya-zamena-oglavlenie.md` | PK2-19, ожидает | нет | критик на план t-043 (N2); PK2-11; P8, FR-53, FR-59 |

## Что эта кучка вберёт из других (фазы 1–6 плана)

Узлы и строки ниже остаются в своих кучках, пока для фазы не написана спека; тогда они получают там `перенос: project-knowledge`
(узел PK0-10 пачки 1 ставит указатели для фазы 0).

| Фаза плана | Откуда | Что |
|---|---|---|
| 1 каталог и один читатель | `onboarding-forge` OH1-6, OH3-42, GW1-38; B-319; находка `forge` о чтении `test_data` мимо читателя | один читатель фактов, шесть мёртвых ключей |
| 2 шов и область ответа | `thinking-roles` TR3-10; B-294; находка `release-next` «роль правит конфиг проекта» | вопрос, который не держит кейсы; запись только со словами человека |
| 3 сторона стори | B-145, B-254, B-257, B-282; `onboarding-forge` SS1-11, OH3-17, SC5-13 | стенд и его карточка, возможности стенда |
| 4 онбординг | `onboarding-forge` OH3-35, OH3-2, OH1-7; B-220, B-234, B-295, B-411; тема интервью TR3-12 | шесть вопросов вместо сорока трёх |
| 5 знание доходит до ролей | спека t-636; B-190, B-133, B-415 | оглавление знаний в брифах |
| 6 накопление и доказательство | `live-runs` LR1-3, LR1-4, LR1-7; B-092 | `faq.md` больше не создаётся; счётчик вопросов на стори |

## Входящие

`findings/` этой кучки; их число и дату последней показывает `plans/PILES.md`.

## Вопросы владельцу

- нет: развилки В1–В8 плана и FK-1…FK-12 спеки решены 10.11.2026.
