# Три медленных файла не в `slow_tests.json`, у одного нет потолка в `TEST_TIMEOUTS`

id: — | кучка: `thinking-roles` | от: ревью критика `docs/tasks/specs/reviews/t-2053-critic-tr2-12.md` (F5) | приоритет: П2 | кандидат наверх: нет

Решение владельца нужно: нет.

## Что наблюдалось

- По отчёту узла TR2-12 три файла идут дольше порога `slow_over_s` (10 с), но в `scripts/slow_tests.json` их нет: `test_exit_limit_halt_answered.py` (238 с), `test_brief_pack_sd_head.py` (81 с), `test_probe_gap_door.py` (36 с). Следствия, названные критиком: они попадают в `--fast` (бюджет ~90 с); балансировщик шардов считает каждый за 2,5 с; `package-full-report` показывает их как `+` и красит выше `max_drift` 5.
- Потолок: 238 с против умолчания 300 с при `--jobs 4` — форма FR-31. Прецеденты с теми же числами получили 600 (`test_blast_radius.py`, `test_story_run_freshness.py`). Строка `TEST_TIMEOUTS` для `test_exit_limit_halt_answered.py` нужна сразу (`scripts/selftest.py:100`).
- Список правится не руками: `--slow-tests --from <вывод канона> --update` после канона пачки (правило докстринга `slow_tests()`).
- Очередь критика: почему 13 проверок стоят 238 с в файле, который отчёт описывает как быстрый.

## Что именно менять

### TR4-4. Реестр медленных тестов после канона

- Где: `scripts/selftest.py` (`TEST_TIMEOUTS`: строка `"test_exit_limit_halt_answered.py": 600`), `scripts/slow_tests.json` (обновление командой `--slow-tests --from <вывод канона CI> --update`, три файла в `files`).
- Поведение: после обновления три файла вне `--fast`; `max_drift` не превышен; выбор между «ждать канон» и «внести раньше» решает Lead пачки (до канона допустимо только строка `TEST_TIMEOUTS`).
- Тест: свидетель — `scripts/tests/test_current_audit_contract.py` (проверка, что `TEST_TIMEOUTS` — одно место для потолка) и сам `--slow-tests` без `--update` (нет дрейфа).
- Отдельно (вопрос в узле, не отмена): почему `test_exit_limit_halt_answered.py` тратит 238 с на 13 проверок — разбор причины и, если это одна дорогая подготовка, её общий фикстур; в узел входит только разбор, правка — по его итогу.

Принципы и правила: FR-31, FR-28.
