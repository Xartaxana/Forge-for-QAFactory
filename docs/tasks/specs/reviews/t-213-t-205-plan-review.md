# t-213 — critic on the PLAN: t-205 (HF8-4, onboarding-forge/2), 11 builder parts

Reviewed: `docs/tasks/specs/t-205-hf8-4-parts.md` (designer t-205), against main `539361a`
(`ai-packages/qa-factory/`), the finding `plans/piles/onboarding-forge/findings/20261026-hf2-0-posle-reliza-dolg-kachestva.md`,
and the in-flight worktrees/branches under `.claude/worktrees/`.

**Verdict: GO WITH FIXES** (schema: `fit_with_fixes`). Two findings block one part each: B1 blocks P6 and B2 blocks P9.
The other parts can go once the small spec edits below are made. The decision to accept the plan and dispatch it belongs
to the Lead (rule 6). This verdict is an input to that decision.

---

## 1. Facts (key 1): spot-checks per part against main

| part | claim | checked on main | result |
|---|---|---|---|
| §2 item 1 | 14 spellings in 12 files | `grep -nE "[\"']contradicts_requirement[\"']" scripts/*.py` | **14 hits in 12 files, exact list confirmed** (acceptance:748, check_delivery:2003, check_traceability:67, contract:83/2576/5335, controller:237, driver_stage_s7:44, gate_brief:4478, s5_precheck:110, s7_pretriage:58, stage_status:181, story_step:1614, traceability:931) |
| P1 | `PENDING_IMPLEMENTATION` :82, `UNRESOLVED_REASONS` :83, `_red_thens_of` :2576, `PROBE_NOT_APPLICABLE_REASON` :5335 | read contract.py:80-84, 2570-2578, 5333-5336 | confirmed |
| P1 | `red_by_requirement` closure :896-925 / loop :939-959 | read acceptance.py:884-967 | confirmed. The split can be done as written |
| P1 | alias importers of `acceptance.CONTRADICTS_REQUIREMENT` | grep `CONTRADICTS_REQUIREMENT` over scripts | confirmed: controller:7330, window_record:75, manifest_put:410, ledger:751, manifest_from_tests:954, test_red_window:382 |
| P2 | `CONTRADICTS_WORD` :237, `names_contradicts` :515/529, `_s5_gap_problems` imports at :7330 in the same method (def :7328), K1 :381-382 | read | confirmed. No module-level `import contract` in controller (the import list :30-49). Lazy `import contract` exists at :1543, :9195, :9350 |
| P3 | `s5_precheck.CONTRADICTS` :110; outside readers `test_ahead_cards.py:63,247`, `test_s5_precheck.py` | grep | confirmed. `dispatch_scope` :450-466 has no running-count logic. The docstring claim is at :3793 |
| P3 | `s7_pretriage.CONTRADICTS` has no outside reader | own grep `\b(S7\|S\|P\|s7_pretriage)\.CONTRADICTS\b` over every importer of s7_pretriage | 0 hits. Positive control: the same pattern gives 5 hits in test_s5_precheck.py |
| P3 | `stage_status.RED_ON_PURPOSE` :181, used :190, :308-309 | read | confirmed. `--selftest` **exists** (stage_status.py:403) |
| P4 | `driver_stage_s7.py:44` with `import contract` at :27 in the same method; `story_step.py:1614`; `gate_brief.py:4478` | read | confirmed |
| P5 | the three sites import `contract as C` at load | grep | confirmed (check_traceability:32, check_delivery:48, traceability:36) |
| P6 | `_case_picture` :1596-1597 raises on hand-sent rows kept by `_merge_bindings` | read manifest_from_tests.py:1520-1600, 636-645, `_blocked_rows` | **FALSE**, see B1 |
| P6 | `ledger.plan_row_state` :866-868 skips `"2"` | read ledger.py:858-872. manifest_put accepts hand rows and reads them through `then_number` (manifest_put.py:1461-1472) | confirmed. A hand-sent `"then": "2"` can reach the ledger |
| P7 | `SETTLED_STATUSES` at planning_contract:1527, used :2711/:2771 (QR at :2663 in the same function `_apply_gate_answers`, def :2661) and :3499 (QR :3497) | grep + read :3496-3591 | confirmed. No outside reader of `planning_contract.SETTLED_STATUSES` (own grep, 0 hits). The only other copy is question_register:85 |
| P8 | same f-string at driver_stage_build:102-103 and driver_stage_s6:603-604. story_run.py holds none | grep | confirmed (story_run: 0 hits for `stand not confirmed\|STAND_NOT_CONFIRMED\|is not confirmed as usable`. Positive control: waiver.py:372 and the 2 driver sites hit) |
| P9 | four own readings in validate_artifacts :1170/:1255/:1408/:1972. `APPENDIX_HEADING` :4751 after literal :81. grammar:105 | read | confirmed. **But** the sweep (F6) misses sites, see B2 |
| P10 | bare `os.replace` at execution_request:411, :3869. `event_store.replace_file` :177-190, stdlib-only imports | read | confirmed. `_probe_cwd` unification is safe: `registered_probe` always sets `cwd` (`str(spec.get("cwd") or ".")`, execution_request.py:2498) |
| P11 | automator's inject list has no rubric (inject-map.json:59-67). Critic has it. The automator's slice and the critic's slice both carry "A commented-out Then: rubric dimension 8." (:68) | read | confirmed. role-load: automator 20,181 / process 18,614, critic 19,389 / 17,566, and **each row equals the measured load** (`role_load.py --all`) |
| §2 item 8 | qa-code-critic half already fixed | `grep -n "<!--" agents/qa-code-critic.md` and case-insensitive `wave 2` over `agents/` | **confirmed fixed**: only `kind:`/`gen:` markers (:12,17,27,42,64,81,83,86), 0 `wave 2` hits in agents/. The finding's :14 names exactly that comment |

Small stale facts (not blocking, builders go by symbol): census rows are 188/826/918 on main, not 186/824/916. The
`os.replace(` count is 45 occurrences in 35 non-test package .py files, counting event_store's survivor and docstring.
After P10 that leaves 41 bare sites in 33 files, not "42". The new F3 finding recounts.

---

## 2. Findings

### B1 — BLOCKS P6: the `_case_picture` defect does not exist, and the DoD row cannot go red
- Carrier: `manifest_from_tests.py:1531-1549`. `_case_picture(story, cases_named, bindings, ...)` gets **`bindings`**, the
  rows the markers wrote. It does not get the list `_merge_bindings` returns, which only goes into `fragment["then_bindings"]`.
  Every row in `bindings` takes its `then` from `_then_numbers` (:636-645). That function refuses anything that is not
  an int >= 1, through `_blocked_rows` too. The only thing that appends to `bindings` is markers (:1143, :1242, :1273,
  :1338, own awk over 1125-1551).
- Failure scenario: the spec's K5 table row (a hand-sent `then` of `"2"`, `[4]`, `"x"`, `True`) never reaches
  `_case_picture`. So (i) the build does not raise on the PRE-change code either, and the DoD clause "the two new rows
  fail on the pre-change code" cannot be met. (ii) The expectation "for `"2"` the picture lists Then 2 under
  `unresolved`" is false AFTER the change too. A Sonnet builder will be stuck or will bend the test.
- Fix: P6 drops the manifest_from_tests test row. Change 1 (`_case_picture` through `then_number`) may stay as a
  behaviour-free AR-13 alignment, stated as such, or be dropped. Change 2 (the docstring) stays. §2 item 3 is restated:
  the manifest site is not live, and only the ledger site is a defect. The ledger row stays.

### B2 — BLOCKS P9: the F6 sweep is incomplete, and a second section reader is unnamed
- Sweep of the same artifact (rule 9), headings spelled as literals inside P9's own three files, and beside them:
  `report_facts.py:4350` (`heading.startswith("## Left with you")`, a third site the spec does not list), :4485, :4720;
  `validate_artifacts.py:1314` (`"## Left with you"`), :1356 (`"## Proven"`), :1420 (`REPORT_HUMAN_HEADING = "## Factory
  defects"`, a second constant), :1549 (`"## Decided at gate B"`); `traceability.py:1625` `LEFT_HEADING`, :1627
  `GATE_B_BEFORE` (outside P9: owned by P5 and touched now by OF4-27).
- Same surface, a second READER: `validate_artifacts._report_section_body` (:1200) reads "the lines under a heading up
  to the next `## `" without fences or block markers. `report_facts._section_span` (:4324) reads the same section with
  fences and markers. That is an AR-13 twin on the same report text, and P9 moves only the appendix readings onto the
  survivor.
- Failure scenario: P9 as written leaves `## Left with you` with four spellings in its own files, while F6 says "about 6
  lines, same three files". Rule 9 says siblings are fixed now or queued explicitly. F6(a) as written does neither for
  the sites above.
- Fix (pick one, Lead): (a') P9 takes grammar constants for every report heading that its three files spell (sites
  enumerated above). `traceability.py:1625/1627` go to P5 (after OF4-27), and the `_report_section_body` /
  `_section_span` unification becomes a NEW finding, because moving that reader changes fence and marker behaviour on
  4 checks. (b) P9 = the appendix only, and every heading site above, plus the reader twin, goes into one new finding.
  I recommend (a'): the constants are behaviour-free, and the reader is not.

### M3 — P9 states a behaviour change but has no row, one edge has no direction, and one call names the wrong variable
- `is_legacy_report` (:1170). Today `"## Appendix" not in text` is a substring test. After the change it is
  `appendix_span is None` (a heading line outside fences). A report with `## Check coverage` that mentions `## Appendix`
  only mid-line or in a fence flips from the current contract to the legacy one (:1141-1146, :1223-1227: other
  checks). The spec's "can only refuse more" covers `check_report_forbidden` and the budget, not this edge. Fix: state
  the edge and its direction. I recommend keeping the current contract, i.e. legacy only when NO `## Appendix`
  substring exists, which keeps this site as it is. Or accept the flip by name.
- Prose budget (:1966-1973): the cut is computed on `authored` (blocks and summary removed), not on `text`. The spec
  writes `RF.appendix_span(text)` / `text[:span[0]]`. Offsets from `text` applied to `authored` would cut the wrong place.
  Fix: write `authored`.
- The change replaces a substring reading with a section reading. That is a defect fix (FR-59 side), so per
  docs/TESTING.md it gets ONE parameterised variant row in a keep file (`test_validators.py` or `test_report_facts.py`):
  a fenced or mid-line `## Appendix` no longer hides the body from the forbidden-id check. §3 "no new rows" for P9 is
  changed accordingly.

### M4 — P11: the ratchet move is under-specified (process slack is 0, and the critic can grow)
- `role_load.process_ratchet_problems` (:259-281): a process row above OR below the measured load is red (slack 0).
  Both roles' rows equal the measured load today. Moving the list into `artifact-contract-automation.md` grows the
  automator's slice and the critic's slice by the same amount, while the critic's rubric shrinks by a shorter
  replacement. **The critic's net can be positive.** The spec covers only "lower qa-code-critic if it shrank".
- Fix: "Set each of `ratchet_tokens` and `process_ratchet_tokens` for qa-automator and qa-code-critic to the value
  `role_load.py --all` measures after the edit. Name every moved row (key, old -> new, reason) in the commit and in the
  diff critic's verdict (axis 18, brief q.9). If either role grows by more than 200 tokens, stop and return the numbers."

### M5 — zones: the frozen HF8-4 cell does not name 13 of the written files, and two active batches overlap
- `batch-2-onboarding-roles-forge-p3.md:60`, HF8-4 «Пишет в». The batch is taken, so the cell is frozen (PROJECT.md
  «Командная работа» p.2). The cell does NOT list: s7_pretriage.py, stage_status.py, driver_stage_s7.py, gate_brief.py,
  check_traceability.py, check_delivery.py, traceability.py, waiver.py, driver_stage_build.py, driver_stage_s6.py,
  grammar.py, references/artifact-contract-automation.md, code-review-rubric.md, references/slices/, design/role-rules.json,
  references/role-load.json. `piles.py check (б)` cannot see overlaps on these files.
- Live overlaps, own check (merge-base diff plus worktree status per worktree):
  - **contract.py**: onboarding-forge/4 (taken 12.11, file on `wip/of-batch4`, not yet on main) OF4-25 cell =
    `scripts/contract.py` (registry_sides :5711). P1 edits :80-84, :2576, :5335, which is textually disjoint. But
    P1 changes MODULE CONSTANTS, which the D-0048 `функции:` door cannot name (it reads defs only, `tools/piles.py`
    `_item_verdict`). The door is an `очередь:` line in BOTH preambles (appendable in a taken batch), or
    `piles-skip: б` with a reason.
  - **traceability.py**: OF4-27 has an uncommitted edit in `resolve` (:1831-1840). P5's site is :931
    (`unconfirmed_basis` region), which is disjoint. P5 is wave 2 and merges main after OF4-27.
  - **gate_brief.py**: onboarding-hooks/4 has an unmerged commit `ca9cdf2` (`carried_concern_cases` :2243). The line
    `очередь: onboarding-hooks/4 -> onboarding-forge/2` already exists in batch-2, so P4 merges after it.
- Not in the dispatcher's list, found by my scan: `worktree-agent-a02faf...` (FV1-1, locked, commits 19:56 today)
  edits contract.py (`case_levels` ~:2096, `CASE_REQ_LINE_RE` ~:3050) and s5_precheck.py (`UNCHECKED_CHECKS` :76-79).
  These are disjoint from P1/P3 by lines. `oh3-9` edits role-rules.json in other rows (disjoint from :74).
  `fix/ci-main` and `conv/accepted-nodes` edit `judgment-census.json`: any part that adds a census row will conflict
  textually there. `agent-a365d2...` has uncommitted edits to gate_brief.py, external_writes.py (also RC1-10's) and
  judgment-census.json on a 14:07 base. It may be stale; the Lead should check.
- Named running work, checked: OH5-7 (check_coverage, onboard_apply), OH3-6 (qa-doctor SKILL.md, evals.json), RC1-10
  (role_cli, critic_rollcall, manual_evidence, plan_row, external_writes, role-commands.json; artifact_producer has no
  diff yet), DC1-10 (factory_dashboard): **none of them is in any part's owns.**
- Fix: write the extra files into batch-2's «Ход» (a writable section), add the `очередь:` lines for contract.py
  between onboarding-forge/4 and /2, and name the census-file conflict to the integrator. The Lead decides.

### m6 — P7 DoD names three keep files that the witness does not print
- I ran `scenario_walk.py --witness-for ai-packages/qa-factory/scripts/planning_contract.py`: exit 0, 34 keep lines.
  None of `test_question_register.py`, `test_gate_preflight_question_status.py`, `test_question_branches.py` is among
  them. Fix: drop the "expect" clause. The witness is what the command prints (builder-rules 7b).

### m7 — P3 DoD hedges on a flag that exists
- `stage_status.py:403` defines `--selftest`. Fix: make `python -B .../stage_status.py --selftest` a definite part of
  the DoD.

### m8 — SIBLING_MAP axis 26 lists stale sites, and P8 moves the builder of the block text
- `docs/SIBLING_MAP.md` axis 26 still names `story_run.py :8718/:10139`. The sites now live in the driver mixins, and
  after P8 the text has one builder, `waiver.stand_block`. Fix: update axis 26 in the same move ("a new symmetry is a
  new axis in the map, same commit", CLAUDE.md rule 9). This is a docs file outside the package, so the Lead does it
  or P8's owns get `docs/SIBLING_MAP.md`.

### m9 — a known reader twin is left out without being queued
- `driver_stage_s7.py:44` and `s7_pretriage.py:129` both read "the word anywhere in `json.dumps(entry)`". s7_pretriage's
  docstring says it reads "as the driver finds it". P3/P4 make these two readers non-goals for the reading and change
  only the spelling. That is right for HF8-4, but rule 9 forbids leaving a known sibling silently. Fix: name them in
  the F7 finding (one reader for "a manifest row carries the red word").

### m10 — carriers for the new findings
- F3 says "onboarding-forge/findings/ (or package-ci)". F5, F6-rest and F7 open findings too. D-0044: in the same
  move, each lands as a node line in an UNtaken batch of its pile. Fix: name one pile for each. The six grown functions
  of F4 take `перенос:` lines with a human's confirmation (the spec says so, which is correct).

---

## 3. Forks: verdict per fork

- **F1 (all 14 spellings): agree, (a).** This is the class fix (rule 9, P31 / axis 34, AR-15), not scope creep. All 14
  sites spell the same closed word of `contract.UNRESOLVED_REASONS`, and the values are unchanged. The data-file
  spellings (`handoffs/vocabulary.yaml:65,107`, `references/*.json`) are AR-1 data, pinned to the tuple by
  `test_handoff.py:90`, so they rightly stay out. A code constant for one branched-on word is not closed variety moved
  into code. The one cost (the extra files in a frozen cell) is M5.
- **F2 (sanctioned paths through the contract slice, raise named): agree, (d), with the M4 edit.** The raise is
  justified. The automator is told today to follow "rubric dimension 8" (`agents/qa-automator.md:72`, its contract
  slice :68), but no rubric is in its inject list (`inject-map.json:59-67`). That is an FR-38 / AR-10 defect, and only
  a carrier change fixes it. (d) keeps one home (AR-13/15) at about +100 tokens. Per AR-20 and axis 18 the raise is
  named row by row in the DIFF critic's verdict with the measured numbers. This plan verdict names the expected
  rows: `ratchet_tokens.qa-automator` 20181 -> measured, `process_ratchet_tokens.qa-automator` 18614 -> measured, and
  both qa-code-critic rows -> measured, either direction. The owner's word is not needed: the role-load note makes a
  ratchet raise a verdict-named act. `threshold_confirmed_by` concerns the threshold, not the ratchet.
- **F3 (event_store.replace_file in P10, new finding for the rest): agree, (a).** The survivor exists and imports only
  the stdlib. Option (b), a retry in the test, would hide a race in product code that a Windows host can hit. The
  finding carries the recount (41 sites / 33 files after P10) and one pile (m10).
- **F4 (split the 4 new ones, queue 6): agree, (a).** Each helper is named, its error direction is stated, and keep
  rows judge it (`test_red_window`, `test_s5_precheck`, `test_execution_request`). The six grown ones are gate paths
  and need their own design read.
- **F5 (scout first): agree.** The validator-vs-reader classification of the 10 `isinstance(then, int)` sites is
  unknown, and guessing it would be a design decision.
- **F6: disagree with (a) as written.** It is incomplete (B2). Take (a') or (b).
- **F7 (new finding, P2 stays one word): agree.** Add the m9 reader twin to it.

---

## 4. Executability (key 4) and AR / class (key 5)

- A Sonnet builder can execute P1, P2, P3, P4, P5, P7, P8 and P10 as written: the symbol, the helper signatures, the
  order invariants and the witness command are all named. P6 can be executed after B1, P9 after B2 and M3, and P11
  after M4. Edges: every part names its edges, and the missing ones are the M3 legacy edge and the M4 critic-growth
  edge. Test rows: no new file anywhere. Rows go into keep files only (test_ledger, test_red_window K1 removal), plus
  the M3 row. I confirmed that test_ledger, test_manifest_from_tests and test_red_window are not quarantined, and that
  test_contract is (test-layers.json).
- AR-n per part: §1 names them, and each part's line repeats them (AR-13/15 for P1-P5 and P7-P10, AR-14 for P9, AR-28
  for P6, AR-10/11/20 for P11). Census: the splits may move a refusal into a helper. The spec's rule (add a row with
  the parent's class, never raise a ceiling, ask the Lead otherwise) is correct (AR-20, AR-29).
- SIBLING_MAP axes walked: axis 5 (stage twins: the red word read by S5 precheck, S7 pretriage and the driver; covered
  by F1 parts plus m9); axis 18 (ratchets: role-load, census; covered by M4 and §1); axis 26 (stand block word: covered
  by P8 plus m8); axis 32 (judgment: no check changes class, P11 is judgment accepted by the code critic, correct);
  axis 34 (one road: see below). No other axis is touched by these files.
- DUPLICATION AND CONSISTENCY (q.6): the plan removes duplicates: one word, one status tuple, one stand text, one
  heading, one reader, one replace. The residual is B2 (headings and the reader twin) and m9.
- CODE QUALITY (q.7): the helper shapes are sound. `_probe_cwd` merges two copies safely (verified above). The
  `_reopened` signature passes 7 arguments plus mutation of `lines`, which is acceptable for a behaviour-free split.
- ONE ROAD (q.12, rule 19): none found. Grepped: the axis-34 detector pattern
  `non-goals?.*(python|typescript|java|c#|csharp|pytest|язык)` over t-205 gave 0 hits (positive control: 2 hits in
  t-1968-mutation-probe-marker-and-critic.md). No non-goal excludes a language, project or case from a shared
  mechanism.

---

## 5. Parts safe to start now, in parallel with the named work

- **Start now:** **P7** (planning_contract.py), **P8** (waiver, driver_stage_build, driver_stage_s6), **P10**
  (execution_request.py). None of these files is in any in-flight diff (own scan of all worktrees).
- **Start after the M4 edit:** **P11**. role-rules.json is also touched by oh3-9 in other rows, which merges cleanly.
- **Start after the M5 queue line is recorded:** **P1**. contract.py is disjoint by lines from OF4-25 and FV1-1.
- **Hold:** **P9** until B2 and M3 are fixed. **P6** until B1 is fixed (wave 2 anyway).
- **Wave 2 after P1 merges:** P2, P3, P4 (after onboarding-hooks/4, per the existing queue line), P5 (after OF4-27,
  traceability.py), P6.

## 6. Minimal spec edits

1. P6: delete the `test_manifest_from_tests.py` row and its DoD clause. Mark change 1 as behaviour-free AR-13
   alignment (or drop it). Restate §2 item 3 so only the ledger site is live (B1).
2. P9 / F6: replace F6(a) with (a') and the enumerated sites, move `traceability.py:1625/1627` to P5, and open a new
   finding for `_report_section_body` vs `_section_span` (B2).
3. P9: state the `is_legacy_report` edge and its direction, write `authored` in the budget cut, and add one
   parameterised row in a keep file (M3).
4. P11 step 5: "set each of the 4 rows to the measured value, either direction, each named row by row; more than 200
   tokens of growth for either role -> stop" (M4).
5. §3 / P1: add a note that the extra files go into batch-2 «Ход», and an `очередь:` line for contract.py between
   onboarding-forge/4 and /2 (M5).
6. P7 DoD: drop the "expect" list (m6). P3 DoD: `--selftest` definite (m7).
7. P8: add axis 26 of `docs/SIBLING_MAP.md` to the move, through the Lead or P8's owns (m8). F7: add the
   `driver_stage_s7:44` / `s7_pretriage:129` reader twin (m9). F3/F5/F6/F7: name one pile each (m10).

---

## Trail

Read: t-205 spec (whole); the finding (grep of items); contract.py:80-84, 224-246, 2570-2578, 5333-5336;
acceptance.py:738-748, 884-967; controller.py:30-49, 225-238, 515-530, lazy-import lines; test_red_window.py:376-396;
s5_precheck.py:105-112, 448-468, 1419-1495, 3780-3796; stage_status.py:178-192, 300-312; driver_stage_s7.py:20-46;
s7_pretriage.py:125-131; manifest_from_tests.py:636-646, 946-956, 1232-1340, 1520-1600; ledger.py:858-872;
manifest_put.py:1275-1295, 1461-1472; planning_contract.py:1527, 2661-2771 (grep), 3496-3591; question_register.py:83-87;
waiver.py:368-381; driver_stage_build.py:98-106; driver_stage_s6.py:598-607; report_facts.py:78-83, 4307-4338,
4748-4760; validate_artifacts.py:1136-1146, 1163-1228, 1200-1212, 1250-1262, 1404-1412, 1966-1976; traceability.py:1622-1628;
execution_request.py:1-21, 2486-2500, 2786-2866; event_store.py:175-192 and imports; references/inject-map.json:55-75;
references/role-load.json:1-35; design/role-rules.json:72-75; code-review-rubric.md:60-80; artifact-contract-automation.md:66-72;
agents/qa-automator.md:70-74; agents/qa-code-critic.md HTML comments; role_load.py:259-281; judgment-census.json (grep);
docs/SIBLING_MAP.md axes 5, 18, 26, 34 and the axis list; docs/tasks/critic-diff-brief.md q.9-12; tools/piles.py:1525-1600;
batch-2 HF8-4 row and preamble; batch-4 (wip/of-batch4) OF4-25/27 rows.

Greps (each negative with a positive control): the literal over scripts/*.py (14 hits); the word over package .py/json/yaml;
alias names `RED_ON_PURPOSE|CONTRADICTS_WORD|.CONTRADICTS|PROBE_NOT_APPLICABLE_REASON`; s7_pretriage.CONTRADICTS
(0, control 5 in test_s5_precheck); `os.replace(` counts; the settled tuple; report heading literals; `dimension 8`;
`wave 2` (0 in agents/, control CHANGELOG); `stand not confirmed` sites; axis-34 detector pattern (0, control 2).

Reruns: `scenario_walk.py --witness-for .../planning_contract.py` (exit 0, 34 keep lines, none of the three P7 names);
`--witness-for .../contract.py` (76 keep lines); `role_load.py --all` (automator 20,181/18,614, critic 19,389/17,566,
ratchet = measured); a per-worktree overlap scan (merge-base diff plus untracked) over all `.claude/worktrees/*`.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "B1 (blocks P6): _case_picture receives marker-made bindings (manifest_from_tests.py:1531-1549; then from _then_numbers :636-645), so hand-sent rows never reach it; the K5 test row cannot fail on pre-change code and its '2 under unresolved' expectation is false after the change",
    "B2 (blocks P9): F6 sweep incomplete - heading literals at report_facts.py:4350, validate_artifacts.py:1314/1356/1420/1549, traceability.py:1625/1627 unlisted; second section reader validate_artifacts._report_section_body (:1200) unnamed (AR-13 twin of report_facts._section_span)"
  ],
  "fixes": [
    "P6: drop the test_manifest_from_tests row and its DoD clause; mark _case_picture change as behaviour-free AR-13 alignment or drop; item 3 live only at ledger",
    "P9/F6: take (a') heading constants for every site in the three files, move traceability.py:1625/1627 to P5, new finding for the _report_section_body vs _section_span reader",
    "P9: state the is_legacy_report edge and direction; use authored (not text) in the prose-budget cut; one parameterised row in a keep file",
    "P11 step 5: set all four role-load rows (automator, critic; ratchet and process) to the measured value either direction, each named row by row; over 200 tokens growth for either role stops",
    "M5: write the extra files into batch-2 Hod; add an ochered line for contract.py between onboarding-forge/4 and /2 (module constants cannot use the funktsii door); tell the integrator about judgment-census.json conflicts with fix/ci-main",
    "P7 DoD: drop the expect list (witness prints none of the three); P3 DoD: stage_status --selftest exists, make it definite",
    "SIBLING_MAP axis 26 updated with P8 (stale story_run sites, new builder waiver.stand_block); F7 includes the driver_stage_s7:44 / s7_pretriage:129 reader twin; F3/F5/F6/F7 each name one pile"
  ],
  "class_completeness": "Item 1 class: all 14 code spellings covered by P1-P5 (own grep confirms the list); data-file spellings are AR-1 data pinned by test_handoff.py:90. Gaps: report headings and the second section reader (B2), the substring reader twin driver_stage_s7/s7_pretriage (m9, into F7), os.replace class queued by F3 (recount 41/33), Then-number readers queued to a scout (F5), controller gap words queued (F7). Axes walked: 5, 18, 26 (stale row, m8), 32, 34 (none found).",
  "trail": {
    "read": [
      "docs/tasks/specs/t-205-hf8-4-parts.md",
      "ai-packages/qa-factory/scripts/contract.py",
      "ai-packages/qa-factory/scripts/acceptance.py",
      "ai-packages/qa-factory/scripts/controller.py",
      "ai-packages/qa-factory/scripts/tests/test_red_window.py",
      "ai-packages/qa-factory/scripts/s5_precheck.py",
      "ai-packages/qa-factory/scripts/stage_status.py",
      "ai-packages/qa-factory/scripts/s7_pretriage.py",
      "ai-packages/qa-factory/scripts/driver_stage_s7.py",
      "ai-packages/qa-factory/scripts/manifest_from_tests.py",
      "ai-packages/qa-factory/scripts/ledger.py",
      "ai-packages/qa-factory/scripts/manifest_put.py",
      "ai-packages/qa-factory/scripts/planning_contract.py",
      "ai-packages/qa-factory/scripts/question_register.py",
      "ai-packages/qa-factory/scripts/waiver.py",
      "ai-packages/qa-factory/scripts/driver_stage_build.py",
      "ai-packages/qa-factory/scripts/driver_stage_s6.py",
      "ai-packages/qa-factory/scripts/report_facts.py",
      "ai-packages/qa-factory/scripts/validate_artifacts.py",
      "ai-packages/qa-factory/scripts/traceability.py",
      "ai-packages/qa-factory/scripts/execution_request.py",
      "ai-packages/qa-factory/scripts/event_store.py",
      "ai-packages/qa-factory/scripts/role_load.py",
      "ai-packages/qa-factory/references/inject-map.json",
      "ai-packages/qa-factory/references/role-load.json",
      "ai-packages/qa-factory/references/code-review-rubric.md",
      "ai-packages/qa-factory/references/artifact-contract-automation.md",
      "ai-packages/qa-factory/design/role-rules.json",
      "ai-packages/qa-factory/agents/qa-automator.md",
      "ai-packages/qa-factory/agents/qa-code-critic.md",
      "ai-packages/qa-factory/scripts/tests/fixtures/judgment-census.json",
      "docs/SIBLING_MAP.md",
      "docs/tasks/critic-diff-brief.md",
      "tools/piles.py",
      "plans/piles/onboarding-forge/batch-2-onboarding-roles-forge-p3.md",
      "wip/of-batch4:plans/piles/onboarding-forge/batch-4-hvosty-onbordinga-i-forzha.md"
    ],
    "reruns": [
      {"command": "python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/planning_contract.py", "result": "exit 0, 34 keep lines; test_question_register/test_gate_preflight_question_status/test_question_branches absent"},
      {"command": "python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/contract.py", "result": "76 keep lines"},
      {"command": "python -B ai-packages/qa-factory/scripts/role_load.py --all", "result": "qa-automator 20,181 total / 18,614 process; qa-code-critic 19,389 / 17,566; ratchet equals measured"},
      {"command": "grep -nE literal contradicts_requirement over scripts/*.py", "result": "14 hits in 12 files, matches spec list"},
      {"command": "per-worktree git diff --name-only <merge-base> plus untracked, intersected with HF8-4 owns", "result": "overlaps: of4-27 traceability.py; agent-a02faf (FV1-1) contract.py, s5_precheck.py; onboarding-hooks/4 gate_brief.py; agent-a365d2 gate_brief.py, judgment-census.json; oh3-9 role-rules.json, judgment-census.json; fix/ci-main and conv/accepted-nodes judgment-census.json; none on P7/P8/P10 files"}
    ]
  }
}
```
