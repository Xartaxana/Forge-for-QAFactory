# T6 report (t-963) - `handoff_check.py` sites (wave A)

Worktree `C:\QAFactory\forge-repo\.claude\worktrees\agent-a10fec4f35cc3b5ed`, builder, Sonnet. One commit, not pushed. No refusal text, `refusal_text` block, `--json` answer
or exit code changed by one byte.

## What was done

- `handoff_check.py`: `from detector_verdict import refusal`; every problem builder of the 21 rows wraps its text: `Problem(path, refusal("handoff_check:<id>", <same expression>), ...)`.
  `Problem.text` is now a `Record` (a `str` subclass: `str(text)`, f-strings, `json.dumps`, `refusal_text`, `_answer_json` print what they printed). The `cli` prints in `main`
  are `print(refusal("handoff_check:cli", <same text>))` (a print of a Record is the bare text; no `spoken()`: the callers read the LAST stdout line as the reason).
- Siting only: no transport edited. `refusal_text`, `_answer_json`, `_answer_text`, `values_report` are untouched, so the expected/door of the Record is carried by the Problem but not yet
  printed (question 1). `_review_receipt`, `_plan_row_of`, the guard, `stage-joints.json`, `told_ratchet`, the K12 pin: not touched (F-1 (a)).
- Test: ONE new function `tbw_t6_sites` in `test_detector_verdict.py` (+ the `T6_OLD` table it reads, + one call in `main`).
- Changelog fragment `changelog.d/tbw-t6.md`.

## Site table (function | fragment | id or E6 reason (class) | test row | proof F fast / N not provoked)

| function | fragment | id | row (`tbw-t6 <key>`) | proof |
|---|---|---|---|---|
| `check` field loop | `not filled. <hint> One of: ...` | field.blank | `field.blank / fresh form, header.verdict` | F |
| `check` field loop | `` `x` is not a value of this field. Write one of: ...`` ; the open-list door (`'new: x' has no reason`) | field.value | `closed list, bogus word`, `row state bogus`, `open list, new: without a reason` | F (both sites) |
| `check` field loop | `N characters, at most M.` | field.max_len | `field.max_len / a reason of 90` | F |
| `check` | `no rows. One row per item in scope` | required_rows | `required_rows / fresh form, scope` | F |
| `check` | `no rows. The verdict V sends the window back` | required_rows.owed_by_verdict | `... / concerns owes findings` | F |
| `check` | `` `none` says ..., and `scope` lists N row(s)`` | required_rows.null_word | `... / window none beside a row` | F |
| `tried_errors` | `no rows and no tried_note` | tried | `tried / fresh S2 form` | F |
| `_blocked_row_problems` | `` `blocked` says something outside you stops this row`` | blocked_problem | `blocked_problem / a blocked row...` | F |
| `check_findings` | `names the factory's own tool` | findings_tooling | `findings_tooling / ...` | F |
| `_fill_claims` (x2), `_check_claims` | `code could not measure it` / `code measured this as false` / `the form claims this is true` | claims | three rows | F (verifiers faked in the row, restored) |
| `_null_outcome_view` | `... and it holds N repair verdict(s)` | null_outcome.repairs | `a TEST_BUG row` | F |
| `_null_outcome_view` | `a triage row has no verdict this check knows` | null_outcome.verdict | `a verdict nobody knows` | F |
| `_null_outcome_view` | `N triage row(s) name no instance` | null_outcome.names | `a row with no instance` | F |
| `_null_outcome_view` | `the run report ... cannot be read` / `shows no results list` | null_outcome.report | `no run report` | F |
| `_null_outcome_view` | `holds no row, and ... so a failure has no verdict` ; `N failure(s) ... have no row` (the same problem also names unnamed, ambiguous, multiple) | null_outcome.failures | three rows | F |
| `_null_outcome_view` | `N triage row(s) are not listed here` ; `X is listed here, and no row ...` | null_outcome.listing | two rows | F |
| `_binding_problems` | `holds rows that cannot be a verdict` (non-empty section) | binding | `binding / non-empty scope...` | F |
| `_investigation_view` (x2) | `must be a list` ; `an investigation hands nothing for repair` | investigation | two rows (view called directly) | F |
| `parse_values.bad` (every line problem, one closure) | `not valid JSON`, `not a path: value line`, `given twice`, `nested` | values_file | five rows | F |
| `_apply_one.refuse` (every apply problem, one closure) incl. `_open_rows_for`'s `why` | `not a field`, `name the field of the row`, `contract-owned`, `one value, not a list`, `the next row is scope[1]` | values_apply | five rows | F |
| `_text_of` | `cannot be read as UTF-8 text` | values_apply | `_text_of, not UTF-8` | F |
| `main` (6 prints + the rename `Problem`) | `--shorten needs --fix`, `no such file`, `not UTF-8`, `does not name its contract`, `no contract X` (FileNotFoundError), `no such values file`; rename failure | cli | six rows (text + exit 2) | F (6 prints); N (rename failure: needs a failing `os.replace`) |

Proof is by text (sha256[:16] of the OLD file's text, `T6_OLD`), by `Record.check == <id>` and `expected == told_text(row)` for every Problem site, and by the scanner row:
`refusal_registry.sites` over `handoff_check.py` reads exactly the 21 ids and no other (E1). The `cli` prints are bare text (not a Record at the printer), so for them the proof is the text + the scanner.

## Left bare (E6), classed

- (role) `_null_outcome_view` `rows is None` (the triage file is missing / not JSON / not an object / no `triage` list, text `... - and <why>. The triage is written before this form`):
  no row of the 21 owns "the triage is readable" (`null_outcome.report` says the RUN REPORT is readable; the aggregator `handoff_check:null_outcome` does not exist as a row, and a literal
  of it would site every `null_outcome.*` row by the C14 sub-id rule). Queue to T1r-cards-R: a row `null_outcome.triage` (or widen `report`).
- (code) `refusal_text` / `values_report` build no problem of their own; no other `Problem(` or `print` refusal of `handoff_check.py` is left bare (every `Problem(` of the file is a site above).

## Rows that over-claim / mismatch (EC-8, for T1r-cards-R; no sentence edited)

- `handoff_check:null_outcome.failures` ("Each shown failure has a triage row") sits on ONE problem that also says ambiguous rows and several rows for one failure (the `binding` row's sentence)
  and unnamed failures: one Record cannot carry two ids; the body says more than the row. Same text via `_binding_texts` is `binding` on the non-empty-scope path.
- `handoff_check:claims` is the id of `_fill_claims`' "not filled. code could not measure it" (a blank problem, `kind="blank"`), not `field.blank`: wave0 item 1 lists `_fill_claims` under `claims`.
- `values_apply` includes `_text_of`'s "cannot be read as UTF-8 text" (wave0 item 1 lists `_text_of :2612` under `values_apply`); the sentence of `values_file` ("The values file is path: value lines ...") reads as the nearer one.

## Counters (EC-3)

`stage_joints.py --check`: unsited 119 -> 98 (BEFORE and AFTER lines below). Rows sited: the 21 ids of section 0.2. I did not edit `told_ratchet.unsited` (stored 119, a ceiling: clean) and
the K12 pin `test_stage_joints.py:927-932` (exact 119: red in the canon until the integrator commit, named, not a defect of this node: the integrator sets 98 after merge).
told-ratchet handoff_check units (bare 28): judged by the canon (`test_judgment_census`, slow); census: no new blocking unit (no raise or print added, only wrappers).

## FR walk

- A: FR-1/2 texts and doors unchanged, the Record adds `expected`/`door` beside; FR-59 unreadable row gives the factory-defect sentence (row `unreadable row` of the test, EC-4); FR-4/57 n/a.
- B: no text a person reads changed. C: FR-14 output shape of the block, `--json` and every `print` unchanged (K11/K12 pins live in `test_handoff_values_main_block`, judged by the canon);
  FR-17 one constructor. D: FR-16 the ids are literals at the site; none outside the 21. E, F: not touched. G: FR-30 ASCII English (`selftest --lang` green), FR-31 no timing assertion,
  FR-32 root cause = the one constructor, FR-54 siblings below.
- AR: AR-9 (the Problem carries the row), AR-13 (`told_text` via `refusal` only), AR-18 (no output shape change), AR-29 (no judgment moved).

## Friction measured (AR-12)

`refusal()` reads and parses `stage-joints.json` per call (about 5 ms). `check` on the worst fresh form of the package (`s4-case-critic-to-designer`, 32 problems) took 0.185 s in total.
A guard write (`values_report`) pays the same per problem. Nothing cached here (a cache of the rows is `stage_joints`' file, not owned).

## Questions for the Lead

1. Transport. `refusal_text`, `--json` and the stdout of `main` carry no `expected:` / `door:` / `check:` / `told`: EC-6 asks a text transport to print them, but (a) K11 pins the exact stdout bytes of text
   and `--json` and K12 / K-A16 pin the exact key set of `--json` (`test_handoff_values_main_block`, `test_handoff_values_keys`, not in owns), (b) the callers read the LAST line of stdout as the reason, and
   (c) the pre-tool guard builds its block with `refusal_text` (E-T6-2: T6 never edits the guard). I left every transport unchanged. Options: a later node edits the pins and prints the lines; or the pages tell it (S-2).
2. `bad` (`parse_values`) and `refuse` (`_apply_one`) are closures with several callers; B3 (multi-caller helper: no literal) read literally would leave them bare. I put the literal in the closure because every
   caller states the SAME requirement (`values_file`, `values_apply`): one id, one requirement (EC-2 invariant). Same for `_text_of` (two callers, one requirement). Say if B3 is meant literally here.
3. The `rows is None` site above (no row owns the triage being readable).

## Verbatim witness

```
$ python -B ai-packages/qa-factory/scripts/stage_joints.py --check          (BEFORE: HEAD file)
stage joints: ... | told counters: hand_cards 12, legacy_legs 0, unsited 119
stage joints: clean
$ python -B ai-packages/qa-factory/scripts/stage_joints.py --check          (AFTER)
stage joints: walked exit 8, detector 5, window 27 | rows 267, gaps 4 (producer 2, told 1, demands 1), joints held 4 of 267 | role leg not walked (code-to-code rows): 26 | stages with no detector: S0, S1, S6, S7, S9 | told counters: hand_cards 12, legacy_legs 0, unsited 98
stage joints: clean
$ python -B ai-packages/qa-factory/scripts/selftest.py --limits --lang
PASS limits: SKILL.md / agents / references within size caps
PASS limits: every mandatory role rule of design/role-rules.json holds in its carrier
=== qa-factory selftest: 4/4 ok ===
$ python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/handoff_check.py ai-packages/qa-factory/scripts/tests/test_detector_verdict.py
(printed 41 rows; each non-slow, non-quarantined file run alone, scratch driver, 100 s cap, cwd = the package)
test_artifact_writers 23/23 ok; test_check_witness 29/29 ok; test_field_producers 885/885 ok; test_knowledge_notice 15 passed; test_null_outcomes 327/327 ok;
test_open_list_fields 15 passed; test_triage_blocked 50/50 ok; test_triage_identity OK; test_detector_verdict 591/591 ok (26.2 s); test_scenario_walk 93/93 ok; test_scenario_world 33/33 ok
judged by the batch canon (all in slow_tests.json): test_handoff_inline_values, test_handoff_values_keys, test_handoff_values_main_block (K11/K12 byte pins), test_s7_investigation_replay,
test_story_step_start, test_brief_pack_s5_plan, test_bug_records, test_guard_dispatch_budget_and_logs, test_handoff, test_handoff_values_refusal, test_judgment_census, test_s5_plan_controller,
test_scenario_cart_1, test_scenario_local_1_0108, test_scenario_local_1_arm_b; test_stage_joints (K12 unsited pin 119, the integrator's)
```

OLD-text capture: the same 43 provocations ran in-process over the pre-edit file (scratch driver in the scratchpad, not committed); the texts printed are the `T6_OLD` hashes; the new
file printed the same 43 texts (diff of the two captures: none, paths and exit codes included) before the test was written.

Negative control: the `field.max_len` wrapper turned bare on the file (byte copy `scratchpad/hc_good.py` taken first):
`FAIL tbw-t6 field.max_len / a reason of 90: the Record carries the id and the row's sentence - expected ('handoff_check:field.max_len', 'every `required` field ...'), got ('', '')`
and `FAIL tbw-t6 the scanner reads the 21 ids ...` (589/591 ok); `stage_joints.py --check` showed `unsited 99`; restored with `cp` from the copy, sha256 equal:
`58df215eb8124fa8df8e4c0eb87d80fd1178e0118385a6083d210b2b62cef1e8` both; then 591/591 ok again.

tests-over: the new function is about 250 lines against about 85 changed product lines: one row per (id, provocation) over 43 provocations, each needing a form fixture and the old text (as a hash).

## Analogs noticed (not widened)

- `validate_artifacts.py`, `planning_contract.py`, `coverage_contract.py`, `s5_precheck.py`, `manifest_put.py`, `controller.py`: the same Problem-of-text pattern (T7a-c, T5r, T9a nodes).
- `story_step.py` / `driver_*` readers that print `Problem.text` or `refusal_text` as plain text: unchanged, they still get no expected/door (question 1).
- `handoff_help.py` (not owned) prints form problems of its own kind: not read.

## Needed beyond the manifest

`scripts/detector_verdict.py` (`Record`, `refusal`), `scripts/stage_joints.py` (`row_for`, `check_ids`, `_is_sited`), `scripts/refusal_registry.py` (`sites`, `raise_family`), `scripts/null_outcomes.py` (`load_data`),
`scripts/handoff.py`, `scripts/handoff_init.py`, `handoffs/s2|s5|s7*.yaml`, `scripts/slow_tests.json`, `scripts/tests/test_handoff_values_main_block.py` / `test_handoff_values_keys.py` (K11/K12/K-A16 pins),
`test_s7_null_outcome.py` (fixtures), `wave0-rows.md` item 1.
