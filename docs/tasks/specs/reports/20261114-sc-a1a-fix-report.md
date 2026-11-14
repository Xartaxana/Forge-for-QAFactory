# Fix report: node A1a (task t-654, attempt 2)

## What was done
1. T1-b fixed in `Controller.stage_repairs` (controller.py): the closing repair now also requires `s3_window_of(last) != "labelling"`.
   `s3_window_of` is the existing one reader of S3's windows (`request_binding.purpose == S3_LABELLING`, any other stage answers "exit");
   no literal list of purposes added (AR-13, AR-1). Window 1 is the only window the code names; the "last window" is any strategist
   record that is not window 1 (the exit window carries no purpose: `driver_stage_plan.py:128` registers it with no `purpose`).
2. Ratchet `qa-case-critic` 6130 -> 6580 in `test_brief_pack.py`, with a named RAISE comment line above `ROLE_BRIEF_BYTES_MAX` (AR-20).
3. `test_no_move_seam_c26_g27_f2.py` C26 F-7: the S2 author strings are `qa-requirements-tester` (ids and role, lines 262-263).

## Row table (test_stage_closure.py, `author_last_closes_by_repair`)
| id | record | stage_repairs returns | why |
|---|---|---|---|
| s3-between-windows-not-closed | S3 strategist, accepted, binding purpose s3_labelling | none | window 1 is between the windows |
| s3-after-last-window-closed | S3 strategist, binding purpose "exit" | closes | not window 1 |
| s3-purpose-absent | S3 strategist, binding without purpose | closes | see QUESTION |
| s2-unchanged | S2 tester with the labelling word in its binding | closes | `s3_window_of` answers "exit" for any non-S3 stage: identical to before |
| (existing) S3 exit window, no binding at all | | closes | same |

## QUESTION for the Lead (edge conflict; I did not decide it)
The edge says "purpose absent -> NOT closing (FR-59)". That contradicts the data and T1's own S3 row: the REAL exit window is registered
with NO purpose (`driver_stage_plan.py:124-129`, `request_binding()` keeps only keys present), and the existing T1 S3 row has no
`request_binding` and expects a close. `s3_window_of` (documented: error direction toward `exit`) treats absent purpose as the exit window.
Not closing on absent purpose would make `stage_repairs` NEVER close S3 in any real state (the invariant in T1). I kept `s3_window_of` and the
rows `s3-purpose-absent` (closes) accordingly. If the Lead wants "unknown" for a non-mapping `request_binding` only, that is a one-line change.
"Unreadable windows source": there is none to read (`s3_window_of` is pure, in the same module, never raises), so no red was added.

## Siblings (stage_closes_with alone; NOT edited)
- controller.py:4075-4080 `_is_review_of`: not applicable - judges a review of reworked work, not closure.
- controller.py:7581 `_closes_stage`: has the same hole for S3 labelling? It returns True for an accepted window-1 strategist (no window test; S3 is not in DERIVED_SCOPE_STAGES) - but `apply` refuses window 1 with stage_complete (controller.py:7528) so closure is not set; the refusal-of-false rule may still treat window 1 as "closing role". Same class, worth a look by the Lead.
- story_step.py:1904, 2494, 2812, 2943 (`finish --not-complete` halt doors / `decide --close`): same shape (role-only test) for window 1 of S3; not verified whether a window-1 halt wrongly offers `--close`. Queued as a question, not edited.
- contract.py:5903: the definition.

## Verification (witness)
From the worktree root (subshell):
```
python -B ai-packages/qa-factory/scripts/tests/test_stage_closure.py  -> === stage closure: 27/27 ok ===  (23 before: +4 rows)
python -B ai-packages/qa-factory/scripts/selftest.py --limits --lang  -> PASS limits ... === qa-factory selftest: 4/4 ok ===
```
`test_brief_pack.py` (34.6 s) and `test_no_move_seam_c26_g27_f2.py` (28.3 s) are in `slow_tests.json`: NOT run locally, named for CI (the 6580 number and the two role strings are the previous run's CI-measured values).
Control of the fix: before my edit the T1-b row returned `[("stage_completed","S3")]` (previous report); the row now expects none and passes.

## FR pass
A: no refusal text changed. B: no text to a person. C: FR-13 window word read through the one reader; FR-42 no state added. D: n/a. E: n/a. F: n/a. G: FR-30 English, `--lang` green; FR-54 siblings above.
axes: 25 (stage_repairs and `_closes_stage` twins named), 20 (ratchet raise named), 13 (one reader) covered; others n/a.
