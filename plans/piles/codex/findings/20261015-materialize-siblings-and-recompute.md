# После `story_step materialize`: диспетчи, регистрируемые мимо `start`, и перерасчёт input_hash для пакета без rework

id: — | кучка: `codex` | от: Dev2 (прогон TP2-2406 S3-3, Codex Desktop), 15.10.2026 | приоритет: П2 | кандидат наверх: нет

Что не так / что сделать: t-021/t-022/t-023 добавили `story_step.py materialize --task <T> --dispatch-id <ID>` — бриф,
форма хэндоффа и карточка запуска строятся из закоммиченного пакета диспетча (запись + событие `dispatch:<ID>`), без
`prepare`/`apply`, идемпотентно (диагноз `docs/tasks/specs/reviews/t-021-s3-rework-materialization-diagnosis.md`,
вердикт `t-022-materialize-review.md`). Остаток по оси SIBLING_MAP «Skill phase <-> driver» (B-261) и по вердикту:

- (а) Драйвер `story_run.run_role(rework=…)` (story_run.py:1802-1814) строит бриф и промпт в процессе, но не форму и
  не карточку — вызывать `_write_dispatch_files` (один писатель трёх артефактов).
- (б) Другие диспетчи, регистрируемые мимо `start`: `question_rework` (story_run.py:2231), ручной блок S6 (:6703),
  retry/relaunch-пакеты `recover` — у них тот же разрыв на Desktop-хосте; `materialize` должен их обслуживать, если
  они несут событие `dispatch:<id>` — тест нужен.
- (в) Решение 1 (перерасчёт `input_hash` для пакета БЕЗ `rework_of` через read-only `prepare`, отказ с дверью `release`
  при расхождении) — отдельный узел с критиком на план (PROJECT.md п. 6: меняет смысл гейта): хэш `prepare`
  покрывает test-plan.json/manifest/bundle, которые сама стадия переписывает (на S3-3 он ушёл с b78a… на b461… после
  S3-2), так что отказ на любое расхождение заблокирует пакеты start-crash/retry, которым эта дверь служит; нужна спека,
  какие пакеты приходят без `rework_of`.
- (г) `brief_pack` печатает `Scope: TP2-2406` для пакета со скоупом `[]` (откат к скоупу стори — на этом стенде
  рукописный ключ тикета): класс t-018 (`20261015-scope-ticket-key-and-tc005-question.md`).
- (д) `s0.md:109`, `s7.md:152`, `controller-api.md:59` упоминают `--operation rework` без шага materialize — в рантайме
  дверь доходит через `next` результата CLI; текст — при следующей правке этих файлов (controller-api.md на пределе
  12000 байт).

Свидетель: стенд rev 71 — `state/events.jsonl` seq 71 (`dispatch:S3-qa-test-strategist-3`, input_hash b78a7144…,
plan_rows TS-1/2/3/4/8, rework_of S3-2), `work/briefs/` без S3-3 до materialize; роллаут 15.10 09:28 строка 320
(`start --id S3-qa-test-strategist-3` → «idempotency key reused with different inputs»); копия: materialize run 1/run 2
(хэши controller.json df28e0ec… и events.jsonl b4aeb39d… без изменений).

Принципы и правила: P1, P10, FR-1, FR-15, FR-37, FR-40, FR-49, FR-54, FR-59.

Решение владельца нужно: нет.
перенесено из ветки dev2/codex-overhead-fixes (plans/piles/driver-controller/findings/20261015-materialize-siblings-and-recompute.md), узел: CX1-14
