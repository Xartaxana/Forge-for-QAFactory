# t-1117 — No standing briefs: fold every brief into the main documents (DRAFT, designer)

Status: designer draft for Lead acceptance; a plan critic follows (PROJECT.md «Как разрабатывается новая идея владельца», step 6).
Feature: F19. Language: this draft is English; texts that land in Russian documents are given in Russian.

Two owner decisions arrived during drafting (coordinator message, 17.11.2026) and are SETTLED here, not forks:
- **O-1** `docs/TESTING.md` is a MAIN document (the owner: «на этот документ смотрят несколько ролей, так что оставляем как
  основной документ и проверяем что на него есть ссылки у всех кто должен его использовать»). → §7 (pointer check + pin).
- **O-2** `plans/builder-rules.md` is a brief to be dissolved (the owner: «Зачем у нас этот отдельный документ если есть роль
  билдера? Там есть что-то что нужно не только билдеру?»). → §4.2 opens with the answer table.

---

## §1 Scope, invariants, owners

**What changes.** Six documents are deleted after every needed statement got one home in a main document:
`docs/tasks/critic-diff-brief.md`, `plans/builder-rules.md`, `docs/tasks/pre-release-0.9-brief-common.md`,
`docs/tasks/pre-release-0.9-critic-brief.md`, `docs/tasks/test-diet-brief.md`, `docs/tasks/test-diet-fold-brief.md`.
A seventh candidate, `docs/tasks/exchange-form.md`, is fork F4 (node N7 of this spec, recommended IN).
A rule forbids standing briefs again (§8), with a deterministic pin and a calibration check.
The owner's refinement on fixing in the round is written into PROJECT.md «Командная работа» п. 9 and CLAUDE.md rule 9 (§6).

**AR-n of `design/architecture.md`.** The package (`ai-packages/qa-factory/`) is NOT edited: `architecture: none -- no
package file changes` is not owed (no package commit). The only package-adjacent reader is
`tools/test_quarantine.FORGE_CARRIERS`, which feeds `selftest.gate_named_files(extra_texts=...)` from OUTSIDE the package
(AR-4 kept: the package still reads no `docs/`); its change check is edge E4 (the gate-named set is unchanged).

**Checks added or altered, with owner and census class (AR-29, P27):**

| Check | Owner it serves | Census class |
|---|---|---|
| K-NOBRIEF: no main document names a `docs/tasks/*brief*.md` path or `plans/builder-rules.md`; the six deleted paths stay absent; no tracked file `docs/tasks/<top level>*brief*.md` | data (code): presence of paths and names | forge test, outside `judgment-census.json` (that census scans the package; estimate — its `SCAN_ROOT` not re-read) |
| K-TESTPTR: every role that must use `docs/TESTING.md` carries a pointer to a named section of it (POINTERS rows) | data (code): pointer presence and target anchor | same |
| POINTERS / OWNER_KEYS rows re-pointed (axis 31) | data (code) | same |
| Calibration check 33 (i): a main document that sends a role to a non-main standing document | judgment (Lead at calibration, accepted by the Architect review of check 49) | n/a (protocol) |

**Mechanism.** This is a mechanism change (rule carriers of roles, a new rule, a new pin): the Lead's commit carries the
rule-10 axis block and `tier: opus`. Axes this change touches (the Lead enumerates all): **1** (policy ↔ role files: the
CLAUDE.md rule 10 package paragraph names "the critic's standing questions 10 and 11"; they move into critic.md with the same
numbers Q10/Q11, so the paragraph stays true — checked in the same commit), **2** (critic.md rule 10: editing critic.md owes
the critic exam; `PROCESS/CRITIC_EXAM.md` is absent — Glob `PROCESS/*.md` lists 12 files, none is CRITIC_EXAM — road: the
commit records `Deviation: exam not run; debt F3-1`, precedent commit 1f165a38 per spec 20261116-spec-facts-by-code §4.1),
**18** (Q9's carrier row, SIBLING_MAP:401), **31** (the main axis: owner per aspect), **34** (the reviewers row,
SIBLING_MAP:602), the AR-29 acceptor row (SIBLING_MAP:577), axis 1 row :34 (what a builder runs ↔ every dispatch text),
axis 4 row :95 ("Builder rules").

---

## §2 Definitions (the border)

**Main document** — derived, not invented: a file that the axis-31 table of `docs/SIBLING_MAP.md` (:482-515) marks as
OWNER of an aspect, minus the briefs this spec dissolves. Today: `CLAUDE.md` with its `@` imports (`PROJECT.md`,
`docs/FACTORY_RULES_INDEX.md`, `docs/ARCHITECTURE_INDEX.md`, `docs/OWNER_PRINCIPLES_INDEX.md`), the role files
`.claude/agents/<role>.md`, `docs/TESTING.md` (O-1), `docs/TEAMWORK.md`, `docs/RUNBOOK.md`, `docs/SIBLING_MAP.md`,
`docs/OWNER_PRINCIPLES.md`, `docs/TWO_VOCABULARIES.md`, `PROCESS/*.md`, `.claude/skills/*/SKILL.md`, `delegation.config.yaml`,
`DELEGATION_TABLE.md`, `SYSTEM_PROMPT.md`, `BOOT.md`, and the package's own rule files `ai-packages/qa-factory/design/`.
Records that are NOT rule carriers: `DECISIONS.md` (append-only record), `CURRENT_CONTEXT.md` (state), `docs/*_FULL.md`
(frozen archives), `docs/DECISIONS_ARCHIVE.md`, generated copies (`AGENTS.md`, the three indexes).

**Extra document (standing brief)** — a document a role must read EVERY time it works (or every time a class of dispatch
names it) beyond its role file and the boot, that is not a main document. Examples dissolved here: the critic's diff brief,
the builder rules, the 0.9 briefs, the test-diet briefs.

**Not extra** (one node / one task / one moment, never "always"): a spec (`docs/tasks/specs/`), a batch file or card, a
finding, a review, a report or handoff, a compact snapshot, a queue (`docs/tasks/lead-queue.md`, `architect-queue.md`), a
plan of one task (`docs/tasks/test-diet.md`, `factory-fixes.md`), and the Lead's intent brief to a designer written in the
dispatch text (CLAUDE.md rule 2 "intent brief" — a word, not a file).

---

## §3 Inventory, by command

All searches by the Grep/Glob tools from `C:/QAFactory/forge-repo`, worktrees under `.claude/worktrees/` excluded from
judgment (a `.claude` Grep timed out on them; the real folders were searched one by one).

| # | Command | Result |
|---|---|---|
| I1 | Glob `**/*brief*` | 4509 hits, almost all worktrees and package code (`brief_pack`, `gate_brief`: package machinery for factory roles, not forge briefs). Forge docs: `docs/tasks/critic-diff-brief.md`, `pre-release-0.9-brief-common.md`, `pre-release-0.9-critic-brief.md`, `test-diet-brief.md`, `test-diet-fold-brief.md`; `docs/tasks/specs/td-11-lead-brief.md` (a spec-folder intent brief: not extra) |
| I2 | Glob `docs/tasks/*.md` | 12 files: the 5 above, `exchange-form.md` (F4), `factory-fixes.md`, `test-diet.md`, `onboarding-streams-2026-11-12.md`, `t-183-of3-1c-config-census.md` (plans/records), `architect-queue.md`, `lead-queue.md` (queues) |
| I3 | Grep `brief\|builder-rules` -i in `.claude/agents` | designer.md :3,8,10,20,35,42,45,48,63 ("intent brief" words; :20 builder-rules 7b; :42 "critic brief item 4"); builder.md :49,53; critic.md :77,161,164,173 |
| I4 | Grep `brief\|builder-rules` -i in `.claude/skills` | 0; positive control Grep `Как пишутся правила для агентов` -i same path → 1 (boot-diet/SKILL.md:111) |
| I5 | Grep `brief\|builder-rules` -i in `.githooks` | 0; control Grep `python` same path → 15 in 4 files |
| I6 | Grep `critic-diff-brief\|builder-rules\|brief\|TESTING\.md` -i in CLAUDE.md | :31, :33, :35 (Contents), :67/:112/:116 ("intent brief" words), :127 (rule 3), :154 (rule 4), :294 (rule 11 → TESTING), :394 (journal example `brief:`) |
| I7 | Same + `бриф` in PROJECT.md | :45 (map row), :75 (p. 1), :79-80 (p. 2), :83 (builder-rules п. 11), :95 ("brief pack", package machinery), :182 («в брифах» — dispatch text, not a file), :237 (п. 13) |
| I8 | Grep the four brief names in `tools/` | install_parity_anchors.json:22; owns_readers.py:26,55; dispatch_gate.py:1870; test_role_carriers_one_owner.py (17 lines); test_handoff_rule_anchors.py :5,9,38,39; test_dispatch_manifest.py:844; test_language_sites.py:4; test_quarantine.py:51; test_split.py:1843; test_test_quarantine.py :389,413,841,1489,1613; fixtures K3/K4/K7 (historical prompts) |
| I9 | Grep `brief` -i in `dispatch_new.py, dispatch_manifest.py, dispatch_gate.py, handoff_gate.py` | 0; control Grep `GIVEN\|given` same glob → 99 in 3 files. The dispatch tools inject no brief |
| I10 | Grep `critic-diff-brief\|builder-rules\|brief` -i in PROCESS | WEEKLY_CALIBRATION_PROTOCOL.md:392 (builder-rules 7b), :1047-1057 (the "brief form" metric of check 34 — dispatch text, not a file) |
| I11 | Grep the brief names in `docs/` minus specs | SIBLING_MAP :34, :95, :401, :478-479, :484-493, :496, :505, :507-508, :564, :577, :602; TESTING.md :65, :89, :102, :123, :170, :228, :229; RUNBOOK :125, :218, :380, :399, :617, :630; CLAUDE_HOST_ADAPTATIONS_FULL :7, :33; PROJECT_FULL :21, :224, :228-229, :243, :256 (frozen); DECISIONS_ARCHIVE (record); FINDINGS.md:96, ADOPTION_LEDGER.md:91, factory-fixes.md (records); test-diet.md :17, :35, :88 (plan); handoffs (records) |
| I12 | Grep in DECISIONS.md | :32 D-0033 names critic-diff-brief (record; divergence D1) |
| I13 | Grep `critic-diff-brief\|test-diet-…brief` in `plans/` | live node rows: told-before-work/batch-1-finish.md:41 TBW1-14 (ожидает), forge/batch-7:76 FG7-51 (ожидает), live-run-fvf/batch-2 FV2-14 (finding row :93 of the card); the rest are cards, findings and closed batches (records) |
| I14 | Grep `TESTING\.md` in `.claude/agents/*.md, tools/dispatch_*.py, dod_gate.py, handoff_gate.py, calibration protocol` | critic.md:174, builder.md:93,95, protocol :1118; designer.md 0, dispatch tools 0 (O-1 check, §7) |
| I15 | Grep `expected from` -i in `tools/*.py` | 0; control the same pattern in docs/TESTING.md → 4. TESTING.md:88 claims `tools/dispatch_manifest.py` checks the `test:` line — not on this tree (D7) |

**Classification.**

| Document | Class | Fate |
|---|---|---|
| `docs/tasks/critic-diff-brief.md` | standing brief of the critic (diff gate; Q12 also plan gate) | dissolved → critic.md rules 21-23 (§4.1) |
| `plans/builder-rules.md` | standing brief of the builder (its own line 3: «Войдут в профиль билдера») — O-2 | dissolved (§4.2) |
| `docs/tasks/pre-release-0.9-brief-common.md` | dead one-off (0.9 designer brief; line 3 «Superseded by D-0056») | deleted (§4.3) |
| `docs/tasks/pre-release-0.9-critic-brief.md` | dead one-off (0.9 plan-critic brief) | deleted (§4.4) |
| `docs/tasks/test-diet-brief.md` | dead standing spec (TD-4 waves 2-3 cancelled, test-diet.md:47-48) | deleted (§4.5) |
| `docs/tasks/test-diet-fold-brief.md` | dead standing spec (TD-14 closed by the pilot, test-diet.md:126) | deleted (§4.6) |
| `docs/tasks/exchange-form.md` | standing grammar of the scout digest + the "brief form v1" for the Lead; a test fixture lives inside it | F4, node N7 (§4.7) |
| `docs/TESTING.md` | MAIN (O-1) | stays; gains 7b (§4.2); pointer pin (§7) |

---

## §4 Paragraph-by-paragraph homes

Legend: **present** = already in the named home (deleted from the brief, nothing added); **diverges** = see §5;
**needed** = new text in the named home; **dropped** = reason given.

### §4.1 `docs/tasks/critic-diff-brief.md` → `.claude/agents/critic.md` rules 21, 22, 23

Who needs it: only the critic acts on it; the dispatcher and the builder need only the mechanical-layer FACT "what is
attached before the critic", which CLAUDE.md rule 3 already states (TWO-LAYER CRITIC ENTRY) and PROJECT.md p. 2 points to.
So the whole text moves to the critic's role file; every outside pointer is redirected there.

The text moves VERBATIM (English), with only the edits listed. Numbering: the questions become `Q1.`…`Q12.` (a leading
`Q` keeps `tools/test_handoff_rule_anchors.rule_block`, which splits on `^\d+\. `, from reading a question as a rule).
Internal references "item N" / "question N" become "QN".

| ¶ (brief line) | Statement | Verdict | Home / action |
|---|---|---|---|
| P0 (:1) | title "Standing brief for the critic gate on a builder diff" | dropped | a title of a file that no longer exists |
| P1 (:3-6) | owner's word 06.10.2026, order KEPT; dup + quality on every diff gate; clone ratchet = deterministic layer; "CLAUDE.md rule 3 and rule 18 point here (B-419)" | present (critic.md rule 18 quotes the 06.10 word; CLAUDE.md rule 3 "the clone ratchet is the deterministic layer") | dropped; the B-419 pointer sentence dies with the file |
| P2 (:8-16) | Mechanical layer: what the builder attaches (DoD tails; `red-before:`; no mutation list; ratchets are forge-check's, read never re-run; old/new counts); a missing layer → request | present in principle (CLAUDE.md rule 3), detail **needed** for the critic; ratchet clause **diverges** with D-0033 (D1) | **critic.md rule 21** "The two layers of a diff gate", first bullet, verbatim; the scope pointer `plans/builder-rules.md` 7b → `docs/TESTING.md` «Что запускать по своей правке»; "7b/7c" → the same section; "D-0033 as refined by the Lead" → "D-0056" |
| P3 (:17-22) | Verdict layer: own zone; ONE cheap control re-run; what is NOT re-run | needed | rule 21, second bullet, verbatim |
| P4 (:24-27) Q1 | Fit to the spec | needed | rule 22 Q1 verbatim |
| P5 (:28-29) Q2 | builder's own decisions | needed | Q2 verbatim |
| P6 (:30) Q3 | seams | needed | Q3 verbatim |
| P7 (:31-38) Q4 | class-wide completeness; repaired IN THE ROUND; analog outside owns → named with its file; another pile / owner's decision → «Остатки» line forms | needed; the line FORMS restate `docs/TEAMWORK.md` § 9 (TEAMWORK:22-25 is their owner) | Q4 verbatim up to "(say which)", then: "comes back as a «Остатки» line in the forms of `docs/TEAMWORK.md` § 9 (a bare line is refused by `piles.py check` (д)); moving a sibling to another pile is the rare case of PROJECT.md «Командная работа» п. 9, never a way to defer a rule fix while rules are being fixed (the owner's word 17.11.2026)." |
| P8 (:39-67) Q5 (a)-(g) | tests | needed | Q5 verbatim; `docs/tasks/specs/td-15-…` reference kept (a spec named as source, not a standing read) |
| P9 (:68-73) Q6 | DUPLICATION AND CONSISTENCY | needed | Q6 verbatim (heading `Q6. **DUPLICATION AND CONSISTENCY**`) |
| P10 (:74-77) Q7 | CODE QUALITY | needed | Q7 verbatim (`Q7. **CODE QUALITY**`; "(item 4: …)" → "(Q4: …)"). OWNER_KEYS `review:critic` key stays verbatim |
| P11 (:78) Q8 | hygiene FR-29/30, size caps, CRLF | needed | Q8 verbatim |
| P12 (:80-89) Q9 | in-tree ratchets list | needed | Q9 verbatim |
| P13 (:91) Q10 | ARCHITECTURE | needed (axis 1 named it "question 10") | Q10 verbatim |
| P14 (:92-100) Q11 | JUDGMENT | needed (axis 1) | Q11 verbatim; "question 9 applies" → "Q9 applies" |
| P15 (:102-114) Q12 | ONE ROAD | needed | Q12 verbatim; OWNER_KEYS `review:one-road` key stays verbatim |
| P16 (:116-122) | What comes back: "accept / accept with fixes / reject with failure_class" … under ~1800 words, json block last | **diverges** (D2: a third verdict vocabulary; "accept" is the coordinator's word, critic.md rule 6) | **critic.md rule 23** "What comes back from a diff gate": "The verdict line in rule 6's words (ACCEPT / NEEDS WORK / REJECT, a REJECT with its `failure_class`), each fix with file:line and whether it blocks the merge; the JSON block of rule 17 carries the same verdict as `fit` / `fit_with_fixes` / `blocker` (`blocker` when any finding blocks). Then Findings numbered / Seam and class notes / Spot-checks (claims verified with their carriers; every negative with its positive control) / Trail (files, line ranges, commands with verbatim output) — under about 1800 words, trail last, then the closing ```json block (rule 17). The form of the file and the fallback with no path are rules 16-17." |
| P17 (:124-125) | review is a FILE; `critic_verdict_check.py` exit 0 | present (critic.md rules 16-17) | merged into rule 23's last sentence; `critic_verdict_check.py` named there (test_handoff_rule_anchors reads it) |

**Edits to existing critic.md rules (same card):**
- rule 5 (:26-32): "Axes of the defect left uncovered and not queued = a NEEDS-WORK finding." → "Axes of the defect left
  neither fixed in the round nor — only when outside the work's context — opened as a node with an executor in another pile
  (PROJECT.md «Командная работа» п. 9) = a NEEDS-WORK finding." (first line unchanged: install_parity anchor
  `5. Class-wide completeness of a fix is a standard finding category`).
- rule 12 (:76-77): "(its size: docs/tasks/critic-diff-brief.md «The two layers»)" → "(its size: rule 21)".
- rule 18 (:158-162): "the rule text is docs/tasks/critic-diff-brief.md items 6-7" → "the rule text is rule 22, Q6-Q7".
- rule 19 (:163-171): "the question is docs/tasks/critic-diff-brief.md item 12" → "the question is rule 22, Q12".
- rule 20 (:172-177): "the question is docs/tasks/critic-diff-brief.md question 5" → "the question is rule 22, Q5".

Rule 22 opens: "22. The standing questions — on every diff gate, each with its own verdict line (Q12 also on a plan gate):"
followed by Q1-Q12 indented three spaces. Rule 21 opens: "21. The two layers of a diff gate (CLAUDE.md rule 3, the
two-layer review rule):". Rule 23 opens: "23. What comes back from a diff gate:".

Size: critic.md 178 lines today (Read); +~115 lines moved, −~3 lines of pointers → ~290 lines, about 20-21 KB (estimate,
not measured: the scout's 11 KB + the brief's 13.5 KB minus the dropped P0/P1/P17 and the TEAMWORK restatement). No ceiling
guards `.claude/agents/*.md` (§9).

### §4.2 `plans/builder-rules.md` — dissolved (O-2)

**Answer to the owner's question «Там есть что-то что нужно не только билдеру?» — yes, six items:**

| Item | Needed by | Home |
|---|---|---|
| 1 file ownership | builder + dispatcher (who sets `owns`) | owns rule: present (CLAUDE.md hygiene 4, R11-f); integrator list: dropped (F7); "new config key: name, default, meaning" → builder.md rule 4 |
| 2 no git state change; commit own owns in a worktree | builder | builder.md rule 10 |
| 3 language | everyone | present: PROJECT.md «Язык» (boot) — dropped |
| 4 style (why-comments, harness/unittest, stdlib only) | builder | builder.md rule 11 |
| 5 size caps | builder, designer, critic (Q8) | numbers live in code (`selftest.py --limits`, audit A22): builder.md rule 11 points at the code; numbers dropped |
| 6 no bytecode in the package | builder | builder.md rule 11 |
| **7** mandatory check (no full selftest / install_smoke; others' reds noted not fixed; size pin is a cap) | **builder, designer (DoD), critic (layer 1), coordinator** | **`docs/TESTING.md` «Что запускать по своей правке»** (new); "size pin is a cap" present (TESTING.md:137) |
| 7a cost of the check (one witness run, one repeat) | builder | builder.md rule 9 |
| **7b** builder level and batch level | **builder, designer, critic, coordinator, integrator** | **`docs/TESTING.md` «Что запускать по своей правке»** (new, Russian, verbatim); canon procedure present (RUNBOOK §7); CLAUDE.md rule 4 points at the TESTING section |
| **7c** story_run.py DoD files | **designer / dispatcher (DoD)** | same TESTING.md section, one row of the per-type list |
| **7d** which tests are written | **builder, designer, critic** | present: TESTING.md (three layers, «Что не пишется», «Правила ролей не теряются», «Бюджет»); CLAUDE.md rule 11 DOC-DISPATCH WITNESS — dropped |
| 8 a person's word passes any block | builder, designer, critic | present: FR-4, FR-57, P13 (factory-rules, read whole on package edits) — dropped |
| 9 backward compatibility | builder, designer (temporal edges) | builder.md rule 11 (F9: a package home later) |
| 10 live project read-only | builder, night agent | builder.md rule 11 (the night agent's rule is RUNBOOK §9.6, not re-measured — §11 Not established) |
| 11 report content | builder | builder.md rule 4 |
| **12** factory rules read whole | **builder, critic, designer** | present: PROJECT.md p. 1 («несёт в «given» `design/factory-rules.md` целиком», the FR walk in the report); builder.md rule 11 keeps one phrase + pointer |
| 13 bounded background wait | builder + coordinator | rule home: RUNBOOK §9.8 «Фоновые ожидания» (:393-401, present for the coordinator); builder.md rule 9 one phrase + pointer |
| 14 a confession names file:line | builder | builder.md rule 4 |
| 15 witness pasted, not typed | builder | present: CLAUDE.md rule 2 ("not a paraphrase"), builder.md rule 4 ("not a paraphrase like 'tests pass'") — dropped |
| **16** worker budget (а) trim output (б) one witness run (в) cap, STOP exits | **every worker; coordinator** | (в) present: CLAUDE.md rule 12 Cost gates + `agent_budget.py` refusal; (а)(б) → CLAUDE.md rule 12 Cost gates, one sentence (§4.2.2); builder.md rule 9 points |
| 17 AGENTS.md is generated | builder, Lead (whoever edits CLAUDE.md/PROJECT.md) | the refusal of `agents_md.py --check` names the command (code carries it); builder.md rule 10 one line |
| 18 commit from the worktree; mechanism paths staged | builder | builder.md rule 10; "the Lead commits mechanism paths" present: CLAUDE.md rule 2 |
| **19** `architecture:` / `judgment:` lines | **builder, Lead, designer** | present: CLAUDE.md rule 10 «a change to the package» (names both lines and the gate); the grammar's only carrier is `tools/architecture_gate.py` (designer.md rule 1) — the copied grammar is dropped; builder.md rule 10 one pointer |
| **20** worktree dispatch and return | **coordinator** | present: CLAUDE.md rule 12 Cost gates ("a push before a worktree launch"), RUNBOOK §12 items 2, 8, 11 (handback_extract, base from pushed origin/main, `handoff:` by role), R11-h — dropped |
| tail (:135) | interfaces fixed / CLI_SCRIPTS / no direct pytest / `judge.provider: none` | builder | "interfaces fixed" dropped (the 0.7 multi-package parallel model is gone); "pytest in the package is refused by a hook" dropped (code refuses with a door); CLI_SCRIPTS and `judge.provider: none` → builder.md rule 11 (F7) |
| header (:1-6) | provenance 29.09, "will go into the builder profile", "rest of common is one-off" | — | dropped: history (git keeps it); its promise is what this spec executes |

#### §4.2.1 New section of `docs/TESTING.md` — «Что запускать по своей правке»

Placed after «Строка теста в DoD» (TESTING.md:75-89), before «Тест может упасть» (:91). Exact text = builder-rules 7b
(:38-65) VERBATIM, Russian, with these edits only:
- heading `### Что запускать по своей правке` and the first sentence: "Слово владельца 21.10.2026 18:3x, D-0056 (замер: у
  фикс-раундов 69–85 % стены — ожидание прогонов, правки кода 1–4 %)." (the clause «П. 7 и 7a переписаны под этот пункт
  (F6-33, 21.10.2026)» is dropped: history);
- builder-rules 7 (:28) appended as one bullet: «Полный `selftest.py` и `install_smoke.py` на машине не гоняет никто — их
  судит CI (D-0059, `docs/RUNBOOK.md` §7). Красный тест вне своих файлов от чужой недоделки — отметить и не чинить.»;
- builder-rules 7c (:68-71) appended to the «так же по типу правки» list as: «`test_story_run_words.py` и
  `test_driver_layers.py` — правка `story_run.py` (Lead, 26.10.2026: `main` красный 16.10 и 21.10, оба раза DoD их не
  называл)»;
- «правило 4 `CLAUDE.md`» stays; «п. 7b» self-references removed;
- the bullet at TESTING.md:123 becomes «- **Что запускать по своей правке** — раздел «Что запускать по своей правке» выше.»;
  :228 becomes «- **Билдер**: пишет по этому документу; что запускает — «Что запускать по своей правке».»
- TESTING.md:65 «`plans/builder-rules.md`, файл роли» → «файл роли».

Bytes: ~3.3 KB moved (7b ~2.9 KB + 7/7c ~0.4 KB; estimate from the Read, Cyrillic 2 bytes/char). TESTING.md has no ceiling.

The OWNER_KEYS key `scope:builder` («не регрессия, не соседи, не большие файлы») moves with the text: owner → `docs/TESTING.md`.

#### §4.2.2 CLAUDE.md rule 12 · Cost gates — one sentence (16 а-б)

After "`tools/agent_budget.py` caps a worker (WARN 250K, STOP 400K; the remainder goes to a fresh worker whole);" insert:
"a worker trims run output before it enters its context (`-q`, a 30-line tail, `Read` with a limit over 400 lines) and
closes a round with ONE witness run after all edits (D-0035);". (+~190 bytes.) The OWNER_KEYS key `cost:cap`
("WARN 250K, STOP 400K") is untouched.

#### §4.2.3 `.claude/agents/builder.md` — exact texts (English)

rule 4 (:39-53): replace "Its scope in this repository: `plans/builder-rules.md` 7b (D-0056) — the files
`scenario_walk.py --witness-for <owns>` prints; a quarantined test file is never run or edited, and no new test file is
written without a keep row (7d). CI is neither started nor waited for: `plans/builder-rules.md` 7b." with
"Its scope in this repository: `docs/TESTING.md` «Что запускать по своей правке» (D-0056) — the files
`scenario_walk.py --witness-for <owns>` prints; a quarantined test file is never run or edited; CI is neither started nor
waited for." and append to rule 4:
"The report's content (its form is rule 7): per item of the plan DONE / PARTIAL / NOT DONE, one line and the files; the
tests added or changed and the exact final lines of the runs; «Needed from integration» (file, exact text, why) for a file
outside your owns; every new config key with its name, default and meaning; the CHANGELOG entry as a fragment file
`ai-packages/qa-factory/changelog.d/<pile>-<batch>-<slug>.md` in the CHANGELOG voice (English; `CHANGELOG.md` itself is
never touched); what was decided differently from the plan and why; at most about 500 words of prose (verbatim run
output does not count). A confession of a hygiene deviation names file:line (critic t-560 had to guess)."

new rule 9:
"9. Runs, cheaply. While working, after an edit run only the test file of the changed module; the witness is ONE run of
rule 4's scope on the final state, repeated once only if code changed after it (the owner, 30.09.2026). The output is
trimmed before it enters your context (CLAUDE.md rule 12, Cost gates). A background wait names the file it waits for and
its end (a count or seconds); an unbounded polling loop is forbidden (the rule: `docs/RUNBOOK.md` §9.8)."

new rule 10:
"10. Git. No git state change in a shared tree (`stash`, `add`, `commit`, `checkout`, `reset`, `restore`, `clean`,
`pull`, `push`); `diff`, `log`, `show`, `status` are free; another worker's uncommitted edits are never touched. In your
own worktree you commit your owns only — `git add` / `git commit` from the worktree root, a plain message with
`axes: not a mechanism (...)`; a package commit also carries the `architecture:` and `judgment:` lines, whose form is
`tools/architecture_gate.py` (CLAUDE.md rule 10). Mechanism paths (`MECHANISM_PREFIXES` of `tools/mechanism_gate.py`)
stay STAGED and are listed in the report: the Lead commits them (CLAUDE.md rule 2). A task that edits `CLAUDE.md`,
`PROJECT.md` or `docs/FACTORY_RULES_INDEX.md` regenerates `AGENTS.md` with `python tools/agents_md.py --repo <worktree
root>` and stages it (no `owns` entry needed). Merges, pushes and branch switches are not yours."

new rule 11:
"11. In the package. `ai-packages/qa-factory/design/factory-rules.md` is read whole before the edit and again before the
report (PROJECT.md «Как принимается изменение пакета» p. 1). Comments explain why, usually naming the incident; tests use
`scripts/tests/harness.py` or unittest, after a look at the neighbouring test; stdlib only, no new dependency. Run with
`python -B`; temporary files go to the OS temp, never into the package. Size caps are `selftest.py --limits` and audit
A22 (text added to a role or reference is paid for by removing redundant text). A project onboarded on an earlier version
works without re-onboarding, and a story in flight is never refused because an earlier artifact lacks a new field. A live
project is read-only: no write and no `cd` there; code runs on a copy in temp. A new CLI script is registered in
`audit_factory.py` `CLI_SCRIPTS`; every code path works with `judge.provider: none`."

Size: builder.md 101 lines (Read) → ~145 lines, ~10-11 KB (estimate).

### §4.3 `docs/tasks/pre-release-0.9-brief-common.md` (86 lines) — deleted

| Section | Verdict |
|---|---|
| header, «Superseded by D-0056» | dropped: one-off record of the 0.9 release; git keeps it |
| Where things are (:8-29): root `D:/ws1/…`, package layout, D-0025…D-0031, backlog lines, rules to satisfy | dropped: stale paths; the rule list is present (PROJECT.md p. 1, CLAUDE.md rule 10, FACTORY_RULES_INDEX) |
| What you return 1-9 (:31-74): spec shape, edges with invariant, acceptance keys, DoD from root no `cd`, manifest, FR walk, siblings, forks | present: designer.md rules 1-7, CLAUDE.md rule 11 / R11-f; "one mutation → one killing test" **diverges** with the owner's word 10.11 (mutation list retired, TESTING.md:93-94) — the newer word holds; dropped |
| completeness criterion, size caps 9000/19000/12000, `[meaning]` mark (:76-83) | caps: code (§4.2 item 5); `[meaning]` → PROJECT.md p. 6 (present) — dropped |

### §4.4 `docs/tasks/pre-release-0.9-critic-brief.md` (57 lines) — deleted

| Section | Verdict |
|---|---|
| context (:3-7) | dropped (0.9 one-off) |
| review against 1 facts by trail | present: CLAUDE.md rule 3 critic-on-plan ("checks the plan's facts by trail"), critic.md rules 11-12 |
| 2 `[meaning]` + error direction | present: PROJECT.md p. 6 (в), designer.md rule 1 |
| 3 challenge the Lead's fork decisions | **needed** for the plan gate: absent from critic.md today (Grep `fork` -i critic.md not run — estimate from the Read of critic.md: no such rule) → F6 (it belongs with stream L's plan-gate Q13; recommend: one sentence in Q13 or rule 24) |
| 4 feasibility | present: CLAUDE.md rule 3 ("feasibility is an architectural judgment") |
| 5 class completeness, seams of parallel specs | present: Q3, Q4 (rule 22) |
| 6 tests: one mutation → one test | diverges, retired 10.11 — dropped |
| 7 FR walk honest, P1-P3, caps | present: Q8, Q10-Q11, PROJECT.md p. 1 |
| 8 duplication on a plan | present: Q6 (diff); on a plan → F6 |
| What you return (:43-56) | present for the diff gate (rule 23); plan-gate form → F6 |

### §4.5 `docs/tasks/test-diet-brief.md` (73 lines) — deleted

| Section | Verdict |
|---|---|
| kinds table (:11-22) | present: TESTING.md «Что не пишется» (source pin, measured constant, as before, negative control, workflow document), «Правила ролей не теряются» (role-text pin), layer 2 data join, layer 3 "keys and hashes of records on disk" (compatibility literal) |
| empty file → `git rm` + `plans/features.json` (:24-25) | **needed**, generalised: a deleted test file leaves no registry naming it → TESTING.md «Когда тест покраснел», new item 4: «4. Удаляя тестовый файл, убери его имя из реестров, которые его называют (`grep` по имени файла: `plans/features.json`, `slow_tests.json`, `CONTRACT_TESTS`/`TEST_TIMEOUTS` в `selftest.py`, `gate-registry.json`, `stage-joints.json`, `driver-layers.json`, `.gitlab-ci.yml`, `judgment-census.json`); файл, который называет гейт, не удаляется — только чистится.» (~0.5 KB) |
| world once (:27-28) | present: TESTING.md «Время» |
| never-do list (:32-38) | present: owns (hygiene 4), builder.md rule 10 (git), PROJECT.md «Сессия форджа» (no `cd`); "no weakening an assertion that stays" → dropped (a pruning-wave duty, the waves are cancelled) |
| edges (:42-55) | wave-specific; `driver-layers.json` rows → the new TESTING item 4 — rest dropped (waves cancelled) |
| witness, report, commit template (:59-72) | dropped: the commit template copies the gate grammar; the gate is its one carrier (finding 20261114 notes it) |

### §4.6 `docs/tasks/test-diet-fold-brief.md` (100 lines) — deleted

| Section | Verdict |
|---|---|
| words, the 3-step fold, fates (:8-35) | dropped: TD-14 closed by the pilot (test-diet.md:126); the general rule "a duplicate check goes, a unique one moves into its home as a row" is present (TESTING.md «Как писать эффективный тест» 1, 3; critic Q5 (e)) |
| budget of a fold (:37-38) | dropped (wave-specific) |
| registries (:40-49) | → the new TESTING item 4 (§4.5) |
| never-do, edges, witness, report, commit (:51-99) | as §4.5 |

### §4.7 `docs/tasks/exchange-form.md` (157 lines) — fork F4, node N7

| Section | Verdict |
|---|---|
| §1 digest form v1 (:7-79): headings, Objects/Trail grammar, flag table | scout.md rule 10 carries the key line and the table headers; the grammar and flag table are read by `tools/digest_form.py` (its docstring :13, FLAG_NAMES pin :39) — needed by the scout and the Lead |
| example t-794 (:81-130) | a TEST FIXTURE: `tools/test_digest_form.py` reads this block (exchange-form:87) |
| §2 the brief form v1 (:132-156) | a dispatcher duty (Lead) → CLAUDE.md rule 11 is its natural home (boot-diet rule 1: the dispatcher's duty lives in the boot) |

Recommended N7 (if F4 = in): grammar + flag table → scout.md rule 10 (or a new rule 12); the example → `tools/fixtures/digest_form/t-794.md`
read by `test_digest_form.py`; §2 → three sentences in CLAUDE.md rule 11 (+~400 bytes); SIBLING_MAP axis 1 row :35 re-pointed.
N7 is drafted after the Lead's answer (its rows above are the inventory).

---

## §5 Divergences found (who holds)

| # | A | B | Holds |
|---|---|---|---|
| D1 | DECISIONS.md:32 D-0033 "every builder's witness carries `--check`" | critic-diff-brief:13-15 "ratchets NOT in the builder's layer … D-0033 as refined by the Lead"; builder-rules 7b:52-53 «храповики — уровень пачки» (owner 21.10, D-0056) | D-0056 and the owner's word 21.10 (newer). Fork F5: the Lead appends to D-0033 "(refined by D-0056: the ratchets run at batch level in `forge-check`; a builder does not run them)" |
| D2 | critic-diff-brief:118 "accept / accept with fixes / reject" | critic.md rule 6 "ACCEPT / NEEDS WORK / REJECT"; rule 17 JSON `fit` / `fit_with_fixes` / `blocker`; rule 6: a verdict phrased as a decision is a violation | critic.md rules 6 + 17 hold; rule 23 maps them (§4.1 P16); the third vocabulary dies |
| D3 | designer.md:42 "critic brief item 4" | the brief disappears | redirect to "critic.md rule 22 Q4" (C3) |
| D4 | owns_readers.py:26 "answered in docs/tasks/critic-diff-brief.md item 13 (d)" | the brief has 12 items; Q13 is a pending text of spec 20261116-spec-facts-by-code §4.1 (stream L, unlanded) | F6: stream L's L1 lands as critic.md rule 24 "The plan gate" (Q13); owns_readers docstring → "critic.md rule 24 Q13 (d)" |
| D5 | critic.md rule 5 "left uncovered and not queued" | owner 17.11: fixed in the round; another pile only rarely | the owner's word; §6 |
| D6 | pre-release brief "one mutation → one killing test" | TESTING.md:93-94 mutation list retired 10.11 | TESTING (owner's word) |
| D7 | TESTING.md:88 «Наличие и форму строки проверяет код (`tools/dispatch_manifest.py`…)» | I15: no `expected from` in any `tools/*.py` | not established whether the check is in flight on another branch (told-before-work / coordinator offload) → F8 |
| D8 | builder-rules 7b:41 cites `td-15` spec; brief Q5 (g) cites it | consistent | — |
| D9 | builder-rules 19 copies the `judgment:` grammar | designer.md rule 1: the gate is its only carrier | the gate; copy dropped |

---

## §6 «Fixed in the round; another pile only as a rare case» (the owner's word 17.11.2026)

**PROJECT.md «Командная работа» п. 9** (the item's bold opener stays byte-identical with TEAMWORK § 9). Replace
«минорные замечания критика не откладываются строкой, а чинятся тут же — фикс-раундом того же узла;» with:

> минорные замечания критика не откладываются строкой, а чинятся тут же — фикс-раундом того же узла, и замечание по
> правилам, когда чиним правила, — тоже; в чужую кучку уходит только то, что для полноты класса требует чинить вне
> контекста узла, — редкий случай, а не способ отложить (владелец, 17.11.2026);

(+~330 bytes; the rest of the item stays.)

**CLAUDE.md rule 9.** Replace "fix now, or EXPLICITLY put the remainder in the queue/log;" with:

> fix now, in the same round (PROJECT.md «Командная работа» п. 9); a sibling outside the work's context leaves only
> EXPLICITLY, as a node with an executor in another pile — a rare case, never a way to defer a rule fix while rules are
> being fixed (the owner's word 17.11.2026);

In the sweep paragraph "(applied / not applicable — why / queued with a pointer)" → "(applied / not applicable — why /
moved to another pile's node, with its id)". "opening a file specially for the sweep is forbidden — queue it instead"
stays: a file outside the work's context is exactly the owner's allowed case. (+~210 bytes.) The OWNER_KEYS key
`routing:rule-9` and the SYSTEM_PROMPT pointer anchor `9. Fix the class, not the instance (fix-the-class-not-the-instance`
are untouched. critic.md rule 5 and Q4: §4.1.

---

## §7 `docs/TESTING.md` — who must point to it (O-1)

| Role / carrier | Must use it for | Pointer today | Action |
|---|---|---|---|
| builder (`.claude/agents/builder.md`) | writing tests, volume, what to run | rule 8 :93-100 `docs/TESTING.md`, «Бюджет / Объём» | + rule 4 names «Что запускать по своей правке» (§4.2.3) |
| critic (`.claude/agents/critic.md`) | Q5, layer 1, rule 20 | rule 20 :174 «Бюджет»; after the fold Q5 names TESTING sections | none beyond the fold |
| designer (`.claude/agents/designer.md`) | the DoD's `test:` lines, the place of a new row, what the DoD runs | **none** (I14: 0) — rule 1 names `plans/builder-rules.md` 7b and `test-layers.json` only | rule 1: "a builder DoD's verification scope in this repository is `plans/builder-rules.md` 7b" → "a builder DoD's verification scope and its `test:` lines are `docs/TESTING.md` («Что запускать по своей правке», «Строка теста в DoD», «Бюджет / Файлы»)" |
| Lead / coordinator (CLAUDE.md) | DoDs, acceptance | rule 11 :294 "the rule text is `docs/TESTING.md`"; Contents row :33 | rule 4 and Contents row :31 re-pointed to the TESTING section (§10) |
| PROJECT.md p. 2 | dispatcher's view | :81 `docs/TESTING.md` | p. 2's 7b pointer → TESTING section |
| dispatch tools (`dispatch_new.py`, `dispatch_manifest.py`) | the `test:` line | none, and no check of the line exists (D7) | none now: a tool that refuses should name the section (FR-1); F8 |
| scout | — | — | not needed (no tests written) |

**Pin K-TESTPTR** — variant rows of POINTERS in `tools/tests/test_role_carriers_one_owner.py` (no new file):
`(".claude/agents/builder.md", "`docs/TESTING.md` «Что запускать по своей правке»", "docs/TESTING.md", "### Что запускать по своей правке")`,
`(".claude/agents/critic.md", "docs/TESTING.md «Бюджет»", "docs/TESTING.md", "### Бюджет")`,
`(".claude/agents/designer.md", "`docs/TESTING.md` («Что запускать по своей правке», «Строка теста в DoD»", "docs/TESTING.md", "### Строка теста в DoD")`,
`("CLAUDE.md", "`docs/TESTING.md` «Что запускать по своей правке»", "docs/TESTING.md", "### Что запускать по своей правке")`.
The CLAUDE.md Contents row stays a TOC_POINTERS row. Error direction: a renamed TESTING heading turns the row red (safe).

---

## §8 The rule «we do not create extra documents»

**Home**: PROJECT.md «Где что лежит», a paragraph right after the table (that section is the map of documents; it is
boot-loaded; the row `plans/builder-rules.md` leaves the table in the same edit). Alternatives: F2.

**Exact text** (~0.75 KB):

> **Лишних документов нет** (владелец, 17.11.2026). Правило для роли живёт только в основном документе: `CLAUDE.md` с
> импортами, файл роли `.claude/agents/<роль>.md`, `docs/TESTING.md`, `docs/TEAMWORK.md`, `docs/RUNBOOK.md`,
> `docs/SIBLING_MAP.md`, `PROCESS/`, скиллы, `design/` пакета (владельцы оси 31). Документа, который роль читает всегда
> сверх своего файла и бута (брифа), нет: нужное — разделом основного документа, лишнее не пишется. Не лишние — спека,
> пачка, находка, ревью, отчёт, снимок, очередь: у них одна задача. Новый основной документ — словом владельца, строкой
> этой таблицы и `CLAUDE.md` § Contents. Проверка: `tools/tests/test_role_carriers_one_owner.py`.

**Four questions (CLAUDE.md rule 10)**
- (a) Cost: role files grow (critic ~+10 KB, builder ~+4.5 KB), paid at every spawn of that role; a builder on a forge-only
  task now carries package lines it did not get before (builder-rules was in `given` only for package edits — PROJECT.md
  p. 1); the dispatcher no longer names brief paths in `given`; boot +~1.8 KB (§9). Paid by: every worker spawn, the Lead
  once now.
- (b) Axes touched: §1 list (1, 2, 4 row :95, 18, 31, 34, the AR-29 acceptor row). The full enumeration is the Lead's
  commit block.
- (c) Detector: K-NOBRIEF (deterministic, `tools/tests/test_role_carriers_one_owner.py`, runs in CI with `pytest tools/`
  — estimate: the CI layout was not re-read) + calibration check 33 new item (i) (text in card L, §11).
- (d) What stops a skip: the pin on the CI path (a resurrected brief or a pointer to one is red on the pushed range);
  critic Q11 "does it add text a role must read" reads a new document; the semantic case the pin cannot see (a standing
  document under another name) is check 33 (i) — on discipline, named.

**K-NOBRIEF design** (new test functions inside the existing file; parameterised):
- MAIN = `CLAUDE.md`, `PROJECT.md`, `.claude/agents/*.md`, `.claude/skills/*/SKILL.md`, `docs/TESTING.md`,
  `docs/TEAMWORK.md`, `docs/RUNBOOK.md`, `docs/SIBLING_MAP.md`, `PROCESS/*.md` (globbed at run time; an empty glob is a
  failure — positive control that the scan saw files).
- FORBIDDEN = regex, case-folded, slashes normalised: `docs/tasks/[^/\s`'"]*brief[^/\s`'"]*\.md` and
  `plans/builder-rules\.md`.
- (1) no MAIN file matches FORBIDDEN (message names file:line); (2) none of the six DELETED paths is tracked; (3) no
  tracked `docs/tasks/<name>.md` (top level only) has `brief` in its name.
- Error direction: false RED is the allowed side (a red names the file and the door "move it under `docs/tasks/specs/`
  or fold it into a main document").
- Adversarial inputs that must stay on the safe side: `docs\tasks\Critic-Diff-Brief.md` (backslash, case) → red;
  `docs/tasks/specs/td-11-lead-brief.md` → green (specs folder, intent brief of one task); the word "INTENT BRIEF" in
  designer.md and `"notes":"brief: …"` in CLAUDE.md → green (not a path); a pointer inside a fenced block of a MAIN file
  → red (fences are not exempt); `plans/builder-rules.md` named in historical files (specs, handoffs, piles,
  PROJECT_FULL, DECISIONS_ARCHIVE, FINDINGS.md, ADOPTION_LEDGER, factory-fixes.md, test-diet.md) → green (not MAIN).

---

## §9 Budgets

| Measure | Before | After (estimate) | Ceiling | Carrier |
|---|---|---|---|---|
| Boot total | 109 921 (brief, SessionStart line; not re-measured — no shell in this role) | ~111 700 | WARN > 110 000, BREACH > 120 000 (`tools/session_context.py` :208-209, :1388) | `python -B tools/session_context.py` BOOT BUDGET line |
| CLAUDE.md incl. imports | 50 808 | ~52 600 (CLAUDE.md own +~600: rule 9 +210, Cost gates +190, rule 3/4/Contents ±0…+60; PROJECT.md +~1 200: rule +750, п. 9 +330, map row −150, p. 1/2/13 ±0) | CLAUDE_WARN 58 500 (:235) | same line |
| critic.md | ~11 KB (scout), 178 lines (Read) | ~21 KB | none found (below) | `wc -c` in the card's witness |
| builder.md | ~6.2 KB (scout), 101 lines | ~10.5 KB | none found | same |
| designer.md | not measured | +~80 B | none | same |
| docs/TESTING.md | ~32 KB (scout) | ~36 KB | none | same |

**Ceiling search for role files:** Grep `(ROLE|AGENT)[A-Z_]*(CAP|CEIL|LIMIT|MAX|BUDGET)|…` -i over `tools/` → only
`agent_budget.py` (context tokens) and `install_parity.MAX_ANCHOR_LEN`; `agents_md.py` copies role FRONT MATTER only (its
`CODEX_LIMIT_STEP` is AGENTS.md's Codex notice); `role-load.json` lives in the package and guards the PACKAGE roles
(Grep `role-load\.json` in package tests → 5 files; in `tools/` → 0). No ceiling guards `.claude/agents/*.md` bodies.

**Raises:** none needed against a BREACH or CLAUDE_WARN. The boot crosses the WARN band (110 000): fork F3 (accept the
WARN line, or offset by a boot-diet pass first). Form rules of boot-diet § «Как пишутся правила для агентов» were applied:
pointers, not restatements (rule 1); the new rule is one paragraph (rule 3); history stays out (rule 4); rule numbers are
not reused (rule 5: builder.md and critic.md only APPEND rules; no rule is renumbered).

---

## §10 Readers of every touched or deleted file (rule 7)

Commands: the Grep calls of §3 (I3-I15) plus Grep `FORGE_CARRIERS` in `tools/` (3 hits: test_quarantine.py :51, :225,
:1340; plus :2199 inside `_purge_named_in_text`), Grep `install_parity_anchors` in `tools/` (2 files), Grep `builder-rules`
in `docs/` minus `tasks/` (27 lines), Grep `exchange-form` in `.claude/agents` (1) and `tools/digest_form.py` (2).

| Reader | Points at | Change |
|---|---|---|
| CLAUDE.md :31 Contents "What a builder may run" | builder-rules § 7b | → `docs/TESTING.md § Что запускать по своей правке` (Lead, L1) |
| CLAUDE.md :35 Contents "Critic review content" | the brief | → `.claude/agents/critic.md § 21-23` (L1) |
| CLAUDE.md :127 rule 3 | brief items 6-7 | → "`.claude/agents/critic.md` rule 22, Q6-Q7" (L1) |
| CLAUDE.md :154 rule 4 | builder-rules 7b | → "`docs/TESTING.md` «Что запускать по своей правке»" (L1) |
| CLAUDE.md rule 9, rule 12 | — | §6, §4.2.2 (L1) |
| PROJECT.md :45 map row | builder-rules | row removed; §8 rule added (L1) |
| PROJECT.md :75 p. 1 | «и `plans/builder-rules.md`» | → «целиком (правила билдера — его файл роли)» (L1) |
| PROJECT.md :79-80 p. 2 | 7b; brief «The two layers» | → TESTING section; «`.claude/agents/critic.md` rule 21» (L1) |
| PROJECT.md :83 p. 2 | «содержание — builder-rules п. 11» | → «содержание — там же, правило 4» (L1) |
| PROJECT.md :237 п. 13 | 7b | → TESTING section (L1) |
| PROJECT.md п. 9 | — | §6 (L1) |
| AGENTS.md | copy | regenerated (L1, `python tools/agents_md.py --repo <root>`) |
| critic.md :77, :161, :164, :173 | brief | rules 12, 18-20 (C3) |
| builder.md :49, :53 | 7b | rule 4 (C3) |
| designer.md :20, :42 | 7b; "critic brief item 4" | rule 1 → TESTING (§7); rule 2 → "critic.md rule 22 Q4" (C3) |
| docs/TESTING.md :65, :89, :102, :123, :170, :228, :229 | builder-rules; brief Q5 / layers | :89, :170 → "вопрос 5 (rule 22 Q5) `.claude/agents/critic.md`"; :102, :229 → "`.claude/agents/critic.md` rule 21" (keep «как и чем он это проверяет, написано только там»); :65, :123, :228 §4.2.1 (C1) |
| docs/RUNBOOK.md :125, :218, :380 | 7b | → TESTING section (C1) |
| docs/RUNBOOK.md :399 | builder-rules п. 13 | → "`.claude/agents/builder.md` rule 9" (C1) |
| docs/RUNBOOK.md :617 | builder-rules п. 18 | → "`.claude/agents/builder.md` rule 10" (C1) |
| docs/RUNBOOK.md :630-631 | builder-rules item 20 | → drop the parenthesis's builder-rules part (the item itself is the home) (C1) |
| docs/CLAUDE_HOST_ADAPTATIONS_FULL.md :7, :33 | the brief | → "`.claude/agents/critic.md` rule 22" (C1) |
| docs/tasks/test-diet.md :17, :35, :88 | the test-diet briefs, critic brief | a note «(удалён 17.11.2026; правило — `docs/TESTING.md`)» after each (C1) |
| docs/SIBLING_MAP.md :34, :95, :401, :478-479, :484-490, :493, :496, :505, :507-508, :564, :577, :602 | builder-rules / brief | axis 31 owner list: builder-rules 7b → `docs/TESTING.md` «Что запускать по своей правке»; brief → `.claude/agents/critic.md` rules 21-23; rows :489, :490, :507, :508 removed; :484-486 pointers re-pointed; :34, :95, :401, :496, :505, :564, :577, :602 re-pointed (Lead, L1) |
| PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md :392 | 7b | → TESTING section; + check 33 (i) (Lead, L1) |
| DECISIONS.md :32 | the brief | F5 (Lead) |
| tools/tests/test_role_carriers_one_owner.py | BRIEF, RULES, 17 lines | C2 |
| tools/test_handoff_rule_anchors.py :5, :9, :38-39, :104-116, :169-172 | BRIEF, RULES | C2 |
| tools/install_parity_anchors.json :22 | CLAUDE.md anchor "`docs/tasks/critic-diff-brief.md` items 6-7" | → "`.claude/agents/critic.md` rule 22, Q6-Q7" (C2); reader `tools/install_parity.py` unchanged, `tools/test_install_parity.py` in the witness |
| tools/test_quarantine.py :51 FORGE_CARRIERS | builder-rules | `"plans/builder-rules.md"` → `"docs/TESTING.md"` (C2; E4) — a gate-adjacent tool: staged, the Lead commits |
| tools/test_test_quarantine.py :389, :413, :841, :1489, :1613 | builder-rules as a fixture carrier | the same rows with `docs/TESTING.md` (C2) |
| tools/test_split.py :1843 | builder-rules in a printed `git grep` | → `docs/TESTING.md` (C2) |
| tools/owns_readers.py :26, :55 | brief item 13 (d); builder-rules 7b | :26 → "critic.md rule 24 Q13 (d)" if F6 = (a), else "the plan critic's own walk"; :55 → TESTING section (C2) |
| tools/dispatch_gate.py :1870 | builder-rules item 20 | comment → "(P31; RUNBOOK §12 item 8)" (C2; hook file: staged, the Lead commits) |
| tools/test_language_sites.py :4 | builder-rules 7b | → TESTING section (C2) |
| tools/test_dispatch_manifest.py :844; fixtures K3, K4, K7 | builder-rules inside frozen historical prompts | **unchanged**: the path is parsed DATA of a fixture, not a pointer |
| told-before-work batch-1 :41 TBW1-14; forge batch-7 :76 FG7-51; live-run-fvf FV2-14 (card :93 + its finding) | critic-diff-brief.md as a file to write | untaken batches («ожидает»): the Lead re-points the file column to `.claude/agents/critic.md` (L1) |
| spec 20261116-spec-facts-by-code §4.1/§4.2/L4/L5 (stream L, unlanded) | brief item 13; builder-rules L5 | F6 |
| historical: docs/tasks/specs/*, handoffs, reviews, compact snapshots, plans/piles cards/findings/closed batches, PROJECT_FULL, DECISIONS_ARCHIVE, FINDINGS.md, ADOPTION_LEDGER.md, factory-fixes.md, BACKLOG.md | any | **not edited** (records; excluded from K-NOBRIEF and from POINTERS) |

---

## §11 Builder cards (disjoint files) and the Lead's part

Order: **C1 ∥ C3 ∥ L1-draft** (one branch `pile/<slug>/batch-<N>` per the Lead's choice) → converge → **C2** → **L-commit**
(deletions + mechanism files + the C2/C3 staged files) in ONE commit, so no tree on `main` has a pointer to a deleted file
(E1). The batch canon runs in CI after convergence (CLAUDE.md rule 4).

### C1 — docs (builder)

given: this spec §4.2.1, §4.5, §10; `C:/QAFactory/forge-repo/plans/builder-rules.md`; `C:/QAFactory/forge-repo/docs/TESTING.md`; `C:/QAFactory/forge-repo/docs/RUNBOOK.md`; `C:/QAFactory/forge-repo/docs/CLAUDE_HOST_ADAPTATIONS_FULL.md`; `C:/QAFactory/forge-repo/docs/tasks/test-diet.md`
owns:
C:/QAFactory/forge-repo/docs/TESTING.md
C:/QAFactory/forge-repo/docs/RUNBOOK.md
C:/QAFactory/forge-repo/docs/CLAUDE_HOST_ADAPTATIONS_FULL.md
C:/QAFactory/forge-repo/docs/tasks/test-diet.md
non-goals: deleting any file; role files; CLAUDE.md, PROJECT.md, SIBLING_MAP, PROCESS; any tools/ file; rewording 7b beyond §4.2.1's listed edits
handoff: C:/QAFactory/forge-repo/docs/tasks/handoffs/t-<id>-c1-testing-runbook.md
edges: E3, E6 (Russian text moves verbatim), E9
DoD: `python -B <scratch>/c1_keys.py` (DOC-DISPATCH witness: full source in the report, never committed; keys verbatim from this DoD; one negative control) — keys present in TESTING.md: `### Что запускать по своей правке`, `не регрессия, не соседи, не большие файлы`, `test_story_run_words.py`, `Удаляя тестовый файл`, `rule 21`; keys ABSENT from all four owns: `builder-rules`, `critic-diff-brief`, `test-diet-brief`, `test-diet-fold-brief` (except the three deletion notes in test-diet.md, which name the files as deleted — the script counts those three exact lines); test: none -- поведения нет | expected from: §4.2.1, §10
siblings: axis 31 (owner moves), axis 1 row :34

### C3 — role files (builder; mechanism paths: STAGED, the Lead commits)

given: this spec §4.1, §4.2.3, §6 (critic.md rule 5), §7; `C:/QAFactory/forge-repo/docs/tasks/critic-diff-brief.md`; `C:/QAFactory/forge-repo/plans/builder-rules.md`; the three role files
owns:
C:/QAFactory/forge-repo/.claude/agents/critic.md
C:/QAFactory/forge-repo/.claude/agents/builder.md
C:/QAFactory/forge-repo/.claude/agents/designer.md
non-goals: renumbering any existing rule; changing install_parity anchor lines (rule openers 1-17 of critic, 1-7 of builder, designer's opener lines); scout.md (N7); the stream-L Q13 text unless F6 = (a)
handoff: C:/QAFactory/forge-repo/docs/tasks/handoffs/t-<id>-c3-role-files.md
edges: E2, E6, E7, E10
DoD: `python -B <scratch>/c3_keys.py` (DOC-DISPATCH witness as C1) — keys present: critic.md `21. The two layers of a diff gate`, `22. The standing questions`, `23. What comes back from a diff gate`, `Q6. **DUPLICATION AND CONSISTENCY**`, `Q7. **CODE QUALITY**`, `Q12. **ONE ROAD**`, `functions over roughly 60 lines or with more than three nesting levels in the NEW code`, `a line for the coordinator to tell someone is itself a finding`, `critic_verdict_check.py`, `rules 16-17`; builder.md `9. Runs, cheaply.`, `10. Git.`, `11. In the package.`, `«Что запускать по своей правке»`; designer.md `«Строка теста в DoD»`, `critic.md rule 22 Q4`; ABSENT from all three: `critic-diff-brief`, `builder-rules`; and `python -m pytest C:/QAFactory/forge-repo/tools/test_handoff_rule_anchors.py -q` green except the two rows C2 rewrites (named in the report); test: none -- текст ролей; поведение проверяет C2 | expected from: §4.1, §4.2.3
siblings: axis 31, axis 2 (exam deviation line), axis 34 row :602

### C2 — tools and tests (builder; after C1, C3, L1-draft converge)

given: this spec §1, §7, §8 (K-NOBRIEF), §10; `tools/tests/test_role_carriers_one_owner.py`; `tools/test_handoff_rule_anchors.py`; `tools/install_parity_anchors.json`; `tools/test_quarantine.py` :45-60, :215-235, :1330-1350, :2190-2210; `tools/test_test_quarantine.py`; `tools/test_split.py` :1835-1845; `tools/owns_readers.py` :20-60; `tools/dispatch_gate.py` :1866-1871; `tools/test_language_sites.py` :1-10; `ai-packages/qa-factory/scripts/selftest.py` :721-736 (read only)
owns:
C:/QAFactory/forge-repo/tools/tests/test_role_carriers_one_owner.py
C:/QAFactory/forge-repo/tools/test_handoff_rule_anchors.py
C:/QAFactory/forge-repo/tools/install_parity_anchors.json
C:/QAFactory/forge-repo/tools/test_quarantine.py
C:/QAFactory/forge-repo/tools/test_test_quarantine.py
C:/QAFactory/forge-repo/tools/test_split.py
C:/QAFactory/forge-repo/tools/owns_readers.py
C:/QAFactory/forge-repo/tools/dispatch_gate.py
C:/QAFactory/forge-repo/tools/test_language_sites.py
non-goals: any new test file; the package; test_dispatch_manifest.py and its fixtures (historical data); behaviour of test_quarantine beyond the one constant
handoff: C:/QAFactory/forge-repo/docs/tasks/handoffs/t-<id>-c2-pins.md
edges: E1, E4, E8, E10
DoD: `python -m pytest tools/tests/test_role_carriers_one_owner.py tools/test_handoff_rule_anchors.py tools/test_install_parity.py tools/test_test_quarantine.py tools/test_owns_readers.py -q` from the repo root on the converged tree, plus the E4 set comparison (script in full in the report: `_TEST_NAME_IN_TEXT.findall` over the OLD `plans/builder-rules.md` blob of the base vs over the NEW `docs/TESTING.md`; the old set must be a subset of the new; every name only in the new set listed); test: tools/tests/test_role_carriers_one_owner.py::K-NOBRIEF rows, K-TESTPTR POINTERS rows | expected from: §7, §8
siblings: axis 31 (pins), axis 18 n/a (no ratchet row moves)

Exact C2 transformations:
- `test_role_carriers_one_owner.py`: `BRIEF`/`RULES` constants → `CRITIC = ".claude/agents/critic.md"`, `TESTING = "docs/TESTING.md"`, `RULES_7B = "### Что запускать по своей правке"`; OWNER_KEYS: `scope:builder` owner TESTING; `scope:tests` owner TESTING with key «Покраснел пин из таблицы выше — удаляется, не чинится» (TESTING.md:219; the builder-rules wording dies); `review:critic`, `review:one-road` owner CRITIC. POINTERS: rows :59, :60, :63, :66-68, :70, :72, :73, :76, :78, :91, :114, :119 re-pointed per §10; rows :61, :62, :71, :92, :96-98 (carrier RULES or BRIEF) removed; row :90 becomes `(TESTING, "`docs/RUNBOOK.md` §7", ...)`; K-TESTPTR rows (§7); K-NOBRIEF functions (§8); module docstring's EXCLUDED list unchanged. `test_negative_control_real_key_in_a_copy` (owner and pointer file become the same file, the check can no longer fail as written) is DELETED under TESTING.md «Что не пишется» (negative control inside a test) — named in the report with "behaviour still checked by: test_one_owner_per_key".
- `test_handoff_rule_anchors.py`: `BRIEF` → `CRITIC` rule 23 block; `test_brief_what_comes_back` → asserts `rule_block(read(CRITIC), 23)` holds "rules 16-17", "`handoff:`" or "rule 16" form chosen by C3's text, and `critic_verdict_check.py`, and `restated(...) == []`; `test_builder_rules_p11` DELETED (its carrier no longer exists; the one carrier is builder.md rule 4/7, whose keys `test_role_rule_carries_file_rule` already checks); `test_negative_control_restatement_in_a_pointer_copy` DELETED (TESTING.md «Что не пишется»); docstring lines :5, :9 updated.
- the remaining files: the one-line edits of §10.

### L — the Lead (mechanism commit; `tier: opus`; axis block; `Deviation: exam not run; debt F3-1`)

- L1: CLAUDE.md (rules 3, 4, 9, 12, Contents rows :31, :35); PROJECT.md (map row, §8 rule, p. 1, p. 2, п. 9, п. 13);
  AGENTS.md regenerated; docs/SIBLING_MAP.md (§10 rows); PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md :392 + check 33 (i):
  "(i) Standing documents (PROJECT.md «Где что лежит», «Лишних документов нет», the owner's word 17.11.2026): sample the
  role files, CLAUDE.md and PROJECT.md for a sentence that sends a role to read a file outside the main documents every
  time (a «read X before work» to a non-main path) — each a finding; the name pin is `tools/tests/test_role_carriers_one_owner.py`
  (K-NOBRIEF)."; the pile rows TBW1-14, FG7-51, FV2-14 re-pointed; DECISIONS.md D-0033 (F5).
- L2: `git rm` of the six files; commits C2/C3 staged mechanism files (role files, dispatch_gate.py, test_quarantine.py
  if gated) with L1 in ONE commit after the critic of code (one pass on the topic, CLAUDE.md rule 13 R13-g).

---

## §12 Edges, each with its invariant

| # | Edge | Behaviour | Invariant |
|---|---|---|---|
| E1 | TEMPORAL: briefs exist before L2, absent after | deletion and every redirect land in ONE commit | no commit on `main` where a main document points at a missing file (POINTERS red otherwise) |
| E2 | stream L (spec 20261116-spec-facts-by-code) still targets brief item 13 and builder-rules L5 | F6 | its text never resurrects a brief; K-NOBRIEF refuses `docs/tasks/*brief*.md` |
| E3 | pile node rows naming the brief | untaken batches: row edited by the Lead | a node never writes a deleted path |
| E4 | FORGE_CARRIERS loses builder-rules | constant → `docs/TESTING.md` | the gate-named set from forge texts never shrinks (a test file named only by 7b would otherwise fall into `unlisted:`/quarantine) |
| E5 | historical files keep dead pointers | not edited | they are outside MAIN and outside POINTERS; nothing reads them as rules |
| E6 | Russian → English (builder.md rules 9-11) | translated; the plan critic checks each condition/consequence pair against §4.2 | no rule of builder-rules loses its condition or its consequence |
| E7 | critic.md edit owes the critic exam (rule 10); exam absent | commit line `Deviation: exam not run; debt F3-1` | an edit to critic.md never lands silently past rule 10 |
| E8 | K-NOBRIEF false red / false green | red names file:line + door; the semantic miss → check 33 (i) | a MAIN pointer to a brief path is always red |
| E9 | a role with no testing duty (scout) | no K-TESTPTR row | the pin lists only roles that must use TESTING.md (§7) |
| E10 | conflict: "no restatement" (axis 31) vs "a role file says what THIS role does" (boot-diet rule 1) | pointers + one phrase; OWNER_KEYS sentences occur only in their owner | a full key sentence never stands in two scanned files |
| E11 | boot crosses WARN 110 000 | F3 | BREACH (120 000) and CLAUDE_WARN (58 500) are not crossed |
| E12 | `rule_block` splits role files on `^\d+\. ` | questions are `Q1.`…`Q12.` | rules 16, 17, 18 stay findable (`test_critic_rule_17_not_renumbered`) |

---

## §13 Forks (returned; recommendation first)

- **F1** (settled by O-1) — TESTING.md is main.
- **F2** Home of the no-extra-documents rule: (a) PROJECT.md «Где что лежит» after the table — **recommended** (the map of
  documents, boot-loaded); (b) boot-diet SKILL § «Как пишутся правила для агентов» item 8 (the topic home of rule-writing,
  but not boot-loaded: a session about to create a file never sees it); (c) PROJECT.md «Командная работа» new п. 14.
- **F3** Boot WARN: (a) accept the WARN line for now, and the next boot-diet pass at handoff absorbs it — **recommended**
  (no breach, the owner allowed size for rules); (b) trim first (e.g. move PROJECT.md «Прогоны и эксперименты» detail to
  RUNBOOK) in the same commit.
- **F4** `docs/tasks/exchange-form.md`: (a) IN, as node N7 of this spec (grammar → scout.md, example → a `tools/fixtures/`
  file, §2 → CLAUDE.md rule 11) — **recommended** (the owner: «всех брифов»; one road for every role's standing reading);
  (b) declare it a code contract (like a schema) and add it to the main list. Cost of (a): one more builder card and a
  test fixture move; CLAUDE.md +~400 B.
- **F5** D-0033 text (D1): (a) the Lead appends the D-0056 refinement clause — **recommended**; (b) leave the record, the
  rule text holds (a reader of DECISIONS.md is misled).
- **F6** Stream L's plan-gate text (D4): (a) this change absorbs it — critic.md rule 24 "The plan gate" with Q13 verbatim
  from spec 20261116 §4.1 (plus pre-release critic brief item 3, "challenge the Lead's fork decisions", as Q13 (e)), the
  designer line of §4.2 pointing at "critic.md rule 24 Q13 (d)", L5 into the TESTING section — **recommended** if that spec
  is accepted; (b) stream L lands later and writes critic.md itself. Not established: whether spec 20261116 is accepted.
- **F7** builder-rules item 1 integrator-only list and the tail's `judge.provider: none`: (a) drop the list (owns decides),
  keep `judge.provider: none` in builder.md rule 11 — **recommended**; (b) keep the list in builder.md. Not established:
  whether any gate still enforces the list.
- **F8** TESTING.md:88 claims a code check of the `test:` line that is not on this tree (D7): (a) ask the coordinator which
  stream owns it; until it lands, the sentence reads «проверит код (узел <id>)» — **recommended**; (b) delete the claim.
- **F9** builder-rules 9 (backward compatibility) is a package rule living in a forge role file: (a) builder.md now, and a
  finding to the package pile proposing it as AR-3's change check — **recommended** (another zone: the package design);
  (b) builder.md only.

## Small choices closed by the designer

- Folded role text is English (every `.claude/agents/*.md` is English; kit parity `toolkit/.claude/agents/*`); text moving
  into TESTING.md stays Russian (verbatim, no translation risk).
- critic questions are labelled `Q1.`…`Q12.` (E12).
- New critic rules append as 21-23 (no renumbering: install_parity anchors 1-17, test_handoff 16-18).
- 7b's home is TESTING.md, not CLAUDE.md rule 4 (O-2's "a main document the role already loads": builder, designer and
  critic all point to TESTING.md; CLAUDE.md budget kept).
- Negative-control tests that the move breaks are deleted, not rewritten (TESTING.md «Что не пишется»), each named.
- test_dispatch_manifest fixtures stay (historical prompts as data).

## Not established

- Byte sizes: not measured (no shell in this role); every "after" is an estimate; the card witnesses measure.
- Whether `tools/test_split.py`'s printed carrier line is pinned by another test (C2 greps it).
- Whether the kit side of `install_parity` needs the same anchor change (C2 runs `tools/test_install_parity.py`).
- Whether RUNBOOK §9.6 carries "live project read-only" for the night agent (not re-read).
- Whether CI runs `tools/tests/` (CI layout not re-read; K-NOBRIEF relies on it).
- The status of spec 20261116-spec-facts-by-code (F6) and of the `test:`-line check (F8).
- `judgment-census.json` `SCAN_ROOT` not re-read (census class claim in §1).

## Owner's sentence → where in this spec

| Owner's sentence (17.11.2026) | Where |
|---|---|
| «который раз бриф расходится с правилами. Проверь все брифы» | §3 inventory, §5 divergences |
| «зачем нам бриф как отдельный документ? У критика есть роль и бут загрузка» | §4.1 (critic brief → critic.md) |
| «избавиться от всех брифов и закрепить что мы не создаём лишние документы» | §1, §8, K-NOBRIEF |
| «не просто удалить, а проверить что есть в брифе и нет в роли или правилах … найти ему "дом"» | §4.1-§4.7 |
| «не в ущерб правилам. Если не влезет можно поднять» | §9 (no raise needed; F3) |
| «если для полноты класса надо починить то что сейчас не в контексте, то можно отложить в чужую кучку, но это должен быть редкий случай» | §6 |
| «на этот документ смотрят несколько ролей … оставляем как основной документ и проверяем что на него есть ссылки» (O-1) | §7 |
| «Зачем у нас этот отдельный документ если есть роль билдера? Там есть что-то что нужно не только билдеру?» (O-2) | §4.2 table |

## Reading trail

Read whole: docs/tasks/critic-diff-brief.md (126 l.), plans/builder-rules.md (136 l.), .claude/agents/critic.md (178),
.claude/agents/builder.md (101), tools/tests/test_role_carriers_one_owner.py (254), tools/test_handoff_rule_anchors.py (173),
.claude/skills/boot-diet/SKILL.md (138), docs/tasks/exchange-form.md (157), the four 0.9/test-diet briefs (86/57/73/100).
Read ranges: docs/TESTING.md :36-230 + headings; docs/SIBLING_MAP.md :24-98, :468-515; docs/tasks/test-diet.md :1-191;
docs/RUNBOOK.md :394-401, :610-654 + headings; PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md :1005-1046, :1130-1144;
tools/install_parity_anchors.json :1-40, :110-179; tools/owns_readers.py :20-59; tools/dispatch_gate.py :1866-1871;
tools/test_dispatch_manifest.py :830-854; tools/test_split.py :1835-1849; selftest.py gate_named_files :721-746;
docs/tasks/specs/20261116-spec-facts-by-code-spec.md :400-489; docs/TEAMWORK.md §2, §9; DECISIONS.md :32;
pile headers told-before-work/batch-1, forge/batch-7, live-run-fvf/batch-2. Searches: §3 I1-I15 and §10 header, each
negative with its positive control.

## Lead decisions (17.11.2026, Lead of the session; all by recommendation, reversible until the builders start)

- F2 = (a) PROJECT.md «Где что лежит». F3 = (a) the WARN line is accepted, the next boot-diet pass absorbs it.
- F4 = (a) `exchange-form.md` is in, node N7 (the owner: «всех брифов»).
- F5 = (a) the Lead appends the D-0056 refinement clause to D-0033.
- F6 = (a): spec 20261116-spec-facts-by-code is accepted (t-897) and in implementation (t-917…); the plan critic checks
  whether stream L has already written `critic.md` on main, and if so the text is joined, not doubled.
- F7 = (a). F8 = (a). F9 = (a) with a finding to the package pile.
- "Not established" list: each line is a witness duty of the card that touches it; the plan critic checks the two that
  can break a builder (CI runs `tools/tests/`; the kit side of `install_parity`).
- Plan critic: mandatory (a new idea of the owner, PROJECT.md step 6) — dispatched next.

## Lead decisions on the forks (architect-rank session, 17.11.2026; by recommendation, until the owner's word)

- F2 = (a) PROJECT.md «Где что лежит». F3 = (a) accept the WARN, boot-diet at handoff. F4 = (a) exchange-form.md is in,
  node N7. F5 = (a). F7 = (a). F8 = (a). F9 = (a).
- F6: the plan critic answers whether spec 20261116 §4.1 is accepted text; if it is, (a); if not, (b).
- Rule 13 of builder-rules (bounded background wait): its home and its code gate are designed by t-1122 (the owner's word
  17.11.2026 on hung processes); this spec keeps only the pointer and takes the home t-1122 names.
- Plan critic: mandatory (a new idea of the owner, step 6) -- t-1126 (report file named t-1124-… by a Lead id error).

Note (17.11.2026): the section «Lead decisions (17.11.2026, Lead of the session…)» above was written by the parallel session
61b75a79 by mistake. Where the two sections differ (F6), THIS section governs: F6 is answered by the plan critic.
