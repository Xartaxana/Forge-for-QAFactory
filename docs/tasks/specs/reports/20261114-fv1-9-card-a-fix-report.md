# t-741 attempt 2 - card A fix round (F1 + Q2)

## Done
- Helper `Driver.tell_rollcall(self, out, code=0)` in `driver_dispatch.py`, next to `tell_next_session`. Designer `question_notes` first (S4 key, S4 tail unchanged), then planner `plan_notes` (S3 key) with the new true tail: "code could not write this onto your plan row and will not try again; add it to the row yourself if it still holds".
- Parameter `code` covers the only difference between the sites: `driver_gates.raise_move` reads `out` only on exit 0/1 (any other exit: designer hears the ONE unknown line, planner nothing, then RepairFailed); `driver_stage_plan.s4_after_critic` ignored the exit and always parsed (default `code=0` is the same). So both sites merge; receivers, keys and order unchanged; only the `plan_notes` tail bytes changed.
- Before/after: both 4-line blocks (2 calls each) became `self.tell_rollcall(out)` (stage_plan) and `self.tell_rollcall(out, code)` (gates; the `said` variable and the `if code in (0, 1)` block are gone).
- `s3_project` tail (`driver_dispatch.py` ~2834) untouched; `question_notes` tail byte-identical.
- Tests (`test_gate_question_form.py`): new constant `FV19_PLAN_TAIL`; row `s4_after_critic: plan_notes (item 13)` expects it; ONE new row `raise_move: plan_notes (exit 0)` proves the `driver_gates` site prints the same tail. Empty input: existing rows (empty question_notes, no plan_notes) unchanged and green.

## Witness (verbatim, each file alone, exit 0)
```
gate question form: 591/591 ok (was 587; +4 checks of the new row)
codex_tool_guidance 217/217 | dispatch_identity 114/114 | driver_stop_record 255/255 | exploratory_answers 107/107
first_look_code_look 127/127 | first_look_step 101/101 | human_questions 291/291 | login_need 33 passed
null_outcomes 327/327 | person_owned 82/82 | probe_gap_door 54 passed | probe_marker_judgment 46 passed
probe_not_proved 47 passed | reference_window 85/85 | s5_window_leftovers 148/148 | walk_account 190/190
walk_lanes_parallel 196/196 | walk_supply 261/261 | whole_list_sites 292/292
selftest --limits --lang: === qa-factory selftest: 4/4 ok ===
```
(The 20 files are the same set card A's report ran; scenario_walk printed 76 files, the rest are slow/story_run, judged by canon.)

Grep, case-insensitive, `tried again when S3 closes` over ai-packages/qa-factory:
- before (positive control): 4 hits - driver_stage_plan.py:677, driver_gates.py:603, driver_dispatch.py:2822 (s3_project), test_gate_question_form.py:1481 (FV19_S3_TAIL, s3_project rows).
- after: 2 hits - driver_dispatch.py:2834 (s3_project) and test_gate_question_form.py:1481 (FV19_S3_TAIL, used only by the s3_project rows).

test_judgment_census.py: `=== judgment_census: 25/25 ok ===` (exit 0).

## FR walk
A: FR-1/FR-2 - the tail now says what code will not do and names the door (the planner edits the row). B: FR-6 - plain English line for a role. C: FR-49/AR-24 - the told line is true, same carrier. D-G not touched except G: FR-29/FR-30 ASCII English (selftest --lang green), FR-54 siblings below.

## Siblings
`s3_project` tail (not touched, true); `question_notes` tail (moved unchanged).

## Questions
none.
