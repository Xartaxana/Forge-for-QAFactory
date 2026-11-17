# Rules-debt C3 fix round — three conversion cards from the C3 topic code critic (t-1094, F19; node rules-debt/1/RD1-26)

Designer draft for the Lead. Source: the code critic of the C3 topic, `docs/tasks/specs/reviews/t-1084-c3-b2-d-topic-code.md`
(fixes 1 and 3 (a), 3 (c)), and the three findings in the C3 wave tree
(`plans/piles/rules-debt/findings/20261117-c3-bound-to-priyom-ne-preobrazovan.md`, `...-c3-slova-probe-verdict-vnutri-preobrazovannyh-sajtov.md`,
`...-c3-slovo-obzora-kritika-chitaetsya-vne-reestra.md`). Pattern: cards C3-b2 and C3-d of
`docs/tasks/specs/20261117-rules-debt-phase2-cards-spec.md` (:918-1162) and «Lead decisions on C3-b2 and C3-d at the build» (:2338-2347).

Every line number below was read in the C3 wave tree
`C:/QAFactory/forge-repo/.claude/worktrees/agent-ac40b44fb0a175afa/ai-packages/qa-factory/` (it carries C3-b2, C3-d and C3-reg-precondition;
the main checkout does not). In the cards, `<PKG>` is `C:/QAFactory/forge-repo/ai-packages/qa-factory` — the path the builder works in, on a
branch based on main AFTER the C3 wave lands. The builder re-reads every line number on its own base.

## §0. Facts that change the brief (read before dispatch)

1. **RD1-28: three of the five sites read OTHER producers' words, not `probe_verdict`'s.** The `probe_verdict` row registers only the
   producers `probe_by_code.judge_probe_row` / `_judge_rows` (`gate-registry.json:592-595`). The sites the critic names read:
   - `proof_level._product_receipt_repeat:1422` (`record.get("verdict") == "intended_failure"`) reads the PRODUCT record written by
     `red_sandbox._write_product_records` from `red_sandbox.product_verdict` (`red_sandbox.py:1478-1489`: words `intended_failure`,
     `probe_defect`, `incomplete`, `survived`). No registry row holds that vocabulary (grep `survived|red_sandbox` over
     `gate-registry.json`: only the prose of `probe_verdict.decides` at :591).
   - `proof_level.already_probed:1508` (`behind.get("verdict") == "intended_failure"`) reads either a `probe_by_code` record
     (`receipt["probe_record"]`, :1500-1501) or the product record (`level_of(receipt) == PRODUCT`, :1502-1503).
   - `acceptance.validate_window:1227` (`probe.get("verdict") != "intended_failure"`) reads the window item's `probe` block, written by
     `window_record._receipt_block` (`window_record.py:885`, `"verdict": "intended_failure"`) or `_probe_from_receipt` (:817 `partial_product`,
     :821 `model_changed`; constants :720-721).
   - `proof_level.already_probed:1536` (`in ("no_failure", "wrong_location")`) is the only site that reads `probe_verdict`'s own producer
     alone — and its words are class `mismatched` (`gate-registry.json:600-601`), which `gate_template.acceptable` never accepts
     (`gate_template.py:9-13, 86-94`). So it cannot go through the predicate as the predicate stands.
   - `proof_level.already_probed:1552` (`== "survived"`) reads a word that is in no row.
   The shared word `intended_failure` means the same thing in all three producers (a probe whose broken check fired: `red_sandbox.py:1483-1484`
   "valid"; `window_record.py:834-835` "written ONLY after verify() accepted the probe"). Forks F-4, F-5.
2. **RD1-29: the delivery readers accept a word the window row refuses.** `case_stamp.APPROVING` (:317), `report_facts.APPROVING` (:63)
   and `check_delivery.lifecycle_reasons:860` accept `approved_with_fixes`; `s5_window`'s `words` are `["approved", "unverified"]`
   (`gate-registry.json:254`) and C3-d pins `approved_with_fixes` as a review gap at the window (`test_window_record.py:2854, 2860`). So no
   `s5_window` consumer can take these sites as the row stands. Fork F-6.
3. **RD1-29: two sites refuse MORE when the word approves.** `lifecycle_reasons` processes a test when it is approved OR green (:860), and
   `handoff_check._claim_rollcall` (:966, a reader of `report_facts.APPROVING`) refuses an approving form over a partial roll-call. The
   predicate errs toward False; at these two sites False means FEWER refusals — the unsafe side. Each needs an explicit registry branch
   (card RD1-29 items 4 and 6).
4. **RD1-29: the class is wider than the critic listed.** The same pair is read as a literal at `traceability.py:884`
   (`_review_basis`) and `factory_dashboard.py:887` (display), the full vocabulary at `ledger.py:1191` (membership, not acceptance),
   `rejected` at `window_record._sent_back_lines:2268`; `handoff_check.py:966` reads `report_facts.APPROVING` (the S4 case critic's and the S5
   plan critic's `review.outcome`, the same words: `handoffs/s4-case-critic-to-designer.yaml:66`). Fork F-7.
5. **No shell here.** No count below is measured; every pin is "by measurement at the build" with the command given.
6. **Quarantine.** `test_acceptance_semantics.py`, `test_receipts_per_function.py` (it imports `_bound_to`, :30), `test_check_coverage.py`,
   `test_factory_dashboard_joins.py`, `test_traceability_report.py` are quarantine cohort rows in `test-layers.json` (:7209, :9373, :7567,
   :8271, :10499): no row goes there. Keep files used: `test_proof_level.py` (gate_named, covers `acceptance.py`, `run_history.py`,
   `proof_level.py`: :4124-4137), `test_window_record.py` (:7025), `test_case_stamp.py` (:459), `test_check_delivery.py` (:531),
   `test_report_facts.py` (:4474), `test_gate_registry.py` (:2032).

## §1. Architecture, rules, owners (designer rule 1; package spec)

AR-n touched (texts: `<PKG>/design/architecture.md`; index `docs/ARCHITECTURE_INDEX.md`) and the change check each card's DoD carries:

| AR | card | how kept | change check in the DoD |
|---|---|---|---|
| AR-13 (a fact with a reader is read only through it) | all | every named site reads its word through `gate_template.acceptable` (or, F-5, a registered helper) | `gate_registry.py --check` exit 0, no F-b; `--sites`: no `UNREGISTERED`, no `NOT ALLOWED` |
| AR-15 (one survivor) | 28, 29 | one helper per word reading (`probe_proved`, one static-review note builder) | the callers call the helper (AST row, K-N2.12 form) |
| AR-1 (closed variety is a data row) | 29 | `APPROVING` (two copies) and the literal pair leave code; the accepted words are the row's | grep `APPROVING` over `scripts/*.py`: no binding left (control: `APPROVING_VERDICTS` in `critic_rollcall.py` is found, another vocabulary) |
| AR-22 (every field read has a producer; producer and readers change together) | 29 | `APPROVING` is deleted in the same commit as all its readers (`case_stamp.instance_hold`, `report_facts._tests`, `handoff_check._claim_rollcall`, the twin pin `test_case_stamp.py:211`) | grep `APPROVING\b` over `scripts/` and `scripts/tests/` |
| AR-28 (an unknown never becomes a pass) | all | absent / None / unknown word / unreadable registry -> the safe side per site (tables below), pinned | the unreadable-registry rows |
| AR-29 (code judges data; judgment by a tier above) | all | every check is a membership join of a word to a registry row (data); the critic's verdict stays the critic's | `judgment-census.json` unchanged (`test_judgment_census.py` in the canon) |
| AR-20 (shrink-only ratchets; a raise is named) | all | D13 count/triples and the allow-list pin move by measurement, each move named in a comment | `test_gate_registry.py` (slow: canon) |

Owner and census class of every check the cards add or alter (AR-29, P27): every one serves **data (code)**: it joins a word a producer wrote
to the registry row's `accepts`; none moves a judgment into code. No check adds a refusal unit (no new `raise`/`refuse`/exit; gaps and
reasons are list transport, census header `judgment-census.json:3`), so no census row moves: `validate_window` stays `shape/data` (:7),
`window_record.build` `shape/data` (:1265); the other touched functions have no census row (grep of the census for `_bound_to`,
`green_on_current_bytes_why`, `_job_contract`, `_compare_shas`, `instance_hold`, `lifecycle_reasons`, `_tests`, `already_probed`,
`_product_receipt_repeat`: only the two rows above; the same grep found `validate_window` :7 and `build` :1265 as its control). Census class
of each alteration: `xref` (a join of a recorded word to a data row), as C3-b2 recorded. If `test_judgment_census.py` reads otherwise, the
node stops with a question.

Commit lines: the `architecture:` and `judgment:` lines in the gate's own form — the only carrier of that form is `tools/architecture_gate.py`
(not copied here). Contents per card are given in each card. `judgment: none` always carries its ` -- <why>`.

Rules walked (FR, by section): A (FR-4: a person's pass is untouched), C (FR-13: words in data; FR-38: no role field changes), D (FR-59: the
unknown branch), E (FR-41: a refusal caused by the registry never claims the bytes or the verdict changed), G (FR-32). B: no text a person
reads changes on a readable registry (the pinned texts below stay byte-identical); the new registry sentences follow the existing family
(`proof_level.py:947-948`).

## §2. Cards

### RD1-26 — `test_identity`: `_bound_to` and its axis-25 twins through the predicate (critic t-1084 fix 1)

given:
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/design/factory-rules.md` (whole), `C:/QAFactory/forge-repo/plans/builder-rules.md`, `C:/QAFactory/forge-repo/docs/TESTING.md`
- this card, §0, §1, the C3 shared items S-a..S-f (`docs/tasks/specs/20261117-rules-debt-phase2-cards-spec.md:278-346`) and the C3-b2 card (:918-1025) as the pattern
- read under `<PKG>/`: `scripts/acceptance.py:1-12, 130-216, 1150-1180`; `scripts/run_history.py:138-262, 689-702`; `scripts/proof_level.py:853-930` (`compare_identity`, `same_test`); `scripts/gate_template.py` (whole, 97 lines); `scripts/gate_registry.py:37-53, 772-841`; `references/gate-registry.json:124-166` (row `test_identity`); `scripts/tests/test_proof_level.py:1329-1445, 1794-1865`; `scripts/tests/test_gate_registry.py:256, 305-312, 963-1076`
owns:
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/references/gate-registry.json` (row `test_identity` only: four `sites` entries, four `accepts` consumers)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/acceptance.py` (`_bound_to`, `green_on_current_bytes_why`, and the import line :11)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/run_history.py` (`_job_contract`, `_compare_shas`, their point-of-use imports)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_proof_level.py` (rows in the table `c3_b2_a_reuse_is_accepted_through_the_registry_row_and_an_unknown_runs_again`, items 2-5)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_gate_registry.py` (D13 pins and the allow-list pin, item 6)
non-goals: `same_test`, `compare_identity`; `validate_window` (the C3-d review branch and the RD1-28 probe line); `_make_pair`'s `verdict == "same"` (:701: `run_history`'s own pair word `same|changed|unknown`, produced by `_compare_shas`, not a `test_identity` word read from `compare_identity`); `run_freshness_of`; `judgment-census.json`; `docs/SIBLING_MAP.md` (axis 25 text, the Lead's at acceptance, item 7); the registry-why family builder (critic fix 2, its own node)
handoff: report path given by the Lead
edges: E1-E10 below
DoD: `python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/gate_registry.py --check` (exit 0; no F-b; `test_identity` stays converted) and `python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for C:/QAFactory/forge-repo/ai-packages/qa-factory/references/gate-registry.json C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/acceptance.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/run_history.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_proof_level.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_gate_registry.py` and the printed non-slow files; `test_proof_level.py` and `test_gate_registry.py` are slow (spec §0.3): batch canon, named in the report
siblings: axis 7 (`docs/SIBLING_MAP.md:194`, "Recorded-carrier readers": `_bound_to` named); axis 25 (:451: `green_on_current_bytes_why`, `run_history.SHA_FIELDS` "queued (batch 3 ...)" — after this card that sentence is stale, item 7); axis 5 (gate rows <-> sites <-> prose twins: grep `same_test|compare_identity|green_on_current_bytes` over `references/execution-lifecycle.md`, `references/slices/qa-automator/execution-lifecycle.md`, `skills/qa-story/phases/s5.md`, each hit a report line "checked, no edit (meaning unchanged)"); axis 34: no language, project or case key is read
designer: `C:/QAFactory/forge-repo/docs/tasks/specs/20261117-rules-debt-c3-fix-conversions-cards.md` (RD1-26)

Sites (verified by reading, C3 wave tree):

| # | file:function (lines) | current expression | after |
|---|---|---|---|
| S1 | `acceptance.py:_bound_to` (:204-216) | `if proof_level.same_test(proof_level.proof_identity(item), proof_level.proof_identity(proof)):` (:211) | `if acceptable(proof_level.same_test(...same arguments...), "test_identity.proof_bound"):` |
| S2 | `acceptance.py:green_on_current_bytes_why` (:130-185) | `if proof_level.same_test({"input_hash": item.get("input_hash")}, {"input_hash": raw}) != "raw":` (:177) | `if not acceptable(proof_level.same_test(...same arguments...), "test_identity.mechanical_raw"):` + the registry why (item 3) |
| S3 | `run_history.py:_job_contract` (:203-223) | `if all(PL.compare_identity(found[0], c) == ("same", "content") for c in found[1:]): return found[0]` (:221) | the loop of item 4 |
| S4 | `run_history.py:_compare_shas` (:248-262) | `verdict, _ = PL.compare_identity(*pair)` (:256); `if verdict != "unknown":` (:257); `return ("same" if verdict == "same" else "changed"), basis, ...` (:259) | item 5 |

Items:
1. **Registry** (row `test_identity`). Add to `sites`: `{"file": "acceptance.py", "function": "_bound_to", "role": "accept"}`,
   `{"file": "acceptance.py", "function": "green_on_current_bytes_why", "role": "accept"}`, `{"file": "run_history.py", "function":
   "_job_contract", "role": "accept"}`, `{"file": "run_history.py", "function": "_compare_shas", "role": "accept", "allow": [...]}` (the
   `allow` entries are the measured state returns of item 5). Add to `accepts`: `"test_identity.proof_bound": ["matched"]` (S1),
   `"test_identity.mechanical_raw": ["matched"]` (S2), `"test_identity.param_twin": ["matched"]` (S3), `"test_identity.pair_same":
   ["matched"]` (S4). `words`, `verdict_map`, `decides`, status unchanged. Each consumer is fed by ONE producer (C3-b2 E11): `proof_bound`,
   `mechanical_raw` <- `same_test`; `param_twin`, `pair_same` <- `compare_identity`. The four functions are registered by no other row
   (grep of `gate-registry.json` for `acceptance.py`: only `validate_window` :249; for `run_history`: no hit), so A26 F-f cannot fire.
2. **S1 `_bound_to`.** The truthiness at :211 becomes the predicate (import `acceptable` is already at :11). The mechanical-round branch
   (:213-216) is unchanged: `bound == record["reviewed_input_hash"]` compares a recorded value with its copy (docstring :209-210), not a word.
   Rows (test_proof_level table): (i) a review whose `proof_identity` matches the item's -> True; (ii) other bytes, no mechanical round ->
   False; (iii) matching identity, registry unreadable (the table's `unreadable_registry()` seam, :1804-1811) -> False. Expected from the row's
   `decides` (`gate-registry.json:126`) and `_bound_to`'s docstring (:205-208), never from its output before the change.
3. **S2 `green_on_current_bytes_why`.** The comparison at :177 becomes `not acceptable(...)`. On refusal: when
   `gate_template.registry_problem()` (import at the point of use, the file's late-import style is not needed: add `registry_problem` to the
   :11 import) is non-empty, the reason appended is `f"job {attempt}: the gate registry cannot be read ({problem}): a factory defect, the
   run's bytes were not judged"`; otherwise the existing sentence (:178-179) byte for byte. Rows: a run block + job + item + window written
   into the table's temp dir in the shapes the docstring names (:134-143; block `{input_fingerprint F, dispatch_id A, attempt_id J,
   block_id B, results [{instance_id I, status passed}]}` under `work/run-blocks/`, job `{job_id J, request {fingerprint_files [{kind
   test_files, path P, sha256 R}]}}` under `state/execution-jobs/`, no manifest so the one test file decides, item `{outcome passed,
   execution_fingerprint F, instance_id I, input_hash H}`, window `{mechanical_round {author_dispatch_id A, reviewer_dispatch_id X,
   reviewed_input_hash Y}}`): (i) H == R -> `(True, "")`; (ii) H != R -> False, the why holds `ran the test file as sha256 R`; (iii) H == R,
   registry unreadable -> False, the why holds `the gate registry cannot be read`, `check_not_in` `ran the test file as sha256`. Before
   writing these, the builder greps `green_on_current_bytes|mechanical_round` in the KEEP test files; an existing table that builds this
   world takes the rows instead (named in the report).
4. **S3 `_job_contract`.** :221-223 become:
   `for c in found[1:]: verdict, basis = PL.compare_identity(found[0], c); if not (acceptable(verdict, "test_identity.param_twin") and basis == "content"): return {}` then `return found[0]`
   (`from gate_template import acceptable` next to `import proof_level as PL` at :220). Equivalence: `compare_identity` returns `same` as its
   only matched word (`proof_level.py:879-885`), so `acceptable(verdict) and basis == "content"` is True exactly when the old tuple equality
   was; `basis` is not a row word, so `basis == "content"` is not counted. Rows: two contracts under one bare function name with
   (i) equal code and content shas -> `found[0]`; (ii) equal code, different content (`("same", "code")`) -> `{}`; (iii) no shas
   (`unknown`) -> `{}`; (iv) case (i) with the registry unreadable -> `{}`. Expected from the comment :215-219 ("the sha of a stranger never
   decides 'the same'"; "any other answer, unknown included, is no match").
5. **S4 `_compare_shas`.** :259 becomes `return ("same" if acceptable(verdict, "test_identity.pair_same") else "changed"), basis, red[basis],
   green[basis]`, guarded per fork F-2 (recommended (a)): when `verdict == "same"` is not acceptable AND `registry_problem()` is non-empty,
   the identity basis is skipped as if `unknown` (fall to the file basis :260-261, then :262). `verdict != "unknown"` (:257) and every
   other comparison the scan counts in this function after the change get an `allow` entry each, the WHOLE text in `ast.unparse` form, why
   "routes an unknown identity to the coarser file basis, not an acceptance" (:257) or "a state the function returns to its caller, not an
   acceptance of an identity word" (the returns; the Lead decision (A) precedent, phase-2 spec :2340-2343). Which texts are counted is BY
   MEASUREMENT (`gate_registry.py --sites` before and after; the bare tuple `"unknown", "unknown", ...` at :262 is expected to count once
   `_compare_shas` is a site, because `unknown` is a row word). A counted comparison that is an acceptance and not a return or the routing
   test is a stop and a question. Rows: (i) code shas equal on both -> `("same", "code", ...)`; (ii) different -> `("changed", ...)`;
   (iii) no identity, file shas equal -> `("same", "file", ...)`; (iv) nothing -> `("unknown", "unknown", ...)`; (v) code shas equal,
   registry unreadable, file shas present and equal -> `("same", "file", ...)`; (vi) as (v) with no file shas -> `("unknown", "unknown", ...)`.
   Expected from the docstring (:249-253: "unknown is never same") and FR-59.
6. **Pins (S-f, deltas from the base).** No row changes status: `EXPECTED_DEBT`, `EXPECTED_CONVERTED`, K-T1.2 (:256), the split (:354-355)
   and the F4 list do not move. D13: re-measure `GR.analyse(PLUGIN_ROOT)` before and after (command in §3); expected triples added:
   `("run_history.py", "_compare_shas", "test_identity")` (its allowed returns/routing); `_bound_to`, `green_on_current_bytes_why`,
   `_job_contract` are expected to hold no counted comparison after the change. `D13_ITEM_COUNT` moves by the measured number, with a comment
   line in the form of :1065-1068 naming each added item. The allow-list pin (:305-312) gains the new entries in registry order, by
   measurement. A different measurement from the expectation is named in the report with its cause (not a stop when every new item is an
   allowed return/routing test; a stop otherwise).
7. **Lead at acceptance (not the builder):** SIBLING_MAP axis 25 (:451) — the sentence "queued (batch 3, finding AR-13/AR-22 remainder)"
   for `green_on_current_bytes_why` and `run_history` is replaced by "read through `gate_template.acceptable` (RD1-26)"; axis 7 (:194) adds
   "through the predicate" to `_bound_to`. A mechanism path: the builder reports it under "Needed from integration".

architecture content: `AR-13 -- every test_identity word these four sites consume is read through gate_template.acceptable`;
`AR-28 -- a non-match, an absent identity or an unreadable registry is no match (run again, stale review, no stranger's shas, no "same")`;
`AR-29 -- xref, owner data, no census unit`; `AR-20 -- D13 and the allow-list pin re-measured, each move named`; judgment
`none -- the reuse decision is a join of a computed identity word to the registry row`.

Edges (each with its invariant):
- E1 POSITIONAL (S1): the predicate replaces only the truthiness at :211; the mechanical-round branch follows unchanged. INVARIANT: a review
  or probe of other bytes never speaks for the test, except through a recorded mechanical round whose author ran green on the current bytes.
- E2 (S2, error direction of a reused function in a gate role): `same_test` is called with dicts that carry only `input_hash`, so it
  can return only `raw` or `""` (`proof_level.py:914-930`: rule 1 needs `instance_identity` on both sides, rule 1b needs one side, rule 3
  needs `test_code_sha`; `_kept(None)` empty — the builder confirms by reading `_kept`, :821). A `["matched"]` consumer is therefore True
  exactly when `== "raw"` was. Permitted error: toward False (a stale review, one more critic round). Adversarial inputs that must stay
  on the safe side: H empty -> `""` -> False; H a non-str (int) -> `str()` on both sides as today; R empty never reaches (`_raw_record` returns
  a `missing` first, :114-115); a future edit that passes an identity-bearing dict would let `instance`/`file_code` through — pinned by
  keeping the call's two literal dict shapes (the report quotes them) and by row (ii). INVARIANT: a mechanical round closes only on the raw
  bytes the reviewer saw (comment :175-176).
- E3 (S3): `found[1:]` empty -> the loop does nothing -> `found[0]` (as `all([])`); contracts that are not dicts never reach (:212).
  INVARIANT: a stranger's sha never decides "the same" (:217).
- E4 (S4, F-2): unreadable registry -> the identity's "same" is never reported; the file basis may still say "same" on equal block
  fingerprints (another quantity, stronger: test + helpers). INVARIANT: no red/green pair is dropped on an identity "same" the predicate did
  not accept; an unknown is never `same` (FR-41).
- E5 (unreadable registry, all sites): S1 False, S2 False with the registry why, S3 `{}`, S4 per E4. Behind C3-reg-precondition (no new
  dispatch on an unreadable registry) these are belt-and-braces inside a stage that began before. INVARIANT: a broken registry never lets an
  old review, probe, contract or run speak for the test.
- E6 (absent / None word): `same_test` and `compare_identity` never return None; `acceptable(None)` and `acceptable("")` are False (C3-0
  table rows `empty-word`, `other-shape-*`, `test_gate_registry.py:1124-1128`). INVARIANT: no word, no reuse.
- E7 TEMPORAL: windows and run blocks recorded before are judged at their next read exactly as today on a readable registry (the trace of
  E2/E3 and the C3-b2 trace "every same_test word is class matched", `gate-registry.json:146-150`). INVARIANT: no recorded verdict changes
  meaning after the fact.
- E8 TEXT: the existing whys stay byte-identical on a readable registry (`acceptance.py:146-151, 161, 168-169, 173, 178-179, 183-184`);
  the new registry why never says "ran the test file as sha256". INVARIANT: FR-41.
- E9 (K-C census, `test_proof_level.py:1439-1445`): `_compare_shas` and `green_on_current_bytes_why` must still call `compare_identity` /
  `same_test` as an attribute call (`PL.`, `proof_level.`); the pin stays green unedited.
- E10 (limit): none introduced.

### RD1-28 — the probe word readers out of the `test_identity` / `s5_window` sites (critic t-1084 fix 3 (a))

given:
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/design/factory-rules.md` (whole), `C:/QAFactory/forge-repo/plans/builder-rules.md`, `C:/QAFactory/forge-repo/docs/TESTING.md`
- this card, §0 fact 1, §1, S-a..S-f and C3-b2 (pattern)
- read under `<PKG>/`: `scripts/proof_level.py:1099-1170` (`tooling_gap_key`, `probe_record_state`: noticed readers, non-goals), `:1409-1579`; `scripts/acceptance.py:1219-1234`; `scripts/red_sandbox.py:1478-1508`; `scripts/window_record.py:720-721, 803-890`; `references/gate-registry.json:589-612` (row `probe_verdict`); `scripts/gate_template.py`; `scripts/gate_registry.py:37-53, 772-841`; `scripts/tests/test_proof_level.py:1794-1865`; `scripts/tests/test_window_record.py:2821-2869`; `scripts/tests/test_probe_by_code.py:2600-2616`; `scripts/tests/test_red_sandbox_probe.py:480-532`; `scripts/tests/test_gate_registry.py:963-1076`
owns:
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/references/gate-registry.json` (row `probe_verdict` only: `decides` (one clause, item 1), `sites` +2, `accepts` +1)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/proof_level.py` (new `probe_proved`, new `_probe_record_defect`; `already_probed` :1508 and :1536; `_product_receipt_repeat` :1422)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/acceptance.py` (`validate_window`: the one probe line :1227 only)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_proof_level.py` (rows in the C3-b2 table, item 4)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_window_record.py` (rows, item 5)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_gate_registry.py` (D13 pins, item 6)
non-goals: `already_probed:1552` (`survived`: a word of no row — §0 fact 1; residual node RD1-28b, fork F-4); `red_sandbox.py`, `window_record.py` code (their vocabularies get no row here, F-4); `probe_by_code.py` readers the row's `decides` names as "not sites yet" (`keep_standing_record`, `publish_binding`, `main`); `tooling_gap_key:1105` and `probe_record_state:1149-1155` (state readers of the same words — noticed analogs, reported); the review branch of `validate_window` (C3-d); `_bound_to` (RD1-26); census
handoff: report path given by the Lead
edges: E1-E9 below
DoD: `python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/gate_registry.py --check` (exit 0; no F-b; no F-f "registered more than once") and `python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for C:/QAFactory/forge-repo/ai-packages/qa-factory/references/gate-registry.json C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/proof_level.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/acceptance.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_proof_level.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_window_record.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_gate_registry.py` and the printed non-slow files; the three test files are slow: canon
siblings: axis 5 (prose twins of `intended_failure` as a reuse word: grep `intended_failure` over `references/execution-lifecycle.md`, `skills/qa-story/phases/s5.md`, `references/code-review-rubric.md`, each hit "checked, no edit"); axis 7 (the probe record readers); axis 34: one helper for every caller, no language key
designer: `C:/QAFactory/forge-repo/docs/tasks/specs/20261117-rules-debt-c3-fix-conversions-cards.md` (RD1-28)

Sites (verified by reading):

| # | site | current | producer of the word read | after (recommendation F-4 (a), F-5 (a)) |
|---|---|---|---|---|
| P1 | `proof_level.already_probed:1508` | `behind.get("verdict") == "intended_failure"` | `probe_by_code` record or `red_sandbox` product record | `probe_proved(behind)` |
| P2 | `proof_level.already_probed:1536` | `record.get("verdict") in ("no_failure", "wrong_location")` | `probe_by_code` record | `_probe_record_defect(record)` |
| P3 | `proof_level._product_receipt_repeat:1422` | `record.get("verdict") == "intended_failure"` | `red_sandbox` product record | `probe_proved(record)` |
| P4 | `acceptance.validate_window:1227` | `probe.get("verdict") != "intended_failure"` | `window_record._receipt_block` / `_probe_from_receipt` | `not proof_level.probe_proved(probe)` |
| — | `proof_level.already_probed:1552` | `record.get("verdict") == "survived"` | `red_sandbox` product record | unchanged (no row holds `survived`; RD1-28b) |

Items:
1. **Registry** (row `probe_verdict`). Add `sites`: `{"file": "proof_level.py", "function": "probe_proved", "role": "accept"}` and
   `{"file": "proof_level.py", "function": "_probe_record_defect", "role": "validate"}`; `accepts`: `"probe_verdict.proved": ["matched"]`.
   `decides` gains one clause, appended: "The word `intended_failure` is read with the same meaning from the product record
   (`red_sandbox.product_verdict`) and the window's probe block (`window_record._receipt_block`); `proof_level.probe_proved` is its one
   reader. A record that judged the test defective (`no_failure`, `wrong_location`) answers a repeated probe through
   `proof_level._probe_record_defect` (a `validate` site: the predicate takes no `mismatched` word, and a wrongly answered repeat only refuses
   a probe, never passes a test)." `words`, `verdict_map`, status unchanged. Both new function names are defined once in `proof_level.py`
   (F-e; the builder greps `def probe_proved|def _probe_record_defect` first).
2. **`probe_proved(record) -> bool`** (public, new, next to `_read_record`): `return acceptable(record, "probe_verdict.proved")` — the row's
   `field` is `verdict` (`gate-registry.json:596`), so a dict is read at `record["verdict"]` by the predicate (`gate_template.py:75-80`); a
   non-dict non-str value is False. P1 and P3 call it in place of the literal; P4 calls `proof_level.probe_proved(probe)` (`proof_level` is
   imported at `acceptance.py:10`). `already_probed` and `_product_receipt_repeat` stay `test_identity` accept sites; after the change they hold
   no `probe_verdict` literal, so the class "a word of one row accepted in a function another row owns" (the finding) is closed for P1-P4.
3. **`_probe_record_defect(record) -> bool`** (new): `return isinstance(record, dict) and record.get("verdict") in ("no_failure",
   "wrong_location")` — the literal moves here from P2 whole; P2 calls it. Registered `validate` (fork F-5): A26 now counts the literal and
   attributes it to `probe_verdict` (today it is invisible: `already_probed` is a `test_identity` site and the words are not anchors).
4. **Rows in the C3-b2 table of `test_proof_level.py`** (the table's `unreadable_registry()` seam):
   - `probe_proved`: `{"verdict": "intended_failure"}` -> True; each of `no_failure`, `wrong_location`, `not_executed`, `incomplete`,
     `survived`, `probe_defect`, `partial_product`, `model_changed`, `""`, `"Intended_failure"`, `" intended_failure"`, `None` as the verdict,
     no `verdict` key, `[]`, `None` as the record -> False; `intended_failure` with the registry unreadable -> False. Expected from the row's
     `verdict_map` (:598-603) and FR-59.
   - `_probe_record_defect`: `no_failure`, `wrong_location` -> True; `intended_failure`, `not_executed`, `incomplete`, `""`, no key, `None`
     record -> False. Expected from the docstring of `already_probed` item 2 (:1460-1461).
   - Behaviour of the callers: already pinned, NAMED in the report, no new row — `test_proof_level.py:1820-1849` (item 2/3 rows: `no_failure`
     and product `intended_failure`, same/other bytes, unreadable), `test_probe_by_code.py:2606-2615` and `test_red_sandbox_probe.py:500-508`
     (a `survived` product record answers the repeat). Their expected values do not move.
5. **Row(s) in `test_window_record.py`** for P4: the builder greps `"sensitivity:` in the file first and adds rows to the existing table that
   pins the `sensitivity:<iid>` gap; with none, one parameterised function in this file (no new file). Rows: an item that ran green, owes a
   live check, whose probe block matches on every other field (location, reason, `failure_kind: assertion`, bound to the bytes) with verdict
   `intended_failure` -> no `sensitivity:` gap; `partial_product`, `model_changed`, `incomplete`, `""`, no `verdict` -> `sensitivity:<iid>`;
   `intended_failure` with the registry unreadable -> `sensitivity:<iid>`. Expected from `validate_window`'s probe rule (:1223-1234) and
   FR-59.
6. **Pins (S-f).** No status moves. D13 re-measured before and after: expected +1 triple `("proof_level.py", "_probe_record_defect",
   "probe_verdict")` and +1 item (the moved `in (...)` comparison; it was not counted before). `probe_proved` holds no literal. By
   measurement; the comment line names the item.

architecture content: `AR-13 -- the intended_failure reuse/close word is read only through proof_level.probe_proved (gate_template.acceptable)`;
`AR-15 -- one helper for the four readers`; `AR-28 -- an absent, unknown or other word, or an unreadable registry, never answers a repeat or
closes a probe`; `AR-29 -- xref, owner data, no census unit`; `AR-20 -- D13 +1/+1 measured and named`; judgment `none -- a join of a recorded
probe word to the registry row; the probe's verdict stays the probe judge's`.

Edges:
- E1 POSITIONAL (P1): `probe_proved(behind)` sits where the literal was, inside the `own = (...)` expression, with the receipt-path conditions
  after it unchanged. INVARIANT: a record that is not the receipt's own proved probe never vouches for what the receipt mutated.
- E2 POSITIONAL (P3): first conjunct as today, before the identity predicate and `_mutated_files_hold`. INVARIANT (C3-b2 E2): a record
  that does not say `intended_failure` is never asked about identity.
- E3 POSITIONAL (P4): the first disjunct of the `sensitivity:` condition, before `_bound_to`. INVARIANT: a probe block that does not say
  `intended_failure` is a `sensitivity:` gap whatever its other fields say.
- E4 (error direction of the reused predicate in three producers' service, F-4 (a)): `acceptable` errs toward False. A product-record or
  window word outside the row's `words` (`survived`, `probe_defect`, `partial_product`, `model_changed`) -> False, exactly as `!=
  "intended_failure"` today. Adversarial inputs pinned in item 4. INVARIANT: only `intended_failure`, exact case, from a dict's `verdict`,
  on a readable registry, is a proved probe.
- E5 (P2, F-5): the literal is unchanged in meaning and position (first conjunct, then the identity predicate). Permitted error of a wrong
  `True`: a repeated probe is refused with the prior defect verdict shown (the person's word passes it, :1575-1578) — never a pass.
  INVARIANT: a `no_failure` / `wrong_location` record answers a repeat only over the same test bytes.
- E6 (unreadable registry): P1 -> `own = None` (the receipt's own record is not trusted; a receipt with no carried mutated file does not
  block, :1513-1515: the probe runs); P3 -> None (the probe runs); P4 -> `sensitivity:`; P2 unaffected (no predicate). Behind
  C3-reg-precondition. INVARIANT: a broken registry never answers a repeat by a proved probe and never closes a window's probe.
- E7 (absent / None): a record with no `verdict`, a `None` record (`_read_record` returns None for an unreadable file, :1263) -> False at
  P1, P3, P4 (P1/P3 already test `is not None` first). INVARIANT: no word, no proof.
- E8 TEMPORAL: records written before are read exactly as today on a readable registry (word-for-word equivalence, E4). INVARIANT: no
  recorded verdict changes meaning.
- E9 TEXT: no text changes (`prior_verdict` values :1444, :1522, :1544, :1557, `_repeat_words`, the `sensitivity:` gap line). Limit: none.

### RD1-29 — the critic's review word outside the window, and one builder of the static-review note (critic t-1084 fix 3 (c))

**Plan critic before the builder** (PROJECT.md «Как принимается изменение пакета» item 6): under either option of F-6 a gate row's
`decides` changes meaning (a row starts to cover the stamp, gate B, the report and a form check). The card is executable by the
recommendations F-6 (b), F-7 (a), F-8 (a).

given:
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/design/factory-rules.md` (whole), `C:/QAFactory/forge-repo/plans/builder-rules.md`, `C:/QAFactory/forge-repo/docs/TESTING.md`
- this card, §0 facts 2-4, §1, S-a..S-f and C3-d (pattern, phase-2 spec :1029-1162)
- read under `<PKG>/`: `references/gate-registry.json:245-270` (row `s5_window`); `scripts/case_stamp.py:315-344`; `scripts/report_facts.py:63, 1507-1550`; `scripts/check_delivery.py:829-880`; `scripts/handoff_check.py:949-975`; `scripts/window_record.py:305-330, 435-446, 1637-1652, 1732-1751, 1937-1995`; `scripts/acceptance.py:1150-1176` (the review branch the notes mirror); `scripts/contract.py:2209-2215` (`CRITIC_VERDICTS`); `handoffs/s4-case-critic-to-designer.yaml:60-70`; `scripts/gate_template.py`; `scripts/tests/test_case_stamp.py:160-215`; `scripts/tests/test_check_delivery.py:1100-1115, 1760-1775`; `scripts/tests/test_report_facts.py:400-420`; `scripts/tests/test_window_record.py:2821-2869`; `scripts/tests/test_gate_registry.py:256, 305-312, 963-1076`
owns:
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/references/gate-registry.json` (row `s5_window` only: `decides`, `words`, `verdict_map`, `accepts`, `sites`)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/case_stamp.py` (`APPROVING` deleted, its comment :315-316; `instance_hold` :344 and its docstring line :332; the import)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/report_facts.py` (`APPROVING` :63 deleted; `_tests` :1536; the import)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/check_delivery.py` (`lifecycle_reasons` :858-861 and one registry reason; the import)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/handoff_check.py` (`_claim_rollcall` :965-969; the import)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/window_record.py` (`build`: the two static-review notes :1641-1648, :1742-1751 and the generic note condition :1649; one new helper `_static_review_note`; `GAP_ORIGIN["review"]` text unchanged)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_case_stamp.py` (rows of the table :166-178; the twin pin :211 replaced, item 7)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_check_delivery.py` (rows, item 7)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_report_facts.py` (rows, item 7)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_window_record.py` (rows, item 7)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_gate_registry.py` (D13 pins, item 8)
non-goals: `acceptance.validate_window` (C3-d's; its three consumers and their tokens are unchanged); `traceability._review_basis:884`, `factory_dashboard:887`, `ledger:1191`, `window_record._sent_back_lines:2268` (RD1-29b, F-7); `critic_rollcall.APPROVING_VERDICTS` and its readers (`controller.py:3547`, `driver_stage_plan.py:819`: the S4 roll-call vocabulary `approve*`, another vocabulary); `validate_artifacts.py:2199, 2203` (the `fix_notes` shape rule: validation, not acceptance); `GAP_ORIGIN` and `ORIGIN` texts; `case_stamp.HOLDS` words; census
handoff: report path given by the Lead
edges: E1-E11 below
DoD: `python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/gate_registry.py --check` (exit 0; no F-b; `s5_window` converted) and `python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for C:/QAFactory/forge-repo/ai-packages/qa-factory/references/gate-registry.json C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/case_stamp.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/report_facts.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/check_delivery.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/handoff_check.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/window_record.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_case_stamp.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_check_delivery.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_report_facts.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_window_record.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_gate_registry.py` and the printed non-slow files; slow files: canon
siblings: axis 5 (prose twins of "approved or approved_with_fixes approves": grep `approved_with_fixes` over `references/code-review-rubric.md`, `skills/qa-story/phases/s5.md`, `s8.md`, `handoffs/s5-critic-to-automator.yaml`, each hit "checked, no edit"); axis 34 (one row and one predicate for the critic's word, every stage alike); the residual siblings: RD1-29b (F-7)
designer: `C:/QAFactory/forge-repo/docs/tasks/specs/20261117-rules-debt-c3-fix-conversions-cards.md` (RD1-29)

Sites (verified by reading):

| # | site | current | after (F-6 (b)) |
|---|---|---|---|
| W1 | `case_stamp.instance_hold:344` | `"" if entry.get("critic_verdict") in APPROVING else NOT_APPROVED` | `"" if acceptable(entry.get("critic_verdict"), "s5_window.stamp") else NOT_APPROVED` |
| W2 | `report_facts._tests:1536` | `verdict not in APPROVING` | `not acceptable(verdict, "s5_window.proven")` |
| W3 | `check_delivery.lifecycle_reasons:860` | `if verdict not in ("approved", "approved_with_fixes") and not green: continue` | item 4 |
| W4 | `handoff_check._claim_rollcall:966` | `if outcome in report_facts.APPROVING and found["verdict_ceiling"] == "partial":` | item 6 |
| W5 | `window_record.build:1641`, `:1742` | `!= BLOCKED_REVIEW_VERDICT` (imported name, invisible to A26) + two near-identical f-string notes | item 5 |
| W6 | `window_record.build:1649` | `elif item["review"]["verdict"] != "approved":` | item 5 |

Items:
1. **Registry, row `s5_window`** (F-6 (b)): `words` -> `["approved", "approved_with_fixes", "unverified"]`; `verdict_map` gains
   `"approved_with_fixes": {"class": "not_applicable", "reason_code": "with_fixes"}`; the three window consumers are unchanged, so
   `approved_with_fixes` stays a review gap at the window (`s5_window.review` / `handed_review` list no `not_applicable:with_fixes`).
   `accepts` gains `"s5_window.stamp"`, `"s5_window.proven"`, `"s5_window.lifecycle"`, `"s5_window.form_outcome"`, each
   `["matched", "not_applicable:with_fixes"]` (one consumer per site, as the finding asks). `sites` gains `case_stamp.py:instance_hold`,
   `report_facts.py:_tests`, `check_delivery.py:lifecycle_reasons`, `handoff_check.py:_claim_rollcall`, each `accept` (none is registered by
   another row: grep of the registry for these names, no hit). `decides` gains one sentence: "Outside the window the same word approves a
   test for the stamp, gate B's lifecycle, the report's proven count and a critic form's outcome: `approved` or `approved_with_fixes`
   (class `not_applicable:with_fixes`, so the window's consumers never take it); a site where an approving word triggers a further check
   names an unreadable registry instead of reading it as not approving." `rejected` stays outside `words` (compared nowhere after this card;
   refused by being outside, as C3-d decided). expected from: `contract.py:2209-2215`, `case_stamp.py:315-316` ("`approved_with_fixes` is a
   legal verdict"), C3-d item 3.
2. **W1, W2.** As in the table (`from gate_template import acceptable` at the point of use or at the import block, the file's style).
   `APPROVING` is deleted from both modules with its comment; `case_stamp.instance_hold`'s docstring line `not_approved the critic's verdict
   is not in APPROVING` (:332) reads "is not one the registry row `s5_window` approves for the stamp".
3. **W3** `lifecycle_reasons`: `approving = acceptable(verdict, "s5_window.lifecycle")`; `if not approving and not green: continue`. Before
   the loop: `problem = registry_problem()`; when non-empty, `reasons` gets ONE line and the loop is not entered: "the gate registry cannot be
   read (<problem>): a factory defect - whether each approved test owes its case's Automated stamp was not checked". This is the function's
   own precedent for "the join could not be built" (`not_read`, :851-854, "ONE reason says so (FR-59) instead of guessing"). The reason's
   owner/class is the one `lifecycle_reasons`' other lines carry (the builder reads how `check_delivery` routes these lines; a reason that
   would be classified as the story's fault is a stop and a question, FR-46).
4. *(numbering kept for the edges: W3 is item 3, W4 item 6, W5/W6 item 5)*
5. **W5, W6 (window notes).** One helper `_static_review_note(said: str, why: str) -> str` returns exactly the text :1644-1648 builds with
   `why` = `"this instance was blocked by the stand"` and the text :1747-1751 with `why` = `"this instance's probe could not run here (a
   person's word or the factory names it)"` — both BYTE-IDENTICAL to today (the builder diffs the two outputs over `said in ("approved", "")`
   before/after). The conditions mirror `validate_window`'s consumers per kind (F-8 (a)): stopped -> `not acceptable(said,
   "s5_window.static_review")`; probe-gapped -> the same; otherwise -> `not acceptable(said, "s5_window.handed_review")` for an instance in
   `handed_ok`, else `not acceptable(said, "s5_window.review")` (replaces :1649). `GAP_ORIGIN["review"]` (:324-328) is not touched. INVARIANT:
   for every instance, `build` writes a `review` note exactly when `validate_window` raises `review:<iid>` — one predicate, one consumer per
   kind.
6. **W4** `_claim_rollcall`: `problem = registry_problem()`; when non-empty -> `return (None, f"the gate registry cannot be read ({problem}):
   whether the form's outcome approves was not judged")` (the function's documented direction: what it cannot measure is `None`, :949-951);
   else the condition reads `acceptable(outcome, "s5_window.form_outcome") and found["verdict_ceiling"] == "partial"`. Placement: after
   `found is None` (:963-964), before the condition. `import report_facts` (:958) stays only if another use remains (the builder greps).
7. **Tests** (rows, never a new file):
   - `test_case_stamp.py` table :166-178 (`instance_hold`): + `unverified`, `rejected`, `""`, `"Approved"`, `None`, no key -> `not_approved`;
     `approved` with the registry unreadable (`gate_template._READ` swapped, restored in `finally`) -> `not_approved`. The existing
     `approved_with_fixes` row (:178) stays. The twin pin :211 (`S.APPROVING == RF.APPROVING`) is replaced by one row: for every word of
     `contract.CRITIC_VERDICTS` plus `""`, `acceptable(w, "s5_window.stamp") == acceptable(w, "s5_window.proven")` (the stamp and the report
     cannot disagree: the drift the pin guarded, now held by data).
   - `test_check_delivery.py` (the A-K5 rows :1105-1114): + `rejected`, not green -> no lifecycle reason; registry unreadable -> exactly one
     reason, naming the registry, and no per-case reason.
   - `test_report_facts.py` (:407-418): + an `unverified` and a `rejected` green row -> not counted as proven; the existing
     `approved_with_fixes` row stays counted.
   - `test_window_record.py`: in `c3_d_review_word_through_the_registry` (:2821), a second check per row: the `review` note of
     `window_record.build` is present iff the row's expected gap is True (same rows, same seams; the builder reads how `build` is driven in
     the file's other build tests). If `build` cannot be driven inside that table's world, rows go to the existing build-note table the
     builder finds by grepping `"review"` notes; none -> a stop and a question.
   - handoff_check: the builder greps `_claim_rollcall|the ceiling is partial` under `scripts/tests/`; rows go into that KEEP table:
     `approved`/`approved_with_fixes` + partial -> False; `rejected` + partial -> not this refusal; registry unreadable -> `(None, ...)` naming
     the registry. A table only in a quarantined file -> stop and question (no new file).
   Expected from: `decides` (item 1), `contract.py:2209-2215`, FR-59, the functions' documented error directions — never from outputs before
   the change.
8. **Pins (S-f).** No status moves. D13 re-measured: expected `("window_record.py", "build", "s5_window")` LEAVES (its one counted
   comparison `item['review']['verdict'] != 'approved'` becomes a predicate call; spec :1029 triple) unless another `s5_window` word literal
   remains in `build`; the new sites `instance_hold`, `_tests`, `lifecycle_reasons`, `_claim_rollcall` are expected to hold no counted
   comparison (but `lifecycle_reasons`/`_tests` may hold other row-word literals once registered — e.g. `"green"` is not a row word; by
   measurement). Any counted comparison at a new accept site is a stop and a question. The allow-list pin does not move.

architecture content: `AR-1 -- the approving pair leaves code: the row s5_window holds which word approves at each site`; `AR-13 -- the
critic's review word is read through gate_template.acceptable at the stamp, the proven count, the lifecycle check, the form check and the
window notes`; `AR-15 -- one builder of the static-review note`; `AR-22 -- APPROVING and every reader change in one commit`; `AR-28 -- an
absent or unknown word holds the stamp and the count; an unreadable registry is named at the two sites where an approving word triggers a
check`; `AR-29 -- xref, owner data, no census unit`; `AR-20 -- D13 re-measured, the build triple's move named`; judgment `none -- the
critic's verdict stays the critic's judgment; the registry carries which word approves where`.

Edges:
- E1 (behaviour on a readable registry): every word -> the same outcome as today at W1-W4 (`approved`, `approved_with_fixes` approve;
  `unverified`, `rejected`, `""`, None, case variants, non-str do not). At the window nothing changes (C3-d table rows unchanged).
  INVARIANT: no test is stamped, counted or spared a check that is not today, and none is held that is not today.
- E2 (error direction, W1/W2 — gate role): False = hold / not counted: safe. INVARIANT: an unknown word never stamps a case or counts a test
  as proven.
- E3 (error direction, W3/W4 — the predicate's False is the UNSAFE side here, §0 fact 3): the registry branch comes first and names the
  registry (one reason / `None`). Adversarial inputs that must stay safe: unreadable registry (pinned), a registry that reads but lacks the
  consumer (`registry_problem()` is "" -> `acceptable` False -> W3: an approved non-green test is skipped, W4: no refusal) — held by CI: A26
  F-b/F-f and the positive rows of each table turn red on a consumer typo (C3-reg E2 precedent). INVARIANT: a broken registry never removes a
  lifecycle demand or a form refusal silently.
- E4 POSITIONAL (W3): the registry reason is computed before the loop and after the `held` / `not_read` join (:851-854). INVARIANT: the
  `not_read` reason is still produced when the join fails.
- E5 POSITIONAL (W4): after `doc is None` and `found is None`; before the outcome test. INVARIANT: a missing form or roll-call is still
  `None` with its own text first.
- E6 POSITIONAL (W5/W6): the stopped branch first, the generic branch second, the probe-gap override later (:1745 removes the earlier
  `review` note, unchanged). INVARIANT: `build`'s note and `validate_window`'s gap agree per kind (item 5).
- E7 TEXT: byte-identical: the two static notes, `GAP_ORIGIN["review"]`, `NOT_APPROVED`, every existing reason of `lifecycle_reasons` and
  claim of `_claim_rollcall`. New texts: the two registry sentences only. FR-41 residue named: on an unreadable registry the stamp's hold
  word is `not_approved` (a false cause); `HOLDS` is not extended here (non-goal); C3-reg-precondition stops the stage first.
- E8 TEMPORAL: manifests recorded before are read word for word as today. INVARIANT: no recorded verdict changes meaning.
- E9 (absent / empty): `critic_verdict` absent -> `None`/`""` -> not approving (W1, W2), W3 skips a non-green row as today. INVARIANT: no
  word, no approval.
- E10 (P31 / one road): every reader of "does this critic word approve" in the owns goes through the same row; the readers left are RD1-29b,
  a named node. INVARIANT: no second copy of the pair survives in the owns (grep in the DoD, §1 AR-1 row).
- E11 (limit): none introduced.

### RD1-29b — the residual readers of the critic's word (named node; rule 6 slice, F-7 (a))

owns (sketch, drafted when the Lead takes it): `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/traceability.py` (`_review_basis`
:884), `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/factory_dashboard.py` (:887), `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/ledger.py`
(:1191, a membership test of the full vocabulary: read `contract.CRITIC_VERDICTS`, AR-1), `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/window_record.py`
(`_sent_back_lines` :2268, `== "rejected"`), the registry row `s5_window` (two display consumers), `test_gate_registry.py` (D13). Test: the
display readers' own tests are quarantined (`test_traceability_report.py`, `test_factory_dashboard_joins.py`); the rows go to the keep file
that covers `traceability.py` / `factory_dashboard.py` (`test-layers.json` `covers`, to be read when drafted) — a stop if none. After RD1-29.

### RD1-28b — the product record and window probe vocabularies (named node, F-4 (a))

The product record words (`red_sandbox.product_verdict`: `intended_failure`, `probe_defect`, `incomplete`, `survived`) and the window block
words (`intended_failure`, `partial_product`, `model_changed`) have no registry row; `already_probed:1552` (`survived`) and
`red_sandbox.request_status:1500` read them. owns (sketch): the registry (a decision: rows or widening, F-4 (b)/(c)), `red_sandbox.py`,
`proof_level.py` (`already_probed` :1552), `window_record.py` (registration only), their keep tests. After RD1-28.

## §3. Measured premises (the commands; nothing was run here)

- D13 before/after (each card): `python -B -c "import sys; sys.path.insert(0, r'C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts'); import gate_registry as GR; r = GR.analyse(); t = sorted({(i['file'], i['function'], x) for i in r['items'] for x in i['rows']}); print(len(r['items']), len(t)); [print(x) for x in t]"`
  (run in the builder's tree; on this wave tree the pin says 150 items, `test_gate_registry.py:1069`; triples per :967-1030).
- Sites and allow texts: `python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/gate_registry.py --sites` (the `ast.unparse`
  form of every counted comparison, its row and `allowed`).
- Behaviour preservation (RD1-26, RD1-28 P4, RD1-29 W5/W6): the six recorded windows, `validate_window` gap lists before/after equal —
  `python -B -c "import json,glob,sys; sys.path.insert(0, r'C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts'); import acceptance as A; [print(p, A.validate_window(json.load(open(p, encoding='utf-8')), p.split('work')[0])) for p in glob.glob(r'C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/fixtures/stories/*/work/windows/*.json')]"`
  (a smoke check: critic t-1039 found the recorded stories exercise few branches; the premise rests on the code traces in the cards).
- RD1-29 word census (premise "the pair is the only approving set"): `grep -rnE "approved_with_fixes" <PKG>/scripts/*.py` — read here with
  the Grep tool: hits at `case_stamp.py:28,315,317`, `check_delivery.py:860`, `factory_dashboard.py:887`, `ledger.py:1191`,
  `report_facts.py:63`, `traceability.py:884`, `validate_artifacts.py:2199,2203`, `contract.py:2209,2212`, `critic_rollcall.py:18`,
  `check_coverage.py:137` (comment); `handoff_check.py:966` reads `report_facts.APPROVING` (found by grep `APPROVING`).

## §4. Order, parallelism, collisions

- **Shared files of the three cards**: `gate-registry.json` (row-disjoint: `test_identity` / `probe_verdict` / `s5_window`);
  `test_gate_registry.py` (D13 count and triples move in all three; the allow-list pin moves in RD1-26 only); `acceptance.py`
  (RD1-26: `_bound_to`, `green_on_current_bytes_why`; RD1-28: `validate_window:1227` — function-disjoint); `test_proof_level.py` (RD1-26 and
  RD1-28 add rows to the SAME table function, `c3_b2_...` :1794 — a text conflict on one function); `test_window_record.py` (RD1-28 probe rows,
  RD1-29 note rows in `c3_d_...` — different functions unless RD1-28's rows land in the C3-d function).
- **Recommendation (fork F-9 (a))**: ONE builder for RD1-26 + RD1-28 (sequential inside one node: they share `test_proof_level.py`'s table and
  `acceptance.py`; splitting costs a merge of one table function and two D13 re-measures for ~6 sites); RD1-29 a SECOND builder after its
  plan critic, in parallel with the first. The later of the two merges main into its tree and re-derives D13 by measurement (S-f, D-0048);
  no number is resolved by keeping either side.
- **Wave-3 cards** (`docs/tasks/specs/20261117-rules-debt-wave3-g-h-cards.md`, `...-wave3-j-k-cards.md`): row-disjoint in `gate-registry.json`
  (C3-g `baseline_identity`, C3-h `stand_identity`, C3-j `s5_stand_limits`, C3-k1..k4 `provenance_acceptance`, C3-k3 also
  `environment_preparation` and `baseline_identity`); no production file in common (their owns: `baseline_contract`, `environment_record`,
  `gate_preflight`, `stand_gaps`, `profile_contract`, `execution_request`, `execution_fingerprint`, `run_suite`, `manual_evidence`,
  `coverage_contract`, `manual_capture`, `environment_preparation`, `driver_stage_build`). Overlap only in `test_gate_registry.py`:
  - RD1-26 x C3-k2 / C3-k3 / C3-k4: the allow-list pin (:305-312; k2/k3 add `provenance_acceptance` allow entries, which come FIRST in
    registry order) and D13 — the later merger re-derives the whole list from the live registry;
  - RD1-28, RD1-29 x every wave-3 card: D13 count/triples only;
  - RD1-29 under F-6 (a) (a new row) would also move the split pin (:354-355), `EXPECTED_CONVERTED` (:68-77) and the F4 list — the pins
    every wave-3 conversion moves; under the recommended (b) it moves none of them.
  Order: none forced; whichever merges later re-derives (S-f E10). `очередь:` none on production files.

## §5. Forks (returned, not decided; each card executable by the recommendation)

- **F-1 (RD1-26, scope)** `run_history._job_contract:221` and `_compare_shas:256-259`: (a) convert both as true accept sites (they decide "a
  stranger's shas stand in" and "a red/green pair is the same test, dropped") — **rec**; (b) name them non-acceptances (register `validate`
  with a why) — cheaper, but `_compare_shas`'s "same" drops a pair with no further check, which is an acceptance (E-c invariant: a re-role
  never hides a literal acceptance).
- **F-2 (RD1-26, edge)** `_compare_shas` on an unreadable registry: (a) skip the identity basis, fall to the file basis, then `unknown` —
  **rec** (no "same" from an unaccepted word; the file basis is another, stronger quantity); (b) return `changed` (a pair recorded on equal
  shas: an unknown said as a fact, FR-41); (c) return `unknown` at once (ignores an equal block fingerprint that would decide today).
- **F-3 (RD1-26, gate role of `same_test`)** `green_on_current_bytes_why`: (a) a `["matched"]` consumer, equal to `== "raw"` because the call's
  two dicts carry only `input_hash` (E2) — **rec**; (b) keep `!= "raw"` and register the function `validate` (F-b forbids a converted accept site
  without `acceptable`); cost of (b): the literal stays a second rule beside the registry.
- **F-4 (RD1-28, vocabulary)** the word `intended_failure` from three producers: (a) one helper `probe_proved` under `probe_verdict`, no new
  words, `decides` names the two other producers; the product/window vocabularies become RD1-28b — **rec** (behaviour identical for every
  input; C3-b2's E11 "one producer per consumer" is relaxed for `probe_verdict.proved`, named); (b) widen `probe_verdict` with the product and
  window words and register their producers (one row for every probe outcome word; a meaning change of the row: classes for `survived`,
  `probe_defect`, `partial_product`, `model_changed` need a decision); (c) one row per producer (three rows sharing a word).
- **F-5 (RD1-28, mismatched words)** `already_probed:1536` accepts `no_failure`/`wrong_location` (class mismatched) to answer a repeat:
  (a) move the literal into `_probe_record_defect`, registered `validate` with the why in item 1 — **rec** (visible to A26, attributed; a wrong
  True refuses a probe, never passes a test); (b) a new token form for "a judged word" in `gate_template` / `_token_problem` (changes the
  predicate's second wall; architecture-level, out of this round); (c) leave it (A26 stays blind to it).
- **F-6 (RD1-29, the row)** where the delivery consumers live: (b) widen `s5_window` (`approved_with_fixes` as `not_applicable:with_fixes`,
  delivery consumers beside the window's) — **rec**, the one-road option (P31, designer rule 6: one vocabulary, one row, one predicate,
  consumers per site); cost: the row id names the window while it now covers delivery, and `not_applicable` is a stretch of the class name
  for "approved with fixes"; (a) a new row `critic_verdict` (all four words, `approved_with_fixes` matched) for every reader outside the
  window — honest classes, but the critic's words then live in two rows (a second road), the new row needs its own `unknown_branch` /
  `waits_at` / `addressee` decided, and it moves the split/converted/F4 pins every wave-3 card moves. Either option changes a row's meaning:
  plan critic first.
- **F-7 (RD1-29, scope)** the readers the critic did not list (§0 fact 4): (a) RD1-29 covers the listed sites plus `handoff_check` (a reader of
  the deleted `report_facts.APPROVING`, AR-22 forces it in); the display readers, `ledger`'s membership test and `_sent_back_lines` go to the
  named node RD1-29b — **rec** (their tests are quarantined: placing their rows is a separate question); (b) all in RD1-29 (one commit, but
  the test placement blocks the node).
- **F-8 (RD1-29, notes)** the condition of `build`'s review note: (a) mirror `validate_window`'s four kinds (handed gets `handed_review`) —
  **rec** (note iff gap; a handed `unverified` loses a note that was never printed, `verdict` explains only existing gaps, :1990); (b) keep
  `build`'s two branches and convert only the literal (the handed case keeps a note with no gap).
- **F-9 (order)** (a) one builder RD1-26+28, one RD1-29 after the plan critic, in parallel — **rec**; (b) three sequential builders (three D13
  re-measures, the shared table function edited twice); (c) one builder for all three (RD1-29 waits for its plan critic and holds 26/28).
- **F-10 (plan critic scope)** RD1-28's `decides` clause (item 1) documents readers and does not change what counts: (a) send it with
  RD1-29 to the one plan critic of the topic (R13-g) — **rec**; (b) treat it as no meaning change and skip.

## §6. Small technical choices closed (designer)

- Consumer names: `test_identity.proof_bound` (the critic's example `review_bound` covered reviews only; `_bound_to` also binds probes,
  :1228), `test_identity.mechanical_raw`, `test_identity.param_twin`, `test_identity.pair_same`, `probe_verdict.proved`, `s5_window.stamp`,
  `.proven`, `.lifecycle`, `.form_outcome`.
- `_job_contract` written as a loop (no nested function: A26 keys sites by the outer `def`, and a lambda/nested def would make the
  `acceptable` call's attribution depend on the scanner's walk).
- `probe_proved` is public (called from `acceptance.py`); `_probe_record_defect` private (one caller).
- Registry-why texts follow the family of `proof_level.py:947-948` (critic fix 2's builder absorbs them later).
- Tests: rows in existing keep tables only; no new test file (TESTING.md; `test-layers.json` keep rows, §0 fact 6).

## §7. Readers of every touched file (designer rule 7)

Command (Grep tool, content, over `C:/QAFactory/forge-repo/tools`): pattern
`gate-registry\.json|test_gate_registry|acceptance\.py|run_history\.py|proof_level\.py|window_record\.py|case_stamp\.py|report_facts\.py|check_delivery\.py|test_proof_level|test_window_record|test_case_stamp|test_check_delivery|test_report_facts|APPROVING|GAP_ORIGIN|_bound_to`
-> 28 hits in 7 files. Over `.githooks`: 0 hits (positive control `\.py` over the same folder: 20 hits). Over `.claude/agents`: 0 (control
`critic-diff-brief|builder-rules`: 7 hits). Over `.claude/settings.json`: 0 for the package names (control `gate-registry|proof_level|window_record|hooks|tools/`: 51 hits, all `hooks|tools/`). `handoff_check.py` was not in the pattern; it is a package file read by no forge tool by the same reasoning (not grepped separately — estimate).

| reader | reads | verdict |
|---|---|---|
| `tools/source-split-carriers.json:15, 25` | `gate-registry.json` (json-file-function carrier), `test_gate_registry.py` (D13 py-triple carrier) | unchanged: the triple tuple form `(file, function, row)` is kept; new triples use it |
| `tools/source_split.py:2753-2891` | the same two carriers (selftest fixtures) | unchanged |
| `tools/controller-blocks-gen.py:145, 186-194` | `window_record.py` named in door texts | unchanged (no CLI or door of `window_record.py` changes) |
| `tools/lint-baseline.json:193, 253` | `test_check_delivery.py`, `test_report_facts.py` (`HandReaderInput` counts 7 and n) | changes in RD1-29 only if a new row adds a hand-read input: the builder keeps the count (ratchet); a raise is a stop |
| `tools/test_forge_metrics.py:253-257` | `check_delivery.py` as a file-index sample | unchanged |
| `tools/test_quarantine.py:2199` | `gate-registry.json` as a prose carrier path | unchanged |
| `tools/fixtures/dispatch_manifest/K8.txt:3` | a fixture text naming one of the files | unchanged |
| package readers (not rule-7 scope, load-bearing): `case_stamp.APPROVING` <- `case_stamp.instance_hold`, `test_case_stamp.py:211`; `report_facts.APPROVING` <- `report_facts._tests`, `handoff_check._claim_rollcall:966`, `test_case_stamp.py:211`; `_bound_to` <- `acceptance.validate_window`, `test_receipts_per_function.py:30` (quarantined, import kept: name and signature unchanged); `GAP_ORIGIN` <- `window_record.py:436, 1824` | | changes in RD1-29 (APPROVING readers, all in its owns); `_bound_to`, `GAP_ORIGIN`: unchanged |

Streams meeting at shared readers: RD1-26/28 (one builder) and RD1-29 meet at `test_gate_registry.py` (D13) — S-f; the wave-3 cards meet
there too (§4).

## §8. Noticed analogs (reported, scope not widened)

- `probe_verdict` words read by state readers with no registration: `proof_level.tooling_gap_key:1105`, `probe_record_state:1149-1155`
  (`PROBE_JUDGED_VERDICTS` :1116), and in `probe_by_code` (`keep_standing_record`, `publish_binding`, `main` — the row's `decides` says "not
  sites yet"). Produce/state readers, not acceptances; a queue line for the Lead.
- `critic_rollcall.APPROVING_VERDICTS` (`approve`, `approve_with_fixes`, `approve_with_concerns`) read at `controller.py:3547`,
  `driver_stage_plan.py:819`: the S4 roll-call vocabulary, no registry row.
- SIBLING_MAP axis 25 (:451) calls the `same_test` twins "queued (batch 3, ...)": the critic did not find that row and I did not either
  (not searched in `plans/piles/` beyond the finding's own statement, :6 of the finding) — RD1-26 item 7 replaces the sentence.
- Critic t-1084 fix 2 (four forms of the registry sentence) gains members from these cards (RD1-26 item 3, RD1-29 items 3 and 6).

## §9. Not done / not established

- Nothing was run: D13 deltas, `--sites` texts, the window smoke, `test_judgment_census.py`. Every count is "by measurement at the build".
- Not read: how `check_delivery` classifies a `lifecycle_reasons` line (owner/FR-46; RD1-29 item 3 makes it a builder stop); the
  `_claim_rollcall` test location; whether `window_record.build` can be driven inside the C3-d table's world; `_kept` (RD1-26 E2 relies on
  `_kept(None)` being empty — builder confirms).
- `handoff_check.py` readers in `tools/`/`.githooks`/`.claude` were not grepped separately (estimate: none).

## §10. Reading trail

- Brief files: the three findings (C3 wave tree), `docs/tasks/specs/reviews/t-1084-c3-b2-d-topic-code.md` (whole), the phase-2 spec
  (:270-409, :918-1257, :2294-2347, headings).
- C3 wave tree, `ai-packages/qa-factory/`: `scripts/acceptance.py:1-235, 1053-1302`; `scripts/run_history.py:136-265, 583-742`;
  `scripts/proof_level.py:840-1000, 1405-1580`, grep of defs and of probe words; `scripts/gate_template.py` (whole);
  `scripts/gate_registry.py:14-123, 740-979`; `references/gate-registry.json:1-7, 120-274, 586-615` and greps for row ids, function names;
  `scripts/red_sandbox.py:1465-1512`; `scripts/window_record.py:305-334, 803-835, 1615-1764, 1937-1996, 2255-2279` and greps;
  `scripts/check_delivery.py:820-879`; `scripts/case_stamp.py:305-349`; `scripts/report_facts.py:55-69, 1515-1549`, def list;
  `scripts/handoff_check.py:935-979`; `scripts/traceability.py:874-889`; `scripts/factory_dashboard.py:878-891`; `scripts/ledger.py:1180-1195`;
  greps `APPROVING|approved_with_fixes` over `scripts/`, `PARTIAL_PRODUCT|MODEL_CHANGED`, `"survived"`, `review\.outcome` over `handoffs/`;
  `scripts/tests/test_gate_registry.py:255-359, 960-1079` and greps; `scripts/tests/test_proof_level.py:1329-1447, 1794-1866` and def list;
  `scripts/tests/test_window_record.py:2815-2898`; `scripts/tests/test-layers.json` (greps for the test files and covers);
  `scripts/tests/fixtures/judgment-census.json:1-6` and the function grep.
- `docs/SIBLING_MAP.md` (wave tree): axis headings, :194, :449-451.
- Wave-3 specs: heading/owns greps of both files.
- Rule-7 greps: §7.

## Lead decisions on the forks (17.11.2026)

- F-1 = (a), F-2 = (a), F-3 = (a), F-5 = (a), F-8 = (a), F-9 = (a), F-10 = (a): by recommendation.
- F-4 = (a) and F-7 = (a) with a condition: RD1-28b and RD1-29b are NOT parked. They are nodes of this same wave: the
  designer cards them right after the plan critic's verdict on this file, and they are built before the C3 fix topic
  is called closed (the owner's word 17.11: the debt is worked down, not grown). The plan critic says whether either
  fits inside RD1-28 / RD1-29 after all.
- F-6 = (b) (one row, one road) — the plan critic judges it explicitly: the row id names the window while it would
  cover delivery, and `not_applicable` for "approved with fixes" is a stretch.
