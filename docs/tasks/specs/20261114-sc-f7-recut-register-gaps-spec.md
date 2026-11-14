# F7 re-cut — the S4 case critic's register gaps reach the test report through its form (DRAFT, designer)

Topic: "stage critics S2/S3 removed" (topic A). Parent spec: `docs/tasks/specs/20261113-stage-critics-s2-s3-removed-spec.md`
(§A.2.4, A2, A3, §F F7). Trigger: critic t-717 finding B1 (`docs/tasks/specs/reviews/20261114-stage-critics-topic-a-critic.md:20-37`).
Lead decision (owner away, reversible): road (c') — the critic WRITES rows in a new optional section of its own form; the DRIVER records
each row in the findings register at the S4 critic finish; one writer of the register stays; `report_facts` unchanged; no Bash for the
critic. Status: DRAFT for Lead acceptance. Forks are §F (returned, not decided); the node in §N is written on the recommended options so
it is executable before the answers (PROJECT.md «Командная работа» п. 11). Line numbers are of `.claude/worktrees/read-main` (origin/main)
unless a worktree is named; the builder re-reads them on its base (wave 8 edits `driver_stage_plan.py` around `stage_acceptance_write`).

## §0 The fact that forces the re-cut (verified on the carriers)

- `agents/qa-case-critic.md:4` `tools: Read, Grep, Glob, Write, Edit` — no Bash (sc-a3 and read-main alike).
- The brief tells it so: `brief_pack.TOOLING_NO_SHELL["qa-case-critic"]` = "your findings file is read by code at the exit gate (the
  roll-call); you run nothing" (`brief_pack.py:385-387`, sc-a3) under `NO_SHELL_HEAD` "The scripts of the plugin are run for you by the
  orchestrator and the exit gate" (`:370-373`).
- A2 (sc-a2, 91ab1f3) `agents/qa-case-critic.md:96` tells it to run `exploratory_findings.py add ...`; A3 (sc-a3) adds `qa-case-critic`
  to `references/role-commands.json:201-209` `exploratory_findings.py add` `roles`. Neither road can be walked by the role.
- The critic fills its form by a values file when it has no shell: "one Write of `<dispatch>.values.yaml` (no Bash; while it waits,
  Edit of the form is refused)" (`references/slices/qa-case-critic/common-rules.md:58-62`). A list row is written by path
  (`questions[0].question: ...`), resolved against the CONTRACT's template rows (`handoff_check._template_nodes`, `:2155`). So a new form
  section exists for the role only if the contract template carries it.

## §1 Invariants touched (designer rule 1), owners and census classes

| AR-n | how it is touched | how kept | change check written into the DoD |
|---|---|---|---|
| AR-14 one writer | the driver adds lines to `work/exploratory-findings.jsonl` | only through `exploratory_findings.append` (the one writer, `exploratory_findings.py:277`; the driver already does this at gate B, `driver_machine.py:2799`) | grep `exploratory-findings.jsonl` and `append_jsonl_line(` over `scripts/*.py` outside tests: no new writer site |
| AR-13 one reader | the driver reads the register to skip a row already recorded | only through `exploratory_findings.read` (`:179`) | same grep for `exploratory-findings.jsonl` opens; positive control `report_facts.py:368` |
| AR-22 producer/reader | new form field `register_gaps[]` | reader: the new driver step; the register lines it writes have the existing reader `report_facts._exploratory`/`_r_exploratory` (`report_facts.py:394`, `:3877`) | `test_field_producers.py` green (the field is produced by a role and read by code) |
| AR-23 empty outcome | an optional list | declared in the contract's comment above the section, the `questions` precedent (`s4-case-critic-to-designer.yaml:129` "`[]` is a legal answer") | key-presence of the declaration sentence |
| AR-10 / FR-38 told before the work | the driver step judges the rows' shape and the writer judges their content | the template row names every field (the skeleton the values file fills) + one charter line; no brief/ahead-card change (fork F-R6) | `role_load.py --all --json` before/after attached |
| AR-11 / FR-56 tools | the critic is NOT given Bash | `tools:` line unchanged | key: `tools: Read, Grep, Glob, Write, Edit` still in the charter |
| AR-9 / FR-1 / FR-2 refusal | a refused row | one refusal that names every shape problem of the section at once, the expected row, and a door the critic can use (its values file) | table rows R5-R8 below |
| AR-25 a returned state has a move | the S4 state "a remainder exists" (B1: no move today) | the move: a form row, recorded by the driver | row R1 |
| AR-27 a gap reaches the report under its owner | the gap line | `recorded_by` = the critic's dispatch id; the report's coverage-gap list (`report_facts.py:3870-3872`) | joint row J1 |
| AR-28 an unknown is never a pass | an unreadable register / form | a refusal on the standard road, never "no gaps" | rows R9, R10 |
| AR-29 code judges data | the new driver step | judges shape only (list, mapping, text, known keys) and an exact-bytes identity; never whether a row is a register gap or whether two rows mean the same gap | census row below |
| AR-20 ratchets | `role-load.json` `qa-case-critic` rows move | named raise or a net-zero text (fork F-R6) | list every row raised: key, old -> new, reason |
| AR-15 one survivor | the "raise a form section into a register" pattern | mirrors `question_register.raise_from_handoff` (`question_register.py:1591-1627`): placeholder row skipped, all shape problems named at once, idempotent replay | named on axis 34 / axis 5 lines below |

Checks the change adds (owner it serves, census class):
- `register_gaps` is a list, each row a mapping, each field text, refs a list of texts, no key outside the template row — class **shape**,
  owner **data**, roles on its path: `qa-case-critic`, `conductor`.
- "this exact row is already an active line" (identity, §D.4) — class **xref** (a join of the form against the register), owner **data**.
- The writer's existing checks (kind, required texts, `missing_prerequisite` for a `coverage_gap`, evidence under the story) — unchanged
  census rows `judgment-census.json:376-385` (shape/xref, data).
- What is a register gap, what its statement and missing prerequisite say — **judgment**, the case critic's; seen and judged by the person
  in the test report (and by gate B, which renders the register, `report_facts.exploratory_gate_parts` `:3936`). No code check is added
  on meaning (AR-29). NOTE for the Lead: no tier above the S4 critic judges these rows before the report; the same holds for the S6
  runner's own register lines today. Not a new gap; named so the acceptor does not assume one.

## §D Design (on the recommended options of §F)

### D.1 The form section (A2's form file; `required: false`)

In `handoffs/s4-case-critic-to-designer.yaml`, after `questions:` (`:130-142` on sc-a2), a new top-level list, with its declaration:

```yaml
# A register gap the cases cannot carry (no case can hold it, or only the person can settle it): one row per gap, written once, when
# you first find it. The driver records each row in the findings register at your finish and it reaches the test report. `[]` (or no
# section) is a legal answer: no such gap. A gap only the person can settle also goes in `questions`.
register_gaps:
  - title: "<the gap in one line>"
    statement: "<the register line, quoted, and what no requirement holds>"
    refs:
      - <R-n or TC-n the gap stands against>
    missing_prerequisite: "<what would close it: a requirement, an answer, a source>"
```

Fields against what `exploratory_findings.append` requires (`exploratory_findings.py:305-336`), every argument the driver passes and its source:

| writer field | required by the writer | value | source |
|---|---|---|---|
| `op` | yes (`_closed("op")` `:295`) | `add` | driver constant |
| `kind` | yes (`KINDS` `:36`) | `coverage_gap` | driver constant (the section IS the classification) |
| `title` | yes (`REQUIRED_TEXT` `:57`) | the row's `title` | role (form) |
| `statement` | yes | the row's `statement` | role (form) |
| `why_not_a_bug` | yes | `REGISTER_GAP_WHY` = "the S4 case critic recorded it as a gap of the requirements register that no case can carry; it is not a product defect" | driver constant (fork F-R1) — precedent: the driver writes this field at gate B (`driver_machine.py:2794`) |
| `missing_prerequisite` | yes for `coverage_gap` (`:330-331`) | the row's `missing_prerequisite` | role (form) |
| `refs` | optional, list of non-empty texts (`:332-334`) | the row's `refs` (placeholder items dropped; absent -> `[]`) | role (form) |
| `evidence_refs` | yes, >= 1 file under the story (`:335-336`, `_judge_refs` `:234`) | `[{"path": "work/handoffs/<dispatch>.yaml"}]` — the form itself; sha256 measured by the writer at add time | driver (fork F-R5: NOT the findings file) |
| `by` (-> `recorded_by`) | yes, non-empty (`:365-367`) | the critic's dispatch id (the `dispatch` of the completion) | driver |
| `origin` | optional | NOT set (no investigation target; `origin.target` is read by S7, `driver_stage_s7.py:684`) | — |
| `oracle_status`, `verification_status`, `probe` | defaulted by the writer (`none`, `unverified`, null) | not passed | writer |
| `window`, `recorded_at`, `id` | set by code (`CODE_SET` `:56`) | not passed | writer (`pre-gate-a` before gate A, `_window` `:190-203`) |

The report renders a coverage-gap line as: statement — status words — "missing: <missing_prerequisite>" — "why it is not a bug: <...>"
(`report_facts._exploratory_item` `:3850-3874`); `title` is read by the gate B question lines only (`:3911`). So every role field has a reader.

### D.2 Told before the work (FR-38, AR-10)

- Skeleton: the template row above IS the field-level requirement (the values file paths `register_gaps[0].title` etc. resolve against it).
- Charter (A2's line `:96` on sc-a2) is REPLACED by: "A register gap the designer cannot close in the cases (no case can carry it, or only
  the person can settle it) goes once, when you first find it, as a row of `register_gaps` in your form: title, statement (the register
  line and what is missing), refs, missing_prerequisite (what would close it); the driver records it and it reaches the test report. A gap
  only the person can settle also goes in `questions[]`." — keeps A2's DoD key "it reaches the test report"; names no command (FR-39).
- Brief / ahead card: unchanged (fork F-R6). `TOOLING_NO_SHELL["qa-case-critic"]` stays true ("you run nothing").
- Byte cost — NOT MEASURED here (this draft had no shell; estimate, not verified): the section with its comment ~ 560 bytes, the new charter
  line ~ 400 bytes, the removed A2 line ~ 590 bytes: net ~ +370 bytes, ~ +90 tokens on `ratchet_tokens` and `process_ratchet_tokens`
  `qa-case-critic` (A2 tip: 18693 / 16333, `role-load.json:15`, `:29` on sc-a2). `role_load.py` counts the form as a layer ("the heaviest
  handoffs/<contract>.yaml of the role", `role_load.py:442-457`), so the form section counts. `ROLE_BRIEF_BYTES_MAX qa-case-critic`
  (6580 after A1a; 6130 at sc-a2 `test_brief_pack.py:2365`) does not move: the brief text is unchanged. The raise is fork F-R6.

### D.3 The driver writer — place and order

New method `DriverStagePlan.register_gaps_write(self, stage: str, dispatch: str) -> None` in `scripts/driver_stage_plan.py`, plus a pure
helper `register_gap_rows(data, fields) -> (rows, problems)` in the same file (the testable core; `fields` = the template row's keys).

Call site (fork F-R2, recommended (b)): inside `s4_critic_completion.complete` (`driver_stage_plan.py:801-835`), in the
`if self.stage_acceptor("S4"):` block, AFTER the `if not dispatch:` branch (`:806-808`) and BEFORE `if not self.stage_verdict_known(form)`
(`:809`) — so before `stage_acceptance_write("S4", dispatch)` (`:811`) and before the finish (`driver_dispatch.finish` calls `complete`
first, `driver_dispatch.py:771-772`), and long before the roll-call (`critic_rollcall.py --apply-fixes` in `s4_after_critic`, `:759-763`,
which runs after the finish and neither reads nor writes the register: grep `exploratory` over `critic_rollcall.py` = 0, positive control
`apply.fixes` = 12 in the same file).

POSITIONAL INVARIANT: (1) no acceptance record (`stage_done.py --acceptance`) is written, and no seam (`stage_review_exhausted`) is
called, over a form whose `register_gaps` were refused — the refusal comes first, as the refused `questions[]` raise comes before the record
today (`:646-651`); (2) a row is recorded whatever the verdict word, readable or not (accept, reject, partial, an unknown word); (3) a
finish with no dispatch id records nothing (no form can be named) and goes on to its existing seam unchanged.

Steps of `register_gaps_write(stage, dispatch)`:
1. `form = self.task_root / "work/handoffs" / f"{dispatch}.yaml"`; not a file -> return (nothing to read; the verdict branch that follows
   handles the missing form as today).
2. Parse with `handoff.parse(...).data` (the reader `stage_verdict_known` uses, `:686`). A form that cannot be parsed -> return: the
   following `stage_verdict_known` sends it to the seam (`unreadable=True`) as today. (No refusal here: one problem, one road.)
3. `rows, problems = register_gap_rows(data, fields)`; `fields` = keys of the contract template's `register_gaps[0]` row
   (`handoff.template("s4-case-critic-to-designer")`; closed variety read from data, AR-1/FR-13). `problems` non-empty -> ONE `Refusal`
   naming every problem (§D.5). Nothing is written.
4. `register = exploratory_findings.read(self.task_root)` (OSError -> Refusal, §D.5 R10). For each row in form order: if an ACTIVE line
   equals it by identity (§D.4) -> print `S4: register_gaps[<i>] of work/handoffs/<d>.yaml is recorded already as <EX-n>; not again` and
   skip; else `exploratory_findings.append(self.task_root, line, by=dispatch)` and print `S4: register_gaps[<i>] recorded in the findings
   register as <EX-n> (coverage gap; it reaches the test report)`. A `ValueError` from the writer -> Refusal (§D.5 R8); rows already
   written stay (error direction below).
5. Returns None. No `OpenWork`, no change to the completion's return value.

ERROR DIRECTION (the one `owe_row` states, `driver_runner.py:267-268`): a duplicate line is allowed, a lost row is not. The identity skip
may err only toward writing a second line, never toward skipping a row that has no equal active line.

### D.4 Identity (idempotence on a repeated finish / resumed run / recovery road)

Recommended (fork F-R3 (a)): a row is "recorded already" when an ACTIVE line of `read()["active"]` has `kind == "coverage_gap"` and
`title`, `statement`, `missing_prerequisite` equal to the row's (after `.strip()`) and `refs` equal as lists — exact bytes, any
`recorded_by`. No meaning is compared (AR-29). Why it holds on every road: a refused finish retried, `completion_for` (recovery road,
same `dispatch_id`), a resumed run — all re-read the same form, so every row already written is skipped.

### D.5 Edges (each with its invariant)

| id | edge | behaviour | INVARIANT |
|---|---|---|---|
| R1 | rows present, verdict `ok`/accept | each row recorded once; then the record and finish as today | a gap is recorded on accept too: the verdict does not gate the remainder |
| R2 | rows present, verdict `concerns`/reject (round left, last round, or exhausted) | recorded BEFORE the record / OpenWork / seam | no return value of `complete` changes |
| R3 | section absent, `[]`, or `null` | nothing written, nothing printed | AR-23: the empty outcome is the declared one; no line in the register means no gap |
| R4 | the template's placeholder row left as is (`handoff.only_template(row)`, `handoff.py:409`) | skipped as "no row" (the `questions` precedent F1 B-11, `question_register.py:1608-1612`); index of later rows stays the form's own | a sample row is never recorded as a gap |
| R5 | `register_gaps` a mapping, a number, or a non-placeholder string (e.g. `none`) | Refusal: "`register_gaps` is a <type>; expected a list of rows {title, statement, refs, missing_prerequisite}, or [] for no gap" | never read as "no gaps" (FR-4: no silent pass). NOTE: the sibling `raise_from_handoff` reads a non-list `questions` as [] in silence (`question_register.py:1606-1607`) — reported as an analog, not widened (§S) |
| R6 | a row that is not a mapping, a key outside the template row, a field that is not text, `refs` not a list or an item not text | ONE Refusal listing every problem as `register_gaps[<i>].<field>: <problem>` | all problems at once (FR-1), nothing written on a shape problem |
| R7 | a field still holding its placeholder in a row that has a real value elsewhere | the field is treated as absent (not passed); `refs` placeholder items dropped | a placeholder text never reaches the register; a required field absent is the writer's refusal (R8) |
| R8 | the writer refuses a row (`ValueError`: empty title/statement/missing_prerequisite, ...) | Refusal: "S4: register_gaps[<i>] of work/handoffs/<d>.yaml was not recorded in the findings register: <writer text>. Expected a row {title, statement, refs, missing_prerequisite} (the writer's `--title`, `--statement`, `--refs`, `--missing-prerequisite` are these fields). Door: correct that row in your form (your values file), or delete it and keep the gap in `questions[]`; rows recorded already are not recorded again." Rows before it stay written. | never a silent drop; the next finish skips the written rows (D.4) and the factory is not stopped: the Refusal takes the standard road the refused `questions[]` raise takes at the same site (`:647-649`). First-error-only of the writer is the known residual N7 (its own node) |
| R9 | the form cannot be parsed | no gap step; `stage_verdict_known` sends it to the seam as today (`:809-810`) | one problem, one road |
| R10 | the register cannot be read (`OSError`) | Refusal "the findings register work/exploratory-findings.jsonl cannot be read (<why>); the register gaps of <form> were not recorded" | AR-28: never "nothing recorded yet"; damaged LINES are not an OSError (`read` returns them as `unreadable`) and do not stop the step |
| R11 | a repair round re-dispatches the critic | its NEW form's rows are recorded; a row equal to an active line (D.4) is skipped; round-1 lines stay | code never withdraws or corrects a line on the critic's silence; withdrawal is the conductor's existing door (`exploratory_findings.py withdraw`) |
| R12 | the same gap reworded in a later round | a second line (both shown) | duplicate allowed, loss never; whether two texts mean one gap is a role/person judgment (AR-29) |
| R13 | a finish with no dispatch id (`:806-808`) | no gap step; seam as today | no form is guessed |
| R14 | after gate A answered (a rework back to S4) | recorded; the writer gives window `s5-s8` | no new window value |
| R15 | very long texts | passed whole; no limit introduced (in-process call: no command-line ceiling — fork F-R8) | nothing truncated |
| R16 | the form's bytes change after the add (evidence sha) | evidence = the form, which no code writes after the finish (writers of forms: `handoff_check.py`, `handoff_init.py`, before the finish — ESTIMATE: grep of `set_value(` callers; no post-finish writer found, not proven) | `exploratory_findings.py check` never reports the S4 line stale on a story where nothing rewrote the form |
| R17 | dry gates (`--dry-run`) | unchanged behaviour (the step is stage work, like `stage_acceptance_write`) | dry concerns gate answers only (`driver_core.py:445`) |

TEMPORAL: the section does not exist before this node. World before (a form written by an older template, or an in-flight story resumed
across the upgrade): no `register_gaps` key -> R3, nothing written. World after: the template carries it. The move that creates it: this
node's commit.

### D.6 What changes in A2 and A3

A2 (sc-a2, 91ab1f3): the charter line `:96` replaced (D.2); the form gains `register_gaps` (D.1); `role-load.json` `qa-case-critic` rows
re-measured (fork F-R6); everything else of A2 stays (all its other keys fit per critic answer 1). `design/role-rules.json`: no anchor of
the critic stands in line `:96` (A2 report: "none stood in a removed line") — builder re-greps; if an anchor sat there, the row moves with
the line.
A3 (sc-a3, c8a1ec2):
- `role-commands.json` `exploratory_findings.py add` (`:201-209`): `roles` = [`qa-runner`, `qa-failure-analyst`] (both have Bash:
  `qa-runner.md:4`, `qa-failure-analyst.md:4`); the `input` drops the critic-only sentence "A requirement-register gap the case designer
  cannot close is a coverage_gap line whose evidence is your own findings file under work/test-cases/. Record it once, when you first find
  it;" and keeps "a line with no evidence file is refused, nothing is written." The epilog follows the card automatically (`epilog(SCRIPT)`,
  `exploratory_findings.py:412`).
- `exploratory_findings.py` epilog line (A3): stays (the card stays for runner/analyst; `test_role_commands.py:1070-1081` needs it).
- `test_role_commands.py` BROKEN row and example (A3, +10): stay; the builder checks the example's `--by` is not a `S4-qa-case-critic-*` id
  (if it is, it becomes an `S6-qa-runner-*` id).
- `test_validator_class.py` TOLD `("file", "references/role-commands.json")` and GUARDED `("open", "append raises the first ValueError only
  ...")` for `exploratory_findings.py add`: STAY (the card still exists; N7 still open).
- `test_exploratory_findings.py` X1: keeps its writer half and its report half; its `by="S4-qa-case-critic-1"` stays TRUE (the driver
  records with the critic's dispatch id); its evidence becomes the critic's form `work/handoffs/S4-qa-case-critic-1.yaml` (fork F-R5).
  X2 stays.
- changelog fragment: A3's sentence rewritten: the critic writes the gap in its form, the driver records it.

## §N Node(s)

Recommended (fork F-R9 (a)): ONE builder node on top of A2+A3 merged together. Reason: A2 and A3 must land together anyway (FR-39, critic
answer 7), and the re-cut edits files of both (the charter line of A2, the card of A3) plus the driver — two nodes would share the A2/A3
merge and order themselves anyway. Base: `origin/main` after A1a+A1b+A1c (and wave 8) merged; then `git merge wip/sc-a2` (91ab1f3) and
`git merge wip/sc-a3` (c8a1ec2) into the node branch (clean: critic answer 7, `merge-tree` c8a1ec2 x 91ab1f3 rc 0); then the re-cut commit.

### F7-RC — register gaps through the critic's form; A2/A3 re-cut  [builder -> critic, topic A]
given: this spec (§0, §1, §D, §F recommended options); `ai-packages/qa-factory/design/factory-rules.md` whole; `plans/builder-rules.md`;
`docs/TESTING.md`; the critic verdict `docs/tasks/specs/reviews/20261114-stage-critics-topic-a-critic.md` (B1, N7); the A2 and A3
reports (`.claude/worktrees/sc-a2/docs/tasks/specs/reports/20261114-sc-a2-report.md`, `.claude/worktrees/sc-a3/docs/tasks/specs/reports/20261114-sc-a3-report.md`);
in the package: `scripts/exploratory_findings.py` (`append` `:277`, `read` `:179`), `scripts/driver_stage_plan.py` (`s4_critic_completion`
`:785-835`, `stage_acceptance_write` `:641-651`), `scripts/question_register.py` (`raise_from_handoff` `:1591-1627`, the sibling),
`scripts/handoff.py` (`only_template` `:409`, `is_placeholder` `:662`, `template`), `scripts/driver_machine.py` (`_confirm_exploratory`
`:2769-2800`, the in-process writer precedent), `scripts/report_facts.py` (`_exploratory_item` `:3850-3874`)
owns:
C:\QAFactory\forge-repo\.claude\worktrees\sc-f7rc\ai-packages\qa-factory\handoffs\s4-case-critic-to-designer.yaml (the `register_gaps` section and its comment only)
C:\QAFactory\forge-repo\.claude\worktrees\sc-f7rc\ai-packages\qa-factory\agents\qa-case-critic.md (the A2 register-remainder paragraph `:96` only; plus the `branch_accounting --units` technique line only if the Lead picks F-R7 (a))
C:\QAFactory\forge-repo\.claude\worktrees\sc-f7rc\ai-packages\qa-factory\references\role-load.json (the two `qa-case-critic` rows only)
C:\QAFactory\forge-repo\.claude\worktrees\sc-f7rc\ai-packages\qa-factory\references\role-commands.json (the `exploratory_findings.py add` entry: `roles` and `input` only)
C:\QAFactory\forge-repo\.claude\worktrees\sc-f7rc\ai-packages\qa-factory\scripts\driver_stage_plan.py (`s4_critic_completion` - the one call line; new `register_gaps_write`, new `register_gap_rows`, new constant `REGISTER_GAP_WHY`)
C:\QAFactory\forge-repo\.claude\worktrees\sc-f7rc\ai-packages\qa-factory\scripts\tests\test_exploratory_findings.py (X1 evidence path; new key function `key_f7rc` with table G1-G12 and joint row J1)
C:\QAFactory\forge-repo\.claude\worktrees\sc-f7rc\ai-packages\qa-factory\scripts\tests\test_role_commands.py (the example's `--by` only, if it names an S4 critic)
C:\QAFactory\forge-repo\.claude\worktrees\sc-f7rc\ai-packages\qa-factory\scripts\tests\test-layers.json (the `covers` of the `test_exploratory_findings.py` keep row only, if `--witness-for driver_stage_plan.py` does not print it)
C:\QAFactory\forge-repo\.claude\worktrees\sc-f7rc\ai-packages\qa-factory\scripts\tests\fixtures\judgment-census.json (new rows for the new units only, as the census test prints; `ratchet` values only as printed)
C:\QAFactory\forge-repo\.claude\worktrees\sc-f7rc\ai-packages\qa-factory\changelog.d\stage-critics-s2-s3-removed.md (the A3 sentence only)
non-goals: Bash for the critic; `exploratory_findings.py` code (writer, validator, window rule, first-error-only — N7 is its own node);
`report_facts.py`; `brief_pack.py` (`TOOLING_NO_SHELL`, ahead cards: unchanged, F-R6); `stage_acceptance_write` (F-R2 (b)); the S6/S7
consumer completions (`driver_stage_s6.py`); `question_register.py` (its non-list analog, §S); `test_validator_class.py` (rows stay);
`critic_rollcall.py`; every other charter, form row and card row; the delivery verdict (a register line never adds to proven,
`exploratory_findings.py:3-6`).
handoff: report at `C:\QAFactory\forge-repo\.claude\worktrees\sc-f7rc\docs\tasks\specs\reports\20261114-sc-f7rc-report.md` + the branch head; the critic gets the diff and this spec.
edges: §D.5 R1-R17 (each with its invariant), the POSITIONAL invariant of §D.3, the ERROR DIRECTION of §D.3, TEMPORAL of §D.5.
DoD:
1. Behaviour table in `test_exploratory_findings.py` (fast, keep row `test-layers.json:1651`), function `key_f7rc`, ONE parameterised
   table over `register_gap_rows` + `register_gaps_write` on a driver stub (a minimal object carrying `task_root` with the real method
   bound; no driver process, no subprocess per row; world built once): G1 rows recorded (R1) — `kind coverage_gap`, `recorded_by` the
   dispatch, `evidence_refs[0].path` the form, `why_not_a_bug` = `REGISTER_GAP_WHY`, window `pre-gate-a`; G2 absent / `[]` / null -> no
   file written (R3); G3 placeholder row skipped, a real row after it recorded with its own index in the print (R4); G4 `register_gaps:
   none` / a mapping -> Refusal, register bytes unchanged (R5); G5 two rows with shape problems -> ONE Refusal naming both, nothing written
   (R6); G6 placeholder field -> absent -> the writer's refusal text names `--missing-prerequisite` and the row index (R7, R8); G7 rows 0
   ok, 1 refused -> row 0 written, Refusal names row 1; the second call after fixing row 1 writes ONLY row 1 (R8 + D.4); G8 the same form
   twice -> one line per row (idempotence, recovery road); G9 a later dispatch with one equal and one new row -> only the new row (R11);
   G10 reworded row -> a second line (R12); G11 register path is a directory -> Refusal naming the register (R10); G12 after gate A
   answered -> window `s5-s8` (R14). Each row id names its case (P16).
2. Joint row J1 (stage joint, form -> register -> report): a form with one `register_gaps` row -> `register_gaps_write` -> the report's
   reader (`report_facts._exploratory`, as X1 does) counts one gap, and `_r_exploratory` text holds the statement and "missing: <...>".
3. Call-site row: in `s4_critic_completion.complete`, the step runs before `stage_acceptance_write` and before `stage_verdict_known` —
   pinned BEHAVIOURALLY in the same table: G13 a form with an unknown verdict word and one gap row -> the line is written, then the seam
   stub is called (stub `stage_review_exhausted` records the call); G14 a form whose gap row is refused -> Refusal, and neither
   `stage_acceptance_write` nor the seam stub was called. (No source pin: TESTING «не пишется».)
4. Key-presence (DOC-DISPATCH, script in full in the report, never committed, a negative control with one key absent reports failure):
   in `agents/qa-case-critic.md` present "as a row of `register_gaps` in your form", "it reaches the test report", "tools: Read, Grep,
   Glob, Write, Edit"; absent "exploratory_findings.py add"; in `handoffs/s4-case-critic-to-designer.yaml` present "register_gaps:",
   "`[]` (or no", "missing_prerequisite:"; in `references/role-commands.json` the `exploratory_findings.py add` entry's `roles` does NOT
   hold `qa-case-critic` and holds `qa-runner` and `qa-failure-analyst` (read as JSON).
5. `python -B ai-packages/qa-factory/scripts/role_load.py --all --json` before/after attached; the `qa-case-critic` rows set to the
   measured values with a raise line `key old -> new reason` (AR-20) — or, on F-R6 (b), the measured net is <= 0 and no row is raised.
6. Census: `test_judgment_census.py` (slow, CI) — if the scan creates units for the new functions, rows with class `shape`
   (`register_gap_rows`, `register_gaps_write`), owner `data`, roles `["qa-case-critic", "conductor"]`; ratchet as printed.
7. Change checks (§1) answered in the report: the AR-14/AR-13 greps with their positive controls; `test_field_producers.py` green locally.
Verification: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/handoffs/s4-case-critic-to-designer.yaml ai-packages/qa-factory/agents/qa-case-critic.md ai-packages/qa-factory/references/role-load.json ai-packages/qa-factory/references/role-commands.json ai-packages/qa-factory/scripts/driver_stage_plan.py ai-packages/qa-factory/scripts/tests/test_exploratory_findings.py`
and the non-slow files it prints (expected among them: `test_exploratory_findings.py`, `test_role_load.py`, `test_role_rules.py`,
`test_field_producers.py`, `test_validator_class.py`, `test_ahead_cards.py`); slow ones (`test_role_commands.py`, `test_judgment_census.py`,
`test_brief_pack.py`, every other slow file it prints) — "judged by the batch canon". No CI run, no mutation pass by the builder
(builder-rules 7b). `python -B scripts/selftest.py --limits --lang` from the package dir.
`architecture: AR-9, AR-10, AR-13, AR-14, AR-20, AR-22, AR-23, AR-25, AR-27, AR-28, AR-29 -- the critic writes a form row, the driver
records it through the one writer after one read through the one reader; shape-only checks; empty outcome declared; ratchet as measured`.
`judgment: the case critic judges what a register gap is; code checks the section's shape and an exact-bytes identity (shape/xref, data)`.
siblings: `question_register.raise_from_handoff` (same road for `questions[]`, axis 34); S6/S7 consumer acceptance (forms without the
section: not wired, F-R2); N7 (writer first-error-only); the no-shell card rows of §C (detector node CL-NS).
designer: this file (once accepted).

FR walk (for the builder's report): A — new refusal (R5/R6/R8/R10) names what is wrong, what is expected and a door the critic can open
(its values file) or the conductor (FR-1, FR-2, FR-57); B — the report line's `why_not_a_bug` constant is a text a person reads (FR-6: plain
words, no codes); C — FR-11 the critic's tool (Write of a values file) produces every field; FR-38 told in the template; FR-39 the charter
names no command; FR-13 field list read from the template; FR-56 no Bash; FR-49 the row travels whole; D — FR-16 `recorded_by` is the
dispatch id from the completion, FR-18 a register line is not coverage; E — FR-21/P21 delivery unchanged (a coverage-gap line never adds to
proven), AR-27 owner = the critic dispatch; F — n/a (no money, no measurer); G — FR-32 test row per behaviour, FR-30 English, FR-47 code is
an instrument (it records, never judges).

### Alternative split (F-R9 (b))
RC-1 (form + charter + role-load + card + X1 + changelog; on A2+A3 merged) and RC-2 (driver + table G/J; after RC-1). Owns disjoint by the
lists above; RC-2 waits for RC-1's template row (its rows read the template). Not recommended: two critic entries for one topic (R13-g
allows one pass anyway) and a window where the charter tells the role a section nobody records (RC-1 merged alone breaks FR-11's spirit:
the row would be written and never recorded).

## §F Forks (returned; recommendation first, executable by it)

- **F-R0 (P31, axis 34) — two roads to one register.** Roles with a shell (S6 runner, S7 analyst) run `exploratory_findings.py add`
  themselves; the S4 critic writes a form row the driver records. (a) RECOMMENDED: keep both, the difference read by a capability key —
  the role's `tools:` line (`host_adapter.role_has_bash`, axis 19) — and the form contract's own section (data, default absent = nothing):
  legal form 1 of designer rule 6; precedent O4 (`contract.py:1547-1551`: the designer has no Bash, so it writes and code raises). (b) one
  road for all: every role writes register lines as form rows and the driver records them — rewrites the S6 recorder habit "recorded when
  you meet it" (`brief_pack.py:343-345`), the S7 investigation chains (`origin.target`, `driver_stage_s7.py:683-686`) and the gate B
  executors; cost: a new topic (~6 nodes), not this node. The Lead takes (a) vs (b) to the owner only if (a) is judged not a "real
  difference".
- **F-R1 — who writes `why_not_a_bug` and `title`.** (a) RECOMMENDED: the critic writes `title`, `statement`, `refs`,
  `missing_prerequisite`; the driver supplies `why_not_a_bug` = `REGISTER_GAP_WHY` (the section itself is the critic's classification;
  precedent `driver_machine.py:2794`). (b) the critic also writes `why_not_a_bug` (one more field, ~ +25 tokens, one more writer refusal
  the critic can hit). (c) no `title` field: the driver derives it from the statement — introduces a truncation limit; not recommended.
- **F-R2 — call site.** (a) inside `stage_acceptance_write` (the one place every acceptor's form passes: S4, S6, S7 consumers alike;
  a form without the section records nothing): one road, but the unknown-verdict branch (`:809-810`) skips it, so the gaps of a form with
  an unreadable verdict are lost when the conductor accepts with the gap. (b) RECOMMENDED: in `s4_critic_completion.complete`, after the
  dispatch check, before `stage_verdict_known` (§D.3): every verdict, readable or not; S4-only call line (the only form that declares the
  section); `stage_acceptance_write` (hot: wave 8) untouched. (c) both (a) and the unknown-verdict branches of every acceptor: touches
  `driver_stage_s6.py` (B2 owns `consumer_completion`) for forms that carry no section; not recommended.
- **F-R3 — identity of a recorded row.** (a) RECOMMENDED: exact content (`title`, `statement`, `refs`, `missing_prerequisite`, kind
  `coverage_gap`) against ACTIVE lines, any `recorded_by` (§D.4): no writer change; a verbatim copy in a repair round is not duplicated;
  a row the critic edits after it was recorded gives a second line (duplicate allowed, loss never). (b) exact content AND `recorded_by ==
  dispatch`: a verbatim copy by a later round is recorded again. (c) a `raised_from {dispatch, row}` field in the register, the exact
  `question_register` sibling (a changed replay refused row by row): changes the one writer (`FIELDS`, `CODE_SET` or a caller-set field,
  a reader for AR-22) and `test_exploratory_findings` — heavier; (d) `origin.target` = `<dispatch>#register_gaps[i]` and the chain rule's
  refusal: overloads the S7 investigation target (`driver_stage_s7.py:684`), not recommended.
- **F-R4 — what a refused row does.** (a) RECOMMENDED: a `Refusal` on the standard road, as the refused `questions[]` raise at the same
  site (`driver_stage_plan.py:647-649`, `check=True`) — one road for "a form section raised by the driver" (P31); the critic or the
  conductor fixes the row; written rows are skipped on the retry. (b) a warning line (`stage_done.py --warn`) naming the row and the
  refusal, and the finish goes on: no paid round, but the gap reaches the report only as a warning, and whether an S4 warning reaches the
  test report is NOT verified (B2's warnings road is topic B, unmerged). (c) the seam (`no_move`) at once: pays a conductor call for what
  the critic can fix with one values file.
- **F-R5 — the evidence file.** The Lead's text says `--evidence <its findings file>`. Measured: `critic-findings.md` takes a new round on
  TOP in every repair round (`agents/qa-case-critic.md:101-103`), and the writer stores its sha256 (`_judge_refs`, `exploratory_findings.py
  :234-252`); `exploratory_findings.py check` then reports every S4 line "has changed since it was referenced (stale sha256)"
  (`contract.py:5951-5952`). (a) RECOMMENDED: the critic's form `work/handoffs/<dispatch>.yaml` (per dispatch; the row's own carrier; no
  post-finish writer found — estimate, R16). (b) the findings file as written (stale after a round). (c) both files (still stale).
- **F-R6 — the byte raise.** `ROLE_BRIEF_BYTES_MAX` does not move (no brief change). `role-load.json` `qa-case-critic` moves by an
  ESTIMATED ~ +90 tokens. (a) a named raise to the measured values (AR-20), RECOMMENDED if (b) cannot reach <= 0; (b) hold net <= 0: the
  section comment cut to one line and the charter line shortened to "A register gap no case can carry goes once, when you first find it,
  as a row of `register_gaps` in your form; it reaches the test report. A gap only the person can settle also goes in `questions[]`." (the
  fields are named by the template) — RECOMMENDED first; (c) also add the requirement to the ahead card / `TOOLING_NO_SHELL` (FR-38
  belt-and-braces): raises `ROLE_BRIEF_BYTES_MAX qa-case-critic` (~ +120 B, estimate), not recommended — the template rows are the field
  statement.
- **F-R7 — the second class hit in the same charter (sweep-the-artifact-first).** `agents/qa-case-critic.md` Techniques: "`branch_accounting
  --units` gives the list" (`:82` on sc-a2, `:83` on sc-a3) names a command the critic cannot run. (a) RECOMMENDED: in this node, reword
  to "count the sentences, fields and branches of the sources you are given" (no command; the critic's brief names the register and its
  sources, A.2.3); (b) hand the critic the units as a file (the driver runs `branch_accounting.py --units` into `work/` and the brief names
  it): new artifact + writer row + brief bytes — its own node; (c) leave it (FR-11/FR-56 defect stays named in §C).
- **F-R8 — in-process writer vs the CLI.** The Lead's text says the driver "calls `exploratory_findings.py add`". (a) RECOMMENDED:
  `exploratory_findings.append` in-process — the one writer function every other in-package writer calls (`driver_machine.py:2799`,
  `investigation.py:14`, `place_answers.py:16`); no command-line ceiling on long texts (R15), no comma split of a ref (the CLI splits
  `--refs` on ","), refusals are the writer's own `ValueError` text. (b) `self.py("exploratory_findings.py", "add", ..., check=True,
  expect=...)` — literally the owner's command (AR-14 change check wording), the gate_refusal shape for free; costs a subprocess per row,
  a Windows command-line ceiling (~32K chars; `subprocess.run` raises `OSError` that `py` does not catch, `driver_runner.py:222-229`) and
  the `--refs` comma split.
- **F-R9 — one node or two.** (a) RECOMMENDED: one node F7-RC on A2+A3 merged (§N). (b) RC-1 + RC-2 (§N alternative).

## Lead decisions (14.11.2026, owner away: by recommendation, reversible, in the morning report)

- F-R0 (a) "by recommendation, until the owner's word": two roads keyed by the role's capability (precedent O4). P31 lets
  only the owner allow an exception, so this goes to the owner as a question; (b) is a new topic and is not started.
- F-R1 (a), F-R2 (b), F-R3 (a), F-R4 (a), F-R5 (a) (the form, not the findings file: the Lead's brief was wrong on this),
  F-R6 (b) first and a named raise to the measure only if net <= 0 is not reachable, F-R7 (a), F-R8 (a) in-process `append`,
  F-R9 (a) one node F7-RC.
- CL-NS (detector for "a no-shell role listed on a command card") and the `raise_from_handoff` non-list analog become queue
  lines of their piles; N7 stays its own node.
- Dispatch: after A1a+A1b+A1c are in `main` and after ONE plan critic pass over this draft.

## Small choices closed by the designer (no design weight)
- The section name `register_gaps` and its place right after `questions` (the brief's working name; adjacency to its sibling).
- The empty outcome declared in the contract's comment, not in `null-outcomes.json`: the walk there covers required lists/index rows/tool
  fields (`null-outcomes.json:3`), and the optional `questions` of the same form declares its own empty answer the same way (`:129`).
- `refs` written as a block list (the form's own list style, `questions[].read`), never a flow list.
- The test host is `test_exploratory_findings.py` (keep, A3 already put X1/X2 there): `test_repair_route.py`, the other file that stubs the S4
  finish, is QUARANTINED (`test-layers.json:9409-9414`), so it is not used.
- `register_gap_rows` is pure (data in, rows/problems out) so the table needs no driver process (TESTING «Время»).
- Print lines on record/skip (the driver's console log, as `stage_acceptance_write`'s steps print through `py`).

## §C Class question — roles without a shell told to run a command

No-shell roles (frontmatter `tools:` read on sc-a3/read-main): `qa-case-critic`, `qa-case-designer`, `qa-test-strategist` (`agents/*.md:4`);
the other nine carry Bash. Carriers walked: the three charters (grep `\.py` and the `` `name --flag `` shape), their slices under
`references/slices/<role>/`, `brief_pack.TOOLING_NO_SHELL`, `references/ahead-cards.json` cards, `references/role-commands.json` `roles`.

| role | command | carrier | verdict |
|---|---|---|---|
| qa-case-critic | `exploratory_findings.py add` | A2 charter `:96` (sc-a2); A3 card `role-commands.json:201-209` | HIT (B1) — fixed by F7-RC |
| qa-case-critic | `branch_accounting --units` | charter Techniques `:82` (sc-a2) / `:83` (sc-a3, main) | HIT — told to a role with no shell; F-R7 |
| qa-case-critic | `critic_rollcall.py --store` | `role-commands.json:194-200` `roles: [qa-case-critic]` | DRIFT — card lists the role; no carrier tells it to run (charter `:118-119` describes code's refusal; `slices/qa-case-critic/case-lifecycle.md:44` "run by the orchestrator") |
| qa-case-designer | `artifact_producer.py publish`, `validate-batch` | `role-commands.json:166-185` | DRIFT — no charter/slice/brief line tells the designer (grep of its charter and slices: no hit; `TOOLING_NO_SHELL` designer: "made by the orchestrator") |
| qa-case-designer | `case_versions.py --pin` | `role-commands.json:218-225` | DRIFT — same; `case-lifecycle.md:31` "the orchestrator runs it" |
| qa-test-strategist, qa-case-designer | `plan_row.py` | `role-commands.json:226-233` | NOT A HIT — the card itself gives the no-Bash road ("by a role without Bash with Edit") |
| qa-test-strategist | `grounding_section.py` | `role-commands.json:234-240` | DRIFT — the guard offers it only with a shell (`guard_pre_tool.py:819-823`); not told to the strategist |
| all three | `handoff_check.py --file ... --fix --values -` | `slices/*/common-rules.md` (critic `:59`) | NOT A HIT — marked "(Bash) or one Write of <dispatch>.values.yaml (no Bash)" |
| all three | `handoff_help.py` | same paragraph | NOT A HIT as read — "the conductor answers it" (the role writes `blocked`) |

Two hits (both in the critic's charter), four drift rows (card `roles` lists a no-shell role nobody tells to run it). Positive control of
the grep shape: it found `critic_rollcall.py` (`:118`) and `branch_accounting --units` in the same charter.
Existing partial detector: `stage_joints.py` refuses `door_needs: shell` without a `when: shell` (`:881-886`) and reads capability through
`host_adapter.role_has_bash` (`:471-476`) — only for stage-joints rows, not for `role-commands.json` or charters.

Proposed node **CL-NS** (detector; not designed in full): a data join in an existing keep test (candidate `test_ahead_cards.py` or the
stage-joints walk, both fast; NOT `test_role_commands.py`, slow): every role in a `role-commands.json` entry's `roles` has
`host_adapter.role_has_bash(role)` True, unless the entry's `input` states a no-shell road (an explicit data key, e.g. `no_shell_road`,
not a phrase match — FR-12); the four drift rows are fixed (roles corrected) in the same node, or start a shrink-only list. Census class
**xref**, owner **data**. The charter side (prose naming a command) stays a judgment: critic standing question on FR-56 plus `role-rules`
— no regex over charter prose.

## §S Siblings and analogs (reported, not widened)
- `question_register.raise_from_handoff` reads a non-list `questions` as `[]` in silence (`question_register.py:1606-1607`) — the FR-4
  analog of R5; one queue line for the Lead (a node of the question-register pile), not this node.
- S6 charter's own use of the register (`references/explore-charter.md:103`) and the runner's manual card (`brief_pack.py:343-345`) —
  unchanged (shell roles).
- N7 (writer reports the first problem only) — its own node (critic proposal).

## SIBLING_MAP axes (mechanism: "a no-shell acceptor's form section recorded by the driver into a register")
axis 1: n/a — no policy/role-file/journal change of this deployment. axis 2: n/a — no exam instrument. axis 3: covered — package only,
reaches the release copy by the normal release. axis 4: n/a — no FR text change. axis 5: covered — stage twins: the S6/S7 consumer
completions are named twins (forms without the section; F-R2). axis 6: n/a — no measurer. axis 7: n/a. axis 8: covered — story paths via
`self.task_root` and the writer's `register_path`. axis 9-11: n/a. axis 12: n/a. axis 13: n/a — the dispatch text unchanged. axis 14-16:
n/a. axis 17: n/a — no detector verdict shape. axis 18: covered — `role-load.json` rows (F-R6) and census ratchet as printed. axis 19:
covered — capability read only through `host_adapter.role_has_bash` (F-R0, CL-NS). axis 20-22: n/a. axis 23-27: n/a. axis 28: covered —
the row form is told in the contract template (the one render site of a role's row fields). axis 29: covered — no new jsonl appender (the
writer's `hooklib.append_jsonl_line` stays the one). axis 30: n/a. axis 31: covered — charter (when), template (fields), card (runner/
analyst only): one owner per aspect. axis 32: covered — census rows of §1; judgment stays with the critic. axis 33: covered — the dispatch
id is the completion's (`dispatch_id` or `last_dispatch`, `:803`), not re-derived. axis 34: covered — F-R0 (two roads keyed by capability,
returned). axis 35-36: n/a.

Four questions (CLAUDE.md rule 10): (a) cost — the critic writes rows it would have written as commands; the driver pays one register read
and one append per row; a refused row may cost one critic round. (b) axes above. (c) detector — table G1-G14 + J1 in
`test_exploratory_findings.py`; the live-runs row below; CL-NS for the class. (d) on the path — the completion of every S4 critic finish
calls the step; nothing to skip.

## Live proof owed (FR-33) — the `live-runs` row text
"F7-RC: on a stand story whose sources hold a sentence no requirement holds and no case can carry, the S4 case critic (no shell) writes a
`register_gaps` row in its form; after the S4 critic finish, `work/exploratory-findings.jsonl` holds one `coverage_gap` line with
`recorded_by` = the critic's dispatch id, window `pre-gate-a`, evidence = its form, and `test-report.md`'s block 'Exploratory findings and
unresolved questions' lists it under the coverage gaps with 'missing: …'; a repeated finish or resume adds no second line; on a story with
no such gap the section is empty and the register gains no S4 line. Closed by: the run log + the register line + the report excerpt."

## BINDING amendments after the plan critic (t-730, `docs/tasks/specs/reviews/20261114-sc-f7-recut-plan-critic.md`)

They override the text above where they differ; the review's section "Binding amendments" A1-A10 is taken WHOLE and is part of
this spec (read it there, verbatim). In one line each:
- A1: `"register_gaps": ("s4-case-critic-to-designer",)` joins `handoff_init.EMPTIED` (owns: that row of `scripts/handoff_init.py`
  and one row in the test that pins `EMPTIED`); the `refs` placeholder says "or omit"; row: the role's copy holds
  `register_gaps: []`, and a filled row with no refs gives no `register_gaps` problem at the exit check.
- A2: owns also `scripts/tests/fixtures/driver-layers.json` (rows `register_gaps_write`, `register_gap_rows`, `REGISTER_GAP_WHY`
  only) and the `qa-requirements-tester` / `qa-test-strategist` rows of `references/role-load.json`; the merge of wip/sc-a2 into
  main conflicts in `role-load.json` — settled by re-measuring with `role_load.py --all --json`.
- A3: the refusal is `Refusal(text, dispatch=dispatch)` and its door addresses the CONDUCTOR (who receives it): `handoff_check.py
  --file work/handoffs/<d>.yaml --set register_gaps[<i>].<field>=<value>`, or delete the row and keep the gap in `questions[]`; then
  the finish is retried; rows already recorded are skipped on the retry. F-R4's cost reason is struck.
- A4: R16 is replaced — the form IS rewritten after the add (`story_step finish` runs `handoff_check --fix`); the evidence sha can
  go stale; accepted residual (the line carries the row's text whole); G-row: a second `--fix` over the unchanged form leaves equal
  bytes (pin it, or name the drift).
- A5: step 4 catches `OSError` from `append` as well as from `read`; G11 = register path is a directory -> `read` gives the empty
  register -> `append` raises `PermissionError` -> Refusal naming the register.
- A6: edge R18 — the skill road records no rows (no driver runs `complete`); named on SIBLING_MAP axis 5 and in the F-R0 owner
  question; queue line, owner the qa-story pile.
- A7: `REGISTER_GAP_WHY` = "the reviewer of the test cases recorded it as a gap in the requirements: no test case can check it; it
  is not a defect of the product".
- A8: census — `register_gaps_write` class `xref`, `register_gap_rows` class `shape`.
- A9: a key outside the template row is ignored with a print line, never refused.
- A10: F-R0 (a) is described as built: the road is chosen by the contract's own section at one S4 call site; `role_has_bash` is
  read nowhere on this path.
- Bytes (F-R6): the measured net change is +28 B, so "(b) net <= 0" is not reached as worded: the builder first trims the charter
  line to reach <= 0; if the meaning would suffer, a NAMED raise of at most 28 B is taken and named in the report (AR-20).
- Queue (Lead): `exploratory_findings.read` reading a directory as "empty" (AR-28 analog); the skill-road line (A6).

## Reading trail
Read whole or in the named ranges: critic verdict t-717 (whole); topic spec lines 200-280, 700-889 and the F7 grep hits; sc-a2
`agents/qa-case-critic.md` (whole), `handoffs/s4-case-critic-to-designer.yaml` (whole), A2 report (whole); sc-a3 A3 report (whole),
`references/role-commands.json` (whole), `scripts/exploratory_findings.py` (whole), `brief_pack.py:170-400`, `references/ahead-cards.json:1-50`;
read-main: `driver_stage_plan.py:560-888`, `driver_dispatch.py:740-880` and `:1015-1074`, `driver_runner.py:205-295`, `driver_core.py:95-135`,
`driver_machine.py:2195-2264` and `:2680-2810`, `driver_stage_s7.py:670-699`, `contract.py:1530-1564` and `evidence_ref_issue` `:5918-5953`,
`report_facts.py:3826-3925` (+ grep hits `:291-434`), `question_register.py:1560-1627`, `handoff.py:409-417`, `:662-664`,
`stage_joints.py:1-80`, `:460-569`, `guard_pre_tool.py:800-827`, `null-outcomes.json:1-40`, `s7-analyst-to-automator.yaml:30-49`,
`judgment-census.json:1-12` (+ grep `:376-385`, `:1104-1111`), `test-layers.json:1651-1700`, `:5370-5410`, `:9403-9414`, `docs/TESTING.md`
(whole), `docs/SIBLING_MAP.md` axis headings, `design/architecture.md` change-check lines (grep).
Greps (with controls): `tools:` over `agents/*.md` (12 hits); `\.py` and `` `name --flag `` over the three no-shell charters (control: found
`critic_rollcall.py`); the command names over `references/slices/qa-case-{critic,designer}` and `qa-test-strategist` (control: generated
headers matched `\.py`); `exploratory` over `critic_rollcall.py` = 0 (control `apply.fixes` = 12); `exploratory_findings` callers over
`scripts/*.py`; `stage_acceptance_write` callers; `set_value(` callers (15 files, writers before the finish only — estimate).
NOT done (no shell in this role): `role_load.py`, `scenario_walk.py --witness-for`, any test run, any byte measurement — every number marked
"estimate" above is owed to the builder's DoD item 5.
