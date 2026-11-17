- `live_check_demand` converted (`proof_level.py`, `acceptance.py`, `window_record.py`, `gate-registry.json`, `qa-code-critic.md`): a
  test row nobody measured (no `novelty`, no flag, not handed) in a manifest whose writer did measure novelty is no longer passed
  silently - the window raises one gap `novelty_question:<instance>` and the code critic answers `probe_owed: yes` (a live probe is
  owed) or `probe_owed: no` with `critic_note` in the manifest fragment; `yes` adds the requirement, `no` never overrules a flag.
  A manifest with no measured row (a story begun before the measurement) is not asked; a stored `unknown` keeps its demanded
  probe; the person's word passes the gap through the window's one word road (B-279)
- `manifest_put` refuses a `tests[]` row whose `probe_owed` is present and is not `yes` / `no`, naming the field, the row and both
  values; an absent key is no refusal. `references/stage-joints.json` gains the joint `acceptance:novelty_question`.
- Raised by name (AR-20): the `qa-code-critic` plugin-share baseline in `references/role-load.json`, 72828 -> 73031 (the charter
  paragraph that tells the critic the `probe_owed` answer does not fit the old figure).
