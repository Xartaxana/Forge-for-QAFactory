# Пробелы покрытия и инструментов фабрики стоят в «What blocks delivery on the product side»

id: — | кучка: `report-delivery` | от: прогон CART-1 (MyBooks), 31.10.2026 (свод `experiments/mybooks/cart-1-run-problems.md` п. 6.5) | приоритет: П2 | кандидат наверх: нет

## Что наблюдалось

В отчёте CART-1 десять строк `coverage: OB-1…OB-10` попали в «What blocks delivery on the product side» (`work/ledger.md`, блок «blocks
delivery»; `test-report.md:66`; отчёт t-1632, строка 23). Это пробелы фабрики и покрытия, не дефекты продукта: OB-1…OB-4 в «Behavior
evidence» — `Design unknown / Execution not_run / Verified False` при зелёных TC_001–004 (прогон окна 1 «no per-test identity» — проба не
читает Playwright TS, см. `execution-probes`); OB-1 «disabled buttons not covered (UI)» — у TS-1 нет UI-теста, регрессия отнесена
«разработчикам на уровне компонента». Владелец причины записан `product`, хотя виноват инструмент или покрытие.

Код: словарь владельцев `references/delivery-reason-owners.json` и `scripts/check_delivery.py` (стр. ~108 `OWNER_BY_TRIAGE_VERDICT`);
какая ветка даёт `product` строкам `coverage: OB-n` — **не проверено**, функцию называет спека.

## Класс

Причина недоставки записана не тому владельцу (FR-19: у каждой блокирующей причины назван владелец, нераспознанная — дефект
классификатора; FR-3: причина, которой владеет фабрика, сообщается человеку, а не ставится как выбор), и вердикт читается как «продукт
плох». Тот же класс, что `findings/B-122-prichiny-nedostavki-nasha-bukhgalteriya-i.md` и B-353 (RD1-4: «blocked on the stand» ->
`environment`).

## Что именно менять

1. **Владелец строки `coverage: OB-n` — не `product`**: `references/delivery-reason-owners.json` получает записи классов «пробел
   покрытия» и «инструмент не прочитал тест» (данные, не список проекта; FR-13, AR-1) с владельцем `factory`; `check_delivery.py`
   читает их тем же `reason_owner`, что остальные. Тест: `test_delivery_ownership.py` — фикстура ledger с пробелом `coverage: OB-1`
   и `Execution not_run` при зелёном тесте: строка в «Factory defects», не в «What blocks delivery on the product side».
2. **Нераспознанная причина — находка, не `product` по умолчанию** (FR-19, AR-28): если строка блокировки не классифицирована, её
   владелец «не определён» и отчёт пишет это словом; отказа вердикта «product» на неопределённом нет. Тест: строка неизвестного
   класса — «owner not established», вердикт не говорит «product».
3. **Различать «кейс не исполнен» и «исполнен, но запись теряется»**: когда тест зелёный в прогоне окна, а «Execution not_run» из-за
   отсутствия идентичности теста в отчёте — строка называет причину «run recorded no per-test identity» и владельца `factory`.
   Тест: `test_ledger.py` — фикстура с окном без идентичности, зелёный тест.

## Принципы и правила

P21, FR-3, FR-19, FR-20, FR-35, FR-41; AR-18, AR-25, AR-27. Пересекается по файлам с RD1-4 (`delivery-reason-owners.json`,
`check_delivery.py`) — узел идёт после него.

Решение владельца нужно: нет.

## Повтор LOCAL-1 (02.11.2026)

Прогон LOCAL-1 (t-1672 П-11): в блоке «What blocks delivery on the product side» итоговой сводки 13 `CASE_DEFECT`, пробел стенда и «coverage red: OB-n — none». RD1-21 («принято, слито 0.10.8») — регрессия/не починено: узел RN1-23 (`release-next/findings/20261102-probely-fabriki-v-bloke-produkta-povtor-rd1-21.md`).
