# t-116 attempt 2 -- fix round report

1. B-1 DONE. `dod_gate._file_fresh` + `_start_time`: `named_handoffs` returns `(path, folder, start_epoch|None)`
   (start = `timestamp` of the first record of the worker transcript); `_handoff_block` passes when the file exists and
   mtime >= start, or start unreadable. Rows added: `file-fresh-not-in-track` (pass), `file-older-than-dispatch`
   (block once), `file-exists-start-unreadable` (pass).
2. B-2 DONE. All three rules: "at most 2,000 characters and at most 4 + N lines", "The form is always four lines",
   N = 0 status line is `done` / `not done -- <one clause>` / `question`; the "0 items: 3 lines" sentence is gone.
3. F-1 DONE. Pointer clause in all three: "a dispatch whose spec is a pointer counts the node it points to, and when you
   cannot tell, N = 0".
4. F-3 DONE. Critic: N = numbered or lettered questions/keys the dispatch asks, status `answered` / `not answered --
   <one clause>`. Designer: N = numbered requirements of the brief, status `drafted` / `fork` / `not drafted -- <one clause>`.
5. F-4 DONE. Row `valve-counts-the-handoff-block` (stops [2,2,0]; gate_log handoff_missing, blocked,
   skipped_after_2_blocks) plus `test_handoff_check_skipped_when_the_valve_is_already_spent` (consecutive_blocks=2 ->
   pass, no handoff_missing). The second is a separate test function, not a table row (a table row cannot preset
   consecutive_blocks); the valve-counting one is a table row.
6. Other F-n:
   - F-5 DONE: scout pins (both) also assert K2 absent; RESTATED gained "2 000 символов", "2000 символов".
   - F-6 DONE: `handoff_written` imports handoff_gate via `_import_readers()` (failure -> pass) and uses
     `hg._real` and `hg.SEGMENT_SPLIT_RE`; the local realpath/split copies are gone.
   - F-9 DONE: `named_handoffs` prefers `payload["agent_transcript_path"]` when present, else derives as before
     (live-proof line for the batch evidence is the Lead's: "one critic that skips its Write gets exactly one HANDOFF MISSING").
   - F-2 NOT DONE (design choice on the status vocabulary, `partial`): left to the Lead.
   - Left to the Lead (outside owns / queue): F-7 SIBLING_MAP rows 316, 333; F-8 race; protocol :828 and :860;
     `handback_extract.py` counts bytes while the cap is in characters (and its "25 lines" docstrings at :31, :158);
     `hop_metrics.py:209` docstring.

Changed expectations: none of the existing `test_handoff_missing_table` rows changed (the rows with no file on disk still
block). The row body now creates the report file only for the three `file-*` rows and passes no green run for the valve row.
Siblings: `critic-diff-brief.md` and `plans/builder-rules.md` 11 still only point (`test_brief_what_comes_back`,
`test_builder_rules_p11` green).

## Final rule texts (rule 7 builder / 16 critic / 5 designer, the changed sentences)

builder.md 7: "...then end with a final message of at most 2,000 characters and at most 4 + N lines (N = the numbered items of
the spec node the dispatch names; a dispatch whose spec is a pointer counts the node it points to, and when you cannot
tell, N = 0; the stricter cap decides). The form is always four lines: the path (`report: <path>`), one status line
`1 done | 2 done | 3 not done -- <one clause> | 4 question` (more than 20 items: ranges, `1-12 done`; with N = 0 the status
line is one of `done` / `not done -- <one clause>` / `question`), `questions: none | 1) <question>`, and `needed beyond
the manifest: none | <paths>`."

critic.md 16: "...at most 2,000 characters and at most 4 + N lines (N = the numbered or lettered questions/keys the dispatch
asks; a dispatch whose spec is a pointer counts the node it points to, and when you cannot tell, N = 0; the stricter cap
decides). The form is always four lines: the path (`report: <path>`), one status line (the verdict line and the number of
blocking findings; per item `1 answered | 2 not answered -- <one clause>`; more than 20 items: ranges; with N = 0 the
status line is one of `done` / `not done -- <one clause>` / `question`), `questions: none | 1) <question>`, and `needed
beyond the manifest: none | <paths>`."

designer.md 5: "...at most 2,000 characters and at most 4 + N lines (N = the numbered requirements of the brief; a dispatch
whose spec is a pointer counts the node it points to, and when you cannot tell, N = 0; the stricter cap decides). The form
is always four lines: the path (`report: <path>`), one status line (per item `1 drafted | 2 fork | 3 not drafted -- <one
clause>`; more than 20 items: ranges; with N = 0 the status line is one of `done` / `not done -- <one clause>` /
`question`), `questions: none | 1) <fork by id, one clause>`, and `needed beyond the manifest: none | <paths>`."

(The files are wrapped at ~70 columns; the anchors K1, K2, "never lost, never shortened", "names no such path",
"the Write is refused", ceil(len/200) are untouched and the anchor tests pass.)

## Witness

`python -m pytest <wt>/tools/test_handoff_rule_anchors.py <wt>/tools/test_dod_gate.py <wt>/tools/test_handoff_gate.py -q -p no:cacheprovider --rootdir <wt>`
closing line: `163 passed in 6.56s`

Needed beyond the manifest: `tools/handoff_gate.py`, `tools/transcripts.py` (read only).
