# t-683 — topic code review FV1-22 re-cut: N1 + N2 + N3 (critic, 14.11.2026)

Spec/DoD: `docs/tasks/specs/20261114-fv1-22-recut-spec.md` §3.1-3.3, §4-6 (F-A..F-D = (a)). Diffs: N1 `f40f24b` (wt `fv1-22r-n1`), N2 `40d7d0a` + N3 `a56ae5c` (wt `fv1-22r-n3`), merge base `50d9012`. The verdict is an input to acceptance. Accepting is the Lead's decision.

## Verdict

| unit | verdict |
|---|---|
| N1 (consumer acceptance form, one reader of where the word is) | **fit_with_fixes** (F1) |
| N2 (conductor-round stop on every stage) | **fit_with_fixes** (F4, F5; proposed node P1) |
| N3 (repeat recorded) | **fit_with_fixes**: B1 blocks the merge; F2, F3, F6, F7 |
| Topic | **fit_with_fixes**: 1 finding blocks the merge (B1); 7 fixes for one round; 1 proposed node |

## Blocking (before merge)

**B1 (N3) `Driver.record_repeat` has no row in `scripts/tests/fixtures/driver-layers.json`.** `test_driver_layers.py:710-716` (L1 census) refuses any `def` with no row: "`driver_runner.py:<n>` defines `Driver.record_repeat`; driver-layers.json has no row for it". The test is slow and judged by CI, so this is a known red at the merge. Minimal fix: add the row the builder proposed, next to `Driver.journal_run` (`:116`), in the `note` form its neighbour `Driver.person_stop_record` (`:821`) uses. It is a one-line fix with no new edge. `driver_core` already sits below `driver_runner`, which already imports from it.

## Fixes (one fix round; none blocks on its own)

- **F1 (N1) Refusal text names the wrong place.** In `acceptance.py` `stage_acceptance_from_form` (~`:1590`) the text still reads "the form must end its header with one of them". For S7/S8 the word now sits at `stage_acceptance.verdict` (FR-1, FR-37). The builder's own negative control prints exactly this text for an S7 form. Fix (in owns: the function's problem line): name `handoff.acceptance_verdict_path(form.get("contract"))`, e.g. "write one of them at `<path>` of the form".
- **F2 (N3; the spec premise is wrong) Rows on S-b..S-d are not once-only.** Spec §3.3 item 1 states the invariant "once per (road, key, finding_key(lines), outcome) … across relaunches" and says the callers already guard it. That holds for S-a (`if not any(...)`, `driver_machine.py:368`) and S-e (a stopped series returns early, `driver_gates.py:906`). It does not hold for S-b, S-c or S-d: `record_repeat` runs before `exit_limit` on every arrival. Scenario: the person answers `round`. On the next arrival `exit_limit` sees `granted > spent` and runs `exit_round`, a paid round with no stop (`driver_dispatch.py:3741-3743`). A `repeat_stop` row has already been written, so one stop is counted twice and a non-stop is recorded as a stop. Rows of one kind then mean different things per road, and per-road counts for the cause analysis are skewed. L8 `looped` is a boolean and stays unaffected. Minimal fix: a persisted mark in `driver-state` (`repeat_recorded`), keyed by the spec's own tuple and checked in `record_repeat`. This needs a Lead decision, because the spec's "the helper adds none of its own" was written on the false premise. Add N3-b's twin row: the second arrival writes nothing.
- **F3 (N3) S-c records a non-repeat.** `handle_refusal` `resume_structured` (`driver_machine.py:~545-553`) records inside `if dispatch:`, and the branch also fires on `not sid and not done.get(dispatch)`: the first refusal, with no session, where nothing was resumed. By the spec's own reasoning for S-d ("the no-session branch is not a repeat") and by FR-41, this is no repeat. Fix: record only when `done.get(dispatch)`. Answers question 5: the asymmetry is a defect, and it comes from the spec text the builder followed.
- **F4 (N2/N3 tests) The keep row no longer fits the file.** `test_probe_gap_door.py` keep row `test-layers.json:3816` says "held by import … leaves the canon when the import is cut (TD-15.8)" and covers only `tests/harness.py` and `tests/story_run_common.py`. The file now carries 14 new rows that judge `window_round_gate`, `stage_acceptance_write`, `record_repeat`, `gate_stop` and `resume_on_refusal`. As things stand, `--witness-for` those modules will not print it, and TD-15.8 would drop it (brief item 5: "a keep row whose layer/why does not hold"). Fix: rewrite `why` (FV1-22 N2/N3 rows) and add `driver_machine.py`, `driver_gates.py`, `driver_runner.py`, `driver_stage_plan.py` to `covers`. The file is outside the nodes' owns, so the Lead names the owner.
- **F5 (N2 test) One line asserts nothing.** The last line of `test_fv122_stage_outside_the_table_is_gated` calls `window_round_gate(fv122_gate_stub(), gap, "S8")` with no assertion. With an empty series it returns whether or not the early return works, so it cannot fail. Add `assert fv122_rounds(stub) == [] and stub.journal_rows == []` on a named stub.
- **F6 (axis 37 text, the Lead's commit) The detector claim is false.** The axis says "the grep `exit_limit(` / `finding_key(` / `same_set` over `scripts/driver_*.py` finds only sites named in this axis". My grep (case-insensitive) also finds:
  - the no-session `exit_limit` branch of `resume_on_refusal` (`driver_machine.py:~270`);
  - `session_gone` (`driver_dispatch.py:~2218`);
  - `close_by_doors` same-key retry (`driver_machine.py:218,230`);
  - the `code_close` defect dedupe (`driver_machine.py:2134`).

  Positive control: the same grep finds S-a `:366`, S-d `driver_dispatch.py:542` and S-e `driver_gates.py:923`. Add these to "Not members", each with its verdict. Also give an explicit member / not-member verdict for `code_close`'s behind-idle stop (`CODE_CLOSE_IDLE_CAP = 2`, `driver_core.py:409`; `driver_machine.py:~2120-2130`): the second identical refusal at the SAME revision goes to the person. That is a repeat by identity (behind, revision), not by a finding set. The spec's map walk did not name it. Also state the once-ness rule decided under F2.
- **F7 (N3 code quality) Two consecutive identical guards.** `driver_dispatch.py:541-544` has two `if result["session_id"]:` blocks in a row (print, then record). Merge them into one block.

Remarks (no fix needed now, each small):
- (a) The N2 commit's `architecture:` line omits AR-28. The DoD and the report name it, and the code keeps it (N2-c).
- (b) The console prints in `window_round_gate` still say "window" / "the window's tests" for every stage (`driver_machine.py:~375`, `~387`, `~425-430`). Only the person's leads were neutralised. Queue as one text line.
- (c) Stale text:
  - `vocabulary.yaml:121-123` still says "stage critic (S2-S4)";
  - `stage_done.py:961` docstring says "built from the form's header verdict word" (outside owns);
  - in the dropped S7 skeleton the "Reviewed dispatch" comment above `inputs_read:` stays when its row is removed.
- (d) A form that deletes the `stage_acceptance.verdict` line still passes finish, because `handoff_check.check` walks `doc.nodes`. It then lands on the unreadable seam, which is the safe direction. This class already existed for `header.verdict`.
- (e) `window_round_gate` grows to about 115 lines, with 4 nesting levels in the lead branches. Queue the extraction of a `window_round_lead(...)` helper.

## Proposed node (the Lead opens it; it is not a line to pass on)

**P1: N2's net works per dispatch at stages whose dispatches carry no scope.** `window_key` falls back to `<stage>|<dispatch id>` when the dispatch record has no scope (`driver_machine.py:306-318`). Measured on the arm's `state/controller.json`: every S1, S2 and S3 dispatch has `scope: []`. S4-S7 carry scopes, so K1 (`S7-qa-failure-analyst-2..4`, scope `TC-005`) does share a key. S8/S9 are not measured (the arm has no such dispatch). A conductor `rework` makes a new dispatch and so starts a new series. A K2-like loop across rework dispatches at S1/S3 (and probably S8/S9) is therefore never `same_set`, which is the F-cmp2-28c loop the gate exists for. The changelog and `driver.md` say "every stage". The builders built the spec as written: the spec gap is the dispatcher's. Proposal: an identity for scope-less dispatches (`<stage>|<role>`, closed by the accepted completion N2 item 3 already wires), with an F-C(b)-style cost note. Node owner: Lead of `live-run-fvf`. It touches the owner's "stop on any stage", so the decision is the Lead's, possibly the owner's.

## Answers to the six builder questions

1. **(N1) Is "one reader of the word" true?** Yes, for the consumer acceptance word. The three sites read the review verdict of a digest:
   - `driver_stage_s7.py:925`: the repair-round critic;
   - `driver_stage_plan.py:778`: the S4 case critic's rework decision `case_verdict`;
   - `driver_dispatch.py:3034`: `route_of`, the code critic's route.

   None of them reads a contract that has `acceptance_verdict_at`. Latent note: the S4 field is read by two roads (`case_verdict` and `acceptance_word`). They agree while S4 has no `acceptance_verdict_at`. The stale problem text is F1.
2. **(N1) Quarantined pin.** Expected red in `quarantine-watch`. `test_stage_acceptance_consumer.py:343` pins `required_when:\n  concerns: [stage_acceptance]`, which is exactly the meaning the Lead decided to change (OLD F2 = a). It is not a sign the change is wrong. Not edited; the Lead tells the owner (td-15 rule).
3. **(N3) `driver-layers.json` row.** Yes, add it as proposed. Without it CI is red (B1).
4. **(N3) N3-d in `test_probe_gap_door.py`.** Acceptable as the home: it is the only non-slow keep file that drives the real `gate_stop`. Its keep row must be updated (F4).
5. **(N3) Keys.** Using the dispatch as the key for S-b..S-d is right (the resume record is per dispatch). For S-e, the gate name is the series id: the series lives at `state["gate_repair"][gate]` (`driver_gates.py:386-389`) and has no other id. The S-c / S-d asymmetry is a defect (F3).
6. **(N3) No dedup on S-b..S-d.** Not right: the rows break the spec's stated once-ness invariant, disagree with S-a and S-e, and record the paid-round arrival as a stop (F2).

## The owner's word of 13.11 («найти причину и там тоже чинить»)

The topic fixes one cause and records the rest.
- **K1 is fixed at its cause in N1.** The analyst's form now holds the acceptance word, class, quote and reviewed-dispatch row (FR-11). The two FV1-22 `known_red` rows are deleted, and the ratchet refuses a stale green row. My control re-run: `test_field_producers` 920/920.
- **K2-K7:** spec §4 sends each to its owning node (A1a/b, FV1-1/2, FV1-19, FV1-20) or marks it "not established — needs". That is the Lead-accepted routing.
- **What N3 adds:** it records the next repeats with stage and set.
- **Still open:** F-F (K5's loop length) is the owner question, not built, as dispatched.

## Seams and merge (N1 ∥ N2+N3)

`git merge-tree --write-tree 1deef49 a56ae5c` exits 0 with no conflicts (tree `2e8c615`).
- `driver_stage_plan.py`: N2 touches `stage_acceptance_write`, N1 touches `stage_verdict_known`; the hunks are 25 lines apart and both appear intact in the merged tree.
- `driver_dispatch.py`, `driver_machine.py`, `driver_gates.py`, `driver_runner.py`, `test_probe_gap_door.py`: N2/N3 only.
- `acceptance.py`: N1 only.
- `judgment-census.json`: neither branch touches it. The new names (`acceptance_word`, `acceptance_verdict_path`, `drop_unowed_acceptance`, `record_repeat`) do not match `UNIT_NAME_RE` (`test_judgment_census.py:77`).
- Semantics: before stage-critics B2, a refused S6 acceptance write at S7 now carries the analyst dispatch (N2 item 2) and meets the gate. N1 removes that refusal's cause. Neither side silently overrides the other.

## Standing questions (brief items)

- **Fit (1):** N1 items 1-14 and N2 items 1-4 as written. N3 items 1-5 as written, except the once-ness invariant (F2) and S-c (F3).
- **Builder's own decisions (2):** S-e key = gate is fine; the S-c guard is F3; N3-d's home is F4.
- **Tests (5):** they reach the real raise (`gate_refusal` → `stage_acceptance_write`), the real `window_round_gate`, `gate_stop` and `resume_on_refusal`, and the AT/BEYOND cap rows. Weak spots: F5, and a missing N3-b twin for the second arrival (F2).
- **DUPLICATION AND CONSISTENCY (6):** nothing new beyond what the spec queued. S-a writes both `window_round` (L2) and `repeat_stop` (L8) for one stop; spec §3.3 keeps L2 on purpose. `acceptance_word`'s dict walker is prescribed by spec item 5. Grep `def (dig|get_path|path_get|_dig|dotted|value_at|get_dotted|lookup)` over `scripts/` found no shared plain-dict dotted reader (control: the same grep found `diff_scope._dotted`, which is not one). Within the diff: F7, and S8's same 3-line comment written twice (as spec item 9 prescribes).
- **CODE QUALITY (7):** new functions are under 60 lines with at most 3 nesting levels: `drop_unowed_acceptance` ~30 lines, `record_repeat` 15, `acceptance_word` 15. Findings: F7, remark (e). No dead branches, apart from the test line in F5.
- **Hygiene (8):** `selftest --limits --lang` green in all three reports.
- **Ratchets (9):** `known_red` shrinks by 2 rows (FV1-22, named). No raises.
- **ARCHITECTURE (10):**
  - N1: AR-10, 11, 13, 19, 20, 22, 23 and 28 are named and kept. The path reader has the 6 callers per the DoD grep; the producer (template + prefill) and the reader change in one commit.
  - N2: AR-15, 17, 19 and 25 are named and kept. The S5 strings stay byte-equal in their `else` branches. AR-28 is kept but not named (a).
  - N3: AR-15 is kept for the five sites (F6 asks for a verdict on `code_close`). AR-22 is kept for L8 and kinds, but the def map row is missing (B1). AR-29 is kept: the row judges nothing.
- **JUDGMENT (11):** none moved into code. The gate compares set identity, and accept/return stays the role's word. No census row, `blocks_override` or craft marker was added.
- **ONE ROAD (12):** N2 removes an S5-only exception, and the remaining `window` cause is the data table `WINDOW_ROUND_STAGES`. The residual is P1 (per-dispatch identity at scope-less stages), proposed as a node above. Grepped `WINDOW_ROUND_STAGES` and `stage == "S5"` in `window_round_gate`: the S5 probe-gap branch is an ordinary S5 condition.

## Class-wide completeness

Map walk on axis 5 and the new axis 37. Grep `same_set|finding_key\(|already resumed|same findings|same set|same reasons` (case-insensitive) over `scripts/*.py`. Positive control: the same grep finds the members S-a, S-d and S-e. Repeat stops beyond S-a..S-e: `code_close` behind-idle (an identity stop with no set; verdict owed, F6). The rest are single-shot or code retries (F6 list). Budgets (controller caps, `repair_limit*`) stay queued as the spec decided.

## Trail

Read:
- the spec (whole) and `critic-diff-brief.md`;
- the N1 diff (all package files) and the N2/N3 diff (all package files);
- the three builder reports;
- `handoff.py:553-605`, `handoff_check.py:1405-1440,1540-1640`, `driver_stage_s6.py:340-412`, `driver_stage_plan.py:640-737,765-790`, `driver_stage_s7.py:910-940`, `driver_dispatch.py:432-452,515-550,946-954,3020-3036,3722-3770`, `driver_machine.py:161-176,228-305,306-440,515-600,2112-2160`, `driver_gates.py:365-389,817-826,905-1000`;
- `story_step._author_argv` (`:319-336`), `brief_pack.reviewed_dispatch` (`:3666-3706`), `acceptance.py:1415-1481,1585-1600`, `stage_done.py:950-1000`;
- `test_driver_layers.py:700-730`, `driver-layers.json` grep, `test-layers.json:3816-3822`, `test_stage_acceptance_consumer.py` grep, `test_judgment_census.py` grep, `slow_tests.json` grep, `critic_verdict.schema.json`;
- the uncommitted `docs/SIBLING_MAP.md` diff in `fv1-22r-n3`; `origin/main` has no axis 37;
- the arm's `state/controller.json` (dispatch scopes).

Re-runs:
- `python -B test_field_producers.py` (wt n1) → `=== test_field_producers: 920/920 ok ===`
- `python -B test_probe_gap_door.py` (wt n3) → `48 passed in 5.94s`
- a pure probe of `drop_unowed_acceptance` on the s7/s8/s4 templates (wt n1): s7 and s8 lose the section and the token row and still parse; s4 is unchanged (diff 0); `contract_of` resolves S7/S8 to the forms with `stage_acceptance.verdict`
- `git merge-tree --write-tree 1deef49 a56ae5c` → exit 0, tree `2e8c615`

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "B1 (N3): scripts/tests/fixtures/driver-layers.json has no row for Driver.record_repeat; test_driver_layers.py L1 census (:710-716) goes red in CI. Fix: add the builder's proposed row beside Driver.journal_run (:116), note form as Driver.person_stop_record (:821)."
  ],
  "fixes": [
    "F1 (N1): acceptance.py stage_acceptance_from_form problem text '~:1590' says 'end its header with one of them'; name handoff.acceptance_verdict_path(form contract) instead (FR-1, FR-37).",
    "F2 (N3, spec premise wrong, Lead decision): S-b..S-d write repeat_stop on every arrival, including the paid-round arrival (driver_dispatch.py:3741-3743, exit_round, no stop); dedupe in record_repeat by a persisted mark keyed (road, key, finding_key(lines), outcome) per the spec's own invariant; add the N3-b second-arrival row.",
    "F3 (N3): handle_refusal resume_structured records with no session and no spent resume (not a repeat); record only when done.get(dispatch).",
    "F4 (tests, Lead names the owner): test-layers.json:3816 keep row of test_probe_gap_door.py says 'held by import ... leaves the canon'; rewrite why and add driver_machine.py, driver_gates.py, driver_runner.py, driver_stage_plan.py to covers so --witness-for prints it.",
    "F5 (N2 test): last line of test_fv122_stage_outside_the_table_is_gated asserts nothing; assert the stub recorded no round.",
    "F6 (axis 37 text, Lead commit): the detector sentence is false; list the no-session exit_limit branches (driver_machine.py ~270, driver_dispatch.py ~2218), close_by_doors (driver_machine.py 218/230), code_close defect dedupe (2134) as not-members, and give a member/not-member verdict for code_close's behind-idle stop (CODE_CLOSE_IDLE_CAP, driver_core.py:409); state the once-ness rule decided in F2.",
    "F7 (N3 quality): merge the two consecutive 'if result[session_id]' blocks at driver_dispatch.py:541-544."
  ],
  "class_completeness": "Axis 5 and new axis 37 walked; case-insensitive grep same_set|finding_key(|already resumed|same findings|same set|same reasons over scripts/*.py, positive control finds S-a/S-d/S-e. Unlisted: code_close behind-idle identity stop (verdict owed, F6); other hits are single-shot stops or code retries. Budgets stay queued per spec. Residual one-road gap: per-dispatch identity at scope-less stages (S1-S3 measured on the arm) - proposed node P1, Lead owner.",
  "trail": {
    "read": [
      "docs/tasks/specs/20261114-fv1-22-recut-spec.md",
      "docs/tasks/critic-diff-brief.md",
      "N1 diff origin/main...f40f24b (all package files)",
      "N2+N3 diff origin/main...a56ae5c (all package files)",
      "three builder reports (n1, n2, n3)",
      "handoff.py 553-605; handoff_check.py 1405-1440, 1540-1640; handoff_init.py drop_unowed_acceptance",
      "driver_stage_s6.py 340-412; driver_stage_plan.py 640-790; driver_stage_s7.py 910-940",
      "driver_dispatch.py 432-452, 515-550, 946-954, 3020-3036, 3722-3770",
      "driver_machine.py 161-176, 228-440, 515-600, 2112-2160; driver_gates.py 365-389, 817-826, 905-1000",
      "story_step.py 319-336; brief_pack.py 3666-3706; acceptance.py 1415-1481, 1585-1600; stage_done.py 950-1000",
      "tests/test_driver_layers.py 700-730; fixtures/driver-layers.json grep; test-layers.json 3816-3822; test_stage_acceptance_consumer.py grep; test_judgment_census.py grep; slow_tests.json grep",
      "fv1-22r-n3 uncommitted docs/SIBLING_MAP.md diff; origin/main SIBLING_MAP axis headings",
      "arm state/controller.json dispatch scopes"
    ],
    "reruns": [
      {"command": "python -B test_field_producers.py (worktree fv1-22r-n1, scripts/tests)", "result": "=== test_field_producers: 920/920 ok ==="},
      {"command": "python -B test_probe_gap_door.py (worktree fv1-22r-n3, scripts/tests)", "result": "48 passed in 5.94s"},
      {"command": "pure probe drop_unowed_acceptance on s7/s8/s4 templates (worktree n1)", "result": "s7 and s8: no stage_acceptance, no token row, parse ok; s4 unchanged (diff 0)"},
      {"command": "git merge-tree --write-tree 1deef49 a56ae5c", "result": "exit 0, tree 2e8c6156, no conflicts"}
    ]
  }
}
```
