# t-1357 -- critic: RD1-14 (C3-k) plan gate + FG7-70 diff gate

Base read: worktree HEAD 1ef42f16; origin/main is db9d9899 now. `git diff --stat 1ef42f16 origin/main -- ai-packages/qa-factory`
touches none of the card's files, so every fact below holds on today's main. These verdicts are inputs to the Lead's
acceptance. They are not the acceptance itself (rule 6).

## Q1 -- plan RD1-14: APPROVE WITH FIXES

The design holds on main. The F-1..F-6 decisions agree with the code. These checks hold:
- `gate_template.acceptable` (gate_template.py:70-106) reads `promotable` from the row that holds the consumer.
- `_consumer_problem` (gate_registry.py:426-444) applies only to converted `accept` sites (gate_registry.py:903-911).
- `driver_stage_build.build_outcome` is a `dispatch` site of `stand_identity` (gate-registry.json:15). The k4 literal
  `provenance.rehearsal` there therefore draws no RD1-25 finding.
- The prefix rule (gate_registry.py:795-808) only bans `person_confirmed` tokens. `baseline_identity.capture` and
  `environment_preparation.deploy_proof` carry no such token.
All the needed fixes are text fixes. P-1 stops k1's dispatch mechanically.

### Findings
- **P-1 (blocks the k1 dispatch): the k1 DoD is refused by `tools/dispatch_manifest.py`.**
  - The cause is the backticked span ``line `not run locally: test_execution_request.py, test_gate_registry.py, canon judges` ``.
    `_command_lines` counts any inline span of 2 or more tokens as a command, so `_dod_run_check` sees two canon-only
    files run whole.
  - Probe: `dm.check` on the k1 header block with the real paths and N() expanded gives `exit 2 | DOD-RUN REFUSED ... runs
    the canon-only file(s) test_execution_request.py, test_gate_registry.py whole`. The same block with the span unquoted
    gives `(0, '')`. k2, k3 and k4 give exit 0. Negative control: adding `--witness-for` gives exit 2 with the R1 reason.
  - Fix: write the line unquoted, as k2 and k3 do.
- **P-2 (fix before k4 dispatch): the k4 DoD carries a placeholder,
  `N(test_runtime_probe_onboarding: <the functions holding :823, :1277, :1389>)`.**
  - That is not "the exact verification run" (R11). The tool passes it as plain text, so no machine catches it.
  - Fix: name the three functions. They are `every_answer_leaves_one_record_and_a_rehearsal_none` (:782),
    `k10_a_label_equal_to_head_is_matched_and_remembered` (:1240) and
    `k13_a_person_confirms_stand_reads_nothing_and_binds_the_word` (:1362).
- **P-3 (fix before dispatch): the line anchors in `test_gate_registry.py` are stale.** The card was read at 239b94ff;
  RD1-32 (t-1335) and others added lines since.

  | card | today |
  |---|---|
  | `:263` | `:265` |
  | `:298-299` | `:300-301` |
  | allow pin `:314-321` | `:316-325` |
  | NEG `:330-331` | `:334-335` |
  | F1 `:709-714` | `:712-714` |
  | F1 list `:711-714` | `:715-718` |
  | F1 loop `:717-725` | `:721-725` |
  | D13 `:1141` | `D13_ITEM_COUNT = 158` at `:1156` |
  | F2 `:770` | `:774-778` |
  | registry `provenance.environment_preparation` `:387` | `:416` |

  - The allow pin now holds 9 entries, including two `case_rollcall` entries. So §7's "then the test_identity entries
    unchanged" must read "then the test_identity and case_rollcall entries unchanged".
  - Fix: point by symbol, as R11 asks: `part_live_registry` K-T1.2/K-N2.12 block, `part_fix_pass` F1 block,
    `D13_ITEM_COUNT`, `part_predicate`.
- **P-4 (fix before k2 dispatch): `test_execution_request.py:17` is left out.** That line is
  `from profile_contract import ACCEPTS as ACCEPTS_OF_THE_PACKAGE`.
  - Its only reader is K-N2.5 `:1335`, which k2 removes. After k2 the import is unused (lint ratchet). After k4 it is an
    ImportError of a keep file, and only E-k4.5's grep would catch it.
  - Fix: list it in the k2 pins, removed together with K-N2.5.
- **P-5 (fix before k3 dispatch): k3 item 6 names `manual_evidence :17` but not `manual_capture.py:99`.**
  - Line :99 imports `ACCEPTS, acceptable_provenance` at the top. Its only reader is `:1676`, which item 4 changes, so
    after k3 the import is unused.
  - Fix: name it in item 6.
- **P-6 (fix before k3 dispatch): the AR-15 check count is wrong.**
  - Grep `target_kind.*local_source` over `P/scripts/*.py` gives **5** today, not 4. The fifth hit is
    `run_suite.py:2523`, a help-table tuple.
  - After k3 the same grep gives 2, not "that function".
  - Fix: write "before 5, after 2 (run_suite.py:2523 prose)", or narrow the pattern to `get("target_kind") == "local_source"`.
- **P-7 (recommended): the E-S7 window from k2 to k4.**
  - In that window, an unreadable registry makes `validate_request`, the fingerprint and the manual sites refuse with
    today's `refusal_text`. That text is "runtime probe returned matched: ...", which names the wrong door (FR-1, AR-9).
    The registry sentence only arrives in k4 item 3.
  - The edge is stated, not silent. But k1 already owns `profile_contract.py`.
  - Fix: move k4 item 3 into k1, so the right door exists before the first consumer reads the registry.

### Per question
- **(a) Facts.** Reproduced on main:
  - Row :37-93 is `debt`.
  - Consumer tokens :81-85. `ACCEPTS` is at profile_contract.py:877 and `acceptable_provenance` at :895-923.
  - All §0 site lines (execution_request :165/:167/:170/:176-177/:2486-2508, gate_preflight :3508/:3919,
    run_suite :938, execution_fingerprint :30/:121, manual_evidence :17/:80/:86/:89/:682/:686,
    coverage_contract :842/:848/:855/:869, manual_capture :1676, environment_preparation :388,
    driver_stage_build :390).
  - The census row at judgment-census.json:830.
  - The r2 names are absent: grep -i `provenance_word|deploy_proof|local_source_request` gives 0, control
    `baseline_identity\.readiness` gives 7.
  - The DoD test functions all exist: test_execution_request :24/:595/:693/:767/:1180, test_gate_preflight
    :4229/:4298, test_manual_capture :518.
  - Readers of `acceptable_provenance|ACCEPTS`: my grep finds the 9 script sites and 8 test files of §7, plus prose
    only. That prose is brief_pack:3702, gate_registry:42/:406, runtime_probe:57 and the package CHANGELOG.md.
  - What did not hold: P-3 (line drift) and P-6 (count).
- **(b) Spec completeness (R11).**
  - Edges, the TEMPORAL cases (E-k1.4, E-k2.3, E-k3.7, E-k4.1) and the POSITIONAL cases (E-k1.2, E-k2.1, E-k3.1) carry
    invariants. Owns, non-goals and siblings are present. `handoff:` is left to the Lead.
  - The DoD tool check: see P-1 and P-2.
  - Slow lists: `test_manual_evidence.py` and `test_environment_preparation.py` are not in slow_tests.json and are keep
    files, so running them whole is legal. `test_manual_capture.py` (8.0 s) is narrow.
  - The new functions are not census units: `provenance_word` and `local_source_request` match no `UNIT_NAME_RE` and
    never raise. So k1 owing no census row is correct.
- **(c) Siblings and pins.**
  - Named in the card: D13 at every step; the allow pin k2 +3 and k3 +4 (in site order; P-3 for the anchors); the F1
    list; K-N2.12; the split and F4 at k4; the census at k4; `tools/lint-baseline.json`.
  - Missing: P-4 and P-5.
  - test-layers: no new file. The quarantined `test_coverage_contract` rows go to the keep file `test_manual_evidence`.
  - Told-ratchet and slices are declared "unchanged". I did not measure them (estimate, not verified). No role text or
    joint is added.
- **(d) Serial or parallel.**
  - k1 must come before k2 and k3: both read `provenance_word` and `local_source_request`.
  - k4 must come after all of them: it deletes the readers' old names and converts the row.
  - **k2 and k3 can run in parallel on code.** Their scripts and test files are disjoint. The shared parts are
    `gate-registry.json` (the same row's `sites`, `accepts` and `allow`) and `test_gate_registry.py`. In that test file
    the shared parts are single literals: `D13_ITEM_COUNT`, the allow-pin list, the F1 list and the K-N2.12 tuple.
  - A parallel pair costs a merge-time rebase of those literals and a fresh D13 measurement. It saves one serial wave.
    Both steps can quote k1's frozen `old` vector.
  - Serial is therefore a cost choice (F-r2-3 (a)), not a necessity. It is the Lead's call; no finding.
- **Q4 class.** The local-source copies, the dead consumer and the prose twins are named. My grep -i of skills/ and
  references/*.md for the old names gives 0 (control: run_suite.py 3, gate-registry.json 8), so k4's prose list may be
  empty.
- **Q6 duplication.** None found. `provenance_word` reuses `validate_runtime_provenance`, `rehearsal_view`,
  `person_confirmed` and `no_changed_file`.
- **Q12 one road.** None found. No language, runner or project name is read; grepped the k1-k4 items.
- **VARIETY.** The axis 7 walk is present. An unknown value goes to the stand_identity question at stage entry, and
  every accept site refuses. No silent default.
- **Q13(d) readers block.** It was missing, so I ran `tools/owns_readers.py` on the union of the four steps' owns and
  names (base db9d9899). The result was 11 "more" lines and no other kind.
  - Answer for every line: "interface kept, except `rehearsal_probe` (loses `accepts`, k2) and `acceptable_provenance` /
    `ACCEPTS` (deleted, k4)".
  - `rehearsal_probe` readers: gate_preflight:3502, test_gate_preflight:4253, test_execution_request:1335 and
    test_launch_wrappers:168 (positional, quarantined). §7 lists all of them.
  - Misses: 3, pinned VALUE: D13 158, measured per step. 6, base: db9d9899 is origin/main, yes.
- **Q13(e) forks.** F-1 (a) is consistent with RD1-25. F-6 (a) is consistent with gate_template's own-row
  `promotable`. F-4 (a): no reader of `question_kind` or `policy_file` exists on this row.

## Q2 -- code FG7-70 (eca0c589, merge base c166611f): APPROVE WITH FIXES

The DoD keys are met:
- The refusal applies to via=cli events in `jv.FEATURE_WARN_EVENTS` with a missing or unregistered feature, and nothing
  is written. `refused()` compares the journal bytes before and after.
- Hook lines keep the WARN.
- The exact triple is skipped, with a note.
- The same task_id at another ts is still an offender.
- An empty list leaves the check unchanged.
- The rows are parameterised.

The triple was checked against `logs/journal/dev1.jsonl:3634` on origin/main: ts `2026-11-18T02:19:45`, `accepted`,
`t-1289`, with 0 `"feature"`. Control: line 3633 carries `"feature":"F19"`.

**Position.** I traced `_write_event`. `_check_feature` runs after `_prepare`, which is pure apart from cleaning text, and
after `_journal_path`, which only reads. It runs before `_pre_lock`, `_locked_counter`, the counter update and
`append_jsonl_line`. So it comes before the lock and before any side effect.

### Findings
- **C-1 (fix before merge, Q2/Q4 positional sibling): `accept --run` runs the witness BEFORE the feature refusal.**
  - `main` calls `_accept_obj`, which calls `run_witness(a.run, ...)` (up to `RUN_TIMEOUT` 600 s). Only after that does
    `write_event` reach `_check_feature`.
  - `check_notes` is deliberately placed "before a --run executes". The new check is not.
  - Input: `accept --task t-1 --agent builder --model sonnet --by opus --notes n --run "<suite>"` with no `--feature`.
    Output: the suite runs to its end, then "refused ... has no `feature`". Nothing is written, but the run is lost and
    must be repeated.
  - Fix: in `_accept_obj`, before the `--run` branch, call
    `_check_feature(root, {"event": "accepted", "feature": a.feature, "task_id": a.task}, "cli")`.
- **C-2 (fix before merge, Q2 error direction and test isolation): the `known is None` branch is not the safe side for
  this node.**
  - When both the root's and the tool checkout's `plans/features.json` are unreadable, an unregistered value is written.
    Once the registry reads again, `forge_metrics.run_check` (c) flags that line ("names feature ... that is not in")
    and it blocks every merge. That is the t-1289 class this node exists to stop, and the only remedy is a hand
    `GRANDFATHERED_EVENTS` entry.
  - The fallback reads the TOOL checkout's registry. `run_check` reads `root / REGISTRY_REL`, so these are two carriers.
  - The tests: the `repo` template writes no `plans/features.json`. So the root read gives None, and every new row (F99)
    and both rows that were edited (F19, at test_journal_hooks:168 and test_journal_write:314) go through the fallback
    to the LIVE forge registry. The template's own comment says "the tests must not depend on whose checkout runs them".
    The production path (root registry present) has no row.
  - Fix: judge against the root registry only. When it is unreadable, refuse with a door naming the unreadable registry
    (FR-41: an unknown is not a pass), unless the Lead decides to keep fail-open and says so. Also have the template
    write a minimal `plans/features.json` with F19.
- **C-3 (fix before merge, Q6 duplication): the feature predicate now lives in three places.**
  - `fv in (None, "") or fv not in known` appears in `jv.feature_warnings` (journal_validator.py:1434-1440),
    `forge_metrics.run_check` (:1626-1631) and `_check_feature` (journal_write.py:476).
  - The commit's axis-34 line says "no copy". That is true of the event set only.
  - In the same `_write_event`, the refusal judges against the root registry, while the WARN at :538
    (`jv.feature_warnings(..., known=None)`) judges against the tool registry.
  - Fix: one helper in journal_validator that both writer-path readers use, or a node the Lead opens.
- **C-4 (fix before merge, doors): the usage lines in the `journal_write.py` docstring are now wrong.**
  - Lines :5 and :7 show `delegated` and `accept` without `--feature`, which is now refused. argparse still lists
    `feature` under `opt`.
  - Grep of `(delegated|accept|defect) --(agent|task)` over tools/*.py (tests excluded), .claude, COORDINATOR.md,
    PROCESS and docs/RUNBOOK.md finds only these 2 lines; they are also the shape's positive control.
  - No repo script calls the CLI with a feature event: hook_liveness_probe:1111 only calls `clone --claim`. The hooks
    pass `via="hook"` (journal_hooks.py:257/281/304). No other test file writes such an event.
  - Fix: add `--feature Fnn` to both usage lines.
- **C-5 (the Lead's call, Q5(f) volume): tests are 39 inserted lines against 30 product lines (`--numstat`), and there is
  no `tests-over:` line.** Cut weakest first:
  - the 3 banner lines at test_forge_metrics.py:1501-1503 and the 1 at test_journal_write.py:661;
  - the `empty-list` row, which asserts the pre-change behaviour that `same-task-other-ts` already implies;
  - the `skip` assertion.
  That leaves 33 against 30. The rest is the Lead's `--tests-over` reason at merge.

### Standing lines
- **Q1 fit.** Met, apart from C-2's silent edge.
- **Q3 seams.** Additive: the return value gains `grand_notes`, which only feed warnings, and those never decide the exit.
- **Q4 class.** Of the run_check kinds, only (c) journal lines are append-only. Kinds (a), (b) and (d) can be fixed in
  place, so no exception list is owed there. **Residual:** a hook-written `delegated` with no feature still becomes a (c)
  offender that blocks merges. The hook copies `feature` only from the dispatch header (journal_hooks.py:244), and
  `check_cut` in dispatch_manifest.py does not require `feature:`. The WARN for hook lines is by the DoD, so this is no
  builder defect. Line for Остатки: `hook-written delegated without feature is a run_check (c) offender | узел: <a
  node row the Lead opens: refuse a dispatch with no feature: header in tools/dispatch_manifest.py, the door that can
  refuse>`.
- **Q5.**
  - (a) Mutants were run on a COPY (git archive of eca0c589 in the scratchpad). With the `_check_feature` call replaced
    by `pass` and the grandfather `if` replaced by `if False`: no-feature, unknown-feature and exact-triple all FAIL.
    `same-task-other-ts` and `empty-list` survive by design.
  - (b) The values trace to the DoD and to dev1.jsonl:3634.
  - (c) There are rows for the CLI refusal, the hook WARN and the note.
  - (d) The two rows edited for the new requirement are a moved pin.
  - (e) No duplicates.
  - (g) No new file.
- **Q6.** C-3.
- **Q7.** No function over 60 lines and no nesting over 3 in the new code. The predicate is copied (C-3).
- **Q8.** Not a package diff.
- **Q9 ratchets.** None touched. `GRANDFATHERED_EVENTS` is a hand-grown exception list, not in axis 18.
- **Q10.** n/a (forge tool).
- **Q11 judgment.** None.
- **Q12 one road.** None found. The hook/cli split is the DoD's own condition.
- **Witness.** I ran collect-only on the 3 files at eca0c589: 325 collected, which equals 322 passed + 3 skipped. The
  forge-check pipeline result was not attached and not read.

## Trail
- Read:
  - the card in full, and cards spec :1340-1384;
  - finding RD2-C3-k and pile row FG7-70;
  - gate-registry.json :7-93 and :404-446;
  - gate_template.py :60-106;
  - gate_registry.py :400-445, :785-810 and :903-911;
  - profile_contract.py :870-940;
  - execution_request.py :148-182 and :2486-2508;
  - gate_preflight.py :3485-3512 and :3905-3930;
  - execution_fingerprint.py :104-138;
  - manual_evidence.py :74-96 and :676-692;
  - coverage_contract.py :840-870;
  - manual_capture.py :1668-1680;
  - environment_preparation.py :380-399;
  - test_gate_registry.py :60-72, :258-340 and :704-780;
  - dispatch_manifest.py :295, :682-735, :953-1035 and :1117;
  - test_judgment_census.py :74-87 and :218-240;
  - slow_tests.json and test-layers.json (keys);
  - TESTING.md :215-224;
  - `git show eca0c589` in full;
  - journal_write.py :353-430, :465-545, :820-925 and :30-91 of the test;
  - journal_validator.py :277-279, :1392-1446;
  - forge_metrics.py :1545-1642.
- Reruns (all in the JSON block).

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "class_completeness": "Plan: local-source copies, dead consumer, prose twins named; missed import siblings test_execution_request.py:17 (P-4) and manual_capture.py:99 (P-5). FG7-70: only run_check kind (c) is append-only, so the exception list is owed there alone; residual sibling = hook-written delegated without feature (journal_hooks.py:244, dispatch_manifest.check_cut requires no feature: header) still a merge-blocking (c) offender -- a node for the Lead.",
  "fixes": [
    "P-1 (blocks the k1 dispatch) card k1 DoD: unquote the not-run-locally line; dispatch_manifest refuses it (exit 2, canon-only files run whole)",
    "P-2 card k4 DoD: name every_answer_leaves_one_record_and_a_rehearsal_none, k10_a_label_equal_to_head_is_matched_and_remembered, k13_a_person_confirms_stand_reads_nothing_and_binds_the_word",
    "P-3 card k1-k4: re-anchor test_gate_registry.py pins by symbol (lines drifted since 239b94ff; allow pin now 9 entries incl. case_rollcall)",
    "P-4 card k2 pins: drop test_execution_request.py:17 ACCEPTS import with K-N2.5",
    "P-5 card k3 item 6: name manual_capture.py:99 import",
    "P-6 card AR-15 check: before 5 / after 2 (run_suite.py:2523 prose) or narrow the pattern",
    "P-7 (recommended) move k4 item 3 (refusal_text registry_why) into k1",
    "C-1 journal_write.py::_accept_obj: feature check before run_witness",
    "C-2 journal_write.py::_check_feature: root registry only, refuse on unreadable (or Lead states fail-open); test template writes plans/features.json",
    "C-3 one feature predicate helper in journal_validator for _check_feature and feature_warnings (or a node)",
    "C-4 journal_write.py docstring :5/:7 add --feature Fnn",
    "C-5 tests 39 vs 30 product lines: cut banners, empty-list row, skip assertion; the rest is the Lead's --tests-over reason"
  ],
  "trail": {
    "read": [
      "docs/tasks/specs/20261118-rd1-14-c3-k-provenance-acceptance-card.md",
      "docs/tasks/specs/20261117-rules-debt-phase2-cards-spec.md:1340-1384",
      "plans/piles/rules-debt/findings/20261117-rd2-c3-k-provenance-acceptance.md",
      "plans/piles/forge/batch-7-vhodyashchie-4.md:95",
      "ai-packages/qa-factory/references/gate-registry.json:7-93,404-446",
      "ai-packages/qa-factory/scripts/gate_template.py:60-106",
      "ai-packages/qa-factory/scripts/gate_registry.py:400-445,785-810,903-911",
      "ai-packages/qa-factory/scripts/profile_contract.py:870-940",
      "ai-packages/qa-factory/scripts/execution_request.py:148-182,2486-2508",
      "ai-packages/qa-factory/scripts/gate_preflight.py:3485-3512,3905-3930",
      "ai-packages/qa-factory/scripts/execution_fingerprint.py:104-138",
      "ai-packages/qa-factory/scripts/manual_evidence.py:74-96,676-692",
      "ai-packages/qa-factory/scripts/coverage_contract.py:840-870",
      "ai-packages/qa-factory/scripts/manual_capture.py:1668-1680",
      "ai-packages/qa-factory/scripts/environment_preparation.py:380-399",
      "ai-packages/qa-factory/scripts/tests/test_gate_registry.py:60-72,258-340,704-780",
      "tools/dispatch_manifest.py:295,682-735,953-1035,1117",
      "eca0c589 tools/journal_write.py, tools/forge_metrics.py, tools/journal_validator.py, tools/test_journal_write.py (windows)",
      "docs/TESTING.md:215-224"
    ],
    "reruns": [
      {"command": "dispatch_manifest.check on card k1..k4 header blocks (scratch dm_probe.py)", "result": "k1 exit 2 DOD-RUN REFUSED canon-only files whole; k2/k3/k4 exit 0; k1 with span unquoted (0, ''); NEG --witness-for exit 2"},
      {"command": "grep target_kind.*local_source P/scripts/*.py", "result": "5 hits (coverage_contract 848, 869; execution_request 165; manual_evidence 80; run_suite 2523)"},
      {"command": "grep -i provenance_word|deploy_proof|local_source_request over package; control baseline_identity.readiness", "result": "0; control 7"},
      {"command": "python -B tools/owns_readers.py --paths <union of k1-k4 owns> --names <card names>", "result": "base db9d9899; 11 more lines, no other kinds"},
      {"command": "pytest -k fg7_70 on a git-archive COPY of eca0c589 (test_journal_write, test_forge_metrics)", "result": "6 passed"},
      {"command": "same on the COPY with _check_feature call -> pass and grandfather if -> if False", "result": "3 failed (no-feature, unknown-feature, exact-triple), 3 passed; 1 error (journal_hooks row needs package files absent from the copy); copy restored, sha256 equal"},
      {"command": "pytest --collect-only on the 3 witness files at eca0c589 (copy)", "result": "325 collected = 322 passed + 3 skipped"},
      {"command": "git diff --numstat c166611f eca0c589", "result": "product +30, tests +39; tests-over line count 0"},
      {"command": "sed -n 3634p logs/journal/dev1.jsonl on origin/main", "result": "ts 2026-11-18T02:19:45 accepted t-1289, no feature; line 3633 control has F19"}
    ]
  }
}
```
