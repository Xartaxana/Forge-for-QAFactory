# t-723 — TQ1-27 (amended): the S4 case critic answers duplicates and level (P16, P19); a merge travels to S5 as a concern; the S4 exit holds the structure by code

Amended spec (designer, 02.11.2026) for node TQ1-27 of `plans/piles/release-next/batch-1-release-0-10-9.md` (release 0.10.9).
SELF-CONTAINED: it replaces `docs/tasks/specs/t-697-tq1-27-case-critic-merges.md` whole; the builder reads this file, not t-697.
It closes the plan critic `docs/tasks/specs/reviews/t-715-tq1-27-plan-critic.md` (`fit_with_fixes`, B-1, B-2, m-1..m-7) with the
Lead's decisions of the dispatch (t-723). R = `C:\Projects\yml-text-factory\.claude\worktrees\release-10-9-706cee`,
P = `R\ai-packages\qa-factory`. Forks in §6 carry a recommendation; §2–§4 are written ON the recommendations.

## 1. Goal, rules, invariants

**Goal.** On TP1-12586 (0.10.5) the S4 case critic approved 12 cases with no word on duplicates, merges, parametrisation or
level; the honest minimum was 9 (finding `R\plans\piles\release-next\findings\20261030-kritik-kejsov-ne-ishchet-dubli-i-sliyaniya-p16.md`).
After this node:
1. the critic's charter carries dimension 2b "Duplicates and level";
2. the critic's findings round carries a table `## Merge candidates` (`| cases | verdict | reason |`, verdict `merge|keep`) that code reads;
3. **a `merge` changes no case** (Lead, B-1): every case of a merge row gets the roll-call verdict `approve_with_concerns` with the
   note `parametrise into one test: <case ids>`; the existing concern carrier (`critic_rollcall.carried_concerns` ->
   `s5_plan.case_concerns`, HF4-11) hands it to the S5 automator as a `CC-n` remark, which the automator answers in `plan_remarks`
   (`applied` / `not_applicable`). The case count stays; the test count drops. No `Archived` status is written, no case is deleted;
4. the S4 exit refuses a round that leaves a pair of cases sharing a requirement unanswered, approves a merged case without that
   concern, leaves an e2e-ui/manual row without its `lower level:` line, or holds more cases than the S3 plan's `case_budget` with no
   `Over the case budget:` line;
5. the budget arrives as a number in the S4 brief; absent until its producer SC5-6 (`words-gates/1`) lands.

**Acceptance wording of the node (m-1):** "the structure by code (pairs answered, merges carried, level line, budget line); the three
calibration merges by the live run (FR-33)". Nothing in this node reports "12 -> 9 delivered"; the live-proof row (§5 Lead lines) is
where the three merges are proven.

**MEASURED FACT that shapes the design** (designer 02.11 on `Requirements:`; re-measured by the plan critic on `covers:` through
`branch_accounting._case_records`; re-read by this designer via Grep of `covers:` over the fixture, §7): the three calibration merges
share NO requirement — TC-003 (R-10) / TC-002 (R-5, R-6); TC-011 (R-9) / TC-001 (R-3, R-7); TC-005 (R-15, R-11) / TC-004 (R-13).
They are "same Given/When form" pairs, which only judgment sees: code never reads the Given/When wording (FR-12, AR-2; Lead
decision). The pairs code DOES owe on 12586 are exactly five, none a calibration merge: R-11 TC-005/TC-006, R-15 TC-005/TC-014,
R-8 TC-006/TC-010, R-4 TC-008/TC-012, R-9 TC-011/TC-012.

**Factory rules (FR) touched:** FR-38 (charter + ahead card + brief line state the check before the work), FR-1/FR-2/FR-57 (every
refusal names what it expected and a door the critic can open — a row, a note, a line; a person's word passes it through the existing
`waiver.py` door, narrowed to this refusal's own words, E11), FR-12 (code reads table cells and three fixed tokens
`parametrise into one test:`, `lower level:`, `Over the case budget:` — the kind of the existing `Unreviewed for Gate A:`; never the
Given/When form), FR-13 (closed words `merge|keep`, `P16|P19` — home: F1), FR-9 / FR-40 (B-1: the merge has an executor — the S5
automator — and no new state without a way out), FR-41/FR-59 (an unreadable budget, plan or scope is a note or the refusing
direction, never a pass, never the role's fault), FR-46 (the refusals are the call's: the critic repairs), FR-47 (code checks
presence and consistency; whether two cases ARE one form stays the critic's), FR-23 (empty outcome named), FR-33 (the three merges
proven live). Sections walked by the builder: A, B (refusal text is read by a role), C, D, E, G.

**Architecture invariants (AR) touched, and the change check each demands (carried into the DoD, §4):**
- **AR-10** (requirement before the work, in its fields). Check: K-DOC — the card names `## Merge candidates`, `merge|keep`,
  `P16 or P19`, `parametrise into one test:`, `lower level:`, `Over the case budget:`; the charter names `## Merge candidates`,
  `parametrise into one test:`, `lower level: impossible`; the S4 brief carries the budget line (K8b). Negative control per key.
- **AR-21 / AR-24** (what a stage gathers travels whole). Check: K-CAL — `carried_concerns` over the calibration round yields a
  `CC-n` for each of the six merged cases whose `problem` holds the token and the partner id.
- **AR-22** (every field read has a producer). `## Merge candidates` / the three tokens: producer the critic (charter 2b + card),
  reader `critic_rollcall.merge_candidate_errors` (this node). `case_budget`: producer SC5-6 (`words-gates/1`, NOT this node; Lead
  line L2), reader `branch_accounting.case_budget` (this node). Until SC5-6 lands the reader answers `None` and every consumer says
  "not set" (temporal edge E9). Check: K9 (reader wired into the S4 exit) + K8 (absent -> note).
- **AR-23** (empty outcome declared). Zero owed pairs, no merge row, no overrun -> the section may be absent; the check passes.
  Check: K1 clean case (E1).
- **AR-25** (every recorded state has a way out). B-1 kept by NOT introducing `Archived` as the merge outcome: the cases stay in
  every delivery reader as they are. Check: the diff touches no reader of case status/index (critic says); K-CAL asserts the six
  merged cases keep their status.
- **AR-13** (a fact with a reader is read through it). Case status through `contract.case_status` (m-7); a case's requirements by
  the reading of `handoff_check._requirements_of` (front `covers:` + `C.REQ_ID_RE`, inside `_case_records`); scope through
  `branch_accounting.critic_scope`; plan through `branch_accounting._plan`; rounds through `critic_rollcall._round_slice` (via the
  new `rounds` generator, also used by `_round_homes`); roll-call through `parse_rollcall`; concerns through `carried_concerns`.
  Check: the critic confirms no new reader of any of them.
- **AR-15 / AR-19** (one approach; twins together). The table copies `## Branch homes` (TQ1-17): newest round held to form, every
  round consulted for answers. The designer twin (F7 of t-697) is the queued node Q1 (§5).
- **AR-28** (an unknown never becomes a pass). Scope unknown -> every live case in scope; budget unknown -> no budget check, said
  in a note (a cost bound, never a correctness gate; E9 explains the direction).

**D-0048:** `exit_gate.py` (XT1-2) and `handoff_check.py` are NOT edited. Shared files carry FUNCTION lists in `owns` (§4):
`branch_accounting.py` (also WG1-1: `excluded:`/`branch_excluded_by_word`; RN1-26: `s5_scope`/`s5_problems` — disjoint),
`brief_pack.py` (7 pending nodes; this node: one new function + one call line in `build`), `qa-case-critic.md` (TQ1-24, CD1-13,
RN1-6, RN1-27 — this node's places are line-anchored). `sizing.py` is no longer touched (B-2) — no overlap with OH3-34.

## 2. Change list (file -> function/anchor -> behaviour/text -> test)

Test ids (K-...) are defined in §4. Refusal texts are English (FR-30), start from the problem, then ` - fix:` with the door.

### 2.1 `P\scripts\critic_rollcall.py`

1. **Constants** next to `CASE_CRITIC_VERDICTS` (line 43):
   `MERGE_HEADING = "## Merge candidates"`, `MERGE_COLUMNS = ("cases", "verdict", "reason")`, `MERGE_VERDICTS = ("merge", "keep")`,
   `KEEP_GROUNDS = ("P16", "P19")`, `PARAMETRISE_TOKEN = "parametrise into one test:"`, `LEVEL_TOKEN = "lower level:"`,
   `LEVEL_IMPOSSIBLE = "impossible"`, `BUDGET_LINE = "Over the case budget:"`,
   `MERGE_ROW_FORM = "| TC-a, TC-b | merge or keep | P16: <why> / P19: <why> / <what the merged test keeps> |"`.
   Every refusal this node adds contains the literal `Merge candidates`, `lower level:` or `Over the case budget:` (E11).
2. **`rounds(text)`** (new generator): yields `(index, round_text)` newest-first, cutting with `_round_slice` exactly as the loop of
   `branch_accounting._round_homes` does today (`first = _round_slice(rest) or rest; rest = rest[len(first):]` while `rest.strip()`).
   `_round_homes` is switched to it (same behaviour; its tests in `test_branch_accounting.py` are the witness). Test: K2 (older round).
3. **`parse_merge_candidates(text, artifacts=None) -> (rows, bad_header)`** — rows of the `## Merge candidates` table of ONE round:
   `[{"ids": [case ids], "verdict": str, "reason": str}]`. Table by `C.md_table(text, MERGE_HEADING)`; header cells lower-cased,
   backticks stripped; columns found by name, any order; a missing column -> `bad_header` = "the table has no `<name>` column".
   Ids by `C.case_ids(cell, cfg=C.case_config(artifacts))` (project id form, B-013). Verdict lower-cased, backticks stripped.
   Absent section -> `([], "")`. Test: K1, K2, K7.
4. **`merge_candidate_errors(task_root, files=None) -> (errors, notes)`** — the new S4 exit check; `files` default
   `findings_files(task_root)`. It only composes the helpers below (each < ~60 lines; code-quality fix of the plan critic):
   a. **Live cases** = `branch_accounting._case_records(task_root)` minus records whose `status` (§2.2) is exactly `Archived`.
      **Scope** = `branch_accounting.critic_scope(task_root)`; `None` -> every live case. **Rounds**: per findings file,
      `rounds(text)`; per round its merge rows and its roll-call rows (`parse_rollcall`).
   b. **`_merge_form_errors`** — the NEWEST round of each file only: per row, a refusal for: fewer than 2 ids; an id that is no live
      case of this story ("names TC-x, which is no case of this story, or it is Archived"); verdict outside `MERGE_VERDICTS`; `keep`
      whose reason's first token (stripped of `*`, `` ` ``, `:`, `(`) is not in `KEEP_GROUNDS`; `merge` with an empty reason; two
      rows of the round answering one pair with different verdicts ("answered twice: merge and keep"). A `bad_header` -> one refusal
      with `MERGE_ROW_FORM`. Every text contains `Merge candidates`. Test: K2.
   c. **`_owed_pair_errors`** — owed pairs = every unordered pair (a, b) of live cases with `covers(a) & covers(b)` non-empty and at
      least one in scope. ANSWERED when some round (newest first) has a merge row whose id set contains both; its ANSWER is the
      newest such row. Unanswered owed pair -> refusal:
      "`TC-a` and `TC-b` both cover R-n[, R-m] and no round answers the pair under `## Merge candidates` - fix: a row
      `| TC-a, TC-b | merge or keep | <reason> |` under `## Merge candidates` of this round (`keep` only with P16: one red line could
      not tell the branches apart, or P19: they need different levels; `merge`: both cases `approve_with_concerns` with
      `parametrise into one test: TC-a, TC-b` in the note)". Pairs one per line up to `branch_accounting.limit("refusal_units_shown")`
      (20 today), then ONE line "<k> more pairs under Merge candidates (<n> in all); answer these first, the check runs again"
      (the `_stage_check` shape). A pair with neither case in scope and no answer -> a NOTE. Test: K1, K3, K3b, K-CAL.
   d. **`_merge_concern_errors`** (replaces t-697's "merge needs rework"; B-1) — for every pair whose ANSWER is `merge`, for every
      case X of that merge row: find the newest round whose roll-call lists X in a row marked `reviewed: yes` (row `ids` contain X;
      the same "latest round that lists the case decides" rule `s5_plan._file_concerns` applies when it carries concerns). Then:
      - X listed nowhere -> NOTE "the merge of <ids> names X, which no round reviewed".
      - its row's word is `approve_with_concerns` and the row's `note` holds `PARAMETRISE_TOKEN` (case-insensitive, whitespace
        collapsed) followed by every OTHER id of the merge row (`C.case_ids` over the note text after the token) -> fine.
      - its word is `approve`, `approve_with_fixes`, or `approve_with_concerns` without the token or without a partner id -> refusal:
        "the round answers `merge` for TC-a, TC-b under `## Merge candidates`, and TC-x is approved without the merge reaching S5:
        only an `approve_with_concerns` row whose note says `parametrise into one test: TC-a, TC-b` is carried to the automator -
        fix: give TC-x's roll-call row the verdict `approve_with_concerns` and that note, or answer the pair `keep` with its P16/P19
        reason".
      - its word is `reject` or `partial` (or the row has no `verdict` column) -> no refusal from this check: X is not approved; the
        round that later approves X is held to the same rule (E8).
      Test: K4, K5, K-CAL.
   e. **`_level_errors`** — for every roll-call row of the NEWEST round marked reviewed whose plan row (`branch_accounting._plan`,
      row by the roll-call `plan_row` cell id) has `level == "e2e-ui"` or `disposition` in `branch_accounting.MANUAL_DISPOSITIONS`,
      skipping `disposition` in `branch_accounting.PLAN_EXCLUDING`: the `note` must contain `LEVEL_TOKEN` followed (after spaces) by
      `impossible` + ` - ` + a non-empty reason, or by one word of `C.PLAN_LEVELS` standing BEFORE the row's own `level` in
      `C.PLAN_LEVELS` (any level word when the row has no `level`) + ` - ` + a reason. A level word (not `impossible`) requires the
      row's verdict `approve_with_concerns` or `reject` (the word reaches the automator only as a concern; P17: the automator chooses
      the level). Refusals name the plan row and the expected token (`lower level: impossible - <why>` or
      `lower level: <unit|component|api|integration> - <why>`). Rows present but the roll-call has no `note` column -> one refusal
      asking for the column. `_plan` raising `Unreadable` -> this step is skipped with a note naming it (E13). Test: K6, K-CAL.
   f. **`_budget_errors`** — `n = branch_accounting.case_budget(task_root)`; `None` -> note "no case budget in the S3 plan
      (work/test-plan.json `case_budget`): the case count was not held to one" and stop. Count = live cases. Count > n and the
      newest round has no line whose stripped text starts with `BUDGET_LINE` followed by non-empty text -> refusal: "the story has
      <count> cases and the S3 plan's case budget is <n>; the round does not say why the cases over it stay (`Over the case
      budget:`) - fix: a line `Over the case budget: <why each case over <n> stays>` in this round, or merge". Count <= n -> nothing.
      Test: K8.
   Never raises on a story artefact (an unreadable file is a note naming it); its own defect propagates to `detector_main`'s
   existing `except` (UNREADABLE, exit 3).
5. **`_detector_body`** (line 787): after `errors = [...findings_errors...]`: `more, notes = merge_candidate_errors(task_root, files)`;
   `errors += more`; print each note as `note: <text>` AFTER the digest lines and BEFORE the `OK:` / `REJECT —` line (never between
   a `REJECT —` head and its `- ` lines: a non-`- ` line there makes `detector_verdict.parse` read the block as unmigrated). The
   REJECT block, the waiver door line, exit codes stay. **`main` is NOT changed** (m-7: its per-file CLI has no caller but
   `--apply-fixes`, and the critic has no Bash; rule 18). `findings_errors` is NOT changed (write-time hook path,
   `validate_artifacts.py`: the new check is exit-only, like `## Branch homes`). Test: K9.

### 2.2 `P\scripts\branch_accounting.py`

1. **`_case_records`** (line 1466): add two keys — `"covers"`: `set(C.REQ_ID_RE.findall(C.front_line(text, "covers") or ""))`
   (the reading of `handoff_check._requirements_of`: front `covers:` + `REQ_ID_RE`, named as reused, not new); `"status"`:
   `C.case_status(path)` (THE reader, contract.py:3234; m-7). Nothing else changes; existing readers ignore the keys. Test: K0.
2. **`case_budget(task_root) -> int | None`** (new, beside `_plan`): `doc = _plan(task_root)[0]`; returns `doc["case_budget"]` when
   `doc` is a dict and the value is an `int` (not `bool`) >= 1; `None` when the plan is absent, `_plan` raises `Unreadable`, the key
   is absent, or the value is of another type or < 1 — never raises. Docstring: "the number of cases the S3 plan allows the story;
   written by the strategist's plan under SC5-6 (words-gates/1); absent until then". Test: K8.
3. **`_round_homes`** (line 1505): its round loop uses `critic_rollcall.rounds` (§2.1.2); behaviour unchanged.

### 2.3 `P\scripts\brief_pack.py`

**`s4_case_budget_line(task_root, role) -> list`** (new): for `role in S4_STAND_ROLES` only: `n = branch_accounting.case_budget(task_root)`;
`n` -> `["- Case budget: <n> cases for this story (the S3 plan); over it, the case critic's round says why each extra case stays (`Over the case budget:`)"]`;
`None` -> `["- Case budget: not set for this story"]`; any exception -> `[]` (a brief line is a courtesy, as `s4_stand_lines`).
**`build`**: one call line right after `head += s4_stand_lines(...)` (line 2721), inside the same `if stage == "S4":`. Test: K8b.

### 2.4 `P\agents\qa-case-critic.md` — charter, PAIRED CUT (net bytes <= 0)

Base: this worktree's file (RN1-7's 7d at lines 59-61; TQ1-2's sentence already merged, line 65 — no other branch to wait for, m-3).
INSERT after line 37 (`   2. Atomicity — one case, one scenario.`):
```
   2b. **Duplicates and level**. Cases one branch apart, on one requirement or one Given/When form, are one
      parametrised test. Answer each such pair under `## Merge candidates`: `keep` only for P16 (one red line could not
      tell the branches apart) or P19 (another level); `merge` puts `parametrise into one test: <ids>` in each case's
      `note`, verdict `approve_with_concerns`. An e2e-ui or manual row's `note` says `lower level: impossible - <why>`
      or `lower level: <level> - <why>`.
```
CUT (the four named cuts stand — Lead; measured by the plan critic 57 / 166 / 65 / 219 B, all present, none pinned):
- lines 40-41: `: as prose it reached S5\n      unchecked on TP1-15045` (the sentence then ends "... is a `concern`.");
- lines 54-55: the sentence `On TP1-15045 both shapes shipped: AC-4's "former position" against the implementing developer's comment, and a 404 body borrowed from another ticket.`;
- line 76: `, because Gate A matches your receipt against the end of the file` (sentence ends "... are never edited.");
- lines 115-117 (`## Witness`, m-3 corrected refs): the first sentence `` `critic_rollcall.py` recomputes the verdict from your roll-call when the file is written and again at the exit gate: an approving verdict beside an unreviewed row is refused there, so write the verdict the table earns. ``
Byte arithmetic: cuts 507 B (measured). The insert above is ~506 B by the designer's hand count (estimate, not measured: no shell) —
it is longer than t-697's 464 B because B-1 replaced "`merge` makes the case to fold `reject`" with the concern wording. The builder
MEASURES before/after; if after > before, it ALSO cuts the fallback `That cap stops review loops, not one-line repairs —\nsee \`approve_with_fixes\`.`
(lines 15-16, 80 B, unpinned — plan critic) and reports both numbers. If still positive: stop and return a question, never invent a cut.

### 2.5 `P\references\ahead-cards.json` -> `cards.qa-case-critic.text` (cap 1,200 B, `test_ahead_cards.py`)

APPEND (after "... beside any other verdict."):
`Cases sharing an R-n: a row per pair under \`## Merge candidates\` (cases | verdict merge|keep | reason; keep starts P16 or P19); merge: each case \`approve_with_concerns\`, note \`parametrise into one test: <ids>\`. e2e-ui/manual row notes: \`lower level: <level|impossible> - <why>\`. Over the brief's case budget: an \`Over the case budget:\` line.`
(one leading space joins it to the previous sentence; ~341 B, hand count).
CUTS, all applied (F3): (1) ` - with that column the code reads the field and stops reading your prose` (73 B); (2) ` - the gate
decides on what was reviewed, so it has to be told what was not` (75 B); (3) ` rather than by another design round` (36 B, mandatory —
Lead, m-2); (4) `, so the file has to carry the trail` (36 B); (5) ` in those words` (15 B). Estimate: 1,077 − 235 + 341 = ~1,183 B.
Cuts 4–5 are needed because the add now carries the B-1 concern wording, the `lower level:` mention (FR-38, m-2) and the renamed
budget line; the Lead's 1,174 B was measured for t-697's 281 B add. None of the five is pinned (Grep §7, positive control = the card
itself). `test_ahead_cards.py` prints the measured size in its check line — that is the witness. Over 1,200 after all five: stop and
return a question. `sources` stays `["critic_rollcall.py"]`.

### 2.6 `P\scripts\tests\test_ahead_cards.py` -> `VOCABULARIES`

Add `("qa-case-critic", "merge verdicts", critic_rollcall.MERGE_VERDICTS)` and `("qa-case-critic", "keep grounds", critic_rollcall.KEEP_GROUNDS)`.

### 2.7 New files

`P\scripts\tests\test_case_merges.py` — every K-test of §4. `P\changelog.d\release-next-1-tq1-27.md` — CHANGELOG voice, English (§4).

**Not touched:** `exit_gate.py`, `handoff_check.py`, `handoffs/*.yaml`, `sizing.py`, `contract.py` (read only), `check_delivery.py`,
`controller.py`, `case_stamp.py`, `s5_plan.py` (the concern carrier is used as is), `agents/qa-case-designer.md` (Q1),
`references/code-review-rubric.md`, `references/coverage-design.md`.

## 3. Edges, each with the invariant it protects

| # | Edge | Behaviour | Invariant |
|---|---|---|---|
| E1 | One live case, or zero | No pair; no section needed; passes. | An empty measurement is a stated outcome, never a refusal for a table nothing could fill (FR-5, AR-23). |
| E2 | Zero owed pairs, >= 2 cases, no overrun | Section absent or empty passes; the charter still asks for form pairs, code cannot see them. | Code never claims a pair it cannot establish structurally (FR-12, AR-2). |
| E3 | A pair shares a requirement, different When | Still owed; `keep` with P16/P19 passes. | A shared requirement is never left unexamined; code never judges the When (FR-47). |
| E4 | `merge` row of three ids | Answers its three pairs; every one of the three, where approved, carries the token naming the two others. | A row answers exactly its own pairs; a merge reaches S5 for each case it names. |
| E5 | Pair answered in an older round, newest silent | Answered. A `merge` answer still holds 2.1.4d against the newest round listing each case. | An earlier merge is never silently dropped by a later round. |
| E6 | Newest round re-answers `keep` after an older `merge` | Newest answer wins; no concern needed. | The critic may change its mind, only in writing with a P16/P19 reason. |
| E7 | A case `status: Archived` (by another flow) | Not live: owes no pair; a merge row naming it is a form refusal. Exact word via `contract.case_status`: `"Archived"` quoted or `archived` lower case are LIVE. | Error direction is over-inclusion only: a live case is never dropped from the pair check. |
| E8 | Merged case `reject`/`partial` (incl. round cap -> gate A) | No refusal here; the round that later approves it must carry the token. At the cap the merge row stays in the findings file gate A shows. | No merged case is ever APPROVED by the critic without the concern; this node adds no halt (FR-57). |
| E9 | `case_budget` absent (always before SC5-6) | No budget check; note; brief says "not set". After SC5-6 writes the key, check and brief activate with no change here. Error direction: an absent budget can only fail to ask for a line, never refuse. | A cost bound unknown to the factory never becomes a refusal of the role (FR-3, FR-46); it is said (FR-41). |
| E10 | Budget present: count == n / n+1; values `0`, `-1`, `"10"`, `true`, `10.0` | == n: nothing; n+1 without line: refusal; with `Over the case budget: <text>`: pass; the prefix with nothing after: refusal; invalid values: `None` (E9). | Over the budget is never passed silently; the factory's own bad datum is never the role's refusal. |
| E11 | In-flight story: a newest round without `## Merge candidates` (builder-rules 9) | Owed pairs -> refusal with the one-row door. A person's word passes ONLY this node's lines: `waiver.py --stage S4 --block "Merge candidates"` (or `"lower level"`, `"Over the case budget"`); records are `critic_rollcall.py: <line>` and matched by `contract.names_whole`, so a word of these never passes a roll-call/verdict refusal (no existing refusal holds them). Older rounds are never form-checked. | An in-flight story is never stuck, and a person's word on merges never lifts an unrelated refusal (m-5). |
| E12 | Scope unreadable (`critic_scope` -> None) | Every live case in scope. | Unknown scope is the whole set (AR-28), the refusing direction. |
| E13 | `test-plan.json` absent/unreadable | Level step skipped with a note naming it; pair, merge-concern steps still run; `case_budget` -> None (E9). | A missing plan never voids the pair check; the level check never guesses a level. |
| E14 | Roll-call row naming several cases (CX1-12) | 2.1.4d reads the row whose `ids` contain the case; the level step is per plan row. | One row's word is never read for a case it does not name. |
| E15 | Case without `covers:`, or `covers: [AC-1]` | `covers` holds only R-ids; empty -> owes no pair. | A non-requirement key never makes a pair (B-405). |
| E16 | Merge row naming a case of another story (shared store) | "no case of this story" form refusal. | A row never answers for a case the story does not own. |
| E17 | `keep` with `P19` but both cases at one level | Passes code. | Code checks that a ground was named, never whether it is true (FR-47). |
| E18 | Conflicting own requirements: "keep only P16/P19" vs two different behaviours sharing a requirement | `P16` covers it (one red line cannot be one test for two behaviours: the critic says which behaviour each red line names). | No requirement of this spec forces a wrong merge. |
| E19 | `lower level: e2e-ui` on an e2e-ui row; `lower level: api` on an api manual row | Refusal "not lower than the row's level". | A level line names a real step down or `impossible`. |
| E20 | Conflicting own requirements: a merged case on an e2e/manual row with a level word | One note carries both tokens; both steps read the same `approve_with_concerns` row. | The two concerns never demand different verdicts. |
| E21 | Merge partners land in different S5 windows (cut not verified by this designer) | Each case's window gets its `CC-n`; the automator answers `applied` or `not_applicable` with its reason in `plan_remarks`. | A merge is advice to S5, never a delivery gate: unapplied, it costs one test, never a lost or uncovered case (check_delivery reads `covers[]` of a test, :626-629). Window co-location is a Lead queue line (L4). |
| E22 | Owed pairs > 20 | 20 lines + one "<k> more pairs under Merge candidates (<n> in all)" line. | Truncation never hides the count, and the tail line carries the waiver words too. |
| E23 | A note `parametrise into one test:` with no merge row | Not read by code; the pair (if owed) still needs its row. | Code reads the token only to verify a written `merge`, never as an answer. |
| E24 | Two rows of the newest round answer one pair differently | Form refusal "answered twice". | One answer per pair per round. |

**Reused functions in a more consequential role** (designer rule 1): `branch_accounting._case_records` and `critic_scope` (advice
readers -> gate input), `contract.case_status` (stamp skip -> gate input). Allowed error direction: OVER-include (a retired case
counted live -> one extra row asked). Forbidden: under-include (a live case missed -> a pair passes unanswered). Adversarial inputs
that must stay safe, each in K0: a BOM before front matter (`_FRONT_RE` and `case_status` both read it); `status: "Archived"` quoted
(live); `status: archived` (live); `covers: [R-1,R-2]` no spaces; `covers: [AC-1]` (empty); `status:` only in the body (live:
`case_status` reads front matter). `carried_concerns` is used as is (its existing role).

## 4. Builder material

```
given: R\docs\tasks\specs\t-723-tq1-27-amended.md (this spec, whole); P\design\factory-rules.md (whole); R\plans\builder-rules.md;
  P\design\architecture.md (AR-10, AR-13, AR-21, AR-22, AR-23, AR-25, AR-28);
  P\scripts\critic_rollcall.py; P\scripts\branch_accounting.py (_case_records, _round_homes, _plan, critic_scope, limit,
  MANUAL_DISPOSITIONS, PLAN_EXCLUDING, _stage_check); P\scripts\contract.py (case_status, case_ids, md_table, front_line, REQ_ID_RE,
  PLAN_LEVELS - read only); P\scripts\s5_plan.py (_file_concerns, case_concerns - read only); P\scripts\waiver.py (split_overridden -
  read only); P\scripts\detector_verdict.py (parse - read only); P\scripts\brief_pack.py (s4_stand_lines, build :2721);
  P\agents\qa-case-critic.md; P\references\ahead-cards.json; P\scripts\tests\test_ahead_cards.py; P\scripts\tests\test_case_gates.py;
  P\scripts\tests\test_branch_accounting.py; P\scripts\tests\test_carried_concerns.py;
  fixture (READ ONLY, copy to temp): P\scripts\tests\fixtures\run-12586-red-then\controller\TP1-12586\work\test-cases\integrations\TC-*.md
  and ...\TP1-12586\work\test-plan.json
owns:
  C:\Projects\yml-text-factory\.claude\worktrees\release-10-9-706cee\ai-packages\qa-factory\scripts\critic_rollcall.py (constants of 2.1.1, rounds, parse_merge_candidates, merge_candidate_errors, _merge_form_errors, _owed_pair_errors, _merge_concern_errors, _level_errors, _budget_errors, _detector_body)
  C:\Projects\yml-text-factory\.claude\worktrees\release-10-9-706cee\ai-packages\qa-factory\scripts\branch_accounting.py (_case_records, case_budget, _round_homes)
  C:\Projects\yml-text-factory\.claude\worktrees\release-10-9-706cee\ai-packages\qa-factory\scripts\brief_pack.py (s4_case_budget_line, build: one call line after :2721)
  C:\Projects\yml-text-factory\.claude\worktrees\release-10-9-706cee\ai-packages\qa-factory\agents\qa-case-critic.md (insert after line 37; cuts at lines 40-41, 54-55, 76, 115-117; fallback 15-16)
  C:\Projects\yml-text-factory\.claude\worktrees\release-10-9-706cee\ai-packages\qa-factory\references\ahead-cards.json (cards.qa-case-critic.text)
  C:\Projects\yml-text-factory\.claude\worktrees\release-10-9-706cee\ai-packages\qa-factory\scripts\tests\test_ahead_cards.py (VOCABULARIES)
  C:\Projects\yml-text-factory\.claude\worktrees\release-10-9-706cee\ai-packages\qa-factory\scripts\tests\test_case_merges.py (new)
  C:\Projects\yml-text-factory\.claude\worktrees\release-10-9-706cee\ai-packages\qa-factory\scripts\tests\test_case_gates.py (fixture rounds inside part_* functions only, if the new check turns them red; expected none)
  C:\Projects\yml-text-factory\.claude\worktrees\release-10-9-706cee\ai-packages\qa-factory\scripts\tests\test_branch_accounting.py (fixture rounds only, if red; expected none)
  C:\Projects\yml-text-factory\.claude\worktrees\release-10-9-706cee\ai-packages\qa-factory\changelog.d\release-next-1-tq1-27.md (new)
non-goals: exit_gate.py, handoff_check.py (D-0048, XT1-2); any Archived/delete/fold of a case and every delivery reader of case
  status (Q1); writing `case_budget` (SC5-6); sizing.py; S5 code duplicates (TQ1-7/TQ1-19); code-review-rubric.md; gate A rendering
  of the table; the S5 window cut (L4); the live calibration run (live-runs, FR-33); critic_rollcall.main; findings_errors.
handoff: C:\Projects\yml-text-factory\.claude\worktrees\release-10-9-706cee\docs\tasks\handoffs\t-NNN-tq1-27.md
edges: §3 E1-E24 of this spec (each has a K-test or is stated code-free)
DoD: the verification run below, verbatim output in the handoff; `python -B ...\scripts\tests\test_case_merges.py` first
```

**Acceptance keys (K-tests, all in `test_case_merges.py`):**
- K0 `_case_records` on temp cases: `covers`/`status` for the six adversarial inputs of §3 (BOM + `status: Archived` -> `Archived`;
  quoted -> `"Archived"`, live; `archived` live; `[R-1,R-2]` -> {R-1, R-2}; `[AC-1]` -> empty; body-only status -> `''`). On the 12586
  fixture copy: owed pairs exactly R-11 TC-005/TC-006, R-15 TC-005/TC-014, R-8 TC-006/TC-010, R-4 TC-008/TC-012, R-9 TC-011/TC-012.
- K1 two cases sharing R-1, round with no section -> one refusal naming both ids, `R-1`, `Merge candidates`; add `keep | P16: ...` ->
  clean; two cases sharing nothing, no section -> clean (E1/E2).
- K2 newest-round form: 1 id; unknown id; verdict `fold`; `keep` reason `because`; `merge` empty reason; one pair answered `merge` and
  `keep` in two rows; table without `reason` column -> seven named refusals. The same defects in an OLDER round -> none.
- K3 A, B, C share R-1: row `A, B, C | keep | P19: ...` -> clean; only `A, B | keep | P16: ...` -> refusals name A/C and B/C.
- K3b 22 owed pairs -> 20 pair lines + one line holding `22 in all` and `Merge candidates` (E22; limit read from
  `branch_accounting.limit`, the test reads the same value, AT and BEYOND: 20 pairs -> 20 lines, no tail; 21 -> 20 + tail).
- K4 `merge` A, B: A `approve_with_concerns` note `parametrise into one test: A, B`, B the same -> clean; B `approve` -> refusal naming
  B; B `approve_with_fixes` -> refusal; B `approve_with_concerns` without the token -> refusal; B's note naming only B -> refusal
  (partner absent); B `reject` -> clean (E8); token in other case (`PARAMETRISE INTO ONE TEST:`) -> clean. Three-id row (E4): one of
  three lacks a partner id -> refusal.
- K5 older round `merge` A, B with both concerns, newest round lists only A with `approve` -> refusal for A; newest lists neither ->
  clean (older round decides); newest answers `keep | P16: ...` -> clean (E6); A `status: Archived` -> the merge row is a form
  refusal only if it is in the NEWEST round (older round: not form-checked).
- K6 plan row `e2e-ui`: no token -> refusal; `lower level: impossible - stand-only path` -> clean; `lower level: component - x` with
  `approve` -> refusal, with `approve_with_concerns` -> clean; `lower level: e2e-ui - x` -> refusal (E19); `manual-agent` row at
  `api` with `lower level: api - x` -> refusal; `skip` row -> nothing; no plan file -> note, no refusal (E13).
- K7 a project case-id form (`TP1-1_TC_001` via `config.case_id_form`, as `test_branch_accounting` sets it) read in the cells and
  after the token.
- K8 `case_budget`: plan absent, key absent, `0`, `-1`, `"10"`, `true`, `10.0`, unreadable plan -> None; `10` -> 10. With budget 2:
  2 live cases -> nothing; 3 -> refusal holding `Over the case budget:`; 3 + `Over the case budget: TC-3 needs its own fixture` ->
  clean; the prefix alone -> refusal; 3 cases, one `Archived` -> nothing.
- K8b `s4_case_budget_line`: budget 10 -> line with `10`; none -> `not set`; role `qa-automator` -> `[]`; `case_budget` raising
  (monkeypatched) -> `[]`.
- K9 `detector_main` on a temp story (`pipeline.json` S4 running, as `test_case_gates` builds one): unanswered pair -> exit 1, the
  waiver door line, `DV.parse` reads >= 1 finding and no `unmigrated`; a budget-absent note printed and still exit 0 on a clean story;
  `merge_candidate_errors` raising (monkeypatched) -> `UNREADABLE`, exit 3. Waiver (E11): `waiver.split_overridden` with an override
  `match: "Merge candidates"` passes the pair refusal and does NOT pass `critic-findings.md: no \`Verdict:\` line ...`.
- K-CAL (12586 fixture copy; docstring: "pins that the code CARRIES and HOLDS the three calibration merges when the critic writes them;
  it does not find them — the three share no requirement; their finding is the live run, FR-33"): one round with a roll-call row per
  plan row that has a case; `## Merge candidates`: TC-002, TC-003 `merge`; TC-001, TC-011 `merge`; TC-004, TC-005 `merge`; the five
  owed pairs `keep` with P16/P19 reasons. Rows TS-1..TS-5, TS-11 `approve_with_concerns` with `parametrise into one test: <both ids>`;
  TS-8, TS-9 (e2e-ui automate) `lower level: component - developers' component test`, `approve_with_concerns`; TS-10, TS-12 (e2e-ui
  manual-agent) and TS-14 (api manual-agent) `lower level: impossible - <why>` (the test asserts these five levels/dispositions from
  `test-plan.json` first). Asserts: no error; `carried_concerns(data, sha256(data))` yields concerns for exactly TC-001..TC-005, TC-011,
  TC-008, TC-009, and each of the six merged cases' `problem` holds the token and its partner id; the six case files' `status` is
  unchanged after the check. Negatives: drop the TC-006/TC-010 row -> refusal names TC-006, TC-010, R-8; TS-3 `approve` -> refusal
  names TC-003; TS-2 note without TC-003 -> refusal; TS-8 note without the token -> level refusal; TS-12 note without the token ->
  level refusal; drop all three merge rows and set the six rows to `approve` -> NO refusal from the merge check (the honest negative).
- K-DOC (doc witness; keys fixed HERE, verbatim; script in `test_case_merges.py`): charter keys `2b. **Duplicates and level**`,
  `## Merge candidates`, `parametrise into one test:`, `lower level: impossible`, `P16`, `P19`; card keys `## Merge candidates`,
  `merge|keep`, `P16 or P19`, `parametrise into one test:`, `lower level:`, `Over the case budget:`. Charter keys ABSENT:
  `both shapes shipped`, `matches your receipt against the end`, `recomputes the verdict from your roll-call`. Negative control: each
  key removed from a temp copy -> reported missing (the test fails on the copy, passes on the real file).
- AR change checks (in the report): AR-10 = K-DOC + K8b; AR-21/24 = K-CAL carried concerns; AR-22 = K9 + E9 note; AR-23 = K1
  clean-with-no-pair; AR-25 = K-CAL statuses unchanged + "no reader of status/index touched" (diff); AR-13 = no new reader (critic).

**Verification run (EXACT; absolute paths, no `cd`):**
```
python -B -c "import pathlib;p=pathlib.Path(r'C:\Projects\yml-text-factory\.claude\worktrees\release-10-9-706cee\ai-packages\qa-factory\agents\qa-case-critic.md');print(len(p.read_bytes()))"
python -B C:\Projects\yml-text-factory\.claude\worktrees\release-10-9-706cee\ai-packages\qa-factory\scripts\tests\test_case_merges.py
python -B C:\Projects\yml-text-factory\.claude\worktrees\release-10-9-706cee\ai-packages\qa-factory\scripts\tests\test_ahead_cards.py
python -B C:\Projects\yml-text-factory\.claude\worktrees\release-10-9-706cee\ai-packages\qa-factory\scripts\tests\test_branch_accounting.py
python -B C:\Projects\yml-text-factory\.claude\worktrees\release-10-9-706cee\ai-packages\qa-factory\scripts\tests\test_case_gates.py
python -B C:\Projects\yml-text-factory\.claude\worktrees\release-10-9-706cee\ai-packages\qa-factory\scripts\tests\test_carried_concerns.py
python -B C:\Projects\yml-text-factory\.claude\worktrees\release-10-9-706cee\ai-packages\qa-factory\scripts\tests\test_detector_unreadable.py
python -B C:\Projects\yml-text-factory\.claude\worktrees\release-10-9-706cee\ai-packages\qa-factory\scripts\tests\test_critic_rollcall_apply_fixes.py
python -B C:\Projects\yml-text-factory\.claude\worktrees\release-10-9-706cee\ai-packages\qa-factory\scripts\tests\test_case_roles_twin_rules.py
python -B C:\Projects\yml-text-factory\.claude\worktrees\release-10-9-706cee\ai-packages\qa-factory\scripts\tests\test_brief_pack.py
python -B C:\Projects\yml-text-factory\.claude\worktrees\release-10-9-706cee\ai-packages\qa-factory\scripts\selftest.py --limits --lang
```
The first line runs BEFORE the first edit and AFTER the last (both outputs in the report; after <= before). The card size is the
number `test_ahead_cards.py` prints in "qa-case-critic: the card fits the budget (<n> B <= 1200)". If a fixture round of
`test_case_gates.py` / `test_branch_accounting.py` goes red because of the new detector call, the builder fixes the FIXTURE ROUND
(adds the row), never the check, and lists each. Batch canon (D-0056), not the builder: the files that drive the S4 exit on a story
with a findings file — the builder Greps `critic-findings` in `P\scripts\tests\test_*.py` and lists in the report the files whose
fixtures also share a `covers:` id (candidates by the plan critic's count: `test_gate_preflight.py`, `test_story_run_gate_repair.py`,
`test_story_run_s6.py`, `test_exit_gate_digest_source.py`), without running the big ones.

**Mutations (named, not run — builder-rules 7b; each killed by `test_case_merges.py`):** M1 `merge_candidate_errors` returns before
`_owed_pair_errors` -> K1. M2 `covers(a) & covers(b)` -> `|` -> K1 clean case. M3 accept `approve` as a carried merge -> K4.
M4 a pair answered only by a two-id row -> K3. M5 budget `>` -> `>=` -> K8 (count == n). M6 drop the `Archived` filter -> K8.
M7 drop the KEEP_GROUNDS check -> K2. M8 only the newest round consulted for answers -> K5. M9 level order check removed -> K6.
M10 partner-id check after the token removed -> K4. M11 the truncation tail line dropped -> K3b.

**Changelog fragment** `P\changelog.d\release-next-1-tq1-27.md`: "The S4 case critic now answers every pair of cases that share a
requirement under `## Merge candidates` (merge or keep, with a P16/P19 reason). A merge changes no case: both cases are approved with
the concern `parametrise into one test: <ids>`, which reaches the S5 automator like any case-critic concern. The critic also states
the lower level an e2e or manual row could take, and explains a case count over the S3 plan's case budget. The S4 exit refuses a
round that leaves a pair unanswered or approves a merged case without that concern."

Commit line: `architecture: AR-10, AR-13, AR-21, AR-22, AR-23, AR-25, AR-28 -- requirement in card/charter/brief before the work; one reader each (case_status, _plan, rounds); merge carried whole as a concern, no new case state; case_budget reader wired, producer SC5-6 named; empty outcomes stated`.

## 5. Closure of the plan critic (t-715) and the Lead's lines

| Item | Closure |
|---|---|
| B-1 | APPLIED (Lead's route): no `Archived`, no merge->reject; a merge is a row + `approve_with_concerns` with `parametrise into one test: <ids>` carried to S5 (2.1.4d, charter 2b, card). F6's "OPEN ... not verified" removed (the critic verified it negative). The fold + delivery readers = queued node Q1. |
| B-2 | APPLIED: producer SC5-6 (`words-gates/1`); one name `case_budget`, one home `work/test-plan.json` (F4); reader `branch_accounting.case_budget`; `sizing.py` out of owns; the critic's line renamed `Over the case budget:` (one name per quantity). |
| (1) measured fact / m-1 | APPLIED: F2-A kept; no Given/When code (FR-12); node acceptance wording in §1; live-proof row = Lead line L3; K-CAL docstring says it does not find the merges. |
| (2) Archived downstream | APPLIED via B-1 (nothing archived; K-CAL asserts statuses unchanged). |
| (3) detector placement / D-0048 | NO CHANGE needed (critic: OK); RN1-2's pending `test_case_gates.py` edit -> fork F2. |
| (4) bytes / m-2 / m-3 | APPLIED: charter four cuts stand + fallback rule (insert grew under B-1); card fallback cut mandatory + `lower level:` mention + two more unpinned cuts (F3); Witness cut at 115-117; TQ1-2 note removed (already merged). |
| (5) waiver / m-5 | APPLIED: E11 narrowed to the literals `Merge candidates` / `lower level` / `Over the case budget`; K9 asserts it does not pass a roll-call refusal. |
| (6) builder material / m-4, m-6, m-7 | APPLIED: TS-10, TS-12, TS-14 tokens in K-CAL + the three merges pinned (carried concerns); owns add `test_case_gates.py`, `test_branch_accounting.py` (fixture-only); function lists on shared files; status via `contract.case_status`; covers reading named as `_requirements_of`'s; helpers split; `main` edit DROPPED; FR-13 home -> fork F1. |
| (7) Lead queue wording | APPLIED: lines L1 (Q1), L2 (SC5-6) below. |

**Lead lines (the Lead writes them; this designer writes only this file):**
- **L1 — queued node Q1** (one node; the designer twin + the fold): designer charter rule "one form, branches as parameters" + the
  designer-side merge execution (the absorbed case `status: Archived`, survivor carries its Thens/`covers`) TOGETHER with every
  delivery reader skipping `Archived`: `contract.case_files`/`case_index` (or each reader), `check_delivery._completeness`
  (:637-649, and :644 for a deleted case), gate A `controller.py:2625` row cases, with tests on each; paired cut in the designer
  charter. Chain "designer → critic на план → builder → critic"; ordered before any live proof that relies on folded cases. Pile:
  the next untaken batch of `release-next` (D-0044) — Lead's choice. Until Q1 lands, TQ1-27's merge stays the S5 concern.
- **L2 — SC5-6 amendment** (`words-gates/1`, not taken -> editable): "writes `case_budget` (int >= 1, cases) as a top-level key of
  `work/test-plan.json`; its readers use `branch_accounting.case_budget` (TQ1-27)". Noticed analog: `gate_brief.py:3455` already lists
  `case_budget` among the SYNONYMS of the requirements' weighted budget read from `work/sizing.json` (`_first(data, "computed_budget",
  "budget", "cases_budget", "case_budget", "weighted")`): SC5-6 must keep that word out of `sizing.json`, or drop it from that list —
  otherwise one word names two quantities. Not widened here.
- **L3 — live-proof row** in `batch-1-release-0-10-9.md` «Живые доказательства»: `| TQ1-27: критик кейсов S4 на копии 12586 (0.10.9)
  отвечает merge на TC-003/TC-002, TC-011/TC-001, TC-005/TC-004 и несёт «parametrise into one test:» в S5; TS-8/TS-9 — «lower level:
  component» | копия testproject1-dev-010, TP1-12586 | live-runs | ожидает |`. The batch is taken: if `piles.py check` refuses a new
  row there, the row goes as a finding to `live-runs` (D-0044).
- **L4 — noticed, not widened:** whether the S5 window cut keeps merge partners in one window is not verified (E21); a scout question
  for the Lead if wanted.

## 6. Forks (Lead decides; §2–§4 follow the recommendation)

- **F1 — home of `merge|keep`, `P16|P19` (FR-13, AR-1; m-7).** (A) module constants beside `CASE_CRITIC_VERDICTS`, pinned by
  `test_ahead_cards.VOCABULARIES` (precedent: `CASE_CRITIC_VERDICTS` itself is a code tuple); (B) glossary rows in
  `handoffs/vocabulary.yaml` (+1 owned file, +1 reader). **Recommend A** now, and one queued class item moving the case critic's
  closed words (verdicts included) to data together — moving two of five words alone splits the set.
- **F2 — order against RN1-2's `test_case_gates.py` edit (commit c0de6d15, not in this branch at review time; not re-checked here —
  no shell).** (A) merge `main` into the builder's worktree first if RN1-2 has landed by dispatch; otherwise the builder edits
  `test_case_gates.py` only in fixture rounds (expected none) and the later node resolves the merge (D-0048); (B) `очередь: RN1-2 →
  TQ1-27`. **Recommend A** (the edit is expected empty).
- **F3 — card cuts 4–5** (`, so the file has to carry the trail`; ` in those words`). The Lead's "fallback cut -> 1,174 B" was
  measured for t-697's add; the B-1 wording + `lower level:` + the renamed line make the add ~341 B. (A) both cuts (estimate ~1,183 B);
  (B) shorten the add instead (drop the level syntax from the card — FR-38 gap again). **Recommend A**; both unpinned (§7).
- **F4 — exact home of `case_budget` in "the S3 plan".** (A) top-level int key of `work/test-plan.json`, read through `_plan` (the
  plan's one reader; the JSON is what code reads); (B) a front-matter field of `test-plan.md` (a second reader of the plan). **Recommend
  A**; it binds SC5-6 by L2.

## 7. Small choices closed by the designer

- S1 Check lives in `critic_rollcall.py` (already the S4 critic's exit detector; `stages.json`), no new script.
- S2 Pairs unordered, ids sorted in refusal text; a pair is answered by any row whose id set holds both.
- S3 The budget line constant renamed `Over the case budget:` with the quantity (B-2, one name).
- S4 Count for the budget = live cases of the story (not only the review scope).
- S5 `rounds(text)` extracted into `critic_rollcall`, used by `_round_homes` too (removes a clone; dup ratchet).
- S6 Brief line for both S4 roles (`S4_STAND_ROLES`); "not set" printed when absent (t-697 behaviour kept).
- S7 Truncation at `branch_accounting.limit("refusal_units_shown")`, tail line in the `_stage_check` wording.
- S8 Notes printed as `note: ...` before the verdict line; they never change the exit code.
- S9 Token match case-insensitive with collapsed whitespace; ids after the token by `C.case_ids` (a superset is fine).
- S10 `approve_with_fixes` on a merged case is refused (concerns are carried only from `approve_with_concerns`, `_read_round`).

## 8. Reading trail (02.11.2026, this designer)

- Read whole: the plan critic `docs/tasks/specs/reviews/t-715-tq1-27-plan-critic.md`; the original spec
  `docs/tasks/specs/t-697-tq1-27-case-critic-merges.md`; `P\agents\qa-case-critic.md` (line refs 15-16, 37, 40-41, 54-55, 76, 115-117
  confirmed; TQ1-2 sentence present at line 65).
- `P\references\ahead-cards.json` line 40 (qa-case-critic card text: the five cut phrases present verbatim).
- `P\scripts\critic_rollcall.py` 1-250, 365-434, 520-604, 765-897 (constants, `parse_rollcall`, `_round_slice`, `_row_outcome`,
  `_receipt_round`, `carried_concerns`/`_read_round`/`accepted_rounds`, `findings_errors`, `_detector_body`, `main`).
- `P\scripts\s5_plan.py` 1095-1160 (`_case_critic_files`, `_file_concerns`: latest listing round decides; `case_concerns`); grep of
  `concern|remarks` there; `P\scripts\brief_pack.py` 1664-1691 (plan slice carries "the case critic's concerns"), 2427-2441, 2690-2725
  (`build` call site :2721), def list.
- `P\scripts\check_delivery.py` 610-654 (`_completeness`; `covers[]` of a test counts both cases, :626-629).
- `P\scripts\contract.py` 886 (`_FRONT_RE` takes a BOM), 939-946 (`front_line`), 2444-2449 (`read_text` utf-8), 3220-3245
  (`case_requirements`, `case_status`), `PLAN_LEVELS` 1788.
- `P\scripts\branch_accounting.py` 1253-1277 (`MANUAL_DISPOSITIONS`, `PLAN_EXCLUDING`, `_plan`), 1460-1625 (`_case_records`,
  `_round_homes`, `_scoped`, `s4_problems`, `critic_scope`, `_stage_check` truncation).
- `P\scripts\handoff_check.py` 339-352 (`_requirements_of`); `P\scripts\waiver.py` 150-244 (`split_overridden`: `names_whole`);
  `P\scripts\detector_verdict.py` 241-313 (`parse`: a non-`- ` line inside a block -> unmigrated).
- `P\scripts\tests\test_ahead_cards.py` 51, 60-97, 149-214 (cap 1,200 B measured on `text.encode`; VOCABULARIES substring check);
  `test_case_gates.py` def list (calls `findings_errors` only, no `detector_main`); `test_detector_unreadable.py` 15-73; test-file
  count of `critic_rollcall` (29 files).
- `P\handoffs\vocabulary.yaml` grep (glossary rows 70-77; `CRITIC_VERDICTS` generated).
- Fixture `...\run-12586-red-then\controller\TP1-12586\work\test-cases\**` grep of `^(plan_row|covers|status):` (five owed pairs
  re-derived by hand from `covers:`; TC-001/TC-004 `status: Automated`); `...\work\test-plan.json` lines 1-30 (a dict with `rows`).
- `R\plans\piles\words-gates\batch-1-slova-i-gejty.md` lines 1-8, 55 (SC5-6: status «ожидает», `case_budget` in the S3 plan);
  `R\plans\piles\release-next\batch-1-release-0-10-9.md` lines 1-14, 20-33, 60, 85-114 (TQ1-27 row; RN1-2 row; live-proof table
  empty; batch taken «в работе»); `R\DECISIONS.md` D-0048 heading.
- Negative claims with positive controls: "`case_budget`/`case_ceiling` nowhere in the package except gate_brief:3455" — Grep over P
  found that hit (control and finding in one call); "no test pins the card cut phrases" — Grep -i of the five phrases over P hit the
  card itself (control) and unrelated "in those words" in other files' own strings, none in `test_ahead_cards.py`.
- Not done (no shell): byte measurements (estimates marked; the builder measures); git state of c0de6d15 in this branch.

Needed beyond the manifest: `s5_plan.py` (the concern carrier B-1 rides on), `brief_pack.py`, `detector_verdict.py`,
`branch_accounting.py`, `gate_brief.py:3455`, `handoffs/vocabulary.yaml`, `test_detector_unreadable.py`.
