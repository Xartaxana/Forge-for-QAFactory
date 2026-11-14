# Хэндофф собирает код: одна система сборки формы передачи на все контракты, роль пишет только суждение

id: — | кучка: `roles-context` | от: Lead-сессия, по слову владельца 14.11.2026; разведка t-863 | приоритет: П1 | кандидат наверх: нет

Узел: RC2-8 пачки 2 (`batch-2-slova-cheloveka-v-brife.md`).

## Слово владельца

«запиши эту доработку как П1 узел. Надо что бы система создания хендофа была одна на всех (может быть с несколькими вариантами реализации если так будет удобно, но общий класс системы/архитектура/идея должна быть одна)» и «сейчас на это нет токенов, но запиши все результаты исследования в узел» — владелец, 14.11.2026.

Одобренная идея: код заполняет все ДАННЫЕ формы передачи до старта роли (id, счётчики, строки из плана / манифеста / отчёта прогона / триажа, дословные цитаты Then, поля из файлов багов и реестров, числа ретро); роль пишет только суждение (вердикт, причины, находки) — P27. После этого копию списка полей в стартовом промпте можно убрать (FV2-92 / Q7).

## Что не так (класс, P2)

Данные, которые фабрика уже держит, роль перепечатывает в форме передачи; форму собирают несколько несвязанных механизмов: `handoff_init` на старте, выводчики `handoff_check --fix` на финише, `repair_carries` на доработке, `BY_PATH`, `prefill_rows`. Одной таблицы «какое поле чем заполняется» нет.

## Что именно менять (направление ВЫБРАНО, правило 11)

ОДНА система сборки передачи для всех контрактов:

1. Одна таблица данных на контракт: для каждого ДАННОГО поля назван производитель (файл-источник + ключ). Поля-суждения в таблице помечены «роль» и остаются пустыми.
2. Один сборщик запускается на `story_step start` — в существующем месте `handoff_init` (`story_step.py:1168-1208`, `_write_dispatch_files`) — и заполняет данные по таблице.
3. Выводчики финиша (`handoff_check.py` DERIVERS / LIST_DERIVERS / BY_PATH / проверенные claims) становятся перепроверкой той же таблицы, а не вторым источником правды; `repair_carries` и `prefill_rows` сводятся к тем же строкам таблицы.
4. Реализации могут различаться по виду источника (JSON-ключ, строки отчёта, цитата Then, файл бага, реестр), но класс системы один (AR-14: один артефакт — один писатель; AR-22: у каждого читаемого поля есть производитель).
5. Отметки «обязательно / необязательно» попадают в файл формы (сегодня их знает только сгенерированный срез `references/slices/<role>/handoff-keys.md`).
6. Исправить внутри узла: `phases/s8.md:223-224` велит bug-reporter вызвать `handoff_init.py --from` после подачи багов — устаревший второй писатель с неверным флагом (`--role`).

Первый шаг узла (рекомендация, развилка (б)): замер на транскриптах прошлого прогона — сколько токенов и отказов стоит перепечатка (FR-55); только потом дизайн.

## Что известно (разведка t-863)

Метод: транскрипты прогонов не читались; «H» (роль копирует руками то, что держит код) ВЫВЕДЕНО из текстов контрактов и кода заполнения полей, не измерено. Проверка Lead (14.11 13:31): устаревший вызов `--from` в `s8.md:223-224` подтверждён; `handoff_check.py` DERIVERS :643 / LIST_DERIVERS :638 / `_code_fills` :2814 подтверждены; в BACKLOG 0 строк про `values_skeleton|prefill` (контроль `handoff_check` → 8) подтверждено.

### Факты

- Форма пишется ДО старта роли: `story_step start` → `_write_dispatch_files` → `handoff_init.py` (`story_step.py:1168-1208`). Заполняет только шапку (role/stage/window/dispatch/ticket), вписывает списки допустимых слов, строку `# Fill:`; единственная предзаполненная строка — `scope[].id` при доработке S3 (`handoff_init.py:358-380`).
- `repair_carries` (`index.yaml:79-95`) переносит значения только при доработке для 4 контрактов (S2, S3, S4 designer→critic, S8 scribe).
- На финише `handoff_check.py --fix` пишет значения, выведенные с диска: 22 DERIVERS, 2(+1) list-выводчика, 5 ключей grounding, 4 строки BY_PATH, 14 проверенных claims (`:638-686`, `:1028-1047`); роль не получает отказ за то, что оставила их пустыми (`:2814`).
- Счёт AR-22: 738 обязательных полей передач, 28 сделаны инструментом (`architecture.md:237`; `field-producers.json` говорит 27).
- Файл формы не несёт отметок обязательно/необязательно (`handoff.py` выводит необязательность по словам-заглушкам, `:34-36`, `:422-447`); сгенерированный срез `references/slices/<role>/handoff-keys.md` отметки несёт и доходит до роли в стартовом промпте через `inject-map.json` — это и есть «копия в промпте». Путь формы роль получает и в брифе.
- S8 bug-reporter: `start` пишет форму до работы (выведено); `s8.md:223-224` по-прежнему велит запустить `handoff_init.py --from` после подачи — устаревший второй писатель, неверный флаг (`--role`).
- Предшественник: находка `plans/piles/driver-hosts/findings/20261031-zapis-znachenij-formy-vse-ili-nichego.md` — правило записано до замера: если ≥ половины отказов «не заполнено», `handoff_init` пишет скелет `values.yaml`; `values_skeleton` есть только в тексте отказов (`handoff_check.py:2848`, `:2911`). Спека t-631 ввела `prefill_rows`.

### Данные, которые роль копирует руками (H, выведено)

- Id из плана / триажа / решения гейта: S3 scope id (первый диспатч), S4 id/obligations/disposition/review_scope.cases, S5 scope id плана, S6/S7 id строк, S8 scope id.
- Счётчики и размеры: S1 diff.bytes; S2 inputs_read.handed; S3 budget.*; S4 rows/manual_rows; S6 handed counts; S7 counts.*.
- Строки из манифеста / отчёта прогона / триажа: S5→runner selector/profile/freshness; S6 строки scope, env_blocked, surprises; S7 repairs/bug_drafts (поля данных).
- Записи проб и прогонов: S5 critic probes.records; S6 probe_before/after; S7 verify.request/result.
- Дословные цитаты строк Then кейсов: S4→runner, S6 manual_observations, S7 then_lines_before.
- Из файлов багов / реестра: S8 filed[] (поля данных), reasons_by_owner; S9 numbers.* (`retro-numbers.json`), delivery bookkeeping.
- Суждение (остаётся у роли везде): verdict, scope[].state/reason, tried, unresolved, findings, problem/fix в repairs, stage_acceptance, regression recommendations и т. п.

### Таблицы по стадиям (разведчика, по сути дословно)

Легенда: start = `handoff_init` при `story_step start`; check = `handoff_check --fix` на финише; const = литерал в контракте; H = данные, которые держит код, а роль печатает руками (выведено). Общее для всех форм: header.role/stage/window/dispatch/TICKET и словарные списки заполняются на старте; `artifacts.*` — const; `inputs_read[].version` выводится при check. Суждение везде: header.verdict, scope[].state/reason, tried[], unresolved[], blocked.*, непроверяемые claims.

| контракт | что код заполняет сегодня | что роль копирует руками (H) | суждение (роль) |
|---|---|---|---|
| S0 setup→scout | task, repositories, environment, tools, obligations «filled by code» по комментарию контракта (код не читан) | — | — |
| S1 scout→tester | implementation.source, diff.files/hunks/production_files, scope[].material_collected (check); claim implementation_source (verifier) | implementation.reference, diff.path, diff.bytes; scope[] id/relation/relevance/revision/read/attachments_inspected; person.review_recorded/words/accepted_gaps/late_sources | ac_code_conflict.* |
| S2 tester→strategist | size.computed (check); size.reasoning_ref (путь sizing.py); claims size_* | inputs_read[].handed (hunks S1; только repair carry) | inputs_read.read; строки реестра scope[] (набираются и в реестре, и в форме); contradiction_matrix, open_questions, size.override |
| S3 strategist→designer | grounding.* (5), blast_radius[] (check); scope[].id при доработке (start) | budget.size/cap/planned_rows/within_cap (только repair carry); scope[].id при первом диспатче (test-plan.json P-n); счётчики inputs_read requirements/candidates | scope[] state/reason/requirements/obligations/behaviour/risk/oracle/level/coverage/environment/flags; budget.if_over; manual_policy; not_planned; regression_recommendations |
| S4 designer→critic | scope[].case_version, requirements, plan_row (check, BY_PATH) | scope[].id/obligations/disposition/design_review_required; review_scope.cases, rounds_used; inputs_read.rows (частично); artifacts.cases_root | origin/reuse_of/self_probe; review_scope.focus |
| S4 critic→designer | review.rollcall, findings_file, scope[].case_version (check); inputs_read[0] строка автора (start) | scope[].id | review.outcome/rounds/rubric, findings, unverified, stage_acceptance, not_looked, advice, questions, register_gaps |
| S4 designer→runner | scope[].requirements, plan_row, case_version (check) | scope[].id/obligations/executed_by; inputs_read.manual_rows; execution[].then (дословная цитата кейса) | execution[] steps_ref/evidence/preconditions/data/inconclusive_when/not_executable_when |
| S5 пара плана | artifacts.plan const; штамп плана на финише | scope[].id | review.outcome, remarks[], scope[].state |
| S5 automator→critic | runtime_provenance/tests/run_witness/probes, scope[].case_version (check); 2 claims | scope[].id/origin/obligations | plan_remarks, deviations, for_the_reviewer |
| S5 critic→automator | review.findings_file, receipt_ref, probes.runtime_provenance (check) | probes.records[] (instance/verdict/record); scope[].id | findings, tooling_findings, unverified, not_looked, outcome |
| S5 automator→runner | runtime.provenance, tests, run_witness, case_version (check); claim fingerprint | scope[] id/case/obligations/selector/profile/last_receipt/freshness/stale_because; runtime.environment/build/probe_command; not_in_scope; handed_profiles | — |
| S6 runner→analyst | run.execution_status/totals/window_totals/witness (check) | run.environment/build/probe_before/after; scope[] id/case/obligations/executed/rerun_reason/evidence/duration (run-report.json); manual_observations.before_change, surprises («as built by code»); env_blocked, superseded; счётчики; цитата manual then | manual observed/result/why_inconclusive |
| S7 analyst→automator | строки not_for_repair, только нулевой исход (`handoff_check.py:1550-1559`) | scope[] id/case/round; repairs[] id/verdict/evidence/then_lines/rerun_series (triage.json) | repairs[] problem/expected/fix/check/mechanism/kind; stage_acceptance; where_it_went |
| S7 automator→analyst | rounds[].verify.witness (check) | verify.request/result; then_lines_before; scope id/round; repairs_answered | changed, then_lines_after, fix_result, cause |
| S7 analyst→scribe | шаг подтверждения bug_drafts выведен (роль пишет константу `unconfirmed`); claim no_bug_without_draft | scope[] id/state/case/requirement/evidence/repaired; counts.* (7); bug_drafts ref/path/triage_ref/requirement/damage/manual_steps; env_issues/not_verified/case_defects частично | reproduction, duplicate_of, stage_acceptance, tried |
| S8 scribe→gate B | delivery.ready, blocked_by (check); message_sections, not_shown const | delivery.reasons_by_owner; rehearsal.ran/factory_fixable_open (реестр); drafts_received/rows частично | rehearsal.person_decides/factory_defect; questions; stage_acceptance |
| S8 bug-reporter→scribe | — | scope[].id (решение gate B); filed[] draft/bug/action/cases/requirements/source_draft/proposal; inputs_read version/drafts_chosen; quarantined[].debt_file | not_filed.why, no_case_reason, quarantined.trigger, tried |
| S9 retro→project | — | numbers.* (4, `retro-numbers.json`: «no model does this arithmetic»), retro_mode, delivery_bookkeeping.* | knowledge_fold, factory_backlog, feedback.answer, строки scope |
| Gate A / Gate B | решения человека пишет `controller gate-decision` (читаются только первые строки) | — | человек |

Аналог: `inputs_read[].handed` в S2 называет hunks S1, но значение приносит только repair carry — тот же класс H. Приложение A спеки K10 r2 (`:474-483`) «K3 handoff form by path»: экономия 3 686 Б автоматор, 3 182 Б код-критик, 5 576 Б стратег; условия — S5 (S8 start пишет форму) и S6 (в форме нет отметок обязательно/необязательно).

### Развилки (для тира выше)

- Где код пишет больше: на старте (`handoff_init`) или на финише (выводчики `--fix`).
- Остаётся ли файл роли формой, которую она заполняет, или код дописывает её первым, а роль добавляет только суждение.

### Не сделано разведкой

Код заполнения S0 не читан; формы gate A/B частично; `handoff_help.py`, `exit_gate.py` — только по попаданиям grep; транскрипты не читались. Полный дайджест с таблицами и трассой из 30 строк — отчёт разведчика в сессии 9408e840 (t-863); сжатый дайджест — `docs/tasks/handoffs/t-863-handoff-assembly-recon.md`.

## Открытые развилки (вопросы с рекомендацией)

(а) Заполнять на старте (рекомендуется: роль видит готовую форму; сборщик на месте `handoff_init`) или на финише (выводчики `--fix`; роль по-прежнему печатает данные и ждёт отказа)?
(б) Сначала замерить на транскриптах прошлого прогона, сколько токенов и отказов стоит перепечатка (рекомендуется шагом 1 узла, до дизайна; FR-55).

## Связи

FV2-92 (`live-run-fvf`, Q7: после этого узла копию списка полей в стартовом промпте можно убрать); находка `plans/piles/driver-hosts/findings/20261031-zapis-znachenij-formy-vse-ili-nichego.md` (предшественник, правило скелета значений); `20261026-formy-porozhdayut-lishnie-hody-rolej.md` (та же кучка, `--values`, отказ одной командой); `20261023-tri-voprosa-zamysla-svip-vocabulary-formy-handoff-i-ukazateli-na-plagin.md` (значения в формах); `docs/tasks/handoffs/t-863-handoff-assembly-recon.md`.

Принципы и правила: P2, P27; AR-22, AR-21, AR-14; FR-49.

Решение владельца нужно: нет (она решила, 14.11.2026).

Следующий шаг: короткий план Lead → дизайнер → критик на план (новая идея, PROJECT.md «Как разрабатывается новая идея владельца»), когда будут токены.

<!-- id выдаёт интегратор при сборке пачки. -->
