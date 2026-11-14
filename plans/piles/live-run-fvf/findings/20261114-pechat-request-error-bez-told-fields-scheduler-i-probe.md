# Ещё два места печатают `RequestError` без записей: `execution_scheduler.py` и `onboarding_probe.py` (S6 критика темы K10)

id: — | кучка: `live-run-fvf` | от: критик темы «K10 pay-down» (`docs/tasks/specs/reviews/20261114-k10-paydown-topic-critic.md`, S6, «Queue lines» 5); слово владельца 14.11.2026: «только B1, остальное завести узлами» | приоритет: П3 | кандидат наверх: нет

## Что не так

Класс фабрики: **один путь для одного и того же (P31): записи `RequestError` печатает каждый печатающий, не часть из них** (вне владельцев K10; рядом с FV2-43/FV2-44, но их владения эти места не называют).

- `ai-packages/qa-factory/scripts/execution_scheduler.py` 709-710 печатает `{"status": "invalid_schedule", "error": str(exc)}` без `**told_fields(exc)`; все JSON-печатающие `run_suite.py` того же исключения несут его (2811, 2842, 2933, 2983).
- `ai-packages/qa-factory/scripts/onboarding_probe.py` 279-280 возвращает `[str(exc)]`.

Покрытие существующим узлом проверено: FV2-43 (голые сайты ER/RS) и FV2-44 (`window_record.py:267`, `probe_by_code.py:2892`) этих файлов не называют.

## Что именно менять

1. `execution_scheduler.py`: печать `invalid_schedule` дополняется `**told_fields(exc)` (тот же вызов, что в `run_suite.py`), ключ `error` остаётся.
2. `onboarding_probe.py` (279-280): возврат несёт записи исключения тем же читателем (`detector_verdict.told_fields`/`told_line`), не `str(exc)` один. Конкретная форма возврата — по месту (функция возвращает список строк): строка на запись; если возврат не годится, функция называется в отчёте и узел возвращается вопросом.
3. Тесты: в таблице `ai-packages/qa-factory/scripts/tests/test_detector_verdict.py` строки `K10p/printer-carries-told/<site>` для обоих мест (запись есть → ключ `told` есть; записей нет → вывод байт-в-байт прежний).

Принципы и правила: P31; AR-13, AR-18; FR-14.

Решение владельцу нужно: нет.
