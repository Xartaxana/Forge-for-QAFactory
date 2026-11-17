# C3-b1 report (t-1051) - live_check_demand -> question to the code critic

State: work STAGED in the worktree, NOT committed: the pre-commit hook refused (verbatim below). Commit message is ready in
`C:/Users/i_mas/AppData/Local/Temp/claude/b3e3188b390a00d9/501cb4e0-b55f-46d8-9262-11b1caefad61/scratchpad/msg.txt`
(carries `architecture:`, `judgment:`, `axes: not a mechanism (package change, card C3-b1)`, `tests-over:`).

Hook output, verbatim:
```
factory rules index: up to date (59 rules)
factory rules index is stale: run python tools/factory_rules_index.py and stage docs/OWNER_PRINCIPLES_INDEX.md
```
`docs/OWNER_PRINCIPLES_INDEX.md` is outside owns and the staleness is not from this diff (no principle text touched): a base defect.

## Items (file:line, worktree copy)
1. `proof_level.novelty_question_owed` - proof_level.py:457 (+ `_probe_owed` :450, `PROBE_OWED_ANSWERS` :447). True iff dict row, no `novelty`,
   no flag, not handed, no closed `probe_owed`, AND a `tests[]` row carries `novelty` OR top-level `novelty_unmeasured` is a non-empty string.
2. `_wanted`: `probe_owed == "yes"` adds the requirement - proof_level.py (the branch right after the flag test); `no` adds nothing.
3. `validate_window`: one gap `novelty_question:<iid>` - acceptance.py:1213, after the review checks and before the sensitivity checks; skipped for
   handed / stopped / pending / explained / unconfirmed items and for an item or row already answered. Window item copies `probe_owed` beside
   `review` - window_record.py:1577 (only a closed value). `WORD_READ_KINDS` gains `novelty_question` - window_record.py:1846; origin/door text
   `GAP_ORIGIN["novelty_question"]` window_record.py:332, door `NOVELTY_QUESTION_RECORD` :309.
4. `manifest_put.CRITIC_FIELDS` gains `probe_owed` - manifest_put.py:1085. **Value refusal NOT done** (question 2).
5. Charter paragraph - agents/qa-code-critic.md (Tools list, before "Each finding is a `findings[N]` row"). AR-10 held in text; see the slice finding below.
6. Registry row - gate-registry.json row `live_check_demand`: question / wait / window_acceptance, closed_by role:qa-code-critic + person, addressee
   role:qa-code-critic, vocabulary code, `unknown.owner: role`, `decides` rewritten, converted, `debt_ref ""`. Sites: `proof_required` re-roled
   `accept` -> `produce` (the E-c table; `--check` refused the converted row with an `accept` site: "calls no acceptable()"), `novelty_of` produce,
   new `novelty_question_owed` produce.
7. Pins (test_gate_registry.py): `EXPECTED_DEBT` -live_check_demand, `EXPECTED_CONVERTED` +it, K-T1.2 "7 gate(s)", K-T1.14 split 19/8/6 -> 20/7/6,
   D13 `GR.analyse` before 140 / after 140 (set of triples unchanged; no comparison of a row word sits in the re-roled / new sites), comment lines
   with card and task. Base main had debt 8 / converted 19 / exempt 6 (t-1032 merged, C3-0 and C3-rr not).
8. `_attach_novelty` marker `novelty_unmeasured` - **NOT done** (question 1). The reader half exists (item 1).

## Verification (witness)
`gate_registry.py --check` (tail, exit 0):
```
A26 gate registry: no violations
  7 gate(s) left as debt:   (stand_identity, provenance_acceptance, test_identity, s5_window, baseline_identity, s5_stand_limits, reporter_rehearsal_identity)
```
`live_check_demand` count in that output: 0 (grep -c). Before: 8 debt, incl. live_check_demand.

Row functions called directly (slow files not run whole):
```
python -B <scratch>/run_rows.py pl   -> 21 PASS lines of the_unmeasured_row_is_a_question_to_the_code_critic (test_proof_level.py), 0 FAIL
  e.g. PASS keyless, flagless row beside a measured row -> asked (E1) / PASS ...with the writer's failure note -> asked (F-T5 a+) /
       PASS ...a marker that is not a string (5) -> not asked (E10) / PASS proof_required over the answer: only `yes` adds, `no` never overrules a flag...
python -B <scratch>/run_rows.py wr   -> 12 PASS lines of c3_b1_novelty_question_gap (test_window_record.py), 0 FAIL
  e.g. PASS E1: ... one gap / PASS E6: a malformed answer on the item never closes it / PASS E4: a handed claim ... not asked /
       PASS E3: an all-keyless manifest ... no gap / PASS E7: `novelty_question` is a kind of the window's word road
python -B <scratch>/d13.py -> PASS D13 (set, count 140), D13 NEG x3; Counter converted 20 / debt 7 / exempt 6; EXPECTED_DEBT and EXPECTED_CONVERTED equal the file
python -B <scratch>/census.py -> PASS test_c1 .. test_c6 (judgment census: 1264 units, breach=0): no new unit, no census edit
```
Negative control (byte copy taken first, `_wanted` branch `if _probe_owed(entry) == "yes": return True` removed, restored from the copy):
```
FAIL proof_required over the answer: ... expected [True, False, False, True, True, False, False], got [False, False, False, True, False, False, False]
FAIL why: an unmeasured keyless row reads `unmeasured` and a `yes` one reads demanded ... got ('unmeasured', 'unmeasured')
sha256 after restore == sha256 of the copy: 64c764940635f59214b5121f1b9443c3d9e191f8ff049a3d331d9c95ec47d174 (both)
```
`scenario_walk.py --witness-for` for proof_level, acceptance, window_record, manifest_put, manifest_from_tests: lists printed (68 distinct files); every
NON-slow file printed was run (`python -B tests/<file>`): test_ledger, test_probe_* (aggregate, languages_plan, languages_ts_playwright, check_records,
marker_judgment, not_proved, readers, replay, target_fact, word_repeat), test_state_exits, test_quality_demand, test_ahead_cards, test_artifact_supersede,
test_check_witness, test_handed_to_person, test_interim_packet, test_manifest_projection, test_manifest_put_assertion_line, test_manifest_put_keep_unsent,
test_manifest_put_merge, test_obligation_join, test_oracle_provenance, test_provisional, test_s5_precheck_sides, test_stand_gap_remedy,
test_then_remainder, test_validator_class, test_whole_list_sites: all `exit 0`. Slow files (incl. test_proof_level, test_window_record, test_gate_registry,
test_judgment_census as whole files): batch canon.
`selftest.py --lang`: `PASS lang: no Cyrillic anywhere in the package` / `=== qa-factory selftest: 2/2 ok ===`.
`tools/architecture_index.py --check`: `architecture index: up to date (29 invariants, 2682 bytes)`.
`controller-blocks-gen.py` output byte-identical to `design/controller-blocks.md` (same sha256 af229041...): no block route changed.

## RED checks I did NOT make green (both outside owns; a raise is the Lead's)
- `contract_slices.py --check` exit 2: `K10 qa-code-critic: the plugin share is 73,031 bytes, over ... its baseline 72,828 (native_headroom in
  references/role-load.json)`. The charter paragraph is 206 bytes (minimal form); before it the share was 72,825 (under baseline by 3). Needs the
  baseline raised 72,828 -> >= 73,031 (+203), or 203+ bytes freed elsewhere in the charter. STOPPED per the dispatch.
- `stage_joints.py --check` exit 1: `stage-joints: acceptance:novelty_question is a check in code (acceptance.py::validate_window:1213) and has no row
  in references/stage-joints.json - add its producer and where the role is told (FR-38, AR-10)`. `references/stage-joints.json` is not in owns; model
  rows: `acceptance:stale_run` (:686), `acceptance:review` (:806). Producer `window_record.py::build` / `acceptance.py::validate_window`, told:
  `agents/qa-code-critic.md`.

## Divergences of the card from reality (findings)
- `CRITIC_FIELDS` (manifest_put.py:1085) is the key set of an `expectation_changes[]` record's critic fields (used only at :1260 to tell a verdict-only
  patch), NOT the critic's write road for `tests[]` rows. A `tests[]` row's `critic_verdict` is validated nowhere in manifest_put. `probe_owed` rides the
  generic row merge (verified: `MP.merge` keeps `probe_owed` and `critic_note`, and a top-level `novelty_unmeasured` string is taken by the scalar loop
  and overwritten by a later `""`). I added the name to the tuple as the card says; it has no effect there.
- `_attach_novelty` has no handle on the fragment (signature `(story, project, keyed, notes, helpers)`); the fragment is built in `build` after the call.
- The window item carries none of the row's flags (only `change_disposition`), so the gap reads the manifest ROW of the instance
  (`acceptance._manifest_under(root)` + `contract.test_instance_id`) through the predicate; the item's `probe_owed` copy is the second closer. The card's
  "window builder records the owed state" is therefore the copy only; no new item key.

## Questions (design, left to the Lead)
1. Item 8: `novelty_unmeasured` writer. `_attach_novelty` cannot write a fragment key; the least change is an optional out-parameter on `_attach_novelty`
   plus one merge line in `build` (after :1515, also before the early `return` at :1528). `build` is outside the card's owns and the card says the clone
   group of `build` stays unchanged (`dup-baseline.json:92`). Allow that edit, or choose another carrier?
2. Item 4: the value refusal (`probe_owed` outside `yes`/`no` refused naming the field and both values, E6/FR-1). It needs a new function in the style of
   `critic_approval_problems` (manifest_put.py:1684) plus its call in `run`; neither is `CRITIC_FIELDS`. Allow a new function + one call line?
   Until then a malformed value is stored but never read as an answer (the gap stays; tested).
3. Raise the role-load baseline of qa-code-critic (+203 bytes) and add the stage-joints row - Lead's / owners of those files.

## FR walk
A: not touched (no refusal text added; the gap is a window line with its origin and door). B: the gap's door text is a window line for the orchestrator/critic,
not a person question; the person's door is `person_words.door` form (FR-6 unchanged). C: AR-22/FR-38 - reader of `probe_owed` and `novelty_unmeasured` in this
commit, writer of `probe_owed` = the critic's fragment via manifest_put, writer of `novelty_unmeasured` OPEN (question 1); the charter states the answer
(FR-38). D: not touched. E: not touched (delivery reads no new field). F: not touched. G: FR-30 `--lang` pass; FR-32 test rows + registry pin.

## Census / architecture statement
`judgment: none` - the probe-owed decision is the code critic's, accepted at window acceptance; code checks presence and closed value (xref); the gap is
list transport (no unit), census C1-C6 pass with no edit. AR-10, AR-13 (WORD_READ_KINDS, one road), AR-20 (debt -1, converted +1, D13 140 -> 140),
AR-22, AR-28, AR-29.

## Analogs noticed (not fixed)
- Other gap kinds with no `stage-joints.json` row would hit the same refusal - not surveyed.
- `proof_required(item, {})` on a window item cannot see a row's `sensitivity_proof_required` / `new_or_changed` (items copy only `change_disposition`): an
  existing blind spot; this card's gap uses the row for that reason.
- `docs/OWNER_PRINCIPLES_INDEX.md` stale on the base (hook refusal above).

## Beyond the manifest
Read: `references/stage-joints.json`, `references/role-load.json` (via the check), `scripts/slow_tests.json`, `tools/controller-blocks-gen.py`,
`design/controller-blocks.md`, `scripts/tests/test_judgment_census.py`, `scripts/contract.py` (`manifest_tests`, `test_instance_id`, `window_shape_errors`).
Note: `tools/controller-blocks-gen.py --help/--check` took the flags as output paths and wrote two stray files in the worktree root; removed (never staged).

## Retry (attempt 2)

### Items
- D-b1-1 (item 8, writer) - NOT done, returned as a question. Reality diverges from the spec: `_attach_novelty` and `build` with the two
  exits (lines 890, 1515, 1528) are in `scripts/manifest_from_tests.py`, NOT `window_record.py` (`window_record.build` is another function,
  :1429, with no `_attach_novelty`; grep of `window_record.py` for `_attach_novelty|novelty_unmeasured` finds nothing). `manifest_from_tests.py`
  and its test `test_manifest_from_tests.py` are not in owns (owns is normative on writes), and the test rows named for `test_window_record.py` have no code to judge there.
- D-b1-2 (item 4) - done. `CRITIC_FIELDS` back to `("critic_verdict", "critic_note")`; new `manifest_put.probe_owed_problems` (+ `PROBE_OWED_VALUES`), ONE call in `run`
  between the critic-approval refusal and the assertion-line refusal (all before any write). Row named by its `instance_id`, else `index N` (the `_identity` fallback
  is a hash, unreadable). Every bad row in one refusal (E3); non-string values refuse without crash (E2); absent key no refusal (E1).
- D-b1-3 - done. (a) role-load `qa-code-critic` 72828 -> 73031 (re-measured: `contract_slices.py --check` printed 73,031); named in the changelog fragment and commit.
  (b) row `acceptance:novelty_question` in stage-joints.json: producer `acceptance.py::validate_window`; told path `scripts/window_record.py` (NOT `agents/qa-code-critic.md` and NOT
  `scripts/acceptance.py`: the checker refused both - "a code producer is called in a `scripts/*.py` file" / "no call of `validate_window` outside its own definition";
  `window_record.py:1954` is the caller). (c) census row in `driver-exits/s5.json` (joint row + ratchet `unwalked` 31 -> 32; no `raised_by` entry: adding one was refused as a stale raise credit, the base counts it).
- E4 temporal: before this commit `stage_joints --check` exit 1, `contract_slices --check` red (73,031 over 72,828), `dry_exits --check` 1 discrepancy after the joint row alone; after: all green, 0 discrepancies.
- E5/E7: no `build` merge line written, `dup-baseline.json` not touched; no other ratchet turned red.

### Runs (verbatim tails, from the tree)
```
stage_joints.py --check        -> "stage joints: clean"  exit 0
contract_slices.py --check     -> "slices: 44 declared, all present and fresh; 19 key pages; 12 charters carry a generated digest line"  exit 0
dry_exits.py --check           -> "dry_exits --check: 0 discrepancies"
gate_registry.py --check       -> exit 0
selftest.py --lang             -> "=== qa-factory selftest: 2/2 ok ==="
test_manifest_put_merge.py     -> "=== test_manifest_put_merge: 452/452 ok ==="
test_proof_level.py            -> "=== test_proof_level: 607/607 ok ==="
test_window_record.py          -> "=== window record: 684/684 ok ==="
```
Negative control: byte copy of manifest_put.py taken first, call replaced by `probe_problems = []`: 24 rows FAIL ("refused, nothing written" x6, names field/row/values x18), `=== 428/452 ok ===`;
restored from the copy, sha256 before == copy == after: 60250d99d273608bc39cf62332c70de06e0eb4cc25acbab6f2b3e695a1957b15.
Witness scope: the 68-file list of the previous round was not re-run whole; ran the three test files above plus the checks. Other slow files: batch canon.

### FR walk
A: FR-1/FR-2 - the refusal names field, row, both values and the door (send one, or leave the key out). B: not touched (no person text). C: FR-38/AR-22 - reader and the closed-value refusal in one commit; the writer of `novelty_unmeasured` stays OPEN (question). D: not touched. E: not touched. F: not touched. G: FR-30 `--lang` pass; FR-32 test rows; FR-45 refusal before any write, tested.
`architecture:` AR-10, AR-22, AR-20 (named raise), AR-28, AR-29. `judgment: none`.

### Questions
1. Item 1 (D-b1-1): allow `scripts/manifest_from_tests.py` and `scripts/tests/test_manifest_from_tests.py` into owns (the spec names `window_record` by mistake)? Until then no writer of `novelty_unmeasured` exists.

### Analogs
- stage-joints told-path rule: a joint whose producer is a validator needs the CALLER file as told; the form "told in the charter" is not accepted by the checker.
- `driver-exits/s5.json` ratchet `unwalked` is a hand-kept count beside the rows: every new joint row moves it.

### Commit
NOT committed: pre-commit hook refused, verbatim:
```
factory rules index: up to date (59 rules)
factory rules index is stale: run python tools/factory_rules_index.py and stage docs/OWNER_PRINCIPLES_INDEX.md
```
Everything is staged (report included); commit message ready at C:/Users/i_mas/AppData/Local/Temp/msg1051.txt.

## C3-b1w (t-1062) - the writer of `novelty_unmeasured`

Code: `manifest_from_tests._attach_novelty(..., helpers=None, unmeasured=None)` (out-list, default None = old behaviour); `build` passes `unmeasured` and, after `stamp_obligation_refs`, sets `fragment["novelty_unmeasured"] = "; ".join(unmeasured)` only when the list is non-empty.

Unmeasured branches of `_attach_novelty` (enumerated):
1. no keyed rows and no helpers -> early `return []`: nothing to measure, NO marker (E1).
2. keyed empty but helpers present and the call raises -> no marker (no test row exists to be unmeasured; helpers return `unknown`, their own stored value) (E1).
3. the measure raised (or wrong answer length -> ValueError), keyed non-empty -> marker "novelty could not be measured (<Exc>)" (E2; the old note and `_keep_stored_novelty` stay).
4. the call returned, `_novelty_block` is None for a key (V2: non-S0 base and value not new/changed) -> marker "N test row(s) got no novelty block (...)". NOTE for acceptance: this counts "returned no value for a unit" as unmeasured, per the spec; it means every build against a non-S0 base (head_now / no git) with an `unchanged`/`unknown` row now asks the critic the question. If that is too wide, it is one `if` (branch 4) to drop.
5. helper unit answer not a dict -> `unknown` helper value; no marker (not a test row).
Early return near the old line 1528 (`fragment == {}`): structurally unreachable with a marker (fragment empty means no tests/unresolved/bindings, so `keyed` is empty and units are empty; branch 1). So the marker is NOT added there and the early return is unchanged (E6 not triggered; `main` still treats `{}` as "nothing to write"). Spec item 2 asked for the key on that exit too: it cannot ever be non-empty there; asked as a question only if the Lead wants dead code added.

Rows (one block in `_novelty_switch`, file test_manifest_from_tests.py): marker absent when everything measured; marker on normal exit when blocks missing; marker on normal exit when the measure raised; old callers (no out-list) byte-identical return and notes; out-list reason on exception (E2); no marker when no test row (E1); JOIN x3: `proof_level.novelty_question_owed` true for a keyless row with the producer's fragment, false when nothing unmeasured, false once `probe_owed: no` is on the row.

Verbatim runs (from the tree):
- `python -B ai-packages/qa-factory/scripts/tests/test_manifest_from_tests.py` -> `=== test_manifest_from_tests: 549/549 ok ===` (the file IS in slow_tests.json, 79 s; it was run whole)
- `test_proof_level.py` -> `=== test_proof_level: 607/607 ok ===`
- `selftest.py --lang` -> `=== qa-factory selftest: 2/2 ok ===`
- E5 before/after (git stash for before): stage_joints `stage joints: clean` both, same summary line (rows 268, gaps 4); contract_slices `slices: 44 declared, all present and fresh; 19 key pages; 12 charters carry a generated digest line` both; gate_registry check tail identical both; dry_exits (scripts/tests/dry_exits.py) `dry_exits --check: 0 discrepancies` both. Judgment census: `_attach_novelty` row unchanged, no new function added (not run separately; the census test is not in the witness list).
- E4: `python -B tools/dup_ratchet.py --check` scripts: `9 groups, 8 known, 0 new, 0 grown, 1 carried, 1 shrunk/gone (1 diverged)` identical before and after (the carried group is `_has_factory_activity`, unrelated).
- negative control: sha256 of manifest_from_tests.py `e72a6c77efbaea0d...` before; merge line replaced by `pass` on the file after a byte copy -> `=== test_manifest_from_tests: 545/549 ok ===` with FAIL on both "marker" rows and both "question owed" join rows (broke, bare); restored from copy, sha256 `e72a6c77efbaea0d...` equal to the copy's.
- witness-for run (non-slow): test_manifest_put_keep_unsent 91/91, test_manifest_put_merge 452/452, test_oracle_provenance 296/296, test_provisional 76/76, test_then_remainder 354/354, test_proof_level 607/607, scenario cart-1 15/15, scenario dry-1 9/9. NOT run (slow_tests.json): test_blocked_by_env_window, test_brief_pack, test_brief_pack_s5_plan, test_field_producers, test_node_ids, test_s5_precheck, test_window_record, scenario local-1-0108, local-1-arm-b. Not run (fast, listed, skipped by me): test_manifest_from_tests covers; test_manifest_put... all done above; none else.

FR walk: A - no refusal text changed. B - no text to a person changed (marker is data). C - FR-14 shape: one new top-level string key, read by `proof_level.novelty_question_owed` (producer and reader meet, join row). D - FR-59/FR-41: unmeasured is a marker, never recorded as measured-not-novel. E - delivery untouched. F - no measurement code changed. G - FR-30 English only (selftest --lang ok), FR-32 test rows added, FR-54 siblings: other `_attach_novelty` callers none (grep: one call, in build).
Architecture: AR-22 (the reader's field now has a producer, on the normal exit), AR-28 (unknown never becomes a pass); AR-13/AR-14 unaffected.
Needed beyond manifest: proof_level.py, manifest_from_tests main (callers), slow_tests.json, tools/dup_ratchet.py.
