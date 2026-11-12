# `app_card.py:247` читает `test_data` мимо читателя; `execution_scheduler._project_parallel_defaults` читает конфиг прямым `utf-8`

id: — | кучка: `onboarding-forge` | от: критик OF3-1 c, `docs/tasks/specs/reviews/t-190-of3-1c-diff.md` (очередь Q3, Q4), 12.11.2026 | приоритет: П3 | кандидат наверх: нет

Вердикты по этим двум местам даст перепись `docs/tasks/t-183-of3-1c-config-census.md` (ветка `wip/of3-1c`, пишется сейчас): перед правкой узел сверяется с ней, а не повторяет поиск.

## Что наблюдалось (проверено на main)

1. Q3. `scripts/app_card.py:247-262`: `data = cfg.get("test_data") if isinstance(cfg, dict) else None`, далее `data.items()` — мимо `config_contract.test_data_states` (AR-13) и с выводом сырых значений (ключ `unknown` выглядит значением). Критик: в спеке и в находке forge `plans/piles/forge/findings/20261102-chitateli-test-data-mimo-odnogo.md` его нет (поиск «app_card» — пусто); псевдоним `data = cfg.get("test_data")` — тот класс, который сканер R2 не видит.
2. Q4. `scripts/execution_scheduler.py:226-233` `_project_parallel_defaults`: `json.loads(path.read_text(encoding="utf-8"))` (:230) — не `utf-8-sig`: конфиг с BOM молча даёт параметры по умолчанию, хотя `artifact_root` в том же прогоне читается той же файлом нормально; список вместо объекта — `effective_config` на `AttributeError`, который не ловится (ловятся `OSError`, `JSONDecodeError`, `ValueError`).

## Что именно менять

1. `scripts/app_card.py` (:247): читать через `config_contract.test_data_states`; ключ в состоянии `unknown` называется «не задан», а не печатается значением.
2. `scripts/execution_scheduler.py` `_project_parallel_defaults`: чтение через `config_contract.read_config_file` (BOM, нечитаемое → ход по умолчанию, объявленный в тексте функции); в `except` добавить `AttributeError`.
3. Тест: `scripts/tests/test_app_card*.py` — `test_data` с `unknown` не печатается значением; `scripts/tests/test_execution_scheduler*.py` — конфиг с BOM и конфиг-список: параметры не по умолчанию / не traceback.
4. Если перепись узла c даст место в N-r4 (`очередь` — узел N-r4 очереди OF3-1 §7), второй пункт делается там, а здесь снимается.

Принципы и правила: AR-13, AR-16, AR-28.

Решение владельца нужно: нет.
