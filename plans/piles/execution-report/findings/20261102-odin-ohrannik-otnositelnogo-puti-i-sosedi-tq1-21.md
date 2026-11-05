# Охрана «относительный путь внутри проекта» написана в нескольких местах, у S5-близнеца и у свободного текста её нет

id: — | кучка: `execution-report` | от: критик t-751 (TQ1-21, m-6, B-3), билдер t-754, 02.11.2026 | приоритет: П2 | кандидат наверх: нет

## Что наблюдалось

Носитель — `ai-packages/qa-factory/scripts/`:

- Охранники «путь относительный, любая запись ОС, без диска/корня/`..`»: `planning_contract._textual_problem` (TQ1-21), `source_inventory._safe_rel` (`:2712`, та же логика PurePosix/PureWindows, возвращает bool), шаг «разрешить и удержать внутри» рядом — `red_sandbox.inside` (`:90`), `install_paths._resolve_inside` (`:134`), `runtime_paths.contained` (`:463`). `_safe_rel` не знает одного из случаев `_textual_problem` (проверить сравнением при узле).
- Близнец S3 в S5: `s5_plan._project_file` (`:506-520`) делает `Path(root) / rel` и `_test_path` без защиты от `..` и абсолютного пути.
- Свободный текст: `handoffs/s3-strategist-to-designer.yaml:64` `existing_coverage` — путь прячется в тексте без проверки.
- Третий разделитель `fit`: `traceability.shape_for`, `s5_plan._s3_comparisons` и новый `split_fit` — три разбора одного поля.
- Ось «S3 ↔ S5 разрешение цели» в `docs/SIBLING_MAP.md` отсутствует (поиск `base_test_file|_extends_problem|_test_path` попадает лишь в строку защиты прохода :142).
- Три НОВЫХ межмодульных вызова закрытых имён (дописано в находку `20261027-s5-plan-zovyot-chastnuyu-test-path.md`): `probe_by_code._test_path`, `probe_by_code._profile_cwd` (в `base_test_file` / `_is_folder`) и `handoff_check._checkout_path` (в `_resolve_candidate`).

Очередь жила только в спеке и в `docs/tasks/handoffs/t-754-tq1-21-fix.md`.

## Класс

Один защитный предикат на одно требование «путь внутри проекта» (AR-13, AR-15; FR-17, FR-54): каждая копия защищает по-своему, и копия без защиты (S5-близнец) — дыра в сторону записи/чтения вне проекта.

## Что именно менять

Направление выбрано (Lead пачки release-next/1, 02.11.2026): выживший — `planning_contract._textual_problem` вынести в `scripts/runtime_paths.py` как `relative_problem(text) -> str` (пусто = путь допустим); `contained` остаётся шагом «разрешить и удержать».

1. `scripts/runtime_paths.py`: `relative_problem` с поведением `_textual_problem`; `planning_contract._textual_problem` и `source_inventory._safe_rel` становятся вызовами. Тест: `test_runtime_paths*.py` — `..`, `a/../b`, `/abs`, `C:\x`, `\\srv\x`, пустая строка, `tests/x.py` (допустим), AT и BEYOND нет предела; существующие тесты `test_fit_targets.py` и `test_source_inventory*.py` без правки ожиданий.
2. `scripts/s5_plan.py`, `_project_file` и `_test_path` (через публичный вход): сначала `relative_problem`, затем `contained`; недопустимое — пробел с причиной, не чтение. Тест: цель `../secret.py` и `/etc/passwd` → отказ с причиной; контроль — `tests/x.py` читается.
3. `handoffs/s3-strategist-to-designer.yaml:64` `existing_coverage` — свободный текст, путь внутри него проверить нельзя. Развилка (вопрос Lead; узел исполним по рекомендации до ответа): (а) рекомендация — рядом структурный список путей, проверяемый `relative_problem` в `scripts/planning_contract.py` (пустой список допустим; тест: путь `../x` в списке → находка); (б) оставить текстом и в брифе дизайнера называть его «не проверено». Тест (б): строка брифа присутствует.
4. Три разбора `fit`: `traceability.shape_for` и `s5_plan._s3_comparisons` зовут `planning_contract.split_fit`. Тест: существующие тесты обоих без правки ожиданий.
5. Закрытые имена: `probe_by_code._test_path`/`_profile_cwd` и `handoff_check._checkout_path` — те же узлы, что делают `_test_path` публичной (SC2-16, `execution-report/2`); новые вызовы идут по тому же пути.
6. Ось «S3 ↔ S5 разрешение цели» в `docs/SIBLING_MAP.md` вносит Lead.

## Принципы и правила

FR-17, FR-54; AR-13, AR-15.

## Связи

- `docs/tasks/specs/reviews/t-751-tq1-21-diff-critic.md` (m-6, B-3); `docs/tasks/handoffs/t-754-tq1-21-fix.md`; `plans/piles/execution-report/findings/20261027-s5-plan-zovyot-chastnuyu-test-path.md`; SC2-16.

Решение владельца нужно: нет.
