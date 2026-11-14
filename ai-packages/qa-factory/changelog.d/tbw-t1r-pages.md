- told before work, pages (`references/stage-joints.json`, `scripts/stage_joints.py`, `scripts/contract_slices.py`): a closed
  `call_told_families` list names the families whose pre-action checks are told at the call by the refusal, not on the injected key
  page; a call marker added to a page item takes effect only while its family is listed, the row states a requirement, the row has a
  site in code and every producer entry naming the role carries the marker, and otherwise the page item stands; each listed family
  leaves one index line on the key page
- a command row renders as a pointer to its command card (`<script> --help`), the exit-gate digest is told once, and the key page
  splits at the stricter of the page width and the one slice-size cap (`contract_slices.SLICE_MAX_BYTES`, also read by
  `selftest.py --limits`); continuation pages are listed in `references/inject-map.json`
- `stage_joints` K5 counts only real legs and reads the demanded tokens on the key page and its continuation pages; the slices are
  regenerated and the A22 ratchet rows are set to the measure
