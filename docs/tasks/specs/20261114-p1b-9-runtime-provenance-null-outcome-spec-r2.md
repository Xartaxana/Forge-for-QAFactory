# P1B-9 r2 — every answer of the runtime probe has a record, and the S5 form names the record of its own run (t-809)

Status: REVISED DRAFT by designer (fix round of t-790 after plan critic t-800) for Lead acceptance.
Inputs: the r1 spec (worktree wave13 `docs/tasks/specs/20261114-p1b-9-runtime-provenance-null-outcome-spec.md`), the critic verdict
`docs/tasks/specs/reviews/20261114-p1b-9-plan-critic.md` (GO WITH FIXES), and the Lead decisions quoted in §2.3.
Product tree: every line number below was re-read in `C:\QAFactory\forge-repo\.claude\worktrees\wave13` (origin/main). Paths are
relative to `ai-packages/qa-factory/` unless they start with `docs/`, `experiments/` or `plans/`.
This file is self-standing: a builder reads only it (plus the rule files named in each card's `given`).

---

## 0. Verdict item -> what changed, where

| item | what changed | where in r2 |
|---|---|---|
| B1 (deriver = last by file name; new A3/A5 files mask the window's record) | Lead decision applied: F3 = (ii) NOW. The deriver binds to the run block of the form's OWN dispatch: block field `dispatch_id` (written by `run_suite.build_run_block`, `scripts/run_suite.py:575`, from the request) equals the form's dispatch (`Artifacts.form_dispatch` = form file stem, `scripts/handoff_check.py:81`, set at `:2919` and `:3088`); the record is that block's `runtime_provenance.evidence_refs[0]` (written by `runtime_probe.py`, copied inline at `run_suite.py:581`). Absent at any step: named `unknown` (field stays blank, the refusal carries the reason), never a pass. File-name order is no longer read by this deriver. | §2.1 I-6, §2.3, Card C3 |
| B1 sub-fix: suffix reorders | S2 replaced: exclusive create (`open(..., "x")`), collision suffix `_NN` (02..99) which sorts AFTER the unsuffixed name (`_` 0x5f > `.` 0x2e), so name order equals write order within one profile and second. | §2.4 SC-2, Card C1 |
| B2 (C2 flips keep fixture `test_manual_capture.py:1351-1363`) | `scripts/tests/test_manual_capture.py` joins C2's owns; the seed gets `"result": "matched"`; expected behaviour stated per row. Second caller of `recorded_checkout_revisions` (`scripts/manual_evidence.py:108,128-132`) added to the inventory with its behaviour per outcome. | §1.3 row 3, Card C2 |
| S1 (contract texts say the file IS the stand identity) | Edited in an owned path: Card C4 edits the comment lines and one `what:` line of three S5 contracts. Placeholders (`<...>`) unchanged, so the generated slices `references/slices/*/handoff-keys.md` (writer `scripts/contract_slices.py:71,541`) do not change. s6/s7 lines (`s6-runner-to-analyst.yaml:41`, `s7-analyst-to-automator.yaml:74`) are neutral placeholders: n/a, reason in C4. | Card C4 |
| S2 (I-1 on WRITTEN records unpinned) | C1 rows: `profile_contract.acceptable_provenance(<record read back from disk>, ACCEPTS)` is True for A3, False for A4 and A5. | Card C1 tests |
| S3 (A4/A5 rehearsal rows; file == printed; A5 write position) | C1 rows for A4/A5 under `--no-evidence`; every `*-writes` row asserts file JSON == printed record; POSITIONAL: the A5 write comes after `finish_unknown` (`runtime_probe.py:1285-1322`). | Card C1 |
| S4 (fold L-4: writer row) | C1 adds `references/artifact-writers.json` row `evidence/runtime-provenance-*.json` -> `runtime_probe.py`. Checked: it does NOT change the guard (`guard_pre_tool.owned_artifacts`, `scripts/guard_pre_tool.py:980-1018`, maps a script writer to a role only through `REGISTRY_ROLE_BY_SCRIPT`, `:958`, which names `manifest_put.py` and `finalize_task.py` only), so L-3 stays open. | Card C1, §5 L-3/L-4 |
| S5 (P31 residual: reserved `no_runtime_record`) | Queued L-6 to t-305 N2. | §5 L-6 |
| S6 (F2 rationale overclaimed; `run_witness` sibling) | F2 text corrected: an A4/A5 run is refused before it starts, writes no run block, so with F3 (ii) its record is named by NO form; F2 (ii) gives the record on disk (one road) but frees no window. L-7 queued. | §2.3 F2, §5 L-7 |
| S7 (test_handoff.py at the one-minute line) | C3's new rows are in-process calls (no subprocess per row, < 1 s); the one existing subprocess fixture is extended, not duplicated. The builder reports the file's measured wall time. | Card C3 |
| S8 (A6-A8 beyond the suffix bound) | Stated: beyond `_99` an A6-A8 write raises `FileExistsError` (today's class of a failed write for these answers: no record printed, the caller refuses); never an overwrite. A3/A4/A5: soft (SC-3). | §2.4 SC-3, Card C1 edges |
| S9 (measurer `check_all_contracts.py:285-290`) | Card C5 relabels it and counts the records per `result`. | Card C5 |
| S10 (line drift) | Every line re-read on main: `driver_dispatch.py:1580,1589`; `null-outcomes.json:177,178,183`; `test_scenario_dry_1.py` does not exist on main (F4 needs no file); r1 claims "K17 and K26 flip" were WRONG on main — both run `--no-evidence` (`test_runtime_probe_onboarding.py:1469`, `:2015`), they stay; the only pinned flip in that file is W4 `:1044-1045`. | §1, Card C1 |
| DUPLICATION note (second list of result words) | No new list: C2 derives the binding set from `profile_contract.PROVENANCE_RESULTS` (`scripts/profile_contract.py:19`) minus `unknown` and `not_applicable`. | Card C2 |
| L-1 claims verifier | kept, unchanged class, queue | §5 L-1 |
| L-2 three glob readers / "newest" | re-worded: the premise was "last by name". The S5 deriver is fixed by C3; what remains is `driver_dispatch.walk_run_values` (`:1580` plain `sorted()`, `:1589`), a S6 manual lane with no run block: queued as a node with owns and test (P31 residual). | §5 L-2 |
| L-3 no guard names the family | stays open (S4 row does not reach the guard, verified above) | §5 L-3 |
| L-4 registry row | closed by C1 (row added); residual: the `work/evidence/` row still lists `runtime_probe.py` as machinery (`artifact-writers.json:184-193`) though the probe never writes there — queued, not edited (the machinery list may be read by other checks). | §5 L-4 |
| L-5 `story_step finish` "checks each exists" comment | kept as queue (critic found only other `is_file()` sites in `handoff_check.py`) | §5 L-5 |
| L-6 (new, critic) | `no_runtime_record` retire / re-scope | §5 L-6 |
| L-7 (new, critic) | `run_witness` (and now the provenance field) of a run refused by `ProvenanceRefused` | §5 L-7 |

New in r2 (not verdict items): forks F6, F7 (§2.5); queue lines L-8, L-9, L-10 (§5).

---

## 1. Inventory (measured on main, file:line)

### 1.1 Every answer of `runtime_probe.py` (no `--suggest`)

| # | answer | decided at | file written today? | after this node |
|---|---|---|---|---|
| A0 | exit 2, no JSON: no `--task` and no running story | `scripts/runtime_probe.py:1627-1633` | no (call refusal, FR-46) | unchanged |
| A1 | exit 2, no JSON: no `--checkout` | `:1639-1643` | no (call refusal) | unchanged |
| A2 | `not_applicable` / `no_changed_file`, reason `REFERENCE_REASON` (`:1565`): `--environment` names a reference stand | `reference_skip` `:1568-1587`, printed `:1635-1638` | no | unchanged: never written (I-3) |
| A3 | `not_applicable` / `no_changed_file`: a recorded diff touches no file of the checkout | `:1660-1669` (docstring rung 0 `:22` "No rung, no write."; comment `:1661-1664`) | no | written (C1) |
| A4 | `unknown` / `no_expected_revision`: the checkout names no commit | `:1670-1675` | no | written (C1, F2 ii) |
| A5 | `unknown` at the end of the ladder (docker down, nothing answered, device, voided word, `asks_person`) | `Reading.finish` `:1271-1283` -> `finish_unknown` `:1285-1322` | no (`finish` writes only at `:1279-1280`) | written after `finish_unknown` (C1, F2 ii) |
| A6-A8 | `matched` / `mismatched` / `person_confirmed` | `Reading.finish` -> `write_evidence` `:1324-1334` (name `:1330-1331`, refs `:1332`, set BEFORE the write) | yes | same answer; write through `write_record` with exclusive create (C1) |
| A9 | any of A3-A8 under `--no-evidence` (rehearsal) | `write_evidence` `:1326-1329` | no (FR-45); A6-A8 get `observed_without_evidence: true` | unchanged; A3/A4/A5 get no marker |

### 1.2 Who takes the printed answer (run path, unchanged by this node)

- `run_suite.probe_runtime` `scripts/run_suite.py:915-929`, through `profile_contract.acceptable_provenance` `scripts/profile_contract.py:893`
  with `ACCEPTS` `:875` = (`matched`, `person_confirmed`, `not_applicable:no_changed_file`): A3 TAKEN, A4/A5 refused (`ProvenanceRefused`
  `:929`) before any job, so no run block exists for them.
- `execution_request._observe_stand` `scripts/execution_request.py:2843-2876` puts the probe's record into the request
  (`runtime_provenance`); `_observe_precedent` `:2801-2840` may COPY an earlier request's record (timestamp replaced, `:2807-2808`;
  a red probe always copies, `:2814`). So a block's inline record is the record the run CARRIED, possibly an earlier one of the story.
- `run_suite.build_run_block` writes `dispatch_id` `:575` and `runtime_provenance` `:581`; `write_run_block` `:719-731` writes
  `work/run-blocks/<%Y%m%dT%H%M%S%fZ>-<attempt>.json` with exclusive create; a reference-stand run goes to `work/reference-runs`
  (`block_folder` `:712-716`), never into `work/run-blocks` (W1).
- The one block order: `run_history.read_run_blocks` `scripts/run_history.py:59-...` ("ONE total order for every reader": time,
  reparse depth, name; returns `(blocks oldest first, unreadable names)`); a reparse block copies the old block's
  `runtime_provenance` (`run_suite.py:791`).

### 1.3 Every reader of `evidence/runtime-provenance-*.json`

Grep `runtime[-_ ]provenance`, case-insensitive, package minus tests: glob readers are exactly three; positive control in the same
call: the writer `runtime_probe.py:1331` (critic t-800 K1, re-checked here for the three sites).

| # | reader | file:line | today | after this node, per outcome |
|---|---|---|---|---|
| 1 | `handoff_check._runtime_provenance`, wired to 3 keys | `scripts/handoff_check.py:514-518`; `DERIVERS` `:577`, `:578`, `:583` | `records[-1]` of `sorted_paths` = last BY NAME (code-point, `scripts/hooklib.py:900-915`), any profile, any window, never opened | C3: reads no file name order at all; names the record of the form's own dispatch's newest run block that carries a `runtime_provenance`, or leaves the field blank with a named reason (§2.3) |
| 2 | `Driver.walk_run_values` (S6 manual lane form) | `scripts/driver_dispatch.py:1580` (`sorted()` glob), `:1589` (`inputs_read[2].path`, `-` when none) | last by name, any profile | unchanged here; queued L-2 |
| 3 | `coverage_contract.recorded_checkout_revisions` | `scripts/coverage_contract.py:722-739` (glob `:730`); callers `validate_manual_current` `:830-833` and `manual_evidence._other_profile_errors` `scripts/manual_evidence.py:108,128-132` | every file of the profile binds its `expected_source_revision` except `unknown` (`:737`) | C2: only files whose `result` is `matched`, `mismatched` or `person_confirmed` bind. Per outcome, for BOTH callers: matched/mismatched/person_confirmed file -> binds (as today); A3 `not_applicable` file -> binds nothing; A4 file -> its revision is `unknown`, binds nothing (as today); A5 file with a 40-hex HEAD -> binds nothing; a file with no `result` -> binds nothing (only fixtures write such files: B2) |
| 4 | `null_outcomes.CONDITIONS["no_runtime_record"]` | `scripts/null_outcomes.py:164` | registry string, `reserved`; a declaration naming it is refused (`:299-300`) | unchanged; L-6 |
| 5 | measurer `s5_automator_to_critic` (outside the package) | `experiments/measurers/check_all_contracts.py:285-290` | counts files, labels them "provenance records exist (expected_source_revision + observed_runtime_identity)" | C5: counts per `result` |
| 6 | qa-collect index / delivery manifest | `references/collect-sets.json:12,39`; `scripts/delivery_manifest.py:3,104` (critic K2 rows 6-7) | index / exclude | unchanged, never interpret |
| 7 | contract texts the ROLE reads | `handoffs/s5-automator-to-critic.yaml:58-60`, `handoffs/s5-automator-to-runner.yaml:9-11,25-26,60-64`, `handoffs/s5-critic-to-automator.yaml:54-55` | say the named file is the stand's identity | C4: say the record's `result` is read first |

`handoff_init.py:272` calls only `DERIVERS["<section>[].version"]` (no provenance key): unaffected.
`test_field_producers.py:158-167` pins that the three keys share ONE deriver object: C3 keeps one deriver (F6 (i)).

### 1.4 The null-outcome registry for these fields

`references/null-outcomes.json:177,178,183`: the three carriers are `tool_field`, `node: N2`, `intent: declare`, inventory `I12`.
A declared null outcome exists only for list sections (`scripts/null_outcomes.py:281-283`); `no_run_in_dispatch` (`:165`) and
`no_runtime_record` (`:164`) are `reserved`. Unchanged by this node.

### 1.5 Keep-layer tests that read these files (who flips)

| file:line | what | after this node |
|---|---|---|
| `scripts/tests/test_runtime_probe_onboarding.py:1044-1045` (W4) | "no evidence file even without --no-evidence" for A3 | FLIPS -> replaced by C1 row; note W1 `:1021-1034` runs three A5 probes in the same task first, so the folder is not empty either |
| same file `:1469-1483` (K17), `:2015-2017` (K26), `:1520-1535` (K19) | all run `--no-evidence` | stay (r1 was wrong about K17/K26) |
| same file `:2548-2550` (H-4, A4 without `--no-evidence`) | asserts no file count | stays; now also writes a file (no assertion on it) |
| `scripts/tests/test_manual_capture.py:1351-1363` `seed_runtime_records` | seeds files with no `result` | FLIPS under C2 -> C2 owns it (B2) |
| `scripts/tests/test_manual_evidence.py:25-34` `seed_provenance` | writes `"result": "matched"` | stays |
| `scripts/tests/test_handoff.py:160-243` | `--fix` fills `artifacts.runtime_provenance` from a lone file (`:180-182`, `:230`), then "answered honestly, the form is accepted" (`:240`) | FLIPS under C3 at `:230` and `:240` (no run block of dispatch `S5-qa-automator-1`) -> C3 owns it; the fixture gets the run block |
| `scripts/tests/test_handoff.py:1391`, `test_handoff_values_main_block.py:57` | the value is typed, the deriver is not called | stay |
| `scripts/tests/fixtures/form-rounds.json:92-94` | excludes the three derives: "evidence/runtime-provenance-*.json is not in the world" | stays green; the reason text goes stale (L-10) |
| `scripts/tests/test_coverage_contract.py`, `test_profile_contract.py` | quarantined (`test-layers.json:7821`, `:9152`, under `quarantine` from `:7174`) | not run, not edited |

---

## 2. The mechanism

### 2.1 Requirement and invariants

Every answer a NON-rehearsal probe run gives is a record on disk that says what it is (`result`, `reason_code`), written by the one
writer `runtime_probe.py` through one function; the S5 forms name the record of THEIR OWN run, never a record chosen by file name.
Invariants (what must stay unreachable or still refused):
- I-1: a `not_applicable` or `unknown` record never reaches any reader as `matched`: `ACCEPTS`, `acceptable_provenance`,
  `validate_runtime_provenance` untouched; pinned on WRITTEN records (C1).
- I-2: a rehearsal (`--no-evidence`) writes nothing, for every answer (FR-45).
- I-3: a reference stand's answer (A2) is never story evidence. Owner's word W1, 11.11.2026, carrier `docs/SIBLING_MAP.md:614`:
  "a run on the reference stand is a sample, never story evidence". Not written; its blocks live in `work/reference-runs`, which the
  C3 reader never reads.
- I-4: a revision carried by a `not_applicable` / `unknown` record never binds a manual proof (C2), in both callers.
- I-5: evidence on disk is never rewritten: exclusive create; two records of one profile in one second both survive.
- I-6 (B1): the S5 deriver never names (a) a record of another dispatch, (b) a file outside the story, (c) a path that is not a file
  of the story, (d) anything when the story's run blocks cannot all be read. In every such case the field stays blank and the
  refusal names why (`unknown`, FR-59, AR-28): never a pass, never a guess.

### 2.2 Error direction of the reused functions in their new role

- `run_history.read_run_blocks` becomes the input of a form field that gates the S5 window. It may err toward REFUSING (an unreadable
  block anywhere in the story blanks the field), never toward naming another window's record. Adversarial inputs that must stay on
  the safe side: a block with no `dispatch_id`; a block of another dispatch that is newer; a reparse block of this dispatch
  (named: it carries the superseded block's record); a block whose `runtime_provenance` is `null`, `{}` or not a dict; refs `[]`,
  refs not a list, refs[0] not a string; refs[0] with `..`, a drive, an absolute path of another machine, a path of another story;
  a file named `runtime-provenance-*.json` that no block names (never named).
- `handoff_check._story_relative` (`scripts/handoff_check.py:521-534`, today a guard against a role-named path) now also guards a
  code-read path: it errs toward "" (refuse) for any absolute, drive, root or `..` path.
- `coverage_contract.recorded_checkout_revisions` (C2) errs toward refusing a manual proof (a smaller set), never toward binding one.

### 2.3 Decided forks (Lead decisions, recorded; not reopened)

- F1 = (a): the probe writes its record for every non-rehearsal answer (one writer, one kind of record). (b) declared null outcome and
  (c) a run-block read in place of a record are not built.
- F2 = (ii): A3, A4 and A5 are written; A2 never (I-3); A0/A1 are no answer. CORRECTED RATIONALE (S6): A4/A5 runs are refused at
  `run_suite.py:927-929` before any job, so no run block names their record and, with F3 (ii), no S5 form names it; that window still
  stops on `artifacts.run_witness` (required, `handoffs/s5-automator-to-critic.yaml:63`; `handoff_check._run_witness` `:139-154`
  returns None unless every test is pending) AND on the provenance field, now with a named reason. F2 (ii) is kept for one road
  (every answer leaves the same record on disk, for the conductor, the person and later readers), not because it frees a window.
  L-7 queues the window. Error direction: recording more, never a pass.
- F3 = (ii) NOW (B1). Binding: form dispatch (`Artifacts.form_dispatch`, else the form's `header.dispatch`, else `dispatch`) ==
  block `dispatch_id` (writer `run_suite.build_run_block` `:575`, from the request the controller's open dispatch named,
  `execution_request.find_active_dispatch` `:876-923`); the record = `runtime_provenance.evidence_refs[0]` of the NEWEST such block in
  `read_run_blocks` order that carries a non-empty `runtime_provenance` dict (writer of refs: `runtime_probe.write_record`; copier
  `run_suite.py:581`). Null outcome when the bound record is absent: the field stays blank and the blank refusal says
  `Code could not fill it: <why>` (one of the reasons of Card C3); never a pass, never another record. (AR-23, AR-28, FR-59.)
- F4 = (i): no new dry-1 assertion (`test_scenario_dry_1.py` does not exist on main).
- F5 = (ii): the known_red row names the TC-2 node with P1B-9 in its note; this node does not write the ledger.

Consequence of F3 (ii) the Lead should see (not a fork, the decision covers it): a window that wrote no run block of its own (an S5
dispatch whose tests are all pending, a critic window that probed no instance, a closing S5->S6 form written by a run-less dispatch,
a resumed `parent_retry` dispatch whose blocks carry the new id) now STOPS on the provenance field with a named reason where today it
was filled with whatever file sorted last. Error direction: stop. The declared road for "no run in this dispatch" is t-305 N2's
`no_run_in_dispatch` (L-6, L-7, L-9).

### 2.4 Small choices closed by the designer (no design weight)

- SC-1: one module-level `write_record` in `runtime_probe.py` replaces the body of `Reading.write_evidence`; `finish`, the A3 branch
  and the A4 branch call it: one write site (AR-14, AR-15).
- SC-2 (B1 sub-fix): exclusive create; first name `runtime-provenance-<profile>-<stamp>.json`, then `..._02.json` .. `..._99.json`.
  `_` sorts after `.`, so within one profile and second, name order = write order; the glob `runtime-provenance-*.json` still matches.
  No reader of this node depends on names (C3 binds through refs); the suffix only keeps every record.
- SC-3: a failed write of an A3/A4/A5 record (folder not creatable, read-only, bound passed) is ONE stderr line through the module's
  `warn`; the record is still printed with `evidence_refs: []`, exit 0. A6-A8: an `OSError` propagates as today; beyond `_99` a
  `FileExistsError` naming the folder is raised (S8). Never an overwrite.
- SC-4: a written record carries `evidence_refs: [<its own absolute posix path>]`, set before serialisation (as `:1332` today), so the
  file equals the printed record byte for byte in content and the run block's inline copy names it.
- SC-5: C3 resolves `evidence_refs[0]` to a story-relative path by its TAIL after the last path part equal to the story folder name
  (AR-4: a record written on another machine still resolves), else the ref itself when relative; then `_story_relative` and
  `is_file()`. A ref may name any file of the story (the real-run fixture `scripts/tests/fixtures/stories/cart-1/work/run-blocks/
  20261031T103644314576Z-c9286026d096394cd0e6.json:35-37` names a hand-written `work/evidence/s5-2-runtime.json`): it is the record
  the run carried.
- SC-6: the reason travels as an optional THIRD element of the deriver's answer, `(None, source, why)`; only `check` reads it and only
  to append to the blank refusal. No other deriver returns three elements, so no other refusal text changes.
- SC-7: C2's binding set is computed from `profile_contract.PROVENANCE_RESULTS` (no second list of result words).

### 2.5 Forks returned (new in r2; cards are buildable by the recommendation)

- **F6 — scope of `runtime.provenance` (S5->S6 form).** Its contract asks for "the runtime_provenance record" the freshness verdicts
  were taken against and "the last run_suite summary" (`handoffs/s5-automator-to-runner.yaml:60-64,82`), not "this window's run".
  (i) RECOMMENDED: the same own-dispatch rule as the two window keys, one deriver for all three (keeps `test_field_producers.py:165-167`).
  Error direction: a S5->S6 form written by a dispatch with no run of its own stops with a named reason; it never names another
  dispatch's record. (ii) the story's newest run block, any dispatch, for this key only: fills that form more often; errs toward
  naming the record of a run that is not the one the scope rows were judged against when windows ran on different stands; costs a
  second deriver and editing the pin at `test_field_producers.py:165-167` (a file outside these owns).
- **F7 — a window that ran two profiles.** The field holds ONE path. (i) RECOMMENDED: the newest own block carrying a record, whatever
  its profile or result. Error direction: may name the profile that compared nothing (A3) while the other profile's `matched` record
  goes unnamed; never another window's; the receiving role reads `profile_id` and `result`. (ii) prefer a block whose record is not
  `not_applicable`: code ranking which stand matters is a judgment (P27) and a second order beside `read_run_blocks`. Lasting answer
  (a list field) queued L-8.

---

## 3. Cards (for builders)

Given (every card): `design/factory-rules.md` whole, `plans/builder-rules.md` (p. 7, 7a, 7b), `docs/TESTING.md`, this spec,
`design/architecture.md` (the AR lines of §4). Non-goals (every card): `references/null-outcomes.json` and `scripts/null_outcomes.py`
(I12 rows stay pending); any guard change; `scripts/driver_dispatch.py` (L-2); the dry stub and `known_red.json` (F4, F5); CI, canon
and mutation runs (builder-rules 7b, PROJECT.md «Командная работа» p. 13); slow files over 60 s in `scripts/slow_tests.json`
(`test_scenario_cart_1.py` 67.4 s `:118`, `test_scenario_local_1_0108.py` 110.4 s `:119`): if `--witness-for` prints them, the report
says "judged by batch canon" and does not run them.

### Builder split

Five cards, owns pairwise disjoint, all can run in parallel (5 writers <= 6). No card imports another card's new code; C3's tests
build their own records, so C3 does not wait for C1. Merge in any order. The canon after convergence judges the cross-effects named
under each card.

| card | owns (summary) |
|---|---|
| C1 | `scripts/runtime_probe.py`, `scripts/tests/test_runtime_probe_onboarding.py`, `references/artifact-writers.json`, `changelog.d/p1b-9-runtime-provenance-record.md` |
| C2 | `scripts/coverage_contract.py`, `scripts/tests/test_manual_evidence.py`, `scripts/tests/test_manual_capture.py` |
| C3 | `scripts/handoff_check.py`, `scripts/tests/test_handoff.py` |
| C4 | `handoffs/s5-automator-to-critic.yaml`, `handoffs/s5-automator-to-runner.yaml`, `handoffs/s5-critic-to-automator.yaml` |
| C5 | `experiments/measurers/check_all_contracts.py`, `experiments/measurers/test_measurers.py` (repo-relative, outside the package) |

### Card C1 — `runtime_probe.py`: one writer for every non-rehearsal answer

given: the files above; `scripts/runtime_probe.py`, `scripts/profile_contract.py:875-921`, `scripts/tests/test_runtime_probe_onboarding.py`,
`references/artifact-writers.json:168-246`, `scripts/tests/test_artifact_writers.py:26-58`.
owns:
- scripts/runtime_probe.py
- scripts/tests/test_runtime_probe_onboarding.py
- references/artifact-writers.json
- changelog.d/p1b-9-runtime-provenance-record.md
non-goals: `write_discovered` (`:1336-...`, stays matched/mismatched only, E10); `reference_skip` behaviour; the `work/evidence/` row's
machinery list (L-4 residual); any reader.

What:
1. `write_record(task_root, profile, now, record, *, no_evidence, soft) -> None` at module level:
   - `no_evidence`: `record["evidence_refs"] = []`; when `not soft` also `record["observed_without_evidence"] = True` (today's
     A6-A8 marker, `:1326-1329`); return.
   - stamp as `:1330`; candidates `runtime-provenance-<profile>-<stamp>.json`, then `_02` .. `_99` before `.json` (SC-2). For each:
     set `record["evidence_refs"] = [path.as_posix()]`, `mkdir(parents=True, exist_ok=True)`, write `json.dumps(record, indent=2)`
     with `path.open("x", encoding="utf-8")`; `FileExistsError` -> next candidate.
   - SC-3: `soft` and (an `OSError` or all candidates taken) -> `record["evidence_refs"] = []`, one `warn(...)` line naming the
     folder and the cause, return. `not soft`: re-raise the `OSError`; all taken -> `raise FileExistsError(<folder> + " holds 99
     records of this profile in this second")`.
   `Reading.write_evidence` (`:1324-1334`) becomes a call `write_record(self.task_root, ns.profile, self.now, record,
   no_evidence=ns.no_evidence, soft=False)`.
2. A3 branch (`:1660-1669`): after the `record.update(...)` at `:1665-1667`, `write_record(task_root, ns.profile, now, record,
   no_evidence=ns.no_evidence, soft=True)`, then `print`. Rewrite the comment `:1661-1664` ("Nothing was observed, so there is no
   evidence file either") to say the answer is recorded like every other and compared nothing; docstring rung 0 `:22` and rung 9
   `:50-51` say the same (rung 9: the evidence file is written for every answer; the discovered row only for matched/mismatched).
3. A4 branch (`:1670-1675`): after `record["checkout"]` (`:1673`), the same call with `soft=True`, then `print`.
4. `Reading.finish` (`:1271-1283`): `if result == "unknown": self.finish_unknown(); write_record(..., soft=True)`.
5. A2 (`reference_skip`, `:1568-1587`): no write; one docstring sentence: a reference stand's answer is a sample, never story
   evidence (W1, `docs/SIBLING_MAP.md:614`), so it is printed and never written.
6. `references/artifact-writers.json`: one row `"evidence/runtime-provenance-*.json": {"writer": "runtime_probe.py", "why": "<one
   sentence: the probe's record of every non-rehearsal answer, one file per answer, never rewritten; no role writes it>"}` beside
   `evidence/diagnostic-*.json` (`:176`). `test_artifact_writers.every_declared_artifact_has_an_owner` (`:26-41`) finds the name in
   `scripts/*.py` (`coverage_contract.py:730`, `driver_dispatch.py:1580` keep the string after C3).
7. Changelog fragment, English, no Cyrillic: one entry ("the runtime probe records not_applicable and unknown answers too; the S5
   form names the record of its own run").

Edges:
- `--no-evidence` on any answer: no file, `evidence_refs: []`; A3/A4/A5 carry no `observed_without_evidence` (that marker is read by
  `profile_contract.rehearsal_view` `:881` for `matched` only) (I-2).
- `task_root` None: unreachable (`story` is set by `hooklib.story_cli` at `:1624` or `:1634` before `:1645`); docstring line, no branch.
- write failure / bound: SC-3 (soft for A3/A4/A5; A6-A8 raise, never overwrite) (I-5).
- conflicting pair resolved: "S2 suffix" vs "A6-A8 keep today's failed-write behaviour" -> beyond `_99` is a failed write for A6-A8
  (raise), soft for the new answers.
- TEMPORAL: stories probed before this change have no A3/A4/A5 files and their run blocks carry A3 records with `evidence_refs: []`;
  the next non-rehearsal probe (`run_suite --mine`, the post-run probe, a red probe, a manual capture) writes one. Before the change:
  no file for A3-A5; after: one per answer. The registry row exists only after this card; before it, the family had no row.
- POSITIONAL: the A3 write sits AFTER `reference_skip` (`:1635-1638`: I-3 stays unreachable) and AFTER `has_diff and not
  compared_files` (`:1660`: a story with no recorded diff never says `not_applicable`, FR-41). The A5 write sits AFTER
  `finish_unknown` (the file holds `tried`, `error`, `remedy`) and never reaches `write_discovered` (E10).

Tests (`test_runtime_probe_onboarding.py`; extend the existing table `the_probe_writes_no_evidence_when_told_not_to` `:739-778`
into one parameterised table, the row id names the answer and the mode):
- `a3-loud`, `a4-loud`, `a5-loud`: exactly one new file; its JSON equals the printed record; `evidence_refs == [that path]`;
  `result`/`reason_code` as A3 (`not_applicable`/`no_changed_file`), A4 (`unknown`/`no_expected_revision`), A5 (`unknown`, `tried` present).
- `a3-quiet`, `a4-quiet`, `a5-quiet`: no file, `evidence_refs == []`, no `observed_without_evidence` key.
- `matched-loud` / `matched-quiet`: today's rows, unchanged.
- `a2-reference-loud`: no file.
- `written-accepts` (S2, I-1): read each loud file back; `acceptable_provenance(rec, ACCEPTS)` is True for A3, False for A4, A5.
- `write-fails` (A3, `evidence` is a FILE in the task root): stdout one JSON record, `evidence_refs == []`, one stderr line, exit 0.
- `collision` (direct `write_record` twice with one `now`, `soft=True`): two files `...Z.json` and `...Z_02.json`, each with its own
  path in `evidence_refs`; `sorted_paths` order = write order.
- replace W4 `:1044-1045` by: "W4: the not_applicable record is written like every other answer" (`api["evidence_refs"]` has one
  path, the file exists, its JSON equals `api`). Do not assert an empty folder: W1 (`:1021-1034`) now leaves three A5 files.
No new test file; no slow test added (the file is 12.0 s, `scripts/slow_tests.json:104`).

DoD:
- the rows above exist under those ids and pass; `git diff` shows one write site of `runtime-provenance-` in `runtime_probe.py`
  (inside `write_record`);
- verification: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/runtime_probe.py ai-packages/qa-factory/scripts/tests/test_runtime_probe_onboarding.py ai-packages/qa-factory/references/artifact-writers.json`
  and every file it prints except the slow ones named above (expected among them: keep `test_runtime_probe_onboarding.py`,
  `test_manual_capture.py`, `test_artifact_writers.py`); plus `python -B ai-packages/qa-factory/scripts/selftest.py --lang` (the
  changelog fragment);
- the report carries the FR walk (A: FR-5; D: FR-40, FR-59; E: FR-23; F: FR-41; G: FR-45, FR-30, FR-32) and the AR lines of §4.
siblings: the four readers of §1.3 (C2, C3, C5 own three; L-2 the fourth).
Canon risk to name in the report: `test_story_run_stand_identity.py:596` counts evidence files of a rig (quarantine/slow status not
checked here: "judged by batch canon").

### Card C2 — `recorded_checkout_revisions` binds only answers that compared a build (I-4, B2)

given: the files above; `scripts/coverage_contract.py:722-840`, `scripts/manual_evidence.py:74-133`, `scripts/profile_contract.py:19`,
`scripts/tests/test_manual_evidence.py:25-34`, `scripts/tests/test_manual_capture.py:1351-1363`.
owns:
- scripts/coverage_contract.py
- scripts/tests/test_manual_evidence.py
- scripts/tests/test_manual_capture.py
non-goals: `validate_manual_current` and `_other_profile_errors` themselves (their callers' code is unchanged; only the set they read
changes); the quarantined `test_coverage_contract.py`.

What: in `recorded_checkout_revisions` (`:722-739`) count a file only when `str(data.get("result") or "")` is in
`profile_contract.PROVENANCE_RESULTS - {"unknown", "not_applicable"}` (import inside the function, as `:809` does; SC-7). Docstring:
one sentence: a `not_applicable` or `unknown` record compared no build, so the revision it carries binds nothing (P1B-9).
B2: `test_manual_capture.py:1362-1363` writes `{"profile_id": profile, "expected_source_revision": S.SOURCE, "result": "matched"}`;
its docstring `:1352-1354` says the seed is a matched run record.

Behaviour per outcome (both callers, `coverage_contract.py:830-833` and `manual_evidence.py:128-132`): see §1.3 row 3. A manual
probe whose own `result` is `not_applicable` is still skipped by both callers before the set is read (`:830`, `:129`), unchanged.

Edges: malformed JSON / not a dict: skipped (today); no `result`: not counted (error direction: refuse the manual proof); `result` not
a string (a list, a number): `str()` of it is not in the set -> not counted; other profile: skipped (today); revision empty or
`unknown`: skipped (today). Expected per B2 row: with the seed fixed, every `build` case of `test_manual_capture.py` that binds
`S.SOURCE` stays as it is today (green); without the fix they would be refused with "manual runtime proof binds a checkout revision
no run of this story recorded".
Census: `coverage_contract.py::validate_manual_current` is `xref`, owner `data` (`scripts/tests/fixtures/judgment-census.json:256`);
`manual_evidence.py::_other_profile_errors` is `shape`, owner `data` (`:675`). Neither row changes; the builder confirms.

Tests (`test_manual_evidence.py`, one table through `seed_provenance` with a `result` argument, row id = outcome): `matched`,
`mismatched`, `person_confirmed` -> revision in the set; `not_applicable` and `unknown` with a 40-hex revision -> not; no `result`
-> not; other profile -> not; one broken JSON file beside a matched one -> the matched revision kept. One row through the second
caller: an `other_profiles[]` part whose profile has only an A3 record -> `_other_profile_errors` names "binds a checkout revision no
run of this story recorded".

DoD: rows pass; `test_manual_capture.py` passes with the seed change;
verification: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/coverage_contract.py ai-packages/qa-factory/scripts/tests/test_manual_evidence.py ai-packages/qa-factory/scripts/tests/test_manual_capture.py`
and every file it prints except the slow ones (expected: keep `test_manual_evidence.py`, keep `test_manual_capture.py` 10.6 s);
report: FR walk (D: FR-58, FR-59; F: FR-41), AR lines of §4.
siblings: the second caller (`manual_evidence.py:128-132`) covered inside the function.

### Card C3 — the S5 deriver names the record of the form's own run (B1)

given: the files above; `scripts/handoff_check.py:73-106`, `:139-154`, `:514-606`, `:1462-1600`, `:2743-2755`;
`scripts/run_history.py:1-120`; `scripts/run_suite.py:572-605`, `:712-731`; `scripts/tests/test_handoff.py:160-243`.
owns:
- scripts/handoff_check.py
- scripts/tests/test_handoff.py
non-goals: `run_history.py` (read only through `read_run_blocks`); `_run_witness`; `null_outcomes`; the contracts (C4);
`driver_dispatch.py` (L-2); `test_field_producers.py` (its pin `:165-167` holds under F6 (i)).

What:
1. New module-level reader `window_runtime_record(task_root, dispatch) -> tuple` returning `(story-relative path, source)` or
   `(None, why)`; it is the ONE reader of "the record of a dispatch's run" (AR-13). In this order:
   a. `dispatch` stripped empty -> `(None, "the form names no dispatch, so its own run cannot be found")`.
   b. `blocks, bad = run_history.read_run_blocks(task_root)` inside `try`; an exception -> `(None, "the run blocks could not be read
      (<exception class>)")`.
   c. `bad` non-empty -> `(None, "<n> run block(s) under work/run-blocks/ could not be read, and one of them may be this dispatch's
      run")`.
   d. own = blocks whose `data["dispatch_id"]` (stripped str) == dispatch and whose `data["runtime_provenance"]` is a non-empty dict.
      None -> `(None, "no run block of dispatch <D> under work/run-blocks/ carries a runtime_provenance record: this dispatch ran no
      test through run_suite, or its run was refused before it started")`.
   e. newest = own[-1]. `refs = newest["data"]["runtime_provenance"].get("evidence_refs")`; not a non-empty list whose first item is
      a non-empty str -> `(None, "the newest run of dispatch <D> (work/run-blocks/<name>) carries a runtime_provenance record with no
      evidence_refs: the probe wrote no file for it (a rehearsal, a failed write, or a record from before P1B-9)")`.
   f. resolve refs[0] by SC-5 (tail after the last part equal to `Path(task_root).name`, else the ref when relative); the result
      must pass `_story_relative` and `(task_root / rel).is_file()`; else `(None, "the run block work/run-blocks/<name> names
      <ref>, which is not a file of this story")`.
   g. `(rel, "the runtime_provenance of run block work/run-blocks/<name> (dispatch <D>)")`.
   Every `why` ends with the producer: "the record is written by runtime_probe.py when run_suite runs this dispatch's tests" (FR-1,
   AR-9: what is wrong, what is expected, what produces it). Never raises.
2. `_runtime_provenance(art, doc, row=None)` (`:514-518`): dispatch = `art.form_dispatch` or `doc.get("header.dispatch")` or
   `doc.get("dispatch")`; `path, why = window_runtime_record(art.root, dispatch)`; return `(path, why)` when a path, else
   `(None, "", why)` (SC-6). The three keys keep this ONE function (`:577`, `:578`, `:583`).
3. `check` (`:1568-1593`): per field, `underived = got[2] if got and len(got) > 2 and got[0] in (None, "", []) else ""` (reset each
   iteration, before the deriver call); the blank refusal at `:1591-1592` appends `f" Code could not fill it: {underived}"` when
   set. POSITIONAL INVARIANT: the reason only extends the text of a refusal the loop raises anyway: nothing new is filled, `kind`
   stays `blank`, the `optional`/`relaxed` skip (`:1588`) and the judge step (`:1576`) are untouched, and no deriver answering two
   elements changes its output.

Edges:
- empty world (no `work/run-blocks/`): `read_run_blocks` gives `([], [])` -> reason d (blank, named).
- a reference-stand block (in `work/reference-runs/`) is never read (I-3).
- a reparse block of this dispatch is newest: its copied record is named (same record as the superseded block).
- a block whose record is a precedent copy (`execution_request.py:2807-2808`): the older record it carried is named (the record the
  run carried; error direction: an earlier record of THIS story, never another window's choice by name).
- a lone `evidence/runtime-provenance-*.json` that no block names: never named (I-6, B1).
- `parent_retry`: blocks carry the resumed id (`execution_request.py:891-910`), the form may carry the old id -> reason d; L-9.
- TEMPORAL: before the change the field was filled from any file; after it, a story whose own blocks carry A3 records written before
  C1 (refs `[]`) gets reason e until its next run; a story with `matched` records already has refs (`runtime_probe.py:1332`).
- F6/F7: by the recommendation (one rule for the three keys; the newest own block whatever its profile).

Tests (`test_handoff.py`):
- extend `a_form_is_written_and_then_repaired_by_code` (`:160-243`): add `work/run-blocks/20260101T000000000000Z-a1.json` =
  `{"attempt_id": "a1", "block_id": "a1", "dispatch_id": "S5-qa-automator-1", "attempt_started_at": "2026-01-01T00:00:00+00:00",
  "runtime_provenance": {"profile_id": "api", "result": "matched", "evidence_refs": ["<absolute posix path of the file written at
  :180>"]}, "results": []}`. Then `:230` and `:240` hold as today. (If another claim of that form reads the new block and changes,
  stop and report: no other assertion of the fixture is to be edited.)
- one new parameterised table `the_runtime_record_is_the_windows_own`, in-process calls of
  `H._runtime_provenance(H.Artifacts(task, dispatch=D), doc)` (no subprocess; S7), row id = case:
  `own-matched` -> its path; `own-not-applicable` -> its path (a field is a path, not a verdict: I-1); `other-dispatch-newer` (a newer
  block of another dispatch, plus a lone file whose name sorts last) -> None, reason names D (fails before the fix: today names the
  last file by name); `two-own-blocks` -> the newer block's path; `refs-empty` -> None, reason e; `ref-missing-file` -> None, reason f;
  `ref-escapes` (`../X/evidence/a.json`) -> None; `ref-other-machine` (`C:/elsewhere/qa-factory/artifacts/<task name>/evidence/<name>`,
  file present) -> `evidence/<name>` (AR-4); `no-dispatch` (Artifacts without dispatch, doc without `header.dispatch`) -> None,
  reason a; `unreadable-block` (`work/run-blocks/bad.json` = `{`) -> None, reason c; `no-blocks-folder` -> None, reason d;
  `reference-run-only` (the block under `work/reference-runs/`) -> None.
- one in-process `H.check(doc, "s5-automator-to-critic", H.Artifacts(task, dispatch=D), fix=True, use_judge=False)` row with no own
  block: a problem on `artifacts.runtime_provenance`, `kind == "blank"`, text contains "Code could not fill it:" and D; the field is
  still blank in the returned doc (never a pass).
The builder reports the measured wall time of `test_handoff.py` (56.8 s in `scripts/slow_tests.json:48`, `max_drift` 5 `:8`).

DoD: rows pass; `grep -n "runtime-provenance" ai-packages/qa-factory/scripts/handoff_check.py` shows no glob left;
verification: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/handoff_check.py ai-packages/qa-factory/scripts/tests/test_handoff.py`
and every file it prints except the slow ones (expected among them: keep `test_handoff.py`, `test_handoff_values_main_block.py`
10.3 s, `test_artifact_writers.py`, `test_field_producers.py`); report: FR walk (A: FR-1, FR-5; C: FR-11, FR-14; D: FR-16, FR-59;
E: FR-23, FR-37; F: FR-41), AR lines of §4.
siblings: `driver_dispatch.py:1580,1589` (L-2), `_run_witness` (L-7).
Canon risk to name in the report: story-run scenarios that `--fix` an S5 form in a world with probe files but no run block of the
form's dispatch.

### Card C4 — the contract texts say the record can say `not_applicable` or `unknown` (S1)

given: the three contracts; `scripts/contract_slices.py:71,541` (the slices are generated from placeholders, which this card leaves).
owns:
- handoffs/s5-automator-to-critic.yaml
- handoffs/s5-automator-to-runner.yaml
- handoffs/s5-critic-to-automator.yaml
non-goals: every `<...>` placeholder (a placeholder edit regenerates `references/slices/*/handoff-keys.md` and changes the refusal
hint); `handoffs/s6-runner-to-analyst.yaml:41-42` and `handoffs/s7-analyst-to-automator.yaml:74-75` (neutral placeholders:
`<the runtime_provenance record>` / the build probed: n/a); any field or key.

What (English; each a comment line or a `what:` value; the role sees comments in its form: `test_handoff.py:243`):
- `s5-automator-to-critic.yaml:58-59`: replace "The identity of the stand these instances ran against ... `runtime_probe.py`
  writes it." by: the record `runtime_probe.py` wrote for this window's run (code fills the field from the run's own block); read its
  `result` first: `matched` or `person_confirmed` identify the build, `not_applicable` (`reason_code: no_changed_file`) says the story
  changes no file of this profile's checkout so no build was compared, `unknown` identifies nothing; the critic re-probes on the same
  stand.
- `s5-automator-to-runner.yaml:9-11` (comment) and `:26` (`what:` of `inputs[2]`): the record of the run; its `result` says whether
  it identified the build (same three cases, one line). `:60-62` comment: "the identity" -> "the record (read its `result`)".
- `s5-critic-to-automator.yaml:54` comment: the record this review probed against, read by its `result`.

Edges: a size ratchet or a role-load count (`role-load.json`) that refuses the added bytes: stop and report, no raise (AR-20).
Tests: none new (text only); the witness prints what judges these files.
DoD: `git diff` shows only comment lines and the one `what:` value changed; no Cyrillic;
verification: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/handoffs/s5-automator-to-critic.yaml ai-packages/qa-factory/handoffs/s5-automator-to-runner.yaml ai-packages/qa-factory/handoffs/s5-critic-to-automator.yaml`
and the files it prints except the slow ones; plus `python -B ai-packages/qa-factory/scripts/selftest.py --lang`.
report: FR walk (B: FR-6 "text a role reads", C: FR-38; G: FR-30), AR lines of §4.
siblings: s6/s7 lines n/a (above).

### Card C5 — the measurer counts records per `result` (S9)

given: `experiments/measurers/check_all_contracts.py:275-290`, `experiments/measurers/test_measurers.py:362-410`.
owns (repo-relative):
- experiments/measurers/check_all_contracts.py
- experiments/measurers/test_measurers.py
non-goals: the other contract checks of the measurer; the package.

What: at `:285-290` read each `evidence/runtime-provenance-*.json` (`utf-8-sig`), count `result` words (`unreadable` for a file that
is not a JSON object); the line says "<n> provenance records exist (by result: matched a, not_applicable b, unknown c, ...); only
matched and person_confirmed identify a build" and keeps its second half (the manifest names the record N times; no instance names
it).
Edges: no files -> "0 provenance records exist" (no division, no traceback); an unreadable file -> counted `unreadable`.
Tests: one row in `test_measurers.py` beside the hollow-folder rows (`:380-383`): two files (`matched`, `not_applicable`) -> the
printed line contains `matched 1` and `not_applicable 1`.
DoD (an owned path outside the package: the test file that judges it, CLAUDE.md rule 4):
verification: `python -B experiments/measurers/test_measurers.py` green (duration: estimate, not verified); FR-28 line in the report.

---

## 4. AR-n, owners and census (designer rule 1)

### 4.1 AR-n touched, with the change check each demands (in the DoDs)
- AR-4 (nothing tied to one machine): C3 resolves `evidence_refs[0]` by its story tail. Check: C3 row `ref-other-machine`.
- AR-13 (one reader per fact): `window_runtime_record` is the one reader of "the record of a dispatch's run"; the S6 lane's second
  road is queued as a node (L-2). Check: C3 DoD grep (no glob left in `handoff_check.py`).
- AR-14 (one writer): one write site in `runtime_probe.py`; registry row added. Check: C1 DoD (one write site), `test_artifact_writers.py`.
- AR-22 (every field read has a producer): the three keys keep a producer for every answer that leaves a run block. Check:
  `test_field_producers.py:158-167` stays green (printed by C3's witness).
- AR-23 (empty outcome declared): the field's null outcome is the named blank refusal; the I12 rows stay `pending` (t-305 N2).
  Check: no `null-outcomes.json` change (non-goal).
- AR-25 (every recorded state has a way out): an A3 window's provenance field closes. Check: C3 row `own-not-applicable`.
- AR-28 (an unknown never becomes a pass): I-1, I-4, I-6. Check: C1 `written-accepts`, C2 table, C3 `check` row.
- AR-29 (code judges data; judgment is judged above): no check judges meaning here; the C3 reader chooses a record by data joins
  (dispatch id, refs, file presence), never by which stand "matters" (F7 (ii) rejected for that reason). Check: census rows unchanged.
- AR-9 / AR-18 (refusal shape): the reason rides in the existing blank refusal, one shape, one reader. Check: C3 `check` row.

### 4.2 Every check the spec adds or alters

| check | change | owner served | census class |
|---|---|---|---|
| `coverage_contract.py::validate_manual_current` (via `recorded_checkout_revisions`) | input set narrowed to records that compared a build (I-4) | data (code) | xref (`judgment-census.json:256`) |
| `manual_evidence.py::_other_profile_errors` (same set) | same | data (code) | shape (`:675`) |
| `handoff_check.py::check` (blank refusal of the 3 provenance keys) | the refusal text gains the deriver's reason; the producer binds to the form's own run | data (code) | shape (`:477`) |
| `runtime_probe.py` write path | not a check (a producer) | — | — |
| `window_runtime_record` / `_runtime_provenance` | not a check (a deriver; refuses nothing itself) | data (code) | no census unit (derivers are not census units: `_runtime_provenance` has no row today) |
`judgment:` line for the commits: `none` (no unit added to or moved in the census). If `test_judgment_census.py` asks for a row for
`window_runtime_record`, the builder stops and reports (no ratchet raise without the Lead, AR-20).

### 4.3 Sibling axes touched (the commit's axis block enumerates every axis, CLAUDE.md rule 10)
- axis 5 (stage twins; row on required lists and null outcomes, `docs/SIBLING_MAP.md:111-135`): pending rows unchanged (AR-23 above).
- axis 25 (freshness, `:440`): n/a — `proof_level` reads the inline record, unchanged.
- axis 32 (judgment census, `:557`): §4.2.
- axis 34 (one road, `:582`): one writer and one record for every answer; the S6 lane residual is node L-2 with owns and a test.
- axis 36 (`:606`, row "The reference run" `:614`, W1): A2 never written; `work/reference-runs` never read by C3.

---

## 5. Queue lines (each needs a home in a pile batch; owners proposed)

- L-1: `handoff_check._claim_instance_versions` gives no answer when no manifest test carries `case_version_links`, and never counts a
  test with no link (r1 §1.6). Owner: the S5 claims node; check the filler's `manifest_row` first.
- L-2 (P31 residual, a node): `Driver.walk_run_values` (`scripts/driver_dispatch.py:1580,1589`) names the last file by plain
  `sorted()` name, any profile, in the S6 manual lane form. owns: `scripts/driver_dispatch.py`; behaviour: `inputs_read[2].path` = the
  record of the lane's start probe (`probes.jsonl` row `when: start`, its `evidence_refs[0]`, resolved by the C3 tail rule, reused
  from `handoff_check`), `-` when none; test: a row in the keep file `--witness-for scripts/driver_dispatch.py` prints. Owner: the S6
  manual-lane pile.
- L-3: no guard names `evidence/runtime-provenance-*.json`; the C1 registry row does not reach the guard (`REGISTRY_ROLE_BY_SCRIPT`,
  `scripts/guard_pre_tool.py:958`). A role-written file is still possible; with C3 it is named only if a run block of the dispatch
  names it. Owner: guard pile.
- L-4 residual: the `work/evidence/` row lists `runtime_probe.py` as machinery (`references/artifact-writers.json:184-193`), a folder
  the probe never writes. Owner: whoever owns the writer registry; check which code reads `machinery` before removing it.
- L-5: `handoffs/s5-automator-to-critic.yaml:54-55` says `story_step finish` checks every artifact exists and is not empty; not
  located in `story_step.py` (not read) nor in `handoff_check.py`. Owner: S5 contracts.
- L-6 (critic S5, P31): with F3 (ii), "no record" for a window means "no run block of this dispatch carries one", i.e.
  `no_run_in_dispatch` (`scripts/null_outcomes.py:165`) or a refused run; the reserved `no_runtime_record` (`:164`) would become a
  second road. Retire it, or merge it into `no_run_in_dispatch`. Owner: t-305 N2.
- L-7 (critic S6): a run refused by `ProvenanceRefused` (A4, A5, a refused `mismatched`) leaves `artifacts.run_witness` blank
  (`handoff_check.py:139-154`, required at `s5-automator-to-critic.yaml:63`, no `required_when` in S5 contracts) and, after C3, the
  provenance field blank with reason d. Owner: t-305 N2 (the declared null outcome of the refused window).
- L-8 (F7): the provenance field is one path; a window that ran two profiles names one record. Lasting form: a list field. Owner: S5
  contracts.
- L-9: `parent_retry` — blocks carry the resumed dispatch id (`scripts/execution_request.py:891-910`) while the form may carry the
  old one; C3 then gives reason d. Reuse `retry_ancestors` in `window_runtime_record`. Owner: S5 / controller pile.
- L-10: `scripts/tests/fixtures/form-rounds.json:92-94` give the reason "evidence/runtime-provenance-*.json is not in the world" for
  excluding the three derives; after C3 the deriver reads run blocks, so the reason should say "no run block of the form's dispatch
  in the world". Owner: the form-rounds fixture's owner.

---

## Reading trail

Read (wave13 = origin/main unless noted):
- r1 spec (whole); critic verdict `docs/tasks/specs/reviews/20261114-p1b-9-plan-critic.md` (whole).
- `scripts/runtime_probe.py` 1-70, 1255-1344, 1560-1699.
- `scripts/handoff_check.py` 60-179, 300-370, 440-609, 1540-1609, 1845-1884, 2743-2763, 2935-2993.
- `scripts/run_suite.py` 540-629, 700-824, 880-939; `scripts/run_history.py` 1-115; `scripts/report_facts.py` 215-264;
  `scripts/acceptance.py` 60-189; `scripts/execution_request.py` 874-923, 2790-2879; `scripts/probe_by_code.py` 2865-2944.
- `scripts/coverage_contract.py` 715-844; `scripts/manual_evidence.py` 70-139; `scripts/hooklib.py` 895-919;
  `scripts/null_outcomes.py` 150-169, 276-303; `scripts/driver_dispatch.py` 1545-1599; `scripts/guard_pre_tool.py` 770-794, 958-1028;
  `scripts/handoff_init.py` 255-284.
- `handoffs/s5-automator-to-critic.yaml` (whole), `handoffs/s5-automator-to-runner.yaml` (whole), `handoffs/s5-critic-to-automator.yaml`
  48-59, `handoffs/s6-runner-to-analyst.yaml` 36-45, `handoffs/s7-analyst-to-automator.yaml` 68-77.
- `references/artifact-writers.json` 168-252; `references/null-outcomes.json` (Grep rows 177, 178, 183).
- tests: `test_runtime_probe_onboarding.py` 180-219, 739-778, 1020-1059, 1455-1544, 1596-1625, 2150-2179, 2525-2553;
  `test_handoff.py` 150-244; `test_manual_capture.py` 1335-1374; `test_manual_evidence.py` 22-35; `test_field_producers.py` 155-172;
  `test_artifact_writers.py` 26-58; `scenario_walk.py` 833-932; `test-layers.json` rows 131-145, 2295-2314, 2410-2424, 3005-3049,
  4721-4735; `slow_tests.json` (Grep rows 8, 48, 51, 65, 104, 118-120); `fixtures/judgment-census.json` 256, 472-482, 675, 832.
- `experiments/measurers/check_all_contracts.py` 270-304; `docs/TESTING.md` 43-60; `plans/builder-rules.md` 10-39;
  `docs/SIBLING_MAP.md` (Grep headings 111, 440, 557, 582, 606, 614).

Searched (Grep/Glob, content), each negative with its positive control:
- `runtime-provenance` in `scripts/tests/*.py` (count, 12 files) and with content in ten named files; `runtime_provenance:|provenance:`
  in `fixtures/stories` (forms carry typed values, deriver not called).
- `run-blocks|run_blocks` in scripts (found `run_history.read_run_blocks`, the one order); `block_id|...` in `run_suite.py`.
- `dispatch_id.*(required|must|missing)` in `execution_request.py`: empty; positive control: `dispatch_id` in the same file found
  `:116` (required string) and `find_active_dispatch` `:876-923`.
- `def \w+...|run-blocks` in `window_record.py`: empty (malformed alternation, a miscall); the follow-up `run-blocks|run_blocks` over
  `scripts/*.py` is the reading used, it found `acceptance.py:67`, `run_history.py:59`.
- Glob `ai-packages/qa-factory/...` with the worktree as `path`: empty twice (a miscall: positive control `test_handoff*.py` in the
  same form also empty); re-run as `**/test_scenario_*.py` and `**/runtime-provenance-*` under `scripts/`: found 5 scenario files,
  25 fixture records, 15 cart-1 run blocks.
- `REGISTRY_ROLE_BY_SCRIPT\s*=` (found `:958`); `_code_fills`; `no_verdict`; `Artifacts\(` (all callers); `"handoff_check\.py"|...`
  in `test-layers.json` (keep rows); `"run_history\.py"|"profile_contract\.py"` in `test-layers.json`; census rows by function.
- `identity of the stand|stand these instances ran against|probed against` (package): three contract lines, one slice (generated),
  six cart-1 fixture forms (copies, not edited).
- `check_all_contracts` (repo): `experiments/measurers/test_measurers.py` is its test.
Not run: any test or script (the designer runs nothing); the `--witness-for` outputs are EXPECTED from the keep rows read, not printed.
Needed beyond the manifest: the files listed above outside the dispatch's `given` (read-only).
