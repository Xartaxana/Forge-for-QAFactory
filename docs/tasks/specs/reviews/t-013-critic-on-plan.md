t-013 critic-on-plan (critic, 11.11.2026): the report as handed back; the handoff path named in the dispatch was outside the critic's writable folder

## t-013 critic-on-plan: review of the draft spec `docs/tasks/specs/t-013-claude-policy-rewrite.md`

**Report file not written.** The handoff gate only lets a critic write inside `docs/tasks/specs/reviews/`, and the dispatch named `docs/tasks/specs/reports/t-013-critic-on-plan.md`. The hook refused even a scratch file and named its door: put the whole report into the final message. So this message is the full report (critic rule 16). To save it, the coordinator can run `tools/handback_extract.py` or re-dispatch with a `reviews/` path.

**VERDICT: ACCEPT WITH FIXES (NEEDS WORK). 3 blocking findings, plus 6 fixes that are not blocking.**

The text in §3 is faithful to the present policy. Every duty I walked is either kept with the same meaning or has a correct DROP fact. The blocking problems are all in what surrounds §3: the size DoD, the node plan, and the calibration bindings.

Duties walked: 182 §2 rows (spec :55-236), each checked against the present CLAUDE.md and against §3. I also read the present policy block (:73-864) and host section (:1-72) sentence by sentence, looking for any duty that has no §2 row. I found none.

---

### Mechanical layer: control re-run (cheap)

- I took spec lines 248-707 as the new text: **460 lines, 44 340 bytes**. This reproduces the Lead's witness.
- §4(a) anchor list, checked as literal case-sensitive substrings (the way `install_parity.py` matches them, `normalize_text` at :166-174):
  - **91 of 91 present.**
  - Negative control `ZZZ never here`: absent, as expected.
  - Two anchors occur more than once: `CONTEXT` 3 times and `Role ≠ tier` 5 times (see fix F3).
- The 81 old `routing-policy` anchors against the new text: **60 survive verbatim, 21 do not.**
  - The 21 split into four groups:
    - judge text: `LEAF closes under ONE`, `CALIBRATED JUDGE`, `does NOT replace the critic gate at INTEGRATION`, the rule 13 opener;
    - dropped rows: R1-a/b `when` cells, hygiene 2, the routing-log heading;
    - reworded openers: rule 8, rule 10, degradation 1, hygiene 1, the kit title;
    - line-split phrases: `CONTEXT ISOLATION`, `MODEL NAME`, `DECLARATIVE on reads and NORMATIVE`, `ISO local time with NO`, `BATCH CANON;`, `INTERACTIVE surface (a CLI/UI`, `AT and BEYOND`, `OR attached in FULL`.
  - Every one of the 21 matches the spec's own spot map at :766-770. The old anchor `BY DEFAULT` survives only through rule 2.
- OWNER_KEYS and the POINTERS anchors, whitespace squashed and case folded:
  - All 5 CLAUDE.md keys present.
  - `6. An environment-negative claim…`, `11. DoD in every dispatch…`, `9. Fix the class…` and the brief pointer are all present.
  - The new COST anchor `Cost gates (D-0035, D-0038, D-0040, D-0054;` is present.
  - The old `6. Cost gates (D-0035` is absent, as §4(b) expects. Negative control absent.
- The K4b fixture `tools/fixtures/host_pre_delivery_CLAUDE.md` contains none of the five K4b markers. Positive control: «DoD in every dispatch» found at :266.
- `git diff 10b6f86~1 10b6f86 -- CLAUDE.md` touches only the host section (:1-72), so the session-injected copy of the policy block equals the file on disk.
- CLAUDE.md is LF on disk (`git ls-files --eol`: `i/lf w/lf`). So the size measure is not inflated by CRLF.

---

### Blocking findings

**B1 — K7 / DoD: the size target is missed, and the spec hands the cutting to the builder.**
- **What:** the brief's target is under 40 000 bytes; the draft measures 44 340. §6 N1 ("measure the size") and §3 :243-245 ("if over 40 000, §3 footnote «What else could go» applies") leave it to a Sonnet builder to choose which policy text to cut, on a mechanism path.
- **Why it blocks:** one footnote option loses a KEEP duty. Spec :713 says "Lead degradation 4 a-c compressed to one sentence (cost: the ENTRY procedure becomes a pointer to check 5)". That removes LD4 a), the ENTRY procedure before the first Lead action, which no code gates. That conflicts with «Правила которые мы не меняли не должны потеряться».
- **Fix:** the Lead (or the designer) picks the cuts in §3 before dispatch, from the K7 list below (about 4.4K available without touching a KEEP duty). Delete the LD4 option from the footnote. N1's DoD then states the measured size as a key (under 40 000).

**B2 — K5: N2's witness depends on N1's uncommitted state.**
- **What:** N2 runs in parallel with N1 and both leave their changes uncommitted (§4h). Yet N2's witness is `install_parity.py --check` plus `test_role_carriers_one_owner.py` (spec :947-949).
  - `--check` covers the whole manifest, including unit `routing-policy`, whose host file (CLAUDE.md) and anchor file are N1's.
  - The one-owner test reads CLAUDE.md, `plans/builder-rules.md`, `docs/RUNBOOK.md`, the FULL doc and the test file itself, which are all N1's paths.
- **Failure scenario:** N1 has rewritten the anchors but not yet pasted §3 (or the reverse). N2's witness comes back MISSING or red for reasons outside N2's owns. Rule 4 names exactly this: "another worker's uncommitted state can break a shared full run".
- **Unclear too:** whether N1 and N2 share one tree or run in worktrees. "ONE commit by the Lead" implies a shared tree. A worktree setup would contradict it.
- **Fix:** run N2 after N1 is handed back, or narrow N2's witness to what N2 owns (the grep for «host adaptation» over N2's carriers, plus `install_parity` limited to the designer/PROCESS/skill units if the tool can filter by unit). Then run the full `--check` and the one-owner test once, as the Lead's pre-commit witness. State shared tree vs worktree explicitly.

**B3 — K2 / K5 / E2: calibration checks 20 and 2 are left pointing at removed text, and E4's detector is check 20.**
- **Evidence:**
  - `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md:80-86`: check 2's "CUMULATIVE SUBCASE (rule 13's judge/critic-integration clause)". That clause no longer exists in §3 rule 13, and R13-g is rewritten.
  - `:650-676`: check 20 "(a) liveness -- rule 13 is present in CLAUDE.md; `"judge"` is in the validator's basis whitelist; judge calibration is alive".
  - Spec §4(a) :771-773 says WEEKLY_CALIBRATION needs "no edit". §4(f) rewords only :964 and :362-366.
  - E4 (:906-911) names check 20 as the detector for "no acceptance with `basis: judge` counts here". But check 20 is written as a liveness test of the judge mechanism, so every window it reports a dead mechanism instead of the new invariant.
  - E2's invariant "a number never points at a different duty than before" is broken by check 2's citation.
- **Also:** `tools/journal_validator.py:521` still legalises `basis: "judge"`. E4 acknowledges this, but no node or fork removes it: F8 (B) lists judge.md, gateway, the protocol, pins and units, not `BASIS_VALUES`.
- **Fix:** add to N2's owns:
  - reword check 2's subcase to the R13-g text that survives;
  - reword check 20 to "(a) rule 13 reads 'not used'; (b) any `accepted` with `basis: "judge"` in the window is a self-certification finding".
  - Add `BASIS_VALUES` "judge" to F8 (B), or to a queued residual node with its owner.

---

### Findings to fix (not blocking)

**F1 — K8 / K3: F2's recommendation (A) adds duties.** Evidence: present R13-g (CLAUDE.md:553) is scoped to "judge acceptance of a leaf". Adaptation 6 (:35) says only "ONE critic pass per topic (R13-g)". The draft row (spec :528) is "integration (a merge into `main`) | parts of the SAME topic are merged TOGETHER through ONE critic pass…; a merge over roughly 100 lines carries that pass (rule 3)". This makes two new demands for non-judge work:
- a merge-batching obligation;
- a critic pass on any merge over about 100 lines. Three small critic-skipped diffs of one topic merged together now need a pass that today's text does not require.

That contradicts §1 "No rule demands anything beyond what it or a host adaptation demands today", which is the same reason the designer itself gave for rejecting option (C). Fix: the row's duty becomes "one critic pass per topic, not one per part (Cost gates, rule 12)", with "merged TOGETHER" and the ">100 lines merge" clause dropped. If kept, the Lead must name it as a new duty.

**F2 — K1 / K6: critic-on-plan narrows PROJECT.md's unconditional cases.**
- Evidence: §3 :330-333 puts "always for a new idea of the owner and for a spec edit that changes a meaning" under the subject "a plan… that will itself serve as the SPEC for more than roughly 30 minutes of work". PROJECT.md «Как разрабатывается новая идея», step 6 ("Критик на план — обязателен для новой идеи"), and «Как принимается изменение пакета» p. 6 (б) are not conditioned on size; a between-attempts spec edit is often under 30 minutes.
- So CLAUDE.md would carry a second, narrower version of a rule whose owner is PROJECT.md.
- Fix: "…when it carries forks or a schema/money change; regardless of size, in PROJECT.md's mandatory cases (new idea, step 6; package change, p. 6); otherwise `critic: skipped, <reason>`."

**F3 — K5: two anchors guard nothing.** `CONTEXT` occurs 3 times in §3. It matches «CONTEXT MANIFEST», so deleting the CONTEXT ISOLATION motive of rule 2 trips nothing. `Role ≠ tier` occurs 5 times, so removing the heading trips nothing. Fix:
- reflow spec :311-312 so «CONTEXT ISOLATION» sits on one line, and make that the anchor;
- use `## Role ≠ tier` as the heading anchor.
- The same check applies to `MODEL` (one occurrence today, but a fragment of «MODEL NAME»): reflow :613-614 and anchor `MODEL NAME`.

**F4 — K5 / E1: a live pointer by adaptation number has no named fate.** `.claude/agents/designer.md:24-25` «(Host adaptation 2, D-0021.)». §4(f) rewords only designer.md:33. Fix: add :24-25 to N2 («(CLAUDE.md rule 2, D-0021.)»).

Also unnamed, and historical. They should be listed under "left as they are" so N2's grep witness does not flag them:
- `plans/BACKLOG.md:528,547` («CLAUDE.md адаптация 6»; frozen file);
- `docs/tasks/test-diet.md:17` («`CLAUDE.md` адаптация 12», a done row);
- `docs/DECISIONS_ARCHIVE.md`;
- the pile files `onboarding-forge/README.md:85`, `batch-1…:49`, `forge/batch-7…:37`.

**F5 — K6 / K7: §3 restates other owners' texts** (not key-pinned, so the one-owner test stays green; axis 31 and the boot rule still apply):
- rule 4a's pile sentence (503 B) repeats PROJECT.md «Командная работа», which is imported in the same session;
- rule 11's quarantine and SCOPE-CEILING list (414 B) repeats `docs/TESTING.md` («Файлы», «Карантин») and `plans/builder-rules.md` 7b;
- rule 10's "Code owns DATA…" sentence (about 400 B) repeats P27, also imported;
- hygiene 1's tail (84 B).

Fix: keep each as a pointer plus only the operative override. Keep the TEST QUARANTINE ALERT duty, which is the Lead's and needed every session.

**F6 — K6 / rule 10 (b): the axis block lines for axes 1 and 2 are incomplete.**
- Axis 1 (SIBLING_MAP:35-37): "a rule change in CLAUDE.md that touches a role's duties is checked against that role's profile in the same commit". R1-a touches scout acceptance (`scout.md:56-60` still requires `PROCESS/SCOUT_GOLDEN_SET.md`, which is absent), and rule 13 touches `judge.md:8,15` («(rule 13)», "which `basis: "judge"` acceptances are legitimate at all").
- Axis 2 lists SCOUT_GOLDEN_SET and the judge calibration as instruments, and both R1-a and rule 13 depend on them.

Fix:
- axis 1 line: "covered — designer.md pointer; scout.md and judge.md checked: no edit, gaps queued (scout.md golden-set clause, F8)";
- axis 2 line: "covered — R1-a and rule 13 read 'not used'; instruments unchanged".

---

### Questions (meaning may have changed; the Lead decides)

- **Q1 — K3: the rule 7 example next to its cancellation.** §3 :369 keeps «"haiku: …"» as a label example right after Tiers says "No tier runs on Haiku". The brief says "never a rule together with its cancellation". The spec keeps it verbatim for FG7-14, but FG7-14 is not designed yet, so no diff depends on that wording. Changing «haiku» to «sonnet» in the example is one word and folds nothing of FG7-14. The Lead decides which rule wins.
- **Q2 — K1: hygiene 1 states the canonical full-run form and, in the same line, "the full sets run on CI, not on this machine".** I read these as two duties: the allowlist form, and where to run. It is not a cancellation if "or a narrower target" is understood as the local default. Please confirm.
- **Q3 — K1: rule 3 widens "a recon deliverable" to "a plan or recon deliverable".** This matches practice (designer drafts reach critic-on-plan, this review included), but it is a widening of KEEP text.

---

### Key-by-key trail

**K1, nothing unchanged is lost: PASS for §3.** Missing from §2: 0. KEEP rows weakened: none blocking (F2 and Q3 are the only meaning shifts).

Duties checked by quoting both sides, with my verdict:
- rule 2 "regardless of the threshold" (CLAUDE.md:170) → spec :314-316: covered by "threshold counts the PRIMARY draft". PASS.
- rule 8 "a task that maps to a cheap tier" (:271) → "cheaper tier, or to a function routed for context isolation" (:376). Same as :274-278. PASS.
- Cost gates "readers are not counted" (:39) → the next sentence, "designers, critics and scouts are never counted" (:519-520). PASS.
- adaptation 2's "adversarial inputs" → now a pointer to designer.md rule 1, which carries it (designer.md:29-32). PASS.
- adaptation 10's designer rule 1 → spec :439-441, the same as designer.md:33. PASS.
- hygiene 6 registry status: "load-bearing" dropped (:691). A slight widening, harmless. PASS.
- R1-b "currency voided…" → "every accepted digest". Correct, since no exam pass can exist. PASS.
- 13.5 negative-form control → R1-b + hygiene 6, both standing. PASS.
- J17 `basis` for a non-Claude performer → kept at :596-597. PASS.
- rule 11's last paragraph: the Lead part is kept (:488). PASS.
- Every other KEEP row: wording tightened, provenance removed, meaning identical.

**K2, no DROP removes a live duty: facts verified on their carriers.**
- R1-a: `PROCESS/` holds 11 files, none `SCOUT_GOLDEN_SET*` (`ls`).
- Judge: `delegation.config.yaml:80-85` has `judge` with `scope: api-keys-only` and empty fields; `ADOPTION_LEDGER.md:99` reads deferred.
- Hygiene 2: contour is subscription (`delegation.config.yaml:14`); `ADOPTION_LEDGER:112` says "nothing in it is wired or run"; no workflow references gateway.
- J5b: `logs/` holds only `journal/dev1.jsonl` (no `journal-segments.json`, no `routing-log.jsonl`); `journal_keys.py:688` says the declaration "applies to the history only".
- J5a label = file slug: true here, because dev1 line 1 has no `continues` (`journal_keys.py:28-35`).
- B0: no tool reads the BEGIN/END markers (grep: CLAUDE.md, AGENTS.md, the skill, a fixture).
- R13-g's cumulative clause is judge-only (WEEKLY_CALIBRATION:80-86).
- The `basis` field for non-Claude work and rule 11's last paragraph are not dropped.
- The only DROP gap is B3: the detector bindings.

**K3, every FOLD is the adaptation and no more:**
- 1, 3, 4, 5, 7, 8, 9, 10, 11 and 12: present at the rule they adapt, with operative wording only. The kit text of rule 4 ("test FILE") and rule 11 ("AT and BEYOND" for every limit, the old SCOPE CEILING) is replaced, not kept next to its override.
- Adaptation 6: folded, plus F10's PROJECT.md cases (F2 above).
- R13-g goes beyond the adaptation (F1).
- E3(b), the witness of a path outside the package: §3 settles it ("the test file that judges the path, named in the DoD"), but it is openly a fork (F5) and agrees with PROJECT.md p. 2 and builder-rules 7b :20.
- Rule-plus-cancellation remaining: Q1 only.

**K4, numbers and ids: PASS, checked by reading §3.** In order: 1 (R1 a, b), 2, 3, 4, 4a, 5-10, 11 (R11 m, f, h), 11a, 12, 13 (R13 g), degradation 1-4 with a/b/c, hygiene 1-7, pt.4 a/b, pt.6 a/b/c.

**K5, bindings:**
- §4(b): POINTERS :57, :69 and :72 and their three carriers are handled; COST is reworded.
- Anchors: 91/91 present (F3 aside). Of the old anchors, 60 survive verbatim; 21 are dropped or reworded, as listed above.
- The temporal edge is settled by one commit (E5).
- CLAUDE_WARN: 44 340 gives 51 000, which lowers the threshold (`session_context.py:203-207`).
- Gaps: B2, B3, F4.

**K6, architecture and principles:**
- P31: the remaining two-road place is F5, named with its residual node.
- The four questions and the 36-line axis block in §4h match the map's 36 axes; axes 1 and 2 need F6.
- The one-owner test stays green, but F5 applies.

**K7, size: removable without touching a KEEP duty (bytes measured on §3):**
- repetition inside §3: the typed-fields list duplicates the event-shapes table (310 B); the validator's list of legal repeat-`delegated` cases duplicates the table's `delegated` row (about 250 of 495 B);
- other owners' texts (F5): about 1 400 B;
- provenance: the intro "It began as the kit's policy…" (258 B), plus the "(the owner's word 10.11.2026)" style datings;
- rare-session text: J5a and the merge-door detail (815 B; the refusal of `journal_validator --merge-parent` names the door).

Together these are about 3.0-3.5K. Adding the footnote's journal-mechanics option, and NOT the LD4 option, reaches under 40 000.

**K8, forks:**
- F1, F3, F4, F6, F7, F8 and F9 are real forks, and their recommendations lose no duty.
- F2 adds duties (F1 above). F10 narrows a PROJECT.md rule (F2 above). F11 is consistent with PROJECT.md «Что решать самому» and keeps "no tier silently decides intent".
- Small choices checked:
  - Dropped class labels: own search, case-insensitive, outside specs/snapshots/CLAUDE/AGENTS. Positive control "two-pass external" found 2 hits. Citers: only the anchors file, the fixture, and one pile finding citing «large-cadence» (history). PASS.
  - The «feature» F19 in the journal example exists (dev1:1).
  - `docs/RELATED_WORK.md` exists.
  - No fork is decided silently beyond the ones marked.

Class completeness, by the map: axis 1 is incomplete (F6, judge.md and scout.md). Axis 31 is covered (pointers and keys). Rule-number citers across PROCESS are incomplete (B3, checks 2 and 20). The adaptation-number citers have one live gap (F4).

```json
{"verdict":"fit_with_fixes","blockers":["B1 K7/DoD: 44340 bytes > 40000 target; spec delegates the cut to the builder via a footnote that includes a KEEP-losing option (LD4 ENTRY procedure). Lead picks cuts in §3 before dispatch; drop the LD4 option.","B2 K5: N2 witness (install_parity --check, test_role_carriers_one_owner.py) reads N1's uncommitted files; sequence N2 after N1 or narrow N2's witness; state shared tree vs worktree.","B3 K2/K5/E2: WEEKLY_CALIBRATION check 2 subcase (:80-86) cites removed rule 13 clause and check 20 (:650-676) tests judge liveness while E4 names it the detector; journal_validator still accepts basis judge with no node. Reword both checks in N2; put BASIS_VALUES judge into F8(B) or a residual node."],"class_completeness":"Axis 31 pointers/keys covered (POINTERS 57/69/72 + carriers). Gaps: designer.md:24-25 'Host adaptation 2' has no named fate (F4); PROCESS checks 2 and 20 cite rule 13 text that is gone (B3); axis 1 profile check misses scout.md and judge.md (F6); historical adaptation-number citers (BACKLOG 528/547, test-diet.md:17, pile files) not listed among the residuals.","fixes":["F1 R13-g row: one critic pass per topic (Cost gates); drop 'merged TOGETHER' and the merge >100 lines clause, or name them as a new duty","F2 rule 3 critic-on-plan: PROJECT.md mandatory cases apply regardless of size","F3 anchors: reflow so 'CONTEXT ISOLATION' and 'MODEL NAME' are one-line anchors; heading anchor '## Role ≠ tier'","F4 add designer.md:24-25 to N2; list BACKLOG/test-diet/pile citers as left-as-is","F5 replace restatements of PROJECT.md/TESTING.md/builder-rules in rules 4a, 10, 11 and hygiene 1 with pointers plus the operative override","F6 axis block lines 1 and 2 name scout.md/judge.md and the R1-a/rule 13 instruments"],"trail":{"read":["docs/tasks/specs/t-013-claude-policy-rewrite.md (whole)","CLAUDE.md:1-135 on disk + policy block via session copy (equal on disk per git diff 10b6f86~1..10b6f86)","tools/tests/test_role_carriers_one_owner.py (whole)","tools/install_parity.py:60-79,166-174","tools/install_parity_anchors.json routing-policy unit","tools/test_install_parity.py:1050-1090","tools/session_context.py:186-207","docs/TESTING.md (whole)","plans/builder-rules.md:15-26","docs/SIBLING_MAP.md:24-67 + axis headings","PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md:76-86,650-676","delegation.config.yaml:10-16,70-90","docs/ADOPTION_LEDGER.md:83-113","tools/journal_keys.py:25-40,684-692","logs/journal/dev1.jsonl:1",".claude/agents/designer.md:18-33","tools/critic_verdict.schema.json"],"reruns":[{"command":"sed -n 248,707p spec | wc -lc","result":"460 lines 44340 bytes (matches witness)"},{"command":"python heredoc: §4(a) anchors as literal substrings of §3","result":"91/91 present; CONTEXT x3, Role ≠ tier x5; negative control absent"},{"command":"python heredoc: old 81 routing-policy anchors in §3","result":"60 verbatim, 21 absent (judge/dropped/reworded/line-split), consistent with spec :766-770"},{"command":"python heredoc: OWNER_KEYS + POINTERS anchors squashed in §3","result":"all CLAUDE.md keys and anchors present; old '6. Cost gates (D-0035' absent; negative control absent"},{"command":"git ls-files --eol CLAUDE.md","result":"i/lf w/lf"},{"command":"Grep -i class labels outside specs/CLAUDE/AGENTS","result":"only anchors, fixture, one pile finding; positive control two-pass external found"}]}}
```
