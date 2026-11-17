# Rules-debt wave 3 — header-ready cards C3-g (baseline_identity) and C3-h (stand_identity) (t-1085, F19)

Designer draft for the Lead. It turns the two sketches of `docs/tasks/specs/20261117-rules-debt-phase2-cards-spec.md`
(«#### C3-f … ; C3-g — baseline_identity (B-281)», :1258-1271, and «#### C3-h — stand_identity (B-257)», :1273-1283) into
builder cards in the form of C3-b2 (:918-1025), C3-d (:1029-1162) and C3-reg-precondition (:1164-1254). The cards spec
itself is not edited. Its shared items S-a..S-f (:278-346), the E-c table (:372-402) and the Lead decisions (:1873-1893,
:2161-2183, :2294-2348) apply to both cards as written.

Every load-bearing fact below was read today (17.11.2026) in the root checkout, `C:/QAFactory/forge-repo`, whose
`.git/HEAD` is `ref: refs/heads/main` (read directly). No shell was available, so nothing was RUN. Every run named below is
a command for the builder or the Lead.

## §0. State of main that the cards are based on (read today)

1. **C3-0 is on main.** `ai-packages/qa-factory/scripts/gate_template.py` exists (Glob `scripts/gate_*.py`: 5 files). It
   holds `_READ = []` (:31), `registry_problem(*, registry=None) -> str` (:46-57) and `acceptable(value, consumer, *,
   registry=None) -> bool` (:60-96). For a dict value the word is `value.get(row["field"])` (:76-80), and that word must
   be a `str` and an exact member of `words` (:81). Class `matched` is acceptable iff the token `matched` is listed
   (:87-88). Every doubt is False, and the function never raises (:95-96).
2. **C3-rr and C3-b1 are merged; C3-b2 and C3-d are not.** In `scripts/tests/test_gate_registry.py`:
   - `EXPECTED_DEBT` (:60-63) holds six rows: `stand_identity`, `provenance_acceptance`, `test_identity`, `s5_window`,
     `baseline_identity`, `s5_stand_limits`;
   - K-T1.2 says `"6 gate(s) left as debt:"` (:252);
   - the split is `{"converted": 21, "debt": 6, "exempt": 6}` (:342-343);
   - the F4 `code` list is :740-747 (neither `baseline_identity` nor `stand_identity` is in it);
   - `D13_TRIPLES` is :954-1013 and `D13_ITEM_COUNT = 145` (:1043). Its comment (:1042) says "145 items / 49 triples".

   No D13 triple has `baseline_contract.py` (read :954-1013). Five triples belong to `stand_identity`: :960, :969, :978,
   :1005, :1006.
3. **Registry rows on main** (`references/gate-registry.json`):
   - `stand_identity` is :7-36. It says `vocabulary: "target"` (:8). Its sites are :10-16, all `produce`/`dispatch`.
     `field: "result"` (:17), five words (:18), `accepts: {}` (:26), `promotable: true` (:27), `question / wait /
     stage_entry` (:28), `policy_file: "records/stand-identity.json"` (:30), `scope_keys` (:31), `question_kind` (:33),
     `test: scripts/tests/test_stand_identity.py` (:34), status debt B-257 (:35).
   - `baseline_identity` is :335-356. It says `vocabulary: "target"` (:336). Its sites are `validate_baseline_request`
     validate and `deployment_readiness` accept (:338-341). `field: null` (:342), words matched/mismatched/unknown
     (:343-348), `accepts: {"provenance.baseline": ["matched", "not_applicable"]}` (:349), `promotable: false` (:350),
     `refuse_with_door` (:351), `test: scripts/tests/test_baseline_contract.py` (:354), status debt B-281 (:355).
4. **Test speed** (`scripts/slow_tests.json`): `test_gate_registry.py` 19.7 s (:46), `test_stand_identity.py` 27.4 s (:133),
   `test_story_run_stand_identity.py` 205.7 s (:151). `test_baseline_contract.py` is not listed: the same grep found the
   other three, which is the positive control. All four are keep rows of `test-layers.json` (:213, :5503, :6275; the
   quarantine section starts at :7208). `plans/builder-rules.md:50-53` says the builder runs neither `SLOW_TESTS` nor
   `test_story_run_*` files: the batch canon judges them.

## §1. Architecture, rules, owners (designer rule 1)

- FR sections: C3-g A/C/D/E (FR-1, FR-13, FR-41, FR-59); C3-h C/D (FR-13, FR-59).
- AR-n and their change checks (`design/architecture.md`):
  - AR-13 (:166): one reader of the registry, `gate_template`;
  - AR-19 (:208): axis 5 prose twins. C3-g changes the row's words, so it walks them; C3-h does not;
  - AR-20 (:224): the pins move by named deltas;
  - AR-22 (:240): a consumer and its reader in one commit; the removed `provenance.baseline` is grepped by name;
  - AR-28 (:282): each new gate read's behaviour on missing, unreadable and empty input, pinned;
  - AR-29 (:155): the class and owner of each check.

Checks the cards add or alter:

| check | card | owner it serves | census class | blocking |
|---|---|---|---|---|
| `deployment_readiness`: is a receipt's `status` word the one a before-evidence consumer takes (through `gate_template.acceptable`, consumer `baseline_identity.readiness`) | C3-g | data (a join of the receipt's word to its registry row) | none: `deployment_readiness` has no census row and gets no refusal site. Grep of `judgment-census.json` for `baseline_contract`: rows :42-47 (`_hash_ref`, `baseline_receipt`, `build_baseline_fields`, `validate_baseline_request`, `validate_managed_gate`, `write_baseline_receipt`), none for `deployment_readiness`; those hits are the positive control. Its gaps are list transport (`gaps.append`, census header :3) | no, as today (`blocks_execution: False`, `ready: True`, `baseline_contract.py:216-221`) |
| the gap reason when the registry cannot be read (F-T11 (a) per-site why) | C3-g | data | none (a string in an appended dict) | no |
| refusal of an unknown old-build identity (`validate_baseline_request:21-23`): pinned, not changed | C3-g | data | unchanged: `shape`, owner data (`judgment-census.json:45`) | yes, as today |
| `stand_identity` row: `vocabulary` target -> code, status converted (no code) | C3-h | data | none (registry rows are not census units) | unchanged |

Commit lines are given as CONTENT in each card. Their grammar has two carriers, and this draft copies neither:
- `architecture:` and `judgment:` — `tools/architecture_gate.py`;
- `tests-over:` — `tools/test_volume.py`.

---

## §2. Card C3-g — baseline_identity through the predicate (B-281) — wave 3, after C3-0 (merged)

**The facts the sketch left to this card (read today).**

- **The refusing site (S-b).** An unknown old-build identity is REFUSED in
  `baseline_contract.validate_baseline_request` (`baseline_contract.py:8-30`; the row's `validate` site, registry :339).
  It compares the request's `runtime_provenance.expected_source_revision` with the contract's `baseline_revision`
  (:21-23). When the revision is absent, None or "" while the contract names one, the request gets the error "baseline
  runtime must match the approved before revision". The function RETURNS an error list. Its callers turn that list into
  a refusal:
  - `build_baseline_fields` raises `ValueError` (:50-52);
  - `baseline_receipt` raises (:114-116);
  - `execution_request.validate_request` collects it (:124-125) and raises `RequestError` (:375-378);
  - `manual_evidence.validate_baseline_record` returns it (:673), and `manual_evidence.write_baseline_receipt` raises
    (:713-715).

  The raises in `build_baseline_fields` and `baseline_receipt` are not separate refusals of identity: they re-raise this
  list.

  The OBSERVED build is a different read. It is refused by the provenance predicate, which is `provenance_acceptance`'s
  business and C3-k's:
  - `execution_request.validate_request:175-179`;
  - `manual_evidence.validate_baseline_record:680-689`, which refuses `person_confirmed` (:682-685) and every result
    outside matched/not_applicable (:686-687).
- **The accept site.** `deployment_readiness` (:175-221) never refuses. It counts a receipt as before-evidence when a
  set of equalities holds (:189-198) and `r.get("status") == "captured"` (:199), and when the evidence files hash as
  recorded (:201-214). A row with no valid receipt gets a gap `awaiting_baseline`, `blocks_execution: False`, reason
  "baseline evidence missing, stale or incomparable" (:216-218).
- **Where the row's words live.** They are in the receipt's `status`. Its two producers are:
  - `baseline_contract.baseline_receipt:134`, which writes `"captured" if captured else "inconclusive"`;
  - `manual_evidence.write_baseline_receipt:718`, which writes `record["capture_status"]`. Before that,
    `validate_baseline_record:668` refuses any value outside `{"captured", "inconclusive"}`.

  The one reader is `deployment_readiness:199`. Its callers read only its result: `controller.py:2252-2263` and
  `delivery_summary.py:154-171`. A grep of those two files for `captured|inconclusive` finds only an unrelated
  `'inconclusive'` result word (`delivery_summary.py:401`) and a comment (`controller.py:2279`).

  The consumer `provenance.baseline` is read by no script. A grep of the whole package for `provenance\.baseline` finds
  only `gate-registry.json:349`, which is the positive control, and `tests/test_gate_registry.py:293, 295, 297, 639,
  648`.
- **Measurement (PROJECT.md p. 6 (a)): there is no recorded data.** No fixture holds a baseline receipt: Glob
  `scripts/tests/fixtures/**/baseline-receipts/**` gives 0. A case-sensitive count grep of `fixtures/` for
  `baseline_required|evidence_phase` also gives 0, and the same call form finds `change_disposition|critic_verdict` in 62
  files (positive control). So a before/after control over recorded stories would be vacuous, as C3-b2's was
  (:1017-1023).

  The premise "not a meaning change" therefore rests on a code trace:
  - `acceptable(r, "baseline_identity.readiness")` with `field: "status"`, words `["captured", "inconclusive"]`
    (`captured` -> matched, `inconclusive` -> unknown) and tokens `["matched"]` is True exactly when `r.get("status")` is
    the str `"captured"` (`gate_template.py:76-88`);
  - every other value is False (`"inconclusive"`, another case, `""`, None, a non-str, an absent key);
  - the one new difference is an unreadable registry, which gives False. That is the safe side: a gap, never a count.

  The control is item 4's table, whose expectations come from the row's `decides`.
- **F-T3 has no recorded Lead decision.** The lists after t-994/t-1033 (:1873-1893, :2161-2171) name F-T1, F-T2, F-T5..F-T11
  but not F-T3. This card executes on F-T3 (a), the brief's direction, and returns fork G-0 for the record.

given:
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/design/factory-rules.md` (whole)
- `C:/QAFactory/forge-repo/plans/builder-rules.md`
- `C:/QAFactory/forge-repo/docs/TESTING.md`
- this card, and the C3 shared items S-a..S-f of `C:/QAFactory/forge-repo/docs/tasks/specs/20261117-rules-debt-phase2-cards-spec.md` (:278-346)
- read, under `C:/QAFactory/forge-repo/ai-packages/qa-factory/`:
  - `scripts/baseline_contract.py` (whole, 222 lines)
  - `scripts/manual_evidence.py:658-737`
  - `scripts/gate_template.py` (whole)
  - `scripts/gate_registry.py:21-45, 485-681, 786-912`
  - `references/gate-registry.json:335-356`
  - `scripts/tests/test_baseline_contract.py` (whole)
  - `scripts/tests/test_gate_registry.py`: :55-74, :246-253, :291-298, :336-343, :636-656, :737-771, :950-1068
  - seam precedent `scripts/tests/test_gate_registry.py` C3-0 table (grep `GT._READ`)
owns:
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/references/gate-registry.json` (row `baseline_identity` only: `decides`, `sites`, `field`, `words`, `verdict_map`, `accepts`, `vocabulary`, `status`, `debt_ref`)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/baseline_contract.py` (`deployment_readiness` only, :175-221, with its point-of-use import)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_baseline_contract.py` (two new parameterised test methods, items 4-5; no existing method edited)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_gate_registry.py` (the S-f pins of `baseline_identity`, and the consumer pins F1 :639, :648 and K-N2.12 NEG :291-298, item 6)
non-goals:
- `validate_baseline_request`, `build_baseline_fields`, `baseline_receipt`, `validate_managed_gate`, `write_baseline_receipt` (code unchanged; fork G-3 asks about the non-dict input);
- `manual_evidence.py` code (only registered on G-1 (a)); `validate_baseline_record:668` (a `provenance_acceptance` site, C3-k);
- `execution_request.validate_request`, `profile_contract.acceptable_provenance`, the five `provenance.*` consumers (C3-k);
- `controller.deployment_inputs`, `delivery_summary` (callers, unchanged);
- `gate_template.py`, `gate_registry.py`; `judgment-census.json` (no unit moves);
- any new test FILE; `docs/SIBLING_MAP.md`.
handoff: report path given by the Lead
edges: E1-E12 below
DoD: `python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/gate_registry.py --check` exits 0; `baseline_identity` is absent from the `N gate(s) left as debt:` block; no F-b names `deployment_readiness`. Then `python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for C:/QAFactory/forge-repo/ai-packages/qa-factory/references/gate-registry.json C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/baseline_contract.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_baseline_contract.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_gate_registry.py` and the printed non-slow files, at least `python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_baseline_contract.py` (keep, fast: it runs here). `test_gate_registry.py` is slow, so the batch canon judges it; it is named in the report.
siblings:
- axis 5 (`docs/SIBLING_MAP.md:143`, gate rows <-> sites <-> prose twins): the row's words change. The builder greps `captured|inconclusive|baseline receipt` case-insensitively over `references/*.md`, `skills/`, `agents/` (positive control: the same grep finds `references/gate-registry.json` when that dir is included). Each hit gets a report line "checked, no edit (meaning unchanged)" or an edit named as a finding.
- the second producer of the word: `manual_evidence.write_baseline_receipt` (fork G-1).
- the shape check of the word in `manual_evidence.validate_baseline_record:668` (a `provenance_acceptance` site): named for C3-k, not swept.
- noticed analogs, reported and not carded:
  - `delivery_summary.py:157-160` skips an unreadable receipt file with no word, and the row then reads "missing, stale or incomparable" (FR-41 shade);
  - a non-dict receipt in `controller.deployment_inputs` (:2258-2259) crashes `deployment_readiness` at `r.get` (no pass);
  - the non-dict `runtime_provenance` of fork G-3.
designer: `C:/QAFactory/forge-repo/docs/tasks/specs/20261117-rules-debt-wave3-g-h-cards.md` (C3-g)

Items:
1. **Registry row `baseline_identity`** (F-T3 (a); expected from S-c and the producers' code, §2 facts):
   - `vocabulary: "code"`; `field: "status"`; `words: ["captured", "inconclusive"]`;
   - `verdict_map: {"captured": {"class": "matched"}, "inconclusive": {"class": "unknown", "owner": "environment"}}`;
   - `accepts: {"baseline_identity.readiness": ["matched"]}`. `provenance.baseline` is REMOVED, with no replacement in this
     commit (AR-22: no consumer without its reader; the A2 precedent, cards spec §7 t-1033). A baseline-provenance
     consumer is C3-k's to add with its reader `manual_evidence.validate_baseline_record`;
   - `promotable: false`, `refuse_with_door` / `refuse_with_door` / `waits_at: null`, `closed_by`, `addressee`,
     `person_subject`: unchanged;
   - sites:
     - `validate_baseline_request` stays `validate`;
     - `deployment_readiness` stays `accept`;
     - on G-1 (a), `{"file": "baseline_contract.py", "function": "baseline_receipt", "role": "produce"}` and
       `{"file": "manual_evidence.py", "function": "write_baseline_receipt", "role": "produce"}` are added;
   - `decides`: "the before-state evidence was captured on the approved old build: a request whose runtime does not name
     the approved before revision is refused (validate_baseline_request), and a receipt counts as before-evidence only
     when its status is `captured` and its identity, gate and evidence hashes match; `inconclusive`, any other word or
     none leaves an awaiting_baseline gap, never a pass (identity on the OLD build stays code-proven: a person's word
     never stands in for it)";
   - `status: "converted"`, `debt_ref: ""`.
2. **`deployment_readiness`, the acceptance.** In the `candidates` comprehension (:189-199), the last conjunct
   `r.get("status") == "captured"` becomes `acceptable(r, "baseline_identity.readiness")`. All the other conjuncts stay,
   in their order, before it. The import is `from gate_template import acceptable, registry_problem` inside the function:
   the file's lazy-import style (:64, :71) keeps the package's import-time cost unchanged for `execution_request` /
   `manual_evidence` / `controller`. `gate_template` imports only `gate_registry` (`gate_template.py:29`). Expected from:
   F-T3 (a), C3-0 E9 (one road), and the row's `decides`.
3. **The gap reason when the registry cannot be read** (F-T11 (a), Lead :2168; the per-site why family of t-1043,
   :2253):
   - Read `problem = registry_problem()` once per call.
   - When it is non-empty AND the row had at least one receipt that met every conjunct except the predicate, the gap's
     `reason` is "the gate registry cannot be read (<problem>): a factory defect, the baseline receipt was not judged".
   - Every other gap keeps "baseline evidence missing, stale or incomparable".
   - The gap dict keeps its keys (FR-14).

   Expected from FR-41 (an unknown is never said as a fact) and FR-59.
4. **Test, the acceptance table** (S-b for the accept side; one new parameterised method in `test_baseline_contract.py`,
   e.g. `test_a_receipt_counts_only_by_its_accepted_status_word`, `subTest` per row). The world is the receipt and plan
   row of `test_runner_receipt_is_captured_not_product_pass_and_detects_stale_binding` (:24-39), with the evidence file
   hashing as recorded. For each row the expectation is (`comparisons_ready`, gap reason); `ready` is True and
   `blocks_execution` False in every row:
   - `captured` -> (True, no gap) (the control row);
   - `inconclusive` -> (False, "baseline evidence missing, stale or incomparable");
   - `Captured`, `" captured"`, `""`, None, `5`, `["captured"]`, no `status` key -> (False, the same reason) each;
   - `captured`, but `source_revision` differs from the row's `baseline_revision` -> (False, the same reason). The
     predicate is never the only guard (E4);
   - the unreadable registry with `captured` -> (False, a reason that starts "the gate registry cannot be read (" and
     does not contain "missing"). The seam: save `list(GT._READ)`, set `GT._READ[:] = [({"rows": "x"},
     GR.structural_error({"rows": "x"}))]`, and restore it in `finally`. That is the C3-0 precedent; if the merged
     `gate_template` names its cache otherwise, use that name, and if it exposes none, stop with a question;
   - the unreadable registry with NO receipt -> (False, "baseline evidence missing, stale or incomparable"). A missing
     receipt is still missing.

   Expected from: the row's `decides` (item 1), FR-59, FR-41 and `gate_template`'s error direction — never from
   `deployment_readiness`'s output before the change. Red before the change: the registry rows (no such reason exists
   today). The word rows are green before and after, which is the behaviour-preservation control. The existing methods
   :24-78 are regression and stay unedited.
5. **Test, the refusal of an unknown old-build identity** (S-b for the refusing side; no existing pin: `:117-125` and
   `test_live_audit_contract.py:44-53` pin only the MISMATCH `"new"`). Add one new parameterised method, e.g.
   `test_an_unknown_old_build_is_refused_never_taken`, over the request of `test_live_audit_contract.py:46-50` / the
   `contract()` helper (:14-20). For `runtime_provenance` = `{}`, `{"expected_source_revision": None}`,
   `{"expected_source_revision": ""}`, and the control `{"expected_source_revision": "new"}`, both of these hold:
   - `validate_baseline_request(request)` contains "baseline runtime must match the approved before revision";
   - `build_baseline_fields(row, "gate-A", runtime)` raises `ValueError` whose text holds that sentence.

   Then, with the contract's `baseline_revision` absent AND the runtime's absent, the request is still refused, by
   "baseline_contract requires baseline_revision" (:17-18). Expected from the row's `decides` ("identity on the OLD build
   stays code-proven") and `unknown_branch: refuse_with_door`. Green today: S-a, no code moves for it.
6. **S-f pins** (deltas from the main the node is based on; base today 6 debt / 21 converted, D13 145 items / 49
   triples, §0.2):
   - `EXPECTED_DEBT` loses `baseline_identity` and `EXPECTED_CONVERTED` gains it, with an AR-20 comment line naming C3-g
     and the task;
   - K-T1.2 `"N gate(s) left as debt:"`: N-1;
   - the split: converted +1, debt -1, with its comment;
   - the K-T1.14 label words that name a count are updated in the same line;
   - the F4 `code` list gains `baseline_identity`;
   - the consumer pins:
     - F1 :639 becomes `home["baseline_identity.readiness"] == "baseline_identity"`, label "F1
       baseline_identity.readiness lives under baseline_identity";
     - the loop :648 becomes `("baseline_identity.readiness", "baseline_identity")` (one finding, naming the consumer
       and the row, because the row is promotable false: `gate_registry.py:658-660`, and F1 :667-668 "ONE finding, not
       two");
     - K-N2.12 NEG :291-298 appends `person_confirmed` to `accepts["baseline_identity.readiness"]`, with the same
       expectations (one finding, naming the consumer and the word);
   - D13: re-measure with `GR.analyse(PLUGIN_ROOT)` before and after (the triple set and `len(items)`). Expected:
     - on G-1 (a), +1 triple `("manual_evidence.py", "write_baseline_receipt", "baseline_identity")` and +1 item,
       exactly `record['capture_status'] == 'captured'` (`manual_evidence.py:728`);
     - nothing else moves. `deployment_readiness` held no counted comparison before (no row word, no anchor: `"captured"`
       was not a word of the target row) and holds none after. `baseline_receipt:134` is a conditional inside a dict
       value, not a Compare (`gate_registry.py:313-316` reads an IfExp only as a Compare operand);
     - on G-1 (b), 0 / 0.

     A different measurement is a stop and a question. The comment line takes the form of :1035-1041.

   Expected from: the status rule (one row debt -> converted) and the list of comparisons above.

architecture content:
- `AR-13 -- the receipt's status word is read only through gate_template.acceptable`;
- `AR-22 -- the consumer baseline_identity.readiness lands with its reader; the readerless provenance.baseline is removed (name grepped over the package: tests only)`;
- `AR-28 -- an absent, unaccepted or unreadable-registry status leaves an awaiting_baseline gap, pinned; an unknown old-build revision is refused, pinned`;
- `AR-29 -- xref (a word joined to its registry row), owner data, no census unit`;
- `AR-19 -- axis 5 prose twins walked by grep`;
- `AR-20 -- debt -1, converted +1, F4 +1, D13 re-measured and named`.

judgment content: `none -- a membership join of the producer's status word; whether the capture proves the old build stays code's equalities and the producers' rule`.

tests-over content: only if `tools/test_volume.py` asks: "C3-g: two parameterised tables in a keep file; the S-b refusal had no unknown-revision pin".

Edges:
- E1 (absent / empty / other case / non-str status): not acceptable -> no count -> gap. INVARIANT: a receipt that does not
  say `captured` exactly never counts as before-evidence.
- E2 (unreadable registry): every receipt is uncounted, so every baseline row has a gap; `ready` stays True and nothing
  blocks. The reason names the registry only where a receipt was otherwise valid (item 3). INVARIANT: a broken registry
  never counts a receipt, and never claims evidence is missing when it was there unjudged (FR-41). C3-reg-precondition
  stops the next dispatch first (`controller.validate`, its item 1). Inside a stage that began before, this branch is
  belt-and-braces.
- E3 (present but incomplete registry): the file parses but lacks the consumer. `registry_problem()` is "", so the reason
  stays the old sentence and nothing counts. That is the false-cause residue C3-reg-precondition E2 accepts, held by CI:
  A26 `--check` and item 4's `captured` control row turn red on a consumer-id typo. INVARIANT: no false count.
- E4 POSITIONAL: the predicate is the LAST conjunct of the candidate filter, after the case, version, revision, fixture,
  gate-ref and assertion equalities; the source-revision and hash checks (:201-214) still follow. INVARIANT: a `captured`
  receipt for another case, version, gate, revision or with changed evidence bytes is never counted (the predicate is
  never the only guard, C3-0 E4).
- E5 TEMPORAL (receipts on disk): receipts written before C3-g carry the same two words, from the same two producers, so
  they are read the same way. INVARIANT: no recorded receipt changes meaning (E-a).
- E6 TEMPORAL (consumer): before C3-g, `provenance.baseline` exists and has no reader. After it, it is gone and
  `baseline_identity.readiness` exists with its reader, in one commit. C3-k, based after C3-g (cards spec :1373), adds
  any baseline-provenance consumer with its reader. INVARIANT: no `accepts` entry without its reader (AR-22).
- E7 TEMPORAL (S-f): the pins are deltas from the base. C3-b2 and C3-d (built, in review) move debt by -2 and D13 by their
  measured values before or after C3-g. A later merger merges main in, re-derives its own row's pins and re-measures D13
  (D-0048). INVARIANT: S-f (pins equal the live registry; no card edits another row's pin).
- E8 (limit): none introduced.
- E9 (conflict on `gate-registry.json` / `test_gate_registry.py`): row-disjoint. The F1 block is shared with C3-k
  (`provenance.environment_preparation` lines :640-641, :649), and C3-k runs after C3-g. INVARIANT: C3-g edits only the
  `baseline_identity` lines of F1.
- E10 (adversarial inputs of the reused predicate, error direction): `acceptable` errs only toward False
  (`gate_template.py:9-13, 95-96`), so every doubt is a gap, never a count. Inputs that must stay on the safe side: the
  word rows of item 4 and a registry row with `field` null (a dict is refused, `gate_template.py:77-79`). INVARIANT:
  `deployment_readiness` can only count fewer receipts than today, never more.
- E11 (non-blocking contract, conflicting requirement pair): the row's `unknown_branch: refuse_with_door` and
  `deployment_readiness`'s "never blocks" (docstring :176-182) both hold. The refusal sits at the request
  (`validate_baseline_request`), and readiness only reports. INVARIANT: C3-g changes neither `ready` nor
  `blocks_execution`.
- E12 (one road, P31): the receipt's word is accepted at one site through the one predicate. No other reader compares it
  (grep §2). INVARIANT: a second reader of `status` is a review finding.

Measurement: see §2 facts. The vacuous recorded control is replaced by item 4's table. The control for the critic is
`python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/gate_registry.py --sites`, filtered for
`baseline_contract.py` before and after: no line before or after. On G-1 (a), one new line, `manual_evidence.py:728`,
`[baseline_identity]`.

---

## §3. Card C3-h — stand_identity, converted by S-b/S-c alone (B-257) — wave 3, last on the S-f order

**Facts (read today).**

- **No accept site.** The row's five sites (registry :11-15) are `runtime_probe.conclude` / `finish` (produce),
  `gate_preflight._derive_probe` / `named_container_said` and `driver_stage_build.build_outcome` (dispatch). The E-c
  table and the Decided-branches row (cards spec :352) say "none". `_derive_probe` compares all five words, each into a
  helper (`gate_preflight.py:4587-4601`, with an unknown sixth word sent to `_probe_defect`, :4597-4601). The probe
  record's `result` carries these words (`test_stand_identity.py:771`, `"result": "unknown"`, and the outcomes at
  :820, :837). So `vocabulary: code` is honest with the words unchanged.
- **S-b is already pinned, in two keep files.**
  - The probe level is pinned in the row's `test` file, `test_stand_identity.py`:
    - `ep1_41e_the_device_build_and_the_word`: a build that is read but cannot be identified gives `result: unknown`,
      `asks_person: "how"` (:818-820); the person's word on the same build gives `person_confirmed`, bound to the image
      (:833-837); a rebuild voids the word and asks again (:840-843);
    - `ep1_41e_stands_words_and_doors`: another story's word is not taken (:932-939); a moved stand definition voids it
      (:941-944); a recorded `command` row for the stand/profile reads the build next time, giving `matched` (:957-960);
    - `ep1_41e_an_unreadable_build_never_takes_a_word`: an unreadable build takes no word (:887-896).
  - The stage level is pinned in `test_story_run_stand_identity.py`, the `test` of row `stand_check`, registry :476:
    - K36 setup: the stage entry asks the `stand_identity` question and waits, exit 3, kind `stand_identity`, variant
      `how` (:449-450);
    - "always confirm" writes a `person_confirms` row into the policy file and the stage goes on (:481-498);
    - a recorded `command` method makes the next probe read this story's commit and the stage goes on (:583-597).

  The card therefore adds NO test row and NAMES these pins (S-b's "where such a pin already exists").
- **Measuring "S-b red today".** The builder may run neither file: `SLOW_TESTS` and `test_story_run_*` (§0.4,
  builder-rules :50-53). The measurement is the Lead's, before dispatch. He reads the last `package-full` nightly or
  main's CI run (`tools/ci_read.py`; builder-rules :61-62: "Lead … читает ночной `package-full`") for those two files.
  Both green means this card as written, with no code site. Either red means no dispatch: the red line goes to a fix
  node that owns the failing site (`runtime_probe.py` / `gate_preflight.py` / `driver_stage_build.py`), and C3-h follows
  it.

given:
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/design/factory-rules.md` (whole)
- `C:/QAFactory/forge-repo/plans/builder-rules.md`
- `C:/QAFactory/forge-repo/docs/TESTING.md`
- this card, and the C3 shared items S-a..S-f of `C:/QAFactory/forge-repo/docs/tasks/specs/20261117-rules-debt-phase2-cards-spec.md` (:278-346)
- read, under `C:/QAFactory/forge-repo/ai-packages/qa-factory/`:
  - `references/gate-registry.json:7-36`
  - `scripts/gate_registry.py:485-681` (the `vocabulary` rule :512-519)
  - `scripts/tests/test_stand_identity.py:813-965`
  - `scripts/tests/test_story_run_stand_identity.py:444-498, 550-598`
  - `scripts/tests/test_gate_registry.py`: :55-74, :246-253, :336-343, :737-771, :950-1068
  - the Lead's CI reading of the two stand-identity files (above)
owns:
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/references/gate-registry.json` (row `stand_identity` only: `vocabulary`, `status`, `debt_ref`)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_gate_registry.py` (the S-f pins of `stand_identity` only)
non-goals:
- any code (`runtime_probe.py`, `gate_preflight.py`, `driver_stage_build.py`, `stand_identity.py`): no code site moves;
- the row's words, `verdict_map`, sites and roles (fork H-1 asks about `named_container_said`), `accepts`, branch,
  `policy_file`, `scope_keys`;
- `test_stand_identity.py` and `test_story_run_stand_identity.py` (pins named, not edited); `judgment-census.json`;
- any new test file.
handoff: report path given by the Lead
edges: E1-E8 below
DoD: `python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/gate_registry.py --check` exits 0, and `stand_identity` is absent from the `N gate(s) left as debt:` block. Then `python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for C:/QAFactory/forge-repo/ai-packages/qa-factory/references/gate-registry.json C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_gate_registry.py` and the printed non-slow files. `test_gate_registry.py`, `test_stand_identity.py` and `test_story_run_stand_identity.py` are judged by the batch canon and named in the report with the S-b pins of the facts above.
siblings:
- axis 5 (`docs/SIBLING_MAP.md:143`): the words do not change, so no prose twin is walked.
- the five sites keep their roles. `named_container_said`'s registration (`driver_machine.py:2644-2648`, which registers
  the probe on `''`, that is on `result == 'matched'`, `gate_preflight.py:4484`) is fork H-1.
- the per-story confirmation file `state/stand-confirmations.jsonl` and the policy file `records/stand-identity.json` are
  the two carriers of the person's word: named, unchanged.
designer: `C:/QAFactory/forge-repo/docs/tasks/specs/20261117-rules-debt-wave3-g-h-cards.md` (C3-h)

Items:
1. **Registry row `stand_identity`.** `vocabulary: "code"`, `status: "converted"`, `debt_ref: ""`. Every other key is
   unchanged: the words, `verdict_map`, `accepts: {}`, `promotable: true`, `question / wait / stage_entry`, `closed_by`,
   `addressee`, `person_subject`, `policy_file`, `scope_keys`, `binding_keys`, `question_kind`, sites, and `test`.
   Expected from S-c (the words are the probe's own `result` words, §3 facts) and `_check_row` :516-519 (a converted row
   must say `code`).
2. **S-b: named, no row.** The report quotes the eight pins of §3 facts, each with file:line on the base tree; the builder
   re-greps them (`asks_person`, `stand_identity`, `person_confirmed`). If one is gone on the base tree, the node stops
   with a question (the Lead opens the fix node), and no row is invented here.
3. **S-f pins** (deltas from the base):
   - `EXPECTED_DEBT` loses `stand_identity` and `EXPECTED_CONVERTED` gains it, with an AR-20 comment naming C3-h and the
     task;
   - K-T1.2: N-1;
   - the split: +1 / -1, and the K-T1.14 label words;
   - the F4 `code` list gains `stand_identity`;
   - D13: re-measure with `GR.analyse` before and after. Expected: no triple and no item moves. `analyse` never reads
     `vocabulary` (`gate_registry.py:843-878` uses anchors and `_row_words`), and neither the words nor the sites
     change. A different measurement is a stop and a question.

   The F4 flip control copies `registry["rows"][0]` (that is `stand_identity`) and overrides `vocabulary`, `status`,
   `test`, `sites` and `accepts` (:762-768), so it survives this conversion unchanged.

architecture content:
- `AR-28 -- the unknown branch (question at stage entry, wait) is pinned by test_stand_identity.py ep1_41e and test_story_run_stand_identity.py K36`;
- `AR-29 -- no check moves; registry row only`;
- `AR-20 -- debt -1, converted +1, F4 +1, D13 re-measured: no move`.

judgment content: `none -- a registry row converted with no code; the person's word stays the person's (intent/world), read through the existing stand-identity carriers`.

tests-over content: not expected (no test lines added).

Edges:
- E1 (empty / absent / unreadable build): `unknown` -> the question at stage entry, the stage waits; an unreadable build
  takes no word (pinned :887-896). INVARIANT: a stand whose build is not established never runs S5 on a guess (AR-28).
- E2 (the person's word, scope): a word binds to its story and its build (image); a policy-file row binds to its
  `scope_keys` (`environment_id`, `profile_id`). INVARIANT: a word given for another story, another build or a moved
  stand definition never covers this one (pinned :932-944, :840-843).
- E3 TEMPORAL (S-f, order): C3-h is last on the expected order (cards spec :330-331). Its pins are deltas from whatever
  merged before it. INVARIANT: S-f.
- E4 TEMPORAL (red today): if the Lead's CI reading shows a stand-identity pin red, C3-h is not dispatched. INVARIANT: a
  row is never converted over a red unknown-branch pin.
- E5 (limit): none introduced.
- E6 (conflict, HOT `gate_preflight.py`): under this card C3-h edits no `gate_preflight.py` code, so its place on the
  queue C3-rr -> C3-j -> C3-k -> C3-h (cards spec :1376) binds only if H-1 (b) or a red S-b adds a code site.
  INVARIANT: no two open nodes edit the HOT file at once.
- E7 (the flip control, positional): the F4 control reads `rows[0]`. If a later edit reorders the registry, the control
  still overrides every key it relies on. INVARIANT: the control never depends on a live row's status (C3-0 E10).
- E8 (one road, P31): no new reader of the probe's words. The five sites stay the only ones registered.

---

## §4. Forks (returned, not decided)

- **G-0 — record F-T3's decision** (C3-g). The cards spec holds no Lead line for F-T3 (§2 facts). (a) F-T3 (a), as the
  brief directs and C3-g executes: the receipt's own words, `field: "status"`, consumer `baseline_identity.readiness`,
  `provenance.baseline` removed; (b) re-role `deployment_readiness` `measure` and convert with no predicate (it never
  blocks); (c) keep `provenance.baseline` (fits no code). **Rec (a)**. Cost: none beyond the card.
- **G-1 — register the two producers of the status word** (C3-g, AR-22 "every field produced has a reader", axis 5). (a)
  add `baseline_contract.baseline_receipt` and `manual_evidence.write_baseline_receipt` as `produce` sites of
  `baseline_identity`. A26 then sees the producer comparison `record['capture_status'] == 'captured'`
  (`manual_evidence.py:728`), at a cost of +1 D13 triple and item. `manual_evidence.validate_baseline_record:668` stays
  out, because a second registration beside its `provenance_acceptance` accept site would be refused once C3-k converts
  that row (`gate_registry.py:831-836`). (b) Register neither; the producers stay invisible (the BLIND SPOT, `:76`).
  **Rec (a)**: registry lines only, and the row then names every place its words are born.
- **G-2 — the refusal's door** (C3-g, FR-1/AR-9). "baseline runtime must match the approved before revision"
  (`baseline_contract.py:23`) says what it expected but names no explicit step. (a) Pin it as is (S-a: the branch already
  refuses) and file one finding "the baseline revision refusal names no door", in the rules-debt pile. (b) C3-g owns
  `validate_baseline_request` and appends a door clause naming the revision (`…: probe a stand that runs <baseline_revision>
  and build the request again`). That clause shows up in `validate_request`'s joined `RequestError` and in the manual
  errors. **Rec (a)**: the conversion is about the unknown branch, and a text change of a shared refusal belongs to an
  AR-9 node with its refusal-registry check (`architecture.md:111`).
- **G-3 — a non-dict `runtime_provenance` / `baseline_contract` crashes the refusing site** (C3-g). The site calls
  `(request.get("runtime_provenance") or {}).get(...)` (`baseline_contract.py:21`), and `request.get("baseline_contract")
  or {}` (:14) works the same way. A truthy non-dict raises `AttributeError`. In `validate_request` this happens before
  that function's own dict check (:150-153). The error direction is safe (a stop, never a pass), but the stop names no
  field (FR-1). (a) A finding, not carded. (b) C3-g also owns `validate_baseline_request` and refuses a non-dict with a
  named error, plus one row in item 5. **Rec (a)**: an outside-input hardening of a shared validator, outside the
  conversion; cost of (b): one function more in owns and one row.
- **H-1 — `named_container_said` reads like a true accept** (C3-h, E-c invariant "a re-role never hides a literal
  acceptance"). It returns `''` exactly on `result == "matched"` (`gate_preflight.py:4484-4485`), and the driver then
  registers the probe (`driver_machine.py:2644-2648`). Its docstring says "Whoever registers the container acts on ''
  alone". It is registered `dispatch` (registry :14), and the t-989 plan critic's column says no accept site. (a) Keep
  `dispatch` as decided. The registration is a config write: every later launch re-probes the stand through
  `provenance_acceptance` (`execution_request.validate_request:175-179`), so no run passes on it. (b) Re-role it `accept`
  and route the comparison through `acceptable(result, "stand_identity.register")` with `accepts:
  {"stand_identity.register": ["matched"]}`. That brings `gate_preflight.py` into owns (HOT, queue position 4), one test
  row, and D13 -1 item (the triple :978 leaves). **Rec (a)**, with the plan critic of C3-h asked to judge it explicitly
  (it is the one site the t-989 judgment covered without reading `driver_machine`).

## §5. Small choices closed

- C3-g imports `gate_template` at the point of use (the file's lazy style), not at module top.
- C3-g's registry-why sentence applies only when a receipt met every other conjunct. A row with no receipt keeps
  "missing", which is true.
- `inconclusive`'s unknown owner is `environment`, as the row's `unknown` owner today (registry :347).
- Both cards put their tests in existing keep files; C3-g uses two new parameterised methods in `test_baseline_contract.py`
  (the file has no table; the C3-reg-precondition precedent, cards spec :1209).
- C3-h adds no test row, because eight pins exist (§3).

## §6. Readers of every touched file (rule 7)

Commands (Grep, today):

| # | path | pattern | result | positive control |
|---|---|---|---|---|
| 1 | `tools/` (count) | `gate-registry\|baseline_contract\|test_baseline_contract\|test_gate_registry\|test_stand_identity\|deployment_readiness\|provenance\.baseline` | 16 hits in 3 files: `source-split-carriers.json` 3, `source_split.py` 12, `test_quarantine.py` 1. In content mode every hit names `gate-registry.json` or `test_gate_registry.py`, so `baseline_contract`, `test_baseline_contract`, `test_stand_identity`, `deployment_readiness` and `provenance.baseline` give 0 | the same call's `gate-registry` hits |
| 2 | `.githooks/` | the same names + `architecture_gate` | 1 hit, `commit-msg:37`, which is the control, so 0 for the names | `architecture_gate` |
| 3 | `.claude/settings.json` | the same names + `hygiene_gate` | 1 hit, the control, so 0 | `hygiene_gate` |
| 4 | `.claude/agents/` | the same names + `designer` | 3 hits, all `designer.md`, the control, so 0 | `designer` |

| touched | reader | verdict |
|---|---|---|
| `gate-registry.json` (C3-g row `baseline_identity`, C3-h row `stand_identity`) | `tools/source-split-carriers.json:15`, `tools/source_split.py:2753-2891`, `tools/test_quarantine.py:2199` (path only); package: `gate_registry.py` (A26), `gate_template.py` (run time), `test_gate_registry.py` | unchanged: they read the path and file/function keys, and both cards keep the row form. The pins: S-f in each card |
| `test_gate_registry.py` (both cards, pins) | `tools/source-split-carriers.json:25` (D13 py-triple carrier), `tools/source_split.py:2812-2826` (selftest strings); `test-layers.json` keep row | unchanged: the triple tuple form is kept; shared pins change in every converting stream (S-f order, D-0048) |
| `baseline_contract.py` (C3-g, `deployment_readiness`) | tools: 0. Package callers: `controller.py:2253-2262`, `delivery_summary.py:154-171` (result only); `execution_request.py:124-127`, `manual_evidence.py:660` (other functions) | unchanged: the same signature and result keys; only the gap reason text differs on an unreadable registry |
| `test_baseline_contract.py` (C3-g) | `test-layers.json:213` keep row; tools: 0 | unchanged |

## §7. Not established

- No run: `gate_registry.py --check` / `--sites`, `GR.analyse`, and the test files. The D13 deltas are by reading the
  scanner rules (`gate_registry.py:21-31, 304-317, 843-853`); the builder measures them.
- Whether any fixture ever recorded a baseline receipt: 0 by Glob and grep, with controls (§2).
- The CI state of `test_stand_identity.py` / `test_story_run_stand_identity.py` on main (the Lead's reading, §3).
- `driver_stage_build.build_outcome` and `runtime_probe.conclude/finish` were not re-read (their roles are as
  registered; the words are unchanged).
- Whether `test_stand_identity.py` pins non-coverage of a registry row across `scope_keys` (another profile): not
  found; S-b does not need it (E2's invariant rests on the story/image/definition pins).

## §8. Reading trail

- cards spec: :1-420, :533-782, :918-1381, :1547-1876, :1873-2348 (whole, except :420-532 and :782-917);
- `baseline_contract.py` (whole); `manual_evidence.py:650-744`; `gate_template.py` (whole);
- `gate_registry.py`: :1-150, :205-424, :425-724, :786-920;
- `gate-registry.json`: :1-95, :120-151, :310-360; ids (grep);
- `test_gate_registry.py`: :30-74, :240-353, :615-775, :940-1074 (+ grep);
- `test_baseline_contract.py` (whole); `test_live_audit_contract.py:38-57`;
- `test_stand_identity.py`: :1-70, :354-433, :726-1025 (+ def grep);
- `test_story_run_stand_identity.py`: :444-503, :550-624 (+ def grep);
- `execution_request.py`: :60-209, :360-384 (+ grep); `run_suite.py:455-494`; `controller.py:2252-2263`;
  `delivery_summary.py:152-173`;
- `gate_preflight.py:4473-4602` (+ grep); `driver_machine.py:2642-2650` (grep context);
- `judgment-census.json`: :1-6 (+ grep); `slow_tests.json` (grep); `test-layers.json` (grep);
- `architecture.md` change-check grep; `plans/builder-rules.md:46-63` (+ grep); `tools/` grep for `tests-over`;
- greps with controls:
  - `provenance\.baseline` over the package (control: the registry hit);
  - `"captured"|"inconclusive"` over `scripts/*.py`;
  - `captured|inconclusive` over `controller.py` / `delivery_summary.py`;
  - the readers of `deployment_readiness|baseline-receipts|…` over the package;
  - the rule-7 greps of §6.

## Lead decisions on the forks (17.11.2026, owner away: by recommendation, until the owner's word)

- G-0 = (a): F-T3 (a) — the receipt's own words, `field: "status"`, consumer `baseline_identity.readiness`,
  `provenance.baseline` removed. This is the F-T3 decision the cards spec lacked.
- G-1 = (a): the two producers of the status word are registered `produce` sites; D13 +1 triple / +1 item, named (S-f).
- G-2 = (a): the refusal is pinned as is; one finding "the baseline revision refusal names no door" (rules-debt pile),
  filed by the C3-g builder with its row.
- G-3 = (a): one finding "a non-dict `runtime_provenance` / `baseline_contract` crashes the refusing site with no named
  field" (rules-debt pile), filed by the C3-g builder with its row.
- H-1 = (a): `named_container_said` stays `dispatch`; the plan critic judges it explicitly.
- E4 of C3-h (the Lead's CI reading): the push canon of main after the P-b merge, run 44052586866, is green
  (`python -B tools/ci_read.py pipelines`), so no stand-identity pin is red on main today.
- Both cards go to ONE plan critic before any builder (they change what a registry row means).
