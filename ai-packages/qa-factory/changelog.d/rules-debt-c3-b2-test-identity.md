- the reuse of an old probe record, product record, receipt or run result reads its test identity through the gate registry row `test_identity`
  (`proof_level.py`: `already_probed`, `_product_receipt_repeat`, `_run_freshness`, `_evaluate`; `execution_request.py`: `_match`; consumers
  `probe_repeat`, `run_reuse`, `run_fresh`, `receipt_holds`): the same reuse decisions as before when the registry reads; an unreadable registry
  refuses every reuse (the probe or the run happens again) and the why names the registry, never a change of the test (B-217)
