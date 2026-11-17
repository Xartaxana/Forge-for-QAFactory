# t-1048 -- told-before-work wave B fix round (critic t-1042 F1-F5, N-b, N-c)

Branch `worktree-agent-ad0767bec786dddde`, base a65afe58. Not pushed. No journal lines.

## Items
| # | where | what | witness |
|---|---|---|---|
| 1 F1 | `scripts/tests/fixtures/judgment-census.json` row `validate_artifacts.py::check_phase_json` | `note` added (a free `note` is a legal field: the header names it and 40+ rows carry one). Roles and ceilings untouched. | census C1-C5: 0 problems (measure below) |
| 2 F2 | `docs/tasks/specs/reports/20261117-tbw-t7a-b-report.md` site table line 25 and E6 list line 39 | bare branches of `check_phase_json` reclassed (code) -> (role): qa-requirements-tester, qa-test-strategist, qa-automator, qa-runner; pointer to node TBW-N1 | text edit |
| 3 F3 | `scripts/stage_guard.py:1238` | `return deny(DV.refusal("stage_guard:SG-walker-error", hooklib.WALKER_DOOR.format(reason=e)))`; the A24 key literal `hooklib.WALKER_DOOR.format(` is still in the source | `test_refusal_registry: 533/533 ok` after the edit |
| 4 F5 | `scripts/tests/test_detector_verdict.py` `tbw_t4b_sites` (last rows, ~2115-2135) | tautological `sg.deny(plain str)` control replaced by a row that drives the real `sg.check(event)` with the walker (`hooklib._Reader._code`, via `reader_patched`) raising; expects deny, id `stage_guard:SG-walker-error`, row sentence/door read from stage-joints.json (`SJ.row_for`/`told_text`), the problem text built from `hooklib.WALKER_DOOR`, `check:` last | positive 804/804; negative control below |
| 5 F4 | `scripts/tests/test_validators.py` | new `_sites_table(label, rows, allowed=())` called by `tbw_t7a_a_sites`, `_b_`, `_c_`; the three loops removed | 236 `t7a-` lines before and after, `diff` empty |
| 6 lint | `test_validators.py` | unused `dash` removed (in `tbw_t7a_c_sites`); the three now-unused `import stage_joints as SJ` removed too | `python -B -m pyflakes test_validators.py` rc=0, empty |
| 7 N-b | census row `stage_guard.py::explain` | roles -> `["conductor"]` (note says why); ceilings lowered; told-ratchet follows the measure | below |
| 8 N-c | `docs/tasks/specs/reports/20261117-tbw-t4b-report.md` lines 46 and 54 | EC-2 reason for `rule_delivery` corrected: only non-test caller is `check_command`; outcome unchanged | text edit |

### 1. corrected per-unit table line for check_phase_json
`validate_artifacts.py::check_phase_json | roles [qa-failure-analyst, qa-scout, conductor] (unchanged) | note: also met with no row by qa-requirements-tester, qa-test-strategist, qa-automator, qa-runner (broken-JSON + bare key branches); rows and true role set -> node TBW-N1 | told-ratchet bare 2, tagged unchanged`

### 3. byte identity of the walker text
Old file = byte copy taken before the edit (sha256 010d2dac...), new = edited. Same input (real `check`, walker raising IndexError, `git commit -m x t.py`), problem text sha256[:16]:
`old code 2 sha 573675dafe638c73` / `new code 2 sha 573675dafe638c73`. `LAST_DENIAL` is the problem only in both. Like every other T4b site, the siting adds the row's `  expected:` / `  door:` / `  check: <id>` lines AFTER the unchanged problem text (the old output had none). I read the spec's "no byte of the text a role reads" as the problem text, as the T4b report did. If the Lead meant the whole stderr, this site (and every T4b site) contradicts it.

### 4. negative control
Byte copies `stage_guard.orig.py` / `stage_guard.new.py` in the scratchpad; after restore both hash `1d819fd855560393af3ffbef66a15d6bd6be1d4a80d80fa23c93daf4c9d72802`.
With the item-3 site removed (orig in place):
`FAIL t4b the walker's door stage_guard:SG-walker-error: the old problem text, then the row's lines, `check:` last ...` and `=== test_detector_verdict: 803/804 ok ===`
With the site: `=== test_detector_verdict: 804/804 ok ===`.

### 5. helper design note
`allowed` is `()` for tables A and B (every message carries exactly the id; same PASS text as before). Table C passes a dict `{row name: extra ids}` (only `check_test_report` has extras) and keeps its own two assertion texts ("the first message carries the id", "every message carries an id of the allowed set"). The spec gave the signature `allowed=()` without saying how table C's per-row set is passed; the dict is my choice, flagged.

### 7. N-b
Grep over agents, references, skills (and commands), shape `stage_guard\.py"? +--(ticket|explain)|stage_guard\.py.*--stage|--explain`: no hit. Positive control of the same shape (`stage_guard\.py"? +--(stories|zzz)`) found `skills/qa-doctor/SKILL.md:183`. `explain` is called only from `stage_guard.py:3571` (`--ticket` and `--stage`); the doctor skill names only `--stories`. Roles: `["conductor"]` (qa-doctor is not a census role).
Measure (`T.told_baselines(T.told_world())` of test_stage_joints and `CT.analyse` of test_judgment_census, scratch script; first run, before the fixtures were updated): `rowless 3 (fixture 3)`, `untold 173 (fixture 175)`, units `210 (fixture 211)`; unit diff: `stage_guard.py::check` bare 0 (fixture 1), `stage_guard.py::explain` gone; C3: 12 roles one below their ceiling, conductor 748 unchanged.
Lowered numbers (nothing raised):
- blocking_per_role: qa-automator 138->137, qa-bug-reporter 98->97, qa-case-critic 114->113, qa-case-designer 102->101, qa-code-critic 104->103, qa-doc-scribe 107->106, qa-failure-analyst 108->107, qa-requirements-tester 119->118, qa-retro-analyst 99->98, qa-runner 109->108, qa-scout 97->96, qa-test-strategist 132->131.
- told-ratchet.json: `untold` 175->173; unit `stage_guard.py::check` bare 1->0 (the walker site); unit `stage_guard.py::explain` removed (211->210 units).
After the update (same tool): `rowless 3 3 untold 173 173 units 210 210`, `problems total {'C1': 0, 'C2': 0, 'C3': 0, 'C4': 0, 'C5': 0}`, measured per_role equals the fixture's.

## Witness (verbatim)
- `scenario_walk.py --witness-for ai-packages/qa-factory/scripts/stage_guard.py` prints 4 scenario rows (cart-1, dry-1, local-1-0108, local-1-arm-b) and 30 `keep` files; it marks none slow. Run by me: test_validators, test_detector_verdict, test_refusal_registry (the A24 check), stage_joints and contract_slices checks, the census/told measure above. NOT run (batch canon): test_stage_guard.py and the other keep files, test_stage_joints.py and test_judgment_census.py (measured through their functions instead), the scenario files.
- `python -B scripts/tests/test_validators.py` -> `=== test_validators: 579/579 ok ===` (same count as before)
- `python -B scripts/tests/test_detector_verdict.py` -> `=== test_detector_verdict: 804/804 ok ===` (was 802: the walker row is 3 checks, the dropped tautology was 1)
- `python -B scripts/tests/test_refusal_registry.py` -> `=== test_refusal_registry: 533/533 ok ===`
- `python -B scripts/stage_joints.py --check` -> `... told counters: hand_cards 12, legacy_legs 0, unsited 17` / `stage joints: clean`. `unsited` before 17, after 17: no move (the counter does not see A24-parented sub-ids, critic N-a, node N2); the K12 pin did not move.
- `python -B scripts/contract_slices.py --check` -> `slices: 44 declared, all present and fresh; 19 key pages; 12 charters carry a generated digest line`
- `python -B -m pyflakes ai-packages/qa-factory/scripts/tests/test_validators.py` -> rc=0, empty (no `dash` line); same for `stage_guard.py`.

## FR walk
- A (refusals): FR-1 and FR-38 for the walker site: problem text unchanged; the Record adds `expected` and `door` of the existing row `SG-walker-error`. FR-4 and FR-59: still a deny.
- AR-10 (the walker site carries its told row), AR-20 (only lowered numbers; none raised).
- B, C, D, E, F: not touched. G: no Cyrillic in added lines, tests are table rows.
- Changelog fragment: none (problem text byte-identical; only the row lines follow, as at every T4b site). If the Lead counts those lines as "what a role reads", a one-bullet fragment is owed.

## Beyond the manifest
`scripts/tests/test_stage_joints.py`, `test_judgment_census.py`, `harness.py` (the measure, `reader_patched`), `scripts/detector_verdict.py`, `scripts/refusal_registry.py`, `references/stage-joints.json` (read-only), `scripts/tests/test_stage_guard.py` (walker probe pattern), the agents/references/skills grep.

## Analogs noticed (not changed)
- `tbw_t4b_sites` no longer pins a dispatch-time bare refusal (the old control was the walker one); nothing asked for it.
- Other census rows labelled "every role meets the hook guard" (T1a Q3) may be overstated the way `explain` was; not walked.
