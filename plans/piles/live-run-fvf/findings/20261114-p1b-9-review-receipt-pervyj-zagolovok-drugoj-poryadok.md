# `_review_receipt` берёт `dispatch` заголовком вперёд, два других вывода — порядком `_form_dispatch`: один порядок на все три (очередь Q-4 вердикта P1B-9)

id: — | кучка: `live-run-fvf` | от: критик темы P1B-9 (`docs/tasks/specs/reviews/20261114-p1b-9-topic-diff-critic.md`, «Queue lines», Q-4; поправка S-2) | приоритет: П3 | кандидат наверх: нет

## Что не так

Класс фабрики: **один факт выводят три функции двумя разными порядками (P31, AR-13)**. `ai-packages/qa-factory/scripts/handoff_check.py` `_review_receipt` (~157-165) определяет
`dispatch` сначала по заголовку, а `_findings_file` и `_runtime_provenance` — через `_form_dispatch(art, doc)` (~172) в порядке form_dispatch, header.dispatch, dispatch.

## Что именно менять

Выбранное направление: один порядок — порядок `_form_dispatch` (form_dispatch, header.dispatch, dispatch); `_review_receipt` берёт `dispatch` через `_form_dispatch`, как два других
(вердикт: «pick one precedence and route all three through S-2's helper»). Инвариант позиции: форма, у которой `form_dispatch` и заголовок называют разные значения, не должна молча читать чужую запись —
расхождение остаётся видимым в тесте, а не исчезает.

1. `ai-packages/qa-factory/scripts/handoff_check.py` (`_review_receipt`): `dispatch` из `_form_dispatch`.
2. `ai-packages/qa-factory/scripts/tests/test_handoff.py`: строки таблицы — форма только с заголовком; только с `form_dispatch`; с обоими, значения разные (порядок `_form_dispatch`); без обоих.

Принципы и правила: AR-13; P31.

Связи: `findings/20261114-p1b-9-rolevoj-provenance-ne-sveryaetsya-s-zapisyu-okna.md` (тот же файл).

Решение владельца нужно: нет.
