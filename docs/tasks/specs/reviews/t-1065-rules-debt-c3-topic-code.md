# t-1065 — code review of the C3 topic (rules-debt phase 2): C3-0, C3-rr, C3-b1, C3-b1w, integrator

Reviewer: critic (Opus). Tree `C:/QAFactory/forge-repo/.claude/worktrees/agent-aa11322709a274e56`, head `00f1d205`, diff `origin/main...HEAD` (26 files).
Spec: cards C3-0 (:533), C3-rr (:679), C3-b1 (:776) of `docs/tasks/specs/20261117-rules-debt-phase2-cards-spec.md` plus the Lead decisions at :2161, :2173, :2294 and :2301 (D-b1-1..3).

**Verdict: NEEDS WORK. 4 blocking findings (B1-B4), 3 fix-now, 4 notes.** One fix round, in the C3-b1 / C3-b1w files only. C3-0 and C3-rr are fit as they stand. Accepting the work is the Lead's decision. This verdict is an input to it.

## Findings

### B1 — blocking — the person's door for `novelty_question` is dead, and the "recorded, not read" safety net is switched off for it
- Where: `scripts/window_record.py:330-336` (the `GAP_ORIGIN["novelty_question"]` door: "the orchestrator records their words with `waiver.py ... --block "novelty_question:<instance id>"`"); `:1846` (`WORD_READ_KINDS` gains `novelty_question`).
- Trace:
  - All three S5 judges let a gap go only through `word_kept` → `word_let_go`. They are `controller._s5_gap_problems` (controller.py:7510-7516), `story_step` finish (story_step.py:2563) and `window_record` main (window_record.py:2291), which goes through `driver_dispatch.py:1018`.
  - `word_let_go` (window_record.py:1350-1386) lets go only three things: the `not_run` tier4 kinds, the `row_fields` tier4 kinds of `references/word-passed-facts.json` (product, evidence, obligation_*, assertion_identity, defect_location), and `review:<iid>` heads (`_review_owner`, :1265-1270, which matches only `review:` heads).
  - `novelty_question` is in none of these, and it is not `derivable` either (:2310-2313).
  - A grep for `novelty_question` over `scripts/` finds only `acceptance.py`, `proof_level.py` and `window_record.py`. The positive control is the hit in `acceptance.py`. Nothing reads a person's word for this gap.
- Effect:
  - A person who follows the printed door records a word that lets nothing go: the window still exits 1 with the gap.
  - Membership in `WORD_READ_KINDS` puts the line into `read`. So `_unread_words` (:1850) no longer prints "recorded, not read by this window" for it, and the one line that would tell the person their word was ignored is suppressed.
- What this breaks:
  - card E7 ("the person passes every block, by the one road");
  - FR-2 / AR-9 (the door named must be usable);
  - FR-8 (a person's word must not be dropped silently);
  - FR-4 / P13.
  - The only other ways out are the critic's `probe_owed` answer and a typed `unresolved` + `reason` acceptance. So FR-40 holds, but the person's road is false.
- The builder's E7 test (test_window_record.py, `c3_b1_novelty_question_gap`) checks only tuple membership. It never drives a recorded word through `word_kept`.
- Fixed looks like:
  - The S9 road is widened from one kind to a kind tuple. `review_gap_words` / `_review_owner` read heads of `("review", "novelty_question")`, so `word_let_go` lets `novelty_question:<iid>` go, one road with `review` (axis 34).
  - One test row records an S5 override `novelty_question:B` in `pipeline.json` and asserts that `word_kept` (or `controller._s5_gap_problems`) lets the line go, with a negative row (`novelty_question:A` does not let `B` go).
  - If the Lead prefers no person road, remove `novelty_question` from `WORD_READ_KINDS` and drop the person clause from the door text. That deviates from E7 and is the Lead's call.

### B2 — blocking — `test_judgment_census.py` C1 is red: the new refusal unit has no census row
- Where: `scripts/manifest_put.py:1702-1718` (`probe_owed_problems`, a `DV.refusal("manifest_put:probe_owed", ...)` site). Not in `scripts/tests/fixtures/judgment-census.json`.
- Witness (my control re-run on the tree):
  ```
  FAIL test_c1_every_unit_has_a_row_and_every_row_a_unit —
    manifest_put.py::probe_owed_problems is a check unit (u1) with no row in judgment-census.json: add a row {file, function, class, roles, owner} - the class is a judgment about what the unit decides, never defaulted
  === judgment_census: 24/25 ok ===
  ```
- Why it slipped:
  - The builder's census run (attempt 1: "1264 units, breach=0") came before the refusal existed, which was added in attempt 2. Attempt 2 did not re-run the census.
  - The commit line reads `judgment: none`, but the commit adds a data check.
- The batch canon (run 44038264125) will show this red. Axis 32 says a new check gets its census row in the same commit.
- Fixed looks like:
  - One census row `{"file": "manifest_put.py", "function": "probe_owed_problems", "class": "shape", "roles": ["qa-code-critic"], "owner": "data"}`. The precedent is `critic_approval_problems` (census :613, class `xref`). The value check is a shape check, and the Lead/builder picks the class.
  - The fix commit carries `judgment: adds data check manifest_put.py::probe_owed_problems`.
  - Witness: `test_judgment_census.py` 25/25.

### B3 — blocking — a `probe_owed` answer survives a change of the test's bytes, so the question stays closed when nobody answered it for the current code
- Where:
  - `scripts/manifest_put.py:1899-1909`: a writer re-run merges shallowly. The only key it drops is `novelty`.
  - `scripts/proof_level.py:457-473` (`novelty_question_owed`: any closed `probe_owed` returns False);
  - `window_record.py:1574-1577` (the item copy);
  - `acceptance.py:1149`.
- Empirical probe (scratch script `probe_merge.py`, `MP.merge` on the tree): a stored row with `probe_owed: "no"` and `test_code_sha: "AAA"`, then a writer patch (`generated_from`) with `test_code_sha: "BBB"` and no novelty:
  ```
  after writer re-run with new bytes: {'test_code_sha': 'BBB', 'probe_owed': 'no', 'critic_note': 'pre-existing', 'critic_verdict': 'approve'}
  question owed: False proof_required: False
  ```
- When it bites: the next measure gives no block, i.e. a non-S0 base with a committed change, or a project without git. Then the changed test needs no live probe, and nobody is asked again.
- Why the review gate does not cover it: the review goes stale on new bytes (`stale_review`), but `probe_owed` is bound to nothing. The charter tells the critic to answer only "when the window asks", and the window no longer asks.
- What this breaks: this is the converted gate's own class ("a new or changed test must carry a live probe"). It is a closure without an answer (FR-4 / FR-59 / AR-28), the K3 failure mode.
- Fixed looks like: the answer is bound to the bytes it judged. Either:
  - (a) the writer-re-run branch at manifest_put.py:1899 also pops `probe_owed` / `critic_note` when the patch's `test_code_sha` (or `trace_binding.test_content_sha`) differs from the stored row's, the same pattern as the `novelty` pop; or
  - (b) the answer carries the sha it judged (`probe_owed_sha`), and `_probe_owed` reads it as "not answered" when that sha differs from `claimed_test_sha(entry)`.
  - Test row: stored `no` + writer patch with new bytes → `novelty_question_owed` is True again. A control row with the same bytes stays closed.

### B4 — blocking (rule 19 / P31) — rows of a non-Python test file are unmeasured, yet the writer never marks them, so a TS-only story is never asked
- Where: `scripts/manifest_from_tests.py:1346-1392` (`language_rows`). Rows are appended to `tests` (:1390) but never to `keyed`. The builder notes this itself at :1392: "novelty is measured for Python tests only; not measured for this file".
- Trace: `_attach_novelty(keyed=[], helpers=units)` (:906-908) either returns `[]` or measures helpers only, and in both cases the `unmeasured` list stays empty.
  - In a TS-only build, no row has `novelty` and there is no marker. `novelty_question_owed` is False for every row, the legacy silent path.
  - In a mixed Python + TS manifest, one measured Python row makes every flagless TS row asked.
- Effect: whether the same TS row is asked depends on whether a Python file sits in the same story. That is a language exception from the shared mechanism with no data row.
- It also contradicts the `unmeasured` docstring (:900-902): "when novelty could NOT be measured for a test row, the reason is appended".
- The card's E3 frames the unasked case as temporal (in flight). For a non-Python project it is permanent.
- Fixed looks like: `build` appends one reason to `unmeasured` whenever `language_rows` wrote a row, e.g. "N test row(s) of a language the measurer does not read". Test: a TS-only fragment carries `novelty_unmeasured`, and the join row shows a flagless TS row is asked. If the Lead keeps the exclusion, rule 19 needs a named data row or the owner's word in the card. Otherwise this is a proposed node owned by the rules-debt Lead.

### F1 — fix now — the closed answer vocabulary and its reader are written four times
- `PROBE_OWED_VALUES = ("yes", "no")` at manifest_put.py:1702.
- `PROBE_OWED_ANSWERS = ("yes", "no")` at proof_level.py:447, with the reader `_probe_owed`.
- Inline membership reads at acceptance.py:1149 (`item.get("probe_owed") not in proof_level.PROBE_OWED_ANSWERS`) and window_record.py:1574. The acceptance comment even says "The ONE reader is `proof_level.novelty_question_owed`".
- Brief item 6, AR-13 / AR-1: a second copy of a closed vocabulary drifts.
- Fixed looks like: one tuple and one public reader, `proof_level.probe_owed_answer(entry) -> str`, used at all three sites. `manifest_put` imports `proof_level`, which imports only `contract`, so there is no cycle. Drop `PROBE_OWED_VALUES`.

### F2 — fix now — `novelty_unmeasured` is never written as `""`, unlike card item 8 / E10; the marker is sticky and the texts still describe the card
- What the code does: `manifest_from_tests.py:1559-1560` writes the key only when non-empty. My probe shows that a later successful run leaves the stored marker: `marker after a successful run that wrote no key: '1 test row(s) got no novelty block'`. The card's E10 invariant ("asked on the marker only when its last writer run failed") therefore does not hold.
- Not named as a deviation: the builder's report describes the behaviour but does not call it a deviation from item 8.
- Why sticky is still defensible:
  - `build` runs per file subset, so a `""` from a later subset would erase an earlier subset's failure.
  - The row route ("some row carries `novelty`") is monotone anyway.
- Stale texts:
  - the `novelty_question_owed` docstring (proof_level.py:461: "the writer ran and its measurement failed"). Branch 4 is not a failure.
  - the changelog line "a fully measured story carries no such key". The fragment carries none, but the manifest can.
- Fixed looks like: the Lead names the sticky behaviour as the decision, the card's E10 and the docstring and changelog say "sticky: set once a writer run could not measure a row", and the report lists it as a deviation. Or `""` is written as the card says. Recommendation: sticky + text fix.

### F3 — fix now — a stale test label in the merged pins
- `scripts/tests/test_gate_registry.py` K-T1.14 label: "debt lists the seven rows left after C3-R, its fix round and C3-b1". The merged tree has six. The value check is right. Only the label is stale (an integrator auto-merge leftover, the class the integrator reported).
- Fixed: the label says "six" (or names no number).

### N1 — note (answer to K2) — branch 4 also asks rows whose author declared `change_disposition: unchanged`
- The card names only three flags as "flagged" (`_wanted`). A row with `change_disposition: "unchanged"` and a `change_basis_ref` is flagless.
- At a non-S0 base or without git, it gets no block (V2) and the manifest is marked, so it is asked. The window test's own item uses `change_disposition: "unchanged"` and gets the gap.
- Direction: correct under FR-59 / AR-28. No measurement exists, the author's word alone would switch the probe off, and asking the critic (a tier above, AR-29) is the safe side. Nothing is asked where a measurement exists, because an S0 base stores `unchanged` blocks and those rows are not asked.
- Cost: one critic field per such row per story, and the answer persists (B3 bounds it to the same bytes).
- The card should say this case out loud. It is not a defect.

### N2 — note, outside the diff, queued — the F-b detector is a pair detector not scoped to its own carrier (rule 15)
- `gate_registry.py:235-236, :837-841`: a converted accept site passes if its body calls anything named `acceptable`, whatever consumer string it passes.
- A site registered under row R that calls `acceptable(x, "<other row>.<c>")`, or a different function named `acceptable`, satisfies the check.
- C3-rr's call names its own consumer, so this diff is correct. The detector would not catch a wrong one.
- Proposed node for the rules-debt pile (the Lead opens it): require the call's first literal consumer to be a key of R's `accepts`.

### N3 — note — two closers of the same answer, and a second manifest read
- `validate_window` closes the question on the item's copy and on the manifest row. The copy is redundant with the row read, and F1 at least makes both one reader.
- The manifest is read up to twice per call (`red_by_requirement`'s `_manifest_under(root)` at acceptance.py:1129 and the new lazy read at :1146). Cheap, and not a blocker.

### N4 — note — the stage-joints `told` path
- `references/stage-joints.json` row `acceptance:novelty_question` names `scripts/window_record.py` as `told`, while the role is told in `agents/qa-code-critic.md` (the checker refuses a charter path, per the builder's analog).
- AR-10 holds in the text. The checker's told-path form is an analog for the stage-joints owner, as the builder reported.

## Answers to the acceptance keys

**K1 — fit to the cards.**
- C3-0: fits.
  - Items 1-9 are met: the predicate, the error direction, `registry_problem`, the covers line, the registration, the F4 copy-row control with an added clean control, and D13 140 → 146 named.
  - Extra rows (`padded`, `bytes`, `consumer-malformed`) only add coverage.
  - Audit A1 "gate_template reachable from nothing" is closed by C3-rr's import.
- C3-rr: fits.
  - Item 2 is the exact line, with the hit checks first (E3).
  - Item 3: all rows, including absent / other_key / registry via `_READ`.
  - Item 4: debt -1, D13 146 → 145.
  - Deviation: K-T1.13 rewritten under a Lead decision, see K5.
- C3-b1: deviates in three places.
  - Item 3 reads the manifest row rather than "the window builder records the owed state". The builder named this, and it is acceptable.
  - Item 4 was replaced by D-b1-2: done.
  - E7 is not met (B1).
  - `proof_required` re-roled accept → produce, required by `--check`. This is consistent with the E-c table "no predicate".
  - Also open: B2, B3, F1.
- C3-b1w:
  - D-b1-1's "both exits": the early return at :1541 cannot carry a marker (the builder's argument holds: that exit needs an empty fragment, and therefore an empty `keyed`). Acceptable as named.
  - Open: item 8's `""` (F2) and the language rows (B4).
- Integrator: the pins re-derive (K6). One stale label (F3).

**K2.** Branch 4 is the right direction under FR-59 / AR-28. The deciding inputs:
- base kind ≠ `s0` (a story in flight, or no git);
- the measured value is `unchanged` or `unknown`, so V2 stores no block;
- the row carries none of the three flags, `change_disposition: unchanged` included (N1).

It never fires with a recorded S0 base (blocks are stored), on a flagged row, or on a handed row. "Nothing was owed" is not established in those runs. Code cannot know novelty there, so asking is the declared safe side, not overreach.

**K3.** The three producers:
- (i) Top-level `novelty_unmeasured`: asked, with doors `probe_owed` yes/no (the critic) and an `unresolved` acceptance. The person door is dead (B1).
- (ii) A `tests[]` row with `novelty`: its flagless keyless siblings are asked. Same doors.
- (iii) Both absent: never asked. But the writer itself produces this state for unmeasured non-Python rows (B4).

Closed without an answer: yes, a stale `probe_owed` after a byte change (B3). A malformed value never closes the question (E6, tested) and is refused at write (D-b1-2, tested). Every recorded state has a move, so FR-40 holds. FR-4 is broken by B1 and B3.

**K4.** For converted rows, `gate_template.acceptable` is now the only reader of a true accept site:
- `gate_registry --check` exits 0 with no F-b line.
- A grep for `"same_command"` over `scripts/*.py` finds only the producer (`onboarding_probe.py:394`), the text table (`gate_preflight.py:4076`) and `profile_contract.selector_contract:417`. The last is the known waiting finding (selector, not reuse), named in the card's siblings.
- `profile_contract.acceptable_provenance` stays the named provenance survivor (F-T2).
- The remaining debt rows (test_identity, s5_window, baseline_identity, provenance_acceptance, stand_identity, s5_stand_limits) are queued under C3-b2/d/g/k/h/j.
- Analog: N2 (the detector does not scope the consumer).

**K5.** The old NEG proved that A1 can call gate_registry.py dead. The fake-root NEG still proves it: no CLI line and no importer, then named. The live row now proves import-liveness. The AST chain facts, with a positive control, state why.
- Still guarded: "the CLI_SCRIPTS line is there" (unchanged row) and A1 over the live tree (the K-T1.13 first row; `audit_factory` A1 runs in the integrator witness).
- Newly unguarded: nothing that was guarded before. Removing the CLI line no longer fails a test, because the file is alive by import, which is A1's own rule.

**K6.** Re-derived from the registry file:
```
python -B -c "...collections.Counter(r['status'] for r in d['rows'])..." gate-registry.json
Counter({'converted': 21, 'debt': 6, 'exempt': 6})
['stand_identity', 'provenance_acceptance', 'test_identity', 's5_window', 'baseline_identity', 's5_stand_limits']
```
This equals the pins (21 / 6 / 6) and `EXPECTED_DEBT` in order. The K-T1.14 pins compare literals to the counted file, so they are ratchets, not restatements of the code. D13 145 is confirmed by my `test_gate_registry` re-run (493/493).

**K7.**
- The charter line is the card's item-5 sentence verbatim, 206 bytes, and the minimum that names the gap word, both answers and the note. AR-10 holds.
- The raise 72828 → 73031 is named in commit 61dc7fd7 (`architecture: AR-20 -- one named raise ...`) and in `changelog.d/rules-debt-c3-b1-novelty-question.md`. K1b (FV2-79) is queued.
- If B1 is fixed by text only, the charter needs no change.

**K8.**
- `test_controller_rework_repair_binding.py`: not on the path. The failing check is "resume existing dispatch", from `controller.validate` (controller.py:5526). The test imports `controller`, `event_store` and controller fixtures, none of which changed. The controller has no top-level import of `gate_preflight`. The integrator ran it 235/235 locally.
- `test_probe_by_code.py` (timeout): not caused.
  - The red was on the head before the integrator, i.e. C3-0 + C3-rr only. `probe_by_code` imports `proof_level` and `acceptance` but not `gate_preflight` / `gate_template` / `gate_registry` (grep).
  - After the merge, C3-b1 adds at most one extra manifest read per `validate_window` call that reaches the branch. Not a 300 s cost.
- `test_stage_guard.py` CX1-20 (a time ratio): not on the path. `stage_guard.py` imports none of the changed modules (the only `gate_preflight` hit is a comment, :793).

**K9.**
- Class completeness against the map:
  - Axis 32 (census): broken by B2.
  - Axis 34 (one road): broken by B1 (person road) and B4 (language).
  - Axis 38 (dry census): covered, with the row in `driver-exits/s5.json` and `unwalked` 31 → 32. `dry_exits --check` 0 is in the integrator's witness.
  - Axis 23 (row fields): `probe_owed` is optional, not a required field. `contract.WINDOW_INSTANCE_FIELDS` (contract.py:5618) is a required-presence list, so an extra item key is fine.
  - Axis 5 (rows ↔ prose twins): the `live_check_demand` `decides` was rewritten. No prose twin outside the charter names the old "shown as a debt" wording, as far as the card read. Not re-scanned (rule 5).
  - Axis 7: n/a.
- Duplication: F1 (four copies of the answer vocabulary/reader) and N3 (two closers).
- Dead code from the merge: none found. The K-T1.13 old row is removed, the `_reporter_outcome` triple removed, and the conflict hunks are resolved without leftovers (diff read whole).

**K10.**
- AR-13 / AR-15 / AR-28 / AR-29 / AR-20 / AR-22 are kept for C3-0 and C3-rr.
- C3-b1: AR-22 is kept for `probe_owed` (writer: the critic's fragment through manifest_put; readers: proof_level and window). AR-28 is broken by B3 and B4. AR-24 / FR-8 are broken by B1.
- Every new check is a data check: membership of a word in a row (`acceptable`), presence and closed value (`probe_owed_problems`, `novelty_question_owed`), and a manifest-level presence marker. The judgment "is a probe owed" goes to the code critic (P27, AR-29). The census row is missing (B2), not a judgment in code.

## Duplication and consistency
F1 and N3, from these greps: `PROBE_OWED|probe_owed` over `scripts/*.py`, `"same_command"` over `scripts/*.py`, and `novelty_question` over the package.

## Code quality
- `gate_template.py` is clean: never raises, the cache is explicit, and `registry_problem` is separate.
- The C3-b1 comments overclaim in two places: "ONE reader" (F1) and "the S5 exit reads a person's recorded word" (B1).

## One action, one road
- B4 is a language exclusion with no data row. Per rule 19, it is a fix this round or a proposed node owned by the rules-debt Lead.
- B1 is a second road: a person's word is promised and not read.

## Tests
- Commit `tests-over:` lines are present (C3-0 a4aca646, C3-rr via 0d97e8bf, C3-b1 61dc7fd7, C3-b1w e2b8c416, 1017d41c), and the reasons hold: parameterised tables, one per behaviour.
- Missing tests:
  - B1: the person's word driven through `word_kept`;
  - B3: the stale answer after a byte change;
  - B4: the TS-only marker.

## Per node
- C3-0 (t-1038): accept.
- C3-rr (t-1055): accept.
- C3-b1 (t-1051): accept after fixes — B1, B2, B3, F1 (F2's text lines too).
- C3-b1w (t-1062): accept after fixes — B4, F2.
- Integrator (t-1064): accept after fixes — F3 (label only).

## Control re-runs (verbatim last lines; run from `( cd <tree>/ai-packages/qa-factory && ... )`)
- `python -B scripts/tests/test_gate_registry.py` → `=== test_gate_registry: 493/493 ok ===`
- `python -B scripts/tests/test_proof_level.py` → `=== test_proof_level: 607/607 ok ===`
- `python -B scripts/tests/test_manifest_put_merge.py` → `=== test_manifest_put_merge: 452/452 ok ===`
- `python -B scripts/tests/test_manifest_from_tests.py` → `=== test_manifest_from_tests: 549/549 ok ===`
- `python -B scripts/gate_registry.py --check` → exit 0
- `python -B scripts/tests/test_judgment_census.py` → `=== judgment_census: 24/25 ok ===` (exit 1; B2)
- Registry count (K6) → `Counter({'converted': 21, 'debt': 6, 'exempt': 6})`
- Probe `probe_merge.py` (scratchpad, `MP.merge` + `PL.novelty_question_owed`) → the B3 and F2 lines quoted above.
- Not run: `test_gate_preflight.py`, `test_window_record.py` (slow; the batch canon).

## Trail (read)
- The diff of all code, test and registry files (whole).
- Cards C3-0 / C3-rr / C3-b1 and the Lead decisions :2161-2316.
- The four reports.
- `manifest_from_tests.py` :820-960, :1346-1400, :1470-1561.
- `manifest_put.py` :1793-1935, :1990-2005.
- `window_record.py` :305-370, :1265-1430, :1836-1880, :1960-2030, :2280-2345.
- `controller.py` :2455-2482, :7005-7030, :7140-7166, :7440-7520.
- `acceptance.py` :1070-1090.
- `gate_registry.py` :815-845, plus grep :235.
- `word-passed-facts.json` :1-40.
- `judgment-census.json` :1-8, plus grep.
- `contract.py` :5618-5621.
- `test_gate_registry.py` :840-900.
- `harness.py` check_in.
- `audit_factory.a1_findings` head.
- The imports of `probe_by_code.py`, `test_probe_by_code.py`, `test_controller_rework_repair_binding.py` and `stage_guard.py`.
- `docs/SIBLING_MAP.md` axes 23, 25, 32, 34 and the axis list.
- `tools/critic_verdict.schema.json`.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "B1 window_record.py:330-336,:1846 - the person door for novelty_question is read by no judge (word_let_go lets go only tier4 kinds and review heads; not derivable), and WORD_READ_KINDS membership suppresses the recorded-not-read note (FR-2, FR-8, card E7)",
    "B2 manifest_put.py::probe_owed_problems has no judgment-census row: test_judgment_census C1 red 24/25 (axis 32); judgment line must say adds data check",
    "B3 manifest_put.py:1899-1909 - probe_owed survives a writer re-run on new bytes (probe: test_code_sha BBB keeps probe_owed no; question owed False): the answer is bound to no bytes (FR-4, FR-59)",
    "B4 manifest_from_tests.py:1346-1392 - non-Python rows are unmeasured but never marked: a TS-only story is never asked, a mixed one is (P31, rule 19)"
  ],
  "fixes": [
    "B1: put novelty_question on the S9 head road (review_gap_words/_review_owner over a kind tuple) plus a word_kept test row with a recorded override and a negative row; or the Lead drops the person door and the WORD_READ_KINDS entry",
    "B2: census row for manifest_put.py probe_owed_problems (owner data) and judgment: adds data check in the fix commit; witness test_judgment_census 25/25",
    "B3: drop probe_owed/critic_note in the writer-re-run merge branch when test_code_sha changes, or bind the answer to the judged sha; test row stored no plus new bytes gives owed True",
    "B4: build appends an unmeasured reason when language_rows wrote rows; test TS-only fragment carries novelty_unmeasured and the join asks a flagless row",
    "F1: one tuple and one public reader proof_level.probe_owed_answer used by acceptance.py:1149, window_record.py:1574, manifest_put; drop PROBE_OWED_VALUES",
    "F2: Lead names the sticky novelty_unmeasured as the decision and the card E10, the novelty_question_owed docstring and the changelog say so (or write the empty string per card item 8)",
    "F3: test_gate_registry K-T1.14 label says six debt rows, not seven"
  ],
  "class_completeness": "Axis 32 broken (B2); axis 34 broken by B1 (person road) and B4 (language); axis 38 covered (s5.json row, unwalked 31 to 32); axis 23 n/a (probe_owed optional, WINDOW_INSTANCE_FIELDS is a required-presence list); axis 5 decides rewritten, prose twins not re-scanned; axis 7 n/a. Outside the diff: the F-b pair detector does not scope the consumer to its row (gate_registry.py:235, :837) - proposed node, Lead opens it. K4: gate_template.acceptable is the only accept reader of converted rows; profile_contract.selector_contract:417 and acceptable_provenance remain as named waiting findings.",
  "trail": {
    "read": [
      "git diff origin/main...HEAD (code, tests, registry, references, charter)",
      "docs/tasks/specs/20261117-rules-debt-phase2-cards-spec.md :533-917, :2161-2316",
      "docs/tasks/specs/reports/20261117-rules-debt-c3-0|c3-rr|c3-b1|c3-integrator-report.md",
      "scripts/manifest_from_tests.py :820-960, :1346-1400, :1470-1561",
      "scripts/manifest_put.py :1793-1935, :1990-2005",
      "scripts/window_record.py :305-370, :1265-1430, :1836-1880, :1960-2030, :2280-2345",
      "scripts/controller.py :2455-2482, :7005-7030, :7140-7166, :7440-7520",
      "scripts/gate_registry.py :815-845; references/word-passed-facts.json :1-40",
      "scripts/tests/fixtures/judgment-census.json (head, grep); scripts/contract.py :5618-5621",
      "scripts/tests/test_gate_registry.py :840-900; scripts/tests/harness.py check_in",
      "imports of probe_by_code.py, test_probe_by_code.py, test_controller_rework_repair_binding.py, stage_guard.py",
      "docs/SIBLING_MAP.md axes 23, 25, 32, 34"
    ],
    "reruns": [
      {"command": "python -B scripts/tests/test_gate_registry.py", "result": "=== test_gate_registry: 493/493 ok ==="},
      {"command": "python -B scripts/tests/test_proof_level.py", "result": "=== test_proof_level: 607/607 ok ==="},
      {"command": "python -B scripts/tests/test_manifest_put_merge.py", "result": "=== test_manifest_put_merge: 452/452 ok ==="},
      {"command": "python -B scripts/tests/test_manifest_from_tests.py", "result": "=== test_manifest_from_tests: 549/549 ok ==="},
      {"command": "python -B scripts/gate_registry.py --check", "result": "exit 0"},
      {"command": "python -B scripts/tests/test_judgment_census.py", "result": "=== judgment_census: 24/25 ok === (C1: probe_owed_problems has no row)"},
      {"command": "registry status count (python -c over gate-registry.json)", "result": "Counter({'converted': 21, 'debt': 6, 'exempt': 6})"},
      {"command": "scratch probe_merge.py (MP.merge + PL.novelty_question_owed)", "result": "probe_owed no survives test_code_sha AAA to BBB; question owed False; stored marker kept after a run without the key"}
    ]
  }
}
```
