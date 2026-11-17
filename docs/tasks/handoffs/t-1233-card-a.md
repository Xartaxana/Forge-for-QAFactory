# t-1233 Card A (FG7-57) report: the text move (docs)

Tree: `C:/QAFactory/forge-repo/.claude/worktrees/wb-int` (branch wb-int at 7f945fdd; `origin/main` is now 79ceaac5, a descendant;
`git diff HEAD origin/main` over every Card A owns path is empty, so the witness base `origin/main` is the same text).
Nothing was committed, staged or reset; no `tools/`, `.githooks/`, `ai-packages/` file touched. All edits keep each file's
line-ending form (CRLF files stay CRLF; CLAUDE.md, AGENTS.md, PROJECT.md, COORDINATOR.md are LF).

## What landed per behaviour item

1. CLAUDE.md and COORDINATOR.md built from the old CLAUDE.md by line ranges (never retyped), §2 order. CLAUDE.md: title, NEW
   intro (under 600 bytes), `## Worker duties` ((a) the enforcement sentence on its original three lines, (b) the trimming
   sentence), `## The dispatch form (rule 11)` (the four `### Rule 11` blocks + R11 table, three `COORDINATOR.md rule N`
   retargets), `## Command hygiene (permission hygiene)` whole (point 3's tail replaced by the cwd bullet, moved verbatim from
   PROJECT.md; one blank line added before point 4 so the bullet does not swallow it), `## Язык` moved from PROJECT.md. No `@`
   line. COORDINATOR.md: NEW head line (C1), the old intro lines, C2 swap, C3 paragraph without the `@` lines, Contents with
   C4 retargets, Tiers, rules 1-10, the rule-11 stub `### Rule 11 · the dispatch form — CLAUDE.md § The dispatch form (rule
   11)`, 11a, 12, 13, Routing log, Role ≠ tier, Lead degradation.
2. Placed: §5.1 (Cost gates, with the t-1202 fixes 1 and 2 applied as written: widened line-start list, mid-line `for`, widened
   write list; `reviewed:<sha>` as the first token after the model label in the critic Agent `description`, the Lead commits the
   reviewed state first, absent or cut token = `nobase`); §5.2 (R13-g row; PROJECT п.12 «(до 4 узлов: R13-g)»); §5.3 (rule 2
   drafting paragraph + designer.md rule 3 sentence); §5.4 (designer.md rule 4 "Write and Edit", rule 8, frontmatter `tools:
   Read, Glob, Grep, Write, Edit`); F3's PROJECT p.1 sentence (a new line after item 1's last line).
3. Every §4.1 row marked A retargeted (diff at the end). Line numbers in the spec were stale in places (builder 107/116/117 are
   107/117/118 here; WEEKLY 1006/1045/1046/1125/1129 are 1013/1052/1053/1132/1136; RUNBOOK 614 is 622): found by text, not number.
4. SIBLING_MAP axis 31: intro 478-479 rewritten; rows 485, 490, 491, 494, 498, 500, 504, 507-508, 531, 533 and line 3 to the
   new homes; the COORDINATOR.md row ADDED as the spec wrote it (Owner cell starts with "owner", `owner word pending`), with the
   two clauses that sat in the CLAUDE.md row (critic questions → critic.md rule 22; Contents cells are POINTERS rows) appended
   to it (a move, I-1); the CLAUDE.md row now describes the worker block and ends "owner".
5. BOOT.md lines 5-8: names the worker block and the `COORDINATOR RULES:` line; no "Read X.md" form, no `COORDINATOR.md`.
6. LEAD_RANKING_EXAM item 2 per e13. WEEKLY_CALIBRATION: check 2 (R13-g of COORDINATOR.md + TOPIC CAP count per critic
   `delegated`), check 7 (first Task/Agent call follows a Read of COORDINATOR.md), check 10 and 33(h)/(i) name COORDINATOR.md,
   check 17 sub-item (g) = §5.1's detector (a)-(c) as (i)-(iii), check 28 sub-item (e) = §5.4's detector.
7. AGENTS.md regenerated with the live generator (`wrote AGENTS.md: 24103 bytes`); transiently the worker block only; B1 regenerates.
8. Install-parity anchors for B1: last section.

## Sizes (k4, measured)

CLAUDE.md 14428 bytes (limit 20000; spec estimate 14.7 KB), COORDINATOR.md 43785 bytes (limit 60000; estimate 43.4 KB),
PROJECT.md 34998, AGENTS.md 24103. Derived CLAUDE_WARN for B1: ceil(14428 x 1.15 / 100) x 100 = 16700 (spec estimate 17000;
B1 re-measures on its tree).

## Calls for the Lead (nothing blocked; each is implemented as stated, a revert is one line)

Q1. C1 keeps the old intro verbatim in COORDINATOR.md ("Auto-loaded into every session: the routing policy ..."), no longer true
    of that file; the NEW head line above it says how it is read. I-1 forbids rewording; one edit by the Lead fixes it.
Q2. C2/C3 deleted the `@` lines but the sentences keep their trailing colon (§3 allows only the phrase swap). Cosmetic.
Q3. Retargets whose NEW wording the spec did not give (I chose the smallest honest one): boot-diet 8, 21-24 ("pulls in by
    `@import`" → "the `COORDINATOR RULES:` line names"), 85, 99, 103; session-handoff 56; README 15 and 41; BOOT.md 5-8; RUNBOOK
    201-202 and 622 (cwd bullet now in CLAUDE.md); SIBLING_MAP 507-508 (readers become "coordinator"), 494.
Q4. §4.1 lists WEEKLY 498 ("a pre-dispatch checklist is an edit of CLAUDE.md"): that is rule 11's five-point checklist, which
    stays in CLAUDE.md under (d), so the citation is still valid; left UNCHANGED.

## Analogs noticed, not widened

- docs/SIBLING_MAP.md: 28 (axis 1 row "Routing policy | CLAUDE.md"), 37, 40, 97 and 105 ("imported by CLAUDE.md"), 99 and 503
  ("copy of CLAUDE.md + imports"), 547, 549 ("every cell of CLAUDE.md § Contents": the TOC pin moves in B1), 667.
- delegation.config.yaml 4, 7, 70 (70 is the same "function/grade split" sentence as gateway/config.template.yaml 49, which §4.1
  lists; yaml 70 is not listed).
- boot-diet 34 ("the CLAUDE.md host adaptations trimmed to pointers": a trimmed/full pair, step 4).
- PROJECT.md: p.1 still says the FR index is «грузится в каждую сессию»; the Оглавление row «Сессия форджа | шелл, коннекторы,
  сжатие контекста» still names the shell (the cwd bullet moved to CLAUDE.md).
- `.gitattributes` pins `CLAUDE.md`, `BOOT.md` and the three indexes to LF because the boot budget reads on-disk size;
  COORDINATOR.md (and PROJECT.md) are now measured by size too and are not pinned (outside my owns; B1 / Lead).

## Commit-message lines for the Lead (F8' as amended by t-1202 fix 3)

`Deviation: exam not run; debt F3-1` (precedent 9616b6f4); axis block: `axis 2: queued -- exam not run after the critic.md edit;
debt F3-1 (plans/piles/onboarding-forge/batch-2-onboarding-roles-forge-p3.md:67)`.

## Install-parity anchors for B1 (computed by literal substring against the new files; lists in the JSON block)

- unit `routing-policy` (host CLAUDE.md): of 89 anchors, 29 still hit CLAUDE.md and stay; the other 60 hit COORDINATOR.md as
  literal substrings (0 in neither) and move to the new unit `routing-policy:coordinator` (host_path COORDINATOR.md, kit_path
  `toolkit/CLAUDE.md`).
- unit `process-docs:lead-ranking-exam` (host PROCESS/LEAD_RANKING_EXAM.md): the anchor
  `2. Claude Code subagents auto-load CLAUDE.md, so the policy is` becomes `2. The dispatch attaches COORDINATOR.md whole, so the
  policy is`. Every anchor of every other unit whose host file I edited still hits.

```json
{
 "stay_in_CLAUDE.md": [
  "CLAUDE.md — QA Factory development",
  "enforcement file (a hook on the active hooks path",
  "11. DoD in every dispatch (DoD-in-every-dispatch rule):",
  "the spec NAMES ITS EDGE BEHAVIOR:",
  "(i) TEMPORAL",
  "Which tests a DoD asks for",
  "SCOPE CEILING:",
  "QUARANTINED",
  "CONTEXT MANIFEST",
  "DECLARATIVE on reads and",
  "FIVE-POINT CHECKLIST",
  "AND the edge behaviors NAMED",
  "DOC-DISPATCH WITNESS:",
  "a WRITING dispatch's \"given\" manifest",
  "given INLINE, never by pointer",
  "`tools/handoff_gate.py` lets it write only that file",
  "Command hygiene (permission hygiene)",
  "1. Tests — the canonical form, from the repo root:",
  "2. The proxy server — not used in this deployment",
  "3. The shell's working directory never moves",
  "4. File edits — by any tool",
  "5. Log entries — through `tools/journal_write.py` only",
  "6. An environment-negative claim requires verification:",
  "-E; -P needs a UTF-8",
  "a project decision rests on an UNKNOWN property of the environment",
  "valid ONLY by reading the carrier directly (the Read tool)",
  "7. Temporary corruption",
  "BYTE COPY,",
  "FROM IT;"
 ],
 "move_to_COORDINATOR.md": [
  "Tiers (see DELEGATION_TABLE.md; all assignments are estimates until calibrated)",
  "Routing rules",
  "1. Recon → scout by default:",
  "not used here: no scout exam set is registered",
  "spot-verifies at least one load-bearing claim",
  "2. Implementation from a finished spec → builder.",
  "DRIVING the UI;",
  "DRAFTING → designer BY DEFAULT",
  "3 OR MORE numbered items",
  "CONTEXT ISOLATION",
  "PRIMARY draft. A RESUBMISSION",
  "NEW task_id is a NEW task",
  "3. critic — a MANDATORY acceptance gate:",
  "`.claude/agents/critic.md` rule 22, Q6-Q7",
  "TWO-LAYER CRITIC ENTRY",
  "starts with EMPIRICS",
  "Critic-on-plan:",
  "4. Independent parts → several parallel subagents,",
  "SCOPE OF THE WITNESS RUN:",
  "scenario_walk.py --witness-for <owns>",
  "the BATCH CANON:",
  "4a. A task spanning 5 or more journal events,",
  "Team work in piles and batches: the rule text is PROJECT.md",
  "5. Flat delegation (flat delegation rule):",
  "6. Escalation: 2 failed attempts,",
  "7. Background execution by default",
  "with the worker's model:",
  "REQUIREMENT closes by MEASUREMENT,",
  "8. Universal skip rule:",
  "ROUTING MOTIVE",
  "SMALL-WORK BATCHING:",
  "SELF-EXECUTION ONLY on the FIRST",
  "IMMEDIATE SOLO builder dispatch",
  "DETERMINISTIC SCRIPT RUNS:",
  "9. Fix the class, not the instance (fix-the-class-not-the-instance",
  "sweep-the-artifact-first rule",
  "10. Four questions for every mechanism",
  "axis-enumeration rule",
  "tier-declaration rule",
  "A change to the package (D-0055, D-0060; P27)",
  "11a. Question routing (question-routing rule):",
  "12. The coordinator's cadence runs on LARGE moves,",
  "Cost gates (D-0035, D-0038, D-0040, D-0054;",
  "13. Leaf routing (leaf-routing rule)",
  "ONE critic pass per TOPIC, not one per part",
  "Routing log — logs/journal/<dev>.jsonl",
  "ACCOMPLISHED FACTS,",
  "ISO local time",
  "DEAD-WORKER REPLACEMENT:",
  "## Role ≠ tier",
  "MODEL NAME",
  "ROLE = ROUTING,",
  "ESCALATES UPWARD",
  "Lead degradation",
  "1. Drop to builder rank (Sonnet)",
  "2. While degraded:",
  "3. Default return at the task/session boundary:",
  "4. Tier verification at BOTH points",
  "ENTRY — before the FIRST",
  "EXTERNAL CROSS-CHECK"
 ],
 "lead_ranking_exam_old": "2. Claude Code subagents auto-load CLAUDE.md, so the policy is",
 "lead_ranking_exam_new": "2. The dispatch attaches COORDINATOR.md whole, so the policy is"
}
```

## Witness (DOC-DISPATCH): command

`python -B <scratchpad>/card_a_check.py --base origin/main` (scratch, never committed; exit code 0)

### Output (verbatim, complete)
```
k1 edited-lines list (every old line lost / new line gained, with its section 3 row):
  old-> [C2] The project's own rules, principles and layout live in PROJECT.md, imported here so every session loads them:
  old-> [C2] @PROJECT.md
  old-> [C3 (@ lines deleted)] @docs/FACTORY_RULES_INDEX.md
  old-> [C3 (@ lines deleted)] @docs/ARCHITECTURE_INDEX.md
  old-> [C3 (@ lines deleted)] @docs/OWNER_PRINCIPLES_INDEX.md
  old-> [C4 Contents rows] | Tiers | CLAUDE.md § Tiers |
  old-> [C4 Contents rows] | Recon → scout; builder; drafting | CLAUDE.md § 1 + CLAUDE.md § 2 + CLAUDE.md § Rule 2 · drafting → designer |
  old-> [C4 Contents rows] | Witness; acceptance by witness | CLAUDE.md § 2 |
  old-> [C4 Contents rows] | Batch canon | CLAUDE.md § Rule 4 · witness scope and the BATCH CANON + docs/RUNBOOK.md § 7. CI на GitHub и BATCH CANON |
  old-> [C4 Contents rows] | Critic gate | CLAUDE.md § 3 |
  old-> [C4 Contents rows] | Journal | CLAUDE.md § Routing log |
  old-> [C4 Contents rows] | Cost gates | CLAUDE.md § Rule 12 · Cost gates |
  old-> [C4 Contents rows] | Fix the class | CLAUDE.md § 9 |
  old-> [C4 Contents rows] | Mechanisms | CLAUDE.md § 10 |
  old-> [C4 Contents rows] | Language | PROJECT.md § Язык |
  old-> [C4 Contents rows] | Decide vs ask; owner away | PROJECT.md § Что решать самому, что спрашивать у владельца + CLAUDE.md § 11a |
  old-> [C4 Contents rows] | Degradation; Role ≠ tier | CLAUDE.md § Role ≠ tier + CLAUDE.md § Lead degradation |
  old-> [C7 enforcement sentence -> pointer] witness is a before/after screenshot or recording — a purely textual witness is insufficient. A self-activating
  old-> [C20-C23 citation retargets (S2 item 4)] fan-out declares ownership per rule 4 plus an optional maxConcurrent cap. The manifest is DECLARATIVE on reads and
  old-> [C20-C23 citation retargets (S2 item 4)] writing dispatch: owns/non-goals/handoff present and its witness scope named (rule 4); (5) freshness — the spec's
  old-> [C20-C23 citation retargets (S2 item 4)] | f | a dispatch to builder, or any dispatch whose `owns:` holds an absolute path (D-0022) | carries its manifest as HEADER LINES outside fences an
  old-> [C26 Cost gates] FRESH worker carrying only the diff and the verdict; `tools/agent_budget.py` caps a worker (WARN 250K, STOP 400K; the remainder goes to a fresh wor
  old-> [C26 Cost gates] re-review carries only the fix diff and the verdict; the Lead compacts by PROJECT.md § Сессия форджа, a stage
  old-> [C27 R13-g + S5.2] | g | the parts of one topic | ONE critic pass per TOPIC, not one per part (Cost gates, rule 12) |
  old-> [C35 point 3 tail replaced by the cwd bullet] why and how to recover: PROJECT.md § Сессия форджа
  old-> [P1] - **правила работы над фабрикой** — этот файл и блок Supervised-Delegation в `CLAUDE.md`: кто что
  old-> [P2] Этот файл читает КАЖДАЯ сессия, поэтому в нём только действующие правила (слово владельца 11.11.2026).
  old-> [P3] | Язык | какой язык где |
  old-> [P3] | Все темы → `CLAUDE.md` § Contents | карта «тема → где читать» |
  old-> [P4 + COORDINATOR row] | `docs/OWNER_PRINCIPLES.md` | полный текст принципов владельца P1–P31 (индекс — `docs/OWNER_PRINCIPLES_INDEX.md`, импорт из `CLAUDE.md`) |
  old-> [P5] импорт из `CLAUDE.md`.
  old-> [P6 + F3 sentence] замена текста правил для того, кто пишет код.
  old-> [P7-P10] (правило 3 `CLAUDE.md`), приёмка проверяет не только то, что края названы, но и то, что каждый
  old-> [P7-P10] (два прохода, правило 1 `CLAUDE.md`).
  old-> [P7-P10] 8. **Код, затем критик кода** (правило 3 `CLAUDE.md`, один проход на тему).
  old-> [P12] доказательства»); перенос подтверждает **человек**, не агент сам. **Остатков в идеале нет вовсе**: минорные замечания критика не откладываются стро
  old-> [P12] шесть; лимиты откатываются в понедельник вечером (владелец, 16.11.2026). Критик кода — один на тему, не на узел.
  old-> [P16] владельцу (правило 11a в `CLAUDE.md`): толкование замысла — не техническое решение.
  new-> [S2.2 NEW CLAUDE.md intro] Auto-loaded into every session and every worker: only what every reader applies — the dispatch form (rule 11), command
  new-> [S2.2 NEW CLAUDE.md intro] hygiene, worker duties, language. A worker's own rules are `.claude/agents/<role>.md` and its dispatch. The
  new-> [S2.2 NEW CLAUDE.md intro] coordinator's rules are not here: the SessionStart line `COORDINATOR RULES:` names their files.
  new-> [S2.3 NEW heading + C7a move + C26 trimming move (CLAUDE.md Worker duties)] ## Worker duties
  new-> [S2.3 NEW heading + C7a move + C26 trimming move (CLAUDE.md Worker duties)] - A self-activating
  new-> [S2.3 NEW heading + C7a move + C26 trimming move (CLAUDE.md Worker duties)] - A worker trims run output before it enters its context (`-q`, a 30-line tail, `Read` with a limit over 400 lines, `Grep` instead of reading a whole
  new-> [S2.4 NEW heading] ## The dispatch form (rule 11)
  new-> [C20-C23 citation retargets (S2 item 4)] fan-out declares ownership per COORDINATOR.md rule 4 plus an optional maxConcurrent cap. The manifest is DECLARATIVE on reads and
  new-> [C20-C23 citation retargets (S2 item 4)] writing dispatch: owns/non-goals/handoff present and its witness scope named (COORDINATOR.md rule 4); (5) freshness — the spec's
  new-> [C20-C23 citation retargets (S2 item 4)] | f | a dispatch to builder, or any dispatch whose `owns:` holds an absolute path (D-0022) | carries its manifest as HEADER LINES outside fences an
  new-> [C1 COORDINATOR head] # COORDINATOR.md — QA Factory development
  new-> [C1 COORDINATOR head] Read by the coordinator at start and after compaction (SessionStart line `COORDINATOR RULES:`); workers do not read it at boot — a role reads only the
  new-> [C2] The project's own rules, principles and layout live in PROJECT.md, read with this file (the `COORDINATOR RULES:` line):
  new-> [C4 Contents rows] | Tiers | COORDINATOR.md § Tiers |
  new-> [C4 Contents rows] | Recon → scout; builder; drafting | COORDINATOR.md § 1 + COORDINATOR.md § 2 + COORDINATOR.md § Rule 2 · drafting → designer |
  new-> [C4 Contents rows] | Witness; acceptance by witness | COORDINATOR.md § 2 |
  new-> [C4 Contents rows] | Batch canon | COORDINATOR.md § Rule 4 · witness scope and the BATCH CANON + docs/RUNBOOK.md § 7. CI на GitHub и BATCH CANON |
  new-> [C4 Contents rows] | Critic gate | COORDINATOR.md § 3 |
  new-> [C4 Contents rows] | Journal | COORDINATOR.md § Routing log |
  new-> [C4 Contents rows] | Cost gates | COORDINATOR.md § Rule 12 · Cost gates |
  new-> [C4 Contents rows] | Fix the class | COORDINATOR.md § 9 |
  new-> [C4 Contents rows] | Mechanisms | COORDINATOR.md § 10 |
  new-> [C4 Contents rows] | Language | CLAUDE.md § Язык |
  new-> [C4 Contents rows] | Decide vs ask; owner away | PROJECT.md § Что решать самому, что спрашивать у владельца + COORDINATOR.md § 11a |
  new-> [C4 Contents rows] | Degradation; Role ≠ tier | COORDINATOR.md § Role ≠ tier + COORDINATOR.md § Lead degradation |
  new-> [C7 enforcement sentence -> pointer] witness is a before/after screenshot or recording — a purely textual witness is insufficient
  new-> [C7 enforcement sentence -> pointer] (enforcement-file review rule: CLAUDE.md § Worker duties).
  new-> [S5.1/S5.3 NEW block] Before a designer dispatch the Lead MEASURES the brief's load-bearing facts by code (the owner's word 17.11.2026).
  new-> [S5.1/S5.3 NEW block] A load-bearing fact is any claim about the CURRENT repo or data that a requirement, an edge or a reader list rests
  new-> [S5.1/S5.3 NEW block] on: a file, function, constant, field, CLI flag or hook that exists, and its shape or value; a count (readers,
  new-> [S5.1/S5.3 NEW block] hits, sizes, lines); a test pin or anchor text; a data premise (PROJECT.md p.6(а)). Each fact goes into the
  new-> [S5.1/S5.3 NEW block] dispatch as a `facts:` header block, one line each: `<claim> | <command> | <verbatim result, at most 200 chars>`.
  new-> [S5.1/S5.3 NEW block] When the brief rests on none, the block is `facts: none -- <why>`. Opinions, intent and the owner's words are not
  new-> [S5.1/S5.3 NEW block] facts: they go in the brief.
  new-> [C20-C23 stub (COORDINATOR keeps a pointer)] ### Rule 11 · the dispatch form — CLAUDE.md § The dispatch form (rule 11)
  new-> [C26 Cost gates] FRESH worker carrying only the diff and the verdict; `tools/agent_budget.py` caps a worker (WARN 250K, STOP 400K; the remainder goes to a fresh wor
  new-> [C26 Cost gates] re-review carries only the fix diff and the verdict;
  new-> [S5.1/S5.3 NEW block] After a critic verdict `fit_with_fixes` on CODE, the Lead checks the fix round ITSELF only inside this border (the
  new-> [S5.1/S5.3 NEW block] owner's word 17.11.2026): the fix diff does exactly what the verdict's `fixes` prescribe and adds no new logic — no
  new-> [S5.1/S5.3 NEW block] new function, branch, state or write path. The base is the reviewed head: the bare token `reviewed:<sha>` is the
  new-> [S5.1/S5.3 NEW block] first token after the model label in the `description` of the critic's Agent call (for example `opus:
  new-> [S5.1/S5.3 NEW block] reviewed:69f6272f re-review …`; the hook builds the `delegated` notes from `description` and cuts them at 300
  new-> [S5.1/S5.3 NEW block] characters), written by the Lead from `git -C <tree> rev-parse HEAD` after COMMITTING the reviewed state — the Lead
  new-> [S5.1/S5.3 NEW block] commits the reviewed state before each critic dispatch, otherwise the fix round is `nobase`. Measured on `git -C
  new-> [S5.1/S5.3 NEW block] <tree> diff -U0 <sha> -- '*.py'` (added lines only; a line whose first non-blank character is `#` is not counted):
  new-> [S5.1/S5.3 NEW block] zero lines matching `^\+\s*(def |class |async def |if |elif |else\b|try:|except\b|finally:|for |while |match |case
  new-> [S5.1/S5.3 NEW block] |return\b|raise\b|break\b|continue\b|yield\b|with\b|assert\b|del\b)`, zero lines containing `\bif\b`, `\bfor\b`,
  new-> [S5.1/S5.3 NEW block] `\blambda\b`, `\band\b` or `\bor\b`, zero new files (`git diff --name-only --diff-filter=A <sha>` and `git ls-files
  new-> [S5.1/S5.3 NEW block] --others --exclude-standard`), zero added `add_argument(`, zero added write calls (`write_text|write_bytes|open\(.*
  new-> [S5.1/S5.3 NEW block] ['"][wax]|append_jsonl|\.write\(|json\.dump|\.unlink\(|os\.(remove|replace|rename|makedirs)|shutil\.|subprocess\.|\
  new-> [S5.1/S5.3 NEW block] .mkdir\(|\.touch\(`), no changed file other than `.py` and `.md`, and no line outside the owns the verdict
  new-> [S5.1/S5.3 NEW block] reviewed. Inside the border the Lead walks the fix diff by the critic's standing questions —
  new-> [S5.1/S5.3 NEW block] `.claude/agents/critic.md` rule 22, Q1-Q12 — one line per question, plus one line per fix (`fixed: <where>` / `not
  new-> [S5.1/S5.3 NEW block] fixed` → another fix round); a new dict entry used as a dispatch table is caught only by this walk (Q1, Q3). The
  new-> [S5.1/S5.3 NEW block] `accepted` notes carry `fixes checked by Lead: <verdict path>, border 0`. Outside the border (any count above
  new-> [S5.1/S5.3 NEW block] zero), with no `reviewed:` token (absent or cut) or a base that is not an ancestor of HEAD, when the verdict was
  new-> [S5.1/S5.3 NEW block] `blocker`, when a fix cannot be matched to its verdict line, or when the acceptor is not strictly above the
  new-> [S5.1/S5.3 NEW block] builder's tier (Role ≠ tier), a critic re-review carries only the fix diff and the verdict, and its dispatch names
  new-> [S5.1/S5.3 NEW block] its case: `re-review: logic|nobase|blocker|unmatched|tier`. Plans keep PROJECT.md new idea, step 6.
  new-> [C26 Cost gates] the Lead compacts by PROJECT.md § Сессия форджа, a stage
  new-> [C27 R13-g + S5.2] | g | the parts of one topic | ONE critic pass per TOPIC, not one per part (Cost gates, rule 12); a topic holds at most 4 nodes (the owner's word 1
  new-> [P1] - **правила работы над фабрикой** — этот файл и `COORDINATOR.md` (воркерский блок — `CLAUDE.md`): кто что
  new-> [P2] Этот файл читает координатор каждой сессии при старте и после сжатия (строка `COORDINATOR RULES:`); воркеры его при старте не читают, поэтому в нём то
  new-> [P3] | Язык → `CLAUDE.md` § Язык | какой язык где |
  new-> [P3] | Все темы → `COORDINATOR.md` § Contents | карта «тема → где читать» |
  new-> [P4 + COORDINATOR row] | `docs/OWNER_PRINCIPLES.md` | полный текст принципов владельца P1–P31 (индекс — `docs/OWNER_PRINCIPLES_INDEX.md`, читается по строке `COORDINATOR RUL
  new-> [P4 + COORDINATOR row] | `COORDINATOR.md` | правила координатора: маршрутизация, журнал, роли и деградация, Cost gates, карта тем; читается по строке `COORDINATOR RULES:` |
  new-> [P5] читается по строке `COORDINATOR RULES:`.
  new-> [P6 + F3 sentence] замена текста правил для того, кто пишет код. Задача критику (дифф или план), которая трогает `ai-packages/qa-factory/`,
  new-> [P6 + F3 sentence] несёт в «given» `design/architecture.md` и `design/factory-rules.md`: индексы в воркеров больше не грузятся.
  new-> [P7-P10] (правило 3 `COORDINATOR.md`), приёмка проверяет не только то, что края названы, но и то, что каждый
  new-> [P7-P10] (два прохода, правило 1 `COORDINATOR.md`).
  new-> [P7-P10] 8. **Код, затем критик кода** (правило 3 `COORDINATOR.md`, один проход на тему).
  new-> [P12] доказательства»); перенос подтверждает **человек**, не агент сам. **Остатков в идеале нет вовсе**: минорные замечания критика не откладываются стро
  new-> [P12] шесть; лимиты откатываются в понедельник вечером (владелец, 16.11.2026). Критик кода — один на тему, не на узел (до 4 узлов: R13-g).
  new-> [P16] владельцу (правило 11a в `COORDINATOR.md`): толкование замысла — не техническое решение.
PASS k1 -- unlisted diff lines=0, listed rows with no diff line=[], old lines lost=38, new lines gained=76
PASS k2 -- 19 keys present in 5 files
PASS k2b PROJECT.md key with outer backticks
PASS k3 -- no ^@ line=True, no 'read COORDINATOR'=True
k4 sizes: CLAUDE.md=14428 bytes, COORDINATOR.md=43785 bytes (PROJECT.md=34998, AGENTS.md=24103)
PASS k4 -- CLAUDE.md < 20000: True; COORDINATOR.md < 60000: True
PASS k5 -- 0 stale hits in 23 section-4.1 A files (positive control below)
k5 positive control on base blobs (PROJECT.md, builder.md, RUNBOOK.md): 11 hits (must be > 0)
PASS k5-control
NEGATIVE CONTROL (COORDINATOR.md copy without the '## Lead degradation' heading): FAIL -- [('COORDINATOR.md', '## Lead degradation')]
PASS negative-control (expected FAIL detected)
OVERALL: PASS
```

### Full source of card_a_check.py
```python
"""Card A DOC-DISPATCH witness (t-1233). Scratch file, never committed.

Usage: python -B card_a_check.py --base origin/main
Keys k1-k5 are quoted verbatim from Card A of docs/tasks/specs/20261117-worker-boot-and-round-rules-spec-r2.md.
Whitespace in presence keys is normalised (a key may wrap across a soft line break).
"""
import argparse
import re
import subprocess
import sys
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8")
W = "C:/QAFactory/forge-repo/.claude/worktrees/wb-int"
ap = argparse.ArgumentParser()
ap.add_argument("--base", default="origin/main")
args = ap.parse_args()


def show(path):
    return subprocess.run(["git", "-C", W, "show", args.base + ":" + path], capture_output=True, check=True).stdout.decode("utf-8")


def rd(path):
    return open(W + "/" + path, encoding="utf-8", newline="").read().replace("\r\n", "\n")


def norm(t):
    return re.sub(r"\s+", " ", t)


RESULTS = {}


def report(key, ok, detail=""):
    RESULTS[key] = ok
    print(("PASS " if ok else "FAIL ") + key + (" -- " + detail if detail else ""))


# ------------------------------------------------------------------ k1
MARK = re.compile(r"^[\s|:\-`]*$")


def k1_lines(t):
    out = []
    for l in t.split("\n"):
        if len(l) < 8 or MARK.match(l) or l.lstrip().startswith("```"):
            continue
        out.append(l)
    return out


# edited-lines groups: (section 3 row, [regexes matching old or new lines of that edit])
GROUPS = [
    ("S2.2 NEW CLAUDE.md intro", [r"^Auto-loaded into every session and every worker", r"^hygiene, worker duties, language\.", r"^coordinator's rules are not here"]),
    ("S2.3 NEW heading + C7a move + C26 trimming move (CLAUDE.md Worker duties)", [r"^## Worker duties$", r"^- A self-activating$", r"^- A worker trims run output"]),
    ("S2.4 NEW heading", [r"^## The dispatch form \(rule 11\)$"]),
    ("C20-C23 citation retargets (S2 item 4)", [r"fan-out declares ownership per", r"witness scope named \(", r"\| f \| a dispatch to builder"]),
    ("C1 COORDINATOR head", [r"^# COORDINATOR\.md", r"^Read by the coordinator at start"]),
    ("C2", [r"^The project's own rules", r"^@PROJECT\.md"]),
    ("C3 (@ lines deleted)", [r"^@docs/"]),
    ("C4 Contents rows", [r"^\| (Tiers|Recon|Witness|Batch canon|Critic gate|Journal|Cost gates|Fix the class|Mechanisms|Language|Decide vs ask|Degradation)"]),
    ("C7 enforcement sentence -> pointer", [r"witness is a before/after screenshot", r"enforcement-file review rule: CLAUDE\.md"]),
    ("C20-C23 stub (COORDINATOR keeps a pointer)", [r"^### Rule 11 . the dispatch form"]),
    ("C26 Cost gates", [r"FRESH worker carrying only the diff", r"^   re-review carries only the fix diff and the verdict;", r"^   the Lead compacts by PROJECT\.md"]),
    ("C27 R13-g + S5.2", [r"\| g \| the parts of one topic"]),
    ("C35 point 3 tail replaced by the cwd bullet", [r"why and how to recover: PROJECT\.md"]),
    ("P1", [r"правила работы над фабрикой"]),
    ("P2", [r"Этот файл читает"]),
    ("P3", [r"^\| Язык", r"Все темы"]),
    ("P4 + COORDINATOR row", [r"docs/OWNER_PRINCIPLES\.md", r"^\| `COORDINATOR\.md` \|"]),
    ("P5", [r"^(импорт из `CLAUDE\.md`\.|читается по строке `COORDINATOR RULES:`\.)$"]),
    ("P6 + F3 sentence", [r"замена текста правил для того", r"несёт в «given» `design/architecture"]),
    ("P7-P10", [r"правило 3 `(CLAUDE|COORDINATOR)\.md`", r"правило 1 `(CLAUDE|COORDINATOR)\.md`"]),
    ("P12", [r"Остатков в идеале нет вовсе", r"Критик кода — один на тему"]),
    ("P16", [r"^владельцу \(правило 11a"]),
]

old_text = show("CLAUDE.md") + "\n" + show("PROJECT.md")
new_claude, new_coord, new_proj = rd("CLAUDE.md"), rd("COORDINATOR.md"), rd("PROJECT.md")
old_c = Counter(k1_lines(old_text))
new_c = Counter(k1_lines(new_claude + "\n" + new_coord + "\n" + new_proj))
miss, extra = old_c - new_c, new_c - old_c

# NEW blocks of S5.1 and S5.3: whole line ranges of the new COORDINATOR.md, bounded by anchors
exempt = set()
cl = new_coord.split("\n")


def region(start_pat, end_pat):
    s = next(i for i, l in enumerate(cl) if re.search(start_pat, l))
    e = next(i for i in range(s, len(cl)) if re.search(end_pat, cl[i]))
    for l in cl[s:e + 1]:
        exempt.add(l)


region(r"^   Before a designer dispatch the Lead MEASURES", r"facts: they go in the brief\.$")
region(r"^   After a critic verdict `fit_with_fixes`", r"Plans keep PROJECT\.md new idea, step 6\.$")

hits = Counter()
unlisted = []
listing = []
for tag, cnt in (("old->", miss), ("new->", extra)):
    for l, c in cnt.items():
        if l in exempt:
            listing.append((tag, "S5.1/S5.3 NEW block", l))
            hits["S5.1/S5.3 NEW block"] += 1
            continue
        row = None
        for name, pats in GROUPS:
            if any(re.search(p, l) for p in pats):
                row = name
                break
        if row is None:
            unlisted.append((tag, l))
        else:
            hits[row] += 1
            listing.append((tag, row, l))
phantom = [n for n, _ in GROUPS if hits[n] == 0]
print("k1 edited-lines list (every old line lost / new line gained, with its section 3 row):")
for tag, row, l in listing:
    print("  %s [%s] %s" % (tag, row, l[:150].strip()))
report("k1", not unlisted and not phantom, "unlisted diff lines=%d, listed rows with no diff line=%s, old lines lost=%d, new lines gained=%d" % (len(unlisted), phantom, sum(miss.values()), sum(extra.values())))
for u in unlisted:
    print("  UNLISTED", u[0], u[1][:160])

# ------------------------------------------------------------------ k2
K2 = {
    "CLAUDE.md": ["## Command hygiene (permission hygiene)", "`COORDINATOR RULES:`", "## Язык", "## Worker duties",
                  "11. DoD in every dispatch (DoD-in-every-dispatch rule)", "DOC-DISPATCH WITNESS:", "a 30-line tail"],
    "COORDINATOR.md": ["## Role ≠ tier", "## Lead degradation", "## Routing log — logs/journal/<dev>.jsonl", "### Rule 12 · Cost gates",
                       "fixes checked by Lead:", "at most 4 nodes", "`facts:`", "rule 22, Q1-Q12"],
    ".claude/agents/designer.md": ["## Revision rN", "40,000 bytes"],
    "docs/SIBLING_MAP.md": ["owner word pending"],
    "PROJECT.md": ["design/architecture.md` и `design/factory-rules.md"],
}


def check_k2(texts):
    bad = []
    for f, keys in K2.items():
        t = norm(texts[f])
        for k in keys:
            if norm(k) not in t:
                bad.append((f, k))
    return bad


texts = {f: rd(f) for f in K2}
bad = check_k2(texts)
report("k2", not bad, "missing=%s" % bad if bad else "%d keys present in %d files" % (sum(len(v) for v in K2.values()), len(K2)))
wide = "`design/architecture.md` и `design/factory-rules.md`" in norm(texts["PROJECT.md"])
report("k2b PROJECT.md key with outer backticks", wide)

# ------------------------------------------------------------------ k3
no_at = not re.search(r"(?m)^@", new_claude)
no_read = "read coordinator" not in new_claude.lower()
report("k3", no_at and no_read, "no ^@ line=%s, no 'read COORDINATOR'=%s" % (no_at, no_read))

# ------------------------------------------------------------------ k4
import os
sz_c = os.path.getsize(W + "/CLAUDE.md")
sz_o = os.path.getsize(W + "/COORDINATOR.md")
print("k4 sizes: CLAUDE.md=%d bytes, COORDINATOR.md=%d bytes (PROJECT.md=%d, AGENTS.md=%d)" % (sz_c, sz_o, os.path.getsize(W + "/PROJECT.md"), os.path.getsize(W + "/AGENTS.md")))
report("k4", sz_c < 20000 and sz_o < 60000, "CLAUDE.md < 20000: %s; COORDINATOR.md < 60000: %s" % (sz_c < 20000, sz_o < 60000))

# ------------------------------------------------------------------ k5
A_FILES = [
    ".claude/agents/critic.md", ".claude/agents/designer.md", ".claude/agents/builder.md", ".claude/agents/judge.md",
    ".claude/skills/boot-diet/SKILL.md", ".claude/skills/session-handoff/SKILL.md", ".claude/skills/permission-audit/SKILL.md",
    ".claude/skills/scout-exam-gen/SKILL.md", "PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md", "PROCESS/JUDGE_CALIBRATION_PROTOCOL.md",
    "PROCESS/LEAD_RANKING_EXAM.md", "PROCESS/PATCH_PROTOCOL.md", "SYSTEM_PROMPT.md", "DELEGATION_TABLE.md", "delegation.config.yaml",
    "README.md", "BOOT.md", "docs/SIBLING_MAP.md", "docs/RUNBOOK.md", "docs/CLAUDE_HOST_ADAPTATIONS_FULL.md", "docs/TESTING.md",
    "gateway/config.template.yaml", "PROJECT.md",
]
K5 = [re.compile(r"CLAUDE\.md(?:'s)?`?\s+(?:routing\s+)?rules?\s+(?!11\b)\d"),
      re.compile(r"правил\w*\s+(?!11\b)\d+\w?\s+(?:в\s+)?`?CLAUDE\.md")]
stale = []
for f in A_FILES:
    t = rd(f)
    for rx in K5:
        for m in rx.finditer(t):
            stale.append((f, t.count("\n", 0, m.start()) + 1, m.group(0).replace("\n", " ")))
report("k5", not stale, "stale hits=%s" % stale if stale else "0 stale hits in %d section-4.1 A files (positive control below)" % len(A_FILES))
# positive control of the k5 regexes: the old CLAUDE.md-citing forms must be found in the base blobs
pc = sum(len(rx.findall(show(f))) for f in ["PROJECT.md", ".claude/agents/builder.md", "docs/RUNBOOK.md"] for rx in K5)
print("k5 positive control on base blobs (PROJECT.md, builder.md, RUNBOOK.md): %d hits (must be > 0)" % pc)
report("k5-control", pc > 0)

# ------------------------------------------------------------------ negative control
neg = dict(texts)
neg["COORDINATOR.md"] = texts["COORDINATOR.md"].replace("## Lead degradation", "")
nbad = check_k2(neg)
neg_ok = ("COORDINATOR.md", "## Lead degradation") in nbad
print("NEGATIVE CONTROL (COORDINATOR.md copy without the '## Lead degradation' heading): %s -- %s" % ("FAIL" if nbad else "PASS", nbad))
report("negative-control (expected FAIL detected)", neg_ok)

all_ok = all(RESULTS.values())
print("OVERALL: " + ("PASS" if all_ok else "FAIL"))
sys.exit(0 if all_ok else 1)
```

## Edited lines outside CLAUDE.md/COORDINATOR.md/PROJECT.md/AGENTS.md (git diff -U0, CR stripped)
```diff
diff --git a/.claude/agents/builder.md b/.claude/agents/builder.md
--- a/.claude/agents/builder.md
+++ b/.claude/agents/builder.md
-   witness is CLAUDE.md rule 12's one run (Cost gates), of rule 4's scope, repeated once only if code changed after it
+   witness is CLAUDE.md § Worker duties' one run, of the `docs/TESTING.md` «Что запускать по своей правке» scope, repeated once only if code changed after it
-   `tools/architecture_gate.py` (CLAUDE.md rule 10). Mechanism paths (`MECHANISM_PREFIXES` of `tools/mechanism_gate.py`) stay
-   STAGED and are listed in the report: the Lead commits them (CLAUDE.md rule 2). A task that edits `CLAUDE.md`, `PROJECT.md`
+   `tools/architecture_gate.py` (COORDINATOR.md rule 10). Mechanism paths (`MECHANISM_PREFIXES` of `tools/mechanism_gate.py`) stay
+   STAGED and are listed in the report: the Lead commits them (CLAUDE.md § Worker duties). A task that edits `CLAUDE.md`, `COORDINATOR.md`, `PROJECT.md`
diff --git a/.claude/agents/critic.md b/.claude/agents/critic.md
--- a/.claude/agents/critic.md
+++ b/.claude/agents/critic.md
-21. The two layers of a diff gate (CLAUDE.md rule 3, the two-layer review rule):
+21. The two layers of a diff gate (COORDINATOR.md rule 3, the two-layer review rule):
-   Q4. **Class-wide completeness** (rule 9, FR-54): the SIBLING_MAP axes and the neighbours in the same artifact. A sibling is fixed in the same round; it leaves only by CLAUDE.md rule 9's exit (the rare case). An analog outside the node's `owns` but inside t
+   Q4. **Class-wide completeness** (COORDINATOR.md rule 9, FR-54): the SIBLING_MAP axes and the neighbours in the same artifact. A sibling is fixed in the same round; it leaves only by COORDINATOR.md rule 9's exit (the rare case). An analog outside the node's
-24. The plan gate (critic on a plan or on a dispatch draft; CLAUDE.md rule 3): answer Q13 below and Q4, Q6, Q12 and Q10's VARIETY sentence of
+24. The plan gate (critic on a plan or on a dispatch draft; COORDINATOR.md rule 3): answer Q13 below and Q4, Q6, Q12 and Q10's VARIETY sentence of
diff --git a/.claude/agents/designer.md b/.claude/agents/designer.md
--- a/.claude/agents/designer.md
+++ b/.claude/agents/designer.md
-tools: Read, Glob, Grep, Write
+tools: Read, Glob, Grep, Write, Edit
-   that its own requirements create is a spec defect. (CLAUDE.md rule 2, D-0021.) Every named edge also states
+   that its own requirements create is a spec defect. (COORDINATOR.md rule 2, D-0021.) Every named edge also states
-   A spec that touches `ai-packages/qa-factory/` names in §1 the AR-n invariants of `design/architecture.md` it touches, with the change check each one demands written into the DoD, and names, for every check the spec adds or alters, the owner it serves — 
+   A spec that touches `ai-packages/qa-factory/` names in §1 the AR-n invariants of `design/architecture.md` it touches, with the change check each one demands written into the DoD, and names, for every check the spec adds or alters, the owner it serves — 
-   hygiene point 6). Report noticed analogs/contradictions in the
+   hygiene point 6). Facts in `facts:` are the Lead's measurement and may be cited with their command; a
+   load-bearing fact the draft adds is measured by the designer the same way and listed in the trail; a
+   fact the designer cannot measure (no shell) is labelled `estimate` with the command the Lead runs.
+   Report noticed analogs/contradictions in the
-   limits any Write to that single path, and `tools` carries Write
+   limits any Write and Edit to that single path, and `tools` carries Write and Edit
+8. Size and fix rounds (the owner's word 17.11.2026, «если это не ухудшит качество»). The draft file is at most 40,000
+   bytes on disk (`python -B -c "import os,sys;print(os.path.getsize(sys.argv[1]))" <path>`). A draft that will not fit
+   returns `decomposable: <parts by disjoint owns>` before writing past the cap. Edges, invariants, readers, forks and the
+   trail are never trimmed to fit. A FIX ROUND (its `handoff:` names the earlier draft) EDITS that file in place: (a) a
+   `## Revision rN` block at the top, one line per finding or decision: `<id> -> change -> section`; (b) every builder card
+   it touches is rewritten WHOLE in place; (c) untouched sections stay byte-identical; (d) a revision touching more than half
+   of the cards, or §1, is a full rewrite. The file at `handoff:` is always the complete current spec: a builder reads one
+   document and never merges two.
diff --git a/.claude/agents/judge.md b/.claude/agents/judge.md
--- a/.claude/agents/judge.md
+++ b/.claude/agents/judge.md
-description: Judge (Sonnet, the subscription form of leaf-class acceptance, CLAUDE.md rule 13). Two tasks share one role, and the CALL SHAPE decides which applies, not the judge's own choice: comparing two answers to the same task (verdict EQUIVALENT/WORSE on
+description: Judge (Sonnet, the subscription form of leaf-class acceptance, COORDINATOR.md rule 13). Two tasks share one role, and the CALL SHAPE decides which applies, not the judge's own choice: comparing two answers to the same task (verdict EQUIVALENT/WOR
-CLAUDE.md), invisibly to whoever relies on you.
+COORDINATOR.md), invisibly to whoever relies on you.
diff --git a/.claude/skills/boot-diet/SKILL.md b/.claude/skills/boot-diet/SKILL.md
--- a/.claude/skills/boot-diet/SKILL.md
+++ b/.claude/skills/boot-diet/SKILL.md
-Boot context is a paid resource (CLAUDE.md, boot-context-is-expensive
+Boot context is a paid resource (COORDINATOR.md, boot-context-is-expensive
-   CLAUDE.md pulls in by `@import` lines — the hook's BOOT BUDGET block
-   (`python tools/session_context.py`) prints them under CLAUDE.md and
+   the `COORDINATOR RULES:` line names — the hook's BOOT BUDGET block
+   (`python tools/session_context.py`) prints them and
-   walk EVERY file the boot loads (CLAUDE.md and its imports,
+   walk EVERY file the boot loads (CLAUDE.md and the files the `COORDINATOR RULES:` line names,
-   put "deep cuts" (operational homes: CLAUDE.md, SYSTEM_PROMPT.md,
+   put "deep cuts" (operational homes: CLAUDE.md, COORDINATOR.md, SYSTEM_PROMPT.md,
-   that isn't auto-loaded gets silently skipped (CLAUDE.md's opening
+   that isn't auto-loaded gets silently skipped (COORDINATOR.md's opening
-   mechanism paths needs CLAUDE.md rule 10's axis block, or an
+   mechanism paths needs COORDINATOR.md rule 10's axis block, or an
-6. Импорт `@` — только из `CLAUDE.md`, один уровень (счётчик бюджета вложенных не видит).
+6. `CLAUDE.md` не импортирует ничего: импорт грузится в каждого воркера; текст координатора — `COORDINATOR.md`.
diff --git a/.claude/skills/permission-audit/SKILL.md b/.claude/skills/permission-audit/SKILL.md
--- a/.claude/skills/permission-audit/SKILL.md
+++ b/.claude/skills/permission-audit/SKILL.md
-   (the gate refuses it itself, with its door); poll loops (a cost finding, CLAUDE.md rule 7, not a hygiene one).
+   (the gate refuses it itself, with its door); poll loops (a cost finding, COORDINATOR.md rule 7, not a hygiene one).
diff --git a/.claude/skills/scout-exam-gen/SKILL.md b/.claude/skills/scout-exam-gen/SKILL.md
--- a/.claude/skills/scout-exam-gen/SKILL.md
+++ b/.claude/skills/scout-exam-gen/SKILL.md
-   (see the trail-based acceptance rule in CLAUDE.md) shows it read
+   (see the trail-based acceptance rule in COORDINATOR.md) shows it read
diff --git a/.claude/skills/session-handoff/SKILL.md b/.claude/skills/session-handoff/SKILL.md
--- a/.claude/skills/session-handoff/SKILL.md
+++ b/.claude/skills/session-handoff/SKILL.md
-   the journal's last event (CLAUDE.md, "Lead degradation"). This
+   the journal's last event (COORDINATOR.md, "Lead degradation"). This
-   BOOT.md's sequence lists. Compare against the last measurement (the
+   BOOT.md's sequence lists and every file the `COORDINATOR RULES:` line names. Compare against the last measurement (the
diff --git a/BOOT.md b/BOOT.md
--- a/BOOT.md
+++ b/BOOT.md
-Note: CLAUDE.md (the routing policy) auto-loads into every session on
-its own — that auto-load is NOT a boot. Full state recovery is this
-sequence, run on the operator's request ("restore context from
+Note: CLAUDE.md (the worker block: dispatch form, command hygiene, worker
+duties, language) auto-loads into every session on its own — that auto-load
+is NOT a boot. The coordinator's rules are named by the SessionStart line
+`COORDINATOR RULES:`. Full state recovery is this sequence, run on the operator's request ("restore context from
diff --git a/DELEGATION_TABLE.md b/DELEGATION_TABLE.md
--- a/DELEGATION_TABLE.md
+++ b/DELEGATION_TABLE.md
-your own usage as you delegate (see CLAUDE.md rules 1-13 for how a
-task gets routed; this table is what "which tier" resolves against).
+your own usage as you delegate (see COORDINATOR.md rules 1-13 for how a
+task gets routed; rule 11: CLAUDE.md; this table is what "which tier" resolves against).
-Flat delegation (CLAUDE.md): workers never spawn workers. Parallelism
+Flat delegation (COORDINATOR.md): workers never spawn workers. Parallelism
diff --git a/PROCESS/JUDGE_CALIBRATION_PROTOCOL.md b/PROCESS/JUDGE_CALIBRATION_PROTOCOL.md
--- a/PROCESS/JUDGE_CALIBRATION_PROTOCOL.md
+++ b/PROCESS/JUDGE_CALIBRATION_PROTOCOL.md
-   CLAUDE.md's rule 13 recognizes a SECOND legitimate judge form
+   COORDINATOR.md's rule 13 recognizes a SECOND legitimate judge form
-   point" CLAUDE.md's rule 13 requires before either judge form is
+   point" COORDINATOR.md's rule 13 requires before either judge form is
diff --git a/PROCESS/LEAD_RANKING_EXAM.md b/PROCESS/LEAD_RANKING_EXAM.md
--- a/PROCESS/LEAD_RANKING_EXAM.md
+++ b/PROCESS/LEAD_RANKING_EXAM.md
-2. Claude Code subagents auto-load CLAUDE.md, so the policy is
-   already in their context. This is a FAIR condition: the exam
+2. The dispatch attaches COORDINATOR.md whole, so the policy is
+   in the candidate's context. This is a FAIR condition: the exam
diff --git a/PROCESS/PATCH_PROTOCOL.md b/PROCESS/PATCH_PROTOCOL.md
--- a/PROCESS/PATCH_PROTOCOL.md
+++ b/PROCESS/PATCH_PROTOCOL.md
-A patch touching a policy carrier this kit ships (CLAUDE.md, an
+A patch touching a policy carrier this kit ships (CLAUDE.md, COORDINATOR.md, an
diff --git a/PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md b/PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md
--- a/PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md
+++ b/PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md
-   CUMULATIVE SUBCASE (R13-g of CLAUDE.md): ONE critic pass per TOPIC,
+   CUMULATIVE SUBCASE (R13-g of COORDINATOR.md): ONE critic pass per TOPIC,
-   semantic call for the calibrating Lead).
+   semantic call for the calibrating Lead). TOPIC CAP (R13-g, the owner's word 17.11.2026): a topic holds at most 4
+   nodes — count the nodes per critic `delegated` (`node` field, then notes); a critic pass that covers 5 or more
+   nodes of one topic is a Cost-gates finding.
-   CLAUDE.md Role != tier).
+   COORDINATOR.md Role != tier).
-   a phantom event.
+   a phantom event. The first Task/Agent call of a main session after a start or compaction follows a Read of
+   `COORDINATOR.md` in the same transcript (SessionStart line `COORDINATOR RULES:`); a call before it is a finding
+   (the read itself is on discipline).
-   CLAUDE.md rule 9). Every window finding that names a CLASS (a
+   COORDINATOR.md rule 9). Every window finding that names a CLASS (a
-    files BOOT.md's boot sequence reads, plus CLAUDE.md and
+    files BOOT.md's boot sequence reads, plus CLAUDE.md, COORDINATOR.md and
-    graph of the same size costs under half of that. The carrier of the
+    graph of the same size costs under half of that; (g) the Lead's fix check inside the border (COORDINATOR.md,
+    Cost gates): (i) a critic re-review dispatch naming no case (`re-review: logic|nobase|blocker|unmatched|tier`);
+    (ii) an `accepted` after a `fit_with_fixes` verdict with neither `fixes checked by Lead` nor a re-review; (iii) a
+    sample re-run of the border counter on the commits of (i) and (ii) — each a finding. The carrier of the
-    CLAUDE.md reads 'not used in this deployment': no judge is bound,
+    COORDINATOR.md reads 'not used in this deployment': no judge is bound,
-    violation, CLAUDE.md's "Role != tier"). `tools/journal_validator.py`
+    violation, COORDINATOR.md's "Role != tier"). `tools/journal_validator.py`
+    (e) Designer drafts (designer.md rule 8, the owner's word 17.11.2026): a draft file over 40,000 bytes on disk
+    (`python -B -c "import os,sys;print(os.path.getsize(sys.argv[1]))" <path>`); a fix round (its `handoff:` names an
+    earlier draft) whose `git diff --stat` touches more than half of the cards or §1 without being a full rewrite — each
+    a finding.
-    CLAUDE.md rule 4a; PROJECT.md «Командная работа»; `docs/TEAMWORK.md`).**
+    COORDINATOR.md rule 4a; PROJECT.md «Командная работа»; `docs/TEAMWORK.md`).**
-    (h) Boot form (boot-by-topic, FG7-51): sample CLAUDE.md and PROJECT.md for a rule sentence restated outside its home (topic map), a section over 50 lines without a table, a `##` heading of the boot that no TOC row routes to — each a finding; on discipli
-    (i) Standing documents (PROJECT.md «Лишних документов нет», the owner's word 17.11.2026): sample the role files, CLAUDE.md, PROJECT.md and the window's new specs for a sentence that sends a role to read, every time, a file that is not
+    (h) Boot form (boot-by-topic, FG7-51): sample CLAUDE.md, COORDINATOR.md and PROJECT.md for a rule sentence restated outside its home (topic map), a section over 50 lines without a table, a `##` heading of the boot that no TOC row routes to — each a find
+    (i) Standing documents (PROJECT.md «Лишних документов нет», the owner's word 17.11.2026): sample the role files, CLAUDE.md, COORDINATOR.md, PROJECT.md and the window's new specs for a sentence that sends a role to read, every time, a 
-46. **Task id race: dispatch id differs from its journal line (F6-58, same spec §C.7 (c); CLAUDE.md, Routing log: id bands).** For each `delegated` in the window, read the worker's dispatch through `dispatch_manifest.handoff_mentions(section_cut(prompt))` —
+46. **Task id race: dispatch id differs from its journal line (F6-58, same spec §C.7 (c); COORDINATOR.md, Routing log: id bands).** For each `delegated` in the window, read the worker's dispatch through `dispatch_manifest.handoff_mentions(section_cut(prompt)
-48. **Journal by code, one merge road, test volume (coordinator offload, spec `docs/tasks/specs/20261114-coordinator-offload-spec-r2.md` §6.4, §7 M2-M7; the owner's word 14.11.2026; CLAUDE.md Routing log, rule 12, hygiene pt.5).** Mechanism: `tools/journal_
+48. **Journal by code, one merge road, test volume (coordinator offload, spec `docs/tasks/specs/20261114-coordinator-offload-spec-r2.md` §6.4, §7 M2-M7; the owner's word 14.11.2026; COORDINATOR.md Routing log, rule 12; CLAUDE.md hygiene pt.5).** Mechanism: 
diff --git a/README.md b/README.md
--- a/README.md
+++ b/README.md
-  the policy is `CLAUDE.md`, model bindings `delegation.config.yaml`, decisions `DECISIONS.md`,
+  the policy is `COORDINATOR.md` (worker block `CLAUDE.md`), model bindings `delegation.config.yaml`, decisions `DECISIONS.md`,
-   Codex users: read `AGENTS.md` (generated by `python tools/agents_md.py`, it inlines CLAUDE.md and its imports) and raise `project_doc_max_bytes` as its first lines say, otherwise Codex cuts the rules off at 32 KiB.
+   Codex users: read `AGENTS.md` (generated by `python tools/agents_md.py`, it inlines CLAUDE.md and the coordinator files named by the `COORDINATOR RULES:` line) and raise `project_doc_max_bytes` as its first lines say, otherwise Codex cuts the rules off at 
diff --git a/SYSTEM_PROMPT.md b/SYSTEM_PROMPT.md
--- a/SYSTEM_PROMPT.md
+++ b/SYSTEM_PROMPT.md
-- Fix the class, not the instance: CLAUDE.md rule 9 is the rule text
+- Fix the class, not the instance: COORDINATOR.md rule 9 is the rule text
diff --git a/delegation.config.yaml b/delegation.config.yaml
--- a/delegation.config.yaml
+++ b/delegation.config.yaml
-  # Mandatory acceptance gate for builder-class diffs (CLAUDE.md rule 3).
+  # Mandatory acceptance gate for builder-class diffs (COORDINATOR.md rule 3).
-  # Implementation from a written spec (CLAUDE.md rule 2).
+  # Implementation from a written spec (COORDINATOR.md rule 2).
-  # Recon: repo search, file reading, context gathering (CLAUDE.md rule 1).
+  # Recon: repo search, file reading, context gathering (COORDINATOR.md rule 1).
diff --git a/docs/CLAUDE_HOST_ADAPTATIONS_FULL.md b/docs/CLAUDE_HOST_ADAPTATIONS_FULL.md
--- a/docs/CLAUDE_HOST_ADAPTATIONS_FULL.md
+++ b/docs/CLAUDE_HOST_ADAPTATIONS_FULL.md
-`.claude/agents/critic.md` rule 22 and of adaptation 6 is `CLAUDE.md` rule 12, Cost gates; this file keeps for them only
-the reason. Adaptation 7 is kept verbatim as it stood at commit `16238d26`; its pointer in `CLAUDE.md` rule 4a and this text are a
+`.claude/agents/critic.md` rule 22 and of adaptation 6 is `COORDINATOR.md` rule 12, Cost gates; this file keeps for them only
+the reason. Adaptation 7 is kept verbatim as it stood at commit `16238d26`; its pointer in `COORDINATOR.md` rule 4a and this text are a
-6. Cost gates — the rule text is `CLAUDE.md` rule 12, Cost gates; here only why. D-0035 (the owner's word 07.10.2026): release
+6. Cost gates — the rule text is `COORDINATOR.md` rule 12, Cost gates; here only why. D-0035 (the owner's word 07.10.2026): release
diff --git a/docs/RUNBOOK.md b/docs/RUNBOOK.md
--- a/docs/RUNBOOK.md
+++ b/docs/RUNBOOK.md
-строка `canon wall time`, дописанные в `witness` последнего `accepted` пачки с меткой BATCH CANON (правило 4 `CLAUDE.md`). Что
+строка `canon wall time`, дописанные в `witness` последнего `accepted` пачки с меткой BATCH CANON (правило 4 `COORDINATOR.md`). Что
-Стоячее поручение сессии, которая ведёт прогон. Оно действует внутри правил этого репозитория (`CLAUDE.md`:
-маршрутизация, журнал, гигиена команд; `PROJECT.md`) и ничего из них не отменяет. Мандат в силе, когда владелец
+Стоячее поручение сессии, которая ведёт прогон. Оно действует внутри правил этого репозитория (`COORDINATOR.md`:
+маршрутизация, журнал; `CLAUDE.md`: гигиена команд; `PROJECT.md`) и ничего из них не отменяет. Мандат в силе, когда владелец
-9. **(i) Держит параллель полной** — правило очереди и предел писателей: `CLAUDE.md` rule 12, Cost gates (не больше 6 пишущих
+9. **(i) Держит параллель полной** — правило очереди и предел писателей: `COORDINATOR.md` rule 12, Cost gates (не больше 6 пишущих
-   узлов) и запускает всё, у чего готова спека, нет пересечения `owns` с живыми воркерами (правило 4 `CLAUDE.md`) и нет
+   узлов) и запускает всё, у чего готова спека, нет пересечения `owns` с живыми воркерами (правило 4 `COORDINATOR.md`) и нет
-адаптации хоста 6 `CLAUDE.md`, в `PROJECT.md` («Рабочий каталог шелла не меняется никогда») и в `.claude/agents/builder.md` rule 10.
+адаптации хоста 6 `COORDINATOR.md`, в `CLAUDE.md` («Рабочий каталог шелла не меняется никогда») и в `.claude/agents/builder.md` rule 10.
diff --git a/docs/SIBLING_MAP.md b/docs/SIBLING_MAP.md
--- a/docs/SIBLING_MAP.md
+++ b/docs/SIBLING_MAP.md
-The tool behind "fix the class, not the instance" (CLAUDE.md rule 9).
+The tool behind "fix the class, not the instance" (COORDINATOR.md rule 9).
-`.claude/agents/<role>.md` (duties, `tools:`, hand-back form), `docs/TESTING.md` «Что запускать по своей правке» (the builder's verification scope and the batch canon's content), `.claude/agents/critic.md` rules 21-24 (the critic re
-hygiene; cost gates in rule 12, Cost gates), `delegation.config.yaml` (the model binding), the exam instruments of axis 2.
+`.claude/agents/<role>.md` (duties, `tools:`, hand-back form), `docs/TESTING.md` «Что запускать по своей правке» (the builder's verification scope and the batch canon's content), `.claude/agents/critic.md` rules 21-24 (the critic re
+hygiene, worker duties), `delegation.config.yaml` (the model binding), the exam instruments of axis 2.
-| `.claude/agents/designer.md` | designer | duties, `tools:`, hand-back (5), edge invariant (CLAUDE.md rule 2 -> designer.md rule 1), one road (6) | owner; draft form → CLAUDE.md rule 11 (1); DoD scope → docs/TESTING.md «Что запускать по с
+| `.claude/agents/designer.md` | designer | duties, `tools:`, hand-back (5), edge invariant (COORDINATOR.md rule 2 -> designer.md rule 1), one road (6) | owner; draft form → CLAUDE.md rule 11 (1); DoD scope → docs/TESTING.md «Что запускать п
-| `CLAUDE.md` | all | routing rules 1-13, journal, Role ≠ tier, degradation, command hygiene; cost gates (rule 12); the cross-file topic map (§ Contents, one row per topic T1-T33 of the boot-by-topic spec) | owner; critic questions → `.claude/agents/crit
-| `docs/CLAUDE_HOST_ADAPTATIONS_FULL.md` | Lead | the reason of the clauses in rule 3 (critic gate) and rule 12 (Cost gates); the clause of rule 4a in full | reason only → critic.md rule 22, CLAUDE.md rule 12; rule 4a a trimmed ↔ full pair |
+| `CLAUDE.md` | all | the worker block: rule 11 (the dispatch form), command hygiene, worker duties, Язык | owner |
+| `COORDINATOR.md` | coordinator; a worker by the section its role file names | routing rules 1-10, 11a, 12, 13, journal, Role ≠ tier, degradation, Cost gates, the topic map (§ Contents) | owner (owner word pending: PROJECT.md «Лишних докумен
+| `docs/CLAUDE_HOST_ADAPTATIONS_FULL.md` | Lead | the reason of the clauses in rule 3 (critic gate) and rule 12 (Cost gates); the clause of rule 4a in full | reason only → critic.md rule 22, COORDINATOR.md rule 12; rule 4a a trimmed ↔ full pair |
-| `docs/OWNER_PRINCIPLES.md` | all | the owner's principles P1–P31, full text | owner; `docs/OWNER_PRINCIPLES_INDEX.md` is its generated index (machine copy), imported by CLAUDE.md |
+| `docs/OWNER_PRINCIPLES.md` | all | the owner's principles P1–P31, full text | owner; `docs/OWNER_PRINCIPLES_INDEX.md` is its generated index (machine copy), read via the `COORDINATOR RULES:` line |
-| `DELEGATION_TABLE.md` | Lead | assignment statuses | owner of statuses; routing → CLAUDE.md rules 1-13 |
+| `DELEGATION_TABLE.md` | Lead | assignment statuses | owner of statuses; routing → COORDINATOR.md rules 1-13 (rule 11: CLAUDE.md) |
-| `SYSTEM_PROMPT.md` | all | permanent principles | owner of principles; fix the class → CLAUDE.md rule 9 |
+| `SYSTEM_PROMPT.md` | all | permanent principles | owner of principles; fix the class → COORDINATOR.md rule 9 |
-| `docs/RUNBOOK.md` | night agent | night run 9.1 | procedure; owner of the branch-run recipe, the BATCH CANON procedure and the docker-fallback wording (§7); package fix → docs/TESTING.md «Что запускать по своей правке»; paralle
+| `docs/RUNBOOK.md` | night agent | night run 9.1 | procedure; owner of the branch-run recipe, the BATCH CANON procedure and the docker-fallback wording (§7); package fix → docs/TESTING.md «Что запускать по своей правке»; paralle
-| `docs/FACTORY_RULES_INDEX.md` | builder, critic | FR one-liners | generated |
-| `docs/ARCHITECTURE_INDEX.md` | builder, critic, designer | AR one-liners | generated |
+| `docs/FACTORY_RULES_INDEX.md` | coordinator | FR one-liners | generated |
+| `docs/ARCHITECTURE_INDEX.md` | coordinator; `tools/architecture_gate.py` by path | AR one-liners | generated |
-| `tools/dispatch_gate.py` | writers | DoD and manifest presence, `PARALLEL_CAP` | machine; the cap moves with CLAUDE.md rule 12 (Cost gates) and PROJECT.md «Командная работа» p. 12 |
+| `tools/dispatch_gate.py` | writers | DoD and manifest presence, `PARALLEL_CAP` | machine; the cap moves with COORDINATOR.md rule 12 (Cost gates) and PROJECT.md «Командная работа» p. 12 |
-| `tools/agent_budget.py` | workers | context cap | machine; the numbers move with CLAUDE.md rule 12 (Cost gates) |
+| `tools/agent_budget.py` | workers | context cap | machine; the numbers move with COORDINATOR.md rule 12 (Cost gates) |
diff --git a/docs/TESTING.md b/docs/TESTING.md
--- a/docs/TESTING.md
+++ b/docs/TESTING.md
-строки `test:` DoD узла (путь вне пакета — тестовый файл, который его судит, правило 4 `CLAUDE.md`); тронут
+строки `test:` DoD узла (путь вне пакета — тестовый файл, который его судит, правило 4 `COORDINATOR.md`); тронут
-против узла (правило 4 CLAUDE.md). CI на каждом MR остаётся регрессией за бесплатно. Тест из `SLOW_TESTS` идёт только в
+против узла (правило 4 COORDINATOR.md). CI на каждом MR остаётся регрессией за бесплатно. Тест из `SLOW_TESTS` идёт только в
diff --git a/gateway/config.template.yaml b/gateway/config.template.yaml
--- a/gateway/config.template.yaml
+++ b/gateway/config.template.yaml
-  # Mandatory acceptance gate for builder-class diffs (CLAUDE.md rule 3;
+  # Mandatory acceptance gate for builder-class diffs (COORDINATOR.md rule 3;
-  # Implementation from a written spec (CLAUDE.md rule 2;
+  # Implementation from a written spec (COORDINATOR.md rule 2;
-  # Recon: repo search, file reading, context gathering (CLAUDE.md
+  # Recon: repo search, file reading, context gathering (COORDINATOR.md
-  # supervised worker, not a rules-level function (CLAUDE.md's
+  # supervised worker, not a rules-level function (COORDINATOR.md's
```
