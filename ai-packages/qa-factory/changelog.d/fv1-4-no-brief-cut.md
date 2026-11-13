- the brief a role is handed is rendered once and whole (`scripts/brief_pack.py`, FV1-4 N1): the size ladder, the 6 KB ceiling and every
  cut of a person's words are gone; a gate, a warning, an override, a halt or an answer is carried whole at any length (a line break
  or a text over 1000 characters becomes a fenced block, wrapped at 1000 characters with the text as given in the `-decisions.md` side
  file); every digest, source file, test file and row id is a line of the brief (the `-files.md` side file and the `## Not in the
  brief` section no longer exist); the `build` result and `state/brief-sizes.jsonl` carry `bytes` only
  (`{ts, stage, role, dispatch, bytes}`); an answer recorded before this change with the factory's old cut marker is re-worded where it
  is read, to say where the rest lives
- stand lessons (`scripts/project_knowledge.py`, `scripts/gate_preflight.py`): every lesson is a line with its words whole; the cut at
  200 characters and the ten-line limit with its `+N more` pointer are gone
- the role-load brief layer (`scripts/role_load.py`, `references/role-load.json`) is an allowance, not a ceiling: `allowances.brief` and
  `allowances.brief_charter_head` carry the numbers, with defaults in `settings()`
- two dev-time size ratchets are re-based on `harness.normalised_bytes` (the plugin root and the project root replaced by `<root>`), so
  the number is the same on every machine
