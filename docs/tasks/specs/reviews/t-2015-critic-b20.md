# t-2015 — critic on the B-20 batch (spec t-1988, N1-N5)

**Verdict: fit_with_fixes (NEEDS WORK).** The live cause is fixed, measured below. Two fixes block the merge: F1 (F2 of the spec is half done, FR-4) and F4 (red `forge-check`). F2 and F3 are fix-before-merge. Acceptance stays with the Lead.

Lines are `D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\` at head 20317b442.

## Findings

**F1. HIGH, blocks. `consumer_person_pass` honours a word of any age at every site but the new step.**
- Where: `story_run.py:9723-9735` (`since=""` by default). Callers without `since`: `:9797` (`consumer_need_record`: S6 `s6_reprobed_close`, `s6_reentry`, `manual_close`; S7 `s7_close`), `:9872` (`consumer_settled`), `:12887` (`s7_await_scribe`).
- Control run (probe, real `consumer_word_step`, a word dated before the acceptance): `step = False | old-site call (no since) = True | record quote = by: person - accept whatever comes`. One word, two answers in one run.
- Failure scenario: this very tree carries live S6 and S7 `stage acceptance` waivers, and waivers never expire. The scribe rejects → `consumer_settled` reworks the analyst → the new dispatch reaches `s7_await_scribe`, where the old waiver passes it with no `since`. Work the person never saw is accepted, against FR-4. Same at `:9872`: an old word overrides a reject record.
- Fix: compute `since` inside `consumer_person_pass` for the waiver road (no `answer`). Move the event-store read out of `consumer_word_step` so that function goes back to a plain loop over `CONSUMER_ROUTES`; unreadable time = not honoured. `answer=` stays exempt, it is a fresh word (`code_close.behind` `go on`, `s7_open_words`). Test every site with a word older than the acceptance. CI-only files that may pin any-age behaviour: `test_story_run_s7_live.py`, `test_s7_investigation_replay.py`, `test_stage_review_person_pass.py`.
- Spec F2 says (b) "also changes the three existing S6 sites". The builder flagged this as a question (t-1990, deviation 4), it was not hidden. The decision is the Lead's; my recommendation is (b) everywhere.

**F2. MEDIUM, fix before merge. `--dry-run` now writes an acceptance record.**
- Where: `story_run.py:9699-9721`, loop step at about `:16190`. `py()` (`:1220`) has no dry guard; the sibling `code_close_step` has one (`:16563`).
- Control: `P2 dry=True: step = True | record written = True | cmds = ['stage_done.py', 'project_decisions.py']`.
- Failure: "print the actions, run nothing" records a person's pass. The spec's own live proof says "`--dry-run` first", so with a live word that proof would change the state it is meant to observe.
- Fix: `if self.dry:` print what would pass, return False. Test it.

**F3. MEDIUM, fix before merge; SPEC. The stuck facts put a dispatch id in text a person reads.**
- Where: `stuck_facts` `:2780-2797`, `stuck_text` `:2807`. The fallback shows the lead as the body (`fallback_person` `:5424`), and in B-20 the conductor answered `_unreadable`, so this road is live.
- Control: `human_broken(lead with facts) = ['dispatch_id']`; without facts `= []`.
- `reason:` also passes raw ids through (`S6 awaits the acceptance of qa-failure-analyst`). N3 tests `human_broken`; N5 does not.
- SPEC: the N5 test text prescribes `... stands for S6-qa-runner-5`.
- Fix: person lines by `stage_place` and role name; ids and the raw reason go to `text` (details and conductor). Add the `human_broken` row.

**F4. LOW in effort, blocks the canon. Two of the 5 new lint findings are B-20's.** `test_consumer_close_route.py:13` `json`, `test_stuck_facts.py:19` `harness` (job 28213673, `lint ratchet: ... 5 new`); both still at head. The other three belong to the walker.

**F5. LOW, fix in the round. The finding is lost on the `retry` road.** `person_pass` raises a Refusal whose `retry` repeats only `stage_done` (`:9778`, `py(check=True)`). `guarded` (`:16921`) runs that retry and returns, so the `owe_row` in `consumer_person_pass` is skipped. On the next turn the record stands, `awaits` is `""`, and no finding is ever filed (P13). Traced by reading, not run. Fix: the `record_close` pattern (`:6626`): catch the Refusal in `consumer_person_pass`, set `refusal.retry` to the whole pass, re-raise.

**F6. LOW. `stuck_pending` is not bound to its question.** See answer 5.

**F7. LOW. The refusal literal has no pin against its source.** `story_run.py:16348` vs `controller.py:800`; the test uses its own copy (`test_code_close_behind.py:33`), and its only `code_close_facts` hit is the docstring (line 4). Reword the controller's message and N3 goes silently dead with green tests, returning the B-20 dead end. Fix: one test row asserting `code_close_conflicts` still yields that sentence.

**F8. LOW, quality.** See item 7.

## Answers

**1.** The builder applied `since` only in the new step; the old sites are wrong by FR-4 (F1). The time comes from the last `accept` event, not "the dispatch row" as the spec says. That is correct: `controller.py` has no `accepted_at` (case-sensitive grep, 0 hits; control: `created_at` is what the new test reads through the real controller). Waiver records replace per stage+match (`waiver.py:153-156`), so a newer word replaces an older one. One residue: `split_overridden` takes the first hit in file order, so an old `*` waiver hides a new word from the `since` check. Safe direction, not a finding.

**2.** No. Every production caller passes the pipeline: `controller.py:1827, 4450, 7738, 7847, 8980`, `story_step.py:151`. The negative is controlled by the same grep finding those; `grep -rni` over the package otherwise lists only tests, CHANGELOG and the debt file. All `awaits_acceptance` callers also pass one (`controller.py:5031, 8207`, `stage_guard.py:751`, `story_run.py:2788, 9709, 12757, 12890, 13898, 16355, 16490`). The default `None` stays as a trap for a new caller; only the N1 source pin guards it. F1(b) has no queue row in the reports, so the Lead should write one (below).

**3. Yes, measured rather than replayed mentally.** I ran the real driver on a scratch COPY with `--answer retry`, `run_role` and the conductor stubbed to halt (no paid call). Verbatim:
```
answer for code_close (S7): retry
S7: nothing is passed; the step runs again
[where] {"action": "prepare_stage", "stage": "S6", "revision": 313}
[progress] S7 Triage · ... done S0–S6, S9
[where] {"action": "prepare_stage", "stage": "S7", "revision": 315}
[progress] S8 Results · ... done S0–S7, S9
[where] {"action": "prepare_stage", "stage": "S8", "revision": 317}
[HALT] run_role S8 qa-doc-scribe
S6 done | digest: accepted by the failure analyst
S7 done | digest: accepted by a person's word
{'S5': 'completed', 'S6': 'completed', 'S7': 'completed', 'S8': 'pending', 'S9': 'completed'} rev 317
```
- Correct attribution: S6's record is the analyst's, S7's is the driver's by the person's word. `asked {}`, `code_close {}`, no new question.
- The first run hit my 280 s timeout after S7; the state was consistent and a resume reached S8.
- This is a control, not the FR-33 proof. N2 on a story with no record and N3 case (b) stay unproved live, as the spec says. The "by person" close files no finding here because the S7 record predates the new code.

**4.** Recognition is sound; I found no wrong pass. Facts without the message:
- `running` and `behind` together give both messages, and the branch's `not running` sends it to today's road (defect filed plus "no word passes"). It needs a stale running row; `where` answers `wait_existing_job` first, so it is close to unreachable.
- `stage_done` at step `record` has its own text (`stage_guard.py:760`, `required stages are not done`). That only occurs when the pipeline and controller differ, which `code_close_step` drains first. Today's road, safe.

Message without facts:
- `behind` empty on re-read, or the stage's own `completed`: today's road.
- The same literal at `controller.py:5033` carries no `.close`, so it never reaches `code_close`.

Case (a) traced to the end: a receipt refusal has `retry=None` (`close_receipt` `:6606`), so `guarded` returns to `where` as intended and does not re-close at once. Weakness: F7.

**5.** Producer `:18180` and reader `:16213` are in one commit, and a test reads it. It cannot swallow an answer: `take_answer` only pops and records, the branches have already read the words. It can mis-attribute (F6): `_ask_conductor` saves state before the paid call, so a process dying in the conductor leaves the mark on disk. A later unrelated `refusal` question at the same stage is then recorded under the old signature, and if that signature returns the lead says "You answered <other words>". Fix: at the top of `run`, drop a pending mark when `asked` is empty.

Analogs:
- `refused_text` (`:2820`): fix now. Same blind lead, one call to the helper after F3 makes the lines person-safe.
- S7 and S8 thresholds: queue, not per site. If they need asking once, it should be one mechanism at `no_move`, and it should join `already_answered` (item 6).

**6.**
- AR-29: no judgment moved. The new checks read shape and joins, `go on` is the person's word, the consumer's verdict stays in its form. `judgment: none` is true on all four commits. No census or `blocks_override` edit, no craft marker; `test_judgment_census` PASS on CI.
- AR-17: every new no-move state goes through the seam (`code_close_ask`, stuck, the two `go on` failures after t-2008). CI's A27 rows at ec7e3c536 are only `walk_before` and `walk_after`, so t-2008's `_answer_code_close` fix holds. `no_move(call=False)` always raises, so `passed` at `:16499` is not unbound.
- `consumer_word_step` never asks, by design: it falls through to `where`, and F1 keeps the two reasons consistent.

## Standing questions

- **Fit to the spec:** N1, N3, N4, N5 as written; N2 and F2 partial (F1).
- **Builder's own decisions:** all safe. Keeping `code_close.behind` out of `CODE_CLOSE_OFFERS` is justified (CC15 PASS through `test_no_move_seam`), one `if` before the table, and the key is pinned by the census of question ids.
- **Seams:** additive. Files outside `owns` are each named in the reports (`driver-layers.json`, `question-prices.json`, the stubs).
- **Class-wide:** axis 5 (S6/S7 twins) is covered by the rows of N1 and N2. F1 is the uncovered part of the class. S9 behind S8 is tested (N3.6).
- **Tests:** rows kill the stated edges by reading. Missing: F1 sites, dry run, `human_broken` for stuck, the F7 pin.
- **Hygiene:** `--lang` green per reports; `test_human_questions` PASS.
- **Ratchets (item 9):** no in-tree ratchet row raised; `audit_factory` is not in the commits' stat. The lint baseline was not raised and is red (F4).
- **Architecture:** AR-13, 14, 16, 17, 22, 24, 25, 27, 28, 9 named. Touched and not named on the commit: AR-20 (no raise, so harmless). Producer-reader walk done for `stuck_asked`; `behind_seen` is written in `code_close` and read there.

**6. DUPLICATION AND CONSISTENCY:**
- `stuck_asked` is a second carrier of "the person already answered this", beside `already_answered` (`:3998`, by question hash). The spec prescribed it (SPEC) and the roads differ: N5 feeds the conductor before any question exists. Keep it, queue the convergence.
- The acceptance-time read is new; `_dispatch_starts` (`:10013` usage) reads start, not accept, so it could not be reused. It should still live in one helper (F1).
- The `owe_row add-finding` shape is now the third copy (`:10021`, `:16510`, `:9736`); dup ratchet `0 new`, so queue only.
- `"by: person"` is a literal at both ends (`:9692` reader, `:9780` writer): name one constant, fix in the round.

**7. CODE QUALITY:** no new function over 60 lines; the `code_close` branch nests four levels and stays readable. Fix in the round:
- the comment "The deferred record..." now sits above `STUCK_REPEATS` instead of `CODE_CLOSE_IDLE_CAP` (`:632-634`) and so lies;
- the loop variable `answered: list` (`:16182`) is rebound to a dict at `:16213`; rename the N5 one.

Dead: the `'next role'` defaults at `:16393`, unreachable because `awaits` implies a route; harmless.

## SPEC findings

- S1: the N5 fact text carries a dispatch id (F3).
- S2: N2's DoD demands a census row the census test refuses (t-1990, deviation 1: "stale row"). Drop the requirement; the builder's removal is right.
- S3: N5's `stuck_asked` ignores the existing `already_answered` (item 6).

## CI, pipeline 8042816 on ec7e3c536 (head 20317b442 has no pipeline listed)

Failed: `package-fast`, `forge-check`, `package-full` 1/2 and 2/2.

B-20's files PASS: `test_consumer_close_route`, `test_code_close_behind`, `test_stuck_facts`, `test_story_run_refusals`, `test_no_move_seam`, `test_story_run_s7_live`, `test_s7_investigation_replay`, `test_conductor_doors`, `test_driver_layers`, `test_human_questions`.

**One red touches B-20's pins:** `test_stage_acceptance_consumer.py` dies at line 260, `AttributeError: 'types.SimpleNamespace' object has no attribute 's7_close_places'` (reproduced locally). The call `story_run.py:13212` is from deb1b702d (t-2005, U3a), so the cause is not B-20, but everything after that line in the file, including the M3 pass checks N2/N4 edited, does not run at head. Green it before accepting.

Other reds, by their names and rows, are not B-20's: `test_validator_class`, `test_audit_rules` (walk_*), `test_task_root_parsers`, `test_bug_records`, `test_surfaces`, `test_collect_history_sets`, `test_story_run_s7` (Places line), `test_s7_investigation_driver`, `test_story_step_manual_block`, `test_story_step_materialize`, `test_story_run_s6` (extra finalize; attributed by inference to `walk_after`, not traced), hygiene `.pytest_cache`.

## Lines for «Остатки» (Lead writes)

- `S7/S8 no_move thresholds and stuck_asked converge on already_answered, one mechanism at the seam | перенос: findings/<new> | обоснование: no live case; one mechanism, not per site | подтвердил: —`
- `make pipeline required in _next_action_for_state (spec F1 b, ~20 test sites) | перенос: findings/<new> | обоснование: only the source pin guards a new caller | подтвердил: —`
- `one helper for the three add-finding passes | перенос: findings/<new> | обоснование: dup ratchet quiet; refactor | подтвердил: —`

## Trail

Read: spec t-1988; critic-diff-brief; reports t-1990, t-1993, t-2001, t-2008; `git show` of the five commits (`story_run.py`, `story_step.py`, `no_move.py`, `question-prices.json`). At head: `story_run.py` (consumer block, `person_pass`, `code_close*`, `_answer_code_close`, `stage_S6` head, `stage_S7`, `s7_*`, loop, `take_answer` tail, `no_move`, `fallback_person`, `guarded`, `close_by_code`, `record_close`, `ask` FR-7 block); `acceptance.py:1279-1360`; `controller.py:751-800, 5020-5040, 8022, 8200-8215`; `waiver.py`; `contract.py:152`; `stage_guard.py:739-770`; tests `test_consumer_close_route.py`, `test_code_close_behind.py:1-146`, `test_stuck_facts.py:1-60`. Kept tree read only: `pipeline.json`, `driver-state.json`, `checkpoint.json`, `standing-refusal.json`.

Runs (all on a scratch copy or temp stories):
- replay harness, two runs, output above;
- probe P1-P3, output above;
- `python -B test_stage_acceptance_consumer.py` → `rc=1`, the AttributeError above;
- `ci_read.py jobs/log/artifact` on 8042816.

Not done: slow files, ratchets and mutations (per brief); FR-33 live run (Lead's). N5 mutation list: the report has one negative control and no list; not a blocker for a node this size, noted. `SIBLING_MAP.md`: axis 5 and the headings only.

Needed beyond the manifest: `waiver.py`, `contract.py`, `stage_guard.py`, the CI artifacts.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "F1: consumer_person_pass honours a stage acceptance word of any age at consumer_need_record, consumer_settled and s7_await_scribe (story_run.py:9797, 9872, 12887); only consumer_word_step applies since; FR-4",
    "F4: forge-check red on two B-20 lint findings, test_consumer_close_route.py:13 and test_stuck_facts.py:19"
  ],
  "fixes": [
    "F1 blocks: compute since inside consumer_person_pass for the waiver road, answer stays exempt; test every site",
    "F2 before merge: consumer_word_step dry guard, story_run.py:9699",
    "F3 before merge, SPEC: stuck facts with no dispatch id or raw reason in the person's text, ids go to details; human_broken row",
    "F4 blocks: remove the two unused imports",
    "F5 in the round: consumer_person_pass sets refusal.retry to the whole pass, so the finding is not lost",
    "F6 in the round: drop stuck_pending at run start when no question is asked",
    "F7 in the round: a test row pins the controller sentence that code_close matches",
    "F8 in the round: misplaced comment at story_run.py:632-634; rename the N5 answered variable; one constant for the by: person prefix",
    "refused_text takes the person-safe facts after F3",
    "test_stage_acceptance_consumer.py line 260 red from deb1b702d must be green before acceptance, it holds the M3 pins"
  ],
  "class_completeness": "Axis 5 S6/S7 twins covered by N1 and N2 rows; S9 behind S8 tested. Word-age class not complete: new step only (F1). Stuck analogs: refused_text fix now; S7, S8 thresholds and already_answered convergence go to the queue with lines given for the Lead. All production callers of _next_action_for_state and awaits_acceptance pass the pipeline, grep with positive control.",
  "trail": {
    "read": [
      "docs/tasks/specs/t-1988-acceptance-chain-close.md",
      "docs/tasks/critic-diff-brief.md",
      "docs/tasks/specs/reports/t-1990-b20-n1-n2-report.md",
      "docs/tasks/specs/reports/t-1993-b20-n3-n4-report.md",
      "docs/tasks/specs/reports/t-2001-b20-n5-report.md",
      "docs/tasks/specs/reports/t-2008-canon-red-report.md",
      "wt-fbfix scripts: story_run.py, story_step.py, no_move.py, acceptance.py, controller.py, waiver.py, contract.py, stage_guard.py",
      "wt-fbfix tests: test_consumer_close_route.py, test_code_close_behind.py, test_stuck_facts.py",
      "mybooks-stand/tr-arm-b LOCAL-1 pipeline.json, driver-state.json, checkpoint.json, standing-refusal.json (read only)"
    ],
    "reruns": [
      {"command": "scratch replay harness on a copy of LOCAL-1, answer retry, run_role and conductor stubbed", "result": "where S6, S7, S8; S6 digest accepted by the failure analyst; S7 digest accepted by a person's word; halted at run_role S8 qa-doc-scribe"},
      {"command": "scratch probe P1-P3 over test_consumer_close_route rigs", "result": "P1 step False, old site True; P2 dry run writes the record; P3 human_broken dispatch_id with facts, empty without"},
      {"command": "python -B test_stage_acceptance_consumer.py", "result": "rc=1, AttributeError s7_close_places at line 260, also red on CI"},
      {"command": "ci_read.py jobs, log, artifact on 8042816", "result": "failed; B-20 test files PASS except the file above; lint ratchet 5 new, 2 from B-20"}
    ]
  }
}
```
