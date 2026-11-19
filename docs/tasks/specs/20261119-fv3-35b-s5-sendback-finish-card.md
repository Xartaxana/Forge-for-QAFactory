# FV3-35 part B (t-1552): the S5 critic's send-back finish is open work, not a bare `--not-complete`

Draft by designer. Node live-run-fvf/3/FV3-35 (B), F19. A fork-decided place is tagged [Fn] with the RECOMMENDED option (§6). Tree: main 261f9592.

## 0. Builder header (R11-f)

given: C:/QAFactory/forge-repo/docs/tasks/specs/reviews/t-1542-fv3-35-diagnosis.md (sections (a) Family B, (b) "B, product node", (d) d3);
this card (§1-§5); `driver_stage_s5.py::DriverStageS5.s5_review`, `::s5_window`, `::s5_close_debt`, `::s5_mechanical_round`;
`driver_stage_plan.py::completion_for` (S5 branch); `driver_dispatch.py::finish`, `::repair_limit_gate`, `::owe_route`, `::repair_answer`;
`story_step.py::_open_window_refusal`; `controller.py::validate` (accept branch, the "no role to close it" refusal), `::_closes_stage`;
`driver_core.py::OpenWork`, `::open_work_reason`; `acceptance.py::SUPERSEDED_WORD`, `::unresolved_has_word`;
`tests/test_story_run_repair_limit.py::rl2_real_controller`, `::f4_recovery_finish_owes_the_round`, `::rl7_recovery_road_asks`;
`tests/test_s5_parallel_admission.py::story`, `::bare_not_complete_on_true_last_refused`; `tests/test_story_step_decide.py::decide_door_checks` (T6)
owns:
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/driver_stage_s5.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/driver_stage_plan.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/driver_dispatch.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/story_step.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/acceptance.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/design/state-exits.md
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_story_run_repair_limit.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_story_step_decide.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/fixtures/driver-exits/known_red/s5.json
non-goals: no controller.py change (it already accepts `--not-complete --unresolved --reason`, :6003); no S4/S7 open-work change; no change to
`s5_open_windows`/`s5_todo` (F3); no fixture change of family A or C (FV3-35 A/C); no dry-world or stub change; no CHANGELOG line (the Lead's wave)
handoff: the builder's report to the Lead: the diff on its branch, the DoD output verbatim (last 30 lines), the `test:` lines not written, the
known_red rows removed (key, old -> new pins), the census and canon files "not run locally: <file>, canon judges"
edges: §3 (E1-E15), each with its invariant; positional: E3; temporal: E11
DoD: `python -B ai-packages/qa-factory/scripts/tests/test_story_step_decide.py` and `python -B ai-packages/qa-factory/scripts/tests/test_state_exits.py`
and the narrow call of the canon-class files: `python -B -c "import sys; sys.path[:0]=['ai-packages/qa-factory/scripts/tests']; import harness,
test_story_run_repair_limit as T, test_s5_parallel_admission as P, test_driver_chain as C; [f() for f in (T.sendback_last_window_real_controller,
T.f4_recovery_finish_owes_the_round, T.s5_critic_completion_table, T.rl7_recovery_road_asks, T.debt_on_an_owed_round_closes_the_window,
P.bare_not_complete_on_true_last_refused, P.own_round_last_window_same_as_today, C.closes_reads_given_dispatch, C.finish_flag_names_open_windows)];
harness.finish('FV3-35b narrow')"`; canon judges: test_story_run_repair_limit.py, test_judgment_census.py, test_scenario_dry_1.py --part exits:s5
test: test_story_run_repair_limit.py::sendback_last_window_real_controller (new row beside rl2_real_controller) | expected from: brief LEAD INTENT,
t-1542 (b) red-before, §3 E1
test: test_story_run_repair_limit.py::f4_recovery_finish_owes_the_round (variant column "only window": the recorded finish's complete gives
OpenWork(word)) | expected from: brief invariant "recovery gives the same OpenWork", §3 E5
test: test_story_run_repair_limit.py::s5_critic_completion_table (new table, rows of §2 C1) | expected from: §2 C1 table, §3 E2-E4, E6
test: test_story_step_decide.py::decide_door_checks T6 -> a two-row variant (`x` exit 2 as today; the reserved word reaches the controller)
| expected from: §2 C3, §3 E10, state-exits.md row "an S5 window accepted as unresolved"
test: test_scenario_dry_1.py --part exits:s5 rows s5.repair_limit/* (canon) | expected from: t-1542 (b) DoD, §3 E14
siblings: FV3-35 A (same file known_red/s5.json: merge in series); FV3-35 C (none in code); FV3-28 (round|fixed rows wait on this node);
FV3-25 (fork d1 of t-1542); FV3-33 (files only); AR-19 twins S4 `s4_critic_completion`/`cases_in_repair`, S7 `repairs_pending`: unchanged
readers: §4 (the word, both ways) and §5 (readers of every touched file)
designer: this file, once accepted

## 1. Scope, AR-n, variety

The defect (t-1542 run1, the Lead's fact): on the serial road the critic that sends the last (here the only) S5 window back finishes with a bare
`--not-complete` (`s5_review.closes` returns a bool; `finish` :839-848), the controller refuses it ("leaves S5 with no role to close it",
controller.py:6003-6011), the driver has no move, and the conductor is called. The same refusal meets the recovery road (`completion_for` S5
closes -> False) and the person's `round` answer (the critic is finished after the answer with `s5_window_closed` False). Live: every S5
send-back on the last window costs a conductor call and a question.

**Measured contradiction with the brief (load-bearing).** `finish` would send `--not-complete --unresolved <word> --reason`, and the CONTROLLER
accepts that, but `story_step.py::_open_window_refusal` (:1788-1799, called at :2460) refuses `--unresolved` with `--not-complete` ON S5 before
the controller is reached (t-721 D1; pinned by test_story_step_decide.py:68 T6 and test_story_step_gate.py:97; state-exits.md:34 "`--not-complete`
is refused with it"). So the brief's move does not land without a story_step change. [F1] decides it; the card carries option (a).

AR-n touched, with the change check each demands (in the DoD of §2):
- AR-13 (one reader): ONE predicate for the live finish and the recovery finish (`s5_critic_completion`, §2 C1); the word is one constant
  (`acceptance.S5_OPEN_WORD`, beside `SUPERSEDED_WORD`/`AWAITS_WORD`); "the route owes the author a round" is one function shared with `owe_route`.
  Check: grep the package for the literal word and for `"test_defect", "mechanical"` tuples in driver_*.py after the change: one site each.
- AR-19 (twins): S4 (`s4_critic_completion`, `cases_in_repair`) and S7 (`repairs_pending`) unchanged, named in the commit. AR-22 (producer <-> reader): §4 walks the word both ways; every reader is answered.
- AR-25 (every recorded state has a way out): new recorded state "S5 critic accepted with the open-work word"; way out = the author round
  (live), the owed `route` round (recovery), the person's answer; residual worlds E12/E13 named with [F3]/[F4]. Check: a state-exits.md row and
  row :34 rewritten; run test_state_exits.py.
- AR-17 (one seam): fewer conductor calls; every remaining stop still goes through the seam (E12, E13). No new driver stop.
- AR-28 (unknown never a pass): an unreadable count still asks `unknown` before the finish; OpenWork is never given on an unknown.
- AR-29 (census): checks altered — `story_step._open_window_refusal` (a refusal: class `shape`, owner data: the factory's own flag combination
  and a reserved token it wrote itself); `s5_critic_completion` (no refusal; it routes recorded data: the route of the critic's form and the
  person's recorded answer; class `shape`, owner data, the person's answer is intent read through `repair_answer`). Check: run
  test_judgment_census.py (canon judges); a census row is added only if the census asks for the new unit; a raised count is named (AR-20).
- AR-20 (ratchets): known_red/s5.json rows that go green are removed and `pins` lowered, each row named old -> new.
- Commit lines: the AR and `judgment:` lines in the form `tools/architecture_gate.py` checks (read it; no grammar copied here); judgment is `none`
  with its reason: no role content is classified, the critic's recorded form and the person's recorded answer are routed.
- variety: none -- the change is the driver's own bookkeeping of a critic's send-back; it reads no value of any project axis.

## 2. Changes

**C1 `driver_stage_s5.py` — one completion predicate.** New method `s5_critic_completion(route, answer, last) -> True | False | OpenWork`, the
body of today's `closes` with one more branch, called by `s5_review.closes` (live) and by the S5 branch of `completion_for` (recovery). ORDER is
the invariant ("a window the predicate closes is never reported as open work; open work is never given without a recorded owed move"):
1. `s5_window_closed(route, answer)` True -> `True` if the window is last, else `False` (today, byte for byte).
2. owed -> `OpenWork(acceptance.S5_OPEN_WORD, reason)`, WHATEVER `last` says [F2 (a)]. Owed = `route_owes_round(route)` (route action
   `test_defect` or `mechanical` with no `code`: the same rule `owe_route` applies today, moved into one function in driver_dispatch.py and
   called by both) OR `answer.get("token") in ("round", "fixed", "review")` (the person's answer for THIS dispatch, `repair_answer`).
3. else `False` (today: on a last window the controller refuses it, E2).
On the parallel road `last` (a callable) is read only in step 1: a raising `last()` never decides an OpenWork. `closes(text, dispatch="")` keeps its
signature (test_driver_chain.py:133 calls it both ways).

| route / answer of THIS dispatch | last | result |
|---|---|---|
| close, no code (approved) / none | yes | True |
| close, no code / none | no | False (+ `--open-windows` on a chain, today) |
| test_defect / none | yes, no | OpenWork(word) |
| mechanical / none | yes, no | OpenWork(word) |
| close, code cap / none (a road that skipped the gate) | yes | False (refused, E2) |
| close, code cap / `round` | yes | OpenWork(word) |
| close, code nobody / `review` or `fixed` | yes | OpenWork(word) |
| close, code cap / `debt` | yes | True (today) |
| test_defect / `debt` with `owed` (t-733) | yes | True (today) |

**C2 `driver_stage_plan.py::completion_for`, S5 branch.** Its inner `closes(digest)` returns `self.s5_critic_completion(route, answer, last)`
with `last` = the window walk it does today (True when it reaches the end of that walk). The early `return False` for a non-last window stays
for an approved window; for a send-back it moves after the route is read, so step 2 applies in any position [F2 (a)]. The serial and parallel
window walks are unchanged.

**C3 `story_step.py::_open_window_refusal`.** The S5 refusal stands for every word EXCEPT `acceptance.S5_OPEN_WORD`: with that word,
`--not-complete --unresolved <word> --reason <r>` reaches the controller [F1 (a)]. Signature unchanged (test_exit_gate_digest_fix.py:275 patches
it by name). Docstring: a third shape, "left open with work the driver owes", next to the two of t-721 D1.

**C4 `acceptance.py`.** `S5_OPEN_WORD = "tests_in_repair"` [F6 (a)] beside `SUPERSEDED_WORD`; comment: an S5 critic's send-back with a round owed.

**C5 reason text** (built in C1, one place): `open_work_reason(f"{critic or 'the critic'} sent the tests of {', '.join(cases) or 'this window'}
back; owed: {what}", f"… [list: work/handoffs/{critic}.yaml]")` where `what` is one of "a test_defect round of the author", "a mechanical round
of the author", "the round the person chose", "the review the person chose". Factory words only: no role prose, no digest text.

**C6 `design/state-exits.md`.** Row :34 loses "`--not-complete` is refused with it" for the reserved word (it stays for every other word); a new
row: state "an S5 critic accepted with `unresolved: tests_in_repair`", reached by the critic's send-back finish, way out: the author round
(live), the owed `route` round (recovery), the person's answer; residuals E12/E13 named; test `test_story_run_repair_limit.py`.

**C7 `known_red/s5.json`.** After the canon run: each `s5.repair_limit/*` row that passes is removed and `pins.known_red` lowered by the count,
each named in the report (key, old -> new); a row still red keeps its own measured FAIL text and a node, never "FV3-35".

`s5_mechanical_round` complete: UNCHANGED: the automator is no closing role of S5 (`dispatch_can_close_stage` False), its `--not-complete` is never
refused; on the last window `complete=last` closes S5 (`_mechanical_completion_problems` reads `status: accepted`, not `unresolved`).

## 3. Edges (each with its invariant)

| id | input / world | behaviour | invariant |
|---|---|---|---|
| E1 | the only window; critic `concerns`, blocking test_defect, counted 0 of cap 2 | finish `--not-complete --unresolved tests_in_repair --reason <C5>`; accepted; author rework (cause test_defect) dispatched; critic again; conductor count 0 | a send-back never costs a conductor call while the route owes a round; S5 never closes on a sent-back window |
| E2 | a truly last window, `complete=False` with no owed move (a seam route with no answer, on a road that skipped the gate) | bare `--not-complete`, refused as today | test_s5_parallel_admission.py:427 and :448 stay green byte for byte; no OpenWork without a recorded owed move |
| E3 | POSITION: `repair_limit_gate` (driver_dispatch.py:787) runs BEFORE `finish` on all three roads; the predicate runs inside `finish` | unchanged order; a seam route (cap, mech_cap, nobody, untyped, unknown, sent_back) with no answer is asked before any finish | no window is closed or kept open over an unasked seam; an unknown count is never a pass (AR-28) |
| E4 | the person's answer: `round`/`fixed`/`review` for THIS critic -> OpenWork; `debt` -> True; `stop` -> held, no finish; an answer for an earlier dispatch | `repair_answer` returns {} for another dispatch -> no owed answer | another dispatch's answer never opens or closes this window |
| E5 | recovery: `_finish_saved_result` -> `repair_limit_gate(recovering=True)` -> `owe_route` -> `finish(complete=completion_for(...))` | the same predicate -> the same OpenWork; `owe_route` still records token `route` first | live and recovery never disagree (one predicate, AR-13) |
| E6 | a non-last window sends back [F2 (a)] | OpenWork; `--open-windows` is NOT added (`finish`: the OpenWork branch is `if`, open_windows `elif`); an approved non-last window keeps today's road | `unresolved` and `open_windows` never travel together (controller.py:7330 refuses both) |
| E7 | mechanical route on the last window | critic OpenWork; then the author's mechanical round `complete=last` closes S5 | the mechanical close still finds an accepted critic of the same window |
| E8 | reason length | `open_work_reason`: at 300 kept whole; at 301 cut, ends with `… [list: work/handoffs/<critic>.yaml]` | the pair is never empty (an empty field becomes the refused bare finish); no gap word (`handed_to_person`, `blocked_by_env`, `probe_gap`, `contradicts_requirement`) enters through role text |
| E9 | empty: scope `[]`, critic id `""`, form absent | reason still non-empty ("the critic", "this window"); an absent/unreadable form or budget routes `untyped`/`unknown` -> asked (E3) | AR-28 |
| E10 | story_step door: S5, `--not-complete`, `--unresolved <w>` | `w == tests_in_repair` reaches the controller; any other `w` exit 2 as today (T6, gate test :97); the word without `--reason` refused by `_unresolved_refusal` first | t-721 D1 holds for every other word |
| E11 | TEMPORAL: before this commit no S5 record carries the word; after it, send-back critics do | a story in flight whose last critic was left RUNNING by today's refused finish: the next entry finishes it through the recovery road -> OpenWork -> accepted -> round; no migration, no record rewritten. The move that creates the word: the first send-back finish after the release | old records stay readable; the word appears only on a send-back finish |
| E12 | new world: the driver dies between the critic's OpenWork accept and the author's rework on the last window | not repaired here [F3]: every window has an accepted critic, S5 is open, `stage_S5` raises its L5 refusal; `recover`'s closure (controller.py:8770-8779) does NOT close S5, because the record names unresolved work | never a silent close over a sent-back window; the stop goes through the seam |
| E13 | new world: an owed round meets an unreadable count, the person answers `debt`, and this window is the last open one | `s5_close_debt` finishes an ACCEPTED critic; the controller refuses ("only the active dispatch can finish", :5950; `accepted` is not in SETTLED) -> seam [F4] | no silent close, no second debt entry (t-733 edges hold) |
| E14 | dry rows `s5.repair_limit/*` (cap 2: 3 critic calls, 2 author rounds) | the canon run decides each row; green rows leave known_red with pins lowered; red rows keep their own text | a green row still listed is refused as stale (AR-20); row cap 240 s (`ROW_CAP_EXITS`) |
| E15 | the person's `round` on the last window (old world: a refused finish) | the critic finish after the answer is OpenWork; `stage_S5` runs the owed round (`repair_owed`, token `round`) | the person's round is never lost to a refused finish |

## 4. The word, walked both ways (AR-22)

Producers of an S5 critic record's `unresolved`: P1 this card (OpenWork, `--not-complete`); P2 `finish`'s `window_gap` pair (`--complete` only);
P3 `story_step` derived pair (`complete` only); P4 the person's `decide --open` (`_open_pair`, ids); P5 a caller's typed pair (the conductor).
Readers of a dispatch record's `unresolved` / an accept payload's `unresolved` (production code), each answered:
- controller.py:5972 (reason required) — satisfied: C5 is never empty. Unchanged.
- controller.py:6003 (the "no role to close it" lift) — the intended reader. Unchanged.
- controller.py:7330 (`open_windows` with `unresolved` refused) — never both (E6). Unchanged.
- controller.py:7605-7666 (`names_handed/blocked/probe_gap/contradicts`, "unresolved window: ...") — reached only with `stage_complete` True
  (`s5_window`, :5988), never by a `--not-complete` finish; C5 carries no gap word anyway. Unchanged: the word is never an unresolved window.
- controller.py:8771 (`recover` closure) — the word bars it: a sent-back window is not a closure (E12). Unchanged code, new effect: intended.
- controller.py:5522 (`reconcile_dispatch`: successor without unresolved) — a send-back critic is no reconciliation successor, now also on
  non-last windows [F2]. Unchanged code.
- acceptance.py:1427 `unresolved_has_word` (exact token; callers :1455, :1494, :1526 with `stage_superseded` / `stage_awaits_acceptance`) —
  `tests_in_repair` matches neither; S5 has no acceptor (stages.json `acceptance_by` at :144, :222, :250 is not S5). Unchanged.
- driver_stage_plan.py:591-603 `stage_repair_owed` (substring `word in json.dumps`) — called only for S4 with `cases_in_repair`; no substring
  overlap with `tests_in_repair`. Unchanged.
- story_step.py:1788 `_open_window_refusal` — changes in C3. story_step.py:2540-2546 (`decided["open_work"]`) — keeps the caller's pair
  (`if not unresolved`). Unchanged.
- factory_dashboard.py:1457 — lists the `reason` of every dispatch with `unresolved` as a "gap" line, as it does S4's `cases_in_repair` and S7's
  `repairs_pending` today. Unchanged here; [F5].
- S5 window-debt readers (`ledger.read_review_debts`, `record_repair_debt`, driver state `repair_limit`) and `s5_open_windows` / `s5_todo` /
  `_s5_author_awaits_critic` read driver state or `status`/`role`/`accepted_by`, never a record's `unresolved`: the word is never a window debt.
- S8 readers (`report_facts`, `gate_brief.open_debts`, `check_delivery`, `delivery_summary`, `ledger`) read the manifest's `unresolved[]` and the
  review-debts file, never a dispatch record's `unresolved`: the word never reaches the report.
Reader -> producer: the one new reader (C3) reads only the constant C4, produced only by C1 (one function, two callers).

## 5. Readers of every touched file (rule 7)

The `owns_readers.py` block is NOT attached to the brief: hand greps below (trail §7); the Lead attaches the block before dispatch.
- driver_stage_s5.py (`s5_review.closes`, new `s5_critic_completion`): callers `finish` (accepts OpenWork, unchanged);
  test_driver_chain.py:133-159 (close route -> (True, True) last, (False, False) not last: unchanged rows). Unchanged / changes in this node.
- driver_stage_plan.py `completion_for`: 72 call/def hits in 21 files (`s5_review\(|completion_for\(|s5_window_closed\(`); S5 callers:
  driver_machine.py (recovery and resume roads), `s5_close_debt`, `resume_with_filed_words` — all hand the value to `finish`. rl7 rows
  (`closes` True after `debt`, False with no answer on a cap route, True on approve): unchanged by the table. Changes in this node only.
- driver_dispatch.py (`route_owes_round` extracted from `owe_route`): `owe_route` callers `repair_limit_gate` only. Unchanged behaviour.
- story_step.py `_open_window_refusal`: caller :2460; test_exit_gate_digest_fix.py:271-275 (patched by name); test_story_step_gate.py:97
  (`blocked_by_env` + `--not-complete` exit 2: unchanged); test_story_step_decide.py:68 (T6, `x`: unchanged). Changes in this node.
- acceptance.py (one constant): new readers story_step, driver_stage_s5, driver_stage_plan. No other stream touches it [estimate: Lead checks].
- design/state-exits.md: read by test_state_exits.py (run in the DoD). FV3-35 A/C do not touch it [estimate].
- known_red/s5.json: read by the dry harness (`known_red` loader); FV3-35 A edits the same file (14 rows, pins 57 -> 43): merge in series,
  pins recomputed by the second commit.

## 6. Forks (the Lead's)

- F1 (story_step refuses the brief's move; t-721 D1). (a) RECOMMENDED: C3, the one reserved word passes, every other word still refused;
  cost ~3 lines + one test row, state-exits row rewritten. (b) drop the S5 narrowing for every word (loses t-721 D1's guard). (c) the driver
  records the open work through `decide --open` (the person's door, P13: wrong owner) — rejected.
- F2 (the brief: "OpenWork over --open-windows on a non-last window?"). (a) RECOMMENDED: yes, every send-back is OpenWork in any position (one
  road, P31; the controller refuses both together anyway); approved non-last windows keep `--open-windows`. Cost: non-last send-back records
  carry the word (reconcile :5522 refuses them as successors). (b) OpenWork only on the last window; non-last keeps today's bare /
  `--open-windows` finish (two roads for one action).
- F3 (E12, a lost author round after an OpenWork accept; pre-existing on non-last windows, new on the last). (a) RECOMMENDED: a follow-up node
  FV3-35b2, owns driver_dispatch.py (`s5_open_windows` clause: a window whose last round is an accepted critic naming the word is open) and
  driver_stage_s5.py (`stage_S5` owes it as `route` from that critic's own `route_of`), test row in test_story_run_repair_limit.py beside f4.
  (b) inside this card (+~25 code, +~25 test lines; touches the TR4 predicates test_driver_chain.py pins).
- F4 (E13, debt on an owed round of the last open window whose critic is accepted). (a) RECOMMENDED: a node that closes S5 there (options for
  it: the controller's `recover` closure reads a review-debts entry naming that critic; or a fresh critic with the debt in its brief); this card
  pins only "refused, through the seam, never a silent close". (b) keep the word off a critic whose owed move is the person's `round`
  (smaller world, but E15 returns to the conductor).
- F5 (factory_dashboard.py:1457 shows the reason as a "gap" after the window closed, as for S4/S7): RECOMMENDED a dashboard-pile finding; or leave.
- F6 (t-1542 d3, the word). (a) RECOMMENDED: new `tests_in_repair`. Walk: `stage_in_repair` has one producer (`stage_review_exhausted`,
  S2/S3/S6/S7 — stages with an acceptor; S5 has none) and no reader by word in code (only test_stage_acceptance_consumer.py:537); reuse would be
  safe today, but it means "the conductor sent the stage back", per stage, while this means "this window owes a round", per window (F3's reader
  is per window); S4 kept its own word for the same reason. (b) reuse `stage_in_repair` (one fewer word; `stage_repair_owed` cannot read S5 per
  window).
- F7 (t-1542 d3, first half): a node inside the dry pile (this card) or its own pile with FV3-35 waiting. Open; no card change either way.
- Live proof (FR-33), a row the Lead files in the live-runs pile: "the next live run whose S5 critic sends a window back: the dispatch
  `S5-qa-code-critic-<n>` is accepted with `unresolved: tests_in_repair` (state/controller.json), the next S5 dispatch is a `qa-automator` rework
  with cause `test_defect`, and state/driver-questions.jsonl has no conductor row for that critic."

## 7. Small choices closed, estimates, trail

Closed: the predicate name `s5_critic_completion` (S4 twin `s4_critic_completion`); `route_owes_round` lives in driver_dispatch.py beside
`owe_route`; the word constant in acceptance.py beside its two siblings; the red-before row is a new function in test_story_run_repair_limit.py
(the brief's place; a row, not a file); DoD uses the import-and-call form (docs/TESTING.md:102) because these files run through `main()`.
Estimates (no shell; the Lead runs): (1) the package tests are not pytest-collected (`python -m pytest --collect-only -q
ai-packages/qa-factory/scripts/tests/test_story_run_repair_limit.py`), so no pytest node id exists; (2) the red-before row needs a story at S5
with one window and the real `story_step.py finish` (handoff form: `handoffs.required: false` in its config, or a form written by the row) —
`test_s5_parallel_admission.py::story` is the real-controller S5 fixture; (3) `harness.finish` exits non-zero on a FAIL line; (4) importing the
three test modules runs no `main()`.
Trail (all Read/Grep on the working tree):
- Read: t-1542 diagnosis (all); driver_stage_s5.py:360-539; driver_dispatch.py:770-869, 2949-3036, 3190-3340, 3430-3494; controller.py:100-125,
  480-546, 5505-5529, 5925-6040, 7304-7340, 7560-7829, 8745-8789; driver_stage_plan.py:560-619, 710-764, 1210-1340; story_step.py:1774-1799,
  2440-2479, 2525-2634, 2735-2764; acceptance.py:1410-1459; driver_core.py:168-192; factory_dashboard.py:1440-1469; gate_brief.py:4500-4531;
  stage_status.py:130-154; state-exits.md:30-41; architecture.md:1-100, 173-322; factory-rules.md:442-449; docs/TESTING.md:60-109;
  test_story_run_repair_limit.py:1-160, 338-407, 541-578, 640-960, 1190-1225; test_s5_parallel_admission.py:380-468;
  test_story_step_decide.py:30-89; test_driver_chain.py:130-160; test_story_step_finish.py:60-76, 150-189; slow_tests.json:1-12.
- Greps (Grep tool, scripts/*.py unless named): `get\(["']unresolved["']\)|\[["']unresolved["']\]` 250+ lines (paginated; production dispatch
  readers listed in §4); `(d|dispatch|record|rec|row|last|entry|item|x)\.get\(\s*["']unresolved["']|unresolved_has_word|stage_repair_owed\(`
  26 lines; `dispatches.*unresolved|unresolved.*dispatch` 23 lines; `names_(handed|blocked|probe_gap|contradicts)\(` 4 production sites
  (controller.py:7607-7644); `stage_in_repair|tests_in_repair` over the package: 2 hits (driver_stage_plan.py:761,
  test_stage_acceptance_consumer.py:537) — `tests_in_repair` absent, control: the same call found `stage_in_repair`; `open_windows` 60+ lines
  (no production reader of the record field besides controller.py:2246, 6003, 7313-7340); `acceptance_by` in references/stages.json: 3 rows;
  `^SETTLED|^TERMINAL|^STOPPED|^DISCOUNTED` in controller.py: SETTLED = {RETURNED, ABANDONED}; slow_tests.json: test_driver_chain.py 10.3,
  test_s5_parallel_admission.py 15.7, test_judgment_census.py 96.9; test_story_step_decide.py and test_state_exits.py absent (control: the
  same call found test_judgment_census.py); test-layers.json `canon_only` holds `test_story_run_*.py`; judgment-census.json has no
  `_open_window_refusal` row (control: the same call found story_step.py rows :1125-1132); known_red/s5.json `s5.repair_limit` rows :136-150
  (debt, stop, free words, empty).
- Not read: the dry world and stub; driver_machine.py (the recovery callers named by the diagnosis and by the count above).
