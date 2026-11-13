# TQ2-1 revised for the owner's option (c): the designer writes one case with a table of values; a critic `merge` stays an instruction to the automator, and it must reach the step that groups tests

Draft by the designer, 13.11.2026, revising `docs/tasks/specs/20261113-tq2-1-case-merge-spec.md` (t-579 draft, "the old draft"
below) for node TQ2-1 of `plans/piles/test-code-quality/batch-2-sliyanie-kejsov-i-chitateli.md`. **Fix round of 13.11.2026** after the
critic-on-plan verdict `docs/tasks/specs/reviews/20261113-tq2-1-revision-plan-critic.md`: every change is listed in §11.
Package read on the worktree `C:\QAFactory\forge-repo\.claude\worktrees\read-main` at **origin/main 5cc4f88** (the first draft read
be2c988; every file:line of §C and §D below is re-taken on 5cc4f88; the root checkout is stale).
P = `C:\QAFactory\forge-repo\.claude\worktrees\read-main\ai-packages\qa-factory` for READING; the `owns:` paths below are written
under `C:\QAFactory\forge-repo\ai-packages\qa-factory\...` (the builder's worktree mirrors them).
Acceptance of this draft is the Lead's. Forks F1-F6 are decided by the Lead, (a) each (§7). New forks F7-F9 (§7) are returned with
a recommendation; §C-§D are written ON the recommendations.

---

## 0. The owner's word, and what it means

**Verbatim, the owner, in the session with the owner, 13.11.2026, on fork F1 of the old draft (chose option (c)):**

> «давай такой вариант. Если критик найдёт что сливать, то это будет инструкция для автоматизатора, как и сейчас. Количество ручных текстовых кейсов не критично, а вот автоматизация с одинаковыми шагами удлиняет время прогона»

**The Lead's reading (carried here as the Lead's reading, not the designer's):**
1. NO `Archived` status written by the factory, no `merged_into`, no fold state, no reader changes. Nodes N1–N4 of the old draft
   are DROPPED. The standing choice of spec t-723 B-1 ("a `merge` changes no case", `docs/tasks/specs/t-723-tq1-27-amended.md:16-19`,
   :376) is CONFIRMED by the owner, not reversed.
2. The designer gets a PROACTIVE rule only: when it writes cases, one case with a table of values instead of several cases that
   differ only in input (P16's example: -1, 0, 1.5, «абв» all turned into 1 = ONE case).
3. A case critic's `merge` answer stays what it is today: an instruction that rides to S5, where the automator parametrises.
4. The owner's VALUE: the count of manual text cases is not critical; automation with identical steps lengthens the run. So the
   automator-side route (one parametrised test, shared steps not repeated) is the part that must not leak.

**What this revision finds (the load-bearing fact, §C):** point 4 CAN leak today. The `merge` instruction reaches S5, but it reaches
the WINDOWS, after the S5 plan has already decided which cases share a test; the windows are cut FROM those tests and packed by
order and cap. The plan dispatch, the only step that makes two cases one test FOR CERTAIN, is not handed the instruction when its
plan is under the guard's read cap (it is handed it when the plan is over the cap: two roads, P31). On the driver process (legacy
S5 form) the instruction reaches no S5 brief at all. Node K2 closes both; the part of the legacy road no brief can close (partners
the cut-by-cases puts in two windows) is fork F7.

---

## 1. AR-n and FR-n touched, change checks, owners and census class (designer rule 1; CLAUDE.md rule 10; AR-29)

| AR | Node | How touched | Change check (in the node's DoD) |
|---|---|---|---|
| AR-29 (code judges data, a role's judgment by a tier above) | K1, K2 | K1: the value-table rule is tester craft, no code check judges it. K2: code JOINS the critic's merge ids against the plan's `tests[].cases` and computes ADVICE (a hint); whether to follow it is the automator's (P17); whether an unanswered merge blocks is the plan critic's judgment (F5 = a). | K2: no new function holds a `raise` statement; `merge_hints` changes no finding, verdict, exit code or `ok` (table row G9); census unchanged (`test_judgment_census.py` green, no new row) |
| AR-21 (what a stage gathers travels whole) | K2 | The S4 critic's carried concerns (CC-n) reach the S5 plan dispatch (author and plan critic) and every legacy window (its own cases) as they reach the planned windows | rows B1-B4, B7-B8 |
| AR-13 (a fact with a reader is read only through it) | K2, N5 | CC-n only through `s5_plan.case_concerns` / its new report `concern_report` (s5_plan.py:1146-1160); the ids after the merge token only through one new `critic_rollcall.parametrise_group` (also used by `_carries`, :914-919); one placement rule `s5_plan._placement` (:1180-1195) for planned and legacy windows; N5: one column reader | critic confirms no second reader of `PARAMETRISE_TOKEN`, of the concern list or of placement in the diff |
| AR-15 / AR-19 (one survivor; twins change together) | K2, K1 | One printer of remark lines (`s5_plan.remark_lines`, extracted from `render_slice` :1358-1364) for the window slice and the side file; one placer (`s5_plan.placed_remarks`, extracted from `window_slice` :1296-1300) for planned slices and legacy windows. K1: designer rule and the case critic's dimension 2 (`qa-case-critic.md:41`) are twins; the critic's :44 wording is corrected in the same commit | existing window-slice rows of `test_brief_pack_s5_plan.py` stay green; K1 key 2 |
| AR-18 (one output shape, one reader) | K2 | merge hints have the grouping hints' row shape `{case, message, fix, tag}` and the one printer `print_hints` (s5_plan.py:1460-1465) on both paths (`--check`, `s5_precheck.plan_result` :4296-4300) | row G9: the same hint line on both paths |
| AR-10 / FR-10 (requirement before the work; one packet does not contradict itself) | K2 | the plan author's head line says a `parametrise into one test:` concern is answered IN THE PLAN; the plan critic gets the merge hints on their OWN line, never counted under the grouping line that says "never a blocker on its own" (brief_pack.py:2015-2017) | row B2: the critic head carries both lines, the grouping count excludes merge rows |
| AR-23 (empty outcome declared) | K2 | no concern carried -> one files line naming which empty it is | rows B5, B6 |
| AR-28 / FR-41 (an unknown never becomes a pass) | K2 | concerns unreadable -> a head line says so; rounds whose receipt did not match -> named as unread, never "none carried"; merge hints not computed -> a `not checked` note | rows B6; G-table "why" |
| AR-20 (shrink-only ratchets; a raise is named) | K1, K2 | four named raises and one compensation, numbers in §D.0 | K1/K2 DoD: `role_load.py --all --json` and the ratchet line of `test_brief_pack_s5_plan.py` before/after, each raise in the diff with its reason |
| AR-22 (every field read has a producer) | — (F4) | `Archived` is read by two code readers (`critic_rollcall.py:1037`, `case_stamp.py:535`) and is a legal value (`validate_artifacts.py:76`); the factory writes it nowhere | F4 = a: no change, reason written (§A.3) |

FR touched: K1 — FR-30 (no Cyrillic: the P16 example is written `"abc"`, as `qa-case-critic.md:41` does), FR-33 (proved by a live
run, §E.3), FR-47, FR-52. K2 — FR-49 / FR-38 (the instruction reaches the role that can act, before its work), FR-17 (the concern
carrier is wired where the problem occurs: the plan and every legacy window), FR-12 (code reads the fixed token and ids, never prose),
FR-4 (an unanswered merge is stopped silent, never informed: F5 = a), FR-10 (B1), FR-41/FR-59, FR-54. N5 — as the old draft.

Checks added or altered (owner it serves; census class from `scripts/tests/fixtures/judgment-census.json`):

| Check | Where | Owner | Census class |
|---|---|---|---|
| value table instead of near-duplicate cases | designer charter `## Techniques` (craft); critic dimension 2 judges | judgment (designer; the case critic accepts, gate A above it) | not a code unit |
| "the plan does not follow a case-critic merge and gives no `apart_reason`" | new `s5_plan.merge_hints` / `merge_hint_rows` (advice, printed by `--check` and `s5_precheck.plan_result`, and counted on its own line in the plan critic's brief) | data (code computes the join) | none: advice with no refusal site and a name outside `UNIT_NAME_RE` (test_judgment_census.py:69), like `grouping_hints`, which has no census row (s5_plan rows :885-894) |
| is the unfollowed merge acceptable; is the `apart_reason` a real one | plan critic, rubric «On the plan», one new bullet | judgment (code critic of the plan; the driver accepts) | not a code unit |
| the plan dispatch and the legacy windows are handed the CC-n | `brief_pack.plan_dispatch_lines` (existing census row :60, class shape), new `case_concern_lines`, `build` | data | shape (row :60 unchanged; `case_concern_lines` and `build` match no unit pattern; no new raise) |

---

## A. The revised node list

### A.1 Kept / new nodes

| Node | What | Status vs old draft |
|---|---|---|
| **K1** | Designer charter: the value-table rule (craft, one rewritten bullet); case critic :44 wording made true at the same byte length; one `role-rules.json` row; one named ratchet raise | replaces old N4 (no fold form, no `Archived`, no contract text) |
| **K2** | The case critic's carried concerns reach the S5 PLAN dispatch (author and plan critic) on both cap roads and every driver/legacy window (its own cases, one placement rule); one advice hint when the plan leaves a merge pair in different tests with no `apart_reason`, on its own line for the plan critic; one rubric bullet; named ratchet raises | NEW — found by §C |
| **N5** | One column helper for the roll-call and merge-table readers (old §6 N5, unchanged in substance, restated inline) | kept per F2 |

### A.2 Dropped (the owner's word)

Old N1 (contract: status/fold in the index), N2 (delivery readers), N3 (S4/S5/gate A readers and the fold check), N4 (fold form,
`Archived`, contract text). Old forks F1 (closed by the owner), F2–F8, F10–F11 fall with them, except F10's home question, which
stays with N5 (§D N5 keeps `contract.md_column`). Old F9 (critic rule allowed?) reappears narrowed as F6.

### A.3 "Reader hardening" without a producer of `Archived` — is anything still a live defect?

Facts (Grep `Archived` over `P\scripts\*.py`, case-sensitive; positive control: the same call finds `validate_artifacts.py:76`):
- `validate_artifacts.py:76` — `Archived` is a legal value of `CASE_STATUS` (a write-time closed list).
- `critic_rollcall.py:1037` — the S4 merge check leaves an `Archived` case out of `live` (exact word only); `:859` names it in the
  form refusal.
- `case_stamp.py:535` — the stamp skips a `Blocked` or `Archived` case.
- No package code WRITES `status: Archived` (the old draft §1.1 row 1e; the other hits are the STORY flag and test fixtures).
- Delivery readers (`check_delivery._completeness`, gate A, ledger) do not know `Archived`: an `Archived` case still owes work there.

Verdict: **no live defect**. The value has a producer — a person's hand edit of a case file, which the contract accepts — and each
of the two readers errs to its consumer's safe side: the stamp does not mark a retired case `Automated`; the merge check asks no
pair for it. A delivery reader that still demands the case's test gives `no`, never `yes`, so the hand edit never turns into a pass
(AR-28). Removing the enum value would make a hand edit fail at write time; nobody has measured whether project stores hold
`Archived` cases (PROJECT.md, package change item 6(a)). F4 = (a): leave all three as they are, and record the reason (§E.1).

---

## B. The overlap with RC1-2 (one home for the designer line)

Facts: `plans/piles/onboarding-forge/batch-1-onboarding-roles-forge.md:44` RC1-2 "P16 в уставах стратега, дизайнера и критиков",
status «ожидает», depends on RC1-1, inside a batch «в работе» (dev1, 12.11.2026, `:3`), so that batch is FROZEN (PROJECT.md
«Командная работа» item 2). Its source B-188 (`plans/BACKLOG.md:168`) spells the designer part: "дизайнер (объединять кейсы с
параметрами, id параметра называет кейс)". That is the same sentence as K1. The TQ2-1 batch is «ожидает», not taken
(`batch-2-sliyanie-kejsov-i-chitateli.md:3`), so its row can still be edited.

F1 = (a), decided: **K1 carries the designer line.** RC1-2 keeps the strategist and the code critic. The pointer, so two builders
never write the same sentence:
- the Lead of `onboarding-forge/1` adds to that batch's «Ход» (a legal edit of a taken batch):
  `13.11 — RC1-2: строку P16 в устав дизайнера («один кейс с таблицей значений») пишет TQ2-1 (test-code-quality/2), слово владельца 13.11.2026; RC1-2 пишет только стратега и критика кода; исполнитель RC1-2 сверяет `agents/qa-case-designer.md` и не дублирует строку`
- TQ2-1's row (§E) names RC1-2 as the twin and says it does not touch the strategist or the code critic.
- File zones: both batches name `agents/qa-case-designer.md`. If `piles.py take` refuses TQ2's batch on check (б) while
  onboarding/1 is still in work, write `очередь: onboarding-forge/1 → test-code-quality/2` in both files. TQ2-1 is then the later
  side and merges `main` into its tree (D-0048). If one developer takes both, no line is owed (the owner, 13.11.2026).
- RC1-2 also writes the code critic, whose start load carries `references/code-review-rubric.md` (inject-map.json:72): K2's rubric
  bullet and its `process_ratchet_tokens["qa-code-critic"]` raise (§D.0) meet RC1-2's code-critic text in the same row. The later
  side re-measures and re-sets the row (it is exact, slack 0); named in X5.

---

## C. The automator side: does the `merge` instruction reach the automator whole, and is it acted on?

### C.1 The carrier chain (file:line on read-main 5cc4f88)

| # | Link | Carrier | What it carries |
|---|---|---|---|
| 1 | critic writes | `agents/qa-case-critic.md:42-46` (2b) | `## Merge candidates` row `merge`; each case's roll-call `note` holds `parametrise into one test: <ids>`, verdict `approve_with_concerns` |
| 2 | S4 exit holds it | `scripts/critic_rollcall.py:1030-1049` `merge_candidate_errors`; `:922` `_merge_concern_errors`; token `:57`; `_carries` `:914-919` | a merged case approved without the token is refused at the S4 exit |
| 3 | round read | `critic_rollcall.py:404-431` `_read_round` (one CC per case of every `reviewed: yes` row with `approve_with_concerns`; `problem` = the note verbatim, :426); `:434-442` `accepted_rounds` | the note WHOLE, receipt-checked: a round whose receipt measured other bytes lists nothing and carries nothing, and says so on stderr only (:398-400, :407-409) |
| 4 | to S5 remarks | `scripts/s5_plan.py:1116-1143` `_file_concerns` (latest listing round decides), `:1146-1160` `case_concerns`, `:1077-1092` `remarks_of` (chain remarks + CC-n) | CC-n as `kind: remark`, `case` = the roll-call's case id, `expected` names the findings file |
| 5 | placed per window | `s5_plan.py:1180-1195` `_placement`; `:1296-1300` in `window_slice` | a CC goes to the window holding its case; unplaced (a case no window holds, e.g. a bare id against area-keyed scope keys) -> every window |
| 6 | printed for the window | `s5_plan.py:1358-1364` `render_slice` "## Remarks (plan review and case critic)"; `scripts/brief_pack.py:2076-2103` `plan_lines` (side file named "the remarks for them (the plan review's and the case critic's concerns)", :2101-2102); resumed window: `delta_lines` :2525 / `_delta_tail` :2561, "Remarks of this window with no `plan_remarks` row" :2575-2580 | the planned window automator reads each CC-n |
| 7 | answered | window form `plan_remarks` (`agents/qa-automator.md:24`, `:69`); `s5_plan.remark_rows_missing` `:1163-1177`, called by `s5_precheck` C12 :4465-4468 (planned windows: it reads `self.piece`); rubric «Conformance to the plan» C12 (`references/code-review-rubric.md:34`) | `applied` / `not_applicable` with a reason |
| 8 | shown to the person | `scripts/gate_brief.py:2226-2234` (through `case_concerns`), printed at :3038 "Concerns carried to automation" | the list at gate A |

### C.2 Where the instruction is lost or cannot be acted on

**Gap G1: the step that makes "one parametrised test" certain is not handed the instruction (plan under the cap).**
- The S5 PLAN dispatch decides grouping: its author head line says "Cases with the same setup and action are one parameterized
  test" (`brief_pack.py:2005-2007`), and it writes `tests[].cases` into `work/s5-plan.json`.
- The windows are cut FROM those tests: "the cases one test covers being one window (`pack_windows`, ...)" (`controller.py:4524-4525`,
  `s5_windows_for`; groups = components of `s5_plan.test_adjacency`, `case_groups` s5_plan.py:157-196). `pack_windows`
  (`controller.py:414-443`) places groups first-fit into the first window of the same surface with room for the whole group.
  Caps: UI `config.dispatch.ui_window_cases`, **default 2** (`DISPATCH_DEFAULTS`, controller.py:271, read by `_dispatch_setting`
  :4287-4303; `or 1` at :4540 applies only when a project sets 0); other surfaces `config.execution.s5_window_cases` when set
  (the driver experiment runs 8), else `dispatch.api_window_cases`, default 4 (`_s5_window_cases` :4305-4320).
- Under the guard's whole-read cap the plan dispatch is handed only the plan file (`brief_pack.py:2022-2025`). The skeleton holds
  `case, requirements, s3, thens, remainders` and no concern (`s5_plan.py:319-323`). Its read list (`_input_names`,
  brief_pack.py:3550-3562 = S5 `inputs` + `ROLE_FILES["qa-automator"]` :99) names no S4 `critic-findings.md`. The plan critic gets
  grouping hints computed from tests in one file at one level (`brief_pack.py:2011-2017`, `s5_plan.py:1405-1433`), not from the
  case critic's merge. Rubric «On the plan» (`code-review-rubric.md:12-28`) does not name the case critic's concerns.
- Result: when the plan author does not group the pair, the two cases sit in different tests, so in different groups. Whether they
  then share a window depends on order and cap: two single-case UI groups land together only if they are next in packing order and
  the window still has room (cap 2); any group placed between them, another surface, or a project cap of 1 puts them in two windows.
  A pair in two windows cannot be merged by either window (rubric :20-21 "the window may parameterize" acts inside one window;
  `qa-automator.md:52` "write all the cases of one test in one window"): each answers `not_applicable`, and two tests with identical
  steps ship (the owner's point 4). A pair that does share a window can be merged only as a declared deviation from the reviewed
  plan. So the leak is **conditional, not certain**; the plan dispatch is the only step that makes the pair one test for certain.
  t-723 E21 and L4 (`t-723-tq1-27-amended.md:241`, :402-403) flagged "partners in different windows" as unverified; the answer is
  this paragraph.
- Over the cap, the plan dispatch IS handed per-window slices (`brief_pack.py:2026-2046`) rendered by `render_slice`, which prints
  the CC-n remarks (`window_slice` -> `remarks_of` -> `case_concerns`). **Same input, two roads by plan size** (P31). K2 makes it one.

**Gap G2: the driver process (legacy S5 form) carries no CC-n to any S5 brief.**
- `s5_plan.mode` gives `legacy` to the driver process before the first S5 record and to any story whose S5 windows began without a
  plan (`s5_plan.py:405-408`; pinned by `test_s5_plan.py:253`, :258, re-read on 5cc4f88: both lines unchanged).
- A legacy S5 is cut by CASES, not tests: `_scope_windows` calls `split_windows(list(scope), ...)` when the form is not planned
  (`controller.py:4428-4443`); `split_windows` = `pack_windows` over groups of one case (:446-449). A legacy window brief is built
  with `scope` = its dispatch's scope (`brief_pack.py:4180`).
- In `brief_pack.build` only `s5_kind == "plan"` and `"window"` get plan lines (chain `brief_pack.py:4244-4256`); `legacy` gets none,
  and `_resumed` delta runs only for `plan`/`window` (:4363). Legacy has no slice and no C12 (link 7 runs on a planned piece).
- Negative claim, with its trail: Grep `carried_concerns|case_concerns|remarks_of|accepted_rounds`, case-insensitive, over
  `P\scripts\*.py` -> non-test hits only in `critic_rollcall.py` (definitions), `s5_plan.py` (:28-29, :1077-1092, :1133, :1146,
  :1297), `gate_brief.py:2226`, :2234 (gate A), `brief_pack.py:2566` (`_delta_tail`, plan blockers of a resumed plan/window).
  None sits on a legacy brief path. Positive control: the same call found the definition `s5_plan.py:1146`.
- `brief_pack.digests` (:1581-1615, read end to end on 5cc4f88) prints each earlier stage's `digest` (or reason) cut to
  `DIGEST_CHARS` and this stage's other dispatches' digests; it names no findings file and no CC. The first draft's estimate ("a
  legacy window may see a path to critic-findings.md") does not hold. No carrier.
- Nightly and comparative runs go through the driver (`docs/RUNBOOK.md` §9, cited from PROJECT.md, not re-read). On that road no
  case-critic concern reaches the automator. F3 = (a): K2 hands each legacy window the concerns of ITS cases (one placement rule
  with the planned windows). What no brief can fix: partners the cut-by-cases puts in two windows (fork F7).

**Not a gap (stated so nobody re-opens it):**
- Link 3's drop on a receipt mismatch is by design. Its invariant: a concern is never taken from bytes the critic's receipt did not
  measure (I3, FR-59). K2 makes the drop VISIBLE in the brief (A4), never undoes it.
- The handoff contract `handoffs/gate-a-to-automator.yaml` names no concern field (Grep `(?i)concern|CC-` over
  `handoffs/*automator*.yaml` hits only `s5-critic-plan-to-automator.yaml:12` and `s5-critic-to-automator.yaml:63`, the positive
  control of the same call; handoffs unchanged be2c988..5cc4f88 is not re-measured: estimate, not verified). CC-n rides the code
  route `remarks_of`, which `s5_plan.py:28-29` documents. Reported as an analog (§9), not widened.

### C.3 Is the automator told the craft?

Yes, nothing missing in the charter (re-read on 5cc4f88):
- `agents/qa-automator.md:50`: "The same setup and action is one parametrised test: the data and the expected value, taken from
  each case's oracle, are its parameters, and the parameter id names the case" (P16, P17).
- `:51`: a consolidated scenario or tests kept apart, said in words.
- `:52`: split by the failure you would diagnose; all the cases of one test in one window.
- `:62`: a red hides no other (P29).
- The plan author's brief head line repeats the rule (`brief_pack.py:2005-2007`).

The missing link is DATA at the right moment (G1, G2), not craft. So K2 is a code node, and the automator charter is not touched.

---

## D. Nodes, dispatchable

Order: K1 -> K2 on the batch branch (K1 and K2 each write one `role-rules.json` row and different keys of `references/role-load.json`;
K1 lands first, K2 merges it; disjoint rows/keys). N5 runs in parallel with both: its owns are disjoint from K2's (`critic_rollcall.py`
functions differ, D-0048). Every builder dispatch carries in `given` the whole `P\design\factory-rules.md` and
`C:\QAFactory\forge-repo\plans\builder-rules.md` (PROJECT.md, package change item 1). Live proof: one live-runs row covers K1 and K2
(§E.3).

### D.0 Ratchets K1 and K2 touch (B2): old value, measured need, decision

Measured at 5cc4f88 by the plan critic (verdict, trail "reruns"): `role_load.py --all --json` -> `qa-case-designer` 13316 tokens,
`qa-case-critic` 18296; `test_brief_pack_s5_plan.py` -> `RATCHET S5_PLAN_BRIEF_BYTES_MAX 9520`. The designer has no shell; the needs
below are byte counts of the expected text divided by `bytes_per_token` 4 (role-load.json:5), estimates the builder replaces by the
before/after measurement. A raise sets the row to the AFTER-measure (role-load.json:2: a row stays at the measured maximum), with the
reason in the diff; a measured delta above the stated bound is a stop and a question (something else grew), never a bigger raise.

| # | Ratchet (carrier) | Old | Room at 5cc4f88 | Need | Decision |
|---|---|---|---|---|---|
| R1 | `ratchet_tokens["qa-case-designer"]` (role-load.json:14) | 13320 | 4 | +154 B (the bullet: 127 B -> 281 B) ≈ +39 tokens | **named raise (K1)**: 13320 -> the after-measure (≈ 13355); bound: delta ≤ 50 tokens. Reason line in the commit and the K1 report: "AR-20 raise qa-case-designer 13320 -> <n>: TQ2-1 K1 value-table rule (owner 13.11.2026, option c)". No compensation: the only owned text is the bullet itself, and the rule needs its words |
| R2 | `process_ratchet_tokens["qa-case-designer"]` (:28) | 12079 | 0 (exact) | 0: the bullet is under `<!-- kind: craft -->` (`qa-case-designer.md:46`) | unchanged; the after-measure must equal 12079 |
| R3 | `ratchet_tokens["qa-case-critic"]` (:15) | 18296 | 0 | 0 B: the :44 parenthesis is rewritten at the SAME length (59 B -> 59 B, text in §D-K1) | **compensated inside the owned parenthesis**; the after-measure must equal 18296; process (:29, 15929) unchanged (section :27-76 is craft) |
| R4 | `S5_PLAN_BRIEF_BYTES_MAX` (`test_brief_pack_s5_plan.py:541`) | 9520 | 0 | +39 B: the K7 plan-critic story has no S4 round, so its brief gains the files line `- case critic's concerns: none carried` (38 B + newline); no merge line (no concern) | **named raise (K2)**: 9520 -> the measured `RATCHET S5_PLAN_BRIEF_BYTES_MAX <n>` after the change; bound: 1 ≤ delta ≤ 60 B. The constant's comment gains: `TQ2-1 K2 (AR-20): +<d> B, the plan brief states the case critic's concerns, "none carried" on the K7 story (AR-23)`. Rejected compensation: printing nothing for 0 concerns would leave the empty outcome undeclared in the one brief that must act on it (AR-23) |
| R5 | `process_ratchet_tokens["qa-code-critic"]` (:31) | 17596 | 0 (exact, both directions: role_load.py:280-287) | the new rubric bullet ≈ 314 B ≈ +79 tokens, IF `delivered_text` hands the code critic the «On the plan» section (the rubric is injected whole by inject-map.json:72 as far as read; the rubric carries no craft marker, so it is process) | **named raise (K2)**: 17596 -> the after-measure, whatever it is, bound delta ≤ 100 tokens; reason "AR-20 raise qa-code-critic process 17596 -> <n>: TQ2-1 K2 rubric bullet, an unanswered case-critic merge (F5 = a)". Not measured in the critic's verdict: the builder's before-run gives the room |
| R6 | `ratchet_tokens["qa-code-critic"]` (:17) | 19420 | not measured | as R5 | raise to the after-measure ONLY if it exceeds 19420 (same reason line); otherwise unchanged |
| R7 | `ROLE_BRIEF_BYTES_MAX` (`test_brief_pack.py:2364-2368`, every role's brief at a dispatch id the seeded story does not hold) | per role | not measured | 0: K2 adds nothing to a brief whose dispatch has no record (the legacy branch requires a dispatch record, §D-K2 item 5; the plan branch requires a plan record) | not touched; red -> stop and question |

### K1 — the designer's value-table rule; the case critic's wording made true

given: this spec §0, §1, §D.0, §D-K1; P\agents\qa-case-designer.md; P\agents\qa-case-critic.md (lines 38-46); P\design\role-rules.json
(rows :26, :161 as the form); P\references\role-load.json (whole; :2 is the rule of the rows); P\references\artifact-contract.md:71-76
(partitions `P-<name>`), :80-88 (`preconditions[].partitions`); P\design\factory-rules.md (whole);
C:\QAFactory\forge-repo\plans\builder-rules.md; C:\QAFactory\forge-repo\docs\TESTING.md
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\agents\qa-case-designer.md (`## Techniques`, the bullet "Equivalence partitioning" at :50 only)
C:\QAFactory\forge-repo\ai-packages\qa-factory\agents\qa-case-critic.md (line 44, the parenthesis only)
C:\QAFactory\forge-repo\ai-packages\qa-factory\design\role-rules.json (one new row)
C:\QAFactory\forge-repo\ai-packages\qa-factory\references\role-load.json (key `ratchet_tokens.qa-case-designer` only)
C:\QAFactory\forge-repo\ai-packages\qa-factory\changelog.d\tq2-1-value-table-cases.md (new fragment, English)
non-goals: any script; any other line of either charter; any other key of role-load.json; the strategist and the code critic
(RC1-2); the automator charter (§C.3); moving the critic's fixed tokens to a process section (RC2-3, `roles-context/2`); `Archived`,
`merged_into`, deleting or emptying any case; `references/ahead-cards.json` (no code check is added, so no card line is owed, AR-10);
any new test file
handoff: builder report path given by the Lead's dispatch
edges: below (K1-E1..K1-E8)
DoD: `python -B C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\scenario_walk.py --witness-for C:\QAFactory\forge-repo\ai-packages\qa-factory\agents\qa-case-designer.md C:\QAFactory\forge-repo\ai-packages\qa-factory\agents\qa-case-critic.md C:\QAFactory\forge-repo\ai-packages\qa-factory\design\role-rules.json C:\QAFactory\forge-repo\ai-packages\qa-factory\references\role-load.json`, run BEFORE the first edit and AFTER the last, both outputs attached: every test green before is green after; a test red before (the cohort lists `test_role_load.py` in `keep_fail_at_entry`, test-layers.json:7101) is attached and keeps exactly the same failing checks; a new red is a defect. And `python -B C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\role_load.py --all --json` before the first edit and after the last, both attached: R1 raised to the after-measure within its bound, R2 and R3 equal to their old values, verdict `within` for `qa-case-designer` and `qa-case-critic`
siblings: RC1-2 (`onboarding-forge/1`, the same designer sentence; pointer §B); `qa-case-critic.md:41` (dimension 2 already judges this, the twin); `qa-automator.md:50` (the S5 twin, unchanged); RC2-3 (`roles-context/2`, same critic lines, X4)
designer: this file

**Expected text (direction chosen; the builder may shorten, never widen):**
- `qa-case-designer.md:50`. Replace the bullet
  `- **Equivalence partitioning.** One case or partition per class that should behave differently; never two cases for one class.`
  with
  `- **Equivalence partitioning.** One partition per class that behaves differently. Inputs with the same steps that differ only in value entered and expected are ONE case with a table of values, a partition per row: -1, 0, 1.5 and "abc" all turned into 1 are one case, not four (P16).`
  (No form detail such as `P-<name>` in this craft bullet: the partition's form is the contract's, artifact-contract.md:71-76; A10.)
- `qa-case-critic.md:44`. Replace `(the fixed marker the roll-call reads; it merges the CASES)` (59 B) with
  `(the roll-call's fixed marker; S5 merges tests, cases stay)` (59 B). Same byte length on purpose (R3).
- `role-rules.json`, one row beside `parametrised-inputs-no-repeat` (:26):
  `{"id": "designer-value-table-one-case", "rule": "Inputs that take the same steps and differ only in the value entered and expected are one case with a table of values, one partition per row.", "source": "TQ2-1; P16; owner 13.11.2026 (option c)", "carriers": [{"file": "agents/qa-case-designer.md", "anchor": "ONE case with a table"}]}`
  (anchor of 5 words, docs/TESTING.md:106 "2–6 words".)
- `role-load.json`: `ratchet_tokens.qa-case-designer` -> the after-measure (R1).
- Changelog fragment: "The S4 case designer now writes one case with a table of values where cases would differ only in the
  input and the expected value. A case critic's merge still changes no case: it travels to the S5 automator as a concern."

**Acceptance keys:** (1) the designer bullet holds `ONE case with a table of values` and `"abc"` and no Cyrillic character (FR-30;
`selftest.py --lang` at integration, not here); (2) `qa-case-critic.md` no longer holds `it merges the CASES` and holds
`S5 merges tests, cases stay`; (3) `test_role_rules.py` (printed by the witness for `role-rules.json`) green with the new row;
(4) role_load before/after attached: R1 = the after-measure, its delta ≤ 50 tokens; R2 = 12079 and R3 = 18296 after; a delta over the
bound, or R2/R3 moved -> stop and return a question, never a cut elsewhere.

**Edges, each with the invariant it protects:**

| # | Edge | Behaviour | Invariant |
|---|---|---|---|
| K1-E1 | Two PLAN ROWS whose cases would differ only in input | They stay two cases, one per plan row (`qa-case-designer.md:23`, registry row `designer-one-case-per-plan-row` :161); the case critic answers `merge`; the instruction rides to S5 (owner's word) | a case names exactly one plan row: no reader of `plan_row` changes (the owner's "no reader changes") |
| K1-E2 | A rework round, or the project's existing cases, already hold two near-duplicate cases | The rule applies to cases the designer writes NEW. An existing case is never deleted, emptied or archived to fold it; the designer names the pair in its digest, and the critic answers `merge` -> S5 | no case file disappears and no case changes state because of a merge (t-723 B-1, confirmed 13.11.2026) |
| K1-E3 | Rows of one table expect DIFFERENT values (0 -> refusal, 5 -> saved) | One case still, one partition per row with its own expected value. `qa-case-designer.md:57` (equivalence by consequence) still splits PARTITIONS, not cases | a partition holds only inputs with the same Then; a case may hold several partitions (no rule of the charter contradicts another) |
| K1-E4 | A row needs another precondition (a flag, an account) | The partition is gated by `preconditions[].partitions` (`artifact-contract.md:84-88`); the case stays one | a gated row is never silently run without its precondition |
| K1-E5 | A row of the table is expected red (a known bug) | Still a row; the automator makes it a parameter, never a consolidated body (`qa-automator.md:51`) | a red row never hides the others (P29) |
| K1-E6 | Steps differ (another screen, another account, another order) | Separate cases ("the same steps" is the rule's condition) | one red line always names the case and the row (P16) |
| K1-E7 | Manual case with a table | the agent walks each row. `references/manual-evidence.md` does not name partitions (Grep `(?i)partition` -> none; control: `(?i)evidence` on the same file counts 18), so K1 promises no per-row evidence form; the case critic judges whether a manual table is walkable | no evidence duty is claimed that no carrier states (§9 analog) |
| K1-E8 | The role_load measure moves more than the bound, or R2/R3 move | stop, report both measures, ask | a shrink-only row is never raised beyond its named need, and never "made room for" by a cut outside owns (AR-20) |

**Live proof (FR-33):** the live-runs row of §E.3 (same 12586 copy run as TQ1-27's row, `plans/piles/live-runs/batch-2-live-proofs.md:128`).

### K2 — the case critic's merge reaches the S5 plan, and every legacy window its own

given: this spec §0, §1, §C, §D.0, §D-K2; P\scripts\brief_pack.py (`_text_whole` :443-446, `_short` :1133, `HEAD_LINE_CHARS` :1952,
`_s5_kind` :1961-1976, `plan_dispatch_lines` :1993-2055, `plan_lines` :2076-2103, `build` :4173-4366 with the chain :4244-4256 and the
comment :4197); P\scripts\s5_plan.py (`remarks_of` :1077-1092, `_case_critic_files` :1095-1107, `_file_concerns` :1116-1143,
`case_concerns` :1146-1160, `_placement` :1180-1195, `window_slice` :1245-1313, `render_slice` :1316-1365, `grouping_hints`
:1405-1433, `plan_for_hints` :1436-1444, `hint_rows` :1447-1457, `print_hints` :1460-1465, `main` --check :1489-1504);
P\scripts\s5_precheck.py (`plan_result` :4280-4300); P\scripts\critic_rollcall.py (`PARAMETRISE_TOKEN` :57, `_read_round` :404-431,
`accepted_rounds` :434-442, `_carries` :914-919); P\scripts\controller.py (read only: `stage_scope` :4147, `_scope_windows`
:4424-4445, `split_windows` :446-449, `S5_PLAN_ROLES` :116); P\scripts\contract.py (read only: `case_ids` :4257-4270, `scope_keys`
:4273-4302, `case_config` :3302); P\references\code-review-rubric.md:12-28; P\references\role-load.json; P\references\inject-map.json:68-76;
P\design\role-rules.json; P\scripts\tests\test_brief_pack_s5_plan.py (whole; K7 :549-601, k8 :517-534, ceiling :539-546);
P\scripts\tests\test_s5_plan_grouping.py (whole; `fixture_story` :51-); P\scripts\tests\test-layers.json (keep rows :345, :4820;
cohort :7094-7105); P\design\factory-rules.md (whole); C:\QAFactory\forge-repo\plans\builder-rules.md; C:\QAFactory\forge-repo\docs\TESTING.md
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\brief_pack.py (functions: `plan_dispatch_lines`; new `case_concern_lines`; `build`: one `elif` appended to the s5_kind chain after :4256 and the comment at :4197)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\s5_plan.py (functions: `_file_concerns`, `case_concerns`; new `concern_report`; new `placed_remarks`, `window_slice` (calls it); new `concerns_for_scope`; new `remark_lines`, `render_slice` (calls it); new `merge_hints`, new `merge_hint_rows`; `main` (the --check branch only); the module docstring's function list :20-30)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\s5_precheck.py (function: `plan_result` only)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\critic_rollcall.py (functions: new `parametrise_group`; `_carries` (calls it))
C:\QAFactory\forge-repo\ai-packages\qa-factory\references\code-review-rubric.md (section «On the plan»: one new bullet after the first)
C:\QAFactory\forge-repo\ai-packages\qa-factory\references\role-load.json (keys `process_ratchet_tokens.qa-code-critic` and, only if over, `ratchet_tokens.qa-code-critic`)
C:\QAFactory\forge-repo\ai-packages\qa-factory\design\role-rules.json (one new row)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_brief_pack_s5_plan.py (one new parameterised function, table rows B1-B8; the constant `S5_PLAN_BRIEF_BYTES_MAX` with its named raise; the docstring line :14)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_s5_plan_grouping.py (one new parameterised table, rows G1-G9)
C:\QAFactory\forge-repo\ai-packages\qa-factory\changelog.d\tq2-1-merge-reaches-s5-plan.md (new fragment, English)
non-goals: any change to how a merge is answered at S4 (`merge_candidate_errors` and its helpers); any new refusal, finding, exit
code, `ok` or verdict from code (advice only); `controller.s5_windows_for`, `split_windows`, `pack_windows` and every window cut
(F7); `hint_rows` and `grouping_hints` (unchanged: the K6 rows of test_s5_plan_grouping.py :218-260 pin them); the planned window's
`plan_remarks`/C12 machinery and C12 on legacy windows (F7); `handoffs/*.yaml`; the automator and case critic charters;
`critic_rollcall` functions owned by N5 (`parse_rollcall`, `parse_merge_candidates`, `_read_rounds`, `_has_note_column`,
`_level_errors`); `gate_brief.py` (reads `case_concerns`, whose output is unchanged); `test_brief_pack.py` and `ROLE_BRIEF_BYTES_MAX`
(R7); any key of role-load.json other than the two named; quarantined tests (`test_carried_concerns.py` test-layers.json:7372,
`test_case_merges.py` :7453): never edited, never cited as the witness; any new test file
handoff: builder report path given by the Lead's dispatch
edges: below (K2-E1..K2-E16)
DoD: `python -B C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\scenario_walk.py --witness-for C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\brief_pack.py C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\s5_plan.py C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\s5_precheck.py C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\critic_rollcall.py C:\QAFactory\forge-repo\ai-packages\qa-factory\references\code-review-rubric.md C:\QAFactory\forge-repo\ai-packages\qa-factory\references\role-load.json C:\QAFactory\forge-repo\ai-packages\qa-factory\design\role-rules.json`, run BEFORE the first edit and AFTER the last, both outputs attached. `test_brief_pack_s5_plan.py` is in the cohort's `keep_fail_at_entry` (test-layers.json:7097) but was GREEN at 5cc4f88 (critic's run: `213/213 ok`, exit 0): after the change it must be green in every check; any other test green before is green after; a test red before is attached and keeps exactly the same failing checks; a new red is a defect. And `python -B C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\role_load.py --all --json` before and after, both attached, R5/R6 set as §D.0 says; the `RATCHET S5_PLAN_BRIEF_BYTES_MAX` line before and after, R4 set as §D.0 says. Test lines in the diff ≤ product code and text lines (docs/TESTING.md:115), or one report line naming why
siblings: `s5_plan.grouping_hints` / `hint_rows` (the advice family: same row shape, same printer, unchanged); `critic_rollcall._carries` (the one token reader, now through `parametrise_group`); `brief_pack.plan_lines` / `_delta_tail` (planned window road, unchanged); `gate_brief.py:2226-2234` (gate A reads the same `case_concerns`, unchanged); `brief_pack.py:4197` comment and `test_brief_pack_s5_plan.py:14` docstring (become false with item 5: owned, rewritten); RC1-2 (code-critic text, X5)
designer: this file

**Expected behaviour per function:**
1. `critic_rollcall.parametrise_group(note, cfg) -> list[str]`: the case ids after the FIRST `PARAMETRISE_TOKEN` in `note`.
   Whitespace collapsed (`" ".join(str(note or "").split())`), case-insensitive `re.search` of the escaped token, ids from
   `C.case_ids(rest, cfg=cfg)` in order, duplicates dropped. `[]` when the token is absent or `note` is None. No `raise`.
   `_carries(note, partners, cfg)` becomes `bool(partners) and set(partners) <= set(parametrise_group(note, cfg))`; with non-empty
   partners this equals today's behaviour (the token must be present for the group to be non-empty), and `_merge_concern_errors` never
   calls it with empty partners (:933-935).
2. `s5_plan.concern_report(task_root, state) -> dict` `{"concerns": list, "rounds": int, "silent": [str]}`: `concerns` exactly as
   `case_concerns` returns today; `rounds` = the number of accepted S4 case-critic rounds (`sum(len(r) for r in _case_critic_files(state).values())`);
   `silent` = the story-relative paths of findings files that WERE read and whose every accepted round listed no case (every
   `accepted_rounds(...)[i]["listed"]` empty: the receipt measured other bytes, no roll-call, or an exception — `_read_round`'s
   `silent()` outcomes). `_file_concerns` returns `(remarks, silent: bool)` for this; its unreadable-file branch returns
   `([global remark], False)` (that file already has a remark). `case_concerns(task_root, state)` = `concern_report(...)["concerns"]`:
   its output is unchanged, so `remarks_of`, `window_slice` and gate A are unchanged. No `raise` statement added.
3. `s5_plan.placed_remarks(remarks, window_of, tests, reach) -> list`: the loop of `window_slice` :1296-1300 moved out unchanged —
   for each remark, `places, how = _placement(remark, window_of, tests)`; kept with `placement=how` when `how != "window"` or
   `places & reach`. `window_slice` calls it with `remarks_of(task_root, state)`, `window_of`, `_rows(plan, "tests")`, `reach`.
4. `s5_plan.concerns_for_scope(task_root, state, concerns, scope) -> (list, why)`: the concerns of ONE legacy window by the same rule.
   `stage = CT.Controller(task_root).stage_scope("S5", state)`; not `derived` -> `([dict(c, placement="unplaced") for c in concerns],
   "<the reason>")`. Else `mine = {str(k) for k in scope}`, `window_of = {str(k): (1 if str(k) in mine else 0) for k in stage["scope"]}`
   plus `{k: 1 for k in mine}`; return `(placed_remarks(concerns, window_of, [], {1}), "")`. Any exception -> all concerns with
   `placement="unplaced"` and `why = f"{type(exc).__name__}: {_show(exc, 100)}"`. Never raises (no `raise` statement).
5. `s5_plan.remark_lines(remarks) -> list[str]`: the lines `render_slice` prints under `## Remarks (plan review and case critic)`
   (:1359-1364), moved out unchanged, including `"no remarks for this window"` when empty. `render_slice` calls it.
6. `s5_plan.merge_hints(plan, concerns, cfg=None) -> list` of rows `{case, message, fix, tag}`; `[]` for a plan that is not a dict;
   a malformed concern or test row is skipped; no `raise`. Definitions:
   - plan keys `P` = the text `case` of each `plan["cases"]` row; a key MATCHES an id `x` when `key == x` or
     `x in C.case_ids(key, cfg=cfg)` (so the area key `speakers/TC-009` matches the roll-call's bare `TC-009`, contract.py:4279; A3).
   - per concern with a text `problem`: `G = critic_rollcall.parametrise_group(problem, cfg)`; skip when `len(G) < 2`.
     `G'` = plan keys matching an id of G (plan order, no repeat). `H` = keys of `G'` that some `tests[]` row lists in its `cases`.
   - `len(H) < 2` -> no row (nothing is automated twice: both left as remainders, one automated, or ids outside the plan; A7).
   - **followed**: one test row's `cases` holds every key of H -> no row (any shape: new, parameterize, extend, reuse).
   - **answered**: every test row whose `cases` meet H has a non-blank text `apart_reason` -> no row (presence only; whether the
     reason is real is the plan critic's, F8).
   - otherwise one row: `case` = H[0]; `tag` = `"merge-" + sha1("\n".join(sorted(H)))[:8]`; `message` = `"the case critic asked to
     parametrise <H, comma-joined> into one test (<concern id>); the plan puts them in <ids of the tests meeting H> and not every one
     of those tests says why in apart_reason"`; `fix` = `"write one parameterized test over <H> (each parameter id naming its case),
     or give each test that holds them an apart_reason naming another setup, surface or fixture"`.
7. `s5_plan.merge_hint_rows(task_root) -> (rows, why)`, beside `hint_rows`, the same contract: `plan, why = plan_for_hints(task_root)`;
   no plan -> `([], "" if why == NO_PLAN or why.startswith(PlanUnreadable.__name__ + ":") else why)`; else, in one `try`:
   `state = CT.Controller(task_root).state()`, `merge_hints(plan, case_concerns(task_root, state), cfg=C.case_config(task_root))`,
   `why = ""`; an exception -> `([], f"{type(exc).__name__}: {_show(exc, 100)}")` (the sibling form of `hint_rows` :1457). `hint_rows`
   is NOT changed (B1).
8. `s5_plan.main --check`: after `hints, why = hint_rows(...)`, `merges, merge_why = merge_hint_rows(task_root)`; `merge_why` -> one
   more note `not checked: the case-critic merge hints of the plan (<merge_why>)`; `print_hints(hints + merges)`; the OK line's
   advice sentence when `hints or merges`. Findings, the verdict line and the exit code are computed exactly as now.
9. `s5_precheck.plan_result`: the same two values; `notes` gains `not checked: the case-critic merge hints of the plan (<why>)` when
   `why`; `hints` gains `_hint("plan", row["case"], row["message"], row["fix"], row["tag"])` per merge row. `ok` stays
   `not findings`. One printer, both paths (AR-18).
10. `brief_pack.case_concern_lines(task_root, dispatch_id, state, role, write, scope=None) -> dict` `{head, files, sides}` (no `raise`;
    every exception text through `_text_whole`, FV1-4 N2, A2):
    - `report = _sp().concern_report(task_root, state)`; `scope is None` (the plan dispatch) -> `shown = [dict(c, placement="plan")
      for c in report["concerns"]]`; else (a legacy window) `shown, why = _sp().concerns_for_scope(task_root, state,
      report["concerns"], scope)`. `cfg = C.case_config(task_root)`; `k` = the shown concerns whose `parametrise_group` holds ≥ 2 ids;
      legacy only: `s` = those of them naming an id that matches none of the window's scope keys (match rule of item 6).
    - `len(shown) ≥ 1`: side `"<dispatch_id>-case-concerns.md"` = `"# The case critic's concerns carried to automation\n\n" +
      "\n".join(remark_lines(shown)) + "\n"`; files line `"- <rel> - the case critic's concerns (CC-n)" + (" (not written in this
      run)" if not write) + ("; the windows get the same lines" if plan else " for the cases of this window")`. Head line through
      `_short(..., HEAD_LINE_CHARS)`:
      - plan author: `"The case critic carried <n> concern(s) to automation (<k> ask to parametrise cases into one test): <rel>.
        Answer each in the plan: a `parametrise into one test:` concern is one parameterized test over its cases, or each test that
        holds them says why in `apart_reason`"`;
      - plan critic: `"The case critic carried <n> concern(s) to automation (<k> ask to parametrise cases into one test): <rel>.
        Judge whether the plan answers each (rubric «On the plan»)"`;
      - legacy automator: `"The case critic carried <n> concern(s) for the cases of this window (<k> ask to parametrise cases into one
        test): <rel>. Answer each in `plan_remarks` (applied / not_applicable with why); a `parametrise into one test:` concern is one
        parameterized test over its cases"` + (`"; <s> name a case of another window: they cannot be merged here, say so in the
        row"` when s ≥ 1) + (`"; not filtered to this window (<why>)"` when `why`);
      - legacy code critic: `"The case critic carried <n> concern(s) for the cases of this window: <rel>. The automator answers each in
        `plan_remarks`; judge each answer (C12)"`.
    - `len(shown) == 0`: no side file; one files line: `rounds == 0` -> `"- case critic's concerns: none carried"`; legacy and the story
      has concerns for other windows -> `"- case critic's concerns: none for the cases of this window (<N> for other windows)"`;
      otherwise -> `"- case critic's concerns: none raised in <rounds> accepted round(s)"`.
    - `report["silent"]` non-empty (with any n): one head line `"Case critic's concerns: <m> findings file(s) gave none because a round
      could not be read against the critic's receipt (the file changed after it, or its roll-call is broken); read the rows marked
      `approve_with_concerns` there before you <group the tests | automate | judge>"` and one files line per path
      `"- <path> - case critic's findings that gave no concern (receipt): read it"` (A4, FR-41).
    - any exception: head line `"Case critic's concerns: could not be read (<_text_whole(exc)>); read the rows marked
      `approve_with_concerns` in work/test-cases/**/critic-findings.md before you <group the tests | automate | judge>"`; no side
      file; the brief is still built.
11. `plan_dispatch_lines`: for BOTH roles, BEFORE the cap branch (so under the cap, over the cap, and when slices cannot be cut),
    merges `case_concern_lines(task_root, dispatch_id, state, role, write)` into `head` (after the role's first line and, for the
    critic, after the grouping line), `files` (after the plan's lines) and `sides`. Critic branch only, right after the grouping
    line (:2011-2017, unchanged): `merges, merge_why = _sp().merge_hint_rows(task_root)`; `merge_why` -> `"merge hints not computed
    (<_text_whole(merge_why)>); compare the case-concerns file with the plan's tests yourself"`; `merges` -> `"`s5_plan.py --check`
    prints <m> merge hint(s): cases the case critic asked to parametrise into one test sit in separate tests with no `apart_reason`.
    Each unanswered one is a blocker (rubric «On the plan»), even where a grouping hint names the same tests"`; none -> no line.
    The over-cap slices keep their own remark section (same printer).
12. `build`: append to the chain after the `unknown` branch (:4254-4256) `elif s5_kind == "legacy" and dispatch:` (both roles of
    `S5_PLAN_ROLES`, :116) merging `case_concern_lines(task_root, dispatch_id, s5_state, role, write and output is None, scope)` into
    `head`, `plan_files` and `side_files` the same way. A `window` or `plan` brief is not changed by this branch. The comment at :4197
    reads: `SC1-14 C2 / TQ2-1 K2: which S5 dispatch this is. `legacy` is the brief as it was plus the case critic's concerns for its
    window; every other stage or role is the brief as it was, byte for byte.`
13. `code-review-rubric.md` «On the plan», a NEW bullet after the first (A6; the first bullet, with its "A `remark`, never a `blocker`
    on its own", is not edited):
    `- **An unanswered case-critic merge.** A `parametrise into one test:` concern (the case-concerns file, `--check` merge hints) that the plan neither follows with one test nor answers by an `apart_reason` naming another setup, surface or fixture: a `blocker`, even where a grouping hint names the same tests. Only the plan makes them one test for certain.`
    (wrapped like its neighbours; per F8 = a, a nominal reason answers nothing).
14. `role-rules.json` row: `{"id": "plan-answers-case-merge", "rule": "A case-critic parametrise concern the S5 plan neither follows nor answers with a real apart_reason is a blocker of the plan review.", "source": "TQ2-1 K2; owner 13.11.2026 (option c)", "carriers": [{"file": "references/code-review-rubric.md", "anchor": "An unanswered case-critic merge"}]}`.
15. `role-load.json`: R5, R6 of §D.0. `test_brief_pack_s5_plan.py:541`: R4 of §D.0. Docstring :14 reads: `* the earlier form
    (`legacy`) is the brief as it was plus the case critic's concerns for its window: no plan path, no slice.`
16. Changelog: "The S5 plan now receives the case critic's concerns, including every request to parametrise cases into one test,
    whether the plan is small or large; on the driver process each S5 window receives the concerns of its own cases. `s5_plan.py
    --check` adds a hint when the plan leaves such cases in separate tests without an `apart_reason`, and the plan critic treats an
    unanswered one as a blocker. Cases the driver's cut puts in two windows still cannot be merged by either window."

**Acceptance keys (table rows, ids naming the input; P16, docs/TESTING.md: rows that fail before the change):**
`test_brief_pack_s5_plan.py`, ONE new parameterised function over a temp story with an accepted S4 case-critic dispatch whose
round has `TC-1`, `TC-2` `approve_with_concerns` with note `parametrise into one test: TC-1, TC-2` (and, where named, `TC-3` with
another concern):
- B1. `author-under-cap` -> files name `<id>-case-concerns.md`; side text holds `CC-1`, `CC-2`, the token; head holds `2 concern(s)`,
  `1 ask to parametrise` and `apart_reason`.
- B2. `critic-under-cap, plan splits TC-1/TC-2 in two tests of one file and level` -> the same side file; head holds the grouping line
  (K7 text, its count NOT including the merge row) AND the line `prints 1 merge hint(s)` with `blocker` (B1 of the verdict: both
  lines, one truth).
- B3. `author-over-cap`, B4. `critic-over-cap` (cap monkeypatched small) -> the side file present AND each slice still prints the
  remarks.
- B5. `no accepted case-critic dispatch` -> files line `case critic's concerns: none carried`; no side file.
- B6. `accepted round, findings edited after its receipt` -> head names the file and `could not be read against the critic's
  receipt`; no `none carried` (A4).
- B7. `legacy author window scope [TC-1]` (driver run mode, TC-2 and TC-3 in other windows) -> side file holds the CC of TC-1 only;
  head holds `1 name a case of another window`; `legacy author window scope [TC-1, TC-2]` -> both CCs, no "another window" clause.
- B8. `legacy code-critic window` -> the same side file and the C12 head line.

`test_s5_plan_grouping.py`, ONE new parameterised table through `merge_hints` (rows G1-G8) plus one consumer row (G9):
- G1. one test `cases: [TC-1, TC-2]` -> none. G2. TC-1 in T-1, TC-2 in T-2, no `apart_reason` -> one hint naming CC-1, TC-1, TC-2,
  T-1, T-2; `tag` equal across two calls. G3. as G2 with `apart_reason` on both -> none; on one only -> the hint.
  G4. group TC-1, TC-2, TC-3; one test holds TC-1, TC-2; TC-3 in T-3 -> hint naming TC-3. G5. group TC-1, TC-9, TC-9 no plan case ->
  none. G6. TC-2 a plan case with no test (remainder) -> none (vacuous, A7). G7. area keys `speakers/TC-1`, `speakers/TC-2` in two
  tests, concern ids bare -> hint (A3). G8. concern without the token, and a global concern (`case` None) -> none.
- G9. `s5_plan.py --check` and `s5_precheck.plan_result` on the producer's real plan (`fixture_story`) with a concern splitting two
  of its cases -> the same `hint:` line on both paths; exit code, findings and `ok` identical to the same plan without the concern.

**Edges, each with the invariant it protects:**

| # | Edge | Behaviour | Invariant |
|---|---|---|---|
| K2-E1 | No case critic round accepted (S4 skipped, a story before TQ1-27) | "none carried"; no hint | an empty measurement is a stated outcome (AR-23), never a refusal |
| K2-E2 | Concerns unreadable (state or file raising) | a head line says so and names where to read; `merge_hint_rows` gives `why` and `--check`/`plan_result` say "not checked"; the critic's brief says "merge hints not computed" | an unknown is said, never a silent pass (AR-28, FR-41) |
| K2-E3 | The findings file was edited after the critic's receipt | the round carries nothing (existing, I3); the brief names the file as "could not be read against the critic's receipt" and never says "none carried" (A4) | a concern is never taken from bytes the receipt did not measure (I3, FR-59), AND a dropped round is never reported as an empty fact (FR-41) |
| K2-E4 | The token note names a case outside S5 scope, of another story, or an id in a later sentence | ids matching no plan key are dropped (G'); a colliding bare id (two areas with `TC-009`) adds keys and gives an extra hint at worst | error direction is OVER-report (a hint the plan critic dismisses), never under-report |
| K2-E5 | Area-keyed plan cases (`speakers/TC-009`) and bare roll-call ids | matched by `case_ids(key)` (item 6) | the area story is not silently skipped (the first draft's G ∩ P = ∅ under-report, A3) |
| K2-E6 | The plan groups the pair in an `extend` or `reuse` test | followed (one test row holds both, any shape) | the automator chooses the shape (P17); code checks only that one test holds the cases |
| K2-E7 | The plan keeps them apart with an `apart_reason` | no hint; the plan critic judges the reason (rubric bullet; F8) | whether the reason holds is judgment (AR-29); code reads presence only, like `grouping_hints` |
| K2-E8 | No test holds two of the group's cases (remainders, or one automated) | no hint (A7) | nothing is automated twice, so the owner's point 4 is not at stake; the remainder is the plan check's and C12's business |
| K2-E9 | The planned window still receives the CC-n after the plan followed it | it answers `applied` in `plan_remarks` (C12, unchanged) | the window road is not changed; one instruction, answered once per window |
| K2-E10 | POSITIONAL: the case-concern lines go before the cap branch of `plan_dispatch_lines`; the merge line right after the grouping line | both cap roads and the "slices cannot be cut" road carry the side file; the role's first head line stays first and the K7 grouping line is byte-unchanged | one road for every plan size (P31); the grouping line never counts merge rows (B1) |
| K2-E11 | POSITIONAL: the legacy `elif` is appended to the chain after `unknown` (:4256), never inside `plan`/`window`, and only for a dispatch the controller holds | a `plan` brief gets the CC-n in its side file, and over the cap ALSO in each slice (same lines, one printer); a `window` brief gets them once, in its slice; a legacy brief once, in its side file; a brief with no dispatch record (`_s5_kind` "no record of this dispatch", :1967-1968) is unchanged | no S5 automator or code-critic brief of a real dispatch carries none; no brief carries them from two different printers (A11); R7 untouched |
| K2-E12 | Legacy partners split by the cut-by-cases | each window gets its own case's CC, the head says "<s> name a case of another window: they cannot be merged here"; the answer is a `plan_remarks` row the code critic judges | the residual is said in the brief, never hidden; closing it is F7, not this node |
| K2-E13 | Legacy window: the stage scope cannot be derived | the whole list is handed with `placement: unplaced` and the head says "not filtered to this window (<why>)" | error direction is over-carry, said aloud (AR-28) |
| K2-E14 | Many concerns (a 40-case story) | the side file lists all of them, no cut; the head holds counts only | a concern is never dropped for size (side files are not counted in the brief ratchet or the role load, role-load.json:2 "side files ... are not counted without a story") |
| K2-E15 | TEMPORAL: a story whose plan was written or reviewed before K2; an S4 rework after the plan review adds new CC-n | `--check` prints merge hints on re-run; a reviewed plan is not re-reviewed by this change; new CC-n reach the planned windows through C12 and the next plan dispatch, the accepted plan is not refreshed | advice never invalidates an accepted review or its receipt (`plan_sha256`, s5_plan.py:412-416) |
| K2-E16 | TEMPORAL: the ratchet constants and rows before and after K2 | before: R4 9520, R5 17596, R6 19420; after: the measured values, raised in the same diff with the reason; a measured delta over the bound -> stop | a shrink-only ratchet is raised only by name, by its measured need (AR-20, axis 18) |

**Reused function in a more consequential role (designer rule 1).** `s5_plan.case_concerns` was advice to the windows (C12 asks one
row each). It now also feeds the plan author's work, every legacy window, and a hint that the plan critic turns into a blocker
(F5 = a). It may err only toward OVER-carrying: an extra or stale concern costs one `apart_reason` line, one `not_applicable` row or
one dismissed hint. It must never UNDER-carry silently. Adversarial inputs that must stay on the safe side, each with its row or its
existing seam: an unreadable findings file (a global remark, `s5_plan.py:1128-1132`: counted in the side file, no hint: G8); a receipt
mismatch (K2-E3, row B6); two accepted rounds where the later one drops the concern on a case (`_file_concerns` latest-listing rule,
unchanged seam); area-keyed scope keys (K2-E5, row G7; on the legacy filter an area key makes the concern "unplaced" and so carried
to every window, K2-E13's direction); a token in another case or spacing (`_carries`'s existing parse, now `parametrise_group`).
`_placement` (s5_plan.py:1180-1195), reused for legacy windows: its error direction is already "a remark is never lost for want of a
place" (unplaced -> every window); window number 0 for "another window" is a known case and excludes, never loses.

**Live proof (FR-33):** the live-runs row of §E.3.

### N5 — one column helper (kept per F2; the old draft §6 N5, restated inline)

Line references re-checked on 5cc4f88 (critic_rollcall.py unchanged be2c988..5cc4f88, per the critic's diff --stat): `parse_rollcall`
:89-140 (columns at :113-118; `note` "" when absent, :136), `parse_merge_candidates` :793-816 (`header.index` :808), `_read_rounds`
:819-833 (`note_col` :832), `_has_note_column` :836-839 (only caller `_read_rounds` :832), `_level_errors` :972 (reads `note_col` at
:990); `contract.md_table` :2845. Readers of `row["note"]` that tolerate None already: `critic_rollcall.py:426` (`or NO_NOTE`), `:917`
(`str(note or "")`), `:996` (`or ""`).

given: this spec §D-N5; the old draft `docs/tasks/specs/20261113-tq2-1-case-merge-spec.md` §1.1 rows 4a-4b, §8 C5, §6 N5 (:290-302);
P\scripts\critic_rollcall.py (:85-140, :790-840, :970-1000); P\scripts\contract.py (:2845-2866); P\scripts\tests\test_critic_rollcall_apply_fixes.py;
P\scripts\tests\test-layers.json (keep :1199); P\design\factory-rules.md (whole); C:\QAFactory\forge-repo\plans\builder-rules.md;
C:\QAFactory\forge-repo\docs\TESTING.md
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\contract.py (new function `md_column` only, beside `md_table` :2845)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\critic_rollcall.py (functions: `parse_rollcall`, `parse_merge_candidates`, `_read_rounds`, `_level_errors`; delete `_has_note_column`)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_critic_rollcall_apply_fixes.py (one table row: a roll-call with no `note` column)
non-goals: `parametrise_group` and `_carries` (K2's); `branch_accounting._table_rows` (old §8 C5); the siblings
`planning_contract.py:1341, 1345, 2488-2489` and `audit_factory.py:748` (queued, old draft §9); any new test file
handoff: builder report path given by the Lead's dispatch
edges: a header cell with backticks or spaces (`  ` `note` `  `) -> found; two columns of the same name -> the first; a name that is a
prefix of another (`case` vs `cases`) -> `md_column` matches EXACTLY; `parse_rollcall`'s `case` column keeps its `startswith("case")`
rule and `reviewed` its `"reviewed" in name` rule (caller-side choices kept as they are); a roll-call with no `note` column -> row
`note` is `None` and every reader that did `or ""` / `or NO_NOTE` keeps working (invariant: an absent column is never read as an empty
note that `_level_errors` would then judge, nor as a crash); a table with no rows -> `note_col` from `md_column` on the header
DoD: `python -B C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\scenario_walk.py --witness-for C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\critic_rollcall.py C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\contract.py`, run before the first edit and after the last, both attached: green before -> green after; red before -> the same failing checks; keys: `md_column(header, name) -> int | None` (cells stripped, backticks off, lower case, exact); `parse_rollcall` row `note` is `None` when the column is absent, the cell text otherwise; `_read_rounds` sets `note_col` from `parse_rollcall` rows (`any(row["note"] is not None ...)`) or, for a table with no rows, from `md_column`; `_level_errors` unchanged in behaviour; `parse_merge_candidates` finds columns by `md_column` with its `bad_header` sentence unchanged; `_has_note_column` gone (Grep `_has_note_column\(` finds no caller; positive control: the same Grep before the edit finds :832); the builder greps every `["note"]` / `.get("note")` reader of `parse_rollcall` rows (gate_brief, s5_plan included) and lists them in the report
siblings: `planning_contract.py:1341, 1345, 2488`, `audit_factory.py:748` — queued, not widened
designer: this file

Its worth without the fold: unchanged. N5 never touched the fold. It removes a second reader of "does the roll-call have a `note`
column" (AR-13) and the ""/None ambiguity that `_level_errors` depends on.

---

## E. What the batch file should now say (text for the Lead to paste)

### E.1 «Ход» line of `plans/piles/test-code-quality/batch-2-sliyanie-kejsov-i-chitateli.md` (append at the end of «Ход»)

`- 13.11 — слово владельца по развилке F1 спеки TQ2-1 (сессия с владельцем, 13.11.2026): «давай такой вариант. Если критик найдёт что сливать, то это будет инструкция для автоматизатора, как и сейчас. Количество ручных текстовых кейсов не критично, а вот автоматизация с одинаковыми шагами удлиняет время прогона». Выбран вариант (c): статуса `Archived` от фабрики нет, `merged_into` нет, читатели доставки не меняются; решение t-723 B-1 «merge не меняет кейс» подтверждено владельцем. Узлы N1–N4 черновика `docs/tasks/specs/20261113-tq2-1-case-merge-spec.md` сняты. Остаются: K1 (правило дизайнера «один кейс с таблицей значений» + правка формулировки критика :44 той же длины), K2 (concern критика кейсов доходит до плана S5 при любом размере плана и до каждого окна процесса драйвера — concern-ы его кейсов; подсказка `merge` в `--check` и `s5_precheck`; пункт рубрики плана), N5 (помощник колонки). Спека: `docs/tasks/specs/20261113-tq2-1-revision-option-c-spec.md` (фикс-раунд по критику на план 13.11). `Archived` в `validate_artifacts.py:76`, `critic_rollcall.py:1037`, `case_stamp.py:535` оставлен с причиной: законное значение ручной правки, оба читателя ошибаются в безопасную сторону, доставка говорит `no`, не `yes`.`

### E.2 The node row (the batch is not taken, so the row may be rewritten; replace the TQ2-1 row and the title/brief words that name `Archived`)

Title (line 1): `# Качество тестов — пачка 2: дизайнер пишет кейс с таблицей значений, слияние критика доходит до плана S5`

Brief (line 16): `Что сделать: правило дизайнера «один кейс с таблицей значений» (P16); concern критика кейсов «parametrise into one test:» доходит до плана S5 при любом размере плана и до окон процесса драйвера; один помощник колонки. НЕ делать: правки узлов `release-next/1`; `Archived`, `merged_into`, удаление или архив кейса (слово владельца 13.11.2026); новые правила критика кейсов (правка формулировки :44 — не правило); нарезку окон (F7).`

Line 9: `Решения владельца: вариант (c) по F1, владелец, 13.11.2026 (слова — «Ход»).`

Row:
`| TQ2-1 | П2 | Вариант (c), слово владельца 13.11.2026: K1 — устав дизайнера: «один кейс с таблицей значений» вместо кейсов, отличающихся только вводом (P16), формулировка критика кейсов :44 «it merges the CASES» исправлена той же длины, строка реестра `role-rules.json`, названный подъём храповика дизайнера; K2 — concern критика кейсов (CC-n) доходит до диспатча плана S5 (автор и критик плана) при плане меньше и больше капа и до каждого окна процесса драйвера (concern-ы его кейсов, одно правило размещения), подсказка `merge` в `s5_plan.py --check` и `s5_precheck`, отдельной строкой у критика плана, пункт рубрики «On the plan», названные подъёмы храповиков; N5 — один помощник «колонка по имени» для читателей ростера и таблицы слияний. Близнец: RC1-2 (`onboarding-forge/1`) — стратег и критик кода, строку дизайнера пишет K1. Спека `docs/tasks/specs/20261113-tq2-1-revision-option-c-spec.md`; P16, P17, P29, P31; FR-4, FR-10, FR-17, FR-33, FR-49; AR-13, AR-15, AR-18, AR-20, AR-21, AR-29 | designer → critic на план → builder → critic | `agents/qa-case-designer.md`, `agents/qa-case-critic.md` (:44), `design/role-rules.json`, `references/role-load.json`, `scripts/brief_pack.py` (`plan_dispatch_lines`, `case_concern_lines`, `build`), `scripts/s5_plan.py` (`_file_concerns`, `case_concerns`, `concern_report`, `placed_remarks`, `window_slice`, `concerns_for_scope`, `remark_lines`, `render_slice`, `merge_hints`, `merge_hint_rows`, `main`), `scripts/s5_precheck.py` (`plan_result`), `scripts/critic_rollcall.py` (`parametrise_group`, `_carries`; N5: `parse_rollcall`, `parse_merge_candidates`, `_read_rounds`, `_level_errors`, `_has_note_column`), `scripts/contract.py` (`md_column`), `references/code-review-rubric.md`, их тесты, `changelog.d/` | TQ1-27 (влит) | ожидает |`

### E.3 Live proof (PROJECT.md «Командная работа» item 9: the row goes to the untaken `live-runs` batch, `plans/piles/live-runs/batch-2-live-proofs.md`, status «ожидает», `:3`)

Row for «Живые доказательства» of `live-runs/2`. It is planned into the same run as the TQ1-27 row `:128`:
`| TQ2-1: на копии 12586 (тот же прогон, что строка TQ1-27): дизайнер S4 пишет один кейс с таблицей значений там, где кейсы отличаются только вводом; план S5 получает concern-ы критика кейсов и сводит каждую пару «parametrise into one test:» в один параметризованный тест или пишет `apart_reason`; ни одна такая пара не уходит в два теста без причины; прогон процессом driver несёт каждому окну S5 concern-ы его кейсов (K2, F3) | копия `testproject1-dev-010`, TP1-12586 | live-runs | ожидает прогона |`

In TQ2-1's own batch, «Живые доказательства» gets a pointer row once the nodes are accepted: `| TQ2-1 K1+K2 | — | live-runs | перенос: live-runs/2 | обоснование: живые прогоны не держат пачку | подтвердил: владелец, 11.11.2026 (класс) |`.

---

## 6. Edges common to the whole node (the pairs of this spec's own requirements that can conflict)

| # | Conflict | Resolution | Invariant |
|---|---|---|---|
| X1 | "no reader changes" (owner) vs K2 changing `brief_pack`, `s5_plan`, `s5_precheck`, `critic_rollcall` | K2 changes no reader of case STATUS or of the case index. It changes who receives an existing remark list | the owner's "no reader changes" was about `Archived` readers; no delivery verdict changes from TQ2-1 |
| X2 | batch brief "НЕ делать: новые правила критика кейсов" vs K1's edit of `qa-case-critic.md:44` | a correction of a false parenthesis, not a rule (F6 = a) | the critic's text never contradicts the confirmed rule "a merge changes no case" |
| X3 | "a merge is advice to S5, never a delivery gate" (t-723 E21) vs F5's plan-review blocker | the blocker is the plan critic's (a role), answered by an `apart_reason` line; nothing reaches delivery | P17 (the automator decides) and FR-4 (silence is stopped, an informed answer passes) both hold |
| X4 | K1 (charter, `agents/qa-case-critic.md:44`) vs RC2-3 (`roles-context/2`, moves the critic's fixed tokens into a process section, same lines 42-46) | if both are in work at once: `очередь:` line, the later merges `main` and keeps K1's wording (D-0048); a move into `process` meets `process_ratchet_tokens["qa-case-critic"]` (exact, slack 0): the mover re-sets that row (A10) | one sentence, one writer per moment |
| X5 | K2's rubric bullet (code-critic process load, R5) vs RC1-2's code-critic P16 text | both re-set `process_ratchet_tokens["qa-code-critic"]` to their after-measure; the later side re-measures after merging `main` | the process row always equals the measured process load (role_load.py:280-287) |
| X6 | "rubric first bullet: a test left unmerged is a remark, never a blocker on its own" vs the new bullet "an unanswered case-critic merge is a blocker" | two triggers: grouping alone -> remark; a case-critic merge -> blocker, "even where a grouping hint names the same tests" (in the rubric bullet and the critic's merge line) | one packet, one truth for the plan critic (FR-10, AR-10; B1) |

## 7. Forks (the Lead decides, the owner where marked)

| # | Fork | Options | Recommendation and cost |
|---|---|---|---|
| F1 | Home of the designer's P16 line (§B) | (a) K1; (b) RC1-2; (c) both | **decided (a)**, Lead |
| F2 | N5 without the fold | (a) keep; (b) narrow; (c) queue | **decided (a)**, Lead |
| F3 | The driver process (legacy S5) gets no CC-n (G2) | (a) one road inside K2; (b) later node; (c) desktop only | **decided (a)**, Lead; written as K2 item 12 with the window filter (B4) |
| F4 | `Archived` with no factory producer (§A.3) | (a) leave, record reason; (b) remove | **decided (a)**, Lead |
| F5 | A case-critic merge the plan neither follows nor answers | (a) plan critic's `blocker`; (b) `remark` | **decided (a)**, Lead. Rationale corrected (B3): partners the window cut puts in two windows cannot be merged by any window, and partners that share a window can be merged only as a deviation from the reviewed plan; only the plan makes them one test for certain |
| F6 | Batch brief forbids new case-critic rules; K1 edits :44 | (a) allowed as wording; (b) leave | **decided (a)**, Lead |
| F7 | NEW (B4). Legacy partners the cut-by-cases puts in two windows cannot be merged; and legacy has no C12 presence check of `plan_remarks`. Designer rule 6: a residual of the one-road class is a node with owns and a test, but the Lead's brief says "no new nodes" for TQ2-1 | (a) the Lead opens a finding now in `plans/piles/test-code-quality/findings/` with its row in the next untaken batch (PROJECT.md «Командная работа» item 2), naming the ONE mechanism for both roads: the window cut keeps merge groups together — `s5_plan.case_groups` / `test_adjacency` gain the case critic's merge edges, `controller.split_windows` likewise for legacy (owns: `scripts/s5_plan.py` `case_groups`, `scripts/controller.py` `split_windows`, `_scope_windows`; test: one row in `test_s5_plan_windows.py` / the controller cut table), plus C12 for legacy windows; a new idea that changes the cut "byte for byte" for legacy, so a plan to the owner and a critic on plan first (PROJECT.md new-idea steps 4, 6); (b) the owner's word accepting the residual for the driver process; (c) widen K2 now | **(a)**: one mechanism closes both the legacy residual and the planned-road pairs the plan leaves apart; it costs window size (a group over the cap becomes one `over_cap` window, `pack_windows` :433-435) and a changed legacy cut, which is why it is not slipped into K2. Until then K2-E12 says the residual in every legacy brief that has one. Owner-level per P31 if (b) |
| F8 | NEW (A6). A nominal `apart_reason` ("x") answering a case-critic merge | (a) the rubric bullet says the reason must name another setup, surface or fixture, otherwise it answers nothing and the merge stays a `blocker`; (b) any non-blank reason answers it, and a weak reason is a `remark` as in the first bullet (rubric :19-20) | **(a)**: under (b) the leak reopens through one word, against the owner's point 4; the judgment stays with the plan critic (AR-29) and code still reads presence only (K2-E7). Cost: none beyond the bullet's words |
| F9 | NEW (B2). Named raises vs compensations (§D.0) | (a) as §D.0: raise R1, R4, R5 (and R6 if over) by name to the after-measure within a bound; compensate R3 in place; (b) compensate everywhere: shorten the designer bullet to the P16 example alone (still over room 4), print nothing for 0 concerns (AR-23 lost in the plan brief), no rubric bullet (F5 unenforced) | **(a)**: (b) cannot fit R1 at all and breaks AR-23/F5; each raise is the measured need of the site that adds it (AR-20, axis 18). Cost: ≈ +39 tokens on the designer, ≈ +79 process tokens on the code critic, +39 B on one test brief |

## 8. Small technical choices closed here

- C1: the value-table rule REPLACES the "Equivalence partitioning" bullet (one bullet, craft section) instead of adding a new
  bullet; "never two cases for one class" is dropped as subsumed (no registry anchor names it: Grep over the package finds it only at
  `qa-case-designer.md:50`).
- C2: the value table uses the existing partition form (`P-<name>`, `artifact-contract.md:71-76`), named by the contract, not in the
  craft bullet (A10). No new case key, so no contract, validator or slice change.
- C3: the designer's rule stays inside ONE plan row (K1-E1). Cross-row duplicates go the owner's way: critic `merge` -> S5.
- C4: the merge hint joins on `tests[].cases` only. The shape, level and file of the tests are not compared.
- C5: one token reader, `critic_rollcall.parametrise_group`, beside `PARAMETRISE_TOKEN`. `s5_plan` imports it lazily, as it already
  imports `critic_rollcall` (`s5_plan.py:1121`).
- C6: one remark printer, `s5_plan.remark_lines`, and one placer, `s5_plan.placed_remarks`, beside `render_slice` / `window_slice`.
- C7: test homes are keep files only: `test_brief_pack_s5_plan.py` (test-layers.json:345, `data_join`), `test_s5_plan_grouping.py`
  (:4820), `test_role_rules.py` (:4623), `test_critic_rollcall_apply_fixes.py` (:1199, N5). No new test file. Rows cut to the ones
  that fail before the change (A5): the first draft's g ("byte-equal as before", docs/TESTING.md:97 «Как раньше»), e, p (internal
  exceptions), m, o (token and id parsing, already `_carries`'s / `case_ids`'s) are dropped.
- C8: the automator charter is not edited (§C.3).
- C9 (B1): `hint_rows` keeps its single meaning (grouping) and its K6 pins; merge hints get their own `merge_hint_rows` with the same
  `(rows, why)` contract, so no `why` of one family hides the other's rows.
- C10: `merge_hint_rows` words an exception as `hint_rows` does (`_show(exc, 100)`, s5_plan.py:1457); the brief prints it through
  `_text_whole` (FV1-4 N2, brief_pack.py:443-446).
- C11: a legacy brief for a dispatch the controller does not hold gets no concern lines (K2-E11): it has no window scope to place
  against, and it is the brief `role_brief_ratchet` builds (R7). That production builds always have the record is an estimate, not
  verified (the brief's caller was not traced).
- C12: role-rules anchors are 4-5 words (docs/TESTING.md:106).

## 9. Analogs and contradictions noticed (reported, not widened)

- `brief_pack._s5_kind` calls `s5_plan.mode(task_root, state)` without the process's `run_mode` (`brief_pack.py:1973`; the
  controller passes `self._run_mode()`, `controller.py:4437`, :6553, `_run_mode` :6519). For a dispatch on record, rule 2 decides
  first (s5_plan.py:405-406), so the legacy branch is reached correctly; for a brief before any S5 record the two could disagree.
- CC-n reaches S5 by the code route `remarks_of`, not through a handoff contract (`handoffs/gate-a-to-automator.yaml` has no concern
  field). AR-21's "each handover has one file that is contract and form" does not describe this carrier.
- `_placement` on area stories: a CC's `case` is the roll-call's bare id and the planned window keys are area keys, so today every
  case-critic concern of an area story is "unplaced" and goes to every planned window (over-carry, not loss). Same on the legacy
  filter. A match by `case_ids` inside `_placement` would fix both; not widened (the remark placement of plan reviews shares it).
- `references/manual-evidence.md` names no partition (K1-E7): a manual case with a table has no per-row evidence rule.
- `qa-case-critic.md:44` contradicts the confirmed rule (K1 fixes it); `test_case_merges.py:588` "a merge changes no case" is the
  pinned truth (quarantined file).
- `qa-automator.md:57` "what its brief does not list is not yours" is about a bind round; the first draft cited it for windows in
  general. §C.2 now cites :52.
- The critic's stale-reference list gives `test_s5_plan.py:253/:258 -> :277/:279`; on 5cc4f88 :253 and :258 still hold the two
  driver/legacy checks (re-read), so they are kept.
- RC2-3 (`roles-context/2`) edits the same critic lines as K1 (X4); RC1-2 meets K2 in the code critic's process row (X5).

## 10. Reading trail

Round 1 (be2c988), kept for history: the old draft; `docs/tasks/specs/t-723-tq1-27-amended.md`; the three charters;
`plans/piles/test-code-quality/batch-2-...md`; `P\handoffs\gate-a-to-automator.yaml`; `P\references\role-load.json`; parts of
critic_rollcall, s5_plan, brief_pack, controller, rubric, artifact-contract, ahead-cards, judgment-census, test-layers, architecture.md;
`plans/piles/onboarding-forge/batch-1-...md:1-46`.

Fix round (read-main **5cc4f88**), read whole: the verdict `docs/tasks/specs/reviews/20261113-tq2-1-revision-plan-critic.md`; this spec;
`P\references\role-load.json`. Read in part: `P\scripts\brief_pack.py:92-101, 440-447, 1581-1616, 1955-2104, 3550-3563, 4173-4269,
4355-4366`; `P\scripts\s5_plan.py:128-137, 157-169, 255-329, 384-419, 890-893, 1014-1026, 1060-1201, 1240-1504`;
`P\scripts\controller.py:410-449, 4285-4322, 4420-4554`; `P\scripts\s5_precheck.py:4280-4311`; `P\scripts\critic_rollcall.py:395-443,
905-924`; `P\scripts\contract.py:4250-4303`; `P\scripts\role_load.py:236-290`; `P\scripts\story_step.py:315-337`;
`P\references\code-review-rubric.md:1-36`; `P\references\inject-map.json:55-84`; `P\references\artifact-contract.md:68-91`;
`P\agents\qa-case-designer.md:44-63`; `P\agents\qa-case-critic.md:38-47`; `P\scripts\tests\test_brief_pack_s5_plan.py:1-25, 505-602`;
`P\scripts\tests\test_brief_pack.py:2340-2396`; `P\scripts\tests\test_s5_plan_grouping.py:1-60`; `P\scripts\tests\test-layers.json:280-365,
4588-4637, 7080-7109`; `docs/TESTING.md:45-119`; the old draft :286-305.
Searches (an empty or load-bearing result with its positive control of the same shape):
- Grep `ui_window_cases|def pack_windows|def split_windows|def _s5_window_cases|s5_window_cases` over controller.py -> :271 (default 2),
  :414, :446, :4305, :4443, :4540.
- Grep `^S5_PLAN_ROLES|^DISPATCH_DEFAULTS` over controller.py -> :116, :271.
- Grep `_file_concerns\(|_case_critic_files\(|case_concerns\(|hint_rows\(|_placement\(` over `P\scripts` -> callers: brief_pack:2011,
  gate_brief:2234, s5_plan :1092, :1158-1159, :1298, :1491, s5_precheck:4296; tests test_s5_plan.py:637-641, test_s5_plan_grouping.py:227-254.
- Grep (-i) `carried_concerns|case_concerns|remarks_of|accepted_rounds` over `P\scripts\*.py` (G2 negative; control: `s5_plan.py:1146`).
- Grep `code-review-rubric` over the package's `*.{json,yaml}` -> inject-map.json:72 (the code critic's load), role-rules rows,
  test-layers rows.
- Grep `kind: craft|^## ` over qa-case-critic.md (:27, :77), qa-case-designer.md (:28, :46, :62 process), code-review-rubric.md (no
  marker: process).
- Grep (-i) `BRIEF\w*_MAX\s*=|BYTES_MAX\s*=` over `P\scripts\tests` -> test_brief_pack_s5_plan.py:541, test_brief_pack.py:2364 (both
  found: the pattern is its own control).
- Grep (-i) `legacy` over `test_brief_pack*.py` -> k8 :517-534, docstring :14; test_brief_pack.py hits unrelated.
- Grep test-file names over test-layers.json -> keep :287, :345, :1199, :2793, :4592, :4623, :4820; cohort :7096-7101; quarantine
  :7372, :7453.
- Grep `"s5_precheck.py", "function": "plan_result"|"brief_pack.py", "function": "plan_dispatch_lines"|"critic_rollcall.py", "function":
  "_carries"` over judgment-census.json -> only :60 (control: the plan_dispatch_lines alternative); `plan_result`, `_carries` have no
  row. An earlier variant of this search with `build` returned nothing and is not used as evidence.
- Grep `remark_rows_missing\(` over `P\scripts` -> brief_pack:2580, s5_precheck:4468 (C12 on `self.piece`), tests.
- Grep `def _run_mode|self\._run_mode\(\)` over controller.py -> :4437, :6519, :6553, :6585, :6714.
- Grep `legacy|LEGACY` over test_s5_plan.py -> :253, :256-258, :267-270, :279, :286.
- Grep (-i) `never two cases|Equivalence partitioning|One case or partition` over the package -> only `qa-case-designer.md:50` among
  role texts (no registry anchor).
- Grep `One case per plan row|parametrised-inputs-no-repeat|designer-one-case-per-plan-row` over role-rules.json -> :26, :161; over
  qa-case-designer.md -> :23. (A first try with a brace glob over two paths returned nothing: a miscall, corrected by the path-specific
  calls.)
- Grep `(?i)partition` over manual-evidence.md -> none; control `(?i)evidence` on the same file -> 18.
- Grep `^def _text_whole|^def _short|^HEAD_LINE_CHARS|^def file_lines|^def _input_names` over brief_pack.py -> :443, :1133, :1952,
  :1207, :3550.
- Grep `^def case_config|^def _cfg_of|^def md_table` over contract.py -> :2845, :3302, :3314; `def stage_scope` over controller.py -> :4147.
Measurements: none by the designer (no shell in its tools). The numbers of §D.0 "Old" and "Room" are the critic's runs at 5cc4f88
(verdict trail "reruns"); the "Need" column is byte arithmetic on the expected text (estimate, not verified).
Not read: `docs/RUNBOOK.md` §9; `role_load.delivered_text` (whether the code critic is handed the rubric whole or a section: R5's
need is conditional on it); the brief's production caller (C11); `test_s5_plan_windows.py` (F7's test home, named, not read).

## 11. Fix round (critic-on-plan verdict, 13.11.2026)

Verdict: `docs/tasks/specs/reviews/20261113-tq2-1-revision-plan-critic.md` (fit_with_fixes, B1-B4, A1-A11). Lead decisions kept: F1-F6 =
(a); F5 (a) stands; §0 verbatim untouched; no node re-cut (K1, K2, N5).

| Item | What changed | Where |
|---|---|---|
| B1 (merge hints counted as grouping hints, "never a blocker") | `hint_rows` stays grouping-only (C9); new `merge_hint_rows` with the same `(rows, why)` contract; the plan critic gets its OWN merge line, which says "blocker ... even where a grouping hint names the same tests"; the grouping line (brief_pack.py:2015-2017) is byte-unchanged and never counts merge rows; `--check` and `s5_precheck.plan_result` print merge hints through `print_hints`; the second effect (a merge `why` hiding computed grouping hints) cannot occur | §1 rows AR-10/FR-10, AR-18; K2 items 7-9, 11; edge K2-E10; X6; row B2; owns gain `s5_precheck.py` `plan_result`, `s5_plan.main` |
| B2 (ratchets at zero room) | new §D.0: per ratchet the old value, the room, the need, the decision; R1 named raise, R2 unchanged, R3 compensated at the same byte length (critic :44 parenthesis rewritten to 59 B), R4 named raise with bound, R5/R6 (the code critic's load carries the rubric: inject-map.json:72, found in this round) named raises, R7 untouched by design; "13320 + slack" misreading removed; K1 and K2 own `role-load.json` keys; fork F9 | §D.0; K1 owns/DoD/key 4/edge K1-E8, expected text :44; K2 owns/DoD/item 15/edge K2-E16; §7 F9 |
| B3 (UI cap default 2; "land apart whenever" overstated) | §C.2 G1 rewritten: default 2 (controller.py:271, `_dispatch_setting` :4287-4303, `or 1` only for a project 0 at :4540), non-UI caps (:4305-4320), `pack_windows` first-fit (:414-443); the leak is conditional; "only the plan makes them one test for certain"; the L4 answer, §0's last paragraph, the F5 rationale and the rubric bullet's last sentence follow | §0, §C.2 G1, §7 F5, K2 item 13 |
| B4 (legacy road not covered) | re-derived on 5cc4f88: a legacy brief is built with `scope` = its dispatch scope (brief_pack.py:4180), the cut is by cases (controller.py:4428-4443, `split_windows` :446-449), no slice, no delta, no C12; K2 now hands each legacy window only the concerns of ITS cases through the one placement rule (`placed_remarks` / `_placement`, new `concerns_for_scope`), both S5 roles, only for a dispatch on record; the split-pair residual is said in the brief (K2-E12) and returned as F7 with the one-mechanism option; changelog no longer says "every road" | §C.2 G2; K2 items 3-4, 10, 12, 16; edges K2-E11..E13; rows B7-B8; §7 F7; §E texts |
| A1 (stale references) | every file:line of §C/§D re-taken on 5cc4f88 (list of the verdict's Q1 applied; `test_s5_plan.py:253/:258` re-read and kept, §9) | §C, §D, §8, §9 |
| A2 (`_text_whole`) | the exception head line uses `_text_whole(exc)` | K2 item 10 |
| A3 (`cfg`; area keys) | `merge_hint_rows` passes `C.case_config(task_root)`; match by `case_ids(key)` | K2 items 6-7; edge K2-E5; row G7 |
| A4 (receipt mismatch is not "none carried") | new `concern_report` with `rounds` and `silent`; the brief names silent files and distinguishes "none carried" / "none raised in N rounds" / "could not be read against the receipt" | K2 items 2, 10; edge K2-E3; row B6 |
| A5 (test rows) | rows cut to B1-B8 (one parameterised function) and G1-G9 (one table); g, e, p, m, o dropped; test-line budget in the DoD | K2 acceptance keys; DoD; §8 C7 |
| A6 (own bullet; nominal reason) | the rubric clause is its own bullet; nominal `apart_reason` returned as F8, written on (a) | K2 items 13-14; §7 F8 |
| A7 (vacuous "answered") | stated: `H` = the group's keys some test holds; `len(H) < 2` -> no hint | K2 item 6; edge K2-E8; row G6 |
| A8 (comment :4197, docstring :14) | both owned and rewritten | K2 owns, items 12, 15; siblings |
| A9 (green at entry) | DoD: `test_brief_pack_s5_plan.py` green at 5cc4f88, so every check green after; before/after rule for the rest | K2 DoD (and K1, N5 DoD in the same form) |
| A10 (`P-<name>` in craft) | removed from the designer bullet; RC2-3 process-row note in X4 | K1 expected text; §8 C2; X4 |
| A11 (E10 wording) | invariant reworded: same lines from one printer, over the cap in side file and slices | edge K2-E11 |
| beyond the verdict | K1-E7 corrected (manual-evidence.md names no partition, verified); registry anchors cut to ≤ 6 words (C12); N5 given/edges/DoD restated inline (a pointer is no DoD); X5 (RC1-2 vs K2 on the code critic's process row) | K1-E7; K1 item role-rules; K2 item 14; §D-N5; §6 X5 |

Forks returned in this round: F7 (legacy split residual and legacy C12: a finding with one mechanism, recommended), F8 (nominal
`apart_reason` answers nothing, recommended), F9 (named raises as §D.0, recommended). Each node is executable on the recommendations
before the answers.
