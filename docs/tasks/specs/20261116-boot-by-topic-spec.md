# FG7-51 — the boot by topic: one home per topic, a table of contents, the boot under budget

task: t-894 (draft), t-912 (fix round 1 after plan critic t-903) | node: forge/7/FG7-51 | feature: F19 | designer, 17.11.2026 |
status: DRAFT after fix round 1 — forks F2/F3/F9 decided by the owner (17.11.2026), the rest by the Lead; new forks F17, F19 open
source: the owner's word 16.11.2026 (finding `plans/piles/forge/findings/20261116-but-odna-tema-v-mnogih-mestah-kopii-pravil-ustareli.md`,
item 2, direction (а)–(д) chosen); Lead intent brief of t-894; plan review `docs/tasks/specs/reviews/t-903-boot-by-topic-plan.md`
(verdict «go with fixes»); the owner's «да» of 17.11.2026 (§9 «Decisions in force»).

Reading rule: a byte figure marked **measured** comes from the t-903 review (its §5, `sed -n A,Bp FILE | wc -c`, and its BOOT
BUDGET re-run); «est.» is an ESTIMATE (lines × average bytes per line, or a row count × a row size) — the designer has no shell.
Every est. is re-measured by the stream that makes the move, with `python -B C:/QAFactory/forge-repo/tools/session_context.py`
(prints the BOOT BUDGET line; `.claude/skills/boot-diet/SKILL.md:21-24`).

Line numbers: CLAUDE.md lines are as of 16.11 (Q7) and serve only as locators — every row is identified by its quoted opener
text; PROJECT.md, `plans/builder-rules.md`, `docs/RUNBOOK.md`, `docs/TESTING.md` lines were re-read for this fix round (17.11,
before any stream). A stream that runs after another stream re-locates by the quoted text, never by the number.

---

## 0. Premises (each load-bearing fact, with its carrier)

| # | Fact | Carrier (file:line or command → output) |
|---|---|---|
| Q1 | Boot budget = files named by BOOT.md `Read X.md` lines + CLAUDE.md + CLAUDE.md's `@` imports, ONE level, no recursion | `tools/session_context.py:1042-1063` (regex `Read ([A-Z_]+\.md)`), `:1153-1162`; re-checked by t-903 §1 |
| Q2 | Thresholds: WARN > 108000, BREACH > 120000; CLAUDE.md own WARN 47800 | `tools/session_context.py:189-191`, `:214`; re-checked by t-903 |
| Q3 | **Measured** 17.11 (t-903 re-run): `BOOT BUDGET: 123942 bytes / 120000 (4 files + 3 imports) BREACH`; CLAUDE.md 43476, PROJECT.md 62252, FR index 5575, AR index 2682, DECISIONS.md 7547, CURRENT_CONTEXT.md 1783, SYSTEM_PROMPT.md 627 (sum 123942) | t-903 §1 row Q3 (`echo '{}' \| python -B tools/session_context.py \| grep BOOT`; `wc -c`) |
| Q4 | `agents_md.py` expands imports RECURSIVELY (MAX_DEPTH 5) — the budget counter does not | `tools/agents_md.py:35`, `:69-80` |
| Q5 | A real-repo pin of the import list | `tools/test_session_context.py:1185-1189` (`== ["PROJECT.md", "docs/FACTORY_RULES_INDEX.md", "docs/ARCHITECTURE_INDEX.md"]`) |
| Q6 | Subagents auto-load CLAUDE.md | `PROCESS/LEAD_RANKING_EXAM.md:19` |
| Q7 | CLAUDE.md: 446 lines (16.11); headings at 1, 21 (Tiers), 35 (Routing rules), 272 (Routing log), 350 (Role ≠ tier), 381 (Lead degradation), 403 (Command hygiene) | Grep of headings over CLAUDE.md, 16.11 |
| Q8 | PROJECT.md: 422 lines; headings 18, 36 (P1–P31, lines 41-174), 176, 235, 256, 279 (Командная работа, items 285-366, check line 368-369), 371 (Релиз), 381, 393, 407 | Read PROJECT.md:176-380 (17.11) |
| Q9 | One-owner + pointer test: 13 OWNER_KEYS, 20 POINTERS; scan excludes `plans/piles/`, `docs/tasks/specs/`, AGENTS.md; `squash()` = whitespace-collapsed + casefold | `tools/tests/test_role_carriers_one_owner.py:24-26, 35-74, 77-78` (read 17.11) |
| Q10 | Pinned: `cost:queue` key «в работе всегда шесть пишущих билдеров» owned by PROJECT.md; `scope:builder` key «не регрессия, не соседи, не большие файлы» and `scope:tests` key «Покрасневший пин удаляется, а не чинится» owned by builder-rules; PROJECT must hold «`plans/builder-rules.md` п. 7b» and «`docs/tasks/critic-diff-brief.md`»; builder-rules must hold «7b. **Уровень билдера и уровень пачки**» | same file :30, :40, :42, :49, :54-55 |
| Q11 | install-parity anchors quote CLAUDE.md lines (unit `routing-policy`, 89 anchors) and role-file rule openers; CI `--check`; no unit has host_path PROJECT.md or builder-rules; `install_parity.py --check` → `MISSING (0) … exit 0` today | `tools/install_parity_anchors.json`; `forge-check.yml:91,94`; t-903 §1 row Q11 |
| Q12 | No kit twin in this repo: `toolkit/` absent | Glob `toolkit/*` → none; control Glob `tools/install_parity*.py` → found |
| Q13 | Mechanism-gate net holds CLAUDE.md, BOOT.md, `.claude/agents/`, `.claude/skills/`, `PROCESS/`, `docs/SIBLING_MAP.md`, `tools/factory_rules_index.py`; NOT PROJECT.md, `plans/builder-rules.md`, `docs/RUNBOOK.md`, `docs/TESTING.md` | `tools/mechanism_gate.py:211-263`; re-checked by t-903 |
| Q14 | AGENTS.md is regenerated from CLAUDE.md + imports + settings + agents; `--check` in pre-commit and CI | `tools/agents_md.py:1-12`; `.githooks/pre-commit`; `forge-check.yml:80` |
| Q15 | boot-diet owns «how to diet»: moves VERBATIM with a pointer left behind | `.claude/skills/boot-diet/SKILL.md:9-11, 57-64, 98-105` |
| Q16 | SIBLING_MAP axis 31: «a new carrier of role text joins this table in the commit that creates it» | `docs/SIBLING_MAP.md:471-478, 552-557` |
| Q17 | `PARALLEL_CAP = 6`, door `budget-skip:` | `tools/dispatch_gate.py:1611, 1614` |
| Q18 | **Refreshed (m7):** the architect-tier spec IS on disk and tracked (`git status` at session start: ` M docs/tasks/specs/20261116-architect-tier-spec.md`); its Stream L (Lead's own, «after A-F are accepted») edits CLAUDE.md «Tiers», «Role ≠ tier», «Lead degradation», the Routing-log `by` paragraph, and adds a D entry to DECISIONS.md (in the boot) | Read `docs/tasks/specs/20261116-architect-tier-spec.md:447-456, 549-556`; §6 row `CLAUDE.md` `:429`, row `DECISIONS.md` `:430` |
| Q19 | **Refreshed (m7):** FG7-50's builder-rules part HAS landed (FG7-50 «принято: 263809e8 (t-891)», batch-7:73): `plans/builder-rules.md:10` carries the fixed language text, `:78` «FR-1…FR-59», `:37-38` «(критерий — список, а не длительность; узкий быстрый свидетель — до минуты каждый, `PROJECT.md` «Как принимается изменение пакета» п. 2)». FG7-50's CLAUDE.md part has NOT landed: live rule 12 reads «at most 6 parallel WRITING workers and a push before a worktree launch», live rule 6 carries no D-0046 line | Read `plans/builder-rules.md` whole (17.11); batch-7:73; CLAUDE.md as loaded into this session (rule 6, rule 12 Cost gates); t-903 §1 row Q19 (`grep -n "at most 6\|D-0046" CLAUDE.md` → :261, no D-0046) |
| Q20 | The parallel spec t-907 (`docs/tasks/specs/20261117-everything-in-piles-spec.md`), which owns the meaning of «Командная работа» п. 9, is NOT on disk yet | Glob `docs/tasks/specs/20261117-*.md` → none; control Glob `docs/tasks/specs/2026111*-*spec.md` → 47 files incl. `20261116-architect-tier-spec.md` |
| Q21 | `piles.py check` items: (а) placement, (б) overlap, (в) frozen, (г) backlog, (д) form (incl. the card's «## Содержание»), (е) findings-in-a-batch; every red names the door `piles-skip: <item> -- <reason>`; inside one developer (б) does not compare | `tools/piles.py:48, 58, 64, 135-143, 1573` |
| Q22 | Two index generators run separately: pre-commit `:54` `factory_rules_index.py --check`, `:58` `architecture_index.py --check` (AR tool has its own cap, ≤ 3 KB); tests `tools/test_factory_rules_index.py`, `tools/test_architecture_index.py` | Grep `index` over `.githooks/pre-commit`; Glob `tools/test_*index*.py` |
| Q23 | TESTING.md holds the builder's run as a bullet (`:80-81` «**Что запускать по своей правке**»), the builder line of «Кто что делает» (`:176-177`), `quarantine-watch` (`:82`) and «Удаление — `purge`, только по слову владельца» (`:87`) | Grep over `docs/TESTING.md` (17.11) |
| Q24 | RUNBOOK §7: `:90` «пуш ветки без PR ничего не запускает»; `:92-97` «Прогнать ветку»; `:99-103` «Слить принятое»; `:105-113` BATCH CANON incl. «Канон всегда на CI», «не больше часа», `:108` «После схождения веток интегратор прогоняет ветку»; `:115-121` «Что остаётся локально и почему» (`:115-116` local run «только когда CI недоступен или красный по причине раннера»); `:123-128` quarantine watcher | Read `docs/RUNBOOK.md:80-129` (17.11) |
| Q25 | The snapshot line for R1 is a Lead paraphrase («Шесть пишущих (дословно по смыслу) …»), not the owner's text | `docs/tasks/compact-snapshots/2026-11-17-0040-narrative.md:39-41` |

---

## 1. What changes, whom it serves, and the one invariant

### 1.1 What changes
1. Every topic of the boot and of the in-scope files gets ONE home (file + section); every other place keeps a one-line pointer
   `rule: <file> § <section>` (Russian files: `правило: <файл> § <раздел>`), no retelling (§2).
2. CLAUDE.md and PROJECT.md begin with a table of contents (§4).
3. A rule that one role executes lives in that role's file; the boot keeps routing and every DISPATCHER duty (§2).
4. One heading per topic; a section is about 40 lines at most; buried rules get their own heading (§3, §6; lever: F19).
5. Text that a gate holds, or that only a role or a moment needs, leaves the boot — at CLAUSE level (§5.1); the boot lands
   under 108000 B (est. ≈ 107.7 KB, §5.2; headroom is thin — F19).
6. Five listed resolutions (§3.3: R1–R5) are the only meaning changes.

### 1.2 The invariant and how it is checked
**INV-M: no rule changes its meaning.** Every edit of this node is one of exactly five kinds; anything else is a defect:

| Kind | What it may change | Mechanical check (data, code) | Judgment check |
|---|---|---|---|
| K1 heading added / text stays | inserts a heading line; touches no rule line | the opener line of every numbered rule stays byte-identical (install-parity anchors, Q11) | critic: the heading names the topic of what follows |
| K2 verbatim move | a whole paragraph / item / table, or a whole CLAUSE (sentence or `;`-segment), moves to another file; text identical after whitespace squashing (§7.4) | DOC-DISPATCH key-presence run (§7.4): key present in the destination, absent from the source | critic: the block's context did not carry meaning (e.g. «above», «(там же)») |
| K3 pointer left | the moved block's place holds `rule: <file> § <section>` plus, for a numbered item, its bold title verbatim; a pointer line may carry a short connective («При общем файле», «Диспетчеру:») listed in its row | the pointer resolves (POINTERS rows, Q9) | critic: the pointer says nothing the home does not |
| K4 restatement removed | a clause that restates its home is replaced by a pointer | the home holds the clause's key (squashed) — `present-in-home` | critic: the removed text was a restatement, not an extra clause — an extra clause moves (K2), never vanishes |
| K5 listed resolution | R1–R5 of §3.3 and nothing else | — | critic + the carrier quoted per row |

The diff critic verifies by the inventory (§3) and counts CLAUSE by clause wherever a row moves or replaces PART of an item
(§3.4 tables; review t-903 §4).

### 1.3 Owners of the checks this node adds or alters (rule 10 / P27 wording; the AR-29 census does not apply outside the package)
| Check | Owner it serves | Class |
|---|---|---|
| Pointer and TOC rows resolve (POINTERS rows of the existing test; FG7-52 extends the scan later) | data — code | shape / presence |
| One-owner keys follow their text (OWNER_KEYS `cost:queue` re-quoted, E19) | data — code | presence |
| install-parity anchors follow changed CLAUDE.md text | data — code | presence |
| The P index stays capped (S4: per line 220 B, per file 6144 B) | data — code | shape |
| BOOT BUDGET under 108000 | data — code (existing counter) | measure |
| «Meaning unchanged» per row of §3 | judgment — critic, accepted by the Lead | — |
| Retellings / sections over 50 lines / a boot heading with no TOC route (calibration check 33 line, m8) | judgment — calibration session (Architect/Lead) | — (on discipline until FG7-52) |
| What leaves the boot (§5), the resolutions (§3.3) | intent — the owner: decided 17.11.2026 (F2 b', F3 a, F9 a); R1 her word 16.11; R2, R3 Lead | — |

AR-n: none — `ai-packages/qa-factory/` is not touched (owns in §7 hold no package path). `architecture: none -- forge-only (boot and
role files)` on every commit; the FR walk is not required (PROJECT «Как принимается» п. 1 applies to the package).

### 1.4 Non-goals
- The CONTENT of «Tiers», «Role ≠ tier», «Lead degradation», the Routing-log `by` paragraph (architect-tier spec, Stream L, lands first).
- FG7-50's CLAUDE.md part (rule 12 «six is the target» wording, the D-0046 line in rule 6) — NOT landed (Q19); this spec's
  R1 alignment of rule 12 (row C12b) supersedes the rule-12 half of it; the D-0046 line stays the Lead's FG7-50 item.
- The MEANING of «Командная работа» п. 9 (owned by t-907, Q20; E20).
- The pointer linter itself (FG7-52 extends `tools/tests/test_role_carriers_one_owner.py`); §4.3 is its contract, kept as a note,
  not part of this node's DoD.
- DECISIONS.md, CURRENT_CONTEXT.md, SYSTEM_PROMPT.md, the generated FR/AR indexes (only their bytes are counted).
- The Routing log (F5 → c: nothing moves; no `docs/JOURNAL.md`, no mechanism-net row, no parity unit — m3, m4).
- Changing any gate's behaviour (`dispatch_gate` cap, `hygiene_gate`, `piles.py`); `CLAUDE_WARN` stays 47800.
- Folding the AR index generator into the FR/P generator (queued as a node, §7.6).
- Package files, kb/, the release repo; the batch files (rows for the Lead are ready text in §7.6).

---

## 2. THE TOPIC MAP (core deliverable)

Rule for choosing a home: **the home is the file of the party that EXECUTES the duty; the party that CHECKS it holds a pointer plus
at most one sentence of its own consequence** (axis 31 closing rule, `docs/SIBLING_MAP.md:552-556`). A DISPATCHER duty («a dispatch
that asks X is a coordinator defect») is executed by the dispatcher, so its home is the boot, never a worker file (t-903 B2).
Invariant: no rule sentence lives in two carriers; a checker never loses the sentence that tells it what to do when the rule bites.

| # | Topic | ONE home (file § section) | Why this home | Places that become pointers |
|---|---|---|---|---|
| T1 | Tiers | CLAUDE.md § Tiers | routing; content per architect-tier spec | DELEGATION_TABLE.md:3-5 (already a pointer) |
| T2 | Routing: recon → scout, implementation → builder, drafting → designer | CLAUDE.md rule 1, rule 2, § Rule 2 · drafting | coordinator executes | designer.md header, builder.md rule 1 (role duties, stay) |
| T3 | Dispatch form: DoD, edges, manifest, R11 | CLAUDE.md rule 11 (sub-headings, F1) | dispatcher executes | designer.md rule 1 (pointer, stays); builder.md rule 1, scout.md rule 5 (role consequences, stay) |
| T4 | Witness; acceptance by witness | CLAUDE.md rule 2 | coordinator accepts | builder.md 4, builder-rules 15, critic.md 7 (role consequences, stay) |
| T5 | What a builder may run (scope of its witness; CI not started/waited; who reads `main`'s pipeline) | `plans/builder-rules.md` § 7b (+ 7, 7a, 7c) | builder executes | CLAUDE.md rule 4 · witness scope keeps the DISPATCHER sentence; PROJECT «Как принимается» п. 2 builder clauses → K4 (§3.4a); PROJECT «Командная работа» п. 13 → pointer + the dispatcher sentence (§3.4d); TESTING.md:80-81 and :176-177 → pointer; critic-diff-brief:10-13 parenthetical → pointer |
| T6 | Batch canon: CI on the batch branch, who runs it, witness append; the integrator's local run | CLAUDE.md rule 4 · BATCH CANON (duty) + `docs/RUNBOOK.md` §7 (procedure, incl. the integrator's local run) | coordinator executes; RUNBOOK owns the recipe | PROJECT «Как принимается» п. 2 canon/integrator/fallback clauses → RUNBOOK §7 (K2/K4, §3.4a); builder-rules 7b integrator sentence → RUNBOOK §7 (F17); «what canon covers» stays in 7b |
| T7 | Which tests are written | `docs/TESTING.md` | its own text says so | CLAUDE.md rule 11 · which tests (pointer + battery duty, stays); builder-rules 7d (F14); builder.md 8, critic.md 20 (pointers) |
| T8 | Critic gate: when mandatory, two layers, plan gate, one pass per topic | CLAUDE.md rule 3 (+ R13 g) | coordinator decides | critic.md 9 (stays); PROJECT «Новая идея» п. 6, 8; «Как принимается» п. 6(б) (stay); PROJECT «Командная работа» п. 12 «Критик кода — один на тему, не на узел» stays K1 (a pointer would cost as many bytes) |
| T9 | Critic review content | `docs/tasks/critic-diff-brief.md` | critic executes | CLAUDE.md rule 3 «items 6-7», critic.md 18-20 (pointers, stay) |
| T10 | Journal: one writer, events, fields | CLAUDE.md § Routing log (whole; F5 → c) | coordinator writes | hygiene pt. 5 (stays); PROJECT «Командная работа» п. 5 stays whole (K1: its «`logs/routing-log.jsonl` — история до 08.10» is not in the home, so it is no restatement) |
| T11 | Merge and CI reading | `docs/RUNBOOK.md` §7 «Слить принятое» + PROJECT «Командная работа» п. 1 (who) | coordinator executes | CLAUDE.md rule 12 · what code does (stays); builder-rules 2 → R3 |
| T12 | Six writers, the full queue, merge waves | PROJECT «Командная работа» п. 12 (stays in the boot; R1 replaces only the cap sentences, §3.4c) | the owner's word; coordinator executes | CLAUDE.md rule 12 · Cost gates «at most 6 parallel WRITING workers and» → removed, «The cap» → «The writers» (pointer, C12b); `dispatch_gate.PARALLEL_CAP` unchanged |
| T13 | Cost gates | CLAUDE.md rule 12 · Cost gates | coordinator | builder-rules 16 (в), RUNBOOK (pointers, stay) |
| T14 | Session hygiene: shell cwd, connectors, compaction | CLAUDE.md hygiene pt. 3 (refusal) + PROJECT § Сессия форджа (new heading) | every session | PROJECT «Прогоны и эксперименты» PR5-PR7 → K2 into § Сессия форджа; CLAUDE.md Cost gates compaction clause → pointer (TR1); RUNBOOK:232 → re-pointed |
| T15 | Command hygiene | CLAUDE.md § Command hygiene | every session | builder.md 6, critic.md 11, scout.md 4 (stay) |
| T16 | Fix the class; sweep the artifact | CLAUDE.md rule 9 | coordinator; workers report | role files (stay); SYSTEM_PROMPT.md (stays) |
| T17 | Mechanisms | CLAUDE.md rule 10 | Lead | designer.md rule 1, builder-rules 19, boot-diet 7 (stay) |
| T18 | Piles and batches | PROJECT «Командная работа» (discipline clauses) + `docs/TEAMWORK.md` (CLAUSES refused by `piles.py check`/`close` with a door; §3.4b) | integrator / coordinator; `piles.py` gates | CLAUDE.md rule 4a (pointer, stays); critic-diff-brief question 4 (stays) |
| T19 | «Бэклог» — the owner's word; findings | PROJECT § Бэклог и находки (new heading) | every session | PROJECT «Как принимается» п. 4 → numbered pointer line |
| T20 | Owner's principles P1–P31 | `docs/OWNER_PRINCIPLES.md` (bullets verbatim) + generated capped index imported into the boot | the index routes; the text is read by package work | PROJECT § Принципы владельца → intro + pointer; «PROJECT.md P31» citations resolve in 2 hops |
| T21 | Package change acceptance | PROJECT § Как принимается изменение пакета | Lead / builder / critic | CLAUDE.md rule 10 · a change to the package (different topic, stays) |
| T22 | A new idea of the owner | PROJECT § Как разрабатывается новая идея владельца | Lead | none |
| T23 | Release | `docs/RUNBOOK.md` § 4.1 (new sub-heading «### 4.1. Шаги релиза») | release session only | PROJECT § Релиз → one pointer line |
| T24 | Language | PROJECT § Язык | every session | builder-rules 3 (already points there) |
| T25 | Decide vs ask; owner away | PROJECT § Что решать самому + CLAUDE.md rule 11a | two topics, cross-pointed | none |
| T26 | Links in answers | PROJECT § Ссылки на файлы в ответах | every session | none |
| T27 | Hand-back form per role | `.claude/agents/<role>.md` | owner keys Q9 | builder-rules 11, critic-diff-brief «What comes back» (stay) |
| T28 | Readers of every touched file (designer duty) | `.claude/agents/designer.md` new rule 7 (K2 out of rule 3) | designer executes | none |
| T29 | Boot diet procedure | `.claude/skills/boot-diet/SKILL.md` | procedure owner | §6 points to it |
| T30 | How rule text for agents is written | PROJECT § Как пишутся правила для агентов (new, F12 a) | anyone editing | none |
| T31 | Session start/end | `PROCESS/SESSION_PROTOCOL.md` | Lead | BOOT.md (stays) |
| T32 | Degradation, Role ≠ tier | CLAUDE.md § Role ≠ tier, § Lead degradation (names per architect spec) | coordinator | critic.md 9 (stays) |
| T33 | Dispatcher duties about workers' runs: one wait loop per round; no dispatch asks for more locally / for CI / a pipeline wait / mutations | PROJECT «Как принимается» п. 2 (the «Диспетчеру:» line) + «Командная работа» п. 13 (its one sentence) | dispatcher executes (t-903 B2, B3) | builder-rules 7b:53-54 keeps the integrator's consequence «интегратор пишет это строкой отчёта и не гоняет» (checker's one sentence) |

Empty-topic rule: a topic with no home gets `home: none — queued <node>`, never an invented home. None found.

---

## 3. Inventory «rule: was where → is where»

Rule numbers stay stable: every «CLAUDE.md rule N», «hygiene point N», «R11-f», «pt.6 b», «PROJECT «Командная работа» п. N»,
««Как принимается» п. N», «P<n>» resolves in at most two hops (E1–E3). No number is moved, reused or deleted. «stays» = K1.
Rows that move or replace PART of an item point to the clause tables of §3.4.

### 3.1 CLAUDE.md (identified by opener; lines as of 16.11)

| ID | Was (line, opener) | Is where | Kind | Stream |
|---|---|---|---|---|
| C0 | 1-19 title, purpose, `@PROJECT.md`, `@docs/FACTORY_RULES_INDEX.md`, `@docs/ARCHITECTURE_INDEX.md` | stays; `@docs/OWNER_PRINCIPLES_INDEX.md` added on its own line right after `@docs/ARCHITECTURE_INDEX.md` (S2); § Contents inserted after line 6 (S1, §4) | K1 + import line | S2 (import), S1 (TOC) |
| C-T | 21 «## Tiers» | stays by name (content: architect spec) | K1 | S1 |
| C1 | 37 «1. Recon → scout by default» + R1 a/b | stays; heading per F19 | K1 | S1 |
| C2a | 51 «2. Implementation from a finished spec → builder» | stays; heading per F19 | K1 | S1 |
| C2b | rule 2 «DRAFTING → designer BY DEFAULT» … | stays; sub-heading «### Rule 2 · drafting → designer» at its paragraph boundary | K1 | S1 |
| C3 | 70 «3. critic — a MANDATORY acceptance gate» | stays; heading per F19 | K1 | S1 |
| C4a | 87 «4. Independent parts → several parallel subagents» | stays; heading per F19 | K1 | S1 |
| C4b | rule 4 «SCOPE OF THE WITNESS RUN» … `defect_found` | stays; sub-heading «### Rule 4 · witness scope and the BATCH CANON» | K1 | S1 |
| C4c | 103 «4a. A task spanning 5 or more journal events» | stays; heading per F19 | K1 | S1 |
| C5 | 107 «5. Flat delegation» | stays (anchor «5. Flat delegation (flat delegation rule):» kept, architect spec :429) | K1 | S1 |
| C6 | 109 «6. Escalation» | stays (no D-0046 line on disk, Q19) | K1 | S1 |
| C7 | 115 «7. Background execution by default» | stays | K1 | S1 |
| C8 | 125 «8. Universal skip rule» | stays | K1 | S1 |
| C9 | 140 «9. Fix the class» | stays | K1 | S1 |
| C10a | 156 «10. Four questions for every mechanism» | stays | K1 | S1 |
| C10b | rule 10 «A change to the package (D-0055, D-0060; P27)» | stays; sub-heading «### Rule 10 · a change to the package» | K1 | S1 |
| C11a-e | 187 «11. DoD in every dispatch» and its parts (which tests; scout/critic DoD + manifest; five-point checklist + doc-dispatch witness; R11 table) | stays; sub-headings «### Rule 11 · …» at paragraph boundaries (F1 a) | K1 | S1 |
| C11f | 239 «11a. Question routing» | stays | K1 | S1 |
| C12a | 250 «12. The coordinator's cadence» | stays | K1 | S1 |
| C12b | rule 12 «Cost gates (D-0035, …)» | stays (anchor COST); sub-heading «### Rule 12 · Cost gates» (S1). Two edits in S2 (with R1 and PR7, one commit): (1) «at most 6 parallel WRITING workers and a push before a worktree launch (`tools/dispatch_gate.py`). The cap, the FULL queue, the per-topic critic and merge waves: PROJECT.md «Командная работа» п. 12.» → «a push before a worktree launch (`tools/dispatch_gate.py`). The writers, the FULL queue, the per-topic critic and merge waves: PROJECT.md «Командная работа» п. 12.» (R1 alignment); (2) «the Lead compacts at ~300K at a stage boundary» → «the Lead compacts by PROJECT.md § Сессия форджа» with «на границе стадии» carried there (TR1, F8 a) | K1, K5 (R1 place), K4 + TR1 | S1 heading; S2 edits |
| C13 | 264 «13. Leaf routing» + R13 g | stays | K1 | S1 |
| C-RL1..4 | 272 «## Routing log» — whole section incl. typed fields `feature: Fnn`, ids, letters, retro, SHAPES | stays whole (F5 → c, m3/m4); sub-heading «### Routing log · event SHAPES» above the table only | K1 | S1 |
| C-RT | 350 «## Role ≠ tier» | stays by name (content: architect spec) | K1 | — |
| C-LD | 381 «## Lead degradation» | stays by name (content: architect spec) | K1 | — |
| C-H0 | 403 «## Command hygiene» intro, doors | stays | — | — |
| C-H1..5 | «1. Tests» … «5. Log entries» | stay; pt. 3 gains one pointer line «why and how to recover: PROJECT.md § Сессия форджа» | K1, K3 | S1 |
| C-H6 | «6. An environment-negative claim» + pt.6 table | stays; sub-heading «### Command hygiene · point 6 — a claim needs a measurement» | K1 | S1 |
| C-H7 | «7. Temporary corruption» | stays; sub-heading «### Command hygiene · point 7 — probes» | K1 | S1 |

Count: 13 numbered rules + 4a + 11a, 3 tables (R1, R11, R13) + pt.6 table, 4 unnumbered sections, hygiene 1-7 — every one has a row.

### 3.2 PROJECT.md (lines re-read 17.11)

| ID | Was (line, opener) | Is where | Kind | Stream |
|---|---|---|---|---|
| P-0 | 1-16 two rule sets | stays; § Оглавление after line 16 (§4; lands in S2, its row «Все темы → CLAUDE.md § Contents» lands in S1, E21) | K1 | S2, S1 |
| P-W | 18 «## Где что лежит» | stays; + rows `docs/OWNER_PRINCIPLES.md`, `docs/TEAMWORK.md` | K1 (+rows) | S2 |
| P-PI | 36-40 principles intro «Они же стоят правилами FR-47…FR-57…» | stays + one line «Полный текст P1–P31 — `docs/OWNER_PRINCIPLES.md`; первая фраза каждого — индекс `docs/OWNER_PRINCIPLES_INDEX.md`, импорт из `CLAUDE.md`.» | K3 | S2 |
| P1…P31 | 41-174, `- **P<n>.**` bullets (P1 41 … P31 173) — **measured 22318 B** | each → `docs/OWNER_PRINCIPLES.md`, same bullet VERBATIM (`- **P<n>.** …`, a true K2, m2), in source order; range sub-headings K1 (§10) | K2 | S2 |
| PA1 | 178 «1. **Проход по правилам фабрики.**» | stays; heading «### Пакет: проход и свидетель» above п. 1 | K1 | S2 |
| PA2 | 187-210 «2. **Свидетель билдера**» — **measured 3820 B** | clause table §3.4a | K1/K2/K3/K4 | S2 |
| PA3 | 211 «3. **Доказанность.**» | stays; heading «### Пакет: доказанность, эталон, смысл» above п. 3 | K1 | S2 |
| PA4 | 213 «4. **Бэклог.**» | number stays: «4. **Бэклог.** — правило: § Бэклог и находки»; text K2 into the new «## Бэклог и находки» (inside the boot, after «Как принимается») | K2, K3 | S2 |
| PA5 | 218 «5. **Шаг, переведённый из роли в код…**» | stays | K1 | — |
| PA6 | 224 «6. **Спека, меняющая смысл…**» | stays | K1 | — |
| PN | 235-254 «Как разрабатывается новая идея владельца» | stays | — | — |
| PR1-PR4 | 258-266 four bullets of «Прогоны и эксперименты» | stay | — | — |
| PR5 | 267-271 «**Рабочий каталог шелла не меняется никогда**…» | → new «## Сессия форджа» (bullet whole; it adds PowerShell detail and the recovery step to hygiene pt. 3) | K2 | S2 |
| PR6 | 272-273 «**Коннекторы выключены**…» | → § Сессия форджа | K2 | S2 |
| PR7 | 274-277 «**Сжатие контекста ничего не останавливает**…» | → § Сессия форджа; TR1: «на ~300K контекста» → «на ~300K контекста, на границе стадии,» (the clause from CLAUDE.md C12b, F8 a) | K2 + TR1 | S2 |
| PT0 | 279-284 «Командная работа» intro | stays | — | — |
| PT1 | 285 «1. **Пачку берёт один разработчик**» | stays | — | — |
| PT2 | 289-302 «2. **Взятая пачка заморожена**» — **measured 2334 B** | clause table §3.4b | K2, K3, K1 | S2 |
| PT3 | 303-308 «3. **Зоны файлов пачек…**» — **measured 996 B** | clause table §3.4b | K2, K3, K1 | S2 |
| PT4 | 309-311 «4. **`plans/BACKLOG.md` заморожен**» — **measured 436 B** | clause table §3.4b | K2, K3, K1 | S2 |
| PT5 | 312-317 «5. **Общие файлы — один писатель**» | stays WHOLE (class sweep: its journal clause carries «`logs/routing-log.jsonl` — история до 08.10, только чтение», which the home lacks → not a restatement) | K1 | — |
| PT6 | 318 «6. **Слово владельца — только от владельца**» | stays | — | — |
| PT7 | 323 «7. **Доски нет**» | stays | — | — |
| PT8 | 325 «8. **Двери**» — **measured 360 B** | clause table §3.4b | K2, K3 | S2 |
| PT9 | 326-341 «9. **Пачка закрывается доделкой…**» — **measured 2889 B**; text owned by t-907 (E20) | clause table §3.4b | K2, K3, K1 | S2 |
| PT10 | 342 «10. **Знание — в проекте…**» | stays | — | — |
| PT11 | 346 «11. **Узел пачки пишется для более слабой модели**» | stays | — | — |
| PT12 | 353-360 «12. **Темп координатора**» | clause table §3.4c: R1 replaces ONLY the cap sentences; every other clause K1 | K5, K1 | S2 |
| PT13 | 361-366 «13. **Проверки билдера**» — **measured 1058 B** (361-367) | clause table §3.4d | K2, K4, K1, K3 | S2 |
| PT-check | 368-369 «Проверка на пути исполнения: `tools/piles.py check --msg-file`…» — **measured 221 B** | → `docs/TEAMWORK.md` (K2); PROJECT keeps «Проверка на пути исполнения и детектор — `docs/TEAMWORK.md`.» | K2, K3 | S2 |
| PRel | 371-379 «## Релиз» — **measured 1807 B** | → `docs/RUNBOOK.md` «### 4.1. Шаги релиза» (end of §4, before «## 5.»); PROJECT keeps «## Релиз» + «Правило: `docs/RUNBOOK.md` § 4.1.» | K2, K3 | S2 |
| PL | 381 «## Язык» | stays | — | — |
| PD | 393 «## Что решать самому…» | stays | — | — |
| PS | 407 «## Ссылки на файлы в ответах» | stays | — | — |
| P-new | — | new «## Сессия форджа», «## Бэклог и находки», «## Как пишутся правила для агентов» (§6 text, F12 a) | K1/K2 | S2 |

Count (m13): P1-P31, «Как принимается» 1-6, «Новая идея» 1-8, «Командная работа» 1-13 + check line, **7** bullets of «Прогоны»
(PR1-PR7), the unnumbered sections — every one has a row.

### 3.3 Resolutions (K5 — the ONLY meaning changes, each with its carrier)

| R | Contradiction (carriers) | Resolution in the home | Carrier | Places aligned |
|---|---|---|---|---|
| R1 | six writers: PROJECT п. 12 «в работе всегда шесть пишущих билдеров … меньше шести — только по слову владельца …», «Шесть — не потолок: седьмого координатор берёт, когда надо (упал мерж)» vs CLAUDE.md rule 12 «at most 6 parallel WRITING workers» | ONLY the cap sentences of п. 12 are replaced by the owner's words (§3.4c gives the ready text); every other clause of п. 12 stays verbatim | the owner's message of 16.11.2026 evening in the Lead session (m12); the exact words reached this spec through the t-894 Lead brief; `docs/tasks/compact-snapshots/2026-11-17-0040-narrative.md:39-41` is a Lead paraphrase («дословно по смыслу») cited as the locator only, never as the text (PROJECT «Командная работа» п. 6) | CLAUDE.md C12b (1); OWNER_KEYS `cost:queue` re-quoted «цель держать 6 пишущих билдеров» (E19); `PARALLEL_CAP = 6` unchanged (Q17); SIBLING_MAP:532 unchanged (still names rule 12 and п. 12) |
| R2 | witness duration: builder-rules 7b «узкий быстрый свидетель — до минуты каждый» (:38), 7c «(меньше минуты каждый)» (:57), PROJECT «Как принимается» п. 2 «(до минуты каждый)» | no minutes number in the builder's rule: the criterion is the slow list (`SLOW_TESTS`, `test_story_run_*`, `test_controller_*`, `test_fixes_13797`, `test_story_step.py`) | a Lead decision of 16.11.2026, told to the owner and marked «решила сама» (snapshot :43); written as the Lead's, stays unless the owner objects; NOT covered by the owner's «да» of 17.11 (that answer covered the forks put to her) | builder-rules 7b, 7c; PROJECT п. 2 (its clause K4'd, §3.4a); TESTING.md «10 с на новый файл» is a different rule (file budget) and stays. Lands in ONE commit (S2), never split across streams (t-903 §7) |
| R3 | who merges and who runs the canon: builder-rules 2 «Мерджи, пуши, переключение веток — только интегратор»; 7b:42 «интегратор делает один прогон BATCH CANON»; RUNBOOK:108 «После схождения веток интегратор прогоняет ветку» vs PROJECT «Командная работа» п. 1 (`wave.py merge` by the coordinator), п. 13 «Канон запускает и читает координатор после слияния», CLAUDE.md rule 4 «the coordinator's duty» | merges: the coordinator (`tools/wave.py merge`); the canon run: the coordinator (RUNBOOK §7); the integrator closes the batch (`piles.py close`); pushes are not re-assigned | the boot's own text: PROJECT «Командная работа» п. 1 and п. 13 (the owner's word 14.11.2026; RUNBOOK:99) — R3 aligns the worker docs to the home | builder-rules 2 (S3), 7b:42 (S3), RUNBOOK:108 (S2) |
| R4 | language (fixed by FG7-50, Q19) | PROJECT «Язык» unchanged | — | none left |
| R5 | local fallback run: PROJECT п. 2 «только по слову владельца и никогда не параллельно с другим» and RUNBOOK:115-116 «только когда CI недоступен или красный по причине раннера» (compatible, m1) | both sentences verbatim side by side in RUNBOOK §7 «Что остаётся локально и почему», followed by the one explicit clause «(оба условия вместе — слово владельца 17.11.2026)» | the owner's «да» of 17.11.2026 to F9 (a), Lead session | RUNBOOK §7 only (S2) |

### 3.4 Clause tables (rows that move or replace PART of an item; the diff critic counts these clause by clause)

Every K2/K4 row's key is the clause text itself, compared squashed (§7.4). «→ boot» = stays in PROJECT.md.

#### 3.4a PROJECT «Как принимается» п. 2 (187-210; t-903 B3)

| # | Clause (verbatim opener … end) | Lines | Destination | Kind | K-check |
|---|---|---|---|---|---|
| 2-1 | «2. **Свидетель билдера** — вывод проверки, а не пересказ.» | 187 | → boot (number + title) | K1 | opener byte-identical |
| 2-2 | «Объём проверки билдера и канон пачки — текст правила `plans/builder-rules.md` п. 7b (D-0056); … Форма отчёта — правило 7 `.claude/agents/builder.md`, содержание — builder-rules п. 11.» | 187-192 | → boot (already pointers; keeps both pinned strings, Q10) | K1 | POINTERS rows PROJECT→7b, PROJECT→critic-diff-brief green |
| 2-3 | «**Тесты идут в CI, не на машине разработчика, и их не ждут на машине**:» | 193 | home: builder-rules 7b («билдер НЕ гоняет и не ждёт») + RUNBOOK §7 | K4 | 7b holds «НЕ гоняет и не ждёт» |
| 2-4 | «билдер гоняет только быстрые узкие свидетели своих путей (до минуты каждый), коммитит и сдаёт;» | 193-194 | home: builder-rules 7b «**точечные проверки своей правки**» (R2: the minutes number is dropped with it) | K4 + R2 | 7b holds «точечные проверки своей правки» |
| 2-5 | «медленный файл (`SLOW_TESTS`, `test_story_run_*`, `test_controller_*`, `test_fixes_13797`) локально не запускается и не ждётся — его судит CI;» | 194-196 | home: builder-rules 7b:35-37 | K4 | 7b holds «`SLOW_TESTS`» and «`test_fixes_13797`» |
| 2-6 | «цикл ожидания в диспатче — один на раунд, с капом, и только на то, что нельзя прочитать иначе (вопрос драйвера; пайплайн — только интегратору, «Командная работа» п. 13).» | 196-197 | → boot, the «Диспетчеру:» line (B3, Lead: the dispatcher reads it there) | K1 (+K3 connective) | present in PROJECT.md |
| 2-7 | «Задача на один инструмент в `tools/` не требует полного `pytest tools/`: свидетель — тест инструмента, полный прогон — при интеграции.» | 197-198 | home: CLAUDE.md rule 4 (an owned path outside the package: «the test file that judges the path») + builder-rules 7b («`pytest tools/` целиком … идут пайплайном») | K4 | CLAUDE.md holds «the test file that judges the path»; 7b holds «`pytest tools/` целиком» |
| 2-8 | «**Канон всегда на CI** (D-0059): BATCH CANON пачки и канон релиза — пайплайн CI на ветке, не больше часа, а не прогон на этой машине;» | 199-200 | home: RUNBOOK §7:105-108 | K4 | RUNBOOK holds «Канон всегда на CI» and «не больше часа» |
| 2-9 | «диспатч интегратору или билдеру, требующий большего локально, — дефект координатора.» | 200-201 | → boot, the «Диспетчеру:» line | K1 | present in PROJECT.md |
| 2-10 | «Полный `selftest.py` и `install_smoke.py` на машине владельца не гоняются.» | 201 | home: builder-rules 7 (:14 «Полный `selftest.py` и `install_smoke.py` не запускать: на машине их не гоняет никто») | K4 | builder-rules holds «на машине их не гоняет никто» |
| 2-11 | «Канон гоняет всё, кроме раздела `quarantine` …; карантин гоняет задача `quarantine-watch` по расписанию и после релиза; удаление — по условию спеки … §D.3 и только по слову владельца.» | 201-204 | home: RUNBOOK §7:123-128 + TESTING «Карантин» (:82, :87) | K4 | RUNBOOK holds «кроме раздела `quarantine`»; TESTING holds «`quarantine-watch`» and «только по слову владельца» |
| 2-12 | «Интегратор перед коммитом гоняет только свидетелей узлов и `--limits --lang`; после пуша читает пайплайн, красный пайплайн на `main` (все причины разом — `python -B tools/ci_read.py why`) — находка в `findings/` своей кучки и починка до следующего пуша.» | 204-207 | → RUNBOOK §7, new paragraph «**Интегратор.**» right after «Прогнать ветку» (:92-97); with F17 (a) the 7b integrator sentence joins it | K2 | present in RUNBOOK, absent from PROJECT |
| 2-13 | «Голый пуш ветки ничего не запускает;» | 207 | home: RUNBOOK:90 «пуш ветки без PR ничего не запускает» | K4 | RUNBOOK holds «пуш ветки без PR ничего не запускает» |
| 2-14 | «как прогнать ветку и прочитать результат — `docs/RUNBOOK.md` §7.» | 208 | → boot, as the pointer line «CI, канон пачки, слияние и запасной локальный прогон — `docs/RUNBOOK.md` §7.» | K3 | POINTERS row PROJECT→RUNBOOK §7 |
| 2-15 | «Локальный прогон и локальный докер — только запасной путь (там же), только по слову владельца и никогда не параллельно с другим; когда лог CI не читается — сначала сказать об этом владельцу.» | 208-210 | → RUNBOOK §7 «Что остаётся локально и почему», right after the sentence ending «(слово владельца 03.11.2026: канон — на CI).» (:116); «(там же)» dropped (context word, K2 rule); then R5's clause | K2 + R5 | present in RUNBOOK, absent from PROJECT |

Ready text of п. 2 after S2 (lines 187-192 verbatim, then two lines):
```
2. **Свидетель билдера** — вывод проверки, а не пересказ. Объём проверки билдера и канон пачки — текст
   …(187-192 verbatim)… Форма отчёта — правило 7 `.claude/agents/builder.md`, содержание — builder-rules п. 11.
   CI, канон пачки, слияние и запасной локальный прогон — `docs/RUNBOOK.md` §7.
   Диспетчеру: цикл ожидания в диспатче — один на раунд, с капом, и только на то, что нельзя прочитать иначе
   (вопрос драйвера; пайплайн — только интегратору, «Командная работа» п. 13); диспатч интегратору или билдеру,
   требующий большего локально, — дефект координатора.
```

#### 3.4b «Командная работа» п. 2, 3, 4, 8, 9 at clause level (F2 b'; t-903 B5; Lead B5)

Criterion (§5.1): a clause leaves for `docs/TEAMWORK.md` only when a gate with a door REFUSES its violation (Q21); a discipline
clause with no refusing gate stays in the boot; where the gate is unknown, the safe default is «stays».

| # | Clause | Lines | Gate that refuses (Q21) | Destination | Kind |
|---|---|---|---|---|---|
| 2a | «**Взятая пачка заморожена** (`piles.py check` (в), гейт commit-msg): в её файле меняются только … в строке карточки — только «Статус» и «MR» (ссылка на PR).» | 289-291 | (в) | TEAMWORK § 2 (opener byte-identical); the boot keeps the number + bold title as the pointer line | K2, K3 |
| 2b | «Новое по теме — файлом в `findings/`, никогда строкой в чужую пачку.» | 291 | (в) (a taken batch's text is frozen) | TEAMWORK § 2 (the boot keeps the essence in «Как принимается» п. 4 → § Бэклог и находки) | K2 |
| 2c | «**Находка сразу попадает в пачку** (D-0044): … и находка ложится туда.» | 292-294 | (е) | TEAMWORK § 2 | K2 |
| 2d | «Тем же ходом находка получает строку в таблице «Содержание» … красит `forge-check`.» | 295-296 | (д) + `test_pile_cards_contents.py` | TEAMWORK § 2 | K2 |
| 2e | «Взятие (или решение Lead «пачка полна») замораживает её, … полный аудит — `check --all`.» | 297-298 | (е) | TEAMWORK § 2 | K2 |
| 2f | «**Находка называет класс фабрики, не правило одного проекта** (P2): … не копии текста.» | 299-301 | none (judgment) | → boot | K1 |
| 2g | «Перед «что сделать» — `grep` по `DECISIONS.md` и `docs/DECISIONS_ARCHIVE.md` на тему.» | 301-302 | none | → boot | K1 |
| 3a | «**Зоны файлов пачек «в работе» не пересекаются** (`check` (б)); две пачки с общим горячим файлом (…) — только с строкой `очередь: A → B` в обеих, **или** с непересекающимися списками функций в `owns` обоих диспатчей (`story_run.py (take_answer, fallback_person)` — D-0048):» | 303-306 | (б) | TEAMWORK § 3 (the closing «:» becomes «.», followed by «Что делает поздний узел — `PROJECT.md` «Командная работа» п. 3.») | K2, K3 |
| 3b | «поздний узел сливает `main` в своё дерево и решает конфликт сам (пины обеих сторон зелёные), критик у него один — после слияния; зависимость по замыслу спеки остаётся последовательной.» | 306-308 | none (a coordinator's decision; (б) sees only zones) | → boot, after the connective «При общем файле» | K1 (+K3 connective) |
| 3c | «Пачки одного разработчика друг друга не держат (владелец, 13.11.2026).» | 308 | none refuses — (б) only EXEMPTS one developer (`piles.py:1573`); a permission, kept where every coordinator sees it | → boot | K1 |
| 4a | «**`plans/BACKLOG.md` заморожен** (`check` (г)): новых строк туда нет, закрытое переносит в «Закрыто» только `close`; одна строка по слову владельца — `close --id B-nnn --word "<кто, дата>"`.» | 309-310 | (г), `close --id --word` | TEAMWORK § 4 | K2, K3 |
| 4b | «B-id выдаёт только интегратор на `main` при сборке пачки; у находки до этого `id: —`.» | 310-311 | not established (`piles.py` reports the next free B-id, :994; no refusal found) → safe default | → boot | K1 |
| 8a | «**Двери**: строка `piles-skip: <пункт> -- <причина>` … и `.py`, названный в списке функций активной пачки.» | 325 | every `piles.py` red names this door itself (`DOOR_HELP`, :143) | TEAMWORK § 8 (whole) | K2, K3 |
| 9a | «**Пачка закрывается доделкой, не переносом**: `close <slug> <N>` отказывает, пока в «Остатках» … `release` — отказной псевдоним `close`.» MINUS the fragment 9c | 326-330 | `close`, (д) | TEAMWORK § 9 | K2, K3 |
| 9b | «То же — для таблицы «Живые доказательства» (FR-33): `close` отказывает, … таблица из одной шапки = доказательств не должно.» | 330-333 | `close` | TEAMWORK § 9 | K2 |
| 9c | «перенос подтверждает **человек**, не агент сам;» | 328 | none (`close` checks the form of `подтвердил:`, not that a human wrote it; calibration check 39) | → boot, in the pointer line | K1 |
| 9d | «**Остатков в идеале нет вовсе**: минорные замечания критика … переносятся в соответствующие кучки строкой с исполнителем.» | 333-336 | none (`close` cannot refuse the choice to carry instead of fix) | → boot | K1 |
| 9e | «Закрытые по тексту строки помечает Lead, не владелец.» | 336 | none | → boot | K1 |
| 9f | «**Живые прогоны не держат пачку вообще** (владелец, 11.11.2026): … снята прогоном.» | 337-341 | none | → boot | K1 |
| ck | «Проверка на пути исполнения: `tools/piles.py check --msg-file` в `.githooks/commit-msg` и CI `forge-check` (`check --base`); детектор — калибровочная проверка 33.» | 368-369 | — | TEAMWORK (last line) | K2, K3 |

п. 9 rows are «text owned by t-907, moved here verbatim, re-synced after t-907 lands» (E20).

Ready text of the boot side after S2:
```
2. **Взятая пачка заморожена** — правило: `docs/TEAMWORK.md` § 2 (что меняется во взятой пачке, находка в пачку, строка
   «Содержание»). **Находка называет класс фабрики, не правило одного проекта** (P2): …(299-302 verbatim)… на тему.
3. **Зоны файлов пачек «в работе» не пересекаются** — правило: `docs/TEAMWORK.md` § 3. При общем файле поздний узел сливает
   `main` в своё дерево и …(306-308 verbatim)… Пачки одного разработчика друг друга не держат (владелец, 13.11.2026).
4. **`plans/BACKLOG.md` заморожен** — правило: `docs/TEAMWORK.md` § 4. B-id выдаёт только интегратор на `main` при сборке
   пачки; у находки до этого `id: —`.
…
8. **Двери** — правило: `docs/TEAMWORK.md` § 8.
9. **Пачка закрывается доделкой, не переносом** — правило: `docs/TEAMWORK.md` § 9 (отказы `close` и `check` (д), «Живые
   доказательства»); перенос подтверждает **человек**, не агент сам. **Остатков в идеале нет вовсе**: …(333-341 verbatim)…
…
Проверка на пути исполнения и детектор — `docs/TEAMWORK.md`.
```
`docs/TEAMWORK.md` (new): title «# Командная работа: механика, которую держит код»; intro «Дисциплина и смысл — `PROJECT.md`
«Командная работа» (его читает каждая сессия); здесь — то, что отказывает `tools/piles.py check`/`close` и называет дверь. Номера
пунктов — те же, что в PROJECT.md.»; then items 2, 3, 4, 8, 9 as numbered list items whose openers are byte-identical to the
PROJECT openers (2a, 3a, 4a, 8a, 9a), followed by 2b-2e, 9b; then the check line.

#### 3.4c «Командная работа» п. 12 (353-360; t-903 B1; Lead B1)

| # | Clause | Destination | Kind |
|---|---|---|---|
| 12-1 | «в работе всегда шесть пишущих билдеров;» | replaced by R1 (a) | K5 |
| 12-2 | «дизайнеры, критики и скауты в счёт не идут и слота не ждут.» | stays verbatim | K1 |
| 12-3 | «Не хватает параллельных узлов — берутся другие узлы П1 любых кучек; меньше шести — только по слову владельца «экономим время / токены».» | replaced by R1 (a) («цель сессии + П1 из бэклога»; «если не сказано в этой сессии иного») | K5 |
| 12-4 | «Шесть — цель, а не потолок экономии: ограничение владельца … новая сессия снова держит шесть; лимиты откатываются в понедельник вечером (владелец, 16.11.2026).» | stays verbatim | K1 |
| 12-5 | «Критик кода — один на тему, не на узел.» | stays verbatim (T8: a pointer would cost as many bytes) | K1 |
| 12-6 | «Волны слияния CI не ждут: принятое сливается в `main` через `tools/wave.py merge`, красный CI чинит там один билдер.» | stays verbatim | K1 |
| 12-7 | «Шесть — не потолок: седьмого координатор берёт, когда надо (упал мерж),» | replaced by R1 (b) | K5 |
| 12-8 | «дверью `budget-skip:`.» | stays verbatim, attached to R1 (b) | K1 |
| 12-9 | «Тем же ходом, что слияние: статусы узлов в пачках обновлены, слитые ветки и папки деревьев убраны.» | stays verbatim | K1 |

R1 words (the owner, 16.11.2026; «билдеров» added after «пишущих» so the noun is explicit — the critic compares): (a) «цель держать 6
пишущих билдеров (если не сказано в этой сессии иного) и не меньше, если есть параллельная работа (цель сессии + П1 из бэклога)»;
(b) «Можно запустить 7, если координатору надо, например упал CI и его надо починить»; (c) «6 — это цель, но не ценой ущерба
эффективности (например, решать мерж-конфликты будет дороже, так что запустить в параллельность сейчас нечего)».

Ready text after S2:
```
12. **Темп координатора** (владелец, 13.11 и 16.11.2026): цель держать 6 пишущих билдеров (если не сказано в этой сессии
   иного) и не меньше, если есть параллельная работа (цель сессии + П1 из бэклога); дизайнеры, критики и скауты в счёт не
   идут и слота не ждут. Можно запустить 7, если координатору надо, например упал CI и его надо починить, — дверью
   `budget-skip:`. 6 — это цель, но не ценой ущерба эффективности (например, решать мерж-конфликты будет дороже, так что
   запустить в параллельность сейчас нечего). Шесть — цель, а не потолок экономии: …(12-4 verbatim)… (владелец, 16.11.2026).
   Критик кода — один на тему, не на узел. Волны слияния CI не ждут: …(12-6 verbatim)… Тем же ходом, что слияние: …(12-9).
```

#### 3.4d «Командная работа» п. 13 (361-366; t-903 B2; Lead B2)

| # | Clause | Destination | Kind | K-check |
|---|---|---|---|---|
| 13-a | «билдер гоняет только узкие быстрые свидетели своих путей» | home: builder-rules 7b «**точечные проверки своей правки**» | K4 | 7b holds it |
| 13-b | «и **CI не запускает и не ждёт** — ни пайплайн ветки, ни канон;» | → builder-rules 7b, new sentence after ««сверх списка» — строка отчёта, не прогон.»: «Билдер **CI не запускает и не ждёт** — ни пайплайн ветки, ни канон (слово владельца 14.11.2026).» | K2 | present in 7b, absent from PROJECT; `.claude/agents/builder.md:52`'s pointer to 7b then resolves (no loop) |
| 13-c | «медленные файлы называет в отчёте строкой «судит канон пачки».» | home: builder-rules 7b («билдер НЕ гоняет и не ждёт: «судит канон пачки»») | K4 | 7b holds «судит канон пачки» |
| 13-d | «Канон запускает и читает координатор после слияния;» | home: CLAUDE.md rule 4 (BATCH CANON «the coordinator's duty», output appended to the witness) + builder-rules 7b «его запускает координатор» (after R3) | K4 | CLAUDE.md holds «the coordinator's duty»; 7b holds «его запускает координатор» |
| 13-e | «пайплайн `main` читают только интегратор волны и билдер, чинящий красный `main`.» | → builder-rules 7b, new sentence after «… его запускает координатор.»: «Пайплайн `main` читают только интегратор волны и билдер, чинящий красный `main` (слово владельца 14.11.2026).» | K2 | present in 7b, absent from PROJECT |
| 13-f | «**Мутации** билдер не прогоняет и не перечисляет — их судит канон (владелец, 28.10 и 10.11.2026).» | home: builder-rules 7b:39-41 | K4 | 7b holds «мутации судит канон пачки» |
| 13-g | «Диспатч, который просит билдера запустить CI, ждать пайплайн или гонять мутации, — дефект координатора.» | → boot (DISPATCHER duty, T33) | K1 | present in PROJECT.md |
| 13-h | «Полный текст — `plans/builder-rules.md` п. 7b.» | → boot, as the pointer | K3 | POINTERS row PROJECT→7b (existing) |

Ready text after S2:
```
13. **Проверки билдера** (владелец, 14.11.2026) — правило: `plans/builder-rules.md` п. 7b. Диспатч, который просит
   билдера запустить CI, ждать пайплайн или гонять мутации, — дефект координатора.
```

---

## 4. The table of contents

### 4.1 Form (F4 = a)
CLAUDE.md, right after the title paragraph (after line 6), the one CROSS-FILE topic map:
```
## Contents — topic → where to read

| Topic | Where |
|---|---|
| Tiers | CLAUDE.md § Tiers |
| Recon → scout | CLAUDE.md § 1 |
| What a builder may run | plans/builder-rules.md § 7b |
| ...one row per T1–T33 of the topic map... |
```
Cell grammar (§4.3): `<file> § <heading text>` or `<file> § <number>` for a numbered item; several homes joined by ` + `. A row
carries the TOPIC NAME only — never a rule sentence (E10). Under F19 (a) a numbered rule is cited by number (`CLAUDE.md § 3`).

PROJECT.md, after its intro (line 16): `## Оглавление` — its OWN sections only, `| Раздел | О чём (≤ 8 слов) |`; the row «Все
темы → `CLAUDE.md` § Contents» is added by S1 (E21).

### 4.2 Byte cost (est.)
CLAUDE.md TOC: 33 rows × ~75 B + header ≈ 2.6 KB (F19 lever: ≤ 2.0 KB). PROJECT.md TOC: ~14 rows × ~100 B ≈ 1.4 KB. Headings:
F19 (b) as drafted ~28 in CLAUDE.md × ~50 B ≈ 1.4 KB; F19 (a) ~10 sub-headings ≈ 0.5 KB; ~8 in PROJECT.md ≈ 0.4 KB.

### 4.3 How it stays true — the contract for FG7-52 (a NOTE, not this node's DoD; owner: data, code)
1. Every cell of both TOCs, and every pointer line `rule: <file> § <x>` / `правило: <файл> § <x>`: `<file>` exists; `<x>` equals the
   text of a heading of `<file>` (after the `#` marks, whitespace squashed), or `<x>` is a number/id and a line of `<file>` starts
   with `<x>.` (or `### <x>` / `**<x>.**` / `- **<x>.**`).
2. A numbered pointer line («N. **<title>** — правило: …») — its `<title>` equals the bold opener of item N in the target.
3. A refusal names carrier file:line, the pointer, and the nearest existing heading in the target (FR-1, FR-2).
4. Error direction: an unresolvable pointer is RED, never skipped (FR-59). Adversarial inputs that must stay red: a heading renamed
   by one character; a heading only inside a code fence; a target file renamed; a `§` cell pointing to a heading of ANOTHER file
   of the same name; a numbered item deleted while its number is cited.
5. Until FG7-52 (F16 = a): every TOC cell and every pointer line this node writes is a POINTERS row of
   `tools/tests/test_role_carriers_one_owner.py` — the existing checker, a table row, no new file. TOC COMPLETENESS (a later topic
   added without a TOC row) has no code detector until FG7-52: calibration check 33 line (§6, m8).

---

## 5. What leaves the boot, and the budget

### 5.1 The criterion (decided: the owner's «да» 17.11.2026 — «what code holds may leave»; applied at CLAUSE level, t-903 B5)
A CLAUSE leaves the boot when EITHER (i) a gate on the execution path refuses its violation and the refusal names the door
(`piles.py check`, `close`), OR (ii) it is read only by one role or at one moment that already loads its carrier (package work
loads `factory-rules.md` whole and builder-rules; a release session runs RUNBOOK §4). A discipline clause with no refusing gate
stays, even inside an item whose other clauses leave; a gate that only exempts (permits) does not count as a refusal; an unknown
gate → stays (safe default). A DISPATCHER duty always stays (T33). Rationale: boot-diet step 6 «policy that isn't auto-loaded gets
silently skipped» (Q15).

### 5.2 Moves and the resulting budget (removals **measured** by t-903 §5 where marked; additions est.)

| Move | Δ boot |
|---|---|
| P1–P31 → `docs/OWNER_PRINCIPLES.md` (**−22318 measured**); capped index imported (≤ 6144 B by S4's cap; uncapped first sentences measured 6485 B; est. with the 220 B line cap ≈ 4.6 KB — upper bound used); pointer line +0.4 | −22.3 + 6.1 + 0.4 = **−15.8 KB** |
| F2 b': gated clauses of п. 2/3/4/8/9 + check line → TEAMWORK (**7236 measured** for the whole items); discipline clauses stay (2f, 2g, 3b, 3c, 4b, 9c-9f ≈ 2.15 KB est.); 6 pointer lines ≈ 0.6 KB est. | −7.2 + 2.15 + 0.6 ≈ **−4.5 KB** |
| п. 13 (**1058 measured**) → pointer + dispatcher sentence (≈ 0.35 KB est.) | **−0.7 KB** |
| «Как принимается» п. 2 (**3820 measured**) → 187-192 kept (≈ 0.9 KB est.) + pointer + «Диспетчеру:» line (≈ 0.5 KB est.) | **−2.4 KB** |
| «Релиз» (**1807 measured**) → RUNBOOK § 4.1; pointer +0.1 | **−1.7 KB** |
| п. 12 R1 (new words vs replaced cap sentences, est.) | +0.2 KB |
| PR5-PR7 move within PROJECT (§ Сессия форджа), C12b edits | ≈ 0 |
| TOCs + headings (§4.2, F19 b as drafted) | +5.8 KB est. |
| §6 writing rule in the boot (F12 a; **1673 measured** + m9 sentence ≈ 0.2) | +1.9 KB |
| architect-tier spec Stream L (architect line in «Tiers», rewrites, a new D entry in DECISIONS.md) | +1.0 KB est. (NOT measured; Phase 0 re-measures) |

| Scenario | Arithmetic (from **123942 measured**) | Result | vs 120000 / 108000 |
|---|---|---|---|
| **Decisions in force** (F2 b', F3 a, F5 c, F7 a, F12 a; R1, B2, B3 kept in the boot) | 123.9 − 15.8 − 4.5 − 0.7 − 2.4 − 1.7 + 0.2 + 5.8 + 1.9 + 1.0 | **≈ 107.7 KB est.** | under BREACH; at the WARN line — headroom ≈ 0.3 KB est. → **F19** |
| same + F19 (a) (headings only where needed, CLAUDE TOC ≤ 2.0 KB) | 107.7 − 0.9 − 0.6 | ≈ 106.2 KB est. | under both, thin |
| same + F19 (a) + §6 into boot-diet (F12 c) | 106.2 − 1.9 | ≈ 104.3 KB est. | under both, ≈ 3.7 KB headroom |
| headings/TOC/§6 before any move (forbidden, B4) | 123.9 + 7.7 | ≈ 131.6 KB est. | over BREACH |
| both owner forks refused (F2 a, F3 c) — hypothetical since the owner's «да» (t-903 §5) | 107.7 + 15.8 + 4.5 | ≈ 128.0 KB est. | over BREACH — fallback below |

Check of the arithmetic of the first scenario: −15.8 − 4.5 − 0.7 − 2.4 − 1.7 = −25.1; +0.2 + 5.8 + 1.9 + 1.0 = +8.9;
123.9 − 25.1 + 8.9 = **107.7 KB est.** (the review's ≈ 105.2 K assumed F5's −2.0 K inside; F5 is dropped, and this fix round keeps
more text in the boot by B1-B3/B5 and counts the architect additions).

**Fallback if both F2 and F3 were refused** (recorded because the review asks for the row; not expected after the owner's «да»):
land only what removes bytes without a TOC — S3, S4 (inert), PA2, п. 13 and «Релиз» moves (−4.8 KB) — and §6 in boot-diet (F12 c);
defer the TOCs and headings until a move pays for them: 123.9 − 4.8 ≈ 119.1 KB est. — under BREACH, over WARN; the Lead then takes
the remaining gap to the owner as a new question.

Per file after the decisions in force (est.): CLAUDE.md ≈ 43.5 + TOC 2.6 + headings 1.4 + architect 1.0 + pointers 0.1 ≈ **48.6 KB —
over CLAUDE_WARN 47800** (F5's −2.0 K is gone) → F19; with F19 (a) ≈ 47.1 KB est. PROJECT.md ≈ 62.3 − 22.3 − 4.5 − 0.7 − 2.4 − 1.7 +
0.4 + 0.2 + 1.4 (TOC) + 0.4 (headings) + 1.9 (§6) ≈ 35.0 KB; `docs/OWNER_PRINCIPLES_INDEX.md` ≤ 6.1 KB; FR 5.6, AR 2.7, DECISIONS
7.5 (+ architect D entry), CURRENT_CONTEXT 1.8, SYSTEM_PROMPT 0.6. The measured figure replaces these in each stream's witness.

### 5.3 What each kind of session reads afterwards
- Every session, workers included (Q6): CLAUDE.md + imports (PROJECT.md, FR index, AR index, P index). The coordinator also gets
  Layer A (SYSTEM_PROMPT.md, DECISIONS.md) and reads CURRENT_CONTEXT.md (BOOT.md:14-27).
- Coordinator, on the topic: `docs/TEAMWORK.md` (take, freeze, zones, close forms — and whenever a `piles.py` refusal names an
  item), `docs/RUNBOOK.md` §7 (CI, merge, canon, the integrator's local run, the fallback), § 4.1 (release), `docs/OWNER_PRINCIPLES.md`
  (steering package work; a P cited in a verdict).
- builder: + `builder.md`, the dispatch, `plans/builder-rules.md`; `docs/TESTING.md` before the first test; package work:
  `design/factory-rules.md` whole.
- critic: + `critic.md`, `docs/tasks/critic-diff-brief.md`, the spec/DoD under review.
- designer: + `designer.md`, `docs/TESTING.md`, builder-rules 7b; package: `design/architecture.md`.
- scout: + `scout.md`, `docs/tasks/exchange-form.md`.

---

## 6. Writing form for agent-read rule text (a standing rule; home: PROJECT § Как пишутся правила для агентов, F12 a)

Draft text (Russian, ≈ 1.9 KB):

1. Одна тема — один дом (файл и раздел). В любом другом месте — строка-указатель `правило: <файл> § <раздел>` и, если роли
   нужно, одна фраза о том, что делает ЭТА роль, когда правило срабатывает. Обязанность диспетчера живёт в буте, не в файле
   исполнителя. Пересказ правила вне дома — дефект.
2. Один заголовок — одна тема; раздел не длиннее ~40 строк (одна таблица дефектом не считается); правило, спрятанное в чужой теме,
   получает свой заголовок. Подзаголовок ставится только на границе абзаца, никогда между условием и следствием; подзаголовок
   внутри нумерованного правила повторяет номер правила («Rule 2 · …»).
3. Одно правило — один пункт списка или строка таблицы: что делать, кто сказал (слово владельца с датой или D-nnnn).
4. История, пример, разбор, замер — не в бут: в спеку, находку, пачку или `docs/*_FULL.md`; в правиле — ссылка.
5. Номера правил не переиспользуются и не сдвигаются: переехавший пункт оставляет на своём номере строку-указатель с тем же
   жирным заголовком.
6. Импорт `@` — только из `CLAUDE.md`, один уровень (счётчик бюджета вложенных не видит).
7. Как сокращать бут — `.claude/skills/boot-diet/SKILL.md`; указатели и оглавление проверяет код (строки POINTERS, затем FG7-52);
   до FG7-52 пересказ, раздел длиннее 50 строк и заголовок бута без строки оглавления ищет калибровочная проверка 33.

**Four questions for this rule (rule 10; m8)** — carried in S2's commit message, because PROJECT.md is outside the mechanism-gate
net (Q13) and no axis block is forced:
- (a) cost: the editor of a rule file looks up the home in the TOC and writes a pointer instead of a copy; the Lead pays one line of
  check 33 per calibration.
- (b) axes: the commit message carries one line «axis N: covered / queued / n/a <why>» for EVERY axis of the current
  `docs/SIBLING_MAP.md` (written by the Lead at commit; axis 31 «role-text carriers» covered by the new rows; axis 34 «one road»
  covered by the one-home rule).
- (c) detector: calibration check 33 gets one line (Lead-placed in `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md` in S2's commit): «Boot
  form (boot-by-topic, FG7-51): sample CLAUDE.md and PROJECT.md for a rule sentence restated outside its home (topic map), a section
  over 50 lines without a table, a heading of the boot that no TOC row routes to — each a finding; on discipline until FG7-52.»
- (d) on the path: pointer resolution — POINTERS rows of `tools/tests/test_role_carriers_one_owner.py` (CI); retelling and length —
  on discipline, the (c) detector named explicitly.

---

## 7. Phases, streams, readers

### 7.1 Order and executability (rewritten, t-903 B4; Lead B4)
- **Phase 0 (Lead, before each stream):** no open branch owns a file the stream owns (`git -C C:/QAFactory/forge-repo worktree list`
  + each worktree's `git -C <wt> diff --stat origin/main`; `python -B C:/QAFactory/forge-repo/tools/piles.py check --all`); for S2/S1
  also: the architect spec's Stream L merged; re-measure the BOOT BUDGET line then (the architect additions replace the est. +1.0).
- **S3 and S4 can start now** (the owner's word is in; FG7-50 has landed, Q19). S3 adds no boot bytes; S4 is inert under its
  TEMPORAL edge (no source → skip). S3 and S4 have disjoint owns.
- **S2 starts after** S3 and S4 are merged AND the architect spec's Stream L has landed (S2 edits CLAUDE.md lines in the same file
  Stream L rewrites, and DECISIONS.md bytes change the budget); for п. 9 also after t-907's п. 9 edit (E20).
- **S1 starts after** S2 is merged (its TOC cells name the final headings of every file, incl. PROJECT's) — and therefore after
  Stream L.
- **Headings and the contents land TOGETHER with the moves, never before them**: the PROJECT TOC and headings land in S2's commit,
  the CLAUDE TOC and headings in S1's; landing headings/TOC first would raise the boot to ≈ 131.6 KB est. (§5.2).
- Queue line for the batch file: `очередь: S3, S4 → S2 → S1`; external: `архитектор/L → S2`, `t-907 (п. 9) → S2`.

### 7.2 Streams (header lines for each builder dispatch; `designer:` = this file once accepted)

Witness scope (CLAUDE.md rule 4): every owned path is outside the package → `scenario_walk.py --witness-for` has no row; the witness
is the test file that judges each path, named per stream, plus the DOC-DISPATCH run (§7.4) for markdown owns. No CI wait, no
mutations, no full `pytest tools/` (builder-rules 7b). New test cases are ROWS of existing tables; no new test file.

**S3 — role and worker docs (now)**
- owns: `C:/QAFactory/forge-repo/.claude/agents/designer.md`, `C:/QAFactory/forge-repo/plans/builder-rules.md` (S3 rows only),
  `C:/QAFactory/forge-repo/docs/TESTING.md`, `C:/QAFactory/forge-repo/docs/tasks/critic-diff-brief.md`
- rows:

| # | File, source → destination | Kind | K-check |
|---|---|---|---|
| S3-1 | designer.md rule 3, the paragraph from «READERS OF EVERY TOUCHED FILE (the owner's word 16.11.2026):» to «…two count pins).» (:45-…) → a NEW rule «7. » appended after rule 6, the paragraph verbatim after «7. »; rule 3 keeps «Readers of every touched file: rule 7.» | K2, K3 | squashed paragraph present in rule 7, absent from rule 3; openers of rules 1-6 byte-identical (`install_parity.py --check` MISSING (0)); OWNER_KEYS `hand-back:designer` green |
| S3-2 | builder-rules: one `### <n>. <bold title>` line above each numbered opener (1-20, 7a-7d); openers byte-identical | K1 | `git diff -U0` shows no removed opener line; `RULES_7B` anchor green |
| S3-3 | builder-rules 2 (:9) «Мерджи, пуши, переключение веток — только интегратор.» → «Мерджи, пуши, переключение веток — не билдер: принятое сливает координатор (`tools/wave.py merge`), пачку закрывает интегратор (`piles.py close`).» | K5 (R3) | new sentence present; old absent |
| S3-4 | builder-rules 7b (:41-42) «интегратор делает один прогон BATCH CANON» → «координатор запускает один прогон BATCH CANON» | K5 (R3) | as S3-3 |
| S3-5 | builder-rules 7d (F14 a): a sentence of 7d leaves (K4, replaced by «полный текст — `docs/TESTING.md`» already in 7d's opener) ONLY when its squashed key phrase is present in `docs/TESTING.md`; otherwise it stays. The `scope:tests` key «Покрасневший пин удаляется, а не чинится» ALWAYS stays (OWNER_KEYS, Q10) | K4 | per removed sentence: key present in TESTING.md (the run prints the key and the TESTING line); OWNER_KEYS `scope:tests` green |
| S3-6 | TESTING.md:80-81 «- **Что запускать по своей правке** — `python -B …scenario_walk.py --witness-for <пути owns>`: печатает истории и строки `keep`, которые покрывают тронутые пути.» → «- **Что запускать по своей правке** — правило: `plans/builder-rules.md` п. 7b.» | K4 | 7b holds «--witness-for» and «строки `keep`» |
| S3-7 | TESTING.md:176-177 «свидетель — то, что печатает `scenario_walk.py --witness-for <пути owns>`; файл карантина не запускает и не правит; мутации не перечисляет (слово владельца 28.10.2026: мутации судит канон).» → «что запускает — `plans/builder-rules.md` п. 7b.» (the line keeps «- **Билдер**: пишет по этому документу;») | K4 | 7b holds «Файл карантина билдер не запускает» and «мутации судит канон пачки» |
| S3-8 | critic-diff-brief:10-13, the parenthetical «(D-0056, 21.10.2026: the files `scenario_walk.py --witness-for <owns>` prints — … — no neighbours, no big files, no docker)» → «(the scope: `plans/builder-rules.md` 7b)»; the rest of the bullet (ratchets, old-vs-new counts) stays — the critic's consequence | K4 | 7b holds «Не регрессия, не соседи, не большие файлы»; BRIEF anchor «## The two layers» green |

- non-goals: CLAUDE.md, PROJECT.md, RUNBOOK, builder.md, critic.md, scout.md; builder-rules 7, 7b's sentences listed for S2 (§7.2 S2
  rows B-1…B-7), 7c; any test file (POINTERS rows TESTING→7b and BRIEF→7b go to «Needed from integration» for S2).
- edges: S3-5 adversarial: a 7d sentence present in TESTING only as a paraphrase → the key is absent → it STAYS (the safe side:
  a duplicate, never a loss); a key present only inside a TESTING code fence → counts as absent (stays).
- DoD: `python -m pytest tools/tests/test_role_carriers_one_owner.py tools/test_handoff_rule_anchors.py -q`;
  `python -B C:/QAFactory/forge-repo/tools/install_parity.py --check`; `python -B C:/QAFactory/forge-repo/tools/agents_md.py --check`;
  the DOC-DISPATCH run §7.4 over S3-1, S3-3…S3-8.
- Lead places: `.claude/agents/designer.md` (mechanism path) with the axis block and `tier:` line.

**S4 — the principles index row (now)**
- owns: `C:/QAFactory/forge-repo/tools/factory_rules_index.py`, `C:/QAFactory/forge-repo/tools/test_factory_rules_index.py`
  (`.githooks/pre-commit` and `forge-check.yml` DROPPED — m5: pre-commit:54 already runs `factory_rules_index.py --check`, which
  checks every row of the tool's table)
- does: a data table of sources inside the tool, generic enough to take the AR index later (fields: source path, out path, opener
  regex, header text, per-line byte cap, per-file byte cap). Row FR: today's behaviour, output byte-identical. Row P: source
  `docs/OWNER_PRINCIPLES.md`, out `docs/OWNER_PRINCIPLES_INDEX.md`, opener `^- \*\*P(\d+)\.\*\* `, line `- P<n> — <first sentence>`,
  per-line cap 220 B (UTF-8), per-file cap 6144 B, header in the FR index's style («Generated by `python tools/factory_rules_index.py`
  from `docs/OWNER_PRINCIPLES.md` — do not edit by hand. …»).
- First sentence: text after the bold opener up to the first `.`, `!` or `?` followed by whitespace, outside backticks; longer than
  the line cap → cut at the last whitespace before the cap and append « …»; never cut inside a UTF-8 character.
- edges: (TEMPORAL) source absent and out absent → `--check` prints `skip: docs/OWNER_PRINCIPLES.md absent` and exits 0; out present
  and source absent → exit 2 naming both (S2's commit creates both). Over the per-file cap → exit 2 naming the three longest lines
  and the door («shorten the first sentence in the source, or raise the cap in the data row with a reason»). Duplicate P id → exit 2
  naming both lines. A bullet with no sentence end → the whole bullet, capped. An empty bullet text → exit 2 naming the line. CRLF
  source → output identical to LF. A gap in the numbering → allowed (P numbers are never reused; a retired one may vanish).
- one road (m5, honest): `tools/architecture_index.py` stays a SECOND generator after this stream (own cap 3072 B, own pre-commit:58
  and CI lines). The fold is queued as node FG7-55 (§7.6 ready row) with owns and a test (designer rule 6: a residual is a node).
- DoD: `python -m pytest tools/test_factory_rules_index.py -q` (new cases = rows of its table: FR byte-identical; P row on a fixture
  source — cap cut, long first sentence like P19, duplicate id, empty bullet, CRLF, both TEMPORAL worlds); `python -B
  C:/QAFactory/forge-repo/tools/factory_rules_index.py --check` (exit 0, prints the P skip line before S2).
- Lead places: `tools/factory_rules_index.py` (mechanism path).

**S2 — the PROJECT side (after S3, S4, architect Stream L; п. 9 after t-907)**
- owns: `C:/QAFactory/forge-repo/PROJECT.md`, `C:/QAFactory/forge-repo/docs/OWNER_PRINCIPLES.md` (new),
  `C:/QAFactory/forge-repo/docs/OWNER_PRINCIPLES_INDEX.md` (new, generated), `C:/QAFactory/forge-repo/docs/TEAMWORK.md` (new),
  `C:/QAFactory/forge-repo/docs/RUNBOOK.md`, `C:/QAFactory/forge-repo/plans/builder-rules.md` (S2 rows B-1…B-7 only),
  `C:/QAFactory/forge-repo/tools/tests/test_role_carriers_one_owner.py`, `C:/QAFactory/forge-repo/tools/test_session_context.py`
  (the one pin row at :1188), `C:/QAFactory/forge-repo/CLAUDE.md` (THREE edits: the import line, C12b (1), C12b (2)),
  `C:/QAFactory/forge-repo/AGENTS.md` (regenerated)
- rows: every §3.2 row marked S2; §3.4a, §3.4b, §3.4c, §3.4d; R1, R2, R3 (RUNBOOK:108), R5; plus:

| # | File, source → destination | Kind | K-check |
|---|---|---|---|
| B-1 | builder-rules 7 (:14) «(D-0059, `PROJECT.md` «Как принимается изменение пакета» п. 2)» → «(D-0059, `docs/RUNBOOK.md` §7)» (m6: the clause's home becomes item 7 itself) | K3 | new citation present |
| B-2 | builder-rules 7b (:37-38) «(критерий — список, а не длительность; узкий быстрый свидетель — до минуты каждый, `PROJECT.md` «Как принимается изменение пакета» п. 2)» → «(критерий — список, а не длительность)» | K5 (R2) | «до минуты» absent from builder-rules and PROJECT |
| B-3 | builder-rules 7b, after ««сверх списка» — строка отчёта, не прогон.» insert 13-b (§3.4d) | K2 | present in 7b, absent from PROJECT |
| B-4 | builder-rules 7b (:40-41) «(слово владельца 28.10 и 10.11.2026, `PROJECT.md` «Командная работа» п. 13)» → «(слово владельца 28.10 и 10.11.2026)» (m6 loop) | K3 | PROJECT п. 13 citation absent from 7b |
| B-5 | builder-rules 7b (:51) «(слово владельца 03.11.2026, PROJECT.md п. 2)» → «(слово владельца 03.11.2026)»; F17 (a): «интегратор локально гоняет только узкие свидетели узлов с конфликтом слияния и `--limits --lang`, затем push;» → K2 to RUNBOOK §7 «**Интегратор.**» paragraph (with 2-12), leaving «что интегратор гоняет локально — `docs/RUNBOOK.md` §7;» | K3, K2 | sentence present in RUNBOOK, absent from 7b |
| B-6 | builder-rules 7b, after «… его запускает координатор.» insert 13-e (§3.4d) | K2 | present in 7b, absent from PROJECT |
| B-7 | builder-rules 7c (:57) «точечные файлы (меньше минуты каждый), НЕ из списка» → «точечные файлы, НЕ из списка» | K5 (R2) | «меньше минуты» absent |
| RB-1 | RUNBOOK §7 :108 «После схождения веток интегратор прогоняет ветку, как выше.» → «После схождения веток координатор прогоняет ветку, как выше.» | K5 (R3) | new present |
| RB-2 | RUNBOOK §7 :115 «(`PROJECT.md`, «Командная работа» п. 13)» → «(`plans/builder-rules.md` п. 7b)» | K3 | POINTERS row RUNBOOK→7b (existing) green |
| RB-3 | RUNBOOK :232 «— `PROJECT.md`, «Прогоны и эксперименты».» → «— `PROJECT.md` § Сессия форджа.» (m6) | K3 | POINTERS row RUNBOOK→PROJECT § Сессия форджа |
| RB-4 | RUNBOOK new «### 4.1. Шаги релиза» at the end of §4 (before «## 5. Коммиты в целевом проекте», :52) ← PROJECT 373-379 verbatim | K2 | squashed keys present / absent |
| PI-1 | `docs/OWNER_PRINCIPLES.md`: title «# Принципы владельца», one intro line «Индекс (первая фраза каждого) — `docs/OWNER_PRINCIPLES_INDEX.md`, импорт из `CLAUDE.md`; номера P1–P31 не переиспользуются.», then PROJECT 41-174 verbatim with range sub-headings (§10); then `python -B tools/factory_rules_index.py` writes the index | K2 | per P: squashed first/last keys present in OWNER_PRINCIPLES, absent from PROJECT; `factory_rules_index.py --check` exit 0 |
| CL-1 | CLAUDE.md: `@docs/OWNER_PRINCIPLES_INDEX.md` after `@docs/ARCHITECTURE_INDEX.md`; `tools/test_session_context.py:1188` pin gets the fourth item | K1 | `-k imports` green |

- test rows (S2): OWNER_KEYS `cost:queue` → «цель держать 6 пишущих билдеров»; POINTERS rows: PROJECT→TEAMWORK § 2, 3, 4, 8, 9 (anchor =
  the byte-identical opener in TEAMWORK); PROJECT→`docs/OWNER_PRINCIPLES.md` (anchor «- **P31.**»); PROJECT→RUNBOOK § 4.1 (anchor
  «### 4.1. Шаги релиза»); PROJECT→RUNBOOK §7 (anchor «## 7. CI на GitHub и BATCH CANON»); PROJECT «правило: § Бэклог и находки»
  (anchor «## Бэклог и находки»); RUNBOOK→PROJECT § Сессия форджа (anchor «## Сессия форджа»); builder-rules→RUNBOOK §7; S3's
  TESTING→7b and BRIEF→7b rows.
- edges: E2, E3, E7, E8, E9, E19, E20, E21; the P index import, the P move, the pin row and the generated index land in ONE commit
  (no window without P in the boot); every PROJECT↔builder-rules↔RUNBOOK exchange lands in ONE commit (E7: no rule in two carriers
  or none — the reason B2's 7b additions are S2's, not S3's); R2 in one commit.
- DoD: `python -m pytest tools/tests/test_role_carriers_one_owner.py tools/test_agents_md.py -q`;
  `python -m pytest tools/test_session_context.py -q -k imports`; `python -B C:/QAFactory/forge-repo/tools/agents_md.py --check`;
  `python -B C:/QAFactory/forge-repo/tools/factory_rules_index.py --check`; `python -B C:/QAFactory/forge-repo/tools/install_parity.py
  --check` (C12b (1) touches a CLAUDE.md line: if an anchor quotes it, the anchor is updated in the same commit — owned via the Lead,
  `tools/install_parity_anchors.json` is a Lead-placed line here); the BOOT BUDGET line of `python -B
  C:/QAFactory/forge-repo/tools/session_context.py`; the DOC-DISPATCH run §7.4 over every K2/K4 row of S2.
- Lead places: the three CLAUDE.md edits (mechanism path); `docs/SIBLING_MAP.md` axis 31 rows for `docs/OWNER_PRINCIPLES.md`,
  `docs/TEAMWORK.md` (Q16) and the `:308` edit «PROJECT.md «Командная работа» item 3» → «`docs/TEAMWORK.md` § 3» (the `очередь:`
  and function-list grammar is clause 3a, which moves); the check-33 line (§6 (c)); the four-question block in the commit message.

**S1 — the CLAUDE side (after S2)**
- owns: `C:/QAFactory/forge-repo/CLAUDE.md`, `C:/QAFactory/forge-repo/PROJECT.md` (ONE line: the TOC row «Все темы → `CLAUDE.md` §
  Contents», E21), `C:/QAFactory/forge-repo/tools/install_parity_anchors.json` (only if an anchored line changes — K1 headings do
  not change anchored lines), `C:/QAFactory/forge-repo/tools/tests/test_role_carriers_one_owner.py` (POINTERS rows),
  `C:/QAFactory/forge-repo/AGENTS.md` (regenerated)
- does: §3.1 rows marked S1 (headings per F19, C-H3 pointer line); the cross-file TOC (§4.1); one POINTERS row per TOC cell of both
  TOCs. No text moves out of CLAUDE.md (F5 → c), so no parity unit is created (m4).
- edges: E1, E10, E14, E17; a TOC cell naming a heading that Stream L renamed → use the name on disk (E17).
- DoD: `python -m pytest tools/tests/test_role_carriers_one_owner.py tools/test_agents_md.py -q`;
  `python -B C:/QAFactory/forge-repo/tools/install_parity.py --check`; `python -B C:/QAFactory/forge-repo/tools/agents_md.py --check`;
  the BOOT BUDGET line (total ≤ 108000; CLAUDE.md ≤ 47800 or the F19 outcome); the DOC-DISPATCH run (TOC rows quote no rule sentence:
  each OWNER_KEYS key absent from the TOC).
- Lead places: everything (CLAUDE.md is a mechanism path).

### 7.3 Regeneration steps
`python -B C:/QAFactory/forge-repo/tools/agents_md.py --repo <worktree root>` then stage `AGENTS.md` (builder-rules 17). A conflict
in `AGENTS.md` or `docs/OWNER_PRINCIPLES_INDEX.md` at merge is resolved by regenerating, never by hand. Parity anchors: edited by
hand (no generator); checked by `install_parity.py --check`.

### 7.4 The DOC-DISPATCH witness (mechanical layer of INV-M)
Per stream, before the run, the DoD quotes the keys VERBATIM from this spec: for each K2 row the stream owns — the first 60 and the
last 60 characters of the moved block or clause AFTER squashing (`" ".join(text.split()).casefold()`, the function `squash` of
`tools/tests/test_role_carriers_one_owner.py:77-78`; m10), its destination and its source; a block shorter than 120 squashed
characters is one key, whole. The script compares squashed text on both sides, so a re-wrap, a re-indent or a list item turned
into a heading does not break a key. It prints per key `present-in-destination yes/no`, `absent-from-source yes/no`, exits 1 on
any `no`. A K4 row: the key is the home's clause, checked `present-in-home`. Negative control in the same run: one key altered by
one character → the script reports failure. The script is attached in full to the report, never committed (CLAUDE.md rule 11).

### 7.5 Readers of every touched file (designer rule 3; the Grep tool; counts as printed)

| Touched file | Search | Hits | Reader → verdict |
|---|---|---|---|
| CLAUDE.md | `CLAUDE\.md[`'"]?,? (rule\|routing rule\|command hygiene\|pt\.\|point)\s*\d+` -i over `tools/` (16.11) | 34 in 20 files | rule-number citations (`dispatch_manifest.py:138,157`, `dispatch_gate.py:620,710`, `journal_write.py:58,416`, `mechanism_gate.py:14,286`, …) → **unchanged** (numbers stable, E1) |
| CLAUDE.md | same over `.claude/agents` / `.claude/skills` | 4 / 8 | → unchanged |
| CLAUDE.md | `["'](CLAUDE\|PROJECT)\.md["']` over `tools/*.py` | agents_md.py:31; session_context.py:193; claim_control_gate.py:253; mechanism_gate.py:212; test_role_carriers :45-72 | agents_md → regen (S2, S1); session_context, claim_control_gate, mechanism_gate → unchanged (F6 n/a); test_role_carriers → changes in S2, S1 |
| CLAUDE.md | `Routing log\|SHAPES table\|Event SHAPES` over `tools/` | 3 | → unchanged (the section stays whole) |
| CLAUDE.md (anchors) | `install_parity_anchors.json` unit `routing-policy` | 89 | → unchanged, except an anchor quoting the C12b (1) line, if any (S2, same commit) |
| CLAUDE.md | architect spec Stream L | — | **changes in the architect stream L** (same file, lands BEFORE S2/S1; §7.1) |
| PROJECT.md | `PROJECT\.md` over `tools/` (16.11) | 50 in 12 files | `agent_budget.py:278` compaction line → unchanged (compaction stays in PROJECT.md, now § Сессия форджа); `language_sites.py:106` «PROJECT.md P31» → unchanged (E3); `piles.py:2183` ««Командная работа» п. 2» → unchanged (E2, 2 hops); `test_quarantine.py:1805` → unchanged; `test_session_context.py:1188` → changes in S2; `test_role_carriers` → changes in S2, S1; the rest → unchanged |
| PROJECT.md | `PROJECT\.md[^\n]{0,60}(п\. ?\d+\|P\d+\|«)` over `.claude/agents` | 2 | `critic.md:165`, `designer.md:87` «PROJECT.md P31» → unchanged (E3) |
| PROJECT.md (section names, m6) | `PROJECT\.md.{0,60}(Командная работа\|Прогоны и эксперименты\|Как принимается\|Релиз\|Принципы владельца)` over `PROCESS/**`, `docs/*.md`, `DECISIONS.md`, `BOOT.md`, `SYSTEM_PROMPT.md`, `DELEGATION_TABLE.md`, `plans/builder-rules.md`, `docs/tasks/critic-diff-brief.md` (positive control: the same call found the known `docs/RUNBOOK.md:232`) | 33 lines in 8 files | RUNBOOK:232 → **changes in S2** (RB-3); RUNBOOK:115 → **changes in S2** (RB-2); RUNBOOK:164 («Прогоны и эксперименты», P8, P18) → unchanged (section stays; P ids via index, 2 hops); RUNBOOK:207, 369, 460 («Как принимается» п. 1-3, 6а) → unchanged; RUNBOOK:208, 346, 352 (п. 2), :377 (п. 4) → unchanged (2 hops via the numbered pointer); SIBLING_MAP:33 (п. 13 + 7b as the rule text of the dispatch axis) → unchanged: after B2 п. 13 still carries the dispatcher sentence this axis row is about (question Q1 to the Lead, t-903 m6 asked for an edit); SIBLING_MAP:308 (item 3 grammar) → **changes in S2, Lead-placed**; SIBLING_MAP:532 (p. 12, the cap) → unchanged; builder-rules:14 → **S2 B-1**; builder-rules:38 → **S2 B-2**; builder-rules:78 (п. 1) → unchanged; critic-diff-brief:88 (п. 6) → unchanged; PROCESS calibration :992 (section), :1095 (п. 9: check 39 judges `piles.py check` (д) — its text now in TEAMWORK § 9, 2 hops), :1101, :1111 (п. 6) → unchanged; DECISIONS_ARCHIVE (10), CLAUDE_HOST_ADAPTATIONS_FULL (1), FINDINGS (1) → unchanged (history records) |
| PROJECT.md (unprefixed) | `Командная работа` over `docs/RUNBOOK.md` | RUNBOOK:102 «(«Командная работа» п. 12)» | → unchanged (12-6 stays) |
| PROJECT.md (internal) | «(п. «Релиз»)» in п. 5 (:317) | 1 | → unchanged (2 hops via the «## Релиз» pointer) |
| plans/builder-rules.md | `builder-rules` over `tools/` (16.11) | 24 in 11 files | `dispatch_gate.py:1866` «item 20» → unchanged; `test_handoff_rule_anchors.py` → unchanged; `test_role_carriers` keys/anchor 7b → unchanged (openers byte-identical); `test_quarantine.py:51` FORGE_CARRIERS → unchanged; the rest → unchanged |
| plans/builder-rules.md | `.claude/agents/builder.md:52` «CI is neither started nor waited for» → points to 7b | 1 | → unchanged; resolves after S2 B-3 (no loop) |
| docs/RUNBOOK.md | `RUNBOOK` over `tools/` | 8 in 4 files | `dispatch_gate.py:1866,1945` «§12 item 8» → unchanged; `test_quarantine.py:490,498,1175` «section 7» → unchanged (§7 keeps its number; § 4.1 is new); `test_role_carriers` → changes in S2 (rows added) |
| role files | `PROJECT\.md\|builder-rules\|RUNBOOK\|critic-diff-brief\|TESTING\.md\|AGENTS\.md` over `.claude/agents` | 12 in 3 files | → unchanged, except designer.md rule 7 (S3) |
| role files | parity units `role-profiles:*` | builder 10, critic 21, designer 12, scout 12 | → unchanged (no opener moves; designer rule 7 appended) |
| docs/TESTING.md, critic-diff-brief | `test_role_carriers` BRIEF keys/anchors | 7 rows | → unchanged (S3 keeps those lines) |
| skills | same search over `.claude/skills` | 2 (boot-diet:36,38) | → unchanged |
| `.claude/settings.json` | `PROJECT\.md\|CLAUDE\.md\|builder-rules\|RUNBOOK` | 0 | no reader |
| tools/factory_rules_index.py | `factory_rules_index\|FACTORY_RULES_INDEX` over `tools/` + `.githooks` | 19 in 6 files + pre-commit:54 | `test_factory_rules_index.py` → changes in S4; `mechanism_gate.py` prefix → unchanged; pre-commit:54 → unchanged (checks every row); `test_workflows.py` → unchanged (no CI edit) |
| install_parity_anchors.json | readers `install_parity.py:19,754`, `test_install_parity.py:39`, `forge-check.yml:91,94` | — | → unchanged code |
| test_role_carriers_one_owner.py | pytest; CI | — | → rows change (S2, S1; FG7-52 later extends its scan) |
| AGENTS.md | `agents_md.py --check` | pre-commit, forge-check.yml:80 | → regenerated |
| `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md` | check-33 line (Lead, S2) | — | **also changed by architect Stream F** (checks 5, 6, 18) — sequential (F before L before S2) |
| new files (OWNER_PRINCIPLES.md, OWNER_PRINCIPLES_INDEX.md, TEAMWORK.md) | created by this node | 0 readers before | after: the TOCs, pointer lines, POINTERS rows, (index) the CLAUDE.md import and S4's `--check` |

### 7.6 Ready rows for the Lead (m11, A1, m5) — the designer does not edit batch files
```
| FG7-51 | П1 | Перестройка бута по темам: один дом на тему, оглавление «тема → где» в `CLAUDE.md` и `PROJECT.md`, правила роли в файле роли, смысл правил не меняется; спека `docs/tasks/specs/20261116-boot-by-topic-spec.md` (потоки S3, S4 → S2 → S1) (та же находка, п. 2; новая идея: план владельцу → дизайнер → критик на план t-903) | Lead → designer → critic → builder | `CLAUDE.md` (Lead), `PROJECT.md`, `AGENTS.md`, `.claude/agents/designer.md` (Lead), `plans/builder-rules.md`, `docs/TESTING.md`, `docs/tasks/critic-diff-brief.md`, `docs/RUNBOOK.md`, `docs/OWNER_PRINCIPLES.md`, `docs/OWNER_PRINCIPLES_INDEX.md`, `docs/TEAMWORK.md`, `tools/factory_rules_index.py` (Lead), `tools/test_factory_rules_index.py`, `tools/tests/test_role_carriers_one_owner.py`, `tools/test_session_context.py`, `tools/install_parity_anchors.json` (Lead); строки `docs/SIBLING_MAP.md` и проверка 33 `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md` — Lead | FG7-50 (принято); S2, S1 — после потока L спеки 20261116-architect-tier; п. 9 — после t-907 | ожидает |
| FG7-52 | П2 | Указатели и оглавления сверяются кодом: скан `tools/tests/test_role_carriers_one_owner.py` (K-PTR) расширяется на строки `правило: <файл> § <раздел>` / `rule: <file> § <section>`, ячейки оглавлений `CLAUDE.md`/`PROJECT.md`, пути, диапазоны FR/P/rules и числа гейтов в текстах правил (контракт — спека boot-by-topic §4.3); отдельного `tools/pointer_lint.py` нет (A1; P31, AR-15); пары записаны в `docs/SIBLING_MAP.md` (та же находка, п. 3; AR-13, FR-54) | builder → critic; строки карты — Lead | `tools/tests/test_role_carriers_one_owner.py`, `docs/SIBLING_MAP.md` (Lead) | FG7-51 | ожидает |
| FG7-55 | П3 | Один генератор индексов: `tools/architecture_index.py` становится строкой таблицы источников `tools/factory_rules_index.py` (кап 3072 Б — поле строки), вывод `docs/ARCHITECTURE_INDEX.md` байт в байт; строка pre-commit `:58` и шаг CI для AR снимаются (Lead) (спека boot-by-topic §7.2 S4, критик t-903 m5; P31, AR-15) | builder → critic | `tools/factory_rules_index.py`, `tools/test_factory_rules_index.py`, `tools/architecture_index.py`, `tools/test_architecture_index.py`; `.githooks/pre-commit`, `.github/workflows/forge-check.yml` (Lead) | FG7-51 (S4) | ожидает |
```
FG7-55 needs, in the same move, a finding file in `plans/piles/forge/findings/` and a «Содержание» row of the card (PROJECT
«Командная работа» п. 2) — the Lead's move.

---

## 8. Edges (each with the invariant it protects)

- **E1 rule cited by number from code refusals.** Numbers never move; headings go ABOVE the opener; the opener line stays
  byte-identical. Invariant: every number citation (34 in tools, 4 in agents, 8 in skills, 44 in the calibration protocol) resolves to
  the same clause, in CLAUDE.md, in one hop.
- **E2 PROJECT numbered items that move or split** («Командная работа» п. 2, 3, 4, 8, 9, 13; «Как принимается» п. 2, 4). The number
  stays in PROJECT.md as «N. **<bold title verbatim>** — правило: <file> § N», followed by the clauses that stay (§3.4). Invariant:
  «п. N» reaches its text in ≤ 2 hops; no number is reused; a clause that stays is never behind a pointer.
- **E3 «PROJECT.md P<n>».** PROJECT § Принципы владельца keeps the pointer; the index line «P<n> — <first sentence, capped>» is in the
  boot. Invariant: every P id is visible in every session and reaches its text in ≤ 2 hops.
- **E4 pointer whose target section is later renamed.** POINTERS rows now, FG7-52 later; renaming turns red. Invariant: a dangling
  pointer is never silent (a false red, never a false green).
- **E5 a rule that is both the coordinator's and a worker's.** Home = the executor's file; a DISPATCHER duty's executor is the
  dispatcher (boot). Invariant: no rule sentence in two carriers; the checker keeps its one sentence.
- **E6 worktree copies; kit twin.** Phase 0 refuses to start while an open branch owns a touched file; no kit twin (Q12). Invariant:
  no merge re-adds a moved clause — a late branch that edited a moved clause conflicts and the late node resolves it into the HOME
  (PROJECT «Командная работа» п. 3, clause 3b), re-running §7.4.
- **E7 TEMPORAL — files this node creates** (`docs/OWNER_PRINCIPLES.md`, `docs/OWNER_PRINCIPLES_INDEX.md`, `docs/TEAMWORK.md`). Before:
  absent, no pointer names them, the import pin lists three imports, S4 prints `skip`. After: present, created in the SAME commit
  (S2) that removes the text from its source, adds the pointers, the import and the pin row. Invariant: no commit in which a rule is
  in no carrier, or in two (hence all PROJECT↔builder-rules↔RUNBOOK exchanges are S2's).
- **E8 nested imports.** Forbidden — imports only from CLAUDE.md, one level. Invariant: the BOOT BUDGET never reports fewer bytes than
  the session pays (Q1 vs Q4).
- **E9 BOOT.md regex.** New files live under `docs/`, never named in BOOT.md as `Read NAME.md`. Invariant: the budget counts exactly
  what is loaded.
- **E10 TOC rows quote nothing.** Topic names only. Invariant: a TOC row never counts as a restatement of an OWNER_KEYS sentence.
- **E11 parity anchors.** No text moves out of CLAUDE.md (F5 → c); C12b (1) changes one line — an anchor quoting it is updated in
  the same commit. Invariant: every clause pinned before is pinned after.
- **E12 mechanism-gate net.** No CLAUDE-origin text leaves (F5 → c, F6 n/a); PROJECT-origin homes keep PROJECT.md's ungated status
  (Q13). Invariant: this node changes no gate status.
- **E13 AGENTS.md.** Regenerated by every stream whose sources changed. Invariant: `agents_md.py --check` green on every commit. New
  docs are not imported (except the P index), so a Codex developer follows the same pointers as a Claude session.
- **E14 limit ~40 lines.** A section over ~40 lines gets a sub-heading at a paragraph boundary (§6 item 2); a single table may exceed
  it; over 50 lines without a table is a finding (check 33 line).
- **E15 empty home.** `home: none — queued <node>`. Invariant: no invented home.
- **E16 conflicting requirements.** (в) vs the budget: role text goes to role files only. (а) vs the TOC: the TOC routes (E10).
  FG7-50's «до минуты каждый» vs R2: R2 (the Lead's later decision, «решила сама», owner told) wins unless the owner objects.
  B5's «discipline stays» vs the budget: discipline wins; F19 covers the headroom.
- **E17 the architect-tier spec lands first.** S1 (and S2's CLAUDE.md edits) read the headings and lines as Stream L left them.
  Invariant: a TOC cell equals an existing heading; S2's C12b edit applies to the live line, re-located by its quoted text.
- **E18 language.** F8 (a); TR1 is the one translated clause. Invariant: no moved rule is paraphrased by translation without a row.
- **E19 OWNER_KEYS `cost:queue`.** R1 changes the sentence; S2 re-quotes the key «цель держать 6 пишущих билдеров» in the same commit.
  Invariant: the owner keeps exactly one key, in PROJECT.md (the key appears nowhere else — the test proves it).
- **E20 п. 9 is t-907's text** (Q20). Order: t-907's п. 9 edit lands BEFORE S2. S2 then re-reads п. 9 as it stands, re-derives the
  9a-9f split by §5.1 (clauses t-907 added are judged by the same criterion; a new clause with no refusing gate stays) and quotes its
  K2 keys from the live text. If S2 is ready first and the Lead does not want to wait, S2 moves п. 9 verbatim as in §3.4b, and the
  Lead re-syncs t-907's spec so its builder writes into the two homes (TEAMWORK § 9 for gated clauses, PROJECT п. 9 for discipline).
  Invariant: п. 9's meaning is decided once, by t-907; this node never rewrites it.
- **E21 the PROJECT TOC row to CLAUDE § Contents (TEMPORAL).** CLAUDE § Contents does not exist until S1; S2's PROJECT TOC omits the
  row; S1 adds it with its POINTERS row. Invariant: no TOC cell ever names a heading that does not exist.
- **E22 headroom.** If the BOOT BUDGET measured in S2 or S1 exceeds 108000, or CLAUDE.md exceeds 47800, the stream stops before
  commit and reports the number; the Lead applies F19. Invariant: the node never lands a boot over WARN silently.

---

## 9. Forks

### Decisions in force (the owner 17.11.2026; the Lead 17.11.2026) — supersede the draft's «Lead decisions» section
- The owner's «да» (17.11.2026, Lead session) to the Lead's recommendations: **F2 (b)** — applied at CLAUSE level (b') per the Lead
  (her criterion: «what code holds may leave»; §5.1, §3.4b); **F3 (a)** P1-P31 to `docs/OWNER_PRINCIPLES.md` with a generated
  imported index (bullets verbatim, capped lines — m2); **F9 (a)** the local fallback needs BOTH conditions (R5).
- The Lead: F1 (a), F4 (a), F7 (a), F8 (a), F11 (a), F12 (a) (with the m8 detector line), F14 (a), F16 (a); A1 accepted (FG7-52
  extends `tools/tests/test_role_carriers_one_owner.py`, no `pointer_lint.py`); **F5 → (c)** and **F6 → n/a** (the Lead: follow the
  review, m3/m4); B1-B5 as in the fix table; R1 carrier = the owner's message 16.11.2026 evening (m12); R2 = the Lead's.

### Fork list (status per fork)
- **F1 — rule 11 split.** Decided (a): number kept, sub-headings only.
- **F2 — «Командная работа».** Decided (b'), the owner + the Lead: gated clauses → `docs/TEAMWORK.md`, discipline clauses stay.
- **F3 — P1-P31.** Decided (a), the owner.
- **F4 — TOC shape.** Decided (a).
- **F5 — Routing log.** Decided (c): nothing moves (t-903 m3: the daily `feature: Fnn` duty has only a WARN on the path; 2.0 KB
  measured is not worth a new home).
- **F6 — mechanism net for new homes.** Not applicable (no CLAUDE-origin text leaves).
- **F7 — «Релиз» → RUNBOOK § 4.1.** Decided (a).
- **F8 — language.** Decided (a).
- **F9 — local fallback.** Closed: not a contradiction (t-903 m1); the owner's «да» to (a) is carried as R5 (both sentences side
  by side + one explicit clause).
- **F10 — carriers.** Closed: R1 the owner's message 16.11.2026 evening; R2 the Lead's; R3 the boot's own п. 1/п. 13; R5 the owner's
  «да» 17.11.
- **F11 — role files import or point.** Decided (a).
- **F12 — home of §6.** Decided (a); F19 may move it to boot-diet (c).
- **F14 — 7d vs TESTING.** Decided (a), executed with the key-presence rule (S3-5).
- **F16 — TOC check before FG7-52.** Decided (a).
- **F17 (NEW) — the integrator's local run in two carriers.** PROJECT п. 2 «Интегратор перед коммитом гоняет только свидетелей узлов и
  `--limits --lang`» vs builder-rules 7b:51-52 «интегратор локально гоняет только узкие свидетели узлов с конфликтом слияния и
  `--limits --lang`, затем push». Compatible (the 7b sentence is the narrower case of the same cap; pushing is added), but two
  carriers. (a) both verbatim side by side in RUNBOOK §7 «**Интегратор.**», 7b keeps a pointer (S2 B-5) — no rewording, one home;
  (b) 7b keeps its sentence, RUNBOOK gets PROJECT's — two carriers stay (against direction (а)); (c) a joint rewording → a K5 row R6
  needing a carrier (the owner or the Lead). **Recommend (a)** — the same move m1 recommended for F9; executable on the
  recommendation.
- **F19 (NEW) — headroom.** With F5 dropped and B1-B5 keeping more text, the est. lands at the WARN line (≈ 107.7 KB) and CLAUDE.md
  over its own WARN (≈ 48.6 KB est.). Options: (a) headings only where needed — a numbered rule's number is its anchor (TOC cells
  `CLAUDE.md § 3`), sub-headings only inside rules over ~40 lines (2, 4, 10, 11, 12), the unnumbered sections and the Routing-log
  SHAPES table; CLAUDE TOC ≤ 2.0 KB (≈ −1.5 KB est.; it reads the owner's direction (г) «one heading per topic» as «a numbered rule
  already has its heading — its number»: an interpretation, hence a fork); (b) a heading above every rule as drafted, accept the
  WARNs (they print every session); (c) restore F5 (a) (−2.0 KB measured, a new file + a net row + S1 work); (d) (a) + §6 into
  boot-diet (F12 c, −1.9 KB). **Recommend (a)**, applied in S1/S2 from the start; if the measured BOOT BUDGET after S2 is still above
  104000, add (d). The Lead measures (E22).

## 10. Small choices closed by the designer
- New file names `docs/OWNER_PRINCIPLES.md`, `docs/OWNER_PRINCIPLES_INDEX.md`, `docs/TEAMWORK.md` — under `docs/` (scanned by the
  one-owner test, not matched by the BOOT.md regex, E9). `docs/JOURNAL.md` and the parity unit `routing-journal-doc` are dropped.
- Heading text: `### Rule N · <sub-topic>` in CLAUDE.md; PROJECT new sections `## Сессия форджа` (short, so `§ Сессия форджа`
  resolves by the §4.3 grammar), `## Бэклог и находки`, `## Как пишутся правила для агентов`; RUNBOOK `### 4.1. Шаги релиза` (RUNBOOK's
  own numbering style).
- `docs/OWNER_PRINCIPLES.md` sub-headings by source-order ranges «### P1–P9», «### P10–P17», «### P18–P22», «### P23–P26», «### P27–P31»
  (no reordering; the index is the topic map of the principles).
- S4: per-line cap 220 B, per-file cap 6144 B, the cut rule; the P index header in English like the FR index, its lines in Russian.
- designer.md readers paragraph → appended rule 7 (no renumbering).
- Connectives in pointer lines («При общем файле», «Диспетчеру:») and the TEAMWORK 3a «:» → «.» — listed in their rows for the critic.
- R1 (b) + the kept fragment «, — дверью `budget-skip:`» joined in one sentence; «билдеров» added to R1 (a).
- The R2 and B2 builder-rules edits moved from S3 to S2 (E7: one commit per exchange); builder.md dropped from S3's owns (it changes
  nothing; its `:52` pointer resolves after S2).
- PT5 kept whole (class sweep: not a restatement); «Критик кода — один на тему» kept K1 (no byte gain).
- 4b (B-id issuance) kept in the boot: no refusing gate established (safe default).
- E20 order: t-907 → S2 for п. 9, with the named fallback.

## 11. Analogs and contradictions noticed (reported, scope not widened)
- A1 — accepted by the Lead (FG7-52 extends the existing test; ready row §7.6).
- A2 — PROJECT.md is not a mechanism path (Q13); unchanged by this node.
- A3 — `claim_control_gate.ROOT_FILES` scopes negative-claim checks to CLAUDE.md, BOOT.md, … not PROJECT.md; text moving between
  them changes coverage. Not this node's.
- A4 — the budget counter (one level) and `agents_md.py` (five levels) read imports differently; E8 avoids the gap.
- A5 — builder-rules 7b on who runs the canon — resolved by R3 (S3-4, RB-1).
- A6 — RUNBOOK §7 vs PROJECT п. 2 on the local fallback — R5.
- A7 (new) — batch file headers say «BATCH CANON — интегратор» (e.g. `plans/piles/forge/batch-7-vhodyashchie-4.md:10`) — the same
  R3 class in `plans/piles/`, which this node does not touch (frozen/taken batches; the Lead's call whether to sweep untaken ones).
- A8 (new) — the integrator-run sentence in two carriers (F17).
- A9 (new) — the t-907 spec is not on disk (Q20); E20's order depends on its landing.

## 12. Reading trail
Draft (t-894): see the previous revision's trail (BOOT.md, builder-rules, role files, CURRENT_CONTEXT, critic-diff-brief, TESTING,
SESSION_PROTOCOL, DELEGATION_TABLE, install_parity_anchors, test_role_carriers, boot-diet; session_context, agents_md, mechanism_gate,
claim_control_gate, test_session_context, test_agents_md, test_install_parity, factory_rules_index, RUNBOOK:86-175, SIBLING_MAP:471-565).
Fix round 1 (t-912), read: the review `docs/tasks/specs/reviews/t-903-boot-by-topic-plan.md` whole; this spec whole; `PROJECT.md:176-380`;
`plans/builder-rules.md` whole; `docs/RUNBOOK.md:80-129`; `docs/tasks/specs/20261116-architect-tier-spec.md:409-560` (+ its heading
grep); `plans/piles/forge/batch-7-vhodyashchie-4.md:1-80`; `docs/tasks/compact-snapshots/2026-11-17-0040-narrative.md:30-49`;
`tools/tests/test_role_carriers_one_owner.py:20-79`. Greps: `tools/piles.py` check items and doors (`\((б|в|г|д|е)\)|piles-skip|B-id`);
`docs/TESTING.md` headings and «слову владельца|quarantine-watch» and «Кто что делает|Что запускать|Билдер»; `docs/tasks/critic-diff-brief.md`
«Mechanical layer»; `.githooks/pre-commit` «index»; `docs/SIBLING_MAP.md` «Командная работа» (-o); `docs/RUNBOOK.md` headings and
section-name citations; the m6 section-name grep over PROCESS/docs/root files (33 lines / 8 files; control: RUNBOOK:232 found);
`.claude/agents/designer.md` openers. Globs: `docs/tasks/specs/20261117-*.md` → none, control `docs/tasks/specs/2026111*-*spec.md` →
47; `tools/test_*index*.py` → 2. A first Grep with a brace glob over two `docs/` subpaths returned nothing and was re-run per file
(the miscall noted, not reported as absence).
Not measured: every byte figure marked est.; the architect additions; whether any `routing-policy` anchor quotes the C12b (1) line.

---

## Fix round 1 (t-912) — review t-903

| Finding | What changed | Section |
|---|---|---|
| B1 | R1 replaces ONLY the cap sentences of п. 12 (12-1, 12-3, 12-7); 12-2, 12-4, 12-5, 12-6, 12-8 (`budget-skip:`), 12-9 keep their own verbatim rows; ready text given; OWNER_KEYS `cost:queue` re-quote named | §3.2 PT12, §3.3 R1, §3.4c, §8 E19 |
| B2 | п. 13 listed clause by clause; 13-b (CI not started/waited) and 13-e (who reads `main`'s pipeline) K2 into builder-rules 7b; 13-g (dispatcher sentence) stays in the boot; pointer loop builder.md:52 ↔ 7b resolved; the additions moved to S2 so the exchange lands in one commit (E7) | §2 T5, T33; §3.2 PT13; §3.4d; §7.2 S2 B-3, B-6 |
| B3 | PA2 full clause list (2-1…2-15); the wait-loop clause stays in the boot on a «Диспетчеру:» line (the Lead's recommendation); 2-13 bare push → RUNBOOK:90, 2-8 «Канон всегда на CI … не больше часа» → RUNBOOK §7 named | §3.2 PA2, §3.4a, §2 T33 |
| B4 | Executability rewritten: S3 and S4 start now; S2 and S1 start after architect Stream L (S2 also after S3/S4; S1 after S2); headings and TOCs land WITH the moves, never before (≈ 131.6 KB est. otherwise); the old «streams that only add headings do not wait» sentence removed | §7.1, §5.2, §9 Decisions in force |
| B5 | F2 (b) applied at clause level: table for п. 2, 3, 4, 8, 9 + check line with the refusing gate per clause (Q21); discipline clauses (2f, 2g, 3b, 3c, 9c-9f) and the unproven-gate clause 4b stay; ready boot text and TEAMWORK layout given | §3.4b, §5.1, §2 T18, §0 Q21 |
| m1 | F9 is no longer a fork; both sentences side by side in RUNBOOK §7 + one explicit clause carried as R5 (the owner's «да» 17.11) | §3.3 R5, §3.4a 2-15, §9 F9 |
| m2 | P bullets moved verbatim (true K2); S4 derives a capped line (220 B/line, 6144 B/file) with a cut rule and refusal; index bytes use the measured 6485 B as the uncapped figure | §3.2 P-rows, §7.2 S4, §5.2 |
| m3 | F5 → (c): C-RL3 stays in CLAUDE.md; `docs/JOURNAL.md` dropped | §3.1 C-RL1..4, §1.4, §9 F5, §10 |
| m4 | No parity unit `routing-journal-doc`; F6 n/a; S1 owns shrink (no mechanism_gate) | §7.2 S1, §8 E11, E12 |
| m5 | «One road» claim corrected: AR index stays a second generator; fold queued as FG7-55 (ready row); S4 drops pre-commit and CI edits (pre-commit:54 checks every row) | §7.2 S4, §7.6, §0 Q22 |
| m6 | Section-name readers outside tools walked (33 lines / 8 files, with control); RUNBOOK:232, :115 and builder-rules:14, :38, :40-41, :51 edits given to S2; SIBLING_MAP:308 to the Lead-placed list; SIBLING_MAP:33 kept unchanged with evidence (question Q1) | §7.5, §7.2 S2 (B-1, B-2, B-4, B-5, RB-2, RB-3, Lead places) |
| m7 | Q18 and Q19 refreshed (architect spec on disk; FG7-50 builder-rules landed, CLAUDE part not); C6 drops the D-0046 claim; the architect additions (+1.0 KB est.) counted; Phase 0 re-measures | §0 Q18, Q19; §1.4; §3.1 C6; §5.2; §7.1 |
| m8 | Four-question block for §6 in S2's commit; calibration check 33 line (retelling, > 50 lines, heading with no TOC route) registered, «on discipline until FG7-52» stated; TOC completeness gap named | §6, §4.3 item 5, §1.3, §7.2 S2 Lead places |
| m9 | §6 item 2: a sub-heading only at a paragraph boundary, never between condition and consequence; inside a numbered rule it repeats the number | §6 item 2, §8 E14 |
| m10 | DOC-DISPATCH keys compared whitespace-squashed + casefolded (the test's `squash`); short blocks one key | §7.4 |
| m11 | Ready batch rows for FG7-51 (all ~18 paths) and FG7-52 (no `pointer_lint.py`, extends the existing test), plus FG7-55 | §7.6 |
| m12 | R1 carrier = the owner's message 16.11.2026 evening in the Lead session; the snapshot line named as a Lead paraphrase/locator only; R2 written as the Lead's | §3.3 R1, R2; §0 Q25; §9 F10 |
| m13 | «Прогоны» bullet count corrected to 7 (PR1-PR7) | §3.2 count line |
| both-refused scenario | Row added (≈ 128.0 KB est., over BREACH) with the fallback (S3, S4, PA2, п. 13, «Релиз» moves + §6 in boot-diet, TOCs deferred → ≈ 119.1 KB est.) | §5.2 |
| owner's word 17.11 | F2 (b'), F3 (a), F9 (a) recorded as decided; «asked of the owner» wording and the old «Lead decisions» / «The owner's word» sections replaced by «Decisions in force» | §9, header |
| t-907 / п. 9 | п. 9 marked «text owned by t-907, moved verbatim, re-synced after t-907 lands»; order t-907 → S2 with the named fallback; t-907 spec not on disk (Q20) | §3.2 PT9, §3.4b, §8 E20, §0 Q20, §7.1 |
| class sweep (not a review finding) | PT5 kept whole (its journal clause is not a pure restatement); R3 also aligns RUNBOOK:108; C12b's R1 alignment and TR1 moved into S2 so R1 lands in one commit; PROJECT TOC row to CLAUDE § Contents made TEMPORAL (E21); CLAUDE.md over its own WARN after F5 dropped → F19; integrator sentence in two carriers → F17; batch headers «BATCH CANON — интегратор» noted (A7) | §3.2 PT5, §3.3 R3, §3.1 C12b, §8 E21, E22, §9 F17, F19, §11 |
| review §6 (forks to change) | F5 → c, F9 → not a fork, F2 → b', F3 a with m2, executability per B4, F12 a with m8 — all applied | §9 |
| review §8 (what the plan does not need) | JOURNAL/F5/F6/parity unit dropped; S4's hook/CI edits dropped; F9 as owner question dropped; §4.3 kept as a note, not DoD | §1.4, §4.3, §7.2, §9 |
