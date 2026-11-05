# C2-3 (ядро) — остатки критика t-826: профильная фикстура `_hand_detail`, вынос дверных тестов, F4/F7/F9/F10/F11

id: — | кучка: `driver-hosts` | от: критик t-826 (`docs/tasks/specs/reviews/t-826-t-817-c2-3-core.md`, таблица находок F4–F11 «queue», аналоги), записал Lead 15.10.2026 16:40 | приоритет: П3 | кандидат наверх: нет

## Что

После слияния conductor/2 C2-3 (ядро; t-817/t-827) остаются:

1. **`_hand_detail` с реальным профилем** пинится только через заглушки `_config`/`s5_profiles`: нужна сквозная фикстура с
   профилем из `config.json` (`profiles[].commands.one_test.argv`) — форма `detail` «`<profile>: <команда> <file>::<test>`».
2. **`test_story_step.py` — 427 проверок, 20–40 минут**: дверные тесты (`decide_door_checks`, `open_close_checks`,
   `door_refusal_checks`, `form_one_checks`) выносятся в `test_story_decide.py`; каждая будущая мутация двери станет дешевле.
3. **F4**: `_put_unresolved` повторяет механику MP-фрагмента `WR:933`; два свёртывания id → имя файла (SS:1197, person_words:157).
4. **F7**: `decide` — 93 строки; `elif` пары вызывающего на глубине 5–6 (SS:1368–1460, SS:1129–1144) — разбить.
5. **F9**: подстрочный тест `missing` (TC-1 внутри TC-10, SS:1140) — класс gates-and-words.
6. **F10**: T5c — `returncode in (0, 2)`: пин точного кода после правки фикстуры под гейт выхода S4.
7. **F11**: перенос расписки теряет `inspection_by` (SI:1575–1576).

## Куда

Строка C3-13 пачки `conductor/batch-3-vhodyashchie.md` (D-0044).
