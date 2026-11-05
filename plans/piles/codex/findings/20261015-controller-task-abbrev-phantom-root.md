# `controller.py --task <TICKET>` молча становится `--task-root` и работает с пустой фантомной стори

id: — | кучка: `codex` | от: Dev2 (прогон TP2-2406, Codex Desktop), 15.10.2026 | приоритет: П1 | кандидат наверх: нет

Что не так / что сделать: диагноз критика t-020 (`docs/tasks/specs/reviews/t-020-s3-rework-refusal-diagnosis.md`).
Оркестратор вызвал `controller.py --task 'TP2-2406' --operation rework --stage S3 --role qa-test-strategist
--rows TS-1,TS-2,TS-3,TS-4,TS-8 …` (роллаут 15.10 09:28, строка 204, 6 таких вызовов). У контроллера нет опции `--task`,
только `--task-root` (`controller.py:4463`); парсер `argparse.ArgumentParser(__doc__)` (:4462) оставляет
`allow_abbrev=True`, поэтому `--task` принят как сокращение `--task-root`, корнем стал относительный путь
`TP2-2406` от cwd проекта — пустая фантомная стори `C:\Runway202609\nightwing-2406-codex\TP2-2406\`
(папка с 14.10 10:34, неотслеживаемая). Отказ «no accepted qa-test-strategist dispatch on S3 to rework; accepted
roles on S3: none» — предикат :1734-1740 верен, он сканировал `{}`. Нативное «восстановление» (`--task … --operation
recover`, строка 192) прочитало тот же фантом, вернуло revision 0 / S0 с exit 0 и ЗАПИСАЛО туда `state/controller.json`,
`checkpoint.json`, `events.lock` (mtime 15.10 10:08). Настоящая стори (`qa-factory/artifacts/TP2-2406`, rev 70)
нетронута: S3-2 `accepted`, `stage_complete`, не superseded. На копии тот же rework с `--task-root <настоящий корень>`
строит `S3-qa-test-strategist-3` (`rework_of S3-2`, rev 71, S4-8 и critic-1 остаются accepted). Кода для
восстановления прогона не требуется.

Сделать (код, следующий узел):
- (а) `controller.py:4462` — `allow_abbrev=False`, и/или принимать `--task <TICKET>` через существующий резолвер
  (`stand_gaps.resolve_task_root` :1269 / `hooklib.artifacts_dir`), как это делают `waiver.py`, `story_step.py`,
  `stand_gaps.py` (откуда оркестратор и перенёс форму). Тест: `--task <T> --operation next` во временном проекте
  либо резолвится в `qa-factory/artifacts/<T>`, либо отказывает; никуда больше не пишет. Мутация: вернуть сокращения.
- (б) Любая операция, кроме `initialize`, отказывает на корне без `state/events.jsonl`, называя форму `--task-root`
  (FR-59, FR-1): сегодня `recover` создаёт пустую стори и рапортует S0 с exit 0 — поэтому «восстановление» выглядело
  выполненным. Тест: `recover` на пустой папке отказывает, папка остаётся пустой. Мутация: убрать гард.
- (в) Тот же класс: 19 скриптов только с `--task-root` и сокращениями: case_stamp, case_versions, delivery_manifest,
  judge_cases, judge_code, judge_diff, judge_plan, judge_requirements, judge_results, judge_run, manual_capture,
  manual_evidence, migrate_artifacts, red_sandbox, render_case_appendix, s5_precheck, story_progress, story_version,
  tms_publication (ticket_adapter не проверен) — какие из них пишут в фантомный корень: вопрос скауту.
- (г) Фантомная папка `nightwing-2406-codex\TP2-2406\` на стенде — удаляет человек; иначе следующий `--task`
  снова её использует.

Свидетель: роллаут `rollout-2026-10-15T09-28-11-01a13e76…` строки 174/192/204/206; `controller.py:4462-4463`
(`ArgumentParser(__doc__)`, только `--task-root`); фантом `…\TP2-2406\state\controller.json` (rev 0,
dispatches {}, mtime 15.10 10:08); копия: run A (тот же отказ), run B (`--task-root` → S3-3 построен, rev 71).

Принципы и правила: P1, P15, FR-1, FR-15, FR-37, FR-41, FR-59.

Решение владельца нужно: нет.
перенесено из ветки dev2/codex-overhead-fixes (plans/piles/driver-controller/findings/20261015-controller-task-abbrev-phantom-root.md), узел: CX1-10
