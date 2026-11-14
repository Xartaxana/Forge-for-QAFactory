# Code critic t-744 — topic A remainder: A2 (91ab1f3), A3 (c8a1ec2), F7 re-cut (74c9430, head 5af10b9), one pass

Diff: `git -C .claude/worktrees/sc-f7rc diff origin/main...HEAD` (head 5af10b9 = origin/wip/sc-f7rc, checked by `rev-parse`).
DoD: topic spec §A.2.2-A.2.4, nodes A2/A3 (`20261113-stage-critics-s2-s3-removed-spec.md:714-775`); re-cut spec
`20261114-sc-f7-recut-register-gaps-spec.md` with the binding amendments A1-A10 of the plan critic (t-730). Earlier verdict t-717 not
re-judged: what it settled for A2/A3 (all keys but B1) stands. No code edited, no CI, no slow file run.

**Verdict: fit_with_fixes.** The re-cut is right in substance. The critic no longer gets a command it cannot run. The driver records the
`register_gaps` rows through the one reader and the one writer, and it does so before the acceptance record and the seam, whatever the
verdict word. The shape judge is pure, and no loss road was found in the driver step. It closes t-717 B1. **One blocker:** the
`test_role_commands.py` example re-pointed by the re-cut is refused by the writer, so the canon goes red. There are four fixes for this
round, and the Lead owes three queue carriers.

## Blocking finding

**B1 — the re-pointed card example is refused, so `test_role_commands.py` goes red on the canon** (`scripts/tests/test_role_commands.py:169`,
`:172`). The example writes `work/critic-findings.md` (`:169`) but passes `--evidence work/runner-notes.md` (`:172`), a file nothing creates.
`accepted_example` (`:113-117`) requires exit 0. I reproduced it with the exact argv, on a story shaped like the test's `story("QA-10")`
(`work/` plus `pipeline.json`):
`exploratory_findings.py add: evidence path work/runner-notes.md is not a file under the task root ...`, rc=2. The control with
`--evidence work/critic-findings.md` (the file that exists) gave `{"id": "EX-1", ...}`, rc=0. Fix: write `work/runner-notes.md` at `:169`,
in place of `critic-findings.md`. The report marks this file "written, not run (slow)". The plan critic asked for both `--by` and evidence
to change. Only half of the move was made.

## Fixes for this round (not blocking alone; one fix round, a fresh worker)

- **F2 — census: a visible unit was renamed away instead of getting its row (A8; AR-29, AR-20).** The report (§4) says: before the rename,
  `units_of` showed `('driver_stage_plan.py', 'refuse') ['u1']` rowless, "hence `gap_refusal`". UNIT_NAME_RE `_?refuse`
  (`test_judgment_census.py:77`) saw the refusing helper of exactly the checks A8 names. The rename moved them into the documented blind
  spot ("a check's meaning under a neutral name ... is not seen", `:41-42`). DoD 6 said rows go in when the scan creates units. It did
  create one, and the move taken was to make the scan stop seeing it. Fix: give the helper back a name the scan sees (e.g.
  `refuse_gap`) and write its row(s) as the census test prints them: class `xref` for the identity join, `shape` for the section judge,
  owner `data`, roles `["qa-case-critic", "conductor"]`, and any `blocking_per_role` move named as a raise (AR-20). The builder's open
  question is answered under key 2.
- **F3 — X1/X2 are now duplicates that pin a road no actor takes** (`test_exploratory_findings.py:481-524`, `key_a3`). The re-cut spec
  D.6 owns "X1 evidence path" and says X1's evidence becomes the critic's form. Plan-critic key 9 also asked for X1's docstring ("the S4
  case critic records") to change. Neither was done. X1 still calls `EF.append(..., by="S4-qa-case-critic-1")` with the critic's
  findings file. No S4 actor does that any more: the driver records the row, with the form as evidence. J1 covers the real road from
  form to register to report, and the writer's basic add is in key_m1_1. X2 ("no evidence refused") repeats K-M1-1 at `:116` ("K-M1-1 no
  evidence"). TESTING.md asks for one test per behaviour. Fix: delete `key_a3` and `critic_findings` (J1 plus K-M1-1 hold both
  behaviours), or re-point X1 to the form and drop X2. Either way, the docstring stops saying the critic records.
- **F4 — SIBLING_MAP axis 5, row :149 "A role without Bash raises a before/now question", is not touched.** The row ends "A third role
  without Bash that must raise a question joins this row". The S4 critic is a no-Bash role whose form section code raises into a
  register, which is the same pattern. Plan-critic key 13 asked for `register_gaps` to be appended to this row in the node's commit. Only
  the "Skill phase <-> driver" row (:128) got its sentence. Fix: one clause on :149 naming `register_gaps` -> `Driver.register_gaps_write`
  -> `exploratory_findings.append`. It also says that row's step (`question_register._question_row`) is not shared, because the
  register differs.
- **F5 — commit 74c9430 declares `axes: not a mechanism`.** The commit adds a form section that is a duty for a role, and a driver step
  that refuses. Under rule 10's recognition clause both are a mechanism. The axis block exists in the spec (§"SIBLING_MAP axes"), so the
  substance is there and the declaration is false. Fix, at the integrator's merge commit: a pointer line to the spec's axis block
  instead of "not a mechanism". This is not a builder code edit.

## Queue lines owed by the Lead (not this builder; a carrier the target reads, CLAUDE.md rule 4)

Grep `-i -E "register_gaps|F-R0|skill road|directory as"` over `plans/`, `docs/tasks/` and `CURRENT_CONTEXT.md` on origin/main, excluding
the two F7 spec/review files, found none of the following in a pile. Positive control: the same grep finds 33 `register_gaps` hits in the
re-cut spec. A compact snapshot says only "skill road queued".
- Q1 — the skill road records no `register_gaps` row (A6/R18). Owner: the qa-story pile (or the skill-retirement node).
- Q2 — the census blind spot of the driver family: `Refusal(Exception)` is neither a ValueError nor a StateConflict subclass, and
  `raise factory(...)` is unseen, so no driver refusal is a census site. `driver_stage_plan.py` has 0 rows in `judgment-census.json` (the
  count by grep; positive control: `exploratory_findings.py` rows found). Owner: Lead / census pile. This holds even after F2: F2 covers
  one helper, not the family.
- Q3 — `exploratory_findings.read` reads a directory as the empty register (AR-28 analog; plan critic A5). Q4 —
  `raise_from_handoff` non-list analog. Q5 — CL-NS. Q6 — the F-R0 owner question (P31; see key 10). All are named by the Lead's decision
  list as queue lines, but none was found in a pile.
- Owner notice (quarantine, key 11): `test_handoff_init_author.py::test_check_verdict_unchanged_by_emptying[s4-case-critic-to-designer-*]`
  goes red for a NEW reason caused by this diff. It is not named in topic §O or in the re-cut spec.

## Answers per key

**1) A1-A10.**
| amendment | status | evidence |
|---|---|---|
| A1 EMPTIED row, refs "or omit", test row | built differently, right | `handoff_init.py:187`; template refs hint ends ", or omit"; the A1 rows live in `test_exploratory_findings.py:723-744`, because the only file that pins EMPTIED is quarantined (`test_handoff_init_author.py`, `test-layers.json:8446`; case-sensitive grep `EMPTIED\|empty_optional_lists` over `scripts/`: handoff_init, the quarantined file, this test). The emptied copy passes; the control (raw sample row refused) passes; the values file opens row 0; a filled row with no refs gives no problem. Side effect: key 11 |
| A2 owns: driver-layers rows, role-load re-measured | built | three rows `driver-layers.json:533-535` (no `row` key, like 219 of 1046 others); role-load re-measured, not hand-merged: my re-run of `role_load.py --all --json` = 12676/11326, 16989/15409, 18686/16333, equal to the committed rows |
| A3 `Refusal(text, dispatch=)`, conductor door | built | `driver_stage_plan.py:655-658`; door `handoff_check.py --file <form> --set register_gaps[<i>].<field>=<value>` or delete the row and keep the gap in `questions[]`, then retry. Door probed: `--set "register_gaps[0].missing_prerequisite=..."` on a scratch form wrote the value |
| A4 re-fix equal bytes | built | row A4 PASS in my re-run |
| A5 OSError from read and append; G11 | built | `:666-668`, `:684-687`; G11 PASS |
| A6 edge R18 on axis 5 | built for the map row; queue line missing | SIBLING_MAP :128 sentence present; Q1 above; row :149 is F4 |
| A7 the why text | built, verbatim | `driver_stage_plan.py:10-11` equals the amendment text |
| A8 census classes | built differently, wrong | no rows; the visible unit was renamed (F2) |
| A9 extra key ignored with a print | built | `:672-673`; G5b |
| A10 F-R0 (a) as built | built | no capability read: `role_has_bash` count 0 in `driver_stage_plan.py` (control: 4 in `host_adapter.py`); the road is chosen by the contract section at one S4 call site |
| bytes (+28 B) | built, trimmed | the re-cut is net -28 B / -7 ratchet tokens / 0 process tokens against the A2 tip; no raise of its own |

**2) Census.** The two functions hold no hidden judgment. `register_gap_rows` judges type, placeholder (`handoff.is_placeholder`: the
template's `<...>` marker or empty, a shape test of the sample, not a phrase list over role content) and template keys.
`register_gaps_write` makes an exact-text comparison against ACTIVE `coverage_gap` lines (xref). Neither judges whether a row is a gap
or whether two rows mean one gap (P27, AR-29 hold). The missing unit is a real blind spot of the census for the whole driver family (Q2,
owner Lead). It is not only a quirk of these names. But a unit DID exist now, and it was renamed away. Fix F2 restores it with its row.
Q2 covers the family.

**3) The three small decisions.**
- (a) `exc.known = False`: right. `route_known` returns None on `known False` (`driver_machine.py:85-86`). The head is not resumable
  anyway (plan critic key 3), so this only hardens it: the writer's own words (`already has line`, ...) can never be table-routed. The
  sibling questions raise is a G refusal (`py(check=True, expect=...)`), so the two roads match.
- (b) A bare `register_gaps:` parsed as `{}` and read as "no gaps": right, and no unknown becomes a pass (AR-28, FR-59). I measured with
  `handoff.parse`: a bare key gives `{}`, `null`/`~` give None, `""` gives `''`, `[]` gives `[]`, and all give `([], [])`. A bare key
  carries no row text, so nothing exists to lose. The parser cannot tell `{}` from a bare key, so R5's "a mapping is refused" holds for a
  NON-empty mapping (G4 "a mapping" passes). Malformed shapes I probed: a flow list and an under-indented list parse to rows and are
  recorded. `refs: R-1, R-2` (a string) is refused naming `register_gaps[0].refs`. `- {}` is skipped as an empty row (no content).
  Multi-line block text is recorded whole. None is silent.
- (c) The A1 EMPTIED rows in `test_exploratory_findings.py`: right (no kept file pins EMPTIED; verified above). It is a Lead/owner
  notice, not a builder fix, that the quarantined pin now disagrees (key 11).

**4) Direction of error.** No silent loss in the driver step:
- malformed form: refused, nothing written (G4, G5);
- OSError from read or append: refused (G11);
- form rewritten after the add: identity is on parsed values, not bytes, and a re-fix of an unchanged form leaves equal bytes (A4);
- equal-bytes replay: skipped (G8);
- extra keys: ignored with a print, the row recorded (G5b);
- a crash between append and the form rewrite: the next finish re-reads the same form and skips (D.4);
- the recovery road: `completion_for` passes the same dispatch.
Residuals, named and accepted by the spec or the plan critic:
- R9: a form `handoff.parse` cannot read goes to the seam, and its rows are recorded only if the finish runs again. This is the same as
  the `questions[]` sibling.
- R18: the skill road.
- An empty `stage_acceptor("S4")`, unreachable in the package.
A gap IS recorded twice in these cases, all in the allowed direction:
- two equal rows in one form on the first finish (`active` is read once, before the loop; disclosed by the builder);
- a reworded row in a later round (G10);
- a line the conductor withdrew between a refused finish and its retry;
- a line the conductor reworded by `correct` before an S4 rework.
An equal row recorded by another role is skipped, with attribution drift (plan critic key 4). `_confirm_exploratory`'s `correct` copies
title, statement, refs and missing_prerequisite (`driver_machine.py:2805-2806`), so a person-confirmed line still matches, and no
duplicate arises there.

**5) The refusal of A3.** FR-1: each text names what is wrong (every shape problem at once as `register_gaps[<i>].<field>: ...`, or the
writer's own text with the row index), what is expected ("Expected a list of rows {title, statement, refs, missing_prerequisite}, or []
for no gap"), and the form and the register path. FR-2/AR-9: the door addresses the conductor, the one who receives it
(`conductor_round` -> `no_move`, `driver_conductor.py:822-850`). The `--set` door works on an indexed path (probe above). "Retry the
finish" maps to the conductor's `retry` move (`:824`). AR-17: one seam. The OSError door "restore the file, then retry" fits the
directory case.

**6) A2/A3 against the topic DoD; the merge.**
- A2: every key t-717 accepted is still present in the diff (register bullet, scope sentence, advice items, strategist reminder, form
  inputs `required: false`, `advice_read` one string). The Tools line is replaced by the re-cut's line, which keeps "it reaches the test
  report". The re-cut key-presence run (report §4) holds, with a negative control.
- A3: the card stays for runner/analyst only (`role-commands.json:201-208`). The critic-only sentence is gone from `input`. The
  epilog, the TOLD/GUARDED rows and the changelog sentence are rewritten.
- B1 (t-717) is closed. My grep `-i "exploratory_findings|findings register|register_gaps"` over the critic's charter, its slices,
  `ahead-cards.json` and `phases/s4.md` finds only the new charter line at `:96`. Positive control: `critic_rollcall` is found in the
  same charter.
- The merge: the role-load conflict was settled by re-measuring (my re-run matches). The three driver-layers rows are present.
- t-717 findings this diff closes: B1. Left untouched: B2 and N1-N6 (A1a/A1b/A1c's, not this diff), and N7 (the GUARDED "open" row
  stays, correctly).

**7) Ratchets.** The role-load raises are named in the commit message and the report against main's rows. All six come from A2's merged
text, and the re-cut itself is net negative. The +28 B allowance was not needed (trimmed to -28 B). `ROLE_BRIEF_BYTES_MAX` is unchanged
(no brief change). The census ratchet did not move, but only because of the rename (F2).

**8) Tests against TESTING.md.**
- `key_f7rc`: each row id names its case (G1-G15, J1, A1, A4). G2 and G4 are loops over labelled variants. One world per row. No driver
  process. G13/G14/G15 pin the call-site order by behaviour, not by a source pin.
- Duplicates: X1/X2 (F3).
- Rows written for slow files:
  - `test_role_commands.py`: RED (B1, reproduced).
  - `test_driver_layers.py`: plausible (row shape as 219 others).
  - `test_judgment_census.py`: plausibly green by regex reading (`register_gaps_write`, `register_gap_rows`, `gap_refusal` match no
    UNIT_NAME_RE branch), but green only because of F2.
  - `test_handoff*.py` / `form_filler` over the new template section: not run. The exit check over every fixture S4 critic form (no
    section) gives 0 problems on the branch (probe), so absent-section forms stay clean. The rest is judged by the canon.
- My control re-run of the one fast file: `=== test_exploratory_findings: 299/299 ok ===`, equal to the report.

**9) Duplication and consistency.** None found for a second register writer. My grep `-i "exploratory-findings.jsonl|exploratory_findings\.append|EF\.append|register_path("`
over `scripts/*.py` found writes only through `EF.append` (`driver_machine.py:2813`, `driver_stage_plan.py:680`). `append_jsonl_line(`
appears only at `exploratory_findings.py:392`; positive control: `def append` at `:277` found by the same grep. The `driver_stage_s7.py`
hits are path text and is_file reads (pre-existing).
None found for a second parser of the critic's form. `register_gaps_write` parses with `handoff.parse` and reads fields from
`handoff.template`. `register_gaps` appears only in `driver_stage_plan.py`, `handoff_init.py` and the template.
Duplication found: X1/X2 versus J1/K-M1-1 (F3). The identity rule differs from `_confirm_exploratory`'s, on purpose (confirmed versus
recorded), so no shared helper is owed.
**Code quality.**
- `register_gaps_write` is about 57 lines and `register_gap_rows` about 45, one job each.
- The OSError door sentence is repeated twice (minor).
- `stage_verdict_known` re-parses the same form right after: cheap, and accepted.
- No dead branch.
- The rename in F2 is the one quality defect: a name chosen to hide a check from its detector.

**10) Class completeness by SIBLING_MAP.**
| axis | status | where |
|---|---|---|
| 5 | covered for "Skill phase <-> driver" (:128); missed for "A role without Bash raises" (:149) | F4 |
| 18 | covered | role-load re-measured |
| 19 | n/a as built | A10, no capability read |
| 29 | covered | no new appender |
| 31 | covered | charter: when; template: fields; card: runner/analyst |
| 32 | census: F2 | |
| 33 | covered | the completion's dispatch id |
| 34 | open | the owner question F-R0, Q6 |
P31 / one road: today each role has ONE road. The critic only writes the form (no carrier tells it to run the command, grep above), and
runner/analyst only use the CLI. The register has two producer roads keyed by the contract section. Only the owner can allow that
(P31), and the Lead decision routes it to the owner. So this verdict does not block on it, but it leaves the residual as a proposed node
with its owner: Q6 (the F-R0 question to the owner, naming the S6/S7 wiring F-R2 (c) as the road to one form) and Q1 (skill road,
qa-story pile). The queue line is enough ONLY once it is written in those carriers. It was not found on origin/main.

**11) Quarantined readers at the next quarantine watch.** The topic §O names the S2/S3 reds of `test_handoff_init_author.py`,
`test_controller_stage_acceptance.py`, `test_rows_owed.py` and others. NEW and unnamed:
`test_check_verdict_unchanged_by_emptying[s4-case-critic-to-designer-{"",ok,concerns}]` (`test_handoff_init_author.py:148-162`) goes red
because `EMPTIED_PATHS = ("questions", "findings")` (`:136`) does not exclude `register_gaps`. I evaluated the invariant in process,
without running the quarantined file: the problems outside the emptied paths, before versus after, are not equal; only before has
`register_gaps[0].missing_prerequisite/.statement/.title`. Door: the owner notice, then `test_quarantine.py judge ... --verdict stale`
(quarantined files are edited only by the owner's word). In the kept set, nothing pins removed behaviour except X1, which pins a
recording road no actor takes (F3).

## Trail

Read:
- the re-cut spec (whole) and the plan-critic verdict (whole); verdict t-717 (whole);
- topic spec `:184-293`, `:714-776`, `:1004-1032`;
- the builder report (whole);
- the full diff origin/main...5af10b9 and the 74c9430 commit message;
- `driver_stage_plan.py:1-60`, `:600-690`, `:795-830`; `driver_core.py:100-122`; `driver_machine.py:68-93`, `:2783-2814`;
  `driver_conductor.py:822-850`;
- `exploratory_findings.py:80-86`, `:225-252`, `:277-372`; `handoff.py:409-418`, `:680-683`;
- `test_judgment_census.py:1-77`, plus greps; `test_role_commands.py:113-173`; `test_exploratory_findings.py` (the diff and `:290-330`);
  `test_handoff_init_author.py:10-30`, `:85-175`;
- `SIBLING_MAP.md:128`, `:149`; `driver-layers.json` (schema count); `judgment-census.json` (ratchet, rows grep);
  `critic_verdict.schema.json`.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "B1 scripts/tests/test_role_commands.py:169,172 - the re-pointed card example writes work/critic-findings.md but passes --evidence work/runner-notes.md, which nothing creates; exploratory_findings.py add refuses it (rc 2, reproduced), so accepted_example fails and the canon goes red"
  ],
  "fixes": [
    "F1 (B1) test_role_commands.py:169 write work/runner-notes.md instead of critic-findings.md",
    "F2 driver_stage_plan.py:655 - the helper was renamed from refuse to gap_refusal to leave the census (report section 4); give it a name the scan sees and write its census row(s) (xref identity / shape section judge, owner data, roles qa-case-critic + conductor), naming any blocking_per_role raise (AR-20)",
    "F3 test_exploratory_findings.py:481-524 key_a3 - X1 pins a recording road no actor takes (critic append with its findings file) and duplicates J1; X2 duplicates K-M1-1 (:116); delete key_a3 and critic_findings, or re-point X1 to the form and drop X2; the docstring stops saying the critic records",
    "F4 docs/SIBLING_MAP.md:149 - append register_gaps -> Driver.register_gaps_write -> exploratory_findings.append to the row 'A role without Bash raises a before/now question'",
    "F5 integrator: the merge commit carries a pointer to the spec's axis block instead of 'axes: not a mechanism' (74c9430 adds a form duty and a refusing driver step)",
    "Lead queue lines, none found in a pile on origin/main: Q1 skill road records no register_gaps row (qa-story pile); Q2 census blind spot of driver Refusal raises (driver_stage_plan.py has 0 census rows; census pile); Q3 exploratory_findings.read reads a directory as empty; Q4 raise_from_handoff non-list analog; Q5 CL-NS; Q6 the F-R0 owner question (P31)",
    "Owner notice: quarantined test_handoff_init_author.py::test_check_verdict_unchanged_by_emptying[s4-case-critic-to-designer-*] goes red because EMPTIED_PATHS (:136) lacks register_gaps; not named in topic section O"
  ],
  "class_completeness": "Class 'a no-shell role told to run a command' (B1 of t-717): closed for the case critic (charter line, card roles, F-R7 units line; grep over charter, slices, ahead-cards, phases/s4.md finds only the new form-row line; control critic_rollcall found); drift rows of the card go to CL-NS (Q5). Axis 5: skill row :128 covered, no-Bash row :149 missed (F4). Axis 32 census: one visible unit renamed away (F2); driver-family blind spot to Q2. Axis 34 / P31: two producer roads keyed by the contract section, routed by the Lead to the owner (Q6) with the skill road (Q1); the queue lines are not yet in a carrier. Analogs: read() of a directory (Q3), raise_from_handoff non-list (Q4).",
  "trail": {
    "read": [
      "docs/tasks/specs/20261114-sc-f7-recut-register-gaps-spec.md",
      "docs/tasks/specs/reviews/20261114-sc-f7-recut-plan-critic.md",
      "docs/tasks/specs/reviews/20261114-stage-critics-topic-a-critic.md",
      "docs/tasks/specs/20261113-stage-critics-s2-s3-removed-spec.md:184-293,714-776,1004-1032",
      ".claude/worktrees/sc-f7rc/docs/tasks/specs/reports/20261114-sc-f7rc-report.md",
      "git diff origin/main...5af10b9 (all 19 files) and the 74c9430 message",
      "sc-f7rc scripts/driver_stage_plan.py:1-60,600-690,795-830; driver_core.py:100-122; driver_machine.py:68-93,2783-2814; driver_conductor.py:822-850",
      "sc-f7rc scripts/exploratory_findings.py:80-86,225-252,277-372; handoff.py:409-418,680-683",
      "sc-f7rc scripts/tests/test_judgment_census.py:1-77; test_role_commands.py:113-173; test_handoff_init_author.py:10-30,85-175; test_exploratory_findings.py diff and 290-330",
      "docs/SIBLING_MAP.md:128,149; scripts/tests/fixtures/driver-layers.json; scripts/tests/fixtures/judgment-census.json; tools/critic_verdict.schema.json"
    ],
    "reruns": [
      {"command": "python -B exploratory_findings.py add ... --by S6-qa-runner-1 ... --evidence work/runner-notes.md (the test_role_commands example argv, scratch story with work/critic-findings.md only)", "result": "rc=2 'evidence path work/runner-notes.md is not a file under the task root'; control with --evidence work/critic-findings.md rc=0 EX-1"},
      {"command": "python -B scripts/tests/test_exploratory_findings.py (sc-f7rc, package dir)", "result": "=== test_exploratory_findings: 299/299 ok ==="},
      {"command": "python -B scripts/role_load.py --all --json (sc-f7rc)", "result": "tester 12676/11326, strategist 16989/15409, case-critic 18686/16333 - equal to role-load.json"},
      {"command": "handoff_check.py --file <scratch S4 form> --set register_gaps[0].missing_prerequisite=...", "result": "value written at the indexed path (the conductor door works); rc 1 from unrelated header problems of the scratch form"},
      {"command": "in-process handoff.parse + register_gap_rows over bare / null / ~ / {} / '' / [] / flow / under-indent / refs csv / - {} / block text", "result": "empties give ([], []); flow and under-indent recorded; refs csv refused naming register_gaps[0].refs; - {} skipped; multiline whole"},
      {"command": "in-process handoff_check.check over every fixture S4-qa-case-critic-*.yaml (no register_gaps section) on the branch", "result": "0 problems on all six plain forms (values.applied copies: one pre-existing scope problem)"},
      {"command": "in-process: the quarantined invariant of test_check_verdict_unchanged_by_emptying for s4-case-critic-to-designer", "result": "outside-emptied problems before != after; only before has register_gaps[0].title/.statement/.missing_prerequisite"},
      {"command": "grep -c role_has_bash driver_stage_plan.py / host_adapter.py; grep writers of the register over scripts/*.py; git grep -i queue lines over plans docs/tasks CURRENT_CONTEXT.md on origin/main", "result": "0 / 4 (control); writes only via EF.append, append_jsonl_line only exploratory_findings.py:392; no pile carries Q1-Q6 (control: 33 register_gaps hits in the spec)"}
    ]
  }
}
```
