# t-2018 - critic re-review of the walker fix round (16b0d74b1, on head 053c7feb4)

**Verdict: fit_with_fixes. No finding blocks the live run; N1, N2, N3, N5 block the merge.** The decision is the Lead's. F1, F3, F4, F6 hold on the road they named; F2 is closed only for its two witnessed shapes. The fix round left the F2 class open and closed one F2 shape with a quote the role never wrote.

## Old findings

| | Status | Proof |
|---|---|---|
| F1 | CLOSED on the charter road; two edges open (N4, N10) | probe: step + final + verdict -> real build -> `pass`; refs `pre_action start`, `post_action completion` |
| F2 | PARTLY: G and H pass, neighbours do not (N1, N2); H is closed by N3 | probes below |
| F3 | CLOSED: mixed rows (inconclusive, refused, unprepared_walk) through real `handoff_check --fix`: `exit 0, applied 60 value(s)`. Words: N8 | probe |
| F4 | CLOSED for resume and for `_act_wait_existing_job`: real halt -> a1 `inconclusive`, real resume -> a2 `passed`, with `record_from_walk` NOT mocked. Remainder: N5, N6, N7, N9 | probe |
| F5 | CLOSED by reading and its test (roles mocked; no real two-account sign-in run). `walk_old_road` has no reader: AR-22, named by the builder, not queued | grep: writer `story_run.py:3345` only |
| F6 | CLOSED. `_case_sections` over `traceability._sections` splits on `## ` exactly as before (`traceability.py:1593`) | read |
| F7 | NOT VERIFIED: not run by the instruction, not read by me. CI judges | - |
| F8, F10 | queued, as before; N3 makes F10 worse | - |

## New findings

**N1. HIGH, blocks merge. `op_verdict` still accepts what the build refuses: no captures.** `manual_evidence.py:1517-1545` does not ask `_attempt_files` (:1734), and `_result_errors` skips `evidence_refs required`.
```
verdict with no step, Then-level limitation : verdict 0 ok | build refused: attempt a1 ... holds no captures: capture first
goto only, inconclusive with limitation     : verdict 0 ok | build refused: the same
```
The roads: the brief's own "Case file: not found ... say so in its verdict", or an item the walker declines to touch. Result: re-queued, then `left_unchecked`. Fix: `walk_rule_errors` reports no captures with a door (`look`); or `op_verdict` takes one `look` itself for an attempt with none (P26: code writes the evidence). Prefer the second.

**N2. HIGH, blocks merge. Same class: `surprise` citation.** `_surprise_cite_errors` is called at build (`manual_evidence.py:1882`), never in `walk_rule_errors` or `verdict_problems`.
```
observation {..., "surprise": "status 404 on /x"} : verdict 0 ok | build refused: observations[0].surprise ... is no surprise line of a1
```
The charter says "A `surprise:` line goes into one too" and names no key and no id. These are the places P26 wants recorded, and they lose the case. Fix: ask it in `walk_rule_errors` with the known ids; name the id in the charter.

**N3. HIGH, blocks merge. The fallback quote is not a quote.** `manual_evidence.py:1471-1484,1501-1504`. See answer 2.
```
{"expected": "the error banner says why", "seen": "nothing happened"} -> record: "quote": "form: aria heading: Cart button: Pay"
picture capture -> record: "quote": "page"
```

**N4. MEDIUM, fix before merge. `pre_action` lands after actions; the door invites a false "before".** `walk_session.py:992-1012`, `PRE_DOOR` :331. See answer 1. Fix: `_with_pre_action` inserts nothing once the attempt holds a non-`goto` action beyond the sign-in; the rule asks that the before-picture's row stands before the first such action (order of rows, data, AR-29 safe); the door says "sign in in a call of its own", or `inconclusive`, and never "take your own" after acting.

**N5. HIGH, blocks merge. Off the live road S6 can complete over a re-queued case.** `story_run.py:16217` `manual_plan(scope, skip=mine)` with :12418 `gone = ... | skip`; the guard `walk_pending` stands only at :12842.
```
state walk_retry {TC-2: open}, own scope [TC-1, TC-2]:
completion_for True | live road walk_pending True | plan without skip [['TC-2']]
```
F4 routes the cut, the never-launched launch and the person's resume through `completion_for`. So a refusal after any of these asks `finish --complete` instead of "walked once more" (E5s.1). I did not trace what `finish` answers: either the stage closes, or the exit check refuses it and no lane re-walks. Fix: `completion_for` S6 manual reads `walk_pending(mine)` first; a test on that road.

**N6. MEDIUM, fix before merge. `_finish_saved_result` has no hook.** `story_run.py:15878-15880`. The saved result is written (:2933) before `after` runs. A driver killed during `after` (close 5.8 s, then build, finalize) re-enters by `_act_wait_existing_job` -> `_finish_saved_result` -> `handoff`, with no `walk_after`: unbuilt items stay, the form has no values. `walk_after`'s docstring promises "a reused saved result runs it safely"; this road never calls it. A third caller, not by `run_role`, so "whoever called it" does not hold. By reading. Fix: call `walk_after` there when `state/walks/<dispatch>.json` exists.

**N7. LOW, queue. `run_role` reopens before it reads the saved result.** `story_run.py:2911` before :2923.
```
saved result present -> py calls [('walk_session.py', 'open'), ('story_step.py', 'bind')]; "reusing the saved result"
```
A browser, a sign-in and the lease (13-23 s, t-2013) for no role. Harmless, not free. Fix: move the reopen under the no-saved-result branch.

**N8. MEDIUM, fix before merge (FR-41). `walk_values` overstates what was walked.** `story_run.py:3520-3610`.
```
3 rows (1 inconclusive, 1 refused never walked, 1 unprepared):
run.witness = ... 3 manual case(s) walked | tried[0].technique = ... over 2 walked case(s)
scope[1].executed = fresh | scope[1].reason = record refused 1x
```
See answer 3. Fix: count rows with steps; `executed` only for an attempt that ran, else a dash (the form's enum needs a check); `reason` carries the row's reason, cut to 80.

**N9. MEDIUM, fix before merge. Stale form after a late verdict.** Guard in `walk_values` (`values.applied.yaml` exists -> return), :3531. Road: handoff applied, then a question stop or a digest halt, then `resume_role` -> real verdict -> rebuilt record.
```
second walk_values with a changed row: values written False, form unchanged True
```
The form says `inconclusive` while the record says `passed`, and the analyst reads the form. Fix: on changed rows write the values again and apply them over (check that `handoff_check --fix` overwrites); or say so in the form.

**N10. MEDIUM, a charter/server choice for the Lead. A read-only item is refused at its first pass.** Item `goto`, `look`, `--final`, `pass` under `ui`: `verdict 2 ... ui requires pre_action`. Own capture, `final` again: `verdict2 0 ok`. The door leads with `inconclusive`, so a display check may turn inconclusive for want of a picture of the same page; `test_verdict_refused_...` pins the refusal. Fix: `_take_final` takes `capture pre_action start` first when the attempt holds no action and no before-picture. Watch on the canary.

**N11. LOW, queue. A case nobody walked is reported as a refused record.** Halt before item 3, in two lanes: `refused: 2`, "the record of its walk was refused twice", `request.json` overwritten `left_unchecked`. State right, words wrong (FR-41). Fix: a `missing_verdict` refusal says "not walked".

**N12. LOW. Tests.** `test_halt_after_item_1...` stubs `record_from_walk`, asserts `in (0, 2)` and force-writes the verdict: it would not catch a broken rebuild (my probe covers that once, no pin). The report carries no mutation list (brief, mechanical layer): requested.

## Answers

**1. F1.** Never in the window: yes (checked at call start, scan stops at `fill-account`, row order proved). Twice on a corrected call: no (`added2 None`). Twice only when the role sends its own capture in the same call (`001-pre_action-mine`, `002-pre_action-start`), harmless. After an action: **yes**:
```
goto, fill-account, fill-account, click "#a", click "#b", capture pre_action start, click "#c" -> pass, refs pre_action start
goto, fill-account, click "#a", look, capture post_action completion, capture pre_action late -> verdict 0 ok
```
The first is a "before" taken after two actions. The second is the door's own road. N4. It needs `fill-account` plus an action in one call; a signed-in lane never meets it.

**2. F2.** One rule function: yes, `validate` and `walk_rule_errors` share `_result_errors`, `_observation_errors`. It does not cover the build's other refusals: N1, N2. No other role-actionable refusal found in `build_record` (read :1806-1917; `_then_quote_problems` covered by `verdict_problems`). Provenance, the end probe and a block validate stay out by design, as the docstring says.
The quote: **not a true quote; it is an evidence claim the role did not make.** P26: a conclusion is accepted only if it cites a recorded piece of evidence. Here code writes the citation, unmarked, in the role's field, then checks that it is present in the file it came from: a check that cannot fail for any observation naming a text capture. The analyst reads the page's header as what the role pointed at. The AR-29 presence check is emptied, and the role's word is written by code. The changelog (`changelog.d/t-1957-fix-round.md`) says "an observation with no quote ... is refused", which is false for that shape. My own H (t-2013) asked to stop losing the case; F2 now gives a live refusal with a door, so the fallback has no job left. Fix: delete `_own_words` and refuse at the verdict; the charter names `quote`. A hand-written record goes to the existing re-queue. If the Lead keeps a fallback: an explicit `quote_by: code` the analyst's brief explains, and `judgment: none` of this commit restated.

**3. F3.** Invented: the `run.witness` count, `executed: fresh` on a never-walked row (N8). Named gaps are honest (`-`, `not_recorded`, "not established"). `inputs_read[2].version` from the probe matches the form's meaning. `run.probe_after` = the same file holds both probes: true. The Thens are verbatim, `observed` is the record's. Three claims are constants `True`: true by construction, with one caveat: `every_blocked_row_...` holds because an env-blocked attempt becomes `manual_skipped` "record refused", which drops the remedy (the reason fix in N8 covers it). `unprepared_walk` is outside the form's listed `row_states` comment, the check passes it: exit 0 above; not traced further.

**4. F4.** Reused saved result: N7 (`run_role`), N6 (`_finish_saved_result`). Double after-step: safe: the marker skips, a real verdict rebuilds, `retry.pop`, `after_end` is replaced; the only trace is a noise note `close exit 3`. Stale form: N9. Two blocks of one case stay on disk; the reducer orders by start (`finalize_task.py:50-71`, read, not run), the re-judge rule. Person's halt: `after` before the halt check, the form is read before values are applied, so `halt` is not overwritten; marked records are no verdict; the resume walks them. Words: N11. Completion after the resume: N5.

**5. `# remains:`** Legitimate door, not silenced: A27 counts results "dropped or only printed", a false red has this door, 41 such lines live in `story_run.py`. Each reason read:
- `:3320` app card: true; the brief names the path unconditionally, a missing card means `look`.
- `:3428` close: true but thin: "ends by itself" is up to `idle_s` 900 s holding the lease, so the next lane's `open` may leave the walker and the items have no end probe. Said, re-queued, no stop.
- `:3440` finalize: true only when the report is missing; `walk_before` made one, so the usual failure is a STALE report, and the form then passes with old totals. Partly true.
None is a state needing the conductor (AR-17). Quality: the survivor for kind T is `py_trace` (:1297), which journals `trace_failed`; `:3428` and `:3440` only print a line and could use it. Fix before merge, low. `NO_MOVE_BASELINE_MAX` stays 51.

**6. Census.** Not this diff. Cause: `walk_session.py:240`, `raise ValueError(f"item ... lane is not a plain id...")` inside `request_problems`, from merge **8ebbfde11 (t-2011 analyst U0)**. The scanner counts a `raise ValueError` as a site, which made `request_problems` blocking with role `conductor`.
```
ec7e3c536 new [] | 8ebbfde11 new [('walk_session.py', 'request_problems')]   (units_of, per commit; offset -2 without the registry)
head: 468, site line 240 | temp copy with that raise -> out.append: 467
```
Shrink: the raise sits in a `try` whose `except ValueError` only appends the text: append directly, with the same guard, and skip `case_dir_name`. Behaviour unchanged, refusal still through `_refuse` (blocking row). Dense at 467; no raise. Red since 8ebbfde11, so CI's census row is red on this branch regardless of the walker. Its owner is t-2011 by attribution; the Lead routes it. A proof on a byte copy, not a patch to the tree.

## Standing questions

**Fit:** see the table. **Own decisions:** `final_also_actions` safe; `_own_words` not (N3). **Seams:** `run_role` hook additive, plain dispatch untouched (test, `plain`). **Class:** F2 class neighbours N1, N2; F4 class neighbours N5, N6. Axis: `docs/SIBLING_MAP.md` still has no row for "a later check refuses what the earlier gate accepted" (grep `walker|walk_`: only the shell walker; hits prove the pipe): my t-2013 proposal stands, unqueued.
**DUPLICATION AND CONSISTENCY:** `walk_actors` repeats the tail of `manual_capture.auto_actor` (builder named it, `manual_capture.py` outside `owns`): queue. `brief_pack._case_sections` duplicate is gone. `_with_pre_action` and `final_state` build the action set separately, by different data keys (`pre_not_before`, `final_also_actions`): one helper, queue. `py_trace`: answer 5.
**CODE QUALITY:** `run_role(after=)`: no package caller left (grep: def :2855, docstring :3419; test `test_walk_lanes.py:120` only): remove it or keep it named as a test seam; queue. `PRE_DOOR` is appended to every rule error, including ones unrelated to pictures: split, queue. `walk_case_records` and `walk_refusal` resolve the 80-line note. `walk_facts` one-line returns over 150 chars: nothing.
**Tests:** N12. **Hygiene:** not re-run; the batch canon's.
**Ratchets:** census +2 rows, class `shape`/`xref`, role qa-runner, non-blocking (qa-runner stays 132): classes honest. `role-load` 15566 -> 15560, 14407 -> 14401: down. `driver-layers`: +5 methods, +`walk_old_road`, no upward edge. A27: 3 doors, no raise. `forge-check` of this branch not attached: requested.
**ARCHITECTURE:** AR-14, 15, 19, 21, 25, 28, 29 named. AR-29 weakened by N3; AR-28 and AR-25 by N5; AR-22 by `walk_old_road`.
**JUDGMENT:** no check judges a role's meaning. `judgment: none` holds for the checks, not for N3, where code writes the role's citation.

## For the live run (input to the Lead)
No need to stop it. Look in the log for: `holds no captures`, `observations cannot be used`, `would be refused` on read-only cards, `added_step` after a sign-in, and any `was refused` followed by a stage close.

## Spot-checks and negatives
- "No package caller of `after=`": grep `after=` over `story_run.py`, the def line hits (control).
- "No reader of `walk_old_road`": grep over scripts, the writer hits (control).
- "`_own_words` is the only fallback": grep `first words|QUOTE_FALLBACK|_own_words`, other hits in `adapter_forms.py`, `story_step.py` unrelated.
- "Red at base": confirmed and located (answer 6). "328/328": rerun.

## Trail
Read: t-2013 verdict; t-2016 report; brief; the diffs of `walk_session.py`, `manual_evidence.py`, `story_run.py`, `brief_pack.py`, charter, census, driver-layers; `test_walk_road.py` whole; `walk_session.py:410-504,690-1110`; `manual_evidence.py:155-280,1548-1928`; `story_run.py:2854-2978,3224-3333,3378-3457,12408-12432,15801-15890,16179-16219`; `manual_capture.py:3296-3340`; form template :34-80; `audit_factory.py:1598-1623`; `test_judgment_census.py` :199-250, :335-400, :415-437.
Reruns: `test_judgment_census.py` -> `20/21 ok`, C3 conductor 468; `test_audit_rules.py` -> `328/328 ok`. Probes through the real `Walk` (fake browser), real `build_record`, real `handoff_check`, temp stories only, sent on stdin, nothing written in a tree. Census by commit: temp copies by `git archive`. No slow file, no docker, no ratchet tool, no real browser; `tr-walk`, `pkg-walk` and the stand's lease untouched. My background census job over the later commits may still run for some minutes; it writes only to temp.
Needed beyond the manifest: `manual_capture.py`, `audit_factory.py`, `refusal_registry.py`, `traceability.py`, `finalize_task.py`, the form template, `test_judgment_census.py`, `story_run.py` beyond the diff.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "fixes": [
    "BLOCKS MERGE N1 manual_evidence.py:1517-1545: walk_rule_errors asks for captures, or op_verdict takes a look for an attempt with none",
    "BLOCKS MERGE N2 manual_evidence.py:1882: surprise citation asked while the session lives; charter names the id",
    "BLOCKS MERGE N3 manual_evidence.py:1471-1504: delete the fallback quote, refuse at the verdict; changelog corrected",
    "BLOCKS MERGE N5 story_run.py:16217: completion_for reads walk_pending for its own cases, with a test",
    "FIX BEFORE MERGE N4 walk_session.py:992-1012,331: no insertion after an action, door does not invite a late before picture",
    "FIX BEFORE MERGE N6 story_run.py:15878: _finish_saved_result runs walk_after when a walk record exists",
    "FIX BEFORE MERGE N8 story_run.py:3520-3610: witness count, executed and reason say what was walked",
    "FIX BEFORE MERGE N9 story_run.py:3531: values re-applied when rows change after a late verdict",
    "LEAD CHOICE N10: final takes the before picture on an item with no action",
    "CENSUS walk_session.py:240: raise inside request_problems becomes out.append; 468 -> 467, no raise (from merge 8ebbfde11, t-2011)",
    "LOW: N7 reopen under no-saved-result; N11 words for a never-walked case; N12 pin the real rebuild, attach the mutation list; py_trace at story_run.py:3428,3440; run_role after= keyword; PRE_DOOR split"
  ],
  "class_completeness": "F2 class (a later check refuses what the earlier gate accepted): neighbours N1 and N2 not closed; still no axis in docs/SIBLING_MAP.md (grep with a control), proposal from t-2013 stands. F4 class (every road of a walk dispatch has the hook): run_role and resume_role wired; _finish_saved_result (N6) and completion_for (N5) not. Twins door, progress, driver keep walk_lanes. walk_actors vs auto_actor and walk_old_road reader named by the builder, not queued.",
  "trail": {
    "read": [
      "docs/tasks/specs/reviews/t-2013-critic-walker-slice1.md",
      "docs/tasks/specs/reports/t-2016-walker-fix-round-report.md",
      "docs/tasks/critic-diff-brief.md",
      "git show 16b0d74b1 (all package diffs except test_story_step_manual_block.py)",
      "ai-packages/qa-factory/scripts/walk_session.py (ranges)",
      "ai-packages/qa-factory/scripts/manual_evidence.py (ranges)",
      "ai-packages/qa-factory/scripts/story_run.py (ranges)",
      "ai-packages/qa-factory/scripts/tests/test_walk_road.py",
      "ai-packages/qa-factory/scripts/tests/test_judgment_census.py (ranges)",
      "ai-packages/qa-factory/scripts/audit_factory.py:1598-1623",
      "ai-packages/qa-factory/handoffs/s6-runner-to-analyst.yaml (ranges)"
    ],
    "reruns": [
      {"command": "python -B scripts/tests/test_judgment_census.py", "result": "20/21 ok, C3 conductor 468 above 467"},
      {"command": "python -B scripts/tests/test_audit_rules.py", "result": "328/328 ok"},
      {"command": "probe: real Walk, fake browser, real build_record, verdict shapes", "result": "no captures and unknown surprise: verdict ok, build refused; quote fallback written unmarked; pre_action after two clicks accepted"},
      {"command": "probe: real halt and resume, record_from_walk not mocked", "result": "a1 inconclusive, a2 passed, retry empty"},
      {"command": "probe: walk_values on mixed rows through real handoff_check --fix", "result": "exit 0; witness says 3 walked, tried says 2"},
      {"command": "probe: completion_for with an own case re-queued", "result": "True, while walk_pending is True"},
      {"command": "probe: census on git archive copies per commit", "result": "request_problems new at 8ebbfde11; head 468; copy with raise replaced 467"}
    ]
  }
}
```
