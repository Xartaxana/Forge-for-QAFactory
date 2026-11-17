
report: C:/QAFactory/forge-repo/docs/tasks/specs/20261117-rules-debt-phase2-cards-spec.md — NOT WRITTEN; the whole fix round is below as text (designer rule 5 fallback)
status: done, but not applied to the file: this worker has whole-file Write only (no Edit). Rewriting the 2,076-line spec by hand would go past the agent budget (WARN 251K at the time) and could corrupt cards this round must not touch. Apply each block below with Edit at its anchor, or re-dispatch with Edit.
questions: 1) F-T12 the precondition's route (rec: person-passable, as AR-9 :111 and FR-4 demand); 2) F-T13 no KNOWN_REFUSALS row (rec); 3) F-T14 "stage entry" = every `dispatch` in `validate` (rec); 4) F-T15 test layer (rec: one table in test_controller_state.py)
needed beyond the manifest: C3-0's tree `.claude/worktrees/agent-aa11322709a274e56/` (no `git show`: there is no shell); `driver_dispatch.py`, `refusal_registry.py`, `test_state_exits.py`, `UPGRADE.md`, the S9/FL spec :334-336, `tools/` greps

=====================================================================
## A. Facts this round rests on (read in t-1043, root checkout; main HEAD 60c41e39 per the session git snapshot, not re-run)

- C3-0 is NOT on main. Glob `ai-packages/qa-factory/scripts/gate_template.py` on the root found nothing; the same Glob over `.claude/worktrees/*/…` found it in `agent-aa11322709a274e56` (positive control).
- That worktree's branch is `worktree-agent-aa11322709a274e56`, ref `a4aca64694799c8c649449d9ce0dd8f054240487` (read from `.git/refs/heads/…`). I read the worktree's checkout, not `git show a4aca646:`, so I could not confirm the tree has no uncommitted edits.
- `gate_template.py` on that tree:
  - :29 `import gate_registry`;
  - :31-37 `_READ = []`, which holds one `(registry, reason)` from `gate_registry.load_registry(gate_registry.PLUGIN_ROOT)`, read once per process; a failure is cached as such;
  - :40-43 `_registry_and_reason`: with `registry=` given, it returns `(registry, structural_error(registry))`;
  - :46 `def registry_problem(*, registry=None) -> str`, which returns "" or the reason, `"it is not available"` when there is no data, or `"it cannot be read (<Exc>)"`, and never raises;
  - :60 `def acceptable(value, consumer, *, registry=None) -> bool`, False on every doubt, never raises;
  - :87-94: the six counted comparisons.
- `test_gate_registry.py` on that tree:
  - :951 has the new triple;
  - :1003-1006 reads `140 -> 146 (C3-0, t-1038)`, `D13_ITEM_COUNT = 146`;
  - :1108-1119 is the cache seam precedent: save `list(GT._READ)`, swap `GR.PLUGIN_ROOT` to an empty dir, `GT._READ.clear()`, restore in `finally`.
- The C3-0 report (on that tree, `docs/tasks/specs/reports/20261117-rules-debt-c3-0-report.md`):
  - :11 has 140 -> 146 with six comparisons, the two `not_applicable` ones included;
  - :54 has an OPEN audit A1 finding, "gate_template.py is reachable from nothing".
- t-1032 is merged on main:
  - `test_gate_registry.py:55-61` EXPECTED_DEBT with `reporter_rehearsal_identity: B-283`;
  - :334-336 split 19/8/6; :247 K-T1.2 "8";
  - :930-932 the `_record_unreadable` / `_reporter_outcome` triples; :991-994 `138 -> 140`, `D13_ITEM_COUNT = 140`;
  - journal `dev1.jsonl:2649` `accepted` t-1032.
  - The merge sha 7f2f6f78 is the critic's run (t-1039), not re-run here.
- Main line numbers in `test_gate_registry.py`: EXPECTED_DEBT :58-61, EXPECTED_CONVERTED :64-69, K-T1.2 :247, split :334-336, F4 flip :753-756 (:760 on C3-0's tree), D13 :913-994.
- `gate-registry.json` on main:
  - test_identity :123-149 (words :135, verdict_map :136-141, status :148);
  - s5_window :227-248;
  - reporter_rehearsal_identity :498-523 (sites :502-506, words :509, status :522).
  - C3-0 adds one line in `provenance_acceptance`, so every later row is +1 on its tree.

=====================================================================
## B. Edits to apply (anchor -> new text)

### B1. C3 shared item S-f, the TEMPORAL paragraph
Anchor: from "TEMPORAL, both worlds: the numbers a card applies are DELTAS" to "(estimate 140, not verified). Every converting card is based on main AFTER t-1032 merges." Replace with:

TEMPORAL, both worlds. The numbers a card applies are DELTAS from the main it is based on, never absolute.

Main at t-1043:
- t-1032 is merged (critic t-1039: `7f2f6f78`). Its pins are on main: `test_gate_registry.py:55-61`, :247 "8", :334-336 (19 converted / 8 debt / 6 exempt), :930-932 (the triples `_record_unreadable` and `_reporter_outcome`), :991-994 (`D13_ITEM_COUNT = 140`).
- C3-0 (t-1038) is not on main yet (Glob: no `gate_template.py` on the root). On its branch `worktree-agent-aa11322709a274e56` (a4aca646) it moves only D13:
  - `D13_TRIPLES` gains `("gate_template.py", "acceptable", "provenance_acceptance")`;
  - `D13_ITEM_COUNT` goes 140 -> 146: six comparisons of `acceptable`, the two `not_applicable` ones included (`test_gate_registry.py:1003-1006` there).

So every converting card is based on main AFTER C3-0 merges, and its D13 base is 146 plus whatever merged in between.

Main line numbers (t-1043): EXPECTED_DEBT :58-61, EXPECTED_CONVERTED :64-69, K-T1.2 :247, split :334-336, F4 flip :753-756 (C3-0 rewrites it; :760 on its branch), D13 :913-994. The F4 `code` list (:729-738) and K-T1.14 (:322) were not re-read.

### B2. C3-rr
- Heading: replace "after t-1032 and C3-0" with "after C3-0 (t-1032 merged)".
- First paragraph: replace "The fix round t-1032 (in flight: registry and tests only) puts the row back to" with "The fix round t-1032 is merged (critic t-1039: `7f2f6f78`; pins on main, S-f). It put the row back to". After "keeps the t-1009 test row as the pin." add: "Row on main: `gate-registry.json:498-523` (status :522; `_reporter_outcome` accept :503, `_record_unreadable` produce :504); +1 line after C3-0. The reuse decision is still `gate_preflight.py:3843` (`_reporter_outcome` :3824-3869), re-read in t-1043."
- `given:`: "row `reporter_rehearsal_identity`, :498-521 on 2151eeef; t-1032 moves it" becomes "row `reporter_rehearsal_identity`, :498-523 on main (t-1043)". Add "`gate_template.py` on C3-0's tree (:29-57)".
- `siblings:`: replace "axis 26-class (one reader: `gate_template.acceptable`)" with "axis 5 (`docs/SIBLING_MAP.md:143`, gate rows <-> sites <-> prose twins): the row's words do not change, so no prose twin is walked. Waiting finding (R12 (b)): `profile_contract.selector_contract:417` (`if state == "same_command": return result(True, …)`) is a second reader of `onboarding_probe.earlier_proof`'s word, registered in no row. It decides 'selector verified', not reuse, and its docstring bounds the error (:361-363, 'a wrong True never gives a pass … Error direction: False when in doubt'). One finding in the rules-debt pile, not carded."
- Item 3: replace "(through C3-0's seam, e.g. monkeypatching the registry `gate_template` reads to `{"rows": "x"}`)" with:
  "The unreadable-registry row patches the registry cache of `gate_template` named in C3-0's accepted diff. At a4aca646 that is `_READ`, a module list holding one `(registry, reason)` pair (`gate_template.py:31-37` there). Save `list(GT._READ)`, set `GT._READ[:] = [({"rows": "x"}, GR.structural_error({"rows": "x"}))]`, and restore it in `finally` (precedent: `test_gate_registry.py:1108-1119` on that branch). If the merged C3-0 names the cache otherwise, use that name; if it exposes no cache, the node stops with a question."
- Item 4: replace "and the count falls by one from t-1032's value" with "and the count falls by one from the base (140 after t-1032, 146 after C3-0's library-site comparisons, a4aca646, S-f; plus whatever merged between C3-0 and this node)".
- Item 5: append "(R5/R15) An unreadable registry is stopped earlier, at the next dispatch, by C3-reg-precondition. Inside a stage that began before, this branch rehearses with no word about the registry: cost only, not a dead end (critic t-1039 R5). `registry_problem()` does not cover a registry that parses but lacks the consumer; there `acceptable` is False and the command is rehearsed (C3-0 R15 note, F-T11)."
- E4: replace "before C3-rr (t-1032's world)" with "before C3-rr (main since t-1032 merged)". Replace "C3-rr cannot be built before C3-0 merges (`gate_template.py` is absent until then)" with "C3-rr cannot be built before C3-0 merges (`gate_template.py` is absent on main at t-1043: Glob, with the worktree hit as the control)".
- Import: add to item 2: "Module-top `from gate_template import acceptable` is cycle-free: `gate_registry.py` imports only stdlib and `hooklib` (:97-104), and `hooklib` only stdlib (`hooklib.py:2-13`). The builder re-checks against the merged C3-0."

### B3. C3-b2
- `owns:` (replace the five lines):
  - `C:/QAFactory/forge-repo/ai-packages/qa-factory/references/gate-registry.json` (row `test_identity` only, :123-149 on main, +1 after C3-0: `accepts`, words (F-T1 (a)), sites, status)
  - `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/proof_level.py` (`already_probed`, `_product_receipt_repeat`, `_run_freshness`, `_evaluate` (F-T10 (a), decided), and the import line it needs)
  - `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/execution_request.py` (`_match` and the import it needs; ONE docstring sentence of `same_instance_bytes`, :2069-2072, R14; `green_over_same_bytes` only as re-roled in the registry, F-T1 (a))
  - `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_proof_level.py` (rows: item 2 one, item 3 one, item 6 two)
  - `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_execution_request.py` (two rows, item 5)
  - `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_run_freshness.py` (one row, item 4)
  - `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_gate_registry.py` (S-f pins of `test_identity` only)
- `non-goals:`: replace "`same_instance_bytes` (it keeps serving …)" with "the code of `same_instance_bytes` (it keeps serving `_same_identity_for_count`, the budget side; only its docstring sentence that names `_match` as a caller changes, R14)". Replace "`holds_over_comments` and `_stale_receipt` (F-T10)" with "`holds_over_comments` (finding, F-T10 (a)); the code of `_stale_receipt` (registered `produce` only) and `probe_freshness` (R2 residue, E8)".
- `siblings:` (append):
  - "axis 5 (`docs/SIBLING_MAP.md:143`): F-T1 (a) changes `test_identity`'s words. The axis's prose twins (`references/execution-lifecycle.md` + slice, `manual-evidence.md`, `environment-preparation.md`, `phases/s5.md`/`s6.md`) are walked by the builder by grep for `instance_code|file_code|same_test|compare_identity`. Each hit gets a report line 'checked, no edit (meaning unchanged)' or an edit named as a finding. Not walked by the designer."
  - "Waiting findings (R12): (a) `probe_verdict`'s words are accepted in functions no probe_verdict site names: `proof_level.already_probed:1463` (`== "intended_failure"`) and :1491 (`in ("no_failure", "wrong_location")`), `_product_receipt_repeat:1378`, and `acceptance.validate_window:1211`. After C3-b2/C3-d those functions are converted accept sites of other rows, and A26 refuses a second registration of a converted accept site (`gate_registry.py:831-836`, 'give each row its own function'). Any later fix therefore needs a function split. One finding. (d) 'delete or wire `holds_over_comments`' (no production caller; F-T10 (a)). One finding."
- Item 2: append "S-b row (moved from item 5, R3) in `test_proof_level.py`: an old probe record (`no_failure`) whose identity does not match the test now -> `already_probed` answers `{"probed": False}` (the probe runs). Expected from: the row's `decides` (`gate-registry.json:125`)."
- Item 4: replace whole with:
  "4. **`_run_freshness`.** The test at :939 becomes `if acceptable(same_test(now, {"instance_identity": dict(shas, job_id="")}), "test_identity.run_fresh"): return "fresh", ""`. On False the `stale` return stays, with its why `WHY_RUN_CHANGED` (:903, :941-942). On F-T11 (a), when `gate_template.registry_problem()` is non-empty, the why names the registry instead: 'the gate registry cannot be read (<reason>): a factory defect, not a change of the test'. The why names the registry; the `stale_run` gap's owner and door stay as they are (`_run_freshness` returns `(state, why)` only; the gap's owner and door come from the window's origin table). The re-run loop is the node C3-reg-precondition's.
  Pins (R1): `test_proof_level.py` has no run_freshness table (critic grep: only :1554-1556, an import; not re-read here). The table is `scripts/tests/test_run_freshness.py` (keep, layer `gate_named`, `test-layers.json:4702`), function `the_run_is_fresh_or_stale_by_the_code_it_ran` (:73). It already pins both rows: K1 (b) :80-86 (a comment, docstring or blank lines in the test -> fresh, the `instance_code` case) and K1 (f) :104-106 (a variable renamed -> stale). K1 (d) :92-98 pins the `WHY_RUN_CHANGED` sentence. These are NAMED in the report and get no new row (S-b). ONE new row beside them: the unreadable registry (the `gate_template` cache patched as in C3-rr item 3, restored in `finally`) -> `stale`, with a why that names the registry and does not say 'changed since'. Expected from: the docstring rule list of `run_freshness` (`proof_level.py:952-960`, rule 4) and FR-59."
- Item 5: replace whole with:
  "5. **`_match`.** Inside the same `author_run_reading != "per_story"` condition (`execution_request.py:2099-2103`), `not same_instance_bytes(a, b)` becomes `not acceptable(proof_level.compare_identity(a, b)[0], "test_identity.run_reuse")` (`import proof_level` in the function, as `same_instance_bytes` does at :2074; `from gate_template import acceptable`). The return stays `("", <why>, _WHY_RANK["bytes"])`. The why is 'instance bytes differ: …' (:2102-2103) or, when `registry_problem()` is non-empty, 'the gate registry cannot be read (<reason>): a factory defect, the earlier run was not judged'. The rank stays `bytes` in both cases, so the order of the first difference is unchanged (docstring :2080-2082). Two rows in `test_execution_request.py`: (i) an earlier job whose instance bytes differ -> `("", "instance bytes differ: …", _WHY_RANK["bytes"])`; (ii) the unreadable registry (cache patched, restored in `finally`) -> `("", <a why that names the registry>, _WHY_RANK["bytes"])`. Expected from: the row's `decides` (:125) and the docstring's order, never from `_match`'s output before the change. The R14 docstring sentence: `same_instance_bytes`'s 'the two callers fold it … `_match` …' (:2070-2072) is rewritten to name its one caller, `_same_identity_for_count`, and to say that `_match` reads `compare_identity` through the predicate."
- Item 6: replace "(t-1033, on F-T10 (a))" with "(F-T10 (a), decided)". After "`_stale_receipt` registered `produce` (it builds a why)." insert:
  "On F-T11 (a) (R2): when `gate_template.registry_problem()` is non-empty, the issue reads 'the gate registry cannot be read (<reason>): a factory defect, the receipt was not judged' instead of the bytes sentence (:1606-1612)."
  Replace "One row in `test_proof_level.py`: a receipt for other code -> not valid." with "Two rows in `test_proof_level.py`: a receipt for other code -> not valid; the unreadable registry (cache patched) -> not valid, and the issue names the registry, not 'other bytes'."
- Item 7: replace from "D13 re-measured with `GR.analyse` before and after:" to the end with:
  "D13 re-measured with `GR.analyse` before and after. Expected: +2 triples:
  - `("proof_level.py", "same_test", "test_identity")`: `:881 verdict == 'same'` is counted once F-T1 (a)'s words land; allowed, because `same_test` becomes `produce`;
  - `("proof_level.py", "_evaluate", "test_identity")`: `:1613 how in ('instance_code', 'file_code')`, covered by item 6's `allow`.

  `D13_ITEM_COUNT` +2 from the base (146 after C3-0, plus what merged since; S-f). `_run_freshness:939` is not counted after the change (its literal is gone). `already_probed:1520` stays counted, with its allow. `_product_receipt_repeat` and `_stale_receipt` hold no row word (critic t-1039 R4, `GR.analyse` on in-memory copies; not re-run here). A different measurement is a stop and a question."
- E5: replace with "E5 (unreadable registry): every reuse is refused, so the probe or run happens (cost, never a false pass). Every run reads `stale`, so each instance that ran gets a `stale_run:` gap. The why names the registry (F-T11 (a)); the `stale_run` gap's owner and door stay as they are; the re-run loop is the node C3-reg-precondition's. INVARIANT: a broken registry never lets an old result or probe speak for a test."
- E8: append "`_evaluate`'s issue and `_match`'s why name the registry (items 5, 6). Known residue (R2): `_stale_receipt` keeps the bare truthiness (a produce site, :1898). On a broken registry `probe_freshness` therefore returns `missing` with `WHY_PROBE_MISSING` (:1814, :1972), a second false cause. Its code is not in owns. C3-reg-precondition closes it in practice (no dispatch on a broken registry); inside a stage that began before, it stays a residue named in that node."
- New E11 (R13): "E11 (one row, two producers' vocabularies, F-T1 (a)): after F-T1 the row's `words` hold both `same_test`'s words and `compare_identity`'s, so `acceptable("same", "test_identity.probe_repeat")` is True. That cannot happen today: `same_test` never returns `same` (:876-892), and `compare_identity` never returns `instance` (:834-847). INVARIANT: each consumer is fed by exactly one producer (`probe_repeat`, `run_fresh`, `receipt_holds` <- `same_test`; `run_reuse` <- `compare_identity`). A call that feeds a consumer another producer's word is a review finding."
- `edges:` header line: "E1-E10" becomes "E1-E11".
- Measurement paragraph (R10): replace with:
  "Measurement (п. 6 (а)). The command below, run by critic t-1039 (verbatim in its trail), gives all 18 recorded instances `('unknown', 'the run recorded no per-test identity')`. With a spy on `same_test`, `reached()` over both recorded manifests (cart-1, 18 rows; local-1-0108, 34 rows) calls it 0 times. So no recorded story reaches `:939`, `:1379`, `:1492`, `:1507` or `:1605`, and 'the six lists equal' is vacuous. The run stays as a smoke check, not as evidence.
  The premise 'not a meaning change' rests on a code trace, re-read in t-1043:
  - `same_test` returns only `raw`, `instance`, `instance_code`, `file_code` or `""` (`proof_level.py:876-892`);
  - the four words are all class `matched` (`gate-registry.json:136-141`);
  - every new consumer lists only `["matched"]`, so the predicate is True exactly when the old truthiness was.

  At `:939` both sides keep their identity (:929-938), so only `instance`, `instance_code` or `""` reach it (E7). The command: (unchanged)."

### B4. C3-d
- `owns:`: acceptance.py line gets "and the import line it needs". The test_window_record.py line becomes "(one table of rows, item 5; item 6: no row, the pin exists, R7)".
- `siblings:` (append):
  - "axis 5 (`docs/SIBLING_MAP.md:143`, gate rows <-> sites <-> prose twins), not 'axis 26' (`docs/SIBLING_MAP.md:453` is the word `stand not confirmed`). C3-d changes `s5_window`'s words. Prose twins walked: `skills/qa-story/phases/s5.md:162` ('records the verdict `unverified`' for a probe that cannot run here) and :184 ('the critic's `approved` stands'); `references/code-review-rubric.md:92-93` ('`unverified` is not a pass … only for a window where the test could not run'): checked, no edit (meaning unchanged)."
  - "Waiting findings (R12): (a) `probe_verdict`'s words accepted in `validate_window:1211` and in `proof_level` (see C3-b2 siblings); a later fix needs a function split (`gate_registry.py:831-836`). (c) The critic's review word is read outside the registry: `check_delivery.py:860` and `case_stamp.APPROVING` :317 (twin `report_facts.APPROVING`) accept `{approved, approved_with_fixes}`. Inside the window, `window_record.build` (:1524, :1532, :1625) and `GAP_ORIGIN["review"]` (:318-319) carry the per-kind rule as door text: three copies beside the registry (P31 drift; `build`'s code is outside owns). One finding each, not carded. (Not re-read in t-1043: check_delivery:860, case_stamp:317, window_record:318-319.)"
- Item 1 (R6): after "either for one handed to the person" insert "; `unverified` closes the review only: the instance stays unresolved (`story_step.py finish` derives the pair, and the report lists it as left with the person, D-0013), so it is never a pass". The charter fact behind it: `agents/qa-code-critic.md:76` says `unverified` is 'could not verify'. `window_record.py:36-41` and :344-351 (PROBE_GAP_KIND, 'S8 reads it as the critic's `unverified`') were re-read. The verdict_map entry is unchanged.
- Item 5 (R9): replace "the unreadable registry (C3-0 seam)" with "the unreadable registry (the `gate_template` cache patched as in C3-rr item 3, restored in `finally`; if the merged C3-0 exposes no cache, the node stops with a question)".
- Item 6 (R7): replace "Only if not pinned (the builder greps … first)." with "Already pinned: named, no new row. `test_window_record.py:2110-2111` (`line.startswith("expectation changes not measured: ")`) and :2117 (the CLI prints the note) pin the line. The literal in that pin equals the data row (`handoffs/vocabulary.yaml:300`, `not_measured: "not measured: {why}"`). Re-sourcing it is optional; recommended: leave it."
- Item 7 (R8): replace from "D13 re-measured with `GR.analyse` before and after:" to the end with:
  "D13 re-measured. Expected: +1 triple `("window_record.py", "build", "s5_window")`, `D13_ITEM_COUNT` +1 from the base (exactly `:1532 item["review"]["verdict"] != "approved"`).
  - The four comparisons of `validate_window` (`acceptance.py:1156, 1161, 1167, 1171`) are removed by item 4.
  - :1524 and :1625 use the imported `BLOCKED_REVIEW_VERDICT` (`window_record.py:75`), which A26 cannot see (docstring `gate_registry.py:63-66`).

  Critic t-1039 measured this on an in-memory copy; not re-run here. A different measurement is a stop and a question."
- E3: replace "fork F-T11 (the Lead decides whether a window-level registry gap with its own door is a node)" with "F-T11 (a) + R5 (b), decided: the dead end is closed by C3-reg-precondition (no dispatch starts while the file cannot be read). Inside a stage that began before, the gap stays, and the per-site why branches are belt-and-braces".
- Measured premise (R10): append "(t-1043, critic t-1039 R10) The review acceptance was emulated on a copy of `acceptance.py` with a C3-0-shaped predicate over item 3's row: all six windows give equal gap lists. A broken consumer (`static_review: ["matched"]`) gives DIFFER on 3 of 6, so the harness can fail. Limit: the recorded windows exercise only the probe-gapped branch (17 `unverified`) and one ran instance (`approved`, failed). The stopped and handed branches rest on item 5's table alone. For F-T7 (ii) (owner question, no edit): `window_record.verdict(..., info)` gives 'run freshness not measured' in windows -2, -3, -6, -7 (18 lines) and 'expectation changes not measured' in -4..-7."

### B5. NEW CARD — insert after C3-d, before "#### C3-e — folded into C3-R (item 3)"

#### C3-reg-precondition — one stop when the gate registry cannot be read (F-T11 residue, critic t-1039 R5 (b), Lead 17.11) — after C3-0; controller.py queue after FL4

Why: with an unreadable registry, every converted site refuses, and three of them loop: `_run_freshness` gives a stale_run gap whose re-run reads stale again; `_evaluate` refuses every receipt, so the probe runs again; `validate_window` gives a review gap no verdict closes. They also answer the same cause five ways (P31). This card puts one survivor in front of all of them (AR-15). The per-site why branches of C3-b2/C3-d stay as belt-and-braces (Lead decision).

given: `C:/QAFactory/forge-repo/ai-packages/qa-factory/design/factory-rules.md` (whole), `C:/QAFactory/forge-repo/plans/builder-rules.md`, `C:/QAFactory/forge-repo/docs/TESTING.md`; this card; the accepted C3-0 card and its diff (`gate_template.py`: `registry_problem(*, registry=None) -> str`, cache `_READ`). Read, under `C:/QAFactory/forge-repo/ai-packages/qa-factory/`:
- `scripts/controller.py:5364-5377` (validate head), `:5493-5529` (dispatch branch head), `:5185-5189` (`apply` runs `validate` in the commit), `:2470-2482` (`_passed_by_person`), `:5612` (a dispatch-branch use of it), `:2109-2147` (`prepare`, read-only), `:9206-9236` (the stage loop's `prepare_stage`);
- `scripts/gate_registry.py:16-19, 97-106, 427-456`;
- `design/controller-blocks.md:1-38` and rows :50-53 (the row form);
- `design/state-exits.md:1-20, 138-143`;
- `scripts/tests/test_state_exits.py:43-54, 124-128`;
- `scripts/refusal_registry.py:41-44` (controller.py is one `operation` entry);
- `scripts/driver_dispatch.py:38-107` (KNOWN_REFUSALS, unchanged);
- `UPGRADE.md:71-90` (the reinstall steps);
- seam precedent: `scripts/tests/test_gate_registry.py:1108-1119` on C3-0's branch.

owns:
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/controller.py` (`Controller.validate`, the `dispatch` branch only: one block and the import it needs) — HOT
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/design/controller-blocks.md` (one row in source order; the header counts it moves)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/design/state-exits.md` (one row in "What an infrastructure failure leaves", :138)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_controller_state.py` (one table, item 4)

non-goals:
- `gate_template.py`, `gate_registry.py`;
- any call of `gate_registry.analyse` / `--check` / `main` from the controller (`gate_registry.py:16-19`), and `audit_factory.py` (the doctor);
- `gate-registry.json`, `test_gate_registry.py` (no row-word comparison is added; D13 unchanged), `judgment-census.json` (no new unit);
- `driver_dispatch.KNOWN_REFUSALS` (F-T13 (a)); `prepare`, `next_action`, `_next_action_for_state` (F-T14 (a));
- the `accept` / `checkpoint` / `resume` / `initialize` branches;
- the per-site texts of C3-b2/C3-d;
- `docs/SIBLING_MAP.md` (its axis-5 line is the Lead's at acceptance, item 5).

handoff: report path given by the Lead
edges: E1-E11 below
DoD: `python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/gate_registry.py --check` exits 0 (no registry edit; the debt block unchanged). Then `python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/controller.py C:/QAFactory/forge-repo/ai-packages/qa-factory/design/controller-blocks.md C:/QAFactory/forge-repo/ai-packages/qa-factory/design/state-exits.md C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_controller_state.py`, and the printed non-slow files. `test_controller_state.py` and `test_controller_blocks.py` are `test_controller_*` (builder-rules 7b): judged by the batch canon and named in the report. `test_state_exits.py` is run if printed and not slow.
siblings: axis 5 (`docs/SIBLING_MAP.md:143`): this is the one stop for "the registry cannot be read" (AR-15: a new survivor is named on its axis, item 5). The per-site texts (C3-b2 items 4-6, C3-d E3) are belt-and-braces. `_stale_receipt` / `probe_freshness` `missing` is the residue named in C3-b2 E8. Open C3-0 finding (its report :54): audit A1 says `gate_template.py` is reachable from nothing; whether this import from `controller.py` (a CLI script) clears it is not established.
designer: `C:\QAFactory\forge-repo\docs\tasks\specs\20261117-rules-debt-phase2-cards-spec.md` (C3-reg-precondition, t-1043)

Items:
1. **The block.** In `validate`'s `dispatch` branch, right after the contract check `required` (:5515-5517: `raise ValueError("dispatch contract incomplete")`) and before the closure test (:5518-5523):
   - read `problem = registry_problem()` (`from gate_template import registry_problem` at the point of use, the file's "late" import style);
   - when it is non-empty, build one text with the stable prefix `gate registry unreadable:`, e.g. "gate registry unreadable: the plugin's references/gate-registry.json cannot be read (<problem>). Owner: factory - a defect of the install, not of the story; nothing is wanted from you. Reinstall or update the qa-factory plugin (UPGRADE.md, step 3), then start the stage again. No stage starts until the file reads, because every reuse and review acceptance reads it.";
   - pass it through `blocking, _ = self._passed_by_person(p["stage"], [text])`, as the branch's other blocks do (:5612), and `raise StateConflict(blocking[0])` when it is still blocking (F-T12 (a)).

   The text reports and does not ask (FR-3: a factory reason is never put as a choice); the person's word is the standing FR-4 road. The builder reads `waiver.split_overridden` for whether a pass over a factory-owned block is filed as a factory finding (FR-4); this was not read here. Expected from: AR-28 / FR-59 (an unknown never becomes a pass at a stage boundary), FR-4, AR-9's change check (`architecture.md:111`: the door and the person's-word route), the Lead decision R5 (b).
2. **controller-blocks.md row** (source order, beside the other `validate` rows): `| \`validate\` | \`StateConflict\` | gate registry unreadable: the plugin's references/gate-registry.json cannot be read | \`person\` | a factory defect (FR-3): reinstall or update the plugin, then start the stage again; a person's recorded words pass it (\`waiver.py --stage <S> --block "gate registry unreadable" --words-file <file>\`), and the stage then runs with every converted site refusing reuse (C3-0 E2) |`. The header counts (352 blocks, route `person` 17, `controller-blocks.md:3,20`) move by one. If `tools/controller-blocks-gen.py` places the row, its output is used. If `test_controller_blocks.py` does not pin the header counts, they still move (the file is the walk).
3. **state-exits.md row** in "What an infrastructure failure leaves" (:138-143): `| a story whose next dispatch is refused because the plugin's \`references/gate-registry.json\` cannot be read (absent, 0 bytes, not UTF-8, not JSON, duplicate keys, not an object, no \`rows\` list) | a broken or partial install or update of the plugin | reinstall or update the plugin (UPGRADE.md step 3); the next \`dispatch\`, in a new process, reads the file again and goes through; a person's recorded word passes it (\`waiver.py\`) | \`test_controller_state.py\` |`. `test_state_exits.py` reads the first backticked token of column 1 (:43-54); extra names are harmless. The doors it checks (`dispatch`, a test file on disk, :124-128) exist.
4. **Test: one table in `test_controller_state.py`** (keep, layer `detector`, covers `controller.py`, `test-layers.json:1082`). The builder greps for an existing dispatch-refusal table first. If there is none, it adds one parameterised function (no new file). Rows (id -> expected):
   - `absent`: `gate_registry.PLUGIN_ROOT` swapped to an empty temp dir and `gate_template._READ.clear()` (restored in `finally`, the precedent seam) -> the dispatch is refused with `StateConflict`, the text starts with `gate registry unreadable:`, names "the file is absent", and the journal records no dispatch;
   - `zero-bytes`, `not-json`, `not-utf8`, `no-rows`: `_READ[:] = [(None, <the load_registry reason>)]` or `[({"rows": "x"}, "it carries no `rows` list")]` -> refused, each naming its reason;
   - `passed-by-word`: `no-rows` plus a recorded waiver for the block `gate registry unreadable` -> the dispatch is recorded;
   - `live`: the live registry -> the dispatch is recorded (control);
   - `malformed-first` (POSITIONAL): `no-rows` and a request missing `input_hash` -> `ValueError("dispatch contract incomplete")`, not the registry text;
   - `after-reinstall` (TEMPORAL): refused; then the root restored and `_READ` cleared -> the next dispatch is recorded.

   Expected from: AR-28, FR-4 and the decided text above; never from the code's output.
5. **SIBLING_MAP axis-5 line (the Lead's, at acceptance):** "one stop for an unreadable registry: `controller.validate` dispatch branch via `gate_template.registry_problem()` (C3-reg-precondition); per-site why texts are belt-and-braces". It is a mechanism path (`tools/mechanism_gate.py`, 7 `SIBLING_MAP` hits; prefix not read), so the builder reports it under "Needed from integration".

architecture content: `architecture: AR-9, AR-13, AR-15, AR-25, AR-28 -- <how kept>`, in the gate's own form (`tools/architecture_gate.py`; the grammar is not copied here). Points:
- AR-9: the refusal names what it expected and two doors (reinstall; the person's word). Change check `architecture.md:111`: controller-blocks row, `test_controller_blocks.py`, `refusal_registry.py --check` (controller is one `operation` entry, `refusal_registry.py:41-44`).
- AR-13: read only through `load_registry`, via `registry_problem()` (:166).
- AR-15: one survivor, named on axis 5 (:180).
- AR-25: a `state-exits.md` row with its reversing command (:261).
- AR-28: an unreadable registry never becomes a pass at a stage boundary, pinned by item 4 (:282).
- AR-29 (:155): the check is class `shape` (a package file reads and has `rows`), owner data; it sits in the existing unit `controller.py::validate` (`judgment-census.json:245`, shape/data), so there is no new census row. If the builder places the raise in a helper (a new unit), the node stops with a question.
- judgment: `judgment: none -- a readability check of a package data file inside the existing shape unit controller.validate; the person's pass is the existing waiver road`. Per check: the readability check serves DATA (code), census class shape; the pass serves INTENT (the person, FR-4).

Edges:
- E1 (empty / absent): an absent file, 0 bytes or no `rows` gives a reason, so the dispatch is refused. INVARIANT: no stage starts on a registry that cannot be read (AR-28).
- E2 (present but incomplete, R15): `registry_problem()` covers a registry that cannot be read, not a missing consumer. A file that parses, with `rows`, but lacks a consumer, `words` or `verdict_map` gives "", so the precondition passes; the site's `acceptable` is False and the site prints its usual cause. INVARIANT: the precondition never stops a registry that reads (no false stop). That blind spot is held by CI (A26 `--check`; the positive rows of every consumer table turn red on a consumer-id typo).
- E3 TEMPORAL:
  - (i) the registry appears after a reinstall. `gate_template` caches per process, and a failure is cached as such (`_READ`, :31-37 at a4aca646). A CLI call is a new process, so the next call reads the file again. The driver imports `controller` in-process (`driver_dispatch.py:2141` and others), so a driver running across a reinstall keeps the cached failure until it restarts. UPGRADE.md:71 asks to stop active factory work before a reinstall; the door says "then start the stage again".
  - (ii) Before C3-0 merges, `gate_template.py` is absent, so this node cannot be built (order).
  - (iii) Before this node, a broken registry loops at the sites (R5); after it, the first dispatch stops.
  - INVARIANT: a fixed registry is read by the next process, and a cached failure only ever stops, never passes.
- E4 POSITIONAL: after `validate_record("Dispatch", p)`, the running-dispatch refusal (:5501-5514) and `required` (:5515-5517); before the closure test (:5518-5523) and every later check. INVARIANTS:
  - (i) a malformed request is still refused as `ValueError` first (the call's fault before the install's, FR-46);
  - (ii) the running-dispatch refusal keeps its text byte for byte (finishing a running dispatch is an `accept`, which is not blocked);
  - (iii) no dispatch is committed while the file cannot be read, on any road that commits one: `story_step.py start`, `rework`, relaunch and retry packets, the driver. All of them go through `apply` -> `store.commit` -> `validate` (:5188);
  - (iv) the closure test and every later check still run on an admitted dispatch;
  - (v) the block reads only `p["stage"]`, which `required` guarantees.
- E5 one road (P31, AR-15): one precondition for every stage and role alike, keyed on no stage, language or project; no per-site variant.
- E6 (not covered, by design): `accept`, `checkpoint` and `resume` of an admitted dispatch (the stage is already entered; its sites refuse with the registry why), and `initialize` (it runs no converted site). INVARIANT: a broken registry is a pass nowhere (the sites err toward not-acceptable, C3-0 E2); the precondition only stops it early.
- E7 doctor separation: this is a read through `registry_problem()` (`load_registry` + `structural_error`, `gate_registry.py:427-456`), never `analyse`, `--check` or `main`. `gate_registry.py:16-19` forbids the A26 AUDIT in the project doctor; a read is not the audit. INVARIANT: no A26 audit runs in a project.
- E8 (limit): none introduced. The reason is passed whole; `load_registry`'s sentences are short, and a JSON error carries its position.
- E9 (cost): one file read and parse per process at its first dispatch (cached); nothing on other operations.
- E10 (conflicts):
  - `controller.py` is HOT: S9 owns `_s5_gap_problems`; FL4 owns `BINDING_KEYS`, `build_rework_request` and `main`'s rework parsing (S9/FL spec :334-336). This node owns `validate`'s dispatch branch: function-disjoint.
  - `controller-blocks.md` is row-disjoint, but the header counts are shared if S9/FL4 add blocks: the later merger re-derives them (D-0048).
  - `очередь: S9 → FL4 → C3-reg-precondition` (controller.py, controller-blocks.md); `C3-0 → C3-reg-precondition` (gate_template).
- E11 (driver): the refusal matches no `KNOWN_REFUSALS` row (`driver_dispatch.py:38-107`), so it goes to the conductor (FR-48, F-T13 (a)). The conductor cannot reinstall; it reports the defect (FR-3). INVARIANT: no silent pass and no question about our own defect; the same refusal repeats until the reinstall.

Measurement (п. 6 (а)): not a meaning change for any story on a sound install (`registry_problem()` is "" on the live registry: the C3-0 row "registry-problem: the live registry", `test_gate_registry.py:1124` on its branch). Not measured here (no shell).

### B6. §3 Waves
- Wave 2: replace "its fix round **t-1032** is in flight now" with "its fix round **t-1032** is merged (critic t-1039: `7f2f6f78`)".
- Wave 2½: append "C3-0 built at a4aca646 (branch `worktree-agent-aa11322709a274e56`), not on main at t-1043".
- Wave 3: add the bullet "- **C3-reg-precondition** (controller `validate` dispatch branch, controller-blocks.md, state-exits.md, test_controller_state.py) after C3-0; on controller.py after S9 and FL4."
- Collisions: "`controller.py` (HOT): S9 → FL4" becomes "S9 → FL4 → C3-reg-precondition (also `design/controller-blocks.md` header counts)".
- The order line "t-1032 -> C3-0 -> C3-rr …" stays: C3-reg-precondition does not touch `test_gate_registry.py`.

### B7. §5 rows (into an untaken batch; NOTE: `plans/piles/rules-debt/` holds only `batch-1-phase-2.md` (Glob), and a grep there for `C3-rr|residue|holds_over|reg-precondition|RD1-7` finds only `RD1-7` (:18, :35, :45, the control). So C3-rr, the residue node and the findings have no carrier yet: the Lead/integrator opens one.)
- `RD2-C3-reg-precondition | П1 | one stop when the gate registry cannot be read (F-T11 residue, R5 (b)) | builder (after C3-0) | controller.validate, controller-blocks.md, state-exits.md, test_controller_state.py | F-T12..F-T15; C3-0 → it; S9 → FL4 → it | ожидает`
- findings, one file each, `id: —`: `holds_over_comments` delete-or-wire (F-T10); probe_verdict accepted in unregistered functions, split needed (R12 a); `selector_contract:417` second reader of `same_command` (R12 b); the critic's review word read outside the registry and three door-text copies (R12 c).
- Batch row RD1-7 still describes C3-d by the (ii) direction (critic R11): the Lead updates it under TEAMWORK §2 (frozen batch).

### B8. §8 readers (rule 7), rows to add
Commands (t-1043):
- Grep (count) over `tools/` for `state-exits|controller-blocks\.md|gate_template`: 3 hits — `controller-blocks-gen.py:1`, `test_controller_blocks_gen.py:1`, `test_test_quarantine.py:863` (a fixture string `design/state-exits.md:34`).
- `controller\.py` over `tools/`: 12 hits in 5 files (`controller-blocks-gen.py` 4, `test_forge_metrics.py` 5, `test_collect_intake.py` 1, `test_controller_blocks_gen.py` 1, `test_dispatch_gate.py` 1).
- Over `.githooks/` with the control `architecture_gate`: 1 hit (the control), so 0 for the names.
- Over `.claude/settings.json` with the control `hygiene_gate`: 1 (the control), so 0.
- Over `.claude/agents/` with the control `designer`: 3, all `designer.md`, so 0.
- `SIBLING_MAP` over `tools/`: 44 hits in 25 files (mechanism_gate.py 7); over `.githooks/`: 0. No positive control was run in that dir for this exact pattern; the earlier combined grep there found `architecture_gate`.

| touched | reader | verdict |
|---|---|---|
| controller.py (C3-reg-precondition) | `tools/controller-blocks-gen.py` (reads raises); `test_forge_metrics.py`, `test_collect_intake.py`, `test_dispatch_gate.py` (name strings) | the generator must place the new `person`-route block (or the row is hand-written, `controller-blocks.md:25-29`); the others unchanged |
| design/controller-blocks.md | `tools/controller-blocks-gen.py`, `tools/test_controller_blocks_gen.py`, package `test_controller_blocks.py` | one row in source order; header counts also move in S9/FL4 if they add blocks (D-0048) |
| design/state-exits.md | package `test_state_exits.py`; `tools/test_test_quarantine.py:863` (fixture string only) | unchanged by an added row |
| test_controller_state.py | `test-layers.json:1082` keep row | unchanged |
| test_run_freshness.py (C3-b2, one row) | `test-layers.json:4702` keep row; imported by test_proof_level.py (its `why`) | unchanged |
| docs/SIBLING_MAP.md (Lead's line) | `tools/mechanism_gate.py` and 24 more tools files | a mechanism path: the Lead commits it with the axis block |

### B9. «Not done / not established (t-1033)», the t-1032 bullet
Append: "(t-1043: superseded — t-1032 is merged and its pins are on main, S-f; D13 is 140 after it and 146 after C3-0, a4aca646.)" Also append to the import-cycle bullet: "(t-1043: closed — `gate_registry.py:97-104` stdlib + `hooklib`, `hooklib.py:2-13` stdlib only; the builder re-checks against the merged C3-0.)"

### B10. Forks returned (t-1043) — new section before the table
None of them reopens F-T1..F-T11. Each card executes on the recommendation.
- **F-T12 — the precondition's route.** (a) person-passable: `_passed_by_person` and the controller-blocks route `person`. The text reports a factory defect and does not ask (FR-3); the waiver is the standing FR-4 road. A pass runs the stage with every converted site refusing reuse, so it is cost, not a false pass. (b) route `command`, no word passes (strict reading of "reported and not asked"). **Rec (a)**: FR-4 ("a person's word passes any block"), P13, builder-rules 8 and AR-9's change check (`architecture.md:111`, "its person's-word route") all demand it. The Lead's "not asked" holds because the text asks nothing. Cost: one line.
- **F-T13 — the driver's routing of the new refusal.** (a) no `KNOWN_REFUSALS` row: it is unmatched and goes to the conductor (FR-48), who reports it. (b) a row `("gate_registry", r"gate registry unreadable", "error")` beside `no_project` (`driver_dispatch.py:106`): it stops with no paid call, but costs a driver_dispatch.py edit, the dry_exits recount (21 -> 22, `tests/dry_exits.py:491,860`) and a driver-layers.json note. **Rec (a)**: a broken install is rare, and a phrase row adds to a table FR-12 is moving out of code (N5).
- **F-T14 — what "stage entry" means.** (a) every `dispatch`, in `validate`'s dispatch branch: the one road all stage starts take (start, rework, relaunch, retry, driver). (b) `prepare` / `_next_action_for_state` (`prepare_stage`): `prepare` is read-only and rework and relaunch bypass it, which would be a second road (P31). (c) also `accept` and `resume`. **Rec (a)**; (c) is not needed, because the sites already err toward not-acceptable (E6).
- **F-T15 — the test layer.** (a) one table in `test_controller_state.py` (keep detector; judged by canon). (b) a `variants.json` row of a recorded story at the walker's `start` door: a better layer, but whether a variant can break a PACKAGE file (not a story file) was not read. **Rec (a)**, executable now; (b) is a scout question if the Lead wants layer 1.

### B11. Fix round t-1043 — where each t-1039 finding went (new section at the end)

| finding | where edited (section, item) | what changed |
|---|---|---|
| R1 | C3-b2 item 4; owns | the existing pins named (test_run_freshness.py:73, K1 (b) :80-86, K1 (f) :104-106, K1 (d) :92-98); one registry row there; owns gains test_run_freshness.py |
| R2 | C3-b2 item 6; E8 | `_evaluate` names the registry; a second row; the `_stale_receipt`/`probe_freshness` `missing` residue named |
| R3 | C3-b2 items 2, 5; owns | probe-record row moved to item 2; `_match` rows return `("", why, _WHY_RANK["bytes"])` for bytes and for the registry; test_execution_request.py gets two rows |
| R4 | C3-b2 item 7 | D13 expected +2 triples (same_test:881, _evaluate:1613), count +2 from base 146; a different measurement stops |
| R5 | C3-b2 item 4, E5; new card C3-reg-precondition; C3-d E3; C3-rr item 5 | "owner factory" dropped; the gap's owner and door stay; the loop is the new node's; node drafted (R5 (b)) |
| R6 | C3-d item 1 | `decides`: `unverified` closes the review only, the instance stays unresolved (D-0013) |
| R7 | C3-d item 6; owns | the pin exists (test_window_record.py:2110-2111, :2117): named, no row |
| R8 | C3-d item 7 | D13 exactly +1 triple build:1532, count +1 |
| R9 | C3-rr item 3; C3-b2 items 4-6; C3-d item 5; owns | the seam is C3-0's `_READ` cache (a4aca646 :31-37), patched and restored in `finally`, or stop; owns name the import lines; the cycle question closed |
| R10 | C3-b2 Measurement; C3-d Measured premise | C3-b2: the run is vacuous, the premise rests on a code trace; C3-d: emulation 6/6 equal, negative control, branch limit |
| R11 | S-f TEMPORAL; C3-rr head, given, item 4, E4; §3; «Not done»; §5 | t-1032 merged; D13 140 -> 146 (C3-0) as base; main line numbers refreshed; batch carriers missing (grep) -> §5 |
| R12 | C3-b2 siblings (a, d); C3-d siblings (a, c, e); C3-rr siblings (b, e) | analogs as waiting findings; axis 26 -> axis 5 :143 with the prose-twin line |
| R13 | C3-b2 E11 | one producer per consumer invariant |
| R14 | C3-b2 owns, non-goals, item 5 | the `same_instance_bytes` docstring sentence (:2069-2072) owned and rewritten |
| R15 | C3-rr item 5; new card E2 | what `registry_problem()` covers (unreadable file) and not (missing consumer/words); the CI backstop |

=====================================================================
## C. Small choices closed (no design weight)
- Test seam = `gate_template._READ` (a private module list): C3-0's own test uses it (:1108-1119 on its branch).
- The new card's raise sits in `validate` (the existing census unit), not in a helper (a new unit).
- The import of `gate_template` in controller.py is at the point of use (the file's late-import style).
- The registry-why wording is one family across sites: "the gate registry cannot be read (<reason>): a factory defect, …".

## D. Conflicts between findings or Lead decisions
None found. R9's "if C3-0 exposes no reset" is settled by `_READ`. R2's residue is now a residue of the R5 (b) node.

## E. Not read (never written as checked)
- `git show a4aca646 --stat` and `git show a4aca646:…` (no shell). The worktree checkout was read instead (branch ref = a4aca646); whether that tree has no uncommitted edits is not established.
- The merge sha 7f2f6f78 (critic's run).
- `test_proof_level.py:1554-1556` (no run_freshness table: the critic's grep).
- The F4 `code` list :729-738.
- `check_delivery.py:860`, `case_stamp.py:317`, `window_record.py:318-319`, `test_window_record.py` helpers.
- `waiver.split_overridden` (whether a pass over a factory block is filed as a finding).
- Whether `test_controller_blocks.py` pins the header counts.
- `controller-blocks-gen.py`'s classifier for a `person` row.
- Whether `test_state_exits.py` is in SLOW_TESTS.
- Whether a controller.py import clears audit A1 for gate_template.
- `tools/mechanism_gate.py`'s prefix list.
- The axis-5 prose twins for test_identity's words (left to the builder).
- `scenario_walk.py --witness-for` output for the new owns.
- No run of `GR.analyse` / `--check` / `--sites` (D13 deltas are the critic's measurement plus C3-0's report).

## F. Reading trail (t-1043)
- review `docs/tasks/specs/reviews/t-1039-rules-debt-c3-redrafts-plan.md` (whole);
- spec :270-409, :529-773, :910-1170, :1458-1707, :1940-2076;
- C3-0 tree: `gate_template.py` (whole), `test_gate_registry.py` (grep of pins; :995-1009, :1095-1143), the C3-0 report (whole), `.git/worktrees/…/HEAD`, `.git/refs/heads/worktree-agent-aa11322709a274e56`;
- main `test_gate_registry.py` :55-70, :328-339, :745-758, :910-997; `gate-registry.json` ids (grep), :122-151, :226-249, :497-524;
- `gate_registry.py` :1-110, :425-469, :829-837; `hooklib.py` imports;
- `gate_preflight.py` imports and :3824-3871 (+ grep); `profile_contract.py` :345-363, :417-418 (grep);
- `proof_level.py` :815-974, :1365-1401, :1462-1463, :1485-1524, :1578-1617 (+ grep :1814, :1886, :1898, :1947, :1972); `execution_request.py` :2062-2113;
- `test_run_freshness.py` :1-125; `test-layers.json` :871-882, :1082-1093, :4702-4710, :5528-5539 (+ grep :7207);
- `acceptance.py` :30-45, :1140-1179 (+ grep :1211); `window_record.py` imports/defs (grep), :28-47, :340-353;
- `agents/qa-code-critic.md` :74-84; `handoffs/vocabulary.yaml` :293-302; `test_window_record.py` :2100-2119;
- `docs/SIBLING_MAP.md` :136-147, :448-456; `phases/s5.md` (grep), :158-187; `code-review-rubric.md` (grep), :90-94;
- `controller.py` defs (grep), :2030-2244, :2470-2483, :5170-5194, :5364-5383, :5488-5547, :8704-8751, :9012-9273, :10050-10083 (+ greps of `self.validate(`, `_passed_by_person(`);
- `design/controller-blocks.md` :1-60 (+ greps); `design/state-exits.md` :1-20, :136-145 (+ heading grep); `test_state_exits.py` :1-131; `test_controller_blocks.py` (grep);
- `judgment-census.json` :1-8 (+ grep :238, :245); `refusal_registry.py` :38-47; `driver_dispatch.py` :30-144; `architecture.md` change-check grep (:111, :155, :166, :180, :261, :282);
- `factory-rules.md` :47-64; `plans/builder-rules.md` (whole); the S9/FL spec :334-337 (+ grep);
- `plans/piles/rules-debt` (Glob + grep with control); `logs/journal/dev1.jsonl` :2642-2649 (grep);
- rule-7 greps as in B8.

## Lead decisions on forks F-T12..F-T15 (17.11.2026, Fable; по рекомендации, до слова владельца — the owner is away)

- F-T12 (a): the precondition's refusal is person-passable (FR-4, P13); its text reports and asks nothing (FR-3).
- F-T13 (a): no `KNOWN_REFUSALS` row; the refusal goes to the conductor.
- F-T14 (a): "stage entry" is every `dispatch`, in `validate`'s dispatch branch.
- F-T15 (a): one table in `test_controller_state.py`.
