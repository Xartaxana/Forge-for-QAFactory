# t-1084 — code critic, topic C3 wave: C3-b2 (t-1080, `18f585f5`), C3-d (t-1081, `1637ce7c`), C3-reg-precondition (t-1082, `c50ca830`)

The topic got one critic pass (R13-g). The third card came in as a mid-task addition from the coordinator. I read each commit through `git show <sha>` or a `git archive` snapshot in the scratchpad. I did not read any working tree, and I did not review the t-1083 merge.

## Verdict per card

- **C3-b2 (t-1080): accept with fixes.** No fix blocks the merge. Fixes 1 and 3 are queue items for the Lead.
- **C3-d (t-1081): accept.** No fix of its own. It shares fix 1 (`_bound_to`, an accept site reached from inside `validate_window`) and fix 3 (waiting findings to file).
- **C3-reg-precondition (t-1082): accept with fixes.** Fix 4 is a fix of this round and does not block the merge. Fixes 5 and 6 are queue items for the Lead.

Nothing blocks. Whether to accept is the Lead's decision (rule 6).

## Numbered fixes

1. **`acceptance._bound_to` is a `test_identity` accept site that is not converted, not registered and not queued.** Location: `acceptance.py:204-211` at `1637ce7c`; its test is `if proof_level.same_test(...)` truthiness. `validate_window` uses it to accept a review (:1165, :1171, :1175) and a probe (:1228). The probe use means "a probe still speaks for this test", which is exactly the row's `decides`. SIBLING_MAP axis 7 names it under "Recorded-carrier readers". A26 cannot see it: it compares no literal. The card's E-c table and its class sweep (t-1033) cover only `proof_level`. Under C3-0 E9 ("a second acceptance reader is a finding"), it should have been in scope.
   - Why it does not block: on an unreadable registry every ran instance already gets `review:<iid>` from C3-d before the review's `_bound_to` runs. C3-reg-precondition also stops the dispatch first. So no window closes falsely today.
   - Line for the Lead: `acceptance._bound_to: route same_test through gate_template.acceptable (register acceptance.py:_bound_to accept under test_identity, consumer e.g. test_identity.review_bound) | узел: <new node, rules-debt>`.
   - The other axis-25 twins: `acceptance.green_on_current_bytes_why:177` (`!= "raw"`) and `run_history.py:221,256` (`compare_identity(...) == ("same","content")`). The axis-25 text says these are queued ("batch 3, finding AR-13/AR-22 remainder"). I did not open that batch to confirm the row exists. The Lead should confirm it, or put them on the same node.
2. **(C3-b2, quality, queue)** The "registry cannot be read" sentence has four forms:
   - `proof_level.py:947-948`, two constants;
   - `execution_request.py:2108`, an inline literal;
   - `controller.py:5549`, C3-reg-precondition.

   The card prescribed each text, and C3-b2 does not own `gate_template.py`, so this is not a defect of this round. One builder for the prefix (for example `gate_template.registry_why(tail)`) would keep the texts from drifting apart (P31, AR-16 spirit). Line: `one builder for the "gate registry cannot be read (<reason>): a factory defect, ..." text family | узел: <rules-debt, low>`.
3. **(C3-b2 and C3-d) The R12 waiting findings are reported but not filed.** The cards say "one finding each":
   - (a) the `probe_verdict` words accepted inside converted accept sites (`already_probed`, `_product_receipt_repeat`, `validate_window:1211`). A later fix needs a function split;
   - (c) the critic's review word is read outside the registry: `check_delivery.py:860`, `case_stamp.APPROVING` / `report_facts.APPROVING`, and the per-kind rule copies at `window_record.py:1641,1742` and `GAP_ORIGIN["review"]`;
   - (d) delete or wire `holds_over_comments`.

   I searched with `grep -rilE "approving|holds_over_comments|function split|probe_verdict"` over `plans/piles/rules-debt/` and got no hits. The positive control `s5_window` hit 3 files. The root checkout may be stale, though. The Lead files these three (`findings/` plus a row), or confirms they already exist on main.
4. **(C3-reg, fix this round) Row `malformed-first` tests a stub, not the invariant.**
   - Location: `test_controller_state.py:2283` (the row) and :2322 (`controller_module.validate_record = (lambda *a, **k: None)`), with the assert at :2332 (`str(got) == "dispatch contract incomplete"`).
   - The problem: the Dispatch schema requires the same seven keys, with `minLength: 1` on `input_hash` (`references/record-schemas.json:174-200`). So `validate_record` raises `ValueError` first, and `dispatch contract incomplete` cannot be reached through `apply`. The row asserts a message only a stubbed world produces. What it pins is the source position relative to dead code, which is a pin on source shape (TESTING.md «Что не пишется»; P20). Moving the block between `validate_record` and `required` would change no behaviour, yet this row would go red.
   - What the row should be: no stub. Keep the registry broken, drop `input_hash` (one variant with `input_hash: ""`), and expect `type(got) is ValueError` with `not str(got).startswith("gate registry unreadable")`. Expected from: E4 (i) and FR-46 (the call's fault before the install's). That tests the real door. A broken registry never hides a malformed request, so the POSITIONAL invariant is kept through `apply`.
   - The dead `required` check is an analog: the builder reported it. Keep it as belt-and-braces, or queue its removal.
5. **(C3-reg, queue; D3 is a standing class, not this card's defect)** Every `_passed_by_person` caller in the dispatch branch discards `passed` (`blocking, _ =` at `controller.py:5548, 5649, 5683, 5698, 5717`). The accept branch records the same kind of pass through `self._record_person_pass(...)` into `state/passed-by-person.jsonl` (`controller.py:2403-2451`, called at :5966, :7146, :7277, ...). That is the FR-4 / P13 carrier. So a person's pass over a dispatch-time block leaves only the `stage_overrides[]` word, and no "passed" line. The card prescribed `blocking, _ =` "as the branch's other blocks do". This block is the most pointed member of the class: a person passing a factory-owned install defect should surface as a factory finding.
   - Line: `dispatch-branch passes are not recorded: route all five dispatch-branch _passed_by_person results through _record_person_pass (after the commit decision, so a later refusal does not leave a pass line for an uncommitted dispatch) | узел: <new node, rules-debt or conductor pile>`.
6. **(C3-reg, queue; D1)** The generated `controller-blocks.md` row is generic. The new row is `validate | StateConflict | raise StateConflict(blocking[0]) | person | raised from the list _passed_by_person has already filtered`.
   - The generic row matches the convention of the other `blocking[0]` rows (184, 204, 294, 312, 313). It is not an AR-9 breach: the refusal text names what is wrong, what is expected and the reinstall door.
   - Correction to the premise of key 3: the refusal text does NOT name the person's door. It says "nothing is wanted from you" (FR-3 intends that). The waiver road appears only in the route table header of `controller-blocks.md` (`person` row).
   - What is lost: a reader looking up "gate registry unreadable" in `controller-blocks.md` finds no row, so card item 2's text (the reinstall door and the `waiver.py --stage <S> --block "gate registry unreadable"` door) is not discoverable there. The precedent for a specific door exists: `tools/controller-blocks-gen.py:351` (`"raise StateConflict(unreadable[0])"`).
   - Owed: a generator entry, plus a distinct local name in `controller.py:5548` (e.g. `registry_blocking`) so the head stays unique. The card accepted the generator's output, and `tools/` is outside the owns, so this is a node, not a blocker. Line: `controller-blocks row for "gate registry unreadable" carries the card item 2 doors (generator entry + unique head) | узел: <rules-debt, low>`.

## Keys

**(1) Each converted site accepts only through the predicate; behaviour is preserved on a readable registry.**
- C3-b2:
  - `already_probed` (:1538, :1554) and `_product_receipt_repeat` (:1424) use `acceptable(same_test(...), "test_identity.probe_repeat")`. `_run_freshness` (:981) uses `run_fresh`; `_evaluate` (:1653) uses `receipt_holds`; `_match` (`execution_request.py:2102-2105`) uses `run_reuse` on `compare_identity(...)[0]`.
  - Literals left in those sites are only the two display flags (`already_probed:1568`, `_evaluate:1663`) and the two state returns of `_run_freshness`. All are allowed (my `GR.analyse` listing, trail).
  - Decision trace: `same_test` returns only {raw, instance, instance_code, file_code, ""} (:888-929). All four non-empty words are class `matched`, and every consumer is `["matched"]`, so the predicate equals the old truthiness exactly. At :981, `same_test` is reached only with both identities kept, so only instance / instance_code / "" arrive, the same set the old `in (...)` accepted. In `_match`, `same` maps to matched, and `different` / `unknown` are refused, so the predicate equals the old `== "same"`. E11 holds: each consumer has one producer.
- C3-d:
  - stopped and gapped use `static_review`, which takes only `not_applicable:static_review`, so it equals `== "unverified"`;
  - handed uses `matched` + `not_applicable:static_review`, equal to the old `{approved, unverified}`;
  - ran uses `matched`, equal to `== "approved"`.
  - The branch order is unchanged. No `"approved"` / `"unverified"` literal is left in `acceptance.py` (grep: only `BLOCKED_REVIEW_VERDICT = "unverified"` at :45, imported by `window_record.py:75`). `HANDED_REVIEW_VERDICTS` has no reader left (grep over the C3-d snapshot: 0 hits; the control `BLOCKED_REVIEW_VERDICT` hits 4). The builder's six-window control is EQUAL, and its negative control is DIFFER.

**(2) Unreadable registry.**
- C3-b2: every reuse is refused. The why names the registry: `_run_freshness` returns `stale` with `WHY_RUN_REGISTRY`, `_evaluate` uses `WHY_RECEIPT_REGISTRY`, `_match` uses its registry sentence at the same rank. None of them claims "bytes differ" or "changed since" (FR-41). The tests pin that with `check_not_in`.
- E1 is held and pinned: identical whole-file fingerprints still reuse in `_match` with the registry broken. That is a POSITIONAL decision, and it is stronger evidence than the identity, so it is no FR-59 breach. The literal E5 phrase "every reuse is refused" is overridden by E1; I note that, it is not a finding.
- The known residue `_stale_receipt` / `probe_freshness` `missing` is named in the card (E8) and the report.
- C3-d: no review word is accepted, so every kind gets `review:<iid>`. The table checks this for every word that would close a review. The plain gap matches the Lead's decision. The gap's door text ("the critic records the verdict") is a dead end only inside a stage that began before; C3-reg-precondition stops new stages.
- C3-reg: `registry_problem()` never raises: an exception becomes a reason, which becomes a stop.
- A pre-existing FR-41 residue I noticed, not caused by the diff: on a readable registry, `_match` gives "instance bytes differ: … was edited" when `compare_identity` says `unknown` (no identity on either side). That reports an unknown as a fact. It is old behaviour (`same_instance_bytes` gave the same why). The Lead may open a low node.

**(3) Option (A) `allow` entries.**
- `('unknown', WHY_RUN_NO_IDENTITY)` and `('unknown', why or WHY_RUN_NOT_COMPARED)` are bare tuple displays in `return` statements (`proof_level.py:973`, :980). They are the freshness STATE handed to `run_freshness`, not a test of a word. `allow` is the right instrument.
- It hides nothing. `_allowed` matches the WHOLE normalized text (`gate_registry.py:772-783`), and a Compare that wrapped the same tuple would have a different source text. A26 still runs F-b on the site, which calls `acceptable` at :981.
- Class-wide: my `GR.analyse` on the C3-b2 snapshot lists exactly 5 `test_identity` items: `same_test` (produce), the 2 `_run_freshness` returns, the 2 display flags. No other converted accept site counts a state return.
- C3-d: the only `s5_window` item is `window_record.build:1649` (produce). The four `validate_window` comparisons were never counted, because the old words were class words. 146 items / 50 triples, matching the pin.
- C3-b2: 149 items / 52 triples, matching the pin and the report.

**(4) Tests.**
- C3-d: one parameterised table, 24 rows plus the E3 rows. Expectations come from the corrected `decides`, the charter and FR-59. It reports every row (`check_eq` per row).
- C3-b2: rows in three existing files, each with its card source.
  - Killing power: reverting any site to bare truthiness or the old literal turns the E5 rows red; reverting `_match` to `same_instance_bytes` turns (ii) red.
  - Minor duplicate, which the card asked for: the "item 6: receipt for other code is not valid" row repeats the existing `comment_only_changes_keep_the_receipt` row (the builder names it). The defect is the spec's, not the builder's. `tests-over:` is named and holds.
- C3-reg: one table of 9 rows.
  - Killing power is shown by the negative control (block removed, red at `absent`).
  - Key 6: the loop stops at the first failing row. `docs/TESTING.md` asks for one parameterised table per behaviour; it does not demand that every row report (`grep -niE "таблиц|table|parametri"` over TESTING.md: no such clause). The file's `tr4_7` harness is assert-and-stop. Not a finding. Collecting per-row failures and asserting once would show the extent of a regression; optional.
  - Row `malformed-first`: fix 4.

**(5) Registry rows and pins.**
- Each diff edits only its own row: `test_identity` in C3-b2, `s5_window` in C3-d. Roles and `accepts` are as the cards state, F-T1 (a) words included. C3-reg does not touch the registry (`--check` debt block unchanged).
- Every pin move carries an AR-20 comment: debt -1, converted +1, K-T1.2, split, F4 `code` +`s5_window` (C3-d), D13 triples/count with cause (C3-b2's +4/+3 against the card's +2/+2, explained by the Lead's decision (A)), and the allow-list pin (C3-b2, named in the report).
- For the t-1083 merger: both cards move 6 -> 5 from the same base, so the merged pins are EXPECTED_DEBT without both, "4 gate(s) left as debt:", split 23/4/6, the D13 union of triples, and a count predicted at 150 / 53 triples. That prediction is not measured; the merger measures it with `GR.analyse`, as S-f says.

**(6) Siblings.**
- Axis 5 prose twins, C3-b2: my grep `instance_code|file_code|same_test|compare_identity` (-i -E) over `execution-lifecycle.md` + the qa-automator / qa-code-critic slices, `manual-evidence.md`, `environment-preparation.md`, `s5.md`, `s6.md` finds 1 hit, `s5.md:193` (`instance_code_sha`, the sha name). The positive controls `probe|person_confirmed` hit 7-37 per file. This matches the report.
- Axis 5, C3-d: `s5.md:162`, `code-review-rubric.md:92` (and :93 per the report) still hold. "Only for a window where the test could not run" covers handed and stopped alike.
- Axes 7 and 25: fix 1.
- Axis 32: census unchanged, rightly.
- Axis 34: C3-d leaves S9's road untouched. C3-reg is keyed on no stage, language or project (E5).
- The stale debt-file line `factory-rules-debt.md:106` goes to S1b by S-d (reported).
- Axis-5 line for C3-reg (card item 5) is the Lead's at acceptance.

**(7) Judgment census.** No diff touches `judgment-census.json` (`--stat` of all three).
- C3-b2: no refusal unit is added; the whys are texts of existing returns.
- C3-d: `validate_window`'s unit is still the `ValueError`, and the gaps are list transport.
- C3-reg: the raise sits inside the existing `controller.py::validate` unit (shape/data).
- AR-29 is kept by all three: membership joins of data; the critic's verdict stays the critic's judgment.

## C3-reg keys (the coordinator's addition)

- **(1) E4 positions.** The block sits after `validate_record`, the running-dispatch refusal and `required`, and before the closure test (`controller.py:5537-5554`).
  - (i) holds through the real door, because `validate_record` raises `ValueError` first. The test row is the problem (fix 4), not the code.
  - (ii) The running-dispatch text is untouched.
  - (iii) `apply` commits through `store.commit(..., lambda: self.validate(...))` (:5209). The other `store.commit` calls (`controller.py:8090, 8115, 8278, 8708, 8716`; `manifest_put`; `stage_done`) commit no dispatch event. The test checks that nothing is recorded (`len(c.store.read()) == before`).
  - (iv) and (v) hold.
- **(2) D2:** fix 4.
- **(3) D1:** fix 6. The generic row is acceptable for this round and owes a node.
- **(4) D3:** a standing class (fix 5), not this card's defect. The card prescribed the form.
- **(5) E3 (i).** `_READ` caches a failure per process (`gate_template.py:31-37`). In a long-lived driver it only ever stops: the refusal repeats until the process restarts, and no branch turns the cached failure into a pass. One note: the door says "then start the stage again". For an in-process driver this works only after the driver restarts. UPGRADE.md:71 covers that ("stop active factory work"), so it is not a finding. A wording such as "restart the run" would be clearer.
- **(6)** See key (4) above: not a finding.

## Duplication and consistency
Fix 2: the registry-why family has four forms. No second predicate or registry reader: every site goes through `gate_template.acceptable` / `registry_problem`. I grepped `registry cannot be read|registry_problem()` over `scripts/*.py`: 3 code sites plus the controller block; the rest are docstrings. `HANDED_REVIEW_VERDICTS` is removed with no copy left. The C3-d waiting finding (c) lists the review-word copies outside the registry (fix 3).

## Code quality
- No new function over 60 lines and no new nesting over three levels.
- `_evaluate`'s `said = A if problem else B if cond else C` parses as intended (`A if p else (B if c else C)`). It is dense; acceptable.
- `_match` calls `registry_problem()` only on refusal.
- No dead branches, except the pre-existing dead `required` check in the dispatch branch (fix 4 analog).
- Names tell the truth.

## One road
None found. All four `test_identity` consumers and all three `s5_window` consumers go through the one predicate. The C3-reg stop is keyed on no stage, language or project. I grepped `acceptable(` and `registry_problem(` in the touched files, and `stage|language` in the C3-reg block.

## Tests verdict line
- C3-b2 and C3-d: fit. `tests-over:` lines are present and hold.
- C3-reg: fit with fix 4.

## Trail
- Read: spec §C3 shared items (S-a..S-f, :270-409); C3-0 (:533-677); C3-b2 (:918-1025); C3-d (:1029-1162); C3-reg-precondition (:1164-1254); the Lead decision sections (:2294-2347); `docs/tasks/critic-diff-brief.md`.
- Read: the three reports; `git show` of `18f585f5`, `1637ce7c`, `c50ca830`.
- Read in the snapshots: `proof_level.py:235-255, 853-990, 1505-1575, 1600-1680, 1735-1760`; `acceptance.py:160-215, 1120-1240`; `gate_registry.py:15-60, 340-380, 765-880`; `gate_template.py:28-60`; `controller.py:2400-2490, 5515-5560, 5955-5968`; `record_schema.py:12-61`; `record-schemas.json:174-215`; `controller-blocks.md` `blocking[0]` rows; `tools/controller-blocks-gen.py:315, 351`; `docs/SIBLING_MAP.md` axes 5, 7, 25.
- Reruns are listed in the json block. Snapshots are `git archive` of each commit into the scratchpad. No suites were re-run.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "class_completeness": "C3-b2/C3-d: every site the cards name is converted, and behaviour on a readable registry is preserved (traced). Axis 7 names acceptance._bound_to, a test_identity accept site (same_test truthiness for the reviews and probes of validate_window). It is not converted, not in the E-c table and not queued (fix 1). The axis-25 twins green_on_current_bytes_why and run_history are queued per the map text; their batch row is not verified. Axis 5 prose twins were re-grepped with a positive control: no stale twin. C3-reg: the dispatch-branch person passes go unrecorded as a standing class over five sites (fix 5).",
  "fixes": [
    "1 (queue, Lead): acceptance.py:204-211 _bound_to accepts by same_test truthiness (reviews :1165/:1171/:1175, probe :1228); register it as a test_identity accept site and route it through gate_template.acceptable; confirm the axis-25 queue row for green_on_current_bytes_why:177 and run_history.py:221,256",
    "2 (queue, low): one builder for the 'gate registry cannot be read (<reason>): a factory defect, ...' family (proof_level.py:947-948, execution_request.py:2108, controller.py:5549)",
    "3 (Lead): file the R12 waiting findings (a) probe_verdict words inside converted accept sites, (c) the critic review word read outside the registry (check_delivery.py:860, case_stamp/report_facts APPROVING, window_record.py:1641,1742, GAP_ORIGIN review), (d) holds_over_comments delete-or-wire",
    "4 (C3-reg, this round, non-blocking): test_controller_state.py:2283/:2322/:2332 row malformed-first stubs validate_record and asserts a dead-branch message; replace with the real door: registry broken, input_hash dropped (and empty) -> type ValueError, text not starting 'gate registry unreadable' (E4 (i), FR-46)",
    "5 (queue, Lead): dispatch-branch _passed_by_person passes are discarded (controller.py:5548,5649,5683,5698,5717) while the accept branch records them via _record_person_pass (FR-4/P13 carrier passed-by-person.jsonl); a node for the five sites",
    "6 (queue, low): controller-blocks.md row for the new block is the generic blocking[0] row; add a tools/controller-blocks-gen.py entry with card item 2's doors and give controller.py:5548 a unique local name (precedent: controller-blocks-gen.py:351)"
  ],
  "trail": {
    "read": [
      "docs/tasks/specs/20261117-rules-debt-phase2-cards-spec.md (:270-409, :533-677, :918-1254, :2294-2347)",
      "docs/tasks/critic-diff-brief.md",
      "docs/tasks/specs/reports/20261117-rules-debt-c3-b2-report.md (at 18f585f5)",
      "docs/tasks/specs/reports/20261117-rules-debt-c3-d-report.md (at 1637ce7c)",
      "docs/tasks/specs/reports/20261117-rules-debt-c3-reg-precondition-report.md (at c50ca830)",
      "git show 18f585f5, 1637ce7c, c50ca830",
      "scripts/proof_level.py, acceptance.py, gate_registry.py, gate_template.py, controller.py, record_schema.py (ranges in Trail)",
      "references/record-schemas.json:174-215, design/controller-blocks.md, tools/controller-blocks-gen.py:315,351",
      "docs/SIBLING_MAP.md axes 5, 7, 25",
      "docs/TESTING.md (table clauses grep)"
    ],
    "reruns": [
      {"command": "python -B <snapshot 18f585f5>/scripts/gate_registry.py --check", "result": "A26 gate registry: no violations; 5 debt (test_identity absent); exit=0"},
      {"command": "python -B <snapshot 1637ce7c>/scripts/gate_registry.py --check", "result": "A26 gate registry: no violations; 5 debt (s5_window absent); exit=0"},
      {"command": "GR.analyse on both snapshots, test_identity/s5_window items listed", "result": "C3-b2: 0 findings, 149 items, 52 triples; 5 test_identity items all allowed (same_test 919, _run_freshness 973/980, already_probed 1568, _evaluate 1663). C3-d: 0 findings, 146 items, 50 triples; s5_window item window_record.build:1649 allowed"},
      {"command": "( cd <snapshot 18f585f5>/scripts/tests && python -B test_run_freshness.py )", "result": "K1 (p) four PASS lines; === run freshness: 100/100 ok ==="},
      {"command": "python -B <snapshot c50ca830>/scripts/gate_registry.py --check", "result": "A26 gate registry: no violations; exit=0"},
      {"command": "( cd <snapshot c50ca830> && python -B scripts/tests/test_controller_blocks.py )", "result": "=== test_controller_blocks: 376/376 ok ==="},
      {"command": "grep -rniE HANDED_REVIEW_VERDICTS <snapshot 1637ce7c> (control BLOCKED_REVIEW_VERDICT)", "result": "0 hits; control 4 hits"},
      {"command": "axis-5 prose twin grep instance_code|file_code|same_test|compare_identity (control probe|person_confirmed)", "result": "1 hit s5.md:193; controls 7-37 per file"}
    ]
  }
}
```
