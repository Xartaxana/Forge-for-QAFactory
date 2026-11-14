# Critic on a PLAN — F7 re-cut (register gaps through the S4 case critic's form), one pass

Under review: `docs/tasks/specs/20261114-sc-f7-recut-register-gaps-spec.md` (whole, with its Lead decisions). Trigger: B1 of
`docs/tasks/specs/reviews/20261114-stage-critics-topic-a-critic.md:20-37`. Code: read-main fd30668, sc-a2 91ab1f3, sc-a3 c8a1ec2.
No code edited. Line numbers below are read-main unless a worktree is named.

**Verdict: fit_with_fixes.** The road (c') is sound: one writer kept (in-process `exploratory_findings.append`), one reader, AR-29
held, the call site precedes the record and the seam. But four facts the draft states are false on the carriers, and each one breaks
the node if it ships as written: (A1) an untouched sample row, and a row with no `refs`, are REFUSED at the exit gate; (A2) the owns
miss two files the node must write (`driver-layers.json`; the `handoff_init.py` EMPTIED row) and the A2 merge conflicts with main on
`role-load.json`; (A3) the refusal never reaches the critic, so its door names a file no reader of the text will open; (A4) the form
IS rewritten after the add (R16 / F-R5 premise). G11 also expects a refusal that cannot happen as designed. All of them are fixes the
Lead can paste into the spec. None of them needs a redraft.

## Binding amendments (paste into the spec)

- **A1 (key 1).** "Add `"register_gaps": ("s4-case-critic-to-designer",)` to `handoff_init.EMPTIED` (owns `scripts/handoff_init.py`,
  that row only, plus one row in `test_handoff_init_author.py` or the file that pins `EMPTIED`), and make the `refs` placeholder
  optional by its own words (`- <R-n or TC-n the gap stands against, or omit>`). The node is tested by a row where the role's copy
  holds `register_gaps: []` and the exit check of a form with one filled row and no refs gives no `register_gaps` problem."
- **A2 (keys 10, 12).** "owns also: `scripts/tests/fixtures/driver-layers.json` (rows for `register_gaps_write`, `register_gap_rows`,
  `REGISTER_GAP_WHY` only); `references/role-load.json` also the `qa-requirements-tester` and `qa-test-strategist` rows (merge
  resolution against main, re-measured). The merge of wip/sc-a2 into main CONFLICTS in role-load.json (measured); the builder settles
  it by re-measuring with `role_load.py --all --json`."
- **A3 (key 3).** "The refusal is `Refusal(text, dispatch=dispatch)`, and its door is written for the CONDUCTOR, who is the one that
  receives it (the head is not a resumable head, so the critic is not resumed): `handoff_check.py --file work/handoffs/<d>.yaml --set
  register_gaps[<i>].<field>=<value>`, or delete the row and keep the gap in `questions[]`; then the finish is retried. Rows already
  recorded are skipped on the retry. F-R4's reason for (a) over (c) is struck: (a) also costs one conductor call."
- **A4 (keys 5, 4).** "R16 is replaced by: the form IS rewritten after the add: `story_step finish` runs `handoff_check --fix`, which
  always writes the file, and a refused finish resumes the critic, who edits its form. The S4 line's evidence sha can therefore go
  stale. `exploratory_findings.py check` (a role-channel command, called by no code) will then report it. The report does not judge
  the sha. Accepted residual: the line carries the row's text whole. G-row: after a second `handoff_check --fix` over the unchanged form,
  the bytes are equal (pin it, or name the drift)."
- **A5 (key 10, R10).** "Step 4 catches `OSError` from `append` as well as from `read` (R10's refusal text). G11 expects: register path
  is a directory -> `read` gives the EMPTY register (measured) -> `append` raises `PermissionError` -> Refusal naming the register.
  Report `read` reading a directory as 'empty' as an AR-28 analog of the reader (queue line, not this node)."
- **A6 (key 6, key 8; axis 5).** "Edge R18: the skill road (`skills/qa-story/phases/s4.md:27-33`, the conductor runs `story_step
  finish` itself): no driver runs `complete`, so no row is recorded. The critic's `questions[]` are not raised on that road today
  either (grep `--raise` / `--from-handoff` over `skills/` = 0). Named on SIBLING_MAP axis 5, row 'Skill phase <-> driver', and in the
  F-R0 owner question as a road the mechanism does not reach. Queue line with an owner (the skill-retirement node or the qa-story pile)."
- **A7 (key 2).** "`REGISTER_GAP_WHY` = 'the reviewer of the test cases recorded it as a gap in the requirements: no test case can
  check it; it is not a defect of the product' (no stage code or role name: `human-questions.md:60`)."
- **A8 (key 7).** "Census: `register_gaps_write` holds the identity join -> class `xref`; `register_gap_rows` -> `shape` (DoD 6 says
  `shape` for both, contradicting §1)."
- **A9 (key 1, R6).** "A key outside the template row is ignored with a print line, not refused: `handoff_check` never refuses a
  value the role added (`handoff_check.py:1554-1555`). Refusing at the finish would send a form the exit gate passed to a paid
  conductor round."
- **A10 (key 8).** "F-R0 (a) is described as it is built: the road is chosen by the contract's own section at one S4 call site.
  `role_has_bash` is read nowhere on this path. It is therefore not 'form 1 of designer rule 6' until the step is called at every
  acceptor's finish, keyed by the section. The owner question stays, and names the S6/S7 wiring (F-R2 (c)) as the road to form 1."

## Answers per key

**1) Can the critic write the section?** The values road holds. `refs` is generic `register_gaps[].refs[]`, so `as_list` applies:
it is written whole, `register_gaps[0].refs: [R-1, TC-2]` (`handoff_check.py:2571-2582`). `register_gaps[1].title` opens row 1
from the CONTRACT's row 0 (`open_row`, `:2429-2469`). A form holding `register_gaps: []` is opened by the header regex (`:2463-2468`).
The exit side is a **DEFECT** (A1), measured on sc-a2 with the section added to a patched template and `handoff_check.check(...,
fix=False, use_judge=False)`:
- the sample row left as is gives `register_gaps[0].title/.statement/.refs[0]/.missing_prerequisite` "not filled" (4 problems);
- the control `register_gaps: []` gives 0;
- a filled row with the refs placeholder kept gives `register_gaps[0].refs[0]` "not filled".
Cause: `_is_empty_section` (`:1075-1084`) calls `is_placeholder` on the `refs` LIST, whose str is "['<...>']", so the section is not
empty. No hint carries an `OPTIONAL_WORDS` phrase (`handoff.py:35-36`; measured `optional=False` on all four). That is exactly why
`questions` and `findings` are in `handoff_init.EMPTIED` (`handoff_init.py:184-188`). The draft's R4 ("sample row skipped") is true in
the driver step, but the form never gets there: `form_errors` sends the critic back first. On unknown keys: none can arise from the
values road, since only spec paths are written (`:2589-2595` refuses the rest). A role's added key is "never refused" (`:1555`); see A9.
On `test_field_producers`: it walks only tool fields (`null_outcomes.tool_fields`, `test_field_producers.py:100-122`). It is not an
AR-22 reader check, so "green" proves nothing about this field. The real AR-22 proof is J1. Not blocking.

**2) §D.1 vs `append`.** Holds. Every REQUIRED_TEXT and `missing_prerequisite` is supplied (`exploratory_findings.py:325-331`).
`kind` is in KINDS. `refs` is a list of texts. The evidence is a file under the root, judged by `contract.evidence_ref_issue`
(`contract.py:5918-5953`; any path under the root, sha measured at add, `:244-247`). `by` is non-empty. The window comes from code
(`:190-203`). `origin` is not set, so the chain rule is not engaged. The `why_not_a_bug` text: see A7. The field's meaning in the
report ("why it is not a bug:") fits.

**3) Call site and the road of a Refusal.** POSITIONAL holds against the code: `complete` (now `driver_stage_plan.py:807-841`, drift
+6 lines, does not change the edit) runs inside `finish` BEFORE `story_step finish` (`driver_dispatch.py:786-787`, `:845`). The
`if not dispatch` branch sits at `:812-814` and `stage_verdict_known` at `:815`. The road of the Refusal: it propagates out of
`finish` with no `retry`, reaching `handle_refusal`. The head is neither "exit gate for" nor "story_step finish ... (exit 3)"
(`RESUMABLE_HEADS`, `driver_machine.py:39-40`), so the call ends in `conductor_round` (`:603-605`). That is a move: the factory does
not stand (FR-57/P22 hold). It is the same road the refused `questions[]` raise takes today (`driver_stage_plan.py:646-656`, which
sets `exc.dispatch`). But the critic is never resumed, so R8's door "your values file" addresses nobody who reads it (FR-2). And
F-R4 (c) was rejected for a conductor cost that (a) pays as well. Fix: A3. Recovery road: `completion_for` passes the record id the
same way for S2/S3 (`:1042-1049`). S4 takes the same rule (a docstring statement at `:792-793`). D.4 identity makes the replay idempotent.

**4) Identity: loss / duplicates.** No loss road found. All three cases below err toward writing a second line:
- an equal line that was withdrawn or superseded is not active, so the row is recorded again;
- an equal line that is damaged is in `unreadable`, not in `active` (`_scan`, `:119-176`), so the row is recorded again;
- an equal line recorded by another role is skipped. The gap stays in the report under that role's id: AR-27 attribution drifts
  for an equal text, which is negligible.
Silent edge (non-blocking, add to D.5): the conductor withdraws EX-n between a refused finish and its retry, and the retry re-adds
it. Duplicates are bounded by the repair-round cap. Clarify: identity is compared on the NORMALISED row, the one passed to `append`
(placeholder refs dropped, stripped).

**5) Post-finish writers / evidence.** **DEFECT in the premise** (A4). The add happens inside `complete`, before `story_step finish`,
whose `_handoff_check` runs `--fix` (`story_step.py:416-423`, `:2441`). `handoff_check.main` writes the file on every `--fix`
(`handoff_check.py:3103-3104`). A refused finish resumes the critic on its form (`driver_machine.py:568-584`). So "no code writes the
form after the finish" asks the wrong window. Stale sha shows only in `exploratory_findings.py check` (`:473-487`). No code calls it
(grep over `scripts/*.py`, `references`, `hooks`; positive control: `report_facts.py:368` found). `report_facts` does not judge the
sha (`_register`, `:362-379`). Evidence = the role's own form is acceptable against FR-18: a register line is never coverage
(`exploratory_findings.py:3-6`), and the form is the carrier of the row's words.

**6) Edges.** R1-R17 each carry a behaviour and, where testable, a G row. Silent edges:
- the skill road (A6);
- `register_gaps` key outside the template row vs `handoff_check` (A9);
- the withdraw-then-retry case (key 4);
- `stage_acceptor("S4")` empty: the step is skipped together with the record. That world has no acceptance at all. Name it in D.5,
  since it cannot be reached in the package (`stages.json acceptance_by`);
- two critic windows at S4: none exist (one critic per round; R11 covers rounds).

**7) P27/AR-29.** Holds: code judges shape and exact-bytes identity. The census class of the write step is wrong (A8). "No tier above
judges these rows before the report" is acceptable: gate B renders the register to the person (`report_facts.exploratory_gate_parts`),
and the person is the judge of a requirement gap (P20). It is the same as the S6 runner's lines today.

**8) P31 / F-R0.** As built, the second road is keyed by the S4 contract section at an S4-only call site. It is not keyed by a
capability read. So it is a second road and needs the owner's word: the Lead's decision to ask is the correct form (A10). The skill
road is not a third road: it is a road the mechanism does NOT reach (P31 (a) "or not reach it"). It belongs in the same owner
question (A6).

**9) A2/A3 changes.** Complete for the carriers that name the command: charter `:96` (sc-a2), card `role-commands.json:201-209`
(sc-a3), the changelog sentence, X1 (`by` and evidence), and the BROKEN example of `test_role_commands.py` (its `--by
S4-qa-case-critic-1` and its evidence `work/critic-findings.md`: change both, not only `--by`). Also X1's docstring "the S4 case
critic records". The epilog follows the card. TOLD/GUARDED rows stay (still true). F-R7: the `--units` output is the S2 tester's tool
(`brief_pack.py:213`). It was never handed to the S4 critic, so the rewording loses nothing it had. The register's `## Source
obligations` homes are readable by the critic.

**10) Tests.** The table is feasible. `register_gaps_write` needs `task_root`, a `pipeline.json` (window), the form file and the
package template. The G13/G14 completion bound to a stub needs `last_dispatch`, `stages()` (for `stage_acceptor`), the real
`stage_verdict_known`, and stubs for `stage_acceptance_write` and `stage_review_exhausted`. `case_verdict` is static. Gaps:
- G11 is wrong as written (A5, measured);
- `test_driver_layers` L1 refuses a def with no row (`test_driver_layers.py:716`, `:1291`), so the three new names need rows (A2);
- A1 needs its own test row (the exit check over the emptied copy);
- import the methods the way other tests reach driver parts. The builder reads `driver-layers.json` "tests that read the driver
  source" first.
No quarantined file is edited (`test_repair_route.py` is avoided, correctly). Slow/fast split as stated.

**11) Byte budget.** `role_load.py --all --json` on sc-a2 ran in 0.3 s: qa-case-critic total 74770 B, 18693 / 16333 tokens. The
ratchet is tight (slack is not used: `test_role_load.py:539`). Computed byte delta of the F-R6 (b) wording (a count, not a rerun on a
modified tree): A2 line 564 B, short charter line 198 B, short section with a one-line comment 394 B, net **+28 B (about +7 tokens)**.
A1's ", or omit" adds about 8 B more. So net <= 0 is NOT reached as drafted; the Lead's fallback (a named raise) applies, or trim one
more sentence. FR-38 holds: the form is a counted layer (`form 7081 handoffs/s4-case-critic-to-designer.yaml`), and the template row
names every field before the work.

**12) Feasibility / cut.** `git merge-tree fd30668 91ab1f3`: CONFLICT in `references/role-load.json`. Main changed the tester row
12630->12670 (and others); A2 changed 12630->12636. `merge-tree fd30668 c8a1ec2`: clean. The spec's "clean: critic answer 7" covers
only A2xA3. Owns are insufficient (A2). A1c owns the `driver_stage_plan.py` T2 rule (about `:904`), and this node is placed after A1c,
in another function: no textual overlap expected. Wave 8-10 changed `driver_stage_plan.py` +14/-8 (FV1-22 N2 acceptance-write
dispatch), and the builder re-reads it.

**13) Class / §C / axes.** Spot-check holds: the 3 no-shell roles (positive control: 9 Bash lines over the same glob). The card
`roles` of the four drift rows match role-commands.json (read as JSON). CL-NS as sketched is a data join (FR-12 kept) only if the
`no_shell_road` key is added. `plan_row.py` today carries that road in prose only, so CL-NS must add the key there in the same node.
Axis enumeration: axis 5 is not honest. It names the S6/S7 twins but not the axis-5 rows "A role without Bash raises a before/now
question" (`SIBLING_MAP.md:149`, "a third role without Bash ... joins this row") and "Skill phase <-> driver" (`:128`). Add both lines
(A6) and append register_gaps to row :149 in the node's commit.

## DUPLICATION AND CONSISTENCY
None blocking in the plan. The `register_gap_rows` + identity mirror `question_register.raise_from_handoff` by design (AR-15 named).
The draft drops the "refuse a changed replay" half of that sibling (F-R3 (a) vs (c)), and says so. Inconsistencies found: DoD 6 vs §1
census class (A8); the R6 refusal vs handoff_check's "never refused" (A9).

## CODE QUALITY
Plan-level: the pure helper plus a thin method is the right split. The print lines go through stdout as `stage_acceptance_write`'s
steps do. Nothing else to judge before code.

## ONE ROAD (critic-diff-brief item 12)
Two residuals of the class, both routed by A6/A10 to the owner question and a node: the S4-only call site (S6/S7 forms not wired),
and the skill road not reached. Neither is a silent line.

## Trail
Read: the spec (whole), the t-717 verdict :1-80, `handoff_check.py` :1049-1084, :1400-1650, :2150-2290, :2429-2737, :3060-3119;
`handoff.py` :31-36, :395-705; `handoff_init.py` :183-219; `driver_stage_plan.py` :636-841, :1017-1061; `driver_dispatch.py`
:340-370, :783-887; `driver_machine.py` :39-45, :189-284, :441-605, :1520-1563; `driver_core.py` :100-125; sc-a3
`exploratory_findings.py` :1-494; `contract.py` :5918-5953; `report_facts.py` :350-434; `story_step.py` (grep `handoff_check`/`--fix`);
`hooklib.py` :600-625; sc-a2 `handoffs/s4-case-critic-to-designer.yaml` whole; the A2 and A3 diffs; `skills/qa-story/phases/s4.md`
:20-49; `SIBLING_MAP.md` headings and :111-158; `critic-diff-brief.md` item 12; `test_field_producers.py` :1-130;
`test_driver_layers.py` :425-450 plus greps; `driver-layers.json` (keys, `allowed_importers`); `artifact-writers.json`,
`gate-registry.json` (grep); `brief_pack.py` :200-224, :3810-3835; `human-questions.md` (grep).
Reruns: listed in the JSON block.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "A1: the untouched register_gaps sample row (refs is a nested list, so _is_empty_section is False) and a filled row without refs are refused at the exit as not filled; add register_gaps to handoff_init.EMPTIED and mark refs optional (measured on sc-a2)",
    "A2: owns miss scripts/tests/fixtures/driver-layers.json (test_driver_layers L1) and the role-load.json tester/strategist rows; merge of 91ab1f3 into fd30668 conflicts in role-load.json",
    "A3: the Refusal is not a resumable head, so it goes to conductor_round and the critic is never resumed; the door must address the conductor and the Refusal must carry dispatch",
    "A4: R16/F-R5 premise false: story_step finish runs handoff_check --fix (always writes) after the add, and a refused finish resumes the critic on its form; the sha can go stale",
    "A5: G11 impossible as written: read() of a directory returns the empty register and append raises PermissionError (OSError), which step 4 does not catch"
  ],
  "fixes": [
    "A1 add register_gaps to handoff_init.EMPTIED for s4-case-critic-to-designer, refs placeholder with 'or omit', and a test row",
    "A2 extend owns: driver-layers.json rows for the three new names; role-load.json tester and strategist rows re-measured at merge",
    "A3 Refusal(text, dispatch=dispatch) with a conductor-addressed door (handoff_check --set register_gaps[i].<field>=...); strike F-R4's cost argument",
    "A4 replace R16 by the honest residual (stale sha possible, check-only, report unaffected) and pin re-fix byte equality",
    "A5 catch OSError from append; reword G11; queue the reader's directory-as-empty analog",
    "A6 edge R18 skill road not reached, named on axis 5 rows :128 and :149 and in the owner question",
    "A7 REGISTER_GAP_WHY without stage code or role name",
    "A8 census class xref for register_gaps_write",
    "A9 ignore-with-print an extra key instead of refusing it",
    "A10 describe F-R0 (a) as contract-keyed at one call site, not capability-keyed; S6/S7 wiring as the road to form 1"
  ],
  "class_completeness": "Siblings by the map: axis 5 rows 'A role without Bash raises a before/now question' (SIBLING_MAP:149) and 'Skill phase <-> driver' (:128) are not named in the draft's axis block. The skill road is not reached, the same as today's questions[] raise (grep --raise/--from-handoff over skills = 0). S6/S7 acceptor forms are not wired (F-R2). Queue them with owners (A6, A10). Analog: exploratory_findings.read reads a directory as an empty register (AR-28 analog, queue line). raise_from_handoff non-list analog already queued by the Lead.",
  "trail": {
    "read": [
      "docs/tasks/specs/20261114-sc-f7-recut-register-gaps-spec.md",
      "docs/tasks/specs/reviews/20261114-stage-critics-topic-a-critic.md",
      ".claude/worktrees/read-main/ai-packages/qa-factory/scripts/handoff_check.py",
      ".claude/worktrees/read-main/ai-packages/qa-factory/scripts/handoff.py",
      ".claude/worktrees/read-main/ai-packages/qa-factory/scripts/handoff_init.py",
      ".claude/worktrees/read-main/ai-packages/qa-factory/scripts/driver_stage_plan.py",
      ".claude/worktrees/read-main/ai-packages/qa-factory/scripts/driver_dispatch.py",
      ".claude/worktrees/read-main/ai-packages/qa-factory/scripts/driver_machine.py",
      ".claude/worktrees/read-main/ai-packages/qa-factory/scripts/driver_core.py",
      ".claude/worktrees/sc-a3/ai-packages/qa-factory/scripts/exploratory_findings.py",
      ".claude/worktrees/read-main/ai-packages/qa-factory/scripts/contract.py",
      ".claude/worktrees/read-main/ai-packages/qa-factory/scripts/report_facts.py",
      ".claude/worktrees/read-main/ai-packages/qa-factory/scripts/story_step.py",
      ".claude/worktrees/read-main/ai-packages/qa-factory/scripts/hooklib.py",
      ".claude/worktrees/sc-a2/ai-packages/qa-factory/handoffs/s4-case-critic-to-designer.yaml",
      ".claude/worktrees/read-main/ai-packages/qa-factory/skills/qa-story/phases/s4.md",
      ".claude/worktrees/read-main/ai-packages/qa-factory/scripts/tests/test_field_producers.py",
      ".claude/worktrees/read-main/ai-packages/qa-factory/scripts/tests/test_driver_layers.py",
      ".claude/worktrees/read-main/ai-packages/qa-factory/scripts/tests/fixtures/driver-layers.json",
      "docs/SIBLING_MAP.md",
      "docs/tasks/critic-diff-brief.md"
    ],
    "reruns": [
      {"command": "python -B (stdin probe) handoff_check.check on sc-a2 form with register_gaps added to a patched template, fix=False, use_judge=False", "result": "sample row kept: 4 not-filled problems on register_gaps[0].*; register_gaps: [] -> 0; filled row with refs placeholder -> register_gaps[0].refs[0] not filled; _is_empty_section False, only_template True, all four fields optional=False"},
      {"command": "python -B sc-a2/scripts/role_load.py --all --json", "result": "rc 0 in 0.3 s; qa-case-critic total 74770 B, tokens 18693, process 16333 (equal to the ratchet rows)"},
      {"command": "python -B (stdin) byte count of A2 line 96 vs F-R6 (b) wording", "result": "564 B removed, 198 B line + 394 B short section added: net +28 B (about +7 tokens)"},
      {"command": "git -C read-main merge-tree --write-tree --name-only fd30668 91ab1f3; same with c8a1ec2", "result": "91ab1f3: CONFLICT (content) in references/role-load.json; c8a1ec2: clean"},
      {"command": "python -B (stdin) EF.read and EF.append with work/exploratory-findings.jsonl as a directory", "result": "read -> empty register; append -> PermissionError [Errno 13] (OSError, not ValueError)"},
      {"command": "grep '^tools:' agents/*.md (sc-a3), case-insensitive bash count", "result": "3 without Bash (case-critic, case-designer, test-strategist), 9 with Bash (positive control)"},
      {"command": "grep exploratory_findings callers / 'check' invokers over scripts, references, hooks", "result": "no code invoker of 'exploratory_findings.py check'; positive control report_facts.py:368 import found"}
    ]
  }
}
```
