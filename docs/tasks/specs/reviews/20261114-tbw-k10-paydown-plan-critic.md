# Critic on plan, t-821: K10 pay-down draft (t-816)

Reviewed: `docs/tasks/specs/20261114-told-before-work-k10-paydown-spec.md` (designer draft), against branch `wip/tbw-t1r` at head
8d71532b (checked: `git -C .claude/worktrees/tbw-t1r log --oneline -1` printed `8d71532b tbw fix round: B1 ...`). Read only, nothing
written in the worktree. `W` = `C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r\ai-packages\qa-factory`. Every number below comes
from one of the commands C1-C6, listed in the trail with their verbatim output. The scripts are in the session scratchpad
`C:\Users\i_mas\AppData\Local\Temp\claude\b3e3188b390a00d9\61b75a79-16bf-492f-9cd2-02266607001d\scratchpad\` (`sec.py`, `rows.py`).

## Verdict

- **K0, K1, K2 (the Lead-level set): GO WITH FIXES.** There are 5 blocking fixes (B1-B5). Each is a spec edit the Lead makes before
  any dispatch; none needs new design. Measured here: three of K2's five levers save 0 bytes or drop a requirement a check judges, as
  written. K1's code-critic saving rests on a proof rule the draft changes without saying so.
- **K3 (form by path, owner fork F-2): GO WITH FIXES as an owner option.** It is real and legal before the work on the start,
  materialize, rebuild and resume roads. But the written form does not say which fields are required, and the page does today
  (S6). The price the owner is told must change: by measurement, K3 alone does NOT bring the automator under H (S1).
- **K4 (manifest_put rows at `--help`, F-3): NO-GO as the default.** FR-38 holds there by instruction only, not by a gate. It adds
  a third telling road beside the page and the refusal (P31). It saves 2,373 B, not 2,750 B, and it still does not close the
  automator.
- `ONE ROAD:` L1-L9 and L10 for every role stay on the existing two roads (the page row, and the refusal of a pre-action call). K4
  adds a third road (`help_told_families`), and S4 rejects it. L10 is one road only if the S8 bug-reporter self-init road is
  covered too (S5). No exclusion by language, project or case was found (searched: the draft's §3/§5 for role-name lists and
  "only for"; the one such option, F-2 (c), is already refused by the draft).

## Q1 FACTS: measured numbers

The K10 totals match the draft, at their carrier (C1: `contract_slices.py --check` from `W`):

| role | U (M, C1) | H (C1) | baseline (C1; `references/role-load.json` 38-40) |
|---|---|---|---|
| qa-automator | 81,385 | 68,400 | none |
| qa-code-critic | 74,417 | 68,400 | none |
| qa-test-strategist | 55,976 | 42,400 | 46,008 |

Each total also equals the sum of the per-file delivered bytes (C2), so the split by file is exact.

**qa-automator:**

| file | bytes |
|---|---|
| charter | 11,094 |
| manifesto | 5,925 |
| common-rules | 8,254 |
| key pages | 11,960 + 11,952 + 3,632 = 27,544 |
| execution-lifecycle | 7,112 |
| vocabularies | 652 |
| artifact-contract-automation | 11,329 |
| test-code-patterns | 9,475 |

**qa-code-critic:**

| file | bytes |
|---|---|
| charter | 12,146 |
| manifesto | 5,925 |
| common-rules | 9,010 |
| key pages | 11,806 + 7,456 = 19,262 |
| execution-lifecycle | 3,834 |
| code-review-rubric | 9,892 |
| artifact-contract-automation | 10,754 |
| test-code-patterns | 3,594 |

**qa-test-strategist:**

| file | bytes |
|---|---|
| charter | 8,927 |
| manifesto | 5,925 |
| common-rules | 5,523 |
| key pages | 11,917 + 5,824 = 17,741 |
| risk-policy | 3,525 |
| artifact-contract-plan | 9,233 |
| automation-candidacy | 5,102 |

Each draft estimate (E) against its measure (M). The "in" column answers: is the E within the draft's stated +-10 %?

| lever | role | E | M | in | command and basis |
|---|---|---|---|---|---|
| L1 | code-critic | 4,950 | 5,070 | yes | C4: 14 ER + 3 RS rows 6,892 - the four unproved rows 1,410 - index lines 412 |
| L1+L3 | code-critic | 6,420 | 6,480 | yes | C4 |
| L2 | automator | 2,950 | 3,056 | yes | C4: 10 request rows 2,709 + `stand.reference` 347 |
| L3 | automator | 1,110 | 1,035 | yes | C4: window_first 372 + stand 303 + begin 360 |
| L4 | automator | 535 | **799** | no | C4/C5: null_outcome.* 658 + findings_tooling 141; s7-automator-to-analyst has no `findings[]` (C5), so findings_tooling leaves the automator too |
| L4 | code-critic | 765 | **877** | no | null_outcome 658 + tried 219 |
| L4 | strategist | 645 | **799** | no | null_outcome 658 + findings_tooling 141 |
| L5 | all three | 380 / 190 / 190 | 352 / 176 / 176 | yes | C4: legend line 176 B per page |
| L6 | every role | 300 | **257** | no | byte length of the clause |
| L7 | every role | 330 | **278**, and **0 as written** | no | C6 and B3 |
| L9 | strategist | 1,000 | 907; **765 after the B4 fix**; **0 as written** | yes / no | C6 |
| L10 | automator | 4,600 | **3,686** | no (-20 %) | C3: `## Handoff form` section |
| L10 | code-critic | 3,000 | 3,182 | yes | C3 |
| L10 | strategist | 6,100 | 5,576 | yes | C3 |
| L11 | automator | 2,750 | **2,373** | no | C4: manifest_put rows 2,623 - 250 for the index line |
| L8 (card no-write sentence) | strategist | 450 | **355** | no | byte length of the sentence |

The section totals are close to the draft: "What code will check of you" plus the card measure 22,609 / 15,127 / 10,934 (C3). The
draft's estimates were ~22,000 / ~15,700 / ~11,350.

**§4 redone with measured numbers.** L7 is counted as if B3 were fixed, and L9 as if B4 were fixed (765 B). L8 and L13 stay
estimates (~800 B for the automator, ~250-320 B per page removed).

| role | now | after K1+K2 (M) | green line | after + L10 + L11 + L8 + L13 |
|---|---|---|---|---|
| qa-code-critic | 74,417 | 74,417 - 6,480 - 877 - 176 - 257 - 278 = **66,349** green, margin 2,051. Without L3: 67,759 (margin 641). Without K1: **72,829, red** | 68,400 | n/a |
| qa-automator | 81,385 | 81,385 - 3,056 - 1,035 - 799 - 352 - 257 - 278 = **75,608**, red +7,208 (+215 more after S2) | 68,400 | -3,536 - 2,373 - ~800 - ~320 = **~68,580, still red by ~180**. Without L3: red by ~1,200 |
| qa-test-strategist | 55,976 | 55,976 - 799 - 176 - 257 - 278 - 765 = **53,701**, red +7,693 / +11,301 (-212 more after S2) | 46,008 (42,400) | -5,426 - 355 - ~249 = **~47,671**, red +1,663 over the baseline, +5,271 over H |

So, on measured numbers, the draft's headline "qa-automator closes with L10 + L11" does not hold. Even with every fork taken, the
automator stays over H.

## Blocking findings

**B1. K1 changes the proof rule without saying so (L1, L3; edges E8/E10).** Today the rule is "proved = provoked by a test that
RAN". `test_contract_slices.py` 960-962 (the T1rs docstring): "a site proved there as F is proved; W (written, not run) and N (not
provoked) are not". The code at 980-981 follows it: `proved()` is true only on the `run_suite` road for ids outside
`unproved_site`. K1 E10 instead flips the proof constants in the same commit as rows that are written but not run. The provoking
rows sit in slow files that are never run locally: `test_probe_by_code.py` 221.4 s and `test_red_sandbox_probe.py` 61.4 s
(`scripts/slow_tests.json` 78, 92), and `test_execution_request.py` (20.9 s, listed in `slow_tests.json` line 36). So the marker
lands on rows of class W, which S-2 explicitly refused (S-2 report line 20; Q2: "may S-2 mark on a reachability reading before the
printed answers are provoked?").

- This changes the meaning of a gate between attempts (PROJECT.md package change item 6). It must be a fork, not an edge.
- E10's rollback path is itself a hidden raise. A red canon flips the marker back, which puts the rows back on the page, which
  RAISES the `role-load.json` `ratchet_tokens` / `process_ratchet_tokens` that K1 had just lowered (AR-20, axis 18).
- L3 is worse. S-1b (report lines 41-42) says `execution_request:stand` needs a live probe and `run_suite:begin` needs the whole
  launch; K1 just says "a provoking row" for them with no design. Under «Командная работа» п. 11, a node that makes the builder
  invent an approach is a Lead defect.

Fix:
- (a) Split K1 into two parts. K1a writes the provoking rows and the `refuse` printer. The canon runs them. K1b flips the
  constants after the canon is green, so the existing rule holds.
- Or (b) a Lead fork that changes the rule, with the ratchet-raise rollback named.
- Either way, drop `stand` and `begin` from L3 until a fixture design exists. The measured cost is 663 B for the automator and
  663 B for the code-critic. The code-critic stays green without them (67,759).

**B2. K2 item 1 joins contract writers "as `role_load._form_candidates`", and that join drops a judged requirement.**
`_form_candidates` (`role_load.py` 483-494) calls `handoff.contract_of(stage, role)` with no `to_role` / `purpose`. So it returns one
contract per stage. Measured (C5):

| role | `_form_candidates` returns | `handoffs/index.yaml` lists |
|---|---|---|
| qa-failure-analyst | `s7-analyst-to-automator` only | also `s7-analyst-to-scribe` (secondary), which IS in `TRIED_CONTRACTS` (`handoff_check.py` 1657-1659) |
| qa-automator | `s5-automator-to-critic` only | also `s5-automator-to-runner`, `s5-automator-plan-to-critic`, `s7-automator-to-analyst` |
| qa-code-critic | `s5-critic-to-automator` only | also `s5-critic-plan-to-automator` |
| qa-case-designer | `s4-designer-to-case-critic` only | also `s4-designer-to-runner` |

Built as written, `handoff_check:tried` leaves the analyst. `check_tried` (`handoff_check.py` 1699-1704) still judges the analyst's
S7-to-scribe form, so the role would no longer be told a requirement a check judges. That breaks the draft's own invariant, and
FR-38.

Fix: writers = every `from` of `handoffs/index.yaml` rows, secondary and purpose rows included, through the handoff module's one
reader of the index. Add a join-test row that checks a secondary contract.

**B3. K2 item 4 (L7) saves nothing as written, and its edge E4 contradicts the lever.** All 12 roles hold the row
`exit_gate:EG-digest-form` on their pages (C6: row 1 and block 1 on every role). So item 4 says "no marker at all". But
`contract_slices.parse` (124-127; 150-151: `roles = list(inherited)`) gives an unmarked `###` the roles of its `##`. That `##` is
marked `<!-- roles: all -->` (`references/common-rules.md` 69-70), so the block stays in every slice: 0 B saved, not 278 B.

E4 ("a marker that would exclude every reader: no marker") points the same wrong way: "no marker" means "every role reads it", not
"only the whole-file readers read it".

Fix: an explicit marker that excludes every role whose page holds the row. Check first that `ROLE_MARKER`
(`contract_slices.py` 61, `([^>]*?)`) gives an empty role list for `<!-- roles: -->`. Rewrite E4 as "no block unread by a role
that is judged on it and has no row for it". Add a test that the strategist slice lacks the block.

**B4. K2 item 5 (L9) is mechanically empty, and its designer check missed a requirement.**

- `HEADING = ^(#{2,3})\s+` (`contract_slices.py` 63). So `#### observation_contract fields ...` is not a heading. Its marker is
  then dropped as "a marker that turned out to head nothing" (156-162), and nothing moves: 0 B.
- The parent `##` is marked for `qa-test-strategist` alone (`references/artifact-contract-plan.md` 110-111). So "keeps every other
  role the parent marker lists" is an empty set.
- A `###` placed before the bullets would also capture the "A ref" bullet and the JSON example that follow them, unless they are
  re-headed.
- **LOSS:** the `surfaces` bullet says "`gap_reason` only on a `gap`". `observation_contract.py` 83-84 refuses it ("gap_reason is
  allowed only for a gap surface"). The row `coverage_contract:obligations.observation` (handoff-keys-2 line 7, quoted in C6)
  says only "a gap with a `gap_reason` ... any other with an `assertion_ref`". It never forbids `gap_reason` on a non-gap surface.

Fix: `###` heading(s) with an explicit order: kept bullets, then the moved block, then the strategist block re-opened for the JSON
example. Keep the `surfaces` bullet, or let a row-sentence edit (outside K2's non-goals, a Lead call) carry the clause. Measured
saving with `surfaces` kept: 765 B.

**B5. The owner question OQ-1 is false on measured numbers (Q8).** "I can shrink the test writer under the limit only if its
handover form is read from the file" is not true. Measured, L10 saves 3,686 B for the automator, not 4,600, and with every fork the
automator stays ~180 over H (~1,200 without L3).

Fix: re-state OQ-1 after K2 lands, with K2's measured U.

- Both roles need option (a) or (b), or the Lead-level L12 prose pass, which is unmeasured for the automator.
- K3 and K4 are not enough on their own.
- Name the code-critic's dependence on B1 (its green waits on the canon).

## Should-fix findings

**S1. Arithmetic.** Replace §4 with the measured table above. Also fix the §2.4 claim "automator kept: it writes
`s7-automator-to-analyst`": that contract has no `findings[]`, only `rounds[].finding` (C5). `check_findings` (`handoff_check.py`
1768-1770) reads `findings`, so findings_tooling leaves the automator too.

**S2. A row already lost before this draft, in the topic's own class; the draft missed it.** The row
`controller:s5_plan_gaps.rework_rows` has stages `["S3"]` and producers `["qa-test-strategist"]` (stage-joints, read through C6).
But its check fires only for the qa-automator plan dispatch in S5 (`controller.py` 6919-6940:
`if d.get("role") == "qa-automator"` ... `_plan_rework_rows_problems`). The automator's pages do not carry it: the grep found
`controller:s5_plan_gaps` only on automator page 2, and `.rework_rows` only on strategist page 1.

So FR-38 is already broken for the automator, and the strategist carries 212 B it can never be judged on. Fix in K2: correct the
row's stages to S5 and its producer to qa-automator (strategist -212 B, automator +212 B). Then walk the other `controller:*` rows
with the same question. That is a scout's job if it goes beyond this family (rule 5).

**S3. L1's cost column understates the price (P11/FR-55, AR-12).** The red_sandbox road refuses only AFTER `prepare()` has cloned
the sandbox and, for an own baseline, a second clone with install budget (`red_sandbox.py` 1645-1664, before the refusal at
1699-1714). "A refused call launches no test" is true, but it is not "one turn".

There is also an edge for the carry list. `told` carried in `_author_baseline` at 1430-1431 is printed only when a later run is
refused (1714). When the probe goes on, it is dropped. That site must not count as a printed carrier (E8).

**S4. K4 (L11): NO-GO as the default.**

- It adds a third telling moment (`help_told_families`) with no gate, so FR-38 holds only if the role runs `--help` first. The Lead
  already took manifest_put off the call list for exactly that reason (pages spec §10 B2 (1), cited by the draft itself).
- It is a second list beside `call_told_families`: a new road (P31, AR-15).
- It saves 2,373 B, not 2,750.

Keep it only as an owner-visible fallback, priced, after OQ-1.

**S5. K3 (L10): the road walk.** "The form exists before the role starts" holds on these roads:

- `start`: `_write_dispatch_files` writes the form at `story_step.py` 1203-1208, before the card at 1212.
- `materialize`: the same function, which keeps a form already on disk (1199-1201).
- the rebuilt card: `_rebuild_card` refuses to write a card while an owed form is missing (3145-3154).
- a resume: the form stays on disk.
- a repair: `_handoff_form` with `--carry-from` (355-358), before the card.
- a failed `handoff_init`: the card is written anyway (1209-1211). With no form, `finish` gets status `none` (411-416) and no
  handoff_check runs, so nothing is left untold.

**Exception:** `skills/qa-story/phases/s8.md` 223-224 tells `qa-bug-reporter` to run `handoff_init.py --stage S8` itself "after
filing". On that road the field list arrives after the filing work. F-2 (a) "for all roles" must either confirm that `start`
already wrote that form (then the phase text is a stale second writer, a separate finding) or make it a K3 STOP.

**S6. K3 loses the required/optional marks.** The page section marks each field `(required)` / `(optional)` / `(only when
blocked)` (automator page 1, `## Handoff form`). The written form carries placeholders and comments, with optional lists emptied
(`handoff_init.py` 191, 522), but no required mark (grep for `required` and `optional` in `handoff_init.py`: only argparse and
`empty_optional_lists`).

The rows `handoff_check:field.*` judge "every `required` field". If the form does not say which fields those are, the role is no
longer told a judged requirement. Fix: K3 adds the mark to the written form, through `handoff_init`'s renderer, or keeps the list.
Name it in the F-2 price.

**S7. F-1 (Q5): what the code enforces.**

- `role_load.py` 337-338: red only when `used > headroom and not (baseline is not None and used <= baseline)`. So the strategist is
  green at its baseline of 46,008.
- `test_contract_slices.py` 853-854 pins that rule. Line 863 pins the shipped package green. Line 865 pins
  `sorted(shipped) == ["qa-test-strategist"]` as a literal, so a raise for the automator (OQ-1 (a)) must edit that pin in the same
  commit.
- Nothing forces a baseline DOWN when U falls below it: there is no tightness check, so growth back up to 46,008 would pass
  silently.

Fix: when a role's measured U falls under its row, K1/K2 lower `native_headroom` to the measured U. Today the K1 non-goals make it
optional; it should be required (AR-20, axis 18). F-1 (a) is what the code enforces. (b) is stricter and unreachable, so the
recommendation stands.

**S8. K2 DoD item 5 runs `test_judgment_census.py` locally.** That file is slow (33.3 s, `slow_tests.json` 63), and PROJECT.md
package change item 2 says slow files are judged by the canon, not run locally. Fix: name it "judged by the batch canon".

**S9. K0 is largely done by this review.** C2-C6 measured every per-file and per-lever number, the writers (C5) and the digest row
on all 12 roles (C6). K0's remaining value is the demand tokens of form-carried rows, which are K3's. Fold K0 into K3's first step,
or keep it to 2 lines.

**S10. Untraceable citations.** The "Lead note 2a" / "Lead note 2b" the draft cites were not found in any carrier I read (grep for
"Lead note" and "2b" over the topic specs, reports and `docs/tasks`). The positive control: the same grep hit the draft itself at
lines 144-145. Fix: cite the carrier (journal event or file:line).

## Q2 FR-38 per option (verdict per "yes, still before the work")

| option | verdict |
|---|---|
| L1 | Holds on the pre-action refusals, but see S3. The probe_by_code walk row (6266, partial launch) is correctly excluded. |
| L2 | Holds: `validate_request` collects all errors before raising (`execution_request.py` 375-377). |
| L3 | Holds in meaning. Fails on proof (B1). |
| L4 | n/a once the join is correct. **Fails as written for the analyst (B2).** |
| L5 | Holds: page 1 is injected with every continuation. |
| L6 | Holds: the clause states what is NOT refused. |
| L7 | Would hold, but is mechanically void (B3). |
| L8 | Holds. |
| L9 | **Fails for the `surfaces` clause (B4).** |
| L10 | Holds on every road except the S8 self-init (S5), and only with the required marks restored (S6). |
| L11 | Holds only by instruction, so it is weak (S4). |

## Q3 LOSS

Three losses, plus one that predates the draft:

1. `handoff_check:tried` for qa-failure-analyst (B2).
2. "gap_reason only on a gap" for qa-test-strategist (B4).
3. Under K3, the required/optional marks behind `handoff_check:field.*` (S6).
4. Already on the branch: `controller:s5_plan_gaps.rework_rows` is untold to qa-automator (S2).

## Q4 The strategist

The conclusion is sound, and stronger on measured numbers: ~47,671 even with L10, L8 and L13. The draft missed these candidates
(measured with C4):

| candidate | bytes |
|---|---|
| the misassigned `controller:s5_plan_gaps.rework_rows` row (S2) | 212 |
| `exit_gate:digest`, a row whose requirement is "the form stated in row [EG-digest-form]" (all 12 roles) | 196 |
| three `handoff_check:field.*` rows with one identical requirement sentence (folding them would need a renderer change; at most) | ~380 |
| the card's no-write sentence, already in the row and in the slice: the requirement is told three times today | 355 |

Total: ~1,140 B. Without L10 the strategist stays ~6,500 over its baseline; with it, ~500 over. The rest of its load (risk-policy,
automation-candidacy, charter, manifesto) predates the baseline and is testing craft, not the rows. L12 there is a designer judgment
and cannot be measured by a read alone. So the strategist needs OQ-1, or L10 plus a measured L12.

## Q6 Order and buildability

K0 -> K1 -> K2 must be sequential: both K1 and K2 own `stage-joints.json`, `slices/`, `role-load.json` and
`test_contract_slices.py`. A weaker model cannot build them as written:

- B2: the wrong join.
- B3 and B4: zero-effect markup.
- L3 for stand/begin: no fixture design.
- S8: the DoD is wrong.

The owns lists, edges E1-E7 of K1 and the test tables are otherwise concrete. The exact DoD commands exist (`scenario_walk.py
--witness-for`, `contract_slices.py --write/--check`, `stage_joints.py --check`, `role_rules.py --check`, `selftest.py --limits
--lang`).

## Q7 Architecture

| invariant | verdict |
|---|---|
| AR-10 | Kept, except for B2, B4 and S6. |
| AR-11 | Kept. |
| AR-12 | The cost is understated (S3). |
| AR-20 | No card raises `native_headroom`. But E10's rollback is a hidden ratchet raise (B1), and lowering a baseline should be required (S7). |
| AR-29 | Code takes no judgment. But the J1 judgment ("does the row say all of it") that K2 asks the Lead to accept was wrong for `surfaces` (B4). |
| P27 | Kept. |
| One road | See the verdict section. |

## DUPLICATION AND CONSISTENCY (plan gate)

- The draft correctly reuses `stage_joints.told_line` as the one renderer, and `role_cli.refuse` as the one printer.
- One second reader is proposed: `_form_candidates` used as the writer join, beside `handoffs/index.yaml` as read by the handoff
  module. That is B2.
- Duplicates the draft missed: `exit_gate:digest` restates `EG-digest-form`; the three `field.*` rows share one sentence; the
  no-write requirement is told three times.
- Grepped: row bytes per check over the three roles' pages (C4); "Your final message IS the digest" over every role's common-rules
  slice (C6).

## CODE QUALITY (plan gate)

No code yet. One planned shape is risky: `refuse` grows an extra-records loop with a limit and a tail line (E5/E6). It stays small
only if the loop is a helper; name it in K1. "None found" otherwise: no long function is planned.

## What the owner should be told (plain words)

After the clean-up the Lead can order on its own, the code critic fits the limit. That still depends on one Lead decision: whether
a test that is written but has not yet run counts as proof (B1). The test writer and the test planner do NOT fit, even if you also
agree that the handover form is read from its file instead of being copied into the prompt.

Measured, that saves ~3.7 thousand characters for the writer and ~5.6 thousand for the planner. The writer would still be ~0.2-1.2
thousand over, and the planner ~1.7 thousand over its recorded ceiling. So the real choice is between three options:

- (a) Record a higher ceiling for both roles at the size measured after the clean-up: about 75.6 and 53.7 thousand. Price: Codex
  refuses the writer when the project's `framework-rules.md` is over ~18.8 thousand characters, and refuses the planner when its
  two strategy files together are over ~40.7 thousand.
- (b) Open a new piece of work so the factory hands large project files to Codex by path instead of pasting them. The direction is
  written down (Appendix A of the mechanism spec, lines 686-702) but it has no plan, size or date yet.
- (c) Do (a) now and (b) later.

The handover-form change is still worth your yes or no on its own: it costs every role one file read and saves 3-6 thousand
characters each.

## Trail

Read:

- the draft, whole
- `W\scripts\role_load.py` 290-430 and 483-503
- `W\references\role-load.json` 36-43
- `W\scripts\tests\test_contract_slices.py` 828-865 and 955-1014
- `W\scripts\role_cli.py` 79-130
- `W\scripts\import_test_receipt.py` 245-300
- `W\scripts\execution_request.py` 355-395
- `W\scripts\red_sandbox.py` 1395-1440 and 1575-1719
- `W\scripts\story_step.py` 330-420, 1170-1320, 1930-1975 and 3100-3170
- `W\scripts\native_context.py` 165-204
- `W\scripts\observation_contract.py` 60-153
- `W\scripts\controller.py` 6900-6960
- `W\scripts\handoff_init.py` 45-70
- `W\scripts\contract_slices.py` 61-63 and 124-164
- `W\handoffs\index.yaml` 1-120
- `W\handoffs\s5-automator-to-critic.yaml` 1-60
- `W\references\artifact-contract-plan.md` 108-175
- `W\references\risk-policy.md`, whole
- `W\references\stage-joints.json` 5306-5385 and 8210-8225
- the three roles' key pages (check and form sections)
- `slices/qa-test-strategist/common-rules.md` 22-40
- `skills/qa-story/phases/s8.md` 218-230
- the S-2 report, whole
- the S-1a / S-1b reports (grep)
- the mechanism spec, Appendix A (686-702)
- `docs/SIBLING_MAP.md` axes 28 and 34
- `docs/tasks/critic-diff-brief.md` 25-104
- `slow_tests.json` (grep)

Commands (each run from `W` through a `( cd ... && ... )` subshell, or with an absolute path):

- C1: `python -B scripts/contract_slices.py --check`. It printed three K10 lines: strategist 55,976 over 42,400 and over baseline
  46,008; automator 81,385 over 68,400, baseline none; code-critic 74,417 over 68,400, baseline none.
- C2: per-file `R._delivered_bytes` over `['plugin:agents/<r>.md'] + plugin entries of I.entries_for(r, m, 'first')`. It printed the
  per-file bytes listed in Q1, totals 81,385 / 74,417 / 55,976. `static_load` layers: charter 11,094 / 12,146 / 8,927; common 5,925;
  role 64,366 / 56,346 / 41,124; the form layer (not in K10) 8,258 / 4,590 / 8,526.
- C3: `sec.py` over the key pages. `## Handoff form` 3,686 / 3,182 / 5,576; check sections as in Q1; "Not yet in rows" 1,220 / 962 /
  1,211.
- C4: `rows.py` per `- [check]` line, `len(line.encode()) + 1`.
  - Families, automator: ER 6,218, s5_precheck 3,948, handoff_check 3,316, manifest_put 2,623, exit_gate 1,330, run_suite 475.
  - Families, code-critic: ER 5,998, run_suite 892.
  - Families, strategist: planning 1,648, coverage 1,560, exit_gate 1,139, validate 845.
  - Rows, all three roles: legend 176 per page; null_outcome.* 658; findings_tooling 141; tried 219; EG-digest-form 751.
- C5: `handoff.null_outcomes` / `handoff.spec` keys per contract of the index, and `_form_candidates` against the index `from` list
  for all 12 roles. Null outcomes: only s7-analyst-to-automator. `findings[].cause` and `tooling_findings`: only
  s5-critic-to-automator. s7-automator-to-analyst: only `rounds[].finding`. Analyst: `_form_candidates` misses
  `s7-analyst-to-scribe`, which is in `TRIED_CONTRACTS`.
- C6: L9 bullet bytes 126 / 97 / 142 / 276 (kept) / 217 / 249 / 76, moved 907. L7 digest block 278. Digest row and block present
  on all 12 roles.
- Negatives with their positive controls:
  - "rework_rows has no site literal": the grep returned nothing for `s5_plan_gaps.rework_rows`, but a widened grep of
    `controller.py` found `_plan_rework_rows_problems` at 6940 and 6946.
  - "Lead note has no carrier": the same grep hit the draft at lines 144-145.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "B1 K1 E10 flips proof constants on written-not-run rows (test_contract_slices.py 960-962, 980-981 say W/N are not proved): an unstated proof-rule change; the rollback raises role-load ratchets (AR-20); L3 stand/begin have no fixture design (S-1b lines 41-42)",
    "B2 K2 item 1 joins writers via role_load._form_candidates (one contract per stage): drops handoff_check:tried from qa-failure-analyst, which writes s7-analyst-to-scribe in TRIED_CONTRACTS (handoff_check.py 1657-1659, 1699-1704)",
    "B3 K2 item 4 (L7): an unmarked ### inherits the ## roles: all (contract_slices.parse 150-151; common-rules.md 69-70), so 0 bytes saved; E4 points the same wrong way",
    "B4 K2 item 5 (L9): a #### line is not a heading (contract_slices.py 63), so 0 bytes saved; moving the surfaces bullet drops 'gap_reason only on a gap', judged at observation_contract.py 83-84 and absent from the row",
    "B5 OQ-1 is false on measured numbers: L10 saves 3,686 B for the automator, not 4,600; with every fork the automator stays about 180 over H, so the owner question must be restated with K2's measured U"
  ],
  "class_completeness": "Class: a row told to roles its check cannot judge, or not told to a role it judges. The draft covers null_outcome, findings_tooling and tried. Missed on the same axis: controller:s5_plan_gaps.rework_rows (S3/strategist in data; fires only for the S5 automator plan, controller.py 6919-6940). The remaining controller:* rows need the same question: a scout request to the coordinator if it goes beyond this family. SIBLING_MAP axis 18 (ratchets): E10's rollback raise and the native_headroom lowering (S7). Axis 34 (one road): K4 adds a third telling road; L10 must cover the S8 bug-reporter self-init road. Axis 28 (render site of a form) is analogous for L10: the form file becomes the one carrier of the field list.",
  "fixes": [
    "B1: split K1 into K1a (provoking rows + refuse printer) and K1b (flip the constants after a green canon), or open a Lead fork that changes the proof rule and names the ratchet rollback; drop stand/begin from L3",
    "B2: writers = every 'from' of handoffs/index.yaml, secondary and purpose rows included; add a join-test row for a secondary contract",
    "B3: an explicit exclusion marker for roles whose page holds EG-digest-form (verify that ROLE_MARKER gives an empty list); rewrite E4",
    "B4: use ### headings with an explicit order; keep the surfaces bullet, or carry the clause in the row (a Lead call); measured saving 765",
    "B5/S1: replace the 4 tables with the measured ones and restate OQ-1 for both roles",
    "S2: correct the stages and producer of controller:s5_plan_gaps.rework_rows to S5/qa-automator in K2",
    "S3: state the red_sandbox prepare cost; exclude the _author_baseline told at 1430-1431 from the carry proof",
    "S4: K4 not the default; keep it as a priced owner fallback only",
    "S5/S6: K3 covers the S8 self-init road and adds required/optional marks to the written form, or STOPs",
    "S7: require lowering native_headroom to the measured U; the raise card edits test_contract_slices.py 865",
    "S8: mark test_judgment_census.py as judged by the batch canon in the K2 DoD",
    "S9: fold K0 into K3's first step",
    "S10: cite the carriers of Lead notes 2a/2b"
  ],
  "trail": {
    "read": [
      "docs/tasks/specs/20261114-told-before-work-k10-paydown-spec.md",
      "W/scripts/role_load.py 290-430, 483-503",
      "W/references/role-load.json 36-43",
      "W/scripts/tests/test_contract_slices.py 828-865, 955-1014",
      "W/scripts/role_cli.py 79-130",
      "W/scripts/import_test_receipt.py 245-300",
      "W/scripts/execution_request.py 355-395",
      "W/scripts/red_sandbox.py 1395-1440, 1575-1719",
      "W/scripts/story_step.py 330-420, 1170-1320, 1930-1975, 3100-3170",
      "W/scripts/native_context.py 165-204",
      "W/scripts/observation_contract.py 60-153",
      "W/scripts/controller.py 6900-6960",
      "W/scripts/handoff_init.py 45-70",
      "W/scripts/contract_slices.py 61-63, 124-164",
      "W/handoffs/index.yaml 1-120",
      "W/handoffs/s5-automator-to-critic.yaml 1-60",
      "W/references/artifact-contract-plan.md 108-175",
      "W/references/risk-policy.md",
      "W/references/stage-joints.json 5306-5385, 8210-8225",
      "key pages of the three roles",
      "skills/qa-story/phases/s8.md 218-230",
      "reports/20261114-t1r-sites-s2-report.md",
      "mechanism spec Appendix A 686-702",
      "docs/SIBLING_MAP.md axes 28, 34",
      "docs/tasks/critic-diff-brief.md 25-104"
    ],
    "reruns": [
      {"command": "python -B scripts/contract_slices.py --check (from W)", "result": "K10: strategist 55,976 > 42,400 and > baseline 46,008; automator 81,385 > 68,400; code-critic 74,417 > 68,400 (matches the draft)"},
      {"command": "per-file R._delivered_bytes over the plugin entries (the draft's 2.1 command)", "result": "per-file sums 81,385 / 74,417 / 55,976; key pages 27,544 / 19,262 / 17,741"},
      {"command": "sec.py over the key pages", "result": "Handoff form 3,686 / 3,182 / 5,576"},
      {"command": "rows.py per-row bytes", "result": "null_outcome 658, findings_tooling 141, tried 219, legend 176; ER+RS code-critic 6,892; manifest_put automator 2,623"},
      {"command": "contract join via handoff.null_outcomes/spec and role_load._form_candidates against index.yaml", "result": "analyst _form_candidates misses s7-analyst-to-scribe (in TRIED_CONTRACTS); s7-automator-to-analyst has no findings[]"},
      {"command": "L9/L7 byte measure and the digest row/block on 12 roles", "result": "moved 907 (765 with surfaces kept); digest block 278; all 12 roles hold both"}
    ]
  }
}
```
