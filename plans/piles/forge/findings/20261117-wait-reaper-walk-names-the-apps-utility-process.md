# Обход предков `wait_reaper` может принять за сессию служебный процесс приложения (`Claude.exe --type=utility`), и `unknown-root` даёт ложный след (критик t-1160, N1)

id: — | кучка: `forge` | от: критик t-1160 (`docs/tasks/specs/reviews/t-1160-bounded-waits-reaper-code.md`, N1; leaving line «узел: new, Lead opens»), 17.11.2026 | приоритет: П3 | кандидат наверх: нет

## Что наблюдалось

Измерено критиком: приложение — `Claude.exe` (17100), имя из Toolhelp сравнивается без учёта регистра, а терминалы приложения (`powershell -NoExit` 8900, 10312) — дети `Claude.exe --type=utility` 11816. Человек, сливающий в таком терминале, получает «сессию» = 11816. Ничего не останавливается (его дети не корни обёрток), но они пишутся как `unknown-root`: проверка 27 (e) читает каждый как «смену обёртки harness», то есть ложный след. Утверждения `docs/tasks/specs/20261117-bounded-waits-mechanism-spec-r2.md` §5.0 «приложение никогда не достигается» и «никогда не называет чужой процесс» в такой раскладке неверны.

## Что именно менять

Направление выбрано Lead (17.11.2026, до слова владельца). Предложение критика: walk the image path (`QueryFullProcessImageNameW`, in-process) with a data row such as `claude-code`, or record a named residual. Развилка — Lead при взятии узла. Файлы: `tools/session_proc.py`, `tools/wait-reaper.json`, `tools/test_wait_reaper.py` (строка P-walk). Тест: обход, чей первый предок по имени `claude.exe` — служебный процесс приложения (`--type=utility`), не возвращает его как сессию.

Связи: `docs/tasks/specs/reviews/t-1160-bounded-waits-reaper-code.md` N1; узел FG7-55 (`batch-7-vhodyashchie-4.md`).

Решение владельца нужно: нет.
