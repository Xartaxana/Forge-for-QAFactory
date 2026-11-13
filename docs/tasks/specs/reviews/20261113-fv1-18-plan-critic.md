Critic on plan: FV1-18 selector contract spec (t-493)

report: not written. The handoff gate refused C:\QAFactory\forge-repo\docs\tasks\specs\reviews\20261113-fv1-18-plan-critic.md ("no handoff path inside docs/tasks/specs/reviews in the dispatch"). As you asked, this is the short hand-back. The full verdict, ending with the json block, is the content of my refused Write call in the transcript; extract it from there (tools/handback_extract.py).

VERDICT: ACCEPT WITH FIXES (fit_with_fixes). 0 blocking, 7 to fix before dispatch, 5 minor. Accepting the plan is the Lead's decision.

Main results:
- K1: the cause in §0.2 is confirmed. The rehearsal record is digested from the command with its `env`; `selectors_verified` digests the argv words alone. N1's fix matches the record for the measured command and still refuses a record of another command, with one exception (D5).
- K3: after N2 a wrong selection or an empty one still cannot come out green. `run_suite.py:505-539` and `_file_verdict:688-692` bind rows by exact report id and give `not_run`.

Fix before dispatch:
- D1: N1's `tests >= 1` rule breaks keep test test_probe_by_code_languages.py:1887 (its fixture at :1867 has no `tests`), which N1 does not own. The quarantined test_profile_contract.py:176 breaks too. Recommendation: drop the `not_counted` state.
- D2: on the `--request` road (and on `--mine` when the precedent command is copied unchecked) the note judges the profile's one_test, not the command that actually runs. The old pytest check read the request's command (execution_request.py:3465).
- D3: "reuse executor_gap's lookup" cannot be done inside N2's owns: the lookup is inline code (run_suite.py:1585), so it needs a helper and `executor_gap` added to the owns.
- D4: the note text, E1, R-N2-4 and the AR-28 row say `not_executed`; the rows actually record `not_run` with reason "report row missing".
- D5: a foreign `env` drops out of `command_identity`, so it can match an older row of the same argv and read as verified for a different command. It should give state `no_command`, False.
- D6: N3's new wording must keep "selector contract is verified": keep test test_probe_fix_round.py:38 (not owned by N3) checks for it.
- D7: N4's data key is not named, and launch_check needs a new reader branch for it, because hooklib drops unknown run_forms keys.

Minor:
- M1: the F2 question can be answered now. `_match`/`covered` do not compare the whole command; `request_digest` does, so a request built before the upgrade costs one extra launch, never a false reuse.
- M2: cite run_suite.build_run_block as the S5 binder (bind_row is the red probe's).
- M3: a non-bool `selectors.verified` literal, and where `hand_unreadable` sits in the order.
- M4: `profile_contract` must import `execution_request` lazily (cycle).
- M5: a rehearsal of "the command as declared" runs the whole command and still counts as proof (queue candidate).
- Also: R6(a) now passes on pytest-shaped profiles (state it in the spec); line numbers of T5's §5.4 rows 11, 16 and 18 shift after N2.

questions: none
needed beyond the manifest: read-main scripts/gate_preflight.py, red_sandbox.py, launch_check.py, references/record-schemas.json, tests/test_probe_fix_round.py, test_guard_write_owners.py, test_probe_walk.py
