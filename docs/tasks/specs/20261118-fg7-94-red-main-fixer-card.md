# FG7-94 -- red main, one fixer: draft card (designer, t-1452)

Status: DRAFT for the Lead. Forks in §7 are returned, not decided. Owner's decisions 18.11 (taken as given, not forks):
ready branches merge without waiting for CI, also over a check that is already red; ONE builder fixes a red main while
every other node goes on; the fixer has no round limit; when real reds run out the fixer takes the known flaky ones.

## §1 Scope, facts, invariants touched

Goal: main's CI state is known without anyone asking, a red main is one list with one fixer, and every red names the
merges that could have brought it.

Facts (Lead's measurement, quoted with the command):
- merge waves do not wait for CI: `grep -n 'Волны слияния CI не ждут' PROJECT.md` -> 233.
- canon starts only by hand: `sed -n 17,18p .github/workflows/canon.yml` -> `on: workflow_dispatch:`.
- canon load 18.11: `gh run list --workflow canon.yml --created >=2026-11-17` -> 136 runs, median 28 min, max 73,
  89 failed; job queue wait up to 446-870 s; 8-20 jobs per run (pile row FG7-91, `gh api .../runs/<id>/jobs`).

Facts measured by the designer (Read/Grep, carrier named; no shell):
- M1 `tools/ci_read.py::cmd_start` dispatches with `body={"ref": "main", ...}`: a dispatched canon's `head_sha` is
  main's HEAD at dispatch time whatever `inputs.ref` canonises (canon.yml line 13 says the same of head_branch).
- M2 `tools/ci_read.py::cmd_run_state` takes `runs[0]` of `/actions/runs?head_sha=<sha>` with NO workflow or event
  filter, and `_state_word` maps `cancelled` to `failure`. So `run_state(<main sha>)` can return a dispatched canon of
  an agent branch (M1), and a run superseded by concurrency reads as red. Unfit as-is for a red list (fork F0).
- M3 `.github/workflows/forge-check.yml` already runs on `push: branches: [main]` with `concurrency: group:
  forge-check-${{ github.ref }}-${{ inputs.ref }}`, `cancel-in-progress: true` (lines 15-28).
- M4 `.github/workflows/quarantine-watch.yml` lines 33-35: `push: branches: [main]`, `paths: [...plugin.json]` -- a
  push run on main whose reds belong to the quarantine, not to main.
- M5 `.github/workflows/nightly.yml` checks out `${{ inputs.ref || 'main' }}` (lines 65-266): called with an empty ref
  it tests main's tip AT JOB TIME, not the pushed sha.
- M6 forge-check.yml line 64: a non-empty `CANON_REF` sets `base=$(git merge-base origin/main HEAD)`; for a main sha
  that base is HEAD itself (diff-scoped steps see an empty diff). Line 124: `runner-facts` runs on event push.
- M7 `tools/session_context.py` docstring lines 45-47: SessionStart is "Fast (<2s) and NO network at all".
  Precedent for a detached background run started by SessionStart after reading its last status:
  `session_context.py::waits_lines` (`wait_reaper.launch`), `worktree_sweep.py::launch_background`.
- M8 `tools/test_workflows.py::test_canons_dry_only_door_calls_dry_story_and_skips_checks_full_clock` pins
  `jobs.checks.if == "${{ !inputs.dry_only }}"`; `test_the_canon_is_named_by_its_ref...` pins `run-name` verbatim.
- M9 `tools/mechanism_gate.py` protected list holds `tools/ci_read.py` (line 271) and `tools/journal_lock.py`
  (line 293); a NEW module imported by session_context would have to join that list.
- M10 `tools/wave.py::Wave.run` holds machine lock `main-merge`; `Wave.finish` prints the summary inside it.

Estimates (no shell; the Lead runs the command):
- main pushes per day: `git -C C:/QAFactory/forge-repo log --first-parent --oneline --since="2026-11-18 00:00"
  --until="2026-11-19 00:00" origin/main` (count lines). `estimate`
- forge-check push runs on main cancelled by its own concurrency: `gh run list --workflow forge-check.yml --branch
  main --event push --created 2026-11-18 --json conclusion --jq 'group_by(.conclusion)|map({(.[0].conclusion):length})|add'`. `estimate`
- jobs of canon's `full` part: `gh api repos/<o>/<r>/actions/runs/<canon run id>/jobs --jq '.jobs[].name'`. `estimate`
- exact test ids of the two known flakes ("t4a 830/831" -> `scripts/tests/test_detector_verdict.py`, plans/features.json:556;
  "the CX1-20 flake" -> id unknown to the designer): the Lead seeds them (§2 D7). `estimate`

AR / variety: `AR: none -- no file under ai-packages/qa-factory/ is touched`; `variety: none -- no language, project
or case axis: one workflow allow-list, one carrier, one writer, one formatter, one launcher, one network road`.

## §2 Design

D1. Canon on main (file `.github/workflows/canon.yml.proposed`; the Lead places it):
- `on:` gains `push: branches: [main]` beside `workflow_dispatch` (inputs unchanged).
- Top-level `concurrency:` with ONE expression that also serves FG7-91:
  `group: ${{ github.event_name == 'push' && format('canon-push-{0}', github.ref) || format('canon-run-{0}', github.run_id) }}`
  (dispatch runs keep today's behaviour: a group of their own, nothing cancelled) and
  `cancel-in-progress:` per fork F1 (recommended `${{ github.ref != 'refs/heads/main' }}`: false on main).
- `checks` is skipped on push (fork F2): `if: ${{ github.event_name != 'push' && !inputs.dry_only }}`; forge-check
  already runs on the same push (M3).
- `full` and `clock` get `ref: ${{ inputs.ref || github.sha }}` (M5: never the moving tip). `run-name` unchanged (M8).
- Queue cost: §6.

D2. The network road: a new command `push_jobs` in `ci_read.py::make_commands` and a module function
`ci_read.main_push_jobs(root, sha) -> (word, {workflow: run_id}, {job_name: verdict})`, built exactly like
`run_state` (same `backend_for`, token door, `_open`; never raises, never prints). It lists
`/actions/runs?head_sha=<sha>&event=push&branch=main&per_page=20`, keeps rows with `head_sha == sha`, `event == "push"`,
`head_branch == "main"` and `path` ending in a file of `MAIN_WORKFLOWS = ("forge-check.yml", "canon.yml")` (the
allow-list: quarantine-watch, M4, never counts); newest run per workflow; one jobs request per kept run.
Job verdict: `success`; `failure` (failure, timed_out); `cancelled`; `skipped`; `pending` (queued, in_progress,
waiting, requested, pending); `unknown` (neutral, action_required, stale, anything else). A run concluded
`startup_failure` yields one job `<workflow>: startup_failure` = `failure`. word: `none` (no kept run), `unknown`
(any transport/parse/token failure), else `read`. `run_state` and `_state_word` stay byte-identical (wave reads them).

D3. The carrier and its one writer: `<git common dir>/main-red/state.json` (fork F6), JSON version 1:
`head`, `read_at`, `error`, `tips` {sha: task, branch, kind, subject, pushed_at, runs, jobs, state, final},
`order` (first-parent list, newest last), `red` {job: first_red, last_green, range, opened_at}, `fixer`
{task, since} | null, `flaky` [{id, why, added}], `history` (last `HISTORY_MAX` = 50 events).
ONE writer: `ci_read.main_red_write(root, mutate)` -- read, apply, `os.replace` from a temp file beside it, under
`journal_lock.machine_lock("main-red", 10, repo=root)`. Every mutation below goes through it; nothing else opens the
file for writing. Readers read without the lock (atomic replace: whole old or whole new file).
Mutations: `record` (wave), `refresh`, `fixer set|done`, `flaky add|done`.

D4. Refresh and the fold (`ci_read.main_red_refresh(root)`, `ci_read.main_red_fold(order, tips, prior_red)` pure):
- `git fetch origin main` (timeout 30 s; failure: the local ref, `error` recorded), then
  `git rev-list --first-parent -n MAIN_WINDOW origin/main` (30). Tips not yet in the file get `kind: direct` and their
  subject; tips already `final` are never re-read; others go through `main_push_jobs`.
- Tip state: `pending` when younger than `GRACE_NEW_S` (120) or any kept run pending; `unknown` on a failed read, or
  word `none` older than `NONE_UNKNOWN_S` (900), or pending older than `PENDING_STALE_S` (5400 = 90 min > the measured
  max 73); `red` when any job is `failure`; `green` when forge-check's push run is present and every kept run's jobs
  are success/skipped (fork F9); otherwise `superseded` (cancelled without failure). `final` = green | red | superseded.
- Fold, per job name J over `order` oldest -> newest, using only tips with a FINAL verdict for J (success/failure):
  J's latest final verdict `failure` -> J is open: `first_red` = the earliest tip of J's trailing failure streak,
  `last_green` = J's latest success before it (or null), `range` = every tip after `last_green` up to `first_red`
  (tips with no verdict for J inside it are named, never skipped). Latest final verdict `success` -> J closes
  (history `closed at <sha8>`, with the tip's task; equal to the fixer's task -> `fixed by fixer`).
  A prior open J with no final verdict in the window stays open unchanged. At a head tip that is `green`, an open J
  with no job of that name in it closes as `gone` (a renamed/removed job, e.g. after FG7-90).
- Range in `show`: every tip as `<sha8> <task|direct> <branch|subject>`, at most 5 then `+N more`.

D5. The SessionStart line (no network: one file read, at most two local git calls of 5 s each, M7).
`ci_read.main_red_line(root, now) -> str | None` is the ONE formatter (also printed by `ci_read.py main-red`);
`session_context.main_red_lines(root)` calls it, THEN calls `ci_read.main_red_launch(root, "session-start")`
(fork F3). Head = the file's `head` when local `origin/main` equals it or is its ancestor; else
`unknown: origin/main <sha8> not read yet`. Forms (ASCII, at most `LINE_MAX` = 300 chars):
- red list non-empty:
  `MAIN RED since <sha8>: <job> [<task>, <task> +N], <job> [...] +N more; head <sha8> <green|red|pending|unknown>; fixer <t-NNN|none>; flaky <n>`
  (`since` = the earliest `first_red`; at most 3 jobs, 2 tasks per job; `; flaky <n>` only when n > 0)
- list empty, head green, no fixer: NO line.
- list empty, head green, fixer open (fork F4): `MAIN GREEN at <sha8>; fixer <t-NNN> on the flaky queue: <n> left`
  (n = 0: `...; nothing left, close: python -B tools/ci_read.py main-red fixer --done <t-NNN>`).
- list empty, head pending (fork F5): `MAIN CI pending at <sha8> (<m> min); last green <sha8|none>`.
- head unknown, or file absent/unreadable: `MAIN CI unknown at <sha8>: <why>; refresh: python -B tools/ci_read.py main-red refresh`
  (why: `never read` | `not read yet` | `no run after 15 min` | `no verdict after 90 min` | `state unreadable (<Exc>)` | the recorded `error`).
- no `origin/main` in the root: NO line (fork F11).
Position: right after `test_quarantine_line` in `build_context_lines`. Exception anywhere -> one line
`MAIN CI: unavailable (<Exc: text, at most 120 ASCII>)`, the rest of the context intact.

D6. wave.py (`Wave.locked` / `Wave.run`): after each successful push to main (the merge tip, and the journal / piles
status commits wave pushes itself) `ci_read.main_red_record(root, sha, task=..., branch=..., kind=merge|journal|piles)`;
it never raises and returns an error text or None; an error prints one line `main ci: tip not recorded (<why>)` and
the exit code is unchanged. After the `main-merge` lock is released, `ci_read.main_red_launch(root, "wave")`.
wave never waits for, reads to decide, or refuses on main's state.

D7. CLI (dispatched in `ci_read.main` before `common.run`; `ci_read_common.py` untouched; docstring of ci_read.py gains
the lines): `python -B tools/ci_read.py main-red [show|refresh]` (no subcommand = the D5 line, or `main green at <sha8>`
when there is no line), `main-red fixer <t-NNN>`, `main-red fixer --done <t-NNN>`,
`main-red flaky add "<id>" --why "<text>"`, `main-red flaky done "<id>" --by <t-NNN>`.
`main_red_launch(root, trigger)`: a detached `refresh` in the shape of `worktree_sweep.launch_background` (never
waits, no console window), skipped when the last launch is younger than `LAUNCH_MIN_S` (300) or `origin/main` does
not resolve; a refresh that finds the lock busy exits 0 with `another refresh is running`.

D8. Opening the fixer (by the Lead, from the line; fork F7):
1. SessionStart shows `MAIN RED since X: ...; fixer none`.
2. Lead: `python -B tools/ci_read.py main-red show` (per red job: range tips with task/branch, run ids), then
   `python -B tools/ci_read.py why <run_id> --tail 60` for the failing job(s).
3. Lead writes a builder dispatch with `python -B tools/dispatch_new.py`: owns = the files the failing tests and the
   range's merges point at (Lead's judgment, widened per round on "needed beyond the manifest"); DoD = the failing
   check(s) green by their narrow run; prose: run `main-red show` at the start of every round (new reds joined the
   list), take the flaky queue when the list is empty, report each flaky id fixed / not fixed.
4. Lead: `python -B tools/ci_read.py main-red fixer t-NNN` (refused while another is open, or when the list is empty).
5. The fixer's branch merges through `wave.py merge`; the refresh after it closes the reds that turned green.
6. Lead: `main-red fixer --done t-NNN` when the list and the flaky queue are empty, or by decision. No round limit.

## §3 Edges (behaviour + the invariant it protects)

| id | edge | behaviour | invariant |
|---|---|---|---|
| E1 | main green, no fixer | no line, no fixer; `fixer t-NNN` refused `main is not red` | no line only after a FINAL green of the head tip; absence of data is never silence-as-green |
| E2 | second red while a fixer is open | J joins `red`; fixer unchanged | at most one fixer exists; a red is never lost because a fixer is open |
| E3 | a red turns green by itself | J leaves the list (history `closed at <sha8>`) | only a final `success` of J at a later tip, or J `gone` at a green head, closes J; cancelled/skipped/pending/unknown/absent never close |
| E4 | no CI run known for main HEAD | `MAIN CI unknown at <sha8>: <why>` | unknown is never printed or stored as green |
| E5 | one fixer at a time | `fixer t-B` while `t-A` open: exit 1 `fixer t-A is open`; `--done t-B` while `t-A` open: exit 1 | the carrier never holds two fixers |
| E6 | a run superseded by concurrency (`cancelled`) | tip `superseded`; J neither opens nor closes | cancelled is never red, never green |
| E7 | a dispatched canon of an agent branch with `head_sha` = main (M1) | excluded (`event != push`) | a run that tested other bytes never counts for main |
| E8 | quarantine-watch push run on main (M4) | excluded (allow-list) | quarantine reds never open MAIN RED |
| E9 | `startup_failure` (a broken workflow file on main) | job `<workflow>: startup_failure`, red | a broken workflow on main is never silent |
| E10 | more than 30 new tips since the last refresh | the oldest are absent from the window; open reds kept | a red never leaves by falling out of the window |
| E11 | carrier corrupt / wrong shape | refresh renames it `state.json.corrupt-<utc>` and starts fresh, prints that; the line says `state unreadable` until then | a corrupt or empty file never reads as green |
| E12 | concurrent writers | lock `main-red` 10 s; refresh busy -> exit 0 quietly; record busy -> wave's one error line; CLI busy -> exit 1 `retry` | no write without the lock; no torn file |
| E13 | TEMPORAL: canon's push trigger | before the Lead places canon.yml.proposed: only forge-check push runs exist, a tip is judged on them (F9); after: canon's push run counts too. Created by the Lead's placement at acceptance | in both worlds green needs forge-check's final success |
| E14 | TEMPORAL: the carrier | absent before the first record/refresh: line `unknown ... never read`; created by the first `main_red_write` | the absent world prints unknown, never nothing |
| E15 | hostile remote text (job names, subjects: newline, ANSI, non-ASCII, 10 kB) | `_ascii_sanitize`, each name at most `NAME_MAX` = 60, the line at most 300 with `+N more` | one line, ASCII, bounded |
| E16 | CLI input battery | task id must match `t-[0-9]{3,9}[a-z]{0,2}`; flaky id / why 1..`FLAKY_ID_MAX` = 200 printable ASCII, no newline; empty, 201 chars, unicode, `t-1;x` -> exit 2 before the lock | nothing malformed reaches the carrier |
| E17 | a range of more than 5 tips / of 1 tip | `show`: 5 then `+N more`; line: 2 tasks then `+N`; one tip: that task alone | a red is never pinned on one merge when the data names several |
| E18 | a red with no earlier success of J anywhere | `last_green: null`; `show` says `before <oldest sha8 read>` | an unknown start is named, not guessed |
| E19 | a branch touching an already red check | merges (owner 18.11); wave unchanged | wave never waits or refuses on main's state |
| E20 | fixer's task closed in the journal while the carrier still names it | carrier unchanged; line keeps `fixer t-NNN` | only `fixer --done` closes a fixer (no round limit, no auto close) |
| E21 | head pending with an empty list | the pending line (F5) | "no line" keeps meaning green |
| E22 | a red caused only by a known flaky test | a red like any other (F10) | job-level data never decides "only flaky" |
| E23 | no `origin/main` in the root (test roots, a bare dir) | no line, no launch (F11) | silence only where there is no main to judge |

Conflicting requirement pairs, each returned as a fork: "cancel-in-progress" vs "a verdict must arrive" (F1);
"run_state per merge commit" vs M2 (F0); "no network at SessionStart" vs a fresh state (F3); "main green: no line,
no fixer" vs "when real reds run out the fixer takes the flaky ones" (F4); "no line = green" vs a pending head (F5).

## §4 A function in a more consequential role: error direction

`main_push_jobs` + the fold move CI data from advice (wave's information line) to the source of a session-wide
status and a fixer. Allowed error direction: toward `unknown`/`pending` (a noisy line), never toward green, never a
red from a run that did not test main's bytes. Adversarial inputs that must stay on the safe side (rows of §5 test 2):
a dispatch run with `head_sha` = main and `event: workflow_dispatch`; a push run of `quarantine-watch.yml`; a run with
`head_sha` of another commit; `conclusion: cancelled` on run and jobs; `conclusion: neutral|action_required|stale`;
`startup_failure` with zero jobs; an empty `workflow_runs`; HTTP 500 / not JSON / `workflow_runs: "x"` / no token / no
origin -> `unknown`.

## §5 Builder card

task: <t-NNN, Lead>
node: forge/7/FG7-94
given:
C:/QAFactory/forge-repo/docs/tasks/specs/20261118-fg7-94-red-main-fixer-card.md (this spec, §2-§4)
C:/QAFactory/forge-repo/tools/ci_read.py (run_state, cmd_run_state, cmd_start, main)
C:/QAFactory/forge-repo/tools/session_context.py (build_context_lines, waits_lines, test_quarantine_line)
C:/QAFactory/forge-repo/tools/wave.py (Wave.run, Wave.locked, Wave.finish)
C:/QAFactory/forge-repo/tools/worktree_sweep.py (launch_background: the detached-launch shape)
C:/QAFactory/forge-repo/tools/journal_lock.py (machine_lock, common_dir)
C:/QAFactory/forge-repo/.github/workflows/canon.yml, forge-check.yml, nightly.yml, quarantine-watch.yml
owns:
C:/QAFactory/forge-repo/tools/ci_read.py
C:/QAFactory/forge-repo/tools/test_ci_read.py
C:/QAFactory/forge-repo/tools/session_context.py
C:/QAFactory/forge-repo/tools/test_session_context.py
C:/QAFactory/forge-repo/tools/wave.py
C:/QAFactory/forge-repo/tools/test_wave.py
C:/QAFactory/forge-repo/tools/test_workflows.py
C:/QAFactory/forge-repo/.github/workflows/canon.yml.proposed
non-goals: forge-check.yml / nightly.yml / quarantine-watch.yml unchanged; `run_state` and `_state_word` byte-identical; no new module (M9); ci_read_common.py unchanged; dispatch_new.py unchanged; no test-level parsing of CI artifacts; canon.yml itself is placed by the Lead
handoff: branch + report C:/QAFactory/forge-repo/docs/tasks/specs/reports/<date>-fg7-94-build-report.md
edges: §3 E1-E23 of the spec, inline there with their invariants
DoD: `python -m pytest tools/test_ci_read.py tools/test_session_context.py -q` and `python -m pytest tools/test_wave.py -k main_red -q`; then the probe for D1: byte copy canon.yml aside, copy canon.yml.proposed over canon.yml in the worktree, `python -m pytest "tools/test_workflows.py::test_canons_dry_only_door_calls_dry_story_and_skips_checks_full_clock" "tools/test_workflows.py::test_the_canon_is_named_by_its_ref_and_its_clock_runs_after_a_red_job" -q`, restore from the byte copy, sha256 before/after in the report (hygiene point 7)
siblings: FG7-90 (ci_read.py `jobs`, forge-check.yml: disjoint functions in ci_read.py, rebase on whichever lands first), FG7-91 (canon.yml: one concurrency block, D1's expression serves both), FG7-92 (wave.py; calls `main_red_record(..., preflight=...)` per F8), FG7-88 (session_context.py: disjoint functions)
designer: C:/QAFactory/forge-repo/docs/tasks/specs/20261118-fg7-94-red-main-fixer-card.md

Acceptance criteria:
A1 `main_push_jobs` follows D2; `run_state`, `_state_word`, `cmd_run_state` unchanged (diff shows no line of them).
A2 the carrier has exactly one writing function (`main_red_write`); grep of `state.json` writes in the diff finds no
other site; atomic replace + lock `main-red`.
A3 the fold, the tip states and the constants follow D4 (`MAIN_WINDOW` 30, `GRACE_NEW_S` 120, `NONE_UNKNOWN_S` 900,
`PENDING_STALE_S` 5400, `HISTORY_MAX` 50) as module constants.
A4 the one formatter (D5) serves both SessionStart and the CLI; the line forms match D5 character for character.
A5 SessionStart makes no network call (the launch is detached and only after the read); one exception = one line.
A6 wave: record only after a push succeeded, launch only after `main-merge` is released; output and exit unchanged
except the one error line.
A7 canon.yml.proposed follows D1; nothing else in the workflow changes; the probe witness is in the report.
A8 the ci_read.py docstring documents `main-red`; the commit carries the form `tools/mechanism_gate.py` demands for a
protected file (ci_read.py is on its list, M9) -- read the form there, the spec does not copy it.

test lines, strongest first (write top-down until test lines reach code lines; report the rest `tests not written: <line> -- over budget`):
1. test: tools/test_ci_read.py::new table `test_main_red_fold` -- rows opens-with-range, second-red-joins-fixer-kept, self-heal-closes, cancelled/skipped/pending/unknown-neither-open-nor-close, gone-at-green-head, range-over-5, prior-red-outside-window-kept, no-earlier-success-null | expected from: §2 D4, §3 E2 E3 E6 E10 E17 E18, owner's word 18.11
2. test: tools/test_ci_read.py::new table `test_main_push_jobs` (beside `test_run_state_reads_the_answers_of_the_backend`, same `state_routes` stubs) -- the §4 inputs | expected from: §2 D2, §3 E4 E7 E8 E9, §4
3. test: tools/test_session_context.py::new table `test_main_red_line` -- green-no-fixer silent, red form, fixer-on-flaky, pending, never-read, origin-ahead, corrupt, hostile names at/over 60 and the line at/over 300, no-origin-main silent | expected from: §2 D5, §3 E1 E4 E11 E14 E15 E21 E23
4. test: tools/test_ci_read.py::new table `test_main_red_cli` -- second fixer refused, `--done` of another task refused, fixer on an empty list refused, task-id and flaky-id battery (empty, 200 ok, 201, unicode, newline, `t-1;x`) | expected from: §3 E1 E5 E16
5. test: tools/test_wave.py::new `test_main_red_record_after_push_and_launch_after_lock` -- no record on a refused push; a failing record = one line, exit unchanged; launch called after the lock is released | expected from: §2 D6, §3 E19
6. test: tools/test_session_context.py::a row in the s8 MAX_LINES cut test -- the MAIN line survives the cut that takes the wiring line; an exception is one `MAIN CI: unavailable` line | expected from: §2 D5 position and fail-open
7. test: tools/test_workflows.py::the two canon tests of the DoD, rows edited for D1 (checks skipped on push, `full`/`clock` ref, the concurrency block) | expected from: §2 D1, fork F1/F2 as decided

## §6 Queue cost of canon on main (D1)

- Base load 18.11 (Lead's fact): 136 canon runs, median 28 min, max 73, job queue wait up to 446-870 s.
- Added per main push: canon minus `checks` (forge-check already runs on that push, M3): `full` + `start` + `clock`;
  the job count of `full` is an `estimate` (§1 command).
- Bound with F1(a) (`cancel-in-progress: false` on main): GitHub keeps one running and one pending run per group and
  a newer pending replaces the older, so at most one main canon runs at a time: at most 1440 / 28 = 51 completed runs a
  day at the median duration (arithmetic on the Lead's fact), each one a verdict.
- With F1(b) (`true`): the same one-slot bound, but a push interval shorter than the run cancels every run before its
  verdict (no verdict while merges keep coming) and cancelled runs still burn runner time up to the cancel.
- Offset: the Lead's hand dispatches of `canon --ref main` stop; their count 18.11 is an `estimate`:
  `gh run list --workflow canon.yml --event workflow_dispatch --created 2026-11-18 --json displayTitle --jq '[.[]|select(.displayTitle|endswith(" main"))]|length'`.
- After placement: one day later the same `gh run list` metrics against 18.11 (as FG7-91 asks for its trigger).

## §7 Forks (numbered, each with a recommendation)

- F0 The DoD says "ci_read.run_state per merge commit"; M2 makes it unfit (no event/workflow filter, cancelled = red).
  (a) a sibling `main_push_jobs` on the same road, `run_state` untouched (wave's branch-head reading keeps its meaning) --
  RECOMMENDED; (b) change `run_state` itself (wave's branch heads have no push runs, so it would read `none` there).
- F1 `cancel-in-progress` for the main group. (a) false on main, true elsewhere (`${{ github.ref != 'refs/heads/main' }}`):
  pending superseded, every run finishes -- RECOMMENDED; (b) true as the pile row says: starves when merges come faster
  than ~28 min. (c) the same question for forge-check's own push run on main (M3, `cancel-in-progress: true` today):
  forge-check.yml is FG7-90's file -- recommended: FG7-90 takes the same expression after the Lead's measurement (§1);
  otherwise a finding row for that pile.
- F2 canon on push and its `checks` job. (a) skip `checks` on push (forge-check runs on the same push; avoids the
  shared concurrency group `forge-check-refs/heads/main-` of M3 cancelling one of the two, an `estimate` of GitHub's
  reusable-workflow concurrency) -- RECOMMENDED; (b) run `checks` with `ref: github.sha` (M6: diff-scoped steps see an
  empty diff, runner-facts runs twice); (c) drop forge-check's push trigger (FG7-90's file; runner-facts loses its trigger).
- F3 freshness without network at SessionStart. (a) refresh only by wave and by hand: a red that lands after the last
  merge stays unseen until the next merge; (b) plus a detached refresh launched by SessionStart after its read,
  rate-limited (precedent M7) -- RECOMMENDED; (c) a machine scheduler (none exists here).
- F4 "main green: no line, no fixer" vs the fixer taking the flaky queue. (a) green never opens a fixer; an OPEN fixer
  continues on the flaky queue and the line `MAIN GREEN ... fixer t-NNN on the flaky queue` stays while it is open --
  RECOMMENDED; (b) the Lead may open a fixer on the flaky queue alone while main is green; (c) the fixer closes at
  green and the flaky queue waits for the next red.
- F5 a pending head with an empty list. (a) the pending line (keeps "no line = green", E21) -- RECOMMENDED;
  (b) silent while the last final head was green and pending is under 90 min (less noise; no line then no longer
  means green).
- F6 carrier location. (a) `<git common dir>/main-red/state.json`: machine-local, untracked, shared by every worktree
  of the clone (precedent `worktree_sweep.STATE_DIRNAME`) -- RECOMMENDED; (b) a tracked repo file (a commit per refresh,
  merge conflicts); (c) journal events (append-only, the list is a state, not events).
- F7 the fixer's identity. (a) the Lead records it with `main-red fixer t-NNN` (D8) -- RECOMMENDED now;
  (b) `dispatch_new.py --fixer` records it (outside these owns: a later node). Question to the Lead: which node id a
  fixer dispatch carries (a standing pile row "main-red fixer" or `node: none`).
- F8 FG7-92's preflight reds "passed to the FG7-94 queue". (a) stored on the tip record (`main_red_record(...,
  preflight=[check names])`), shown by `show` to the fixer, never opening MAIN RED (a prediction, not a CI red) --
  RECOMMENDED; FG7-92 is the producer and owns the call; (b) a `suspect` section counted in the line.
- F9 what makes a tip green. (a) forge-check's push run required, every other allow-listed run counted when present
  (works in both E13 worlds) -- RECOMMENDED; (b) both required: before placement no tip is ever green.
- F10 job vs test granularity. (a) job-level (the data `run_state` already reads); a red caused only by a known flaky
  test is a red (E22), the fixer sees it through `why` -- RECOMMENDED; (b) test-level from CI junit artifacts
  (a reader per artifact form; later node).
- F11 a root with no `origin/main`. (a) no line, no launch (test roots; a clone of the project always has it) --
  RECOMMENDED; (b) an `unknown` line there too (every tmp-root test of build_context_lines changes).

## §8 Small choices closed by the designer

- Everything in `ci_read.py`, no new module: `ci_read.py` and `journal_lock.py` are already on mechanism_gate's list (M9);
  a new module imported by session_context would widen owns to mechanism_gate.py.
- `main-red` is dispatched in `ci_read.main` before `common.run`, so the shared parser in ci_read_common.py stays.
- `run-name` unchanged (pinned, M8); the run list's event column tells push runs apart.
- Lock name `main-red`, 10 s; `LAUNCH_MIN_S` 300; `NAME_MAX` 60; `LINE_MAX` 300; `FLAKY_ID_MAX` 200.
- Refresh fetches `origin main` itself (timeout 30 s) and falls back to the local ref with `error` recorded.
- One builder card (one API shared by all four files; the test budget fits one node).

## §9 Readers of every touched file (rule 7)

The `owns_readers.py` block was not attached to the brief. The Lead runs
`python -B tools/owns_readers.py --paths tools/ci_read.py tools/session_context.py tools/wave.py .github/workflows/canon.yml --names run_state build_context_lines Wave.finish main --readers`
and the plan critic answers its lines; until then the hand grep below (Grep tool, glob
`{tools/*.py,.githooks/*,.claude/*.json,.claude/agents/*.md,.github/workflows/*.yml}`):
- `canon\.yml`: 35 hits in 6 files (positive control: canon.yml itself, 2 hits). test_workflows.py (13) -- changes in
  this stream (§5 test 7); test_ci_read.py (12, dispatch tests) -- unchanged; ci_read.py (5, `WORKFLOW` and docs) --
  unchanged; nightly.yml (2), dry-story.yml (1) -- comments, unchanged; canon.yml -- changes (.proposed). Sibling
  FG7-91 writes the same file: one concurrency block (D1).
- `ci_read`: wave.py:100-107 `forge_check_state` -> `run_state` -- unchanged (A1); test_quarantine.py:575-664
  (`GithubCI` uses `_open`, `_repo_name`, `split_origin`, `origin_url`, `github_backend`, `REPO_DOOR`) -- unchanged;
  test_wave.py:170 -- unchanged plus §5 test 5; test_ci_read.py -- changes; mechanism_gate.py:271 -- entry unchanged,
  the new import of journal_lock is already listed (293); session_context.py -- now imports ci_read directly (changes
  in this stream; ci_read was already in its closure through test_quarantine).
- `session_context.py|import session_context|wave\.py|import wave`: 107 hits in 39 files. Classes: hook wiring and
  command names (.claude/settings.json, mechanism_gate, owns_gate, hygiene_gate, wiring_check, hook_liveness_probe,
  dispatch_gate, dod_gate, no_reaper_wrap) -- unchanged (no CLI or entry change); importers of session_context
  (compact_snapshot, coordinator_rules, calibration_counts, preflight_quota, worktree_sweep, dod_track, piles_testkit)
  -- unchanged API; tests that run the hook on the real root (test_session_context_wiring, _layer_a, _autoboot,
  test_p4_stdin_deadline, test_hook_liveness_probe) -- a clone gains the MAIN line and a detached launch: the builder
  greps them for whole-output pins and reports (CI judges them); test_wave.py -- §5 test 5.
- New carrier `<git common dir>/main-red/state.json`: readers session_context and the CLI only (this stream).
Known misses of the hand grep: dynamic imports by string, docs/ and plans/ prose.

## Reading trail

- plans/piles/forge/batch-7-vhodyashchie-4.md lines 113-119 (rows FG7-88..FG7-94).
- tools/ci_read.py lines 1-54, 160-209, 254-315, 339-419.
- .github/workflows/canon.yml lines 1-86; forge-check.yml lines 1-40 plus Grep of `if:|EVENT_NAME|CANON_REF|ref:`;
  nightly.yml and all workflows Grep of triggers / `ref:`.
- tools/wave.py lines 1-140, 560-689; tools/session_context.py lines 38-67, 1948-1997, 2405-2452 plus Grep of defs.
- tools/test_ci_read.py lines 800-851; tools/test_workflows.py Grep of canon + lines 325-338;
  tools/test_session_context.py Grep of test names; tools/test_quarantine.py lines 575-664;
  tools/mechanism_gate.py lines 240-284 plus Grep; PROJECT.md line 231-235; docs/TESTING.md lines 75-114, 213-242.
- Grep `flaky|CX1-20|test_detector_verdict` (repo, case-insensitive): no flaky registry in tools/ besides the quarantine
  verdict `flaky` (test_quarantine.py:58, a different domain: quarantined files) -- noticed analog, not reused.

## §10 Lead decisions (18.11)

F0 (a) a sibling `main_push_jobs`, `run_state` untouched; F1 (a) cancel-in-progress false on main, true elsewhere, and
(c) forge-check.yml takes the same expression in this node's builder card, after FG7-90 merges (forge-check.yml is then on
main; this builder edits its `.proposed` copy); F2 (a); F3 (b); F4 (a) plus (b): an open fixer continues on the flaky
queue, and while main is green with a non-empty flaky queue and no fixer the line reads `MAIN GREEN, flaky queue <n>:
no fixer` so the Lead opens one (owner's word 18.11: the known flaky reds are fixed too); F5 (a); F6 (a); F7 (a), a fixer
dispatch carries `node: forge/7/FG7-94` until the Lead adds a standing pile row at acceptance; F8 (a); F9 (a); F10 (a);
F11 (a). Order: the builder starts after FG7-90 and FG7-91 merge (ci_read.py, canon.yml and forge-check.yml are shared).
