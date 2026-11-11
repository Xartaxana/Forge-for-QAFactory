- `s5_precheck.py`: the checks that judged test code (a sleep or an environment read in a test, a before/after comparison on an unasserted base, tests that differ only in data, a copy of
  an existing helper) now print an `ADVICE` block for the code critic and never refuse the author; the cross-reference checks (an unconfirmed expectation asserted as proved, a test changed after a red run)
  still block. The route word of an unresolved row is chosen by the role and checked against the closed list; the judge that translated free words into a route word is gone.
