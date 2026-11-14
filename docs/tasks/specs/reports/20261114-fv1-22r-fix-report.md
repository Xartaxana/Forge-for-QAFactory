# t-686 - FV1-22 re-cut, the one fix round after the topic critic (t-683), builder report

Worktree `.claude/worktrees/fv1-22r-fix`, branch `wip/fv1-22r-fix` (from N3 a56ae5c with N1 merged, d3a8c66).

## Per finding

| finding | what changed | where | test row |
|---|---|---|---|
| B1 | row `Driver.record_repeat` (note form, home `driver_runner`) next to `Driver.journal_run`; plus the state-key row `repeat_recorded` (owner `driver_runner`, the lowest accessor - it is new with F2, the L-census would refuse it without) | `scripts/tests/fixtures/driver-layers.json` (names, after `Driver.journal_run`; state_keys, after `window_rounds`) | `test_driver_layers.py` L1/L-state: SLOW, judged by CI |
| F1 | S7/S8 refusal reads "write one of them at `<path>` of the form", `<path>` = `handoff.acceptance_verdict_path(form["contract"])`; a form with no contract, or a contract `handoff.template` cannot read (unknown), keeps a generic sentence ("the form must carry one of them as its verdict"); never prints `None` or an empty path | `acceptance.py` `stage_acceptance_from_form` (the problem line, ~:1590-1600) | pure probe below (no test file of the finding is in owns; `test_stage_acceptance_consumer.py` is quarantined) |
| F2 | `record_repeat` keeps its own persisted mark `state["repeat_recorded"]` keyed `road|key|finding_key(lines)|outcome`; second arrival writes nothing; another outcome writes; absent / None / not-a-dict mark = empty and is replaced by a dict; the mark is set only after `journal_run` succeeded (a failed write is retried at the next arrival) and saved by `save_state` | `driver_runner.py` `Driver.record_repeat` (~:421-452); import of `finding_key` | `test_fv122_n3b_second_arrival_of_the_same_set_writes_nothing` (3 older-state shapes x: first writes, second no, other outcome yes, relaunch from the JSON-round-tripped state no) |
| F3 | S-c records only when `done.get(dispatch)` | `driver_machine.py` `handle_refusal`, `resume_structured` (~:549-556) | `test_fv122_n3b_structured_resume_without_a_spent_resume_is_no_repeat[False-0 / True-1]` through the real `handle_refusal` |
| F4 | keep row rewritten (`why`) and `covers` + `driver_gates.py`, `driver_machine.py`, `driver_runner.py`, `driver_stage_plan.py` | `scripts/tests/test-layers.json` `test_probe_gap_door.py` | `scenario_walk.py --witness-for ...driver_runner.py ...driver_machine.py` now prints `keep test_probe_gap_door.py (layer data_join, covers it)` (lines 67 and 143 of the run) |
| F5 | named stub, `assert fv122_rounds(stub) == [] and stub.journal_rows == []` | `test_probe_gap_door.py` `test_fv122_stage_outside_the_table_is_gated` | itself |
| F7 | one `if result["session_id"]:` block (print then record) | `driver_dispatch.py` `handoff_ladder` (~:541-544) | covered by CI slow files; no unit row |

## F2: the invariant "a row is never written for a non-stop" - how it is kept, and the one residue

The call stays where it is at S-b..S-d (before `exit_limit`); S-a and S-e are unchanged (S-a's own `if not any(...)` and S-e's early return stay; the mark is a second, harmless guard there). The paid-round arrival (`granted > spent`, `exit_round`, no stop) has the SAME set as the stop that asked the person, so it is the same tuple and writes nothing: a stop is counted once and the paid round is never a second row.

I first wrote a direct `granted > spent` check inside `record_repeat` (reading `state["exit_limit"]`) and removed it: `exit_limit` is owned by `driver_dispatch`, `record_repeat` lives in `driver_runner`, a lower layer, and `test_driver_layers` (L7: owner at or below every accessor) would refuse it. A check at the three callers would need a new reader of the exit record in `driver_machine`/`driver_dispatch` - beyond "only the place the finding names".

RESIDUE (a fact for the Lead): a paid round granted on a set whose stop was NOT recorded (the no-session branches at `driver_machine.py:~270`, `driver_dispatch.py` no-session `handoff_ladder`, and S-c with no session - none of them is a repeat, so none records), followed by an arrival of the same set WITH a session, would write one `repeat_stop` row at that arrival although it spends a paid round. It needs a person to buy a round on a no-session question and then a session to appear for the same dispatch and the same lines; not seen in any run. If the Lead wants it closed, the move is a caller-side guard (not in this round).

## Remarks (a)-(e)

- (a) `architecture:` line of the N2 commit omits AR-28: history, not editable; this commit's line names AR-18, AR-22, AR-10.
- (b) console prints "window" in `window_round_gate`: NOT done - they are four strings with branching text (`~:375`, `~:387`, `~:425-431`), not one line. Queue.
- (c) `vocabulary.yaml:121-123` "stage critic (S2-S4)" and `stage_done.py:961` docstring are outside the owns; the S7 skeleton comment "Reviewed dispatch" is in a template outside the owns. Queue.
- (d) a form that deletes the `stage_acceptance.verdict` line: safe direction, no fix.
- (e) `window_round_lead(...)` extraction: queue.

## Siblings

- Other callers of `record_repeat`: five, all named in the critic's verdict: `driver_machine.py:301` (S-b), `:373` (S-a), `:552` (S-c, now guarded), `driver_dispatch.py:544` (S-d, was already guarded by the session), `driver_gates.py:1000` (S-e). All go through the mark now.
- Other `Driver.*` methods without a `driver-layers.json` row: not checked by a run (`test_driver_layers.py` is slow, CI). I did not grep the whole class by hand.
- Other refusal texts in `stage_acceptance_from_form` saying "end its header": none (grep `end its header` over `scripts/*.py` after the edit: no hit).
- `driver_gates.py` is the S-e site and was not edited: `record_repeat` there needs no change.

## Divergences from the spec / facts found

- The reader `handoff.acceptance_verdict_path` NEVER returns nothing: for an unknown contract it answers its default `header.verdict`. The Lead's edge "unknown contract keeps the generic sentence" is therefore done by calling `handoff.template(contract)` first (raises for an unknown id) and falling back to the generic sentence.
- F2 mark: the driver-layers state-key row `repeat_recorded` was needed (not named in the verdict) - added in B1's file.

## Verification (verbatim)

`python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for acceptance.py driver_runner.py driver_machine.py driver_dispatch.py` lists 253 keep/scenario rows. The non-slow files among them (not in `slow_tests.json`, not `story_run`/`controller`), each run as `python -B tests/<file>` from `scripts/`: 31 files, all rc 0:

```
test_check_witness 29/29; test_codex_tool_guidance 217/217; test_dispatch_identity 114/114; test_driver_stop_record 255/255;
test_exploratory_answers 107/107; test_field_producers: 920/920 ok; test_first_look_code_look 127/127; test_first_look_step 102/102;
test_gate_question_form 297/297; test_handed_to_person 58/58; test_human_questions 291/291; test_interim_packet 54/54;
test_login_need 33 passed; test_manifest_put_merge 378/378; test_null_outcomes 337/337; test_person_owned 82/82;
test_probe_by_code_languages_plan 502/502; test_probe_by_code_languages_ts_playwright 140/140;
test_probe_gap_door 51 passed in 7.09s; test_probe_marker_judgment 46 passed; test_probe_not_proved 47 passed;
test_probe_readers 16 passed; test_probe_target_fact 13 passed; test_quality_demand 84/84; test_reference_window 85/85;
test_s5_precheck_sides 142/142; test_s5_window_leftovers 148/148; test_walk_account 190/190; test_walk_lanes_parallel 196/196;
test_walk_supply 261/261; test_whole_list_sites 292/292
```

`python -B -m pytest test_probe_gap_door.py -q -p no:cacheprovider` -> `51 passed in 8.32s` (was 48; +3 = F2 twin x1, F3 x2).

`python -B ai-packages/qa-factory/scripts/selftest.py --limits --lang` -> `PASS limits: SKILL.md / agents / references within size caps`, `PASS limits: every mandatory role rule of design/role-rules.json holds in its carrier`, `=== qa-factory selftest: 4/4 ok ===`.

F1 probe (pure, `acceptance.stage_acceptance_from_form` on empty forms):
```
contract s7-analyst-to-automator -> ...is not one of approve|...|return; write one of them at `stage_acceptance.verdict` of the form
contract s7-analyst-to-scribe    -> ...; write one of them at `header.verdict` of the form
contract nope (unknown)          -> ...; the form must carry one of them as its verdict
no contract                      -> ...; the form must carry one of them as its verdict
```

Slow files NOT run here, judged by the one CI run: `test_driver_layers.py` (B1 and the state-key row), `test_story_run_loop_b_loop.py` (loop_waiver_and_journal_shapes: the row shape and L8), `test_story_run_refusals.py`, the `test_no_move_seam_*` files, `test_driver_chain.py`, `test_conductor_doors.py`, `test_infra_failure_*`, the `test_story_run_*` set.

## Pushed commit and CI

Fix commit pushed to `wip/fv1-22r-fix`: `01563f1960848c3769bec22eab2060e53e86dc5f`. CI run started once (canon.yml, `python -B tools/ci_read.py start --ref wip/fv1-22r-fix`): run id `43534916929`; NOT read - the Lead's correction says do not wait. The slow files named above are judged by the batch canon after the merge.
