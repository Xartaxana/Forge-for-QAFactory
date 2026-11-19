# t-1532 -- critic: narrow re-review of the FG7-88 card A fix round (t-1527 round 2), head b7e11ea4

Reviewed: `git -C <worktree agent-a5775220a29f5925e> diff 7ae89de7 b7e11ea4` (4 files, +15 -6) against the verdict
`docs/tasks/specs/reviews/t-1529-fg7-88-a-code.md` (F1-F3) and the dispatch's Lead decisions (F2 = drop the cap; F1 = one
row through `run_main('post-send')`; F3 = no whitespace-only hunk vs origin/main).

**Verdict: ACCEPT (fit) -- 0 blocking findings, 0 fixes.** All three findings are fixed; the rewritten guard keeps the
verdict of every E13 row; the probe killed both valid mutants. The acceptance stays the Lead's (rule 6).

## F1-F3

- **F1 fixed** -- `tools/test_journal_hooks.py:320` row `post-send-through-main` (steps `launch, stop, send:main`), driven at
  `:335-337` through `run_main("post-send", <stdin bytes>)`, parsing `hookSpecificOutput.additionalContext`. Red-before run by
  me (the builder ran none): mutant M1 (the `elif mode == "post-send":` of `main`, `tools/journal_hooks.py:596`, renamed so the
  branch is unreachable) -> exactly this row fails, `1 failed, 116 passed`, sha256 restored equal. The row asserts both the
  journal (`resumed` present) and the printed text count, so a branch that writes but prints nothing also fails it (`said`=1,
  `len(out)` must be 1).
- **F2 fixed** -- `AGENT_ID_MAX` and its check removed (`tools/journal_hooks.py:299`); case-sensitive grep `AGENT_ID_MAX` over
  `tools/` of the worktree = 0 hits (control: the same grep found it at 7ae89de7 per the diff's removed lines). The `to-huge`
  row (`tools/test_journal_hooks.py:345`, `"a" * 100000`) still passes: `[]` and journal bytes unchanged (in the 486-pass run).
- **F3 fixed** -- `git diff --stat origin/main...HEAD` and the same with `-w` over `tools/journal_hooks.py`
  `tools/test_session_context.py` print identical counts (58 / 9 lines, 1 deletion each way), so no hunk is whitespace-only;
  grep of the three-dot diff for `=re\.|=lambda|AGENT_ID_MAX` on +/- lines = 0. The one remaining deletion is the comment of the
  timed-out branch (`post-send stay silent` added), part of the task.

## The rewritten guard vs the E13 rows (traced)

`if transcripts.agent_file_name(to) is None or "agent_id" in payload: return []`. `post_send` passes `to` = None for every
non-dict payload or non-dict `tool_input`, so rows `empty`, `str`, `list`, `null`, `tool_input-int`, `no-to` short-circuit on
the first operand (the `in` on a str/list payload is never evaluated). `to-empty`, `to-int`, `to-path` (`../x`), `to-glob`
(`a*`), `to-non-ascii` (Cyrillic; `AGENT_ID_RE` `^[A-Za-z0-9_-]+$` is ASCII ranges) -> `agent_file_name` None -> `[]`. Only
`to-huge` changes path: it now passes the guard, `repo_root(cwd)`, `_locate` (read-only: `is_file` / tail reads; no write before
`write_event`), finds no `delegated` for that ref -> `None` -> `[]`; journal bytes unchanged. All 12 rows green in the run.
The `"agent_id" in payload` operand is load-bearing: M2 (drop it) -> row `send-inside-a-worker` fails.

## Standing questions (fix diff only)

- Q1 FIT: the three fixes as the Lead decided them. Q2 builder decisions: none new.
- Q3 SEAMS: test signature gains `monkeypatch, capsys` fixtures; additive.
- Q4 CLASS-WIDE: F1's class is "a mode of `main` with no row": `post-agent` and `pre-edit` already have `run_main` rows
  (round 1 trail, `tools/test_journal_hooks.py:490` table); no other mode in `main` (`:591-604`). F2's class, a second id
  acceptance form: now one form, `AGENT_ID_RE`, as the other producers. Residuals of round 1 (calibration_counts, liveness
  probe) unchanged, already handed to the Lead.
- Q5 TESTS: (a) M1 and M2 killed. (b) the row's expected `resumed` and `said`=1 trace to E1 of the card. (c) the `main` door now
  has a row. (d) none rewritten. (e) not a duplicate: the other rows call `jh.post_send` directly, this one the CLI mode.
  (f) +4 test lines vs -2 code lines in this round; whole branch remains under budget per round 1. (g) no new file.
- Q6 DUPLICATION AND CONSISTENCY: none found: the new branch reuses the file's existing `run_main` helper (`:89`), no second
  stdin driver.
- Q7 CODE QUALITY: none found; the test function grows by one 3-line branch, nesting 2.
- Q8 HYGIENE: no package path.
- Q9 IN-TREE RATCHETS: none touched (4 files, none a ratchet).
- Q10 ARCHITECTURE: unchanged from round 1 (AR-22 walk); VARIETY: n/a, a forge tool.
- Q11 JUDGMENT: none.
- Q12 ONE ROAD: none found: the diff's added lines carry no language/runner/project name (read, 15 lines).

## Spot-checks

- Builder witness "486 passed": reproduced, `486 passed in 69.66s`.
- `git -C <wt> status --porcelain` empty before the first mutant and after the last.

## Trail

Read: the t-1529 verdict; the fix diff; `tools/journal_hooks.py:280-330, 471-491, 580-607`; `tools/transcripts.py:44, 84-88`;
`tools/test_journal_hooks.py:85-95, 290-375`; report section "Round 2".

Commands (tails):
- `git -C <wt> rev-parse HEAD origin/main` -> b7e11ea4, 9ee5c5e2; merge base 29add319.
- `git -C <wt> diff [-w] --stat origin/main...HEAD -- tools/journal_hooks.py tools/test_session_context.py` -> both
  `2 files changed, 66 insertions(+), 1 deletion(-)`.
- `( cd <wt> && python -m pytest tools/test_journal_hooks.py tools/test_session_context.py -q -p no:cacheprovider )` ->
  `486 passed in 69.66s`.
- M1 runner -> `1 failed, 116 passed ... [post-send-through-main]`, sha256 equal=True, `outcome: killed`.
- M2 runner -> `1 failed, 116 passed ... [send-inside-a-worker]`, sha256 equal=True, `outcome: killed`.
- M3 runner -> `does not compile (SyntaxError ... line 299); nothing was touched`, `outcome: invalid` (my anchor replaced only
  the tail of `transcripts.agent_file_name(to)`; the cap of 3 runs was reached, no re-run).

```json
{
  "verdict": "fit",
  "blockers": [],
  "class_completeness": "F1 class (a main mode with no row): post-agent and pre-edit already have run_main rows; post-send now has one; no other mode in main. F2 class (second id acceptance form): removed, AGENT_ID_RE is the only form as in the other producers. Round 1 residuals (calibration_counts copies, hook_liveness_probe post-send case) unchanged and already with the Lead.",
  "trail": {
    "read": [
      "docs/tasks/specs/reviews/t-1529-fg7-88-a-code.md",
      "git diff 7ae89de7 b7e11ea4 (worktree agent-a5775220a29f5925e)",
      "tools/journal_hooks.py:280-330,471-491,580-607",
      "tools/transcripts.py:44,84-88",
      "tools/test_journal_hooks.py:85-95,290-375",
      "docs/tasks/handoffs/t-1527-fg7-88-a-report.md (Round 2)"
    ],
    "reruns": [
      {"command": "git -C <wt> diff --stat origin/main...HEAD and with -w, two files", "result": "identical: 2 files changed, 66 insertions(+), 1 deletion(-)"},
      {"command": "python -m pytest tools/test_journal_hooks.py tools/test_session_context.py -q (worktree)", "result": "486 passed in 69.66s"},
      {"command": "mutate_once.py --root <wt> --id M1-main-post-send --target tools/journal_hooks.py --test tools/test_journal_hooks.py --pytest", "result": "1 failed, 116 passed [post-send-through-main]; sha256 equal=True; outcome: killed"},
      {"command": "mutate_once.py --root <wt> --id M2-guard-worker-skip --target tools/journal_hooks.py --test tools/test_journal_hooks.py --pytest", "result": "1 failed, 116 passed [send-inside-a-worker]; sha256 equal=True; outcome: killed"},
      {"command": "mutate_once.py --root <wt> --id M3-guard-id-check --target tools/journal_hooks.py --test tools/test_journal_hooks.py --pytest", "result": "does not compile (SyntaxError line 299); nothing was touched; outcome: invalid"}
    ]
  },
  "mutants": [
    {"place": "tools/journal_hooks.py:596 main", "change": "elif mode == \"post-send\" -> elif mode == \"post-send-dropped\" (branch unreachable)", "run": "mutate_once.py --root <wt> --id M1-main-post-send --target tools/journal_hooks.py --test tools/test_journal_hooks.py --pytest", "outcome": "killed", "killed_by": "test_fg7_88_a_resumed_round_is_journaled_once_and_only_for_this_sessions_worker[post-send-through-main]"},
    {"place": "tools/journal_hooks.py:299 _post_send guard", "change": "dropped the 'agent_id' in payload operand", "run": "mutate_once.py --root <wt> --id M2-guard-worker-skip --target tools/journal_hooks.py --test tools/test_journal_hooks.py --pytest", "outcome": "killed", "killed_by": "test_fg7_88_a_resumed_round_is_journaled_once_and_only_for_this_sessions_worker[send-inside-a-worker]"},
    {"place": "tools/journal_hooks.py:299 _post_send guard", "change": "agent_file_name check replaced by an isinstance check (anchor error: did not compile)", "run": "mutate_once.py --root <wt> --id M3-guard-id-check --target tools/journal_hooks.py --test tools/test_journal_hooks.py --pytest", "outcome": "invalid", "remark": "critic's anchor error, not a product finding; cap reached"}
  ]
}
```
