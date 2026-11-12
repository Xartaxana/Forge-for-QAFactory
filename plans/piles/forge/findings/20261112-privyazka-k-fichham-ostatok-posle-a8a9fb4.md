# Привязка к фичам: 85 находок, пять файлов CI и один тестовый файл без фичи; файлы новой резки тестов привязаны этим же ходом

id: — | кучка: `forge` | от: Lead, калибровка 12.11.2026 (`docs/tasks/specs/reports/calibration-20261112.md`, п. 11), записал builder t-093 | приоритет: П3 | кандидат наверх: нет

## Что не так

Класс: «реестр фич `plans/features.json` отстаёт от дерева: новый файл не получает фичи, и ни один шаг, добавляющий файл, этого не
требует (проверка `forge_metrics.py --check --base` стоит в pre-commit как `--warn`)». Следствие: показатели хрупкости фич считаются по
неполному дереву.

Свидетель (часть p4, проверка 31; печать `python -B tools/forge_metrics.py --window 2026-11-05`):
- 85 находок без привязки — все первые под `plans/piles/live-runs/` (карточка `live-runs` несёт `фичи: —`);
- пять отслеживаемых файлов вне пакета: `.github/workflows/canon.yml`, `forge-check.yml`, `nightly.yml`, `quarantine-watch.yml`, `scenario-clock.yml`;
- файл пакета `ai-packages/qa-factory/scripts/tests/test_manifest_projection.py`;
- 29 файлов резки тестов `a8a9fb4` (шесть `*_common.py` и 23 части) — **сделано этим ходом** правкой `plans/features.json` (t-093):
  `test_controller_rework_*.py` и `controller_rework_common.py` → F05; `test_no_move_seam_*.py`, `no_move_seam_common.py`,
  `test_infra_failure_*.py`, `infra_failure_common.py`, `story_run_*_common.py` → F06; `handoff_values_common.py` → F12. Части
  `test_story_run_freshness_*`, `test_story_run_loop_b_*` (F06, глоб `test_story_run*.py`) и `test_handoff_values_*` (F12, глоб `test_handoff*.py`)
  попадали под существующие глобы уже до правки; все шесть старых файлов привязаны были (F05/F06/F12), без привязки — только новые общие модули
  и части трёх основ. Свидетель правки: `python -B tools/forge_metrics.py --window 2026-11-12` печатает «files in window commits matching
  no feature: 0» и «Overlaps: 0».

## Что именно менять

1. `plans/features.json`: `.github/workflows/*.yml` → F19 (корень `repo`, как у остальных файлов форджа этой фичи; проверить, что у F19 есть
   блок `root: repo`, иначе — открыть для него блок); `scripts/tests/test_manifest_projection.py` → фича файла `scripts/manifest_put.py`
   (по строке 533 реестра), ПРОВЕРИТЬ командой `python -B tools/forge_metrics.py --window 2026-11-05`, что после правки «matching no feature: 0».
2. 85 находок: поле `фичи:` в шапке `plans/piles/live-runs/README.md` — выбрать фичу(и) по теме находок кучки (живые доказательства
   правок поведения роли: по FR-33 это F15 «package hygiene and self-checks» или по стадиям — выбор Lead пачки, развилка с рекомендацией
   F15); проверка: «findings with no attribution» падает с 85. Тест: `python -m pytest tools/test_forge_metrics.py -q`.
3. Детектор: `forge_metrics.py --check` остаётся предупреждением (P1); число «без привязки» — строка калибровки.

Края: файл, подходящий двум фичам, берёт первую по порядку реестра (`Overlaps` показывает); пустая шапка `фичи:` у кучки — находки
остаются без привязки и это явно в строке отчёта.

Исполнитель: builder (узел-документ).

## Связи

`20261028-globy-f04-f05-v-features-json-perekryvayutsya.md` (`onboarding-forge`, F6-49: тот же файл и порядок глобов).

Принципы и правила: P11, P31; AR-19; FR-54.

Решение владельца нужно: нет (выбор фичи для `live-runs` решает Lead пачки).

<!-- id выдаёт интегратор при сборке пачки. -->
