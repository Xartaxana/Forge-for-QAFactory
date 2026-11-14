# Три правки тестов K10 по вердикту темы: пин исходника, отрицательный контроль внутри теста, устаревшее сообщение пина (S2, S3, S5)

id: — | кучка: `live-run-fvf` | от: критик темы «K10 pay-down» (`docs/tasks/specs/reviews/20261114-k10-paydown-topic-critic.md`, S2, S3, S5); слово владельца 14.11.2026: «только B1, остальное завести узлами» | приоритет: П3 | кандидат наверх: нет

## Что не так

Класс фабрики: **тест вне трёх слоёв `docs/TESTING.md` (строки «Пин исходника» и «Отрицательный контроль внутри теста» — «не пишется»); сообщение пина, не пережившее правку числа ролей**. Три независимых правки, каждая свой узел, одна находка.

- **S2 (K1a).** `K10p/refuse-no-literal-line` (`ai-packages/qa-factory/scripts/tests/test_detector_verdict.py`, конец `refuse_cases`) читает текст `role_cli.py` в поисках `- [`: пин исходника. Спека §2 AR-13 просила grep в отчёте, не тест.
- **S3 (K2; дефект спеки, не билдера).** `test_k10p_k2` (`ai-packages/qa-factory/scripts/tests/test_contract_slices.py`) держит `K10p/digest-block-on-page-only/control` и `/negative` — доктор-копия исходника, которая обязана перевернуть результат: отрицательный контроль внутри теста.
  Спека K2 (строка 304) требовала его; построчная проверка «iff» уже есть в строке на роль.
- **S5 (KR).** `test_contract_slices.py` 864: сообщение «its one role over H stands at its named baseline» — теперь три строки `native_headroom`.

## Что именно менять

1. S2: удалить строку `K10p/refuse-no-literal-line` в `test_detector_verdict.py`; grep по `role_cli.py` остаётся строкой отчёта билдера (контроль той же формы, что и поиск).
2. S3: удалить обе строки `K10p/digest-block-on-page-only/control` и `/negative` в `test_k10p_k2`; строка «по ролям» (`iff`) остаётся единственной. Направление выбрано: удалить (вариант критика «сохранить с причиной Lead» не берётся — спека, которая просила контроль, сама дефект).
3. S5: сообщение пина 864 в `test_contract_slices.py` называет три строки, не «one role» (текст берёт число из ключей, не из слова).

Тесты: `python -B ai-packages/qa-factory/scripts/tests/test_detector_verdict.py` и `python -B ai-packages/qa-factory/scripts/tests/test_contract_slices.py` — число проверок падает ровно на удалённые строки (2 в `test_contract_slices.py` для S3, 1 в `test_detector_verdict.py` для S2), остальное зелёное.

Принципы и правила: `docs/TESTING.md` (скоуп-потолок); AR-20 (число проверок падает, не растёт).

Решение владельцу нужно: нет.
