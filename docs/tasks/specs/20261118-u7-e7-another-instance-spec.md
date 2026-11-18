# Spec U7 / E7 - another instance of the stand or device: asked once, when needed (t-1291, node universality/1/U1-11, F19)

Owner, 17.11.2026: «спросить один раз, но не на онбординге, а тогда когда это понадобится». Decided by the Lead (not reopened):
F-E7-1 = (a) typed need on `manual_evidence.py unprepared` + ONE trigger at the top of `stage_S7` through `Driver.no_move`; F-E7-2 = (a)
answer registry key + CLI verb + conductor-actions row; F-E7-3 = one answer per stand, the text names the stand. Frozen facts: digest
`docs/tasks/specs/reports/t-1273-e7-trigger-site-digest.md` (ids q1a-q5k); every site below was re-read on main 18.11.2026 by symbol.

**DECIDED 18.11.2026 (architect session; the owner may reverse): F-N1 = (a), F-N2 = (a), F-N3 = (a).** F-N1: invariant E5.8 is
restated, not dropped - a runner-written marker is honoured ONLY as the closed need word with the code-written reason and no result,
and every such record reaches the person (the question, or an answer the person recorded). F-N2: the owner's "ask once" is a standing
answer per stand, yes or no; the question text says so and names `ask again`. F-N3: one road (P31) - the walk verdict carries `needs`.
Not accepted for dispatch until the plan critic (t-1295) returns. Order with other nodes: E7-3 shares `manual_evidence.py` and
`test_manual_evidence.py` with the 1b fix round (t-1294) and goes after 1b merges.

## 0. Forks returned (the Lead decides; each node is drafted on the recommendation)

- **F-N1 - a need on a PREPARED case meets invariant E5.8.** Read on main: `manual_evidence.py::write_unprepared` refuses a case whose
  `request.json` holds no `unprepared` marker ("The `unprepared` command is for a case whose request.json says it was not prepared"), and
  `coverage_contract.py::_validate_unprepared` honours an unprepared record only where code wrote the request marker (docstring: "The
  marker is honoured only where code wrote it (E5.8)"); `finalize_task.py` then turns any other issue into `result: inconclusive,
  evidence_errors`. Another instance is needed exactly on a case the factory DID prepare. (a) `--needs <closed word>` lifts the marker
  requirement: the record's `unprepared.reason` is a code-written constant of the need, `unprepared.need` is the closed word, and
  `_validate_unprepared` honours that pair with no request marker. Invariant kept by (a): a runner-written marker is honoured only with a
  closed need and no result, and every such record reaches the person (the question, or an answer the person recorded) - no prepared
  case leaves the results silently. (b) keep E5.8: a need only on a case the factory failed to prepare - the decided F-E7-1 then never
  fires on the case it exists for. **Recommend (a)**; cost: `coverage_contract.py` joins E7-3.
- **F-N2 - what `I will check these cases myself` remembers.** (a) a standing "no" for the stand (`authorized: false`): later stories
  hand such cases to the person without asking; (b) this story only, the next need asks again. The owner's "ask once" reads as (a);
  (b) asks every story. **Recommend (a)**; the question text says the answer is kept for the stand and `ask again` takes it back.
- **F-N3 - the walk road (one road, P31).** On the walk road the runner closes a case through `walk_session.py verdict`, and
  `manual_evidence.py::record_from_walk` writes the record; a runner that called the CLI there would be overwritten by the walk's own
  record (`walk_session.py::_missing_verdict` writes an all-`inconclusive` record for an item with no verdict). (a) the verdict takes an
  optional closed `needs`, and `record_from_walk` sends it to the same `write_unprepared(need=...)` - one writer, both roads;
  (b) CLI only, walk road left out (a `narrows` line: walk-road projects never reach the question). **Recommend (a)**; cost:
  `walk_session.py` and `references/walk-charter.md` join E7-3 / E7-2.

## 1. Architecture, owners, variety walk

| AR | how E7 meets it | change check (copied into the node DoD) |
|---|---|---|
| AR-3 | new registry key `environments.extra_instance` (stand scope) in `config-keys.json` `knowledge`; read through `project_knowledge` | registry row only: no template row and no interview topic, by the owner's word 17.11.2026 (carrier: §6 of `docs/tasks/specs/20261117-u7-pass-without-stuck-spec-r4-7b-7c-e7.md`); `ask_when: null` stays (test_config_migration `knowledge_rows`) |
| AR-13 / AR-14 | one writer `project_knowledge.record`, one reader `project_knowledge.instance_answer` (new) read by `brief_pack` and the trigger; the need word set has ONE home (`project_knowledge.INSTANCE_NEEDS`); one record writer `manual_evidence.write_unprepared` for both roads | critic greps `environments.extra_instance` and `another_instance`: only `config-keys.json`, `project_knowledge.py`, tests, role text |
| AR-16 | the question is key `s7.extra_instance` of `question-prices.json`, raised as ONE literal `closed_question` through `Person` / `take_answer` | census K15 both ways (`test_conductor_doors.py`); `human_text.problems` passes |
| AR-17 | the trigger calls `Driver.no_move` with `call: False` (model `s7_open_work_ask`); free words go to the conductor once through `unread` | A27: one new baseline row, `NO_MOVE_BASELINE_MAX` raised by 1, named |
| AR-24 | the person's answer words go whole into the registry row (`provenance.words`) | E7-3 row f |
| AR-25 | new states have rows in `design/state-exits.md` (registry row; the driver's `extra_instance_asked` / `extra_instance_held` / `extra_instance_rewalk`) | rows present, each with its way out |
| AR-20 | `qa-runner` rows of `role-load.json` rise by the measured amount | `role_load.py --role qa-runner` before/after in the report |
| AR-29 | checks below are shape/join; whether a case needs another instance is the runner's judgment, accepted by the person's answer | `test_judgment_census.py` (canon judges); builder stops with a question if a unit needs a row |
| AR-1 | no project or platform word in code; the need is a factory word (closed set), the stand is the project's own name | diff adds no Android/iOS/device-brand word |

Checks added or altered: `project_knowledge.record_problems` (value shape of the new key) - owner data, census shape; `_validate_unprepared`
(honours a closed need) - data, shape; `walk_session.verdict_problems` (`needs` closed, no pass/fail beside it) - data, shape;
`write_unprepared` / CLI `--needs` - data, shape; the S7 trigger (a typed need joined to a registry state) - data, xref; none is a
refusal on a role's content (a need outside the set is a form refusal with its door). Commit lines `architecture:` and `judgment:` in the
form `tools/architecture_gate.py` checks (the one carrier); for each node `judgment: none -- <why>` (e.g. "a closed field joined to a
registry state; the need itself is the runner's judgment, accepted by the person's answer"), never bare.

Variety walk (architecture.md § A):
- axis 7: held by key|role -- registry key `environments.extra_instance` per stand + the runner's judgment of the need; unknown value -> nothing started, one question at S7 entry naming the stand and the cases; on `by hand` the cases go to the report as checks left with the person
- axis 2: held by role -- "another instance of the stand or device", no platform word; unknown value -> as axis 7
- axis 13: held by key -- the registry is append-only and carried by reinstall; unknown value (no row, unreadable file) -> asks once
- axes 1, 3, 4, 5, 6, 8, 9, 10, 11, 12: n/a -- no site of E7 reads the product language, test stack, flow, requirement source, delivery target, host, people, artifact language, task size or check kinds

No `narrows` line under F-N3 (a). E7-1 edits the axis 7 line of `design/architecture.md` IN PLACE (same line, no line added: test-layers
`named_by` pins `design/architecture.md:256` and `design/state-exits.md:69`).

## 2. Behaviour (settles the brief's list)

**Position of the trigger.** `Driver.stage_S7`, inside `if not analyst_done:`, right AFTER `reasons = self.failures_to_triage(awaiting=awaiting)`
and BEFORE the `if not reasons and not awaiting:` close. INVARIANTS: (i) after `s7_closed_by_scribe`, `consumer_settled` and the entry
refusal of `failures_to_triage` - a halted or refused S7 entry raises its Refusal first and is never turned into this question; (ii) before
the no-failures close, `s7_pretriage.pretriage` and the analyst dispatch - no triage row (code's or the analyst's) is ever written over a
case whose need has no answer; (iii) a `known` registry row (yes or no) never raises the question (FR-7); (iv) a `state["seam_rework"]`
pending -> the step returns without triage (the person's chosen rework goes first). Runs on the freshness re-triage path too (that path sets
`analyst_done = False`); does not run while an accepted fresh triage stands (the need was answered before it was triaged).

**The step** `Driver.s7_extra_instance_step() -> bool` (True: stage_S7 returns this entry):
1. rows = `manual_evidence.unprepared_rows(report)` with a `need`. None -> False (records written before E7 carry no `need` and read as today).
2. stand = `stand_gaps.stand_name(task_root)` (one stand per story; the placeholder `this stand` = none chosen). Group by need (sorted;
   one value now). For each need: `PK.instance_answer(project, stand, need)`.
3. `authorized` None (no row, revoked, unreadable registry, no stand) and no `state["extra_instance_held"][<stand>|<need>]` -> raise the
   question (below). Several cases -> ONE question listing them all; several needs -> the first unanswered, the next on the next entry.
4. `authorized` True -> owed = the need rows whose `ended_at` is EARLIER than the answer's moment (registry row `at`; a held answer: every
   row) and whose `state["extra_instance_rewalk"][case]` is 0. Moments compared by `environment_record._moment`; an unparseable moment
   -> not owed (printed line; the case goes on as an unprepared walk - never a paid round on an unknown). Owed -> ONE
   `self.rework("S6", "qa-runner", <first block of controller.manual_blocks(owed)>, reason, cause="question_answer", complete=False,
   on_request=<count each case +1 in extra_instance_rewalk>, extra=[manual lines + "Starting another instance of the stand or device on
   <stand> is authorized (the person's answer): start it with the project's own actions, write what you started in tried.md, then walk
   these cases again."])` - the shape of `s7_rejudge_round`. `ReworkRefused` -> each case of the block counted, one printed line, the
   cases go on to triage. Return True. A case re-walked once that is still owed is never re-sent (no loop): it goes on to triage.
5. `authorized` False -> nothing; triage goes on; the cases are unprepared walks (delivery `unprepared_walk`, a check left with the person).

**The question** (`Driver.s7_extra_instance_ask` raises through `no_move({"why": "threshold", "kind": "extra_instance", "call": False,
"stage": "S7", "dispatch": "", "lead": lead, "site_doors": ("start it", "by hand"), "site_fallback": ...})`; `Driver.s7_extra_instance_person`
builds `Person("extra_instance", self.closed_question("s7.extra_instance", lead, [start, by_hand, dict(self.STOP_OPTION)]), "S7", "")`,
NO `holds` (a question with `holds` may be deferred and the analyst would run). Lead: the stand by name, each case with the runner's
`not_walked` words quoted, "Should the factory start one when a case needs it? Your answer is kept for the stand `<stand>` and is not
asked again; say `ask again` later to change it." No chosen stand, or a story that leaves no trace: "... your answer holds for this
story only". Asked again after `stop`: the lead starts "You answered `stop` earlier." (FR-7). State `extra_instance_asked = {stand, need,
cases, lead, at, stopped}`.

**The answers** (`Driver._answer_extra_instance`, branch `elif kind == "extra_instance":` in `take_answer` right AFTER the `open_work`
branch - `test_walk_account.py` pins `walk_supply` < `walk_account` < `open_work`):
- `start it` -> `PK.record(key=EXTRA_INSTANCE_KEY, environment=stand, element=need, state="known", scope="stand", value={"authorized":
  True}, words=<the answer, whole>, source="person", story, by="driver", where="S7 another-instance question", task_root)`; a refused write
  (no stand, no-trace story, unreadable registry) -> `extra_instance_held[<stand>|<need>] = {authorized, words_file, at}` and a printed
  line that it is kept for this story only. Then `answer_row`, the asked record goes. The next entry's step 4 re-walks the cases.
- `by hand` -> the same with `authorized: False` (F-N2 a); the cases go on to triage and delivery as checks left with the person.
- `stop` -> nothing recorded; `stopped: True`; `raise self.held_question(self.stop_held(...))`; a rerun asks again.
- any other words, or no asked record -> `self.unread("extra_instance", ..., doors=("start it", "by hand", "stop"), again=...)`: the
  conductor reads them once and may run the new `project_knowledge.py instance` row; its `continue` re-enters S7 and step 3 reads the row.

**Next story / revoke.** A `known` row -> no question; the runner's brief line says what was answered (E7-2) and the runner acts on it.
`project_knowledge.py revoke --id PK-<n>` -> the row reads as nothing, the next need asks again (the revoke message names it). Two stories
on one stand asking at once: both ask; the later answer is the newer row and wins (append-only).

## 3. Nodes. Order: E7-1 first; then E7-2 and E7-3 in parallel (no shared file); merge E7-3 before E7-2

TEMPORAL: E7-2's page tells the runner to use `--needs`, which E7-3 brings into existence; merged first, the flag would be refused. Before
E7-3 merges, `--needs` does not exist and no record carries `need`; after, a record may, and the trigger reads it. Shared reads only:
both read E7-1's `PK.instance_answer`, `PK.INSTANCE_NEEDS`, `PK.EXTRA_INSTANCE_KEY` (fixed by E7-1, frozen for both).

### E7-1 - registry key, reader, verb, conductor row

given: this spec §1, §2; `project_knowledge.py` (`KEYS`, `record`, `record_problems`, `cmd_lesson`, `cmd_revoke`, `_story_stand`, `main`); `references/config-keys.json` `knowledge` row `environments.stand_lessons`; `references/conductor-actions.json` rows 29-30; `design/state-exits.md` § What a person said about the product
owns:
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/project_knowledge.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/references/config-keys.json
C:/QAFactory/forge-repo/ai-packages/qa-factory/references/conductor-actions.json
C:/QAFactory/forge-repo/ai-packages/qa-factory/design/state-exits.md
C:/QAFactory/forge-repo/ai-packages/qa-factory/design/architecture.md
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_project_knowledge.py
non-goals: the trigger, the record field, the runner page, the brief line; any onboarding question; delivery wording
handoff: branch + report (witness tails, `role`-free; the reader's signature as built)
edges: below
DoD: `python -m pytest ai-packages/qa-factory/scripts/tests/test_project_knowledge.py -q`
siblings: `cmd_lesson` (twin verb, same prologue `_write_prologue` + `_story_stand`); revoke row 30 says; `cmd_revoke` branch of keys asked again
designer: C:/QAFactory/forge-repo/docs/tasks/specs/20261118-u7-e7-another-instance-spec.md

Work: (1) `config-keys.json` `knowledge`: `"environments.extra_instance": {"store": "registry", "compare": "exact", "scope": "stand",
"needed_by": ["project_knowledge.py:instance_answer", "brief_pack.py:instance_lines", "driver_stage_s7.py:s7_extra_instance_step"],
"ask_when": null}`. (2) `project_knowledge.py`: `EXTRA_INSTANCE_KEY = "environments.extra_instance"`; `INSTANCE_NEEDS = ("another_instance",)`
(the ONE home of the need words); `record_problems` branch for the key BEFORE the role rules (as `LESSONS_KEY`): element in
`INSTANCE_NEEDS`, value exactly `{"authorized": true|false}`; the empty-words door names `instance`. Reader `instance_answer(root, stand,
need) -> {"authorized": True|False|None, "row", "problem", "no_stand"}` - PURE, never raises; shape of `lessons` (no stand / placeholder ->
`no_stand`; key not in `KEYS` or unreadable -> `problem`, authorized None). Verb `instance --task <T> --allowed yes|no [--stand <name>]
[--need another_instance] --words-file <f>` (prologue and stand as `cmd_lesson`; `by="conductor"`); prints `<need> on <stand>:
environments.extra_instance recorded (PK-n)` / `already recorded`. `cmd_revoke`: the key joins the "asked again where it is needed"
branch. (3) `conductor-actions.json` `actions`: a row twin of line 29 - says "the person says whether the factory may start another
instance of the stand or device when a case needs it (a yes or a no for the stand, meant for the next runs too)", run `project_knowledge.py
instance --task <T> --allowed yes|no [--stand <name>] --words-file <file holding their words>; a story that leaves no trace refuses it`;
row 30's says gains "or the answer about another instance". (4) `state-exits.md` row 167: the state list and the entering commands name
`instance`; the way out names revoke (the question speaks again at the next need) - edited in place. (5) `architecture.md` axis 7 line:
append "; registry: another-instance answer per stand, asked once at the moment of need (E7)" in place.

Edges (each with its invariant):
- absent registry file -> authorized None, no problem (INV: unknown asks once, never reads as a yes); unreadable / other schema -> None
  with problem (INV: an unread registry is never a "no"); catalogue without the row -> None with `CATALOGUE_PROBLEM`.
- stand: `--stand` absent and no chosen stand -> refusal listing the stands, nothing written (`_story_stand`); a `--stand` naming no
  configured stand is recorded as given (as `lesson`) and never read for another stand (INV: an answer for a misspelled stand errs toward
  asking again, never toward starting).
- same answer twice -> `already recorded` (the existing row); the other answer -> a new row that wins (INV: latest row in force).
- empty words file / no `--words-file` -> refusal with door (AR-24); `--allowed` outside yes|no, `--need` outside `INSTANCE_NEEDS` ->
  argparse refusal; story that leaves no trace -> `NO_TRACE_WORDS`, nothing written.
- revoked row -> None (INV: revoke makes the question speak again at the next need).
- value `{"authorized": "yes"}`, extra keys, element `""` -> `record_problems` refusal, nothing written (INV: only a typed yes/no is ever read).
Tests, `test_project_knowledge.py` (keep 4119), one parameterised table, strongest first:
- test: test_project_knowledge.py::<instance table> row "yes/no recorded on the chosen stand, read back by instance_answer, words whole; the other answer wins" | expected from: §2 "The answers", owner's word 17.11.2026
- test: same table row "absent file / unreadable / revoked / no stand -> authorized None" | expected from: §E7-1 edges
- test: same table row "CLI battery: no stand, empty words, bad --allowed, bad --need, no-trace story -> refusal, nothing written" | expected from: §E7-1 edges, CLAUDE.md rule 11 (outside input)
- test: none -- the conductor-actions row is read by the conductor's judgment | expected from: live L8 (§4)
Narrow, canon judges: `test_config_migration.py::knowledge_rows` (import and call; report `not run locally: test_config_migration.py,
canon judges` if not called). AR change checks: the AR-3 line of §1 in the commit.

### E7-2 - runner page, walk charter, brief line, role-load

given: this spec §2 (contract: `--needs another_instance`, verdict `"needs": "another_instance"`, `PK.instance_answer`); `agents/qa-runner.md` (section `When to ask`, `kind: process`); `references/walk-charter.md` § After the steps; `brief_pack.py::stand_lesson_lines`, `::manual_stand_lines`; `app_card.py::_stand_lines`; `references/role-load.json`; `design/role-rules.json`
owns:
C:/QAFactory/forge-repo/ai-packages/qa-factory/agents/qa-runner.md
C:/QAFactory/forge-repo/ai-packages/qa-factory/references/walk-charter.md
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/brief_pack.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/app_card.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/references/role-load.json
C:/QAFactory/forge-repo/ai-packages/qa-factory/design/role-rules.json
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_brief_pack.py
non-goals: the record field and the trigger (E7-3); the registry (E7-1); any Android/iOS word; the S5 brief head
handoff: branch + report with the doc-dispatch witness script in full, `role_load.py --role qa-runner` before/after
edges: below
DoD: `python -m pytest ai-packages/qa-factory/scripts/tests/test_role_rules.py ai-packages/qa-factory/scripts/tests/test_role_load.py -q` and the narrow call of `test_brief_pack.py::ss1_11_stand_lessons` (import, call)
siblings: `stand_lesson_lines` (the one formatter: the new `instance_lines` sits beside it and is read by the same two places); `app_card._stand_lines` prefix filter (walk road)
designer: C:/QAFactory/forge-repo/docs/tasks/specs/20261118-u7-e7-another-instance-spec.md

Work: (1) `qa-runner.md`, `When to ask`, one bullet: "When a case needs another instance of the stand or device than the one prepared:
if your brief says starting one is authorized, start it with the project's own actions and write what you started in `tried.md`; if it
says not authorized, or says nothing, do not start it - record the case unprepared with the need (`manual_evidence.py unprepared --needs
another_instance`, or `\"needs\": \"another_instance\"` in a walk verdict), naming what you would start and why, with what you tried.
The factory asks the person once and remembers the answer." (2) `walk-charter.md` § After the steps, one bullet: a case that needs another
instance and may not start one: the verdict carries `"needs": "another_instance"`, a `limitation` saying what you would start and why, and
no pass or fail. (3) `brief_pack.instance_lines(project, stand) -> list`: through `PK.instance_answer` only; one line `- Another
instance on <stand>: authorized (the person's answer, given in <story> on <date>)` / `not authorized (...)` / `not answered yet` /
`could not be read (<problem>)`; no stand chosen -> []; never raises (an exception -> the `could not be read` line). `manual_stand_lines`
appends it right after `stand_lesson_lines`. (4) `app_card._stand_lines` keeps lines starting `- Another instance` (walk road).
(5) `role-rules.json`: row `runner-another-instance-asks-once`, carriers `agents/qa-runner.md` anchor "another instance of the stand or
device" and `references/walk-charter.md` anchor `"needs": "another_instance"`; source "owner 17.11.2026 (E7)". (6) `role-load.json`
`ratchet_tokens.qa-runner` and `process_ratchet_tokens.qa-runner` set to the measured values (`python -B
ai-packages/qa-factory/scripts/role_load.py --role qa-runner` before and after; the raise named in the commit, AR-20).

Edges (each with its invariant):
- registry unreadable -> the `could not be read` line (INV: an unread answer is never shown as authorized; the page then says do not start).
- no stand chosen -> no line; the page's "says nothing -> do not start it" decides (INV: silence never authorizes).
- a revoked row -> `not answered yet` (INV: revoke takes effect at the next brief).
- the line is in both roads' stand text (manual block brief and the walk's app card) (INV: one road, P31).
- page vs brief conflict impossible by construction: the page defers to the brief line; with no line the safe branch runs.
Tests, strongest first:
- test: test_brief_pack.py::ss1_11_stand_lessons (new rows) "the four registry states give their line in `manual_stand_lines` and in `app_card._stand_lines`; no stand -> no line" | expected from: §E7-2 Work (3)-(4), edges
- test: test_role_rules.py (registry walk, the new row) | expected from: docs/TESTING.md «Правила ролей не теряются»
- test: test_role_load.py (rows equal the measured load) | expected from: role-load.json note (shrink-only, a raise named)
- test: none -- the page and charter text are role judgment text | expected from: DOC-DISPATCH witness: keys K1 `another instance of the stand or device`, K2 `The factory asks the person once`, K3 `do not start it`, K4 `"needs": "another_instance"` (in walk-charter.md); negative control: K5 `start it anyway` must be ABSENT and the script must report a deliberately absent key as failure
Not run locally: `test_brief_pack.py` whole (canon judges; narrow call above).

### E7-3 - the record field (both roads) and the S7 trigger

given: this spec §0-§2; `manual_evidence.py::write_unprepared`, `::unprepared_rows`, `::record_from_walk`, CLI `unprepared`; `coverage_contract.py::_validate_unprepared`; `walk_session.py::verdict_problems`, `::walk_record_of`; `driver_stage_s7.py::stage_S7`, `::s7_open_work_ask`, `::s7_open_work_person`, `::_answer_open_work`, `::s7_rejudge_round`; `driver_machine.py::take_answer`; `controller.py::manual_blocks`; `question-prices.json` keys `s7.open_work`, `s6.walk_account`; `audit_factory.py` `NO_MOVE_BASELINE`; digest q1f, q3c-q3k
owns:
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/manual_evidence.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/coverage_contract.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/walk_session.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/driver_stage_s7.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/driver_machine.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/references/question-prices.json
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/audit_factory.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/design/state-exits.md
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/fixtures/driver-layers.json
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_conductor_doors.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_no_move_seam_sites.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_manual_evidence.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_walk_record.py
non-goals: a road from a mid-S6 runner turn to the person (digest q2e); delivery wording of an unprepared walk; the S6 close sites; the runner page (E7-2); starting any instance by code
handoff: branch + report (witness tails; `dry_exits.py --check` tail; lines `not run locally: <file>, canon judges`)
edges: below
DoD: `python -m pytest ai-packages/qa-factory/scripts/tests/test_manual_evidence.py ai-packages/qa-factory/scripts/tests/test_walk_record.py -q`, the narrow call of the new `test_no_move_seam_sites.py::e7_extra_instance_trigger` (import, call), `python -B ai-packages/qa-factory/scripts/tests/dry_exits.py --check`
siblings: `s7_rejudge_round` (the S7 -> S6 rework shape); `s7_open_work_ask`/`_person`/`_answer_open_work` (the site question shape); `_answer_walk_account` (`by hand`); `write_unprepared` callers (CLI, `record_from_walk`)
designer: C:/QAFactory/forge-repo/docs/tasks/specs/20261118-u7-e7-another-instance-spec.md

Work: (1) `manual_evidence.py`: `write_unprepared(task, case, observations, not_walked="", need="")`; `need` in `PK.INSTANCE_NEEDS` or
ValueError with the door; with a need and no request marker the obligations come from the case's prepared request (the reader the build
road uses) and `unprepared = {"reason": NEED_REASON, "need": need, walked...}` with `NEED_REASON` a module constant ("needs another
instance of the stand or device; not started without the person's word"); with a marker, the marker's reason stays and `need` is added;
the walked / `not_walked` rules unchanged. CLI `unprepared --needs <word>` (choices `PK.INSTANCE_NEEDS`). `unprepared_rows`: an entry
gains `need` and `ended_at` (`attempt_ended_at`) ONLY when the marker carries a need. `record_from_walk`: a walk record with `needs` ->
`write_unprepared(..., not_walked=<limitation> if not walked else "", need=...)`, never `build_record`. (2) `coverage_contract.
_validate_unprepared`: a marker with `need` in `PK.INSTANCE_NEEDS` and `reason == ME.NEED_REASON` is honoured with no request marker
(issues `[UNPREPARED]` plus the result check); everything else as today. (3) `walk_session.py`: `verdict_problems` - `needs` outside the
set -> problem with door; `needs` beside a pass/fail Then -> problem; `needs` on an item with no step and no `limitation` -> problem
("say what you would start and why in `limitation`"); `walk_record_of` copies `needs`. (4) the trigger, the question and the executor of
§2 in `driver_stage_s7.py` (`s7_extra_instance_step`, `s7_extra_instance_ask`, `s7_extra_instance_person`, `_answer_extra_instance`) and the
`take_answer` branch in `driver_machine.py`. (5) Registrations: `question-prices.json` `"s7.extra_instance": [{"answer": "start it",
"factory": "role_round", "person": "answer", "delivery": "waits"}, {"answer": "by hand", "factory": "record", "person": "your_checks",
"delivery": "not_known", "unverified": "the cases named above; they are left with you and the report lists them"}, {"answer": "stop",
"factory": "nothing", "person": "none", "delivery": "no"}]` (slots: `start it` {"role": "the runner"}, `by hand` {"what": "the cases
named above"}); `test_conductor_doors.py` `PINNED_ELSEWHERE["s7.extra_instance"] = "test_no_move_seam_sites.py (E7)"`; `driver-layers.json`
four rows (`home` driver_stage_s7, `row` 76, as the open_work rows); `audit_factory.py` `NO_MOVE_BASELINE` row `('driver_stage_s7.py',
'Driver._answer_extra_instance', 'P', 'builder:held_question'): 1` and `NO_MOVE_BASELINE_MAX` +1 with its reason in the comment;
dry exits: none owed (a keyed `closed_question`, `dry_exits.py` docstring lines 9-10) - `--check` proves it; `state-exits.md` § What the
driver keeps: rows `extra_instance_asked` (entered by the ask; out: the answer, or `stop` keeps it and the rerun asks again),
`extra_instance_held` (a refused registry write; out: the story ends, nothing reads it after), `extra_instance_rewalk` (counted on the
rework's registration; out: inert after the story), and § The run's own records: an unprepared record with `need` (entered by `--needs` or
a verdict's `needs`; out: a re-walk's newer record, or it stays an unprepared walk the report lists) - rows appended below line 69.

Edges (each with its invariant):
- record without `need` (before E7, or any other unprepared walk) -> `unprepared_rows` byte-identical, no question (INV: old records read as today).
- need on a prepared case -> honoured (F-N1 a); need outside the set, edited reason, need with `result` -> an issue, the record reads
  `inconclusive` with `evidence_errors` as any bad record (INV: a runner-written marker counts only in its closed, code-written form).
- `--needs` with `--not-walked` on a walked case -> today's refusal; unwalked with no `--not-walked` -> today's refusal (INV: what was not
  walked always says why). CLI `--needs ""`, unknown word, repeated flag -> argparse refusal (outside input battery).
- halted run (`broken_run`, `timeout`, `env_blocked`) with need records -> `failures_to_triage` Refusal, no question (INV i).
- registry unreadable -> asks (toward asking); the answer's write refused -> held for this story (INV: an answer is never lost and never
  silently widened to other stories).
- `stop` -> no row; asked again on rerun with a changed lead (INV: stop is not a no; FR-7).
- six owed cases -> block of 5, then 1 on the next entry; a re-walked case still owed -> triage (INV: one re-walk per case per answer; no loop).
- rework refused -> cases counted, line printed, triage (INV: nothing silent; the report lists them as unprepared walks).
- `seam_rework` pending -> no step, no triage this entry (INV iv).
- a need record NEWER than a yes row (the runner could not start one) -> not owed, triaged (INV: the runner's own failure after a yes is the analyst's).
Tests, strongest first (`test_no_move_seam_sites.py` keep 3230, one new function, rig of `u7_r9_s0_readiness_pays_no_conductor_turn`):
- test: test_no_move_seam_sites.py::e7_extra_instance_trigger row "need, no row -> one Person `extra_instance` (key s7.extra_instance, doors start it / by hand / stop), conductor calls 0, no analyst dispatch, text names the stand and every case" | expected from: §2 position INV ii, owner's word 17.11.2026
- test: same row "known yes, record older -> one rework S6 qa-runner on the cases, no Person; known no -> no Person, no rework, triage goes on" | expected from: §2 step 4-5, FR-7
- test: same row "answers: start it -> registry known authorized true by driver with the words whole; by hand -> false; stop -> no row, held, rerun asks with a changed lead; free words -> unread once" | expected from: §2 The answers, AR-24
- test: same row "halted run with a need -> Refusal, no Person; records without need -> no Person" | expected from: §2 INV i, both worlds
- test: same row "six owed -> 5 then 1; re-walked still owed -> triage, no second rework" | expected from: §E7-3 edges
- test: test_manual_evidence.py::<unprepared table> rows "need on a prepared case written and read `unprepared_only`; bad need / edited reason / need with result -> issue; no need -> unchanged rows; CLI battery" | expected from: F-N1 (a), §E7-3 edges
- test: test_walk_record.py rows "verdict `needs` -> write_unprepared(need), no build_record; needs + pass, bad word, no limitation unwalked -> verdict_problems" | expected from: F-N3 (a)
Not run locally (canon judges): `test_conductor_doors.py` (census K15), `test_driver_layers.py`, `test_audit_rules.py` (A27),
`test_judgment_census.py`, `test_story_run_*`, `test_state_exits.py` (if not fast: it is not in `slow_tests.json`, run it whole as a 4th
file only if the DoD cap allows - it does not: report line). Touched `story_run_common.py`: no.

## 4. Live proof (FR-33), row for `live-runs`

L8: a manual case that needs another instance on a stand with no answer asks once at S7 entry, naming the stand and the case; `start it` re-walks it;
the next story on that stand asks nothing and its runner brief says `authorized`; `revoke` makes the next need ask again.

## 5. Readers of every touched file (designer rule 7)

`owns_readers.py` block: NOT attached to this dispatch. Lead runs `python -B tools/owns_readers.py --paths <the three owns lists> --names
write_unprepared,unprepared_rows,record_from_walk,_validate_unprepared,verdict_problems,walk_record_of,manual_stand_lines,_stand_lines,
stage_S7,take_answer,instance_answer,EXTRA_INSTANCE_KEY,INSTANCE_NEEDS,NO_MOVE_BASELINE_MAX` and answers each line in the forms of critic
rule 24 Q13 (d). Hand reads (Grep over `scripts/`, tests excluded; positive control: the definitions found in the same call):
- `write_unprepared(`: CLI `manual_evidence.py:2224`, `record_from_walk:1621` -> change E7-3 (new optional arg; old calls unchanged).
- `unprepared_rows(`: `ledger.py:1668` (`unprepared_walks`) -> unchanged code; ledger rows of need records gain `need`, `ended_at`;
  `check_delivery.py::unprepared_records` reads that ledger key -> the E7-3 builder confirms extra keys are ignored, else a question.
- `record_from_walk(`: `driver_dispatch.py:1476` -> unchanged (signature same).
- `_validate_unprepared`: via `validate_manual_current` (`finalize_task.py:566` and others) -> changes E7-3 for need records only.
- `verdict_problems(` / `walk_record_of(`: `walk_session.py:1699, 1705` (`op_verdict`) -> unchanged signature.
- `manual_stand_lines(`: `app_card.py:156`, `brief_pack.py:4680` -> changes E7-2 (one appended line).
- `stage_S7` / `take_answer`: `driver_machine.py:1342-1355` loop dispatch (q1a) -> unchanged; `test_walk_account.py:183` source order -> unchanged by the placement after `open_work`.
- `question-prices.json`: `no_move.load_question_prices`, `test_conductor_doors.py` census, `dry_exits.py` -> changes E7-3.
- `conductor-actions.json` `actions`: the conductor prompt; `NM.reserved_tokens` reads `moves` only -> unchanged.
- `config-keys.json`: `project_knowledge._derive_keys`, `config_contract.config_keys` readers, `test_config_migration.knowledge_gaps` (dotted registry rows exempt) -> unchanged.
- `state-exits.md`: `test_state_exits.py`, test-layers `named_by` `:69` -> unchanged if rows are appended below line 69 and row 167 is edited in place.
- `architecture.md`: `tools/architecture_index.py` (AR lines), test-layers `named_by` `:256` -> unchanged (axis 7 line edited in place).
- `role-load.json`: `role_load.py`, `test_role_load.py`, audit A22 -> changes E7-2. `role-rules.json`: `role_rules.py`, `test_role_rules.py` -> E7-2.
- `audit_factory.py` baseline: A27 via `test_audit_rules.py` -> E7-3. `driver-layers.json`: `test_driver_layers.py` -> E7-3.
- `qa-runner.md`, `walk-charter.md`: inject map / role_load, role-rules registry -> E7-2.
Readers in `tools/`, `.githooks/`, `.claude/`: the tool block's job (KNOWN MISSES not run: no shell).

## 6. Small choices closed

- Key name `environments.extra_instance` (§6 proposal of r4); element = the need word (one answer per stand per need, F-E7-3), not the
  role's free words; value `{"authorized": bool}`, state `known` (stand facts are recorded `known` only, `record_problems`).
- The need words live in `project_knowledge.INSTANCE_NEEDS` (E7-1) so both E7-2 and E7-3 read one constant; a factory word, not a project
  difference (AR-1 not met).
- Tokens `start it`, `by hand` (`by hand` already means "you check these yourself" in `s6.walk_account`), `stop`; neither door is a move's
  token (`conductor-actions.json` moves: rework, approve, restart, go on, prepare the stand, retry, stop).
- A token answer is recorded by the driver (`by="driver"`), free words by the conductor through the CLI row: both through `record`.
- The re-walk is started by the S7 step for any yes (token or CLI), by the moment rule; not by the executor - one road for both.
- `call: False`: no paid conductor call at this site (model `s7_open_work_ask`); no `holds` (no deferral).
- E7-3 stays one node: the field merged without the trigger would let a need reach the analyst unanswered (breaks INV ii between merges).
- Stand per story via `stand_gaps.stand_name`; "several stands" = several stories, each asks once for its own stand.

## 7. Reading trail (18.11.2026, main)

Read: brief; r4 spec §1, §6, §11 (F-E7-1..3); digest t-1273 whole; `docs/TESTING.md` whole; `driver_stage_s7.py` 1-160, 440-530, 1030-1079;
`driver_machine.py` 600-707, 3370-3500; `driver_conductor.py` 600-690, 757-776; `driver_dispatch.py` 2849-2901, 3700-3799; `driver_s0.py`
551-565; `controller.py` 4027-4136 (+ Grep `MANUAL_BLOCK_CASES` 551, `manual_blocks` 636, `REPAIR_CAUSES` 280); `project_knowledge.py`
40-360, 430-1221; `manual_evidence.py` 1236-1275, 1476-1556, 1590-1629 (+ Grep `unprepared`); `coverage_contract.py` 748-782 (+ Grep);
`finalize_task.py` 530-579; `walk_session.py` 630-801; `brief_pack.py` 2876-2965, 4670-4694; `app_card.py` 130-179; `stand_gaps.py` 148-172;
`agents/qa-runner.md` whole; `references/walk-charter.md` whole; `role-commands.json` 1-46; `conductor-actions.json` 1-7, 40-139 (+ Grep
tokens, project_knowledge rows); `question-prices.json` Grep `s7.open_work`/`s6.`; `config-keys.json` Grep `knowledge`; `role-load.json`
whole; `role-rules.json` Grep qa-runner; `state-exits.md` 104-118, 155-209 (+ headings); `architecture.md` 33-72, 101-106, 173-197, 221-232;
`factory-rules.md` 146-165; `person-owned.json` Grep; `audit_factory.py` 1690-1719; `dry_exits.py` 1-110; `test_conductor_doors.py` Grep
K15/PINNED; `test_no_move_seam_sites.py` 460-499, 595-679; `test_config_migration.py` 370-410; `test-layers.json` 1-40 + keep rows of the
named files; `slow_tests.json` 1-12 + Greps (positive control `test_brief_pack.py` found by the same pattern shape).
Negative claims with controls: `manual_evidence.py unprepared` is not in `state-exits.md` (Grep, control: `manual_evidence\.py (unprepared|build)`
matched lines 70, 74); `test_manual_evidence/test_walk_record/test_walk_session/test_role_rules/test_role_load/test_project_knowledge/
test_state_exits` absent from `slow_tests.json` (control: `test_brief_pack.py` found by the same pattern). Not read: `check_delivery.py::
unprepared_records` (E7-3 builder confirms), `Driver.deferrable`, `brief_pack._stand_pick`, `audit_factory.a27_scan` internals.
Budget: the 250K warn was passed; reading stopped there.
