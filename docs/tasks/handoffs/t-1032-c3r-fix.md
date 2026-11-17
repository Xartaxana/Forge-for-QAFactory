# t-1032 — C3-R fix round (verdict t-1026, A1/A3/A4/A5)

## Findings -> changes

| finding | change | where |
|---|---|---|
| A1 (option a) | row `reporter_rehearsal_identity`: sites + `{_reporter_outcome, accept}` and `{_record_unreadable, produce}`; `status` back to `debt`, `debt_ref: B-283`; `decides` now says matched = `same_command` AND the durable key hits (a `same_command` whose key misses is rehearsed again). `verdict_map` kept (same_command -> matched; the text carries the AND) | `references/gate-registry.json` row `reporter_rehearsal_identity` |
| A1 pins | `EXPECTED_DEBT` +`reporter_rehearsal_identity: B-283`; removed from `EXPECTED_CONVERTED`; K-T1.2 text "7" -> "8 gate(s) left as debt:"; K-T1.14 title/split; `D13_TRIPLES` +`(gate_preflight.py, _reporter_outcome, reporter_rehearsal_identity)` and also `+(…, _record_unreadable, …)` (the produce site's comparison is attributed too, so its triple is a consequence, named here) | `scripts/tests/test_gate_registry.py` lines 55-68, 246, 322-336, 928-930, 987-992 |
| A3 | NOT applied: restored. With words `["blocked"]` only, `D13` went red: the scan attributes a comparison of `unknown` at `environment_preparation.py::_facts` (a registered site), so the triple `(environment_preparation.py, _facts, environment_preparation)` vanished and the count fell 140 -> 139. The condition "no registered site compares `unknown`" does not hold (it compares it as an input value, as the verdict says; the audit cannot tell input from outcome). Words stay `["blocked","unknown"]`. Question below | gate-registry.json row `environment_preparation` (unchanged) |
| A4 | `decides` of `delivery`: an unknown kind or an unreadable kinds file is `no`, refused with the kinds-file door (owner factory); `after_checks` hands the person their checks (P21), not a refusal. Text only | gate-registry.json row `delivery` |
| A5 | deleted the `check_eq("the block word the registry row carries is the code's", RS.NODE_ID_BLOCK, ...)` line | `scripts/tests/test_node_ids.py` (was :899) |

## Numbers old -> new (measured)

- D13_ITEM_COUNT 138 -> 140 (named change; `--sites` prints +2 lines: `gate_preflight.py:3843 _reporter_outcome earlier['state'] == 'same_command'` and `:3969 _record_unreadable earlier.get('state') != 'unreadable'`). The verdict's estimate of the rise was "the named number"; measured +2.
- Debt rows 7 -> 8, converted 20 -> 19, exempt 6. The verdict's "19 / 8 / 6" is converted 19 / debt 8 / exempt 6: measured the same, no difference.
- No raise on a ratchet other than D13_ITEM_COUNT.
- E-c invariant: after the fix the acceptance at `_reporter_outcome` is in `--sites` under a `debt` row (A26 lists the row under "8 gate(s) left as debt").

## FR walk (touched sections)

- A, B, C, D, E, F: not touched (registry data + test pins; no refusal, human text, contract, identity, delivery text or measurement changed in code).
- E (FR-19/FR-20 language): `decides` text of `delivery` only, no code path changed.
- FR-59 / AR-28: the unknown branch of `reporter_rehearsal_identity` stays `rerun`; no unknown passes. Visibility of the acceptance restored (E-c).
- G: FR-29/FR-30: JSON and test checked by the file's own control-byte/Cyrillic rows, green (441/441).
- Architecture: AR-20 (D13 raise named; debt/converted move together with the row), AR-29 (a registry row, no judgment moved).

## Siblings / classes seen

- `--sites` shows no other unregistered comparison of a converted row's word in the sites it lists. The class members the verdict named (red_sandbox.py:2292, execution_request.py:3187, environment_preparation execute_environment/read_object, stand_gaps._c4) were not touched (non-goals).
- Same-file note: A2 (`provenance.environment_preparation` dead consumer) remains queued with C3-k.

## Witness (verbatim)

```
$ python -B ai-packages/qa-factory/scripts/tests/test_gate_registry.py | tail -1
=== test_gate_registry: 441/441 ok ===
$ python -B .../test_node_ids.py | tail -1
=== test_node_ids: 258/258 ok ===
$ python -B .../test_selftest_slow_tests.py | tail -1   (keep row covering gate-registry.json)
=== test_selftest_slow_tests: 124/124 ok ===
$ python -B .../gate_registry.py --sites | grep _reporter_outcome
gate_preflight.py:3843  _reporter_outcome  earlier['state'] == 'same_command'  [reporter_rehearsal_identity]
$ python -B .../gate_registry.py --check | head -3
A26 gate registry: no violations
  blind spot: a gate that compares only non-anchor words, outside any registered site, is not seen (a literal-free pass is the per-gate behaviour test's)
  8 gate(s) left as debt:
$ python -B .../selftest.py --limits --lang | tail -1
=== qa-factory selftest: 4/4 ok ===
```

`scenario_walk.py --witness-for` printed: gate-registry.json -> keep test_gate_registry.py, keep test_selftest_slow_tests.py; for the two test files: "run the whole scenario layer" (test_scenario_cart_1/dry_1/local_1_0108/local_1_arm_b/walk/world). The six scenario files are not run to the end here: the run of them exceeded 180 s and went to the background (heavy files, judged by the batch canon). The A3 red run (words `["blocked"]`): `FAIL D13: and the number of comparisons it counts — expected 140, got 139` and the missing triple above.

## Questions

1) A3: the audit stays green with `["blocked"]`, but the D13 pin loses the `_facts` triple (a registered comparison of `unknown` disappears from attribution). Lead decides: keep `unknown` (done), or drop the word AND take the `_facts` triple out of D13_TRIPLES with count 139 (a fall; the comparison is then unseen).
