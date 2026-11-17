# P1-b walker: how a gate key row is judged — builder card r2 (t-1057, designer fix round of t-1045)

Status: DRAFT r2 for Lead acceptance. It replaces `docs/tasks/specs/20261117-p1b-gate-ask-judge-card.md` (r1) WHOLE: the builder
gets this file alone. Fix round of the plan critic's verdict `docs/tasks/specs/reviews/t-1054-p1b-gate-ask-judge-plan.md`
("needs work, dispatchable after B1-B6"). Every finding B1-B6, F1-F10 is applied (table "Fix round t-1057", the last section).

Base read this round: branch `worktree-agent-a4aebd95c3ca7d59c`, tree
`C:/QAFactory/forge-repo/.claude/worktrees/agent-a4aebd95c3ca7d59c` (called `<tree>` below). Prefixes: `T/` =
`<tree>/ai-packages/qa-factory/scripts/tests/`, `S/` = `<tree>/ai-packages/qa-factory/scripts/`, `R/` =
`<tree>/ai-packages/qa-factory/references/`. Every file:line below was read in THAT tree unless it says "main checkout".

## 0. Preconditions of the dispatch (F10, B6)

1. **Dispatched only after N2h-v is merged to `main`.** `T/dry_stub.py` is shared with N2h-v
   (`docs/tasks/specs/20261117-p1b-n2h-v-critic-stub-window-card.md`): both touch `fill_role` (this card: the conductor `else:`
   branch, `T/dry_stub.py:903-913`; N2h-v: the ROLE branch and `critic_branch` / `automator_branch`) and both append selftest
   rows. Disjoint by block, not by function. The Lead puts the N2h-v merge commit sha into the dispatch (`given:`).
2. **The builder's FIRST move** (before any edit): `git -C <tree> fetch origin`, then `git -C <tree> merge origin/main`. On a
   conflict in `T/dry_stub.py` keep BOTH sides (N2h-v's branches and selftest rows, and this branch's), then
   `git -C <tree> merge-base --is-ancestor <N2h-v sha> HEAD` must exit 0. The merge also brings the main checkout's
   `T/fixtures/driver-exits/known_red.json` label `main/S5 -> FV3-20` (main checkout, read this round: `"node": "FV3-20"`,
   written by N2h-b2, commit fda7c6d5; this tree still says `FV3-5`, `T/fixtures/driver-exits/known_red.json:5`). The merge is
   not authoring: files it brings are not owns and are not edited.
3. **The "before" lines of B4** are taken right after the merge, before any edit (DoD (7)).

## 1. Chosen option (F-1 decided: (b)) and why

**(b) drive each gate key row on to the gate's priced question (the seam question), plus one ask-identity rule for every key
row.** At the plain gate ask the driver offers nothing and prices nothing (`S/driver_gates.py:322` raises a bare `Person`;
`S/driver_dialog.py:321` writes `offered` only `if person.offered`). `rework / approve / retry / stop` are the answers of the
price key `gate_A` (`R/question-prices.json:143-148`; `gate_B` `:149-154`), and the only question that offers them to a person
is the seam question at a gate. The product's packet tells the person this very road ("say what in your own words instead of
`approve` ... you get the choices", `S/driver_gates.py:136-141`). At the plain ask the only closed word is the approval word
(`R/gate-approval-words.json:3-4`; read from the first line only, `S/driver_gates.py:1099-1117`); every other answer is words
that go to the conductor (`S/driver_machine.py:3606-3607`). The plain-ask words road is judged by every gate row's seed (§4):
a seed that does not reach a question with offered answers is a FAIL (`T/dry_exits.py:1414-1415`). The plain-ask approval
word is walked by the main pass (`T/fixtures/stories/dry-1/story.json:85`, `gate_A: approve`).

## 2. Architecture, FR, census (test layer only)

- Touches only `scripts/tests/` (walker, stub, spy, fixtures). No package behaviour, no text a person reads.
- AR-n touched, each kept, with its change check in the DoD:
  - **AR-22** (every field read has a producer): new spy fields `q` and `prompt` (producer `dry_driver.passing_spy`, reader
    `dry_world.ask_window`), new stub journal fields `chosen` and `prompt_chars` (producer the conductor branch of
    `dry_stub.main`, readers `dry_world.row_facts` (`chosen`) and the builder's report (`prompt_chars`)); producer and readers
    in one commit. DoD (3), (4): the selftest rows of §8 show each field written and read.
  - **AR-28** (an unknown never becomes a pass): no record / no ordinal / an empty offered set / a prompt-only window is FAIL;
    an n/a declaration that its guard refuses is FAIL. DoD (3): the judge table rows of §8.
  - **AR-13** (a fact with a reader function is read only through it): question rows are counted by the spy through
    `driver_journal.question_rows` (`S/driver_journal.py:396-399`); prices through `dry_exits.scan_prices`; approval words
    through `gate_brief.approval_words` (the driver's reader, `S/driver_gates.py:1109`); tokens normalised by `dry_exits._norm`
    (= `DriverDialog.s0_normalize`, `T/dry_exits.py:1280-1282`). DoD: review of the diff (no second reader).
  - **AR-20** (ratchets shrink): no reach changes unless the rework probe fails (§9). DoD (5): `dry_exits.py --check` =
    `0 discrepancies`.
  - **AR-29** (code judges data): every check below is data vs a driver record; no role judgment is judged.
- Checks added or altered — owner served, census class:
  | check | change | owner | class |
  |---|---|---|---|
  | K15 | altered: reads the ask's own window; (iii) offered tokens vs rows added; (ii) is a shape guard (F2) | data (code) | xref |
  | C2 | altered: offered set from the ask's own record; conductor calls counted only in the answer's own turn and not when marked `chosen` | data (code) | xref |
  | K15 n/a guard | new: legal only when the judged ask carries no `offered` | data (code) | xref (run record) |
  | C2 n/a guard | new: legal only when the row's answer has no token (loader) | data (code) | shape |
  | C3 n/a guard | new: legal only with no token, or the token's price row says `factory: nothing` (B5) | data (code) | xref (price data) |
  | `say` seed step | new walker grammar; not a check | - | - |
  | post-answer turn end (§5) | walker mechanics; not a check | - | - |
  | `na <n>` NUMBER line | visibility only, not a check, not a ratchet (F9) | - | - |
  No role and no person owns any of them. The judgment census does not scan these files: its `about` says "one row per check
  unit of scripts/*.py outside scripts/tests/" (`T/fixtures/judgment-census.json:3`, read this round).
- Commit lines: `architecture:` and `judgment:` in the form `tools/architecture_gate.py` defines (read it there; the grammar is
  not copied here). Expected content: the AR-n above, each with how it is kept; `judgment: none` WITH its ` -- <why>` (the why:
  test-layer checks under `scripts/tests/`, outside the judgment census scope; no package code changes). Never bare.
- FR: C-11/C-14 (the spy's and the stub journal's output shapes are contracts: the new fields are documented in the docstrings
  of `passing_spy` and the conductor branch); D-59 (an unknown is never a pass); G-30 (fixtures ASCII). Sections A, B, E, F:
  test layer, no refusal, no text a person reads, no delivery, no measurement of money — not applicable.

## 3. The ask identity (applies to every key row in every group)

Today `facts["priced_at_ask"] = priced[-1]` (`T/dry_world.py:1243-1244`) and `_holds` reads `priced[-1]` (`:1153-1154`): the
LAST spy record, whatever ask it belonged to (at the S4 snapshot: `s1.review`'s record).

Rule (invariant: **a price record counts for an ask only if it was written while raising THAT question for the person**):
1. **The spy stamps every record** (`T/dry_driver.py:44-52`; the record becomes `{"key", "answers", "q", "prompt"}`):
   - `q` = `len(driver_journal.question_rows(task_root)[0])` at the moment of the call, with `task_root = sink.parent.parent`
     (the sink is `<task_root>/state/dry-priced.jsonl`, `T/dry_driver.py:31`) (F7). The driver writes a question row in
     `judge_own_question` (`S/driver_dialog.py:410-419`) AFTER pricing it, so every record priced while raising question number
     `n` (0-based) carries `q == n`.
   - `prompt` = `true` when the call happens while the driver composes a conductor prompt: a frame named `_conductor_text`
     is on the call stack (walk `sys._getframe(1)` up by `f_back`, compare `f_code.co_name`; no `inspect.stack()`, which reads
     source). Else `false`. The only conductor-prompt pricing road today: `_conductor_text` (`S/driver_conductor.py:679-687`)
     -> `gate_prices` (`:779-784`) -> `priced_section` (`S/driver_runner.py:1277`) -> `priced_options`. (B3 (a))
2. **The ask's ordinal** = the index of the LAST row of `driver-questions.jsonl` whose (`kind`, `stage`, `dispatch`) equal the
   pending ask's (`driver-state.json` `asked`, `T/dry_world.py:1115-1121`). Not simply the last row: a deferred question writes
   a row and is not pending (`S/driver_dialog.py:429-433`, `:488-492`).
3. **The ask's window** = the records with integer `q == ordinal` AND `prompt` not `true`, in file order. ONE helper in
   `dry_world.py`, `ask_window(copy) -> (ordinal, window)`, is the one reader. Its users: `run_exit_row` (facts at the ask),
   `_holds` (`:1148-1154`), the `say` step (§4), `_ask_of` at `:1251` and the post-answer ask at `:1279` (both take the
   identified row, not `questions[-1]`; F5). `facts["priced_at_ask"]` is REPLACED by `facts["priced_window"]` (the list) and
   `facts["ask_ordinal"]` (int or None).
4. **Error direction: false RED is allowed, false GREEN is not.** Adversarial inputs that must stay on the safe side:
   - a record of an EARLIER ask (`q < ordinal`): never in the window (the s1.review case);
   - a conductor-PROMPT record (`prompt: true`) in the raising turn, with any key: never in the window, so K15 (i) cannot be
     satisfied by a record written for the conductor (B3);
   - a record with no integer `q` (an older spy): never in any window (edge 6);
   - two rows with the same triple (seam after plain; plain after `retry`): the LAST row is the pending one — correct for both;
   - a rename of `_conductor_text` in the driver: prompt records would lose their stamp and enter windows (a false-green
     road). Guard: a selftest row asserts `hasattr(driver_conductor.DriverConductor, "_conductor_text")` AND that
     `driver_conductor.py` calls `self.gate_prices(` exactly once, inside `_conductor_text` (by the module's AST: the call's
     enclosing `def` is `_conductor_text`), with a positive control that the AST walk finds `gate_prices` defined. A fail
     names the function to re-point the stamp at;
   - a record priced, then the rendering failed and the floor was shown (`last_resort`, `S/driver_conductor.py:499-500`,
     `:536-555`): the window holds the priced record of this ask. K15 stays green because its meaning is "the key's prices were
     resolved while raising THIS ask", not "the person saw price lines". That road files a factory `defect_found` and needs an
     unreadable reference file, which the dry world does not ship. Stated, not hidden (noticed analog 3 in §14).

## 4. The checks on a gate row (K15, C2, C3, C6) and the n/a declaration

The judged ask of every `gate_A/*` and `gate_B/*` key row is the gate's priced question, reached by the seed `say` step (§5).

| check | expectation (data) | observation (driver) | FAIL when |
|---|---|---|---|
| K15 | the key's answer rows, `R/question-prices.json:143-148` (`gate_A`) / `:149-154` (`gate_B`) | **(i)** a window record with `key == <row key>` (the key was priced while raising this ask); **(iii)** when the ask carries `offered`, every offered token (by `_norm`) is among the data rows (`asked.offered` is driver-side, after validation). **(ii) shape, not an observation:** the window record's `answers` are non-empty and among the rows — the price resolver refuses an answer outside the rows (`S/no_move.py:612-626`) and the spy records only after success (`T/dry_driver.py:48-50`), so only "non-empty" can really fail (F2) | no window record of the key: `key not observed: expected gate_A, observed <window keys or none> at question <n>`; empty answers; an offered token outside the rows |
| C2 | the row's token is an answer of the key | the token is in the ask's own offered set: `asked.offered` when non-empty, else the `answers` of the window record whose key is the row key (key rows) or the last window record (other sections); a `driver-answers.jsonl` row with this ask's `question_sha`; **no conductor call in the answer's own turn** — counted from the answer up to the end of the FIRST post-answer turn that wrote a new question row (or the last turn when none did), and a stub line marked `chosen: true` is not counted (F-2, B1) | as today (`T/dry_exits.py:1314-1329`), with the offered source and the call count above |
| C3 | the price row's `factory` column is not `nothing` -> the state moves | the state fingerprint (`T/dry_exits.py:941-986`) after vs at the ask | unchanged (as today); listed only where data expects a change |
| C6 | the gate is asked only when its rehearsal is ready | `gate_ready` on the row's copy at every gate ask in the row (`T/dry_world.py:1254-1259`) | as today (`T/dry_exits.py:1355-1359`) |

**C2 cut (B1).** Invariant: **the walker's own re-sent answer is never judged as the person's.** `run_exit_row` takes
`counts(copy)` once more at the end of the first post-answer turn whose question count grew (`first`); `row_facts` counts
`conductor_calls` over `stub[mid["stub"]:first["stub"]]` (to the end when `first` is None) and only lines with
`conductor` set and `chosen` not `true`; `conductor_whys` keeps only the whys seen in turns up to and including that turn.
This changes C2 for every group, so DoD (7) applies.

**The n/a declaration (F-3 decided: (a)).** A row may carry `expect.na: {"<check>": "<why>"}` for K15, C2 or C3 (never C6:
the rehearsal is always observable at a gate ask). `EXPECT_KEYS` (`T/dry_exits.py:64`) gains `na`. The judge prints
`n/a <check>: <why>` in the outcome detail of a PASS or NOTE; an n/a check is never counted as passed and never read from
another ask. Guards (a declaration cannot hide a red):
- **K15 n/a** is legal only when the judged ask carries NO `offered` (run time); else FAIL
  `K15 declared n/a but the ask offered [<tokens>]`.
- **C2 n/a** is legal only on a row whose answer has no token (loader, `walk_row_problems`); a token is always C2-judged.
- **C3 n/a** is legal only when the row's answer has no token, OR the token's row in `question-prices.json` under the row's key
  has `factory: nothing` (run time, in `judge_row`, which already receives `prices`); else FAIL
  `C3 declared n/a but the price row of <token> says factory <x>` (B5). Invariant: a token whose data expects the state to move
  is always C3-judged.
- a check both listed in `checks` and declared n/a is refused by the loader; a key or why that is not non-blank text is refused
  by the loader; a runnable row with no listed check is refused as today (`T/dry_exits.py:1117-1118`).

### Per variant (the six of `gate_A`; `gate_B` identical at S8)

Seed for all six: `to-gate-A-priced` (§5). Data from `R/question-prices.json:143-148`; executors from
`S/driver_machine.py:2387-2400` (`take_seam_answer`) and `:2440-2449` (`seam_chosen`).

| variant | what the driver is expected to do (data) | K15 | C2 | C3 | C6 |
|---|---|---|---|---|---|
| `rework` | factory `stages_again`: the token goes to the conductor (`why=chosen`, `S/driver_machine.py:2446`) with the ORIGINAL words file; a one-option `rework` answer with `args` is recorded as `seam_rework` (`S/driver_conductor.py:675-676`, `:727-752`) | on the seeded ask | token in `asked.offered`; answer row; the `chosen` call is not counted | listed | listed |
| `approve` | factory `record`: recorded by code from the original answer's words file (`S/driver_machine.py:2390-2391`) | on the seeded ask | token offered; answer row; no conductor call | listed | listed |
| `retry` | factory `nothing`: "nothing is recorded; the gate is shown again" (`S/driver_machine.py:2392-2394`) | on the seeded ask | token offered; answer row; no conductor call in the answer's own turn | n/a: "factory nothing: the gate is shown again and nothing is recorded; the unchanged-state check is F-5 (b), queued at finding R1-a (§11)" | listed |
| `stop` | factory `nothing`: held, the question comes back (`S/driver_machine.py:2395-2397`) | on the seeded ask | token offered; answer row; no conductor call | n/a: "factory nothing: the unchanged-state check is F-5 (b), queued at finding R1-a (§11)" | listed |
| `free words` | not a token: new gate words (`S/driver_machine.py:3403-3407`); not the approval word -> to the conductor | on the seeded ask | n/a: "at the seam question, words that are not a token are new gate words and go to the conductor by design (driver_machine.py:3403-3407, :3606-3607)" (guard holds: no token) | n/a: "nothing is recorded until the person chooses; the packet says so (driver_gates.py:136-141)" (guard holds: no token) | listed (the only listed check, F-4) |
| `empty` | refused before any branch: `... is empty` (`S/driver_machine.py:3380-3381`), the same ask still pending | on the seeded ask | not listed | not listed | not listed (`checks: ["empty"]`) |

### Row data after the change (exact, `T/fixtures/stories/dry-1/exits/gates.json`)

- `gate_A/rework`: `seed: "to-gate-A-priced"`, `answer: {"token": "rework", "words": null, "words_file": null}`,
  `checks: ["C2","C3","C6"]`, `stub` per §9. **Why `words: null` is NECESSARY (F3):** with both set, `answer_bytes` writes
  `"rework\n<words>"` (`T/dry_world.py:1108-1109`), and the driver compares the WHOLE answer with the seam tokens
  (`S/driver_machine.py:3403-3404`), so `rework\n...` would be new gate words, not the token. The instruction words the rework
  acts on are the seed's words (the ORIGINAL answer).
- `gate_A/approve`: `seed` set, checks `["C2","C3","C6"]`.
- `gate_A/retry`: `seed` set, checks `["C2","C6"]`, `na: {"C3": <why above>}`.
- `gate_A/stop`: `seed` set, checks `["C2","C6"]`, `na: {"C3": <why above>}`.
- `gate_A/free words`: `seed` set, checks `["C6"]`, `na: {"C2": ..., "C3": ...}`.
- `gate_A/empty`: `seed` set, checks `["empty"]`.
- The six `gate_B/*` rows the same with `to-gate-B-priced`.
- `gate_A/words:questions-deferred` (FV1-8, `live_only`, plain ask by intent) (B2): `answer: {"token": null, "words": "approve",
  "words_file": null}`, `checks: ["C3","C6"]`, `na: {"K15": "a plain gate ask offers nothing and prices nothing
  (driver_gates.py:322, driver_dialog.py:321)", "C2": "at a plain gate the approval word is words read by gate_approval, not an
  offered token (driver_gates.py:1099-1117)"}`; `seed` stays null, `reach` stays `live_only`, `why_unreached` unchanged. Both
  guards hold: no token (C2), and the plain ask carries no `offered` (K15).

## 5. The seed step `say` (new; `dry_exits` grammar + `dry_world.run_seed`)

`{"say": {"stage": "S4", "question": "gate_A", "words": "<text>"}}` — exactly these three keys, all non-blank text. Loader
(`_seed_problems`, `T/dry_exits.py:1211-1235`; `SEED_STEP_KEYS` `:67` gains `say`, a new `SAY_KEYS`): stage `S0`..`S9`; words
ASCII; no line of the words starts with `## `; the FIRST non-empty line of the words, normalised by `_norm`, is NOT an approval
word of the stage's gate (`gate_brief.approval_words("A"|"B")`; such words record the gate, `S/driver_gates.py:1117`) (F4).

Run (in `run_seed`, `T/dry_world.py:1157-1205`):
1. the pending ask must be kind `question` at `stage`, else NOT reached:
   `say: pending is <kind> at <stage>, expected <question> at <stage>` (a pending `conductor` likewise);
2. write the words as the answer, ONE driver process (`--answer <file> --max-boundaries 60`, the `drive_until` turn form,
   `:1187-1198`), under the row's budget;
3. reached only when ALL hold: a new question row was written, the pending ask is STILL kind `question` at `stage` (F4), and it
   carries a non-empty `offered`. Else NOT reached, naming which: `say: the words at <question> raised no new question`
   / `say: pending is now <kind> at <stage>, expected <question>` / `say: the new <question> ask offers nothing (offered [])` /
   `the driver exited (<rc>) with no new question`.
Invariants: a seed never reaches a plain ask by `say`, so a token row can never be judged at a plain ask; the seed reaches THIS
gate's priced question, never another question that happens to carry `offered`.

**Which road the seed takes (B3 (b)), by reading — the first probe run measures it.** The default stub conductor offers every
move of `## Moves open here` (`T/dry_stub.py:91-115`), `rework_stage` included, with no `args`; `check_args` refuses an option
with no `args` (`S/no_move.py:231-232`, per critic t-1054 trail) -> `ArgsRefused` -> one re-ask (`S/driver_conductor.py:661-669`)
-> the same answer -> `fallback_person` with the rule (`:663-664`), which files ONE `defect_found` (`:487-488`) and builds
`gate_fallback_question` (priced at `:523`). So every gate seed is expected to reach the CODE fallback, with offered tokens from
`GATE_OPTIONS` filtered by the open moves (`:513-524`), and to file one factory `defect_found` per row — a stub artefact, stated,
never judged by any check of this card. The `rework` row's control (§9) is also active during the seed (`copy.control` runs
before `run_seed`, `T/dry_world.py:1232-1235`): its lone option is refused at a non-chosen call ("one option is legal only as the
rework option when chosen"; `again` is False for a non-chosen call, `:702`) and the road ends at the same fallback. The probe
(§9, step 1) prints, for `gate_A/approve`, the window (records with `q`, `prompt`) and `asked.offered`, so the road is measured.

Recipes in `T/fixtures/stories/dry-1/seeds/gates.json` (today `recipes: {}`):
`"to-gate-A-priced": [{"say": {"stage": "S4", "question": "gate_A", "words": "Before approving, add a case for the empty cart."}}]`,
`"to-gate-B-priced"`: the same at `S8` / `gate_B`.

## 6. Post-answer turns: the answer is re-sent only to the ask it was written for (B1; fork F-6, executable by its recommendation)

Today the post-answer loop (`T/dry_world.py:1263-1286`) re-sends the same answer every turn until the fingerprint changed, a
loop showed, or `POST_TURNS` (4, `:1076`) ran out. Traced for `gate_A/retry` (by reading): turn 1 `retry` at the seam -> "the gate
is shown again" -> a PLAIN gate ask (new row, fingerprint unchanged: it holds `asked.kind/stage` only, `T/dry_exits.py:958`);
turn 2 re-sends `retry` to the PLAIN gate, where it is words -> conductor -> fallback seam; turns 3-4 alternate seam/plain. The
offered sets differ (plain `[]`, seam tokens), so `same_ask` (`T/dry_exits.py:1004-1009`) never sees three equal asks; no loop,
fingerprint unchanged -> `exhausted` -> the always-check `turns` FAILs (`T/dry_exits.py:1397-1398`), besides C2 (cut above).
So the C2 cut alone does not make the row green: the critic's B1 trace stops at C2.

Rule (recommendation of F-6): after a post-answer turn that wrote a new question row, the turns END when the new pending ask is
not `same_ask` as the judged ask (the ask the answer was written for). Invariant: **the walker's answer is only ever sent to the
ask it was written for.** C5 is unaffected (it needs three identical asks in a row, which only arise while the ask stays the same).
Error direction: fewer turns can only show an unchanged fingerprint where a later re-sent turn would have changed it (C3 false
red, allowed); a row that today passes only because the walker re-sent its answer to a different question was a false green.
The `exhausted` flag is not set when the turns end by this rule.

## 7. Edges (each with the invariant it protects)

1. **No record at all** (`dry-priced.jsonl` absent or empty): window empty -> K15 FAIL `key not observed ... none`; C2 on a token
   row reads `asked.offered` only. Invariant: absence of evidence never passes.
2. **Records of an EARLIER ask only** (`q < ordinal`): window empty, same FAIL; the detail names the newest earlier key once
   (`an earlier ask's record (s1.review) is not read`). Invariant: another ask's record never counts.
3. **Only a prompt record in the window's ordinal** (`prompt: true`): excluded -> window empty -> K15 FAIL with
   `only a conductor prompt priced <key> at question <n>; the person's question carries no price record`. Invariant: a record
   written for the conductor never counts for the person's question.
4. **Empty offered set** (`asked.offered == []` after `say`, or a window record with `answers: []`): `say` NOT reached (seed FAIL);
   a record with no answers -> K15 FAIL (`T/dry_exits.py:1387`). Invariant: an ask offering nothing never passes a token row.
5. **Seam vs plain ask**: told apart by the driver's own record — plain = gate kind with no `offered`, seam = with `offered`
   (`S/driver_conductor.py:419-427` sets it on every seam Person). Token rows reach only the seam (§5); a plain-ask row must
   declare K15 n/a, and the guard refuses that declaration on an ask with `offered`. Invariant: a plain-ask approval word is never
   counted as the `approve` option.
6. **TEMPORAL — the `q` and `prompt` fields.** World before this change: records carry only `{key, answers}`. World after:
   every record carries both; every exits part rebuilds its snapshots from S0, so no old record is read in a run after the
   change. A record without an integer `q` is never attributed; a window empty for that reason says `the price records carry no
   ask ordinal (older spy)`. The move that creates the fields: this card's change to `T/dry_driver.py`.
7. **TEMPORAL — the `gate_B` label (B6).** The `gate_B/*` rows start at S8; the main pass stops before S8 at the row
   `main/S5` of `T/fixtures/driver-exits/known_red.json`. Its node is `FV3-5` in this tree before the merge (`:5`) and `FV3-20`
   after the merge of `origin/main` (§0 step 2; the move that changed it is N2h-b2, commit fda7c6d5). Worlds at run time:
   (W1) `known_red.json` holds a `main/*` row whose stop is before S8 -> the six `gate_B/*` rows print NOTE `after:<that row's
   node>`, read from the file at run time (not typed in the DoD); their new `seed`/`na` fields are still validated by the loader
   (a recipe that does not exist is refused, EW5). (W2) no `main/*` row stops the pass before S8 and the S8 snapshot exists ->
   the six rows run with `to-gate-B-priced` and the same expectations as `gate_A`. The move that makes S8 is the fix of the node
   that labels `main/S5` (FV3-20 / N2h-v, or a later node), not this card. Invariant: a row whose start snapshot does not exist is
   never judged and never green.
8. **No question row matches the pending ask** (ordinal unknown): K15 FAIL `the pending ask has no question record; its price
   records cannot be identified`; C2 reads `asked.offered` only. Also the case where `human_text` raises in
   `judge_own_question` and the row is never written (`S/driver_dialog.py:403-409`). Invariant: an unknown is never a pass (AR-28).
9. **A malformed line in `driver-questions.jsonl`**: the walker's `read_rows` raises (`T/dry_world.py:726-742`) -> the row
   errors, never judged. The spy counts good rows only (`question_rows` skips bad lines), so the two counts can disagree only in a
   file the walker refuses. Invariant: a count the walker cannot read never yields a judgment.
10. **An ask re-raised without pricing (F6)**: `held_question` builds the Person from `asked` with NO pricing
    (`S/driver_dialog.py:600-629`, per critic trail) and `ask()` writes a new row; a deferred question asked again before gate B is
    the same re-raise. Window empty -> K15 FAIL `the ask was raised again without pricing (held); question <n>`. It is never read
    from the earlier raise's window. Invariant: a record of an earlier raise never counts for the re-raise (false red allowed).
    In this card, `stop`'s post-answer ask is such a held ask; K15 judges the SEEDED ask, so the gate rows are not affected; groups
    s6-s9 will meet it on their own key rows.
11. **Cap**: the extra `say` turn counts against the 240 s row cap (`T/dry_world.py:1075`); over it -> FAIL naming the phase
    (EW23, existing). Headroom not measured; the gates run reports per-row seconds.
12. **The chosen heading is cut from the conductor's prompt (F1).** `_conductor_text` appends `## The person's choice` LAST
    (`S/driver_conductor.py:687`), and the whole text goes into the prompt's `## The refusal` cut at 6000 characters
    (`:320`); at a gate the chosen call's text is the details file (`S/driver_machine.py:2443-2448`). The stub reads the heading
    as a LINE EQUAL to `## The person's choice` ANYWHERE in the prompt (not the last heading: four sections follow it,
    `S/driver_conductor.py:320-325`). If the heading is cut, the stub journals `chosen: false` and C2 FAILs on `gate_A/rework`.
    That red is a PRODUCT finding (the person's choice can be cut from the conductor's prompt, FR-8), reported with
    `prompt_chars`, never set `live_only` as a stub gap. Invariant: a call the driver did not mark as the person's choice is
    never excused.
13. **A `## ` heading inside our own words** (adversarial input of F-2): the `say` grammar and the row words refuse a line starting
    `## `; fixtures are ours. Error direction: a misread can only hide an unread call behind a heading in OUR words, which the
    loader refuses.
14. **An n/a declaration on an ask that turns out priced/offered**: guard FAIL as §4. Invariant: a declaration never hides a red.

## 8. Test rows (docs/TESTING.md: the scenario part is the test; pure judges get table rows; no new test file)

All rows are added to the existing selftest tables of the owned files.
- `T/dry_exits.py` judge table (`:2593-2607`; the `good` facts `:2585-2587` take `priced_window`, `ask_ordinal` instead of
  `priced_at_ask`; rows `:2600-2602` re-expressed over `priced_window`): (1) K15 window has only an earlier key -> FAIL
  `key not observed`; (2) K15 window record of the key, `asked.offered` holds a token outside the rows -> FAIL; (3) K15 n/a, ask
  without `offered` -> detail carries `n/a K15`, not FAIL; (4) K15 n/a, ask WITH `offered` -> FAIL `declared n/a`; (5) C2 offered
  from `asked.offered` wins over the window record; (6) C2 a `chosen` conductor call is not counted; (7) C2 a conductor call in a
  LATER post-answer turn (beyond `first`) is not counted (B1); (8) C3 n/a on a token whose price row says `stages_again` ->
  FAIL `C3 declared n/a but the price row of rework says factory stages_again` (B5); (9) C3 n/a on `retry` (`factory: nothing`)
  -> detail `n/a C3`, not FAIL; (10) a window holding only a `prompt: true` record of the key -> FAIL (B3).
- `T/dry_exits.py` loader cases (beside the existing `walk_row_problems` cases): C2 n/a on a token row -> refused; a check both
  listed and n/a -> refused; `na` with a blank why -> refused; `say` grammar: a missing key, blank words, stage outside S0..S9, a
  words line starting `## `, words whose first line is `approve` -> refused (F4); a good `say` recipe -> accepted.
- `T/dry_exits.py` `--check`: the NUMBER list gains `na: <n> declarations (<check> <count>, ...)   [recount: python -B -c "import
  json, glob; print(sum(len((r.get('expect') or {}).get('na') or {}) for f in glob.glob('tests/fixtures/stories/dry-1/exits/*.json')
  for r in json.load(open(f))['rows']))" in scripts/]` (F9, visibility only). A selftest case beside `:1774` checks the count on
  a two-row table.
- `T/dry_world.py` / `T/dry_exits.py` `run_seed` cases (beside `T/dry_exits.py:2575-2581`, fake `drive_fn`): `say` reached when
  the next ask is the same kind and stage and carries `offered`; not reached when it carries none; not reached when the pending
  ask before is another question; not reached when the new ask is another kind (F4).
- `run_exit_row` post-answer end (§6), with a fake `drive_fn`: a turn that raises a different ask ends the turns, `exhausted`
  unset; three identical asks still set `loop`.
- `T/dry_stub.py` spy rows (`:1376-1381`), sink moved under `tmp/<case>/state/dry-priced.jsonl` (F7): (a) no questions file ->
  record `{"key": "s1.gap", "answers": ["go on", "stop"], "q": 0, "prompt": false}`; (b) a questions file of 2 rows in
  `tmp/<case>/state/driver-questions.jsonl` -> `q == 2`; (c) the spy called from inside a function named `_conductor_text` ->
  `prompt: true`; (d) the guard of §3 item 4 (`_conductor_text` exists and is the only caller of `self.gate_prices(`, with its
  positive control).
- `T/dry_stub.py` conductor branch: a prompt carrying a line equal to `## The person's choice` (not last) journals
  `chosen: true`; one without journals `chosen: false`; both journal `prompt_chars == len(prompt)`.
- The scenario: `test_scenario_dry_1.py --part exits:gates` is the behaviour test of the twelve rows; `--part exits:s0` and
  `--part exits:s1-s4` show the merged groups unchanged (B4).

## 9. Census, ratchet, probes (`T/fixtures/driver-exits/gates.json`)

- The twelve rows keep `reach: story`; no census entry changes; `ratchet` unchanged; `live_only` raised_by entries unchanged
  (the FV1-8 entry stays). `dry_exits.py --check` stays `0 discrepancies`.
- **Probe, step 1 (do FIRST, one row run, after the merge and the spy change):** run `gate_A/approve` alone and print its window
  and `asked.offered` (§5, B3 (b)); write them in the report.
- **Probe, step 2 — rework.** The row's `stub.conductor` is a verdict as written (`conductor_verdict` prints a control with
  `options` as is, `T/dry_stub.py:97-99`): `{"action": "ask_person", "question": "...", "why_person": ..., "checked": ...,
  "options": [<one option>]}`, where the one option is `move_option("rework_stage", "rework")` (`T/dry_stub.py:74-88`; its price
  lines are copied as data, never typed) plus `args` from the closed list the chosen prompt prints under `## Moves open here`
  (stage, role, cases|rows, cause, `S/driver_conductor.py:332`). If no such control yields a recorded `seam_rework` within the
  cap, the builder sets `gate_A/rework` and `gate_B/rework` to `live_only` with the measured why, adds one `raised_by` entry each
  (`live_only | walk/gate_X/rework | <why>`), and reports; then `gate_A`/`gate_B` are not in `dry_exits.driven_keys()`
  (`T/dry_exits.py:885-896`) and N4c keeps their `PINNED_ELSEWHERE` entries. **Exception (F1):** a red on C2 with
  `chosen: false` is first checked against the prompt the stub received: if the heading is absent (cut), it is a PRODUCT finding
  (edge 12), reported with `prompt_chars`, and the row stays `reach: story` and red — never `live_only`.
- No `known_red/gates.json` row is written by this card: a row still red is reported with its evidence; the Lead labels.

## 10. Lead decisions on forks F-1..F-5 (17.11.2026, by recommendation, until the owner's word)

Decided by the Lead in the owner's absence, each by the r1 card's recommendation with the plan critic's condition (t-1054,
section "Forks"). Each is a requirement of this card. None of the conditions makes its recommendation unworkable.

| fork | decision | condition (critic t-1054) -> requirement here |
|---|---|---|
| F-1 | (b) drive to the seam question | B1, B3, B4 edited in: §4 C2 cut + §6 turn end; §3 `prompt` stamp + §5 road; DoD (7) |
| F-2 | (a) the stub journals `chosen` | F1: a line equal to the heading anywhere (§7 edge 12, §8); a cut heading is a product finding, never `live_only` (§9); `prompt_chars` journalled |
| F-3 | (a) `expect.na: {check: why}` | B5: C3 n/a guard (§4) besides the K15 and C2 guards |
| F-4 | (a) `free words` judged on the seeded ask: K15 + C6, C2 and C3 n/a with why | the PASS line prints its two n/a (§4). No residual: the critic showed (b) would judge the seed road a second time, so F-4 (b) is NOT queued |
| F-5 | (a) C3 n/a on `retry`/`stop` for this card | B5's guard (§4); the n/a why says the unchanged-state check is F-5 (b), queued at a named finding (R1-a, §11) with its pile, not "as a finding" |

## 11. Forks returned (new in r2; the card is executable by each recommendation)

- **F-6. How the post-answer turns end (§6).** The critic's B1 edit (C2 cut) does not make `gate_A/retry` green: the always-check
  `turns` still FAILs on `exhausted` (§6 trace). Options: (a) end the turns at a new ask that is not `same_ask` as the judged ask
  (general, one road for every group; may change outcomes of merged rows that today pass only by re-sending their answer to a
  different question — DoD (7) shows any change); (b) end the turns at the first new ask only for a token whose price row says
  `factory: nothing` (data-driven, narrower, still one road via the price data); (c) declare `turns` n/a on `retry` (a fourth
  n/a check; hides the walker's own artefact as a product fact). Recommendation (a): the invariant "the answer is sent only to
  the ask it was written for" is the same for every row; (b) leaves the same defect on every other row. Cost of (a): one branch
  in `run_exit_row`, one fake-driver case, the B4 runs (already owed).
- **F-7. Who writes the residual findings (rule 6: every producer has an owning node).** Residuals of this card: R1-a (F-5 (b):
  C3 data-driven for `factory: nothing` — the fingerprint must stay UNCHANGED), R1-b (`main_pass` takes `questions[-1]` as the
  ask, `T/dry_world.py:928`; F5), R1-c (the default stub conductor offers `rework` with no `args`, so every seam call through the
  default stub ends in the code fallback and files a `defect_found`; B3 analog). Options: (a) node **R1 — Lead, at acceptance of
  this card's builder node**, owns: three finding files under `C:/QAFactory/forge-repo/plans/piles/live-run-fvf/findings/`
  (names `20261117-p1b-walker-c3-factory-nothing.md`, `20261117-p1b-walker-main-pass-newest-row.md`,
  `20261117-p1b-stub-rework-no-args.md`), one row each in an UNTAKEN batch of `live-run-fvf` (batch 1 or 2, TEAMWORK §2; batch 3
  is taken) and the card's «Содержание» rows (`plans/piles/live-run-fvf/README.md`); texts: the "what to change" lines of this
  section; (b) the builder writes the three finding files in its owns (on the gates branch) and the Lead adds the batch and
  «Содержание» rows — splits one producer over two moves, and a finding with no «Содержание» row fails
  `tools/test_pile_cards_contents.py` on the branch. Recommendation (a). Not queued: F-4 (b) (§10).
- **F-8 (question, small). The gate-A-only word `approve as is`** (`R/gate-approval-words.json:4`) is walked by nothing (critic
  t-1054 key 4). It is not a price key, so axis 38 does not list it. Options: (a) a fourth finding R1-d in node R1; (b) out of
  scope. Recommendation (a): one line, no cost now.

## 12. The card (header-ready)

given: this file `C:/QAFactory/forge-repo/docs/tasks/specs/20261117-p1b-gate-ask-judge-card-r2.md`; the N2h-v merge sha (the dispatch names it, §0); `C:/QAFactory/forge-repo/.claude/worktrees/agent-a4aebd95c3ca7d59c/docs/tasks/specs/reports/20261117-p1b-n4-gates-report.md` (sections "Walker defects noticed", "Walker fix"); `C:/QAFactory/forge-repo/docs/tasks/specs/20261114-p1b-n4w-exit-walker-spec.md` (K15, C2 F-W7, C3, C6, EW17-EW24); `C:/QAFactory/forge-repo/plans/builder-rules.md`; `C:/QAFactory/forge-repo/ai-packages/qa-factory/design/factory-rules.md`; `C:/QAFactory/forge-repo/docs/TESTING.md`; `C:/QAFactory/forge-repo/tools/architecture_gate.py` (commit-line grammar); read-only code in the tree: `scripts/driver_gates.py`, `scripts/driver_conductor.py`, `scripts/driver_machine.py`, `scripts/driver_dialog.py`, `scripts/driver_journal.py`, `scripts/driver_runner.py`, `scripts/no_move.py`, `scripts/gate_brief.py`, `references/question-prices.json`, `references/gate-approval-words.json`
owns: C:/QAFactory/forge-repo/.claude/worktrees/agent-a4aebd95c3ca7d59c/ai-packages/qa-factory/scripts/tests/dry_driver.py
C:/QAFactory/forge-repo/.claude/worktrees/agent-a4aebd95c3ca7d59c/ai-packages/qa-factory/scripts/tests/dry_world.py
C:/QAFactory/forge-repo/.claude/worktrees/agent-a4aebd95c3ca7d59c/ai-packages/qa-factory/scripts/tests/dry_exits.py
C:/QAFactory/forge-repo/.claude/worktrees/agent-a4aebd95c3ca7d59c/ai-packages/qa-factory/scripts/tests/dry_stub.py
C:/QAFactory/forge-repo/.claude/worktrees/agent-a4aebd95c3ca7d59c/ai-packages/qa-factory/scripts/tests/fixtures/stories/dry-1/exits/gates.json
C:/QAFactory/forge-repo/.claude/worktrees/agent-a4aebd95c3ca7d59c/ai-packages/qa-factory/scripts/tests/fixtures/stories/dry-1/seeds/gates.json
C:/QAFactory/forge-repo/.claude/worktrees/agent-a4aebd95c3ca7d59c/ai-packages/qa-factory/scripts/tests/fixtures/driver-exits/gates.json
C:/QAFactory/forge-repo/.claude/worktrees/agent-a4aebd95c3ca7d59c/docs/tasks/specs/reports/20261117-p1b-gate-ask-judge-report.md
non-goals: any file under `scripts/` outside `scripts/tests/` and anything under `references/` (no production change, including the cut of the chosen heading: a product finding, reported); rows of other groups (s0, s1-s4, s5, s6-s9: they inherit the identity rule, the C2 cut and the turn end automatically; their gate key rows take the `say` form in their own nodes); `main_pass` at `dry_world.py:928` (finding R1-b); the default stub conductor's `rework` without `args` (finding R1-c); C3 for `factory: nothing` (finding R1-a); `test_conductor_doors.py` / `PINNED_ELSEWHERE` (N4c); `known_red` labels (Lead); finding and pile files (node R1, Lead); the walker defects 2-4 of the gates report; files the merge of `origin/main` brings (not edited)
handoff: `C:/QAFactory/forge-repo/.claude/worktrees/agent-a4aebd95c3ca7d59c/docs/tasks/specs/reports/20261117-p1b-gate-ask-judge-report.md`: the merge result (sha, conflicts and how kept), the probe outputs (§9 steps 1-2), the row table (row -> seed reached -> outcome -> seconds), the before/after outcome lines of `exits:s0` and `exits:s1-s4`, the verbatim witness outputs, the FR walk, the commit lines, analogs noticed
edges: §7 items 1-14, each with its invariant; §3 item 4 (adversarial inputs; error direction: false red allowed, false green not); §4 n/a guards; §6 turn end; limits: `POST_TURNS` 4, the 240 s row cap, the prompt cut at 6000 characters (edge 12); empty/absent: no price file (edge 1), no question row (edge 8), empty offered (edge 4), no S8 snapshot (edge 7), records without `q` (edge 6); conflicting pairs: "a token is always C2-judged" vs `rework`'s own conductor call (resolved by `chosen`, F-2), "re-send the answer for C5" vs "never answer another ask" (resolved by §6, F-6)
DoD: (0) §0 steps 1-2 done, `git -C <tree> merge-base --is-ancestor <N2h-v sha> HEAD` exits 0; (1) §3 implemented through one helper `ask_window`; `priced_at_ask` gone, `priced_window` + `ask_ordinal` in its place; spy fields `q`, `prompt`; (2) `say` step and its loader per §5; (3) checks, C2 cut and the three n/a guards per §4, the turn end per §6, the stub fields `chosen`/`prompt_chars` per §7 edge 12; (4) the twelve gate rows and the FV1-8 row exactly per §4 "Row data", the two recipes per §5; (5) table rows per §8; witness, run ONCE on the final state, each output verbatim in the report: `python -B C:/QAFactory/forge-repo/.claude/worktrees/agent-a4aebd95c3ca7d59c/ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <the seven package owns above>` and every file it prints; `( cd C:/QAFactory/forge-repo/.claude/worktrees/agent-a4aebd95c3ca7d59c/ai-packages/qa-factory && python -B scripts/tests/dry_exits.py --selftest )` -> all cases ok; `( cd C:/QAFactory/forge-repo/.claude/worktrees/agent-a4aebd95c3ca7d59c/ai-packages/qa-factory && python -B scripts/tests/dry_stub.py --selftest )` -> all cases ok; `( cd C:/QAFactory/forge-repo/.claude/worktrees/agent-a4aebd95c3ca7d59c/ai-packages/qa-factory && python -B scripts/tests/dry_exits.py --check )` -> `dry_exits --check: 0 discrepancies` and a `NUMBER na:` line; (6) test: ONE run of `( cd C:/QAFactory/forge-repo/.claude/worktrees/agent-a4aebd95c3ca7d59c/ai-packages/qa-factory && python -B scripts/tests/test_scenario_dry_1.py --part exits:gates )` (about 11 minutes, not re-measured) in which `gate_A/{approve,retry,stop,free words,empty}` PASS (the `retry`, `stop`, `free words` lines print their n/a), `gate_A/rework` PASS or `live_only` per §9 or red as a product finding per edge 12, `gate_B/*` per §7 edge 7 (W1: NOTE `after:<node of the stopping main/* row in known_red.json at run time>`; W2: the gate_A expectations), the `outcomes` line PASS; (7) test: ONE run each, BEFORE (after the merge, before any edit) and AFTER (final state), of `( cd C:/QAFactory/forge-repo/.claude/worktrees/agent-a4aebd95c3ca7d59c/ai-packages/qa-factory && python -B scripts/tests/test_scenario_dry_1.py --part exits:s0 )` and `( cd C:/QAFactory/forge-repo/.claude/worktrees/agent-a4aebd95c3ca7d59c/ai-packages/qa-factory && python -B scripts/tests/test_scenario_dry_1.py --part exits:s1-s4 )`: every row's outcome AFTER equals its outcome BEFORE; any change is reported with both lines, not labelled; (8) a row still red is reported with its verbatim line, not labelled; (9) commit lines per §2
siblings: axis 34 (one action, one road): the gate key rows of groups s5 and s6-s9 reach the gate's priced question by the same `say` form in their own seed files (their nodes); every key row of every group reads its ask's window, the C2 cut and the turn end (automatic: one helper, one loop); axis 38: census unchanged, N4c `PINNED_ELSEWHERE` stays while `rework` is `live_only`; inside the artifact: the sweep of §13 (applied: `dry_world.py:1153-1154`, `:1243-1244`, `:1251`, `:1279`, `dry_exits.py:1316`, `:1384`, `:2585`, `:2600-2602`, `dry_stub.py:1376-1381`; queued: `dry_world.py:928` -> finding R1-b; n/a: `dry_world.py:1024`, `:1131`); the prompt-record class applies to every key row whose ask is raised in a turn that built a gate-priced conductor prompt and is fixed once in the spy
designer: C:/QAFactory/forge-repo/docs/tasks/specs/20261117-p1b-gate-ask-judge-card-r2.md

## 13. Sweep inside the same artifact (F5; enumeration, one verdict per neighbour)

Class: "the newest row/record is taken as THIS ask's". Searched with the Grep tool for `priced|questions\[-1\]` in
`T/dry_world.py` and `priced_at_ask|\[-1\]` in `T/dry_exits.py` (positive control: the known sites `:1243-1244` and `:1316`
were found).

| neighbour | what it reads | verdict |
|---|---|---|
| `T/dry_world.py:928` (`main_pass`: `asked, q = len(questions), questions[-1]`) | newest question row as the ask | queued: finding R1-b (main pass is a non-goal of this card; a deferred row is not pending, `S/driver_dialog.py:429-433`) |
| `T/dry_world.py:1024-1025` | the SET of all price keys, printed as a `main/priced` NOTE | not applicable: a note, judges nothing (it will list prompt keys too; stated) |
| `T/dry_world.py:1131` (`counts`) | the number of records | not applicable: a count, no attribution |
| `T/dry_world.py:1153-1154` (`_holds`) | `priced[-1]` | applied: `ask_window` |
| `T/dry_world.py:1243-1244` | `priced[-1]` as `priced_at_ask` | applied: `priced_window` + `ask_ordinal` |
| `T/dry_world.py:1251` (`_ask_of(questions[-1])`) | newest row as the judged ask | applied: the identified row |
| `T/dry_world.py:1279` (post-answer ask) | newest row as the new ask | applied: the identified row of the then-pending ask |
| `T/dry_exits.py:1316` (`_check_c2`) | `priced_at_ask` | applied: the window |
| `T/dry_exits.py:1384-1388` (K15) | `priced_at_ask` | applied: the window |
| `T/dry_exits.py:2585`, `:2600-2602` (selftest facts) | `priced_at_ask` | applied: re-expressed |
| `T/dry_stub.py:1376-1381` (spy selftest) | the record shape | applied: `q`, `prompt`; sink under `state/` |
| `T/dry_exits.py:416` | a parser's own stack | not applicable: not an ask |

## 14. Small technical choices closed by the designer

- The identity counts question rows through `driver_journal.question_rows` (the one reader), not by counting lines.
- `ask_window` lives in `dry_world.py` (the world reads files; `judge_row` opens none, `T/dry_exits.py:1402`).
- `priced_at_ask` is replaced, not kept beside the window (one fact, one name).
- The prompt stamp walks frames with `sys._getframe`, not `inspect.stack()` (no source read per call).
- The `say` turn uses `--max-boundaries 60` like `drive_until`'s turns.
- Seed words: "Before approving, add a case for the empty cart." (ASCII, first line not an approval word, usable as a rework
  instruction).
- Recipes are repeated per group seed file (seeds are per group by the loader, `T/dry_exits.py:1238-1256`).
- The stub journal key names `chosen` and `prompt_chars`; the conductor's journal line keeps every existing key.
- The `na` NUMBER line is added (F9), not a ratchet.

Noticed analogs (reported, scope not widened): (1) R1-c, the default stub's `rework` without `args` (every seam call through
the default stub files a `defect_found`); (2) `approve as is` unwalked (F-8); (3) the floor after a rendering failure keeps a
priced record (§3 item 4, last bullet) — K15 does not claim the person saw price lines.

## 15. Readers of every touched file (designer rule 7)

Commands (Grep tool) and hit counts, this round:
- pattern `dry_exits|dry_world|dry_driver|dry_stub|dry-priced|seeds/gates|exits/gates|driver-exits/gates|priced_at_ask|passing_spy|conductor_calls`
  over `C:/QAFactory/forge-repo/tools`: 3 hits in 1 file, `tools/test_workflows.py:348` (CI `tables` job runs
  `dry_exits.py --check`, `dry_stub.py --selftest`, `--part exits:selftest`) — **unchanged** (no CLI or file name changes; the new
  NUMBER line is not parsed: `report.numbers` is only printed, `T/dry_exits.py:2768-2769`, `T/test_scenario_dry_1.py:30-31`).
- same pattern over `.githooks`: 0 hits; positive control `python|tools/` in the same folder: 22 hits in 4 files.
- same pattern over `.claude/agents`: 0 hits; positive control `scenario_walk|handoff`: 10 hits in 3 files. Over `.claude/skills`:
  0 hits. `.claude/settings.json` for `dry_exits|dry_world|dry_driver|dry_stub|python`: 41 hits, all `python` (hook commands);
  0 for the dry files — **unchanged**.
- inside the package (`<tree>/ai-packages/qa-factory/scripts`), pattern `dry_exits|dry_world|dry_driver|dry_stub`: 136 hits in
  13 files: the four owned files; `T/test_scenario_dry_1.py` 24 (calls `walk_exits`, prints `report.numbers`; signatures of
  `run_exit_row`/`judge_row` unchanged) — **unchanged**; `T/test-layers.json` 5, `T/fixtures/driver-layers.json` 2,
  `T/fixtures/driver-exits/s1-s4.json` 6, `T/fixtures/driver-exits/classes.json` 1, `T/fixtures/stories/dry-1/exits/s1-s4.json` 3,
  `.../exits/gates.json` 1 (owned), `T/fixtures/stories/dry-codemie-14857/tracker/routes.json` 1 (file names / prose only) —
  **unchanged**; `T/test_question_lines_unread.py` 5 (a local variable named `dry_stub`, not the module) — **unchanged**.
- changed names `priced_at_ask|passing_spy|conductor_calls|dry-priced|SEED_STEP_KEYS|dry_world\.row_facts` over the same folder:
  174 hits in 33 files; outside the four owned files the hits are a different symbol `conductor_calls` of the driver tests
  (`story_run_common.py`, `test_story_run_*`, `no_move_seam_common.py`, ...) and driver prose — **unchanged** (this card keeps the
  facts key name `conductor_calls`; only `dry_exits` reads the dry facts key).
- parallel streams meeting these files: N2h-v at `dry_stub.py` (§0: dispatched after its merge, merged in first); FV3-14
  (`_count_reach`) and N3a at `dry_exits.py` per the finish spec — **changes in those streams**, sequenced after this card;
  `dry_driver.py` record shape is read by `dry_world.py:1024` (keys only) — **unchanged**.

## 16. Reading trail

Read this round in `<tree>`: `T/dry_world.py` 1095-1300 (`answer_bytes`, `pending_ask`, `counts`, `row_facts`, `_holds`,
`run_seed`, `_ask_of`, `run_exit_row`), grep 714-716, 798-807 (`loop_problem`), 928, 1024, 1075-1076; `T/dry_driver.py` 1-83
whole; `T/dry_exits.py` 646-677 (`check`), 846-882 (`_numbers`), 938-987 (`state_fingerprint`), 1004-1009 (`same_ask`),
1085-1256 (expect/answer/seed loaders, `_seed_problems`, `load_seeds`), 1280-1282 (`_norm`), 1300-1438 (`_check_*`,
`_judge_always`, `judge_row`), 2750-2782 (CLI), grep 64-68, 885, 2585-2602; `T/dry_stub.py` 50-124 (`parse_moves`,
`move_option`, `conductor_verdict`), 890-920 (conductor branch), 1368-1397 (spy selftest);
`T/fixtures/stories/dry-1/exits/gates.json` whole; `.../seeds/gates.json` whole; `T/fixtures/driver-exits/known_red.json`
whole (tree and main checkout); `T/fixtures/judgment-census.json:3` (`about`, by grep); `T/scenario_walk.py` grep
`witness-for`; `T/test_scenario_dry_1.py` grep `--part`; `S/driver_conductor.py` 315-349, 460-790, grep of `def`;
`S/driver_dialog.py` 395-494; `S/driver_journal.py` 385-400; `S/driver_gates.py` 1096-1120; `S/driver_machine.py` 2385-2450,
3376-3407, 3596-3609; `R/question-prices.json` 140-155; `R/gate-approval-words.json` whole; `plans/builder-rules.md` 7a-7d;
`plans/piles/live-run-fvf/batch-3-live-run-fvf.md` grep N2h; the N2h-v card 1-40; the r1 card whole; the critic verdict whole.

Taken from the critic's trail, not re-read (marked "per critic trail" where used): `S/no_move.py:231-232` (`check_args`),
`:612-626` (`priced_options` refusal); `S/driver_dialog.py:600-629` (`held_question`); `S/driver_gates.py:136-141`, `:322`;
`S/driver_dialog.py:321`.

NOT read (claims depending on them are probes or stated as such): whether the `rework` lone-option control passes `check_args`
with the dry world's facts (probe §9 step 2); the gate A packet length (edge 12, decided by the run); `walk_exits` `after:` logic
(edge 7 reads the label at run time); `combine_gate_words` and gate B's stand-gap/exploratory readers on the seed words; the
240 s headroom with the extra `say` turn; the duration of the `exits:s0` / `exits:s1-s4` parts.

## Fix round t-1057

| # | finding (t-1054) | what changed | where in r2 |
|---|---|---|---|
| 1 | B1 retry red from the re-sent answer | C2 counts conductor calls only in the answer's own turn (up to the first new question row); the turn-end rule closes the second red the critic's trace missed (`turns` exhausted), returned as F-6 with recommendation | §4 "C2 cut", §6, §8 rows (7) and the post-answer case, F-6 in §11 |
| 2 | B2 FV1-8 row contradicts the guard | row becomes words `approve`, checks C3/C6, n/a K15 and C2 with whys; both guards hold | §4 "Row data", last bullet |
| 3 | B3 K15 (i) satisfied by the prompt record; road not pinned | spy stamps `prompt`; window excludes prompt records; old adversarial bullets 2-3 dropped; the seed's road (code fallback, one `defect_found` per row) stated and measured by probe step 1; rename guard | §3 items 1, 3, 4; §5 "Which road"; §7 edge 3; §8 rows (10), spy (c)(d); §9 step 1 |
| 4 | B4 merged groups not shown green | DoD (7): before/after runs of `exits:s0` and `exits:s1-s4`, exact commands, equal outcomes | §0 step 3; §12 DoD (7) |
| 5 | B5 C3 n/a unguarded | C3 n/a legal only with no token or a `factory: nothing` price row; whys re-worded to point at F-5 (b) | §4 guards and per-variant table; §8 rows (8)(9) |
| 6 | B6 TEMPORAL `after:FV3-5` | both worlds stated (W1 label read at run time, W2 S8 exists); the move that changed the label (N2h-b2) and the move that makes S8 named | §7 edge 7; §12 DoD (6) |
| 7 | F1 heading wording and cut prompt | "a line equal to the heading anywhere"; cut heading = product finding, never `live_only`; `prompt_chars` journalled | §7 edge 12; §8 stub rows; §9 exception |
| 8 | F2 K15 (ii) tautology | (ii) labelled shape, with the reason; observations are (i) and (iii) | §4 K15 row; §2 table |
| 9 | F3 wrong `words: null` reason | reason corrected: `answer_bytes` writes `token\nwords`, the driver compares the whole answer | §4 "Row data", first bullet |
| 10 | F4 `say` reach too wide; approval words | reached only if the pending ask is still the same kind at the same stage; loader refuses approval-word first lines | §5 grammar and step 3; §8 loader and run_seed cases |
| 11 | F5 siblings inside the artifact | enumeration with a verdict per neighbour; `:1279` applied, `:928` queued as R1-b | §13; §3 item 3; §12 siblings |
| 12 | F6 re-raised asks unpriced | new edge with its FAIL text and invariant | §7 edge 10 |
| 13 | F7 spy task root | `task_root = sink.parent.parent`; selftest sink under `tmp/<case>/state/` | §3 item 1; §8 spy rows |
| 14 | F8 citation | the chosen call cited at `S/driver_machine.py:2446` | §4 per-variant table (`rework`) |
| 15 | F9 n/a invisible to ratchets | `NUMBER na: <n>` line with its recount command (visibility, not a ratchet) | §8; §2 table; §14 |
| 16 | F10 `dry_stub.py` shared with N2h-v | dispatched only after N2h-v is merged; the builder first merges `origin/main` and keeps both sets of rows | §0 steps 1-2; §12 DoD (0); §15 |

## Lead decisions on forks F-6..F-8 (17.11.2026, by recommendation, until the owner's word)

- **F-6 — (recommended).** The walker stops the post-answer turns at a new ask that is not the same as the judged one (§6). Because this
  changes how the `turns` check is reached for every walked row, §6 gets a narrow plan-critic pass (t-1060) before the builder is dispatched.
- **F-7 — (recommended).** A Lead node R1 at acceptance writes the finding files R1-a/b/c, their rows in an untaken batch of `live-run-fvf`
  and the «Содержание» rows.
- **F-8 — (recommended).** `approve as is` walked by nothing is recorded as a finding by the same node R1; the card does not walk it.
- F-4 is not queued (the designer's evidence: the critic's own Forks table says (b) would judge the same road twice).

## Binding edits after the narrow plan critic t-1060 (17.11.2026; accepted by the Lead)

The findings below are quoted whole from `docs/tasks/specs/reviews/t-1060-p1b-gate-ask-judge-r2-turns.md`. Every "Exact edit" in them is PART OF THIS CARD: where it replaces or extends a sentence of §6, §8, §9 or DoD (7) above, the text here holds and the older sentence does not. The builder implements §6 WITH G1 (the `ended_at` fact and the armed `turns` rule), G2 (the position and its invariant), G3 (the three edges of "the same ask"), G4 (the four control cases and judge row (11)) and G5 (which flips fail the node and which are reported). N1 corrects one sentence of §6. `T/` and `S/` in the quotes are the card's own abbreviations for `scripts/tests/` and `scripts/`.

### G1 — §6 removes the `turns` backstop and puts nothing in its place (fix before dispatch)
The code: the loop `T/dry_world.py:1263-1286` sets `exhausted` only through `for ... else` (`:1285-1286`), that is, when 4 turns each wrote a new question, `fp_after == fp_ask` every time, and there was no loop. `_judge_always` fails `turns` on it (`T/dry_exits.py:1397-1398`) for EVERY row, whatever its listed checks. So today `turns` is the one always-check that says "the answer moved nothing". It acts for rows that do not list C3.
§6: "The `exhausted` flag is not set when the turns end by this rule." After the change, a row whose answer leads to a different question with the state unchanged ends at turn 1, gets no `exhausted`, and is judged only by its listed checks. The §6 error-direction paragraph says "fewer turns can only show an unchanged fingerprint ... (C3 false red)". That is true for a row that lists C3. It is false for a row that does not list C3 and declares no n/a. The loader allows such a row: only an EMPTY `checks` is refused (`T/dry_exits.py:1117-1118`). The C3 n/a guard of §4 acts on a DECLARATION, not on an omission. So "a token whose data expects the state to move is always C3-judged" does not hold for a row that simply leaves C3 out.
Concrete false-green input (future s5/s6-s9 key rows, which inherit §6 "automatically", §12 non-goals): a row with `checks: ["C2"]`, a token whose price row says `stages_again`. The product answers by raising a DIFFERENT question and records nothing (a dead end dressed as a question). §6 stops at turn 1 and C2 passes, so the row is PASS. Today the walker keeps re-sending, the asks alternate, and the row ends `exhausted` -> `turns` FAIL.
No walked row today is in this shape (key 2), so this is a class gap, not a flip of an existing row.
Exact edit, §6, replace the sentence "The `exhausted` flag is not set when the turns end by this rule." with:
> "When the turns end by this rule, `run_exit_row` sets `facts["ended_at"] = {"turn": <n>, "kind": <kind>, "stage": <stage>}` instead of `exhausted`. `_judge_always` FAILs `turns` with `<row id>: the answer moved nothing and the next ask is another question (<kind> at <stage>, turn <n>); C3 is neither listed nor declared n/a` when ALL of these hold: `ended_at` is set, `fp_after == fp_ask`, and the row neither lists C3 nor declares C3 n/a. A listed C3 judges the same fingerprint itself. A C3 n/a that passed its guard (§4: no token, or `factory: nothing`) is data saying the state does not move. Invariant: **a stop at a different ask never counts as the state moved**. The outcome detail of a PASS or NOTE whose turns ended this way prints `ended at <kind> at <stage> after turn <n>`."
Also edit the error-direction sentence to: "fewer turns can only show an unchanged fingerprint where a later re-sent turn would have changed it (C3 false red, allowed); the `turns` always-check stays armed for a row that does not judge C3 (above)."
Add to §8 the judge-table row (11): "`ended_at` set, `fp_after == fp_ask`, checks `["C2"]`, no `na` -> FAIL `turns ... C3 is neither listed nor declared n/a`; the same facts with `na: {"C3": ...}` on a `factory: nothing` token -> not FAIL".
Gate rows under this edit: `retry` (C3 n/a, guard holds) and `free words` (C3 n/a, no token) stay green. `approve` and `rework` list C3. `stop` (held, same ask, so no §6 stop) is unaffected.

### G2 — POSITIONAL: §6 does not say where the stop sits in the loop (fix before dispatch)
CLAUDE.md rule 11 (ii) requires this. The loop body, in order (`T/dry_world.py:1264-1284`): run; `post_turns`; outputs; cap; fingerprint (`fp_after`); questions; `now`; whys appended (`:1274-1275`); the no-new-row break (`:1276-1277`); `asked_count`; asks appended (`:1279`); rehearse (`:1280-1281`, C6); `loop_problem` (`:1282`); the fp/loop break (`:1283-1284`). If a builder puts the §6 stop right after `:1277`, the stopped turn loses several facts:
- its asks entry is not appended;
- its gate rehearsal is not run. For `retry` the stopped ask is the re-shown plain `gate_A`, so C6 silently checks one ask fewer;
- its loop check is not run.
Exact edit, §6, add after the rule: "Position: the test sits in the same `if` as the existing loop/fingerprint break (`T/dry_world.py:1283`), after `fp_after`, the whys of the turn, the asks entry, `rehearse` and `loop_problem` are taken: `if facts["loop"] or fp_after != facts["fp_ask"] or not same_ask(asks[0]["ask"], asks[-1]["ask"]): break` (with `ended_at` set only by the third clause, and only when the first two are false). Invariant: the turn that ends the loop is collected whole. C2 reads its whys, C6 rehearses its ask when it is a gate, C3 reads its fingerprint. The comparison is with the JUDGED ask (`asks[0]`), never with the previous ask."

### G3 — "the same ask" at the §6 site: three edges unstated (fix before dispatch)
§6 uses `dry_exits.same_ask` (`T/dry_exits.py:996-1009`). That identity is (price key or kind, stage, dispatch with its number replaced, normalised SET of offered tokens). It does not compare the text, `question_sha` or the held lead.
- (a) **Equal identity, different question.** Example: a second seam question at the same gate for another reason, with the same option set; or a re-shown plain gate after the answer changed something that is not in the fingerprint. §6 calls it "the same" and re-sends the answer. So the card's absolute invariant "the walker's answer is only ever sent to the ask it was written for" overstates. It holds up to the C5 identity. This is deliberate and right: a held re-raise (`held_question`, `S/driver_dialog.py:600-629`) keeps kind, stage, dispatch and offered (`:620-621`) but changes the text (`lead`). Comparing text would end the turns on every held re-raise, and C5 would never see a product loop of "answer not read" re-raises. Edit the §6 invariant to: "the walker's answer is only re-sent to an ask with the same C5 identity as the judged ask (`same_ask`: key or kind, stage, dispatch without its number, offered set; text not compared, so a held re-raise is the same ask). Residual direction: a different question with an equal identity still gets the re-send. That is the C5 identity's own known merge (its docstring, `T/dry_exits.py:1005-1008`), not a new road."
- (b) **A free-words ask (no `offered`).** Two plain asks of the same kind, stage and dispatch are the same (an empty frozenset on both sides). State: "an ask with no offered tokens is the same as another with none at the same kind, stage and dispatch (a re-shown plain gate is the same ask)."
- (c) **No pending ask after a turn that wrote a row.** A deferred question writes a row and is not pending (`S/driver_dialog.py:429-433`). A turn can also clear `asked`. §3 item 3 now makes `:1279` take "the identified row of the then-pending ask", and there is none. The card is silent on this. State: "a turn that wrote a question row and left no pending ask ENDS the turns (it is not the judged ask). No asks entry is added. `ended_at` is set with kind `none`, and G1's `turns` rule applies."

### G4 — the §8 control does not catch every too-wide §6 (fix before dispatch)
The §8 case "a turn that raises a different ask ends the turns, `exhausted` unset; three identical asks still set `loop`" covers two failures:
- **stopping on the same ask** (too wide): the loop case fails. Good.
- **stopping before the answer is consumed**, or the G2 position: a stop placed before the asks/rehearse/fp collection still ends the turns with `exhausted` unset, so the case passes. Not caught.

Exact edit, §8 `run_exit_row` post-answer end, replace the case with: "(i) a turn whose new pending ask differs from the judged ask, with the fingerprint unchanged: `drive_fn` called exactly once with `--answer`, `post_turns == 1`, `fp_after` equals the fingerprint the fake turn left, `ended_at` set, `exhausted` unset, and with C6 listed and the new ask a gate kind, `gates` holds TWO entries (judged + stopped); (ii) the same with the new ask equal to the judged ask (same kind, stage, offered, other text): the turns go on (turn 2 runs); (iii) three identical asks set `loop`, `ended_at` unset; (iv) a row that wrote a question row and left no pending ask ends with `ended_at.kind == "none"`." Plus the judge row (11) of G1.
Feasibility pointer (no existing case drives `run_exit_row`; it starts with `from_snapshot`, `T/dry_world.py:364-376`): "build the world with the selftest's `fake_world` / `put_state` (`T/dry_exits.py:2524-2535`) and a snapshot dir `world.snaps/<row id>/<start>/` holding `.dry-snapshot.json` with `label` = `dry_world.RUN_LABEL`; the fake `drive_fn` rewrites `driver-state.json` / `driver-questions.jsonl` as `put_state` does."

### G5 — DoD (7) says AFTER == BEFORE, but §6 predicts flips (fix before dispatch)
F-6 text: "(a) ... may change outcomes of merged rows that today pass only by re-sending their answer to a different question — DoD (7) shows any change". DoD (7): "every row's outcome AFTER equals its outcome BEFORE; any change is reported with both lines, not labelled". The pair is a conflict the card does not resolve (rule 11: conflicting requirements). A builder seeing `s1.review/free words` flip from PASS to FAIL C3 cannot tell whether it has to fix its code or report the flip and stop.
Exact edit, DoD (7), append: "A flip whose AFTER line carries `ended at <kind> at <stage> after turn <n>` (G1) is §6 exposing a re-send green: it does not fail this node. The builder reports it with both lines and does not change the row, the stub or §6 for it; the Lead labels. A flip WITHOUT that detail is a defect of this change and is fixed in this node." The same rule goes in §9 for `gate_A/rework`: a C3 red with an `ended at` detail is reported with that line, and is not by itself grounds for `live_only`.

### N1 — §6 "C5 is unaffected" is slightly inaccurate (note)
Today, the sequence judged J, then B, B, B (the walker re-sending J's answer to B) sets `loop` on B,B,B (`T/dry_world.py:798-807`, `:1282`). Under §6 the turns end at the first B. So C5 changes for that sequence. It was a walker artefact (an answer re-sent to a question it was not written for), so the change is right. Edit: "C5 is unaffected for the judged ask: three identical asks of the JUDGED ask still arise and are still caught; a loop of a DIFFERENT ask that only the re-send produced is no longer manufactured."
