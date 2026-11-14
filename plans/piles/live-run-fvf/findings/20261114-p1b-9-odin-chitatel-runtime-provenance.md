# Три читателя `evidence/runtime-provenance-*.json` берут «последний по имени» файл любого профиля: один читатель-выживший (очередь L-2 плана P1B-9)

id: — | кучка: `live-run-fvf` | от: план-критик P1B-9 (`docs/tasks/specs/reviews/20261114-p1b-9-plan-critic.md`, K2 строки 1-2, K5 «AR-13», строка очереди L-2 — посылка уточнена критиком) | приоритет: П2 | кандидат наверх: нет

## Что не так

Класс фабрики: **один факт читают несколько glob-читателей без функции-читателя (AR-13)**. Не «самый новый запись любого профиля/окна», как в спеке, а «последняя по имени»: имя файла
`runtime-provenance-<профиль>-<метка>.json` сортируется сначала по профилю, потом по метке (`sorted_paths`), поэтому «последний» может быть чужой профиль (блокер B1 критика P1B-9).
Читатели на `main`: `ai-packages/qa-factory/scripts/handoff_check.py::_runtime_provenance` (~514-515), `ai-packages/qa-factory/scripts/driver_dispatch.py` (`walk_run_values`, ~1580/1589) и
`ai-packages/qa-factory/scripts/coverage_contract.py` (~724-730, функция называет `profile_id`; фильтр по профилю есть). Измеритель вне пакета `experiments/measurers/check_all_contracts.py:285-290` читает те же файлы — отдельная находка forge.

## Что именно менять

Выбранное направление: ОДНА функция-читатель, три места её зовут; направление ошибки — «не называть чужую запись» (неизвестное, FR-59, а не последняя по имени).

1. `ai-packages/qa-factory/scripts/coverage_contract.py`: уже читает по профилю — оставить носителем; новая функция `provenance_record(task_root, profile_id) -> dict | None` — все записи профиля, выбор по метке записи
   (`stamp`), а не по имени; нет записи / профиль не назван / неразбираемый файл — `None` и причина (FR-41).
2. `handoff_check.py::_runtime_provenance` и `driver_dispatch.py::walk_run_values` зовут её с профилем строки/окна; профиль не известен — «unknown», не последний по имени.
3. Тесты — строки таблицы в `ai-packages/qa-factory/scripts/tests/test_handoff.py` и `ai-packages/qa-factory/scripts/tests/test_coverage_contract.py` (keep, быстрые): две записи двух профилей, чужой профиль «новее» по имени — читается свой профиль;
   записей нет; профиль не назван; неразбираемый файл рядом — пропущен, остальные читаются.
4. Согласовать с карточкой B1 плана P1B-9: если B1 строит читателя раньше — этот узел становится «перевести остальных», а не «построить».

Принципы и правила: AR-13, AR-28; FR-54, FR-59.

Связи: `findings/20261114-p1b-9-handoff-check-pustye-ishody-polej-s5.md` (тот же файл `handoff_check.py`, другие функции).

Решение владельца нужно: нет.

## Поправка вердикта P1B-9 (Q-2)

Источник: критик темы P1B-9 (`docs/tasks/specs/reviews/20261114-p1b-9-topic-diff-critic.md`, «Queue lines», Q-2). После C3 пункты 1-2 выше («новая функция `provenance_record`» и перевод `handoff_check._runtime_provenance`) — второй читатель того же факта (AR-13, P31).
Узел сужен до L-2 ровно: `driver_dispatch.walk_run_values` привязывает `evidence_refs[0]` стартовой пробы через хвостовой разрешитель, ВЫНЕСЕННЫЙ из `handoff_check.window_runtime_record` (одна функция, два зовущих); `handoff_check.py` из «Пишет в» убран. C1 сделал L-2 срочнее: файлы A3/A5 теперь сортируются среди последних имён.
