---
id: TC-002
title: Out-of-stock book is refused with an out-of-stock message and no cart item
area: cart
priority: P2
status: Draft
channel: auto
reuse_decision: new
updated: 2026-11-12
task: LOCAL-1
covers: [R-2]
defect_class: contract
basis: requirement:R-2
then_oracles: [{"then": 1, "source": "requirement", "ref": "R-2"}, {"then": 2, "source": "requirement", "ref": "R-2"}, {"then": 3, "source": "unknown", "ref": "Q10"}]
preconditions: [{"id": "PC-1", "kind": "data", "what": "a book with stock 0", "check": {"none": "only a person can name a stock-0 book on the stand if none is seeded"}}]
question_thens: [{"question": "Q10", "then": 3, "readings": {"now": "the message names the book as out of stock", "before": "unknown"}, "not_needed": ""}]
---

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
3. Conditional on Q1: under reading a the message equals "Out of stock"; under reading b any message mentioning out of stock passes.
