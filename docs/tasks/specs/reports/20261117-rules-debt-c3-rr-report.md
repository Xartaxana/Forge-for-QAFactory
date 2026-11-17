# C3-rr report (t-1055) - reporter_rehearsal_identity: the reuse through the predicate

Base: branch `worktree-agent-aa11322709a274e56` (a4aca646, C3-0) + `git merge origin/main` (no conflicts; merge commit 960bcf9c; the merge's forge_metrics line about gate_template.py "matches no feature" is a WARN, not a refusal).

## Items (file:line)
1. Registry row `reporter_rehearsal_identity`: `gate-registry.json:517` `"accepts": {"reporter_rehearsal_identity.reuse": ["matched"]}`; `status: converted`, `debt_ref: ""` at the row's status line (:523). Words, verdict_map, sites, roles untouched.
2. `gate_preflight.py:3844` `if isinstance(hit, dict) and isinstance(hit.get("at"), str) and acceptable(earlier.get("state"), "reporter_rehearsal_identity.reuse"):` (the two hit checks first, E3); import `gate_preflight.py:87` `from gate_template import acceptable` at module top (cycle-free: gate_template -> gate_registry -> hooklib, stdlib only; imported fine).
3. Tests: table of `test_c3r_reporter_rehearsal_identity_an_unknown_is_rehearsed_again_never_reused` (`test_gate_preflight.py:5199`) is now `(state, reused, variant)`: the 4 old rows + `Same_command`, `None`, absent state (variant "absent"), `same_command` with the map holding ANOTHER key (variant "other_key"; grep: no case of test_gate_preflight.py pinned it - `test_reporter_rehearsal.py:1164` pins an older-key case, not owned), `same_command` + unreadable registry (variant "registry": `GT._READ[:]` set to `({"rows": "x"}, structural_error(...))`, restored in `finally`, :5212 on). No new function or file. Expected values from the row's `decides` / C3-0 E2.
4. S-f pins (`test_gate_registry.py`): EXPECTED_DEBT -reporter_rehearsal_identity (:58-62); EXPECTED_CONVERTED + it (:66-72); K-T1.2 "7 gate(s) left as debt:" (:250); split 20/7/6 with comment (:338-340); D13 triple `_reporter_outcome` removed (was :940); `D13_ITEM_COUNT = 145` with the comment line (:1009-1011). F4 unchanged (row already `code`).
5. No text moves: `_EARLIER_SAYS` and the rehearse branch untouched.

## D13 / S-f numbers (measured on the MERGED tree with `GR.analyse(GR.PLUGIN_ROOT)`)
before: 146 items / 50 triples (the triples include `_reporter_outcome` and `_record_unreadable`); after: 145 items / 49 triples, `_reporter_outcome` gone, `_record_unreadable` stays. The base after merging main is 146 (main's merge brought no D13 change).
`gate_registry.py --sites | grep -c _reporter_outcome`: 1 before (`gate_preflight.py:3843 _reporter_outcome earlier['state'] == 'same_command' [reporter_rehearsal_identity]`), 0 after.
Debt block: before 8 gates (incl. reporter_rehearsal_identity), after 7.

## Witness
`python -B ai-packages/qa-factory/scripts/gate_registry.py --check` -> exit 0:
```
A26 gate registry: no violations
  7 gate(s) left as debt:   (reporter_rehearsal_identity absent; no F-b line)
```
A1 audit (`audit_factory.py`, `a1_findings`): `A1 hook liveness: no violations`. Control (byte copy of gate_preflight.py with the import line removed): `['gate_template.py is reachable from nothing ... dead code shipped as if it ran']`; restored from the copy (`cmp` identical).
Row function called directly from a scratch script (all PASS, 27 lines; the last four of the table): `PASS reporter_rehearsal_identity `same_command`/key hits: reused=True, and the command is run 0 time(s)` ... `PASS ... `Same_command`/key hits: reused=False ... 1 time(s)`, `PASS ... `None`/key hits: reused=False`, `PASS ... ``/absent: reused=False`, `PASS ... `same_command`/other_key: reused=False`, `PASS ... `same_command`/registry: reused=False, and the command is run 1 time(s)`.
Negative control (the predicate call replaced by `earlier.get("state") == "same_command":` on a byte copy): `FAIL reporter_rehearsal_identity `same_command`/registry: reused=False, and the command is run 1 time(s) — expected (False, 1), got (True, 0)`; restored from the copy, sha256 identical, 0 FAIL after. (Only the registry row discriminates: every unknown-WORD row is rehearsed by the old comparison too.)
`scenario_walk.py --witness-for <the four owns>`: 39 lines (4 scenarios, keep rows, 6 scenario files for test_gate_registry.py). Non-slow files run (slow_tests.json < 10 s or absent), rc 0, 0 FAIL: question_status 25/25, gate_role_accounts 44 passed, scenario_local_1_arm_b 5/5, scenario_walk 95/95, scenario_world 33/33, stand_gaps 182/182, gate_vocabulary 141/141, handed_to_person 58/58, login_need 33 passed, manual_capture 1213/1213, not_needed_role 22 passed, one_source_per_fact 21/21, reference_window 85/85, whole_identifier 166/166. `selftest.py --lang`: `PASS lang ... === qa-factory selftest: 2/2 ok ===`. Slow files (test_gate_preflight.py, the other scenarios...) judged by the batch canon.
I also ran `test_gate_registry.py` once (20 s): `=== test_gate_registry: 487/488 ok ===`, the one FAIL is the finding below.

## FINDING (needs a Lead decision) - K-T1.13 NEG fails after this change
`test_gate_registry.py:869` `FAIL K-T1.13 NEG: CLI_SCRIPTS without it names gate_registry.py as dead code`. Cause: the control discards `gate_registry` from `audit_factory.CLI_SCRIPTS` and expects A1 to call it dead; with `gate_preflight` (hook-reachable) now importing `gate_template` -> `gate_registry`, gate_registry is reachable by import and A1 no longer names it. Not an A1 regression (A1 is green); the control's premise is outdated by the first consumer of gate_template. Every later C3 card inherits it. Not fixed: it is outside "pins of this row only", and which control replaces it (another dead script? an in-memory one?) is a design decision. Question for the Lead.

## FR walk (sections touched)
A refusals/doors: no refusal added (the branch rehearses, as before). B text: no person-facing text moved. C contracts: FR-13/AR-13 the word is read through the registry predicate; the consumer and its reader land in one commit (AR-22). D identity: FR-59 unknown never reuses (E1/E2 pinned). E, F: not touched. G: FR-30 `--lang` green, FR-29 no control bytes, FR-54 siblings below.
Architecture: AR-13 (the reuse word is read only through gate_template.acceptable), AR-22, AR-28, AR-29 (xref, owner data, no census unit), AR-20 (debt -1, converted +1, D13 -1 triple).

## Siblings / analogs (report only)
- `_record_unreadable` (produce, `earlier.get('state') != 'unreadable'`) and `_rehearse_reporter` (`countable['state'] == 'none'`): registered, left as the card says.
- `profile_contract.selector_contract:417` (`state == "same_command"`): second reader of `earlier_proof`'s word, registered in no row (waiting finding, not carded).
- `test_reporter_rehearsal.py:1164` already pins an older-key `same_command` case (analog of the added other_key row).

## Beyond the manifest
`audit_factory.py`, `scripts/slow_tests.json`, `.github/workflows/forge-check.yml`, `test_reporter_rehearsal.py` (grep), `test_gate_registry.py:842-870`.
No journal lines, no push.
