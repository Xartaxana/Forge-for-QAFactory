# K10 pay-down, card K1b r3: flip the proof constants after the canon (builder report, t-1120, node FV2-79)

Worktree `C:\QAFactory\forge-repo\.claude\worktrees\agent-a9f89661be4c45267`, branch `worktree-agent-a9f89661be4c45267`, base 43eb3811. Card: `docs/tasks/specs/20261117-tbw-k1b-card-r3.md` (forks F1-F5 = (a)).

## What was done (items 1-8)
1. `unproved_site` = `{execution_request:stand, run_suite:begin}` (`selector_args`, `window_first` removed).
2. `test_t1rs` constants: `road_token` (ONE dict of road -> agent-file token, read by `T1rs/roads-of-role`), `roads_of` with the mode split (F4 a), `PROVED_ROAD`, `CARRIED`, `L_SITE`, `carries`, `proved`; the S1 = A sentence is in the comment verbatim.
3. 30 markers flipped (list below); entries joined/split/flipped by the card's rule (script run once, deterministic, `json.dumps(indent=2)` round-trip of the untouched file was byte-equal first).
4. New rows `T1rs/l-site-keeps-page/<road>/<role>`, `T1rs/unproved-road-keeps-page/<road>/<role>`, `T1rs/road-carries/<road>`; `partial-split` expected list now `[False, key not in unproved_site, False, key not in unproved_site]`; `counted`, `n_er`, `n_rs` and the `(31, 31)` literal removed (`T1rs/rows` = unique ids; index-line/door-words rows run on `len(own)`).
5. `contract_slices.py --write` then `--check`; `stage_joints.py --check`.
6. Pin `T3a (j)`: a join (`RL.settings` patched for the call to return the real settings with `native_headroom: {}`; roles named "the plugin share is" = keys; any other line fails; message counts the keys: "its 3 roles over H stand at their named baselines").
7. Ratchets (below). 8. Changelog fragment `ai-packages/qa-factory/changelog.d/tbw-k10-paydown-k1b.md`.

## Canon lines each proof rests on (attached input, Lead decisions section; run 44068480897)
- success; `full / package-full (1)` 133988524640 success, `(2)` 133988524751 success; no FAIL line matches `K10p/` or `T1rs ` in either shard; a failed file fails its job. So `test_probe_by_code.py`, `test_red_sandbox_probe.py`, `test_execution_request.py` are file-level green (C7).
- `selector_args` / `window_first` removed from `unproved_site`: `test_execution_request.py` file-level green (rows `T1rs selector_args`, `T1rs window_first`).
- `PROVED_ROAD["red_sandbox.diagnostic"] = "pass-through"`: `test_red_sandbox_probe.py` file-level green (`K10p/rs-told-passes-through/diagnostic/*`).
- `PROVED_ROAD["import_test_receipt"] = request`: `test_import_test_receipt_refusal.py` run by me, 7 passed (below) (`K10p/import-prints-every-check/*`).
- `probe_by_code`, `red_sandbox.probe`: empty, no canon line needed (S1 = A, L sites; F4).
- E-canon check: the three §0 fixes are in my tree: `ToolRefusal.__init__(self, message="", *records, name_unproved...)` `probe_by_code.py:225`; `dispatch="S7-qa-failure-analyst-1"` `test_red_sandbox_probe.py:995`; `"case": "TC-001"` `test_execution_request.py:2189-2190`.

## Ids per road (constants)
- `import_test_receipt`: proved = the 11 `request` ids (carries only those).
- `red_sandbox.diagnostic`: pass-through; carried = all 31 ids except `run_suite:phantom_story`, `:recover`, `:reparse` (file:line reasons in the comment).
- `red_sandbox.probe`: proved empty; carried same set as diagnostic; L_SITE = same set.
- `probe_by_code`: proved empty; carried = L_SITE = every `execution_request:*` id (14 held by the critic), no `run_suite:*`.

## Marker old -> new per (row, role) (all page -> call; "how" = entry edit)
```
execution_request:purpose | qa-automator | page | call | flipped in place
execution_request:selection | qa-automator | page | call | flipped in place
execution_request:budget | qa-automator | page | call | flipped in place
execution_request:freshness | qa-automator | page | call | flipped in place
execution_request:runtime | qa-automator | page | call | flipped in place
execution_request:fingerprint | qa-automator | page | call | flipped in place
execution_request:command | qa-automator | page | call | flipped in place
execution_request:execution | qa-automator | page | call | flipped in place
execution_request:selector | qa-automator | page | call | flipped in place
execution_request:instance_contracts | qa-automator | page | call | flipped in place
run_suite:phantom_story | qa-code-critic | page | call | joined
run_suite:phantom_story | qa-failure-analyst | page | call | joined
execution_request:sandbox | qa-failure-analyst | page | call | split
execution_request:place_rows | qa-failure-analyst | page | call | joined
execution_request:active_dispatch | qa-failure-analyst | page | call | joined
execution_request:case_entries | qa-failure-analyst | page | call | joined
execution_request:profile | qa-failure-analyst | page | call | joined
execution_request:profile_command | qa-failure-analyst | page | call | joined
execution_request:stand.probe | qa-failure-analyst | page | call | joined
execution_request:stand.reference | qa-automator | page | call | joined
execution_request:stand.reference | qa-failure-analyst | page | call | joined
execution_request:mine_call | qa-failure-analyst | page | call | joined
execution_request:scope | qa-failure-analyst | page | call | joined
execution_request:no_test | qa-failure-analyst | page | call | joined
execution_request:selector_args | qa-runner | page | call | split
execution_request:selector_args | qa-failure-analyst | page | call | joined
execution_request:window_first | qa-automator | page | call | split
execution_request:window_first | qa-runner | page | call | joined
execution_request:window_first | qa-failure-analyst | page | call | joined
run_suite:recover | qa-code-critic | page | call | joined
30 changes
```
Divergence from the card's §1 estimate: the automator's `stand.reference` and `window_first` leave too (the test decides: `stand.reference` is in `request`, proved on both roads; `window_first` is not carried by `import_test_receipt`, proved on `run_suite`). Runner `stand.reference`... n/a (not held). The code-critic's ER rows all stay (L sites), as estimated.

## U per role, before / after (U-CMD; bytes)
```
before                        after
qa-scout 46336                46336
qa-requirements-tester 36330  36330
qa-test-strategist 53739      53739
qa-case-designer 39828        39828
qa-case-critic 62574          62574
qa-automator 79906            76472
qa-code-critic 73134          72717
qa-runner 52618               51871
qa-failure-analyst 66553      61126
qa-bug-reporter 45575         45575
qa-doc-scribe 57743           57743
qa-retro-analyst 42829        42829
```
`role_load.py --all --json` tokens / process tokens before -> after: automator 25683/24116 -> 24824/23257; code-critic 23073/21250 -> 22969/21146; runner 18528/16919 -> 18341/16732; failure-analyst 22286/20261 -> 20930/18905; the other 8 roles unchanged.

## Ratchet rows old -> new (all down; no raise)
- `process_ratchet_tokens`: qa-automator 24116 -> 23257; qa-code-critic 21250 -> 21146; qa-runner 16919 -> 16732; qa-failure-analyst 20261 -> 18905.
- `ratchet_tokens` (excess > 1000 slack): qa-automator 26053 -> 24824; qa-failure-analyst 22442 -> 20930 (code-critic 23394 vs 22969 and runner 18906 vs 18341 are within slack, unchanged).
- `native_headroom`: qa-automator 79909 -> 76472; qa-test-strategist 53739 unchanged; qa-code-critic 73134 -> 72717.
- `native_headroom.qa-code-critic: lowered to 72717 (E7)`. U 72,717 > H 68,400: residual 4,317 bytes for the owner (decision 7). STOP of further pay-down (F2 a); nothing else pursued.

## AR-12 lines
- AR-12: qa-failure-analyst: 13 `execution_request:*` rows + `run_suite:phantom_story` learned at `red_sandbox.py --diagnostic` after the cost of `prepare()` (the clone, `red_sandbox.py:2185`) before the refusal at 2194-2198; no extra turn.
- AR-12: qa-automator / qa-runner: learned at `run_suite.py` / `import_test_receipt.py` refusal, before any launch.
- AR-12: qa-code-critic: friction unchanged (its ER rows stay on the page).

## Verification (verbatim tails, each alone from the worktree root)
```
python -B ai-packages/qa-factory/scripts/tests/test_contract_slices.py   -> === contract slices (markup, generation, freshness, shipped map): 530/530 ok ===  (exit 0; before the edits of this node the same run: 522/529, the 7 reds named marked-by-proof, entry-uniform, 5 partial-split)
python -B ai-packages/qa-factory/scripts/contract_slices.py --write      -> slices: 44 declared, 0 rewritten / wrote 8 pages
python -B ai-packages/qa-factory/scripts/contract_slices.py --check      -> slices: 44 declared, all present and fresh; 19 key pages; 12 charters carry a generated digest line  (exit 0)
python -B ai-packages/qa-factory/scripts/stage_joints.py --check         -> ... told counters: hand_cards 12, legacy_legs 0, unsited 17 / stage joints: clean
python -B ai-packages/qa-factory/scripts/tests/test_role_load.py         -> === role_load (the one measure of a role's start load): 186/186 ok ===
python -B ai-packages/qa-factory/scripts/tests/test_import_test_receipt_refusal.py -> 7 passed in 8.05s
python -B ai-packages/qa-factory/scripts/selftest.py --limits --lang     -> PASS limits: ... PASS limits: every mandatory role rule ... === qa-factory selftest: 4/4 ok ===
test_first_look_wiring 102/102 ok; test_charters_s5_s9 60 passed; test_scenario_walk 95/95 ok; test_scenario_world 33/33 ok
```
`scenario_walk.py --witness-for <the four owns>` printed: keep rows `test_contract_slices.py`, `test_detector_verdict.py`, `test_selftest_slow_tests.py`, `test_stage_joints.py`, `test_audit_rules.py`, `test_first_look_wiring.py`, `test_role_load.py`, `test_brief_pack.py`, `test_charters_s5_s9.py`, `test_hooks_wiring.py`, and the scenario layer (`test_scenario_cart_1.py`, `_dry_1`, `_local_1_0108`, `_local_1_arm_b`, `_walk`, `_world`). Run alone, green: the six non-slow files above. Slow file run by the DoD's test line (F1 a): `test_contract_slices.py`. Judged by the batch canon (listed in `slow_tests.json`, not run): `test_detector_verdict.py`, `test_selftest_slow_tests.py`, `test_stage_joints.py`, `test_audit_rules.py`, `test_brief_pack.py`, `test_hooks_wiring.py`, `test_scenario_cart_1.py`, `test_scenario_dry_1.py`, `test_scenario_local_1_0108.py`, `test_scenario_local_1_arm_b.py`; also `test_judgment_census.py`, `test_execution_request.py`, `test_probe_by_code.py`, `test_red_sandbox_probe.py` (named by the card).

## Negative control (byte copy, hashes equal)
Copy of `test_contract_slices.py` taken before; the one proof `"red_sandbox.diagnostic": "pass-through"` replaced by `set()` (diagnostic road proof removed). Run: exit 1, 3 FAIL: `T1rs/marked-by-proof` (analyst rows now marked but unproved), `T1rs/entry-uniform`, `T1rs/unproved-road-keeps-page/red_sandbox.diagnostic/qa-failure-analyst` (ids named). Restored from the copy:
```
ab133f5cf48afcb9065dc7f98059d1a52901c91ad240cdf73b607662711eb3aa  test_contract_slices.py (before probe)
ab133f5cf48afcb9065dc7f98059d1a52901c91ad240cdf73b607662711eb3aa  test_contract_slices.py (after restore)
```

## FR walk (touched sections)
A: FR-1/FR-2 no refusal text changed; FR-4 n/a; FR-59 an unproved road keeps its page (unknown never a pass). B: not changed (generated pages only; wording and doors untouched). C: FR-13 closed variety stays data (markers in `stage-joints.json`, ratchets in `role-load.json`); FR-14 n/a; FR-42 each state has a row. D: FR-16/FR-18 n/a; FR-58 the proof constants come from canon runs and the K1a table, not from the implementation. E: n/a. F: FR-41 numbers carry their command (U-CMD, `role_load.py --all --json`). G: FR-30 `--lang` PASS; FR-31 n/a; FR-32 n/a; FR-54 siblings below.
Architecture (commit): AR-10, AR-12, AR-20; judgment: none.

## Siblings / analogs and notes
- `test_stage_joints.py` and `test_audit_rules.py` (slow, not run) may read the markers/ratchets: judged by the batch canon.
- Analog noticed, not changed (out of owns): `T1rs/sited` and `T1rs/index-line` rows now loop four roles; the test comment at the old line 1002 ("the other eight roles hold none") is dropped with the rewrite.
- `run_suite:detail_target`, `:untyped_story_run`, `:missing_executor` are carried by `red_sandbox.*` in my constants (card: only phantom_story/recover/reparse excluded) although the K1a table says "not carried": the safe direction (more page), noted for FV2-86/FV2-91.
- Needed beyond the manifest: `ai-packages/qa-factory/scripts/role_load.py` (`settings`, `native_headroom_problems`), `ai-packages/qa-factory/agents/qa-*.md` tokens, `slow_tests.json`; the temp helper scripts (flip.py, tok.py) are not committed.
- The pre-edit state of one card premise: card §1 expected `qa-automator` U about 76,500: measured 76,472.
