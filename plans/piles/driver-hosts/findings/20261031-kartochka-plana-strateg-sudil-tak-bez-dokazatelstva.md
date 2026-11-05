# Карточка гейта A «e2e rows without a highest-risk field» говорит «The strategist judged them so», а предупреждение до стратега не доходит (t-542 F11)

id: — | кучка: `driver-hosts` | от: критик t-542, F11 (`docs/tasks/specs/reviews/t-542-gate-answers-critic.md`), t-525 §4; решение 31.10.2026 «GW1-29: оставить предупреждение (вариант б)», 31.10.2026 | приоритет: П3 | кандидат наверх: нет

## Что наблюдалось

- `gate_brief._tail_sections` (:2796–2805) печатает человеку: «`automate` at e2e-ui, as written or after an answer to a question, while `impact`, `likelihood` and `verification_depth` do not say highest risk. **The strategist
  judged them so**; this is no question to you …». Закреплено в `scripts/tests/test_gate_brief_and_retro.py:1509`.
- Докстринг `gate_brief.unearned_automation` (:387) прямо говорит обратное: `planning_contract.plan_warnings` «prints these at the S3 exit, where a passing detector's output reaches nobody». То есть на
  чистом проходе стратег предупреждения не видит и «судил» уровень, не зная об этом. Фраза — посылка без носителя (FR-41, FR-37), а вариант (б) GW1-29 (оставить предупреждение) принят владельцем 31.10.2026
  именно на этой посылке. Критик t-542 не проверял её отдельно («не проверено мной»).
- Класс: текст человеку заявляет факт о работе роли, которого код не устанавливает (FR-10, AR-22: поле без читателя).

## Что именно менять

1. Сначала замерить посылку (одна команда, результат записать в узел): прогнать S3-выход на фикстуре плана с `automate`/`e2e-ui` без поля риска и посмотреть, попадает ли строка `plan_warnings` в вывод, который
   читает роль-стратег (`planning_contract` последние строки выхода S3; `finish`). Если НЕ попадает (докстринг прав) — пункт 2; если попадает — пункт 3.
2. Не попадает: `gate_brief._tail_sections` (:2803–2805) заменяет «The strategist judged them so» на то, что верно: «The plan was not checked against this by the strategist; a critic of the plan reads
   the level» (без утверждения о суждении стратега), заголовок и остальной текст — как были. Пин `test_gate_brief_and_retro.py:1509` и хэш текста меняются в том же коммите.
3. Попадает: фраза остаётся, в карточку добавляется носитель (имя строки выхода S3, где стратег её видел), тест на этом носителе.
4. Тест: карточка не содержит фразу «judged them so», пока тест S3-выхода не доказывает, что стратег предупреждение получил (мутация: вернуть фразу — красит).

## Принципы и правила

P9, P20 (утверждение о поведении без носителя); FR-10, FR-37, FR-41; AR-22. Связи: GW1-29 (`docs/tasks/specs/reviews/t-542-gate-answers-critic.md` F9, F10), t-525 §4.

Решение владельца нужно: нет (вариант (б) принят 31.10.2026; здесь правится только текст).
