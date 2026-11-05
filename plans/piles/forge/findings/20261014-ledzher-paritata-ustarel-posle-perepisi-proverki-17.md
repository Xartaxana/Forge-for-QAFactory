# Леджер паритета ждёт якорь «17. Reserved for deployment-specific checks», а проверка 17 переписана под гейты цены

id: — | кучка: `forge` | от: Lead, 14.10.2026 08:00 (первая недельная калибровка, проверка 22) | приоритет: П3 | кандидат наверх: нет

Что не так: `python tools/install_parity.py --check` → MISSING (1): `unit=process-docs:weekly-calibration-protocol`,
`host_path=PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md`, `anchor='17. Reserved for deployment-specific checks (register yours
here —'`. Проверка 17 протокола переписана этим деплойментом под D-0035 (гейты цены, CLAUDE.md адаптация 6: «Detector:
calibration check 17»), а строка леджера `docs/ADOPTION_LEDGER.md` по-прежнему ждёт якорь исходника. 45 единиц CLEAN;
красный — один, и он ложный: единица на месте, устарел якорь.

Что сделать: строка леджера для этой единицы получает якорь нынешнего заголовка проверки 17 (прочитать его в протоколе,
не угадывать) и пометку «host-adapted: check 17 rewritten (D-0035)»; тест леджера (если есть) — положительный контроль
на новый якорь. Детектор: калибровочная проверка 22 (`install_parity --check` зелёный).

Строка в пачке: `plans/piles/forge/batch-6-vhodyashchie-2.md` F6-4 (D-0044, тем же ходом).
