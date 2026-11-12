# t-102 report - TR3-9 fix round (F1, F3, F4, B1 diagnosis)

Worktree: C:\QAFactory\forge-repo\.claude\worktrees\agent-aa37c93d9788f33c1 (nothing committed).

## Items
1. F1 DONE. `controller.py` `_holder_would_refuse`: both sites (dispatch, resume) now ask `_window_beside_running(...) or _lane_beside_running(...)`
   with the same argument shape as their S5 neighbour (dispatch: `request, current, running`; resume: `target, current, beside, flagged=False`);
   docstring updated. `validate` (:5449) and `_resume_problems` (:6369) already asked both, so the three now ask the same question.
   Invariant kept: the clause only widens "admitted beside a sibling"; a request no clause admits is still settled as before (control inside the new key:
   a lane sharing a case is not admitted, liveness IS asked, L1 closes). First lane / nothing running: covered by existing early return `if not running`
   (existing keys `two_lanes_disjoint_distinct_accounts_admitted`, `with_one` first dispatch). Stage neither S5 nor S6: both clauses false, unchanged.
   New key `admitted_lane_never_runs_close_settled` (liveness reader stubbed to "session over"; asserts L1 row byte-equal, both running, liveness never asked).
   No existing key turned red.
2. F4 DONE. `test_walk_lanes_parallel.py`: new helper `hold_first_lane` (first lane to enter holds on a `threading.Event`; a watcher thread gives the
   other lane `GRACE` = 0.5 s to wrongly enter, then releases in `finally`; join timeout `WAIT` = 10 s with a named check "the holding watcher finished (no hang)").
   `same_account_lanes_in_turn` and `overlapping_part_sets_in_turn` now assert "second does not enter while the first holds" and that both ran. No pin on which
   lane is first. Note: GRACE is a bounded wait for an event that must NOT come; a broken gate goes green only if the second lane is slower than 0.5 s to
   start, and a correct gate can never go red. Guest half: requirement now = guest lanes run side by side when data is disjoint (TR3-10; key
   `guest_lanes_side_by_side_when_data_disjoint` already asserts it); the old half asserted only `done_cases`, so it is deleted with a comment. Dead `enter` call removed.
3. F3 DONE. `changelog.d/tr3-9c-walker-lanes.md`: the all-guest sentence replaced by "Guest cases do not wait for each other: each guest lane gets its own guest
   handle (`guest#<lane>`), so guest lanes run side by side whenever the records they use do not overlap." (wording from `s6_lane_holds` + tr3-10c fragment). English only.
4. B1 DIAGNOSIS DONE (nothing edited). See below.

## Witness
### test_s6_lane_admission (with fix)
`python -B <wt>\...\tests\test_s6_lane_admission.py`  ->  `=== test_s6_lane_admission: 98/98 ok ===` (94 before + 4 new checks)
### red probe F1 (byte copy, clause removed at the dispatch site, restored)
orig hash   99ABA1048C5276AD34C1280B86F2E74F623B9FC46D5179430CE7AE3E373F2CC9
probe run:
```
FAIL an admitted second lane: the first lane's row is untouched - ... 'status': 'returned_unaccepted' ... 'repaired_by_recover': True, 'reason': 'dispatch: L1 was recorded as running but its role stopped without acceptance - probe: the session is over'
FAIL both lanes run - expected ['L1', 'L2'], got ['L2']
FAIL liveness was never asked about a sibling of an admitted lane - expected [], got ['L1']
=== test_s6_lane_admission: 95/98 ok ===
```
restored hash 99ABA1048C5276AD34C1280B86F2E74F623B9FC46D5179430CE7AE3E373F2CC9 (identical).
### test_walk_lanes_parallel (with fix)
`python -B <wt>\...\tests\test_walk_lanes_parallel.py`  ->  `=== test_walk_lanes_parallel: 196/196 ok ===`
### red probe F4 (byte copy of driver_stage_s6.py; `s6_lane_holds` returned only the `case:` holds; restored)
orig hash   4BF7EFE18287EED52AA0DBE6C5629B70AA02D37873E024992D3FEEE918B1F841
```
FAIL two lanes on one account: the second does not enter while the first holds - ['TC-1', 'TC-2']
FAIL lanes whose part sets meet: the second does not enter while the first holds - ['TC-1', 'TC-2']
=== test_walk_lanes_parallel: 184/196 ok ===
```
restored hash 4BF7EFE18287EED52AA0DBE6C5629B70AA02D37873E024992D3FEEE918B1F841 (identical).
### others
`python -m pytest <wt>\...\tests\test_walk_lanes.py -q` -> `13 passed in 1.86s`
`python -B <wt>\...\selftest.py --limits --lang` -> `PASS limits: ... PASS limits: every mandatory role rule ... === qa-factory selftest: 4/4 ok ===`

## FR pass (touched sections)
A (refusals) - no refusal text changed; the clause only widens admission, the old texts stay byte for byte (existing keys green).
B - text to a person not changed. C - no contract field added; FR-14 output shape unchanged. D - n/a. E - n/a (changelog fragment corrected, FR-10: the two
unreleased fragments no longer contradict). F - n/a. G - FR-31: new waits are event-based with one bounded negative grace; FR-30: English only, no Cyrillic added.
AR-19 (stage twins change together): kept for the controller admission (three callers now ask both clauses). AR-25/AR-28: the repair still fires only when a
row would REFUSE; error direction unchanged (doubt = True).

## Siblings: axis "S5 windows <-> S6 lanes"
| caller | asks | verdict |
|---|---|---|
| controller.py `validate` ~:5449 | `_window_beside_running` or `_lane_beside_running` | asks both |
| controller.py `_resume_problems` ~:6369 | both | asks both |
| controller.py `_holder_would_refuse` dispatch site ~:4989 | was S5 only | fixed, asks both |
| controller.py `_holder_would_refuse` resume site ~:4995 | was S5 only | fixed, asks both |
| controller.py `stage_entry_beside_running` (:991, :998-1010) | not these two functions; uses the S6 manual-runner predicate (:974) beside the S5 window rule per its docstring | covers S6 (key "a stop beside a running lane keeps S6 running"); not re-derived line by line |
| story_step.py:945 `request["parallel_window"]` and driver_stage_s6.py:1717 `walk_lane`/`walk_actor` | producers of the two flags | each stage sets its own flag; matched readers are the two clauses |
| tests (test_s5_parallel_admission, test_s6_lane_admission, test_controller_state:1868-1872) | S5 / S6 / S5 | `test_controller_state` `_holder_would_refuse` keys exercise only the S5 window (CI file, not run here; unaffected, both clauses false for S5 requests beside S5 windows or the S5 clause already true) |
Findings not fixed (Lead's): SIBLING_MAP rows (F2), Q2 duplication of the two functions, F5.

## B1 diagnosis (no edits)
Command: `python -B <wt>\ai-packages\qa-factory\scripts\tests\test_story_run_s6_w1_frozen.py` (background, finished well inside 8 min, exit 1):
```
FAIL (the whole list of this file): w1_frozen_calls ... | w1_frozen_console ...
FAIL w1_frozen_calls: every call of the story ... — first difference at #0: live {... "Inputs:\n  qa-factory/artifacts/QA-9/work/automation-manifest.json\n  qa-factory/artifacts/QA-9/state/story-case-links.json\n  qa-factory/artifacts/QA-9/work/first-look.yaml\n  Rework reason: manual block ...  | frozen {... Inputs:\n ...story-case-links.json\n  Rework reason: manual block ...
PASS w1_frozen_events
PASS w1_frozen_state_keys
FAIL w1_frozen_console ... first difference at #0: live "...note: brief: qa-factory/artifacts/QA-9/work/briefs/S6-qa-runner-1.md (5,752 B, 4,344 budget B against the ceiling)..." | frozen "...note: brief: ... (<bytes> B, <bytes> B against the ceiling)..."
PASS w1_frozen_brief_bytes_mask (x2)
=== test_story_run_s6_w1_frozen: 4/6 ok ===
```
Causes (2 red keys, 2 causes; the full log is in the scratchpad `b1.log`):
- CALLS: the live prompt has one more input line, `work/first-look.yaml`. Source: `brief_pack.py:3771` `FIRST_LOOK_FILE` ("the record `first_look.py put` writes; its name is
  spelled by stages.json too (the inputs of S3-S7)"), added by the first-look work (t-2277 FL-2) after the capture. It is the stage input list, shared by every road;
  not lane code. By the SPEC (C.1, `walkers: 1` = the road before lanes) the code is right: the input list is not the lane road. The capture is stale. NOT the
  `boundary = "S6"` assignment, not `walk_next_id`. (Grep-level attribution: I found the producer, I did not bisect the commit.)
- CONSOLE: the brief note now prints `4,344 budget B against the ceiling` (label from commit 2b1b36c, brief_pack.py:4532), while the mask `BRIEF_BYTES`
  (test :158) only matches `(N B, N B against the ceiling)`. The mask pattern is stale; code is right (PC2-3 relabel, independent of walkers). The frozen text is
  not the oracle here.
- NOT proven: `boundary = "S6"` (:1667) and `walk_next_id` (:1703) show no red line: `w1_frozen_events` (registrations, ids, closes) and `w1_frozen_state_keys` PASS.
  Caveat: the calls and console comparisons report only the FIRST difference, so any later difference in those two keys is hidden until the two causes above are
  fixed. A recapture/mask fix (Lead's, quarantined file not edited by me) and one re-run would say whether anything else is behind them.

## Needed beyond the manifest
brief_pack.py (grep), test_story_run_s6_w1_frozen.py (run, read lines 150-170), dispatch_liveness constants (via controller), driver_stage_s6.py `s6_lane_holds` (for the F4 probe),
controller.py `close_settled`/`liveness_fixes` (to build the F1 stub).
