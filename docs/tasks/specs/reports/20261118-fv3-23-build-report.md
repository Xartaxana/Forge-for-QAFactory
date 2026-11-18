# FV3-23 build report (t-1512)

Item: DONE (one stub row). File: `ai-packages/qa-factory/scripts/tests/fixtures/stories/dry-1/story.json` (new key `qa-failure-analyst@S7`, inserted before `qa-case-designer@S4`; every other row byte-identical). `dry_stub.py` unchanged. No test added (data row; the dry scenario file judges it in CI).

## Cause (verified)
`stub_control(..., "qa-failure-analyst", "S7")` returned `{}` -> `fill_role` used the default digest (no TC lines, no path) and the form was left unfilled (the form `s7-analyst-to-automator` has token `<the author's dispatch>` that no rule fills; the filler's default triage is a junk `APP_BUG` row for `test_removed_node[chromium]`). A missing row, so no STOP.

## What the row does
- verdict `ok`; digest: header, `TC-1 · passed`, `TC-2 · NOT_EXECUTED`, last line the form path. Empty-scope shape: path named, no repair.
- form overrides (`s7-analyst-to-automator`): `inputs_read[0].path` = runner form `S6-qa-runner-1`, `[1].failures` 0, `[2].path` = `<newest:evidence/runtime-provenance-*.json>` (the `--fix` step then derives all three versions by sha256), `header.window` none, `scope/repairs/not_for_repair/unresolved` empty, `blocked` absent, three claims true, `stage_acceptance` kept as `accept` (failure_class, quote, witness_paths[0] absent).
- `work/triage.json` override `{"triage": []}` (replaces the filler's junk row).

## Witness (narrow call, scratchpad probes; positive run)
`python -B .../scratchpad/probe3.py <new story.json>` printed (tail):
```
ROW KEYS ['overrides', 'result_text', 'verdict']
--- DIGEST
qa-failure-analyst S7 DRY-1 · ok
TC-1 · passed · the S6 run is green; nothing to triage, nothing to repair
TC-2 · NOT_EXECUTED · left unchecked by the person's word at S6; no run to triage
work/handoffs/S7-qa-failure-analyst-1.yaml
--- RD.check []
```
Written form (comments stripped): header `window: none`, `verdict: ok`, `stage_acceptance: {verdict: accept, witness_paths:}`, `scope: []`, `repairs: []`, `not_for_repair: []`, `unresolved: []`, claims true, inputs_read rows 0..2 with filled paths.
The product's own checker on that form in a temp task (run-report with 1 passed, empty triage, a runner form and provenance file present):
```
exit 0
filled by code: inputs_read[0].version = 54b1b553676036c9 (from sha256 of work/handoffs/S6-qa-runner-1.yaml)
filled by code: inputs_read[1].version = c41b0ea169411500 (from sha256 of work/run-report.json)
filled by code: inputs_read[2].version = 44136fa355b3678a (from sha256 of evidence/runtime-provenance-1.json)
handoff_check: s7-analyst-to-automator is complete (54 fields checked)
```
Triage fill: `work/triage.json '{\n  "triage": []\n}\n'`.
Negative control (old story.json from HEAD):
```
ROW KEYS []
wrote=0: no row for qa-failure-analyst@S7
```
Lint: `python -B tools/registry_preflight.py check lint --paths ai-packages/qa-factory/scripts/tests/dry_stub.py` -> `registry preflight: lint ok (0.8 s)`.
Not run locally: the dry story scenario file, canon judges.

## Unverified / risks for the canon run
- The real S7 world was not run (dry stories CI only): I assumed the run report holds no failure and TC-2 has no manual-check row (refused `left_unchecked`, so `triage_targets` finds no target), hence empty triage / empty scope. If the report carries an `unprepared` row for TC-2, the null-outcome check will demand a TC-2 triage row; the fix is then a triage override row, not a product change.
- `work/bug-drafts/` stays a `live_only` row of the stub journal (ctx has no bug ids), as before this change; not part of the measured stop.
- `S6-qa-runner-1` as the reviewed runner dispatch is taken from the S6 digest text in the same story.
- DoD edge: empty scope at S7 -> digest names path, zero repair lines: held (TC lines are per scope item, as the exit gate demands).

## Needed beyond the manifest
`handoffs/s7-analyst-to-automator.yaml`, `scripts/handoff_check.py`, `scripts/acceptance.py`, `scripts/contract.py::triage_targets`, `scripts/tests/form_filler.py`, `scripts/role_digest.py`.

## Same-class notes
FV3-25 / FV3-36 write the same story file (not dispatched). `known_red.json` untouched (non-goal). No CHANGELOG fragment: test fixture, no product change.
