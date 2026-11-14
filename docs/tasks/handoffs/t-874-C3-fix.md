# t-874 C3 fix round (offload/c3, commit 281c614d, pushed to origin/offload/c3)

Witness: `( cd C:/QAFactory/forge-repo/.claude/worktrees/offload-c3 && python -m pytest tools/test_wave.py -q )`
-> `49 passed in 160.60s (0:02:40)` (run before the CRLF->LF normalisation of wave.py; after it a re-run of
`-k "task or node or restore or unlocked"` -> `13 passed, 36 deselected`).

`git show --stat HEAD`: tools/test_wave.py 115 lines changed, tools/wave.py 114 lines changed (189 insertions, 40 deletions).
B0's unstaged files were not staged.

Items:
- C3-1 fixed: `refresh` catches the step-9 fetch Refuse and returns "git fetch origin failed"; a restore mismatch is a flag
  (`self.mismatch`), `finish()` always runs and then exits 1. Rows: test_fetch_failure_in_step_9_after_the_push_still_finishes_C3_1,
  test_restore_mismatch_keeps_the_copy_and_the_summary_exit_1_C3_1.
- C3-2 / Q5 fixed: swap compares the file with what wave left (origin blob after a good merge, HEAD bytes otherwise); an
  appended tail is carried over (cur + tail, copy kept and named); anything else keeps the copy and is the mismatch;
  OSError names the copy (Q5c). Rows: test_unlocked_appender_in_the_window_is_carried_over_Q5a, test_oserror_in_the_window_names_the_copy_Q5c.
  Q5b (unlocked readers see the truncated journal inside the window): reported, not C3 code -- queue as a note on B1/B0's id road.
- C3-3 fixed: `push --force-with-lease=refs/heads/<b>:<step-3 sha> origin --delete`; on lease failure prints
  "remote branch kept: it moved". Row: test_remote_branch_that_moved_is_kept_by_the_lease_C3_3.
- C3-4 fixed: `jk.parse_id` for --task (t-123ab accepted), `jk.NODE_RE` on "/".join(node); TASK_RE and `import re` removed.
  Row: test_clone_letters_pass_the_task_check_and_bad_nodes_are_refused_C3_4 (+ the existing bad-task table).
- C3-5 / Q3 fixed: a piles refusal AND a refused status commit take one road: merge pushed without the status commit,
  text + exact command (now "run by hand, from <root>: ... -- then commit and push the batch file") printed, exit 1;
  `piles_text` reset at the start of each attempt. Rows: test_status_commit_refusal_takes_the_same_road_C3_5,
  test_piles_refusal_on_attempt_1_then_success_exits_0_C3_5, test_piles_refusal_keeps_the_pushed_merge... (updated).
- C3-6 partly fixed, remainder reported: CI_TIMEOUT 60 -> 15 (two calls <= 30 s < LOCK_WAIT 60). The text scrape of ci_read
  (FR-14) stays; move to a ci_read function once C2 lands (queued by the critic).
- C3-7 fixed inside wave.py without editing .githooks: the post-merge sweep is not suppressed; when step 10's `branch -d`
  fails and the ref is already gone, the summary says "deleted (by the post-merge sweep that the root refresh started)".
  Row: test_sweep_deleting_the_branch_first_is_not_reported_as_kept_C3_7. Residual: worktree remove of a clean worktree by
  wave can still race the sweep; its result is not inspected (git remove failure is ignored, as before). To suppress the
  race fully a skip switch in .githooks/post-merge would be needed (report only).
- Q4 fixed: a dirty worktree keeps local branch, worktree and the remote; prints "remote kept: <worktree> is dirty".
  Row: test_branch_in_dirty_worktree_is_kept_E_C3_12 (extended).

Test size: tests-over: +109 test lines vs +80 code lines; nine new rows each need real-origin fixtures (hooks, concurrent
push, unlocked write), and the old mocked-_sha mismatch row was replaced by a real garbage-write row.

Deviations / notes: the status line of the mismatch now reads "root checkout not refreshed: journal restore mismatch"
plus the full MISMATCH line; a mismatch return does NOT write back over the file (per Q5: keep the copy, raise).
wave.py was briefly CRLF after my scripted edit; normalised to LF before commit (git warned).
Needed beyond the manifest: journal_keys.py (ID_RE, NODE_RE, parse_id), .githooks/post-merge.
