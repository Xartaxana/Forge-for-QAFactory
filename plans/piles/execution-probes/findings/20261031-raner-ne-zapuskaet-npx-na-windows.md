# Раннер не запускает команды-обёртки Windows (`npx` → `npx.cmd`): `WinError 2` и `launcher_missing` вместо запуска

id: — | кучка: `execution-probes` | от: прогон CART-1 (MyBooks), 31.10.2026 (свод `experiments/mybooks/cart-1-run-problems.md`, п. 4.8; в проекте — запись `local-urgent` FB-3 в `qa-factory/factory-backlog.md`) | приоритет: П2 | кандидат наверх: нет

## Что наблюдалось

Отчёт `docs/tasks/specs/reports/t-1632-cart1-run-problems-artifacts.md`, строка 42: на онбординге MyBooks (Windows, тесты Playwright) раннер
фабрики не запустил `npx playwright test`: `subprocess` без `.cmd`, `WinError 2`, `launcher_missing npx`. Обход проекта: команды
профиля переведены на `node scripts/run-playwright.mjs` (`QF/config.json`, `profiles[0].commands`, `argv: ["node", …]`); запись FB-3
открыта, правило файла требует закрыть её до следующей истории. Обход переносит работу фабрики в проект: каждый проект на Windows с
`npx`/`npm`/`yarn`/`pnpm` (все на Windows — `.cmd`) получит то же.

Причина в коде (проверено 31.10.2026): запуск без оболочки получает `argv[0]` как есть —
`scripts/run_suite.py:1684` (`subprocess.Popen(cmd, …)` без `shell=True`), `scripts/gate_preflight.py:2636` (`_probe_reporter`,
`subprocess.run([...])`), и ветка `except FileNotFoundError` обеих превращает это в «программы нет на этой машине»
(`refuse_missing_executor`, `{"launcher_missing": True}`; в онбординге — `onboarding_probe.py:390`, состояние `launcher_missing`). Программа на машине
есть — `shutil.which("npx")` находит `npx.cmd` через `PATHEXT`; `CreateProcess` Windows без расширения `.cmd` не запускает. Текст отказа
после этого утверждает неверный факт («not found in this session»).

## Класс

Фабрика запускает команды проекта единообразно и сама отвечает за то, чтобы команда нашлась тем способом, которым её находит ОС (AR-4 —
ничто не привязано к одной машине/раскладке; AR-15 — общая проблема решается в одном месте; FR-17; FR-41 — «не нашёл» из-за способа
запуска не выдаётся за «нет программы»).

## Что именно менять

Направление выбрано: одна функция разрешения запускаемой программы, вызываемая всеми местами, что запускают `argv` проекта.

1. **Новая функция в `scripts/hooklib.py` (или там, где живёт общий запуск — место уточняет спека; в `hooklib.py` уже есть `_EXE_SUFFIXES =
   (".exe", ".cmd", ".bat", ".com", ".ps1")` для разбора команд): `resolve_launcher(argv: list) -> list`.** Для `argv[0]` без пути и без расширения:
   `shutil.which(argv[0])`; нашёлся — возвращается `[<полный путь>] + argv[1:]` (на Windows это `npx.cmd`; `subprocess` запускает `.cmd`-файл
   через `cmd.exe`, список аргументов не склеивается в строку оболочки руками — кавычки не меняются); не нашёлся — `argv` без изменений
   (пусть падает исходной ошибкой с честным текстом). Для `.ps1` — не разрешается (нужен `powershell -File`; дверь в отказе: «перепишите
   команду профиля на `node …`/`pwsh -File …`»). На не-Windows функция возвращает вход как есть. Тест: монкипатч `shutil.which` → `C:\\x\\npx.cmd`;
   вход `["npx","playwright","test"]` → путь + хвост; вход с путём/расширением — без изменений; не-Windows — без изменений.
2. **Подключить во всех местах запуска `argv` проекта:** `scripts/run_suite.py` (основной запуск, строка ~1684 и ветка `--mine`),
   `scripts/gate_preflight.py` (`_probe_reporter`), `scripts/onboarding_probe.py` (проба отчёта), `scripts/runtime_probe.py` и
   `scripts/execution_request.py` (где собирается `argv` запроса) — по `grep` на `subprocess.(run|Popen)` с `argv` проекта; список уточняет
   спека, остальные — записью остатка (FR-54 — найти соседей по карте). Тест: на каждый подключённый запуск — фикстура с `which`, подменённым на
   `.cmd`, запуск идёт.
3. **Текст отказа при `FileNotFoundError` после разрешения** называет, что искали (`PATH`, `PATHEXT`), и дверь: «установите программу /
   поправьте `argv` профиля» (не «нет в этой сессии»). Тест: программа, которой нет в `which`, — прежний отказ с дополненным текстом.
4. **Обход проекта снимается:** живое доказательство (FR-33) — онбординг/запуск на Windows-проекте с `npx` в команде профиля без
   `node scripts/run-playwright.mjs` (FB-3 закрыть записью в проекте; это работа проекта).

## Принципы и правила

P2, P15; FR-1, FR-17, FR-33, FR-41, FR-54; AR-4, AR-15.

Связи: `execution-probes/findings/20261028-playwright-junit-otchet-ne-chitaetsya.md` (EP1-22 — команда Playwright, где `npx` уже упомянут; делать после него:
общие `run_suite.py`, `execution_request.py`, `gate_preflight.py`); `onboarding-hooks` — онбординг, который выдал `launcher_missing`.

Решение владельца нужно: нет.
