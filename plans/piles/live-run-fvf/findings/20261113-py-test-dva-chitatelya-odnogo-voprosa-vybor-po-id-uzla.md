# Два читателя одного вопроса «раннер выбирает тест по id узла?» отвечают по-разному для `py.test`

id: — | кучка: `live-run-fvf` | от: критик кода темы FV1-18, ключ K2 / FIX-1, `docs/tasks/specs/reviews/20261113-fv118-topic-code-critic.md`; условие Lead F6 (спека `docs/tasks/specs/20261113-fv1-18-selector-contract-spec.md` §9c, §12), 13.11.2026 | приоритет: П2 | кандидат наверх: нет

## Что не так

Класс фабрики (P31, AR-13): **один вопрос, два читателя** — «выбирает ли этот раннер тест по id узла». Для команды `py.test` они
расходятся (проба критика, K1/K2):

- читатель маршрутизации и сборки id узлов — `is_pytest_command`: `execution_request.py:315` (выбор «pytest или склейка» в
  `validate_request`), `execution_request.py:3463` (`pytest_run`, строит селекторы по id узла в `--mine`), `run_suite.py:306`
  («путь pytest решает этот один предикат, не данные»); для `py.test` отвечает «да»;
- читатель контракта селекторов — `launch_check.runner_identity(words)["node_id_selection"]` (`profile_contract.py:399`), ключ данных
  `selection_by_node_id` строки запуска; для `py.test` отвечает `no_selection_form`.

Последствие (K2): отказа нет, прогон идёт, но каждый поведенческий прогон проекта на `py.test` печатает заметку SELECTORS «выбор
раннера не проверен», хотя фабрика сама собрала для него селекторы по id узла; дверь заметки это не лечит. `tox -e py`: оба
читателя согласны (оба «нет») — не дефект. Условие Lead F6 «брешь гарда на `py.test` заведена находкой» не выполнено, пока этого файла нет.

## Что менять

Направление выбрано (Lead пачки, 13.11.2026): **один читает другого; единственный ответ — ключ данных `node_id_selection`
(поле `selection_by_node_id` строки запуска)**; вызывающие `is_pytest_command`, которым нужно «выбирает по id узла», читают его.

1. `scripts/execution_request.py:315` и `:3463`, `scripts/run_suite.py:306`: там, где значит «выбирает по id узла», брать
   `launch_check.runner_identity(words)["node_id_selection"]`, а не `is_pytest_command`. Остальные смыслы `is_pytest_command`
   (например, формулировка `no_direct_form`, `launch_check.py:739`) не трогать. Тест: строка на каждое слово раннера — `pytest`,
   `python -m pytest`, `py.test`, `tox -e py`, `npx jest` — ответ маршрутизации и ответ `selector_contract` совпадают.
2. Данные: строка запуска `py.test` в `references/launch-causes.json` получает `selection_by_node_id` (или `py.test` признаётся
   формой строки `pytest`) — по правилу данных (AR-1), не списком в коде. Тест: `py.test` даёт `node_id_selection` True и заметка SELECTORS не печатается.
3. Тест на класс: ни одно место пакета (вне `tests/`) не отвечает на «выбирает по id узла» мимо ключа данных (Grep-ряд как
   у критика, с положительным контролем).

Принципы и правила: P31, P2; FR-17, FR-54; AR-13, AR-15; оси карты 11 и 34.

Решение владельца нужно: нет.
