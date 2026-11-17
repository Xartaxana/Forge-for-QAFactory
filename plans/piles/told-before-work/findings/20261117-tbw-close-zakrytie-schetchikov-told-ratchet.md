# Закрытие: счётчики `told_ratchet` и `told-ratchet.json` по замеру, мёртвый код карточек

id: — | кучка: `told-before-work` | от: спека «Told before work: finish» (`docs/tasks/specs/20261117-told-before-work-finish-spec.md`), 17.11.2026 | приоритет: П1 | кандидат наверх: нет

Что не так / что сделать: Класс: пока узлы одного замысла сливаются, счётчики и пин K12 стоят на промежуточных значениях; мёртвый код карточек (`ahead_card`, `CARD_GROUP`, `NOT_YET_HEAD`) остаётся до `hand_cards` 0.

Что именно менять: `stage_joints.py --check`: записать замеренные значения (`hand_cards` 0, `legacy_legs` 0, `unsited` 0 — или объявленные пробелы механизма §5.0 с причиной); `told-ratchet.json` (`rowless`, `untold`, потолки единиц) — по замеру, только вниз; `test_stage_joints.py` — пин K12 и пины счётчиков; `contract_slices.py` — удалить `ahead_card`, `CARD_GROUP`, `NOT_YET_HEAD`, когда `hand_cards` 0; единицы T7a-8/T7d/T7e — замерить, считает ли K6 `untold`, если да — переписать в `conductor`; строки `design/factory-rules-debt.md:271-272` — текст Lead. Любой счётчик больше 0 без объявленного класса — «ночь не доделана». Значение `unsited` и пин K12 по ходу слияний двигает интегратор волны (F-1 (a)), не узлы. Lead: BATCH CANON на CI — к последнему `accepted`.

Карточка: `docs/tasks/specs/20261117-told-before-work-finish-spec.md`, карточка §6 «Card closing» — читать там, не копировать сюда.

Свидетель: спека §6 «Card closing», §0.

Принципы и правила: AR-20, AR-22.

Решение владельца нужно: нет.
