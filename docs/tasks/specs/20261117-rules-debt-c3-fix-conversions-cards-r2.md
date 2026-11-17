# Rules-debt C3 fix round, round 2 — cards RD1-26, RD1-28, RD1-29 (t-1107, F19; node rules-debt/1/RD1-26)

Designer draft for the Lead. This file REPLACES `docs/tasks/specs/20261117-rules-debt-c3-fix-conversions-cards.md` (round 1) and
stands alone: a builder executes a card from this file only. It applies the plan verdict t-1103
(`docs/tasks/specs/reviews/t-1103-c3-fix-conversions-plan.md`, fixes 1-13) and the Lead decisions of 17.11.2026 (the round-1
fork decisions at the end of the round-1 file, and the t-1107 brief). RD1-28b is folded into RD1-28 and RD1-29b into RD1-29;
there is no residual node. The closing table (§9) maps every fix and every brief decision to the place it is applied.

The parent spec `docs/tasks/specs/20261117-rules-debt-phase2-cards-spec.md` (C3 shared items S-a..S-f, :278-346; the C3-b2 card
:918-1025 and the C3-d card :1029-1162 as patterns) still applies; where this file states a rule, this file wins.

**Where the facts were read.** The C3 wave tree `C:/QAFactory/forge-repo/.claude/worktrees/agent-ac40b44fb0a175afa/ai-packages/qa-factory/`
(it carries C3-b2, C3-d, C3-reg-precondition and RD1-27). A builder is writing in that tree now in `controller.py`, `gate_template.py`,
`proof_level.py` and `execution_request.py` (the RD1-27 fix round); for those four files this file names FUNCTIONS, never line numbers.
Line numbers of other files are of that tree and are re-read by the builder on its own base. In the cards `<PKG>` is
`C:/QAFactory/forge-repo/ai-packages/qa-factory`. **Base: main AFTER the C3 wave branch is merged** (that merge carries the RD1-27
fix round). Nothing was RUN in this dispatch (no shell): every count is "by measurement at the build", with the command in §3; the
numbers marked (t-1103) are the plan critic's measurements on a scratch copy and are expectations, not pins.

---

## §0. Facts (read before dispatch)

1. **The probe word has three producers.** Row `probe_verdict` registers only `probe_by_code.judge_probe_row` / `_judge_rows`
   (`gate-registry.json:592-595`). Readers of `intended_failure`:
   - `proof_level._product_receipt_repeat` (first conjunct of its loop condition) reads the PRODUCT record written by
     `red_sandbox._write_product_records` from `red_sandbox.product_verdict` (`red_sandbox.py:1478-1489`: `intended_failure`,
     `probe_defect`, `incomplete`, `survived`);
   - `proof_level.already_probed`, item 1 (the `own = (...)` expression) reads a `probe_by_code` record or the product record;
   - `acceptance.validate_window:1227` reads the window item's `probe` block, written by `window_record._receipt_block`
     (`window_record.py:885`) or `window_record._probe_from_receipt` (:803; `PARTIAL_PRODUCT` / `MODEL_CHANGED`, :720-721);
   - DISPLAY readers (t-1103 key 1): `window_record._probe_scope_notes:664` and `window_record.unproved_keys_text:698` — they choose
     text, they accept nothing.
   `already_probed` item 2 reads `no_failure` / `wrong_location` (class `mismatched`, which `gate_template.acceptable` never takes);
   item 3 reads `survived`, a word of no row. `red_sandbox.request_status:1500` compares `product_verdict(p) == "survived"`.
   The shared word `intended_failure` means one thing in all three producers (`red_sandbox.py:1483-1484`; `window_record.py:834-835`).
2. **The approving pair.** `case_stamp.APPROVING` (:317), `report_facts.APPROVING` (:63) and `check_delivery.lifecycle_reasons:860`
   accept `approved_with_fixes`; row `s5_window` `words` are `["approved", "unverified"]` (`gate-registry.json:254`) and C3-d pins
   `approved_with_fixes` as a review gap at the window (`test_window_record.py:2854, 2860`).
3. **Two sites refuse MORE when the word approves**: `lifecycle_reasons` (approved OR green enters the loop) and
   `handoff_check._claim_rollcall:966` (an approving outcome over a partial roll-call is refused). There the predicate's False is the
   unsafe side.
4. **The pair outside the listed sites** (all now in RD1-29): literal pair at `traceability.py:884` (`_review_basis`, a method) and
   `factory_dashboard.py:887` (`instance_basis`); the full vocabulary at `ledger.py:1191` (membership, after `is_rejected` returned at
   :1189); `rejected` at `window_record._sent_back_lines:2268` and `ledger.is_rejected:1041`.
   Correction (t-1103 key 1): `_claim_rollcall` serves the S4 CASE critic's form only (`handoffs/s4-case-critic-to-designer.yaml:66`,
   `review.outcome: <one of vocabulary.critic_verdicts>`); that outcome is vocabulary-checked by the handoff
   (`handoffs/vocabulary.yaml:119`, `test_handoff.py:93-107`).
5. **The registry sentence has one builder** on the base: `gate_template.py` holds the family's builder of "the gate registry cannot
   be read" (RD1-27). It is being reshaped by the fix round on the wave branch (the `stop` flag goes). Every new registry sentence of
   these cards calls **the family's builder as it stands on the base at the build (`gate_template.py`); never a literal copy**; this
   file does not quote its signature. The table that pins the family is the RD1-27 table in `test_gate_registry.py` (grep `RD1-27`;
   on the wave tree :1188-1199); each new user adds one row there, in that table's form at the build.
6. **Tests.** Quarantine cohort rows (no row goes there): `test_acceptance_semantics.py`, `test_receipts_per_function.py`,
   `test_check_coverage.py`, `test_factory_dashboard_joins.py`, `test_traceability_report.py`, `test_run_history_identity.py` (cohort
   8073673, `test-layers.json:9692`). Keep files used (a `layer` row in `test-layers.json`): `test_proof_level.py` (:4124),
   `test_window_record.py` (:7025), `test_case_stamp.py` (:459), `test_check_delivery.py` (:531), `test_report_facts.py` (:4474),
   `test_gate_registry.py` (:2032), `test_handoff.py` (:2300, holds the `_claim_rollcall` checks in
   `rollcall_the_claim_checks_the_ceiling_and_the_forms_n_of_m`, :2647), `test_probe_marker_judgment.py` (:3892, holds the
   `_sent_back_lines` checks :430-435). Named, not edited: `test_probe_by_code.py` (:3689) and `test_red_sandbox_probe.py` (:4335)
   pin the `survived` answer; `test_ledger.py` (:2830) pins `review_unrecognised` (5 hits); `test_s5_process.py:328-334` (keep, held by
   import) pins `green_on_current_bytes_why` green / other bytes in a full mechanical-round world. The mechanical-round lines of
   `test_blocked_by_env_window.py:627-631` do NOT reach the identity comparison: its instance is blocked and returns at "the instance's
   outcome is not passed" (read: :629-631) — so RD1-26's rows stay in `test_proof_level.py` (fix 9).
7. **Census.** `judgment-census.json` holds rows only for `acceptance.validate_window` (:7, `shape`) and `window_record.build` (:1265,
   `shape`) among every function these cards touch (Grep of the census for all touched function names; the two hits are the control).

## §1. Architecture, rules, owners (designer rule 1; package spec)

AR-n touched (texts: `<PKG>/design/architecture.md`; index `docs/ARCHITECTURE_INDEX.md`) and the change check each card's DoD carries:

| AR | card | how kept | change check in the DoD |
|---|---|---|---|
| AR-13 (a fact with a reader is read only through it) | all | every named acceptance reads its word through `gate_template.acceptable` (directly or through one registered helper) | `gate_registry.py --check` exit 0; `--sites`: no `UNREGISTERED`, no `NOT ALLOWED` |
| AR-15 (one survivor) | 28, 29 | one helper per reading: `proof_level.probe_proved`, `proof_level._probe_record_defect`, `window_record._review_note` / `_static_review_note`; one reader of `rejected` (`ledger.is_rejected`, fork F-r2-3) | the callers call the helper (AST/grep line in the report) |
| AR-1 (closed variety is a data row) | 29 | `APPROVING` (two copies) and every literal copy of the approving pair leave code | Grep `APPROVING\b` and `"approved_with_fixes"` over `<PKG>/scripts/*.py`: the only hits left are `contract.py` (the vocabulary), `validate_artifacts.py` (the four `fix_notes` shape lines), `critic_rollcall.py` (another vocabulary) and comments (positive control: `contract.py:2212` is found) |
| AR-22 (every field read has a producer; producer and readers change together) | 28, 29 | the product-record and window-block producers are registered `produce` in row `probe_verdict` (the relaxed "one producer per consumer" is data, not prose); `APPROVING` is deleted with all its readers in one commit | `--check` exit 0; Grep `APPROVING\b` over `scripts/` and `scripts/tests/` |
| AR-28 (an unknown never becomes a pass) | all | absent / None / unknown word / unreadable registry -> the safe side per site, pinned; where False is the unsafe side (W3, W4) the registry branch keeps the refusal or names the registry | the unreadable-registry rows of each card |
| AR-29 (code judges data; judgment by a tier above) | all | every check is a membership join of a recorded word to a registry row; the critics' and the probe judge's verdicts stay theirs | `judgment-census.json` unchanged (`test_judgment_census.py`, canon) |
| AR-20 (shrink-only ratchets; a raise is named) | all | D13 count/triples, the allow-list pin (RD1-26) and the RD1-27 table move by measurement, each move named in a comment | `test_gate_registry.py` (slow: canon) |

Owner and census class of every check added or altered (AR-29, P27): every one serves **data (code)** — it joins a word a producer
wrote to a registry row (census class `xref`, as C3-b2 recorded). None moves a judgment into code. No check adds a refusal unit (no
new `raise` / exit; reasons and notes are list transport, `_claim_rollcall` returns tuples), so no census row moves: `validate_window`
stays `shape` (:7), `window_record.build` `shape` (:1265). If `test_judgment_census.py` reads otherwise, the node stops with a question.

Commit lines: `architecture:` and `judgment:` lines in the gate's own form — the only carrier of that form is
`tools/architecture_gate.py` (not copied here). Each card gives the CONTENT; `judgment: none` always carries its ` -- <why>`.

Rules walked (FR, by section): A — FR-4 (a person's pass untouched), FR-46 (W3's line is owned `factory_record`, `check_delivery.py:2619`);
B — no text a person reads changes on a readable registry (pinned texts stay byte-identical); the new registry sentences come from the
family builder (FR-6 via one form); FR-10 (W5/W6: no note contradicts the instance on an unreadable registry); C — FR-13 (words in data),
FR-38 (no role field changes); D — FR-59 (every unknown branch named); E — FR-41 (a registry-caused refusal never claims the bytes or
the verdict changed; residues named per card); G — FR-32. F: not touched.

---

## §2. Cards

### RD1-26 — `test_identity`: `_bound_to` and its axis-25 twins through the predicate (critic t-1084 fix 1)

given:
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/design/factory-rules.md` (whole), `C:/QAFactory/forge-repo/plans/builder-rules.md`, `C:/QAFactory/forge-repo/docs/TESTING.md`
- this card, §0, §1, §3, §4; the parent spec's S-a..S-f (`docs/tasks/specs/20261117-rules-debt-phase2-cards-spec.md:278-346`) and the C3-b2 card (:918-1025) as the pattern
- read under `<PKG>/`: `scripts/acceptance.py:1-12, 130-216`; `scripts/run_history.py:138-262, 689-702, 740`; `scripts/proof_level.py` functions `compare_identity`, `same_test`, `_kept`; `scripts/gate_template.py` (whole); `scripts/gate_registry.py` (`analyse`, the sites scan); `references/gate-registry.json` row `test_identity`; `scripts/tests/test_proof_level.py` (`c3_b2_a_reuse_is_accepted_through_the_registry_row_and_an_unknown_runs_again` and its `unreadable_registry()` seam; the K-C census block with `callers = (...)`); `scripts/tests/test_gate_registry.py` (D13 pins, the allow-list pin, the RD1-27 table); `scripts/tests/test_s5_process.py:270-337` (the existing mechanical-round world, read only)
owns:
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/references/gate-registry.json` (row `test_identity` only: four `sites` entries, four `accepts` consumers)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/acceptance.py` (`_bound_to`, `green_on_current_bytes_why`, one module constant for the registry tail, the `gate_template` import line)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/run_history.py` (`_job_contract`, `_compare_shas`, their point-of-use imports)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_proof_level.py` (rows in the C3-b2 table, items 2-5; one dict-shape check beside the K-C census, item 3)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_gate_registry.py` (D13 pins, the allow-list pin, one RD1-27 row; item 6)
non-goals: `same_test`, `compare_identity`; `validate_window` (C3-d's review branch; RD1-28's probe line); `_make_pair`'s `verdict == "same"` (`run_history`'s own pair word, produced by `_compare_shas`); `run_freshness_of`; `judgment-census.json`; `docs/SIBLING_MAP.md` (the Lead's, item 7); `gate_template.py` (the family builder is the RD1-27 round's); `test_s5_process.py` and `test_blocked_by_env_window.py` (read, not edited)
handoff: report path given by the Lead
edges: E1-E10 below
DoD: `python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/gate_registry.py --check` (exit 0; no F-b; `test_identity` stays converted) and `python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for C:/QAFactory/forge-repo/ai-packages/qa-factory/references/gate-registry.json C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/acceptance.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/run_history.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_proof_level.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_gate_registry.py` and the printed non-slow files; slow files (`test_proof_level.py`, `test_gate_registry.py`): batch canon, named in the report
siblings: axis 7 (`docs/SIBLING_MAP.md`, "Recorded-carrier readers": `_bound_to` named); axis 25 (`green_on_current_bytes_why`, `run_history.SHA_FIELDS` "queued (batch 3 ...)" — stale after this card, item 7); axis 5 (grep `same_test|compare_identity|green_on_current_bytes` over `references/execution-lifecycle.md`, `references/slices/qa-automator/execution-lifecycle.md`, `skills/qa-story/phases/s5.md`, each hit "checked, no edit (meaning unchanged)"); axis 34: no language, project or case key is read
designer: `C:/QAFactory/forge-repo/docs/tasks/specs/20261117-rules-debt-c3-fix-conversions-cards-r2.md` (RD1-26)

Sites (read on the wave tree):

| # | file:function | current expression | after |
|---|---|---|---|
| S1 | `acceptance.py:_bound_to` (:204-216) | `if proof_level.same_test(proof_level.proof_identity(item), proof_level.proof_identity(proof)):` (:211) | `if acceptable(proof_level.same_test(...same arguments...), "test_identity.proof_bound"):` |
| S2 | `acceptance.py:green_on_current_bytes_why` (:130-185) | `if proof_level.same_test({"input_hash": item.get("input_hash")}, {"input_hash": raw}) != "raw":` (:177) | `if not acceptable(proof_level.same_test(...same arguments...), "test_identity.mechanical_raw"):` + the registry reason (item 3) |
| S3 | `run_history.py:_job_contract` (:203-223) | `if all(PL.compare_identity(found[0], c) == ("same", "content") for c in found[1:]): return found[0]` (:221) | the loop of item 4 |
| S4 | `run_history.py:_compare_shas` (:248-262) | :256-259 | item 5 (F-2 = (c)) |

Items:
1. **Registry** (row `test_identity`). Add to `sites`: `{"file": "acceptance.py", "function": "_bound_to", "role": "accept"}`,
   `{"file": "acceptance.py", "function": "green_on_current_bytes_why", "role": "accept"}`, `{"file": "run_history.py", "function":
   "_job_contract", "role": "accept"}`, `{"file": "run_history.py", "function": "_compare_shas", "role": "accept", "allow": [<item 5>]}`.
   Add to `accepts`: `"test_identity.proof_bound": ["matched"]` (S1), `"test_identity.mechanical_raw": ["matched"]` (S2),
   `"test_identity.param_twin": ["matched"]` (S3), `"test_identity.pair_same": ["matched"]` (S4). `words`, `verdict_map`, `decides`,
   status unchanged. One producer per consumer (C3-b2 E11): `proof_bound`, `mechanical_raw` <- `same_test`; `param_twin`, `pair_same`
   <- `compare_identity`. The four functions are registered by no row (Grep of the registry for the four names, 0 hits; control:
   `validate_window|same_test|_match`, 3 hits).
2. **S1 `_bound_to`.** The truthiness at :211 becomes the predicate (`acceptable` is imported at :11). The mechanical-round branch
   (:213-216) is unchanged: `bound == record["reviewed_input_hash"]` compares a recorded value with its copy (docstring :209-210).
   Rows (C3-b2 table): (i) a review whose `proof_identity` matches the item's -> True; (ii) other bytes, no mechanical round -> False;
   (iii) matching identity, registry unreadable (the table's `unreadable_registry()` seam) -> False. Expected from the row's `decides`
   (`gate-registry.json:126`) and `_bound_to`'s docstring, never from its output before the change.
3. **S2 `green_on_current_bytes_why`.** The comparison at :177 becomes `not acceptable(...)`. On refusal: `problem =
   registry_problem()` (add `registry_problem` to the :11 import); when non-empty the reason appended is `f"job {attempt}: "` followed
   by the family builder's sentence (§0.5) for `problem` and the module constant `WHY_RAW_REGISTRY_TAIL = "the run's bytes were not
   judged"` (name: the family's constant pattern on the base; the builder may follow the base's naming); otherwise the existing
   sentence (:178-179) byte for byte. Rows, in the C3-b2 table of `test_proof_level.py` (fix 9: the blocked world of
   `test_blocked_by_env_window.py:627-631` returns before :177, and `test_s5_process.py` is held only by an import that will be cut),
   in a temp world written in the shapes the docstring names (:134-143; block `{input_fingerprint F, dispatch_id A, attempt_id J,
   block_id B, results [{instance_id I, status passed}]}` under `work/run-blocks/`, job `{job_id J, request {fingerprint_files [{kind
   test_files, path P, sha256 R}]}}` under `state/execution-jobs/`, no manifest so the one test file decides, item `{outcome passed,
   execution_fingerprint F, instance_id I, input_hash H}`, window `{mechanical_round {author_dispatch_id A, reviewer_dispatch_id X,
   reviewed_input_hash Y}}`): (i) H == R -> `(True, "")`; (ii) H != R -> False, the why holds `ran the test file as sha256 R`;
   (iii) H == R, registry unreadable -> False, the why holds `the gate registry cannot be read` and `job J: `, `check_not_in`
   `ran the test file as sha256`. The same green / other-bytes behaviour is already pinned at `test_s5_process.py:328-334` (named in the
   report, unedited). **Dict-shape pin (fix 10):** beside the K-C census `callers` loop add one check: in the AST of
   `green_on_current_bytes_why`, every argument of every `same_test` call is an `ast.Dict` with exactly one key, the constant
   `"input_hash"` (with a positive control on the current source). It fails when a later edit passes an identity-bearing dict.
   **RD1-27 row:** one row in the RD1-27 table: the family builder over `"R"` and the constant gives
   `"the gate registry cannot be read (R): a factory defect, the run's bytes were not judged"` (the expected text as that table writes
   its expectations at the build).
4. **S3 `_job_contract`.** :221-223 become
   `for c in found[1:]: verdict, basis = PL.compare_identity(found[0], c); if not (acceptable(verdict, "test_identity.param_twin") and basis == "content"): return {}` then `return found[0]`
   (`from gate_template import acceptable` next to `import proof_level as PL` at :220). Equivalence: `compare_identity` returns `same` as
   its only matched word, so the new test is True exactly when the old tuple equality was (t-1103: `_job_contract` 4 cases EQUAL);
   `basis` is not a row word. Rows: two contracts under one bare function name with (i) equal code and content shas -> `found[0]`;
   (ii) equal code, other content (`("same", "code")`) -> `{}`; (iii) no shas (`unknown`) -> `{}`; (iv) case (i), registry unreadable
   -> `{}`. Expected from the comment :215-219.
5. **S4 `_compare_shas` (F-2 = (c), fix 1).** Right after `verdict, _ = PL.compare_identity(*pair)` (:256) insert
   `if verdict != "unknown" and registry_problem(): return "unknown", "unknown", _first_sha(red), _first_sha(green)`; :259 becomes
   `return ("same" if acceptable(verdict, "test_identity.pair_same") else "changed"), basis, red[basis], green[basis]`
   (`from gate_template import acceptable, registry_problem` beside `import proof_level as PL` at :254). The site's `allow`, verbatim
   (`ast.unparse` form, t-1103): `{"compare": "verdict != 'unknown'", "why": "routes an unknown identity to the coarser file basis, and a
   verdict the registry cannot judge to unknown; not an acceptance"}` and `{"compare": "('unknown', 'unknown', _first_sha(red),
   _first_sha(green))", "why": "a state the function returns to its caller, not an acceptance of an identity word"}` (each text occurs
   twice after the edit; one entry covers both, t-1103). Any OTHER counted comparison `--sites` shows here is a stop and a question.
   Rows (C3-b2 table, red/green dicts `{code, raw, file}` as `_shas` returns them): (i) code shas equal -> `("same", "code", ...)`;
   (ii) code different -> `("changed", "code", ...)`; (iii) no identity, file equal -> `("same", "file", ...)`; (iv) nothing ->
   `("unknown", "unknown", ...)`; (v) code equal, registry unreadable, file equal -> `("unknown", "unknown", <first sha red>,
   <first sha green>)`; (vi) code different, registry unreadable, file equal -> `("unknown", "unknown", ...)`, never `same`;
   (vii) no identity, registry unreadable, file equal -> `("same", "file", ...)` (the file basis reads no registry word; unchanged).
   Expected from the docstring (:249-253, "unknown is never same") and FR-59. Rows (v) and (vi) are the flipping cases of t-1103
   (504 broken-registry combinations flip, all to `unknown`; none to `same`).
6. **Pins (S-f, deltas from the base).** No status moves: `EXPECTED_DEBT`, `EXPECTED_CONVERTED`, K-T1.2, the split and the F4 list
   stay. D13: re-measure (§3) before and after; expected (t-1103, fix-1 form) +4 items / +1 triple `("run_history.py",
   "_compare_shas", "test_identity")`; `_bound_to`, `green_on_current_bytes_why`, `_job_contract` hold no counted comparison.
   `D13_ITEM_COUNT` moves by the measured number with a comment line naming each added item. The allow-list pin gains the two entries
   in registry order, by measurement. The RD1-27 table gains the row of item 3. A measurement other than the expectation is named
   with its cause (not a stop when every new item is an allowed text of item 5; a stop otherwise).
7. **Lead at acceptance (not the builder):** SIBLING_MAP axis 25 — "queued (batch 3, finding AR-13/AR-22 remainder)" for
   `green_on_current_bytes_why` and `run_history` becomes "read through `gate_template.acceptable` (RD1-26)"; axis 7 adds "through
   the predicate" to `_bound_to`. The builder reports it under "Needed from integration".

architecture content: `AR-13 -- every test_identity word these four sites consume is read through gate_template.acceptable`;
`AR-28 -- a non-match, an absent identity or an unreadable registry is no match: run again, a stale review, no stranger's shas, and an
identity verdict the registry cannot judge is unknown, never same or changed`; `AR-29 -- xref, owner data, no census unit`;
`AR-20 -- D13, the allow-list pin and the RD1-27 table re-measured, each move named`; judgment `none -- the reuse decision is a join of a
computed identity word to the registry row`.

Edges (each with its invariant):
- E1 POSITIONAL (S1): the predicate replaces only the truthiness at :211; the mechanical-round branch follows unchanged. INVARIANT: a
  review or probe of other bytes never speaks for the test, except through a recorded mechanical round whose author ran green on the
  current bytes.
- E2 (S2, a reused function in a gate role): `same_test` is called with two dicts carrying only `input_hash`, so it can return only
  `raw` or `""` (`_kept(None)` is `{}`, t-1103 key 3); a `["matched"]` consumer is True exactly when `== "raw"` was. Permitted error:
  toward False (a stale review, one more critic round). Adversarial inputs that must stay safe: H empty -> `""` -> False; H non-str ->
  `str()` on both sides as today; R empty never reaches (`_raw_record` returns `missing` first); an identity-bearing dict passed by a
  later edit -> caught by the dict-shape pin of item 3 (not by a behaviour row). INVARIANT: a mechanical round closes only on the raw
  bytes the reviewer saw (comment :175-176).
- E3 (S3): `found[1:]` empty -> the loop does nothing -> `found[0]` (as `all([])`); non-dict contracts never reach (:212). INVARIANT: a
  stranger's sha never decides "the same".
- E4 POSITIONAL (S4, F-2 (c)): the registry guard sits after `compare_identity` and before the `verdict != "unknown"` branch; it fires
  only for a verdict that would decide (`same` or `different`). INVARIANT: no red/green pair is dropped on an identity word the predicate
  did not accept; a verdict the registry cannot judge is never reported as `changed` (FR-41) nor replaced by the file basis (which would
  drop pairs, 56 of 729 cases, t-1103); `unknown` is never `same`. The no-identity path (row vii) is untouched.
- E5 (unreadable registry, all sites): S1 False, S2 False with the family sentence, S3 `{}`, S4 `unknown`. Behind
  C3-reg-precondition (no new dispatch on an unreadable registry) these act inside a stage that began before. INVARIANT: a broken
  registry never lets an old review, probe, contract or run speak for the test.
- E6 (absent / None word): `same_test` and `compare_identity` never return None; `acceptable(None)` / `acceptable("")` are False
  (C3-0 rows in `test_gate_registry.py`). INVARIANT: no word, no reuse.
- E7 TEMPORAL: windows and run blocks recorded before are judged at their next read exactly as today on a readable registry
  (t-1103: 729 `_compare_shas` combinations and the six-window smoke EQUAL). INVARIANT: no recorded verdict changes meaning after the fact.
- E8 TEXT: the existing whys stay byte-identical on a readable registry (`acceptance.py:146-151, 161, 168-169, 173, 178-179, 183-184`);
  the new reason never says "ran the test file as sha256". INVARIANT: FR-41.
- E9 (K-C census, `test_proof_level.py`): `_compare_shas` and `green_on_current_bytes_why` still call `compare_identity` / `same_test` as
  an attribute call (`PL.`, `proof_level.`); the census check stays green unedited.
- E10 (limit): none introduced.

### RD1-28 — the probe word readers, the product-record vocabulary and its producers (critic t-1084 fix 3 (a); former RD1-28b folded)

given:
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/design/factory-rules.md` (whole), `C:/QAFactory/forge-repo/plans/builder-rules.md`, `C:/QAFactory/forge-repo/docs/TESTING.md`
- this card, §0 fact 1, §1, §3, §4, S-a..S-f and C3-b2 (pattern)
- read under `<PKG>/`: `scripts/proof_level.py` functions `_read_record`, `_product_receipt_repeat`, `already_probed` (whole), `tooling_gap_key`, `probe_record_state` (noticed readers, non-goals); `scripts/acceptance.py:1219-1234`; `scripts/red_sandbox.py:1478-1508`; `scripts/window_record.py:650-700, 720-721, 803-890`; `references/gate-registry.json` row `probe_verdict` (:589-612); `scripts/gate_template.py`; `scripts/gate_registry.py` (`analyse`, the sites scan); `scripts/tests/test_proof_level.py` (the C3-b2 table); `scripts/tests/test_window_record.py` (`sensitivity_gaps` :2008 and its users); `scripts/tests/test_probe_by_code.py:2600-2616`; `scripts/tests/test_red_sandbox_probe.py:480-532`; `scripts/tests/test_gate_registry.py` (D13)
owns:
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/references/gate-registry.json` (row `probe_verdict` only: `decides`, `words` +1, `verdict_map` +1, `sites` +6, `accepts` +1)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/proof_level.py` (new `probe_proved`, new `_probe_record_defect`; in `already_probed` the three verdict conjuncts of items 1-3; in `_product_receipt_repeat` its verdict conjunct)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/acceptance.py` (`validate_window`: the one probe line :1227 only)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_proof_level.py` (rows in the C3-b2 table, item 5)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_window_record.py` (one new parameterised function, item 6 — NOT in `c3_d_review_word_through_the_registry`)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_gate_registry.py` (D13 pins, item 7)
non-goals: `red_sandbox.py` and `window_record.py` CODE (registered in data only); the display readers `window_record._probe_scope_notes`, `unproved_keys_text` (named in `decides`, not converted: they choose text); the `probe_by_code.py` readers the row names "not sites yet" (`keep_standing_record`, `publish_binding`, `main`); `tooling_gap_key`, `probe_record_state` (state readers, §8); the review branch of `validate_window` (C3-d); `_bound_to` (RD1-26); census; words for `probe_defect`, `partial_product`, `model_changed` (no site compares them; a word outside the vocabulary is already False — said in `decides`)
handoff: report path given by the Lead
edges: E1-E11 below
DoD: `python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/gate_registry.py --check` (exit 0; no F-b; no F-f "registered more than once") and `python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for C:/QAFactory/forge-repo/ai-packages/qa-factory/references/gate-registry.json C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/proof_level.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/acceptance.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_proof_level.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_window_record.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_gate_registry.py` and the printed non-slow files; slow files: canon
siblings: axis 5 (grep `intended_failure|survived` over `references/execution-lifecycle.md`, `skills/qa-story/phases/s5.md`, `references/code-review-rubric.md`, each hit "checked, no edit"); axis 7 (the probe record readers); axis 34: one helper for every caller, no language key
designer: `C:/QAFactory/forge-repo/docs/tasks/specs/20261117-rules-debt-c3-fix-conversions-cards-r2.md` (RD1-28)

Sites:

| # | site | current | producer of the word read | after |
|---|---|---|---|---|
| P1 | `proof_level.already_probed`, item 1, the `own = (...)` expression | `behind.get("verdict") == "intended_failure"` | `probe_by_code` record or product record | `probe_proved(behind)` |
| P2 | `proof_level.already_probed`, item 2 loop condition | `record.get("verdict") in ("no_failure", "wrong_location")` | `probe_by_code` record | `_probe_record_defect(record)` |
| P3 | `proof_level._product_receipt_repeat`, loop condition | `record.get("verdict") == "intended_failure"` | product record | `probe_proved(record)` |
| P4 | `acceptance.validate_window:1227` | `probe.get("verdict") != "intended_failure"` | `window_record._receipt_block` / `_probe_from_receipt` | `not proof_level.probe_proved(probe)` |
| P5 | `proof_level.already_probed`, item 3 loop condition | `record.get("verdict") == "survived"` | product record | `_probe_record_defect(record, product=True)` |

Items:
1. **Registry** (row `probe_verdict`).
   - `words` gains `"survived"`; `verdict_map` gains `"survived": {"class": "mismatched"}` (fork F-r2-1, recommended: the broken product
     survived the test, a defect of the test — the twin of `no_failure`, `red_sandbox.py:1479-1482`).
   - `sites` gains: `{"file": "proof_level.py", "function": "probe_proved", "role": "accept"}`, `{"file": "proof_level.py", "function":
     "_probe_record_defect", "role": "validate"}`, `{"file": "red_sandbox.py", "function": "product_verdict", "role": "produce"}`,
     `{"file": "red_sandbox.py", "function": "request_status", "role": "produce"}`, `{"file": "window_record.py", "function":
     "_receipt_block", "role": "produce"}`, `{"file": "window_record.py", "function": "_probe_from_receipt", "role": "produce"}` (none is
     registered by another row: Grep of the registry for the six names, 0 hits, control as in RD1-26 item 1).
   - `accepts` gains `"probe_verdict.proved": ["matched"]`.
   - `decides` gains, appended: "The word `intended_failure` is written with the same meaning by three producers: this row's judge, the
     product record (`red_sandbox.product_verdict`, which also writes `survived`, `incomplete` and `probe_defect`) and the window's probe
     block (`window_record._receipt_block`, `_probe_from_receipt`, which also write `partial_product` and `model_changed`).
     `proof_level.probe_proved` is its one ACCEPTING reader; `window_record._probe_scope_notes` and `unproved_keys_text` read it for
     display only. `survived` (mismatched): the broken product survived the test, a defect of the test. A record that judged the test
     defective (`no_failure`, `wrong_location`, or a product record's `survived`) answers a repeated probe through
     `proof_level._probe_record_defect` (a `validate` site: the predicate takes no `mismatched` word, and a wrongly answered repeat only
     refuses a probe, never passes a test). `probe_defect`, `partial_product` and `model_changed` are compared by no site and are not
     words of this row: outside the vocabulary they are never acceptable." `field`, status, the other keys unchanged.
   - Both new function names are defined once (F-e; the builder greps `def probe_proved|def _probe_record_defect` first).
2. **`probe_proved(record) -> bool`** (public, new, next to `_read_record`): `return isinstance(record, dict) and acceptable(record,
   "probe_verdict.proved")` (fix 6: a bare str `"intended_failure"` is True through the predicate today, t-1103 key 2). P1 and P3 call it in
   place of the literal conjunct; P4 calls `proof_level.probe_proved(probe)` (`proof_level` is imported at `acceptance.py:10`).
3. **`_probe_record_defect(record, *, product=False) -> bool`** (new, private):
   `if not isinstance(record, dict): return False`; `if product: return record.get("verdict") == "survived"`;
   `return record.get("verdict") in ("no_failure", "wrong_location")`. P2 calls it bare, P5 with `product=True`. Each producer keeps
   exactly the words it answered by before (small choice §6). Both literals become visible to A26 and attributed to `probe_verdict`.
4. **`already_probed` docstring**: items 2 and 3 unchanged in meaning; no text edit is required. `prior_verdict` values unchanged.
5. **Rows in the C3-b2 table of `test_proof_level.py`** (its `unreadable_registry()` seam):
   - `probe_proved`: `{"verdict": "intended_failure"}` -> True; each of `no_failure`, `wrong_location`, `not_executed`, `incomplete`,
     `survived`, `probe_defect`, `partial_product`, `model_changed`, `""`, `"Intended_failure"`, `" intended_failure"`, `None` as the
     verdict, no `verdict` key -> False; the bare str `"intended_failure"`, `[]`, `None` as the record -> False; `intended_failure` with
     the registry unreadable -> False. Expected from the row's `verdict_map` and FR-59.
   - `_probe_record_defect`: bare: `no_failure`, `wrong_location` -> True; `survived`, `intended_failure`, `not_executed`, `incomplete`,
     `""`, no key, `None` record, a str record -> False. `product=True`: `survived` -> True; `no_failure`, `intended_failure`,
     `probe_defect`, `incomplete`, `""`, no key, `None` -> False. Unreadable registry: the same answers (no predicate). Expected from
     `already_probed`'s docstring items 2-3.
   - Callers' behaviour: already pinned, NAMED in the report, no new row — the C3-b2 table rows for item 2/3 (`no_failure`, product
     `intended_failure`, same/other bytes, unreadable), `test_probe_by_code.py:2606-2615` and `test_red_sandbox_probe.py:500-508`
     (a `survived` product record answers the repeat). Their expected values do not move.
6. **P4 rows in `test_window_record.py`**: one new parameterised function (next to `sensitivity_gaps`, :2008; never inside
   `c3_d_review_word_through_the_registry`, fix 13), driven through `sensitivity_gaps(window, task)` in the world of the file's existing
   `sensitivity:` tests (the builder reads one, e.g. the users at :2066/:2095). Rows: an item that ran green, owes a live check, whose
   probe block matches on every other field (location, reason, `failure_kind: assertion`, bound to the bytes) with verdict
   `intended_failure` -> no `sensitivity:` gap; `partial_product`, `model_changed`, `incomplete`, `survived`, `""`, no `verdict` ->
   `sensitivity:<iid>`; `intended_failure` with the registry unreadable (the `GT._READ` swap restored in `finally`, the C3-d form) ->
   `sensitivity:<iid>`. Expected from `validate_window`'s probe rule and FR-59.
7. **Pins (S-f).** No status moves. D13 re-measured before and after; expected (t-1103 for the single-tuple form; this card's split adds
   one comparison): +3 items / +2 triples — `("proof_level.py", "_probe_record_defect", "probe_verdict")` (the `in (...)` and the
   `== 'survived'` comparisons) and `("red_sandbox.py", "request_status", "probe_verdict")` (its `== 'survived'`). `probe_proved` and the
   other produce sites hold none (t-1103: 0 for the window producers). By measurement; the comment line names each item. Any counted
   comparison at `probe_proved` or a NOT ALLOWED line is a stop and a question.

architecture content: `AR-13 -- the intended_failure close/repeat word is read only through proof_level.probe_proved
(gate_template.acceptable); the defect words through one registered validate helper`; `AR-15 -- one helper per reading for the five
readers`; `AR-22 -- the product-record and window-block producers are registered produce in probe_verdict`; `AR-28 -- an absent, unknown
or other word, a non-record, or an unreadable registry never answers a repeat by a proved probe or closes a probe`; `AR-29 -- xref,
owner data, no census unit`; `AR-20 -- D13 re-measured and named`; judgment `none -- a join of a recorded probe word to the registry row;
the probe's verdict stays the probe judge's`.

Edges:
- E1 POSITIONAL (P1): `probe_proved(behind)` replaces only the verdict conjunct inside `own = (...)`; the receipt-path conditions follow
  unchanged. INVARIANT: a record that is not the receipt's own proved probe never vouches for what the receipt mutated.
- E2 POSITIONAL (P3): the first conjunct after `record is not None`, before the identity predicate and `_mutated_files_hold`. INVARIANT
  (C3-b2 E2): a record that does not say `intended_failure` is never asked about identity.
- E3 POSITIONAL (P4): the first disjunct of the `sensitivity:` condition, before `_bound_to`. INVARIANT: a probe block that does not say
  `intended_failure` is a `sensitivity:` gap whatever its other fields say.
- E4 (error direction of the predicate serving three producers): `acceptable` errs toward False. A product or window word outside
  `words` (`probe_defect`, `partial_product`, `model_changed`) -> False, exactly as `!= "intended_failure"` today; `survived` is now a
  word of class `mismatched` -> never acceptable. INVARIANT: only `intended_failure`, exact case, from a dict's `verdict`, on a readable
  registry, is a proved probe.
- E5 (P2, P5, F-5): the literals keep their meaning and position (first conjunct, then the identity predicate). Permitted error of a wrong
  True: a repeated probe is refused with the prior defect verdict shown (a person's word passes it) — never a pass. INVARIANT: a defect
  record answers a repeat only over the same test bytes, and each record kind answers only with the words its producer writes.
- E6 (unreadable registry): P1 -> `own = None` (a receipt with no carried mutated file does not block: the probe runs); P3 -> the loop
  continues, None (the probe runs); P4 -> `sensitivity:`; P2/P5 unaffected (no predicate; the identity predicate after them is False on
  an unreadable registry, so they answer nothing either). Behind C3-reg-precondition. INVARIANT: a broken registry never answers a repeat
  and never closes a window's probe.
- E7 (absent / None / non-record): no `verdict`, a `None` record (`_read_record` returns None for an unreadable file), a str or list ->
  False at every site. INVARIANT: no word, no proof.
- E8 TEMPORAL: records written before are read exactly as today on a readable registry (word-for-word, E4/E5). INVARIANT: no recorded
  verdict changes meaning.
- E9 TEXT: no text changes (`prior_verdict` values, `_repeat_words`, the `sensitivity:` gap line).
- E10 (bare str at P4): an item whose `probe` is a str crashed at `.get` before; now the first disjunct is True and the gap is
  `sensitivity:` (the later `probe.get("obligation_ids")` of the schema-2 block is not this card's; noticed, §8).
- E11 (limit): none introduced.

### RD1-29 — the critic's review word at every reader, one builder of the static-review note (critic t-1084 fix 3 (c); former RD1-29b folded)

The plan critic t-1103 judged F-6 (b) right with fix 11; this card applies it. No second plan-critic pass is owed unless the Lead takes
a non-recommended option of F-r2-2 / F-r2-3.

given:
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/design/factory-rules.md` (whole), `C:/QAFactory/forge-repo/plans/builder-rules.md`, `C:/QAFactory/forge-repo/docs/TESTING.md`
- this card, §0 facts 2-6, §1, §3, §4, S-a..S-f and C3-d (pattern, phase-2 spec :1029-1162)
- read under `<PKG>/`: `references/gate-registry.json` row `s5_window` (:245-270); `scripts/case_stamp.py:315-345`; `scripts/report_facts.py:63, 1507-1550`; `scripts/check_delivery.py:829-898, 2610-2625`; `scripts/handoff_check.py:949-976, 2023-2045`; `scripts/window_record.py:318-330, 1637-1652, 1732-1751, 2263-2280`; `scripts/acceptance.py:1150-1176` (the review branch the notes mirror); `scripts/traceability.py:874-892`; `scripts/factory_dashboard.py:872-893`; `scripts/ledger.py:1027-1042, 1183-1195`; `scripts/contract.py:2209-2215`; `handoffs/s4-case-critic-to-designer.yaml:59-70`; `handoffs/vocabulary.yaml:119`; `scripts/gate_template.py`; `scripts/tests/test_case_stamp.py:160-215`; `scripts/tests/test_check_delivery.py:1100-1115`; `scripts/tests/test_report_facts.py:400-420`; `scripts/tests/test_window_record.py:2821-2869` and its build-driven `probe_gap` tests; `scripts/tests/test_handoff.py:2647-2690`; `scripts/tests/test_probe_marker_judgment.py:428-436`; `scripts/tests/test_gate_registry.py` (D13, the RD1-27 table)
owns:
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/references/gate-registry.json` (row `s5_window` only: `decides`, `words`, `verdict_map`, `accepts`, `sites`)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/case_stamp.py` (`APPROVING` and its comment deleted; `instance_hold`: the last line and the docstring line `not_approved`; the import)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/report_facts.py` (`APPROVING` :63 deleted; `_tests` :1536; the import)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/check_delivery.py` (`lifecycle_reasons` and one module tail constant; the import)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/handoff_check.py` (`_claim_rollcall` and one module tail constant; its `import report_facts` line)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/window_record.py` (`build`: the review-note code :1637-1650 and :1740-1751; new `_static_review_note`, new `_review_note`, one module tail constant; `_sent_back_lines`: the `rejected` line :2267-2268)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/traceability.py` (`_review_basis`: the condition :884 and its point-of-use import)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/factory_dashboard.py` (`instance_basis`: the condition :887 and its point-of-use import)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/ledger.py` (the membership test :1191 only)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_case_stamp.py` (rows of the `instance_hold` table :166-178; the twin pin :211 replaced)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_check_delivery.py` (rows beside the A-K5 rows)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_report_facts.py` (rows :407-418)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_window_record.py` (`c3_d_review_word_through_the_registry`: a second check per row; one variant in a build-driven `probe_gap` test)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_handoff.py` (checks in `rollcall_the_claim_checks_the_ceiling_and_the_forms_n_of_m`)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_probe_marker_judgment.py` (one check in the `_sent_back_lines` test :428-436)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_gate_registry.py` (D13 pins; three RD1-27 rows)
non-goals: `acceptance.validate_window` (C3-d's; its three consumers and tokens unchanged); `ledger.is_rejected` (kept as THE reader of `rejected`); `critic_rollcall.APPROVING_VERDICTS` and its readers (`controller.py`, `driver_stage_plan.py`: the S4 roll-call vocabulary `approve*`); `validate_artifacts.py` (the four `fix_notes` shape lines); `GAP_ORIGIN` / `ORIGIN` texts; `case_stamp.HOLDS` words; the quarantined display tests (`test_traceability_report.py`, `test_factory_dashboard_joins.py`: named, not edited); census
handoff: report path given by the Lead
edges: E1-E14 below
DoD: `python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/gate_registry.py --check` (exit 0; no F-b; `s5_window` converted) and `python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for C:/QAFactory/forge-repo/ai-packages/qa-factory/references/gate-registry.json C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/case_stamp.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/report_facts.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/check_delivery.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/handoff_check.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/window_record.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/traceability.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/factory_dashboard.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/ledger.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_case_stamp.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_check_delivery.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_report_facts.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_window_record.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_handoff.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_probe_marker_judgment.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_gate_registry.py` and the printed non-slow files; slow files: canon; plus the AR-1 Grep of §1 (its output in the report)
siblings: axis 5 (grep `approved_with_fixes` over `references/code-review-rubric.md`, `skills/qa-story/phases/s5.md`, `s8.md`, `handoffs/s5-critic-to-automator.yaml`, each hit "checked, no edit"); axis 34 (one row and one predicate for the critic's word at every stage and every reader; no language/project key)
designer: `C:/QAFactory/forge-repo/docs/tasks/specs/20261117-rules-debt-c3-fix-conversions-cards-r2.md` (RD1-29)

Sites:

| # | site | current | after |
|---|---|---|---|
| W1 | `case_stamp.instance_hold:344` | `"" if entry.get("critic_verdict") in APPROVING else NOT_APPROVED` | `"" if acceptable(entry.get("critic_verdict"), "s5_window.stamp") else NOT_APPROVED` |
| W2 | `report_facts._tests:1536` | `verdict not in APPROVING` | `not acceptable(verdict, "s5_window.proven")` |
| W3 | `check_delivery.lifecycle_reasons:860` | `if verdict not in ("approved", "approved_with_fixes") and not green: continue` | item 3 |
| W4 | `handoff_check._claim_rollcall:966` | `if outcome in report_facts.APPROVING and found["verdict_ceiling"] == "partial":` | item 4 |
| W5 | `window_record.build:1641`, `:1742` | `!= BLOCKED_REVIEW_VERDICT` + two near-identical f-string notes | item 5 |
| W6 | `window_record.build:1649` | `elif item["review"]["verdict"] != "approved":` | item 5 |
| W7 | `traceability._review_basis:884` | `if verdict not in ("approved", "approved_with_fixes"):` | `if not acceptable(verdict, "s5_window.shown"):` |
| W8 | `factory_dashboard.instance_basis:887` | `if verdict not in ("approved", "approved_with_fixes"):` | `if not acceptable(verdict, "s5_window.shown"):` |
| W9 | `ledger.py:1191` | `if review not in {"approved", "approved_with_fixes", UNVERIFIED}:` | `if review not in C.CRITIC_VERDICTS:` |
| W10 | `window_record._sent_back_lines:2268` | `... and i["review"].get("verdict") == "rejected"` | item 7 (fork F-r2-3, recommended (a)) |

Items:
1. **Registry, row `s5_window`** (F-6 (b), fix 11).
   - `words` -> `["approved", "approved_with_fixes", "unverified"]`; `verdict_map` gains `"approved_with_fixes": {"class":
     "not_applicable", "reason_code": "with_fixes"}`. The three window consumers are unchanged, so `approved_with_fixes` stays a review gap
     at the window.
   - `accepts` gains `"s5_window.stamp"`, `"s5_window.proven"`, `"s5_window.lifecycle"`, `"s5_window.shown"`,
     `"s5_window.form_outcome"`, each `["matched", "not_applicable:with_fixes"]`.
   - `sites` gains, each `"role": "accept"`: `case_stamp.py:instance_hold`, `report_facts.py:_tests`, `check_delivery.py:lifecycle_reasons`,
     `handoff_check.py:_claim_rollcall`, `traceability.py:_review_basis`, `factory_dashboard.py:instance_basis`, `window_record.py:_review_note`
     (it calls `acceptable`). `window_record.py:build` stays `produce`. None of these names is registered by another row (Grep, 0 hits,
     control as in RD1-26 item 1); if A26 keys the method `_review_basis` otherwise, `--sites` says so and the entry follows the scanner.
   - `decides` gains, appended: "Outside the window the same word approves a test: `approved` or `approved_with_fixes` (class
     `not_applicable:with_fixes`, so the window's consumers never take it). Its consumers, each with its stage and producer: `stamp`
     (`case_stamp.instance_hold`, the case's Automated stamp), `proven` (`report_facts._tests`, the S9 report's proven count),
     `lifecycle` (`check_delivery.lifecycle_reasons`, gate B's lifecycle demand) and `shown` (`traceability._review_basis`,
     `factory_dashboard.instance_basis`, the review basis shown in the report and the dashboard) read the S5 code critic's manifest
     `critic_verdict`; `form_outcome` (`handoff_check._claim_rollcall`) reads the S4 case critic's form `review.outcome`, the same
     vocabulary (`vocabulary.critic_verdicts`), which the handoff checks by its own vocabulary. A site where an approving word triggers a
     further check (lifecycle, form_outcome) names an unreadable registry instead of reading it as not approving. `rejected` is not a word
     of this row (outside it, it closes nothing); its one reader is `ledger.is_rejected`, a routing reader — the ledger's `review_rejected`
     state and the window's send-back (`window_record._sent_back_lines`), which never accepts a window."
   - `addressee` unchanged (fork F-r2-2, recommended (b), with the reason in that fork). `unknown_branch`, `waits_at`, status unchanged.
   expected from: `contract.py:2209-2215`, `case_stamp.py:315-316`, C3-d item 3.
2. **W1, W2, W7, W8, W9.** As in the table. `from gate_template import acceptable` at the import block (case_stamp, report_facts) or at
   the point of use beside the existing `import ledger as L` / `import proof_level as PL` (traceability, factory_dashboard). `APPROVING`
   is deleted from both modules with its comment; `instance_hold`'s docstring line reads "`not_approved` the critic's verdict is not one
   the registry row `s5_window` approves for the stamp". W9: `C` is `contract` (`ledger.py:26`); equivalent because `review` is stripped
   (`verdict_of`) and `rejected` returned at :1189 (t-1103 key 4); `UNVERIFIED` stays (used elsewhere in the file; the builder greps).
3. **W3 `lifecycle_reasons`** (fix 4). Before the loop `problem = registry_problem()` and `unjudged = False`. In the loop:
   `approving = acceptable(verdict, "s5_window.lifecycle")`; `if not approving and not green:` -> `if problem and verdict: unjudged =
   True`; `continue`. Everything after is unchanged (green tests, `is_unverified`, handed, pinned, held, stamp). After the existing
   `if undecided:` line: `if unjudged: reasons.append(<family builder>(problem, WHY_LIFECYCLE_REGISTRY_TAIL))` with
   `WHY_LIFECYCLE_REGISTRY_TAIL = "whether an approved test that is not green owes its case's Automated stamp was not checked"`. The
   reason is owned `factory_record` like every line of this function (`check_delivery.py:2619`), FR-46 holds.
4. **W4 `_claim_rollcall`** (fix 3). After `found is None` and `outcome = ...`: the outcome test reads `acceptable(outcome,
   "s5_window.form_outcome") and found["verdict_ceiling"] == "partial"` (on an unreadable registry `acceptable` is False, so this
   refusal is skipped — the only thing skipped). The placeholder check and the digest check follow unchanged (a digest mismatch is still
   `False`). The final `return (True, ...)` is preceded by: `if found["verdict_ceiling"] == "partial" and registry_problem(): return
   (None, <family builder>(registry_problem(), WHY_ROLLCALL_REGISTRY_TAIL))` with `WHY_ROLLCALL_REGISTRY_TAIL = "whether the form's
   outcome approves over a partial roll-call was not judged"`. A ceiling that is not partial needs no word: `True` stays. `import
   report_facts` (:958) is deleted when no other use remains in the function (the builder greps); never left as an unused import.
5. **W5, W6 window notes** (F-8 (a), fix 5).
   - `_static_review_note(said, why) -> str` returns exactly `(f"the manifest row's `critic_verdict` is `{said}`" if said else "the
     manifest row carries no `critic_verdict`") + f", and {why}; the verdict of such an instance is `{BLOCKED_REVIEW_VERDICT}` (a static
     review): the critic records it through `manifest_put.py`"`, with `why` = `"this instance was blocked by the stand"` (stopped) and
     `"this instance's probe could not run here (a person's word or the factory names it)"` (gapped) — both BYTE-IDENTICAL to today's
     :1644-1648 and :1747-1751 (the builder diffs old/new outputs over `said in ("approved", "approved_with_fixes", "rejected", "", None)`).
   - `_review_note(kind, said) -> str | None`, `kind` in `stopped`, `gapped`, `handed`, `ran`; the consumer per kind mirrors
     `validate_window` (:1156-1176): stopped, gapped -> `s5_window.static_review`; handed -> `s5_window.handed_review`; ran ->
     `s5_window.review`. `None` when `acceptable(said, consumer)`; otherwise, when `registry_problem()` is non-empty, the family builder's
     sentence for it and `WHY_REVIEW_REGISTRY_TAIL = "whether the critic's review word closes this instance's review was not judged"`;
     otherwise `_static_review_note(said, why)` for stopped / gapped and `_origin_text("review")` for handed / ran.
   - **Kind derivation in `build`** (stated, fix 5): at :1637, `stopped` (= `identity in blocked`, exactly when build writes
     `BLOCKED_OUTCOME`) -> kind `stopped`; else kind `handed` when `identity in handed_ok and not runs.get(identity)` (exactly when build
     writes `HANDED_OUTCOME`: stopped is excluded, a run outranks), else `ran`; `note = _review_note(kind, item["review"]["verdict"])`,
     appended as `(identity, "review", note)` when not None (replaces :1641-1650). At the probe gap (:1740-1751): when `gap` is set, the
     earlier `review` notes of this identity are removed UNCONDITIONALLY, then `_review_note("gapped", said)` is appended when not None
     (the removal was conditional before; with it unconditional a gapped `unverified` instance no longer keeps the generic note that
     claimed a gap validate_window does not raise). Where build's kinds and validate_window's can still differ: validate_window confirms
     the stopped and handed claims through its readers (`blocked_instances`, `handed_instances`) and asks `proof_required(item, {})`
     where build asked `proof_required(entry, manifest)`. INVARIANT: on the item build writes, for a claim validate_window confirms, build
     writes a `review` note exactly when validate_window raises `review:<iid>`; a divergence a table row finds is a stop and a question.
6. **Tests** (rows, never a new file):
   - `test_case_stamp.py` table :166-178 (`instance_hold`): + `unverified`, `rejected`, `""`, `"Approved"`, `None`, no key ->
     `not_approved`; `approved` with the registry unreadable (`gate_template._READ` swapped, restored in `finally`) -> `not_approved`. The
     `approved_with_fixes` row (:178) stays. The twin pin :211 (`S.APPROVING == RF.APPROVING`) is replaced by one row: for every word of
     `contract.CRITIC_VERDICTS` plus `""`, `"Approved"`, `" approved"`, `None`: `acceptable(w, c)` is equal for c in `stamp`, `proven`,
     `lifecycle`, `shown`, `form_outcome`, and True exactly for `approved`, `approved_with_fixes` (the drift the pin guarded, now held by
     data across every outside reader).
   - `test_check_delivery.py` (beside the A-K5 rows): readable: `rejected`, not green -> no lifecycle reason. Unreadable registry:
     (a) an approved non-green test -> exactly one reason holding the family head (`the gate registry cannot be read`) and no per-case
     reason for it; (b) an approved GREEN test whose case lacks the stamp -> its per-case stamp reason is still produced and no registry
     line (the demand that does not depend on the word is kept); (c) both together -> the per-case reason of (b) and the one line of (a).
   - `test_report_facts.py` (:407-418): + an `unverified` and a `rejected` green row -> not counted as proven; the `approved_with_fixes`
     row stays counted; an `approved` green row with the registry unreadable -> not counted (the W2 residue, E12).
   - `test_window_record.py`, `c3_d_review_word_through_the_registry`: after its loops, a second check per row:
     `(WR._review_note(kind, None if word is absent else word) is not None) == gap` (same rows); and for every row with the registry
     unreadable, the note is not None and holds `the gate registry cannot be read` and not `is \`unverified\``. One variant in a
     build-driven `probe_gap` test of the file (the builder greps `probe_gap`; 9 hits on the wave tree): a gapped instance whose verdict
     is `unverified` -> no `review` note in `build`'s notes; none drivable -> a stop and a question.
   - `test_handoff.py`, `rollcall_the_claim_checks_the_ceiling_and_the_forms_n_of_m` (its `_verify(ROLLCALL_CLAIM, ...)` form): readable:
     `approved_with_fixes` + partial -> False with the ceiling text; `rejected` + partial + digest `1 of 2 reviewed` -> True. Unreadable
     registry (`GT._READ` swap in `finally`): `approved` + partial + `1 of 2 reviewed` -> `(None, <holds the family head>)`;
     `approved` + partial + `2 of 2 reviewed` -> `(False, "the form says 2 of 2 reviewed, critic_rollcall computes 1 of 2 reviewed")`;
     `approved` + full roll-call + `2 of 2 reviewed` -> True; `approved` + partial, digest not filled -> `(None, "review.rollcall is not filled")`.
   - `test_probe_marker_judgment.py` (the `_sent_back_lines` test): + one check: an instance whose review verdict is `" rejected "` is
     sent back like `rejected` (the reading `ledger.is_rejected` gives; E13).
   - Display sites W7/W8: their behaviour rows live only in quarantined files (`test_traceability_report.py:249`,
     `test_factory_dashboard_joins.py:199`, named, not edited); the data row above (`shown` == `stamp`) is this card's pin. W9: the
     `review_unrecognised` rows of `test_ledger.py` (named, not edited) pin the unchanged behaviour.
   - **RD1-27 rows** (`test_gate_registry.py`): three rows, the family builder over `"R"` and `WHY_LIFECYCLE_REGISTRY_TAIL`,
     `WHY_ROLLCALL_REGISTRY_TAIL`, `WHY_REVIEW_REGISTRY_TAIL`, each expected `"the gate registry cannot be read (R): a factory defect, <tail>"`.
   Expected from: `decides` (item 1), `contract.py:2209-2215`, FR-59, the functions' documented error directions — never from outputs
   before the change.
7. **W10 `_sent_back_lines`** (fork F-r2-3 (a)): the set reads `L.is_rejected({"critic_verdict": i["review"].get("verdict")})` with
   `import ledger as L` at the point of use (window_record does not import ledger at module level; a point-of-use import avoids a cycle).
   The literal `"rejected"` leaves `window_record.py`.
8. **Pins (S-f).** No status moves; split, `EXPECTED_*` and F4 do not move (t-1103 key 3). D13 re-measured: expected (t-1103) -1 item /
   -1 triple (`("window_record.py", "build", "s5_window")` leaves); the new accept sites are expected to hold no counted comparison (by
   measurement; any counted comparison at a new accept site is a stop and a question). The allow-list pin does not move. The RD1-27
   table gains the three rows of item 6.

architecture content: `AR-1 -- the approving pair leaves code at every reader: the row s5_window holds which word approves where`;
`AR-13 -- the critic's review word is read through gate_template.acceptable at the stamp, the proven count, the lifecycle check, the form
check, the two displays and the window notes`; `AR-15 -- one builder of the review note; one reader of rejected`; `AR-22 -- APPROVING and
every reader change in one commit`; `AR-28 -- an absent or unknown word holds the stamp and the count; an unreadable registry is named
where an approving word triggers a check, and the digest refusal is kept`; `AR-29 -- xref, owner data, no census unit`; `AR-20 -- D13
and the RD1-27 table re-measured, the build triple's move named`; judgment `none -- the critics' verdicts stay their judgment; the registry
carries which word approves where`.

Edges:
- E1 (readable registry): every word -> the same outcome as today at W1-W4, W7-W9 (`approved`, `approved_with_fixes` approve; `unverified`,
  `rejected`, `""`, None, case variants, non-str do not; t-1103 consumer tables). At the window nothing changes (C3-d rows unchanged).
  INVARIANT: no test is stamped, counted, shown as approved or spared a check that is not today, and none is held that is not today.
- E2 (error direction, W1/W2 — gate role): False = hold / not counted: safe. INVARIANT: an unknown word never stamps a case or counts a
  test as proven.
- E3 (error direction, W3/W4 — False is the UNSAFE side): W3 sets the flag and names the registry once; W4 skips only the outcome
  refusal and keeps the digest refusal, then answers `None` naming the registry where the word would decide. Adversarial inputs: an
  unreadable registry (pinned); a registry that reads but lacks the consumer (`registry_problem()` "" -> `acceptable` False -> W3 skips an
  approved non-green test, W4 no ceiling refusal) — held by CI: A26 F-b/F-f and the positive rows of each table turn red on a consumer
  typo (C3-reg E2 precedent). INVARIANT: a broken registry never removes a lifecycle demand or a form refusal silently.
- E4 POSITIONAL (W3): the flag is set inside the loop at the `continue` that the word decides; the line is appended after the
  `undecided` line. INVARIANT: every demand that does not depend on the word (green tests, `_pinned_proof_reasons`, the `not_read` line)
  is still produced.
- E5 POSITIONAL (W4): after `doc is None` and `found is None`; the registry `None` only replaces the final `True`. INVARIANT: a missing
  form or roll-call keeps its own `None` text; a digest the form misstates is `False` with or without the registry.
- E6 POSITIONAL (W5/W6): the stopped / generic note at :1637, the gapped override at the probe gap (removal first, then the note).
  INVARIANT: build's note and validate_window's gap agree per kind (item 5).
- E7 TEXT: byte-identical on a readable registry: the two static notes, `GAP_ORIGIN["review"]`, `NOT_APPROVED`, every existing reason of
  `lifecycle_reasons`, every claim text of `_claim_rollcall`, the display strings of W7/W8. New texts: the three family sentences only.
- E8 (unreadable registry, notes; fix 5): every note says the registry could not be read — never "the verdict is `unverified` … such an
  instance's verdict is `unverified`" for an `unverified` instance, never "is not `approved`" for an `approved` one. INVARIANT: FR-10,
  FR-41 — no note contradicts the instance.
- E9 TEMPORAL: manifests and windows recorded before are read word for word as today. INVARIANT: no recorded verdict changes meaning.
- E10 (absent / empty): `critic_verdict` absent -> `""`/None -> not approving (W1, W2, W7, W8), W3 skips a non-green row as today and
  sets no flag (an empty word decides nothing). INVARIANT: no word, no approval.
- E11 (P31 / one road): every reader of "does this critic word approve" goes through the same row, and the one reader of `rejected` is
  `ledger.is_rejected`. INVARIANT: no literal copy of the pair survives in `scripts/*.py` (AR-1 Grep in the DoD).
- E12 (residues, FR-41, fix 12): on an unreadable registry (a) the stamp's hold word is `not_approved` (a false cause; `HOLDS` not
  extended here), (b) the report counts an approved green test as not proven with no cause shown, (c) the displays drop the proof
  suffix (they still say only what the critic said). Each is behind C3-reg-precondition (no new stage on an unreadable registry) and each
  is pinned by a row; none prints an unknown as a fact.
- E13 (W10): `ledger.is_rejected` strips (`verdict_of`): a window verdict `" rejected "` now sends the window back instead of listing a
  `review:` gap. Both roads refuse the window ("this branch never returns 0", `window_record.py:2360`); the window now agrees with the
  ledger, which already reads it as rejected. INVARIANT: the send-back never accepts a window.
- E14 (limit): none introduced.

---

## §3. Measured premises (commands; nothing was run here)

- D13 before/after: `python -B -c "import sys; sys.path.insert(0, r'C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts'); import gate_registry as GR; r = GR.analyse(); t = sorted({(i['file'], i['function'], x) for i in r['items'] for x in i['rows']}); print(len(r['items']), len(t)); [print(x) for x in t]"`
  (t-1103 on the wave tree: 150 items / 53 triples, the pin agrees. Expected after all three cards, summing the per-card expectations
  above: 150 + 4 + 3 - 1 = 156 items, 53 + 1 + 2 - 1 = 55 triples — an estimate, not verified; by measurement, never copied).
- Sites and allow texts: `python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/gate_registry.py --sites`.
- Behaviour preservation (RD1-26, RD1-28 P4, RD1-29 W5/W6): `python -B -c "import json,glob,sys; sys.path.insert(0, r'C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts'); import acceptance as A; [print(p, A.validate_window(json.load(open(p, encoding='utf-8')), p.split('work')[0])) for p in glob.glob(r'C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/fixtures/stories/*/work/windows/*.json')]"`
  before/after equal (a smoke: t-1103 EQUAL on the simulated cards).
- RD1-29 word census: Grep `approved_with_fixes` over `<PKG>/scripts/*.py` (wave tree, round 1: `case_stamp.py:28,315,317`,
  `check_delivery.py:860`, `factory_dashboard.py:887`, `ledger.py:1191`, `report_facts.py:63`, `traceability.py:884`,
  `validate_artifacts.py` (4 lines), `contract.py:2209,2212`, `critic_rollcall.py:18`, `check_coverage.py:137` comment).

## §4. Order, parallelism, collisions (fix 13; brief: one order with wave 3)

**Builders.** Two nodes (F-9 (a)): ONE builder for RD1-26 + RD1-28 (they share the C3-b2 table function in `test_proof_level.py` and
`acceptance.py`, function-disjoint), and one for RD1-29. Both start from main after the C3 wave merge.

**Shared files of the three cards** (fix 13): `gate-registry.json` (row-disjoint: `test_identity` / `probe_verdict` / `s5_window`);
`test_gate_registry.py` (the D13 count and triples in all three, the allow-list pin in RD1-26 only, the RD1-27 table in RD1-26 (one row)
and RD1-29 (three rows)); `test_window_record.py` (RD1-28: a new function; RD1-29: `c3_d_review_word_through_the_registry` and one
build-driven variant — function-disjoint as long as RD1-28's rows stay out of the C3-d function). PROJECT.md «Командная работа» п. 3
allows this: the later merger merges main into its tree, keeps both sides' rows and re-measures every count (D-0048); no number is
resolved by keeping either side.

**With wave 3** (owns lines read: g-h r2 :194-198, :518-522, :677-679; k r2 :370-374, :451-459, :575-585, :713-722):
- Production files: none shared. C3 fix: `acceptance`, `run_history`, `proof_level`, `window_record`, `case_stamp`, `report_facts`,
  `check_delivery`, `handoff_check`, `traceability`, `factory_dashboard`, `ledger`. Wave 3: `baseline_contract`, `controller` (C3-g2,
  HOT), `delivery_summary`, `profile_contract`, `execution_request`, `execution_fingerprint`, `run_suite`, `gate_preflight` (HOT),
  `manual_evidence`, `coverage_contract`, `manual_capture`, `environment_preparation`, `driver_stage_build`.
- Test files: none shared except `test_gate_registry.py` (wave 3: `test_baseline_contract`, `test_execution_request`,
  `test_gate_preflight`, `test_manual_evidence`, `test_manual_capture`, `test_environment_preparation`,
  `test_runtime_probe_onboarding`, `test_role_commands`; k4 also `judgment-census.json`, which no C3 fix card touches).
- `gate-registry.json`: row-disjoint with every wave-3 card (C3-g `baseline_identity`, C3-h `stand_identity`, k1-k4
  `provenance_acceptance`, k3 also `environment_preparation`). Separate rows are separate text hunks.
- `test_gate_registry.py` statements several streams rewrite: `D13_ITEM_COUNT` and its comment and the D13 triple set (every card);
  the exact allow-list pin (RD1-26; k2, k3, k4); the RD1-27 table (RD1-26, RD1-29; C3-g "one RD1-27 row if that table is on the base");
  `EXPECTED_*`, split, F4, K-T1.2 NEG, K-N2.12 (wave 3 only — F-6 (b) moves none of them).

**One merge order for the two shared files** (recommended; the builders may run in parallel because no production file is shared — only
the MERGE is serial, and each later merger re-derives the shared statements by measurement):
`C3-g -> RD1-26+28 -> RD1-29 -> C3-k1 -> C3-k2 -> C3-k3 -> C3-k4 -> C3-h`.
- C3-g first keeps the Lead's order of the k cards (§0.2 of the k r2 cards); C3-g2 touches neither shared file and is not in the line.
- The C3 fix cards next: they close the C3 fix topic before the long k chain and touch the allow-list pin only once (RD1-26), before
  k2-k4 re-derive it.
- RD1-26+28 before RD1-29: arbitrary (no file of theirs collides except the two shared ones and `test_window_record.py`, function-disjoint);
  this order puts the larger D13 delta first.
- k1 -> k4 stay serial among themselves (their own card: shared row `provenance_acceptance`). C3-h last (or before k1, row-disjoint, as
  the later merger — its own card).
- Truly parallel without any re-measure: none — every pair above shares at least `D13_ITEM_COUNT`. Parallel in code, serial in merge:
  all of them.

## §5. Forks

New forks of round 2 (each card is executable by the recommendation):

- **F-r2-1 (RD1-28, the class of `survived`)** — the critic names it a Lead decision (t-1103 key 4, fix 7); the brief folds RD1-28b in
  the critic's simulated form. (a) `survived` = `mismatched` — **rec**: `product_verdict`'s docstring calls it an invalid proof that is not
  the probe's defect and not unjudged — the broken product survived the test, a defect of the test, the twin of `no_failure`; the
  predicate never accepts it and `_probe_record_defect` reads it; (b) `unknown` (owner factory) — wrong: `survived` is a judged verdict on
  the test, and `unknown` would say a factory fault; (c) leave it outside `words` — A26 stays blind to the item-3 comparison, and the
  "word of no row" defect of round 1 stays open.
- **F-r2-2 (RD1-29, `addressee` of `s5_window`; fix 11's choice)** (a) add `role:qa-case-critic` — the row's question
  (`unknown_branch: question`, `waits_at: window_acceptance`, `closed_by` the S5 code critic or the person) would name an addressee that
  is never asked there; (b) keep `addressee` and say why in `decides` — **rec**: the `form_outcome` consumer has no unknown branch of
  this row: an S4 `review.outcome` outside `vocabulary.critic_verdicts` is refused by the handoff's own vocabulary check
  (`handoffs/vocabulary.yaml:119`, `test_handoff.py:93-107`), and a word the row does not approve only withholds the ceiling refusal.
  Under (b) item 1's `decides` sentence already says "which the handoff checks by its own vocabulary". Cost of (a): a data line
  that contradicts `waits_at`; cost of (b): none beyond the sentence.
- **F-r2-3 (RD1-29, `_sent_back_lines`; t-1103 key 4's choice)** (a) read through `ledger.is_rejected` — **rec** (one reader of
  `rejected`, P31; the window agrees with the ledger on a whitespace-padded word; both outcomes refuse the window, E13); (b) keep
  `== "rejected"` and one `decides` sentence calling it a routing reader — cheaper, but a second road for the same word and a
  disagreement with the ledger on `" rejected "`.

Round-1 forks, as decided (Lead 17.11.2026, with the verdict t-1103):

| fork | decision | applied in |
|---|---|---|
| F-1 | (a) both `run_history` sites are accept sites | RD1-26 S3, S4 |
| F-2 | **(c)**, flipped from (a) by the verdict (56 of 729 drops under (a)) | RD1-26 item 5, E4, rows v-vii |
| F-3 | (a) with fix 10 (the dict-shape pin) | RD1-26 item 3, E2 |
| F-4 | (a) with fix 6; RD1-28b folded (no residual) | RD1-28 items 1-3, 5 |
| F-5 | (a) | RD1-28 item 3, E5 |
| F-6 | (b) with fix 11 | RD1-29 item 1 |
| F-7 | folded: every reader in RD1-29 | RD1-29 W7-W10 |
| F-8 | (a) with fix 5 (derivation stated) | RD1-29 item 5 |
| F-9 | (a) with fix 13 and the wave-3 order | §4 |
| F-10 | done (the plan critic covered RD1-28's clause) | — |

## §6. Small technical choices closed (designer)

- Consumer names: `test_identity.proof_bound`, `.mechanical_raw`, `.param_twin`, `.pair_same`; `probe_verdict.proved`; `s5_window.stamp`,
  `.proven`, `.lifecycle`, `.shown` (one consumer for the two display sites: they show the same thing), `.form_outcome`.
- `_job_contract` as a plain loop (A26 keys sites by the outer `def`; a lambda would make attribution depend on the scanner's walk).
- `probe_proved` public (called from `acceptance.py`); `_probe_record_defect`, `_review_note`, `_static_review_note` private.
- `_probe_record_defect` takes `product=False` and keeps each producer's own words exactly (the critic simulated one tuple of three
  words; that would let a `probe_by_code` record answer by `survived` and a product record by `no_failure`, which no producer writes —
  harmless, but a widening E8 forbids). Cost: one more counted comparison, by measurement.
- Every registry tail is a module constant (`WHY_..._REGISTRY_TAIL`) so the RD1-27 row reads the site's own tail; the names may follow
  the base's naming at the build.
- The window notes: the kind decision is a pure helper (`_review_note`) so the C3-d table can check note-iff-gap row by row without
  driving `build`; `build` keeps the two note positions (no reordering of the notes list).
- W4: the registry `None` only when the ceiling is partial (elsewhere the word decides nothing and `True` is honest).
- W3: the flag only for a non-empty word (an empty word approves nothing on any registry).
- Tests: rows in existing keep tables only; one new parameterised function in `test_window_record.py` for P4 (a keep file); no new test file.

## §7. Readers of every touched file (designer rule 7)

Commands (Grep tool, content mode):
- over `C:/QAFactory/forge-repo/tools`, round 1 pattern `gate-registry\.json|test_gate_registry|acceptance\.py|run_history\.py|proof_level\.py|window_record\.py|case_stamp\.py|report_facts\.py|check_delivery\.py|test_proof_level|test_window_record|test_case_stamp|test_check_delivery|test_report_facts|APPROVING|GAP_ORIGIN|_bound_to` -> 28 hits in 7 files (round 1, not re-run);
- over `C:/QAFactory/forge-repo/tools`, round 2 pattern `traceability\.py|factory_dashboard\.py|ledger\.py|handoff_check\.py|test_handoff\.py|is_rejected|_sent_back_lines|probe_proved|_review_note` -> 27 lines in 8 files (`dup-baseline.json` 1, `lint-baseline.json` 4, `piles_testkit.py` 1, `test_piles_split.py` 6, `test_collect_intake.py` 10, `test_ci_read.py` 1 (a test name with `is_rejected` inside a longer word), `fixtures/dispatch_manifest/K1.txt` 3, `K3.txt` 1);
- over `C:/QAFactory/forge-repo/.githooks`: the package file names -> 0 (positive control `\.py`: 20 hits in 5 files);
- over `C:/QAFactory/forge-repo/.claude/agents`: the package file names -> 0 (control `critic-diff-brief|builder-rules`: 7 hits);
- over `C:/QAFactory/forge-repo/.claude/settings.json`: the package file names -> 0 (control `tools/`: 37 hits).

| reader | reads | verdict |
|---|---|---|
| `tools/source-split-carriers.json:15, 25` | `gate-registry.json`, `test_gate_registry.py` (D13 py-triple carrier) | unchanged: the triple form `(file, function, row)` is kept |
| `tools/source_split.py:2753-2891` | the same carriers (selftest fixtures) | unchanged |
| `tools/controller-blocks-gen.py:145, 186-194` | `window_record.py` door texts; the registry block prefix | unchanged (no CLI, door or `REGISTRY_BLOCK` use changes) |
| `tools/lint-baseline.json:43-59` | `factory_dashboard.py` `UnusedImport` (driver_journal) | unchanged: W8 adds a used point-of-use import |
| `tools/lint-baseline.json:193, 235, 253` | `test_check_delivery.py`, `test_handoff.py`, `test_report_facts.py` (`HandReaderInput`) | changes only if a new row adds a hand-read input; the count is a ratchet: a raise is a stop |
| `tools/dup-baseline.json:139` | `factory_dashboard._has_factory_activity` (clone) | unchanged (other function) |
| `tools/test_forge_metrics.py:253-257` | `check_delivery.py` as a file-index sample | unchanged |
| `tools/test_quarantine.py:2199` | `gate-registry.json` as a prose carrier path | unchanged |
| `tools/piles_testkit.py:54`, `tools/test_piles_split.py`, `tools/test_collect_intake.py` | `traceability.py` as a path string in fixtures | unchanged |
| `tools/test_ci_read.py:566` | the substring only (a test name) | unchanged |
| `tools/fixtures/dispatch_manifest/K1.txt`, `K3.txt`, `K8.txt` | fixture texts naming the files | unchanged |
| package readers (load-bearing, not rule-7 scope) | `case_stamp.APPROVING` <- `instance_hold`, `test_case_stamp.py:211`; `report_facts.APPROVING` <- `_tests`, `handoff_check._claim_rollcall`, `test_case_stamp.py:211`; `_bound_to` <- `validate_window`, `test_receipts_per_function.py:30` (quarantined; name and signature unchanged); `ledger.is_rejected` <- ledger, now also `_sent_back_lines`; `proof_level.probe_proved` <- `acceptance.validate_window` (new) | APPROVING readers all in RD1-29's owns; the rest unchanged |

Streams meet at `test_gate_registry.py` and `gate-registry.json` (§4).

## §8. Noticed analogs (reported; scope not widened)

- `probe_verdict` words read by state readers with no registration: `proof_level.tooling_gap_key`, `probe_record_state`
  (`PROBE_JUDGED_VERDICTS`), and the `probe_by_code` readers the row calls "not sites yet". State readers, not acceptances — another
  pile's queue line (offered to the Lead, not filed here).
- `critic_rollcall.APPROVING_VERDICTS` (`approve`, `approve_with_fixes`, `approve_with_concerns`) at `controller.py`,
  `driver_stage_plan.py`: the S4 roll-call row vocabulary, no registry row.
- `validate_window`'s schema-2 block calls `probe.get(...)` on the item's `probe` (`acceptance.py:1238`): a non-dict `probe` would still
  raise there after P4 stops raising (RD1-28 E10). C3-d's function, not this card's.

## §9. Every fix and brief decision -> where applied

| # | fix (t-1103) / decision (brief) | where applied |
|---|---|---|
| 1 | RD1-26 item 5 / E4 / F-2: take (c), rows v-vi, verbatim allow entries, D13 by measurement | RD1-26 item 5 (guard, allow entries, rows i-vii), item 6, E4, E5; §5 table F-2 |
| 2 | every registry sentence through the family builder; RD1-27 rows; §6 stale line removed | §0.5; RD1-26 item 3 (+ RD1-27 row); RD1-29 items 3, 4, 5 and item 6 (three RD1-27 rows); §6 (no "absorbs later" line) |
| 3 | RD1-29 W4: skip only the outcome test, keep the digest refusal, broken registry + wrong digest -> False | RD1-29 item 4, E3, E5, item 6 (test_handoff rows) |
| 4 | RD1-29 W3: fold per test, a flag, one line at the end; owner factory_record | RD1-29 item 3, E3, E4, item 6 (test_check_delivery rows a-c) |
| 5 | RD1-29 W5/W6: registry sentence on an unreadable registry; build's kind derivation stated | RD1-29 item 5 (`_review_note`, derivation, invariant), E6, E8, item 6 (C3-d second check, build variant) |
| 6 | RD1-28: dict guard + bare-str row; "one ACCEPTING reader" naming the display readers; producers registered `produce` | RD1-28 items 1, 2, 5, E7, E10; §0 fact 1; §1 AR-22 row |
| 7 | RD1-28b into RD1-28: `survived` mismatched (Lead), item 3 into `_probe_record_defect`, `request_status` produce | RD1-28 P5, items 1, 3, 5, 7; fork F-r2-1 |
| 8 | RD1-29b into RD1-29: display consumer, ledger membership, `_sent_back_lines` decided; `rejected` prose; AR-1 grep covers the pair | RD1-29 W7-W10, items 1, 2, 7, E11, E13; §1 AR-1 row; fork F-r2-3 |
| 9 | RD1-26 owns: the mechanical-round world, or rows stay in test_proof_level.py | RD1-26 item 3 (rows stay; the reason read at `test_blocked_by_env_window.py:627-631`); §0 fact 6 |
| 10 | RD1-26 E2: drop "pinned by row (ii)"; pin the dict displays | RD1-26 item 3 (dict-shape pin), E2 |
| 11 | RD1-29 item 1: `decides` names each consumer, stage and producer; addressee | RD1-29 item 1; fork F-r2-2 |
| 12 | RD1-29 E7: the W2 residue | RD1-29 E12 (b), item 6 (test_report_facts unreadable row) |
| 13 | shared files named; the later merger re-measures; RD1-28 window rows out of the C3-d function | §4; RD1-28 owns and item 6 |
| B1 | F-2 flips to (c); every input class of t-1103 stated; flipping cases are rows | RD1-26 item 5 rows v-vii, E4 |
| B2 | RD1-28b / RD1-29b folded, owns and rows grown, residual sections gone | RD1-28, RD1-29 owns/items; no residual section |
| B3 | W3, W4, W5/W6: keep the refusal, never print an unknown as a fact | fixes 3-5 above; RD1-29 E3, E8, E12 |
| B4 | "the family's builder as it stands on the base at the build; never a literal copy", no signature quoted | §0.5 and every registry item |
| B5 | other round-1 decisions stand (F-6 per the verdict) | §5 table |
| B6 | base after the C3 wave merge; shared files with the wave-3 cards; one serial order | header; §4 |
| B7 | function names, not line numbers, for `controller.py`, `gate_template.py`, `proof_level.py`, `execution_request.py` | RD1-28 sites P1-P3, P5 and given lines; RD1-26 given |
| B8 | §1 kept: AR-n, owner and census class per check, FR walk | §1 |

## §10. Not established

- Nothing was run: D13 deltas (the t-1103 numbers are a simulation of round-1 forms; this file's split and the extra sites move them),
  `--sites` texts, the window smoke, `test_judgment_census.py`, `test_handoff.py`'s `_verify` behaviour on a swapped `GT._READ` (the
  builder confirms the seam reaches `handoff_check`'s point-of-use `acceptable`).
- How A26 keys the method `traceability.<class>._review_basis` (by function name is expected; `--sites` decides).
- Whether `test_window_record.py` has a build-driven `probe_gap` world that can take the gapped-`unverified` variant (9 `probe_gap` hits;
  the builder reads them; none -> stop).
- The family builder's final shape after the RD1-27 fix round (§0.5: the cards do not depend on it).
- Grep of `.claude/hooks` for the package names was not run separately (the `.claude` tree scan hit the worktrees and stopped; estimate:
  none, as in round 1).

## §11. Reading trail

- Given: the round-1 cards file (whole, 605 lines, with the Lead decisions), the verdict t-1103 (whole).
- Wave-3: k r2 :1-66 and the owns lines (grep `^owns:|^- \`C:/QAFactory`); g-h r2 :23-59, :997-1005 and the owns lines.
- Wave tree `ai-packages/qa-factory/`: `scripts/gate_template.py` (whole, with the in-flight edits); `scripts/run_history.py:195-266,
  685-714` and imports; `scripts/acceptance.py:1-14, 128-217, 1140-1240`; `scripts/proof_level.py:1405-1580`; `scripts/red_sandbox.py:1470-1514`;
  `scripts/window_record.py:1615-1759, 2258-2282`, imports, grep of `intended_failure|_probe_scope_notes|...`; `scripts/check_delivery.py:826-907`,
  grep `lifecycle_reasons`; `scripts/handoff_check.py:940-981, 2018-2042`; `scripts/case_stamp.py:310-345`; `scripts/report_facts.py:58-67,
  1520-1547`; `scripts/traceability.py:872-893`; `scripts/factory_dashboard.py:874-895` and its def list; `scripts/ledger.py:1025-1043,
  1178-1197`, imports; `scripts/contract.py:2205-2216`; `handoffs/s4-case-critic-to-designer.yaml:55-79`; grep `critic_verdicts` over the
  package; `references/gate-registry.json:120-274, 586-615`, grep of every new site name (0) with control (3);
  `scripts/tests/test_gate_registry.py:1175-1200`, grep `RD1-27`; `scripts/tests/test_proof_level.py:1415-1446`, grep `def c3_`;
  `scripts/tests/test_window_record.py:2000-2029, 2821-2870`, grep `def c3_|sensitivity:`, count `probe_gap`;
  `scripts/tests/test_handoff.py:2610-2680`; `scripts/tests/test_blocked_by_env_window.py:590-649`; `scripts/tests/test_s5_process.py:280-337`;
  grep `green_on_current_bytes` (counts), `_sent_back_lines\(`, `_review_basis|instance_basis`, `review_unrecognised` (counts) under
  `scripts/tests/`; `scripts/tests/test-layers.json` rows :222, :437-458, :2300, :3892-3910, :4952, :9692 and the grep of 16 test-file keys;
  `scripts/tests/fixtures/judgment-census.json` grep of every touched function.
- Forge: `tools/dup-baseline.json:125-147`, `tools/lint-baseline.json:38-59, 228-239`; rule-7 greps of §7.

## §12. Lead decisions on the r2 forks (17.11.2026, Lead of the batch; by recommendation)

- F-r2-1 = (a): `survived` is class `mismatched` (a judged verdict on the test, the twin of `no_failure`).
- F-r2-2 = (b): `s5_window` keeps its `addressee`; the reason is written in `decides`.
- F-r2-3 = (a): `_sent_back_lines` reads through `ledger.is_rejected`.
- §9 checked against verdict t-1103 by the Lead: fixes 1-13 and brief decisions B1, B2 each have a place. No second plan-critic
  pass (the r2 changes apply the verdict; PROJECT.md, new idea, step 6).
- Dispatch: after the C3 wave branch merges, in the one serial order of §4.
