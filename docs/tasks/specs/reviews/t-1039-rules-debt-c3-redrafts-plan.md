# t-1039 — critic: re-review of the t-1033 redrafts C3-b2, C3-d, C3-rr (plan, R13-g follow-up of t-1026)

Reviewer: critic (Opus). Read on the root checkout, `main` = `origin/main` = `e9d6195b` (`git rev-parse --short origin/main`;
the read-only tree `.claude/worktrees/read-main` does not exist, so the root checkout was used: HEAD = e9d6195b, no
`ai-packages/` change in `git status`). This is a verdict, an input to acceptance. The decisions belong to the Lead.

## Verdicts

| card | verdict |
|---|---|
| **C3-b2** (test_identity) | **dispatchable after listed edits**: R1, R2, R3, R4, R9, R10 (notes R13, R14) |
| **C3-d** (s5_window) | **dispatchable after listed edits**: R6, R8, R9, R10, R12 (e) (note R7) |
| **C3-rr** (reporter_rehearsal_identity) | **dispatchable after listed edits**: R9, R11 (two stale facts), R12 (b) |
| Lead decision F-T11 (a) | **text fix before C3-b2/C3-d go out**: R5 (scope of the residue node, and one unrealizable clause) |

No finding blocks the topic. Every edit below is text in the spec; none needs a new fork except R5 (b), which is the
Lead's.

---

## Findings

### R1 (fix-in-round; C3-b2 item 4; owns) — the `_run_freshness` rows are already pinned, in a file the card does not own

- Item 4 asks for two rows "in `test_proof_level.py` (the existing `run_freshness` table if it has one)". There is none
  there (grep `run_freshness` in `test_proof_level.py`: only :1554-1556, a story import). The table is
  `scripts/tests/test_run_freshness.py` (keep row, `test-layers.json:4702`, before `"quarantine"` :7207), function
  `the_run_is_fresh_or_stale_by_the_code_it_ran` (:73). It already pins both rows the card wants:
  K1 (b) :80-86 "a comment / docstring / blank lines in the test - fresh" (the `instance_code` case) and K1 (f) :104-106
  "a variable renamed in the test - stale" (code differs). K1 (d) :92-96 also pins the WHY_RUN_CHANGED sentence.
- **Edit:** item 4 names K1 (b) and K1 (f) as the existing pins (S-b: "NAMED in the report and no new row"). The one new
  row (unreadable registry -> `stale` with the registry why) goes beside them in `test_run_freshness.py`. `owns:` gains
  `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_run_freshness.py (one row, item 4)`. The expected values
  stay as written (docstring rule 4, :952-960; FR-59).

### R2 (fix-in-round; C3-b2 item 6; FR-41, the F-T11 class) — `_evaluate` prints a why, and F-T11 (a) does not reach it

- `_evaluate` refuses a receipt with a sentence that names a cause: `proof_level.py:1606-1612`, "its receipt is for other
  bytes (...) and other code" or "something the test depends on (...) has changed since, or cannot be told now". Once
  item 6 replaces `if not how:` (:1605) with the predicate, an unreadable registry refuses every receipt with that false
  cause. F-T11 (a) says "a site that prints a WHY (`_run_freshness`, `_match`) names the registry"; F-T10 (a) adds a third
  site that prints a why, and the card does not apply the rule to it.
- The sibling inside the same function family: `_stale_receipt` keeps the bare truthiness (:1898, `not same_test(...)`, a
  produce site). On a broken registry, `reached` gives no level and `_stale_receipt` finds the receipt still "speaking",
  so `probe_freshness` returns `missing` with WHY_PROBE_MISSING (:1966-1971, text :1814-1815, "no receipt of a live check
  reaches this test"). This is a second false cause, and the two readers of one decision then disagree.
- **Edit:** item 6 adds: "when `gate_template.registry_problem()` is non-empty, the issue reads 'the gate registry cannot be
  read (<reason>): a factory defect, the receipt was not judged' instead of the bytes sentence". Add one row to
  `test_proof_level.py`: unreadable registry -> not valid, issue names the registry. E8 names `_stale_receipt` /
  `probe_freshness` `missing` on a broken registry as a known residue of R5's node. The alternative is to give
  `probe_freshness` the same registry branch, but `probe_freshness` is not in owns, so the residue is the cheaper road.

### R3 (fix-in-round; C3-b2 item 5) — one S-b row is in the wrong item, and the F-T11 branch of `_match` has no row

- Item 5's first S-b row ("an old probe record whose identity does not match -> `{"probed": False}`") tests
  `already_probed`, which lives in `test_proof_level.py`. It is not a `_match` row, and `owns` gives
  `test_execution_request.py` "one row".
- `_match` returns `(outcome, why, rank)` (`execution_request.py:2079-2112`), not `""`. Item 5 adds a registry reason on
  F-T11 (a), but no row pins it, and no rank is stated for it.
- **Edit:** move the probe-record row to item 2 (or item 3). Item 5's rows: (i) an earlier job whose instance bytes differ ->
  `("", "instance bytes differ: …", _WHY_RANK["bytes"])`; (ii) the unreadable registry -> `("", <the registry
  reason>, _WHY_RANK["bytes"])`. The rank stays `bytes`, so the order of the first difference is unchanged, as the
  docstring :2081-2083 says. With the registry row, `test_execution_request.py` gets two rows, not one.

### R4 (fix-in-round; C3-b2 item 7; S-f) — the D13 move can be named now; it is not "named by the builder from the measurement"

I measured with `GR.analyse` on in-memory registry copies (script and output in the trail):
- F-T1 (a)'s new words make `proof_level.py:881 same_test verdict == 'same'` a counted item under `test_identity`. The
  triple `("proof_level.py", "same_test", "test_identity")` joins. It is allowed, because `same_test` becomes `produce`.
- Registering `_evaluate` makes `:1613 how in ('instance_code', 'file_code')` counted (+1 triple). Item 6's `allow` entry
  covers it.
- `_run_freshness:939` is counted only while the literal stays, and item 4 removes it. `already_probed:1520` stays, with
  an allow. `_product_receipt_repeat` and `_stale_receipt` hold no row word.
- **Edit:** item 7: "expected: +2 triples (`same_test`, `_evaluate`), `D13_ITEM_COUNT` +2 from the base. A different
  measurement is a stop and a question." This follows S-f's own rule: "its reason is that list, never the scanner's
  number alone".

### R5 (fix the Lead-decision text; FR-57, P31, AR-15) — F-T11's residue node covers one dead end of four, and C3-b2 item 4 promises an owner nothing carries

- **The dead ends.** On an unreadable registry:
  - `validate_window`: a review gap that no critic verdict can close. This is the one the residue node names.
  - `_run_freshness`: every instance that ran reads `stale`, which gives a `stale_run:` gap. Its door is a re-run, and the
    re-run reads `stale` again (acceptance.py:1148, `run_freshness_of(item)[0] == "stale"`).
  - `_evaluate`: every receipt is refused, so the probe runs again, and the new receipt is refused again.
  - `_match` / `already_probed` / `_reporter_outcome`: cost only (they run again), not dead ends.
- **The texts.** The converted sites answer the same cause five ways. Two name the registry (`_run_freshness`, `_match`).
  `validate_window` says "review". `_evaluate` gives a false bytes cause (R2). `already_probed`, `_product_receipt_repeat`
  and `_reporter_outcome` say nothing (C3-rr item 5). That is several roads for one situation (P31, axis 34).
- **The owner.** C3-b2 item 4 and E5 say the registry why is "owner factory". `_run_freshness` returns `(state, why)`, and
  the `stale_run` gap's owner and door come from the window's origin table. Nothing in the card carries an owner, so the
  clause cannot be built.
- **Edit (text, now):** C3-b2 item 4 / E5: "the why names the registry; the `stale_run` gap's owner and door stay as they
  are; the re-run loop is the residue node's". Drop "owner factory".
- **Edit (Lead's, the residue node's scope):** the node covers every converted site, not only `validate_window`.
  **Recommendation (b):** ONE precondition, not a gap kind per window. A story-level read of `gate_template.registry_problem()`
  at story start or stage entry stops with the reinstall door, owner factory, reported and not asked (FR-3). That is one
  survivor (AR-15). It stops every site at once, before any of them can loop, and the per-site text branches of F-T11 (a)
  become belt-and-braces. Cost: one controller block and one row in `state-exits.md`, instead of a window gap kind with a
  controller route. `gate_registry.py:16-19` forbids wiring the A26 AUDIT into the project doctor; a READ of the file is a
  different thing (`load_registry` only parses, :427-447). Both shapes are the Lead's choice. The node needs a pile carrier
  (R11).

### R6 (fix-in-round; C3-d item 1; FR-41 in data) — `decides` must say where `unverified`'s unknown goes

- F-T9 (a) maps `unverified` -> `not_applicable` / `static_review`. The charter says `unverified` is "could not verify"
  (`agents/qa-code-critic.md:76`: "a tool or the stand ... stopped your proof"). That is an unknown in FR-59 terms. The
  window lets it close the REVIEW, because the unknown travels on: `story_step.py finish` derives the `unresolved` pair, and
  S8 lists it as `review_unverified` in "Left with you" (D-0013; `window_record.py:36-41`, :344-351). The new `decides`
  (item 1) does not say this, so the registry data would read "not applicable" for an open unknown.
- **Edit:** item 1's `decides` adds, after "either for one handed to the person": "; `unverified` closes the review only:
  the instance stays unresolved (`story_step.py finish` derives the pair, and the report lists it as left with the person,
  D-0013), so it is never a pass". The verdict_map entry is unchanged. The Lead approved the class word, and this sentence
  is what keeps that word honest.

### R7 (note; C3-d item 6, B9) — the INFO pin already exists

`test_window_record.py:2110` (`line.startswith("expectation changes not measured: ")`) and :2117 pin the line. Item 6's
"only if not pinned" therefore resolves to "named, no new row". Write that into the card now. The literal in that old pin
equals the data row (`handoffs/vocabulary.yaml:300`). Re-sourcing it is optional; recommend leaving it.

### R8 (fix-in-round; C3-d item 7; S-f) — the D13 move is exact, not "at least"

Measured on an in-memory copy (s5_window words `approved`/`unverified`, `verdict` and `build` produce, code unchanged).
The counted items are `acceptance.py:1156, 1161, 1167, 1171` (validate_window) and `window_record.py:1532` (build). Item 4
removes the four, and :1524 / :1625 use the imported name, which A26 cannot see (docstring :63-66). **Edit:** "expected:
+1 triple `("window_record.py", "build", "s5_window")`, `D13_ITEM_COUNT` +1 from the base (exactly :1532)".

### R9 (fix-in-round; C3-rr item 3, C3-b2 items 4-6, C3-d item 5; owns) — the "C3-0 seam" for the broken-registry rows is not a seam the consumers can reach

- C3-0's seam is the `registry=` parameter (C3-0 item 1). The consumer sites call `acceptable(word, consumer)` without it,
  so a test of a consumer must patch C3-0's process cache, and C3-0's card does not name that cache. The builder of C3-0
  (t-1038) chooses it.
- **Edit (each of the three cards):** "the unreadable-registry row patches the registry cache of `gate_template` named in
  C3-0's accepted diff, to the `{"rows": "x"}` reason, and restores it in `finally`. If C3-0 exposes no reset, the node
  stops with a question." Also `owns`: C3-b2 and C3-d own functions only, but each adds an import of `gate_template` to
  `proof_level.py`, `execution_request.py` and `acceptance.py`. Add "and the import line it needs", as C3-rr already does.
- The import-cycle question («Not done (t-1033)») can be closed: `gate_registry.py` imports only stdlib and `hooklib`
  (:97-104). On C3-0's stated design (`gate_template` imports `gate_registry`), a module-top import in the three consumers
  is cycle-free. The builder re-checks it against C3-0's diff.

### R10 (fix-in-round; п. 6 (а) of C3-b2 and C3-d) — the controls as written prove nothing on recorded data; what they rest on must be said

- **C3-b2.** The card's command, run now (verbatim in the trail): all 18 recorded instances read
  `('unknown', 'the run recorded no per-test identity')`. `:939` is never reached. With a spy on `same_test`, `reached()`
  over both recorded manifests (cart-1, 18 rows; local-1-0108, 34 rows) calls it 0 times (every level None). So no
  recorded story exercises `:939`, `:1379`, `:1492`, `:1507` or `:1605`, and "the six lists equal" is vacuous.
  The premise "not a meaning change" rests on a code trace. It holds:
  - `same_test` returns only `raw`, `instance`, `instance_code`, `file_code` or `""` (`proof_level.py:876-893`);
  - the four words are all class `matched` (registry :134-141);
  - every new consumer lists only `matched`, so the predicate is True exactly when the old truthiness was.

  At `:939` both sides are kept, so only `instance`, `instance_code` or `""` reach it (E7 holds).
  **Edit:** the card's Measurement paragraph says this, with the trace, and keeps the run as a smoke check rather than
  evidence.
- **C3-d.** I emulated item 4 on a copy of `acceptance.py`, with a C3-0-shaped predicate over the proposed row. All six
  windows give equal gap lists. A broken consumer (`static_review: ["matched"]`) gives DIFFER on 3 of 6, so the harness can
  fail. The recorded windows exercise only the probe-gapped branch (17 `unverified`) and one ran instance (`approved`,
  failed). The stopped and handed branches rest on item 5's table alone. **Edit:** put this measurement and its limit in
  the card.
- Also measured, for the owner question F-T7 (ii) (not a C3-d edit): `window_record.verdict(..., info)` over the six
  windows gives "run freshness not measured" lines in windows -2, -3, -6, -7 (18 lines) and "expectation changes not
  measured" in -4..-7.

### R11 (Q5; coordination, the Lead's; two card edits) — stale facts

- t-1032 is MERGED (`7f2f6f78 wave: merge … (t-1032)`, before the spec commit e9d6195b). The registry row is debt B-283
  with `_reporter_outcome` accept and `_record_unreadable` produce (`gate-registry.json:499-523`, read). The pins are
  debt 8, K-T1.2 "8" (:247) and `D13_ITEM_COUNT = 140` (:994; `GR.analyse` counts 140 items). The spec still says "in
  flight" and "estimate 140, not verified" (S-f, C3-rr head and E4, §3 wave 2, «Not done»). **Card edits:** C3-rr's head
  says "t-1032 merged (7f2f6f78)". C3-rr item 4 says "the count falls by one from the base (140 after t-1032, plus C3-0's
  library-site comparisons)", not "from t-1032's value". The S-f line numbers drifted by +1..+7 (EXPECTED_DEBT :58,
  K-T1.2 :247, split :336-337, F4 flip :754-756, D13 :913-994). The deltas rule covers that; re-read once.
- The frozen batch `plans/piles/rules-debt/batch-1-phase-2.md` has no carrier for C3-rr, the F-T11 residue node or the
  `holds_over_comments` finding: grep `C3-rr|residue|holds_over` gives no hit, while the positive control
  `B-283|C3-d|s5_window` finds the batch file. Row RD1-7 still describes C3-d by the (ii) direction ("неизмеренный детектор
  -> пробел"). The Lead's §5: findings into a batch that is not taken (TEAMWORK §2).
- Order today: C3-0 (t-1038) is based after t-1032, so S-f holds. S9 (t-1035) owns `window_record.verdict`,
  `controller._s5_gap_problems` and rows in `test_window_record.py`. C3-d follows S9 and C3-b1 on `test_window_record.py`
  and on `validate_window`, serially, so there is no collision. C3-d edits only the registry for `verdict`, and S-f's
  re-measure absorbs any comparison S9 adds there. C3-b1 and C3-b2 on `proof_level.py` are function-disjoint, but both
  may add a module-top import, which is a one-line merge conflict (D-0048, the later node resolves). Nothing goes stale
  except the items above.

### R12 (Q6; class, A1's "a converted row's word compared in an unregistered function"; wait as findings, named in siblings)

- **(a) `probe_verdict`.** The row is converted, with produce-only sites and `accepts: {}` (`gate-registry.json:568-590`).
  Its words are accepted literally in functions no probe_verdict site names: `acceptance.validate_window:1211`
  (`!= "intended_failure"`), `proof_level.already_probed:1463, :1491` (`== "intended_failure"`,
  `in ("no_failure", "wrong_location")`), `_product_receipt_repeat:1378`. After C3-b2 and C3-d, those functions are
  converted accept sites of OTHER rows, and A26 refuses a second registration of a converted accept site
  (`gate_registry.py:831-836`, "give each row its own function"). Any later fix therefore needs a function split. This is
  the designer's noticed "probe comparisons" analog. It is wider than noted, and its structural consequence is new.
  **Edit:** C3-b2 and C3-d `siblings:` name it with that consequence. One finding in the rules-debt pile.
- **(b) `profile_contract.selector_contract:417`.** `if state == "same_command": return result(True, …)` is a second reader of
  `onboarding_probe.earlier_proof`'s word, registered in no row. It decides "selector verified", not reuse, and its own
  docstring bounds the error ("a wrong True never gives a pass", :361-363). **Edit:** C3-rr `siblings:` names it. One
  finding.
- **(c) The critic's review word.** `check_delivery.py:860` and `case_stamp.APPROVING` :317 (its twin `report_facts.APPROVING`)
  accept `{approved, approved_with_fixes}`; the window accepts `approved` only. They are different gates, but they are
  unregistered readers of a word that becomes a registered row word, and A26 cannot see them (non-anchor). Inside the
  window, `window_record.build` (:1524, :1532, :1625) and `GAP_ORIGIN["review"]` (:318-319) carry the per-kind rule as door
  text: three copies beside the registry. A later registry edit would make the door contradict the gate. One finding
  (P31 drift). `build`'s code is outside C3-d's owns.
- **(d) `holds_over_comments`.** No production caller (verified: the def and `tests/test_proof_level.py:1499-1500`).
  F-T10 (a)'s finding stands. It has no carrier yet (R11).
- **(e) SIBLING_MAP.** The cards' siblings say "axis 26-class (one reader of a verdict word)", but axis 26 is "the word
  `stand not confirmed`" (`docs/SIBLING_MAP.md:453`). The map row for this class is axis 5's "Gate rows <-> their sites
  <-> the prose twins of their words" (:143), whose rule is that a change of a row's words walks the prose twins by hand.
  C3-d changes s5_window's words, and C3-b2 (F-T1) changes test_identity's. **Edit:** both `siblings:` lines name axis 5
  :143 and carry one line: "prose twins walked: `skills/qa-story/phases/s5.md:162` …, `references/code-review-rubric.md`:
  checked, no edit (meaning unchanged)". Correct the axis label in C3-rr too.
- **Must any be carded before the three go out?** No. None changes what the three cards do, and (a) is the only one whose
  later fix the cards make dearer. Naming it in siblings is enough.

### R13 (note; C3-b2 item 1, F-T1 (a)) — one row, two producers' vocabularies

After F-T1 (a), `test_identity.words` holds `same_test`'s words and `compare_identity`'s. Then
`acceptable("same", "test_identity.probe_repeat")` is True. Today that cannot happen: `same_test` never returns `same`,
and `compare_identity` never returns `instance`. **Edit:** add an E-row: "INVARIANT: each consumer is fed by exactly one
producer (`probe_repeat`, `run_fresh`, `receipt_holds` <- `same_test`; `run_reuse` <- `compare_identity`)".

### R14 (note; C3-b2 non-goals) — a docstring that would lie

`execution_request.same_instance_bytes`'s docstring names `_match` as one of its "two callers" (:2069-2072). After item 5,
`_match` no longer calls it. **Edit:** allow that one docstring sentence in owns, or the docstring states a false fact.

### R15 (note; C3-0, in flight; no rework) — `registry_problem()` covers an unreadable registry, not a missing consumer

A registry that parses but lacks the consumer or the row's `words`: `acceptable` returns False and `registry_problem`
returns `""`, so the site prints its usual cause. In practice the positive rows of every consumer table (approved -> no
gap, `fresh`, `same_command` reused) turn red on a consumer-id typo, and CI checks the live registry. Say so in F-T11's text;
no change to t-1038.

---

## Answers to the questions

**1. B3, B4, B9, A1.**
- **B3: fully.** `validate_window` stays `accept`. The four comparisons go through the predicate on three consumers, and
  `HANDED_REVIEW_VERDICTS` is deleted (re-grep over the package: only `acceptance.py:34,1161`; control
  `BLOCKED_REVIEW_VERDICT` found in two files). Queue `C3-0 -> C3-d`. Facts re-read: `acceptance.py:33-34, :42-44,
  :1154-1174` hold, and the branch order (stopped -> handed -> gapped -> ran) matches E4.
- **B4: fully in substance, partly in test placement (R1).** `_product_receipt_repeat` (:1365; the test :1378-1379, display
  :1400) and `_run_freshness` (:924; :939) are carded at the right positions. E2 and E7 match the code (:927-938 before
  :939; the verdict check before `same_test` before `_mutated_files_hold`).
- **B9: answered.** The expected value is the data row `vocabulary.yaml:300` with `why` substituted. It is moot, because the
  pin already exists (R7).
- **A1: fully.** t-1032 is merged with the registration (registry read). C3-rr routes :3843 through the predicate, with the
  hit checks first (E3, :3841-3843 read). The class sweep is partly done (R12 (a), (b)).

**2. Dispatchable?** Each card names file, function, behaviour, expected source and edges (limits none; empty/absent
named; TEMPORAL and POSITIONAL present: C3-b2 E1, E2, E4, E7, E10; C3-d E1, E4; C3-rr E3, E4). The exact edits that remain:
- C3-b2: R1, R2, R3, R4, R9, R10 (R13, R14 optional).
- C3-d: R6, R8, R9, R10, R12 (e) (R7 optional).
- C3-rr: R9, R11's two edits, R12 (b) and (e).

The DoD runs are exact (`--check` with the debt-block condition, `--witness-for` the owns, the slow files named for the
canon).

**3. The three shapes.**
- **F-T9 (a).**
  - Keeps: AR-13 (one reader); AR-28 (an absent word is a gap); AR-29 (a data join); FR-59 (the error goes toward a gap;
    the emulation shows the same gaps on recorded data, R10).
  - FR-41 holds only with R6's sentence. FR-57 holds only through R5's node. P31 has residue: three door-text copies of
    the per-kind rule (R12 (c)).
  - What a builder gets wrong: collapsing to one consumer and losing the per-kind split (E4 pins it); the cache seam (R9);
    the D13 number (R8).
- **F-T10 (a).**
  - Keeps: AR-13, AR-28 and AR-29. The error direction is right: the same receipts count, by the code trace of R10.
  - FR-41 breaks on a broken registry until R2's edit.
  - What a builder gets wrong: forgetting the `:1613` allow (A26 F-a, red at once); treating `_stale_receipt` as an accept
    site; the D13 count (R4).
- **F-T11 (a).**
  - Keeps: `registry_problem` is pure and reads through `load_registry` (AR-13); every site errs toward "not accepted"
    (AR-28, FR-59).
  - FR-57: the residue covers one of three dead ends (R5). P31: five answers to one situation (R5). FR-41: `_evaluate`
    and `probe_freshness` (R2).
  - What a builder gets wrong: the "owner factory" clause (R5), which nothing carries.

**4. Meaning changes (п. 6).** No card changes what a field, condition or gate means on recorded stories. C3-d: measured
equal on 6/6 windows, with a negative control. C3-b2: recorded data never reaches the converted lines (measured), so the
no-change claim rests on the code trace (R10). C3-rr: the same words are accepted and refused (`--sites` today: exactly
one item in `_reporter_outcome`, :3843; the after-state is for the builder's control). F-T9's class word changes no
behaviour; its honesty is R6.

**5. Order and collisions.** R11. No collision beyond the module-top import lines on `proof_level.py` (C3-b1 / C3-b2).
The stale items are "t-1032 in flight", the 140 estimate, the line drift, and the batch carriers.

**6. Analogs.** R12. None must be carded first. (a) must be named in the siblings lines because the cards make its later fix
need a function split.

**Standing lines.**
- DUPLICATION AND CONSISTENCY (plan): the per-kind review rule in four carriers after C3-d (R12 (c)); `_evaluate` /
  `_stale_receipt` diverging on a broken registry (R2). Grepped: `approved|unverified|BLOCKED_REVIEW_VERDICT` over
  `scripts/*.py`, `same_command` (case-insensitive) over `scripts/*.py`, `intended_failure|no_failure|wrong_location` in
  `proof_level.py` / `acceptance.py`.
- CODE QUALITY: none found in the planned shapes (one call per decision, no new function except C3-0's).
- ONE ROAD (P31, brief item 12): R5. Five site answers to an unreadable registry is a residue of this class. It leaves as a
  fix of this round (the text) plus a proposed node with its owner, the Lead (scope).
- TESTS (brief question 5): rows only, no new test file. R1 avoids a duplicate row where a pin exists, and R7 likewise.
  C3-d's single table is within volume. No `tests-over:` is owed by the cards as written.

## What I did not check

- C3-0's diff (t-1038, in flight): its cache name and `registry_problem` are taken from the card.
- S9's diff (t-1035): whether it adds `approved`/`unverified` comparisons inside `verdict`. S-f's re-measure covers that.
- C3-b1's text (passed by t-1026; it was context only).
- Whether `pile/live-run-fvf/batch-3` has merged (C3-0's queue line).
- The stopped and handed branches of `validate_window` on real data. None are recorded, so they rest on the tables.
- `test_window_record.py` helpers for building stopped and handed windows. The builder greps.
- No test suite or CI was run (the dispatch limit).

## Trail

Read (on e9d6195b): the spec C3 head and shared items :270-405, C3-0 :529-674 (context), C3-rr :675-772, C3-b2 :917-1029,
C3-d :1032-1166, §3 :1458-1523, forks t-1033 / fix round / not done / Lead decisions :1948-2064; the earlier verdict t-1026
:1-260; `proof_level.py:784,815-975,1365-1625,1640-1680,1720-1775,1810-1816,1886-1910,1955-1980`; `execution_request.py:2060-2120`;
`acceptance.py:25-50,1052-1080,1130-1235`; `window_record.py:28-48,1466-1548,1612-1642,1816-1915` and the def list;
`gate_preflight.py:3822-3872,3950-3975` and the imports; `gate_registry.py:1-80,420-466,485-684,820-842`;
`gate-registry.json` rows test_identity :124-149, s5_window :228-249, reporter_rehearsal_identity :499-523, probe_verdict
:568-590, header :1-7; `test_gate_registry.py:40-64,198-202,247,323-342,728-760,913-1018` (grep); `test_gate_preflight.py:5195-5245`;
`test_run_freshness.py:73-116`; `test_proof_level.py:1336-1390`; `profile_contract.py:345-425`; `check_delivery.py:845-868`;
`case_stamp.py:310-320`; `vocabulary.yaml:290-304`; `agents/qa-code-critic.md:68-86`; `judgment-census.json` (grep);
`docs/SIBLING_MAP.md` (headings, :143, :194, :449-456); S9/FL spec :145-160, :332-346; batch file (grep);
`logs/journal/dev1.jsonl` (grep t-1032..t-1038); `git log origin/main` (25).

Runs (verbatim tails):
- `git -C C:/QAFactory/forge-repo log --oneline origin/main --grep=t-1032` -> `7f2f6f78 wave: merge worktree-agent-abc8139531bba0904 (t-1032)` / `809b1f87 t-1032: C3-R fix round - reporter_rehearsal_identity back to debt (B-283), its reuse acceptance registered`
- `python -B …/scripts/gate_registry.py --sites | grep …` -> `gate_preflight.py:3843  _reporter_outcome  earlier['state'] == 'same_command'  [reporter_rehearsal_identity]` … `proof_level.py:1520  already_probed  hit['holds'] in ('instance_code', 'file_code')  [test_identity]`; `--check` tail: the eight debt rows, `6 gate(s) exempt:`
- the C3-b2 control (the card's command, verbatim) -> `S5-qa-code-critic-2.json ['unknown' x12]`, `-3 ['unknown' x4]`, `-4 []`, `-5 []`, `-6 ['unknown']`, `-7 ['unknown']`
- tally: `18 ('unknown', 'the run recorded no per-test identity')`, `17 ('review', 'unverified', 'passed', True)`, `1 ('review', 'approved', 'failed', False)`
- `same_test` spy over `reached()`: `cart-1 18 rows; levels {'None': 18}`, `local-1-0108 34 rows; levels {'None': 34}`, `same_test returned: {}`
- C3-d emulation (scratchpad `emulate_c3d.py`): six lines `equal`, `equal windows: 6`; negative control (`static_review: ["matched"]`): `-2 DIFFER`, `-3 DIFFER`, `-7 DIFFER`, `equal windows: 3`
- INFO count: `-2 {'run freshness not': 12}`, `-3 {… 4}`, `-4 {'expectation changes not': 1}`, `-5 {… 1}`, `-6 {run freshness 1, expectation 1}`, `-7 {run freshness 1, expectation 1}`
- D13 what-if (scratchpad `d13.py`): base 140; F-T1 words -> `('proof_level.py', 'same_test', ('test_identity',), 881, "verdict == 'same'", True)`; C3-d words -> `acceptance.py` 1156, 1161, 1167, 1171 and `('window_record.py', 'build', ('s5_window',), 1532, "item['review']['verdict'] != 'approved'", True)`; C3-b2 sites -> `_evaluate` 1613, `_run_freshness` 939
- greps with positive controls: `HANDED_REVIEW_VERDICTS` (2 hits; control `BLOCKED_REVIEW_VERDICT` 2 files); pile `C3-rr|residue|holds_over` 0 (control `B-283|C3-d|s5_window` 3 files); `same_command` case-insensitive over `scripts/*.py`; SIBLING_MAP `gate_registry|A26` -> :143 (control `run_freshness` -> :194, :449)

Scratchpad scripts: `C:\Users\i_mas\AppData\Local\Temp\claude\b3e3188b390a00d9\501cb4e0-b55f-46d8-9262-11b1caefad61\scratchpad\emulate_c3d.py`,
`…\scratchpad\emulate_c3d_neg.py`, `…\scratchpad\d13.py`.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "class_completeness": "A1 class swept: probe_verdict is converted with produce-only sites, while its words are accepted in acceptance.validate_window:1211 and proof_level.already_probed:1463/:1491 and _product_receipt_repeat:1378; after C3-b2/C3-d those are converted accept sites of other rows, so a later registration needs a function split (gate_registry.py:831-836). The second same_command reader is profile_contract.selector_contract:417. The critic-word readers check_delivery:860, case_stamp.APPROVING:317 and window_record.build door texts each go to a finding and are named in siblings. None must be carded first. Map: the cards cite axis 26, which is the wrong axis; the right one is axis 5 row :143 (gate rows <-> prose twins), and its prose-twin walk is owed in C3-d and C3-b2. F-T11 residue scope widened to every converted site (R5).",
  "trail": {
    "read": [
      "docs/tasks/specs/20261117-rules-debt-phase2-cards-spec.md (C3 head, C3-0, C3-rr, C3-b2, C3-d, section 3, t-1033 sections)",
      "docs/tasks/specs/reviews/t-1026-rules-debt-wave2-code-and-cards.md",
      "ai-packages/qa-factory/scripts/proof_level.py",
      "ai-packages/qa-factory/scripts/execution_request.py",
      "ai-packages/qa-factory/scripts/acceptance.py",
      "ai-packages/qa-factory/scripts/window_record.py",
      "ai-packages/qa-factory/scripts/gate_preflight.py",
      "ai-packages/qa-factory/scripts/gate_registry.py",
      "ai-packages/qa-factory/references/gate-registry.json",
      "ai-packages/qa-factory/scripts/tests/test_gate_registry.py",
      "ai-packages/qa-factory/scripts/tests/test_gate_preflight.py",
      "ai-packages/qa-factory/scripts/tests/test_run_freshness.py",
      "ai-packages/qa-factory/scripts/tests/test_proof_level.py",
      "ai-packages/qa-factory/scripts/profile_contract.py",
      "ai-packages/qa-factory/scripts/check_delivery.py",
      "ai-packages/qa-factory/handoffs/vocabulary.yaml",
      "ai-packages/qa-factory/agents/qa-code-critic.md",
      "docs/SIBLING_MAP.md",
      "docs/tasks/specs/20261117-rules-debt-phase2-s9-fl-cards-spec.md",
      "plans/piles/rules-debt/batch-1-phase-2.md"
    ],
    "reruns": [
      {"command": "python -B ai-packages/qa-factory/scripts/gate_registry.py --sites (filtered)", "result": "one item in _reporter_outcome (:3843); test_identity only already_probed:1520"},
      {"command": "C3-b2 card control: run_freshness_of over the six recorded windows", "result": "all 18 instances unknown (the run recorded no per-test identity): the control is vacuous"},
      {"command": "same_test spy over reached() on cart-1 and local-1-0108 manifests", "result": "18 and 34 rows, all levels None, same_test called 0 times"},
      {"command": "scratchpad emulate_c3d.py (C3-d item 4 on a copy of acceptance.py)", "result": "6/6 windows equal; negative control DIFFER on 3"},
      {"command": "scratchpad d13.py (GR.analyse on in-memory registry copies)", "result": "base 140; F-T1 adds same_test:881; C3-d leaves build:1532 (+1); C3-b2 adds _evaluate:1613 (+1)"},
      {"command": "window_record.verdict info count over six windows", "result": "run freshness INFO in 4 windows (18 lines), expectation changes INFO in 4"}
    ]
  },
  "fixes": [
    "R1 C3-b2 item 4: name test_run_freshness.py K1 (b) and K1 (f) as existing pins; the registry row goes there; owns + test_run_freshness.py",
    "R2 C3-b2 item 6: the registry branch in _evaluate's issue text plus a row; E8 names the _stale_receipt / probe_freshness 'missing' residue",
    "R3 C3-b2 item 5: move the probe-record row to item 2 or 3; _match rows return ('', why, _WHY_RANK['bytes']) for bytes and for the registry reason",
    "R4 C3-b2 item 7: expected D13 +2 triples (same_test:881 via F-T1, _evaluate:1613), count +2",
    "R5 Lead text: drop 'owner factory' from C3-b2 item 4 and E5; widen the F-T11 residue node to every converted site (rec: one story-level registry precondition)",
    "R6 C3-d item 1: decides says unverified closes the review only and the instance stays unresolved (D-0013)",
    "R8 C3-d item 7: exact D13 +1 triple (build:1532), count +1",
    "R9 all three cards: the broken-registry rows patch C3-0's cache named in its diff, or stop with a question; owns name the gate_template import lines",
    "R10 C3-b2 and C3-d measurement paragraphs: state the code trace (C3-b2) and the emulation result with its branch limit (C3-d)",
    "R11 C3-rr: t-1032 merged (7f2f6f78); the D13 base is 140 plus C3-0's comparisons; batch carriers for C3-rr, the residue node and holds_over_comments are the Lead's",
    "R12 siblings: C3-b2/C3-d name probe_verdict's unregistered acceptances and the split consequence; C3-rr names selector_contract:417; replace the 'axis 26' label with axis 5 :143 and add the prose-twin line"
  ]
}
```
