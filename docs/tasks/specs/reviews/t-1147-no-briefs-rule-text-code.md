# t-1147 — code critic: no-briefs cards C3 (role files) and L-a (Lead text), commit 9616b6f4

Scope: commit 9616b6f4 on `pile/forge/batch-9` (worktree `.claude/worktrees/nobriefs-batch`, head 7a2cf516, read only),
against spec `docs/tasks/specs/20261117-no-briefs-fold-into-roles-spec-r2.md` (§4.1-§4.3, §4.6, §4.8, §6, §7, §8, §10,
§11 C3/L-a, Lead decisions). C1, PKG, C2 are out of scope (t-1148).

## Verdict

**NEEDS WORK — годно с правками.** No finding blocks the merge as a broken tree (pins green, pointers resolve, nothing
the roles need was lost). Per CLAUDE.md rule 9 / W-4, every finding below is fixed in this round, not queued. Fixes F1-F5
before the wave merge; F6-F9 are small and ride in the same fix round. Acceptance is the Lead's decision (rule 6); F3
reverses a spec decision (§6) and is therefore the Lead's call.

Per card: **C3** — fit with fixes (F1, F4, F5, F6, F7). **L-a** — fit with fixes (F2, F3, F6, F8, F9).

## Findings

**F1 (fix before merge) — `builder rule 9` in 10 package comments now resolves to the WRONG rule.**
Surface: rule-number citations from package comments into forge role files. builder.md now has a NEW rule 9 "Runs,
cheaply" (`.claude/agents/builder.md:106`). Ten package sites cite "builder rule 9" meaning the old backward-compatibility
item 9: `scripts/contract.py:217`, `driver_s0.py:705`, `planning_contract.py:236, :1535, :1626`, `validate_artifacts.py:220,
:233`, `tests/test_probe_gap_word.py:286`, `tests/test_s3_s4_chain.py:290`, `tests/test_story_run_s0.py:2397`. A reader who
follows "builder rule 9" lands on the runs rule, not on "an older project/story in flight is never refused". The mapping
sentence (`builder.md:130-131`) only covers the literal `"builder-rules N"`; spec I-2 searched `builder-rules|critic-diff-brief`
and missed the "builder rule N" spelling. Neighbouring forms walked: `builder-rules N` (1, 5, 7a, 8, 9, item 1/5/9, p.9) —
all mapped; "critic question 9/11/12" (`tools/language_sites.py:36-51`, `tools/architecture_gate.py:66`, protocol check 41) —
still correct, Q-numbers were kept; "brief item 13 (d)" (`tools/owns_readers.py:26`) — re-pointed by C2.
Fix: after the mapping sentence add a stem-free sentence (K-NOBRIEF ALLOWED match is untouched):
`Package comments that cite "builder rule 9" mean this rule's backward-compatibility clause, not rule 9 above.`
While there, "this rule's former numbering" reads as if all numbers were rule 11's; → "the former numbering of the builder's
rules".

**F2 (fix before merge) — the commit's four questions: axis block lines false for axes 4, 18, 32, 34; cost (a) under-stated.**
The commit marks axes 4, 18, 32, 34 "n/a -- nothing on this axis changes", yet the same commit edits rows of exactly those
axes in `docs/SIBLING_MAP.md`: axis 4 :95 ("Builder rules" row), axis 18 :401 and :405 (Q9 carrier), axis 32 :574 (the
acceptor row), axis 34 :599 (the reviewers row) — `git show 9616b6f4 -U0 -- docs/SIBLING_MAP.md`. Spec §1 itself lists 4,
18, 32, 34 as touched. Cost (a): "critic about +12 KB" — measured `git show <rev>:.claude/agents/critic.md | wc -c`:
10804 -> 28089 = **+17 285 bytes** (builder +4 476, designer +590 match). "(BOOT BUDGET: 112557 bytes / 120000 WARN)" labels
the limit as WARN; `tools/session_context.py:207-209` WARN 110000, BREACH/LIMIT 120000 (the Deviation line is right).
Fix: a pushed commit is not rewritten; the next Lead mechanism commit (L-b) or the DECISIONS-free route carries a
correction block: `axis 4: covered -- "Builder rules" row re-pointed (:95)`, `axis 18: covered -- Q9 carrier rows :401,
:405 re-pointed`, `axis 32: covered -- acceptor row :574 re-pointed`, `axis 34: covered -- reviewers row :599 re-pointed`,
and "(a) correction: critic +17.3 KB measured (wc -c); 120000 is the BREACH line". (b) other lines: axis 1, 2, 31 correct
(F3-1 exists, `plans/piles/forge/batch-3-exam-debts.md:24`); (c), (d) hold (K-NOBRIEF is on CI path after C2, check 33 (i)
added at protocol :1046).

**F3 (fix before merge, Lead's decision) — the W-4 criterion now has three hand-written homes.**
The same sentence stands in `CLAUDE.md:226` (rule 9), `.claude/agents/critic.md:198-202` (Q4) and, in Russian,
`PROJECT.md:206` (п. 9) — grep count 1 each for "never a way to put off a rule fix while rules are being fixed" /
«редкий случай, а не способ отложить починку правил». The dispatch DoD ("no rule duplicated in two homes") and axis 31's own
rule (one owner, others a one-line pointer) both forbid this; spec §6 ordered it (plan verdict B M3 "one wording in four
places"), so the deviation sits in the spec. The pin cannot see it (no OWNER_KEYS row; the Russian copy is invisible to it).
Fix (recommended): owner CLAUDE.md rule 9 keeps the text; critic Q4 → "A sibling is fixed in the same round; it leaves only
by CLAUDE.md rule 9's exit (the rare case)." + the critic-specific line forms; PROJECT.md п. 9 → «уйти из раунда — только
выходом правила 9 `CLAUDE.md` (редкий случай)»; C2-file follow-up: an OWNER_KEYS row `("routing:rule-9-exit", "CLAUDE.md",
"never a way to put off a rule fix while rules are being fixed")`. If the Lead keeps three copies, record why in the spec.

**F4 (fix before merge) — designer.md: the readers duty now has two contradicting procedures.**
New text in rule 3 (`designer.md:49-53`): the readers list IS the `owns_readers.py` block; "a hand grep is owed only for what
its KNOWN MISSES name"; "the plan critic re-runs it". Rule 7 (`designer.md:103-108`, unchanged): readers "found by a grep
for the file's name ... (the command and its hit count in the draft)". And critic Q13 (d) (`critic.md` rule 24): the critic
does NOT re-run the tool unless the block is missing or its base is stale. A designer cannot satisfy both rule 3 and rule
7; "re-runs" contradicts Q13 (d).
Fix: move the block sentence into rule 7, replacing "found by a grep ... (the command and its hit count in the draft)" with
"found by the `owns_readers.py` block the Lead attaches (quote it; answer every line in the forms of critic.md rule 24, Q13
(d)); a hand grep, with its command and hit count, only for its KNOWN MISSES"; "the plan critic re-runs it" → "the plan
critic re-runs it only when the block is missing or stale (Q13 (d))"; rule 3 keeps "Readers of every touched file: rule 7".

**F5 (fix before merge) — the plan gate lost the duplication question; rule 22's header disagrees with rule 24.**
Spec §4.3 homes pre-release critic brief item 8 (duplication on a plan) as "Q6 + rule 24 asks Q4/Q12", but rule 24
(`critic.md:284-285`) asks only Q13, Q4, Q12; Q6 is diff-only (rule 18 "on EVERY diff gate"; rule 22 header :192 "Q12 also
on a plan gate"). So the claimed home does not apply on a plan; item 7 (AR/FR walk on a plan) is likewise homed in Q8/Q10/Q11,
which rule 24 does not invoke (PROJECT.md new-idea step 6 does demand AR/P/FR on a plan). The header ":192 (Q12 also on a
plan gate)" omits Q4, which rule 24 asks.
Fix: rule 24 → "answer Q13 below and Q4, Q6 and Q12 of rule 22 (read "the diff" as "the plan")" — Q10 too if the Lead wants
the AR walk on every plan gate; rule 22 header → "(Q4, Q6 and Q12 also on a plan gate, rule 24)".

**F6 (fix in round) — sweep-the-artifact misses of the "queue" class (W-4).**
Same artifacts as §6's sweep, three neighbours left: `CLAUDE.md:232` "before walking the map and before queuing anything";
`critic.md:236-237` Q6 "whether the convergence is already queued (a queued analog named in the spec is queued, not a
finding)" — a queued residual accepted without Q4's exit; `critic.md:242` Q7 "(Q4: no "queue" severity)" — Q4 no longer
says that in words. Fix: rule 9 "before moving anything out of the round"; Q6 "or whether the convergence is already a node
(Q4's exit; a node named in the spec is not a finding)"; Q7 "(Q4: there is no "queue" severity)".

**F7 (fix in round) — builder rule 9 restates CLAUDE.md rule 12's new sentence.** `builder.md:106-108` "the witness is ONE
run ... on the final state" vs `CLAUDE.md` rule 12 "closes a round with ONE witness run after all edits, never one after each
edit (D-0035)". Fix: rule 9 "the witness is CLAUDE.md rule 12's one run (Cost gates), of rule 4's scope, repeated once only if
code changed after it" — keep only the builder-specific clauses.

**F8 (minor) — retro skill: the README's «Недельное сведение» heading was dropped**, so the procedure (steps 1-6) now sits
under "### Что где лежит" (`.claude/skills/session-retro/SKILL.md:50`; diff vs the README body: only the heading changed).
Fix: a `### Порядок` heading before «Делает Архитектор при включении».

**F9 (minor) — PC4-6 cell** (`plans/piles/package-ci/batch-4-dieta-testov-td-11-td-15.md:27`) "строка 7c списка по типу
правки" — the TESTING list has no "7c" label. Fix: «пункт про `story_run.py` списка по типу правки».

## Paragraph walk — where every brief paragraph lives now

**critic-diff-brief.md** (word-diff of brief :10-114 against critic.md rules 21-22, script in Trail): verbatim except the
spec's edits (builder-rules 7b → TESTING section ×2; "the Lead" → D-0057, present at DECISIONS_ARCHIVE:145; Q4 replaced by
§6 wording; "item 4" → Q4; "question 9" → Q9; "(a data ledger…)" added). Title/P1 :1-6 → critic rule 18 + CLAUDE.md rule
3. Two layers → rule 21. Q1-Q12 → rule 22 (Q6/Q7 spot-checked: verbatim). What comes back :116-125 → rule 23 (vocabulary
mapped to rules 6/17). Dropped from old Q4: the pointer "PROJECT.md п. 9" and "the debt is worked down, not grown" —
substance kept by "fixed in the same round".

**builder-rules.md**: 1 → rule 4 («Needed from integration», keys) + rule 11 (key default); integrator list dropped (F7(a)).
2 → rule 10. 3 → PROJECT.md «Язык». 4 → rule 11. 5 → rule 11 (caps in code; phases clause kept). 6 → rule 11. **7** →
TESTING :134-135 bullet; size pin = cap → TESTING «Что не пишется» row 3. 7a → rule 9. **7b** → TESTING «Что запускать по
своей правке» :91-132 (spot-read: verbatim, edits per §4.2.1). 7c → TESTING :108-109. 7d → TESTING layers/«Что не
пишется»/«Правила ролей не теряются»/«Бюджет», DOC-DISPATCH in CLAUDE.md rule 11. 8 → rule 11 + FR-4/FR-57 (the "not the
person's repair" half is FR-3, read whole per rule 11). 9 → rule 11. 10 → rule 11 (+ RUNBOOK §9.6). **11** → rule 4
(spot-checked: all keys present, incl. SKILL < 200 bytes, changelog.d fragment, 500 words). **12** → rule 11 + PROJECT.md
p. 1. **13** → rule 9 + RUNBOOK §9.8 :391-398 («Отчёт воркера называет цикл, оставленный позади» present). 14 → rule 4. 15
→ CLAUDE.md rule 2 / builder rule 4. 16 (а)(б) → CLAUDE.md rule 12; (в) → rule 12 + the hook's own STOP message. 17, **18**
→ rule 10 (no `-c core.hooksPath` clause present). 19 → rule 10 pointer; grammar in `tools/architecture_gate.py` + designer
rule 1. **20** → RUNBOOK §12 items 2, 8 (C1, not re-judged here), R11-h, Cost gates "a push before a worktree launch".
Tail → rule 11 (CLI_SCRIPTS, judge.provider: none); the rest dropped with reason (§4.2).

**pre-release-0.9-brief-common.md** (the "designer brief"): paths/versions/D-0025… dropped (one-off); return shape 1-9 →
designer rules 1-3, 5, 7, CLAUDE.md rule 11/R11-f, PROJECT.md p. 1, 3, 6; "one mutation → one test" dropped (TESTING
retired it); caps → code; `[meaning]` → PROJECT.md p. 6. Nothing standing lost.

**pre-release-0.9-critic-brief.md**: 1 → rule 12 + Q13 (c); 2 → Q13 (b) + PROJECT.md p. 6; 3 → Q13 (e) (present,
:319-321); 4 → CLAUDE.md rule 3; 5 → Q4 via rule 24; 6 → TESTING; **7, 8 → claimed Q6/Q8/Q10-11, not invoked on a plan (F5)**;
return form → rules 16-17, 23.

**test-diet-brief.md / test-diet-fold-brief.md**: waves cancelled (`docs/tasks/test-diet.md:46-48`), TD-14 closed (:126-127);
registry cleaning → TESTING «Когда тест покраснел» item 4 (:271-274); kinds → «Что не пишется»; fold rule → «Как писать
эффективный тест» 1, 3. Dropped: "no weakening of an assertion that stays" (see Questions).

**docs/retro/README.md** → session-retro SKILL :48-end, verbatim (diff: one heading, F8); pointers :13, :42 re-pointed.

## Standing questions (rules 18-20)

- **DUPLICATION AND CONSISTENCY**: findings F3, F4, F7 (and F5's header mismatch). Grepped: the W-4 sentence in CLAUDE.md,
  critic.md, PROJECT.md, AGENTS.md, TEAMWORK.md; "readers" duty across designer rules 3/7 and critic Q13 (d).
- **CODE QUALITY** (text): F1's "this rule's former numbering" wording; F8 heading. No other.
- **TESTS**: C3/L-a carry no test change (role text; `test: none` per spec); pins are C2's (t-1148). No `tests-over:` owed.
- **ONE ROAD**: none found: grepped role files and the L-a text for a language/project/case exclusion; the single ALLOWED
  sentence of K-NOBRIEF is a data row of C2.

## Pointers resolve

CLAUDE.md Contents "docs/TESTING.md § Что запускать по своей правке" → TESTING:91 heading; ".claude/agents/critic.md §
21-24" → rules 21-24 present; rule 3 → Q6/Q7; rule 4 → TESTING:91; rule 9 → TEAMWORK item 9 (:22-25, `узел:`/`перенос:`
forms). PROJECT.md p. 1, p. 2 (critic rule 21, builder rule 4), п. 13, §8 rule (axis-31 table, check 33 (i)). critic.md
rule 21 «Тест может упасть» (:140), Q5 «Откуда берётся ожидаемое значение» (:61), «Бюджет / Объём», «Бюджет / Файлы»
(:204-227), «не пишется» (:180). builder.md rule 9 → RUNBOOK §9.8 (:391); rule 11 → PROJECT.md p. 1; tools named exist
(architecture_gate, agents_md, mechanism_gate MECHANISM_PREFIXES :215, wiring_check, harness.py, audit_factory CLI_SCRIPTS).
designer.md → TESTING «Строка теста в DoD» (:75), critic rule 22 Q4, rule 24 Q13 (d). Residual deleted-path mentions in
role files, CLAUDE.md, PROJECT.md, TESTING, RUNBOOK, TEAMWORK, SIBLING_MAP, AGENTS, skills, PROCESS: only the ALLOWED
builder.md sentence (case-insensitive grep; positive control: the same call finds it at builder.md:130).

## Questions I could not settle

1. "No weakening of an assertion that stays" (both test-diet briefs) was dropped as wave-only; it reads as a general
   test-edit rule. Keep dropped, or one clause in TESTING «Когда тест покраснел» item 1? (Lead's call.)
2. The commit carries `tier: fable` while the spec says `tier: opus`; legal (the gate refuses only below lead) — noted, not
   judged.
3. BOOT BUDGET not re-run (the SessionStart script; not run from a worker): consistency only — CLAUDE.md +666, PROJECT.md
   +2084, DECISIONS.md −114 = +2636 = 112557 − 109921 (spec §9 "before").

## Spot-checks

- Mechanical layer re-run (cheap): 199 = 183 + 16 (anchors) — consistent with the attached 183.
- Batch statuses before L-a edited pile cells: all six batches `статус: ожидает` (cells may be edited; TEAMWORK § 2).
- D-0033 trim: the old full line is in DECISIONS_ARCHIVE:57-58; D-0057 at :144-145.
- AGENTS.md regenerated: `agents_md.py --check` exit 0.

## Trail

Read: spec r2 whole (960 l.); `git show 9616b6f4` (role files, CLAUDE.md, PROJECT.md, DECISIONS.md, protocol, SIBLING_MAP
-U0, pile rows, spec 20261116 supersede line); worktree builder.md whole, designer.md whole, critic.md :179-321 (diff), TESTING
:75-154, :180-284, RUNBOOK :391-399, TEAMWORK :1-25, SIBLING_MAP headings, retro SKILL :48-end; the seven deleted files from
origin/main 23c9fee3 (critic-diff-brief 125 l., builder-rules 135, pre-release common 85, critic 56, test-diet 72, fold 99,
retro README 33); session_context.py :204-209; owns_readers.py :20-30, :642-648; test_role_carriers_one_owner.py OWNER_KEYS,
DELETED/ALLOWED; schema. Not read: the two plan reviews beyond a grep for my findings (none raised them).
Commands: word-diff script (python, scratchpad cmp.py) brief :10-114 vs critic.md rules 21-22 → only the spec's edits;
`grep -rhoiE 'builder(\.md)? rules? ...[0-9]+'` over package/tools/main docs → 10 × "builder rule 9" (package only);
`grep -rhoiE 'builder[- ]rules?...'` package census; byte deltas via `git show <rev>:<f> | wc -c`; `diff` README body vs
SKILL tail; batch header status greps; `( cd <worktree> && python -B -m pytest tools/tests/test_role_carriers_one_owner.py
tools/test_handoff_rule_anchors.py -q -p no:cacheprovider )` → `199 passed in 2.78s`; `( cd <worktree> && python -B
tools/agents_md.py --check --repo . )` → `AGENTS.md: up to date (111225 bytes)`, exit 0.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "fixes": [
    "F1 builder.md:130-131 add a stem-free sentence: package comments citing 'builder rule 9' mean the backward-compatibility clause of rule 11 (10 package sites now resolve to the new rule 9 'Runs, cheaply'); reword 'this rule's former numbering'",
    "F2 next Lead mechanism commit: correct axis lines 4, 18, 32, 34 to covered (SIBLING_MAP rows :95, :401/:405, :574, :599 were edited); correct cost (a): critic +17285 bytes measured, 120000 is the BREACH line",
    "F3 (Lead's decision, reverses spec 6) W-4 criterion stands in CLAUDE.md:226, critic.md:198-202 and PROJECT.md:206; keep CLAUDE.md rule 9 as owner, turn Q4 and PROJECT.md p.9 into pointers; add an OWNER_KEYS row",
    "F4 designer.md: move the owns_readers block sentence from rule 3 into rule 7, replacing the grep procedure; plan critic re-runs only when the block is missing or stale (critic rule 24 Q13 (d))",
    "F5 critic.md:284 rule 24 also asks Q6 (and Q10 at the Lead's choice) on a plan; rule 22 header :192 names Q4, Q6, Q12 as plan-gate questions",
    "F6 queue-class sweep: CLAUDE.md:232 'before queuing anything'; critic.md:236-237 Q6 'already queued'; critic.md:242 Q7 '(Q4: no queue severity)'",
    "F7 builder.md:106-108 rule 9 points to CLAUDE.md rule 12 for the one-witness-run rule instead of restating it",
    "F8 session-retro SKILL.md:50 re-add a heading before the procedure steps (README heading dropped)",
    "F9 package-ci batch-4:27 PC4-6 'строка 7c' names a label TESTING does not carry; name the story_run.py bullet"
  ],
  "class_completeness": "F1 surface (rule-number citations into forge role files) walked: builder-rules N (mapped), builder rule N (missed, F1), critic question N in tools (still correct, Q numbers kept), brief item 13 (d) (re-pointed by C2). W-4 queue class swept in the same artifacts: CLAUDE.md rule 9 and sweep paragraph, critic rule 5, Q4, Q6, Q7, Q12 (d), rule 19, PROJECT.md p.9, designer rule 2 -- three leftovers (F6). Axis walk of the commit: axes 1, 2, 31 correct; 4, 18, 32, 34 mislabelled (F2).",
  "trail": {
    "read": [
      "docs/tasks/specs/20261117-no-briefs-fold-into-roles-spec-r2.md",
      "git show 9616b6f4 (role files, CLAUDE.md, PROJECT.md, DECISIONS.md, PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md, docs/SIBLING_MAP.md, pile rows, spec 20261116 line)",
      ".claude/worktrees/nobriefs-batch/.claude/agents/builder.md",
      ".claude/worktrees/nobriefs-batch/.claude/agents/designer.md",
      ".claude/worktrees/nobriefs-batch/.claude/agents/critic.md:179-321",
      ".claude/worktrees/nobriefs-batch/docs/TESTING.md:75-154,180-284",
      ".claude/worktrees/nobriefs-batch/docs/RUNBOOK.md:391-399",
      ".claude/worktrees/nobriefs-batch/docs/TEAMWORK.md:1-25",
      ".claude/worktrees/nobriefs-batch/.claude/skills/session-retro/SKILL.md:48-end",
      "origin/main: docs/tasks/critic-diff-brief.md, plans/builder-rules.md, docs/tasks/pre-release-0.9-brief-common.md, docs/tasks/pre-release-0.9-critic-brief.md, docs/tasks/test-diet-brief.md, docs/tasks/test-diet-fold-brief.md, docs/retro/README.md",
      "tools/session_context.py:204-209",
      "tools/owns_readers.py:20-30,642-648",
      "tools/critic_verdict.schema.json"
    ],
    "reruns": [
      {
        "command": "( cd .claude/worktrees/nobriefs-batch && python -B -m pytest tools/tests/test_role_carriers_one_owner.py tools/test_handoff_rule_anchors.py -q -p no:cacheprovider )",
        "result": "199 passed in 2.78s"
      },
      {
        "command": "( cd .claude/worktrees/nobriefs-batch && python -B tools/agents_md.py --check --repo . )",
        "result": "AGENTS.md: up to date (111225 bytes); exit 0"
      },
      {
        "command": "python -B scratchpad/cmp.py <origin/main critic-diff-brief.md> <worktree critic.md> (word diff of brief :10-114 vs rules 21-22)",
        "result": "only the spec-listed edits differ (7b pointers, D-0057, Q4 wording, Q-labels, data-ledger clause)"
      }
    ]
  }
}
```
