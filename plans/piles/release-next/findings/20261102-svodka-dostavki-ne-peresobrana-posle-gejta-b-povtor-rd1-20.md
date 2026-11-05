# Сводка доставки и ledger не пересобраны после гейта B: `delivery-summary.md` говорит «1 с багом, 21 не доказано», финальный отчёт — «4 с багом, 19 не доказано» (регрессия узла RD1-20)

id: — | кучка: `release-next` | от: прогон LOCAL-1, разбор t-1672 П-17 (МАЛАЯ), 02.11.2026 | приоритет: П2 | кандидат наверх: нет

Сокращения: `A` = `mybooks-stand/test-automation-framework/qa-factory/artifacts/LOCAL-1`; `T` = транскрипт дирижёра.
Разбор: `docs/tasks/specs/reviews/t-1672-local-1-whole-run.md` (П-17).

## Что наблюдалось

- `A/work/delivery-summary.md:173` (mtime 10:51): «qty-invalid-input-coerced: a draft, not chosen so far», «1 with a product bug, 21 not proven». Финальный `A/test-report.md:6` (11:20): «4 with a product bug, 19 not proven», «BUG-1 … in an unfiled draft». `A/work/ledger.md` — версия 10:50–10:51.
- S9 сначала отказал: «report has no `gate-b` block» (`T` L3347).
- Узел RD1-20 (0.10.8, «принято, слито»; `report-delivery/findings/20261031-chisla-otcheta-ne-shodyatsya-svodka-ustarela.md`) обещал «сводка не старше отчёта». Здесь она старше: регрессия/не починено: RD1-20.

## Причина

Производные артефакты (`delivery-summary.md`, `ledger.md`) пересобираются на S8 до гейта B; после ответа гейта B пересобирается только `test-report.md` (`scripts/story_run.py` `rebuild_report`, `:3021`, `refresh_after_reporter`, `:12559`). Проверка RD1-20 «сводка не старше отчёта» не покрывает порядок «после слов гейта B».

## Класс

Производный артефакт после изменения источника пересобирается вместе с отчётом, иначе два артефакта расходятся (FR-25, FR-37; AR-22). Фабричный класс.

## Что именно менять

Направление выбрано (Lead, 02.11.2026).

1. **Один порядок пересборки.** `scripts/story_run.py` `rebuild_report` (`:3021`): после слов гейта B пересобирает в одном вызове `ledger.md`, `delivery-summary.md` и `test-report.md` (`scripts/delivery_summary.py` `build`, `:224`). Тест: слово гейта B «завести баг» → `delivery-summary.md` и отчёт называют одинаковое число багов.
2. **Сторож устаревания.** `scripts/delivery_summary.py` (рядом `left_with_you_stale`, `:205`): сводка, чья mtime раньше записи гейта B, считается устаревшей — S9 не принимает её. Тест: сводка раньше гейта B → отказ с дверью «пересобрать».
3. **Сверка с проверкой RD1-20.** Тест RD1-20 («сводка не старше отчёта») расширяется кейсом «слово гейта B пришло после сборки сводки».

## Принципы и правила

P18, P21; FR-25, FR-37; AR-22.

## Связи

- RD1-20 (регрессия), RN1-23 (причины в блоке product, тот же `delivery-summary.md`).
- Разбор t-1672 П-17.

Решение владельца нужно: нет.
