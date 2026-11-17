# T4b report (t-1031) - stage_guard sites, hooklib, G-dispatch census relabels

Branch `worktree-agent-ad26d38b91588bc3c`, code commit `711d0c3b` (this report is the next commit). Builder, Sonnet. Refusal text changed by no byte.

## What was done

- `stage_guard.py`: the role-facing command refusals write their row id through `DV.refusal("<id>", <same text>)`. `rule_typed_runner` writes `SG-command.opaque`;
  `_judge_slice` writes `SG-command.typed_runner` (region, no request path) and `SG-command.request` (file missing / unreadable, empty `requests`,
  other dispatch id, selection not a list, outside scope). `check_command` writes the ids of the helpers that have several callers (EC-2): `rule_pathspec`
  -> `SG-command.commit.pathspec`, `rule_manifest` -> `SG-command.commit.manifest` (row 28 as two sub-ids), `rule_stash` -> `SG-command.stash`,
  `rule_delivery` -> `SG-command.delivery`. Same decisions for every input: the `message or ...` chain became two `if` returns in the same order.
- The runner's Record carries its id through the `f"{ticket}: {message}"` prefix by `message.check` (a field, never the words) read in `check_command` and
  re-written as a literal `DV.refusal` at the call (three branches, one literal each). First attempt (`DV.Record(...)` copy into a variable) turned
  `test_refusal_registry` red (the registry keys `deny(<first arg>)` by its source text: "the refusal `told` is not in REGISTRY"); the literal form is green (533/533).
- `hooklib.py`: NOT edited. `shell_opaque_found` / `_opaque_member` / `_DOOR_*` return `(what, door)` strings and have TWO callers with different requirements
  (`stage_guard.rule_typed_runner`, row 25; `host_adapter` read-only command check, row 35), so by EC-2 the id is on the caller. Byte hash equal to the pre-change copy
  (`af3d70da450d87d6...`). The backslash instance of FV1-27 (row 25) is the first site (`rule_typed_runner`).
- Census: 12 G-dispatch rows -> `roles: ["conductor"]` + `note: "dispatch-time unit: no role's tool line reaches it (mech §2.8, T0 M8)"`:
  stage_guard `check_dispatch`, `_check_exploration`, `check_resume`, `_unidentified_resume`; inject_context `collect_blocks`, `refuse_native_packet`, `refuse_native_stage`,
  `map_problems`, `refuse_receipt`; native_context `stage` and codex_roles `check_override`, `export` (these three already `["conductor"]`: note only). The set is the spike's
  "first set" (`reports/20261113-told-before-work-spike.md` M8, lines 159-168).
- Test: ONE new function `tbw_t4b_sites` (+ its registration line in `main`) in `test_detector_verdict.py`: 13 rows driven through the REAL `check_command` and `deny`,
  expected ids/sentences from `stage-joints.json` rows (`SJ.row_for`), old text as a sha256 digest captured by running the same rows over a byte copy of `stage_guard.py`
  taken before the edit, plus controls (three allowed commands print nothing; the walker's door prints no `check:`).
- Changelog `changelog.d/tbw-t4b.md`.

## Site table

Proof: F = proved fast in `tbw_t4b_sites` (run).

| function | fragment | id / E6 reason (class) | test row | proof |
|---|---|---|---|---|
| rule_typed_runner | the command holds {what}, which the shell reads differently from this guard | stage_guard:SG-command.opaque | opaque | F |
| _judge_slice | region (`REGION_REFUSAL`) | stage_guard:SG-command.typed_runner | typed_runner region | F |
| _judge_slice | legacy --task/--label and the default full suite | stage_guard:SG-command.typed_runner | typed_runner no path | F |
| _judge_slice | typed run request is unreadable: FileNotFoundError | stage_guard:SG-command.request | request missing file | F |
| _judge_slice | typed run request is unreadable: <ExcName> | stage_guard:SG-command.request | request unreadable | F |
| _judge_slice | typed schedule requires a non-empty requests array | stage_guard:SG-command.request | request no requests | F |
| _judge_slice | RunRequest dispatch_id does not match | stage_guard:SG-command.request | request other dispatch | F |
| _judge_slice | selected instances exceed the scope (not a list) | stage_guard:SG-command.request | request selection not a list | F |
| _judge_slice | selected instances exceed the scope: <ids> | stage_guard:SG-command.request | request outside scope | F |
| check_command (caller of rule_pathspec) | -a/--all; names no files | stage_guard:SG-command.commit.pathspec | commit pathspec | F (-a text; "names no files" text same wrapper) |
| check_command (caller of rule_manifest) | committing test code: unresolved cases | stage_guard:SG-command.commit.manifest | commit manifest | F (helper stubbed: its body is not under test) |
| check_command (caller of rule_stash) | takes everything / `--` without path / names qa-factory | stage_guard:SG-command.stash | stash | F (takes-everything text; the others same wrapper) |
| check_command (caller of rule_delivery) | delivery form before gate B | stage_guard:SG-command.delivery | delivery | F |
| rule_pathspec / rule_stash / rule_manifest / rule_delivery bodies | all their texts | no literal id inside (EC-2: other callers `dispatch_errors`, `repo_words.py`, tests) (code) | - | - |
| check | `WALKER_DOOR` deny | bare: row 31 is a pointer to PT-walker-error (spec); see question 1 (code) | control row: no `check:` line | F |
| check_dispatch (9 sites), _check_exploration (5), check_resume (3), _unidentified_resume (1) | G-dispatch refusals | bare: no row, mech 5.3 "No row (E5)" SG-resume-*, SG-probe-*, SG-ambiguous-task, SG-explicit-no-story, SG-explore-*, SG-unreadable-pipeline, SG-role-stage-unset, SG-stage-rules, SG-manifest-unread (code, dispatch-time, conductor road) | - | - |

## E6 list of the bare remainder of stage_guard (class)

- (code) the four dispatch-time functions above and their helpers `dispatch_errors`, `rule_order`, `rule_gate_a`, `rule_awaiting_code`, `rule_tracker_route`, `rule_gate_ordered`
  (SG-stage-rules, SG-tracker-route, SG-manifest-delivery, SG-gate-ordered: G-dispatch, no row). Their census rows still list the 12 roles (see question 2).
- (code) `rule_pathspec`, `rule_stash`, `rule_manifest`, `rule_delivery` bodies, bare inside (their other callers: dispatch gate, `repo_words.py`).
- (code) `check` walker deny (row 31 pointer).
- (role) none found: every refusal a role's Bash call can meet from the stage guard has a row id.

## Census rows relabelled and ceilings (old -> new)

Rows: the 12 listed above. `blocking_per_role`, computed by `test_judgment_census.analyse` over the real package (the test file itself is slow and was not run; the script only
calls `analyse` and prints its C3 lines; before my edit: no problem, equal to the ceilings of main, qa-case-critic 157 already):

qa-automator 176 -> 167, qa-bug-reporter 141 -> 132, qa-case-critic 157 -> 148, qa-case-designer 145 -> 136, qa-code-critic 147 -> 138, qa-doc-scribe 137 -> 128,
qa-failure-analyst 149 -> 140, qa-requirements-tester 162 -> 153, qa-retro-analyst 142 -> 133, qa-runner 146 -> 137, qa-scout 138 -> 129, qa-test-strategist 173 -> 164 (each -9, a shrink);
conductor 748 -> 748 (its rows already held it). No ceiling raised. After the edit `analyse` printed no C1-C5 problem: `blocking_units 870 units 1264` before and after
("census: no new blocking unit": no unit created, none flipped).

## Counters

`stage_joints.py --check`: `unsited 46` before (pre-change `stage_guard.py` put back for the run, restored, hashes equal) and `unsited 46` after. Rows sited by a literal id: the 7 ids
above (`SG-command.opaque`, `.typed_runner`, `.request`, `.commit.pathspec`, `.commit.manifest`, `.stash`, `.delivery`). I did not touch `told_ratchet.unsited` or the K12 pin. DIVERGENCE from DoD (4): the
count does not move, because `stage_joints.sited_ids` already counts a sub-id of an A24 id as sited (`stage_guard:SG-command` is an A24 entry), so the 7 rows were never in the 46; the
negative control below shows the test row failing and `unsited` staying 46.

## FR walk

A: FR-1/2 text unchanged, expected/door added by the Record (the door of each row is the shell's: `door_needs shell`, rows `when: shell`); FR-59 unreadable row -> the factory-defect sentence (the
`unreadable` row of `test_detector_verdict`, EC-4); FR-4/57 n/a no gate added. B: not touched. C: FR-14 stderr shape additive (`expected:`/`door:` after the problem, `check:` last, EC-6); FR-38 n/a (pages are T1r).
D: FR-16 the id is a literal at the site. E, F: not touched. G: FR-30 `selftest --lang` green, FR-32 root fix in the sites, FR-54 siblings below.
AR: AR-9 (rows' expected/door ride with the refusal), AR-13 (`told_text` through `refusal()` only), AR-18 (`check:` last), AR-20 (ceilings only lowered), AR-29 (no judgment added or moved; the `message.check` read is a field, not a text).

## Rows that over-claim (EC-8; not edited)

- `stage_guard:SG-command.stash`: sentence "A `git stash` names its paths." UNDER-claims: `rule_stash` also refuses a stash that names `qa-factory/` among its paths (the wave0 8b corrected sentence had it; the shipped row dropped it), and the door "name the paths" does not say to leave qa-factory out.
- `stage_guard:SG-command.opaque`: "a command that launches the runner" - the body judges every command that MENTIONS the runner (the hint gate), a `grep ... run_suite.py "a\(b"` is refused too (the sentence is narrower than the body).
- No sentence over-claims the body: 26, 27, 28 (both), 30 read as the bodies do (row 30's "before gate B" not re-read against all `rule_delivery` branches).

## Verbatim witness

```
$ python -B ai-packages/qa-factory/scripts/tests/test_detector_verdict.py
=== test_detector_verdict: 802/802 ok ===        (57 `PASS t4b ...` lines of it)
$ python -B ai-packages/qa-factory/scripts/stage_joints.py --check
stage joints: walked exit 8, detector 5, window 27 | rows 267, gaps 4 (producer 2, told 1, demands 1), joints held 4 of 267 | role leg not walked (code-to-code rows): 26 | stages with no detector: S0, S1, S6, S7, S9 | told counters: hand_cards 12, legacy_legs 0, unsited 46
stage joints: clean
$ python -B ai-packages/qa-factory/scripts/selftest.py --limits --lang
PASS limits: SKILL.md / agents / references within size caps
PASS limits: every mandatory role rule of design/role-rules.json holds in its carrier
=== qa-factory selftest: 4/4 ok ===
$ python -B scripts/tests/test_refusal_registry.py     (needed: the registry keys deny() by source text)
=== test_refusal_registry: 533/533 ok ===
$ python -B scripts/tests/scenario_walk.py --witness-for scripts/stage_guard.py scripts/hooklib.py scripts/tests/fixtures/judgment-census.json scripts/tests/test_detector_verdict.py   (87 files)
 fast, each alone (39 files, `python -B scripts/tests/<f>` from the package dir, second run after the last edit): 39/39 exit 0 -
 test_adapter_forms 449/449, test_case_id_form 514/514, test_check_witness 34/34, test_codex_tool_guidance 217/217, test_config_projection 223/223, test_controller_doors 31/31,
 test_cost_capture_settled 159/159, test_detector_verdict 802/802, test_dispatch_liveness 441/441, test_exit_gate_scope 106/106, test_exploration_identity 66/66,
 test_gate_ordered_reporter 89/89, test_gate_vocabulary 141/141, test_guard_big_read_sections 248/248, test_guard_command_text 197/197, test_guard_project_knowledge 10/10,
 test_guard_window_files 103/103, test_hook_lifecycle 25/25, test_hooklib_append_jsonl 10/10, test_human_questions 651/651, test_interim_packet 54/54, test_ledger 452/452,
 test_manifest_projection 182/182, test_oracle_provenance 296/296, test_package_identity 47/47, test_project_knowledge (pytest) 157 passed, test_reference_window 85/85,
 test_refusal_registry 533/533, test_resume_story_isolation 310/310, test_scenario_walk 95/95, test_scenario_world 33/33, test_source_stage_integration 21/21,
 test_stage_of_dispatch 17/17, test_stages 133/133, test_stand_gap_remedy 34/34, test_stand_gaps 182/182, test_test_files 190/190, test_whole_identifier 166/166, test_whole_list_sites 292/292
 judged by the batch canon (48 files, all in slow_tests.json): test_stage_guard, test_run_forms, test_hooklib_scan, test_judgment_census, test_stage_joints, test_guard_dispatch_budget_and_logs,
 test_gate_preflight, test_check_delivery, test_codex_host, test_execution_request, test_scenario_cart_1/dry_1/local_1_0108/local_1_arm_b, and 34 more of the walk's list
```

The first full fast pass (before the last edit) had `test_refusal_registry 530/533`, the red named above; fixed, second pass all green.

Negative control (DoD 4): byte copy of `stage_guard.py` taken first (`sha256 fecd0c43...`); `check_command`'s `stash` site turned bare (`deny(f"{ticket}: {message}")`): `test_detector_verdict` printed
`FAIL t4b stash stage_guard:SG-command.stash: the row's lines follow the problem, `check:` last` (801/802); `stage_joints.py --check` still `unsited 46` (divergence above); restored with `cp`,
hashes equal `fecd0c439655d1ad5c0f59b911197ccc6719626da4e0d8851f19d19bad349675` both. (That copy predates the last edit of `check_command`; the final file was re-run green: 802/802, registry 533/533, stage_joints clean.)

## Questions for the Lead

1. Row `stage_guard:SG-walker-error` exists in `stage-joints.json` (rows+page+call told) but the spec says row 31 is a pointer and has no site: `check`'s `deny(hooklib.WALKER_DOOR...)` stays bare. If the row should be sited, it is one line in `check` (`DV.refusal("stage_guard:SG-walker-error", ...)`, owned). Which?
2. The spike's "first set" (what I relabelled) leaves `dispatch_errors`, `rule_order`, `rule_gate_a`, `rule_awaiting_code`, `rule_tracker_route`, `rule_gate_ordered`, `explain` (all G-dispatch in the E5 list) with 12 roles in the census; `rule_tracker_route` and `rule_gate_ordered` have `check_dispatch` as the only caller. Relabel them too (lowers the ceilings further)?
3. Row 29 sentence under-claim (above): T1r-cards-R input.
4. The pre-commit regenerated `docs/OWNER_PRINCIPLES_INDEX.md` (left unstaged, dirty in the worktree, per the dispatch) - the index looks stale on main, not a T4b matter.

## Analogs noticed (not widened)

- `host_adapter.py:541` and `hooklib.shell_opaque_found` are the same shell-opaque ban for the read-only-role reader (row 35): sited by T4a on its own id.
- `repo_words.py:187` calls `stage_guard.rule_pathspec`/`rule_stash` for a person text: a third caller, bare.
- `guard_pre_tool.walker_refusal` (PT-walker-error) and `stage_guard.check` use the same `WALKER_DOOR`: two sites, one text, two ids (T4a / row 31).

## Needed beyond the manifest

`PKG/scripts/refusal_registry.py` (`_key_text`, `SG-command` entry; the first attempt failed `test_refusal_registry`), `PKG/scripts/stage_joints.py` (`sited_ids`, `check_ids`), `PKG/scripts/tests/test_refusal_registry.py`,
`PKG/scripts/tests/test_judgment_census.py` (`analyse`), `PKG/scripts/host_adapter.py` (:541 caller), `PKG/references/stage-joints.json` (rows), `docs/tasks/specs/reports/20261113-told-before-work-spike.md` (M8), the wave0 rows file (8b), `PKG/scripts/slow_tests.json`.
