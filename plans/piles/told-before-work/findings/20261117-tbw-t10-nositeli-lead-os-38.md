# Носители Lead: ось 38, AR-10/AR-9, FR-38, critic-brief, калибровка

id: — | кучка: `told-before-work` | от: спека «Told before work: finish» (`docs/tasks/specs/20261117-told-before-work-finish-spec.md`), 17.11.2026 | приоритет: П1 | кандидат наверх: нет

Что не так / что сделать: Класс: механизм «требование проверки — одна строка ↔ `refusal()` ↔ страница/раздел дирижёра ↔ транспорты» не имеет оси карты, детектора и правил в носителях (ось, AR, FR, критик, калибровка).

Что именно менять: Lead (§5 спеки): `docs/SIBLING_MAP.md` — новая Axis 38 (перед коммитом перечитать хвост карты: номер мог занять другой); упоминания «axis 37» в механизм-спеке и в спеках T1r-sites/T1r-pages переуказать на 38 там, где это эта ось; `design/architecture.md` AR-10 Detector/Gap и AR-9 change check; `docs/tasks/critic-diff-brief.md` J1/J2 и вопрос 9 (новые счётчики `unsited`, `hand_cards`, `legacy_legs`, `rowless`, `untold`, `native_headroom`); `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md` — проверка «предложение строки заявляет больше, чем её тело»; `design/factory-rules.md` FR-38 *Check:* называет `stage_joints.py --check` и `contract_slices.py --check`; P1-b C11 зовёт `rows_for` — убедиться, что его узел есть. Коммит механизма — четыре вопроса с блоком осей (38 осей) и строкой `tier:`.

Карточка: `docs/tasks/specs/20261117-told-before-work-finish-spec.md`, карточка §5 «T10» — читать там, не копировать сюда.

Свидетель: спека §5; механизм-спека §5.1 T10.

Принципы и правила: AR-9, AR-10; FR-38.

Решение владельца нужно: нет.
