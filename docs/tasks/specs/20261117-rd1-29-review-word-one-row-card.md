# RD1-29 card (draft) — the critic's review word read through one registry row; one builder for the review door

Designer draft for task t-1222, node `rules-debt/1/RD1-29`, feature F19. Source: finding
`plans/piles/rules-debt/findings/20261117-c3-slovo-obzora-kritika-chitaetsya-vne-reestra.md` (verdict t-1084, fix 3 (c)).
The Lead decides the forks in §2. Until then the items in §4 follow the recommended options and say so where they depend on them.

## 0. The future builder dispatch: header lines (R11-f)

```
task: <new id at dispatch>
node: rules-debt/1/RD1-29
feature: F19
given:
C:/QAFactory/forge-repo/docs/tasks/specs/20261117-rd1-29-review-word-one-row-card.md
C:/QAFactory/forge-repo/ai-packages/qa-factory/design/factory-rules.md
C:/QAFactory/forge-repo/ai-packages/qa-factory/design/architecture.md
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/gate_template.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/gate_registry.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/acceptance.py
C:/QAFactory/forge-repo/docs/TESTING.md
owns:
C:/QAFactory/forge-repo/ai-packages/qa-factory/references/gate-registry.json
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/window_record.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/case_stamp.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/check_delivery.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/report_facts.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/handoff_check.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/traceability.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/factory_dashboard.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/ledger.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_case_stamp.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_window_record.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_check_delivery.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_report_facts.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_handoff.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_traceability_report.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_factory_dashboard_joins.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_ledger.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_gate_registry.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/fixtures/judgment-census.json
non-goals: rows of gate-registry.json other than `s5_window` (one site added) and the new `critic_review` (RD1-26 owns `test_identity`, RD1-28 owns `probe_verdict`); no second predicate or registry reader in production code (only `gate_template.acceptable` / `registry_problem` / `registry_why`); `acceptance.py` is not edited (RD1-26/RD1-28 own it); the S4 roll-call vocabulary `critic_rollcall.APPROVING_VERDICTS` (fork F3); unifying the strip/raw readings (fork F5); no new test file
handoff: a report with the FR walk (sections A-G), the before/after numbers of `gate_registry.py --sites`, the witness output, and the `architecture:` / `judgment:` lines
edges: §5 of the card (E1-E12, each with its invariant)
DoD: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <every owns path above>` and every file it prints; `python -B ai-packages/qa-factory/scripts/gate_registry.py --check` exits 0; `python -B ai-packages/qa-factory/scripts/tests/test_judgment_census.py` green
siblings: axis 34 (one road for the review word: the s5_window row inside the window, the critic_review row after it, no literal list left); axis 5 row "The critic's verdict word in the ledger" (ledger.verdict_of / is_unverified / is_rejected); RD1-28 (probe_verdict words) is the nearest sibling; critic_rollcall.APPROVING_VERDICTS is fork F3
designer: C:/QAFactory/forge-repo/docs/tasks/specs/20261117-rd1-29-review-word-one-row-card.md
```

The owns are wider than the batch row (`check_delivery`, `case_stamp`, `report_facts`, `window_record`, `gate-registry.json`). The card
widens them under designer rule 2: `handoff_check.py` is forced, because it reads the deleted `report_facts.APPROVING`; the other three
carry copies of the same word list. The Lead confirms the widening against the zones of batches in work (fork F2).

## 1. Measured facts (read from the carriers 17.11.2026)

| # | Fact | Carrier |
|---|---|---|
| m1 | `s5_window` row: words `approved` (matched), `unverified` (not_applicable, reason `static_review`); consumers `s5_window.review` ["matched"], `.static_review` ["not_applicable:static_review"], `.handed_review` ["matched", "not_applicable:static_review"]. `approved_with_fixes` is NOT a word of the row | `references/gate-registry.json` row `s5_window` |
| m2 | In the window, `approved_with_fixes` is a review gap for a test that ran and for a handed one | `tests/test_window_record.py:2854`, `:2860` (C3-d table) |
| m3 | After the window, `approved` and `approved_with_fixes` approve, as literal lists: `case_stamp.APPROVING` (:317, read at :344 `instance_hold`), `report_facts.APPROVING` (:63, read at :1536 `_tests`), `check_delivery.py:860` (`lifecycle_reasons`), `traceability.py:884` (`Story._review_basis`), `factory_dashboard.py:887` (`instance_basis`) | the files at those lines |
| m4 | `handoff_check.py:966` (`_claim_rollcall`) reads `report_facts.APPROVING` against the S4 case critic's form `review.outcome` (same vocabulary `vocabulary.critic_verdicts`) | `handoff_check.py:952-974`; `references/slices/qa-case-critic/handoff-keys.md:23` |
| m5 | `ledger.test_state:1191` holds the vocabulary as a third literal set `{"approved", "approved_with_fixes", UNVERIFIED}` (a known-word check, not an approving one). `contract.CRITIC_VERDICTS` (:2212) is the code vocabulary | `ledger.py:1183-1195`; `contract.py:2209-2215` |
| m6 | `window_record.build` holds THREE copies of the per-kind rule, not two: `:1641` (stopped, `!= BLOCKED_REVIEW_VERDICT`), `:1649` (every other kind, `!= "approved"`, including handed), `:1742` (probe gap). `GAP_ORIGIN["review"]` (:324) is the fourth text. `:1649` writes the note `ORIGIN["review"]` ("carries no `critic_verdict`") even when a word IS present | `window_record.py:1637-1651`, `:1740-1751`, `:312-328`, `:155` |
| m7 | `acceptance.validate_window` decides the review per kind with four literal calls: stopped and gapped `s5_window.static_review`, handed `.handed_review`, the rest `.review` | `acceptance.py:1156-1176` |
| m8 | `_explain_parts` picks a note when `field in line`, so a note of field `review` also explains the line `stale_review:<id>`. Today a handed `unverified` instance (no review gap) carries a `review` note, which then explains its `stale_review` gap with the wrong door | `window_record.py:1815-1824` |
| m9 | Readings of the word differ: `case_stamp` reads raw, `check_delivery` reads `str()` without a strip, and `report_facts`, `traceability` and `factory_dashboard` read through `ledger.verdict_of`, which strips. `acceptable` is case-exact and does not strip | `case_stamp.py:344`; `check_delivery.py:858`; `ledger.py:1027-1030`; `gate_template.py:9-11` |
| m10 | The registry schema has no cross-row word check: only row ids and consumer ids must be unique | `gate_registry.py:684-743` (`_check_registry`) |
| m11 | F-b today: a converted accept site must call something named `acceptable`. RD1-25 (in work) narrows this: the call's first literal consumer must be a key of the site's own row | `gate_registry.py:831-841`; RD1-25 finding |
| m12 | D13 pins: `D13_ITEM_COUNT = 151` and the triple set. `("window_record.py", "build", "s5_window")` is held by ONE counted comparison, `item['review']['verdict'] != 'approved'` | `tests/test_gate_registry.py:1069-1081` |
| m13 | `lifecycle_reasons` already has a "could not be read" road: one reason, head `case lifecycle not checked: ` | `check_delivery.py:851-855`, `:895-897` |
| m14 | `report_facts._tests` returning None is an existing state that readers handle, rendered by `_r_proven` through `_unknown_line(facts, "ledger", ...)`. `_unknown_line` reads `<key>_code == "tool"` | `report_facts.py:1511-1512`, `:3660-3665`, `:3086-3090` |

## 2. Section 1 — invariants, owners, census, commit lines

AR-n touched (`design/architecture.md`), and the check each demands in the DoD:

- AR-1 (closed variety is a data row): the approving words leave code for the `critic_review` row. Check: no literal pair
  `("approved", "approved_with_fixes")` is left in `scripts/*.py` outside `scripts/tests/`. Run the Grep
  `approved_with_fixes"\)|"approved", "approved_with_fixes"`, with positive control `contract.py:2212` (CRITIC_VERDICTS stays).
- AR-13 / AR-15 (one reader, one survivor): every site asks `gate_template.acceptable`, and the twin pin `case_stamp.APPROVING ==
  report_facts.APPROVING` is replaced by the word table. The change check: grep SIBLING_MAP axis 5 row "The critic's verdict word in the
  ledger"; that row gains a line naming `critic_review` (a doc edit for the Lead, outside owns: the docs are not package).
- AR-9 (a refusal names what it expected and a door): one builder writes the review door for every kind. Check: every kind's note
  names the words its consumer accepts (the test row in item 2).
- AR-19 (stage twins): the S5 window (`s5_window`) and the post-window readers (`critic_review`) are twins over one word; the card
  names both sides, and the window's semantics stay as they are (E7).
- AR-20 (ratchets): the D13 count and triples move DOWN. The estimate (not verified): 151 -> 150, and the triple `window_record.py/build/s5_window`
  leaves. A raise of any pin is named row by row in the report; the judgment census counts only shrink.
- AR-28 (an unknown never becomes a pass): an unreadable registry gives a stated unknown at every site (E2).
- AR-29 (code judges data): the word stays the critic's judgment. Code reads a token of a closed vocabulary through data.

Owner and census class of every check the card adds or alters (P27, AR-29):

| Check | Owner it serves | Census class |
|---|---|---|
| `case_stamp.instance_hold` `not_approved` branch through `critic_review.stamp` | data (code reads the critic's token) | shape (unit not in the census today; no row added unless the census test asks) |
| `check_delivery.lifecycle_reasons` approving filter + registry line | data | shape |
| `report_facts._tests` proven filter + registry unknown | data | shape |
| `handoff_check._claim_rollcall` approving test | data (the verifier); the verdict itself is the case critic's judgment, accepted at S4 | shape |
| `traceability.Story._review_basis`, `factory_dashboard.instance_basis` display pick | data | not a check (display) |
| `ledger.test_state` known-word check through `C.CRITIC_VERDICTS` | data | shape (unchanged class) |
| `window_record.review_note` (new) | data | shape; census row `{"file": "window_record.py", "function": "review_note", "class": "shape", "roles": ["conductor"], "owner": "data"}` only if `test_judgment_census.py` asks |
| `window_record.build` | data | shape (row 1265 unchanged) |

Commit lines: the only carrier of their form is `tools/architecture_gate.py` (its docstring, points 1 and 6). In that form:
`architecture: AR-1, AR-9, AR-13, AR-15, AR-19, AR-20, AR-28, AR-29 -- <how each is kept, one clause each>` and
`judgment: none -- the critic's review word stays the critic's judgment; code reads its token through the registry row instead of a literal list, and no check reads a role's content`.

## 3. Forks (the Lead decides; recommendations are marked)

**F1 — `s5_window` row vs a separate review row (the finding's fork).** The measurement is m1, m2, m3, m10 and m12.
- (A) Add `approved_with_fixes` to `s5_window`, with a new consumer for the post-window readers. The word cannot be class `matched`:
  `s5_window.review` and `.handed_review` accept `matched`, so the window would start closing a review on `approved_with_fixes`. That flips rows
  2854 and 2860 and breaks "behaviour on a readable registry is kept". (A) works only with a false class, `not_applicable` plus a
  reason code such as `with_fixes` for an approving word. The row's `decides`, its `waits_at: window_acceptance` and its unknown
  branch (a question to the critic) would then also govern gate B, the stamp and the report, which ask no question. Cost: one row, a
  class that lies, mixed unknown branches.
- (B, recommended) A new row `critic_review` (§4 item 1): the four words of `contract.CRITIC_VERDICTS`, with `approved` and
  `approved_with_fixes` both `matched`, `unverified` `not_applicable:static_review`, `rejected` `mismatched`, and one consumer per
  post-window site, all ["matched"]. `s5_window` stays as it is. Cost: `approved` and `unverified` are mapped in two rows. The schema
  allows it (m10); a test row pins that a word present in both rows has the same class and reason code (E9).

**F2 — the owns widen beyond the batch row.** `handoff_check.py` is forced: it reads the deleted `report_facts.APPROVING`.
`traceability.py`, `factory_dashboard.py` and `ledger.py` hold the same list (m3, m5). Designer rule 2 says the card fixes them.
- (a, recommended) Widen as in §0. The Lead checks that no batch in work owns these files (rule 4).
- (b) Keep the batch owns and leave three copies. That breaks P31 and the rule 9 sweep.

**F3 — `critic_rollcall.APPROVING_VERDICTS` (`approve`, `approve_with_fixes`, `approve_with_concerns`).** It is the same class (a
review word accepted outside the registry), read at `critic_rollcall.py:44,251,255,299,362,607,1007,1009`, `controller.py:3556-3561`
and `driver_stage_plan.py:819`. It is a different vocabulary (the S4 roll-call) and a different gate.
- (a, recommended) A new node in this pile after RD1-29: its own row (e.g. `case_review_rollcall`), with owns `critic_rollcall.py`,
  `controller.py` (hot: queue it behind the nodes holding it), `driver_stage_plan.py`, `gate-registry.json` and their tests.
- (b) Widen RD1-29. That adds the hot `controller.py` and an S4 gate to an S5/S8 node.

**F4 — the person's door in every review note.** S9 (RD1-17) lets a person's word pass any `review:<id>` gap (`word_let_go`), but
today only the generic `GAP_ORIGIN["review"]` names `REVIEW_GAP_RECORD`. The per-instance notes, which win in `_explain_parts`, never
name it.
- (a, recommended) The one builder ends EVERY kind's door with the person's door, as `GAP_ORIGIN["review"]` does today. This
  changes text a person and a role read: the door becomes reachable from every review line (FR-57, FR-2).
- (b) Keep the per-kind notes without it, so only the text's builder is unified.

**F5 — raw vs stripped reading of the word (m9).** A padded `" approved"` today holds the stamp and gate B's demand, but it counts
as proven in the report and shows its proof level on the dashboard.
- (a, recommended for this node) Keep each site's reading, as the brief's edge "behaviour kept" requires. Pin today's behaviour with
  `" approved"` rows, so that a later unification is a visible change.
- (c) Pass the raw word at every site. This errs toward "not approving" at the report and the displays. The cost is three sites
  bypassing `ledger.verdict_of` (axis 5 survivor) for the decision, plus 3 row changes.
- (b) Pass `verdict_of` at every site. This errs toward ACCEPTING at the stamp and at gate B, the wrong direction for a gate. Not recommended.

**F6 — `test_gate_registry.py` is shared with RD1-25, RD1-26 and RD1-28 (the D13 pins are one constant).**
- (a, recommended) RD1-29 starts after RD1-25 has landed on main, so its own-row detector judges the new sites in the builder's own
  run. RD1-26 and RD1-28 may run in parallel: the later node merges main and remeasures D13 on the merged tree (batch "Порядок по общим файлам").
- (b) Run in parallel with RD1-25 and accept that its detector first sees these sites at the batch canon.

## 4. Builder items (numbered; each: file, function, expected behaviour, test row)

1. `references/gate-registry.json`
   - (a) Add to `s5_window.sites` the entry `{"file": "window_record.py", "function": "review_note", "role": "accept"}`.
   - (b) Add the row below, per F1 (B). Fields not named take the values of `probe_verdict`'s row form:
     ```json
     {"id": "critic_review", "inventory": "RD1-29", "vocabulary": "code",
      "decides": "the critic's review word on a manifest row (`critic_verdict`), or on a critic's form (`review.outcome`), approves the test AFTER its S5 window: `approved` and `approved_with_fixes` approve (the case stamp is given, the test counts as proven, gate B demands the case's Automated transition, the basis shows the proof level); `unverified` (a static review, D-0013) and `rejected` never approve; any other word or none is not approving, and the ledger names it `review_unrecognised` (FR-19). Inside the window the review is closed by `s5_window`, where `approved_with_fixes` does not close it",
      "sites": [
        {"file": "case_stamp.py", "function": "instance_hold", "role": "accept"},
        {"file": "check_delivery.py", "function": "lifecycle_reasons", "role": "accept"},
        {"file": "report_facts.py", "function": "_tests", "role": "accept"},
        {"file": "handoff_check.py", "function": "_claim_rollcall", "role": "validate"},
        {"file": "traceability.py", "function": "_review_basis", "role": "measure"},
        {"file": "factory_dashboard.py", "function": "instance_basis", "role": "measure"}
      ],
      "field": "critic_verdict",
      "words": ["approved", "approved_with_fixes", "rejected", "unverified"],
      "verdict_map": {
        "approved": {"class": "matched"}, "approved_with_fixes": {"class": "matched"},
        "rejected": {"class": "mismatched"},
        "unverified": {"class": "not_applicable", "reason_code": "static_review"}
      },
      "accepts": {
        "critic_review.stamp": ["matched"], "critic_review.lifecycle": ["matched"], "critic_review.proven": ["matched"],
        "critic_review.rollcall_claim": ["matched"], "critic_review.basis_report": ["matched"], "critic_review.basis_dashboard": ["matched"]
      },
      "promotable": false,
      "unknown_branch": "refuse_with_door", "on_no_answer": "refuse_with_door", "waits_at": null,
      "closed_by": [], "addressee": ["role:qa-code-critic"], "person_subject": null,
      "policy_file": null, "scope_keys": [], "binding_keys": [], "question_kind": null,
      "test": "scripts/tests/test_case_stamp.py",
      "status": "converted", "debt_ref": "", "exempt_reason": ""}
     ```
   - Test row (`test_case_stamp.py`, replacing A-K1 at :211 "`APPROVING` equals `report_facts.APPROVING`"), one table. For every
     consumer of `critic_review` and every word in `C.CRITIC_VERDICTS` plus `"Approved"`, `" approved"`, `"approved "`, `""`, `None`,
     `["approved"]`, `"\u0430pproved"` (written as the escape, FR-30), `"approved;rejected"` and a 10,000-character string:
     `GT.acceptable(word, consumer) is (word in ("approved", "approved_with_fixes"))`. Further rows:
     - the same table with an unreadable registry, which must be all False;
     - an injected registry whose `critic_review.words` lacks `approved_with_fixes`, which must give False (the data drives it);
     - `set(row["words"]) == set(C.CRITIC_VERDICTS)` (E11);
     - every word present in both `s5_window` and `critic_review` maps to the same class and reason code (E9). The test reads the
       file through `gate_registry.load_registry`; a test is not a production reader.
   - `test_gate_registry.py`: D13 pins remeasured with `gate_registry.py --sites` before and after; the numbers and the
     moved triples go into the comment block above `D13_ITEM_COUNT`, in its own form (AR-20).

2. `scripts/window_record.py` — one builder for the review door.
   - New `review_note(identity, kind, said) -> tuple | None`. `kind` is one of `"stopped"`, `"handed"`, `"gapped"`, `"ran"` (the
     kinds of m7). It returns None when the word closes the review for that kind, through ONE literal call per kind:
     `acceptable(said, "s5_window.static_review")` for stopped and gapped, `"s5_window.handed_review"` for handed,
     `"s5_window.review"` for ran. Literal consumers only: no table lookup or f-string, because RD1-25 reads the first literal (m11).
     Otherwise it returns `(identity, "review", what + "; " + door)`.
   - `what` is "the manifest row's `critic_verdict` is `<shown>`" or "the manifest row carries no `critic_verdict`" (word absent,
     None or `""`), followed by the kind's clause: blocked by the stand / its probe could not run here (a person's word or the factory
     names it) / the person runs it / it ran with its proof.
   - `door` is the kind's expected words, then "the critic records it through `manifest_put.py`", then (F4 (a)) "; or, when the
     person accepts the test without the critic's verdict, the orchestrator records their words with `" + REVIEW_GAP_RECORD + "` (the
     S5 step passes; delivery still reads no critic verdict)".
   - The kinds' clause and door texts are module-level string constants. No tuple, list or set display of verdict words sits inside
     `review_note`: the scanner would count it.
   - `<shown>` = `detector_verdict.one_line(str(said))` with `;` replaced by `,`, cut at 60 characters plus `...` (E5).
   - With `gate_template.registry_problem()` non-empty, it returns `(identity, "review", "the review word of this instance cannot be
     judged; " + gate_template.registry_why(reason, "repair the package install, then build this record again"))` (E2).
   - `GAP_ORIGIN["review"]` is built by the same builder: a module-level `review_origin()` returns `(what, door)` for no particular
     kind. It names every kind's words in one sentence, as today's text does, plus the person's door. `ORIGIN["review"]` stays (it is
     the field-missing origin read by `_origin_text` for other callers).
   - `build`: the block at `:1637-1651` becomes one call `review_note(identity, "stopped" if stopped else "handed" if identity in
     handed_ok else "ran", item["review"]["verdict"])`, and its result is appended when not None. The block at `:1740-1751` (probe gap
     set) removes the instance's `review` notes, then appends `review_note(identity, "gapped", said)` when not None. `build` keeps no
     comparison of a review word.
   - Test rows (`test_window_record.py::c3_d_review_word_through_the_registry`, the existing table at :2853-2861): every row gains
     the column `(WR.review_note("A", kind, word) is not None) == gap`, for a readable and an unreadable registry.
   - Further rows: for each kind, the set `{w in C.CRITIC_VERDICTS : acceptable(w, consumer of kind)}` equals the set of
     backticked verdict words its door names, and `review_origin()` names the union (the text cannot drift from the data);
     `said="x; y"` gives a note whose first `"; "` is the builder's boundary (E5); `said=["approved"]` and `said=None` do not raise.

3. `scripts/case_stamp.py::instance_hold`
   - Delete `APPROVING` and its comment (:315-317). The last line becomes `return "" if gate_template.acceptable(entry.get("critic_verdict"),
     "critic_review.stamp") else NOT_APPROVED`, which keeps the raw reading (F5 (a)). The docstring line for `not_approved` names the row.
   - Test rows (`test_case_stamp.py`, the verdict table at :166-180): the existing rows stay green, including `approved_with_fixes`
     stamping like `approved`; add `" approved"` -> `not_approved` (F5 pin) and unreadable registry -> `not_approved`.

4. `scripts/check_delivery.py::lifecycle_reasons`
   - Before the loop: when `gate_template.registry_problem()` is non-empty, return exactly
     `["case lifecycle not checked: " + gate_template.registry_why(reason, "the critic's review word cannot be judged - repair the
     package install, then run gate B again")]`.
   - In the loop, `:860` becomes `if not gate_template.acceptable(verdict, "critic_review.lifecycle") and not green: continue`,
     with `verdict` read as today.
   - Test rows (`test_check_delivery.py`): the A-K5 rows (:1105-1114, :1767-1772) stay green; add unreadable registry -> one reason
     whose head is `case lifecycle not checked: the gate registry cannot be read`. If `test_delivery_ownership.py` classifies the
     existing join line by its head, add one row there; that file is then the one extra path, reported under "needed beyond the manifest".

5. `scripts/report_facts.py::_tests` and `_r_proven`
   - Delete `APPROVING` (:63).
   - In `_tests`, after `if ledger is None: return None`: when `gate_template.registry_problem()` is non-empty, set
     `unknown["tests"] = gate_template.registry_why(reason, "which green tests are proven is not known")` and `unknown["tests_code"] =
     "tool"`, and return None.
   - `:1536`: `verdict not in APPROVING` becomes `not gate_template.acceptable(verdict, "critic_review.proven")`, with
     `verdict = L.verdict_of(entry)` kept.
   - `_r_proven` None branch: `_unknown_line(facts, "tests" if "tests" in facts["unknown"] else "ledger", "which tests are proven")`.
   - Test rows (`test_report_facts.py`, the Proven-counts row near :407-418): it stays green with `approved_with_fixes` counted; add
     unreadable registry -> `facts["tests"] is None` and the rendered block says "Unknown which tests are proven — a gap of the
     factory's tool, not of the product: the gate registry cannot be read".

6. `scripts/handoff_check.py::_claim_rollcall`
   - After the `doc is None` and `found is None` returns: when `gate_template.registry_problem()` is non-empty, return
     `(None, gate_template.registry_why(reason, "whether the form's outcome approves is not known"))`.
   - `:966` becomes `if gate_template.acceptable(outcome, "critic_review.rollcall_claim") and found["verdict_ceiling"] == "partial":`.
     Delete `import report_facts` there.
   - Test rows (`test_handoff.py`, the roll-call claim rows): `approved_with_fixes` with a partial ceiling gives False (kept);
     unreadable registry gives `(None, <reason naming the registry>)`.

7. `scripts/traceability.py::Story._review_basis` and `scripts/factory_dashboard.py::instance_basis` (F2 (a))
   - `verdict not in ("approved", "approved_with_fixes")` becomes `not gate_template.acceptable(verdict,
     "critic_review.basis_report")` / `"critic_review.basis_dashboard"`, with `verdict = L.verdict_of(entry)` kept.
   - Test rows: `test_traceability_report.py:249` and `test_factory_dashboard_joins.py:198` (`approved_with_fixes` shows its level)
     stay green; add unreadable registry -> words without the level, no exception.

8. `scripts/ledger.py::test_state` (F2 (a))
   - `:1191` `review not in {"approved", "approved_with_fixes", UNVERIFIED}` becomes `review not in C.CRITIC_VERDICTS`. The
     behaviour is identical because `rejected` returned at `:1189`.
   - Test row: the existing `test_ledger.py:513` (`approved_with_fixes` is green) and the `review_unrecognised` rows stay green; no
     new row (a refactor with no behaviour change).

## 5. Edges and their invariants

- E1 readable registry: every site decides as today for every word of the tables in items 1-2. Invariant: no word that did not
  approve or close yesterday does today, and the reverse.
- E2 unreadable registry (`registry_problem()` non-empty). Each site:
  - window note: the registry note (item 2);
  - `validate_window`: gaps, unchanged (E3 rows at :2865-2867);
  - stamp: `not_approved` (hold);
  - gate B: exactly one reason;
  - report: `tests` None with the registry reason;
  - claim verifier: `None` with the reason;
  - displays: no level.

  Invariant: an unreadable registry never gives a stamp, a counted proven test, a skipped claim check or a silent "no lifecycle
  demand" at gate B (AR-28, FR-59). The story-level door is the controller's existing dispatch stop `REGISTRY_BLOCK` (unchanged).
- E3 word absent, None, `""`, a non-str or a list: not approving, no gap closed. The ledger keeps `review_skipped` /
  `review_unrecognised` (unchanged). Invariant: the empty outcome is a hold (AR-23).
- E4 padded or case-variant word: each site keeps its reading (F5 (a)), pinned by rows. Invariant: no site widens what it accepts in this node.
- E5 `said` containing `; `, a newline, or over 60 characters: shown folded, `;` -> `,`, cut. Invariant: the note's first `"; "` is
  the builder's what/door boundary, so `_explain_parts` prints the builder's door, never a piece of the record's value.
- E6 note vs gap: a `review` note exists for an instance exactly when `validate_window` raises `review:<id>` for its kind. Invariant:
  a review note never explains another gap (m8). Today's handed+`unverified` and gapped+`unverified` notes go; the notes change, the
  gaps do not.
- E7 `approved_with_fixes` inside the window stays a review gap for ran and handed (rows 2854 and 2860 unchanged), and it stays
  approving after the window. Invariant: no `critic_review` consumer is called by `acceptance` or `window_record`, and no
  `s5_window` consumer by the post-window sites.
- E8 consumer scope: each accept site's literal consumer is a key of its own row (RD1-25), and consumer ids are unique (m10).
  Invariant: a site cannot borrow another row's `accepts`.
- E9 a word in two rows: `approved` (matched) and `unverified` (not_applicable:static_review) have the same class and reason code in
  both rows. Invariant: one word never has two classes.
- E10 TEMPORAL: item 1 creates `critic_review`. Before it exists, `acceptable(..., "critic_review.<c>")` is False everywhere, so
  every stamp would hold. Hence the row and every site land in ONE commit (AR-22: a producer and its readers change together).
  Test: the injected registry without the row gives False (item 1).
- E11 a new word added to `contract.CRITIC_VERDICTS` without the row is red (the set pin). Invariant: an unmapped word is a factory
  defect (FR-19), never silently not approving.
- E12 POSITIONAL:
  - `lifecycle_reasons`: the registry check comes before the loop. Invariant: no per-case reason is computed from a word the
    registry could not judge.
  - `_claim_rollcall`: the check comes after the no-form and no-roll-call returns and before the approving test. Invariant: the
    ceiling check is never skipped into the digest comparison because the registry is unreadable.
  - `build`: the review note is decided once the kind is known, and the probe-gap block replaces it. Invariant: at most one review
    note per instance, of its final kind.

## 6. The reused function in a more consequential role (designer rule 1)

`gate_template.acceptable` moves from advice to the gate at the stamp, gate B, the report count and the claim verifier. Its error
direction is fixed: toward "not acceptable", never raising (`gate_template.py:9-13`). The safe side differs by site:

| Site | `False` means | Safe? | What keeps it safe |
|---|---|---|---|
| stamp | hold | yes | — |
| report proven | not counted | yes, if said | E2 unknown line |
| gate B lifecycle | no stamp demanded | NO on an unknown registry | E2 one reason before the loop |
| claim verifier | ceiling check skipped | NO on an unknown registry | E2 `None` before the test |
| displays | level not shown | yes | — |
| window note | note written | yes | E2 registry text |

Adversarial inputs that must stay on the safe side are the rows of items 1-3: `"Approved"`, `" approved"`, `"approved "`, `""`, `None`,
`["approved"]`, `"\u0430pproved"`, `"approved;rejected"`, a 10,000-character string, an unreadable registry, and a registry without the row
or without the word.

## 7. Readers of every touched file (designer rule 7)

Greps (Grep tool) over `tools/`, `.githooks/` and `.claude/` for the touched files' names and the changed names:

- `APPROVING|GAP_ORIGIN|BLOCKED_REVIEW_VERDICT|gate-registry\.json|s5_window` in `tools/`: 13 hits in 4 files.
- `case_stamp|report_facts|check_delivery|window_record|handoff_check|traceability\.py|factory_dashboard|ledger\.py` in `tools/`: 52
  hits in 13 files.
- Both sets in `.githooks/`: 0. The positive control `python|tools` gave 22 hits.
- `.claude/agents`: 0. The positive control `APPROVING|handoff_gate|scenario_walk` gave 3 hits, from the second term.
- `.claude/settings.json`: 0. The positive control `gate-registry|hooks` gave 16 hits.
- A whole-`.claude/` grep timed out on `.claude/worktrees/` (other sessions' copies, not live readers).

| Touched file / name | Reader | Verdict |
|---|---|---|
| `gate-registry.json` | `gate_registry.load_registry` (the one reader), `gate_template` | unchanged |
| | `tests/test_gate_registry.py` D13 pins | changes in this stream; also in RD1-25/26/28 (F6) |
| | `tools/source-split-carriers.json:15,35`, `tools/source_split.py` (fixtures), `tools/test_quarantine.py:2199` (path list), `tools/controller-blocks-gen.py:352` (comment) | unchanged |
| | controller dispatch stop `REGISTRY_BLOCK` | unchanged |
| `case_stamp.APPROVING` (deleted) | `tests/test_case_stamp.py:211` | changes in this stream (item 1) |
| `case_stamp.instance_hold` | `check_coverage.collect_cases`, `check_delivery._cases_held`, `case_stamp.plan` | unchanged code; same answer on a readable registry, hold on an unreadable one |
| `report_facts.APPROVING` (deleted) | `handoff_check._claim_rollcall` | changes in this stream (item 6) |
| `report_facts._tests` / `facts["tests"]` | `_count_by_tests`, `_changes`, `_r_proven` | `_r_proven` changes (item 5); the others already handle None |
| `window_record.GAP_ORIGIN["review"]` | `_explain_parts` | unchanged code, new text (item 2) |
| `window_record.GAP_ORIGIN` (other rows) | `tests/test_probe_gap_word.py:594`, `test_probe_gap_door.py:104`, `test_run_freshness.py:483`, `test_s5_precheck.py:3185`, `test_window_record.py:992-1047, 2784, 3116` | unchanged (other keys) |
| `window_record.py` (module) | `tools/controller-blocks-gen.py:145,186-194` (command texts) | unchanged |
| `check_delivery.lifecycle_reasons` | gate B assess; `tests/test_delivery_ownership.py:261` | unchanged code; one new reason head checked (item 4) |
| `factory_dashboard.py` | `tools/lint-baseline.json:43-59` (unused imports of other names), `tools/dup-baseline.json:139` (`_has_factory_activity`) | unchanged; the builder adds no unused import |
| `traceability.py`, `check_delivery.py` | `tools/test_collect_intake.py`, `test_piles_split.py`, `test_forge_metrics.py`, `tools/fixtures/dispatch_manifest/K1,K3,K8.txt` (path strings in text fixtures, no import) | unchanged |
| `ledger.py` | no hit in `tools/`, `.githooks/` or `.claude/` | — |
| `handoff_check.py` | `tools/test_dod_gate.py:1254` (the name `handoff_check` in another sense: a function name of the dod gate) | unchanged |
| `judgment-census.json` | `tests/test_judgment_census.py`, `tools/architecture_gate.py` | a row only if the census asks; AR-20 counts |

Not a hit: `tools/warn_density.py` (`in_window_records` is a word, not the module); `tools/piles_testkit.py:54` (a fixture string).

## 8. Siblings

- Sweep of the artifact (rule 9). `window_record.build`, the enclosing block, holds three review-word sites (m6), applied in item 2.
  `GAP_ORIGIN`: the `review` row is applied (item 2); the other rows are not applicable (they are not review words). The registry's
  other rows with words read outside it: `test_identity` (RD1-26) and `probe_verdict` (RD1-28) are other nodes.
- Axis 34 (one road). After the change the review word has two roads by design, one per stage (`s5_window` in the window,
  `critic_review` after it). Each is a data row read by a consumer key; no literal list is left (AR-1 grep, §2).
  `critic_rollcall.APPROVING_VERDICTS` is a third road for the S4 roll-call: F3.
- Axis 5 row "The critic's verdict word in the ledger": `ledger.verdict_of` stays the one strip-reading; the row gains a line for
  `critic_review` (Lead doc edit). F5 records the raw/strip divergence.
- RD1-28 (probe_verdict words) is the nearest sibling with the same shape: converted sites keep a word list beside the registry.
  No file overlap except `gate-registry.json` (row-separated) and `test_gate_registry.py` (F6).
- Analogs, reported and not taken:
  - `s5_plan._review_form` reads `plan_verdicts`: a different vocabulary of a different gate (plan review). Not applicable.
  - `references/verification-levels.json` `review_words` (read by `proof_level.review_words`) maps the same words to display text.
    A data carrier of display, not acceptance; unchanged.

## 9. Small choices closed by the designer

1. One consumer per site, not one shared consumer. This follows the registry's own pattern (`test_identity` has four ["matched"]
   consumers) and the brief's words.
2. `critic_review.words` = all four words of `CRITIC_VERDICTS`, so a known non-approving word is told from an unknown one (FR-19),
   pinned to the code vocabulary (E11). Measured risk: none of the six site functions compares `rejected` or `unverified` as a literal.
   The builder re-measures with `--sites`.
3. `handoff_check._claim_rollcall` gets role `validate`, and the two displays get `measure`: they verify or show, they accept nothing.
4. `window_record.review_note` gets role `accept` under `s5_window`: it decides whether the word closes the review.
5. Sites pass the word string, not the entry, so each site's reading stays explicit (F5).
6. `<shown>` uses `detector_verdict.one_line` (an existing public one-line survivor) rather than a fourth local fold.
7. The `lifecycle_reasons` registry line keeps the existing head `case lifecycle not checked: `, so it reads as the existing
   join-unreadable line does.

## 10. Reading trail

- Read:
  - the finding;
  - `t-1084` review (Grep, lines 27, 116, 146);
  - `gate-registry.json` whole;
  - `gate_template.py` whole;
  - `gate_registry.py` 200-249, 485-889, 935-986;
  - `acceptance.py` 28-39, 1140-1184;
  - `window_record.py` 290-349, 443-447, 1445-1474, 1600-1779, 1808-1837, 1937-1976;
  - `check_delivery.py` 798-807, 820-898;
  - `case_stamp.py` 305-349;
  - `report_facts.py` 55-66, 1507-1560, 3082-3090, 3660-3671;
  - `handoff_check.py` 945-974;
  - `factory_dashboard.py` 870-894;
  - `traceability.py` 866-893;
  - `ledger.py` 1027-1041, 1170-1204;
  - `contract.py` 2205-2220;
  - `s5_plan.py` 960-979;
  - `test_window_record.py` 2830-2879;
  - `test_gate_registry.py` 1060-1104;
  - `test-layers.json` 455-544;
  - `design/architecture.md` 134-223;
  - `docs/TESTING.md` (Grep 91-98, 137-138, 239-241);
  - `docs/SIBLING_MAP.md` 589-600 and Grep of axis 5 lines 138, 445-447;
  - `plans/piles/rules-debt/batch-1-phase-2.md` 1-60;
  - the RD1-25 finding;
  - `tools/architecture_gate.py` (Grep 4-68);
  - `tools/dup-baseline.json` 128-145;
  - `tools/lint-baseline.json` 40-59.
- Greps:
  - `APPROVING|approved_with_fixes` over `scripts/*.py`;
  - `s5_window\.|acceptable\(` over `scripts`;
  - `GAP_ORIGIN` readers;
  - `review_words`;
  - census rows (positive control `case_stamp|check_delivery` hit);
  - the rule 7 greps of §7 with their controls;
  - `def` uniqueness of the six site functions (each unique in its file).
- Not measured: the zones of other piles' batches in work for the widened owns (F2: the Lead's rule 4 check). The D13 after-values
  are an estimate, not verified.
- Contradictions with the brief:
  - "four readers" is more: `handoff_check`, `traceability`, `factory_dashboard` and `ledger` are not in the finding (m3-m5).
  - `window_record.build` holds a third copy at `:1649` beside `:1641` and `:1742` (m6).
  - The brief's line numbers held exactly (860, 317, 1641, 1742).

## Lead decisions (Lead, 17.11.2026, Opus; «решила сама»)

F1 = (B) a separate `critic_review` row; F2 = (a) owns widened as §0 (`handoff_check.py` is also in the FV3-19 node: different functions, the later of the two merges main and re-runs its witness, TEAMWORK §3); F3 = (a) a new node RD1-32 for `critic_rollcall.APPROVING_VERDICTS` after RD1-29; F4 = (a) every review door ends with the person's door; F5 = (a) each site keeps its reading, pinned by `" approved"` rows; F6 = (a) RD1-29 starts after RD1-25 lands on main.
