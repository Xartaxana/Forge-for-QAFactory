# `row_field_gaps` требует `obligation_hash` у ссылок на обязательства, а контракт и `manifest_put.py` хеш от роли отказывают (бывшая метка `P1B-2f`)

id: — | кучка: `live-run-fvf` | от: отчёт узла N2f сухой стори (`docs/tasks/specs/reports/20261114-p1b-n2f-report.md` на ветке `wip/p1b-n4m`, «Factory gap candidates» № 8; вопрос Q3); метка `P1B-2f` в `ai-packages/qa-factory/scripts/tests/fixtures/form-rounds.json:70` (ветка `wip/p1b-n4m`) | приоритет: П1 | кандидат наверх: нет

## Что не так

Класс фабрики: **читатель требует форму поля, которую контракт запрещает роли произвести (AR-22, FR-11; тот же класс, что `findings/20261114-row-field-gaps-i-kontrakt-rashodyatsya-ob-obligation-hash.md`, FV2-71, но на другой строке и с измеренным проявлением в сухой истории)**.

- Источник: отчёт N2f, «Factory gap candidates» № 8: `window_record.row_field_gaps` без карты плана судит ссылки через `contract.obligation_ref_problems` (`hash_required=True`) и отказывает ссылки только с id: «has no obligation_hash (missing hash)»; при этом `artifact-contract-automation.md` и `manifest_put.py` отказывают хеш, который шлёт роль. Читатель и контракт расходятся на строке до штампа кода.
- Следствие в сухой истории: заполнитель формы S5 пишет `obligation_refs` только id, без хеша (по контракту); читатель красит строку. Расхождение записано красной строкой реестра `form-rounds.json` на ветке `wip/p1b-n4m` (`obligation_refs <- manifest_row@all -> window_record.row_field_gaps`, узел `P1B-2f`; ожидание `test_field_producers.py` — без хеша).
- Метка `P1B-2f` не имеет файла находки и строки пачки: этот файл — её носитель; узел — FV3-18.

source not found: отчёт N2f `20261114-p1b-n2f-report.md` и строка `form-rounds.json:70` лежат только на ветке `wip/p1b-n4m` (дерево `.claude/worktrees/p1b-n4m`), на `main` их нет; текст строки реестра приведён по отчёту (Q3), номер строки — по спеке `docs/tasks/specs/20261117-p1b-finish-spec.md` §2.

## Что именно менять

Выбранное направление (Lead, 17.11.2026, F-P19 (а)): находка заводится узлом FV3-18; метка `P1B-2f` остаётся на строке реестра до узла и называет FV3-18; разбор — «какая сторона следует за какой».

1. Разбор (Lead → builder): по контракту `ai-packages/qa-factory/references/artifact-contract-automation.md` (~157-167) и `scripts/manifest_put.py` хеш пишет код, роль его не шлёт; значит `scripts/window_record.py::row_field_gaps` не должен требовать хеш у ссылок, выданных ролью (`contract.obligation_ref_problems` вызывается с `hash_required=True` — читать вызов и выбрать `hash_required` по происхождению ссылок); либо обратное — контракт и `manifest_put.py` принимают хеш. Выбор — по измерению на реальных артефактах (см. FV2-71, п. 1: одна команда, результат в спеке).
2. После исправления сторона сухой истории: строка `P1B-2f` в `form-rounds.json` удаляется тем же узлом (иначе `test_field_producers.py` краснеет «stale»); ожидание `obligation_refs` без хеша остаётся.
3. Тест — строка таблицы `scripts/tests/test_window_record.py` (если файл не быстрый — меньший, называет дизайнер): ссылки только id без карты плана; ссылки с хешем; пустые ссылки.
4. Узел пересекается с FV2-71 (`window_record.py`, `acceptance.py`, `artifact-contract-automation.md`): исполнитель читает обе находки; общие файлы — списки функций в `owns`.

Принципы и правила: AR-22, AR-13, FR-11; PROJECT.md п. 6а (смысл поля меняется — критик на план до кода).

Решение владельца нужно: нет.
