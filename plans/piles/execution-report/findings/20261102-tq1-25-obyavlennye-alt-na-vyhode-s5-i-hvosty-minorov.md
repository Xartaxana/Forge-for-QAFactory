# Объявленные трактовки ALT доходят до человека только дисциплиной критика: выход S5 их не читает

id: — | кучка: `execution-report` | от: критик t-765 (TQ1-25, B-1, m-6…m-10), билдер t-768, 02.11.2026 | приоритет: П2 | кандидат наверх: нет

## Что наблюдалось

TQ1-25 (`release-next/1`) добавил к кейсу ключ `alternatives` (трактовки B) и пробу `probe_by_code.py --alternatives`; записи `work/probes/alternative/<IID>--<CASE>--<ALT>.json`.

- **B-1 (Lead при приёмке).** Отчёт пробы (`_print_alternatives`) показывает `unknown`, `stale`, `case_unreadable`, `incomplete`; устав критика (шаг 3) велит их прогнать, но НА ВЫХОДЕ S5 их не читает ничто: поиск `alternatives|ALT-1|TQ1-25` по `plans/piles/execution-report` пуст (контроль: `window_record` — три файла). Пока строки нет, утечка держится на дисциплине критика, а строка очереди — детектор этой утечки (спека t-739, §4 m8: «`window_record.py` печатает объявленный ALT без судимой записи как пробел экземпляра»).
- Остатки минорных (t-765/t-768, очередь):
  - m-6: на `wrong_location` человеческая причина — голый токен несовпадения `failure_kind`, а `model:` печатается только рядом с `proven`/`not_separated`; критик решает, чья вина (модель или тест) без имени вида падения и места;
  - m-7: проверка символической ссылки не воспроизведена на Windows — добавить случай `try: os.symlink … except OSError: skip`, чтобы Linux `package-full` его гонял;
  - m-8: `parse_alternative_token` проверяет `ALT-\d{1,3}`, а `alternatives_errors` — 1..999: `TC-001:ALT-0` и `ALT-000` проходят разбор и кончаются `unknown` «not declared»; нужен один предикат `C.alternative_id_ok`;
  - m-9 (Lead): коммит несёт `axes: not a mechanism`, хотя добавлен долг критика, форма дизайнера и схема записи — запись «механизм» в журнале Lead;
  - m-10: `_case_rows` (`probe_by_code.py:~3674`) передаёт `entries and json.dumps(entries)` в `alternatives_errors`, который разбирает строку заново; `parse_json_list` принимает список — сериализация лишняя.

## Класс

Состояние, которое видит только роль и которое не читает выход стадии (AR-22, AR-28; FR-41): пробел в пробе доходит до человека лишь дисциплиной.

## Что именно менять

Направление выбрано (Lead пачки release-next/1, 02.11.2026).

1. B-1: `scripts/window_record.py` — для каждого объявленного ALT (`alternatives_from_text`) окна без судимой записи (`work/probes/alternative/…`, свежей по `probe_by_code.alternative_fresh`) печатать строку пробела экземпляра `alternative <ID> of <CASE>: not judged (<unknown|stale|incomplete|case_unreadable>)`; такой пробел идёт тем же путём, что `probe_gap_block` (виды `named_by: factory:` не вводить — это пробел слова критика, а не данных). Ожидание: окно без объявленных ALT — вывод не меняется (AR-23); все ALT судимы и свежи — строки нет. Тест: `scripts/tests/test_window_record*.py` — (а) нет ALT → вывод прежний, (б) один ALT без записи → строка `not judged`, (в) запись есть и устарела (изменён `reading`) → `stale`, (г) запись `intended_failure` → строки нет.
2. m-6: `probe_by_code._print_alternatives` печатает `model:` и рядом с `wrong_location`; причина называет вид падения и место (`failure_kind=NameError at <file>:<line>`). Тест: `test_probe_by_code_alternative.py` — вход `replace: ""` → причина с `NameError`.
3. m-7: тест K14 в `test_probe_by_code_alternative.py` получает случай с символической ссылкой на файл вне проекта (`os.symlink` в `try`, `OSError` → пропуск).
4. m-8: `contract.alternative_id_ok(value)` — единственный предикат 1..999; `parse_alternative_token` и `alternatives_errors` зовут его. Тест: `ALT-0`, `ALT-000`, `ALT-1`, `ALT-999`, `ALT-1000`.
5. m-10: `_case_rows` передаёт список, не JSON-строку. Тест: существующий `test_probe_by_code_alternative.py` без правки ожиданий.
6. m-9: запись «механизм» в журнал и блок осей — делает Lead при приёмке.

## Принципы и правила

FR-33, FR-41; AR-22, AR-23, AR-28.

## Связи

- `docs/tasks/specs/reviews/t-765-tq1-25-diff-critic.md` (B-1, m-6…m-10); `docs/tasks/handoffs/t-768-tq1-25-fix.md`; `docs/tasks/specs/t-739-tq1-25-amended.md` §4 m8; живое доказательство FR-33 — строка «TQ1-25: проба ALT-1» в «Живых доказательствах» `release-next/1`.

Решение владельца нужно: нет.
