# Список env-файлов и пустые значения читаются разными дорогами: `gate_preflight.env_values` бросает пустые, `stand_health._env_values` нет; список файлов читают мимо `configured_env_files`

id: — | кучка: `onboarding-forge` | от: слова Lead 12.11.2026 (`gate_preflight.env_values` против `stand_health`); критик t-172 (`docs/tasks/specs/reviews/t-172-of3-1-bde-diff.md`: R-1 «OF3-1e2», e-1, строка «a lone quote kept»), 12.11.2026 | приоритет: П3 | кандидат наверх: нет

## Что наблюдалось (по main; OF3-1 e на ветке `wip/of3-1e`, в main нет)

1. Пустые значения: `scripts/gate_preflight.py` `env_values` (:1043-1053) — «процесс с наложенными файлами, пустые значения опущены» (`str(v or "").strip()`); `scripts/stand_health.py` `_env_values` (:432-442) — `dict(os.environ)` + `parse_env_file(...)` без отбрасывания пустых. Один и тот же ключ с пустым значением для одного читателя «задан пустым», для другого «не задан» (AR-13).
2. Список файлов: `stand_health._env_values` читает один `cfg["env_file"]`; шлюз читает список `gate_preflight.configured_env_files`. Критик t-172 R-1: список ещё читают мимо — `machine_facts.secret_values` (только `env_file`), `source_inventory` (:60-68, оба ключа), `env_probe._frontend_hint` (:518), ключи стенда (:483), `load_env` (:131) — только `env_file`; в `machine_facts._env_file_values` остался мёртвый срез `export `. `load_env` порядок — не цель (F11 спеки), список файлов — цель.
3. e-1: `scripts/tests/test_manual_capture.py` — 4 строки с литеральным U+FEFF внутри строковых литералов (проходит `--lang`, но читатель не видит, где BOM); строка теста «a lone quote kept» (`A="` → `"`) фиксирует выбор: на `gate_preflight.env_values` такой ключ раньше отсутствовал, теперь «задан» — направление ошибки «задан» на искажённой строке принято критиком, названо.

## Что именно менять

1. Одно правило пустых значений: функция `env_values` (или её вызов) в `gate_preflight` остаётся единственным читателем «что задано для запуска», `stand_health._env_values` вызывает её (с тем же списком файлов `configured_env_files`); решение «пустое значение — не задано» — как в `gate_preflight` (так читает человек: пустая переменная не адрес).
2. Список файлов: `machine_facts.secret_values`, `source_inventory`, `env_probe` (:131, :483, :518) берут список через `gate_preflight.configured_env_files`; мёртвый срез `export ` в `machine_facts._env_file_values` удаляется.
3. e-1: в `test_manual_capture.py` литералы `""﻿"` вместо невидимых символов.
4. Тест: таблица случаев в `scripts/tests/test_stand_health.py` и `scripts/tests/test_gate_preflight.py`: ключ пустой в файле / в процессе / в обоих × читатель шлюза и читатель `stand_health` — одно и то же; конфиг с `env_files` из двух файлов: все названные читатели видят оба.
5. Порядок: после слияния OF3-1 e (`wip/of3-1e`) и OF1-1 (`env_probe.py`, `очередь: OF1-1 → …` спеки OF3-1).

Принципы и правила: FR-54, FR-58; AR-13, AR-15.

Решение владельца нужно: нет.
