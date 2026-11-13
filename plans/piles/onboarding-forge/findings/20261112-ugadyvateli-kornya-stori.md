# Угадыватели корня стори: `source_exclusions`, `stand_identity`, `story_step`, `archive_task`, `external_writes` и другие определяют проект или корень стори по форме пути

id: — | кучка: `onboarding-forge` | от: отчёт билдера t-165 (узел OF3-1 d; слова Lead 12.11.2026, снимок `docs/tasks/compact-snapshots/2026-11-12-2032-narrative.md`, строка «угадыватели корня стори»), 12.11.2026 | приоритет: П3 | кандидат наверх: нет

**источник не найден:** отчёт билдера t-165 как файл не лежит ни в `docs/tasks/specs/reviews/`, ни в `docs/tasks/specs/reports/`, ни в журнале (`logs/journal/dev1.jsonl`: t-165 — только события delegated/rejected/accepted, перечня угадывателей нет).
Искал: `grep t-165` по журналу (находит 4 события — положительный контроль), `grep -rl "story_step.*archive_task"` по `docs/` и `plans/` (находит только снимок), чтение перечисленных файлов на main (ниже). Перечень «и другие» восстановить без отчёта нельзя.

## Что наблюдалось (проверено по main)

- `scripts/source_exclusions.py` `_task_root` (:586-588) уже идёт через `hooklib.story_root(task, "--task")` — по форме пути не угадывает.
- `scripts/stand_identity.py` `_project()` (:640-642) берёт `hooklib.project_root()` — корень процесса, не корень стори.
- `scripts/story_step.py` `_project_rel` (:314), `scripts/archive_task.py` (:311-333) и `scripts/external_writes.py` (:1056-1373) — строки `proj / "qa-factory" / "artifacts" / <T>` стоят в самопроверках (`QA-9`, `QATF-*`), не в боевом коде.
- Боевые угадыватели «корень стори = `task_root.parents[2]`» по main найдены в `walk_timing.py:172, :241` и `gate_brief.py:2303` (отдельная находка `20261112-put-stori-k-proektu-po-glubine.md`).

## Что именно менять

**Вопрос владельцу / Lead пачки.** Какие места имел в виду отчёт t-165? Нужен перечень «файл:строка» (из отчёта билдера; Lead его держит). Рекомендация, до слова владельца: Lead передаёт отчёт t-165 в `docs/tasks/specs/reports/t-165-story-root-guessers.md`, и этот узел превращается в «каждое место из отчёта идёт через `runtime_paths.project_for_task` / `hooklib.story_root`» с таблицей случаев (корень артефактов по умолчанию / настроенный) на место. Пока перечня нет — узел исполним только как «scout: перечень по `.parents[`, `parent.parent`, `"artifacts"` в `scripts/*.py` без тестов»; результат — файл отчёта, не код.

Принципы и правила: P2, P31; AR-4, AR-13, AR-15.

Решение владельца нужно: да (источник).
