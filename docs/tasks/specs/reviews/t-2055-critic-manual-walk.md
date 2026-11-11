# t-2055 critic: manual walk (TR1-1, TR1-2, TR1-4, TR1-9), critic-entry on t-2038, t-2048, t-2039, t-2049

Chains against 77b448a3e: `tr/tr1-2` at 35311bfa2 (`D:/ws1/wt-tr1-2`), `tr/tr1-9` at 5f573e4ae (`D:/ws1/wt-tr1-9`). Line numbers are of those two heads.

## Verdict: NEEDS WORK. 5 findings block the merge, 5 fix in the same round, 4 go to the queue. Acceptance is the Lead's.

Answers to the DoD's three questions:

1. **False pass for cards 3 and 23: still possible.** The exact two calls are closed, across separate `step` calls too (the attempt and `type_chain` live for the whole item). But a `read` or `wait` between the two `type` calls puts the focus back and gives '12', all ok (B1).
2. **A closing stage swallowing unaccepted work silently: yes, by two roads.** A row still `running` is named only in a stage `reason` that no report reads. A row that `close_settled` already moved to `returned_unaccepted` gets no name at all (B4).
3. **Merge conflict: none.** `git merge-tree --write-tree 35311bfa2 5f573e4ae` exits 0 (tree 0673725ca). The two chains' changed-file lists have an empty intersection: `story_run.py` is only in tr1-9, `manual_capture.py` only in tr1-2, and the tests are disjoint. The merged tree was not run (batch canon).

## Blocking findings

**B1. TR1-1: a passive step between two `type` calls restores the false pass.** `manual_capture.py:4163` shifts the chain on EVERY step. Probe with the test's own `_TypePage(drops=True)` and `_TypeBrowser`:

    ['type #qty 1','type #qty 2']              -> ('1',  ['ok','failed'], 1 focus)
    ['type #qty 1','read #qty','type #qty 2']  -> ('12', ['ok','ok','ok'], 2 focus)
    ['type #qty 1','wait 100','type #qty 2']   -> ('12', ['ok','ok','ok'], 2 focus)

A person who reads the screen has not clicked. `stop_on_default` has no `field`, so the walk runs on, and the test row "a `read` between counts as a step between" pins the hole. The spec's words "без шага между ними" carry it, so this is a spec defect too; editing the finding's text is the Lead's.
Fix:
- Add `keeps_run: ["read","look","wait","watch","capture","fail_request","restore_request"]` to the `type` row of `manual-capture-steps.json` (data, FR-13).
- In `_run_step`, shift only when the word is not in `keeps_run`; read it through `spec()`, because the tests pass `spec_data={}`.
- Change the `does` text of `type` to "no action between".
- Invert the TR1-1 `read` row and the TR1-2 row "a `read` between the `type` and the `press`".
- Add rows: drop page with `read`, and with `wait` -> value '1', second `type` not ok, one focus; holding page with `read` -> '12', ok, one focus. `click` still resets.

**B2. TR1-9: the run's own state still lands on the defect road.** Probe on the real `tr-walk` `controller.json`:

    with verdicts: conflicts ['required prior logical stage incomplete'], running [], behind ('S6','pending')
    driver's reading (no verdicts): running ['S7-qa-failure-analyst-6'], B-20 branch condition: False

`Driver.code_close` (`story_run.py:16734-16736`) calls `code_close_facts(ctl, stage)` with no verdicts, so `not facts["running"]` is False and it falls to `file_defect` plus the question "no word of yours passes". That is the refusal this node set out to end. The TR1-9 tests seed S6 completed, so they never meet it.
Fix: replace `not facts["running"]` with `"checkpoint active work" not in refusal.text`. The refusal carries that sentence exactly when a holder remains; the branch already reads the other fixed sentence this way, and the case with both sentences keeps today's road.
Test in `test_code_close_behind.py`: S6 pending, S7 row running, refusal text with the `behind` sentence only -> key `code_close.behind`, no `file_defect`. I did not trace that question's answer road on the copy; the fixer's test must reach the offer.

**B3. TR1-9: a passed-over row stays `running`, so the story does not move on.** Probe of `_next_action_for_state` on that state with S6 and S7 completed:

    row left running:          wait_existing_job S7-qa-failure-analyst-6, cancel_allowed False
    row returned_unaccepted:   resolve_return    S7-qa-failure-analyst-6

`where` is read-only (`story_step._next(read_only=True)`), so `close_settled` does not run. `_act_wait_existing_job` then re-finishes the saved result of the closed stage's dispatch, and that road ends in the form refusal of `conductor.jsonl:55`. `dispatch` also refuses while the row is `running` (`controller.py:5054`). The close succeeds and the next stage stays held.
**Fork for the Lead**, what a passed-over row becomes. Recommended: the `code_only` event carries a typed `passed_over: [{id, label}]` (set in `apply`, the request's own copy; add it to any field allowlist), and the projection (`controller.py:1692`) sets each row to `superseded` (already in `DISCOUNTED`) with `passed_over_by: <receipt>`. The alternative leaves `resolve_return` demanding acceptance over a closed stage.
Test: after a close over a returned row, `next` does not name it and the S8 dispatch is not refused; a replay of the journal gives the same state.

**B4. TR1-9: "returned, never accepted" does not reach the report, and no finding is filed (AR-27). The named edge, and wider than it.**
- Case-insensitive grep of `report_facts.py`, `report_adapt.py`, `reporters.py` for `returned_unaccepted|never accepted|stages.*reason|code_only`: no hit; the same file's `left_gap_line` is found by the same tool. The note's only reader is `story_progress._code_only`, a progress line. The comment at `controller.py:4677` ("so the report reads it") is untrue.
- Second road, probe: row status `returned_unaccepted`, S6 completed -> `conflicts []`, `passed_over []`, note `''`. The name depends on whether `close_settled` ran first. `status_of` only looks at `running`.
- The note is computed in `apply` and the decision again in `validate`: a verdict that flips between them closes with no name.

Fix (the builder's question 1 is answered here: the hook is `close_by_code`, in the driver):
- `code_close_facts` lists in `passed_over` every row of the closing and earlier stages whose status is in `OPEN_AFTER_CLOSURE` minus `running`, plus running rows released by a verdict; labels `returned, never accepted`, `abandoned`, `stopped, never accepted`. Skip a row an accepted later dispatch of the same stage and role replaced.
- `validate` refuses (`StateConflict`, "the state moved, send again") when its own `passed_over` is not the payload's.
- `Driver.close_by_code`, right after `close_receipt`, reads `stages[stage].passed_over` and calls `owe_row(... "add-finding", "--scope", "local-calibration", "--idempotency-key", f"close-passed-over:{task}:{stage}:{id}")` per row. `stage_done`'s rewrite must keep the field: add `passed_over` to `STAGE_RUN_MARKS` (`controller.py:944`).
- `report_facts.py`: `_passed_over_gap(art)` on the `_owed_rework_gap` pattern, one `left_gap_line(<id>, "<role>'s work of <stage> returned and was never accepted", "<what was closed over it>")` per row; unreadable state -> one line saying so (AR-28).

Tests: both roads named in the gap; findings idempotent; no row -> no line.

**B5. TR1-4: the old road survives for every account except a one-part `env`. Named edge, wider than multi-part.** Spec item (3) keeps the old road ONLY for a session that did not open for an environment reason. Today `walk_account_gap` returns "" unless the key is one `env:` part, so these all reach `walk_before`, print "walked on the recorder" and stop the run the way lane 13 did: `env:X+stand_account:y`; a `stand_account` with no two-key note; a role the stand does not list; `none`; more accounts than `max_actors`; `key is None`. `auto_actor`'s `ValueError` for the single-part ones goes to `walk_before`'s `except`, also the old road. With the owner's word (no exceptions for cases) the fit is one road:
- `walk_account_gap(lane)`: `key is None` -> "the accounts of <case> could not be read from its request"; `key == ""` -> ""; otherwise call `walk_actors(lane[0], key)` and return its `why`. On `ValueError`, return `the account of <case> (<key>) is not one a machine can sign in as`; the door text with `--as` stays out of the person's report (P9). This removes the second parse of the key.
- `walk_actors`: move the `load_config` `ValueError` to `cfg = {}` there. In the multi-part loop add `kind == "env"` -> `walk_env_pair(stand, value)` (no role -> its `why`). Drop a duplicate handle when two parts resolve to one role.
- `walk_before`'s old road then holds only a failed `walk_session.py open`.

Tests: one row per shape above -> not walked, reason named, no `walk_old_road`, next lane opens; `env:USER_EMAIL+stand_account:admin` with a pair -> `--actor`, `--actor2`; `open` exit 1 -> old road and the mark.

## Fix in the same round

**F6. TR1-2: the hint and the `surprise:` line never reach the walker on the road they were written for.** `walk_session.op_step` (about line 1064) sends each step as `{k, step, outcome, surprise}`, no `detail`. Probe through the `Rig` of `test_walk_session.py`:

    fail_request */api/cart 500 -> HINT in answer: False; in steps.jsonl: True
    restore_request + read      -> 'surprise: fail_request' in answer: False; steps.jsonl: both rows

Only `op_look`/`final` show `detail`. The existing `failure_idle` limitation does reach the answer, but the hint for cards 5 and 6 does not. The report's "AR-18, one `surprise:` line in a step answer" holds only at `_run_steps`, where the tests read it.
Fix: `Attempt.step` and the ok return of `_run_step` store the lines as a typed `told: [...]` (kept in `detail` too); `op_step` copies `told` into the step row; `_fit` must not cut it. Tests through `Rig.step`: hint present in the answer, absent for `**/api/cart`; line on `restore_request` and the first `read`, not the second.

**F7. TR1-4: `walk_timing` does not name the old road on real data.** A lane on the old road never opened a session, so it has no item row. Probe, mark on TC-18 and TC-19, a walked lane beside it: `old_road: []`, `names TC-18: False`; no walks at all: `no walk timed`, no `old_road`. The test seeds a timing row the old road cannot write.
Fix: `report()` takes `sorted(old_road_items(task_root))`, on the no-walk return too, and `render` prints it there. Keep the row filter. Test: mark with no row -> named in both shapes.

**F8. TR1-9: dead branch.** `dispatch_liveness.state` adds `process: gone` only when the verdict is NOT `alive`, so `alive` with `gone` cannot be produced. Deviation 2 of the report is moot. `controller.py` `code_close_passed_label` (the `alive` and `gone` branch), test row "process: gone does not hold it either" and the changelog's "or with its process gone" describe a state that does not exist. `unknown` with `gone` holds, as the reader's docstring wants. Delete all three.

**F9. TR1-1: the stop has no door in the answer.** The walker IS told: exit 1, `stopped_at` with the fact, `not_run`, a page snapshot, the session stays ready, and the next `step` call continues the same attempt. The charter's "one corrected call, a second stop is a result" applies, so it can go on. But `type_chain` is still set after the failed step, so a resend fails again, and the `click` door lives only in the hint. Fix: append "; a `click` on the field is a person's new click" to the `StepFailed` text only, at one local variable (the f-string is copied three times in `_run_input`, 3906, 3909, 3921).

**F10. TR1-1: the chain is by selector string and shared between actors.** `type #qty 1`, `type input#qty 2` -> ('12', ok, ok): another false-pass road, spelling only. Two actors share `rec["attempt"]`, so B's first `type` on a selector A just used is "continued" on B's page: a false failure. Fix: in `op_step`, reset `attempt.type_chain` when the actor differs from the last call's. For spelling, when `type_prior` is set and differs, ask a backend `same_field(a, b)` (a doubt is False, today's road). If the fixer's round runs out, this half goes to the queue line below.

## Judged edges

- **`fill` after `type` as a new focus: the coordinator's reading is right**, by reading `_run_fill`: `clear_field` then `type_chars` with one focus and rows per character, so a page that drops the focus is still seen. It replaces the text rather than continuing it, and `_field_fact` compares by equality. My probe's fake does not reach that road, so it is not cited.
- **TR1-1's stop of the batch: right.** The keys went elsewhere, so the plan is void; F9 is the only gap.
- **`invalidate` (`controller.py:5564`) and `s6_close_dispatch`: the safe direction, not blocking.** The class is wider than the report says: also `revise_plan` 4961, `semantic_reopen` 5004, `dispatch` 5054, resume 5843. Queue line below.

## Standing questions

- Fit to spec: not yet (B1-B5, F6, F7). Builder's decisions: finding scope `local-calibration` is acceptable; the reason reaches the report through `request.json` and `report_facts._refusal` (read). The `--as` reach requirement is the safe direction.
- Seams: additive. `scaffold.py` outside `owns` is needed and declared. `test_code_close_behind.py` has a stray `tests =[`: restore it.
- **DUPLICATION AND CONSISTENCY**: (a) `_close_verdicts` repeats the loop of `liveness_fixes` (`controller.py:7219-7240`) without `_denied`: extract one `_running_verdict`, fix now; (b) `walk_account_gap` re-resolves `walk_actors`: B5; (c) the `{"refused": {...}}` write is now in three places (`manual_close`, `stand_login_gate`, `walk_refuse_gaps`): extract `refuse_case(plan, case, reason, door, by)`, fix now; (d) three `str(row.get("id") or key)` readings in TR1-9, one helper. Clone ratchet: branches not pushed, no `forge-check` to read; owed at the batch canon.
- **CODE QUALITY**: no new function over 60 lines (`walk_refuse_gaps` about 25, `walk_env_pair` about 20). Lying comment `controller.py:4677` (B4), dead branch (F8). `test_the_gap_check_stands_before_the_dispatch_is_registered` is a source pin: queue a real entry test. Two `_close_verdicts` calls per close scan the transcripts twice: goes with B4.
- Ratchets (question 9): the census, `role-load.json`, `dup-baseline` and A27 are not in the diff stat: none raised. Hygiene: FR-30 by the reports' `--lang`, not re-run.
- ARCHITECTURE: AR-13 "kept" is doubtful for TR1-9: the default reading and the verdict reading now disagree inside one seam (B2). AR-27 is claimed and not met (B4). AR-18 is claimed and not met on the walker road (F6). AR-22: the note has no report reader (B4).
- JUDGMENT: none found. The label carries the reader's verdict, the pair lookup is data, no census row or craft marker moved. Grepped: diff stat for census files; `judgment:` lines read on 66b05e29f and 5f573e4ae.

## Queue lines (Lead writes them into «Остатки»)

- `the S7 analyst's finish refused on inputs_read row path (conductor.jsonl:55): the cause no node owns | узел: <Lead opens>`
- `running rows read with no liveness: revise_plan, semantic_reopen, dispatch, invalidate, resume, s6_close_dispatch: one helper, a door in each text | узел: <Lead opens>`
- `test_walk_charter.py has no main: run as a script it proves nothing | узел: <Lead opens>`
- `same_field for selector spelling, if not done in F10 | узел: <Lead opens>`

## Spot-checks

- t-2036's inference "this dispatch reads `returned`": MEASURED on the copy with `dispatch_liveness.state`, `now` = 07:28:19, +5, +11, +30 min: all `returned`, evidence the driver's end row (exit 0). The inference holds.
- t-2049 "story_run.py is unchanged": `git show --stat 5f573e4ae` lists controller, test, changelog, report: holds.
- t-2048 "only the scaffold fake touched": grep of `def type_chars|press_key|paste_text` across tests: `test_manual_fill_human.py:43` keeps the old signature; it passed 79/79 after TR1-1 but was NOT re-run after TR1-2, nor was `test_manual_surprise.py`. Left to the canon, named here.
- t-2049 witness: re-run below, equal.

## Trail

Read: the given files; `manual_capture.py` (`_keyboard_step`, `_run_input`, `_run_step`, `_run_steps`, `_store_failure`, `auto_actor`); `walk_session.py` (`stop_at`, `op_step`, `op_verdict`, `_lift_failures`, `_run_words`); `controller.py` (751-860, 2288-2310, 4674-4680, 5531-5575, 7205-7282, 7705-7760, 8115-8165); `story_run.py` (`walk_before`, `walk_actors`, `walk_env_pair`, `walk_account_gap`, `walk_refuse_gaps`, `run_manual_block`, `manual_close`, `code_only`, `close_by_code`, `code_close`, `_act_wait_existing_job`); `dispatch_liveness.py` 919-1040; `walk_timing.py`; `story_step.py` (`_next`, `where`); `report_facts.py` (`_refusal`, `left_gap_line`, `_owed_rework_gap`); `walk-charter.md`; `manual-capture-steps.json`; both test diffs.

Not traced: the `code_close.behind` answer road; a boundary log written after an item's verdict (`_lift_failures` after `write_verdict`).

Runs (verbatim tails; the probes are read-only scratchpad scripts, no worktree or copy written):

    python -B D:/ws1/wt-tr1-9\ai-packages\qa-factory\scripts\tests\test_code_close_behind.py
    === test_code_close_behind: 68/68 ok ===
    git merge-tree --write-tree --name-only 35311bfa2 5f573e4ae
    0673725cae3509b416ccedcd0af25a5226746e89 (exit 0)

Probe outputs are quoted in B1, B2, B3, B4, F6, F7, F10 and the spot-checks. Not run, per the brief: `test_manual_capture.py`, `test_walk_session.py` as a whole, `test_walk_road.py`, slow files, ratchets, mutations.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "B1 TR1-1: a read or wait between two type calls refocuses, value 12, all ok: the false pass of cards 3 and 23 remains",
    "B2 TR1-9: Driver.code_close reads facts with no verdicts, so the B-20 branch is not taken on the tr-walk state: file_defect and the no-word question again",
    "B3 TR1-9: a passed-over row stays running: next answers wait_existing_job on the closed stage's dispatch and dispatch refuses; fork for the Lead: the row's status",
    "B4 TR1-9: returned, never accepted reaches no report, no finding is filed, and a row already returned_unaccepted is closed over with no name",
    "B5 TR1-4: every account shape except a one-part env still takes the old road (multi-part env, unlisted role, no two-key note, none, over max_actors, unreadable request)"
  ],
  "fixes": [
    "B1: keeps_run data list on the type row; _run_step shifts the chain only for other words; invert the two read rows; add read and wait rows",
    "B2: story_run.py code_close: replace not facts[running] with the checkpoint sentence absent from refusal.text; test S6 pending with S7 row running",
    "B3: on the Lead's fork: typed passed_over in the code_only event, projection sets superseded with passed_over_by; test next and S8 dispatch, journal replay",
    "B4: passed_over covers OPEN_AFTER_CLOSURE rows; validate refuses a mismatch; close_by_code files one finding per row; STAGE_RUN_MARKS keeps the field; report_facts._passed_over_gap",
    "B5: walk_account_gap calls walk_actors for every non-empty key; env branch in the multi-part loop; old road only for a failed open; one test per shape",
    "F6: typed told on the step row, copied by op_step into the answer, tested through Rig.step",
    "F7: walk_timing report and render name old_road_items whole, the no-walk return too",
    "F8: delete the alive plus gone branch, its test row and its changelog words",
    "F9: door in the StepFailed text, one local variable for the fact",
    "F10: reset type_chain on an actor change; same_field for selector spelling or its queue line",
    "Duplication: one _running_verdict with liveness_fixes; refuse_case for the three refused writes; one row id helper; restore the stray tests =[ edit"
  ],
  "class_completeness": "Not complete. TR1-1: passive steps, selector spelling and actors are uncovered. TR1-4: all non-env account shapes are uncovered. TR1-9: the status road and the default-facts reader in code_close are uncovered; running-row readers with no liveness (revise_plan, semantic_reopen, dispatch, invalidate, resume, s6_close_dispatch) are fail-closed and go to one queue line. The press and paste sibling of TR1-1 is covered by TR1-2. SIBLING_MAP was only grepped (focus, typed, walk_session, code_close, liveness, case-insensitive): the first six hits are rows 136, 140, 214, 258, 274, 277, none read as an axis of these fixes except possibly row 136 (where the story is, in_flight); it was not walked axis by axis, a scout can be asked.",
  "trail": {
    "read": [
      "docs/tasks/critic-diff-brief.md",
      "plans/piles/thinking-roles/findings/20261106-hodok-lozhnyj-pass-i-pravila-sboya.md",
      "plans/piles/thinking-roles/findings/20261106-hodok-uchyotki-i-vhod.md",
      "plans/piles/thinking-roles/findings/20261106-analitik-prohodit-mesta-ostatki.md",
      "docs/tasks/specs/reports/t-2036-tr1-9-triage.md",
      "docs/tasks/specs/reports/t-2038-tr1-1-report.md",
      "docs/tasks/specs/reports/t-2048-tr1-2-report.md",
      "docs/tasks/specs/reports/t-2039-tr1-4-report.md",
      "docs/tasks/specs/reports/t-2049-tr1-9-report.md",
      "ai-packages/qa-factory/scripts/manual_capture.py",
      "ai-packages/qa-factory/scripts/walk_session.py",
      "ai-packages/qa-factory/scripts/controller.py",
      "ai-packages/qa-factory/scripts/story_run.py",
      "ai-packages/qa-factory/scripts/dispatch_liveness.py",
      "ai-packages/qa-factory/scripts/walk_timing.py",
      "ai-packages/qa-factory/scripts/story_step.py",
      "ai-packages/qa-factory/scripts/report_facts.py",
      "ai-packages/qa-factory/references/walk-charter.md",
      "ai-packages/qa-factory/references/manual-capture-steps.json",
      "ai-packages/qa-factory/scripts/tests/test_code_close_behind.py",
      "ai-packages/qa-factory/scripts/tests/test_walk_road.py",
      "ai-packages/qa-factory/scripts/tests/test_manual_capture.py",
      "ai-packages/qa-factory/scripts/tests/test_walk_session.py"
    ],
    "reruns": [
      {"command": "python -B D:/ws/wt-tr1-9\\ai-packages\\qa-factory\\scripts\\tests\\test_code_close_behind.py", "result": "=== test_code_close_behind: 68/68 ok ==="},
      {"command": "git merge-tree --write-tree --name-only 35311bfa2 5f573e4ae", "result": "exit 0, tree 0673725cae3509b416ccedcd0af25a5226746e89, no conflicted file"},
      {"command": "scratchpad probe: dispatch_liveness.state on the tr-walk copy at the refusal time and later", "result": "returned at 07:28:19, +5, +11, +30 min"},
      {"command": "scratchpad probe: code_close_facts and conflicts on the tr-walk controller.json", "result": "with verdicts behind only; default running holds the row; B-20 condition False; a returned_unaccepted row: no conflict, no name"},
      {"command": "scratchpad probe: _next_action_for_state after the close", "result": "row running: wait_existing_job; row returned_unaccepted: resolve_return"},
      {"command": "scratchpad probe: test_manual_capture stubs, steps between two type calls", "result": "read: 12 all ok; wait: 12 all ok; another selector spelling: 12 all ok; no step: 1, second failed"},
      {"command": "scratchpad probe: test_walk_session Rig, fail_request and restore_request answers", "result": "hint and surprise line absent from the answer, present in steps.jsonl"},
      {"command": "scratchpad probe: walk_timing with a mark and no item row", "result": "old_road empty, TC-18 not named"}
    ]
  }
}
```
