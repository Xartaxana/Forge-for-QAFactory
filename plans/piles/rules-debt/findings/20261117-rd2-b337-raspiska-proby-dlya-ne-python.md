# B-337: `red_sandbox.py --probe` для языка без строки пробы отвечает `incomplete` и не оставляет расписки

id: — | кучка: `rules-debt` | от: спека карточек фазы 2 (`docs/tasks/specs/20261117-rules-debt-phase2-cards-spec.md`), 17.11.2026 | приоритет: П1 | кандидат наверх: нет

Что не так / что сделать: Результат C4 (t-961, 17.11.2026): для суффикса без строки пробы (`.kt`), команды не-pytest и отчёта junit-xml `red_sandbox.py --probe` отвечает `incomplete` («assertion site of a junit-xml/python report is not read yet (B-337)») и не публикует расписку, поэтому `proof_level.reached` нечего считать; команда с именем pytest не выбирает не-.py тест (`node_ids` хранит только .py). Причина по чтению билдера (Lead не перепроверял): `red_sandbox._frame_grammar` возвращает {} для суффикса без строки, `reporters.assertion_site` даёт `site_unread`. Класс: дорога роли обязана быть рабочей на языке без строки (FR-2, FR-57; AR-1).

Что именно менять: Дизайнер устанавливает, где читается место утверждения отчёта junit-xml для суффикса без строки, и как расписка «проверка живая» доходит до `proof_level.reached`; красная строка C4 (`test_probe_by_code.py`) входит вместе с починкой (красная-до). Отчёт билдера t-961: `docs/tasks/handoffs/t-961-rules-debt-c4.md` на ветке `worktree-agent-a72a37ff6d6ddc10a` (коммит `dd27d27e`). Живое доказательство B-373 уже записано как LR1-1 в `live-runs/2`.

Карточка: `docs/tasks/specs/20261117-rules-debt-phase2-cards-spec.md`, карточка раздел «C4 result (t-961…)» — читать там, не копировать сюда.

Свидетель: спека, раздел «C4 result (t-961…)»; отчёт `docs/tasks/handoffs/t-961-rules-debt-c4.md`.

Принципы и правила: FR-2, FR-57, FR-18; AR-1, AR-28; P2.

Решение владельца нужно: нет.
