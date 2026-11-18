# t-1487 census C3 red

Re-measured on origin/main f6f1c916 (merged, "Already up to date"): C3 RED, `blocking_per_role.qa-code-critic` 94>93, `blocking_per_role.conductor` 749>748.

Cause (one commit): 64493180 "RD1-37 S3 ... (t-1435)" added the row `red_sandbox.py::_write_receipt_file` (roles conductor + qa-code-critic, raises on a receipt-name collision) and did not raise the ceilings (found by `git diff 1524b7d3 HEAD` of the fixture: the only new row with qa-code-critic). Ceilings 93/748 date from 1524b7d3 (t-1172).
Card line: docs/tasks/specs/20261118-rd1-37-38-probe-site-door-card.md:174 `D11 | fires, receipt name exists with other bytes | refused, nothing written` (intended refusal); :298 "census rows added if a unit appears"; :282 owns the fixture.

Fix: ratchet `qa-code-critic` 93->94 and `conductor` 748->749 (exactly the measured excess, named raise); the row note names the commit and card. Only judgment-census.json edited.

Witness:
`python -B tools/registry_preflight.py check census --root <worktree>` tail:
registry preflight: census ok (37.8 s)
rc=0
