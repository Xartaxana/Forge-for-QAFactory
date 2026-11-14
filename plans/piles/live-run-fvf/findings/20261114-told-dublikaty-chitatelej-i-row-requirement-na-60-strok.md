# Перепись «told»: копии читателей (`role_set`, `measure_untold`, `_hand_cards`, чтение `own`) и `_row_requirement` на 61 строку с вложенной лямбдой

id: — | кучка: `live-run-fvf` | от: критик темы «told before work» T1, `docs/tasks/specs/reviews/20261113-tbw-t1-topic-code-critic.md` (строки очереди Q-d и Q-e); пачка выбрана по запасному правилу (кучки с узлами T1 нет), Lead может перенести | приоритет: П3 | кандидат наверх: нет

## Что не так

Класс фабрики: **копии одного читателя и переросток (AR-13, AR-15, FR-54)**. Строки — по ветке `wip/tbw-t1`, пути от `ai-packages/qa-factory/scripts/`:

- Q-d (1): `role_set` (`tests/test_stage_joints.py:736`) заново реализует `stage_joints._row_names` (`stage_joints.py:486-491`, `*` в сопоставленные роли, не правило дирижёра).
  Чинится вместе с F2 критика (K5 на реальном дереве всегда с пустыми `unit_rows`).
- Q-d (2): `measure_untold` (`tests/test_stage_joints.py:723-733`) — третья копия правила переключения `units_of` (функция ИЛИ строка в промежутках).
- Q-d (3): `_hand_cards` (`stage_joints.py:1017-1025`) — второй читатель `ahead-cards.json` рядом с `hooklib.load_ref_json` (`brief_pack.py:416`); ему нужен `(None, why)`, которого
  тот читатель не даёт.
- Q-d (4): `exit_members` (`stage_joints.py:145-158`) и `_passthrough` (`refusal_registry.py:1367-1408`) оба читают литерал `own`; обе копии предписаны спекой (§3.4, §3.5), поэтому это
  строка Lead для закрывающей волны, не вина сборщиков.
- Q-e: `_row_requirement` (`stage_joints.py:836-896`) — около 61 строки, 4 уровня вложенности (else, for, if, if); вложенная лямбда на `:890` прячет чтение `role_rules.load`.

## Что именно менять

1. `tests/test_stage_joints.py`: `role_set` вызывает `SJ._row_names`; `measure_untold` берёт правило переключения из одного места (из `units_of`, не копией).
2. `stage_joints.py`: `_hand_cards` читает через `hooklib.load_ref_json` либо общий читатель получает форму `(None, why)` — тот выбор, при котором остаётся один читатель
   `ahead-cards.json`; `_row_requirement` разрезан на по одной функции на поле строки, лямбда на `:890` заменена именованной функцией.
3. Пункт Q-d (4): решение Lead — оставить как предписано спекой или свести `exit_members` и `_passthrough` к одному читателю `own`; до решения не трогать.
4. Тест: существующие числа переписи и joints не двигаются; `_row_requirement` на каждом виде строки возвращает прежнее (таблица случаев по полям).

Принципы и правила: FR-54; AR-13, AR-15.

Решение владельца нужно: нет (пункт 3 — Lead пачки).
