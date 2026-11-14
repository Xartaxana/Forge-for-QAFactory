# T1r-sites S-1b report (t-753) - `told_fields`, `run_suite.py` sites, the road printers

Worktree `C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r`, branch `wip/tbw-t1r`, on top of 3051b16 (S-1a). Builder, Sonnet. No refusal text, `error`
value, person question or `MINE (note)` line changed by one byte (rows assert it). One JSON line stays one line, `told` is appended LAST, exit codes unchanged.

## What was done

- `detector_verdict.told_fields(source)` (next to `spoken`): collects the Records with a check from a Record, a list/tuple, or an exception (its `records`
  when non-empty, else `args[0]` when that is a Record); `{"told": [{check, expected, door}]}` distinct by check, first-seen order, an empty value's key left out;
  `{}` otherwise (str `args[0]`, `args == ()`, odd source); never raises.
- `run_suite.py`: `from detector_verdict import refusal, spoken, told_fields`. Sites: `run_suite:phantom_story` (`_refuse_phantom_story`), `run_suite:detail_target`,
  `run_suite:untyped_story_run` (`ap.error(spoken(refusal(...)))`), `run_suite:missing_executor` (the `told` key beside the unchanged question),
  `run_suite:reparse` (8 raises, `RequestError(refusal(...))`), `execution_request:stand.reference` (`main`'s `reference_target_problem` print),
  `execution_request:stand` (the "runtime probe does not match" raise, edge 5), `run_suite:begin` (`main`'s `store.read` lookup, B3), `execution_request:active_dispatch`
  (`resolve_mine_detail`, B3). Printers with `**told_fields(...)`: `invalid_request` (main x2 incl. the launch-path `store.begin`, phantom story, detail target),
  `invalid_recovery`, `invalid_reparse`, `invalid_schedule`, `mine_refused` (x2), the `WindowFirst` payload, `run_refused` (stand.reference), `executor_unavailable`.
- `red_sandbox.py`: `_carry_told` (copies the child's own `told` list from the summary `_run_mine` already parsed, or `told_fields(exc)`; distinct by check); `probe` and `diagnostic`
  answer a refused run with a `told` key beside the unchanged notes; the in-process `ER.fresh_evidence` handlers (`_author_baseline`, `_diagnostic_red`) collect `told_fields(exc)`.
- `probe_by_code.py`: `Refusal(message, *records)` (`records`, same text); `_profile_of`, `_profile_cwd` (`execution_request:profile`) and `_dispatch_context` (`execution_request:active_dispatch`)
  raise it with the row; the one-JSON printers of `main` and `_plan_cli` add `told_fields(exc)`; the handlers of a refused `build_mine_request` add `told` (the probe record in `_run_and_judge`,
  the row outcome in the walk via `_walk_stamp`).
- `import_test_receipt.py`: the handler of `validate_request`'s `RequestError` re-raises the same message as the `args[0]` Record of its first check, so `role_cli.run_guarded` prints the row's `expected:` / `door:` / `check:` lines.
- `execution_scheduler.py`: `_child_row` keeps the child's `told` list on a `run_refused` group row.
- Tests: rows of the existing table `t1rs_sites` (`test_detector_verdict.py`, function `t1rs_roads`, column `road`); `told_fields` shapes are rows of the same table; two printer rows written, NOT run, in `test_execution_request.py`.
- Changelog bullet appended to `changelog.d/tbw-t1r-sites.md`.

## Site table (function | fragment | id / E6 reason (class) | road | test row | proof)

Proof: F = proved fast (run), W = written in `test_execution_request.py`, not run, N = not provoked.

| function | fragment | id | road | row | proof |
|---|---|---|---|---|---|
| `_refuse_phantom_story` | the `StoryRootError` text | run_suite:phantom_story | run_suite | `t1rs road run_suite run_suite:phantom_story` | F |
| `resolve_detail_target` | `OSError/ValueError` text | run_suite:detail_target | run_suite | `... run_suite:detail_target` | F |
| `refuse_untyped_story_run` | UNTYPED_STORY_RUN | run_suite:untyped_story_run | run_suite | `... untyped_story_run` (stderr: old text, then `expected:` line) | F |
| `refuse_missing_executor` | the person question | run_suite:missing_executor | run_suite | `... missing_executor` | F |
| `reparse_run_block` | 8 raises | run_suite:reparse | run_suite | `... run_suite:reparse` (first raise; the 7 others same wrapper) | F |
| `main` | reference_target_problem print | execution_request:stand.reference | run_suite, schedule | `... stand.reference`, `schedule ... stand.reference` | F |
| `main` | existing-key `store.read` corrupt | run_suite:begin | run_suite | `... run_suite:begin` | F |
| `main` | `JobStore.recover` | run_suite:recover | run_suite | `... run_suite:recover` ("unknown execution job") | F |
| `main` | "runtime probe does not match requested profile/source/runtime" | execution_request:stand | run_suite | none (needs a live probe) | N |
| `main` | `store.begin` in the launch path | (printer only; ids come from JobStore, S-1a) | run_suite | none (needs the whole launch) | N |
| `main` | `validate_request` error | execution_request:freshness (representative) | run_suite, import_test_receipt, schedule (`invalid_schedule`) | three rows | F |
| `mine` | `MineRefusal` | execution_request:active_dispatch (representative) | run_suite | `... active_dispatch` | F |
| `mine` | `WindowFirst`, `selector_args` | window_first, selector_args | run_suite | `t1rs_sites_after_the_probe` | W |
| `resolve_mine_detail` | `find_active_dispatch` | execution_request:active_dispatch | run_suite | `... (--mine --detail)` | F |
| `_run_mine` / `probe` / `diagnostic` | refused summary | (child's own) | red_sandbox | `... red_sandbox active_dispatch` (real child), `... profile` (two in-process handlers) | F; the `told` key on the final `probe` / `diagnostic` dict: N (needs a sandbox) |
| `_profile_of`, `_profile_cwd` | `_profile_for` / `unknown_profile_refusal` | execution_request:profile | probe_by_code | `... probe_by_code ... (_profile_of / _profile_cwd)` | F (the exception); the printed line of `main`: N |
| `_dispatch_context` | `find_active_dispatch` | execution_request:active_dispatch | probe_by_code | `... (_dispatch_context)` | F (the exception); printed line: N |
| `_run_and_judge`, `_walk_attempt` handlers | refused `build_mine_request` | the Record's own | probe_by_code | none (need a probe) | N (`test_probe_walk.py` / `test_probe_by_code.py` judged by the batch canon) |
| `import_receipt` | `validate_request` error | first record's check | import_test_receipt | `... import_test_receipt freshness` | F |
| `_child_row` | child's `run_refused` line | child's `told` | schedule | `... schedule stand.reference` (real child) | F |

## Road table (road -> printer -> carries `told`)

| road | printer | `told` | why |
|---|---|---|---|
| run_suite | main/mine/recover/reparse/schedule/refusers, one JSON line | yes (key `told`, last) | `told_fields` |
| run_suite untyped | `ap.error(spoken(...))` | yes, as text (`expected:` / `door:` / `check:` lines), no JSON | the T2 text road of the same Record |
| red_sandbox | `probe`/`diagnostic` answer dict | yes, on a refused run (key `told`, notes unchanged) | `_carry_told`, no third parser |
| red_sandbox in-process handler | same dicts | yes on the refused answer; the fallback ("own baseline") that goes on to a result carries none, nothing refused | no refusal reaches the role there |
| probe_by_code refusal JSON | `main` / `_plan_cli` | yes | `Refusal.records` + `told_fields` |
| probe_by_code probe record / walk outcome | `record["told"]`, outcome `told` | yes (code written, N proof) | `told_fields(exc)` |
| import_test_receipt | `run_guarded` text refusal | yes for the FIRST check only (see questions) | one Record per refusal on the text road |
| schedule | group row of `_child_row` | yes (pass-through of the child's list) | existing reader |

## E6 (bare) sites in `run_suite.py`, classed

- (code) `raise ProvenanceRefused(value)` (930), `RuntimeError("immutable run block already exists")`, `raise known["error"]`, the budget `run_refused` prints (`_say_budget`, `verdict["message"]`: no row, S-1a E6), `stand_busy`, `nothing_to_wait`, `still running`.
- (code) `ap.error` argument checks of `main` (`--mine ... do not combine`, `--reparse-block requires`, `--recover requires`, `--detail needs`, `--collect-only needs`, `--task and --label are required`): argparse usage, `role_cli:run_suite` card.
- (role, queue to T1r-cards) `no_recorded_run` print of `resolve_detail_target` (1131): states "no finished run of this request ... is recorded", the same requirement as row `run_suite:detail_target`, left bare because the spec's site list names only line 1115; a role that meets it is not told the row (E4 residual).
- (role, queue to T1r-cards) `main`'s `story_root(raw_task, "run_suite.py --request: the request's task")` `StoryRootError`: the request's task names a story that is not there; row `run_suite:phantom_story` is for `--task`, no row owns the request field; prints `invalid_request` with no `told`.
- `probe_by_code.py` `_dispatch_stage` / `_judge_dispatch_why` (calls of `find_active_dispatch`): (code) read a row to build the caller's own context; the returned reasons are the caller's words, never the helper's `str(exc)`.
- Siblings, not edited: `onboarding_probe.py:278` (`ER._command_from_profile`, returns `[str(exc)]` to the onboarding skill): (role) - the onboarding role reads it, class `profile_command`. `window_record.py:267` (`unknown_profile_refusal` as plain text in the window-record gap sentence): a role reads it, it is the `execution_request:profile` requirement; not edited (not owned). `execution_scheduler.py` `main`'s own `invalid_schedule` print (708) and the `_apply_budget` `run_refused` row: not in owns; the first is the same class as `run_suite`'s `invalid_schedule` (queue).

## P-7 grep witness (`run_suite.py`)

Direction 1 (every literal, `grep -n 'refusal("' run_suite.py`): `run_suite:reparse` x8 (739-819), `run_suite:phantom_story` 971, `run_suite:detail_target` 1119, `run_suite:untyped_story_run` 1420,
`run_suite:missing_executor` 1576, `execution_request:stand.reference` 2888, `run_suite:begin` 2894, `execution_request:stand` 2912, `execution_request:active_dispatch` 3118.
Direction 2 (every `refusal("execution_request:|run_suite:` of `scripts/*.py`, `grep -ho ... | sort | uniq -c`): 29 distinct ids on one line, `place_rows` and `selector_args` call through a multi-line form; `stage_joints.py --check` counts all 31 sited
(`unsited 150 -> 124 -> 119`). No id outside the 31 rows. No raise or JSON refusal print of `run_suite.py` is unaccounted: every one is a site above, a printer above, or in the E6 list.

## `stage_joints.py --check` summary

BEFORE (S-1a report): `... unsited 124`. AFTER: `stage joints: ... told counters: hand_cards 12, legacy_legs 0, unsited 119` / `stage joints: clean`.

## FR walk

- A: FR-1/2/9 texts and doors unchanged, the row's `expected` / `door` ride beside; FR-59 an unreadable row gives the factory-defect sentence, no `door` key (row `unreadable` of S-1a is the same `refusal()`; `told_fields` leaves an empty key out).
- B: no text a person reads changed (the person question of `executor_unavailable` byte-identical, `told` a sibling key). C: FR-14 output shape additive, `told` last; FR-17 one projection `told_fields`; FR-38/49 page carriage is S-2.
- D: FR-16 literal ids; none outside the 31 rows. E/F: n/a. G: FR-30 English/ASCII (`selftest --lang` green); FR-31 no timing assertion; FR-32 root-cause; the road rows run real child processes only twice (a `run_suite.py` child each, seconds).
- AR: AR-9, AR-13 (`told_fields` the one builder of the key; `_carry_told` copies, builds nothing), AR-15, AR-18, AR-22 (`records` / `told` have readers), AR-28 (unknown row -> sentence, `{}` on odd source), AR-29 (no meaning check).

## Verbatim witness

```
$ python -B ai-packages/qa-factory/scripts/tests/test_detector_verdict.py          (inside the node's witness run below)
=== test_detector_verdict: 430/430 ok ===
$ python -B ai-packages/qa-factory/scripts/stage_joints.py --check
stage joints: walked exit 8, detector 5, window 27 | rows 267, gaps 4 (producer 2, told 1, demands 1), joints held 4 of 267 | role leg not walked (code-to-code rows): 26 | stages with no detector: S0, S1, S6, S7, S9 | told counters: hand_cards 12, legacy_legs 0, unsited 119
stage joints: clean
$ python -B ai-packages/qa-factory/scripts/selftest.py --limits --lang
PASS limits: SKILL.md / agents / references within size caps
PASS limits: every mandatory role rule of design/role-rules.json holds in its carrier
=== qa-factory selftest: 4/4 ok ===
$ python -B ai-packages/qa-factory/scripts/tests/test_judgment_census.py
=== judgment_census: 25/25 ok ===
$ scenario_walk.py --witness-for run_suite.py detector_verdict.py red_sandbox.py probe_by_code.py import_test_receipt.py execution_scheduler.py   (81 files; each non-slow file alone, scratch driver, 60 s cap)
test_config_projection 223/223; test_delivery_ownership 310/310; test_detector_verdict 430/430; test_dispatch_identity 114/114; test_exit_gate_scope 104/104; test_exit_text_end 50/50;
test_field_producers 920/920; test_fit_targets 116/116; test_guard_big_read_sections 248/248; test_handed_to_person 58/58; test_import_test_receipt_refusal 5 passed; test_ledger 452/452;
test_manifest_put_assertion_line 20 passed; test_manual_evidence 248/248; test_probe_aggregate 19; test_probe_alternative_road 24; test_probe_by_code_languages_plan 502/502;
test_probe_by_code_languages_ts_playwright 189/189; test_probe_check_records 27; test_probe_every_check 319; test_probe_fix_round 38; test_probe_joint_judge 46; test_probe_judge_languages 7;
test_probe_marker_judgment 46; test_probe_not_proved 47; test_probe_readers 16; test_probe_replay 14; test_probe_target_fact 13; test_probe_walk 32; test_probe_walk_edges 27; test_probe_word_repeat 15;
test_reducer_supersession 91/91; test_s5_window_leftovers 148/148; test_stand_gaps 182/182; test_then_remainder 320/320 (23.3 s, the slowest); test_validator_class 51/51; test_whole_list_sites 292/292
(every rc=0, each under 24 s)
judged by the batch canon (all in slow_tests.json): test_execution_request (also holds the written W rows), test_probe_by_code, test_probe_by_code_alternative, test_probe_by_code_copy, test_probe_by_code_languages_cli,
test_probe_debt, test_probe_gap_word, test_probe_product_publish, test_red_sandbox_probe, test_red_sandbox_reports, test_red_window, test_proof_level, test_node_ids, test_story_run_*, test_scenario_*, test_stage_joints and the rest of the listed slow set
```

Negative control: `run_suite.py` `main`'s `invalid_request` print had `**told_fields(exc)` removed after a byte copy (`scratchpad/run_suite.good.py`); `test_detector_verdict.py` then printed
`FAIL t1rs road run_suite execution_request:freshness: ... expected (..., 'told', False), got (..., 'error', False)` (4 FAILs, 407/411); restored with `cp` from the copy, hashes equal:
`7bf622e48ee8ceabc11c2cbb97d9744d0375777cd0476490bcbe97727e795ce5` both (then 430/430 again).

## Questions for the Lead

1. `import_test_receipt` (text road): `refuse` prints ONE Record. With several refused checks in one request the raised Record carries the FIRST check's `expected` / `door` / `check` and the full unchanged message; the other checks stay in `exc.records` but are not printed. Options: keep (done); or print a sentence per check (changes the shape of `refuse`, T2's sink). S-2 should treat this road as carrying the first check only.
2. `red_sandbox` carries the child's `told` by copying the list from the summary (`_carry_told`), not by `told_fields`: `told_fields` takes Records/exceptions only (edge 2), and rebuilding Records from a parsed entry would need a non-literal `refusal(check, ...)`. Say if you want `told_fields` to accept a printed `told` list too.
3. The `told` key on the final `probe` / `diagnostic` dicts, the printed line of `probe_by_code.main` for a Refusal, and the probe_by_code handlers (`_run_and_judge`, walk) are written but not provoked locally (they need a full sandbox/probe: files judged by the batch canon). They count UNPROVED for S-2 (the pages keep those rows for roles whose road list includes them).
4. `execution_scheduler.main`'s own `invalid_schedule` print and `window_record.py:267` are the same class, outside this node's owns (queue).

## Needed beyond the manifest

`hooklib.py` (`_PROJECT_ROOT_CACHE`), `tests/harness.py` (`use_project`), `role_cli.py` (`run_guarded`, `refuse`), `slow_tests.json`, `scenario_walk.py` output, `onboarding_probe.py`, `window_record.py`, `execution_request.py` (`fresh_evidence`, `build_mine_request` order), `execution_scheduler.py` (`_ChildOutput`, `prepare_schedule`).
