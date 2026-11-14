# t-872 C1 fix round (commit 7704f734 on offload/c1, pushed)

Items:
- C1-0: not mine (landing condition: C1 merges after B0's Fable commit; header_ids still comes from B0's unstaged dispatch_manifest.py; Lead records it). No B0 grammar copied; B0 files not staged.
- C1-1: fixed. dispatch_new now calls dispatch_gate.decide_full (cwd = repo top, tool_name Agent, no description) and refuses with the hook's text. Rows: E-C1-5-missing-given (now exit 2), C1-1-new-owns-unmarked, C1-1-new-owns-marked, C1-1-critic-handoff-outside. A trailing " (new)" on an --owns item is kept outside the backtick span. The old "given not found" stderr note is removed (the hook now refuses).
- C1-2: fixed. Empty/whitespace --given/--owns item refused. Rows: C1-2-empty-owns-item, C1-2-empty-given-item.
- C1-3: fixed. --designer classified by dispatch_manifest._DESIGNER_SKIP_RE / _DESIGNER_RESUBMISSION_RE. Row: C1-3-designer-skip-case ("Skip -- tiny").
- C1-4: fixed inside dispatch_new: refuse when decision.cut is None or degraded. Test: test_degraded_cut_is_refused (monkeypatched decide_full).

Test changes: fixtures now use real files (the hook's path check stats them); round-trip test strips " (new)".

Witness:
`( cd .../offload-c1 && python -m pytest tools/test_dispatch_new.py -q )` -> `36 passed in 0.22s` (dirty tree with B0 patch; C1-0 stands).
Lines: dispatch_new.py 155, test_dispatch_new.py 120 (tests <= code).
`git show --stat HEAD`: tools/dispatch_new.py 58 +-, tools/test_dispatch_new.py 34 +-; 2 files, 69 insertions, 23 deletions.

Analogs noticed: none beyond the above. Note: a missing given path OUTSIDE the repo root is not refused by the hook (status "outside"), so the generator accepts it; this is the hook's behavior.
Needed beyond manifest: dispatch_gate.py (decide_full, Decision), dispatch_manifest.py (_DESIGNER_*_RE).
