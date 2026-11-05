NOTE ON DELIVERY: the hook (`tools/handoff_gate.py`) refused the Write to `docs/tasks/specs/reports/t-008-gm3-2-critic.md`. A critic may write only inside `docs/tasks/specs/reviews`. Its door is to put the whole report in this message, so the full verdict is below. Extract it with `tools/handback_extract.py`, or move the handoff path into `docs/tasks/specs/reviews`.

# t-008 GM3-2: critic gate on the combined diff (d123544..26ba10c)

I reviewed against:
- the spec `docs/tasks/specs/reports/t-002-gm3-1-red-package-tests.md` (C1-C8);
- the standing brief `docs/tasks/critic-diff-brief.md` (items 1-11);
- the Lead's fork decisions in the dispatch (C3, C6/C7, C1).

The diff file is byte-for-byte equal to `git diff d123544..26ba10c -- ai-packages` (`diff` exit 0; 29 files, +191/-52).

## Verdict

**ACCEPT WITH FIXES.** No finding blocks the merge on its own. Three fixes are owed before release (F1-F3); the rest are queue lines. Separately, one product-code defect turned up next to the pins (F4: the S6 recovery road differs from the live road). The diff does not cause it, but it disproves the spec's "no class C" claim, and it needs a node.

## Findings

**F1 (fix before release; AR-20): the manual-brief ratchet was loosened by a change of measure, and nothing names the loosening.**
- `scripts/tests/test_brief_pack_manual.py:63-67` still describes `MANUAL_BUDGET_BYTES = 6794` as "dense (measured, 0 slack)".
- Under `measured_bytes` the same fixture now weighs **6703**. My control probe printed `bytes 7354 budget_bytes 6703`. The plugin root appears twice, each occurrence 55 B longer than the 8-char token, so 110 B leave the measure.
- On the raw measure the spec recorded 6813 (19 B over). C6 went green only because the measure changed: no brief text was cut, and the pin now has 91 B of silent slack.
- Commit `c1c46c8` says "no ratchet raised (K1 passes as is)" and commit `c421363` says "no cap raised". Both are true of the number, not of the bound.
- Fix: re-pin to 6703. The measure is now path-independent, so the pin can be dense again. Add the history line `6794 (t-1812, raw) -> 6703 (GM3, plugin root as a token)`. The alternative is to keep 6794 and name the loosening in a verdict, as AR-20 requires.
- Only the manual pin is a dense ratchet. The other brief checks compare against `BRIEF_MAX_BYTES`, which is a ceiling, not a ratchet.

**F2 (fix before release; CODE QUALITY: dead writes and a wrong comment): `test_story_run_s6.py:523-526` and `:685`.**
- `F.runner(..., True)` already writes the consumer's record for its own dispatch (`test_fixes_13797.py:253-255`, the C1a change).
- So the two explicit `F.BASE.record_stage_acceptance(...)` calls just before it are duplicate writes that nothing reads.
- The comment at `:525` ("the record is for this one dispatch; the later closing calls below stand on it too") is wrong. Each later `runner(..., True)` writes its own record, and the `code_only` close reads none.
- Fix: delete both calls and that sentence, or replace them with one comment saying the helper writes the record.

**F3 (fix before release; tests: stale mutation docstring): `test_story_run_s6.py:2306-2309`.**
- The K3 docstring still says "launched with `complete=False` when stale live checks are owed" and "MUTATION `complete=True with stale probes` -> the complete check".
- The re-expressed pin at `:2322` now expects the awaits word whether or not proofs are owed. That follows `story_run.py:11255`, whose consumer branch sends `s6_awaits(True)` and ignores `owed`.
- Under the shipped table, this check can no longer kill the named mutation.
- The `not owed` term of the no-consumer branch (right side of `:11255`) is now pinned nowhere in this file, because the file runs only the shipped table.
- Fix: rewrite the docstring for the consumer world and drop or re-aim the mutation line. Pinning the no-consumer branch is a queue line; that branch is reachable only with a table that gives S6 no `acceptance_by`.

**F4 (queue, new node; product code outside the diff; class C): the S6 recovery road disagrees with the live road on a refused case, and the result is a dead end.**
- Live road, `run_manual_block` (`story_run.py:11976-11979`): with a consumer, the last block gets `s6_awaits(True)` whatever was refused or held. Its comment says a refused case is closed later by `manual_close`.
- Recovery road, `completion_for` (`story_run.py:15214-15216`): `s6_awaits(not plan["blocks"] and not plan["refused"])` returns plain `False` when a case was refused. The comment at `:15215` nevertheless says "(as the live `run_manual_block` does)".
- Trace when a saved last-block result is finished through `wait_existing_job` with a refused case:
  1. The runner is accepted without the awaits word.
  2. `acceptance.awaits_acceptance` (`acceptance.py:1252-1276`) therefore returns "".
  3. `controller.py:4969-4971` refuses the analyst's S7 dispatch ("required prior logical stage incomplete").
  4. The next `stage_S6` entry runs `run_manual_block`, finds no block, calls `manual_close`, and `s6_need_record` (`:9292-9301`) raises a Refusal.
  5. That Refusal's door ("the consumer judges ...") names a role that step 3 will not dispatch (FR-2 / AR-25). Only the person's-word door is left.
- The diff's own pins match the code on both roads: `test_story_run_s6.py:688-689` keeps `False` for the refused case, and `:683-686` converts the no-refusal case to the awaits word. They do not paint anything green, but they freeze the divergence in place.
- I established this by reading, not by running it: the scenario needs the real controller, and the story_run test files belong to the CI canon.
- Queue: a node that makes the recovery rule `s6_awaits(not plan["blocks"])`, the same as the live rule, plus a pin for the refused recovery case.

**F5 (queue; DUPLICATION): three new spellings of one normaliser, and a near-copy of an existing record writer.**
- (a) Three new copies of one normaliser:
  - `seen` at `test_story_run_s6.py:57-59`;
  - `s6_rule` at `test_s7_rejudge.py:330-331`;
  - the inline `getattr(e["complete"], "unresolved", ...)` at `test_story_run_deferred.py:110`.
  - The same idiom already exists at `test_stage_critic_route.py:158,303`, `test_stage_acceptance_consumer.py:170` and `test_story_run_s7.py:934`.
- (b) `consumer_accepts` (`test_story_run_s6.py:343-355`) re-implements `record_stage_acceptance` (`test_controller_state.py:32-45`): same record shape, same file write. Its only addition is resolving the author id.
  - It should be the two-line call `record_stage_acceptance(task_root, "S6", acceptance.stage_author_dispatch({"dispatches": dispatches}, acceptance.stage_def_of("S6")))`.
  - The shared home for both helpers should be `story_run_common.py`: the awaits normaliser, and an `accept_record(root, stage, dispatch)` that `test_controller_state` re-exports.
  - This is a queue line, not a must-fix: these are test fixtures, and in every scenario that uses them the real reader (`acceptance.stage_acceptance_errors`) checks the record shape.
- (c) `s4_critic_form` (`test_story_run_refusals.py:3411-3420`) is used twice, both in one file.
  - Its stub of `stage_acceptance_write` is legitimate. `s4_critic_completion` (`story_run.py:9500-9530`) returns on the digest verdict, never on the written record, so the stub removes nothing the S4 keys claim to prove.
  - The writer has its own pins in `test_controller_stage_acceptance.py` and `test_stage_acceptance_consumer.py:148-170` (the three close sites).

**F6 (queue; tests: labels that claim more than they check).**
- `test_story_run_refusals.py:3451` says "written first, once per finish" but compares `set(written)`. A duplicate write per finish, or a wrong order, would pass unseen. Fix: compare the list length with the number of `rule(...)` calls, or drop "once per finish".
- `test_brief_pack_s5_plan.py:742` (K11) checks `long_ in body(long_)`. The test built that string itself, so the check cannot fail; and since Python strings are immutable, `measured_bytes` cannot rewrite its argument anyway. The real claim (the BRIEF keeps the real paths) needs a check that a built brief's `markdown` contains `brief_pack.SCRIPTS`.

**F7 (queue; data row): `fixtures/driver-layers.json:613`.**
- `Driver.ticket_rerun_critic` is filed in row 76, the S7 group next to `s7_close`.
- The method is the S2/S3 stage-critic restart route: `story_run.py:14781-14797` returns early when `stage not in ("S2","S3")`.
- Its neighbours by meaning, `stage_acceptor` and `stage_critic_route`, sit in row 67 (`driver-layers.json:471,475`).
- The home (`driver_stages`) is right, and the L1 check does not read rows. Fix: row 67.
- The other seven rows are plausible:
  - s6_* in row 74, with `s6_reentry` and `s6_reprobed_close`;
  - s7_consumer_* in row 76, with the S7 closers;
  - `_wait_then_critic` in `driver_machine` row 85, next to `_act_wait_existing_job`, which it calls.

**F8 (queue; class completeness of C5): `test_contract_slices.py:446-458`.**
- The expected set now holds seven roles, but the per-role anchor loop (`:455 for role in roles`) still checks only the original four.
- The three new key pages (bug reporter, doc scribe, retro analyst) are counted, but their `## Outputs`, `## Witness` and `## Handoff form` anchors and generated header are not checked.
- The spec marked this optional. A sibling that is neither fixed nor queued counts as a finding, so it needs a queue line.

**F9 (note; error direction of `measured_bytes`, an accepted design):**
- The budget now under-counts the real brief by `(len(root) - 8) x occurrences`: 110 B on this path, more on a deep plugin-cache path.
- The guards on real bytes stay raw and correct: `SLICE_BYTES` (`brief_pack.py:3469-3480`) and `CODE_FILE_BYTES` (`:2142-2146`). So a long path can push the real brief over 6 KB without an `over_ceiling` line, but never past the whole-read limit.
- Two places print the measured number with a plain "B":
  - `brief_pack.py:3139`, "head over cap: N B";
  - `:3532`, "... B against the ceiling", which now prints on every brief.
- `role_load._brief_ceiling` (`role_load.py:450-460`) counts the brief layer as the ceiling allowance, so for a long-path brief it under-counts by the same amount.
- Queue: label these figures "budget B", or accept them as they are by the Lead's word.

## Answers to the dispatch's five questions

**1. Re-expressed pins.** Each pin follows the code line that produces its value:
- S6 K3, K4 and K5, D1(i)-(iii) and "manual half absent" -> `story_run.py:11255`, the consumer branch `s6_awaits(True) if not manual_scope else False`.
- K2 entry 2, the 5/6/11 flags, K-RES and K19 -> `:11979`: the last block gets `s6_awaits(True)` whatever was refused or held, and an earlier block gets `False`.
- The recovery last block and the recovery automation runner -> `:15216-15217`.
- Deferred K-D1 -> `:11979`, where `waiting` is ignored under a consumer.
- s7_rejudge Q9c -> `:15216`, with `manual_plan` stubbed to no blocks and no refusals. The re-judge `False` (`:15199-15204`) stays distinct from the awaits word, so the test still tells the two rules apart.

None of these is a break painted green: each follows the shipped code, and the awaits word still means "not closing".
- The K-D1 pin loses the held-versus-not-held distinction because the code itself dropped it under a consumer. The cover moved to `manual_close` plus the controller's derived-scope gate. The scenario's next key ("S6 closes over the rest with the code-only receipt") still proves the held case stays outside the cover.
- The real gaps are F4 (live versus recovery) and F3 (a mutation label).

Refusals:
- The last-round pins set the no-acceptor world explicitly and label it (`stage_acceptor = lambda s: ""`, the old `None` kept). The acceptor world goes to the seam stub.
- The code really routes there (`:9518-9524`) both for counted == cap and for a cap or count that is not a number (`last_round` at `:9496`).
- The `"id"` added to the recovery record follows `:15251` (`dispatch_id=str(record.get("id"))`, t-1815 F1).

Other helpers:
- C1a writes the record only when `complete` is true, and for that dispatch. This matches `stage_acceptance_refusal` (`acceptance.py:1314+`), where `stage_author_dispatch(state, def, d)` returns `d.id` for the author.
- In controller_state late-s6, `reviewed_dispatch=""` is correct: the dispatch's role is `qa-worker`, not the author `qa-runner`, so the gate computes the author as "".

**2. Nothing weakened or deleted silently.** Every changed pin keeps its key and has a reason comment.
- My grep found these files closing S6 with `stage_complete: True` and writing no record of their own: `test_resume_packet`, `test_story_closed`, `test_story_run_gate_repair`, `test_refusal_ready_commands`, `test_window_record`, `test_words_doors`.
- All of them except `test_words_doors` are absent from the spec's 16-file red list, so CI had them green; I did not re-run them here.
- `test_words_doors` goes through `FIX.runner`, so C1a covers it. It is not proved locally; CI judges it.
- Gap: in the K3 re-entry of `test_story_run_s6` (`ACCEPTED_S6`, `:2050`), the dispatch records have no `role`. So `stage_author_dispatch` returns "", and `s6_need_record` is switched off without being tested.
  - The new comment at `:2319-2320` says the close comes "after the consumer's record", but the scenario writes no record.
  - The X7-6 close-site gate is proved elsewhere, by `test_stage_acceptance_consumer.py:148-170`.
  - Queue: add `"role": "qa-runner"` plus a record there, or reword the comment.

**3. Duplication.** See F5. It is a queue line, not a must-fix.

**4. Registry rows, tree line and slices.**
- driver-layers rows: see F7 (one row number).
- The `artifact-contract.md` tree line and the seven regenerated slices carry the same 64-byte LF line, and each slice index grew by exactly 64 B (for example 3,847 -> 3,911).
- The source and the slices are `eol=lf` (checked with `git ls-files --eol`).
- The producer, `retro_numbers.py:2828-2829`, writes exactly those three names under `work/`.
- The seven roles in `test_contract_slices` match `keys_targets`; see F8 for the anchors.

**5. brief_pack.py.**
- The door (`brief_pack.py:3450-3451`) matches only the rubric line, which carries «On the plan» (`:1686-1687`). With no rubric there is no line and so no door.
- The helper's edges:
  - an empty or None root is skipped;
  - the longest root is replaced first;
  - both separators are replaced, and a trailing separator is stripped;
  - a bare `/` becomes empty and is skipped.
  K11 pins all of these.
- Mis-replacement: the brief spells paths from `HERE.parent.as_posix()` and `SCRIPTS = HERE.as_posix()` (`:70, 887, 2997, 3310`), the same source as the default root, so the normal case cannot mis-replace. A root that is a prefix of an unrelated path (`.../qa-factory-old`) would shorten only the measure, which is harmless.
- Every comparison of a brief against its own ceiling now uses the measure: `budget_of` (`:3424`, trim loops at `:3433-3460`), `form_cost` (`:3417`), and `head_bytes` for the SD head cap (`:3132-3139`, `:3467`).
- Raw comparisons that remain, all acceptable:
  - `request_lines` `<= BRIEF_MAX_BYTES // 2` (`:2901`) is equivalent: those lines carry task-relative and project paths, never the plugin root.
  - `SHARED_SECTION_BYTES` (`:2096-2105`) contains no plugin path.
  - `SLICE_BYTES` and `CODE_FILE_BYTES` are rightly raw, because the guard reads real bytes.
  - `:1664` is the read cap of the plan file, not a brief size.
- Architecture: AR-4 kept; AR-10 kept by the door; AR-20 see F1; AR-29 untouched — the code measures bytes and keeps a pointer, and no census row, scan constant or `craft` marker was touched.
- The three wording cuts (`:1631`, `:1669`, `:1675`) keep the meaning:
  - "do not re-report what `s5_plan.py --check` already found" means the same as before;
  - the re-look line loses "so no id repeats", but the instruction (number after PR-{last}) is unchanged.

## Standing questions

1. **Fit to spec:** C1a, C1a', C1b, C1c and C2-C8 are implemented as written and as the Lead decided the forks. C6/C7 take the Lead's decision over the spec's recommendation (a raise); that decision is reviewed in F1 and F9.
2. **Builder decisions:** all lean the safe way, except that the measure change opened slack (F1).
3. **Seams:** `controller.py` changes only a comment, which is now accurate (S6 included, order stated). The `brief_pack.py` changes are additive.
4. **Class completeness:** see F4, F8 and the K3 re-entry note in answer 2. The SIBLING_MAP axes touched:
   - live versus recovery road: F4, not covered, queue;
   - producer versus doc tree: covered by C4, with the siblings `retro-numbers.md` and `estimate-facts.json`;
   - in-tree ratchets: F1.
5. **Tests:** F3, F6.
6. **DUPLICATION AND CONSISTENCY:** F5. Searches run over `scripts/tests`:
   - `setdefault("acceptance"` found 3 files: test_controller_state, test_stage_critic_route, test_story_run_s6;
   - `"unresolved", ` found the getattr idiom in 7 files;
   - `def seen|def consumer_accepts|def s6_rule` found the new helpers.
   Positive control: each search found the writer I already knew about.
7. **CODE QUALITY:** F2 (dead writes and a wrong comment) and F6 (an over-claiming label and a check that cannot fail). No new function is over 60 lines or nested deeper than 3 levels; `measured_bytes` is 7 lines.
8. **Hygiene:** no Cyrillic in the diff. `grep -P '[\x{0400}-\x{04FF}]'` on the diff printed 0 lines; the same pattern on a control file holding `а` counted 1. Line endings are LF, and the changelog fragment is English.
9. **In-tree ratchets:** no ratchet number was raised. F1 is a loosening by measure, and nothing names it.
10. **ARCHITECTURE:** `c421363` names AR-4, AR-10 and AR-20; `fbd1ed4` names AR-22. The test commits say `architecture: none`, which is acceptable for test-only edits. F4 touches AR-25 and AR-19 (stage twins) in product code that no commit names.
11. **JUDGMENT:** nothing moved into code; no census row, `blocks_override` or scan constant was edited.

## Spot-checks of the submitter's claims

- "The diff equals the range": `diff <(git diff d123544..26ba10c -- ai-packages) gm3-2-combined.diff` exited 0.
- "The ceilings were not raised": true of the numbers, but the bound loosened (F1). A scratch probe wrapped `test_brief_pack_manual.brief` and called `k1_the_joint(real_requests())`. It printed `PROBE bytes 7354 budget_bytes 6703 measured 7244 root C:/.../ai-packages/qa-factory occurrences 2` and `PASS K1 the brief is within the ceiling`.
- "test_brief_pack_manual 101/101": my re-run printed `=== test_brief_pack_manual: 101/101 ok ===`.
- "test_brief_pack_s5_plan 188/188": my re-run printed `PASS K11: a backslash spelling of the root is replaced too` and `=== test_brief_pack_s5_plan: 188/188 ok ===`, with 188 PASS lines and 0 FAIL lines.
- The spec's "no class C": not reproduced. See F4.

## Trail

Read:
- the diff (790 lines), spec t-002, and critic-diff-brief.md;
- `story_run.py` lines 9255-9310, 9363-9545, 11170-11200, 11240-11262, 11960-11990, 12062-12090, 14775-14797, 15190-15225;
- `acceptance.py` 1225-1350; `controller.py` 4958-4975;
- `brief_pack.py` 60-80, 2085-2110, 2875-2905, 3455-3485, plus a grep of every byte comparison;
- `role_load.py` 450-460;
- tests: `test_controller_state.py` 25-90 and 1950-1990; `test_fixes_13797.py` 244-262; `test_story_run_s6.py` 515-545, 2080-2100, 2300-2400; `test_stage_acceptance_consumer.py` (grep); `test_brief_pack_manual.py` 150-186 and 515-532;
- `driver-layers.json` (grep); `artifact-contract.md` 18-30; `retro_numbers.py` (grep);
- the commit messages of the range, and `tools/critic_verdict.schema.json`.

Commands:
- `git -C <clone> log`, `diff` and `ls-files --eol`;
- `python -B scripts/tests/test_brief_pack_manual.py` -> 101/101 ok;
- the scratch probe above;
- `python -B scripts/tests/test_brief_pack_s5_plan.py` -> 188/188 ok. It took several minutes on this machine, not the 67 s the spec recorded.

Needed beyond the manifest: `story_run.py`, `acceptance.py`, `controller.py`, `role_load.py`, the test files listed above, and `driver-layers.json`.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "class_completeness": "The live and recovery roads of the S6 runner finish disagree: completion_for answers False on a refused case where run_manual_block answers the awaits word (story_run.py 15216 vs 11979). That is a dead end for the consumer dispatch; queue a node (F4). Producer vs doc tree is covered with its siblings (C4). The key-page anchors of the three new roles are not checked (F8, queue). The K3 re-entry fixture has role-less dispatches, so the X7-6 close gate is never exercised there (queue).",
  "fixes": [
    "F1 test_brief_pack_manual.py:63-67: re-pin MANUAL_BUDGET_BYTES to the path-independent 6703, or name the 91 B loosening in a verdict (AR-20)",
    "F2 test_story_run_s6.py:523-526 and :685: delete the duplicate record_stage_acceptance calls before F.runner(..., True) and the wrong comment",
    "F3 test_story_run_s6.py:2306-2309: rewrite the K3 docstring and its mutation line for the consumer world",
    "Queue: F4 a node for the S6 recovery rule; F5 one shared awaits normaliser and one record writer in story_run_common.py; F6 the labels at refusals:3451 and K11:742; F7 driver-layers.json:613 to row 67; F8 contract_slices anchors for the three new key pages; F9 labels of the measured-bytes figures"
  ],
  "trail": {
    "read": [
      "gm3-2-combined.diff",
      "docs/tasks/specs/reports/t-002-gm3-1-red-package-tests.md",
      "docs/tasks/critic-diff-brief.md",
      "ai-packages/qa-factory/scripts/story_run.py",
      "ai-packages/qa-factory/scripts/acceptance.py",
      "ai-packages/qa-factory/scripts/controller.py",
      "ai-packages/qa-factory/scripts/brief_pack.py",
      "ai-packages/qa-factory/scripts/role_load.py",
      "ai-packages/qa-factory/scripts/tests/test_controller_state.py",
      "ai-packages/qa-factory/scripts/tests/test_fixes_13797.py",
      "ai-packages/qa-factory/scripts/tests/test_story_run_s6.py",
      "ai-packages/qa-factory/scripts/tests/test_brief_pack_manual.py",
      "ai-packages/qa-factory/scripts/tests/fixtures/driver-layers.json",
      "ai-packages/qa-factory/references/artifact-contract.md"
    ],
    "reruns": [
      {"command": "python -B scripts/tests/test_brief_pack_manual.py", "result": "=== test_brief_pack_manual: 101/101 ok ==="},
      {"command": "scratch probe: k1_the_joint with brief() wrapped", "result": "PROBE bytes 7354 budget_bytes 6703 measured 7244 occurrences 2; PASS K1 the brief is within the ceiling"},
      {"command": "python -B scripts/tests/test_brief_pack_s5_plan.py", "result": "=== test_brief_pack_s5_plan: 188/188 ok === (188 PASS, 0 FAIL)"}
    ]
  }
}
```
