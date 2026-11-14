# t-826 — critic, one topic pass: P1B-9 (runtime-provenance record), merged C1-C5

Tree reviewed: `C:\QAFactory\forge-repo\.claude\worktrees\wave13` at e18e622f (read-only). Spec/DoD:
`docs/tasks/specs/20261114-p1b-9-runtime-provenance-null-outcome-spec-r2.md`. Merges: fbef5a3a (C1, first parent bc741cef),
caa63da8 (C2+C4+C5, first parent cfd3f902), e18e622f (C3, first parent caa63da8). The diffs were read against each merge's first parent.

## Verdict

| card | verdict |
|---|---|
| C1 runtime_probe one writer | GO |
| C2 recorded_checkout_revisions | GO |
| C3 own-run deriver | GO WITH FIXES (S-1 test rows, S-2 one form-dispatch helper) |
| C4 contract texts | GO WITH FIXES (S-3: one comment line is now false, one still says "identity") |
| C5 measurer | GO |
| **topic** | **GO WITH FIXES**: 0 blockers, 3 should-fix (this round, fresh fix worker), 5 queue lines |

Blockers: none. Nothing lets an `unknown` or a failed write become a pass, and no reader is starved (traced and probed below).

## Lead decisions

**(a) C4 trimmed to fit K10: partly upheld.**
- `s5-automator-to-critic.yaml:58-59`: upheld. The new text is true. `matched`/`person_confirmed` identify the build;
  `not_applicable`/`unknown` do not; ACCEPTS still lets a `not_applicable` run go ahead, but the record identifies nothing, and the
  text says only that. The dropped sentence ("the critic re-probes on the same stand; another build proves nothing") was not a
  requirement that any check judges, and no role decision depends on it. Code runs the critic's re-probe: `probe_by_code` ->
  `run_suite --request` red_probe (run_suite.py:471) -> the strict `probe_runtime` with ACCEPTS. So no FR-38/AR-10 requirement is
  lost.
- `s5-critic-to-automator.yaml:53` left as on main: **wrong, should-fix S-3**. The line does not say "identity". It says "The stand
  the probes ran on: the record the author handed over, re-read." Since C3 plus F6 (i), that is false.
  `probes.runtime_provenance` is in DERIVERS (handoff_check.py:639) and is filled from the CRITIC dispatch's own newest run block
  (its red-probe blocks carry the critic's `dispatch_id`, run_suite.py:575, :471), not from the author's record. Worse, when the
  critic window has no own block the field is blank (reason d), and this comment then tells the critic to type the author's record
  by hand. No check rejects a typed value (Q-L1), so the stale text leads the role onto the very cross-window road B1 removed for code.
- `s5-automator-to-runner.yaml:60` "The identity the freshness verdicts above were taken against": C4's own DoD (spec §3 C4) asked
  for "the identity" -> "the record (read its `result`)". It was left, and is now inaccurate (the record can be `not_applicable`).
  Should-fix S-3, same token-neutral treatment.

**(b) C1 deviations: upheld.**
- The `a2-reference` row stubs `reference_skip` (test_runtime_probe_onboarding.py:827-833). It pins the POSITION in `main`: a truthy
  `reference_skip` returns at runtime_probe.py:1670-1673, before any `write_record`. The real predicate is pinned separately
  (test_reference_window.py:181-191, test_stand_identity.py:995-1005; C1's witness ran test_reference_window 85/85). Together the
  two pins cover I-3. The stub's shape (`not_applicable`/`no_changed_file`, refs `[]`) mirrors the real A2.
- New function `every_answer_leaves_one_record_and_a_rehearsal_none` (test file :782-879) instead of extending :740-779. The old
  function stays the pin for the matched-family marker and the comparisons-equal claim; the new table is itself one parameterised
  loop with ids `<answer>-<mode>`. This is a cosmetic gap against TESTING.md's "one table per behaviour", not a defect. No action.

**(c) Writer/reader agreement: upheld, empirically.** The reader never reads a file name. It reads
`block.data.runtime_provenance.evidence_refs[0]` (handoff_check.py:549-551). The writer sets that to the file's own absolute posix
path, `_NN` suffix included, before serialising (runtime_probe.py:1580-1588). `run_suite.build_run_block` carries the request's
record into the block unchanged (run_suite.py:575, :581), and a reparse keeps the old `dispatch_id` and record (run_suite.py:787-791).
I probed the join myself (trail R2): three `write_record` calls in one second gave
`runtime-provenance-api-20261114T100000Z.json`, `..._02.json`, `..._03.json`. A block of dispatch D carrying the `_03` record ->
`window_runtime_record(task, "D")` = `evidence/runtime-provenance-api-20261114T100000Z_03.json`. The fields agree (`dispatch_id`,
`runtime_provenance`, `evidence_refs`) and the suffixes agree. The request digest and the fingerprint drop `evidence_refs`/`timestamp`
(execution_request.py:374-377, execution_fingerprint.py:131-133), so the refs that A3 records now carry do not change dedupe.

## Questions of the DoD

**1. Card DoD, edges, §2 invariants.**
- C1: all DoD rows exist and pass (729/729). There is one write site of `runtime-provenance-` (runtime_probe.py:1578, inside
  `write_record`; package grep, trail S1). SC-3 holds: `mkdir` over a file, and the all-99-taken `FileExistsError`, are both
  `OSError` and caught by the soft branch (:1592-1596); the strict branch re-raises. The A5 write comes after `finish_unknown`
  (:1279-1281). The A3 write comes after `reference_skip` and after `has_diff and not compared_files` (:1695-1703). I-1 is pinned on
  written records (`written-accepts`). I-2 is covered by the quiet rows. One edge has no row: an A6-A8 OSError under `soft=False`
  propagates. That is today's behaviour; no row is required.
- C2: matches the card. All edges have a row, including both callers. Control re-run 262/262 (R1).
- C3: steps a-g are implemented as written, and the POSITIONAL invariant in `check` holds. `underived` is reset per field
  (:1619), is read only when nothing was derived (:1633), only extends the blank text (:1657), and `kind` stays `blank`; the judge
  has no ROW_JUDGMENTS row for these keys (:1969-1972). The §2.2 adversarial inputs **with no row**: refs not a list, refs[0] not a
  string, an absolute path of ANOTHER story (drive or POSIX, without this story's folder name), a block with no `dispatch_id`, and a
  reparse block of this dispatch as the newest. I probed each (R2) and the code is on the safe side for all of them. The rows are
  missing: should-fix S-1.
- C4: see (a). C5: both edges have rows (`0 provenance records exist`, `unreadable 1`); 607/607.

**2. Cross-card joins as merged.**
- Pattern and vocabulary: one writer pattern. C2 derives its set from `profile_contract.PROVENANCE_RESULTS` (profile_contract.py:19)
  minus `unknown`/`not_applicable`, so there is no second word list. C5 counts whatever `result` says. C3 reads no `result` at all:
  the field is a path, not a verdict (I-1, row `own-not-applicable`).
- `not_applicable`/`unknown` are read the same way everywhere: neither binds a revision (C2, both callers), and neither is
  `acceptable_provenance` for `unknown` (C1 row).
- Readers that still choose by existence or by name: `driver_dispatch.walk_run_values` (driver_dispatch.py:1580, :1589), which
  names the last file by plain `sorted()`. C1 makes this WORSE in practice: A3/A5 files now exist, so the last name can be an
  `unknown` record of another profile. It is queued (L-2), but its pile home is a problem (Q-2 below).
  `null_outcomes.CONDITIONS["no_runtime_record"]` (:164) is reserved and not live (L-6).
- No package reader treats a record's existence as "identified". `handoff_check` has no verifier of the typed value
  (case-insensitive grep, `runtime.provenance|runtime-provenance` in handoff_check.py: only :520-644), which is Q-L1.

**3. FR-41 / FR-59 / AR-28 on the S5 road: no pass from an unknown.**
- A4/A5 are refused by ACCEPTS before any job, so no block and the field is blank (reason d).
- A failed A3 write gives refs `[]`, then the block, then reason e, so the field is blank. C2 then binds nothing, so the manual
  proof is refused.
- A failed A6-A8 write raises, the probe exits non-zero, and the strict reader refuses.
- An unreadable block anywhere gives reason c. A ref outside the story is refused: `_story_relative` rejects absolute paths, drives,
  roots and `..`. R2 cases `abs-other-story-drive`, `abs-posix-other`, `story-name-then-dotdot` and `ends-at-story` all gave None.
- The only way to put a non-own record in the field is a role typing one (Q-L1). That predates this node and is outside its DoD.

**4. AR-14 / AR-13.**
- AR-14: one write site (above), and the registry row was added (artifact-writers.json:180-183, test_artifact_writers 23/23).
- AR-13, private parses of the record FILE: `coverage_contract.recorded_checkout_revisions` (the package's one) and
  `check_all_contracts.s5_automator_to_critic` (outside the package, a measurer's own read, legitimate).
- AR-13, readers of "the record of a dispatch's run": `window_runtime_record` (one), plus `walk_run_values` by name (L-2). No
  second parser was born in this diff.
- One embedded resolver: the SC-5 tail rule (handoff_check.py:555-562) is inline, not a function. L-2's prescription "reused from
  `handoff_check`" therefore cannot be followed without extracting it, which belongs in Q-2's re-scope.

**5. Class completeness by the map (spec §4.3 axes).**
- Axis 5: I12 rows pending, unchanged.
- Axis 25: `proof_level` reads the inline record, and the fingerprint ignores refs, so n/a holds.
- Axis 32: the census is unchanged (judgment: none, test_judgment_census 25/25 per C3).
- Axis 34: residuals are L-2 and Q-L1 (below).
- Axis 36: C3 reads only `work/run-blocks` (row `reference-run-only`).
- Siblings outside the §5 queue: (i) the typed-value road, Q-L1; (ii) pile node FV2-67, whose text predates C3 and would build a
  SECOND reader, Q-2; (iii) the red ratchet on the base, Q-5. The rest are in §5.

**6. Duplication / code quality / architecture / judgment.**
- DUPLICATION: the form's dispatch is resolved in three derivers in two orders.
  - `_findings_file` handoff_check.py:179 (form_dispatch, header, dispatch).
  - The new `_runtime_provenance` :576-577 (the same order, re-typed).
  - `_review_receipt` :163-165 (header first, then `art.dispatch`).
  The new code copies :179 instead of sharing it: should-fix S-2. The precedence split at :163 predates this node: Q-4.
  - The SC-5 tail resolver vs `runtime_paths._under` (runtime_paths.py:578-598, which resolves "a record of another machine" by
    declared roots, case-folded). These are different problems: there is no known root here. The tail rule is case-sensitive: R2
    case `lowercase-story` gave None, which errs toward blank, the safe side. Queue note inside Q-2.
  - Grepped: `form_dispatch|header.dispatch` and `another machine|[::-1].index|def .*story_rel` over the package scripts.
- CODE QUALITY: `window_runtime_record` is 56 lines (handoff_check.py:517-572), nesting <= 2, no dead branches. The names and the
  docstring match the code. `write_record` is 34 lines. None found beyond S-2.
- ARCHITECTURE: the reports name AR-4, 13, 14, 23, 25, 28, 29 and 9/18. I walked producer->reader both ways: probe -> request ->
  block -> C3, and probe file -> C2/C5. No producer was removed.
- JUDGMENT: no check of a role's judgment was added. C3 joins on data (dispatch id, refs, file presence). The census rows
  (judgment-census.json:256, :675) are unchanged. No `craft` marker, no `blocks_override` added.
- RATCHETS: no row raised. role-load net 0 (C4 report; Lead re-run 186/186); census and form-rounds unchanged.

## Should-fix (this round; a fresh fix worker with this verdict and the files)

- **S-1** `ai-packages/qa-factory/scripts/tests/test_handoff.py` (`the_runtime_record_is_the_windows_own`, from :266). Add
  in-process rows from spec §2.2:
  - `refs-not-a-list` (`"evidence_refs": "evidence/x.json"`) -> None, "no evidence_refs";
  - `ref-not-a-string` (`[5]`) -> None, same reason;
  - `ref-absolute-other-story` (`D:/proj/artifacts/QA-8/evidence/<name>`, with the same name present in this story) -> None, "not a
    file of this story";
  - `block-without-dispatch-id` -> None, reason d;
  - `reparse-of-own-is-newest` (a `<attempt>-reparse-<h>.json` with `supersedes_block_id` carrying the copied record) -> its path.
  R2 shows the current code passes all of them; the rows pin it.
- **S-2** `ai-packages/qa-factory/scripts/handoff_check.py:576-577` and `:179`. One helper, `_form_dispatch(art, doc)`, used by
  `_findings_file` and `_runtime_provenance`, with the same order (form_dispatch, header.dispatch, dispatch). Do not change `:163`
  here (Q-4).
- **S-3** `ai-packages/qa-factory/handoffs/s5-critic-to-automator.yaml:53` and `s5-automator-to-runner.yaml:60`. Rewrite both
  comments token-neutrally (K10-b exact; measure with `test_role_load.py`). For example, :53 "The stand the probes ran on: the record
  of this review's own probe run." and :60 "The record (read its `result`) the freshness verdicts above were taken against." Do not
  touch placeholders. If no token-neutral wording fits, stop and return. Do not raise the ratchet (AR-20).

## Queue lines (homes proposed; the coordinator of the proper tier opens them)

- **Q-L1** (S5 contracts / handoff_check owner, P31 axis 34): a ROLE-TYPED `artifacts.runtime_provenance` /
  `probes.runtime_provenance` / `runtime.provenance` is never compared with `window_runtime_record`. It can name another window's
  record or no file at all (the typed rows at test_handoff.py:1391 stay green). Code fills the field by one road and the role by a
  second. Direction: when `window_runtime_record` answers a path and the typed value differs, refuse with that path as the door.
  Census class xref, owner data.
- **Q-2** (live-run-fvf pile, node FV2-67, `plans/piles/live-run-fvf/batch-2-live-run-fvf.md:94`, status "ожидает"): the node still
  prescribes a new `provenance_record(task_root, profile_id)` "by record label" and owns `handoff_check._runtime_provenance`. After C3
  that is a second reader of the same fact (AR-13, P31). Re-scope it to L-2 exactly: `walk_run_values` binds the start probe's
  `evidence_refs[0]` through a tail resolver EXTRACTED from `window_runtime_record` (one function, two callers). Drop
  `handoff_check.py` from its owns. Note there that C1 made L-2 more urgent (A3/A5 files now sort among the last names).
- **Q-3** (S5 contracts, L-8 neighbour): C1's TEMPORAL edge means stories probed before P1B-9 carry A3 inline records with refs `[]`;
  their S5 forms stop with reason e until the next run. This is expected, and the batch canon (cart-1, local-1-0108,
  `test_story_run_stand_identity.py:596`) will show it if a scenario `--fix`es an S5 form. Watch for it, no code.
- **Q-4** (handoff_check owner): `_review_receipt` (handoff_check.py:163-165) resolves the dispatch header-first, unlike the other two
  derivers. Pick one precedence and route all three through S-2's helper.
- **Q-5** (owner of `S5_PLAN_BRIEF_BYTES_MAX`): `test_brief_pack_s5_plan.py` is 249/250 on the base (9702 B vs 9559 B; C3 report
  FINDING 1, with a control against HEAD). Not this topic. It needs a B-line or a defect against the node that grew the brief.

ONE ROAD: two residual roads, each with a proposed node and owner, and no exclusion stays unnamed. (1) The S6 manual lane names its
record by file name (`driver_dispatch.walk_run_values:1580,1589`): L-2, carried by FV2-67, which must be re-scoped (Q-2) or it births
a second reader. (2) A role-typed provenance path bypasses the own-run reader: Q-L1. No language, project or case exclusion was added
by the diff. Grepped: the `runtime-provenance` family over the package (case-insensitive), DERIVERS consumers, `form_dispatch`.

## Spot-checks of the submitters' claims

- C1 claims "one write site": verified by grep (S1), with the writer line as positive control.
- C3 claims "no glob left": `grep -n -i "runtime-provenance"` on handoff_check.py found only docstring/reason text; the glob is gone.
  The positive control found coverage_contract.py:724/733 and driver_dispatch.py:1580 in the same call.
- C2 claims "the only other caller is manual_evidence": not re-scanned (spec §1.3 row 3 plus the plan critic). C2's own
  second-caller row exercises it.
- C3's witness caveat: the builder swapped `handoff_check.py` mid-sequence, so the tail of its keep-file runs may have used the old
  file. test_handoff 661/661 and test_field_producers 885/885 ran before the swap, and the Lead re-ran test_handoff (661/661) on the
  merge tree. Residual: test_story_step_start / test_triage_* / selftest were not re-run against the final file. They are cheap; the
  batch canon covers them.
- C3's measured wall time is ~81 s on a loaded machine vs 56.8 s in slow_tests.json:48. This is a note for the slow-list owner, not
  a finding.

## Trail

Read (wave13):
- The spec r2 (whole) and the four builder reports (whole).
- `docs/tasks/critic-diff-brief.md` 37-104.
- `scripts/runtime_probe.py` 1180-1329, 1556-1600, 1625-1730.
- `scripts/handoff_check.py` 156-185, 511-596, 1600-1661, 1969-1992, 2800-2839.
- `scripts/run_history.py` 50-119.
- `scripts/run_suite.py` 570-585, 712-731, 775-800.
- `scripts/execution_request.py` 368-382, 2435-2466, 2845-2876 (grep), 3250-3290, 3672-3716.
- `scripts/execution_fingerprint.py` 126-150.
- `scripts/profile_contract.py` 15-25, 725-754.
- `scripts/runtime_paths.py` 560-619.
- `scripts/driver_dispatch.py` 1570-1595.
- The diffs of all three merges against their first parents (the 12 files named in the dispatch, plus both changelog fragments).
- `handoffs/s5-critic-to-automator.yaml` 50-58 and `s5-automator-to-runner.yaml` 55-66.
- `docs/SIBLING_MAP.md` (axis headings, 606-616).
- `plans/piles/live-run-fvf/batch-2-live-run-fvf.md:94` (grep).

Searches (case-insensitive where content-negative; the positive control is in the same call):
- S1: `runtime-provenance` over the package minus tests, in `*.py|*.json|*.md|*.sh|*.ps1`. Found: artifact-writers.json,
  environment-preparation.md:51 (text), coverage_contract, driver_dispatch, null_outcomes, runtime_probe.
- `evidence_refs` across scripts: none of the inline-record readers check refs for non-matched results.
- `DERIVERS` consumers: only `check`, `_code_fills` and handoff_init (the version key).
- `form_dispatch|header.dispatch`.
- `no-evidence` callers.
- `reference_skip` in tests.

Re-runs:
- R1: `( cd .../wave13/ai-packages/qa-factory && python -B scripts/tests/test_manual_evidence.py | tail -1 )` ->
  `=== test_manual_evidence: 262/262 ok ===` (matches the attached witness).
- R2: an in-process probe, heredoc payload, temp folders only. Output verbatim (abridged to the result per case):
  `written names: [...Z.json, ...Z_02.json, ...Z_03.json]`;
  `join D: ('evidence/runtime-provenance-api-20261114T100000Z_03.json', ...)`; `C2 set: {'aaaa...'}`.
  None for: `refs-a-string`, `refs0-number`, `abs-other-story-drive`, `abs-posix-other`, `ends-at-story`, `story-dir-not-file`,
  `lowercase-story`, `story-name-then-dotdot`.
  `evidence/..._03.json` for `backslash-same-story` and `relative-plain`.
  `no-dispatch_id block, form D -> None`; `form blank -> None`.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "class_completeness": "Axes 5, 25, 32, 34 and 36 walked. Axis 34 residuals: driver_dispatch.walk_run_values by name (L-2, pile node FV2-67, which must be re-scoped so it does not build a second reader: Q-2) and the role-typed provenance path never compared with window_runtime_record (Q-L1, new). Axis 36 holds (work/reference-runs never read). Axis 25 n/a holds (the fingerprint and the request digest drop evidence_refs). Census unchanged.",
  "fixes": [
    "S-1 test_handoff.py the_runtime_record_is_the_windows_own: add rows refs-not-a-list, ref-not-a-string, ref-absolute-other-story, block-without-dispatch-id, reparse-of-own-is-newest (spec 2.2 adversarial inputs; the probe shows the code already passes them)",
    "S-2 handoff_check.py:576-577 and :179: one helper _form_dispatch(art, doc) shared by _findings_file and _runtime_provenance (same precedence); leave :163 to Q-4",
    "S-3 s5-critic-to-automator.yaml:53 is false after C3 and F6(i) (the field is the critic's own run record, not the author's) and s5-automator-to-runner.yaml:60 still says identity: rewrite both comments token-neutrally under K10-b; no placeholder edit and no ratchet raise"
  ],
  "trail": {
    "read": [
      "docs/tasks/specs/20261114-p1b-9-runtime-provenance-null-outcome-spec-r2.md",
      "docs/tasks/specs/reports/20261114-p1b9-c1-report.md",
      "docs/tasks/specs/reports/20261114-p1b9-c2-report.md",
      "docs/tasks/specs/reports/20261114-p1b9-c3-report.md",
      "docs/tasks/specs/reports/20261114-p1b9-c45-report.md",
      "docs/tasks/critic-diff-brief.md",
      "scripts/runtime_probe.py 1180-1329 1556-1730",
      "scripts/handoff_check.py 156-185 511-596 1600-1661 1969-1992 2800-2839",
      "scripts/run_history.py 50-119",
      "scripts/run_suite.py 570-585 712-731 775-800",
      "scripts/execution_request.py 368-382 2435-2466 3250-3290 3672-3716",
      "scripts/execution_fingerprint.py 126-150",
      "scripts/profile_contract.py 15-25 725-754",
      "scripts/runtime_paths.py 560-619",
      "scripts/driver_dispatch.py 1570-1595",
      "diffs fbef5a3a^1..fbef5a3a, cfd3f902..caa63da8, caa63da8..e18e622f",
      "handoffs/s5-critic-to-automator.yaml 50-58, handoffs/s5-automator-to-runner.yaml 55-66",
      "docs/SIBLING_MAP.md axis headings and 606-616",
      "plans/piles/live-run-fvf/batch-2-live-run-fvf.md:94"
    ],
    "reruns": [
      {
        "command": "python -B scripts/tests/test_manual_evidence.py | tail -1 (package dir, wave13)",
        "result": "=== test_manual_evidence: 262/262 ok ==="
      },
      {
        "command": "in-process probe: runtime_probe.write_record x3 in one second, run blocks of dispatch D, handoff_check.window_runtime_record and coverage_contract.recorded_checkout_revisions, plus 10 adversarial refs",
        "result": "suffixes .json/_02/_03 written; join names evidence/...Z_03.json; C2 binds only the matched revision; every adversarial ref outside the story gives None; same-story backslash and relative refs resolve; a block with no dispatch_id is never named"
      }
    ]
  }
}
```
