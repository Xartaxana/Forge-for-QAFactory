# t-1030 wave B integrator, part 2 — hand-back as received inline (copied by the Lead, 17.11.2026)

Branch `worktree-agent-ad0767bec786dddde`, commit `a65afe58`. Merges: T4b clean at `d713ec07`, origin/main clean at `378a1ddd`.

## Witness lines (the integrator's runs, once each after the edits)
- `stage_joints.py --check`: `told counters: hand_cards 12, legacy_legs 0, unsited 17 / stage joints: clean`
- `contract_slices.py --check`: `slices: 44 declared, all present and fresh; 19 key pages; 12 charters carry a generated digest line`
- `test_stage_joints.py`: `=== test_stage_joints: 340/340 ok ===` (K5/real, K4/baseline-covers-join, K1-A24/at-baseline PASS)
- `test_judgment_census.py`: `=== judgment_census: 25/25 ok ===`, `census breaches: none`,
  `census: 280 files scanned, 1264 units; shape=932 xref=214 word-list=0 meaning-proxy=7 meaning=24 safety=87; breach=0; blocks_overrides=10`

## Edits
Two fixtures under `scripts/tests/fixtures/`: `judgment-census.json`, `told-ratchet.json`. No row of `stage-joints.json` touched.

`blocking_per_role` before -> after: qa-automator 167 -> 138, qa-bug-reporter 132 -> 98, qa-case-critic 148 -> 114,
qa-case-designer 136 -> 102, qa-code-critic 138 -> 104, qa-doc-scribe 128 -> 107, qa-failure-analyst 140 -> 108,
qa-requirements-tester 153 -> 119, qa-retro-analyst 133 -> 99, qa-runner 137 -> 109, qa-scout 129 -> 97,
qa-test-strategist 164 -> 132, conductor 748 unchanged.

`told-ratchet.json` (NOT named by the dispatch) rewritten to the measure, no entry rose: rowless 25 -> 3, untold 253 -> 175,
units 220 -> 211. Without it K4/baseline-covers-join and K1-A24/at-baseline were red. Nine units dropped: the six stage_guard
ones plus `inject_context.py::collect_blocks`, `map_problems`, `refuse_native_packet` (already off the join: stale baselines).

## Per-unit table (before = all 12 roles + conductor; after keeps conductor and the writer role of the artifact whose write fires the hook)
- check_context_manifest_v0 -> qa-scout
- check_manifest_v0, check_manifest_invariants, check_self_fixes, check_marker_in_file -> qa-automator
- check_remedy_rows -> qa-automator, qa-runner
- check_run_report_coverage, _empty, _head, _v0, check_result_rows -> qa-runner
- check_triage_v0 -> qa-failure-analyst
- check_plan, check_plan_v0 -> qa-test-strategist
- check_test_report, check_ptr_readiness, check_legacy_report_sections, check_report_{blocks, coverage, forbidden, gate_b,
  human_text, ledger_and_readiness, left_with_you, sections, test_marks, traceability} -> qa-doc-scribe
- check_phase_json -> qa-failure-analyst, qa-scout (only the roles that have a row)

Step 4: dispatch_errors, rule_order, rule_gate_a, rule_awaiting_code, rule_tracker_route, rule_gate_ordered ->
`roles: ["conductor"]` with the T4b note; callers all dispatch-time (stage_guard.check, controller, gate_preflight, waiver;
rule_gate_ordered only at stage_guard.py:1887).

## A role meets it, no row (rows not edited)
- check_phase_json: qa-automator (automation-manifest.json required keys), qa-runner (run-report.json required keys).

## Deviations
- check_phase_json keeps only the roles with a row (K5 is red otherwise); the no-row roles are listed above.
- The census narrowing forced the told-ratchet.json rewrite.
