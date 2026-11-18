# t-1148 — code critic: no-briefs wave 1, cards C1, PKG, C2 (+ L-b) — verdict

Reviewed: branch `pile/forge/batch-9` at 7a2cf516 (worktree `.claude/worktrees/nobriefs-batch`, read only); commits
60f481c6 (C1, t-1138), 6405f1f8 + 4c34fcdb (PKG, t-1140), 937210dc (C2, t-1144), 0a8c8fd1 (L-b). Spec:
`docs/tasks/specs/20261117-no-briefs-fold-into-roles-spec-r2.md` (§1, §2, §4.2.1, §4.2.4, §4.7, §7, §8, §10, §11 C1/PKG/C2,
§12 E1-E13, Lead decisions). C3 and L-a are out of scope (t-1147).

**Verdict: годно с правками (NEEDS WORK, non-blocking list; JSON: fit_with_fixes).** Per card: C1 — годно (two minor
wording fixes, F3, F4); PKG — годно (its report is not attached, F6); C2 — годно с правками (F1, F2). No finding blocks the
merge; F1-F4 are minor and are fixed in this round (PROJECT.md «Командная работа» п. 9). The decision to accept is the Lead's.

## Findings

**F1 (C2 / the spec's own claim; fix this round, does not block the merge). A deleted negative control leaves `restated()`
unable to fail.** `tools/test_handoff_rule_anchors.py:99-105`: `test_critic_rule_23_what_comes_back` asserts
`restated(block) == []`. Spec §11 C2 deletes `test_negative_control_restatement_in_a_pointer_copy`, saying "behaviour still
checked by test_critic_rule_23_what_comes_back". That claim is false. A positive `== []` passes when `restated()` is broken,
and no other test in the file ever gets a non-empty result from `restated()`. Measured with a mutant on a scratch copy
(`return []` in place of the body of `restated`, `HANDOFF_ANCHORS_ROOT` = the batch worktree): new suite **16 passed**
(the mutant lives). The same mutant against the pre-C2 suite and its files (937210dc^): **1 failed, 17 passed**, and the
one that failed is `test_negative_control_restatement_in_a_pointer_copy`. So the deletion follows the letter of the spec,
but its reason does not hold: the "rule 23 carries no copy of the hand-back rule" pin can no longer fail.
Fix: add one line inside `test_critic_rule_23_what_comes_back` (no new test, no fixture). Critic rule 16 really does carry
those words, and `test_role_rule_carries_file_rule` already requires K2 and K_LINE there:
`assert restated(rule_block(read(CRITIC), 16)) == [K2, K_LINE]  # negative control: restated() finds the words where they are`.
The deletion of `test_negative_control_real_key_in_a_copy` in `tools/tests/test_role_carriers_one_owner.py` is a
different case. It is allowed and its reason holds: `violations()` is still killed by the synthetic controls
`test_negative_control_restatement_is_named` and `test_negative_control_owner_lost_its_key` (`:232-239`).

**F2 (C2, Q6 duplication; minor).** `tools/tests/test_role_carriers_one_owner.py` `_tracked_all` (`git ls-files -z`, or
`rglob` when there is no `.git`) copies the body of `tracked()` (`:177-183`) and drops only the `is_scanned` filter.
That gives two ways to list tracked files in one module, and it is called once per parameter (8 git subprocesses).
Fix: `def tracked(root): return sorted(r for r in _tracked_all(root) if is_scanned(r))`, with `_tracked_all` defined
above it.

**F3 (C1; minor, consistency).** `docs/CLAUDE_HOST_ADAPTATIONS_FULL.md:33` now reads "`.claude/agents/critic.md` rule 22
items 6-7". The spec replaced only the token, but critic.md labels them Q6-Q7. CLAUDE.md:127 and
`tools/install_parity_anchors.json:22` say "rule 22, Q6-Q7". Fix: "rule 22, Q6-Q7". The POINTERS row
`the rule text is \`.claude/agents/critic.md\` rule 22` still matches after this edit.

**F4 (C1; minor, record consistency).** `docs/tasks/test-diet.md:17` (TD-0 row) has the deletion note after
`docs/tasks/critic-diff-brief.md`, but there is none after `plans/builder-rules.md` 7b/7d. That file was deleted in the
same wave. Fix: after it, «(удалён 17.11.2026; правила — `docs/TESTING.md` и `.claude/agents/builder.md`)». The file is a
plan, outside MAIN, so no pin is affected.

**F5 (L-b, Lead's commit; proposal, the decision is the Lead's).** The 0a8c8fd1 message says "axes: not a mechanism (… no
duty or check changes meaning)". Spec §1 «Mechanism» says every Lead commit of this change carries the rule-10 axis block.
`FORGE_CARRIERS` (`tools/test_quarantine.py:51`) is the input set of two gates: `enter` refuses names outside keep
(`:1134-1137`), and `--phase2` refuses "a carrier still names" (`:1361`). It now reads all of `docs/TESTING.md`, a document
much wider than the old 7b. Today the effect is nil: E4 gives the same set apart from `test_arch_check.py`. But from now
on, any example `test_x.py` written into TESTING prose becomes gate input. The history is pushed and stays as it is.
Proposed fix: the wave-merge message (or the `accepted` notes) carries the axis enumeration for this one constant, with a
sentence that TESTING.md prose is now a gate carrier.

**F6 (attachment layer, rule 7; does not block the code).** No C1 (t-1138) or PKG (t-1140) hand-off or witness came with
this review. The journal has `delegated` t-1138, and `delegated` + `returned` t-1140, with no `accepted`. Spec §1 asks the
PKG report to list the AR-20 change check rows. From the diff they are: `test_arch_check.py` gate_named → data_join, plus 6
why rewrites (`test_story_step.py` also named_by `plans/builder-rules.md:26` → `docs/TESTING.md`; `test_audit_rules`,
`test_console_encoding`, `test_driver_layers`, `test_probe_by_code_copy`, `test_story_run_words`). No ratchet row was
raised. Their mechanical checks were cheap, so I re-ran them myself (trail below), and all pass. Fix: the Lead puts the two
hand-offs, with the PKG row list, into their `accepted` events.

## DoD keys, one by one

- **C1** — годно. All C1 DoD presence keys are in TESTING.md, RUNBOOK.md and batch.md (my key script, with a negative
  control). `critic-diff-brief`, `test-diet-*brief`, `extract_handback.py` and `builder-rules` are absent from the C1 owns.
  The only exceptions are the test-diet.md notes; RUNBOOK §9.8's line is gone since the main merge 23c9fee3. The 7b text
  in TESTING «Что запускать по своей правке» is verbatim, apart from the spec's own edits (heading, the dropped
  F6-33 clause, «раздел … ниже», the item-7 bullet, the 7c row, the split paragraph). TESTING:88 is in the «пока не
  проверяет» world (F-R2-6) ✓. RUNBOOK §12 items 2 and 8 match §4.2.4 ✓. The template line matches §4.7 ✓.
  `prepare_copy.py:195` ✓.
- **PKG** — годно. The pointers sit at architecture.md :64 (AR-3 → builder.md rules 4, 11), :122 (AR-11 → rule 11), :144
  (AR-29 → critic.md rule 22 Q11), :222 (AR-20 → rule 22 Q9), :223 (Latin form, the Lead's decision). All targets exist:
  critic.md rule 22 has Q9 and Q11, and builder.md rule 11 carries the caps and the default-key text. FR-30: no Cyrillic,
  and `selftest.py --lang` passes. Both commits carry the `architecture:` and `judgment:` lines. `test_arch_check.py` as
  data_join holds: `test_arch_check.py:162-188` drives `check_files` through `detectors.json` rows, missing keys, a broken
  file and custom rows. `named_by` only needs to be a non-empty list for `detector` rows (`selftest.py:628-630`) ✓.
  `gate-registry.json:188` and the package `.py` comments stay as history (Lead decision) ✓.
- **C2** — годно с правками (F1, F2).
  - The pins judge what the spec says. K-REG reads the axis-31 table through `md_table.table_after` (one road). It
    case-folds `owner`/`procedure`, ignores text after the closing backtick, and expands the `*` row. K-NOBRIEF covers
    paths, stems and the top-level brief regex. ALLOWED is builder.md only, one sentence. All 12 adversarial rows of §8
    are there, plus 2 more. K-TESTPTR has the four rows of §7 and the designer → rule 24 Q13 row. POINTERS and
    OWNER_KEYS match §11.
  - The pins can fail (five corrupted copies, each restored by byte copy, `cmp` equal):
    - TESTING heading renamed → 5 K-TESTPTR/POINTERS reds.
    - Bare stem in PROJECT.md → `test_no_main_document_names_a_deleted_file[PROJECT.md]` red.
    - Axis-31 heading renamed → `test_register_sees_the_main_documents` red, and the MAIN-param test collapses to 1 skip
      (E11 holds: never a silent pass).
    - Stem in a second builder.md sentence → red.
    - A deleted path in `design/architecture.md` → red.
  - C2's judgment calls are right. A per-line scan after blanking is the same as a whole-text scan, because the paths and
    stems hold no whitespace, and it gives file:line. A sentence ends at a period followed by whitespace or the end; that
    is the right reading of "through its final period", because the sentence contains `TESTING.md`.
  - Observation (spec-conformant, not a finding): a pointer placed INSIDE the ALLOWED sentence would be blanked too. The
    spec accepts this; check 33 (i) covers the semantic side.
- **No live pointer to a deleted file in a MAIN document** — holds. I ran `git grep -i` for the six names and
  `retro/README` over the whole tree, minus specs/handoffs/snapshots/piles/package/logs/experiments/task_reports. The only
  hits are builder.md's ALLOWED sentence and records §10 leaves unedited: ADOPTION_LEDGER, DECISIONS_ARCHIVE, FINDINGS,
  PROJECT_FULL, factory-fixes, BACKLOG, feature-fragility, test-diet, the dispatch_manifest fixtures. There is no hit in
  DECISIONS.md, CURRENT_CONTEXT.md, AGENTS.md, `.github`, `.githooks` or `tools/*.py`, apart from the pin itself. The
  same call found the builder.md line, which is the positive control.
- **E4 set unchanged** — reproduced. My script uses the old carriers from 9616b6f4 (L-a), 1d1e8b21 (pre-L-a) and
  fdf90f7f (pre-batch), the new carriers from the batch head, and the package from the batch head. On each base: old 235,
  new 234, `old − (new ∪ {test_arch_check.py})` = [], only-new = [], and `test_arch_check.py` keep layer `data_join`. So
  C2's E4 witness is consistent whatever `HEAD~1` was when it ran. Four names are gate-named without being keep rows
  (`test_import_test_receipt`, `test_real_or_mock`, `test_story_run_s5_parallel`, `test_validate_artifacts_report`).
  They are the same in the old and new sets, so they are not this diff's.

## Standing questions

- **DUPLICATION AND CONSISTENCY** — F2 (`_tracked_all` ↔ `tracked`), F3 (items vs Q vocabulary). Otherwise none found. I
  grepped for: a second axis-31 reader (only `md_table`); a second list of deleted files (only `DELETED`); the Latin
  pointer form (the same wording in architecture.md:223 and the 6 test-layers rows).
- **CODE QUALITY** — none blocking. The new functions are under 25 lines, with at most 2 nesting levels. The pin message
  names file:line and the door.
- **ONE ROAD** — the register goes through `md_table` ✓. The second git-listing road inside one module is F2. No language,
  project or case is excluded.
- **TESTS** — the C2 commit has `tests-over: K-NOBRIEF/K-REG table rows of spec section 8`. The reason holds: the rows are
  required by §8, they form one parametrised table, and the four tests have the shapes the spec names. The negative-control
  gap is F1.
- **Class completeness (map)** — axis 31 (the pins, MAIN by register): covered. Axis 18: no ratchet row moved. Axis 1
  (AR-29 carrier ↔ critic Q11): PKG pointer resolves to rule 22 Q11 ✓; the CLAUDE.md rule 10 / designer side is t-1147's.
  Axis 20/AR-20: one keep row re-layered, none raised ✓.

## Questions I could not settle

1. C2's full DoD set after the main merge: 23c9fee3 touched none of C2's files (RUNBOOK, hygiene_gate, permission_audit).
   My re-run of the smaller DoD files was cut off by my own 300 s cap (trail), and `test_test_quarantine.py` was not
   re-run. The batch canon decides both; I make no claim about them.

## Trail

- Read: spec r2 whole (960 l.); C2 hand-off `t-1144-c2-pins.md`; `git show` of the five commits (full diffs);
  `tools/test_handoff_rule_anchors.py` whole; `tools/tests/test_role_carriers_one_owner.py` :1-60, :125-250 and the
  added block; `docs/SIBLING_MAP.md` :473-540; `tools/md_table.py` :90-107; `selftest.py` :595-660, :700-745;
  `tools/test_quarantine.py` :51, :220-232, :1125-1145, :1330-1370, :2190-2210; `builder.md` :126-134 (`cat -A`: LF, the
  sentence ends "FR-57.\n"); `test_arch_check.py` :160-190; base `plans/builder-rules.md` :30-75 (937210dc^).
- Re-runs:
  - Pin suite on the copy of the batch tree: `183 passed in 1.22s`.
  - Corruption probes (a)-(e) as listed above, then restored: `183 passed`, `cmp` same ×5.
  - Mutant `restated` → `16 passed` (new suite) vs `1 failed, 17 passed` (pre-C2 suite).
  - `python -B scripts/selftest.py --lang` → `PASS lang: no Cyrillic anywhere in the package … 2/2 ok`.
  - `python -B tools/architecture_index.py --check` → `up to date (29 invariants, 2682 bytes)`, rc 0.
  - E4 re-run on three bases → old 235 / new 234 / left [] / only-new [] / `data_join`.
  - C1 key script → 11 PRESENT, negative control False.
  - Small DoD files at the batch head: see the line below.
  - `git grep -i` deleted names (above). Grep `dev:` in tools/*.py → 0; the control (the same call on package scripts)
    → 4 hits, so no code resolves `dev:` carriers.
- Small-file re-run at the batch head (`test_install_parity`, `test_owns_readers`, `test_language_sites`,
  `test_handoff_rule_anchors`, `test_role_carriers_one_owner`): my `timeout 300` cut it off at about 14 % of the collected cases (`.......... [ 14%]` plus 22 dots, no F or E in what ran). Not finished, so no claim rests on it: the batch canon decides. The two C2-owned files among them were run whole earlier: anchors `16 passed`, pins `183 passed` (copy).

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "fixes": [
    "F1 tools/test_handoff_rule_anchors.py:99-105 - restated() lost its only negative control (mutant return [] survives: 16 passed; pre-C2 suite kills it); add inside test_critic_rule_23_what_comes_back: assert restated(rule_block(read(CRITIC), 16)) == [K2, K_LINE]",
    "F2 tools/tests/test_role_carriers_one_owner.py _tracked_all duplicates tracked() (:177-183); make tracked() filter _tracked_all",
    "F3 docs/CLAUDE_HOST_ADAPTATIONS_FULL.md:33 'rule 22 items 6-7' -> 'rule 22, Q6-Q7'",
    "F4 docs/tasks/test-diet.md:17 add the deletion note after plans/builder-rules.md 7b/7d",
    "F5 L-b 0a8c8fd1 declared not a mechanism though FORGE_CARRIERS feeds the enter/phase2 gates; carry the axis enumeration in the wave-merge message or accepted notes (Lead's decision)",
    "F6 attach the C1 (t-1138) and PKG (t-1140) hand-offs, with the PKG AR-20 row list, to their accepted events"
  ],
  "class_completeness": "axis 31 covered (K-REG reads the register; K-NOBRIEF over MAIN by path and stem; git grep over live files: only records and the ALLOWED sentence); axis 18 n/a (no ratchet row moved); axis 20/AR-20 one keep row re-layered, none raised; axis 1 AR-29 carrier resolves to critic.md rule 22 Q11 (CLAUDE.md/designer side is t-1147)",
  "trail": {
    "read": [
      "docs/tasks/specs/20261117-no-briefs-fold-into-roles-spec-r2.md (whole)",
      ".claude/worktrees/nobriefs-c2/docs/tasks/handoffs/t-1144-c2-pins.md",
      "git show 60f481c6 6405f1f8 4c34fcdb 937210dc 0a8c8fd1",
      "tools/test_handoff_rule_anchors.py (whole)",
      "tools/tests/test_role_carriers_one_owner.py :1-60, :125-250, K-NOBRIEF block",
      "docs/SIBLING_MAP.md :473-540; tools/md_table.py :90-107",
      "ai-packages/qa-factory/scripts/selftest.py :595-660, :700-745",
      "tools/test_quarantine.py :51, :220-232, :1125-1145, :1330-1370, :2190-2210",
      ".claude/agents/builder.md :126-134; test_arch_check.py :160-190; plans/builder-rules.md at 937210dc^ :30-75"
    ],
    "reruns": [
      {
        "command": "ROLE_CARRIERS_ROOT=<copy of batch tree> python -m pytest tools/tests/test_role_carriers_one_owner.py -q",
        "result": "183 passed in 1.22s"
      },
      {
        "command": "five corruption probes on the copy (TESTING heading, PROJECT stem, axis-31 heading, builder.md second sentence, design path)",
        "result": "5 / 1 / 1 (+1 skip) / 1 / 1 failed as expected; restored: 183 passed, cmp same x5"
      },
      {
        "command": "restated() mutant (return []) vs new and pre-C2 test_handoff_rule_anchors.py",
        "result": "new: 16 passed (mutant survives); pre-C2: 1 failed, 17 passed (killed by the deleted control)"
      },
      {
        "command": "python -m pytest tools/test_handoff_rule_anchors.py -q (batch head)",
        "result": "16 passed in 0.17s"
      },
      {
        "command": "python -B scripts/selftest.py --lang (package of batch head)",
        "result": "PASS lang: no Cyrillic anywhere in the package; 2/2 ok"
      },
      {
        "command": "python -B tools/architecture_index.py --check (batch head)",
        "result": "architecture index: up to date (29 invariants, 2682 bytes), rc 0"
      },
      {
        "command": "E4 script on bases 9616b6f4, 1d1e8b21, fdf90f7f",
        "result": "old 235 new 234 left [] only_new [] test_arch_check.py layer data_join"
      },
      {
        "command": "C1 DoD key script with a negative control",
        "result": "11 PRESENT, negative control False"
      },
      {
        "command": "git grep -n -i deleted names over live files",
        "result": "only builder.md ALLOWED sentence and section-10 records"
      }
    ]
  }
}
```
