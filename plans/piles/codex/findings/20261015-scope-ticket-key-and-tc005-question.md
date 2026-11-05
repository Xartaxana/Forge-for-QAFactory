# Скоуп контроллера = ключ тикета, и незаданный вопрос TC-005 (прогон TP2-2406, S4 → гейт A)

id: — | кучка: `codex` | от: Dev2 (прогон TP2-2406, Codex Desktop), 15.10.2026 | приоритет: П1 | кандидат наверх: нет

Что не так / что сделать: диагноз критика t-017 (`docs/tasks/specs/reviews/t-017-scope-mismatch-diagnosis.md`).
`state["scope"]` контроллера по контракту — id кейсов (все читатели: отказ rework `controller.py:1683-1686`, карта
кейс→строка плана :1123-1136, скоуп S5/S6 :1796, пометки гейта A :1004-1014, привязка решения :1382, проверка пинов :1470,
`prepare` :851). Единственный писатель — `revise_plan` (:1049); драйвер инициализирует `[]` и на S4 переводит в
запиненные id (story_run.py:5551-5560, s4.md:79). В прогоне 2406 оркестратор Codex вручную записал
`controller-initialize.json` с ключом тикета (роллаут 10.10 22:28, строки 211/237; controller-api.md:89 «initial known
IDs» двусмысленно; `validate` :2538 принимает любой список), `revise_plan` не запускался ни разу → rework TC-004
отказан («case(s) outside the approved scope: TC-004; the approved scope is TP2-2406»), скоуп S5 пуст,
R-11–R-13 не покрыты. Чинится в t-018: членство `revise_plan` по пинам, дверь `revise_plan` в отказах, `initialize`
отказывает собственному ключу стори, тексты controller-api.md / s0.md.

Остаток (не в t-018):

- (а) **TC-005 — незаданный вопрос** (Q4 диагноза): `gate_preflight.py:1322-1334` срабатывает на
  `session-detail-feedback/TC-005.md:14` (Then 1 `unknown`/`raise`); шаг поднятия — `critic_rollcall.raise_pending`
  (:475-509) через `--apply-fixes` на выходе S4, который ни один роллаут не выполнил. Запускать нельзя:
  `question_register._raise` (:741-761) нумерует id только по `open_questions` (пусто) и выдаст новый Q1 — коллизия с
  отвеченным Q1 владельца (`state/words/q1-option-b.txt`) и повторный вопрос (FR-7). Сам TC-005 в
  `session-detail-feedback` — устаревший дублирующий пин: дизайнер-8 закрыл живой `session-detail/TC-005` на R-5.
  Нужно: поднятие не переиспользует отвеченный id, ключ — кейс с областью; устаревшему пину — решение жизненного
  цикла, не вопрос.
- (б) `unmapped_scope` (:1796) ложно перечисляет 6 id, запиненных в двух областях; детектор сброса в plan-baseline
  слеп к ключам с областью; шесть дублирующих пинов по областям — решение человека.
- (г) Из вердикта критика t-018 (`docs/tasks/specs/reviews/t-018-scope-review.md`): в `docs/SIBLING_MAP.md` нет оси
  «идентичность кейса в скоупе» (читатели предиката членства: проверка пинов гейта A, `revise_plan`, дверь rework,
  карта :1111, литеральное сравнение rework :1713) — строка оси на решение Lead владельца; словари пинов по голому id
  вне диффа (`check_delivery.py:675` и другие) схлопывают пины в двух областях — вопрос скауту; на устаревшем хранилище
  `rework --cases TP2-2406` всё ещё строится (внутри сохранённого скоупа, `case_version_links: []`) — не
  регресс, но дыра старой формы; тесты печатают «gate-A override marks could not be written (SystemExit: 3)» без
  `qa-factory/config.json` — шум без утверждения.
- (в) Восстановление прогона после деплоя t-018 (Q5): `--operation next` → await_gate A rev 70; человек подтверждает
  скоуп TC-001..TC-009, судьбу шести дублей (включая TC-005 `session-detail-feedback`), новые id для R-11–R-13
  (каждый — ещё один `revise_plan` после пина); `revise_plan` с запиненными id (plan revision = sha256 test-plan.json,
  expected_revision 70); rework дизайнера на TC-004 (TS-4/TS-8/TS-9, `--cause test_defect`), accept; re-pin
  `case_versions.py`; rework критика, accept с `stage_complete` (пересъёмка baseline); приложение кейсов, репетиция
  гейта A, решение словами человека. Не трогать: пины и `story-case-links.json` руками, принятые S4-8 и critic-1,
  слова Q1 и R-5, `plan-baseline.json`, `events.jsonl`, `critic_rollcall --apply-fixes` до починки (а).

Свидетель: роллаут `2026-10-14T22-34-04-01a13c1f…` строки 640/641 (отказ дословно); `state/controller.json`
(`scope: ["TP2-2406"]`, 70 событий без `revise_plan`); копия C: `raise_probe.py` → `{"raised": [{"case":
"TC-005", "then": 1, "question": "Q1"}]}`.

Принципы и правила: P1, P13, P20, FR-1, FR-2, FR-7, FR-40, FR-41, FR-59.

Решение владельца нужно: нет (решения по дублям и новым id — человека в прогоне, по процедуре (в)).
перенесено из ветки dev2/codex-overhead-fixes (plans/piles/driver-controller/findings/20261015-scope-ticket-key-and-tc005-question.md), узел: CX1-11
