# Импорт `transcripts` в `agent_budget.py` ловит только `ImportError`: `SyntaxError` в `transcripts.py` роняет хук на каждом вызове инструмента

id: — | кучка: `forge` | от: критик t-757 (находка 2, аналог; `class_completeness`), записал билдер t-761 по поручению Lead 14.10.2026 | приоритет: П2 | кандидат наверх: нет

Что не так: `tools/agent_budget.py:57-63` импортирует `transcripts` вложенным `try … except ImportError` и при отказе
ставит `transcripts = None` («evaluate() then fails open, silently»). Это ловит только ОТСУТСТВИЕ модуля. Модуль,
который есть, но не импортируется (`SyntaxError`, ошибка выполнения при импорте), не ловится: `agent_budget` падает при
импорте с кодом 1, не блокирующим, — гейт стоимости (D-0035) молча выключен на каждом вызове инструмента, а он идёт на
КАЖДОМ. Тот же класс, что находка 2 критика t-757 для `dispatch_manifest` в том же файле; её починили в t-759
(`_manifest_import_failed`, `:66`, одна громкая строка в stderr), а импорт `transcripts` остался прежним.
Хук `tools/handoff_gate.py:59-66` этим дефектом НЕ страдает: оба его импорта в `except Exception`, сломанный
`transcripts` даёт отказ воркеру гейтируемого вида и пропуск главной сессии (`test_main_broken_imports_refuse_a_worker`).
Соседи по классу (ловят только `ImportError` вокруг `transcripts`): `tools/dispatch_gate.py:315-320` (там запасной путь
с видимой фразой `PARALLEL CAP`, но `SyntaxError` и там не ловится), `tools/journal_echo.py:259-261`,
`tools/tier_echo.py:95-97` — ось 14 `docs/SIBLING_MAP.md`.

Что сделать: в `agent_budget.py` второй и внешний `except` импорта `transcripts` — `Exception`, с одной строкой в
stderr по образцу `_manifest_import_failed` (громко один раз, хук живёт, лимит по `usage_total` остаётся измеримым только
если модуль есть, иначе пропуск как сегодня); тот же осмотр у трёх соседей — починка или запись «не нужно — почему»
построчно. Тест — подпроцесс с битым `transcripts.py` первым на `sys.path`: хук выходит 0, в stderr одна строка.
Детектор: тест выше и калибровочная проверка 17(a) (воркер с контекстом выше 400K: гейт стоимости молчал).

Строка в пачке: `plans/piles/forge/batch-6-vhodyashchie-2.md` F6-9 (D-0044, тем же ходом).
