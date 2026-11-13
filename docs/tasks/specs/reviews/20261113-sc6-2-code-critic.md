# SC6-2 code critic: test launches per stage, their minutes, and repeats over unchanged inputs

Diff: worktree `.claude/worktrees/sc6-2`, branch wip/sc6-2, commit 5dc3e88 over base 7cf8c34.
Spec / DoD: `docs/tasks/specs/20261113-sc6-2-extra-test-runs-spec.md` (§2, §2.1, §3; forks F1 b, F2 a, F3 a, F4 a, F6 a).
Builder report: `.claude/worktrees/sc6-2/docs/tasks/specs/reports/20261113-sc6-2-report.md`.
Reviewer: critic (Opus), 13.11.2026.

**Verdict: fit_with_fixes. One blocking finding (B1) to fix in this round; four non-blocking findings (N1-N4); one decision for the Lead (L1).**
This verdict is input to acceptance. The decision to accept belongs to the Lead.

I started with empirics, as the brief asks for a numeric diff. Every number below comes from a run I made myself and is pasted verbatim. I read the code only where a run diverged or where no deterministic check exists (the repeat predicate's error direction, §3.3).

---

## Findings

### B1 (blocking): a reparse drops the data seed, so two attempts over DIFFERENT seeds read as a repeat "yes", the side the spec forbids

- **Where.** `retro_numbers.py:1491` takes `"seed": block.get("data_seed_contract")` from the CHOSEN item, which is the deepest reparse. The writer, `run_suite.py:792` (`reparse_run_block`), builds the reparse request with `"execution": {"repo_id": ...}` only. `build_run_block` reads the seed from `request.execution.data_seed_contract` (`run_suite.py:486`) and writes `"data_seed_contract": data_seed or None` (`:577`). So **every reparse block carries `data_seed_contract: null`**, whatever the original had. The spec's premise C-4 lists what a reparse keeps: attempt, times, dispatch, purpose, fingerprint. The seed is not on that list, and it is not kept.
- **Failure (probe P2, verbatim below).** Attempt aaa has seed `{"seed":"one"}` and attempt bbb has seed `{"seed":"two"}`. Both have fingerprint F1 and test set {t_a}, and each attempt is reparsed once. Result: `('bbb', 'yes', 'aaa')`. Without the reparses (P1) the same two attempts give `('bbb', 'no', None)`. Spec §3.3: "It never errs toward «yes» when any input changed", and the adversarial row "a different data_seed_contract with equal fingerprints → no". The variant table misses this because V6's reparse carries the same (absent) seed as its original.
- **The mirror case.** A reparsed attempt (seed None) followed by a non-reparsed attempt over the SAME seed gives "no" because the seeds differ. That is the safe side, but it is still a wrong fact.
- **Surface: the launch-identity fields of a collapsed reparse chain.** Neighbouring classes I walked:
  - `input_fingerprint`: kept by the writer (`run_suite.py:790`). Safe.
  - `attempt_started_at` / `attempt_ended_at`: kept (`:770`, via `started_at`/`ended_at`). Safe; confirmed on the cart-1 reparse files, whose times equal their originals'.
  - `dispatch_id`, `purpose`: kept (`:789`). Safe.
  - `import_provenance`: NOT kept. That is N1.
  - `selection_provenance`: not kept, but not read by this diff.
- **Fix.** In `_block_launches`, take the launch's identity fields (`seed`, and for robustness `fingerprint`, `start_raw`, `ended`, `dispatch_id`, `purpose`) from the attempt's ORIGINAL item: `depth == 0`, or the first item of the chain in `read_run_blocks` order. Take only `results` / `execution_status` from the deepest readable item. Add a variant row V6b: two attempts with different seeds and equal fingerprints, each with a reparse whose seed is null → `repeat == "no"`.
- **Writer sibling.** `reparse_run_block` should carry `data_seed_contract` the way it carries the fingerprint. That file is outside this node's owns, so it goes in the queue (see Class completeness).

### N1: an imported attempt's reparse is counted as a launch (P24)

- The reparse writer does not copy `import_provenance`. A chain [imported original, its reparse] therefore picks the reparse, `_block_verdict` returns `ok`, and the attempt is counted as one launch of this run.
- Probe P3 (verbatim below): `launches 1`, row `('external-1', 'no', None)`.
- The base code counted it too (as the reparse block), so this is no regression. But the spec §3.1 edge says imported blocks are skipped (P24), and decision 3 in the report covers only an import as the LAST item.
- **Fix (same function, cheap).** Skip the attempt when ANY item of its chain carries `import_provenance`. Add a variant row.

### N2: `unreadable_blocks` drifts from what its reader prints

- `retro_numbers.py:1483` adds 1 only when every item of the chain is shape-damaged, and adds that 1 once per attempt.
- The reader at `:1817` prints "N run block files could not be read", and the docstring at `:1593` says "counts run blocks whose shape is damaged".
- Two cases now print the wrong thing:
  - (a) a damaged reparse whose original is readable is counted nowhere: the damaged file disappears silently;
  - (b) an attempt with two damaged files prints "1 run block file".
- The spec prescribed "counts once", so the builder followed the spec. The drift sits where the spec meets the existing reader. **Fork for the Lead (L1-b):**
  - count damaged FILES (`unreadable += damaged`, still never a second launch). This keeps the reader's word. Recommended.
  - or keep the per-attempt count and change the sentence to "attempts".

### N3: code quality

- **Two fields for one fact.** The launch dict keeps both `started` (str-coerced, used for sorting) and `start_raw` (used for timing) at `:1489` and `:1531`.
- **Purpose read twice.** The purpose is derived twice: in `_block_verdict` and again in the launch dict.
- **Duplicate literal set (pre-existing).** `run_block_metrics` still spells out the purpose set that `_BLOCK_RUN_PURPOSES` (`:1389`) already names.
- **Fix.** These can ride along in the B1 fix. They do not block.

### N4: per-launch rounding drift in the stage sum

- `by_stage.seconds` sums durations that were already rounded to one decimal. On cart-1 S5 the sum prints 134.4 s, while the raw sum is 134.307 s.
- This is consistent with `launch_rows`, which the spec asks for, so it is not a defect. I record it only so the "control values" below are not misread.

### L1: Lead decision, the sibling `run_block_metrics` (question 6)

- **The retro contradicts itself today, on any story with reparses.** The new stage table and `**Test runs:**` say 8 launches / 42 runs on cart-1, while the line rendered from `run_block_metrics` says "Test-execution jobs: 15 (unscoped: 15) · 80 test executions" (committed fixture `cart-1/work/retro-numbers.md:64`, `retro.md:56`; the function is unchanged by this diff, so it still yields 15/80). That is one packet contradicting itself (FR-10).
- **The "queue line" has no carrier.** Spec §5 names it only as a "proposal". `Grep -i run_block_metrics` over `plans/` (in the worktree) finds only CD1-34, which is a different defect (damaged `results`). No finding file and no node for the reparse overcount exists. Per rule 9 that is a known sibling left unqueued.
- **Recommendation.** Fold it into this node's fix round: same file, same reader (`read_run_blocks`, one launch per attempt), and its owns line widened by the Lead. Otherwise, before acceptance, open the finding plus its node row in an un-taken speed-cost batch (D-0044). The decision belongs to the Lead.

---

## Q1: control values, recounted by hand

**Script, full source.** It reads the JSON directly and does not import `retro_numbers`. Path: `C:\Users\i_mas\AppData\Local\Temp\claude\b3e3188b390a00d9\61b75a79-16bf-492f-9cd2-02266607001d\scratchpad\hand.py`.

```python
import json, sys, glob, os
root = sys.argv[1]
print("BLOCKS")
for p in sorted(glob.glob(os.path.join(root, "work/run-blocks/*.json"))):
    d = json.load(open(p, encoding="utf-8-sig"))
    res = d.get("results") or []
    names = [r.get("instance_id") for r in res if isinstance(r, dict)]
    print(os.path.basename(p)[:44], "| att", (d.get("attempt_id") or "")[:20], "| blk", (d.get("block_id") or "")[:34],
          "| purp", d.get("purpose"), "| disp", d.get("dispatch_id"), "| st", d.get("attempt_started_at"), "| en", d.get("attempt_ended_at"),
          "| fp", (d.get("input_fingerprint") or "")[:10], "| seed", d.get("data_seed_contract"), "| imp", bool(d.get("import_provenance")),
          "| n", len(names), "| status", d.get("execution_status"), "| reparse_of", d.get("reparse_of"), d.get("supersedes_block_id"))
print("JOBS")
for p in sorted(glob.glob(os.path.join(root, "state/execution-jobs/*.json"))):
    d = json.load(open(p, encoding="utf-8-sig"))
    r = d.get("request") or {}
    print(os.path.basename(p)[:12], "| job", d.get("job_id"), "| state", d.get("state"), "| purp", r.get("purpose"), "| disp", r.get("dispatch_id"))
```

**Raw facts on cart-1.** The fixture has 15 block files. 8 are originals, each its own attempt. The other 7 are reparses, which keep the `attempt_id`, the times, the dispatch and the fingerprint of their original:

| attempt | reparses | dispatch | n | fp | duration |
|---|---|---|---|---|---|
| 446b57… | 1 | S5-qa-automator-2 | 12 | 265c… | 24.75 s |
| 6b183c… | 0 | S5-qa-automator-3 | 4 | fc5c… | 27.68 s |
| d67215… | 1 | S5-qa-automator-3 | 4 | c6a5… | 16.62 s |
| 4d9f93… | 0 | S5-qa-automator-4 | 1 | a494… | 17.63 s |
| 4bfb53… | 0 | S5-qa-automator-4 | 1 | 2856… | 12.01 s |
| c7f562… | 2 (chain) | S5-qa-automator-4 | 1 | 3959… | 12.86 s |
| c92860… | 2 (chain) | S5-qa-automator-7 | 1 | 0e07… | 22.76 s |
| 2605aa… | 1 | S6-qa-runner-1 | 18 | 2231… | 43.51 s |

The 8 job files have job_ids equal to the 8 attempt ids, so all 8 are covered by blocks and none adds a launch.

**Hand totals:**
- Launches: 8 attempts + 0 job launches = **8**.
- Runs: 12+4+4+1+1+1+1+18 = **42**.
- S5: 7 launches, 24 runs; durations rounded per launch 24.8+27.7+16.6+17.6+12.0+12.9+22.8 = **134.4 s**.
- S6: 1 launch, 18 runs, **43.5 s**.
- Repeats: TC_005-008 has fingerprints fc5c then c6a5; TC_009 has a494, 2856, 3959. No equal pair, so **0 repeats**.
- after_red: TC_005-008 repair after red (4), TC_009 two repairs after red (2), S6's TC_009 after its last red (1) = **7**.
- Check: first_run 18 + after_red 7 + stage_run 17 = 42.
- **Every new number matches 8 / 42 / 7 / 0 and the by_stage rows.**

**Which old number was wrong, and why.** The base `_block_launches` keyed a launch by `block_id`. A reparse takes a new `block_id` (`<attempt>-reparse-<hash>`), so all 7 reparse blocks counted as launches. That gives 15 launches, 42 + 38 reparse rows = 80 runs, and initial 68 / repair_verify 12. The cause reader had no job for the 4 reparse ids whose original was green, so `unknown_jobs` held 4 ids and 18 runs went to `unknown`. The 20 rows after a red, re-read by reparses of red blocks, went to after_red (27 = 7 + 20). **So yes: the reparse blocks counted as launches, and every old figure was inflated by them.**

**Run (verbatim), base vs new on cart-1.** The base tree is `git archive 7cf8c34 ai-packages/qa-factory` extracted into the scratchpad.

```
=== BASE 7cf8c34
known true
launches 15
runs 80
tests 18
by_cause {"first_run": 18, "after_red": 27, "stage_run": 17, "unknown": 18}
by_purpose {"initial": 68, "repair_verify": 12}
unknown_jobs ["446b57460fbe233362ab-reparse-9e61821ee753", "d67215ba124bbc6b138b-reparse-f6cc89666345", "c9286026d096394cd0e6-reparse-5085efd08807", "c9286026d096394cd0e6-reparse-dba7e3576bb8"]
unreadable 0
unreadable_blocks 0
=== NEW 5dc3e88
known true
launches 8
runs 42
tests 18
by_cause {"first_run": 18, "after_red": 7, "stage_run": 17}
by_purpose {"initial": 36, "repair_verify": 6}
unknown_jobs []
unreadable 0
unreadable_blocks 0
by_stage {"S5": {"launches": 7, "runs": 24, "tests": 18, "seconds": 134.4, "not_timed": 0, "repeats": 0, "repeat_seconds": 0.0, "repeats_not_timed": 0, "repeats_not_established": 0}, "S6": {"launches": 1, "runs": 18, "tests": 18, "seconds": 43.5, "not_timed": 0, "repeats": 0, "repeat_seconds": 0.0, "repeats_not_timed": 0, "repeats_not_established": 0}}
cells {'S4': '0', 'S5': '7 launches, 24 runs, 2m 14s; repeats over unchanged inputs: 0 (0m 0s)', 'S6': '1 launch, 18 runs, 0m 43s; repeats over unchanged inputs: 0 (0m 0s)', 'S7': '0'}
```

**Second fixture: `fixtures/investigation-14857/TP1-14857`.** It has 9 blocks, no reparses and no jobs. These are the only other run blocks under `fixtures/`; `find -type d -name run-blocks` finds two directories, this one and cart-1. Hand count: 4×6 + 1 + 1 + 5 = 31 runs, 9 launches, S5 8 launches / 26 runs, S6 1 / 5. Without reparses the old totals must not move, and they do not:

```
=== BASE
launches 9
runs 31
tests 5
by_cause {"first_run": 5, "launch_failed": 9, "after_red": 12, "stage_run": 5}
=== NEW
launches 9
runs 31
tests 5
by_cause {"first_run": 5, "launch_failed": 9, "after_red": 12, "stage_run": 5}
by_stage {"S5": {"launches": 8, "runs": 26, "tests": 5, "seconds": 416.2, ...}, "S6": {"launches": 1, "runs": 5, "tests": 5, "seconds": 196.3, ...}}
```

All 9 fingerprints differ, so repeats = 0, which is correct. This is also the fixture behind the quarantined `test_retro_test_runs.py` S1 pin "5 tests, 31 runs in 9 launches", and that pin still holds.

## Q2: the slow scenario files left to CI

They do NOT read retro numbers, and the canon will not go red on this diff's counts:
- `test_scenario_cart_1.py` is 13 lines that call `scenario_walk.run("cart-1")`.
- In cart-1's `story.json`, S9 is an `exit_gate` door with the facet `accepted`. `expected.json` S9 lists `work/retro-numbers.json` only under `handed`, and the `handed` facet checks presence plus JSON parse (`scenario_walk.py:511-549`). Nothing compares numbers.
- `door_exit_gate` calls `exit_gate.all_errors`. No package module outside `retro_numbers.py` imports `test_run_counts`, except `factory_dashboard.py:1435` (for the sentence). Grep over `scripts/*.py`, with positive control `run_block_metrics` = 17 hits.
- Grep `-i "test_run|launch|retro|Machine time|\| Stage"` over `test_scenario_cart_1.py`: 0 hits.
- `test_scenario_local_1_0108.py` / `_arm_b`: their stories have no run blocks and no jobs. `test_story_run_refusals.py`: its hits are driver "launch flags", not retro.

Header pins: `test_retro_wait_rework.py:142` pins the substring "| Wall time | Machine time |", which survives the new header. The old 7-cell separator `|---|---|---|---|---|---|---|` is pinned only in unrelated tables (audit, requirements). No machine parser of the `retro-numbers.md` stage table exists. Its readers are the retro role (`agents/qa-retro-analyst.md:61`, "paste the table unchanged") and `brief_pack`.

## Q3: spec §3 edges and their invariants

- **An attempt with no readable item counts once.** Holds: `:1483`. But see N2: it drifts from the reader's word "files", and a damaged reparse with a readable original is counted nowhere.
- **A job with a block on disk is never counted twice.** Holds. `block_ids` = every attempt id ∪ every block id or stem, and that includes attempts that were skipped or all-damaged. `_job_launches` skips `job_id in block_ids`. Cart-1 has 8 jobs, all matched, and 0 job launches.
- **Additive keys; old keys keep their meaning for existing readers.** The names are kept and `by_stage` and `launch_rows` are added. The values of `launches`, `runs`, `per_test`, `by_purpose`, `by_cause`, `unknown_jobs` change on reparse stories, and spec §2.1 C calls that a correction. Readers (Grep `-i "test_run_counts|test_run_cell|test_run_lines|test_run_sentence"` over the package `.py`, and `-i "test_run_counts|unknown_jobs|by_cause"` over `.md`/`.json`/`.yaml`; positive control as in Q2):
  - `factory_dashboard.py:1435` (sentence);
  - `retro_numbers.observations` `:2889` (`runs > tests`);
  - `estimate_facts` `:2930`, which copies `tests/runs/launches/by_cause` into the estimate precedent record;
  - `render` / `test_run_lines`;
  - the quarantined `test_retro_test_runs.py`.

  The meaning is unchanged for all of them. One note: precedent records written before SC6-2 carry inflated `runs/launches` for reparse stories, so a later comparison across records mixes the two counts. That is no blocker. The one key whose meaning drifts is `unreadable_blocks` (N2).
- **Other §3 edges, re-run or read.**
  - Reparse = same launch: holds (cart-1 15 → 8).
  - Damaged chain falls back: holds.
  - Unattributed stage printed under the table: V8 holds, and `render` prints it only when `run_counts` is a dict.
  - Import skipped: holds only when the import is the last item (N1).
  - Repeat never errs toward "yes": FAILS on a reparsed chain (B1).

## Q4: the four decisions the spec was silent on

1. **Empty results → "no".** Right. "No earlier launch of this set" is a recorded fact, and a launch that ran nothing has no set. An all-unnamed launch against an earlier empty set gives "not established", which is on the safe side.
2. **Differing seeds outrank a missing fingerprint → "no".** Right, but only once B1 is fixed. "No" here rests on a recorded difference, the seed, not on the missing fingerprint. In `_repeat_of` (`:1686-1702`), the missing fingerprint by itself always ends in "not established" when the seeds are equal, so **a "no" never rests on a missing fingerprint (FR-41, AR-28 kept)**. The caveat is B1: today an ABSENT seed on a reparse is a LOST value, an unknown. Once the seed is taken from the original, an absent seed means "no seed contract", a fact written by `build_run_block` as `data_seed or None`.
3. **An import or non-run last block ends the attempt as skipped.** Right for the case it covers. It is incomplete for the inverse chain, an imported original with a plain reparse (N1).
4. **Seeds compared with `==`.** Right. Dict equality ignores key order. A seed contract with run-specific fields (`evidence_refs`) can make equal seeds compare unequal, which errs toward "no", the allowed direction.

## Q5: test_silent_passes K1 on the base

**I ran the file on a pure 7cf8c34 tree,** `git archive 7cf8c34 ai-packages/qa-factory` extracted into the scratchpad. I did not run it in the sc6-2 tree and did not stash anything. I also did not use `wave1`, because its HEAD 5cc4f88 is a wave-1 CI-repair branch, not main.

```
FAIL K1: the row carries the words by ARGUMENT, for the second write — 'S2 test: my words' not found in:
=== test_silent_passes: 325/326 ok ===
```

**K1 is red on the base. This diff does not cause it.**
- The likely fix exists: `git log 7cf8c34..5cc4f88 -- scripts/tests/test_silent_passes.py` shows 5cc4f88, "wave 1 CI repair round 1: ... tests follow FV1-4 notes-file". It lands with the wave-1 repair.
- The builder labelled the base status "estimate, not verified" and said so honestly. This run closes that estimate.

## Q6: duplication and code quality (critic-diff-brief items 6-7)

- **DUPLICATION AND CONSISTENCY.**
  - (a) `run_block_metrics` is a second reader of `work/run-blocks` that still counts reparses (L1), and it contradicts the new numbers in the same retro. The report misleads a reader today on every story with reparses.
  - (b) It also keeps its own purpose literal instead of using `_BLOCK_RUN_PURPOSES` (N3).
  - (c) `_block_verdict` is the extracted survivor of the old inline checks, and nothing duplicates it.
  - Grepped: `run-blocks` and `_BLOCK_RUN_PURPOSES` in `retro_numbers.py`; `run_block_metrics` and `read_run_blocks` in `plans/`, `docs/SIBLING_MAP.md` and the package.
- **CODE QUALITY.** N3 (`started`/`start_raw` duplicate fields; purpose derived twice). Otherwise:
  - the helpers are small and single-purpose;
  - `test_run_cell` is the one place the cell's words are made;
  - there is no bare except and no new glob;
  - the lazy import of `run_history` follows the file's pattern.
- **One action, one road (item 12, P31).** No exclusion of a language, project or case. The stage comes from the controller record, then the dispatch id, then `unattributed`: one road for every stage.

## Q7: JUDGMENT (standing question 11) and AR-n

- **No new count judges meaning.** The repeat predicate is data equality: set equality of instance ids, string equality of `input_fingerprint`, dict equality of `data_seed_contract`. It reads no prose and no phrase list (FR-12 kept). The label is "repeats over unchanged inputs", not "extra" (F3 a, AR-29 kept).
- **No observation or finding line is added.** `observations()` is untouched, so a measurement does not become a finding (FR-26 kept).
- The census is unchanged; the builder reports `test_judgment_census` 24/24 and I did not re-run it. The `judgment: none` line is right.
- **AR-n by AR-n.**
  - AR-13: kept for `_block_launches`, which now reads through `run_history.read_run_blocks`. Still open for `run_block_metrics` (L1).
  - AR-15: kept; `test_run_counts` stays the one counter.
  - AR-22: `by_stage` is read by `render`; `launch_rows` is read by the role through the facts file.
  - AR-23: `n/a` vs `0` is kept, per V1/V2 and the cells I printed above.
  - **AR-28 is violated by B1**: a lost seed reads as "equal", and an unknown becomes "yes".

---

## Class completeness (map walk, rule 5)

- `docs/SIBLING_MAP.md` has no axis for readers of run blocks. Grep `(?i)reparse` and `read_run_blocks`: 0. Positive control `(?i)report-row readers`: 1.
- Known siblings outside the diff:
  - (1) `run_block_metrics`: L1, no queue carrier yet;
  - (2) the writer `run_suite.reparse_run_block` drops `data_seed_contract` and `import_provenance`: B1 and N1 writer side, outside the owns, to be queued;
  - (3) the other package readers of `work/run-blocks` that may count a reparse as an attempt (`acceptance._run_blocks`, `probe_by_code`, `metrics_projection`, `finalize_task`, named in the `read_run_blocks` docstring and by Grep of `import_provenance`). That is wider than the map, so **request to the coordinator: one scout dispatch** asking "which readers of `work/run-blocks` do not go through `run_history.read_run_blocks`, and does each collapse reparses by attempt".
- **Proposal to the Lead (the decision is the Lead's):** a new SIBLING_MAP axis, "run-block readers: one reader `run_history.read_run_blocks` ↔ N consumers; a reparse is the same attempt".

## Trail

- **Read:**
  - the spec in full;
  - the builder report in full;
  - the full code diff and test diff `7cf8c34..5dc3e88`;
  - `run_history.py:50-121`;
  - `run_suite.py:560-600, 734-818`;
  - `import_test_receipt.py:270-305`;
  - `retro_numbers.py:1329-1389, 1500-1530, 1587-1662, 1686-1702, 1815-1817, 2880-2935`;
  - `scenario_walk.py` (index, plus 262-276 and 511-549);
  - cart-1 `story.json:135-160`, `expected.json:105-130`;
  - cart-1 `work/retro-numbers.md:64`, `retro.md:56`;
  - SIBLING_MAP via Grep;
  - `plans/` via Grep;
  - `tools/critic_verdict.schema.json`.
- **Reruns:** listed in the block below. The builder's other witness files were not re-run; they are consistent with the diff (no shared surface).

**Probe P1-P3, full source** (`...\scratchpad\probe_seed.py`, run against the sc6-2 `scripts`):

```python
import sys, json, tempfile
from pathlib import Path
sys.path.insert(0, sys.argv[1])
import retro_numbers as R
def blk(att, start, seed, reparse=False, imp=False):
    b = {"block_id": att + ("-reparse-aaaaaaaaaaaa" if reparse else ""), "attempt_id": att,
         "attempt_started_at": start + ":00+00:00", "attempt_ended_at": start + ":30+00:00",
         "dispatch_id": "S5-qa-automator-1", "purpose": "initial", "input_fingerprint": "F1",
         "data_seed_contract": None if reparse else seed, "execution_status": "passed",
         "results": [{"instance_id": "t_a", "status": "passed"}]}
    if reparse:
        b["reparse_of"] = "work/run-blocks/" + att + ".json"; b["supersedes_block_id"] = att
    if imp:
        b["import_provenance"] = {"receipt_sha256": "x"}
    return b
def run(name, blocks):
    with tempfile.TemporaryDirectory() as d:
        rb = Path(d) / "work" / "run-blocks"; rb.mkdir(parents=True)
        for fname, b in blocks:
            (rb / fname).write_text(json.dumps(b), encoding="utf-8")
        c = R.test_run_counts(Path(d))
        print(name, "| launches", c["launches"], "| rows", [(r["id"], r["repeat"], r["repeat_of"]) for r in c["launch_rows"]])
s1 = {"seed": "one"}; s2 = {"seed": "two"}
run("P1 two attempts, seeds differ, no reparse", [...two originals...])
run("P2 same, each attempt reparsed (reparse writer drops the seed)", [...two originals + their reparses...])
run("P3 an imported attempt and its reparse", [...])
```

Note on the listing: the elided `[...]` lists are exactly the block tuples in the scratchpad file. In P2 the reparse dicts carry `data_seed_contract: None`, which mirrors `run_suite.py:792`.

Output, verbatim:

```
P1 two attempts, seeds differ, no reparse | launches 2 | rows [('aaa', 'no', None), ('bbb', 'no', None)]
P2 same, each attempt reparsed (reparse writer drops the seed) | launches 2 | rows [('aaa', 'no', None), ('bbb', 'yes', 'aaa')]
P3 an imported attempt and its reparse | launches 1 | rows [('external-1', 'no', None)]
```

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "B1 retro_numbers.py:1491 takes data_seed_contract from the deepest reparse; run_suite.py:792 reparse_run_block writes no seed, so two attempts over different seeds with equal fingerprints, each reparsed, read repeat yes (probe P2: ('bbb','yes','aaa')); violates spec 3.3 and AR-28"
  ],
  "fixes": [
    "B1: in _block_launches take seed (and fingerprint, start_raw, ended, dispatch_id, purpose) from the attempt's original item (depth 0 / first in read_run_blocks order), results and execution_status from the deepest readable item; add variant V6b (different seeds, equal fingerprints, each reparsed with a null seed -> repeat no)",
    "N1: skip an attempt when any item of its chain carries import_provenance (the reparse writer does not copy it); add a variant row",
    "N2 (Lead fork L1-b): unreadable_blocks drifts from its reader's words 'run block files' (retro_numbers.py:1483 vs :1817); recommended: count damaged files (unreadable += damaged), never a second launch",
    "N3: drop the started/start_raw double field and the second purpose derivation; run_block_metrics to use _BLOCK_RUN_PURPOSES",
    "L1 (Lead decision): run_block_metrics still counts reparses (cart-1 prints 'Test-execution jobs: 15, 80 executions' beside 8 launches / 42 runs: the packet contradicts itself, FR-10) and has no queue carrier in plans/; fold it into this fix round or open the finding plus node row before acceptance"
  ],
  "class_completeness": "SIBLING_MAP has no run-block-readers axis (Grep reparse/read_run_blocks 0; control 'report-row readers' 1). Siblings: run_block_metrics (L1, unqueued); writer run_suite.reparse_run_block drops data_seed_contract and import_provenance (queue, outside owns); other readers of work/run-blocks (acceptance._run_blocks, probe_by_code, metrics_projection, finalize_task) wider than the map: request a scout. Proposed new axis for the Lead: one reader read_run_blocks, a reparse is the same attempt.",
  "trail": {
    "read": [
      "docs/tasks/specs/20261113-sc6-2-extra-test-runs-spec.md",
      ".claude/worktrees/sc6-2/docs/tasks/specs/reports/20261113-sc6-2-report.md",
      "git diff 7cf8c34..5dc3e88 (retro_numbers.py, test_gate_brief_and_retro.py, changelog fragment)",
      "ai-packages/qa-factory/scripts/run_history.py:50-121",
      "ai-packages/qa-factory/scripts/run_suite.py:560-600,734-818",
      "ai-packages/qa-factory/scripts/import_test_receipt.py:270-305",
      "ai-packages/qa-factory/scripts/retro_numbers.py:1329-1389,1500-1530,1587-1662,1686-1702,1815-1817,2880-2935",
      "ai-packages/qa-factory/scripts/tests/scenario_walk.py:262-276,511-549",
      "ai-packages/qa-factory/scripts/tests/fixtures/stories/cart-1/story.json, expected.json, work/run-blocks/*, state/execution-jobs/*, work/retro-numbers.md:64, retro.md:56",
      "ai-packages/qa-factory/scripts/tests/fixtures/investigation-14857/TP1-14857/work/run-blocks/*",
      "docs/SIBLING_MAP.md (Grep)",
      "plans/ (Grep run_block_metrics, SC6-2)",
      "tools/critic_verdict.schema.json"
    ],
    "reruns": [
      {"command": "python -B scratchpad/hand.py <cart-1> (independent JSON dump, no retro_numbers import)", "result": "8 attempts, 7 reparses keeping attempt/times/dispatch/fp, 8 jobs all matching attempt ids; hand totals 8 launches, 42 runs, S5 7/24/134.4 s, S6 1/18/43.5 s, 0 repeats"},
      {"command": "python -B scratchpad/count.py on cart-1, base tree (git archive 7cf8c34) vs sc6-2", "result": "base launches 15 runs 80 after_red 27 unknown 18; new launches 8 runs 42 after_red 7 no unknown; by_stage S5 7 launches 134.4 s, S6 1 launch 43.5 s, 0 repeats"},
      {"command": "python -B scratchpad/count.py on investigation-14857/TP1-14857, base vs new", "result": "both launches 9 runs 31 tests 5, by_cause identical; new by_stage S5 8/26, S6 1/5, 0 repeats"},
      {"command": "python -B scratchpad/probe_seed.py <sc6-2 scripts>", "result": "P1 bbb no; P2 (each attempt reparsed, seed dropped) bbb yes repeat_of aaa; P3 imported attempt plus reparse counted as 1 launch"},
      {"command": "python -B <git archive 7cf8c34>/ai-packages/qa-factory/scripts/tests/test_silent_passes.py", "result": "FAIL K1 'S2 test: my words' not found; === test_silent_passes: 325/326 ok === (red on base, not caused by the diff)"},
      {"command": "python -B .claude/worktrees/sc6-2/ai-packages/qa-factory/scripts/tests/test_gate_brief_and_retro.py", "result": "=== gate brief and retro numbers: 1059/1059 ok ==="}
    ]
  }
}
```
