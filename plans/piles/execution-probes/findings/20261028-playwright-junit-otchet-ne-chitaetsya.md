# Playwright Test (JS): отчёт JUnit не читается — проба требует `{report_path}` в команде, а путь отчёта Playwright берёт только из переменной окружения или конфига; проба сканирует весь каталог и ловит чужой файл

id: — | кучка: `execution-probes` | от: отзыв пользователя Dev6 (TP2-2702), плагин 0.10.x, 28.10.2026 (разбор t-1553) | приоритет: П1 (слово владельца 28.10.2026: «Приоритет 1. Берём в следующий релиз» — релиз 0.10.7) | кандидат наверх: да

## Что наблюдалось

Слова пользователя, как написаны: «Back and forth with reporting: - The tests run on this machine. With npx.cmd, the S1 spec ran 5 passed, 0 failed. - A report did get written. With a JUnit reporter in the config, Playwright wrote a clean results.xml (5 tests, 0 failures, no XML entities). - The factory's probe still can't read it. The factory insists the command carry the report location as a {report_path} word, so it controls where the report lands. Playwright has no flag that takes a file path for JUnit, only an environment variable the factory can't set. The one flag I tried, --output, is Playwright's artifact directory and not a report file. The probe read the wrong thing and failed with "declares XML entities". - Result: this is a limit of the factory's Playwright support, not of your setup. The factory's own guidance says it doesn't attempt this change. I choose to run cases myself which took some time, because I had to give him the results of each later.»

Итог: на проектах с Playwright Test весь S6 уходит вручную; человек сам прогоняет кейсы и сам сообщает результат по одному.

## Где в коде

Из разбора t-1553 (пункт 4; пути от `ai-packages/qa-factory/`; номера строк проверить по коду при взятии):
- Контракт `{report_path}`: `scripts/execution_request.py:220-232` (внешний репортёр `junit-xml`/`trx`: `command.report_path == "{report_path}"` и ровно один токен argv с ним, ради уникального отчёта запуска), запись — `execution_request.py:1558`; `scripts/profile_contract.py`; `scripts/onboarding_probe.py:239-264` (отказ «its report kind is `junit-xml` and no word of it carries `{report_path}`»); подстановка в раннере `scripts/run_suite.py`; проба гейта A `scripts/gate_preflight.py:2456-2462`.
- Окружение: раннер передаёт только унаследованное, `scripts/run_suite.py:1675` `env = dict(os.environ)`; поля `env` у профиля или конфига нет (`profile_contract.py`, `execution_request.py`, `templates/config.json`, `config-keys.json`). Playwright берёт путь JUnit только из `PLAYWRIGHT_JUNIT_OUTPUT_NAME` или конфига.
- Фабрика знает требование и отказывается: `references/report-cures.json:64-73`, строка `playwright`: флаг `--reporter=junit`, `add_argv: null`, `needs`: переменная `PLAYWRIGHT_JUNIT_OUTPUT_NAME`; `person_words`: «the factory cannot set an environment variable for a command, so I do not make that change»; `propose_text: null`.
- Путь отчёта из конфига: `run_suite.py:327-330` `report_path(cfg)` читает `config.run.report_path`, `no_report_words` (`:363-364`) отсылает к `run.reporter` и `run.report_path`; но контракт S5 (`execution_request.py:221`) и проба онбординга (`onboarding_probe.py:258-262`) всё равно требуют токен `{report_path}` в команде.
- Проба читает не тот файл: `gate_preflight.py:2648-2670` просматривает каждый файл родительского каталога отчёта (`report.parent.rglob("*")`); при `--output` (каталог артефактов Playwright) она открыла соседний файл с DOCTYPE и подняла «the report declares XML entities, which the factory does not expand» (`gate_preflight.py:2669`; тот же текст `scripts/reporters.py:170`, `entity_declared`, отказ B-416 N1). Сообщение — ложный диагноз «чужой файл в каталоге пробы» (вывод из кода, файл не виден).

Ограничение вывода: прогона TP2-2702 в руках не было.

## Класс

Фреймворк без флага командной строки для пути отчёта — класс, не один проект (P2, AR-1, FR-13). Две части: (1) фабрика не умеет задать окружение команды, (2) проба смотрит каталог, а не файл отчёта. Блокер на практике для проектов с таким репортёром: дверь формально есть (`scripts/manual_capture.py`), но цена — весь S6 вручную. Родственные (в этой же кучке): пробы не-Python (B-337, B-345).

## Решения владельца

Владелец, 28.10.2026: «Приоритет 1. Берём в следующий релиз» — это П1 релиза 0.10.7 (не 0.10.5). Узел EP1-22: у профиля команды поле `env` с подстановкой `{report_path}` (или файл отчёта, объявленный в конфиге), которое читают `execution_request`, `onboarding_probe`, `run_suite`; лекарство `playwright` из `report-cures.json` применяет сама фабрика; проба читает только файл отчёта, а не каталог. Решение владельца нужно: нет (направление дано; форму поля выбирает спека дизайнера).

Принципы и правила: P1, P2, P19, FR-1, FR-11, FR-13, FR-17, FR-57, AR-1, AR-22.
