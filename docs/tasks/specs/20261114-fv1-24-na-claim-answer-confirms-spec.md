# N-a (FV1-24 family): a person's answer to a claim question confirms its requirements — DRAFT spec

task: t-763 (designer draft; owner away: forks carry a recommendation, none decided). Source of the defect: plan critic t-754,
`docs/tasks/specs/reviews/20261114-fv1-24-plan-critic.md` §0.2 L8, Key 5, Key 12. Code read: `.claude/worktrees/read-main`
(origin/main). Real story read (read only): `C:\QAFactory\mybooks-stand\arm-factory\test-automation-framework\qa-factory\artifacts\LOCAL-1`.

## 0. What the data says (read by me, carrier beside each line)

- R-8, R-10, R-11, R-12 are `derived`, `current-code:` observable, no `ac_ref`, matrix silent (register `created: 2026-11-12`,
  lines 21-25, 76-80) -> `code_sourced_requirements`; each has a `## Behaviour claims` row pointing to `Q5` (register :87-90).
- Q5 in `work/requirements-readiness.json` :125-154 carries `before {value: unknown}`, `now`, and two readings
  `{id, from: claim, reading, cost}` — NO `claim` key, NO `if_chosen`, and `sources_say` (a string) instead of `source_says`.
  Q1-Q6 all carry the same `{id, reading, cost}` / `sources_say` / `statement` shape.
- That shape is exactly the tester's HANDOFF form: `references/slices/qa-requirements-tester/handoff-keys.md:44-50`
  (`open_questions[].sources_say`, `readings[].reading`, `readings[].cost`). The readiness question form (`source_says`,
  `{reading, from, if_chosen}`, `claim`) lives only in `references/artifact-contract-json.md:133-147`, which the tester is not
  injected (`references/inject-map.json:28-35`; slice index `references/slices/qa-requirements-tester/index.md`).
  The tester's slice says only "Its readings are the fixed pair, both `from: claim`" (`.../artifact-contract.md:60-61`).
- `question-answers.jsonl` line 4: Q5 `answered`, `reading: a`, `row_hash 7312c4...`, at S3 stop. Line 20: the applier wrote
  `not_applied: before_value_missing` for Q5 (`planning_contract._apply_recorded` :3593-3598 — `QR.settled(Q5)` is False because
  `contract.before_value_needed` :1788-1810 returns True for ANY letter of an unmarked question whose `before` is `unknown`).
  `state/words/driver-shownA-*.txt` (two files) list Q5 with the SAME row hash 7312c4... (shown again; the file family name
  suggests gate A — not verified, §9).
- Q8 / Q9 / Q17 ARE marked (`claim: now|before`, readiness :222-235 for Q8), answered `a`, `raised_for {case, then}`.
  Their Thens' oracles are `{"source": "unknown", "ref": "Q8"}` / `"Q9"` / `"Q17"` (TC-001.md:14, TC-008.md:14) —
  NOT `{source: requirement, ref: R-n}`. The only R in Q8 is in its `source_says` prose "(R-8, derived)".
- The recorded fixture story `scripts/tests/fixtures/stories/local-1-arm-b` (another LOCAL-1 run, 0.10.9) has the correct
  shape: its claim question Q4 (`work/requirements-readiness.json` :126-159, `open_questions[3]`) carries `claim: now` /
  `claim: before` and `if_chosen`. So the role CAN write it; nothing makes it.

### Premise measurement (PROJECT.md package change 6 (a)) — ONE command

I have no shell in this role, so the command is written for the Lead to run (a pure read; hygiene pt.4 b) on a byte copy of
the story (`Copy-Item -Recurse <LOCAL-1> <scratch>\LOCAL-1`), and its output goes into this section at acceptance:

```
python -B -c "import sys;sys.path.insert(0,r'C:\QAFactory\forge-repo\.claude\worktrees\read-main\ai-packages\qa-factory\scripts');import contract as C,question_register as QR;t=r'<scratch>\LOCAL-1';v={q['id']:q for q in QR.load(t)['questions']};reg=open(t+r'\work\requirements-register.md',encoding='utf-8').read();print(sorted(C.unconfirmed_requirements(reg,v)));print({q:(v[q]['status'],v[q]['reading'],v[q]['changed_since_answer'],C.claim_confirmed(v[q]),C.before_value_needed(v[q]),bool(C.claim_mark_problem(v[q])),QR.settled(v[q]),C.claim_row_errors({'r':'R-8','before':'unknown','before_ref':'absent','now':'x','now_ref':'current-code:a:1','differs':'unknown','question':q},v)) for q in ('Q5','Q8','Q9','Q17')})"
```

Expected, from the code read and from critic t-754's own probe (§0.2 :35, :72): `['R-10','R-11','R-12','R-8']`; Q5
`('answered','a',False,False,True,True,False,[])` — the last `[]` is the defect: today the register validator accepts Q5.
Q8/Q9/Q17: `claim_confirmed` True, `claim_mark_problem` False. NOT RUN BY ME (estimate, not verified).

## 1. AR-n touched, owners and census classes

| AR | how it is kept |
|---|---|
| AR-10 (a check's requirement reaches the role before the work, in its fields) | the `claim` key is put into the tester's injected slice (card A) before the S2 exit starts refusing it (card B); A lands with or before B |
| AR-9 (refusal names what it expected and a door) | the new line names the question, the field `claim`, the two words, and that the tester rewrites the question (card B); the rehearsal line names the tester and the waiver door (card C, existing text) |
| AR-13 (one reader) | `contract.claim_confirmed` / `_confirmed_claims` / `unconfirmed_requirements` are NOT changed; no second "is R-n confirmed" function (item 4) |
| AR-15 (one survivor) | the mark check is `contract.claim_mark_problem` (exists); card B calls it from the one claim-row judge `claim_row_errors`, which `validate_artifacts.check_behaviour_claims`, `exit_gate.collect_errors` and both `claim_projector` sites already call |
| AR-22 (every field read has a producer) | `claim` is read by `claim_reading_index`; its role producer now is told it (A) and refused without it (B) |
| AR-28 / FR-59 (an unknown never becomes a pass) | an unmarked question stays "confirms nothing" (reader untouched) AND is now refused at the write instead of passing silently |
| AR-12 (friction) | cost to the role: two words per claim question; a refusal only on a question the role wrote unmarked |
| AR-24 (a person's words reach what acts on them) | the in-flight road (card C) gets the answer re-given on a marked question, so it reaches `_confirmed_claims` |
| AR-29 / P27 | no meaning moves to code: code checks presence and form of two marks; whether the mark matches the reading text is the S2 case critic's judgment |

Checks added or altered (owner; census class, `scripts/tests/fixtures/judgment-census.json`):
- `contract.claim_row_errors` — gains one line (mark present). Owner: DATA (code). Class `shape` (row :165, unchanged; no new unit).
- `gate_preflight.check_open_questions` — the existing mark line now also fires for a question a `## Behaviour claims` row
  points to. Owner: DATA. Class `shape` (row :413, unchanged; no new unit).
- `validate_artifacts.check_behaviour_claims` — unchanged code; its census row (:1187, `meaning-proxy`, judgment) unchanged.
- The mark-vs-text fit (did the role mark the "intended" reading `now`): JUDGMENT, the S2 `qa-case-critic`, accepted by the tier
  above. No code reads reading wording (FR-12).
`judgment:` line for the commit: `adds data check contract.claim_row_errors (claim marks)`; census unchanged (no new unit) —
`test_judgment_census.py` is slow (`slow_tests.json:63`): judged by the batch canon.

FR walk (sections touched): A (refusal names door: FR-1, FR-2, FR-57), C (FR-11, FR-38: the role is told the field the check
reads), D (FR-58/FR-59: safe reader kept), B (FR-7: no re-ask with the same text — card C re-asks only on changed text).
E/F/G: not touched beyond FR-30 (English) and FR-32 (root cause, with a test).

## 2. Items of the brief -> cards

| brief item | outcome |
|---|---|
| 1 (a) tester told `claim` in the slice | card A |
| 1 (b) unmarked claim question refused where the role writes it | card B |
| 2 in-flight Q5 shape, both worlds | card C (recommended road, fork F-2) |
| 3 per-Then confirmed questions confirm their R | NOT BUILT — not the same fact, and the data link does not exist (§5; fork F-3) |
| 4 one reader stays one | kept: no card touches the reader (§1 AR-13) |

The Lead's direction holds against the code with one correction: the "earliest code that already validates the question row"
is `contract.claim_row_errors` (called by `validate_artifacts.check_behaviour_claims` at the register write and re-run by
`exit_gate.collect_errors` at the S2 stop, :1330-1338), not `before_now_errors` (which every question goes through and which
has no reason to know the claim rows).

## 3. Cards (for a Sonnet builder; one worktree `C:\QAFactory\forge-repo\.claude\worktrees\fv1-24-na`)

Common `given:` for every card: `ai-packages/qa-factory/design/factory-rules.md` (whole), `plans/builder-rules.md`, this spec,
`docs/TESTING.md`, `ai-packages/qa-factory/scripts/tests/test-layers.json`, `ai-packages/qa-factory/scripts/slow_tests.json`.

### Card A — the tester is told the mark (item 1 a)

- File/section: `references/artifact-contract.md`, section "`## Behaviour claims` of the register" (:168 area, the sentence
  "Its readings are the fixed pair, both `from: claim`"). Extend the sentence, keeping the anchor words "Its readings are the
  fixed pair" byte for byte: each reading carries `claim: now` (the behaviour now is the expected one) or `claim: before`
  (a regression), once each, in any order; a question without them is refused at the S2 stop and the person's answer to it
  confirms nothing. Then regenerate: `python -B scripts/contract_slices.py --write` (the slice
  `references/slices/qa-requirements-tester/artifact-contract.md` and any other role whose slice carries the section change
  with it; never hand-edit a slice) and `--check` green.
- `design/role-rules.json`: one new row `tester-claim-question-marks-now-before`, anchor `` `claim: now` `` in both carriers of
  the existing row :342 (whole-source and slice). The existing row stays.
- Edges: (E-A1) the slice grows -> `references/role-load.json` token figures for `qa-requirements-tester` may move; if a ceiling
  in `role_load.py` refuses, the builder STOPS and returns the number (a raise is named, AR-20/axis 18), never trims other rule
  text to fit. Invariant: no rule text leaves a role to make room. (E-A2) the anchor of row :342 must still be found in both
  carriers (`test_role_rules.py`, keep). Invariant: an accepted role rule is never lost by an edit.
- Non-goals: the handoff form (`handoffs/*.yaml`, `handoff-keys.md`) — fork F-4; `artifact-contract-json.md` (already says it).
- DoD: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for references/artifact-contract.md
  references/slices/qa-requirements-tester/artifact-contract.md design/role-rules.json` and every file it prints that is not
  in `slow_tests.json`; plus `python -B ai-packages/qa-factory/scripts/contract_slices.py --check`.

### Card B — the S2 write refuses an unmarked claim question (item 1 b)

- File/function: `scripts/contract.py` `claim_row_errors` (:1466-1513). In the branch where the question exists and
  `before_now_errors(question)` is empty and `"before" in question` (today the `else:` at :1511), BEFORE the link errors,
  append `f"question {qid} {claim_mark_problem(question)}"` when `claim_mark_problem(question)` is non-empty; then the link
  errors as today.
- `claim_mark_problem` (:869-878) text: keep "claim: now|before" and the opening clause; replace the tail "the case's texts
  cannot be tied to a reading without it" with "without it neither the person's answer nor a case's texts can be tied to a
  reading - qa-requirements-tester rewrites the question". (Rehearsal test K9 checks only `claim: now|before`.)
- POSITIONAL invariant: a missing question, or a question whose before/now pair is malformed, keeps its ONE existing line
  (no second line about marks on a question that already fails); the mark line never replaces the link line; the code's own
  pair (`claim_readings` texts, `claim_reading_index` case (ii)) and every question built by `claim_question` /
  `claim_projector` stay accepted (they are marked or equal to the code pair).
- Error direction (a reused function, advice -> gate): `claim_mark_problem` was a rehearsal advice; it now gates the S2 stop.
  It may err only toward REFUSING. Adversarial inputs that must stay refused: one reading marked, the other not; both `now`;
  `claim: "Now"` / `" now"` / `"current"` / `1` / `null` / `["now"]`; three readings marked now/before/now; readings absent
  or not a list on a question with before/now. Must stay accepted: marked reversed (`before` first) — the reader handles it;
  the code pair unmarked with byte-equal texts. A question that shows before/now on NO claim row is not judged here (it is
  the rehearsal's, card C).
- TEMPORAL: the check exists only after this commit. Before: an unmarked claim question passes the S2 stop (today's LOCAL-1).
  After: a NEW S2 stop refuses it. A story in flight past S2: `exit_gate.scoped_errors` hands register errors only to the stop
  of the stage that lists the file (S2) (:1421-1434), so S3..S9 stops are NOT newly refused; an S2 re-dispatch of such a story
  (e.g. card C's question packet) IS refused until the question is marked — that is the intended door. Dating it by the
  register's `created`: fork F-1 (recommended: undated).
- One question serving several claim rows (Q5 -> 4 rows): one line per row, as every claim-row line today. Invariant: the
  line names the R and the question, so the role sees one question to fix.
- Test (TESTING.md: role-written input from outside -> scenario variant rows; no new test file): create
  `scripts/tests/fixtures/stories/local-1-arm-b/variants.json` (the first `variants.json` in the repo; shape by
  `scenario_walk._walk_variants` :781-808 and `apply_op` :225-251): rows on `stage: "S2"` (door `exit_gate`), `file:
  "work/requirements-readiness.json"`, `op: "set"`, `pointer: "/open_questions/3/readings"` (Q4), value = the two readings
  with: (v1) no `claim` keys at all (the LOCAL-1 Q5 shape); (v2) only the first marked; (v3) both `now`; (v4) `claim: "Now"`;
  (v5) three readings. Each `expect: {"outcome": "refused", "names": "claim: now|before"}`. Control (v6): `stage: "S4"`, same
  v1 value, `expect: {"outcome": "accepted"}` — the TEMPORAL invariant that a later stop is not newly refused. NOTE: the S2
  door of this story is ALREADY refused for an unrelated recorded reason (`story.json` `not_walked` :70-75, owner_role), which
  is why S2 rows assert `names`, never `accepted`. If `story_cut(entry, "variant")` needs a `variant` key in the S2/S4
  `cut_before_seq`, the builder adds it in `story.json` (fixture data) and says so. If v6 is refused for a reason not caused by
  the variant, the builder returns it as a question, never changes the expectation.
- Non-goals: the reader (`claim_confirmed`, `_confirmed_claims`, `unconfirmed_requirements`, `before_value_needed`) — unchanged;
  any quarantined file (`test_question_thens_claim_keys.py`, `test_d1_gate_words.py`, `test_claim_projector.py`,
  `test_contract.py` are in `test-layers.json` `quarantine`, cohort 8073673); K10 there stays true as written.
- DoD: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for scripts/contract.py
  scripts/tests/fixtures/stories/local-1-arm-b/variants.json` and every printed file not in `slow_tests.json`;
  `test_scenario_local_1_arm_b.py` IS in `slow_tests.json` (:120, 22.8 s) — under 60 s, so the builder runs it as its own
  witness (builder-rules 7b: a narrow witness up to a minute) and pastes the variant lines; the rest "judged by the batch canon".

### Card C — the in-flight Q5 shape (item 2; recommended road of fork F-2)

- Both worlds. BEFORE: an answered unmarked claim question is not `settled` (`before_value_needed`), the applier writes
  `before_value_missing`, the gate card shows `gate_brief.unmarked_value_note` ("you chose a: ...; ... say what the behaviour
  before was") — a request that makes no sense to a person who chose "now" — and every reader keeps R-8..R-12 unconfirmed.
  AFTER: the gate A rehearsal sends that question to the tester for a re-mark; the rewritten row has a new hash, so the old
  answer stops holding (`changed_since_answer` True) and the card asks it again saying "its text changed after your answer"
  (`gate_brief.question_note` :4317-4318); the person answers once on the marked text; `claim_confirmed` then holds.
- File/function: `scripts/gate_preflight.py` `check_open_questions` (:1993-2015). Today the mark line is added only when a case
  keys texts by meaning on the question (`qid in keyed`). Add a second condition read once per call: `qid` is a value of
  `contract.claim_questions(register)` (the register text is already read at :1962 for `norm_ids`; reuse it; unreadable ->
  the existing note, and only the `keyed` condition applies — FR-59 toward the existing behaviour, never a crash).
- POSITIONAL invariant: the new condition sits where `keyed` is tested, AFTER the skips for `row_answered`, `settled` and
  `hidden_repeat` (:1994-1999). A SETTLED question is never sent back (a marked, answered Q stays answered); only an
  unsettled one — which an unmarked answered claim question is — reaches the line. The finding stays `FACTORY_FIXABLE`, to
  `qa-requirements-tester`, with the existing waiver door.
- FR-7: the person is asked again only on CHANGED text (the re-mark changes the row bytes); the same text is never re-shown
  as a new question. Cost: one re-answer per such question (fork F-2 states the alternative).
- TEMPORAL: a story already PAST gate A (LOCAL-1 is at S7/S8) does not run the rehearsal again: its Q5 stays unconfirmed — the
  safe side — and nobody re-asks it. That residual is named for node N-b (the second question road) and must not be "closed"
  by FV1-24 K2 re-asking the R through the findings road (critic Key 5). Recorded in §8.
- Test: one row in `scripts/tests/test_gate_preflight_question_status.py` (keep, `data_join`, covers gate_preflight +
  question_register; not slow): a story with a claim row -> Q unmarked, before `unknown`, answered `a` -> one finding naming
  the question and `claim: now|before`; the same with the readings marked -> no finding (it is settled). No new file.
- Hot file: `gate_preflight.py` is on PROJECT.md «Командная работа» п.3 list -> a queue line or a disjoint function list in
  `owns` (this card owns `check_open_questions` only).
- DoD: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for scripts/gate_preflight.py` plus
  `python -B ai-packages/qa-factory/scripts/tests/test_gate_preflight_question_status.py`; `test_gate_preflight.py` is slow
  (`slow_tests.json:41`): "judged by the batch canon".

### Manifest header (one builder dispatch, three cards in order A, B, C)

given: the common list above; `docs/tasks/specs/reviews/20261114-fv1-24-plan-critic.md` §0.2, Key 5
owns:
C:\QAFactory\forge-repo\.claude\worktrees\fv1-24-na\ai-packages\qa-factory\references\artifact-contract.md
C:\QAFactory\forge-repo\.claude\worktrees\fv1-24-na\ai-packages\qa-factory\references\slices\qa-requirements-tester\artifact-contract.md
C:\QAFactory\forge-repo\.claude\worktrees\fv1-24-na\ai-packages\qa-factory\references\slices\
C:\QAFactory\forge-repo\.claude\worktrees\fv1-24-na\ai-packages\qa-factory\design\role-rules.json
C:\QAFactory\forge-repo\.claude\worktrees\fv1-24-na\ai-packages\qa-factory\references\role-load.json
C:\QAFactory\forge-repo\.claude\worktrees\fv1-24-na\ai-packages\qa-factory\scripts\contract.py (claim_row_errors, claim_mark_problem)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-24-na\ai-packages\qa-factory\scripts\gate_preflight.py (check_open_questions)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-24-na\ai-packages\qa-factory\scripts\tests\fixtures\stories\local-1-arm-b\variants.json
C:\QAFactory\forge-repo\.claude\worktrees\fv1-24-na\ai-packages\qa-factory\scripts\tests\fixtures\stories\local-1-arm-b\story.json
C:\QAFactory\forge-repo\.claude\worktrees\fv1-24-na\ai-packages\qa-factory\scripts\tests\test_gate_preflight_question_status.py
C:\QAFactory\forge-repo\.claude\worktrees\fv1-24-na\ai-packages\qa-factory\changelog.d\fv1-24-na.md
non-goals: the reader functions of item 4; per-Then confirmation (item 3); the handoff form (F-4); any quarantined test; CI
edges: E-A1, E-A2; card B POSITIONAL, error direction, adversarial list, TEMPORAL, shared question; card C both worlds, POSITIONAL, FR-7, TEMPORAL past gate A
DoD: the three `scenario_walk.py --witness-for` runs above plus `contract_slices.py --check`, `test_scenario_local_1_arm_b.py`, `test_gate_preflight_question_status.py`
siblings: §6 enumeration; analogs F-4 (readiness question form), §8
designer: <this file, once accepted>
handoff: builder report per `.claude/agents/builder.md` rule 7, FR walk, the witness output verbatim

`references/slices/` is in `owns` because `contract_slices.py --write` may re-render other roles' slices of the same section;
the builder lists exactly which files changed.

## 4. Edges common to the cards (with invariants)

- Empty/absent: no `## Behaviour claims` section -> `claim_row_errors` is not called; no readiness file -> `questions` None ->
  no question checks (today's E-B8, unchanged). Invariant: card B adds no refusal where there is no question to judge.
- A claim row naming a question with no before/now -> the existing single line (POSITIONAL above).
- Conflicting requirements: card B refuses at S2 what card C sends back to S2 — they agree (C's door is B's demand).
- Card A must land in the same commit as or before B (AR-10). Invariant: no role is refused for a field it was never told.

## 5. Item 3 — why it is not built (the honest answer: not the same fact)

- No data link: the Thens of Q8/Q9/Q17 have oracle `source: unknown, ref: Qn` (TC-001.md:14, TC-008.md:14). Under
  `unconfirmed_requirements`' own rule ("a Then resting on such an R reads `unknown` with the claim's question", contract.py
  :1446-1447) that is by design: there is NO `requirement` ref to follow. The only R is in prose (`source_says`), and reading
  it would be a phrase reading (FR-12); `named_r_ids` on question text is structural but names whatever the text mentions.
- Different fact: Q8 confirms one Then's expected value ("integer 1..999 accepted, else refused"); R-8 also says "changes
  nothing". Q9 covers part of R-11; Q17 a product-page subset. Lifting R-8 to confirmed on Q8 would confirm text the person
  never saw — the error direction of `claim_confirmed` is toward unconfirmed (:1344-1347), so this is refused.
- Nothing is lost: each per-Then answer already settles its own Then through `resolve_then_oracle` / `question_then_text`;
  R-level confirmation comes from the claim question once it is marked (cards B, C).
- Adversarial inputs that would have broken a mapping (recorded for whoever reopens it): a Then with several refs; a question
  answered then changed (`changed_since_answer` True); a case edited after the answer (the Then number moves); a Then whose
  oracle source is not `requirement` (all three measured ones).

## 6. SIBLING_MAP axes (origin/main, 37 axes) — one mechanism: "a claim question's marks are told and required at the write"

axis 1: n/a — no policy/role-file/journal change in this deployment. axis 2: n/a — no exam instrument. axis 3: covered —
package change reaches release via the normal copy; changelog fragment `changelog.d/fv1-24-na.md`. axis 4: covered — FR-38/
FR-11 instance closed by fix; no debt row. axis 5: covered — stage twins: the claim row has two writers (S2 role, S3
`claim_projector`); the projector's questions are code-built and marked (card B keeps them accepted). axis 6: n/a. axis 7: n/a.
axis 8: n/a. axis 9: n/a. axis 10: n/a. axis 11: n/a. axis 12: covered — node goes into a pile batch, not BACKLOG. axis 13:
n/a. axis 14: n/a. axis 15: n/a. axis 16: n/a. axis 17: n/a — refusal lines keep the existing shape. axis 18: covered —
role-load ceiling raise, if any, is named (E-A1); census unchanged. axis 19: n/a. axis 20: n/a. axis 21: n/a — the register
table is read by the existing readers. axis 22: n/a. axis 23: n/a. axis 24: n/a. axis 25: n/a. axis 26: n/a. axis 27: n/a.
axis 28: queued — the analog "where a role is told the fields of its row" for the READINESS question form (handoff form says
`reading/cost`, contract says `reading/from/if_chosen/claim`): fork F-4, node N-a2. axis 29: n/a. axis 30: n/a. axis 31:
covered — one owner of the readiness question form text (`artifact-contract-json.md`), the slice is a machine copy of
`artifact-contract.md`'s section; F-4 names the second carrier that contradicts it. axis 32: covered — §1 owners/classes, no
new unit. axis 33: n/a. axis 34: covered — one road: every claim question (S2 role, S3 projector, S4 raise) must carry the
marks or be the code pair; no language/project branch. axis 35: n/a. axis 36: n/a. axis 37: n/a — no repeat stop.

Sweep of the artifact (`claim_row_errors` and its neighbours in contract.py): `before_now_errors` — not applicable (every
question, knows no claim row); `question_errors` — not applicable (shape of any question; the S2 role's readiness form
defects are F-4); `_claim_link_errors` — not applicable (link, not marks); `claim_question` — already marked by construction;
`grounding_row_question` — not a before/now question (no `before`), never judged by the mark rule.

## 7. Four questions (rule 10)

(a) Cost: the tester writes two words per claim question; a refused S2 stop costs one rewrite; an in-flight story pays one
re-answer per unmarked answered claim question (card C). (b) Axes: §6. (c) Detector: the scenario variants v1-v6 (refusal and
the not-newly-refused later stop) and the `test_gate_preflight_question_status.py` row; the live leak detector is the
critic's §0.2-style probe — a claim question answered `a` whose Rs stay in `unconfirmed_requirements` (calibration check 41
reads census/judgment; no new check id proposed). (d) On the path: `validate_artifacts.check_behaviour_claims` at the register
write and `exit_gate.collect_errors` at every S2 stop (code-gated); gate A rehearsal for the in-flight world.

## 8. Overlap, queue, residuals

- wip/tbw-t1r and wip/tbw-t3a edit `references/role-load.json` and role slices (critic t-754 Key 10). Card A writes
  `role-load.json` (if figures move) and re-renders slices. Queue line: `очередь: tbw-t1r → tbw-t3a → fv1-24-na` for
  `role-load.json`, or fv1-24-na merges main and re-runs `contract_slices.py --write` after them (the late node resolves).
- `gate_preflight.py` (hot): card C owns `check_open_questions` only; the A2 node of the FV1-24 plan
  (`check_bug_drafts`) is a disjoint function — the D-0048 function-list form applies.
- Residual (node N-b, not this node): a story past gate A keeps Q5 unconfirmed with no road to re-ask it; FV1-24 K2's door
  must name the existing claim question, not mint a new requirement_silent place (critic A9).
- Analogs noticed, not widened: (1) the tester's handoff form `reading/cost`/`sources_say`/`statement` vs the readiness
  contract `reading/from/if_chosen`/`source_says` — Q1-Q6 of LOCAL-1 all fail `question_errors` today and pass only because
  nothing checks the readiness questions before gate A (F-4). (2) `gate_brief.unmarked_value_note` asks "say what the
  behaviour before was" of a person who chose a reading the question does not mark — wrong ask for "now"; after card C it is
  reached only when the rehearsal finding is waived. (3) Q4 (`norms_list`, answered `a`) names R-7, R-10, R-11, R-12; a norm
  confirmation is not a behaviour-now confirmation — not mapped (F-5).

## Forks (decisions for the Lead; recommendation first)

- F-1 Card B dated or undated. (a) RECOMMENDED undated: only an S2 stop sees it (scoped_errors), and its door exists; dating
  would keep the silent loss alive in every story created before the cut. (b) dated by register `created` (house pattern
  `UNCONFIRMED_SOURCE_CUTOFF`): no old story is touched, the false negative stays there.
- F-2 In-flight road. (a) RECOMMENDED: rehearsal -> tester re-mark -> one re-ask on changed text (card C; existing seam, form
  and FR-7-legal; costs the person one answer). (b) a hash-bound "mark" record in `question-answers.jsonl` (like the FV1-9
  `note`: measured on the row's bytes, a mark on other bytes never counts) written by the conductor after reading the
  readings — no re-ask, but a new record kind and a judgment that can flip the meaning of a given answer (a wrong mark turns
  "now" into "before"); must refuse any mark that differs from one already standing. (c) nothing: in-flight stories keep the
  safe false negative.
- F-3 Item 3. (a) RECOMMENDED not built (§5). (b) a structural link: the S4 raise writes `raised_for.requirement` (the field
  `gate_brief.requirement_help` already reads) and `_confirmed_claims` counts a claim-confirmed per-Then question for that R
  only when the case's Then text set covers the whole R — not checkable by code (meaning), so it would need a role verdict.
- F-4 The readiness question form reaches the tester (axis 28 analog). (a) RECOMMENDED a separate node N-a2: one form for
  `open_questions` in the handoff yaml and the readiness file (`handoffs/*.yaml` -> generated `handoff-keys.md`), with the
  readiness section of `artifact-contract-json.md` marked for the tester's slice. (b) fold into card A (wider diff, touches the
  handoff contract all S2 runs use).
- F-5 Norms-list answers as confirmation. (a) RECOMMENDED leave: different question ("the norm holds" vs "the behaviour now is
  intended"). (b) count a `norms_list` answer `a` as confirming its named norm rows' claims — a meaning change for every reader.

## Small choices I closed

- The mark line goes in `claim_row_errors`, not `check_behaviour_claims` (one judge for both writers and the projector check).
- One line per claim row (existing pattern), no de-duplication per question.
- Test homes: `local-1-arm-b/variants.json` (scenario layer, role-written input) and the keep file
  `test_gate_preflight_question_status.py`; no row in slow `test_gate_preflight.py`; nothing in quarantined files.
- Worktree name `fv1-24-na`; changelog fragment name `fv1-24-na.md`.

## 9. What I did NOT establish

- The premise command was not run by me (no shell): §0 numbers are code-read plus critic t-754's probe.
- That `driver-shownA-*` means "shown at gate A", and whether gate A on LOCAL-1 raised a rehearsal finding for Q5 (Q5 fails
  `question_errors` too: no `source_says`, no `if_chosen`).
- Whether `story_cut(entry, "variant")` needs a `variant` key in local-1-arm-b's `cut_before_seq`, and whether the S4 door
  stays accepted with a modified readiness file (v6) — the builder's first run tells.
- Whether `contract_slices.py --write` re-renders slices of roles other than the tester for that section.
- Whether a gate B (or later) rehearsal re-checks open questions (decides how big the N-b residual is).
- The exact `role_load.py` ceiling margin of `qa-requirements-tester`.

## Reading trail

critic review §0.2/Key 5/9/10/11/12 (:30-99, :147-168, :220-246, :262-272); contract.py :560-663, :690-878, :1097-1105,
:1186-1219, :1307-1513, :1555-1596, :1788-1811; question_register.py :174-181, :286-391, :434-509; planning_contract.py
:3477-3485, :3530-3610; gate_brief.py :4230-4244, :4289-4328; gate_preflight.py :1940-2031; validate_artifacts.py :690-718;
exit_gate.py :1276-1354, :1421-1434; claim_projector.py :1-200, :600-629, :815-862; place_answers.py :110-127;
references: slices/qa-requirements-tester/{index,artifact-contract,handoff-keys}.md, artifact-contract-json.md :120-147,
inject-map.json :28-35, role-rules.json :342; contract_slices.py :1-130; tests: test-layers.json (keep :36-7113, quarantine
:7168-), slow_tests.json, scenario_walk.py :1-60, :209-268, :781-890, test_scenario_local_1_arm_b.py, local-1-arm-b
story.json :1-138, README.txt (head), work/requirements-readiness.json Q4, work/requirements-register.md :100-108;
test_question_thens_claim_keys.py K9/K10 (:269-330, quarantined); judgment-census.json :165, :413, :1187; SIBLING_MAP.md axis
list, axes 28, 31, 32, 34; docs/TESTING.md :20-124; LOCAL-1: requirements-register.md :1-95, requirements-readiness.json
:1-260, question-answers.jsonl (all 34 lines), state/words grep Q5, test-cases/cart TC-001.md/TC-008.md front matter, S2
handoff yaml grep.
Negative claims and their controls: "no variants.json exists" — Glob `**/variants.json` empty, control `**/story.json` in the
same folder found 4; "the tester slice never names `claim`" — Grep `if_chosen|cost|sources_say|source_says` over the slice
folder hit only handoff-keys.md:48 (control: the same call found that line), and the `claim: now` grep over references/ hit no
tester slice file while hitting case-designer/critic slices.
