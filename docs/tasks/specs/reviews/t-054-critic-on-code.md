# t-054 — critic on CODE: node PC2-4 (t-041, batch package-ci/2)

Under review: the uncommitted diff of `ai-packages/qa-factory/scripts/probe_by_code.py` (`_walk_plan`, `_repeat_same_entries`) and
`ai-packages/qa-factory/scripts/tests/test_probe_by_code.py` (`INVERT_RECORD_KEYS`, `the_record_and_the_answer_are_pinned`,
`the_repeat_is_answered`), plus `ai-packages/qa-factory/changelog.d/package-ci-2-probe-receipt-and-repeat.md`. Spec: `docs/tasks/specs/t-041-pc2-4-probe-receipt-and-repeat.md`
with «Answers to the forks» and «Fixes after the plan critic». Reviewer: critic (Opus), 12.11.2026. PBC = `scripts/probe_by_code.py`, PL =
`scripts/proof_level.py`, T = `scripts/tests/test_probe_by_code.py`, FR = `scripts/tests/test_probe_fix_round.py`, EC = `scripts/tests/test_probe_every_check.py`
(all under `ai-packages/qa-factory/`).

## Verdict

**ACCEPT WITH FIXES.** The code is right: one blocking finding, and it is a missing test, not a code defect. B1: the E5 row (a walked row plus a
`product` row, repeated -> `already_probed`) has no pin. My probe run shows a cheap pin exists in the existing scaffolding of FR/EC, so the builder's
"cannot carry a product entry" holds only for T's own fixtures. Four non-blocking fixes for this round (N1-N4). Accepting the work, and widening
`owns` for B1, are decisions for the Lead (rule 6).

## Control runs (verbatim)

1. `python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_probe_by_code.py`, run once, output filtered by
   `grep -E "^(FAIL|===)"`:

```
exit=0
=== test_probe_by_code: 762/762 ok ===
```

   No FAIL line. This matches the builder's witness (762/762) and the plan review's entry state (756/762, whose six FAIL lines are now ok).

2. Probe of the E5 case through the EXISTING helpers (`flip`, `flip_call`, `flip_models`, `flip_actual`, `real_receipt` from EC; `with_row`
   from FR). It ran in a temp folder through a stdin script, not committed, and no repo file was touched. The first attempt also gave the row
   `case_version_links` (my fixture mistake): then `_repeat_look` does not hit at all (`look: None`) for the product and the plain world alike,
   so that attempt says nothing about the code. The second run, without that key:

```
links=True product=True: first=intended_failure receipt=True again=intended_failure log={'look': None, 'notes': []}
links=False product=True: first=intended_failure receipt=True again=already_probed log={'look': 'receipt', 'notes': [], 'same': True}
links=False product=False: first=intended_failure receipt=True again=already_probed log={'look': 'receipt', 'notes': [], 'same': True}
links=True product=False: first=intended_failure receipt=True again=intended_failure log={'look': None, 'notes': []}
```

3. The branches of the kind lookup (same world: `keys[0]` = `product`, `keys[1]` = `actual`; spies on `_per_check_read` and `_repeat_same_entries`):

```
A plain repeat: keys=['tests/test_t.py:3', 'tests/test_t.py:4'] -> already_probed; new runs 0; log={'read': [('tests/test_t.py:4', 'intended_failure')], 'same': True}
B product entry removed from models, aggregate readable: keys=['tests/test_t.py:3', 'tests/test_t.py:4'] -> already_probed; new runs 0; log={'read': [('tests/test_t.py:4', 'intended_failure')], 'same': True}
C product entry removed, aggregate unreadable: keys=['tests/test_t.py:3', 'tests/test_t.py:4'] -> REFUSAL: probe_by_code: the model file work/probe-models/D.json: no model is stored for these check; new runs 0; log={'read': [('tests/test_t.py:3', None)], 'same': False}
D models file removed entirely: keys=['tests/test_t.py:3', 'tests/test_t.py:4'] -> already_probed; new runs 0; log={'read': [('tests/test_t.py:4', 'intended_failure')], 'same': True}
```

   The first probe of the same world printed `per-check files: ['i1--L4-097867e4.json']`: a glob of the checks folder listed one per-check
   record, the line-4 walked row's, and none for the product row on line 3. That is the plan critic's B1 premise, measured (the line-4 file is
   the positive control of the same glob). After a repeat, corrupting that walked record gave `corrupt walked record: intended_failure new
   runs 1`. The call walks and reruns only the walked row (FR-59 direction).

What the runs show. (A) The product row is NEVER read: `_per_check_read` is called for `:4` only, so the B1 fix works end to end. (C) The read of
the product key returns None, so without the `kind == "product"` skip the answer would be False: a pin over (A) kills a revert of the B1 fix.
(B, D) The fallback to the stored aggregate works when the model entry or the whole models file is gone.

## Answers

### Q1 — Fit to the amended spec. Verdict: FITS, except the unpinned E5 row (B1).

- **One receipt-capable publish per walk.** PBC :6529-6536: `write(...)`, then `if result["ended"]: break`, then `if index < len(groups) - 1:
  publish()`. The end publish (:6553) and the no-group publish (:6457) are unchanged. This is §3 to the letter. An intermediate publish cannot
  attach a receipt: the rows of the groups not yet run are `not_reached` (:6704), so `_aggregate_verdict` is `incomplete` (rule 1, :6714-6716).
- **Kill between groups: still recoverable.** Every group but the last still publishes after its `write` (:6532-6536). A kill after group k leaves
  the per-check records of groups 1..k and an incomplete aggregate with no receipt. Next call: `already_probed` item 1 finds no new receipt and
  item 2 needs `no_failure`/`wrong_location` (PL :1491), so there is no hit and the call walks. `_check_standing` skips the proved rows
  (:6443-6447) and carries the survivors (:6450-6452). Same as before the diff. The only window that changed is the last group (between `write`
  and :6553) and an ended walk (`break` -> :6553). Both self-heal as the plan critic traced (a later call publishes at :6457).
- **F2 with the B1 fix.** PBC :7312-7325. A `not_owed` row is skipped (:7312-7313). The kind comes from `picked` (:7314), else from the stored
  aggregate row's `entry.kind` (:7315-7320; aggregate rows carry `entry` whole, PBC :6639), else None. Kind `product` skips the read (:7321-7322).
  Any other kind, None included, reads the per-check record and needs `verdict == intended_failure` and the same `entry_sha` (:7323-7325).
  This matches B1 items (1)-(4).
- **N1.** The read is `_per_check_read(ctx, check)` (:7323), the wrapper over the one reader `_read_check_record` (:6618-6621). No `json.loads`
  of `work/probes/checks/` was added.
- **F1 repin.** T :2336-2341: `(0, "already_probed")` and `sorted(ANSWER_KEYS + ["notes"])`. The comment states what the checks add (N4 of the
  plan review). Correct.
- **F3 fixture.** T :2524-2527 stamps `verdict: incomplete` on every `test_dead_assert--*.json` per-check record. The expectation `("no_failure", 2)`
  is unchanged.
- **The two keys.** T :2308 `judgment_owed` and T :2315 `walk_ended` sit in their sorted positions, each with a reader comment.

### Q2 — Correctness of `_repeat_same_entries`. Verdict: NO wrong True is possible, and no loop.

- **The unsafe direction is closed by construction.** Old loop body: two `return False` checks, then the end of the iteration. New body: the same
  two checks, then only `continue` (= end of the iteration, as before) or `return False` (:7312-7325). So the diff can only turn a True into a
  False; the set of True answers is a SUBSET of the old one. No input can make it answer a repeat the old code would not have answered. Measured:
  in run 3 a corrupt walked record walks (`new runs 1`); T's corrupt group (`("intended_failure", 2)`) pins the same.
- **Product-only plan:** every row has a picked kind `product`, so it is skipped and the answer is True. Answered, no loop (traced; run A covers
  the product branch with one walked row beside it).
- **Mixed plan:** run A gives `already_probed`, 0 new runs.
- **A `not_owed` row:** skipped before the kind lookup (:7312-7313). Its per-check record does not exist (the walk drops `not_here`, :6380-6381).
- **A row whose entry was removed from the models file:** the kind comes from the aggregate. Runs B and D: answered.
- **Aggregate absent or unreadable at the kind lookup:** `stored_rows` is `[]` (:7318), so the kind is None and the record is read as a walked row.
  For a walked row that is right. For a product row whose entry is ALSO gone from the models file (run C), the read is None, the answer is False,
  and the walk refuses with the model refusal ("no model is stored", the existing door; nothing written, 0 runs). Before the diff that case was
  answered `already_probed`. This is the direction B1 (4) chose ("unknown -> walk"), and it is a refusal with a door, not a loop. The spec's
  "this cannot loop, a walk writes the per-check record" is slightly off for this case: the outcome is a refusal, not a walk. That is correct
  behaviour, so there is no finding. If the aggregate path is `""` (a receipt with no `probe_record`), `_repeat_record` reads the task folder
  itself, gets OSError -> None, and lands on the same safe side.
- **AR-13, second reader?** No new reader. The aggregate is read through the existing `_repeat_record` (PBC :7264-7272), the module's reader
  of "the record an answer stands on", already used by `_repeat_is_new` for the same `answer["record"]` path. The per-check read goes through
  the declared one reader. Code quality: the call relabels the answer (`{**answer, "by": "probe_record"}`, :7317) to steer `_repeat_record`'s
  path choice. That couples to the internals of a function outside `owns`; see N3.
- **Loop for walked rows:** a False sends the call to the walk. The walk reruns or carries every row whose standing record is not
  `intended_failure` on these bytes, and rewrites its per-check record (:6486-6494). The next repeat reads an agreeing record.

### Q3 — The unpinned E5 case. Verdict: (b), a cheap pin exists in an existing test file. As the fix of this round it is B1, blocking.

- **The builder's reason is true for T and false as a general claim.** T's `run()` (T :345-346) calls `model_entries`, which rewrites the window's
  model file with `invert` entries for every plan key (T :332-342, `PE.write_invert_entries`). So T's fixtures overwrite a product entry on every
  call, and a holding product receipt has no producer in T. But FR and EC already carry everything: `real_receipt` (EC :2468-2485, the real
  producer of a `one_check` product receipt), `flip_models` with a `product` entry (EC :2503), and `with_row` plus the receipt on the row
  (FR :141-146, :184). Run 2 proves the case end to end in about 12 lines. Run 3 (C) proves the pin kills a revert of the product skip.
- **Exact shape (to be added in FR; the Lead widens `owns` to FR, function `test_b3_repeat_of_a_complete_walk_is_already_probed`; no new
  function).** The behaviour is the same B3 one ("a whole standing record answers the repeat"), now for every entry kind. Append to that test:

```python
    # E5 of t-041 (B1 of its plan critic): a walked row plus a `product` row, both proved, repeated on the same bytes and entries: answered by
    # the receipt, no run. The product row has no per-check record by construction; reading one for it would walk every repeat forever.
    # Killed by: dropping the `kind == "product"` skip in `_repeat_same_entries`.
    product_world = flip(tmp_path / "with-product", monkeypatch, "ss", stage="S5")
    good, _receipt = real_receipt(product_world, monkeypatch, product_world.keys[0])
    product_row = with_row(product_world, monkeypatch)        # after real_receipt: its manifest_entry patch is replaced by this row
    monkeypatch.setattr(PBC.proof_level, "binding_facts", lambda task_root, iid: {
        "case_version": "cv_1", "test_content_hash": PBC.sha256(product_world.original), "source_revision": "rev1", "build_id": "b1"})
    flip_models(product_world, [{"check": product_world.keys[0], "instance": "i1", "product": good}] + flip_actual(product_world, product_world.keys[1:]))
    proved = flip_call(product_world)
    assert [(r["probe_kind"], r["verdict"]) for r in proved["checks"]] == [("product", "intended_failure"), ("actual", "intended_failure")] and proved["receipt"], proved["checks"]
    product_row["sensitivity_proof"] = {"receipt_ref": proved["receipt"]}
    runs = len(product_world.runs)
    repeat = flip_call(product_world)
    assert repeat["verdict"] == "already_probed" and repeat["by"] == "receipt" and len(product_world.runs) == runs, (repeat.get("verdict"), repeat.get("notes"))
```

  The import line FR :17 gains `real_receipt`. Do NOT give the row `case_version_links` (run 2: with it, the receipt is not reached and the case
  says nothing). `tmp_path / "with-product"` keeps it apart from the first world of the same test. Estimated cost: about 15 lines, one fast test
  file. Its witness is `python -B .../tests/test_probe_fix_round.py` (one file of the existing scope N3). Why not (a): the product skip IS the
  plan critic's blocker fix, and the plan critic showed that no existing pin catches its regression (an endless walk with "already holds this
  proof" on every repeat, the very symptom PC2-4 removes). A live-proof line would leave a deterministic, cheap, data-only branch to a stand run
  that may never build a product receipt (FR-32: a fix with a test).

### Q4 — Tests. Verdict: they test requirements. Nothing weakened or deleted.

- **F1 repin (T :2339-2341):** the expected `already_probed` comes from B3 (spec t-2064 :541, PBC :7437 comment), and the key set is
  `_repeat_answer`'s (PBC :7332-7335), the old road's answer shape the spec names. The exact key-set equality adds something over the «twice»
  subset check (T :2389-2390). A wrong key added to or dropped from the answer goes red. The expectation is a requirement, not a read of the code.
- **INVERT_RECORD_KEYS:** an exact-set check (T :2329) is now green with two named readers. It is stricter, not looser: any further key goes red.
- **F3 fixture (T :2521-2530):** it still exercises «an incomplete record does not answer a repeat». (i) The aggregate stamp still keeps
  `already_probed` item 2 from hitting (PL :1491). (ii) The per-check stamp makes `_check_standing` return `incomplete`, which is not in
  `_CARRIED_VERDICTS` (PBC :6030), so the check reruns: 2 launches. It goes red if `incomplete` is ever carried, or if item 2 ever answers on
  `incomplete`. That is the requirement (spec t-2064 :824, B-373 R10).
- **Corrupt group (T :2509-2516):** the expectation is unchanged and is now met through F2 (receipt standing, per-check record `{not json` ->
  False -> walk -> rerun).
- **Deleted or weakened:** none (`git diff --stat` of T: 30 lines changed, all in the three owned spots; no check removed, no expectation loosened).

### Q5 — Architecture and rules.

- **AR-13 kept:** the per-check read goes through `_per_check_read` -> `_read_check_record` (PBC :6618-6621, :6033-6041), and the aggregate
  through the existing `_repeat_record`. Grep `_per_check_read\(|_read_check_record\(` (diff): only :7323 is new.
- **AR-14 kept:** no new writer. `_repeat_same_entries` writes nothing; `_aggregate_record` stays the only aggregate writer (callers :6409,
  :7474, :7820) and `write_receipt` the only receipt writer. Per walk there is now one receipt-capable call.
- **AR-22 kept (caveat 4 re-run by me):** a case-insensitive Grep `judgment_owed|walk_ended` over `scripts/{probe_by_code,proof_level}.py` finds
  the producers PBC :6756 and :6894 (positive control: the producers found by the same search) and the readers PL :1123-1126 / :1170-1174 and
  PBC :7816 (`_refold`).
- **AR-28 kept:** every new branch errs toward walking (Q2). The answer set only shrinks.
- **AR-29 kept:** presence, readability and equality of two stored keys (`verdict`, `entry_sha`) plus a stored `kind`. Data, no judgment. The
  builder reports census and gate-registry green with no row change.
- **FR walk:** A (refusals): no refusal text changed; run C reaches the existing model refusal with its door (FR-1, FR-2 kept). B (text to a
  person): the note «already holds this proof» no longer appears inside one walk (§3 invariant), and no other text changed. C (contracts): the
  answer shape is unchanged (FR-14); the record's key set is unchanged in content (the two keys were already written, now pinned). D: FR-59 is
  kept (an unknown kind or record -> walk); FR-58: tests take their expectations from B3, F3 and B-373, not from code. E, F: not touched.
  G: FR-30, the changelog fragment is English (builder: `selftest.py --lang` 2/2); FR-32 needs a test for the B1 branch, hence B1 below.
- **DUPLICATION AND CONSISTENCY:** none in the code. The new read reuses `_per_check_read` and `_repeat_record`, and does not copy
  `_check_standing` (it deliberately asks a weaker question, receipt-bound bytes; the docstring says FR-59 and the error direction). Grepped:
  `_per_check_read\(|_read_check_record\(|_repeat_record\(` over `scripts/*.py`. The F1 pins duplicate the «twice» pins only in the verdict
  line; the key-set line is new (accepted in the plan as N4).
- **CODE QUALITY:** (i) the relabel of `answer` at :7317 (N3); (ii) a stale docstring of `_walk_plan` at :6351 (N1); (iii) stale test comments
  (N2). Nothing else.
- **ONE ACTION, ONE ROAD (P31):** the repeat question stays on one road (`_repeat_look` -> `_repeat_is_new` / `_repeat_same_entries`). The
  product exclusion from the per-check read is not an exclusion of a case from a shared mechanism: a product row is proved by another mechanism
  (EP-W) and has no per-check record by design. The shared answer is still reached for it (run A).
- **Caveat 5, the stale comments:** fix now (N2). They sit in the owned function `the_repeat_is_answered`, cost only comment lines, and now
  state the opposite of what the code does.

### Q6 — Class-wide completeness.

- **SIBLING_MAP:** no axis for the repeat answer or the receipt writers. A case-insensitive Grep `already_probed|receipt|repeat|per-check` over
  `docs/SIBLING_MAP.md` finds only Axis 20 (host receipt names) and unrelated rows (lines 113-614). The positive control is Axis 20 itself,
  found by the same search. So the map gives nothing to walk; the artifact sweep follows.
- **Other answerers of a repeat** (Grep `_repeat_same_entries|_repeat_record|_repeat_is_new|already_probed\(` over `scripts/*.py`):
  - PBC :7438-7440, the EP-I branch: old single records that have no per-check records by design. Not applicable.
  - PBC :4496, `_repeat_check`: off the road, called only by `test_probe_one_road.py` (plan critic). Not applicable.
  - `red_sandbox.py:1605`: the product road. It answers by the product receipt and product record, has no walk per-check records, and so is not
    applicable.
  - `_repeat_same_entries`: the only answerer over a walk record. Covered.
- **Other publish call sites** (`_aggregate_record` callers):
  - :6409 `publish`: the in-loop calls are now intermediate only, with one receipt-capable call at :6457 or :6553.
  - :7474, the no-live-key path: one call.
  - :7820 `_refold`: one call per judge.
  - :7870, the single-record `attach_receipt` of `judge_record`: one call.
  No other double call.
- **Inside the artifact (`_repeat_same_entries`, its loop branches):**
  - row shape and key: unchanged.
  - entry_sha: unchanged.
  - not_owed: applied (skip).
  - product: applied (skip).
  - actual/find/invert/unknown: applied (read).
  No neighbour left. The stale-comment class is swept across the whole owned test function (N2, three sites).

## Blocking findings

1. **B1 — the E5 row is unpinned; a cheap pin exists** (surface: the repeat answer, `_repeat_same_entries` product skip, PBC :7321-7322).
   Failure if it stays: dropping or breaking the skip makes every repeat of a plan with a `product` row walk, with the receipt note «already
   holds this proof» on every call (the plan critic's B1 trace). Every pin of T, FR, `test_probe_one_road.py`, `test_probe_word_repeat.py` and
   `test_probe_by_code_languages.py` stays green, because none of them builds a product row on the walk road. The plan critic's grep is the
   carrier, and the builder's own caveat 2 confirms it. Neighbouring classes of the surface were walked by run 3: entry removed (B), aggregate
   unreadable (C), models file gone (D); all behave as the spec says. Exact change: the block in Q3, appended to
   `test_b3_repeat_of_a_complete_walk_is_already_probed` in FR, with `real_receipt` added to the import at FR :17. The Lead widens `owns` to that
   one function and import line. Witness: `python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_probe_fix_round.py` (38
   passed, the count stays: the block goes into an existing test), plus a negative control in the report: the run with the `kind == "product"`
   line commented out goes red, rolled back by byte copy (CLAUDE.md hygiene 7).

## Non-blocking findings (fixes of this round, each with its exact change)

- **N1 — `_walk_plan` docstring stale (PBC :6351).** "After EVERY row and at the end `_aggregate_record` writes ..." becomes "After every row
  but the last, and once at the end (the walk's one receipt-capable call), `_aggregate_record` writes ...". The function is in `owns`.
- **N2 — stale comments in `the_repeat_is_answered` (caveat 5).**
  - T :2370-2374 says the B3 answer pins "stay red (PRODUCT QUESTION 1 ...), unbent". They are green since fix round A B3. Replace the
    sentences from "The spec's ANSWER of the repeat" to "unbent." with "The ANSWER of the repeat is `already_probed` by the receipt (t-2064 fix
    round A, B3; the spec's keys, `by`, block and words, one printed line)."
  - T :2506-2508: "the walk reads no note about it: an unreadable record is simply not a proof (`_check_proved`, AR-28)" becomes "an unreadable
    per-check record answers no repeat (`_repeat_same_entries`, t-041 F2) and is not a proof on the walk (`_check_standing`, AR-28): the check
    runs again, and the aggregate is rewritten readable".
  - The same stale claim stands at T :2532-2537 ("Their ANSWER pins stay red and unbent: PRODUCT QUESTION 1"). Since it is in the same owned
    function, drop the words "PRODUCT QUESTION 1 (the person's-word door and the answer), and" or replace them with "the answer is B3's
    `already_probed`;".
  Comment lines only. They are the same class (sweep-the-artifact-first), so all three are fixed together.
- **N3 — the relabel `{**answer, "by": "probe_record"}` (PBC :7317).** It works: `_repeat_record` reads `answer["record"]` for any `by` other
  than `receipt`, and for a receipt answer that is the receipt's `probe_record`, the aggregate (PL :1476). But it borrows a branch of a function
  outside `owns`, and its intent is not visible. Minimal fix inside `owns`: a trailing comment saying that `_repeat_record` reads
  `answer["record"]` for any `by` but "receipt", and that for a receipt answer this is the aggregate the receipt names (proof_level.already_probed
  item 1). A cleaner fix (a keyword `which="record"` on `_repeat_record`) needs `owns` widened; Lead's call, and not required.
- **N4 — optional hardening: bind the aggregate's kind to the receipt row (PBC :7319-7320).** Today the aggregate's `entry.kind` is taken for
  the key whatever entry it holds. An aggregate rewritten after the receipt (for instance an `--at` call that did not complete the plan) could
  hold another entry for the key. Not a regression: the diff never widens a True (Q2), and the old code answered such a case anyway. The cheap
  hardening keeps "any doubt is False": take the kind only when
  `_entry_sha(dict(one["entry"], check=check["key"])) == row.get("entry_sha")`, else None (read as walked). If the Lead declines it, no node is
  needed (no case is widened); say so in the acceptance note.

## What I did not check

- `test_probe_fix_round.py`, `test_probe_one_road.py`, `test_probe_word_repeat.py`, `test_probe_by_code_languages.py`, `test_judgment_census.py`,
  `gate_registry.py --check`, `selftest.py --lang`: not re-run. I rely on the builder's attached outputs (consistent with the diff: no gate or
  census row could change, since the diff adds no check unit and no refusal).
- The builder's «before» runs of the four neighbour files: by its own caveat 1 they are not a clean baseline. I did not reconstruct one.
  K2 for them rests on the final-state runs alone.
- The slow and scenario files that `scenario_walk.py --witness-for` prints (left to the batch canon, spec N3).
- Whether a product receipt still holds for a key on a repeat (`_product_entry_holds` is not re-asked on the answered road): pre-existing B3
  behaviour, outside this diff.
- Commit lines (`architecture:` / `judgment:`): the builder does not commit (N2 of the spec). The Lead checks them at commit.
- The B1 pin shape was run as a stdin probe with the same helpers and values, not as the literal block inside FR. The builder's FR run is its
  witness.

## Trail

Read: the spec t-041 (whole) and its plan review t-041-critic-on-plan.md (whole); `git diff` of PBC and T; the changelog fragment and
`changelog.d/README.md` head; PBC :5995-6089, :6320-6569, :6614-6723, :7240-7479, :7790-7873; PL :1404-1532; T :300-389, :2286-2560; FR :1-215;
EC :1699-1756, :2455-2546; `docs/SIBLING_MAP.md` (grep).
Greps (case-insensitive where content-negative, each with its positive control named above): `judgment_owed|walk_ended`; `_check_record\(`;
`ONE reader|the one reader of`; `_repeat_same_entries|_repeat_record|_repeat_is_new|already_probed\(`; `already_probed` in FR/EC/word_repeat/walk;
`"kind": "product"|kind="product"`; `EP-W|def test_.*product` in `test_probe_*.py`; SIBLING_MAP `already_probed|receipt|repeat|per-check`.
Runs: the control run of T (above); three probe runs of the E5 world through the existing helpers (temp folder, stdin, no repo file touched;
output verbatim above).

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "B1: the E5 row of t-041 (a walked row plus a product row, both proved, repeated -> already_probed) is unpinned, and the product skip in _repeat_same_entries (PBC :7321-7322) is the plan critic's B1 fix with no detector: reverting it keeps every existing pin green. A cheap pin exists with the existing helpers (EC real_receipt, flip_models, flip_call; FR with_row): verified by a probe run (already_probed, 0 new runs; the per-check read of the product key returns None, so the pin kills a revert). Fix: append the Q3 block to FR test_b3_repeat_of_a_complete_walk_is_already_probed and add real_receipt to the FR :17 import; the Lead widens owns to that function."
  ],
  "fixes": [
    "B1 as above.",
    "N1: _walk_plan docstring PBC :6351 'After EVERY row and at the end' -> 'After every row but the last, and once at the end (the walk's one receipt-capable call)'.",
    "N2: stale comments in the_repeat_is_answered: T :2370-2374 (B3 answer pins said to stay red), T :2506-2508 (the repeat answer now reads the per-check record, F2), T :2532-2537 (same stale PRODUCT QUESTION 1 claim); comment-only rewrite per the report.",
    "N3: comment the relabel of answer to by=probe_record at PBC :7317 (it steers _repeat_record to answer['record'], the aggregate the receipt names); or a keyword on _repeat_record if the Lead widens owns.",
    "N4 (optional, Lead's call): take the aggregate's entry kind only when _entry_sha of that entry equals the receipt row's entry_sha, else unknown -> read as walked; declining needs no node since the diff never widens a True."
  ],
  "class_completeness": "SIBLING_MAP has no repeat/receipt axis (grep -i already_probed|receipt|repeat|per-check: only Axis 20 host receipt names and unrelated rows). Artifact sweep: repeat answerers -- EP-I branch n/a, _repeat_check off the road, red_sandbox.py:1605 product road n/a, _repeat_same_entries covered; publish sites -- :6409 now one receipt-capable call per walk (:6457 or :6553), :7474, :7820, :7870 one each; branches of the _repeat_same_entries loop -- not_owed skip, product skip, actual/find/invert/unknown read, all applied. Stale-comment class swept across the whole owned test function (three sites, N2).",
  "trail": {
    "read": [
      "docs/tasks/specs/t-041-pc2-4-probe-receipt-and-repeat.md (whole)",
      "docs/tasks/specs/reviews/t-041-critic-on-plan.md (whole)",
      "git diff of scripts/probe_by_code.py and scripts/tests/test_probe_by_code.py; changelog.d/package-ci-2-probe-receipt-and-repeat.md",
      "ai-packages/qa-factory/scripts/probe_by_code.py :5995-6089, :6320-6569, :6614-6723, :7240-7479, :7790-7873",
      "ai-packages/qa-factory/scripts/proof_level.py :1404-1532",
      "ai-packages/qa-factory/scripts/tests/test_probe_by_code.py :300-389, :2286-2560",
      "ai-packages/qa-factory/scripts/tests/test_probe_fix_round.py :1-215",
      "ai-packages/qa-factory/scripts/tests/test_probe_every_check.py :1699-1756, :2455-2546",
      "docs/SIBLING_MAP.md (grep)"
    ],
    "reruns": [
      {
        "command": "python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_probe_by_code.py",
        "result": "exit=0; === test_probe_by_code: 762/762 ok === ; no FAIL line"
      },
      {
        "command": "stdin probe script (temp folder, no repo write): EC flip/real_receipt/flip_models/flip_call + FR with_row, a product row plus an actual row, called twice",
        "result": "links=False product=True: first=intended_failure receipt=True again=already_probed, look=receipt, same=True; branches: A plain -> already_probed (per-check read only :4); B entry removed -> already_probed; C entry removed + aggregate unreadable -> model refusal, 0 runs (read of :3 = None); D models file removed -> already_probed; corrupt walked record -> walk, 1 new run"
      }
    ]
  }
}
```
