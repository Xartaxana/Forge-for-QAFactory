# P1-b walker: how a gate key row is judged (draft builder card, t-1045, designer)

Status: DRAFT for Lead acceptance. Base: branch `worktree-agent-a4aebd95c3ca7d59c` head 11494798 (tree
`C:/QAFactory/forge-repo/.claude/worktrees/agent-a4aebd95c3ca7d59c`); every file:line below was read in THAT tree this round
(prefix `T/` = `<tree>/ai-packages/qa-factory/scripts/tests/`, `S/` = `<tree>/ai-packages/qa-factory/scripts/`,
`R/` = `<tree>/ai-packages/qa-factory/references/`). The owns below are written as main-checkout paths; the Lead names the
tree the builder works in (the gates batch branch).

## 0. Chosen option and why (fork F-1, recommendation)

**(b) drive each row on to the gate's priced question (the seam question), plus one ask-identity rule for every key row.**
Measured against the Lead's three constraints:

| constraint | (a) judge vs `question-prices.json` | (b) drive to the seam question (chosen) | (c) `live_only` |
|---|---|---|---|
| P20/FR-58: expectation from data, observation from the driver | fails for K15 and C2: at a plain gate ask the driver offers nothing and prices nothing (`S/driver_gates.py:322` raises a bare `Person`; `S/driver_dialog.py:321` writes `offered` only `if person.offered`), so the "offered set" would come from the same data file as the expectation and could only pass | holds: K15/C2 compare the `gate_A` data rows with the driver's own ask record (`asked.offered`) and with the spy record the driver wrote while raising THAT ask | holds trivially (nothing judged) |
| P31 one road for `gate_A`, `gate_B`, gate key rows of s5, s6-s9 | one road, but a false one | one seed step form (`say`) and one identity rule, data rows per group | one road of not walking |
| judge reads the record of the ask it judges | does not address it | the ask ordinal (section 2) | n/a |

Why (b) is also the honest semantics: `rework / approve / retry / stop` are the answers of the price key `gate_A`
(`R/question-prices.json:143-148`), and the only question that offers them to a person is the seam question at a gate
(`S/driver_conductor.py:504-527`, priced at `:523`, or the conductor's own options priced in its prompt `:686` -> `:783` ->
`S/driver_runner.py:1285`). At the plain ask the only closed word is the approval word (`R/gate-approval-words.json:3-4`,
named in the packet `S/driver_gates.py:136-141`); every other answer, `rework`/`retry`/`stop` included, is words that go to the
conductor (`S/driver_machine.py:3586-3588`, `:3606-3607`, `:4115-4121`). A key row of `gate_A` therefore judges the priced
question of `gate_A`, the same meaning every other key row has. The plain-ask road (words -> the gate's priced choices) is
proven by the seed of every gate row: a seed that does not reach a question with offered answers is a FAIL (`T/dry_exits.py:1414-1415`).
The plain-ask approval-word road stays walked by the main pass (`T/fixtures/stories/dry-1/story.json:85` answers `gate_A: approve`).

## 1. Architecture, FR, census (test layer only)

- Touches only `scripts/tests/` (walker, stub, spy, fixtures). No package behaviour, no text a person reads.
- AR-n touched, each kept, with the change check in the DoD:
  - AR-22 (every field read has a producer): new spy field `q` -> producer `dry_driver.passing_spy`, reader `dry_world`
    ask window; one commit. DoD: the spy table row in `dry_stub.py` shows `q`.
  - AR-28 (an unknown never becomes a pass): no record / no ordinal / an empty offered set is FAIL; a declared n/a over a
    priced ask is FAIL. DoD: the judge table rows of section 6.
  - AR-13 (a fact with a reader function is read only through it): question rows are counted by the spy through
    `driver_journal.question_rows` (`S/driver_journal.py:396-399`), prices through `dry_exits.scan_prices`.
  - AR-20 (ratchets shrink): no reach changes unless the rework probe fails (section 7). DoD: `dry_exits.py --check` = 0 discrepancies.
  - AR-29 (code judges data): every check below is data vs a driver record; no role judgment is judged.
- Checks added or altered, owner served, census class: K15 (altered: the ask's own records) - data (code), xref; C2 (altered:
  offered set from the ask's own record) - data (code), xref; `n/a` guard (new) - data (code), shape; `say` seed step - not a
  check (walker grammar). No role and no person owns any of them. Whether `scripts/tests/fixtures/judgment-census.json` scans
  `scripts/tests/` was NOT read: the builder reports what `scenario_walk.py --witness-for` prints for it.
- Commit lines: `architecture:` and `judgment:` in the form `tools/architecture_gate.py` defines (read it; the grammar is not
  copied here). Expected content: AR-22, AR-28 kept as above; `judgment: none` with its ` -- <why>` (test-layer data checks only).
- FR: C-11/C-14 (the spy's output shape is a contract: the new field is documented in its docstring); D-59 (unknown never a
  pass); G-30 (fixtures ASCII). A-F otherwise: test layer, not applicable.

## 2. The ask identity (applies to every key row in every group)

Today `facts["priced_at_ask"] = priced[-1]` (`T/dry_world.py:1243-1244`) and `_holds` reads `priced[-1]` (`:1153-1154`): the
LAST spy record, whatever ask it belonged to. At the S4 snapshot that is `s1.review`'s record (report quote:
`K15: key not observed: expected gate_A, observed s1.review`).

Rule (invariant: **a price record written for another ask never counts for this one**):
1. The spy stamps each record with `q` = the number of rows `driver_journal.question_rows(task_root)` returns at the moment of
   the call (`T/dry_driver.py:44-52`; record becomes `{"key", "answers", "q"}`). The driver writes a question row in
   `judge_own_question` (`S/driver_dialog.py:410-419`) AFTER pricing it, so every record priced while raising question number
   `n` (0-based) carries `q == n`.
2. The ask's ordinal = the index of the LAST row of `driver-questions.jsonl` whose (`kind`, `stage`, `dispatch`) equal the pending
   ask's (`driver-state.json` `asked`, `T/dry_world.py:1115-1121`). Not simply the last row: a deferred question writes a row
   and is not pending (`S/driver_dialog.py:430-433`, `:488-492`).
3. The ask's window = the records with `q == ordinal`, in file order. One helper in `dry_world.py` (name: `ask_window(copy)`
   -> `(ordinal, window)`) is the ONE reader; `run_exit_row`, `_holds` and the `say` step use it (P31; `_ask_of` at `:1251`
   uses the same identified row instead of `questions[-1]`).
4. Error direction: false RED is allowed, false GREEN is not. Known adversarial inputs that must stay safe:
   - a record of an EARLIER ask (`q < ordinal`): never in the window (the s1.review case);
   - a conductor-PROMPT record (`S/driver_conductor.py:686`, written while asking the conductor, not the person) in the raising
     turn of a plain gate ask (e.g. the gate-repair conductor, `S/driver_gates.py:802-813`): it lands in the window with key
     `gate_A`; it cannot make a token row green because the `say` step only reaches an ask that CARRIES `offered`, C2 reads
     `asked.offered` first, and K15 also requires `asked.offered` within the data rows (section 3);
   - a prompt record whose conductor answered `continue`, followed in the same process by another question: it carries that
     question's ordinal; it cannot satisfy another key (K15 compares the key) and cannot widen `asked.offered`;
   - records with no integer `q` (written by an older spy): never in any window (TEMPORAL edge 6).

## 3. The checks on a gate row (K15, C2, C3, C6)

The judged ask of every `gate_A/*` and `gate_B/*` key row is the gate's priced question, reached by the seed `say` step
(section 4). For each check: the expectation (from data) and the observation (what the driver did or wrote in the run).

| check | expectation (data) | observation (driver) | FAIL when |
|---|---|---|---|
| K15 | the key's answer rows, `R/question-prices.json:143-148` (`gate_A`) / `:149-154` (`gate_B`) | (i) a window record with `key == <row key>`; (ii) its `answers` all among the data rows; (iii) when the ask carries `offered`, every offered token (normalised by `s0_normalize`) is among the data rows | no window record of the key ("key not observed: expected gate_A, observed <window keys or none> at question <n>"); empty answers; an answer or offered token outside the rows |
| C2 | the row's token is an answer of the key | the token is in the ask's own offered set: `asked.offered` when non-empty, else the `answers` of the window record whose key is the row key (key rows) or the last window record (other sections); a `driver-answers.jsonl` row with this ask's `question_sha`; no conductor call after the answer except one marked `chosen` (F-2) | as today (`T/dry_exits.py:1314-1329`), with the offered source above |
| C3 | the price row's `factory` column: not `nothing` -> the state moves | the state fingerprint (`T/dry_exits.py:941-986`) after vs at the ask | unchanged (as today); listed only where data expects a change |
| C6 | the gate is asked only when its rehearsal is ready | `gate_ready` on the row's copy at every gate ask in the row (`T/dry_world.py:1254-1259`) | as today (`T/dry_exits.py:1355-1359`) |

`n/a` (fork F-3, recommendation (a)): a row may declare `expect.na: {"<check>": "<why>"}` for K15, C2 or C3 (never C6: the
rehearsal is always observable at a gate ask). The judge prints `n/a <check>: <why>` in the outcome detail; an n/a check is
never counted as passed and never read from another ask. Guards (checked against the run's observation, so a declaration
cannot hide a red): K15 n/a is legal only when the judged ask carries NO `offered` (else FAIL "K15 declared n/a but the ask
offered [...]"); C2 n/a is legal only on a row whose answer has no token (a token is always C2-judged); a check both listed and
n/a is refused by the loader; a runnable row with no listed check is refused as today (`T/dry_exits.py:1117-1118`).

### Per variant (the six of `gate_A`; `gate_B` identical at S8)

Seed for all six: `to-gate-A-priced` (section 4). Driver expectations are from `R/question-prices.json:143-148` and the
executors named at `S/driver_machine.py:2360-2361` / `S/driver_conductor.py:757-762`.

| variant | what the driver is expected to do (data) | K15 | C2 | C3 | C6 |
|---|---|---|---|---|---|
| `rework` | factory `stages_again`, person `answer`, delivery `waits`: the token goes to the conductor (`why=chosen`) with the ORIGINAL words file; a one-option `rework` answer is recorded as `seam_rework` and run (`S/driver_conductor.py:675-676`, `:727-752`) | observed on the seeded ask | token in `asked.offered`; answer row; the `chosen` call is allowed (F-2) | listed: dispatches move | listed |
| `approve` | factory `record`, delivery `unchanged`: recorded by code from the original answer's words file (`approved_by` option, `S/driver_gates.py:1262-1287`) | observed | token offered; answer row; no conductor call | listed: `pipeline.gates` moves | listed |
| `retry` | factory `nothing`, person `your_work`: the gate is shown again | observed | token offered; answer row; no conductor call | `na`: "price row retry: factory nothing - the gate is shown again and nothing is recorded" | listed |
| `stop` | factory `nothing`, delivery `no`: held, the question comes back changed (`S/driver_machine.py:2354`) | observed | token offered; answer row; no conductor call | `na`: "price row stop: factory nothing" (today the row omits C3 silently) | listed |
| `free words` | not a token: a new gate answer (`S/driver_machine.py:3397-3407`); not the approval word -> kept words go to the conductor, which returns the gate's priced choices | observed on the seeded ask | `na`: "at a gate, words that are not a token or the approval word go to the conductor by design (driver_machine.py:3606-3607, driver_conductor.py:880-882)" (guard holds: no token) | `na`: "nothing is recorded until the person chooses; the packet says so (driver_gates.py:138-141)" | listed (the only listed check; see F-4) |
| `empty` | refused before any kind branch: `Stop ... is empty` (`S/driver_machine.py:3380-3381`), the same ask still pending | observed on the seeded ask | not listed (the `empty` check is the variant's whole expectation, F-W8) | not listed | not listed |

Row data after the change (exact): `gate_A/rework` `seed: "to-gate-A-priced"`, `answer.words: null` (a token answer ignores
words, `T/dry_world.py:1110-1112`), `checks: ["C2","C3","C6"]`, `stub` per section 7; `gate_A/approve` checks `["C2","C3","C6"]`;
`gate_A/retry` checks `["C2","C6"]`, `na: {"C3": ...}`; `gate_A/stop` checks `["C2","C6"]`, `na: {"C3": ...}`;
`gate_A/free words` checks `["C6"]`, `na: {"C2": ..., "C3": ...}`; `gate_A/empty` checks `["empty"]`; all six `seed` set. The six
`gate_B/*` rows the same with `to-gate-B-priced`. `gate_A/words:questions-deferred` (live_only, FV1-8, plain ask by intent): add
`na: {"K15": "a plain gate ask offers nothing and prices nothing (driver_gates.py:322, driver_dialog.py:321)"}` so it is
judgeable once its state has a writer; its reach stays `live_only`.

## 4. The seed step `say` (new, `dry_exits` grammar + `dry_world.run_seed`)

`{"say": {"stage": "S4", "question": "gate_A", "words": "<text>"}}` - exactly these three keys, all non-blank text, stage
`S0`..`S9`, words ASCII and not starting a line with `## ` (section 5, adversarial input of F-2).
Run: (1) the pending ask must be `question` at `stage`, else NOT reached: "say: pending is <kind> at <stage>, expected
<question> at <stage>" (a pending `conductor` likewise); (2) write the words as the answer, one driver process
(`--answer <file> --max-boundaries 60`, the `drive_until` turn form, `T/dry_world.py:1187-1198`), under the row's budget;
(3) reached only when a new question row was written AND the pending ask carries a non-empty `offered`; else NOT reached:
"say: the words at <question> raised no question with offered answers (pending <kind>, offered [])" or "the driver exited (<rc>)
with no new question". Invariant: a seed never reaches a plain ask by `say`, so a token row can never be judged at a plain ask.
Recipes in `T/fixtures/stories/dry-1/seeds/gates.json` (today `recipes: {}`):
`to-gate-A-priced: [{"say": {"stage": "S4", "question": "gate_A", "words": "Before approving, add a case for the empty cart."}}]`,
`to-gate-B-priced`: the same at `S8` / `gate_B`. The words are not an approval word (`R/gate-approval-words.json:3-4`); they
become the ORIGINAL answer the `approve` and `rework` options act on.

## 5. Edges (each with the invariant it protects)

1. No record at all (`dry-priced.jsonl` absent or empty): window empty -> K15 FAIL "key not observed ... none"; C2 on a token row
   reads `asked.offered` only. Invariant: absence of evidence never passes.
2. Records of an EARLIER ask only (`q < ordinal`, the s1.review case): window empty, same FAIL; the detail names the newest
   earlier key once ("an earlier ask's record (s1.review) is not read"). Invariant: another ask's record never counts.
3. Empty offered set (`asked.offered == []` after `say`, or a window record with `answers: []`): `say` is NOT reached (seed FAIL);
   a record with no answers -> K15 FAIL (as today `T/dry_exits.py:1387`). Invariant: an ask offering nothing never passes a token row.
4. A gate reached by the seam question vs a plain ask: told apart by the driver's own record - plain = gate kind with no
   `offered`, seam = with `offered` (`S/driver_conductor.py:419-427` sets it on every seam Person). Token rows reach only the
   seam (section 4); a plain-ask row must declare K15 n/a and the guard refuses that declaration on a priced ask. `drive_until`
   is unchanged in meaning (`_holds`: kind matches, or a window record names the question). Invariant: a plain-ask approval word
   is never counted as the `approve` option.
5. TEMPORAL - `gate_B` rows print `after:FV3-5` today (start snapshot S8 not made; report line 10, 40). World before FV3-5: same
   NOTE, the new `seed`/`na` fields are validated by the loader now (a recipe that does not exist is refused, EW5) but nothing
   runs. World after FV3-5 lands (the main pass passes S5 and makes S8): the rows run with `to-gate-B-priced`, same checks. The
   move that creates the S8 snapshot is FV3-5, not this card.
6. TEMPORAL - the `q` field: records without it exist only in a world made by the old spy; every part run rebuilds its
   snapshots (report line 53, prefix from S0), so after this change every record carries `q`. A record without an integer `q`
   is never attributed; a window empty for that reason says "the price records carry no ask ordinal (older spy)".
7. No question row matches the pending ask (ordinal unknown): K15 FAIL "the pending ask has no question record; its price records
   cannot be identified"; C2 reads `asked.offered` only. Invariant: an unknown is never a pass (AR-28).
8. A malformed line in `driver-questions.jsonl`: the walker's `read_rows` raises (`T/dry_world.py:726-742`) - the row errors,
   never judged; the spy's count through `driver_journal.question_rows` cannot then disagree with an accepted judgment.
9. Cap: the extra `say` turn counts against the 240 s row cap; over it -> FAIL naming the phase (EW23, existing).
10. Post-answer turns re-send the same answer each turn (`T/dry_world.py:1263-1284`): for `free words` the conductor returns the
    same gate question; a third identical ask sets `loop` and ends the turns. C5 is not listed on that row, so the walker's own
    repetition is not judged as a product loop (stated, not hidden: F-4).

## 6. Test rows (docs/TESTING.md: the scenario part is the test; pure judges get table rows; no new test file)

- `T/dry_exits.py` judge table (`:2593-2607`, the `good` facts `:2585-2587` take `priced_window`, `ask_ordinal` instead of
  `priced_at_ask`): rows - (1) K15 window has only an earlier key -> FAIL "key not observed"; (2) K15 window record of the key but
  `asked.offered` holds a token outside the rows -> FAIL; (3) K15 n/a declared, ask without `offered` -> outcome detail carries
  `n/a K15`, not FAIL; (4) K15 n/a declared, ask WITH `offered` -> FAIL "declared n/a"; (5) C2 offered from `asked.offered` wins
  over the window record; (6) C2 a `chosen` conductor call is not an unread call (F-2); (7) C2 n/a on a token row -> loader refusal
  (a `walk_row_problems` case beside the existing loader cases).
- `T/dry_exits.py` loader cases: `say` grammar (missing key, blank words, stage outside S0..S9, a words line starting `## `).
- `T/dry_exits.py` `run_seed` cases (beside `:2575-2581`, fake `drive_fn`): `say` reached when the next ask carries `offered`;
  not reached when it does not; not reached when the pending ask is another question.
- `T/dry_stub.py` spy row `:1379-1381`: expected record becomes `{"key": "s1.gap", "answers": ["go on", "stop"], "q": 0}` (no
  questions file in the tmp task); one more row: with a questions file of 2 rows, `q == 2`. If F-2 (a): one stub row - a prompt
  whose last section heading is `## The person's choice` journals `chosen: true`, one without journals `false`.
- The scenario: `test_scenario_dry_1.py --part exits:gates` is the behaviour test of the twelve rows.

## 7. Census and ratchet effect (`T/fixtures/driver-exits/gates.json`)

- The twelve rows keep `reach: story`; no census entry changes; `ratchet` (`:430`) unchanged; `live_only` raised_by entries
  unchanged (the FV1-8 entry `:472` stays). `dry_exits.py --check` stays `0 discrepancies`.
- Rework probe (do FIRST, one row run): the stub's default conductor offers every open move (`T/dry_stub.py:91-115`), so at the
  `chosen` call it does not return ONE rework option and nothing is recorded. The row's `stub.conductor` carries a verdict as
  written: `ask_person` with exactly one `rework` option whose `args` come from the closed list the prompt prints ("Moves open
  here"). If no such control yields a recorded `seam_rework` within the cap, the builder sets `gate_A/rework` and `gate_B/rework`
  to `live_only` with the measured why, adds one `raised_by` entry each (`live_only | walk/gate_X/rework | <why>`), and reports;
  then `gate_A`/`gate_B` are not in `dry_exits.driven_keys()` (`T/dry_exits.py:885-896`) and N4c keeps their `PINNED_ELSEWHERE`
  entries (finish spec, N4c edge 1).
- No `known_red/gates.json` row is written by this card: a row still red after it is reported with its evidence; the Lead labels.

## 8. The card (header-ready)

given: this file; `C:/QAFactory/forge-repo/.claude/worktrees/agent-a4aebd95c3ca7d59c/docs/tasks/specs/reports/20261117-p1b-n4-gates-report.md` (sections "Rows that run but are red", "Walker defects noticed", "Walker fix"); `C:/QAFactory/forge-repo/docs/tasks/specs/20261114-p1b-n4w-exit-walker-spec.md` (K15, C2 F-W7, C3, C6, EW17-EW24); `C:/QAFactory/forge-repo/plans/builder-rules.md`; `C:/QAFactory/forge-repo/ai-packages/qa-factory/design/factory-rules.md`; `C:/QAFactory/forge-repo/docs/TESTING.md`; read-only code: `scripts/driver_gates.py`, `scripts/driver_conductor.py`, `scripts/driver_machine.py`, `scripts/driver_dialog.py`, `scripts/driver_journal.py`, `references/question-prices.json`, `references/gate-approval-words.json`
owns: C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/dry_driver.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/dry_world.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/dry_exits.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/dry_stub.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/fixtures/stories/dry-1/exits/gates.json
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/fixtures/stories/dry-1/seeds/gates.json
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/fixtures/driver-exits/gates.json
non-goals: any file under `scripts/` outside `scripts/tests/` and anything under `references/` (no production change); rows of other groups (s0, s1-s4, s5, s6-s9: they inherit the identity rule automatically; their gate key rows take the `say` form in their own nodes); `test_conductor_doors.py` / `PINNED_ELSEWHERE` (N4c); `known_red` labels (Lead); the joint and post-answer-window walker defects 2-4 of the report; changing C3's meaning for `factory: nothing` rows (F-5)
handoff: a report `docs/tasks/specs/reports/20261117-p1b-gate-ask-judge-report.md` in the tree: the row table (row -> seed reached -> outcome), the rework probe result, the verbatim witness outputs, the FR walk, analogs noticed
edges: section 5 of this file, items 1-10, each with its invariant; section 2 item 4 (adversarial inputs, error direction: false red allowed, false green not)
DoD: (1) section 2 rule implemented through one helper `ask_window`; `priced_at_ask` removed in favour of `priced_window` + `ask_ordinal`; (2) `say` step per section 4; (3) checks and `na` per section 3, guards included; (4) the twelve gate rows and the FV1-8 row per section 3 "Row data"; (5) table rows per section 6; (6) witness, run once on the final state: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <the owns above>` and every file it prints; `( cd <tree>/ai-packages/qa-factory && python -B scripts/tests/dry_exits.py --selftest )`; `( cd <tree>/ai-packages/qa-factory && python -B scripts/tests/dry_stub.py --selftest )`; `( cd <tree>/ai-packages/qa-factory && python -B scripts/tests/dry_exits.py --check )` = `0 discrepancies`; ONE run of `( cd <tree>/ai-packages/qa-factory && python -B scripts/tests/test_scenario_dry_1.py --part exits:gates )` (about 11 minutes) in which `gate_A/{approve,retry,stop,free words,empty}` PASS, `gate_A/rework` PASS or `live_only` per section 7, `gate_B/*` NOTE `after:FV3-5`, `outcomes` PASS; a row still red is reported with its verbatim line, not labelled
siblings: axis 34 (one action, one road): the gate key rows of groups s5 and s6-s9 reach the gate's priced question by the same `say` step form in their own seed files (their nodes); every key row of every group reads its ask's window (automatic: one helper); axis 38 per the report's "Siblings noticed": the walker limits 2-4 stay queued as written there
designer: C:/QAFactory/forge-repo/docs/tasks/specs/20261117-p1b-gate-ask-judge-card.md

## 9. Forks (Lead decides; the card is executable on each recommendation)

- **F-1. Which option for the six rows.** (a) judge vs data rows; (b) drive to the seam question; (c) `live_only`.
  Recommendation (b), reasons in section 0. Cost of (b): one new seed step, one spy field, about one extra driver turn per gate
  row (inside the 240 s cap, not measured). Cost of (c): `gate_A`/`gate_B` never driven; N4c keeps them pinned elsewhere.
- **F-2. C2's "no conductor call after the answer" at `rework`.** The `rework` token's executor IS a conductor call
  (`why=chosen`, `S/driver_machine.py:2355`, `:2361`); the walker reads a call's why only when the next pending ask is kind
  `conductor` (`T/dry_world.py:1274-1275`), and at a gate the seam asks with kind `gate_A`, so today C2 reads "a conductor call
  followed ... why not on record" -> a designed red. The driver records no why for a call (`S/driver_conductor.py:342-347`).
  (a) the stub journals `chosen: true` when the prompt's section heading `## The person's choice` is present (the driver's own
  structural heading, `S/driver_conductor.py:687`; precedent: the stub already parses `## Moves open here`, `T/dry_stub.py:57-68`);
  C2 counts only calls not marked `chosen`. Adversarial input: a person's words carrying that heading line - the `say` grammar
  and row words refuse a line starting `## ` (fixtures are ours); error direction: misreading can only hide an unread call
  behind a heading in OUR words, which the loader refuses. (b) the rework row drops C2 (breaks the guard "a token is always
  C2-judged"). (c) rework `live_only`. Recommendation (a).
- **F-3. Shape of the not-applicable declaration.** (a) row field `expect.na: {check: why}` with the observation guards of
  section 3; (b) a data file of ask forms (`plain_gate`) read by a capability key; (c) no mechanism: rows omit checks silently
  and a plain-ask row stays red / `live_only`. Recommendation (a): the declaration sits beside the row it qualifies, and the
  guards make it unable to hide a red. Cost: one `EXPECT_KEYS` entry and three guard rules.
- **F-4. How strongly `free words` at a gate is judged.** (a) at the seam question: K15 (on the seeded ask) + C6, C2 and C3 n/a
  with why - weak for the answer itself, but the plain-ask words road is proven by every other row's seed; (b) at the PLAIN ask
  with a new check "the answer raised a question whose offered answers are all rows of the key" (K15 applied to the ask after the
  answer) - strong, costs a new check id (data, xref) and a second meaning of "the judged ask" for one variant; (c) `live_only`.
  Recommendation (a) now, (b) as a finding for the walker pile if the Lead wants the answer itself observed.
- **F-5. C3 on `factory: nothing` answers.** (a) declare C3 n/a on `retry`/`stop` (this card); (b) make C3 data-driven for all
  key rows: `factory: nothing` expects the fingerprint UNCHANGED (a real data-vs-driver check), else changed. (b) changes verdicts
  of other groups' rows that list C3 on such answers. Recommendation (a) here, (b) as a finding.

## 10. Small technical choices closed by the designer

- The identity counts question rows through `driver_journal.question_rows` (the one reader), not by counting lines.
- `ask_window` lives in `dry_world.py` (the world reads files; `judge_row` opens none, `T/dry_exits.py:1402`).
- `priced_at_ask` is replaced, not kept beside the window (one fact, one name).
- The `say` turn uses `--max-boundaries 60` like `drive_until`'s turns.
- Seed words: "Before approving, add a case for the empty cart." (ASCII, not an approval word, usable as a rework instruction).
- `answer.words` set to null on the two `rework` rows (a token answer ignores it, `T/dry_world.py:1110-1112`).
- Recipes are repeated per group seed file (seeds are per group by the loader, `T/dry_exits.py:1238-1256`); no shared recipe file.

## 11. Readers of every touched file (designer rule 7)

Commands (Grep tool, pattern `dry_exits|dry_world|dry_driver|dry_stub|dry-priced|seeds/gates|exits/gates|driver-exits/gates`):
- over `C:/QAFactory/forge-repo/tools`: 3 hits, 1 file - `tools/test_workflows.py:348` (CI `tables` job runs `dry_exits.py --check`,
  `dry_stub.py --selftest`, `--part exits:selftest`) and `:351-352` (pytest install for the dry world). Unchanged: no CLI or file
  name changes.
- over `.githooks`: 0 hits; positive control `python|tools/` in the same folder: 22 hits in 4 files.
- over `.claude/agents`, `.claude/skills`, `.claude/settings.json`: 0 hits; positive control `scenario_walk|handoff` in
  `.claude/agents`: 10 hits in 3 files. (A search over the whole `.claude/` hit only worktree copies and timed out; scoped as above.)
- inside the package (`<tree>/ai-packages/qa-factory/scripts`, pattern adds `priced_at_ask|DRIVE_UNTIL_KEYS|SEED_STEP_KEYS|EXPECT_KEYS`):
  `T/dry_exits.py` 22, `T/dry_world.py` 31, `T/dry_stub.py` 8, `T/dry_driver.py` 3 (all owned here); `T/test_scenario_dry_1.py` 16
  (calls the walker; signatures of `run_exit_row`/`judge_row` unchanged - unchanged); `T/test-layers.json` 1, `T/fixtures/driver-layers.json`
  1, `T/fixtures/driver-exits/classes.json` 1 (file names only - unchanged).
- parallel streams that meet at `dry_exits.py`: FV3-14 (`_count_reach`) and N3a (after N4R) per the finish spec (`:485`, `:510`) -
  changes in those streams, sequenced after this card; `dry_driver.py` record shape is read by `dry_world.py:1024` (keys only -
  unchanged).

## 12. Reading trail

Read this round (tree above): report `20261117-p1b-n4-gates-report.md` whole (1-121); `T/dry_exits.py` 1280-1509 (`_check_c2`
1314-1329, `_judge_always` 1380-1398, `judge_row` 1401-1437, `judge_group`), 885-896 (`driven_keys`), 941-1009 (fingerprint,
`same_ask`), 1013-1256 (`_subject_of`, grammar, `_seed_problems`, `load_seeds`), 2575-2654 (selftest tables); `T/dry_world.py`
726-742, 1110-1297 (`pending_ask`, `counts`, `row_facts`, `_holds`, `run_seed`, `run_exit_row`), grep hits 716, 1024; `T/dry_driver.py`
1-83 whole; `T/dry_stub.py` 56-120, 1370-1394, grep of `conductor`; `S/driver_gates.py` 1-102, 104-322, 788-800, 1099-1124,
1262-1287; `S/driver_conductor.py` 320-348, 419-438, 460-555, 600-700, 754-799, 852-882; `S/driver_machine.py` 3375-3504,
3560-3629, 4080-4139, 2349-2371, 2715-2754; `S/driver_dialog.py` 290-349, 395-424; `S/driver_journal.py` 388-399 (grep);
`S/driver_runner.py` 452-453, 1277-1285 (grep); `R/question-prices.json` 135-159; `R/gate-approval-words.json` (grep 3-4);
`T/fixtures/stories/dry-1/exits/gates.json` 1-31; `.../exits/s1-s4.json` whole; `.../seeds/gates.json` whole; `.../story.json:85`;
`T/fixtures/driver-exits/gates.json` (grep 430, 472); N4w spec (grep K15/C2/C3/C6, 485-499); finish spec (grep F-P8/F-P9/F-P15/N4c);
`plans/builder-rules.md` 7a-7d (28-83).

NOT read (claims depending on them are marked as probes or forks): `no_move.validate_options` / `open_moves` / `moves_section`
and `references/conductor-actions.json` (whether the stub conductor's option tokens at a gate equal the gate answers - if not,
K15 (iii) turns red, which is the correct direction); `combine_gate_words`, `seam_tokens`; gate B's stand-gap and exploratory
readers on the seed words; `test_scenario_dry_1.py` and `walk_exits` (the `after:` logic); `driver_core.GATE_KINDS`;
`judgment-census.json` scope; what `scenario_walk.py --witness-for` prints for these owns; whether `s1.review/free words` passes
C2 today; the 240 s cap headroom with the extra `say` turn (not measured).
