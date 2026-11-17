# Spec r2 t-1187: short worker boot (CLAUDE.md split) + fewer rounds — fix round after plan critic t-1174 (designer, 17.11.2026)

Status: DRAFT for Lead acceptance; a FULL spec (r1 `20261117-worker-boot-and-round-rules-spec.md` is superseded, not merged).
Base: origin/main **da47f648** (`.git/refs/remotes/origin/main` = `.git/refs/heads/main`, read 17.11.2026). Brief: Lead
t-1137 (owner 17.11.2026: «давай сделаем сейчас»; item 6 «ок»; item 7 «если это не ухудшит качество, то ок»; border of item 6;
facts before the designer «да, поднимаем»; topic cap «принимаю»). Lead decisions in force: r1 §9 F1(a)→ superseded by the
edges line (draft (d)), F2, F3, F4(a), F5 = copies, F6 40,000, F7, F8, F9, F10, F11 = 4, F12(a), F13(a), F14 = cite the critic
role file; B4 = the trimming sentence goes to the CLAUDE.md worker block. Forks in §10; none decided here.

Measurement limit: the designer has no shell (tools: Read, Glob, Grep, Write). Line numbers, presence and counts below were
re-read on da47f648 by Read/Grep. BYTE sizes were NOT re-measured: they are the critic's run at c75dd0c7 (t-1174 trail) plus
arithmetic, labelled "estimate"; the Lead re-measures them as `facts:` lines (commands in §12) and Card A (k4) measures them.

## Revision r2: verdict item -> change -> section

| t-1174 item | change | where |
|---|---|---|
| B1 deleted files | no card owns or is given a deleted file; C9-C12 reader = `docs/TESTING.md` «Что запускать по своей правке»; item-6 text cites `.claude/agents/critic.md` rule 22, Q1-Q12 (rule 24 Q13 is the plan gate) | §3, §5.1, §8 |
| B2 critic.md stale | critic.md in Card A owns (178, 198 ×2, 281); 286 stays valid under (d); critic reads rule 11 by auto-load under (d); the exam: instruments absent, precedent deviation line (F8') | §4.1, §8 A, §10 F8' |
| B3 F5 not carried | file-by-file copy table: why each fires in a builder, its import closure, how tests resolve it, when the Lead places it | §7 |
| B3 F14 | §5.1 rewritten | §5.1 |
| B3 F3 executor | Card A writes the PROJECT.md p.1 sentence | §3 P5, §8 A |
| B4 trimming duty | sentence moves to CLAUDE.md `## Worker duties`; worker-duty sweep of rules 1-13 enumerated | §2, §3 C26, §4.3 |
| B5 new main docs | (d) drafted: rule 11 stays in CLAUDE.md, no DISPATCH_RULES.md; COORDINATOR.md gets an axis-31 row "owner (owner word pending)" | §2, §8 A, §10 F1' |
| N1 border regex | F12(b)+lambda+and/or, comment lines excluded, dict-dispatch named as Q-walk only | §5.1, §10 F12' |
| N2 base sha | carrier `reviewed:<sha>` token; absent → re-review `nobase` | §5.1, §10 F16 |
| N3 k1 | multiplicity check, markup-only lines exempt | §8 A DoD |
| N4 branch mechanics | one integration worktree, builders commit nothing, two critic topics with the Lead's placement between | §7, §10 F15 |
| N5 CLAUDE_WARN | derived ceil(measured×1.15/100)×100 from Card A's size (≈17000, estimate) | §8 B1, §6 e5 |
| N6 readers/wording | readers block answers; S4 edge; wording "workers do not read these at boot"; F13 branch named with its positional invariant; K4/K8 unaffected (scout, critic fixtures) | §4.2, §5.3, §6, §8 |
| N7 stale numbers | corrected with carriers | §12 |
| N8 cost | post-split totals stated, next lever named | §9 |

## §1 Scope, invariants, owners

- Nothing under `ai-packages/qa-factory/` changes: no AR-n applies; `architecture:`/`judgment:` lines are not owed
  (`tools/architecture_gate.py` asks on package commits only). Forge MECHANISM commits: axis block (§9) and `tier: opus`.
- Forge invariants:
  - I-1 MOVE: every rule sentence of today's CLAUDE.md and PROJECT.md has exactly ONE home after the topic, word for word,
    except the edits listed in §3's last column and the new texts of §5.
  - I-2 ONE OWNER (axis 31): each K-OWN key keeps one carrier; no pointer names a home its text has left (K-STALE, §8 B1).
  - I-3 GATE NET: moved text keeps its gates (`mechanism_gate.py` prefixes, install_parity anchors follow the text).
  - I-4 NO SILENT ABSENCE: a coordinator session either has its rules or sees a hook line saying what is missing; `main`
    never holds the short CLAUDE.md without the hook line (one wave merge, §7).
  - I-5 WORKER SCOPE: nothing a worker auto-loads gives it a duty to read a coordinator file (citations allowed).
  - I-6 NO UNREVIEWED GATE: no builder's tool calls ever run hook code that has not passed the critic (F5 copies, §7).
- Owner of each check (P27 vocabulary, applied to the forge; no census class: the census is package-only):

  | check | owner |
  |---|---|
  | hook line; K-STALE, K-WORKER rows; derived CLAUDE_WARN; the `facts:` refusal; the border counter | data (code) |
  | the Lead's fix check inside the border | judgment of the Lead, a tier above the builder |
  | designer cap and fix-round form; topic cap | judgment, accepted by the Lead |

## §2 Part A: the split (alternative (d) drafted, per the dispatch's edges line)

| file | auto-loaded? | read by | content |
|---|---|---|---|
| `CLAUDE.md` | yes, every session and every worker | all | the worker block below; NO `@` imports |
| `COORDINATOR.md` (new, root) | no | the coordinator, at start and after compaction (hook line); a worker only the section its role file names | intro, Contents, Tiers, rules 1-10, the rule-11 stub, 11a, 12, 13, Routing log, Role ≠ tier, Lead degradation; numbers and headings kept |
| `PROJECT.md` | no longer imported | coordinator (hook list); builder p.1 (builder.md rule 11); critic p.6/«Командная работа» citations | unchanged minus Язык and the cwd bullet |
| the three indexes | no longer imported | coordinator (hook list); `architecture_gate.py` reads the AR index by path | unchanged |

New CLAUDE.md, in order (verbatim moves unless marked NEW):

1. `# CLAUDE.md — QA Factory development` (install_parity anchor).
2. NEW, ≤ 600 bytes: "Auto-loaded into every session and every worker: only what every reader applies — the dispatch form
   (rule 11), command hygiene, worker duties, language. A worker's own rules are `.claude/agents/<role>.md` and its dispatch.
   The coordinator's rules are not here: the SessionStart line `COORDINATOR RULES:` names their files." No "read COORDINATOR".
3. `## Worker duties` (NEW heading): (a) the enforcement-file sentence of rule 2 ("A self-activating enforcement file …
   ahead of its own review."), verbatim; (b) from rule 12 Cost gates: "A worker trims run output before it enters its context
   (`-q`, a 30-line tail, `Read` with a limit over 400 lines, `Grep` instead of reading a whole file) and closes a round with
   ONE witness run after all edits, never one after each edit (D-0035)." — verbatim except the capital A and the period.
4. `## The dispatch form (rule 11)` (NEW heading) holding the four `### Rule 11 · …` blocks and the R11 table verbatim, with
   three relative citations retargeted: checklist item (4) "(rule 4)" → "(COORDINATOR.md rule 4)"; "declares ownership per
   rule 4" → "per COORDINATOR.md rule 4"; R11-f "over rule 2's threshold" → "over COORDINATOR.md rule 2's threshold".
5. `## Command hygiene (permission hygiene)` whole; point 3's tail "why and how to recover: PROJECT.md § Сессия форджа" is
   replaced by the PROJECT.md bullet «Рабочий каталог шелла не меняется никогда …», moved verbatim.
6. `## Язык` from PROJECT.md (F10). `## Ссылки на файлы в ответах` stays in PROJECT.md (F9).

Size (estimate from t-1174's section bytes: hygiene 4386 + r11 6975 + Язык 1167 + cwd 910 + enforcement 340 + trimming ≈260
+ new ≈670): **≈14.7 KB**; Card A (k4) measures; a measured size over 20000 stops Card A with a question (F1').

Hook line (Card B1):

- `tools/coordinator_rules.py` (new) is the one owner of `COORDINATOR_FILES = ("COORDINATOR.md", "PROJECT.md",
  "docs/FACTORY_RULES_INDEX.md", "docs/ARCHITECTURE_INDEX.md", "docs/OWNER_PRINCIPLES_INDEX.md")` and of
  `coordinator_lines(root, source)`, which never raises and prints ASCII only.
- startup / clear / compact: `COORDINATOR RULES: read <files> (<n> files, <bytes> bytes) before your first dispatch,
  acceptance or commit; workers do not read these at boot -- a role reads only the section its role file names`.
- resume: the same line with "re-read only if your context no longer holds them".
- Position: `session_context.main()` appends it after layer A and before `compact_snapshot_lines` (session_context.py
  2630-2641). Outside `build_context_lines`, so `MAX_LINES = 25` (:190) never cuts it; `AFTER COMPACT:` stays the last line
  before `peer_note_lines` (empty in the pins `test_compact_snapshot.py:684`, `test_session_context.py:3335`).
- BOOT BUDGET: `boot_path_files` (:1161) appends `COORDINATOR_FILES` after its BOOT.md names (dedupe kept); the `CLAUDE.md:`
  suffix now measures the worker auto-load; `CLAUDE_WARN` (:235, 58500) is re-derived (N5, §8 B1).

## §3 The DoD table: paragraph, home, reader

Reader codes: W every worker + coordinator (auto-load); C coordinator (hook line); D designer; B builder; K critic.

| # | paragraph today | home after | reader | edit beyond the move |
|---|---|---|---|---|
| C1 | title + intro "Auto-loaded into every session …" | title: CLAUDE.md; intro: COORDINATOR.md head | W / C | NEW COORDINATOR head line: "Read by the coordinator at start and after compaction (SessionStart line `COORDINATOR RULES:`); workers do not read it at boot — a role reads only the section its role file names" |
| C2 | "The project's own rules … imported here" + `@PROJECT.md` | sentence: COORDINATOR.md; `@` line deleted | C | "imported here so every session loads them" → "read with this file (the `COORDINATOR RULES:` line)" |
| C3 | the FR/AR/P index sentence + 3 `@` lines | COORDINATOR.md; `@` lines deleted | C | same swap |
| C4 | Contents | COORDINATOR.md | C | rows whose target moved name it: § 11 → `CLAUDE.md § 11`; Command hygiene → `CLAUDE.md`; Language → `CLAUDE.md § Язык`; every other `CLAUDE.md §` → `COORDINATOR.md §` |
| C5-C6 | Tiers; rule 1 + R1 | COORDINATOR.md | C | none |
| C7 | rule 2, implementation/witness | COORDINATOR.md | C | the enforcement sentence → "(enforcement-file review rule: CLAUDE.md § Worker duties)" |
| C7a | the enforcement sentence | CLAUDE.md § Worker duties | W | none |
| C8 | rule 2, drafting → designer | COORDINATOR.md | C, D | + §5.3 facts rule |
| C9-C12 | rule 3; rule 4 parallel; rule 4 witness/BATCH CANON; rule 4a | COORDINATOR.md | C (K reads critic.md 21-24; B reads `docs/TESTING.md` «Что запускать по своей правке», builder.md :50) | none |
| C13-C17 | rules 5-9 | COORDINATOR.md | C (role files restate 5 and 9's worker part, §4.3) | none |
| C18-C19 | rule 10 both blocks | COORDINATOR.md | C, D (designer rule 1), B (builder :116 citation) | none |
| C20-C23 | rule 11, four blocks + R11 | CLAUDE.md `## The dispatch form (rule 11)` | W | the three citation retargets of §2 item 4; COORDINATOR.md keeps `### Rule 11 · the dispatch form — CLAUDE.md § The dispatch form (rule 11)` |
| C24-C25 | 11a; rule 12 cadence | COORDINATOR.md | C | none |
| C26 | rule 12 Cost gates | COORDINATOR.md | C | the trimming/one-run clause leaves (→ CLAUDE.md § Worker duties, pointer "(worker trimming and the one witness run: CLAUDE.md § Worker duties)"); + §5.1 text |
| C27 | rule 13 + R13 | COORDINATOR.md | C | R13-g + topic cap (§5.2) |
| C28-C32 | Routing log, all blocks | COORDINATOR.md | C | none (hygiene point 5 stays W) |
| C33-C34 | Role ≠ tier; Lead degradation | COORDINATOR.md | C | none |
| C35-C37 | hygiene intro + 1-5; point 6 + table; point 7 | CLAUDE.md | W | point 3 as §2 item 5 |
| P1 | title + "Два набора правил" | PROJECT.md | C | :10 «блок Supervised-Delegation в `CLAUDE.md`» → «`COORDINATOR.md` (воркерский блок — `CLAUDE.md`)» |
| P2 | «Этот файл читает КАЖДАЯ сессия …» | PROJECT.md | C | → «координатор каждой сессии при старте и после сжатия (строка `COORDINATOR RULES:`); воркеры его при старте не читают» |
| P3 | Оглавление | PROJECT.md | C | Язык row → `CLAUDE.md` § Язык; :35 → `COORDINATOR.md` § Contents |
| P4 | Где что лежит | PROJECT.md | C | + a COORDINATOR.md row; :54 «импорт из `CLAUDE.md`» → «читается по строке `COORDINATOR RULES:`» |
| P5 | Принципы (:65) | PROJECT.md | C | «импорт из `CLAUDE.md`» → as P4 |
| P6 | Пакет p.1-2 | PROJECT.md | C, B | p.1 + F3: «Задача критику (дифф или план), которая трогает `ai-packages/qa-factory/`, несёт в «given» `design/architecture.md` и `design/factory-rules.md`: индексы в воркеров больше не грузятся.» |
| P7-P10 | Пакет 3-6; Бэклог; Новая идея; Прогоны | PROJECT.md | C | :105 «правило 3 `CLAUDE.md`», :128 «правило 1», :137 «правило 3» → `COORDINATOR.md` |
| P11a | Сессия форджа: cwd bullet | CLAUDE.md hygiene point 3 | W | none |
| P11b | connectors, compaction | PROJECT.md | C | none |
| P12 | Командная работа | PROJECT.md | C | :206 «правила 9 `CLAUDE.md`» → `COORDINATOR.md`; п.12 «Критик кода — один на тему» + «(до 4 узлов: R13-g)» |
| P13-P17 | Релиз; Как пишутся правила; Что решать самому (:268 «правило 11a в `CLAUDE.md`» → `COORDINATOR.md`); Ссылки (F9) | PROJECT.md | C | as stated |
| P15 | Язык | CLAUDE.md (F10) | W | none |
| X1-X3 | indexes | not imported | C | none |

Deleted as duplicates: the four `@` lines and the point-3 pointer whose target now stands in its place. Index readers: FR,
P → coordinator; AR → coordinator + gate by path; workers needing FR/AR read `design/*.md` (builder p.1, critic F3, designer
reads `architecture.md` itself).

## §4 Census and readers

### §4.1 Stale-citation census (Card owns follow it; under (d) every `CLAUDE.md rule 11` citation and every hygiene citation stays valid)

Command: Grep `CLAUDE\.md(?:'s)?`?\s+(?:routing\s+)?rules?\s+\d` per directory (`tools/`, `.claude/agents`, `.claude/skills`,
`PROCESS/`, `docs/`, root files), plus Grep `CLAUDE\.md` in role files, skills, PROCESS, PROJECT.md, RUNBOOK, TESTING,
gateway. Hits outside K-STALE's scan set (`docs/tasks/specs|handoffs|compact-snapshots/`, `plans/piles/`, AGENTS.md,
DECISIONS*, fixtures) are not edited.

| file | lines → new home (C = COORDINATOR.md) | card |
|---|---|---|
| `.claude/agents/critic.md` | 178 rule 3 → C; 198 "(rule 9" and "CLAUDE.md rule 9's exit" → C; 281 rule 3 → C (66, 165, 266, 286-287 unchanged) | A |
| `.claude/agents/designer.md` | 24 rule 2 → C; 32 rule 10 → C (17, 83 unchanged) | A |
| `.claude/agents/builder.md` | 107 "CLAUDE.md rule 12's one run (Cost gates), of rule 4's scope" → "CLAUDE.md § Worker duties' one run, of the `docs/TESTING.md` «Что запускать по своей правке» scope"; 116 rule 10 → C; 117 rule 2 → "CLAUDE.md § Worker duties"; 117-118 list + `COORDINATOR.md` (67, 121, 130 unchanged) | A |
| `.claude/agents/judge.md` | 3 (frontmatter) rule 13 → C ×2; 15-16 → C | A |
| skills | boot-diet 8, 21-24, 85, 99-108, 123 (item 6 → «`CLAUDE.md` не импортирует ничего: импорт грузится в каждого воркера; текст координатора — `COORDINATOR.md`»); session-handoff 24, 56; permission-audit 60 (52 unchanged); scout-exam-gen 64 | A |
| PROCESS | WEEKLY 88, 140, 195, 207, 498, 689, 694, 1006, 1045, 1046, 1125, 1129; JUDGE_CALIBRATION 78, 96; LEAD_RANKING_EXAM 19 (edge e13); PATCH_PROTOCOL 19 "(CLAUDE.md, COORDINATOR.md, an …)" | A |
| root | SYSTEM_PROMPT 17; DELEGATION_TABLE 4 ("rules 1-13" → "COORDINATOR.md rules 1-13; rule 11: CLAUDE.md"), 37; delegation.config.yaml 42, 51, 60 (comments); README.md 15, 41; BOOT.md 5-8 | A |
| docs | SIBLING_MAP 3, 478-479, 485, 490, 491, 494, 498, 500, 504, 507-508, 531, 533 + new row; RUNBOOK 124, 201-202, 247, 250, 614; CLAUDE_HOST_ADAPTATIONS_FULL 7-8, 36; TESTING 99, 121 (64, 68, 83 unchanged) | A |
| `gateway/config.template.yaml` | 27, 34, 41-42, 49 (comments) | A |
| tools (builder-firing, as copies §7) | claim_control_gate 99 → "CLAUDE.md § Worker duties", 253 ROOT_FILES; search_control_gate 21 → same; handoff_gate 42 → same; owns_gate 5 rule 4 → C; journal_write 58, 422 rule 12 → C; journal_hooks 41 → C; journal_validator 17, 153, 315, 679 → C; journal_echo 1526, 1541, 1574, 1815 → C; dispatch_gate 3-5 "two CLAUDE.md rules … rule 7" → "CLAUDE.md rule 11 and COORDINATOR.md rule 7" | B2 |
| tools (live) | judge_calib_sanitize 3; calibration_counts 79, 494, 829; test_journal_echo_escalation 6 | B2 |
| tools (live) | mechanism_gate 14 → C, 61 (+ COORDINATOR.md in the net list), 293 unchanged (`toolkit/CLAUDE.md`, the kit keeps rule 10); test_mechanism_gate 6; architecture_index 5 (docstring: no longer imported); `.githooks/pre-commit.next` 50-51, 59 | B1 |

### §4.2 Machine readers (designer rule 7)

Greps (da47f648): `CLAUDE\.md|PROJECT\.md|FACTORY_RULES_INDEX|ARCHITECTURE_INDEX|OWNER_PRINCIPLES_INDEX` → `tools/` 387 hits in
59 files, `.githooks/` 5 hits in 1 file (pre-commit 36, 50, 51, 55, 59), `.claude/agents` 19 lines in 4 files, `.claude/skills`
15 lines in 4 files. New names `(?i)coordinator\.md|coordinator_rules|COORDINATOR RULES` → 0 in `tools/` (positive control, same
form with `dispatch_form_refuses`: 8 hits). `CLAUDE_WARN|_ALWAYS_INCLUDE_BOOT_FILE|ROOT_FILES|MECHANISM_PREFIXES|
boot_path_files|NOTES_MAX` → 75 hits in 15 files of `tools/`; `.claude/agents` 1 (builder.md :116).

| reader | verdict |
|---|---|
| `session_context.py` (CLAUDE_WARN :235, `_ALWAYS_INCLUDE_BOOT_FILE` :211, imports :1185-1281, `boot_path_files` :1161, main :2570) | changes in B1 |
| `test_session_context.py`, `test_session_context_layer_a.py`, `test_compact_snapshot.py`, `test_session_context_autoboot.py`, `test_p4_stdin_deadline.py`, `test_journal_fresh_clone.py` (import session_context) | B1 edits the first; the rest unchanged and in B1's DoD where they import session_context |
| `compact_snapshot.py:288` (guarded import of session_context) | unchanged |
| `agents_md.py` + `test_agents_md.py` + `AGENTS.md` | changes in B1 (F7) |
| `install_parity_anchors.json` (routing-policy 89 anchors :7-95; designer :177 "the text is CLAUDE.md rule 11" stays; lead-ranking anchor) + `install_parity.py` (unique `unit_id` only, :366; no kit_path check) | changes in B1: new unit `routing-policy:coordinator`, host COORDINATOR.md, kit_path `toolkit/CLAUDE.md`; hygiene, rule 11, worker-duty anchors stay in `routing-policy` |
| `mechanism_gate.py` MECHANISM_PREFIXES :215; `test_mechanism_gate*.py`; `test_streams.py` S4 (:346-394); `test_worktree_sweep.py` | B1: + `COORDINATOR.md`, `tools/coordinator_rules.py`; test_streams/test_worktree_sweep unchanged (S4 edge e16; sweep calls `_matches`) |
| `worktree_sweep.py`, `streams.py`, `gitcmd.py`, `handoff_gate.py` (name MECHANISM_PREFIXES in comments) | unchanged |
| `claim_control_gate.py` ROOT_FILES :253 + test | changes in B2 (copy) |
| `tests/test_role_carriers_one_owner.py`: OWNER_KEYS 57-61, POINTERS 73-104, TOC 109-164, DELETED 254-263, `main_documents` 268 | changes in B1: 59-61 → COORDINATOR.md (57-58 stay CLAUDE.md); POINTERS 80, 83, 85, 86, 88 → C; 103 → `("CLAUDE.md", "Рабочий каталог шелла не меняется никогда", …)` dropped (pointer gone); `_TOC_CL` = COORDINATOR.md with each target per C4; 161 → CLAUDE.md § Язык; 164 → COORDINATOR.md; `need` += COORDINATOR.md; + K-STALE, K-WORKER |
| `dispatch_manifest.py`, `dispatch_gate.py`, `dispatch_new.py` + tests | changes in B2 (F13) |
| `owns_verify.py` 3/26, `hook_liveness_probe.py` 971-984/1273, `test_piles_take.py` 401, `test_dispatch_*` rule-11 pins | unchanged under (d) |
| `escape_check.py` + `escape_allowlist.json` (`entries: []`) | unchanged |
| `permission_audit.py`, `factory_rules_index.py`, `architecture_gate.py`, `owns_readers.py`, `md_table.py`, `md_regions.py`, `hop_metrics.py`, `wiring_check.py`, `agent_budget.py` (:278 "(PROJECT.md)" stays), `piles.py`, `language_sites.py`, `tools/fixtures/*` (K4 scout, K8 critic: unaffected by F13) | unchanged |
| `.claude/settings.json` | unchanged |
| `tools/conftest.py` | changes in B2 (copy loader, F5-r) |

The critic's `owns_readers.py` lines: `names: tools/test_streams.py` → edge e16 (B1); `names: tools/test_worktree_sweep.py`
→ unchanged (calls `_matches`); `absent: docs/tasks/critic-diff-brief.md` → path dropped from every card. A fresh block on
da47f648 is a Lead `facts:` line (command §12; the designer cannot run it).

### §4.3 Worker-duty sweep of the sections leaving CLAUDE.md (rule 9, sweep the artifact)

rule 1 (scout trail) → scout.md ✓; rule 2 (questions; enforcement file) → builder.md 23 ✓ / § Worker duties ✓; rule 3 (own
DoD self-run, mechanical layer) → builder.md 41-43, critic.md 21 ✓; rule 4 (parallel sessions, witness scope) → builder.md 10,
50 ✓; rule 4a, 7, 8, 10 (Lead), 12 cadence, 13, Role ≠ tier, degradation → not applicable: coordinator duties; rule 5 → role
files ✓; rule 6 "beyond my level" → not applicable: a worker's free signal, role files already return questions or
`decomposable`; rule 9 analogs → builder.md 5, designer rule 3, critic Q4 ✓; rule 11 → stays W ✓; 11a → builder questions,
designer forks ✓; rule 12 Cost gates trimming + one run → moved (B4) ✓; Routing log hand-back → role files' handoff ✓.

## §5 Part B: rule texts

### §5.1 Item 6 + border: COORDINATOR.md rule 12 Cost gates, after "a re-review carries only the fix diff and the verdict;"

> After a critic verdict `fit_with_fixes` on CODE, the Lead checks the fix round ITSELF only inside this border (the
> owner's word 17.11.2026): the fix diff does exactly what the verdict's `fixes` prescribe and adds no new logic — no new
> function, branch, state or write path. The base is the reviewed head: the bare token `reviewed:<sha>` in the notes of the
> critic's `delegated` event, written by the Lead from `git -C <tree> rev-parse HEAD` after committing the reviewed state.
> Measured on `git -C <tree> diff -U0 <sha> -- '*.py'` (added lines only; a line whose first non-blank character is `#` is
> not counted): zero lines matching `^\+\s*(def |class |async def |if |elif |else\b|try:|except\b|finally:|for |while |match
> |case )`, zero lines containing `\bif\b`, `\blambda\b`, `\band\b` or `\bor\b`, zero new files (`git diff --name-only
> --diff-filter=A <sha>` and `git ls-files --others --exclude-standard`), zero added `add_argument(`, zero added write calls
> (`write_text|write_bytes|open\(.*['"][wax]|append_jsonl|\.write\(`), no changed file other than `.py` and `.md`, and no
> line outside the owns the verdict reviewed. Inside the border the Lead walks the fix diff by the critic's standing
> questions — `.claude/agents/critic.md` rule 22, Q1-Q12 — one line per question, plus one line per fix (`fixed: <where>`
> / `not fixed` → another fix round); a new dict entry used as a dispatch table is caught only by this walk (Q1, Q3). The
> `accepted` notes carry `fixes checked by Lead: <verdict path>, border 0`. Outside the border (any count above zero), with
> no `reviewed:` token or a base that is not an ancestor of HEAD, when the verdict was `blocker`, when a fix cannot be
> matched to its verdict line, or when the acceptor is not strictly above the builder's tier (Role ≠ tier), a critic
> re-review carries only the fix diff and the verdict, and its dispatch names its case: `re-review:
> logic|nobase|blocker|unmatched|tier`. Plans keep PROJECT.md new idea, step 6.

- Invariant: no new statement- or expression-level branch, function or write path is accepted without a critic; a
  dispatch-table entry is the one named exception, judged by the Lead's Q-walk.
- Error direction: the counter errs only toward a re-review. Adversarial inputs that must land outside: `+ m = "a" if f
  else "b"`; `+ key=lambda r: r[1]`; `+ v = x or default`; `+ ok = a and b`; `[x for x in y if p(x)]`; a JSON data row; a hook
  config; a new file; a docstring line containing "or" (outside: the cost of a re-review, accepted). Inside: a renamed
  local, a changed string literal without those words, a comment line.
- Detector: calibration check 17 sub-item: (a) a re-review naming no case; (b) an `accepted` after `fit_with_fixes` with
  neither `fixes checked by Lead` nor a re-review; (c) a sample re-run of the counter on (a)/(b) commits.

### §5.2 Topic cap: COORDINATOR.md R13-g (+ PROJECT п.12 pointer)

> One critic pass per TOPIC, and a topic holds at most 4 nodes (the owner's word 17.11.2026); a fifth node opens a new
> topic, split by disjoint owns or seams.

- Invariant: per-node critics stay unreachable; the topic count grows only by splitting. Edge: exactly 4 legal, 5 splits.
- Detector: check 2's cumulative subcase counts nodes per critic `delegated` (`node` field, notes).

### §5.3 Facts before the designer: COORDINATOR.md rule 2 drafting (+ designer.md rule 3, + the dispatch header)

> Before a designer dispatch the Lead MEASURES the brief's load-bearing facts by code (the owner's word 17.11.2026). A
> load-bearing fact is any claim about the CURRENT repo or data that a requirement, an edge or a reader list rests on: a
> file, function, constant, field, CLI flag or hook that exists, and its shape or value; a count (readers, hits, sizes,
> lines); a test pin or anchor text; a data premise (PROJECT.md p.6(а)). Each fact goes into the dispatch as a `facts:`
> header block, one line each: `<claim> | <command> | <verbatim result, at most 200 chars>`. When the brief rests on none,
> the block is `facts: none -- <why>`. Opinions, intent and the owner's words are not facts: they go in the brief.

- designer.md rule 3 gains: "facts in `facts:` are the Lead's measurement and may be cited with their command; a
  load-bearing fact the draft adds is measured by the designer the same way and listed in the trail; a fact the designer
  cannot measure (no shell) is labelled `estimate` with the command the Lead runs."
- Code (F13, Card B2): data row `FACTS_KINDS = ("designer",)` in `dispatch_manifest.py` beside `HANDOFF_DIRS` (read by the
  dispatch kind, never by a name in code); `facts` joins the cut's header vocabulary (one cut, axis 13); a new
  `facts_check(payload, cut, dm)` in `dispatch_gate.py` runs in `decide_full` as completeness → handoff folder → **facts**
  → path → label. Refusal: `FACTS MISSING (COORDINATOR.md rule 2): this designer dispatch does not go out. It has no facts:
  header (or an empty one, or a bare none). Add one line per load-bearing fact (<claim> | <command> | <result>), or
  facts: none -- <why>.`
- Positional invariant: the facts branch is reached only when the handoff check returned 0 for a kind in `FACTS_KINDS`; a
  completeness or handoff refusal always fires first and is never replaced; a non-designer dispatch never reaches it;
  `manifest-skip: facts -- <reason>` passes it with a note (FR-4); an unknown (no cut, degraded cut, import failure) is a
  NOTE and a pass, the same direction as its sibling `handoff_folder_check` (dispatch_gate.py:741-774).
- Invariant: no spec premise about the repo rests on memory. Detector: `rejected` with `failure_class: spec` whose note
  names a premise without a `facts:` line; code: the refusal.

### §5.4 Item 7: designer.md rule 8; rule 4 "Write and Edit"; frontmatter `tools: Read, Glob, Grep, Write, Edit`

> 8. Size and fix rounds (the owner's word 17.11.2026, «если это не ухудшит качество»). The draft file is at most 40,000
> bytes on disk (`python -B -c "import os,sys;print(os.path.getsize(sys.argv[1]))" <path>`). A draft that will not fit
> returns `decomposable: <parts by disjoint owns>` before writing past the cap. Edges, invariants, readers, forks and the
> trail are never trimmed to fit. A FIX ROUND (its `handoff:` names the earlier draft) EDITS that file in place: (a) a
> `## Revision rN` block at the top, one line per finding or decision: `<id> -> change -> section`; (b) every builder card
> it touches is rewritten WHOLE in place; (c) untouched sections stay byte-identical; (d) a revision touching more than half
> of the cards, or §1, is a full rewrite. The file at `handoff:` is always the complete current spec: a builder reads one
> document and never merges two.

- `handoff_gate.py` gates Edit for the designer (`WRITE_TOOLS`, `GATED_KINDS`, :68-69). Detector: check 28 sub-item (drafts
  over 40,000 bytes; fix rounds whose `git diff --stat` breaks (d)). This r2 is a full rewrite at a new path, as dispatched.

## §6 Edges, each with the invariant it protects

1. A coordinator file missing, empty (0 bytes), a directory or unreadable: per file `COORDINATOR RULES: MISSING <path>
   (<reason>) -- read it from git: git -C <root> show origin/main:<path>; until then this session has no coordinator
   rules`; good files still listed. Presence by `stat`, never by decoding; errs toward MISSING. Invariant I-4.
2. Import/run of `coordinator_rules.py` fails: `COORDINATOR RULES: unavailable (<exc>) -- read <literal list> yourself`;
   the literal is the one fallback copy, pinned equal to `COORDINATOR_FILES` by a test row. Invariant: the hook never fails
   the session start and the read duty still appears.
3. A worker sees no line (SessionStart does not fire for it); CLAUDE.md names no read duty (K-WORKER). Invariant I-5.
4. An old worktree keeps its long CLAUDE.md and old hook: complete rules, dearer. Invariant: reachable rules = the tree's
   CLAUDE.md ∪ the tree's hook-listed files; hook code and CLAUDE.md are one generation per tree.
5. Merging an old branch that edited a moved paragraph conflicts on CLAUDE.md; the merger re-applies it in COORDINATOR.md
   (TEAMWORK §3). Invariant: one home per rule — K-OWN reds on a doubled key; the derived WARN (≈17000, 15 % over ≈14.7 KB)
   fires when a moved paragraph of ≥ ≈2.3 KB lands back (rule 4 is ≈3 KB, t-1174 estimate).
6. Compaction: the line prints again before `AFTER COMPACT`; resume prints the "re-read only if" form.
7. MAX_LINES=25 never cuts the line (outside `build_context_lines`).
8. Temporal: COORDINATOR.md, `coordinator_rules.py`, the `facts:` refusal and the hook line do not exist before the topic;
   on `main` they land in ONE wave merge. On the integration branch, between Lead commit #1 and B1, COORDINATOR.md exists
   without the hook line and install_parity's routing anchors fail; no session runs there except B1's builder (a worker, no
   SessionStart). A designer dispatch drafted before the merge and sent after it is refused with the door `facts: none --
   <why>`. Fixtures K4 (scout) and K8 (critic) are unaffected.
9. Codex AGENTS.md = CLAUDE.md + every coordinator file under the import markers (F7): the same text as today, reordered.
10. A retarget changes only the home a citation names; a pinned string changes in the same card as its test.
11. "Workers do not read the coordinator file" vs "workers need rule 11": (d) keeps rule 11 in the auto-load.
12. Each coordinator file stays under the Read default (≈25K tokens): COORDINATOR.md ≈43.4 KB (estimate) ≈ 11K tokens.
13. LEAD_RANKING_EXAM item 2 (:19 "Claude Code subagents auto-load CLAUDE.md, so the policy is already in their context")
    becomes "the dispatch attaches COORDINATOR.md whole, so the policy is in the candidate's context" — keeps the FAIR
    condition; its anchor moves in B1.
14. Item-6 border on a `.md`-only fix diff: zero by construction; allowed (prose is walked by Q1-Q12).
15. A `*.py.next` copy present while live tests run: live tests test the live file; new behaviour is tested through the
    copy loader only (§7); a subprocess-based case (`python tools/x.py`) of new behaviour is written in-process or waits for
    the Lead's post-placement run. Invariant I-6.
16. S4 (`test_streams.py`): `coordinator_rules.py` joins MECHANISM_PREFIXES, so it imports no module that reaches
    `tools/streams.py` (stdlib only). Invariant: only the sanctioned road reaches the helper.
17. `boot_path_files` vs BOOT.md (critic Q6): BOOT.md stays the one owner of its own "Read X.md" list; Card A never writes
    "Read COORDINATOR.md" or "Read PROJECT.md" in BOOT.md (it names the hook line), so the two lists never double-count.
18. K-STALE false positives: `toolkit/CLAUDE.md rule N` (the kit keeps every rule) and `CLAUDE.md rule 11` are not stale.
    Invariant: a citation of a rule still living in the cited file never fails the pin.

## §7 Order, trees and copies (F5 = copies, Lead decision; mechanics forks F5-r, F15)

Order (recommended in F15):

1. The Lead creates ONE integration worktree on `pile/<slug>/batch-<N>` from origin/main. Cards A and B2 run in parallel in
   it (disjoint owns; a shared tree, so neither builder runs any git state change — builder.md rule 10); nothing is committed.
2. Critic topic 1 on A + B2 (2 nodes). The Lead stages A and B2, then PLACES each copy: a byte move of
   `tools/<name>.py.next` over `tools/<name>.py`, the `.next` file removed; runs B2's DoD without the `*_PATH` variables
   on the placed tree (a deterministic run; its output is the witness of B2's `accepted`); Lead commit #1 (axis block,
   `tier: opus`, `Deviation: exam not run; debt F3-1` for critic.md — F8').
3. Card B1 in the same worktree on top of commit #1 (B2's reviewed hooks are now live there; I-6 holds).
4. Critic topic 2 on B1. The Lead places `.githooks/pre-commit.next`, runs B1's DoD, Lead commit #2, `tools/wave.py merge`.

Why each file fires in a builder (settings.json hook commands :5-132; `.githooks/` lines; import lines read by Grep):

| live file (B2) | reached in a builder by | delivered as |
|---|---|---|
| `tools/dispatch_manifest.py` | handoff_gate.py:64 (PreToolUse Edit/Write); agent_budget.py:101 (PreToolUse, every tool); dod_gate.py:350 (SubagentStop) | `tools/dispatch_manifest.py.next` |
| `tools/dispatch_gate.py` | owns_gate.py:476-484 (module level) ← dod_gate.py:433; dispatch_manifest.py:248 | `.py.next` |
| `tools/journal_write.py` | journal_hooks.py:80, 97, 334 (PreToolUse Edit/Write `pre-edit`) | `.py.next` |
| `tools/journal_validator.py` | journal_echo.py:254 (PostToolUse); journal_write.py:51 | `.py.next` |
| `tools/journal_hooks.py` | PreToolUse Edit/Write `journal_hooks.py pre-edit`; dod_gate.py:748 | `.py.next` |
| `tools/journal_echo.py` | PostToolUse Edit/Write/Bash; journal_hooks.py:451 | `.py.next` |
| `tools/claim_control_gate.py` | PreToolUse Edit/Write | `.py.next` |
| `tools/search_control_gate.py` | PostToolUse Bash/Grep/Glob/Read | `.py.next` |
| `tools/owns_gate.py` | dod_gate.py:433 (SubagentStop) | `.py.next` |
| `tools/handoff_gate.py` | PreToolUse Edit/Write; dod_gate.py:349 | `.py.next` |
| `dispatch_new.py`, `judge_calib_sanitize.py`, `calibration_counts.py`, tests, `conftest.py` | no hook path (CLI or tests only; import Grep) | live edit |

| live file (B1) | reached in a builder by | delivered as |
|---|---|---|
| `tools/session_context.py`, `tools/agents_md.py`, `tools/coordinator_rules.py` (new) | SessionStart only (never fires in a worker); compact_snapshot.py:288 imports session_context inside try/except (fail-open, cannot gate) | live edit |
| `tools/mechanism_gate.py`, `tools/architecture_index.py` | `.githooks/commit-msg:32`, `pre-commit:58` — fire only on a commit; no builder commits in this topic | live edit (F5-r option: copy) |
| `.githooks/pre-commit` | an active hooks-path file (CLAUDE.md § Worker duties) | `.githooks/pre-commit.next` |

Import resolution (recommended in F5-r): ONE loader in `tools/conftest.py`, run at its import: for every environment
variable `<NAME>_PATH` whose value names an existing `tools/<name>.py.next` (`<name>` = NAME lower-cased, and
`tools/<name>.py` must exist, else a loud error naming the variable), it installs one `importlib.abc.MetaPathFinder` at the
front of `sys.meta_path` that answers `find_spec(<name>)` with `spec_from_file_location(<name>, path,
loader=SourceFileLoader(<name>, path))` and `None` for every other name. So a test's `import dispatch_manifest` and a
sibling's own import (`owns_gate`'s module-level `from dispatch_gate import …`) both resolve to the copy, in any order.
Variables naming a `.py` file (the existing `HYGIENE_GATE_PATH` loaders in `test_hygiene_gate.py`/`test_permission_audit.py`)
are ignored by it. The environment read stays in test code only. Placement: Lead, step 2 above, before B1.

## §8 Builder cards (paths under `C:/QAFactory/forge-repo/`; the Lead substitutes the integration worktree root, §7)

### Card A: the text move (docs)

given: this spec §2, §3, §4.1, §5, §6; `CLAUDE.md`; `PROJECT.md`; `.claude/agents/{designer,builder,critic,judge}.md`;
`docs/SIBLING_MAP.md` axis 31 (473-562)
owns:
C:/QAFactory/forge-repo/CLAUDE.md
C:/QAFactory/forge-repo/COORDINATOR.md
C:/QAFactory/forge-repo/PROJECT.md
C:/QAFactory/forge-repo/BOOT.md
C:/QAFactory/forge-repo/README.md
C:/QAFactory/forge-repo/SYSTEM_PROMPT.md
C:/QAFactory/forge-repo/DELEGATION_TABLE.md
C:/QAFactory/forge-repo/delegation.config.yaml
C:/QAFactory/forge-repo/AGENTS.md
C:/QAFactory/forge-repo/.claude/agents/designer.md
C:/QAFactory/forge-repo/.claude/agents/builder.md
C:/QAFactory/forge-repo/.claude/agents/critic.md
C:/QAFactory/forge-repo/.claude/agents/judge.md
C:/QAFactory/forge-repo/.claude/skills/boot-diet/SKILL.md
C:/QAFactory/forge-repo/.claude/skills/session-handoff/SKILL.md
C:/QAFactory/forge-repo/.claude/skills/permission-audit/SKILL.md
C:/QAFactory/forge-repo/.claude/skills/scout-exam-gen/SKILL.md
C:/QAFactory/forge-repo/docs/SIBLING_MAP.md
C:/QAFactory/forge-repo/docs/RUNBOOK.md
C:/QAFactory/forge-repo/docs/CLAUDE_HOST_ADAPTATIONS_FULL.md
C:/QAFactory/forge-repo/docs/TESTING.md
C:/QAFactory/forge-repo/PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md
C:/QAFactory/forge-repo/PROCESS/LEAD_RANKING_EXAM.md
C:/QAFactory/forge-repo/PROCESS/JUDGE_CALIBRATION_PROTOCOL.md
C:/QAFactory/forge-repo/PROCESS/PATCH_PROTOCOL.md
C:/QAFactory/forge-repo/gateway/config.template.yaml
non-goals: `tools/`, `.githooks/`, `ai-packages/`; scout.md; any rule meaning beyond §3's last column and §5; no git state change (shared tree)
handoff: the builder report path `C:/QAFactory/forge-repo/docs/tasks/handoffs/<task>-card-a.md`
edges: §6 e3, e10, e11, e12, e13, e17, e18; a sentence §3 does not place → a question; Russian moves verbatim
DoD: a DOC-DISPATCH witness (CLAUDE.md § DOC-DISPATCH WITNESS: keys verbatim from this DoD, the full script in the report, a negative control; scratch file, never committed): `python -B <scratch>/card_a_check.py --base origin/main`
siblings: axis 31 (rows written here), axis 1 (role files + AGENTS.md), axis 2 (critic.md edit: deviation line, F8')
designer: C:/QAFactory/forge-repo/docs/tasks/specs/20261117-worker-boot-and-round-rules-spec-r2.md

Behaviour:

1. Build CLAUDE.md (§2) and COORDINATOR.md (§3 C-rows), line by line; apply §3's last column and nothing more.
2. Place §5.1 (Cost gates), §5.2 (R13-g; PROJECT п.12), §5.3 (rule 2 + designer.md rule 3), §5.4 (designer.md rules 4, 8,
   frontmatter `Edit`), F3's PROJECT p.1 sentence (§3 P6).
3. Retarget every §4.1 row marked A, exactly as written there.
4. `docs/SIBLING_MAP.md` axis 31: rewrite the intro sentence (478-479: `COORDINATOR.md` routing rules and Cost gates;
   `CLAUDE.md` rule 11, hygiene, worker duties) and the rows of 485, 490, 491, 494, 498, 500, 504, 507-508, 531, 533 to the new
   homes; ADD the row `| \`COORDINATOR.md\` | coordinator; a worker by the section its role file names | routing rules 1-10,
   11a, 12, 13, journal, Role ≠ tier, degradation, Cost gates, the topic map (§ Contents) | owner (owner word pending:
   PROJECT.md «Лишних документов нет»); read via the SessionStart line \`COORDINATOR RULES:\` |`. Its Owner cell starts with
   "owner", so K-NOBRIEF scans the file.
5. BOOT.md 5-8: name the worker block and the `COORDINATOR RULES:` line, never in the form "Read X.md" (e17).
6. LEAD_RANKING_EXAM item 2 per e13. Calibration: check 10 and 33(h) name COORDINATOR.md; check 2 counts nodes per topic;
   check 17 gets §5.1's sub-item; check 28 §5.4's; check 7 gets: the first Task/Agent call of a main session after a start or
   compaction follows a Read of COORDINATOR.md.
7. Regenerate AGENTS.md: `python -B tools/agents_md.py --repo <tree>` (transiently the worker block only; B1 regenerates).
8. Report the new texts of the install_parity anchors that A changes (routing anchors now in COORDINATOR.md, the
   lead-ranking item 2 line) for B1.

DoD keys (the script checks, each printing PASS/FAIL):

- (k1) For every line of `git show origin/main:CLAUDE.md` + `origin/main:PROJECT.md` with ≥ 8 characters that is not
  markup-only (`^[\s|:\-`]*$` or a fence line), its count in new CLAUDE.md + COORDINATOR.md + PROJECT.md equals its count in
  the two old files; every new or changed line is in the report's edited-lines list (old → new, each with its §3 row).
- (k2) present: CLAUDE.md `## Command hygiene (permission hygiene)`, `` `COORDINATOR RULES:` ``, `## Язык`, `## Worker
  duties`, `11. DoD in every dispatch (DoD-in-every-dispatch rule)`, `DOC-DISPATCH WITNESS:`, `a 30-line tail`;
  COORDINATOR.md `## Role ≠ tier`, `## Lead degradation`, `## Routing log — logs/journal/<dev>.jsonl`, `### Rule 12 · Cost
  gates`, `fixes checked by Lead:`, `at most 4 nodes`, `` `facts:` ``, `rule 22, Q1-Q12`; designer.md `## Revision rN`,
  `40,000 bytes`; SIBLING_MAP `owner word pending`; PROJECT.md `design/architecture.md` и `design/factory-rules.md`.
- (k3) CLAUDE.md has no `^@` line and no `read COORDINATOR` (case-insensitive).
- (k4) byte sizes printed; CLAUDE.md < 20000, COORDINATOR.md < 60000.
- (k5) no §4.1 row marked A still matches `CLAUDE\.md(?:'s)?`?\s+(?:routing\s+)?rules?\s+(?!11\b)\d` or `правил\w*\s+(?!11\b)\d+\w?\s+(?:в\s+)?`?CLAUDE\.md`.
- Negative control: a copy of COORDINATOR.md without `## Lead degradation` → FAIL.

### Card B2: citation strings in tools + the `facts:` header (parallel with A)

given: this spec §4.1 (rows B2), §5.3, §7; the homes: rules 1-10, 11a, 12, 13, Routing log → `COORDINATOR.md`; rule 11, hygiene, worker duties → `CLAUDE.md`
owns:
C:/QAFactory/forge-repo/tools/dispatch_manifest.py.next
C:/QAFactory/forge-repo/tools/dispatch_gate.py.next
C:/QAFactory/forge-repo/tools/journal_write.py.next
C:/QAFactory/forge-repo/tools/journal_validator.py.next
C:/QAFactory/forge-repo/tools/journal_hooks.py.next
C:/QAFactory/forge-repo/tools/journal_echo.py.next
C:/QAFactory/forge-repo/tools/claim_control_gate.py.next
C:/QAFactory/forge-repo/tools/search_control_gate.py.next
C:/QAFactory/forge-repo/tools/owns_gate.py.next
C:/QAFactory/forge-repo/tools/handoff_gate.py.next
C:/QAFactory/forge-repo/tools/dispatch_new.py
C:/QAFactory/forge-repo/tools/judge_calib_sanitize.py
C:/QAFactory/forge-repo/tools/calibration_counts.py
C:/QAFactory/forge-repo/tools/conftest.py
C:/QAFactory/forge-repo/tools/test_dispatch_manifest.py
C:/QAFactory/forge-repo/tools/test_dispatch_gate.py
C:/QAFactory/forge-repo/tools/test_dispatch_new.py
C:/QAFactory/forge-repo/tools/test_claim_control_gate.py
C:/QAFactory/forge-repo/tools/test_journal_echo_escalation.py
non-goals: every live file listed as a copy (never edited in place); rule-11 strings (valid under (d)); docs (A); no behaviour change beyond F13 and ROOT_FILES; no git state change
handoff: `C:/QAFactory/forge-repo/docs/tasks/handoffs/<task>-card-b2.md`
edges: e15; a non-designer dispatch is unaffected; `facts:` with empty content is refused; `facts: none` without ` -- <why>` is refused; `manifest-skip: facts -- <r>` passes with a note; an unknown cut is a note and a pass; the handoff refusal wins over the facts refusal; a copy differs from its live file only in §4.1 lines plus (dispatch_*) F13 and (claim_control) ROOT_FILES
DoD: `DISPATCH_MANIFEST_PATH=tools/dispatch_manifest.py.next DISPATCH_GATE_PATH=tools/dispatch_gate.py.next CLAIM_CONTROL_GATE_PATH=tools/claim_control_gate.py.next python -m pytest tools/test_dispatch_manifest.py tools/test_dispatch_gate.py tools/test_dispatch_new.py tools/test_claim_control_gate.py tools/test_journal_echo_escalation.py -q`, then `python -B -m py_compile` on each `.py.next`, then `git diff --no-index --stat` live vs copy for each comment-only copy with the changed lines quoted (each contains `COORDINATOR.md` or `CLAUDE.md §`)
siblings: axis 13 (the `facts` header joins the one cut; dispatch_gate reads it only through dispatch_manifest); axis 31 (comment pointers)
designer: C:/QAFactory/forge-repo/docs/tasks/specs/20261117-worker-boot-and-round-rules-spec-r2.md

Behaviour: (1) each copy starts as a byte copy of its live file; (2) §4.1 B2 retargets; (3) ROOT_FILES += `"COORDINATOR.md"`
(claim_control copy) with a test row; (4) F13 per §5.3 in the dispatch_manifest/dispatch_gate copies, `dispatch_new.py`
printing `facts:` for the designer kind; new cases are table rows in the existing test files: designer with/without
`facts:`, empty, bare `none`, `none -- why`, waiver, builder kind untouched, handoff-missing + facts-missing (handoff wins),
degraded cut; (5) the conftest loader per §7 with three rows in an existing test file (a `.py.next` variable maps; a `.py`
variable is ignored; a variable naming a missing file fails loudly).

### Card B1: hook line, generators, gates, pins (after the Lead's placement of B2, §7 step 3)

given: this spec; Card A's report (anchor texts); the placed tree of commit #1
owns:
C:/QAFactory/forge-repo/tools/coordinator_rules.py
C:/QAFactory/forge-repo/tools/session_context.py
C:/QAFactory/forge-repo/tools/test_session_context.py
C:/QAFactory/forge-repo/tools/agents_md.py
C:/QAFactory/forge-repo/tools/test_agents_md.py
C:/QAFactory/forge-repo/AGENTS.md
C:/QAFactory/forge-repo/tools/mechanism_gate.py
C:/QAFactory/forge-repo/tools/test_mechanism_gate.py
C:/QAFactory/forge-repo/tools/test_mechanism_gate_md.py
C:/QAFactory/forge-repo/tools/install_parity_anchors.json
C:/QAFactory/forge-repo/tools/tests/test_role_carriers_one_owner.py
C:/QAFactory/forge-repo/tools/architecture_index.py
C:/QAFactory/forge-repo/.githooks/pre-commit.next
non-goals: doc text (A); B2's tools; `.githooks/pre-commit` itself; no commit, no git state change
handoff: `C:/QAFactory/forge-repo/docs/tasks/handoffs/<task>-card-b1.md`
edges: e1, e2, e6, e7, e16, e17, e18; changed BOOT BUDGET pins compute their value from the fixture; new cases are variant rows (present / missing / empty / directory / import fails / resume / compact order; fallback list == COORDINATOR_FILES)
DoD: `python -m pytest tools/test_session_context.py tools/test_session_context_layer_a.py tools/test_compact_snapshot.py tools/test_agents_md.py tools/test_mechanism_gate.py tools/test_mechanism_gate_md.py tools/test_streams.py tools/test_install_parity.py tools/tests/test_role_carriers_one_owner.py -q`; then `python -B tools/agents_md.py --check`, `python -B tools/install_parity.py --check`, `python -B tools/architecture_index.py --check`, `python -B tools/factory_rules_index.py --check`, `python -B tools/session_context.py </dev/null`; the witness quotes the `BOOT BUDGET`, `CLAUDE.md:` and `COORDINATOR RULES:` lines verbatim
siblings: axis 31 (pins), axis 18 (CLAUDE_WARN lowered, named, derived), axis 1 (AGENTS.md), axis 34 (Codex keeps the full text by the same generator)
designer: C:/QAFactory/forge-repo/docs/tasks/specs/20261117-worker-boot-and-round-rules-spec-r2.md

Behaviour: (1) `coordinator_rules.py` per §2 and e1, e2, e6 (stdlib only, e16); (2) wire `main()` per §2; `boot_path_files`
appends `COORDINATOR_FILES`; `CLAUDE_WARN = ceil(<CLAUDE.md bytes measured on this tree> × 1.15 / 100) × 100` with the comment
"Re-derived 2026-11-17 (t-1137): CLAUDE.md N bytes … NAMED LOWERING 58500 -> X; cause: the worker split"; (3) `agents_md`
appends `COORDINATOR_FILES` under the import markers; (4) MECHANISM_PREFIXES += `COORDINATOR.md`, `tools/coordinator_rules.py`,
mechanism_gate 14 and 61 per §4.1, a COORDINATOR.md variant row; (5) install_parity per §4.2 with A's anchor texts; (6) role
carriers per §4.2, plus K-STALE: no scanned file matches `(?<!toolkit/)CLAUDE\.md(?:'s)?`?\s+(?:routing\s+)?rules?\s+(?!11\b)\d`,
`(?<!toolkit/)CLAUDE\.md(?:'s)?\W{0,4}(?:Tiers|Routing log|Routing rules|Role\s*(?:≠|!=)\s*tier|Lead degradation|Contents)`,
`\b(?:rule \d+\w?|R13-g) of CLAUDE\.md`, or `правил\w*\s+(?!11\b)\d+\w?\s+(?:в\s+)?`?CLAUDE\.md` (positive control: a row
with a stale sample; negative: `toolkit/CLAUDE.md rule 10`, `CLAUDE.md rule 11`); `docs/ADOPTION_LEDGER.md` joins EXCLUDED as a
record; K-WORKER: CLAUDE.md has no `^@` line and no `read COORDINATOR`; (7) regenerate AGENTS.md; (8) `pre-commit.next`: the
whole file, comments 50-51 and 59 retargeted; (9) `architecture_index.py:5` docstring: the index is no longer imported (cap kept).

## §9 Mechanism commits: four questions, axes, budget

- M1 split + hook line: (a) the coordinator reads 5 files per start/compaction (≈ COORDINATOR 43.4 + PROJECT 34.2 + three
  indexes; estimate) instead of auto-loading them, plus the Read tool's line-number overhead; each worker call drops from
  101,738 bytes (t-1174 measurement) to ≈14.7 KB (estimate). **BOOT BUDGET after the split ≈116.8 KB of 120,000** (t-1174's
  116,770 with DISPATCH 7,035 folded back into CLAUDE.md; estimate): headroom ≈3.2 KB. Next lever if a later rule crosses
  120,000: drop the FR and P indexes from `COORDINATOR_FILES` (read on demand: FR when the package is touched, P for a
  principle question) — a Lead decision then. (c) the line; K-OWN, K-STALE, K-WORKER; install_parity in CI; the derived
  WARN; check 7. (d) SessionStart in code; the read itself is discipline, detector check 7 (F4).
- M2 the Lead's fix check: (a) a counter run + a 12-question walk; one critic run saved per pure fix round. (c) check 17
  (a-c). (d) the border is a command; promotion to a `dispatch_gate` re-review case line on a leak.
- M3 designer cap/delta: (c) check 28; (d) discipline; `handoff_gate` confines Edit.
- M4 topic cap: (a) splitting adds critic passes beyond 4 nodes; (c) check 2; (d) discipline.
- M5 facts before the designer: (a) 3-10 commands per brief; (c) `rejected` spec naming an unmeasured premise; (d) the
  `dispatch_gate` refusal.
- (b) axes, one block for M1-M5 (38 axes, `docs/SIBLING_MAP.md` headings):

  | axis | verdict |
  |---|---|
  | 1 | covered: policy, role files, AGENTS.md in one wave; journal untouched |
  | 2 | covered: critic.md edited with `Deviation: exam not run; debt F3-1` (CRITIC_EXAM.md and SCOUT_GOLDEN_SET.md absent, PROCESS/README.md:22-25; F8'); Lead exam item 2 (e13) |
  | 3, 4 | n/a: no package change; indexes unchanged |
  | 5-11 | n/a: package / test identity |
  | 12 | n/a: pile rules unchanged |
  | 13 | covered: the `facts` header joins the one cut (B2) |
  | 14 | n/a now (check 7 by hand; F4) |
  | 15 | covered: coordinator_rules.py stdlib-only, S4 (e16) |
  | 16, 17 | n/a |
  | 18 | covered: CLAUDE_WARN lowered by the 1.15 formula, named |
  | 19-30 | n/a: package readers |
  | 31 | covered: owners, pointers, TOC, K-STALE, the COORDINATOR.md row (owner word pending) |
  | 32, 33 | n/a |
  | 34 | covered: one CLAUDE.md for every Claude Code worker; Codex by the same generator (F7); `facts` read by kind |
  | 35-38 | n/a: package |

## §10 Forks (the Lead decides; the owner where marked)

- **F1' (B5) Rule 11's home — owner's word on new main documents.** (d) rule 11 in the CLAUDE.md worker block — DRAFTED,
  recommended: no new document; every rule-11 pin, anchor and citation stays valid (dispatch_gate :620/:710,
  dispatch_manifest :138, probe :1273, designer.md :17, critic.md :286, install_parity :177, 6 test pins); cost ≈7 KB on every
  worker call (estimate; CLAUDE.md ≈14.7 KB, under 20,000, so no budget breaks — Card A k4 measures, and over 20,000 returns
  here). (a) `docs/DISPATCH_RULES.md`: a third main document (owner's word + axis-31 row), ≈8 pinned strings and their tests
  retargeted, the critic added as a reader. Either way COORDINATOR.md needs the owner's word; its row is written "owner word
  pending".
- **F5-r Copy mechanics.** (a) suffix `.py.next` + ONE `MetaPathFinder` loader in `tools/conftest.py` keyed by `<NAME>_PATH`
  (recommended: censuses over `tools/*.py` — test_streams S3, the mechanism closure test, K-STALE, the clone ratchet — never
  see a copy; imports between copies resolve in any order); (b) `*_next.py` + per-test-module loaders as in
  `test_permission_audit.py:23-39` (four test files gain a loader each; owns_gate's module-level `from dispatch_gate import`
  needs load order; S3 sees the copies of chain links that call `reconfigure(`); (c) a temp placement tree for the witness.
  Sub-option: `mechanism_gate.py` also as a copy (belt and braces; it fires only on a commit, and no builder commits here).
- **F8' Exams.** The F8 decision cannot run: `PROCESS/` holds 12 files, no CRITIC_EXAM.md / SCOUT_GOLDEN_SET.md
  (PROCESS/README.md:22-25). Recommended: the precedent line `Deviation: exam not run; debt F3-1` (no-briefs r2, commit
  1f165a38; D-0037). Alternative: generate the critic exam first (`.claude/skills/critic-exam-gen`), a separate node.
- **F12' Border counter (N1).** Recommended: §5.1 as written (line-start keywords + anywhere `if`, `lambda`, `and`, `or`;
  comment lines excluded; dict-dispatch by the Q-walk) — cost: docstring/string lines with those words force a re-review.
  Alternative: the critic's literal (b) + lambda, with `and`/`or` and dict entries judged by the Q-walk and the invariant
  weakened to "statement-level branches".
- **F15 (N4, B3 timing) Order and tree.** Recommended: §7 — one integration worktree, builders commit nothing, two critic
  topics (A+B2, then B1) with the Lead's placement between; +1 critic pass. Alternative: one topic, B1 runs before placement
  with `ROLE_CARRIERS_ROOT` (test_role_carriers_one_owner.py:29) on a temp placed tree and the copy loader; one critic pass,
  a harder card.
- **F16 (N2) Border base carrier.** Recommended: `reviewed:<sha>` token in the critic `delegated` notes (absent → `nobase`
  re-review). Alternative: a `reviewed_head` field in `tools/critic_verdict.schema.json` (critic.md rule 17 + schema +
  `critic_verdict_check.py` change; the critic cannot name a sha for an uncommitted state).
- **F17 Parallel stream.** Bounded-waits r2 (`docs/tasks/specs/20261117-bounded-waits-mechanism-spec-r2.md` :370-390) ships
  `session_context_next.py`, `compact_snapshot_next.py`, `dod_gate_next.py` with `SESSION_CONTEXT_PATH` and edits
  `test_session_context.py`; B1 owns `session_context.py` and `test_session_context.py`. Recommended: B1 starts after that
  stream merges (its placed `session_context.py` is B1's base; TEAMWORK §3); alternative: bounded-waits merges `main` after
  this wave and resolves. Both streams' loaders coexist (F5-r(a) ignores `.py` variables).

## §11 Small choices closed

- `COORDINATOR.md` at the root (matches `boot_path_files`' `[A-Z_]+\.md`, never listed by BOOT.md: e17).
- `## Worker duties` heading (it holds a builder duty and a duty of every worker); `## The dispatch form (rule 11)` heading;
  rule numbers kept; the agent_budget cap clause stays in Cost gates (the hook shows it to the worker).
- `tools/coordinator_rules.py` owns the list, so `agents_md` imports a light module, not the hook; prefix `COORDINATOR RULES:`.
- Re-review case `nobase`; `FACTS_KINDS` data row beside `HANDOFF_DIRS`; the facts branch after the handoff branch.
- `facts_check` unknown → note + pass, mirroring `handoff_folder_check` (one road for both header checks).
- K-STALE carries a Russian form (PROJECT.md, TESTING.md, RUNBOOK cite «правило N `CLAUDE.md`») and a `toolkit/` lookbehind.
- README.md and gateway/config.template.yaml join Card A (they carry stale citations); docs/ADOPTION_LEDGER.md is a record.
- Resume prints the "re-read only if" form; an empty coordinator file counts as MISSING.

## §12 Facts with carriers, and the reading trail

| fact | carrier | value |
|---|---|---|
| base | `.git/refs/remotes/origin/main`, `.git/refs/heads/main` | da47f648 both |
| deleted files | Glob `{factory-fixes.md,critic-diff-brief.md}` in docs/tasks (control found) ; `{BACKLOG.md,builder-rules.md}` in plans | critic-diff-brief.md, exchange-form.md, builder-rules.md absent |
| BOOT BUDGET / CLAUDE.md / incl. imports | t-1174 run at c75dd0c7 (estimate for da47f648) | 112646 / 51953 / 101738; re-measure: `python -B tools/session_context.py </dev/null \| grep BOOT` |
| CLAUDE_WARN, formula, MAX_LINES, `_ALWAYS_INCLUDE_BOOT_FILE` | session_context.py :235, :222-224, :190, :211 | 58500; ceil(m×1.15/100)×100; 25 |
| routing-policy anchors | install_parity_anchors.json :7-95 | 89 |
| role-carriers lines | test_role_carriers_one_owner.py | OWNER_KEYS CLAUDE.md 57-61; POINTERS 69-105; TOC 109-164; DELETED 254-263 |
| critic.md citations | Grep | 178, 198, 281 stale; 286-287 rule 11; 66 hygiene |
| builder.md citations | Grep | 67 hygiene; 107, 116, 117 stale |
| standing questions | critic.md :192 rule 22 Q1-Q12; :281 rule 24 Q13 | — |
| verdict schema | Grep `"[a-z_]+":` in critic_verdict.schema.json | no sha field |
| exams | Glob `*.md` in PROCESS (12 files) | no CRITIC_EXAM.md, SCOUT_GOLDEN_SET.md |
| uncommitted state in the main checkout | gitStatus at start | `M docs/OWNER_PRINCIPLES_INDEX.md`: measure on the integration tree, not here |

Section sizes (estimate, t-1174 script): hygiene 4386, r11 6975, enforcement 340, Язык 1167, cwd 910, COORD 43711 (with r11
out), PROJECT 34249. Lead `facts:` commands for r2: the BOOT line above; `python -B tools/owns_readers.py --base origin/main
--paths <Card owns> --names CLAUDE_WARN _ALWAYS_INCLUDE_BOOT_FILE ROOT_FILES MECHANISM_PREFIXES boot_path_files COORDINATOR_FILES`.

Read: t-1174 review whole; r1 spec whole; critic.md 50-74, 176-191, 279-303; designer.md 1-40; builder.md 100-134;
session_context.py 205-236, 1161-1324, 2600-2654; test_role_carriers_one_owner.py 30-335; SIBLING_MAP 473-562;
mechanism_gate.py 215-274; dispatch_gate.py 1-8, 741-785; dispatch_manifest.py 185-200; critic_snapshot.py 1-60;
compact_snapshot.py 280-295; conftest.py; test_permission_audit.py 15-39; install_parity_anchors.json 1-12, 88-101;
search_control_gate.py 14-23; escape_check.py 1-6; PATCH_PROTOCOL 14-23; PROCESS/README 15-29; LEAD_RANKING_EXAM 17-22; BOOT.md
1-20; bounded-waits r2 1-12. Greps: settings.json hook commands; `.githooks` tool references; import lines of the B1/B2 files;
the K-STALE regex per directory; `CLAUDE\.md` in agents, skills, PROCESS, PROJECT, RUNBOOK, TESTING, gateway, root files;
`reconfigure\(|import streams`; `_GATE_PATH|_PATH`; S4 in test_streams; install_parity unit checks; no-briefs r2 exam road.
Noticed, not widened: plans/piles/forge/README.md :33, :115, :221 name the deleted builder-rules file (excluded from scans; the
forge pile's zone). designer.md on disk is newer than the role text this session was started with (agent-definition cache).

## Lead decisions (Lead, 17.11.2026, Opus; «решила сама», the owner can stop or roll back)

- F1' = (d): rule 11 stays in the CLAUDE.md worker block; no `docs/DISPATCH_RULES.md`. COORDINATOR.md is a new main document:
  its axis-31 row stays «owner word pending» and Card A's move into COORDINATOR.md does not land in `main` before the owner's
  word (asked 17.11.2026); the cards are built and reviewed meanwhile.
- F5-r = (a): `.py.next` + one MetaPathFinder loader in `tools/conftest.py` keyed by `<NAME>_PATH`; `mechanism_gate.py` is NOT copied.
- F8' = the precedent line `Deviation: exam not run; debt F3-1`.
- F12' = §5.1 as written.
- F15 = §7 as recommended: one integration worktree, two critic topics (A+B2, then B1), the Lead places between.
- F16 = `reviewed:<sha>` token in the critic `delegated` notes; absent → `nobase` re-review.
- F17 = B1 starts after the bounded-waits r2 stream merges into `main`.
- Next: a critic re-review of r2 against verdict t-1174 (revision table + §10 decisions), then the cards.
