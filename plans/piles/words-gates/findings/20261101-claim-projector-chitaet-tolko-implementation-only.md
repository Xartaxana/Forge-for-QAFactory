# `claim_projector.py` (`_post_build`, проверка `R-d`) читает множество `implementation_only`, которое F-4 критика S2 признаёт узким

id: — | кучка: `words-gates` | от: критик диффа S2 релиза 0.10.8 (`docs/tasks/specs/reviews/t-574-s2-critic.md`, F-4), строки `claim_projector.py` найдены 01.11.2026 | приоритет: П2 | кандидат наверх: нет

Что не так: F-4 критика S2: `validate_artifacts.check_behaviour_claims` обходит только `C.implementation_only(text)`, а требования с источником `current-code:` без пары в матрице (`code_sourced_requirements` при `created` не раньше `UNCONFIRMED_SOURCE_CUTOFF`) остаются без строки в `## Behaviour claims` и без вопроса: S2 закрывается, спросить некому (AR-23, AR-25, FR-42). Исправление F-4 внесено: множество «кто должен строку» теперь одна функция `contract.claim_required_requirements` (`contract.py:1231`), её зовёт `validate_artifacts.py:596` (прочитано на `1afda33f`). Тот же узкий читатель стоит ещё в двух местах `claim_projector.py`, которые правка F-4 не тронула: `_post_build` (строка 597: `only = set(C.implementation_only(text))`) и обход строк в проверке дороги `R-d` (строка 732: `only, asked, seen = set(C.implementation_only(text)), …`). После правки F-4 проектор не прочитает назад строку, которую требование `current-code:` теперь обязано иметь: `_post_build` скажет, что `R` «не implementation-only», а проверка `R-d` пропустит или ложно отвергнет её (по чтению; не прогонялось — это первое, что делает узел).

Что именно менять: `ai-packages/qa-factory/scripts/claim_projector.py`, функции `_post_build` и проверка `R-d` (строки около 597 и 732 на `1afda33f`): брать множество «кто должен строку» из `contract.claim_required_requirements`, а не из `implementation_only` (AR-13: одна функция). Сначала проба: реестр `created: 2026-10-31`, R-1 `derived`, `ac_ref -`, `current-code:`, строка в Behaviour claims от проектора — прочесть назад обоими местами, записать результат в узле. Тест: `scripts/tests/test_claim_projector.py` — для `code_sourced_requirement` проектор строит строку, читает её назад без проблемы; для требования, которому строка не положена, — как раньше; реестр до отсечки — как раньше.

Свидетель: `docs/tasks/specs/reviews/t-574-s2-critic.md` F-4 (проба и исправление); `ai-packages/qa-factory/scripts/claim_projector.py:597`, `:732`; `ai-packages/qa-factory/scripts/contract.py:1231`; `ai-packages/qa-factory/scripts/validate_artifacts.py:596`.

Принципы и правила: P20, P23; FR-42; AR-13, AR-19, AR-22, AR-23, AR-25.

Решение владельца нужно: нет.
