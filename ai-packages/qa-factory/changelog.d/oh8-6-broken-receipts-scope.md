- a broken host receipt, controller file, legacy activity spool or host binding no longer raises out of a hook
  (`host_dispatch.py`, `activity_capture.py`, `cost_capture.py`): the SubagentStop mark, the launch scan and the controller
  lookup read through `hooklib.read_json`, skip the file (bytes unchanged, the new receipt is still written) and say so once
  per path through `person_signal` (`host_receipt_unreadable`); a broken project config at the launch names no story and
  still writes the receipt; `receipt_files` takes an optional `skipped` list; a cost capture whose host binding gives no
  usable activity keeps the session total and prints `telemetry_coverage.attribution: incomplete: ...`
- the SCOPE paragraph of `refusal_registry.py` names all six scanned modules, and a test holds it to `SCANNED`
