# Генератор `scripts/field_cards.py` и остаток свипа валидаторов (строки 4, 5, 10, 12, 18, 27, 33)

id: — | кучка: `onboarding-forge` | от: спека t-1355 §7, решение Lead F-8, 27.10.2026 | приоритет: П3 | кандидат наверх: нет

Что не так / что сделать: пачка валидаторов (узлы VC-N1..VC-N3, спека t-1355) вручную держит копии списков полей: `FIELD_VOCABULARIES`, список `:118` и ключи `:111` в `role-commands.json`, карточки `ahead-cards.json`. Что сделать (форма, не построено): генератор `scripts/field_cards.py` над константами-носителями (`V2_REQUIRED`/`V2_RULES`, `SPEC_REQUIRED`, `FACTS_KEYS`, `TRIAGE_ROW_IDS`, `window_record.REQUIRED_ROW_FIELDS`, источники VOCABULARIES): `render(name)` и `--write` / `--check`, размеченные отрезки `<!-- field:<name> -->…<!-- /field -->`, как у `tools/factory_rules_index.py`; `--check` в `selftest --contracts` и CI `package-fast`. Критик на план до кода (генератор правит карточки кодом). Туда же: остаток строк свипа 4, 5, 10, 12, 18, 27, 33 (`docs/tasks/specs/reviews/t-1349-validator-class-sweep.md`, таблица §3) и перевод любого локального рендерера закрытых списков на единый.

Свидетель: `docs/tasks/specs/t-1355-validator-class-fields-and-all-problems.md`, §7 и §8 F-8; `docs/tasks/specs/reviews/t-1349-validator-class-sweep.md`.

Принципы и правила: FR-13, FR-17, FR-38, AR-1, AR-10, AR-15.

Решение владельца нужно: нет.
