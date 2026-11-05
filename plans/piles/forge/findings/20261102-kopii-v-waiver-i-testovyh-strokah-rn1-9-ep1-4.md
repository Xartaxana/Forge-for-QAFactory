# Три копии цикла штампов в `waiver.py` и три копии одной тестовой строки «передано человеку»

id: — | кучка: `forge` | от: критик t-764 (RN1-9, m-6), билдер t-767 и t-760 (EP1-4), 02.11.2026 | приоритет: П3 | кандидат наверх: нет

## Что наблюдалось

Носитель — `ai-packages/qa-factory/scripts/`:

- `waiver.py`: `run_revoke`, `run_remark`, `run` пишут один и тот же цикл «поставить поля на запись» (штамп `why_person`, `by`) три раза; `record_stage_overrides` уже принимает `fields`. Критик t-764 m-6: «queue acceptable». Билдер t-767 (K1) добавил дорогу `Driver.waiver_road`, и цикл стал третьим носителем штампа.
- Тесты: строка `HANDED_ROW` (запись манифеста «передано человеку») скопирована в `scripts/tests/test_acceptance_semantics.py:602`, `test_window_record.py` и локально в `test_story_run_loop_b.py` (билдер t-760 не импортировал первую: модуль создаёт временный каталог при импорте).

## Класс

Один и тот же кусок записи написан несколько раз там, где следующая правка поля обязана обойти каждую копию (FR-54; AR-13, AR-15): штамп без одного из циклов даст запись без класса, а строка теста с устаревшей формой даст зелёный тест на старой форме.

## Что именно менять

Направление выбрано (Lead пачки release-next/1, 02.11.2026).

1. `scripts/waiver.py`: `apply_waiver`, `apply_remark`, `apply_revoke` получают параметр `fields` (как `record_stage_overrides`), цикл штампа живёт в одной функции `_stamp(entry, fields)`; `run_revoke`, `run_remark`, `run` вызывают её. Ожидание: файл `pipeline.json` после каждой из трёх команд побайтно тот же, что до правки. Тест: `test_waiver_release.py` без правки ожиданий (714 проверок) + одна строка на каждый путь со `--why-person`.
2. Тесты: общая строка в `scripts/tests/story_step_common.py` (или `harness.py`) `handed_row(case, **fields)`; три места зовут её; ожидание — те же тесты зелёные без правки. Тест-страж: поиск литерала строки по `scripts/tests/` находит только общий помощник.
3. Не часть узла: `person_owned.as_class` уже единственный (t-767).

## Принципы и правила

FR-54; AR-13, AR-15.

## Связи

- `docs/tasks/specs/reviews/t-764-rn1-9-integration-critic.md` (m-6); `docs/tasks/handoffs/t-760-ep1-4-fix.md`; `docs/tasks/handoffs/t-767-rn1-9-fix.md`.

Решение владельца нужно: нет.
