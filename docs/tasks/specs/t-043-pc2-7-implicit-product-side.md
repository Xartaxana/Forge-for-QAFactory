# t-043 — PC2-7: this story's own side answer does not remove its implicit `product` (DRAFT spec, designer)

Batch `package-ci/2`, node PC2-7. Owner's word 11.11.2026: «Да, в работу». Source finding:
`plans/piles/package-ci/findings/20261111-kanon-krasnyj-no-mr-entry-otvet-o-storone-vyklyuchaet-produkt.md`.
This spec CHANGES THE MEANING of the sides record (which registry rows switch the implicit side off), so PROJECT.md
«Как принимается изменение пакета» item 6 applies: plan critic before the builder; the premise is measured (§4).
Status: DRAFT — forks F-1..F-4 at the end are the Lead's (F-2 goes to the owner).

## 0. The defect in one paragraph (so the builder needs nothing else)

`scripts/tests/test_no_mr_entry.py:423-440`: a story is launched with `--side backend=substituted`, the factory asks
«Whose is it?» (`sides.deliverable`), the person answers `another team's`. Expected in `pipeline.sides`: `backend`
(substituted, deliverable false, source person) AND `product` (real, deliverable true, source default). The check at
:436-438 is red in CI (run 43092267661, `package-full-shard-2`: `got {'reality': None, ...}`). Order of events:
1. `s0_write_sides` (`story_run.py:8493-8538`) asks the question; the answer is taken at `story_run.py:8315-8317` by
   `_keep_sides_answer` (`:8579-8617`), which writes a `product.sides` registry row through
   `project_knowledge.record(..., story=self.task, by="driver")` (`:8606-8611`).
2. On the next entry `s0_rest` calls `s0_sides_sets` (`:9913`), which reads the registry through `_sides_entries`
   (`:8457-8491`) -> `contract.registry_sides` (`contract.py:5697-5770`). That reader sets `product_rows=True` for ANY
   well-formed `product.sides` row (`contract.py:5730`), including the row this very story wrote a moment ago.
3. `s0_sides_sets` adds `product` only `if not got["product_rows"]` (`story_run.py:8561-8562`) -> no `product`.
With `--no-trace` step 1 writes nothing (`story_run.py:8603-8605`), `product_rows` stays False and `product` IS added:
one action, two records (P31). The docstring `story_run.py:8546-8547` says `product` is always carried («the Lead's
call, t-2378 (b)»); the comment `:8561` and spec t-2181 (lines 48, 280, 696) say it is not implied once any
`product.sides` row exists. Both texts sit on the same function.

## 1. Architecture, principles, rules touched; checks and their owners

AR-n touched (`design/architecture.md`), each with the change check written into the DoD (§5):

| AR | how this node touches it | change check (DoD key) |
|---|---|---|
| AR-13 (`architecture.md:161-166`) | the registry stays read ONLY through `contract.registry_sides` (axis 35, `docs/SIBLING_MAP.md:595`); the new discriminator lives inside that reader, no second parser of `records/project-knowledge.json` | K7: `git grep -n "product_rows" -- ai-packages/qa-factory/scripts` lists only `contract.py` (registry_sides, story_sides) and `story_run.py` (`_sides_entries`, `s0_sides_sets`, `sides_reread`); no new `PK.load`/`json.loads` of the registry outside `project_knowledge.py` |
| AR-22 (`:233-238`) | a field gets a new reader: `provenance.story` of a `product.sides` row (producer `project_knowledge.record`, `project_knowledge.py:422`); the meaning of `product_rows` narrows when a `story` is passed — its three readers change in the same commit | K8: the report lists the readers of `product_rows` (`story_run.py:8491`, `:8561`, `:18222`; `contract.py:5686`) with one line each: changed / unchanged-why |
| AR-28 (`:275-280`) | INVARIANT kept: a side the person marked non-real is never recorded as real (`story_run.py:8544-8545`); an unreadable registry still writes `sides_unknown` (`:8551-8558`) | K1-K4 (the table rows in §5) plus the existing `test_story_sides.py:343-357` (unreadable registry) green |
| AR-19 / axis 35 (`SIBLING_MAP.md:591-600`) | the twin of the S0 condition is `sides_reread` (`story_run.py:18216-18223`, same `if not read["product_rows"]`); both change together | K6: both call sites pass `story=self.task` |
| AR-14 | unchanged: `pipeline.sides` keeps its one writer (`stage_done.coerce_value` via `s0_sides_sets`, `side_set_args`) | none beyond K1 |
| AR-29 | no check is added or altered that judges a role; see the census line below | K9: `test_judgment_census.py` green, no census row added |

Principles: P31 (one action, one result — the trace / `--no-trace` pair), P8 (an experiment writes no registry row;
untouched), P27 (code reads a data field, decides nothing about a role's output). FR sections: D (FR-59 — the
unknown registry keeps its declared default `sides_unknown`), G (FR-32 — root cause, with the failing row green),
C (FR-13 — no closed list in code is added). A, B, E, F — not touched (no refusal, no text to a person, no report or
money change).

Checks this node adds or alters, owner and census class (designer rule 1, AR-29, `architecture.md:155`):

| check / condition | owner it serves | census class | note |
|---|---|---|---|
| `registry_sides(..., story=)`: a well-formed `product.sides` row counts toward `product_rows` only when its latest row's `provenance.story` differs from `story` | data (code: joins a row's provenance to the running story's id) | xref (a join of two data fields); NOT a check unit of the census — it refuses nothing and blocks nothing, it chooses a default data row | `judgment-census.json` holds 47 rows for `story_run.py`/`contract.py` and none for `registry_sides`, `s0_sides_sets`, `_sides_entries`, `sides_reread` (Grep `"file": "(story_run|contract)\.py"` = 47 — the positive control; Grep of the four names in the census = 0) |
| `s0_sides_sets` / `sides_reread`: add `product: real, deliverable: true, source: default` when `product_rows` is False | data | none (a default, not a check) | the person's word on `product` always wins (`entries.setdefault`) |

## 2. Item 1 — what the readers do with `product` absent vs present-by-default

Every reader reads the story's sides through `contract.story_sides` (`contract.py:5660-5694`); when `pipeline.sides` is
a non-empty dict it is returned AS IS (`:5670-5674`), so `product` exists for a reader exactly when the S0 record
carries it. Readers (Grep `story_sides\(|registry_sides\(|product_rows` over `scripts/` outside `tests/`):

| reader | file:line | uses | product absent | product present (real, default) |
|---|---|---|---|---|
| S5 exit C1/C2 names | `s5_precheck.py:4505` -> `check_sides` `:2355-2389` -> `_sides_declared` `:2026-2059` | the SET OF NAMES: a test's `sides` key or a Then's `about` naming a side not in the record is a finding (`sides-name-*` :2044-2046, `about-name-*` :2056-2059) | `about: [product]` is REFUSED; no name exists for "the real part of the story" | `about: [product]` is legal |
| walk C11 names | `manual_evidence.py:556-575` | same set of names for a walked case's `about` | `about: [product]` refused (:572-575) | legal |
| ledger proof | `ledger.py:373-385` (`_resolved_about`), `:400-413` (`_proof`) | a Then with no `about` resolves to the test's declared sides UNION every non-real side of the stamp; a Then with `about: [x]` resolves to `x` only | every Then of the story resolves to include `backend` (substituted) -> never proven on this story: the one-side run (t-2181 S-b, «UI story with mocked API») cannot prove a UI-only Then | a Then `about: [product]` is judged on `product` alone (real) -> provable while `backend` is substituted |
| proof stamp | `run_suite.py:668-672` | copies every side into `sides_met` | no `product` key in the stamp | `product: real` in the stamp |
| role briefs | `brief_pack.py:882-901` | lists the sides to the role (S5 brief) | the role never sees a name for the real part | the role sees `product: real` |
| interim packet | `interim_packet.py:56`, `:80-81`, `:118-126` | lists sides to the person | not listed | listed as real |
| reports / counters | `report_facts.py:1904-1920`, `check_delivery.py:2066`, `first_look.py:435`, `manifest_from_tests.py:687-688`, `story_run.py:10433`, `:18390`, `:18457` | non-real sides only, or `source != "default"` | no effect | no effect |
| pending / hold | `acceptance.py:1082`, `window_record.py:1267-1268`, `contract.py:5822` (`parks_after_s5`), `controller.py:5064`, `:9073` | absent+deliverable sides; copies | no effect (product is real) | no effect |
| arrival words | `story_run.py:18169-18180` | `--side x=real` only for a recorded non-real side | no effect | no effect |
| references | `stand_identity.py:180-190` (the ONLY caller of `story_sides(root=)`) | `reference` fields only | no effect | no effect |

Verdict for item 1: the readers NEED the implicit `product` whenever the story's record names no other real side —
it is the only name under which `about` can scope a Then to the real part (s5_precheck C2, manual_evidence C11,
ledger `_resolved_about`). That is the docstring's side (`story_run.py:8546-8547`, «so no reader loses the implicit
side»). The rule «not implied once a `product.sides` row exists» (t-2181:280) is safe only when the registry's rows
NAME the story's real part (e.g. `ui: ours`). The Lead's recommendation removes the contradiction for the story that
gave the answer itself (the red test) — correct and sufficient for this node. It does NOT remove it for the NEXT story
of the same project (edge E2): there the row written by story 1 still switches `product` off although it names only
`backend`. That is today's behaviour, unchanged by this node, and it is returned as fork F-2 (owner), with a residual
node PC2-7b specified in §6 so it is not a bare «tell the owner». The t-2378 (b) text itself is not in `main`: a
repo-wide Grep for `t-2378` finds only the finding, `plans/piles/pre-code/batch-1-progon-bez-koda.md:51` and
`story_run.py:8547` (positive control: the same Grep found those 3 files); the batch file says that journal lives in
the `exp-final` bundle (`batch-1-progon-bez-koda.md:51`). The docstring is the only carrier read.

## 3. Item 2 — the condition and where it is evaluated

Condition (recommended, fork F-1 (a)): `product` is implied on the S0 record when the record is owed (some entry is
non-real or carries a reference, `story_run.py:8489-8490`), the entries do not already hold `product`, and the project's
registry holds NO well-formed `product.sides` row written by ANOTHER story — a row whose latest version carries
`provenance.story` equal to the running story's id (`self.task`) does not count.

WHERE: inside `contract.registry_sides` (`contract.py:5697-5770`), the one reader of the registry rows (AR-13),
through a new keyword argument `story=None`:
- at `contract.py:5730` (`out["product_rows"] = True`) the flag is set only when `story` is falsy OR
  `str(((row or {}).get("provenance") or {}).get("story") or "") != str(story)`; `row` is the latest live row the
  loop already holds (`:5723`, from `PK.state`). Everything else in the loop (`deliverable`, `settles_by`,
  `registry_key`, `names`, `problem`) stays exactly as now for every row, own or not: an own row still gives its
  side's `deliverable` (that is how the answer reaches `pipeline.sides` on a traced run).
- callers that pass `story`: `Driver._sides_entries` (`story_run.py:8468`: `contract.registry_sides(self.project,
  env or flags.get("env"), story=self.task)`) and its twin `Driver.sides_reread` (`story_run.py:18211`, same
  argument). `story_sides(root=)` (`contract.py:5681`) passes none (unchanged, see the small choices).
- `s0_sides_sets` keeps its position: the `got["problem"]` branch first (`:8551-8558`), the S13 return second
  (`:8559-8560`), the default third (`:8561-8562`).

INVARIANT the position keeps: (i) the default is added AFTER the S13 return, so an all-real launch still writes no
record; (ii) `setdefault` never replaces an entry the launch, the registry or the person put under `product`
(`not built yet` -> `absent`, `story_run.py:8482-8483`; `--side product=...`, `:8479-8481`); (iii) the default is
`real` only for `product`, never for a named side, so a side the person marked non-real is never recorded as real
(AR-28, `:8544-8545`); (iv) a project whose registry described its sides BEFORE this story (a row of another story)
gets exactly those sides and no implied `product` — the t-2181:280 rule for every row this story did not write.

Error direction (designer rule 1: `product_rows` moves from "the registry describes sides" advice to the switch that
decides whether a default side is written). Permitted direction: towards `product_rows = True` (product NOT implied):
the story then has fewer names, a Then cannot be scoped to the real part and stays unproven — more items left with the
person, never a false pass (ledger `_proof`, `ledger.py:400-413`). Adversarial inputs that must land on that side:
- a row whose `provenance.story` is `""` or missing (an old or hand-edited row): `"" != self.task` -> counts (not
  implied);
- a row of a story id that differs from the running one only by letter case (`proj-1` vs `PROJ-1`): compared
  exactly -> counts;
- `story` not passed (`story=None`, every other caller): every row counts — today's behaviour;
- a malformed own row: never reaches `:5730` (`continue` at `:5729`), fills `problem` -> `sides_unknown` (E1).
The one input on the other side is E10 (fork F-3).

## 4. Item 4 — the premise measured on real data (the builder runs this FIRST)

Premise: every `product.sides` row carries `provenance.story`; the rows the driver writes for the running story carry
that story's id; rows of earlier stories carry another id.
Measured by the designer (code reading, carrier-checked):
- `project_knowledge.record` takes `story` as a keyword-only argument with NO default (`project_knowledge.py:402`)
  and writes `"story": str(story or "")` into `provenance` (`:422`) — every row carries the key.
- Writers of `product.sides` rows: the driver, `story=self.task` (`story_run.py:8610`); the conductor's `side`
  subcommand, `story=story` (`project_knowledge.py:676`), where `story = pipeline.ticket or task`
  (`project_knowledge.py:550`) and `pipeline.ticket = self.task` (`story_run.py:9904`) — the SAME id as the driver.
- Test fixtures: `test_story_sides.py` writes rows with `story="S-0"` (10 lines: :292, :328, :368, :370, :389, :405,
  :420, :422, :436), `"S-1"` (:195, :407), `"QA-9"` (:522); the stories it runs are `PROJ-1`, `PROJ-2`, `QA-5`,
  `QA-6` — no fixture row shares the id of the story that reads it. No `records/project-knowledge.json` exists in the
  repository (Glob `**/project-knowledge.json` = 0; positive control Glob `**/test-layers.json` = 5 hits): registries
  are built in temp folders by the tests, so the fixtures ARE the available real-shaped data.
The command the builder runs and pastes before any edit (pure read; expected output on the right):
```
git -C C:\QAFactory\forge-repo grep -n -E "story=(self\.task|story|\"[^\"]*\")" -- ai-packages/qa-factory/scripts/story_run.py ai-packages/qa-factory/scripts/project_knowledge.py ai-packages/qa-factory/scripts/tests/test_story_sides.py
```
Expected: `story_run.py:8610` (`story=self.task`), five `project_knowledge.py` lines (493, 598, 607, 628, 676), twelve
`test_story_sides.py` lines, none of them `story="PROJ-1"`, `"PROJ-2"`, `"QA-5"` or `"QA-6"`. If any fixture row
carries the id of the story that reads it, or `record` gains a default for `story`, STOP and report: the discriminator
then needs another field (the fallback discriminator would be `provenance.by == "driver"` AND `element` in
`launch.sides_answers` — which leaves the conductor road unequal, see F-1 (d)).

## 5. Item 3 — edges, each with the invariant it protects

| id | edge | behaviour | invariant |
|---|---|---|---|
| E1 | the registry unreadable (`unreadable`, `contract.py:5767-5769`) or a malformed row (`problem`, `:5725-5729`) | unchanged: `product_rows` False when unreadable -> `sides_unknown` written (`story_run.py:8551-8558`) AND, when the launch named a non-real side, `product` default added as today; a malformed row never sets `product_rows` | an unknown never becomes a pass: every proof of the story is stamped `sides_unknown` (`run_suite.py:663-674`) and reads unknown in the ledger (`ledger.py:407-408`); the unknown side itself is never recorded real |
| E2 | a second story of the same project, same launch `--side backend=substituted`, after story 1 answered (registry row `backend`, `story` = story 1) | NOT implied: story 1's row is another story's -> `product_rows` True -> story 2's record is `{backend}` (not asked, deliverable from the row — `test_story_sides.py:289-300`) | t-2181:280 for rows this story did not write. Consistent with this node's rule (the row is the project's knowledge, recorded before story 2), but NOT consistent across stories: story 1 = `{backend, product}`, story 2 = `{backend}` for the same launch; and if story 1 ran `--no-trace`, story 2 gets `product`. Returned as F-2 (owner), residual node PC2-7b |
| E3 | the launch names `product` (`--side product=absent`, `not built yet`) | the entry stands; the default is never written over it (`setdefault`) | the person's word on `product` is never replaced by a default |
| E4 | all-real launch (S13) | `entries = {}` (`story_run.py:8489-8490`) -> return at `:8559-8560`; no `pipeline.sides` (`test_no_mr_entry.py:416-422`) | no record is owed; readers derive the default |
| E5 | `--no-trace` | nothing is written to the registry (`story_run.py:8603-8605`); own rows do not exist; the record equals the traced run's record (fields other than `at`) | P31: the same launch and answer give the same `pipeline.sides` with and without `--no-trace` |
| E6 | the S5-hold caller `_side_not_ours` (`story_run.py:21657-21674`, t-2559) writes an own row mid-story | no effect on this story: `s0_sides_sets` runs once, before S0 is recorded done (`:9913`, `:9929`); the hold writes `pipeline.sides` itself (`:21670-21672`). `sides_reread` (only when `sides_unknown` and `pipeline.sides` empty, `:18208`, `:18216`) excludes the own row the same way. For the NEXT story the row is another story's (E2) | one road: the S0 answer, the S5 answer and the conductor's `side` (axis 35 symmetry, `SIBLING_MAP.md:598`) are judged alike — by the story that wrote the row, never by the door |
| E7 | the same story id run again from scratch (new artifacts, registry kept) | its own earlier rows are excluded -> `product` implied as on its first run | a story's own answers never remove its implicit product, on any rerun |
| E8 | a row with empty / missing `provenance.story` | counts as another story's -> not implied | error direction §3 (safe side) |
| E9 | the conductor records `side --name backend --deliverable no` during THIS story (`project_knowledge.py:648-683`) | the row carries this story's id (§4) -> excluded like the driver's | one road for the same fact (P31): the closed answer and the conductor's free-words road give the same record |
| E10 | a subject whose LATEST row is this story's while an EARLIER row is another story's (the person changed their mind mid-S0 through the conductor) | counted as own -> `product` implied (the latest row is all `PK.state` exposes) | errs towards implying — the unsafe direction of §3; fork F-3 |
| E11 | `environments.sides` / `environments.reference_for` rows | never set `product_rows` (only the `SIDES_KEY` loop does, `contract.py:5721-5732`) — unchanged | a stand row describes a stand, not the project's parts |

## 6. Item 5 — the builder node PC2-7 (header lines per CLAUDE.md R11-f)

given: this spec (C:\QAFactory\forge-repo\docs\tasks\specs\t-043-pc2-7-implicit-product-side.md, §0-§5 are the whole requirement); C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\story_run.py (:8457-8617, :9900-9931, :18197-18234); C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\contract.py (:5660-5770); C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\project_knowledge.py (:402-426, :534-551, :648-683); C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_no_mr_entry.py (:388-440); C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_story_sides.py (:282-442); C:\QAFactory\forge-repo\docs\tasks\specs\t-2181-pre-code-and-one-side-runs.md (:275-288, :690-697); C:\QAFactory\forge-repo\ai-packages\qa-factory\design\factory-rules.md (whole); C:\QAFactory\forge-repo\plans\builder-rules.md (whole); C:\QAFactory\forge-repo\docs\TESTING.md
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\story_run.py (_sides_entries, s0_sides_sets, sides_reread)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\contract.py (registry_sides)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_story_sides.py (driver_cases)
C:\QAFactory\forge-repo\docs\tasks\specs\t-2181-pre-code-and-one-side-runs.md (lines 280 and 696, one clause each)
C:\QAFactory\forge-repo\ai-packages\qa-factory\changelog.d\package-ci-2-implicit-product-side.md
non-goals: the cross-story rule (E2, F-2, node PC2-7b); `contract.story_sides` and `stand_identity.py` (no root caller observes `product`, §2); `_keep_sides_answer` and the S5 hold (they write correctly); `project_knowledge.py` (no history reader, F-3); `test_no_mr_entry.py` (the red check turns green with NO edit); any new test file; quarantine files; `sides_unknown` reader (axis 35 queued road)
handoff: C:\QAFactory\forge-repo\docs\tasks\handoffs\pc2-7-implicit-product-side.md (builder-rules item 11 form)
edges: E1-E11 of §5 — each behaviour as stated; E2 and E10 stay as stated (forks F-2, F-3), not "fixed" in this node
DoD: `python -B C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\scenario_walk.py --witness-for C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\story_run.py C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\contract.py C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_story_sides.py` then the files it prints that builder-rules 7b lets a builder run, at least `python -B C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_no_mr_entry.py`, `python -B C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_story_sides.py`, `python -B C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_story_run_words.py`, `python -B C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_driver_layers.py`, `python -B C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_judgment_census.py`

What to change (the direction is chosen; no alternatives for the builder):
1. `contract.registry_sides(root, env_name=None, story=None)`: the `product_rows` line (`contract.py:5730`) counts a
   row only when `not story` or the row's `provenance.story` (string, `""` when absent) differs from `str(story)`.
   Docstring (`:5698-5705`): one sentence — «with `story`, a row whose latest version that story wrote does not count
   toward `product_rows` (its own answer never removes its implicit `product`, PC2-7); its `deliverable` is read as any
   row's». Nothing else in the function changes.
2. `Driver._sides_entries` (`story_run.py:8468`) and `Driver.sides_reread` (`:18211`) pass `story=self.task`.
3. `Driver.s0_sides_sets`: docstring `:8546-8547` and comment `:8561` say ONE thing, e.g. docstring: «When the launch
   names a side and nothing names `product`, the record also carries `product: real, deliverable: true, source: default`
   (t-2378 (b)), unless the project's registry already holds a `product.sides` row written by another story (t-2181
   E-O2): this story's own answer never removes it, so the record is the same with and without `--no-trace` (PC2-7).»
   The comment at `:8561`: `# no product.sides row of ANOTHER story (this story's own answer does not count, PC2-7)`.
   Remove the words «as story_sides(root=) reads it» (no longer equal; see small choices).
4. `test_story_sides.py` `driver_cases`: ONE parameterised table (P16: the row id names the case) over two
   registry situations, each run twice — traced and `--no-trace` (`s0_run(..., "--no-trace", ...)` and
   `s0_answer(..., "--no-trace")` as at `:313-314`) — asserting (a) the two `pipeline.sides` are equal once every
   `at` is dropped, (b) `product` is as expected:
   | id | situation | `product` in `pipeline.sides` |
   |---|---|---|
   | own-answer | no registry row; `--side backend=substituted`; answer `another team's` | `{reality: real, deliverable: true, source: default}` |
   | other-story-row | a `product.sides` row `backend` with `story="S-0"` recorded first (as `:291-292`); `--side backend=substituted`; no question | absent |
   The existing block `:289-300` becomes the traced half of `other-story-row` (fold it in, do not duplicate it).
   `test_no_mr_entry.py:423-440` is NOT edited: its check `:436-438` must turn green with its label and expected value
   unchanged.
5. `t-2181-pre-code-and-one-side-runs.md` lines 280 and 696: after «`product` is not implied» add «(a row this story
   itself wrote does not count: the story's own answer never removes its implicit `product` — PC2-7, t-043)».
6. Changelog fragment (English): one entry — a story's own answer about a side no longer drops the implicit
   `product` side from its record; the record is the same with and without `--no-trace`.

Acceptance keys (verbatim, checked by the acceptor against the witness):
- K1 `test_no_mr_entry.py` check «... and the implicit product side is carried beside it (real, deliverable,
  default)» passes, file unedited (`git diff --stat` shows no line for it).
- K2 the `own-answer` row passes in both modes and the two records are equal (without `at`).
- K3 the `other-story-row` row passes in both modes: no `product`, and the records are equal.
- K4 the existing F6 check `test_story_sides.py:429` and `:203-230` (reader path) stay green unedited.
- K5 the docstring of `s0_sides_sets` and the comment at the condition say the same rule (quoted in the report).
- K6 `_sides_entries` and `sides_reread` both pass `story=self.task` (quoted lines).
- K7 the AR-13 grep of §1 (output pasted).
- K8 the AR-22 reader list of §1 (one line per reader).
- K9 `test_judgment_census.py` green; no census row added.
- K10 the §4 measurement output pasted BEFORE the first edit.
- K11 commit message lines: `architecture: AR-13, AR-19, AR-22, AR-28 -- the registry is still read only through
  registry_sides; the S0 default and its relaunch twin change together; product_rows readers named; a non-real side is
  never recorded real` and `judgment: none -- a default data row chosen by joining a row's provenance to the story id;
  nothing judges a role`.
- K12 the t-2181 clause present at both lines (quoted).

Budget: product diff ~15 lines; test diff not larger than that plus the folded block (builder-rules 7d — a larger test
diff is a report line with its reason).

### Residual node PC2-7b (opens only on the owner's answer to F-2; not dispatched with PC2-7)

owns: C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\story_run.py (s0_sides_sets, sides_reread);
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\contract.py (registry_sides, story_sides);
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_story_sides.py (driver_cases, registry_cases);
C:\QAFactory\forge-repo\docs\tasks\specs\t-2181-pre-code-and-one-side-runs.md (lines 280, 696).
Test: the PC2-7 table gains the row `second-story` (story 1 answers `another team's`, story 2 same launch on a copy of
the registry, as `test_story_sides.py:509-517` copies it): story 2's record equals story 1's (without `at`). Under
F-2 (a) the node is closed with no code (the rule stands, recorded by the owner); under F-2 (b) the condition becomes
«`product` is implied unless the story's merged entries already hold a REAL side» and F6 (`test_story_sides.py:429`)
and `:209` flip to the new expectation.

## 7. Small choices closed by the designer (no design weight; reversible)

- The keyword is `story`, the output key stays `product_rows` (no new field; AR-22 walk is the four existing readers).
- `contract.story_sides(root=)` does not take `story`: its only root caller, `stand_identity.reference_stands`
  (`stand_identity.py:188-190`), reads `reference` fields only, so no output of the factory depends on `product`
  there; the comment at `story_run.py:8561` stops claiming equality with it. (If F-2 (b) is taken, PC2-7b changes it.)
- `sides_reread` passes `story` too (axis 35 twin), although its own-row case is rare: one road for the same condition.
- A row is "own" by its LATEST version (what `PK.state` returns, `contract.py:5716`, `:5723`); see F-3.
- Story ids compared exactly (no case-folding): a mismatch lands on the safe side (§3).
- Unreadable-registry behaviour (E1) is left exactly as today.
- The witness list follows builder-rules 7b; files `scenario_walk` prints that 7b excludes (SLOW_TESTS,
  `test_story_run_*` beyond 7c) are named in the report and left to the batch canon in CI.

## 8. Forks (the Lead's; F-2 to the owner)

F-1 — which rows switch the implicit `product` off at S0 (this node).
- (a) every well-formed `product.sides` row EXCEPT those this story wrote (`provenance.story == self.task`) — the Lead's
  recommendation. Red check green unchanged; trace == `--no-trace`; t-2181:280 and every existing test expectation hold
  (F6 `:429`, `:209`); cost ~15 product lines. Leaves E2 (F-2).
- (b) none — `product` always implied when the record is owed and nothing names it (the docstring read literally).
  Fixes E2 too; reverses t-2181:280/:696 and flips `test_story_sides.py:209` and `:429`; a project that described
  `ui`/`backend` also gets `product` — two names for one part (the risk t-2181 E-O2 guards), a role could scope a
  Then to `product` to avoid `on_substitute` (only the code critic would catch it).
- (c) this story's answers count like registry rows (product dropped once anyone answered, also under `--no-trace`).
  P31-consistent and cross-story consistent, but the red test's expectation flips and every multi-side story loses the
  name that lets a UI-only Then be proven (§2) — the one-side run (t-2181 S-b) degrades to all `on_substitute`.
- (d) exclude by door (`by: driver` rows never count, conductor rows do). Rejected: the same fact through two doors
  gives two records (P31, axis 35 symmetry `SIBLING_MAP.md:598`).
Recommendation: (a).

F-2 — the cross-story difference E2 (owner question; residual node PC2-7b).
After (a), the same launch gives story 1 `{backend, product}` and story 2 `{backend}`, and story 2's record depends on
whether story 1 was an experiment. Readers (§2) show story 2 then cannot scope a Then to the real part.
- (a) keep t-2181:280 as is: a project that has any recorded side gets exactly its recorded sides; cost: none now,
  story 2 of a project that only ever named the other team's side proves nothing UI-only while that side is mocked.
- (b) imply `product` when the story's merged entries (registry + launch + answers) hold NO real side — "the real rest
  has no name, so it is called `product`"; independent of history and of `--no-trace`; a project that recorded
  `ui: ours` still gets no `product`. Cost: PC2-7b (~10 product lines, 2 flipped expectations: F6 `:429`, `:209`);
  a reference-only story (S-c: all sides real, one with a reference) stops getting `product` — vocabulary only, no proof
  changes there (nothing is substituted).
Recommendation: (b) — it is the only rule under which one launch gives one record in every story of a project (P31);
the Lead takes it to the owner in plain words: «Если в проекте уже записана одна чужая сторона (бэкенд другой
команды), должна ли следующая стори того же проекта видеть остальное как сторону `product`?».

F-3 — E10: "own" judged by the latest row of a side, or by the whole history.
- (a) latest row (what `PK.state` exposes now) — zero new reader; errs towards implying `product` only when the person
  re-records, during THIS story's S0, a side another story recorded earlier.
- (b) history: a side counts when ANY live row of it was written by another story — needs a new lister in
  `project_knowledge.py` (a reader of row history; `registry_sides` must not read the file itself, AR-13), one more owned
  file and a test row.
Recommendation: (a); the edge needs a conductor re-record inside S0 and its error keeps AR-28 (no non-real side becomes
real; any Then scoped to `product` still passes the code critic).

F-4 — ownership of `contract.py`. `plans/builder-rules.md:8` (item 1) lists `scripts/contract.py` as integrator-only.
- (a) the Lead grants it to PC2-7 explicitly in the dispatch (one function, `registry_sides`).
- (b) the builder hands the `contract.py` hunk under «Needed from integration» and the integrator applies it.
- (c) evaluate the exclusion in `story_run.py` by reading the rows there — rejected: a second reader of the registry
  (AR-13).
Recommendation: (a) — the hunk is three lines and its test runs in the same node.

### Answers to the forks (Lead, 12.11.2026)

- F-1: (a) — every well-formed `product.sides` row except those this story wrote. Lead's technical call.
- F-2: (b) — the owner's word, 12.11.2026 («да» to: the next story of a project that recorded only another team's
  side sees the rest as `product`). `product` is implied whenever the story's merged entries (registry + launch +
  answers) hold NO real side — independent of history and of `--no-trace`. Lead's call on how it lands: the answer came
  before any builder started, so PC2-7 is built DIRECTLY on the (b) condition (it also makes the red check green: the
  story's own `backend` row is non-real); F-1 (a)'s `story=` argument is then not needed and is NOT built. The rewrite
  of §3-§6 to (b) follows the plan critic's verdict (t-050), which was asked to judge (b) as well.
- F-3: (a) — "own" by the latest row. Lead's technical call. Noted while accepting: `project_knowledge.record`
  (`project_knowledge.py:417-419`) returns the HELD row and writes nothing when this story repeats the state and value
  another story recorded, so that row stays another story's and counts — the safe side of §3.
- F-4: (a) — `contract.py (registry_sides)` is granted to the PC2-7 builder by the dispatch; no other function of the
  file. The builder does not commit; the Lead commits (shared tree on `main`).
- Handoff path: the builder's report goes in its final message; the file under `docs/tasks/handoffs/` is optional.

### The node as it stands after the plan critic (t-050; Lead, 12.11.2026) — OVERRIDES §3-§6

Verdict of `docs/tasks/specs/reviews/t-043-critic-on-plan.md`: accept with fixes; building PC2-7 directly on F-2 (b)
is sound. The section «F-2 (b) as the node's condition» of that report — (b)2 where the condition lives, (b)3 the
flip list, (b)4 the edge table, (b)5 the §3 text, the builder node, the test table and keys K-b1, K-b2 — IS the node's
requirement; §3-§6 above (the F-1 (a) design with `story=` and `provenance`) are history and are NOT built. Decisions:

- **B5 — the rule's wording.** `product` is implied exactly when no entry of the story's merged sides is real AND this
  team's (`deliverable` true or absent). An entry with an empty reality is not real. Taken by the critic's
  recommendation until the owner's word: the owner's «да» was to «a project that recorded only another team's side
  sees the rest as `product`», and the literal «no real side» would contradict it when that other team's side is real
  on the stand. The question is put to the owner; the row `other-team-real` of the test table carries the variant's
  expectation (real / true / default).
- **B6:** `contract.story_sides(root=)` follows the rule; under the variant `test_story_sides.py:209` and `:228-230`
  flip, and `:429` flips; each is an edit of the existing check.
- **B7:** the `second-story` row compares `product` whole and `backend` on `reality` and `deliverable` only.
- **B8:** one helper `contract.product_implied(sides)`, three callers; `product_rows` is removed; `sides_reread`
  evaluates over `read["sides"]` and writes the default `product` with `source: default`.
- **B2 — the witness.** Run locally: `test_story_sides.py`, `test_driver_layers.py`, `test_judgment_census.py`,
  `selftest.py --lang`. `test_no_mr_entry.py` (a SLOW_TESTS file) and `test_story_run_words.py` are judged by the batch
  canon in CI, K1 included. **B3':** K7 reads: `git grep -n "product_rows" -- ai-packages/qa-factory/scripts` shows
  only the unrelated variable of `finalize_task.py` (:526, :531, :623). **B4':** t-2181 lines 280 and 696 both state
  the new rule. **B1:** moot under (b) — nothing reads `provenance`.
- **F-4 widened:** `contract.py (registry_sides, story_sides, product_implied)` is granted to the PC2-7 builder.
- Non-blocking findings N1-N7 of the report: accepted as worded, except N2 (outside the node).
- Queued outside the node (finding of the pile, Lead, same night): during S0 of a `--no-trace` story the conductor's
  `side` / `account` / `revoke` commands still write a registry row — their experiment check reads `pipeline.json`,
  which does not exist yet.

## 9. Reading trail

Read whole or by range: the finding (whole); `story_run.py` :8305-8322, :8420-8639, :9890-9933, :18160-18259,
:21655-21679; `contract.py` :5660-5790; `project_knowledge.py` :395-434, :534-553, :560-684; `test_no_mr_entry.py`
:330-469; `test_story_sides.py` :180-638; `test_story_run_words.py` :470-489; t-2181 spec :240-289, :405-429,
:685-704, :715-744 plus Grep of `product.sides|implied|t-2378|implicit` and `F-17|F-12`; `batch-1-progon-bez-koda.md`
:40-59; `s5_precheck.py` :2026-2061, :2355-2390, :4490-4525; `manual_evidence.py` :550-584; `ledger.py` :370-449;
`run_suite.py` :630-676; `brief_pack.py` :872-901, :980-1004; `report_facts.py` :1898-1922, :2112-2127;
`interim_packet.py` :50-129; `stand_identity.py` :172-195; `manifest_from_tests.py` :680-693; `acceptance.py`
:1074-1085; `window_record.py` :1260-1271; `architecture.md` :134-168, :200-281; `SIBLING_MAP.md` axis list and
:591-600; `builder-rules.md` whole; `TESTING.md` :55-99; `test-layers.json` :1-1587 and Grep of the sides test rows,
`keep_fail_at_entry`, `quarantine`; `scenario_walk.py` :11-48, :887-931.
Searches with their positive controls: Grep `story_sides\(|registry_sides\(|\.get\("sides"\)|\["sides"\]|product_rows`
over `scripts/` (142 hits, the reader table of §2); Grep `t-2378` repo-wide (3 files) and in `docs/tasks/compact-snapshots`
and `logs` (0; control `t-2181` in compact-snapshots also 0 — so that folder holds neither; the batch file names the
`exp-final` bundle as the carrier); census Grep (0 for the four functions, control 47 rows for the two files); Glob
`**/project-knowledge.json` (0, control `**/test-layers.json` 5); Grep `story="[^"]*"` in `test_story_sides.py` (12) and
`story=self\.task|story=story` over `scripts/*.py` (writers).
Needed beyond the manifest: `project_knowledge.py` (writers and `_context`), `s5_precheck.py`, `manual_evidence.py`,
`ledger.py`, `run_suite.py`, `brief_pack.py`, `interim_packet.py`, `stand_identity.py`, `report_facts.py`,
`SIBLING_MAP.md` axis 35, `scenario_walk.py`, `judgment-census.json`, `test-layers.json`.
Noticed analogs (not widened): `sides_reread` (`story_run.py:18222`) carries the same condition — folded into this node
as the axis-35 twin; `report_facts._side_used` reads `pipeline["sides"]` raw (already queued on axis 35,
`SIBLING_MAP.md:599`).
