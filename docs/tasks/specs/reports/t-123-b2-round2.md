# t-123 (with t-121) — FG7-8 part B, node B2, fix round 2 (attempt 2): report

Builder (Sonnet), 12.11.2026, in worktree `agent-a365d2def0628cb25`, uncommitted. Input: the critic's verdict `docs/tasks/specs/reviews/t-124-fg7-8-b-code.md` (fit_with_fixes: BL-1, F-1..F-9, seven open questions taken as written).

## One line per item

| Item | Result |
|---|---|
| BL-1 | FIXED. `gate_preflight.git_env(literal)` is the one environment of a git call; `repo_words._env()` = `git_env(literal=True)` (every git call of `_exec`: add, commit, stash) and the `ls-files` pathspec read of `vcs_changes` passes `literal=True`. Probe case: person `?? q[a]-factory/tracked.txt` beside a dirty `qa-factory/tracked.txt`, both words: exactly that path is taken, the factory file stays ` M`, the pass is recorded. The `*` and `?` names cannot be created on this Windows machine: those two rows are in the test behind `os.name != "nt"` (CI on Linux judges them; NOT run here). Optional hardening (judge the stash on `stash show --name-only` == paths): NOT done — the git form was not measured in t-118 and literal mode removes the cause; the verdict marks it optional. |
| F-1 | FIXED. `_said` = `contract.person_decision(option, line, replaced)` (lines whitespace-folded). The hand-built tail is gone. |
| F-2 | FIXED. `_git` = `_git_raw(...).strip()` (None kept); one env builder `git_env`; `repo_words._env` calls it. |
| F-3 | FIXED. `run` is 22 lines; split into `_plan` (steps 1-4), `_write` (5-6), `_judge_commit`, `_judge_stash`, `_kept`, `_done`; `_failed(plan, ran)` takes two dicts, not 12 parameters. Longest function ~45 lines, none deeper than three levels, no new name matches `UNIT_NAME_RE` (`_judge_*` starts with `_`; census safety stays 55, test 22/22). |
| F-4 | FIXED. `_commit_undo(..., spans=True)` gives two spans: "`git reset --soft X`, then `git read-tree Y`"; used by the landed-not-exact problem, `done_line`, the unread problem. |
| F-5 | FIXED. A commit that landed but is not exactly the shown set, and a stash entry left by a stash that did not end cleanly, return `done` with `failed: True` (stage, decision = the person's word + what landed + the undo): `record_args` writes `--remark` (no pass); driver: recorded, then joins `failed` with the problem (conductor told once); CLI: recorded, prints the problem + door, exit 3. |
| F-6 | FIXED. `FINDING_ID` deleted; `run(..., door, finding_id, timeout=...)`; the driver passes `entry["id"]`, the CLI the stored-door key; `_own_door(rows, finding_id)`. |
| F-7 | FIXED. `human-text.json` `action_lines`: `prefixes` gained `to undo it:` and `to take them back:`; new data row `done_prefixes: {commit, stash}`; `repo_words._prefix(verb)` reads it (falls back to `the fix:` when the row cannot be read); used by `done_line` and `reminder_line` for a success only; failures keep today's wording. |
| F-8 | FIXED. `your uncommitted changes (N), files outside your tests folder included, all listed - <words> take(s) exactly these:`; with no path outside the tests folder the line is byte-identical to B1's (the existing row "Q-1 inside only" still equals it). |
| F-9 | FIXED. `vcs_changes` returns None when the `status` read gives None; after a write `run` reads `after is None` as `unread`: commit → done with `unread` → remark, problem "could not be read afterwards, so the result is not known ... To undo it: <two spans>"; stash → `kept` → remark, the problem names the entry and `git stash apply --index`. |
| Q1 | = F-7. |
| Q2 | = F-8. |
| Q3 | = F-5 + F-4 (the factory never resets on its own). |
| Q4 | `still`: exit 0 kept (unchanged, as proposed). |
| Q5 | stash timeout with a stale lock, no `read-tree`: unchanged (as proposed). |
| Q6 | = BL-1 via `GIT_LITERAL_PATHSPECS=1`, no blocker row. |
| Q7 | N-1 is the Lead's node; nothing done here. |

## Red before (the fix neutered in a COPY of the package under the scratchpad, never in the worktree)

Copy `scratchpad/red/pkg`, runner `scratchpad/red/runner.py` (prints FAIL lines of named test functions). Each neutering was made in the copy only; the copy's `gate_preflight.py` was restored from the worktree by byte copy and checked (`cmp` identical, sha256 prefix `6db56dbda6d2490569a3` on both).

- BL-1 (`git_env` does not set `GIT_LITERAL_PATHSPECS`): `test_repo_words_a_glob_path_of_the_person_never_takes_the_factorys_file` 12 pass 6 fail: `vcs_commit of q[a]-factory/tracked.txt: done, no problem — got (True, 'A commit ... was made, but it does not hold exactly the changes you were shown ...')`, `the factory's file stays dirty`, `exactly the listed path was taken — got ['q[a]-factory/tracked.txt', 'qa-factory/tracked.txt']` (same for `vcs_stash`), `the executor's git environment`.
- F-1 (hand-built text): `F-1: the decision is the one writer's text`.
- F-4 (one span): `F-4: the undo is two backtick spans, each one command`.
- F-5 (`record_args` without `failed`): round-two function raised `KeyError: 'block'` (the record became a pass form), driver row `a write that landed wrong is a REMARK ... got ([], '--task', ...)`, and `test_words_doors.row_repo_words_cli`: `a commit that landed wrong exits 3 (F-5) ... got (1, False, False)` and `...kept as a remark ... got (0, [])`.
- F-6 (literal id in the door): `F-6: the refusal's door names the id it was given`, `...and no other`.
- F-7 (`_prefix` returns `the fix:`): `F-7` five rows (commit lead, no `the fix:`, stash lead, reminder lead).
- F-8 (old clause order in `gate_brief`): `Q-1 one outside: the clause stands before the colon (F-8)`.
- F-9 (`vcs_changes` without the None return): `F-9 vcs_commit` (4 rows), `F-9 vcs_stash` (4 rows), `F-9: vcs_changes is None when the status cannot be read`.
- F-2, F-3: structure; no behaviour row can go red (guarded by the existing rows, the census and the size limits).

## Tests added / changed expectations (old → new)

Added in `test_gate_preflight.py` (no new test file): `test_repo_words_a_glob_path_of_the_person_never_takes_the_factorys_file` (BL-1; ls-files literal; env), `test_repo_words_round_two_texts_records_and_edges` (F-1, F-4, F-5 commit and stash, F-6, F-7, F-9 commit and stash, `vcs_changes` None, edges: no stored door, empty door, a hook that fails silent); a row in the driver test (F-5 `failed` joins `failed`, record is a remark; F-6 the entry id reaches `run`). Added in `test_words_doors.py` `row_repo_words_cli`: a commit that landed wrong → exit 3 and one remark, no override.

Changed expectations:
- `test_gate_preflight.py` `words_run` helper: passes `finding_id` (new required argument of `run`) and optional `replaced`.
- Q-1 row: `... take exactly these:, files outside your tests folder included` → `your uncommitted changes (2), files outside your tests folder included, all listed - commit and stash take exactly these:` (F-8).
- `test_gate_preflight.py` K-B6 row ("the vcs finding is `vcs-test-repo`, in both branches"): it stubbed `_git` only and relied on a failed `status` read reading as "clean"; with F-9 that is no finding, so it now also stubs `_git_raw` for the `status` read (`""` and ` M a.py\0`). Same ids expected.
- `test_human_questions.py` (outside owns; allowed by the dispatch's siblings line): the pinned `action_lines.prefixes` list gained `to undo it:`, `to take them back:`, plus one row: every `done_prefixes` value stands in `prefixes`.

## The sentences, flags and exit codes B3's texts must follow

B3's texts (checked in `agent-a06a045949100fa96`: `conductor-actions.json`, `conductor.md`, `halts.md`, `s4.md`, `s9.md`, `state-exits.md`) say "the line it prints is told to the person as it stands" and name `repo_words.py --task <T> --word commit|stash --words-file <file>`: no CLI flag changed; no flag added. Differences the Lead may want mirrored (NOT edited by me):
1. The line the CLI/driver prints after a success: `the fix: undo it with ...` → `to undo it: `git reset --soft X`, then `git read-tree Y`.` and `the fix: take them back with ...` → `to take them back: `git stash apply --index X`; then remove the entry: ...`; the end-of-run line likewise (`to take them back: `git stash apply --index X`; afterwards `git stash drop stash@{N}` removes the entry.`). `state-exits.md` rows 133-134 say the same commands in other words and stay true.
2. CLI exit 3 now also covers a write that landed wrong (a commit that is not the shown set; a stash entry left): the word IS recorded as a remark and nothing is passed — B3's wording "a refusal is told to the person in words and nothing else runs" fits, but "nothing was done in the repository" does not hold for these two (the printed problem names the undo).
3. First `answers` line of the question: the clause moves before the colon (F-8).
4. Unreadable repository after a write: the problem says the result is not known and names the undo; exit 0 as for `still` (remark recorded).

## Findings outside the owns (reported, not edited)

- `test_person_owned_paths.py:289` pins "seven recording call sites" (`self.py("waiver.py"` in the driver sources, FAIL `K1 positive control: the seven recording call sites — expected 7, got 8`). The 8th is the repository word's record call that B2 round 1 added in `_record_door_lines` (HEAD has 3 sites in `driver_machine.py`, the worktree 4; round 2 added none). Not in my owns: the one-line fix is `7` → `8` in that row. It is the only red of the files run.
- `stage_guard.rule_stash` / `_names_factory` glob sibling (N-2) and the duplicate porcelain parsers (N-3), N-1: the verdict's node proposals, the Lead's.
- Same class near this diff: `onboard_apply.py:703` (`ls-files -z -- <home>`) and `regression_scope.py:99` (`ls-tree ... -- <text>`) hand a path to git as a pathspec too; the first is the factory's own folder name (no person path), the second a project path from a scope list. I did NOT change them (they go through their own `_git`; `literal` is an opt-in keyword of `gate_preflight._git`). Candidates for the same flag.

## Verification (verbatim)

Command 1 (the narrowed witness list the dispatch names): `python -B C:/QAFactory/forge-repo/.claude/worktrees/agent-a365d2def0628cb25/ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/repo_words.py ai-packages/qa-factory/scripts/gate_preflight.py ai-packages/qa-factory/scripts/gate_brief.py ai-packages/qa-factory/scripts/driver_machine.py ai-packages/qa-factory/references/human-text.json` printed 100 distinct test files. Each of the 78 whose recorded time in `scripts/slow_tests.json` is at most 60 s was run (one `python -B <file>` after another, one process each); closing lines (loop log, copied):

```
test_gate_preflight.py rc=0 127s | === gate rehearsal: 1442/1442 ok ===
test_gate_question_form.py rc=0 12s | === gate question form: 297/297 ok ===
test_gate_vocabulary.py rc=0 4s | === test_gate_vocabulary: 141/141 ok ===
test_human_questions.py rc=0 3s | === test_human_questions: 291/291 ok ===
test_driver_layers.py rc=0 13s | === test_driver_layers: 283/283 ok ===
test_gate_preflight_question_status.py rc=0 2s | === gate A: question status from the register: 25/25 ok ===
test_scenario_local_1_arm_b.py rc=0 11s | === scenario local-1-arm-b: 5/5 ok ===
test_scenario_walk.py rc=0 3s | === test_scenario_walk: 93/93 ok ===
test_scenario_world.py rc=0 1s | === test_scenario_world: 33/33 ok ===
test_whole_list_sites.py rc=0 7s | === test_whole_list_sites: 292/292 ok ===
test_person_owned_paths.py rc=1 11s | === person_owned_paths: 95/96 ok ===   (FAIL K1 positive control: the seven recording call sites — expected 7, got 8: see "Findings outside the owns")
```
All the other 67 files of the 78: `rc=0` (the full loop log lists each file with its `=== ... ok ===` line; one file, `test_gate_role_accounts.py`, has rc=0 and prints no `===` line).

Not run (22, over 60 s per `slow_tests.json`, CI judges them): test_branch_accounting, test_check_delivery, test_controller_gate_decision, test_gate_brief_and_retro, test_handoff_values_refusal, test_infra_failure_classify, test_infra_failure_retries, test_infra_failure_stops, test_infra_failure_texts, test_needs_author, test_no_mr_entry, test_scenario_cart_1, test_scenario_local_1_0108, test_silent_passes, test_story_run_arrival, test_story_run_refusals, test_story_run_s0, test_story_run_s3_windows, test_story_run_s6, test_story_run_stand_identity, test_window_record, test_words_doors. Of these, the new CLI row of `test_words_doors.py` was run alone through the scratchpad runner: worktree `32 pass, 0 fail` (red copy: `30 pass, 2 fail`, above). The `*` / `?` glob rows are skipped on Windows (names illegal here), CI judges them.

Command 2: `python -B .../scripts/tests/test_judgment_census.py` → `=== judgment_census: 22/22 ok ===` (ratchet `safety` 55, row `repo_words.py run` safety/intent unchanged).

Command 3: `python -B .../scripts/selftest.py --limits --lang` → `PASS limits: SKILL.md / agents / references within size caps`, `PASS limits: every mandatory role rule of design/role-rules.json holds in its carrier`, `=== qa-factory selftest: 4/4 ok ===`.

## Four questions / architecture

AR-13 (one env builder, one decision writer), AR-14, AR-19 (one executor), AR-1 (the prefix is a data row), AR-9 (every refusal names its door), AR-20 (census 55, unchanged), AR-22 (`failed`/`unread` have a producer and readers: `record_args`, driver, CLI), AR-24 (the person's word is kept whole in a remark on the failure roads), AR-28 (F-9). `judgment: none`. FR walk: A (refusals: F-5/F-9 texts name what was and the undo; door unchanged), B (text a person reads: F-4, F-7, F-8 keep the shape rules — `done_line` and `reminder_line` are checked by `human_text.problems`), C (contracts: `run`'s new argument has both callers and the tests), G (FR-30 English, `--lang` ok; FR-29 no control bytes).

## Needed beyond the manifest

`ai-packages/qa-factory/scripts/tests/test_human_questions.py` (edited: the pinned prefix list; allowed by the dispatch), `slow_tests.json` and `test_person_owned_paths.py` (read, red pin reported), `contract.py` (read), `human_text.py` (read), `waiver.py` (flags read), the other worktree's B3 texts (read by grep), `onboard_apply.py` / `regression_scope.py` (read by grep for the class).
