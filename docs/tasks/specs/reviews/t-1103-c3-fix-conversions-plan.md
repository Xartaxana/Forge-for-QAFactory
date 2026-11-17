# t-1103 — plan critic: C3 fix-round cards RD1-26, RD1-28, RD1-29 (+ residual nodes RD1-28b, RD1-29b)

Reviewed: `docs/tasks/specs/20261117-rules-debt-c3-fix-conversions-cards.md` (draft + Lead fork decisions), against critic t-1084,
the phase-2 C3-b2/C3-d pattern, and the wave-3 g/h r2 cards. Code: the C3 wave tree
`.claude/worktrees/agent-ac40b44fb0a175afa/ai-packages/qa-factory/` (HEAD f1265890). NOTE: that tree carries UNCOMMITTED edits of another
session (`controller.py`, `gate_template.py`, `proof_level.py`, `test_gate_registry.py`: `registry_why` loses `stop=`, `REGISTRY_BLOCK` is
added, `WHY_*_REGISTRY` become `*_TAIL`). I measured on the working copy; none of those hunks touches a card site.

Method: every site expression grepped; the three cards SIMULATED on a scratch copy of `scripts/*.py` + `references/` (registry rows and
code edits as the cards prescribe), then `GR.analyse`, consumer tables through `gate_template.acceptable`, a 729-combination
equivalence run of `_compare_shas`, `_job_contract` cases, and the six-window smoke, before/after.

## Verdict

**NEEDS WORK (fit_with_fixes).** The facts of §0 hold and the measured premises match the expectations. The fork decisions are mostly
right. Two are wrong as written: F-2 (a), and the blocker named for F-7 (a). Three of the edges in RD1-29 lose a refusal or print a
false text. The cards are dispatchable after fixes 1-13 below. All of them are text edits of the spec; none needs a new decision of the
owner. Fixes 7 and 8 carry proposals that the Lead decides (rule 6). Whether to accept is the Lead's decision.

## Key 1 — facts by trail (reproduced)

- §0 fact 1: confirmed. `probe_verdict` registers only `probe_by_code` producers. P3 :1422 reads the product record (`red_sandbox.product_verdict` :1478-1489). P1 :1508 reads either record. P4 `acceptance.py:1227` reads the window block (`window_record.py:885`, `PARTIAL_PRODUCT`/`MODEL_CHANGED` :720-721). P2 :1536 reads the mismatched words. :1552 reads `survived`, which is in no row.
  - Missed by the designer: `window_record._probe_scope_notes:664` and `unproved_keys_text:698` also read `intended_failure`. Both are display readers (fix 6).
- §0 facts 2-4: confirmed (`test_window_record.py:2854,2860`, the `approved_with_fixes` gap rows). The census grep has 16 hits; `validate_artifacts` has 4 lines, not 2, and all of them are the shape rule.
- Correction: `_claim_rollcall` serves the S4 case critic's form ONLY. The claim `the_verdict_was_computed_by_rollcall_not_typed` appears in `handoffs/s4-case-critic-to-designer.yaml` alone. It is not on the S5 plan-critic form.
- Every site line exists with the quoted text: acceptance :177, :211, :1227; run_history :221, :256-259; proof_level :1422, :1508, :1536, :1552; case_stamp :344; report_facts :63, :1536; check_delivery :860; handoff_check :966; window_record :1641, :1649, :1742.
- §0 fact 6: confirmed (the quarantine lines, `test_receipts_per_function.py:30`). One more fact: `test_run_history_identity.py` (it pins `_compare_shas`/`_job_contract`) is quarantined too, in cohort 8073673.
- §3, measured on the wave tree: `--check` exit 0; D13 = 150 items / 53 triples (the pin agrees).
  - RD1-26 alone: +2 items / +1 triple. Both are in `_compare_shas`: `verdict != 'unknown'` and `('unknown', 'unknown', _first_sha(red), _first_sha(green))`. S1-S3 hold no counted comparison.
  - RD1-28 alone: +1 / +1 (`_probe_record_defect`).
  - RD1-29 alone: -1 / -1 (the `build` triple leaves). No F-f, no new UNREGISTERED item.
  - All three: 152 / 54. With fix 1's form it is 154 / 54 (the duplicate tuple text is covered by the same allow entry).
- Behaviour on a readable registry: `_compare_shas` on 729 combinations and `_job_contract` (4 cases) are EQUAL before and after. The six-window smoke is EQUAL. Consumer tables: W1-W4 accept exactly {approved, approved_with_fixes}. The window consumers are unchanged. `probe_verdict.proved` accepts only `intended_failure`.

## Key 2 — meaning of the rows

| card | word | before | after (readable) | unreadable registry |
|---|---|---|---|---|
| 26 | raw/instance/instance_code/file_code (same_test), same (compare_identity) | accepted per site | same | S1 False, S2 False plus the registry why, S3 `{}`, S4 see fix 1. All of these flips are intended (AR-28) |
| 26 | different/unknown/""/None/case variants | refused | refused | refused |
| 28 | intended_failure (dict) | proved | proved | P1 `own=None`, P3 None (the probe runs), P4 `sensitivity:`. Intended |
| 28 | any other word, no key, None, `[]` | not proved | not proved | same |
| 28 | bare str `"intended_failure"` | crashed later or was False | **True** (measured, fix 6) | False |
| 29 | approved, approved_with_fixes | approve at W1-W4 | same; still a gap at the window | W1 hold, W2 not counted, W3/W4 see fixes 3-4, W5/W6 a note for every instance (fix 5) |
| 29 | unverified, rejected, "", None, case variants, non-str | do not approve | same | same |

No input changes its outcome on a readable registry. Every flip is on the unreadable-registry branch. All of them are intended, except the
three named in fixes 1, 3 and 5.

## Key 3 — forks

- **F-1 (a): right.** `_compare_shas` "same" drops a pair (`_make_pair` returns None only on "same", :698-700). That is an acceptance.
- **F-2 (a): WRONG; take (c)** (fix 1).
  - "Skip the identity basis" cannot tell `same` from `different` without the literal `verdict == "same"`. That is an acceptance-shaped comparison, which A26 counts and the card's own item 5 makes a stop.
  - Written literal-free, it skips both verdicts. Measured on broken registries: 56 of 729 combinations flip from `changed` to `same/file`. That drops a red/green pair (the case: code sha differs, file fingerprint equal, a tooling change). That is the unsafe side.
  - The designer objects that (c) "ignores an equal block fingerprint that would decide today". That is false: the file basis is reached only when the identity verdict is `unknown` (:257, :260).
  - (c) measured: readable EQUAL. Broken: every identity verdict becomes `unknown` (504 flips, all to `unknown`). No pair is dropped, nothing is stated as a fact (FR-41), and no finding comes once the two allow entries are in.
- **F-3 (a): right with a condition.** The equivalence holds (`_kept(None)` is `{}`, so only `raw`/`""` are possible). But E2's claim that "row (ii) pins the dict shape" is false. No row fails if a later edit passes an identity-bearing dict. Fix 10.
- **F-4 (a): right with conditions** (fix 6): a dict guard; the producers registered as `produce`; the `decides` text corrected.
- **F-5 (a): right.** A wrong True only refuses a repeat, behind the identity predicate (:1537). `validate` is honest, and the precedent is `execution_request.green_over_same_bytes`.
- **F-6 (b): right with conditions** (fix 11).
  - It is one road in fact. Under (a), `approved_with_fixes` would be `matched` in one row and a review gap in the other, so one word would carry two classifications (P31, AR-15).
  - The class stretch has a precedent (`unverified` = `not_applicable:static_review`). The ONLY reader of `verdict_map` classes is `gate_template.acceptable`. My grep for `verdict_map|reason_code` over `scripts/*.py` found no other class reader.
  - Pins, measured: no status, split, `EXPECTED_*` or F4 move; D13 -1/-1. Option (a) would move all four, colliding with every wave-3 card.
  - Cost the designer missed: W4 is the S4 CASE critic's form. The row would then govern another stage and another addressee.
- **F-7 (a): its blocker does not hold** (key 4, fix 8).
- **F-8 (a): right with a condition** (fix 5). The flip is intended: a handed `unverified` loses a false note.
- **F-9 (a): right with conditions** (key 7).
- **F-10 (a): right.** This review covers the RD1-28 clause.

## Key 4 — residual nodes

- **RD1-28b can ride inside RD1-28.** Nothing blocks it.
  - Tests: `test_probe_by_code.py` and `test_red_sandbox_probe.py` are keep files, and they already pin the `survived` answer (:2606-2615, :500-508).
  - Collisions: the registration is JSON only, and `window_record.py` code is untouched.
  - Simulated: `survived` added as `mismatched`, :1552 moved into `_probe_record_defect`, and `red_sandbox.product_verdict`, `request_status`, `window_record._receipt_block`, `_probe_from_receipt` registered `produce`. Result: +1 item / +1 triple over RD1-28 (`request_status`'s `== 'survived'`), no findings.
  - The one decision (Lead): `survived` is `mismatched`. The product record's docstring says the broken product survived the test, which is a test defect, the twin of `no_failure`.
  - `probe_defect`, `partial_product`, `model_changed` need no word: no site compares them, and a word outside the vocabulary is already False. The `decides` text says so.
- **RD1-29b can ride inside RD1-29.**
  - The stated blocker is false. KEEP files cover the three modules: `test_case_key_identity_join.py` (traceability, factory_dashboard, ledger), `test_pinned_lifecycle.py`, `test_ledger.py`, `test_sides_ledger.py`.
  - Without it, RD1-29's own line `AR-1 -- the approving pair leaves code` is false at commit: `traceability.py:884` and `factory_dashboard.py:887` keep the literal pair.
  - Decisions the card must take (fix 8): the two display sites get their own consumer (e.g. `s5_window.shown`, accept). `ledger.py:1191` becomes `C.CRITIC_VERDICTS` membership; this is equivalent, because `is_rejected` returns first (:1188). For `_sent_back_lines:2268` (`== "rejected"`), either route it through one reader or write one `decides` line calling it a display.
  - Item 1's "rejected is compared nowhere after this card" is false: `window_record.py:2268` and `ledger.is_rejected:1041` still compare it.

## Fixes (all before dispatch, this round)

1. **RD1-26 item 5 / E4 / F-2:** replace with (c). `if verdict != "unknown" and registry_problem(): return "unknown", "unknown", _first_sha(red), _first_sha(green)`.
   - Rows: (v) code equal, registry broken, any file shas → `("unknown","unknown",…)`. (vi) code different, registry broken, file equal → `unknown`, never `same`.
   - Allow entries, verbatim: `verdict != 'unknown'` and `('unknown', 'unknown', _first_sha(red), _first_sha(green))`.
   - D13 is by measurement (simulated: +4 items / +1 triple for RD1-26).
2. **Registry sentences:** RD1-26 item 3 and RD1-29 items 3 and 6 hand-build the text. The RD1-29 forms even differ (` - `, and no "a factory defect"). They must call `gate_template.registry_why(problem, tail)` (2-arg form only; the `stop=` keyword is being removed in the tree).
   - Each new user gets a row in the RD1-27 family table (`test_gate_registry.py:1188-1199`).
   - §6's "fix 2's builder absorbs them later" is stale: f1265890 landed it.
3. **RD1-29 W4 (E5):** returning `(None, …)` before the digest check turns the digest refusal, which can be measured without the registry, into `no_verdict` (`handoff_check.py:2035-2038`: None is neither accepted nor refused).
   - On a registry problem, skip only the outcome test, run the digest checks, and return False on a digest refusal. Else return `(None, registry_why(...))`.
   - Add a row: broken registry plus a wrong digest → False.
4. **RD1-29 W3 (item 3, E3/E4):** "the loop is not entered" drops demands that do not depend on the word: green tests, and `_pinned_proof_reasons`. It also departs from the function's own `not_read` precedent, where the loop runs and one line is appended (:894-896).
   - Fold it per test: a non-green test whose word cannot be read sets a flag; one registry line is appended at the end.
   - The reasons' owner is `factory_record` (:2619), so FR-46 holds.
5. **RD1-29 W5/W6 (E6/E7, F-8):** on an unreadable registry the notes say false things. A stopped `unverified` instance gets "the verdict is `unverified` … such an instance's verdict is `unverified`". An `approved` instance gets "is not `approved`" (FR-10, FR-41).
   - `_static_review_note` and the generic note print `registry_why(...)` when `registry_problem()`.
   - The F-8 invariant "for every instance" overclaims. Build's kinds (`identity in blocked`; `handed_ok`; a gap set under `proof_required(entry, manifest)`) are not validate_window's (`outcome == BLOCKED`; `claimed_handed`; `proof_required(item, {})`). State the derivation; a divergence the table finds is a stop.
6. **RD1-28 item 2:** `probe_proved` must be `isinstance(record, dict) and acceptable(...)`, with a row for a bare str.
   - Item 1's clause: "its one ACCEPTING reader", naming the display readers `window_record:664, :698`.
   - Register `red_sandbox.product_verdict` and `window_record._receipt_block`/`_probe_from_receipt` as `produce` (measured: 0 new items). This puts the E11 relaxation in data (AR-22), not in prose only.
7. **RD1-28b → into RD1-28** (key 4). The Lead decides whether `survived` is `mismatched`. +1 item / +1 triple, by measurement.
8. **RD1-29b → into RD1-29** (key 4): the three decisions named there. Correct the `rejected` prose. The AR-1 grep becomes the literal pair, not only `APPROVING`.
9. **RD1-26 owns:** the mechanical-round world already exists in KEEP `test_blocked_by_env_window.py:627-630`, and item 3 tells the builder to use it. Add that file to owns, or say the rows stay in `test_proof_level.py`.
10. **RD1-26 E2:** drop "pinned by row (ii)". Either pin the call's two dict displays (one `input_hash` key each) beside the K-C census (`test_proof_level.py:1439`), or name it as an accepted residue.
11. **RD1-29 item 1 (F-6):** `decides` names each outside consumer with its stage and whose word it reads. The S5 code critic's manifest `critic_verdict` feeds stamp, proven and lifecycle. The S4 case critic's `review.outcome` feeds form_outcome. `addressee` gains `role:qa-case-critic`, or the text says why not.
12. **RD1-29 E7:** name the W2 residue: on an unreadable registry the report undercounts proven tests with no cause shown, the same as the stamp's `not_approved`.
13. **F-9 / §4:** state that owns overlap in three files (`gate-registry.json` row-disjoint, `test_gate_registry.py` D13 + the RD1-27 table, `test_window_record.py`). PROJECT.md «Командная работа» п. 3 allows this: the later merger merges main and re-measures. RD1-28's window rows must not land in `c3_d_review_word_through_the_registry`.

## Key 5 — architecture and rules

- Kept and named after the fixes: AR-13, AR-15, AR-22, AR-28, AR-29, AR-20.
  - AR-1 is false without fix 8.
  - AR-22 is kept only with fix 6's producer registration.
- FR-59: with fix 1 no gate decides on an unknown. Without it, S4 is either a fact on an unknown (b) or a corner unsafe drop (a).
- Census: only `validate_window` (shape) and `window_record.build` (shape) have rows. No new refusal unit; `_claim_rollcall` returns tuples (grep of the census over every touched function).
- Pins the cards move: D13 count and triples, the allow-list (RD1-26), and the RD1-27 table (missing from the cards, fix 2). The cards name the rest. Lint-baseline `HandReaderInput` is named.

## Key 6 — edges

The edge lists are complete except for: E4 of RD1-26 (fix 1), E5 of RD1-29 (fix 3), E3/E4 of RD1-29 (fix 4), E6/E7 of RD1-29 (fix 5), the
bare-str input of RD1-28 (fix 6), and the W2 residue (fix 12). TEMPORAL: the base is still moving (the uncommitted `registry_why` edit). The
cards say "builder re-reads every line on its own base"; fix 2 pins the call form that survives either state. The tests are table rows
with expected values from `decides` and the docstrings, and each can fail. The twin-pin replacement (`stamp` == `proven` over
`CRITIC_VERDICTS`) fails on a data drift.

## Key 7 — order and collisions

- F-9 (a) holds with fix 13.
- Wave-3 g/h (r2 :195-198, :519-522, :678-679) own `baseline_contract.py`, `controller.py` (C3-g2, HOT) and `delivery_summary.py`. They share no production file with the three cards.
- Shared with g/h: the D13 pin and the RD1-27 table (C3-g adds "one RD1-27 row"). The later merger re-derives both. `EXPECTED_*`, split and F4 are moved by g/h only, since F-6 (b) moves none of them.
- k1-k4 are not in my manifest. The designer's §4 claim (k2/k3 add `provenance_acceptance` allow entries ahead in registry order) was not verified.

## Duplication and consistency

Found: three hand-built copies of the registry sentence (fix 2), and the literal pair surviving at two display sites (fix 8). Grepped:
`registry cannot be read|registry_why`, `APPROVING\b`, `approved_with_fixes` over `scripts/*.py`.

## Code quality

None found at the plan level. The `_job_contract` loop and the `_static_review_note` helper are small. Grepped: the prescribed bodies.

## One road

Found: W3/W4 readers outside the row, and the two display copies (fix 8). F-6 (b) is the one-road option (fix 11). No language or project
key is read (checked: the prescribed conditions).

## Tests

Fit after fixes 1, 3, 4, 5, 6, 9 and 10 adjust their rows. All rows go into keep files. `test_handoff.py` holds the `_claim_rollcall` table
(:2658) and is a keep file.

## Trail

- Read: the cards file (whole), t-1084 (whole), wave-3 g/h r2 (owns, greps), `critic-diff-brief.md` :8-140, `critic_verdict.schema.json`, SIBLING_MAP :194, :449-452 (wave tree).
- Code, wave tree: gate_template (whole), gate_registry :20-100, :746-915, the three registry rows plus `delivery`, acceptance :1-14, :108-216, :1150-1240, run_history :200-265, :685-742, proof_level :821-935, :1405-1562, red_sandbox :1465-1510, window_record :318-330, :640-705, :715-890, :1630-1756, case_stamp :312-346, report_facts :60-66, :1525-1545, check_delivery :829-905, handoff_check :945-978, :2010-2040, traceability :874-892, factory_dashboard :878-893, ledger :1038-1042, :1180-1196, contract :2205-2216, the s4 handoff :55-75, test-layers.json (keep/quarantine), judgment-census.json.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "class_completeness": "Site lists verified by grep. RD1-28: two display readers of intended_failure missed (window_record:664, :698), and the producers red_sandbox.product_verdict and window_record._receipt_block/_probe_from_receipt are unregistered (AR-22). RD1-29: traceability:884 and factory_dashboard:887 keep the literal approving pair, ledger:1191 the full vocabulary, window_record:2268 and ledger.is_rejected the word rejected. The residual nodes RD1-28b and RD1-29b are not blocked (keep tests exist; simulated A26 cost +1/+1 for 28b) and ride inside RD1-28 / RD1-29. Axes 7/25 (RD1-26) are covered; axis 5 prose greps stay with the builder.",
  "fixes": [
    "1 RD1-26 item 5/E4/F-2: take (c) - on registry_problem with an identity verdict, return unknown/unknown; never skip to the file basis (measured: 56 of 729 combinations flip changed->same/file under (a)); allow entries verdict != 'unknown' and ('unknown', 'unknown', _first_sha(red), _first_sha(green))",
    "2 RD1-26 item 3, RD1-29 items 3 and 6: every registry sentence via gate_template.registry_why(problem, tail), 2-arg form; rows in the RD1-27 table test_gate_registry.py:1188-1199; section 6 is stale",
    "3 RD1-29 W4: on a registry problem skip only the outcome test, keep the digest refusal (None is no_verdict, handoff_check.py:2035); a row for broken registry plus a wrong digest -> False",
    "4 RD1-29 W3: fold per test (a non-green test with an unread word sets a flag, one line at the end) like the not_read precedent; do not skip the loop",
    "5 RD1-29 W5/W6: on an unreadable registry the notes print registry_why, not a false critic_verdict sentence; state build's kind derivation, since the note-iff-gap invariant is measured, not assumed",
    "6 RD1-28: probe_proved guards isinstance dict (a bare str is accepted today, measured); the decides clause says one ACCEPTING reader and names window_record:664,:698; register red_sandbox.product_verdict and window_record._receipt_block/_probe_from_receipt as produce",
    "7 RD1-28b into RD1-28: survived as mismatched (Lead decides), :1552 into _probe_record_defect, request_status registered produce; +1 item/+1 triple by measurement",
    "8 RD1-29b into RD1-29: display sites get their own consumer, ledger:1191 reads C.CRITIC_VERDICTS, _sent_back_lines decided; correct the 'rejected compared nowhere' prose; the AR-1 grep covers the literal pair",
    "9 RD1-26 owns: add test_blocked_by_env_window.py (the existing mechanical-round world :627-630), or say the rows stay in test_proof_level.py",
    "10 RD1-26 E2: drop 'pinned by row (ii)'; pin the two input_hash-only dict displays, or name the residue",
    "11 RD1-29 item 1: decides names each outside consumer with its stage and producer (S4 case critic review.outcome for form_outcome); addressee gains role:qa-case-critic or says why not",
    "12 RD1-29 E7: name the W2 residue (the report undercounts proven tests on an unreadable registry, no cause shown)",
    "13 Section 4/F-9: state the three shared files (registry row-disjoint, test_gate_registry D13 and the RD1-27 table, test_window_record); the later merger re-measures; RD1-28 window rows stay out of the c3_d function"
  ],
  "trail": {
    "read": [
      "docs/tasks/specs/20261117-rules-debt-c3-fix-conversions-cards.md (whole)",
      "docs/tasks/specs/reviews/t-1084-c3-b2-d-topic-code.md (whole)",
      "docs/tasks/specs/20261117-rules-debt-wave3-g-h-cards-r2.md (owns lines, greps)",
      "docs/tasks/critic-diff-brief.md :8-140; tools/critic_verdict.schema.json",
      "wave tree scripts: gate_template, gate_registry, acceptance, run_history, proof_level, red_sandbox, window_record, case_stamp, report_facts, check_delivery, handoff_check, traceability, factory_dashboard, ledger, contract (ranges in Trail)",
      "wave tree references/gate-registry.json rows test_identity, probe_verdict, s5_window, delivery; handoffs/s4-case-critic-to-designer.yaml; tests/test-layers.json; tests/fixtures/judgment-census.json; docs/SIBLING_MAP.md :194, :449-452"
    ],
    "reruns": [
      {"command": "python -B <wave>/scripts/gate_registry.py --check", "result": "A26 gate registry: no violations; 4 debt, 6 exempt; exit=0"},
      {"command": "GR.analyse on the wave tree (section 3 command)", "result": "0 findings, 150 items, 53 triples"},
      {"command": "simulated RD1-26 / RD1-28 / RD1-29 / all, measure.py", "result": "+2/+1 (2 findings: _compare_shas allow texts) ; +1/+1 ; -1/-1 ; 152/54; with fix 1 form 154/54, no findings once allowed"},
      {"command": "simulated RD1-28b on top of RD1-28", "result": "152 items/55 triples from base, no findings; new item request_status product_verdict(p) == 'survived'"},
      {"command": "eq.py: _compare_shas over 729 combinations and _job_contract, base vs all three cards (readable)", "result": "readable equal: True"},
      {"command": "eq.py with GT._READ broken: skip-all form vs (c)", "result": "skip-all: 56 changed->same/file flips; (c): 504 flips, all to unknown, none to same"},
      {"command": "six-window smoke (section 3), base vs all three cards", "result": "6 lines each; diff EQUAL"},
      {"command": "acceptable tables on the simulated registry", "result": "stamp/proven/lifecycle/form_outcome = {approved, approved_with_fixes}; review {approved}; static {unverified}; handed {approved, unverified}; proved {intended_failure}, and the bare str 'intended_failure' True"}
    ]
  }
}
```
