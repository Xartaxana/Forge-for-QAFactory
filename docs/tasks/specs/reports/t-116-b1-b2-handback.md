# t-116 B1 + B2 hand-back (builder, worktree agent-ac59fdf8d182e6ef9, not committed)

## Done
- B1 DONE: builder rule 7, critic rule 16, designer rule 5 carry the new cap and form; numbers unchanged; anchors kept
  ("the file at `handoff:`", ceil(len/200), "names no such path", "the Write is refused", "never lost, never shortened").
  "the closing lines of the witness" left builder 7 (both places). The anchor test: `K2 = "at most 2,000 characters"` (replaces
  "at most 25 lines"); RESTATED follows K2; the negative-control copy text updated; docstring updated.
- B2 DONE: items 1-4 in `tools/dod_gate.py`; test table in `tools/test_dod_gate.py`.

## New rule text (shared core; each role's own status line differs)
Builder 7: "...then end with a final message of at most 2,000 characters and at most 3 + N lines (N = the numbered spec items;
0 items: 3 lines; the stricter cap decides): the path (`report: <path>`), one status line `1 done | 2 done | 3 not done --
<one clause> | 4 question` (more than 20 items: ranges, `1-12 done`), `questions: none | 1) <question>`, and `needed beyond the
manifest: none | <paths>`. No witness lines, tables, logs or file lists in the message: they are in the file. [line definition,
ceil(len/200)] Every closing message -- a resubmission after a hook block or a question included -- repeats the path and the
digest WHOLE; "see above" is forbidden. When the dispatch names no such path, or the Write is refused (the hook says why), the
FULL report, witness included, goes into the final message as before -- never lost, never shortened, and the cap does not apply."
Critic 16: same form, status line = "the verdict line and the number of blocking findings; per item `1 done | 2 not done --
<one clause>`"; "No tables, logs or file lists"; fallback "the FULL verdict ... the cap does not apply".
Designer 5: same form, status line per item, `questions: none | 1) <fork by id, one clause>`; fallback "the draft WHOLE ...
the cap does not apply".

## B2 design (dod_gate.py)
- `BLOCK_MESSAGE`: "Re-submission = repeat the path and the digest whole (or, with no handoff path, the full report); only your
  LAST message reaches the coordinator ...". `HANDOFF_MISSING_MESSAGE`, `HANDOFF_ONCE_KEY` added.
- `named_handoffs(payload, base)`: reads the dispatch via `handoff_gate._worker_file/_dispatch_text/_in_folder/_real` and
  `dispatch_manifest.section_cut/handoff_paths/HANDOFF_DIRS` (lazy `_import_readers`); returns exactly one `(path, folder)` or [].
  Any failure/degraded cut/2+ candidates -> [] (pass), stderr line on a failure. No `transcript_path` in the payload -> [] silently.
- `decide(track, agent_id, handoffs=None, base=None)`: the check runs BEFORE `evaluate` (so before "no-edits"); path match =
  equal normcase(realpath) OR equal trailing segments (HANDOFF_DIRS folder + file name) against this agent's edit records only;
  block -> exit 2, once-key set in `per_agent[key]`, `gate_log` action `handoff_missing`.
- `main`: saves the track when the once-key is set even if the track did not exist.

## Decisions I had to make (flag for Lead; spec was silent / terse)
1. "the existing safety valve counts this block too": the block increments `consecutive_blocks` (a passing stop resets it as
   usual; the once-key is never reset). If `consecutive_blocks` is already >= 2 the handoff check is skipped (the normal path
   decides), so this block can never itself pass the valve.
2. The check needs `base` (payload cwd) to resolve relative edit paths; `decide`'s new params default to None (no check) so old
   callers are unchanged.

## Questions returned
None blocking. `tools/test_handoff_gate.py` stayed green (not edited).

## Siblings / needed beyond the manifest
- Still say "25 lines" (not owned, not edited): `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md:828` (check 28, node P), `tools/handback_extract.py:31,158`
  (line counting by "the 25-line rule", docstrings), `tools/hop_metrics.py:209` (docstring). `docs/tasks/critic-diff-brief.md` and
  `plans/builder-rules.md` 11: `test_brief_what_comes_back` and `test_builder_rules_p11` green = they still only point.
- Read beyond the manifest: `tools/transcripts.py` (agent_file_name, AGENT_ID_RE), `tools/dod_track.py` (edit record format).

## Witness
Command: `python -m pytest tools/test_handoff_rule_anchors.py tools/test_dod_gate.py tools/test_handoff_gate.py -q`
```
........................................................................ [ 45%]
........................................................................ [ 91%]
..............                                                           [100%]
158 passed in 9.37s
```
(First run, before the "no transcript_path -> silent" fix, was 8 failed / 150 passed: the old echo-JSON tests assert empty stderr
for payloads with no transcript_path; fixed in dod_gate, tests not touched.)
