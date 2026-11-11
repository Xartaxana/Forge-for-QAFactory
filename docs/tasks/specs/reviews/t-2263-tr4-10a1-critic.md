# t-2263 — critic diff gate: TR4-10 part A1 (S5 window leftovers, driver side), commits 4f96c0eae + f32f87c0f

Reviewed: `git -C D:/ws1/wt-tr4-10a1 diff 4f96c0eae~1 f32f87c0f` (10 files). Line numbers are the tree at f32f87c0f
(`story_run.py`, `window_files.py` and the test file are byte-identical at branch HEAD b956e4c47: `git diff --stat f32f87c0f HEAD` on them is empty).
Against: spec t-2222 §2 items 10.1, 10.2, 10.4 and §9 D1-D7 (with "D3 AMENDED" and "D1 widened"), plan critic t-2227 B-1/B-2/§5/§7,
`docs/tasks/critic-diff-brief.md`, builder report t-2251.

**Verdict: fit_with_fixes (NEEDS WORK) — 1 blocking finding (B1), 5 non-blocking fixes.** Everything else checked holds: 10.1/D4/D5, 10.2, D1
(both branches), D6, the N == 1 road. The decision to accept the diff belongs to the Lead.
(Superseded by the later re-review sections at the end of this file; the LAST JSON block is the current verdict.)

## Blocking finding

### B1 — D3 as landed: the person's words are never consumed in the only state the new branch serves; the stated road out does not exist (AR-24/FR-8, AR-25)

Surface: the way out of "a window held open by a returned last round" (the `stage_S5` branch, `story_run.py:11858-11883`, and the `state-exits.md` row).

The report's deviation, the code comment at :11861-11862, the test comment and the new state-exits row all say: after the packet goes to the
person, "the person's words then take `_act_resolve_return` -> `resume_role` as today". That road starts only when the controller's `next`
returns the action `resolve_return` (`dispatch_action`, :16776-16777). It cannot return it in this state:

1. `stage_S5` reaches the new branch only when `next` answered `prepare_stage` for S5. In `controller._next_action_for_state` the returned scan
   (`controller.py:8555-8569`) comes BEFORE `prepare_stage` (:8651). So a returned dispatch R that `next` can see is offered as `resolve_return`
   first, and `stage_S5` is never entered. The branch is reachable only when R is in `superseded_by_later_work` (:8544-8550: any later
   dispatch of the same STAGE that holds a move, e.g. W2's accepted critic, hides it). The builder's own state-exits row says the same thing in
   its "entered" column: "a later dispatch of the stage hides the return from `next`".
2. The packet is a Refusal with `dispatch=R` (`resolve_return_refusal`, :17201-17204). The person answers in free words, and `_file_words`
   files them as `pending_words[R]` (:19851-19856, kind `refusal`, dispatch field set).
3. Next entry: R is still hidden, because the later W2 critic is still `accepted`. `next` again answers `prepare_stage` S5, and
   `_act_resolve_return` is never called. `stage_S5` hits :11858 again: `todo == []`, R is still the last round, and the SAME packet is raised.
   Nothing reads `pending_words[R]`. The test pins this outright (`returned_last_round_raises_resolve_return_naming_the_dispatch`, "words filed"
   part: `pending_words = {"m1": "go on"}` and the packet is raised again, `resume_role` is never called).
4. Result: the person's words go nowhere. `ask()` re-asks with "You have answered this exact question before" (:4447-4457) until the stuck
   seam at `STUCK_REPEATS` (:660, :17553). This is exactly the run-5 class (one `resolve_return` packet three times, :671, :4446). The only
   exit left is a conductor who happens to run a controller command on R, and that is not the road the row or the report names.

Concrete failing scenario (N = 3, the t-2227 B-1 counter-scenario carried on):
- W1's critic is accepted with route mechanical, and W1's mechanical round R comes back `returned_unaccepted`. W2's chain then has its critic
  accepted `--not-complete`, because the returned clause now holds W1 open (correct).
- Re-entry: `next` hides R behind W2's accepted critic and answers `prepare_stage` S5. `stage_S5` raises `resolve_return: {"dispatch_id": R, ...}`.
- The person answers "accept it". The words are filed under R.
- Next entry: `prepare_stage` S5 again. `stage_S5` raises the identical packet again, and so on until the stuck seam.

D3 AMENDED's text ("the person's words resume the role on today's road") and the Lead's reason for dropping `same_returned_id_twice_raises_named`
("no loop once it is a Refusal") both assume `next` offers the return. The plan critic t-2227 B-1 (:52-54) showed that it does not.

The L5 obstacle the builder met is real only for `_act_resolve_return` (driver_machine). It does not apply to the move itself:
`Driver.resume_role` lives in `driver_dispatch` (driver-layers.json row 165), BELOW `driver_stages`, so `stage_S5` may call it.

Fix (one fix round, inside A1's owns `stage_S5` block): in the branch, when `self.state["pending_words"].get(returned["id"])` holds words, take
the same move `_act_resolve_return` takes. Best is to lift its three lines (words + stage + role -> print -> `resume_role(..., complete=self.completion_for(...))`)
into one helper homed at `driver_dispatch` or `driver_stages`, called by both `_act_resolve_return` and `stage_S5`. That keeps one move and
no copy (AR-15). Then return, so the stage re-enters. Raise the packet only when no words are filed. Test: rewrite the "words filed" part of
the key so `resume_role` IS called once with R and the words, and add a key that walks the two entries (packet -> words filed -> re-entry
resumes, no second packet). Correct the state-exits row's way-out text and the :11861-11862 comment to the road that actually runs. Read N1
below before you choose `complete=`.

## Non-blocking fixes

- **N1 (Lead decision, adjacent to B1): after the return is resolved, the stage still ends in the old refusal.** `completion_for("S5", role)`
  answers `False` for any role but the critic (`story_run.py:17371-17372`). So the resumed mechanical round R (an automator) finishes
  `--not-complete`. Then every window is critic-accepted, nothing is returned or owed, and the next entry raises "every window is accepted ...
  run `controller.py --operation recover`" (:11884-11887). On the live road the same round closes S5 with `complete=last` (:12096). Under D3's
  wording this is legitimate (the refusal's own state), but the person-facing exit then is "recover", not "the stage re-enters and closes".
  This is outside A1's owns (`completion_for`). Either name it in the state-exits row or queue it: an S5 mechanical-round completion on the
  recovery road through `s5_last_fn(record.scope)`.
- **N2 (DUPLICATION, AR-15): the D1 line repeats `s5_last_fn` verbatim.** :11931-11934 (`try: last = not self.s5_open_windows(excluding=...)
  except: last = False`) is the body of `s5_last_fn` (:11605-11612, same layer driver_stages). Write `last = self.s5_last_fn(window.get("scope")
  or [])()`. Or pass the callable itself, as the chain road does: `s5_review` / `s5_mechanical_round` accept a callable, and that reads the rule
  at the finish instead of at entry.
- **N3 (DUPLICATION, D3 AMENDED "text not retyped"): the action dict is a hand copy of the controller's.** :11877-11883 retypes all 9 keys and the
  default reason sentence of `controller.py:8560-8569`. Today the key set is complete (action, dispatch_id, stage, role, dispatch_status,
  digest, options, retry_reason, reason: 9 = 9, and `_act_resolve_return` reads only `dispatch_id`). A later edit on one side drifts silently.
  Minimum now: one pin test that builds a state where R is NOT hidden, takes `Controller._next_action_for_state(...)` for it, and asserts it
  equals the driver's dict for the same record. Queue the lift (a controller-side `resolve_return_action(record)` both call). The builder
  reported this as analog 1.
- **N4 (test assertions weaker than their names).** (a) `n1_reads_nothing`'s last check "returns without reading" only asserts `None`. The rig's
  `controller_state` does not raise, so a read would pass unseen: make it throw, as the first half does. (b) `closed_by_debt_then_rework_automator_not_refused`
  never goes through `s5_close_debt`. It calls `finish(..., complete=True)` directly, which is the shared point, but the name promises the debt
  road. Either drive `s5_close_debt` with a `repair_limit` debt entry or rename the key.
- **N5 (note text): `s5_release_completed` counts every `*.json` left as "claim(s) left"** (:11710), including a young empty claim that
  `release`'s own rule keeps on purpose, and any non-S5 claim. That gives a false "could not be released" note. Count only S5 claims (or
  readable ones) left. The builder reported this as analog 2.

## Answers to the Lead's questions

**1. D1 invariant.** At N != 1, every `last` of the old body reads `s5_open_windows`. `last` is produced on one line (:11927) by both branches
(owed: `not [w for w in todo if w.scope != window.scope]`; plain: `len(todo) == 1`). :11928 overrides it whenever it is True and `parallel != 1`.
A False is never raised to True, which is the safe direction. No other expression decides last: `s5_window` only passes `last` on to
`s5_review.closes` (:12035) and `s5_mechanical_round` (:12096). The `pending` debt branch (:11855-11857) returns before and closes through
`completion_for`, which reads `s5_open_windows` at N != 1 (:17378-17384). At N == 1: `parallel != 1` is False, so nothing is read.
`s5_open_windows` is not called (pinned by `n1_old_body_reads_nothing`, which makes it raise). The new `s5_parallel_cap()` call at :11858 runs only
when `todo == [] and not owed`, prints only on a bad value (which never reads 1), and the old refusal follows unchanged. `s5_auto_extra` reads
`parallel_windows`, which prints nothing, and adds no line at N == 1. `s5_release_completed` returns before any read. So the N=1 road is
behaviour-equal. B-1 walk: W1 is critic-accepted, and R (W1's mechanical round) is `returned_unaccepted`. `todo` is built by `accepted_by`
(:11847), so `todo == [W2]` and the stage takes the old body (not `len(todo) >= 2`). :11927 gives `last = True`. :11932 calls
`s5_open_windows(excluding=["W2"])`. For W1, `_s5_last_round(rows, {W1})` is R (the last non-discounted non-plan S5 row meeting W1), its
status is `RETURNED`, so W1 is open and `last = False`. W2's critic finishes `--not-complete`. Driven through `stage_S5` itself by
`two_windows_old_body_does_not_close_over_returned_round`, with an accepted control.

**2. D3 as landed.** The mirror is complete: the same 9 keys as `controller.py:8560-8569`, the same `retry_reason_for`, the same default
reason. Nothing breaks for lack of a key, since `_act_resolve_return` reads only `dispatch_id`, and `Refusal.dispatch` is set so `_file_words`
files the words under R. But the road does not work: see **B1**. Yes, the state loops. The conductor answers or the person's words are filed,
the driver re-enters `stage_S5` (R still hidden from `next`), and the same packet is raised with the words still unconsumed. That ends only at
the FR-7 re-ask and the stuck seam. The old refusal is still reachable exactly when no window's last non-discounted round is `RETURNED`
(:11875 falls through) and when the state is unreadable (`except` -> `returned = None`). One asymmetry is acceptable and stays on the safe side:
a returned dispatch with NO scope makes `s5_open_windows` raise (open), but the `stage_S5` branch skips it (`_s5_last_round` needs a scope
match) and raises the old refusal. That is the documented "unreadable: the old refusal".

**3. D4.** Yes. `busy = {"running"} | CT.STOPPED | {CT.RETURNED}` (:11704) uses the controller's names (`"running"` is the literal D4 itself
prescribes). Absent state (`{}`), stage not a dict, status not `"completed"`, dispatches not a collection, an S5 status that is not text, or a
reader that raises: each returns without release (:11694-11712). Pinned row by row in `unreadable_stage_frees_nothing`. `release_stage` is one
loop with a predicate: `release(task_root, prefix, match=...)` (`window_files.py:204-209`), and `release` keeps its single walk and the
empty-claim rule (:170-201). The guard test pins both the young-empty-stays and old-empty-goes rules through `release_stage`. No copy.

**4. D5.** Yes. :3233-3234 sits after `if code: raise Refusal(...)` (:3212-3224), so it runs only on exit 0, in the post-finish block right after
the `s5_release_of_dispatch` call. `complete` is the resolved value there: callables are evaluated at :3147-3148, and a tuple reads as True.

**5. D6.** The chain text is byte-equal: `"...refuses your " "Write or Edit: " + S5_OWN_FILE_DOOR` reproduces the old literal, and the test
asserts `chain[-2:] == [CHAIN_LINE, STAND_LINE]`. The variant shares the door through the one class constant (:11747). The `CHAIN_ONLY_LINES`
edit is a legitimate strip. `clean()` (test_story_run_s5_parallel.py:639-640) removes whole lines with their newline, on both sides. The one
N=1-vs-default difference it hides is the variant line, which D6 makes by design (the guard enforces at N != 1 and not at N == 1). Any other
difference stays visible. It does not touch the frozen N=1 set (`test_story_run_s5_n1_frozen.py`, where the line never appears).

**6. Tests.** `two_windows_old_body_does_not_close_over_returned_round`, `owed_branch_does_not_close_over_open_window` and
`no_returned_round_keeps_the_old_refusal` drive the real `stage_S5` with role calls faked, and each has a control. Good. Every key of §2 as
replaced by D4, and of §9 as amended, is present (21 keys). One key asserts the wrong thing: the "words filed" part of
`returned_last_round_raises_resolve_return_naming_the_dispatch` pins the B1 defect as intended. Weaker than named: N4 (a), (b). Missing: a
mirror-equality pin (N3).

**7. Class completeness, axis 5 (stage twins).** The S6 twin is rightly out of scope. `s6_open_lanes` (:13683-13695) counts a case open
unless `manual_done_cases` holds it accepted, so a returned lane is open by construction. That is the spec §1 / t-2147 C.6 line, so no
returned clause is needed. Q1 and Q4 have no S6 twin, because S6 claims no files. Inside S5 the three close predicates of t-2227 B-1 are now:
(i) `s5_open_windows` plus the returned clause, (ii) the old body at N != 1 through (i), (iii) the N == 1 loop of `completion_for`, which is
the named residual D2 (docstring line present, :11553-11554). The way-out class has one more sibling, the recovery completion of the author's
mechanical round (N1), which is not covered and not queued yet. The Lead should queue it or name it.

## Standing questions

- **DUPLICATION AND CONSISTENCY:** found: N2 (the D1 line is a copy of `s5_last_fn`), N3 (the action dict is copied from the controller), and
  the predicate `last is not None and last.get("status") == CT.RETURNED`, written twice (:11587, :11872): minor, so a
  `_s5_returned_round` helper could carry it. Checked and clean: `release`/`release_stage` (one loop), `_s5_last_round` (one walk for both
  readers), the door constant, and `resolve_return_refusal` (one Refusal builder). Grepped: `s5_open_windows(` callers,
  `resolve_return` across `story_run.py`/`controller.py`, `"running"`/`RETURNED` in the diff.
- **CODE QUALITY:** apart from B1 and N2-N5, none found. Two `if chain:` blocks around an `elif` in `s5_auto_extra` are readable. The broad
  `except Exception` blocks are FR-59 guards that read unreadable as open, never as a close.
- **Architecture AR-n (question 10):** kept: AR-13, AR-14, AR-15 (except N2/N3), AR-17 (the packet goes through the one seam), AR-19 (S6
  twin, answer 7), AR-20 (no ratchet raised, L5 exceptions untouched), AR-28. BROKEN: AR-24 (a person's words reach whatever acts on them,
  B1) and AR-25 (the named way out of the new recorded state does not run, B1). The commit lines claim AR-25 as kept, which B1 refutes.
- **JUDGMENT / AR-29 (question 11):** no check reads a role's text, verdict or form. The new predicates are xref (dispatch status x window
  scope; stage status x dispatch statuses), owned by data. The new `WindowsUnreadable("a returned dispatch of S5 names no cases")` is a
  `ValueError` subclass raised by its own name. It falls in the census blind spot (Q7 of the spec, B2's text). It is caught by every caller as
  "open" and never reaches a role, so it is legitimate. `judgment: none` is correct.

## Trail

Read: the diff 4f96c0eae~1..f32f87c0f (all 10 files). `story_run.py` at f32f87c0f: `finish` :3144-3240, `s5_parallel_cap`/`say_once`
:11469-11486, `s5_open_windows`/`_s5_last_round`/`s5_last_fn` :11544-11612, `s5_release_of_dispatch` :11658-11673, `s5_release_completed`
:11675-11715, `s5_auto_extra` :11747-11772, `stage_S5` :11841-11950, `s5_window`/`s5_review`/`s5_mechanical_round` :11958-12102, `s5_close_debt`
head, `question_body_sha` :660-676, `ask` FR-7 block :4425-4460, `dispatch_action` :16760-16790, `_act_wait_existing_job` head,
`_act_resume_checkpoint` head, `_act_resolve_return`/`resolve_return_refusal` :17177-17204, `completion_for` :17314-17395, `funnel`/`boundary_step`
:18240-18263, `take_answer` branches :19410-19500, `_file_words` :19834-19880. Also read: `controller.py` :8470-8580 (`superseded_by_later_work`,
the returned scan, the `resolve_return` action) and the `prepare_stage` line :8651. `window_files.py` :1-90 (SUBDIR, `_file`) and :160-210.
`driver-layers.json` layers line and rows (`resume_role` driver_dispatch, `stage_S5`/`completion_for`/`s5_last_fn` driver_stages,
`_act_resolve_return` driver_machine). `test_s5_window_leftovers.py` (whole), `test_story_run_s5_parallel.py` :590-680. Spec t-2222 (whole),
plan critic t-2227 :1-60 and the headings/fix list, report t-2251 (whole), the commit messages of both commits, SIBLING_MAP axis 5 table,
`critic_verdict.schema.json`. Rerun (one, fast): `python -B D:/ws2/wt-tr4-10a1/ai-packages/qa-factory/scripts/tests/test_s5_window_leftovers.py`
-> `=== test_s5_window_leftovers: 81/81 ok ===` (matches the builder's line). The other witness lines were checked by consistency only (no test_story_run_*
run, per the dispatch). B1 rests on a code trace (`controller.py:8544-8569` before :8651; `story_run.py:16776`, :19851-19856, :11858-11883) and
on the test that pins the re-raise. It is not a live run.

Needed beyond the manifest: `controller.py` :8470-8580 and :8651 (the `next` order and hiding), `story_run.py` `_file_words`/`take_answer`/`ask` FR-7
block/`dispatch_action`/`completion_for` S5 branch, `driver-layers.json` layer rows, `test_story_run_s5_parallel.py` `clean()`.

First-pass verdict block (superseded by the re-review block at the end of this file; kept as a record, tagged `text` so the checker reads only the current one):

```text
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "B1 D3 as landed: the stage_S5 branch (story_run.py:11858-11883) is reachable only when controller next hides the returned dispatch R behind later S5 work (controller.py:8544-8550, returned scan :8555 precedes prepare_stage :8651), so the person's words filed as pending_words[R] (story_run.py:19851-19856) are never read: next keeps answering prepare_stage, _act_resolve_return (:16776) never runs, stage_S5 re-raises the same packet until the FR-7 re-ask and the stuck seam; the state-exits row, the comment :11861 and the test's words-filed part claim a road that does not run (AR-24, AR-25). Fix: with words filed for R, take the resume move from stage_S5 (resume_role is driver_dispatch, below driver_stages; lift _act_resolve_return's three lines into one shared helper), raise the packet only without words; test the two-entry walk"
  ],
  "fixes": [
    "B1 (above) - resume with filed words from stage_S5 through one helper shared with _act_resolve_return; fix the test, the comment and the state-exits row",
    "N1 Lead decision: completion_for S5 answers False for the author (story_run.py:17371-17372), so a resolved returned mechanical round finishes not-complete and the stage ends in the old recover refusal; name it in the row or queue the recovery completion of the mechanical round through s5_last_fn",
    "N2 the D1 override (story_run.py:11931-11934) copies s5_last_fn (:11605-11612); call self.s5_last_fn(scope)() or pass the callable as the chain road does",
    "N3 the resolve_return action dict (:11877-11883) is a hand copy of controller.py:8560-8569; add a pin test comparing it with Controller._next_action_for_state for an unhidden R, and queue a shared controller-side builder",
    "N4 n1_reads_nothing's last check asserts only None (make controller_state raise); closed_by_debt_then_rework_automator_not_refused never drives s5_close_debt (drive it or rename)",
    "N5 s5_release_completed counts every json left (:11710), including young empty claims release keeps on purpose; count S5 claims only"
  ],
  "class_completeness": "Axis 5: S6 twin rightly out of scope; inside S5 the three close predicates of t-2227 B-1 covered or named (D2); the way-out class had the uncovered N1 sibling plus the B1 words-consumption gap.",
  "trail": {"read": ["see the Trail section above"], "reruns": [{"command": "python -B D:/ws2/wt-tr4-10a1/ai-packages/qa-factory/scripts/tests/test_s5_window_leftovers.py", "result": "=== test_s5_window_leftovers: 81/81 ok ==="}]}
}
```

## Re-review (fix diff 601b793dd)

Scope: `git -C D:/ws1/wt-tr4-10a1 diff b956e4c47 601b793dd` (5 files), checked against my verdict above (B1, N1-N5). Line numbers are the tree
at 601b793dd. `story_run.py` and the test file are byte-identical at branch HEAD 1c0ea4e06 (`git diff --stat 601b793dd HEAD` on them is empty).

**Verdict: fit_with_fixes (NEEDS WORK). 1 blocking finding (B2, NEW, introduced by the N1 change). B1 is closed. N2-N5 are closed.** The
decision to accept belongs to the Lead.

### Blocking finding

**B2 — the resumed author's round closes S5 by `s5_last_fn` whatever its repair cause; a returned `test_defect` round closes S5 with no critic review (silent close, AR-28)**

Where: `story_run.py:11886-11890`. `complete_for` keys on `role == "qa-automator"` alone. The returned record carries its cause
(`repair_cause`, set by the controller at `controller.py:3683`), and the code never reads it.

The live road gives a different completion for each cause:
- a mechanical round: `complete=last` (:12112);
- a `test_defect` round: `complete=False` (the `rework` default, :10680; `s5_author_round` passes none, :12098). The critic reviews the new
  bytes afterwards (`s5_window` `continue`).

The fix gives both causes the mechanical rule.

Failing scenario (N = 3, chains):
1. W1's critic rejects with route `test_defect`. The critic dispatch is accepted (`--not-complete`), so W1's `accepted_by` holds the critic
   (`controller._mark_accepted_by`, :4225-4236: role -> any accepted dispatch over the window).
2. W1's author round R (`repair_cause: test_defect`) comes back `returned_unaccepted`.
3. W2's chain closes with its critic accepted `--not-complete`, because R holds W1 open. W2's later accepted dispatch hides R from `next`.
4. Re-entry: `todo == []`. The person answers the packet, and the words are filed under R.
5. Next entry: `resume_with_filed_words(R, complete_for)`. The role is `qa-automator`, so the completion is
   `lambda: bool(s5_last_fn(["W1"])())`. That excludes W1 itself, and W2 is closed, so it answers True.
6. R's finish is `--complete`, and S5 closes over a repair the critic never saw.

Before this fix round, the same resume went through `completion_for` -> False. The stage stayed open and the old refusal followed. That was a
dead end, but on the safe side.

The test rig never sets `repair_cause` (`returned_rig`, `rec(... role=AUTH)`). So `resumed_mechanical_round_of_last_window_completes_s5` proves
the rule for a round whose cause is absent, not for a mechanical one. Nothing pins the `test_defect` case.

Fix:
- Take the `s5_last_fn` completion only when `record.get("repair_cause") == "mechanical"`. Any other author round gets `False`, which is the
  live road's own value.
- Keys: `resumed_test_defect_round_does_not_complete_s5` (cause test_defect, last window -> False), and `repair_cause: "mechanical"` set on the
  rig of the two existing N1 keys.
- What happens after a resumed `test_defect` round (the window needs a new critic and `todo` excludes it) is the pre-existing gap. It lands in
  the old refusal. Name it in the state-exits row or queue it. Do not close it here.

### Answers

**1. B1: closed.**
- Words filed for R are consumed exactly once. `stage_S5` calls `resume_with_filed_words` (:11891), which calls `resume_role` (:17219).
  `resume_role` pops `pending_words[R]` as soon as the result carries text (:3464) and again after the threshold (:3476).
- The words reach the role through the prompt `The person answered: "<words>"` in the role's own session.
- The packet is no longer raised for words already filed: the branch returns before the raise (:11891-11892). Pinned by
  `returned_last_round_with_words_resumes_role_and_consumes_them` and `second_entry_after_resume_does_not_raise_again`. The second key's rig
  marks R accepted, as a real finish would.
- The old refusal is still reached exactly when no window has a returned last round, when the state is unreadable, or when R's record is gone
  at the resume (:11893). Words of another dispatch are left alone (`words_of_another_dispatch_are_not_used`).
- New loop: none of a new class. If the resume fails before the role answers (no session known: a `Refusal` with `dispatch=R`; or an error
  result with empty text, where the words stay by the t-781 m2 rule), the words stay, R stays returned, and the next entry resumes again.
  That is the same repeat the visible road (`next` -> `_act_resolve_return`) already has. Every turn goes through the seam with the refusal's
  own text, never silently. Inherited, not introduced.

**2. N1.**
- A resumed author round of the last window completes S5, and one of a window that is not last does not: correct, through `s5_last_fn`,
  pinned by the two keys. But only for a mechanical round, and the code does not check that (B2).
- "A resumed critic keeps `completion_for`" is right. `completion_for` S5 for the critic (body unchanged by this diff) reads
  `s5_open_windows(excluding=mine)` at N != 1, and then the route and the person's answer of that critic dispatch. That is the same rule as
  the live critic's `closes` and the recovery road's.

**3. Whitespace-only words.** Acceptable here: the helper is the one move, and `if words` is `_act_resolve_return`'s own test, unchanged by
this diff. A blank answer would resume the role with `The person answered: ""`. Whether `take_answer` can file a blank answer at all was not
checked in this pass. If it can, that is a defect of the filing or of `_act_resolve_return`, to queue against those (not this diff).

**4. N2-N5.**
- N2 closed: :11950 is `last = self.s5_last_fn(window.get("scope") or [])()`.
- N3 closed for now: `resolve_return_action_equals_the_controllers` builds an unhidden state, takes `Controller._next_action_for_state`, and
  asserts the same keys and values. The shared controller builder is queued.
- N4 closed: `n1_reads_nothing` counts reads (zero) and its no-claim half throws on any read. The debt test drives `s5_close_debt` with a
  `repair_limit` debt entry and asserts `finished` and the release.
- N5 closed: :11711-11713 counts only readable `S5|` claims (through `window_files._read`), with a control that does count a left S5 claim.

**5. What the fix round broke or duplicated.**
- B2 above.
- Layer placement is correct. `resume_with_filed_words` is homed in driver_stages, called from driver_stages (`stage_S5`) and driver_machine
  (`_act_resolve_return`, which is higher), and it calls `resume_role` (driver_dispatch, lower). `test_driver_layers` is 54/54 per the
  witness.
- `_act_resolve_return`'s text and behaviour are unchanged: same print, same `resume_role` arguments with `completion_for`, same packet
  without words.
- No second copy: the old three lines now exist only in the helper. The action-dict mirror remains, pinned and queued (N3).
- Nits (non-blocking):
  - (a) The helper sets `self.boundary = f"{stage}:{dispatch}"` (:17214) before it knows it will resume. On the record-gone road the old
    refusal is then raised under boundary `":R"` instead of `"S5"`. This matters only for that rare edge.
  - (b) `window_files._read` is a private reader used across modules (:11713). It is the right reader (AR-13); a public alias would be
    cleaner.

### Standing questions (fix diff)

- **DUPLICATION:** none new. Checked: the helper replaces the copy in `_act_resolve_return`, and the `s5_last_fn` reuse (N2) removed one.
  Grepped `resume_role(` and `s5_last_fn(` in the fix diff.
- **CODE QUALITY:** B2, plus nits (a) and (b).
- **AR-n:** AR-24 and AR-25 are now kept (B1 closed). AR-28 is BROKEN by B2 (a silent close over an unreviewed round). AR-15 is kept.
- **JUDGMENT / AR-29:** unchanged. The new branch reads statuses and the presence of words. It does not read the words' meaning: the role reads
  them.

### Trail (re-review)

Read:
- the fix diff b956e4c47..601b793dd (all 5 files);
- `story_run.py` at 601b793dd: `record_running` and `resume_role` (:3380-3488), `stage_S5` :11855-11952, `resume_with_filed_words` and
  `_act_resolve_return` :17195-17225, `rework` signature :10679-10681, the `s5_author_round` / `s5_mechanical_round` rework calls :12098, :12111-12112;
- `controller.py` at 601b793dd: `_mark_accepted_by` :4225-4236, `repair_cause` writer :3683, `REPAIR_CAUSES` :232.

Rerun (one): `python -B D:/ws2/wt-tr4-10a1/ai-packages/qa-factory/scripts/tests/test_s5_window_leftovers.py` ->
`=== test_s5_window_leftovers: 114/114 ok ===`, which matches the witness. The other witness lines were checked for consistency only.

B2 rests on a code trace (:11886-11890 against :10680, :12098, :12112, controller :3683, :4225-4236) and on the rig's missing `repair_cause`.
It is not a live run.

Re-review verdict block (superseded by Re-review 2 below; kept as a record, tagged `text`):

```text
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "B2 (re-review, new in the fix round): story_run.py:11886-11890 gives every resumed qa-automator round the s5_last_fn completion, ignoring record repair_cause; the live road gives a test_defect round complete=False (rework default :10680, s5_author_round :12098) and only the mechanical round complete=last (:12112). Scenario N=3: W1 critic rejects test_defect (critic accepted, so W1 leaves todo), W1's test_defect round R returns, W2 closes and hides R, the person's words resume R with complete=s5_last_fn(W1) -> True, S5 closes over a repair no critic reviewed (AR-28). Fix: s5_last_fn only when repair_cause == mechanical, else False; add key resumed_test_defect_round_does_not_complete_s5 and set repair_cause mechanical in the two N1 rigs"
  ],
  "fixes": [
    "B2 (above): condition the resumed author's completion on repair_cause == mechanical, test_defect and others get False; pin both",
    "Name or queue the pre-existing gap after a resumed test_defect round (the window needs a new critic, todo excludes it, the old refusal follows)",
    "Nit: resume_with_filed_words sets self.boundary (:17214) before it knows it resumes; on the record-gone road the old refusal carries boundary ':R'",
    "Nit: story_run uses the private window_files._read (:11713); a public alias would keep the reader public"
  ],
  "class_completeness": "B1 closed for both callers of the one move through one helper; N2-N5 closed; the completion class of a resumed S5 author round was incomplete (B2). Axis 5: S6 twin still rightly out of scope.",
  "trail": {"read": ["see the Trail (re-review) section above"], "reruns": [{"command": "python -B D:/ws2/wt-tr4-10a1/ai-packages/qa-factory/scripts/tests/test_s5_window_leftovers.py", "result": "=== test_s5_window_leftovers: 114/114 ok ==="}]}
}
```

## Re-review 2 (round 3, 433eb32d1)

Scope: `git -C D:/ws1/wt-tr4-10a1 diff 1c0ea4e06 433eb32d1` (5 files, +214/-16), checked against B2 and the two nits above. Line numbers
are the tree at 433eb32d1. `story_run.py`, `window_files.py` and the test file are byte-identical at branch HEAD 0cbafeed2 (`git diff --stat
433eb32d1 HEAD` on them is empty).

**Verdict: accept (fit). No blocking findings. B2 is closed and both nits are closed. One item to note: the `todo` gap after a resumed
non-mechanical round goes to a pile finding, which the Lead files.** The decision to accept belongs to the Lead.

**1. B2: closed.**
- `complete_for` (story_run.py:11890-11896) returns `False` for a `qa-automator` unless `CT.repair_cause(record) == "mechanical"`. Only a
  mechanical round reaches the `s5_last_fn` rule.
- `controller.repair_cause` (controller.py:254-256) is the one reader. It maps any absent, empty, non-string or unknown value to `"test_defect"`
  (`str(... or "test_defect")`, then a membership test in `REPAIR_CAUSES`). So every odd input lands on False, the safe side. No second reader
  is added.
- `CT` is bound by the `import controller as CT` in the same block's `try`. `complete_for` runs only after that block succeeded with a
  `returned` row, so the name is always bound.
- No resumed round other than a mechanical one can complete S5:
  - a critic goes through `completion_for` (unchanged);
  - every other automator cause gets False;
  - a mechanical round gets True only when no other window is open.
- Pinned:
  - `resumed_test_defect_round_does_not_complete_s5` runs the same three-window rig with only the cause flipped: test_defect -> False,
    mechanical -> True. That proves the cause decides it.
  - `resumed_round_with_no_cause_does_not_complete_s5` covers absent, `""`, `"whatever"`, `7` and `environment`, all False. Its critic case
    shows that `completion_for` is passed through unchanged even when the record says `repair_cause: mechanical`.
  - The two N1 rigs now carry `repair_cause: mechanical`.
- The builder's mutation claim ("6 checks red" with the condition removed) is consistent with these keys: 1 in the test_defect key and 5 in the
  no-cause loop. I did not run the mutation myself.

**2. The `todo` gap goes to a pile finding: acceptable for THIS diff.**
- A1 only exposes the gap; it does not make it worse.
- Before A1, a hidden returned `test_defect` round R ended in the same old "every window is accepted ... recover" refusal. W1 was
  critic-accepted, so it was out of `todo`, and nothing read R.
- After A1, the person's words reach R and R finishes `--not-complete`. The next entry reaches the same refusal, now with the repair actually
  done by the role.
- Two things that were not reachable before are now: the words are used, and nothing closes silently.
- The same gap exists on the live road after a crash between the author round and the next review. That is the builder's point, and it is
  consistent with `_mark_accepted_by` (controller.py:4225-4236): any accepted critic of the window counts.
- The door the state-exits row names is real as a door: the old refusal tells the person to run `controller.py --operation recover`. Whether
  `recover` then re-routes the window to a critic is NOT verified here. The row says "known gap (not closed here)" and no more, which is the
  honest form.
- The fix belongs in the pile finding the Lead files: one predicate, "the last round is an accepted non-mechanical author round", read by
  `todo` and by `s5_open_windows`.

**3. Nits: both closed.**
- (a) `stage_S5` saves `stage_boundary = getattr(self, "boundary", "S5")` (:11897) and puts it back when the helper returns False (:11902). The
  helper and `_act_resolve_return` are unchanged. Pinned by `record_gone_refusal_keeps_the_stage_boundary`, whose control shows the visible
  road still raises its packet under `S5:m1`.
- (b) `window_files.read_claim` is the public reader. `_read = read_claim` is kept as an alias for the module's own call sites (one function,
  two names, no copy), and `s5_release_completed` calls `read_claim` (:11713).

**4. Nothing new broken.**
- The diff touches only the `complete_for` closure, the boundary save and restore, the reader's name, comments, the state-exits row and tests.
- A resumed non-mechanical round now passes `complete=False` to `resume_role` -> `finish`, which sends a plain `--not-complete`. This is the
  same value `s5_author_round` passes on the live road (`rework` default). The controller's refusal of a bare `--not-complete` applies only to
  the stage's closing critic.
- DUPLICATION: none. `repair_cause` reuses the controller's reader, and `read_claim` is one function with a kept alias.
- CODE QUALITY: none found.
- AR-28 is now kept (B2 closed). AR-13: `repair_cause` and `read_claim` are the one reader each. AR-24 and AR-25 are kept.
- JUDGMENT / AR-29: unchanged, because the code reads a typed cause field and never judges the role's text.

**Trail (re-review 2).**
- Read:
  - the fix diff 1c0ea4e06..433eb32d1: the story_run.py and window_files.py hunks in full, the test hunks (all new and changed keys), the
    state-exits row;
  - `controller.py` at 433eb32d1, `repair_cause` :250-262.
- Rerun (one): `python -B D:/ws2/wt-tr4-10a1/ai-packages/qa-factory/scripts/tests/test_s5_window_leftovers.py` ->
  `=== test_s5_window_leftovers: 128/128 ok ===`, which matches the witness. The other witness lines were checked for consistency only.

```json
{
  "verdict": "fit",
  "blockers": [],
  "fixes": [
    "Lead (not this diff): file the pile finding for the todo gap after a resumed non-mechanical author round (one predicate 'last round is an accepted non-mechanical qa-automator round' read in todo and s5_open_windows; the same gap on the live road after a crash between the author round and the next review); whether controller recover re-routes such a window to a critic is unverified"
  ],
  "class_completeness": "B1 closed for both callers of the one resume move; B2 closed: a resumed author round completes S5 only for repair_cause mechanical (controller.repair_cause, the one reader; absent/unknown/odd -> test_defect -> False); a resumed critic keeps completion_for. The remaining sibling (todo / s5_open_windows blind to a non-mechanical author round after an accepted critic) is pre-existing, exposed not worsened, named in the state-exits row and handed to a Lead pile finding. Axis 5: S6 twin rightly out of scope.",
  "trail": {
    "read": [
      "git diff 1c0ea4e06 433eb32d1 (story_run.py and window_files.py hunks in full, test hunks, state-exits row)",
      "wt-tr4-10a1 controller.py at 433eb32d1: repair_cause 250-262",
      "own earlier sections of this file (B1, B2, nits)"
    ],
    "reruns": [
      {
        "command": "python -B D:/ws2/wt-tr4-10a1/ai-packages/qa-factory/scripts/tests/test_s5_window_leftovers.py",
        "result": "=== test_s5_window_leftovers: 128/128 ok === (matches the witness line)"
      }
    ]
  }
}
```
