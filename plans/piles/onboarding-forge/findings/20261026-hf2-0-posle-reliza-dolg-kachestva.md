# Критик HF2-0: список «после релиза» — дубли, читатели номера Then, длинные функции, лгущие комментарии, рубрика автомата

id: — | кучка: `onboarding-forge` | от: критик HF2-0 (t-138), решение Lead 26.10.2026 | приоритет: П3 | кандидат наверх: нет

Что не так / что сделать: вердикт `docs/tasks/specs/reviews/t-138-hf2-wave1-review.md` (п. 1(b), 1(c), 2, 3, 4) оставил после релиза список, который не блокирует слияние. Одна находка на пачку 3, строки по классам:

1. Четыре написания `contradicts_requirement` появились в волне 1: `acceptance.py:533`, `contract.py:3427`, `controller.py:122`, `story_step.py:1146`. Что сделать: импорт из `contract`, одно написание (тест держит их равными, но это не носитель).
2. У автоматора нет `code-review-rubric.md` ни в срезах, ни в тексте роли (FR-15, FR-38): он не видит трёх условий санкционированного пути (dim 8, `code-review-rubric.md:58-62`). Что сделать: дать путь в срезы и текст роли; стоит один круг критика.
3. Читатели номера Then вне носителя `contract.then_number` (остаток HF2-2): `manifest_from_tests.py:1115-1116` (`int(b["then"])` читает теперь и строки, присланные рукой) и `ledger.py:412` (`isinstance(..., int)`).
4. `SETTLED_STATUSES` дважды: `question_register.py:85` и `planning_contract.py:838`.
5. Текст блока «stand not confirmed» собран дважды: `story_run.py:8718-8719` и `:10139-10140` (сосед по оси 26).
6. Читатели раздела приложения дважды: `validate_artifacts.py:1090` и `report_facts._section_span`; константа `APPENDIX_HEADING` рядом с литералом `report_facts.py:78` (две строки очереди t-125).
7. Длинные функции, целиком новые: `acceptance.red_by_requirement` (115 строк, около 30 — докстринг), `planning_contract._apply_recorded` (79), `execution_request._observe_stand` (71), `s5_precheck._check_blocked_then` (64). Выросшие и без того длинные: `build_mine_request` (584), `manifest_from_tests.build` (307), `window_record.build` (268), `validate_window` (176), `plan_row_state` (174), `stage_S6` (88).
8. Лгущие комментарии: `s5_precheck.py:2051` («or two running» — такой логики в `dispatch_scope` нет) и `<!-- wave 2: plan critic -->` в `agents/qa-code-critic.md` (волна 2 перенесена в пачку 3).
9. Наблюдение FR-31: `PermissionError [WinError 5]` в `execution_request.py:386` (`os.replace`) под нагрузкой канона (`test_ledger`, первый запуск; повтор 328/328) — разовое падение теста Windows, код не из волны.

Свидетель: вердикт `docs/tasks/specs/reviews/t-138-hf2-wave1-review.md` (разделы 1–4 и TRAIL; перепрогоны и пробы в скретче критика).

Принципы и правила: FR-54, FR-13, FR-15, FR-38, FR-31, AR-13; DUPLICATION и CODE QUALITY из `docs/tasks/critic-diff-brief.md`.

Решение владельца нужно: нет.
