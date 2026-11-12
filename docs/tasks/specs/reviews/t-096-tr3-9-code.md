# t-096 — critic on the landed code of TR3-9 (S6 walker lanes), node thinking-roles/3/TR3-9, F17

Reviewed: the state of `main` (HEAD 90c02d4) against spec `docs/tasks/specs/t-2147-tr3-9-walker-lanes.md` parts A, B, D, C0, C1, C2 and §3.
The code landed through merge 5498318, and its history is squashed: `git cat-file -t 124d8c966` (the C0 capture commit the spec names)
answers "Not a valid object name", so the review covers the landed state, not a diff. TR3-10d code sits on top of the same functions,
and I name it where it changes a TR3-9 answer. Successor files: the driver was cut on 11.11. The S6 lanes are in
`scripts/driver_stage_s6.py:1228-1827`, the S5 call in `driver_stage_s5.py:222`, `s6_walkers_cap` in `driver_dispatch.py:3853`,
`walk_before`/`walk_after` in `driver_dispatch.py:1078/1303`, and the launcher in `driver_runner.py:669-726`.

**Verdict: NEEDS WORK (fit_with_fixes). 1 finding blocks acceptance of the node (B1), 5 fixes, 3 queue items.**
Acceptance itself is the Lead's decision. This verdict is an input to it.

## Findings

**B1 (blocks acceptance of C.1): the only proof of "`walkers: 1` = the road before lanes" is red and quarantined.**
`scripts/tests/test-layers.json:9928-9936` puts `test_story_run_s6_w1_frozen.py` under `quarantine` (cohort 8073673, entered 2026-11-11,
`"red_at_entry": true` at commit 5498318). The Lead's F3 ruling (spec :432-434) says that only the captured set proves walkers-1 parity,
and C.1 (spec :334-336) names it as the proof. The snapshot `docs/tasks/compact-snapshots/2026-11-12-1210-manual.md:46-48` also expects
it to turn red again after PC2-3 (the "budget B" label against `BRIEF_BYTES`, test :158). The cause of the first red is not on record.
`ci-out/` holds no run of the file: grep `test_story_run_s6_w1_frozen` over `ci-out` is empty, while the same grep finds
`test_walk_lanes_parallel` in 8 logs. The fast key `walkers_1_takes_old_road_no_thread` (test_walk_lanes_parallel.py:235-246) proves
only the structure: no thread, no flag, no new state key, not complete. It does not prove calls, events or console byte for byte.
By reading, the old road still differs from the pre-lane body in at least two places: `self.boundary = "S6"` (driver_stage_s6.py:1667)
and `walk_next_id(..., len(prior) + 1, reserved)` in place of `len(prior)+1` (:1703). Either one may be what the frozen set caught.
Fix: read the red lines (quarantine-watch, or one CI run of the file per RUNBOOK §7), name the cause, then repair the code or recapture
with a reason. The file goes back to `keep`, or the Lead records that parity is proven some other way. Owner: the Lead (node TR3-9).

**F1 (fix): `_holder_would_refuse` knows only the S5 clause. An admitted S6 lane runs the dead-holder repair over its running siblings.**
`controller.py:4989` and `:4995` call `_window_beside_running` alone. Trace for a second lane that `validate` admits
(`:5449-5450` has `or self._lane_beside_running`): `running=[lane 1]`, op `dispatch`, no replay, then `_window_beside_running` gives
False because `window_like` needs S5 (`:6287`), so `_holder_would_refuse` gives True, and `apply` runs `close_settled(current)`
(`:5013-5022`) over every running row. That breaks the B1 invariant the comment states ("an admitted S5 window never touches its
siblings", `:5016-5017`), and the docstring (`:4973-4974`, "the same call `validate` and `_resume_problems` make") is now false, since
both of those make two calls. Consequence, bounded but not reproduced: liveness reads "alive"/"unknown" as no change. A sibling in its
backoff (`driver_runner.py:938`, unbooked, no process, `in_flight` cleared) is the only window in which a provably-over verdict could
close a lane the driver still holds. Fix: add `or self._lane_beside_running(...)` at both sites, plus one admission key "an admitted lane
never runs close_settled". This is the S5-to-S6 twin miss of TR4-7 (Q5).

**F2 (fix, Lead-tier): the SIBLING_MAP rows for the twin were never written.** Spec §2 C AR-n (:376-377) says "Lead writes axis 5 /
axis 33 rows — decision 3, in C's commit", and axis 33's own symmetry line says "the S6 twin (walkers, TR3-9) joins this row in its own
commit". A grep `_s6_runner_half|S6 lanes|s6_lane` over `docs/SIBLING_MAP.md` is empty. Control: the same grep for
`s5_precheck.running_dispatch` hits :575. A grep `lane|_window_beside_running` finds only the code-only close row :125. With no axis 5
row "S5 windows <-> S6 lanes", the next S5-window fix has no pointer to its twin. F1 is the instance that proves it.

**F3 (fix before release): the changelog fragments contradict each other.** `changelog.d/tr3-9c-walker-lanes.md:1` says "a story whose
manual cases are all guest cases still runs one walker at a time, because guests share one account". `tr3-10c-pool-and-claims.md`
(`guest#<lane>` per guest lane) and the key `guest_lanes_side_by_side_when_data_disjoint` (test_walk_lanes_parallel.py:920-930) say
otherwise. Both fragments are unreleased, so one CHANGELOG entry would say both things (FR-10). Fix: amend the guest sentence of the
tr3-9c fragment.

**F4 (fix): two keys cannot go red for the defect they are named for (tests, Q4).** `same_account_lanes_in_turn`
(test_walk_lanes_parallel.py:280-293) checks `seen.most == 1` with sessions that hold nothing (`with seen.at_work(): pass`). If the gate
were broken, two instant sessions would still rarely overlap, so the key goes green for the wrong reason. Its guest half (:290-293)
asserts only `done_cases`, not "in turn", so its message lies. `overlapping_part_sets_in_turn` has the same empty session and a stray
first `enter` (:308) whose result is thrown away. Fix: hold lane 1's session on an event that lane 2's start would trip (the
`close_exactly_once_order_free` pattern), and assert the order. The key that DOES kill the defect is
`same_account_second_lane_never_registers` (:536-541, the fake controller records `prior.done` at `apply`), and its killing power
depends on thread timing.

**F5 (fix, residual named): role-invoked `finalize_task` runs unbooked, beside booked reductions.** The recorder road brief tells the
walker to run `finalize_task.py` (driver_stage_s6.py:1807), and so does `report_last` (:1768). Those runs happen inside the role session,
outside `_book`, while another lane's `walk_after` reduces under `_book` (driver_dispatch.py:1349). `finalize_task.py` is a whole-story
reducer over immutable blocks with `atomic_json` writes (:750-752). That meets the spec's C.5 invariant ("atomic, idempotent reducer"),
but the three outputs (report, triage, receipt) are three separate atomic writes. A reducer that read the blocks earlier can publish
last: the run-report then misses one lane's block, or report and triage come from two different reductions, until the next reduce. The
S6 close reduces again (driver_stage_s6.py:717, :966), so the closed state is right, and the error direction on a lane's handoff check
is a refusal, not a pass. Fix: write this as the named C.5 residual in the TR3-9 batch file (spec C.5 asked for "the report names each
writer with its lock or this reason"; no such report is in the given set).

**Q1 (queue):** `run_manual_lane` is 167 lines (driver_stage_s6.py:1661-1827). Its nested `record_then_role` reaches 5 levels (most of
that from TR3-10d). Split the prompt-line build out. Node: TR3-10 follow-up.
**Q2 (queue):** duplication. `_lane_beside_running` (controller.py:6312-6351) repeats `_window_beside_running` (:6271-6306) line for
line, apart from the kind predicate and the actor check. `config_contract.walkers` (:576-590) repeats `parallel_windows` (:555-570).
Each can be one body with a kind or key argument. `_config_cap` already shows the way (:6255-6265).
**Q3 (queue):** in `run_complete` (driver_stage_s6.py:1749-1750) the term `not self.walk_pending(block) if walking else True` is
subsumed by `not self.walk_pending(view cases)`. Dead logic, harmless.

## Answers

**Q1.** Lanes run on the generic scheduler: `run_s6_lanes` calls `run_chains(..., self.chain_launchable, self.run_manual_lane, ...,
kind=self.s6_chain_kind(), seam=self.s6_seam)` (driver_stage_s6.py:1658-1659). One `def run_chains`, in driver_chains.py:353. Two
`threading.Thread(` sites in the driver set (driver_chains.py:394, driver_runner.py:707). The default of 3 comes from
`config_contract.walkers` (:573-590), the template `manual.walkers: 3` (templates/config.json:61-62) and the keys row
(config-keys.json:271-274). `walkers: 1`: `run_manual_block` takes `run_manual_lane(None, lanes[0])` (driver_stage_s6.py:1512, :1526),
with no flag and no thread. Structure holds, byte parity is unproven (B1). Same account: holds are one `account:<part>` per key part
(:1613; assigned handles :1608), the start gate `chain_launchable` covers live chains (driver_chains.py:282-291), and the controller
requires distinct whole `walk_actor` (controller.py:6346-6348). Same case: lanes partition the plan (`walk_lanes`, :1246), and the
controller refuses scope overlap with running and returned siblings (:6339-6345). A returned lane counts as open: `s6_open_lanes`
counts every plan case not in `manual_done_cases` (:1620-1632), and a blocked lane stays open (key `close_waits_for_a_blocked_lane`).

**Q2.** Driver state: every chain step holds `_book` (`_chain_thread`, driver_chains.py:445). It is released only around `communicate`
(driver_runner.py:711) and the backoff sleep (:938), and neither writes state. The watcher thread only tells (:704-708). `walk_after`
runs in `run_role`'s `finally` after `run_claude` re-took `_book` (driver_dispatch.py:710-714), and in the lane's `except`
(driver_stage_s6.py:1824-1826), which is also booked. Its files are per walk id. `walk_before` (finalize when absent, app_card build,
`walk_old_road`) is booked (C.9, :1690-1693, :1742). `created-accounts.json` has its own OS lock (manual_capture.py:733-734, changelog
t-1957-n1c). Dispatch id plus registration happen in one booked step (:1694-1725). The one writer outside a lock is the role-invoked
`finalize_task`: an atomic reducer as the spec allows, with the residual in F5. Outside the driver, the controller's
`_holder_would_refuse` writes a repair beside an admitted lane (F1).

**Q3.** A dying walker: `walk_after` closes the walk and the exception drains (driver_chains.py:452-454). The seam re-raises one
failure and the dispatch stays running for re-entry (key `lane_crash_others_finish_one_seam`). A person's question in one lane: the
drain lets the running ones finish, Person ranks last, and the others are named "also ended with Person" (driver_chains.py:469-472;
key `lane_question_queued_next`). A refused stand: `walk_session open` fails, so `walking` is False and the lane goes to the recorder
road (driver_dispatch.py:1128-1136, FR-57). `execution.parallel.mode: serial` makes it serial with a reason (driver_stage_s6.py:1546-1547).
The lease supports `walk` in all cases (stand_lease.py:193-225), so the spec's "stand not shareable" row folds into that one, a safe
choice. One case means one lane: `run_s6_lanes` takes the old body (:1654-1655). More walkers than cases: cap `min(walkers, lanes)`
(:1525, :1658). Guest limit of §3: TR3-10d superseded it by the owner's word of 10.11 (spec :436), but the changelog was not updated (F3).
Every refusal keeps the controller's old text byte for byte (admission key "a lane sharing a case is refused with the old text, byte for byte").

**Q4.** The expectations come from the spec, not from code output: distinct ids, closing exactly once whatever the finish order, open
on unknown, no thread at 1. FR-58 holds. The admission file goes red on a shared case or account through the real controller
(`shared_case_refused`, `same_account_refused`, `guest_beside_guest_refused`; my re-run: 94/94). On the driver side the killing key is
`same_account_second_lane_never_registers`. The keys named "in turn" are weak (F4). Layers: `test_s6_lane_admission.py` is kept as
`detector` (test-layers.json:4773-4777), `test_walk_lanes.py` is kept as `gate_named` by import only (:6344-6348),
`test_walk_lanes_parallel.py` is kept as `gate_named` (:6349-6353), and `test_story_run_s6_w1_frozen.py` is QUARANTINED (B1). A canon
flake is on record: `ci-out/canon-130772252066.log:773-774`, where `crashed_lane_closes_its_walk` failed once on lane order. The check
was later relaxed to be order-free (test :631-634), and the relaxed form still proves the close.

**Q5.** TR4-10 (1), the claim release at close: S6 claims no files (twin table §4 row `s5_release*`), n/a. TR4-10 (2), returned counts
as open: holds by construction in `s6_open_lanes`. TR4-10 (3), no start after the drain in `session_gate`: generic, in
driver_chains.py:299-335, inherited, and S6 never waits there because the start gate is over live lanes. TR4-10 (4), the file
ownership line: n/a. TR4-10 (5), stage `pending` beside a stopped window: `stage_entry_beside_running` covers S6 (controller.py:998-1010;
admission key "a stop beside a running lane keeps S6 running"). TR4-13, the accepted author round: S6 has no author/critic rounds, n/a.
**Missing:** TR4-7's admitted-sibling exemption in `_holder_would_refuse` (F1), and the map rows that would have pointed at it (F2).

## Standing questions

- Fit to the spec: A, B, D, C1 and C2 have landed. `_s6_runner_half` goes through `dispatch_identity.own` (validate_artifacts.py:2069-2072),
  and the state-exits row is present (state-exits.md:54). C0 landed but is red and quarantined (B1). The spec's C1 report with the
  twin table and the C.5 writer list was not in the given set.
- DUPLICATION AND CONSISTENCY: Q2 and F1. The grep was `_window_beside_running\(` over controller.py, which found 4 call sites, 2 of
  them without the lane clause. I read the clone ratchet's verdict from the green canon and did not re-derive it.
- CODE QUALITY: Q1 (167-line function, 5 nesting levels), Q3 (subsumed term), F4 (a dead `enter` in a test).
- Ratchets: the census row `driver_stage_s6.py::s6_open_lanes` is `xref/data` (judgment-census.json:820), as the spec names it. Nothing
  else was checked beyond the green `forge-check`.
- ARCHITECTURE: AR-15 holds (one scheduler). AR-13 holds (one walkers reader: grep `walkers(` callers are controller `_config_cap` and
  `s6_walkers_cap`). AR-17 holds (one seam per run). AR-19 is broken at one site (F1, F2). AR-28 holds (unknown counts as open or
  serial: `s6_open_lanes` raises and `run_complete` catches it as False, :1748-1752; `s6_serial_reason` returns rows for anything it
  cannot read). AR-22 holds: `walk_lane`/`walk_actor` are produced at :1716-1724 and read at controller.py:6326-6331.
- JUDGMENT: no check judges a role's content. Every new unit is shape or xref over data.
- ONE ROAD: none found. Guests, named accounts and unreadable keys all take the same scheduler, and only their holds differ (data). The
  unreadable key runs alone first, which is the safe default, not a second road. I grepped `host|language|python|pytest` in the S6 lane
  block (driver_stage_s6.py:1490-1660). The only hit is `host_window_reason`, the shared host reader, which is also S5's.

## Trail

Read: the spec t-2147 (all 511 lines); critic-diff-brief.md; driver_chains.py (all); driver_stage_s6.py:1210-1830;
driver_dispatch.py:594-800, :1020-1420; driver_runner.py:660-740, :915-945; controller.py:970-1016, :4959-5047, :6255-6373, plus the
grep of the clause call sites; config_contract.py:550-600; config-keys.json:262-282; templates/config.json (grep); finalize_task.py
(grep for writers); stand_lease.py (grep); manual_capture.py (grep for the lock); validate_artifacts.py:2056-2078;
test_walk_lanes_parallel.py:40-720; test_story_run_s6_w1_frozen.py (all); test-layers.json (rows named above); SIBLING_MAP.md axes 5,
33, 34; batch-3 and batch-4 rows TR3-9, TR4-7, TR4-10, TR4-13; reviews t-2227 and t-2263 (greps); the changelog fragments;
ci-out/canon-130772252066.log:771-776.
Negative searches and their controls: SIBLING_MAP twin rows (control `s5_precheck.running_dispatch` hit :575); ci-out for the frozen
file (control `test_walk_lanes_parallel` hit in 8 files); `git log --all -S` for both controller functions (both resolve only to the
merge 5498318, so the order of TR4-7 and TR3-9d cannot be told).
Re-runs: see the JSON block.
Needed beyond the manifest: driver_dispatch.py, driver_runner.py, finalize_task.py, stand_lease.py, manual_capture.py,
validate_artifacts.py, test_story_run_s6_w1_frozen.py, ci-out logs, the batch-4 file.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "B1: the walkers-1 parity proof test_story_run_s6_w1_frozen.py is quarantined and red at entry (test-layers.json:9928-9936); C.1 and the F3 ruling name it as THE proof; cause not on record; the old road differs at driver_stage_s6.py:1667 (boundary) and :1703 (walk_next_id)"
  ],
  "fixes": [
    "F1: controller.py:4989 and :4995 _holder_would_refuse lacks `or self._lane_beside_running(...)`; an admitted S6 lane runs close_settled over its running siblings, against the B1 invariant at :5016-5017; add the clause and one admission key",
    "F2: SIBLING_MAP axis 5 has no S5 windows <-> S6 lanes row and axis 33 lacks the S6 twin (_s6_runner_half) promised in its own symmetry line; Lead writes both",
    "F3: changelog.d/tr3-9c-walker-lanes.md says all-guest stories run one walker at a time; TR3-10c/d run guest#<lane> side by side; amend before release",
    "F4: test_walk_lanes_parallel.py:280-311 same_account_lanes_in_turn and overlapping_part_sets_in_turn use sessions that hold nothing (cannot go red), the guest half asserts no order, and :308 is a dead enter; hold lane 1 on an event and assert the order",
    "F5: role-invoked finalize_task (driver_stage_s6.py:1768, :1807) runs unbooked beside booked reductions; atomic reducer per C.5, but a stale publish and a report/triage mix are possible until the next reduce; write the named C.5 residual in the batch file",
    "Queue Q1: run_manual_lane is 167 lines (driver_stage_s6.py:1661-1827), 5 nesting levels",
    "Queue Q2: _lane_beside_running duplicates _window_beside_running (controller.py:6271-6351); config_contract.walkers duplicates parallel_windows (:555-590)",
    "Queue Q3: subsumed walk_pending term in run_complete (driver_stage_s6.py:1749-1750)"
  ],
  "class_completeness": "Axis 5 (S5 windows <-> S6 lanes): TR4-10 items 1-5 and TR4-13 are covered or n/a for S6; the TR4-7 admitted-sibling exemption in controller._holder_would_refuse was not carried to S6 (F1). The map rows that would have pointed at it are missing on axis 5 and axis 33 (F2). Inside the controller the clause has 4 call sites: validate and _resume_problems carry the S6 clause, _holder_would_refuse (two sites) does not.",
  "trail": {
    "read": [
      "docs/tasks/specs/t-2147-tr3-9-walker-lanes.md",
      "docs/tasks/critic-diff-brief.md",
      "ai-packages/qa-factory/scripts/driver_chains.py",
      "ai-packages/qa-factory/scripts/driver_stage_s6.py:1210-1830",
      "ai-packages/qa-factory/scripts/driver_dispatch.py:594-800,1020-1420",
      "ai-packages/qa-factory/scripts/driver_runner.py:660-740,915-945",
      "ai-packages/qa-factory/scripts/controller.py:970-1016,4959-5047,6255-6373",
      "ai-packages/qa-factory/scripts/config_contract.py:550-600",
      "ai-packages/qa-factory/references/config-keys.json:262-282",
      "ai-packages/qa-factory/scripts/validate_artifacts.py:2056-2078",
      "ai-packages/qa-factory/scripts/tests/test_walk_lanes_parallel.py:40-720",
      "ai-packages/qa-factory/scripts/tests/test_story_run_s6_w1_frozen.py",
      "ai-packages/qa-factory/scripts/tests/test-layers.json (rows 4773, 6344, 6349, 9928)",
      "docs/SIBLING_MAP.md axes 5, 33, 34",
      "plans/piles/thinking-roles/batch-3-parallelnost.md, batch-4-ostatki.md (rows)",
      "ai-packages/qa-factory/changelog.d/tr3-9c-walker-lanes.md, tr3-9d, tr3-10c",
      "ci-out/canon-130772252066.log:771-776"
    ],
    "reruns": [
      {"command": "python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_s6_lane_admission.py", "result": "=== test_s6_lane_admission: 94/94 ok === exit 0"},
      {"command": "python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_walk_lanes.py", "result": "13 passed in 0.43s, exit 0"}
    ]
  }
}
```
