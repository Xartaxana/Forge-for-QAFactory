---
id: TC-007
title: Header count and cart page agree after an add and after a refused add
area: cart
priority: P2
status: Draft
channel: auto
reuse_decision: new
updated: 2026-11-12
task: LOCAL-1
covers: [R-13]
defect_class: state
basis: requirement:R-13
then_oracles: [{"then": 1, "source": "requirement", "ref": "R-13"}, {"then": 2, "source": "requirement", "ref": "R-13"}, {"then": 3, "source": "requirement", "ref": "R-13"}]
preconditions: [{"id": "PC-1", "kind": "service", "what": "the stand UI is reachable", "check": {"stand_frontend": "the header badge is UI-only"}}]
---

Requirements: R-13
Plan row: P-7

## Obligation coverage

| Obligation | Oracle | Boundary | Then / evidence | Residual gap |
|---|---|---|---|---|
| OB-7 | R-13 | count 0 (badge hidden), 1, many; refused add | Thens 1-3, header badge vs cart page lines | Whether count means lines or units is not stated: both are read and compared to the cart page |

## Steps

1. Empty cart: read the header badge.
2. Add one book (quantity 1), then another book (quantity 3) without reloading; read the badge and the cart page after each.
3. Attempt a refused add (stock-0 book); read the badge and the cart page.

## Then

1. At an empty cart the badge is hidden.
2. After each add the badge value matches the cart page content (same measure), without a reload.
3. After the refused add the badge and the cart page are unchanged.
