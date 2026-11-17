# t-931 rules-debt S3 (W1, FR-13)

DoD: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/candidate_evidence.py ai-packages/qa-factory/scripts/profile_contract.py` plus `python -B ai-packages/qa-factory/scripts/tests/test_gate_registry.py`

## Output
```
scripts/candidate_evidence.py: scenario test_scenario_cart_1.py (story cart-1)
scripts/candidate_evidence.py: scenario test_scenario_local_1_0108.py (story local-1-0108)
scripts/candidate_evidence.py: scenario test_scenario_local_1_arm_b.py (story local-1-arm-b)
scripts/profile_contract.py: scenario test_scenario_cart_1.py (story cart-1)
scripts/profile_contract.py: scenario test_scenario_local_1_0108.py (story local-1-0108)
scripts/profile_contract.py: scenario test_scenario_local_1_arm_b.py (story local-1-arm-b)
scripts/profile_contract.py: keep test_config_migration.py (layer detector, covers it)
... (keep rows: test_config_projection, test_execution_request, test_gate_registry, test_manual_capture, test_manual_evidence, test_profile_reader, test_runtime_probe_onboarding)
---
PASS A26 writes nothing (FR-45, AST form): no write call in gate_registry.py
PASS FR-45 CONTROL: the same read sees the five planted writes and not the read
=== test_gate_registry: 438/438 ok ===
```
Extra narrow runs (not required): test_profile_reader 197/197 ok, test_config_projection 223/223 ok, test_manual_evidence 262/262 ok.
Value check: `profile_contract.LEVELS` = api, component, e2e-ui, integration, unit; `EXECUTION_BOUNDARIES` = the same + unknown (identical to the old sets). `python -B profile_contract.py --help` (script mode) still works.

## What changed
- candidate_evidence.py:3-10 `import contract`; `EXECUTION_BOUNDARIES = set(contract.PLAN_LEVELS) | {"unknown"}` with the comment (unknown = AR-23 not-stated; manual levels have no test file).
- profile_contract.py:16 `import contract`; :27 `LEVELS = frozenset(contract.PLAN_LEVELS)` (uses :188, :201, :211 are membership only).
- Cycle check (E1): contract.py top-level imports are case_forms (-> adapter_forms), grammar, runtime_paths (its `contract` import is lazy, :952); none imports profile_contract or candidate_evidence. No cycle; no local copy.

## AR-13 grep of `"e2e-ui"` over scripts/*.py (non-test hits)
candidate_evidence.py:7 and profile_contract.py:25 (fixed); contract.py:594 TRACE_LEVELS, :2175 PLAN_LEVELS (owner); controller.py:4435/4453 (reads contract.PLAN_LEVELS; single-word branch); critic_rollcall.py:1030, planning_contract.py:321, s5_plan.py:192, gate_preflight.py:153 (single-word uses); factory_dashboard.py:698/705 (label map keyed by level, display text; not a set copy); gate_brief.py:5214-5219 (self-test data). No other set copies seen (head_limit cut at 60 results, all within tests after the non-test hits).

## FR walk
- A: refusals unchanged. B: no text shown to a person changed. C FR-13: closed variety now one data owner, read by both. D: n/a. E: n/a. F: n/a. G: FR-29/30 hold (ASCII, test_gate_registry green).
- AR-1, AR-13 kept. E2 (absent -> unknown) and E4 (manual levels refused) unchanged: manual words are not in PLAN_LEVELS.

## Deviations
None. No new test (per block).

## Questions
none

## Needed beyond the manifest
contract.py, case_forms/adapter_forms/grammar/runtime_paths imports (cycle check), test_profile_reader/test_config_projection/test_manual_evidence (extra runs).
