# t-1075 — plan critic on the P-b card (`probes.runtime_provenance` producer)

Under review: `docs/tasks/specs/20261117-p1b-pb-runtime-provenance-card.md`, the whole card, executed with the Lead's fork decisions (F1=B, F2=b, F3=b, F4=a, F5=a).
Critic: opus, 17.11.2026. This is a plan gate (PROJECT.md package item 6). The verdict is an input to the Lead's acceptance and decides nothing by itself.

**Verdict: ACCEPT WITH FIXES (NEEDS WORK before dispatch). 0 blocking, 6 FIX, 6 NOTE.**
The direction is right. F3-b is the truthful source, and the error direction is kept on every edge the card names. The fixes are
two edges that are named nowhere and whose J3 text is false, the operational form of F4-a, and one sibling that must be queued.
Each fix is a text edit to the card. None of them changes the design.

---

## Key 1 — facts by trail

Checked against the code (file:line) and the kept world. Every load-bearing fact holds, with one exception that needs a more precise wording (F-6).

| Fact | Verdict | Trail |
|---|---|---|
| A1, A2 | holds | `handoff_check.py:522-580` read whole: `bad` at :541, own-filter at :544-550, `own[-1]` at :555, tail rule at :563-576 |
| A3, A4 | holds | `:583-586`, `DERIVERS` at :644-651. `probes.runtime_provenance` appears in ONE contract only (grep `runtime_provenance` over `handoffs/`: `s5-critic-to-automator.yaml:55`), so rebinding the generic key affects no other form |
| A6 | holds | `run_suite.py:470-473` (`red_probe` -> None) and `:582` (the block copies `request.runtime_provenance`) |
| A7 | holds | `probe_by_code.py:2939-2961` and `:4674-4676`, `:6168`. Also: `while key in taken` (`:2958`) means every probe call gets a NEW job, so several qualifying jobs (E9) is the normal case, not an edge |
| A8 | holds | `execution_request.py:2841-2850`. The red probe keeps the copy |
| A9 | holds for the reading DICT | `run_suite.py:2904-2923`. `runtime_probe_before` is set before `store.begin` (:2989). `apply_resolved_ids` copies the request after :2923 (:2979), so the launched job keeps it. `_observed_while_building` (:1898-1907) returns None for a request built from a file (probe_by_code) and for a red-probe `--mine` that did not observe, so `probe_runtime` runs fresh. See F-6 for the FILE that `evidence_refs[0]` names |
| A10 | holds | `execution_request.py:404-518`. `.tmp` files do not match `*.json` (`write` at :431). `jobs()` drops a dict without `request`, so E13's "dict without request -> J2" matches the code |
| A11 | holds | `red_sandbox.py:1250-1263`. An omitted `--dispatch` is resolved by `--mine` to the active dispatch (`execution_request.py:3910`, `dispatch_id` comes from `find_active_dispatch`), so the red_sandbox road still lands under the critic's dispatch id |
| A12 | holds | `runtime_probe.py:1562-1596`: an exclusive create, refs set to the file's own path, `--no-evidence` gives `[]` |
| A13 | holds, MEASURED | Read-only dump of both job files of the kept world (rerun 1). Job `44bcd10c384267c69a56`: `S5-qa-code-critic-1`, `red_probe`, completed (`execution_status: failed`). `runtime_provenance.evidence_refs[0]` = `...075205Z.json` (the automator's), `runtime_probe_before.evidence_refs[0]` = `...075258Z.json`. The automator job `66bd1d15...`: both name `...075205Z.json`. All four evidence files exist (075205, 075211, 075258, 075303) |
| A14, A15 | holds | the contract read whole (`:53-55`). A case-insensitive grep `runtime_provenance\|provenance` over `agents/` gives 0 hits; positive control `window_record` gives 1 (`qa-code-critic.md`) |
| A16 | holds | `test_judgment_census.py:77`. None of the three new names matches the regex |
| A17 | holds | `test_handoff.py:257-430` read |
| A19 | holds | `known_red.json` read whole. The ledger reconciles BY ROW ID (`main/S5`), not by the text or the finding count (`dry_world.py:962-977`, `known_red.py:141`). That matters for F-4 |
| A20 | holds | rerun 2: 8 cart-1 jobs, all `completed` with a `runtime_probe_before` dict |

---

## Key 2 — meaning (item 6)

**Is `runtime_probe_before.evidence_refs[0]` of the newest completed own `red_probe` job a truthful value for "the record of this review's own probe run"?**
Yes, with the precision in F-6. The dict is the stand reading `run_suite` took at this probe's launch, after the launch check refused any
moved identity, profile or revision (`run_suite.py:2913-2922`). Each probe's precedent is the newest job of the profile, and every
launch is checked against it, so all readings in one window share one identity. The newest reading therefore never names a stand the
review did not run on. The rejected F3-a value (the precedent copy) is identity-equal too, but its FILE belongs to another dispatch's
launch (A13). F3-b is strictly better.

**The direction of the permitted error.** The card says (§4.1): blank when a record exists, and never a record this review did not probe
against. That is the correct direction. It holds on every edge the card names. It does NOT hold on the text that two unnamed edges print
(F-1, F-2): the field stays blank (safe), but the reason states a false cause and points to a door that does not work.

Per edge the Lead listed:

| Edge | Decided correctly? |
|---|---|
| unreadable jobs (E13/J2) | Yes. It mirrors `bad` on the run-block road. A corrupt job of ANOTHER dispatch blocks too: the Lead accepted that with F5-a (NOTE N-3) |
| several jobs (E9) | Yes. The order comes from the one reader. P11 (the exact tie) must assert MEMBERSHIP in the set of own jobs, never one specific winner, or the test takes its expectation from glob order (NOTE N-5) |
| a refused run | Yes. A refusal at the stand check comes before `store.begin`, so no job exists. A refusal from the budget/executor/begin also comes before the job. An exception after `begin` leaves `persisted` or `running`, then `incomplete` on recovery, and E7 excludes it |
| a job of another dispatch (E5) | Yes. Matched on the stripped `dispatch_id`. An S6-close probe carries the close dispatch's id, never the critic's |
| a run block present AND a job present (E3) | Yes. The block decides, and the positional invariant (item 2.4) is stated. For the critic this is legitimate: the critic's own run block is identity-equal by the same launch chain |
| the `red_sandbox --probe` road | Yes. The job store covers it (A11). With `--dispatch` omitted, the active dispatch is resolved (`execution_request.py:3910`) |

**Unnamed edges** (FIX F-1, F-2) below.

---

## Findings

### FIX

**F-1 (FIX): edge not named — a red-probe job with `runtime_required: false` (a local_source world).**
`run_suite.py:2904`: `runtime_probe_before` is set only when `request.get("runtime_required", True)`. A red probe copies
`runtime_required` from its precedent (`execution_request.py:2841`), and `runtime_required: false` + `target_kind: local_source` is a
supported request (`execution_request.py:164-176`). In that world every completed own `red_probe` job fails item 3 step 3's
`runtime_probe_before` filter, and the result is J3:
"this review ran no probe through run_suite, or every probe was refused before it started; ... probe_by_code.py ... runs the probe through run_suite".
Both causes are false: the review DID run its probes, and they were not refused. Re-running `probe_by_code` gives the same J3 again.
This breaks FR-1 (the text says what is wrong), FR-41 (an unknown said as a fact) and FR-2 (the door must be one the party can use).
§9.3 ("runtime_required is not checked separately") assumes the key is always true. The code does not support that assumption.
Correction: add edge E22 with a row. The behaviour has to be decided, and there are two candidates:
- (a) a distinct reason J6: "the probe runs of dispatch X ran with no stand to read (`runtime_required: false`), so run_suite took no stand reading; the field has no record by code";
- (b) take `request.runtime_provenance.evidence_refs[0]` for such a job. That is the run-block road's own source (A6), and in this world it is the only record that exists.

I recommend (a). It stays on the safe side. Whether (b) is the contract's meaning there is a fork for the Lead. The declared empty
outcome for this field is the reserved condition `no_runtime_record` (`null_outcomes.py:164`, `null-outcomes.json` row
`s5-critic-to-automator:probes.runtime_provenance`, `default: false`, I12). Name that as the eventual home and queue it, do not wire it here.

**F-2 (FIX): edge not named — the review ran no probe because every probe was answered by an earlier one (a repair round).**
`proof_level.already_probed` (`:1404-1430`) answers a probe from an earlier receipt or record on the same bytes, and
"nothing is to be written": `probe_by_code` then never calls `run_suite`, so the new critic dispatch (`S5-qa-code-critic-2..n`) owns no
job. Repair rounds are routine: cart-1's critic forms run up to `S5-qa-code-critic-7` (diagnosis `:74`). The result is J3 again.
"this review ran no probe through run_suite" is literally true here, but its door ("probe_by_code.py --dispatch <this dispatch> runs
the probe") answers "already probed" and runs nothing. The only exit left is a typed value, the road the diagnosis (`:76`) found
produces wrong values. The card's invariant ("never another dispatch's record") is correct, so blank is the right VALUE.
Correction:
- add edge E23 + a row;
- reword J3 so it does not promise a door that `already_probed` closes. For example: "... carries a runtime_provenance record: no probe of this review ran through run_suite (none was launched, every one was refused before it started, or every one was answered by an earlier probe's receipt); ...";
- name in the reason that the earlier run belongs to another dispatch.

Whether the contract wants the earlier probe run's record in a repair round ("this review's own probe run" when the review reused
probes) is a meaning question. It goes to the Lead/owner as a fork. It is not the builder's call.

**F-3 (FIX): J3's cause list is incomplete even without F-1/F-2.**
J3 is also the outcome when own red_probe jobs exist but are `running` / `persisted` / `incomplete` (E7), or lack the launch reading (E8).
"this review ran no probe ... or every probe was refused" is then false. Correction: J3 lists "not finished" as a cause, or J3 splits
into J3a (no own red_probe job at all) and J3b (own red_probe jobs exist, none completed with a stand reading: name the count and the newest
job's status). Both are joins, and neither creates a census unit. Rows P8/P9 then assert the J3b text.

**F-4 (FIX): F4-a as written leaves a red window on `main`, and a single main pass does not see all of it.**
- (i) The ledger reconciles by row id (`dry_world.py:966-977`). After P-a alone, the main pass still stops at S5, so `main/S5` stays red and is fine. After P-b, `main/S5` goes green, which gives `stale: ... remove its known_red row` = fail. A stop at S6 with no row is an UNLABELLED RED (`:488`). The Lead's line says "runs one main pass AFTER P-a and P-b merge". If P-b goes through `wave.py merge` first, `main` is red until the relabel lands: exactly F4-c, a `defect_found` known in advance.
- (ii) The exit groups (`walk_exits`, `dry_world.py:1353-1411`) run the main-pass PREFIX up to their latest start. Rows whose start snapshot was missing because of the S5 stop are a NOTE `after:FV3-20` today (`:1403-1406`). Once S5 passes they RUN for the first time and can be red in `known_red/<group>.json`. The canon reaches these parts (`.github/workflows/dry-story.yml:76`, called from nightly/canon). A local main pass never runs them.

Correction to F4-a:
- the coordinator merges `origin/main` (with P-a) INTO the P-b branch;
- on that branch it runs the main pass AND the canon's dry-only door (`python tools/ci_read.py start --ref <branch> --var dry_only=true`, the door named at `dry-story.yml:3`);
- it relabels `known_red.json` and any group ledger from what both show, as a coordinator commit ON THE P-b BRANCH;
- only then does it call `wave.py merge`.

The builder still does not touch the ledger. This is safe for the canon. "After merge" is not.

**F-5 (FIX, class-wide completeness, rule 5): the "copied runtime_provenance" sibling on the run-block road is named nowhere and not queued.**
The card rejects F3-a because a request's `runtime_provenance` can be a precedent COPY written for another dispatch's launch (A8). The run
block has the same property. `run_suite.py:582` copies `request.runtime_provenance` into the block. When a non-probe `--mine` could not
observe (`execution_request.py:2852-2853`, `runtime_observed: false`: no probe given, or a precedent with no `argv`), that value stays the
precedent's copy (`:2843-2844`). Meanwhile `run_suite` takes a fresh `runtime_probe_before` at launch (:2908, because
`_observed_while_building` returns None for `runtime_observed is False`). So `artifacts.runtime_provenance` / `runtime.provenance` can name
an earlier dispatch's file while the job holds this run's reading. That is the defect class this card fixes, on the twin road
(SIBLING_MAP axis 5, S5 automator/critic twins). F2-b keeps those roads byte-identical, which is right for this card, but the sibling
must be QUEUED. Correction: a finding in `live-run-fvf` (owner: the Lead): "the run block's `runtime_provenance` is the request's
(possibly copied) record, not `runtime_probe_before`; one road for all three provenance fields = the launch reading of the dispatch's
newest completed job". Add it to `siblings:` and §11. This is also the natural P31 follow-up: once measured, the three fields read one source.

**F-6 (FIX, the wording of a premise): `runtime_probe_before.evidence_refs[0]` is "the file the launch reading cites", not always "a file written at this launch".**
`probe_runtime` returns whatever JSON the registered probe printed (`execution_request.py:105-116`). With the factory's
`runtime_probe.py`, the refs name a file created exclusively at that call (A12). With a project's own registered probe argv, the refs are
whatever that script prints. A cart-1 fixture (rerun 2) shows every job of 5 dispatches citing ONE file, `work/evidence/s5-2-runtime.json`,
in both fields. So "the record written at THIS probe's launch" (A13 bullet 3, F3-b, E8's invariant) holds for the factory probe only.
The safety argument does not depend on it (the reading dict is fresh and identity-checked). But §4.1 and E8 must say "the record the
launch reading cites", or the next reader takes an unproved premise as a fact. The run-block road (A1) has the same property: no new exposure.

### NOTE

- **N-1:** `from pathlib import PurePosixPath` at `handoff_check.py:532`. After item 1 it is used only inside `_story_record`, so move the import into the helper. Otherwise an unused local import is left in `window_runtime_record`.
- **N-2:** `_probe_runtime_provenance` repeats `_runtime_provenance` except for one keyword (three lines). It is acceptable as a named data-row binding, the reason item 4 gives. A `functools.partial` would be shorter, but it would lose the docstring. No change required.
- **N-3:** J2's glob count re-encodes JobStore's file layout (`*.json` in one folder, "readable = dict with a `request` dict"), so it is a second statement of a fact that has a reader (AR-13, weak form). The Lead chose this over F5-c. Keep it, and add one line to the card's §1.1 AR-13 row naming the duplication and its drift risk. Also, a job file in the middle of `begin`'s O_EXCL create (`execution_request.py:457-471`) reads as empty and gives J2 for one moment. That is safe (blank), and a retry of `--fix` clears it.
- **N-4:** The test expression `H.Artifacts(task, dispatch=C)` is written against the pre-P-a constructor. P-a touches `Artifacts.__init__` (non-goals). By precondition 1 the builder reads the merged signature, so the card should say "the constructor as P-a leaves it".
- **N-5:** For row P11 (an exact tie of `updated_at` and mtime): assert that the answer is ONE OF the own jobs' records. Never assert a particular one: that winner comes from glob order, and asserting it would make the code its own oracle (FR-58).
- **N-6:** An `inconclusive` probe job (the stand moved between before and after, `run_suite.py:2353-2358`) still answers with the before reading (§9.4). That mirrors the run-block road. The `execution_status` carries the warning elsewhere. Acceptable.

---

## Key 3 — architecture and principles

- **AR-13:** kept. There is one reader (`window_runtime_record`), the jobs are read through `JobStore.jobs()`, and the tail rule is extracted. Weak duplication: N-3.
- **AR-14:** not touched. The card only reads, and `run_suite` stays the one writer of the job store.
- **AR-15 / P31 (critic rule 19):** not a second road. The shared reader is reached first, and the probe branch serves the task's own condition (a probe writes no run block, A6), selected by a `DERIVERS` key, which is a data row. The residual "one source for all three fields" goes into the F-5 finding, owner the Lead. It is not left as a line to pass on.
- **AR-22:** kept. The field gets a producer that the critic's road reaches.
- **AR-28 / FR-59:** kept for values. Every unknown is blank with a name. Broken for TEXT on F-1/F-2/F-3, where the reason states an unestablished cause as fact (FR-41).
- **AR-29 / P27:** kept. It is a join of dispatch, purpose, status and presence, and it refuses nothing. The census needs no row (A16).
- **FR-58:** kept, if P11 follows N-5.
- **A legitimate producer, or papering over a field the critic should not have?** A legitimate producer. The contract (`:54-55`) asks for exactly the stand the review's probes ran on. Probes launch through `run_suite`, which records that reading. The field is meaningful whenever a stand exists. Where none exists (F-1), the right home is the reserved empty outcome `no_runtime_record`, not removing the field.

## Key 4 — feasibility for a weaker model

Items 1-6 can be executed as written: functions, positions, exact strings, filters and order are given, and so is a row per edge.
- Expectations come from the contract (P1: file `b`, the launch reading), from the existing reader's order (P10), or from the invariants (P2-P4, P20, P21). None comes from the new code, except P11 (N-5).
- The fixes add two rows (E22, E23) and reword J3. Both stay executable without inventing an approach, provided the Lead picks F-1 (a) or (b) first.

## Key 5 — class-wide completeness

§7's sweep and its one scout question are enough for the EXISTENCE class (a deriver whose input the listing role's road never writes).
`artifacts.probes` is correctly flagged as first priority. One sibling of a different axis is left unnamed: the SOURCE-SEMANTICS class
("the run's record is a precedent copy, not the launch reading") on the run-block road (F-5). It is outside the scout question and must
be queued as its own finding. Inside the same artifact (`window_runtime_record`), the J3-cause defect also applies to its run-block twin
reason (`:552-554`: "this dispatch ran no test through run_suite, or its run was refused"). That twin is correct for the automator,
because a test run always writes a block. So the defect does not apply there: no neighbour to fix.

## Key 6 — F4 (a) and the canon

It is safe only in the operational form of F-4: the pass and the dry-only canon door run on the P-b branch after `origin/main` is merged
into it, the ledgers are relabelled on that branch, then the branch is merged. "After both merge" as written in the Lead decision leaves
`main` red (a stale `main/S5` row, or an unlabelled stop), and possibly red in group ledgers that a local main pass never walks.

## Standing questions

- **DUPLICATION AND CONSISTENCY:**
  - item 1 removes a planned duplicate (FV2-67's resolver);
  - residuals: N-2 (a three-line twin, accepted as a data-row binding) and N-3 (J2's re-encoded layout);
  - grepped: `execution_request|JobStore` in `handoff_check.py`: 0 hits; positive control `import run_history`: hit at `:537`.
- **CODE QUALITY:** N-1 (an import left behind). Otherwise the item texts are precise. Nothing blocking.
- **ONE ACTION, ONE ROAD (P31):** no exclusion of a language, project or case. The local_source world (F-1) is an ordinary condition that the shared mechanism reaches. It needs a decided reason, not a branch. The one-source residual goes into the F-5 finding, owner the Lead.
- **TESTS (budget):** one table function plus one variant in a KEEP `data_join` file, with a row per edge. Within the volume rule. Adding E22/E23 adds 2 rows.

## Proposed for the Lead (decisions belong to the Lead's tier)

1. Choose F-1 (a) or (b). The recommendation is (a).
2. Decide whether the repair-round meaning question of F-2 goes to the owner.
3. Rewrite the F4-a decision line in the form of F-4.
4. Open the F-5 finding in `live-run-fvf`.

## Trail

Read:
- the card (whole);
- `handoff_check.py:515-689`;
- `run_suite.py:466-476`, `578-584`, `912-951`, `1895-1924`, `2348-2358`, `2405-2418`, `2870-3004`;
- `execution_request.py:105-184`, `385-524`, `2301-2340`, `2780-2914`, plus greps for `red_probe`, `runtime_required`, `dispatch_id`, `load_run_budget`;
- `probe_by_code.py:2870-2969`, `4668-4680`, `6160-6172`, `8066`;
- `red_sandbox.py:996-1010`, `1250-1266`, `1595-1619`, `2170-2194`, `2264-2272`;
- `runtime_probe.py:1560-1599`;
- `proof_level.py:1404-1434`;
- `handoffs/s5-critic-to-automator.yaml` (whole), plus the `runtime_provenance` grep over `handoffs/`;
- `test_handoff.py:257-431`;
- `test_judgment_census.py:77`;
- `known_red.json` (whole);
- `dry_world.py:1352-1411`, plus the `known_red` grep over `tests/*.py`;
- `.github/workflows/dry-story.yml:1-40`, `76`;
- `null-outcomes.json:168-215`, `null_outcomes.py:164-165`;
- `docs/SIBLING_MAP.md` headings and axes 24, 25, 33, 34;
- the diagnosis t-1070 (grep).

Greps:
- `agents/`: `provenance` gives 0 hits; control `window_record` gives 1;
- `handoff_check.py`: `execution_request|JobStore` gives 0 hits; control `import run_history` hits at `:537`.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "class_completeness": "Existence class (deriver input not produced on the listing role's road): the card's sweep and its one scout question suffice, artifacts.probes is flagged first. Source-semantics sibling NOT covered: the run block copies request.runtime_provenance (run_suite.py:582), which is a precedent copy when the build did not observe (execution_request.py:2843-2853), while the job holds a fresh runtime_probe_before. Same defect as F3-a on the automator/runner twin road (SIBLING_MAP axis 5). Must be queued as a live-run-fvf finding (F-5). Same-artifact neighbour, the run-block J3 twin at handoff_check.py:552-554: not applicable, because a test run always writes a block.",
  "fixes": [
    "F-1: name edge E22 (red_probe job with runtime_required false, local_source; run_suite.py:2904 sets no runtime_probe_before) with a row. Decide (a) a distinct J6 reason that does not claim 'ran no probe' (recommended) or (b) request.runtime_provenance as the source. Point to the reserved null outcome no_runtime_record (null_outcomes.py:164) as its future home",
    "F-2: name edge E23 (a repair round where every probe was answered by proof_level.already_probed, so no job of this dispatch exists) with a row. Reword J3 so its door does not promise a probe_by_code run that already_probed closes. Return the repair-round meaning question to the Lead/owner",
    "F-3: J3 must list 'not finished / no launch reading' as causes, or split into J3a (no own red_probe job) and J3b (own jobs exist, none completed with a reading; name count and newest status). P8/P9 assert J3b",
    "F-4: restate F4-a. Merge origin/main into the P-b branch, run the main pass AND the canon dry-only door (ci_read start --var dry_only=true) there, relabel known_red.json and any group ledger as a coordinator commit on that branch, then wave.py merge. 'After both merge' leaves main red (stale main/S5 or unlabelled stop), and exits groups first walk rows past S5 (dry_world.py:1403-1406)",
    "F-5: queue a live-run-fvf finding for the run-block copy sibling (run_suite.py:582 vs runtime_probe_before) and add it to siblings: and section 11",
    "F-6: reword A13 bullet 3, F3-b, E8 and section 4.1 to 'the record the launch reading cites'. With a project's own probe argv the refs are whatever that script prints, not necessarily a file written at this launch (cart-1 fixture: 5 dispatches cite one file)"
  ],
  "trail": {
    "read": [
      "docs/tasks/specs/20261117-p1b-pb-runtime-provenance-card.md",
      "ai-packages/qa-factory/scripts/handoff_check.py:515-689",
      "ai-packages/qa-factory/scripts/run_suite.py:466-476,578-584,912-951,1895-1924,2348-2358,2405-2418,2870-3004",
      "ai-packages/qa-factory/scripts/execution_request.py:105-184,385-524,2301-2340,2780-2914",
      "ai-packages/qa-factory/scripts/probe_by_code.py:2870-2969,4668-4680,6160-6172,8066",
      "ai-packages/qa-factory/scripts/red_sandbox.py:996-1010,1250-1266,1595-1619,2170-2194,2264-2272",
      "ai-packages/qa-factory/scripts/runtime_probe.py:1560-1599",
      "ai-packages/qa-factory/scripts/proof_level.py:1404-1434",
      "ai-packages/qa-factory/handoffs/s5-critic-to-automator.yaml",
      "ai-packages/qa-factory/scripts/tests/test_handoff.py:257-431",
      "ai-packages/qa-factory/scripts/tests/test_judgment_census.py:77",
      "ai-packages/qa-factory/scripts/tests/fixtures/driver-exits/known_red.json",
      "ai-packages/qa-factory/scripts/tests/dry_world.py:1352-1411",
      ".github/workflows/dry-story.yml:1-40,76",
      "ai-packages/qa-factory/references/null-outcomes.json:168-215",
      "docs/SIBLING_MAP.md axes 24,25,33,34",
      "docs/tasks/specs/reviews/t-1070-p1b-main-s5-residue-diagnosis.md (grep)"
    ],
    "reruns": [
      {"command": "python -B -c (read-only json dump of DRY-1/state/execution-jobs/*.json: status, dispatch_id, purpose, runtime_provenance.evidence_refs, runtime_probe_before.evidence_refs)", "result": "job 44bcd10c384267c69a56 S5-qa-code-critic-1 red_probe completed/failed: provenance ...075205Z.json, before ...075258Z.json; job 66bd1d15b5fe5da442d7 S5-qa-automator-1 initial completed/passed: both ...075205Z.json; A13 confirmed"},
      {"command": "python -B -c (read-only dump of cart-1 state/execution-jobs/*.json)", "result": "8 jobs, all completed, all with a runtime_probe_before dict (A20 confirmed); every job of 5 dispatches cites one file work/evidence/s5-2-runtime.json in both fields (F-6)"},
      {"command": "ls DRY-1/evidence DRY-1/state/execution-jobs DRY-1/work/run-blocks", "result": "4 runtime-provenance records (075205, 075211, 075258, 075303); 2 job files; 1 run block (automator)"}
    ]
  }
}
```
