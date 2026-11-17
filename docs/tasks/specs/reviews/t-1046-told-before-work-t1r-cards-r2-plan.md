# t-1046: plan critic on the T1r cards, redraft r2

Critic (Opus), a plan review under CLAUDE.md rule 3, PROJECT.md "new idea" step 6 and package change item 6.
Plan under review: `docs/tasks/specs/20261117-told-before-work-t1r-cards-spec-r2.md` (r2), read whole, including the Lead decisions R2-F1..R2-F7 and R3-F1..R3-F3.
Tree: the root checkout on `main` at `e28f8ece`, which is `origin/main`. `git diff --stat e9d6195b HEAD -- ai-packages` shows only `dry_stub.py`, `harness.py`, `story.json` and one changelog fragment, so the designer's read base still holds.
Wave B: branch `worktree-agent-ad0767bec786dddde`, head `a65afe58`, read with `git diff HEAD...<branch>` and in its worktree.

## Verdict

**NEEDS WORK** (`fit_with_fixes`). One finding blocks dispatch: F1, the dry census on axis 38. The other edits are text edits the Lead can make in this round. None of them changes the architecture, so the fix round needs no second critic pass, except F1 if the Lead picks another road for it.

| card | verdict |
|---|---|
| T1r-cards-a | dispatchable after edits F1, F2, F3, F4, F5, F7, F8 (notes F11, F13, F14, F15 also apply) |
| T1r-cards-b | dispatchable after edits F6, F9, F10, F12 |

Standing lines (critic-diff-brief, plan gate):
- DUPLICATION AND CONSISTENCY: three inconsistencies, all listed as findings. F13: a K line that contradicts the field's own definition. F14: an accounting sentence that is false. F6: a registry rule against the row that carries it. Searched: §3.1 against `role-rules.json` lines 64, 161-164, 181, 306, 347, 482-484, and the card texts in `ahead-cards.json`.
- CODE QUALITY: there is no code in the cards. On the data side, the R-4 row template matches `stage_joints.py` `ROW_KEYS` and `PAGE_ITEM` (`:74-79`).
- ONE ROAD (q12): no block. `gate_preflight:question_branches` is a new id rather than ROLE+ on `planning_contract:branches`. The two calls differ: the S3 block (`planning_contract.py:4007-4016`) against the S4 `variant_errors(at_cases_stage=True)` called from `gate_preflight.py:2142-2145`. The shared reader `variant_errors` is still reached, so this is not an exclusion. ROLE+ (R2-F4) and per-role witness sub-ids (R2-F5) also hold: each sub-id carries a different requirement text.
- TESTS (q5): -a adds no committed test. That is legal under `docs/TESTING.md` "Что не пишется": a role-text pin and a receipt per key are not written. -b deletes rows and re-points existing ones, so it stays under the volume rule. The label on -a's proof is wrong, though (F3).

## Findings

### F1 — blocks dispatch. Axis 38: every new joint needs a row in the dry census in the same commit; card -a cannot write that row and never runs the check

SIBLING_MAP axis 38 (`docs/SIBLING_MAP.md:644-655`): "A package commit that adds … a joint … changes its census row in the SAME commit". The census lives in `scripts/tests/fixtures/driver-exits/<group>.json`, and `python -B scripts/tests/dry_exits.py --check` must report `0 discrepancies` (the `full` and `dry-story` CI jobs).

Card -a adds 12 joints: 3 witness sub-ids, `source_preflight:check_source_inventory`, `estimate_record:facts_problems`, `artifact_producer:validate`, `gate_preflight:question_branches`, and the 5 rows of §4. But:
- its owns do not hold `fixtures/driver-exits/`;
- its DoD does not run `dry_exits.py --check`;
- its `siblings:` line names axis 34 only.

Probe: `dry_exits.main(["--check"])` with `stage_joints.DATA` pointed at a scratchpad copy that holds one extra row. Only the copy was changed; the real file was not touched (pt.7 (d)).
```
REAL rc 0 ['dry_exits --check: 0 discrepancies']
COPY+1row rc 1 [... "FAIL joint source_preflight:check_source_inventory: the driver has it and no row names it; add a row to fixtures/driver-exits/<group>.json with reach seed or live_only (or unwalked, counted in that group's ratchet) and a why_unreached", 'dry_exits --check: 1 discrepancies']
```
As written, -a would turn the canon red 12 times, and the builder could not fix it inside its owns.

Edit:
- Add `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\driver-exits\` to -a's owns. Scope: rows for the 12 new joints only, each with its group chosen by the `stages` rule of axis 38:
  - `s1-s4.json`: sc-3 (S1), witness `.requirements-tester` (S2), cd-4b (S4);
  - `s5.json`: `s5_precheck:sides.provisional`, `sides.pending`;
  - `s6-s9.json`: witness `.runner`, witness `.failure-analyst`, `artifact_producer:validate`, `estimate_record:facts_problems`;
  - `gates.json`: `execution_request:profile.none` and `fingerprint.build` (S5-S7, two groups), and `handoff_check:cli.values_rename` (`*`).
- Each row gets `reach` and `why_unreached`. Every rise of a group's `unwalked` ratchet is named in `raised_by` and in the report's raise table (axis 18).
- Add to the DoD: `python -B ai-packages/qa-factory/scripts/tests/dry_exits.py --check` -> `0 discrepancies`.
- Add to `siblings:`: "axis 38: a row per new joint".
- Add an order line in §7 against any open node that writes `driver-exits/*.json` (the P1-b nodes).

### F2 — fix in round. The unsited raise is +6, not +4, and two of the new rows have no node that will site them

Measured with `stage_joints.sited_ids(universe(), check_ids())` and `_is_sited` on main and on the wave B tree (script `sited.py`, see the trail). Results are the same on both trees:
```
True exit_gate:witness_errors.{requirements-tester,runner,failure-analyst}
False source_preflight:check_source_inventory / estimate_record:facts_problems / artifact_producer:validate / gate_preflight:question_branches
False s5_precheck:sides.provisional
False s5_precheck:sides.pending
True execution_request:profile.none / execution_request:fingerprint.build / handoff_check:cli.values_rename
unsited 46 (main) / 17 (wave B)
```
The sides findings are added as bare strings: `add` -> `_sited("sides", case, message, …)`, and `message` is a `str` (`s5_precheck.py:2417-2418`, `_sited` docstring `:294-298`). So nothing sites them. The finish spec's T5r card excludes them ("their sites wait for those rows"). The residual siting node of §7 does not own `s5_precheck.py`. The decision line "R3-F2 (a): `unsited` +4" is false on the measurement.

Edit:
- R3-F2 line and §5 E-9 record: "+6 (four function rows and the two §4 `sides.*` rows)".
- §7 residual node owns: add `scripts/s5_precheck.py` (`_sides_provisional`, `_sides_pending`) and `scripts/tests/fixtures/told-ratchet.json`. Siting moves `bare` to `tagged` in the K4 unit rows (`test_stage_joints.py:722-736`); wave B had to edit that fixture for the same reason (`told-ratchet.json`, 164 lines).

### F3 — fix in round. Key 4: R3-F3's "DOC-DISPATCH witness" is not the rule-11 form, and its keys are not quoted verbatim

- **The owns have test sets.** Rule 11 allows the DOC-DISPATCH witness only "when the owns are markdown/config with no test set of their own". `scenario_walk.py --witness-for` on -a's owns prints keep tests for every path (rerun below): stage-joints.json has test_contract_slices, test_detector_verdict, test_selftest_slow_tests and test_stage_joints; inject-map.json has test_role_load and others; role-load.json has test_role_load; `agents/qa-*.md` have test_audit_rules, test_validator_class, test_oracle_provenance and test_s5_precheck. The witness is that run. The key script is a supplementary check of A-2, which is legitimate, but not under that name.
- **Property (i) fails.** Roughly 15 landed texts in §3.1 are given as recipes, not text: "BRIDGE: same words ending with '.'" (rt-1a, au-2b, ru-4a, ru-4b, br-1b, br-2a, br-2c, br-4a, ck-3a), "BRIDGE: 'Every row's observable …'" (rt-1c), "card words after 'give'" (ck-3b), and fa-1f's "up to … then …". The §4 texts are "r1 §4 text" in a file that is not in -a's given. So the builder would write the keys AND the text, and the check would only check the builder against itself.

Edit:
- Add a §3.4 "landed texts in full": one row per landed seg and per §4 row, with role, row id and the exact text. The Lead or designer writes it before dispatch, from the card text by the recipes.
- The script's keys are quoted from §3.4.
- Rename the item "supplementary key-presence check of A-2 (keys from §3.4, script attached, negative control as written)".
- Keep R3-F3 (a) on the test question itself.

### F4 — fix in round. The §4 rows come from r1, which -a is not given, and the door of `execution_request:profile.none` contradicts its refusal

- §4 gives three rows as "r1 §4 text". The bodies were not re-read (§12), and `20261114-…-t1r-cards-spec.md` is not in -a's given.
- The functions moved since r1 measured them: r1 had `_sides_provisional` at 2085-2149, today it is at `s5_precheck.py:2104`; `_sides_pending` was at 2152, today it is at `:2171`.
- The `profile.none` door (r1 :340) is "report it in your digest as an onboarding gap, and write this one run with `run_suite.py --template request`". The refusal says something else (`execution_request.py:1823-1830`): "this is a gap of the onboarding, not of your test — the gate-A rehearsal asks the person (answer a/b/c); to onboard now: `/qa-factory:qa-onboarding`". The comment right above it names typing request files by hand (106 of them) as the harm. The page would therefore give a door that the refusal does not give, which breaks E-8 and R-6.

Edit:
- Copy the three r1 texts inline into §4 (and into §3.4, see F3).
- Make `profile.none`'s door the refusal's own: "report it in your digest: the gate-A rehearsal asks the person about the onboarding gap". If the Lead wants the template road instead, that is a fork to the Lead: it would also change the refusal text, which lives in the residual node.
- Add an edge E-13: "a §4 clause the body at today's line no longer checks: the row is not landed; the report names it". The invariant is AR-29.

### F5 — fix in round. Key 3, AR-29: the sc-3 bridge claims a check that does not run when the file is absent

`source_preflight.py:12-15`: `required = pipeline.get("source_inventory_required") is True`. When the file is missing and not required, the result is `allowed: True` with no errors. The bridge says "S1 closes on work/source-inventory.json: it lists at least one required source …", as if the file were always judged. The row is `when: always`.

Edit (bridge): "When work/source-inventory.json exists, or the pipeline requires it, S1 closes on it: it lists at least one required source, none is `pending`, and no source material lacks its retrieval or inspection receipt."

Neighbour on the same surface (the row text against the body), ck-3b: "plus `critic_verdict` … and `critic_note`". The body requires `critic_note` only with `could_not_judge` (`manifest_put.py:1088, 1299-1308`) and checks only that it is a string otherwise. Edit: "… and `critic_note` (owed with `could_not_judge`)".

I checked these bridges and replacements against their bodies and they hold: rt-1b, rt-4, ru-1, ru-3a, ru-4b, fa-1a, fa-1b, fa-1c, fa-1f, ts-1a, ts-3b, ts-3c, cd-4b, ra-3, §3.3, §3.3b, §3.3c, `values_rename`. Lines are in the trail.

### F6 — fix in round. A role-rules registry rule would contradict its carrier after -b

The registry rule `designer-one-case-per-plan-row` (`role-rules.json:163`) says "The designer writes one case per plan row, an unverifiable row too." The cd-4b bridge makes that conditional, and it is right to: `planning_contract.py:1927-1941` owes a case for a `skip`/`unverifiable` row only when an answer would make it tested. The comment there even says "a `skip` / `unverifiable` row gets no case". The anchor "an `unverifiable` row too" still matches, so `role_rules.py --check` stays green. But after -b re-points the carrier to the page, the registry's `rule` text states what the page denies.

Edit: -b's owns scope for role-rules.json gains "the `rule` text of :163 restated to the cd-4b meaning". Changing a registered rule's meaning is the Lead's call (its source is t-1685, not the owner), so state the Lead's decision in the spec.

### F7 — fix in round. The `values_rename` row shows a door that needs a shell to three roles that have none (FR-2, E-10)

§4 tells "delete the values file the refusal names" to all 12 roles of `handoff_check:cli`. qa-case-critic, qa-case-designer and qa-test-strategist have no Bash (`agents/*.md:4`, re-grepped). The door is the code's own (`handoff_check.py:3209`, `f"delete {…}"`), so the row is truthful. E-10's invariant "a no-shell role never sees a shell door" still breaks.

Edit (recommendation; the decision is the Lead's):
- Narrow the row's producers to the 9 Bash roles.
- Queue a door for the three no-Bash roles to the residual node, which owns `handoff_check.py`: "say in your digest that `<values file>` could not be renamed; the orchestrator removes it".
- E-10 names this as a known residual.

### F8 — fix in round. Key 5: R2-F6 calls a runtime refusal a cap, and the number it asks for is printed by no tool

`native_context.py:174-175`: `if len(context) > 100000: raise ValueError('Native context exceeds 100000 characters …')`. Past that point the role cannot launch on Codex at all. No ratchet is raised; the product breaks on one host. That is a product risk, and PROJECT.md "Что решать самому" puts product risks with the owner. The owner's word ("если не влезет можно поднять") speaks of raising caps, not of this.

E-9 also asks for "the bytes past 100,000", which nothing measures. K10 prints the share U against the headroom H (`role_load.py:334-345`).

The risk in practice is small. The largest share is qa-automator at 79,909 B (`role-load.json:38-42`), and the told-twice window adds about one card (cards are 939-1,197 characters, measured).

Edit, E-9 last sentence:
- A K10 rise, including a new `native_headroom` row, is named: `raise: <role> native_headroom <old> -> <new> (U-H = <n> B)`.
- A role whose plugin share alone (U) exceeds 100,000 B, so that no project could launch it on Codex: STOP before commit, and the Lead asks the owner.
- So R2-F6 becomes (b) for that one case, and stays (a) for every K10 rise below it.

### F9 — fix in round. E-b2 does not say how the walk is made to count 1 hand card while the stored number is 0

At stored 0, the "plus-one" form `update({counter: stored - 1})` writes -1 (`test_stage_joints.py:950-952`, P-2 confirmed). The floor form for legacy_legs works because `extra_leg` mutates the DATA. Hand cards, though, are read from `env.plugin/references/ahead-cards.json` (`stage_joints._hand_cards`, `:1163-1170`), which `mutated()` cannot reach. A weak model has to invent the way.

Edit, E-b2:
- The +1 row builds `env = copy.copy(ENV)` with `env.plugin` set to a temp dir that holds `references/ahead-cards.json` with one card.
- It calls `SJ.audit(copy.deepcopy(REAL), UNI, None, env, sited=set(UNI[0]))`. This is the pattern of `told/hand-cards-unreadable`, at `:957-960` on the wave B tree.
- Expected text: `told_ratchet.hand_cards is 0 but the walk counts 1`.
- The -1 row expects `a count (an integer, 0 or more) is expected`.

### F10 — note. Wave B moves line numbers but no row (P-1 settled)

`git diff HEAD...worktree-agent-ad0767bec786dddde -- references/stage-joints.json` shows a single hunk: `"unsited": 46` -> `17`. No row changed and no producer list was narrowed. The census narrowing lives in `judgment-census.json` and `told-ratchet.json`. So P-1 is settled, E-12 is vacuous, and the §7 sentence "rows … a T7a census narrowing can touch" rests on a premise that is false (it does no harm).

After the merge, line numbers do move:
- `validate_artifacts.py` cites shift by up to +9 after `:1711` (hunk `@@ -1711,10 +1711,19 @@`, and `check_triage_v0` goes from 2495 to 2504);
- the told loop of `test_stage_joints.py` goes from `:938` to `:939` (grep on both trees).

Edit: -b's owns scope names the loop by content ("the `for counter, up, down in` loop of `told_variants`"), not by `:938-955`.

### F11 — note. Collisions §7 does not declare (key 6)

- (a) RD1-1 (`plans/piles/rules-debt/batch-1-phase-2.md:29`) owns `references/common-rules.md` and `references/slices/*/common-rules.md`. That overlaps -a's and -b's `references/slices/`, and the common layer is part of the K10/A22 measure.
- (b) FV2-81 and FV2-82 (`plans/piles/live-run-fvf/batch-2-*.md:108-109`) own `test_contract_slices.py`, and so does -b (`:660-662`).
- (c) The driver-exits writers (F1).
- K1b (FV2-79) is still "ожидает" behind designer -> builder -> critic, so -a waits on a chain that has not started.

Edit: add order lines for (a)-(c), and tell the Lead that -a's start depends on K1b's whole chain.

### F12 — note. -b depends on the integrator commit, and that is not written down

-a raises `unsited`, which is a ceiling. So after -a, `stage_joints.py --check` is red ("told_ratchet.unsited is 17 but 23 rows have no site", `stage_joints.py:1143-1146`), and so is the exact K12 pin. They stay red until the integrator commits. Siting nodes only ever lowered the number, which is why F-1 (a) never met this. -b's DoD expects "unsited <the integrator's number>".

Edit, §7: "-a merges into the wave-C integration branch; the integrator raises `unsited` and the K12 pin by -a's named list in the same wave, before main; -b starts from that commit".

### F13 — note. The ts-3a K line gives `source_conflict` the wrong meaning

The planning_contract docstring (`planning_contract.py:1480-1482`) defines `source_conflict: true` as "sources disagree with each other or with the code" and `oracle_unknown: true` as "no settled expected value". The K line "An oracle you cannot settle is `oracle_unknown: true` with `source_conflict: true`" tells the strategist to set the conflict flag on every unsettled oracle.

Edit (bridge): "An oracle you cannot settle is `oracle_unknown: true`; add `source_conflict: true` when the sources disagree."

### F14 — note. The accounting sentence "No anchor stands in a K line (E-5)" is false for cd-4a

The fact of cd-4a, "One case per plan row", is the charter anchor of `role-rules.json:163` (`agents/qa-case-designer.md:23`). R-5 skips that K line because the fact is already present, so nothing breaks. Edit the sentence to: "cd-4a is skipped: its fact is the role-rules anchor already in the charter."

### F15 — note, class. Key 7: the EC-8 class is broader than the three corrections

- The existing sentences of the roughly 25 rows that -a appends to were not swept for over-claims; §3.3b and §3.3c were found by chance.
- The refusal text of `check_case_form` still says "inherited from the plan row" (`validate_artifacts.py:384`). That is the §3.3 defect on the refusal surface.

None of this gets harder to fix because of -a, provided the ec8 node can find the original sentence.

Edit:
- -a's report records each appended row's pre-append sentence verbatim, so TBW-T1rc-ec8 can replace it without touching the appended clauses (E-4).
- Queue to TBW-T1rc-ec8: a sweep of those rows' original sentences, and the `check_case_form` refusal text.

## Answers to the keys

1. **Facts by trail.** I spot-verified these as true:
   - T2: `told_ratchet` at `:8126-8129`, `UNSITED_CAP = 46` at `:927`.
   - T3: role-load `:38-42`.
   - T14: tools lines re-grepped.
   - T15: the 11 anchors read, and each lands in its §3.1 text. ts-3b, cd-1, cd-4b, cd-4e, cc-1, ds-2, rt-3, ts-3c and cd-2 each contain their anchor.
   - P-4: `contract_slices.py:786-795`. P-5: `source_preflight.py:7-50`. P-6: `check_witness.py:121-143`. P-14: `manifest_put.py:1292-1296`. P-17: `artifact_producer.py:14, 74-107`.
   - §3.3: `validate_artifacts.py:59, 376-407`. §3.3b: `planning_contract.py:1477-1505`.
   - The handoff_check rename at `:3199-3209`. The K counts (29 K, 7 NEW, 7 T/R, 4 M2), recounted from the table.

   P-2 is a failed premise, confirmed (`:950-952` writes -1). It hands -b the loop, which is right, but without a method (F9). P-1 ("still owed, git") I ran: no row changed (F10).

   Built on facts nobody read: the §4 rows (F4), "+4" (F2) and the axis-38 duty (F1).
2. **Can a weaker model run each card?** Files, fields and directions are named, and the forks are decided. What is missing:
   - full texts for about 15 segs (F3);
   - the r1 texts (F4);
   - the hand-card method (F9);
   - the driver-exits rows (F1).

   TEMPORAL (E-2, E-3) and POSITIONAL (E-4) carry their invariants. The order is TEMPORAL against the integrator only (F12).
3. **Meaning changes.**
   - R3-F1 measured on the bodies: both corrected sentences are true (§3.3b, §3.3c).
   - The new row `gate_preflight:question_branches` claims only what `variant_errors(at_cases_stage=True)` checks (`:1927-1941, 2054-2125`).
   - One sentence claims more than its body: sc-3 (F5).
   - The direction of the allowed error is stated only for the reader (E-11). The counters' direction (ceiling, raise named) is stated.
   - The meaning of a role-rules rule changes (F6).
4. **DOC-DISPATCH.** Not legal under that name: keep tests judge every owned path, and the keys are not verbatim (F3). It is legal as a supplementary check, with §3.4 added.
5. **Lead decisions.** R2-F6 hands the owner's product risk to "go on" (F8). R3-F2's "+4" is factually wrong (F2). R3-F3 is mislabelled (F3). R2-F1..F5, R2-F7 and R3-F1 contradict no rule, AR or P that I found. Where a pair of decided roads could clash (R2-F4 and R2-F5), I checked it (ONE ROAD line).
6. **Order and collisions.**
   - Wave B: no row overlap, only line shifts (F10).
   - K1b: ordered, not started (F11).
   - T9a: no shared file, only the integrator's `unsited` number.
   - T9c: ordered.
   - T10: Lead docs only, no overlap.
   - T3b: ordered after -b.
   - Undeclared: RD1-1, FV2-81 and FV2-82, the driver-exits writers (F11, F1).
   - `judgment-census.json`: neither card touches it. I simulated K5 on the wave B census with the M2 sentences added, and it stays `[]` (k5sim). So no census edit is owed.
7. **Class completeness.**
   - TBW-T1rc-ec8 holds the EC-8 lines. Add the sweep of existing sentences and the refusal surface (F15).
   - Axis 38 is missed (F1).
   - Axis 18 is covered by E-9, with F2 and F8 corrected.
   - Axis 34 is covered.
   - Axis 32 is unaffected: there is no census unit.
   - The FR-2 residual on the `values_rename` code door is queued (F7).
8. **Can it be built?** -a and -b are serial by design: they share stage-joints.json, slices, inject-map and role-load, so they are not parallel builders. The residual siting node can run in parallel with -b, since its scripts and `test_detector_verdict.py` do not overlap -b's owns, once F2 adds `s5_precheck.py` and `told-ratchet.json` to it. Buildable in the stated order after F1 and F12.

## What I did not check

- Every one of the 42 A segments against its body: about 18 were traced (F5 lists them).
- The accounting line's A=42.
- The `fingerprint.build` sentence beyond `execution_fingerprint.build:104-175` ("keeps its bytes while hashed" was not traced).
- The r1 texts of `sides.provisional` and `sides.pending` against today's bodies.
- K8, K10 and A22 numbers after -a, which were not measured.
- `role_rules.py --check` was not run.
- `test_validator_class.py:198-210` and the `test_ahead_cards.py` pin tables (-b's E-b1 targets) were not read.
- T8, T9 and T10 lines in `test-layers.json` and `slow_tests.json`, beyond what the witness-for run printed.
- Whether `NUMBER joints` in the dry census is a pinned count.

## Trail

Read:
- The r2 spec whole.
- finish spec §2, §3, lines 1-60, 140-160, 328-340, 425-480, and its F-1 grep.
- t-979 review (EC-8 and K5 lines).
- r1 §4 rows (`:41, :119, :140, :338-340`).
- `docs/TESTING.md:125-180`.
- `docs/SIBLING_MAP.md` axes 18, 32, 34, 38.
- `plans/piles/told-before-work/batch-1-finish.md` rows TBW1-10..14.
- `plans/piles/live-run-fvf/batch-2` rows FV2-79, 81, 82.
- `plans/piles/rules-debt/batch-1-phase-2.md:29`.
- Package:
  - `stage_joints.py:74-79, 291-342, 712-767, 1090-1265`.
  - `test_stage_joints.py:660-875, 920-962` (main and wave B).
  - `source_preflight.py:1-50`.
  - `check_witness.py:45-90, 115-200, 225-255`.
  - `exit_gate.py:110-150`.
  - `manifest_put.py:150-158, 1200-1310`.
  - `vocabulary.yaml:288-291`.
  - `estimate_record.py:60-115`.
  - `artifact_producer.py:10-110`.
  - `planning_contract.py:170-198, 1477-1505, 1880-1945, 2050-2128, 3995-4016`.
  - `coverage_contract.py:321-382`.
  - `validate_artifacts.py:57-60, 210-216, 376-410, 2495-2535`.
  - `contract.py:5012-5052`.
  - `gate_preflight.py:2108-2172`.
  - `handoff_check.py:3196-3212`.
  - `execution_request.py:170-180, 1815-1835, 3755-3775`.
  - `execution_fingerprint.py:104-175`.
  - `s5_precheck.py:266-298, 2100-2176, 2400-2432`.
  - `contract_slices.py:780-832`.
  - `role_load.py:302-345`.
  - `native_context.py:160-185`.
  - `role-load.json` whole.
  - `role-rules.json` 11 carrier lines.
  - `ahead-cards.json` cards.
  - `agents/*.md:4`.
  - `test_ahead_cards.py:166-200`.
  - the qa-case-designer page `:82-95`.
  - `dry_exits.py:521-532`.
  - the driver-exits folder listing.

Reruns and probes (scripts in the scratchpad `C:\Users\i_mas\AppData\Local\Temp\claude\b3e3188b390a00d9\501cb4e0-b55f-46d8-9262-11b1caefad61\scratchpad\`):
- `python -B ai-packages/qa-factory/scripts/stage_joints.py --check` -> `told counters: hand_cards 12, legacy_legs 0, unsited 46` / `stage joints: clean`.
- `sited.py` on main and on wave B -> the table in F2.
- `k5sim.py` on wave B -> `BEFORE []`, `AFTER M2 []`.
- `dryprobe.py` -> F1 output.
- `scenario_walk.py --witness-for references/stage-joints.json references/inject-map.json references/role-load.json agents/qa-scout.md agents/qa-code-critic.md` -> keep tests per path (F3).
- `git diff --stat e9d6195b HEAD -- ai-packages` -> 4 files (dry_stub, harness, story.json, a changelog fragment).
- `git diff HEAD...worktree-agent-ad0767bec786dddde -- references/stage-joints.json scripts/tests/test_stage_joints.py` -> the `unsited` line plus the K12 pin.
- Negative-claim greps, with controls: the new ids over `scripts/*.py`, all empty, with control `exit_gate:grounding` found at `exit_gate.py:1894`. `gate_preflight|source_preflight|estimate_record` over stage-joints.json returned only `role_cli:artifact_producer.py …` rows at `:7756, :7791`.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "F1: card -a adds 12 joints but owns no fixtures/driver-exits/*.json and runs no dry_exits.py --check; SIBLING_MAP axis 38 demands a census row in the same commit; probe on a copy: 1 new row -> dry_exits --check rc 1, '1 discrepancies'"
  ],
  "fixes": [
    "F1: -a owns scripts/tests/fixtures/driver-exits/ (rows of the 12 new joints, group by stages); DoD + dry_exits.py --check 0 discrepancies; unwalked raises named; siblings axis 38; order line vs driver-exits writers",
    "F2: unsited raise is +6 (sides.provisional, sides.pending unsited on main and wave B); R3-F2 line and E-9 corrected; residual node owns s5_precheck.py (_sides_provisional, _sides_pending) and told-ratchet.json",
    "F3: add section 3.4 with every landed text in full (incl. section 4 rows); key script quotes it; rename to supplementary key-presence check (the witness is scenario_walk; keep tests judge every owned path)",
    "F4: copy the r1 texts of the three section-4 rows inline; profile.none door = the refusal's own (execution_request.py:1827-1830) or a Lead fork; edge E-13: a clause the body no longer checks is not landed",
    "F5: sc-3 bridge conditioned on the file existing or being required (source_preflight.py:12-15); ck-3b critic_note owed with could_not_judge",
    "F6: -b restates role-rules.json :163 rule text to the cd-4b meaning, by a Lead decision",
    "F7: values_rename producers narrowed to the 9 Bash roles; the no-Bash door queued to the residual node (FR-2, E-10)",
    "F8: E-9 - a role whose plugin share alone exceeds 100,000 B stops before commit and goes to the owner (native_context.py:174 raises); K10 rises named as U-H",
    "F9: E-b2 names the +1 hand-card method: ENV copy with plugin = temp dir holding one card, SJ.audit(..., sited=set(UNI[0])), expected 'told_ratchet.hand_cards is 0 but the walk counts 1'",
    "F10: -b owns scope names the told loop by content, not :938-955 (wave B shifts it to :939)",
    "F12: section 7 - -a merges into the wave-C integration branch; integrator raises unsited and K12 before main; -b starts from that commit"
  ],
  "class_completeness": "Axis 38 missed (F1, blocking). Axis 18 covered by E-9 once F2 (+6) and F8 are corrected. Axis 34 holds (gate_preflight id differs by caller; ROLE+ vs witness sub-ids carry different texts). Axis 32 unaffected (no census unit; K5 simulated green on the wave B census). EC-8 class: TBW-T1rc-ec8 should also take a sweep of the original sentences of the ~25 rows -a appends to and the check_case_form refusal text (validate_artifacts.py:384); -a's report should record each pre-append sentence (F15). FR-2 residual on the handoff_check rename door queued (F7). Undeclared collisions RD1-1 (common-rules slices), FV2-81/82 (test_contract_slices) to order lines (F11).",
  "trail": {
    "read": [
      "docs/tasks/specs/20261117-told-before-work-t1r-cards-spec-r2.md (whole)",
      "docs/tasks/specs/20261117-told-before-work-finish-spec.md (sections 2, 3, card T5r/T9a/T9c lines, F-1)",
      "docs/tasks/specs/reviews/t-979-told-before-work-wave-a.md (EC-8, K5)",
      "docs/tasks/specs/20261114-told-before-work-t1r-cards-spec.md (section 4 rows)",
      "docs/TESTING.md:125-180",
      "docs/SIBLING_MAP.md axes 18, 32, 34, 38",
      "plans/piles/told-before-work/batch-1-finish.md; plans/piles/live-run-fvf/batch-2 FV2-79/81/82; plans/piles/rules-debt/batch-1-phase-2.md:29",
      "ai-packages/qa-factory/scripts: stage_joints.py, test_stage_joints.py (main and wave B), source_preflight.py, check_witness.py, exit_gate.py, manifest_put.py, estimate_record.py, artifact_producer.py, planning_contract.py, coverage_contract.py, validate_artifacts.py, contract.py, gate_preflight.py, handoff_check.py, execution_request.py, execution_fingerprint.py, s5_precheck.py, contract_slices.py, role_load.py, native_context.py, tests/dry_exits.py, tests/test_ahead_cards.py",
      "ai-packages/qa-factory/references: role-load.json, ahead-cards.json, stage-joints.json rows, slices/qa-case-designer/handoff-keys.md; design/role-rules.json; handoffs/vocabulary.yaml; agents/*.md:4"
    ],
    "reruns": [
      {"command": "python -B ai-packages/qa-factory/scripts/stage_joints.py --check", "result": "told counters: hand_cards 12, legacy_legs 0, unsited 46; stage joints: clean"},
      {"command": "scratchpad sited.py on main and on the wave B worktree", "result": "4 function rows and s5_precheck:sides.provisional/.pending unsited; witness sub-ids, profile.none, fingerprint.build, values_rename sited; unsited 46 / 17"},
      {"command": "scratchpad k5sim.py on wave B (M2 sentences simulated)", "result": "BEFORE [] AFTER M2 []"},
      {"command": "scratchpad dryprobe.py (dry_exits --check with stage_joints.DATA on a copy + 1 row)", "result": "REAL rc 0 '0 discrepancies'; COPY+1row rc 1 'FAIL joint source_preflight:check_source_inventory ... 1 discrepancies'"},
      {"command": "python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for references/stage-joints.json references/inject-map.json references/role-load.json agents/qa-scout.md agents/qa-code-critic.md", "result": "keep tests listed for every path (test_stage_joints, test_contract_slices, test_detector_verdict, test_role_load, test_validator_class, test_oracle_provenance, test_s5_precheck, ...)"},
      {"command": "git diff HEAD...worktree-agent-ad0767bec786dddde -- references/stage-joints.json", "result": "one hunk: told_ratchet.unsited 46 -> 17; no row changed"}
    ]
  }
}
```
