# Часть регрессии, которую ведут разработчики, названа без путей

id: — | кучка: `execution-report` | от: прогоны TP1-12586 (28.10 и 29.10) и 14857 (ручной), 30.10.2026 (владелец, 30.10.2026) | приоритет: П1 | кандидат наверх: нет

Что не так / что сделать: пункты «за разработчиками» записаны словами, а не путями: 12586, 28.10 — «a test that save()/update() keep the old
commit semantics…»; 12586, 29.10 — «both already have developer tests, C4»; 14857, ручной прогон — «provider response mapping and SVN
stamp (C2, C3, router test)». Человек не может найти ни тест, ни убедиться, что его нет. Нужно: каждый пункт этой части — реальный путь
существующего теста либо явная строка-пробел «теста нет», обращённая к разработчикам, и такой пробел не считается пунктом регрессии.

Свидетель: `testproject1-dev-010/testproject1-sdk/test-harness/qa-factory/artifacts/TP1-12586/test-report.md:80`; ночной 14857 — пути названы
(`test-report.md:65`), ручной — нет (разбор `docs/tasks/specs/reviews/t-1605-14857-night-vs-manual.md`); архивные копии:
`archive/testproject1-dev-010-run-12586-20261028/…/TP1-12586/test-report.md`. Производители: `agents/qa-test-strategist.md` п. 6 (поле
`regression` области), `scripts/report_facts.py` (`_regression`), `scripts/delivery_verdict.py` (`regression_lines`).

Принципы и правила: P24 («реальные пути»); P20; FR-37; FR-41; AR-27.

Решение владельца нужно: нет.
