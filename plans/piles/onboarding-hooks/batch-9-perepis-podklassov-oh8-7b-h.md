# Онбординг, установка, хуки и гард — пачка 9: перепись суждений классифицирует 190 функций, отказывающих только через подкласс (OH8-7b…h)

кучка: `onboarding-hooks` | статус: ожидает | взял: — | ветка: `pile/onboarding-hooks/batch-9` | MR: — | стенд: не нужен (CI) | приоритет: П3

Открыта 13.11.2026 (спека `docs/tasks/specs/t-346-oh8-7b-chain-spec.md`; решения Lead F1 (a), F3, F4 от 13.11.2026): хвост узла OH8-7 (t-321 часть B, вариант (d)+(c1)) — 190 функций в «pending» под `SUBCLASS_PENDING_CEILING`.

Правило готовности: пачка закрыта, когда каждый узел «принято», свидетели узлов — в журнале взявшего.

Решения владельца: нет (решения Lead 13.11.2026; развилки спеки t-346 §6 — у Lead).
Порядок: узлы строго один за другим (каждый переписывает `judgment-census.json`); критик — один проход на пару (b+c, d+e, f+g), OH8-7h — свой проход. Узел начинает с перезамера (спека §3.2) и останавливается вопросом при расхождении. OH8-7b и OH8-7h — коммиты механизма: коммитит Lead (строка `tier:`).
очередь: onboarding-hooks/8 → onboarding-hooks/9
Идентификаторы узлов OH9-1..OH9-7 — это OH8-7b..OH8-7h спеки docs/tasks/specs/t-346-oh8-7b-chain-spec.md; OH9-8 — узел находки про форму гейта.
Скоуп свидетеля: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <пути узла>`; BATCH CANON — CI интегратора.

## Бриф

Что сделать: семь узлов по спеке t-346 — каждый добавляет свои файлы в `SUBCLASS_UNIT_FILES`, пишет строки переписи по каждой функции (класс, роли, владелец), опускает `SUBCLASS_PENDING_CEILING` ровно на своё число и называет каждый подъём храповика построчно; OH8-7h убирает обе константы. НЕ делать: править скрипты пакета (они только читаются), `refusal_registry.py`, `tools/architecture_gate.py`, `MEANING_CEILING`; понижать класс или добавлять `blocks_override` существующим строкам; угадывать класс вне `shape`/`xref` — это вопрос (спека §4.3).

## Узлы

Исполнитель «builder → critic» — кодовый узел по готовой спеке. Статусы: `ожидает` → `в работе` → `сдано` → `принято` / `отклонено`.

| Узел | Приоритет | Что | Исполнитель | Пишет в | Зависит от | Статус |
|---|---|---|---|---|---|---|
| OH9-1 | П3 | **OH8-7b.** Механизм `SUBCLASS_UNIT_FILES` (спека t-346 §2, §3.4) + первые 23 функции scripts/probe_by_code.py (строки 217–2902, записями `файл::функция`; скрипт только читается). Потолок 190 → 167. Тест: строки `SUBCLASS_ROWS` со столбцом `unit_files`, таблица C7 (дубль, устаревшая запись); C1/C7/C3 зелёные. Списки вопросов 9 и 11 брифа критика получают обе константы. Коммит механизма — Lead | builder → critic (пара 1) | `scripts/tests/test_judgment_census.py`, `scripts/tests/fixtures/judgment-census.json`, `docs/SIBLING_MAP.md` (оси 18, 34), `docs/tasks/critic-diff-brief.md` (вопросы 9, 11) | OH8-7 | ожидает |
| OH9-2 | П3 | **OH8-7c.** Остальные 23 функции scripts/probe_by_code.py (строки 3738–8309; скрипт только читается); 23 записи заменяются записью файла. Потолок 167 → 144. Тест: C1/C7/C3 | builder → critic (пара 1) | `scripts/tests/test_judgment_census.py`, `scripts/tests/fixtures/judgment-census.json` | OH9-1 | ожидает |
| OH9-3 | П3 | **OH8-7d.** 38 функций (скрипты только читаются): execution_request (14), environment_preparation (10), execution_scheduler (4), managed_dependency (1), run_suite (3), red_sandbox (6). Потолок 144 → 106. Тест: C1/C7/C3 | builder → critic (пара 2) | `scripts/tests/test_judgment_census.py`, `scripts/tests/fixtures/judgment-census.json` | OH9-2 | ожидает |
| OH9-4 | П3 | **OH8-7e.** 32 функции (скрипты только читаются): exploration (11), explore_step (1), manual_evidence (3), manual_capture (2), import_test_receipt (7), s7_reorder (8). Потолок 106 → 74. Тест: C1/C7/C3 | builder → critic (пара 2) | `scripts/tests/test_judgment_census.py`, `scripts/tests/fixtures/judgment-census.json` | OH9-3 | ожидает |
| OH9-5 | П3 | **OH8-7f.** 24 функции (скрипты только читаются): ticket_light (7), ticket_adapter (1), source_inventory (2), source_exclusions (2), vcs_evidence (4), local_keys (2), onboard_apply (6). Потолок 74 → 50. Тест: C1/C7/C3 | builder → critic (пара 3) | `scripts/tests/test_judgment_census.py`, `scripts/tests/fixtures/judgment-census.json` | OH9-4 | ожидает |
| OH9-6 | П3 | **OH8-7g.** 29 функций (скрипты только читаются): s5_plan (6), question_register (6), question_stop (3), person_words (2), grammar (3), assertion_detectors (5), machine_facts (3), driver_dispatch (1). Потолок 50 → 21. Тест: C1/C7/C3 | builder → critic (пара 3) | `scripts/tests/test_judgment_census.py`, `scripts/tests/fixtures/judgment-census.json` | OH9-5 | ожидает |
| OH9-7 | П3 | **OH8-7h.** 21 функция (скрипты только читаются): hooklib (4), controller (1), story_step (1), event_store (2), retro_numbers (1), host_adapter (1), role_load (6), release_fingerprint (2), selftest (2), config_view (1); потолок 21 → 0, затем тем же коммитом удаляются `SUBCLASS_UNIT_FILES`, `SUBCLASS_PENDING_CEILING`, C7 и ветка pending; тексты слепого пятна, `about`, оси 18/34 и списки вопросов 9/11 брифа критика переписаны (спека §3.5). Коммит механизма — Lead. Тест: C1/C3 зелёные, `neutral_only` создаёт единицу | builder → critic (свой проход) | `scripts/tests/test_judgment_census.py`, `scripts/tests/fixtures/judgment-census.json`, `docs/SIBLING_MAP.md` (оси 18, 34), `docs/tasks/critic-diff-brief.md` (вопросы 9, 11) | OH9-6 | ожидает |
| OH9-8 | П3 | **OH8-7i.** Находка `findings/20261113-gate-form-for-blocks-override-on-non-refusing-units.md`: у `tools/architecture_gate.py` нет формы для «`blocks_override` на единице, которая никого не отказывает»; после появления формы каждая строка переписи с пометкой `E3:` получает `blocks_override: false`, потолки опускаются ровно на их число. Тест: grep `"note": "E3:` по данным переписи ничего не находит | Lead (механизм) → builder | `tools/architecture_gate.py`, тест шлюза в `tools/`, `ai-packages/qa-factory/scripts/tests/fixtures/judgment-census.json` | OH9-7 | ожидает |

## Ход

Журнал передачи Lead пачки, новые записи в конец: `<дата время> — <что сделано, диспатчи t-nnn, хэши>`.

- 13.11 — пачка открыта по спеке t-346 (D-0044); не взята

## Живые доказательства

| Что | Стенд / проект | Кто | Статус |
|---|---|---|---|

## Остатки

<!--
Пачка закрывается доделкой, не переносом (слово владельца 08.10.2026): `close` отказывает, пока в этом разделе есть
пункт, у которого нет одной из двух форм (ключи в нижнем регистре, пары `ключ: значение` через ` | `, текст впереди):
  - <что осталось> | сделано: <хэш 7-40 hex | t-nnn>
  - <что осталось> | перенос: <findings/<файл> | пачка N | <кучка>/findings/<файл>> | обоснование: <почему> | подтвердил: <кто, дата>
Пустой раздел — можно закрывать.
-->
