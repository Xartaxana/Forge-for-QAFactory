# FV1-30b topic fix round - report

Branch `wip/fv130b-topic`, worktree `C:\QAFactory\forge-repo\.claude\worktrees\fv130b-fix`, base f1ecdb0. Pushed.

- Commit 1 (F3 survivors first): `04d8b07`
- Commit 2 (everything else): `87799fb`

## What was done (per finding)

- F3 (commit 1, then commit 2): `s5_precheck.live_word_index(task_root, scope=None, dispatch_id=None)` beside `word_passes`, and
  `waiver.record_word_index(task_root)` beside `person_passes`; both never raise, None = names nobody (an empty read is an empty index).
  8 sites migrated: `controller._s5_word_index`, `window_record.build.live_index`, `branch_accounting._word_pass_rows`,
  `check_traceability._word_index`, `check_delivery._record_word_index`, `check_delivery._word_passed_then_words` (now through the new
  `_word_passed_ts`), `coverage_contract._record_word_index`, `traceability.Story.word_index`. `Controller._s5_word_index` memoises per
  completion call: `_s5_completion_problems` is now a thin wrapper (sets `_s5_word_memo = {}`, calls `Controller._s5_completion_tiers`,
  drops the memo in `finally`); the memo key is (dispatch id, scope). TEMPORAL: memo lives for one call; a stub without the attribute
  (test_probe_gap_door, test_probe_not_proved call the method unbound) reads `getattr(self, "_s5_word_memo", None)` -> no memo.
- F1: `_s5_v2_collect` asks the index when `refs_bad or ref_kinds or no_fp`. The unnamed instance reaches the same refusals in the same order
  (version test first, shape, fingerprint, `ref_kinds` -> StateConflict text, ids, hash). `window_record.build` writes the entry for EVERY
  passed field (the live index names a field only while its finding stands) and keeps the empty keys only where the item's key is empty.
  The index is now asked in `build` for every item, not only when a field is empty (cost: `live_word_index` returns at once with no live
  S5 word; the per-call cache is unchanged).
- F2: `coverage_contract._refs_word_text` matches the manifest row by `waiver.same_instance(iid, C.test_instance_id(t))`;
  `waiver._same_instance` made public as `same_instance` (grep: no other importer, no alias kept).
- F4: `check_delivery.traceability_records` appends `_word_passed_mention(...)` = "; Then <n> of <case>: passed by your word at S5 (<ts>)"
  AFTER the 120-char cut, for every `word_passed:then_unbound` gap of a `no` row; no ts -> no parenthesis.
- F5: DEVIATION, see below: `_finding_tag` stays local; docstrings corrected (waiver splitter, `_finding_tag`).
- F6: `window_record._word_kept_keys(identity, empty_fields, index, table)` (3 nesting levels), the table read once per `build`
  (`row_table()` cache), no `input_hash` literal (the row says `pass: false`, so `passed_fields` never lists it), `window_keys` VALUES used
  (the dict stays as shipped; `kept[key] = table value`, applied with `copy.deepcopy`); `references/word-passed-facts.json` NOT touched.
- F7: window-instance key `passed_by_word` -> `word_passed` (list) at both producers in `build`. The bool `passed_by_word` on
  `expectation_changes[]` is untouched.
- F9: `references/word-passed-facts.json` added to `covers` of `test_words_doors.py` and `test_window_record.py` in `test-layers.json`.
- F10: the two shipped-value checks dropped from `row_fv130b_n1_the_not_run_section_and_the_field_rows` (docstring trimmed).

## Rows (each under an id naming the input)

- F1: `test_controller_state.py` `fv1_30b_the_finish_reads_the_persons_word`: "(F1) a {stale|unknown} ref with a fingerprint + a refs word naming
  it: no plan text, the unnamed one still refused"; "(F1) the same ... ref, the word naming another instance: today's plan text"; "(F1) a ...
  ref let go still owes the fingerprint"; accepted end to end: "(F1) a stale ref with a fingerprint + a refs word naming it, no pair: accepted".
  `test_window_record.py` `fv1_30b_the_window_carries_the_word_it_was_given`: "(F1) a word for refs the row HAS ... the entry is written" and
  "(F1) every passed field is listed, though only the empty one keeps a key". The `not_run` instance rows are the unchanged old rows.
- F2: `test_obligation_join.py` `fv1_30b_n2_refs_words`: "F2: TC-1::test_x has bad refs, TC-2::test_x good ones (TC-1 listed first: True/False)",
  "F2: TC-1::test_x repaired, TC-2::test_x with bad refs (...) -> no words (E8)", "F2: an empty manifest -> no words, no crash".
- F3: `test_words_doors.py` new `row_fv130b_the_two_survivors` (live: forwards scope/dispatch, empty scope, raising reader -> None, no live word ->
  empty index; record: no file -> empty index, a line names the instance, unreadable -> None, no-path root -> None); `test_controller_state.py`:
  "(F3) tiers 2, 3 and 4 asked ONE live reader run for the whole finish (+ the recording's own read)" (count 2: one index run + the recording's own
  `word_passes` read in `_record_s5_word_passes`; it was 4 runs before), "(F3) no word yet ... after ONE run of the reader",
  "(F3) a word recorded between two completions is seen by the second (the memo lived for one call)".
- F4: `test_then_remainder.py` `fv1_30b_n2_trace_and_verdict`: "F4: the `no` record's text ends with the word, the Then and the time";
  "F4: a case detail of 120 / 121 / 400 characters is cut at 120 and the mention stays whole"; "F4: a pass with no time -> the mention without
  the parenthesis, no invented time".
- F5: `test_words_doors.py` `row_fv130b_the_two_survivors`: "F5: `_finding_tag` is the waiver splitter's tag"; "F2: `waiver.same_instance` is public".
- F6: covered by the F1 window rows (the helper is what writes them) - no separate row; nesting counted: `_word_kept_keys` loop body = 3 levels.
- F7: the renamed key is asserted by the existing `fv1_30b_the_window_carries_the_word_it_was_given` rows (renamed to `word_passed`).
- F9 / F10: data / removal, no row.

## Verification run (verbatim)

`python -B C:\QAFactory\forge-repo\.claude\worktrees\fv130b-fix\ai-packages\qa-factory\scripts\tests\scenario_walk.py --witness-for <nine owned scripts>`
printed 140 distinct test files (tail: `scripts/traceability.py: keep test_whole_identifier.py (layer detector, covers it)`); 31 of them are
slow (`scripts/slow_tests.json`, `test_controller_*`, `test_scenario_*`, `test_story_run_*`), 57 are not, plus `test_words_doors.py` and
`test_probe_gap_door.py` (the witnesses named by the dispatch). Each run from the package dir in a `( cd ... && )` subshell.

Non-slow files (python -B file, or `python -m pytest file -q` for the pytest ones):
```
test_ahead_cards.py: === test_ahead_cards: 297/297 ok ===
test_awaiting_state.py: === test_awaiting_state: 144/144 ok ===
test_case_key_identity_join.py: === case_key_identity_join: 154/154 ok ===
test_delivery_ownership.py: === test_delivery_ownership: 310/310 ok ===
test_detector_verdict.py: === test_detector_verdict: 195/195 ok ===
test_dispatch_identity.py: === test_dispatch_identity: 114/114 ok ===
test_env_evidence.py: === env evidence: 42/42 ok ===
test_environment_lifecycle.py: pytest 2 passed in 0.90s
test_event_store.py: pytest 48 passed, 27 subtests passed in 3.35s
test_exploratory_answers.py: === test_exploratory_answers: 107/107 ok ===
test_first_look_step.py: === test_first_look_step: 102/102 ok ===
test_fit_targets.py: === test_fit_targets: 116/116 ok ===
test_fixes_13797.py: === TP1-13797 fixes (F1 FB-10, F2, F3, F5, F6, F7 FB-12, F8): 70/70 ok ===
test_flow_requests.py: === flow requests: 94/94 ok ===
test_gate_vocabulary.py: === test_gate_vocabulary: 141/141 ok ===
test_guard_big_read_sections.py: === test_guard_big_read_sections: 248/248 ok ===
test_guard_command_text.py: === test_guard_command_text: 197/197 ok ===
test_handed_to_person.py: === test_handed_to_person: 58/58 ok ===
test_hook_lifecycle.py: === test_hook_lifecycle: 25/25 ok ===
test_local_keys.py: === test_local_keys: 199/199 ok ===
test_manual_evidence.py: === test_manual_evidence: 248/248 ok ===
test_obligation_join.py: === obligation join (TP2-2553): 72/72 ok ===
test_one_source_per_fact.py: === test_one_source_per_fact: 21/21 ok ===
test_oracle_provenance.py: === oracle provenance: 296/296 ok ===
test_pinned_lifecycle.py: === test_pinned_lifecycle: 51/51 ok ===
test_probe_every_check.py: pytest 319 passed in 6.34s
test_probe_marker_judgment.py: pytest 46 passed in 8.92s
test_probe_not_proved.py: pytest 47 passed in 4.78s
test_probe_readers.py: pytest 16 passed in 2.35s
test_probe_target_fact.py: pytest 13 passed in 1.00s
test_quality_demand.py: === quality demand: 84/84 ok ===
test_reducer_recovery.py: === test_reducer_recovery: 11/11 ok ===   (own runner; the pytest form collected nothing)
test_reducer_supersession.py: === test_reducer_supersession: 91/91 ok ===
test_reference_window.py: === test_reference_window: 85/85 ok ===
test_refusal_registry.py: === test_refusal_registry: 354/354 ok ===
test_regression_scope.py: === test_regression_scope: 93/93 ok ===
test_resume_packet.py: === resume packet: 117/117 ok ===
test_resume_story_isolation.py: === test_resume_story_isolation: 310/310 ok ===
test_role_digest.py: === test_role_digest: 93/93 ok ===
test_s0_close_order.py: === S0 close order: 29/29 ok ===
test_s5_plan_windows.py: === test_s5_plan_windows: 104/104 ok ===
test_s5_precheck_sides.py: === s5 precheck sides: 142/142 ok ===
test_s5_window_leftovers.py: === test_s5_window_leftovers: 148/148 ok ===
test_scoped_invalidation.py: pytest 3 passed in 1.15s
test_session_handoff.py: pytest 15 passed, 6 subtests passed in 2.17s
test_sides_ledger.py: === test_sides_ledger: 120/120 ok ===
test_source_stage_integration.py: === test_source_stage_integration: 21/21 ok ===
test_stage_closure.py: === stage closure: 19/19 ok ===
test_stand_gap_remedy.py: === test_stand_gap_remedy: 34/34 ok ===
test_stand_gaps.py: === stand gaps: 182/182 ok ===
test_state_exits.py: === test_state_exits: 142/142 ok ===
test_task_root_project_door.py: === task_root_project_door: 13/13 ok ===
test_then_remainder.py: === test_then_remainder: 320/320 ok ===
test_triage_blocked.py: === test_triage_blocked: 50/50 ok ===
test_triage_identity.py: pytest 31 passed in 1.52s
test_whole_identifier.py: === whole identifier and the revoked word: 166/166 ok ===
test_whole_list_sites.py: === test_whole_list_sites: 292/292 ok ===
test_words_doors.py: === test_words_doors: 710/710 ok ===
test_probe_gap_door.py: pytest 34 passed in 6.07s
```
(control: `test_words_doors` was 702/702 at f1ecdb0 per the dispatch; now 710/710 - the new survivors row adds checks, the two shipped-value checks are gone.)

Slow files, once each after the last edit (the three named exceptions, plus `test_check_delivery` and `test_s5_precheck`, see "needed" below):
```
=== test_controller_state: 377/377 ok ===      exit=0
=== window record: 531/531 ok ===               exit=0
=== test_branch_accounting: 942/942 ok ===      exit=0
=== test_check_delivery: 648/648 ok ===         exit=0
=== test_s5_precheck: 1185/1185 ok ===          exit=0
```
`selftest.py --lang` (package-dir subshell):
```
PASS lang: no Cyrillic anywhere in the package
PASS lang: no control byte left by an eaten escape sequence (FR-29)

=== qa-factory selftest: 2/2 ok ===
```

## Siblings grep (`word_passed_index\(` in non-test scripts)

Before the edit (positive control, the same Grep, same tool): 8 compositions + the producer
(`branch_accounting.py:1917`, `check_delivery.py:1195`, `:1617`, `check_traceability.py:171`, `controller.py:7403`, `coverage_contract.py:566`,
`traceability.py:1171`, `window_record.py:1314`, `waiver.py:942` def). After:
```
s5_precheck.py:4067:        return waiver.word_passed_index(word_passes(task_root, scope or None, dispatch_id))     (survivor 1)
waiver.py:943:def word_passed_index(rows, table=None) -> WordPasses:                                          (producer)
waiver.py:1046:        return word_passed_index(rows) if rows is not None else None                              (survivor 2)
```
Clean. `\b_same_instance\b` in the package: no match (same pattern, without `\b`, found 4 sites before the rename).

## F7 grep (both shapes, case-insensitive, positive control: the pattern found the producers)

`passed_by_word` (bool, per pair of `expectation_changes[]` / `word_passed_pairs`): readers `acceptance.py:283`, `brief_pack.py:691`,
`report_facts.py:1647`, `window_record.py:1105-1106` (copies it), `window_record.py` gap line (`item.get("passed_by_word") is True`),
`finalize_task.py:254-268`; `s5_precheck._flag_word_passed` writes it. None of them is a window INSTANCE.
`word_passed` (list on a window INSTANCE, the F7 key): producers `window_record.build` (two); readers NONE in this round - the AR-22 reader
owed is N6's `window_record.run` (print the item's entries as the "passed by the person's word" note). Observation: the name `word_passed`
now exists in three shapes on three carriers (window-instance list; trace row dict `traceability.py`; coverage item bool `coverage_contract.py`);
no reader crosses carriers, but the "one name one meaning" aim of F7 holds only per carrier - Lead to judge.

## FR walk (sections touched)

- A (refusals): FR-1/FR-2/FR-4 - refusal texts unchanged for an unnamed instance; the let-go only through `window_record.word_let_go`
  on a live, named pass. FR-57 n/a.
- B: text shown to a person changed in F4 only (gate-B reason gains the word mention; English, ASCII, "your word" as the existing `how` text).
  FR-6/FR-10: the reason now agrees with the row's own `how`.
- C: FR-15/FR-42 unchanged; FR-14: the window-instance key rename `passed_by_word` -> `word_passed` is a shape change with NO reader today (named above).
- D: FR-17 (one survivor per problem, wired everywhere): F3. FR-59: None = names nobody, never a pass.
- E: FR-35/FR-41 - text only, `verified`/`person_debt` untouched.
- F, G: FR-28 n/a; FR-29/FR-30 - ASCII only (checked: `git diff -U0 | grep -P '[^\x00-\x7F]'` empty), `selftest --lang` green; FR-31 n/a; FR-45: no validator writes.
- AR-13, AR-15, AR-28 named in both commits (one survivor per composition; a failed index build = None = refuse as today).
- Census/ratchets: no ratchet row touched or raised.

## Deviations and decisions to confirm

1. F5: the dispatch asked `_finding_tag` to delegate to the waiver splitter. Reality: `test_s5_precheck.py` (~line 3063, "no waiver") sets
   `sys.modules["waiver"] = None` and runs `passed_by_word`; `_passable` -> `_finding_tag` must work with NO waiver import, and the delegation
   raised `ModuleNotFoundError` (1 test file red). Commit 1 (04d8b07) carries the delegation; commit 2 reverts it to the local split and
   corrects both docstrings (the waiver splitter no longer claims to be the one; `exit_gate._finding_tag_of` and `_finding_tag` are the two
   queued copies). This is the verdict's own second option. A design fork for the Lead: a splitter in a module both can import without
   `waiver` (e.g. `contract.py`) would give one survivor - not decided here.
2. Commit 1 is not the survivors ALONE: it also holds `waiver.same_instance` (public) and the F5 delegation (same two files). N3/N6 can start
   from it as asked; the F5 part is reverted in commit 2.
3. `_word_kept_keys(identity, empty_fields, index, table)` - the spec's first parameter `item` was dropped: nothing in the helper read it.
4. `window_keys` stays a dict (values used), so `word-passed-facts.json` and the two shipped-row checks that read it are untouched.
5. F3 memo count: the finish still reads `word_passes` once more in `_record_s5_word_passes` (it needs the ROWS, not an index, and runs only on an accepted
   completion). Not routed through the memo (not named by the verdict); the row pins "2 = one index run + the recording read".
6. `test_check_delivery.py` is in `scripts/slow_tests.json` (85 s) and `test_s5_precheck.py` is not named there but is large; the dispatch's DoD named
   both, so both were run once (plus window_record, branch_accounting, controller_state). `test_controller_state.py` was run three times: runs 1 and 2
   exposed my own row mistakes (a row that accepted the story and closed it for the rows after it; the F3 count of 2); the quoted run is the last, green.
7. A `sed -i` on `test_window_record.py` (a rename inside lines 1639-1715) was used once instead of Edit; the hygiene gate did not refuse it; the diff is
   the 12 renamed lines (reviewable in commit 2).

## Test-line budget (F10, one reason line each)

- N1 (~435 test lines for ~259 product lines): the product code is a table-driven let-go at three tiers, and every refusal text plus every accepted-completion
  path needs its own story fixture (an accepted stage is closed, so each accepted row builds a fresh story); rows (a)-(n) of the spec are one assert each.
- N2 (~245 test lines for ~205 product lines): three independent readers (trace rows, ledger/verdict text, coverage words) over three constructed carriers;
  the spec's seven v-rows and four c-rows are separate readers of the same fact, each needing its own fixture. Neither count is reduced by this round
  (this round adds ~70 test lines for ~70 product lines).

## Siblings / class (rule 5), noticed but not done

- `exit_gate._finding_tag_of` (third splitter) and `s5_precheck._finding_tag` (second): queued; one survivor needs a home both can import without `waiver`.
- `_record_s5_word_passes` still reads `word_passes` rows by itself (see 5): a fourth reader of the same rows, outside the index memo.
- `controller._passed_by_person` / `exit_gate.judge_words` text road, N5 alias split, `build_left_items` (F8): unchanged, already named by the verdict.
- Name `word_passed` on three carriers (see F7 grep).

## Needed beyond the manifest

`scripts/slow_tests.json` and `scripts/tests/test_s5_precheck.py` (the F5 break), `scripts/tests/test_probe_not_proved.py` (stub that calls `_s5_completion_problems`
unbound; the memo is read through `getattr`), `scripts/contract.py` (`test_instance_id`).
