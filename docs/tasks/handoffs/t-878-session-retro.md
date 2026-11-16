# t-878 session_retro handoff

branch: worktree-agent-a2a006db4d7e0dc7d ; commit sha: see the final message / `git log -1` (a file cannot hold its own sha)

## DoD run: `python -m pytest tools/test_session_retro.py -q`
```
.....                                                                    [100%]
5 passed in 17.85s
```

## Real run: `python -B tools/session_retro.py --dir C:/Users/i_mas/.claude/projects/C--QAFactory-forge-repo --last 1 --top 8`
```
## 501cb4e0-b55f-46d8-9262-11b1caefad61.jsonl
span: 2026-11-14T14:57:11.050Z .. 2026-11-16T21:39:01.890Z
operator messages: 2
compactions: 0
agent hand-backs: 4

tool calls: Bash 37, Edit 33, Read 28, Agent 7, mcp__ccd_turn__update_plan 3, Write 3, ToolSearch 1, mcp__ccd_session_mgmt__list_sessions 1, mcp__ccd_turn__wrap_up 1
agent launches: scout 6, builder 1

shell shapes (top 8):
- `grep -nE` x5
- `python -B` x4
- `date +%Y-%m-%dT%H:%M:%S;` x3
- `export PYTHONIOENCODING=utf-8;` x3
- `git -C` x3
- `sed -n` x2
- `tail -c` x2
- `ls -lt` x1

errors by class:

repeats:
- Read 4 times in a row: C:\QAFactory\forge-repo\.claude\worktrees\offload-land\docs\SIBLING_MAP.md
- Read 4 times in a row: C:\QAFactory\forge-repo\.claude\worktrees\offload-land\PROJECT.md

retries after a refusal: 0
```
(whole output; under 60 lines)

## Deviations / notes
- Real run passed `--dir`: the default dir is derived from the tool's own top path, which in a worktree is the worktree slug (no transcripts there); in the main checkout it equals C--QAFactory-forge-repo.
- Shape rule follows the spec literally (`VAR=value;` only): `export PYTHONIOENCODING=utf-8;` and `date ...;` keep the export word / trailing `;`, visible in the real run. Fork for Lead: also strip `export X=y;` and a trailing `;`?
- Operator message = user text not starting with `<` (harness tags / system reminders), not compaction, not hand-back (the spec did not define "system reminder" precisely).
- `--session` takes one or more values (nargs="+"); `--repeat-min` added as the spec's text names it.
- Read-run (b): any non-Read tool call between two Reads breaks the run.

## Needed beyond the manifest
none

## Test lines vs product lines
test 65, product 200 (ok).
