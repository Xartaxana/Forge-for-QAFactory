# Две другие дороги reopen (`release`, `rework --reason`) перезапускают никогда не стартовавшую работу закрытой истории без вопроса

id: — | кучка: `driver-hosts` | от: Lead, 21.10 (приёмка C1-6a, t-699 §12 Q2) | приоритет: П2 | кандидат наверх: нет

Что не так / что сделать: C1-6a закрыл дорогу `next` → `relaunch`: на закрытой истории never-started диспатч стал
`held`, и его перезапуск идёт только через `reopen_story` со словами человека (AR-20: `held` убывает только через
`reopen_story` / `leave_unlaunched`). Две другие дороги reopen остались как были: `controller.py --operation release
--dispatch <id>` и `rework --reason <слова>` по-прежнему перезапускают never-started rework-диспатч завершённой стадии
(класс C:4370) без вопроса и без записи, какую именно работу человек покрыл своим словом; `release_dispatch` вдобавок
обходит `validate`. Сделать: обе дороги проходят через тот же `_reopen_stamp` и ту же запись «что покрыто / что
оставлено» (`reopen_covers` / `reopen_left_held`), что и `reopen_story`; `release_dispatch` — через `validate`. Инвариант
узла C1-6a держится: слово человека о reopen покрывает ровно то, что назвал вопрос. Узел — C1-6a′ или пачка 3 (C3),
один исполнитель; пин в `test_story_closed.py` рядом с `a_partial_reopen_keeps_a_door_for_the_work_it_left`.

Свидетель: `docs/tasks/specs/t-699-c1-6-s6-s9-delivery.md` §12 Q2 (решение «не расширять здесь — находка при слиянии»);
`ai-packages/qa-factory/scripts/controller.py` — `release_dispatch` (коммит `release` без `validate`), `relaunch_candidates`,
`_held_work_refusal`; обзор критика `docs/tasks/specs/reviews/t-1182-t-1115-c1-6a.md` (B1 — частичный reopen терял held-вопрос;
закрыто фикс-раундом t-1188, 016060e3). Негативная проверка: на слитом дереве `grep -n "_reopen_stamp" scripts/controller.py`
находит только `reopen_story`'s вызов (контроль: та же команда находит `def _reopen_stamp`).

Принципы и правила: P22, P13; FR-9, FR-40, FR-59; AR-20, AR-25; D-0039.

Решение владельца нужно: нет (техническое; подсвечено в ответе 21.10).
