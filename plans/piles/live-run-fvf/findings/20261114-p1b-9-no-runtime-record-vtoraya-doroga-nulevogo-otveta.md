# Условие `no_runtime_record` рядом с записью ответа пробы — вторая дорога для нулевого ответа (очередь L-6 плана P1B-9)

id: — | кучка: `live-run-fvf` | от: план-критик P1B-9 (`docs/tasks/specs/reviews/20261114-p1b-9-plan-critic.md`, K5 «Reserved `no_runtime_record`», поправка S5; правило 19) | приоритет: П3 | кандидат наверх: нет

## Что не так

Класс фабрики: **две дороги для одного нулевого ответа (P31, AR-25)**. `ai-packages/qa-factory/scripts/null_outcomes.py:164`: `"no_runtime_record": Condition({}, "evidence/runtime-provenance-*.json", (), "N2/N3", "reserved", None, False)` —
строка реестра, которую ничто не вычисляет (зарезервирована, владелец t-305 N2). После P1B-9 «нет файла» может значить только «проба не запускалась», а это уже `no_run_in_dispatch` (`null_outcomes.py:165`).
Если N2 когда-нибудь построит `no_runtime_record` для трёх носителей, нулевой ответ получит две дороги: пустое поле под заявлением или запись на диске.

## Что именно менять

Выбранное направление: УЗЕЛ с владельцем, не «сообщить» — условие `no_runtime_record` снимается или сужается до «проба не запускалась» и сливается с `no_run_in_dispatch`; выбор между «снять» и «слить» делает дизайнер по списку читателей.

1. Перечислить читателей `no_runtime_record` одной командой чтения (`ai-packages/qa-factory/scripts/`, `references/null-outcomes.json`, `design/`, тесты; контроль того же вида: `no_run_in_dispatch` находится). Результат — в спеке узла.
2. `ai-packages/qa-factory/scripts/null_outcomes.py` (`CONDITIONS`) и `ai-packages/qa-factory/references/null-outcomes.json` (строки того же ключа): снять или слить, читатели переведены в том же коммите (производитель и читатели вместе, AR-22).
3. Тест — строка таблицы `ai-packages/qa-factory/scripts/tests/test_null_outcomes.py` (keep, быстрый): ключа `no_runtime_record` нет (или он псевдоним `no_run_in_dispatch` — как решит дизайнер) и у «никогда не запускали» ровно один исход.
4. Узел идёт ПОСЛЕ слияния плана P1B-9 и после взятия t-305 N2 владельцем (или вместе с ним): условие «Зависит от» заполняет Lead при взятии.

Принципы и правила: P31, AR-25, AR-23; FR-23, FR-40.

Решение владельца нужно: нет.
