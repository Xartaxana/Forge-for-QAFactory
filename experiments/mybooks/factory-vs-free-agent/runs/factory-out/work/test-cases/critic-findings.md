# Round 3 - S4-qa-case-critic-3, area cart (repair_verify, plan rows P-2, P-4, P-5, P-10)

Verdict: reject

Scope: TC-002, TC-004, TC-005, TC-010 at the pinned versions in state/story-case-links.json. All eight dimensions applied, 7b-7g included. 4 of 4 reviewed. Advice: work/advice-S4.json not read separately; no advice entered or rejected. Not looked at: the live stand (no stand walk), response shapes (no context-bundle fact read).

## Roll-call

| plan row | case | reviewed | verdict | note |
|---|---|---|---|---|
| P-2 | TC-002 | yes | approve_with_concerns | Stock-0 precondition is case_seeds reading stock; none found means could-not-check, not green. Seed defect (add accepted or line created) fails Then 1-2. Then 3 is wording only. 7e unverified: no response shape read for the "out-of-stock reason" field. |
| P-4 | TC-004 | yes | reject | Round-2 F-2 not repaired: Step 4 "guest quantity above the book's stock" has no setup. R-7 refuses a guest add above stock, so the branch is not shown reachable and Then 4 could not fail (dim 8). Then 2 is conditional on Q12, fine. |
| P-5 | TC-005 | yes | approve_with_concerns | oracle_unknown: R-12 is a norm and all Thens are raises. It reaches Gate A as the owner's question. Then 3 has an allowed add by the same account. Seed defect (add lands in another owner's cart) fails Then 1-2. |
| P-10 | TC-010 | yes | approve_with_concerns | Then 3 rests on Q18 (raise). evidence_policy ui is named, with before/after screenshots and actual steps. lower level: api - TC-004 and TC-005 cover merge and isolation; kept as the manual smoke walk (P19). |

## Merge candidates

| cases | verdict | reason |
|---|---|---|
| TC-004, TC-010 | keep | P19: manual walk vs API merge on R-9 |
| TC-005, TC-010 | keep | P19: manual walk vs API owner isolation on R-12 |
| TC-002, TC-004 | keep | P16: different requirements (R-2 vs R-9) |

## Branch homes

| BN | home | reason |
|---|---|---|
| BN-1 | excluded | TC-002 covers stock 0 by content but carries no `branches` key; the owner of the key is the designer |
| BN-2 | excluded | outside this round's scope (TC-001, not dispatched); no case in scope carries it |
| BN-3 | excluded | outside this round's scope (TC-001, not dispatched); no case in scope carries it |
| BN-4 | excluded | outside this round's scope (TC-001, not dispatched); no case in scope carries it |
| BN-5 | excluded | outside this round's scope (TC-006, not dispatched); no case in scope carries it |
| BN-6 | excluded | outside this round's scope (TC-003, not dispatched); no case in scope carries it |
| BN-7 | excluded | TC-004 covers the merge partitions by content but carries no `branches` key; P-above-stock and P-zero-stock are not reachable (F-1) |
| BN-8 | excluded | outside this round's scope (TC-007, not dispatched); no case in scope carries it |

## Findings

- F-1 TC-004 (dim 8): quote "4. P-above-stock: guest quantity above the book's stock; sign in; read the cart." Expected: a setup step that produces a guest cart line above stock, or the partition dropped and recorded as a residual gap, as P-zero-stock was. Check: a step exists that creates that state.
- F-2 TC-002 (7e): unverified: no response shape for the out-of-stock reason field.

# Round 2 - S4-qa-case-critic-2, area cart

Verdict: approve_with_concerns

Scope: TC-001..TC-010 at the pinned versions of state/story-case-links.json (links[]). Dimensions applied: all eight, 7b-7g included. 10 of 10 reviewed. Round-1 rejects on TC-007 are repaired: the refused add is an API call (reachable), Then 3 names the working base. Concerns remain and go to the S5 automator.

## Roll-call

| plan row | case | reviewed | verdict | note |
|---|---|---|---|---|
| P-1 | TC-001 | yes | approve_with_concerns | 7e unverified: Then 2 subtotal field and Then 5 error-code field have no response shape read; the automator names them from the first real response. Partitions pass P16. |
| P-2 | TC-002 | yes | approve_with_concerns | Precondition is now case_seeds reading stock; if no stock-0 book exists the case is could-not-check, not green. Then 3 is wording-only (Q1/Q10), asserts nothing new. |
| P-3 | TC-003 | yes | approve_with_concerns | Then 3 names "a second guest's seeded line" but no step seeds a second guest: add the step or drop the clause. lower level: api - the cookie-jar persistence is API-reachable (the case notes it); keep the browser only for the cookie-cleared step and badge. |
| P-4 | TC-004 | yes | approve_with_concerns | P-above-stock: a guest cannot add above stock (R-7 refuses it), so the branch is not shown reachable (dim 8) and Then 4 could not fail; say how the guest cart gets qty above stock or drop the partition as P-zero-stock was. Then 2 rests on Q12 (higher wins) and is conditional, fine. |
| P-5 | TC-005 | yes | approve_with_concerns | oracle_unknown: R-12 is a norm and all Thens are raises; reaches Gate A as the owner's question. Allowed call by the same account is in Then 3; seed defect (add lands in another owner's cart) fails Then 1-2. |
| P-6 | TC-006 | yes | approve_with_concerns | lower level: impossible - the wishlist move-to-cart and card button are UI seams. Step 4 repeats "one path" while Then 2 says "each path": align them. |
| P-7 | TC-007 | yes | approve_with_concerns | Then 2 "the badge shows the number the requirement names (lines or units - Q-badge)" gives no expected value and the requirement names none (7b/oracle_unknown): the badge half cannot tell lines from units. Write it in the conditional form per the raise (lines = 2 under reading now). lower level: impossible - the header badge exists only in the UI. |
| P-8 | TC-008 | yes | approve_with_concerns | Then 4 expects an out-of-stock message from the UI, but Q1 says the button is disabled for stock 0: the step cannot show a message. State what is seen (disabled button) as the expected value. evidence_policy ui named. lower level: api - partitions are in TC-001/TC-002; this is the UI smoke walk. |
| P-9 | TC-009 | yes | approve_with_concerns | Then 3 "header count matches the cart content" has no measure (lines or units), same gap as TC-007 Then 2. evidence_policy ui named. lower level: impossible - the display format is UI-only. |
| P-10 | TC-010 | yes | approve_with_concerns | Then 3 depends on Q18, a raise. evidence_policy ui named. lower level: api - TC-004 and TC-005 cover merge and owner isolation; kept as the manual smoke walk (P19). |

## Merge candidates

| cases | verdict | reason |
|---|---|---|
| TC-001, TC-008 | keep | P19: TC-008 is a manual UI smoke walk, TC-001 the API partitions |
| TC-003, TC-010 | keep | P19: manual walk vs automated check on R-5 |
| TC-004, TC-010 | keep | P19: manual walk vs API merge on R-9 |
| TC-005, TC-010 | keep | P19: manual walk vs API owner isolation on R-12 |
| TC-006, TC-008 | keep | P19: manual walk vs automated UI paths on R-6 |
| TC-007, TC-009 | keep | P19: R-13 automated badge check vs manual format walk |
| TC-001, TC-009 | keep | P19: R-4 at the API vs the displayed dollar format, UI-only |
| TC-002, TC-008 | keep | P19: R-2 at the API vs the manual UI walk |

## Branch homes

| BN | home | reason |
|---|---|---|
| BN-1 | TC-002 | stock 0 refusal |
| BN-2 | TC-001 | stock cap, P-stockcap |
| BN-3 | TC-001 | quantity 3 partition, P-qty3 |
| BN-4 | TC-001 | P-invalid quantities and bookIds |
| BN-5 | TC-006 | three add paths |
| BN-8 | TC-007 | header count and refused add |
| BN-6 | TC-003 | guest cookie, cookie cleared |
| BN-7 | TC-004 | merge partitions |

## Findings

- F-1 TC-007 (7b, oracle_unknown): quote "the badge shows the number the requirement names (lines or units - Q-badge)". Expected: a Then in conditional form per the raise, e.g. "under reading now the badge equals the 2 lines; the units value 4 is the other reading". Check: the Then names a value for each reading.
- F-2 TC-004 (dim 8): quote "P-above-stock: guest quantity above the book's stock". Expected: show how the branch is reached or drop it. Check: a setup step that produces the state.
- F-3 TC-003 (dim 3): quote "a second guest's seeded line (a different book) never appears". Expected: a step that seeds the second guest. Check: step exists.
- F-4 TC-008 (7b): quote "The out-of-stock book shows an out-of-stock message". Expected: the disabled button per Q1. Check: Then matches the answer.
- F-5 TC-001 (7e): unverified: no response shape read for subtotal and error-code fields.


Verdict: reject

Scope: TC-001..TC-010 (pinned versions in state/story-case-links.json). Dimensions applied: all eight, 7b-7g included. 10 of 10 reviewed.

## Roll-call

| plan row | case | reviewed | verdict | note |
|---|---|---|---|---|
| P-1 | TC-001 | yes | approve_with_concerns | 7e unverified: Then 5 "stable error code" and Then 2 "subtotal" name no response field and no response shape was read. Name the fields (error code, line subtotal) or mark them unverified. Parametrised partitions pass P16. |
| P-2 | TC-002 | yes | approve_with_concerns | Dim 3: precondition `{"none": ...}` for a stock-0 book where a GET of the catalog would do; use an http check or case_seeds that reads stock. Also the plan row is `unverifiable` until Q1 but the case is `channel: auto`. |
| P-3 | TC-003 | yes | approve_with_concerns | Then 3 passes for "empty or only its own" so it cannot fail on most defects; state a single expected value. lower level: api - a session cookie jar sees persistence without a browser, the plan gives no reason for e2e-ui. |
| P-4 | TC-004 | yes | approve_with_concerns | Step 3 P-zero-stock "has gone to stock 0 or is capped" cannot be set up by the case without changing the stand's stock; name how the branch is reached or drop the partition. |
| P-5 | TC-005 | yes | approve_with_concerns | oracle_unknown (R-12 is a norm, all Thens are raise); it reaches Gate A as the owner's question. Allowed call by the same account is present in Then 3. Seed defect (add lands in the wrong owner's cart) fails Then 2. |
| P-6 | TC-006 | yes | approve_with_concerns | lower level: impossible - the wishlist move-to-cart seam is in the UI. Then 3 repeats Then 1 and 2 of the same R-6; fold it in. |
| P-7 | TC-007 | yes | reject | Step 3 refused add on a stock-0 book through the UI: TC-002 residual says "the click path is disabled in UI", so the branch is not shown reachable (dim 8); Then 3 "unchanged" states no working base (7c); Then 2 "matches ... (same measure)" gives no expected value (lines or units). lower level: impossible - the header badge exists only in the UI. |
| P-8 | TC-008 | yes | approve_with_concerns | Manual evidence: no `evidence_policy` word; "screenshots per manual-evidence rules" does not name before/after and actual steps. lower level: api - the partitions are in TC-001, this walk is the smoke at e2e. |
| P-9 | TC-009 | yes | approve_with_concerns | Same evidence_policy gap (ui: before and after images plus actual steps). lower level: impossible - the display format is UI-only. |
| P-10 | TC-010 | yes | approve_with_concerns | Same evidence_policy gap. Then 3 depends on Q2/Q3 raises; steps overlap TC-003/004/005 at a higher level. lower level: api - TC-004 and TC-005 already cover merge and owner isolation. |

## Merge candidates

| cases | verdict | reason |
|---|---|---|
| TC-001, TC-008 | keep | P19: TC-008 is a manual smoke walk at the UI, TC-001 the API partitions |
| TC-003, TC-010 | keep | P19: manual walk vs automated e2e on R-5 |
| TC-004, TC-010 | keep | P19: manual walk vs API merge on R-9 |
| TC-005, TC-010 | keep | P19: manual walk vs API owner isolation on R-12 |
| TC-006, TC-008 | keep | P19: manual walk vs automated UI paths on R-6 |
| TC-007, TC-009 | keep | P19: R-13 automated badge check vs manual format walk |
| TC-001, TC-009 | keep | P19: R-4 at the API (TC-001) vs the displayed dollar format, UI-only (TC-009) |
| TC-002, TC-008 | keep | P19: R-2 at the API (TC-002; the UI click is disabled) vs the manual UI walk (TC-008) |

## Branch homes

| BN | home | reason |
|---|---|---|
| BN-1 | TC-002 | stock 0 refusal |
| BN-2 | TC-001 | stock cap, P-stockcap |
| BN-3 | TC-001 | quantity 3 partition, P-qty3 |
| BN-4 | TC-001 | P-invalid quantities and bookIds |
| BN-5 | TC-006 | three add paths |
| BN-8 | TC-007 | header count and refused add |
| BN-6 | TC-003 | guest cookie, cookie cleared |
| BN-7 | TC-004 | merge partitions |

## Findings

- F-1 TC-007 (dim 8, 7c): quote "Attempt a refused add (stock-0 book); read the badge and the cart page." Expected: prove the refusal is reachable in the UI (a path that is not disabled) or make the refused add an API call; Then 3 states the working base (an allowed add by the same session afterwards raises badge and cart page together).
- F-2 TC-007 (dim 3): Then 2 "the badge value matches the cart page content (same measure)". Expected: name the measure the badge shows (lines or units) with a source or raise it as a question; with adds of qty 1 and 3 the case can tell lines (2) from units (4).
- F-3 TC-001 (7e): name the response fields read by Thens 2 and 5, or mark them unverified.
