# LOCAL-1 — understanding

## Why this change
No code changes: we check "Add to Cart" in MyBooks as it behaves now, on every entry path. Requirements: story XPANBFLFA-44 and the code, not limited to them.

## Size
M (3 functions) · cap 28 · budget 31 · overage 3 · unverifiable 0

## What we verify

- R-1 — in-stock book from the product page lands in the cart, right price, quantity 1
- R-2 — out-of-stock book is refused with a message, nothing added (wording: Q1)
- R-3 — chosen quantity gives that quantity and the right subtotal (rounding: Q6)
- R-4 — cart price is the backend's current price, in dollars with two decimals
- R-5 — guest cart survives between visits (cookie; local storage: Q2)
- R-6 — product page, catalog card and wishlist move all add the same way
- R-13 — after an add, the header count and the cart page show the cart
- R-7 — cart quantity never exceeds stock, also on repeated adds
- R-8 — quantity must be a whole number in range; bad input changes nothing
- R-9 — guest cart merges into the user's cart at sign-in, nothing lost (rule: Q3)
- R-10 — same book added again: one line, larger quantity
- R-11 — a failed add shows as a failure, cart unchanged
- R-12 — an add never touches another owner's cart

## What we do not verify, and why

- Checkout, promo, shipping, tax: outside "Add to Cart". Tests XPANBFLFA-141..167: not read.

## What else the change may touch

- Cart page edit/remove (shares stock rules); sign-in merge; stock changed by admin or orders

## Questions without which testing is pointless

- Q1 — must the out-of-stock text be exactly "Out of stock" (code differs)?
- Q2 — is local storage required for the guest cart (code uses a cookie only)?
- Q3 — at merge, higher quantity wins or quantities add (code: higher wins)?
- Q4 — confirm the derived norms R-7, R-10, R-11, R-12; Q5 — is today's behaviour of R-8, R-10..R-12 intended?
- Q6 — how is the subtotal rounded to cents?
