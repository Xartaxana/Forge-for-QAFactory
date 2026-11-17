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

## Fix round after critic t-1065

Commit: one commit on `worktree-agent-aa11322709a274e56` (sha in the handoff message). Nothing pushed.

- B1 done. `window_record.py`: `GAP_WORD_KINDS = ("review", "novelty_question")`; `_review_gap_head(iid, kind)`, `_review_owner(text, ids, kind)`, `review_gap_words` and `word_let_go` read both kinds by the one head road. `review_gap_words` keys: bare instance id for `review` (unchanged, so controller.py and the old rows are untouched), `(kind, id)` tuple for `novelty_question` (a tuple cannot collide with an id). Test row: `c3_b1_novelty_word_road` (test_window_record.py), driven through `word_kept` with a recorded `pipeline.json` word; edges: word for A does not let B go, kinds do not cross both ways, malformed heads, `*`, no word. Negative control: with window_record.py reverted to HEAD, `FAIL B1: novelty_question:B lets go the novelty line of B - expected ['novelty_question:B'], got []` (`=== window record: 688/693 ok ===`); sha256 before and after restore `fead36a1f165ebce22c9de8a8754b44474db7553f0d40c527aa45cf8d5ae5e48` (copy identical).
- B2 done. Census row `manifest_put.py::probe_owed_problems` (shape, qa-code-critic, data) placed alphabetically; no key/ceiling move demanded. `test_judgment_census.py` 24/25 -> 25/25.
- B3 done. `manifest_put.py` writer re-run branch (inside `WRITER_MARK in patch`), new `_test_bytes_changed(stored, patch)`: fields compared are `trace_binding.test_content_sha` and `test_code_sha` (each only when the PATCH carries it; stored missing = differing). Drops `probe_owed` and `critic_note` (unless the patch itself carries them). Row: `c3_b1_probe_owed_bound_to_bytes` (test_manifest_put_merge.py): new code sha, new binding sha, stored without sha -> owed True; same sha, same binding sha, patch without sha, role patch -> stays; first write. Negative control (the `if` forced to False): `FAIL B3: new test_code_sha -> the answer is dropped: question owed - expected True, got False` (`462/468`); sha256 before and after `875245678886e9a61671db1fb03d730dab46624d44f3f7b49614d02a0ab72dad`.
- B4 done. `manifest_from_tests.build` counts rows `language_rows` wrote and appends one reason `"<N> test row(s) of a language the measurer does not read"` to `unmeasured` after `_attach_novelty`. Rows in `ep1_37`: ts-only fragment carries the marker (2 rows) and the join asks a flagless ts row (closed answer ends it); mixed py+ts carries the reason once; py-only build carries none.
- F1 done. `proof_level.probe_owed_answer(entry)` (public, over `PROBE_OWED_ANSWERS`); used in manifest_put (`PL`), acceptance.py, window_record.py; `PROBE_OWED_VALUES` dropped. Rows: test_proof_level.py "F1: ..." (reader values; tuple; no second copy in manifest_put). Old rows of the three sites unedited and green.
- F2 done, DEVIATION from card item 8 / E10: the marker is STICKY, `""` is not written. Reason: `build` runs per file subset, so a `""` from a later subset would erase an earlier subset's failure. Texts fixed: `novelty_question_owed` docstring, the `build` comment, changelog. Row: "F2: the marker is sticky" in test_manifest_put_merge.py.
- F3 done. test_gate_registry.py K-T1.14 label says "six". Label only, no row can fail on it.
- 8 done. `process_ratchet_tokens.qa-code-critic` 21173 -> 21224 (measured by test_role_load: "carries 21,224 process tokens"; charter untouched, bytes ceiling 73031 not touched). test_role_load.py 184/186 -> 186/186; test_audit_rules.py 375/375. Named in the commit (`architecture: AR-20`) and the changelog fragment.
- 9 PARTLY done, 2 reds left, returned as a question. Deviation: `stage-joints.json` has NO `pins` block (grep `pins` over it: no hit; the pin `PINS` is a literal in test_stage_joints.py), so only the test file changed: PINS window 27 -> 28, universe 40 -> 41 keys, `window 27` -> `window 28` in the summary check, rows 267 -> 268 (label "+1 acceptance:novelty_question, C3-b1"), `[8, 5, 27]` -> `[8, 5, 28]`, `code-to-code rows: 26` -> `27`. test_stage_joints.py 327/340 -> 338/340. Remaining FAIL lines, verbatim:
  - `FAIL K1-A24/at-baseline: the A24 and literal ids a role can meet and no row covers equal the baseline - expected [], got ['rowless is 4, baseline 3: add a row for guard_pre_tool:PT-doctor-probe, manifest_put:probe_owed, stage_done:SD-stage-done... ` (ids: guard_pre_tool:PT-doctor-probe, manifest_put:probe_owed, stage_done:SD-managed-stage, stage_done:SD-stage-close)
  - `FAIL K4/at-baseline: bare/tagged of every role-reachable unit at or under its baseline - expected [], got ['manifest_put.py::run: bare is 17, baseline 16']`
  Both come from the C3-b1 refusal `manifest_put:probe_owed` (a new id with no joint row; one more bare site in `run`), and the fix lives in the told-ratchet fixture or a new joint row: a design decision, not a pin of the added row `acceptance:novelty_question`.
- 10 done: test_role_load, test_audit_rules, test_stage_joints, test_judgment_census run.

### Verification (verbatim tails; each `( cd <tree>/ai-packages/qa-factory && python -B scripts/tests/<file> )`)
```
=== window record: 693/693 ok ===
=== test_manifest_put_merge: 468/468 ok ===
=== test_proof_level: 610/610 ok ===
=== test_manifest_from_tests: 553/553 ok ===
=== test_gate_registry: 493/493 ok ===
=== judgment_census: 25/25 ok ===
=== role_load (the one measure of a role's start load): 186/186 ok ===
=== audit rules (A1/A9/A11/A13/A14/A17/A20/A21/A22/A27): 375/375 ok ===
=== test_stage_joints: 338/340 ok ===
gate_registry.py --check -> exit 0
selftest.py --limits --lang -> === qa-factory selftest: 4/4 ok ===
```
scenario_walk named many more files (scenario stories, keep rows); not run here, they belong to the batch canon.

### FR walk
- A (refusals): the `probe_owed` refusal keeps its text and door; no new refusal. The person's door for `novelty_question` is now one the word can use (FR-2).
- B (text to a person): door text unchanged; not touched.
- C (contracts): F1 gives one reader (FR-17/AR-13); producer and readers (`manifest_put`, `acceptance`, `window_record`) changed in one commit.
- D (identity): the answer is bound to the bytes it judged (FR-4/FR-59); an unknown (stored row without sha) is the safe side.
- G (code): English only; no control bytes; tests are rows of existing scenarios; sibling sweep in item list below.

### Analogs noticed (not widened)
- controller.py:7544 builds the `passed` records only for `review:` lines; a `novelty_question` line let go by a person's word gets no such record (outside owns). 
- story_step / driver_dispatch call the same `word_kept`, so they read the new kind with no change.
- The two stage_joints reds above (rowless ids, `run` bare) are the same C3-b1 class.

### Step 2 after the Lead's answer (joint row for `manifest_put:probe_owed`) - NOT committed, one question open
- Merge of origin/main: clean, committed (merge commit on the branch; told-ratchet `rowless` is now 1, only `guard_pre_tool:PT-doctor-probe`).
- Done in the working tree (uncommitted): joint row `manifest_put:probe_owed` in `references/stage-joints.json` (copy of `manifest_put:critic_approval`, roles qa-code-critic, told page); stage-joints pin rows 268 -> 269; dry census row `manifest_put:probe_owed` (unwalked, group s5, unwalked 32 -> 33) -> `dry_exits.py --check` 0 discrepancies; `contract_slices.py --write` regenerated `references/slices/qa-code-critic/handoff-keys-2.md` (needed by A9; outside the named owns); role-load: process ratchet qa-code-critic 21224 -> 21250 and `native_headroom` qa-code-critic 73031 -> 73134 (both measured, the row adds text to the critic's slice); changelog updated.
- BLOCKED: the site tag. `DV.with_check(text, "manifest_put:probe_owed")` in `run` makes the unit state `tagged` 1 against the told-ratchet baseline 0 (`manifest_put.py::run: tagged is 1, baseline 0`) and the plain print is `bare` 17 against 16. Moving the print to a helper `_refuse_probe_owed` (tagged, no baseline row needed) moves the refusal out of `run` (bare 16, tagged 0) but the helper is a new census unit: `test_judgment_census` C3 `blocking_per_role.conductor is 749, above its ceiling 748` (or `qa-code-critic 94 > 93` with that role). Every tag/no-tag form needs one named raise of a shrink-only ratchet; the only raise-free form is `refuse(..., DV.refusal(...))` (a `sourced` site), which changes the exit code and output of the refusal. Decision wanted.

### Step 2 resolved: form (c), the sourced site (Lead's answer)
- `manifest_put.py::run`: `return refuse("manifest_put.py --fragment", DV.refusal("manifest_put:probe_owed", _problems_text(...)))` (the form of the other sourced `refuse` sites). Exit is now `role_cli.EXIT_REFUSED` (2) instead of `EXIT_BAD_FRAGMENT` (3); the printed `expected:` / `door:` come from the joint row (`A tests[] row's probe_owed is yes or no.` / `send yes or no`; read as truthful for the closed answer). No helper unit, so no census row and no ratchet raise: told-ratchet.json untouched, `blocking_per_role` untouched.
- Test rows updated (`c3_b1_probe_owed_value`): exit pinned to `RC.EXIT_REFUSED`, and the expected / door lines are taken from `DV.refusal("manifest_put:probe_owed", "x")` (the row), not from the output; a row checks the joint row is readable and says `yes` or `no`.
- Other readers of the old text/exit: none. Command: `grep -rn "probe_owed" scripts references agents -l` (minus tests) gives acceptance.py, manifest_put.py, proof_level.py, window_record.py, gate-registry.json, the slice, stage-joints.json, qa-code-critic.md: all read the answer, none the refusal text or exit 3; `grep -rn "EXIT_BAD_FRAGMENT\|MP.EXIT"` outside manifest_put.py hits only test_manifest_projection.py (other refusals). Positive control: the same grep style found the slice `handoff-keys-2.md:12` for `manifest_put:probe_owed`.
- Raises named in the commit (measured): `process_ratchet_tokens.qa-code-critic` 21224 -> 21250; `native_headroom.qa-code-critic` 73031 -> 73134 (the joint row's slice text).
- Witness: test_stage_joints 340/340; judgment_census 25/25; role_load 186/186; audit rules 375/375; test_gate_registry 493/493; test_manifest_put_merge 481/481; contract slices 522/522; `dry_exits --check`: 0 discrepancies; `stage_joints --check`: clean; `contract_slices --check`: 44 declared, all present and fresh; selftest `--limits --lang` 4/4.
