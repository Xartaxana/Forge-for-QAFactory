# t-1410 RD1-37 S2 producer: report

DONE: reporters.py `FAILURE_TEXT_MAX`, `cut_failure_text` (moved body); probe_by_code.py `cut_text`/`FAILURE_TEXT_MAX` are aliases.
DONE: red_sandbox.py `_receipt_body` (extracted; `write_sensitivity_receipts` uses it, same keys), `judgment_owed`, `_failure_problem`, `_owed_extras`; `_write_product_records` adds `task`/`case` always, `cause`/`judgment_facts`/`pending_receipt`(+`_why`) only on J1; `probe()` keeps `rows_of`, passes it plus results/baseline/receipt; incomplete branch note names `--judge` and `--product` and the record path, no `--judge "` text; the generic tooling sentence stays only when a site_unread proof is not owed.
DONE: tests (test_red_sandbox_reports.py): row 1 in junit_runner_that_is_not_pytest_is_incomplete, row 2 (J1-J4) in request_status_of_proofs. Both rows written; +20 test lines vs ~158 code lines.
Changelog fragment: ai-packages/qa-factory/changelog.d/rules-debt-1-rd1-37-product-judgment-owed.md. No new config key.

Deviation: `judgment_owed(proof, result, base_row, row=None)` has a 4th argument `row` (the bound report row) because the card's 3-argument form cannot see the failure text (result carries the message only).
Noticed analogs: `red_sandbox._failure_problem` duplicates `probe_by_code.failure_problem` (red_sandbox may not import it; a move to reporters would unify).
Needed from integration: none. Beyond manifest: none.

Witness:
- `python -m pytest .../test_probe_marker_judgment.py -q` -> `47 passed in 13.70s`
- narrow call (request_status_of_proofs, junit_runner..., a_baseline..., site_unread_is_incomplete) -> `=== rd1-37a: 87/87 ok ===`
- `selftest.py --lang` -> `=== qa-factory selftest: 2/2 ok ===`
- `tools/lint_ratchet.py --check` -> `lint ratchet: 76 findings, 76 in the baseline, 0 new, 0 stale`

not run locally: test_red_sandbox_reports.py, test_red_sandbox_probe.py, test_gate_registry.py, canon judges
