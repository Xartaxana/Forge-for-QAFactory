# TBW1-17 (TBW-T1rc-site) report, task t-1246

## Plan items
- DONE `source_preflight.py::check_source_inventory`: literal `source_preflight:check_source_inventory` on the 4 errors the row names (missing file when required, no required source, pending, materials without receipts).
- DONE `estimate_record.py::facts_problems`: literal `estimate_record:facts_problems` on all 3 problems.
- DONE `artifact_producer.py::validate`: literal `artifact_producer:validate` on the triage `instance_id`/`attempt_id` error (the row's one requirement).
- DONE `gate_preflight.py::check_question_branches`: message is `refusal("gate_preflight:question_branches", ...)` (text unchanged; `add` str()s it, so no `told` rides on the finding).
- DONE `s5_precheck.py::_sides_provisional` (8 adds) and `_sides_pending` (2 adds): `DV.refusal("s5_precheck:sides.provisional"|"sides.pending", ...)` as `_sides_settled`. Sibling sides adds (`sides.declared`, `sides.settled`, `sides.placeholders`) were already literal: none left bare.
- DONE `execution_request.py::_profile_for` -> `execution_request:profile.none`; `build_mine_request` fingerprint failure -> `execution_request:fingerprint.build`. The caller's `except MineRefusal` re-wrapped every helper refusal as `execution_request:profile`; it now re-raises a refusal that already carries a check, so `profile.none` is the row told, not its parent.
- DONE `handoff_check.py` rename failure: id `handoff_check:cli.values_rename` (was `handoff_check:cli`); the Problem's fix is `delete <file>` for a role with Bash (`host_adapter.role_has_bash`), else "say in your digest that <file> could not be renamed; the orchestrator removes it" (F7). Unreadable role/host = no shell.
- DONE `test_contract_slices.py::test_t1rs`: `NOT_YET_SITED` is empty; its third-id row stays (a plain refusal row: `zz_third` still refused, the two sited ids now pass `sited`).
- DONE `stage-joints.json` `told_ratchet.unsited` 17 -> 11 and `test_stage_joints.py` `UNSITED_CAP` 17 -> 11 (expected number).
- DONE `test_detector_verdict.py`: the T6 scanner row reads 22 ids (adds `cli.values_rename`).
- NOT DONE (not needed): `told-ratchet.json` unchanged; K4 stays green without moving unit rows.

## Unsited
before 17, after 11. The 11 left are `first_look:put.*` (not this node). Measured by `stage_joints.py --check`: `told counters: hand_cards 12, legacy_legs 0, unsited 17` before, `... unsited 11` / `stage joints: clean` after.

## Decided differently / for the Lead
- Emptying `NOT_YET_SITED` alone turned `T1rs/marked-by-proof` and `entry-uniform` red: the two ids became "proved" while the data does not mark them call-told. I moved the two ids into the typed `unproved_site` set (site exists, no provoking row ran green; same behaviour as before). Marking them call-told would change role pages: a decision for the Lead.
- No test row provokes the no-Bash rename door or `profile.none` through the caller; `test_handoff_values_main_block` K13 covers the rename failure and is green.
- Told is carried to no printer: `estimate_record` (`compound` returns str), `gate_preflight.add` (str), `artifact_producer`, `source_preflight`. The sites make the rows count; printing `told_fields` there is a sibling item, not done.

## Pass over factory-rules
A, B, E, F: texts unchanged except one fix sentence (FR-2: a no-shell role is not told to delete a file). C: no contract field changed. D: ids are literals (FR-16/17). G: English only; FR-31 n/a. Axis 38 (dry census): no new joint ids, rows unchanged.

## Witness
Command per site set: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <the 7 owned code files>` printed 83 non-slow, non-quarantined files; plus the three owned tests. Run once each from the package dir (`python -B scripts/tests/<file>`); verbatim last lines:
```
=== test_detector_verdict: 831/831 ok ===
=== contract slices (markup, generation, freshness, shipped map): 532/532 ok ===
=== test_stage_joints: 340/340 ok ===
=== test_execution_request: 667/667 ok ===
=== test_s5_precheck: 1306/1306 ok ===
=== s5 precheck sides: 201/201 ok ===
=== test_handoff: 757/757 ok ===
=== test_handoff_values_refusal: 6509/6509 ok ===
=== test_handoff_values_main_block: 47/47 ok ===
=== test_null_outcomes: 327/327 ok ===
=== test_field_producers: 885/885 ok ===
=== brief_pack / ahead_cards / branch_accounting / bug_records / check_witness / question_register / window_record: all N/N ok (first full pass, same code)
python -B ai-packages/qa-factory/scripts/stage_joints.py --check -> told counters: hand_cards 12, legacy_legs 0, unsited 11 / stage joints: clean
```
The full 83-file set ran once before the `test_contract_slices.py` fix (all green except that file, 2 FAIL, fixed and re-run green above) and again in part (machine shared with other workers, ~3 files per 100 s); `test_gate_preflight.py` was still running at report time (no FAIL line so far). `test_probe_debt.py` (in the printed list) failed once with a temp-dir `FileNotFoundError` (`calls.log`) under load; a re-run alone hit my 110 s timeout under the same load and printed no verdict, so it is UNPROVEN here, and this diff does not touch its code path (`probe_by_code.py` unedited). Other FAIL lines seen in the shared scratch folder (`test_selftest_slow_tests`, `test_audit_rules`, `test_config_migration`) belong to other workers' runs, not this tree.

## Needed from integration / config / analogs
- Needed from integration: none. New config keys: none.
- Analogs (not fixed): `estimate_record.append_record` writes no `delta`/`hit`/`ts` while the card names them (spec §4 sibling); printers above carry no `told`.
- Needed beyond the manifest: `host_adapter.py::role_has_bash`, `detector_verdict.py`, `stage_joints.py`, `test_handoff_values_main_block.py` (read only).
- Ratchet: `shrink: told_ratchet.unsited 17 -> 11; UNSITED_CAP 17 -> 11`.

- Needed beyond the manifest (owns): ai-packages/qa-factory/changelog.d/told-before-work-1-t1rc-site.md (the CHANGELOG fragment builder rule 4 requires).
owns-skip: ai-packages/qa-factory/changelog.d/told-before-work-1-t1rc-site.md -- CHANGELOG fragment owed by builder rule 4, not listed in owns
