# Привязки диспетчей (host-dispatches): два писателя, восемь читателей, и ни одной оси в карте

id: — | кучка: `codex` | от: Dev2 (прогон TP2-2406, Codex Desktop), 13.10.2026 | приоритет: П2 | кандидат наверх: да (ось SIBLING_MAP)

Что не так / что сделать: S3 (12.10) и S4 (13.10) прогона 2406 выходной гейт отработал как `unknown-task` и
аудит чужих багов (BUG-1..3 историй 2530/2534) заблокировал стори, хотя `story_step bind` записал привязку
ребёнка к стори. Причина класса: читатель (`host_dispatch.enrich`) требовал поле `parent_session_id`, которое
писатель `story_step.bind` (CLI, сессии не знает) никогда не пишет. Починено в t-007/t-008 (принятие записи
story_step по точному пути ребёнка без перезаписи; правило «только названная стори» и полный аудит на
`unknown-task` не тронуты). Остаток по вердикту критика t-007 (`docs/tasks/specs/reviews/t-007-s4-binding-review.md`):

- (а) **Новая ось SIBLING_MAP** «писатели и читатели привязок»: писатели `story_step.bind`, `host_dispatch.record`;
  читатели `enrich`, `record`, `_release_binding`, `resolve_binding_path`, `stage_guard`, `dispatch_liveness`,
  `worker_lifecycle`, `launch_card`. Класс дефекта: «читатель требует поле, которое один из писателей не пишет».
  Решение Lead владельца: вносить ось — да/нет.
- (б) F-4 — узкий случай чужой стори: путь ребёнка вне контракта `<role>__<slug>` + остаточная запись другой
  стори + стоп до `bind` новой; закалка — сверять тикет записи с путём через `stage_guard.slug_in_task_name`.
- (в) F-5 — пятая рукописная фикстура `session_meta` роллаута в тестах (test_codex_host, test_scout_reliability,
  test_doctor_context, test_doctor_access, test_s8_reporting_regressions): общий хелпер.
- (г) F-3 — `enrich` работает на каждом хуке: собственные PreToolUse/PostToolUse ребёнка Desktop теперь несут
  роль и стори через привязку story_step, значит на них действуют правила гарда роли и стадийные проверки на
  стопе — намеренно, но живым прогоном не доказано (FR-33): проверить на следующем S4.
- (д) На диске прогона 2406 стори TP2-2534 стоит открытой с зависшим `S8: running` (gate B с решением,
  `story_closed` → пусто): данные проекта, не код; из-за этого правило «единственная открытая стори» на этом
  диске не срабатывало никогда, и фикстура t-003 (2534 закрыта) не соответствовала живому состоянию.

Свидетель: `qa-factory/state/.exit_gate_blocks.json` записи `9b6a01b9…`/`6dd64e48…` (13.10 12:04Z, agent default,
task unknown-task); `records/journal.jsonl` 12:04:43 `subagent_stop task: unknown-task`; привязка
`state/host-dispatches/f857cfee….json` (agent_id = путь, bound_by story_step, без parent_session_id);
репродукция на копии — `docs/tasks/specs/t-007-s4-binding-identity.md`.

Принципы и правила: P10, P12, FR-16, FR-17, FR-54, FR-59.

Решение владельца нужно: да — пункт (а), новая ось карты симметрий.
перенесено из ветки dev2/codex-overhead-fixes (plans/piles/driver-controller/findings/20261013-binding-readers-writers.md), узел: CX1-8
