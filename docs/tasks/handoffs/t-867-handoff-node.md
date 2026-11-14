# t-867 report: owner idea recorded as node RC2-8 (P1), roles-context batch 2

Branch `piles/handoff-by-code` from origin/main, pushed (not merged). Docs only. (Report is the worktree copy: the root path was refused for this isolated agent; it is NOT committed.)

## Done
1. Finding `plans/piles/roles-context/findings/20261114-handoff-sobiraet-kod-odna-sistema.md` (new, pile findings form). Contains owner words verbatim («владелец, 14.11.2026»), class, chosen direction (one table per contract, one assembler at `story_step start`, finish derivers = re-check, judgment fields empty, required/optional marks into the form file, s8.md:223-224 fix), full t-863 digest (facts, hand-copied list, forks, not-done) AND the full «Per-stage tables» (20 rows, read from the ROOT path after Lead's update), forks (a)/(b) with recommendation, links, next step.
2. Node row RC2-8 (П1) in `batch-2-slova-cheloveka-v-brife.md` (untaken, «ожидает»; next free id). Executor: designer -> critic on plan -> builder -> critic.
3. Card `README.md`: row in «Содержание» + RC2-8 added to batch 2's «Пачки» row.

## Witness
`python -B tools/piles.py check --all` tail: `(д) form: ok (33 piles, 103 batches)` / `(е) findings: ok (1107 findings read, 0 dated from 2026-10-13 on are orphans, ...)` / `piles check: ok`
`git show --stat HEAD`: 3 files changed, 109 insertions(+), 1 deletion(-): README.md, batch-2-slova-cheloveka-v-brife.md, findings/20261114-handoff-sobiraet-kod-odna-sistema.md.
Key-presence (script in full below, scratchpad, not committed):
```
keys [... 't-863', ... 'handoff_init'] -> OK
keys [... 'KEY_DELIBERATELY_ABSENT'] -> FAIL missing ['KEY_DELIBERATELY_ABSENT']
negative control reports failure: True
```
(Cyrillic keys printed as mojibake by the console only; the keys are `одна на всех`, `t-863`, `П1`, `handoff_init`.)
```python
import sys
W = r"C:\QAFactory\forge-repo\.claude\worktrees\agent-a4767519cf8b01ed4\plans\piles\roles-context"
files = [W + r"\findings\20261114-handoff-sobiraet-kod-odna-sistema.md", W + r"\batch-2-slova-cheloveka-v-brife.md", W + r"\README.md"]
text = "".join(open(f, encoding="utf-8").read() for f in files)
def run(keys):
    miss = [k for k in keys if k not in text]
    print("keys", keys, "->", "FAIL missing %s" % miss if miss else "OK")
    return not miss
ok = run(["одна на всех", "t-863", "П1", "handoff_init"])
neg = run(["одна на всех", "t-863", "П1", "handoff_init", "KEY_DELIBERATELY_ABSENT"])
print("negative control reports failure:", not neg)
sys.exit(0 if ok and not neg else 1)
```

## Deviations / notes
- Worktree started on 8fd381cc, not origin/main; created `piles/handoff-by-code` from origin/main.
- RC2-8 placed in batch 2 (the only untaken roles-context batch). The «Пишет в» list is my reading of the t-863 refs (handoff_init.py, handoff_check.py, story_step.py, phases/s8.md), not verified on disk; the spec may widen it.
- Commit message has `axes: not a mechanism (...)`.
- Handoff report root path refused by the isolation guard; this worktree copy is the report.

## Siblings
none. Needed beyond manifest: nothing beyond batch-2 file and two sibling findings (form).
