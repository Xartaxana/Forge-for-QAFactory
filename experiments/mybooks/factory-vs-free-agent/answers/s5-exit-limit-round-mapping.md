round

The tests ran: the run block 20261112T194312786104Z-54369b0ebc7cd1fa9f76.json exists, only the ids did not bind. Do exactly the two things the check names, nothing else:
1. Every tests[] row of TC-006 gets `obligation_refs: [OB-6]` and every row of TC-007 gets `obligation_refs: [OB-7]` (the obligation ids of plan rows P-6 and P-7 in work/test-plan.json).
2. Run `run_suite.py --task LOCAL-1 --reparse-block 20261112T194312786104Z-54369b0ebc7cd1fa9f76.json --mapping <JSON>` with a mapping from each of the 7 instance ids to its test id in that run's JUnit report (read the report the block names; do not run the tests again unless the report lacks them).
