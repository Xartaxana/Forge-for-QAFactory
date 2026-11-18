# FG7-62 — boot squeeze card (DRAFT r1, designer, t-1504)

Feature F19. Node `forge/7/FG7-62` (`plans/piles/forge/batch-7-vhodyashchie-4.md`, row FG7-62). Owner's word 18.11.2026
(brief `facts:`): squeeze the boot, no threshold raise. Procedure: `.claude/skills/boot-diet/SKILL.md` steps 1-5b.
Line numbers below are orientation only, at HEAD `e6faa917`; every span is located by its QUOTED text (E1).
SIZE (designer rule 8): estimate ~37 KB (328 lines), not measured (no shell); the Lead checks
`python -B -c "import os,sys;print(os.path.getsize(sys.argv[1]))" docs/tasks/specs/20261118-fg7-62-boot-squeeze-card.md`.

## 1. Frame

- Goal: boot total (canonical run `python -B tools/session_context.py`, line `BOOT BUDGET:`) at most 108000 bytes,
  2 KB under BOOT_WARN 110000 (`tools/session_context.py:219`), WITHOUT counting the t-1489 TEAMWORK move.
- Allowed move classes (brief non-goals): HIST (closed item, history, example, rationale -> archival home), DUP (text whose
  home already holds it -> pointer or nothing), STALE (text false against its carrier). An operational rule that would
  leave the boot is a fork (§9), never a card line.
- Not a package change: no `ai-packages/qa-factory/` path is touched; no AR-n touched; no check added or altered.
  `variety: none -- forge boot documents only; no language, project or case branch exists in a text move`.
- Mechanism paths touched (`tools/mechanism_gate.py:216-230`): CLAUDE.md, COORDINATOR.md, DECISIONS.md,
  docs/SIBLING_MAP.md -> the ONE commit is the Lead's, with `axes: not a mechanism (<reason>)` and `tier: opus` (S1).
- No `test:` lines: no item has behaviour («Пункт без поведения (перенос текста, переименование) строки не получает»,
  `docs/TESTING.md`, OWNER_KEYS `tests:line`). The witness is the existing pins + a DOC-DISPATCH key run + the budget run.

## 2. Measured table (step 1)

Boot files = BOOT.md `Read X.md` lines (SYSTEM_PROMPT, DECISIONS, CURRENT_CONTEXT) + `coordinator_rules.COORDINATOR_FILES`
(fallback copy `tools/session_context.py:257-263`: COORDINATOR, PROJECT, three indexes) + CLAUDE.md (`:1239`); no `@`
imports (K-WORKER). Read by me: `tools/session_context.py:1225-1241`, `BOOT.md` grep `Read [A-Z_]+\.md` (3 hits).

| file | bytes | source |
|---|---|---|
| COORDINATOR.md | 44213 | Lead, `facts:` (session_context.py, 18.11) |
| PROJECT.md | 35403 | Lead, `facts:` |
| CLAUDE.md | 14495 | Lead, `facts:` |
| DECISIONS.md | ~8800 | estimate, not measured (designer has no shell; char count of the Read) |
| docs/OWNER_PRINCIPLES_INDEX.md | ~6500 | estimate (31 lines, Cyrillic, cut at ~120 chars) |
| docs/FACTORY_RULES_INDEX.md | ~4800 | estimate (59 lines) |
| docs/ARCHITECTURE_INDEX.md | ~2000 | estimate (29 lines) |
| CURRENT_CONTEXT.md | ~1800 | estimate |
| SYSTEM_PROMPT.md | ~570 | estimate |
| total | 118475 | Lead, `facts:` (9 files); the six estimates sum to the measured remainder 24364 within ~2 % |

The Lead measures the six before dispatch:
`python -B -c "import os;[print(os.path.getsize(p),p) for p in ['SYSTEM_PROMPT.md','DECISIONS.md','CURRENT_CONTEXT.md','COORDINATOR.md','PROJECT.md','docs/FACTORY_RULES_INDEX.md','docs/ARCHITECTURE_INDEX.md','docs/OWNER_PRINCIPLES_INDEX.md','CLAUDE.md']]"`
and each move's span (estimate column of §3) with
`python -B -c "import sys;t=open(sys.argv[1],'rb').read().split(b'\n');a,b=int(sys.argv[2]),int(sys.argv[3]);print(sum(len(x)+1 for x in t[a-1:b]))" <file> <first> <last>`.

Baseline and cause (step 1): 109956 at the 17.11 raise to 110000 (`tools/session_context.py:216`); 117987 after card
B1 of FG7-59 (FG7-62 row); 118475 now. The growth is the worker split (COORDINATOR.md born at 44 KB with its Contents
table and topic pointers) plus the coordinator files counted in the total; no single closed item explains it.

## 3. Move list (steps 2, 3, 5, 5b)

Bytes = estimate of the net saving (removed minus the pointer left). `@`= archival home. Pins = the anchors the move
must leave intact (§5).

### Part B — builder

| id | step | class | source (file § section, quoted span) | ~B | home | pointer / replacement left | pins |
|---|---|---|---|---|---|---|---|
| C1 | 5 | DUP | COORDINATOR.md preamble :5-15, «The coordinator's routing policy of this repository» … «rule 10).» | 650 | none (CLAUDE.md:3-5, PROJECT.md:10-13, the index headers, rule 10 hold it) | text R-C1 below | SKILL step 6 cites «COORDINATOR.md's opening rationale» and SKILL:8 the boot-context-is-expensive rule: both sentences KEPT |
| C2 | 5 | DUP | COORDINATOR.md rule 3 :131-133, «critic's own zone is the VERDICT layer» … «does not execute it.» | 200 | none (critic.md rule 21 :182-195 holds every clause) | «the critic's VERDICT layer and its control re-run: `.claude/agents/critic.md` rule 21.» | anchor `TWO-LAYER CRITIC ENTRY` (same paragraph, untouched); `starts with EMPIRICS` untouched |
| C3 | 5 | DUP | COORDINATOR.md rule 4 :151-155, «SCOPE OF THE WITNESS RUN: for every writing node» … «can break a shared full run.» | 280 | none (docs/TESTING.md «Что запускать по своей правке» :94-108; OWNER_KEYS `scope:builder`) | text R-C3 below | anchors `SCOPE OF THE WITNESS RUN:`, `scenario_walk.py --witness-for <owns>`, `the BATCH CANON:`; POINTERS row (COORD, «`docs/TESTING.md` «Что запускать по своей правке»») |
| C4 | 2 | HIST (example) | COORDINATOR.md § Routing log :360-363, the ```json fence with the `delegated` example | 210 | @ docs/CLAUDE_HOST_ADAPTATIONS_FULL.md, new § (S3) | the sentence before it ends «as the witness).» instead of «as the witness):» | none (no test reads the example: grep `brief: what was delegated` over tools/, hits are journal fixtures and a role-carrier test string) |
| C5 | 2 | HIST | COORDINATOR.md § Routing log :392-393, «Bands (`id_band`) are retired for new lines and still read in old ones;» | 85 | @ same § as C4 | none; «`journal_keys.py declare` repairs only collisions already in history.» STAYS (a door) | none |
| C6 | 5 | DUP | COORDINATOR.md § Routing log :394-395, «`ts` is read from the system clock by the writer, never taken from the session's narrative;» | 95 | none (:355 «the machine lock, the clock, the validator BEFORE the write») | sentence restarts «A wrong `ts` noticed later gets a note …» | anchor `ISO local time` (:378, untouched) |
| P1 | 5 | DUP | PROJECT.md intro :14-16, «Дословные слова владельца, примеры и разборы прогонов» … «а не сюда.» | 425 | none (SKILL step 2 and «Как пишутся правила» п. 4; PROJECT.md:246 points there) | «Слова владельца, примеры и разборы — `docs/PROJECT_FULL.md` (копия 11.11.2026).» | none |
| P2 | 5b | STALE+DUP | PROJECT.md § Принципы владельца :62-66, «Они же стоят правилами» … «`COORDINATOR RULES:`.» | 170 | none («здесь — коротко» is false: the P-texts left on 11.11) | «Полный текст P1–P31 — `docs/OWNER_PRINCIPLES.md` (они же FR-47…FR-57 и правки FR-2, FR-4, FR-6, FR-13); индекс `docs/OWNER_PRINCIPLES_INDEX.md` читается по строке `COORDINATOR RULES:`.» | POINTERS row 101 needs «`docs/OWNER_PRINCIPLES.md`» (kept); pointer_lint R-range «P1–P31» on the P-home line (kept whole) |
| P6 | 5 | DUP | PROJECT.md п. 2 :84-85, «(три слоя: сценарии на артефактах настоящих прогонов, стыки данных, таблицы случаев; теста на каждую строку и мелкую функцию нет; » | 230 | none (docs/TESTING.md:43 «Что пишется — три слоя, и только они») | parenthesis becomes «(объём считает `tools/test_volume.py`)» | POINTERS rows 75, 76, 103 (`docs/TESTING.md` «Что запускать…», `.claude/agents/critic.md` rule 21, `docs/RUNBOOK.md` §7): untouched |
| P3 | 5 | DUP | PROJECT.md § Прогоны :152-153, « (копия проекта, стенд, запуск драйвера отдельным процессом, журналы, ответы на вопросы драйвера)» | 175 | none (RUNBOOK §9, the target of the bold pointer) | nothing | none |
| P8 | 2 | HIST (reason) | PROJECT.md § Сессия форджа :158-159, « — схемы неиспользуемых инструментов стоят токенов каждой сессии» | 100 | PROJECT_FULL.md:320 holds the reason | parenthesis keeps «(Gmail, Calendar, Drive, Docs)» | RUNBOOK -> «`PROJECT.md` § Сессия форджа» heading untouched |
| P4 | 5 | DUP | PROJECT.md п. 5 :189-191, «журнал — файл на разработчика» … «в истории репозитория);» | 170 | none (COORDINATOR § Routing log :353-358, CLAUDE.md hygiene 5) | «журнал — правило: `COORDINATOR.md` § Routing log (старый журнал до 08.10 — только чтение, в истории репозитория);» | pointer_lint prose anchor `§ Routing log` resolves to heading «## Routing log — …» |
| P5 | 5 | DUP | PROJECT.md п. 6 :198-199, «`DECISIONS.md` держит только то, что нужно каждой сессии» … «архиве решений.» | 185 | none (DECISIONS.md header, after L10) | «Что держит `DECISIONS.md` — его шапка.» | none |
| P7 | 2 | HIST (example) | PROJECT.md § Ссылки :273-274, «Ссылка `<папка клона>/docs/...` из сессии, открытой в самом клоне, даёт «Couldn't find this file».» | 145 | PROJECT_FULL.md:454 holds it | nothing; the next sentence «Перед первой ссылкой…» starts the line | none |
| K1 | 5 | DUP | CLAUDE.md hygiene :96-100, the bullet «- **Рабочий каталог шелла не меняется никогда** …» … «сброс папки сессии на корень.» merged into point 3 :95 | 580 | none (every fact kept in the new point 3) | text R-K1 below | anchor `3. The shell's working directory never moves` (line start kept); K-WORKER: the text names no read duty of COORDINATOR.md |
| B1 | 2 | HIST+DUP | CURRENT_CONTEXT.md § Current Milestone :8-13, heading + paragraph (move to GitHub, O2/O3) | 380 | @ docs/tasks/compact-snapshots/2026-11-18-current-context-archive.md (new, E2) | none (D-0064 and PROJECT.md:3-5 hold the repo facts) | none |
| B2 | 2 | HIST | CURRENT_CONTEXT.md § Current Task :16-22, «Release 0.11.0 is out» … «2026-11-16-2323-narrative.md`.» | 610 | @ same archive | text R-B2 below; sentences with no other home STAY (E4) | none |
| B3 | 2 | HIST | CURRENT_CONTEXT.md :24, «The journal starts anew in this repository» … «`continues_from: t-NNNN`.» | 265 | @ same archive | none (the first `journal_created` line carries the field) | none |
| B4 | 5 | DUP | CURRENT_CONTEXT.md § Maintenance Rule :5-6 body | 70 | none (PROJECT.md «Командная работа» п. 5) | «Rule: `PROJECT.md` «Командная работа» п. 5; read on every boot — keep it short.» | none |
| S9 | 3 | record | docs/SIBLING_MAP.md:493, axis-31 row of `docs/CLAUDE_HOST_ADAPTATIONS_FULL.md`, Aspect cell | +40 (not boot) | — | Aspect gains «; COORDINATOR.md text moved out by a boot diet, verbatim» | Owner cell unchanged (starts «reason only»; `pointer_lint.main_documents` reads it) |

Part B subtotal: ~5025 B.

Replacement texts (the builder copies them verbatim; wrap at the file's ~120-char width, an anchor never split across lines):

- R-C1: «The coordinator's routing policy of this repository; it holds nothing that not every session needs. The worker block
  is `CLAUDE.md` (auto-loaded); the project's own rules, principles and layout are PROJECT.md, read with this file;
  history of its clauses: `docs/CLAUDE_HOST_ADAPTATIONS_FULL.md`. Full state restoration goes through BOOT.md, not here:
  boot context is expensive (boot-context-is-expensive rule). Without this policy in context (the `COORDINATOR RULES:`
  line), Lead ends up doing delegable work itself on a tier above the work's (cheapest-tier-default rule).»
- R-C3: «SCOPE OF THE WITNESS RUN: for every writing node, solo or parallel, the files that
  `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <owns>` prints, by the rule
  `docs/TESTING.md` «Что запускать по своей правке» (an owned path outside the package, where that command has no row:
  the test file that judges the path, named in the DoD).» — then the paragraph continues unchanged «The full sets are the
  BATCH CANON: …».
- R-K1 (replaces line :95 and deletes :96-100 and nothing else): «3. The shell's working directory never moves (`cd`,
  `Set-Location`, `Push-Location`), not even inside one command (the PowerShell location outlives the call): refused; the
  Bash `( cd <dir> && ... )` subshell is the door. Hooks run `python tools/...` relative to the cwd: after a move they find
  no `tools/*.py` and EVERY tool is blocked. Package tests that need the package as cwd run in the builder's worktree. A
  hook that "cannot find tools/x.py" -> stop and reset the session folder to the root.» (the Bash subshell door is
  `tools/hygiene_gate.py:73`, `subshell_scopes_cwd` True for Bash, False for PowerShell :119-122).
- R-B2: «State of `main` and the next session's queue: the newest
  `docs/tasks/compact-snapshots/<date>-<HHMM>-narrative.md`; open plan phases are nodes in `plans/piles/`; open
  dispatches: the SessionStart open-dispatch scan.»

### Part L — Lead (DECISIONS.md is written only by the Lead or the Architect, PROJECT.md «Командная работа» п. 5)

Step-5b verdict for every live entry (DECISIONS_ARCHIVE grounds (a)/(b)/(c) of its :158-161, the owner's 11.11 «Да, убирай»):

| id | entry | verdict | ground | ~B |
|---|---|---|---|---|
| L1+L2+L10 | header :3-25 | merged to ONE paragraph, text R-L10; the two number lists («Archived so far: …», «Moved out whole on this ground …») leave: the archive's own headings and lists (:156-215) already enumerate them | DUP | 1050 |
| L3 | D-0002 | moved whole | (b) COORDINATOR § Tiers «No tier runs on Haiku (D-0002)», P7; (c) «host adaptation 1 in CLAUDE.md» no longer exists | 215 |
| L4 | D-0003 | moved whole | (b) `delegation.config.yaml`; (c) lead superseded by D-0067 | 250 |
| L5 | D-0007 | moved whole | (b) PROJECT.md § Прогоны и эксперименты :148-149 | 420 |
| L6 | D-0039, D-0043, D-0047 (heading block :38-40), D-0049, D-0050 | moved whole | factory behaviour, the class of «part 2» (:195-198); carriers P22 (cites D-0039), P5 (cites D-0043, D-0047), P23 (cites D-0049, D-0050) in docs/OWNER_PRINCIPLES.md; D-0049's grounding mechanism is package code (`coverage_contract.py`, `gate-registry.json`) | 2165 |
| L7 | D-0064 | moved whole | (b) PROJECT.md:3-5 | 280 |
| L8 | D-0067 | trimmed, text R-L8; line as it stood -> «Full text of trimmed lines» | DUP: architect duties = COORDINATOR § Tiers; stand-in = rule 6; no worker acceptance = § Role ≠ tier; `tier: opus` = lead rank | 590 |
| L9 | D-0033, D-0037, D-0063 | trimmed: D-0033 drops «(the owner, 06.10.2026: «поддерживать порядок» after the 0.8.1 clean-up; B-417, B-309)»; D-0037 drops «(inventory …t-600-exam-debts.md), priority П3; the weekly calibration runs after forge batch 4 closes»; D-0063 drops «spec t-2065;» and «because `PROCESS/CRITIC_EXAM.md` does not exist and exams stand deferred by D-0037; … the debt joins `plans/piles/forge/batch-3-exam-debts.md`». The words «this line is the recorded pass» and every «Detector:» stay | HIST (story, schedule) | 490 |
| — | D-0046 | STAYS pending F3 | contradicts COORDINATOR rule 12 (§11 N2) | 0 |

Part L subtotal: ~5460 B.

- R-L10: «One line per decision — the operative statement, not the discussion. This log is read by EVERY session, so it
  keeps only what every session needs (the owner, 06.10 and 11.11.2026): a lasting rule, a binding, a boundary. A
  temporary decision (a one-time plan, a schedule, a "confirm next session" note, a branch's state) goes to
  CURRENT_CONTEXT.md or the backlog; a decision that belongs to one node, spec, batch or day, or whose rule text lives in
  CLAUDE.md, COORDINATOR.md, PROJECT.md or a role file, is written into that carrier and, if it needs a number, into
  docs/DECISIONS_ARCHIVE.md. A new decision is appended at the end, in the order it was made; a line is never edited or
  renumbered, with one move allowed: a line that has stopped being operative is MOVED whole to docs/DECISIONS_ARCHIVE.md
  with the date and the reason, and an over-long line is trimmed here to its operative statement with its full text kept
  there; a number is never reused. A D-number cited anywhere and absent below resolves in the archive.» + the unchanged
  «Format:» line.
- R-L8: «- D-0067 — The ladder (the owner, 16–17.11.2026; spec docs/tasks/specs/20261116-architect-tier-spec.md): Lead
  is bound to claude-opus-5-5, a new function `architect` above Lead to claude-fable-5-1 (`delegation.config.yaml`;
  ranks and the one reader: `tools/tier_ladder.py`); the rules are COORDINATOR.md § Tiers, rule 6 and § Role ≠ tier.
  The Lead exam for the Opus candidate is deferred to FG7-54 by the owner's word: the informed pass of
  `exam.on_failure`. Full text: `docs/DECISIONS_ARCHIVE.md`.» (one line in the file).
- Archive form: a new section «## Moved out whole by the every-session audit, part 3 (18.11.2026, FG7-62)» after :215,
  one `### D-nnnn — (<ground>) …` heading per moved line with the line verbatim under it (the :174-193 form); trimmed
  lines under «## Full text of trimmed lines» as «### D-nnnn — trimmed to its operative statement; the line as it stood
  (boot squeeze, trimmed 18.11.2026)»; the two header lists verbatim under «### The live log's header lists as they stood
  (moved 18.11.2026)».

## 4. Two-world totals (all estimates until the Lead's span run, §2)

| world | before | card saving | after |
|---|---|---|---|
| A: t-1489 not landed | 118475 (measured) | ~10485 (B ~5025 + L ~5460) | **~107990** — at the target, band ±1000 |
| B: t-1489 landed first (its F9 (a): COORDINATOR_FILES unchanged) | ~113500-114500 (t-1489's own 4-5 KB estimate, not measured) | ~10485 (spans disjoint, E1) | **~103000-104000** |
| B': t-1489 with its F9 (b) (`docs/TEAMWORK.md` added to COORDINATOR_FILES) | grows by the whole TEAMWORK.md | ~10485 | not bounded by this card: F9 (b) is a boot GROWTH, ask before choosing it |

Reading: in world A the card alone lands within about 1 KB of 108000 either side; every safe class is spent. It removes
the WARN for sure (after < 110000 even at the pessimistic edge) but meets the 2 KB margin only by luck; the remainder is a
deep cut and belongs to the owner (F1). The Lead's span run before dispatch turns the estimate into a number; if it shows
a shortfall, the dispatch waits for F1.

## 5. Pins and anchors touched — how each stays green

- `tools/install_parity_anchors.json` units `routing-policy` (CLAUDE.md) and `routing-policy:coordinator` (COORDINATOR.md):
  K1 keeps `3. The shell's working directory never moves`; C2 keeps `TWO-LAYER CRITIC ENTRY`, `starts with EMPIRICS`;
  C3 keeps `SCOPE OF THE WITNESS RUN:`, `scenario_walk.py --witness-for <owns>`, `the BATCH CANON:`; C6 keeps
  `ISO local time`, C4/C5 keep `ACCOMPLISHED FACTS,`, `DEAD-WORKER REPLACEMENT:`. No anchor string is edited; each stays on
  one physical line. Witness: `tools/test_install_parity.py` (`test_manifest_anchors_match_live_sources`).
- `tools/tests/test_role_carriers_one_owner.py` OWNER_KEYS: `routing:rule-11`, `routing:hygiene-6` (CLAUDE.md),
  `routing:rule-9`, `routing:rule-9-exit`, `cost:cap` (COORDINATOR.md), `cost:queue` (PROJECT.md «цель держать 6
  пишущих билдеров») — no move touches them. POINTERS rows 75, 76, 85, 88, 91, 96-105, 107 — carriers keep the pointer
  text (P2 keeps row 101, P6 keeps rows 75/76/103, C3 keeps row 85). K-WORKER: R-K1 carries no `@` import and no read duty.
- `tools/pointer_lint.py --check`: TOC tables (COORDINATOR § Contents, PROJECT § Оглавление) are not edited and every
  heading they name stays; NUMBER_PAIRS sentences («carries 3 OR MORE numbered items», «| 6 writers, queue», «держать 6
  пишущих», «WARN 250K», «STOP 400K») untouched; new path tokens resolve (`docs/PROJECT_FULL.md`,
  `.claude/agents/critic.md` rule 21, `COORDINATOR.md` § Routing log); the R-B2 path uses the `<date>-<HHMM>` placeholder.
- `tools/agents_md.py --check`: AGENTS.md is regenerated after K1 (`python -B tools/agents_md.py`).
- `tools/session_context.py` constants (BOOT_WARN 110000, BREACH 120000, CLAUDE_WARN 16700): unchanged (non-goal).

## 6. Cards

### Card B — builder

task: <new task id>
node: forge/7/FG7-62
given: this spec (C:/QAFactory/forge-repo/docs/tasks/specs/20261118-fg7-62-boot-squeeze-card.md) §3 Part B, §5, §7; C:/QAFactory/forge-repo/COORDINATOR.md; C:/QAFactory/forge-repo/PROJECT.md; C:/QAFactory/forge-repo/CLAUDE.md; C:/QAFactory/forge-repo/CURRENT_CONTEXT.md; C:/QAFactory/forge-repo/docs/CLAUDE_HOST_ADAPTATIONS_FULL.md; C:/QAFactory/forge-repo/docs/PROJECT_FULL.md; C:/QAFactory/forge-repo/docs/TESTING.md; C:/QAFactory/forge-repo/.claude/agents/critic.md; C:/QAFactory/forge-repo/tools/install_parity_anchors.json; C:/QAFactory/forge-repo/tools/tests/test_role_carriers_one_owner.py
owns:
C:/QAFactory/forge-repo/COORDINATOR.md
C:/QAFactory/forge-repo/PROJECT.md
C:/QAFactory/forge-repo/CLAUDE.md
C:/QAFactory/forge-repo/AGENTS.md
C:/QAFactory/forge-repo/CURRENT_CONTEXT.md
C:/QAFactory/forge-repo/docs/CLAUDE_HOST_ADAPTATIONS_FULL.md
C:/QAFactory/forge-repo/docs/SIBLING_MAP.md
C:/QAFactory/forge-repo/docs/tasks/compact-snapshots/2026-11-18-current-context-archive.md
non-goals: no edit of DECISIONS.md or docs/DECISIONS_ARCHIVE.md (Card L); no move outside §3 Part B, however tempting; no threshold or constant change; no TOC row, heading or anchor edited; no rewording of a kept rule; no `test:` file; no commit (the Lead commits, S1); the t-1489 spans of PROJECT.md (TOC rows «Бэклог и находки» and «Командная работа», rows `plans/BACKLOG.md` and `docs/TEAMWORK.md` of «Где что лежит», п. 4 of the package section, § Бэклог и находки, «Командная работа» lead-in and п. 1-4, 7, 9, 11) and COORDINATOR.md :38, :39, :168 are not touched
handoff: the worktree diff, uncommitted + the report (builder.md rule 7) with: per move id the verdict (done / stayed -- why, E4); before/after bytes per touched boot file (command below); the DOC-DISPATCH script in full source, its output, and its negative-control output; the `BOOT BUDGET:` line before and after
edges: §7 E1-E12
DoD: `python -m pytest tools/test_install_parity.py tools/tests/test_role_carriers_one_owner.py tools/test_pointer_lint.py -q` + `python -B tools/pointer_lint.py --check` (exit 0) + `python -B tools/agents_md.py --check` (exit 0) + `python -B <worktree>/tools/session_context.py </dev/null` (the `BOOT BUDGET:` line: 9 files, no `missing`, total lower than before by the Part B saving, within ±25 % of ~5025) + the DOC-DISPATCH key run below
siblings: t-1489 (backlog rules -> docs/TEAMWORK.md; owns PROJECT.md, AGENTS.md, test_role_carriers_one_owner.py, Lead texts for COORDINATOR.md :38/:39/:168 and SIBLING_MAP.md :479/:494/:495): spans disjoint, order S2; SIBLING_MAP axis 31 (row 493, S9); boot-diet SKILL step 4 pairs (PROJECT.md <-> PROJECT_FULL.md: P7/P8 delete only text PROJECT_FULL holds)
designer: C:/QAFactory/forge-repo/docs/tasks/specs/20261118-fg7-62-boot-squeeze-card.md

DOC-DISPATCH keys (verbatim, whitespace-squashed; script in full source in the report, never committed; negative control:
the run on a COPY of COORDINATOR.md with KB-1 removed reports failure):
- present: KB-1 COORDINATOR.md `SCOPE OF THE WITNESS RUN:`; KB-2 COORDINATOR.md `scenario_walk.py --witness-for <owns>`;
  KB-3 COORDINATOR.md `(cheapest-tier-default rule)`; KB-4 COORDINATOR.md `(boot-context-is-expensive rule)`; KB-5
  COORDINATOR.md `` `.claude/agents/critic.md` rule 21 ``; KB-6 CLAUDE.md `subshell is the door`; KB-7 PROJECT.md
  `` правило: `COORDINATOR.md` § Routing log ``; KB-8 PROJECT.md `` `docs/OWNER_PRINCIPLES.md` (они же FR-47…FR-57 ``;
  KB-9 CURRENT_CONTEXT.md `the SessionStart open-dispatch scan`.
- absent: KA-1 CLAUDE.md `Рабочий каталог шелла не меняется никогда`; KA-2 COORDINATOR.md `brief: what was delegated`;
  KA-3 COORDINATOR.md `id_band`; KA-4 PROJECT.md `Couldn't find`; KA-5 PROJECT.md `здесь — коротко, для`; KA-6
  CURRENT_CONTEXT.md `## Current Milestone`; KA-7 COORDINATOR.md `investigating the mechanics by reading is not`.
- verbatim: KV-1 every span of C4, C5, B1, B2 (as moved), B3, taken from `git show HEAD:<file>`, is a squashed substring
  of its home file.

### Card L — Lead (after Card B is accepted, same worktree)

1. DECISIONS.md and docs/DECISIONS_ARCHIVE.md: L1-L10 by §3 Part L (archive first, then the live log).
2. Span check: every moved D-line, verbatim from `git show HEAD:DECISIONS.md`, is a substring of the archive (KV-2);
   absent from DECISIONS.md: `- D-0002`, `- D-0003`, `- D-0007`, `- D-0039`, `- D-0043`, `## D-0047`, `- D-0049`,
   `- D-0050`, `- D-0064`, `Archived so far:` (KA-8..KA-17).
3. `python -B tools/session_context.py` in the worktree: `BOOT BUDGET:` total <= 108000, 9 files, no `missing`.
   108001-110000 -> F2; > 110000 -> reject (regression).
4. One commit: the boot-diet step-7 report lines (before/after per file, moves, step-4 verdicts: «PROJECT.md <->
   PROJECT_FULL.md: P7, P8 deleted only text PROJECT_FULL holds (:454, :320); DECISIONS.md <-> ARCHIVE: every moved line
   verbatim; COORDINATOR.md <-> CLAUDE_HOST_ADAPTATIONS_FULL.md: C4, C5 verbatim, rule 4a pair untouched»), plus the
   gate's lines `axes: not a mechanism (boot squeeze FG7-62: verbatim moves and pointers, no duty added or removed)` and
   `tier: opus` (the gate's form is `tools/mechanism_gate.py`; not copied here). Then `wave.py merge`.

## 7. Edges (behaviour + invariant)

| id | edge | behaviour | invariant |
|---|---|---|---|
| E1 | TEMPORAL: t-1489 lands before or after | every span is found by its quoted start/end text, not its line; the t-1489 spans (non-goals) are never edited; if a quoted span is not found verbatim, the move is reported «stayed -- span changed» | no line is edited by both cards; neither order breaks the other |
| E2 | TEMPORAL: archive homes created by this card (the CC archive file; the FULL § for C4/C5; ARCHIVE part 3) | before: absent; after: holding the verbatim spans. A home that already exists at run time (another diet the same day) is APPENDED to, never overwritten | evidence is never deleted, only moved (SKILL step 3) |
| E3 | a span with no other carrier | moved only with its archive copy in the same diff (KV-1/KV-2); DUP moves rest on the home named in §3, re-read by the builder before the cut; a home that does not hold the clause -> the span stays | an operational clause never leaves the boot without its home holding it |
| E4 | open remainder in B2 | «Open dispatch t-073 = node PC4-1: … waits for the owner's word» moves only if the PC4-1 row of `plans/piles/package-ci/batch-4-*.md` shows that wait; «`main` carries FG7-8 part B … NOT in 0.11.0» moves only if a fragment under `ai-packages/qa-factory/changelog.d/` names FG7-8; otherwise the sentence stays in CURRENT_CONTEXT.md | a live item never loses its only carrier (SKILL step 3) |
| E5 | anchors and pins (§5) | none is edited; a move that would split one across a line or change it is not made | the three witness files and `pointer_lint --check` stay green |
| E6 | the 108000 limit | `<= 108000` passes; 108001 fails Card L step 3 -> F2; the builder never adds a move to close a gap | no threshold constant changes; no unlisted cut |
| E7 | a boot file missing after the edits | `session_context` counts it 0 and names it: a `missing` in the line fails the DoD | the total never drops because a file vanished |
| E8 | encoding and line ends | files keep UTF-8 without BOM and the line ending they have at HEAD; no re-wrap outside the edited paragraph | the saving comes from moved text only |
| E9 | «no cut of meaning» vs «reach 108000» | meaning wins; the shortfall is F1's | an operational rule never leaves the boot by this card |
| E10 | a pointer left | resolves (`pointer_lint --check`); a pointer to a section names a heading that exists | no dangling pointer is created |
| E11 | the kept sentences of C1 | SKILL:8 and SKILL step 6 cite them: kept verbatim in R-C1 | a reader of COORDINATOR.md's opening still finds both rules |
| E12 | AGENTS.md | regenerated after K1, `--check` exit 0 | the Codex copy never lags CLAUDE.md |

## 8. Readers of every touched file (designer rule 7)

The `owns_readers` block is NOT attached to the brief: the Lead runs, before dispatch,
`python -B tools/owns_readers.py --paths COORDINATOR.md PROJECT.md CLAUDE.md AGENTS.md CURRENT_CONTEXT.md DECISIONS.md docs/DECISIONS_ARCHIVE.md docs/CLAUDE_HOST_ADAPTATIONS_FULL.md docs/SIBLING_MAP.md --readers`
and the plan critic checks the lines below against it. Hand grep (my trail): tools/*.py
`DECISIONS(_ARCHIVE)?\.md|CLAUDE_HOST_ADAPTATIONS_FULL` -> 8 files, 41 hits; tools/*.py
`Maintenance Rule|Current Task|Current Milestone|CURRENT_CONTEXT` -> 8 files, 33 hits; .githooks the five boot names ->
0 hits (control: `tools/` -> 26 hits in 4 files); `install_parity_anchors.json` `host_path` -> boot files CLAUDE.md, COORDINATOR.md only.

| file | reader | verdict |
|---|---|---|
| all 9 boot files | `tools/session_context.py` (sizes, BOOT BUDGET) | unchanged; the total drops |
| COORDINATOR.md, PROJECT.md | `tools/coordinator_rules.py` (COORDINATOR_FILES) | unchanged |
| CLAUDE.md, COORDINATOR.md | `tools/install_parity.py` + `install_parity_anchors.json`, `tools/test_install_parity.py` | unchanged; anchors kept (§5) |
| CLAUDE.md, COORDINATOR.md, PROJECT.md, SYSTEM_PROMPT.md, CLAUDE_HOST_ADAPTATIONS_FULL.md | `tools/tests/test_role_carriers_one_owner.py` | unchanged here; changes in stream t-1489 (its owns) |
| CLAUDE.md, COORDINATOR.md, PROJECT.md (main documents) | `tools/pointer_lint.py`, `tools/pointer-lint-exempt.json` | unchanged; new tokens resolve |
| docs/SIBLING_MAP.md | `pointer_lint.main_documents` (axis-31 Owner cells) | unchanged (row 493's Owner cell not edited) |
| CLAUDE.md, COORDINATOR.md, DECISIONS.md, docs/SIBLING_MAP.md | `tools/mechanism_gate.py` (MECHANISM_PREFIXES, DECISIONS diff) | unchanged; the Lead's commit carries its lines |
| CLAUDE.md, COORDINATOR.md, DECISIONS.md, CURRENT_CONTEXT.md, SYSTEM_PROMPT.md | `tools/claim_control_gate.py` (ROOT_FILES; WARN-only Edit/Write hook) | unchanged; a WARN is possible, never a block |
| CLAUDE.md -> AGENTS.md | `tools/agents_md.py` | AGENTS.md regenerated in Card B |
| CURRENT_CONTEXT.md | `tools/compact_snapshot.py` (mtime; «read CURRENT_CONTEXT.md, then the newest narrative») | unchanged; R-B2 says the same |
| CURRENT_CONTEXT.md | `.claude/skills/session-handoff/SKILL.md` check 3 (closed work archived out) | unchanged; this card is that move |
| DECISIONS.md | `tools/escape_check.py --hash` (reads `docs/DECISIONS_FULL.md`; `escape_allowlist.json` `entries: []`) | unchanged; no pinned decision hash |
| DECISIONS.md, SYSTEM_PROMPT.md | `session_context` layer A (`layer_a_file_names`) | unchanged; less text injected |
| COORDINATOR.md opening | `.claude/skills/boot-diet/SKILL.md` :8 and step 6 | unchanged; sentences kept (E11) |
| PROJECT.md, COORDINATOR.md, SIBLING_MAP.md, AGENTS.md | t-1489 card | changes in stream t-1489; disjoint spans; SIBLING_MAP rows 493 (here) and 494 (there) are adjacent -> the later merge resolves (S2) |
| DECISIONS_ARCHIVE.md, CLAUDE_HOST_ADAPTATIONS_FULL.md, the CC archive | humans; `test_role_carriers` POINTERS rows 89-90 (carrier FULL) | unchanged; rows' texts stay in FULL |

## 9. Forks for the owner (plain words)

**F1 — If the card falls short of 108 KB, which bigger cut may we make?** Every "safe" cut (archives, duplicates,
pointers) is in the card and lands at about 108 KB, give or take 1 KB. The rest means moving a working rule out of the
files every coordinator session reads. Options (bytes are estimates):
(a) COORDINATOR rule 12: the recipe for measuring a fix round (git diff command, three regex lines, ~1.5 KB) becomes a
small tool that prints the count; the rule keeps one line naming the tool. Cost: one builder node. Fits «what code can
do, code does» (owner, 14.11).
(b) the journal section's descriptions of what the validator does by itself (~1.3 KB) move to the history file; the
section keeps the duties and one line «checked at write and at commit».
(c) «Как разрабатывается новая идея»: steps 1-4 (the Architect's part) move to `PROCESS/ARCHITECT_START.md` (~1.2 KB).
(d) the shorter one-line index of the owner's principles (cut lines at ~80 instead of ~120 characters, ~2 KB) — a
generator change; the coordinator sees less of each principle.
(e) the «Где что лежит» path map (~2.4 KB) leaves PROJECT.md (after t-1489, which edits two of its rows).
Recommendation: (a), then (d) if still short. Ask: which of (a)-(e) are allowed?

**F2 — Land the card if the measured total is between 108 and 110 KB?** The warning disappears (it fires above 110 KB),
but the 2 KB margin is not met until an F1 cut follows. (a) land now, F1 as the next node; (b) hold the card until F1 is
decided. Recommendation: (a) — every session stops paying the warning today, and nothing in the card is lost.

**F3 — D-0046 says "no critic re-review of a fix round"; COORDINATOR rule 12 now orders a re-review in five named cases.**
(a) archive D-0046 as no longer true (rule 12 is the rule; its clause «`rejected` with `basis: critic`» has no home in
the journal shapes and would need one); (b) keep D-0046 and change rule 12; (c) leave both, ask the Architect (a rule
conflict is Architect-class, COORDINATOR rule 6). Recommendation: (c) now; (a) saves ~560 B once decided.

## 10. Small choices closed by the designer

- S1 the Lead commits (the commit-msg gate needs a Lead-tier `tier:` line on mechanism paths; t-1489's §6 precedent).
- S2 order with t-1489: FG7-62 first (it waits for no owner fork except F1/F2, which act after it); t-1489 then merges
  `main` and resolves (TEAMWORK § 3 «поздний узел сливает main»), its spans being quoted text. Either order works (E1).
- S3 the C4/C5 home is `docs/CLAUDE_HOST_ADAPTATIONS_FULL.md` (COORDINATOR.md:6-7 already names it «History of its
  clauses»), a new section «## COORDINATOR.md text moved by boot diets (verbatim)»; its axis-31 row gains the aspect (S9).
- S4 K1 merges the Russian duplicate into English point 3 (the anchored line); every fact of the bullet is kept.
- S5 R-L10 adds COORDINATOR.md to the carrier list of the DECISIONS header (it holds former CLAUDE.md rules since t-1137).
- S6 D-0033/D-0037/D-0063 are trimmed, not moved: they are standing gate passes that calibration reads by number.

## 11. Noticed, not widened

- N1 t-1489 rewrites COORDINATOR.md:168, whose phrase «Team work in piles and batches: the rule text is PROJECT.md» is an
  anchor (`tools/install_parity_anchors.json:66`): its Lead text must keep the phrase or update the anchor in the same
  commit — for t-1489's card, not this one.
- N2 D-0046 vs COORDINATOR rule 12 (F3).
- N3 COORDINATOR rule 7 still cites D-0016 («the interface already shows the model»), archived as «decided and NOT built».
- N4 PROJECT.md:43 calls `plans/BACKLOG.md` «единый список» while п. 4 freezes it — t-1489 S4 fixes it.

## 12. Reading trail

Read whole: `.claude/skills/boot-diet/SKILL.md`; `COORDINATOR.md`; `PROJECT.md`; `DECISIONS.md`; `CURRENT_CONTEXT.md`;
`SYSTEM_PROMPT.md`. Windows: `tools/session_context.py:205-229, 1225-1440, 2703-2754` and greps (`BOOT_`,
`_coordinator_files`, `repo_root`); `CLAUDE.md:93-108` (+ the auto-loaded copy); `docs/TESTING.md:91-110`;
`.claude/agents/critic.md:82-93, 182-195`; `.claude/agents/builder.md:125-136`; `docs/OWNER_PRINCIPLES.md:13-24,
80-109`; `docs/DECISIONS_ARCHIVE.md` headings + :156-217; `docs/SIBLING_MAP.md:478-527`;
`tools/install_parity_anchors.json:1-139` + `host_path` grep; `tools/tests/test_role_carriers_one_owner.py:36-115`;
`tools/pointer_lint.py:1-30` + grep; `tools/mechanism_gate.py:212-236`; `tools/claim_control_gate.py:250-269`;
`tools/escape_check.py:18-39, 275`; `tools/escape_allowlist.json`; `tools/hygiene_gate.py` grep `subshell`;
`tools/agents_md.py` grep `--check`; t-1489 spec greps + :174-213; batch-7 row FG7-62; the three index heads.
Positive controls: `docs/PROJECT_FULL.md` holds «Couldn't find» (:454), «схемы неиспользуемых» (:320); no
`*current-context*` file under `docs/tasks/compact-snapshots/` (control: the same glob form lists 2026-11-17/18
snapshots); `CLAUDE_HOST_ADAPTATIONS_FULL.md` lacks «cheapest-tier-default» and `id_band` (control: «Cost gates», 3 hits);
`PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md` check 14 read at :442-459 (reads role-file edits, not DECISIONS text).
Measured by me: nothing (no shell) — every byte figure outside `facts:` is an estimate; the Lead's commands are in §2.

## 13. Lead decisions (18.11, Lead 501cb4e0)

- F2 (a), decided by the Lead: the card lands when the measured total is below 110000; 108000 stays the target; a
  shortfall is a report line, not a hold. The Lead's span run before dispatch is replaced by the builder's measured
  total (session_context.py in its worktree), since under F2 (a) the dispatch no longer waits on the number.
- F1 (a), decided by the Lead (the rule stays, its recipe becomes code: owner 14.11 «what code can do, code does»): a
  separate node after this card -- a small tool prints the fix-round count; COORDINATOR rule 12 keeps one line naming
  it. (b)-(e) are not taken.
- F3 (c): sent to the Architect (docs/tasks/architect-queue.md, line of 18.11); this card does not touch D-0046 or rule 12.
- Card B goes as task t-1519; Card L follows after Card B is accepted, in the same worktree.
