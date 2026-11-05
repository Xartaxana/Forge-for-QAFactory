# N-4: гард стадии ловит команду доставки в безобидном чтении (`for … in`, `def log(`)

id: — | кучка: `onboarding-hooks` | от: отчёт проекта TP1-14857 (0.10.2), N-4 и дополнение, 27.10.2026 | приоритет: П2 | кандидат наверх: нет

Что не так / что сделать: после Gate B две команды анализа только для чтения — фрагмент Python с `for … in …` и цикл shell `for` с `grep` — заблокированы как «delivery command … from references/adapter-forms.json (gitlab)» при `delivery_ready is not yes`; внутри ранера тот же гард принял `def log(...)` за команду доставки (01:30:59Z). Обход: файлы-скрипты и инструмент Grep. Критерий проекта: гард распознаёт команды доставки по имени инструмента и аргументам, а не по рыхлым подстрокам произвольного shell. Сопутствующее наблюдение: Gate B «deliver with known gaps» записан, но события `deliver_with_risks` в журнале нет, команды доставки остаются заблокированными — согласуется с `s8.md` §4 (событие пишет дирижёр), ничего не доставлено. Код — `scripts/stage_guard.py`, `references/adapter-forms.json` (по классу «токенайзер оболочки», узлы пачки 1 этой кучки).

Свидетель: `docs/tasks/specs/reviews/external-14857-0.10.2/QA-Factory-0.10.2-Defects-for-Dev1.md`, раздел 3.12; `docs/tasks/specs/reviews/external-14857-0.10.2/QA-Factory-0.10.2-Marathon-Addendum-for-Dev1.md`, раздел «Already covered elsewhere».

Принципы и правила: P15, FR-4, FR-12, FR-57, AR-9.

Решение владельца нужно: нет.
