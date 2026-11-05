# Путь `handoff:` в диспатче не сверен ни с ролью, ни с изоляцией: отчёт критика отбит `handoff_gate`, отчёты worktree-билдеров и скаутов Lead собирает руками

id: — | кучка: `onboarding-forge` | от: Lead пачки hotfix-12586/1 (dev2), 23.10.2026 | приоритет: П2 | кандидат наверх: нет

Что не так: строка `handoff:` диспатча называет файл, который воркер пишет сам (`tools/handoff_gate.py`, спека t-744). Но путь выбирает Lead по памяти, и два
класса промахов повторяются в одной пачке (hotfix-12586/1):

(1) Папка не той роли. `tools/dispatch_manifest.py:138-143` держит данные `HANDOFF_DIRS` (critic → `docs/tasks/specs/reviews`, designer → `docs/tasks/specs`,
builder → `docs/tasks/handoffs`, scout → `docs/tasks/specs/reports`); их читают `handoff_gate` (на записи) и `agent_budget` (кого пустить в папки), но НЕ проверка
манифеста до запуска: `dispatch_manifest.py` проверяет наличие строки `handoff:`, не соответствие её папки роли. Диспатч критика t-048 назвал `docs/tasks/handoffs`;
Write критика отказал `handoff_gate`, и отчёт Lead сохранил из ответа сам (шапка `docs/tasks/specs/reviews/t-048-hf1-0-hotfix-review.md`: «a spec defect of the dispatch,
R11-h»).

(2) Путь в главном чекауте, который воркер не может записать. Билдеры в `isolation: "worktree"` не пишут в главный чекаут: отчёт t-053 («the Write tool refused the
main-checkout path (worktree isolation). The Lead copies it»), t-055, t-056, t-058 («Saved by the Lead from the builder's handback, verbatim: the worktree isolation refused the builder's
Write to this path»), t-054 (отчёт «сохранён Lead», Ход 23.10 14:1x). Скаут записи не имеет вовсе: его итоговое сообщение и есть отчёт (docstring `handoff_gate.py`), так что
`handoff:` на `docs/tasks/specs/reports/…` для скаута — цель, которую Lead заполняет. Отчёты t-053…t-058 доехали до главного чекаута копированием Lead: ход, который
шаблон диспатча мог бы назвать заранее.

Что сделать: (а) `dispatch_manifest.py` при наличии роли (`subagent_type` / строки роли в диспатче) сверяет папку `handoff:` с `HANDOFF_DIRS[роль]` и называет ожидаемую
папку (FR-1) — до запуска, а не отказом на записи; (б) для `isolation: "worktree"` шаблон диспатча билдера даёт путь отчёта ВНУТРИ worktree (относительный путь в той же
папке `docs/tasks/handoffs`), по которому `handoff_gate` и так сравнивает по хвосту сегментов, а Lead при слиянии забирает файл вместе с веткой; (в) для скаута
шаблон не называет пишущий `handoff:`, а говорит «отчёт — ответом; Lead сохранит в `docs/tasks/specs/reports/…`». Тест: `tools/test_dispatch_manifest*.py` — критик с
`handoff:` в `docs/tasks/handoffs/` получает отказ с именем верной папки; прежний отрицательный контроль — критик с верной папкой проходит.

Свидетель: `docs/tasks/specs/reviews/t-048-hf1-0-hotfix-review.md` (шапка); `docs/tasks/handoffs/t-053-hf1-1.md` (шапка), `t-055-hf1-3.md`, `t-056-hf1-4.md`, `t-058-hf1-6.md`
(первая строка); `tools/dispatch_manifest.py:138-143`; `tools/handoff_gate.py` (docstring: «scout (has no Write: its final message is the report)»; порядок 6: сравнение по хвосту
сегментов). Контроль отсутствия: поиск `HANDOFF_DIRS` по `tools/*.py` вне тестов находит определение (`dispatch_manifest.py:138`), читателя `agent_budget.py:122` и читателя `handoff_gate.py:145`;
проверки в самом манифесте среди них нет.

Принципы и правила: правило 11 `CLAUDE.md`, строки R11-f и R11-h; P15; FR-1, FR-2.

Решение владельца нужно: нет.
