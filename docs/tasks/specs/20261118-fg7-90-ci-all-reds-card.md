# FG7-90 -- every CI check runs after a red neighbour; ci_read lists every failed step (draft card, t-1450)

Status: DRAFT by designer for the Lead. Forks F1-F7 are returned, not decided. Pile row: `plans/piles/forge/batch-7-vhodyashchie-4.md:115`.
Owner's word 18.11 (brief t-1450): even after one check fails, every other check must still run, so one CI round shows every red.
Capacity direction (brief): prefer the form that adds no queue slots (row FG7-91, pile :116, measured 18.11: 8-20 jobs a run, queue
wait per job up to 446-870 s, canon 136 runs that day, median 28 min).

## 1. Scope, package invariants, variety

- Touched: `.github/workflows/forge-check.yml` (as `.proposed`), `.github/workflows/dry-story.yml` (as `.proposed`, only if F6 = a),
  `.github/workflows/nightly.yml` (as `.proposed`, only if F2 = b), `tools/ci_read.py`, `tools/test_ci_read.py`, `tools/test_workflows.py`.
- No file under `ai-packages/qa-factory/` is created or changed (package-fast only RUNS package scripts; their command lines stay
  byte-identical). AR-n walk and AR-29 owner/census lines: not applicable (rule 1 binds specs that touch the package).
- `variety: none -- the spec touches no package file and adds no language/project/case branch`.
- One road (rule 6): the predicate "this step failed" is ONE function in `ci_read.py`, read by `jobs` and `why` alike (today `why`
  carries it inline at `ci_read.py:303`); the always-run form is ONE condition shape on every check step of every job it covers.

## 2. Today: which steps hide later checks (enumeration, line numbers of the live files)

Mechanism: a step's `if:` without a status function is `success() && ...` (GitHub default), so the first red step skips every
later step of its job; a multi-command `run:` runs under `bash -e` (critic t-1443 F6 measured `bash -e {0}` for a step with no
`shell:`; `docs/tasks/specs/reviews/t-1443-rd1-37s3-fg7-78b2b3-code.md:120`), so the first red command skips the rest of the step.

| file / job | setup steps (keep default) | check steps hidden by an earlier red | today |
|---|---|---|---|
| forge-check.yml / `forge-check` (:40-119) | :44 checkout, :48 setup-python, :51 deps, :54 git setup, :60-67 `base` (id :61) | :68 lint_ratchet, :69 dup_ratchet, :70 language_sites, :74 journal, :78 feature attribution, :82 escape_check, :83 factory_rules_index, :84 architecture_index, :85 agents_md, :86 piles, :92 install parity (PR), :97 install parity (push, canon), :101 `pytest tools/`, :102 measurers, :104 scoreboard norms | 15 checks in sequence; a red at :68 hides the other 14 (the pair :92/:97 runs one per event) |
| forge-check.yml / `package-fast` (:193-225) | :202 checkout, :206 setup-python, :209 pip, :210 git config (no id today) | :215 `--contracts`, :216 test_audit_rules, :217 `--fast --jobs 4`, :219 audit_factory `--agents` | a red `--contracts` hides 3 |
| forge-check.yml / `package-fast` job level | `needs: changes` (:194) | the whole job, when `changes` (:176) fails | input absent, not a hidden check (E7) |
| nightly.yml / `package-full-report` (:156-186) | -- | the whole job: `needs: package-full` (:159), comment :157-158 "Needs both shards green" | any red shard hides the drift report -> F2 |
| dry-story.yml / `tables` (:78-100) | :83-93 | ONE step, four commands :97-100 under `bash -e` | a red `dry_exits.py --check` hides 3 -> F6 |

Already independent (no change): nightly `package-full` one check step :106 (`dup_ratchet --report ... || echo` :110 is a measurement,
`selftest ... || rc=1; exit $rc` :113-115), shards `fail-fast: false` :87; `install-smoke` one check :141; `quarantine-check` one
check :249; dry-story `parts` `fail-fast: false` (dry-story.yml:58); forge-check `min-python-compile` one step that already prints
every failing file (:165-173); `runner-facts` a probe (`continue-on-error: true` :127); canon `checks`/`full` are separate jobs
(canon.yml:51-64), `clock` `always()` (:73). Measurements out of scope: crap-measure (`continue-on-error` nightly.yml:193),
test-redundancy (:259, `|| true`), quarantine-watch.yml (`continue-on-error` :56, :98).

## 3. Chosen form (recommended; F1) and its cost

Step-level condition, no new job. Every CHECK step (a step after the job's setup marker, other than a `uses:` artifact step) carries
exactly:

    if: ${{ !cancelled() && steps.<marker>.conclusion == 'success' }}

- marker: `forge-check` job -> `base` (exists, :61); `package-fast` -> a new `id: setup` on the git config step (:210); dry-story
  `tables` (F6 = a) -> a new `id: setup` on its git config step (:90). The marker is the LAST setup step; it runs only when every
  setup step before it succeeded (default `success()`), so `conclusion == 'success'` of the marker = all setup succeeded.
- install parity pair: `${{ !cancelled() && steps.base.conclusion == 'success' && github.event_name == 'pull_request' }}` and the same
  with `!=`; the `env:` and run strings stay byte-identical.
- `!cancelled()` (= `success() || failure()`, the row's own text) and NOT `always()`: a cancelled run (concurrency
  `cancel-in-progress: true`, forge-check.yml:26-28; the premise of FG7-91/FG7-94) starts no further check.
- No `continue-on-error` and no `|| true` on a check step: a red check keeps the step, the job and the run red.
- setup steps keep no `if:`; the upload-artifact step keeps `if: always()` (:115).
- YAML: an `if:` that begins with `!` must be wrapped in `${{ }}` (a bare `!` is a YAML tag).

Cost (one metric each):
- Queue slots: +0 per run (same jobs). Split jobs (F1 b) would add one slot per new job per run; each slot waited up to 446-870 s on
  18.11 (FG7-91 row), and each new job re-pays checkout (`fetch-depth: 0`), setup-python and pip install.
- Runner minutes, green run: +0 (the same steps run). Red run: the job runs to its end instead of stopping at the first red, so a red
  run costs at most the green-run minutes of that job (bounded by `timeout-minutes` 40 forge-check :42, 30 package-fast :197).
  Today each hidden red costs another whole round (queue wait + canon median 28 min, FG7-91 row). Step durations are `estimate, not
  verified`: the Lead measures one green canon run with
  `gh api repos/{owner}/{repo}/actions/runs/<id>/jobs --jq '.jobs[] | select(.name|test("forge-check")) | .steps[] | [.name,.started_at,.completed_at] | @tsv'`.

## 4. ci_read change

- New pure helper `failed_steps(job) -> list[dict]`: the dict entries of `job["steps"]` (absent, None, a non-list, non-dict entries
  -> skipped, never raises) whose `conclusion` is in `FAILED` (`ci_read.py:71`), in the API order.
- `why_job` (`ci_read.py:292-313`) reads its step list through it instead of the inline filter at :303; output byte-identical.
- `cmd_jobs` (`ci_read.py:217-219`): after each job line (format unchanged: `<id> <name> <state>`), one line per failed step:
  `  step <number> <name> <conclusion>` (two spaces, remote text through `emit`/sanitize). A COMPLETED job whose conclusion is in
  `FAILED` but whose steps show none: one line `  no failed step recorded (job <conclusion>)` (own words, `emit_own`). A job that is
  green, skipped, queued or in progress with no failed step: no extra line (the existing `test_jobs_path_and_output` output stays
  byte-identical). An in-progress job WITH a failed step lists it (new world: a check can be red while the job still runs) and its job
  line still says `in_progress`.
- Module docstring line 5 gains: "under each job, every failed step". `run_state` (`ci_read.py:394`) unchanged (F3).

## 5. Edges and their invariants

- E1 setup fails (checkout, setup-python, deps, git setup, base, pip): the marker is skipped -> every check is skipped -> ONE red (the
  setup step). Invariant: a check never runs without its input, so no second misleading red.
- E2 a check fails: every later check still runs; the job and the run end `failure`. Invariant: a red check stays red (no
  `continue-on-error`, no `|| true`, no exit-0 wrapper on a check step).
- E3 the run is cancelled (cancel-in-progress, a manual cancel): no further check starts. Invariant: a superseded run frees its runner.
- E4 job timeout: `estimate, not verified` that GitHub cancels the remaining steps (`cancelled()` true); either way the job is
  `timed_out` = red. Invariant: red stays red. Measured only when it happens (no probe spent on it).
- E5 install parity: exactly one of the pair runs per event, as today. Invariant: event branching unchanged.
- E6 two or more checks red in one job: `ci_read jobs` lists every one; `why` prints every one with its section (it already loops,
  :303); `step_section` finds a later step by name or ordinal (`ci_read_common.py:129-148`: steps after a red now open groups, they
  are no longer `skipped`). Invariant: no red step is silently dropped from either listing.
- E7 `changes` job fails: package-fast is skipped by `needs` (:194). Behaviour unchanged: `changes` is itself red, the skipped job is
  input-absent, not a second red. Invariant: same as E1.
- E8 ci_read input (a host answer = outside input): steps absent / None / a string / entries not dicts -> no step lines, exit 0;
  100 jobs (per_page cap, existing) each with many steps -> every failed step printed, no new limit; non-ASCII and control/`##[`
  text in step names -> sanitized like every remote line. Invariant: a red job never prints as if nothing failed (the
  `no failed step recorded` line).
- E9 TEMPORAL: before the Lead places the `.proposed` files the live workflows are the old ones; runs made with them show one
  failed step per job, and the new `jobs` prints exactly that one (no world detection needed in ci_read). The new test_workflows
  rows are red against the old live files until placement; placement happens on the branch before merge (F7), so main never
  carries the new pins with the old files.
- E10 POSITIONAL: the condition goes on every step AFTER the marker and on none before it. Invariant: nothing after a failed setup
  runs except the existing `if: always()` artifact upload; nothing after a red check is skipped.
- E11 a check that changes the tree for the next one: the order is unchanged, so any such interaction already exists in a green run;
  `forge_metrics.py` writes `plans/forge-metrics.md` only with `--write` (`tools/forge_metrics.py:26`). Other tools: `estimate`.

## 6. Forks (returned, not decided)

- F1 FORM. (a) step-level `!cancelled() && marker` on one job (recommended: +0 queue slots, +0 minutes on green; the brief prefers
  it); (b) split forge-check into jobs (each check or 2-3 groups): +1 slot per new job per run and repeated setup, and order inside a
  group still hides; (c) hybrid (a) + split `pytest tools/` out for wall time: +1 slot. Recommendation: (a).
- F2 package-full-report after a red shard. (a) keep `needs: package-full` green-only (recommended for THIS node): its input is the
  durations of a whole run; a shard that crashed or timed out leaves a partial output and the drift diff would print a second,
  misleading red (the brief's edge). (b) `if: ${{ !cancelled() && needs.package-full.result != 'skipped' }}` plus a guard that a
  joined output with a missing or unfinished shard prints `drift not measured: shard <n> output incomplete` and exits 0; needs a
  measured "shard finished" marker in the selftest output (unknown today, `estimate`), nightly.yml joins owns. (a) departs from the
  owner's literal word for one job -> the Lead takes it to the owner.
- F3 `run_state` failed STEPS. (a) unchanged here; FG7-94 (pile :119, "MAIN RED ... <failed checks>") extends it through
  `failed_steps` (recommended: FG7-94 owns `ci_read.py` and its consumer `wave.py`); (b) return `job/step` names now: changes the
  data of `wave.py:100-104` in this node.
- F4 `why` volume: with every check running, one job may show many red steps, each with `--tail` lines (default 60, cap 500), at most
  3 jobs (`WHY_MAX_JOBS` :72). (a) no new cap (recommended: `jobs` is the cheap list, `why --tail 5` the cheap read); (b) a total
  line cap for `why`.
- F5 "one summary of every red at the end" (row). (c) the summary IS `ci_read.py jobs <run>`: every failed step of every job in one
  call, the reader the sessions use (recommended: covers all jobs, 0 runner seconds, no ids on ~20 steps); (a) an inline summary step
  per job reading `toJSON(steps)` (needs an `id` on every check step, two copies of one script = two roads, per job only);
  (b) a token-free `ci_read.py summary` subcommand called from each job (one road, but `ci_read` would serve a CI step without a
  token or backend).
- F6 dry-story `tables` (dry-story.yml:94-100), same class, not in the row's owns. (a) widen owns: split into four steps with the
  same condition and a marker `id: setup` on :90 (recommended: rule 2, a defect in the node's reach is fixed by the card; +0 slots);
  (b) leave it and offer a pile row.
- F7 witness before placement (workflows are enforcement files, `.proposed`, Lead places). (a) the builder byte-copies each
  `.proposed` over its live name in ITS worktree, runs the DoD, restores from the copy and reports the sha256 equality (probe rule,
  CLAUDE.md hygiene pt 7); commits only `.proposed` + tools/ files; the Lead places and reruns the same command (recommended,
  precedent FG7-78: `driver-golden.yml.proposed`, card `20261118-fg7-78-driver-golden-coverage-card.md:151-155`); (b) test_workflows
  judges `<name>.proposed` when present: a second world detector in the test.

## 7. Small choices closed by the designer

- `!cancelled()` spelled that way, not `success() || failure()` (same truth table, shorter).
- marker id `setup` for package-fast and dry-story tables; forge-check keeps `base`.
- `jobs` step line form `  step <number> <name> <conclusion>` mirrors `why` (:306).
- `.proposed` files sit next to the live file in `.github/workflows/` (precedent FG7-78); `test_workflows.NAMES` (:29) ignores them.

## 8. Builder card (assuming F1 a, F2 a, F3 a, F4 a, F5 c, F6 a, F7 a; the Lead edits after its decisions)

given: C:/QAFactory/forge-repo/docs/tasks/specs/20261118-fg7-90-ci-all-reds-card.md (this card, §2-§5), C:/QAFactory/forge-repo/.github/workflows/forge-check.yml, C:/QAFactory/forge-repo/.github/workflows/dry-story.yml, C:/QAFactory/forge-repo/tools/ci_read.py::cmd_jobs, C:/QAFactory/forge-repo/tools/ci_read.py::why_job, C:/QAFactory/forge-repo/tools/ci_read_common.py::step_section, C:/QAFactory/forge-repo/tools/test_workflows.py, C:/QAFactory/forge-repo/tools/test_ci_read.py
owns:
C:/QAFactory/forge-repo/.github/workflows/forge-check.yml.proposed
C:/QAFactory/forge-repo/.github/workflows/dry-story.yml.proposed
C:/QAFactory/forge-repo/tools/ci_read.py
C:/QAFactory/forge-repo/tools/test_ci_read.py
C:/QAFactory/forge-repo/tools/test_workflows.py
non-goals: no edit of a live workflow file (Lead places); no new job; nightly.yml, canon.yml, quarantine-watch.yml unchanged; `run_state` unchanged; no package file; no in-workflow summary step
handoff: builder report (path from dispatch_new.py) + the two `.proposed` files + the sha256 restore witness of F7 (a)
edges: §5 E1-E11 of the card, each with its invariant; positional E10 and temporal E9 are binding
DoD: with both `.proposed` byte-copied over their live names in the worktree (copy taken first, restored after, sha256 equal): `python -m pytest tools/test_workflows.py tools/test_ci_read.py -q`
siblings: nightly.yml package-full `fail-fast: false` (:87); dry-story parts `fail-fast: false` (:58); canon clock `always()` (canon.yml:73); FG7-91 and FG7-94 build on this node (pile :116, :119)
designer: C:/QAFactory/forge-repo/docs/tasks/specs/20261118-fg7-90-ci-all-reds-card.md

Acceptance criteria:
- A1 every check step of forge-check (:68-113), package-fast (:215-225) and dry-story tables (four steps) carries exactly the §3
  condition with its marker; no setup step carries an `if:`; no check step carries `continue-on-error` or a run ending `|| true`.
- A2 the install parity pair keeps its event split and env, inside the combined condition.
- A3 run strings of every existing step byte-identical (FORGE_CHECK_RUNS :140-162 stays green unchanged; the four dry-story
  commands keep their text, one per step).
- A4 `ci_read.py jobs` prints the §4 lines; `why` output unchanged for every existing test; `failed_steps` is the one predicate both read.
- A5 `python -B -c "import sys,yaml;[yaml.safe_load(open(p,encoding='utf-8')) for p in sys.argv[1:]]" <both .proposed>` exits 0.

test: (one per behaviour, strongest first; a new case is a row)
1. test_workflows.py -- `hidden_checks(job, marker)` (pure, in the test file) + one parametrized test: rows real forge-check/`base`,
   real package-fast/`setup`, real dry-story tables/`setup` -> `[]`; mutated copies, each named by the function: a check without
   the condition; the condition with `always()` instead of `!cancelled()`; the condition without the marker; `continue-on-error:
   true` on a check; a check run ending `|| true`; a setup step carrying `!cancelled()`; the marker id absent -> `no marker <id>`.
2. test_ci_read.py -- one parametrized `jobs` test (E8): two failed steps among success/skipped -> both, API order; green job -> job
   line only; in-progress job with a failed step -> listed, job line `in_progress`; completed `timed_out` job whose steps show
   `cancelled` -> `no failed step recorded (job timed_out)`; steps absent / None / a string / a non-dict entry -> job line only,
   exit 0; a step name with `##[error]` and a control char -> sanitized.
3. test_ci_read.py -- `why` row: a job with failures at steps 3 and 5 and a success at 4 (every group present) -> both step lines and
   both sections, step 5's section found by its ordinal (E6).
4. test_workflows.py -- the existing `test_install_parity_has_two_branches...` (:188-196) rewritten: the event test inside the
   combined `if`, plus the always-run condition, env unchanged (A2).

## 9. Readers of every touched file (rule 7)

The `owns_readers.py` block was NOT attached to the brief. Hand grep below; the Lead runs
`python -B tools/owns_readers.py --paths .github/workflows/forge-check.yml .github/workflows/dry-story.yml tools/ci_read.py --names cmd_jobs why_job failed_steps --readers`
and the plan critic answers its lines (Q13 (d)).

- forge-check.yml: `tools/test_workflows.py` (changes in this node); `canon.yml:54` calls it (`workflow_call`, inputs unchanged ->
  unchanged); `tools/test_test_quarantine.py:1867,1887` name it as a run path in fixtures (unchanged); `tools/owns_readers.json`
  (registry mention, unchanged).
- dry-story.yml: `nightly.yml:77` and `canon.yml:68` call it (inputs unchanged -> unchanged); `tools/test_workflows.py:341,352`
  (changes in this node only if a pin reads the tables step; the builder checks).
- `ci_read.py` `cmd_jobs` output: no parser of its stdout in `tools/` (hand grep below); text mentions only:
  `tools/test_quarantine.py:59` (door text), `tools/canon_clock.py:85` (text) -> unchanged. `tools/test_quarantine.py:590-660`
  imports ci_read internals (`token_env_name`, `_open`, `github_backend`, `REPO_DOOR`, `_repo_name`, `split_origin`, `origin_url`)
  -> unchanged names. `tools/wave.py:100-104` reads `run_state` -> unchanged (F3 a), stream FG7-94 later.
- `why_job` output: `tools/test_ci_read.py` only -> unchanged bytes.

## 10. Reading trail (facts with their carrier)

- Lead facts (brief): `grep -n lint_ratchet forge-check.yml` -> :68; `grep -n fail-fast nightly.yml` -> :87; `grep -n '^def run_state'
  tools/ci_read.py` -> :394. All three re-seen by Read.
- Read whole: `.github/workflows/forge-check.yml` (226 lines), `nightly.yml` (296), `canon.yml` (86); `dry-story.yml:22-101`.
- Read: pile rows `batch-7-vhodyashchie-4.md:113-119`; `tools/ci_read.py:1-80`, `:160-414`; `tools/test_workflows.py:1-230`;
  `tools/test_ci_read.py:300-324`, `:640-729`; `tools/test_quarantine.py:585-660`.
- Grep (content): `tools/ci_read.py` `^def |jobs|failed|step` (-i) -> cmd_jobs :217, why_job :292-313, FAILED :71;
  `tools/test_workflows.py` defs -> 50+ lines incl. :169, :188, :215; `tools/test_ci_read.py` `^def test_.*(jobs|why|step|run_state)`
  -> 22 tests; `quarantine-watch.yml` jobs/if/continue-on-error -> :56, :58, :95, :98, :110; `dry-story.yml` -> :53-58;
  `ci_read_common.py` `def step_section` -> :129-148; `forge_metrics.py` `forge-metrics\.md|\.write\(|write_text` (-i) -> :26, :70.
- Readers hand grep: Grep `ci_read(\.py)? jobs|cmd_jobs|ci_read\.run_state|from ci_read import|import ci_read\b` over
  `{tools,.githooks,.claude/agents,.claude/hooks,docs}/**` -> 40 shown (head 40; tools/ hits all inside: wave.py, test_wave.py,
  test_quarantine.py x3, test_ci_read.py x3, ci_read.py x2, canon_clock.py; the rest docs/ history). Workflow readers: Grep
  `forge-check\.yml|nightly\.yml|\.github/workflows` over `{tools,.githooks,.claude/hooks,ai-packages/qa-factory/scripts}/**` -> 9
  files (driver_golden.py hits name driver-golden.yml only).
- Negative with control: `forge-check.yml.proposed|yml.proposed` (-i) over docs/tasks found the FG7-78 card (positive control of the
  `.proposed` precedent). A first search of `\.proposed` limited to `*fg7-27*` found nothing: not used as a claim.
- `estimate, not verified`: step durations (§3 command); job-timeout cancel semantics (E4); whether `test_workflows.py` /
  `test_ci_read.py` sit on a slow-list or `canon_only` list (Grep of their names in `tools/*.json` empty, no same-shape control):
  the Lead confirms before the dispatch gate.

## 11. Lead decisions (18.11)

F1 (a) step-level `!cancelled()` plus the setup marker; F2 (a) package-full-report stays green-only: it is a drift report
over the durations of a whole run, not a check that hides another check, so the owner's word (every check runs after a
failure) holds; F3 (a); F4 (a); F5 (c) the summary is `ci_read.py jobs <run>`; F6 (a) dry-story tables join the owns;
F7 (a) byte-copy witness, the Lead places the `.proposed` files. The builder card of section 8 stands as written.
