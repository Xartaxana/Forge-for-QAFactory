- The gate B bug-draft check (`gate_preflight.py`: `check_bug_drafts`) reads the same `bug_records.no_run_target` as the bug-record
  verdict: a draft of a place the analyst walked, for a case the runner never ran, no longer gets the two findings "bug draft
  without a triage verdict" / "bug draft without an APP_BUG verdict" (such a draft has no live triage row by construction, its
  walk record is its evidence, which `reproduction_problems` still checks). Every other finding of the draft (case review, steps,
  red test, cause, reproduction, manifestations) stays. A draft whose instance the run report holds, a missing or unreadable
  report, or a predicate that cannot answer keeps both findings (an unknown never lifts).
