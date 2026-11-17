# t-1083 (rules-debt/1/RD1-7): C3-b2 + main merged into the C3-d branch

Steps: `git merge origin/main` (clean, no conflict); `git merge origin/worktree-agent-a792e825fd0ee2fb6` (C3-b2, 18f585f5).

## Conflict hunks (all in `scripts/tests/test_gate_registry.py`; `references/gate-registry.json` auto-merged, both rows `converted`)
1. `EXPECTED_DEBT` header: both cards' comment lines kept, plus one merged line (6 -> 4 debt rows); dict loses both `s5_window` and `test_identity`.
2. `EXPECTED_CONVERTED` tail: both ids kept (`s5_window`, `test_identity`), each with its card's comment.
3. K-T1.14 debt text: one line naming "four rows left after ... C3-b1, C3-d and C3-b2".
4. K-T1.14 split comment: both cards' lines kept + `merged (t-1083): converted 21 -> 23, debt 6 -> 4`.
5. `D13_ITEM_COUNT`: both cards' comment blocks kept + a merged line; value 150.
Outside the hunks (re-measured, edited): K-T1.2 text "5" -> "4 gate(s) left as debt:"; split pin {22,5,6} -> {23,4,6}.
`D13_TRIPLES` auto-merged with both cards' triples, no edit needed.

## Measured pins (merged tree)
- `python -B ai-packages/qa-factory/scripts/gate_registry.py --check`: exit 0, "4 gate(s) left as debt:" (stand_identity, provenance_acceptance, baseline_identity, s5_stand_limits); neither test_identity nor s5_window in the debt block.
- `GR.analyse(PLUGIN_ROOT)`: 150 items / 53 triples (= 145 + 1 (C3-d) + 4 (C3-b2); 49 + 1 + 3). `--sites` shows both `window_record.py:1649 build [s5_window]` and the proof_level sites.
- converted 23 / debt 4 / exempt 6 from the pin test passing.

## Witness (each alone, from ai-packages/qa-factory)
```
=== test_gate_registry: 498/498 ok ===       exit 0
=== window record: 722/722 ok ===            exit 0
=== test_proof_level: 627/627 ok ===         exit 0
=== test_execution_request: 667/667 ok ===   exit 0
=== run freshness: 100/100 ok ===            exit 0
=== judgment_census: 25/25 ok ===            exit 0
=== qa-factory selftest: 4/4 ok ===          (selftest.py --limits --lang) exit 0
A26 gate registry: no violations             (gate_registry.py --check, exit 0)
```
Six-window control (C3-d's script was not in the tree; rebuilt in the session scratchpad: before = `git show 3d8c0ee1:.../acceptance.py`, sha256 eb0e4315d960..., after = merged tree; windows `work/windows/S5-qa-code-critic-{2..7}.json`; digest = sha256 of `json.dumps(sorted({name: gaps}.items()))`, the form found by matching the report's hash):
```
before 6 windows gaps: 20 sha256 1a7bcdb1754ef8e17e0887fade02fb975366558a9a0fb83c01fe4d8ac7cf45b9
after 6 windows gaps: 20 sha256 1a7bcdb1754ef8e17e0887fade02fb975366558a9a0fb83c01fe4d8ac7cf45b9
EQUAL
```
Nothing red. Needed beyond manifest: git history of acceptance.py (control's before copy).
