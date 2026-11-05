# Playwright TypeScript не читается манифестом, селектором запуска и детектором «изменено после красного»: роли строят всё руками

id: — | кучка: `execution-probes` | от: прогон CART-1 (MyBooks), 31.10.2026 (свод `experiments/mybooks/cart-1-run-problems.md`, п. 5.2, 5.3, 5.6) | приоритет: П2 | кандидат наверх: нет

Склейка: 5.2 (`manifest_from_tests.py` не читает `.ts`) + 5.3 (`run_suite --mine` строит селектор только для pytest; идентификатор теста из отчёта
Playwright не строится кодом) + 5.6 (детектор «тест изменён после красного» не читает не-python файл и пишет «неизвестно») — один класс «весь путь S5
от файла тестов до результата завязан на python-тест» и общий узел: три инструмента читают один и тот же файл тестов и должны читать его одним
читателем (AR-13). Проба чувствительности (5.1) — отдельная находка и узел: `20261031-proba-chuvstvitelnosti-ne-chitaet-playwright-ts-18-iz-18.md`.

## Что наблюдалось

Отчёты `docs/tasks/specs/reports/t-1632-cart1-run-problems-artifacts.md` (строки 24, 26, 32, 40) и `t-1633-…-transcript.md` (п. 21, 22, 28):
- 5.2: `manifest_from_tests.py` не читает `.ts`; манифест собран автоматором вручную. Exit-gate S5 отказал: `tests[0..11] without case/file/status` — 12 строк
  `tests[]` без `case`; автоматор чинит. Заголовки экземпляров несут теги `@api @regression`, плана они не знают: `s5_precheck` C3, строки PR-1/PR-2
  «не в форме автора». В проекте — FB-4.
- 5.3: `run_suite.py --mine` отказывает: «the factory builds a selector by itself only for pytest node ids. Give the manifest entry `selector_args` and
  `report_test_id` through manifest_put.py once» (`scripts/execution_request.py:2761`). Каждый из четырёх авторов писал `selector_args`/`report_test_id` и запрос
  руками (≈ 3–5 мин на окно, ≈ 15 мин суммарно). Первый запуск TC_009 читался `not_run`: рукописный `report_test_id` не совпал с JUnit; нужен
  `--reparse-block` с `instance_contracts`; 6 «призрачных» `not_run` строк без префикса файла; итоги `passed 34 / failed 2 / not_run 6` против окна
  `passed 17 / failed 1`.
- 5.6: в отчёте — «Unknown which tests changed after a red run — … the test file … cannot be read (not a Python file…)» про `cart-quote-order.spec`,
  хотя записи `expectation_changes` для TC_005 есть (`A/test-report.md:21-23`). Строка собирается `scripts/report_facts.py:1982`
  (`_unknown_line(facts, "expectation_changes", "which tests changed after a red run")`); шифры кода теста (`instance_code_sha`, `instance_content_sha`)
  считает `scripts/proof_level.py` (разделы про `instance_code`, строки ~593–780) по питоновскому синтаксическому дереву. Неизвестное от нечитаемого
  языка выдаётся человеку пробелом продукта.

## Класс

Каждый шаг S5, читающий файл тестов (манифест, селектор запуска, идентичность кода теста), знает только устройство pytest/Python, и для другого языка
молчит или отказывает вместо того, чтобы использовать общее устройство: «язык теста — строка данных, а не код» (AR-1; FR-13). Роль подбирает
идентификаторы вручную, потому что производитель идентификатора (код) и читатель (разбор отчёта) не одна пара (AR-22; FR-17).

## Что именно менять

Направление выбрано: один читатель файла тестов по данным языка (тот же, что у пробы, `probe_by_code.lex` + запись языка в `references/detectors.json`),
и один производитель идентификатора на пару «селектор запуска — разбор отчёта».

1. **Манифест (5.2): `scripts/manifest_from_tests.py`.** Для профиля не-pytest вместо `ast` (python) файл читается тем же лексером, что у пробы
   (`probe_by_code.lex`/`declaration_candidates`, запись `typescript` в `detectors.json`): находит объявления `test(...)`/`test.describe`, заголовок (с тегами `@x` как у
   п. 1(а) EP1-36), маркер кейса из заголовка (форма маркера — из `case_forms`, как у python), файл и строку; пишет в `tests[]` строки с `case`, `file`, `status`, `instance_id`,
   `selector_args`, `report_test_id`. Цикл с шаблонным заголовком даёт одну строку с `generated: true` (EP1-36), экземпляры подтягиваются из отчёта. Что не нашёл —
   отказ списком одним сообщением (как EP1-25): «в `spec.ts` не прочитан тест на строке N: <причина>». Тест: фикстура `spec.ts` из 3 тестов и цикла → манифестная
   вставка с `case` во всех строках; файл `.py` — поведение прежнее (pytest).
2. **Селектор и идентификатор (5.3): `scripts/execution_request.py` (`build_mine_request`; место отказа ~2761) и `scripts/run_suite.py`.** Для профиля не-pytest
   `selector_args` и `report_test_id` строит код по строке данных раннера (`references/launch-causes.json`, таблица раннеров; она строится в EP1-1 — «одна таблица
   идентичности раннера»; здесь добавляется строка `playwright`): `selector_args = [<файл>, "-g", <заголовок как регулярное выражение, экранированный>]`,
   `report_test_id = <та же форма, что читает разбор JUnit раннера>`. Разбор отчёта (`reporters.py`, читатель JUnit) и производитель берут форму ИЗ одной строки данных
   (пара «произвёл — прочёл», AR-22): рукописные значения роли остаются дверью и не нужны. Строка манифеста, чей `report_test_id` не найден в отчёте после прогона, не
   читается `not_run`: она получает `id_not_in_report` и ближайшее имя отчёта (FR-41, FR-59) — призрачные `not_run` невозможны. Тест: фикстура JUnit Playwright и запрос
   `--mine` по строке `.spec.ts` → селектор построен кодом, результат прочитан `passed`; строка с чужим `report_test_id` → `id_not_in_report`.
3. **Детектор изменения (5.6): `scripts/proof_level.py` и `scripts/report_facts.py` (строка ~1982).** Шифр кода теста для не-python файла считается по границам объявления,
   найденным лексером (`body_span`/`locate_target` из п. 1): тот же `same_test` (`instance_code`/`file_code`, D-0017), комментарий в диапазоне не меняет шифр (лексер
   `blank`-ит комментарии). Если лексер объявление не нашёл — «неизвестно» остаётся, но с причиной «не нашёл объявление теста» и владельцем `factory` (не пробелом
   продукта: FR-19, FR-41); отчёт различает «неизвестно из-за инструмента» и «неизвестно из-за данных». Тест: фикстура `.spec.ts`, тест правится после красного (изменён
   вызов) → `changed after red` находит пару; правится комментарий → не находит; сломанный файл → «неизвестно: инструмент» с владельцем `factory`.

Тесты (по одному на пункт): `scripts/tests/test_manifest_from_tests*.py` (п. 1), `test_execution_request*.py`/`test_run_suite*.py` (п. 2), `test_proof_level*.py` и
тест отчёта (`test_report_facts*.py`, п. 3) — имена уточнить по коду. Живое доказательство (FR-33): S5 на MyBooks `a25b080` без рукописных `selector_args` и `report_test_id`.

## Принципы и правила

P1, P2, P11, P17; FR-1, FR-13, FR-17, FR-19, FR-41, FR-59; AR-1, AR-13, AR-22, AR-28.

Связи: EP1-1 (одна таблица раннеров — предпосылка п. 2), EP1-22 (JUnit Playwright читается), EP1-25 (форма маркера и отказ списком), EP1-36 (проба — тот же лексер и
сопоставление заголовка), EP1-17/EP1-23 (число collect при запуске), EP1-20 и EP1-15 (общий `proof_level.py`); `execution-probes/findings/20261028-playwright-junit-otchet-ne-chitaetsya.md`.
Общие файлы: `execution_request.py`, `run_suite.py`, `probe_by_code.py` — порядок EP1-1 → EP1-22 → EP1-37 → EP1-36 (поле «Зависит от» узлов).

Решение владельца нужно: нет.

## Повтор LOCAL-1 (02.11.2026)

Прогон LOCAL-1 (t-1672 П-7, П-8, П-10): манифест TS строился руками (`gen-w9.py`…`gen-w12.py`), селектор держит один `--grep` (TC_012: 1 из 11 тестов), id экземпляров расходятся (43 против 34), квитанции рассчитаны только на pytest. EP1-37 («принято, слито 0.10.8») — регрессия/не починено: узел RN1-21 (`release-next/findings/20261102-playwright-ts-manifest-selektor-id-ekzemplyara-povtor-ep1-37.md`).
