# Пакет называет старые пути `readiness.json` и `obligations.md`: дашборд показывает человеку `qa-factory/state/obligations.md`, `stages.json` пишет `project:readiness.json`

id: — | кучка: `onboarding-forge` | от: Lead-сессия (Opus), 26.10.2026, по очереди из «Хода» `kb/batch-1-kb-update.md` (20.10 18:2x, критик t-1147) | приоритет: П3 | кандидат наверх: нет

Слово владельца 26.10.2026 (чат): «внеси сейчас, чтобы не потерялось».

## Откуда

Критик t-1147 (KB1-3, 20.10) нашёл на страницах КБ три ложных пути и сверил их по `runtime_paths.py`: coverage map и estimation ledger
лежат в `qa-factory/records/`, `readiness.json` — в `qa-factory/state/`, `obligations.md` — в корне `qa-factory/`. Страницы КБ поправлены
(`cfd1743a`), а аналоги в самом пакете Lead поставил в очередь «строкой в невзятую пачку driver-controller». Строки не появилось — эта
находка её закрывает.

## Что на `main` (26.10.2026, `7ecf7974`; пути от `ai-packages/qa-factory/`)

- `scripts/factory_dashboard.py:3582` — текст, который читает человек на дашборде: «Ledger: qa-factory/state/obligations.md; written by S8/S9…».
  Канон — `qa-factory/obligations.md`: так говорит `ledger_path()` в том же файле (`:973-984`, `state/` — только старое место до 0.3.0).
  Нарушение FR-37 (путь в тексте человеку — не тот, что пишет код).
- `scripts/factory_dashboard.py:1362`, `:3536` — комментарии с тем же старым путём `state/obligations.md`.
- `references/stages.json:17` — выход S0 `"project:readiness.json"`: старое место рядом с `config.json`; сейчас `state/readiness.json`
  (`runtime_paths.py:41-42`, `readiness()` / `readiness_write()` `:107-114`).
- Соседи того же написания, проверить тем же ходом: `scripts/brief_pack.py:71` (скаут `qa-scout` получает `project:readiness.json` в бриф),
  `references/artifact-writers.json:192` (`project:readiness.json`). Важно понять, разрешается ли `project:readiness.json` через
  `runtime_paths.readiness()` (тогда это только слово в данных) или читается буквально (тогда скаут получает путь к файлу, которого на
  проекте после реонбординга нет).

## Что сделать

Один путь у одного факта (AR-13: факт с функцией-читателем читается только через неё): тексты и комментарии дашборда называют
`qa-factory/obligations.md`; строки `project:readiness.json` в данных либо называют новое место, либо доказанно разрешаются через
`readiness()`; тест на текст дашборда, если такого нет. Соседей искать по `docs/SIBLING_MAP.md` (ось путей артефактов).

Узел: `batch-1-controller-seams.md` DC1-10.
