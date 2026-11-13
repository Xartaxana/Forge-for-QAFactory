# Critic: P1-b N1 code review — the census of the driver's exits (`dry_exits.py`, `fixtures/driver-exits/`)

Diff: `68c49c6` on `origin/wip/p1b-n1` (parent `8b6dcb4`), worktree `.claude/worktrees/p1b-n1`. The spec (DoD) is
`docs/tasks/specs/20261113-p1b-dry-story-spec.md`: N1 (`:542-565`), §3.2-3.6, E5/E7/E8/E12/E19/E20, and N-L (`:663-677`).
Line numbers below refer to `ai-packages/qa-factory/scripts/tests/dry_exits.py` unless another file is named.

**Verdict: fit_with_fixes (NEEDS WORK).** Nothing here is reject-level. The mechanical layer reproduces exactly. Four
fixes must land before the Lead accepts: F1-F4, two of them holes in the ratchet the node exists for. F5-F7 are cheap and
belong in the same round. F8 is a fork for the Lead, and it has to be settled before N4. F9-F12 are queued, each with its
owner. Acceptance belongs to the Lead.

## Findings

**F1 — E19 diverges from the spec (fix before merge; its form depends on the Lead's answer to Q1).** At `:515-518` a
route of `ask_person` with no `class_source` becomes a NOTE. `--check` still prints `0 discrepancies`. The spec says red
twice: E19 (`:496`), and §3.6 (`:329`, `:332-334`: "строка без него — красное «class unknown»"). The docstring at `:17` and
the `classes.json` `_about` say "printed and counted", which is what the code does, not what the spec says. Surface: the
class resolver. Neighbours walked:
- the `marked_person` route is also `ask_person` (`driver_machine.py:59-60`), and it is not censused at all (F4);
- a `class_source` that resolves to nothing gives `class unknown` correctly (`:402-403`);
- `default: null` behaves correctly.

**F2 — the ratchet's raise door is shared across the four counts and never goes stale (fix before merge; AR-20, the one
stale semantics of axis 18).** At `:501`, `named = len(census["raised_by"])` is one global credit. It is applied to
`live_only`, `after`, `unwalked` and `hook_layer` alike, and nothing refuses a credit nobody uses any more. I probed this on
scratch copies:
- **ca:** `raised_by: ["x"]` and nothing else changed gives `0 discrepancies`. The credit sits there silently, and the next
  unnamed row passes as a NOTE.
- **cb:** one `raised_by` entry legitimises 1 row above the base in `live_only` AND 1 in `unwalked` (two NOTEs, `0
  discrepancies`).

Axis 18 (`SIBLING_MAP.md:391`) asks for "ONE stale/cap semantics": a stale row is refused. The `known_red` pin is
strict in both directions (`known_red.py:114-126`).

Fix: each `raised_by` entry names its count (`"<count>: <who, where>"`). Then for each count require
`count == base + entries(count)`. Above that is red (an unnamed raise). Below it is red ("stale raise credit: drop the
entry or lower the base").

**F3 — a row claiming `reach: seed|story` with no walk row behind it is green (fix before merge; E1/AR-28, and the
census's "both directions").** Section 2 of `check()` (`:489-496`) checks walk row → subject only. Probe **cc**: I added
`routes.story_budget = {"reach": "seed"}` with no walk rows and lowered `unwalked` by 1. The result was `unwalked 86/86`,
`0 discrepancies`. So the cheapest way past the ratchet is to relabel a row `seed`, and a new route can arrive the same way
with no red. Fix: for every census row whose reach is in `EXECUTABLE`, require at least one walk row whose id-subject is
that name. Otherwise it is red: "claims <reach>, no walk row; write the row or set unwalked". Today this is free (all 87
rows are `unwalked`).

**F4 — the routes `match_known` mints itself are outside the census, and a new one would be too (fix before merge; E5).**
`scan_routes` (`:301-318`) imports `KNOWN_REFUSALS` and probes only the "no match → None" branch. `match_known`
(`driver_machine.py:57-60`) returns `marked_repair`/`resume_repair` and `marked_person`/`ask_person` before the table is
consulted at all. A third marker branch would not turn anything red. See Q3.

**F5 — numbers not reproducible from the named command (fix in round).**
- `gate_questions` is the literal `2` at `:434`, not a count. It should come from the `question:` sources of `classes.json`
  that exist in the prices.
- The classes recount command (`:549-550`) prints `len(REGISTRY)` and the number of operations, not 58/19/2.
- `ban_doors 0` has no recount at all.
- "kinds without a key" is recounted by "this file", which is circular.

I reproduced every number independently (see the trail). The commands just need to print what the line claims.

**F6 — AR-13: the "word does not pass" predicate is re-implemented (fix in round).** `ban_doors` (`:418-420`) and
`class_counts` (`:431`) recompute blank `override`. The registry already has its reader, `refusal_registry.unpassable()`
(`refusal_registry.py:1308-1310`). Filter that result by `SCANNED` and non-operation. My control through it: 58 and 0,
the same numbers.

**F7 — code quality (fix in round).** `check()` (`:453-555`) is about 103 lines across six concerns. Split it into
code↔rows, walk subjects, ratchets, classes and ledger, and numbers. `_selftest_cases` (`:736-1211`) is a table and is
acceptable. `TIME_KEYS` (`:51`) plus the `_at` suffix rule is a small closed list in code (AR-1 inside the layer, spec
`:61-63`). It is low-severity, so put it in a comment or a data row of the layer.

**F8 — Lead fork, before N4: the literal "same call" rule produces false keyless kinds (an AR-15 double road).** Seven of
the 21 kinds get their key one statement earlier in the same function:
- `closed_held`, `code_close`, `delivery`, `exit_limit`, `repair_limit`, `report_match`, `ticket_auth`;
- for example, `driver_dispatch.py:3763-3765`: `text = self.closed_question("exit.resume_limit", …)` and then
  `Person("exit_limit", text, …)`.

Under the literal rule, N4 would walk these questions under kind ids as well as under the key that
`test_conductor_doors.py` already censuses. §3.2 forbids exactly that: "driver-exits держит только то, чего та перепись не
знает". The builder's reading is faithful to the spec's letter (`:222`), so this is a spec defect, not a build defect.

**F9 — clone, queued.** `_no_duplicate_keys`/`_read_json` (`:77-94`) is the same strict reader as
`known_red._no_duplicates`/`_read` (`known_red.py:43-70`), and dry_exits already imports known_red. Survivor: the
known_red reader, made public by P1-a's owner. Node for the Lead: `strict JSON reader: dry_exits._read_json -> known_red | узел: <P1-a helper node>`.

**F10 — seam with N2 (node N2).** `dry_stub.py:305-306` hashes the prompt with only its own dispatch id replaced, and
`:312` hashes the conductor prompt raw. `author_input_sha` (`:675-678`) normalises with `DISPATCH_ID_RE` and collapses
whitespace. C5 compares this hash, so there must be one function. Survivor: `dry_exits.author_input_sha`. N2 writes
`prompt_sha` through it.

**F11 — the `architecture:` line omits AR-25, AR-22 and AR-15.** The spec §1 assigns them to N1's DoD (`:49`, `:55`,
`:56`; this node is the AR-25 detector and the producer of `driven_keys` for the AR-15 survivor). Fix the line in the
fix-round commit.

**F12 — owed by the Lead, not the builder.**
- N-L R-L1/R-L2 (axis 18/34/17 lines, brief question 9) must land with N1's merge (AR-20 change check,
  `architecture.md:222`).
- Until N3's test file runs the census, `--check`/`--selftest` sit on no CI path. `canon.yml` runs only
  `dry_world.py --spike`. Item (d) of the commit message states this honestly.

Process notes, not blocking:
- two edits went in through a `python -` heredoc (hygiene pt.4);
- the builder did not read `factory-rules.md`, `builder-rules.md` or `TESTING.md` in full, although PROJECT.md p.1 puts
  them in `given`.

## Answers to the builder's questions (the Lead decides)

**Q1 — E19.** The NOTE reading breaks AR-28/FR-41. The run's summary line, `0 discrepancies`, reports clean while three
classes are unknown, so an unknown sits under a pass. The reading that keeps both AR-28 and FR-41 is E19 as written
(red), with the DoD's "0 discrepancies" reached by naming the sources. The designer's premise (`:332-333`: the source is a
joint check or a registry id) is not verified for these routes. Candidates:
- `readiness` might be `SG-tracker-route` (`refusal_registry.py:254`);
- `story_budget` comes from the controller sentence (`controller.py:6217-6219`);
- `executor` comes from the contract prefix (`contract.py:117`).

Recommendation:
1. Let `class_source` name any `by_source` key directly. That is one branch in `class_of` at `:396-401`.
2. The Lead adds data rows for the three producers, and for `marked_person`, with the class word the Lead chooses (P13:
   the person answers, so "gate" is the natural reading, but that is the Lead's call).
3. E19 stays red for every future `ask_person` route.

**Q2 — the readings.**
- **ratchet = base:** right. It is the AR-20 in-tree model.
- **raise = one `raised_by` per extra row:** right in intent, wrong in mechanics (F2: global, never stale).
- **`hook_layer` = 77 from `hooks.json`:** a right reading of E8/§3.3 ("один счёт"). Note that it makes every new hook
  refusal in the package red here, and the friction is accepted by the spec. Rows with `reach: hook_layer` in group files
  are allowed by `REACH_RE` but not counted. Refuse them as walk rows already are (`:495`).
- **ledger at `fixtures/driver-exits/known_red.json`:** acceptable. P1-a §3.6 (`p1a spec :226-227`) leaves the file to
  P1-b's spec, which named none. The Lead writes the path into spec §3.2 in one line. No overlap with N4's owns
  (`<group>.json` only).
- **keyless "same call", 21 of 29:** faithful to the letter, but it contradicts §3.2's intent (F8). Recommendation: a site
  is keyed when its text argument is a name bound in the same function to an expression that calls
  `closed_question`/`priced_section`. The function-scope approximation leaves 12 keyless kinds plus 2 mixed (`package`,
  `questions`), matching §3.1's expectation ("conductor, refusal, environment, retro, stand_identity и др.").

**Q3 — `marked_repair`/`marked_person`:** these are rows to add, inside the census's universe. They are exits of the same
surface, the refusal router. Read the routes `match_known` mints from its own source: the AST of its literal
`return "<name>", "<action>"` tuples, or probes with `role_cli.REPAIR_MARKER`/`PERSON_MARKER`. AST is preferred, because
a new marker branch then turns red. Expected numbers: 21 + 2 + 2. `marked_person` falls under E19 (Q1).

## Topic questions

1. **One reader:**
   - routes come by import (`:309`), prices through their loader (`:325`), joints through `null_outcomes.load_data(stage_joints.DATA)` (`:335`; `stage_joints.audit` uses the same, `stage_joints.py:604`), kinds through `harness.driver_sources` (`:268`), registry by import;
   - the group files are hand rows, reconciled both ways, which is the design;
   - drift risks: F4 (match_known), F6 (override predicate), `KEYED` (`:47`) mirroring `test_conductor_doors.py:626` `QUESTION_SITE_RE`; that last one is queued with N4c.
   - Numbers: 61/188, 21, 43 (8/8/27), 58/19/25, 29 literal kinds and ban_doors 0 all reproduced independently. Reproducing them from the named commands needs F5.
2. **AR-20:**
   - the ratchet is shrink-only with a named door, but the door leaks (F2), and a route or row can arrive unseen via `seed` (F3) or via a marker branch (F4);
   - control 1 (route removed → red naming it) corrupts what it claims;
   - control 2 lowers the base instead of adding a row, which is equivalent for the inequality at `:502`;
   - control 3 exercises `known_red.reconcile` on a scratch ledger, matching the DoD wording.
3. **AR-29:**
   - no judgment: `class_of` maps source to class from data, and `ban_doors` checks the presence of a field;
   - census class: xref (C1), presence (C4з), shape (fingerprint);
   - `judgment-census.json` needs no rows: `SCAN_EXCLUDE = ("tests",)` (`test_judgment_census.py:67`), and the file is untouched in the diff.
4. **Clones:**
   - `dry_stub`: F10, survivor `author_input_sha`;
   - `known_red`: F9;
   - `refusal_registry`: F6, survivor `unpassable()`;
   - `stage_joints`: no clone, its reader is reused;
   - `dry_world`: no scanner overlap. Its `jsonl`/`question_kinds` are N3's carriers, not re-read here.
   - The clone ratchet output (`forge-check`) was not attached and is not read here; it is batch level.
5. **Tests:**
   - `--selftest` is a layer-3 table inside the helper, with N0 precedent (`dry_stub.py --selftest`);
   - there are fewer test lines than product lines;
   - the cases are behaviours, not self-controls;
   - it would catch the node's main defect (a route with no row) through `check()`, but not F2/F3/F4;
   - add one table row each: stale credit, cross-count credit, a seed row with no walk row, a marker route.
   - Registration: a `keep` row keys only `test_*.py`, so the builder's suggested `dry_exits_census` row is wrong in form. N3's `keep` row for `test_scenario_dry_1.py` (N3 owns `test-layers.json`, spec `:621`) carries `covers` += `tests/dry_exits.py`, `scripts/tests/fixtures/driver-exits`.
   - N-L owes R-L1 (`SIBLING_MAP` axis 18: the four counts plus `raised_by` with F2's semantics; axis 34; axis 17) and R-L2 (brief question 9).
   - A `plans/features.json` row is not required by the spec; the batch's feature id suffices.
6. **N2/N3 unblocked:** yes, apart from F10. The signatures match the spec: `state_fingerprint(task_root, stages=None)`, `same_ask(a, b)`, `driven_keys(walk_dir, prices)` and `load_walk_rows`. N3 must feed `same_ask` dicts with `key|kind`, `stage`, `dispatch`, `tokens|offered`. Walk rows accept `reach: unwalked` (`REACH_RE`), while §3.3 allows only story/seed/live_only/after; N4's DoD wants 0, so refusing it for walk rows is a one-line fix to take in this round.

## Standing lines

- **Fit to spec:** E5/E7/E8/E12/E20 and the §3.4 awkward inputs are implemented. E19 deviates (F1).
- **Builder decisions:** 1 (F2 mechanics), 2 (accepted pending the Lead's path), 3 (F1), 4 (F8), 5-7 safe.
- **Seams:** additive. No driver or package code was touched.
- **Class completeness:** the router surface (F4, `marked_person` under E19); the ratchet's semantics vs axis 18 (F2); AR-13 siblings (F6).
- **Duplication and consistency:** F6, F9, F10; `KEYED` vs `QUESTION_SITE_RE` queued to N4c.
- **Code quality:** F7.
- **Hygiene:** `selftest.py --lang` 2/2 per the report. The file is ASCII.
- **In-tree ratchets (q.9):** a new ratchet, with NEW rows rather than raises: `live_only` 0, `after` 0, `unwalked` 87, `hook_layer` 77, `raised_by` [], and `known_red.json` `pins.known_red` 0. They need the N-L axis-18 line in the same merge.
- **Architecture:** F11.
- **Judgment:** none.
- **One road:** none found. I searched `dry_exits.py` case-insensitively for language and project names; the only hits are invocation lines, which serves as the positive control.

## Trail

- **Read:** the diff's 10 files (`dry_exits.py` whole; fixtures `classes.json`, `hooks.json`, `known_red.json`, `s5.json` via probe); the report whole; the spec `:38-157`, `:152-500`, `:505-711`; `critic-diff-brief.md` whole; `known_red.py:1-150` (grep plus `:40-70`); P1-a spec `:222-279`; `driver_dispatch.py:90-107`; `driver_machine.py:47-95`; `refusal_registry.py:250-262`, `:1219-1310`; `stage_joints.py` def list; `harness.py:54-66`; `dry_stub.py:298-314` and def list; `dry_world.py` def list; `retro_numbers.py:268-276`; `architecture.md` AR-13, AR-20; `SIBLING_MAP.md` axis 18; `TESTING.md:40-127`; `test_judgment_census.py:66-67`; `canon.yml` grep `dry_`; the N0 verdict tail.
- **Re-runs:**
  - `dry_exits.py --check` gives the report's output byte-for-byte: NUMBER lines 21+2 / 61, 188 / 43 (8, 8, 27) / 21 of 29, 9 / 58/19/25(0)/43/2 / 0 / 87/87, 77/77, then `dry_exits --check: 0 discrepancies`, exit 0.
  - `--selftest` gives `dry_exits selftest: 62/62 cases`, exit 0.
- **Independent recounts:**
  - registry: `102 77 58 25 other 0`;
  - `unpassable()` filtered: `58 0`;
  - `len(KNOWN_REFUSALS)`: `21`;
  - grep of literal `Person(`/`site_seam_person(` kinds: `29`;
  - the AST function-scope rule: 12 keyless plus 2 mixed.
- **Probes** on scratch copies of `driver-exits/` (originals sha256-checked, 0 mismatches):
  - **ca:** `raised_by 1`, `0 discrepancies`;
  - **cb:** `live_only 1/0, unwalked 86/85; raised_by 1`, two NOTE lines, `0 discrepancies`;
  - **cc:** `unwalked 86/86`, `0 discrepancies`.
- **Negative check:** "number of word skips" is absent from `driver_dialog.py`. Case-insensitive `skip` found only `:160` `"skipped"` status, which is the control.
- **Not run:** CI, the scenario files, the ratchets.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "class_completeness": "Router surface: match_known mints marked_repair/marked_person outside KNOWN_REFUSALS and outside the census (F4); marked_person is ask_person and falls under E19 too (F1). Axis 18: the new ratchet's raised_by door is global and never stale, a second semantics against axis 18 one stale/cap semantics and the known_red pin (F2); the axis-18/34/17 lines and brief question 9 are N-L R-L1/R-L2 owed in the same merge (F12). AR-13 siblings: override predicate re-implemented beside refusal_registry.unpassable (F6); KEYED mirrors test_conductor_doors QUESTION_SITE_RE, queued with N4c. Same-artifact sweep of check(): both directions hold for routes/joints/kinds, the walk direction lacks row->walk (F3). Clones: known_red strict reader (F9, queued), dry_stub prompt_sha vs author_input_sha (F10, node N2).",
  "fixes": [
    "F1 dry_exits.py:515-518 (+docstring :17, classes.json _about) - class unknown on an ask_person route is red per E19, not a NOTE; reach 0 discrepancies by naming sources: class_of :396-401 accepts a class_source that is a by_source key; Lead names the class rows for story_budget, executor, readiness (and marked_person after F4) - before merge",
    "F2 dry_exits.py:500-508 - raised_by entries name their count ('<count>: <who, where>'); per count require count == base + entries(count); above = unnamed raise red, below = stale credit red; table rows for cross-count and stale credit - before merge",
    "F3 dry_exits.py:489-496 - add the row->walk direction: a census row with reach story|seed needs at least one walk row whose subject is its name, else red with door; table row - before merge",
    "F4 dry_exits.py:301-318 - census the routes match_known mints itself (AST of its literal return tuples, or probes with role_cli.REPAIR_MARKER/PERSON_MARKER) and add rows marked_repair, marked_person in fixtures/driver-exits/gates.json; numbers 21+2+2 - before merge",
    "F5 dry_exits.py:434,549-551 - gate_questions counted from classes.json question: sources present in prices, not the literal 2; recount commands print exactly 58/19/25/2 and ban_doors - this round",
    "F6 dry_exits.py:418-420,431 - read the word-does-not-pass set through refusal_registry.unpassable() filtered by SCANNED and non-operation (AR-13) - this round",
    "F7 dry_exits.py:453-555 - split check() (~103 lines) into code-rows, walk, ratchets, classes, ledger, numbers helpers; refuse reach unwalked/hook_layer in walk rows (REACH_RE is shared, :44,:225) - this round",
    "F11 commit message of the fix round - architecture line names AR-25, AR-22, AR-15 besides AR-1/13/20/28 - this round",
    "F8 Lead fork before N4: keyless-kind rule - recommend keyed when the Person text argument is a name bound in the same function to a closed_question/priced_section call (7 kinds drop: closed_held, code_close, delivery, exit_limit, repair_limit, report_match, ticket_auth) - Lead decides, spec section 3.2 line",
    "F9 queued node: dry_exits._read_json/_no_duplicate_keys :77-94 clone of known_red._read/_no_duplicates known_red.py:43-70; survivor known_red reader made public by its owner (P1-a helper node)",
    "F10 node N2: dry_stub.py:305-306,312 prompt_sha computed through dry_exits.author_input_sha (one normalisation for C5)",
    "F12 Lead-owed: N-L R-L1 (SIBLING_MAP axis 18 with F2 semantics, 34, 17) and R-L2 (brief question 9) in the same merge; ledger path fixtures/driver-exits/known_red.json written into spec section 3.2; N3 keep row covers tests/dry_exits.py and fixtures/driver-exits"
  ],
  "trail": {
    "read": [
      "ai-packages/qa-factory/scripts/tests/dry_exits.py (whole, 68c49c6)",
      "ai-packages/qa-factory/scripts/tests/fixtures/driver-exits/classes.json, hooks.json, known_red.json, s5.json",
      "docs/tasks/specs/reports/20261113-p1b-n1-report.md",
      "docs/tasks/specs/20261113-p1b-dry-story-spec.md:38-711",
      "docs/tasks/critic-diff-brief.md",
      "docs/tasks/specs/20261113-p1a-writer-reader-round-spec.md:222-279",
      "ai-packages/qa-factory/scripts/tests/known_red.py:40-150",
      "ai-packages/qa-factory/scripts/driver_dispatch.py:90-107,3761-3765",
      "ai-packages/qa-factory/scripts/driver_machine.py:47-95",
      "ai-packages/qa-factory/scripts/refusal_registry.py:250-262,1219-1310",
      "ai-packages/qa-factory/scripts/tests/dry_stub.py:298-314",
      "ai-packages/qa-factory/scripts/tests/harness.py:54-66",
      "ai-packages/qa-factory/design/architecture.md AR-13, AR-20",
      "docs/SIBLING_MAP.md axis 18",
      "docs/TESTING.md:40-127",
      "docs/tasks/specs/reviews/20261113-p1b-n0-code-critic.md (tail)"
    ],
    "reruns": [
      {"command": "python -B scripts/tests/dry_exits.py --check (in the package of the worktree)", "result": "identical to the report witness; dry_exits --check: 0 discrepancies, exit 0"},
      {"command": "python -B scripts/tests/dry_exits.py --selftest", "result": "dry_exits selftest: 62/62 cases, exit 0"},
      {"command": "python -B -c refusal_registry recount (scanned, unpassable, operations; unpassable() filtered)", "result": "102 77 58 25 other 0; 58 0"},
      {"command": "grep literal Person/site_seam_person kinds over story_run.py driver_*.py", "result": "29"},
      {"command": "probe ca/cb/cc on scratch copies of fixtures/driver-exits, then sha256sum -c of the originals", "result": "ca 0 discrepancies with a stale raised_by; cb one raised_by covers live_only and unwalked, 0 discrepancies; cc seed row with no walk row, 0 discrepancies; originals 0 mismatches"}
    ]
  }
}
```
