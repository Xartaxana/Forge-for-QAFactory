# t-1119 — re-review of the C3 fix round 3 (RD1-27, RD1-31), diff f1265890..748a72d5

Tree: `.claude/worktrees/agent-ac40b44fb0a175afa`, HEAD `748a72d5`. There are three commits: 8f6c860d (A–E), 902e5373 (F) and 748a72d5 (step 3). The spec is my verdict t-1100 plus the Lead's step-3 invariant and D1–D4.

## Verdict

**NEEDS WORK (fit_with_fixes), with no blocker.** Fixes A–F of t-1100 are done as written. The step-3 invariant holds on every path I traced: a row exists iff the event committed, one row per distinct `(stage, item)`, nothing is written outside `apply`, and `_record_noted_passes` is the only caller of the writer. Five fixes remain. The weightiest is F-1: rows are now written AFTER the derived-view refresh, so the dashboard lags one event. This is a regression for the accept-side rows that used to be written before the event. Every fix is "fix before merge" and sits in the node's owns, except where noted. The decision to accept stays with the Lead.

## Findings

**F-1. The rows land after the dashboard refresh (fix before merge). Surface: `apply`'s commit/after-commit order.**
- `apply` (controller.py:5231-5273) records `kept` only after the `with self.store.deferred_after_commit():` block has exited.
- The block's exit runs `_run_after_commit` → `refresh_derived` → `dashboard_refresh.refresh_for_task` → `factory_dashboard.main`. That renders `coverage_contract.coverage_projection`, which reads the pass rows (`_record_word_index` → `waiver.record_word_index` → `person_passes`, coverage_contract.py:565-570, :714). The render's input hash also covers every `*.jsonl` under the story (dashboard_refresh.py:40-48).
- So for an S5 completion whose FV1-30a word passes are noted, the refresh renders `word_passed` WITHOUT them. The view catches up only at the next event's refresh, or never if the story pauses there.
- At f1265890 these accept-side rows (`_record_s5_word_passes`, the probe-gap and review lines, and the rest) were written inside `validate`, so the refresh saw them. Dispatch rows have had the same lag since round 1. My t-1100 accepted that position and missed this, which is my error.
- I traced this by reading; I did not run a probe.
- Fix (controller.py `apply`):
  - Inside the `with` block, right after `receipt = self.store.commit(...)` returns, record and close the collector: `noted, self._passes = self._passes, None; self._record_noted_passes(request.get("id"), noted)`. Then call `_after_commit`.
  - In `except StateConflict`, record only while the collector is still open: `if isinstance(exc, EventCommitted) and self._passes:`. That case is `ProjectionStale` raised inside `commit`. `DerivedViewStale` is raised at block exit, by which point the rows are already written.
  - `finally` restores `outer_passes`. Drop the `if kept:` tail.
- Test: add one more `REG_PRECONDITION_ROWS` row in `test_controller_state.py`. Patch `c.store._run_after_commit` to note whether the pass file holds the row at refresh time, and expect it to.

**F-2. Leftovers and names that lie (fix before merge). Surface: the step-2/step-3 change of road.**
- (a) Unused `passed` locals: `_plan_review_problems` :7096, `_beside_running_refusal` :7310, `_s5_v2_collect` :7418. Use `_`. The locals at ~7107/~7182 that the dispatch asked about are these sites plus :7169. :7169 is still used by the `print`, so it stays.
- (b) Step 2 changed `_code_review_refusal` (:6575-6596) to return `(problems, passed)`. Since step 3 the only caller discards `passed` (:5936 `review, _passed =`). The docstring says "the caller records them once the accept stands", which is now false. Revert it to returning the problem list, and revert its docstring and the caller. Also drop the `_passed` names at :5999 and :6021 (use `_`).
- (c) The `_note_pass` docstring (:2473-2475) says passes are "noted here, by the ONE road every pass goes through (`_passed_by_person`)". In fact six sites call `_note_pass` directly: :2465, :7010, :7093, :7609, :7618, and the hand-built items of D2/D3. Say what is true: `_note_pass` is the one road; `_passed_by_person` is the caller for split words, and the hand-built passes call it directly. Step 3's commit line "AR-13 -- the one note road _passed_by_person" has the same slip. Correct it in the fix commit's `architecture:` line.
- (d) The `gate_template.REGISTRY_BLOCK` comment (:60) says the constant keeps "the refusal, the waiver door and the generator" from drifting apart. The `registry_why` docstring (:66) says "the prefix is matched by `tools/controller-blocks-gen.py`". Both claims are false:
  - the generator matches the local name `registry_blocking[0]`;
  - it carries its own literal `--block \"gate registry unreadable\"` (tools/controller-blocks-gen.py:354).
  - Fix: reword both texts to "the dispatch stop's block; the door text of controller-blocks-gen.py:354 is a copy". Making the generator read the constant would touch tools/, which is outside the owns; the Lead's choice.

**F-3. Axis 29 sibling: the one writer does not use the one appender (fix before merge, in owns).**
- `_record_person_pass` (:2403-2450) appends with `path.open("a")`. It does no torn-tail repair.
- SIBLING_MAP axis 29 names `hooklib.append_jsonl_line` as the appender for every `.jsonl` carrier. It does not list `passed-by-person.jsonl` as adopted, and it is not on the axis's queued list.
- This round makes that function THE writer for every event (AR-14 is claimed). A torn tail would glue the next row onto it, and `person_passes` then skips both lines.
- Fix: write each line through `hooklib.append_jsonl_line(path, json.dumps(line, ensure_ascii=False))`, keeping the `OSError` → stderr branch.

**F-4. Tests: a road with no positive row, and duplicate rows (fix before merge). Surface: the door rows of the collector.**
- (a) The person_words look's hand-built `_note_pass` (:7093) lost its only positive check: `test_s5_grown_windows.py` k4 now asserts only "no row outside apply". A grep for `person_words=True` and the decision text "ordered in the person's own words" across the tests finds no other test of it. So if that `_note_pass` line were dropped, every test would stay green.
  - Fix: in `k4_look_scope`, accept a person_words narrow look through `accept_it(c, root, <id>)` (the apply door the test already drives). Expect one row, stage S5, block `S5 plan before windows: ...`, decision "the look is a rework ordered in the person's own words".
- (b) Under 5(e), these rows assert the same behaviour through the same door and road (`apply` → `validate` → `_passed_by_person` → the one collector):
  - `test_controller_rework_scope.py` (the empty-scope pair) duplicates `test_controller_gate_decision.py` (the design-review pair): same op `decision`, same road.
  - `test_fixes_13797.py` (the S6 row) and `test_controller_release.py` (the code-critic pair) duplicate the S3 pair in `test_controller_state.py`: same op `accept`, same road.
  - `test_s5_kind_readers.py` `round_passes` drives a helper with a hand copy of `apply`'s protocol. It only pins that `_s5_v2_collect` calls `_passed_by_person`, which is wiring (TESTING: an internal boundary gets no test).
  - The `tests-over:` reason ("rows added to existing scenarios") explains where the rows went, not why there are this many. Per-site rows made sense in step 2, when each site recorded on its own. Step 3's one road made them wiring pins.
  - Fix: delete those four blocks, or name in `tests-over:` a reason that holds.
  - Keep: the items-unreadable pair (it is the only one that covers the memo pre-read), the S3 pair, K-R2-2 and (2e).
- (c) Q5, the direct-call rows:
  - `_committed` (test_words_doors) and `problems(commit=True)` (test_probe_gap_word) do kill a dropped `_note_pass` at :2465/:7609/:7618: no note means no row, and the test goes red.
  - A real-apply S5 completion exists in `test_words_doors._s5_completion`, but it costs a full story per row. I accept the two copies of the protocol as written, provided F-1 does not change the note→record contract (it does not).
  - With (b) applied, `_s5_v2_collect` needs no row: its pass goes through `_passed_by_person`.

**F-5. Witness detail (no fix).**
- The builder's grep claim says "def, two docstring mentions, the one call". `grep -rn -i _record_person_pass ai-packages/qa-factory --include=*.py` returns the def (:2403), ONE docstring mention (:2483), the call (:2488) and one test comment (test_s5_precheck.py:4891).
- The load-bearing part, "one call", holds. The count is off by one, probably the :2455 text from before the step-3 rewording.

## Answers to the dispatch's questions

**1. A–F.**
- A: one head, `REGISTRY_BLOCK + ": " + registry_why(...)`.
  - FR-1: it says what is wrong (cannot be read, with the reason), what is expected (the file present and readable) and the door (reinstall or update).
  - FR-6: the person-facing text holds; a factory reason is not put to the person as a choice (FR-3: "nothing is wanted from you").
  - FR-4: the block still opens with `gate registry unreadable`, so the waiver word still matches it.
  - Pins kept: the prefix, "Reinstall or update", "nothing is wanted from you", "Owner: factory". The block is about 200 characters, under the 400 cut.
  - The leftover issue is F-2(d).
- B: fixed, with a row and a byte-copy red proof.
- C: fixed in the one-road shape; the five per-site calls are gone.
- D: names fixed and the label fixed.
- E: row (2e) added.
- F: fixed. The decision collector, the S6 completion, the code receipts and the mechanical round all go through the one collector.

**2. The invariant, path by path (traced):**
- Exception before commit (`stale expected revision`, a validate refusal, `validate_record`): not `EventCommitted`, so `finally` restores and no row is written.
- `ProjectionStale` from `commit`, and `DerivedViewStale` at block exit: recorded once in the except branch. Every later branch of the handler raises, so the `if kept:` tail is never reached and there is no double write.
- `ProjectionStale` on the store's replay branch: validate did not run, so `_passes` is `[]` and nothing is written.
- A non-StateConflict raised by `_after_commit` (outside its caught set) would leave a committed event with no row. This edge existed before; F-1's shape closes it, because the rows are written before `_after_commit`.
- Decision pre-read: it runs before the collector opens (the outer value, None at top level) and returns `self.apply(...)`, which opens its own collector. The `open_gate_items` inside `validate` notes.
- Re-entrant `apply`: the only one is that memo pass. The helpers at :8475-8671 are top-level only (callers: the CLI, :10112-10120). Save and restore is correct anyway.
- Rehearsal and probe roads run with None: `prepare` (:2191/:2200), `build_rework_request` (:3863/:3932), `check_decision` (:3345, CLI :9760), `story_step.py:2347` `validate("dispatch")` on a copy, `record_as_is` (:3453).
- Concurrency: no package module that imports `threading` constructs a `Controller` (I grepped `Controller(` in all 11 such files). The instance-state pattern is the same as `_items_memo`'s.

**3. The widening, site by site.** For every `_passed_by_person` call site I checked whether its result decides a raise. No call site is a look-ahead or advisory read, so every new row is a true "this word lifted a block of this committed event":
- `:3178` `_design_review_problems` (via `_decision_problems` :3310, in validate decision :6045 and `check_decision`): blocking → raise. True.
- `:3267` the empty scope (same road): true.
- `:3405` `open_gate_items` (validate :6048; memo :5101 with None; `record_as_is` and the CLI with None): true.
- `:4296` `_unreadable_plan_problems` (dispatch :5676; `_half_membership_problems` :5609/:5611; rehearsals with None): every result is raised or passed as `extra`. True.
- `:5583`, `:5684`, `:5718`, `:5733`, `:5752` (dispatch): true.
- `:5999` via acceptance `split` (stage = `d.stage`): true.
- `:6021` S6: true.
- `:6581` `_code_review_refusal`: true. A pass is noted even when `review` refuses, but then the accept is refused and no row is written.
- `:6607` `_plan_refusal`: every caller adds its result to `problems`. True.
- `:7096`, `:7169` (noted before the `if review: return review`; review is then raised), `:7310`, `:7418`, `:7708`: true.

Readers that now show more rows:
- `waiver.person_passes` reads S5 rows only. New S5 dispatch-side rows (plan order, `S5 scope: unreadable`, mechanical round/cap, the registry stop at S5) carry no subjects. They map to fact `other` and appear in `report_facts._word_bare_lines` as a person-pass line, collapsed per finding. That matches P13: a pass is written into the findings.
- `run_counters` counts every row. S4 decision rows (dispatch = the decision id) are counted there and read nowhere else. That is right.
- No reader is starved, and none treats a new row as a field pass: an empty `subjects` passes no field.

**4. Deleted direct writes.** Each was checked against the `_passed_by_person` or `_note_pass` call that now notes it:

| site | now noted at | stage | items | id |
|---|---|---|---|---|
| 6000 | acceptance `split` | `d.stage` (str), same | same items | `request.id` = `p.id` = `d.id` (:5862) |
| 6017 | :7418 | S5 | same | same |
| 6042 | :6021 | S6 | same | same |
| 6045 | :6581 | `stage or S5` | same | same |
| 7113 | :7096 | S5 | same | same |
| 7195 | :7169 | S5 | same | same |
| 7326 | :7310 | stage | same | same |
| 7737 | :7708 | S3 | same | same |

No text or stage changed. There is a timing difference only, which is F-1.

**5. Tests:** see F-4. The pairs (refused later → 0 rows, committed → 1 row) pin the invariant through `apply`. Two red proofs were attached; the remaining rows can fail by construction.

**6. Standing questions.**
- Duplication and consistency: one appender missing (F-3) and one generator literal (F-2(d)). Grepped:
  - `REGISTRY_BLOCK`, `gate registry unreadable`, `gate-registry.json cannot be read` over the package, tools and kb. The other hits are the A26 linter family (`gate_registry.py:797/979`) and its tests, a different family: not applicable.
  - the writers of `passed-by-person`: controller only.
  - leftovers `_note_dispatch_pass|_dispatch_passes|_s5_round_passed|WHY_RUN_REGISTRY\b|stop=True`: none in code. Positive control of the same shape: `WHY_RUN_REGISTRY_TAIL` found 3 hits.
- Code quality: F-2. No new function over 60 lines and no nesting over three levels in the new code.
- Axis 5 Lead line: still true after A. The one stop is the dispatch branch of `validate` via `registry_problem()` (:5580-5589); the per-site texts take `registry_why`.
- Ratchets: none touched; the diff's file list has no ratchet file. The clone ratchet is the batch canon's to read, and I have not read it.
- AR-14: kept (one writer, one caller). With F-3 it uses the one appender.
- AR-25: kept (no row for a refused event, a row for a committed one).
- AR-13: kept in substance, but the wording is wrong (F-2(c)).
- Judgment: `none` holds.
- One road: closed. The six hand-built notes are separate judgments with no `split_overridden` reading: `person_words`, the window record's probe-gap words, review words, `s5_precheck.word_passes`. They are not a second road for one action.
- Tests budget: F-4(b).

**The red in `test_controller_stage_acceptance.py`:**
- It is owned by **stage-critics node A1b (t-680, commit 34fabeaa)**. That node deleted `acceptance.author_exit_owes_plan` and its `_s3_completion_gate` branch (spec `docs/tasks/specs/20261113-stage-critics-s2-s3-removed-spec.md` :72, :312) but left the test's line 279 and the "S3 author's exit ... with an acceptor: refused" row.
- The file is quarantined (a `test-layers.json` cohort row). Its repair is a `defect_found` against t-680, done as a `quarantine-edit:` or deletion under TESTING. It is not part of RD1-31.

## Trail

- Read:
  - t-1100;
  - `critic-diff-brief.md`;
  - `git diff f1265890 748a72d5` (whole) and the three commit messages;
  - `controller.py`: 2395-2505, 3380-3470, 4284-4320, 5095-5290, 5550-5618, 5668-5684, 5855-6040, 6575-6640, 7058-7102, 7127-7186, 7296-7340, 7389-7432, 7511-7625, `_after_commit`, `refresh_derived`;
  - the controller.py of 902e5373 (the deleted sites);
  - `event_store.py` 530-575, 632-760;
  - `acceptance.py` 1525-1565;
  - `waiver.py` 791-798, 915-1040;
  - `report_facts.py` 3335-3365; `check_delivery.py` 1625-1650; `coverage_contract.py` 565, 700-720; `dashboard_refresh.py` 40-90; `factory_dashboard.py` 1108-1120;
  - `SIBLING_MAP.md` axes 5 and 29;
  - the stage-critics spec (grep);
  - `test-layers.json` :7759.
- Re-runs: listed in the block below. My control run of `test_controller_gate_decision.py` gives 336/336 and matches the builder.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "class_completeness": "A-F of t-1100 fixed; the invariant holds on every traced path (pre-commit refusals, ProjectionStale/DerivedViewStale, replay, the decision memo pre-read, the rehearsal roads with None, no multi-thread Controller). All 21 _passed_by_person call sites decide a raise, so every new row is true. The 8 deleted direct writes are noted upstream with the same stage, items and id. Open: the recording position after the derived refresh (F-1); axis 29 sibling: _record_person_pass is not on hooklib.append_jsonl_line and not queued (F-3); the person_words look note has no positive door row (F-4a). The stage-acceptance red is owned by stage-critics A1b t-680 (34fabeaa), a quarantined file.",
  "fixes": [
    "F-1 controller.py apply: record the noted passes inside the deferred_after_commit block right after store.commit returns (close the collector), record in the EventCommitted branch only while the collector is still open, drop the post-finally tail; add a REG_PRECONDITION_ROWS row asserting the after-commit refresh sees the pass row",
    "F-2a controller.py: unused passed locals in _plan_review_problems :7096, _beside_running_refusal :7310, _s5_v2_collect :7418 become _",
    "F-2b controller.py _code_review_refusal: revert to returning the problem list (its docstring claims the caller records passed; the caller discards it), adjust the caller :5936 and the _passed names at :5999/:6021",
    "F-2c controller.py _note_pass docstring: _note_pass is the one road; _passed_by_person and the hand-built sites call it; correct the AR-13 line in the fix commit",
    "F-2d gate_template.py REGISTRY_BLOCK comment and the registry_why docstring: the generator matches registry_blocking[0] and holds its own literal at tools/controller-blocks-gen.py:354; reword (making the generator read the constant is outside the owns, the Lead's choice)",
    "F-3 controller.py _record_person_pass: write each line through hooklib.append_jsonl_line (axis 29), keep the OSError stderr branch",
    "F-4a test_s5_grown_windows.py k4_look_scope: accept a person_words narrow look through accept_it and expect one S5 row with the person's-own-words decision",
    "F-4b delete the duplicate door rows (test_controller_rework_scope empty-scope pair, test_fixes_13797 S6 row, test_controller_release code-critic pair, test_s5_kind_readers round_passes) or name a reason in tests-over that holds"
  ],
  "trail": {
    "read": [
      "docs/tasks/specs/reviews/t-1100-c3-fix-round2-code.md",
      "docs/tasks/critic-diff-brief.md",
      "git diff f1265890 748a72d5 and git log of 8f6c860d, 902e5373, 748a72d5",
      "scripts/controller.py at 748a72d5 (ranges in Trail) and at 902e5373 (the deleted sites)",
      "scripts/event_store.py 530-575, 632-760; scripts/acceptance.py 1525-1565; scripts/waiver.py 791-798, 915-1040",
      "scripts/report_facts.py 3335-3365; check_delivery.py 1625-1650; coverage_contract.py 565, 700-720; dashboard_refresh.py 40-90; factory_dashboard.py 1108-1120",
      "docs/SIBLING_MAP.md axes 5 and 29; docs/tasks/specs/20261113-stage-critics-s2-s3-removed-spec.md (grep); scripts/tests/test-layers.json 7759",
      "tools/controller-blocks-gen.py:354"
    ],
    "reruns": [
      {"command": "( cd <tree>/ai-packages/qa-factory && python -B scripts/tests/test_controller_gate_decision.py )", "result": "=== test_controller_gate_decision: 336/336 ok === (matches the builder)"},
      {"command": "( cd <tree>/ai-packages/qa-factory && python -B scripts/tests/test_controller_stage_acceptance.py )", "result": "FAIL S3 author's exit ... with an acceptor: refused; AttributeError: module 'acceptance' has no attribute 'author_exit_owes_plan' (line 279)"},
      {"command": "git log --oneline -S author_exit_owes_plan -- ai-packages/qa-factory", "result": "34fabeaa stage-critics node A1b, t-680; 9ac00f09 Initial import"},
      {"command": "grep -rn -i _record_person_pass ai-packages/qa-factory --include=*.py", "result": "def :2403, docstring :2483, the one call :2488, test comment test_s5_precheck.py:4891"}
    ]
  }
}
```
