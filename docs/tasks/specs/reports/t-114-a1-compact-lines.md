# t-114 A1 report: post-compaction lines, identity by content

Worktree: agent-af2af1d4bd0f91021. Nothing committed.

## Behaviour items
1. Header: DONE. `compact_snapshot.header_line` writes line 1 `<!-- compact-snapshot: hook; session: <id|unknown>; trigger: <manual|auto|unknown>; written: <ISO> -->`; `snapshot_identity(path)` is the one reader (512 bytes; corrupt header -> fields "unknown"; no header -> None; a read failure raises OSError, the caller skips the file). Session id from the payload (`_read_trigger_from_stdin` now returns `(trigger, session_id)`) or `--session`; `--session` wins.
2. Hook snapshot vs narrative by header, not by name: DONE.
3. "This compaction's" = not announced, age <= STALE_MIN (10 min, compared in seconds), session clause skipped when either id is unknown or `MATCH_SESSION` is False; newest by (mtime, name) wins: DONE.
4. Block (SNAPSHOT or MISSING + door, NARRATIVE only when newer than S or S missing, AFTER COMPACT line): DONE.
5. Announced record `.claude/compact_seen.json` (JSON list, last 200 names), written after the block is built when S is fresh: DONE.
6. REMINDER names CURRENT_CONTEXT.md and `docs/tasks/compact-snapshots/` (newest `*-narrative.md`), no factory-fixes.md: DONE; test is a data join.

## Questions returned / small decisions to confirm
- The door prints `--session <id>` only when the SessionStart payload carries an id; with none it prints the command without the flag (the spec's literal `<id>` has nothing to fill).
- MISSING with no hook snapshot at all reads `(newest hook snapshot none)` (no age); the two record warning lines come after the AFTER COMPACT line.
- Added public helper `compact_snapshot.clean_session_id` (id sanitising: `[A-Za-z0-9_.-]`, 64 chars; used by writer and reader so the compare is like for like) and `header_line` (the writer). Both are in the spirit of "writer and reader in one module"; not in the owns list by name.
- `build_snapshot` and `write_snapshot` gained optional `session=` (and `trigger=` on build); defaults keep every old call valid. Header trigger = source when it is manual/auto, else unknown.

## Callers of the renamed function
`compact_snapshot_line` was called from `tools/session_context.py` (main) and tested in `tools/test_compact_snapshot.py` (rows replaced, both owned). No other caller (grep over the repo; other hits are copies in sibling worktrees and the spec). `tools/hook_liveness_probe.py` only pins the output prefix `COMPACT SNAPSHOT: docs/tasks/compact-snapshots/` of the writer's summary, which is unchanged; its artifact check looks for `# Compact snapshot -- manual` etc. (header is line 1, heading line 2) - not run here, outside owns (probe test file `test_hook_liveness_probe.py` not in the DoD run; an analog worth a Lead look).

## Tests
`test_session_context.py`: one parameterised table `test_a1_compact_block` (19 rows: fresh headed, 11 min, 10 min boundary, already announced, two compactions with second PreCompact absent, unheaded hand-written newest, `-2` suffix, other source name, session mismatch, session unknown in header / in payload, two sessions in a clone, no folder, only README, record corrupt, record not a list, record not writable, last-200 trim, non-compact source) plus single tests for `MATCH_SESSION`, clock skew, unreadable file -> unavailable, temporal both worlds, old name gone.
`test_compact_snapshot.py`: header from payload / `--session` overrides / no session -> unknown / identity round trip / REMINDER data join / main on compact source. All paths through `tmp_path`.

## Verification (witness)
Command: `python -m pytest tools/test_session_context.py tools/test_compact_snapshot.py -q`
Closing lines:
```
........................................................................ [ 94%]
..................                                                       [100%]
306 passed in 63.50s (0:01:03)
```

## Sample blocks (tmp dir; S 3 min old, header session s1, a hand-written narrative 1 min old)
Fresh case:
```
COMPACT SNAPSHOT: docs/tasks/compact-snapshots/2026-11-12-1257-manual.md (3 min old, trigger manual)
COMPACT NARRATIVE: docs/tasks/compact-snapshots/2026-11-12-1210-manual.md (1 min old)
AFTER COMPACT: read the snapshot above before your next action; accept the OPEN DISPATCH lines in a batch
```
MISSING case (same tree, second call 1 minute later, S now announced):
```
COMPACT SNAPSHOT: MISSING for this compaction (newest hook snapshot docs/tasks/compact-snapshots/2026-11-12-1257-manual.md, 4 min old) -- write it now: python -B tools/compact_snapshot.py --source manual --session s1
COMPACT NARRATIVE: docs/tasks/compact-snapshots/2026-11-12-1210-manual.md (2 min old)
AFTER COMPACT: read the snapshot above before your next action; accept the OPEN DISPATCH lines in a batch
```

## Needed beyond the manifest
`tools/hook_liveness_probe.py` (grep for callers/anchors), `tools/gitcmd.py` import chain of compact_snapshot (no edit).
