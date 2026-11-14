# `told_from` — третья копия разбора среза JSON `json.loads(out[out.index("{"):out.rindex("}") + 1])`

id: — | кучка: `live-run-fvf` | от: критик темы FV1-9 хвост (t-747), `docs/tasks/specs/reviews/20261114-fv1-9-tail-diff-critic.md` (строка очереди Q1; вне owns карточки A; в вердикте пометка `перенос: code-quality node P7 of spec §5`, `подтвердил: —`) | приоритет: П3 | кандидат наверх: нет

## Что не так

Класс фабрики: **один разбор вывода подпроцесса написан в трёх местах** (FR-54, AR-13, AR-15).
`told_from` (`ai-packages/qa-factory/scripts/driver_dispatch.py`) — третья копия среза `json.loads(out[out.index("{"):out.rindex("}") + 1])`; две другие — `driver_gates.py:331`
(`rehearse`, `gate_preflight`) и `driver_machine.py:1706`.

## Что именно менять

1. Одно место разбора: две другие копии зовут `told_from` (вердикт: «сходятся на `told_from` либо на нейтральном помощнике»; из двух вариантов выбран первый, `told_from` как выживший, —
   выбор помечен, Lead может сменить на нейтральный помощник). Файлы: `ai-packages/qa-factory/scripts/driver_dispatch.py`, `ai-packages/qa-factory/scripts/driver_gates.py` (`rehearse`),
   `ai-packages/qa-factory/scripts/driver_machine.py` (около `:1706`).
2. Поведение при мусоре неизменно: вывод без `{`/`}` или не JSON — как у каждой копии сегодня (исполнитель сверяет три сайта и называет расхождение в отчёте, если оно есть).
3. Тест: строка таблицы в `ai-packages/qa-factory/scripts/tests/test_gate_question_form.py` (или в файле, судящем `rehearse`): один и тот же вывод с хвостом даёт один результат у всех трёх зовущих.
4. Порядок: после слияния хвоста FV1-9 (карточка A), потому что `driver_dispatch.py` и `driver_gates.py` в её owns.

Принципы и правила: FR-54; AR-13, AR-15.

Решение владельца нужно: нет.
