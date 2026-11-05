# `calibration_counts`: `rejected` с `"agent": null` (или `failure_class`/`model` null) роняет отчёт `TypeError` в сортировке

id: — | кучка: `forge` | от: билдер t-646 / критик t-648, 09.10 | приоритет: П2 | кандидат наверх: нет

Что не так / что сделать: `tools/calibration_counts.py` :479-493 (после D10 — внутри `_rejected_distribution`): две строки
`rejected` с одинаковым `failure_class`, у одной `"agent": null` (или `"failure_class": null`) → `sorted(...)` падает с
`TypeError: '<' not supported between instances of 'str' and 'NoneType'`; одиночная null-строка не падает. Причина:
`.get(f, "<none>")` не покрывает ключ, присутствующий со значением null; `_rule6` (:271) нормализует агента, остальные
секции — нет. Дефект существовал до узла B-426 D10 (чистый перенос поведение не менял; теперь исключение возникает в
секции 8, а не при сборке словаря — всё равно до любого вывода). Что сделать: `v if isinstance(v, str) else "<none>"` для
трёх ключей (failure_class, agent, model) + тест на две null-строки; та же находка несёт второй дефект того же файла:
`_false_accept` обходит `set(...)`, и порядок ключей сырого JSON зависит от `PYTHONHASHSEED` (скрыто `sort_keys`, но мешает
диффу сырого вывода) — обойти `sorted(set(...))`. Соседи по классу «длинные функции» в том же файле (не в списке B-426):
`render_text` 97 строк, `main` 73 — кандидаты на тот же приём.

Свидетель: отчёт `docs/tasks/specs/reports/t-646-builder-report.md` (найдено при сборке фикстуры); вердикт
`docs/tasks/specs/reviews/t-648-b-426-wave-2a.md` (F-7: проба критика — TypeError в обоих случаях, одиночная null-строка ок).

Принципы и правила: FR-31/FR-32 (корень + тест), правило 9 CLAUDE.md (класс: `.get(k, default)` при присутствующем null);
ось 11 SIBLING_MAP (читатели журнала).

Решение владельца нужно: нет.
