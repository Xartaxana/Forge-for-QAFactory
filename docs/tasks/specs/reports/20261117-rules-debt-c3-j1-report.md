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


---

# Round 2 (fresh worker, t-1206): the owner's correction D1-D4, DoD (2) (3), siblings

Status: the questions of the first section are ANSWERED by the Lead decisions D1-D4, now implemented. Items 1-7 are the first worker's.

## What was done

- `project_knowledge.py`: constants `PAGE_LOAD_REASON_KEYS`, `PAGE_LOAD_FAILED_KEYS`, `PAGE_LOAD_CAUSES` (closed: factory, no_browser, unreachable,
  outside_hosts, credentials_in_address), `PAGE_LOAD_ATTEMPTS_MAX = 2`, `PAGE_LOAD_WHY_MAX = 200`; `_page_load_value_faults` takes a reason
  element (`failed` in value) and `_page_load_failed_faults` (cause closed, why one line <= 200, at a moment, attempts an int >= 1, not bool);
  `page_load` says `state: failed` + `failed: {...}` (new key, None otherwise) when the kept reason fits the stand definition and address (no age
  limit; only another identity or a revoke ends it); `record` replaces a held reason IN PLACE (same id) whatever replaces it (same cause with new
  attempts/at, another cause, the number); a number is still appended as before.
- `gate_preflight.py`: `check_stand_page_load` (a kept reason with attempts >= 2: no attempt, ONE note state `failed_kept` with cause/why/attempts/at/
  address/door as machine fields = the existing seam, the gate note the conductor reads, AR-17; otherwise measures), `_page_load_failed` records the
  reason (same cause as kept -> attempts+1, else 1), helpers `_kept_page_load`, `_page_load_identity`, `_page_load_reason_words`,
  `_page_load_kept_text`; `check_s5_stand_limits` appends the kept sentence + `kept_*` machine fields to its `unmeasured` note (the ONE card, D3).
  No brief line added (ratchets equal, below).
- `references/config-keys.json` (note of `environments.page_load`), `changelog.d/rules-debt-c3-j1-stand-page-load.md`.
- Tests (rows, no new file): `test_gate_preflight.py` (the failed-measurement function now asserts the reason row, no number, attempts 1, per cause;
  new `test_c3_j1_a_kept_reason_gets_one_more_try...`: attempts 1->2 in place, third start no attempt + seam fields + e2e card, revoke retry,
  another cause -> attempts 1, success replaces reason, changed address fresh; `_PageLoadFake` callable may answer None = default measurement),
  `test_project_knowledge.py` (`test_page_load_kept_reason_shape` 22-row table, `..._reads_replaces_in_place_and_is_never_a_pass`,
  `..._a_broken_kept_reason_in_the_file_is_read_as_broken...`).

## Decisions made by me within the Lead decisions ("reshila sama")

- The reason value also carries `definition_sha` and `address` beside `failed` (the card's "under the same identity as the number"): without them
  the reader could not tell "identity changed -> fresh". Address is the safe URL (no credentials).
- A reason is kept only when the identity can be read; else the note says "could not be kept" and the next rehearsal tries again.
- A broken reason in the file (attempts 0/negative/wrong type, unknown cause, missing field) reads as `none` with why `malformed` (same as a broken
  number: the default limit, a fresh attempt, never `measured`/`failed`); `record` REFUSES it with "nothing was recorded". If the Lead wants a broken
  reason to STOP the tries (state unreadable), it is a one-line change in `page_load`.
- The person's word to retry = the existing `project_knowledge.py revoke` of the row (named in the machine field `door`, not in the person's text, FR-6).
- The default test stub (`no_browser`) now leaves a reason row in other gate tests' registries: the slice and the 42-file run are green; the slow
  `test_gate_preflight.py` whole is the canon's.

## Witness (one run after all edits; an earlier attempt with a wrong slow filter was killed and re-run)

- `python -B <scratchpad>/runlist.py <walk.txt>` (walk.txt = output of `scenario_walk.py --witness-for <the 14 owns>`; runs every printed non-slow file):
  `RUN 42 SKIP-SLOW 35 ... BAD 0` and 42 lines `OK <file> | <tail>` (e.g. `test_first_look: 450/450 ok`, `test_manual_evidence: 262/262 ok`,
  `test_gate_vocabulary: 141/141 ok`, `test_human_questions: 651/651 ok`, `test_walk_session: 102/102 ok`, `test_project_knowledge.py | 200 passed`).
- My new rows by name, slow files: `run_pl2.py` (calls every `test_c3_j1_*` of test_gate_preflight.py): `grep -c "^FAIL"` -> `0`, ends `slice done`.
  `python -m pytest test_project_knowledge.py -q` -> `200 passed`.
- DoD (2) Grep (case-insensitive) `PAGE_LOAD_KEY|environments\.page_load` over `scripts/`, non-test hits: `gate_preflight.py:3285` and `:3373` (both
  `PK.record`; the first in `check_stand_page_load`, the second in its helper `_page_load_failed`: ONE check, two record calls, number and reason),
  the rest in `project_knowledge.py` (constants, reader, `record_problems`, `record`'s in-place rule). No other writer or reader.
  Positive control: the same call finds the `project_knowledge.py` lines. (The glob exclusion of tests/ did not apply in the Grep tool; the
  test hits were filtered by reading the paths.)
- DoD (3) ratchet lines, `role_brief_ratchet()` run in this worktree (AFTER) and in the main checkout (BEFORE, no j1):
  `RATCHET ROLE_BRIEF_BYTES_MAX qa-automator 6855`, `qa-code-critic 7177`, `qa-failure-analyst 6435` in BOTH; `RATCHET S5_PLAN_BRIEF_BYTES_MAX 9547`
  in BOTH (`test_brief_pack_s5_plan.py`). Equal, no raise.
- Slow files named, judged by the batch canon whole: `test_gate_preflight.py`, `test_brief_pack.py`, `test_judgment_census.py`, `test_gate_registry.py`
  and the 34 other slow-listed files of the walk.

## Siblings (axis 5 prose twins, axis 34 one road)

Grep (case-insensitive) over package `*.md` for `stand limit|page_object|e2e stand|stand_limit`: 2 hits; positive control: same call finds both.
- `design/factory-rules-debt.md:111` (`s5_stand_limits` FR-59 debt line): n/a, a non-goal (its line moves by S1b, RD1-23).
- `changelog.d/rules-debt-c3-j1-stand-page-load.md:5` (`skip_stand_limits` sentence): applied, extended with the kept-reason sentence.
Grep `page load|page-load|180 s|measured limit` over package `*.md`: `CHANGELOG.md:1148` history (n/a); `design/state-exits.md:26` (a liveness 180 s: n/a);
`references/controller-api.md:32` (`never_started_after_s` 180 s: n/a); `references/manual-evidence.md:56-57` (the 180 s + load sentence: unchanged, still true);
`design/factory-rules-debt.md:111` (n/a, above). No `s4.md`/`s5.md`/agent charter hit.
Axis 34 (one road): the reason is read only through `PK.page_load`, written only through `PK.record`; the card reads it through `_kept_page_load` -> `PK.page_load`.

## Same-class sightings (rule 5)

- The reporter's `timed_out` card (card fork F-j-reporter) is unchanged (j2's).
- `check_s5_stand_limits` other states (`unreadable`, `incomplete`) do not carry the kept reason: they concern the config's own recorded limit, not this measurement.
