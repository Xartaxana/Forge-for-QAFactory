# TBW-T3b report (t-1567, TBW1-12): brief without ahead cards, groups line, first_look:put.* ids

Branch `worktree-agent-acf7909480b48d8d4` on 33ead99f. Commits: `39e3169d` (item 1, first_look sites), `78303f23` (brief, prompt, window_record, tests, changelog). Builder, Sonnet.

## HEAD OF REPORT: changes needed outside owns (the DoD cannot be fully green without them)

1. `scripts/tests/test_first_look_wiring.py` `test_first_look_brief_names_no_run_report` (:272-274) now FAILS two rows, both because the spec removes what they pin:
   - :272-273 asserts `"first_look.py put"` is in the brief's `DoD:` line; the card says `FIRST_LOOK_DOD` keeps its first sentence only, so the line no longer names `put`. Needed: drop `and "first_look.py put" in (lines_of(text, "DoD: ") or [""])[0]` (keep the goal assertion).
   - :274 asserts the sentence `The record is checked by \`first_look.py put\`` (FIRST_LOOK_AHEAD, removed). Needed: delete the row (the `first_look:put.*` rows on the page tell it).
2. `scripts/tests/test_ahead_cards.py` :354-360 (the "brief carries the rules ahead" loop, 2 rows per role) FAILS 24 rows. The card said "not owned, T1r-cards landed", but reality at 33ead99f: those rows are still there and call the brief section. Needed: delete the two `check_in` rows at :358-360 (the card text is on the page; test_contract_slices already pins the page).
3. `scripts/tests/test_contract_slices.py:664` calls `brief_pack.ahead_card("qa-scout")` (AttributeError now). Needed: drop that comparison row (the moved copy `contract_slices.ahead_card` stays).
4. `scripts/tests/test_ahead_cards_rules.py` (quarantined, not run, not edited) monkeypatches `brief_pack.ahead_card` and asserts the card line in a built brief; it is dead after this node. `test_brief_pack_roles.py` (quarantined) pins the `## Commands` section by hash and reads `AHEAD_HEAD`; same.
5. `scripts/driver_dispatch.py:655` calls `story_step._prompt(...)` directly for a driver rework prompt; it passes no `groups`, so that prompt has no groups line (an analog of the card's prompt, the `groups=None` default adds nothing). A driver-owner change if the Lead wants the line there too.
6. Pre-existing, NOT mine: `test_role_load.py` is red on main too (A22 qa-bug-reporter 15,733 < row 15,734; run on the root checkout, same 2 FAILs).

## Plan items

| item | state | files |
|---|---|---|
| 11 `first_look:put.*` ids at their sites | DONE | first_look.py |
| `ahead_card`, ahead section, `FIRST_LOOK_AHEAD` removed; `FIRST_LOOK_DOD` first sentence; `FIRST_LOOK_ROLES_MAX` and its 3 arguments removed | DONE | brief_pack.py |
| `_row_field_lines` -> a call; new `window_record.row_field_lines` | DONE (kept as a one-line delegate: test_window_record.py:2188 calls `brief_pack._row_field_lines`) | brief_pack.py, window_record.py |
| `dispatch_groups`, `groups_line`, brief line under `## Commands`; card fill through `stage_joints.fill` | DONE | brief_pack.py |
| `_prompt` groups line outside the `not resumed` branch; `_card_text` passes it | DONE | story_step.py |
| tests | DONE (see below) | test_first_look.py, test_brief_pack.py |
| changelog | DONE | changelog.d/tbw-t3b.md |

## Site table (function | fragment | id or E6 reason | test row | proof)

Proof: F = proved fast in `test_first_look.py::test_put_problems_carry_their_row_ids`, run, green.

| function | fragment | id / reason | row | proof |
|---|---|---|---|---|
| put | `--null is why no first look was walked` | put.null_reason | null_reason | F (+ CLI row: expected line and last `check:`) |
| put | `a walked first look ... exists and is current` | E6: no row (F-W6) | - | bare, comment at the site |
| put | `the first-look walk ... is not open` | put.walk_open | walk_open | F (negative control) |
| put | `the code or the register changed since this walk was opened` | put.inputs_current | inputs_current | F |
| put (caller of `_load_input`, one caller) | `--file ... cannot be read / not UTF-8 / JSON / no mapping` | put.input | input | F |
| put_problems | `rows is one mapping`, `a second row`, `no row for` | put.rows | rows | F (`no row for`) |
| _row_faults (wraps `_row_problems`) | every non-path problem of a row (words, req, why, evidence, quote, capture_cited reason) | put.rows.row | rows.row | F |
| _path_faults | not a mapping, unknown key, url text | put.rows.path | rows.path | F |
| _path_faults | list fields (EC-2: `_list_faults` has 4 callers, id on the caller), `locators`/`api` not a list | put.rows.list | rows.list | F |
| _api_faults | not a mapping, unknown key, method/path text, seen, sample | put.rows.api | rows.api | F |
| _auth_faults | `.auth is one of` | put.rows.auth | rows.auth | F |
| _locator_faults | mapping, unknown key, what/selector, seen | put.rows.locator | rows.locator | F |
| put_problems / `_sign_in_faults` / `_list_faults(gaps)` / top-level unknown key / attempt-names-no-walk / register unreadable | - | E6 (role) or (code): no row says them | - | bare |

`unsited 17 -> 6` (summary line `told counters: hand_cards 12, legacy_legs 0, unsited 6`; was 17 before the node: `stage_joints.py --check` run on the base).

Byte identity: `str(Record)` is the old text; `" | ".join(problems)` is unchanged; 450 existing rows of test_first_look.py green unchanged. The CLI (`_refuse_put`) prints the joined text, then the FIRST problem's `expected:`/`door:` and every further sited check as a told line, `check:` last = the first problem's id (before: `role_cli:first_look.py put`). A parser of the refusal sees the same first line.

## Decisions (not in the card) and why

- `dispatch_groups` reads the rows of ALL stages of the role (as the page does), not `[stage]`: the first-look rows say `stages: ["S6"]` while the first look runs at S3, so `[stage]` named no group for a first look (my first run showed it). FINDING for T1r-cards-R: the 11 first_look rows say S6; the walk is S3.
- The group names are the page's own headings without `### ` (`contract_slices._group_heading`, a private call across modules: no public heading function exists; contract_slices.py is not mine). Only groups the role has rows in are named.
- Could-not-tell: plan/window when `_s5_kind` is `unknown` or there is no dispatch record for an S5 plan role; first_look/not_first_look when a runner has no record. Text: `could not tell: read both "<A>" and "<B>" and ask the conductor` (mech 2.4 (3)).
- When the rows file cannot be read `dispatch_groups` raises; `build` and `_card_text` then print NO line (the page holds every group; invention of a fallback sentence avoided). QUESTION for the Lead: prefer a could-not-tell line there?
- `_prompt(..., groups=None)`: None adds nothing, so every existing caller/test prompt is byte-identical; the line stands right before the `resumed` computation (after the form lines, before the brief line).
- In-flight cards written before this node differ from `_card_text` now (`materialize` compare reports a differing card: one note, the role runs).
- Rows that over-claim (EC-8, not edited): `put.rows.path` "names a real place of the product" (code checks shape only); `put.rows` "states its path, API, auth and locator correctly" (also covers the rows-set checks); `put.rows.row` also carries the `capture_cited` reasons (a capture of this walk), which "required fields" does not say. For T1r-cards-R.
- Analogs noticed, not widened: `stage_joints._carrier_expected` renders REQUIRED_ROW_FIELDS itself and does not call `window_record.row_field_lines` (mech 2.3 says it should; stage_joints.py not owned); `window_record.py:267` / `probe_by_code.py:2892` print `unknown_profile_refusal` as plain text.

## Tests

- `test_first_look.py`: `test_put_problems_carry_their_row_ids` (11 ids, one table) + one CLI assertion on the existing bogus-null row. Written and run.
- `test_brief_pack.py` (slow, canon): `t3b_groups_line` (8 fixtures: plan, window, first look, plain runner, plain scout, no record x2, broken state; the line variants; a resumed prompt and a first prompt) + 3 rows in `main` (start's prompt carries the line, the scout brief has the line under Commands and no ahead section, the S5 automator row replaced). NOT RUN as a file (slow); I ran `t3b_groups_line()` alone through a scratch driver in temp (not committed): `=== t3b_only: 22/22 ok ===`.
- Budget: tests added ~100 lines vs ~190 lines code and product text.
- Not run locally: `test_brief_pack.py`, `test_window_record.py`, `test_story_step*.py` and every other slow file of `scenario_walk --witness-for` (70 files): canon judges.
- Negative control: `first_look:put.walk_open` made bare on a byte copy (sha256 `e81330f2...e9353aa` before): `FAIL put_problems_carry_their_row_ids: walk_open: refused, the problem is a Record of first_look:put.walk_open`, `=== test_first_look: 462/463 ok ===`, `unsited 7`; restored by `cp`, hashes equal (`e81330f2...e9353aa` both), `git status` clean.

## Verbatim witness (one run after all edits, HEAD 78303f23)

```
$ python -B ai-packages/qa-factory/scripts/tests/test_first_look.py
=== test_first_look: 463/463 ok ===
$ python -B ai-packages/qa-factory/scripts/tests/test_first_look_wiring.py
FAIL first_look_brief_names_no_run_report: the goal is the first look's, recorded with put - # Brief - S3-qa-runner-1 ...
FAIL first_look_brief_names_no_run_report: the ahead card says put checks the record - 'The record is checked by `first_look.py put`' not found in: ...
=== test_first_look_wiring: 100/102 ok ===        (both rows pin what the card removes: item 1 above, outside owns)
$ python -B ai-packages/qa-factory/scripts/stage_joints.py --check
stage joints: walked exit 8, detector 5, window 28 | rows 287, gaps 4 (producer 2, told 1, demands 1), joints held 4 of 287 | role leg not walked (code-to-code rows): 27 | stages with no detector: S0, S1, S6, S7, S9 | told counters: hand_cards 12, legacy_legs 0, unsited 6
stage joints: clean
$ python -B ai-packages/qa-factory/scripts/selftest.py --limits --lang
PASS limits: SKILL.md / agents / references within size caps
PASS limits: every mandatory role rule of design/role-rules.json holds in its carrier
=== qa-factory selftest: 4/4 ok ===
```

The 29 fast files of `scenario_walk.py --witness-for <owns>` run one by one (scratch loop in temp): all green except `test_ahead_cards.py` 229/253 (item 2), `test_first_look_wiring.py` (item 1), `test_role_load.py` (item 6, pre-existing). The rest (test_first_look_briefs 261/261, test_first_look_step, test_first_look_code_look, test_brief_s3_roster, test_codex_tool_guidance, test_fit_targets, test_regression_scope, test_stage_cards, probe tests, ...) green.

## Hygiene / telemetry

- `FIRST_LOOK_ROLES_MAX` removal was optional ("may go"); done. `_stand_names(limit=None)` keeps its parameter (test_brief_pack.py:2952 calls it with two arguments).
- Needed beyond the manifest: `contract_slices.py` (`GROUPS`, `_group_heading`, page layout), `stage_joints.py` (`rows_for`, `load_rows`, `fill`), `controller.py` (`s5_part_of`), `s5_plan.mode`, `role_cli.refuse`, `driver_dispatch.py:655`, `test_first_look_wiring.py`, `test_ahead_cards.py`, `test_ahead_cards_rules.py`, `test_contract_slices.py:664`, `test_window_record.py:2188`, `slow_tests.json` via scenario_walk.
- Loops or processes left running: none. Scratch files only in the OS temp.
