# TBW-T1rc-site report (t-1568, TBW1-17)

Branch `worktree-agent-a45f5217496cff74f`, base 33ead99f. Commits: 8eed9b55 (code + `told-ratchet.json`), 01c4dae6 (test + changelog), 66a29d73 (test trimmed to the budget), the report commit after it.

## Plan items

- Site the 4 function ids: DONE - `source_preflight.py`, `estimate_record.py`, `artifact_producer.py`, `gate_preflight.py`.
- Site `s5_precheck:sides.provisional` / `sides.pending`: DONE - `s5_precheck.py` (`_sides_provisional` 9 sites, `_sides_pending` 2 sites).
- No-Bash door of `values_rename`: DONE - `handoff_check.py` (the rename refusal's `Problem.fix`).
- Test row per sited id (6): DONE - `test_detector_verdict.py::tbw_t1rc_site_sites`.
- `unsited` 17 -> 11 (-6): DONE (measured, `stage_joints.py --check`; `told_ratchet.unsited` NOT edited, EC-3).
- The door row (shell / no-shell) in the test: NOT written -- over budget (39 test lines = 38 code + 1 changelog). Proved by a scratch run instead (below).
- `told-ratchet.json`: `untold` 173 -> 163 (measured by `told_world()`, a ceiling); no K4 unit row moved (see Deviations).

## Site table (function | fragment | id | test row | proof)

F = proved fast by the row (run); S = same id and wrapper, no row of its own.

| function | fragment | id | row | proof |
|---|---|---|---|---|
| `source_preflight.check_source_inventory` | required file missing / no required sources / pending / materials lack receipts / source (material) unavailable and not accepted | `source_preflight:check_source_inventory` | t1rc source_preflight | F (missing text); the other five S |
| `estimate_record.facts_problems` | estimate facts must be an object / `<key>` must be an object / drivers must be an array | `estimate_record:facts_problems` | t1rc estimate_record | F (two problems of `{}`), the rest S |
| `artifact_producer.validate` | `triage[i]: instance_id and attempt_id required (missing: ...)` | `artifact_producer:validate` | t1rc artifact_producer | F |
| `gate_preflight.Rehearsal.check_question_branches` | `question branches - <variant_errors message>` (the caller of `planning_contract.variant_errors`, EC-2) | `gate_preflight:question_branches` | t1rc gate_preflight | F (2 findings of `BAD_PLAN`) |
| `s5_precheck._sides_provisional` | registry unreadable / kinds unverified / kind / settles_on / home x2 / dependent / dependents shape / marker without row | `s5_precheck:sides.provisional` | t1rc sides.provisional | F (kind), rest S |
| `s5_precheck._sides_pending` | pending-not-excused / pending-row-leftover | `s5_precheck:sides.pending` | t1rc sides.pending | F (not-excused), leftover S |
| `handoff_check.main` (rename refusal) | `delete <values file>` | `handoff_check:cli` (sub-id `.values_rename`, unchanged) | none | scratch run, see below |

Left bare (class code): `source_preflight` `validate_inventory` / `verify_inventory_files` lines, `review_missing`, "cannot be read" (other functions' texts or another requirement); `gate_preflight.add` rebuilds the message with `str`, so the Record rides only as the literal id (siting), nothing printed changes; `estimate_record.append_record` still raises `ValueError(compound(problems))` with plain strings (no `told` in `main`'s JSON: that would change a printed refusal, not asked).

## unsited

`unsited 17 -> 11` (`stage_joints.py --check`, summary line below). Rows sited: the 6 ids of spec 4.4.

## Door (F7)

Rule: `_doors(role)[0]` (the existing reader; True for a role with Bash, or a role not named / unreadable) -> today's `delete <file>`; else `say in your digest that `<file>` could not be renamed; the orchestrator removes it`. A role with Bash sees today's text byte for byte. Scratch proof (not committed, budget): a copy of the package with the 6 old files overlaid, the same row run: Bash role -> `['delete S2-qa-requirements-tester-1.values.yaml']` PASS; no-Bash role -> old file gives `delete ...` (red), new file the digest sentence (green).

## Old text (EC-1)

`/tmp/tbw/oldpkg` = the package with the six pre-change files byte-copied back; the test's `old` values are what that copy printed (`OLDVAL` lines): `source_preflight` b71a3229b88a50c7, `estimate_record` 18ea182807961c03, `artifact_producer` 1c42699e77eb33c7, `gate_preflight` 6961288ad83f1734, provisional 4dae0129d5649ae2, pending d52022a0aa35b627 (sha256[:16] of the text). The new files give the same values (the rows are green).

## Verbatim witness (one run after the last edit)

```
## control: artifact_producer:validate made bare (byte copy /tmp/tbw/ap.bak)
FAIL t1rc artifact_producer:validate: every item is a Record of the row, with its sentence - expected {(True, 'artifact_producer:validate', 'Every row also names its `instance_id` and `attempt_id`.')}, got {(False, None, None)}
=== test_detector_verdict: 839/841 ok ===       (1 of the 2 FAILs is the t4a one below)
... unsited 12                                  (11 + 1)
66a175e5df0e43ab   <- artifact_producer.py after cp restore
66a175e5df0e43ab   <- the byte copy   (hashes equal)
## WITNESS
FAIL t4a human word guard_pre_tool:PT-human-word: the problem text is the old one - expected '4da061f97df6c201', got 'e9c392cec0aad1d5'
=== test_detector_verdict: 840/841 ok ===
stage joints: ... told counters: hand_cards 12, legacy_legs 0, unsited 11
stage joints: clean
=== qa-factory selftest: 4/4 ok ===   (--limits --lang)
```

Also run (pre-final, same code): `test_handoff_values_main_block` 47/47, `test_source_preflight` 52/52, `test_estimate_record` 16/16.

The one FAIL (`t4a human word guard_pre_tool:PT-human-word`, a `guard_pre_tool` text) is not mine: it fails identically in the copy with the six old files overlaid (`/tmp/tbw/oldpkg`, same hashes `4da061f97df6c201` / `e9c392cec0aad1d5`), and no file of mine is on its path. Probably a path-dependent text in the worktree; not verified further (estimate).

## Not run locally

`scenario_walk.py --witness-for` printed 28 run-locally files and 50 judged by the canon; I ran only the DoD three plus the three neighbouring files above. Not run: the four `test_scenario_*` stories, `test_s5_precheck.py`, `test_handoff.py`, `test_question_branches.py` (its `branch_findings` is used by my row), `test_judgment_census.py`, `test_stage_joints*.py`, the slow files (canon). `test_stage_joints_told_real.py` not run as a test; its measurement (`told_world()`) was run by a scratch script: `rowless 1 untold 163`, every `by_unit` row equal to the fixture (no K4 unit differs).

## Deviations from the spec

- Spec 7 says K4 unit rows move `bare` -> `tagged` (e.g. `check_sides`). Reality: no unit differs after the edit (the two `sides.*` functions are not role-reachable units in the fixture, `check_sides` is untouched); the only change in `told-ratchet.json` is `untold` 173 -> 163, which the census measured.
- `stage_joints.py --check` is clean with `unsited` stored 17 and measured 11 (the ratchet is a ceiling here); TBW1-15 lowers the stored number.
- The spec said `told_ratchet.unsited` "goes down by 6": the stored value is not touched (EC-3), the measured one is 11.

## Analogs noticed (not fixed)

- `gate_preflight.add` and `estimate_record.append_record` drop the Record (message rebuilt by `str` / `compound`): the row is sited but never told there; a transport (JSON `told` in `estimate_record.main`) would be a printed-text change.
- 3 `refusal` local variable names in other `gate_preflight` methods (4442, 4445, 4619) now shadow the imported function inside those methods only; harmless, but a later siting there must rename the local.

## Rows that over-claim (EC-8)

none found.

## Mechanism paths

none staged.

## Needed beyond the manifest

`test_handoff_values_main_block.py`, `test_question_branches.py` and `test_s5_precheck_sides.py` helpers (read; the last two are imported by my row); `stage_joints_common.py`, `test_stage_joints_told_real.py` (read to measure).
