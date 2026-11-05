# Окно S5 требует квитанции качества, которых не пишет ни один скрипт фабрики: закрытие только словом человека

id: — | кучка: `hotfix-12586` | от: прогон TP1-12586 на 0.10.3, `testproject1-dev-010` (`factory-backlog.md` FB-8; `state/words/s5-20261028-quality-receipts.txt`; карта t-1468 P5); слово владельца 28.10.2026 | приоритет: П1 | кандидат наверх: нет

## Что наблюдалось

Окна S5 закрываются только словом человека «без квитанций качества». Состояние стенда: `required_quality_checks: ["ticket_adapter","test_repo","vcs","config_schema"]` — это id проверок готовности (`readiness.py`), записанные дирижёром по `references/controller-api.md:89` и `skills/qa-story/phases/s0.md:445`. `window_record.py:940-950` пишет `"quality_receipts": []` с комментарием «nothing in this package writes a quality receipt». Читатели требования: `acceptance.validate_window` (пробел `quality:<id>`), `coverage_contract`, `controller._s5_collect` (равенство окна и состояния); отказ `controller._code_review_refusal` называет починку «review's own receipts» — двери у критика нет (FR-2).

Это проверка того, что никто не пишет (FR-5, AR-22). Квитанция готовности адаптера тикетов не говорит ничего о коде окна (FR-18) — подставлять её как квитанцию окна было бы ложью.

## Узел

`hotfix-12586/4` HF4-10 (спека t-1469 §5.5, вариант F-5 (а)): требование окна = записанные id ∩ закрытый список id с производителем (`references/quality-receipt-producers.json`, сегодня пусто); остальное — поле окна `quality_not_run`, не проход; окна S5 не ждут слова. Печать `quality_not_run` в отчёте («Quality checks the factory did not run: …») — отдельная строка пачки (`report_facts.py`, вне owns HF4-10). Настоящий производитель (вариант F-5 (в)) — отдельная находка-вопрос `20261028-lint-proekta-na-okne-s5-vopros-vladelcu.md`.

Принципы и правила: FR-2, FR-4, FR-5, FR-18, FR-41, FR-59, AR-9, AR-22, AR-23, AR-28, P11, P22.

Решение владельца нужно: нет (вариант (а) решён Lead 28.10; вопрос про (в) — в отдельной находке).
