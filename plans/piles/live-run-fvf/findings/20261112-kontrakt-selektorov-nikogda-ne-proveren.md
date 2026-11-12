# Контракт селекторов профиля не может стать «проверенным»: онбординг не репетирует команду, а запись пробы не совпадает с тем, что спрашивает проверка

id: — | кучка: `live-run-fvf` | от: живой прогон LR2-1 (плечо `factory`, релиз 0.11.0 + FV1-1), 12.11.2026 | приоритет: П1 | кандидат наверх: да

## Что не так

S5, окно 2 (TC-006, TC-007): автоматор написал тесты, `run_suite --mine` отказал: «invalid_request (no verified adapter selector
contract; profile selectors empty); settle by declaring selectors for profile playwright-tests»
(`work/handoffs/S5-qa-automator-2.yaml:129`). Дирижёр предложил человеку «you declare the selectors in qa-factory/config.json»
(какие и в какой форме — не сказано).

Проверка оператора 20:28–20:30:

- `profile_contract.selectors_verified` (единственный ответ, AR-13): без литерала `selectors.verified` нужна запись онбординга,
  что ЭТА команда отрепетирована (`onboarding_probe.earlier_proof(...) == "same_command"`). Онбординг 17:22 такой записи не
  оставил — `config.json` вышел с `"selectors": {}`.
- Собственная проба фабрики `onboarding_probe.py --probe-profiles --profile playwright-tests` (дверь, которую называет отказ):
  `report.state: proven`, «one existing test ran and left a report the factory can read (6 test(s) counted)», выход 0.
- После неё `selectors_verified` → `False`: `earlier_proof` → `{'state': 'command_changed'}`. Запись пробы и проверка сравнивают
  разные формы команды (`_one_test_argv` отдаёт шаблон с `<test-file>`), так что честная проба команду «проверенной» не делает
  никогда. Единственная рабочая дверь — литерал `"selectors": {"verified": true}` руками.

Класс: гейт требует доказательство, которое производитель (проба онбординга) произвести не может (FR-5, FR-11, AR-22); дверь
отказа ведёт к инструменту, чей результат гейт не читает (FR-2); человеку предложено «объявить селекторы» без формы (FR-1, P15).

Обход оператора (по слову владельца «конфиг проекта»): в копии плеча `profiles[playwright-tests].selectors: {"verified": true}`
(копия до правки `config.json.before-selectors-verified-20261112`), основание — проба фабрики `proven`; `selectors_verified` →
True. Перезапуск `factory-17` с `retry`.

Свидетель: `runs/factory-16.log`; `notebook.md`, «Ход прогона», 20:27–20:31.

## Что сделать (предложение оператора)

Проба онбординга пишет запись в той форме команды, которую читает `selectors_verified` (одна функция digest на обе стороны,
AR-13), и онбординг запускает её всегда, когда у профиля есть `one_test`; отказ `run_suite` называет команду пробы и форму
литерала. Тест: проба `proven` → `selectors_verified` True без литерала; изменённая команда → False.

Принципы и правила: P1, P15; FR-1, FR-2, FR-5, FR-11; AR-9, AR-13, AR-22.

Решение владельца нужно: нет.
