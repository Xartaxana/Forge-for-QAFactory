---
id: TC-005
title: An add never touches another owner's cart
area: cart
priority: P0
status: Draft
channel: auto
reuse_decision: new
updated: 2026-11-12
task: LOCAL-1
covers: [R-12]
defect_class: permission
basis: external:owner-isolation norm (no access beyond the owner)
then_oracles: [{"then": 1, "source": "unknown", "ref": "raise"}, {"then": 2, "source": "unknown", "ref": "raise"}, {"then": 3, "source": "unknown", "ref": "raise"}]
raise_questions: [{"then": 1, "question": "Must two guests and a guest and a user have fully separate carts after an add?", "source_says": [{"quote": "An add never touches another owner's cart (R-12, derived from the no-access-beyond-owner norm)", "where": "work/requirements-register.md:25"}], "severity": "major", "owner_role": "po_ba", "before": {"value": "unknown", "where": "no base reading"}, "now": {"value": "cart rows selected by owner (user id or session id)", "where": "../MyBooks/src/lib/cartOwner.ts:7"}}, {"then": 2, "question": "Must an add by one owner leave other owners' carts unchanged?", "source_says": [{"quote": "An add never touches another owner's cart", "where": "work/requirements-register.md:25"}], "severity": "major", "owner_role": "po_ba", "before": {"value": "unknown", "where": "no base reading"}, "now": {"value": "carts selected by owner", "where": "../MyBooks/src/lib/cartOwner.ts:7"}}, {"then": 3, "question": "Must a signed-in user's cart hold only the user's own adds?", "source_says": [{"quote": "a guest and a user, or two guests, stay apart", "where": "work/requirements-register.md:25"}], "severity": "major", "owner_role": "po_ba", "before": {"value": "unknown", "where": "no base reading"}, "now": {"value": "cart by user id", "where": "../MyBooks/src/lib/cartOwner.ts:7"}}]
preconditions: [{"id": "PC-1", "kind": "account", "what": "a user account that can sign in", "check": {"stand_account": "user"}}]
question_thens: [{"question": "raise", "then": 1, "readings": {"now": "each owner's cart read-back holds only its own books", "before": "unknown"}, "not_needed": ""}, {"question": "raise", "then": 2, "readings": {"now": "other owners' carts are unchanged after an add", "before": "unknown"}, "not_needed": ""}, {"question": "raise", "then": 3, "readings": {"now": "the user's cart holds only the user's own add", "before": "unknown"}, "not_needed": ""}]
---

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
