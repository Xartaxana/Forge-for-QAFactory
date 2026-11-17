# t-1008 — FG7-51 stream S1 (the CLAUDE side) — builder report

Nothing committed; everything staged in worktree `C:\QAFactory\forge-repo\.claude\worktrees\agent-ac0ebd53313b8a61e`
(CLAUDE.md, PROJECT.md, AGENTS.md regenerated, tools/tests/test_role_carriers_one_owner.py, this report).

## Done
- CLAUDE.md § Contents (line 9), 33 rows T1-T33, right after the title paragraph (cell grammar §4.1; topic names only).
- Headings added (CLAUDE.md, line numbers after the edit):
  - 9 `## Contents — topic → where to read`
  - 105 `### Rule 2 · drafting → designer` (before «DRAFTING → designer BY DEFAULT»)
  - 140 `### Rule 4 · witness scope and the BATCH CANON` (before «SCOPE OF THE WITNESS RUN»; a blank line splits a sentence boundary inside the rule-4 paragraph, whitespace only)
  - 235 `### Rule 10 · a change to the package`
  - 317 `### Rule 12 · Cost gates`
  - 383 `### Routing log · event SHAPES` (above the «Event SHAPES —» intro line, so the intro stays with its table)
  - 504 `### Command hygiene · point 6 — a claim needs a measurement`
  - 528 `### Command hygiene · point 7 — probes`
- C-H3 pointer line, CLAUDE.md:496, under hygiene pt. 3: `   why and how to recover: PROJECT.md § Сессия форджа` (text exactly as the spec quotes it, no final period).
- PROJECT.md:35 TOC row `| Все темы → `CLAUDE.md` § Contents | карта «тема → где читать» |` (the right-hand cell is mine: the spec gives only the left cell; ≤ 8 words).
- Test file: `TOC_POINTERS` (50 rows: 37 for CLAUDE TOC cells, 13 for PROJECT TOC incl. the new row), `POINTERS = POINTERS + TOC_POINTERS`; no new file.
- AGENTS.md regenerated: `python -B tools/agents_md.py --repo <worktree>` -> `wrote AGENTS.md: 107817 bytes`.

## TOC rows (cell text as written)
Tiers: CLAUDE.md § Tiers | Recon/builder/drafting: CLAUDE.md § 1 + § 2 (full form) + § Rule 2 · drafting → designer | Dispatch form: § 11 |
Witness: § 2 | What a builder may run: plans/builder-rules.md § 7b | Batch canon: CLAUDE.md § Rule 4 · witness scope and the BATCH CANON +
docs/RUNBOOK.md § 7. CI на GitHub и BATCH CANON | Which tests: docs/TESTING.md | Critic gate: § 3 | Critic review content:
docs/tasks/critic-diff-brief.md | Journal: § Routing log | Merge and CI reading: RUNBOOK § 7… + PROJECT.md § Командная работа (кучки и пачки) |
Six writers: PROJECT § Командная работа… | Cost gates: § Rule 12 · Cost gates | Session hygiene: § Command hygiene + PROJECT § Сессия форджа |
Command hygiene | Fix the class: § 9 | Mechanisms: § 10 | Piles: PROJECT § Командная работа… + docs/TEAMWORK.md | «Бэклог»: PROJECT § Бэклог и находки |
Owner's principles: docs/OWNER_PRINCIPLES.md | Package change: PROJECT § Как принимается изменение пакета | New idea: PROJECT § Как разрабатывается
новая идея владельца | Release: docs/RUNBOOK.md § 4.1. Шаги релиза | Language: PROJECT § Язык | Decide vs ask: PROJECT § Что решать самому, что
спрашивать у владельца + CLAUDE.md § 11a | Links: PROJECT § Ссылки на файлы в ответах | Hand-back form: `.claude/agents/<role>.md` | Readers of
touched files: .claude/agents/designer.md § 7 | Boot diet: .claude/skills/boot-diet/SKILL.md | Rule-text writing: PROJECT § Как пишутся правила для
агентов | Session start/end: PROCESS/SESSION_PROTOCOL.md | Degradation: § Role ≠ tier + § Lead degradation | Dispatcher duties: PROJECT § Как
принимается изменение пакета + PROJECT § Командная работа… (the file itself, lines 9-52, is the carrier).

## Measured sizes (carrier: `echo {} | python -B tools/session_context.py`, from the worktree)
`BOOT BUDGET: 109298 bytes / 120000 (4 files + 4 imports) WARN | CLAUDE.md: 50150/47800 incl. imports 98276 OVER -> boot-diet due`
- CLAUDE.md 47132 -> 50150 B: **2350 B over the 47800 cap** (S1 added 3018 B: TOC ~2.5 KB + headings/pointer ~0.5 KB).
- Boot total 109298: **1298 B over 108000** (the WARN line); under BREACH 120000.
- Not trimmed, no heading dropped (edges); the raise or the cut is the Lead's.

## Card items NOT done / questions for the Lead
1. **F19 outcome not stated in the dispatch.** I read «headings per F19» as F19 (a) (the spec's recommendation, §4.1 «a numbered rule is cited
   by number»): NO heading above numbered rules 1, 2, 3, 4, 4a, 5-9, 10, 11, 11a, 12, 13; only the sub-headings with exact text in §3.1. If the
   Lead decided F19 (b) (a heading above every rule), those headings have no text in the spec — a question; not done.
2. **Rule 11 sub-headings (C11a-e «### Rule 11 · …»)**: the spec gives no text for them -> NOT added (question: texts?).
3. **TOC cells the spec does not give literally** (derived by me from §2's «ONE home» column and the heading text on disk — please check):
   all rows but the three samples (Tiers, Recon, builder-rules 7b). Specific doubts: (a) T27 cell is the literal `.claude/agents/<role>.md`, not a
   resolvable path -> NO POINTERS row for it; (b) whole-file homes (TESTING, critic-diff-brief, OWNER_PRINCIPLES, SESSION_PROTOCOL, boot-diet,
   TEAMWORK) are written without `§` (grammar §4.1 has no form for a whole file); POINTERS rows anchor on the file's title line; (c) «Tiers» and
   «Routing log» cells are prefixes of the longer on-disk headings («Tiers (see DELEGATION_TABLE.md; …)», «Routing log — logs/journal/<dev>.jsonl»)
   as in the spec sample; (d) T30's home per spec is PROJECT § Как пишутся правила для агентов, but after S2's F4 its text lives in boot-diet SKILL.md
   (PROJECT keeps heading + pointer) — I cited PROJECT per spec; (e) the RUNBOOK cell uses the full heading «7. CI на GitHub и BATCH CANON».
4. **TOC size**: the F19 lever «CLAUDE TOC ≤ 2.0 KB» is not met (~2.5 KB); shortening cells is a decision for the Lead (it is the cause of most of the overshoot).
5. Critic t-999 «For S1» items outside the S1 card's word edits -> NOT done, Lead decides: (a) hygiene pt. 1 «(PROJECT.md, package change p. 2)» -> cite
   `docs/RUNBOOK.md` §7; (b) rule 4a «the rule text is PROJECT.md «Командная работа»» -> add «+ `docs/TEAMWORK.md`».
6. «Lead places» items outside my owns: none beyond the commit itself (CLAUDE.md, PROJECT.md are mechanism paths: Lead commits with axis block and `tier:`).
   `tools/install_parity_anchors.json` untouched (no anchored line changed; `install_parity.py --check` green).
7. DOC-DISPATCH key-presence run (TOC rows quote no OWNER_KEYS sentence): covered by the owned test `test_one_owner_per_key` (all 16 keys green, run below);
   no separate script was written.

## Siblings noticed
- `docs/CLAUDE_HOST_ADAPTATIONS_FULL.md` twin not touched (not required by the spec).
- The 4-import list in `test_agents_md.py` was already fixed by S2 per critic F7 (not re-checked beyond the green run).

## DoD output (verbatim)
```
$ python -m pytest tools/tests/test_role_carriers_one_owner.py tools/test_agents_md.py -q
162 passed in 11.10s
$ python -B tools/install_parity.py --check
MISSING (0)
UNKNOWN (0)
informational (0)
$ echo {} | python -B tools/session_context.py | grep 'BOOT BUDGET'
BOOT BUDGET: 109298 bytes / 120000 (4 files + 4 imports) WARN | CLAUDE.md: 50150/47800 incl. imports 98276 OVER -> boot-diet due (CLAUDE layer; report first, operator word starts it)
$ python -m pytest tools/test_session_context.py -q -k "budget or imports"
38 passed, 271 deselected in 4.08s
$ python -B tools/agents_md.py --check
AGENTS.md: up to date (107817 bytes)
```
Needed beyond the manifest: the spec §2 (topic map) and the heading lists of PROJECT.md, RUNBOOK, TESTING, brief, boot-diet, SESSION_PROTOCOL.
