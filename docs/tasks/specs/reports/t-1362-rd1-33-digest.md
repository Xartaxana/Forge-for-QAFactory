# digest v1 t-1362 (scout, sonnet) -- RD1-33: readers of `probe_verdict` / `test_identity` words outside registered sites

Frozen by the Lead from the scout's hand-back (18.11.2026). Package code only (scripts/*.py, tests excluded). Line numbers at main 65bc13ce.
Control: `instance_code` found at the registered site already_probed, proof_level.py:1582.

## probe_verdict -- unregistered readers (P = ai-packages/qa-factory/scripts)
| id | where | read |
|---|---|---|
| f-pv01/02 | proof_level.py:1116, :1170 | PROBE_JUDGED_VERDICTS tuple; probe_record_state `verdict in` it (card F5) |
| f-pv03 | proof_level.py:1092 tooling_gap_key | named by card F5; no literal hit, not read (unconfirmed) |
| f-pv04 | red_sandbox.py:1525-1534 request_status | status == probe_defect / incomplete / survived (card F5) |
| f-pv05 | red_sandbox.py:741-743 verify | p["verdict"] == probe_defect; status fold |
| f-pv06 | red_sandbox.py:845 write_sensitivity_receipts | status == probe_defect |
| f-pv07 | red_sandbox.py:1807-1841 probe | status chain probe_defect/survived/not_executed/incomplete |
| f-pv08 | red_sandbox.py:2321 main | status in (accepted, survived, already_probed) exit |
| f-pv09 | red_sandbox.py:718 verify | semantic_verdict == intended_failure |
| f-pv10 | driver_stage_s6.py:678-680 s6_reprove | verdict == intended_failure / incomplete |
| f-pv11..14 | probe_debt.py:300-329 _scan, :358 _owed_words, :686-697 _classify, :745 | intended_failure / not_executed |
| f-pv15/16 | window_record.py:719 _probe_scope_notes, :753 unproved_keys_text | intended_failure |
| f-pv17..42 | probe_by_code.py: _judge_joint_rows 3338, _receipt_core 4062, _SURVIVOR_ORDER 4245, _worst_of_rows 4268, _proved_standing 4706-4718, _finish_record 4743, _judge_alt_row 5905-5918, keep_standing_record 5967-5973, _attempt_why 5999, _check_proved 6062, _CARRIED_VERDICTS 6065, _walk_attempt.settle 6325-6332, _walk_plan 6482-6485, _AGG_KNOWN 6596, _aggregate_rows 6705-6744, _aggregate_verdict 6770-6779, _judgment_fold 6794-6796, _aggregate_record 6847-6951, _repeat_same_entries 7345-7362, publish_binding 7609, _unsettled_checks 7683, _judge_walk 7724, _judged_record 7754, _judge_cli 7943, _finish_alternative 8324, main 8402 | verdict-word comparisons and tuples |

## test_identity -- unregistered readers
| id | where | read |
|---|---|---|
| f-id01 | proof_level.py:248-250 held_words | how == instance_code / file_code |
| f-id02/03 | proof_level.py:1745 _HOLDS_RANK, :1803 reached | rank keyed by identity words |
| f-id04 | execution_request.py:2077 same_instance_bytes | compare_identity(...)[0] == same |
| f-id05 | run_history.py:708 _make_pair | verdict == same after _compare_shas |
| f-id06 | window_record.py:1963 _run_freshness_unknown | state == unknown |
| f-id07 | ledger.py:1273 (function unresolved) | freshness[0] == unknown |

## Not done (scout's own list)
`unknown` scanned by comparison shape, first 60 hits only; variable-held word sets not searched; function names by nearest def;
tooling_gap_key not read; homonyms (`not_executed`, `incomplete` of other vocabularies) excluded as one family.
