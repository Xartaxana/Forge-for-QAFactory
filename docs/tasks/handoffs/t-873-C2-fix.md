# t-873 C2 fix round (offload/c2, commit b5bd6320, pushed to origin)

- C2-1: fixed. `step_section` leaves skipped steps out of `eligible` (ci_read_common.py). Row `test_why_C2_1_skipped_steps_open_no_group_so_the_ordinal_still_finds_a_named_failing_step`: named failing step, trailing skipped steps, log with no Set up/Complete groups.
- C2-2 / Q1: fixed. `_check` refuses an explicit run id with --branch or --workflow before any request, exit 2, text "--branch/--workflow select `latest` only; with run <id> drop them". Rows `test_why_Q1_..._refused_before_any_request[branch]` and `[workflow]` (assert net.requests == []).
- C2-3: fixed, no behaviour change. cmd_why split into helpers `why_run` and `why_job` (nesting down to 3 levels).
- Tests vs code: ci_read.py net -73/+... (diff 39 ins/34 del within it), tests +20 lines; code +~39 lines incl. common; tests-over: 20 test lines vs about 5 net code lines is the refusal and filter (3 rows; the refactor is behaviour-neutral and carries no new test).

Witness: `( cd .../agent-a116e352b6254c7f7 && python -m pytest tools/test_ci_read.py -q )` -> `138 passed, 2 skipped in 5.47s`
(pre-commit hooks passed: escape allowlist, indexes, WARN ok).

git show --stat HEAD:
 tools/ci_read.py        | 73 +++++++++++++++++++++++++++----------------------
 tools/ci_read_common.py |  5 ++--
 tools/test_ci_read.py   | 20 ++++++++++++++
 3 files changed, 64 insertions(+), 34 deletions(-)

Note: refusals print to stdout in this tool (the shared `emit` path), so the Q1 row reads stdout, not stderr.
Siblings: none noticed. Needed beyond manifest: none.
