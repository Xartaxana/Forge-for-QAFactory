# C3 integrator report (t-1064)

Tree: `.claude/worktrees/agent-aa11322709a274e56`, branch `worktree-agent-aa11322709a274e56`, not pushed.

## Merges
1. `git merge origin/main` -> commit 2994f964, no conflict, no stash needed (OWNER_PRINCIPLES_INDEX.md stayed modified and unstaged).
2. `git merge origin/worktree-agent-aff41d56bd7610681` -> ONE conflict, `scripts/tests/test_gate_registry.py` (4 hunks), commit c10fb749. No other file conflicted (E1 not triggered). pre-commit: `gates: ok (7 checks)`, `gates: ok (4 checks)`; no "factory rules index is stale".
Both commit messages carry the `architecture:` / `judgment:` / `axes:` lines.

Note: this report file is created after the merge commit and is left uncommitted (owns: new file).

## Conflict hunks and derivation
- Hunk 1 `EXPECTED_DEBT`: HEAD (rr) = 7 rows with `live_check_demand` and without `reporter_rehearsal_identity`; theirs (b1) = 7 rows with `reporter_rehearsal_identity` and without `live_check_demand`. Merged = both removed -> 6 rows (stand_identity, provenance_acceptance, test_identity, s5_window, baseline_identity, s5_stand_limits).
- Hunk 2 `EXPECTED_CONVERTED`: kept both appended rows: `reporter_rehearsal_identity` (rr) and `live_check_demand` (b1) -> 21.
- Hunk 3 (K-T1.14 comment): both comments kept plus a merged line (19 -> 21, debt 8 -> 6).
- Hunk 4 `D13_ITEM_COUNT`: rr said 145, b1 said 140 (b1 base had no gate_template sites). Merged = measured 145.
- Pins changed outside hunks (auto-merged to one side's stale value, re-derived): K-T1.2 "7 gate(s) left as debt:" -> "6 gate(s) left as debt:"; K-T1.14 split `{"converted": 20, "debt": 7, "exempt": 6}` -> `{"converted": 21, "debt": 6, "exempt": 6}` (label text updated too). The "6 gate(s) exempt:" pin unchanged (measured 6).
- K-T1.13 rows (import-alive, chain, fake-root NEG) untouched.

Measure (one-off script, scratchpad `measure.py`, using `gate_registry.analyse` and the registry file, on the merged tree):
```
items 145 triples 49
Counter({'converted': 21, 'debt': 6, 'exempt': 6})
debt ['stand_identity', 'provenance_acceptance', 'test_identity', 's5_window', 'baseline_identity', 's5_stand_limits']
```
Arithmetic (debt 6, converted 21) equals the measure; E2 not triggered. D13 triples 49 equals rr's after (set test passes unchanged). E3: no pin without a reader.

## DoD witnesses (merged tree)
- `python -B .../tests/test_gate_registry.py` -> `=== test_gate_registry: 493/493 ok ===`
- `gate_registry.py --check` -> first line `A26 gate registry: no violations`, `6 gate(s) left as debt:`, `6 gate(s) exempt:`; exit 0.
- `audit_factory.py` -> `A1 hook liveness: no violations`
- `stage_joints.py --check` -> `stage joints: clean` (rc 0; summary: `gaps 4 (producer 2, told 1, demands 1), joints held 4 of 268`)
- `contract_slices.py --check` -> `slices: 44 declared, all present and fresh; 19 key pages; 12 charters carry a generated digest line`
- `tests/dry_exits.py --check` -> `dry_exits --check: 0 discrepancies` (preceded by two NOTE ratchet lines, live_only raised 31 and unwalked raised 227, each with raised_by named; informational)
- `test_proof_level.py` -> `=== test_proof_level: 607/607 ok ===`
- `test_controller_rework_repair_binding.py` -> `=== test_controller_rework_repair_binding: 235/235 ok ===` (green locally; the CI red was not reproduced)
- `selftest.py --limits --lang` -> `=== qa-factory selftest: 4/4 ok ===` (rc 0)
- Negative control: byte copy of test_gate_registry.py taken (sha256 aa331073bd593d3d41e068d9657275284a57910518d465cf05d80cc08cf2fb7e); `D13_ITEM_COUNT = 145` -> 146:
  `FAIL D13: and the number of comparisons it counts — expected 146, got 145` / `=== test_gate_registry: 492/493 ok ===`.
  Restored from the copy; sha256 of file and copy both `aa331073bd593d3d41e068d9657275284a57910518d465cf05d80cc08cf2fb7e`.

## Analogs noticed
- Count pins in test_gate_registry.py are stated in several places (K-T1.2 text, K-T1.14 label and dict, comment blocks); a pin edited by only one side auto-merges silently stale (the K-T1.2 and K-T1.14 lines did exactly that). A single derived source (read from the registry) would remove the class; not done (non-goal).

## Beyond the manifest
none (read test_gate_registry.py, gate-registry.json via the reader only).
