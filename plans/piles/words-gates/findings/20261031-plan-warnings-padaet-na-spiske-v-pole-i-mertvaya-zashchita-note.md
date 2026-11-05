# `plan_warnings` падает `TypeError` на строке плана с `impact: ["severe"]`; `getattr(self, "question_lines_note", "")` — мёртвая защита (t-542 F12)

id: — | кучка: `words-gates` | от: критик t-542, F12 (`docs/tasks/specs/reviews/t-542-gate-answers-critic.md`), 31.10.2026 | приоритет: П3 | кандидат наверх: нет

## Что наблюдалось

1. `planning_contract._unearned_e2e` (:248): `row.get("impact") in {"severe", "unknown"}` — множество хэшируемых значений, а значение поля может быть списком: проба критика, `impact: ["severe"]` даёт
   `TypeError: unhashable type: 'list'`. Для самой строки так было и до GW1-29; ветка `if_answered` (`_unearned_branch`) расширила вход: тот же вызов теперь идёт над строкой с наложенной заплаткой, значения которой
   пишет роль. `gate_brief.unearned_automation` (:387) оборачивает вызов в `except Exception: return []` — падение превращается в «предупреждений нет» (молчаливый проход, FR-4/FR-59); на S3-выходе `plan_warnings` зовут без обёртки.
2. `story_run.py:16300`: `getattr(self, "question_lines_note", "")`, хотя атрибут ставится в `__init__` (`:1149`) — защита мёртвая, читателя сбивает с толку (как будто атрибут бывает не задан).

## Что именно менять

1. `planning_contract.py`: `_unearned_e2e` читает закрытые поля через один маленький читатель `_closed(row, key)` — значение берётся, только если оно строка (`str`), иначе `None`
   (список, число, словарь — «не сказано»); сравнение идёт по нему. Ошибка в безопасную сторону: нечитаемое поле НЕ доказывает «высокий риск», строка получает предупреждение (FR-59). Исключение наружу не вылетает.
2. `gate_brief.unearned_automation`: `except Exception: return []` остаётся, но строка вида «the plan warnings could not be read (<тип>)» добавляется в `missing_inputs`/предупреждения карточки (неизвестное не пустой список, FR-41).
3. `story_run.py:16300`: убрать `getattr`, читать `self.question_lines_note` напрямую.
4. Тесты (`scripts/tests/test_plan_warnings_info.py`): строка `automate`/`e2e-ui` с `impact: ["severe"]`, `likelihood: {"x": 1}`, `verification_depth: 3` — `plan_warnings` не падает и даёт предупреждение; та же строка в ветке
   `if_answered`; с `impact: "severe"` предупреждения нет (контроль). Мутация: вернуть `in {…}` на сыром значении — красит первый случай. Пункт 3: тест `Driver` без `getattr` (атрибут задан в конструкторе) не нужен, правка проверяется чтением.

## Принципы и правила

P1, P22; FR-4, FR-41, FR-59; AR-13, AR-28. Связи: GW1-29, t-542 F9–F11.

Решение владельца нужно: нет.
