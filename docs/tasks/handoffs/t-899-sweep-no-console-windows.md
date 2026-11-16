# t-899 report: sweep without console windows

Done. `spawn_detached` (tools/worktree_sweep.py) on Windows now uses `CREATE_NO_WINDOW 0x08000000 | CREATE_NEW_PROCESS_GROUP 0x200` (DETACHED_PROCESS removed); `CREATE_BREAKAWAY_FROM_JOB` and the OSError fallback unchanged; non-Windows branch untouched; docstring now says "a hidden console (no window; children inherit it)".
Test pin (tools/test_worktree_sweep.py, test_w8_spawn_detached_...) updated to the new flags plus one assertion that bit 0x8 is not set in either call.

DoD: `python -B -m pytest tools/test_worktree_sweep.py -q -p no:cacheprovider`
Output (verbatim tail):
```
...............................s........................................ [ 49%]
........................................................................ [ 98%]
..                                                                       [100%]
145 passed, 1 skipped in 229.24s (0:03:49)
```

Children helper: git calls do NOT go through this module's own subprocess use; they go through `tools/gitcmd.py:44` (`subprocess.run(argv, capture_output=True, timeout=..., stdin=DEVNULL)`), a shared module outside `owns`. worktree_sweep.py has 1 Popen site (spawn_detached) and 0 other subprocess call sites. Per the spec I did not touch children. Defence in depth would be `creationflags=0x08000000` in gitcmd.py (single helper, 1 call site) -- question below.

Siblings (`git grep -n "0x00000008\|DETACHED_PROCESS" -- tools .githooks`): only one hit, tools/worktree_sweep.py:1215 (the one fixed here). No other DETACHED_PROCESS spawns in tools/ or .githooks.

Not verified on a desktop; the owner sees it at the next merge.

Questions: 1) Add `creationflags=0x08000000` (nt only) in tools/gitcmd.py:44 as defence in depth? It is a shared helper used by other tools, so I left it.
