# Слово «resume» в отказах повтора означает повтор, а после узла FB-4 — другое действие

id: — | кучка: `driver-hosts` | от: спека t-1351 (FB-4), 27.10.2026 | приоритет: П3 | кандидат наверх: нет

Что не так / что сделать: отказ повтора «only a checkpointed dispatch can be resumed» и текст `relaunch_of` «to resume a stopped role use its retry packet» называют повтором (новый диспатч, другой агент) слово «resume». После узла FB-4 `resume` — отдельная операция (тот же агент продолжает). Две вещи под одним словом ведут к неверной двери. Что сделать: в этих двух текстах заменить слово на «retry» / «continue with the retry packet», тест на текст каждого отказа (`controller.py`, `Controller.validate`).

Свидетель: `docs/tasks/specs/t-1351-fb4-checkpoint-retired-on-resume.md`, §6 (non-goals).

Принципы и правила: FR-1, FR-2, AR-9.

Решение владельца нужно: нет.
