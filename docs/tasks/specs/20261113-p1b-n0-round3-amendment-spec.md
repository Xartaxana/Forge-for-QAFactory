# P1-b N0, round 3 - amendment spec (DESIGNER DRAFT)

Status: designer draft (Opus) from the Lead's intent brief of 13.11.2026. It does not edit the P1-b spec or the A1 amendment.
Forks are listed in section 6 and none is closed here. Small choices I closed are in section 7, the reading trail in section 8.
Until the Lead accepts it, this is not a dispatch.

Trees: `WT` = `C:\QAFactory\forge-repo\.claude\worktrees\p1b-n0` (branch `wip/p1b-n0`); `PKG` = `WT\ai-packages\qa-factory`.
"P1-b" = `C:\QAFactory\forge-repo\docs\tasks\specs\20261113-p1b-dry-story-spec.md`; "A1" = section A1 of
`C:\QAFactory\forge-repo\docs\tasks\specs\20261113-p1-specs-amendment-owner-words.md`; "R2" = the round-2 report
`WT\docs\tasks\specs\reports\20261113-p1b-n0-round2-report.md`; "R1" = the round-1 report next to it. All line numbers come
from reading these files on 13.11.2026.

---

## 0. Verdict in brief

- The relevance verdict on TP1-15791 is the **first** blocker, and very likely not the only one. S2 and S3 contain at least
  two more judgments the dry world has no value for today. The clearest is the S2 exit detector `branch_accounting.py`: every
  unit of the story text must have a home in `## Source obligations`, and the filler's register template has no such section.
  Section 1 lists them all.
- Option (a), replaying recorded role outputs, is not workable. A1 forbids it, and the 0.10.2 snapshot lacks today's sections
  and today's files anyway, so today's detectors would refuse the replay. Option (b), declared stub values kept as data,
  follows the P1-b spec's own AR-29 rule: the row sets the outcome, the stub does not compute it. Option (c) can judge
  **time**. It cannot judge **feasibility**: it does not show that a stub road gets through S1..S3 without hand-written outputs.
- The printed `gate: continue` breaks AR-28. `dry_world.gate_verdict` (`PKG\scripts\tests\dry_world.py:453-458`, printed at
  `:510`) never checks whether S3 was reached, so an unknown was printed as a pass. Every option needs this fixed.
- Recommendation (fork F-R3-1): **one bounded round 3 using option (b)**. It declares the relevance verdict as type data. It
  allows the contract's own empty/remainder forms for S2/S3 (fork F-R3-4). It fixes the gate line. It ends at the next
  labelled stop, wherever that is. N0 then gets **no round 4**: whatever is still open moves to N2, where the stub grows anyway.

---

## 1. Question 1 - what stops S1, and the class

### 1.1 What stops S1 (facts)

- R2 `:4-7`, `:96-101`, `:68` (the verbatim CI line). The road reaches `s1_review`, the answer is "go on", and then
  `review --record failed (exit 3): ticket_adapter: review rejected: assess these sources before showing the review:
  SRC-50693ee590c6eac703d3`. The driver ends at the conductor (`stub: the prompt lists no open move to offer`).
- The refusal is raised in `PKG\scripts\source_inventory.py:3408-3411` (`record_source_review`). It refuses the review while
  any `required` source still has `relevance == "pending"`. The driver's call is in `PKG\scripts\driver_sources.py:700-704`.
- A pending source becomes decided only through the role's `assess`: `PKG\scripts\ticket_adapter.py:3000-3010` (it requires
  `--output --source-id --relevance relevant|not_relevant|unknown --reason --assessment-ref`), which writes through
  `source_inventory.record_relevance_assessment` (`:3187-3223`; an empty reason is refused at `:3189-3190`; the
  `assessment_ref` must be a safe task-relative path, `:3191-3192`). `peek` (`ticket_adapter.py:2738-2752`) is a read through
  the tracker client and produces the material the assessment cites.
- The stub sees this and declines to judge: `PKG\scripts\tests\dry_stub.py:76-88` (`pending_judgments`) and `:164-166`. Its
  only S1 role step is `collect --relation task`, a read (`:38-39`). Labelling it `live_only` was correct under E13.
- "Kept live_only" (R2 `:121-122`) covers the relevance verdict, `work/reference-snapshot.yaml` (an optional dispatch outside
  the main pass, `PKG\references\stages.json:39-45`), and "the later stages' role outputs are untried".
- R2 Questions 1-2 (`:139-145`). Q1 is the same choice as this spec's F-R3-1/F-R3-2 (the builder recommended the type-row data
  form). Q2, registering the files in `plans/features.json`, is outside N0's owns and is left with the Lead (section 7, S-5).

Recorded truth for this story: the real run judged TP1-15791 `relevant` with reason `explicit required source`. The carrier is
`PKG\scripts\tests\fixtures\investigation-14857\TP1-14857\work\source-inventory.json:432-433` (source
`SRC-5a93606917e1f7d2c56b`, canonical ref `:383`), and the person's review words are at `:388-396`.

### 1.2 The class: every role judgment on S0..S3 that needs a value in the dry world

"Value today" = whether the round-2 world supplies a value without hand-written text. "Status" = met by a run (R1/R2) or
untried. For untried rows the evidence is the code that will judge the output.

| # | Stage | Judgment (whose) | Where code consumes or judges it (file:line) | Value today | Status |
|---|---|---|---|---|---|
| J0 | S0 | none: S0 has no role (`stages.json:5-23`, `role: null`) | - | n/a | met, done (R2 `:63`) |
| J1 | S1 | Scout's handover form: verdict and fields | form `contract:` filled by `form_filler.fill_form`; verdict from the row control or the vocabulary's first word (`dry_stub.py:145,152`; module text `:6-11`) | yes (data/template) | met (R2 `:97`) |
| J2 | S1 | `work/context-manifest.json` content (issue type, AC, implementation, related) | template `PKG\scripts\tests\fixtures\form-fill-rules.json:232-271`; `source_sha` declared synthetic (`:267-269`) | yes (template) | met (R2 `:96`, "witness OK") |
| J3 | S1 | `work/impl-diff.txt` | world data (`tracker/mr-4566.diff`, R2 `:10-17`), not a judgment | yes (data) | met |
| **J4** | S1 | **Relevance of each required mentioned source** (TP1-15791) | `source_inventory.py:3408-3411` refuses the review; writer `:3187-3223` via `ticket_adapter.py:3000-3010` | **none** | **met: the blocker** |
| J5 | S1 | Inspection status of a kept source's materials (`inspect --inspection-status read\|partial\|unavailable`) | `ticket_adapter.py:2922-2927`; open point `source:not_inspected` at `source_inventory.py:2497-2500` | none | untried. Reachable only if J4 = `relevant` and code's own stamp does not cover it (the recorded run shows `inspection_by: code:snapshot`, `source-inventory.json:397-399`) |
| J6 | S1 | A source gap accepted by the person (`s1_gap`): the person's, not a role's | `driver_dispatch.py:400-402` | the closed answer only if a probe row names `s1_gap` (A1-E3; `dry_world.py:443-446`) | untried |
| J7 | S1 | The person's source review words (`s1_review`) | `driver_dispatch.py:403-408`, `:746-748` | yes: "go on" (`fixtures\dry-walk\seeds\probe.json:5`) | met |
| J8 | S1 | Reference walk (optional `qa-runner` dispatch) | `stages.json:39-45` | n/a (outside the main pass) | kept live_only (R2 `:121`) |
| J9 | S2 | Register rows (each requirement, its source and observable) | template `form-fill-rules.json:272-278`; S2 detectors `stages.json:85-90` | yes (one generic R row) | untried |
| **J10** | S2 | **A home for every unit** of the story text and of every kept ticket (`## Branches`, `## Source obligations`) | S2 exit detector `branch_accounting.py` (`stages.json:87-88`); `reconcile` `branch_accounting.py:732-770`; `REJECT ... have no home` `:1388`; contract `references\artifact-contract-plan.md:19-23` | **none**: the register template (`form-fill-rules.json:276`) has neither section | untried, **expected blocker** |
| J11 | S2 | One reading row per attachment (`## Attachments`) | contract `artifact-contract-plan.md:24-27` | none (no section in the template) | untried; reached only if the story or a kept ticket has files |
| J12 | S2 | Readiness verdict `ready\|blocked` | template `form-fill-rules.json:279-291`, closed list, first option | yes | untried |
| J13 | S2 | `understanding.md` | template `:293-299` | yes | untried |
| J14 | S2 | Critic acceptance verdict (`qa-case-critic`, `stages.json:66`) | form verdict, as in J1 | yes (data) | untried |
| J15 | S3 | Plan rows (disposition, level, risk, obligations) | templates `form-fill-rules.json:50-148`; detector `planning_contract.py` (`stages.json:133-136`) | yes (generic row) | untried |
| J16 | S3 | Grounding labels per diff hunk, plus claims | template `form-fill-rules.json:149-156` (one `G-n` row, `now_ref: diff:src/app.py:1`, a path that is not in the world's diff of 25 files, R2 `:97`); one reader `planning_contract.read_grounding` `:1011-1055` | a value exists, but it does not match world data | untried, likely blocker |
| J17 | S3 | Every register unit/branch has a home in the plan | `branch_accounting.py:1656` | follows J10 | untried |
| J18 | S3 | Critic acceptance verdict | form verdict | yes | untried |
| J19 | end | Gate A | the road ENDS there (`dry_world.py:438`); measuring needs no answer | n/a | - |

What the class shows: J4, J5, J10, J11, J16 and J17 are all role judgments **over world data**. The value must agree with the
ticket, the diff or the inventory. J1/J12/J14/J18 are closed verdicts, which the stub already reads from data. For each item
in the first group, the contract names a legal **empty or remainder form** that is not a per-item judgment: `Branches: none --
<why>`, a `rest | unreconciled: <why>` home (`artifact-contract-plan.md:20-23`; branch_accounting reads `rest`,
`branch_accounting.py:764-765`), and `| rest | - | not_opened | - | - | <why> |` for attachments (`:26-27`). J4 has no such
form. Its closed list is `relevant | not_relevant | unknown` plus a reason, so the value must be data.

Honesty note on the remainder forms: `rest | unreconciled` turns into a gate-A debt (`branch_accounting.py:2385`,
`source_unreconciled`). It is not a pass. The dry road would carry a declared debt and report it as one, which keeps it honest
under AR-28/FR-41.

---

## 2. Question 2 - the options for a value

| Option | What it is | Rule kept / broken | Cost | What the measurement then proves / does not prove about the P1-b premise |
|---|---|---|---|---|
| (a) replay | Recorded role outputs of the real run (snapshot 0.10.2) become fixture data, one row per judgment | P27/AR-29: kept (code computes nothing). **Broken:** A1 table `:97` (the snapshot's `source-inventory.json` and `ticket.json` are "not taken": old-schema code output), `:99` (role outputs "no: the stub writes them with the P1-a filler from today's forms"), `:100`; F-A1-4 (b) (old code output never becomes input to today's code); P1-b reason A (no hand-written or past world). Infeasible beyond J4: the snapshot register has no `## Source obligations`/`## Branches` (its headings: `investigation-14857\TP1-14857\work\requirements-register.md:19,46,74,83,93`), and the snapshot has no `context-manifest.json`, `understanding.md` or `grounding.yaml` (Glob `**/{grounding.yaml,context-manifest.json,understanding.md,test-plan.json}` over the snapshot finds only `work/test-plan.json`, a positive control of the same form) | One round of copying, then refusals from today's detectors on the old shapes | It would show that old outputs fail today's gates, which is not the question. It says nothing about stubs on today's forms |
| (b) declared stub value | The verdict is a data value in the type row (or a walk row's `stub`). The stub runs the role's own commands (`peek`, `assess`) with exactly that value and refuses (`live_only`) for any source the data does not name | Kept: P27/AR-29 (P1-b `:51`: "the row's outcome ... is SET by the walk row, not computed"; grammar `stub` at P1-b `:257-259`, `:265-267`); A1-E3 ("the answer is a closed variant from the walk row; without one, red"; this is the role-side twin of the person-side rule); AR-1/P2 (keyed by the ticket key in a data row, never a project name); AR-14 (the inventory's one writer stays `ticket_adapter`) | Small: one field in `dry-types.json`, two role steps in `ROLE_STEPS`, selftest rows. More if S2/S3 need the contract's remainder forms (F-R3-4) | It proves that the real driver, today's forms and today's gates carry a story through S1 (and S2/S3 as far as the declared forms reach) with no LLM, measured in seconds. It does not prove that a role's judgment is right; that stays with P2-g and live runs (P1-b `:89-90`) |
| (c) keep live_only | Judge the gate on the reached part (S0 + S1 to the review) | Kept, provided the gate line says "partial" (today it does not: AR-28, section 4.1) | Zero code, apart from the gate-line fix | **Time:** the measured part gives S0..S3 a margin of about 10x (11.5 s vs 120 s, R2 `:75-76`). **Feasibility:** unproven, and that is what the "stop -> reconsider the layer's form" branch of the gate exists for (P1-b `:540`). Also, all three row timings end at the same S1 blocker (R2 `:71-73`), so the median 7.2 s measures rows that never reach their named state |

---

## 3. Question 3 - `events.jsonl` refused by `story_step`

Fixed in round 2. `dry_world._rewrite` now skips `events.jsonl` (`PKG\scripts\tests\dry_world.py:221-222`; R2 `:29-30`, item 5).
Witness: in the round-2 CI run both probe rows reach their named question from a snapshot copy (R2 `:71-72`). In round 1 every
copy hit the conductor first (R1 `:50-52`).

Residual edge, not yet checked by anything: the copy's `events.jsonl` now still holds the **source** world's absolute paths
("only history", `:221`). If any reader acts on a path taken from an event, a row would write into the snapshot or the source
world. That breaks P1-b `:445` ("the snapshot itself never changes") and E16. Round 3 adds a check (edge E-R8).

---

## 4. Question 4 - what the gate needs and what one round can deliver

### 4.1 The numbers the gate needs (P1-b `:535-540`, F12 `:804`)

The verdict needs S0->S3 seconds on CI, the median and the worst of the three probe rows started from snapshot copies, and an
implied premise: S0->S3 actually reached S3. Today's code prints a verdict without that premise
(`dry_world.py:494, 508-510`, `gate_verdict` `:453-458`). The road stopped in S1 and the line still read `continue`.

Arithmetic with the measured numbers (carriers: formula P1-b `:536`; numbers R2 `:75-76`): 2.5 x 11.5 s + 120 rows x 7.2 s =
28.75 + 864 = 892.75 s, about 14.9 min, against the "<= 15 min" estimate in that same line. **The binding number is the row
median, not S0..S3**, and that median comes from rows stuck in S1.

### 4.2 Can (a)/(b)/(c) deliver in one more round?

- (a): no (section 2).
- (c): delivers the time numbers now, but only with the gate-line fix and the wording "partial road". That fix is a small edit
  that could go in the Lead's small-work batch.
- (b): delivers J4 for certain. It delivers S2/S3 only if F-R3-4 (a) is taken and J16 (the grounding hunk paths) is solved by
  a data token rather than a judgment. That is likely but not certain, which is why the node below is **bounded**: it ends at
  the next labelled stop, and the gate is then judged on what was reached, with honest wording.

---

## 5. The node (if F-R3-1 = round 3)

### N0-r3 - declared judgments as data, honest gate line, next labelled stop

given: this file (sections 1-4); R2 and R1 (paths above); P1-b sections 3.3, 4, 5 (E7, E13, E15, E16, E18) and section 6 N0 (`:522-540`); A1 (A1-E3, A1-E4, A1-E6); `PKG\scripts\tests\dry_stub.py`; `PKG\scripts\tests\dry_world.py`; `PKG\scripts\tests\fixtures\stories\dry-types.json`; `PKG\scripts\tests\fixtures\dry-walk\seeds\probe.json`; `PKG\scripts\tests\fixtures\form-fill-rules.json`; `PKG\scripts\source_inventory.py:2485-2500,3035-3053,3187-3223,3397-3419`; `PKG\scripts\ticket_adapter.py:2738-2752,3000-3010`; `PKG\scripts\branch_accounting.py:1-31,732-770,1388`; `PKG\references\artifact-contract-plan.md:15-27`; `PKG\scripts\planning_contract.py:1011-1055`; `PKG\references\stages.json:24-138`; `PKG\scripts\tests\fixtures\investigation-14857\TP1-14857\work\source-inventory.json:381-439` (provenance of the declared value only); `PKG\design\factory-rules.md`; `C:\QAFactory\forge-repo\plans\builder-rules.md`
owns:
C:\QAFactory\forge-repo\.claude\worktrees\p1b-n0\ai-packages\qa-factory\scripts\tests\dry_stub.py
C:\QAFactory\forge-repo\.claude\worktrees\p1b-n0\ai-packages\qa-factory\scripts\tests\dry_world.py
C:\QAFactory\forge-repo\.claude\worktrees\p1b-n0\ai-packages\qa-factory\scripts\tests\fixtures\stories\dry-types.json
C:\QAFactory\forge-repo\.claude\worktrees\p1b-n0\ai-packages\qa-factory\scripts\tests\fixtures\dry-walk\seeds\probe.json
C:\QAFactory\forge-repo\.claude\worktrees\p1b-n0\ai-packages\qa-factory\scripts\tests\fixtures\form-fill-rules.json
C:\QAFactory\forge-repo\.claude\worktrees\p1b-n0\ai-packages\qa-factory\scripts\tests\test_field_producers.py
C:\QAFactory\forge-repo\.claude\worktrees\p1b-n0\docs\tasks\specs\reports\20261113-p1b-n0-round3-report.md
(The last two package paths apply only under F-R3-4 (a). Under (b) they drop out. Whether P1-a currently owns
`form-fill-rules.json` is the Lead's overlap check, rule 4.)
non-goals: any edit outside `scripts/tests/` (driver, controller, gates, `ticket_adapter.py`, `source_inventory.py`, `branch_accounting.py`, `planning_contract.py` are read-only: a gate that refuses a legal declared form is a FINDING in the report, not a fix); a new filler GENERATOR in `form_filler.py` (a template that needs one is `live_only` with its reason, and a question); per-unit or per-hunk content written for this story (hand-written world, P1-b reason A); switching the declared relevance value to get past a cascade (that is fork F-R3-3, the Lead's); walk/exits/census (N1); `keep` rows; `canon.yml` (unchanged: the `dry-story-spike` job runs the branch as in round 2); `plans/features.json` (S-5); a round 4 of N0
handoff: builder report at the `owns` report path (rule 7 of `.claude/agents/builder.md`): per-stage outcomes, the seconds table (S0, S1, S2, S3, snapshot, three rows), the CI run link and verbatim log lines, the list of templates/fields added with their derivation lines (as R2 `:115-122`), every stop with its label, and the gate line as printed
edges: E-R1..E-R11 below; P1-b E7, E13, E16, E18; A1-E3, A1-E4
DoD: (1) `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <owns>` is run and its output attached (E12/A1-E6: no row covers these files yet; the expected output is "run the whole scenario layer" and nothing more is run for it, as in R1 `:32-33`); (2) local: `python -B ai-packages/qa-factory/scripts/tests/dry_stub.py --selftest` prints all rows `ok`, including the new rows of the case table below; (3) only if `form-fill-rules.json` changed: `python -B scripts/tests/test_field_producers.py` from the package directory (as R2 `:44-46`), green, and the known-red / not-in-world counts printed against R2's 29 / 47; (4) `python -B scripts/selftest.py --lang` from the package directory, green; (5) CI: `canon.yml` `dry-story-spike` on `wip/p1b-n0` (started as in R2 `:56-57`), read with `python -B tools/ci_read.py jobs <run>` and `python -B tools/ci_read.py log <job> --grep ''`; the log shows `outcome S1: done` OR S1 with a labelled stop that is NOT the relevance of TP1-15791, every later stage done or labelled (never `UNLABELLED RED`), the `spike[...]` line, and a gate line in the section 5 E-R7 form; (6) the commit message carries `architecture:` and `judgment:` lines naming the AR-n below (tools/architecture_gate.py)
siblings: axis 34 (one road: the stub reaches `source_inventory` only through `ticket_adapter.py` commands, the same as a live scout; the declared value is a data row keyed by ticket key, the same field form for every type); axis 17 (the gate line and the stop labels keep one output shape: `outcome <stage>: ...`, `gate: ...`); axis 18 (no ratchet changes in this round: n/a)
designer: C:\QAFactory\forge-repo\docs\tasks\specs\20261113-p1b-n0-round3-amendment-spec.md

#### AR-n named, with the change check

| AR | What the round does | Change check (in DoD) |
|---|---|---|
| AR-29 | A role's judgment (relevance) is a DATA value of the type row. The stub reads it and never computes it; with no data value, `live_only` | Selftest row: a pending source not named in the data gives `live_only` naming the source and no `assess` call (the stub's journal holds no `assess`) |
| AR-28 | Gate line: no verdict unless S3 is done | Selftest rows: S3 not done gives `gate: undecided -- ...`; S3 done gives the numbers verdict |
| AR-14 / AR-13 | `work/source-inventory.json` keeps one writer (`ticket_adapter.py`). The stub reads it through the package's reader `source_inventory.load_inventory` instead of `json.loads` (today `dry_stub.py:81`) | grep of `dry_stub.py` finds no `write_text`/`write_bytes` on `source-inventory`; `pending_judgments` calls `load_inventory` (positive control: `load_inventory` is defined in `source_inventory.py`, used at `:3193`) |
| AR-1 | The declared value is keyed by ticket key inside the type row. There is no branch on a type id or project name in code | grep of `dry_stub.py`/`dry_world.py` for `codemie` and `14857` finds no hits outside comments (positive control: `codemie-14857` is found in `dry-types.json:1`) |
| AR-23 | Remainder/empty forms of S2/S3 (if F-R3-4 (a)) are exactly the contract's declared empty outcomes | each template row added names its contract line (`artifact-contract-plan.md:20-27`) in the report's derivation table |

Untouched: AR-2...AR-12 apart from AR-7 (code stays an instrument: the stub runs the role's own commands), AR-15...AR-22,
AR-24...AR-27. The round adds no package code outside `scripts/tests/`.

#### Checks the round adds: owner and census class

`test_judgment_census.py` does not count `scripts/tests/` (P1-b `:71-73`). The classes below are given for critic question 11.

| # | Check | Owner (P27) | Class (AR-29) |
|---|---|---|---|
| C-R1 | A declared judgment row is well-formed (known key, value in the closed list, non-empty reason, no duplicate key) | data (code) | shape |
| C-R2 | A declared judgment naming no source in the inventory prints NOTE `unused judgment <key>` | data | xref |
| C-R3 | The gate verdict is printed only when S3 is `done` | data | presence |
| C-R4 | Snapshot tree hash is unchanged after the probe rows | data | xref |
| C-R5 | The declared VALUE itself (`relevant` for TP1-15791) | intent/judgment: chosen by the Lead (F-R3-3); provenance is the recorded run's verdict | - (not a code check) |

#### Items

| # | File, function | Behaviour | Check (a row of the `dry_stub.py --selftest` table unless named) |
|---|---|---|---|
| 1 | `dry-types.json`, type `codemie-14857` | New field `stub` with the same grammar as a walk row's `stub` (P1-b `:257`), first key `source_relevance`: `{"TP1-15791": {"relevance": "<F-R3-3 value>", "reason": "<one sentence>", "from": "investigation-14857/TP1-14857/work/source-inventory.json:432-433"}}`. A type row without `stub` = `{}` | `load_types()` reads a row without `stub` (round-2 file) and with it. Bad value, empty reason, duplicate key: red with file and key (A1-E4 form) |
| 2 | `dry_world.py`, control writing | The control the stub reads = the type's `stub`, overlaid by the row's `stub` (row wins, key by key). The main pass uses the type's `stub` alone | Row with its own `source_relevance` for the same key: the row's value is used |
| 3 | `dry_stub.py`, `ROLE_STEPS` / S1 | After `collect`: for each required source with `relevance: pending` whose key IS in `source_relevance`, run `ticket_adapter.py peek <KEY> --output <inventory>`, then `ticket_adapter.py assess --output <inventory> --source-id <id> --relevance <v> --reason <r> --assessment-ref <the path peek wrote>`. A key not named stays `live_only` (today's text). A failed command is `live_only` with its stderr verbatim (cut at 400, as `:163`) | (a) named key: both commands are built with exactly the data values (argv compared); (b) unnamed key: `live_only`, no command; (c) `assess` exit != 0: `live_only` with the refusal text |
| 4 | `dry_stub.py`, cascade after `relevant` | Run further steps only if they are reads that decide nothing (e.g. the complete collector for a kept source: `source_inventory.py:3220` "Relevant remains pending until the complete collector replaces it"); each one is named in the report with its s1.md line. A step that judges (`inspect --inspection-status`) is `live_only` with its reason | Selftest: a kept source left `pending` after `assess relevant` with no read step gives `live_only` naming it |
| 5 | `dry_stub.py`, `pending_judgments` | Reads through `source_inventory.load_inventory` | the existing three cases plus the missing file stay green |
| 6 | `form-fill-rules.json` (only F-R3-4 (a)) | Register template gains `## Branches` with `Branches: none -- <why>` and `## Source obligations` with one `\| rest \| unreconciled: <why> \|` row (headers exactly as the contract, `branch_accounting.py:738-740` refuses another header); an `## Attachments` `rest \| not_opened` row only if the S2 refusal asks for it; grounding: the hunk path comes from a data token over the world's diff (the first file of `impl_diff`) ONLY if an existing generator yields it, otherwise `live_only` (non-goal: new generators) | `test_field_producers.py` rows: the register template carries both sections with the contract's header; the `rest` row is present |
| 7 | `dry_world.py`, `gate_verdict` / spike print | `gate: <verdict> (...)` only when `statuses()["S3"] == "done"`; else `gate: undecided -- the road ended at <stage>: <first 160 chars of its outcome line>; measured: S0..<stage> <s> s, row median <s> s` | two rows: S3 done / S3 not done |
| 8 | `dry_world.py`, rows | Before the rows, hash the snapshot tree of each `start` (sha256 over sorted relative paths + bytes). After the rows, hash again; a difference is red `snapshot changed by a row: <name>` | selftest on a temp tree: a byte change between the two hashes is red |
| 9 | `probe.json` | Row `halt/words` may gain `"s1_review": "go on"` (the words of row 1), the same move R2 item 6 made for row 2, so it can reach its named state now that S1 can pass the review | reported outcome per row; nothing hand-tuned beyond that one key |

#### Edges (behaviour | invariant)

| # | Edge | Behaviour | Invariant protected |
|---|---|---|---|
| E-R1 | Pending required source not named in the data | `live_only` naming the source; no `peek`/`assess` | the stub never makes a judgment up (AR-29, A1-E3) |
| E-R2 | Data names a key that the inventory does not hold as a pending required source | NOTE `unused judgment <key>` (same class as A1-E2 "unused words"), not PASS, not red | a declared answer is never applied to another source, and never vanishes without a line |
| E-R3 | Malformed data: value outside `relevant\|not_relevant\|unknown`, empty or whitespace reason, a key twice (JSON cannot hold two equal keys, so the check is on case-folded duplicates), `stub` not a mapping | red with file and key, before the world is built (A1-E4 form) | an unknown declared value never reaches the factory (AR-28) |
| E-R4 | Today's code refuses the `assess` (a source `excluded_by` the person, `source_inventory.py:3198-3209`; unsafe `assessment_ref` `:3191-3192`; more than one match `:3195-3196`) | `live_only` with the refusal verbatim; no second attempt with another value | the stub never searches for a value that passes |
| E-R5 | `peek` gets a 404 from the world (no route) | the source is recorded as the live code records it (A1-E8); `assess` still runs with the declared value if `peek` wrote an assessment path, otherwise `live_only` | what the world does not hold is a gap, never an invented answer |
| E-R6 | TEMPORAL: `stub` in `dry-types.json` and the new templates are created by this round | before it: round-2 behaviour (relevance `live_only`); after it: declared. `load_types()` accepts both. The move that creates them is items 1 and 6 of this node | the round-2 world stays readable, and nothing becomes declared silently |
| E-R7 | S3 not reached (any cause, including a cascade of item 4) | gate line `undecided -- ...` (item 7) | an unknown never becomes `continue` (AR-28, FR-41) |
| E-R8 | A probe row writes into its snapshot (a path taken from the un-rewritten `events.jsonl`) | red `snapshot changed by a row: <name>` | the snapshot never changes (P1-b `:445`, E16) |
| E-R9 | LIMIT: the road reaches `max_turns` 12 / `--max-boundaries` 40 (`dry_world.py:416-422`) with S2/S3 added | the stop prints `12 turns without reaching gate A` (`:449`); counts as E-R7 | a long road is never cut into a pass |
| E-R10 | LIMIT: stderr cut at 400 chars (`dry_stub.py:163,181`) and the gate line's outcome cut at 160 | the cut text keeps its head; the full text stays in the stub journal | a cut never hides which command refused |
| E-R11 | CONFLICT: "the stage closes" vs "no hand-written output / no new generator" | the no-hand-written rule wins: `live_only` with the reason, and the road ends there | the dry layer is never built on hand-written forms (P1-b reason A, E13) |

#### Tests (docs/TESTING.md)

No new test file. Every new case is a row in the existing `dry_stub.py --selftest` table (items 1-5, 7, 8) and, only under
F-R3-4 (a), a row in `test_field_producers.py` (item 6). The adversarial battery for outside input does not apply: the type row
is internal fixture data. E-R3 covers malformed input in the A1-E4 form already used by `load_types()`.

---

## 6. Forks (returned, not decided)

**F-R3-1. Round 3, or judge the gate as it stands.**
- (A) One bounded round 3 using option (b), the node in section 5. Cost: one builder round and one CI run; the S2/S3 reach is
  uncertain (J10, J16). It answers feasibility (S1 surely, S2/S3 as far as the declared forms reach) and makes the gate line
  honest.
- (B) Judge now under option (c): fix only the gate line (a small-work batch item) and record the verdict as "time: continue,
  measured on S0 + S1 to the review; feasibility of S2/S3 not shown". N2 inherits J4/J10/J16 as its first items. Cost: zero
  builder rounds. Risk: N1/N2 start on an unproven premise (P1-b `:540`).
- (C) Round 3 using option (a). Breaks A1 `:97,:99,:100` and F-A1-4 (b), and is infeasible past J4 (section 2).
- Recommendation: **(A)**, bounded. It is N0's last round. Whatever stop it ends at is labelled, and the gate is judged on
  that.

**F-R3-2. Where the declared judgment lives.**
- (a) The type row's new `stub` field (P1-b row grammar, `:257`), which a walk row's `stub` overlays.
- (b) Only in walk rows. This needs a "main pass row", which does not exist today; `Road` takes words from the union of probe
  rows, `dry_world.py:398-405`.
- (c) A new per-type file.
- Recommendation: **(a)**. One grammar for type and row, one road (P31). A per-story fact sits with the story's data.

**F-R3-3. The declared value for TP1-15791.**
- (a) `relevant`: the recorded run's verdict (`source-inventory.json:432-433`), so no judgment is invented. It may cascade
  (item 4, J5), and it enlarges S2's unit set (the units of the kept ticket).
- (b) `not_relevant`: a shorter road, but the dry world states a verdict the real run did not make.
- Recommendation: **(a)**. If it cascades into a judgment with no data value, the round stops there, labelled. The builder
  does NOT switch to (b); the Lead decides after the report.

**F-R3-4. May round 3 add the contract's empty/remainder forms to the S2/S3 templates?**
- (a) Yes, limited to forms the contract declares (`artifact-contract-plan.md:20-27`), each with its derivation line. The
  result is a gate-A debt (`source_unreconciled`), honestly labelled.
- (b) No: S2 stops `live_only` at `branch_accounting`.
- Cost of (a): `form-fill-rules.json` and `test_field_producers.py` move into the owns. Possible overlap with P1-a's nodes,
  which the Lead checks.
- Recommendation: **(a)**. Without it the round is very likely to end at S2, and the feasibility question stays open.

**F-R3-5. Wording when the road ends early.**
- (a) `gate: undecided -- ...` with the measured part.
- (b) `gate: continue (partial road)`.
- Recommendation: **(a)**. Under (b) a reader of the gate line alone still reads "continue" (AR-28, FR-41).

---

## 7. Small choices I closed (no design weight)

- S-1. An unused declared judgment is a NOTE, not red: the same class and treatment as A1-E2 "unused words".
- S-2. Snapshot hash: sha256 over sorted relative paths plus bytes; it lives only in the test run.
- S-3. The gate line's outcome cut is 160 characters (the stub journal holds the whole text).
- S-4. The CI start stays as in R2 `:56-57` (`gh workflow run ... -f spike=true`); `canon.yml` is unchanged.
- S-5. `plans/features.json` registration (R2 Q2) stays outside the node: it is a Lead small-work item, not N0's.

## 8. Analogs and contradictions noticed (not widened)

- In round 2 the driver asked `s1_review` while a required source was still `pending`. The person's answer then could not be
  recorded (`source_inventory.py:3408-3411`), and the road fell to the conductor. Yet the code's own summary tells "awaiting
  review" apart from "pending" (`awaiting_review` is false while any required source is pending, `source_inventory.py:3046-3047`).
  A live scout normally assesses before ending, so this may only show up in the dry world. Whether the driver should send a
  pending source back to the role instead of asking the person is a question for the owner of `driver_dispatch.s1_person`
  (`:395-408`). It is reported here, not in scope.
- `dry_stub.pending_judgments` reads the inventory with `json.loads` (`dry_stub.py:81`) instead of the package reader (AR-13).
  Folded into item 5.
- The gate formula's 15-min estimate (P1-b `:536`) and the "continue" thresholds (120 s, 20 s) disagree: at the threshold values,
  2.5 x 120 + 120 x 20 = 2,700 s = 45 min. Whether the cap applies per CI part (F6 (a)) or per job is for the Lead, when it
  sets the cap after N0.
- The R1 analog (`FakeJira` vs `TrackerServer`, a clone candidate) still stands (R2 `:135`).

## 9. Reading trail

Read: R2 whole; R1 whole; P1-b `:1-570` (header, sections 1-4, section 5 E1-E22, section 6 N0/N1/N2 head); A1 amendment
`:1-437` (sections 0, A1, A2, A3, A4 head); `dry_stub.py:1-230`; `dry_world.py:210-527`; `form-fill-rules.json` whole;
`dry-types.json` whole; `probe.json` whole; `stages.json:1-140`; `source_inventory.py:2485-2500, 3035-3053, 3185-3224, 3395-3419`
(plus a Grep for `relevance`); `ticket_adapter.py` (Grep: `peek` `:2738-2752`, `assess` `:3000-3010`, args `:2448-2475`);
`branch_accounting.py:1-40, 730-780` (plus a Grep for headings and `no home`); `artifact-contract-plan.md:15-34`;
`planning_contract.py:1011-1055` (plus a Grep for `hunk`); `driver_dispatch.py:29-31, 395-414, 715-754`; Grep for `s1_review` over
`driver_*.py`; snapshot `investigation-14857\TP1-14857\work\source-inventory.json:380-439` (plus a Grep for relevance),
`requirements-register.md` headings (Grep `^## `), and a Glob of the snapshot tree.
Negative claims with controls: "the snapshot has no grounding.yaml/context-manifest.json/understanding.md" (the same Glob found
`work/test-plan.json`); "the register template has no `## Source obligations`/`## Branches`" (read whole at
`form-fill-rules.json:276`, a direct read, not a search).
Not read: `form_filler.py` (generators: the node forbids new ones, so their list is not load-bearing here); `peek_jira_source`
body (what `peek` writes as the assessment path: the builder reads it, item 3); `sizing.py`; the bodies of
`planning_contract`'s hunk checks (J16 is marked "likely", not "certain"). Glob over the worktree's `docs/tasks/specs` returned
nothing (likely a Glob limit on the `.claude` path), but direct Reads of the report files there work. The P1-b spec and A1
were found under the main repo's `docs/tasks/specs`.
