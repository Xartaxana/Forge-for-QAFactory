# Знания о проекте — пачка 1: роли продукта и учётки по ролям запоминаются и спрашиваются по нужде

кучка: `project-knowledge` | статус: в работе | взял: dev1, 11.11.2026 | ветка: `pile/project-knowledge/batch-1` | MR: — | стенд: нужен | приоритет: П1 | issue: https://git.example.com/dev1/yml-text-factory/-/work_items/74

Правило готовности: пачка закрыта, когда каждый узел «принято», свидетели узлов — в журнале взявшего,
живые доказательства (FR-33) сделаны или переданы строкой в кучку «живые прогоны».

Решения владельца: слово владельца 10.11.2026 — план `plans/project-knowledge-plan.md` (В1–В8), развилки спеки FK-3, FK-4, FK-6 «по рекомендациям»; «саму разработку не начинаем, пока не закончит параллельная сессия».
очередь: project-knowledge/1 → pre-code/1 (`scripts/project_knowledge.py`, `scripts/guard_pre_tool.py`: PK0-1, PK0-8 → PC-1b; `docs/SIBLING_MAP.md` ось 34: PK0-6 → PC-10)
очередь: project-knowledge/1 → pre-code/1
очередь: project-knowledge/1 → github-move/3
Порядок по общим файлам: `scripts/tests/fixtures/judgment-census.json`: PK0-1 → PK0-4; `scripts/gate_preflight.py`: PK0-4 → PK0-9, PK0-5 — другие функции; `scripts/stand_gaps.py`, `scripts/gate_brief.py`: PK0-4 → PK0-9; `scripts/story_run.py`: PK0-3, PK0-5, PK0-9 — разные функции, поздний сливает ветку; `scripts/project_knowledge.py`: PK0-1 → PK0-3; `scripts/guard_pre_tool.py`: PK0-8 после слияния TR3-5, TR3-14, TR3-16 кучки `thinking-roles`.
Скоуп свидетеля: новый тестовый файл узла и быстрые соседние, названные в узле спеки (до минуты каждый); файлы из списка медленных, `test_story_run_*`, `test_controller_*`, `test_judgment_census.py` — только CI; канон пачки — пайплайн CI.
Общий бриф: узел исполняется по разделу §5 спеки `docs/tasks/specs/t-2142-project-knowledge-phase0.md` со своим id; поведение — §2–§4, решения развилок — блок «Lead acceptance». Повышение храповика одобрено одно: `judgment-census.json` `safety` 51 → 52 (PK0-1); любое другое — стоп и возврат.

## Бриф

Цель пачки — доказать схему на одном факте до того, как заполнять каталог: стратег получает перечень ролей, вопрос об учётке задаётся
только по роли, нужной кейсам стори, ответ записывается и переживает закрытие стори, следующая стори не спрашивает. Начать с PK0-1; после
него PK0-2, PK0-3, PK0-4, PK0-5, PK0-8 идут параллельно, PK0-9 — после PK0-4, PK0-6 — последним. **До первого диспатча:** параллельная
сессия закончила; каждая ссылка `путь:строка` спеки перемерена по ветке; U-5 спеки оставлен тесту узла PK0-3.

## Узлы

Статусы: `ожидает` → `в работе` → `сдано` → `принято` / `отклонено`.

| Узел | Приоритет | Что | Исполнитель | Пишет в | Зависит от | Статус |
|---|---|---|---|---|---|---|
| PK0-1 | П1 | Реестр ответов `records/project-knowledge.json`: чтение без записи, один писатель под замком, отмена, команды дирижёра; первый тест — факт переживает закрытие стори. Спека §2, §5 PK0-1 | builder → critic | `scripts/project_knowledge.py`, `scripts/tests/test_project_knowledge.py`, `references/install-paths.json`, `references/collect-sets.json`, `references/conductor-actions.json`, `references/state-exits.md`, `scripts/tests/fixtures/judgment-census.json`, `changelog.d/t-2142-pk0-1.md` | — | принято |
| PK0-2 | П1 | Перечень ролей продукта в брифе стратега S3 и абзац опыта в его хартии. Спека §3 (1), §5 PK0-2 | builder → critic | `scripts/brief_pack.py`, `agents/qa-test-strategist.md`, `scripts/tests/test_brief_s3_roster.py`, `changelog.d/t-2142-pk0-2.md` | PK0-1 | принято |
| PK0-3 | П1 | Необязательный раздел `product_roles` передачи S3; замеченная стратегом роль записывается как неподтверждённая. Спека §3 (6), §5 PK0-3 | builder → critic | `handoffs/s3-strategist-to-designer.yaml`, `scripts/project_knowledge.py`, `scripts/story_run.py`, `scripts/tests/test_knowledge_notice.py`, `changelog.d/t-2142-pk0-3.md` | PK0-1 | принято |
| PK0-4 | П1 | Карточка гейта A на пару «стенд + роль» по дороге карточек пробелов стенда, карточка подтверждения замеченных ролей, строка «действую по прежним ответам». Спека §3 (2), (5), (6), §5 PK0-4 | builder → critic | `scripts/gate_preflight.py`, `scripts/stand_gaps.py`, `scripts/gate_brief.py`, `scripts/tests/test_gate_role_accounts.py`, `scripts/tests/fixtures/judgment-census.json`, `changelog.d/t-2142-pk0-4.md` | PK0-1 | принято |
| PK0-5 | П1 | Учётка стенда по умолчанию спрашивается одним правилом и только по нужде — на гейте A и перед ручным проходом. Спека §3 (7), §5 PK0-5 | builder → critic | `scripts/gate_preflight.py`, `scripts/story_run.py`, `scripts/tests/test_login_need.py`, `changelog.d/t-2142-pk0-5.md` | PK0-1 | принято |
| PK0-6 | П2 | Тексты для дирижёра, ось «память ответа человека» в карте симметрий, правка текста AR-3 и пересборка индекса. Спека §5 PK0-6 | builder | `skills/qa-story/phases/s4.md`, `references/environments.md`, `design/architecture.md`, `docs/SIBLING_MAP.md`, `docs/ARCHITECTURE_INDEX.md`, `changelog.d/t-2142-pk0-6.md` | PK0-1, PK0-2, PK0-3, PK0-4, PK0-5, PK0-8, PK0-9 | принято |
| PK0-8 | П1 | Команды записи в реестр закрыты от ролей стражем: записывает только дирижёр со словами человека. Спека §5 PK0-8 | builder → critic | `scripts/guard_pre_tool.py`, `scripts/tests/test_guard_project_knowledge.py`, `changelog.d/t-2142-pk0-8.md` | PK0-1; слияние TR3-5, TR3-14, TR3-16 | принято |
| PK0-9 | П1 | Ответ «это не роль продукта» не переспрашивается ни на гейте A, ни на гейте B следующих стори. Спека §3 (2b), §5 PK0-9 | builder → critic | `scripts/gate_preflight.py`, `scripts/stand_gaps.py`, `scripts/gate_brief.py`, `scripts/story_run.py`, `scripts/tests/test_not_a_role_carry.py`, `changelog.d/t-2142-pk0-9.md` | PK0-4 | принято |
| PK0-10 | П2 | Остатки спеки (§6 R-2) заведены находками этой кучки; у узлов и строк других кучек, которые вбирает фаза 0, стоит `перенос: project-knowledge` (таблица карточки) | builder | `plans/piles/project-knowledge/findings/`, `plans/piles/project-knowledge/README.md` | — | принято |

Имена тестовых файлов PK0-8 и PK0-9 — по спеке §5; при расхождении верна спека.

## Ход

Журнал передачи Lead пачки, новые записи в конец: `<дата время> — <что сделано, диспатчи t-nnn, хэши>`.

- 10.11.2026 — пачка открыта: план (критик t-2104), спека t-2142 в третьей редакции (критик t-2143, повторный проход t-2159). Кода нет; старт — после окончания параллельной сессии.
- 11.11.2026 — узлы PK0-1…PK0-6, PK0-8, PK0-9, PK0-10 приняты: код слит в ветке эксперимента 11.11 по общему плану t-2277 и пришёл в `main` коммитом слияния `5498318`. Свидетели — журнал сессии общего плана (бандл истории, `docs/tasks/compact-snapshots/journal-root-copy-2026-11-11.jsonl` ветки `exp-final`; в `main` этого файла нет): PK0-1 t-2333, фикс t-2359, критик t-2349; PK0-2 t-2345, фикс t-2367, критик t-2358; PK0-3 t-2364, фикс t-2379, критик t-2370; PK0-4 t-2397/t-2428, критик t-2407; PK0-5 t-2350, фикс t-2372, критик t-2365; PK0-6 t-2467; PK0-8 t-2346, фикс t-2367, критик t-2358; PK0-9 t-2408/t-2457, критик t-2443; PK0-10 — находки R-2 заведены (коммит эксперимента `dd036135d`). Статусы проставлены 11.11 при сверке бэклога с историей слияния. Пачка не закрыта: живое доказательство PK0-7 не сделано.

## Живые доказательства

| Что | Стенд / проект | Кто | Статус |
|---|---|---|---|
| Две стори подряд на одном стенде: в первой один вопрос об учётке роли и подтверждение замеченных ролей, запись жива после закрытия стори; вторая не спрашивает и говорит, что действует по прежнему ответу (спека §8, PK0-7) | MyBooks | Lead пачки | ожидает |

## Остатки
