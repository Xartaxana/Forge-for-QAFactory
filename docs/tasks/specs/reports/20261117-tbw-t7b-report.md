# TBW T7b report (t-966) - `planning_contract.py` sites (wave A)

Worktree `C:\QAFactory\forge-repo\.claude\worktrees\agent-abd9ee64efb51bac3`, branch `worktree-agent-abd9ee64efb51bac3`. Builder, Sonnet. No REJECT line, `str(exc)` or exit code changed by one byte
(rows assert the old text; REJECT blocks, headers, the `S3 exit:` tail and the waiver line are untouched).

## What was done

- `planning_contract.py`: `from detector_verdict import refusal`; 12 row ids sited as literal `refusal("<id>", <same text>)` calls (table below). `refusal()` is the only road (axis 34); no hand-built `Record`.
- Re-located by Grep (the card's numbers are old): `gate_plan_errors` 286, `contradiction_errors` 1468, `s3_branch_refusals` ~3250, `fence_lines` ~3952, `_branch_block_lines` ~3986, `_regression_findings` ~3998, `fit_target_block` ~4328, `_request_findings` ~4384, `_detector_body` ~4453.
- `_regression_findings` docstring reworded per F-W5 (a): "a check that CANNOT RUN ... never holds a story; a problem the check FINDS is a REJECT of the S3 exit (P24)".
- Test: ONE new function `tbw_t7b_sites` in `test_detector_verdict.py` (placed before `if __name__`, one call line `tbw_t7b_sites()` added to `main`; nothing else in the file touched). 14 table rows + 3 control rows = 31 PASS lines.
- Changelog `changelog.d/tbw-t7b.md` (one English ASCII bullet).
- Not touched: stage-joints.json (rows, `told_ratchet`), `test_stage_joints.py` (K12 pin), pages, role-*.json, inject-map.json, `regression_scope.py`, `unmarked_revision_errors`, WARN lines, waiver line, quarantined tests.

## Site table (function | fragment | id or E6 reason (class) | test row | proof)

Proof: F = proved fast (run, `test_detector_verdict.py`); N = not provoked.

| function | fragment | id | row (`t7b <id> (<key>)`) | proof |
|---|---|---|---|---|
| `gate_plan_errors` (wraps `validate_plan` + `coverage_revision_errors` lines; one id at the S3/gate caller, EC-2) | every plan problem line | planning_contract:plan | `plan depth`, `plan revision` | F |
| `contradiction_errors` | "no plan row covers R" ; "carry neither source_conflict nor oracle_unknown" (2 appends) | planning_contract:contradictions | `contradictions none`, `contradictions unflagged` | F |
| `_branch_block_lines` | each `- ` line of the question-branch REJECT block | planning_contract:branches | `branches` (header stays plain) | F |
| `s3_branch_refusals` (+ kept through `_branch_block_lines`) | the `new_questions` problems (`bad_branch` dicts) | planning_contract:branches.new_questions | `branches new_questions` | F |
| `fence_lines` | no plan row for R | planning_contract:fence.plan_row | `fence plan_row` | F |
| `fence_lines` | R in plan json, not in the md `R` column | planning_contract:fence.r_column | `fence r_column` | F |
| `fence_lines` | candidate defect without a planned test | planning_contract:fence.candidate_defects | `fence candidate_defects` | F |
| `fence_lines` | requirement waits for a question with no branch | planning_contract:fence.waiting_branch | `fence waiting_branch` | F |
| `_regression_findings` (caller of `regression_scope.problems`, E-T7b-1) | each problem of `## Recommended regression` | planning_contract:regression | `regression` | F |
| `fit_target_block` | each `- ` line of the plan-target REJECT block | planning_contract:targets | `targets` | F |
| `_request_findings` | form lines, closure lines, the "N more problems" tail | planning_contract:requests | `requests`, `requests capped` (tail via a patched `branch_accounting.limit`) | F |
| `_detector_body` | "<plan> is not readable JSON" print | planning_contract:plan_json | `plan_json` (runs the body, spies on `refusal`: a print cannot carry the Record, the REJECT text is unchanged) | F |

Edges: EC-5 empty - one row asserts no problem gives `[]` for plan, contradictions, branches, targets, fence, requests, regression (F). EC-4 unreadable row: the one constructor's own answer (S-1a row `unreadable`), not repeated. EC-2: `validate_plan` has 7 callers (controller x3, manual_evidence, plan_row, validate_artifacts, CLI) so it carries no literal; the id sits in `gate_plan_errors`. Its other callers inside the module (`variant_errors` x2: the same requirement, the Record is discarded in their joined text) and `gate_preflight` ask the same requirement. EC-6: no key/line moved. E-T7b-1: `regression_scope.py` not edited (`git diff --stat`: 2 source files + report + fragment).
Bare on purpose: `unmarked_revision_errors` lines (their `check` stays `""`, row asserts it; conductor door, node T9c).

## E6: bare remainder, classed

- (code) `validate_plan` direct callers outside `gate_plan_errors`: `controller.py` 3258/5487/7618, `manual_evidence.py` 988, `plan_row.py` 234/259/260, `validate_artifacts.py` 2679, `planning_contract.py` CLI `main` ~4669: conductor/CLI/write-time, same text, no id (EC-2).
- (code) `unmarked_revision_errors` lines: T9c (F-W4 (b)).
- (code) WARN lines, the waiver line, the exit-0 "no structured test plan yet" line, `UNREADABLE:` exits, `validate_case_actions`, `publication_manifest`, the CLI "not a file" error: no row per wave0 item 3a.
- (code) `grounding_table.role_exit_lines` lines appended to `errors` in `_detector_body`: another module, its own row family.
- (role) none found: no bare site states a requirement a role can meet that is not a row.

## Rows that over-claim (EC-8, for T1r-cards-R; not edited)

- `planning_contract:plan` sentence says "every obligation of the registry has its row" but the lines it now tags are `validate_plan`'s risk/coverage-field checks and `coverage_revision_errors`; "every requirement has a plan row" is what `fence.plan_row` states. The `plan` sentence claims more than `gate_plan_errors` checks (the obligation lines come from `coverage_contract.validate_obligations`, T7c).

## Analogs noticed (not widened)

- `gate_preflight.py:1918` calls `gate_plan_errors` and now receives `plan` Records inside its `problems`; it joins them as text (no transport change; its sibling sites belong to another node).
- `grounding_table.role_exit_lines` and `regression_scope.py` print `"- " + line` themselves (`regression_scope.main`): same class, other modules.

## Counters

`python -B ai-packages/qa-factory/scripts/stage_joints.py --check`: BEFORE `told counters: hand_cards 12, legacy_legs 0, unsited 119`; AFTER `... unsited 107` (-12): plan, contradictions, branches, branches.new_questions, fence.plan_row, fence.r_column, fence.candidate_defects, fence.waiting_branch, regression, targets, requests, plan_json. `told_ratchet.unsited` and the K12 pin are NOT edited (F-1 (a)): `test_stage_joints.py` pins 119 exactly and stays red in the canon until the integrator commit - named, not a defect of this node. Ratchets: no raise anywhere (AR-20).

## FR walk

- A: FR-1/2/9 refusal texts and doors unchanged, the Record adds `expected`/`door` beside; FR-59 an unreadable row gives the factory-defect sentence (`refusal()`); FR-4/57 n/a, no gate added.
- B: no text a person reads changed. C: FR-14 output shape unchanged (stdout lines identical); FR-38 n/a here (page carriage not touched). D: FR-16 literal ids at the site, all 12 are existing rows. E, F: not touched.
- G: FR-30 English/ASCII (`selftest --lang` PASS); FR-31 no timing assertion; FR-32 root cause = the one constructor; FR-54 siblings listed above.
- AR: AR-9 (sites carry the row), AR-13 (`told_text` through `refusal()` only), AR-18 (output shape unchanged), AR-29 (no judgment moved or added). census: no new blocking unit (a siting attaches an id to an existing refusal; `test_judgment_census.py` is slow, judged by the batch canon).

## Cost note

`refusal()` reads `stage-joints.json` (215 KB) once per problem line. `gate_plan_errors` also runs inside `variant_errors` per patched row; with no error it costs nothing, with errors ~3 ms each. Not measured further.

## Verbatim witness

```
$ python -B ai-packages/qa-factory/scripts/tests/test_detector_verdict.py
=== test_detector_verdict: 495/495 ok ===                     (31 `PASS t7b ...` lines; 21.7 s)
$ python -B ai-packages/qa-factory/scripts/stage_joints.py --check
stage joints: walked exit 8, detector 5, window 27 | rows 267, gaps 4 (producer 2, told 1, demands 1), joints held 4 of 267 | role leg not walked (code-to-code rows): 26 | stages with no detector: S0, S1, S6, S7, S9 | told counters: hand_cards 12, legacy_legs 0, unsited 107
stage joints: clean
$ python -B ai-packages/qa-factory/scripts/selftest.py --limits --lang
PASS lang: no Cyrillic anywhere in the package
PASS lang: no control byte left by an eaten escape sequence (FR-29)
PASS limits: SKILL.md / agents / references within size caps
PASS limits: every mandatory role rule of design/role-rules.json holds in its carrier
=== qa-factory selftest: 4/4 ok ===
$ scenario_walk.py --witness-for ai-packages/qa-factory/scripts/planning_contract.py ai-packages/qa-factory/scripts/tests/test_detector_verdict.py   (each non-slow, non-quarantined file alone, 90 s cap, scratch runner)
test_baseline_contract rc0; test_detector_verdict 495/495; test_dispatch_identity 114/114; test_fit_targets 116/116; test_flow_requests rc0; test_gate_question_form 591/591;
test_gate_role_accounts 44 passed; test_guard_window_files 103/103; test_owner_role_one_list 15/15; test_regression_scope 93/93 (55 s); test_s5_window_leftovers 148/148;
test_stage_joints_12586 12/12; test_validator_class 51/51; test_walk_plan_fields rc0; test_whole_list_sites 292/292; test_scenario_walk 93/93; test_scenario_world 33/33
judged by the batch canon (all in slow_tests.json): test_scenario_cart_1, test_scenario_local_1_0108, test_scenario_local_1_arm_b, test_branch_accounting, test_check_delivery, test_console_encoding,
test_controller_gate_decision, test_gate_brief_and_retro, test_gate_preflight, test_gate_registry, test_grounding_table, test_handoff, test_story_closed, test_story_run_loop_b_answers,
test_story_run_loop_b_loop, test_story_run_loop_b_threshold, test_story_run_s3_windows, test_story_run_s6, test_words_doors (it holds the planning_contract detector row of FR gate words)
```

Old text (EC-1): captured by running the SAME test function over a byte copy of the pre-change `planning_contract.py` (scratch driver, not committed; sha256 of the copy
`844cccb4a7793e0b05bc04b0901544ed18e5c8aabe9bdabcc4d0a83e665a1b3d` = HEAD file); the texts it printed are the literals of `old` in `tbw_t7b_sites`; the new file gives the same on every row.

Negative control: byte copy of the good file (`t7b_pc_good.py` in the scratchpad) taken first; the `requests` site turned bare (`return lines`): `test_detector_verdict.py` printed
`FAIL t7b planning_contract:requests (requests): every finding is a Record of the row ...` and the same for `(requests capped)` (493/495), `stage_joints.py --check` showed `unsited 108`;
restored with `cp` from the copy, hashes equal: `5490eb8ccbfa1c44c4a5af71463a31f017422459303a83941a53f683514550d1` both, `unsited 107` again.

tests-over: test lines (162) exceed code lines (89): about 75 of them are the old-text literals that prove EC-1 byte identity for 12 ids.

## Questions for the Lead

none. (Decision I took inside the card: `validate_plan` carries no literal because of EC-2; the id is in `gate_plan_errors`, which the card lists first. Say if you want it elsewhere.)

## Needed beyond the manifest

`detector_verdict.py` (`refusal`, `Record`, `one_line`), `stage_joints.py` (`check_ids`, `row_for`, `told_text`, `_is_sited`), `regression_scope.py` (`problems`), `user_path_failures.py` (`read_requests`, `failure_axis`), `runtime_paths.py` (`project_for_task`), `harness.py` (`temp_project`, `use_project`), `test_words_doors.py` / `test_case_gates.py` / `test_s3_s4_chain.py` (fixture shapes), `slow_tests.json`, `test-layers.json`, `scenario_walk.py` output, wave0 rows file `docs/tasks/specs/20261113-told-before-work-wave0-rows.md` (the card named it only by §3a).
