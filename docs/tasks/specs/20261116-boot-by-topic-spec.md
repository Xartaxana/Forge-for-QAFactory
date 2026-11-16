# FG7-51 — the boot by topic: one home per topic, a table of contents, the boot under budget (DRAFT)

task: t-894 | node: forge/7/FG7-51 | feature: F19 | designer draft, 17.11.2026 | status: DRAFT — forks open, Lead decides
source: the owner's word 16.11.2026 (finding `plans/piles/forge/findings/20261116-but-odna-tema-v-mnogih-mestah-kopii-pravil-ustareli.md`,
item 2, direction (а)–(д) chosen); Lead intent brief of t-894.

Reading rule for this draft: «est.» marks a byte figure computed as lines × the file's average bytes per line — an ESTIMATE,
not a measurement (the designer has no shell). Every est. is re-measured by the stream that makes the move, with
`python -B C:/QAFactory/forge-repo/tools/session_context.py` (prints the BOOT BUDGET line; `.claude/skills/boot-diet/SKILL.md:21-24`).

---

## 0. Premises (each load-bearing fact, with its carrier)

| # | Fact | Carrier (file:line or command → output) |
|---|---|---|
| Q1 | Boot budget = files named by BOOT.md `Read X.md` lines + CLAUDE.md + CLAUDE.md's `@` imports, ONE level, no recursion | `tools/session_context.py:1042-1063` (regex `Read ([A-Z_]+\.md)`), `:1153-1162` («one level, no recursion into the imported files») |
| Q2 | Thresholds: WARN > 108000, BREACH > 120000; CLAUDE.md own WARN 47800 | `tools/session_context.py:189-191`, `:214` |
| Q3 | Measured 16.11: 123942 B; per file (brief): CLAUDE.md 43476, PROJECT.md 62252, FACTORY_RULES_INDEX 5575, ARCHITECTURE_INDEX 2682, DECISIONS.md 7547, CURRENT_CONTEXT.md 1783 (sum 123315; the remaining 627 B is SYSTEM_PROMPT.md, BOOT.md Layer A) | SessionStart line quoted by the Lead brief; BOOT.md:14-15, 27 (SYSTEM_PROMPT.md, DECISIONS.md, CURRENT_CONTEXT.md); NOT re-measured by the designer |
| Q4 | `agents_md.py` expands imports RECURSIVELY (MAX_DEPTH 5) — the budget counter does not | `tools/agents_md.py:35`, `:69-80` vs Q1 |
| Q5 | A real-repo pin of the import list | `tools/test_session_context.py:1185-1189`: `assert [...] == ["PROJECT.md", "docs/FACTORY_RULES_INDEX.md", "docs/ARCHITECTURE_INDEX.md"]` |
| Q6 | Subagents auto-load CLAUDE.md (so every worker pays CLAUDE.md + imports) | `PROCESS/LEAD_RANKING_EXAM.md:19` «2. Claude Code subagents auto-load CLAUDE.md, so the policy is already in their context» |
| Q7 | CLAUDE.md: 446 lines; headings at 1, 21 (Tiers), 35 (Routing rules), 272 (Routing log), 350 (Role ≠ tier), 381 (Lead degradation), 403 (Command hygiene) | Grep `^(#+ \|\d+[a-z]?\. ...)` over CLAUDE.md; Read CLAUDE.md:440-446 (last line 446) |
| Q8 | PROJECT.md: 422 lines; headings 18, 36 (P1–P31, lines 41-175), 176, 235, 256, 279 (Командная работа, items at 285-361), 371, 381, 393, 407 | Grep `^(#+ \|\d+\. \|- \*\*P\d+\.)` over PROJECT.md; Read PROJECT.md:404-422 |
| Q9 | An existing one-owner + pointer test already enforces direction (а) for listed keys: 13 OWNER_KEYS, 20 POINTERS; scan excludes `plans/piles/`, `docs/tasks/specs/`, AGENTS.md | `tools/tests/test_role_carriers_one_owner.py:24-26, 35-74` |
| Q10 | That test pins, among others: key «в работе всегда шесть пишущих билдеров» owned by PROJECT.md; PROJECT.md must hold «`plans/builder-rules.md` п. 7b» and «`docs/tasks/critic-diff-brief.md`»; builder-rules must hold «7b. **Уровень билдера и уровень пачки**» | same file :49, :54-55, :30 |
| Q11 | install-parity anchors quote CLAUDE.md lines (unit `routing-policy`, 89 anchors) and every role file's rule openers; checked in CI | `tools/install_parity_anchors.json:2-98`; `.github/workflows/forge-check.yml:91,94` (`python tools/install_parity.py --check`) |
| Q12 | No kit twin in this repo: `toolkit/` absent | Glob `toolkit/*` → no files; positive control Glob `tools/install_parity*.py` → `tools\install_parity.py`; `tools/test_install_parity.py:958-964` skips the freshness test on this (host) layout |
| Q13 | Mechanism-gate net holds CLAUDE.md, BOOT.md, `.claude/agents/`, `.claude/skills/`, `PROCESS/`, `docs/SIBLING_MAP.md`, `tools/factory_rules_index.py`, `tools/session_context.py`; it does NOT hold PROJECT.md, `plans/builder-rules.md`, `docs/RUNBOOK.md`, `docs/TESTING.md` | `tools/mechanism_gate.py:211-263`; Grep `MECHANISM_PREFIXES\|^MECHANISM\|PROJECT\.md\|CLAUDE\.md"` over mechanism_gate.py → only :211 and :388 (no PROJECT.md line); same grep found the `MECHANISM_PREFIXES` sample (positive control) |
| Q14 | AGENTS.md is regenerated from CLAUDE.md + imports + `.claude/settings.json` + `.claude/agents/*.md`; `--check` in pre-commit and CI | `tools/agents_md.py:1-12`; `.githooks/pre-commit:34`; `forge-check.yml:80` |
| Q15 | The boot-diet procedure exists and owns «how to diet»: deep cuts into operational homes need the operator's decision; moves are VERBATIM with a pointer left behind | `.claude/skills/boot-diet/SKILL.md:9-11, 57-64, 98-105` |
| Q16 | SIBLING_MAP axis 31 already states (а) for role aspects and requires «a new carrier of role text joins this table in the commit that creates it» | `docs/SIBLING_MAP.md:471-478, 552-557` |
| Q17 | `PARALLEL_CAP = 6`, door `budget-skip:` | `tools/dispatch_gate.py:1611, 1614` |
| Q18 | The architect-tier spec is not on disk yet | Glob `docs/tasks/specs/20261116-*.md` → none; control Glob `docs/tasks/specs/2026111*-*.md` → 54 files |
| Q19 | builder-rules on disk still carries the pre-FG7-50 text («дольше ~5 минут», «FR-1…FR-57», «Весь репозиторий на английском») | `plans/builder-rules.md:30-31, 78, 10` — the brief says assume FG7-50 landed; this spec does not re-specify those edits |

---

## 1. What changes, whom it serves, and the one invariant

### 1.1 What changes
1. Every topic of the boot and of the 14 in-scope files gets ONE home (file + section); every other place keeps a one-line
   pointer `rule: <file> § <section>` (Russian files: `правило: <файл> § <раздел>`), no retelling (§2).
2. CLAUDE.md and PROJECT.md begin with a table of contents (§4).
3. A rule that one role executes lives in that role's file; the boot keeps routing (§2, column «why this home»).
4. One heading per topic; a section is about 40 lines at most; buried rules get their own heading (§3, §6).
5. Text that only a role or a moment needs leaves the boot; the boot lands under 108000 B (the WARN line) with headroom (§5).
6. Four contradictions are resolved by the home's text (§3.3).

### 1.2 The invariant and how it is checked
**INV-M: no rule changes its meaning.** Concretely, every edit of this node is one of exactly five kinds; anything else is a defect:

| Kind | What it may change | Mechanical check (data, code) | Judgment check |
|---|---|---|---|
| K1 heading added | inserts a `###` line; touches no rule line | the opener line of every numbered rule stays byte-identical (install-parity anchors, Q11) | critic: the heading names the topic of what follows |
| K2 verbatim move | a whole paragraph / item / table moves to another file, byte-identical | DOC-DISPATCH key-presence run (§7.4): each moved block's first and last 60 characters present in the destination, absent from the source | critic: the block's context did not carry meaning (e.g. «above», «this rule») |
| K3 pointer left | the moved block's place holds `rule: <file> § <section>` plus, for a numbered item, its bold title verbatim | the pointer resolves (POINTERS rows of Q9, later FG7-52) | critic: the pointer says nothing the home does not |
| K4 restatement removed | a sentence that restates the home is replaced by a pointer | the home holds the sentence (key presence) | critic: the removed text was a restatement, not an extra clause — an extra clause moves (K2), never vanishes |
| K5 listed resolution | the four contradictions of §3.3 and nothing else | — | critic + the owner's word carrier quoted per row (fork F10) |

The critic of the plan and the critic of the diff verify by the table «rule: was where → is where» (§3), counting the rows against
the sources (CLAUDE.md rules 1–13 with sub-clauses, PROJECT.md P1–P31 and every numbered list).

### 1.3 Owners of the checks this node adds or alters (rule 10 / P27 wording; AR-29 census does not apply outside the package)
| Check | Owner it serves | Class |
|---|---|---|
| Pointer and TOC rows resolve (POINTERS table rows; FG7-52 contract §4.3) | data — code | shape / presence |
| One-owner keys moved with their text (OWNER_KEYS rows) | data — code | presence |
| install-parity anchors follow moved text (new unit per new home) | data — code | presence |
| BOOT BUDGET under 108000 | data — code (existing counter) | measure |
| «Meaning unchanged» per row of §3 | judgment — critic, accepted by the Lead | — |
| What leaves the boot (§5), the four resolutions (§3.3) | intent — the owner (forks F2, F3, F5, F7, F9, F10) | — |

AR-n: none — `ai-packages/qa-factory/` is not touched by any stream (owns in §7 hold no package path). `architecture: none --
forge-only (boot and role files)` on every commit; FR walk not required (PROJECT «Как принимается» п. 1 applies to the package).

### 1.4 Non-goals
- Rewriting the CONTENT of «Tiers», «Role ≠ tier», «Lead degradation» (the architect-tier spec, which lands first).
- The FG7-50 stale-copy fixes (assumed landed; Q19).
- The pointer linter itself (FG7-52); this spec states the contract it must check (§4.3).
- DECISIONS.md, CURRENT_CONTEXT.md, SYSTEM_PROMPT.md, the generated FR/AR indexes (only their bytes are counted).
- Changing any gate's behaviour (`dispatch_gate` cap, `hygiene_gate`, `piles.py`); `CLAUDE_WARN` stays 47800 (lowering is
  safe and optional, `session_context.py:210-213`).
- Package files, kb/, the release repo.

---

## 2. THE TOPIC MAP (core deliverable)

Rule for choosing a home (closes the edge «text that is both a coordinator's and a worker's rule»): **the home is the file of the
party that EXECUTES the duty; the party that CHECKS it holds a pointer plus at most one sentence of its own consequence** (axis 31
closing rule, `docs/SIBLING_MAP.md:552-556`). Invariant: no rule sentence lives in two carriers; a checker never loses the
sentence that tells it what to do when the rule bites.

«Home» uses the section names this spec creates (§3); `§ Rule N` = the heading this spec adds above rule N's opener.

| # | Topic | ONE home (file § section) | Why this home | Places that become pointers (each: the pointer line that replaces the text) |
|---|---|---|---|---|
| T1 | Tiers: who is scout/builder/critic/designer/Lead | CLAUDE.md § Tiers | routing; content per architect-tier spec | DELEGATION_TABLE.md:3-5 (already a pointer) |
| T2 | Routing: recon → scout, implementation → builder, drafting → designer | CLAUDE.md § Rule 1, § Rule 2, § Rule 2 · drafting | coordinator executes | designer.md header (role duty, stays); builder.md rule 1 (role duty, stays) |
| T3 | Dispatch form: DoD, edges, manifest, R11 header lines | CLAUDE.md § Rule 11 (sub-headings, F1) | dispatcher executes | designer.md rule 1 «the text is CLAUDE.md rule 11» (stays — pointer); builder.md rule 1 manifest sentence (role consequence, stays); scout.md rule 5 (role consequence, stays) |
| T4 | Witness: what a witness is; acceptance by witness | CLAUDE.md § Rule 2 (witness rule) | coordinator accepts | builder.md rule 4 (role consequence, stays); builder-rules 15 (role practice «pasted, not typed», stays); critic.md rule 7 (role consequence, stays) |
| T5 | What a builder may run (scope of its witness) | `plans/builder-rules.md` § 7b (+ 7, 7a, 7c) | builder executes (direction (в)) | CLAUDE.md § Rule 4 · witness scope keeps the DISPATCHER sentence (what the DoD names) + pointer; PROJECT «Как принимается» п. 2 → pointer line; PROJECT «Командная работа» п. 13 → pointer line; TESTING.md «Что запускать по своей правке» and «Кто что делает / Билдер» → pointer; critic-diff-brief «The two layers / Mechanical layer» list → pointer; builder.md rule 4 (already pointer) |
| T6 | Batch canon: CI on the batch branch, who runs it, witness append | CLAUDE.md § Rule 4 · witness scope and the BATCH CANON (duty) + `docs/RUNBOOK.md` §7 (procedure) | coordinator executes; RUNBOOK owns the recipe (axis 31 row :500) | builder-rules 7b canon paragraph lines 46-49 → pointer to RUNBOOK §7 (the «what canon covers» sentence stays in 7b, axis 31 :476); PROJECT «Как принимается» п. 2 canon sentences → RUNBOOK §7 (K2) |
| T7 | Which tests are written | `docs/TESTING.md` | its own text says so (TESTING.md:4-5) | CLAUDE.md § Rule 11 · which tests (already a pointer + the adversarial-battery DoD duty, stays); builder-rules 7d (F14); builder.md rule 8 (pointer, stays); critic.md rule 20 (pointer, stays) |
| T8 | Critic gate: when mandatory, two layers, plan gate, one pass per topic | CLAUDE.md § Rule 3 (+ R13 g) | coordinator decides | critic.md rule 9 (role consequence, stays); PROJECT «Новая идея» п. 6, п. 8 (stay: the order of a new idea, points to rule 3); PROJECT «Как принимается» п. 6(б) (stays, points to rule 3); PROJECT «Командная работа» п. 12 «Критик кода — один на тему» → pointer to rule 3 (K4) |
| T9 | Critic review content | `docs/tasks/critic-diff-brief.md` | critic executes | CLAUDE.md § Rule 3 «items 6-7» (pointer, stays); critic.md 18-20 (pointers, stay) |
| T10 | Journal: one writer, events, fields | CLAUDE.md § Routing log (core) + `docs/JOURNAL.md` (rare-event detail, F5) | coordinator writes; `journal_write.py` validates | hygiene pt. 5 (refusal; stays — the gate's rule); PROJECT «Командная работа» п. 5 journal clause → pointer to § Routing log (K4); CLAUDE.md § Rule 12 «journal lines through `tools/journal_write.py`» → stays as an item of the «what code does» list |
| T11 | Merge and CI reading | `docs/RUNBOOK.md` §7 «Слить принятое» (procedure) + PROJECT «Командная работа» п. 1 (who) | coordinator executes | CLAUDE.md § Rule 12 · what code does (one list line each, stays); PROJECT «Как принимается» п. 2 pipeline sentences → RUNBOOK §7; builder-rules 2 «Мерджи … — только интегратор» → resolution R3 |
| T12 | Six writers, the full queue | PROJECT «Командная работа» п. 12 (stays in the boot, §5) | the owner's word; coordinator executes | CLAUDE.md § Rule 12 · Cost gates writer clause → pointer; CLAUDE.md rule 4 «the writer cap and the full queue: Cost gates, rule 12» → stays (a pointer already) |
| T13 | Cost gates: worker cap, fresh fix round, compaction trigger | CLAUDE.md § Rule 12 · Cost gates | coordinator; `agent_budget.py` | builder-rules 16 (в) (pointer, stays); RUNBOOK (pointer, stays) |
| T14 | Session hygiene: shell cwd, connectors, context compaction | CLAUDE.md hygiene pt. 3 (cwd refusal) + PROJECT § Сессия форджа (new heading: why/recovery of cwd, connectors, compaction) | every session | PROJECT «Прогоны и эксперименты» three bullets → K2 into § Сессия форджа; CLAUDE.md § Rule 12 compaction clause → pointer (F8 translated row) |
| T15 | Command hygiene (canonical tests, edits, journal writes, claims, probes) | CLAUDE.md § Command hygiene (split at pt. 6, pt. 7) | every session | builder.md 6, critic.md 11 (pointers, stay); scout.md 4 (role consequence: Grep only, stays) |
| T16 | Fix the class; sweep the artifact | CLAUDE.md § Rule 9 | coordinator owns; workers report | builder.md 5, critic.md 5, scout.md 8 (role consequences, stay); SYSTEM_PROMPT.md pointer (stays) |
| T17 | Mechanisms: four questions, axis block, tier line, package paragraph | CLAUDE.md § Rule 10 (+ § Rule 10 · a change to the package) | Lead executes | designer.md rule 1 last sentence (role consequence, stays); builder-rules 19 (role practice, stays); boot-diet 7 (pointer, stays) |
| T18 | Piles and batches: take, freeze, zones, backlog freeze, one writer, owner's word, doors, close | PROJECT «Командная работа» (discipline items) + `docs/TEAMWORK.md` (gated mechanics, F2) | integrator / coordinator; `piles.py` gates | CLAUDE.md rule 4a «the rule text is PROJECT.md «Командная работа»» (pointer, stays); critic-diff-brief question 4 «Остатки» line form (critic consequence, stays) |
| T19 | «Бэклог» — what the owner's word means; findings | PROJECT § Бэклог и находки (new heading) | every session (the owner says «отметь в бэклоге») | PROJECT «Как принимается» п. 4 → numbered pointer line |
| T20 | Owner's principles P1–P31 | `docs/OWNER_PRINCIPLES.md` (full) + a generated index in the boot (F3) | the index routes; the text is read by package work | PROJECT § Принципы владельца → intro + pointer; critic.md:165, designer.md:87, `tools/language_sites.py:106` cite «PROJECT.md P31» (resolve in 2 hops, unchanged) |
| T21 | Package change acceptance | PROJECT § Как принимается изменение пакета (п. 1, 3, 5, 6) | Lead / builder / critic | CLAUDE.md § Rule 10 · a change to the package (stays: AR-n and judgment gate, a different topic) |
| T22 | A new idea of the owner | PROJECT § Как разрабатывается новая идея владельца | Lead executes | none |
| T23 | Release | `docs/RUNBOOK.md` §4.1 Шаги релиза (new sub-heading, F7) | release session only | PROJECT § Релиз → one pointer line |
| T24 | Language | PROJECT § Язык | every session | builder-rules 3 (pointer after FG7-50) |
| T25 | What to decide vs ask; owner away | PROJECT § Что решать самому + CLAUDE.md § Rule 11a (upward routing) | two distinct topics already cross-pointed (PROJECT:402 cites 11a) | none |
| T26 | Links in answers | PROJECT § Ссылки на файлы в ответах | every session | none |
| T27 | Hand-back form per role | `.claude/agents/<role>.md` (builder 7, critic 16-17, designer 5, scout 9-10) | owner keys Q9 | builder-rules 11, critic-diff-brief «What comes back» (pointers, stay) |
| T28 | Readers of every touched file (designer duty) | `.claude/agents/designer.md` new rule 7 (K2 out of rule 3) | designer executes | none |
| T29 | Boot diet procedure | `.claude/skills/boot-diet/SKILL.md` | procedure owner (Q15) | §6's standing rule points to it |
| T30 | How rule text for agents is written | PROJECT § Как пишутся правила для агентов (new, F12) | anyone editing | none |
| T31 | Session start/end | `PROCESS/SESSION_PROTOCOL.md` | Lead | BOOT.md (sequence, stays) |
| T32 | Degradation, Role ≠ tier | CLAUDE.md § Role ≠ tier, § Lead degradation (names may change with the architect-tier spec) | coordinator | critic.md rule 9 (role consequence, stays) |

Empty-topic rule: a topic with no home yet gets the row `home: none — queued <node>`, never an invented home. None found in the
14 files.

---

## 3. Inventory «rule: was where → is where»

Rule numbers stay stable: every «CLAUDE.md rule N», «hygiene point N», «R11-f», «pt.6 b», «PROJECT «Командная работа» п. N»,
««Как принимается» п. N», «P<n>» keeps resolving in at most two hops (E1–E3). No number is moved, reused or deleted. Kinds K1–K5:
§1.2. «stays» = K1 only (a heading may be added above).

### 3.1 CLAUDE.md (446 lines; line numbers from Q7)

| ID | Was (line, opener) | Is where | Kind |
|---|---|---|---|
| C0 | 1-19 title, purpose, `@PROJECT.md`, `@docs/FACTORY_RULES_INDEX.md`, `@docs/ARCHITECTURE_INDEX.md` | stays; § Contents inserted after line 6 (§4); `@docs/OWNER_PRINCIPLES_INDEX.md` added after the FR/AR imports if F3=a | K1 (+ import line) |
| C-T | 21 «## Tiers» | stays by name (content: architect-tier spec) | K1 |
| C1 | 37 «1. Recon → scout by default» + two-pass + trail-based acceptance; R1 a (48), R1 b (49) | stays; heading «### Rule 1 — Recon → scout» | K1 |
| C2a | 51 «2. Implementation from a finished spec → builder» — witness rule, UI witness, enforcement-file rule | stays; heading «### Rule 2 — Implementation, the witness, enforcement files» | K1 |
| C2b | rule 2 «DRAFTING → designer BY DEFAULT» … resubmission, new task_id, decomposable parts | stays; sub-heading «### Rule 2 · drafting → designer» | K1 |
| C3 | 70 «3. critic — a MANDATORY acceptance gate» — two-layer entry, empirics, critic-on-plan | stays; heading «### Rule 3 — The critic gate» | K1 |
| C4a | 87 «4. Independent parts → several parallel subagents» — owns overlap, parallel sessions, cross-deployment queue | stays; heading «### Rule 4 — Parallel work» | K1 |
| C4b | rule 4 «SCOPE OF THE WITNESS RUN» … BATCH CANON … `defect_found` | stays (dispatcher + coordinator duty); sub-heading «### Rule 4 · witness scope and the BATCH CANON» | K1 |
| C4c | 103 «4a. A task spanning 5 or more journal events» + «Team work in piles and batches» | stays; heading «### Rule 4a — Task DAG; team work» | K1 |
| C5 | 107 «5. Flat delegation» | stays; heading «### Rule 5 — Flat delegation» | K1 |
| C6 | 109 «6. Escalation» (+ D-0046 line from FG7-50) | stays; heading «### Rule 6 — Escalation and rejections» | K1 |
| C7 | 115 «7. Background execution by default» — label, tier measurement | stays; heading «### Rule 7 — Background; the tier label» | K1 |
| C8 | 125 «8. Universal skip rule» — small-work batching, operator-waiting, deterministic runs | stays; heading «### Rule 8 — Skips and small-work batching» | K1 |
| C9 | 140 «9. Fix the class» + sweep-the-artifact-first | stays; heading «### Rule 9 — Fix the class» | K1 |
| C10a | 156 «10. Four questions for every mechanism» — gate, tier line, recognition | stays; heading «### Rule 10 — Four questions for a mechanism» | K1 |
| C10b | rule 10 «A change to the package (D-0055, D-0060; P27)» | stays; sub-heading «### Rule 10 · a change to the package» | K1 |
| C11a | 187 «11. DoD in every dispatch» — edge behavior, (i) TEMPORAL, (ii) POSITIONAL | stays; heading «### Rule 11 — DoD and edges» (F1) | K1 |
| C11b | rule 11 «Which tests a DoD asks for» … quarantine alert | stays; sub-heading «### Rule 11 · which tests a DoD asks for» | K1 |
| C11c | rule 11 «scout: …», «critic: …», «CONTEXT MANIFEST» … returned as questions | stays; sub-heading «### Rule 11 · scout and critic DoD; the context manifest» | K1 |
| C11d | rule 11 «FIVE-POINT CHECKLIST» (1)-(5), inline DoD, «DOC-DISPATCH WITNESS» (i)-(iii), emergency net | stays; sub-heading «### Rule 11 · the dispatcher's checklist; doc-dispatch witness» | K1 |
| C11e | R11 table m (235), f (236), h (237) | stays; sub-heading «### Rule 11 · table R11» | K1 |
| C11f | 239 «11a. Question routing» | stays; heading «### Rule 11a — Questions route up» | K1 |
| C12a | 250 «12. The coordinator's cadence» — batch acceptance, one question, what code does (`journal_write.py`, `dispatch_new.py`, `wave.py merge`, `ci_read.py why`), boot-diet, ~15 turns | stays; heading «### Rule 12 — Cadence; what code does» | K1 |
| C12b | rule 12 «Cost gates (D-0035, …)» — fresh fix round, `agent_budget` caps, one critic pass, compaction, journal notes, writers cap, push before worktree | stays (anchor COST, Q9:31); sub-heading «### Rule 12 · Cost gates»; the writers clause (text after FG7-50) → pointer «six writers: PROJECT.md «Командная работа» п. 12» (K4 — the home holds the owner's 16.11 text); the compaction clause «the Lead compacts at ~300K at a stage boundary» → pointer to PROJECT § Сессия форджа with «на границе стадии» carried there (F8 translated row TR1) | K1, K4 |
| C13 | 264 «13. Leaf routing» + R13 g (270) | stays; heading «### Rule 13 — Leaf routing (not used)» | K1 |
| C-RL1 | 272 «## Routing log» — one file per developer, one writer, accomplished facts, `worker_ref`, open-dispatch reconciliation, `closes:` token, `order-known:` token | stays; sub-heading «### Routing log · the writer and the facts» | K1 |
| C-RL2 | Routing log — five base fields, `ts` form, `model` field mandatory, `by` bare tier word vs free `model`, validator at two points, event list | stays (F5=a) | K1 |
| C-RL3 | Routing log — task identity `<id>@<label>`, `--merge-parent`; typed-fields rule + `feature: Fnn`; id issuance, clone letters, bands, collisions; `ts` from the clock and late notes; RETRO pair | → `docs/JOURNAL.md` (F5=a), pointer «rare events (identity, ids, letters, collisions, retro): `docs/JOURNAL.md`» | K2, K3 |
| C-RL4 | Routing log — Event SHAPES table (7 rows) | stays (F5=a) / → `docs/JOURNAL.md` (F5=b) | K1 / K2 |
| C-RT | 350 «## Role ≠ tier» — three definitions, acceptance from above, matrix | stays by name (content: architect-tier spec) | K1 |
| C-LD | 381 «## Lead degradation» 1-4, 4 a/b/c | stays by name (content: architect-tier spec) | K1 |
| C-H0 | 403 «## Command hygiene» intro, doors | stays | — |
| C-H1..5 | 409 «1. Tests», 412 «2. The proxy server», 413 «3. The shell's working directory», 414 «4. File edits», 417 «5. Log entries» | stay under «### Command hygiene · points 1-5»; pt. 3 gains one pointer line «why and how to recover: PROJECT.md § Сессия форджа» | K1, K3 |
| C-H6 | 420 «6. An environment-negative claim» + table pt.6 a (438), b (439), c (440) | stays; sub-heading «### Command hygiene · point 6 — a claim needs a measurement» | K1 |
| C-H7 | 442 «7. Temporary corruption» (a)-(d) | stays; sub-heading «### Command hygiene · point 7 — probes» | K1 |

Count: 13 numbered rules + 4a + 11a, 3 tables (R1, R11, R13) + pt.6 table, 4 unnumbered sections, hygiene 1-7 — every one has a row.

### 3.2 PROJECT.md (422 lines; line numbers from Q8)

| ID | Was (line, opener) | Is where | Kind |
|---|---|---|---|
| P-0 | 1-16 two rule sets; where history lives | stays; § Оглавление after line 16 (§4) | K1 |
| P-W | 18 «## Где что лежит» table | stays; +rows `docs/OWNER_PRINCIPLES.md`, `docs/TEAMWORK.md`, `docs/JOURNAL.md` (only those the forks create) | K1 (+rows) |
| P-PI | 36-40 principles intro «Они же стоят правилами FR-47…FR-57…» | stays + pointer «полный текст P1–P31: `docs/OWNER_PRINCIPLES.md`; индекс — импорт `docs/OWNER_PRINCIPLES_INDEX.md`» (F3=a) | K3 |
| P1…P31 | 41-175, `- **P<n>.**` bullets (31 rows: P1 41, P2 43, P3 44, P4 46, P5 47, P6 55, P7 56, P8 57, P9 59, P10 60, P11 61, P12 62, P13 63, P14 64, P15 65, P16 67, P17 72, P18 79, P19 86, P20 93, P21 100, P22 108, P23 121, P24 127, P25 132, P26 136, P27 150, P28 160, P29 165, P30 169, P31 173) | each → `docs/OWNER_PRINCIPLES.md`, same id, verbatim, one `### P<n>` heading per principle whose text is the first sentence verbatim (F3=a/b); F3=c: stays, grouped under sub-headings «Код и роль» P1-P3, P6, P11-P12, P14-P15, P27; «Данные» P4-P5, P9, P13; «Тесты и кейсы» P16-P17, P19-P20, P28-P30; «Доставка и отчёт» P18, P21-P24, P26; «Хост и модели» P7, P25; «Единообразие» P10, P31; «Эксперименты» P8 | K2 (F3=a/b) / K1 (F3=c) |
| PA1 | 178 «1. **Проход по правилам фабрики.**» | stays; heading «### Пакет · п. 1 проход по FR» optional — the section is 58 lines: split into «Пакет: проход и свидетель» (п. 1-2) and «Пакет: доказанность, эталон, смысл» (п. 3-6) | K1 |
| PA2 | 187 «2. **Свидетель билдера**» (24 lines) | number stays: «2. **Свидетель билдера** — правило: `plans/builder-rules.md` п. 7b (объём проверки билдера, канон пачки), `docs/TESTING.md` (какие тесты), `docs/tasks/critic-diff-brief.md` («The two layers»), `docs/RUNBOOK.md` §7 (CI, канон, запасной путь)» — keeps both pinned strings (Q10). Clauses not already in a home move K2: «Интегратор перед коммитом гоняет только свидетелей узлов и `--limits --lang`; после пуша читает пайплайн, красный пайплайн на `main` … — находка в `findings/` своей кучки и починка до следующего пуша» → RUNBOOK §7 after «Прогнать ветку»; «Локальный прогон и локальный докер — только запасной путь …, только по слову владельца и никогда не параллельно с другим; когда лог CI не читается — сначала сказать об этом владельцу» → RUNBOOK §7 «Что остаётся локально» (F9 decides the joint wording); «Полный `selftest.py` и `install_smoke.py` на машине владельца не гоняются» → already builder-rules 7 after FG7-50 (K4); quarantine sentences → TESTING «Карантин» holds them (K4); «Тесты идут в CI…, медленный файл… локально не запускается» → builder-rules 7b holds them after R2 (K4); «Задача на один инструмент в `tools/`…» → builder-rules 7b canon list «`pytest tools/` целиком» (K4) | K3, K2, K4 |
| PA3 | 211 «3. **Доказанность.**» | stays | K1 |
| PA4 | 213 «4. **Бэклог.**» | number stays as pointer «4. **Бэклог.** — правило: § Бэклог и находки»; text K2 into the new PROJECT section «## Бэклог и находки» (inside the boot) | K2, K3 |
| PA5 | 218 «5. **Шаг, переведённый из роли в код…**» | stays | K1 |
| PA6 | 224 «6. **Спека, меняющая смысл…**» (а)-(г) | stays | K1 |
| PN | 235-254 «Как разрабатывается новая идея владельца» intro, п. 1-8, detector | stays | — |
| PR1 | 256 «Прогоны и эксперименты»: «Фабрика гоняется не здесь…» | stays | — |
| PR2 | «В этом репозитории плагин qa-factory выключен» | stays | — |
| PR3 | «Сравнительный прогон…» | stays | — |
| PR4 | «Как запустить прогон фабрики в фоне… RUNBOOK §9» | stays | — |
| PR5 | «**Рабочий каталог шелла не меняется никогда**…» | → new «## Сессия форджа: каталог шелла, коннекторы, сжатие контекста» (K2); the sentence restating the refusal stays the CLAUDE.md hygiene pt. 3 rule (K4 only for the words «не меняется никогда — ни `cd`…» if the critic finds them a pure restatement; recommended: keep the bullet whole, it adds PowerShell detail and the recovery step) | K2 |
| PR6 | «**Коннекторы выключены**…» | → § Сессия форджа | K2 |
| PR7 | «**Сжатие контекста ничего не останавливает**…» | → § Сессия форджа, + «на границе стадии» (TR1) | K2 (+TR1) |
| PT0 | 279-284 «Командная работа» intro | stays | — |
| PT1 | 285 «1. **Пачку берёт один разработчик**» | stays (who merges: already coordinator via `wave.py merge`) | — |
| PT2 | 289 «2. **Взятая пачка заморожена**» (+ D-0044 finding-in-batch, «Содержание» row, class not rule) | F2=b/c: number stays as «2. **Взятая пачка заморожена** — правило: `docs/TEAMWORK.md` § 2»; text K2 | K2, K3 (F2=b/c) |
| PT3 | 303 «3. **Зоны файлов пачек…**» | F2=b/c: as PT2 | K2, K3 |
| PT4 | 309 «4. **`plans/BACKLOG.md` заморожен**» | F2=b/c: as PT2 | K2, K3 |
| PT5 | 312 «5. **Общие файлы — один писатель**» | stays (discipline; every session); its journal clause → pointer to CLAUDE.md § Routing log (K4) | K4 |
| PT6 | 318 «6. **Слово владельца — только от владельца**» | stays (discipline) | — |
| PT7 | 323 «7. **Доски нет**» | stays (one line) | — |
| PT8 | 325 «8. **Двери**» | F2=b/c: as PT2 | K2, K3 |
| PT9 | 326 «9. **Пачка закрывается доделкой…**» (+ «Живые доказательства», live runs) | F2=b/c: as PT2 | K2, K3 |
| PT10 | 342 «10. **Знание — в проекте…**» | stays (discipline) | — |
| PT11 | 346 «11. **Узел пачки пишется для более слабой модели**» | stays (discipline) | — |
| PT12 | 353 «12. **Темп координатора**» | stays; text replaced by the owner's 16.11 wording (R1); «Критик кода — один на тему» → pointer to CLAUDE.md § Rule 3 / R13 g (K4) | K5, K4 |
| PT13 | 361 «13. **Проверки билдера**» | number stays as «13. **Проверки билдера** — правило: `plans/builder-rules.md` п. 7b» (K4: 7b holds every clause, incl. «мутации судит канон», «CI не запускает и не ждёт» after FG7-50) | K4, K3 |
| PT-check | «Проверка на пути исполнения: `tools/piles.py check --msg-file`…» | moves with PT2 (F2=b/c), else stays | K2 |
| PRel | 371-379 «## Релиз» (fingerprint step, publish, release-check, CHANGELOG assembly) | F7=a: → `docs/RUNBOOK.md` «### 4.1 Шаги релиза»; PROJECT keeps «## Релиз — правило: `docs/RUNBOOK.md` §4.1» | K2, K3 |
| PL | 381 «## Язык» 3 bullets | stays | — |
| PD | 393 «## Что решать самому…» + owner away | stays | — |
| PS | 407 «## Ссылки на файлы в ответах» | stays | — |

Count: P1-P31, «Как принимается» 1-6, «Новая идея» 1-8, «Командная работа» 1-13, 6 bullets of «Прогоны», the unnumbered
sections — every one has a row.

### 3.3 Resolutions (K5 — the ONLY meaning changes; each needs its carrier, fork F10)

| R | Contradiction (carriers) | Resolution in the home | Places aligned |
|---|---|---|---|
| R1 | six writers: PROJECT п. 12 «в работе всегда шесть пишущих билдеров … меньше шести — только по слову владельца» vs CLAUDE.md rule 12 cap wording | PROJECT п. 12 carries the owner's 16.11 words in meaning: «цель держать 6 пишущих (если не сказано в этой сессии иного) и не меньше, если есть параллельная работа (цель сессии + П1 из бэклога). Можно запустить 7, если координатору надо, например упал CI и его надо починить. 6 — это цель, но не ценой ущерба эффективности (например, решать мерж-конфликты будет дороже, так что запустить в параллельность сейчас нечего)» | CLAUDE.md § Rule 12 · Cost gates → pointer; OWNER_KEYS `cost:queue` key re-quoted from the new text (Q10); `dispatch_gate.PARALLEL_CAP = 6` unchanged (Q17) |
| R2 | witness duration: builder-rules 7b «до минуты каждый» (after FG7-50) / «~5 минут» (Q19), 7c «меньше минуты каждый», PROJECT п. 2 «до минуты каждый» | no minutes number in the builder's rule: the criterion is the slow list — `SLOW_TESTS` and the named slow files (`test_story_run_*`, `test_controller_*`, `test_fixes_13797`, `test_story_step.py`) are never run locally | builder-rules 7b, 7c; PROJECT п. 2 becomes a pointer (PA2); TESTING.md «10 с на новый файл» is a different rule (file budget) and stays |
| R3 | who merges: builder-rules 2 «Мерджи, пуши, переключение веток — только интегратор»; 7b «интегратор делает один прогон BATCH CANON» vs «его запускает координатор» (7b:48) and CLAUDE.md rule 4 «the coordinator's duty» | merges and the canon: the coordinator (`tools/wave.py merge`; canon per RUNBOOK §7); the integrator closes the batch (`piles.py close`) | builder-rules 2, 7b |
| R4 | language: «весь репозиторий на английском» (builder-rules 3, fixed by FG7-50) vs PROJECT «Язык» | PROJECT «Язык» unchanged: the package, `kb/` and everything that reaches the release repo are English; forge working docs may be Russian | none left after FG7-50 |

A fifth contradiction found by this draft (not in the brief) is fork F9: PROJECT п. 2 «локальный прогон … только по слову
владельца и никогда не параллельно» vs RUNBOOK §7:115-116 «только когда CI недоступен или красный по причине раннера».

---

## 4. The table of contents

### 4.1 Form (F4 = a, recommended)
CLAUDE.md, right after the title paragraph (after line 6, before «The project's own rules…»), a CROSS-FILE topic map — the only
one in the repository:

```
## Contents — topic → where to read

| Topic | Where |
|---|---|
| Tiers | CLAUDE.md § Tiers |
| Recon → scout | CLAUDE.md § Rule 1 |
| What a builder may run | plans/builder-rules.md § 7b |
| ...one row per T1–T32 of the topic map... |
```

Cell grammar (the FG7-52 contract, §4.3): `<file> § <heading text>` or `<file> § <number>` for a numbered item; several homes
joined by ` + `. A row carries the TOPIC NAME only — never a rule sentence (E10).

PROJECT.md, after its intro (line 16): `## Оглавление` — its OWN sections only, `| Раздел | О чём (≤ 8 слов) |`, plus the row
«Все темы → CLAUDE.md § Contents».

### 4.2 Byte cost (est.)
CLAUDE.md: 32 rows × ~75 B + header ≈ 2.6 KB. PROJECT.md: ~14 rows × ~100 B (Cyrillic) ≈ 1.4 KB. Headings added (§3): ~28 in
CLAUDE.md × ~50 B ≈ 1.4 KB; ~6 in PROJECT.md ≈ 0.4 KB.

### 4.3 How it stays true — the contract for FG7-52 (owner: data, code)
1. Every cell of both TOCs, and every pointer line `rule: <file> § <x>` / `правило: <файл> § <x>` in the scanned files: `<file>`
   exists; `<x>` equals the text of a heading of `<file>` (after the `#` marks, whitespace squashed), or `<x>` is a number/id and
   a line of `<file>` starts with `<x>.` (or `### <x>` / `**<x>.**` / `- **<x>.**`).
2. A numbered pointer line («N. **<title>** — правило: …») — its `<title>` equals the bold opener of item N in the target.
3. A refusal names carrier file:line, the pointer, and the nearest existing heading in the target (FR-1, FR-2).
4. Error direction: a pointer that cannot be resolved is RED, never skipped (FR-59). Adversarial inputs that must stay red: a
   heading renamed by one character; a heading present only inside a code fence; a target file renamed; a `§` cell pointing to a
   heading of ANOTHER file of the same name; a numbered item deleted while its number is cited.
5. Until FG7-52 lands (fork F16 = a, recommended): every TOC row is a POINTERS row of `tools/tests/test_role_carriers_one_owner.py`
   (`(carrier, cell text, target, heading line)`) — the existing checker, a table row, no new file.

---

## 5. What leaves the boot, and the budget

### 5.1 The criterion (proposed, fork F2/F3)
A text leaves the boot when EITHER (i) a gate on the execution path refuses its violation and the refusal names the door (the rule
is met when it bites — `piles.py check`, `close`, `journal_write.py`), OR (ii) it is read only by one role or at one moment that
already loads a carrier (package work loads `factory-rules.md` whole; a release session runs RUNBOOK §4). A discipline-only rule
that every session must obey stays. Rationale and its risk: boot-diet step 6 «policy that isn't auto-loaded gets silently
skipped» (Q15) — hence criterion (i) demands a gate, and the owner decides the list (F2, F3, F5, F7).

### 5.2 Moves and the resulting budget (est.; averages: CLAUDE.md 43476/446 = 97.5 B/line, PROJECT.md 62252/422 = 147.5 B/line)

| Move | Fork | Δ boot (est.) |
|---|---|---|
| P1–P31 → `docs/OWNER_PRINCIPLES.md`; generated index (31 lines ≈ 4.5 KB) imported | F3=a | −19.8 + 4.5 = −15.3 KB |
| «Командная работа» gated items п. 2, 3, 4, 8, 9 + check line → `docs/TEAMWORK.md`; п. 13 → pointer | F2=b | −7.4 + 0.9 = −6.5 KB |
| — or the whole section → `docs/TEAMWORK.md`, 13 pointer lines | F2=c | −13.4 + 2.0 = −11.4 KB |
| «Как принимается» п. 2 → pointer line | — | −3.5 + 0.5 = −3.0 KB |
| «Релиз» → RUNBOOK §4.1 | F7=a | −2.2 KB |
| Routing log rare-event detail → `docs/JOURNAL.md` | F5=a | −3.5 KB |
| — plus the SHAPES table | F5=b | −5.5 KB |
| TOCs + headings (§4.2) | — | +5.8 KB |

| Scenario | Total (est.) | vs WARN 108000 |
|---|---|---|
| Recommended: F2=b, F3=a, F5=a, F7=a | 123.9 − 15.3 − 6.5 − 3.0 − 2.2 − 3.5 + 5.8 ≈ **99.2 KB** | ~8.8 KB headroom |
| F3=c (principles stay), rest recommended | ≈ 114.5 KB | over WARN, under BREACH |
| Maximal: F2=c, F3=a, F5=b, F7=a | ≈ 92.3 KB | ~15.7 KB headroom |

Per file after the recommended scenario (est.): CLAUDE.md ≈ 43.5 − 3.5 + 4.0 = 44.0 KB (under its own WARN 47800); PROJECT.md ≈
62.3 − 19.8 − 6.5 − 3.0 − 2.2 + 1.8 = 32.6 KB; `docs/OWNER_PRINCIPLES_INDEX.md` ≈ 4.5 KB; FR 5.6, AR 2.7, DECISIONS 7.5,
CURRENT_CONTEXT 1.8, SYSTEM_PROMPT 0.6. The measured figure (command in the header) replaces these in each stream's witness.

### 5.3 What each kind of session reads afterwards
- Every session, workers included (Q6): CLAUDE.md + its imports (PROJECT.md, FR index, AR index, P index). The coordinator also
  gets Layer A (SYSTEM_PROMPT.md, DECISIONS.md) and reads CURRENT_CONTEXT.md (BOOT.md:14-27).
- Coordinator, on the topic: `docs/TEAMWORK.md` (take, freeze, zones, close, findings into batches — and whenever a `piles.py`
  refusal names it), `docs/JOURNAL.md` (a validator refusal, a retro pair, a collision), `docs/RUNBOOK.md` §7 (CI, merge, canon),
  §4.1 (release), `docs/OWNER_PRINCIPLES.md` (steering package work; a P cited in a verdict).
- builder: + `.claude/agents/builder.md`, the dispatch, `plans/builder-rules.md`; `docs/TESTING.md` before the first test;
  package work: `design/factory-rules.md` whole (PROJECT «Как принимается» п. 1, unchanged).
- critic: + `critic.md`, `docs/tasks/critic-diff-brief.md`, the spec/DoD under review.
- designer: + `designer.md`, `docs/TESTING.md` (DoD), builder-rules 7b; package: `design/architecture.md`.
- scout: + `scout.md`, `docs/tasks/exchange-form.md`.

---

## 6. Writing form for agent-read rule text (becomes a standing rule; home: F12)

Draft text (Russian, for PROJECT.md § Как пишутся правила для агентов, ≈ 1 KB):

1. Одна тема — один дом (файл и раздел). В любом другом месте — строка-указатель `правило: <файл> § <раздел>` и, если роли
   нужно, одна фраза о том, что делает ЭТА роль, когда правило срабатывает. Пересказ правила вне дома — дефект.
2. Один заголовок — одна тема; раздел не длиннее ~40 строк (таблица — одной строкой счёта не считается дефектом); правило,
   спрятанное в чужой теме, получает свой заголовок.
3. Одно правило — один пункт списка или строка таблицы: что делать, кто сказал (слово владельца с датой или D-nnnn).
4. История, пример, разбор, замер — не в бут: в спеку, находку, пачку или `docs/*_FULL.md`; в правиле — ссылка.
5. Номера правил не переиспользуются и не сдвигаются: переехавший пункт оставляет на своём номере строку-указатель с тем же
   жирным заголовком.
6. Импорт `@` — только из `CLAUDE.md`, один уровень (счётчик бюджета вложенных не видит).
7. Как сокращать бут — `.claude/skills/boot-diet/SKILL.md`; оглавление и указатели проверяет код (FG7-52).

---

## 7. Phases, streams, readers

### 7.1 Order
- Phase 0 (Lead): forks decided; FG7-50 merged; the architect-tier spec merged (its headings are read then — E17); no open
  branch owns CLAUDE.md, PROJECT.md, `.claude/agents/`, builder-rules, RUNBOOK, TESTING, critic-diff-brief (`git -C
  C:/QAFactory/forge-repo worktree list` + each worktree's `git -C <wt> diff --stat origin/main`; `python -B
  C:/QAFactory/forge-repo/tools/piles.py check --all` zones).
- Phase 1 (parallel, disjoint owns): S3 (role files and worker docs), S4 (index generator; only if F3=a).
- Phase 2: S2 (PROJECT side) — after S3 and S4 merge (S2 runs S4's generator; S2's pointers target S3's headings).
- Phase 3: S1 (CLAUDE side + the cross-file TOC) — last, because its TOC cells name the final headings of every file.
- Queue line for the batch file: `очередь: S3, S4 → S2 → S1`.

### 7.2 Streams (header lines for each builder dispatch; `designer:` = this file once accepted)

**S3 — role files and worker docs**
- owns: `C:/QAFactory/forge-repo/.claude/agents/designer.md`, `C:/QAFactory/forge-repo/.claude/agents/builder.md`,
  `C:/QAFactory/forge-repo/plans/builder-rules.md`, `C:/QAFactory/forge-repo/docs/TESTING.md`,
  `C:/QAFactory/forge-repo/docs/tasks/critic-diff-brief.md`
- does: designer.md — «READERS OF EVERY TOUCHED FILE» paragraph K2 out of rule 3 into a NEW rule 7 appended at the end (numbers 1-6
  unchanged; install-parity anchors are rule openers 1-5, Q11); builder-rules — a heading per point (`### <n>` line above each
  opener, the opener lines byte-identical, «7b. **Уровень билдера и уровень пачки**» kept, Q10), R2, R3, 7b canon paragraph → pointer
  to RUNBOOK §7 except «what canon covers», 7d per F14; TESTING.md and critic-diff-brief — the restated builder-run lists → pointer
  to builder-rules 7b (K4).
- non-goals: CLAUDE.md, PROJECT.md, RUNBOOK, critic.md and scout.md bodies, any test file (a needed POINTERS/OWNER_KEYS change goes
  to «Needed from integration» for S2).
- witness: `python -m pytest tools/tests/test_role_carriers_one_owner.py tools/test_handoff_rule_anchors.py -q`;
  `python -B C:/QAFactory/forge-repo/tools/install_parity.py --check`; `python -B C:/QAFactory/forge-repo/tools/agents_md.py --check`
  (stale → regenerate only if the roles section changed, E13); DOC-DISPATCH run §7.4 over S3's rows.
- Lead places: `.claude/agents/*.md` are mechanism paths (Q13) — committed by the Lead with the axis block and `tier:` line.

**S4 — the principles index generator (only if F3=a)**
- owns: `C:/QAFactory/forge-repo/tools/factory_rules_index.py`, `C:/QAFactory/forge-repo/tools/test_factory_rules_index.py`,
  `C:/QAFactory/forge-repo/.githooks/pre-commit` (one `--check` line), `C:/QAFactory/forge-repo/.github/workflows/forge-check.yml`
  (one `--check` line)
- does: a second source row (source `docs/OWNER_PRINCIPLES.md`, out `docs/OWNER_PRINCIPLES_INDEX.md`, opener `### P<n>` heading,
  header text) read from a data table inside the same tool — one road for generated indexes (P31, AR-15 by analogy); the existing
  FR output byte-identical. Cases are rows of the existing test table.
- edges: source absent (before S2 creates it) → `--check` for that row prints `skip: <path> absent` and exits 0 ONLY while the out
  file is also absent; out present and source absent → exit 2 naming both (TEMPORAL: both worlds; S2's commit creates both).
- witness: `python -m pytest tools/test_factory_rules_index.py -q`; `python -B C:/QAFactory/forge-repo/tools/factory_rules_index.py --check`.
- Lead places: `tools/factory_rules_index.py`, `.githooks/` are mechanism paths.

**S2 — PROJECT side**
- owns: `C:/QAFactory/forge-repo/PROJECT.md`, `C:/QAFactory/forge-repo/docs/OWNER_PRINCIPLES.md` (new),
  `C:/QAFactory/forge-repo/docs/OWNER_PRINCIPLES_INDEX.md` (new, generated), `C:/QAFactory/forge-repo/docs/TEAMWORK.md` (new, F2=b/c),
  `C:/QAFactory/forge-repo/docs/RUNBOOK.md`, `C:/QAFactory/forge-repo/tools/tests/test_role_carriers_one_owner.py`,
  `C:/QAFactory/forge-repo/tools/test_session_context.py` (the one row at :1188), `C:/QAFactory/forge-repo/CLAUDE.md` (ONE line: the
  `@docs/OWNER_PRINCIPLES_INDEX.md` import), `C:/QAFactory/forge-repo/AGENTS.md` (regenerated)
- does: §3.2 rows; R1; PROJECT TOC (§4.1); new headings § Сессия форджа, § Бэклог и находки, § Как пишутся правила для агентов
  (F12=a); OWNER_KEYS `cost:queue` re-quoted; POINTERS rows for PROJECT TOC and every numbered pointer line; S3's «Needed from
  integration» rows.
- edges: E2, E3, E7, E8, E9, E19; the P index import and the P text move land in ONE commit (no window without P in the boot).
- witness: `python -m pytest tools/tests/test_role_carriers_one_owner.py tools/test_agents_md.py -q`;
  `python -m pytest tools/test_session_context.py -q -k imports`; `python -B C:/QAFactory/forge-repo/tools/agents_md.py --check`;
  `python -B C:/QAFactory/forge-repo/tools/factory_rules_index.py --check`; `python -B C:/QAFactory/forge-repo/tools/install_parity.py --check`;
  the BOOT BUDGET line of `python -B C:/QAFactory/forge-repo/tools/session_context.py`; DOC-DISPATCH run §7.4.
- Lead places: the CLAUDE.md line; `docs/SIBLING_MAP.md` axis 31 rows for `docs/OWNER_PRINCIPLES.md`, `docs/TEAMWORK.md`
  (Q16 duty, mechanism path) in the same commit.

**S1 — CLAUDE side**
- owns: `C:/QAFactory/forge-repo/CLAUDE.md`, `C:/QAFactory/forge-repo/docs/JOURNAL.md` (new, F5=a/b),
  `C:/QAFactory/forge-repo/tools/install_parity_anchors.json`, `C:/QAFactory/forge-repo/tools/tests/test_role_carriers_one_owner.py`,
  `C:/QAFactory/forge-repo/AGENTS.md`; if F6=a also `C:/QAFactory/forge-repo/tools/mechanism_gate.py` (one prefix row
  `docs/JOURNAL.md`) and `C:/QAFactory/forge-repo/tools/test_mechanism_gate.py` (one row)
- does: §3.1 rows; the cross-file TOC; anchors that quote moved Routing log text (e.g. «ISO local time», «DEAD-WORKER
  REPLACEMENT:» if F5=b) move to a new unit `routing-journal-doc` (`host_path: docs/JOURNAL.md`, `kit_path: toolkit/docs/JOURNAL.md`,
  `kind: anchor`); POINTERS rows for every CLAUDE.md TOC cell.
- witness: `python -m pytest tools/tests/test_role_carriers_one_owner.py tools/test_agents_md.py -q`;
  `python -B C:/QAFactory/forge-repo/tools/install_parity.py --check`; `python -B C:/QAFactory/forge-repo/tools/agents_md.py --check`;
  BOOT BUDGET line; if F6=a `python -m pytest tools/test_mechanism_gate.py -q`; DOC-DISPATCH run §7.4.
- Lead places: everything (CLAUDE.md, mechanism_gate.py are mechanism paths) + SIBLING_MAP axis 31 row for `docs/JOURNAL.md`.

### 7.3 Regeneration steps (every stream that touches their sources)
`python -B C:/QAFactory/forge-repo/tools/agents_md.py --repo <worktree root>` then stage `AGENTS.md` (builder-rules 17). A conflict
in `AGENTS.md` or `docs/OWNER_PRINCIPLES_INDEX.md` at merge is resolved by regenerating, never by hand. Parity anchors: edited by
hand in S1 (no generator exists); checked by `install_parity.py --check`.

### 7.4 The DOC-DISPATCH witness (mechanical layer of INV-M)
Per stream, before the run, the DoD quotes the keys VERBATIM: for each K2 row of §3 that the stream owns, the first 60 and the
last 60 characters of the moved block, its destination path and its source path. The script (attached in full to the report,
never committed) prints per key `present-in-destination yes/no`, `absent-from-source yes/no`, and exits 1 on any `no`. Negative
control in the same run: one key deliberately altered by one character → the script reports failure. A K4 row: the key is the
home's sentence, checked `present-in-home`.

### 7.5 Readers of every touched file (rule 3; command = the Grep tool, pattern, path; counts as printed)

| Touched file | Search | Hits | Reader → verdict |
|---|---|---|---|
| CLAUDE.md | `CLAUDE\.md[`'"]?,? (rule\|routing rule\|command hygiene\|pt\.\|point)\s*\d+` -i over `tools/` | 34 in 20 files | rule-number citations in `claim_control_gate.py:99`, `dispatch_gate.py:620,710`, `dispatch_manifest.py:138,157`, `hook_liveness_probe.py:1273`, `handoff_gate.py:42`, `journal_hooks.py:40`, `journal_echo.py:1422`, `journal_write.py:58,416`, `judge_calib_sanitize.py:3`, `mechanism_gate.py:14,286`, `owns_gate.py:5`, `owns_verify.py:3,26`, `search_control_gate.py:21`, tests `test_dispatch_gate.py`, `test_dispatch_manifest.py`, `test_journal_echo_escalation.py`, `test_mechanism_gate.py`, `test_piles_take.py` → **unchanged** (numbers stable, E1) |
| CLAUDE.md | same pattern over `.claude/agents` | 4 | `designer.md:17,24,32`, `judge.md:3` → unchanged |
| CLAUDE.md | same pattern over `.claude/skills` | 8 | `permission-audit:61`, `onboarding:40,166,216`, `next-task:45,53,63`, `boot-diet:108` → unchanged |
| CLAUDE.md | `CLAUDE\.md\|PROJECT\.md` over `.githooks` | 3 (comments in pre-commit:9,24,32) | pre-commit `agents_md.py --check` (:34) → unchanged, runs on every stream's commit |
| CLAUDE.md | `["'](CLAUDE\|PROJECT)\.md["']` over `tools/*.py` | agents_md.py:31; session_context.py:193; claim_control_gate.py:253; mechanism_gate.py:212; test_role_carriers :45-72 | agents_md → regen (S1, S2); session_context → unchanged code; claim_control_gate `ROOT_FILES` → unchanged (analog A3); mechanism_gate → changes in S1 only if F6=a; test_role_carriers → changes in S2, S1 |
| CLAUDE.md | `Routing log\|SHAPES table\|Event SHAPES` over `tools/` | 3 | `journal_echo.py:1455` comment → unchanged (section name kept); `install_parity_anchors.json:68` → unchanged (heading kept); `fixtures/host_pre_delivery_CLAUDE.md:320` → unchanged (fixture) |
| CLAUDE.md (anchors) | `tools/install_parity_anchors.json` unit `routing-policy` | 89 anchors | → changes in S1 only for text moved out (C-RL3/4) |
| PROJECT.md | `PROJECT\.md` over `tools/` | 50 in 12 files | `agent_budget.py:278` «(PROJECT.md)» compaction line → unchanged (compaction stays in PROJECT.md § Сессия форджа); `install_parity_anchors.json` (anchor of CLAUDE rule 4a) → unchanged; `factory_rules_index.py` header → unchanged (S4 adds its own header); `md_regions.py:46` docstring → unchanged; `language_sites.py:106` «PROJECT.md P31» → unchanged (E3); `piles.py:2183` ««Командная работа» п. 2» → unchanged (number kept, E2); `test_quarantine.py:1805` «PROJECT.md, Teamwork, item 2» → unchanged (E2); `test_session_context.py:1188` → changes in S2 if F3=a; `test_agents_md.py` (36, synthetic repos) → unchanged; `test_role_carriers` (3) → changes in S2; fixtures `dispatch_manifest/K4.txt`, `K8.txt` → unchanged |
| PROJECT.md | `PROJECT\.md[^\n]{0,60}(п\. ?\d+\|P\d+\|«)` over `.claude/agents` | 2 | `critic.md:165`, `designer.md:87` «PROJECT.md P31» → unchanged (E3) |
| PROJECT.md | same over `.claude/skills` | 0 (control: same pattern over `tools/` → 3) | — |
| plans/builder-rules.md | `builder-rules` over `tools/` | 24 in 11 files | `dispatch_gate.py:1866` «builder-rules item 20» → unchanged (numbers kept); `test_handoff_rule_anchors.py` (pointer of rule 11) → unchanged; `test_role_carriers` keys/anchor 7b → unchanged (openers byte-identical); `test_quarantine.py:51` FORGE_CARRIERS (purge «still named in text») → unchanged; `test_test_quarantine.py`, `test_split.py`, `test_language_sites.py:4`, fixtures K3/K4/K7 → unchanged |
| docs/RUNBOOK.md | `RUNBOOK` over `tools/` | 8 in 4 files | `dispatch_gate.py:1866,1945` «§12 item 8» → unchanged; `test_quarantine.py:490,498,1175` «section 7» → unchanged (§7 keeps its number); `test_role_carriers` pointers → unchanged (pinned strings kept) |
| role files | `PROJECT\.md\|builder-rules\|RUNBOOK\|critic-diff-brief\|TESTING\.md\|AGENTS\.md` over `.claude/agents` | 12 in 3 files | builder.md 4, critic.md 6, designer.md 2 pointers → unchanged, except designer.md rule 7 (S3) |
| role files | anchors in `install_parity_anchors.json` units `role-profiles:*` | builder 10, critic 21, designer 12, scout 12 | → unchanged (no opener moves; designer rule 7 appended) |
| docs/TESTING.md, critic-diff-brief | `test_role_carriers` BRIEF keys/anchors «## The two layers», «6. **DUPLICATION…», «7. **CODE QUALITY**», «12. **ONE ROAD**» | 7 rows | → unchanged (S3 keeps the lines) |
| skills | `PROJECT\.md\|builder-rules\|RUNBOOK\|critic-diff-brief\|TESTING\.md\|AGENTS\.md` over `.claude/skills` | 2 (boot-diet:36,38) | boot-diet step 2 list of trimmed↔full pairs → unchanged (the moves here are homes, not trimmed↔full pairs) |
| `.claude/settings.json` | `PROJECT\.md\|CLAUDE\.md\|builder-rules\|RUNBOOK` | 0 | no reader |
| tools/factory_rules_index.py | `factory_rules_index\|FACTORY_RULES_INDEX` over `tools/` + `.githooks` | 19 in 6 files + pre-commit:27 | `test_factory_rules_index.py` → changes in S4; `mechanism_gate.py` prefix → unchanged; `test_workflows.py` → unchanged unless it pins forge-check steps (S4 reads it); `test_session_context.py`, `test_agents_md.py` → unchanged |
| install_parity_anchors.json | `install_parity_anchors` over the repo (worktrees excluded) | readers `tools/install_parity.py:19,754`, `tools/test_install_parity.py:39`, `forge-check.yml:91,94` | → install_parity.py unchanged; CI runs `--check` |
| test_role_carriers_one_owner.py | pytest; CI full `pytest tools/` | — | → rows change (S2, S1) |
| AGENTS.md | `agents_md.py --check` | pre-commit:34, forge-check.yml:80 | → regenerated |
| new files (OWNER_PRINCIPLES.md, OWNER_PRINCIPLES_INDEX.md, TEAMWORK.md, JOURNAL.md) | created by this node | 0 readers before | their readers after: the TOC, pointer lines, POINTERS rows, (index) the CLAUDE.md import and S4's `--check` |

---

## 8. Edges (each with the invariant it protects)

- **E1 rule cited by number from code refusals** (e.g. `dispatch_manifest.py:138` «CLAUDE.md rule 11»). Behaviour: numbers never
  move; headings go ABOVE the opener; the opener line stays byte-identical. Invariant: every number citation (34 in tools, 4 in
  agents, 8 in skills, 44 in the calibration protocol) resolves to the same clause, in CLAUDE.md, in one hop.
- **E2 PROJECT numbered items that move** (п. 2, 3, 4, 8, 9, 13 of «Командная работа»; п. 2, 4 of «Как принимается»). Behaviour:
  the number stays in PROJECT.md as one line «N. **<bold title verbatim>** — правило: <file> § N». Invariant: «п. N» reaches the
  text in ≤ 2 hops; no number is reused for another rule.
- **E3 «PROJECT.md P<n>»**. Behaviour: PROJECT § Принципы владельца keeps the pointer; the index line «P<n> — <first sentence>» is in
  the boot. Invariant: every P id is visible in every session and reaches its text in ≤ 2 hops.
- **E4 pointer whose target section is later renamed.** Behaviour: POINTERS rows now, FG7-52 contract §4.3 later; renaming turns
  red. Invariant: a dangling pointer is never silent (the safe direction: a false red, never a false green).
- **E5 a rule that is both the coordinator's and a worker's.** Behaviour: home = the executor's file (§2 rule). Invariant: no rule
  sentence in two carriers (OWNER_KEYS), and the checker keeps its one sentence of consequence.
- **E6 worktree copies; kit twin.** Behaviour: phase 0 refuses to start while an open branch owns a touched file; a worker in an
  old worktree reads its whole old tree (consistent). No kit twin here (Q12); host-layout freshness is `install_parity.py --check`.
  Invariant: no merge re-adds a moved paragraph — a late branch that edited a moved block conflicts and the late node resolves it
  into the HOME (PROJECT «Командная работа» п. 3), re-running §7.4.
- **E7 TEMPORAL — files this node creates** (`docs/OWNER_PRINCIPLES.md`, `docs/OWNER_PRINCIPLES_INDEX.md`, `docs/TEAMWORK.md`,
  `docs/JOURNAL.md`). Before: absent, no pointer names them, the import pin lists three imports. After: present, created in the SAME
  commit that removes the text from its source and adds the pointers (and the import + pin row for the index). Invariant: no commit
  in which a rule is in no carrier, or in two.
- **E8 nested imports.** Behaviour: forbidden — imports only from CLAUDE.md, one level. Invariant: the BOOT BUDGET never reports
  fewer bytes than the session pays (Q1 vs Q4).
- **E9 BOOT.md regex.** Behaviour: new files live under `docs/` and are never named in BOOT.md as `Read NAME.md`. Invariant: the
  budget counts exactly what is loaded (`session_context.py:1057`).
- **E10 TOC rows quote nothing.** Behaviour: topic names only. Invariant: a TOC row never counts as a restatement of an OWNER_KEYS
  sentence (one-owner test).
- **E11 parity anchors of moved text.** Behaviour: moved to a new unit in the same commit. Invariant: every clause pinned before is
  pinned after, in its new carrier.
- **E12 mechanism-gate net.** Behaviour: F6. Invariant: text that leaves CLAUDE.md does not leave the gate's net; PROJECT-origin
  text keeps its current (ungated) status — this node changes no gate status (Q13).
- **E13 AGENTS.md.** Behaviour: regenerated by every stream whose sources changed; conflicts by regeneration. Invariant:
  `agents_md.py --check` green on every commit. New docs are not imported, so not in AGENTS.md — a Codex developer follows the same
  pointers as a Claude session.
- **E14 limit ~40 lines.** Behaviour: a section over ~40 lines gets a sub-heading; a single table may exceed it; over 50 lines
  without a table is a finding (F12/F13). Rule 11 (51 lines) is split by sub-headings (F1).
- **E15 empty home.** Behaviour: `home: none — queued <node>`. Invariant: no invented home.
- **E16 conflicting requirements.** (в) vs the budget: role text goes to role files only — never into the boot to «save a pointer».
  (а) vs the TOC: the TOC routes, it does not restate (E10). FG7-50's «до минуты каждый» vs R2's «no minutes number»: R2 (later
  word) wins, F10 names its carrier.
- **E17 the architect-tier spec lands first.** Behaviour: S1 reads the headings of «Tiers», «Role ≠ tier», «Lead degradation» as
  they stand after it and uses them verbatim in the TOC. Invariant: a TOC cell equals an existing heading.
- **E18 language.** Behaviour: F8. Invariant: no moved rule is paraphrased by translation without a row the critic can compare.
- **E19 OWNER_KEYS `cost:queue`.** Behaviour: R1 changes the sentence; S2 re-quotes the key from the new text in the same commit.
  Invariant: the owner keeps exactly one key, in PROJECT.md.

---

## 9. Forks (each: options, consequences, recommendation — the Lead decides; owner questions marked)

- **F1 — rule 11: split into numbered rules or keep the number with sub-headings.** (a) keep «11» and add five sub-headings
  «### Rule 11 · …» (C11a–e); (b) split into 11, 11b, 11c…; (c) split into new numbers 14+. (b)/(c) move text away from the number
  that `dispatch_manifest.py:138`, `designer.md:17`, POINTERS Q9:64 and the parity anchor «11. DoD in every dispatch» cite; every
  «rule 11» citation would need a second look. **Recommend (a)**: zero readers change.
- **F2 — PROJECT «Командная работа»** (owner question: what leaves the boot). (a) stays whole, sub-headings only (0 KB); (b) gated
  mechanics п. 2, 3, 4, 8, 9 + the check line → `docs/TEAMWORK.md` by pointer, numbers stay as pointer lines (−6.5 KB est.);
  (c) whole section → `docs/TEAMWORK.md`, 13 pointer lines (−11.4 KB); (d) `docs/TEAMWORK.md` imported from CLAUDE.md (structure
  only, 0 KB, and an extra import row in the pin). **Recommend (b)**: criterion §5.1 (i) — each moved item is refused by
  `piles.py check`/`close` with a door; discipline items (6, 10, 11, 12) stay where every session sees them. Not `plans/piles/`:
  the one-owner scan excludes it (Q9).
- **F3 — P1–P31** (owner question). (a) → `docs/OWNER_PRINCIPLES.md`, index generated by S4 (one road with the FR/AR indexes),
  imported (−15.3 KB); (b) → same file, hand-written index of first sentences checked by FG7-52 (−15 KB; a second index road);
  (c) stay, grouped sub-headings (0 KB; budget ≈ 114.5 KB, over WARN). **Recommend (a)**.
- **F4 — TOC shape.** (a) CLAUDE.md = the one cross-file topic map, PROJECT.md = own sections; (b) both full maps (two copies,
  drift); (c) both own-sections only, the topic map in SIBLING_MAP axis 31. **Recommend (a)** — the direction (б) names both files;
  only one may route across files.
- **F5 — Routing log.** (a) rare-event detail → `docs/JOURNAL.md` (−3.5 KB), SHAPES stays (the coordinator writes `accepted`/
  `rejected` daily); (b) + SHAPES (−5.5 KB; `journal_write.py` validates before writing anyway); (c) nothing moves. **Recommend (a)**.
- **F6 — mechanism-gate net for the new homes.** (a) add `docs/JOURNAL.md` (CLAUDE-origin text) to `MECHANISM_PREFIXES`; leave
  PROJECT-origin homes as PROJECT.md is today (ungated); (b) add every new home and PROJECT.md (a status change: every PROJECT.md
  commit then needs an axis block); (c) add nothing (CLAUDE-origin journal text silently leaves the net). **Recommend (a)**; (b) is a
  separate decision the Lead may queue — note the brief's premise «PROJECT.md is a mechanism path» does not hold on disk (Q13).
- **F7 — «Релиз» → RUNBOOK §4.1.** (a) move (−2.2 KB; read only by a release session, which already follows RUNBOOK §4); (b) stay.
  **Recommend (a)**.
- **F8 — language of moved text.** (a) a move stays within its language; a cross-language move is allowed only for one clause, each
  a «translated» row (TR1 «at a stage boundary» → «на границе стадии») the critic compares; (b) translate freely into the target
  file's language; (c) mixed-language sections allowed. **Recommend (a)**.
- **F9 — local fallback run (a contradiction found here; owner question).** PROJECT п. 2 «только по слову владельца и никогда не
  параллельно» vs RUNBOOK §7:115-116 «только когда CI недоступен или красный по причине раннера». (a) conjunction in RUNBOOK §7:
  both conditions; (b) RUNBOOK wins; (c) PROJECT wins. **Recommend (a)** (the strictest reading of both carriers).
- **F10 — carriers of the resolutions (Lead/owner).** R1's wording is quoted from the brief; R2 («no minutes number») contradicts
  FG7-50's own fix «дольше ~5 минут → до минуты каждый». PROJECT «Командная работа» п. 6 requires the owner's word from a session
  with the owner. (a) the Lead names the carrier (session date/line) for R1 and R2 before S2/S3 start; (b) R2 waits, S3 keeps
  FG7-50's text. **Recommend (a)**.
- **F11 — role files: import their rule home, or point to it.** (a) point (status quo, axis 31); (b) `@import` builder-rules into
  builder.md — unverified that agent files expand `@` (pt.6 a: one experiment first), and it would load ~7.5 KB into every builder
  twice-read. **Recommend (a)**.
- **F12 — home of the writing-form rule (§6) and the hardness of «~40 lines».** (a) PROJECT § Как пишутся правила для агентов
  (boot, ≈ 1 KB), ~40 a target, >50 without a table a finding for FG7-52 to WARN on; (b) a docs file by pointer; (c) a step in
  boot-diet. **Recommend (a)**.
- **F14 — builder-rules 7d vs TESTING.md.** 7d restates TESTING's «Что не пишется» table. (a) 7d → pointer + only the builder-only
  clauses TESTING lacks (role-rules register guard, `keep` row for a new script's file ≤ 10 s, quarantine file not run); (b) leave.
  **Recommend (a)**; every removed clause checked K4 «present in TESTING.md».
- **F16 — TOC check before FG7-52.** (a) POINTERS rows in the existing test (no new file; FG7-52 later absorbs them); (b) critic reads
  until FG7-52. **Recommend (a)**.

## 10. Small choices closed by the designer
- New file names `docs/OWNER_PRINCIPLES.md`, `docs/OWNER_PRINCIPLES_INDEX.md`, `docs/TEAMWORK.md`, `docs/JOURNAL.md` — under
  `docs/` (scanned by the one-owner test, not matched by the BOOT.md regex, E9).
- Heading text style: `### Rule N — <topic>` / `### Rule N · <sub-topic>` in CLAUDE.md; Russian `### <тема>` in PROJECT.md.
- designer.md readers paragraph → appended rule 7 (no renumbering).
- Parity unit name `routing-journal-doc`, kit_path convention `toolkit/<host_path>`.
- The ordering of streams (§7.1) and the AGENTS.md conflict rule (regenerate).

## 11. Analogs and contradictions noticed (reported, scope not widened)
- A1 — FG7-52's planned `tools/pointer_lint.py` would be a second pointer checker beside `test_role_carriers_one_owner.py` K-PTR
  (Q9): one road suggests FG7-52 extends the existing test's scan rather than adding a tool (P31, AR-15 by analogy).
- A2 — the brief says PROJECT.md is a mechanism path; it is not in `MECHANISM_PREFIXES` (Q13).
- A3 — `claim_control_gate.ROOT_FILES` (`tools/claim_control_gate.py:252-263`) scopes negative-claim checks to CLAUDE.md, BOOT.md, …
  but not PROJECT.md; text moving between them changes coverage. Not this node's.
- A4 — the budget counter (one level) and `agents_md.py` (five levels) read imports differently (Q1, Q4); E8 avoids the gap, the
  asymmetry itself is a sibling for SIBLING_MAP axis 13-style «one reader» work.
- A5 — builder-rules 7b is internally inconsistent on who runs the canon (integrator at :36, coordinator at :48) — R3.
- A6 — RUNBOOK §7 vs PROJECT п. 2 on the local fallback — F9.

## 12. Reading trail
Read whole: the finding; `BOOT.md`; `plans/builder-rules.md`; `.claude/agents/builder.md`, `critic.md`, `scout.md` (designer.md from
the session's role text); `CURRENT_CONTEXT.md`; `docs/tasks/critic-diff-brief.md`; `docs/TESTING.md`; `PROCESS/SESSION_PROTOCOL.md`;
`DELEGATION_TABLE.md`; `tools/install_parity_anchors.json`; `tools/tests/test_role_carriers_one_owner.py`;
`.claude/skills/boot-diet/SKILL.md`. Read in part: `tools/session_context.py:170-219, 1036-1275`; `tools/agents_md.py:1-80`;
`tools/mechanism_gate.py:211-263`; `tools/claim_control_gate.py:244-265`; `tools/test_session_context.py:1180-1193`;
`tools/test_agents_md.py:66-85`; `tools/test_install_parity.py:925-964`; `tools/factory_rules_index.py:1-60`;
`docs/RUNBOOK.md:86-175`; `docs/SIBLING_MAP.md:471-565`; `PROJECT.md:404-422`; `CLAUDE.md:440-446` (CLAUDE.md and PROJECT.md
whole as loaded into the session). Greps: as in §7.5, plus headings of CLAUDE.md, PROJECT.md, RUNBOOK, SIBLING_MAP axes,
`PARALLEL_CAP`, `subagents auto-load`, `process_ratchet_tokens` (package `role-load.json` — unaffected), the calibration protocol
rule citations (44 hits, unchanged by E1). Globs: `toolkit/*` (none) with control `tools/install_parity*.py`;
`docs/tasks/specs/20261116-*.md` (none) with control `docs/tasks/specs/2026111*-*.md` (54).
Not measured: every byte figure marked est.; the Codex/agent-file `@` behaviour (F11).

## Lead decisions on the forks (Lead, 17.11.2026) -- the plan critic reviews the spec WITH these

Decided by the Lead (each is the recommended option): F1 (a) rule 11 keeps its number, sub-headings only; F4 (a) CLAUDE.md
carries the one cross-file topic map; F5 (a) rare-event journal detail to `docs/JOURNAL.md`, SHAPES stays; F6 (a);
F7 (a) «Релиз» to RUNBOOK §4.1; F8 (a) a move stays within its language; F11 (a) point, no import; F12 (a); F14 (a);
F16 (a) POINTERS rows in the existing test. A1 accepted: FG7-52 extends the scan of
`tools/tests/test_role_carriers_one_owner.py` (K-PTR) instead of a second tool `pointer_lint.py` (P31, AR-15).

F10 carriers: R1 (six writers) -- the owner's message of 16.11.2026 evening in the Lead session (quoted in
`docs/tasks/compact-snapshots/2026-11-17-0040-narrative.md`, «Шесть пишущих»). R2 (no minutes number in the builder rule;
the criterion is the slow-file list) -- a Lead decision of 16.11.2026 told to the owner and marked «решила сама», NOT the
owner's word; it is written as the Lead's, and S3 keeps it unless the owner objects.

Asked of the owner, executable on the recommendation until her word: F2 (b) gated mechanics of «Командная работа» to
`docs/TEAMWORK.md`; F3 (a) P1-P31 to `docs/OWNER_PRINCIPLES.md` with a generated imported index; F9 (a) the local
fallback needs BOTH conditions. Streams that move text out of the boot under F2/F3 start only after the owner's word;
the streams that only add headings and the contents do not wait.
