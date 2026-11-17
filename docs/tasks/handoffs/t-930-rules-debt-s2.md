# t-930 rules-debt S2 (R7)

DoD: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/tests/test_stand_lease.py` and `python -B ai-packages/qa-factory/scripts/tests/test_stand_lease.py`

## Output
```
(scenario_walk --witness-for, tail)
no scenario or keep row covers scripts/tests/test_stand_lease.py: run the whole scenario layer
scripts/tests/test_stand_lease.py: test_scenario_cart_1.py
scripts/tests/test_stand_lease.py: test_scenario_local_1_0108.py
scripts/tests/test_stand_lease.py: test_scenario_local_1_arm_b.py
scripts/tests/test_stand_lease.py: test_scenario_walk.py
scripts/tests/test_stand_lease.py: test_scenario_world.py
(test_stand_lease.py, tail)
PASS and the next run enters
PASS the person's reason is kept
PASS t-2070 F6: the release note carries no `pid` key (held_pid), so no reader takes it for a holder
PASS --status prints JSON
PASS --selftest passes
PASS nothing was written into the package

=== test_stand_lease: 50/50 ok ===
```
The walk names five scenario files as neighbours; I did not run them (the scenario layer is canon-judged, builder-rules 7b).

## What changed
test_stand_lease.py:319-324: the `waited_s == 15` check became one `check(...)`: `15 <= waited_s <= 1800 and waited_s % 5 == 0`, with an FR-31 comment. The `queued_behind` and `took_over` checks are untouched. E1: the upper bound is wait_s=1800, so a wait past the limit stays red. E2: the took_over check is unchanged. E3: no wall time asserted.
Sibling :386 (`([5, 2], 7)`, now about :390): not applicable. The holder is a live child that is never killed, so no extra poll can occur (read, confirmed).

## FR walk
G (FR-31): a load-dependent equality replaced by a poll-count bound. A, B, C, D, E, F: not touched.

## Deviations / questions / beyond manifest
None. Beyond the manifest: none.
