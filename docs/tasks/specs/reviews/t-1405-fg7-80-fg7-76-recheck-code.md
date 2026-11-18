# t-1405 code review: FG7-80 (t-1404) and FG7-76 re-check (t-1397)

## Verdicts

- **FG7-80 (c1f33f65, diff vs merge base 4f22cb77): NEEDS WORK.** There is one blocking finding, B1 (Q4 class completeness). It carries a `failure_class: spec` note against the dispatch's `siblings:` premise. There are also three fixes before merge: F1, F2 and F3.
- **FG7-76 re-check (f0f499ef vs 350c9868): ACCEPT on the re-check scope.** t-1402 B1 and F3 are fixed. 14 scratch rows on `is_the_swap` and 3 window rows on `_reorder_resume_with` all came out as expected.
- Overall JSON verdict: `blocker`, because FG7-80 B1 blocks. Accepting either node, or taking the rule-9 exit in place of a fix, is the Lead's decision (rule 6).

## The question asked (FG7-80)

"Do the enter refusal and the status line take their words from the CI reader class of the configured host, with the GitLab words kept for GitLab and no change in what enter/status decide?"

- **Yes for the two named texts.**
  - The status line at test_quarantine.py:547 now uses `ci_class(d.get("ci")).START_WATCH`.
  - The schedule refusal at :1190-1193 now uses `ci_class(cfg.get("ci")).SCHEDULE_DOOR`.
  - The GitLab texts are byte-identical to the old ones. The enter refusal is the old string with the door spliced in.
  - Decisions are unchanged: the conditions at :546 and :1188 are untouched, and the only change to `status_data` is the extra `ci` key.
- **No for the class.** Five other enter door texts still give GitLab words when the host is GitHub. That is B1.

## Findings

**B1 (blocks; FG7-80; Q4 / rule 5; dispatcher note `failure_class: spec`). With `ci: github`, five enter refusals still say "run a web pipeline ...", which is GitLab's UI word.**
- The sites in tools/test_quarantine.py:
  - :1166, "run a web pipeline on the current HEAD, then enter again";
  - :1227, "run a web pipeline with TEST_REDUNDANCY=1 REDUNDANCY_SCOPE=keep";
  - :1231-1232, "run a web pipeline with --var ... (a token that reads pipeline variables ...)";
  - :1235, the same text as :1231;
  - :1381, "run a web pipeline on the current HEAD".
- The node itself treats "web pipeline with X" as GitLab words. It replaced exactly that phrase at :547 with `python tools/ci_read.py start ...` for GitHub. The same phrase in the neighbouring refusals of the same command stayed.
- The GitHub door already exists and is documented:
  - ci_read.py:14-17 shows `start [--ref] [--workflow canon.yml] [--var KEY=VALUE ...]`;
  - canon.yml:24-27 declares the inputs TEST_REDUNDANCY and REDUNDANCY_SCOPE, and :25 names `ci_read.py start --ref <b> --var TEST_REDUNDANCY=1`.
- **Scratch proof.** `test_p780_probe.py` sits in the session scratchpad. It imports the worktree's test module and its autouse fixtures, builds a world in tmp, and writes no live file. It sets the config to `ci: github`, applies the file's own `_other_sha` and `_no_report` mutators, and runs `tq.main(["enter", ...])`:
  - `PROBE _other_sha rc= 1 ci= github | [' pipeline on the current HEAD, then enter again ; or, if the owner says the last finished pipeline may stand, pass --owner-word ...']` (the line starts "run a web pipeline");
  - `PROBE _no_report rc= 1 ci= github | ['quarantine enter refused: pipeline 101 has no coverage measurement (test-redundancy) -- run a web pipeline with TEST_REDUNDANCY=1 REDUNDANCY_SCOPE=keep']`.
- **Fix, in the node's own owns (tools/test_quarantine.py).**
  - Add one more per-host attribute beside START_WATCH. For example, a `RUN_DOOR` template: GitLab "run a web pipeline%s on <ref>", GitHub "python tools/ci_read.py start --ref <ref>%s" with the `--var` pairs.
  - Read it at the five sites through `ci_class(cfg["ci"])` (at :1381, `_config(root)`).
  - Add one github row to the existing `ENTER` table, for example a `c7-no-report` github variant.
  - Alternatively, the Lead takes COORDINATOR rule 9's exit with a line `enter refusals :1166/:1227/:1231/:1235/:1381 still give the GitLab "web pipeline" door on ci=github | узел: <id>`.
- **Dispatcher note.** The dispatch's `siblings:` line said "the door texts are its last GitLab words". It gave no premise for that, and a grep of `web pipeline` in the same file disproves it. This is checklist point (5) (freshness), a calibration case.

**F1 (fix before merge; FG7-80; Q6 / Q7 / Q10 one-way). There are now two host pickers, and the old one's docstring is false.**
- `ci_class` (:738-740) maps `ci` to a class. `ci_reader` (:743-746) still maps `ci` to an instance by its own `== "github"` branch.
- `ci_reader`'s docstring still says "The one place that picks the host". The `CI_HOSTS` comment at :70 says "ci_reader() picks the reader".
- The `_GITLAB_HOST` alias (:735) exists only because two tests replace `tq.GitlabCI` with a function (test_test_quarantine.py:524, :1342). So code was shaped around a test stub.
- Fix: correct the two comments so they name both functions and their split (class for words without a token, instance for reads). Or let `ci_reader` choose through `ci_class` for GitHub and keep the late-bound `GitlabCI()` for the stubbed path.
- It does not block: both pickers agree on every value (scratch rows `github -> GithubCI`, `gitlab`/`None`/`other -> GitlabCI`), and `_config` refuses any host outside `CI_HOSTS` first (:152-154).

**F2 (fix before merge; FG7-80; Q5(e) and Q5(g)). The gitlab rows of both new tests repeat existing rows through the same door.**
- The `gitlab` row of `test_status_line_start_words_follow_the_host` (test_test_quarantine.py:327-333) repeats `test_status_line_table` row `release-without-run` (:301). It is the same world (V2, `run_row(1, "0.11.0", **GREEN)`, `pull()`) and the same exact text. The default config at :156 has no `ci`, so `_config` sets `gitlab`.
- The `gitlab` row of `test_enter_schedule_door_follows_the_host` (:336-343) repeats `ENTER` row `c6-schedule-missing` (:501).
- Fix: cut the two gitlab rows. Better still, put the github cases into those two existing tables as one row each (a config mutator `ci: github`) and drop the two new functions and `HOSTS`.

**F3 (fix before merge; FG7-80; Q7). Dead data in the test.**
- The third member of each `HOSTS` tuple (`"Settings -> CI/CD"` / `None`, at :319-320) is never read. Both tests hard-code `"Settings -> CI/CD"` and `"QUARANTINE_WATCH=1"` instead.
- This goes away with F2's fold. Otherwise, drop it.

**Notes (no finding).**
- START_WATCH is filled by `%` and SCHEDULE_DOOR by `.replace("%s", ...)`, because GitHub's door holds two `%s`. Both are single-pass. Scratch rows with branch `a%sb` and `x%d` show each placeholder replaced once, no re-expansion, no leftover `%s`, and ASCII text for both classes.
- The GitHub schedule refusal reads "ask the owner to create it: the schedule is the cron of ...; ... or start one run: ...". The wording is awkward, but the spec's edges (workflow name, cron, the one-off run) are met.
- The mechanical layer has no `red-before:` line. By reading, the github rows would be red on 4f22cb77, which hard-coded both GitLab strings at old :547 and :1174. That covers Q5(a), but the line belongs in the builder's layer (rule 21).

## Standing questions, FG7-80

- **Q1 fit:** the two texts were asked for and are done. Edges:
  - absent `ci`: `setdefault("gitlab")` (:152), and `status_data` defaults `ci` to None, which gives GitLab;
  - github and gitlab: per class;
  - unknown host: refused by `_config` before any text;
  - placeholders: single pass;
  - ASCII: yes.
  - Length: the GitHub suffix is 132 characters against GitLab's 104. session_context.py has only `MAX_LINES = 25` (:202) and no per-line character cap (grep `MAX_LINE|LINE_CAP|[:2xx]`), so the builder's "cap unverified" stands. No defect.
- **Q2 builder decisions:** the unknown host keeps the GitLab text through `ci_class`. That is safe, and it is unreachable behind `_config`.
- **Q3 seams:** additive; `status_data` gains a key that no reader rejects.
- **Q4 class completeness:** B1.
- **Q5 tests:**
  - (a) the github rows kill the defect;
  - (b) the expected values trace to the spec's edges, which give the ci_read command verbatim, and the GitLab values are today's text;
  - (c) both doors have a row;
  - (d) nothing was rewritten;
  - (e) F2;
  - (f) 27 test lines against 31 product lines changed, within budget;
  - (g) no new file.
- **DUPLICATION AND CONSISTENCY (Q6):** F1, the second host picker. No other words table was found: grep `START_WATCH|SCHEDULE_DOOR|ci_class` over tools/*.py finds only the diff's own sites.
- **CODE QUALITY (Q7):** no new function over 60 lines and no deep nesting. Dead data: F3. Lying comments: F1.
- **Q8 hygiene:** not a package file. ASCII confirmed by `.isascii()` in the scratch run.
- **Q9 ratchets:** none touched; the diff stat is 3 files, none a ratchet file.
- **Q10 ARCHITECTURE:** ai-packages/qa-factory/design/architecture.md:258-261 names test_quarantine for purge/enter/check semantics only. Those semantics are unchanged, so no AR-n is touched.
  - **VARIETY:** a GitLab-hosted or GitHub-hosted forge both get their own words. An unknown host is refused loudly, with no silent default.
- **Q11 judgment:** none; only texts changed.
- **ONE ROAD (Q12):** none found. The branch is on the configured host value, the same data row (`ci`, `CI_HOSTS`) that `ci_reader` already reads, and not on a language or project name.
  - Grep: `== "github"` in test_quarantine.py finds two hits, `ci_class` and `ci_reader`; the positive control is that it finds `ci_reader`'s existing branch.

## FG7-76 re-check

**B1 is fixed.** `is_the_swap` (driver_golden.py:976-1016) now implements the shape t-1402 asked for:
- the write at `seq`, plus its publish unit (renames whose `src` equals the write's path);
- k is the first progress record after the unit;
- the mutant has the progress record at `seq`, the records between equal, and the same unit after them;
- the lengths are equal.

Whether a write and its rename share a path was read from driver_trace.py: the write record's path comes from `_abs(path)` (:730) and the rename's `src` from `_abs(args[0])` (:738). event_store `_publish` (:188-204) opens a temp file in the same dir, `path.name + "." + token + ".tmp"`, so the path still contains "driver-runs".

Whether the progress text is the same in both streams was checked by reading. story_progress.py reads `driver-runs.jsonl` and `driver-state.json` (:489-490), not the `driver-runs/` directory. The grep for `"driver-runs"` finds driver_dispatch.py and others but not story_progress.py or task_price.py. `save_state` comes before the progress line in both streams. So the moved write does not change the progress text.

This is an estimate, not checked against a real stream. No golden exists, and recording one is FG7-78's.

Scratch proof: `p776.py` in the session scratchpad makes pure calls with JSON rows built in the script. The verbatim results:
```
OK  exchange W,S,G / G,S,W (True, '')
OK  adjacent W,G / G,W (True, '')
OK  publish unit W+R,S,G / G,S,W+R (True, '')
OK  unit W+R,S,S,G / G,S,S,W+R (True, '')
OK  foreign rename stays between (True, '')
OK  middle differs (False, 'the records between the write and the progress line differ')
OK  unequal lengths (False, 'the streams are 3 and 4 records long')
OK  write changed (False, 'the mutant does not carry the same write after the records between')
OK  rename dropped in mutant (False, 'the mutant does not carry the same write after the records between')
OK  unit split (R left behind) (False, 'the records between the write and the progress line differ')
OK  progress text differs (False, "the mutant's progress line is not the control's")
OK  no progress in control (False, 'the control has no progress line after the driver-runs write')
OK  control has no write at seq (False, 'the control has write here, not the driver-runs write')
OK  stream ends (False, 'a stream ends here')
```

**F3 is fixed.** The window now ends at the first non-blank line indented 4 or fewer spaces (:879-880). The same script refuses three cases, each with the anchor-not-found Refusal:
- a module-level `def helper` holding `self.progress_line()` after `resume_with` as the class's last method (t-1402's row 6 shape);
- a `    @property` decorator after the method;
- class-level code after the method.

Positive control: with a progress line inside the method, the exchange happens and the helper is untouched (`helper intact: True`), and CRLF is kept. A read-only pure call `p776b.py` on the live driver_dispatch.py gives the same two-line exchange as the builder's Witness 1 (:2331 and :2334). Afterwards, `git status --short` in the worktree is empty.

Residual, no finding: a column-0 comment inside `resume_with` would end the window early. That fails toward a refusal, which is the safe direction. The tail after the exchanged span is not compared, as before, and B1 did not ask for it.

## Trail

- Read:
  - the dispatch (scratchpad d-fg780.txt);
  - report t-1404-fg7-80.md;
  - `git diff 4f22cb77 c1f33f65 -- tools/`;
  - test_quarantine.py :59, :70, :152-154, :450-470, :540-581, :625-636, :735-746, :1155-1238, :1375-1383;
  - test_test_quarantine.py :21-27, :98-115, :150-157, :290-345, :361-415, :443-525, :1336-1346;
  - session_context.py :202, :697-707;
  - ci_read.py :14-20;
  - canon.yml :8-31;
  - t-1402 review :13-60;
  - t-1397 report;
  - `git diff 350c9868 f0f499ef`;
  - driver_trace.py :680-738;
  - event_store.py :180-198;
  - driver_runner.py :455-469;
  - story_progress.py :9-10, :489-490;
  - driver_dispatch.py :2326-2334.
- Reruns:
  - DoD witness in the FG7-80 worktree, `python -B -m pytest <wt>/tools/test_test_quarantine.py -q -k "schedule or enter or status"`, gave `84 passed, 190 deselected in 48.11s`. It matches the report's 84, and it imported the worktree's module (the new tests need `ci_class`).
  - Scratch `p780.py`: ci_class rows and placeholder/ASCII rows.
  - `test_p780_probe.py`: B1 proof, 2 passed with the PROBE lines above.
  - `p776.py`: 14 + 3 rows, `BAD ROWS: 0`.
  - `p776b.py`: the live text, read-only.
- Not run: test_quarantine.py check, full sets, any driver probe (no golden).

```json
{
  "verdict": "blocker",
  "blockers": [
    "B1 FG7-80 (Q4 class completeness; dispatcher note failure_class spec): with ci=github five enter refusals still give the GitLab door 'run a web pipeline ...' at tools/test_quarantine.py:1166, :1227, :1231-1232, :1235, :1381; scratch probe test_p780_probe.py prints 'run a web pipeline with TEST_REDUNDANCY=1 REDUNDANCY_SCOPE=keep' and '... pipeline on the current HEAD' under ci=github; fix: one per-host door attribute read through ci_class at those sites plus one github ENTER row, or the Lead's rule-9 exit with a node line"
  ],
  "fixes": [
    "F1 FG7-80 tools/test_quarantine.py:70 and :743-746: ci_reader docstring 'The one place that picks the host' and the CI_HOSTS comment are false now that ci_class (:738) also picks; name both or route ci_reader through ci_class (fix before merge)",
    "F2 FG7-80 tools/test_test_quarantine.py:327-343: gitlab rows duplicate release-without-run (:301) and c6-schedule-missing (:501); cut them or fold the github cases into those two tables (fix before merge)",
    "F3 FG7-80 tools/test_test_quarantine.py:319-320: third HOSTS tuple member never read; drop it (fix before merge)"
  ],
  "class_completeness": "FG7-80: incomplete, five sibling GitLab door texts in the same command remain (B1). FG7-76: t-1402 B1 and F3 fixed; exchange shape, publish unit, differing middle, unequal lengths and dedent window verified by pure calls",
  "trail": {
    "read": [
      "tools/test_quarantine.py diff 4f22cb77..c1f33f65 and :59-70, :152-154, :450-581, :625-746, :1155-1238, :1375-1383",
      "tools/test_test_quarantine.py :21-27, :98-157, :290-345, :361-525, :1336-1346",
      "tools/session_context.py :202, :697-707; tools/ci_read.py :14-20; .github/workflows/canon.yml :8-31",
      "driver_golden.py diff 350c9868..f0f499ef; driver_trace.py :680-738; event_store.py :180-198; driver_runner.py :455-469; story_progress.py :489-490; driver_dispatch.py :2326-2334",
      "t-1402 review :13-60; t-1397 report; t-1404 report; dispatch d-fg780.txt"
    ],
    "reruns": [
      {"command": "python -B -m pytest <FG7-80 wt>/tools/test_test_quarantine.py -q -k 'schedule or enter or status'", "result": "84 passed, 190 deselected in 48.11s"},
      {"command": "python -B scratchpad/p780.py <FG7-80 wt>/tools", "result": "ci_class github->GithubCI, gitlab/None/other->GitlabCI; placeholders single-pass, no leftover %s, ASCII"},
      {"command": "python -B -m pytest scratchpad/test_p780_probe.py -q -s", "result": "2 passed; under ci=github the refusals print 'run a web pipeline with TEST_REDUNDANCY=1 REDUNDANCY_SCOPE=keep' and '... pipeline on the current HEAD' (B1 proof)"},
      {"command": "python -B scratchpad/p776.py", "result": "14 is_the_swap rows and 3 window rows as expected, BAD ROWS: 0"},
      {"command": "python -B scratchpad/p776b.py", "result": "read-only pure mutation on live driver_dispatch.py: the same two-line exchange at :2331/:2334"}
    ]
  }
}
```
