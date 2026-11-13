# SC6-2 — test runs per stage, their minutes, and repeats over unchanged inputs — DRAFT SPEC

Status: designer DRAFT for Lead acceptance (13.11.2026). Not a dispatch until accepted. Forks in §6 are returned, none decided.
Source: Lead intent brief (13.11.2026); node row `plans/piles/speed-cost/batch-6-tsena-i-samouluchshenie.md:24`; finding
`plans/piles/speed-cost/findings/20261104-m9-lishnie-zapuski-testov-v-tsene-stadii.md` (read whole); M9 text
`docs/tasks/specs/t-1765-thinking-roles.md:560-563`; P1-v spec `docs/tasks/specs/20261113-p1v-run-scoreboard-spec.md`.

Trees read: `main:` = `.claude/worktrees/read-main/ai-packages/qa-factory/` (origin/main); `p1v:` =
`.claude/worktrees/p1v-n4fix/ai-packages/qa-factory/` (branch wip/p1v-n4fix).

---

## 0. Facts that correct the brief (read first)

| # | Brief / finding says | Carrier says | Consequence |
|---|---|---|---|
| C-1 | Test runs are counted by `run_counters` maybe; settle the overlap | `p1v:scripts/run_counters.py` counts NO test run. Its rows are T1-T10, F1, G1, G2, Q1-Q3, B1, R1r, U1 (`p1v:scripts/run_counters.py:6-8`, the one function `counters` `:570-643`). Grep `(?i)pytest\|npm\|playwright\|test_run\|test run` over the file → 0 matches; positive control, same tool and file, `(?i)friction\|resume` → 45. Its only call into `retro_numbers` is `dispatch_rounds` (`:472-481`). The P1-v spec says so itself: «run_counters does NOT count test runs; SC6-2 stays the survivor; the scoreboard reads `retro_numbers.test_run_counts` later» (`20261113-p1v-run-scoreboard-spec.md:528`) | No second counter, and nothing to read from P1-v. SC6-2 builds on **origin/main** |
| C-2 | `retro-numbers.json` has no test-run counts; M9 is not built (finding «Свидетель», `:19`) | **Part of M9 is already on main, in `retro_numbers.py` (SC2-37), not in run_counters.** `test_run_counts` (`main:scripts/retro_numbers.py:1558-1632`) counts `tests`, `runs` (executed instances), `launches`, `per_test`, `by_purpose`, `by_cause` (why each repeat: `references/test-run-causes.json`). `run_block_metrics` (`:1329-1381`) counts jobs per S5 window and `duplicate_green_executions`. `numbers` writes both into the facts (`:2126-2128`). `render` prints them (`:2611-2620`). The p1v tree carries the same lines at the same numbers (Grep output identical: `p1v:scripts/retro_numbers.py:1558, 1635, 1653, 2126, 2128`) | SC6-2 **extends `test_run_counts`**. What is missing: the split by stage, the duration of each launch, the tests in each launch, the repeat over unchanged inputs per launch, the minutes, and the print beside the stage price |
| C-3 | Carrier: `driver-runs.jsonl` / `events.jsonl` (finding `:11`; t-1765 `:561` «commands in the roles' records») | Test runs are recorded in `work/run-blocks/*.json` and `state/execution-jobs` (`main:scripts/retro_numbers.py:1579-1580`). A block carries `attempt_id`, `attempt_started_at`, `attempt_ended_at`, `dispatch_id`, `purpose`, `input_fingerprint` and `results[]` (writer `main:scripts/run_suite.py:572-582`). `driver-runs.jsonl` holds role, conductor, launched, process and gate_repair rows (by its readers: `p1v:scripts/run_counters.py:576-577, 616, 151-163`). `events.jsonl` is read here only for `dispatch` payloads (`main:scripts/retro_numbers.py:1520-1523`). Both are read by readers only, not by a walk of every writer | The node reads run blocks and jobs, the factory's own record of runs. The brief's carrier is corrected here. Fork F4 covers runs a role starts outside `run_suite` |
| C-4 | (not in brief) | **A reparse block is counted as a second launch.** A reparse keeps the original's `attempt_id`, times, `dispatch_id`, `purpose` and `input_fingerprint`, but takes a new `block_id` (`main:scripts/tests/fixtures/stories/cart-1/work/run-blocks/c7f56259e689c93a9ddf-reparse-a0cb4a33e66f.json:3-14, 78, 87` against `…/20261031T102446900511Z-c7f56259e689c93a9ddf.json:3-19`). `_block_launches` keys a launch by `block_id` (`main:scripts/retro_numbers.py:1463`). The cart-1 fixture has 8 originals and 7 reparse files (Glob), and its retro prints «15 (unscoped: 15)» jobs (`main:scripts/tests/fixtures/stories/cart-1/work/retro-numbers.md:64`). The package's one reader that orders blocks and knows reparses is `run_history.read_run_blocks` (`main:scripts/run_history.py:59-121`) | Unless this is fixed, every reparse reads as a repeat over unchanged inputs with its full duration: the overcount the invariant forbids. Fork F6 |
| C-5 | Equal fingerprint = «no edit between» | `input_fingerprint` is the hash of `source_sha`, `test_content_sha`, `config_sha`, `dependency_sha`, `runtime_sha`, `policy_revision` (`main:scripts/execution_fingerprint.py:144-150`). It is whole-story and coarse: a neighbour edit moves it (`main:scripts/execution_request.py:2140-2142`). It does not hold the data seed, which is recorded separately (`data_seed_contract`, `run_suite.py:577`) | An equal fingerprint proves code, tests, config, dependencies, runtime and policy did not change. Its error falls toward «changed», which is the safe side (§3.3) |
| C-6 | Money: «$» in the output, not in a committed report (finding `:13`); brief: no money number in a repository or report file | `retro.md` is committed to the project and **already carries the story's money**, by the owner's word (30.09, F11), stated at the writer: `main:scripts/retro_numbers.py:2496-2500, 2861-2863`. The stage table prints `Cost` per stage (`:2561-2574`) | The brief and the finding are stricter than the owner's standing exemption. The money question is F2 (how a test run would be priced) and F2's sub-point (where) |
| C-7 | Test home `test_gate_brief_and_retro.py` (batch row) | A keep row, layer `gate_named`, covers `retro_numbers.py` (`main:scripts/tests/test-layers.json:1794-1810`). `test_retro_numbers.py` is also keep (`:4475-4489`, the AR-12 detector), but the unmerged P1-v branch edits it (`p1v:scripts/tests/test_retro_numbers.py`: 26 `run_counters` hits). SC2-37's own test `test_retro_test_runs.py` is in QUARANTINE (`test-layers.json:9446`; quarantine starts `:7067`) | New cases go into `test_gate_brief_and_retro.py`, as the batch row says. That avoids a conflict with P1-v and stays out of the quarantine |
| C-8 | — | Existing pins the new column must keep: `"| Wall time | Machine time |"` (`main:scripts/tests/test_retro_wait_rework.py:142`), `"| Stage | Dispatches"` (`test_retro_task_price.py:309`), `"**Test runs:**"` (`test_retro_test_runs.py:235`, quarantined) | The new column goes AFTER `Machine time`, so both substrings survive |

**The overlap, in two lines.** P1-v (`p1v:scripts/run_counters.py:6-8, 570-643`; spec `:528`) counts no test run, and no counter of
its can be reused. The counter already exists on main in `retro_numbers.test_run_counts` (`:1558-1632`, SC2-37). SC6-2 extends that function on **origin/main**, adding the stage split, the minutes and the repeats over unchanged inputs.

---

## 1. Architecture, rules, owners (designer rule 1)

### 1.1 AR-n touched

| AR | How SC6-2 keeps it | Change check in the DoD |
|---|---|---|
| AR-12 (friction measured; `retro_numbers.py` is a carrier, `architecture.md:127-132`) | The minutes of test launches and their repeats per stage join the retro numbers, the measurement of what a stage cost | DoD key K-1: the stage table cell exists for every stage row |
| AR-13 (one reader per fact, `:161-166`) | Run blocks are read through `run_history.read_run_blocks` (F6 a), jobs through `execution_request.JobStore` (already), controller records through `dispatch_rounds`, times through `moment`. No new `json.loads` or glob of `run-blocks` in `retro_numbers.py` | DoD K-6: after the change, Grep `run-blocks` in `retro_numbers.py` hits only `run_block_metrics` (the queued sibling) and a docstring; positive control: the same Grep hits `run_block_metrics:1338` before the change |
| AR-15 (one survivor, `:175-180`) | `test_run_counts` stays the ONE counter of test runs. run_counters gets none (C-1). `dispatch_rounds` is not changed, because `run_counters` calls it (`p1v:run_counters.py:472-481`) | DoD K-7: `git diff` shows no change inside `dispatch_rounds` |
| AR-22 (every field produced has a reader) | New keys `by_stage` and `launch_rows`. `render` reads `by_stage`. `launch_rows` is read by the retro role through the facts file (SC6-1 charter cites `retro-numbers.json`) and by the scoreboard follow-up (P1-v `:528`) | Test row V13 |
| AR-23 (every list declares its empty outcome) | No carrier → `known: False` → cell `n/a`. Carrier with no launch → `by_stage: {}` → cell `0` | V1, V2 |
| AR-28 (unknown never a pass) | Duration not recorded → `not measured`. Repeat not provable → `not established`. Neither becomes 0 or «no» | V3, V7, V9, V10 |
| AR-29 (code judges data, `:134-157`) | Code reports a FACT: «this launch ran the same tests as an earlier one, over the same inputs». It never says «extra» or «wasteful». That is the retro reader's judgment | §1.3; label fork F3 |
| AR-1 (closed variety is data) | No list of stage names in code. A stage comes from the dispatch record or the dispatch id | V8 |

AR-14, AR-17, AR-24 are not touched: no artifact gets a new writer, no question is asked, and no person's words are read.

### 1.2 FR walk (sections touched)

- A, refusals: n/a. No refusal is added.
- B, text a person reads: the new cell and line are plain words with no field names (FR-6), in the same form as the existing `**Test runs:**` lines.
- C, contracts: the `test_run_counts` output gains keys and keeps every old key, so it stays additive (FR-14). No phrase list and no `reason` prose is read (FR-12). Stage names are not a list in code (FR-13).
- D, identity and evidence: n/a. FR-18 note: a launch count is evidence of execution, and the node never presents it as coverage.
- E, delivery: n/a. The test report is not touched.
- F, measurement: FR-24/FR-25 apply only under F2 (b/c). FR-28: every edge is a test row (§4). FR-41: `not measured` and `not established` are distinct states. FR-51/FR-55 context: a test run is work done by a deterministic tool. Its cost to a stage is wall time and the role's turns around it. A repeat caused by the factory (`by_cause`: `launch_failed`, `factory_defect`) is friction under FR-55. This node gives the minutes and leaves the judgment to the role.
- G, code: English (FR-30), the change goes to the root cause (FR-32), and live proof follows FR-33 (§5, the live-runs row).

### 1.3 Every check the node adds or alters: owner and census class

| Unit | What it does | Census class | Owner it serves | Blocks? |
|---|---|---|---|---|
| repeat predicate (inside `test_run_counts`) | compares two run records: equal test-name set + equal non-empty `input_fingerprint` + equal `data_seed_contract` | not a census unit: it neither refuses nor gates (a counter, like the rest of `test_run_counts`, which has no census row; the only `retro_numbers.py` row is `write_retro`, `judgment-census.json:851`). If the critic labels it anyway: `xref` | data (code) | no |
| «was this repeat wasteful / extra» | — | judgment, never code | the retro reader: the S9 retro role (its `kind: craft` finding with numbers, SC6-1, `batch-6…:23`), accepted by the tier above it (AR-29). In `retro_mode: numbers` the person reads the table | — |

The DoD runs `test_judgment_census.py` to show that no unit was added (census counts only shrink).

---

## 2. The node — SC6-2 (one builder node; files do not force two)

Header lines (CLAUDE.md R11-f):

given: this spec (§0-§4) — inline enumeration below; `ai-packages/qa-factory/design/factory-rules.md` whole; `plans/builder-rules.md`; `ai-packages/qa-factory/scripts/retro_numbers.py` (functions `test_run_counts` :1558-1632, `_block_launches` :1437-1469, `_job_launches` :1472-1507, `_cause_reader` :1510-1555, `test_run_lines` :1653-1684, `render` stage table :2559-2578, `moment` :100-113, `DISPATCH_ID` :236, `dispatch_rounds` :268-310, `clock` :2145-2150); `ai-packages/qa-factory/scripts/run_history.py` (`read_run_blocks` :59-121); `ai-packages/qa-factory/scripts/run_suite.py` (`build_run_block` :469-600, block fields); `ai-packages/qa-factory/scripts/execution_fingerprint.py:144-150`; fixtures `ai-packages/qa-factory/scripts/tests/fixtures/stories/cart-1/work/run-blocks/` (reparse shape, read only); `ai-packages/qa-factory/scripts/tests/test_gate_brief_and_retro.py` (`story` helper, `test_retro_numbers` :886-961 as the model); `ai-packages/qa-factory/scripts/tests/test_retro_test_runs.py` (QUARANTINED: read only, for the job-file shape of variant V11; never run, never edited)
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\retro_numbers.py (test_run_counts, _block_launches, test_run_lines, render — and new private helpers beside them)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_gate_brief_and_retro.py (one new test function with a variant table)
C:\QAFactory\forge-repo\ai-packages\qa-factory\changelog.d\sc6-2-test-runs-by-stage.md
non-goals: `run_block_metrics` (sibling, queued §5); `dispatch_rounds` (run_counters depends on it); `run_counters.py` and anything on wip/p1v-n4fix; `estimate_facts`, `observations`, `factory_dashboard.py`; `references/test-run-causes.json`; `agents/qa-retro-analyst.md` (SC6-1 done); `docs/SIBLING_MAP.md` (Lead); any money figure for a test run (F2 a); reading role transcripts (F4); the quarantined `test_retro_test_runs.py`
handoff: the builder report (builder.md rule 7) with the verbatim witness of the DoD runs, the FR walk lines A-G, the `architecture:` and `judgment:` commit lines, and the full list of numbers that changed on the cart-1 fixture (F6 consequence)
edges: §3 (every edge with its invariant); limits: none introduced (`launch_rows` keeps every launch, nothing is truncated)
DoD: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/retro_numbers.py`, the same for `ai-packages/qa-factory/scripts/tests/test_gate_brief_and_retro.py`, then every file those two print (not quarantined) plus `python -B ai-packages/qa-factory/scripts/tests/test_judgment_census.py` and `python -B ai-packages/qa-factory/scripts/selftest.py --lang`; all green, output pasted verbatim
siblings: `run_block_metrics` counts reparse blocks as jobs (C-4) — queued §5, not fixed here; `run_counters` (P1-v) — reads nothing of this, no change (C-1); P1-v scoreboard follow-up reads `test_run_counts` (spec `:528`) — additive keys keep it valid
designer: <the accepted path of this draft>

### 2.1 What to change (direction chosen; written for the recommended fork options — a different Lead choice changes only the marked lines)

**A. Launch identity: one launch per attempt (F6 a).** In `_block_launches`, read blocks through `run_history.read_run_blocks(task_root)`, with a lazy
import like `execution_request` at `:1592`. Group the items by `item["attempt"]`. A launch is ONE attempt. Its record is the LAST
readable item of that attempt in read order (the deepest reparse), and its `id` is the attempt. Keep every shape check that exists today and apply it to the chosen item. A chosen item that fails a check falls back to the previous item of the same attempt. An attempt with no readable item counts once in `unreadable_blocks`. Files `read_run_blocks` returns as `bad` count in `unreadable_blocks`.
`block_ids` (used by `_job_launches` to skip jobs that have a block) = every attempt id ∪ every item's `block_id`, so a job with a block on disk is never counted twice.
Add to each launch dict: `"ended"` (the item's `attempt_ended_at`, raw), `"fingerprint"` (`input_fingerprint`), and `"seed"`
(`data_seed_contract`). In `_job_launches`, add the same keys from the job: `ended: None`, `fingerprint` = `request.input_fingerprint`, and
`seed` = `request.execution.data_seed_contract`.

**B. Per-launch facts.** In `test_run_counts`, after the launches are sorted (`:1603`), build `launch_rows`, one per launch in that order:
`{"id", "stage", "purpose", "tests", "runs", "seconds", "seconds_why", "repeat", "repeat_of"}`:
- `stage`: the `stage` of the controller dispatch record whose `id` equals the launch's `dispatch_id` (from `dispatch_rounds(task_root)`,
  keyed by id). Else `DISPATCH_ID.match(dispatch_id).group(1)`. Else `"unattributed"`, the word `dispatch_rounds` already uses (`:296`).
- `tests`: the number of named entries. `runs`: the number of entries (the same unit as the existing `runs`).
- `seconds`: `(moment(ended) - moment(started)).total_seconds()` rounded to 1 decimal when both are strings that `moment` reads, both are
  offset-aware or both naive, and the result is ≥ 0. Otherwise `None`, with `seconds_why` exactly one of: `"no end time recorded"` (end
  absent or empty; every job launch), `"no start time recorded"`, `"the time cannot be read"` (unparsable, a non-string, or an aware/naive mix),
  `"ends before it starts"`. `span_seconds` is NOT used, because it clamps a negative to 0 (`:116-120`).
- `repeat` / `repeat_of` (F1 b): let P be the most recent EARLIER launch whose test-name set equals this launch's set (set equality,
  order ignored). `repeat = "yes"`, `repeat_of = P.id` when every entry of both launches is named, both `fingerprint`s are non-empty strings and
  equal, and both `seed`s are equal (two absent seeds count as equal; see §3.3). `repeat = "no"` when no such P exists, or the fingerprints are
  both non-empty and differ, or the seeds differ. `repeat = "not established"` when P exists but either fingerprint is absent or empty, or
  either launch has an unnamed entry. Purpose and status are not consulted: a diagnostic repeat is still a fact for the role to judge.

**C. Per-stage sums.** Add `by_stage`: `{stage: {"launches", "runs", "tests" (distinct named), "seconds" (sum of non-None, 1 decimal),
"not_timed" (launches with seconds None), "repeats" (launches with repeat "yes"), "repeat_seconds" (sum of their non-None seconds),
"repeats_not_timed", "repeats_not_established"}}`, with stages sorted. Add both keys to the `known: True` return. Every old key
keeps its name and meaning. Under F6 (a) the VALUES of `launches`, `runs`, `tests`, `per_test` and `by_cause` change for stories with reparse
blocks, and this is a correction.

**D. Print beside the stage price.** In `render`, append a column `Test runs` after `Machine time`: the header row becomes
`| Stage | Dispatches | Requests | Tokens | Cost | Wall time | Machine time | Test runs |` and the separator gets one more cell. The cell comes from ONE new
helper `test_run_cell(counts, stage) -> str` (one place, so the table and any later reader print the same words):
- `counts` is not a dict, or has no `by_stage` key (a facts file written before SC6-2), or `known` is False → `n/a`.
- the stage has no `by_stage` entry → `0`.
- otherwise `"<L> launch(es), <R> run(s), <time>; repeats over unchanged inputs: <N> (<rtime>)"`. Here `<time>` is `clock(seconds)`, then
  `", <k> not measured"` when `not_timed` > 0. When every launch is untimed, `<time>` is `time not measured`. `<rtime>` follows the same rule over
  the repeats. `", <m> not established"` is appended when `repeats_not_established` > 0. The `<N> (<rtime>)` part is printed even when N is 0. (The label is fork F3.)
- the orchestrator row gets `-` in the new column.
Stages in `by_stage` that have no row in the money table (e.g. `unattributed`) are printed right after the table as one line,
`**Test runs outside the stage table:** <stage>: <cell>; …`. INVARIANT: every launch appears in exactly one printed cell.
In `test_run_lines`, after the sentence, when `known` is true and any launch exists, add one line:
`- money of a test run: not attributed — a run is executed by code, and the role's spend around it is not recorded per call.` (F2 a.)

**E. Changelog fragment** `changelog.d/sc6-2-test-runs-by-stage.md` (English, no Cyrillic): one paragraph. The retro's stage table
names, per stage, the test launches, their minutes and the repeats over unchanged inputs. A reparse of a launch is no longer counted as a
second launch.

---

## 3. Edges, each with the invariant it protects

### 3.1 Data edges

| Edge | Behaviour | Invariant |
|---|---|---|
| Neither `work/run-blocks` nor `state/execution-jobs` exists (an older story or the skill road) — TEMPORAL world 1 | `known: False` as today; cell `n/a` on every stage row; no `by_stage` key | a story with no carrier never reads as «0 runs» |
| A facts file written before SC6-2 is rendered — TEMPORAL world 1 | no `by_stage` key → cell `n/a` | an old file never prints 0 |
| A story run after SC6-2 lands — TEMPORAL world 2 (the node's commit creates the keys) | keys present; cells computed | — |
| Carrier present, no launch at all | `known: True`, `runs: 0`, `by_stage: {}`; every stage cell `0` | finding `:13`: a stage without runs is 0, not «no data» |
| A stage that ran no test while others did | cell `0` | same |
| A launch with no `attempt_ended_at` (an open or killed run), or a job launch | `seconds: None`, `seconds_why` set; counted in `not_timed`; the cell says `<k> not measured` | FR-41: an unknown duration is never 0, and a partial sum is never shown as the whole |
| End before start; aware/naive mix; non-string time | `None` + its why; not clamped | a clock defect never shrinks to «0 s» |
| A reparse block (F6 a) | the same launch; its results replace the original's; never a repeat | a run measured once counts once |
| A reparse chain whose last file is damaged | falls back to the previous readable item; if none, `unreadable_blocks` + 1 | a damaged file never takes the retro down (existing AR-2 note `:1438-1441`) |
| `dispatch_id` absent or unparsable and not in the controller records | stage `unattributed`, printed under the table | every launch is printed once; sum of `by_stage[*].launches` == `launches` |
| A test run by the role outside `run_suite` (raw shell) | not counted (F4); the existing sentence names the carrier | the count is of the factory's recorded runs, and the line says which carrier |
| An imported block (`import_provenance`) or a regression run on someone else's stand | skipped (as `:1452`) | P24: only runs this run made are counted |

### 3.2 Conflicting requirements, decided or forked

- «A stage without runs → 0» (finding) against «a journal without the carrier → n/a» (brief). Both hold: `0` needs a carrier that exists, and `n/a` means
  there is no carrier. Decided as above.
- «Print $ beside the stage price» (batch row, finding) against «no money number in any file» (brief) against «retro.md keeps money» (owner 30.09
  F11, `:2496-2500`). This is fork F2.
- «Code calls them extra» (batch row «лишние запуски») against «code names facts, the role decides what is extra» (finding `:12`, P27). This is fork F3.

### 3.3 The reused function in a more consequential role: the repeat predicate's error direction

`input_fingerprint` equality is used today by the run budget (`execution_request._match` `:2058-2059`) and by `run_block_metrics`
(advice). Here it becomes the fact a retro reader blames time on, so its error direction is fixed:
**it may err toward «no» / «not established» (undercounting repeats). It never errs toward «yes» when any input changed.**
Adversarial inputs that must stay on the safe side, each a variant row in §4:
- both fingerprints `""` or absent → `not established`, never `yes` (empty strings are equal, and equal must not mean «unchanged»);
- the same set, with a launch of that set over a different fingerprint in between → the latest earlier launch decides → `no`;
- a subset (`[a]` after `[a, b]`) → `no`: only set equality counts;
- the same set in another order → `yes`;
- a reparse of the same attempt → not a launch, so never `yes` (F6);
- a different `data_seed_contract` with equal fingerprints → `no`.

Known residual on the unsafe side, stated and not hidden: a data change that is recorded in NEITHER the fingerprint NOR
`data_seed_contract` reads as unchanged. The cell's label says «unchanged inputs». It does not say «nothing changed», and whether a repeat was needed remains the role's call.

---

## 4. Tests — one new function in `test_gate_brief_and_retro.py`, a variant table

`test_sc6_2_test_runs_by_stage_and_repeats()` iterates a list of variant rows. Each row writes run blocks (the minimal shape of
`run_suite.py:572-582`: `block_id`, `attempt_id`, `attempt_started_at`, `attempt_ended_at`, `dispatch_id`, `purpose`, `input_fingerprint`,
`results` with `instance_id`/`status`), plus job files for V11 only and an optional `state/controller.json`, into a temp story. It calls
`retro_numbers.test_run_counts(task_root)` and `test_run_cell` / `render` on a minimal facts dict, and checks the named keys. Every check
message starts with the variant id, so a red line names the case (P16).

| Id | Input | Expected |
|---|---|---|
| V1 | no carrier | `known` False; `test_run_cell(counts, "S5") == "n/a"`; same for a dict without `by_stage` |
| V2 | empty `work/run-blocks/` | `known` True, `by_stage == {}`, cell for S5 `"0"` |
| V3 | one S5 launch, no `attempt_ended_at` | `seconds` None, `seconds_why == "no end time recorded"`, `by_stage["S5"]["not_timed"] == 1`, cell contains `time not measured` |
| V4 | three S5 launches of `{a, b}`, same fingerprint, 60 s each | repeats 2, `repeat_seconds` 120.0, the 2nd's `repeat_of` = the 1st's id, the 3rd's = the 2nd's |
| V5 | as V4, but the fingerprint changes before the 3rd | repeats 1 |
| V6 | V4's first launch plus its reparse file (same attempt) | `launches` 3, not 4; repeats 2 |
| V7 | end before start | `seconds` None, `"ends before it starts"` |
| V8 | `dispatch_id` `"weird"`, no controller record | stage `unattributed`; `render` prints `**Test runs outside the stage table:**`; sum of `by_stage[*].launches` == `launches` |
| V9 | two launches of `{a}`, the second without `input_fingerprint` | `repeat == "not established"`, `repeats_not_established` 1, `repeats` 0 |
| V10 | adversarial: both fingerprints `""`; subset `[a]` after `[a,b]`; reversed order `[b,a]` after `[a,b]`; same fingerprint with a different `data_seed_contract` | not established; no; yes; no |
| V11 | one job launch with no block (job shape as in the quarantined `test_retro_test_runs.py`) | `seconds` None, `"no end time recorded"` |
| V12 | any of the above | no key of `by_stage` or `launch_rows` contains `usd`, `cost`, `price` or `money` (F2 a) |
| V13 | S5 and S7 launches with the controller record giving S7 | `by_stage` keys `["S5", "S7"]`; the `render` header ends `| Machine time | Test runs |`; the S7 row's cell is not `0`; an S4 row (money present, no launch) has cell `0` |

---

## 5. Queued, not done here (rule 9: named)

- **`run_block_metrics` counts reparse blocks as jobs** (C-4; same file, `:1347-1365`). The printed «Test-execution jobs: 15» on cart-1 is
  wrong in the same way. Its test is quarantined (`test_run_execution_metrics.py`, `test-layers.json:9543`). Proposal: a finding in
  `speed-cost` that reads through `read_run_blocks` the same way. The Lead decides whether it joins this node (it fits the owns) or waits.
- `_block_launches` will read through `read_run_blocks` after A. `run_block_metrics` remains a second glob of `run-blocks` (AR-13): same finding.
- The money of a test run (F2 c) depends on P1-v N4b's `friction.call_spans` (spec `:243, 300-302`), which is not on main: a follow-up after N4b.
- The quarantined `test_retro_test_runs.py` pins numbers that F6 (a) may change on fixtures with reparses. Builders never run it (builder-rules 7b).
  The `quarantine-watch` job will show whether it turns red. If it does, the Lead tells the owner (CLAUDE.md rule 11).
- Live proof (FR-33): one row in the `live-runs` pile, «the retro of a real run shows the Test runs column», per PROJECT.md «Командная
  работа» 9.

---

## 6. Forks returned to the Lead

| # | Fork | Options | Consequences | Recommendation |
|---|---|---|---|---|
| F1 | What the code counts as the repeat fact. The finding: «Что считается лишним, решает роль ретро по данным (код называет запуски и повторы одного набора без правки между ними как факт, не как вердикт; P27)» (`findings/…m9…:12`). t-1765 M9 is wider: «повтор без изменения кода, теста или данных между запусками, запуск всего набора там, где менялся один файл, прогон того же теста в S5 и снова в S7 без починки» (`t-1765:562-563`). This leaves room: the unit (launch or test), what «без правки» is measured by, and whether status matters | (a) reuse `run_block_metrics`' rule: same test, same fingerprint as its last GREEN run, purpose initial/repair_verify; unit = execution; per stage. (b) the finding's literal reading at launch level: the same test set, equal fingerprint and seed, status-agnostic (§2.1 B). (c) t-1765's three clauses | (a) is one definition (AR-15), but has no minutes: duration is recorded per launch, not per test, and red repeats are left out. (b) gives minutes and matches «одного набора». It is a launch-level fact beside `run_block_metrics`' execution-level one, so the two need different names (they have them: «re-ran an already-green, unchanged test» vs «repeats over unchanged inputs»). (c) clause 2 («whole suite where one file changed») is open variety, a role's judgment (AR-2, AR-29). Clause 3 is covered by (b) across stages | **(b)**. Clause 3 of (c) is already inside (b) (a cross-stage repeat counts against the later stage). Clause 2 stays with the retro role |
| F2 | The money of a repeat («цена: $/мин») | (a) minutes only. Money is «not attributed», with the reason line. (b) stage cost × (repeat minutes / stage wall minutes), labelled as an estimate. (c) the role's token spend on the turns around the run call, from transcripts (P1-v N4b `call_spans`) | (b) is the wrong model: a role's tokens do not grow while a test runs, so it overstates long suites. It is a figure that only looks measured (FR-41, P18 «one true price»). (c) is right, but its reader is not on main. (a) is honest now | **(a) now, (c) as the follow-up** (§5). Sub-point, only if (b) or (c) is chosen: where the $ goes. `retro.md` already keeps money by the owner's word (`:2496-2500`), but the brief says no money in a file. That would be an owner question |
| F3 | The label of the count | (a) «repeats over unchanged inputs» (a fact). (b) «extra runs / лишние запуски» (the batch row's words) | (b) makes code issue a verdict (AR-29, finding `:12`) | **(a)**. The role writes «extra» in its finding when it judges so (SC6-1 charter) |
| F4 | The carrier: the factory's run records only, or also test commands a role runs in its shell (t-1765 `:561` «команды … в записях ролей») | (a) run blocks + jobs only (one road: every language and framework runs through `run_suite`; an existing reader). (b) also scan role transcripts for test commands | (b) reads open variety (command shapes per language) by pattern: FR-12, and a second road per language (P31). A direct shell run by a role is itself a friction or guard matter. Cost of covering it under (a): one transcript-based count in `friction.py` later (P1-v N4b family). Whether roles CAN run tests outside `run_suite` today is not verified here (estimate) | **(a)**. If the Lead wants the other side covered, it becomes a node in the N4b family with owns and a test, not a line here |
| F6 | Reparse blocks (C-4) | (a) one launch per attempt, read through `run_history.read_run_blocks`; this changes `launches` and `runs` for stories with reparses (cart-1: 15 → 8 launches). (b) leave the totals as they are and collapse only for the new keys. (c) leave both and queue | (b) breaks «`by_stage` sums to the totals». (c) makes every reparse a «repeat over unchanged inputs» with full minutes: an overcount on the forbidden side (§3.3) | **(a)**. `run_block_metrics` is queued (§5), or joins the node if the Lead prefers (same file) |

## 7. Small technical choices closed by the designer

- Test home: `test_gate_brief_and_retro.py` (batch row; C-7: `test_retro_numbers.py` collides with the unmerged P1-v branch).
- Base: **origin/main**. The node needs nothing from wip/p1v-n4fix, and P1-v does not edit `retro_numbers.py` (P1-v spec `:530`; the test-run lines sit at identical numbers in both trees). Not done here: a full file diff of `retro_numbers.py` between the trees (this role runs no shell). The merge of whichever lands second is ordinary.
- Stage of a launch: controller record first, then the dispatch id, then `unattributed`. This is the same order and the same word as `dispatch_rounds:296`, and it reuses `dispatch_rounds` without changing it.
- Stages are not filtered to S5-S7. Every stage that launched is shown, so that no run is hidden. In practice runs occur in S5-S7.
- Duration comes from block times only. A job's `created_at`/`updated_at` is not a run's duration. The summary's `duration_s` would be a second carrier.
- No `observations()` line. The stage table carries the fact, and the role or the person judges it.
- `launch_rows` is not printed (JSON only, no truncation).

## 8. Reading trail

- `plans/piles/speed-cost/batch-6-tsena-i-samouluchshenie.md` whole; `plans/piles/speed-cost/findings/20261104-m9-lishnie-zapuski-testov-v-tsene-stadii.md` whole.
- `docs/tasks/specs/t-1765-thinking-roles.md` Grep `M9` → `:560-563`.
- `docs/tasks/specs/20261113-p1v-run-scoreboard-spec.md` `:1-337`, `:505-544`; Grep `(?i)test run|pytest|npm test|playwright|M9|SC6|test_runs|tests_run` → `:94`, `:528` only.
- `p1v:scripts/run_counters.py` whole (711 lines); Grep negative + control (C-1); `p1v:scripts/retro_numbers.py` Grep test-run names; `p1v:scripts/tests/` Grep `run_counters` → `test_retro_numbers.py` 26, `test-layers.json` 1.
- `main:scripts/retro_numbers.py` `:96-120`, `:230-310`, `:1329-1685`, `:1889-1916`, `:1956-2138`, `:2489-2627`, `:2704-2867`; Grep `^def ` index.
- `main:references/test-run-causes.json` whole; `main:scripts/run_suite.py:469-593`; `main:scripts/run_history.py:50-139`; `main:scripts/execution_request.py:2040-2079, 2130-2160, 2345-2362`, Grep fingerprint; `main:scripts/execution_fingerprint.py` Grep → `:142-150`.
- `main:scripts/tests/test-layers.json` `:1790-1814`, `:4472-4491`, Grep keep/quarantine rows; `main:scripts/tests/test_retro_numbers.py:1-80` + Grep; `main:scripts/tests/test_gate_brief_and_retro.py` Grep + `:886-961`; Grep `| Stage |` pins over the package.
- cart-1 fixtures: Glob of run-blocks, reparse files; Grep of two block headers.
- `main:design/architecture.md:127-181`; `main:scripts/tests/fixtures/judgment-census.json` Grep `retro_numbers` → `:851`.
- `plans/builder-rules.md` 7b.
