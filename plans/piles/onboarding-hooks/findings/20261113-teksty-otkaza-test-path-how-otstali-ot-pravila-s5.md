# Тексты отказа гарда тестовых путей отстали от расширенного правила S5

id: — | кучка: `onboarding-hooks` | от: Lead, 13.11.2026 | приоритет: П3 | кандидат наверх: нет

## Что наблюдалось

B-355 (J) расширил правило S5: `skills/qa-story/phases/s5.md:234` — «A test file that has to live in a place no recorded carrier of its area covers (inside the
application tree, or in the test repository)…». Тексты отказа остались на старой формулировке:
- `guard_app_under_test.py:25` `TEST_PATH_HOW` — «If this file is a test that has to live inside the application tree, …»;
- `tests/test_protected_test_path.py:602` `HOW` — тот же текст (эталон теста).

Роль читает отказ и правило S5 с разным определением случая (FR-37, P31).

## Что именно менять

Направление выбрано: выровнять `HOW` под s5.md.
1. `TEST_PATH_HOW` (:25): первая фраза — «If this file is a test that has to live in a place no recorded carrier of its area covers (inside the application tree, or in
   the test repository), …»; остальной текст и дверь (`waiver.py … protected test path`) не меняются.
2. `test_protected_test_path.py:602` `HOW` — тот же текст в том же коммите (производитель и читатель вместе).
3. Тест: проверка текста отказа в `test_protected_test_path.py` красит, если фраза разошлась с `s5.md` (сверка по подстроке из s5.md, не по копии).

## Принципы и правила

P15, P31; FR-1, FR-37; AR-9. Связи: B-355, OH1-1 (зона `guard_app_under_test.py`).

Решение владельца нужно: нет.
