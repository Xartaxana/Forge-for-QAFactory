# Поле `owner` в `delivery-verdict-kinds.json` объявлено и проверяется, но в проде его не читает никто

id: — | кучка: `execution-report` | от: критик t-711 (RD1-4, m-4), t-745/m-9 и t-758 (RD1-4, m-1), 02.11.2026 | приоритет: П3 | кандидат наверх: нет

## Что наблюдалось

Носитель — `ai-packages/qa-factory/references/delivery-verdict-kinds.json` (46 видов; измерение на дереве релиза: `product` 25, `factory` 13, `environment` 7, `review` 1) и `scripts/delivery_verdict.py:63` (проверка поля).

- Читатель `delivery_verdict.owner_of_kind` (`:113`): `grep -rn owner_of_kind ai-packages/qa-factory --include=*.py` находит определение и четыре вызова ТОЛЬКО в тестах (`test_check_delivery.py:530`, `test_mixed_then_outcomes.py:693/695`, `test_third_verdict.py:1034`, `test_triage_control.py:329`); в производственном коде вызова нет.
- Владельца причины в проде считает `check_delivery.assess` (`:2246-2252`) по ТЕКСТУ причины через `reason_record`/`reason_owner`; вид кладётся рядом и не читается как владелец.
- Поле вольно расходиться с текстом: так было у `env_undecided` (вид — `environment`, текст — `product`; починено RD1-4) и есть у `factory_record` против `manifest: … unresolved`.
- Билдер t-745 (RN1-9) добавил в таблицу виды с `owner`, не читаемым никем (m-9): видимость AR-27 держится на этой находке.
- Враждебный вход из RD1-4 (m-1): суффикс B-361 несёт дословный `ran red: <причина прогона>`, а `_owner_decided` гонит `FACTORY_BOOKKEEPING_PHRASES` и `LEDGER_STATE_IN_REASON` по ВСЕМУ тексту раньше семейства: ``… (ran red: status is `failed:APP_BUG` got 500)`` → владелец `product`, «stale case link in fixture» → `factory`, простой текст AssertionError → `environment`. Вид (`environment`) и текст расходятся.

## Класс

Объявление без читателя и без проверки согласия с реальным читателем (AR-13, AR-22): два места говорят «чья причина», тест видит только одно.

## Что именно менять

Направление выбрано (Lead пачки release-next/1, 02.11.2026): СНАЧАЛА замер, потом решение — узел начинается с замера и не пишет код до его результата.

1. Замер (builder, отчёт в `docs/tasks/specs/reports/`): для каждого `reason_records` записи фикстурных историй (`scripts/tests/fixtures/`, истории 12586/14857/LOCAL-1, если есть) — владелец по тексту (`check_delivery.reason_record`) против `owner_of_kind(kind)`; исключить записи с делом в `factory_refs` (устаревший стендовый ряд законно `factory`, §3.2a t-701) и поднятые кейсом. Таблица «вид → совпало / разошлось → пример».
2. Решение по замеру (Lead): (а) поле удалить из файла и из проверки `delivery_verdict.py:63`; либо (б) ключ согласия `scripts/tests/test_delivery_owner_agreement.py` на всю таблицу: для каждого вида пример причины даёт тот же владелец текстом и видом, расхождение — красная строка с именем вида. По умолчанию, если расхождений ≤ 3 — (б).
3. Враждебные входы m-1 пойдут в тот же тест: три строки суффикса выше → ожидание «владелец по семейству `blocked on the stand:` — `environment`, текст после `ran red:` владельца не меняет». Если ожидание требует правки `_owner_decided`, правка — узел RD2-3 (`report-delivery/2`) или здесь, но в одной функции `check_delivery._owner_decided`.

## Принципы и правила

FR-19, FR-41; AR-13, AR-22, AR-27.

## Связи

- `docs/tasks/specs/reviews/t-711-rd1-4-plan-critic.md` (m-4); `docs/tasks/specs/reviews/t-758-rd1-4-diff-critic.md` (m-1); `docs/tasks/handoffs/t-745-rn1-9-b2.md` (m-9).

Решение владельца нужно: нет.
