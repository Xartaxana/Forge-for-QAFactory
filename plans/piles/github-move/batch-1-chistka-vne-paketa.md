# Переезд на GitHub — пачка 1: форж вне пакета готов к GitHub, main по-прежнему работает на GitLab

кучка: `github-move` | статус: закрыта | взял: dev1, 04.11.2026 | ветка: `pile/github-move/batch-1` | MR: `1e8cd2c1b` https://git.example.com/dev1/yml-text-factory/-/merge_requests/15 | стенд: не нужен

Правило готовности: пачка закрыта, когда каждый узел «принято», свидетели узлов — в журнале взявшего.

Решения владельца: O1–O9 (`docs/migration/MIGRATION_PLAN.md`, 03.11.2026); слова владельца 04.11.2026 — «начать чистку сейчас, пакет позже» и ответы по форкам (спека t-1855, §12).
Порядок по общим файлам: `tools/test_ci_layout.py`: GM1-1 → GM1-5; `tools/ci_read.py` после GM1-1, GM1-2; `PROJECT.md`: только GM1-7, последним.
Скоуп свидетеля: тестовый файл каждого пути `owns`, команда — `docs/tasks/specs/t-1855-github-move-nodes.md`, раздел узла; полный канон — пайплайн ветки, интегратор.
Общий бриф дизайнерам: спека `docs/tasks/specs/t-1855-github-move-nodes.md` — узлы уже написаны, дизайнер не нужен; §12 и §13 спеки главнее её разделов.

## Бриф

Начать с волны А (GM1-1, GM1-2, GM1-3, GM1-6, GM1-8). Волна Б (GM1-4, GM1-5, GM1-9, GM1-10, GM1-11) — после неё, GM1-7 последним. Стенд не нужен, ветка `pile/github-move/batch-1`. main работает на GitLab до D2; всё, что нельзя посадить, сводится к списку `docs/migration/cutover.json`. Пути механизмов билдер оставляет staged, коммитит Fable Lead.

## Узлы

Исполнитель «builder → critic» — кодовый узел; «builder» — узел-документ. Статусы:
`ожидает` → `в работе` → `сдано` → `принято` / `отклонено`.

| Узел | Приоритет | Что | Исполнитель | Пишет в | Зависит от | Статус |
|---|---|---|---|---|---|---|
| GM1-1 | П1 | GM1-1: `take`/`close` без зеркала, `piles_gitlab` удалён, `sanitize` и `why_paragraph` переехали | builder → critic | `tools/piles.py`, `tools/piles_gitlab.py`, `tools/test_piles_gitlab.py`, `tools/piles_gitlab_users.json`, `tools/collect_intake.py`, `tools/test_pile_cards_contents.py`, `tools/test_piles_take.py`, `tools/test_piles_close.py`, `tools/test_piles_frozen.py`, `tools/mechanism_gate.py`, `tools/test_streams.py`, `tools/test_ci_layout.py`, `.gitlab-ci.yml`, `docs/SIBLING_MAP.md`, `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md`, `plans/piles/_template/batch.md` | — | принято |
| GM1-2 | П1 | GM1-2: `release_repo_root`, `github_token_env`, без путей первого разработчика; старые ключи читаются | builder → critic | `tools/dev_config.py`, `tools/dev.config.example.yaml`, `tools/test_dev_config.py`, `experiments/measurers/paths.py` | — | принято |
| GM1-3 | П1 | GM1-3: дверь `parity-skip:` из `git log`, не из `CI_COMMIT_MESSAGE` | builder → critic | `tools/install_parity.py`, `tools/test_install_parity.py` | — | принято |
| GM1-4 | П1 | GM1-4: `ci_read` на GitHub по `origin`, GitLab отдельным файлом до переезда | builder → critic | `tools/ci_read.py`, `tools/ci_read_common.py`, `tools/ci_read_gitlab.py`, `tools/test_ci_read.py`, `tools/test_ci_read_gitlab.py` | GM1-1, GM1-2 | принято |
| GM1-5 | П1 | GM1-5: черновики workflow догоняют `.gitlab-ci.yml`, золото по ним, пины GitLab собраны в один файл | builder → critic | `tools/test_workflows.py`, `tools/test_ci_layout.py`, `tools/test_crap_report.py`, `tools/test_dup_ratchet.py`, `docs/migration/forge-repo/.github/workflows/forge-check.yml`, `docs/migration/forge-repo/.github/workflows/nightly.yml`, `docs/migration/forge-repo/.github/workflows/canon.yml`, `docs/migration/qafactory-repo/.github/workflows/package-check.yml`, `docs/migration/forge-repo/cloud-setup.sh` | GM1-1, GM1-6 | принято |
| GM1-6 | П1 | GM1-6: разовый сканер — пути, регистр, имена, двоичные, ноль файлов как отказ; список переезда | builder → critic | `docs/migration/scrub_scan.py`, `docs/migration/scrub_rules.json`, `docs/migration/cutover.json`, `docs/migration/MIGRATION_PLAN.md`, `tools/test_scrub_scan.py` | — | принято |
| GM1-7 | П2 | GM1-7: сжатие контекста в PROJECT.md, зеркало из правил | builder | `PROJECT.md`, `docs/RUNBOOK.md` | GM1-1 | принято |
| GM1-8 | П2 | GM1-8: LF для `.sh` и workflow, проверка `cloud_setup`, строки тестов на ветки Windows и слаги, `*.bundle` в `.gitignore` | builder → critic | `.gitattributes`, `.gitignore`, `docs/migration/forge-repo/cloud-setup.sh`, `tools/test_cloud_setup.py`, `tools/test_agent_budget.py`, `tools/test_exam_runner.py`, `tools/test_permission_audit.py` | — | принято |
| GM1-9 | П3 | GM1-9: `docs/provenance.md` без хостов и путей машины | builder | `docs/provenance.md` | GM1-6 | принято |
| GM1-10 | П1 | GM1-10: инструмент выгрузки — дерево через временный индекс, скан, два коммита, команда push только на зелёном; содержимое стража `pre-push` | builder → critic | `docs/migration/cutover_export.py`, `tools/test_cutover_export.py` | GM1-6 | принято |
| GM1-11 | П2 | GM1-11: остаток `tools/` вне названных узлов (§7 C спеки, FK-8) | builder → critic | `tools/test_collect_intake.py`, `tools/test_dispatch_manifest.py`, `tools/test_dispatch_gate.py`, `tools/test_dod_track.py`, `tools/fixtures/dispatch_manifest/`, `tools/claude-mods/cost-band/.claude-plugin/plugin.json` | GM1-1 | принято |

## Ход

- 04.11: критик t-1877 по волне А: GM1-3, GM1-8 приняты и слиты; GM1-1 принят, дополнение t-1881 в работе, коммитит Fable; GM1-2 и GM1-6 в фикс-раунде. GM1-9, GM1-10, GM1-11 сданы, ждут критика волны Б.
- 04.11, вечер (Fable): GM1-1 с t-1881 закоммичен (`24f7291f2`), GM1-2 с фиксом закоммичен; слиты GM1-6 с фиксом, GM1-9, GM1-11, GM1-10 с дополнением t-1882 (24 passed); страж `.githooks/pre-push` на живом пути (`8bd28327f`). Запущены GM1-4 (t-1887), GM1-5 (t-1888), GM1-7 (t-1889). Дальше критик волны Б и канон — пайплайн ветки.
- 05.11, ночь (Fable): критик волны Б t-1893 (fit_with_fixes) закрыт фикс-раундами A/B/C (t-1894, t-1895, t-1896) и правками Lead F-12/F-13; GM1-4, GM1-5, GM1-7 слиты. Линт `main` (3 импорта пакета) починен t-1900, дубль `main` от X7-2 записан в базу ратчета (`11a6f467c`). Канон — пайплайн 8035798 на `d53bde37c`: `forge-check` зелёный (7566 passed, 21 skipped), `package-fast`/`package-full` красные от `main` (`test_stage_joints`, якорь «Witness» в хартиях) — наследованное, пачка `ai-packages/` не трогает. Все узлы приняты, журнал t-1871…t-1896 с BATCH CANON. Очередь: остаток F-14 (длина `run_checks`), `jev` в тестах — GM2-6, один детектор мира `test_cloud_setup.script_path`/`live_or_draft`.

## Живые доказательства

| Что | Стенд / проект | Кто | Статус |
|---|---|---|---|

## Остатки

