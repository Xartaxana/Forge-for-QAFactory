# Spec U7 / E7 r2 - another instance of the stand or device: asked once, when needed (t-1301, node universality/1/U1-11, F19)

Standalone: a builder dispatch is cut from this file alone; r1 (`20261118-u7-e7-another-instance-spec.md`) is not edited. Owner, 17.11.2026:
«спросить один раз, но не на онбординге, а тогда когда это понадобится». Decided, not reopened: F-E7-1..3 (r1 header), F-N1 = (a),
F-N2 = (a), F-N3 = (a) (architect 18.11.2026), Q1 = (a), Q2 = (b), Q3 = (a) (architect 18.11.2026, this dispatch). Base read: the working
tree at HEAD = origin/main = 6be36343 (`.git/refs/heads/main` and `.git/refs/remotes/origin/main` read; no shell, so no `git status` of the
package files: estimate, Lead confirms). 1b and its fix t-1292 F1 merged at e2ddb6d7 (review header); t-1294: status not verified.
Code is cited by `path::symbol`; the review's line numbers (e2ddb6d7) are not reused.

## R. Amendments of t-1295 and the decisions -> where placed in r2

| id | placed in | how |
|---|---|---|
| N1 | §2.3, E7-3b Work 3 | both worlds with their exact `complete=`; lines by source symbol; walk road through `walk_before` in `on_request`; seam rows A and B |
| N2 | §2.1, E7-3b Work 2 | every S7 entry, right before `if not analyst_done:`; invariants i-iv re-checked; second call site = fork F-r2-1 |
| N3 | §2.6, E7-3b Work 6 | need branch of `check_delivery.unprepared_records`; one world (7c in); words name the answer's world (Q1) |
| N4 | §2.2, E7-3a Work 1, E7-2 page | `--need-why` stored as `unprepared.need_why`; walk road: the verdict's `limitation` |
| N5 | §3 order, E7-3a Work 6 | way 1: `told-ratchet.json` joins E7-3a owns, `write_unprepared` bare 4 -> 5, named; green between every pair of merges |
| N6 | E7-3a Work 2 | markerless need record honoured only over a prepared, non-refused request with equal obligation ids |
| N7 | §2.3 | key `extra_instance_rewalk["<case>|<answer id>"]`; equal moments not owed |
| N8 | §2.4, edges of E7-1/3a/3b | lead cap 10 cases + "and K more"; runner words masked and cut at 300; batteries AT and BEYOND; `needs` checked against `write_unprepared`'s rules while the session lives |
| N9 | every DoD | exact commands; script-style files run `python -B`; narrow runs = pytest ids of `test_` wrappers (§6 C1); `test_state_exits.py` whole in E7-1, 3a, 3b |
| N10 | §2.4, §2.5, §2.7 | doors' `says`, every printed line, lead, conductor row, page and charter bullets written out |
| N11 | header, §5 | base 6be36343; §5 against the r2 block (base 76768bac); no `manual_evidence.py` line numbers kept |
| Q1 (a) | §2.6 | no verdict of its own: 7c's rule decides; the words say "the person said no" / "allowed, but not started: <why>" |
| Q2 (b) | §3 | E7-1 -> E7-3a -> E7-3b -> E7-2; `--needs`/`--need-why` hidden from help (`argparse.SUPPRESS`) until E7-2; the 3a window stated |
| Q3 (a) | §3 premise, E7-3b | words in E7-3b; one world (7c in); builder checks `manual_evidence.py::current_unprepared` at start |
| conflict | N2 vs §2.3 | N2's "with a known answer it is a no-op" holds for the question and a "no"; a "yes" still starts ONE re-walk per (case, answer) - N1's own subject. Read as: a known answer never raises the question |
| correction | N9, r1 DoD | r1 and the review ran `test_manual_evidence.py`, `test_state_exits.py`, `test_role_rules.py` with pytest: they hold no `test_` function (Grep `^def test_`: 0 each; control: 82 in test_project_knowledge.py), so pytest collects nothing. `harness.check` never raises (`harness.py::check` appends to `RESULTS`; `finish` exits 1): such files run as `python -B <file>`, a narrow run needs a wrapper that asserts |

## 0. Forks returned in r2 (each node drafted on the recommendation)

DECIDED (architect, 18.11.2026, t-1301 acceptance): F-r2-1 = (a) - the step is called a second time in `s7_repairs`, after the re-judge
loop and before the close; F-r2-2 = (a) - the S7 step writes `work/extra-instance.json`, delivery reads it. Size: the file is 57,914 bytes
(`wc -c`), over the 40,000-byte cap; accepted whole - every builder dispatch is cut as one node card plus §1 and §2, never the whole file.

ACCEPTED WITH AMENDMENTS for E7-3a, E7-3b, E7-2 (architect, 18.11.2026; plan review t-1307,
`docs/tasks/specs/reviews/t-1307-u7-e7-plan-r2.md`, section "Amendments"). The amendments M1-M18 of that review are part of this
spec in the review's own words; where a card and an amendment disagree, the amendment wins. A dispatch of a node carries its
amendments INLINE. By node:
- E7-3a: M3 (need fields only on a row with no `result`, no `evidence_errors`, no `current_reason`), M13 (`need_record_problems`
  never raises), M14 (`needs` plus a pass/fail Then at build time is refused into the `walk_retry` road), M16 (a wrapper judges
  only `harness.RESULTS[n:]`), and Q-B below.
- E7-3b: M1 (`driver_stage_plan.py` joins the owns; `completion_for` knows the re-walk ids), M4 (the A27 run is
  `python -B <package>/scripts/audit_factory.py --no-move`), M5 (a moment parses when `_moment(x) != float('-inf')`), M6 (the second
  call's arguments and return), M7 (`ALLOWED_LINE` written out, the review's words), M8 (need rows counted by case), M9 (below),
  M12 (test rows swapped and added as the review's section H lists), M15 (one note per case, latest wins; another schema reads `{}`),
  M17 (base re-read: the builder works on origin/main as cut), M18 (runner words shown as written after masking).
- E7-2: M2 (the skill twin `skills/qa-story/phases/s7.md` gets the same step; AR-19), M11 (the wrapper `test_ss1_11_stand_lessons`).
Decided: Q-A = (a) - the skill twin lands in E7-2. Q-B = (a) - the need branch of `check_delivery.unprepared_records` (HEAD words;
WORLD = "no answer about starting one was recorded") moves into E7-3a, so no false sentence reaches the person in the window
"3a merged, 3b not"; E7-3b then only adds the outcomes parameter and the run-file reader. M9 = the builder of E7-3b reads
`controller.py::_rerun_stamp`: if a person-chosen S6 rework does not stale the S7 analyst, the step is ALSO called before
`s7_closed_by_scribe` (INVARIANT: no `s7.accepted` close over a need with no answer); the builder reports which world holds.
E7-1 (merged separately) is outside these amendments; its own review is t-1311.

- **F-r2-1 - a need written inside S7's own re-judge round.** `driver_stage_s7.py::s7_repairs` runs `s7_rejudge_round` (a `rework` of S6) and then
  `s7_close` in the SAME call; a runner of that round may record `unprepared --needs`; the old triage row binds it (no attempt answers any row's
  attempt: review P2) and S7 closes unasked - N2's invariant broken by a road N2 does not name. (a) a second call of the same
  `s7_extra_instance_step` in `s7_repairs`, after the re-judge loop and before `if "open_work" in decided`; (b) accept it: the delivery words
  still name the case. **Recommend (a)** (one function, two positions, both under one invariant); cost: ~3 lines and one seam row.
- **F-r2-2 - where delivery reads the answer's world (Q1 words).** `unprepared_records(ledger)` sees only ledger rows. (a) the S7 step writes
  `work/extra-instance.json` `{"schema_version": 1, "cases": {case: {"answer": "no"|"yes", "why": "<clause>", "at"}}}` (one writer
  `Driver.s7_extra_instance_note`, one reader `check_delivery.extra_instance_outcomes`); (b) delivery reads `PK.instance_answer` by stand:
  no reason for a "yes" not started, a held (no-trace) answer invisible; (c) one generic sentence - contradicts Q1's words. **Recommend (a)**;
  cost: a run file with a state-exits row; `artifact-writers.json` row only if `test_artifact_writers.py` demands one (not verified, §7).

## 1. Architecture, owners, variety walk

| AR | how E7 meets it | change check (copied into the node DoD) |
|---|---|---|
| AR-3 | registry key `environments.extra_instance` (stand scope) in `config-keys.json` `knowledge`, read through `project_knowledge` | registry row only, no template row, no interview topic (owner 17.11.2026, r4 §6); `ask_when: null` (test_config_migration `knowledge_rows`) |
| AR-13 / AR-14 | one writer `PK.record`, one reader `PK.instance_answer`; need words one home `PK.INSTANCE_NEEDS`; one record writer `ME.write_unprepared` (both roads); one prepared-request reader `ME.prepared_request`; one need rule `ME.need_record_problems` (CLI, walk verdict, validator) | critic greps `environments.extra_instance`, `another_instance`: only config-keys, project_knowledge, tests, role text, the two helpers |
| AR-16 | key `s7.extra_instance` of `question-prices.json`, ONE literal `closed_question` | census K15 (`test_conductor_doors.py`, PINNED_ELSEWHERE) |
| AR-17 | the ask goes through `Driver.no_move` with `call: False` (model `s7_open_work_ask`); free words once through `unread` | A27: one baseline row, `NO_MOVE_BASELINE_MAX` +1, named |
| AR-22 | `need`, `need_why`, `ended_at`, `prepared` of `unprepared_rows` have readers (S7 step, delivery); `work/extra-instance.json` writer and reader in one commit (3b) | producer and reader named per field in the 3a / 3b commit |
| AR-24 | the person's answer words whole into `provenance.words` | E7-1 row 1, E7-3b row 4 |
| AR-25 | rows in `design/state-exits.md`: registry key (E7-1), need record (3a), driver keys and run file (3b) | each row with its way out |
| AR-27 | a need record reaches "Left with you" under its own words, owner factory (7c's kind) | E7-3b check_delivery rows |
| AR-20 | `qa-runner` rows of `role-load.json` rise by the measured amount | `role_load.py --role qa-runner` before/after in the report |
| AR-29 | checks are shape/xref; whether a case needs another instance is the runner's judgment, accepted by the person's answer | census rows: E7-3a owns `judgment-census.json` for `need_record_problems`; 3b stops with a question if a driver unit needs one |
| AR-1 | no project or platform word in code | diff adds no device-brand or OS word |

Checks added or altered (owner, census class): `PK.record_problems` branch (data, shape); `ME.need_record_problems` (data, shape; new
census row, roles qa-runner); `coverage_contract._validate_unprepared` (data, xref); `walk_session.verdict_problems` `needs` shape (data,
shape); the S7 step (data, xref: a typed need joined to a registry state). None refuses a role's content. Commit lines `architecture:` and
`judgment:` in the form `tools/architecture_gate.py` checks (the one carrier); each node `judgment: none -- a closed field joined to a registry
state; the need itself is the runner's judgment, accepted by the person's answer`, never bare.

Variety walk (architecture.md § A):
- axis 7: held by key|role -- registry key `environments.extra_instance` per stand + the runner's judgment of the need; unknown value -> nothing started, one question at S7 entry naming the stand and the cases; on `by hand` the cases go to the report as checks left with the person
- axis 2: held by role -- "another instance of the stand or device", no platform word; unknown value -> as axis 7
- axis 13: held by key -- the registry is append-only and carried by reinstall; unknown value (no row, unreadable file) -> asks once
- axes 1, 3, 4, 5, 6, 8, 9, 10, 11, 12: n/a -- no site of E7 reads the product language, test stack, flow, requirement source, delivery target, host, people, artifact language, task size or check kinds

No `narrows` line (F-N3 a: both roads). E7-1 edits the axis 7 line of `design/architecture.md` in place (test-layers `named_by` pins
`architecture.md:256`, `state-exits.md:69`).

## 2. Behaviour

**2.1 Position (N2).** `driver_stage_s7.py::stage_S7`: `s7_extra_instance_step(state, analyst_done, awaiting)` is called on EVERY entry right
before `if not analyst_done:` (after the freshness block); `True` -> `stage_S7` returns. INVARIANT: no S7 close (`s7.no_failures`,
`s7.pretriaged`, `s7_close`), no pre-triage row and no analyst dispatch over a need with no answer; a known answer never raises the question.
Re-check: (i) `s7_closed_by_scribe` and `consumer_settled` still come first; the entry refusal of `failures_to_triage` now comes AFTER the
position, so the step, once it has need rows, calls `self.failures_to_triage(awaiting=awaiting)` first and lets its `Refusal` rise (pure read;
a halted run is never turned into the question; no need row -> not called, so a story without need records runs as today). (ii) holds: the
position precedes the no-failures close, `s7_pretriage.pretriage`, the analyst and `s7_repairs`; with F-r2-1 (a) also the re-judge -> close
road. (iii) holds: a `known` row or a held answer never asks. (iv) holds by the loop: `seam_rework_step` runs before `where` in every
turn (`driver_machine.py` run loop), so a pending `seam_rework` never reaches `stage_S7`; the step does not test it. Runs on the re-triage path
and with an accepted fresh triage (the in-S7 rework world of review P2).

**2.2 The need record (E7-3a).** `ME.write_unprepared(task, case, observations, not_walked="", need="", need_why="")`. `need_record_problems(
task, case, need, need_why, marker) -> [problem]`, the ONE rule: need not in `PK.INSTANCE_NEEDS`; `need_why` blank (after `_squash`) with a
need; `need_why` without a need; no marker and `prepared_request` None. `write_unprepared` raises ONE `ValueError("; ".join(problems))`.
With a need: `need_why` cut at `NOT_WALKED_MAX` (300) with "…"; no marker -> obligations from `prepared_request`, `unprepared = {"reason":
NEED_REASON, "need", "need_why", walked...}`; marker -> its reason stays, `need`, `need_why` added. A need and no recorded walk: `not_walked`
defaults to `need_why` (what was not walked still says why). `NEED_REASON = "needs another instance of the stand or device; not started
without the person's word"`. `prepared_request(task, case) -> dict|None`: the case's `request.json` when it exists, reads, holds no `refused`
and no `unprepared`; else None. `unprepared_rows`: an entry gains `need`, `need_why`, `ended_at` (`attempt_ended_at`), `prepared` (reason ==
NEED_REASON) ONLY when the marker carries a need.

**2.3 The step** `Driver.s7_extra_instance_step(...) -> bool`:
1. rows = `ME.unprepared_rows(report)` with `need`. None -> False.
2. `failures_to_triage` (2.1 i). stand = `stand_gaps.stand_name(task_root)` (placeholder = none). For each need (sorted):
   answer = `PK.instance_answer(project, stand, need)`, else `state["extra_instance_held"]["<stand>|<need>"]`.
3. No answer (None: no row, revoked, unreadable, no stand) -> the question (2.4); several needs: the first unanswered.
4. Answer yes (answer id = `PK-n`, or `held:<at>`): owed = rows whose `ended_at` and the answer moment both parse
   (`environment_record._moment`), `ended_at` STRICTLY earlier, and no `extra_instance_rewalk["<case>|<answer id>"]`. Equal -> not owed.
   Unparseable -> not owed, printed line, note. A running S7 dispatch -> no re-walk this entry, nothing counted, False. Owed -> the first
   block of `controller.manual_blocks(owed)` (r1's read: `MANUAL_BLOCK_CASES`), ONE re-walk (below), True. Not owed and rewalk spent or need
   newer -> note, False.
5. Answer no -> note per case ("no"), `say_once` line, False (the analyst triages; delivery by 7c's rule).

Re-walk (N1). `self.rework("S6", "qa-runner", block, "S7 another instance: " + ", ".join(block), cause="question_answer", complete=C,
on_request=registered, extra=lines)` with `lines = []` filled by `registered`. WORLDS: **A** `awaiting` non-empty (S6 awaits its consumer):
`C = self.consumer_awaits("S6", True)` - an `OpenWork(acceptance.AWAITS_WORD, ...)` (`driver_stage_s6.py::consumer_awaits`); the re-walk is the
runner's LAST dispatch and carries the awaits word, so `acceptance.awaits_acceptance` holds for it and `controller.next` moves past S6 to S7
(controller.py X7-6 branch `if i < 9 and awaits_acceptance(...)`); the analyst's word then binds the new dispatch. **B** `awaiting` empty and
`stages.S6.status == "completed"` (in-S7 rework; no S6 consumer): `C = False`; S6 stays completed (`set_stage` monotonic,
`s7_rejudge_round` docstring). Neither -> no re-walk, printed line, note, False. INVARIANT: after the re-walk returns, `controller.next` is S7
and no S6 manual block is re-planned; `C` is never True. Back to S7: `rework` is synchronous (`run_role` inside it); the step returns True,
`stage_S7` returns, the next `where` is S7. `registered(id)`: (1) `extra_instance_rewalk["<case>|<answer id>"] = id` per case, `save_state`
(a crash costs one round, never two); (2) `walk = self.walk_before(block, id)` - the existing door (`driver_dispatch.py::walk_before`: needs
the registered dispatch, runs before the role; no `assigned`, the re-walk is one lane); (3) `lines += self.manual_block_lines(block, id, walk,
unprepared) + [ALLOWED_LINE] + self.role_lines("S6", "qa-runner")`. `rework` copies `extra` after `on_request` returns
(`driver_dispatch.py::rework`), so the lines name the road actually opened. `run_role`'s hook (`walk_reopen` finds `state/walks/<id>.json`,
leaves a live server alone, `after=walk_after`) closes the session and builds the records (`record_from_walk`, `finalize_task.py`); a walk
that did not open -> `walk_before` removed the record, the recorder lines go (FR-57). `manual_block_lines(block, dispatch, walk,
unprepared)` is EXTRACTED from `driver_stage_s6.py::run_manual_lane` (`record_then_role`, the non-assigned part): walking -> the `Execution
kind: manual — walk the items of walk session <id> ...` line (+ `Your last command: finalize_task.py ...` when `walk["report_last"]`);
not walking -> `Execution kind: manual — execute the approved manual-agent cases in this block, record each observation as manual
evidence, then `finalize_task.py <task root>`.`, `Prepared requests, one per case ...` and per factory-unprepared case its `<case>:
unprepared - <why>; ...` line (`unprepared` = rows of the block whose reason is not NEED_REASON). `run_manual_lane` calls it; its lines stay
byte-identical (one copy, Q6). `ReworkRefused` (raised before `on_request`, nothing counted): each case `extra_instance_rewalk[...] =
"refused"`, note, printed line, False.

**2.4 The question.** `s7_extra_instance_ask` -> `self.no_move({"why": "threshold", "kind": "extra_instance", "call": False, "stage": "S7",
"dispatch": "", "lead": lead, "site_doors": ("start it", "by hand"), "site_fallback": lambda said: self.s7_extra_instance_person(lead,
said)})`; `s7_extra_instance_person` -> `Person("extra_instance", self.closed_question("s7.extra_instance", lead, [start, by_hand,
dict(self.STOP_OPTION)]), "S7", "")`, NO `holds`. State `extra_instance_asked = {stand, need, cases, lead, at, stopped}`. Lead (kept
answer variant; `<words>` = `need_why` masked by `Driver.masked_words` and cut by `s0_quote` at 300 with "…"; at most 10 cases, sorted):

> `[You answered `stop` earlier. ]`<n> check(s) on the stand `<stand>` need another instance of the stand or device, which the factory has not
> started:
> - <case>: "<words>"
> - and <K> more (the report lists them all)
>
> Should the factory start one when a check needs it? Your answer is kept for the stand `<stand>` and is not asked again; to change it later,
> say `ask again`.

Story-only variant (no stand chosen, or a story that leaves no trace): "on the stand of this story" for "on the stand `<stand>`", and the
last sentence "Your answer holds for this story only." `masked_words(words) -> str` is EXTRACTED from `run_manual_lane`'s walk-supply
masking (`MC.secret_pattern_hit` with `guard_secrets._patterns`; a hit or an unreadable list -> `(not shown: they look like a secret)`).

Doors' `says`: `start it` - "the factory may start another instance of the stand or device on `<stand>` whenever a check needs one, now and in
later stories; the checks above are walked again now" (story-only: "... for this story only; the checks above are walked again now");
`by hand` - "the factory never starts one on `<stand>`; these checks and later ones like them are left for you to check and the report lists
them; say `ask again` to change it" (story-only: "the factory does not start one in this story; these checks are left for you to check and the
report lists them"); `stop` - `STOP_OPTION`. Slots: `start it` {"role": "the runner"}, `by hand` {"what": "the checks named above"}.

**2.5 The answers** (`elif kind == "extra_instance":` in `take_answer` right after the `open_work` branch; `_answer_extra_instance`):
`start it` / `by hand` -> `PK.record(key=EXTRA_INSTANCE_KEY, environment=stand, element=need, state="known", scope="stand",
value={"authorized": True|False}, words=<answer whole>, source="person", story, by="driver", where="S7 another-instance question",
task_root)`; refused write (no stand, no trace, unreadable) -> `extra_instance_held["<stand>|<need>"] = {authorized, words_file, at}`; then
`answer_row`, the asked record goes. `stop` -> nothing recorded, `stopped: True`, `raise self.held_question(self.stop_held("If you want to
answer after all, say `start it` or `by hand`."))`. Other words or no asked record -> `self.unread("extra_instance", ..., doors=("start it",
"by hand", "stop"), again=...)`; the conductor may run the `instance` row; its `continue` re-enters S7, step 3 reads the row.

**2.6 Delivery words (N3, Q1, E7-3b).** `unprepared_records(ledger, outcomes=None)`; a row with `need` (else today's words, byte-identical):
`to_check = HEAD + "; " + WORLD + "; what the runner would start and why: " + need_why` [+ `"; it was not walked either - not walked: " +
not_walked` when `walked` is False]. HEAD: `prepared` -> "the factory prepared this check, but it needs another instance of the stand or
device, which was not started"; else "the factory could not prepare this check (" + reason + ") and it needs another instance of the stand
or device, which was not started". WORLD = the outcome's `why`, or "no answer about starting one was recorded". `why` clauses (the note
writer): no -> "the person said the factory may not start one"; refused -> "the person allowed it, but the factory could not start the new
walk: <refusal, first line, 200>"; re-walked -> "the person allowed it; the runner walked it again and still could not start one"; newer ->
"the person allowed it, but the runner could not start one"; unparseable -> "the person allowed it, but the factory could not tell whether
the walk came before the answer"; neither world -> "the person allowed it, but the factory could not start a new walk from this stage".
Verdict: 7c's rule (walked -> `unprepared_walk`, `after_checks`; not walked or stale -> `no`).

**2.7 Printed lines (prefix `S7: `).** ask: "<n> check(s) need another instance of the stand or device on <stand> and nobody has said
whether the factory may start one; the person is asked". recorded: "the person's answer `<token>` about another instance on <stand> is
recorded (<PK-n>)". held: "the answer `<token>` about another instance is kept for this story only (<refusal>)". re-walk: "<cases> are walked
again with another instance of the stand or device on <stand> (the person allowed it)". refused: "the new walk of <cases> could not be
started (<refusal, 200>); they go on to triage as checks left with the person". unparseable: "<case>: the moment of its walk or of the answer
cannot be read, so it is not walked again; it goes on to triage as a check left with the person". no (`say_once`): "<cases> need another
instance on <stand>; the person's answer is not to start one, so they go on to triage as checks left with the person".

**2.8 Next story / revoke.** A known row -> no question; the runner's brief line says it (E7-2). `revoke --id PK-<n>` -> the row reads as
nothing, the next need asks; a new yes has a new id, so its re-walk is owed again (N7). Two stories at once: the later row wins.

## 3. Nodes. Order E7-1 -> E7-3a -> E7-3b -> E7-2 (Q2 b); 7b-B and 7c merge before E7-3a

TEMPORAL premise of 3a and 3b: cut after 7c merges, ONE world (7c in). At start each builder Greps `def current_unprepared` in
`manual_evidence.py`; no hit -> stop with a question, nothing built. Green between merges (N5, way 1): E7-1 touches no `told-ratchet.json`
unit (`project_knowledge.py` census rows are conductor-only: `test_stage_joints.reachable`); E7-3a adds ONE raise to `write_unprepared`
and its ceiling 4 -> 5 in the same commit (`bare` is a ceiling, only `rowless` is dense: `told-ratchet.json` note); E7-3b adds no site to
a ratchet unit (builder confirms: no new `raise` in `manual_evidence.py`, `coverage_contract.py`, `walk_session.py`); E7-2 changes text, a
count can only fall. Window 3a-without-3b: a runner that improvises the hidden `--needs` writes an honoured need record; S7 asks nobody;
the record is a triage target (`contract.triage_targets`) the analyst triages (`s7_pretriage` never code-triages an unprepared row);
delivery: walked -> `after_checks` with today's words carrying NEED_REASON, not walked -> `no`. No worse than today in what reaches the
person (triaged and listed, never silent); the one softening (`after_checks` instead of `no` on the runner's word) is the cost P8 named
and Q2 (b) accepted; the flag is in no page and no help until E7-2. Window 3b-without-E7-2: no page names the flag; the trigger fires only
on improvised records, as designed. Shared reads: `PK.instance_answer`, `PK.INSTANCE_NEEDS`, `PK.EXTRA_INSTANCE_KEY` (E7-1, frozen).

### E7-1 - registry key, reader, verb, conductor row

given: this spec §1, §2.5, §2.8; `project_knowledge.py::KEYS, record, record_problems, lessons, cmd_lesson, cmd_revoke, _story_stand, _write_prologue, main`; `references/config-keys.json` row `environments.stand_lessons`; `references/conductor-actions.json` stand-lesson and revoke rows; `design/state-exits.md` § What a person said about the product
owns:
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/project_knowledge.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/references/config-keys.json
C:/QAFactory/forge-repo/ai-packages/qa-factory/references/conductor-actions.json
C:/QAFactory/forge-repo/ai-packages/qa-factory/design/state-exits.md
C:/QAFactory/forge-repo/ai-packages/qa-factory/design/architecture.md
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_project_knowledge.py
non-goals: the record field, the trigger, the page, the brief line; any onboarding question; delivery words
handoff: branch + report (witness tails; the reader's signature as built; `not run locally: test_config_migration.py, canon judges`)
edges: below
DoD: `python -m pytest C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_project_knowledge.py -q` and `python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_state_exits.py`
siblings: `cmd_lesson` (twin verb: `_write_prologue` + `_story_stand`); `lessons` (twin pure reader); `cmd_revoke` branch "asked again"
designer: C:/QAFactory/forge-repo/docs/tasks/specs/20261118-u7-e7-another-instance-spec-r2.md

Work: (1) `config-keys.json` `knowledge`: `"environments.extra_instance": {"store": "registry", "compare": "exact", "scope": "stand",
"needed_by": ["project_knowledge.py:instance_answer", "brief_pack.py:instance_lines", "driver_stage_s7.py:s7_extra_instance_step"], "ask_when":
null}`. (2) `project_knowledge.py`: `EXTRA_INSTANCE_KEY`, `INSTANCE_NEEDS = ("another_instance",)`; `record_problems` branch for the key
before the role rules: element in `INSTANCE_NEEDS`, value exactly `{"authorized": bool}`; the empty-words door names `instance`.
`instance_answer(root, stand, need) -> {"authorized": True|False|None, "row", "problem", "no_stand"}`, PURE, never raises (shape of
`lessons`). Verb `instance --task <T> --allowed yes|no [--stand <name>] [--need another_instance] --words-file <f>` (`by="conductor"`;
prints `<need> on <stand>: environments.extra_instance recorded (PK-n)` / `already recorded (PK-n)`). `cmd_revoke`: the key joins the "asked
again where it is needed" branch. (3) `conductor-actions.json` row, twin of the stand-lesson row: says "the person says whether the factory
may start another instance of the stand or device when a check needs it (a yes or a no for the stand, meant for later stories too)"; run
`project_knowledge.py instance --task <T> --allowed yes|no [--stand <name>] --words-file <file holding their words>; a story that leaves no
trace refuses it`. The revoke row's says gains "or the answer about another instance". (4) `state-exits.md` § What a person said about the
product: the registry row's state list and entering commands name `instance`, its way out names revoke (the question speaks again at the
next need), edited in place. (5) `architecture.md` axis 7 line: append "; registry: another-instance answer per stand, asked once at the
moment of need (E7)" in place.

Edges (each with its invariant):
- absent registry -> None, no problem (INV: unknown asks once, never a yes); unreadable / other schema -> None with problem (INV: an unread
  registry is never a "no"); catalogue without the row -> None with `CATALOGUE_PROBLEM`; revoked -> None (INV: revoke makes it ask again).
- stand: `--stand` absent or `""` -> the chosen stand (`ns.stand or ""`); none chosen -> refusal listing the stands, nothing written;
  `--stand " "` -> `record_problems` refusal; a stand with spaces or non-ASCII is recorded as given and never read for another stand (INV:
  a misspelled stand errs toward asking, never toward starting).
- same answer twice -> `already recorded`; the other answer -> a new row that wins (INV: the latest row is in force).
- words (outside input, `person_words.read`): empty, BOM-only, whitespace-only -> refusal with door; UTF-16 / invalid UTF-8 -> refusal; a
  BOM -> stripped; no size limit: a 200 KB file is recorded whole (INV: AR-24, never cut); `--allowed YES` / `--allowed ""` and `--need`
  outside the set -> argparse refusal; no-trace story -> `NO_TRACE_WORDS`; all: nothing written.
- value `{"authorized": "yes"}`, an extra key, element `""` -> refusal, nothing written (INV: only a typed yes/no is ever read).

Tests, `test_project_knowledge.py` (pytest style), one parameterised table, strongest first (new rows ~14; budget: tests <= the ~75 added
product lines):
- test: test_project_knowledge.py::<instance table> "yes / no on the chosen stand read back by instance_answer, words whole; same twice -> already recorded; the other answer wins" | expected from: §2.5, owner 17.11.2026
- test: same table "absent / unreadable / revoked / no stand / placeholder -> authorized None (+ problem / no_stand)" | expected from: E7-1 edges
- test: same table "CLI battery: no stand chosen, `--stand \" \"`, empty / BOM / UTF-16 / 200 KB words, `--allowed YES`, bad `--need`, no-trace -> refusal or whole record as stated" | expected from: E7-1 edges, CLAUDE.md rule 11 (outside input)
- test: same table "value shape refusals" | expected from: E7-1 edges
- test: none -- the conductor row is read by the conductor's judgment | expected from: live L8 (§4)
Not written, by budget (in order): non-ASCII stand row, `--stand ""` row.

### E7-3a - the record field on both roads, the validator, walk_session, the record row

given: this spec §2.2, §3; `manual_evidence.py::write_unprepared, unprepared_request, unprepared_rows, record_from_walk, walk_rule_errors, _recorded_walks, _load_request, NOT_WALKED_MAX, main`; `coverage_contract.py::_validate_unprepared`; `walk_session.py::verdict_problems, walk_record_of, Walk.op_verdict`; `tests/fixtures/told-ratchet.json` unit `manual_evidence.py::write_unprepared`; `tests/fixtures/judgment-census.json` row `write_unprepared`; review t-1295 P1, P5, N4-N6, N8
owns:
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/manual_evidence.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/coverage_contract.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/walk_session.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/design/state-exits.md
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/fixtures/told-ratchet.json
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/fixtures/judgment-census.json
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_manual_evidence.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_walk_record.py
non-goals: the trigger, the question, delivery words (3b); 7c's `current_unprepared`; any role text or help naming the flags
handoff: branch + report (witness tails; the ratchet raise named `write_unprepared bare 4 -> 5: need_record_problems refusal`; lines `not run locally: test_stage_joints.py, test_judgment_census.py, canon judges`)
edges: below
DoD: `python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_manual_evidence.py`, `python -m pytest C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_walk_record.py -q` and `python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_state_exits.py`
siblings: `write_unprepared` callers (CLI `unprepared`, `record_from_walk`); `walk_rule_errors` (the build's rules while the session lives); `unprepared_request` (the marker reader, unchanged)
designer: C:/QAFactory/forge-repo/docs/tasks/specs/20261118-u7-e7-another-instance-spec-r2.md

Work: (1) `manual_evidence.py` per §2.2: `NEED_REASON`, `prepared_request`, `need_record_problems`, `write_unprepared(..., need="",
need_why="")`, `unprepared_rows` keys; CLI `unprepared --needs <word> --need-why "<words>"` (choices `PK.INSTANCE_NEEDS`, lazy import;
both `help=argparse.SUPPRESS` until E7-2). `record_from_walk`: a walk record with a str `needs` -> `write_unprepared(task, case, observations,
not_walked="", need=needs, need_why=limitation)` on either request kind, never `build_record`; the need kwargs are passed ONLY when `needs`
is present (the existing mock `lambda t, c, o, not_walked=""` in test_walk_record stays valid). `walk_rule_errors`: a record with `needs`
-> `need_record_problems(task, case, needs, limitation, unprepared_request(...))` plus "a check that needs another instance gives no Then a
pass or fail", INSTEAD of `_result_errors` (the one rule, while the session lives: P5 f). (2) `_validate_unprepared`: a marker with `need`
in `PK.INSTANCE_NEEDS`, `reason == ME.NEED_REASON` and no `unprepared_request` is honoured only when `ME.prepared_request` is not None and
the record's obligation ids equal the request's; else "unprepared marker without an unprepared request" (N6). Everything else as today.
(3) `walk_session.py`: `verdict_problems` - `needs` present and not a str in `PK.INSTANCE_NEEDS` (null, list, number, unknown word) ->
problem "`needs` is `another_instance` or absent"; `walk_record_of` copies a str `needs`. (4) `state-exits.md` § The run's own records: row
"an unprepared record with `need`" (entered by `unprepared --needs` or a verdict's `needs`; out: a newer record of the case, or it stays and
the report lists it), appended below line 69. (5) `judgment-census.json`: row `manual_evidence.py::need_record_problems`, class shape, roles
["qa-runner"], owner data. (6) `told-ratchet.json`: `manual_evidence.py::write_unprepared` `bare` 4 -> 5 (the one new raise).

Edges (each with its invariant):
- record without `need` -> `unprepared_rows` byte-identical, validator as today (INV: old records read as today).
- need on a prepared case -> honoured (F-N1 a); markerless with request missing / `refused` / other obligation ids -> issue (INV N6: a
  runner-written marker counts only over a request code prepared, with its obligations).
- need outside the set, an edited reason, a need with `result` or `then_quotes` -> issue; the record reads `inconclusive`, `evidence_errors`
  (INV: a runner-written marker counts only in its closed, code-written form).
- CLI battery (outside input): `--needs ""`, `--needs ANOTHER_INSTANCE`, repeated flag -> argparse refusal; `--need-why` blank or whitespace
  with `--needs`, `--need-why` without `--needs` -> the one refusal, nothing written; `--need-why` of 300 characters AT the limit -> kept
  whole, 301 BEYOND -> 299 + "…" (INV: the record never holds more than its limit and says it was cut); walked + `--not-walked` -> today's
  refusal; unwalked with a need and no `--not-walked` -> `not_walked` = `need_why` (INV: what was not walked always says why).
- walk verdict battery: `needs` null / list / number / unknown -> `verdict_problems`; `needs` + a pass or fail Then, or with no
  `limitation` -> `walk_rule_errors` refusal while the session lives (INV: a verdict the build would refuse is refused before the session
  ends); `needs` on a factory-unprepared case -> marker kept, need added.

Tests (new rows ~10; budget: tests <= ~95 added product lines):
- test: test_manual_evidence.py::f5_unprepared_cases rows "prepared case + need: record shape, validator honours it, unprepared_rows carries need/need_why/ended_at/prepared" | expected from: §2.2, F-N1 (a)
- test: same rows "markerless need over missing / refused / other-ids request -> issue" | expected from: N6
- test: same rows "bad need / edited reason / need with result -> issue; CLI battery incl. 300 / 301" | expected from: E7-3a edges
- test: same rows "no need -> rows byte-identical" | expected from: E7-3a edges (INV old records)
- test: test_walk_record.py::<table> "verdict needs -> write_unprepared(need, need_why=limitation), no build_record; verdict battery" | expected from: F-N3 (a), P5 f
Not written, by budget (in order): repeated-flag row, factory-unprepared + need row.

### E7-3b - the trigger, the question, the answers, the registrations, the delivery words

given: this spec §0-§2; `driver_stage_s7.py::stage_S7, s7_repairs, s7_open_work_ask, s7_open_work_person, _answer_open_work, s7_rejudge_round, failures_to_triage`; `driver_stage_s6.py::run_manual_lane, consumer_awaits`; `driver_dispatch.py::rework, walk_before, walk_reopen, run_role`; `driver_machine.py::take_answer`; `check_delivery.py::unprepared_records` and its caller; `controller.py::manual_blocks`; `question-prices.json` `s7.open_work`, `s6.walk_account`; `audit_factory.py` `NO_MOVE_BASELINE`; `test_no_move_seam_sites.py::u7_r9_s0_readiness_pays_no_conductor_turn` (rig)
owns:
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/driver_stage_s7.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/driver_stage_s6.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/driver_machine.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/check_delivery.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/references/question-prices.json
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/audit_factory.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/design/state-exits.md
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/fixtures/driver-layers.json
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_conductor_doors.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_no_move_seam_sites.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_check_delivery.py
non-goals: a road from a mid-S6 runner turn to the person (digest q2e); 7c's verdict rule; starting any instance by code; the page (E7-2); any line of `run_manual_lane` changed in its output
handoff: branch + report (witness tails; `dry_exits.py --check` tail; lines `not run locally: <file>, canon judges` for test_driver_layers, test_judgment_census, test_story_run_*)
edges: below
DoD: `python -m pytest C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_no_move_seam_sites.py::test_e7_extra_instance_trigger -q`, `python -m pytest C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_check_delivery.py::test_f5_unprepared_walk_is_a_left_item -q`, `python -m pytest C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_audit_rules.py::test_a27_baseline -q`, `python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_state_exits.py`, `python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/dry_exits.py --check`
siblings: `s7_rejudge_round` (S7 -> S6 rework); `s7_open_work_ask`/`_person`/`_answer_open_work` (site question); `_answer_walk_account` (`by hand`); `run_manual_lane` (lines, masking); `unprepared_records` readers
designer: C:/QAFactory/forge-repo/docs/tasks/specs/20261118-u7-e7-another-instance-spec-r2.md

Work: (1) start: the 7c check (§3). (2) §2.1 position; F-r2-1 (a) second call in `s7_repairs`. (3) §2.3 step and re-walk;
`driver_stage_s6.py`: extract `manual_block_lines` and `masked_words` from `run_manual_lane` (output byte-identical). (4) §2.4 question,
§2.5 answers, `take_answer` branch. (5) `s7_extra_instance_note` writes `work/extra-instance.json` atomically (F-r2-2 a). (6) §2.6:
`unprepared_records(ledger, outcomes=None)`, `extra_instance_outcomes(task_root) -> dict` (absent / unreadable -> `{}`), the call site in
`check_delivery` passes it. (7) Registrations: `question-prices.json` `"s7.extra_instance": [{"answer": "start it", "factory": "role_round",
"person": "answer", "delivery": "waits"}, {"answer": "by hand", "factory": "record", "person": "your_checks", "delivery": "not_known",
"unverified": "the checks named above; they are left with you and the report lists them"}, {"answer": "stop", "factory": "nothing", "person":
"none", "delivery": "no"}]`; `PINNED_ELSEWHERE["s7.extra_instance"] = "test_no_move_seam_sites.py (E7)"`; `driver-layers.json` rows (home
`driver_stage_s7`, row 76, as the open_work rows) for `s7_extra_instance_step`, `s7_extra_instance_ask`, `s7_extra_instance_person`,
`_answer_extra_instance`, `s7_extra_instance_note`, and (home `driver_stage_s6`) `manual_block_lines`, `masked_words`; `NO_MOVE_BASELINE`
row `('driver_stage_s7.py', 'Driver._answer_extra_instance', 'P', 'builder:held_question'): 1`, `NO_MOVE_BASELINE_MAX` +1 with its reason;
dry exits: none owed (keyed `closed_question`), `--check` proves it; `state-exits.md` § What the driver keeps: rows `extra_instance_asked`
(out: the answer; `stop` keeps it, the rerun asks), `extra_instance_held` (out: the story ends), `extra_instance_rewalk` (out: inert after
the story); § The run's own records: `work/extra-instance.json` (out: read at delivery, inert after). (8) Wrappers (§6 C1):
`test_e7_extra_instance_trigger`, `test_f5_unprepared_walk_is_a_left_item`.

Edges (each with its invariant):
- no need record -> no read beyond `run-report.json`, no `failures_to_triage` call, False (INV: stories without need run as today).
- halted run with need records -> `failures_to_triage` Refusal, no Person (INV i).
- registry unreadable -> asks; the answer's write refused -> held for this story (INV: an answer is never lost, never widened to other stories).
- lead: 10 cases AT the cap -> 10 lines, no "more" line; 11 BEYOND -> 10 + "and 1 more"; `need_why` of 300 kept, longer cut "…"; a secret-like
  `need_why` or an unreadable pattern list -> `(not shown: they look like a secret)` (INV: no runner word reaches the person unmasked).
- `stop` -> no row; rerun lead starts "You answered `stop` earlier." (INV: stop is not a no; FR-7).
- equal moments / need newer than the yes / unparseable -> not owed, note (INV: never a paid round on an unknown).
- six owed -> a block now, the rest next entry; key per (case, answer): no second re-walk under one answer; a revoke + new yes -> owed again
  (INV: one re-walk per case per answer; no loop).
- `ReworkRefused` -> counted `refused`, note, line, triage (INV: nothing silent); a running S7 dispatch -> no re-walk, nothing counted.
- neither world A nor B -> no re-walk (INV: S7 never passes `complete=True` for S6).
- walk does not open -> recorder lines (INV: the lines name the road opened); the re-walk's build refused -> the old need record stands,
  the case goes to triage with its re-walk spent.
- outcomes file absent / unreadable / case missing -> "no answer about starting one was recorded" (INV: delivery never says "allowed" or
  "said no" without a note).

Tests, strongest first (new rows ~12; budget: tests <= ~230 added product lines):
- test: test_no_move_seam_sites.py::e7_extra_instance_trigger row "world A (awaiting): need, no answer -> one Person `extra_instance` (doors start it / by hand / stop), conductor calls 0, no analyst dispatch, lead names stand and cases" | expected from: §2.1, N1, owner 17.11.2026
- test: same "world B (S6 completed, accepted fresh triage binds the need) -> Person, no s7_close" | expected from: N2
- test: same "known yes, record older: A -> one rework S6 qa-runner, complete is the awaits word, lines hold the finalize line and the allowed line; B -> complete False; known no -> no Person, no rework, note" | expected from: §2.3, N1
- test: same "answers: start it -> registry row by driver, words whole; by hand -> false; stop -> no row, held, rerun lead changed; free words -> unread once" | expected from: §2.5, AR-24
- test: same "halted run with a need -> Refusal; no need records -> no Person" | expected from: §2.1 (i)
- test: same "equal moments not owed; one re-walk per (case, answer); revoke + new yes -> owed" | expected from: N7
- test: test_check_delivery.py::f5_unprepared_walk_is_a_left_item rows "need + no / refused / no note -> the §2.6 words; no need -> today's words" | expected from: §2.6, Q1
- test: test_no_move_seam_sites.py::e7_extra_instance_trigger "11 cases -> 10 + more; secret need_why masked" | expected from: N8
- test: same "ReworkRefused -> counted, line, triage" | expected from: E7-3b edges
- test: same "walk road: walk_before called in on_request; not walking -> recorder lines" | expected from: N1 walk road
Not written, by budget (in order): F-r2-1 re-judge-round row, running-S7-dispatch row, neither-world row.

### E7-2 - runner page, walk charter, brief line, role-load, help text

given: this spec §2.2, §2.8 (contract: `--needs another_instance --need-why`, verdict `"needs"` + `limitation`, `PK.instance_answer`); `agents/qa-runner.md` § When to ask; `references/walk-charter.md` § After the steps; `brief_pack.py::stand_lesson_lines, manual_stand_lines, _stand_pick`; `app_card.py::_stand_lines`; `references/role-load.json`; `design/role-rules.json`; `manual_evidence.py::main` (the two hidden flags)
owns:
C:/QAFactory/forge-repo/ai-packages/qa-factory/agents/qa-runner.md
C:/QAFactory/forge-repo/ai-packages/qa-factory/references/walk-charter.md
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/brief_pack.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/app_card.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/manual_evidence.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/references/role-load.json
C:/QAFactory/forge-repo/ai-packages/qa-factory/design/role-rules.json
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_brief_pack.py
non-goals: the record field and the trigger; the registry; any platform word; the S5 brief head; any `manual_evidence.py` change but the two `help=` values
handoff: branch + report with the doc-dispatch witness script in full, `role_load.py --role qa-runner` before/after
edges: below
DoD: `python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_role_rules.py`, `python -m pytest C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_role_load.py -q` and `python -m pytest C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_brief_pack.py::test_ss1_11_stand_lessons -q`
siblings: `stand_lesson_lines` (the formatter `instance_lines` sits beside); `app_card._stand_lines` prefix filter (walk road); `brief_pack._stand_pick` vs `stand_gaps.stand_name` (two readers of the stand; a disagreement errs toward asking: review Q6)
designer: C:/QAFactory/forge-repo/docs/tasks/specs/20261118-u7-e7-another-instance-spec-r2.md

Work: (1) `qa-runner.md` § When to ask, one bullet: "When a check needs another instance of the stand or device than the one prepared:
if your brief says starting one is allowed, start it with the project's own actions and write what you started in `tried.md`; if it says
not allowed, or says nothing, do not start it. Record the check with the need instead: `manual_evidence.py unprepared --needs
another_instance --need-why \"<what you would start and why>\"` with what you tried, or in a walk verdict `\"needs\": \"another_instance\"`
with the same words in `limitation` and no pass or fail. The factory asks the person once and remembers the answer." (2) `walk-charter.md` §
After the steps: "A check that needs another instance of the stand or device, which your brief does not allow you to start: give the verdict
`\"needs\": \"another_instance\"`, say in `limitation` what you would start and why, and give no Then a pass or fail." (3)
`brief_pack.instance_lines(project, stand) -> list` through `PK.instance_answer` only: `- Another instance on <stand>: allowed (the person's
answer, given in <story> on <date>)` / `not allowed (...)` / `not answered yet` / `could not be read (<problem>)`; no stand -> `[]`; never
raises (an exception -> the `could not be read` line); `manual_stand_lines` appends it after `stand_lesson_lines`. (4) `app_card._stand_lines`
keeps lines starting `- Another instance`. (5) `role-rules.json` row `runner-another-instance-asks-once`: carriers `agents/qa-runner.md`
anchor "another instance of the stand or device", `references/walk-charter.md` anchor `"needs": "another_instance"`; source "owner
17.11.2026 (E7)". (6) `role-load.json` `ratchet_tokens.qa-runner`, `process_ratchet_tokens.qa-runner` = measured, the raise named (AR-20).
(7) `manual_evidence.py`: `--needs` / `--need-why` help texts "the need of a check that wants another instance of the stand or device" /
"what you would start and why" (SUPPRESS removed).

Edges (each with its invariant):
- registry unreadable -> the `could not be read` line (INV: an unread answer is never shown as allowed; the page then says do not start).
- no stand -> no line; "says nothing -> do not start it" decides (INV: silence never allows).
- revoked -> `not answered yet` (INV: revoke takes effect at the next brief).
- the line in both roads' stand text (manual brief and the walk's app card) (INV: one road, P31); page vs brief: the page defers to the line.

Tests (new rows ~4; budget: tests <= ~35 added product lines):
- test: test_brief_pack.py::ss1_11_stand_lessons rows "four registry states -> their line in manual_stand_lines and app_card._stand_lines; no stand -> no line" | expected from: E7-2 Work (3)-(4)
- test: test_role_rules.py (registry walk, the new row) | expected from: docs/TESTING.md «Правила ролей не теряются»
- test: test_role_load.py (rows equal the measured load) | expected from: role-load.json note
- test: none -- page and charter are role text | expected from: DOC-DISPATCH witness, keys K1 `another instance of the stand or device`, K2 `The factory asks the person once`, K3 `do not start it`, K4 `"needs": "another_instance"` (walk-charter.md), K5 `--need-why`; negative control: a deliberately absent key `start it anyway` must make the script report failure
Not run locally: `test_brief_pack.py` whole (canon judges; the pytest id above).

## 4. Live proof (FR-33), row for `live-runs`

L8: a manual check that needs another instance on a stand with no answer asks once at S7 entry, naming the stand and the check; `start it`
walks it again; the next story on that stand asks nothing and its runner brief says `allowed`; `revoke` makes the next need ask again.

## 5. Readers of every touched file (the r2 block, base 76768bac; HEAD is 6be36343: delta not read, §7)

- L2 test_audit_rules (NO_MOVE_BASELINE_MAX, slow): changes in 3b; computed from the sum (review miss 3); `test_a27_baseline` id in 3b DoD.
- L3 test_brief_pack (manual_stand_lines, slow): changes in E7-2 (rows + wrapper).
- L4 test_check_delivery (unprepared_records, slow): changes in 3b (rows + wrapper); the new parameter is optional, old calls unchanged.
- L5 test_conductor_doors (take_answer, slow): changes in 3b (PINNED_ELSEWHERE row only).
- L6-10, 13, 14, 16, 17, 19, 20, 22-24, 26, 29-32 (take_answer): unchanged - one `elif` after `open_work`, signature same; `test_walk_account`
  pins `walk_supply < walk_account < open_work` only.
- L11 test_ledger (unprepared_records): unchanged - reads cases and single fields; new keys only on need rows.
- L12 test_manual_evidence: changes in 3a (owned).
- L15, 18, 21 (stage_S7: s7_investigation_replay, story_run_refusals, story_run_s7; slow): unchanged for fixtures with no need record (the
  step returns False after one read); canon judges.
- L25 test_validator_class (verdict_problems): unchanged for verdicts with no `needs`.
- L27 test_walk_lanes (record_from_walk): unchanged - need kwargs only with `needs`.
- L28 test_walk_record: changes in 3a (owned).
- L33 artifact-writers.json (record_from_walk): unchanged; the new run file of 3b: §7.
- L34 null-outcomes.json NE7 (stage_S7 guard): unchanged - the analyst still writes the scribe form only for a triage.
- L35 driver-layers.json: changes in 3b (owned). L36 judgment-census.json: changes in 3a (owned); 3b stops with a question if needed.
- L37 project_knowledge.py: changes in E7-1, additive; existing keys unchanged. L38 config-keys.json: one row (E7-1); readers unchanged.
- L39 conductor-actions.json: one row + revoke says (E7-1); `NM.reserved_tokens` reads `moves` only, unchanged.
- L40 state-exits.md: E7-1 (in place), 3a and 3b (appended below line 69); `named_by` pins hold; `test_state_exits.py` in all three DoDs.
- L41 manual_evidence.py: 3a (additive), E7-2 (help values). L42 coverage_contract.py: 3a, markerless need records only; gap text reads
  NEED_REASON (review Q4). L43 walk_session.py: 3a. L44 driver_stage_s7.py, L45 driver_machine.py: 3b.
- L46 check_delivery.py: 3b. L47 question-prices.json: 3b (`load_question_prices`, census K15, `dry_exits`). L48 audit_factory.py: 3b.
- L49 brief_pack.py, L50 app_card.py, L51 qa-runner.md (role_load, inject map, role-rules), L52 walk-charter.md: E7-2.
- L53 told-ratchet.json: 3a (`test_stage_joints` K4, slow, canon).
- L54-62 (quarantined readers): not run, not fixed (quarantine rule). Code readers: `unprepared_rows` -> `ledger.build` (whole rows ->
  check_delivery, 3b); `record_from_walk` -> `walk_case_records` (unchanged); `stage_S7` -> the loop (unchanged); `take_answer` (16 code):
  unchanged signature; `unprepared_records` -> its one caller in check_delivery (3b); `NO_MOVE_BASELINE_MAX` -> A27 (3b).
- Review P7: `told-ratchet` (3a), `judgment-census` (3a), `ledger.unprepared_walks` keys (above), test_manual_evidence whole-row compare
  (need-less rows only: unchanged), test_walk_account order, `named_by` pins - all answered above.
- KNOWN MISSES of the block (not in its `--paths`/`--names`): `driver_stage_s6.py` and `run_manual_lane`, `walk_rule_errors`, `s7_repairs`
  (hand Grep `run_manual_lane|walk_rule_errors|\.s7_repairs\(` over the package: 14 files, among them test_walk_lanes_parallel,
  test_unprepared_outcome, test_story_run_s7, test_story_run_repair_limit: unchanged, the extracted lines are byte-identical and
  `walk_rule_errors` changes only for records with `needs`). The Lead re-runs `owns_readers.py` with these names on 6be36343.

## 6. Small choices closed

- C1 Narrow runs of script-style files: a `test_<name>` wrapper beside the scenario, `<name>(); assert all(ok for ok, _ in
  harness.RESULTS), [n for ok, n in harness.RESULTS if not ok]`; `main()` keeps calling the scenario. Whole runs of such files: `python -B`.
- Words: "allowed" (not "authorized") in every person- and runner-facing text; value key stays `authorized` (registry data).
- Key `environments.extra_instance`, element = need word, value `{"authorized": bool}`, state `known`; need words in `PK.INSTANCE_NEEDS`.
- Tokens `start it`, `by hand`, `stop` (no move token); `call: False`; no `holds`; token answers by the driver, free words by the conductor.
- The re-walk uses the default purpose and `cause="question_answer"` (the `s7_rejudge_round` road); the cut of `need_why` reuses `NOT_WALKED_MAX`.
- One raise in `write_unprepared` (joined problems) so N5 raises the ceiling by exactly one.

## 7. Open after r2 (not verified: no shell; every item is the builder's or the Lead's first check)

- not verified: the package files at 6be36343 are clean (git status); the delta 76768bac..6be36343 against these owns; t-1294 still open.
- not verified: pytest collects a `test_` wrapper from a script-style file without side effects; `test_audit_rules.py::test_a27_baseline`
  asserts (pytest style).
- not verified: `controller rework --stage S6 --cause question_answer` is accepted while S6 AWAITS its consumer (proven only with S6
  completed, `s7_rejudge_round`); and the awaits word on a rework dispatch without `execution_kind` passes `_s6_completion_problems`.
- not verified: nothing but S6 reads `walk_retry` after a re-walk's refused build; `test_artifact_writers.py` needs no row for
  `work/extra-instance.json` (a driver file not declared in `stages.json`).
- not verified: a human_text or question-length limit on a lead of 10 x 300 characters.
- not verified: `controller.manual_blocks` and `MANUAL_BLOCK_CASES` unchanged since r1's read.
- not verified: the K4 scanner of `test_stage_joints.py` counts one site per `raise` statement (so `bare` 4 -> 5 is exact); the builder
  reports the measured count.
- Size: this file is over the 40,000-byte cap of designer rule 8 (estimate ~54 KB from 454 non-empty lines; not measured, no shell; the Lead
  runs `python -B -c "import os,sys;print(os.path.getsize(sys.argv[1]))" <this path>`). Not trimmed: the dispatch asks for one whole
  standalone spec and the cut parts would be edges, texts or readers. `decomposable:` §R-§2 + §4-§8 (shared) | E7-1 card | E7-3a card |
  E7-3b card | E7-2 card - the owns of the cards are disjoint except `state-exits.md` (E7-1, 3a, 3b) and `manual_evidence.py` (3a, E7-2),
  both touched in merge order. The Lead decides (question 1 of the digest).
- Forks: F-r2-1, F-r2-2 (§0).

## 8. Reading trail (18.11.2026, working tree at 6be36343)

Read: brief; r1 whole; review t-1295 whole; readers block r2 whole; r4 §5-§6; `docs/TESTING.md` 70-144, 195-264; `driver_stage_s7.py`
1-175, 440-520, 1020-1089; `driver_dispatch.py` 619-728, 1100-1229, 1282-1481, 2849-2908 (+ Grep `walk_before|rework|run_role`);
`driver_stage_s6.py` 160-190, 1638-1727, 1809-1983; `driver_machine.py` 1925-1964, 3460-3484 (+ Grep); `controller.py` Grep
`awaits_acceptance(`; `manual_evidence.py` 1255-1304, 1500-1669 (+ Grep); `coverage_contract.py` 695-789; `check_delivery.py` 1895-1934 (+ Grep
callers); `ledger.py` Grep `unprepared_walks`; `walk_session.py` 632-801, 1690-1730; `project_knowledge.py` 440-490, 700-810, 900-1080 (+ Grep);
`environment_record.py` 60-80, 380-405; `person_words.py` 14-53; `driver_dialog.py` Grep `s0_quote`; `driver_core.py`, `driver_s0.py` Grep
`QUOTE_LIMIT|CUT`; `told-ratchet.json` 1-10, 344-350, 786-805 (+ Grep); `judgment-census.json` Grep; `test_stage_joints.py` 660-750 (+ Grep);
`harness.py` 100-239; `test_manual_evidence.py` 1280-1314; `test_no_move_seam_sites.py` 600-679; `test_walk_record.py` Grep `^def`;
`test_check_delivery.py` 2052-2070 (+ Grep); `test_conductor_doors.py` 640-680 (+ Grep); `test_audit_rules.py` Grep `test_a27`;
`tools/dispatch_manifest.py` 930-1038; `question-prices.json` Grep; `null-outcomes.json` 34-43; `driver-layers.json` Grep;
`artifact-writers.json` 1-6 (+ Grep); `architecture.md` Grep AR headings; `slow_tests.json` Greps.
Negative claims with controls: `current_unprepared` absent from the package (Grep; control `unprepared_rows` found by the same call, 7
files); `^def test_` 0 in test_manual_evidence, test_state_exits, test_role_rules, test_no_move_seam_sites, test_check_delivery, test_brief_pack
(control: 82 in test_project_knowledge, 30 in test_walk_record by the same pattern); test_state_exits, test_role_rules, test_manual_evidence,
test_walk_record, test_project_knowledge, test_role_load absent from `slow_tests.json` (control: test_brief_pack, test_check_delivery,
test_no_move_seam_sites, test_conductor_doors, test_config_migration, test_audit_rules, test_driver_layers, test_stage_joints,
test_judgment_census found by the same Grep shape). t-1294: Grep over `docs/tasks` found none, but the control (t-1295, known in a spec)
found only a snapshot (the Grep tool skips ignored paths), so its status is labelled not verified.
