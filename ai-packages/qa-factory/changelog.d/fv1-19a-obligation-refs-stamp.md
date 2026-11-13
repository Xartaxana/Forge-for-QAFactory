### Changed
- `obligation_refs` hashes are written by the code alone: `manifest_put` stamps each ref's `obligation_hash`, each binding's hash, the row's `obligation_ids` and its row `obligation_hash` from the plan. A role sends obligation ids only; a hash that differs from the plan's is refused with the one to leave out.
- `manifest_from_tests` writes ids-only refs through the same stamp, and a marker is judged against the whole plan, like a fragment. `migrate_artifacts` no longer forwards stored hashes.
- A plan file that cannot be read prints one note; refs are then stored as sent and the window finish still refuses them.
- A stale stored binding hash is never refreshed by a patch that does not re-judge: only a binding that re-sends its `design_assessment` gets the current plan hash; a receipt or sensitivity patch leaves the stored hash as it is.
- `migrate_artifacts` retractions (case ghosts, legacy selector rows) resend a row by identity only; the stored refs, ids and hashes of a covering row stay exactly as stored and a retraction never reads the plan.
