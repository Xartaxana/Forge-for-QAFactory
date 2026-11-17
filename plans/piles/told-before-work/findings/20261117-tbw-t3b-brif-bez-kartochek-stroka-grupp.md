# Бриф без карточек, строка групп в промпте, `first_look:put`

id: — | кучка: `told-before-work` | от: спека «Told before work: finish» (`docs/tasks/specs/20261117-told-before-work-finish-spec.md`), 17.11.2026 | приоритет: П1 | кандидат наверх: нет

Что не так / что сделать: Класс: карточки правил идут и страницей, и брифом (две дороги одного требования); `first_look.put` не несёт id строк (AR-10, AR-13, AR-15).

Что именно менять: `brief_pack.py`: `ahead_card` и секция удаляются, `FIRST_LOOK_AHEAD` удалён, `FIRST_LOOK_DOD` — первое предложение, новая `dispatch_groups`, строка в брифе; `window_record.py` — новая `row_field_lines`; `story_step._prompt`/`_card_text`; `first_look.put` — 11 id `first_look:put.*`. Исход опыта M9 выбирает вид; нечитаемый факт диспатча — ни один из исключающих членов и текст «could not tell». До T1r-cards карточка стоит на странице, потеря брифа ничего не отнимает. Строки в `test_first_look.py`, `test_brief_pack.py` (медленный: канон). Пилотные узлы `first_look.py` (FV2-54/57) и `brief_pack.py` (FV2-56/58) — по функциям, при работе `очередь:`.

Карточка: `docs/tasks/specs/20261117-told-before-work-finish-spec.md`, карточка §6 «Card T3b» — читать там, не копировать сюда.

Свидетель: спека механизма T3b (a)-(e), §2.2, §2.4, §2.6.

Принципы и правила: AR-10, AR-13, AR-15, AR-29.

Решение владельца нужно: нет.
