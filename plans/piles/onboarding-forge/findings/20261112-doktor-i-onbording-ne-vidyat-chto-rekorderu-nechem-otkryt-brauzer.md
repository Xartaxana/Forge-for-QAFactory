# Доктор говорит «установка здорова», онбординг — «ничего не ставится», а рекордеру фабрики нечем открыть браузер

id: — | кучка: `onboarding-forge` | от: подготовка плеча `factory` прогона LR2-1 на новой машине, релиз 0.11.0, 12.11.2026 (слово владельца: «заводи находки») | приоритет: П2 | кандидат наверх: нет

## Что не так

На машине не было Python-пакета `playwright`: `python -c "import playwright"` → `ModuleNotFoundError`. Рекордер ручных кейсов
(`scripts/manual_capture.py`, `PlaywrightBackend.__init__`, `from playwright.sync_api import sync_playwright`) без него не открывает
браузер (`BrowserUnavailable`; дверь `browser_door` в `references/manual-capture-steps.json`: «python -m pip install playwright, then
python -m playwright install chromium»).

- `/qa-factory:qa-doctor` до онбординга: «The install is healthy».
- Сводка онбординга, раздел 3: «Nothing is installed. `npm ci` and the Playwright browsers stay as they are».
- `qa-factory/state/readiness.json` после онбординга: слово `playwright` встречается только как профиль тестов проекта
  (`playwright-tests`); о браузере рекордера — ни строки.

Проект — веб-приложение с UI-входом, который онбординг сам записал рецептом рекордера (`manual_capture.login.ui`), то есть ручные
проходы по UI заведомо будут. О том, что их нечем исполнить, человек узнал бы посреди первой стори (гейт A или S6), а не на установке.

Класс: зависимость собственного инструмента фабрики не проверяется там, где проверяется установка (FR-17: проба есть — в
`gate_preflight.py`, ловит `MC.BrowserUnavailable`, — но не подключена к доктору и готовности); неизвестное подано как «здорово» (FR-41).

Свидетель: `experiments/mybooks/factory-vs-free-agent/notebook.md`, раздел «Условия 4–7 и репетиция» (проба запуска после установки:
«launch: Bookstore», «persistent: Bookstore»).

## Что сделать

Готовность называет, может ли рекордер открыть браузер, сразу после онбординга проекта, у которого есть UI-поверхность; доктор
печатает строку с дверью установки.

## Что именно менять (направление выбрано Lead 12.11.2026; владелец может отменить словом)

1. `scripts/readiness.py`: строка готовности `manual_capture.browser` со значениями `ready` / `unavailable` / `not_needed` — проба та же,
   что в `gate_preflight.py` (одна функция, AR-15: вынести существующую пробу, а не написать вторую); `not_needed` — когда в
   `config.json` нет UI-поверхности (нет `manual_capture.login.ui` и нет профиля с браузером).
2. `skills/qa-doctor/SKILL.md` и раздел 3 сводки `skills/qa-onboarding/phases/p3-summary-gate.md`: при `unavailable` — одна строка
   человеку с дверью из `references/manual-capture-steps.json` (`browser_door`), владелец — человек (установка на его машину — его
   решение; онбординг ставит только то, что покрыто одобрением, инвариант «Dependencies are activated on demand»).
3. Проба различает «пакета нет» и «пакет есть, браузер не запускается» (второе — текст ошибки запуска, дословно).
4. Тест: готовность на фикстуре без пакета даёт `unavailable` с дверью; на проекте без UI-поверхности — `not_needed`.

Связи: `execution-probes` (находка «стенд без Docker: ручная проверка не спрашивает версию»), OH3-6 (доктор и шаги человеку).
Принципы и правила: P5, P22; FR-17, FR-41, FR-50; AR-15, AR-28.

Решение владельца нужно: нет.
