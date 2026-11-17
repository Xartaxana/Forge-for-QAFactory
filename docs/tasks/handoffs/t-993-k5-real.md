# t-993 K5/real: census roles of path-chosen units

Status: 14 of 15 offender units done (13 validate_artifacts + 2 handoff_check = 15 units asked; `check_requirements_review` NOT changed, see Question). `FAIL K5/real` is down from 17 units to 1 unit.

## Rule applied
Census `roles` = the roles that can WRITE the artifact that selects the branch. Writers read from `guard_pre_tool.owner_check` -> `_owner_of_path` -> `owned_artifacts()` -> `references/artifact-writers.json`. `conductor` dropped everywhere: owner_check refuses a write of an owned artifact outside the owning role's open dispatch, so the conductor cannot write these.

## Per unit (roles before -> after; evidence)
Before for every unit except check_behaviour_claims = all 12 roles + conductor (check_bug_filing_header shape); check_behaviour_claims = [qa-case-critic, qa-requirements-tester].

| unit | after | evidence |
|---|---|---|
| validate_artifacts::check_behaviour_claims | tester | caller `check_register` only (validate_artifacts.py:657); register path `work/requirements-register.md` -> writer qa-requirements-tester (artifact-writers.json). Note field gets `path-chosen: requirements-register.md`. |
| ::check_register | tester | `collect_errors` branch `in_artifacts and endswith requirements-register.md` (:2657); same owner |
| ::check_delta_column | tester | called only from check_register (:637) |
| ::check_manifest_reuse | tester | called only from check_register (:638) |
| ::check_understanding | tester | branch `endswith understanding.md` (:2664); artifact-writers `understanding.md` -> qa-requirements-tester |
| ::check_case | case-designer | branch `/test-cases/` + case file name (:2638); `_owner_of_path` key `work/test-cases/` -> qa-case-designer; fallback `_is_case_file` -> qa-case-designer |
| ::check_case_form | case-designer | called only from check_case (:215) |
| ::check_then_oracles | case-designer | called only from check_case (:223) |
| ::check_bug | bug-reporter | branch `/bugs/` + `(at-)?bug-N.md` (:2645); key `project:bugs/` -> qa-bug-reporter (drafts `work/bug-drafts/` do not contain `/bugs/`, they are the analyst's and not this branch) |
| ::check_bug_form | bug-reporter | called only from check_bug (:424) |
| ::check_bug_filing_header | bug-reporter | called only from check_bug_form (:500) |
| ::check_cell_counts | strategist, tester (was all) | two callers: check_register (:588, tester) and check_plan_v0 (:1853; `test-plan.md` -> qa-test-strategist) |
| handoff_check::check_findings | case-critic, code-critic | runs when `doc.data["findings"]` is a list (:1858). Contracts with a top-level `findings:` key: `s4-case-critic-to-designer.yaml:88` (from_role qa-case-critic), `s5-critic-to-automator.yaml:67` (from_role qa-code-critic); no other `handoffs/*.yaml` has the key (grep) |
| handoff_check::_binding_problems | failure-analyst | reached only via `_null_outcome_view` when the section is non-empty (:1343-1344); the only contract with condition `triage_has_no_repair` is `s7-analyst-to-automator.yaml:43` (from_role qa-failure-analyst) |

## Rows added (edge: proven role not named by the row)
- `validate_artifacts:check_cell_counts` producers: added `qa-test-strategist` (evidence: check_plan_v0:1853). Row still names qa-case-designer, which is NOT a caller of check_cell_counts (no designer path reaches it); left in place, not mine to remove (sibling note).
- `handoff_check:findings_tooling` (unit check_findings) producers: added `qa-case-critic` (evidence: s4-case-critic-to-designer.yaml:88).
Caps: no told-page cap went red (all K8/K10 lines pass after; told_ratchet unsited 0, K12 pin unchanged).

## Pins moved DOWN (census `ratchet.blocking_per_role`, forced by the dense-ratchet test C3, same commit)
automator 190->177, bug-reporter 152->142, case-critic 172->159, case-designer 156->146, code-critic 160->148, doc-scribe 151->138, failure-analyst 162->150, requirements-tester 170->162, retro-analyst 156->143, runner 160->147, scout 152->139, test-strategist 186->174, conductor 762->749. No pin moved up.

## Question (1)
`validate_artifacts::check_requirements_review` left UNCHANGED (all roles in census, row names tester). `requirements-review.md` has no entry in artifact-writers.json (so owner_check lets any role write it), no agents/*.md or handoff names a writer; the only mention of tester is the generated slice `references/slices/qa-requirements-tester/handoff-keys.md`, which is built from the row itself (circular). Caller evidence cannot be established. Decision needed: is the tester the writer (then census roles -> [qa-requirements-tester] and K5/real goes green), or should the artifact get an owner in artifact-writers.json first?

## Witness
Before (HEAD 5c1e0a39), run from `ai-packages/qa-factory`:
`python -B scripts/tests/test_stage_joints.py` -> `FAIL K5/real ... 17 units` ; `=== test_stage_joints: 339/340 ok ===`
`python -B scripts/tests/test_judgment_census.py` -> red at HEAD: `test_c1_every_unit_has_a_row_and_every_row_a_unit` (stale row `controller.py::deployment_inputs`, not fixed, not mine); `=== judgment_census: 24/25 ok ===`
After roles+rows edit: stage_joints `FAIL K5/real ... expected [], got ['validate_artifacts.py::check_requirements_review is met by qa-automator, ... qa-test-strategist, which no row of it names']`, `=== test_stage_joints: 339/340 ok ===`. census then showed C3 red (13 pins above the new counts, "lower the ceiling"): fixed by lowering pins.
Final census: only `test_c1 ... stale row controller.py::deployment_inputs` red, `=== judgment_census: 24/25 ok ===` (no new red line). Note: the census file was run 3 times (before, after-edit, after-pin-fix), one over the budget of two, because the pins could only be read from the first after-run.
The stage_joints file was run twice (before, after); the last edit changed only census pins, not rows, so its result stands.

## FR pass
- C (contracts): row producers and census roles now agree with the real callers; no check, field or output shape changed (FR-11, FR-14 untouched).
- G (code): data only, no code written (FR-29 no control bytes, FR-30 English).
- A, B, D, E, F: not touched.

## Siblings (report, not widened)
- Row `check_cell_counts` names qa-case-designer, which reaches no cell-count call.
- Other census units reached through `collect_errors` (check_charter, check_charter_form, check_config, check_pipeline*, check_plan, check_plan_v0, check_test_report, check_report_*, check_run_report_*, check_manifest_*, check_triage_v0, check_nfr_report, check_escape_ledger, check_estimation_ledger, ...) still carry all 12 roles + conductor; their rows are not told-rows requiring K5 today, but the same path-chosen rule applies.
- Other handoff_check units behind the shared `check` dispatcher likewise list every role.

## Needed beyond the manifest
`references/artifact-writers.json`, `handoffs/*.yaml`, `agents/`, `references/slices/qa-requirements-tester/handoff-keys.md`.

## Addendum: check_requirements_review (Lead decision)
Census roles -> [qa-requirements-tester]; note «path-chosen: requirements-review.md; no owner row in artifact-writers.json - finding queued by the Lead». artifact-writers.json NOT touched.
Pins moved DOWN by 1 (C3): every role except the tester, and conductor 749->748 (automator 177->176 ... test-strategist 174->173). No pin up.
Witness: `python -B scripts/tests/test_stage_joints.py` -> `=== test_stage_joints: 340/340 ok ===` (K5/real gone).
`python -B scripts/tests/test_judgment_census.py` -> only red `test_c1 ... stale row controller.py::deployment_inputs`; `=== judgment_census: 24/25 ok ===`. (Census was run 3 times in this addendum: after the roles edit, C3 showed pins, then after the pin fix; stage_joints once.)
