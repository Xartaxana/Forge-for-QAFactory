# FV1-18 topic (N1-N4 merged) — code critic, t-522

Base used: `3e292d7~1` = `f4dfd07`, which is also `git merge-base HEAD origin/main` in the worktree `fv118-topic`, so the requested range is correct. Diff reviewed: `git -C <fv118-topic> diff 3e292d7~1 9fc7d61 -- ai-packages/qa-factory` (12 files, +489/-52; the topic total is 16 files once the four reports are counted).
Spec: `docs/tasks/specs/20261113-fv1-18-selector-contract-spec.md` (read whole, §0-§12). I also read the four builder reports, critic-diff-brief, `docs/TESTING.md` §"Что не пишется" and SIBLING_MAP (only the axes the spec names).

## Mechanical layer: control re-run on the MERGED tree (9fc7d61)

Command: `( cd <fv118-topic>/ai-packages/qa-factory/scripts && python -B tests/<t>.py )`, run once per file.

```
=== test_execution_request: 649/649 ok ===
=== test_run_forms: 254/254 ok ===
=== test_probe_by_code_languages: 1075/1075 ok ===
=== judgment_census: 24/24 ok ===
```
Consistency check on the counts: N2 reported 646 and N4 adds three `check_eq` rows (R-N4-2), which gives 649. `test_run_forms` is 254, the same as N4's run and the Lead's control. The merge broke nothing.

Empirical probe (scratchpad script `probe_sc.py`, run with `python -B -I` against the merged scripts dir; it calls `selector_contract` and `selector_note` and writes nothing):
```
['py.test', '<test-file>'] is_pytest_command= True | state= no_selection_form | note door present= True
['tox', '-e', 'py', '--', '<test-file>'] is_pytest_command= False | state= no_selection_form | note door present= True
['python', '-m', 'pytest', '<test-file>'] is_pytest_command= True | state= node_id | note door present= False
['npx', 'jest', '<test-file>'] is_pytest_command= False | state= no_selection_form | note door present= True
```

## Verdict per key

**K1. One answer, one reader: ok, with one residual (QUEUE, see K2).**
I searched the package outside `tests/` for `selectors_verified|selector_contract|selectors\.verified|selection_by_node_id|node_id_selection` (case-insensitive Grep). As a positive control, the same call found `profile_contract.py:343`. Readers of the answer:
- `run_suite.py:1593` (`selector_note`);
- `probe_by_code.py:2776` and `:2790`.

`execution_request.py` no longer derives the answer. Its only remaining mention is the copy filter at `:3403`. The old expressions are gone:
- `command["selector_contract_verified"] = ...`;
- `selectors_verified(profile_doc` (no hit outside the CHANGELOG history at `CHANGELOG.md:1264`);
- `_one_test_argv` used as the digest input (grep: it is no longer in `profile_contract.py`).

No second derivation of the *contract* survives. A second derivation of *"does this runner select by node id"* does survive, through `is_pytest_command`, at these sites:
- `execution_request.py:315`: pytest-vs-join selector routing in `validate_request`;
- `execution_request.py:3463`: `pytest_run`, which builds node-id selectors in `--mine`;
- `run_suite.py:306`: "the pytest path is decided by this one predicate, never by data".

The probe shows the two derivations disagree on `py.test`. Details and severity are under K2.

**K2. Closed variety as data: the row is the only carrier inside `selector_contract`, ok. The `py.test` outcome is a FIX (process) plus a QUEUE node.**
- `selector_contract` no longer calls `is_pytest_command`. The `node_id` step reads `launch_check.runner_identity(words)["node_id_selection"]` (`profile_contract.py:399`). That field comes only from the data key, through `_selection_rows` (`launch_check.py:190-196`, `:738`). The `_is_pytest` call left in `launch_check.py:739` feeds only `no_direct_form` wording, not selection: ok.
- `tox -e py`: `is_pytest_command` is False for it too (probe line 2), so both readers agree. This is not a defect of this topic.
- `py.test`: in one run, `build_mine_request` treats it as pytest (`pytest_run`, node-id selectors, `_place_rows`), while `selector_contract` answers `no_selection_form` (probe line 1). The consequences:
  - No false refusal: the run goes and the R6(a) probe refusal is the same as on origin/main.
  - But every behavioural run of a `py.test` project prints a SELECTORS note claiming the runner's selection is unverified, while the factory itself built node-id selectors for it.
  - The note's door cannot fix it (see K5-a).
- Lead decision F6(a) (spec §9c) accepted this narrowing, on condition that "the guard's `py.test` gap is filed as an analog finding" (§9c, §12). That finding is **not filed**. Search: case-insensitive Grep for `py\.test|tox -e` and for `selection_by_node_id|F6 analog|node id selection` over `plans/piles` in the root checkout, `read-main` and `fv118-topic`. Positive control: the same calls find `FV1-18` in `live-run-fvf/batch-1`, findings and README, and `py.test` in `execution-probes/README.md:74` (B-440, an older, unrelated row).
- **FIX-1 (process, before merge):** file the F6 analog finding in its pile in the same move, with its batch row and README "Содержание" row. Name it a one-road node: "`is_pytest_command` (pytest path: routing, node-id build) and `runner_identity.node_id_selection` (contract) answer differently for `py.test`; one of them must read the other". Owner: Lead. Under P31 this is a residual of the "one action, one road" class: it cannot stay a chat line (rule 19).
- Severity: not a BLOCKER. The shared mechanism is reached, the error direction is False, and nothing stops. Without the filed finding, though, the F6 condition the Lead set is unmet.

**K3. N2's deviations: safe defaults, ok.**
- `request_profile` returns `{}` for non-list `profiles` (`run_suite.py:1575-1582`). The old inline expression iterated a dict or a string and returned `{}` (non-dict items are skipped), and raised only on a non-iterable value such as `5`. The new guard turns that crash into `{}`. That `{}` then reaches `selector_contract`, which answers `command_not_profile` / `no_command`: False, and the note prints. This is no pass and no stop. `executor_gap` keeps its answers (R-N2-5 rows; the census and handed-to-person runs are green per N2's witness).
- `selector_note` returns "" when `root is None`. `main` always passes `project_root()` (`run_suite.py:2923`), so this branch serves only direct callers. The note is advice; exact-id binding still makes an unselected test `not_run` (R-N2-4 AR-28 row, green). No unknown becomes a pass.
- One remark, not a finding: a swallowed exception in `selector_note` makes "verified" and "could not judge" look the same (both silent). The spec prescribed `except -> ""` (§5 N2 item 4). `selector_contract` itself never raises (it has an `error` state), so only import failures are silenced. Acceptable as written.

**K4. Census: no judgment-census row is owed; the spec line is right, the builder misread it. FIX-2 (docs).**
- "Census row M4 of t-2046" is not `judgment-census.json`. It is the P31 language-exceptions census `docs/tasks/specs/reports/t-2046-language-exceptions-census.md`: table M4 "Execution: the pytest road", row `:63` "selector contract verified ... pytest: a node id as an argument IS pytest's contract; others ask selectors_verified". Spec §0.1 row 48 cites exactly that carrier.
- The builder searched only `judgment-census.json`, so "no such row" is a search of the wrong file.
- That row is still open in the merged tree (`fv118-topic` `:63`, unchanged).
- N4's owns did not list this docs file, so the omission is partly a dispatch defect (owns missing).
- **FIX-2:** mark row `:63` closed, "FV1-18 N4, `selection_by_node_id`, <hash>", and add the `py.test` narrowing with a pointer to the FIX-1 finding.
- `judgment-census.json`: no row owed. `selector_contract` returns data and never refuses. R6(a) is unchanged (`xref`, owner data). The removed refusal leaves the `validate_request` unit standing. `judgment_census: 24/24 ok` on the merged tree.

**K5. Refusal texts and doors: FIX-3.**
- (a) Dead door, in both places:
  - The SELECTORS note (`run_suite.py:1597-1603`) always names `onboarding_probe.py ... --probe-profiles --profile <id>` as the way "to verify".
  - The N3 sentence (`probe_by_code.py:2793-2797`) names it first too.
  - That door can open only the record states `none` / `command_changed` / `unreadable`. For the other states, running it changes nothing:
    - `no_selection_form`: the record is never read; the test row `test_execution_request.py:1965` "npx jest with its digest on record -> no_selection_form" proves a proven record does not help;
    - `command_not_profile`: the record proves only the profile's command;
    - `hand_false` / `hand_unreadable`: the hand wins.
  - Concrete case: a jest / vitest / dotnet / wrapper-script / `py.test` project runs the probe as told, re-runs, and gets the same note.
  - This breaks FR-2 / AR-9 ("the door must be one the receiver can use") and adds friction (P11, FR-55).
  - **FIX-3:** choose the door by `state`:
    - record states: the probe command;
    - `no_selection_form`: "the run-form data has no selection for this runner; nothing to do, the run goes by selector_args (a person may set selectors.verified)";
    - `command_not_profile`: "only the profile's one_test command is proven; run with --mine, or the record does not apply";
    - `hand_false`: "a person wrote false in qa-factory/config.json".

    In the probe sentence, put the person's `selectors.verified` first for the non-record states.
- (b) The new data problem "`selection_by_node_id` must be true when present" (`launch_check.py:194-195`) names the file, the row, the key and the expected value: ok (FR-1). Its receiver is the factory maintainer, not a role.
- (c) The N3 sentence names the bare `onboarding_probe.py`, unlike the note, which gives the full plugin path. The neighbouring door in the same ToolRefusal (`manifest_put.py`) is bare too, so this matches existing practice. QUEUE-level only (AR-8), not this round.
- (d) Does the automator's guard let it run `onboarding_probe.py`? I have not verified this. `onboarding_probe` appears in no `agents/*.md`, `guard_pre_tool.py` or `stage_guard.py`; the control grep for `run_suite` hits `agents/qa-automator.md`. I am not claiming a defect: if the Lead wants the door's reachability proven, that is a scout question.

**K6. Told before the work: ok / n/a.**
After N2, nothing in the run judges the selector contract any more. The note is advice printed at launch, and there is no later check for a brief to announce (FR-38 binds a check that judges the role's output). The only check left is the probe's R6(a). It was unchanged before this topic, and its input now answers True in more cases. Whether R6(a) is told before the work is pre-existing and not widened here. The automator's brief is FV1-29's file (spec §8).

**K7. Tests against TESTING.md: FIX-4.**
- Rows are parameterised with ids that name the case. The R-N1-1 table (`test_execution_request.py:1945-1971`) covers the outside input `config.json`:
  - empty: argv `[]`, `selectors ""`;
  - wrong type: profile as None / string / list, argv as a string, a boolean word, `selectors` as string / list;
  - nested: `commands` as a list, `one_test` as a string / list;
  - broken record files.
- R-N4-1 covers the key values `"yes"`, `false`, `1`, `null`, missing data and non-JSON. Good.
- Non-ASCII input is not exercised; a profile id or argv word in Cyrillic would be one cheap row. Minor; it can ride FIX-4.
- **Source pins, forbidden by TESTING.md:94** ("Пин исходника ... `inspect.getsource` — закрепляет устройство, а не результат"):
  - `test_execution_request.py:2033-2035` (R-N1-1 "runner_identity is handed argv WORDS": `"runner_identity(words)" in source`);
  - `:2074-2075` (R-N2-2: `build_mine_request` source lacks `command["selector_contract_verified"]`);
  - `:2076-2077` (R-N2-3: source contains the literal `k not in ("selector_args", "selector_contract_verified")`).
- The spec asked behavioural rows for R-N2-2/R-N2-3 (§5 N2 item 6): a `--mine` build in the `ep1_37` fixture with `selectors: {}`, and a precedent job whose command carries `false`.
- The behavioural row also matters for substance: no test drives a REAL `build_mine_request` output into `selector_note`. So the spec's FR-5 claim "the factory's own proof reaches `--mine`" (§2 item 5, E13/E14) has a witness only on a hand-built command (R-N1-8), not on the command `--mine` actually builds.
- **FIX-4:**
  - replace the two N2 pins with the spec's behavioural rows, and in that row assert `selector_note(...) == ""` for the built request against a proven record;
  - drop the R-N1-1 source pin, or turn it into a behaviour row: an identity string with its `"\u0000env"` word handed to `runner_identity` gives the same answer as the words alone, if that is wanted.
  - The spec's own "a source-level row" for R-N1-1 (§4) conflicts with TESTING.md: a spec defect of the dispatcher, noted.

**K8. Duplication and code quality; class completeness.**
- DUPLICATION AND CONSISTENCY:
  - `probe_by_code.py:2776` computes `selectors_verified(profile, root)`, then `:2790` calls `selector_contract(profile, root)` again for `why`. That is two evaluations of one answer (two record reads), wrapped in a try/except around a function documented as never raising. **FIX-5 (small):** `got = PC.selector_contract(profile, root)`, then `verified = got["verified"]`, and use `got["why"]` in the sentence. Drop the dead try.
  - `request_profile` removes the duplicated lookup (AR-15): good.
  - The rest of the grep (above) found no further duplicates.
- CODE QUALITY:
  - `run_suite.py:2926` `launched =apply_resolved_ids(` lost its space in the N2 edit (lint, FIX-5).
  - The stale docstring `profile_contract.py:428-432` still says `build_mine_request` asks `selectors_verified`. It no longer does: the readers are `run_suite.selector_note` and the probe. It also says "a pytest command (True)" where the step is now the data key. FIX-5.
  - `selector_contract` (`:343-424`) reads in spec order. The positional invariants hold: hand before command, env before record, record read with `command_identity` of the profile's one_test (`:416`), `runner_identity` fed words (`:398`). I traced the run road for E18 (`{}` profile, Playwright command): `command_not_profile`, matching the spec.
- Class completeness by the map:
  - axis 5 (stage twins): one `main` serves `--mine` and `--request` (S5/S6/S7): covered.
  - axis 30 (profile commands): reads go through `command_argv` / `command_env` / `command_identity`: covered.
  - axis 34 (one road): the contract has one road; the node-id question has two (K2): FIX-1 files it.
  - axis 11 (shell-command recognizers): the `py.test` divergence: FIX-1.
  - Per-language: only `pytest` (node id) and `playwright-test` (selection row) can ever read verified. Every other runner of the run-form table (jest, vitest, dotnet-test, ...) is permanently `no_selection_form`, so it gets the note on every run. The note is harmless only once its door is honest (FIX-3). The data gap (selection rows for the other forms) is a QUEUE item for the execution-probes pile, not this topic.
- JUDGMENT (brief questions 10/11): no role judgment moved into code. A refusal that judged an unproducible fact became advice (AR-7, AR-29): ok.
- ONE ACTION, ONE ROAD (question 12): the residual is the K2 `py.test` split. It leaves this verdict as FIX-1 (finding with an owner), not as a chat line.

## Findings summary

BLOCKER: none.

FIX (land before merge):
1. File the F6 analog finding (Lead's condition in §9c, §12): `is_pytest_command` vs `runner_identity.node_id_selection` disagree on `py.test`. Proposed node; owner Lead.
2. Close row M4 `:63` of `docs/tasks/specs/reports/t-2046-language-exceptions-census.md`, with the `py.test` narrowing noted. That file is the census the spec meant; `judgment-census.json` owes nothing.
3. Choose the door in the SELECTORS note (`run_suite.py:1597-1603`) and in the R6(a) sentence (`probe_by_code.py:2793-2797`) by state. The onboarding probe only for the record states. Honest words for `no_selection_form`, `command_not_profile` and `hand_false`.
4. Replace the source pins at `test_execution_request.py:2033-2035, 2074-2077` with behaviour rows. The R-N2-2/3 behaviour row must drive a real `build_mine_request` output plus a proven record into `selector_note` and expect "".
5. Small quality items: compute once in `probe_by_code.py:2776/2790` and drop the dead try; `run_suite.py:2926` spacing; stale `selectors_verified` docstring `profile_contract.py:428-432`.

QUEUE: selection rows for jest / vitest / dotnet forms (execution-probes); full plugin path in the R6(a) door (AR-8); proving that the automator's guard admits `onboarding_probe.py` (a scout question).

Decision note: this verdict is input to acceptance. Accepting t-522 and deciding whether FIX-1/FIX-2 ride this topic or the coordinator's own move belongs to the Lead (rule 6).

DUPLICATION AND CONSISTENCY: one finding (FIX-5, double evaluation in the probe). Grepped: the answer's readers and `is_pytest_command` callers across `scripts/`.
CODE QUALITY: FIX-5 (spacing, stale docstring); test-quality FIX-4.
ONE ROAD: FIX-1.

VERDICT: ACCEPT WITH FIXES (fit_with_fixes), 0 blocking findings, 5 fixes.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "class_completeness": "axis 5 covered (one main for --mine/--request); axis 30 covered (command_argv/command_env/command_identity); axis 34 and axis 11: the contract has one road, but the node-id question keeps a second reader (is_pytest_command at execution_request.py:315, :3463, run_suite.py:306) that disagrees with runner_identity.node_id_selection on py.test; the F6 analog finding the Lead required is not filed (FIX-1). Per-language: only pytest and playwright-test can read verified; other run forms are permanently no_selection_form (QUEUE, execution-probes).",
  "fixes": [
    "FIX-1: file the F6 analog finding (py.test: is_pytest_command vs runner_identity.node_id_selection), batch row and README row, owner Lead",
    "FIX-2: close row M4 line 63 of docs/tasks/specs/reports/t-2046-language-exceptions-census.md (the census the spec meant), with the py.test narrowing noted",
    "FIX-3: state-dependent door in run_suite.selector_note (run_suite.py:1597-1603) and probe_by_code R6(a) sentence (probe_by_code.py:2793-2797): onboarding probe only for none/command_changed/unreadable; honest words for no_selection_form, command_not_profile, hand_false",
    "FIX-4: replace inspect.getsource pins test_execution_request.py:2033-2035 and 2074-2077 (TESTING.md:94) with behaviour rows; R-N2-2/3 drives a real build_mine_request output plus a proven record into selector_note expecting empty",
    "FIX-5: compute selector_contract once in probe_by_code.py:2776/2790 and drop the dead try; run_suite.py:2926 spacing; stale selectors_verified docstring profile_contract.py:428-432"
  ],
  "trail": {
    "read": [
      "docs/tasks/specs/20261113-fv1-18-selector-contract-spec.md (whole)",
      ".claude/worktrees/fv118-topic/docs/tasks/specs/reports/20261113-fv118-n2-report.md",
      ".claude/worktrees/fv118-topic/docs/tasks/specs/reports/20261113-fv118-n4-report.md",
      "git diff 3e292d7~1 9fc7d61 -- ai-packages/qa-factory (all 12 files)",
      "execution_request.py:300-330, 615-625, 1802-1840, 3455-3480",
      "run_suite.py:295-320, 1575-1620, 2915-2930",
      "launch_check.py:172-215, 711-748; hooklib.py:2294-2310",
      "gate_preflight.py:3655-3675; brief_pack.py:3185-3200; onboarding_probe.py argparse 962-969",
      "docs/TESTING.md:80-104",
      "docs/tasks/specs/reports/t-2046-language-exceptions-census.md (grep M4, line 63)",
      "tools/critic_verdict.schema.json"
    ],
    "reruns": [
      {"command": "python -B tests/test_execution_request.py (merged tree 9fc7d61)", "result": "=== test_execution_request: 649/649 ok ==="},
      {"command": "python -B tests/test_run_forms.py (merged tree)", "result": "=== test_run_forms: 254/254 ok ==="},
      {"command": "python -B tests/test_probe_by_code_languages.py (merged tree)", "result": "=== test_probe_by_code_languages: 1075/1075 ok ==="},
      {"command": "python -B tests/test_judgment_census.py (merged tree)", "result": "=== judgment_census: 24/24 ok ==="},
      {"command": "python -B -I scratchpad/probe_sc.py <scripts dir>", "result": "py.test: is_pytest_command True, state no_selection_form, note door present; tox -e py: False/no_selection_form; python -m pytest: True/node_id, no note; npx jest: False/no_selection_form, door present"}
    ]
  }
}
```
