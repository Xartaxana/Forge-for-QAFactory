# t-870 -- critic, offload topic C (C1 dispatch_new.py t-862, C2 ci_read why t-851, C3 wave.py merge t-868)

Verdict: **GO WITH FIXES** (fit_with_fixes). 6 fix-before-merge findings (C1-1, C1-2, C2-1, C3-1, C3-2, C3-3), and the
rest go into the same fix round. The proposed decisions are for the Lead tier to take (rule 6).

DoD under review: spec r2 §3 C1 (545-560), C2 (561-577), C3 (578-626), §7 M6/M7, §11/§11'.

## Findings

### C1 -- tools/dispatch_new.py (db7f6182)

**C1-0 (landing condition, blocks merge order).** The committed tip does not run on its own. `dispatch_new.py:86` calls
`dispatch_manifest.header_ids`, but `def header_ids` is missing from origin/main, origin/offload/c1 and offload/b0 6d31157f
(grep count 0 on all three). It exists only in B0's UNCOMMITTED files in the offload-c1 worktree. I ran the tests on a clean
`git archive db7f6182 tools`: **26 failed, 2 passed**. The submitted witness (28 passed) was taken on the dirty tree.
Fix: merge C1 only after B0's Fable commit lands, rebase onto it, and re-run the witness on the committed tree. The same
applies to C3: its base is B1 (7217de57) plus B0's dirty `journal_keys.py`.

**C1-1 (fix before merge; part spec defect, the dispatcher's).** The generator runs one of the hook's three refusing
layers. `dispatch_gate.decide_full` (dispatch_gate.py:790-835) runs completeness, then `handoff_folder_check`, then
`_path_check`. `dispatch_new.py:110` runs only `dispatch_manifest.check`. I fed the generator's exit-0 output through
`dispatch_gate.decide` with cwd = the worktree:
- missing `--given` (E-C1-5 as specified): generator 0, hook **2** `DISPATCH PATHS MISSING`;
- `--owns` of a new file without `(new)`: generator 0, hook **2**;
- `--kind critic --handoff C:\tmp\x.md`: generator 0, hook **2** `HANDOFF PATH (R11-h)`.
The spec invariant names only `check`, and E-C1-5 contradicts `_path_check` outright: that half is a spec defect. Still,
the commit's claim "axis 13: covered" is wrong. SIBLING_MAP axis 13 lists `dispatch_gate.decide_full` as a reader of the
same cut, with the path check "before the send".
Fix: call `dispatch_gate.decide({"cwd": <repo top>, "tool_input": {"subagent_type": kind, "prompt": text}})` with no
`description`, so the label check is skipped. Refuse on exit 2 with the hook's text. Its doors are `(new)` and
`manifest-skip:`. E-C1-5 becomes "refused with the hook's door". Add table rows for all three cases.

**C1-2 (fix before merge).** An empty or whitespace-only list item breaks the section. `--owns C:/r/a.py "" C:/r/b.py`
prints `owns:\nC:/r/a.py\n\nC:/r/b.py` with exit 0. The blank line ends the extent, so the checker owns only a.py. The
printed text still shows b.py under `owns:`, so the reader and handoff_gate disagree. Fix: in `_forbidden`
(dispatch_new.py:52), refuse an empty or whitespace-only list value.

**C1-3 (fix).** `build_text` has a grammar of its own for `--designer` (dispatch_new.py:78). `--designer "Skip -- tiny"`
is classed as a path, gets backticks and is refused. The checker's `_DESIGNER_SKIP_RE` is IGNORECASE. Fix: classify with
`dispatch_manifest._DESIGNER_SKIP_RE` and `_DESIGNER_RESUBMISSION_RE`, or print the value verbatim unless it is a path
holding whitespace.

**C1-4 (queue).** The degraded cut fails open. `check()` returns `(0, "", UNCHECKED note)` for a degraded cut, and the
generator prints the text. The docstring at dispatch_new.py:107 says an unchecked text is not handed out. Make the two
agree: refuse when the cut is degraded, or correct the comment.

### C2 -- ci_read why (8d3ae135)

**C2-1 (fix before merge; empirical, rule 13).** The ordinal fallback in `step_section` (ci_read_common.py, the
`eligible` list) counts skipped steps. A skipped step writes no `##[group]` to the log. I measured this on the real red run
43599158536, job 132459994342 (forge-check):
- `steps[]` holds 13 `skipped` steps (8-20);
- the log holds 7 `##[group]Run ` lines;
- the `eligible` count is 20.
A named step such as `deps`, `journal` or `piles frozen batches` is logged as `##[group]Run <command>`, so the name match
fails. The ordinal then fails too, because the counts differ. So on every red run where a named step fails and later steps
are skipped, the answer drops to the whole job tail. The fallback is safe (never empty), but most of the feature is lost.
The live run worked only because step 7 is an unnamed `Run python tools/lint_ratchet.py --check`. The fixtures
(test_ci_read.py:618-683) have no skipped steps, and their `##[group]Set up job` / `Complete job` groups are not in the
real log. Fix: leave out steps whose `conclusion == "skipped"` when building `eligible`. Add a row with a real-shaped log:
a named failing step, trailing skipped steps, no Set up/Complete groups.

**C2-2 (Q1, fix).** See Q1.

**C2-3 (queue).** `cmd_why` (ci_read.py:239-294) is about 57 lines and nests five levels deep:
make_commands > cmd_why > for job > for step > if. Move the per-job body into a helper.

### C3 -- tools/wave.py merge (35299992)

**C3-1 (fix before merge).** A step-9 fetch failure comes after the push but reports "refused". `refresh()`
(wave.py:264) calls `self.fetch("step 9")`, which raises `Refuse(code=2)`. Nothing between it and `run()` catches it, so:
- the run exits 2, which the docstring defines as "refused before any push";
- `finish()` never runs: no summary, no merge sha, the branch is not deleted.
`JOURNAL RESTORE MISMATCH` (wave.py:311) skips the summary the same way. Fix: catch `Refuse` inside `refresh` and return
the reason ("root checkout not refreshed: fetch failed"). Carry the mismatch as a flag so that `finish()` still runs and
then exits 1. Add a test with a network failure at step 9 after a pushed merge.

**C3-2 (fix before merge; Q5).** A journal line can be lost silently in step 9. The details are under Q5 (a).

**C3-3 (fix before merge; part spec defect).** `delete_remote` (wave.py:355) runs `git push origin --delete <branch>`
with no old-value guard. Commits pushed to the branch after the step-2 fetch, for example by a live worker (the dirty-tree
case), are deleted from origin, and nothing says so. The local side is guarded (`update-ref -d <ref> <sha>`, X-5); the
remote side is the uncovered half of the same class. The spec wrote the bare command. Fix:
`git push --force-with-lease=refs/heads/<b>:<sha from step 3> origin --delete <b>`. On a lease failure, print
`remote branch kept: it moved`.

**C3-4 (fix).** `TASK_RE` (wave.py:44) is a private id grammar: `[a-z]?`. B0's `journal_keys.ID_RE` is `[a-z]{0,2}`
(clone letters aa..zz, D3). So `--task t-123ab` is refused, against E-C3-3 ("per B0"). `--node` checks only that N is
numeric (wave.py:407). `jk.NODE_RE` exists. Fix: use `jk.ID_RE` or `jk.parse_id`, and validate `"/".join(node)` against
`jk.NODE_RE`.

**C3-5 (fix).** Step 6 takes two roads.
- A `piles status` refusal pushes the merge and exits 1 (wave.py:208-212).
- A refusal of the status COMMIT is `Refuse` code 2, and nothing is merged (wave.py:217-218).
Both are bookkeeping failures of one step, so take one road (the Q3 one) for both. Two smaller defects on the same path:
- `self.piles_text` is never reset between push attempts. A refusal on attempt 1 followed by success on attempt 2 still
  exits 1.
- The "run by hand" line says nothing about where to run it, nor that a commit and push of the batch file must follow.

**C3-6 (queue).** `forge_check_state` (wave.py:73-98) has three problems:
- it scrapes the printed text of `ci_read pipelines` / `jobs`, a second reader of a print shape (FR-14);
- it can hold `main-merge` for up to 2 x `CI_TIMEOUT` = 120 s of network while a second wave waits `LOCK_WAIT` = 60 s
  and refuses;
- per PROJECT.md, a bare branch push runs nothing, so the answer is mostly `unknown`.
Fix: cut `CI_TIMEOUT` to about 15 s, or read the state before taking the lock. Move to a ci_read function once C2 lands.

**C3-7 (queue).** The root ff merge in step 9 fires `.githooks/post-merge`, which starts the full `worktree_sweep` in the
background (gd == common). That sweep races with step 10's `worktree remove` / `branch -d`. No data is lost (the sweep
archives a ref before `branch -D`), but the summary's `branch:` line can be wrong. Either note the race in step 10's text,
or skip step 10's local removal when the root was refreshed and let the sweep do it.

## Answers

**Q1.** Agree. Refuse in `_check` (ci_read.py:309), before any request. Name both flags: "--branch/--workflow select
`latest` only; with run <id> drop them". Under sweep-the-artifact-first, `--workflow` with an explicit id is the same
silent ignore, so refuse both. Add a table row for each flag.

**Q2.** Yes on both counts. One path per line under `given:`/`owns:` is the continuation form the checker reads, and a
comma inside a path survives it. stdout is the pasteable product, so a refusal belongs on stderr with stdout empty. Two
conditions: refuse empty list items (C1-2), and refuse whatever the launch hook would refuse (C1-1).

**Q3.** The Lead's lean is what the builder already built, and I agree with it. Push the merge without the status commit,
print the command, exit 1. E-C3-8's "changed nothing" covers refusals at steps 3 and 5 only. Step 6 is bookkeeping, and
refusing the merge over it would contradict the owner's cadence (Командная работа п. 12: merges do not wait). "Never undo
a pushed merge" holds because nothing is undone. The spec defect is the dispatcher's: reword E-C3-7 to "piles refuses in
step 6 -> the merge is pushed without the status commit". Also apply it to the commit-refusal branch (C3-5).

**Q4.** Agree: keep the remote too. A dirty tree is the signal of a live worker. Deleting the remote makes the worker's
next push quietly recreate the branch. Without a lease it also destroys anything already pushed (C3-3). Print
`remote kept: <worktree> is dirty`.

**Q5.** Yes, there are loss paths:
- **(a) Silent loss, blocking.** Unlocked by-hand writers bypass the lock. Edit/Write is the journal road CLAUDE.md
  prescribes today, and B23 ships in WARN mode, where "a by-hand Edit appends without the lock" (spec §3.B23 item 7).
  Suppose a second session Reads and Edits the journal inside the window between `path.write_bytes(head_bytes)`
  (wave.py:301) and the write-back (wave.py:308). It appends its line to the HEAD-state bytes, and the write-back then
  overwrites it. The sha check compares the file with `cur`, so it passes, and the loss is SILENT. If the Read came before
  the window, Edit's stale check probably refuses the Edit; that is friction, not loss (an estimate, not measured). The
  window covers a whole-tree ff merge, so it lasts seconds. E-C3-11's "no line lost" holds only for writers that take the
  lock; the test appender takes it (test_wave.py:256).
  Fix: before the write-back, read the file. It should equal what wave left there: origin's blob after a good merge, or
  the HEAD bytes after a failed one. If it does not, and `now.startswith(expected)`, write `cur + now[len(expected):]`,
  keep the copy and print it. Otherwise keep the copy and raise the MISMATCH. Add a row with an unlocked appender.
- **(b)** Unlocked readers inside the window see a truncated journal: the HEAD-state bytes. That includes
  `journal_keys where`, `journal_echo` and a session reading the tail to issue an id. A reader that issues ids without
  B1's counter can reissue a used id. This is not C3's code, but C3's window creates it. Queue it as a note on B1/B0's id
  road.
- **(c)** An `OSError` from the write-back (wave.py:308) is not caught. The copy stays in the lock dir, but nobody is told,
  and the root journal stays at the origin state. Fix: try/finally around merge + write-back, printing the copy path.
- **(d)** Two sessions sharing one root are safe for git-side contention:
  - an `index.lock` held by the other session makes the ff merge fail, and the journal is restored;
  - a `git add` of the journal between the unlocked status check (wave.py:271) and the swap makes the ff merge fail on
    local changes, and the journal is restored.
- **(e)** Changes to the root beyond the invariant:
  - the post-merge sweep (C3-7), which is the normal behaviour of any main merge;
  - `git merge` overwrites ignored files at paths the incoming commit starts tracking. That is rare; note it in the text.

## Standing questions

- Fit to spec: C1 meets its stated invariant, but that invariant is too narrow (C1-1). C2 meets the spec, but with a
  semantic defect (C2-1). C3 meets the spec except C3-1, C3-3 and C3-4.
- DUPLICATION AND CONSISTENCY: wave.py:44 duplicates `journal_keys.ID_RE` (journal_keys.py:80) and does not use NODE_RE
  (:101). Wave scrapes ci_read's printed shape (C3-6). The designer classification is a second grammar
  (C1-3). wave imports the private `journal_lock._git_env`; the builder reported it, so queue it for B1 to export. Grep
  for a second merge or `--ff-only` road in tools/ on origin/main: only test_worktree_sweep.py. The positive control
  found 3 hits in wave.py.
- CODE QUALITY: `cmd_why` nesting (C2-3, queue). Dead clause at wave.py:281: `(cur is None and orig)` is already covered by
  the startswith test (queue). `piles_text` is stale across attempts (C3-5). No wave.py function exceeds 60 lines.
- ONE ROAD: step 6 takes two roads (C3-5). No exclusion of a language, project or case. Wave is the one merge road, with
  the by-hand merge as the named fallback (axis 34).
- ARCHITECTURE / JUDGMENT: forge tools only. `architecture: none` holds; question 11 does not apply.
- Tests: none of the three test sets would catch its main defect:
  - C1's table never runs the hook (C1-1);
  - C2's fixtures are not shaped like a real log (C2-1);
  - C3's appender takes the lock, and no test fails the network at step 9 (C3-1, C3-2).

## Axis lines (SIBLING_MAP, touched axes)

- axis 10: covered (C3). The common dir is read through `journal_lock.common_dir`.
- axis 12: covered (C3). Status goes only through `piles.py status`. The two-road defect is C3-5.
- axis 13: NOT covered (C1). `decide_full`'s handoff and path checks are a reader the generator skips (C1-1).
- axis 15: covered for C1 and C3 (`streams.utf8_stdio`). C2 inherits ci_read's existing setup.
- axis 29: C3 rewrites an append-only carrier twice, with a truncation in between (Q5 a). The "n/a" line is wrong. Mark it
  covered by the delta guard once that fix lands.
- axis 34: covered. Wave is the one merge road. The step-6 split is C3-5.

## Trail

Read:
- spec r2 lines 545-626, 325-340, 490-530 and 982-1010;
- C1: the diff, its tests and the t-862 report;
- C2: the diff (ci_read.py, ci_read_common.py) and test fixtures 618-683;
- C3: wave.py in full, the test_wave.py outline and the t-868 report;
- dispatch_manifest.py (check / check_cut / cut_payload) and dispatch_gate.py 640-835;
- SIBLING_MAP axis 13 and the axis headings 10/12/15/29/34;
- `.githooks/post-merge`, `pre-merge-commit` and `pre-push`;
- critic-diff-brief.md items 6-7 and 12.

Re-runs and probes:
- offload-c1, `python -B -m pytest tools/test_dispatch_new.py -q`: 28 passed in 0.15s.
- Clean archive of db7f6182, same command: 26 failed, 2 passed.
- offload-c3, `python -B -m pytest tools/test_wave.py -q`: 41 passed in 128.14s.
- C1 probes: empty owns item: exit 0, blank line. `Skip --`: refused. Hook decide on generator output: 2 / 2 / 2 for
  missing-given, new-owns and critic-wrong-folder. `(new)`-marked owns: 0.
- C2 live (read-only): `ci_read.py why 43599158536 --tail 15` prints step 7's section, `(15 of 21 lines)`. Job
  132459994342: 13 skipped steps in `steps[]`. `ci_read.py log 132459994342 --grep "##\[group\]"` shows 7 `Run` groups
  and no Set up/Complete group.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "C1-0 landing: db7f6182 alone fails 26 of 28 tests (header_ids exists only in B0's uncommitted files); merge after B0's Fable commit and re-witness on the committed tree; same order condition for C3 (B1 base + B0 journal_keys)",
    "C1-1 dispatch_new.py:110 runs only dispatch_manifest.check; the launch hook (dispatch_gate.decide_full) refuses its exit-0 output for a missing given, a new owns without (new), a critic handoff outside the folder; E-C1-5 contradicts the path check (spec defect)",
    "C1-2 an empty --owns/--given item prints a blank line that ends the section: a path printed under owns: that is not owned",
    "C2-1 step_section ordinal fallback counts skipped steps; measured on job 132459994342 (20 eligible vs 7 Run groups): a named failing step with later skipped steps always falls back to the job tail",
    "C3-1 wave.py:264 a step-9 fetch failure after a pushed merge exits 2 (documented as refused before any push) with no summary and no branch deletion; the restore mismatch also skips finish",
    "C3-2 wave.py:301-308 an unlocked by-hand journal Edit inside the step-9 window is overwritten by the write-back and the sha check passes (silent loss)",
    "C3-3 wave.py:355 remote branch delete has no lease: commits pushed after the step-2 fetch are deleted silently"
  ],
  "fixes": [
    "C1-0: land C1 and C3 only after B0 (and B1 for C3) are committed; rebase and re-run the witnesses on committed trees",
    "C1-1: call dispatch_gate.decide with cwd = repo top and no description; refuse on its exit 2 with its text; E-C1-5 becomes a refusal with the (new) / manifest-skip door; rows for the three cases",
    "C1-2: refuse an empty or whitespace-only list value in _forbidden (dispatch_new.py:52)",
    "C1-3: classify --designer with dispatch_manifest's own regexes (case-insensitive) instead of the split test at dispatch_new.py:78",
    "C1-4 (queue): degraded cut -> refuse, or correct the fail-closed comment",
    "C2-1: exclude steps with conclusion skipped from eligible; add a real-shaped fixture (named failing step, trailing skipped steps, no Set up/Complete groups)",
    "C2-2 (Q1): refuse --branch and --workflow together with an explicit run id in _check, naming both",
    "C2-3 (queue): split cmd_why's per-job body into a helper",
    "C3-1: catch Refuse inside refresh and return the reason; carry the restore mismatch as a flag so finish runs, then exit 1; test a step-9 network failure after the push",
    "C3-2: before the write-back compare the file with what wave left; append any delta to cur, keep and print the copy; else raise the mismatch; try/finally around merge plus write-back; test an unlocked appender",
    "C3-3: delete the remote with --force-with-lease=refs/heads/<b>:<step-3 sha>; in the dirty-worktree case keep the remote too (Q4)",
    "C3-4: use journal_keys.ID_RE or parse_id for --task and NODE_RE for the joined --node",
    "C3-5: one road for step 6 (status refusal and commit refusal both push the merge, exit 1); reset piles_text per attempt; the by-hand line names where to run and the commit plus push",
    "C3-6 (queue): CI_TIMEOUT about 15 s or read forge-check before the lock; later a ci_read function instead of scraping",
    "C3-7 (queue): note or avoid the race between the post-merge sweep and step 10",
    "Spec (dispatcher's): C1 invariant to name the launch hook; reword E-C1-5 and E-C3-7; lease on the remote delete in step 10"
  ],
  "class_completeness": "axis 13 not covered by C1 (decide_full readers skipped); axis 29 line of M6 wrong (step 9 rewrites the append-only journal); remote-delete is the unguarded half of the X-5 old-value class; step 6 has two roads (axis 34 within the artifact); axes 10, 12, 15, 34 otherwise covered",
  "trail": {
    "read": [
      "docs/tasks/specs/20261114-coordinator-offload-spec-r2.md 545-626, 325-340, 490-530, 982-1010",
      "origin/offload/c1 tools/dispatch_new.py, tools/test_dispatch_new.py; docs/tasks/handoffs/t-862-C1.md",
      "origin/offload/c2 tools/ci_read.py, tools/ci_read_common.py diff, tools/test_ci_read.py 618-683",
      ".claude/worktrees/offload-c3/tools/wave.py (all), tools/test_wave.py outline; docs/tasks/handoffs/t-868-C3.md",
      "tools/dispatch_manifest.py check/check_cut/cut_payload; tools/dispatch_gate.py 640-835",
      "docs/SIBLING_MAP.md axis 13 and headings 10/12/15/29/34; docs/tasks/critic-diff-brief.md items 6, 7, 12",
      ".githooks/post-merge, pre-merge-commit, pre-push"
    ],
    "reruns": [
      {"command": "offload-c1: python -B -m pytest tools/test_dispatch_new.py -q", "result": "28 passed in 0.15s"},
      {"command": "clean git archive db7f6182: python -B -m pytest tools/test_dispatch_new.py -q", "result": "26 failed, 2 passed"},
      {"command": "offload-c3: python -B -m pytest tools/test_wave.py -q", "result": "41 passed in 128.14s"},
      {"command": "dispatch_gate.decide on dispatch_new exit-0 output (missing given / new owns / critic wrong folder)", "result": "hook exit 2 / 2 / 2"},
      {"command": "ci_read.py why 43599158536 --tail 15 (live, read-only)", "result": "step 7 section printed, (15 of 21 lines)"},
      {"command": "ci_read.py log 132459994342 --grep group headers; job steps", "result": "7 Run groups vs 20 eligible steps (13 skipped)"}
    ]
  }
}
```
