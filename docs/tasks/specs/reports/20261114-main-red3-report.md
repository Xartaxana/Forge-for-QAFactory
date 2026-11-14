# t-764 main-red3 report

Cause: in `driver_stage_plan.py::s4_after_critic` the call `_code, out = self.py("critic_rollcall.py", ... "--apply-fixes")` was an A27 counted site (U, uncontrolled exit) before FV1-9, because `out` was never read after the assignment, so the `# remains: R1 (C1-7b)` door covered it. Since da10e9d/2f6e4bf the next statements read `out` (`self.tell_rollcall(out)`), so `_a27_window_read` is true, the site classes as "ok" and is no longer counted; the door then "touches no counted site" (A27 line 2304).

Fix: the comment above the statement no longer starts with `# remains:` (reworded as an ordinary comment keeping the R1 / C1-7b reason and noting why it is not a counted site). One package file, comment only. Baseline not touched.

Witness (from the package dir, subshell):
- `python -B scripts/tests/test_audit_rules.py` -> `=== audit rules (A1/A9/A11/A13/A14/A17/A20/A21/A22/A27): 375/375 ok ===`
- `python -B scripts/selftest.py --limits --lang` -> `=== qa-factory selftest: 4/4 ok ===`

Analogs: S3 twin: the planner's tell goes through the same `tell_rollcall` inside the one call; no separate S3 roll-call call or door exists in driver*.py. The only other `critic_rollcall.py` call is `driver_gates.py:595` (`code, out = ...`, `code` is read, no door). Other `remains:` doors in driver_stage_plan.py (lines 228-469) do not involve FV1-9 statements; audit reports zero findings so none is stale.
