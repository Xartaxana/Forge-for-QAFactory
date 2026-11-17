# Spec draft t-1137: short worker boot (CLAUDE.md split) + fewer rounds (designer, 17.11.2026, r1)

Status: DRAFT for Lead acceptance. Decide the forks in §9 before any card goes out; F1, F5, F9 and F13 change card
text. Brief: Lead intent t-1137, the owner's words of 17.11.2026 («давай сделаем сейчас»; item 6 «ок»; item 7 «если
это не ухудшит качество, то ок»). Addition (same day, folded in): the border of item 6 («а когда лид будет проверять
правки … он эти ошибки пропустит?»); facts measured before the designer («да, поднимаем»); a critic topic holds at
most 3-4 nodes («принимаю»).

## §1 Scope, invariants, owners

- Nothing under `ai-packages/qa-factory/` changes, so no AR-n applies. `architecture:` and `judgment:` lines are not
  owed: `tools/architecture_gate.py` asks for them on package commits only. This is a forge MECHANISM commit: the
  axis block (§8) and `tier: opus`.
- Forge invariants:
  - I-1 MOVE: every rule sentence of today's CLAUDE.md and PROJECT.md has exactly ONE home after the commit, word for
    word. The exceptions are the pointer retargets of §3 and the new rules of §5.
  - I-2 ONE OWNER (axis 31): each K-OWN key keeps one carrier, and no pointer names a home its text has left.
  - I-3 GATE NET: moved rule text keeps its gates. `mechanism_gate.py` nets the new homes, and the install_parity
    anchors follow the text.
  - I-4 NO SILENT ABSENCE: a coordinator session either has its rules or sees a hook line saying they are missing.
  - I-5 WORKER SCOPE: nothing a worker auto-loads tells it to read the coordinator file.
- Who owns each check (P27 vocabulary, used here for the forge):

  | check | owner |
  |---|---|
  | the hook line, K-STALE / K-WORKER rows, CLAUDE_WARN=20000, the `facts:` header check | data (code) |
  | the Lead's own fix check | judgment of the Lead, a tier above the builder; its border is measured by code |
  | the designer cap / delta rule and the topic cap | judgment, accepted by the Lead |

  No census class applies: the census is package-only.

## §2 Part A: the split

| file | auto-loaded? | read by | content |
|---|---|---|---|
| `CLAUDE.md` | yes, every session and every worker | all | the worker-common block only (below); NO `@` imports |
| `COORDINATOR.md` (new, root) | no | the coordinator, at start and after compaction, via the hook line | CLAUDE.md's coordinator text: intro, Contents, Tiers, rules 1-10, 11a, 12, 13, Routing log, Role ≠ tier, Lead degradation; numbers and headings kept |
| `docs/DISPATCH_RULES.md` (new; F1) | no | coordinator (hook list), designer (role file), builder (DOC-DISPATCH pointer) | rule 11 whole: its four `### Rule 11 · …` blocks and the R11 table |
| `PROJECT.md` | no longer imported | coordinator (hook list) | unchanged, minus what moves to CLAUDE.md |
| `docs/FACTORY_RULES_INDEX.md`, `docs/ARCHITECTURE_INDEX.md`, `docs/OWNER_PRINCIPLES_INDEX.md` | no longer imported | coordinator (hook list); `architecture_gate.py` reads the AR index by path, as today | unchanged |

New CLAUDE.md, in order. Everything is a verbatim move unless marked NEW:

1. Title `# CLAUDE.md — QA Factory development` (an install_parity anchor).
2. NEW text, at most 600 bytes: "Auto-loaded into every session and every worker: only what every reader applies.
   A worker's own rules are `.claude/agents/<role>.md` and its dispatch. The coordinator's rules are not here: the
   SessionStart line `COORDINATOR RULES:` names their files." It never says "read COORDINATOR.md" (I-5).
3. `## Writing` (NEW heading): the enforcement-file sentence of rule 2 ("A self-activating enforcement file …"),
   moved out because it is a builder duty. Rule 2 keeps "(enforcement-file review rule: CLAUDE.md § Writing)".
4. `## Command hygiene (permission hygiene)` whole (points 1-7, both tables). In point 3, the tail "why and how to
   recover: PROJECT.md § Сессия форджа" is replaced by the PROJECT.md bullet «Рабочий каталог шелла не меняется
   никогда …», moved verbatim.
5. `## Язык` from PROJECT.md (F10). `## Ссылки на файлы в ответах` stays in PROJECT.md (F9).

Size of the new CLAUDE.md, an estimate (no shell in this role): about 10-11 KB, or 12-13 KB if F9 is rejected.
What keeps it from going lower:

- hygiene point 6 with its table, about 3 KB, applied by every worker;
- the Russian sections, at 2 bytes a character.

Card A measures the real size.

Trigger, the hook line:

- `tools/coordinator_rules.py` (new) is the one owner of
  `COORDINATOR_FILES = ("COORDINATOR.md", "PROJECT.md", "docs/DISPATCH_RULES.md", "docs/FACTORY_RULES_INDEX.md",
  "docs/ARCHITECTURE_INDEX.md", "docs/OWNER_PRINCIPLES_INDEX.md")` and of `coordinator_lines(root, source)`.
  `coordinator_lines` never raises and prints ASCII only.
- Startup, clear or compact: `COORDINATOR RULES: read <files> (<n> files, <bytes> bytes) before your first dispatch,
  acceptance or commit; workers never read them`.
- Resume: the same line, saying "re-read only if your context no longer holds them".
- Position: `session_context.main()` appends it after layer A and before `compact_snapshot_lines`.
  - It sits outside `build_context_lines`, so MAX_LINES=25 never cuts it.
  - `AFTER COMPACT:` stays last (pins: `test_compact_snapshot.py:684`, `test_session_context.py:3335`).
- SessionStart fires in the main session only. Measured: this designer subagent's context holds the auto-loaded
  CLAUDE.md and its imports, but no SessionStart line (`BOOT BUDGET`, `NOW` …).
- BOOT BUDGET: the coordinator files join the boot-path total. The `CLAUDE.md:` suffix now measures the worker
  auto-load. `CLAUDE_WARN` goes down to 20000; it is a named lowering, which the constant's comment calls always
  safe.

## §3 The DoD table: paragraph, home, reader

Reader codes:

- W: every worker and the coordinator (auto-load);
- C: the coordinator (hook line);
- D: the designer;
- B: the builder.

| # | paragraph / section today | home after | reader | edit beyond the move |
|---|---|---|---|---|
| C1 | title + intro "Auto-loaded into every session …" | title: CLAUDE.md; intro: COORDINATOR.md head | W / C | NEW head line: "read by the coordinator at start and after compaction (hook line); workers never read it" |
| C2 | "The project's own rules … imported here" + `@PROJECT.md` | sentence: COORDINATOR.md; `@` line deleted | C | "imported here" becomes "read with this file (hook line)" |
| C3 | "The factory building rules … AR-n" + 3 `@` index lines | sentence: COORDINATOR.md; `@` lines deleted | C | same wording swap |
| C4 | `## Contents — topic → where to read` | COORDINATOR.md | C | rows whose target moved are retargeted |
| C5 | `## Tiers` | COORDINATOR.md | C | none |
| C6 | Rule 1 + R1 | COORDINATOR.md | C | none |
| C7 | Rule 2, implementation / witness | COORDINATOR.md | C | the enforcement-file sentence becomes a pointer |
| C7a | the enforcement-file sentence | CLAUDE.md § Writing | W | none |
| C8 | Rule 2, drafting → designer | COORDINATOR.md | C | + the facts rule (§5) |
| C9-C12 | Rule 3; Rule 4, parallel; Rule 4, witness / BATCH CANON; Rule 4a | COORDINATOR.md | C (B reads builder-rules 7b, as today) | none |
| C13-C17 | Rules 5, 6, 7, 8, 9 | COORDINATOR.md | C (role files restate 5 and 9's worker part) | none |
| C18-C19 | Rule 10, four questions; Rule 10, a package change | COORDINATOR.md | C, D (designer rule 1 cites 10) | none |
| C20-C23 | Rule 11, all four blocks + R11 | docs/DISPATCH_RULES.md | C, D, B | COORDINATOR.md keeps the stub `### Rule 11 · the dispatch form — docs/DISPATCH_RULES.md` |
| C24-C25 | Rule 11a; Rule 12, cadence | COORDINATOR.md | C | none |
| C26 | Rule 12, Cost gates | COORDINATOR.md | C | + item-6 text (§5) |
| C27 | Rule 13 + R13 | COORDINATOR.md | C | R13-g + the topic cap (§5) |
| C28-C32 | Routing log: intro + json; append-only; base fields; typed fields; SHAPES + paragraph | COORDINATOR.md | C | none (W keeps hygiene point 5) |
| C33-C34 | Role ≠ tier; Lead degradation | COORDINATOR.md | C | none |
| C35-C37 | hygiene intro and points 1-5; point 6 + table; point 7 | CLAUDE.md | W | point 3: the pointer is replaced by P11a |
| P1 | PROJECT.md title + "Два набора правил" | PROJECT.md | C | none |
| P2 | "Этот файл читает КАЖДАЯ сессия …" | PROJECT.md | C | becomes «координатор каждой сессии при старте и после сжатия (строка `COORDINATOR RULES:`); воркеры его не читают» |
| P3 | Оглавление | PROJECT.md | C | Язык row → `CLAUDE.md` § Язык; the last row → `COORDINATOR.md` § Contents |
| P4 | Где что лежит | PROJECT.md | C | + rows for COORDINATOR.md and DISPATCH_RULES.md |
| P5-P10 | Принципы; Пакет 1-2; Пакет 3-6; Бэклог; Новая идея; Прогоны | PROJECT.md | C (B gets factory-rules whole in given, p.1) | none |
| P11a | Сессия форджа: the cwd bullet | CLAUDE.md, hygiene point 3 | W | none |
| P11b | Сессия форджа: connectors, compaction | PROJECT.md | C | none |
| P12 | Командная работа 1-13 + closing line | PROJECT.md | C | п.12 «Критик кода — один на тему» gets «(до 4 узлов: R13-g)» |
| P13, P14, P16, P17 | Релиз; Как пишутся правила; Что решать самому; Ссылки (F9) | PROJECT.md | C | none |
| P15 | Язык | CLAUDE.md (F10) | W | none |
| X1-X3 | FR / AR / P indexes | not imported | C | none |

Deleted as duplicates: only the four `@` lines, and the point-3 pointer whose target text now stands in its place.

Who needs each index at boot (item 5):

- FR index: the coordinator only; a package builder gets the whole rules file (PROJECT p.1).
- AR index: the coordinator (specs, commit lines, acceptance); the gate reads it by path; the designer reads
  `architecture.md` itself; the critic: F3.
- P index: the coordinator only. Critic 19 and designer 6 reach P31 through PROJECT.md, which points to
  `docs/OWNER_PRINCIPLES.md`.

## §4 Machine readers (rule 7)

The searches behind this table:

| search | where | hits |
|---|---|---|
| `CLAUDE\.md\|PROJECT\.md\|FACTORY_RULES_INDEX\|ARCHITECTURE_INDEX\|OWNER_PRINCIPLES_INDEX` | `tools/` | 385 in 59 files |
| the same | `.githooks/` | 5 in 1 file |
| the same | `.claude/` | timed out on `worktrees/`; narrowed: agents 4 files + judge, skills 4 files |
| `CLAUDE\.md`? (rule\|§\|routing rule\|command hygiene\|«\|"Routing)` | repo minus history and worktrees | 134 in 43 files |
| `(?i)coordinator\.md\|dispatch_form\|coordinator_rules` | repo | 8 hits, all the unrelated `DISPATCH_FORM_REFUSES`: the positive control for "no reader of the new names yet", and the reason for the name DISPATCH_RULES |

| reader | verdict |
|---|---|
| `tools/session_context.py` (`_ALWAYS_INCLUDE_BOOT_FILE`, `CLAUDE_WARN` 58500, F6-27 import counting, main()) | changes in B1 |
| `tools/test_session_context.py` 1035-1140, 3173-3350 | changes in B1; existing rows stay, new variant rows |
| `tools/test_compact_snapshot.py:684` | unchanged (position kept) |
| `tools/agents_md.py` + `test_agents_md.py` 73-106 (asserts the PROJECT.md / FR index imports) + `AGENTS.md` (pre-commit and CI `--check`) | changes in B1: appends `COORDINATOR_FILES` under the same markers (F7); the fixture copies them; AGENTS.md regenerated |
| `tools/install_parity_anchors.json`, CI `install_parity.py --check`: unit `routing-policy` (88 anchors), `role-profiles:designer` anchor "the text is CLAUDE.md rule 11", `process-docs:lead-ranking-exam` anchor "2. Claude Code subagents auto-load CLAUDE.md, so the policy is" | changes in B1: `routing-policy` → host COORDINATOR.md; rule-11 anchors → a unit on DISPATCH_RULES.md; `routing-policy:hygiene` → host CLAUDE.md (title, enforcement-file, hygiene anchors); the two anchors follow A's new text |
| `tools/mechanism_gate.py` MECHANISM_PREFIXES; `test_mechanism_gate*.py` | changes in B1: + `COORDINATOR.md`, `docs/DISPATCH_RULES.md`, `tools/coordinator_rules.py` (transitive-import test); + a COORDINATOR variant row |
| `tools/claim_control_gate.py` ROOT_FILES + its test | changes in B2: + `COORDINATOR.md` |
| `tools/tests/test_role_carriers_one_owner.py` OWNER_KEYS 47-50, POINTERS 62/64/65/69/72/74/75/77/94, TOC 107-158 | changes in B1: rule-11 → DISPATCH_RULES; rule-9 and cost:cap → COORDINATOR; hygiene-6 stays; `_TOC_CL` = COORDINATOR.md; + K-STALE, K-WORKER |
| `tools/escape_check.py` + `escape_allowlist.json` | unchanged: `entries` is empty |
| `tools/permission_audit.py` HYGIENE_CLASS_LABELS | unchanged: hygiene stays |
| `tools/dispatch_gate.py` 620/710, `dispatch_manifest.py` 138, `journal_write.py` 58/422, `journal_validator.py` 153/315/679, `journal_hooks.py` 41, `hook_liveness_probe.py` 1273 anchor | changes in B2 (citations) |
| `tools/dispatch_manifest.py` + `tools/dispatch_new.py` (header lines) | changes in B2: the `facts:` header (F13) |
| comment citations: search_control_gate, owns_gate, owns_verify, handoff_gate, journal_echo, judge_calib_sanitize, calibration_counts, escape_check; mechanism_gate 14/293 | changes in B2; mechanism_gate's in B1 |
| `tools/architecture_index.py:5` docstring | changes in B1 (docstring; the cap stays) |
| `factory_rules_index.py`, `architecture_gate.py`, `owns_readers.py`, `md_table.py`, `md_regions.py`, `hop_metrics.py`, `wiring_check.py`, `agent_budget.py`, `piles.py`, `language_sites.py`, `hook_liveness_probe.py` 971-984, `tools/fixtures/*` | unchanged; each mention stays true or is a fixture |
| `.githooks/pre-commit` 50-61 comments | changes in B1, handed as `.githooks/pre-commit.next` |
| `.claude/settings.json` SessionStart | unchanged |
| `.claude/agents/designer.md` 17/24/32 | changes in A; 83 "PROJECT.md P31" unchanged |
| `builder.md` 62, `critic.md` 66/165 | unchanged (targets stay valid) |
| `builder.md` rule 4 (+ DOC-DISPATCH pointer), `judge.md` 3/16 | changes in A |
| skills: boot-diet 8/21-24/85/99-108/123, session-handoff 24/56, permission-audit 52/60, scout-exam-gen 64 | changes in A (boot-diet item 6 becomes «CLAUDE.md не импортирует ничего: импорт грузится в каждого воркера; текст координатора — COORDINATOR.md») |
| PROCESS: WEEKLY_CALIBRATION 88/140/195/207/498/689/694/1006/1045; LEAD_RANKING_EXAM 19; JUDGE_CALIBRATION 78/96 | changes in A |

## §5 Part B: rule texts

### Item 6 + addition 1: home COORDINATOR.md rule 12 Cost gates, after "a re-review carries only the fix diff and the verdict;"

> After a critic verdict `fit_with_fixes` on CODE, the Lead checks the fix round ITSELF only inside this border
> (the owner's word 17.11.2026): the fix diff does exactly what the verdict's `fixes` prescribe and adds no new
> logic — no new function, branch, state or write path. Measured on the fix diff (`git diff -U0 <verdict sha>..HEAD
> -- '*.py'`, added lines only): zero lines matching
> `^\+\s*(def |class |async def |if |elif |else\b|try:|except\b|finally:|for |while |match |case )`, zero new files,
> zero added `add_argument(`, zero added write calls (`write_text|write_bytes|open\(.*['"][wax]|append_jsonl|
> \.write\(`), and no line outside the owns the verdict reviewed. Inside the border, the Lead walks the fix diff by
> the critic's standing questions — today `docs/tasks/critic-diff-brief.md` items 1-12; after the no-briefs fold,
> the critic role-file rule that holds them — one line per question, plus one line per fix (`fixed: <where>` /
> `not fixed` → another fix round). The `accepted` notes carry `fixes checked by Lead: <verdict path>, border 0`.
> Outside the border (any count above zero), when the verdict was `blocker`, when a fix cannot be matched to its
> verdict line, or when the acceptor is not strictly above the builder's tier (Role ≠ tier), a critic re-review
> carries only the fix diff and the verdict, and its dispatch names its case: `re-review: logic|blocker|unmatched|
> tier`. Plans keep PROJECT.md new idea, step 6.

- Invariant: no new logic is ever accepted without a critic. The Lead's check covers only edits the critic
  already prescribed, and it walks the same questions the critic would.
- Error direction: the border counter may err only toward a re-review. Adversarial inputs that must stay outside
  the border:
  - a ternary or `and/or` short-circuit hiding a branch (a fork F12 option adds `\bif\b.*\belse\b` on one line);
  - a lambda;
  - a new dict entry used as a dispatch table;
  - a non-`.py` change: a JSON data row, a hook config. Any non-`.py` file other than `.md` counts as outside.
- Detector: calibration check 17 gets a sub-item.
  - (a) A re-review whose dispatch names no case. That is a wasted round.
  - (b) An `accepted` after `fit_with_fixes` with neither `fixes checked by Lead` nor a re-review. That is a
    skipped check.
  - (c) A sample re-run of the border counter on (a)/(b) commits.

### Addition 3: home COORDINATOR.md R13-g (and PROJECT п.12 pointer)

> One critic pass per TOPIC, and a topic holds at most 4 nodes (the owner's word 17.11.2026); a fifth node opens a
> new topic, split by disjoint owns or seams.

- Invariant: per-node critics stay unreachable; the topic count grows only by splitting.
- Detector: check 2's cumulative subcase counts nodes per critic `delegated` (`node` field, notes).

### Addition 2: home COORDINATOR.md rule 2 drafting (+ designer.md rule 3, + the dispatch header)

> Before a designer dispatch the Lead MEASURES the brief's load-bearing facts by code (the owner's word
> 17.11.2026). A load-bearing fact is any claim about the CURRENT repo or data that a requirement, an edge or a
> reader list rests on:
> - a file, function, constant, field, CLI flag or hook that exists, and its shape or value;
> - a count (readers, hits, sizes, lines);
> - a test pin or anchor text;
> - a data premise (PROJECT.md p.6(а)).
>
> Each fact goes into the dispatch as a `facts:` header line block, one line each:
> `<claim> | <command> | <verbatim result, at most 200 chars>`. When the brief rests on none, the block is
> `facts: none -- <why>`. Opinions, intent and the owner's words are not facts: they go in the brief.

- The designer side, added to designer.md rule 3: "facts in `facts:` are the Lead's measurement and may be cited
  with their command; a load-bearing fact the draft adds is measured by the designer the same way and listed in
  the trail."
- Invariant: no spec premise about the repo rests on memory. Every premise has a command, either the Lead's or
  the designer's.
- Detector:
  - `rejected` with `failure_class: spec`, whose note names a premise without a `facts:` line;
  - code: F13.

### Item 7: home designer.md, new rule 8; rule 4 says "Write and Edit"; frontmatter `tools: Read, Glob, Grep, Write, Edit`

> 8. Size and fix rounds (the owner's word 17.11.2026, «если это не ухудшит качество»). The draft file is at most
> 40,000 bytes on disk (`python -B -c "import os,sys;print(os.path.getsize(sys.argv[1]))" <path>`). A draft that
> will not fit returns `decomposable: <parts by disjoint owns>` before writing past the cap. Edges, invariants,
> readers, forks and the trail are never trimmed to fit. A FIX ROUND (its `handoff:` names the earlier draft)
> EDITS that file in place:
> (a) a `## Revision rN` block at the top, one line per finding or decision: `<id> -> change -> section`;
> (b) every builder card it touches is rewritten WHOLE in place;
> (c) untouched sections stay byte-identical;
> (d) a revision touching more than half of the cards, or §1, is a full rewrite.
> The file at `handoff:` is always the complete current spec: a builder reads one document and never merges two.

- Quality: whole cards always; `git diff` of the card proves (c); the cap splits by owns and never trims; critic-on-
  plan still sees every part.
- `handoff_gate.py` already gates Edit for the designer (`WRITE_TOOLS`, `GATED_KINDS`, lines 68-69).
- Detector: check 28 gets a sub-item: drafts over 40,000 bytes, and fix rounds whose `git diff --stat` breaks (d).
- Note: this draft was written by Write, twice. The designer still has no Edit, and the coordinator's addition came
  mid-task.

## §6 Edges, with the invariant each protects

1. A coordinator file missing, empty, a directory or unreadable prints, per file, `COORDINATOR RULES: MISSING <path>
   (<reason>) -- read it from git: git -C <root> show origin/main:<path>; until then this session has no coordinator
   rules`. The good files are still listed.
   - Invariant: I-4.
   - Error direction: always toward MISSING. Adversarial inputs: a 0-byte file, a directory, a permission error,
     non-UTF-8. Presence is judged by `stat`, never by decoding.
2. The import or run of `coordinator_rules.py` fails: `COORDINATOR RULES: unavailable (<exc>) -- read <literal
   list> yourself`. That literal is the one fallback copy, and a test row pins it equal to `COORDINATOR_FILES`.
   - Invariant: the hook never fails the session start, and the read duty still appears.
3. A worker sees no line, because SessionStart does not fire for it. CLAUDE.md names no read duty (I-5; the
   K-WORKER row).
4. A parallel old worktree keeps working.
   - Its workers auto-load that tree's long CLAUDE.md, which holds every rule; it is a move, so nothing in it is
     wrong, only dearer.
   - A coordinator session there runs that tree's old hook: no line, but a complete CLAUDE.md.
   - Invariant: the rules a session can reach = its tree's CLAUDE.md ∪ its tree's hook-listed files. Hook code and
     CLAUDE.md are one generation per tree.
5. Merging an old branch that edited a moved paragraph conflicts on CLAUDE.md. The merger re-applies the edit in
   COORDINATOR.md (TEAMWORK §3).
   - Invariant: one home per rule. K-OWN turns red on a doubled key, and the CLAUDE.md WARN fires above 20000.
6. Compaction: the line prints again before `AFTER COMPACT`. Resume: the "re-read only if" form.
7. MAX_LINES=25 can never cut the line.
8. Temporal: COORDINATOR.md, DISPATCH_RULES.md, `coordinator_rules.py` and the `facts:` check do not exist before
   the commit and land in ONE Lead commit.
   - A designer dispatch drafted before the commit and sent after it lacks `facts:` and is refused with the door
     `facts: none -- <why>`.
   - Fixtures K4/K8 in `tools/fixtures/dispatch_manifest/` are judged under the new rule. Whether they now refuse
     is B2's case table.
9. Codex AGENTS.md gets CLAUDE.md plus every coordinator file, the same text as today, reordered (F7).
10. "No meaning change" against "retarget pointers": a retarget changes only the home a citation names. A pinned
    string changes in the same card as its test.
11. "Workers do not read the coordinator file" against "the designer and builder need rule 11": DISPATCH_RULES.md
    resolves it (F1).
12. Each coordinator file stays under the Read tool's default (about 25K tokens). COORDINATOR.md is about 37 KB of
    English (an estimate); Card A reports the real sizes.
13. The Lead ranking exam (a subagent) loses the policy auto-load. Its item 2 now says the dispatch attaches
    COORDINATOR.md whole, which keeps the "FAIR condition".
14. The item-6 border on a diff that touches only `.md` files: zero by construction. Allowed, because prose is
    reviewed by the standing questions.
15. A topic of exactly 4 nodes is legal; 5 splits.

## §7 Builder cards (paths under `C:/QAFactory/forge-repo/`)

Order: A and B2 run in parallel (disjoint). B1 runs after both, on the same branch, because its pins read A's text
and B2's strings. One Lead mechanism commit.

### Card A: the text move (docs)

- given: this spec §2, §3, §5, §6; CLAUDE.md; PROJECT.md; the four role files; critic-diff-brief.md.
- owns:
  - `CLAUDE.md`, `COORDINATOR.md` (new), `docs/DISPATCH_RULES.md` (new), `PROJECT.md`, `BOOT.md`
  - `.claude/agents/designer.md`, `.claude/agents/builder.md`, `.claude/agents/judge.md`
  - `.claude/skills/boot-diet/SKILL.md`, `.claude/skills/session-handoff/SKILL.md`,
    `.claude/skills/permission-audit/SKILL.md`, `.claude/skills/scout-exam-gen/SKILL.md`
  - `docs/tasks/critic-diff-brief.md`, `plans/builder-rules.md`, `docs/RUNBOOK.md`,
    `docs/CLAUDE_HOST_ADAPTATIONS_FULL.md`, `SYSTEM_PROMPT.md`, `docs/SIBLING_MAP.md`
  - `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md`, `PROCESS/LEAD_RANKING_EXAM.md`, `PROCESS/JUDGE_CALIBRATION_PROTOCOL.md`
  - `DELEGATION_TABLE.md`, `delegation.config.yaml`, `docs/TESTING.md`, `gateway/config.template.yaml`
- Behaviour:
  1. Build CLAUDE.md, COORDINATOR.md and DISPATCH_RULES.md by §2 and §3, line by line.
  2. Apply §3's last column and nothing more.
  3. Put in place §5's texts: Cost gates, R13-g, the rule-2 facts rule, designer.md rules 3, 4 and 8 plus the
     frontmatter `Edit`, and PROJECT п.12's pointer.
  4. designer.md: `CLAUDE.md rule 11` becomes `docs/DISPATCH_RULES.md` rule 11; rule 2 and rule 10 become
     `COORDINATOR.md`.
  5. builder.md rule 4: append "A doc-only witness: `docs/DISPATCH_RULES.md` § DOC-DISPATCH WITNESS." Line starts
     are anchors: keep them.
  6. Retarget every remaining citation of a moved rule in the owned files.
  7. BOOT.md lines 5-8: name the worker block and the `COORDINATOR RULES:` line.
  8. LEAD_RANKING_EXAM item 2 per edge 13.
  9. Calibration:
     - check 10 and check 33(h) name the new files;
     - check 2 counts nodes per topic;
     - check 17 gets the item-6 sub-item;
     - check 28 gets the item-7 sub-item;
     - check 7 gets a new sub-item: the first Task/Agent call of a main session, after a start or a compaction,
       follows a Read of COORDINATOR.md.
  10. Report the new texts of the two changed install_parity anchor lines for B1.
- Edges: §6. A sentence whose home §3 does not decide comes back as a question. Russian moves verbatim.
- DoD: a DOC-DISPATCH witness (DISPATCH_RULES § DOC-DISPATCH WITNESS: keys verbatim, full script source in the
  report, a negative control). The script is a scratch file, never committed. It checks:
  - (k1) Every line of 8 or more characters in `git -C C:/QAFactory/forge-repo show HEAD:CLAUDE.md` and in
    `HEAD:PROJECT.md` occurs in exactly one of CLAUDE.md / COORDINATOR.md / docs/DISPATCH_RULES.md / PROJECT.md.
    The exception is the edited-lines list, given in the report as old → new, each line a §3 row.
  - (k2) These keys are present:
    - CLAUDE.md: `## Command hygiene (permission hygiene)`, `` `COORDINATOR RULES:` ``, `## Язык`;
    - COORDINATOR.md: `## Role ≠ tier`, `## Lead degradation`, `## Routing log — logs/journal/<dev>.jsonl`,
      `### Rule 12 · Cost gates`, `fixes checked by Lead:`, `at most 4 nodes`, `` `facts:` ``;
    - DISPATCH_RULES.md: `11. DoD in every dispatch (DoD-in-every-dispatch rule)`, `DOC-DISPATCH WITNESS:`;
    - designer.md: `## Revision rN`, `40,000 bytes`.
  - (k3) CLAUDE.md has no `^@` line and no `read COORDINATOR` (case-insensitive).
  - (k4) Print the byte sizes; CLAUDE.md must be under 20000.
  - Negative control: a copy of COORDINATOR.md without `## Lead degradation` must fail.
- siblings: axis 1 here; axis 31 judged in B1.
- non-goals: tools/; critic.md and scout.md (an exam is owed on any edit); ai-packages/.

### Card B2: citation strings + `facts:` header (parallel with A)

- given: §4 rows marked B2; §5 addition 2; the homes (rule 11 → `docs/DISPATCH_RULES.md`; the other moved rules →
  `COORDINATOR.md`; hygiene stays `CLAUDE.md`).
- owns:
  - `tools/dispatch_gate.py`, `tools/test_dispatch_gate.py`, `tools/dispatch_manifest.py`,
    `tools/test_dispatch_manifest.py`, `tools/dispatch_new.py`, `tools/fixtures/dispatch_manifest/`
  - `tools/journal_write.py`, `tools/journal_validator.py`, `tools/journal_hooks.py`, `tools/journal_echo.py`,
    `tools/test_journal_echo_escalation.py`
  - `tools/hook_liveness_probe.py`, `tools/claim_control_gate.py`, `tools/test_claim_control_gate.py`
  - `tools/search_control_gate.py`, `tools/owns_gate.py`, `tools/owns_verify.py`, `tools/handoff_gate.py`
  - `tools/judge_calib_sanitize.py`, `tools/calibration_counts.py`, `tools/escape_check.py`, `tools/test_piles_take.py`
- Behaviour:
  1. Replace each citation of a moved rule with its new home. A pinned refusal string changes together with its
     test and with the probe anchor at line 1273.
  2. ROOT_FILES += `"COORDINATOR.md"`.
  3. F13: for a designer dispatch, `dispatch_manifest` requires a `facts:` header (one or more lines, or
     `facts: none -- <why>`) and its refusal names that door; `dispatch_new.py` prints the line. The rule is read
     by the role key `designer`, through the same path as `designer:`.
- Edges:
  - A non-designer dispatch is unaffected.
  - `facts:` with empty content is refused.
  - `none` without ` -- <why>` is refused.
  - Fixtures K4/K8 get a case row each (§6.8).
  - A fixture's own citation text stays.
- DoD: `python -m pytest tools/test_dispatch_gate.py tools/test_dispatch_manifest.py tools/test_journal_echo_escalation.py
  tools/test_claim_control_gate.py tools/test_piles_take.py tools/test_hook_liveness_probe.py -q`, green.
- siblings: axis 13 (dispatch-text readers): new header item; `dispatch_gate` reads through `dispatch_manifest` only.
- non-goals: everything else; no behaviour change beyond (3).

### Card B1: hook line, generators, gates, pins (after A and B2)

- given: this spec; Card A's report.
- owns:
  - `tools/coordinator_rules.py` (new), `tools/session_context.py`, `tools/test_session_context.py`
  - `tools/agents_md.py`, `tools/test_agents_md.py`, `AGENTS.md`
  - `tools/mechanism_gate.py`, `tools/test_mechanism_gate.py`, `tools/test_mechanism_gate_md.py`
  - `tools/install_parity_anchors.json`, `tools/tests/test_role_carriers_one_owner.py`
  - `tools/architecture_index.py` (docstring only)
  - `.githooks/pre-commit.next`
- Behaviour:
  1. Build `coordinator_rules.py` per §2 and edges 1, 2, 6.
  2. Wire `main()` per §2. Set `CLAUDE_WARN = 20000`, with a "Re-derived 2026-11-17 (t-1137)" comment. Add the
     coordinator files to `boot_path_files`.
  3. `agents_md` appends `COORDINATOR_FILES` under the import markers.
  4. MECHANISM_PREFIXES += the three paths.
  5. Split install_parity per §4, with the two new anchors.
  6. Role carriers per §4:
     - K-STALE: no scanned file matches `CLAUDE\.md(?:'s)?`?\s+(?:routing\s+)?rules?\s+\d` or names CLAUDE.md
       § Tiers / Rule / Routing log / Role ≠ tier / Lead degradation / Contents;
     - `docs/ADOPTION_LEDGER.md` joins EXCLUDED as a record;
     - K-WORKER: CLAUDE.md has no `@` line and no `read COORDINATOR`.
  7. Regenerate AGENTS.md.
  8. `pre-commit.next`: the whole file, with comments 50-61 retargeted.
- Edges:
  - install_parity may refuse two units on one `kit_path`. Then return a question.
  - Changed BOOT BUDGET pins: compute the expected value from the fixture.
  - New cases are variant rows: line present / missing / empty / directory / import fails / resume / compact order;
    fallback list == `COORDINATOR_FILES`.
- DoD:
  - `python -m pytest tools/test_session_context.py tools/test_compact_snapshot.py tools/test_agents_md.py
    tools/test_mechanism_gate.py tools/test_mechanism_gate_md.py tools/test_install_parity.py
    tools/tests/test_role_carriers_one_owner.py -q`
  - then `python -B tools/agents_md.py --check`, `python -B tools/install_parity.py --check`,
    `python -B tools/architecture_index.py --check`, `python -B tools/factory_rules_index.py --check` and
    `python -B tools/session_context.py < NUL`
  - The witness carries the `BOOT BUDGET`, `CLAUDE.md:` and `COORDINATOR RULES:` lines verbatim.
- siblings: axis 31; axis 18 (CLAUDE_WARN lowered, named); axis 1 (AGENTS.md).
- non-goals: doc text (A); other tools (B2).

## §8 Mechanism commit: four questions and axes

- M1, the split and the hook line:
  - (a) The coordinator pays one Read of 6 files (about 25-30K tokens) per start or compaction, which it already
    paid through auto-load. Each worker call drops from about 99 KB to about 11 KB (an estimate). An author pays one
    placement choice.
  - (c) The line itself; K-OWN, K-STALE and K-WORKER; install_parity in CI; the 20000 WARN; check 7's sub-item.
  - (d) SessionStart, in code. The read itself is discipline, with check 7 as the leak detector (F4).
- M2, the Lead's fix check with its border:
  - (a) The Lead pays a counter run plus a 12-question walk; one critic run is saved per pure fix round.
  - (c) Check 17 (a-c).
  - (d) The border is a command; its use is discipline plus check 17. Promotion goes into `dispatch_gate` (a
    re-review case line) on a leak.
- M3, the designer cap and delta:
  - (c) Check 28.
  - (d) Discipline; `handoff_gate` confines Edit; promotion to `dod_gate`.
- M4, the topic cap:
  - (a) Splitting topics adds critic passes beyond 4 nodes.
  - (c) Check 2.
  - (d) Discipline.
- M5, facts before the designer:
  - (a) The Lead runs about 3-10 commands per brief.
  - (c) `rejected` with `failure_class: spec` naming an unmeasured premise.
  - (d) Code: the `dispatch_manifest` refusal (F13).
- (b) Axes, one block for M1-M5:

  | axis | verdict |
  |---|---|
  | 1 | covered: policy, role files and AGENTS.md in one commit; journal untouched |
  | 2 | covered: F8 (critic and scout exams after the context shrinks) and Lead exam item 2; designer has no exam |
  | 3, 4 | n/a: no package change; indexes unchanged, only who reads them |
  | 5-11 | n/a: package / test identity |
  | 12 | n/a: pile rules unchanged |
  | 13 | covered: refusal texts plus the `facts:` item, the cut unchanged (B2) |
  | 14 | n/a now (check 7 reads transcripts by hand; queued with F4) |
  | 15-17 | n/a |
  | 18 | covered: CLAUDE_WARN lowered and named |
  | 19-30 | n/a: package readers |
  | 31 | covered: owners, pointers, TOC, K-STALE |
  | 32, 33 | n/a |
  | 34 | covered: one CLAUDE.md for every Claude Code worker, one hook set per coordinator; Codex asymmetry stated (F7); the `facts:` rule is read by role key, not by name |
  | 35-38 | n/a: package |

  Commit lines: this block and `tier: opus`.

## §9 Forks (the Lead decides)

- F1. Rule 11's home.
  - (a) `docs/DISPATCH_RULES.md`, read by the coordinator, the designer and the builder (recommended).
  - (b) The designer reads the rule-11 blocks of COORDINATOR.md. This breaks the brief's edge.
  - (c) The Lead attaches rule 11 to every designer dispatch.
- F2. PROJECT.md stays one file, no longer imported (recommended: every pointer stays valid), or merges into
  COORDINATOR.md, which costs about 40 retargets.
- F3. Package critic dispatches lose the AR and FR indexes. Recommend: they carry `design/architecture.md` and
  `design/factory-rules.md` in given, like the builder's (one line in PROJECT p.1; a meaning change). The
  alternative accepts the loss.
- F4. Enforcement of the coordinator read.
  - (a) The hook line plus check 7 (recommended; rule 10(d)).
  - (b) Also a `dispatch_gate` refusal when there is no Read of COORDINATOR.md since the last start or compaction
    (axis 14, one transcript read per dispatch).
- F5. Hook placement.
  - Recommend: B1 and B2 edit the live hook scripts in their OWN worktree. They activate only through the Lead's
    `wave.py merge`, which is the Lead's placement after review. Only `.githooks/pre-commit` is handed as `.next`.
  - The alternative is `.next` copies plus a test harness per card.
- F6. Card cap: 40,000 bytes (recommended), 30,000, or 12 KB per builder card.
- F7. Codex: AGENTS.md keeps the full text (recommended) or gets only the worker block.
- F8. Run `PROCESS/CRITIC_EXAM.md` and `PROCESS/SCOUT_GOLDEN_SET.md` once after B1, since the workers' context
  shrinks (recommended), or skip them because the role text is unchanged.
- F9. Link form.
  - Recommend: it stays in PROJECT.md (coordinator only). The brief listed it as auto-loaded, but it contradicts
    the workers' absolute-path hand-backs.
  - The alternative moves it into CLAUDE.md with the line "workers: absolute paths in hand-backs".
- F10. Language: the whole § Язык into CLAUDE.md (recommended), or only its package-English bullet.
- F11. The topic cap: 4 nodes (recommended: the owner said "3-4", and 4 is the larger legal value), or 3.
- F12. The border counter.
  - (a) The keyword regex of §5 (recommended; it errs toward a re-review).
  - (b) Plus same-line `if … else` and `lambda`.
  - (c) An AST diff of function and branch counts, more exact but a new tool.
- F13. Facts gate.
  - (a) `dispatch_manifest` refuses a designer dispatch without `facts:` (recommended: the owner raised its
    priority; the cost is small, in B2).
  - (b) Discipline plus the `rejected` detector only.
- F14. Pointer to the standing questions. Today they are `docs/tasks/critic-diff-brief.md` items 1-12; the
  no-briefs fold has NOT landed in main (critic.md has no Q1-Q13; read here).
  - Recommend: the rule cites the brief now, and the fold node retargets it in its own commit.
  - The alternative waits for the fold.

## §10 Small choices closed

- `COORDINATOR.md` at the root: it matches `boot_path_files`' `[A-Z_]+\.md`.
- `docs/DISPATCH_RULES.md`: the name avoids colliding with `DISPATCH_FORM_REFUSES`.
- The list owner is `tools/coordinator_rules.py`, so agents_md imports a light module, not the hook.
- The prefix is `COORDINATOR RULES:`.
- Rule numbers are kept.
- Russian moves verbatim.
- ADOPTION_LEDGER is treated as a record.
- Resume prints the "re-read only if" form.
- An empty file counts as MISSING.
- Card order: A and B2 in parallel, then B1. claim_control_gate goes to B2 whole.
- The border counts `.py` added lines only. A non-`.py`, non-`.md` file falls outside the border.

## §11 Reading trail

Read:

- `tools/session_context.py` 205-244, 1155-1189, 2440-2459, 2570-2660;
- `tools/escape_check.py` 1-40; `tools/escape_allowlist.json`; `tools/install_parity_anchors.json`;
- `tools/mechanism_gate.py` 205-269; `tools/agents_md.py` 1-66; `tools/test_agents_md.py` 69-107;
- `tools/tests/test_role_carriers_one_owner.py` 1-160; `tools/claim_control_gate.py` 244-259;
- `tools/permission_audit.py` 168-187;
- `BOOT.md`; `.claude/agents/{critic,builder,scout}.md`.

Greps:

- the §4 patterns;
- in `session_context.py`: main, source and layer-A names;
- `.githooks/pre-commit` and `.github/workflows` (CI 77-94, pre-commit 42-61);
- `test_*.py` for `CLAUDE_WARN|AFTER COMPACT`;
- `PROCESS/` for CLAUDE.md; SIBLING_MAP headings (38 axes);
- in critic-diff-brief: `(?i)re-review|fix round|fix diff|the two layers` (control found, the others absent) and
  `^\d+\. \*\*` (items 1-12);
- `designer.md` frontmatter (`tools: Read, Glob, Grep, Write`); Edit handling in `handoff_gate.py`.

In context at start: CLAUDE.md, PROJECT.md, the three indexes, designer.md.

## Lead decisions on the forks (17.11.2026, «решила сама», до слова владельца)

- By recommendation: F1 (a), F2, F3, F4 (a), F6 40,000 bytes, F7, F8, F9, F10, F11 = 4, F12 (a), F13 (a).
- F5 = the alternative: hook scripts go as `.next` / `*_next.py` copies with the `*_PATH` test variable, as in the
  bounded-waits cards. Reason: a worker's hooks run from its own worktree, so an edited live hook would gate the builder
  that wrote it before any review.
- F14 = the alternative: this spec is built after the no-briefs waves, so the rule cites the critic role file's Q1-Q13
  directly; no interim pointer to the brief.
