# P-b report (t-1076): `probes.runtime_provenance` has a producer on the critic's road

Branch `worktree-agent-a3398935dd81f7c74`, one commit (sha in the final message), not pushed.

## Done

- `handoff_check.py`: `_story_record` (the tail rule extracted, one copy: C1), `window_runtime_record(..., *, probe_run=False)`
  with `_PROBE_RECORD_PRODUCER`, `_probe_run_record` (joins only), `_probe_runtime_provenance`, and the `DERIVERS` key
  `probes.runtime_provenance` rebound (the other two keys keep `_runtime_provenance`). `from pathlib import PurePosixPath` moved into `_story_record` (N-1). The run-block branch stays above the probe branch (item 2.4).
- Outcomes as the fix-round states: J1 (jobs unreadable, exception), J2 (`bad` job files named), J3a (no own `red_probe` job: "no probe of this review ran through run_suite (none was launched, every one was refused before it started, or every one was answered by an earlier probe's receipt, which belongs to another dispatch)"), J3b (own `red_probe` jobs exist, none completed with a stand reading: count and newest job's status), J4, J5, J6 (all own completed probes `runtime_required: false`: no door named, no producer tail), success source "the stand reading of red_probe run <job> ...".
- `_probe_run_record` docstring names that J2's glob count restates JobStore's layout and may drift (N-3). Wording "the record the launch reading cites" (F-6).
- Tests, existing `test_handoff.py` only: helper `_probe_job`, table `the_probe_record_is_the_reviews_own` (registered in `main()` after the C3 table), and the (c1)/(c2) variant in `the_blank_provenance_field_says_why_code_could_not_fill_it`. Expected values come from the card, never from the deriver (P11 asserts membership in `{a, b}`).
- Changelog fragment `ai-packages/qa-factory/changelog.d/p1b-pb-probe-run-record.md` (ASCII, verified 0 non-ASCII bytes).

## Edge table (edge | row | result)

| Edge | Row | Result |
|---|---|---|
| E1 no dispatch | P20 | PASS |
| E2 unreadable run block | P4 | PASS |
| E3 own run block (path / named reason), job never outranks | P2 (also byte-identical to `probe_run=False`), P3 | PASS |
| E4 no jobs folder | P5 (J3a) | PASS |
| E5 other dispatches' jobs | P6 (J3a) | PASS |
| E6 purpose not red_probe | P7 (J3a) | PASS |
| E7 status persisted/running/incomplete/absent | P8 x4 (J3b) | PASS |
| E8 launch reading absent / {} / str / list | P9 x4 (J3b) | PASS |
| E9 several jobs | P10 (newest decides), P11 (membership) | PASS |
| E10 newest refs empty / not list / not str / blank, older good | P12 x4 | PASS |
| E11 missing file / `../X` / another story / placeholder | P14 x4 | PASS |
| E12 other machine path | P15 | PASS |
| E13 malformed / BOM / list / no request | P18 x4 (J2) | PASS |
| E14 import/glob/jobs raises | no row (card: optional) | covered by `except` only |
| E15 temporal | P9 + (c1) | PASS |
| E16 positional | P2, P3, P4, P20 | PASS |
| E17 automator/runner never reach the branch | P21 (reason byte-identical to `window_runtime_record(task, A)`, carries `runtime_probe.py`, no `probe_by_code.py`; DERIVERS bindings) | PASS |
| E18 | P1 | PASS |
| E19 10000 refs | P17 | PASS |
| E20 non-ASCII ref (`ü` escape) | P16 | PASS |
| E21 forged request file | P19b (J3a) | PASS |
| P19 spaces around dispatch_id | P19 | PASS |
| E22 `runtime_required: false` only | E22 (J6, asserts NO `probe_by_code.py`), E22b (mixed -> J3b) | PASS |
| E23 repair round, only an earlier dispatch's job | E23 ("belongs to another dispatch") | PASS |
| blank refusal on the critic form | (c1) filled, not a problem; (c2) one `blank` problem with `Code could not fill it:`, the dispatch and `probe_by_code.py` | PASS |

Decision noted (fix-round left it to wording): J6 applies only when there is at least one completed own `red_probe` job and EVERY completed one has `runtime_required is False`; any other no-reading case is J3b. An absent `runtime_required` key is read as required (run_suite's own default, `.get("runtime_required", True)`).

## Controls

- C1: `_story_record(` : 1 `def` (line 526), 2 call sites (594, 646); `parts[::-1]` occurs once (535).
- C2: row P1 and (c1) are red with the deriver disabled (below) and green after.
- C3: every no-path reason on the probe road other than J6 contains `probe_by_code.py` (table assertion); J6 asserts the absence.
- C4: rows P4, P18. C5: row P21. C6: `test_judgment_census.py` 25 passed with no census edit.
- Negative control (byte copy): `cp handoff_check.py -> scratchpad/handoff_check.orig`; `sed` turned `probe_run=True)` into `probe_run=False)` inside `_probe_runtime_provenance`; `test_handoff.py` then printed FAIL for P1 (`expected ('evidence/runtime-provenance-api-b.json',), got (None,)`), P10, P11 and the reason rows (P3-P9, P12, P18 ... ). Restored by `cp`. sha256 before and after identical:
  `7dbbeb767b64ba82de8b650288870bab2aea208628b20da88033d0301d5d7e04` (both).
  Quoted red line: `FAIL P1 dry-world shape: the launch reading, not the request's copy: the path — expected ('evidence/runtime-provenance-api-b.json',), got (None,)`.

## Witness (verbatim tails, each after the last code edit)

```
python -B ai-packages/qa-factory/scripts/tests/test_handoff.py
=== test_handoff: 749/749 ok ===

python -B ai-packages/qa-factory/scripts/tests/test_field_producers.py
known red rows 21, not in world rows 47, rows walked 870
=== test_field_producers: 885/885 ok ===

python -m pytest ai-packages/qa-factory/scripts/tests/test_judgment_census.py -q
.........................                                                [100%]
25 passed in 51.56s

python -B ai-packages/qa-factory/scripts/selftest.py --limits --lang
PASS limits: SKILL.md / agents / references within size caps
PASS limits: every mandatory role rule of design/role-rules.json holds in its carrier
=== qa-factory selftest: 4/4 ok ===
```

(Order: all edits, then the negative control with its byte-copy restore, then these runs on the restored file.)

`scenario_walk.py --witness-for ai-packages/qa-factory/scripts/handoff_check.py ai-packages/qa-factory/scripts/tests/test_handoff.py` printed the scenario rows (cart-1, dry-1, local-1-0108, local-1-arm-b), 24 keep rows for `handoff_check.py`, and for `test_handoff.py` "no scenario or keep row covers scripts/tests/test_handoff.py: run the whole scenario layer" with the scenario files. Slow (judged by the batch canon, not run): test_scenario_cart_1, test_scenario_dry_1, test_scenario_local_1_0108, test_scenario_local_1_arm_b, test_brief_pack_s5_plan, test_bug_records, test_guard_dispatch_budget_and_logs, test_handoff_inline_values, test_handoff_values_keys, test_handoff_values_main_block, test_handoff_values_refusal, test_s5_plan_controller, test_s7_investigation_replay, test_story_step_start (test_handoff, test_field_producers, test_judgment_census were run above as this change's own judges). Fast, run:

```
test_artifact_writers: 23/23 ok   check witness: 34/34 ok   test_knowledge_notice: 15 passed   test_null_outcomes: 327/327 ok
test_open_list_fields: 15 passed  test_triage_blocked: 50/50 ok   test_triage_identity: OK
test_scenario_walk: 95/95 ok      test_scenario_world: 33/33 ok
```

## D. Read-only measure in the kept dry world (N6; world still present, nothing written)

```
('evidence/runtime-provenance-dry-pytest-20261117T075258Z.json', 'the stand reading of red_probe run 44bcd10c384267c69a56 (dispatch S5-qa-code-critic-1, state/execution-jobs/)')
(None, "no run block of dispatch S5-qa-code-critic-1 under work/run-blocks/ carries a runtime_provenance record: this dispatch ran no test through run_suite, or its run was refused before it started; the record is written by runtime_probe.py when run_suite runs this dispatch's tests")
('evidence/runtime-provenance-dry-pytest-20261117T075205Z.json', 'the runtime_provenance of run block work/run-blocks/20261117T075212305241Z-66bd1d15b5fe5da442d7.json (dispatch S5-qa-automator-1)')
```
All three as the card states.

## FR pass (touched sections)

- A refusals: FR-1 the reasons say what is wrong and what was expected; FR-2 every probe-road reason except J6 names `probe_by_code.py`/`red_sandbox.py --probe`, J6 names no door because none re-runs a probe that has no stand; FR-4/5 n/a (no check added); FR-46/48/50/57 n/a.
- B: the only person-read text changed is the blank refusal's tail on the critic form (FR-1/FR-2 lines above); FR-6 n/a, no question to a person.
- C: FR-11 the field gets a producer on the critic's road (AR-22); FR-13 no closed list in code; FR-14 the deriver's tuple shape `(path, source)` / `(None, "", why)` unchanged; FR-39 n/a; FR-42 every returned job state has a move or named blank.
- D: FR-16/17 one reader, tail rule shared; FR-40 n/a; FR-58 no expectation taken from the new code (P11 membership); FR-59 every unknown is blank with a name (J1, J2, J3a/b, J4, J5, J6).
- E: FR-37 `state/execution-jobs/` is written by `run_suite.py` (JobStore); FR-41 no unknown reported as fact (J6/J3a/J3b worded by what is known).
- F: n/a. G: FR-29/30 package file ASCII (selftest --lang green); FR-31 no load-sensitive test; FR-32 test row per edge; FR-54 siblings below.

## Analogs noticed (not fixed)

- The run block's `runtime_provenance` is the request's possibly-copied record, not `runtime_probe_before` (`run_suite.py:582`); one road for the three provenance fields (F-5, queued by the Lead, SIBLING_MAP axis 5).
- The run-block twin (critic F-5) is the Lead's. FV2-76 (typed value vs this reader: table needs the critic path), FV2-67 (this card performed the `_story_record` extraction; its node should import it), FV2-78: pointers are the Lead's.
- `artifacts.probes` on the automator's form (card section 7 scout priority): untouched.
- The reserved null outcome `no_runtime_record` (`null-outcomes.json` row for this field) is not wired; J6/J3 are its eventual home.
- Repair-round meaning question (should a review that reused earlier probes carry the earlier run's record?) stays for the owner; value is blank (E23).

## Changelog fragment

```
- the code critic's `probes.runtime_provenance` is filled by `handoff_check --fix` from the stand reading run_suite takes when it
  launches the review's own red probe (`runtime_probe_before` of the dispatch's newest completed `red_probe` job under
  `state/execution-jobs/`); a run block of the dispatch still decides first; the automator's and runner's fields are unchanged;
  a field code cannot fill says why and, where a probe run could still give it, names `probe_by_code.py` (P-b)
```

Beyond the manifest: `slow_tests.json` (to classify slow files); `selftest.py` (grep). tests-over: rows per edge of the deriver.

## Fix round after critic t-1078

- FIX-1: `handoff_check.py` J6 test is now `not job["request"].get("runtime_required", True)` (run_suite.py:2904). Rows beside E22: `runtime_required` None and 0 -> J6, no door (E22 rows in `test_handoff.py`).
- FIX-2: `_PROBE_RECORD_PRODUCER` now "the record is the file the stand reading cites, which run_suite takes when it launches this review's own probe: ..." (probe_by_code.py kept); changelog fragment "from the record cited by the stand reading run_suite takes when it launches". No row asserted the old words.
- NOTE-1: P8 rows assert "1 red_probe run(s)" and "status <s>" (a fixture with no status prints `absent`, as the code does).
- Ledger: `known_red.json` row `main/S5`, `raised_by` replaced verbatim; `pins` and other rows untouched; the dry scenario was not run. `test_known_red`-style pin: field_producers run says "known_red: the red rows of the walk are exactly the ledger" PASS.
- Witness tails (T/ai-packages/qa-factory): test_handoff `=== test_handoff: 757/757 ok ===`; test_field_producers `=== test_field_producers: 885/885 ok ===`; selftest `=== qa-factory selftest: 4/4 ok ===` (--limits --lang); known_red.json: `json ok`.
- Mid-run: first test run had 2 FAILs of my own rows (a misplaced loop in the E22b block; the `absent` status word); both fixed, then green.
