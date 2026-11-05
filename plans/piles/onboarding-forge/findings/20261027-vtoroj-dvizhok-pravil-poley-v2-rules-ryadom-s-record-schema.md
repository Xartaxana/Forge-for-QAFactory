# Второй движок правил полей: `V2_RULES` рядом с `record_schema`

id: — | кучка: `onboarding-forge` | от: end-критик t-1398, очередь Q3 (ответ 3), 27.10.2026 | приоритет: П3 | кандидат наверх: нет

Что не так / что сделать: `V2_RULES` + `v2_discovery_problems` (`scripts/context_bundle.py` :222-313) — движок правил полей рядом с `record_schema._problems` (`record_schema.py:17`), который уже собирает проблемы с локаторами и умеет required / enum / minLength / items; `references/record-schemas.json:424-441` уже объявляет те же три раздела (items только `type: object`). Спека выбрала константу осознанно; сведение — решение одного носителя для пакета §7 (`scripts/field_cards.py`): либо правила v2 переезжают в `record-schemas.json` и читаются `record_schema`, либо генератор берёт `V2_RULES` носителем, а схема на эти разделы ссылается. Решить в плане SC2-23 до кода (критик на план), не строить третий вариант.

Свидетель: `docs/tasks/specs/reviews/t-1398-vc-end-review.md`, ответ 3 и Q3.

Принципы и правила: FR-13, AR-1, AR-13, AR-15, AR-18.

Решение владельца нужно: нет.

Связи: t-1398 Q3, t-1355 §7; парная находка про рендереры — `20261027-vstroennye-renderery-zakrytyh-spiskov-v-zatronutyh-faylah.md` (Q4, тот же носитель §7).
