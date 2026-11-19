# FV3-35b3 (t-1587): a `debt` on the owed round of the last open S5 window closes S5 by code, not by a conductor stop

Draft by designer. Node live-run-fvf/3/FV3-35b3, F19. World E13 of the FV3-35b card (fork F4 (a), Lead 19.11). A fork-decided place is
tagged [Fn] with the RECOMMENDED option (§7). Tree: main a9bdd6d4 (FV3-35b merged, t-1559). Goes AFTER FV3-35b2 (t-1583): §6, [F4].

## 0. Builder header (R11-f)

given: C:/QAFactory/forge-repo/docs/tasks/specs/20261119-fv3-35b-s5-sendback-finish-card.md (§3 E12, E13; §4); this card (§1-§6);
`driver_stage_s5.py::DriverStageS5.stage_S5`, `::s5_close_debt`, `::s5_critic_completion`; `driver_dispatch.py::s5_open_windows`,
`::_s5_last_round`, `::repair_entry`, `::repair_debt_pending`, `::_answer_repair_limit`, `::record_repair_debt`, `::close_receipt`,
`::s5_release_of_dispatch`; `driver_core.py::CODE_CLOSE_SITES`; `stage_close.py::close_by_code`; `controller.py::Controller._s5_code_only_problems`,
`::validate` (`code_only` branch), `::stage_repairs`, `::repair_cause`, `::s5_part_of`, `::DISCOUNTED`; `ledger.py::read_review_debts`,
`::debt_entry`; `acceptance.py::S5_OPEN_WORD`, `::unresolved_has_word`, `::_s5_closed_by_code`, `::run_witness_excused`;
`tests/test_story_run_repair_limit.py::debt_on_an_owed_round_closes_the_window`, `::debt_on_an_owed_round_of_a_non_last_window`,
`::sendback_last_window_real_controller`, `::Rig`; `tests/test_controller_state.py::s5_code_only_is_closed_over_its_own_empty_derived_scope`;
`tests/test_check_witness.py` (the 5b block); `tests/test_s5_window_leftovers.py::closed_by_debt_then_rework_automator_not_refused`;
`tests/test_story_run_refusals_cc.py::refusal_cc9_every_close_of_s6_s7_s9_goes_through_the_one_record`; FV3-35b2's merged diff (t-1583)
owns:
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/controller.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/driver_stage_s5.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/driver_dispatch.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/driver_core.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/acceptance.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/design/state-exits.md
C:/QAFactory/forge-repo/ai-packages/qa-factory/changelog.d/fv3-35b3-s5-debt-close.md
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_story_run_repair_limit.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_controller_state.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_check_witness.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/fixtures/judgment-census.json
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/fixtures/driver-layers.json
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/fixtures/driver-exits/known_red/s5.json
non-goals: no change to the person's question, its offers or `_answer_repair_limit` (the `debt` answer and its review-debts entry stay as
t-733 wrote them); no change to `s5_critic_completion`, `story_step.py`, `recover`/`stage_repairs`, the S5 window-record tiers
(`_s5_completion_problems`) [F2]; no S4/S7 change; no fresh critic dispatch; judgment-census.json, driver-layers.json and known_red/s5.json
are touched ONLY when the canon asks (a census unit for a new raise site, a layer row for a new Driver member, a row named green)
handoff: the builder's report to the Lead: the diff on its branch (rebased on FV3-35b2's merge), the DoD output verbatim (last 30 lines),
the `test:` lines not written, "not run locally: <file>, canon judges" for each canon file, and where FV3-35b2's predicate took the C4 exception
edges: §4 (E1-E14), each with its invariant; positional: E9, E10; temporal: E12
DoD: `python -B ai-packages/qa-factory/scripts/tests/test_s5_window_leftovers.py` and `python -B ai-packages/qa-factory/scripts/tests/test_check_witness.py`
and `python -B ai-packages/qa-factory/scripts/tests/test_state_exits.py` and the narrow call of the canon-class files: `python -B -c "import sys;
sys.path[:0]=['ai-packages/qa-factory/scripts/tests']; import harness, test_story_run_repair_limit as T, test_controller_state as K,
test_story_run_refusals_cc as R; [f() for f in (T.debt_close_last_window_real_controller, T.debt_on_an_owed_round_closes_the_window,
T.debt_on_an_owed_round_of_a_non_last_window, T.sendback_last_window_real_controller, K.s5_code_only_is_closed_over_its_own_empty_derived_scope,
R.refusal_cc9_every_close_of_s6_s7_s9_goes_through_the_one_record)]; harness.finish('FV3-35b3 narrow')"`; canon judges: test_story_run_repair_limit.py,
test_controller_state.py, test_story_run_refusals_cc.py, test_judgment_census.py, test_scenario_dry_1.py --part exits:s5
test: test_story_run_repair_limit.py::debt_close_last_window_real_controller (new row beside sendback_last_window_real_controller, the same P.story
world) | expected from: brief (2) close rule, §3 C1-C3, §4 E1 (red before: the finish of an accepted critic is refused, controller.py:5950)
test: test_controller_state.py::s5_code_only_is_closed_over_its_own_empty_derived_scope (new rows of the existing table, §3 C1 gaps g0-g5)
| expected from: §3 C1, §4 E3, E5, E6, E7, E8, E10
test: test_story_run_repair_limit.py::debt_on_an_owed_round_closes_the_window (variant column "critic accepted with tests_in_repair": the code
close, no finish) and ::debt_on_an_owed_round_of_a_non_last_window (the same column: the window closes, B is reviewed next) | expected from:
§3 C2, §4 E2, E4, E9
test: test_check_witness.py 5b loop (one row: a debt close, an accepted S5 critic naming the word, an empty manifest -> no excuse) | expected
from: §3 C5, §4 E13
test: test_story_run_refusals_cc.py CC9 (unchanged function; the new literal site must be a key) | expected from: §3 C3
siblings: FV3-35b2 (t-1583, in build; same files driver_dispatch.py, driver_stage_s5.py, test_story_run_repair_limit.py: this node goes after
it, §6); FV3-35 A (known_red/s5.json: series); FV3-28 (round|fixed rows); AR-19 twins: S4 `s4_critic_completion`/`cases_in_repair` and S7
`repairs_pending`: unchanged [F7]; the U7 5b close `s5.nothing` (same controller admission, unchanged behaviour, E10)
readers: §5
designer: this file, once accepted

## 1. Scope, AR-n, variety

The world (FV3-35b card E13; measured on main): the last open window's critic was accepted as open work
(`--not-complete --unresolved tests_in_repair`, FV3-35b), its author round is owed (token `route` from `owe_route`, or the person's `round`),
the round cannot run (an unreadable count, `s5_window` :429-434) and the person answers `debt`. `_answer_repair_limit` writes the
review-debts entry (`record_repair_debt`, :3469) and the slot `{token: debt, owed: <route|round>, dispatch: <critic>}` (:3475-3479). The next
`stage_S5` entry calls `s5_close_debt` (:276-279), which `finish`es the critic with `complete=True`; the controller refuses it ("only the
active dispatch can finish; <id> is accepted", controller.py:5925-5951, `accepted` is not in `SETTLED` :211). No move is left: the
conductor is called. `recover` does not close it either (controller.py:8770-8771: a record naming unresolved work is no closure).

**Decision of the brief's item (1): the close lives in controller.py, the debt stays where it is recorded.** The debt is ALREADY recorded at
the person's answer, by the one writer `ledger.write_review_debt` (`work/review-debts.json`, the entry names `critic_dispatch`, `cases`,
`reason`, `rounds`, `choice`). What is missing is a road that closes S5 over it. Reason: the controller owns the stage close and already has
the code-close road (`code_only` receipt + `stage_done`, `stage_close.close_by_code`, used by `s5.nothing`); it reads the debt itself (AR-28,
never the request's word). The critic's brief is rejected: a fresh critic is a paid call over unchanged bytes, `repair_answer` keys the
answer by dispatch, so the new critic's own route sends the window back again (a loop), and steering a reviewer's verdict by a brief line
turns a recorded person's choice into role content [F1].

AR-n touched, with the check each demands (in the DoD):
- AR-13 (one reader): the review-debts file is read only through `ledger.read_review_debts`; "the last round of a window" is ONE walk: the
  body of `Driver._s5_last_round` moves to `controller.s5_last_round` and the driver's static method returns it (no copy); the cause through
  `controller.repair_cause`; the word through `acceptance.unresolved_has_word` + `S5_OPEN_WORD`; "this critic is accepted as open work" is
  one driver predicate read by `stage_S5` and `s5_close_debt`. Check: grep the package for `"S5_OPEN_WORD"` uses and for a second walk over
  `DISCOUNTED` beside `s5_last_round`: one site each.
- AR-17 (one seam): one conductor stop fewer; a refused debt close carries `close` (site `s5.debt_close`) and goes to the PERSON through
  `Driver.code_close` (no paid call), as every code-close site does. No new driver stop.
- AR-19 (twins): S4 and S7 unchanged, named in the commit [F7].
- AR-22 (producer <-> reader): new reader of `work/review-debts.json` (the controller); new row of `CODE_CLOSE_SITES` (read by
  `driver_machine.py:2160`, CC9); `stages.S5.code_only` now has a second producer, its one reader `acceptance._s5_closed_by_code` is answered
  (C5). §5 walks them.
- AR-25 (every recorded state has a way out): the state "S5 critic accepted with `tests_in_repair`, the person's `debt` on its owed round"
  gets its way out (the code close); state-exits.md row :35 loses this residual and names the road. Check: run test_state_exits.py.
- AR-28 (unknown never a pass): an unreadable debt record, an unreadable window list or an unreadable critic record is never a close (E5-E7).
- AR-29 (census): altered check `controller._s5_code_only_problems` (row exists: class `xref`, owner `data`; it now cross-references the
  controller's own records with the person's answer as RECORDED by its one writer - the person's intent read as data, no judgment). New
  `controller.s5_debt_close_gaps` returns a list (list transport: no census unit). A `raise Refusal` added in `s5_close_debt` (E6) is a new
  unit: its row `driver_stage_s5.py`/`s5_close_debt`, class `shape`, owner `data`. Check: test_judgment_census.py (canon judges); a raised
  count is named (AR-20).
- AR-20: no ratchet is raised; a `known_red/s5.json` row the canon names green is removed with `pins` lowered (key, old -> new in the report).
- Commit lines: the AR and `judgment:` lines in the form `tools/architecture_gate.py` checks (read it; no grammar copied here); `judgment: none`
  with its reason: the close reads the factory's records and the person's recorded answer; no role content is classified.
- variety: none -- the factory's own bookkeeping of an answer to an existing closed question; it reads no value of any project axis.

One road (P31): the repair-limit question exists only on the driver road (`story_step.py` has no `repair_limit`, count 0; control: the same
call finds 6 in driver_stage_s5.py), so no world of this card reaches the skill road; the controller admission is road-neutral (both roads
close through `code_only`).

## 2. The close rule (the brief's item 2)

S5 closes by code at the site `s5.debt_close` exactly when ALL hold, read fresh at the entry:
1. the driver state holds a pending debt (`repair_debt_pending`: token `debt`, `owed` set, not `finished`) for window W and critic K;
2. K's controller record is `accepted` and names `tests_in_repair` (`unresolved_has_word`) - the FV3-35b open work;
3. K is W's last round (`s5_last_round`): the round the debt replaced has not run;
4. no other window is open (`s5_open_windows(excluding=W)` is `[]`; unreadable is open);
5. the controller's own check passes (C1): every window's last round is accepted and closed, each critic naming the word is named by a
   readable `debt` entry of review-debts.json for the same cases.
The record says what is owed: the receipt's `reason` (C2) names the window, the critic and the round given up; the debt entry itself (its
`reason`, `rounds`, the person's words file) is the evidence the receipt hashes. If 1-3 hold and 4 does not, only the window closes
(`finished`), and the last remaining window closes S5 by its own critic (E4). If 3 fails, nothing closes (E2).

## 3. Changes

**C1 `controller.py` - the S5 code close over recorded debts.**
- Module function `s5_last_round(rows, cases) -> dict | None`: the body of `driver_dispatch.Driver._s5_last_round`, moved (AR-13); the driver's
  static method keeps its name and signature and returns `controller.s5_last_round(rows, cases)`.
- Module function `s5_debt_close_gaps(windows, rows, debts) -> list[str]` (pure; `windows` = `stage_scope("S5")["windows"]`, `rows` =
  `dispatch_identity.records(state["dispatches"])`, `debts` = `ledger.read_review_debts(root)`); `[]` = closable. Gaps, collected:
  g0 `debts["problem"]` non-empty: "the record of the repair-limit answers (work/review-debts.json) cannot be read: <problem>" - and
  nothing else is checked (a debt read from a damaged file is not trusted);
  per window, by its cases: g1 the last round is None or not `accepted`; g2 the last round is a `qa-automator` round whose `repair_cause`
  is not `mechanical` (an author round no critic reviewed) or a mechanical one with no `qa-code-critic` in `accepted_by`; g3 the last round
  is a critic naming `tests_in_repair` and no debt entry has stage `S5`, `critic_dispatch` == its id, sorted `cases` == the window's sorted
  scope and `choice.token` == `debt`;
  g4 no window's last round names the word: "no window is left over a review debt; S5 closes by its last critic's finish".
  A critic last round without the word is closed (today's meaning of an accepted window).
- `_s5_code_only_problems`: POSITION (E10): after the derived / `unmapped_scope` / `undisposed` checks, and only when those three found
  nothing and `scope` is non-empty, it calls `s5_debt_close_gaps`; `[]` -> no problem; else `why` = today's scope sentence ("cases ... are
  automate cases that need their tests written; S5 runs its author and critic for them") + the gaps. Any exception reading the debts or the
  rows is one gap with its type (refusal). The refusal prefix keeps "S5 only over its own empty derived plan scope" and adds ", or over windows
  the person left as review debts". `ledger` is imported inside the function (ledger does not import controller: measured, ledger.py:16-28).

**C2 `driver_stage_s5.py`.**
- New predicate `s5_debt_on_open_work(entry) -> bool`: the controller record of `entry["dispatch"]` is `accepted` and names `S5_OPEN_WORD`;
  any read failure -> False (today's finish road, which the controller judges). Read by both places below (AR-13).
- `stage_S5` :277: the condition gains one disjunct: `pending and (not todo or <critic not in accepted_by> or self.s5_debt_on_open_work(pending))`.
  POSITION (E9) unchanged: after `owed` (pending is `{}` while any round is owed) and before the D3 block and the L5 refusal.
- `s5_close_debt(entry, window)`: signature kept (test_s5_window_leftovers.py:267 calls it positionally). A new FIRST branch when
  `s5_debt_on_open_work(entry)`:
  (a) K is not W's last round (`_s5_last_round`): print one line ("the round the debt replaced for <cases> has already run (<id>); its review
  decides the window"), mark `finished`, save, return - nothing closed;
  (b) `s5_open_windows(excluding=cases)` raises: `raise Refusal("S5: the debt of <cases> is recorded, but the other windows cannot be read
  (<type>); S5 is not closed over them")`, `finished` NOT set;
  (c) another window is open: print one line, mark `finished`, save, return;
  (d) else `self.close_by_code("S5", reason, ["work/review-debts.json", f"work/handoffs/{K}.yaml"], finalize=False, site="s5.debt_close",
  digest=<one line>)`, then `self.s5_release_of_dispatch(K)` (the claims of a completed S5 are freed, as the finish road does), then mark
  `finished`, save. `close_by_code` on an S5 the controller holds `completed` writes nothing and returns True (stage_close.py:243-246).
  `reason` = "S5 closed over the person's review debt: the tests of <cases> stay rejected instead of <owed words> (critic <K>); every window
  left this way is in work/review-debts.json"; `<owed words>` = "the author's repair round" for `owed: route`, "the round the person chose"
  for `owed: round`. No truncation: the text is bounded by one window's case list.
  Without the predicate: today's body, byte for byte.

**C3 `driver_core.py::CODE_CLOSE_SITES`**: row `"s5.debt_close": ("S5", "the person left the tests of the last open window rejected, so S5
closed over that review debt")` (CC9 requires the literal site to be a key; `Driver.code_close` reads the words).

**C4 the exception in FV3-35b2's predicate (`driver_dispatch.py`).** FV3-35b2 makes "a window whose last round is an accepted critic naming
the word" open (`s5_open_windows`, `s5_todo`) and owed as `route` (`stage_S5`). That predicate gains ONE exception, at the one place it
lives after the merge: the driver state holds a `debt` slot for that window whose `dispatch` is that critic -
`self.repair_entry([window], lambda e: e.get("token") == "debt" and e.get("dispatch") == <critic id>)[0]` (the one scan, no new member).
Invariant: a window the person left as a debt is never reopened, never owed a round and never re-reviewed; a pending (unfinished) debt keeps
it open through the existing `repair_debt_pending` clause until C2 marks it.

**C5 `acceptance.py::_s5_closed_by_code`** additionally returns False when any accepted S5 dispatch names `S5_OPEN_WORD`
(`unresolved_has_word`), read from the same controller state. Invariant: a debt close never reads as "nothing to automate"
(`run_witness_excused` -> `nothing` stays bound to a close over an empty plan).

**C6 `design/state-exits.md`** row :35: the residual "a `debt` on an owed round of the last open window" is replaced by its way out: "the
person's `debt` closes the window; on the last open window S5 is closed by code (`s5.debt_close`, the controller reads the debt in
`work/review-debts.json`); a refused close is put to the person (`code_close`)". The other residual (the driver dying between the accept and
the round) is FV3-35b2's.

**C7 `changelog.d/fv3-35b3-s5-debt-close.md`**: one line, English, no Cyrillic (`selftest.py --lang`).

## 4. Edges (each with its invariant)

| id | input / world | behaviour | invariant |
|---|---|---|---|
| E1 | the only window; K accepted with the word; owed `route`; count unknown; the person answers `debt` | next entry: code close `s5.debt_close`, receipt + `stage_done`; S5 `completed`; K never finished again; `finished` set; no conductor row | a person's `debt` on the last window never costs a conductor call; S5 closes only over a debt the controller itself read |
| E2 | the owed round was ALREADY run (K is not W's last round: an author round after it, running or accepted) | C2 (a): nothing closed, `finished` set, the debt entry stays in review-debts.json; W is open (`_s5_author_awaits_critic` or running), its critic reviews next; C1 g1/g2 refuse a code close | a debt never closes S5 over an author round no critic reviewed |
| E3 | two windows owe (A and B, each K accepted with the word); the person answers `debt` for A | A's entry: C2 (c), A closed, nothing else; B's owed round runs; B's critic closes S5 by its own finish (A is closed: C4, `repair_debt_pending` false after `finished`) - or B also gets `debt` and B's entry is the last: code close; C1 checks BOTH debts (g3) | one window's debt never closes S5 while another window owes; every word-critic needs its own debt entry |
| E4 | a debt on a NON-last window (other windows not yet reviewed) | C2 (c): the window closes, the entry returns, the next entry reviews the others; the last of them closes S5 by its critic's finish | the debt window counts closed for `s5_last_fn` and `s5_open_flag` (no `--open-windows` naming it) |
| E5 | review-debts.json unreadable or absent AT THE CLOSE (it was written at the answer) | absent: `code_only_request` finds no evidence -> `Refused(title=code_only_evidence)` marked `close` step `evidence`; unreadable: C1 g0 refuses -> marked `close` step `receipt`; both go to the person through `Driver.code_close`; `finished` not set; the next entry retries | S5 never closes over a debt nobody can read (AR-28); the stop is the person's question, not the conductor |
| E6 | the window list or the controller state unreadable at C2 (b) | `Refusal` naming the read, `finished` not set | unreadable is open (FR-59); never a close, never a lost debt |
| E7 | the critic record unreadable or not naming the word (an older record, an accepted critic before FV3-35b) | `s5_debt_on_open_work` False -> today's t-733 finish road, byte for byte (the controller judges it) | the code close is reached only through the recorded open-work word |
| E8 | review-debts.json was unreadable at the ANSWER | unchanged: the held question "Your choice could not be recorded..." (:3469-3471), no slot written, nothing closes | no close without the person's recorded answer |
| E9 | POSITION in `stage_S5`: the new disjunct sits in today's condition, after `owed`, before D3 and L5 | an owed round of ANY window runs first (pending is `{}` while owed); the L5 refusal stays reachable when no debt is pending | a debt is never handled over an owed round; the factory's own-state refusal is not hidden |
| E10 | POSITION in `_s5_code_only_problems`: the debt check runs only after derived / unmapped / undisposed found nothing and `scope` is non-empty | `s5.nothing` (empty scope) closes exactly as before; an unreadable, unmapped or undisposed scope is refused first with today's text; the existing table rows stay green | the debt road never widens the empty-scope close and never runs over a scope nobody could read |
| E11 | the person answers later: (a) the question still open; (b) `debt` again after the close; (c) `round`/`fixed` after the close; (d) `stop` | (a) S5 waits on the held question, nothing closes; (b) "recorded already; nothing more is written" (:3441-3445); (c) the ask is gone -> `unread` -> the conductor once, S5 stays `completed`, a reopen is the controller's `rework` only; (d) held, nothing written | the factory never records a debt on its own (the owner of that choice is the person); a late answer never reopens S5 or writes a second debt |
| E12 | TEMPORAL: before this node a story in E1's world is stopped at the seam (refused finish); after it no record changes | the next entry after the release takes C2 (d); the first `s5.debt_close` receipt is created by that entry; no migration | old records stay readable; the site appears only on a close this node makes |
| E13 | a debt close over a manifest whose `tests` and `unresolved` are empty | `run_witness_excused` gives `""` (C5): the run witness is owed | a debt close never excuses a witness as "nothing to automate" |
| E14 | S5 already `completed` when C2 (d) runs (a refused `stage_done` retried, a parallel close) | no second receipt; claims released; `finished` set | one receipt per close |

Limits: the change introduces none (no cut, no count). Empty inputs: an empty `cases` cannot reach C2 (a window with no cases raises
`WindowsUnreadable`, E6); an empty critic id cannot be a pending slot (`repair_entry` matches by cases, the slot always carries `dispatch`).

## 5. Readers of every touched file (rule 7)

The `owns_readers.py` block is NOT attached to the brief; hand greps (trail §8). The Lead attaches `python -B tools/owns_readers.py --paths
<owns> --names _s5_code_only_problems,_s5_last_round,s5_close_debt,stage_S5,CODE_CLOSE_SITES,_s5_closed_by_code` before dispatch.
- controller.py `_s5_code_only_problems`: caller `validate` :6150-6151 (unchanged); census row judgment-census.json:214 (xref/data,
  unchanged class); test_controller_state.py:1900-1936 (rows unchanged, new rows here). New `s5_last_round`, `s5_debt_close_gaps`: readers
  this node only. `code_close_conflicts`, `code_close_facts`: unchanged.
- driver_dispatch.py `_s5_last_round` (now a delegate): callers :2991 (`s5_open_windows`), driver_stage_s5.py:95 (`s5_todo`), :302 (D3);
  driver-layers.json:1037 (unchanged row). Unchanged behaviour. FV3-35b2's predicate: changes in this node (C4), after its merge.
- driver_stage_s5.py `s5_close_debt`: caller `stage_S5` :278; test_s5_window_leftovers.py:217-271 (critic accepted WITHOUT the word: E7,
  today's road, stays green); driver-layers.json:573 (unchanged); test_driver_chain.py:1053 (docstring of the finish road: unchanged).
  `stage_S5`: every S5 story test; the disjunct is false for every record that does not name the word (E7). Changes in this node.
- driver_core.py `CODE_CLOSE_SITES`: driver_machine.py:2160 (the person's words of `code_close`: new row read, unchanged code);
  driver_stage_s6.py:183 (reads `s6.accepted`: unchanged); test_story_run_refusals_cc.py:541 (CC9: the new literal must be a key - it is);
  test_stage_acceptance_consumer.py:318 (S7 row: unchanged); driver-layers.json:80 (unchanged row).
- acceptance.py `_s5_closed_by_code`: caller `run_witness_excused` :672; test_check_witness.py:170-218 (rows unchanged: their states carry
  no dispatch naming the word; one row added).
- design/state-exits.md: test_state_exits.py (in the DoD). FV3-35b2 may edit row :35 too (its residual): merge in series.
- `work/review-debts.json` (no write here; a NEW reader): writer `ledger.write_review_debt` (unchanged); readers `ledger.attach_review_debts`
  (:1576, the delivery ledger behind the S8 report: lists each rejected test with the critic's remarks, unchanged), test_ledger.py,
  test_story_run_repair_limit.py, test_story_run_s7_live.py; driver_stage_s7.py:793 (S7 close evidence, unchanged); now controller.py (C1).
- `stages.S5.code_only` (a second producer): readers acceptance.py:648 (C5 answers it); s7_pretriage.py:339 and story_step.py:1184 read S6's
  entry only (unchanged).
- Who reads the debt later (the brief's item 1): the REPORT (S8, through `ledger.attach_review_debts`: each test of the window stays
  `review_rejected` with the critic's remarks and `repair_limit`); S6: no reader of review-debts.json (the readers above; no S6 module),
  it runs the manifest as for any t-733 debt window today; the NEXT story: no reader (the file lives under the story's own artifacts) [F6].

## 6. Order against FV3-35b2 (the brief's item 3)

Overlap: driver_dispatch.py, driver_stage_s5.py, test_story_run_repair_limit.py are FV3-35b2's owns too. Why it cannot be avoided: the
close lives in `s5_close_debt`/`stage_S5` (driver_stage_s5.py), and FV3-35b2's new "word-critic window is open / owed" predicate must not
reopen a debt window (C4) - without C4, E3 and E4 put the debt window back into `todo`, `stage_S5` reviews it again and the person's
choice is lost. So this node is dispatched AFTER t-1583 is accepted and merged, on a branch from that merge; C4 is written into the merged
predicate. If FV3-35b2 lands with no such predicate, C4 is a no-op and the report says so [F4].

## 7. Forks (the Lead's)

- F1 (item 1: where). (a) RECOMMENDED: controller.py `code_only` admission over the debt (C1) + driver code close `s5.debt_close` (C2);
  the debt is the existing review-debts entry. (b) lift `recover`'s closure bar (controller.py:8770-8771) for the word when a debt names the
  critic; the driver calls `recover`: `recover` is the factory's own-defect repair, and a person's debt is no defect; no receipt names the
  debt. (c) the critic's brief: a fresh critic told of the debt: a paid call, a loop (its own route sends back again), a verdict steered by
  the brief - rejected.
- F2 (the S5 window-record tiers). (a) RECOMMENDED: the debt close runs no window-record tiers (`_s5_completion_problems`), like `s5.nothing`
  and `recover`'s TP2-2553 closure; K's receipts were judged at its own accept (controller.py:5987-5992), and the window's tests stay
  rejected by the person's word. Cost: a probe gap or handed instance of the debt window is not refused at S5 (the report still lists the
  window). (b) build K's window record and run the tiers over it (+~40 lines; a refusal there is a stop again, and tier 4 refuses
  `unresolved window` for the rejected tests unless the pair names them).
- F3 (who chooses the debt; the brief reads "S5 closes by recording the debt"). (a) RECOMMENDED: only the person's recorded `debt` answer
  (the 35b card's E13, t-733; the factory does not decide to leave tests rejected). (b) the factory records the debt itself when the last
  window's owed round cannot run - this skips the person's question t-698 L3 made mandatory ("asked, never in silence").
- F4 (overlap with FV3-35b2, §6). (a) RECOMMENDED: series, after t-1583, C4 in its merged predicate. (b) add C4 to FV3-35b2 now (a
  mid-build change of t-1583) and keep this node off driver_dispatch.py.
- F5 (an unreadable entry elsewhere in review-debts.json, while K's own entry reads). (a) RECOMMENDED: refuse (g0; the file is damaged,
  AR-28; at S5 time only S5 entries exist, S7 writes later). (b) accept when K's entry reads (FR-41 keeps unread entries in place).
- F6 (the next story). (a) RECOMMENDED: no carry; the S8 report is the person's carrier, as for every t-733 debt today. (b) file a
  project finding per debt (`project_decisions.py add-finding`) so a later story sees rejected tests left in the product repository.
- F7 (AR-19 twin, another pile's zone): whether S4 has the same world (an S4 critic accepted with `cases_in_repair`, its round owed, the
  person's `go on`) was not measured. RECOMMENDED: a scout question for the Lead; no S4 change here.

**FR-33 live proof line** (the Lead files it in the live-runs pile): "The first live run where an S5 critic returns a window: the dispatch
`S5-qa-code-critic-<n>` is accepted with `unresolved: tests_in_repair` (state/controller.json), the next S5 dispatch of the same window is a
`qa-automator` rework with cause `test_defect` (its record's repair cause), and state/driver-questions.jsonl holds no conductor row for that
critic." The debt close itself is proven by the narrow rows until a live run meets it; an optional second line: "the first live run whose
S5 closes at site `s5.debt_close`: a `code_only` receipt for S5 whose evidence is work/review-debts.json, no conductor row".

## 8. Small choices closed, estimates, trail

Closed: the site id `s5.debt_close` (the `s5.nothing` pattern); the evidence pair (review-debts.json + K's form; a missing form is dropped
by `code_only_request`, the debts file alone stands); "last" by `s5_open_windows` at every N (the stricter reading; unreadable is open) -
not `len(todo)`, which cannot see a running dispatch; the moved walk keeps the driver's name (no caller changes); the strongest test is a
real-controller row in the P.story world of `sendback_last_window_real_controller` (a row, not a file); the rig variants extend the two
t-733 functions (the Rig's `controller_state` record carries no status, :83, so today's rows keep today's road).
Estimates (no shell; the Lead runs): (1) importing test_controller_state, test_story_run_refusals_cc and test_story_run_repair_limit runs
no `main()` (`python -B -c "import sys; sys.path[:0]=['ai-packages/qa-factory/scripts/tests']; import test_controller_state"` prints
nothing); (2) test_s5_window_leftovers.py, test_check_witness.py and test_state_exits.py are local-class (`python -B
ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <owns>` lists them in its first block); (3) `ledger` imports no
`controller` transitively (`python -B -c "import sys; sys.path[:0]=['ai-packages/qa-factory/scripts']; import ledger; print('controller' in
sys.modules)"` -> False); (4) the volume: ~90 product lines, ~80 test lines.
Facts added and measured (Read/Grep, working tree at a9bdd6d4): FV3-35b in main (acceptance.py:1424 `S5_OPEN_WORD`, driver_stage_s5.py:459,
story_step.py:1930-1933); the refusal controller.py:5925-5951, `SETTLED` :211, `DISCOUNTED` :219; `recover` bar :8770-8771; `code_only`
S5 admission :6130-6152 and `_s5_code_only_problems` :4298-4325; the reducer :1949-1951; `close_by_code` stage_close.py:234-257; CC9
test_story_run_refusals_cc.py:496-533; `CODE_CLOSE_SITES` driver_core.py:387-405; `_answer_repair_limit` driver_dispatch.py:3432-3482,
`record_repair_debt` :3491-3502, `s5_open_windows` :2951-2998, `_s5_last_round` :3011-3023; `stage_S5` driver_stage_s5.py:226-395,
`s5_close_debt` :531-542; ledger.py:1338-1460, :1567-1576, :1674; acceptance.py:640-676, :1423-1440; test-layers.json:13-18 (`canon_only`);
slow_tests.json :31 (test_controller_state 18.2), :68, :153; pile row plans/piles/live-run-fvf/batch-3-live-run-fvf.md:68-69.
Greps (Grep tool): `debt` -i in controller.py: 2 hits, none a reader (control: `code_only` found in the same file); `review-debts|review_debts|
open_debts` over scripts/*.py: 9 files, readers listed in §5; `repair_limit|s5_close_debt|repair_debt_pending` over scripts/*.py: 35 files,
story_step.py absent (control: driver_stage_s5.py 6); `get\(["']code_only["']\)` : 3 production readers; `CODE_CLOSE_SITES`: 11 lines;
`35b|review debt|tests_in_repair` -i in docs/SIBLING_MAP.md: none (control: `t-1583` found at :474, an unrelated id); judgment-census.json
has no `s5_close_debt`/`run_witness_excused` row (control: `_s5_code_only_problems` found at :214); `import controller` in contract.py and
ledger imports (ledger.py:16-28): none (control: driver_dispatch.py 11).
Not read: FV3-35b2's diff (in build); driver_machine.py beyond `code_close` :2084-2104; `stage_done.py`; the dry world.

## 9. Lead decisions (19.11.2026)

F1a, F2a, F3a, F4a (dispatch after FV3-35b2 t-1583 merges; C4 goes into its merged predicate), F5a, F6a, F7a (S4 twin is a scout
question, not this node). The FR-33 live proof lines are filed in the live-runs pile with the builder's accept.
