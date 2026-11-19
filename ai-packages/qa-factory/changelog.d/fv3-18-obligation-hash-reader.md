- the row-field check no longer demands a per-reference `obligation_hash` when the plan's obligations cannot be read (`scripts/window_record.py`,
  `scripts/contract.py`): the code writes that hash only with a readable plan, so a role-sent row of ids only passes there; with a readable
  plan a hash-less reference is still refused, and a wrong or non-string hash, an unknown id and the window finish are unchanged (FV3-18)
