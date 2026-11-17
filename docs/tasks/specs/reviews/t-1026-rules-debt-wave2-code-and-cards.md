# t-1026 — critic: rules debt phase 2, wave 2 (one pass, R13-g): Part A code C3-R (5751426c), Part B plan cards

Reviewer: critic (Opus). Read on `main` = `origin/main` = `35e24f38` (both refs printed by `git rev-parse`). This is a
verdict, an input to acceptance. The decisions belong to the Lead. The forks are returned with a recommendation and are
not decided here.

## Verdicts

| part / card | verdict |
|---|---|
| **Part A — C3-R (merged)** | **NEEDS WORK, one fix round.** Six of the seven rows are honest. `reporter_rehearsal_identity` is not: its true acceptance site is unregistered (A1). Smaller items: A2–A6 |
| C3-0 | dispatchable after listed edits (B1, B2, B10) |
| C3-b1 | dispatchable after listed edits (B1, B5; F-T5's consequence text has to be corrected before the Lead or owner answers it) |
| C3-b2 | not dispatchable as written: it misses two test_identity reuse sites (B4). Also needs B1 |
| C3-d | not dispatchable as written: the re-role of `validate_window` is wrong (B3). Also needs B1 and B9 |
| S9 | dispatchable after listed edits (B6, B7). Fork F9-1 goes back to the Lead or owner with real evidence (B8) |
| FL4 | dispatchable after listed edits (B11, B12) |
| FL2 (partial) | not dispatchable. What it is missing: B13 |

---

## Part A — C3-R code review (5751426c)

**Mechanical layer.** The builder's witness is attached in `docs/tasks/handoffs/t-1009-c3-r.md`. I re-ran it as a cheap control, verbatim:
- `python -B .../scripts/tests/test_gate_registry.py` → `=== test_gate_registry: 439/439 ok ===` (35.4 s).
- `python -B .../scripts/gate_registry.py --check` → `A26 gate registry: no violations` … `7 gate(s) left as debt:` (stand_identity,
  provenance_acceptance, test_identity, live_check_demand, s5_window, baseline_identity, s5_stand_limits) … `6 gate(s) exempt:`.
The witness reproduces.

### A1 (blocking for the claim "converted per F-D1 (b)"; cheap fix) — `reporter_rehearsal_identity`: its real acceptance of its own word sits in an unregistered function; the D13 +1 is the coincidence

- The reuse decision is at `gate_preflight.py:3843`, inside `_reporter_outcome` (:3824):
  `if isinstance(hit, dict) and isinstance(hit.get("at"), str) and earlier["state"] == "same_command":` → `{"reused": …}`.
  This is a literal comparison of the row's matched word `same_command`. It consumes the word to reuse a proof, which makes
  it a true acceptance.
- `_reporter_outcome` is registered in no row (grep of `gate-registry.json` for `_reporter_outcome`: no hit; positive
  control: the same grep found `_rehearse_reporter` at :502). A26 reads row words only inside registered sites
  (docstring `gate_registry.py:26-28`). So `--sites` lists nothing at :3843.
- The only item the conversion added is `gate_preflight.py:3650 _rehearse_reporter countable['state'] == 'none'` (the
  `--sites` output line 37). That `'none'` is a word of `report_adapt.countable`'s state vocabulary {`none`, `rows`,
  `unknown`}, as the docstring of `_adaptation_state` says (`gate_preflight.py:3876-3880`). It is not the
  `earlier_proof` state {`same_command`, `command_changed`, `none`, `unreadable`} that the row's words were taken from
  (`gate_preflight.py:3956`, `onboarding_probe.py:374-394`).
- **Answer to the builder's question.** As mechanics, the count of 138 is accurate: the comparison exists, it sits in a
  registered site, and its word is in `words`. As meaning, it is a coincidence. The row's status does not come from the
  D13 count (`analyse` puts `converted` in the result from the data alone, `gate_registry.py:909-910`), so the
  coincidence does not *make* the row converted. But it does hide two things. The audit counts a helper-state comparison
  as this gate's verdict, and the comparison that really decides (:3843) is not seen. The behaviour is correct and
  pinned: the builder's new row `test_c3r_reporter_rehearsal_identity_…` drives `_reporter_outcome` and catches a
  `command_changed`-reused regression. The defect is in the registry's claim. The E-c invariant "a re-role never hides a
  literal acceptance" (cards spec :288) and F-D1 (b) "the predicate for true accept sites" are not kept.
- Calibration note: the judgment in t-989 F-S5 ("the reuse decision is a key join; no verdict word is compared") was
  mine, and it was wrong. It read `_rehearse_reporter` and missed the extracted `_reporter_outcome`. t-994 marked it
  "not re-read".
- `verdict_map` `same_command → matched` also claims more than the code does. Matched means `same_command` AND the
  durable key hits (:3841-3843; the row's `decides`: "the same command, and the key hits"). A `same_command` whose key
  misses is rehearsed again.
- **Proposed edit (Lead's choice, two options):** (a, recommended, the same treatment as test_identity) add
  `{"file": "gate_preflight.py", "function": "_reporter_outcome", "role": "accept"}`, put the row back to
  `status: debt, debt_ref: B-283`, and make it a C3-0 consumer in wave 3: `acceptable(earlier["state"],
  "reporter_rehearsal_identity.reuse") and hit`. The new test row stays as the pin. (b) Register `_reporter_outcome` as
  `validate` with a written Lead judgment on E-c, and keep the row converted. Either way: D13_TRIPLES gains
  `(gate_preflight.py, _reporter_outcome, reporter_rehearsal_identity)` and D13_ITEM_COUNT rises by the named number;
  under (a), `EXPECTED_DEBT`/`EXPECTED_CONVERTED`/the split go back to 19/8/6. Also register
  `_record_unreadable` (:3966-3971, `earlier.get("state") != "unreadable"`) as `produce`, so every comparison of the row
  word is attributed.

### A2 (fix-in-round, spec defect) — `environment_preparation`: a dead consumer

The row keeps `accepts: {"provenance.environment_preparation": ["matched"]}` (`gate-registry.json:325`; the card said
"accepts unchanged"). But after C3-R no word of the row maps to `matched` (words `blocked`/`unknown`, both unknown). No
`scripts/*.py` reads the consumer (grep `provenance\.environment_preparation` over `scripts/` minus tests: 0; positive
control: the same grep finds it in `tests/test_gate_registry.py:631,640`). This is the same class as F-T3's
`provenance.baseline` (:347). Under C3-0 such a consumer can never accept anything. **Edit:** queue it with C3-k (where
provenance consumers are decided): "remove `provenance.environment_preparation` or move it to the reader that accepts a
prepared-environment provenance". This needs a line in C3-k's card, because C3-R's owns are done.

### A3 (note) — `environment_preparation` words

`unknown` is an INPUT value the code reads (`environment_preparation.py:51,76`, `in {"", "unknown"}`). It is not an
outcome the code writes. `blocked` is also written for a capability gap (`:106`, `:171` "adapter has no … action"), which
is not an unknown fact. The words are tolerable under F-T6 (b), because the builder flagged them. To make the row fully
honest: words `["blocked"]` only. Optional.

### A4 (note) — `delivery`: the unknown-class word has no refusal

The row now declares `unknown_branch: refuse_with_door`. Its only unknown-class word is `after_checks` (owner
`person`, `gate-registry.json:255-262`). That word is a third delivery outcome (P21), not a refusal, and `addressee: []`.
The real unknowns (a kind not in the file, an unreadable file) answer `no` (class mismatched) with a factory finding
(`delivery_verdict.py:119-145`), and that part is pinned by the new rows. **Edit (text only, any later registry
touch):** `decides` says both. An unknown kind or an unreadable file → `no`, refused with the kinds-file door (factory).
`after_checks` → the person's checks (P21), not a refusal.

### A5 (fix-in-round, TESTING (f)) — a pin on a constant

`test_node_ids.py:899`: `check_eq("the block word the registry row carries is the code's", RS.NODE_ID_BLOCK, "node_id_mismatch")`
pins a constant (TESTING.md «не пишется»). The tie between the registry and the code belongs to A26. **Edit:** delete
the line.

### A6 (note) — collected_ids: deviation from the card, reported by the builder

The card asked the S-b row to assert the summary (`node_id_mismatch`, `execution_status: not_executed`). The builder
pinned the functions instead (`ids_pytest_did_not_find`, `_not_verified`, `_checked_by_the_first_collect`). The
unknown branch (an unreadable collect → "not verified", never "missing", the run goes on) is pinned with killing
power. The summary mapping of the mismatched branch is pinned only in quarantined files (`test_run_budget.py:1426-1427`
M-B11, `test_run_suite_mine.py` M-B3; `test_run_budget.py` sits in the quarantine section, `test-layers.json:9674` >
:7182). I accept the deviation for S-b. Queue line: `summary node_id_mismatch -> not_executed pinned only in quarantine | перенос: findings of the rules-debt pile | обоснование: mismatched branch, not the unknown one | подтвердил: —`.

### Seven rows left as debt (key 2)

Each one is left for a reason the spec names: stand_identity → C3-h; provenance_acceptance → C3-k; test_identity → C3-b2
(predicate); live_check_demand → C3-b1; s5_window → C3-d / F-T7; baseline_identity → C3-g / F-T3; s5_stand_limits → C3-j.
Converted rows that claim more than their code path: `reporter_rehearsal_identity` (A1) and `delivery`'s branch text
(A4). One claims less: `environment_preparation`'s consumer (A2). FR-59 holds on every code path I read: no unknown
passes. FR-1/FR-2: the doors of `delivery` (kinds file, factory) and `environment_preparation` (the missing facts named,
exit 2) are usable.

### Standing questions, Part A

- Fit to the spec (q1): items 1–9 done. Item 7's S-b row is good. A1 is a spec-level miss (the E-c table) that the code
  inherited.
- Builder decisions (q2): safe direction. It stopped at item 9 as the card required.
- Class completeness (q4): the A1 class is "a converted row's word compared in an unregistered function". Swept over the
  seven rows: `collected_ids` — `red_sandbox.py:2292 result.get("status") == "node_id_mismatch"` (unregistered) and
  `execution_request.py:3187` (an imported Name, invisible to A26) → queue: register `red_sandbox` site as
  `dispatch`/`produce` under collected_ids. `environment_preparation` — `:444`, `:616` in `execute_environment` /
  `read_object` (unregistered, produce/dispatch). `environment_property_cover` — `stand_gaps._c4` (:756-802, `covering`
  truthiness, no word). The rest: none found. SIBLING_MAP axis 4 (B-ids): listed correctly, B-255 kept open.
- Tests (q5): new rows have killing power. Expected values come from `decides`/FR-19. `tests-over:` is named and holds
  (three S-b rows the card required). A5 is the one (f) finding.
- DUPLICATION AND CONSISTENCY: none found beyond A5. Grepped: `VERDICT_KINDS_UNREADABLE` (only the new row),
  `ids_pytest_did_not_find` (only the new row), `command_changed|same_command` in `test_gate_preflight.py` (only the new
  row; positive control `uncheckable`: 5).
- CODE QUALITY: none found. New functions are 25–30 lines, depth ≤ 3.
- AR (q10): AR-13 and AR-28 are named. The card's `AR-29 -- no check unit moves` line is missing from the commit (note).
  A1 is an AR-28/E-c gap.
- JUDGMENT (q11): no judgment moved. `judgment: none -- …` holds. No census edit.
- ONE ROAD (q12): none found. Grepped the diff for language/runner names: none.
- Ratchets (q9): D13_ITEM_COUNT 137 → 138 is named in the diff. Its reason is the coincidence (A1). After A1 the count is
  re-measured and named again.

---

## Part B — plan review

### B1 (blocking for every converting card; K7/K4 TEMPORAL) — `test_gate_registry.py` pins move with every conversion, and no converting card owns them

C3-R already showed this: item 9 stopped the node. The pins are `EXPECTED_DEBT` (:55), `EXPECTED_CONVERTED` (:63), the
K-T1.2 text `"7 gate(s) left as debt:"` (:246), the K-T1.14 debt list and the split `{20,7,6}` (:322-334), the F4
`code` list (:732-735), the F4 flip control (:751-754; it flips the live debt row `s5_window`), `D13_TRIPLES` and
`D13_ITEM_COUNT` (:925-987). The cards C3-b1, C3-b2, C3-d, C3-g, C3-h, C3-j and C3-k each convert a row, and none of
them owns `test_gate_registry.py`. C3-0 owns it (one table), and C3-0 and C3-b1 can run in parallel in wave 2½, which is
a same-file collision with no order.
**Edit:** (1) Every converting card gets `owns: scripts/tests/test_gate_registry.py (the debt/converted/split/F4/D13 pins
for its own row only)` and an item: "re-measure D13 with `GR.analyse` before/after and name the raise". (2) §3 gets one
order on that file: `C3-0 → C3-b1 → C3-b2 → C3-g → C3-d → C3-j → C3-k → C3-h` (or the merge rule of D-0048, which needs
the pins of both sides to be green). (3) C3-0 rewrites the F4 flip control on an in-memory copy row with
`vocabulary: target`, not a live row. Otherwise the control dies when the last `target` debt row converts (C3-d makes
`s5_window` `code`).

### B2 (fix-in-round, K1) — C3-0 E6: a false negative

"before C3-b2/C3-g/C3-k, no consumer id exists in the registry". Two exist: `provenance.environment_preparation`
(`gate-registry.json:325`) and `provenance.baseline` (:347). No script reads either (A2, F-T3). **Edit:** "two consumer
ids exist and are read by no script (A2, F-T3); C3-k/C3-g remove or move them; no real call of `acceptable` exists
before C3-b2".

### B3 (blocking for C3-d; K2/K8, E-c judged as asked) — `acceptance.validate_window` is a true acceptance of the critic's review word, not `validate`

`acceptance.py:1171` `elif item.get("review", {}).get("verdict") != "approved": gaps.append("review:" + identity)`.
Also `:1161` `not in HANDED_REVIEW_VERDICTS` (`("approved", "unverified")`, :34), and `:1156`/`:1167`
`!= BLOCKED_REVIEW_VERDICT`. The function accepts the critic's verdict word in order to close a review. If it is
re-roled `validate` after its words become `code`, these acceptances are allowed silently (the role-allow rule,
`gate_registry.py:37-41`). That is exactly what E-c forbids. `window_record.verdict` → `produce`: holds (it builds
problems and `info`). **Edit for C3-d item (2):** `validate_window` stays `accept`. C3-d then needs C3-0 and a consumer
(`s5_window.review: ["matched"]`, with the review words `approved` → matched, `unverified` → … per the handed rule), or
the review acceptance becomes its own row with a predicate call. Queue: `C3-0 → C3-d`. Under F-T7 (i) the registry
correction is otherwise as drafted.

### B4 (blocking for C3-b2; K1/K8, class) — two test_identity reuse decisions are not in the card

- `proof_level._product_receipt_repeat` (:1379 `and same_test(now, proof_identity(record)) and …` → hit, called from
  `already_probed` :1515). It is a reuse acceptance by truthiness, the same shape as :1492/:1507. It is registered in no
  row.
- `proof_level._run_freshness` (:939 `if same_test(now, …) in ("instance", "instance_code"):`). This is a literal
  comparison of the row's words in an unregistered function (axis 25, freshness).
**Edit:** item (2) adds `_product_receipt_repeat` (route it through `acceptable(…, "test_identity.probe_repeat")`, owns
+1 function, one S-b row). `_run_freshness` is registered (role per the plan critic of C3-b2: it decides whether a run
row still speaks for the test, so it is a true accept → predicate, or a named residue with a node). Siblings line: axis
25.

### B5 (fix-in-round before the fork is answered; K5/K9) — F-T5's consequence statement is incomplete

The fork says that under (a) the owner's «да» "bites only on rows added by hand into a measured manifest". The writer
facts say otherwise. `manifest_from_tests._novelty_block` returns None by policy V2 when the base is not S0 and the
value is not in `NOVELTY_KEPT_WITHOUT_S0` (:835-840). Such rows are keyless in a manifest where other rows are keyed,
and (a) asks about them. A whole-call failure (`except` at :922-925, note "novelty could not be measured", every row
keyless) reads as "a legacy manifest", and (a) never asks: the case where nobody measured anything is the one that
escapes. **Edit:** rewrite the consequence with these carriers. Recommendation on F-T5 stays (a) for in-flight safety,
with one addition: the writer's failure note becomes a manifest-level marker, so an all-keyless manifest written by THIS
writer is asked. That is a new field, so the card names both worlds. If the Lead declines, the owner is told the
whole-failure gap in plain words.

### B6 (fix-in-round; K4, error direction) — S9: `names_whole` lets a word for one instance lift a review gap of another

Instance ids carry spaces (P-c, real). `names_whole` treats a space as a whole-word edge (`contract.py:152-153`:
the right edge refuses only `[\w-]` and `. : / \ [ @` followed by a non-space). So the word `review:A b — …` for
instance `A b` also names `review:A` for an instance `A`. With Playwright titles, one title that is a prefix of another
followed by a space is likely. It is also case-insensitive (:149). **Edit to §2.2 item 2 / E4:** the review rule
matches the gap HEAD exactly: `match.strip() == "review:" + iid` or `match.strip().startswith("review:" + iid + " — ")`
(the verdict separator, `window_record.py:1868`; the real P-a data has that form). This is case-exact, and
`names_whole` is not used for this rule. Add battery rows: instance `A` vs word for `A b`; `Review:A`.

### B7 (fix-in-round; K4/K6) — S9 item 6: the `*` refusal row depends on a completion field the card does not name

`controller.py:7523-7524` refuses `unresolved window` only when the completion lacks `unresolved` or `reason`. If the
test's `p` carries them, the `*` row is accepted for a reason that has nothing to do with the word, and the row has no
killing power. **Edit:** item 6 names `p` = a completion with no `unresolved`/`reason` for both rows. E10 adds: "a
completion carrying `unresolved`+`reason` already passes a review gap today (the debt row's 'unresolved acceptance'
door); S9 changes nothing there and records a person pass only when the word is read".

### B8 (fork returned; K3/K9) — F9-1 against the person's recorded words

P-a's real decision text says: "… They stay unverified in the report." (`local-1-arm-b/pipeline.json:618`). In factory
words that is `unverified` → `review_unverified` → `after_checks` ("Left with you"), which is the P-h precedent that
already exists for probe gaps (`window_record.py:344-351`, `ledger.py:1213-1217`). Reading (i) delivers `no`, owner
`review`. That contradicts what the person was promised (FR-8, AR-24). It also makes "a person's word on a window gap"
end in two different delivery effects depending on the gap kind (P31 / axis 34: probe gap → after_checks, review gap
→ no). **Recommendation:** the Lead takes F9-1 to the owner with P-a quoted. The card stays executable on (i) until she
answers, because (i) is the stricter and reversible choice. (ii) is a follow-up node (ledger state + kinds row).

### B9 (fix-in-round; K6, expected value) — C3-d S-b

The INFO text is `"expectation changes " + (change_word("not_measured", why=why) or "not measured: " + why)`
(`window_record.py:1834-1836`). The expected value comes from the `change_word` data row, not from the literal
"expectation changes not measured: <why>". **Edit:** "expected = the `not_measured` row of the change-word data, with
`why` substituted".

### B10 (note) — C3-0, other keys

K1 spot-checks hold: `CONSUMER_RE` :138, `load_registry` :427-447 (reason, never an empty registry), `_token_problem`
:467, `_check_registry` :684, library sites :65-67, `ANCHOR_FLOOR` :119, the keep row `test_gate_registry.py` layer
`gate_named` (`test-layers.json:2032-2033`; the card says :2028-2030, drifted by about 3). K3: the error direction (False,
never raises) is right for a gate role (PROJECT.md п. 6 (в)). K9 F-T1 (a): agreed, one call per decision. F-T2 (a):
agreed, and C3-k carries the convergence with `acceptable_provenance` (named, owned).

### B11 (fix-in-round; K1/AR-29) — FL4: the census "two new rows" are one new row and one reclassification

`no_move.check_args` already has a census row: `judgment-census.json:705`, class `shape`, owner data. Adding the
membership rule makes it `xref`. That is a class change of an existing row. A raise in `xref` and a fall in `shape` must
be named (AR-20, q9/q11). **Edit:** item 8 says "one new row (`build_rework_request` membership, xref) + the
`check_args` row reclassified `shape → xref`, named in the verdict". The builder reads whether `build_rework_request`
already has a row.

### B12 (fix-in-round; K4/FR-41) — FL4: "does not hold" is said on a partial read

§3b.4 `no_move_facts` returns a LIST when one input is unreadable and the other gave candidates. §3b.5 `check_args` then
refuses a ref outside it with "the story does not hold". That claims a fact that was not established (FR-41/FR-59
text). The controller's twin (rule 2c) names the unreadable input. **Edit:** `no_move_facts` also carries
`candidates_unreadable` (names). `check_args` appends "; <names> could not be read, so a candidate there is not known",
the same text as 2c (one text builder, AR-13). Add a row to item 4.
Other FL4 keys: K1 spot-checks hold. Refusal at `controller.py:3779-3788` ✓, `BINDING_KEYS` :310 ✓, `ARGS_KEYS` :191 ✓,
"names no case" :251 ✓, `_grounding_candidates` :2371 ✓, `bug_candidate_record` :2363 ✓, `ANSWER_REWORK_OWNERS` :9387 ✓,
`--cases` :9904 ✓, `build_rework_request` :3705 ✓, `seam_rework_step` :608 / call :639 ✓. **PL4-1 measured:**
`_grounding_candidates(cart-1)` → `['R-13'] []`. **PL4-2 by reading:** `_rerun_stamp` (:4068-4097) with `wanted=[]`
stamps the completed stages after S7 and the approved later decisions; `reviews` is empty. E12 holds when S8 or gate B
was completed or approved. K7: function-disjoint from S9 on `controller.py`; the order S9 → FL4 is fine. F-L4-B (a),
F-L4-C (a), F-L4-D (a): I agree with all three recommendations, and the card is executable on each.

### B13 — FL2: what is missing before it is dispatchable

(1) The name of the `planning_contract.py` function that checks plan-row fields: candidates are `validate_plan` (census
:761, shape) or `gate_plan_errors` (:756). A new rule in an existing row is a class question, not a new row, so the
census bullet changes the same way as B11. (2) The strategist charter line (`agents/qa-test-strategist.md`, where
`disposition: skip` is described). (3) The rule-7 grep (§5 item 2). (4) PL-1 run. (5) The plan critic of §3, required
by п. 6 (б): a delivery word changes meaning (a skip row can read `no`). §3.2/§3.3 (one road through the existing state
word) are right under P31. E1–E6 are well formed. The `wave-a/integrate` order is already satisfied: merged as
`71d36190` (t-993).

### C3-b1 other keys (K1–K9)

K1 holds: `_NOVELTY_DEMANDS` :327, `novelty_of` :393 (absent → `(None, "")` :414), `_wanted` :447, `_handed` :460,
`proof_required` :467, `not_required_why` → `unmeasured` :501, `CRITIC_FIELDS` :1085, `validate_window` :1052,
`sensitivity:` :1218. K2: AR-22 is kept (writer manifest_put, readers proof_level/window in one commit). K4: E4's position
(after the review checks, before `sensitivity:`) is stated with its invariant. K9: F-T4 (a) agreed. F-T8 (a) agreed
(after S9).

### Answers to the t-989 findings (fix round t-994)

Checked: F-S1–F-S5, F-K7, F-0-1/2, F-a1/2, F-b1–5, F-c1/2, F-d1, F-e1/2, F-f1/2, F-i1/2, F-9-1–6, F-L2-1–3,
F-L4-1/2. All are answered as the table says. Two exceptions: my own F-S5 row for `_rehearse_reporter` was wrong (A1),
and the S9/FL4 `wave-a` order lines are stale (already merged).

### Standing questions, Part B

- Class completeness: walked axes 4, 5, 7, 25, 26, 32, 34. Uncovered axis 25 → B4. Uncovered axis 34 (delivery effect of
  a word by gap kind) → B8. Axis 32 class change → B11/B13.
- DUPLICATION: `check_args`/`build_rework_request` refusal texts for an unreadable input → one builder (B12). Otherwise
  none found. Grepped `_grounding_candidates|bug_candidates` (one body plus the planned wrapper).
- ONE ROAD (q12): B8 is the only finding. No language or project exclusion was found: I grepped the cards for
  pytest/python/language names, and the only hits are the factory's existing `is_pytest_command` reads.
- Tests (q5): no new test file in any card. B7 and B9 are killing-power and expected-value fixes.

## What I did NOT check

The C3-g/C3-h/C3-j/C3-k cards (not in scope). The S9 premise run (step 0: the builder's). PL-1, PL4-3, PL4-4. The rule-7
reader greps of §2.4/§3b.7. The slow test files (canon). Whether gate B counts as "after S7" in `_is_decision_after` (by
name only). The `.claude/` positive control.

## Trail

Read: `git show 5751426c` (whole diff); `docs/tasks/handoffs/t-1009-c3-r.md`; cards spec :1-100, :253-792,
:1040-1464; S9/FL spec whole; t-989 :78-177, :309-488; critic-diff-brief.md; `gate_registry.py` :20-70, :427-450,
:842-912 (+greps); `gate-registry.json` :1-6, :121-149, :249-312, :500-527 (+greps of accepts/sites);
`gate_preflight.py` :3577-3700, :3824-3975, :4214-4250; `environment_record.py` :160-210, :295-310; `stand_gaps.py`
:790-812; `environment_preparation.py` (greps); `delivery_verdict.py` :100-150; `acceptance.py` :1150-1176 (+greps);
`proof_level.py` :393-502, :1488-1522 (+greps); `execution_request.py` (greps); `manifest_from_tests.py` :835-945;
`window_record.py` :1242-1312, :1826-1840 (+greps); `controller.py` :2403-2440, :3776-3790, :4068-4097, :7440-7540
(+greps); `contract.py` :135-175; `local-1-arm-b/pipeline.json` :613-686; `judgment-census.json` (greps); tests: K-C4,
E9/E14, `uncheckable` count, `node_id_mismatch` pins, `test-layers.json` rows.
Runs (verbatim tails): `test_gate_registry.py` → `=== test_gate_registry: 439/439 ok ===`; `gate_registry.py --check`
→ `A26 gate registry: no violations` / `7 gate(s) left as debt:` / `6 gate(s) exempt:`; `gate_registry.py --sites |
grep _rehearse_reporter` → `gate_preflight.py:3650  _rehearse_reporter  countable['state'] == 'none'  [reporter_rehearsal_identity]`
(no `_reporter_outcome` line); PL4-1 → `['R-13'] []`; `git log origin/main --grep=wave-a` → `71d36190 wave: merge wave-a/integrate (t-993)`.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "A1: reporter_rehearsal_identity converted while its true accept site gate_preflight.py:3843 (_reporter_outcome, earlier['state'] == 'same_command') is unregistered; the D13 +1 at :3650 is a coincident helper-state 'none'",
    "B1: every converting card (C3-b1, C3-b2, C3-d, C3-g, C3-h, C3-j, C3-k) must own the test_gate_registry.py pins of its row, in a stated order on that file",
    "B3: C3-d re-roles acceptance.validate_window to validate although it accepts the critic's review word (acceptance.py:1171, :1161)",
    "B4: C3-b2 misses test_identity reuse sites proof_level._product_receipt_repeat (:1379) and _run_freshness (:939)"
  ],
  "fixes": [
    "A1: register _reporter_outcome (rec: accept, row back to debt B-283, C3-0 consumer; alt: validate with a Lead E-c judgment); register _record_unreadable as produce; re-measure D13 and name it",
    "A2: C3-k card line: remove or move provenance.environment_preparation (dead consumer, no matched word)",
    "A5: delete the NODE_ID_BLOCK constant pin at test_node_ids.py:899",
    "B1: owns + order on test_gate_registry.py; F4 flip control on an in-memory target row (in C3-0)",
    "B2: correct C3-0 E6 (two unread consumer ids exist)",
    "B5: correct F-T5's consequence with manifest_from_tests.py:835-840 and :922-925 before the fork is answered",
    "B6: S9 review rule matches the gap head exactly (review:<iid> or review:<iid> plus the em-dash separator), case-exact; battery rows for a space-prefix instance",
    "B7: S9 item 6 names a completion with no unresolved/reason; E10 states today's unresolved-acceptance door",
    "B8: F9-1 to the owner with the P-a decision text quoted; card runs on (i) until then",
    "B9: C3-d S-b expected value from the change_word not_measured row",
    "B11: FL4 census: check_args row reclassified shape to xref, named",
    "B12: FL4 no_move_facts carries unreadable names; check_args refusal says not known, one text builder with rule 2c",
    "B13: FL2 needs the planning_contract function, the charter line, rule-7 grep, PL-1 run and its plan critic"
  ],
  "class_completeness": "Class 'converted row word compared in an unregistered function' swept over the seven C3-R rows: reporter_rehearsal_identity _reporter_outcome/_record_unreadable (A1), collected_ids red_sandbox.py:2292 and execution_request.py:3187 (queue), environment_preparation execute_environment :444/:616 (produce, note), environment_property_cover stand_gaps._c4 (truthiness, note); same class found in plan cards: C3-b2 _product_receipt_repeat/_run_freshness (B4, axis 25), C3-d validate_window (B3). SIBLING_MAP axes walked for Part B: 4, 5, 7, 25, 26, 32, 34; axis 34 delivery effect by gap kind -> B8; axis 32 class change -> B11/B13.",
  "trail": {
    "read": [
      "git show 5751426c",
      "docs/tasks/handoffs/t-1009-c3-r.md",
      "docs/tasks/specs/20261117-rules-debt-phase2-cards-spec.md",
      "docs/tasks/specs/20261117-rules-debt-phase2-s9-fl-cards-spec.md",
      "docs/tasks/specs/reviews/t-989-rules-debt-phase2-wave2-plan.md",
      "docs/tasks/critic-diff-brief.md",
      "ai-packages/qa-factory/scripts/gate_registry.py",
      "ai-packages/qa-factory/references/gate-registry.json",
      "ai-packages/qa-factory/scripts/gate_preflight.py",
      "ai-packages/qa-factory/scripts/environment_record.py",
      "ai-packages/qa-factory/scripts/stand_gaps.py",
      "ai-packages/qa-factory/scripts/environment_preparation.py",
      "ai-packages/qa-factory/scripts/delivery_verdict.py",
      "ai-packages/qa-factory/scripts/acceptance.py",
      "ai-packages/qa-factory/scripts/proof_level.py",
      "ai-packages/qa-factory/scripts/manifest_from_tests.py",
      "ai-packages/qa-factory/scripts/window_record.py",
      "ai-packages/qa-factory/scripts/controller.py",
      "ai-packages/qa-factory/scripts/contract.py",
      "ai-packages/qa-factory/scripts/tests/fixtures/stories/local-1-arm-b/pipeline.json",
      "ai-packages/qa-factory/scripts/tests/fixtures/judgment-census.json"
    ],
    "reruns": [
      {"command": "python -B ai-packages/qa-factory/scripts/tests/test_gate_registry.py", "result": "=== test_gate_registry: 439/439 ok ==="},
      {"command": "python -B ai-packages/qa-factory/scripts/gate_registry.py --check", "result": "A26 gate registry: no violations; 7 gate(s) left as debt; 6 gate(s) exempt"},
      {"command": "python -B ai-packages/qa-factory/scripts/gate_registry.py --sites (grep _rehearse_reporter|_reporter_outcome)", "result": "gate_preflight.py:3650 _rehearse_reporter countable['state'] == 'none' [reporter_rehearsal_identity]; no _reporter_outcome line"},
      {"command": "python -B -c check_delivery._grounding_candidates(cart-1)", "result": "['R-13'] []"}
    ]
  }
}
```
