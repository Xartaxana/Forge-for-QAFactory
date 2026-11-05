# Очередь критика t-1342 (HF2-18 B): близнецы N9, общий помощник ключевых фраз, один экспорт пределов

id: — | кучка: `onboarding-forge` | от: критик t-1342, 27.10.2026 | приоритет: П3 | кандидат наверх: нет

Что не так / что сделать (три строки очереди ревью):
- Q1 — близнецы N9 вне вопроса: `factory_dashboard.py:934`, `check_witness.py:228-236` — как записано в t-1256.
- Q2 — общий помощник «ключевые фразы PRESENT/ABSENT/COUNT + свёртка пробелов» в `scripts/tests/harness.py` вместо копий в `test_gate_continuation_texts.py`, `test_mixed_then_texts.py`, `test_critic_lines_hf2.py`, `test_s7_control_experiment_texts.py`; табличная форма негативных контролей (рядом: `the_checker_reports_what_it_should`, ~70 строк при пороге 60).
- Q3 — один экспорт пределов `selftest.py --limits` для тестов-пинов (пять копий `12000`).

Свидетель: `docs/tasks/specs/reviews/t-1342-hf2-18b-diff-review.md`, раздел «Очередь (строкой в невзятой пачке кучки)».

Принципы и правила: FR-54, FR-28, AR-15, AR-20.

Решение владельца нужно: нет.
