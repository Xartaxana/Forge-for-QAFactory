- An unverified selector contract no longer stops a behavioural run: `validate_request` stops refusing on
  `command.selector_contract_verified`, and `run_suite.py` prints ONE `SELECTORS (note)` line on both roads (`--request`,
  `--mine`) naming what was not proven and the door (`onboarding_probe.py --probe-profiles --profile <id>`).
- A selected test the runner did not run still comes back `not_run` ("report row missing"), never passed. New requests no
  longer carry `selector_contract_verified` (the template drops it, `--mine` neither writes nor copies it); an old request
  that still has it resolves as one without.
