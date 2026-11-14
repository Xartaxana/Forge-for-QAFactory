# P1B-9 plan critic (t-800) — review of `docs/tasks/specs/20261114-p1b-9-runtime-provenance-null-outcome-spec.md` (t-790)

VERDICT: GO WITH FIXES — 2 blockers (B1, B2) to fix in the spec before any builder dispatch; 9 should-fixes.
The mechanism (F1 = (a): one writer, one kind of record) is right, and so is its error direction. But two facts the cards
rest on are wrong when checked against main:
- B1: the deriver's "newest record" is really "last by file name". With the S2 suffix and the new A3/A5 files, that
  ordering names the wrong record.
- B2: C2's filter turns a keep-layer fixture red, and the cards don't name it.
This verdict is an input to acceptance. Acceptance and the fork decisions stay with Lead.

Product tree checked: `C:\QAFactory\forge-repo\.claude\worktrees\wave13` (origin/main). Paths below are relative to
`ai-packages/qa-factory/` unless they say otherwise.

---

## K1 — Facts by trail: PASS on substance, with line drift and two missed facts

Spot-checked on main (each claim re-read, not taken from the plan):

| plan claim | main evidence | result |
|---|---|---|
| A3 at `:1660-1669`, "No rung, no write" at `:22` and in the comment at `:1663-1664` | `scripts/runtime_probe.py:1660-1669` (comment 1661-1664, `print` 1668, `return 0` 1669); `:22` "No rung, no write." | PASS |
| A4 at `:1670-1675` | `runtime_probe.py:1670-1675` (`reason_code = NO_EXPECTED_REVISION`, print, return) | PASS |
| A2 `reference_skip` at `:1568-1587`, printed at `:1635-1638` | `runtime_probe.py:1568-1587`, `1635-1638` (`evidence_refs: []`, no write) | PASS |
| A5 `finish` writes only for the three answers | `runtime_probe.py:1276-1282` (`unknown` -> `finish_unknown`; write only for matched/mismatched/person_confirmed) | PASS |
| `write_evidence` at `:1324-1334`, name at `:1331`, refs at `:1332` | `runtime_probe.py:1324-1334`; refs set BEFORE the write, as an absolute `as_posix()` | PASS |
| `_runtime_provenance` at `:514-518`, three keys at `:577/578/583` | `scripts/handoff_check.py:514-518`, `576-583` | PASS (but see B1: "newest" is false) |
| blank -> `Problem(..."not filled")` | `handoff_check.py:1587-1593`; deriver call at `1568-1575` | PASS |
| `recorded_checkout_revisions` at `:722-739`, read by `validate_manual_current` `:830-833` | `scripts/coverage_contract.py:722-739`, `830-833` | PASS, incomplete: it has a SECOND caller, `scripts/manual_evidence.py:108,128-132` (`other_profiles[]`). The C2 filter sits inside the function, so it covers both callers; the inventory of §1.3 is short by one row |
| `no_runtime_record` reserved, `impl None`, refused by `entry_problems` | `scripts/null_outcomes.py:164`; `:299-300` (status != live -> refused); `:281-283` (REQUIRED_LISTS only) | PASS |
| `Driver.walk_run_values` at `driver_dispatch.py:1559/1568` | on main: `scripts/driver_dispatch.py:1580` (glob) and `:1589` (`inputs_read[2].path`) | drift (p1b-n3 line numbers) |
| `null-outcomes.json:185,186,191` | on main: `references/null-outcomes.json:177,178,183` | drift |
| `slow_tests.json:119` = `test_scenario_dry_1.py` 51 s | on main `scripts/slow_tests.json:119` is `test_scenario_local_1_0108.py`; `test_scenario_dry_1.py` does not exist on main (it exists only in worktree p1b-n3) | wrong for main |
| `profile_contract.ACCEPTS` `:875`, `acceptable_provenance` `:893-921` | `scripts/profile_contract.py:875`, `893-921` | PASS |

The negative claim "only four non-test readers glob these files", re-run myself:
- Grep `runtime[-_ ]provenance` (case-insensitive) over the package, excluding `**/tests/**`. Positive control in the
  same call: it found the writer `runtime_probe.py:1331` and `handoff_check.py:515`. Glob readers in `scripts/`: exactly
  three (`handoff_check.py:515`, `coverage_contract.py:730`, `driver_dispatch.py:1580`) plus the registry string at
  `null_outcomes.py:164`. So "four" means three readers plus one registry row. Substantively the claim is right inside
  the package.
- Grep `["']runtime-|provenance-\{|-provenance` (case-insensitive): no constructed-name reader beyond those.
- **Missed outside `scripts/`**: `experiments/measurers/check_all_contracts.py:285-290` globs
  `evidence/runtime-provenance-*.json` (control: the same Grep over `experiments/` found it). The plan searched
  `scripts/*.py` only. See K2 row 5.

## K2 — Any reader that takes "a file exists" as "the build was established": PASS for code. FAIL on two points: B1, and should-fix S1 (contract texts)

No CODE reader turns the presence or path of a `runtime-provenance-*.json` file into a verified build. The full list:

| # | reader | file:line | what it does with the file | C2-style result filter owed? |
|---|---|---|---|---|
| 1 | `handoff_check._runtime_provenance` (3 S5 keys) | `scripts/handoff_check.py:514-518`, `576-583` | names `records[-1]` by NAME order (`hooklib.sorted_paths`, code-point order: `scripts/hooklib.py:900-915`); never opens it | No. Filtering by `result` would bring the gap back. What is owed is BINDING to the window's run: **B1** |
| 2 | `Driver.walk_run_values` | `scripts/driver_dispatch.py:1580,1589` | `inputs_read[2].path` = last by name, any profile; `version` comes from the case probes (`:1568`), not from the file | No filter. Same last-by-name defect as row 1 (B1 class, queue it with L-2) |
| 3 | `coverage_contract.recorded_checkout_revisions` (callers `coverage_contract.py:830-833` and `manual_evidence.py:128-132`) | `scripts/coverage_contract.py:730-738` | turns the `expected_source_revision` of every file of the profile into a binding set; today it drops only `unknown` | YES. This is the one reader where a newly written A3/A5 record (A3 and A5 carry the 40-hex checkout HEAD, `runtime_probe.py:1648-1655`) would bind a manual proof. C2 covers it inside the function, so both callers are covered |
| 4 | `null_outcomes.CONDITIONS["no_runtime_record"]` | `scripts/null_outcomes.py:164` | a registry string, never evaluated (reserved) | n/a. But see K5 (P31 residual) |
| 5 | measurer `s5_automator_to_critic` | `experiments/measurers/check_all_contracts.py:285-290` | counts the files and describes them as "provenance records exist (expected_source_revision + observed_runtime_identity)" | Outside the package: after F2 (ii) the count includes unverified answers and the label goes stale. Should-fix S9 (filter or relabel), not a blocker |
| 6 | qa-collect index | `references/collect-sets.json:12,39` (B11 `mode: index`: path, bytes, sha256) | indexes; never interprets | No |
| 7 | delivery manifest | `scripts/delivery_manifest.py:3,104` (`evidence/**` excluded) | excludes | No |
| 8 | contract texts and role slices | `handoffs/s5-automator-to-critic.yaml:58-60` ("The identity of the stand these instances ran against … `runtime_probe.py` writes it"), `handoffs/s5-automator-to-runner.yaml:25-26` ("the identity of the stand the evidence was taken on"), `:60-64`, `handoffs/s5-critic-to-automator.yaml:55`, `handoffs/s6-runner-to-analyst.yaml:41`, `handoffs/s7-analyst-to-automator.yaml:74`, `references/slices/qa-automator/handoff-keys.md:30`, `references/slices/qa-code-critic/handoff-keys.md:32` | tell the receiving ROLE that the named file IS the stand's identity | A judgment reader (P27). After F2 (ii) the named file can say `not_applicable` or `unknown`, and these texts then mislead a Sonnet role into reading "a record exists" as "the stand was identified". The plan only asks this as Q-L3 ("not in this node's owns"). It should be a line in each `what:` / comment, in this node or a named sibling node: **S1** |

Hooks and guards: no `guard_*.py`, `stage_guard.py` or `hooklib.py` names the file family. The same Grep over
`scripts/` (non-test) showed no guard hit. `hooks/` holds only `hooks.json`, `codex.json` and `run-py.cmd` (control:
Grep `PreToolUse|python` over `hooks/` found those three files). Forge `tools/`: no hit (control: `journal[-_]validator`
found `tools/journal_validator.py`).

Inline record readers (`evidence_refs` of the INLINE record): see K4. None takes a non-empty `evidence_refs` as proof.

## K3 — Invariants I-1..I-5: FAIL (only I-3 and I-4 are fully protected by rows)

| inv | protecting row | status |
|---|---|---|
| I-1 (`not_applicable` / `unknown` never read as `matched`) | C3 `unknown-file` row (claims unchanged). Nothing pins the RUN-PATH half on a WRITTEN record, which now carries `evidence_refs: [path]`. `test_profile_contract.py` is quarantined (`scripts/tests/test-layers.json:9150`), so no kept file covers it | **stated only** for the run path. Add a C1 row: `acceptable_provenance(written A5, ACCEPTS) is False`, `(written A4) is False`, `(written A3) is True` (S2) |
| I-2 (rehearsal writes nothing) | C1 `a3-rehearsal` only | **partial**: no A4/A5 rehearsal row, though C1 item 3 adds writes on both paths (S3) |
| I-3 (A2 never story evidence) | C1 `a2-reference` | protected |
| I-4 (binding set unchanged) | C2 table | protected (it narrows hand-written no-`result` files; the error direction is refusal) |
| I-5 (never overwrite) | C1 `collision`: two sequential runs, frozen clock | **partial**: (i) S2 "takes the next free suffix" is check-then-write. Two processes in one second (parallel S5 windows exist: `test_s5_parallel_admission.py`) can both pick the same free name and overwrite. The spec must say exclusive create (`open(..., "x")` / `O_EXCL` loop). (ii) Nothing covers the `-99` bound. (iii) The suffix ordering defeats the deriver: **B1** |

## K4 — Error direction of the fork decisions: PASS for F1, F2, F4, F5. FAIL for F3 (B1)

- **F1 (a)**: errs toward naming a record that says `not_applicable` / `unknown`, never a fabricated path, never
  `matched`. Safe.
- **F2 (ii)**: errs toward recording more. Safe. The rationale overclaims, though. A window whose run was refused on
  `unknown` (A4/A5, `ProvenanceRefused` at `scripts/run_suite.py:925-929`) has no summary, so `_run_witness`
  (`handoff_check.py:139-154`) returns None unless every test is pending. `artifacts.run_witness` is required
  (`handoffs/s5-automator-to-critic.yaml:63`), and S5 contracts carry no `required_when` (Grep `required_when` over
  `handoffs/`: only s4-case-critic, s7 x2 and s8; control positive). That window still stops. F2 (ii) removes one of its
  two blanks, not the stop (K7). The decision stands; the text of F2 must not claim otherwise (S6).
- **A5 written with `evidence_refs: [own path]`, copied inline**: no inline reader treats a non-empty `evidence_refs` as
  proof.
  - `profile_contract.validate_runtime_provenance:741-743`: the refs rule applies only when `declared == "matched"`.
  - `:763`: content binding also needs `technical` and `verified_content`.
  - `acceptable_provenance:911-921`: by `result` only. `no_changed_file:715-716`: by `result` and `reason_code`.
  - `run_suite.py:488`: `result == "matched" and evidence_refs`.
  - `report_facts._person_build:235-243`: `person_confirmed` only.
  - `proof_level.py:1791-1802`: `observed_runtime_identity` / `environment_id` only.
  - `window_record.py:512-522,537`: run block and `environment_id` only.
  - `baseline_contract.py:21,83,141-142`: revision and identity fields.
  - `execution_request.py:151-173`: validator + acceptance. `:374-377` strips `timestamp` and `evidence_refs` from the
    fingerprint material, so the fingerprint does not change.
  - `execution_fingerprint.py:115-124`: validator + acceptance.
  - `manual_evidence.py:79-95,681-687`: validator.
  - `environment_preparation.py:69-71` reads a different record shape (`observed_at`, `source_revision`).
  - A5 is never in a run block anyway: refused before the run.
- **F3 (i)**: errs toward naming the wrong record, and more often than the plan says. See B1. Not safe as decided.
- **F4 (i)**: neutral. `test_scenario_dry_1.py` does not exist on main, so there is nothing to assert there.
- **F5 (ii)**: the row names the last blocker (TC-2), with P1B-9 in its note. It stays true across both landings.
  `known_red.py` (p1b-n3) `:141` flags a row only when it turns green, so a P1B-9-named row would be wrong but not
  caught. (ii) is the safer choice.

## K5 — Architecture and principles: PASS with one P31 residual to queue

- AR-14 / P31: (a) leaves ONE writer (`runtime_probe.py`, one site per S1) and ONE kind of record (the printed record,
  byte-equal on disk) for every non-rehearsal answer. Yes.
  - A2 is excluded with a quoted owner word: W1, carrier `docs/SIBLING_MAP.md:614` ("a run on the reference stand is a
    sample, never story evidence"), verified. Rule 19 is satisfied.
  - The writer registry has no row for this family. `references/artifact-writers.json:184-193` registers
    `work/evidence/`, while the probe writes `<task>/evidence/runtime-provenance-*.json` (`runtime_probe.py:1331`).
    Siblings in the same folder have their own rows: `evidence/diagnostic-*.json` `:176`,
    `evidence/place-answer-*.json` `:243`. L-4 is real. It is a one-row data fix, and the plan should fold it into C1
    (S4), because the guard reads this registry (`scripts/guard_pre_tool.py:778-784,981`). Whether that row also closes
    L-3 is a question for the builder or a scout.
- **Reserved `no_runtime_record` beside (a)** = a latent second road. After (a), "no file" can only mean "never
  probed", which is already `no_run_in_dispatch` (`null_outcomes.py:165`). If t-305 N2 later implements
  `no_runtime_record` for the three carriers, a null answer would get two roads: an empty field under a declaration, or
  a record on disk. Under rule 19 this residual must leave as a fix or a proposed node with an owner. Proposed: a queue
  line to t-305 N2: retire `no_runtime_record`, or re-scope it to "never probed" and merge it with
  `no_run_in_dispatch` (S5).
- AR-13: three glob readers, no survivor (L-2). After B1 the binding wants one reader function. Recommend it as the
  B1 fix (see Fixes).
- AR-22, AR-23, AR-25, AR-28, AR-29: the plan's lines hold. C2 is a data check, class xref.
- FR-5 / FR-23: closed for A3. For A4/A5 the field closes but the window does not (K7).
- FR-40, FR-41 (the written `unknown` says unknown), FR-45 (rehearsal path `runtime_probe.py:560-591` untouched),
  FR-59: hold.
- P27: code writes the data, the role reads `result`. This holds only if the role is told the record can say
  `not_applicable` / `unknown` (S1).

## K6 — Cards as dispatch material for a weaker model: FAIL (B1, B2, plus edge gaps)

- **Owns disjoint**: yes. C1 = `runtime_probe.py`, `test_runtime_probe_onboarding.py`, changelog. C2 =
  `coverage_contract.py`, `test_manual_evidence.py`. C3 = `test_handoff.py`.
- **Layers**: `test_runtime_probe_onboarding.py` (test-layers keep `:4719`, 12.0 s), `test_manual_evidence.py` (keep
  `:3035`, not in `slow_tests.json`, so fast) and `test_handoff.py` (keep `:2295`, 56.8 s) are all kept, not
  quarantined. `test_coverage_contract.py` is quarantined (`:7819`), as the plan says.
  - `test_handoff.py` at 56.8 s, with `max_drift: 5` (`slow_tests.json:8`), sits at the one-minute line. Three new
    `--fix` rows can push it over. Consider `test_handoff_values_main_block.py` (10.3 s) for C3 (S7).
- **B2 (blocker)**: C2's "no `result` -> not counted" breaks a keep-layer fixture nobody owns.
  `scripts/tests/test_manual_capture.py:1351-1363` (`seed_runtime_records`, keep `:3003`) writes
  `runtime-provenance-{profile}.json` with `{"profile_id", "expected_source_revision"}` only, no `result`. After C2,
  its manual `build` cases lose their binding and turn red. That file is not in any card's owns and is not named as an
  expected flip. Fix: add `test_manual_capture.py` to C2's owns (the seed gets `"result": "matched"`) and name the flip.
- **B1 (blocker)** concerns S2 together with F3 and §1.3, measured below.
- **Edges its own requirements create, stated?**
  - `--no-evidence`: stated. Rows only for A3 (S3).
  - TEMPORAL: stated, both worlds.
  - POSITIONAL: stated for A3 (after `reference_skip`, after the `has_diff` test: holds at `runtime_probe.py:1635-1638`
    and `1660`). **Not stated for A5**: the write must come AFTER `finish_unknown` (`:1285-1322`), so the file holds
    `tried`, `error` and `remedy`. Only `a3-writes` asserts "JSON equals the printed record"; `a4-writes` and
    `a5-writes` must assert it too (S3).
  - `-99` bound: stated for new answers (S3 soft path). **Unstated for A6-A8**: S1 routes them through the same
    `write_record` with S2, while S3 says "A6-A8 keep today's behaviour on a failed write". What happens to a `matched`
    at suffix `-100` (raise, overwrite, soft)? This is a conflicting pair of the spec's own requirements (S8). A test
    AT/BEYOND the bound is not owed (an internal limit, CLAUDE.md rule 11), but the behaviour must be written down.
  - Write failure: stated (S3). The order is right: `evidence_refs` is set before the write today (`:1332`), so the soft
    path must reset it to `[]`. The spec says so.
- **Line drift**: the cards cite p1b-n3 line numbers while claiming "main-identical" (K1 table). Re-point them to main
  (S10).

## K7 — Class-wide completeness

Same class (a tool's legitimate null answer leaves a required S5 handover field that nothing can produce):
- `artifacts.run_witness` / `run.witness` for a run refused by `ProvenanceRefused` (A4, A5, or a `mismatched` that is
  refused). See `handoff_check.py:139-154`: None unless all tests are pending. Required at
  `s5-automator-to-critic.yaml:63`. No `required_when` in S5 contracts. Not queued by the plan, and it is exactly the
  window F2 (ii) claims to free. **Needs a queue line** (S6).
- `claims.every_instance_names_its_current_case_version` -> None (`handoff_check.py:641-642`, per plan §1.6). Queued as
  L-1.
- `Driver.walk_run_values` already uses a declared `-` for no file (`driver_dispatch.py:1589`). Not this class.
- `runtime.application_build` (`s5-automator-to-runner.yaml:66`) has no deriver. It is role-typed, not a code stop.
  Noted, not this class.

Queue lines L-1..L-5:
- **L-1**: real, separate class, correctly kept out of this node.
- **L-2**: real, but its premise is wrong. It is not "the newest of any profile/window" but "the last by name": the
  profile name sorts first, the stamp second (B1). Re-word it, or absorb it into the B1 fix.
- **L-3**: real (no guard names the family; Grep confirmed). It probably shares its root with L-4. Merge them into one
  line, or fold both into C1 via the writer row.
- **L-4**: real. Verified at `references/artifact-writers.json:184-193` vs `runtime_probe.py:1331`.
- **L-5**: plausible. In `handoff_check.py` I found only other `is_file()` sites (`:169,555,869`). I did not check
  `story_step.py`.
- **Missing**: L-6, retire or re-scope `no_runtime_record` (owner t-305 N2, K5). L-7, the `run_witness` sibling above.
  Also turn Q-L3 into a node or card for the contract texts (S1).

---

## Fixes the plan needs before a builder

1. **B1 (blocker)**: contradicts plan lines 47 ("newest file by `sorted_paths`"), 145-149 (F3: "the ambiguity exists
   today…; an analog, not created by this node") and 163-164 (S2).
   - `hooklib.sorted_paths` orders by code point (`hooklib.py:900-915`). Measured with the real function:
     - `[…api-20261114T120000Z.json, …api-20261114T120000Z-2.json, …api-20261114T120000Z-10.json,
       …e2e-ui-20261101T000000Z.json, …api-20261114T130000Z.json]` -> last = `runtime-provenance-e2e-ui-20261101T000000Z.json`.
     - The three same-second api names sort as `[…Z-10.json, …Z-2.json, …Z.json]`.
   - So (i) the deriver names the alphabetically last PROFILE's record, not the newest. (ii) S2's suffix makes the
     FIRST record of a second the "newest".
   - With F2 (ii) this becomes a new mis-naming, not an analog. Example: a backend-only story whose `e2e-ui` checkout is
     untouched. Every manual-capture or red probe of `e2e-ui` now writes an A3 file, and the api window's
     `artifacts.runtime_provenance` names the `e2e-ui` `not_applicable` record for good. The critic is told "the stand
     these instances ran against" is a probe that "does not apply". Today that A3 writes nothing and the api `matched`
     record is named.
   - Fix: choose F3 (ii) now. S4 makes it cheap: every written record's path rides inline in the run block's
     `runtime_provenance.evidence_refs[0]`. Bind to the window's latest run block. With no run block, use the latest by
     the record's `timestamp` field among the window's profiles. With none, return None.
   - Fix S2 so ordering never depends on the suffix (exclusive create plus a zero-padded suffix always present, or a
     sub-second stamp), and add a row for it.
   - Apply the same reader to `driver_dispatch.py:1580`.
   - This adds code in `handoff_check.py` (C3 owns) and a reader function (one survivor, AR-13).
2. **B2 (blocker)**: contradicts plan lines 222-238 (C2 owns, edges "a record with no `result`: not counted").
   `scripts/tests/test_manual_capture.py:1351-1363` (keep) seeds no-`result` records. Add it to C2's owns with the seed
   fixed, and name the flip. Also add `manual_evidence.py:128-132` to the §1.3 caller list.
3. **S1 (should)**: one line in each contract `what:` / comment listed in K2 row 8, saying the record can say
   `not_applicable` / `unknown` and the role reads `result`. Make it a card or a named node, not Q-L3.
4. **S2 (should)**: C1 rows pinning I-1 on WRITTEN records (`acceptable_provenance` False for A4/A5, True for A3).
5. **S3 (should)**: A4/A5 `--no-evidence` rows (I-2). `a4-writes` / `a5-writes` assert file == printed record.
   POSITIONAL: the A5 write comes after `finish_unknown`.
6. **S4 (should)**: fold L-4 into C1 (one `artifact-writers.json` row `evidence/runtime-provenance-*.json`, writer
   `runtime_probe.py`), and check whether it closes L-3.
7. **S5 (should, rule 19)**: queue L-6, retire or re-scope `no_runtime_record`, owner t-305 N2.
8. **S6 (should)**: correct F2's rationale (lines 140-142) and queue L-7 (`run_witness` for a refused run).
9. **S7 (should)**: C3 rows in a smaller kept file, or a measured note that `test_handoff.py` stays under 60 s.
10. **S8 (should)**: state the A6-A8 behaviour beyond `-99` (conflict between S2 and S3).
11. **S9 (should)**: the measurer at `experiments/measurers/check_all_contracts.py:285-290`: relabel or filter by `result`.
12. **S10 (should)**: re-point line refs to main (driver_dispatch 1580/1589; null-outcomes.json 177/178/183;
    slow_tests.json has no `test_scenario_dry_1.py` on main).

DUPLICATION AND CONSISTENCY: one finding. C2's new constant of "the three answers written before" adds a second list of
result words beside `profile_contract.PROVENANCE_RESULTS` / `ACCEPTS`. Keep it next to the writer's survivor (the B1
reader function) or `profile_contract`, never a private list in `coverage_contract`. Grepped: `PROVENANCE_RESULTS`,
`ACCEPTS` (`profile_contract.py:875`).

CODE QUALITY (plan level): the three glob readers have no survivor (AR-13). B1 is the place to create one. Nothing else
found. Grepped: `runtime-provenance` readers (K1).

ONE ACTION, ONE ROAD (P31): (a) is the one road. A2's exclusion carries the owner's word (SIBLING_MAP:614). The
residual (reserved `no_runtime_record`) is proposed as node L-6, owner t-305 N2 (S5). No blocking exclusion.

---

## Trail

Read in full: the plan (348 lines).

Read on main (worktree wave13):
- `scripts/runtime_probe.py`: 1-70, 1260-1339, 1560-1699
- `scripts/handoff_check.py`: 139-178, 505-606, 1555-1599
- `scripts/null_outcomes.py`: 140-309
- `scripts/coverage_contract.py`: 718-842
- `scripts/profile_contract.py`: 709-727, 728-927
- `scripts/driver_dispatch.py`: 1545-1594
- `scripts/manual_capture.py`: 1495-1624
- `scripts/manual_evidence.py`: 100-135
- `scripts/probe_by_code.py`: 2865-2924
- `scripts/run_suite.py`: 912-931
- `scripts/proof_level.py`: 1780-1803
- `scripts/report_facts.py`: 220-259
- `scripts/window_record.py`: 512-542
- `scripts/environment_preparation.py`: 55-84
- `scripts/execution_request.py`: 3258-3277
- `scripts/guard_pre_tool.py`: 1225-1284
- `handoffs/s5-automator-to-runner.yaml` (whole), `handoffs/s5-automator-to-critic.yaml`: 1-90
- `references/environment-preparation.md`: 44-57
- `references/artifact-writers.json`: 170-194
- `scripts/slow_tests.json` (whole)
- `scripts/tests/fixtures/driver-exits/known_red.json` (whole)
- `scripts/tests/test_manual_evidence.py`: 1-40
- `scripts/tests/test_manual_capture.py`: 1340-1369
- `scripts/tests/test_stand_identity.py`: 755-799
- `scripts/tests/test_story_run_stand_identity.py`: 565-599
- `experiments/measurers/check_all_contracts.py`: 270-309

Also read:
- the source report line 15 / Q2 (`worktrees/p1b-n3/docs/tasks/specs/reports/20261114-p1b-n2f-report.md`)
- `docs/SIBLING_MAP.md:614`
- p1b-n3 `scripts/tests/known_red.py` (stale lines)
- `tools/critic_verdict.schema.json`

Greps, each with its control:
- `runtime[-_ ]provenance` -i, package, not tests. Control: found writer `:1331` and `handoff_check:515`.
- `["']runtime-|provenance-\{|-provenance` -i. Control: same hits as above.
- `evidence["/)]…glob|iterdir|evidence_dir|evidence/\*` -i. Control: found `coverage_contract:730`.
- `runtime[-_]provenance` in `experiments/measurers` (hit), in forge `tools/` (none; control `journal[-_]validator`
  found), in `hooks/` (none; control `PreToolUse|python` found 3 files).
- `provenance` -i in `skills/` (hits) and `agents/` (none; control `runtime|build` found qa-runner/qa-code-critic lines).
- `evidence_refs` -i, package. Every runtime-provenance consumer was checked against `result` gating.
- `--no-evidence`, `rehearsal_argv|probe_runtime|runtime_probes`, `ProvenanceRefused` in `run_suite`,
  `recorded_checkout_revisions` (found the second caller), `required_when` over `handoffs/` (4 files, none S5:
  control positive), `application_build`, `def sorted_paths`, `def no_changed_file`.
- test-layers keep/quarantine rows; `runtime-provenance-` in `scripts/tests/test_*.py`.

Reruns:
- One pure-read probe of `hooklib.sorted_paths` (command and output in the json block).
- No test, CI or mutation run (out of scope).

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "B1: plan lines 47, 145-149, 163-164 rest on a false premise: handoff_check._runtime_provenance (handoff_check.py:514-518) takes the LAST BY NAME via hooklib.sorted_paths (code-point order, hooklib.py:900-915), i.e. the alphabetically last profile, not the newest; S2's -<n> suffix sorts before the unsuffixed name, so the newest in one second is never last. With F2 (ii) new A3/A5 files of other profiles mask the window's own record (new, not an analog). Fix: F3 (ii) via the run block's inline evidence_refs[0] (made reliable by S4), timestamp-field ordering among the window's profiles, a suffix scheme that cannot reorder, one reader function also used by driver_dispatch.py:1580.",
    "B2: plan lines 222-238 (C2) flip a keep-layer fixture they do not own: scripts/tests/test_manual_capture.py:1351-1363 seeds runtime-provenance files without result; under C2 they no longer bind and manual build cases turn red. Add the file to C2 owns with the seed fixed, and name the flip; also list manual_evidence.py:128-132 as the second caller of recorded_checkout_revisions."
  ],
  "class_completeness": "Same class as the gap: artifacts.run_witness / run.witness stay blank for a run refused by ProvenanceRefused (handoff_check.py:139-154; required at s5-automator-to-critic.yaml:63; no required_when in S5 contracts), so F2 (ii) frees the provenance field but not that window: queue L-7. P31 residual: reserved no_runtime_record (null_outcomes.py:164) becomes a latent second road: queue L-6 to t-305 N2 (retire or merge with no_run_in_dispatch). L-1..L-4 real (L-2 re-worded: last by name, not newest; L-3 and L-4 likely one root: the missing artifact-writers row); L-5 plausible, not fully verified. Contract and slice texts (K2 row 8) need a line that the record may say not_applicable/unknown: make Q-L3 a card or node.",
  "trail": {
    "read": [
      "docs/tasks/specs/20261114-p1b-9-runtime-provenance-null-outcome-spec.md (whole)",
      "wave13 ai-packages/qa-factory/scripts/runtime_probe.py 1-70, 1260-1339, 1560-1699",
      "wave13 scripts/handoff_check.py 139-178, 505-606, 1555-1599",
      "wave13 scripts/null_outcomes.py 140-309",
      "wave13 scripts/coverage_contract.py 718-842",
      "wave13 scripts/profile_contract.py 709-927",
      "wave13 scripts/driver_dispatch.py 1545-1594",
      "wave13 scripts/manual_capture.py 1495-1624",
      "wave13 scripts/manual_evidence.py 100-135",
      "wave13 scripts/probe_by_code.py 2865-2924",
      "wave13 scripts/run_suite.py 912-931",
      "wave13 scripts/proof_level.py 1780-1803",
      "wave13 scripts/report_facts.py 220-259",
      "wave13 scripts/window_record.py 512-542",
      "wave13 scripts/environment_preparation.py 55-84",
      "wave13 scripts/execution_request.py 3258-3277",
      "wave13 scripts/guard_pre_tool.py 1225-1284",
      "wave13 handoffs/s5-automator-to-runner.yaml, s5-automator-to-critic.yaml 1-90",
      "wave13 references/artifact-writers.json 170-194, references/environment-preparation.md 44-57",
      "wave13 scripts/slow_tests.json, scripts/tests/fixtures/driver-exits/known_red.json",
      "wave13 scripts/tests/test_manual_evidence.py 1-40, test_manual_capture.py 1340-1369, test_stand_identity.py 755-799, test_story_run_stand_identity.py 565-599",
      "wave13 experiments/measurers/check_all_contracts.py 270-309",
      "p1b-n3 docs/tasks/specs/reports/20261114-p1b-n2f-report.md line 15 and Q2; p1b-n3 scripts/tests/known_red.py stale lines",
      "docs/SIBLING_MAP.md:614"
    ],
    "reruns": [
      {
        "command": "python -B -c (import hooklib.sorted_paths from wave13 scripts; sort five runtime-provenance names: api 120000Z, api 120000Z-2, api 120000Z-10, e2e-ui 20261101, api 130000Z)",
        "result": "last = runtime-provenance-e2e-ui-20261101T000000Z.json; same-second api order = [Z-10.json, Z-2.json, Z.json]"
      },
      {
        "command": "Grep runtime[-_ ]provenance -i over the package excluding tests (control: writer runtime_probe.py:1331 found)",
        "result": "glob readers: handoff_check.py:515, coverage_contract.py:730, driver_dispatch.py:1580; registry null_outcomes.py:164; outside package: experiments/measurers/check_all_contracts.py:285"
      }
    ]
  },
  "fixes": [
    "B1: bind the deriver to the window's run (F3 (ii)) via the inline evidence_refs[0], timestamp-field ordering among the window's profiles, a non-reordering suffix with exclusive create, one reader function shared with driver_dispatch.py:1580",
    "B2: add scripts/tests/test_manual_capture.py to C2 owns (seed gets result matched), name the flip, list manual_evidence.py:128-132 as a caller",
    "S1: a line in each contract/slice text of K2 row 8 that the record may say not_applicable/unknown and the role reads result",
    "S2: C1 rows: acceptable_provenance on WRITTEN A3 True, A4/A5 False (I-1)",
    "S3: A4/A5 --no-evidence rows; a4/a5-writes assert file equals printed record; A5 write placed after finish_unknown",
    "S4: fold L-4 into C1 (artifact-writers row evidence/runtime-provenance-*.json, writer runtime_probe.py); check whether it closes L-3",
    "S5: queue L-6 retire or re-scope no_runtime_record, owner t-305 N2 (P31 residual)",
    "S6: correct the F2 rationale; queue L-7 run_witness for a run refused by ProvenanceRefused",
    "S7: C3 rows in a smaller kept file, or a measured note that test_handoff.py stays under 60 s",
    "S8: state A6-A8 behaviour beyond the -99 suffix bound (S2 vs S3 conflict)",
    "S9: relabel or filter the measurer count at experiments/measurers/check_all_contracts.py:285-290",
    "S10: re-point line refs to main (driver_dispatch 1580/1589, null-outcomes.json 177/178/183, no test_scenario_dry_1.py on main)"
  ]
}
```
