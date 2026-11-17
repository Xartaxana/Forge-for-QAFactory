# t-1213 report: bounded waits K-DOC + K-FIND + review leaving lines (worktree bw-int, no commit)

All edits are in `C:/QAFactory/forge-repo/.claude/worktrees/bw-int/` (twins of the owns). tools/ and .githooks/ not touched; no git state change.

## Items

1. Spec 6.1: RUNBOOK 9.1(f) already present :237 (identical to the quote). 9.8 part A already present :391-398 (identical to the quote) -> no edit, no duplicate.
2. Spec 6.2 part B appended to RUNBOOK 9.8 (FA = (a) text, FA(b) variant NOT applied), after the part A paragraph, before `### 9.9`. The 9.9 sentence appended at the end of the 9.9 paragraph (after «Число убитых — в дополнение к снимку.»); placement at the paragraph end is my reading of «§9.9 gains».
3. builder.md: rule 9 had a differently worded sentence on the same subject («a polling wait lasts no longer than the run itself and names the file it waits for and its end; an unbounded polling loop is forbidden, and a loop you leave running is named in your report»). The key phrase «A background wait names the file it waits for…» was absent, so the quoted sentence was ADDED after it (existing text kept). The two now overlap; see Questions.
   Calibration check 27: it had no item (e) (items a-d only), so (e) was ADDED after (d), with the quoted text plus R3: also `kept root=<pid>` lines and the `fails=` field.
   SIBLING_MAP axis 11: the quoted sentence appended to the end of the "Queued (C1, F-C4, t-120)" paragraph (the last line of the axis).
   PROJECT.md § Сессия форджа snapshot bullet: the stamp sentence inserted into the bullet (one added line).
4. Spec r2 (R3): the Log paragraph now lists `kept` and `fails=`; `status.json` keys read `trees_stopped, procs_stopped, procs_failed` (as tools/wait_reaper.py:463,537 prints); WAITS wording reads «<n> trees stopped, <m> processes failed, <u> unknown roots» (tools/wait_reaper.py:585); §6.3 check 27 (e) text carries the kept/fails= addition. Printed forms read in tools/wait_reaper.py :389-400 (log_line, `fails=<name/pid/outcome>;…`), :520-531 (`kept root=<pid>` via `log_line(..., "kept", proc=p)`), :585.
5. K-FIND: `plans/piles/onboarding-hooks/findings/20261117-unbounded-background-wait-of-a-role.md` (text of r2 §10 verbatim in «Что наблюдалось»; «Решение владельца нужно: нет.»), README «Содержание» row, batch-9 node OH9-9 (new node row; untaken, status ожидает). Prior-art grep over `plans/piles/*/findings` for `unbounded|ascii_clip|utility process|ASCII sanitizer|wait-loop|bounded wait` (-rl -i -E): empty; control with the same shape `-rl -i -E "unbounded|wait-loop"` over docs/tasks/specs found 3 files; separate control `Решение владельца нужно` in forge/findings: 89 hits.
6. Leaving lines. Reviews scanned for «узел: new»: t-1160 (Q4 line :133-134: N1, N6), t-1159 (grep `узел|node: new|new node|Node|leaving|new` -> none; same grep shape found the t-1160 lines), t-1177 (count 0 for `узел|node: new`; its G6/G7/R-items are fix-round/placement items, not "new node"). Filed in plans/piles/forge/findings/: `20261117-wait-reaper-walk-names-the-apps-utility-process.md` (N1), `20261117-ascii-sanitizer-seven-copies-converge.md` (N6); README rows x2; batch-7 nodes FG7-55 (N1), FG7-56 (N6), status ожидает. Direction «Lead, 17.11.2026», «Решение владельца нужно: нет».

## DOC-DISPATCH witness
Keys quoted from the dispatch DoD before the run. Script (full source, scratch only, not committed): `C:/Users/i_mas/AppData/Local/Temp/claude/b3e3188b390a00d9/501cb4e0-b55f-46d8-9262-11b1caefad61/scratchpad/kdoc_check.py`

```python
import sys, io
from pathlib import Path
ROOT = Path("C:/QAFactory/forge-repo/.claude/worktrees/bw-int")
def rd(p): return (ROOT / p).read_text(encoding="utf-8")
def between(t, a, b):
    i = t.index(a); j = t.index(b, i + len(a)); return t[i:j]
runbook = rd("docs/RUNBOOK.md")
s98 = between(runbook, "### 9.8. Фоновые ожидания", "### 9.9.")
s99 = runbook[runbook.index("### 9.9."):runbook.index("\n## 10.")]
spec = rd("docs/tasks/specs/20261117-bounded-waits-mechanism-spec-r2.md")
s52_53 = between(spec, "### §5.2 Stop and edges", "### §5.4")
s53 = between(spec, "### §5.3 Launcher", "### §5.4")
find_p = ROOT / "plans/piles/onboarding-hooks/findings/20261117-unbounded-background-wait-of-a-role.md"
keys = [
 ("RUNBOOK 9.8 heading", runbook, "### 9.8. Фоновые ожидания"),
 ("RUNBOOK 9.8 'останавливает'", s98, "останавливает"),
 ("RUNBOOK 9.8 tools/wait_reaper.py", s98, "tools/wait_reaper.py"),
 ("RUNBOOK 9.9 sentence", s99, "Остановку зависших фоновых вызовов этой сессии делает"),
 ("calibration UNBOUNDED WAITS:", rd("PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md"), "UNBOUNDED WAITS:"),
 ("calibration kept", between(rd("PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md"), "UNBOUNDED WAITS:", "28. **Completeness"), "kept"),
 ("SIBLING_MAP wrapper_forms", rd("docs/SIBLING_MAP.md"), "wrapper_forms"),
 ("PROJECT.md --stamp-narrative", rd("PROJECT.md"), "--stamp-narrative"),
 ("builder.md phrase", rd(".claude/agents/builder.md"), "A background wait names the file it waits for"),
 ("spec 5.2-5.3 log: kept", s52_53, "kept"),
 ("spec 5.2-5.3 log: fails=", s52_53, "fails="),
 ("spec 5.3 'trees stopped'", s53, "trees stopped"),
 ("K-FIND file exists", find_p.read_text(encoding="utf-8") if find_p.exists() else "", "Решение владельца нужно: нет"),
]
if "--negative" in sys.argv:
    keys.append(("NEGATIVE CONTROL absent key", runbook, "ZZZ-key-that-is-not-there"))
fails = 0
for name, text, key in keys:
    ok = key in text
    fails += not ok
    print(("PASS " if ok else "FAIL ") + name)
print("fails=%d" % fails)
sys.exit(1 if fails else 0)
```

Run: `python -B <scratch>/kdoc_check.py` -> exit 0:
```
PASS RUNBOOK 9.8 heading
PASS RUNBOOK 9.8 'останавливает'
PASS RUNBOOK 9.8 tools/wait_reaper.py
PASS RUNBOOK 9.9 sentence
PASS calibration UNBOUNDED WAITS:
PASS calibration kept
PASS SIBLING_MAP wrapper_forms
PASS PROJECT.md --stamp-narrative
PASS builder.md phrase
PASS spec 5.2-5.3 log: kept
PASS spec 5.2-5.3 log: fails=
PASS spec 5.3 'trees stopped'
PASS K-FIND file exists
fails=0
```
Negative control: `python -B <scratch>/kdoc_check.py --negative` (adds an absent key) -> `FAIL NEGATIVE CONTROL absent key`, `fails=1`, exit 1.

## Deviations / findings
- The DoD says «'kept' and 'fails=' in 5.2»; the Log paragraph (r2 :131) is physically under `### §5.3`, not §5.2 (the t-1177 R3 text also calls it §5.2). The script checks §5.2..§5.4 combined for kept/fails=, §5.3 alone for `trees stopped`.
- The reviews t-1159/t-1160/t-1177 exist only in the main root (not in the worktree); read from `C:/QAFactory/forge-repo/docs/tasks/specs/reviews/`.
- t-1160 N3 (kept line) and N7 are done in code per t-1177; not leaving lines.
- Finding files carry no «Правила и принципы» line (the spec gives none; I did not invent FR/AR citations).
- Not run: piles.py check (not in the DoD).

## Questions
1) builder.md rule 9 now says the same thing twice (old «polling wait …» sentence and the quoted «A background wait …» sentence). Replace the old clause with the quoted sentence, or keep both?
2) N1 finding: the review's fix is an either/or («image path + data row `claude-code`, or record a named residual»); the fork is left in the finding as the review wrote it. FG7-55/56 executor «designer → builder → critic» is my choice for a code node (the Lead may change it).
3) RUNBOOK 9.9 sentence placed at the end of the paragraph; confirm.

## Siblings noticed
- axis 1: other role files carrying the old builder rule 9 wording: none found beyond builder.md (not searched repo-wide).

Needed beyond the manifest: C:/QAFactory/forge-repo/docs/tasks/specs/reviews/ (main root), tools/wait_reaper.py (worktree), plans/piles/*/findings, ai-packages/qa-factory/scripts/guard_pre_tool.py (existence only).

## Update after the Lead's answers (t-1213)
- Q1: builder.md rule 9 de-duplicated. The old clause's overlapping parts (file+end, unbounded loop forbidden, loop left running named in the report) were dropped in favour of the quoted sentence; kept from the old clause: «Run a test synchronously when you can; a polling wait lasts no longer than the run itself.» and «(a count or seconds)», which the quoted sentence lacked (inserted into it after «its end»). Rule 9 now ends: `A background wait names the file it waits for and its end (a count or seconds); the gate refuses …`. Note: the exact quoted sentence now has «(a count or seconds)» inserted; the DoD key «A background wait names the file it waits for» still matches.
- Q2: the N1 finding now has «Развилка — Lead при взятии узла.» before the files line; executor unchanged.
- Q3: 9.9 placement kept.
- Re-run of kdoc_check.py (keys unchanged): 13 PASS, `fails=0`, exit 0; `--negative` -> `fails=1`, exit 1 (output below).
