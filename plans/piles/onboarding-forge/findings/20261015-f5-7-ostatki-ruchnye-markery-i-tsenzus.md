# F5-7 — остатки: 43 ручных маркера `{}`, четыре локальных помощника, детектор-ценз, m4–m6 критика t-788

id: — | кучка: `onboarding-forge` | от: критик t-788 (`docs/tasks/specs/reviews/t-788-t-774-f5-7.md`, class_completeness, m4–m7), записал Lead 15.10.2026 09:55 | приоритет: П3 | кандидат наверх: нет

## Что

После слияния forge/5 F5-7 (фикстуры пакетных тестов пишут маркер `qa-factory/config.json` через один помощник
`harness.mark_project`/`temp_project`; 18 файлов переведены, фиксы M1–M3 в t-818) в классе «второй писатель маркера» остаются:

1. **43 файла с ручным `{}`** и **4 файловых помощника** (перечень — отчёт критика t-788, §class_completeness); среди них
   `test_scout_reliability` и `test_story_closed` (`closed_story`) держат копию намеренно — остаются с комментарием.
2. **Детектора нет**: нужен сжимающийся ценз форм ручного маркера (allowlist + cap), по образцу `OUTSIDE_WALKS` в
   `test_runtime_paths.py`.
3. **m4** — неверные ссылки в комментариях `tests/test_judge.py:67`, `tests/test_bug_records.py:194` (и соседи); **m5** — устаревшие
   комментарии (`tests/test_post_commit_refresh.py:177` «no marker, no project» при помощнике, который маркер пишет); **m6** —
   двойные и мёртвые записи маркера у вызовов, переведённых на `temp_project`.
4. Файлы, свободные после слияний conductor/2: `test_check_coverage`, `test_question_branches` (после C2-1), `s5_precheck` (C2-9),
   `handoff` (C2-4), `gate_vocabulary` (C2-5), три непроверенных файла `story_run`; раскладка «корень стори = корень проекта»
   (`dashboard_refresh`).

## Куда

Строка F6-17 пачки `forge/batch-6-vhodyashchie-2.md` (D-0044); ось 8 карты — строка «The fixture marker writer» (Lead, при слиянии).
