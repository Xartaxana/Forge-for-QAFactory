# t-988 S-C report: the `test:` line gate

Nothing committed; all owns STAGED (dispatch_manifest.py included, for the Lead to commit).

## What changed

`tools/dispatch_manifest.py`
- `SKIP_ONLY_ITEMS = ("test",)`, `_ALL_ITEMS = ITEMS + SKIP_ONLY_ITEMS`, `_DISPLAY` gains `test` (lines 97-100), `TEST_LINE_REFUSES = True` (103). `KEY_GROUPS`, `ITEMS`, the header grammar untouched.
- `_FORM_HINTS["test"]` (129, text of spec 5.1 item 4); `_expected_forms` appends it (145-146; it is built over KEY_GROUPS, so the test hint is added by SKIP_ONLY_ITEMS loop, not by ITEMS).
- New `TEST_LINE_NOT_ENFORCED_NOTE_TEMPLATE` (177) for the False switch (spec: "False -> reported as a note"; the wording of the note is mine, see Questions).
- New `_test_candidates` (927), `test_lines(cut)` (954, returns [(line_index, where, source)] of well-formed lines), `_test_state` (960: `no line` | `ill-formed: <first bad line, 80 chars>`).
- `check_cut`: after `_form_missing`, for `is_builder` and `max(designer_threshold(cut)) >= DESIGNER_THRESHOLD` -> `missing["test"]`; not on a degraded cut (early return), not under threshold, not for non-builder.
- Iteration sites of item 4 (line after edit): `_parse_skip_line` 288 (`_ALL_ITEMS`); `SKIP_REFUSED_TEMPLATE` 159; `newly` 1025; `still` 1033; `_items_text` via `_DISPLAY` (updated at 100; the function body is unchanged and no longer KeyErrors); `_expected_forms` 145-146; INCOMPLETE hint 129. `section_cut`'s `sections` dict stays on `ITEMS` on purpose (no `test` section exists). `waivers()` goes through `_parse_skip_line`, so it returns a `test` waiver too (harmless, readers `.get` named items).
- Switch False: `test_unenforced` (1036, 1043) removes `test` from `still` and adds the note.

`tools/dispatch_new.py`: `--test` (repeatable, `action="append"`), printed as `test: <value>` right after the `DoD:` line (`build_text`); `_empty_item` also checks `test` (empty-item refusal); the newline/backtick refusal already walks list values.

`tools/test_dispatch_manifest.py`: `PARTS` gained a default `test:` line after `dod` (E-C3: every over-threshold builder prompt of the file asserting exit 0 now carries a line; none weakened); K1/K5/K6/K7 and `_EXPECTED_INCOMPLETE` expectations gained `test` (expected from spec 5.1 items 3-4: the item name `test` last in `_ALL_ITEMS`, hint text verbatim from item 4); new table `_TEST_LINE_ROWS` + `test_test_line`, and `test_test_line_skip_door_and_reader_and_switch`.

`tools/test_dispatch_new.py`: `THREE_OWNS` carries `--test` (E-C3); new rows `test-line-printed-under-dod`, `test-line-absent-over-threshold` (item 7) plus `test-line-ill-formed`, `test-line-empty-item`, `test-line-backtick`; row `C1-2-empty-owns-item` now builds from `THREE_OWNS_NO_TEST`.

`test_dispatch_gate.py`, `test_dispatch_gate_md.py`: no change needed (green as is; no over-threshold exit-0 prompt in them turned).

## E-C3 changed cases
test_dispatch_manifest: all 30 `test_form_table_siblings_and_designer[des-*]` rows, `test_owns_continuation_limit_40...`, `test_designer_skip_note...` (2), `test_form_switch_off...` (all via the `PARTS` default line), K1, K5, K6, K7, `test_incomplete_text_is_verbatim` (expectation edited, exit codes kept). test_dispatch_new: 4 designer rows x2 tests and `test_block_leaves_the_manifest_reads_unchanged` (via `THREE_OWNS --test`).

## Table rows -> spec item (expected values from the spec text)
- pass: plain line, after last header, under `siblings:`, bullet, `**test:**`, `**` prefix, backtick pair, `TEST:`, `Expected From:`, `|` inside WHERE, FIRST `| expected from:` splits, `none -- reason` (and `—`), CRLF, one good line beside a bad, nonsense source, Cyrillic source, 100000-char source (magnitude), `manifest-skip: test`, `manifest-skip: TEST`, under threshold (2 owns), critic and scout kinds -> spec item 1, 2, error-direction paragraph, E-C1/E-C4 door.
- refuse (label exact): no line; 3 numbered items no line (item 2); line only in fence / blockquote / nested blockquote (item 1); prose `Test row:`; fullwidth colon; `none | expected from: x`; `none -- -`; no source; empty source; blank source in backticks; empty WHERE; label cut at 80 chars (item 2).
- door: `manifest-skip: tests -- r` unknown item and the refusal lists `test`; `manifest-skip: test` no reason -> SKIP REFUSED; skip note names `test`; reader `test_lines` returns well-formed unquoted only; `TEST_LINE_REFUSES` False -> note, exit 0; degraded cut -> unchecked note (items 2, 3, 5, 6).
- dispatch_new: `--test` printed under DoD, absent/ill-formed over threshold refused, empty and backtick items refused (item 7).
- AT and BEYOND the limit: threshold AT = 3 owned paths / 3 numbered items (refused without a line) and below = 2 owns (passes); the 80-char cut AT (74 w's after the 6-char prefix makes 80) and beyond (200).

## Witness (verbatim tails)
`python -m pytest tools/test_dispatch_manifest.py tools/test_dispatch_new.py tools/test_dispatch_gate.py tools/test_dispatch_gate_md.py -q -p no:cacheprovider`
```
......................................................................   [100%]
790 passed in 25.40s
```
Before the tests were adapted the same run was `46 failed, 700 passed` (the E-C3 cases above), i.e. the gate does turn over-threshold prompts without a line.

Sibling runs (each once):
- `tools/test_owns_gate.py` 103 passed in 4.97s; `test_owns_gate_md.py` 28 passed in 1.07s; `test_owns_gate_retry.py` 14 passed in 0.97s
- `tools/test_hook_liveness_probe.py` 88 passed in 74.47s (over a minute; ran anyway)
- `tools/test_journal_hooks.py` 92 passed in 48.04s
Answer: none of these asserts a launch decision on an over-threshold builder prompt that the new gate turns (all green unedited). Not proven by reading each file, proven by the green run on the new gate.

## Four questions (spec 10.1, M2) and axis block
(a) cost: designer <= 1 line per behaviour item; coordinator `--test`. (c) detector: check "Forge test discipline" (a). (d) not skipped: `dispatch_manifest.check_cut` on the launch hook (`dispatch_gate.decide_full` calls it), code on the path. (b) = the axis block below.

Paste into the commit message (spec 10.2):
```
axis 1 (Policy <-> role files <-> journal): covered -- M1-M5: critic.md 17/20, builder.md 4/8, designer.md 1, CLAUDE.md rule 3 and R11-h (M3) and the calibration check change together in S-B; journal fields unchanged
axis 2 (Per-tier exam instruments): covered -- M3/M4 edit critic.md; PROCESS/CRITIC_EXAM.md absent, debt F3-1, deviation line; M1/M2/M5: no exam instrument reads these texts
axis 3 (Factory package <-> its release copy <-> the installed plugin): covered -- M3: scripts/tests/mutate_once.py changes in the package and travels with the next release copy, changelog.d fragment in S-E; M1/M2/M4/M5: n/a, forge texts and tools only
axis 4 (Factory rules <-> their debt <-> the backlog <-> the principles): n/a -- M1-M5 change no FR, principle or debt line; S-E's FR pass is in its report
axis 5 (Stage twins inside the package): n/a -- M1-M5: the runner is a test helper with no stage twin; no stage function touched
axis 6 (Measurement tools <-> the package they measure): n/a -- M1-M5: no measurer changes
axis 7 (Per-test identity <-> every scope a test's behaviour depends on): n/a -- M1-M5: no per-test identity is computed or stored; the runner runs one given file
axis 8 (Where the story is on disk): n/a -- M1-M5: no story path is read
axis 9 (is this a test file): n/a -- M1-M5: no code decides whether a path is a test file; the test: WHERE is free text, the runner runs what it is given
axis 10 (git-top readers): n/a -- M3: the runner takes --root explicitly and reads no git top; M1/M2/M4/M5 read none
axis 11 (shell-command recognizers): n/a -- M3: the probe is a python -B <abs path> call, a listed hygiene door; hygiene_gate.py unchanged; M1/M2/M4/M5 none
axis 12 (carriers of the work plan): covered -- M1-M5: the five nodes go into an untaken batch of pile forge (L-7); no BACKLOG.md line
axis 13 (the dispatch text): covered -- M2 reads the one cut, adds no private scan, and joins the skip vocabulary at every iteration site of check_cut; dispatch_new asks the hook's decision; M1/M3/M4/M5 n/a
axis 14 (readers of agent transcripts): n/a -- M3: no new code reader; the check's (b) counts runner calls by a hand Grep over the critic's transcript, as check 13 (c) does; M1/M2/M4/M5 none
axis 15 (console stream setup): covered -- M3: the changed runner prints; S-E runs test_console_encoding.py (7b); M1/M2/M4/M5 n/a
axis 16 (one JSON reader of the package): n/a -- M3: S-E adds no JSON read; the spec-file form's existing json.loads stays untouched (analog noted in the spec, not widened); M1/M2/M4/M5 none
axis 17 (detector verdict shape): covered -- M3: mutants joins the one verdict shape and its one reader check_text; M1/M2/M4/M5 n/a
axis 18 (in-tree shrink-only ratchets): n/a -- M1-M5 raise no ratchet; a dup or lint raise in S-C, S-D or S-E would be named in the verdict
axis 19 (one reader of a role file's tools line): n/a -- M1-M5: no code reads a tools: line; critic.md's tools: line unchanged (Bash already there)
axis 20 (host receipt names): n/a -- M1-M5 touch no host receipt
axis 21 (readers of the package's markdown tables): n/a -- M1-M5 read no package markdown table
axis 22 (a host's return form): n/a -- M1-M5 touch no host return form
axis 23 (fields of a tests[] row): n/a -- M1-M5 touch no tests[] row
axis 24 (the record of an execution): n/a -- M1-M5 write no execution record
axis 25 (freshness of a run and of a live check): n/a -- M1-M5 judge no freshness
axis 26 (the word stand not confirmed): n/a -- M1-M5 do not use it
axis 27 (the profile of a test row): n/a -- M1-M5 name no profile
axis 28 (the render site of the row form): n/a -- M1-M5 render no row form
axis 29 (append-only jsonl writers): n/a -- M1-M5 append no jsonl line
axis 30 (the commands of a profile): n/a -- M3: the runner builds its own python/pytest argv for a probe, not a project profile command; M1/M2/M4/M5 none
axis 31 (Role carriers): covered -- M1-M5: one home per aspect (oracle, test line, red-before, new-file goal in TESTING.md; the probe, its runner and its cap in the brief, the cap number also in the checker as data); pointers elsewhere; SIBLING_MAP row; carrier-test rows
axis 32 (Where judgment lives): covered -- M2/M3: code checks presence, shape, joins and process outcomes; sufficiency, equivalence, load-bearing places, the value's source and the new-file choice stay with the critic and the Lead (M1/M4/M5)
axis 33 (which dispatch am I): n/a -- M1-M5 pick no dispatch for a session
axis 34 (One road for one action): covered -- M2: every builder dispatch over the threshold; M3: every critic diff verdict, every probe through the one runner, package and forge tests alike; M5: one file rule for package and forge; no language, project or case exempt
axis 35 (Sides of a story): n/a -- M1-M5 touch no story side
axis 36 (The row written against a substitute): n/a -- M1-M5 touch no substitute row
axis 37 (A repeat stop): n/a -- M1-M5 touch no repeat stop
```
tier line for the commit: Lead's.

## Questions (not decided by me)
1. The note text for `TEST_LINE_REFUSES = False` is not in the spec ("reported as a note"); I wrote `TEST LINE NOT ENFORCED (TEST_LINE_REFUSES is off): ...` modelled on the siblings/designer note. The switch is final True, so the text is dead; confirm or drop.
2. The hint text of item 4 contains Cyrillic («Строка теста в DoD») and is now part of every INCOMPLETE refusal on stderr; the spec mandates it verbatim, `tools/` is outside the package (no FR-30). A console with a non-UTF-8 stderr could fail to print it: not measured here (pytest passed; hooks' stderr encoding not tested).
3. The spec's `none`-WHERE rule: I read "WHERE is `none`" as WHERE starting with the word `none` (`none(?!\w)`); `none.py` therefore counts as the none-form with reason `py` (passes). Edge not in spec.

## Deviations / findings
- `_expected_forms` is built over KEY_GROUPS, not ITEMS, so I appended the test hint explicitly (spec: "if it is built over ITEMS").
- `docs/TESTING.md` section «Строка теста в DoD» exists (S-A1 landed, E-C2 satisfied): not re-verified by grep in this run.

## Analogs noticed outside owns (report only)
- `UNCHECKED_NOTE_TEMPLATE` lists items by KEY_GROUPS and does not name `test` (fine: not checked on a degraded cut).
- `SECTION_STOP_RE` / `_HEADER_RE` do not know `test:`: a `test:` line is absorbed into the extent of the section above it (DoD, or `siblings:`), as pass-under-siblings shows; a bare path on it could count as a siblings continuation path (`_REL_PATH_RE`) -- harmless (false pass of siblings only when it already has a tail).
- Another reader of the dispatch text (`owns_gate`, `dod_gate`) was not walked for the extra line.

needed beyond the manifest: tools/hook_liveness_probe.py (const_ref INCOMPLETE_TEMPLATE, grep), test_owns_gate*.py, test_hook_liveness_probe.py, test_journal_hooks.py (run only)

## Fix round t-996

- C-F1: `_KEY_PREFIX` defined once, used by `_IDS_HEADER_RE` and `_TEST_KEY_RE` (which now accepts `**test**:`). Rows `pass-bold-key-inner`, `pass-bullet-bold-key-inner`.
- C-F2: `_TEST_NONE_WORD_RE = none(?=\s|--|—|$)`. Rows `pass-where-path-none-dash`, `pass-where-path-none-dot`, `refuse-none-trailing-space`.
- C-F3: rows `pass-designer-kind-not-checked`, `refuse-resubmission-without-line`, `pass-resubmission-with-skip-door`, `refuse-ill-formed-label-at-80`; renamed `pass-huge-source-100k`.
- C-F4: door table `_SKIP_DOOR_ROWS` (skip-unknown-item-tests, skip-no-reason, skip-note-names-test) + three small tests (reader, switch-off, degraded cut).
- C-F5: both NOT_ENFORCED templates name their forms inline (test: via the two `test:` forms; siblings/designer via `_FORM_HINTS`); switch-off test asserts `expected from:`; form-switch test pins the siblings/designer text.
- C-F6: UNCHECKED template lists `_DISPLAY[i] for i in _ALL_ITEMS` (names `test`); degraded-cut test asserts `test` in note; verbatim test updated.
- C-F7: `WHAT_DEGRADED = "..."` spacing restored; `counts` computed once in `check_cut`, passed to `_form_missing`.
- C-F8: tests-over: the spec's pass/refuse list for outside input (dispatch text) and the E-C3 expectation edits (test diff 133 vs code+text 93, from --stat of round 1).
- NEEDED BEYOND MANIFEST: `tools/dispatch_gate.py` line 2042: `_UNCHECKED_NOTE_FALLBACK` must end `siblings, designer and test by eye.` (pinned equal by `test_dispatch_gate.py::test_unchecked_note_fallback_template_equals_the_modules`, currently RED because of C-F6).

DoD output: `python -m pytest tools/test_dispatch_manifest.py tools/test_dispatch_new.py tools/test_dispatch_gate.py tools/test_dispatch_gate_md.py -q` -> `1 failed, 803 passed in 27.55s`; the failure is the fallback pin above.
