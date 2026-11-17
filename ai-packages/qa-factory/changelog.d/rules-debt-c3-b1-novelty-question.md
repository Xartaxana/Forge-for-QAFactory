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
- `manifest_from_tests.py` now writes the marker the question reads: when novelty could not be measured for a test row (the measure
  raised, or the measurer gave a row no stored block) the fragment carries a top-level `novelty_unmeasured` text naming why; a fully
  measured story carries no such key in its fragment, and a story with nothing to measure carries none either. The marker is
  sticky: set once a writer run could not measure a row, a later run does not clear it (the writer builds per file subset, and a
  later subset must not erase an earlier subset's failure). Rows of a language the measurer does not read (non-Python test files)
  are marked too: the fragment's `novelty_unmeasured` names how many.
- A person's recorded S5 word `novelty_question:<instance>` now lets that gap go, by the same head road as `review:<instance>`
  (kinds never cross, an instance never lends its word to another). A writer re-run that carries other test bytes drops the stored
  `probe_owed` / `critic_note` of the row, so the question is asked again for the new code. One reader of the closed answer:
  `proof_level.probe_owed_answer`.
- Raised by name (AR-20): the `process_ratchet_tokens` entry of `qa-code-critic` in `references/role-load.json`, 21173 -> 21224 (the charter line of C3-b1; node K1b pays it down). The stage-joints walk pins follow the one added row `acceptance:novelty_question`: window 27 -> 28, rows 267 -> 268.
