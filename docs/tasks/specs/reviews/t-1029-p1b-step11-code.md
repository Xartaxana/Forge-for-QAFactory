# t-1029 — critic, code: the dry story, step 11 (N4R, N2h-а, N5)

DoD: spec `docs/tasks/specs/20261117-p1b-finish-spec.md` §1, §4 cards N4R / N5 / N2h (part а), §7 F-P16/17/18, Lead decisions (F-P4 reading 2 (б), F-P16 (а), F-P17 (а), F-P18 (а)). Brief: `docs/tasks/critic-diff-brief.md` (questions 1-12).
This verdict feeds the decision; accepting the work is the Lead's call (critic rule 6).

## Verdicts per node

- **N4R (t-1020, branch worktree-agent-a4b8077bf099b8406, not merged)**: accept once F1-F3 are fixed in its fix round. F4 is a Lead commit in the same wave.
- **N2h-а (t-1022, branch worktree-agent-af175eb746148d531, not merged)**: accept once F6-F9 are fixed. **F5 blocks the merge** (DoD line not yet run). F7 is the predicted S5 stop and needs the CI output before anyone acts on it.
- **N5 (t-1021 + t-1028, merged 905e9735 / 7981ccb6)**: accept. N1-N4 are notes; N1 is a missing DoD key in the report.

## Findings

**F1 (fix-in-round, N4R): a ledger file whose stem is no group is never read: a dead label, and it can also dodge the check from edge 7.**
`dry_exits.py` `_ledgers` (branch, around :783-791) only goes through `census["files"]` and opens `known_red/<stem>.json` for each one. A file `known_red/<x>.json` where `<x>` is no group is read by no one: `check` skips it, and no part ever reads it. That breaks the card's edge-4 invariant: no label may hang without a row that can print it (I8, AR-28).
- Probe, run on a temp copy of `driver-exits/` (scratchpad `probe_orphan.py`, verbatim): `orphan file known_red/zz-typo.json holding an s0 row id problems: 0 ledger-lines: []`.
- The orphan file held the same id as `known_red/s0.json`. Even so, `_ledger_twice` stayed silent, because the orphan never enters `files`.
- Fix: in `_ledgers`, go through `sorted((directory / LEDGER_DIR).glob("*.json"))`. A stem that is not in `census["groups"]` gets a red line: `known_red/<x>.json names no walk group; expected known_red/<group>.json for a group file of driver-exits/ - rename or remove it`. Every file found goes into `_ledger_twice`. Add one selftest row: "a ledger file of no group is red".
- Open point (a): yes, this should be red. The rule that decides it is the card's edge 4 (I8 under AR-28: no label hangs without a row that can print it). Axis 18 also says a stale site is refused with a door and never shrinks silently.

**F2 (fix-in-round, N4R + dry_world; Lead widens owns): one rule ("an absent group file is an empty ledger") is coded in two places, and the walker's copy of it is wrong.**
- `dry_world.py:1396-1399`: `main_ledger = {**known_red.load(KNOWN_RED_FILE), **known_red.load(ledger_path)}` sits inside `except LedgerError: main_ledger = {}`.
- `known_red.load` raises `LedgerError` on a missing file (`known_red.py:59`).
- So a missing group file empties the whole merge, including the shared `main/*` rows. A row whose start snapshot was not made then reads `fail ... no known_red row` instead of `note after:FV3-5`.
- Open point (b): the defect is real. Its direction is a false red, so it never makes a red expected, but it does hide the main rows, which is the second half of the invariant.
- Callers: only `test_scenario_dry_1.py:116`, `exits_part` (grep `walk_exits(` over `ai-packages tools .github`; the positive control finds the `def` in dry_world). That one caller is patched (`:115`, it passes `KNOWN_RED_FILE` when the group file is absent), so the defect is latent today, with no other live caller.
- The rule now lives in `judge_group` (`dry_exits.py:1438`, `is_file()`) and in `exits_part` (`:115`), and the walker does not have it. That is a second road (P31, brief question 6).
- Fix (one site): `dry_world.py:1397` becomes `{**known_red.load(KNOWN_RED_FILE), **(known_red.load(ledger_path) if Path(ledger_path).is_file() else {})}`, and the `walk_ledger` patch in `exits_part` is dropped. Better still, both `judge_group` and the walker read through one helper in `dry_exits`, e.g. `group_ledger_rows(path)`.
- Owner: the N4R fix round, with `dry_world.py` (only `walk_exits` :1396-1399) added to owns. No parallel node owns `dry_world.py` now: N2h-а owns `dry_stub.py`, N5 is merged, and the group nodes come after N4R. If the Lead keeps owns as they are, then: `Остатки`: `dry_world.walk_exits: an absent group ledger drops the main/* rows | узел: <id the Lead opens, before N4:gates>`.

**F3 (fix-in-round, N4R): the `tests-over:` line is missing.** The report says +136 test lines against +0 product lines, and that the commit has no `tests-over:` line (the hook WARNed). The reason it names does hold: the five rows the card asks for, and all of the code is in the test layer. Fix: put the line in the fix-round commit (brief question 5(f), critic rule 20).

**F4 (Lead, same wave): axis 18 gets a new member nobody named.** `driver-exits/known_red/<group>.json` is a new shrink-only ledger, with `pins.known_red` per file. Axis 18 (`docs/SIBLING_MAP.md:395-406`) and brief question 9 name only `driver-exits/known_red.json` and the selftest ledger. The axis says: "A new shrink-only ratchet joins this table in the commit that creates it, and the brief's question 9 names it." Both are mechanism paths, so this is a Lead commit (axis block + `tier:`) in the N4R wave.

**F5 (BLOCKS THE MERGE of N2h-а): the main-pass lines the DoD requires are not attached.** The card asks for `dry-1/main/stop` and `dry-1/main/time` from the CI of the N2h branch, verbatim. Under F-P18 (а) / edge 8, more than 800 s, or a kill at 900, means no merge. The report says "NOT RUN here". This is the coordinator's CI step, not a code fix. Until it is done, the node is "code done, not provable".

**F6 (fix-in-round, N2h-а, plus a note on the spec): "rc != 0 -> no record" is false for the real tool, and the docstring states it as fact.**
- `probe_by_code.py:63`: `incomplete` exits 1 and writes the record.
- `:8364-8368`: a `ToolRefusal` exits 2 and writes a `refused: tool` record (`_record_tool_refusal` :8003-8005).
- For both, `critic_branch` (branch `dry_stub.py`, around :515-519) writes a `live_only` "exit N" row and puts nothing in `wrote`. Its docstring says "no record is made for it". The record is there, though, and `world_list` will name it in the form. That part is correct under AR-29: it is the tool's data, and the stub never deletes it.
- Fix: when rc != 0 and `task_dir/record` exists, say so in the row: `... exit N: <text>; the tool left <record>`, and drop the "no record is made" claim.
- Lead: edge 3 of the card should read "a record the tool itself wrote stays; it is the tool's data". Also `run_probe` returns `stderr or stdout`, while probe_by_code prints its refusal JSON on stdout. Any stderr noise (for example the `_unrestored_exit` line) would lose the refusal. Return stdout + stderr, as `run_script(both=True)` does.

**F7 (open point (a); N2h-а fix round, after CI): the predicted stop holds when read against the tool's code.**
- At S5, `_no_role` is False (`probe_by_code.py:6984-6991`: only S6 counts as "no role").
- A check with no entry in `work/probe-models/<dispatch>.json` is owed, and `_models_refusal` (:4917-4923) is a plain `Refusal`: exit 2, no record.
- The stub writes no model file. The story has no `qa-code-critic@S5` stub row at all (read from story.json: the only critic rows are `qa-case-critic@S2/S3/S4`).
- So S5 should stop with a NEW reason: the record is missing, so the form's `probes.records` cannot be filled.
- The order is wrong for this: `fill_role` writes `files` after `_fill_form` and after `critic_branch`. A real role writes its models before it probes.
- Fix, in the N2h-а fix round (both `dry_stub.py` and `story.json` are in its owns):
  - (1) Move the `if "files" in mine: write_files(...)` block above the critic branch. The only `files` today are `qa-case-critic@S4` -> `work/test-cases/critic-findings.md`. That is not a form, so nothing gets overwritten, and it still lands before `--fix`.
  - (2) Add a `qa-code-critic@S5.files` row with `work/probe-models/<dispatch>.json`. Its entries are the role's judgment, taken as story data in the `--plan` shape for the check keys the CI run prints.
  - Wait for the F5 CI output first. N2h-б (it owns only the label and `slow_tests.json`) is the wrong node for this.

**F8 (fix-in-round, N2h-а): `run_probe` is a second package-script runner.** `dry_stub.run_script` (:197-205) says it is "the ONE runner of a package script ... `harness.run_script`". `run_probe` builds the same thing again: `sys.executable -B SCRIPTS/x`, `PYTHONDONTWRITEBYTECODE`, capture, timeout. The only thing it adds is the 120 s cap; the run class is already inherited from the driver's environment (`dry_world.py:304`), and it is set explicitly as edge 1 asks. Fix: give `harness.run_script` a `timeout=300` kwarg (one line; `harness.py` joins owns), add a `timeout` to `dry_stub.run_script`, and call it with `both=True`. If the Lead keeps owns as they are, this becomes an `Остатки` line with a node.

**F9 (fix-in-round, N2h-а): a pin on a constant.** The row `"N2h: the probe cap is 120 s ..."` asserts `PROBE_TIMEOUT_S == 120`. `docs/TESTING.md:137` («Пин измеренной константы», seconds) says such a pin is not written. Delete the row. The timeout behaviour is already a row of its own.

**F10 (proposal for the Lead; N2h-б DoD): the main-pass label is keyed by stage only, so a new stop reason at the same stage stays hidden.** `dry_world.py:1055-1057`: `results = {main/<stage>: done}`, and `known_red.reconcile` matches by id. Any stop at S5 reads `known red: main/S5 -> FV3-5`, while the label's `raised_by` still names the old reason ("critic stub leaves the handover form unfilled"). After N2h-а, the pass will most likely stop at S5 again, for the F7 reason. N2h-б's edges only cover "the pass went further". Proposed edge for N2h-б: if `dry-1/main/stop` names a reason other than the label's `raised_by`, take a new id from the Lead and re-label; a same-stage stop is no reason to keep the label. Only a person reading `main/stop` (F5) catches this today.

**Open point N2h (b), note -> residual:** the card says "каждый экземпляр окна", and the critic form scopes the window by case (`handoffs/s5-critic-to-automator.yaml:34`, `window: <the case ids under review>`; the brief says "every new/changed test"). Reading ALL `tests[]` rows gives the same set only in a one-window story such as dry-1. With two windows, later critics would re-probe earlier instances (they would get `already_probed` and list a record in `wrote` that they did not write). `Остатки`: `dry_stub.critic_branch: filter manifest rows to the cases of the reviewed window | узел: N4:s5`.

**Open point N2h (c), fix-in-round (low):** the real role's manifest row carries `selector` / `test` (`manifest_from_tests.py:1369,1451`). The dry row has neither. `<file>::<instance id>` only works because the dry row's explicit `instance_id` happens to equal the function name. `contract.test_instance_id` (:4026-4034) derives the id from function + parameter, so for a parametrised test the node comes out wrong (the result is a ToolRefusal record, not a pass). Fix: the dry automator fragment carries `selector`, as the real manifest does, and the stub reads `selector` only. If it is absent, write a `live_only` row "no selector in the manifest row" and never guess a node (FR-59).

**N5 notes:**
- **N1:** the card DoD wants "минуты в отчёте"; the report says not measured. Fix: the coordinator adds the minutes of run 44021364352 (`ci_read.py jobs`) to the report.
- **N2:** `tables` runs four commands in one step under `bash -e`. A red `--check` hides the results of the three tables after it. That is not a mask (the job is red anyway), but cheap to fix: collect `rc` and `exit $rc` at the end.
- **N3:** `test_no_run_string_splices_inputs` repeats the F19E loop of `test_f19e_no_run_string_splices_a_value_a_person_controls` (`tools/test_workflows.py:~300-309`, which already covers `NAMES`, now including dry-story). Fold the `${{ matrix.` clause into it (brief question 5(e)).
- **N4 (twin of F-P17):** `dry_world.py --spike` (:9, :642 `def spike`, :1422-1425) lost its only caller, the canon's `dry-story-spike` job. Grep: `--spike` / `def spike` over `ai-packages .github tools`; the positive control finds the def. `Остатки`: `dry_world.py --spike branch and spike() dead after N5 | узел: <Lead>`.
- Edge 11: the line for RUNBOOK §7 is in the report, for the Lead.

**N5 masking question, answered (no mask):**
- The parts never reach the profile's pytest. `s0` rows all start `fresh` and `s1-s4` rows all start `S0` (counted from the exits files: `s0 {'fresh': 10}`, `s1-s4 {'S0': 9}`).
- The prefix is `drive_main(stop_after=S<max start>)` (`dry_world.py:1381-1383`), and each row runs single boundary turns from its snapshot. S5 (the automator's `run_command`, the critic's probe) is never entered.
- The `s0` label `kind:halt/free words -> FV3-16` is an S0 product gap, unrelated to pytest.
- The main pass runs inside `package-full`, which installs pytest (`nightly.yml:101,136`).
- From s5/s6-s9 on, the parts will reach pytest; 135c8f89 adds the install step there in time.
- The structural risk sits in F10, not in N5.
- Canon without `dry_only`: `checks`/`full`/`clock` keep `if: !inputs.dry_only` (default false). The one change: `full` -> nightly now also carries `dry-story`, which the spec intends (F-P3 (а), edge 10). No `run:` splices `inputs.*`/`matrix.*` (the group goes through `env: GROUP`, quoted).
- The list job cannot drop a group silently. It prints every name, and a name with a space splits into parts whose rows file is absent, which turns red.
- `spike=true` / `inputs.spike` / `dry-story-spike`: none left in `.github tools docs/RUNBOOK.md CLAUDE.md PROJECT.md plans/builder-rules.md` (positive control: `dry_only=true` hits `canon.yml:36` and `dry-story.yml:3`).

**Open point N4R (c) answered:** no caller of `dry_exits.judge` / `--judge` is left. Grep `-i -E "[^_]judge\(|--judge"` over `ai-packages/qa-factory/scripts .github tools` (minus `judge_*`); the hits are unrelated (`collect_stall.judge`, `probe_by_code --judge`, controller text). Positive control: `def judge_group` found at `dry_exits.py:1425`. The deleted test row covered behaviour the spec removed (F-P17 (а)); the known-red/new-red reading is still covered by the `judge_group` rows (`dry_exits.py:~2629-2690`).

## Standing questions

1. **Fit:** N4R edges 1, 2, 3, 5, 6, 7 hold; edge 4 has a gap (F1). N2h edges 1, 2, 4, 5, 6, 7 hold; edge 3's premise is wrong (F6); edge 8 is not yet run (F5). N5 edges 1-11 hold, except the minutes (N1).
2. **The builders' own decisions:** N4R did not create `known_red/s1-s4.json` (it has no rows; the card says so). N5 made `tables` a separate job (safe, runs in parallel). N2h fell back on the node (open point (c)).
3. **Seams:** additive. The `exits_part` patch is a seam workaround (F2).
4. **Class completeness:** axis 18 (F4), axis 34 (F2, F8, N4), axis 30 (`world_command` now serves both automator and critic, good), axis 5 twin (automator and critic each run their tool as a process), axis 38 (the `--check` step is in `tables`). Sweep inside the artifact, N4R `_ledgers`: shared file = applied; group file = applied; file of no group = missing (F1); explicit `--ledger` = unchanged (edge 5).
5. **Tests:**
   - (a) The rows would catch their defects (`absent ledger` goes through `judge_group`, `orphan` and `twice` through `check`).
   - (b) Expected values come from the card's rules.
   - (c) No row exists for the orphan file (F1) or for the walker-glue path (it needs a world; CI covers it).
   - (d) The `judge` row was deleted along with its behaviour (spec).
   - (e) N3.
   - (f) F9; F3.
   - (g) No new test files.
6. **Duplication:** F2 (one rule in two places, and the walker's copy wrong), F8 (`run_probe` vs `run_script` / `harness.run_script`), N3. `world_command` removed a duplicate. The ratchets are not re-run (forge-check's job).
7. **Code quality:** new functions are all under 60 lines, nesting is 3 levels or less. The `critic_branch` docstring overstates (F6). `wrote` lists an `already_probed` record this call did not write (minor; see open point (b)).
8. **Hygiene:** 0 Cyrillic and 0 control bytes on the added package lines of both branches (script with a positive control).
9. **Ratchets:** `driver-exits/known_red.json` `pins.known_red` goes 2 -> 1, because the row `kind:halt/free words` moves out. `known_red/s0.json` is new, `pins.known_red` 0 -> 1, the same row moved verbatim (node FV3-16, `raised_by` "product gap: Lead t-828"). Total rows stay 2 -> 2, with no raise. The new member is not in the axis-18 table yet (F4). N2h and N5 touch no ratchet.
10. **Architecture:**
    - N4R names AR-14, AR-22, AR-13, AR-20, and they hold. AR-28 holds except F1.
    - N2h names AR-29, AR-22, AR-13. AR-29 holds: the stub never writes a verdict, and the record comes from the real process.
    - AR-17: grep `driver\.[a-z_]+ =` over the added lines of both branches finds nothing.
11. **Judgment:** none moved into code. Ledger checks are presence/xref; the stub runs the tool. The model file in F7 is story data (the role's judgment as data), not code.
12. **One road:** F2, F8 and N4 are residuals of this class. Each comes back as a fix or as a node line above. No language/project exclusion found (grep of the added lines for language/runner names: only the profile reader).

## What I did NOT check
- No slow file was run (`test_scenario_dry_1.py`), no CI, no ratchets.
- `test_workflows.py` was not re-run (33 passed is attached).
- I did not prove that the CI stop after N2h-а is F7's (it is a prediction from reading).
- I did not check the `_path` key of walk rows beyond the green selftest.
- I did not check the N5 report's 33 vs 32 count past the dispatcher's line.

## Trail
- Read:
  - the spec: §1 (:55-126), §4 N4R/N5/N2h (:368-431), §7 F-P16..F-P18 (:608-620), §8, the Lead decisions (:773-837)
  - `critic-diff-brief.md`; SIBLING_MAP axes 18, 30, 34, 38
  - `git diff origin/main...origin/worktree-agent-a4b8077bf099b8406` and its report; `git diff origin/main...origin/worktree-agent-af175eb746148d531` and its report; `git show 89b33ba8`, `git show 135c8f89`
  - `dry_world.py` :961-978, :1044-1062, :1353-1420; `dry_exits.py` :755-830, :1425-1470, :2600-2635; `test_scenario_dry_1.py` :85-140; `known_red.py` (grep of load/raise)
  - `probe_by_code.py` :1-72, :210-225, :4917-4923, :6984-6991, :7125-7150, :8327-8420; `brief_pack.py` :225-250; `contract.py` :3786, :4016-4045
  - `dry_stub.py` :197-210, :440-463, :760-766, :863-960; `handoffs/s5-critic-to-automator.yaml` :10-62; `nightly.yml` (origin/main) :1-80 and the pytest lines; `TESTING.md:137`
- Ran:
  - `python -B .../agent-a4b8077bf099b8406/.../dry_exits.py --check` -> `dry_exits --check: 0 discrepancies` (HEAD 26552e5a = branch tip)
  - `python -B .../agent-af175eb746148d531/.../dry_stub.py --selftest` -> 11 `PASS N2h:` rows, `=== dry_stub --selftest: 200/200 ok ===` (52 s, HEAD 0c40986b = tip; tree clean afterwards apart from the pre-existing `docs/OWNER_PRINCIPLES_INDEX.md`)
  - probe `scratchpad/probe_orphan.py` on a temp copy -> `baseline problems: 0`, `orphan file ... problems: 0 ledger-lines: []`, `s0 group ledger removed (absent = empty) problems: 0`
  - greps as cited above, each with its positive control

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "N2h-a merge gate (F5): the CI main-pass lines dry-1/main/stop and dry-1/main/time from the N2h branch are not attached; F-P18 (a) / edge 8 (over 800 s or a kill at 900 means no merge) is unchecked"
  ],
  "class_completeness": "Axis 18: the new member driver-exits/known_red/<group>.json is not in the axis table or in brief question 9 (F4, Lead commit). Axis 34: the absent-ledger rule is coded twice and the walker's glue lacks it (F2); run_probe duplicates the one script runner (F8); dry_world --spike is dead after N5 (N4, node line). Axis 30 and the axis 5 twin are covered (world_command shared by automator and critic). Axis 38: the --check step is in the tables job. Artifact sweep of N4R _ledgers: shared file and group file applied, file of no group missing (F1).",
  "fixes": [
    "F1 N4R dry_exits._ledgers: go through known_red/*.json; a stem that is no census group is red; every file found goes into _ledger_twice; add one selftest row",
    "F2 dry_world.py:1397 load the group ledger only when the file exists (or one helper shared with judge_group); drop the walk_ledger patch in test_scenario_dry_1.exits_part:115; Lead widens owns or opens a node",
    "F3 N4R: tests-over: line in the fix-round commit",
    "F4 Lead: SIBLING_MAP axis 18 and critic-diff-brief question 9 name driver-exits/known_red/<group>.json (mechanism commit, same wave)",
    "F6 N2h-a critic_branch: on rc != 0 with the record present, the row says the tool left it; drop the docstring claim 'no record is made'; run_probe returns stdout plus stderr; Lead corrects card edge 3",
    "F7 N2h-a, after the CI output: write the story files before critic_branch; add a qa-code-critic@S5 files row with work/probe-models/<dispatch>.json in the --plan entry shape",
    "F8 N2h-a: run the probe through dry_stub.run_script / harness.run_script with a timeout kwarg instead of a second runner (or a residual node)",
    "F9 N2h-a: delete the selftest row pinning PROBE_TIMEOUT_S == 120",
    "F10 Lead: N2h-b edge - re-label main/S5 with a new id when the main/stop reason differs from the label's raised_by",
    "N2h (c): the dry manifest fragment carries selector; the stub reads selector only, absent means a live_only row, no guessed node",
    "N5 N1: the coordinator adds the measured minutes of run 44021364352 to the N5 report",
    "Residual lines: critic_branch window filter (node N4:s5); dry_world --spike dead branch (node by the Lead)"
  ],
  "trail": {
    "read": [
      "docs/tasks/specs/20261117-p1b-finish-spec.md (sections 1, 4 N4R/N5/N2h, 7 F-P16..18, 8, Lead decisions)",
      "docs/tasks/critic-diff-brief.md",
      "docs/SIBLING_MAP.md axes 18, 30, 34, 38",
      "git diff origin/main...origin/worktree-agent-a4b8077bf099b8406 and docs/tasks/specs/reports/20261117-p1b-n4r-report.md",
      "git diff origin/main...origin/worktree-agent-af175eb746148d531 and docs/tasks/specs/reports/20261117-p1b-n2h-report.md",
      "git show 89b33ba8, git show 135c8f89, docs/tasks/specs/reports/20261117-p1b-n5-report.md",
      "ai-packages/qa-factory/scripts/tests/dry_world.py :961-978, :1044-1062, :1353-1420",
      "ai-packages/qa-factory/scripts/tests/dry_exits.py :755-830, :1425-1470, :2600-2635",
      "ai-packages/qa-factory/scripts/tests/test_scenario_dry_1.py :85-140",
      "ai-packages/qa-factory/scripts/tests/dry_stub.py :197-210, :440-463, :760-766, :863-960",
      "ai-packages/qa-factory/scripts/probe_by_code.py :1-72, :210-225, :4917-4923, :6984-6991, :7125-7150, :8327-8420",
      "ai-packages/qa-factory/scripts/brief_pack.py :225-250; contract.py :3786, :4016-4045",
      "ai-packages/qa-factory/handoffs/s5-critic-to-automator.yaml :10-62",
      ".github/workflows/nightly.yml (origin/main) :1-80 and pytest lines; docs/TESTING.md :137"
    ],
    "reruns": [
      {"command": "python -B C:/QAFactory/forge-repo/.claude/worktrees/agent-a4b8077bf099b8406/ai-packages/qa-factory/scripts/tests/dry_exits.py --check", "result": "dry_exits --check: 0 discrepancies (HEAD 26552e5a, branch tip)"},
      {"command": "python -B C:/QAFactory/forge-repo/.claude/worktrees/agent-af175eb746148d531/ai-packages/qa-factory/scripts/tests/dry_stub.py --selftest", "result": "11 PASS N2h rows; === dry_stub --selftest: 200/200 ok === (HEAD 0c40986b, branch tip)"},
      {"command": "python -B scratchpad/probe_orphan.py (check() on a temp copy of driver-exits with known_red/zz-typo.json added)", "result": "orphan file known_red/zz-typo.json holding an s0 row id problems: 0 ledger-lines: [] (F1 confirmed)"}
    ]
  }
}
```
