# Переезд на GitHub (`github-move`)

приоритет: П1 | фичи: F19 | стенд: не нужен | зона: `tools/piles_gitlab*`, `tools/ci_read*`, `tools/dev_config.py`, `tools/install_parity.py`, `docs/migration/`

## Зачем

Форж переезжает в приватный репозиторий на GitHub, релизы фабрики — в публичный. На новом месте работа идёт так же: те же гейты и те же проверки в CI, но без внутренних имён, чужих данных и старой истории. На GitHub уходит один чистый коммит, и вынести запрещённое мешает проверка до отправки, а не память человека.

## Что не так сегодня (факты)

- Единственный скан точного дерева стоял после отправки на GitHub, а сборка шла руками (`docs/tasks/specs/reviews/t-1856-critic-plan-github-move.md`, F-1).
- Сканер печатает `total: 0` на пустом наборе файлов и пропускает двоичные (там же, F-2, F-4).
- `tools/ci_read.py` умеет читать только внутренний GitLab; черновики workflow отстали от `.gitlab-ci.yml` (`docs/tasks/specs/t-1855-github-move-nodes.md`, GM1-4, GM1-5).
- В публичный пакет ушли бы сырые данные Jira с именами сотрудников (`ai-packages/qa-factory/scripts/tests/fixtures/investigation-14857/`, F-18).

## Пачки

| № | Что изменится для пользователя | Строки | Размер | Статус | Взял | Ветка | MR |
|---|---|---|---|---|---|---|---|
| 1 | форж вне пакета готов к GitHub, main по-прежнему работает на GitLab | GM1-1, GM1-2, GM1-3, GM1-4, GM1-5, GM1-6, GM1-7, GM1-8, GM1-9, GM1-10, GM1-11 | L | закрыта | dev1, 04.11.2026 | `pile/github-move/batch-1` | `1e8cd2c1b` https://git.example.com/dev1/yml-text-factory/-/merge_requests/15 |
| 2 | пакет без внутренних имён, дерево готово к выгрузке | GM2-1, GM2-2, GM2-3, GM2-4, GM2-5, GM2-6, GM2-7 | M | закрыта | dev1, 05.11.2026 | `pile/github-move/batch-2` | `b0b92fb86` |

Статусы пачки: `ожидает` → `в работе` → `сдано` → `принято` → `закрыта`. Размер — по узлам: S ≤ 4 узлов,
M 5–9, L 10–15 (больше — две пачки). Взятая пачка заморожена: её файл правит только взявший, новое
по теме — файлом в `findings/`.

## Бриф пачки 1

Начать с волны А (GM1-1, GM1-2, GM1-3, GM1-6, GM1-8). Стенд не нужен, слово владельца получено. Подробно — `batch-1-chistka-vne-paketa.md`, раздел «Бриф».

## Дороги

Читать по порядку: эта карточка → `batch-1-chistka-vne-paketa.md` → раздел узла в `docs/tasks/specs/t-1855-github-move-nodes.md` и его §12–§13 → названные там F-n в `docs/tasks/specs/reviews/t-1856-critic-plan-github-move.md` → `docs/migration/MIGRATION_PLAN.md`.
Слова: `plans/features.json` F19 (поле `words`) и сверх них: `piles_gitlab`, `mirror_board`, `ci_read`, `backend_for`, `scrub_scan`, `cutover_export`, `cutover.json`, `dev_config`.
Не читать: `logs/journal/` и ветку `experiment/thinking-roles`: узлам они не нужны, ветка живёт в параллельной сессии.

## Содержание

Снимок 04.11.2026; пути — от корня репозитория; суть узлов — из спеки t-1855. При расхождении авторитетна доска `plans/PILES.md`. Каждый id строки карточки и каждый файл из `findings/` стоит здесь ровно один раз
(`tools/test_pile_cards_contents.py`); id строки стоит и в «Что» ровно одного узла файла своей пачки (`piles.py check` (д)).

| id / файл | вид | суть (≤ 20 слов) | пути | статус | слово владельца | связи |
|---|---|---|---|---|---|---|
| **Пачка 1** | | | | | | |
| GM1-1 | узел | `take`/`close` без зеркала, `piles_gitlab` удалён | `tools/piles.py`, `tools/piles_gitlab.py` | пачка 1 | O6, 04.11 | GM1-4, GM1-5 |
| GM1-2 | узел | конфиг разработчика без путей первого разработчика, старые ключи читаются | `tools/dev_config.py` | пачка 1 | FK-11 | GM1-4 |
| GM1-3 | узел | дверь `parity-skip:` из `git log` | `tools/install_parity.py` | пачка 1 | нет | GM1-5 |
| GM1-4 | узел | `ci_read` на GitHub по `origin`, GitLab отдельным файлом до переезда | `tools/ci_read.py` | пачка 1 | нет | GM1-1, GM1-2 |
| GM1-5 | узел | черновики workflow догоняют `.gitlab-ci.yml`, золото по ним | `docs/migration/forge-repo/.github/workflows/` | пачка 1 | FK-4 | GM1-1, GM1-6 |
| GM1-6 | узел | разовый сканер: пути, регистр, имена, двоичные; список переезда | `docs/migration/scrub_scan.py`, `docs/migration/cutover.json` | пачка 1 | FK-5, FK-11 | GM1-10 |
| GM1-7 | узел | сжатие контекста в PROJECT.md, зеркало из правил | `PROJECT.md`, `docs/RUNBOOK.md` | пачка 1 | нет | GM1-1 |
| GM1-8 | узел | LF для `.sh` и workflow, проверка `cloud_setup`, слаги на Linux | `.gitattributes`, `tools/test_cloud_setup.py` | пачка 1 | нет | — |
| GM1-9 | узел | `docs/provenance.md` без хостов и путей машины | `docs/provenance.md` | пачка 1 | нет | GM1-6 |
| GM1-10 | узел | инструмент выгрузки: дерево, скан, потом команда push; страж голого push | `docs/migration/cutover_export.py` | пачка 1 | нет | GM1-6 |
| GM1-11 | узел | остаток `tools/` вне названных узлов | `tools/test_collect_intake.py`, `tools/test_dispatch_manifest.py` | пачка 1 | нет | — |
| **Пачка 2** | | | | | | |
| GM2-1 | узел | LICENSE, манифесты, маркетплейс `qafactory`, URL установки | `ai-packages/qa-factory/LICENSE` | пачка 2 | O1a, O5 | пачка 1; t-1765 не вливается (владелец, 05.11.2026) |
| GM2-2 | узел | обезличивание пакета по O7, карта рядом с бандлом | `ai-packages/qa-factory/` | пачка 2 | O7, FK-11 | GM2-1 |
| GM2-3 | узел | документы форжа, `kb/` обезличен, `kb_publish` удалён | `PROJECT.md`, `kb/` | пачка 2 | FK-6, FK-11 | GM2-2 |
| GM2-4 | узел | отбор по O3, журнал не едет, список непереезжающего | `docs/migration/cutover.json` | пачка 2 | FK-14 | GM2-3, GM2-6 |
| GM2-5 | узел | `controller-blocks-gen.py` без внутренних имён | `tools/controller-blocks-gen.py` | пачка 2 | нет | пачка 1; t-1765 не вливается (владелец, 05.11.2026) |
| GM2-6 | узел | измерители под новым именем `experiments/measurers/` | `experiments/measurers/` | пачка 2 | O3 | пачка 1; t-1765 не вливается (владелец, 05.11.2026) |
| GM2-7 | узел | корпус с данными Jira заменён синтетикой той же формы | `ai-packages/qa-factory/scripts/tests/fixtures/investigation-14857/` | пачка 2 | FK-13 | GM2-2 |

## Входящие

`findings/` этой кучки; их число и дату последней показывает `plans/PILES.md` (собирает `piles.py board`; карточку код не правит).
Каждая новая находка тем же ходом получает строку в пачке этой кучки, которую ещё не взяли, или указатель `перенос: <кучка>/…`
(`piles.py check` (е)); нет такой пачки — открывается следующая со статусом «ожидает».

## Вопросы владельцу

- минуты Actions: решение после замера первой недели на GitHub (ночной `package-full` до 180 минут против 2000 минут в месяц; это оценка)
