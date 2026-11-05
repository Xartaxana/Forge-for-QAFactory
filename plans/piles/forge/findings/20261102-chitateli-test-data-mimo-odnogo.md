# Блок `test_data` проекта читают напрямую двое в обход единственного читателя `config_contract.test_data_states`

id: — | кучка: `forge` | от: критик t-724 (TQ1-11, Q6 и m-2), 02.11.2026 | приоритет: П3 | кандидат наверх: нет

## Что наблюдалось

После TQ1-11 блок `test_data` конфига проекта читает одна функция `config_contract.test_data_states` (`config_contract.py:604-641`; её зовут `brief_pack._approach_test_data` и `judge_code.test_data_for_judge`). Прямые читатели мимо неё — поиск `test_data` без учёта регистра по `ai-packages/qa-factory/scripts/*.py` (контроль: тот же вызов находит `brief_pack.py:2502` и `judge_code.py:216`):

- `env_probe.py:603` — `data_cleanup` (строки 588-612) со своей константой `CLEANUP_UNKNOWN` (`:589`);
- `audit_factory.py:766` — полнота темы 3 онбординга.

Не читатели: `manual_capture.py:675` (текст), `repo_map.py:64` (имя каталога), `gate_preflight.py:587` (имя файла). Очередь жила только в `docs/tasks/handoffs/t-708-*`; в пачке и в `docs/SIBLING_MAP.md` строки нет.

## Класс

Факт проекта, у которого есть функция-читатель, читается только через неё (AR-13; FR-17): два «неизвестных» кортежа (`config_contract.TEST_DATA_UNKNOWN` и `env_probe.CLEANUP_UNKNOWN`) могут разойтись, и тогда один и тот же ключ для одной роли «не записан», а для пробы — «известен».

## Что именно менять

Направление выбрано (Lead пачки release-next/1, 02.11.2026).

1. `scripts/env_probe.py`, `data_cleanup`: состояние ключа берётся из `config_contract.test_data_states(config)`; локальная `CLEANUP_UNKNOWN` удалена, вместо неё `config_contract.TEST_DATA_UNKNOWN`. Ожидание: `data_cleanup` на конфиге без блока, с блоком `none` и с `recorded` возвращает то же, что вчера. Тест: существующий тест `env_probe` без правки ожиданий + строка «блок отсутствует».
2. `scripts/audit_factory.py:766`: проверка полноты темы 3 читает ключи через `test_data_states` (статус `recorded` / иной), а не `config["test_data"]` напрямую. Тест: `test_audit_*` с шаблоном и с конфигом без блока.
3. Ключ против возврата: тест в `scripts/tests/` — поиск по `scripts/*.py` (кроме `config_contract.py` и тестов) не находит `["test_data"]` и `.get("test_data"` (положительный контроль — сама `config_contract.py`).
4. `docs/SIBLING_MAP.md`: строки оси «`test_data` → `test_data_states`» и «бриф называет записанное знание проекта по пути» вносит Lead.
5. Попутно (m-4 того же вердикта): строка документов стратегии `brief_pack.py:2521` берёт `RP.home_dir(project) / "strategy"`, а не литерал `project / "qa-factory" / "strategy"`. Тест: существующий `test_project_approach`.

## Принципы и правила

FR-17; AR-13, AR-22.

## Связи

- `docs/tasks/specs/reviews/t-724-tq1-11-diff-critic.md` (Q6, m-2, m-4).

Решение владельца нужно: нет.
