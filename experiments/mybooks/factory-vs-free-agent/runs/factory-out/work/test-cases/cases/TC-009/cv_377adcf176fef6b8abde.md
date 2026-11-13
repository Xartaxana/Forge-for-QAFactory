---
id: TC-009
title: Walk - price, subtotal and count shown in dollars with two decimals
area: cart
priority: P0
status: Draft
channel: manual-agent
reuse_decision: new
updated: 2026-11-12
task: LOCAL-1
covers: [R-4, R-13]
defect_class: smoke
basis: requirement:R-4
then_oracles: [{"then": 1, "source": "requirement", "ref": "R-4"}, {"then": 2, "source": "requirement", "ref": "R-4"}, {"then": 3, "source": "requirement", "ref": "R-13"}]
preconditions: [{"id": "PC-1", "kind": "service", "what": "the stand UI is reachable", "check": {"stand_frontend": "the walk is done in the browser"}}]
---

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
