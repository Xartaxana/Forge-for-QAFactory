# `test_stand_lease` «a free stand is taken without waiting» краснеет под нагрузкой: `waited_s == 0` меряет часы, не ожидание (FR-31)

id: — | кучка: `onboarding-forge` | от: Lead, 21.10 (измерение билдера t-1185 ремонта CI, хэндофф `docs/tasks/handoffs/t-1236-ci-red-cx1-18.md`) | приоритет: П2 | кандидат наверх: нет

Что не так / что сделать: кейс «a free stand is taken without waiting» в `stand_lease.py --selftest` утверждает `waited_s == 0`, а
`waited_s = int(round(_monotonic() - began))` (`scripts/stand_lease.py:232`) — это время взятия замка по часам, не факт ожидания. Один
в docker файл даёт 41/41; шесть `stand_lease.py --selftest` разом в docker — шесть `FAIL a free stand is taken without waiting`; в
`selftest.py --fast` на той же машине — 312/313 дважды. CI 7948891 его прошёл: скрытый флейк под нагрузкой — ровно класс FR-31
(«тест, падающий только под нагрузкой, — дефект теста»), сосед PC1-3 (`test_obligation_join` под нагрузкой). Сделать: кейс
проверяет, что замок взят без ожидания, по факту — `queued_behind is None` и ни одного вызова `_sleep` (подменённого в тесте), а не
по стенным часам; `waited_s` остаётся в результате как измерение (FR-26), но не как утверждение теста. Один узел билдера (Sonnet);
свидетель — файл один и шестью копиями разом в docker python:3.12. `stand_lease.py` не менялся с 15c83eac (28.09); CX1-18 его не
трогает.

Свидетель: хэндофф t-1236 (две команды docker `selftest.py --fast`: `FAST_EXIT=1 … test_stand_lease.py 6.8s — exit 1 | 40/41 ok | FAIL
--selftest passes`; шесть параллельных `--selftest` — шесть FAIL); `scripts/stand_lease.py:225-233`.

Принципы и правила: FR-31, FR-26, FR-32; AR-12 (трение CI с собственным тестом).

Решение владельца нужно: нет (техническое).
