# t-1445 -- RD1-37 S3 fix round (critic t-1443 F1-F4)

fixed F1: red_sandbox.py publish_product_refs -- manifest_put run in try; OSError/SubprocessError (TimeoutExpired included) append a `manifest_put.py: not run (...)` note and return; receipt stays, nothing counted; probe() gets it through the same road.
fixed F2: probe_by_code.py _judge_input and _demand_critic_dispatch take `door=JUDGE_DOOR`; _judge_product passes JUDGE_PRODUCT_DOOR; without --product text is byte for byte unchanged.
fixed F3: probe_by_code.py main stray-flag list gains ("--product", args.product or None).
fixed F4: test_red_sandbox_probe.py row 1: the self-compare element is removed from the tuple and replaced by an assert that the S2 note names --judge, --product and the record path.

Tests (rows, not new files): test_probe_marker_judgment.py -- F2 asserts inside test_judge_refusals_name_the_door (D4/D5 name the product door; live verdict/dispatch refusals hold no --product); new small tests test_publish_failure_keeps_the_receipt_and_notes (F1, TimeoutExpired and OSError rows) and test_product_flag_without_judge_is_a_stray_flag (F3).

Deviation: the DoD names `test_red_sandbox_probe.py::test_add`; that file is a harness script with no pytest function of that name (`test_add` is a fake-project function in strings), so the run was the whole file plus test_probe_marker_judgment.py.

Witness: `python -B -m pytest <wt>/ai-packages/qa-factory/scripts/tests/test_red_sandbox_probe.py <wt>/.../test_probe_marker_judgment.py -q -p no:cacheprovider`
-> `50 passed in 13.73s` (an earlier run of the same, before narrowing the F2 assert to D4/D5, had 1 failed: my own assert on D1; fixed, rerun green).
Noted analog: none beyond F1's probe() (covered). Changelog fragment: none (fix of an unmerged card).
