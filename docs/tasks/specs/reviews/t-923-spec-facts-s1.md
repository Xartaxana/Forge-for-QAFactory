# t-923 (F19) — critic on the S1 diff of "Spec facts by code" (builder t-917, commit 8c9e53af)

Diff: `git -C .claude/worktrees/agent-a585c072bec1720f8 diff origin/main...HEAD` (6 files, +1174 −19). Spec: `docs/tasks/specs/20261116-spec-facts-by-code-spec.md`
§0-§2, §3.1, §5 T1/T2, §6 S1; F-11/F-12/F-13. Brief: `docs/tasks/critic-diff-brief.md`. Base at review time: origin/main 237ead44 (it moved
from the builder's 2b6b1577).

## Verdict

**NEEDS WORK (accept with fixes) — 2 findings block the merge (B1, B2), 9 fixes before merge (F1-F9).** The tool is sound in its core:
on three real cases plus five more it found every reader that its scope covers, and no reader it invented (key 1). The unknown forms
for base / grep / ls-tree / registries work as the spec says. Two holes remain against the stated intent ("an UNKNOWN must never read
as 'no readers'"): a header that says `0 outside owns` when nothing was searched (B1), and a class of executable readers outside the
scope with no KNOWN MISS that names them (B2). Acceptance is the Lead's call (critic.md rule 6).

## Blockers

**B1 — `owns_readers.py:577-580` (render header) with `:362-365`, `:380-383`, `:354-356`: a header count of ZERO when no owned path was
searched.** `<R>` is counted only over subjects that were actually grepped, but the header never says that some or all owned paths
were skipped. Measured in the worktree:
`--paths C:/QAFactory/forge-repo/tools/gitcmd.py` (a main-checkout path, run from the worktree) →
`readers: 0 outside owns, 1 lines below -- base origin/main 237ead44 (...)` + `- unsearched: gitcmd.py (outside the repo; ...)`;
`--paths tools/` → `readers: 0 outside owns ...` + `- unsearched: tools holds 229 files ...`; `--paths .` → the same with 5789 files.
gitcmd.py really has 32 outside readers (the same call with a repo-relative path). This is the false zero FR-59 / the dispatch's
intent forbids, and S2's note regex `^readers:[ \t]*(\d+ outside owns|unknown)` will take this line as a pass. The `unsearched`
line underneath does not undo a header that reads "0". Surface: "the header count when part of the input was not searched".
Neighbours walked: (a) every owned path outside the repo — false 0 (shown); (b) every owned directory over `dir_cap` — false 0
(shown); (c) every owned path holding a control character — the same code path (`bad`, :354), a false 0; (d) PATH_CAP overflow —
a partial count with no mark in the header; (e) `report([])` through the API (builder deviation 8) — `readers: 0 outside owns, 0 lines
below`, a header about nothing, which E-1 forbids. A mixed input (one path searched, one outside) gives a correct count for the
searched part and no partial mark in the header (shown: `--paths ../outside.py tools/gitcmd.py` → `readers: 32 outside owns`).
**Expected fix:** when no owned path subject was searched → `readers: unknown -- no owned path was searched (<k> unsearched below); <L>
lines below -- base ...`; when some were skipped → add a header segment `; unsearched: <k> paths` so the count reads as partial;
`report([])` gives the unknown form too. T1 rows: `outside-repo` and `dir-wide` assert the header form; one mixed row.

**B2 — `owns_readers.json` scope + docstring KNOWN MISS 5 (`owns_readers.py:30`): CI workflows read the tools, are not searched, and no
miss names them.** `.github/workflows/forge-check.yml` runs `python tools/piles.py check --base`, `tools/install_parity.py --check`,
`tools/lint_ratchet.py --check`, `tools/journal_validator.py --all`, … (`git grep -n tools/ origin/main -- .github/workflows/forge-check.yml`:
16 lines); canon.yml, nightly.yml, quarantine-watch.yml, scenario-clock.yml name tools too. Run on `--paths tools/mechanism_gate.py --all`:
`.githooks/commit-msg` is listed (good) and `.github/workflows/forge-check.yml` (independent grep finds it) is not. A builder who
changes a tool's CLI breaks CI with a block that never mentioned it. KNOWN MISS 5 says "readers outside the scope (docs, plans: prose
readers are the designer's own walk)" — it names prose, not executable YAML, so a reader of the docstring cannot learn this miss.
By key 1's rule this is a missed reader with no covering line. The spec's scope list has the same gap (a dispatcher spec defect,
noted for the Lead). **Expected fix:** add `.github/workflows/*` to the `code` row (over-report direction, as the spec's error direction
asks); rewrite KNOWN MISS 5 to list what the scope leaves out by name: `docs/`, `plans/`, root `*.md` (CLAUDE.md, PROJECT.md), nested
fixture JSON under `scripts/tests/fixtures/<dir>/` (52 files at 237ead44 name a `.py`; only the top level is in scope by the spec's
choice), the md/yaml fixtures under `tools/` (8 files name a `.py`), `gateway/`.

## Fixes before merge

- **F1 `dispatch_new.py:173-175, 180-182, 188`** — when headers pass and headers+block makes the checker RAISE (`_decide` returns a string)
  or gives a DEGRADED cut, the whole dispatch is refused (exit 2, nothing on stdout). That breaks §3.1's invariant "a failing helper
  never blocks or hides a dispatch". Expected: anything other than a clean pass on headers+block (an exception, a refusal, a
  degraded cut) goes to the step-4 replacement line and is decided once more. Only a failure of the replacement refuses.
- **F2 `dispatch_new.py:154`** — `_ids_refusal` runs on the headers only. §3.1 step 3 runs it on `text`. The handoff's deviation 1 names
  only `decide_full`. It is harmless today: I checked that `header_ids` is identical with and without a real block, and no block kind
  matches `_IDS_HEADER_RE` (`dispatch_manifest.py:751`). Expected: run it on the final text too (one call), or name it as a deviation.
- **F3 unknown quarantine registry (builder deviation 4), `owns_readers.py:495, 524, 530, 557`** — keeping these readers listed is the
  right direction (hiding them would under-report). But a listed layered test reader prints as plain `(test)` / `(test, slow)`, the
  `N test` count and the `hot` count include them, and the spec says "no reader is counted as non-quarantined". Measured at base
  `54983180~1` (before test-layers.json existed): `- outside: .../test_driver_layers.py (test, slow) names ...` with nothing that marks
  it as possibly quarantined. Also `? quarantined` is raised by NON-test readers under `scripts/tests/` (fixture JSON, helper code).
  Same run on `fixtures/driver-layers.json`: the only layered unknowns were 1 data + 1 code reader, and the more line still said
  `? quarantined`. Expected: listed lines `(test, quarantine unknown)`; the more part `N test (quarantine unknown)` in place of
  `N test, ? quarantined`; the `?` condition limited to `cls == "test"`.
- **F4 code quality, `owns_readers.py:339-469` `report()` (131 lines; 4 nesting levels at 376-386) and `:508-581` `render()` (74
  lines)** — both are over the brief's ~60-line bar. Expected: split `report()` into inputs / presence / layer status / names steps, and
  take the per-subject part of `render()` out into its own function.
- **F5 duplication, `owns_readers.py:164-167` `_first_line`** — a second copy of `gitcmd._first_line` (`gitcmd.py:63`, same
  semantics). `dispatch_new.py:135` and `:177` add two more inline first-line copies. That makes three implementations in one diff
  where one exists. Expected: one helper, imported (make gitcmd's helper public, or have dispatch_new import the tool's).
- **F6 docstring `owns_readers.py:52`** "Their convergence is a queued node". No such node exists at origin/main: case-insensitive
  `git grep -l owns_readers origin/main` → the spec, review t-904 and the journal only, and nothing under `plans/`. The positive control
  is the same call finding the spec. Expected: "node C6 of the spec (§6 L9), opened by the Lead". Better still, the Lead lands L9 in
  the same wave and the docstring names its node id.
- **F7 `test_dispatch_new.py:119-121`** — the docstring claims "the designer count read the same", but no assertion checks it. Expected:
  `assert dm.designer_threshold(cut_a) == dm.designer_threshold(cut_b)`. I ran it on a real printed dispatch: (3, 0) both ways.
- **F8 the outside-input battery (key 4), missing rows in `tools/test_owns_readers.py`:** caps AT the limit — `test_cap` 25 (no `hot`, 25
  listed, no `more`), `data_cap` 12, `dir_cap` 40, `names_cap` 20; `PATH_CAP` 200 has no row AT or BEYOND; a control character in a
  path and in a name (deviation 6 has no row); a regex-metacharacter name (`a.b*`, `[x]`); a Cyrillic name; a `..` relative path that
  leaves the repo; the mixed searched/unsearched row of B1. I ran each of these by hand and they behave safely today (trail). The rows
  pin that behaviour. `SHARD` 80 is internal (no row needed).
- **F9 listing order under `--all` with 2+ owned paths, `owns_readers.py:516-572`** — `merged["outside"]` keeps insertion order, so the
  test lines of subject 2 come after the code lines of subject 1. Measured: `--paths tools/gitcmd.py tools/streams.py --all` → lines
  15-32 code (gitcmd), 33+ tests (streams). §2.2 says test readers come first within a kind. Expected: sort the outside slots by (test
  before code, quarantined last, tier, path) before rendering.

## Keys

**1. EMPIRICS.** (a) dispatch_manifest.py + test_dispatch_manifest.py `--readers`: 20 outside (9 test, 10 code, 1 data). An
independent `git grep -l -i -F dispatch_manifest origin/main` with prose dirs removed gives exactly 21 files: the 20 plus the owned
test. `test_dispatch_manifest` is named by no other file. `--all` lists the same 10 code files. No miss, nothing invented. (b) story_run.py
`--names s0_criteria`: names lines test_conductor_doors / test_silent_passes / test_story_run_s0 (test, slow) + driver-layers.json
(data) + `1 code` (driver_s0.py). Independent `git grep -c -i s0_criteria`: exactly those five in scope, the rest docs/plans/changelog
(out of scope, KNOWN MISS 5). No miss. 253 outside agrees with my rough `-w` count of 255 over a wider pathspec. (c) Easy-to-miss readers:
`.githooks/commit-msg` for mechanism_gate.py — found. `.claude/settings.json` + `tools/warn_layers.json` + `tools/dup-baseline.json` for
journal_echo.py — found. The one difference from an independent grep (`tools/test_dod_track.py`) is `test_journal_echo_r3.py` in a
comment: it names another file, so not a reader (correct under `-w`). **`.github/workflows/forge-check.yml` for mechanism_gate.py and
piles.py — missed, no covering line → B2.**

**2. Deviations.** 1 (headers first) — accept; it saves a git search on refused dispatches, and the refusals are identical; see F2. 2
(several grep calls) — accept, the reason holds (one `-w` setting per call; `-o` longest match). 3 (`-o -z` with names for K) — accept.
**4 (unknown registry lists tests + `? quarantined`)** — the direction is right (over-report), but the form is not: F3. **5 (`--all`
suppresses `hot`)** — accept. Under `--all` the list is complete and the `hot` advice ("pass --names for a usable list") has nothing
left to do. No unknown is hidden, because the counts are all listed. 6 (control character → unsearched) — accept; untested (F8);
part of B1's header. 7 (`--paths -x.py` read by argparse) — accept; the API road is what dispatch_new uses. 8 (`report([])`) — **not
accepted**: B1(e). 9 (time) — the world IS built once per file (module fixture, `test_owns_readers.py:86`). The cost is ~7 git subprocesses
per `report()` (measured: 6 `gitcmd.git` calls + 1 `test_quarantine._git`; ~0.45 s a call on this machine) × 44 rows. My re-run took
14.55 s. That is inherent to running the tool per row, not a TESTING.md defect. The spec's "well under 10 s" was the designer's
estimate, not a measurement; no fix asked. 10 (`C:\` on POSIX → outside) — accept (named, safe).

**3. dispatch_new.** I ran the REAL gate functions on a printed dispatch (worktree, real tool, owns with a `(new)` file and a quarantined
test, given with a file absent on the base, `--names` with a present and an absent name). `decide_full` 0 / `check` 0 / `header_ids`
`{'task': 't-862'}` / owned 3 / given 2 / `designer_threshold` (3, 0) / `given_path_warn` empty — identical for headers alone and for
headers + block. The block printed `quarantined`, `absent (given)`, `absent: name`, `names` and `more` lines. The `(new)` owned file gave
no line (correct). critic / scout / designer dispatches without owns print no block. A refused dispatch prints nothing (existing rows
plus 2 new ones). No block kind collides with KEY_GROUPS or the id keys, and no block line is numbered. Defects: F1, F2.

**4. Battery.** Hand runs, all safe: `a.b*` → `absent: name` (fixed string); `[x]`, `^git`, `as_text(` matched literally; Cyrillic name
`кучка`/`ф` matched as plain strings (ASCII-only `_WORDY`, over-report — git's `-w` treats UTF-8 bytes as non-word anyway); a tab in a
path or name → `unsearched ... control character`; `../outside.py` → unsearched by base name; a lowercase-drive backslash absolute path
inside the repo resolved correctly; blank path and blank name items ignored; `--base origin/main:tools` → Example C. Missing rows: F8.
Header defect: B1.

**5. Standing questions.** DUPLICATION AND CONSISTENCY: F5 (`_first_line` ×3). `_glob_re` has no forge twin. I grepped tools/ for
`fnmatch|def _?glob|translate(`: only dup_report.py uses fnmatch, with other semantics. A divergence from git's glob falls to `code`,
which is over-report. The `test_quarantine` reuse goes through `_blob_sections` / `_pkg_module` / `Unknown` as F-13 says, and there is
no second parser of either registry. `gitcmd.git` is the runner. The `_git` wrapper around it only turns a raising (monkeypatched)
runner into rc -1. Axis 34 / one road: the §2.7 split in the docstring is honest about the two questions, but the tool's test readers
do overlap with "what to run", so the claim of a queued convergence must be true before merge: F6. F-11 is kept (no package file
touched). CODE QUALITY: F4, F9; no dead branch found. CLASS-WIDE: axes 9 / 10 / 13 / 34 are Lead edits L8 / L9 queued in the spec §6,
so they are not findings here. B1 is walked over its whole surface (5 neighbours above). REFUSAL TEXTS: E-1 matches the spec
verbatim. The step-4 stderr line matches. TESTS: 279 + 75 test lines against ~690 product lines, so no `tests-over:` is needed. The
T1 rows kill the unknown classes they are for (grep-rc-128/-1, lstree-fails, base-missing, quarantine-*). The false zero of B1 has no
row: F8. ARCHITECTURE: `architecture: none` holds (no `ai-packages/` file in the diff). RATCHETS / JUDGMENT: none touched; the tool
prints no verdict word (P27).

## Trail

- Read: the spec (lines 1-420, 480-868); the handoff t-917 (whole); critic-diff-brief.md (whole); `tools/owns_readers.py` (whole),
  `tools/owns_readers.json` (whole), `tools/test_owns_readers.py` (whole); the diffs of `tools/dispatch_new.py` and `tools/test_dispatch_new.py`;
  `tools/test_dispatch_new.py:1-45`; `tools/dispatch_manifest.py:80-100, 860-880`; `tools/dispatch_gate.py:938-990`;
  `tools/test_quarantine.py:85-125`; `tools/gitcmd.py:36-75`; `.gitattributes` and `ai-packages/qa-factory/.gitattributes` at origin/main.
- Re-run (worktree subshell): `python -m pytest tools/test_owns_readers.py tools/test_dispatch_new.py -q -p no:cacheprovider` →
  `91 passed in 14.55s`.
- Tool runs (worktree, base origin/main 237ead44): case (a) `--readers` → `readers: 20 outside owns, 11 lines below` (0.78 s); (a)
  `--all` → 20 lines; case (b) → `readers: 253 outside owns, 6 lines below` (1.04 s); story_run.py with no names → `hot` + `more`; base
  `54983180~1` → `quarantine: unknown (test-layers.json absent at be804ba2)`, `127 test, ? quarantined`; mechanism_gate `--all`,
  journal_echo `--all`, piles.py `--all`, ci_read.py `--all`; the battery of key 4; two owned paths `--all` (F9).
- Independent greps (origin/main): `git grep -l -i -F dispatch_manifest` (21 files); `git grep -c -i -F s0_criteria`; `git grep -l -F
  journal_echo -- tools .claude .githooks .github ai-packages` (diffed against the tool's list: 1 difference, explained); `git grep -l -F
  mechanism_gate -- .githooks .claude/settings.json .github` (commit-msg + forge-check.yml); `git grep -n -F tools/ --
  .github/workflows/forge-check.yml`; nested fixture JSON naming `.py` (52) and tools md/yaml (8), using the `:(glob)` pathspec form; `git
  grep -l -i owns_readers` (negative for `plans/`; positive control: the spec found).
- A scratch script (`scratchpad/k3.py`, not committed) ran `dispatch_new.main` and then `decide_full`, `check`, `header_ids`, `owned_paths`,
  `given_paths`, `designer_threshold` and `given_path_warn` on the headers and on the full text; the results are given under key 3.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "B1 owns_readers.py:577-580 (with :354-365, :380-383): the header prints 'readers: 0 outside owns' when no owned path was searched (outside the repo, a directory over dir_cap, a control character, report([])), and gives no partial mark when some were skipped. This is a false zero, and S2's note regex takes it as a pass. Fix: 'readers: unknown -- no owned path was searched (<k> unsearched below)'; a '; unsearched: <k> paths' segment when partial; T1 rows.",
    "B2 owns_readers.json scope + docstring KNOWN MISS 5: .github/workflows/*.yml run the tools (forge-check.yml: piles.py, install_parity.py, lint_ratchet.py ...), are not searched, and no miss names them. Fix: add .github/workflows/* to the code row; KNOWN MISS 5 lists the unsearched areas by name (docs/, plans/, root md, nested fixture JSON under scripts/tests/fixtures/<dir>/, tools md/yaml fixtures, gateway/)."
  ],
  "fixes": [
    "B1 and B2 above (block the merge).",
    "F1 dispatch_new.py:173-175,180-182,188: a checker exception or a degraded cut on headers+block refuses the whole dispatch; route it to the step-4 replacement line instead.",
    "F2 dispatch_new.py:154: _ids_refusal runs on the headers only; run it on the final text too (spec 3.1 step 3) or name the deviation.",
    "F3 owns_readers.py:495,524,530,557: with the quarantine registry unknown, listed layered test readers print as plain (test) and are counted in 'N test' and hot. Mark them '(test, quarantine unknown)' / 'N test (quarantine unknown)', and raise the '?' only for cls == test readers (now fixture JSON and helper code raise it).",
    "F4 owns_readers.py:339-469 report() 131 lines / 4 nesting levels and :508-581 render() 74 lines: split them.",
    "F5 owns_readers.py:164-167 duplicates gitcmd._first_line (gitcmd.py:63); dispatch_new.py:135,177 add two more inline copies; use one helper.",
    "F6 owns_readers.py:52 'Their convergence is a queued node': no node exists at origin/main; name spec node C6 (L9), or land L9 in the same wave and name its id.",
    "F7 test_dispatch_new.py:119-121: the docstring claims the designer count but nothing asserts it; add the designer_threshold assert.",
    "F8 test_owns_readers.py: missing battery rows: AT-cap rows for test_cap 25, data_cap 12, dir_cap 40, names_cap 20; PATH_CAP 200 AT and BEYOND; a control character in a path and in a name; regex-metacharacter and Cyrillic names; a .. relative path; the mixed searched/unsearched row of B1.",
    "F9 owns_readers.py:516-572: under --all with 2+ owned paths, subject 2's test lines follow subject 1's code lines; sort the outside slots test-first before rendering."
  ],
  "class_completeness": "B1 walked over its surface (the header count when input was not searched): outside-repo, directory over dir_cap, control character, PATH_CAP overflow, empty API list, mixed input; all go into one fix. B2: the scope's executable readers (.githooks found, .claude/settings found, .github/workflows missed); the other unsearched areas are measured (52 nested fixture JSON, 8 tools md/yaml) and are to be named in KNOWN MISS 5. SIBLING_MAP axes 9, 10, 13, 34 are Lead edits L8/L9 queued in spec section 6; F6 asks that L9 be real before the docstring claims it.",
  "trail": {
    "read": [
      "docs/tasks/specs/20261116-spec-facts-by-code-spec.md (1-420, 480-868)",
      ".claude/worktrees/agent-a585c072bec1720f8/docs/tasks/handoffs/t-917-spec-facts-s1.md",
      "docs/tasks/critic-diff-brief.md",
      "tools/owns_readers.py (worktree, whole)",
      "tools/owns_readers.json (worktree)",
      "tools/test_owns_readers.py (worktree, whole)",
      "tools/dispatch_new.py diff, tools/test_dispatch_new.py diff and 1-45",
      "tools/dispatch_manifest.py 80-100, 860-880",
      "tools/dispatch_gate.py 938-990",
      "tools/test_quarantine.py 85-125",
      "tools/gitcmd.py 36-75",
      ".gitattributes, ai-packages/qa-factory/.gitattributes at origin/main"
    ],
    "reruns": [
      {"command": "python -m pytest tools/test_owns_readers.py tools/test_dispatch_new.py -q -p no:cacheprovider (worktree)", "result": "91 passed in 14.55s"},
      {"command": "python -B tools/owns_readers.py --paths tools/dispatch_manifest.py tools/test_dispatch_manifest.py --readers", "result": "readers: 20 outside owns, 11 lines below -- base origin/main 237ead44; matches independent grep (21 files incl. the owned test)"},
      {"command": "python -B tools/owns_readers.py --paths ai-packages/qa-factory/scripts/story_run.py --names s0_criteria", "result": "readers: 253 outside owns, 6 lines below; 3 test + 1 data names lines, 1 code; matches independent grep"},
      {"command": "python -B tools/owns_readers.py --paths tools/mechanism_gate.py --all", "result": ".githooks/commit-msg listed; .github/workflows/forge-check.yml missed (B2)"},
      {"command": "python -B tools/owns_readers.py --paths C:/QAFactory/forge-repo/tools/gitcmd.py (from worktree); --paths tools/; --paths .", "result": "readers: 0 outside owns + one unsearched line each (B1)"},
      {"command": "scratchpad k3.py: dispatch_new.main + decide_full/check/header_ids/owned_paths/given_paths/designer_threshold/given_path_warn on headers vs headers+block", "result": "identical: decide 0, check 0, ids {task: t-862}, owned 3, given 2, designer (3, 0), warn empty; critic/scout/designer: no block"}
    ]
  }
}
```
