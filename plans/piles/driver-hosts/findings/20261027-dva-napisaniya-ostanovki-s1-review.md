# Две записи остановки S1 «Source review» в `s1.md`: `pause --reason "source review"` и `checkpoint --reason "source review awaiting the person"`

id: — | кучка: `driver-hosts` | от: спека t-1351 (FB-4), 27.10.2026 | приоритет: П3 | кандидат наверх: нет

Что не так / что сделать: `skills/qa-story/phases/s1.md` в разделе «Source review» остановку первого диспатча скаута описывает через `controller.py --operation checkpoint --status blocked --reason "source review awaiting the person"`, а в разделе «Boundary and judge» — через `story_step.py pause ... --reason "source review"`. Две записи одного события дают два разных ключа идемпотентности и разные тексты причины. Что сделать: оставить одну запись (та же команда на обоих местах), ключ-тест на совпадение причины в `s1.md`. Правка рядом с узлом FB-4, но вне его owns.

Свидетель: `docs/tasks/specs/t-1351-fb4-checkpoint-retired-on-resume.md`, §0 (skill road) и §6 (non-goals).

Принципы и правила: FR-54, AR-15, AR-19.

Решение владельца нужно: нет.
