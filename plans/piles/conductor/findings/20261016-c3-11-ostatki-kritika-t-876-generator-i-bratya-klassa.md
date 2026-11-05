# C3-11, остатки критика t-876 и билдера t-871: генератор карты блоков без строк `BY_SEGMENT` для `(ValueError, issue)` / `(StateConflict, issue)` (шесть циклов по ссылкам и строка `prepare` карты) и братья класса K1 вне контроллера

id: — | кучка: `conductor` | от: критик t-876 (F-4, F-6) и билдер t-871 (Q1), записал Lead 16.10.2026 08:2x | приоритет: П3 | кандидат наверх: нет

## Что

1. **Генератор `tools/controller-blocks-gen.py`** (Q1 билдера t-871, F-4 критика): шесть циклов проверки по ссылкам (reconcile,
   request_cancel, accept + unresolved reason, policy, code_only, Gate A carry) ловят `(ValueError, issue)` / `(StateConflict,
   issue)`, а в `BY_SEGMENT` таких маршрутов нет — карта `design/controller-blocks.md` не знает их формы, и строка `prepare`
   потеряла своё объяснение после C3-11. Что сделать: две строки `BY_SEGMENT` в генераторе (тест генератора на них), карта
   перегенерирована, затем шесть циклов переводятся на `_raise_all` по правилу C3-11 (независимые проверки одного класса — вместе;
   зависимые — `_noted`).
2. **Братья класса K1 вне `controller.py`** (F-6 критика; аналоги билдера): `session_handoff.validate_takeover`,
   `worker_lifecycle.cancellation`, `contract.validate_record`; по grep — `gate_preflight.py:3726`, `stand_gaps.py:352`. Первый ход
   — та же перепись с вердиктом на цепочку (C / D / M / X / 1), затем перевод подтверждённых; строка оси 17 SIBLING_MAP «отказы
   по одному → вместе» получает этих потребителей.

## Куда

Строки C4-4 и C4-5 пачки `conductor/batch-4-vhodyashchie-2.md` (D-0044).
