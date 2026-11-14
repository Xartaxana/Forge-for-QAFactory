- the generated key page of a role (`references/slices/<role>/handoff-keys.md`) gains the section `## What code will check of you`: the
  rows of `references/stage-joints.json` that state a requirement, for that role, stage and capability (a shell or no shell), one line
  each through `stage_joints.told_line`, the dispatch-only rows under one sub-heading per group (`Only in a plan dispatch (replaces ...)`
  and the others, the `(replaces ...)` text generated from `when_exclusive`), and `Not yet in rows` with the role's hand card while
  `told_ratchet.hand_cards` is above 0; a role with no rows says so, an unreadable rows file is named on the page and red;
  `contract_slices.requirement_section` turns the page leg of `stage_joints` on
- the qa-case-critic gets a key page too (`inject-map.json` lists it after its `common-rules.md` slice)
- a key page over 80 % of `MAX_BLOCK_CHARS` prints `WARN K8 ...` with the split (a hand line for `handoff-keys-<n+1>.md` in
  `inject-map.json`, then `contract_slices.py --write`), over 100 % it is red; `--write` lays the rows over the listed pages, a row is
  never cut, a group heading repeats with `(continued)`, a listed page with no row says so, an unlisted generated page is deleted by
  `--write` and red under `--check`, pages that are not consecutive are red
- the key pages (and every continuation page) are injected inline in every `config.prompts.slices` mode and a `kinds.*.drop_sections`
  row naming one is refused by `inject_context.map_problems` and ignored by `delivered_text`; one list for all readers,
  `contract_slices.inline_subject`
- `role_load.native_headroom_problems` (K10): the plugin share of a role against the Codex native-context ceiling
  (100000 characters less 26000 per `project:` entry, the packet allowance and 200), red over the headroom unless at or under the role's
  baseline `native_headroom.<role>` of `references/role-load.json`; `contract_slices.py --check` calls it
- `references/role-load.json`: `ratchet_tokens` and `process_ratchet_tokens` rise for all twelve roles by the measured size of the new
  section (the hand card is told on the page as well as in the brief until the brief side moves to rows); `native_headroom` baseline for
  qa-test-strategist
