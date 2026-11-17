# t-1124 — plan critic: no standing briefs, fold every brief into the main documents

Spec under review: `docs/tasks/specs/20261117-no-briefs-fold-into-roles-spec.md` (designer t-1117, Lead fork decisions at its end).
Journal note: the journal labels this review t-1126 ("dispatch text says t-1124 by Lead error"); the handoff path names t-1124, so this file keeps that name.

**VERDICT: GO WITH FIXES** — the direction is sound and the inventory is mostly right, but 3 findings block dispatching the cards (B1-B3: they make a card's DoD unpassable, a convergence step unexecutable, or open a window with dead pointers under running workers), plus 9 fixes to the spec text (M1-M9) and 6 minor items (m1-m6). All of these are spec edits; none needs a new design. The decision to accept is the Lead's.

## Keys

- **K1 NOTHING LOST — FIX.** Both briefs were read whole and checked paragraph by paragraph against §4.1/§4.2. The critic brief's homes are complete except that Q4's first sentence (kept verbatim) contradicts the §6 edits (M3). builder-rules: every DUTY has a home, but six clauses are dropped without being named in §4.2 (m1). F7 drops the integrator-only list, an unenforced duty; that is a stated weakening, not a silent one (my check: no gate enforces it). The four dead briefs: deletion is right, because nothing live reads them beyond SIBLING_MAP :507-508 and test-diet.md, and the spec handles both. exchange-form has more live readers than §4.7 names (M7).
- **K2 INVENTORY COMPLETE — FIX.** The six brief files match my search. Missed: (1) the pile template `plans/piles/_template/batch.md:16` «Общий бриф дизайнерам: <путь к файлу …>», which tells a dispatcher to attach a brief FILE: it is the generator of this whole class. (2) The mandatory `## Бриф` section of untaken batches and `## Бриф пачки 1` of cards, both required by `tools/piles.py:1934`. (3) `docs/retro/README.md`, a standing procedure read on every retro reduction that is neither main nor listed. (4) The census report that critic Q12(c) makes a standing read. See M5. The §2 border is usable, but §2, §8 and K-NOBRIEF MAIN are three different lists (M4).
- **K3 READERS AND GATES — FIX.** Missed readers: `ai-packages/qa-factory/design/architecture.md:144` (an AR-29 carrier names `dev:docs/tasks/critic-diff-brief.md` question 11) and `:223`; three keep rows of `scripts/tests/test-layers.json`; about 40 package code comments that cite "builder-rules N"; `experiments/measurers/prepare_copy.py:195`; plus the N7 readers listed in M7. The two "not established" lines are settled. CI runs `tools/tests/`: `.github/workflows/forge-check.yml:96` runs `python -m pytest tools/ -q`. The kit side of install_parity needs no change: `toolkit/` does not exist in this repo, and `install_parity.run_check` reads only `host_path`. The only anchor affected is `install_parity_anchors.json:22`, which C2 already owns. The E4 subset check fails as written (B1).
- **K4 BUDGETS — PASS (one label fixed, m2).** Measured with `wc -c`: CLAUDE.md 50808 (the cap of 58500 applies to this file ALONE, `session_context.py:1312-1319`), CLAUDE.md with its four imports 98899, critic.md 10981, builder.md 6239, designer.md 7495, TESTING.md 32159. Estimates after the change: CLAUDE.md about 51.4K, below 58500. Boot total about 111.7K: over the WARN line of 110000, below the BREACH line of 120000. The WARN is really only a WARN: `_budget_status` returns the string " WARN" and nothing else reads `BOOT_WARN_THRESHOLD` outside `session_context.py` and its tests (my grep over tools/, .githooks/ and workflows). No ceiling guards `.claude/agents/*.md`. No raise is needed; F3 (a) stands.
- **K5 THE RULE ITSELF — FIX.** All four questions are answerable: (a) cost stated; (b) axes deferred to the Lead's commit block, which rule 10 allows; (c) K-NOBRIEF runs in CI (forge-check.yml:96), and check 33 (i) is free (check 33 today has (a)-(h)); (d) the "on discipline" part names check 33 (i). Its home, PROJECT.md «Где что лежит», is boot-loaded, and workers load it too (this critic's own context carries PROJECT.md). Three problems. (1) The "Не лишние" list is closed and misses things the process needs: plans of one task, retro inbox entries, exam run logs, experiment notebooks (PROJECT.md p. 5). (2) «строкой этой таблицы» makes the «Где что лежит» table the register of main documents, but that table lists BACKLOG, MEASUREMENTS, provenance and DECISIONS_ARCHIVE (not main) and lacks TESTING.md, PROCESS/, skills and the role files. (3) §6 is narrower and wider than the owner's word (M3). See M4 and M3.
- **K6 EXECUTABILITY — FIX (blocking).** Owns are disjoint: C1 docs; C3 the three role files; C2 tools; L CLAUDE.md, PROJECT.md, SIBLING_MAP, PROTOCOL, DECISIONS and pile rows. Two things break. The convergence that C2 needs cannot be built (B2). The order has no rule for the open dispatches citing the paths (B3). The negative-control deletions are right: each is the TESTING.md «Что не пишется» kind «Отрицательный контроль внутри теста», each is named, and the behaviour stays checked by `test_one_owner_per_key` / `test_brief_what_comes_back`'s successor. C3's card does not carry the F6 (a) text (B3).
- **K7 FORKS AND FEASIBILITY — FIX.** F6: stream L of 20261116 has NOT landed critic.md or designer.md text on main. `git grep -E "Q13|plan gate|rule 24" origin/main -- critic.md designer.md` finds only rule 19's own words; HEAD equals origin/main (b89871b3); only its S1 tool part merged (21c3ec90). So F6 (a) can join without doubling, but only if 20261116's Lead edits L1-L5 are cancelled in their carrier (B3). F4: moving the grammar into scout.md is sound, but exchange-form is HALF a code contract. `test_digest_form.py` reads its examples and asserts FLAG_NAMES against it, and `test_handoff_rule_anchors.py:151` pins its path inside scout rule 10. N7 is undrafted. F5 (a) breaks DECISIONS.md's own header rule (M6). F2, F3, F7, F8, F9 hold on the evidence; D7 is confirmed (no `test:` check in dispatch_manifest.py, dispatch_new.py or dod_gate.py; positive control: "given" → 14 hits in dispatch_manifest.py). Overall: TWO waves. Wave 1 is this spec minus N7. Wave 2 is N7 (a code contract plus a test fixture plus CLAUDE.md rule 11 plus gateway) together with the template / `## Бриф` question of M5.

## Findings (by severity)

### Blocking dispatch

**B1. C2's E4 check cannot pass, and the package is NOT untouched as §1 claims.** (§1 "The package is NOT edited … The only package-adjacent reader is FORGE_CARRIERS"; §11 C2 DoD; E4.)
- Measured: I ran selftest's `_TEST_NAME_IN_TEXT` (`test_[a-z0-9_]+\.py`, selftest.py:588) over `plans/builder-rules.md`. It finds 10 names; the moved part (items 7-7c, lines 26-71) holds 9. `test_arch_check.py` comes only from item 14 (:105), which goes into builder.md in English without the file name, and builder.md is not a FORGE_CARRIER. So "old set ⊆ new set" is false on the first run. The card states no behaviour for that case, and C2 owns no file in which it could restore the name.
- The same move silently falsifies package data. `test-layers.json` row `test_arch_check.py` has layer `gate_named`, why "named by plans/builder-rules.md:71". The row `test_probe_by_code_copy.py` cites builder-rules :37, and the row `test_story_step.py` has `named_by` "plans/builder-rules.md:26". Nothing turns red (selftest.py:629 checks only that `named_by` is non-empty; no code checks the `gate_named` layer against `gate_named_files`), so this is a silent false row. test_arch_check.py also loses its quarantine protection (`_enter_phase2`, test_quarantine.py:1361).
- `design/architecture.md:144` names the deleted brief as an AR-29 carrier; `:223` names builder-rules rule 7. No tool resolves `dev:` carriers (`architecture_index.py` and `architecture_gate.py` have no such code; 32 `dev:` pointers exist), so the pointer goes dead silently in an architecture invariant.
- **Fix:** add a package part, either a small card or a Lead edit, with an `architecture: AR-29 -- carrier re-pointed to .claude/agents/critic.md rule 22 Q11` line. It re-points architecture.md :144 and :223, rewrites the three test-layers.json why / named_by texts, and decides test_arch_check.py's layer (either a reclassification row, or the name kept in a forge carrier). E4 then reads: "old ⊆ new, except names listed in the card with their new keep layer". §1's claim is corrected. The ~40 package comments that cite "builder-rules N" (acceptance.py:285, contract.py:34, brief_pack.py:3164 and others; most say "builder-rules 9" or "7a") are named and queued with the F9 package finding, never left silent (CLAUDE.md rule 9).

**B2. The convergence that C2 runs on cannot be built as written.** (§11 order "C1 ∥ C3 ∥ L1-draft → converge → C2"; E1 "ONE commit".)
- C3's three role files are mechanism paths that stay STAGED, uncommitted, in C3's worktree.
- The L1 draft (CLAUDE.md, PROJECT.md, SIBLING_MAP) is the Lead's uncommitted text.
- C1 commits its docs on its own branch, as builder.md rule 10 says.
- C2's DoD runs `test_role_carriers_one_owner.py` "on the converged tree". Its re-pointed CLAUDE.md and PROJECT.md rows pass only when L1 and C3 are present. No branch holds them, and a weaker model cannot assemble uncommitted files from two worktrees.
- If C1's branch is merged on its own (a routine `wave.py merge`), main turns red: C1 removes TESTING.md's pointer while POINTERS row :78 still expects it.
- "ONE commit" contradicts C1 committing its own owns.
- **Fix:** name a batch branch. Under the enforcement-file rule the Lead commits the C3 staged files and the L1 text there, with `tier: opus`, after reading them; this is not main, so E1 still holds. C2 is cut from that branch (`git worktree add … <batch branch>`, RUNBOOK §12 item 8, no `isolation`). C1 and C3 are never wave-merged alone. E1 becomes "ONE merge into main; no commit reachable from main's first-parent chain points at a deleted file".

**B3. The window under running work and under stream L.**
- (a) Open now, by the journal: about 12 builders (t-1080 … t-1127) and 4 critics in the main checkout (t-1065, t-1121, t-1123/1125, this one), plus designer t-1122. Their dispatches cite `plans/builder-rules.md` 7b and `docs/tasks/critic-diff-brief.md`. Worktree builders keep their own copies, but critics read the MAIN tree: an L-commit landing mid-review deletes a file a critic was told to read. A branch merged after L that adds a pointer turns main red through K-NOBRIEF.
- (b) t-1122 (bounded waits) is choosing "the home" for builder-rules 13 (the spec's last section). If nobody tells it that builder-rules is being dissolved, it may pick builder-rules.
- (c) Spec 20261116 was accepted (t-897, fix round t-913 accepted 00:46). Its Lead edits L1-L5 write into `docs/tasks/critic-diff-brief.md` (L1), critic.md as **rule 21** (L2, a number that collides with this spec's rule 21), a POINTERS row to BRIEF item 13 (L4), and `plans/builder-rules.md` (L5). Under F6 (a) nothing cancels them in their carrier.
- (d) C3's card does not carry F6 (a). Its non-goals say "the stream-L Q13 text unless F6 = (a)", but its given lacks 20261116 §4.1 (:418-452) and §4.2 (the designer line), and its DoD keys lack `24. The plan gate` / Q13 (e).
- **Fix:** add a precondition line. The L-merge waits until no critic or designer dispatch citing the two paths is open in the main checkout. Branches merged after L carry the K-NOBRIEF run in their witness. t-1122 gets one line: builder-rules is being dissolved and the home is RUNBOOK §9.8 or what t-1122 names. Write one line into 20261116 (its Lead-edits section): "L1, L2, L4, L5 superseded by t-1117 F6 (a); L3 lands as C3's designer edit". Close or annotate the node that carries them. Add the §4.1/§4.2 source paragraphs to C3's given and `24. The plan gate`, `Q13` to its DoD keys.

### Fixes to the spec text

**M1. Rule-number collision risk stated as an invariant.** Rule 24 is free only while 20261116 L2 has not run. Add the invariant "critic.md rules 21-24 are assigned by t-1117; no other spec appends a critic rule until it lands" next to E12.

**M2. The §9 row "CLAUDE.md incl. imports | 50 808 … CLAUDE_WARN 58 500" mixes two measures.** 50808 is CLAUDE.md alone, and that is what CLAUDE_WARN compares (`session_context.py:1312-1319`). With its imports it is 98899. The row also adds PROJECT.md's +1200 to the CLAUDE.md-alone cap. Split the row: CLAUDE.md alone 50808 → about 51.4K against 58500; boot total about 111.7K against WARN/BREACH.

**M3. §6 and Q4 do not say the same thing, and §6 is not exactly the owner's word.**
- (a) Q4 is kept "verbatim up to '(say which)'", so it still opens with "a sibling neither fixed nor queued is a finding" (brief :32), while critic.md rule 5 and CLAUDE.md rule 9 drop "queued". This is the same class inside the same artifact (sweep-the-artifact-first).
- (b) CLAUDE.md rule 9's new text allows only "a node with an executor in another pile". Q4 and TEAMWORK §9 (:23-25) also keep `перенос: … | подтвердил:` and the "waits for an owner's decision" exit. Rule 9 is narrower than its own owners.
- (c) "never a way to defer a rule fix while rules are being fixed" and «замечание по правилам, когда чиним правила, — тоже» are wider than the quoted words («можно отложить в чужую кучку, но это должен быть редкий случай»). Quote their carrier or drop them.
- (d) The sweep leaves "queue it instead" (rule 9 sweep paragraph) and rule 10 (b)'s "covered / queued / n/a". Enumerate them: change the first; mark the second "n/a — mechanism axes, grammar parsed by mechanism_gate" or decide otherwise.
- **Fix:** one wording used in all four places: CLAUDE.md rule 9, PROJECT.md п. 9, critic.md rule 5, Q4.

**M4. One list of main documents, not three.**
- §2 lists OWNER_PRINCIPLES, TWO_VOCABULARIES, delegation.config.yaml, DELEGATION_TABLE, SYSTEM_PROMPT, BOOT.md and design/.
- The §8 rule text lists fewer.
- K-NOBRIEF MAIN lists fewer again: no BOOT.md, SYSTEM_PROMPT.md, OWNER_PRINCIPLES, design/.
- «строкой этой таблицы» points at a table that is neither of these lists.
- This is a second road for one fact (P31, AR-13).
- **Fix:** one register, either the axis-31 owner column of SIBLING_MAP or an explicit list inside the §8 paragraph. K-NOBRIEF's MAIN is read from it, or names it in a comment with a K-PTR row. The «Где что лежит» table gets the missing main rows, or the rule stops calling that table the register. Make the "Не лишние" list open ("one task, one moment, or a record — e.g. …") and include plans of one task, retro inbox entries, exam run logs and experiment notebooks.

**M5. The generator of briefs is left in place.**
- `plans/piles/_template/batch.md:16` «Общий бриф дизайнерам: <путь к файлу или 3–5 строк …>» invites a brief FILE. That is how `pre-release-0.9-brief-common.md` was born.
- `piles.py:1934` requires `## Бриф` in every untaken batch; the card template has `## Бриф пачки 1`.
- **Fix:** template line 16 → "a spec path, or 3-5 lines inline; never a separate standing file (PROJECT.md «Лишних документов нет»)". Mark the `## Бриф` sections in §2 explicitly as "per-batch text, not extra". Whether «избавиться от всех брифов» also means renaming these sections is the owner's intent: one question to the owner (CLAUDE.md 11a). It can go in wave 2.

**M6. F5 (a) breaks DECISIONS.md's header.** DECISIONS.md:8-13: "a line is never edited … with one move allowed: … MOVED whole to the archive … an over-long line is trimmed here to its operative statement with its full text kept there". Appending a clause to D-0033 is an edit. **Fix:** use the trim move. D-0033 keeps its operative part (the ratchet is a merge gate in forge-check). "every builder's witness carries --check … (docs/tasks/critic-diff-brief.md …)" goes, with the full text kept in DECISIONS_ARCHIVE, and D-0033 is added to the header's "trimmed" list.

**M7. N7's reader list is incomplete; draft N7 as wave 2.** Readers of `docs/tasks/exchange-form.md` beyond §4.7:
- `tools/test_handoff_rule_anchors.py:151` (`K_SCOUT_FORM` pins the path inside scout rule 10)
- `tools/test_digest_form.py:5, :26, :69, :118-119, :671`
- `tools/handback_extract.py:37`
- `gateway/PI_HARNESS.md:58` ("read it first")
- SIBLING_MAP :35, :506
- WEEKLY_CALIBRATION check 34's "brief form" metric (its §2)

N7 touches CLAUDE.md and SIBLING_MAP, which are L's files.

**M8. The spec's own §11 C1 DoD key "rule 21" in TESTING.md is ambiguous.** TESTING.md has numbered lists of its own (e.g. «Когда тест покраснел» 1-4). **Fix:** use the exact pointer text `.claude/agents/critic.md` rule 21 as the key.

**M9. §10 misses the C2 file list's own reader `tools/test_owns_readers.py`.** The DoD runs it, but no test pins owns_readers' docstring line :26. Say so ("docstring only; no test reads it"), or name the test that does.

### Minor

- **m1.** Clauses of builder-rules dropped without a row in §4.2 (name each "dropped — why", or home it):
  - 5: «Файлы phases/ без потолка, но оркестратор читает их каждый прогон — добавлять кратко»
  - 7a: «лучше запускать его синхронно»
  - 11: «текст для SKILL.md — строки < 200 байт, запаса нет» (obsolete if F7 drops the integrator list; say so)
  - 13: «рапорт называет цикл, оставленный позади»
  - 8: the note «роль сама waiver не запускает … слово записывает оркестратор»
  - 20: «пустой tasks/*.output не значит потерянный отчёт» (RUNBOOK §12 covers the scout case :649 and the lost hand-back case :619-621, not the empty-output case)
  - builder.md rule 4: "no new test file is written without a keep row (7d)" is cut from the new text. Present in substance in builder.md rule 8 and TESTING «Бюджет»; name it.
- **m2.** See M2 (label).
- **m3.** Q12(c) makes `docs/tasks/specs/reports/t-2046-language-exceptions-census.md` a standing read from a main document, which is exactly what check 33 (i) will flag. Name it as a data ledger (like a ratchet file) in the rule, or move it.
- **m4.** `experiments/measurers/prepare_copy.py:195` cites "builder-rules 10"; `docs/FINDINGS.md:96` and `plans/BACKLOG.md` are records. Add prepare_copy.py to §10 or the queued comment list (B1).
- **m5.** A stale worktree `.claude/worktrees/agent-ac59fdf8d182e6ef9` (base 933b7f97) holds uncommitted edits of critic.md, builder.md and designer.md that main already carries (the 4+N hand-back form). It is not a running builder by the journal scan, but a careless resume would reintroduce old role text. The Lead may remove it at the wave cleanup.
- **m6.** K-TESTPTR and K-NOBRIEF are rows of an existing parameterised file. That is consistent with TESTING.md «Правила ролей не теряются» for the forge's axis-31 table. Not a finding; noted for the code critic so Q5 (f) is not misapplied.

## Not established

- Whether any pile node row (other than TBW1-14, FG7-51, FV2-14) carries 20261116's Lead edits L1-L5. I found no node id for them in forge/7; a scout or the Lead's own grep of `plans/piles/*/batch-*.md` for "t-897|spec facts" settles it.
- Whether RUNBOOK §9.6 carries "live project read-only" for the night agent. My Grep for «только чтени|read-only|копи» found no clear line in §9.6; the spec already lists this.
- Whether `tools/test_split.py`'s printed carrier line is pinned elsewhere (C2 duty, as the spec says).
- The exact byte size of critic.md after the fold (estimate about 22K = 10981 + about 11K of the brief).

## Trail

Read whole:
- the spec (688 lines)
- `docs/tasks/critic-diff-brief.md` (126)
- `plans/builder-rules.md` (136)
- `.claude/agents/critic.md` (178)
- `.claude/agents/builder.md` (101)

Read in part:
- `.claude/agents/scout.md` :80-109
- `tools/tests/test_role_carriers_one_owner.py` :1-254
- `tools/test_handoff_rule_anchors.py` :60-173
- `tools/test_quarantine.py` :40-69, :205-244, :1325-1364
- `ai-packages/qa-factory/scripts/selftest.py` :715-749
- `tools/install_parity.py` :527-601
- `tools/session_context.py` :1305-1379
- `docs/TESTING.md` :131-142 plus headings
- `.github/workflows/forge-check.yml` :80-104
- `DECISIONS.md` :1-19, :32
- `tools/test_dispatch_manifest.py` :826-855
- `tools/critic_verdict.schema.json`
- `docs/tasks/specs/20261116-spec-facts-by-code-spec.md` (headings, §4, the Lead-edits section by grep)
- batch headers forge/7, told-before-work/1, live-run-fvf/2
- `plans/piles/_template/batch.md` (grep)

Commands (outputs summarised; verbatim numbers quoted above):
- `git rev-parse HEAD origin/main` → both b89871b3
- `git grep -n -i -E "Q13|plan gate|rule 24" origin/main -- critic.md designer.md` → 1 hit (critic.md:163 rule 19)
- `git grep -n -i -E "critic-diff-brief|builder-rules|test-diet-brief|test-diet-fold-brief|pre-release-0\.9-…|exchange-form" HEAD` minus records → 30 KB of hits; positive control in the same call: CLAUDE.md:31/35 found
- the E4 measurement script (python, `test_[a-z0-9_]+\.py` over builder-rules vs lines 26-71 vs other carriers) → lost: ['test_arch_check.py']
- `grep '"gate_named"'` and `named_by` in selftest.py / test_quarantine.py → no layer check, only non-empty named_by (selftest.py:629)
- `grep dev:` in architecture_index.py / architecture_gate.py → no resolver; `git grep -c "dev:"` architecture.md → 32
- `wc -c` CLAUDE.md, imports, role files, TESTING, briefs → numbers in K4
- grep `BOOT_WARN_THRESHOLD` over tools/, .githooks/, workflows → only session_context.py and its tests
- `ls PROCESS/` → 12 files, no CRITIC_EXAM.md
- `git log -1 1f165a38` → the exam-deviation precedent exists
- journal scan (python over logs/journal/dev1.jsonl) → open dispatches since 08:00 listed in B3; t-897 accepted 00:15, t-913 accepted 00:46, t-917 merged 21c3ec90
- grep in PROTOCOL → check 33 sub-items (a)-(h)
- `grep "test:|expected from"` in dispatch_manifest/dispatch_new/dod_gate → 0; control "given" in dispatch_manifest → 14
- `git grep -i "integrator[-_ ]only|INTEGRATOR_(FILES|PATHS|ONLY)|only the integrator"` → 0; control `-c integrator` → tools/piles.py 4
- worktree scan for uncommitted edits of the moved files → one stale worktree (m5)

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "B1: C2 E4 subset check fails (test_arch_check.py named only by builder-rules item 14); package readers missed: design/architecture.md:144 AR-29 carrier and :223, test-layers.json rows test_arch_check.py / test_probe_by_code_copy.py / test_story_step.py; section 1 claim that the package is untouched is false",
    "B2: convergence for C2 not buildable: C3 mechanism files staged-only in a worktree, L1 draft uncommitted, C1 committed on its own branch; Lead must commit C3 and L1 on a named batch branch before C2; E1 restated as one merge",
    "B3: window under open dispatches (critics read the main tree, t-1122 picks the home of builder-rules 13) and under spec 20261116 Lead edits L1-L5 (L2 would take critic.md rule 21); C3 card lacks the F6 (a) Q13 source and DoD keys"
  ],
  "fixes": [
    "M1 invariant: critic.md rules 21-24 assigned by t-1117",
    "M2 split the budget row: CLAUDE.md alone 50808 vs 58500; with imports 98899; boot total vs WARN/BREACH",
    "M3 one wording for rule 9, PROJECT p.9, critic rule 5 and Q4: drop neither-fixed-nor-queued in Q4, keep the perenos form and the owner-decision exit, quote or drop the rules-while-fixing-rules clause, enumerate queue-it-instead and rule 10 (b)",
    "M4 one register of main documents read by the rule text and K-NOBRIEF MAIN; open the not-extra list",
    "M5 pile template batch.md:16 must not invite a brief file; name the batch Brief sections in section 2; owner question on renaming them",
    "M6 F5 via the DECISIONS.md trim move, not an in-place clause",
    "M7 N7 readers: test_handoff_rule_anchors K_SCOUT_FORM, test_digest_form 5/26/69/118/671, handback_extract.py:37, gateway/PI_HARNESS.md:58, SIBLING_MAP 35/506, check 34; land N7 as wave 2",
    "M8 C1 DoD key rule 21 written as the exact pointer text",
    "M9 state that no test reads the owns_readers docstring",
    "m1 name the six dropped builder-rules clauses and the dropped keep-row clause of builder.md rule 4"
  ],
  "class_completeness": "Same artifact: Q4 first sentence and the rule 9 sweep words left out of the section 6 sweep (M3). Map axis 31: three lists of main documents (M4). The generator class (pile template brief line) not covered (M5). Package side of the readers walk missed (B1); the package comment citations of builder-rules N to be queued with the F9 finding.",
  "trail": {
    "read": [
      "docs/tasks/specs/20261117-no-briefs-fold-into-roles-spec.md",
      "docs/tasks/critic-diff-brief.md",
      "plans/builder-rules.md",
      ".claude/agents/critic.md",
      ".claude/agents/builder.md",
      ".claude/agents/scout.md:80-109",
      "tools/tests/test_role_carriers_one_owner.py",
      "tools/test_handoff_rule_anchors.py:60-173",
      "tools/test_quarantine.py:40-69,205-244,1325-1364",
      "ai-packages/qa-factory/scripts/selftest.py:715-749",
      "tools/install_parity.py:527-601",
      "tools/session_context.py:1305-1379",
      "docs/TESTING.md:131-142",
      ".github/workflows/forge-check.yml:80-104",
      "DECISIONS.md:1-19,32",
      "docs/tasks/specs/20261116-spec-facts-by-code-spec.md (section 4 and Lead edits by grep)",
      "tools/critic_verdict.schema.json"
    ],
    "reruns": [
      {"command": "git rev-parse HEAD origin/main", "result": "b89871b3 both"},
      {"command": "git grep -n -i -E 'Q13|plan gate|rule 24' origin/main -- .claude/agents/critic.md .claude/agents/designer.md", "result": "1 hit, critic.md:163 rule 19 only"},
      {"command": "python E4 measurement over plans/builder-rules.md with test_[a-z0-9_]+.py", "result": "lost: test_arch_check.py"},
      {"command": "wc -c CLAUDE.md PROJECT.md indexes role files TESTING.md", "result": "CLAUDE.md 50808; with imports 98899; critic.md 10981; builder.md 6239"},
      {"command": "grep pytest .github/workflows/forge-check.yml", "result": "96: python -m pytest tools/ -q"},
      {"command": "ls PROCESS/", "result": "12 files, no CRITIC_EXAM.md"}
    ]
  }
}
```
