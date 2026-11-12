# Носитель переживает резку без изменений: `source-split-carriers.json` проверяет носитель по файлу-оболочке, `named_by` ключей `split-keep` наследуются устаревшими

id: — | кучка: `forge` | от: builder t-093 по записи Lead 12.11.2026 (после резки `a8a9fb4`; `docs/tasks/specs/td-11c-test-split.md`) | приоритет: П2 | кандидат наверх: нет

## Что не так

Класс: «указатель на носитель (файл в `verify`, строка `file:line` в `named_by`) переносится инструментом резки КАК ЕСТЬ, и после резки он
либо ничего не проверяет, либо ведёт не туда». Два экземпляра:

1. `tools/source-split-carriers.json:19-20` (носитель с `id: 4`, форма `py-tuple`, файл `scripts/audit_factory.py`): `verify` содержит
   `{"args": ["scripts/tests/test_no_move_seam.py"], "verify_timeout": 300}`. После резки `a8a9fb4` `test_no_move_seam.py` — оболочка (shim)
   над пятью частями `test_no_move_seam_{n1_n9,n2b_n15,sites,k4s,c26_g27_f2}.py` и `no_move_seam_common.py` (`docs/tasks/specs/td-11c-test-split.md` §7,
   N2: «test_no_move_seam.py (+shim)»), поэтому проверка носителя через оболочку пуста: она не исполняет тестов частей.
2. `named_by` строк `keep`, которые пишет `split-keep` (`tools/test_split.py:1835-1837`: «test-layers.json keep: add ... inherit
   layer/why(+" (part of {old} split, TD-11c)")/named_by/...»), наследуются от материнского файла, включая номера строк. Строки частей
   `test_handoff_values_*` указывают `design/state-exits.md:112` (`ai-packages/qa-factory/scripts/tests/test-layers.json` строки 2240, 2273, 2306;
   ещё одна ссылка на то же в тексте `why`, строка 3671), а текст, о котором речь (строка таблицы `<dispatch>.values.yaml`), стоит в
   `ai-packages/qa-factory/design/state-exits.md:120` (прочитано прямым чтением строк 118–121).

## Что именно менять

Направление выбрано: починить экземпляры сейчас, классом — не наследовать номер строки.

1. `tools/source-split-carriers.json` (строка 19–20): `verify` носителя 4 — части вместо оболочки: `scripts/tests/test_audit_rules.py` и пять
   `scripts/tests/test_no_move_seam_*.py` (каждый со своим `verify_timeout`, значение — по `ai-packages/qa-factory/scripts/slow_tests.json`;
   оболочка остаётся в списке, только если она сама что-то исполняет — проверить чтением файла). Тест: `python -B tools/source_split.py --help`
   называет режим проверки носителей (имя не угадывать) — прогнать на копии дерева; красная проба: заменить файл в `verify` на пустую оболочку и
   убедиться, что проверка носителей это называет (если не называет — это расширение пункта 3).
2. `ai-packages/qa-factory/scripts/tests/test-layers.json`: `design/state-exits.md:112` → `:120` в трёх строках `named_by` и в `why` (строка 3671),
   после чтения `design/state-exits.md:118-121`. Остальные `named_by` с наследованным номером строки для файлов, чья резка шла инструментом
   (`test_infra_failure_*`, `test_no_move_seam_*`, `test_story_run_freshness_*`, `test_story_run_loop_b_*`, `test_controller_rework_*`):
   перечислить по `git show a8a9fb4 -- ai-packages/qa-factory/scripts/tests/test-layers.json` и по каждому открыть указанную строку и сверить текст
   (результат — таблица «строка: верно / исправлено / не определено» в отчёте узла).
3. Класс (designer → builder → critic): `tools/test_split.py` (`split-keep`) пишет в наследуемый `named_by` ссылку БЕЗ номера строки
   (`design/state-exits.md`), а номер — только если сверка по якорю-тексту строки `why` его подтверждает; тест `tools/test_test_split.py`:
   таблица — `named_by` с номером (наследуется без номера) / без номера (как есть) / ссылка на несуществующий файл (отказ). Читателей
   `named_by` проверить командой `grep -rn "named_by" tools ai-packages` до правки: формат поля не ломает читателей.

Края: пустой `named_by` — как есть; ссылка на файл вне репозитория — отказ с текстом (FR-1); оболочка, которая только импортирует части,
остаётся в `verify` носителя лишь с комментарием «shim».

Исполнитель: пункты 1–2 — builder; пункт 3 — designer → builder → critic.

## Связи

`../../onboarding-forge/findings/20261027-a19-nad-realnym-paketom-tolko-v-install-smoke.md` (другой класс, но тот же «носитель»); критик-вердикты
TD-11: `docs/tasks/specs/reviews/t-079-td11-p1-2-cut.md`; ось 13 карты `docs/SIBLING_MAP.md` (driver-layers).

Принципы и правила: P31; AR-19, AR-22; FR-37, FR-54.

Решение владельца нужно: нет.

<!-- id выдаёт интегратор при сборке пачки. -->
