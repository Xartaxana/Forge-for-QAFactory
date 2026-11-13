### Changed
- `obligation_refs` hashes are written by the code alone: `manifest_put` stamps each ref's `obligation_hash`, each binding's hash, the row's `obligation_ids` and its row `obligation_hash` from the plan. A role sends obligation ids only; a hash that differs from the plan's is refused with the one to leave out.
- `manifest_from_tests` writes ids-only refs through the same stamp, and a marker is judged against the whole plan, like a fragment. `migrate_artifacts` no longer forwards stored hashes.
- A plan file that cannot be read prints one note; refs are then stored as sent and the window finish still refuses them.
