# FG7-27 - one road wired: the baseline, the hook and CI step, the verdict list (draft card)

task: t-1421 | node: forge/7/FG7-27 | feature: F19 | designer draft 18.11.2026 | status: DRAFT, forks open (§7)
Row: `plans/piles/forge/batch-7-vhodyashchie-4.md:52`; finding `plans/piles/forge/findings/20261112-verdikty-kritika-bez-one-road-i-kodovyj-sloj-ne-podklyuchen.md`
(calibration 12.11 item 10; P31). Siblings in the row: FG7-21 (`calibration_counts.py`) - accepted a48dc25 (t-434), so no conflict left.

## 0. Target on main, measured (file:symbol)

What exists: `tools/language_sites.py` is the whole tool; `main` has `--check/--raises/--totals/--shrink/--predicates/--init` plus
`--staged/--base/--rev/--repo`; exits 0 pass, 1 red, 2 cannot judge (`CannotJudge`, AR-28). `run_check --staged` reads the index
against HEAD and exits 0 before any parse when no package script, baseline or token data file is staged (`_staged_relevant`);
`_missing_baseline`: exit 2 (W3) package without baseline, exit 1 (W4) baseline deleted; `load_doc`: bad JSON or shape (C4) exit 2;
`_live_compare`: C1 new/grown site, C2 row above the code (exit 1), at most `MAX_SHOWN = 25` lines then "... and N more"; `run_init`
refuses when the file exists and writes every live site as `road`/`M8`/since `t-2065`. `tools/test_language_sites.py` exists (16
`--staged` hits; own trees under tmp_path).

What is NOT wired:
- The baseline `tools/language-sites-baseline.json` is absent. Glob `tools/language*` finds only `language_sites.py`.
- The `language_sites.py` docstring (lines 5-6) still says "INERT until wired (node N3): no hook, no CI line calls it".
- `.github/workflows/forge-check.yml` has no language_sites step. In the same Grep call, `language_sites|lint_ratchet` hit only line 68
  (`lint_ratchet`).
- `.githooks/pre-commit` has no language_sites line. Grep found nothing; the positive control `python|tools/` in the same file has 12 hits.
- `tools/calibration_counts.py` reads no `docs/tasks/specs/reviews/` and no `ONE ROAD`. In one Grep call over the file, the pattern
  `^def |...|ONE ROAD|reviews` matched only def/constant lines.
- `tools/mechanism_gate.py::MECHANISM_PREFIXES` does not list `language_sites.py`. Grep `language_sites` over tools/ finds only
  `test_streams.py` and `test_language_sites.py`.
- `tools/test_streams.py::KEPT` holds the row "inert until node N3 ... REMOVE this row at N3". The S3 positive control there asserts
  `not in_chain("tools/language_sites.py")` (:305).

Defects in reach:
- `language_sites.py::REFUSAL_TAIL` says "docs/SIBLING_MAP.md axis 33". The one-road axis is 34 (`docs/SIBLING_MAP.md:591`; axis 33 is
  dispatch identity, :581). The text is pinned at `test_language_sites.py:315`.
- `.claude/agents/critic.md:270-271` (Q12) says to read "the `--raises --base <merge base>` output attached by the mechanical layer".
  No tool attaches it (the tools/ Grep above). That is a producer with no owner (§7 F4).
- critic.md Q12 never asks for a `ONE ROAD:` line. Only VARIETY has "its own verdict line `VARIETY:`" (critic.md:254). Yet
  `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md:1136` 42(b) demands "every critic verdict ... carries a `ONE ROAD:` line" (§7 F3).
- Measured: the literal `ONE ROAD:` stands in 71 files of `docs/tasks/specs/reviews/` (Grep count, case-sensitive). The glob there has
  345 `.md` files.

What remains (this node): create the baseline; wire `--check --staged` into pre-commit and `--check --base "$BASE"` into forge-check;
put the tool into the mechanism net; fix the axis text; add a calibration list of verdicts without `ONE ROAD:`.

## 1. Architecture

No staged path is under `ai-packages/qa-factory/`, so `tools/architecture_gate.py` stays silent and no `architecture:`/`judgment:`
line is owed. Commits that touch mechanism paths (`docs/SIBLING_MAP.md`, `.githooks/`, `tools/mechanism_gate.py`, `PROCESS/`,
`.claude/agents/`) carry axis lines in the form `tools/mechanism_gate.py` reads. That file is the only carrier of the grammar; it is
not copied here. The AR lines below are the invariants the change keeps (named because the finding cites them):

- AR-15 (one survivor, wired everywhere): wire the existing `language_sites.py`; no second detector. Change check: the only new
  callers are the hook line and the CI step, and both run the same `main`. The calibration list does not re-scan code.
- AR-20 (shrink-only; a raise is named): the baseline joins axis 18. A row added or raised is named in the merge verdict (critic Q9/Q12).
  `--shrink` is the only automatic writer after `--init`. Change check: SIBLING_MAP axis 18 members list the file; the card adds no
  `--update`.
- AR-28 (an unknown never becomes a pass): exit 2 stops the commit in the hook (`gate` exits with the tool's own code) and fails the
  CI step. Change check: edges E3, E4, E5 and E9 below; no `|| true` and no `--warn` on either wire.
- AR-29 (code judges data): each check that is added or altered, with its owner and census class:
  - the hook and CI wire of `language_sites --check` - owner: data (live AST sites joined to baseline rows); class `xref`. It is a
    forge tool, so it is outside `judgment-census.json`, whose scope is package `scripts/*.py`. Whether a road is legitimate stays the
    critic's call, accepted by the Lead (the tool docstring, lines 31-33).
  - the calibration list of verdicts without `ONE ROAD:` - owner: data (presence of a literal); class `shape`. It is advice: exit
    stays 0, it never refuses. Whether a file is a verdict on a plan or diff, and whether its line says enough, is judgment, owned by
    the Lead at calibration.
  - the C3b owner's word (presence of a quote in its carrier) - owner: intent. This spec does not alter it.
- Error direction (designer rule 1, a function in a new, gate role): `language_sites` moves from advice-by-hand to a gate. It errs
  toward OVER-reporting (docstring lines 31-33): a false stop costs one row or a data row. These adversarial inputs must stay refused:
  - a new site in a staged script (C1);
  - a raised row with no new word (C3, CI only);
  - a deleted baseline (W4);
  - an unparsable script (C7);
  - a token file grown in the same commit (the staged mode widens to the whole scan, `_count_paths`);
  - a malformed baseline (C4, exit 2).
  The 14 KNOWN MISSES of the docstring stay the critic's.
  The calibration list errs the same way. These must stay listed: `one road:` in lower case, `**ONE ROAD**:`, `ONE ROAD` with no colon,
  a non-UTF-8 file, an empty file, an uncommitted file. Known miss, by the literal rule of the finding: a prose mention of
  "`ONE ROAD:`" counts as carried.

variety: none -- forge tooling only; no package file changes. The gate guards the existing holding of axes 1 and 3 (data rows, AR-1)
and changes no table, key or role step.

## 2. Design

D1 - the baseline. `python -B tools/language_sites.py --init --repo <worktree>` writes `tools/language-sites-baseline.json` (the only
writer; rows `M8`/`road`/`t-2065`, "grandfathered, not approved"). It is committed alone in its own commit. Who runs it and how
interleaved package commits are met: §7 F2.

D2 - the CI step. In `.github/workflows/forge-check.yml`, job `forge-check`, add one step right after
`run: python tools/dup_ratchet.py --check`:
`- name: one road (language sites)` / `env: BASE: ${{ steps.base.outputs.base }}` / `run: python tools/language_sites.py --check --base "$BASE"`.
POSITIONAL invariant: the step runs after `base` (it needs `$BASE`) and before `python -m pytest tools/ -q`, so a red ratchet shows
before the long suite. The order lint < dup < pytest that `test_workflows.py::test_the_dup_gate_is_in_forge_check...` pins stays true.
A person-supplied value reaches the shell only through `env:` (the pin in the workflow header). `tools/test_workflows.py::FORGE_CHECK_RUNS`
gains the row `'python tools/language_sites.py --check --base "$BASE"'` at the same index. Its comment names FG7-27, because there is
no `.gitlab-ci.yml` mirror (precedent: the P1-v N8 rows).

D3 - the hook line. In `.githooks/pre-commit`, after `gate python tools/agents_md.py --check` and before the forge_metrics WARN block:
a 3-line comment (one road, P31, FG7-27: silent unless a package script, the baseline or a token data file is staged; exit 2 stops
the commit like a red), then `gate python tools/language_sites.py --check --staged`.
POSITIONAL invariant: the existing gates keep their order (the output policy at :8). The hook exit stays the FIRST failing gate's own
code. The non-blocking forge_metrics block stays last, so no refusal comes after a path that never exits. On success the tool's
`ok (...)` line and its stderr timing go to `$tmp` and are not shown: neither carries `WARN`, by the strings in `run_check`.

D4 - the mechanism net. `tools/mechanism_gate.py::MECHANISM_PREFIXES` gains `"tools/language_sites.py",  # .githooks/pre-commit
(one-road ratchet, FG7-27)`. With F6 (a) it also gains `"tools/language-sites-baseline.json",  # DATA that decides what
language_sites.py refuses: a row added or raised lets a language branch pass`. `gitcmd.py`, its only tools import, is already listed.
`tools/test_streams.py`:
- `KEPT` becomes `{}`; the dict and its comment stay for a future copy;
- the S3 positive control asserts `in_chain("tools/language_sites.py")`;
- the `"language_sites.py" in KEPT` line is removed.
The negative control (`test_s3_negative_control...`) still proves that the census tells a non-link apart.

D5 - texts in reach:
- `language_sites.py` docstring lines 5-6 become "Wired (FG7-27): .githooks/pre-commit runs `--check --staged`; forge-check runs
  `--check --base $BASE`."
- `REFUSAL_TAIL` "axis 33" becomes "axis 34", and the pin at `test_language_sites.py:315` changes the same way.
- `docs/SIBLING_MAP.md`:
  - :598 "The code layer (planned) ... INERT" becomes "The code layer: wired (FG7-27) in pre-commit and forge-check; the baseline is
    the live count, a member of axis 18";
  - :602 the detector names the hook and the CI step beside check 42;
  - axis 18 "The members" (:400) gains `tools/language-sites-baseline.json` (one-road sites: a row added needs the owner's word or a
    reason, C3).

D6 - the calibration list (`tools/calibration_counts.py`). A new function `verdicts_without_one_road(root, start, end)` returns
`{"dir", "since", "listed": [{"path", "added"}], "problem"}`:
- Files: `sorted((root / "docs/tasks/specs/reviews").glob("*.md"))`, top level only (the finding's glob).
- Carried: the file BYTES contain `b"ONE ROAD:"` (case-sensitive literal, the finding §3). Nothing is decoded, so an encoding cannot
  raise.
- Date: the committer date of the file's FIRST add, from ONE call:
  `git -C <root> log --no-renames --diff-filter=A --name-only --date=format:%Y-%m-%dT%H:%M:%S --format=<sep>%cd -- docs/tasks/specs/reviews`.
  Keep the oldest date per path. This is the finding's "date of the first commit, not the merge date".
- Window: listed when `max(start, ONE_ROAD_SINCE) <= added < end` (start and end are the existing `--window-start/--window-end`;
  `ONE_ROAD_SINCE` per §7 F1). Aware window values have their tzinfo dropped before comparing (wall clock, as journal `ts`).
- Printed only in the DEFAULT mode (no `--journal`), after the reports and the SUMMARY, as a section titled "Critic verdicts without
  a `ONE ROAD:` line (candidates; the Lead judges)". It goes through the existing `_list_section`, one line per file:
  `<rel path> (added <date>)`.
- JSON (default mode): a top-level key `one_road_verdicts` beside `journals`.
- `--journal` mode, text and JSON: byte-identical to today, and no git call.
- Exit codes do not change.

D7 - the Lead's stream L (only if F3/F4 are taken as recommended): text edits by the Lead to `.claude/agents/critic.md` Q12 and
`PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md` 42(b).

## 3. Edges, each with its invariant

- E1 TEMPORAL, the baseline absent (today) vs present (after D1). Absent: `--check` exits 2 (W3); `--totals` says "cannot judge"
  (protocol 42(d): "code layer not wired", not a zero). Present: judged. The move that creates it is the D1 commit. Neither wire
  goes live before the baseline is on the same tree: the Lead places D2+D3+D4 in the wave merge that carries D1, or after it.
  Invariant: a tree with the package and no baseline is never a pass.
- E2 TEMPORAL, live worktrees at placement. If `core.hooksPath` points at the main checkout's `.githooks` (wiring_check B-470 accepts
  that form; which form this machine uses is an estimate, and the Lead runs `git config --get core.hooksPath`), a worktree whose base
  predates D1 gets exit 2 W3 "merge the branch that has it" on its next package commit. With a relative `.githooks`, its own old hook
  runs unwired until it merges main. Invariant: no commit with a package script is judged against a missing baseline as green. Merging
  main is the door (the tool says so). Placement timing: §7 F5.
- E3 A new site over the baseline. Pre-commit: C1, exit 1, refusal with the three doors (REFUSAL_TAIL). CI: C1 on the whole tree.
  At most 25 sites are shown, then "... and N more". Invariant: a new language branch never lands without a row, a data row or a
  removed site.
- E4 A site removed below the baseline (ratchet down). The staged mode judges the rows of the staged scripts' paths; CI judges every
  row. C2, exit 1, door `--shrink` in the same commit. Invariant: a row never outlives its site; a stale count would let a later
  re-added road pass unseen. It is never shrunk silently.
- E5 An unreadable baseline: invalid JSON, bad shape (C4), or a blob git cannot give (W5). Exit 2 in both wires. The door is to fix
  or restore the file (a byte copy from HEAD). Invariant: an unreadable ratchet is never a pass.
- E6 The baseline deleted in a commit: W4, exit 1, "deleting a ratchet is a Lead act". Invariant: the ratchet cannot be removed by an
  ordinary commit.
- E7 Pre-commit run time. With no relevant staged path the cost is one `git diff --cached` (silent exit 0). With a package script
  staged, the cost is bounded by the whole-scan time. The whole scan runs when the base or token union changes (`_count_paths`).
  No number is measured (estimate). The builder reports the whole-scan wall time from `--init` and from `--check` (stderr
  `scanned N files in X s`). The time is never pinned in a test (FR-31). The threshold for placing the hook is §7 F5. Invariant: the
  hook never skips the scan to save time; a slow wire is moved to CI-only by the Lead, never made silent.
- E8 CI base. `$BASE` comes from the existing ladder. When the base does not resolve (a force-push "before" sha that is gone), exit 2
  and the step is red, the same as `journal_validator --base "$BASE"` today. When the base holds no baseline, the effective base is the
  first commit that adds it (F13 in `pick_base`), or the note "created here". Invariant: C3/C5 never narrow to HEAD~1 silently.
- E9 The wire's tool is missing or crashes (python error, exit 1 or 2): the hook stops the commit and the CI step is red. Invariant:
  a gate that cannot run is not a pass. There is no `|| true`.
- E10 A verdict file without the `ONE ROAD:` literal, dated in the window: listed. `one road:`, `**ONE ROAD**:`, `ONE ROAD` without a
  colon, an empty file or a non-UTF-8 file: listed (the literal rule). Invariant: a verdict without the line is never silently
  counted as carrying it. Over-reporting is struck by the Lead (AR-29).
- E11 An uncommitted verdict file (no add commit): listed with `added uncommitted`, but only when `--window-end` is not given (it is
  newer than any past end). An unreadable file (OSError) is listed with `(unreadable: <first line>)`. Invariant: a file the tool could
  not date or read is a candidate, never dropped.
- E12 No reviews directory under the root: the section prints `(no verdict directory at docs/tasks/specs/reviews)` and makes no git
  call. Git fails, or the root is not a repository: `cannot judge: git log failed (<first stderr line>)`. Exit stays 0 (a measurement
  tool, docstring :20). Invariant: an unknown is a line of the report, never `(none)` (AR-28, FR-41).
- E13 Window bounds: a file added before `max(start, ONE_ROAD_SINCE)` is not listed. Files added at or after `--window-end` are not
  listed. A rename counts as an add at the new path (`--no-renames`), so it is listed when the rename falls in the window.
  Invariant: a verdict written before the rule existed is never a finding; doubt resolves toward listing.
- E14 The `--journal` mode is unchanged byte for byte and makes no git or tree read. Invariant: the explicit mode reads only the files
  it is given (existing tests `test_k14_an_explicit_journal_still_reads_just_that_file`, `test_d3_json_prints_the_reports_only...`).
- E15 The packet patch (Card A) no longer applies because main moved in one of its paths: `git apply --check` fails, and the Lead
  returns it as a fix round. Invariant: a hunk is never hand-merged at placement unseen by the critic.

## 4. Builder cards

### Card A - the wire (baseline, texts, placement packet)

given: C:/QAFactory/forge-repo/docs/tasks/specs/20261118-fg7-27-language-sites-one-road-card.md §0-§3, §5; tools/language_sites.py::run_init, ::run_check, ::REFUSAL_TAIL; tools/test_language_sites.py::test_r_the_refusal_holds_the_three_doors_path_qualname_token; tools/test_streams.py::KEPT, ::test_s3_positive_control_the_real_census_sees_the_helper_and_a_chain_link; tools/test_workflows.py::FORGE_CHECK_RUNS; tools/mechanism_gate.py::MECHANISM_PREFIXES; .githooks/pre-commit; .github/workflows/forge-check.yml; docs/SIBLING_MAP.md:400, :598, :602
owns:
C:/QAFactory/forge-repo/tools/language-sites-baseline.json
C:/QAFactory/forge-repo/tools/language_sites.py
C:/QAFactory/forge-repo/tools/test_language_sites.py
C:/QAFactory/forge-repo/docs/SIBLING_MAP.md
C:/QAFactory/forge-repo/docs/tasks/handoffs/t-<task>-fg7-27-wire.patch
non-goals: no edit that stays on the live paths of `.githooks/pre-commit`, `.github/workflows/forge-check.yml` or `tools/mechanism_gate.py` (enforcement files: they travel in the patch and the Lead places them); no edit to `tools/test_streams.py` or `tools/test_workflows.py` outside the patch; no hand row in the baseline, no relabel of `M8` rows; no change to the scanning logic of `language_sites.py`
handoff: report + the patch path; the commit sha of the baseline commit and of the text commit
edges: E1, E2, E3, E5, E7, E9, E15 of §3 (the spec); `--init` refusing on a script that does not parse (C7): stop and return a question with the file named, write nothing
DoD: `python -m pytest "tools/test_language_sites.py::test_r_the_refusal_holds_the_three_doors_path_qualname_token" -q`, then under the probe below `python -m pytest "tools/test_streams.py::test_s3_positive_control_the_real_census_sees_the_helper_and_a_chain_link" "tools/test_streams.py::test_s3_no_tool_outside_the_chain_carries_its_own_stream_reconfigure" "tools/test_workflows.py::test_forge_check_steps_equal_the_ordered_list_and_there_is_no_scrub_anywhere" "tools/test_workflows.py::test_the_dup_gate_is_in_forge_check_and_the_report_is_in_package_full_and_never_flips_the_verdict" "tools/test_mechanism_gate.py::test_every_githooks_script_reference_is_covered_by_mechanism_prefixes" "tools/test_mechanism_gate.py::test_transitive_import_closure_of_live_wiring_is_covered_by_mechanism_prefixes" -q`; `python -B tools/language_sites.py --totals`; `python -B tools/language_sites.py --check --base origin/main`
siblings: FG7-26 (`tools/ratchet-files.json`, absent today: whoever lands second adds the baseline row, §7 F9); FG7-15 (one road for paths outside the package, its own files); the ratchet steps `lint_ratchet`/`dup_ratchet` in forge-check (pattern only, unchanged); calibration_counts readers: Card B
designer: C:/QAFactory/forge-repo/docs/tasks/specs/20261118-fg7-27-language-sites-one-road-card.md

Work, in order:
1. Commit 1, the baseline alone. Run `python -B tools/language_sites.py --init --repo <worktree>`. Then run `--totals`, which must
   print `rows N, ...` and not "cannot judge", and `--check --base origin/main`, which must exit 0. Report the stderr wall time of
   each, N rows, and the files scanned. Commit lines: axis lines only if F6 (a) puts the file in the net.
2. Commit 2, the texts: D5 in `language_sites.py` (docstring lines 5-6, REFUSAL_TAIL axis 34), the pin at
   `test_language_sites.py:315`, and the three SIBLING_MAP rows. Axis lines per `tools/mechanism_gate.py`: axis 34, and axis 18 for
   the member row.
3. The packet, as a probe (CLAUDE.md hygiene 7):
   - take byte copies of `.githooks/pre-commit`, `.github/workflows/forge-check.yml`, `tools/mechanism_gate.py`,
     `tools/test_streams.py` and `tools/test_workflows.py` FIRST;
   - edit them per D2, D3 and D4 (D4's baseline row only with F6 (a)) and run the DoD's second command, with NO commit in between;
   - write `git diff -- <the five paths>` to the patch path;
   - restore all five FROM the byte copies and report the hash comparison (restored = HEAD).
   - Commit 3 holds the patch alone.

test lines (strongest first):
- test: tools/test_workflows.py::FORGE_CHECK_RUNS, a new row `'python tools/language_sites.py --check --base "$BASE"'` right after the dup_ratchet row (in the patch) | expected from: §2 D2 of this spec
- test: tools/test_streams.py::test_s3_positive_control_the_real_census_sees_the_helper_and_a_chain_link, edited per D4 (in the patch) | expected from: the KEPT row's own text "REMOVE this row at N3" + §2 D4
- test: tools/test_language_sites.py::test_r_the_refusal_holds_the_three_doors_path_qualname_token, the part `docs/SIBLING_MAP.md axis 34` | expected from: docs/SIBLING_MAP.md:591 (the axis 34 heading)
- test: none -- the hook line is an enforcement file; the behaviour it reaches (`--check --staged` on a new site, exit 1) is already in test_language_sites.py; the wire is witnessed by the Lead's placement probe (§4 Lead placement) | expected from: CLAUDE.md enforcement-file rule
- test: none -- the baseline is data written by `--init`; its witness is `--totals` plus `--check` exit 0 | expected from: §2 D1

Lead placement (after acceptance, in the wave merge that carries commits 1-3):
- `git apply --check` the patch, then apply it;
- re-run the DoD's second command;
- placement probe: in a scratch worktree of the merged tree, stage a package script with one added `endswith(".ts")` and run the
  hook. It must exit 1 with C1. Then unstage it and confirm `gates: ok (N checks)`;
- commit with axis lines per `tools/mechanism_gate.py`;
- delete the patch in the same commit, or keep it as a record (Lead's choice; the patch is not a test).

### Card B - the verdict list in calibration

given: C:/QAFactory/forge-repo/docs/tasks/specs/20261118-fg7-27-language-sites-one-road-card.md §1, §2 D6, §3 E10-E14; tools/calibration_counts.py::main, ::_list_section, ::_fmt_section, ::parse_ts, ::_default_reports; tools/test_calibration_counts.py::_run_main
owns:
C:/QAFactory/forge-repo/tools/calibration_counts.py
C:/QAFactory/forge-repo/tools/test_calibration_counts.py
non-goals: no change to `render_text`, to the per-journal report dict or to any existing section; no output change in `--journal` mode; no import beyond the standard library (the script runs alone, `test_streams.py::GUARDED`); no judgment of a line's content; no edit to critic.md or the protocol (stream L)
handoff: report with the witness tail and the commit sha
edges: E10, E11, E12, E13, E14 of §3; `ONE_ROAD_SINCE` per the Lead's answer to F1 (until answered: return the question, do not pick)
DoD: `python -m pytest tools/test_calibration_counts.py -q`
siblings: FG7-21 (same file, accepted a48dc25: the skip table stays as is); Card A (disjoint files)
designer: C:/QAFactory/forge-repo/docs/tasks/specs/20261118-fg7-27-language-sites-one-road-card.md

The git call uses `subprocess.run` with a list of arguments, no shell, and `timeout=60`. A timeout gives the E12 line. The section
is computed only after the reports load, so every early exit 2 stays as it is (`test_journal_fresh_clone.py` J5).

test lines (strongest first):
- test: tools/test_calibration_counts.py, a new parametrized table `test_fg7_27_one_road_cases` over ONE module-scoped git repo built
  once. Commits are dated by `GIT_COMMITTER_DATE`. Rows:
  - in the window, without the literal -> listed;
  - with `ONE ROAD:` -> not listed;
  - added before the floor -> not listed;
  - lower case `one road:`, `**ONE ROAD**:` and non-UTF-8 bytes -> each listed;
  - uncommitted with no `--window-end` -> listed as `added uncommitted`;
  - added at or after `--window-end` -> not listed.
  | expected from: §2 D6, §3 E10, E11, E13; finding §3 item 3
- test: the same file, one CLI row in default mode with `--root`. The text prints the section title and the listed path, and the JSON
  carries `one_road_verdicts`. A root with no reviews directory prints `(no verdict directory at ...)`, and a non-repository root with
  the directory prints `cannot judge: git log failed`. Exit is 0 in every case | expected from: §3 E12, §2 D6

## 5. Readers of every touched file

The `python -B tools/owns_readers.py` block was NOT attached (`facts: none`). The Lead runs
`python -B tools/owns_readers.py --paths tools/language-sites-baseline.json tools/language_sites.py tools/test_language_sites.py tools/mechanism_gate.py tools/test_streams.py tools/test_workflows.py .githooks/pre-commit .github/workflows/forge-check.yml docs/SIBLING_MAP.md tools/calibration_counts.py tools/test_calibration_counts.py --names MECHANISM_PREFIXES KEPT FORGE_CHECK_RUNS REFUSAL_TAIL verdicts_without_one_road ONE_ROAD_SINCE`.
Until then, the hand greps below stand (Grep tool, the counts are its output):

- `tools/language-sites-baseline.json` (new). Grep `language_sites|language-sites-baseline` over tools/ gives 2 files besides the tool.
  - `tools/language_sites.py` (`BASELINE_REL`, all modes): unchanged code.
  - `tools/test_language_sites.py` (builds its own trees): unchanged.
  - `.claude/agents/critic.md:270-271` (reads its row): unchanged text; stream L if F4.
  - `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md:1136` 42(d): unchanged text; `--totals` now prints numbers.
  - `docs/SIBLING_MAP.md` :400/:598: change in Card A. Calibration check 12 (map liveness): the named path exists after the merge.
  - `tools/mechanism_gate.py`: changes in the Card A patch, if F6 (a).
  - FG7-26 `tools/ratchet-files.json`: absent today (Glob) - sibling, F9.
  - `.githooks/`: 0 hits (control: `gate python` hits in pre-commit).
- `tools/language_sites.py`:
  - `tools/test_language_sites.py` (imports it; the pin at :315): changes in Card A.
  - `tools/test_streams.py` :247, :302-306: changes in the Card A patch.
  - `tools/mechanism_gate.py::MECHANISM_PREFIXES`: patch.
  - `tools/enforcement_probe.py` (its chain is `.githooks/*` plus every tools/*.py the hook names, :41): unchanged code. After
    placement it covers language_sites.py, so a commit touching it runs wiring_check.
  - `tools/test_mechanism_gate.py` :942, :1041, :1673 (parse the live hook and need its scripts in the net): unchanged, green after
    the patch.
  - `tools/test_streams.py::GUARDED`: not concerned.
- `tools/test_language_sites.py`: read only by pytest. Unchanged.
- `tools/mechanism_gate.py` (`MECHANISM_PREFIXES`). Grep `MECHANISM_PREFIXES|mechanism_paths` over tools/ gives 9 files, 52 hits.
  - mechanism_gate itself (commit-msg): later commits on language_sites.py (and on the baseline with F6) need axis lines. That
    changes the cost, by intent.
  - `test_mechanism_gate.py`, `test_mechanism_gate_md.py`: unchanged.
  - `test_streams.py` (`in_chain`): patch.
  - `test_worktree_sweep.py:1187-1192` (asserts its own refs are in the net; negative control `tools/not_in_the_net.py`): unchanged.
  - mentions only, unchanged: `handoff_gate.py:42`, `gitcmd.py:10`, `streams.py`, `worktree_sweep.py`.
  - `install_parity_anchors.json:526` (kind `path`, no anchors): unchanged.
- `.githooks/pre-commit`. Grep `githooks/pre-commit|"pre-commit"` over tools/ gives 9 files, 35 hits.
  - `test_mechanism_gate.py` (as above): green after the patch.
  - `enforcement_probe.py` (as above): unchanged.
  - `test_enforcement_probe.py` (synthetic repos): unchanged.
  - `wiring_check.py:228` (presence and tracking): unchanged.
  - `session_context.py:1485` and `test_session_context.py:2043` (hook names): unchanged.
  - `test_wave.py:309`, `:635` (their own `.git/hooks`): unchanged.
  - `agents_md.py`: not a source (Grep `githooks` hits only the help text, :267). Unchanged.
  - The `gates: ok (N checks)` count: no pin. Grep `gates: ok` over tools/ gives 0; the same tool and mode hit `pre-commit` in tools/.
- `.github/workflows/forge-check.yml`. Grep `forge-check\.yml` over tools/ gives 2 files.
  - `test_workflows.py` (`FORGE_CHECK_RUNS`, the dup order, env-only values, `canon.yml` calling it, :483): patch.
  - `test_test_quarantine.py:1867`, `:1887` (a run name in fixtures): unchanged.
  - `canon.yml` (calls the workflow): unchanged; the canon gets the step too, with the merge-base as its base.
- `docs/SIBLING_MAP.md`. Grep `SIBLING_MAP` over non-test tools gives 18 files, 33 hits.
  - `mechanism_gate.py` (reads the axis HEADINGS and labels): rows only change, no heading changes, so unchanged.
  - the others are mentions: unchanged.
  - `install_parity_anchors.json:533` (kind `path`): unchanged.
- `tools/calibration_counts.py`. Grep `calibration_counts` over tools/ gives 8 files, 36 hits.
  - `test_calibration_counts.py`: Card B.
  - `test_streams.py::GUARDED` (copied alone, `--help` must work): unchanged; the standard library only keeps it green.
  - `test_journal_fresh_clone.py` J5 (exit 2 without a journal): unchanged; the section comes after the load.
  - `test_journal_per_developer.py` (fixture builders): unchanged.
  - `journal_validator.py`, `journal_keys.py`: mentions, unchanged.
  - `install_parity_anchors.json:603` (kind `path`, kit copy `toolkit/tools/calibration_counts.py`; a content compare is an estimate,
    not verified): unchanged.
  - `.github/`: 0 hits (control: `lint_ratchet` hits forge-check.yml:68).
- `tools/test_calibration_counts.py`: read by pytest and `test_journal_per_developer.py:12` (a mention). Unchanged.

## 6. Test cost (docs/TESTING.md)

- No new test file (Budget / Files): every case is a row in an existing forge test file; forge tests have no `keep` row
  (TESTING.md:236); none is canon-only (`canon_only` = package globs) or in `slow_tests.json` (Grep 0; control `"files"` hits).
- Card A: +1 list row, KEPT emptied + one assertion flipped, 1 string - under its code/text lines. Card B: one table on one repo
  built once + one CLI test; the builder stops at budget (Budget / Volume) and names what it did not write.
- Card A runs 1 + 6 node ids, no whole file; Card B one whole file, its own. `pytest tools/` runs on CI.

## 7. Forks (returned, not decided)

- F1 The floor of the verdict list. t-2065 is an experiment-line id, and ids do not compare across clones (B-402).
  - (a) A constant `ONE_ROAD_SINCE`, the day Q12 landed on this main. Estimate: 2026-11-11T00:00:00, from p4 "came in with 5498318 on
    2026-11-11". The Lead measures it with `git log --diff-filter=A --format=%cI -S"ONE ROAD" -- .claude/agents/critic.md`.
  - (b) No floor: the window flags only; without a window the whole history is listed.
  - (c) Compute the floor at run time with git pickaxe.
  Recommend (a): one named constant with its carrier comment, effective start = max(window start, floor).
- F2 Who makes the baseline, and what happens when package commits land between `--init` and the merge.
  - (a) The builder runs `--init` in its worktree. At the wave merge the integrator runs `--check --base origin/main` on the merged
    tree. A red C1 or C2 from interleaved commits leads to re-running `--init` in the merge (remove the file, `--init`), before the
    push. That is legal while main holds no baseline. Rows are never hand-added.
  - (b) The Lead runs `--init` on main as its own commit at acceptance; the builder ships no baseline.
  Recommend (a): the producer stays a node with owns (designer rule 6).
- F3 The producer of the `ONE ROAD:` line. critic.md Q12 has no line form, so the list measures a form the critic is not asked to
  write.
  - (a) Stream L: the Lead adds "on its own verdict line `ONE ROAD:`" to Q12 (the VARIETY form) and names the Card B section in
    protocol 42(b).
  - (b) Card B also matches looser forms. That is safe only if they over-report, and they would hide nothing new.
  Recommend (a). Until then the list over-reports by design.
- F4 critic.md:271 promises `--raises` output "attached by the mechanical layer"; nothing attaches it.
  - (a) Stream L: the Lead edits Q12 so that the critic runs `python -B tools/language_sites.py --raises --base <merge base>` itself.
  - (b) A new node attaches it through the critic dispatch tooling (`critic_snapshot.py`).
  Recommend (a): no new producer.
- F5 Placement conditions for the hook.
  - (a) The Lead places it if the builder's whole-scan wall time is at or under a threshold. The designer's estimate is 10 s, an
    estimate, not a measured norm. If over, the step stays CI-only and a finding is opened for a faster staged path. Before placing,
    the Lead lists live worktrees with package work whose base lacks the baseline (E2) and accepts their W3 refusals ("merge main").
  - (b) Place it unconditionally.
  Recommend (a).
- F6 The baseline in `MECHANISM_PREFIXES` as DATA (precedent: `tools/worktree-junk.json`, `tools/wait-reaper.json`), so every baseline
  edit carries axis lines.
  - (a) yes;
  - (b) no: the C3/C3b gate and the critic are enough.
  Recommend (a). The finding asks for an axes block on the creating commit.
- F7 How the enforcement edits travel. The brief makes the workflow an enforcement file. The designer adds `mechanism_gate.py` by
  CLAUDE.md (it runs on commit-msg; precedent: `handoff_gate.py:41-42` "the Lead ... adds it to MECHANISM_PREFIXES").
  - (a) One patch that also carries the two dependent test edits, so nothing is red on any branch and placement is atomic.
  - (b) The tests are committed in the branch, red until placement.
  - (c) Treat the workflow and mechanism_gate as non-self-activating for the builder (the workflow runs only after the Lead's push;
    the prefix only tightens) and edit them directly; only the hook goes in the patch.
  Recommend (a). (c) is cheaper, but it reverses the brief's line.
- F8 The finding prescribes extending `tools/test_wiring_check.py` so the line must stand on both paths.
  - (a) No such text pin (TESTING «Что не пишется»: a phrase-in-file pin). The workflow already has its ordered-list pin; the hook
    is witnessed by the Lead's placement probe and by the closure tests that read the live hook.
  - (b) Add the pin as the finding says.
  Recommend (a).
- F9 FG7-26 creates `tools/ratchet-files.json` (absent today), and the baseline belongs in it as a ratchet file.
  - (a) Whoever lands second adds the row: if FG7-27 lands first, the FG7-26 card carries the row.
  - (b) This card waits for FG7-26.
  Recommend (a).

## 8. Small choices closed by the designer

- The literal match is on bytes, case-sensitive, anywhere in the file, as the finding's text has it ("без литерала `ONE ROAD:`").
- Dates are the committer date of the first add, `--no-renames`, naive local wall time (same as journal `ts`); aware window values
  have their tz dropped.
- One `git log` call for all files, not one per file. `subprocess.run` with a list, no shell, timeout 60 s. No `gitcmd` import (the
  script must run alone).
- The section runs in default mode only, after the SUMMARY; the JSON key is `one_road_verdicts`; `--journal` stays byte-identical.
- An uncommitted file is listed only with no `--window-end`.
- The `M8` rows from `--init` are kept. Relabelling them to census mechanisms M1-M7 is judgment and belongs to TR2-16.
- The CI step name is `one road (language sites)`. The FORGE_CHECK_RUNS comment names FG7-27 (no GitLab mirror).
- The hook comment is 3 lines in the style of the file's other gate comments.

## 9. Reading trail (all measured in this session with Read/Grep/Glob; no shell)

- The batch row: Read `batch-7-vhodyashchie-4.md:52` (owns, siblings) and :46 (FG7-21 accepted a48dc25).
- The finding: Read whole.
- `language_sites.py`: Read 1-137, 886-980, 1276-1456, 1500-1728; Grep of defs and constants.
- forge-check.yml: Read whole. pre-commit: Read whole.
- `test_workflows.py`: Read 135-214. `test_streams.py`: Read 225-313.
- `mechanism_gate.py`: Read 60-89, 240-297, 395-402. `test_mechanism_gate.py`: Read 935-1084, 1655-1683.
- `calibration_counts.py`: Read 1-81, 201-224, 773-831, 905-1041. `test_calibration_counts.py`: Grep of the test list; Read 1373-1378,
  1663-1673.
- `critic.md` 262-276, plus a Grep of `ONE ROAD:|VARIETY:` (only :254, VARIETY).
- Protocol :1136 (check 42). SIBLING_MAP: 396-400, 590-602, plus the axis 32-35 headings.
- `calibration-20261112-p4.md` 26, 203-210.
- TESTING.md: 1-110, 128-147, 211-258. `test-layers.json` 1-40. `slow_tests.json` Grep.
- architecture.md 33-72, 173-185; `ARCHITECTURE_INDEX.md` Grep; `architecture_gate.py` 1-38.
- `handoff_gate.py` 36-45. `install_parity_anchors.json` (Grep, 596-607). `agents_md.py` Grep. `dup_ratchet.py`/`lint_ratchet.py`
  Grep (scan roots: tools/*.py and package scripts; `docs/tasks/handoffs/` is not scanned, so the patch is safe).
- Counts: `ONE ROAD:` in reviews/ = 71 files (Grep count); reviews/*.md = 345 (Glob).
- Positive controls are named inline beside each negative claim (§0, §5).

Noticed, not in scope:
- `forge-check.yml:2-4` still says "STAGED COPY: lives in docs/migration/", which is stale: the file is live in `.github/workflows/`.
- Protocol 42 names `SIBLING_MAP.md:586` through p4 (the row is :598 now).

## 10. Lead decisions (18.11, Lead 501cb4e0, accepted)

- F1 (a) `ONE_ROAD_SINCE = "2026-11-17T13:51:09+01:00"`, measured: `git log --format="%h %cI" -S"ONE ROAD" -- .claude/agents/critic.md` -> the earliest commit 9616b6f4 2026-11-17T13:51:09+01:00 (the `--diff-filter=A` form finds nothing: the file existed before the words). The estimate 2026-11-11 is not used.
- F2 (a) the builder runs `--init`; the integrator re-runs it at the merge on a red C1/C2. F3 (a) and F4 (a): the Q12 text edits are a Lead stream L edit, after card B merges. F5 (a) place the hook only when the measured whole-scan wall time is at or under 10 s, else CI-only plus a finding. F6 (a) the baseline joins MECHANISM_PREFIXES as data (in the patch). F7 (a) one patch with the two dependent test edits. F8 (a) no wiring text pin. F9 (a) whoever lands second adds the ratchet-files row.
- `docs/SIBLING_MAP.md` is a mechanism path: in card A the builder STAGES it with commit 2's texts and the Lead commits it; the builder commits the baseline (commit 1), the language_sites texts and the patch file itself.
