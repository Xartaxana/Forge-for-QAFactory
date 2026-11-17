# t-1124: plan review of the no-briefs spec (t-1117)

Spec reviewed: `docs/tasks/specs/20261117-no-briefs-fold-into-roles-spec.md` (688 lines), read in full, including «Lead decisions» and «Lead decisions on the forks».
Tree: root HEAD `b89871b3`, which equals `origin/main` (`git log -1 origin/main`).
Critic: opus, 17.11.2026.

**Verdict: READY WITH FIXES (NEEDS WORK). 7 findings block code (B1-B7); 12 fixes are non-blocking (F1-F12).** Every fix below says what to change. The plan holds up overall: the critic brief folds verbatim, TESTING.md stays the main document, and the pins are designed. What fails: one card cannot go green in the order given; the package readers were missed; and two forks the Lead decided "in" (F4, F6) have no texts.

---

## Blocking findings

**B1. C2 cannot go green in the order the plan gives (K9).**
- §11 order: C1 ∥ C3 ∥ L1-draft → C2 → L2. L2 runs the `git rm` of the six files.
- C2's DoD runs `test_role_carriers_one_owner.py` "on the converged tree", and that tree still holds the six files. So K-NOBRIEF (2), "none of the six DELETED paths is tracked", is red.
- OWNER_KEYS also go red. C3 copies Q6/Q7/Q12 verbatim into critic.md while the brief still holds them, so the keys `review:critic` and `review:one-road` occur in two scanned files. The same happens to `scope:builder` (TESTING.md and builder-rules).
- The plan never says how the uncommitted L1-draft (CLAUDE.md, a mechanism path) gets into C2's worktree. The K-TESTPTR CLAUDE.md row needs it there.
- E1 claims "ONE commit", but C1 commits on its own branch.
- **Fix:**
  - Move the `git rm` of the six files into C2's owns. None of them is a mechanism path (`tools/mechanism_gate.py:215-276`).
  - The Lead commits L1-draft on the batch branch, with `tier: opus` and the axis block, before C2.
  - C2 gets a worktree that the coordinator cuts from that branch, and is dispatched without isolation (RUNBOOK §12 item 8).
  - Restate E1 as: "main receives the batch as one `wave.py merge`; no first-parent state of main has a pointer to a missing file".
  - Add a temporal edge (CLAUDE.md rule 11 (i)): `test_role_carriers_one_owner.py` is expected red on the branch between C1/C3 and C2, and it is in no witness before C2.

**B2. The C3 witness checks the wrong tree (K9).**
- The C3 DoD runs `python -m pytest C:/QAFactory/forge-repo/tools/test_handoff_rule_anchors.py`.
- That test resolves `REAL = pathlib.Path(__file__).resolve().parent.parent` (`tools/test_handoff_rule_anchors.py:20`). Given the main-clone path, it reads main's critic.md, not the worktree's edits.
- Its clause "green except the two rows C2 rewrites" is also wrong: at C3 time the brief and builder-rules still exist, so `test_brief_what_comes_back` and `test_builder_rules_p11` pass.
- **Fix:** make the DoD `( cd <C3 worktree root> && python -m pytest tools/test_handoff_rule_anchors.py -q )`, all green.

**B3. Package readers missed; "the package is NOT edited" (§1) is false (K3).**
`git grep -E "builder-rules|critic-diff-brief" -- ai-packages` finds:
- `design/architecture.md:64, :122, :144, :222, :223`.
  - :144 is the AR-29 carrier: `dev:docs/tasks/critic-diff-brief.md` question 11. CLAUDE.md rule 10 ties it to axis 1: "This paragraph, critic question 11 and designer rule 1 change together".
  - :222 says "critic-diff-brief question 9".
  - :64 and :122 point at builder-rules rules 1, 9 and 5.
- `scripts/tests/test-layers.json`: 7 `why`/`named_by` values name `plans/builder-rules.md`, at lines 89, 171, 793, 1392, 3727, 6310, 6350-6353.
- About 36 package `.py` files carry comments citing "builder-rules 9" (in-flight compatibility), "7a" or "5".
  - Examples: `acceptance.py:1206`, `controller.py:2991`, `proof_level.py:465`, `test_report_texts.py:26`.
  - Count: `grep -rc ... --include=*.py | grep -v :0 | wc -l` → 36.

`design/` is a main document under §2 and §8, yet K-NOBRIEF's MAIN set leaves it out (see B6).

**Fix:** add a package card (or widen C2) with owns `ai-packages/qa-factory/design/architecture.md` and `ai-packages/qa-factory/scripts/tests/test-layers.json`.
- architecture.md: :144 → `dev:.claude/agents/critic.md` rule 22 Q11; :222 → critic.md rule 22 Q9; :64 → `dev:.claude/agents/builder.md` rules 4 and 11; :122 → builder.md rule 11; :223 → `dev:docs/TESTING.md` «Что запускать по своей правке».
- test-layers.json: each `why`/`named_by` gets its new carrier; for test_arch_check see B4.
- The commit carries `architecture: AR-29 -- carrier pointer re-pointed, invariant unchanged` and `judgment: none -- pointers only`. Run `selftest.py --lang`.
- The `.py` comments: one Lead decision line in the spec. Recommended: leave them as history (E5) and add one line to builder.md rule 11: «"builder-rules N" in package comments = this rule's former numbering: 1, 9 → rule 11; 5 → rule 11; 7a → rule 9». An alternative is to re-point them under F9's package finding.

**B4. Edge E4 is broken by the plan itself (K1, K3).** Measured by running `selftest.gate_named_files` on today's tree:
- OLD extra texts: SIBLING_MAP + protocol + builder-rules.
- NEW extra texts: SIBLING_MAP + protocol + TESTING.md + the moved 7b/7c text.
- Result: `lost ['test_arch_check.py']`, `gained []`.
- `test_arch_check.py` is a keep row with `layer: gate_named` and `why: "named by plans/builder-rules.md:71 (a history or example line ...)"` (test-layers.json:89). Only item 14's anecdote names it, and builder.md rule 4 drops the file name.
- C2's DoD, "the old set must be a subset of the new", will fail.
- **Fix (a Lead decision):**
  - (a), recommended: re-layer the keep row honestly. Its layer and why were a by-product of an example line. Choose its real layer (it `covers` arch_check.py, detectors.json) or quarantine it, in the B3 package card. Then E4 reads "subset, minus test_arch_check.py (re-layered, named)".
  - (b) Keep the name in TESTING.md.

**B5. Live untaken batch rows missed (K3, E3).** §10 lists only TBW1-14, FG7-51 and FV2-14. Also «ожидает» (untaken, editable by the Lead):
- `plans/piles/onboarding-hooks/batch-9-perepis-podklassov-oh8-7b-h.md:25` (OH9-1) and `:31` (OH9-7): owns name `docs/tasks/critic-diff-brief.md` (questions 9, 11).
- `plans/piles/package-ci/batch-4-dieta-testov-td-11-td-15.md:27` (PC4-6): a node whose job is to WRITE a note into `plans/builder-rules.md` п. 7c, and whose owns name that file.
- `plans/piles/release-next/batch-2-one-bug-many-manifestations.md:12`: «Общий бриф дизайнерам: ... `plans/builder-rules.md`».

**Fix:** add these rows to §10 and to L1. The new targets are critic.md rule 22 (Q9, Q11), the TESTING section (PC4-6's note lands there), and the TESTING section / builder.md, respectively.

**B6. K-NOBRIEF has a false-green class the plan does not name (K5, E8).**
- FORBIDDEN matches only path forms (`docs/tasks/...brief....md`, `plans/builder-rules.md`). Short forms pass: `critic-diff-brief question 9` (architecture.md:222), `(builder-rules п. 13)` (RUNBOOK §9.8), `builder-rules 7b` (test_language_sites.py:4).
- MAIN leaves out `ai-packages/qa-factory/design/*.md`, although §2 and §8 call design/ main. Running the regex over design/ finds architecture.md 64, 122, 144, 223.
- E8's invariant, "a MAIN pointer to a brief is always red", is therefore false as designed.
- **Fix:**
  - FORBIDDEN gains the bare names `critic-diff-brief` and `builder-rules`, case-folded.
  - MAIN gains `ai-packages/qa-factory/design/*.md`.
  - Adversarial rows gain `builder-rules 7b` in a MAIN file → red.

**B7. F4 and F6 are decided "in" but have no texts (K10, K11).**
- §4.7 ends "N7 is drafted after the Lead's answer". The Lead answered (a), but there is no N7 card, no exact texts and no owns.
- `tools/test_handoff_rule_anchors.py:123-130` pins `docs/tasks/exchange-form.md` in scout.md rule 10 (`K_SCOUT_FORM`). §10 does not list it.
- F6 (a) has no rule 24 text, no designer-line rewrite, no POINTERS row and no TESTING-section sentence for stream L's L5.
- `tools/owns_readers.py:55` already claims "TWO QUESTIONS, TWO ANSWERS (spec section 2.7; plans/builder-rules.md 7b)". The split is in neither builder-rules (Read: 7b has no `owns_readers`) nor TESTING.md. So the re-pointed docstring would point at absent text.
- **Fix:** a designer fix round adds, as exact texts:
  - N7 as a card: scout.md rule 10/12 text, the fixture move to `tools/fixtures/digest_form/t-794.md` with the `test_digest_form.py` reader line, CLAUDE.md rule 11 sentences, and the `K_SCOUT_FORM` update.
  - critic.md rule 24 «The plan gate»: Q13 verbatim from spec 20261116 §4.1, with "items 4 and 12" → "Q4 and Q12", plus Q13 (e) "challenge the Lead's fork decisions" worded.
  - designer.md rule 3, the stream-L line with "critic.md rule 24 Q13 (d)".
  - POINTERS row `(".claude/agents/designer.md", "critic.md rule 24 Q13 (d)", CRITIC, "Q13. **FACTS AND EDGES**")`.
  - One Russian sentence in «Что запускать по своей правке» stating the split (`--witness-for` answers WHAT TO RUN; `owns_readers` answers WHAT MUST NOT BREAK).
  - A Lead decision line appended to spec 20261116: «L1, L2, L3, L4, L5 superseded by t-1117 (critic.md rule 24, designer rule 3, TESTING section); stream L does not write rule 21». Rule 21 is taken by «two layers» here, so stream L's planned rule 21 would collide.

---

## Non-blocking fixes (each is fixed in this round)

- **F1 (K8, D1). Wrong holder; F5 (a) breaks the record's own rule.**
  - The refinement of D-0033 is D-0057 ("D-0033 refined: ... a builder's witness no longer carries `--check`"). It sits in `docs/DECISIONS_ARCHIVE.md:144-145`, not D-0056.
  - The DECISIONS.md header says "a line is never edited". The only allowed moves are archiving a line whole or trimming it.
  - Fix:
    - §4.1 P2: "D-0033 as refined by the Lead" → "D-0057".
    - F5 becomes: the Lead TRIMS D-0033 to its operative statement, dropping the superseded witness clause and the brief pointer (full text is already in the archive), and adds D-0033 to the header's "trimmed" list.
- **F2 (K1). Losses in §4.2.3's texts.** Add the following.
  - Item 18: builder.md rule 10 + "no `git -c core.hooksPath` workaround is needed: `wiring_check.py` accepts the main checkout's `core.hooksPath`". RUNBOOK §12:617 says quirks 1, 5 and 6 "live in builder-rules п. 18".
  - Item 20, the coordinator half: "an empty `tasks/*.output` is not a lost report; extract with `python tools/handback_extract.py --agent <id> <path>`". RUNBOOK §12 item 2 says only "transcribe by hand" and names a non-existent `extract_handback.py` (`ls tools/extract_handback.py` → no such file). C1 rewrites item 2 with the right tool and the `--agent` form.
  - Item 11: "text for SKILL.md: lines under 200 bytes" in rule 4's «Needed from integration».
  - Item 7a: "a polling wait lasts no longer than the run itself; prefer running it synchronously" in rule 9.
  - Item 16 (а): "`Grep` instead of reading a whole file" in the CLAUDE.md Cost-gates sentence.
  - Item 13: "the report names any loop left behind". It can wait for t-1122's home, as the Lead decided; then say so in §4.2's item 13 row.
- **F3 (K8, new D10). An unlisted divergence moves forward.** 7a says "after an edit run only the test file of the changed module". 16 (б) says "re-running after each edit is a violation; ONE run after all edits". The proposed rule 9 plus the Cost-gates sentence carry both. Fix: one Lead line choosing the holder. Recommended wording for rule 9: "while working, at most the changed module's test file, and not after every edit".
- **F4 (K6). The criterion in rules 5, 9 and Q4 is out of line.**
  - Q4 lets an analog leave the round for TWO reasons: "ANOTHER pile's zone, or one that waits for an owner's decision". Rule 9's new text and critic.md rule 5 allow one, and say "outside the work's context", which a weaker model cannot decide.
  - The sweep paragraph keeps "queue it instead".
  - Fix: one wording in all three, "in another pile's zone, or waiting for the owner's word (named), as a node with an executor"; and "queue it instead" → "move it to another pile's node (the rare case)".
  - PROJECT п. 9's text is faithful to the owner's word, and TEAMWORK §9's line forms stay consistent with it.
- **F5 (K5). The border is three lists that disagree.**
  - §2's main-document list, §8's PROJECT text and K-NOBRIEF's MAIN differ. For example, §8 leaves out OWNER_PRINCIPLES, TWO_VOCABULARIES, BOOT, SYSTEM_PROMPT, delegation.config and DELEGATION_TABLE.
  - The axis-31 table (SIBLING_MAP:482-515), from which §2 claims to "derive" the list, has no `docs/TESTING.md` row and no skills row.
  - PROJECT's «Где что лежит» table, which §8 makes the registry ("строкой этой таблицы"), has no TESTING.md row and mixes records (BACKLOG, MEASUREMENTS, provenance).
  - §8's sentence «Документа, который роль читает всегда сверх своего файла и бута, нет» is literally false of TESTING.md.
  - Fix:
    - One list: the axis-31 table gains rows `docs/TESTING.md` and `.claude/skills/*/SKILL.md`, and §8's paragraph points to it instead of re-listing.
    - Reword to «документа вне основных, который роль обязана читать, нет».
    - «Не лишние» gains «запись (журнал решений, реестр, архив), шаблон, план одной задачи, раздел «Бриф» пачки или карточки».
    - PROJECT's map gains a TESTING.md row.
- **F6 (K2). Inventory misses.**
  - `plans/piles/_template/batch.md:16`: «Общий бриф дизайнерам: <путь к файлу или 3–5 строк ...>» invites a brief FILE, which is exactly the class this spec forbids. Fix: drop «путь к файлу или». Neighbours: the `## Бриф` heading that `tools/piles.py:1934` requires and the card's «Бриф пачки 1` section are per-batch sections, so they are allowed; name them in §2.
  - `docs/retro/README.md`: the weekly-reduction procedure, pointed to by session-retro SKILL.md:13 and :42. It is a standing procedure outside the main list and needs a class line, either main (axis-31 row) or folded into the skill.
  - Unlisted but harmless; give each a class line:
    - `docs/tasks/specs/fg-context-and-hygiene-lead-brief.md` (a spec-folder intent brief);
    - `plans/RULES-PROPOSAL.md`, `plans/forge-metrics.md`, `plans/project-knowledge-plan.md`, `plans/thinking-roles-portable-to-main.md` (records, plans, generated);
    - `docs/RELATED_WORK.md` (a record).
  - §2 says an intent brief is "a word, not a file", while two `*-lead-brief.md` files exist under specs. State that a file under `docs/tasks/specs/` is legal.
- **F7 (K3). Small readers missed.**
  - `experiments/measurers/prepare_copy.py:195` "(builder-rules 10)" → "builder.md rule 11".
  - `plans/feature-fragility-2026-10-02.md:482`: a record; name it as not edited.
  - SIBLING_MAP line numbers drifted by +1 (the regex finds 402, 479-480, 490-491, 508-509, 578, 603, against the spec's 401, 478-479, ...). L1 should grep by name, not by line.
- **F8 (K4). TESTING.md texts.**
  - :229 should read «Критик: вопрос 5 (`.claude/agents/critic.md` правило 22 Q5) и правило 21», not rule 21 alone.
  - Inside the moved 7b, «`docs/TESTING.md` «Тест может упасть»» becomes «раздел «Тест может упасть» ниже» (a self-reference in its own file).
- **F9 (K7). §9's table is mislabelled.**
  - The row "CLAUDE.md incl. imports 50 808 → ~52 600, ceiling CLAUDE_WARN 58 500" is wrong. 50 808 is CLAUDE.md's OWN bytes. CLAUDE_WARN compares own bytes (`tools/session_context.py:1313-1321`). Including imports, it is 98 899 (the BOOT BUDGET line).
  - Measured deltas of the spec's own texts (UTF-8 bytes): §8 paragraph +1 029, п. 9 +361, map row −129, rule 9 +236, Cost gates +180, rule 4 +49.
  - Corrected rows:
    - CLAUDE.md own: 50 808 → ~51 400 (without N7), ~51 800 (with N7's +400). Limit 58 500, not crossed.
    - Boot total: 109 921 → ~111 900 (~112 300 with N7). WARN 110 000 crossed by about 1.9-2.3 K, which F3 already accepted. BREACH 120 000 not crossed.
  - No test pins the size of `.claude/agents/*.md`; role-load.json guards package roles only (confirmed).
- **F10 (K11). "Not established", resolved here; strike these from the list.**
  - CI runs `tools/tests/`: `.github/workflows/forge-check.yml:96`, `python -m pytest tools/ -q`.
  - Kit side of install_parity: there is no `toolkit/` tree (`ls` → none). `test_install_parity.py:40` uses `TOOLKIT_ROOT = HERE.parent` (the repo itself). The CLAUDE.md anchor change and the JSON change must land together, as C2 plans.
  - test_split's printed line: no other carrier (grep `carrier search (spec 2.7)` → test_split.py only).
  - `SCAN_ROOT = "scripts"` (test_judgment_census.py:74), so the forge pins are outside the census.
  - RUNBOOK §9.6 has «живое дерево проекта не трогается».
  - The integrator-only list (F7 of the spec) is enforced nowhere: grep in tools → 0, with `owns_gate.py` as the positive control (33 defs).
- **F11 (K9). Small card items.**
  - §2 calls `docs/*_FULL.md` frozen while C1 edits `CLAUDE_HOST_ADAPTATIONS_FULL.md`. Add the carve-out: it keeps live "where it stands now" pointers.
  - C3's `given` should name the three role files as absolute paths.
- **F12 (rule 18, DUPLICATION).** Covered by F5: three lists of main documents.

---

## Answers per key

- **K1. Fails** (B4; F2 items 18, 20, 11, 7a, 16а, 13).
  - Checked present and holding: P1 (critic.md rule 18 and CLAUDE.md rule 3); item 8 (FR-4 + FR-3, factory-rules.md:46-56); item 16 (в) (`agent_budget.stop_message`, :254-262); item 19 (gate text, `architecture_gate.py:16-38, :150-159`); item 7's size cap (TESTING.md:137); Q4's line forms (TEAMWORK.md:22-25); TESTING :219 key.
  - One-off briefs §4.3-§4.6: the rows hold. The "one mutation → one test" row diverges and is correctly dropped (TESTING.md:91-94).
- **K2. Fails** (F6).
- **K3. Fails** (B3, B5, B7 test pin, F7).
- **K4. Holds with F8.** Pointers: builder, critic, designer and CLAUDE.md rule 4 get them. The scout correctly gets none. The new section is consistent with CLAUDE.md rule 4's witness scope and with «Тест может упасть». D7 confirmed: grep `expected from` in dispatch tools → 0, control → 4.
- **K5. Fails** (B6, F5).
  - Detector: check 33 (i) is free (check 33 ends at (h), protocol :1045).
  - Execution path: the pin runs on CI (forge-check :96).
  - The "on discipline" line names check 33 (i). That holds once B6 closes the bare-name hole.
- **K6. Holds with F4.** PROJECT п. 9 is faithful; TEAMWORK §9 is consistent. Rule 9, rule 5 and Q4 need one shared criterion.
- **K7. Holds with F9.** WARN is crossed by about 2 K (accepted by F3). No limit is breached. No raise is needed.
- **K8.** Holds: D2, D3, D4, D5, D6, D7, D9. Fails: D1 (F1). Missing: D10 (F3).
- **K9. Fails** (B1, B2).
  - Owns are disjoint.
  - Mechanism paths are staged for the Lead. test_quarantine.py and dispatch_gate.py are in `MECHANISM_PREFIXES`.
  - No enforcement file goes live from a builder: the C2 comment edit sits in its worktree and the Lead commits it.
- **K10. (a) absorb.**
  - Spec 20261116 is accepted text: plan critic t-904, fix round t-913, and `accepted` t-897 `by: fable` (dev1.jsonl:2214); S1 was implemented (t-917, accepted :2316).
  - Its L1/L2 have NOT landed. critic.md was last touched at 81b0e635, and `git log --all --since=2026-11-16` on the brief and critic.md shows no FACTS AND EDGES; the brief has 0 hits for "FACTS AND EDGES".
  - So join it here as rule 24, with no double (B7).
- **K11.** Must be settled before code: B4's re-layer decision, F3's holder, and B3's decision on package comments. The rest are resolved by F10.

**Standing lines.**
- **DUPLICATION AND CONSISTENCY:** F5/F12. Found by reading §2, §8, the K-NOBRIEF MAIN list, SIBLING_MAP:482-515 and the PROJECT map.
- **CODE QUALITY:** none found. This is a plan; I read the K-NOBRIEF and K-TESTPTR designs and the C2 transformations.
- **ONE ROAD:** B6. MAIN leaves out the package's design/ from the shared pin with no data row and no owner's word. Fix this round.
- **TESTS:** new rows go into an existing file (TESTING «Бюджет / Файлы» holds). The negative-control deletions are justified by «Что не пишется». `tests-over:` is not expected: the pin rows are smaller than the deleted tests.

## Trail

- **Read:**
  - the spec, whole;
  - `plans/builder-rules.md` (136 lines);
  - `docs/tasks/critic-diff-brief.md` (125);
  - `.claude/agents/designer.md` :15-46 and `builder.md` :39-56, :88-100;
  - `docs/TESTING.md` :60-105, :118-140, :165-172, :212-234 and its headings;
  - `docs/TEAMWORK.md` :1-32;
  - `docs/SIBLING_MAP.md` :470-520;
  - `docs/RUNBOOK.md` :366-402, :614-653;
  - `docs/CLAUDE_HOST_ADAPTATIONS_FULL.md` :1-10, :33;
  - `tools/test_handoff_rule_anchors.py` (all);
  - `tools/tests/test_role_carriers_one_owner.py` :1-130;
  - `tools/test_quarantine.py` :40-62, :1125-1140, :1335-1365, :2190-2210;
  - `selftest.py` :721-736;
  - `tools/session_context.py` :204-235, :1300-1330;
  - `tools/agent_budget.py` :250-262;
  - `tools/mechanism_gate.py` :215-276;
  - `factory-rules.md` :38-60;
  - spec 20261116 :408-482, :621-660, :690-730, :795-872;
  - DECISIONS.md :1-20, :32;
  - DECISIONS_ARCHIVE :144-145;
  - the batch headers listed in B5;
  - `tools/critic_verdict.schema.json`.
- **Runs, with verbatim results:**
  - `python -B tools/session_context.py | grep "BOOT BUDGET"` → `BOOT BUDGET: 109921 bytes / 120000 (4 files + 4 imports) | CLAUDE.md: 50808/58500 incl. imports 98899`.
  - `wc -c` → CLAUDE.md 50808, PROJECT.md 34622, critic.md 10981, builder.md 6239, designer.md 7495, TESTING.md 32159.
  - The E4 simulation through `selftest.gate_named_files` → `lost ['test_arch_check.py'] gained []`.
  - The K-NOBRIEF regex over MAIN + design → CLAUDE.md [31, 35, 127, 154], PROJECT.md [45, 75, 79, 80, 237], TESTING.md [65, 89, 102, 123, 170, 228, 229], RUNBOOK [125, 218, 380, 617, 630], SIBLING_MAP [34, 95, 402, 479, 480, 490, 491, 508, 509, 578, 603], builder [49, 53], critic [77, 161, 164, 173], designer [20], protocol [392], architecture.md [64, 122, 144, 223].
  - `git grep -E "builder-rules|critic-diff-brief"` outside records → 32 files, including `experiments/measurers/prepare_copy.py`.
  - The package grep → architecture.md (5 lines), test-layers.json (7), 36 `.py` files.
  - Byte deltas of the spec's texts (python, UTF-8): +1029, +361, −129, +236, +180, +49.
  - Each negative had a positive control:
    - dev-path resolver: 0 hits, with `FORGE_CARRIERS` as the control;
    - integrator list: 0, control `owns_gate.py`;
    - `expected from`: 0, control 4;
    - D-0057 in DECISIONS.md: 0 with grep "D-0057 —", control "D-0033 —" found at :32.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "B1 C2 cannot pass its own DoD: the six files are deleted only at L2, and OWNER_KEYS sit in two files until then; the L1-draft has no route into the C2 tree",
    "B2 the C3 witness runs the main-clone test path, so it judges main instead of the worktree; the 'except two rows' clause is wrong",
    "B3 package readers missed: architecture.md AR-29 carrier :144 and :64/:122/:222/:223, test-layers.json whys, 36 package comments; the spec says the package is not edited",
    "B4 E4 breaks: test_arch_check.py drops out of the gate-named set (keep row layer gate_named named only by builder-rules item 14)",
    "B5 untaken batch rows missed: OH9-1, OH9-7, PC4-6 (writes builder-rules 7c), release-next/2 line 12",
    "B6 K-NOBRIEF false green: bare names like 'builder-rules 7b' pass, and MAIN leaves out package design/ although section 2 calls it main",
    "B7 F4 and F6 decided in but no N7 card or rule-24 texts; the test_handoff K_SCOUT_FORM pin is unlisted; owns_readers:55 points at absent split text"
  ],
  "class_completeness": "Readers of the six deleted files walked by git grep over the whole tree outside records: package, experiments and untaken batches missed (B3, B5, F7); SIBLING_MAP axis 1 (AR-29 carrier with critic Q11), axis 31 (no TESTING or skills row) and axis 18 (test-layers keep rows) need edits in the same commit.",
  "trail": {
    "read": [
      "docs/tasks/specs/20261117-no-briefs-fold-into-roles-spec.md",
      "plans/builder-rules.md",
      "docs/tasks/critic-diff-brief.md",
      "docs/tasks/specs/20261116-spec-facts-by-code-spec.md:408-482,621-660,690-730,795-872",
      "docs/TESTING.md:60-140,165-172,212-234",
      "docs/TEAMWORK.md:1-32",
      "docs/SIBLING_MAP.md:470-520",
      "docs/RUNBOOK.md:366-402,614-653",
      "tools/test_handoff_rule_anchors.py",
      "tools/tests/test_role_carriers_one_owner.py:1-130",
      "tools/test_quarantine.py:40-62,1125-1140,1335-1365,2190-2210",
      "ai-packages/qa-factory/scripts/selftest.py:721-736",
      "tools/session_context.py:204-235,1300-1330",
      "tools/agent_budget.py:250-262",
      "tools/mechanism_gate.py:215-276",
      "DECISIONS.md:1-20,32",
      "docs/DECISIONS_ARCHIVE.md:144-145",
      ".claude/agents/designer.md:15-46",
      ".claude/agents/builder.md:39-56,88-100"
    ],
    "reruns": [
      {"command": "python -B tools/session_context.py | grep BOOT BUDGET", "result": "BOOT BUDGET: 109921 bytes / 120000 (4 files + 4 imports) | CLAUDE.md: 50808/58500 incl. imports 98899"},
      {"command": "selftest.gate_named_files old carriers vs TESTING.md plus moved 7b/7c", "result": "lost ['test_arch_check.py'] gained []"},
      {"command": "K-NOBRIEF regex over MAIN plus ai-packages/qa-factory/design/*.md", "result": "hits include ai-packages/qa-factory/design/architecture.md [64, 122, 144, 223] outside the spec's MAIN"},
      {"command": "git grep -E builder-rules|critic-diff-brief -- ai-packages", "result": "architecture.md 5 lines, test-layers.json 7, 36 py files"}
    ]
  },
  "fixes": [
    "B1 move the six git rm into C2 owns; the Lead commits L1-draft on the batch branch first; C2 gets a coordinator-made worktree from that branch; restate E1 as one wave merge; add a temporal edge for the expected red",
    "B2 C3 DoD: run from the worktree root with a relative path, all green",
    "B3 add a package card for architecture.md and test-layers.json with architecture AR-29 and judgment none lines; a Lead decision line on package comments plus a former-numbering line in builder.md rule 11",
    "B4 Lead decision: re-layer or quarantine test_arch_check.py in the package card; E4 names the exception",
    "B5 add OH9-1, OH9-7, PC4-6 and release-next/2:12 to section 10 and L1",
    "B6 FORBIDDEN gains the bare names critic-diff-brief and builder-rules; MAIN gains ai-packages/qa-factory/design/*.md; add an adversarial row",
    "B7 designer round: N7 card with exact texts and the K_SCOUT_FORM update; critic.md rule 24 Q13 verbatim plus Q13(e); designer rule 3 line; POINTERS row; TESTING split sentence; supersede line in spec 20261116",
    "F1 D-0057 is the holder; trim D-0033 instead of appending",
    "F2 restore the lost sentences of items 18, 20 (RUNBOOK 12 item 2 with handback_extract --agent), 11, 7a, 16a, 13",
    "F3 Lead picks the holder of 7a vs 16b",
    "F4 one leave-the-round criterion in rule 9, critic rule 5 and Q4; replace queue it instead",
    "F5 one main-document list via the axis-31 rows for TESTING and skills; reword the PROJECT paragraph; widen the not-extra list",
    "F6 batch template line 16 drops the file option; classify docs/retro/README.md and the other unlisted documents",
    "F7 prepare_copy.py:195 re-pointed; SIBLING_MAP edited by name, not line",
    "F8 TESTING :229 text and the 7b self-reference",
    "F9 correct the section 9 table: own bytes ~51.4-51.8K of 58.5K; boot ~111.9-112.3K",
    "F10 strike the resolved not-established lines",
    "F11 carve out CLAUDE_HOST_ADAPTATIONS_FULL; absolute given paths in C3"
  ]
}
```
