# Маркер отложенного решения `[DEFERRED…]` читается регистрозависимо в `sizing` и по-своему на дашборде: ложная строка «не спрашивали»

id: — | кучка: `driver-hosts` | от: критик диффа OH3-23 релиза 0.10.7 (`docs/tasks/specs/reviews/r0107-s4b2-oh3-23-diff-critic.md`, п. 2 и F-4), 30.10.2026 | приоритет: П3 | кандидат наверх: нет

Что не так / что сделать: OH3-23 свёл маркер в один `DEFERRED_MARKER` (`re.I`) в `project_decisions`, и `audit_factory`, `resolve` читают любой регистр. `sizing.RISK_AREAS_DEFERRED_MARKER = "[DEFERRED: risk areas not named]"` (`sizing.py:227`) проверяется как `in text` (`sizing.py:255`): `[deferred: risk areas not named]` в `test-strategy.md` читается как `not_asked`, строка гласит «no answer and no deferral: topic 4 was not asked» — ложная (FR-41), тогда как A13 читает тот же текст как маркер. Вред ограничен: `areas` пусто в обоих случаях, единственный вызывающий отбрасывает состояние (`sizing.py:774`), вес и размер не двигаются; спека §6 Q3 исключила это явно. Ни один файл пакета не пишет нижний регистр (grep критика). Второй носитель — `factory_dashboard.parse_deferred_decisions`: вариант заголовка молча даёт пусто. `sizing.strategy_area_state` сидит на оси 5 карты (строка «Onboarding answer <-> its written place <-> its readers»). Что сделать: оба читателя берут `project_decisions.DEFERRED_MARKER`; пины — нижний регистр и заголовок-вариант дают то же, что точная форма.

Свидетель: `ai-packages/qa-factory/scripts/sizing.py:227`, `:255-256`; критик `r0107-s4b2-oh3-23-diff-critic.md:8`, `:58-60`; билдер `docs/tasks/specs/reports/r0107-s4b2-oh3-23-builder.md:104`.

Принципы и правила: P2; FR-12, FR-41; AR-1, AR-13, AR-19.

Решение владельца нужно: нет.
