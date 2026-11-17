# id строк §5.3 25-31 на `stage_guard` и `hooklib`; перепись единиц G-dispatch

id: — | кучка: `told-before-work` | от: спека «Told before work: finish» (`docs/tasks/specs/20261117-told-before-work-finish-spec.md`), 17.11.2026 | приоритет: П1 | кандидат наверх: нет

Что не так / что сделать: Класс: требование названо в строке, отказ его id не несёт; единицы, до которых не доходит ни одна строка роли, числятся за ролью (AR-9, AR-20).

Что именно менять: `stage_guard.py`: ролевые `deny` → `refusal("stage_guard:SG-…", …)` для строк 25-30 (строка 28 — два подидентификатора `commit.pathspec`/`commit.manifest`; 31 — указатель без своего сайта); первым — вариант FV1-27 с обратной косой чертой в `hooklib` (строка 25). Перепись `judgment-census.json`: единицы G-dispatch (`stage_guard`, `inject_context`, `native_context`, `codex_roles`) → `roles: ["conductor"]` с `note` «dispatch-time unit: no role's tool line reaches it». Потолки `blocking_per_role` только вниз; требование поднять — STOP (AR-20). Перепись сливается первой (порядок T4b → T7f → T9c → T9a). Тест — `tbw_t4b_sites`.

Карточка: `docs/tasks/specs/20261117-told-before-work-finish-spec.md`, карточка §6 «Card T4b» — читать там, не копировать сюда.

Свидетель: спека §5.3 строки 25-31; G-dispatch (механизм-спека :509-512).

Принципы и правила: AR-9, AR-13, AR-18, AR-20, AR-29.

Решение владельца нужно: нет.
