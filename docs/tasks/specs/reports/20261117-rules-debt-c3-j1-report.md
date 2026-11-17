# Report: node rules-debt/1/RD1-13, C3-j1 (t-1206), builder

Branch: worktree-agent-a5dcea7ed81ed1834. Card: `docs/tasks/specs/20261117-rules-debt-c3-j-card-r3.md` §2.

## Status: items 1-7 of §2 done; the owner's correction (failed measurement keeps its REASON) NOT implemented: returned as questions

The correction is a design fork the card does not settle (rule 1: no invented requirement). The code is as card §2 item 3 step 6 says
(a failed measurement records nothing, a note by owner, retried at the next rehearsal). Questions for the Lead:

1. Where does the reason row live? The registry store is stated, but not the key. Same key `environments.page_load` with another element
   (for example `frontend_failed`) and a value `{cause, why, at, attempts}`, or a new catalogue key `environments.page_load_failed`?
   (`page_load()` reads one element of `environments.page_load`; a new key means a second catalogue row, FIVE_KEYS pin, `needed_by`.)
2. "A second start with the reason present makes one attempt and carries the reason to whoever acts": does that mean retry exactly once
   per rehearsal (so attempts count rises by 1 each gate A) and then NEVER stop, or is there a cap (attempts N: stop measuring, only report)?
   Which `cause`s are retried at all (`no_browser` is a fact of one machine, AR-4: a registry row carried to a colleague's machine would
   stop that machine's attempt; `unreachable` is a moment of downtime)? What "names what changed" means in code (a changed definition_sha
   or address makes the reason stale, as for a number)?
3. "Carried to whoever acts": to the conductor through the gate note only (the existing note, with the kept reason and the attempt
   count in `extra`), or also a brief line for the roles (AR-10/AR-11 would then add a line to ratchets)?
4. Is a kept reason shown at the S5 brief when the number is absent (brief line)? Card E15 says no line on `none`.
5. Which writer: `check_stand_page_load` through `PK.record` (a new `source`/`by` value is already added: `measured`/`gate`), with the
   "same value -> existing row" rule of `record` (:789) conflicting with "attempt count" (a new row each time, or the value carries
   the count and changes)?

## What was done (files)

- `scripts/project_knowledge.py`: constants, `SOURCES`+`measured`, `BY`+`gate`, `_page_load_value_faults` and its branch in
  `record_problems` (before the role rules), `stale_against_verified`, `page_load` (11 steps, pure, never raises), module docstring.
- `scripts/manual_capture.py`: `PAGE_LOAD` seam, `measure_page_load`, `timeout_for(project_root, cfg, stand)` (`max(180, load+30)`), the four
  callers; constant comments. Lazy imports only (the import line :99-100 untouched).
- `scripts/gate_preflight.py`: `_page_load_due`, `check_stand_page_load` (+ helpers `_page_load_text`, `_page_load_failed`,
  `_page_load_address`), place in gate A tuple after `check_s5_stand_limits`, `run` docstring, `measurement_is_stale` one-line delegate, call
  :2808 changed.
- `scripts/investigation_probe.py` (call), `scripts/walk_session.py` (call).
- `scripts/brief_pack.py`: `STAND_LOAD_ROLES`, `stand_page_load_lines`, one call after the `test_timeout_line` statement.
- `references/config-keys.json` (row `environments.page_load`, `needed_by` of `environments` and `gate_rehearsal`),
  `references/manual-evidence.md` (the 180 s sentence), `judgment-census.json` (one row), `scaffold.py` (`measured` block deleted),
  `changelog.d/rules-debt-c3-j1-stand-page-load.md`.
- Tests: `test_project_knowledge.py` (FIVE_KEYS pin, 3 test functions with a 14-row shape table, age and state rows), `test_manual_capture.py`
  (`timeouts` replaced, `measure_page_load_table` new, 100 s expectations moved to 180 s), `test_gate_preflight.py` (default stub at import,
  6 new test functions, `NEW_CHECK_FUNCTIONS` and the FR-6 scan list, `_ProbeWorld.limits`), `test_brief_pack.py` (`c3_j1_stand_page_load`).

## Deviations and findings

- `plans/builder-rules.md` does not exist (told); read `.claude/agents/builder.md`.
- E15 estimate: the measured line is 258 B (`STAND_LOAD_LINE_BYTES 258`, printed by the test), not about 230 B. No ratchet moves on the seed
  (no registry row: no line); a real run with a measurement grows the three briefs by about 258 B each. Ratchets not re-run (see witness).
- `test_manual_capture.py` had one hidden `if seconds <= 100:` branch (http timeout row) beside the 100/100.001 pair: moved to 180.
- `check_stand_page_load` helpers `_page_load_text` and `_page_load_failed` hold the sentences; the FR-6 literal scan lists only
  `check_stand_page_load` (per card); the global sweep test `test_t357_every_text_of_every_run...` reads every note of my rows (it passed
  in the slice run).
- `timeout_for` callers (8 sites, Grep `timeout_for\(` over `scripts/`, non-tests): `gate_preflight.py:2808` self.project_root/self.config;
  `manual_capture.py` sign_in :3084 (project_root, cfg), run_ui :3247, run_app :3482, http run :5452 (all `project_root`, `cfg` in scope);
  `investigation_probe.py:419` (project, cfg); `walk_session.py:1221` (self.project_root, self.cfg). None passes None.
- 100-s hits in `test_manual_capture.py` (one per line): :61 comment, :172-179 timeouts table (replaced), :194 ui opened (180), :248 AT/BEYOND
  (180/180.001), :262 "limit is 180 s", :266 `limit_s: 180`, :269-273 wait 180000/180001, :951 AT 180/BEYOND 180.001 and its `<= 180`
  branch, :1040 comment, :1467 `LANDING_LIMIT = MC.DEFAULT_TIMEOUT_S`, :1558 "within 180 s", :1660-1681 poll 720/721, 180.0. Kept as
  independent explicit parameters: :1919 `StepTimeout(100)`, :2429-2611 `timeout_s=100` of `_input_step`.
- Siblings (axis 5/34): the builder did NOT run the prose-twin Grep of `s4.md`, `s5.md`, agent charters for `page load|timeout|wait`
  (context cap at ~250K reached): not done, to the Lead or a next round. Axis 34: gate A holds the measurement, as the card says.
- Same-class sighting (rule 5): the reporter's `timed_out` card (card fork F-j-reporter) and, after the correction lands, `_page_load_failed`'s
  "measured again at the next rehearsal" text (it says retry; the correction may change it).

## Witness

Slow-listed and named, not run as whole files: `test_gate_preflight.py`, `test_brief_pack.py`, `test_judgment_census.py` and the 33 other
`SLOW_TESTS`/`test_story_run_*`/`test_controller_*` files of the printed list (batch canon). Two honest partial runs of my own rows:

- `python -B <scratchpad>/run_pl.py` (imports `test_gate_preflight`, calls the six `test_c3_j1_*` functions + the FR-6 sweep):
  `=== c3-j1 slice: 50/51 ok ===`; the one FAIL is `the sweep saw a good many texts` (a slice records few texts; the rule check itself passed).
- `python -B <scratchpad>/run_bp.py` (calls `c3_j1_stand_page_load`): `STAND_LOAD_LINE_BYTES 258`, `=== c3-j1 brief slice: 17/17 ok ===`.
- `python -B scripts/tests/test_manual_capture.py` (from tests dir): `=== test_manual_capture: 1236/1236 ok ===` (it is slow-listed; run
  because it is an owned test file with expectations that moved).
- `python -m pytest test_project_knowledge.py -q`: `176 passed`.
- The 41 non-slow files printed by `scenario_walk.py --witness-for <the 14 owns>` (list: scratchpad `run-list.txt`), each `python -B <file>`:
  39 lines `N/N ok` or `passed` (e.g. `test_first_look: 450/450 ok`, `test_exploratory_findings: 362/362 ok`, `test_first_look_briefs: 261/261 ok`,
  `test_codex_tool_guidance: 217/217 ok`, `test_fit_targets: 116/116 ok`, `gate A: question status from the register: 25/25 ok`,
  `test_guard_project_knowledge: 10/10 ok`, `test_first_look_wiring: 102/102`, `test_project_knowledge: 176 passed`); no FAIL/Error line in
  the 41 outputs (`grep -E "FAIL|failed|Error"` over the collected output: empty; positive control: the same file holds the `ok ===` lines).
- Grep (2) `PAGE_LOAD_KEY|environments\.page_load` case-insensitive over `scripts/`: non-test writer only `gate_preflight.py:3271`
  (`PK.record`), reader code uses `PK.page_load` (`manual_capture.timeout_for`, `brief_pack.stand_page_load_lines`); positive control: the
  same call finds `project_knowledge.py` lines.
- (3) `RATCHET ROLE_BRIEF_BYTES_MAX` lines before/after: NOT RUN (`test_brief_pack.py` slow, canon). Expected equal on the seed (no row, no line).
- DOC-DISPATCH witness for the prose (config-keys row, manual-evidence.md): the Grep of the verbatim keys was not run separately; the file
  content is in the diff (`180 s, or the stand's\n  measured page load + 30 s when that is longer` wraps over a line in manual-evidence.md).
  No negative-control script was produced (context cap): the Lead to run or accept.

Not done: tests in the `Not written` list (by card); `test_gate_registry.py`/`test_judgment_census.py` (canon): the census row
`check_stand_page_load` was added; a ceiling move, if the canon shows one, is a named raise.
