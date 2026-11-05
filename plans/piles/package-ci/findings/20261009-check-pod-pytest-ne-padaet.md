# Тесты пакета под pytest: `check()` только записывает, красная проверка не роняет прогон

id: — | кучка: `package-ci` | от: билдер t-597 (аналог, не в owns), 09.10 | приоритет: П2 | кандидат наверх: нет

Что не так / что сделать: в `ai-packages/qa-factory/scripts/tests/*.py` помощник `harness.check()` под
pytest лишь записывает результат, а падает только раннер скрипта / `selftest.py` (`finish()` → exit 1 при
FAIL). Поэтому `python -m pytest scripts/tests/<file>.py` зелёный и при красной проверке — свидетель
«N passed» под pytest ничего не доказывает для этих файлов; класс — все скрипт-тесты пакета, которые
гоняются и так, и так (CI `package-fast` зовёт `selftest.py --fast`, разработчики — pytest). Сделать:
`check()` под `PYTEST_CURRENT_TEST` поднимает `AssertionError` (или `pytest.fail`) на FAIL, не меняя
поведения раннера; один тест на оба пути; builder-rules: какой из двух раннеров — свидетель.

Свидетель: `docs/tasks/specs/reports/t-597-builder-report.md` («Analogs» 3); `scripts/tests/harness.py`
`check`/`finish`; пример — `test_critic_rollcall_apply_fixes.py` (t-597: `SKIP:` и `pytest.skip` в двух
раннерах).

Принципы и правила: FR-18 (свидетельство исполнения — не свидетельство покрытия), FR-28 (измеритель — код
с тестом), FR-31.

Решение владельца нужно: нет.
