# t-117 A2 -- main-session WARN names the snapshot duty

Old (main and worker): `AGENT BUDGET WARN: the <who> context is N tokens (warn from W[, repeated every S]); every turn re-reads it. Trim output, stop re-running after each edit, commit and hand over before the cap.`

New, main session only: the same text + ` Write the compact snapshot (docs/tasks/compact-snapshots/) and tell the operator the one line (PROJECT.md).` Worker text byte-identical (duty is "" for a worker).

Test: `test_main_warn_at_300k_and_again_only_at_350k` gained `assert "docs/tasks/compact-snapshots/" in _ctx_of(first)`. (There is no separate main-WARN table; this is the existing main-WARN test.)

Edges: agent_budget is not registered in warn_layers.json / test_warn_messages.py (0 matches), so its 550-char budget does not apply; no shortening was needed. Thresholds and `evaluate` untouched.

DoD run: `python -m pytest tools/test_agent_budget.py tools/test_warn_messages.py -q`
```
..............................                                           [100%]
174 passed in 23.08s
```
Questions: none. Not committed.
