- dry story stub (`scripts/tests/dry_stub.py`, `dry_driver.py`, `fixtures/stories/dry-1/`): the stub that stands in for `claude -p` in the dry
  world fills every role output through the P1-a filler and raises `Unfillable` (form, field, reason) where the filler has no kind, so nothing is
  ever hand-written; the automator branch writes the test file of the runner row's language and runs the command of the world's own profile
  (`profile_contract.profile_commands`), never one found in a brief; the conductor branch offers every open move priced from the move's own row,
  or the row's variant, and runs a move's own command or names `conductor_judgment`; `session_id` is `stub-<dispatch>-<n>` with a counter per
  dispatch and the journal `state/dry-stub.jsonl` opens with the run class; `dry_driver.py` records `{key, answers}` of every closed question
  to `state/dry-priced.jsonl` behind a passing spy on `no_move.priced_options`; the synthetic story `dry-1` (two requirements, one automated case,
  one manual case, the first runner row `python-pytest`) is readable by `scenario_walk.load_story` (P1-b N2)
- dry story, main pass past gate A (P1-b N2e): the runner project holds one passing test (`test_cart.py`) so the reporter probe has a test to name and
  gate A records its approval; the profile command targets the project root; the story's S5 rows carry the scripted stand answer, the automator's
  digest, its `then_bindings`/`obligation_bindings` fragment (`manifest_fragments`, merged by `manifest_put.py`) and a manifest override that
  leaves the code-written hash out; the automator branch derives `profile_id` from the runner row and runs the role's scoped run
  (`run_suite.py --mine`); a stop prints up to 6000 characters of the question details
