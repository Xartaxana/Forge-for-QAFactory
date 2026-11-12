# Суженный свидетель билдера молчал в пяти из шести поздних дефектов: первым ловил канон, `main` стоял красным ~3 часа

id: — | кучка: `forge` | от: Lead, калибровка 12.11.2026 (`docs/tasks/specs/reports/calibration-20261112.md`, п. 2), записал builder t-093 | приоритет: П1 | кандидат наверх: нет

## Что не так

Класс: «свидетель узла (`scenario_walk.py --witness-for <owns>`) покрывает тесты собственных файлов узла, но не читателей, храповики и
время перенесённого; слой, который ловит дальше, — канон на CI после пуша». Вопрос Lead к механизму: какие быстрые проверки
интегратор обязан гонять ДО пуша сверх свидетелей узлов.

Свидетель (часть p3, `docs/tasks/specs/reports/calibration-20261112-p3.md`, проверка 24; p2, 13(j)):
- 6 `defect_found` в окне; CI/канон поймал 5, критик 1 (t-037); молчал в 5 из 6 один и тот же слой — суженный свидетель билдера (p3, 24,
  итог «Summary by gate»): t-005 (`test_audit_rules` вне свидетеля), t-054 (`test_probe_walk_edges` читал то, что узел убрал), t-053
  (pytest собрал `tools/test_split.py` как тест; правило A1 назвало `module_facade.py` мёртвым скриптом; `test_walk_lanes_parallel` красный
  только на Linux), t-060 (`test_driver_layers.py` 300 с на CI при 72 с локально; канон 43150280844), t-047
  (`test_story_run_stand_identity.py` 300 с, `module_facade.install` компилирует каждую часть второй раз).
- `main` стоял красным 12.11 с ~03:00 до ~06:20 (запись Lead, калибровка п. 2).
- свидетель не входит в `witness` целиком: для узла, владеющего `harness.py`, `--witness-for` печатает сотни `keep`-строк или «run the
  whole scenario layer» (p2, 13(j), t-085/t-086), то есть правило 4 `CLAUDE.md` для таких узлов недостижимо.

## Что именно менять

Направление: по записи («какие быстрые проверки интегратор гоняет до пуша»). Часть I — документ, исполняется сразу; часть II — механизм,
решение владельца нужно (перевод в код-гейт); исполнять по рекомендации.

1. **Часть I (документ, builder).** `docs/RUNBOOK.md` §7 (раздел «интегратор перед пушем»): список быстрых проверок до пуша сверх
   свидетелей узлов, каждая с командой и временем: `python -B ai-packages/qa-factory/scripts/selftest.py --lang --limits` (уже
   положена PROJECT.md п. 2), `python -B ai-packages/qa-factory/scripts/tests/test_audit_rules.py` (~5 с; ловит класс t-005/t-053 A1),
   `python -m pytest tools/ --collect-only -q` (класс «`test_*.py` в `tools/` собирается как тест», t-053), `python -B tools/lint_ratchet.py
   --check` (храповик линтера). Тест: ручной ключ-прогон DOC-DISPATCH WITNESS (правило 11 `CLAUDE.md`): ключи цитируются из DoD
   до прогона, скрипт приложен к отчёту, негативный контроль.
2. **Часть II (код, designer → builder → critic).** `scenario_walk.py --witness-for <path>` печатает также тесты читателей того,
   что узел двигает (строки `reader` — по осям `docs/SIBLING_MAP.md` и `test-layers.json` `keep`/`covers`) и отдельную строку
   `runtime`: секунды файла из `ai-packages/qa-factory/scripts/slow_tests.json` против потолка CI 300 с; файл выше 240 с — строка-
   предупреждение «file X at N s of 300: cut or in-process before adding code to it». Тест: `ai-packages/qa-factory/scripts/tests/` —
   тест `scenario_walk` с параметрами: путь с читателем / путь без читателей / файл ниже и выше 240 с.
   Края: `harness.py` и общие модули дают сотни строк — вывод ограничивается списком «ближайших» (первый уровень импортёров),
   остальное одной строкой «+N readers, run the scenario layer in CI» (решение: что считать «ближайшими» — спрашивает designer
   у Lead, развилкой в спеке).

Исполнитель: часть I — builder; часть II — designer → builder → critic.

## Связи

`20261111-svidetel-dlya-putej-vne-paketa-odin-put.md` (FG7-15: тот же `scenario_walk.py`, файл `test-layers.json`; порядок: после FG7-15);
`20261112-spec-dispatchera-ne-nesyot-sosednij-klass.md` (тот же класс со стороны постановки); `20261015-slow-tests-spisok-selftest-ustarel.md`
(F6-18: список `SLOW_TESTS`). Правила 4, 10 `CLAUDE.md`; `plans/builder-rules.md` п. 7b.

Принципы и правила: P27, P31; AR-29, AR-19; FR-31, FR-54.

Решение владельца нужно: да — вопрос простыми словами: «Показывать ли в свидетеле узла тесты читателей перенесённого и время файла против
потолка CI (предупреждение до пуша), а не ждать красного канона? Рекомендация: да; цена — длиннее вывод свидетеля, быстрее красный».

<!-- id выдаёт интегратор при сборке пачки. -->
