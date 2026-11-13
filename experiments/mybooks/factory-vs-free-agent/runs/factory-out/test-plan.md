---
task: LOCAL-1
created: 2026-11-12
rows_total: 10
candidates: 10
planned: 10
---

Pyramid: api 2 automate, e2e-ui 2 automate, 3 manual-agent walks, 3 unverifiable until Q1, Q2, Q3 are answered (TS-n here is P-n in work/test-plan.json). Budget cap 28; 10 rows planned, within the cap.

## Plan

| TS | what we verify | R | defect hypothesis | impact class | priority | observable | oracle | disposition + reason | fit | level | technique |
|---|---|---|---|---|---|---|---|---|---|---|---|
| TS-1 | Add API partitions: price, qty 1/3, repeat add, stock cap, invalid input, failed add leaves cart unchanged | R-1, R-3, R-4, R-7, R-8, R-10, R-11 | boundary @ cartService add | money | P0 | expected-contract:work/requirements-register.md:15 | requirement:R-3 | `automate` — regression: yes | new | api | Boundary value analysis |
| TS-2 | Out-of-stock book refused, no item (wording open, Q1) | R-2 | contract @ out-of-stock message | degraded | P2 | expected-contract:work/requirements-register.md:14 | requirement:R-2 | `unverifiable` — waits for Q1; on a: exact text | new | api | Error guessing |
| TS-3 | Guest cart persists between visits (Q2: cookie or local storage) | R-5 | state @ guest persistence | data-loss | P0 | expected-contract:work/requirements-register.md:17 | requirement:R-5 | `unverifiable` — waits for Q2; on a: cookie | new | e2e-ui | State transition testing |
| TS-4 | Sign-in merges guest cart, no item lost (Q3: higher wins or sum) | R-9 | data-loss @ cart merge | data-loss | P0 | expected-contract:work/requirements-register.md:22 | requirement:R-9 | `unverifiable` — waits for Q3; on a: higher wins | new | api | Decision table testing |
| TS-5 | Add never touches another owner's cart | R-12 | permission @ cart owner selection | access | P0 | expected-contract:work/requirements-register.md:25 | | `automate` — regression: yes, P0 | new | api | Risk-based testing |
| TS-6 | Product page, card and wishlist give the same cart line | R-6 | seam @ wishlist move-to-cart | blocked-flow | P1 | expected-contract:work/requirements-register.md:18 | requirement:R-6 | `automate` — regression: yes; e2e: three UI paths | new | e2e-ui | Equivalence partitioning |
| TS-7 | Header count and cart page agree after add and after refused add | R-13 | state @ Navigation badge | degraded | P2 | expected-contract:work/requirements-register.md:19 | requirement:R-13 | `automate` — regression: yes; e2e: badge is UI-only | new | e2e-ui | State transition testing |
| TS-8 | Walk: add three ways, repeat, out of stock, bad quantity | R-1, R-2, R-3, R-6, R-7, R-8, R-10, R-11 | smoke | blocked-flow | P1 | current-code:../MyBooks/src/components/pages/BookDetailPage.tsx | requirement:R-1 | `manual-agent` — regression: no | | e2e-ui | Exploratory charters |
| TS-9 | Walk: price, subtotal, count in dollars with two decimals | R-4, R-13 | smoke | money | P0 | current-code:../MyBooks/src/components/Navigation.tsx:58 | requirement:R-4 | `manual-agent` — regression: no | | e2e-ui | Exploratory charters |
| TS-10 | Walk: guest leaves and returns, signs in, second guest | R-5, R-9, R-12 | smoke | data-loss | P0 | current-code:../MyBooks/src/lib/session.ts:34 | requirement:R-5 | `manual-agent` — regression: no | | e2e-ui | Exploratory charters |

## Recommended regression

No regression: the only existing tests, src/lib/cartRules.test.ts (MB-cartRules-merge, MB-cartRules-fits), are in the read-only application repository and belong to its own suite. This suite has no cart spec; TS-4 extends the merge idea at the API.

## Open items

- Q1 wording, Q2 cookie or local storage, Q3 merge rule: planned on reading a until answered.
- Q6 subtotal rounding is not stated: TS-1 and TS-9 record the gap.
- The index could not read the application files (not canonical repository paths): observables are unmeasured; flow requests are not measured.
- The stand login is refused by POST /login (405): walks sign in through the UI form.
- R-12 is derived from a norm and has no independent oracle: its row leaves `oracle` empty and the Thens carry the owner-isolation norm.
- Depth: TS-1 is the deep row for R-3, R-4, R-7, R-8, R-10 and R-11; the pairs of quantity and stock partitions are left to boundary values.

<!-- qa-factory:case-appendix:start -->
## Case appendix

| Case | Plan row | Oracle/basis | Channel | Review status | Version |
|---|---|---|---|---|---|
| TC-001 | unlinked | requirement:R-3 | auto | Draft | cv_c8a64053d0336ad2fde7 |
| TC-002 | unlinked | requirement:R-2 | auto | Draft | cv_db6a24c95f4961d4b654 |
| TC-003 | unlinked | requirement:R-5 | auto | Draft | cv_1ef35b09452b352c2e12 |
| TC-004 | unlinked | requirement:R-9 | auto | Draft | cv_a3b811c9760500751b01 |
| TC-005 | unlinked | external:owner-isolation norm (no access beyond the owner) | auto | Draft | cv_0eec4cd0b2868fdb85f3 |
| TC-006 | unlinked | requirement:R-6 | auto | Draft | cv_70980e1a0ee70392ab80 |
| TC-007 | unlinked | requirement:R-13 | auto | Draft | cv_4796484d0ac8055c472d |
| TC-008 | unlinked | requirement:R-1 | manual-agent | Draft | cv_172cc51a3871c5758930 |
| TC-009 | unlinked | requirement:R-4 | manual-agent | Draft | cv_377adcf176fef6b8abde |
| TC-010 | unlinked | requirement:R-5 | manual-agent | Draft | cv_5a84597a1f23316f6527 |

Cases: 10. Generated from pinned case content; do not edit this section by hand.

### TC-001 — cv_c8a64053d0336ad2fde7

Requirements: R-1, R-3, R-4, R-7, R-8, R-10, R-11
Plan row: P-1

## Obligation coverage

| Obligation | Oracle | Boundary | Then / evidence | Residual gap |
|---|---|---|---|---|
| OB-1 | R-3, R-1, R-4, R-7, R-8, R-10, R-11 | qty 0, 1, 999, 1000, -1, 1.5, "abc"; stock-1, stock, stock+1; bookId missing, 0, unknown | Thens 1-6, cart read back through a separate GET of the cart | Subtotal rounding to cents not stated (Q6): recorded, not asserted beyond whole-cent prices |

## Steps

1. Read the book's current price and stock from the catalog API (own seed, uniquely marked guest session).
2. P-qty1: add the book with quantity 1; read the cart back with a separate GET.
3. P-qty3: in a fresh session add quantity 3; read the cart back.
4. P-repeat: add the same book twice; read the cart back.
5. P-stockcap: add up to stock, then add 1 more; add stock+1 in a fresh session; read the cart back after each.
6. P-invalid: add with quantity 0, 1000, -1, 1.5, "abc", and with bookId missing, 0 and unknown; read the cart back after each.

## Then

1. P-qty1: the cart read-back has one line for the book with the catalog's current price and quantity 1.
2. P-qty3: the read-back line has quantity 3 and subtotal = price x 3 (price in whole cents); the subtotal field name of the cart line is unverified (no response shape read) - the automator names it from the first real cart response.
3. P-repeat: the read-back has exactly one line for the book with the summed quantity, no duplicate line.
4. P-stockcap: the line quantity never exceeds stock, also after the second add; the add beyond stock is refused.
5. P-invalid: quantities 0, 1000, -1, 1.5, "abc" and the bad bookIds are each refused (not a 2xx with a true success flag), with the same error code for the same class of input; the error-code field name is unverified (no response shape read) - the automator names it from the first real refusal.
6. P-invalid: after every refused add the cart read-back is identical to its state before the call; an allowed add by the SAME session afterwards succeeds.

### TC-002 — cv_db6a24c95f4961d4b654

Requirements: R-2
Plan row: P-2

## Obligation coverage

| Obligation | Oracle | Boundary | Then / evidence | Residual gap |
|---|---|---|---|---|
| OB-2 | R-2 | stock 0 (and stock 1 as the neighbour that is accepted) | Thens 1-3, cart read back separately | Wording open (Q1); the click path is disabled in UI, so API only |

## Steps

1. Pick a book with stock 0; read the cart (empty, own marked session).
2. Add it via the API with quantity 1.
3. Read the cart back with a separate GET.

## Then

1. The add is refused (not a 2xx with a true success flag) and the response names an out-of-stock reason.
2. The cart read-back holds no line for the book and the cart equals its state before the call.
3. Per Q1/Q10 a stock-0 book shows a disabled "Out of Stock" button in the UI (correct, not a defect); the API refusal of Then 1 is still asserted, and its exact wording is an open question for the product owner (only the out-of-stock reason is asserted).

### TC-003 — cv_1ef35b09452b352c2e12

Requirements: R-5
Plan row: P-3

## Obligation coverage

| Obligation | Oracle | Boundary | Then / evidence | Residual gap |
|---|---|---|---|---|
| OB-3 | R-5 | cookie present, cookie cleared | Thens 1-3, cart page and header count after a new visit | Cookie vs local storage open (Q2) |

Level note: persistence is reachable at the API with a session cookie jar (add, new jar object with the same cookie, GET cart); the browser path is kept for the cookie-clearing step and the header badge, which the API cannot show.

## Steps

1. As a guest in a fresh browser context add a book (quantity 2); note the cart page lines.
2. Close the page, open a new page in the SAME browser context, open the cart.
3. P-cleared: clear the cart cookie, reload, open the cart.

## Then

1. The cart page after the new visit lists the same book and quantity 2.
2. Conditional on Q2: under reading a the cart survives with the cookie and local storage need not hold it; under reading b the cart also survives with the cookie removed.
3. P-cleared: with the cookie cleared the cart page is empty (zero lines) and the header badge is hidden; a second guest's seeded line (a different book) never appears.

### TC-004 — cv_a3b811c9760500751b01

Requirements: R-9
Plan row: P-4

## Obligation coverage

| Obligation | Oracle | Boundary | Then / evidence | Residual gap |
|---|---|---|---|---|
| OB-4 | R-9 | book only in guest cart, in both carts, zero stock, guest qty above stock | Thens 1-4, user cart read back after sign-in | Merge rule open (Q3); existing MB-cartRules-merge belongs to the app repo |

## Steps

1. P-guest-only: as a guest add book A (2); sign in; read the user's cart.
2. P-both: user cart holds book B (3) before; as guest add B (2); sign in; read the cart.
3. P-zero-stock: not reachable without changing the stand's stock (a guest cannot add a stock-0 book, see TC-002); dropped from this case, recorded as a residual gap.
4. P-above-stock: guest quantity above the book's stock; sign in; read the cart.

## Then

1. P-guest-only: the user's cart read-back contains book A with quantity 2.
2. P-both: conditional on Q12 (the person answered "the higher quantity wins", AUTH.md; the register has not recorded it yet): the line for B has quantity 3, not the sum 5, and is neither missing nor duplicated.
3. P-zero-stock: dropped (not reachable on a stand whose stock cannot be changed); no assertion.
4. P-above-stock: no merged line exceeds its stock; the user's pre-existing lines are unchanged.

### TC-005 — cv_0eec4cd0b2868fdb85f3

Requirements: R-12
Plan row: P-5

## Obligation coverage

| Obligation | Oracle | Boundary | Then / evidence | Residual gap |
|---|---|---|---|---|
| OB-5 | R-12 (derived from the no-access-beyond-owner norm; no independent oracle) | guest vs user, guest vs guest | Thens 1-3, each owner's cart read back by its own session | Oracle is a norm, not a ticket statement |

## Steps

1. Guest G1 (own cookie) adds book A (1); guest G2 (separate cookie) adds book B (1).
2. Read G1's and G2's carts, each by its own session.
3. The signed-in user adds book C (1); read the guest carts again and the user's cart.

## Then

1. G1's cart holds only A and G2's cart holds only B (two guests stay apart).
2. After the user's add, the guests' carts are unchanged.
3. The user's cart holds C and none of the guests' books; an allowed add by the same user account succeeded, proving the account works.

### TC-006 — cv_70980e1a0ee70392ab80

Requirements: R-6
Plan row: P-6

## Obligation coverage

| Obligation | Oracle | Boundary | Then / evidence | Residual gap |
|---|---|---|---|---|
| OB-6 | R-6 | three entry paths; book absent from cart and already in it | Thens 1-2, cart page read after each path | Wishlist needs a signed-in account |

## Steps

1. P-detail: from the product page of book A click Add to Cart; open the cart page.
2. P-card: in a clean cart click the card button for A; open the cart page.
3. P-wishlist: put A on the wishlist, click Move to cart; open the cart page.
4. P-already: repeat one path with A already in the cart.

## Then

1. Each path (P-detail, P-card, P-wishlist) from an empty cart gives exactly one line for A with A's price and quantity 1, identical across the three paths.
2. P-already: each path gives the same single line with quantity 2, no duplicate line.

### TC-007 — cv_4796484d0ac8055c472d

Requirements: R-13
Plan row: P-7

## Obligation coverage

| Obligation | Oracle | Boundary | Then / evidence | Residual gap |
|---|---|---|---|---|
| OB-7 | R-13 | count 0 (badge hidden), 1, many; refused add | Thens 1-3, header badge vs cart page lines | Whether count means lines or units is not stated: both are read and compared to the cart page |

## Steps

1. Empty cart: read the header badge.
2. Add one book (quantity 1), then another book (quantity 3) without reloading; read the badge and the cart page after each.
3. Refused add as an API call (the UI click on a stock-0 book is disabled, see TC-002): with the same session cookie, POST the add of a stock-0 book chosen from the catalog API (stock read first); then reload the page and read the badge and the cart page.
4. Allowed add by the SAME session (an in-stock book, quantity 1); read the badge and the cart page again.

## Then

1. At an empty cart the badge is hidden.
2. After the two adds (quantity 1, then quantity 3, two lines) the cart page shows 2 lines and 4 units; the badge shows the number the requirement names (lines or units - Q-badge), updated without a reload.
3. After the refused add (answer is not a 2xx with a true success flag) the badge and the cart page equal their values before the call; after the allowed add of step 4 the badge and the cart page both rise together (working base: the session still adds).

### TC-008 — cv_172cc51a3871c5758930

Requirements: R-1, R-2, R-3, R-6, R-7, R-8, R-10, R-11
Plan row: P-8

## Obligation coverage

| Obligation | Oracle | Boundary | Then / evidence | Residual gap |
|---|---|---|---|---|
| OB-8 | R-1 | quantity 3, repeat, stock 0, quantity 0/1000 | Thens 1-5, evidence_policy ui: a before and an after screenshot for each step plus the actual steps taken, per references/manual-evidence.md | Not regression; deep partitions are in TC-001 |

## Steps

1. Add an in-stock book from the product page (quantity 1), card and wishlist; open the cart.
2. Add the same book again; note the line.
3. Try the out-of-stock book.
4. On the product page type quantity 0, then 1000, then 3.

## Then

1. The product-page add shows the book with its price and quantity 1 in the cart.
2. The card and wishlist adds give the same line as the product page.
3. The repeat add keeps one line with increased quantity.
4. The out-of-stock book shows an out-of-stock message and no item appears.
5. Quantity 0 and 1000 are refused and the cart is unchanged; quantity 3 gives a line with quantity 3.

### TC-009 — cv_377adcf176fef6b8abde

Requirements: R-4, R-13
Plan row: P-9

## Obligation coverage

| Obligation | Oracle | Boundary | Then / evidence | Residual gap |
|---|---|---|---|---|
| OB-9 | R-4 | whole-dollar price, price with cents, quantity 3 | Thens 1-3, evidence_policy ui: a before and an after screenshot per step plus the actual steps taken, per references/manual-evidence.md | Subtotal rounding (Q6) recorded as a gap |

## Steps

1. Note the catalog price of a book with whole-dollar price and one with cents.
2. Add each (quantity 1, then 3) and read price, subtotal and header count.

## Then

1. The cart price equals the catalog's current price, shown in dollars with two decimals (e.g. $12.00, not $12).
2. The subtotal equals price x quantity with two decimals.
3. The header count matches the cart content.

### TC-010 — cv_5a84597a1f23316f6527

Requirements: R-5, R-9, R-12
Plan row: P-10

## Obligation coverage

| Obligation | Oracle | Boundary | Then / evidence | Residual gap |
|---|---|---|---|---|
| OB-10 | R-5, R-9, R-12 | guest returns; sign-in merge; second guest | Thens 1-3, evidence_policy ui: a before and an after screenshot per step plus the actual steps taken, per references/manual-evidence.md | Merge rule and persistence mechanism open (Q3, Q2); the walk records what is seen |

## Steps

1. As a guest add a book, close the browser tab, reopen the site, open the cart.
2. Sign in through the UI form; open the cart.
3. In a second, private browser context as another guest open the cart.

## Then

1. After returning, the guest cart still holds the book.
2. After sign-in the user's cart holds the guest's book, nothing lost.
3. The second guest sees an empty cart, not the first guest's or the user's lines.
<!-- qa-factory:case-appendix:end -->
