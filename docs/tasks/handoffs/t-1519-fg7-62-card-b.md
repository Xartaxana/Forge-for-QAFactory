# t-1519 FG7-62 Card B -- report

Boot-file edits are STAGED (not committed). Committed by me: this report and `docs/tasks/compact-snapshots/2026-11-18-current-context-archive.md`.

## Result

`BOOT BUDGET:` before: `118404 bytes / 120000 (9 files) WARN | CLAUDE.md: 14495/16700`
after:  `114035 bytes / 120000 (9 files) WARN | CLAUDE.md: 14011/16700` -- no `missing`. Saved 4369 B (card ~5025; DoD band 3769-6281: inside).
Not at 108000 and not below 110000 on Card B alone: 114035. The card's Part L estimate (~5460) would give ~108575 -- F2 (a) band, not verified.
(Before is 118404, not the card's 118475: HEAD moved; measured in this worktree.)

Per file (bytes, `git show HEAD:` vs now): COORDINATOR.md 44213 -> 43156; PROJECT.md 35403 -> 33781; CLAUDE.md 14495 -> 14011; CURRENT_CONTEXT.md 1757 -> 551; AGENTS.md 117705 -> 114542 (not boot).

## Per move (net bytes saved, measured per cut)

| id | verdict | B |
|---|---|---|
| C1 | done | 473 |
| C2 | done | 199 |
| C3 | STAYED -- home lacks a clause (E3), see Question 1 | 0 (card 280) |
| C4 | done, fence verbatim in FULL new § | 221 |
| C5 | done, verbatim in FULL | 72 |
| C6 | done (verbatim copy also in FULL) | 92 |
| P1 | done | 375 |
| P2 | done | 166 |
| P6 | done | 237 |
| P3 | done | 178 |
| P8 | done | 123 |
| P4 | done | 214 |
| P5 | done (home = current DECISIONS.md header, which holds the clause today; re-read before cut) | 181 |
| P7 | done | 148 |
| K1 | done | 491 |
| B1 | done, archive | 350 |
| B2 | done, archive; the FG7-8 sentence STAYS (E4), t-073 sentence moved | 541 |
| B3 | done, archive | 246 |
| B4 | done | 69 |
| S9 | done (SIBLING_MAP row axis 31, Aspect cell +~55 B, not boot) | -- |

Sum of boot cuts 4369 = measured total drop.

## Deviations / findings

- C3 stayed: R-C3 drops «not merely the files the worker judges to be its own; another worker's uncommitted state can break a shared full run». `docs/TESTING.md` «Что запускать по своей правке» (:91-110) does not hold that clause (grep of `чужое|незакоммич|another worker|общий полный` found only :144, unrelated). The card says the home holds it; reality differs. E3 -> span stays.
- B2/E4: PC4-1 row (`plans/piles/package-ci/batch-4-*.md:22`) shows the owner-word wait (`слово владельца (вопрос выше) | ожидает`) -> t-073 sentence moved. No `changelog.d/` fragment names FG7-8 in its TEXT (case-insensitive grep over content: no hits; only the file NAME `fg7-8-b-vcs-words.md` does) -> the «`main` carries FG7-8 part B ... NOT in 0.11.0» sentence stayed in CURRENT_CONTEXT.md (ambiguity: «names» read as content).
- K1: R-K1 as written had «"cannot find tools/x.py"»; `pointer_lint` flagged `tools/x.py` as an untracked path (CLAUDE.md:98). Changed to «"cannot find" its tools/ script» (E10 wins over verbatim R-K1). AGENTS.md regenerated after.
- C1: R-C1 also replaces the paragraph about the project's rules and the factory-rules/AR-n paragraph (the quoted span :5-15 covers both) -- as the card says.
- Line endings: COORDINATOR/PROJECT/CLAUDE/CURRENT_CONTEXT/AGENTS are LF, FULL and SIBLING_MAP are CRLF at HEAD; each kept (script detects per file). Edits within a paragraph rewrapped only where the card text is a replacement.
- C5: after the cut `journal_keys.py declare repairs ...` sits on a long line (line 379, not re-wrapped, E8). C2/C6 likewise have one long line.

## Question for the coordinator

1) C3: cut it anyway (the clause «another worker's uncommitted state can break a shared full run» disappears, ~280 B), or first add that clause to TESTING.md, or keep as is?

## Fix-the-class notes (not done)

- Same long-line pattern at COORDINATOR.md C2/C5/C6 results; harmless.
- The card's S9 text says SIBLING_MAP axis-31 row is row 493; the line exists with Aspect text ending «rule 4a a trimmed ↔ full pair».

## Witness

```
$ python -m pytest tools/test_install_parity.py tools/tests/test_role_carriers_one_owner.py tools/test_pointer_lint.py -q
325 passed, 2 skipped in 140.49s (0:02:20)
$ python -B tools/pointer_lint.py --check      -> exit 0, "pointer_lint: ok (34 files, 1956 pointers)"
$ python -B tools/agents_md.py --check         -> exit 0, "AGENTS.md: up to date (114542 bytes)"
$ python -B tools/session_context.py </dev/null | grep "BOOT BUDGET"
BOOT BUDGET: 114035 bytes / 120000 (9 files) WARN | CLAUDE.md: 14011/16700
```

DOC-DISPATCH key run (script in full below; keys quoted from card §6 before the run; not committed):

```
KB-1..KB-9 present; KA-1..KA-7 absent; KV-1 C4 C5 B1 B2 B3 verbatim
RESULT PASS   (exit 0)
negative control (copy of COORDINATOR text with KB-1 removed in memory):
KB-1 MISSING
RESULT FAIL   (exit 1)
```

Script (`keys.py <worktree> [neg]`):

```python
import sys, subprocess, re
W = sys.argv[1]; neg = len(sys.argv) > 2
sq = lambda s: ' '.join(s.split())
rd = lambda p: sq(open(W + '/' + p, encoding='utf-8').read())
present = [
 ('KB-1','COORDINATOR.md','SCOPE OF THE WITNESS RUN:'),
 ('KB-2','COORDINATOR.md','scenario_walk.py --witness-for <owns>'),
 ('KB-3','COORDINATOR.md','(cheapest-tier-default rule)'),
 ('KB-4','COORDINATOR.md','(boot-context-is-expensive rule)'),
 ('KB-5','COORDINATOR.md','`.claude/agents/critic.md` rule 21'),
 ('KB-6','CLAUDE.md','subshell is the door'),
 ('KB-7','PROJECT.md','правило: `COORDINATOR.md` § Routing log'),
 ('KB-8','PROJECT.md','`docs/OWNER_PRINCIPLES.md` (они же FR-47…FR-57'),
 ('KB-9','CURRENT_CONTEXT.md','the SessionStart open-dispatch scan')]
absent = [
 ('KA-1','CLAUDE.md','Рабочий каталог шелла не меняется никогда'),
 ('KA-2','COORDINATOR.md','brief: what was delegated'),
 ('KA-3','COORDINATOR.md','id_band'),
 ('KA-4','PROJECT.md',"Couldn't find"),
 ('KA-5','PROJECT.md','здесь — коротко, для'),
 ('KA-6','CURRENT_CONTEXT.md','## Current Milestone'),
 ('KA-7','COORDINATOR.md','investigating the mechanics by reading is not')]
bad = 0
for k, f, s in present:
    t = rd(f)
    if neg and k == 'KB-1':
        t = t.replace('SCOPE OF THE WITNESS RUN:', '')
    ok = sq(s) in t; bad += not ok; print(k, 'present' if ok else 'MISSING')
for k, f, s in absent:
    ok = sq(s) not in rd(f); bad += not ok; print(k, 'absent' if ok else 'STILL PRESENT')
def head(p):
    return sq(subprocess.run(['git', '-C', W, 'show', 'HEAD:' + p], capture_output=True).stdout.decode('utf-8'))
c = head('COORDINATOR.md'); cc = head('CURRENT_CONTEXT.md')
spans = {
 'C4': (c, r'```json\s*\{"ts":"2026-11-11.*?```'),
 'C5': (c, r'Bands \(`id_band`\) are retired for new lines and still read in old ones;'),
 'B1': (cc, r'## Current Milestone.*?\(decisions O2, O3\)\.'),
 'B2': (cc, r'Release 0\.11\.0 is out.*?2026-11-16-2323-narrative\.md`\.'),
 'B3': (cc, r'The journal starts anew in this repository.*?`continues_from: t-NNNN`\.')}
home_f = rd('docs/CLAUDE_HOST_ADAPTATIONS_FULL.md')
home_a = rd('docs/tasks/compact-snapshots/2026-11-18-current-context-archive.md')
for k, (txt, rx) in spans.items():
    m = re.search(rx, txt, re.S); assert m, k
    ok = m.group(0) in (home_f if k in ('C4', 'C5') else home_a); bad += not ok
    print('KV-1', k, 'verbatim' if ok else 'NOT IN HOME')
print('RESULT', 'FAIL' if bad else 'PASS'); sys.exit(1 if bad else 0)
```

Note: KB-1 stays present only because C3 stayed. No test file added or changed; no config key; no changelog fragment (forge boot documents, no package path).

## Needed beyond the manifest

`plans/piles/package-ci/batch-4-*.md` (E4), `ai-packages/qa-factory/changelog.d/` (E4), `docs/RUNBOOK.md` §9 (P3 home), `DECISIONS.md` header (P5 home), `tools/pointer_lint.py`.
