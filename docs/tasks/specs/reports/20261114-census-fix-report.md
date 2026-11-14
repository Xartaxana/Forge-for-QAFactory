# census-fix (t-799) report

## BEFORE (`python -B scripts/tests/test_judgment_census.py`, from ai-packages/qa-factory)

```
FAIL test_c1_every_unit_has_a_row_and_every_row_a_unit — 
  stale row `exploratory_findings.py::_check_probe`: no such check unit any more - remove the row, or move it to the function that took its place (a row is never dropped silently)
  stale row `exploratory_findings.py::_closed`: no such check unit any more - ...
  stale row `exploratory_findings.py::_judge_refs`: ...
  stale row `exploratory_findings.py::_link`: ...
  stale row `exploratory_findings.py::_nested_keys`: ...
  stale row `exploratory_findings.py::_origin`: ...
FAIL test_c3_the_ratchet_is_dense_and_only_shrinks — 
  `blocking_per_role.conductor` is 760, below its ceiling 764: lower the ceiling to 760 (the ratchet is dense and only shrinks)
=== judgment_census: 23/25 ok ===
```
(the five stale lines after the first differ only in the unit name; same text.)

## Rows removed (fixture judgment-census.json)
All `exploratory_findings.py`, class/owner as written: _check_probe shape/data, _closed shape/data, _judge_refs shape/data, _link xref/data, _nested_keys shape/data, _origin shape/data. Why: units no longer exist in the file. The path guard moved from `_judge_refs` into `contract.evidence_ref_issue` (commit 90bbf55e per the dispatch). No row added or moved: the test reported no unit without a row, so contract.py needed nothing.

## Ceilings
`blocking_per_role.conductor`: 764 -> 760 (shrinks only). No other change.

## AFTER
```
=== judgment_census: 25/25 ok ===
=== qa-factory selftest: 4/4 ok ===   (selftest.py --limits --lang)
```
