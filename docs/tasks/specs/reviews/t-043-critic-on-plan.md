# t-043 PC2-7 — critic on PLAN

Spec under review: `docs/tasks/specs/t-043-pc2-7-implicit-product-side.md` (DRAFT + «Answers to the forks (Lead, 12.11.2026)»,
re-read after the owner answered F-2 with (b): `:301-315`).
Reviewer: critic (Opus). Mode: plan review, pure reads and greps; no package test run.

**Verdict (covers the spec as it will stand under F-2 (b)): ACCEPT WITH FIXES** — building PC2-7 directly on (b) is sound:
(b) alone turns the red check green with `test_no_mr_entry.py` unedited, and it removes both the in-story difference
(trace / `--no-trace`) and the cross-story one. Before dispatch the spec needs B2 (DoD executability), B3' (K7 reworded for
the removed field), B4' (t-2181 lines 280 and 696 rewritten for the new rule), and the (b)-specific B5-B8 from the section
«F-2 (b) as the node's condition» at the end: B5 the Lead's wording «no real side» differs from the owner's own sentence on one
input (a real side of ANOTHER team) — a meaning question that goes back up; the node runs on the recommendation meanwhile;
B6 the spec's flip list is wrong (`:209` does not flip under the literal rule, `:230` does) and the `story_sides(root=)` choice
must be made; B7 the `second-story` row's «records equal» is false (`backend.source` differs by design); B8 the one condition
lives in one helper used by all three sites, and `product_rows` is removed (AR-15, AR-22). B1 (the provenance guard) is MOOT
under (b): nothing reads `provenance` any more. Answers 1-7 were written for F-1 (a) and stay as the trail of the facts;
where (b) changes an answer, the last section says so. Acceptance of the plan is the Lead's decision; this verdict is an input.

## Answers (written for F-1 (a); see the last section for (b))

### 1. Facts by trail — TRUE, with one imprecision (N1)

- `contract.py:5730` `out["product_rows"] = True` is reached for every row that passes the shape test at `:5725-5729`
  (state known, value dict, `deliverable` bool, `settles_by` str, env "", name not keyless); there is no other condition. TRUE.
- `project_knowledge.record` (`project_knowledge.py:402`) takes `story` keyword-only with no default and writes
  `"story": str(story or "")` into `provenance` at `:422` on every NEW row. TRUE. Caveat (decided right in the Lead's F-3 note):
  `:417-419` returns the HELD row unchanged when state+value repeat — that row keeps the earlier writer's `story`.
- Writers of `product.sides` rows: only `record`; callers with `SIDES_KEY` are `Driver._keep_sides_answer`
  (`story_run.py:8608-8611`, `story=self.task`) and `cmd_side` (`project_knowledge.py:663`, `:675-676`, `story=story`).
  Search: Grep `SIDES_KEY\s*=|"product\.sides"` -i over the package → only `project_knowledge.py:43`, `report_facts.py:1940` (a
  tuple of names, no write), `test_brief_pack.py:2745` (a literal in a fixture); positive control: the same Grep hit `:43`.
- "The SAME story id": `self.task = ns.task` (`story_run.py:1090`), `pipeline.ticket = self.task` (`:9904`), conductor
  `story = pipeline.ticket or task` (`project_knowledge.py:550`). TRUE after `pipeline.json` is written. During S0 —
  exactly when the `sides.deliverable` question stands — `pipeline.json` is not written yet (`test_no_mr_entry.py:430`
  asserts it), so the conductor's `story` is its own `--task` string verbatim (`project_knowledge.py:547-550`). Same string in
  the normal case; a differently-cased `--task` still resolves the folder on NTFS (`hooklib.artifacts_dir`,
  `hooklib.py:228-232`, no case fold) and then lands on "counts" = the safe side. See N1. (Moot under (b).)
- Fixture ids: the 12 `test_story_sides.py` lines (:195, :292, :328, :368, :370, :389, :405, :407, :420, :422, :436, :522)
  carry `S-0`, `S-1`, `QA-9`. Reading stories: `PROJ-1` (`:289-442`), `QA-5` (`:487`, `:530`), `PROJ-2` (`:509`). No row
  carries the id of the story that reads it. TRUE. Note `:487-517`: the row written by `QA-5` (S5 hold) is read by `PROJ-2`.
- The §4 grep matches the «Expected» lines exactly: 1 `story_run.py` line (8610), 5 `project_knowledge.py` lines
  (493, 598, 607, 628, 676), 12 `test_story_sides.py` lines, none with `PROJ-1`/`PROJ-2`/`QA-5`/`QA-6`.

Verbatim output of the §4 grep (`git -C C:/QAFactory/forge-repo grep -n -E "story=(self\.task|story|\"[^\"]*\")" -- ai-packages/qa-factory/scripts/story_run.py ai-packages/qa-factory/scripts/project_knowledge.py ai-packages/qa-factory/scripts/tests/test_story_sides.py`):

```
ai-packages/qa-factory/scripts/project_knowledge.py:493:                                           value={"sign_in": item["sign_in"]}, words="", source="role", story=story, by="driver",
ai-packages/qa-factory/scripts/project_knowledge.py:598:                                   scope="stand", value=None, words=words, source="person", story=story, by="conductor",
ai-packages/qa-factory/scripts/project_knowledge.py:607:                                      value={"sign_in": "account"}, words=words, source="person", story=story, by="conductor",
ai-packages/qa-factory/scripts/project_knowledge.py:628:                                   story=story, by="conductor", task_root=task_root)
ai-packages/qa-factory/scripts/project_knowledge.py:676:                                   words=words, source="person", story=story, by="conductor", task_root=task_root)
ai-packages/qa-factory/scripts/story_run.py:8610:                                        story=self.task, by="driver",
ai-packages/qa-factory/scripts/tests/test_story_sides.py:195:                                    source="person", story="S-1", by="conductor")
ai-packages/qa-factory/scripts/tests/test_story_sides.py:292:                  value={"deliverable": False, "settles_by": "platform team"}, words="theirs", source="person", story="S-0", by="conductor")
ai-packages/qa-factory/scripts/tests/test_story_sides.py:328:                  words="ours", source="person", story="S-0", by="conductor")
ai-packages/qa-factory/scripts/tests/test_story_sides.py:368:                  value={"deliverable": False, "settles_by": "platform team"}, words="theirs", source="person", story="S-0", by="conductor")
ai-packages/qa-factory/scripts/tests/test_story_sides.py:370:                  value={"reality": SUBSTITUTED}, words="the stand", source="person", story="S-0", by="conductor")
ai-packages/qa-factory/scripts/tests/test_story_sides.py:389:                  value={"reality": SUBSTITUTED}, words="the stand", source="person", story="S-0", by="conductor")
ai-packages/qa-factory/scripts/tests/test_story_sides.py:405:                  words="another team's", source="person", story="S-0", by="driver")
ai-packages/qa-factory/scripts/tests/test_story_sides.py:407:                  words="no, this backend is ours", source="person", story="S-1", by="conductor")
ai-packages/qa-factory/scripts/tests/test_story_sides.py:420:                  value={"deliverable": False, "settles_by": ""}, words="theirs", source="person", story="S-0", by="conductor")
ai-packages/qa-factory/scripts/tests/test_story_sides.py:422:                  value={"reality": SUBSTITUTED}, words="the stand", source="person", story="S-0", by="conductor")
ai-packages/qa-factory/scripts/tests/test_story_sides.py:436:                  value={"reality": ABSENT}, words="the stand", source="person", story="S-0", by="conductor")
ai-packages/qa-factory/scripts/tests/test_story_sides.py:522:                  words="no, the api is ours after all", source="person", story="QA-9", by="conductor")
```

### 2. Does the condition turn `test_no_mr_entry.py:436-438` green with no edit — YES (traced)

Order, `test_no_mr_entry.py:423-438`, story `PROJ-1`, traced, registry file absent at start:
1. Entry 1 `--side backend=substituted`: `_sides_entries` → registry empty → `{backend: substituted, source launch}`;
   `s0_write_sides` asks `deliverable:backend` (`story_run.py:8521-8538`); exit 3, no `pipeline.json` (`:430`).
2. Entry 2 answer `another team's`: `s0_read_word` → `_keep_sides_answer("backend", ...)` (`:8315-8317`):
   `launch.sides_answers = {backend: False}` (`:8587`), then `PK.record(..., story="PROJ-1", by="driver")` writes the row.
3. Same entry: `s0_write_sides` — registry gives `backend {real, deliverable False, settles_by ""}`, the launch overrides the
   reality to `substituted`, the answer sets `source person` → `deliverable` present → not asked (`:8522`).
4. `s0_rest` → `s0_sides_sets` (`:9913`) → with F-1 (a) `product_rows` False → `entries.setdefault("product", ...)`
   (`:8561-8562`) → `coerce_value` for `sides.product.*` (keys the `--no-trace` road already writes) → `apply_facts` →
   `pipeline.json` written once (`:9913-9917`).
Nothing else between the answer and the record touches `product`: `apply_facts` only adds keys; `stage_done.py --stage S0`
(`:9929`) is a status call; C15 does not fire (`backend` exact). The CI witness (`got {'reality': None, ...}`) is consistent
with `product_rows` being the only cause.

### 3. Readers of `product_rows` — COMPLETE and correctly classed; the `story_sides(root=)` omission is SAFE

Grep `product_rows|registry_sides\(` -i over `ai-packages/qa-factory`: `contract.py:5681, 5686, 5697, 5701, 5706, 5730, 5768`;
`story_run.py:8459, 8468, 8491, 8561, 18211, 18222`; tests `test_story_sides.py:237, 247, 259, 271, 279`; and
`finalize_task.py:526, 531, 623` — an UNRELATED local variable (`C.product_result_rows`), which breaks K7 as written (B3).
Readers of the flag: `story_run.py:8491`, `:8561`, `:18222`, `contract.py:5686`. Matches K8.
`story_sides(root=)` callers outside tests: only `stand_identity.py:188` (21 non-test hits of `story_sides\(`, one with
`root=`). It keeps only sides with a non-empty string `reference` (`:189-190`); the default `product` carries
`reference: None` (`contract.py:5679`). Whether `product` is present there is unobservable. SAFE.

### 4. Error direction and edges (F-1 (a))

- §3 direction (towards `product_rows = True`) is the safe side: with fewer names a Then cannot be scoped to the real part
  and stays unproven, never a false pass.
- B1 (moot under (b)): the prescribed expression `str(((row or {}).get("provenance") or {}).get("story") or "")` raises
  `AttributeError` on a non-dict `provenance` (`PK._usable`, `project_knowledge.py:131-141`, does not validate it); the outer
  `except` (`contract.py:5767-5769`) would then read the WHOLE registry as unreadable for the driver's callers. The sibling
  `PK._source_of` (`:189-191`) guards with `isinstance`.
- Held row (`:417-419`): decided right; at S0 the driver only asks when no row gives `deliverable` (`story_run.py:8522`).
- E7, E10, E5, E1, E3, E4, E6, E8, E9, E11: as stated in the spec (E5's premise is true for the driver road only, N2).

### 5. Architecture (F-1 (a)) — the right AR-n, kept; no AR-29 judgment

AR-13 kept (no second parser), AR-19 twin `sides_reread` changes too, AR-22 named, AR-28 kept. Census: 0 hits for the four
function names in `judgment-census.json` (control: 47 hits for `"file": "(story_run|contract)\.py"`). FR-13, FR-58, FR-59 —
no conflict.

### 6. Tests (F-1 (a))

The table form fits `docs/TESTING.md:96`; folding `:289-300` must keep its two assertions (N3); the traced own-answer half
duplicates `test_no_mr_entry.py:423-438` (N4). Under (b) the table is replaced (last section).

### 7. Executability for a Sonnet builder — NOT executable as written (B2, B3)

- B2: `scenario_walk.py --witness-for <the three owns>` prints ~140 files (run by me, read-only: 59 `keep` rows for
  `story_run.py`, 3 scenarios and ~80 `keep` rows for `contract.py`, the whole scenario layer for `test_story_sides.py`).
  «the files it prints that builder-rules 7b lets a builder run» leaves the choice to the builder. `slow_tests.json`
  (`slow_over_s: 10`) lists `test_no_mr_entry.py: 61.6`, `test_driver_layers.py: 40.0`, `test_judgment_census.py: 37.5`,
  `test_story_run_words.py: 20.0`; `test_story_sides.py` is NOT listed (control: the same Grep found the four). PROJECT.md
  «Как принимается изменение пакета» item 2: a `SLOW_TESTS` file is not run locally, a builder witness is «до минуты».
  `test_no_mr_entry.py` is over a minute and `keep_fail_at_entry` (`test-layers.json:5363`), and K1 rests only on it.
  `test_story_run_words.py` and `test_driver_layers.py` are mandated by builder-rules 7c (each < 1 min). The scenario layer
  includes `test_scenario_world.py`, an UNTRACKED file of another session (`git status`: `?? .../test_scenario_world.py`).
- B3: K7's `git grep -n "product_rows"` also lists `finalize_task.py:526, 531, 623`.

## Blocking findings

1. **B1 — MOOT under (b)** (kept for the record: only if the Lead returned to F-1 (a), prescribe
   `isinstance(provenance, dict) and str(provenance.get("story") or "") == str(story)`).
2. **B2 — DoD not executable inside builder-rules 7b / PROJECT.md item 2** (§6 `DoD:` line, K1, §7 last bullet). Replace
   «then the files it prints that builder-rules 7b lets a builder run, at least ...» with: «Run locally, in this order:
   `scenario_walk.py --witness-for <owns>` (paste its output as the scope record); then `python -B .../test_story_sides.py`,
   `python -B .../test_story_run_words.py`, `python -B .../test_driver_layers.py`, `python -B .../test_judgment_census.py`.
   Every other file it prints — `test_no_mr_entry.py` (SLOW_TESTS, 61.6 s, keep_fail_at_entry), the other `test_story_run_*`
   and slow `keep` rows, and the scenario layer (it includes another session's untracked `test_scenario_world.py`) — is NOT
   run: the report names them as left to the BATCH CANON in CI.» K1: «judged on the BATCH CANON (CI) after convergence:
   `test_no_mr_entry.py` check «... and the implicit product side is carried beside it (real, deliverable, default)» passes;
   the builder's own proof of the same scenario is the `own-answer` row; `git diff --stat` shows no line for that file.»
3. **B3' — K7 under (b)**: `product_rows` is removed (B8), so K7 becomes: «`git grep -n -E "\"product_rows\"|product_rows="
   -- ai-packages/qa-factory/scripts` prints nothing; `git grep -n "product_implied" -- ai-packages/qa-factory/scripts` lists
   the helper in `contract.py` and exactly three callers: `story_sides`, `Driver.s0_sides_sets`, `Driver.sides_reread`» (the
   quoted-key/assignment form does not match the unrelated `finalize_task.py:526` variable; read at `:526`, `:531`, `:623`).
4. **B4' — t-2181 under (b)**: lines 280 and 696 both state the OLD rule («once any `product.sides` row exists, `product` is
   not implied»), and under (b) both the reader and the S0 record change. Item 5 becomes: replace that sentence at 280 and at
   696 with «`product` is implied when the story's sides (the registry's, the launch's and the person's answers merged) hold
   no real side of this team (PC2-7, t-043, the owner's word 12.11.2026); a project that recorded its real side (`ui: ours`)
   gets no `product`».
5. **B5-B8** — see «F-2 (b) as the node's condition», blocking list there.

## Non-blocking findings

- **N1** (moot under (b)) S0-window story id of the conductor.
- **N2** (sibling outside the node — a proposed finding for the Lead to open): `cmd_side` refuses an experiment through
  `_refuse_no_trace` → `external_writes.closed_by_run` (`external_writes.py:189-202`), which reads `pipeline.no_trace` only;
  during S0 of a `--no-trace` story `pipeline.json` is not written yet, so the conductor's `side` WRITES a registry row (P8,
  FR-53), while the driver checks `launch.no_trace` (`story_run.py:8603`). PC2-7 under (b) is unaffected (no history is
  read). Surface: experiment detection before `pipeline.json` is written; neighbours by reading: `cmd_account`, `cmd_revoke`
  share `_write_prologue` (same gap); `cmd_role` calls `record` without `task_root` (no check at all). Owner: the Lead's call
  (pile `package-ci` or `pre-code`).
- **N5** (§6 header `handoff:` and K11): align the header with the Lead's answer («final message, file optional»); K11 → «the
  report proposes the commit lines (the Lead commits)».
- **N6'** under (b): PC2-7b is folded into PC2-7 (its `second-story` row is now in the node, last section); strike the
  «Residual node PC2-7b» subsection and the F-1 (a) / F-3 answers' operative text so the spec has one rule (the «Answers»
  still read «F-1: (a) ...» at `:303` above the F-2 (b) line).
- **N7**: name `test_scenario_world.py` / `scenario_world.py` (another session's uncommitted files) as not run, not the node's.
- **N8**: the table adds driver runs to `test_story_sides.py` (not in `slow_tests.json`, threshold 10 s) — not measured; a
  report line with the file's wall time.

## F-2 (b) as the node's condition

Condition as the Lead wrote it (`spec :304-309`): «`product` is implied whenever the story's merged entries (registry +
launch + answers) hold NO real side — independent of history and of `--no-trace`».

### (b)1. Does (b) alone make `test_no_mr_entry.py:436-438` green, file unedited — YES

Trace (same events as answer 2): at `s0_sides_sets`, `entries` = `{backend: {reality: substituted, deliverable: False,
source: person}}` — the registry's own row gave `backend` reality `real` at `story_run.py:8473`, but the launch flag overrides
the reality at `:8479-8481` before any condition is evaluated. No entry is real → `product` added
`{real, deliverable true, source default}`. The `--no-trace` run gives the same entries (no registry row) → same record. No
history or provenance is read. Nothing between the answer and the record drops `product` (answer 2).

### (b)2. Where the condition is evaluated — one helper in `contract.py`, called by three sites; `story_sides(root=)` follows

- The merged entries exist only in the driver: `_sides_entries` (`story_run.py:8469-8490`) merges registry + launch +
  `not built yet` + reference + answers. So the condition is a predicate over an already-merged `{name: {reality, ...}}`
  dict, NOT a new reading of the registry: AR-13 is kept automatically (`registry_sides` stays the only reader of the rows).
- Three sites apply the default today with the same `if not product_rows` shape: `s0_sides_sets` (`:8561`), its twin
  `sides_reread` (`:18222`) and `story_sides(root=)` (`contract.py:5686`). Under (b) they must say the same thing (AR-19,
  axis 35; AR-15 one survivor): one pure function in `contract.py` beside `story_sides`, e.g.
  `product_implied(sides) -> bool` — True when no entry with a non-empty reality is real (exact wording in (b)5, subject to
  B5). Callers: `s0_sides_sets` over `entries` (after the S13 return, before `setdefault`); `sides_reread` over
  `read["sides"]` — NOT over its filtered `entries`, which drop every real side without a reference (`:18218-18220`), so
  evaluating there would always find "no real side"; `story_sides(root=)` over `read["sides"]`.
- Does `story_sides(root=)` have to follow? Not for any output (its only root caller reads references, answer 3), but YES for
  the rule: leaving it on `product_rows` keeps a second meaning of "implied" alive on axis 35 and keeps `product_rows` with
  one reader. Recommended: it follows, `product_rows` is removed from `registry_sides`' output and docstring
  (`contract.py:5701`, `:5706`, `:5730`, `:5768`) and from `_sides_entries`' return (`story_run.py:8459`, `:8491`) — AR-22:
  a field with no reader is removed in the same commit. Consequence for ownership: F-4's grant widens from
  `contract.py (registry_sides)` to `contract.py (registry_sides, story_sides, product_implied)`.
- Sibling found on the way (fix in this node — `sides_reread` is owned): the re-read writes the default `product` with
  `source: registry` (`story_run.py:18223-18225`, every entry gets `source: registry`), while S0 writes it with
  `source: default` (`:8562`). Under (b) this path fires for every relaunch of an unknown-sides story whose registry holds no
  real side (`test_story_sides.py:371-378` becomes such a case), so one default gets two spellings. The re-read must write the
  default `product` with `source: default` (no `deliverable`/`settles_by` change) — the S0 spelling.

### (b)3. Which existing checks flip — grep with a positive control

Grep `"product" (not )?in|\["product"\]|get\("product"|sides\.product\.` -i over `scripts/tests` (35 hits; the positive
control is the hit list itself: it contains `test_story_sides.py:209`, `:229`, `:429` and `test_no_mr_entry.py:437`). Every
hit that reads a `product` derived from registry rows:

| check | today | literal (b) «no real side» | owner-sentence variant «no real side of this team» (B5) |
|---|---|---|---|
| `test_story_sides.py:209` (`story_sides(root=)`, registry `ui` deliverable false, real) | not implied | does NOT flip (`ui` is real) | FLIPS (`ui` is another team's) |
| `test_story_sides.py:228-230` (reference row alone, `ui` real with reference) | product stays | FLIPS (`ui` real) | FLIPS (`ui` deliverable reads true) |
| `test_story_sides.py:429` F6 (registry `backend` + stand row substituted) | not implied | FLIPS | FLIPS |
| `test_no_mr_entry.py:436-438` | red | green | green |

Both flips at `:209`/`:230` happen only if `story_sides(root=)` follows (recommended); if it does not, only `:429` flips. The
spec's «F6 `:429` and `:209` flip» is wrong under the literal rule (it is right only under the owner-sentence variant, and
misses `:230` under both) — B6.
Records that change with NO assertion flipping (the builder must not "fix" them, and the report lists them):
`test_story_sides.py:289-300` (product now added), `:371-378` (re-read adds product; `:377-378` compares the record with
itself across launches — still equal), `:404-411` (registry `backend` ours + launch substituted → product added),
`:513-517` (`PROJ-2` `--side api=absent` → product added). Hits that do not depend on the rule: `test_story_sides.py:49`,
`:120-123`, `:158`, `:203`, `:223`, `:270` (record path, default path, unreadable path); `test_no_mr_entry.py:400`, `:470`,
`:483` (`product` named by the launch / `not built yet`); `test_story_run_words.py:485-491` (S1 vs S0 `not built yet`);
`test_story_run_arrival.py`, `test_story_run_s1_reference.py:37-38`, `test_reference_window.py:186`, `test_sides_ledger.py:190`,
`test_manual_evidence.py:1191` (record set explicitly); the rest are other uses of the word. Scenario fixtures: Grep `"sides"`
over `scripts/tests/fixtures` = 0 (control: Grep `"file"` over the same folder found files).

### (b)4. Edges under (b)

| edge | merged entries | «no real side» | behaviour | direction / invariant |
|---|---|---|---|---|
| all-real launch (S13) | `{}` (`story_run.py:8489-8490`) | — | return before the default (`:8559-8560`); no record | unchanged; readers derive the default |
| launch names `product` (`--side product=absent`, `not built yet`, `product=substituted`) | holds `product` | either | `setdefault` never replaces it (`test_no_mr_entry.py:467-471`, `:481-485` unchanged) | the person's word wins |
| reference-only story (`--reference ui=old`, all real) | `{ui: real, reference}` | false (`ui` real) | NO `product` — today it gets one (reference rows never set `product_rows`) | the owner accepted it in F-2 (b) («vocabulary only»); no test asserts it today (Grep `"--reference"` over tests: only `test_no_mr_entry.py:410`, `:481`, neither checks `product` beside a `ui` reference) — a new table row |
| registry `ui: ours` + launch `backend=substituted` | `{ui: real, backend: substituted}` | false | no `product` | the E-O2 guard: one real part, one name |
| registry `ui: another team's` (real on this stand) + launch `backend=substituted` | `{ui: real (deliverable false), backend: substituted}` | literal: false → no `product`; owner variant: true → `product` | **B5** | see below |
| unreadable registry | launch entries only; `problem` set | evaluated over the launch entries | `sides_unknown` written (`:8551-8558`) AND `product` implied when no launch side is real — the same as today (`product_rows` False when unreadable, `contract.py:5768`) | AR-28 held by the mark: every proof stamped `sides_unknown`, read unknown in the ledger (`run_suite.py:663-674`, `ledger.py:407-408`) |
| a side whose reality is empty (malformed row, `contract.py:5727`; two reference stands, `:5758`) | the side is LEFT OUT of `entries` (`story_run.py:8471-8472`) and `problem` set | computed over the readable entries only | `product` may be implied beside an unknown side | Decide explicitly: an unknown side does NOT count as real (it is not known to be real, S12) — the same rule as the unreadable registry, one rule for every unknown; the `sides_unknown` mark keeps every proof unknown, so implying `product` can never make a pass. The opposite choice (unknown counts as real → no `product`) would make one malformed row change the story's vocabulary while the whole-unreadable case does not — two rules for one unknown |
| `--no-trace` | registry rows of earlier stories are read, own answer not written | same as traced (own row non-real or overridden by the launch) | same record but `at` | P31 inside a story |
| second story, same launch, after story 1 answered `another team's` | `{backend: substituted, deliverable false (registry), source launch}` | true | `product` implied — same `product` as story 1 | P31 across stories; but see B7: `backend.source` is `launch` in story 2 and `person` in story 1 (`:8479-8481` vs `:8486-8488`) |

B5 — the formalisation differs from the owner's sentence. The owner's «да» (`spec :304-305`) was to: «the next story of a
project that recorded only another team's side sees the rest as `product`». Input: the project recorded only `ui: another
team's` (`deliverable false`), and that `ui` is real on this stand; story 2 launches `--side backend=substituted`. The
literal «no real side» finds `ui` real → NO `product`, although the project recorded only another team's side — the opposite
of the owner's sentence. A real side that is another team's is not "the rest" of this story's product. The variant «no real
side whose `deliverable` is true (this team's; a missing `deliverable` reads true, as `story_sides` reads it,
`contract.py:5689`)» matches the sentence on this input and agrees with the literal rule everywhere else in the table above.
This is an interpretation of the owner's intent (CLAUDE.md 11a): it goes to the owner as one plain question; the node is
executable by the recommendation until the answer (PROJECT.md «Командная работа» item 11). Recommendation: the variant
(«this team's real side»). Question in plain words: «Если в проекте записана только чужая сторона, и на этом стенде она
настоящая (не подменена), — остальное в стори всё равно называется `product`?». Not my decision; the Lead's tier opens it.

### (b)5. Spec text for the Lead (§3 and the builder node)

§3 condition (replace the F-1 (a) paragraph and its WHERE block; keep the INVARIANT block, (iv) rewritten):
«Condition (F-2 (b), the owner's word 12.11.2026): when a record is owed (`story_run.py:8489-8490`) and the merged entries
do not hold `product`, `product: real, deliverable: true, source: default` is added exactly when no entry with a non-empty
reality is real AND counts as this team's — `deliverable` true or absent [B5: the clause in brackets stands until the owner
answers; if the owner says the literal rule, drop it]. An entry whose reality is empty (unknown) is not real. WHERE: one
pure function `contract.product_implied(sides) -> bool` beside `story_sides`; called by `Driver.s0_sides_sets` over
`entries` (after the S13 return, before `setdefault`), by `Driver.sides_reread` over `read["sides"]` (the registry's sides,
never its filtered `entries`), and by `contract.story_sides` over `read["sides"]` in its registry branch. `product_rows`
is removed from `registry_sides` and `_sides_entries`. Error direction: the function decides vocabulary, not proof; a wrong
`True` adds a name next to sides that are all non-real or unknown — the proofs of non-real sides stay `on_substitute` and an
unknown side keeps `sides_unknown`, so no pass is created; a wrong `False` leaves the real part unnamed — more items with the
person. Adversarial inputs: an empty dict (`False` is never reached — the caller returns earlier on no record; the function
returns True on `{}` and `story_sides` only calls it when the registry has sides); a non-dict entry (`False`-safe: treat as
not real); `reality` missing or `""` (not real); `deliverable` not a bool (reads true, as `story_sides` reads it).»
INVARIANT (iv) becomes: «a project whose registry or launch names a real side of this team gets exactly its named sides and
no implied `product` (E-O2: one real part, one name)».

Builder node (§6), replacing «What to change»:
1. `contract.product_implied(sides)` (new, beside `story_sides`), docstring states the rule, the unknown and the error
   direction above; `story_sides` registry branch (`:5685-5690`): drop `product` only when `not product_implied(read["sides"])`;
   `registry_sides`: remove `product_rows` from the output, the docstring and `:5730`, `:5768`.
2. `Driver._sides_entries`: stop returning `product_rows` (docstring `:8459`, return `:8491`).
3. `Driver.s0_sides_sets`: `if product_implied(entries): entries.setdefault("product", ...)`; docstring `:8546-8547` and the
   comment say ONE rule (quote (b)), «as story_sides(root=) reads it» stays true now and may stay.
4. `Driver.sides_reread`: `if product_implied(read["sides"]): entries.setdefault("product", ...)`, and the default
   `product` is written with `source: default` (the S0 spelling), other entries keep `source: registry`.
5. t-2181 lines 280 and 696: B4'.
6. Changelog fragment: «a story whose sides hold no real part of this team now always carries the implicit `product` side,
   whatever earlier stories recorded and with or without `--no-trace`; a reference-only story no longer gets it».
owns: `story_run.py (_sides_entries, s0_sides_sets, sides_reread)`; `contract.py (registry_sides, story_sides,
product_implied)` (F-4 widened by the dispatch); `tests/test_story_sides.py (registry_cases, driver_cases)`; t-2181 (lines
280, 696); the changelog fragment. non-goals: `_keep_sides_answer`, the S5 hold, `project_knowledge.py`, `stand_identity.py`,
`test_no_mr_entry.py` (unedited; green on the canon), N2.
Test table (one parameterised table in `driver_cases`, id = case; P16), each S0 row run traced AND `--no-trace` asserting
(a) the two `pipeline.sides` equal without `at` and (b) `product` as below:

| id | situation | `product` |
|---|---|---|
| own-answer | no registry; `--side backend=substituted`; answer `another team's` | real / true / default (fails before the fix on the traced half's equality) |
| other-story-row | registry `backend` (deliverable false, `S-0`) recorded first (fold `:289-300`, keeping its two assertions: not asked; `(SUBSTITUTED, False, "platform team")`); same launch; not asked | real / true / default |
| real-side-named | registry `ui` ours (deliverable true) + launch `--side backend=substituted` | absent |
| other-team-real [B5] | registry `ui` another team's (deliverable false) + launch `--side backend=substituted` | variant: real/true/default; literal: absent — the row's expectation is the one the owner confirms |
| reference-only | `--reference ui=old` (all real) | absent |
| second-story | story 1 `PROJ-1` answers `another team's`; story 2 `PROJ-2` same launch on a copy of the registry (as `:509-512`) | story 2's `product` equals story 1's; story 2's `backend` equals story 1's on `reality` and `deliverable` (NOT `source`: `launch` vs `person` by design — B7) |

and in `registry_cases` the flipped `:209` / `:228-230` expectations per the chosen variant (B6), as edits of those checks,
not new checks. The `second-story` row has no `--no-trace` half (story 1 `--no-trace` writes no registry; story 2 is then
asked — a different flow, not this row). The traced `own-answer` half asserts only the equality (N4).
Acceptance keys to add: «K-b1 the report lists every check that flipped with old → new expectation, and the records that
changed with no assertion (`test_story_sides.py:289-300`, `:371-378`, `:404-411`, `:513-517`)»; «K-b2 the re-read writes the
default `product` with `source: default` (quoted line)».

### Blocking list for (b)

- **B5** — the formalisation «no real side» contradicts the owner's sentence on a real side of another team; return the one
  plain question to the owner, run the node on the recommended variant («this team's real side») with the row
  `other-team-real` carrying the confirmed expectation.
- **B6** — the flip list: under the literal rule `:209` does not flip and `:230` does; under the variant both flip; plus
  `:429` under both; and the decision «`story_sides(root=)` follows» (recommended) must be written, with F-4 widened.
- **B7** — `second-story` «records equal» is false: compare `product` whole and `backend` on `reality`/`deliverable` only.
- **B8** — one helper for the three sites; remove `product_rows` (AR-15, AR-22); `sides_reread` evaluates over
  `read["sides"]` and writes the default with `source: default`.

### Architecture under (b)

AR-13 kept (a predicate over returned data; `registry_sides` stays the only reader). AR-15/AR-19 kept by B8 (one helper,
three sites, the S0 condition and its twin change together). AR-22: `product_rows` loses all readers → removed same commit;
no new field read (no `provenance`). AR-28: the default is `real` only for `product`; a non-real side is never recorded real;
unknown sides keep `sides_unknown`. AR-29: the helper picks a default data row; it refuses nothing and judges no role's
output; no census row. P31: one launch gives one record in every story of a project and with or without `--no-trace` (the
reason the owner chose (b)). FR-13: the only word read is `SIDE_REAL`, already a data-file word (`test_no_mr_entry.py:476`).
FR-59: the unknown keeps its declared default (`sides_unknown`). No conflict found.

## Standing questions

- DUPLICATION AND CONSISTENCY: three copies of the default condition (`story_run.py:8561`, `:18222`, `contract.py:5686`)
  → one helper (B8); two spellings of the default `product` (`source: default` at S0, `source: registry` on the re-read) →
  one (B8); the traced own-answer half vs `test_no_mr_entry.py:423-438` (N4). Grepped: `product_rows`, `story_sides\(`,
  `SIDES_KEY|product\.sides`, `"product" (not )?in|\["product"\]|get\("product"|sides\.product\.`.
- CODE QUALITY: under (b) no finding beyond B8; B1 moot.
- ONE ACTION, ONE ROAD (P31): (b) closes the in-story and the cross-story two-road defects; B5 is a meaning question for the
  owner, not an exclusion; N2 (the conductor's experiment check before `pipeline.json`) is a second road, proposed as a
  finding for the Lead.

## Class-wide completeness (SIBLING_MAP axis 35)

Class: "whether the implicit `product` is carried depends on something other than the story's merged sides". Instances on
axis 35: `s0_sides_sets` — fixed; `sides_reread` — fixed (and its default spelling, B8); `story_sides(root=)` — follows by
B8; the S5 hold `_side_not_ours` — writes one side through `stage_done`, applies no default (n/a); the arrival record
(`side_set_args`) — sets named sides only (n/a). Cross-story instance (former E2) — closed by (b) itself. Out of the node:
N2 (proposed finding).

## What I did not check

- No package test was run (dispatch non-goal); the green trace of `:436-438` is by reading, not a run.
- `stage_done.coerce_value` for `sides.product.*` and for `source=default` on the re-read path was not read; I relied on S0
  already writing those keys and value.
- The t-2378 (b) text itself (not in `main`); t-2181 line 48 not read.
- Whether `test_driver_layers.py` is still red at HEAD (`keep_fail_at_entry`); builder rule 7 covers a red file outside the
  change. Whether `test_driver_layers` pins `contract` names (a new function `product_implied` in `contract.py`, not in
  `story_run.py`, so `driver-layers.json` should not need a row — not verified).
- The clone/lint ratchets' reaction to the table's setup lines; the wall time of `test_story_sides.py` after the table.

Trail (read): the spec whole and `:300-315` again after the owner's answer; the finding whole; `contract.py:5655-5774`;
`story_run.py:1089-1093, 8300-8629, 9880-9939, 18190-18239, 21652-21679`; `project_knowledge.py:131-158, 189-191, 215-255,
300-689`; `test_no_mr_entry.py:330-494`; `test_story_sides.py:170-539`; `test_story_run_words.py:468-492`;
`stand_identity.py:170-199`; `external_writes.py:189-202`; `hooklib.py:228-232`; `report_facts.py:2110-2131`;
`t-2181...md:270-291, 685-699`; `SIBLING_MAP.md:588-600`; `architecture.md` AR lines (grep); `builder-rules.md:6-73`;
`TESTING.md:40-104`; `test-layers.json:2415-2426, 4670-4681, 5340-5419`; `slow_tests.json:1-30` + grep;
`critic_verdict.schema.json`. Searches with controls: listed inline above.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "B2: DoD not executable within builder-rules 7b / PROJECT.md item 2: witness-for prints about 140 files and the builder is left to choose; test_no_mr_entry.py is SLOW_TESTS (61.6 s, keep_fail_at_entry) and K1 rests on it; enumerate the local list and judge K1 on the batch canon",
    "B3': K7 must be rewritten for the removed product_rows field (the old grep also hits the unrelated finalize_task.py:526,531,623)",
    "B4': t-2181 lines 280 and 696 both carry the old rule; under (b) both are replaced with the merged-sides rule",
    "B5: the Lead's wording 'no real side' contradicts the owner's sentence on a real side of another team (registry ui deliverable false, real on the stand); one plain question to the owner, node runs on the variant 'no real side of this team' meanwhile",
    "B6: the spec's flip list is wrong: under the literal rule test_story_sides.py:209 does not flip and :228-230 does; :429 flips under both; the decision that story_sides(root=) follows must be written and the contract.py grant widened",
    "B7: the second-story row's 'records equal' is false: backend.source is launch in story 2 and person in story 1 by design; compare product whole and backend on reality/deliverable",
    "B8: one helper contract.product_implied for s0_sides_sets, sides_reread (over read sides, not its filtered entries) and story_sides; remove product_rows; the re-read writes the default product with source default"
  ],
  "fixes": [
    "Section 6 DoD: explicit local run list (scenario_walk output, test_story_sides, test_story_run_words, test_driver_layers, test_judgment_census); all else, incl. test_no_mr_entry.py and the scenario layer with the untracked test_scenario_world.py, left to the BATCH CANON; K1 on CI",
    "K7: grep for the quoted product_rows key or product_rows= prints nothing; product_implied has one definition in contract.py and three callers",
    "t-2181 :280 and :696: replace the old sentence with the merged-sides rule (PC2-7, t-043, owner 12.11.2026)",
    "Section 3 and section 6 rewritten to the (b) text given in the review, the bracketed this-team clause standing until the owner answers B5",
    "Test table rows own-answer, other-story-row (folded, two assertions kept), real-side-named, other-team-real, reference-only, second-story; registry_cases :209/:230 edited per the chosen variant; K-b1 lists flips and silently changed records; K-b2 the re-read default source",
    "Strike F-1 (a), F-3 operative text and the PC2-7b subsection so the spec has one rule; align handoff header and K11 (Lead commits)",
    "Proposed finding for the Lead (N2): the conductor's side/account/revoke do not detect a --no-trace story before pipeline.json is written"
  ],
  "class_completeness": "Axis 35: s0_sides_sets and its twin sides_reread change together through one helper, story_sides(root=) follows it, the duplicate default spelling on the re-read (source registry vs default) is fixed in the node; the S5 hold and the arrival record apply no default (n/a); the cross-story instance is closed by (b) itself. Outside the node: the conductor's experiment check before pipeline.json (N2), proposed as a finding.",
  "trail": {
    "read": [
      "docs/tasks/specs/t-043-pc2-7-implicit-product-side.md",
      "plans/piles/package-ci/findings/20261111-kanon-krasnyj-no-mr-entry-otvet-o-storone-vyklyuchaet-produkt.md",
      "ai-packages/qa-factory/scripts/contract.py:5655-5774",
      "ai-packages/qa-factory/scripts/story_run.py:1089-1093,8300-8629,9880-9939,18190-18239,21652-21679",
      "ai-packages/qa-factory/scripts/project_knowledge.py:131-158,189-191,215-255,300-689",
      "ai-packages/qa-factory/scripts/tests/test_no_mr_entry.py:330-494",
      "ai-packages/qa-factory/scripts/tests/test_story_sides.py:170-539",
      "ai-packages/qa-factory/scripts/tests/test_story_run_words.py:468-492",
      "ai-packages/qa-factory/scripts/stand_identity.py:170-199",
      "ai-packages/qa-factory/scripts/external_writes.py:189-202",
      "ai-packages/qa-factory/scripts/hooklib.py:228-232",
      "ai-packages/qa-factory/scripts/report_facts.py:2110-2131",
      "docs/tasks/specs/t-2181-pre-code-and-one-side-runs.md:270-291,685-699",
      "docs/SIBLING_MAP.md:588-600",
      "plans/builder-rules.md:6-73",
      "docs/TESTING.md:40-104",
      "ai-packages/qa-factory/scripts/tests/test-layers.json:2415-2426,4670-4681,5340-5419",
      "ai-packages/qa-factory/scripts/slow_tests.json:1-30",
      "tools/critic_verdict.schema.json"
    ],
    "reruns": [
      {
        "command": "git -C C:/QAFactory/forge-repo grep -n -E story=(self.task|story|quoted) over story_run.py, project_knowledge.py, tests/test_story_sides.py (spec section 4)",
        "result": "1 story_run.py line (8610), 5 project_knowledge.py lines (493, 598, 607, 628, 676), 12 test_story_sides.py lines with S-0/S-1/QA-9 only; matches the Expected lines"
      },
      {
        "command": "python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for story_run.py contract.py tests/test_story_sides.py",
        "result": "about 140 files printed (59 keep rows for story_run.py, 3 scenarios and about 80 keep rows for contract.py, the whole scenario layer for test_story_sides.py incl. untracked test_scenario_world.py)"
      },
      {
        "command": "Grep -i product_rows|registry_sides( over ai-packages/qa-factory",
        "result": "contract.py and story_run.py readers as in K8, plus finalize_task.py:526,531,623 (unrelated variable)"
      },
      {
        "command": "Grep -i product-presence assertions over scripts/tests; Grep sides over tests/fixtures with a positive control",
        "result": "35 hits; registry-derived product assertions only test_story_sides.py:209, :228-230, :429 and test_no_mr_entry.py:436-438; fixtures 0 hits for sides, control found files"
      },
      {
        "command": "Grep census: four function names in judgment-census.json; control file pattern story_run|contract",
        "result": "0 hits; control 47 hits"
      }
    ]
  }
}
```
