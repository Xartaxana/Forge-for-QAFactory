# id 6 строк `controller:*` и перепись ролей возобновлённых единиц

id: — | кучка: `told-before-work` | от: спека «Told before work: finish» (`docs/tasks/specs/20261117-told-before-work-finish-spec.md`), 17.11.2026 | приоритет: П1 | кандидат наверх: нет

Что не так / что сделать: Класс: требование, которое роль встречает при возобновлении, названо в строках, отказы контроллера id не несут (AR-9, AR-10).

Что именно менять: `controller.py` (`_s3_completion_gate`, `_code_review_refusal`, `_s5_plan_accept_problems`, `_plan_rework_rows_problems`, `_plan_review_problems`): единицы переписываются на роли диспатча с `note`; `raise StateConflict(refusal("controller:<id>", <тот же текст>))`, текст побайтно прежний (маркер `REPAIR_MARKER` сохранён). У `_code_review_refusal` в переписи строки нет — добавить, названо. Не трогать `:7479`/`:7515`, `controller-blocks.md` остаётся неизменным. Перепись сливается последней в порядке T4b → T7f → T9c → T9a. Строки в `test_controller_doors.py`.

Карточка: `docs/tasks/specs/20261117-told-before-work-finish-spec.md`, карточка §6 «Card T9a» — читать там, не копировать сюда.

Свидетель: спека механизма §5.3a; M7 (mech :771).

Принципы и правила: AR-9, AR-10, AR-13, AR-29.

Решение владельца нужно: нет.
