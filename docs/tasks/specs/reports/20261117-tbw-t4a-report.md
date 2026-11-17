# TBW T4a report (t-965): guard_pre_tool + host_adapter.role_policy sites

Worktree `C:\QAFactory\forge-repo\.claude\worktrees\agent-a201e90fdcd751f88`, one commit `54e769c6`, not pushed. Builder, Sonnet. Text of every refusal byte-identical
(proof: digests below). TWO findings need a Lead decision (questions Q1, Q2): the commit leaves `refusal_registry.py --check` and one fast keep test red.

## What was done

- `guard_pre_tool.py`: every role-facing `block(<text>)` of the owned functions is `block(refusal("guard_pre_tool:PT-...", <same expression>))`, with
  `from detector_verdict import refusal` placed right before each block (a passing call pays no import: `detector_verdict` costs ~77 ms to import, measured with
  `-X importtime`). A local named `refusal` in `handoff_values_check` was renamed `problem_text` (same text, no shadowing).
- `host_adapter.py` `role_policy`: the eight HA sites likewise (`host_adapter:HA-...`).
- `tests/test_detector_verdict.py`: new `t4a_provoke`, `t4a_digest`, `T4A_OLD` and `tbw_t4a_sites` (+ ONE call line in `main()`, the only other touch: the function
  cannot run without it), inserted before `main()`.
- `changelog.d/tbw-t4a.md`: one ASCII bullet.

## Site table (function | fragment | id | row | proof)

Proof: F = proved fast (`tbw_t4a_sites` row, run, real `hooklib.block`: stderr = old text + `expected:`/`door:` of the row + `check:` last + TRAPPED; the old text by digest of the pre-change stderr).

| function | fragment | id | test row | proof |
|---|---|---|---|---|
| size_check | command over 64 KB | PT-command-size | size | F |
| runs_check | direct test launch, two messages (FV1-27 row 2: `playwright test`) | PT-direct-test-run | direct run, playwright test | F |
| git_config_check | git config change | PT-git-config | git config | F |
| logs_check | heavy evidence log, Read and shell (2 sites) | PT-logs | logs Read, logs shell | F |
| plugin_read_check | plugin read by a role | PT-plugin-read | plugin read | F |
| big_read_check | whole read over the cap | PT-big-read | big read | F (text-only; see Q2) |
| case_store_check | case outside `cases_root` | PT-case-store | case store | F |
| handoff_write_check | rewrite of a form / edit under a waiting values file / write of a code trace (E-T4a-2: three functions-in-one, three row ids, one site each) | PT-handoff-rewrite, PT-handoff-edit-pending, PT-handoff-code-file | handoff rewrite, handoff edit pending, handoff code file | F |
| handoff_values_check | values leave the form not ready (FV1-27 row 11) | PT-handoff-values | handoff values (`values_report`/`refusal_text` patched: the row proves the site, not the form contract) | F |
| artifact_rewrite_check | whole Write over an artifact with `rewrite` | PT-artifact-rewrite | artifact rewrite | F |
| plan_write_check | json plan / md plan (2 sites) | PT-plan-rewrite, PT-plan-md-rewrite | plan rewrite, plan md rewrite | F |
| manifest_write_check | manifest with entries | PT-manifest-shrink | manifest shrink | F |
| owner_check | story artifact / project ledger (2 sites) | PT-owner | owner story, owner ledger | F |
| window_file_check | claimed test file (`_window_refusal` text wrapped at the block, not inside the helper) | PT-window-file | window file | F |
| writes_check | declared command / tracker verb / api method (3 sites) | PT-external-writes | external writes (one of the three; same wrapper) | F, 2 siblings N |
| human_word_check | a person's word recorded by a role | PT-human-word | human word | F |
| config_write_check | role writes config.json | PT-config-write | config write | F |
| stand_record_write_check | role writes a stand record | PT-stand-record-write | stand record | F |
| walker_refusal | WalkerError | PT-walker-error | walker | F |
| _guard | unchecked patch | PT-patch-unchecked | patch unchecked (real malformed patch) | F |
| main | unparsed event (`read_event` returns None) | PT-unparsed-event | unparsed event | F |
| role_policy | transport refusal dict | HA-call-shape | call shape | F |
| role_policy | no command text | HA-no-command-text | no command text | F |
| role_policy | Agent/Task by a role | HA-role-nested-delegation | nested delegation | F |
| role_policy | role without shell, not one plain read | HA-role-read-only | role read only | F |
| role_policy | write_stdin chars | HA-stdin-chars | stdin chars | F |
| role_policy | exec_command tty | HA-exec-tty | exec tty | F |
| role_policy | connector, no-shell role / other caller | HA-connector-unclassified, HA-connector-orchestrator | connector no shell, connector orchestrator | F |

No-row sites left bare (E6, item 4): `_guard` doctor probe `QA FACTORY DOCTOR: expected harmless deny probe` (class code, probe, E5); `role_policy` `FACTORY DOCTOR: the context
diagnostic must return its challenge without tools` (class code, probe). No (role) residual in the owned functions. `stage_joints` rows 33-37 already carry the wave0 8a
"On Codex" sentences (read from stage-joints.json :2499-2660), so item 8a needed no row edit (rows are a non-goal). Sites in unowned helpers of the files (`_split_off_*`, `_segments`,
`_shell_words`, ..., `patch_operations`, `normalize`, ...) are parser/internal raises, not role-facing blocks, left as they are.

## Counters

- `stage_joints.py --check` BEFORE `told counters: hand_cards 12, legacy_legs 0, unsited 119`, AFTER the same (`unsited 119`): the 32 T4a rows are already sited through A24 `check_of`
  (spec §0), so `unsited` cannot move for this node; `told_ratchet.unsited` and the K12 pin untouched (F-1 (a)).
- Wide scan of the two files after the change (`refusal_registry.sites` with `raise_family(wide=True)`): guard_pre_tool sourced 28, bare 24; host_adapter sourced 8, bare 21. The bare ones
  are inside the helper/parser functions named above plus the two doctor probes (`_guard` 1, `role_policy` 1). The baseline of the told-ratchet units (guard_pre_tool bare 29)
  is the integrator's/closing's to reset; I did not edit `told-ratchet.json`.
- Census: no new blocking unit (no function added, no `block` added or moved; the only new function bodies are the test helpers).

## Verbatim witness

```
$ python -B ai-packages/qa-factory/scripts/tests/test_detector_verdict.py
=== test_detector_verdict: 570/570 ok ===                      (35 rows x 3 checks of tbw_t4a_sites among them)
$ python -B ai-packages/qa-factory/scripts/stage_joints.py --check
stage joints: walked exit 8, detector 5, window 27 | rows 267, gaps 4 (producer 2, told 1, demands 1), joints held 4 of 267 | role leg not walked (code-to-code rows): 26 | stages with no detector: S0, S1, S6, S7, S9 | told counters: hand_cards 12, legacy_legs 0, unsited 119
stage joints: clean
$ python -B ai-packages/qa-factory/scripts/selftest.py --limits --lang
PASS limits: SKILL.md / agents / references within size caps
PASS limits: every mandatory role rule of design/role-rules.json holds in its carrier
=== qa-factory selftest: 4/4 ok ===
$ scenario_walk.py --witness-for guard_pre_tool.py host_adapter.py tests/test_detector_verdict.py   (45 files printed; each non-slow, non-quarantined file alone, scratch runner, 60 s cap)
test_artifact_supersede 71/71; test_codex_tool_guidance 217/217; test_doctor_access OK; test_fixes_13797 70/70; test_guard_big_read_sections 247/248 RED (Q2); test_guard_command_text 197/197;
test_guard_project_knowledge 10/10; test_guard_window_files 103/103; test_refusal_registry 524/528 RED (Q1); test_s5_window_leftovers 148/148; test_source_stage_integration rc=0;
test_conductor_stop 48/48; test_cost_capture_settled rc=0; test_cost_capture_start_turn rc=0; test_dispatch_liveness 441/441; test_exit_gate_digest_source 94/94; test_exit_text_end 50/50;
test_host_adapter 95/95; test_resume_story_isolation 310/310; test_role_policy_reads 198/198; test_detector_verdict 570/570 (run above)
judged by the batch canon (slow_tests.json / quarantine / scenario): test_branch_accounting, test_brief_pack, test_brief_pack_s5_plan, test_codex_hooks_matchers, test_codex_host,
test_controller_rework_scope, test_doctor_context, test_guard_dispatch_budget_and_logs, test_guard_write_owners, test_hooklib_scan, test_hooks_wiring, test_judgment_census, test_profile_reader,
test_protected_test_path, test_resolver, test_run_forms, test_stage_guard, test_test_locations, test_words_carry and the three test_scenario_* (full list in /scratchpad witness_out.txt)
```
Output of the two reds, verbatim heads:
```
$ python -B ai-packages/qa-factory/scripts/refusal_registry.py --check
A24 refusal registry: VIOLATIONS (68)  owner: factory - nothing wanted from you
  - guard_pre_tool.py:320 (size_check): the refusal `refusal('guard_pre_tool:PT-command-size', SIZE_MSG.format(si` is not in refusal_registry.REGISTRY - say what it refuses, ...
  (36 sites "not in REGISTRY" + 32 entries "the entry is stale")
$ python -B ai-packages/qa-factory/scripts/tests/test_guard_big_read_sections.py
FAIL IM-g a role with a shell: the door names ticket_adapter.py inspect with cause too_large, not Grep -n - 'PRE-TOOL GUARD: reading .../huge whole is blocked ... This is a picture: it cannot be read in parts ... do not try `offset`/`limit`.\nWith a shell: python ".../ticket_adapter.py" inspect ...' (the assertion `"Grep -n" not in text` now fails)
=== test_guard_big_read_sections: 247/248 ok ===
```

## Negative control (byte copy, cp, equal hashes)

`guard_pre_tool.py` byte-copied to the scratchpad BEFORE the corruption (sha256 `ae9cb74765d3609eafef58b97a9c0145a935e0027cb82270a82bbe2e9c4c3773` both); `PT-git-config`'s
`block(refusal(...))` turned bare; `test_detector_verdict.py` then printed `FAIL t4a git config guard_pre_tool:PT-git-config: the row's lines follow the problem, ... TRAPPED closes`
and `=== test_detector_verdict: 569/570 ok ===`; `stage_joints.py --check` still `unsited 119` (the row is sited by A24, the S-1a "unsited rises by 1" does not apply to T4a, measured);
restored by `cp` FROM the copy: hashes equal `ae9cb747...4c3773`, test 570/570 again.

## How the old text was captured

Byte copies of the two pre-change files (`guard_old.py` sha256 `ca4ed954...299297`, `host_old.py` sha256 `d8abf98e...a0c34`) were loaded as separate modules and the SAME provocations
(`t4a_provoke`) ran over them; `T4A_OLD` holds the 16-hex digest of each row's stderr problem text (trailing white space cut as `block` cuts it; the temporary and plugin roots written
`<ROOT>`/`<PLUGIN>`). The new files give the same digest on all 35 rows. Digests, not literals: 35 texts of 400-3000 characters would have been the bulk of the test (tests-over reason in the commit).

## FR walk

- A: FR-1/2 text and doors unchanged, `expected`/`door` added after them; FR-59/AR-28 an unreadable row prints the factory-defect sentence (S-1a row, shared constructor), checked by the shared `refusal()` tests; FR-4/57 n/a (no gate added); FR-57 door of a ban unchanged.
- B: not touched (no text a person reads changes; TRAPPED stays the last line). C: FR-14 output shape additive (`expected:`/`door:`/`check:` lines between the text and the TRAPPED line, by `hooklib.block`'s existing Record path); FR-38/49 n/a here.
- D: FR-16 literal ids at the sites (scanner counts `sourced` 28 + 8). E, F: not touched. G: FR-30 English/ASCII (`selftest --lang` green), FR-31 no timing test, FR-32 root cause = the one constructor, FR-54 siblings below.
- AR: AR-9 (the row's door rides the refusal), AR-10 (the row sentence repeats at the refusal), AR-13 (`refusal()` the only reader of the rows), AR-18 (one output shape), AR-29 (no judgment moved).

## Questions for the Lead (not decided, left as found)

Q1 (A24 registry, blocks `refusal_registry.py --check`, `test_refusal_registry`, and `selftest` A24 in the canon): `refusal_registry.sites()` keys a site by `ast.unparse(args[0])` of the `block(...)` call and an entry matches by PREFIX
(`_covers`, `refusal_registry.py:1705`). After `block(refusal("<id>", <text>))` the key starts with `refusal('guard_pre_tool:...`, so 36 sites are "not in REGISTRY" and 32 entries are "stale" (68 violations; the spec's
AR-9 check "`refusal_registry.py --check` green" is not met). `refusal_registry.py` is not in my owns and the cards do not mention it. Options: (a) one change in `_key_text` (and the same for `deny`): when `args[0]` is a `refusal(<id>, X)` call key on `X`
(one place, covers T4a, T4b and every later site; probe on a scratch copy: `findings()` 68 -> 0, `scratchpad/a24_probe.py`); (b) rewrite the `call` of each of the ~32 A24 entries to `refusal('<id>', <old call>` (data, 32 edits, T4b's stage_guard entries conflict).
Recommendation: (a). The same applies to T4b (`stage_guard`, `inject_context`).

Q2 (`test_guard_big_read_sections.py` IM-g, fast keep file, red): the row `guard_pre_tool:PT-big-read` has the door "`Grep -n` for the line, then Read with offset/limit; a PDF by `pages` ranges", and the transport now prints it after the text
of EVERY big-read refusal, including the picture branch whose own door says "it cannot be read in parts ... do not try `offset`/`limit`" (and the PDF branch). The printed refusal contradicts itself and the old assertion `"Grep -n" not in text`
fails. A sentence-vs-body mismatch (EC-8 class); the row is stage-joints data (non-goal) and the test is not owned. Options: (a) split the row by sub-id (`PT-big-read.picture`, `.pdf`) with their own doors, site picks the sub-id by branch (rows are T1r-cards' file: a node for it);
(b) leave the row and change the IM-g assertion (its owner); (c) keep as is and name the contradiction. No code of mine decides it.

## Bare remainder / siblings (rule 5)

- Same class, other files: T4b (`stage_guard`, `hooklib.block`, G-dispatch units): the A24 key problem Q1 applies there identically.
- The same row-door/branch contradiction as Q2 may exist where one row has several branches with different doors: `PT-logs` (Read vs shell: the row door names `run_suite.py --request ... --detail` "with a shell"), `PT-owner` (story vs project ledger: row door is `controller.py --operation rework`, the ledger branch names the same). Not tested for contradiction here; queue for the critic.
- `guard_pre_tool.selftest` (`--selftest`) holds an inline local named `refusal` (a string); untouched.
- Per-unit told-ratchet baselines (`guard_pre_tool.py::*`, bare 29) are not edited (non-goal); the measure is in the Counters section.

## Deviations from the spec

- One extra line in `test_detector_verdict.py` `main()` (the call of `tbw_t4a_sites`); the spec said "touch nothing else".
- Digests instead of text literals for the old text (reason above).
- `handoff_values` row patches `handoff_check.values_report` / `refusal_text` (the real form contract world is the slow `test_handoff_values_refusal`, canon).
- `unsited` does not move (spec's DoD (2) expected "the lowered `unsited`" for siting nodes; T4a's rows are sited already).

## Needed beyond the manifest

`ai-packages/qa-factory/scripts/refusal_registry.py` (`sites`, `_key_text`, `_covers`, `findings`), `hooklib.py` (`block`, `TRAPPED`), `detector_verdict.py`, `references/stage-joints.json` (rows),
`references/artifact-writers.json`, `tests/test_guard_write_owners.py`, `tests/test_guard_window_files.py`, `tests/test_codex_tool_guidance.py` (fixtures), `tests/harness.py`, `scripts/slow_tests.json`, `test-layers.json`.

## Round 2 (Lead answers to Q1, Q2; one new commit on top of 86ce4caf)

- Q1 done: `refusal_registry.py` `_key_text` only: a first argument `refusal("<literal id>", X)` (two or more arguments, literal str id) is keyed by X; any other shape keeps today's key.
- Q2 done: bare site: guard_pre_tool big_read_check:~896, picture/PDF branch - needs its own row id (row split), queue to T1r-cards-R. The text-file branch of the same function stays `refusal("guard_pre_tool:PT-big-read", ...)`.
- Verbatim witness after the change:
```
$ python -B ai-packages/qa-factory/scripts/tests/test_refusal_registry.py       => === test_refusal_registry: 528/528 ok ===
$ python -B ai-packages/qa-factory/scripts/tests/test_guard_big_read_sections.py => === test_guard_big_read_sections: 248/248 ok ===
$ python -B ai-packages/qa-factory/scripts/tests/test_detector_verdict.py       => === test_detector_verdict: 570/570 ok ===
$ python -B ai-packages/qa-factory/scripts/refusal_registry.py --check          => A24 refusal registry: no violations (rc=0; was 68 violations)
$ python -B ai-packages/qa-factory/scripts/stage_joints.py --check              => ... told counters: hand_cards 12, legacy_legs 0, unsited 119 / stage joints: clean
$ python -B ai-packages/qa-factory/scripts/selftest.py --limits --lang          => === qa-factory selftest: 4/4 ok ===
```
No test row added to test_refusal_registry (its existing rows are green; the unwrap is proved by the 68 -> 0 of `--check`).
