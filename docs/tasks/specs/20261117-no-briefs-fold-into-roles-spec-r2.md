# t-1133 — No standing briefs: fold every brief into the main documents — spec r2 (DRAFT, designer fix round)

Status: designer draft r2 for Lead acceptance. Supersedes r1 (`20261117-no-briefs-fold-into-roles-spec.md`, t-1117) WHOLE:
a builder reads this file only. Applies every fix of both plan verdicts (`reviews/t-1124-no-briefs-spec-plan.md` = verdict
**A**, B1-B7 / F1-F12; `reviews/t-1124-no-briefs-plan.md` = verdict **B**, B1-B3 / M1-M9 / m1-m6) and the Lead decisions of
17.11.2026 (architect-rank session). Feature F19. This draft is English; texts that land in Russian documents are given in
Russian.

## §0 What binds this spec

The owner's words (17.11.2026), quoted as the Lead carried them in dispatch t-1133:
- **W-1** «Надо избавится от всех брифов и закрепить что мы не создаём лишние документы. Но не просто удалить, а проверить
  что есть в брифе и нет в роли или правилах и если это что-то нужное, то найти ему "дом" из основных документов».
- **W-2 (O-1)** `docs/TESTING.md` stays a MAIN document, and every role that must use it points to it.
- **W-3 (O-2)** `plans/builder-rules.md` is dissolved («Зачем у нас этот отдельный документ если есть роль билдера?»).
- **W-4** «если для полноты класса надо починить то что сейчас не в контексте, то можно отложить в чужую кучку, но это
  должен быть редкий случай, а не отложить починку правил когда мы чиним правила».

Lead decisions carried in (not forks here): r1 F2 (a) rule home PROJECT.md «Где что лежит»; F3 (a) the boot WARN is
accepted (§9 carries the number with its carrier); F4 (a) `exchange-form.md` is in (node N7); F6 (a) stream L's plan-gate
text is absorbed (critic.md rule 24); F7 (a); F8 (a); F9 (a); F5 WITHDRAWN — replaced by the D-0033 trim (§5 D1). Verdict A
B3: the package IS edited (card PKG). Verdict A B4: (a) re-layer the `test_arch_check.py` keep row honestly. Verdict A F3:
the holder of 7a vs 16 (б) is 16 (б). builder-rules item 13: the rule text and RUNBOOK §9.8 belong to spec t-1122
(`20261117-bounded-waits-mechanism-spec.md` §6, its stdin class G2 dropped by the Lead); this spec only points there.

---

## §1 Scope, invariants, owners

**What changes.** Six standing briefs are deleted after every needed statement got one home in a main document:
`docs/tasks/critic-diff-brief.md`, `plans/builder-rules.md`, `docs/tasks/pre-release-0.9-brief-common.md`,
`docs/tasks/pre-release-0.9-critic-brief.md`, `docs/tasks/test-diet-brief.md`, `docs/tasks/test-diet-fold-brief.md`
(wave 1). `docs/tasks/exchange-form.md` is folded and deleted in wave 2 (N7). `docs/retro/README.md` is folded and
deleted (fork F-R2-3, recommended). A rule forbids standing briefs again (§8) with a deterministic pin on the CI path and a
calibration check. The owner's W-4 is written, in ONE wording, into CLAUDE.md rule 9, PROJECT.md п. 9, critic.md rule 5 and
critic.md Q4 (§6).

**The package is edited** (verdict A B3, B B1; r1's "not edited" was false). Card PKG owns
`ai-packages/qa-factory/design/architecture.md` and `ai-packages/qa-factory/scripts/tests/test-layers.json`. AR-n touched,
each with the change check its own text demands, written into PKG's DoD:

| AR | Where | What changes | Change check (from `design/architecture.md`) in the DoD |
|---|---|---|---|
| AR-29 | architecture.md:144 carrier `dev:docs/tasks/critic-diff-brief.md` question 11 | → `dev:.claude/agents/critic.md` rule 22 Q11 | the producer–reader walk both ways: CLAUDE.md rule 10 paragraph ("critic question 11"), SIBLING_MAP:577 (acceptor row) and designer.md rule 1 change in the same batch (axis 1 tie); :151 "the critic's question 11" stays true (same number) |
| AR-20 | architecture.md:222 "critic-diff-brief question 9", :223 `dev:plans/builder-rules.md` rule 7; test-layers.json rows | :222 → `dev:.claude/agents/critic.md` rule 22 Q9; :223 → `dev:docs/TESTING.md` «Что запускать по своей правке»; one keep row re-layered, none leaves `keep`, none is added | "list every row added or raised (key, old -> new, reason)": the PKG report lists `test_arch_check.py` gate_named -> data_join and the six `why`/`named_by` rewrites; no ratchet row raised. :224 "question 9" stays true (Q9) |
| AR-11 | architecture.md:122 `dev:plans/builder-rules.md` rule 5 | → `dev:.claude/agents/builder.md` rule 11 | no role load changes (forge role files are not package roles): "Text added to a role's context removes at least as much" n/a — named in the report |
| AR-3 | architecture.md:64 `dev:plans/builder-rules.md` rules 1 and 9 | → `dev:.claude/agents/builder.md` rules 4 and 11 | the carrier still states "read a new key with a default; an older project runs without re-onboarding" (builder.md rule 11 text, §4.2.3) |

Package commit lines (PKG): the form's only carrier is `tools/architecture_gate.py`; the lines are
`architecture: AR-29, AR-20, AR-11, AR-3 -- dev: carrier pointers re-pointed to the role files and docs/TESTING.md; one keep row re-layered by its real layer; no invariant changed`
and
`judgment: none -- pointers and one keep-row label; no check unit, census row or refusal changes`.
`python -B scripts/selftest.py --lang` (FR-30) runs in PKG's witness. The ~36 package `.py` comments and one
`references/gate-registry.json:188` text citing "builder-rules N" stay as history (Lead decision); builder.md rule 11 carries
the mapping line (§4.2.3).

**Checks added or altered — owner served and census class (AR-29, P27):**

| Check | Owner it serves | Census class |
|---|---|---|
| K-NOBRIEF (`tools/tests/test_role_carriers_one_owner.py`): no MAIN document names a deleted file or its stem; the deleted paths stay untracked; no top-level `docs/tasks/*brief*.md` | data (code): presence of paths and names | forge test, outside `judgment-census.json` (`SCAN_ROOT = "scripts"`, `test_judgment_census.py:74`, measured by verdict A F10) |
| K-REG: MAIN is READ from the axis-31 table of `docs/SIBLING_MAP.md` (one register) | data (code): a table row and its class word | same |
| K-TESTPTR: every role that must use `docs/TESTING.md` carries a pointer to a named section (POINTERS rows) | data (code) | same |
| POINTERS / OWNER_KEYS re-pointed (axis 31); `test_handoff_rule_anchors` rule 23 row; `test_digest_form` fixture/scout rows (wave 2) | data (code) | same |
| critic.md rule 24 Q13 (the plan gate, absorbed from spec 20261116) | judgment (the critic; accepted by the Lead) | n/a (role text) |
| Calibration check 33 (i): a main document sending a role to a non-main standing file; a new file outside the not-extra classes | judgment (Lead at calibration, accepted by the Architect's review) | n/a (protocol) |
| test-layers.json `test_arch_check.py` layer | data (a keep row; its layer and why are judged by the code critic, Q5 (g)) | package data, no census unit |

**Mechanism.** A mechanism change (role carriers, a new rule, a new pin, a calibration item): every Lead commit carries
the rule-10 axis block for EVERY axis of the current map (the Lead enumerates) and `tier: opus`. Axes this change touches:
**1** (policy ↔ role files: CLAUDE.md rule 10 paragraph ↔ critic Q11 ↔ designer rule 1, kept in one merge; SIBLING_MAP:34
"what a builder runs ↔ every dispatch text"; :35 the digest trio, wave 2), **2** (critic.md rule 10 exam; scout.md rule 6
golden set — both instruments absent: `PROCESS/` holds 12 files, no `CRITIC_EXAM.md`, no `SCOUT_GOLDEN_SET.md` (Glob
`*.md` in `PROCESS/`); road: commit lines `Deviation: exam not run; debt F3-1` (precedent 1f165a38) and, wave 2,
`Deviation: scout golden set not run (PROCESS/SCOUT_GOLDEN_SET.md absent; exams deferred, D-0037)`), **4** (SIBLING_MAP:95
"Builder rules" row), **18** (SIBLING_MAP:401 Q9's carrier; architecture.md:222), **20/AR-20** (test-layers.json), **31**
(the main axis), **32** (AR-29 acceptor row :577), **34** (reviewers row :602).

---

## §2 Definitions — the border (verdict A F5, F6, F11; B M4, M5)

**One register (B M4, A F5/F12).** A MAIN document is a `.md` file named in the axis-31 table of `docs/SIBLING_MAP.md`
(heading `## Axis 31 — Role carriers: one owner per aspect`) whose last cell («Owner / pointer») starts with the word
`owner` or `procedure`. Nothing else is a list of main documents: PROJECT.md's rule (§8) points to that table and re-lists
nothing; K-NOBRIEF reads MAIN from it (K-REG). Today's owner/procedure `.md` rows include CLAUDE.md, PROJECT.md, the role
files, TEAMWORK, RUNBOOK, OWNER_PRINCIPLES, TWO_VOCABULARIES, SYSTEM_PROMPT, BOOT, DELEGATION_TABLE, SIBLING_MAP, the
PROCESS files, the skills (rows :524-529 already exist — verdict A F5's "no skills row" is corrected by reading :518-533).
Rows ADDED by this spec: `docs/TESTING.md` (owner) and `ai-packages/qa-factory/design/*.md` (owner; a glob row). Rows
REMOVED: `plans/builder-rules.md` (:489), `docs/tasks/critic-diff-brief.md` (:490), the two 0.9 briefs (:507, :508); wave 2
`docs/tasks/exchange-form.md` (:506). Non-main classes keep their rows (`record`, `state`, `generated`, `form`, `machine`,
`reason only`, `historical`).

**Extra document (standing brief)** — a file a role must read every time it works, or every time a class of dispatch names
it, that is not MAIN.

**Not extra — an OPEN class (B M4, A F5):** whatever has one task, one moment, or is a record. Examples, not a closed list:
a spec under `docs/tasks/specs/` (its `reports/`, `reviews/`, and a Lead's intent brief to a designer as a file there, e.g.
`specs/td-11-lead-brief.md`, `specs/fg-context-and-hygiene-lead-brief.md` — legal: one task); a batch file with its
`## Бриф` section and its header line «Общий бриф дизайнерам» (per-batch text; `tools/piles.py:1934` requires the heading);
a card and its «Бриф пачки N» section; a finding; a review; a report or handoff; a compact snapshot; a queue
(`docs/tasks/lead-queue.md`, `architect-queue.md`); a plan of one task (`docs/tasks/test-diet.md`, `factory-fixes.md`,
`onboarding-streams-2026-11-12.md`, `t-183-of3-1c-config-census.md`); an experiment notebook; a retro inbox entry; an exam
run log; a journal; a register or ledger the rules read as DATA (`docs/tasks/specs/reports/t-2046-language-exceptions-census.md`
read by critic Q12 (c), like a ratchet file — B m3); an archive; a fixture.

**`docs/*_FULL.md` carve-out (A F11).** `docs/PROJECT_FULL.md` is frozen. `docs/CLAUDE_HOST_ADAPTATIONS_FULL.md` keeps live
"where it stands now" pointers (its axis-31 row: `reason only`), so its two pointers are re-pointed (card C1).

**Decidable border for a weaker model (K5).** A new tracked file is legal when ONE holds: (1) it is code, a test, data or a
fixture; (2) it falls in the not-extra class above (it serves one task or moment, or it is a record or ledger); (3) it is a
new main document: a row `owner`/`procedure` in the axis-31 table, added by the Lead's mechanism commit (SIBLING_MAP is a
`MECHANISM_PREFIXES` path, `tools/mechanism_gate.py:218`, so only a `tier:` commit lands it) on the owner's word. Anything
else that a role is told to read every time is an extra document. On the execution path: K-NOBRIEF in CI
(`.github/workflows/forge-check.yml:96`, `python -m pytest tools/ -q`, measured by both verdicts) and the mechanism gate on
the register. The semantic case (a standing file under another name, never cited by a stem) is on discipline, detector
calibration check 33 (i) (§8).

---

## §3 Inventory and classification (K2: verdict A F6, B M5, B K2)

Searches (Grep tool, `C:/QAFactory/forge-repo`, worktrees/logs/ci-out excluded): I-1 the six names + `exchange-form` over the
repo minus `docs/tasks/specs|handoffs|compact-snapshots` and the package → 261 hits in 95 files (positive control: the same
call lists CLAUDE.md 4, critic.md 4). I-2 the package: `builder-rules|critic-diff-brief` → architecture.md 5 lines,
test-layers.json 8 lines, 30+ `.py` comment lines (numbers 1, 5, 7a, 7b, 8, 9), `references/gate-registry.json:188` (found
here, in neither verdict). I-3 `retro/README` over the repo → session-retro SKILL :13, :42; SIBLING_MAP:525. r1's I1-I15 stand.

| Document | Class | Fate |
|---|---|---|
| `docs/tasks/critic-diff-brief.md` | standing brief of the critic | folded → critic.md rules 21-23 (+ rule 24), deleted (§4.1) |
| `plans/builder-rules.md` | standing brief of the builder (W-3) | folded (§4.2), deleted |
| `docs/tasks/pre-release-0.9-brief-common.md`, `pre-release-0.9-critic-brief.md` | dead one-offs | deleted (§4.3) |
| `docs/tasks/test-diet-brief.md`, `test-diet-fold-brief.md` | dead standing specs | deleted (§4.4) |
| `docs/tasks/exchange-form.md` | half a code contract: grammar + flag table + a test fixture + the brief form | folded and deleted, wave 2, N7 (§4.5) |
| `docs/retro/README.md` (A F6, B K2 (3)) | standing procedure outside MAIN | folded into `.claude/skills/session-retro/SKILL.md`, deleted (§4.6; fork F-R2-3) |
| `plans/piles/_template/batch.md:16` (A F6, B M5) | the GENERATOR of brief files («путь к файлу или») | line rewritten (card C1, §4.7) |
| `## Бриф` / «Общий бриф дизайнерам» / «Бриф пачки N» (B K2 (2)) | per-batch text | not extra (§2); renaming is the owner's question F-R2-5 |
| `docs/tasks/specs/reports/t-2046-language-exceptions-census.md` (B m3) | data ledger read by Q12 (c) | not extra (§2); Q12 (c) names it as a ledger |
| `docs/tasks/specs/td-11-lead-brief.md`, `fg-context-and-hygiene-lead-brief.md` (A F6) | intent brief of one task, in specs/ | legal (§2) |
| `plans/RULES-PROPOSAL.md`, `plans/forge-metrics.md`, `plans/project-knowledge-plan.md`, `plans/thinking-roles-portable-to-main.md` (A F6) | records / plans / generated | not extra; not edited |
| `docs/RELATED_WORK.md` (A F6) | record (CLAUDE.md rule 1 trail register) | not extra |
| `docs/TESTING.md` | MAIN (W-2) | stays; gains a section and an axis-31 row (§4.2.1, §7) |

---

## §4 Paragraph-by-paragraph homes

Legend: **present** = already in the named home; **needed** = new text there; **dropped** = reason given.

### §4.1 `docs/tasks/critic-diff-brief.md` → `.claude/agents/critic.md` rules 21-23 (card C3)

Who needs it: only the critic acts on it; the mechanical-layer FACT for dispatcher and builder is CLAUDE.md rule 3
(TWO-LAYER CRITIC ENTRY). The text moves VERBATIM with only the listed edits. Questions are labelled `Q1.`…`Q12.`, indented
three spaces (`tools/test_handoff_rule_anchors.rule_block` splits on `^\d+\. `: a `Q` label is never read as a rule).
Internal "item N" / "question N" → "QN".

- **Rule 21** opens `21. The two layers of a diff gate (CLAUDE.md rule 3, the two-layer review rule):` followed by brief
  :10-22 (the two bullets) verbatim, edits: "the scope: `plans/builder-rules.md` 7b" → "the scope: `docs/TESTING.md` «Что
  запускать по своей правке»"; "(batch level, `plans/builder-rules.md` 7b/7c; D-0033 as refined by the Lead)" → "(batch
  level, `docs/TESTING.md` «Что запускать по своей правке»; D-0033 as refined by D-0057)" (verdict A F1).
- **Rule 22** opens `22. The standing questions — on every diff gate, each with its own verdict line (Q12 also on a plan gate):`
  followed by brief :26-114 (items 1-12) with `N. ` → `QN. `, edits:
  - Q4 (brief :31-38) is REPLACED whole by the one wording of §6 (B M3 (a): the old opener "a sibling neither fixed nor
    queued is a finding" goes), then the line forms verbatim from brief :36-38 ("`<what> | узел: <node id>` … `piles.py
    check` (д) (F6-30).").
  - Q7: "(item 4: no "queue" severity)" → "(Q4: no "queue" severity)".
  - Q11: "question 9 applies to them" → "Q9 applies to them".
  - Q12 (c): after "`docs/tasks/specs/reports/t-2046-language-exceptions-census.md`" insert " (a data ledger, like a ratchet
    file)".
- **Rule 23**:
  `23. What comes back from a diff gate: the verdict line in rule 6's words (ACCEPT / NEEDS WORK / REJECT, a REJECT with its`
  ``failure_class`), each fix with file:line and whether it blocks the merge; the JSON block of rule 17 carries the same``
  `verdict as fit / fit_with_fixes / blocker (blocker when any finding blocks). Then Findings numbered / Seam and class notes`
  `/ Spot-checks (claims verified with their carriers; every negative with its positive control) / Trail (files, line ranges,`
  `commands with verbatim output) — under about 1800 words, trail last. The review is a FILE at the dispatch's `handoff:``
  `path; its form, the closing json block and the fallback with no path are rules 16-17; acceptance runs`
  `` `python tools/critic_verdict_check.py <file>`, exit 0 required.`` (D2: the third verdict vocabulary dies.)
- **Rule 24** (F6 (a), verdict A B7, B B3 (d)): see §4.8.

Edits of existing critic.md rules (same card): rule 5 (:26-32) — "Axes of the defect left uncovered and not queued = a
NEEDS-WORK finding." → "Axes of the defect left unfixed, outside the one exit of rule 22 Q4, = a NEEDS-WORK finding."
(first line unchanged: install_parity anchor); rule 12 (:76-77) "(its size: docs/tasks/critic-diff-brief.md «The two
layers»)" → "(its size: rule 21)"; rule 18 (:161) "the rule text is docs/tasks/critic-diff-brief.md items 6-7" → "the rule
text is rule 22, Q6-Q7"; rule 19 (:164) "the question is docs/tasks/critic-diff-brief.md item 12" → "the question is rule
22, Q12"; rule 20 (:173) "the question is docs/tasks/critic-diff-brief.md question 5" → "the question is rule 22, Q5".

| ¶ (brief) | Verdict |
|---|---|
| title, P1 (:1-6) | present (critic.md rule 18 quotes the 06.10 word; CLAUDE.md rule 3 the clone ratchet) — the B-419 pointer sentence dies with the file |
| two layers (:8-22) | needed → rule 21 |
| Q1-Q12 (:24-114) | needed → rule 22 |
| What comes back (:116-125) | needed → rule 23 (D2) |

**Invariant M1 (B):** critic.md rules 21, 22, 23, 24 are assigned by this spec; no other spec appends a critic rule until
wave 1 is on main (spec 20261116's planned "rule 21" is superseded, §4.8).

### §4.2 `plans/builder-rules.md` — dissolved (W-3)

**Answer to «Там есть что-то что нужно не только билдеру?» — yes:** items 7, 7b, 7c, 7d, 12, 16, 19, 20 (bold rows).

| Item | Needed by | Home |
|---|---|---|
| 1 file ownership | builder + dispatcher | owns rule present (hygiene 4, R11-f); integrator-only list dropped (F7 (a); enforced nowhere — verdict A F10: grep in tools → 0, control `owns_gate.py`); «Needed from integration» → builder.md rule 4; "new config key: read in code with a default" → rule 11; "in the report: name, default, meaning" → rule 4 |
| 2 no git state change; worktree commit | builder | rule 10 |
| 3 language | everyone | present: PROJECT.md «Язык» — dropped |
| 4 style | builder | rule 11 |
| 5 size caps; «Файлы phases/ без потолка … добавлять кратко» (B m1) | builder, designer, critic (Q8) | rule 11 points at `selftest.py --limits` / A22 (numbers live in code) and carries the phases/ clause |
| 6 no bytecode | builder | rule 11 |
| **7** mandatory check | builder, designer, critic, coordinator | TESTING «Что запускать по своей правке» (one bullet); "a size pin is a cap" present (TESTING «Что не пишется» row 3) |
| 7a cost; «лучше запускать его синхронно», «не дольше, чем сам прогон» (A F2, B m1) | builder | rule 9, in the holder's wording (A F3: 16 (б) holds) |
| **7b** builder level and batch level | builder, designer, critic, coordinator, integrator | TESTING «Что запускать по своей правке» (new, verbatim Russian, §4.2.1) |
| **7c** story_run.py DoD files | designer / dispatcher | same section, one row of the per-type list |
| **7d** which tests are written | builder, designer, critic | present: TESTING (three layers, «Что не пишется», «Правила ролей не теряются», «Бюджет»), CLAUDE.md rule 11 DOC-DISPATCH; "no new test file without a keep row" (cut from builder.md rule 4, B m1) present in builder.md rule 8 + TESTING «Бюджет / Файлы» — dropped |
| 8 a person's word passes any block; the note «роль сама waiver не запускает … слово записывает оркестратор» (B m1) | builder, designer, critic | FR-4, FR-57 present; the clause and the note → rule 11 |
| 9 backward compatibility | builder, designer | rule 11 (F9 (a): the Lead offers the package pile a finding proposing it as AR-3's change check — §11 L-a) |
| 10 live project read-only | builder, night agent | rule 11; night agent: RUNBOOK §9.6 «живое дерево проекта не трогается» present (verdict A F10) |
| 11 report content; «текст для SKILL.md — строки < 200 байт» (A F2) | builder | rule 4 (the SKILL clause stays: «Needed from integration» survives F7 — B m1's "obsolete" does not hold) |
| **12** factory rules read whole | builder, critic, designer | present PROJECT.md p. 1; rule 11 one phrase + pointer |
| 13 bounded background wait; «рапорт называет цикл» (A F2, B m1) | builder + coordinator | rule text: RUNBOOK §9.8, owned by t-1122 K-DOC (its §6.1 text carries «Отчёт воркера называет цикл, оставленный позади»); builder.md rule 9 one sentence + pointer (§4.2.3) |
| 14 confession names file:line | builder | rule 4 |
| 15 witness pasted | builder | present: CLAUDE.md rule 2, builder.md rule 4 — dropped |
| **16** (а) trim output incl. «`Grep` вместо чтения файла целиком» (A F2), (б) one witness run, (в) cap | every worker; coordinator | (в) present: CLAUDE.md rule 12 + `agent_budget.stop_message` (:254-262, verdict A K1); (а)(б) → CLAUDE.md rule 12 Cost gates sentence (§4.2.2) |
| 17 AGENTS.md generated | builder, Lead | rule 10 |
| 18 commit from worktree; «обход `git -c core.hooksPath` не нужен» (A F2) | builder | rule 10 |
| **19** `architecture:`/`judgment:` lines | builder, Lead, designer | present CLAUDE.md rule 10; grammar's one carrier `tools/architecture_gate.py`; rule 10 one pointer |
| **20** worktree dispatch and return; «пустой tasks/*.output не значит потерянный отчёт» + `handback_extract.py --agent` (A F2, B m1) | coordinator | RUNBOOK §12 item 2 rewritten (card C1, §4.2.4); item 8 present; R11-h present |
| tail: interfaces fixed / CLI_SCRIPTS / no direct pytest / `judge.provider: none` | builder | "interfaces fixed" dropped (0.7 model gone); "pytest refused by a hook" dropped (the hook's refusal carries the door); CLI_SCRIPTS, `judge.provider: none` → rule 11 |
| header | — | dropped (history) |

#### §4.2.1 New section of `docs/TESTING.md` — «Что запускать по своей правке» (card C1)

Placed after «Строка теста в DoD» and before «Тест может упасть». Text = builder-rules 7b (:38-65) VERBATIM, Russian, edits:
- heading `### Что запускать по своей правке`; first sentence «Слово владельца 21.10.2026 18:3x, D-0056 (замер: у фикс-раундов
  69–85 % стены — ожидание прогонов, правки кода 1–4 %).» (the clause «П. 7 и 7a переписаны под этот пункт (F6-33,
  21.10.2026).» dropped: history);
- «`docs/TESTING.md` «Тест может упасть»» inside the moved text → «раздел «Тест может упасть» ниже» (A F8);
- appended bullet (item 7): «Полный `selftest.py` и `install_smoke.py` на машине не гоняет никто — их судит CI (D-0059,
  `docs/RUNBOOK.md` §7). Красный тест вне своих файлов от чужой недоделки — отметить и не чинить.»;
- appended to the «так же по типу правки» list (item 7c): «`test_story_run_words.py` и `test_driver_layers.py` — правка
  `story_run.py` (Lead, 26.10.2026: `main` красный 16.10 и 21.10, оба раза DoD их не называл)»;
- appended last paragraph (the split, A B7; spec 20261116 §2.7): «`--witness-for` отвечает, ЧТО ЗАПУСТИТЬ по пути пакета;
  `python -B tools/owns_readers.py` — что НЕЛЬЗЯ СЛОМАТЬ или править (читатели, карантин, медленные, наличие); как билдер
  читает его блок — правило 12 `.claude/agents/builder.md`.»
Other TESTING edits (card C1): :65 «`plans/builder-rules.md`, файл роли» → «файл роли»; :88 per F8 (a), BOTH worlds: the
Lead names in C1's dispatch the node that will add the `test:` check; with a node → «Наличие и форму строки проверит код
(узел <id>);»; with none → «Наличие и форму строки код пока не проверяет;» (D7); :89 and :170 «(вопрос 5
`docs/tasks/critic-diff-brief.md`)» → «(вопрос 5, `.claude/agents/critic.md` правило 22)»; :102 → «судит по вопросу 5 (а) и
правилу 21 `.claude/agents/critic.md`; как и чем он это проверяет, написано только там.»; :123 → «- **Что запускать по своей
правке** — раздел «Что запускать по своей правке» выше.»; «Когда тест покраснел» gains item 4: «4. Удаляя тестовый файл,
убери его имя из реестров, которые его называют (`grep` по имени файла: `plans/features.json`, `slow_tests.json`,
`CONTRACT_TESTS`/`TEST_TIMEOUTS` в `selftest.py`, `gate-registry.json`, `stage-joints.json`, `driver-layers.json`,
`.gitlab-ci.yml`, `judgment-census.json`); файл, который называет гейт, не удаляется — только чистится.»; :228 → «- **Билдер**:
пишет по этому документу; что запускает — «Что запускать по своей правке».»; :229 → «- **Критик**: вопрос 5 (`.claude/agents/critic.md`
правило 22) и правило 21 там же.» (A F8). The OWNER_KEYS key `scope:builder` («не регрессия, не соседи, не большие файлы»)
moves with the text.

#### §4.2.2 CLAUDE.md rule 12 · Cost gates — one sentence (16 а-б) (Lead, L-a)

After "`tools/agent_budget.py` caps a worker (WARN 250K, STOP 400K; the remainder goes to a fresh worker whole);" insert:
"a worker trims run output before it enters its context (`-q`, a 30-line tail, `Read` with a limit over 400 lines, `Grep`
instead of reading a whole file) and closes a round with ONE witness run after all edits, never one after each edit
(D-0035);". `cost:cap` key untouched.

#### §4.2.3 `.claude/agents/builder.md` — exact texts (card C3)

Rule 4 (:48-53): replace "Its scope in this repository: `plans/builder-rules.md` 7b (D-0056) — the files
`scenario_walk.py --witness-for <owns>` prints; a quarantined test file is never run or edited, and no new test file is
written without a keep row (7d). CI is neither started nor waited for: `plans/builder-rules.md` 7b." with "Its scope in
this repository: `docs/TESTING.md` «Что запускать по своей правке» (D-0056) — the files `scenario_walk.py --witness-for
<owns>` prints; a quarantined test file is never run or edited; CI is neither started nor waited for." and append to rule
4: "The report's content (its form is rule 7): per item of the plan DONE / PARTIAL / NOT DONE, one line and the files; the
tests added or changed and the exact final lines of the runs; «Needed from integration» (file, exact text, why) for a file
outside your owns — text meant for a `SKILL.md` keeps lines under 200 bytes; every new config key with its name, default
and meaning; the CHANGELOG entry as a fragment file `ai-packages/qa-factory/changelog.d/<pile>-<batch>-<slug>.md` in the
CHANGELOG voice (English; `CHANGELOG.md` itself is never touched); what was decided differently from the plan and why; at
most about 500 words of prose (verbatim run output does not count). A confession of a hygiene deviation names file:line
(critic t-560 had to guess)."

New rule 9: "9. Runs, cheaply. While working, run at most the changed module's test file, and not after every edit; the
witness is ONE run of rule 4's scope on the final state, repeated once only if code changed after it (the owner,
30.09.2026; the output trimming is CLAUDE.md rule 12, Cost gates). Run a test synchronously when you can; a polling wait
lasts no longer than the run itself and names the file it waits for and its end (a count or seconds); an unbounded polling
loop is forbidden, and a loop you leave running is named in your report (the rule: `docs/RUNBOOK.md` §9.8)."

New rule 10: "10. Git. No git state change in a shared tree (`stash`, `add`, `commit`, `checkout`, `reset`, `restore`,
`clean`, `pull`, `push`); `diff`, `log`, `show`, `status` are free; another worker's uncommitted edits are never touched. In
your own worktree you commit your owns only — a plain `git add` / `git commit` from the worktree root (no `git -c
core.hooksPath=…` workaround: `wiring_check.py` accepts the main checkout's `core.hooksPath`), a message with `axes: not a
mechanism (...)`; a package commit also carries the `architecture:` and `judgment:` lines, whose form is
`tools/architecture_gate.py` (CLAUDE.md rule 10). Mechanism paths (`MECHANISM_PREFIXES` of `tools/mechanism_gate.py`) stay
STAGED and are listed in the report: the Lead commits them (CLAUDE.md rule 2). A task that edits `CLAUDE.md`, `PROJECT.md`
or `docs/FACTORY_RULES_INDEX.md` regenerates `AGENTS.md` with `python tools/agents_md.py --repo <worktree root>` and stages
it (no `owns` entry needed). Merges, pushes and branch switches are not yours."

New rule 11: "11. In the package. `ai-packages/qa-factory/design/factory-rules.md` is read whole before the edit and again
before the report (PROJECT.md «Как принимается изменение пакета» p. 1). Comments explain why, usually naming the incident;
tests use `scripts/tests/harness.py` or unittest, after a look at the neighbouring test; stdlib only, no new dependency.
Run with `python -B`; temporary files go to the OS temp, never into the package. Size caps are `selftest.py --limits` and
audit A22 (text added to a role or reference is paid for by removing redundant text); `phases/` files have no cap, but the
orchestrator reads them every run — add tersely. A new config key is read in code with a default; a project onboarded on an
earlier version works without re-onboarding, and a story in flight is never refused because an earlier artifact lacks a
new field. A new refusal names how a person's recorded decision passes it (the orchestrator records the word; a role never
runs the waiver itself — FR-4, FR-57). A live project is read-only: no write and no `cd` there; code runs on a copy in
temp. A new CLI script is registered in `audit_factory.py` `CLI_SCRIPTS`; every code path works with `judge.provider:
none`. "builder-rules N" in package comments = this rule's former numbering: 1, 9 → rule 11; 5 → rule 11; 7a → rule 9;
7b, 7c → `docs/TESTING.md` «Что запускать по своей правке»; 8 → FR-4, FR-57."
(The last sentence is verdict A's recommended wording, extended by the numbers 7b, 7c, 8 that I-2 found in package
comments; it is the ONE sentence K-NOBRIEF allows, §8.)

New rule 12 (spec 20261116 §3.3 builder bullet; its L5 is superseded here, so the duty needs this home — K1): "12. The
readers block. When the dispatch carries the block of `tools/owns_readers.py`, you never write into a file it marks
`quarantined`; a `slow` owned test is named \"judged by the batch canon\" and not run; an `absent` given or owned path is a
question returned before work; for every `names` line you keep that reader green or return \"changes needed outside owns:
<path>\" and stop (a return, not an edit outside owns); a `more` count is not a duty — run `python -B tools/owns_readers.py
--readers` yourself when your change alters a file's interface. What to RUN stays rule 4's scope."

#### §4.2.4 RUNBOOK §12 item 2 (card C1; A F2 item 20)

Replace item 2 (:619-621) with: "2. A hand-back can be LOST from the transcript (the critic t-572's report arrived as a
message, the extractor found nothing), and an empty `tasks/*.output` is not a lost report (79 of 412 were empty; the full
transcripts are in `subagents/agent-<id>.jsonl`): extract with `python tools/handback_extract.py --agent <id> <report
path>`, never retype; a resumed agent's or critic's later reports may be absent from the transcript — transcribe them from
the message into `docs/tasks/handoffs/` at once." (`extract_handback.py` does not exist — verdict A F2.)

### §4.3 The 0.9 briefs — deleted

`pre-release-0.9-brief-common.md`: header/«Superseded by D-0056» dropped; stale paths dropped; "What you return 1-9"
present (designer.md rules 1-7, CLAUDE.md rule 11 / R11-f); "one mutation → one killing test" diverges with the owner's
word 10.11 (D6) — dropped; caps → code; `[meaning]` → PROJECT.md p. 6. `pre-release-0.9-critic-brief.md`: facts by trail
present (CLAUDE.md rule 3, critic.md 11-12); `[meaning]` present (p. 6 (в), designer rule 1); item 3 "challenge the Lead's
fork decisions" **needed** → rule 24 Q13 (e) (§4.8); feasibility present (rule 3); class/seams present (Q3, Q4); mutation
dropped (D6); FR walk present (Q8, Q10-11, p. 1); duplication on a plan → Q6 + rule 24 asks Q4/Q12; return form → rule 23.

### §4.4 The test-diet briefs — deleted

`test-diet-brief.md`: kinds table present (TESTING «Что не пишется», «Правила ролей не теряются», layers 2-3); "empty file →
`git rm` + `plans/features.json`" **needed**, generalised → TESTING «Когда тест покраснел» item 4 (§4.2.1); world once
present; never-do list present (owns, rule 10, «Сессия форджа»); "no weakening an assertion" dropped (the waves are
cancelled, test-diet.md:47-48); commit template dropped (copies the gate grammar). `test-diet-fold-brief.md`: TD-14 closed
(test-diet.md:126) — dropped; the general fold rule present (TESTING «Как писать эффективный тест» 1, 3; Q5 (e));
registries → item 4.

### §4.5 `docs/tasks/exchange-form.md` → N7, wave 2 (A B7, B M7)

| Section | Home |
|---|---|
| intro (:1-5) | dropped (the trio is SIBLING_MAP axis 1 :35) |
| §1 grammar (:7-47) | `.claude/agents/scout.md` rule 10 already carries headers, id, gist, status, ev, Trail columns, op, flags-as-set, result forms, zero/control, `-i`, one table per section. NEEDED, into new rule 11: "`found <n>` with n ≥ 1 and no leading zeros; anything else (`found 0`, `0`, `0 matches`, `count 01`, free text, `count` without the `count` flag) is out of grammar — neither a zero nor a control; before the key, whole-line HTML comments and closed fenced blocks are skipped; after it, comment and fenced lines are blanked; the one unflagged fence is the container around the whole digest" (from :17-21, :38-47) |
| flag table (:49-79) | needed by the scout (FR-38: the check that judges its output states the requirement before the work) and by the Lead reading `first=<flag>` → scout.md rule 11, the table verbatim (fork F-R2-4) |
| example t-794 (:81-130) | a TEST FIXTURE → `tools/fixtures/digest_form/t-794.md` (verbatim, the `### Example` heading line through the closing fence) |
| §2 brief form (:132-156) | a dispatcher duty → CLAUDE.md rule 11 · inline DoD, three sentences (§11 N7-L) |

### §4.6 `docs/retro/README.md` → `.claude/skills/session-retro/SKILL.md` (fork F-R2-3)

The table «Что где лежит» and the section «Недельное сведение» (:7-33) move VERBATIM (Russian) as a new last section
`## Недельное сведение (weekly reduction)` of the skill; the README intro (:3-5) is present in the skill's own opening.
Skill :13 and :42 pointers → "(section «Недельное сведение» below)". SIBLING_MAP:525 → "procedure (the weekly reduction
included)". Lead's part (skills are mechanism paths).

### §4.7 `plans/piles/_template/batch.md:16` (card C1; A F6, B M5)

«Общий бриф дизайнерам: <путь к файлу или 3–5 строк: где что лежит, что вернуть, DoD узла>.» →
«Общий бриф дизайнерам: <путь к спеке или 3–5 строк здесь: где что лежит, что вернуть, DoD узла; отдельного постоянного
файла-брифа нет — PROJECT.md «Лишних документов нет»>.» (The `## Бриф` heading, read by `piles.py:1934`, is not touched.)

### §4.8 The plan gate absorbed (F6 (a); A B7, B B3 (c)(d))

critic.md **rule 24** (card C3):
```
24. The plan gate (critic on a plan or on a dispatch draft; CLAUDE.md rule 3): answer Q13 below and Q4 and Q12 of
   rule 22, each sub-question with its own verdict line.
   Q13. **FACTS AND EDGES** ...
```
Q13 = spec 20261116 lines 420-451 VERBATIM (from "**FACTS AND EDGES** (evidence: t-896" through "miss 7 (common-word stem)
-> nothing owed: it over-counts, never hides"), re-indented by three spaces, edits: "13. " → "Q13. "; "(c) PREMISES:
critic.md rule 12 applies" → "(c) PREMISES: rule 12 applies". Appended sub-question (pre-release critic brief item 3):
"(e) FORKS: for every fork the Lead decided, is the decision consistent with the spec's evidence, the owner's words it
quotes and the AR-n / P-n it names? A decision the evidence contradicts is a finding with the alternative named; the
decision stays the Lead's (rule 6)."

designer.md **rule 3** appended line (spec 20261116 §4.2, re-pointed; L3): "   The readers list is the block of `python -B
tools/owns_readers.py --paths <touched files> --names <changed names>` (counts by default; `--readers` lists): you have no
shell, so the Lead attaches it to the brief and the plan critic re-runs it on your touched-file list; quote the block and
give every line its answer in the forms of `.claude/agents/critic.md` rule 24, Q13 (d). A hand grep is owed only for what
its KNOWN MISSES name."

Supersede line (Lead, L-a, appended to spec 20261116 §6 «Lead edits»): «L1, L2, L4, L5 superseded by t-1117/t-1133
(critic.md rule 24; the POINTERS row to rule 24 Q13; TESTING «Что запускать по своей правке» and builder.md rule 12); L3 lands
as t-1133 card C3's designer.md rule 3 line, re-pointed to critic.md rule 24, Q13 (d); stream L writes no critic.md rule.»
(Wordings of A and B harmonised: both put the designer line in C3.) No pile node carries L1-L5: `t-897|spec-facts-by-code`
over `plans/piles` → only `conductor/batch-4` (:27, :41), status «закрыта» (settles B's first "Not established").

`tools/owns_readers.py:26` "answered in docs/tasks/critic-diff-brief.md item 13 (d)" → "answered in .claude/agents/critic.md
rule 24, Q13 (d)"; `:55` "(spec section 2.7; plans/builder-rules.md 7b)" → "(spec section 2.7; docs/TESTING.md «Что
запускать по своей правке»)" — now pointing at present text (A B7). No test reads that docstring: Grep `KNOWN MISSES|TWO
QUESTIONS|__doc__` in `tools/test_owns_readers.py` → 0, control `owns_readers|import` same file → 19 (B M9).

---

## §5 Divergences (who holds)

| # | A | B | Holds |
|---|---|---|---|
| D1 | DECISIONS.md:32 D-0033 "every builder's witness carries `--check` … (`docs/tasks/critic-diff-brief.md`; …)" | D-0057 (DECISIONS_ARCHIVE:144-145) "a builder's witness no longer carries `--check`"; D-0056 | D-0057. Lead TRIMS D-0033 (the header's one allowed move, DECISIONS.md:9-13): new line = "- D-0033 — The clone ratchet is a merge gate: `tools/dup_ratchet.py --check` against `tools/dup-baseline.json` (only shrinks) runs in `forge-check` on every push and MR; a new clone group or a new copy in one is red with a door (remove the copy, or `--update` on the Lead's word) (the owner, 06.10.2026: «поддерживать порядок» after the 0.8.1 clean-up; B-417, B-309). Detector: the `forge-check` job, `tools/test_dup_ratchet.py`. Full text: `docs/DECISIONS_ARCHIVE.md`." and adds "D-0033 (17.11.2026, t-1133)" to the header's trimmed list. Before trimming, the Lead greps `D-0033` in the archive: if the dropped clause is not there, it appends the full old line there first |
| D2 | brief "accept / accept with fixes / reject" | critic.md rule 6 + rule 17 | rules 6 + 17; rule 23 maps them |
| D3 | designer.md rule 2 "critic brief item 4" | brief deleted | → "`.claude/agents/critic.md` rule 22, Q4" |
| D4 | owns_readers.py:26 "brief item 13 (d)" | Q13 never landed | rule 24 Q13 (d) (§4.8) |
| D5 | critic.md rule 5 "not queued" | W-4 | §6 one wording |
| D6 | pre-release "one mutation → one test" | TESTING:93-94 retired 10.11 | TESTING |
| D7 | TESTING:88 claims a `test:` check in `dispatch_manifest.py` | no such check (both verdicts: grep → 0, control 4/14) | F8 (a), both worlds (§4.2.1) |
| D9 | builder-rules 19 copies the `judgment:` grammar | designer rule 1 | the gate; copy dropped |
| D10 (A F3) | 7a "after an edit run only the changed module's test file" | 16 (б) "re-running after each edit is a violation; ONE run after all edits" | 16 (б) (Lead): rule 9 "at most the changed module's test file, and not after every edit" |
| D11 | t-1122 §6.3 builder.md phrase "the gate refuses an unbounded loop and a stdin read nothing feeds" | the Lead dropped G2 (stdin), and the gate (K-GATE) may land after C3 | rule 9 uses the duty-only sentence true in both worlds (§4.2.3; small choice S4) |

---

## §6 «Fixed in the round; another pile only as a rare case» — ONE wording (A F4, B M3)

The criterion, English (CLAUDE.md rule 9, critic.md rule 5 by pointer, Q4):
> A sibling is fixed in the same round. It leaves the round only when it lies in ANOTHER pile's zone or waits for the
> owner's word (say which), and only as a node with an executor (`узел:`) or a confirmed transfer (`перенос: … | подтвердил:`)
> in the forms of `docs/TEAMWORK.md` § 9 — the rare case, never a way to put off a rule fix while rules are being fixed
> (the owner's word 17.11.2026).

B M3 (c) asked to quote or drop "rules while fixing rules": it is quoted — W-4's full text carries «а не отложить починку
правил когда мы чиним правила» (§0).

| Place | Edit |
|---|---|
| CLAUDE.md rule 9 (L-a) | "fix now, or EXPLICITLY put the remainder in the queue/log;" → "fix now, in the same round; a sibling leaves the round only when it lies in ANOTHER pile's zone or waits for the owner's word (say which), and only as a node with an executor or a confirmed transfer in the forms of `docs/TEAMWORK.md` § 9 — the rare case, never a way to put off a rule fix while rules are being fixed (the owner's word 17.11.2026);" |
| CLAUDE.md rule 9 sweep (L-a) | "(applied / not applicable — why / queued with a pointer)" → "(applied / not applicable — why / moved to another pile's node, with its id)"; "opening a file specially for the sweep is forbidden — queue it instead" → "opening a file specially for the sweep is forbidden — move it to another pile's node instead (the rare case)" |
| PROJECT.md п. 9 (L-a) | «минорные замечания критика не откладываются строкой, а чинятся тут же — фикс-раундом того же узла;» → «минорные замечания критика не откладываются строкой, а чинятся тут же — фикс-раундом того же узла; уйти из раунда может только то, что лежит в зоне ДРУГОЙ кучки или ждёт слова владельца (сказать, чего), и только узлом с исполнителем или подтверждённым переносом в формах `docs/TEAMWORK.md` § 9 — редкий случай, а не способ отложить починку правил, когда мы чиним правила (владелец, 17.11.2026);» (bold opener unchanged, byte-identical with TEAMWORK § 9) |
| critic.md rule 5 (C3) | §4.1 ("outside the one exit of rule 22 Q4") |
| critic.md Q4 (C3) | "Q4. **Class-wide completeness** (rule 9, FR-54): the SIBLING_MAP axes and the neighbours in the same artifact. " + the criterion above + " An analog outside the node's `owns` but inside this pile is named with its file so the Lead widens the fix round or sends a sibling builder. A leaving sibling comes back as a line the Lead writes into «Остатки» as is:" + brief :36-38 verbatim from "`<what> | узел: <node id>`" |

Sweep of the same artifacts (CLAUDE.md rule 9, sweep-the-artifact-first): rule 9 main clause — applied; rule 9 sweep
paragraph (two phrases) — applied; rule 10 (b) "covered / queued / n/a" — not applicable: those are mechanism AXES left for a
later commit, a grammar `tools/mechanism_gate.py` parses, not sibling defects; rule 13 R13-g — n/a (critic passes); critic.md
rules 14 ("siblings outside the diff follow rule 5") — applied through rule 5; rule 19 ("a fix of this round or a proposed
node with its owner") — consistent, unchanged; Q12 (d) — consistent, unchanged; PROJECT.md п. 9 rest («замечания,
относящиеся к другим кучкам … строкой с исполнителем») — consistent, unchanged; designer.md rule 2 ("a finding is offered
only for another pile's zone or an owner's decision") — consistent; its pointer re-pointed (D3). OWNER_KEYS `routing:rule-9`
and the SYSTEM_PROMPT anchor `9. Fix the class, not the instance (fix-the-class-not-the-instance` are untouched.

---

## §7 `docs/TESTING.md` — who must point to it (W-2) and K-TESTPTR

| Role / carrier | Uses it for | Pointer after the change (exact text) |
|---|---|---|
| builder.md rule 4, rule 8 | what to run; writing tests | rule 4 "`docs/TESTING.md` «Что запускать по своей правке»"; rule 8 unchanged |
| critic.md rules 20, 21, 22 Q5 | layer 1, tests | rule 20 "docs/TESTING.md «Бюджет»" (unchanged); rule 21 "`docs/TESTING.md` «Что запускать по своей правке»" |
| designer.md rule 1 | DoD scope, `test:` lines, a new row's place | "`docs/TESTING.md` («Что запускать по своей правке», «Строка теста в DoD», «Бюджет / Файлы»)" (C3: rule 1's "a builder DoD's verification scope in this repository is `plans/builder-rules.md` 7b:" → "a builder DoD's verification scope and its `test:` lines are `docs/TESTING.md` («Что запускать по своей правке», «Строка теста в DoD», «Бюджет / Файлы»):") |
| CLAUDE.md rule 4, rule 11, Contents | witness scope; which tests | rule 4 "`docs/TESTING.md` «Что запускать по своей правке»"; Contents row "| What a builder may run | docs/TESTING.md § Что запускать по своей правке |" |
| PROJECT.md p. 2, п. 13, map | dispatcher | p. 2 / п. 13 "`docs/TESTING.md` «Что запускать по своей правке»"; map row (§8) |
| scout | — | none (writes no tests; E9) |
| dispatch tools | `test:` line | none now (D7) |

K-TESTPTR = POINTERS rows (C2): ("`.claude/agents/builder.md`", "`docs/TESTING.md` «Что запускать по своей правке»", TESTING,
"### Что запускать по своей правке"); ("`.claude/agents/critic.md`", "docs/TESTING.md «Бюджет»", TESTING, "### Бюджет");
("`.claude/agents/designer.md`", "`docs/TESTING.md` («Что запускать по своей правке», «Строка теста в DoD»", TESTING, "### Строка
теста в DoD"); ("CLAUDE.md", "`docs/TESTING.md` «Что запускать по своей правке»", TESTING, "### Что запускать по своей правке").
Error direction: a renamed TESTING heading turns the row red (safe).

---

## §8 The rule «we do not create extra documents»

**Home** (F2 (a)): PROJECT.md «Где что лежит», a paragraph right after the table; in the same edit the row
`plans/builder-rules.md` leaves the table and a row `docs/TESTING.md` joins it (A F5): «| `docs/TESTING.md` | какие тесты
пишутся и что билдер запускает по своей правке — основной документ билдера, дизайнера и критика |».

**Exact text** (Russian; A F5, B M4 applied: one register, «вне основных», an open not-extra class):
> **Лишних документов нет** (владелец, 17.11.2026: «избавится от всех брифов и закрепить что мы не создаём лишние
> документы»). Правило для роли живёт только в основном документе; реестр основных — строки `owner` и `procedure` таблицы
> оси 31 `docs/SIBLING_MAP.md`. Документа вне основных, который роль обязана читать (брифа), нет: нужное — разделом основного
> документа, лишнее не пишется. Не лишнее — то, у чего одна задача или один момент, и запись: спека (и бриф дизайнеру файлом
> в `docs/tasks/specs/`), пачка с её разделом «Бриф», карточка, находка, ревью, отчёт, снимок, очередь, план одной задачи,
> тетрадь эксперимента, запись ретро, журнал, реестр, архив, фикстура. Новый основной документ — словом владельца и строкой
> оси 31 (коммит Lead). Проверка: `tools/tests/test_role_carriers_one_owner.py`; остальное — калибровочная проверка 33 (i).

**Four questions (CLAUDE.md rule 10).**
- (a) Cost: role files grow (critic ~+12 KB, builder ~+5 KB, designer ~+0.8 KB; scout ~+3.5 KB in wave 2), paid at every
  spawn of that role; a builder on a forge-only task now carries package lines it did not get before; dispatchers stop naming
  brief paths in `given`; boot +~2.0 KB wave 1 (§9). Paid by every worker spawn and the Lead once now.
- (b) Axes: §1 list; the full enumeration is the Lead's commit block.
- (c) Detector: K-NOBRIEF + K-REG (deterministic, CI `forge-check.yml:96`) and calibration check 33 (i) (text in §11 L-a).
- (d) What stops a skip: the pin on the CI path (a resurrected brief or a pointer by path or by stem is red on the pushed
  range); the register edit is a mechanism path (Lead, `tier:`); critic Q11 "does it add text a role must read"; the
  semantic case the pin cannot see — on discipline, detector check 33 (i).

**K-NOBRIEF / K-REG design** (new functions inside `tools/tests/test_role_carriers_one_owner.py`; parameterised):
- `main_documents(root)`: reads the axis-31 table of `docs/SIBLING_MAP.md` through `tools/md_table.py` (the one table
  reader, as `digest_form` and `piles` use it); a row counts when its «Owner / pointer» cell starts with `owner` or
  `procedure` (case-folded) and its «File» cell holds a backticked path ending in `.md` (text after the closing backtick,
  e.g. ` §7`, is ignored; a `*` is expanded with `pathlib` glob under the root). Positive control
  (`test_register_sees_the_main_documents`): the result is non-empty and holds `CLAUDE.md`, `docs/TESTING.md`,
  `.claude/agents/critic.md`, `ai-packages/qa-factory/design/architecture.md` (a broken parse fails, never passes).
- `DELETED` = rows `(path, stem)`: the six of wave 1 with stems `critic-diff-brief`, `builder-rules`,
  `pre-release-0.9-brief-common`, `pre-release-0.9-critic-brief`, `test-diet-brief`, `test-diet-fold-brief`;
  `("docs/retro/README.md", None)` (no stem: "README" is a common word); wave 2 adds `("docs/tasks/exchange-form.md",
  "exchange-form")`.
- `ALLOWED` = `{".claude/agents/builder.md": '"builder-rules N" in package comments = this rule\'s former numbering'}`: in
  that file only, the ONE sentence that starts with this text (whitespace squashed, through its final period) is removed
  before the scan.
- `forbidden_hits(text)`: case-folded, `\` → `/`; hits = the path regex `docs/tasks/[^/\s`'"]*brief[^/\s`'"]*\.md`, every
  DELETED path, every DELETED stem as a substring.
- Tests: (1) `test_no_main_document_names_a_deleted_file` (param over MAIN; message names file:line and the door "fold the
  text into a main document, or move the file under docs/tasks/specs/"); (2) `test_deleted_files_stay_untracked` (param
  over DELETED, `git ls-files`); (3) `test_no_brief_file_at_the_top_of_docs_tasks` (no tracked `docs/tasks/<name>.md`, top
  level only, with `brief` in the name); (4) `test_forbidden_hits` — ONE table, the adversarial rows below.
- Error direction: false RED is the allowed side.
- Adversarial rows (input → expected): `docs\tasks\Critic-Diff-Brief.md` → hit; `builder-rules 7b` → hit (B6 false-green
  class); `(builder-rules п. 13)` → hit; `critic-diff-brief question 9` → hit; `docs/tasks/specs/td-11-lead-brief.md` → none;
  `INTENT BRIEF` → none; `"notes":"brief: what was delegated"` → none; a fenced block holding `plans/builder-rules.md` → hit
  (fences are not exempt); builder.md's ALLOWED sentence → none, the same stem in any other sentence of builder.md → hit;
  `docs/retro/inbox/x.md` → none; `docs/retro/README.md` → hit.

---

## §9 Budgets (A F9, B M2)

| Measure | Before (carrier) | After (estimate, wave 1 / +N7) | Ceiling (carrier) |
|---|---|---|---|
| Boot total | 109 921 (`python -B tools/session_context.py`, BOOT BUDGET line, verdict A rerun) | ~111 900 / ~112 350 | WARN 110 000 crossed by ~2 K (accepted, F3 (a)); BREACH 120 000 not crossed (`tools/session_context.py` :208-209) |
| CLAUDE.md own bytes | 50 808 (`wc -c`, both verdicts) | ~51 500 / ~51 950 (rule 9 ~+300, Cost gates ~+220, rule 4 +49, rule 3/Contents ~+30; N7 rule 11 ~+450) | CLAUDE_WARN 58 500 compares OWN bytes (`session_context.py:1312-1321`) — not crossed |
| CLAUDE.md incl. imports | 98 899 (BOOT BUDGET line) | ~100 900 / ~101 350 | — (part of the boot total) |
| PROJECT.md | 34 622 (`wc -c`) | ~35 950 (§8 ~+1 150, п. 9 ~+420, map row −129 +~170) | — |
| critic.md | 10 981 | ~23 000 | none guards `.claude/agents/*.md` (both verdicts) |
| builder.md | 6 239 | ~11 500 | none |
| designer.md | 7 495 | ~8 300 | none |
| scout.md | not measured | +~3 500 (wave 2) | none |
| docs/TESTING.md | 32 159 | ~36 500 | none |

Measured deltas of r1's texts (verdict A, UTF-8): §8 +1 029, п. 9 +361, map row −129, rule 9 +236, Cost gates +180, rule
4 +49; r2's texts are longer (estimates above). The L-a and L-b witnesses carry the BOOT BUDGET line verbatim; the card
witnesses carry `wc -c` of their owns. No raise needed.

---

## §10 Readers of every touched or deleted file (rule 7)

Commands: I-1 (261 hits / 95 files) and I-2 of §3; Grep `SIBLING_MAP` in `tools/*.py` → 37 hits / 22 files; `exchange-form`
in `tools/` → 7 lines in 5 files; `retro/README` repo-wide → 3 live lines; `t-897|spec-facts-by-code` in `plans/piles` → 2
(closed batch). `.githooks/`: 0 for the six names (same call as I-1, which lists other hits: positive control of the same
shape).

| Reader | Points at | Change (card) |
|---|---|---|
| CLAUDE.md Contents ×2, rule 3, rule 4, rule 9, rule 12 | 7b; brief | §7, §6, §4.2.2; rule 3 "the rule text is `.claude/agents/critic.md` rule 22, Q6-Q7 (its rule 18 points there)" (L-a); Contents "| Critic review content | .claude/agents/critic.md § 21-24 |" |
| CLAUDE.md rule 10 package paragraph | "critic's standing questions 10 and 11" | unchanged — stays true (Q10/Q11); checked in the same merge (axis 1 tie) |
| CLAUDE.md rule 11 (wave 2) | — | N7-L brief-form sentences |
| PROJECT.md map row, p. 1, p. 2 (×2), п. 9, п. 13 | builder-rules; brief | p. 1 «целиком и `plans/builder-rules.md`:» → «целиком (правила билдера — его файл роли):»; p. 2 «текст правила `plans/builder-rules.md` п. 7b (D-0056)» → «`docs/TESTING.md` «Что запускать по своей правке» (D-0056)», «`docs/tasks/critic-diff-brief.md` («The two layers»)» → «`.claude/agents/critic.md` rule 21», «содержание — builder-rules п. 11» → «содержание — его правило 4»; п. 13 → TESTING section; п. 9 §6; map §8 (L-a) |
| AGENTS.md | copy of CLAUDE.md/PROJECT.md | regenerated `python tools/agents_md.py --repo <root>` in L-a and N7-L; `agents_md.py --check` in pre-commit refuses a stale copy |
| critic.md :77, :161, :164, :173; builder.md :49, :53; designer.md :20, :42 | brief / 7b | C3 |
| scout.md rule 10 | exchange-form | N7-L (wave 2) |
| docs/TESTING.md :65, :88, :89, :102, :123, :170, :228, :229 | | C1 (§4.2.1) |
| docs/RUNBOOK.md :125, :218, :380 | 7b | → «`docs/TESTING.md` «Что запускать по своей правке»» (C1) |
| docs/RUNBOOK.md :399 (§9.8) | builder-rules п. 13 | NOT this spec: t-1122 card K-DOC replaces §9.8 whole (its §6.1 text names no builder-rules) — precondition P1 (§11), fork F-R2-2 |
| docs/RUNBOOK.md :617 | builder-rules п. 18 | → «`.claude/agents/builder.md` rule 10» (C1) |
| docs/RUNBOOK.md :619-621 item 2; :630 item 8 | extract_handback (absent tool); "plans/builder-rules.md item 20" | item 2 §4.2.4; item 8 "(F6-35; plans/builder-rules.md item 20)" → "(F6-35)" (C1) |
| docs/CLAUDE_HOST_ADAPTATIONS_FULL.md :7, :33 | brief | the token "`docs/tasks/critic-diff-brief.md`" → "`.claude/agents/critic.md` rule 22" (C1; carve-out §2) |
| docs/tasks/test-diet.md :17, :35, :88 | test-diet briefs, critic brief | after each, «(удалён 17.11.2026; правило — `docs/TESTING.md`)» (C1) |
| plans/piles/_template/batch.md:16 | brief file | §4.7 (C1) |
| experiments/measurers/prepare_copy.py:195 (A F7, B m4) | "(builder-rules 10)" | → "(`.claude/agents/builder.md` rule 11)" (C1) |
| docs/SIBLING_MAP.md :34, :95, :401, :478-479, :484-493, :496, :505, :507-509 rows, :525, :564, :577, :602; wave 2 :35, :343, :487, :506 | | L-a (grep BY NAME, not by line — A F7): axis-31 owner sentence: builder-rules 7b → `docs/TESTING.md` «Что запускать по своей правке», the brief → `.claude/agents/critic.md` rules 21-24; rows builder-rules / brief / two 0.9 briefs removed; rows TESTING and `ai-packages/qa-factory/design/*.md` added (§2); :484-486, :491-493, :496, :505 pointers re-pointed; :34 → TESTING section; :95 row "Builder rules" → "| Builder rules | .claude/agents/builder.md; docs/TESTING.md «Что запускать по своей правке» |"; :401 → "`.claude/agents/critic.md` rule 22 Q9"; :525 §4.6; :564 "the pointer form of the brief and builder-rules 11" → "the rule 23 block of critic.md"; :577 → "`.claude/agents/critic.md` rule 22 Q11 (JUDGMENT)"; :602 → "`.claude/agents/critic.md` rule 19 -> rule 22 Q12". Map readers in tools: `test_quarantine.py` (FORGE_CARRIERS, test names — new rows name no test file: unchanged), `test_role_carriers_one_owner.py` (K-REG reads the axis-31 table: C2), `mechanism_gate.py` (prefix: unchanged); the other 19 files mention the name in docstrings (estimate, by count) |
| PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md :392; check 33 | 7b | :392 → "(`docs/TESTING.md` «Что запускать по своей правке»)"; check 33 gains (i) after (h) (:1045) (L-a). Check 34 (brief form metric) names no path: unchanged |
| DECISIONS.md :32 | brief | D1 trim (L-a) |
| .claude/skills/session-retro/SKILL.md :13, :42 | docs/retro/README.md | §4.6 (L-a) |
| spec 20261116 §6 | L1-L5 | supersede line (L-a) |
| ai-packages/qa-factory/design/architecture.md :64, :122, :144, :222, :223 | | PKG (§1) |
| ai-packages/qa-factory/scripts/tests/test-layers.json rows | | PKG: `test_arch_check.py` layer `gate_named` → `data_join`, why "data join: the rows of references/detectors.json (keys sleep, locator) reach arch_check.check_files — shipped rows, missing keys, a broken file, custom rows (test_arch_check.py:163-188); its former forge carrier plans/builder-rules.md item 14 was dissolved (t-1133)"; `test_probe_by_code_copy.py` why → "named by docs/TESTING.md «Что запускать по своей правке» (a history or example line of the forge, read by tools/test_quarantine.py enter); not a DoD row"; `test_audit_rules.py` "builder-rules 7b DoD row" → "docs/TESTING.md «Что запускать по своей правке» DoD row"; `test_console_encoding.py` same; `test_driver_layers.py` "builder-rules 7c DoD row" → same; `test_story_run_words.py` same; `test_story_step.py` why "also named by docs/TESTING.md", `named_by` "plans/builder-rules.md:26" → "docs/TESTING.md «Что запускать по своей правке»" |
| package `.py` comments (~36 files), `references/gate-registry.json:188` | "builder-rules N" | unchanged (history, Lead decision); builder.md rule 11 mapping sentence |
| tools/tests/test_role_carriers_one_owner.py (17 lines) | BRIEF, RULES | C2 (§11) |
| tools/test_handoff_rule_anchors.py :5, :9, :28, :38-39, :104-116, :169-172; wave 2 :151 | BRIEF, RULES; K_SCOUT_FORM | C2; N7 |
| tools/install_parity_anchors.json:22 | CLAUDE.md anchor "`docs/tasks/critic-diff-brief.md` items 6-7" | → "`.claude/agents/critic.md` rule 22, Q6-Q7" (C2); reader `install_parity.py` unchanged; no `toolkit/` tree (A F10) |
| tools/test_quarantine.py:51 FORGE_CARRIERS | builder-rules | → `"docs/TESTING.md"` (C2, staged: mechanism path :271); E4 |
| tools/test_test_quarantine.py :389, :413, :841, :1489, :1613 | builder-rules as a fixture carrier | same rows with `docs/TESTING.md` (C2) |
| tools/test_split.py:1843 | printed `git grep` | → `docs/TESTING.md` (C2; no other carrier of the line — A F10) |
| tools/owns_readers.py :26, :55 | | §4.8 (C2) |
| tools/dispatch_gate.py:1870 | builder-rules item 20 | comment → "(P31; RUNBOOK §12 item 8)" (C2, staged: mechanism path :236) |
| tools/test_language_sites.py:4 | builder-rules 7b | → TESTING section (C2) |
| tools/test_dispatch_manifest.py:844; fixtures K3, K4, K7 | builder-rules inside frozen historical prompts | unchanged: parsed DATA of a fixture; outside MAIN |
| tools/digest_form.py :13, :39; tools/handback_extract.py:37; tools/test_digest_form.py :5, :26, :69, :118, :671; gateway/PI_HARNESS.md:58 | exchange-form | N7 (wave 2) |
| told-before-work/batch-1 :41 TBW1-14; forge/batch-7 :76 FG7-51; live-run-fvf/batch-2 :41 FV2-14 + card README :93; onboarding-hooks/batch-9 :25 OH9-1, :31 OH9-7; package-ci/batch-4 :27 PC4-6; release-next/batch-2 :12 (A B5, B K3) | brief / builder-rules as a file to write or read | L-a, per row, BOTH worlds: the Lead reads the batch header `статус:`; untaken → edits the cell (brief → `.claude/agents/critic.md` (rule 22 Q9/Q11 for OH9); builder-rules → `docs/TESTING.md` «Что запускать по своей правке» (PC4-6's note lands there); release-next :12 → «`docs/TESTING.md` «Что запускать по своей правке», `.claude/agents/builder.md`»); taken → the cell is frozen, the Lead adds a «Ход» line naming the new target (TEAMWORK § 2) |
| plans/piles cards, findings, closed batches; docs/tasks/specs/*; handoffs; reviews; snapshots; PROJECT_FULL; DECISIONS_ARCHIVE; FINDINGS.md; ADOPTION_LEDGER.md; factory-fixes.md; BACKLOG.md; plans/feature-fragility-2026-10-02.md:482 (A F7) | any | not edited (records; outside MAIN) |
| `.claude/worktrees/agent-ac59fdf8d182e6ef9` (B m5) | stale uncommitted role-file edits | the Lead removes it at the wave cleanup |

---

## §11 Order, cards and the Lead's part (K9: A B1, B2; B B1, B2, B3)

**Batch branch.** The Lead names `pile/<slug>/batch-<N>` (placement in a pile is the Lead's), cuts it from pushed
`origin/main`, pushes it. Nothing of this spec is wave-merged into main except the converged batch branch (C1, C3, PKG are
never merged alone — B B2: C1 alone would turn main red).

**Preconditions.** P1: t-1122 K-DOC is on main (RUNBOOK §9.8 no longer names builder-rules) before the wave-1 merge
(fork F-R2-2). P2: the supersede line is in spec 20261116 (L-a). P3 (B B3 (a)): before `wave.py merge` of wave 1, the
open-dispatch scan shows no open critic, designer or main-checkout builder dispatch whose text cites a deleted path; one that
is open → the merge waits, or that work is re-issued with the new pointers.

**Order (wave 1):** C1 ∥ C3 ∥ PKG ∥ L-a draft → **L-a commit** on the batch branch (C1 and PKG branches merged in; C3's staged
role files read and committed by the Lead with the L-a text; `tier: opus`, axis block, `Deviation: exam not run; debt
F3-1`) → push → **C2** in a worktree the coordinator cuts from the pushed batch branch (`git -C <repo> worktree add <path>
-b <branch> pile/<slug>/batch-<N>`, dispatched WITHOUT isolation, RUNBOOK §12 item 8) → **L-b**: the Lead reads and commits
C2's staged mechanism files; one critic of code on the topic (R13-g); `wave.py merge` (P1, P3). **Wave 2:** after wave 1
is on main: **N7-L** commit on a wave-2 branch → **N7** builder from it → Lead commit, critic, merge.

### C1 — docs (builder)

given: this spec §2, §4.2.1, §4.2.4, §4.4, §4.7, §10; `C:/QAFactory/forge-repo/plans/builder-rules.md`;
`C:/QAFactory/forge-repo/docs/TESTING.md`; `C:/QAFactory/forge-repo/docs/RUNBOOK.md`;
`C:/QAFactory/forge-repo/docs/CLAUDE_HOST_ADAPTATIONS_FULL.md`; `C:/QAFactory/forge-repo/docs/tasks/test-diet.md`;
`C:/QAFactory/forge-repo/plans/piles/_template/batch.md`; `C:/QAFactory/forge-repo/experiments/measurers/prepare_copy.py`;
the node id for TESTING:88 (the Lead fills it in the dispatch, or writes "none")
owns:
C:/QAFactory/forge-repo/docs/TESTING.md
C:/QAFactory/forge-repo/docs/RUNBOOK.md
C:/QAFactory/forge-repo/docs/CLAUDE_HOST_ADAPTATIONS_FULL.md
C:/QAFactory/forge-repo/docs/tasks/test-diet.md
C:/QAFactory/forge-repo/plans/piles/_template/batch.md
C:/QAFactory/forge-repo/experiments/measurers/prepare_copy.py
non-goals: deleting any file; RUNBOOK §9.8 (t-1122 K-DOC owns it); role files; CLAUDE.md, PROJECT.md, SIBLING_MAP, PROCESS; any `tools/` file; rewording 7b beyond §4.2.1's edits
handoff: C:/QAFactory/forge-repo/docs/tasks/handoffs/t-<id>-c1-testing-runbook.md
edges: E2, E6, E13; TESTING:88 both worlds (§4.2.1)
DoD: `python -B <scratch>/c1_keys.py` — DOC-DISPATCH witness (keys verbatim from this DoD, full source in the report, never committed, one negative control): present in TESTING.md `### Что запускать по своей правке`, `не регрессия, не соседи, не большие файлы`, `test_story_run_words.py`, `Удаляя тестовый файл`, `правилу 21 `.claude/agents/critic.md``, `(вопрос 5, `.claude/agents/critic.md` правило 22)`, `` `python -B tools/owns_readers.py` — что НЕЛЬЗЯ СЛОМАТЬ ``, `раздел «Тест может упасть» ниже`; present in RUNBOOK.md `handback_extract.py --agent <id>`, `` `.claude/agents/builder.md` rule 10 ``; present in batch.md `отдельного постоянного файла-брифа нет`; ABSENT from all owns `critic-diff-brief`, `test-diet-brief`, `test-diet-fold-brief`, `extract_handback.py`, and `builder-rules` except RUNBOOK §9.8's one line (owned by K-DOC; the script counts that exact line and the three test-diet.md deletion notes); test: none -- поведения нет | expected from: §4.2.1, §4.2.4, §10
siblings: axis 31 (owner moves); axis 1 row :34

### C3 — role files (builder; mechanism paths: STAGED, the Lead commits)

given: this spec §4.1, §4.2.3, §4.8, §6, §7; `C:/QAFactory/forge-repo/docs/tasks/critic-diff-brief.md`;
`C:/QAFactory/forge-repo/plans/builder-rules.md`; `C:/QAFactory/forge-repo/docs/tasks/specs/20261116-spec-facts-by-code-spec.md`
lines 418-482; `C:/QAFactory/forge-repo/.claude/agents/critic.md`; `C:/QAFactory/forge-repo/.claude/agents/builder.md`;
`C:/QAFactory/forge-repo/.claude/agents/designer.md` (A F11, B B3 (d))
owns:
C:/QAFactory/forge-repo/.claude/agents/critic.md
C:/QAFactory/forge-repo/.claude/agents/builder.md
C:/QAFactory/forge-repo/.claude/agents/designer.md
non-goals: renumbering any existing rule; changing install_parity anchor lines (rule openers 1-17 of critic, 1-7 of builder, designer's opener lines); scout.md (N7); committing (mechanism paths stay staged)
handoff: C:/QAFactory/forge-repo/docs/tasks/handoffs/t-<id>-c3-role-files.md
edges: E6, E7, E10, E12, E15
DoD: `python -B <scratch>/c3_keys.py` (DOC-DISPATCH as C1) — present: critic.md `21. The two layers of a diff gate`, `22. The standing questions`, `23. What comes back from a diff gate`, `24. The plan gate`, `Q6. **DUPLICATION AND CONSISTENCY**`, `Q7. **CODE QUALITY**`, `Q12. **ONE ROAD**`, `Q13. **FACTS AND EDGES**`, `(e) FORKS:`, `functions over roughly 60 lines or with more than three nesting levels in the NEW code`, `a line for the coordinator to tell someone is itself a finding`, `never a way to put off a rule fix while rules are being fixed`, `critic_verdict_check.py`, `rules 16-17`, `(a data ledger, like a ratchet file)`; builder.md `9. Runs, cheaply.`, `10. Git.`, `11. In the package.`, `12. The readers block.`, `«Что запускать по своей правке»`, `this rule's former numbering`; designer.md `«Строка теста в DoD»`, `critic.md` rule 22, Q4`, `rule 24, Q13 (d)`; ABSENT from all three `critic-diff-brief`, and `builder-rules` except builder.md's one mapping sentence; and `( cd <C3 worktree root> && python -m pytest tools/test_handoff_rule_anchors.py -q )` ALL green (A B2: run from the worktree root; at C3 time the brief and builder-rules still exist, so every row passes); test: none -- текст ролей; поведение проверяет C2 | expected from: §4.1, §4.2.3, §4.8
siblings: axis 31, axis 2 (exam deviation, Lead's commit), axis 34 row :602

### PKG — package carriers (builder; commits itself: no mechanism path)

given: this spec §1, §10 (package rows); `C:/QAFactory/forge-repo/ai-packages/qa-factory/design/architecture.md` :60-66,
:118-124, :138-152, :212-225; `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test-layers.json`;
`C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_arch_check.py`; `ai-packages/qa-factory/design/factory-rules.md`
(whole); `C:/QAFactory/forge-repo/docs/tasks/specs/td-15-scenarios-quarantine.md` :303-322 (layer criteria)
owns:
C:/QAFactory/forge-repo/ai-packages/qa-factory/design/architecture.md
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test-layers.json
non-goals: package `.py` comments and `references/gate-registry.json` (history); any other keep row; quarantine entries (`test_quarantine.py enter` needs a CI pipeline — not a builder's)
handoff: C:/QAFactory/forge-repo/docs/tasks/handoffs/t-<id>-pkg-carriers.md
edges: E4, E14
DoD: `( cd <PKG worktree root> && python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/design/architecture.md ai-packages/qa-factory/scripts/tests/test-layers.json )` and every file it prints, run; `( cd <PKG worktree root>/ai-packages/qa-factory && python -B scripts/selftest.py --lang )`; `( cd <PKG worktree root> && python -B tools/architecture_index.py --check )` exit 0; the report lists every keep row changed (key, old → new layer/why) — AR-20's change check; the commit carries the two lines of §1 (the gate checks them); test: none -- данные и указатели; слой строки судит критик (Q5 (g)) | expected from: §1, §10
siblings: axis 18 (no ratchet row raised), axis 1 (AR-29 carrier ↔ critic Q11)

### C2 — tools, tests and the deletions (builder; after the L-a commit)

given: this spec §1, §7, §8, §10, §12; the worktree cut from the pushed batch branch (it holds C1, C3, PKG, L-a);
`tools/tests/test_role_carriers_one_owner.py`; `tools/test_handoff_rule_anchors.py`; `tools/install_parity_anchors.json`;
`tools/test_quarantine.py` :45-60, :1337-1346; `tools/test_test_quarantine.py`; `tools/test_split.py` :1835-1845;
`tools/owns_readers.py` :20-60; `tools/dispatch_gate.py` :1866-1871; `tools/test_language_sites.py` :1-10; `tools/md_table.py`;
`ai-packages/qa-factory/scripts/selftest.py` :721-736 (read only)
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
C:/QAFactory/forge-repo/docs/tasks/critic-diff-brief.md
C:/QAFactory/forge-repo/plans/builder-rules.md
C:/QAFactory/forge-repo/docs/tasks/pre-release-0.9-brief-common.md
C:/QAFactory/forge-repo/docs/tasks/pre-release-0.9-critic-brief.md
C:/QAFactory/forge-repo/docs/tasks/test-diet-brief.md
C:/QAFactory/forge-repo/docs/tasks/test-diet-fold-brief.md
C:/QAFactory/forge-repo/docs/retro/README.md
non-goals: any new test file; the package; test_dispatch_manifest.py and its fixtures; behaviour of test_quarantine beyond the one constant; committing `test_quarantine.py` / `dispatch_gate.py` (mechanism paths: staged)
handoff: C:/QAFactory/forge-repo/docs/tasks/handoffs/t-<id>-c2-pins.md
edges: E1, E3, E4, E8, E10, E11
DoD: `( cd <C2 worktree root> && python -m pytest tools/tests/test_role_carriers_one_owner.py tools/test_handoff_rule_anchors.py tools/test_install_parity.py tools/test_test_quarantine.py tools/test_owns_readers.py tools/test_language_sites.py -q )` all green, plus the E4 comparison (script in full in the report): `selftest.gate_named_files(extra_texts=<old forge texts with the base blob of plans/builder-rules.md>)` ⊆ `gate_named_files(<new forge texts with docs/TESTING.md>)` ∪ {`test_arch_check.py`}, and `test_arch_check.py`'s keep row reads layer `data_join`; every name only in the new set listed; test: tools/tests/test_role_carriers_one_owner.py::test_forbidden_hits rows, ::test_pointer_resolves K-TESTPTR rows | expected from: §7, §8
siblings: axis 31 (pins), axis 18 n/a (no ratchet row moves)

Exact C2 transformations:
- `git rm` of the seven owned documents (the six briefs + `docs/retro/README.md`); none is a mechanism path
  (`tools/mechanism_gate.py:215-279`), so C2 commits them with its non-mechanism files (A B1).
- `test_role_carriers_one_owner.py`: constants `BRIEF`, `RULES`, `RULES_7B` → `CRITIC = ".claude/agents/critic.md"`,
  `TESTING = "docs/TESTING.md"`, `TESTING_RUN = "### Что запускать по своей правке"`. OWNER_KEYS: `scope:builder` owner TESTING;
  `scope:tests` owner TESTING, key «Покраснел пин из таблицы выше — удаляется, не чинится»; `review:critic`,
  `review:one-road` owner CRITIC. POINTERS: rows with carrier RULES or BRIEF removed (:61, :62, :71, :90's carrier, :92,
  :96-98); :59 → ("PROJECT.md", "`docs/TESTING.md` «Что запускать по своей правке»", TESTING, TESTING_RUN); :60 → ("PROJECT.md",
  "`.claude/agents/critic.md` rule 21", CRITIC, "21. The two layers of a diff gate"); :63 → builder K-TESTPTR row; :66 →
  (CRITIC, "the rule text is rule 22, Q6-Q7", CRITIC, "Q6. **DUPLICATION AND CONSISTENCY**"); :67 → (CRITIC, "(its size: rule
  21)", CRITIC, "21. The two layers of a diff gate"); :68 → (CRITIC, "the question is rule 22, Q12", CRITIC, "Q12. **ONE
  ROAD**"); :70 → designer K-TESTPTR row; :72 → ("CLAUDE.md", "`.claude/agents/critic.md` rule 22, Q6-Q7", CRITIC, "Q7. **CODE
  QUALITY**"); :73 → ("docs/CLAUDE_HOST_ADAPTATIONS_FULL.md", "the rule text is `.claude/agents/critic.md` rule 22", CRITIC, "Q6.
  **DUPLICATION AND CONSISTENCY**"); :76 → ("docs/RUNBOOK.md", "`docs/TESTING.md` «Что запускать по своей правке»", TESTING,
  TESTING_RUN); :78 → ("docs/TESTING.md", "правилу 21 `.claude/agents/critic.md`", CRITIC, "21. The two layers of a diff
  gate"); :90 → ("docs/TESTING.md", "`docs/RUNBOOK.md` §7", "docs/RUNBOOK.md", RUNBOOK_7); :91 removed (self-reference);
  :114 → ("CLAUDE.md", "| What a builder may run | docs/TESTING.md § Что запускать по своей правке |", TESTING, TESTING_RUN);
  :119 → ("CLAUDE.md", "| Critic review content | .claude/agents/critic.md § 21-24 |", CRITIC, "21. The two layers of a diff
  gate"); new: the four K-TESTPTR rows of §7; (".claude/agents/designer.md", "`.claude/agents/critic.md` rule 24, Q13 (d)",
  CRITIC, "Q13. **FACTS AND EDGES**"). K-NOBRIEF / K-REG functions (§8). `test_negative_control_real_key_in_a_copy` DELETED
  (owner and copy become one file; TESTING «Что не пишется», negative control inside a test) — "behaviour still checked by
  test_one_owner_per_key and test_negative_control_restatement_is_named". Docstring EXCLUDED list unchanged.
- `test_handoff_rule_anchors.py`: `BRIEF`, `RULES`, `K3`, `K_BRIEF` removed; `test_brief_what_comes_back` →
  `test_critic_rule_23_what_comes_back`: `block = rule_block(read(CRITIC), 23)`; `missing_keys(block, ["`handoff:`", "rules
  16-17", "critic_verdict_check.py"]) == []` and `restated(block) == []`; `test_builder_rules_p11` DELETED (carrier gone;
  builder.md rule 7 checked by `test_role_rule_carries_file_rule`); `test_negative_control_restatement_in_a_pointer_copy`
  DELETED (TESTING «Что не пишется») — "behaviour still checked by test_critic_rule_23_what_comes_back"; docstring :5, :9
  updated.
- the remaining files: the one-line edits of §10.

### L-a — the Lead (mechanism commit on the batch branch; `tier: opus`; axis block; `Deviation: exam not run; debt F3-1`)

CLAUDE.md rules 3, 4, 9 (+ sweep), 12, Contents ×2; PROJECT.md map row + TESTING row + §8 paragraph, p. 1, p. 2, п. 9,
п. 13; AGENTS.md regenerated; docs/SIBLING_MAP.md (§10 rows, by name); PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md :392 and check
33 (i): "(i) Standing documents (PROJECT.md «Лишних документов нет», the owner's word 17.11.2026): sample the role files,
CLAUDE.md, PROJECT.md and the window's new specs for a sentence that sends a role to read, every time, a file that is not an
`owner`/`procedure` row of axis 31 (`docs/SIBLING_MAP.md`), and the tracked files added in the window outside the
not-extra class of that rule — each a finding; the name pin is `tools/tests/test_role_carriers_one_owner.py` (K-NOBRIEF)."
DECISIONS.md D-0033 trim + header (D1); `.claude/skills/session-retro/SKILL.md` (§4.6); the pile rows (§10, both worlds);
the supersede line in spec 20261116 (§4.8); the C3 staged files read and committed; C1 and PKG branches merged in; the F9
(a) finding offered to the package pile (AR-3 change check: backward compatibility). Witness: BOOT BUDGET line verbatim;
`python -B tools/agents_md.py --check`.

### L-b — the Lead (after C2)

Read and commit C2's staged `tools/test_quarantine.py` and `tools/dispatch_gate.py` (`tier: opus`); the one critic of code
on the topic gets the C1/C3/PKG/C2 reports and witnesses (two-layer entry); after ACCEPT: P1, P3, then `python -B
tools/wave.py merge`; remove the stale worktree (B m5); node statuses moved in the same move.

### Wave 2 — N7 (exchange-form; fork F-R2-1)

**N7-L (Lead, `tier: opus`, `Deviation: scout golden set not run (PROCESS/SCOUT_GOLDEN_SET.md absent; exams deferred,
D-0037)`):** scout.md rule 10 parenthetical "(the grammar, the flag list and an example are in `docs/tasks/exchange-form.md`;
`tools/digest_form.py` reads the digest back and `tools/handback_extract.py` prints what it found)" → "(the flags the reader
raises are rule 11; an example is `tools/fixtures/digest_form/t-794.md`; `tools/digest_form.py` reads the digest back and
`tools/handback_extract.py` prints what it found)"; new scout.md rule 11 "11. What the reader flags." + the §4.5 grammar
sentence + exchange-form :49-79 (the flag table and the note after it) verbatim. CLAUDE.md rule 11 · inline DoD, after its
first sentence: "A brief carries FACTS by pointer: `given:` names the frozen file (a hand-back report, a digest) and the
digest's objects by their exact ids (`q2a, q2b`), never by a prefix, so a scout's reservation travels with its object;
changing code is pointed at by `path::symbol`, not a line range. The DoD, the edges and the non-goals stay inline. Prose
outside the manifest is at most about 8 counted lines (a target read by calibration check 34, not a gate)." AGENTS.md
regenerated. SIBLING_MAP :35 → "`.claude/agents/scout.md` rules 10-11 (the form and the flag table) <->
`tools/fixtures/digest_form/t-794.md` (the example) <-> `tools/digest_form.py`"; :343 "by pointer to `exchange-form.md`" → "by
pointer to `.claude/agents/scout.md` rules 10-11"; :487 "rule 10 ↔ exchange-form ↔ digest_form a pinned trio" → "rules 10-11
↔ digest_form ↔ the t-794 fixture, a pinned trio (axis 1)"; row :506 removed. Committed on a wave-2 branch, pushed.

**N7 (builder, worktree from the wave-2 branch, no isolation):**
given: this spec §4.5, §8, §11 N7; `C:/QAFactory/forge-repo/docs/tasks/exchange-form.md`; `tools/test_digest_form.py`;
`tools/digest_form.py` :1-50; `tools/handback_extract.py` :30-40; `gateway/PI_HARNESS.md` :50-65;
`tools/test_handoff_rule_anchors.py` :150-167; `tools/tests/test_role_carriers_one_owner.py`
owns:
C:/QAFactory/forge-repo/tools/fixtures/digest_form/t-794.md
C:/QAFactory/forge-repo/tools/test_digest_form.py
C:/QAFactory/forge-repo/tools/digest_form.py
C:/QAFactory/forge-repo/tools/handback_extract.py
C:/QAFactory/forge-repo/gateway/PI_HARNESS.md
C:/QAFactory/forge-repo/tools/test_handoff_rule_anchors.py
C:/QAFactory/forge-repo/tools/tests/test_role_carriers_one_owner.py
C:/QAFactory/forge-repo/docs/tasks/exchange-form.md
non-goals: digest_form behaviour; FLAG_NAMES; scout.md, CLAUDE.md, SIBLING_MAP (N7-L); a mechanism path is staged, never committed
handoff: C:/QAFactory/forge-repo/docs/tasks/handoffs/t-<id>-n7-digest-fixture.md
edges: E16
DoD: `( cd <N7 worktree root> && python -m pytest tools/test_digest_form.py tools/test_handoff_rule_anchors.py tools/tests/test_role_carriers_one_owner.py tools/test_handback_extract.py -q )` all green; test: tools/test_digest_form.py::test_the_example_of_the_note_flags_exactly_the_two_it_names (reads the fixture), ::test_the_flag_name_list_is_the_one_list_the_reader_note_and_corpus_agree_with (reads scout.md) | expected from: §4.5
Transformations: the fixture = exchange-form :81-130 verbatim (the regex `^```\n(digest: v1 t-794\n.*?)\n```$` still finds
it once); `test_digest_form.py`: `NOTE` → `FIXTURE = ROOT / "tools" / "fixtures" / "digest_form" / "t-794.md"` in
`example_block`; the flag-name test reads `SCOUT = ROOT / ".claude" / "agents" / "scout.md"` instead of the note; the
PI_HARNESS wanted entry "docs/tasks/exchange-form.md" → ".claude/agents/scout.md"; docstring :5 updated. `digest_form.py:13`
→ "The grammar and the flag list live in .claude/agents/scout.md rules 10-11; the example is tools/fixtures/digest_form/t-794.md";
`:39` "the note exchange-form.md must carry every FLAG_NAMES entry" → "scout.md rule 11 must carry every FLAG_NAMES entry".
`handback_extract.py:37` "Form: docs/tasks/exchange-form.md." → "Form: .claude/agents/scout.md rules 10-11.". PI_HARNESS.md:58
the sentence naming the path → "the grammar and the flag list are in .claude/agents/scout.md rules 10 and 11 -- read them
first." `test_handoff_rule_anchors.py` `K_SCOUT_FORM = ("digest: v1", "`tools/digest_form.py`")`. K-NOBRIEF DELETED gains
`("docs/tasks/exchange-form.md", "exchange-form")`. `git rm docs/tasks/exchange-form.md`.

---

## §12 Edges, each with its invariant

| # | Edge | Behaviour | Invariant |
|---|---|---|---|
| E1 | TEMPORAL — the briefs exist before C2's commit, absent after; main sees them until the wave merge (B B2, A B1) | the deletion and every redirect reach main in ONE `wave.py merge` | no commit reachable from main's first-parent chain has a MAIN document pointing at a deleted file |
| E2 | TEMPORAL — between the L-a commit and C2 on the batch branch, `test_role_carriers_one_owner.py` is red (OWNER_KEYS in two files: brief + critic.md, builder-rules + TESTING; POINTERS to removed rows) (A B1) | expected red; in NO witness before C2's | a red that is the plan's own window is never read as a defect, and C2's witness is the first that must be green |
| E3 | TEMPORAL — a branch merged into main AFTER wave 1 that cites a deleted path or stem (B B3 (a)) | K-NOBRIEF is red in its CI / witness; a worktree branch that edits a deleted file meets a modify/delete conflict in `wave.py merge` → its content goes to the new home (the pile rows are already re-pointed) | a deleted file is never resurrected by a late merge |
| E4 | FORGE_CARRIERS loses builder-rules, gains TESTING.md (A B4, B B1) | gate-named set: old ⊆ new ∪ {`test_arch_check.py`}, whose keep row becomes `data_join` (PKG) | a test file never falls out of keep silently: every name that leaves the gate-named set is re-layered by name in the same batch |
| E5 | historical files keep dead pointers | not edited | they are outside MAIN and POINTERS; nothing reads them as rules |
| E6 | Russian → English (builder.md 9-12) | translated; the plan critic checks each condition/consequence pair against §4.2 | no item of builder-rules loses its condition or its consequence |
| E7 | critic.md and scout.md edits owe exams that are absent | commit lines `Deviation: …` | an edit to an exam-gated role file never lands silently past its rule |
| E8 | K-NOBRIEF false red / false green | false red names file:line + door; bare stems are hits (B6); the semantic miss → check 33 (i) | a MAIN mention of a deleted file, by path or by stem, is always red, except the one ALLOWED sentence |
| E9 | a role with no testing duty (scout) | no K-TESTPTR row | the pin lists only roles that must use TESTING.md |
| E10 | "no restatement" (axis 31) vs "a role file says what THIS role does" | pointers + one phrase; OWNER_KEYS sentences only in their owner after C2 | a full key sentence never stands in two scanned files on a green tree |
| E11 | the register read by code: an axis-31 row with an unknown class word, a malformed row, a missing table | not MAIN (unknown class) / the row is skipped / a missing table fails `test_register_sees_the_main_documents` | an unparseable register can never make the scan pass with an empty MAIN |
| E12 | `rule_block` splits role files on `^\d+\. ` | questions are `Q1.`…`Q13.` | rules 16, 17, 18, 21-24 stay findable; M1: rules 21-24 are this spec's |
| E13 | RUNBOOK §9.8 owned by t-1122 (TEMPORAL: K-DOC before / after) | C1 never edits §9.8; the wave-1 merge waits for K-DOC (P1) | two specs never both rewrite §9.8, and main never holds a MAIN pointer to builder-rules |
| E14 | the package edit (AR-29 carrier) and CLAUDE.md rule 10 / designer rule 1 / critic Q11 | land in the same wave merge | the axis-1 tie never holds two homes on main |
| E15 | t-1122's K-GATE may land before or after C3 (TEMPORAL) | builder.md rule 9 states the duty only (true in both worlds) | the role file never claims a gate that is not on main |
| E16 | wave 2 before / after: exchange-form exists until N7's commit | N7-L lands first on the wave-2 branch; `test_digest_form.py` reads the note until N7, the fixture and scout.md after; one merge | main never has scout.md pointing at a missing note or a test reading a missing file |

---

## §13 Closing table — every fix of both verdicts → where applied in r2

| Fix | Verdict | Applied in |
|---|---|---|
| B1 C2 order, git rm in C2, L-a commit first, worktree from batch branch, E1 restated, temporal edge | A | §11 order + C2 owns + L-a; §12 E1, E2 |
| B2 C3 witness from the worktree root, all green | A | §11 C3 DoD |
| B3 package card, AR-29 line, judgment line, selftest --lang, .py comments + mapping line | A | §1; §11 PKG; §4.2.3 rule 11 last sentence; §10 package rows |
| B4 re-layer test_arch_check, E4 rewritten | A | §10 test-layers row (data_join, evidence); §12 E4; C2 DoD |
| B5 OH9-1, OH9-7, PC4-6, release-next/2:12 | A | §10 pile rows; L-a |
| B6 bare stems, design/ in MAIN, adversarial row | A | §8 K-NOBRIEF (stems, adversarial rows); §2 design/ row |
| B7 N7 card, rule 24, designer line, POINTERS row, TESTING split, supersede line | A | §4.5, §11 N7-L/N7; §4.8; §4.2.1 split; §11 C2 POINTERS |
| F1 D-0057 holder; trim D-0033 | A | §4.1 rule 21 edit; §5 D1 |
| F2 items 18, 20, 11, 7a, 16а, 13 | A | §4.2 table; §4.2.3 rules 4, 9, 10; §4.2.2; §4.2.4 |
| F3 holder 7a vs 16 (б) | A | §5 D10; §4.2.3 rule 9 |
| F4 one leave-the-round criterion; "queue it instead" | A | §6 |
| F5 one register; «вне основных»; not-extra widened; PROJECT map TESTING row | A | §2; §8 |
| F6 template line 16; docs/retro/README; unlisted documents; specs-folder briefs legal | A | §3; §4.6; §4.7; §2 |
| F7 prepare_copy.py; feature-fragility record; SIBLING_MAP by name | A | §10 |
| F8 TESTING :229 text; 7b self-reference | A | §4.2.1 |
| F9 §9 table corrected | A | §9 |
| F10 strike resolved not-established lines | A | Not established (struck); §1/§2/§10 cite the settling measurements |
| F11 HOST_FULL carve-out; absolute given paths in C3 | A | §2; §11 C3 given |
| F12 duplication: three lists | A | §2 (one register) |
| B1 E4 fails; package readers; §1 claim | B | as A B3/B4 |
| B2 convergence not buildable | B | as A B1 |
| B3 (a) open-dispatch window | B | §11 P3; §12 E3 |
| B3 (b) tell t-1122 | B | settled: t-1122 §6.3 already says builder-rules is being dissolved there (read); §4.2 row 13 |
| B3 (c) cancel 20261116 L1-L5 in their carrier | B | §4.8 supersede line |
| B3 (d) C3 given/DoD carry rule 24 | B | §11 C3 |
| M1 rules 21-24 invariant | B | §4.1 M1; §12 E12 |
| M2 split the budget row | B | §9 |
| M3 one wording in four places; (c) quote; (d) sweep enumeration incl. rule 10 (b) | B | §6 |
| M4 one register; open not-extra list | B | §2; §8 |
| M5 template; Бриф sections named; owner question | B | §4.7; §2; fork F-R2-5 |
| M6 F5 via trim | B | §5 D1 |
| M7 N7 readers; wave 2 | B | §10 N7 rows; §11 wave 2; fork F-R2-1 |
| M8 exact pointer key in C1 DoD | B | §11 C1 DoD |
| M9 owns_readers docstring readers | B | §4.8 last paragraph |
| m1 dropped clauses named | B | §4.2 table (5, 7a, 11, 13, 8, 20, 7d) |
| m2 label | B | §9 |
| m3 t-2046 census as a ledger | B | §2; §4.1 Q12 (c) |
| m4 prepare_copy.py | B | §10 |
| m5 stale worktree | B | §10; §11 L-b |
| m6 pin rows legal | B | §8 (rows of an existing file) — note for the code critic |
| Lead: F4 (a), F6 (a), F5 withdrawn, F3 number with carrier | Lead | §4.5; §4.8; §5 D1; §9 |
| Lead: B3 package edited, axis-1 tie kept | Lead | §1; §12 E14 |
| Lead: B4 (a) | Lead | §10; §12 E4 |
| Lead: builder-rules 13 home from t-1122, §9.8 ownership | Lead | §4.2 row 13; §10; §11 P1; §12 E13 |

Applied: 71 of 71; forks returned: 6 (below), one question for the owner (F-R2-5).

---

## §14 Forks (recommendation first)

- **F-R2-1 N7 timing** (A B7 "a card now" vs B M7 "wave 2"). (a) Drafted now (§11), landed as wave 2 after wave 1 is on main
  — **recommended**: N7 touches CLAUDE.md and SIBLING_MAP (L-a's files) and a code contract with a fixture; a second merge
  keeps wave 1's critic pass small. (b) One wave: N7-L joins L-a and N7 joins C2 (C2's owns grow by 7 files; one critic
  pass). Both verdicts' substance (exact texts, readers) is met either way.
- **F-R2-2 RUNBOOK §9.8 sequencing with t-1122.** (a) The wave-1 merge waits for t-1122 K-DOC (a small Lead / small-work
  doc edit) — **recommended**: one owner of §9.8. (b) If K-DOC is late, the Lead's L-b replaces only «(builder-rules п. 13)»
  by «(`.claude/agents/builder.md` rule 9)» and K-DOC's whole-section text later supersedes it (two writers of one line,
  for one wave).
- **F-R2-3 home of `docs/retro/README.md`.** (a) Folded verbatim into `.claude/skills/session-retro/SKILL.md` —
  **recommended**: the skill holds both pointers to it and the inbox topic; no translation. (b) A check of
  `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md` (the weekly carrier; the README says the reduction runs at calibration until the
  Architect's entry), translated. (c) Keep it as a main document (an axis-31 `procedure` row) — contradicts W-1's «найти ему
  дом».
- **F-R2-4 home of the digest flag table.** (a) scout.md rule 11 — **recommended** (FR-38: the requirement reaches the role
  before the work; one place for scout and Lead; cost ~+1 K tokens per scout spawn). (b) `tools/digest_form.py` docstring
  (code carries its legend; the scout never sees the flags before it is judged).
- **F-R2-5 (the owner's question, CLAUDE.md 11a; B M5)** «избавиться от всех брифов» — do the per-batch `## Бриф` section,
  the header line «Общий бриф дизайнерам» and the card's «Бриф пачки N» get renamed? (a) Keep the names: they are per-batch
  text, legal by §2 — **recommended** (renaming touches `piles.py:1934` BATCH_HEADINGS, the template and every untaken
  batch). (b) Rename (e.g. «Вводная») — a later node with `piles.py` in its owns. The spec is written for (a).
- **F-R2-6 TESTING:88 node id** (F8 (a)). The Lead names the stream/node that will add the `test:` check (told-before-work /
  coordinator offload were r1's guesses, not established); with none, the «код пока не проверяет» world applies (§4.2.1).

## Small choices closed by the designer

- S1 Folded role text is English; text moving into TESTING.md and the retro skill section stays Russian (verbatim).
- S2 `test_arch_check.py` → `data_join`: td-15 §B.2 criterion 4 («строка реестра и её читатель») holds — the test drives
  `arch_check.check_files` with the shipped `references/detectors.json` rows, missing keys, a broken file and custom rows
  (test_arch_check.py:163-188; arch_check.py:41, :66); criteria 1, 1b, 2, 3 do not hold (no carrier names it — repo Grep
  `test_arch_check` lists only builder-rules, test-layers, features.json, records). Quarantine was not chosen: `enter`
  needs a CI pipeline (test_quarantine.py:3-4).
- S3 critic questions `Q1.`…`Q13.`; new critic rules append as 21-24; builder rules append as 9-12 (no renumbering).
- S4 builder.md rule 9 carries the bounded-wait duty without t-1122 §6.3's gate clause (D11, E15); t-1122 §6.3's phrase
  "and a stdin read nothing feeds" is moot after the Lead dropped G2 — noticed for the Lead (t-1122's text, not mine).
- S5 The mapping sentence extends verdict A's wording by the numbers 7b, 7c, 8 found in package comments (I-2).
- S6 Negative-control tests broken by the move are deleted, not rewritten, each named with where the behaviour stays checked.
- S7 MAIN is the `.md` rows only (`owner`/`procedure`); `.yaml`, directories and `tools/*.py` rows of axis 31 are skipped by
  K-REG.

## Not established

- Struck (settled by verdict A F10 / this round): CI runs `tools/` tests (forge-check.yml:96); no kit tree for
  install_parity; test_split's printed line has no other carrier; `SCAN_ROOT = "scripts"`; RUNBOOK §9.6 read-only line
  exists; the integrator list is enforced nowhere; no pile node carries 20261116 L1-L5 (§4.8); spec 20261116 is accepted
  text (t-897) with L1/L2 not landed (both verdicts).
- Byte sizes after the change: estimates (no shell in this role); the card and L witnesses measure.
- Whether any tool checks that SIBLING_MAP paths exist (t-1122 §11 mentions a "check 12" liveness reader): the rows naming
  deleted files leave in the same commit either way.
- The batch header `статус:` of each pile row in §10 (L-a reads it; both worlds stated).
- Whether `DECISIONS_ARCHIVE.md` holds D-0033's dropped clause verbatim (L-a greps before trimming; both worlds stated).
- The exact sentence of `gateway/PI_HARNESS.md` around :58 (N7 reads :50-65; the replacement keeps the test's wanted strings).

## Reading trail

Read whole: spec r1 (691 l.); verdict A (293); verdict B (204); spec 20261117-bounded-waits (649, two parts);
`docs/tasks/critic-diff-brief.md` (126); `plans/builder-rules.md` (136); `.claude/agents/critic.md` (178), `builder.md` (101),
`designer.md` (107), `scout.md` (117); `docs/tasks/exchange-form.md` (157); `tools/tests/test_role_carriers_one_owner.py` (254);
`tools/test_handoff_rule_anchors.py` (173); `plans/piles/_template/batch.md` (84); `docs/retro/README.md` (34).
Read ranges: `docs/TESTING.md` :36-235; `docs/SIBLING_MAP.md` :473-533; `ai-packages/qa-factory/design/architecture.md`
:60-66, :118-124, :138-153, :214-225; `test-layers.json` :80-95, :167-171, :789-793, :1388-1392, :3718-3731, :6300-6357;
`selftest.py` :580-739; `tools/test_quarantine.py` :40-64, :1325-1369; `tools/test_digest_form.py` :1-130, :660-691;
`tools/digest_form.py` :1-50; `tools/mechanism_gate.py` :210-279; spec 20261116 :325-334, :395-482 (+ heading grep);
`DECISIONS.md` :1-33; `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md` :388-393, :1046-1080; `docs/RUNBOOK.md` :612-633;
`plans/piles/onboarding-forge/batch-1` :1-12; `release-next/batch-2` :1-14; `conductor/batch-4` :1-4;
`td-15-scenarios-quarantine.md` :303-322; `test_arch_check.py` :1-30.
Greps (Grep tool; each empty result with a same-shape positive control): the six names + exchange-form over the repo
(count, 95 files); the same over `ai-packages/qa-factory` (`.py` -o; non-`.py` files: 3); `gate-registry.json` line 188;
`builder-rules|critic-diff-brief` in `design/`; `question \d|critic brief|the brief` -i in `design/`; `exchange-form` in
`tools/` (7) and `gateway/` (2); `test_arch_check` repo-wide (23 files); `detectors|json` in test_arch_check.py and
arch_check.py; `"layer": "detector"` in test-layers.json; `gate_named|detector` in td-15; batch rows with the names in
`plans/piles/**/batch-*.md` and their statuses (the CRLF-safe `\|\s*$` form after a `$` miss); `t-897|spec-facts-by-code` in
`plans/piles` (2); `Бриф` in `tools/piles.py` (2); `retro/README` repo-wide; `SIBLING_MAP` in `tools/*.py` (37/22);
`KNOWN MISSES|TWO QUESTIONS|__doc__` in test_owns_readers.py (0; control 19); `--check` in architecture_index.py;
`never edited|trimmed` in DECISIONS.md; `^33\.|^34\.|builder-rules|brief form` in the protocol; RUNBOOK names; Glob
`PROCESS/*.md` (12 files).
Needed beyond the manifest: the files above outside the four given specs.

## Lead decisions on r2 (Lead, 17.11.2026)

- F-R2-1: (a) — N7 is drafted here and lands as wave 2.
- F-R2-2: (b) — wave 1 does not wait for the bounded-waits K-DOC: L-b replaces only the pointer; K-DOC's whole-section
  text supersedes it later (the bounded-waits spec is in its own designer round, t-1136, by the owner's word «делаем всё
  сейчас»).
- F-R2-3: (a) — `docs/retro/README.md` folds into the session-retro skill.
- F-R2-4: (a) — the digest flag table goes to scout.md rule 11.
- F-R2-5: the owner's question, asked; the spec stays written for (a) until her word.
- F-R2-6: no node is named; the «код пока не проверяет» world applies.
- S1-S7: accepted as closed by the designer.
- No third plan critic (the owner's word 17.11.2026 on rounds); the code critic judges the result, one pass per topic.
- Ordering with t-1137 (short auto-loaded text for workers): this spec's waves land FIRST; the split works from main
  after them.

## The owner's answer to F-R2-5 (owner, 17.11.2026)

«нет. Бриф о том как делать узел необходим, бриф который даётся роли когда у нас и так куча документов для ролей -
лишний» — the per-batch `## Бриф` sections and their names stay: (a).
