# t-107 report: recapture of the s6-w1-frozen fixture, return of the test to the kept set

Worktree: C:\QAFactory\forge-repo\.claude\worktrees\agent-af7d81777a54bb206 (base tree 8afd343). Not committed.

## Items

1. DONE. Byte copy of the fixture taken to the scratchpad (`...\scratchpad\orig`) first; file run as is: 4/6 (tally below).
2. DONE. `BRIEF_BYTES` now matches `N B, N B` and `N B, N budget B` (the label is kept in the replacement, so a label change stays visible; the existing
   wording-change negative control still holds). Run: still 4/6; `calls` red (first-look line), `console` red now only on the label (old fixture says
   `B against`, live says `budget B against`).
3. DONE. Recapture twice into new temp folders; the two captures are byte-equal for all four files (stable).
4. DONE. Differences table below: 4 rows, all of the first kind. No lanes-made difference.
5. DONE. New capture installed (converted to LF: the capture writes CRLF on Windows, the repo's `.gitattributes` says `eol=lf`, `git ls-files --eol` of the old files i/lf),
   docstring line added (retaken 12.11.2026 at tree 8afd343, the two named changes), file 6/6. Negative control red.
6. DONE. `test_quarantine.py check` passes without refusal; row moved from `quarantine` to `keep` (details below).

## Differences, old fixture vs new capture (structural diff, ALL differences)

| # | file / key | what changed | brought by | verdict (spec C.1) |
|---|---|---|---|---|
| 1 | calls.json [0] prompt (S6-qa-runner-1) | one extra input line `  qa-factory/artifacts/QA-9/work/first-look.yaml` after `story-case-links.json` | first-look work: `brief_pack.FIRST_LOOK_FILE = "work/first-look.yaml"`, landed with the merge 5498318 ("the experiment line"), after the capture | legitimate change of the old road, not lanes (the runner prompt lists the first-look record, `brief_pack.py` FIRST_LOOK_FILE / `digest_template_lines`); lanes-independent: it appears at walkers-1 identically in both lanes |
| 2 | calls.json [1] prompt (S6-qa-runner-2) | the same extra line | same | same |
| 3 | console.json [0] note line | `(5,480 B, 4,174 B against the ceiling)` became `(<bytes> B, <bytes> budget B against the ceiling)` | label: 2b1b36c (PC2-3: "the brief note prints budget bytes as `budget B`"); the `<bytes>` form is only the M7 mask now applied at capture (the old fixture was masked at compare time) | legitimate change of the old road, not lanes (the label is the PC2-3 wording) |
| 4 | console.json [1] note line | same as 3, for S6-qa-runner-2 | same | same |

events.json: no difference (script rows, registrations, starts, finishes, errors, accepted: equal). state_keys.json: no difference (`asked, interrupted,
package_check, pending_words, sessions, walk_old_road`). So neither `self.boundary = "S6"` (driver_stage_s6.py:1667) nor `walk_next_id(...)` (:1703)
shows in this capture (critic t-096 B1 reading: "may or may not show"; it does not). Note: the compare of `events` and `state_keys` passed against the OLD fixture too
(PASS before and after the mask).

Git view of the install (`git diff --stat`): calls.json 4 lines, console.json 4 lines, the test file 6 lines; events.json and state_keys.json byte-unchanged.

## Verbatim tallies

Before (as is):
```
FAIL (the whole list of this file): w1_frozen_calls: ... | w1_frozen_console: ...
PASS w1_frozen_events / PASS w1_frozen_state_keys / PASS w1_frozen_brief_bytes_mask x2
=== test_story_run_s6_w1_frozen: 4/6 ok ===
```
After the mask (old fixture):
```
FAIL (the whole list of this file): w1_frozen_calls ... | w1_frozen_console ...
console: live "...(<bytes> B, <bytes> budget B against the ceiling)..." | frozen "...(<bytes> B, <bytes> B against the ceiling)..."
=== test_story_run_s6_w1_frozen: 4/6 ok ===
```
After the recapture:
```
PASS w1_frozen_calls: every call of the story (kind, role, resume, prompt) equals the pre-C1 capture, in order
PASS w1_frozen_events: ...
PASS w1_frozen_state_keys: ...
PASS w1_frozen_console: ...
PASS w1_frozen_brief_bytes_mask: M7 holds for both byte variants (5,480/4,174 and 5,554/4,248)
PASS w1_frozen_brief_bytes_mask: a wording change on the same line is still caught (negative control)
=== test_story_run_s6_w1_frozen: 6/6 ok ===
```

## Negative control
Copy of the new fixture folder with `Return your digest line only` -> `Return your DIGEST line only` in calls.json, run with `--fixtures <copy>`:
```
FAIL w1_frozen_calls: every call of the story (kind, role, resume, prompt) equals the pre-C1 capture, in order — first difference at #0: live {"kind": "role", ...
=== test_story_run_s6_w1_frozen: 5/6 ok ===
```
(the other keys PASS: only the altered key goes red.)

## Item 6: test-layers.json
- Row removed from `quarantine` (it was `red_at_entry: true`, cohort 8073673). The cohort `keep_fail_at_entry` list does not name this file; no cohort count touched.
- Kept row `test_story_run_s6_w1_frozen.py` added after `test_story_run_s6.py`: `layer: detector` (chosen because the dispatch asked for `named_by` + `replaced_by: null`, which `selftest.layers_problems` demands only of a detector; see question Q1), `named_by`: spec t-2147 lines 334 (C.1) and 370 (CI), `replaced_by: null`, `covers`: controller.py, story_run.py, driver_*.py (as `test_walk_lanes_parallel.py`), brief_pack.py, tests/harness.py, tests/story_run_common.py, tests/test_controller_state.py, tests/test_story_run_s5_parallel.py (every tests/ module the file imports; B2 check) and the four fixture files.
- `fixture_owners`: four entries `s6-w1-frozen/<file>.json` -> this test (the check at test_selftest_slow_tests.py:487 requires each owned fixture in `covers`; keys with a folder part work with `is_file`).
- No SLOW_TESTS or timeout row was demanded (the file ran 9 s; `test_selftest_slow_tests.py` 124/124).

## Witness (verbatim, closing lines)
```
python -B tools/test_quarantine.py check            -> quarantine check: 0 violation(s)
python -B .../tests/test_selftest_slow_tests.py     -> === test_selftest_slow_tests: 124/124 ok ===
python -B .../scripts/selftest.py --limits --lang   -> PASS limits: ... / === qa-factory selftest: 4/4 ok ===
python -B .../tests/test_story_run_s6_w1_frozen.py  -> === test_story_run_s6_w1_frozen: 6/6 ok ===
```

## Siblings (report only, no edits)
- `test_story_run_s5_n1_frozen.py` (`--capture` mode, fixture s5-n1-frozen): QUARANTINED; its fixture holds neither `first-look` nor `against the ceiling`, so by the fixture it is not affected by these two changes (live run NOT done: estimate, not verified). It has a stale-by-time risk of the same kind, no more.
- `test_story_step_materialize.py:247` regex `\((\d..) (B|KB)(, \d.. (B|KB) against the ceiling)?\)`: QUARANTINED; does not match the new `N budget B against the ceiling` form, so it is AFFECTED if its output now prints that label (not run: estimate, not verified).
- `test_scenario_world.py:550` (`--capture scenario_beta`): KEPT; a different capture mode (scenario worlds), no brief note or runner prompt pinned (grep of the tests dir for `against the ceiling` shows no hit): not affected.
- `fixtures/judgment-census.json` holds `first-look` words: unrelated (census), not affected.

## Questions / findings
- Q1 (layer): the dispatch's model row (`test_walk_lanes_parallel.py`) is `gate_named` with no `named_by`; the task asked for `named_by` + `replaced_by`, so I used `detector`. If the Lead wants `gate_named` or `scenario`, change one word; checks pass either way as far as `layers_problems` goes (not run for the alternatives).
- The kept file imports the QUARANTINED `test_story_run_s5_parallel.py` (`import ... as P`); `test_quarantine.py check` raises no violation, but when TD-15.8 cuts held-by-import files this kept row is the importer to name.
- Capture writes CRLF on Windows (`write_text`): a later recapture on Windows needs the same LF conversion. Docstring does not say so; not in my owns scope to alter code of `main`.

## FR pass
D (identity and evidence): FR-58 kept: the capture was not used as its own oracle — the old fixture was copied first, differences were enumerated key by key against the product's commits, events/state_keys were byte-equal; FR-41/FR-59 n/a. G (code): FR-30 English only (docstring line, JSON, row text; `selftest --lang` ok); FR-31 n/a (no load-dependent test; capture stable twice); FR-29 no control bytes (LF fixtures); FR-33 n/a (no role behaviour changed). Sections A, B, C, E, F: not touched. AR touched: AR-20 (a kept row, no ratchet raised), AR-13/22 none.

## Needed beyond the manifest
`tools/test_quarantine.py` (functions, FORGE_CARRIERS), `selftest.py` `layers_problems` and `gate_named_files`, `test_selftest_slow_tests.py:478-490`, `.gitattributes` via `git ls-files --eol`, git log for 5498318 / 2b1b36c, test-layers.json `keep` shape.
