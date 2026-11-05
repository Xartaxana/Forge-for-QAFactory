# `story_step.pause` и `finish` строят заявки без `owner_session_id`

id: — | кучка: `driver-hosts` | от: спека t-1351 (FB-4), критик t-1354 F4, 27.10.2026 | приоритет: П3 | кандидат наверх: нет

Что не так / что сделать: после `handoff` аренда оркестратора держит сессию; `Controller.build_checkpoint_request` копирует `leases.orchestrator` в `owner_session_id`, а `story_step.pause` и `finish` строят свои заявки без него, и `apply` может отказать им под арендой. В узле FB-4 `resume` копирует владельца (R1); аналоги `pause` / `finish` остались. Что сделать: тот же перенос владельца в заявки `pause` и `finish`, тест «под арендой после handoff».

Свидетель: `docs/tasks/specs/t-1351-fb4-checkpoint-retired-on-resume.md`, §6 (non-goals) и §11 (F4 критика); `docs/tasks/specs/reviews/t-1354-t-1351-plan-review.md`.

Принципы и правила: FR-42, AR-14, AR-25.

Решение владельца нужно: нет.
