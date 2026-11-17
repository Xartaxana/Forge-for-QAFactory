- `source_preflight.py`, `estimate_record.py`, `artifact_producer.py`, `gate_preflight.py`, `s5_precheck.py`, `execution_request.py`, `handoff_check.py`:
  the last refusals that had a joint row but no site are now built with `detector_verdict.refusal` and a literal id (`check_source_inventory`,
  `facts_problems`, `validate`, `question_branches`, `sides.provisional`, `sides.pending`, `profile.none`, `fingerprint.build`,
  `cli.values_rename`); their texts are unchanged. A role with no shell that meets the values-file rename refusal is told to say so in its digest
  instead of being told to delete the file. `profile.none` reaches the caller as its own row, not as the parent `profile` row. The `unsited`
  ceiling of `stage-joints.json` and its test cap go down from 17 to 11.
