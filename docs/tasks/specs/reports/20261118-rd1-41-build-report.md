# RD1-41 (RD1-37c) build report, t-1495

DONE: `proof_level.probe_record_state` reads `work/probes/product/<stem>.json` when the live record FILE is absent; the same state
machine, so `probe_could_not_run`, `probe_owes_judgment`, `probe_plain_call_owed` follow unchanged. `cannot_judge_facts` now reads the
record the state named (`state["record"]`, live or product) instead of the live path. `window_record.py` NOT changed: its callers go
through these readers; `unproved_keys_text` reads `state["record"]` and a product record has no `checks`, so it gives "".
Files: scripts/proof_level.py, scripts/tests/test_probe_readers.py.

Binding (edge 5, not a stop): the product record carries `instance_id` and `test_file_sha256` (red_sandbox.py::_write_product_records).
Bound = `instance_id == identity` AND `test_file_sha256 == input_hash` (both non-empty). Anything else -> not_run naming the path.
Product `probe_defect` / any unknown verdict -> not_run naming the path. `record` key = path of the record read (product path).

Tests (one parameterised test, 10 rows, + 1 invariant test); each row's result on main BEFORE (derived by reading the old code, which
reads the live path only; not executed on the old code: estimate, not verified): every product row gave state not_run, owes "", facts None:
owed -> was not_run (now incomplete/unjudged); cannot_judge -> was not_run (now facts with the person's door); judged -> was not_run (now judged);
tooling incomplete -> was not_run (now could_not_run true); other bytes / other instance / unknown verdict / no verdict / broken JSON /
not an object -> not_run before and after (new: why names the product path). Live-present test: same before and after.

Witness: `python -B -m pytest ai-packages/qa-factory/scripts/tests/test_probe_readers.py -q -p no:cacheprovider`
-> `27 passed in 3.96s`

Test lines added ~38, product lines ~16 plus text: over the 1:1 budget by the table rows; flagged for the Lead (tests-over is his word).

Needed from integration: changelog fragment `ai-packages/qa-factory/changelog.d/rules-debt-1-rd1-41-product-record-readers.md` (not in owns):
"The probe record readers now read the product probe's record (`work/probes/product/`) when no live record exists: a product record that owes the code critic's judgment reads as unjudged, one that could not be judged opens the person's `probe not proved` door; a record of other bytes or a broken one reads as not run."

Analogs noticed: `proof_level.tooling_gap_key` and `window_record.py:787,880` read the live path only (not changed; non-goal/out of the card).
Needed beyond manifest: none (read red_sandbox.py::_write_product_records, given).

## Fix round (t-1495 resumed; critic t-1499)

- F1 DONE: `window_record.judge_door` (new) picks `JUDGE_PRODUCT_DOOR` when `probe_record_state["record"]` is the product path, else `JUDGE_DOOR`;
  used in `build`'s unjudged note and `probe_word_door` (grouped by door). Docstrings at the three places updated. Row failing on 0c55a95e:
  `test_product_record_is_read_when_live_is_absent[owed]` / `[cannot_judge]`... (`WR.judge_door` absent; `probe_word_door` lacked `--product`),
  and `test_live_record_present_is_read_as_today` (live keeps the plain door).
- F2 DONE: rows "not an object", "no verdict" and the both-absent assertion cut (named as `tests not written ... over budget` in the test file);
  the remainder still exceeds the budget: Lead's `--tests-over`.
- F3 DONE: docstring of `probe_record_state` names the product fallback; a product `incomplete` with no notes says "the product probe record <path> says its
  proof could not be judged" (row `[tooling incomplete]` asserts "did not run" absent; fails on 0c55a95e).
- F4, F5: remarks, no change (changelog fragment text above; `probe_debt.py:284-288` live-only, for the Lead).

Witness: `python -B -m pytest .../test_probe_readers.py .../test_probe_marker_judgment.py -q -p no:cacheprovider` -> `75 passed in 20.37s`
