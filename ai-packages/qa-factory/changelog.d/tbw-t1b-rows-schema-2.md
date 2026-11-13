- `references/stage-joints.json`, `stage_joints.py`, `exit_gate.py`, `contract_slices.py`: the joints rows file moves to schema 2 with
  renamed keys, and `stage_joints.load_rows` is its one reader: a schema 1 file, an unknown schema, an absent or a broken file is named
  and refused, never read as "no rows". `exit_gate.all_errors` now takes the full check id in `own(...)`, so the id a family carries
  at run time is the id the rows file names; the text-end record carries the check `exit_gate:text_end_after_handback`. Every reader
  of the old keys changed in the same commit (`exit_members`, the pins, `audit`, `demand_tokens`, the contract slices).
