# Отказы контроллера называют дверь `--operation recover`, когда она не печатает пакета (мёртвая дверь), и фраза двери написана тремя способами

id: — | кучка: `onboarding-forge` | от: критик переисследования пачки 2, `docs/tasks/specs/reviews/t-161-batch2-rereview.md` (N1 и строка «Standing questions»; задача t-163, поток hot, узел H4 критика `docs/tasks/specs/reviews/t-147-of2-batch-critic.md`), 12.11.2026 | приоритет: П2 | кандидат наверх: нет

Правки H3/H4 потока hot — на ветке `wip/of-hot` (коммит 0013879), в main нет; номера строк ниже — по main, у критика сдвинуты.

## Что наблюдалось

1. `scripts/controller.py` (main) `accept` остановленного диспетчера, ~:5767-5775: отказ говорит «`--operation recover` prints the ready packet» без условия. `retry_packets` пропускает остановку `BUDGET_EXHAUSTED` и диспетчер с более поздней записью той же стадии и роли — для них названная дверь мёртвая (FR-2).
2. `scripts/controller.py` ~:5701, отказ `relaunch_of`: «to resume a stopped role use its retry packet (`--operation recover` prints it)» — тот же пробел.
3. Фраза двери записана тремя способами рядом с «единственной» `_recover_words`/`incomplete_words`: :5701, :5771 и ~:9632 (по критику; «operation recover» в `controller.py`, 8 мест, все прочитаны) — формулировки не совпадают (H4 нашёл третье написание в `_resume_stop_problems`).

## Что именно менять

1. `scripts/controller.py`: оба отказа (1, 2) идут через выбор двери `_incomplete_problem`, обобщённый на остановленные статусы: `retry_packets` называет диспетчер → «recover»; остановка по бюджету стори → `_budget_words`; иначе → `next`.
2. Три места фразы двери (:5701, :5771, ~:9632) строятся из одной `_recover_words` (одно написание, AR-15), без изменения смысла там, где дверь живая.
3. Тест: `scripts/tests/test_resume_stopped.py` (где живёт H3) — таблица «остановка по бюджету / диспетчер с более поздней записью / обычная остановка» × «accept / relaunch_of»: названная дверь есть в выводе и работает (одно из: пакет, `_budget_words`, `next`). Мёртвая дверь в выводе — красная строка.

Зависит от слияния потока hot (`wip/of-hot`) в ветку пачки. Принципы и правила: FR-2, FR-57; AR-9, AR-15.

Решение владельца нужно: нет.
