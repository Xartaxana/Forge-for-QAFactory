# P1B-9 — every answer of the runtime probe has a record (draft spec, t-790)

Status: DRAFT by designer for Lead acceptance. Forks are in §2.4; nothing in §2.4 is decided here.
Source of the gap: `docs/tasks/specs/reports/20261114-p1b-n2f-report.md` (worktree p1b-n3) STOP TABLE row 3, gap candidate 9.
Product files read on `wip/p1b-n3`; the four load-bearing sites were re-checked on origin/main (worktree `wave13`):
`runtime_probe.py:22` and `:1668/:1674`, `handoff_check.py:514`, `null_outcomes.py:164` are byte-identical in line and text.

---

## 1. Inventory (measured, file:line)

Paths are relative to `ai-packages/qa-factory/`.

### 1.1 Every answer of `runtime_probe.py` (no `--suggest`)

| # | answer (`result`, `reason_code`) | where decided | record written today? | where the write is decided |
|---|---|---|---|---|
| A0 | exit 2, no JSON: `--task` absent and no running story | `scripts/runtime_probe.py:1627-1633` | no (a call refusal, FR-46: not an answer) | — |
| A1 | exit 2, no JSON: `--checkout` absent | `:1639-1643` | no (call refusal) | — |
| A2 | `not_applicable`, `no_changed_file`, reason REFERENCE_REASON — `--environment` names a REFERENCE stand of the story | `reference_skip` `:1568-1587`, printed `:1635-1638` | **no** | early return, before `Reading` |
| A3 | `not_applicable`, `no_changed_file` — a diff is recorded and none of its production files is in the checkout ("rung 0") | `:1660-1669` | **no** ("No rung, no write", docstring `:22`, comment `:1663-1664`) | early return |
| A4 | `unknown`, `no_expected_revision` — the checkout names no commit | `:1670-1675` | **no** | early return |
| A5 | `unknown` (any rung-8 end: docker down, nothing answered, a device, a voided word, `asks_person: how/confirm`) | `Reading.finish` `:1276-1278` -> `finish_unknown` `:1285-1322` | **no** (`finish` writes only for the three words below) | `:1279-1280` |
| A6 | `matched` | ladder, `Reading.finish` | yes, `evidence/runtime-provenance-<profile>-<stamp>.json` | `write_evidence` `:1324-1334` |
| A7 | `mismatched` | ladder | yes | same |
| A8 | `person_confirmed` | ladder rung 7 (`:1221`) | yes | same |
| A9 | any of A3..A8 under `--no-evidence` (the rehearsal: gate A, `build_check`, S6 freshness) | `write_evidence` `:1326-1329` | no, by design (FR-45) — `evidence_refs: []`, `observed_without_evidence: true` (A6..A8 only) | `:1326` |

Measured consequence: of the answers a NON-rehearsal run can give, only A6/A7/A8 leave a file. A2, A3, A4, A5 leave none.
The dry story's answer was A3 (report row 2: "the real `runtime_probe.py` answers `not_applicable` / `no_changed_file`").

### 1.2 Who takes the printed answer (the run path)

| reader | file:line | A3 (not_applicable) | A5 (unknown) |
|---|---|---|---|
| `run_suite.probe_runtime` (the one strict reader of the run path, `--mine`, red probe, post-run probe) | `scripts/run_suite.py:915-929` via `profile_contract.acceptable_provenance` `scripts/profile_contract.py:893-921`, `ACCEPTS` `:875` | TAKEN (`not_applicable:no_changed_file`) — the run goes on | refused (`ProvenanceRefused`) — no run |
| the run block | `scripts/run_suite.py:581` (`"runtime_provenance": request.get("runtime_provenance")`) | the printed record is copied INLINE; with no file, its `evidence_refs` is `[]` | no block (refused) |
| `driver_stage_build.build_outcome` (rehearsal, `--no-evidence`) | `scripts/driver_stage_build.py:297-302` | line `not_applicable`, no question | `:319-336` question or line |

### 1.3 Every reader of `evidence/runtime-provenance-*.json`

Grep `runtime-provenance` over `scripts/*.py` (positive control: the same Grep found the writer `runtime_probe.py:1331` and
the registry row `null_outcomes.py:164`). Non-test readers: four.

| reader | file:line | what it does with the files | file exists (A6-A8) | no file (A2-A5 today) |
|---|---|---|---|---|
| `handoff_check._runtime_provenance` (deriver of 3 keys) | `scripts/handoff_check.py:514-518` | newest file by `sorted_paths`, any profile, any window | fills the field with `evidence/<name>` | `None` -> field stays blank -> `Problem(path, "not filled. <hint>", kind="blank")` `:1587-1593` — **the S5 stop** |
| the deriver table, key `artifacts.runtime_provenance` (s5-automator-to-critic) | `:577`; contract `handoffs/s5-automator-to-critic.yaml:60`, required (`references/slices/qa-automator/handoff-keys.md:30`) | same | filled | blank -> refused |
| key `probes.runtime_provenance` (s5-critic-to-automator) | `:578`; `handoffs/s5-critic-to-automator.yaml:55` | same | filled | blank -> refused |
| key `runtime.provenance` (s5-automator-to-runner) | `:583`; `handoffs/s5-automator-to-runner.yaml:64` (and `inputs[2]` `:25-27`, `required: true`) | same | filled | blank -> refused |
| `coverage_contract.recorded_checkout_revisions` | `scripts/coverage_contract.py:722-739`, read by `validate_manual_current` `:830-833` | the `expected_source_revision` of every file of the profile (any `result`), minus `unknown` | binds a manual proof to a revision a run recorded | empty set -> a manual proof whose probe is not `not_applicable` is refused ("binds a checkout revision no run of this story recorded") |
| `Driver.walk_run_values` (S6 manual lane form) | `scripts/driver_dispatch.py:1559`, `:1568` | `inputs_read[2].path` = newest file, else `-` | names the path | writes `-` (a declared empty, no refusal) |
| `null_outcomes.CONDITIONS["no_runtime_record"]` | `scripts/null_outcomes.py:164` | registry only, `status: reserved`, `impl: None`; any declaration naming it is refused (`entry_problems` `:299-300`) | — | — |

Readers of the INLINE record (run block / request `runtime_provenance`), not of the file — listed so the walk is closed:
`report_facts._person_build` `scripts/report_facts.py:222-258`, `proof_level.py:1791`, `window_record.py:504-512`,
`baseline_contract.py:21/83/141`, `execution_request.py:171`, `execution_fingerprint.py:121`, `manual_evidence.py:79/681`.
None of them globs `evidence/`; none changes with this node (their input — the printed record — is unchanged).

### 1.4 The null-outcome registry for these fields

`references/null-outcomes.json:185,186,191`: the three carriers (`s5-automator-to-critic:artifacts.runtime_provenance`,
`s5-critic-to-automator:probes.runtime_provenance`, `s5-automator-to-runner:runtime.provenance`) are `pending`, kind
`tool_field`, node `N2` (of t-305), `intent: declare`, inventory `I12`. A declared null outcome exists today ONLY for list
sections: `null_outcomes.entry_problems` refuses any section outside `handoff.REQUIRED_LISTS` (`scripts/null_outcomes.py:281-283`).
Only one condition of the registry is `live` (`triage_has_no_repair`, `:154-156`); no condition has ever moved from `reserved` to
`live` for a scalar tool field. So "how other conditions moved to declared" has no precedent to copy: the road does not exist yet.

The road the factory DOES use for a tool field whose producer had no output in a legitimate null case:
`handoff_check._run_witness` `scripts/handoff_check.py:139-154` — when every test is pending its absent side
(`acceptance.run_witness_excused == "pending"`, t-2181 PC-4 B3), the DERIVER names a code-written artifact that exists for the null
case (the collect row's label). The field is filled by code with a record that says what it is; nothing is declared empty.

### 1.5 Downstream of S5 (S6/S7/delivery), both worlds

| place | reads | file exists | no file | changes with this node? |
|---|---|---|---|---|
| `Driver.stand_check` | pipeline `environment`, the person's word `stand not confirmed` (`scripts/driver_stage_build.py:72-124`) | — | — | no: reads no provenance |
| `Driver.build_check` / `build_outcome` | the rehearsal's printed record (`--no-evidence`) `:209-339` | — | — | no: a rehearsal never writes (A9 stays) |
| `first_look._stand_build` (`stand_build: not_established`) | the person's `deployed` word (`scripts/first_look.py:440-452`) | — | — | no: reads no provenance file |
| S6 runner / S7 analyst forms | `runtime.provenance` / `inputs[].path` as a PATH the role reads (`handoffs/s6-runner-to-analyst.yaml:41`, `s7-analyst-to-automator.yaml:68`) | role reads the record and its `result` | today: blank | yes: the path now exists for A3 (and A4/A5 per F2) — the ROLE reads `result` |
| delivery (`check_delivery`, `report_facts`) | run blocks' inline record, the stand word | — | — | no: no reader of the file (§1.3) |

Conclusion of §1.5: no reader after S5 turns a missing or `not_applicable` FILE into a pass or a block; the only blocking reader of
the file is the S5 form check (§1.3 row 1). The delivery verdict never reads the file.

### 1.6 The second S5 finding (brief item 5): its own gap, not this one

`claims.every_instance_names_its_current_case_version` is verified by `handoff_check._claim_instance_versions`
(`scripts/handoff_check.py:629-644`). It reads `automation-manifest.json` `tests[].case_version_links` and the story's case links —
NOT the provenance record. It returns `None` when no test of the manifest carries `case_version_links` (`:641-642`), and
`_fill_claims` turns `None` into "not filled. code could not measure it: the verifier gave no answer" (`:1832-1844`).
So the finding follows from the dry window's manifest rows carrying no `case_version_links` (the filler's `manifest_row` shape, or
the TC-2 row of Q1), never from the missing record. A second observation on the same verifier: a test row with NO links is not
counted at all (`:634-635`), so "0 of 0" hides a row that names no version. Both go to a separate queue line (§5 L-1); no card here.

---

## 2. The mechanism

### 2.1 Requirement, as an invariant

Every answer a NON-rehearsal probe run gives is a record on disk that says what it is (`result`, `reason_code`), written by the one
writer `runtime_probe.py`; every reader of the files reads `result` and none of them reads "a file exists" as "the build was
established". INVARIANTS that must stay unreachable:
- I-1: a `not_applicable` or `unknown` record never reaches any reader as `matched` (no reader of the run path changes: `ACCEPTS`,
  `acceptable_provenance`, `validate_runtime_provenance` untouched).
- I-2: a rehearsal (`--no-evidence`) still writes nothing (FR-45).
- I-3: a reference stand's answer (A2) is never story evidence (owner's word W1, 11.11.2026; carrier SIBLING_MAP axis 36 row "The
  reference run": "a run on the reference stand is a sample, never story evidence").
- I-4: `coverage_contract.recorded_checkout_revisions` returns exactly the set it returned before the change for the same probe history
  (a revision a `not_applicable`/`unknown` record carries never binds a manual proof).
- I-5: evidence on disk is never rewritten (artifact-writers `why` lines): two records of one profile in one second never overwrite.

### 2.2 Options and their error direction

| option | what | error direction | cost |
|---|---|---|---|
| (a) RECOMMENDED | the probe writes its record for A3 (and, by F2, A4/A5) exactly as for A6-A8; the deriver is unchanged and finds the file | may err toward NAMING a record that says `not_applicable`/`unknown` in the form field — never toward a fabricated path and never toward `matched`; the form field is a path the next ROLE reads, no code reads it as a verdict (§1.3, §1.5) | one writer change, one reader filter (I-4), test rows |
| (b) declared null outcome `no_runtime_record` | implement the reserved condition for a scalar tool field; the role leaves the field empty under it | the condition "no file" cannot tell `not_applicable` from "never probed" or "run refused on `unknown`" -> errs toward a PASS on an unknown (FR-59, AR-28) unless it also reads the run block's inline record; the receiving roles get no path; the scalar-field declaration road does not exist (§1.4) and belongs to t-305 N2 | new machinery in `null_outcomes.py` + `handoff_check` + contract `null_outcome` blocks on 3 contracts, a new reader of run blocks |
| (c) deriver reads the run block's inline record | `_runtime_provenance` falls back to the newest run block's `runtime_provenance` when no file exists | errs toward filling a PATH field with a run-block path whose record has `evidence_refs: []`; the record is the printed answer (code-written by `run_suite`), so no pass; but a second carrier of "the window's provenance" (AR-13: two reads of one fact) and a value of another shape in a field typed "path of the record" | deriver change + a reader of run blocks in handoff_check |

One road (P31): (a) keeps ONE writer and ONE kind of record for every answer; (b) and (c) give the null answers another road than
the established ones. The precedent of §1.4 (`_run_witness`: a code-written artifact for the null case, found by the deriver) is (a)'s
shape.

### 2.3 Who establishes that the probe said `not_applicable` (brief item 3)

Code: `runtime_probe.py` decides A3 from the recorded diff and the checkout (`:1658-1660`) and is the writer of the file; the role
neither types the field (the deriver fills it, `handoff_check.py:1568-1575`) nor the record. A role that hand-writes a file into
`evidence/` is the SAME hole that exists today for `matched` (this draft found no guard rule naming `runtime-provenance`: Grep over
`guard_*.py`, `stage_guard.py`, `hooklib.py`, case-insensitive, empty; positive control `def deny` found in `stage_guard.py`). Not
widened here: queue line §5 L-3. The written record keeps `reason_code: no_changed_file` as a FIELD (FR-12); no reader reads the
`reason` sentence.

### 2.4 Forks (returned, not decided)

- **F1 — mechanism.** (a) / (b) / (c) of §2.2. Recommendation: (a). Cost of (b): implementing a part of t-305 N2 here.
- **F2 — which answers are written.** (i) A3 only (the dry story's case); (ii) every non-rehearsal answer: A3, A4, A5 — not A2 (I-3),
  not A0/A1 (no answer). Recommendation: (ii): with (i), an S5 window whose run was refused on `unknown` and handed over
  `blocked_by_env` still has a required field nothing can fill — the same FR-5/FR-23 defect for another answer, i.e. two roads for one
  action (P31). Cost of (ii): four pinned "no evidence file" rows of `test_runtime_probe_onboarding.py` flip (`:1044` W4, `:1483` K17,
  `:2017` K26, and the A4 row if pinned), and the evidence folder now holds records of unverified answers (I-1/I-4 keep every reader
  safe; §1.3 lists all four readers). Error direction of (ii): toward recording more, never toward a pass.
- **F3 — which record the deriver names.** Today: the newest file of ANY profile and ANY window (`handoff_check.py:515-518`). With (a)
  more files exist, so a mixed window (api + e2e) may name the other profile's record. (i) keep "newest" in this node and queue the
  binding to the window's own run block (`evidence_refs[0]` of the block's inline record); (ii) bind now. Recommendation: (i) — the
  ambiguity exists today between two `matched` records; it is an analog, not created by this node; queue line §5 L-2. Error direction
  of (i): names a real record of this story, possibly of another profile/window; the receiving role reads its `profile_id`.
- **F4 — the dry-1 scenario.** (i) no new assertion: the builder's report quotes the dry-1 stop NOTE line verbatim, without
  `artifacts.runtime_provenance`; (ii) a new check in `test_scenario_dry_1.py`. Recommendation: (i) (TESTING.md: a scenario judges
  the stop by its known_red row; S5 still stops for Q1/TC-2, finding 8 and §1.6, so the scenario stays red at `main/S5` either way).
- **F5 — the known_red row `main/S5` (report Q2).** Today the ledger is empty (`scripts/tests/fixtures/driver-exits/known_red.json:3-4`)
  and the run FAILs "new red: main/S5". Options: (i) add `"main/S5": {"node": "P1B-9", ...}` now and re-point it to the node of the
  NEXT S5 finding when P1B-9 lands; (ii) add it naming the TC-2 node (Q1/N2g) at once, with `note` listing P1B-9. Recommendation: (ii):
  after P1B-9 lands S5 still stops (Q1), so a row naming P1B-9 would be stale and is refused by the loader's stale rule only once S5
  passes; naming the last blocker keeps the row true across both landings. Lead's call; this node does not write the ledger.

### 2.5 Small choices closed by the designer (no design weight)

- S1: one module-level writer function in `runtime_probe.py` (`write_record`) replaces the body of `Reading.write_evidence` and is
  called by `finish` and by the A3/A4 branches — one write site (AR-15).
- S2: a name collision (same profile, same second) takes the next free `-<n>` suffix before `.json`; the glob
  `runtime-provenance-*.json` still matches (I-5).
- S3: a failed write of a NEW record (A3/A4/A5) is one stderr line; the record is still printed, with `evidence_refs: []`, exit 0 —
  the answer stands and the reader sees today's world (no file). A6-A8 keep today's behaviour on a failed write (not widened).
- S4: the written A3/A4/A5 record gets `evidence_refs: [<its own path>]` (as A6-A8 do, `:1332`), so the run block's inline copy names it.
- S5: no new `stages.json` output: the artifact family already has its writer row (`references/artifact-writers.json:184-193`,
  `runtime_probe.py` as machinery of `work/evidence/`). Noticed, not widened: that row says `work/evidence/` while the probe writes
  `<task>/evidence/` (`runtime_probe.py:1331`) — §5 L-4.

---

## 3. Cards (for a builder)

One builder node, three cards, owns disjoint by file. Paths below are written against the main checkout; the Lead rewrites the prefix
to the builder's worktree in the dispatch. Given (all cards): `design/factory-rules.md` whole, `plans/builder-rules.md`, this spec,
`docs/TESTING.md`. Non-goals (all cards): the dry stub; FV1-28 (A2 changes `walk_session.survey_opens_on` — NO overlap: no card here
touches `walk_session.py`); the kit/`plan_rows` question of N2g; `null-outcomes.json` (the I12 pending rows STAY: they still cover the
window with no probe at all — `no_run_in_dispatch`, t-305 N2); the deriver binding of F3; any guard change.

### Card C1 — `runtime_probe.py`: one writer for every non-rehearsal answer

owns:
- C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\runtime_probe.py
- C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_runtime_probe_onboarding.py
- C:\QAFactory\forge-repo\ai-packages\qa-factory\changelog.d\p1b-9-runtime-provenance-record.md

What:
1. `write_record(task_root, profile, now, record, no_evidence) -> None` at module level: the body of `Reading.write_evidence`
   (`:1324-1334`) plus S2 (collision suffix) and S3 (for the new answers only — a flag `soft=True`). `Reading.write_evidence` calls it.
2. A3 branch (`:1660-1669`): after `record.update(...)`, call `write_record(..., soft=True)` before `print`. Comment `:1663-1664` and the
   docstring rung 0 (`:22`) and rung 9 (`:50-51`) say: "the answer is recorded like every other; it compared nothing".
3. By F2 (ii) only: A4 branch (`:1670-1675`) and `Reading.finish` for `unknown` (`:1277-1278`) call it too. `write_discovered` stays
   matched/mismatched only (E10 unchanged).
4. A2 (`reference_skip`, `:1635-1638`): NO write (I-3). Add one sentence to its docstring saying why.

Edges:
- `--no-evidence` on any answer: no file, `evidence_refs: []` (I-2). A3 under `--no-evidence` keeps today's printed shape (no
  `observed_without_evidence` key: that marker belongs to `matched`, `profile_contract.rehearsal_view` `:881-890`).
- `task_root` absent/None: unreachable here (`hooklib.story_cli` resolved it, `:1623-1634`); state it in the docstring, no branch.
- write fails (evidence path is a file, read-only folder): S3.
- collision: S2. Limit: the suffix search stops at `-99`; beyond it S3 applies (one stderr line, no file).
- TEMPORAL: stories recorded before the change have no A3 file; their next non-rehearsal probe run writes one (the move that creates
  it is the next `run_suite --mine` / post-run probe). A story with no further run keeps today's refusal (§3 C3 row 1) — no regression.
- POSITIONAL: the A3 write sits AFTER `reference_skip` (I-3 stays unreachable) and AFTER the `has_diff and not compared_files` test
  (a story with no recorded diff never says `not_applicable`, `:1676-1677`, FR-41).

Test rows (`test_runtime_probe_onboarding.py`, one parameterised table, id names the answer):
`a3-writes` (one file; its JSON equals the printed record; `evidence_refs == [path]`; `result: not_applicable`,
`reason_code: no_changed_file`) — this REPLACES the W4 row `:1044`; `a3-rehearsal` (no file); `a2-reference` (no file);
`a4-writes` / `a5-writes` (F2 (ii): one file each, registry still absent — K17 `:1483` and K26 `:2017` flip their evidence half only);
`a6..a8` (unchanged: one file); `write-fails` (stderr one line, stdout still one JSON record, exit 0, `evidence_refs: []`);
`collision` (two runs, same profile, frozen clock: two files).

Witness: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/runtime_probe.py`
and the files it prints (expected among them: keep `test_runtime_probe_onboarding.py`, ~12 s per `scripts/slow_tests.json:104`).

### Card C2 — `coverage_contract.recorded_checkout_revisions`: the reader keeps its set (I-4)

owns:
- C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\coverage_contract.py
- C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_manual_evidence.py

What: in `recorded_checkout_revisions` (`:722-739`) count a file only when its `result` is one of `matched`, `mismatched`,
`person_confirmed` — the three answers that were written before this change (a constant beside the function, named for that reason).
Docstring: one sentence on why a `not_applicable`/`unknown` record binds nothing.

Edges: malformed JSON / not a dict: skipped (today); a record with no `result`: not counted (error direction: toward refusing the manual
proof, never binding it); other profile: skipped (today); revision `unknown`/empty: skipped (today).
Owner/class of the altered check: the check `validate_manual_current` (`:830-833`) is a DATA check (owner: code), census class `xref`;
the builder confirms the class in `scripts/tests/fixtures/judgment-census.json` for `coverage_contract.py::validate_manual_current` and
does not change it (if the unit has no row, the report says so — C1 of the census would already refuse that).
Note: `test_coverage_contract.py` is QUARANTINED (`scripts/tests/test-layers.json:7828`, under `quarantine` from `:7181`): not run, not
edited. The table row goes to the keep file `test_manual_evidence.py`, which already writes these files (`:26-29`).

Test rows (one table): `matched`/`mismatched`/`person_confirmed` -> revision in the set; `not_applicable`/`unknown` with a 40-hex
revision -> not in the set; no `result` -> not; other profile -> not; broken JSON -> skipped, others kept.

Witness: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/coverage_contract.py`
and the files it prints (keep `test_manual_evidence.py` expected).

### Card C3 — the S5 form gets the record (test rows only)

owns:
- C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_handoff.py

What: no code change in `handoff_check.py` (the deriver already names the newest file, §1.3). Rows prove the joint: an S5
`s5-automator-to-critic` form checked with `--fix` (the pattern of `test_handoff.py:180`):
`no-file` -> `artifacts.runtime_provenance` stays blank and the problem is "not filled" (today's behaviour, the empty world);
`not-applicable-file` -> filled with `evidence/<name>`, no problem on that path; `unknown-file` (F2 (ii)) -> filled with its path and no
`claims.*` value changes because of it (I-1: the field is a path, never a verdict).
Edges: a non-JSON file named `runtime-provenance-x.json` is still named (the deriver reads names only, today) — one row pinning that
the deriver never opens it; this is the existing behaviour, recorded, not changed.

Witness: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/tests/test_handoff.py`
(`test_handoff.py` ~57 s, `scripts/slow_tests.json:48`, under the one-minute line of PROJECT.md acceptance p.2).

### Scenario row (dry-1) and what the batch canon judges

- After C1 lands, the dry-1 S5 stop loses the finding `artifacts.runtime_provenance: not filled`; S5 still stops on Q1 (TC-2 bindings,
  obligations, digest), on §1.6 and possibly gap 8. The builder runs `test_scenario_dry_1.py --part main` ONLY if `--witness-for`
  prints it for its owns (51 s, `slow_tests.json:119`) and quotes the `NOTE dry-1/main/stop` line verbatim. The known_red row: F5.
- The canon judges: every `test_story_run_*.py`, `test_run_suite_mine.py` and `test_profile_contract.py` (both quarantined — not run by
  the canon either; `quarantine-watch` runs them), and any file `--witness-for` prints beyond the narrow ones.

DoD (inline, for the dispatch): (1) the three cards' test rows exist as named and are green in the files `--witness-for` prints;
(2) a grep `runtime-provenance` over `scripts/*.py` shows the same four readers of §1.3 and one write site in `runtime_probe.py`;
(3) the report carries the FR walk (A: FR-5; D: FR-40, FR-59; E: FR-23; F: FR-41; G: FR-45, FR-32), the AR lines of §4 and the axis
lines of §4.3; (4) `changelog.d` fragment present, English, no Cyrillic (`selftest.py --limits --lang`).

---

## 4. AR-n / FR-n / census

### 4.1 AR-n touched (with the change check written into the DoD)
- AR-14 (one writer): `runtime_probe.py` stays the one writer of the files; S1 makes one write site. Check: grep, DoD (2).
- AR-22 (every field read has a producer): the three keys of §1.3 get a producer for A3 (and A4/A5). Check: `test_field_producers.py`
  is NOT owed (no contract field changes); C3 rows pin the joint.
- AR-23 (empty outcome): the I12 pending rows stay pending for the no-probe window; nothing new is required. Check: no
  `null-outcomes.json` change, `test_null_outcomes.py` not owed (builder-rules 7b: owed only when the registry changes).
- AR-25 (every recorded state has a way out): `not_applicable` at S5 now has its move (the form closes). Check: C3 row 2.
- AR-28 (an unknown never becomes a pass): I-1, I-4; the deriver fills a PATH, never a verdict. Check: C2 table, C3 row 3.
- AR-13 (one reader per fact): three glob readers of the same files, no survivor — named, queued §5 L-2 (not widened).
- AR-29: no check is added; the only altered check (C2) is a data check, class `xref`, owner data (code).

### 4.2 Census line (designer rule 1)
| check | change | owner | class |
|---|---|---|---|
| `coverage_contract.validate_manual_current` via `recorded_checkout_revisions` | input set narrowed to the three answers written before (I-4) | data (code) | xref |
| `handoff_check` form check of the 3 provenance keys | unchanged code; new producer output reaches it | data (code) | shape |
`judgment:` line for the commit: `none` (no unit added or moved).

### 4.3 Sibling axes (SIBLING_MAP)
- axis 5, row "Required lists <-> null outcomes": walked — pending rows unchanged, reason §4.1 AR-23.
- axis 36, row "The reference run" (W1): kept — A2 writes nothing (I-3).
- axis 25 (freshness): n/a — `proof_level` reads the inline record (`:1791`), unchanged.
- axis 34 (one road): the recommendation of F1/F2 is the one-road option; the residual left by F2 (i), if chosen, is named there.
- axis 32 (judgment census): §4.2.

---

## 5. Open questions

### For the Lead
- Q-L1: F1, F2, F3, F4, F5 (§2.4).
- Q-L2: the branch this node lands on: the dry-1 proof needs `wip/p1b-n3`'s stub (N2f); C1-C3 themselves are main-identical.
- Q-L3: the S5/S6 role texts (automator, code critic, runner) do not say that a provenance record may say `not_applicable` or
  `unknown`; should a line be added (the record's `result` is read before a re-probe)? Not in this node's owns.
- Queue lines proposed (each needs a home in a pile batch):
  - L-1: `_claim_instance_versions` gives no answer for a window whose manifest tests carry no `case_version_links`, and never
    counts a test with no link (§1.6) — check the filler's `manifest_row` first (stub gap or product gap).
  - L-2: `_runtime_provenance` names the newest record of any profile/window; three glob readers with no reader function (F3, AR-13).
  - L-3: no guard rule names `evidence/runtime-provenance-*.json`; a role-written file would be named by the deriver (§2.3).
  - L-4: `artifact-writers.json:184` registers `work/evidence/` while the probe writes `<task>/evidence/` (S5).
  - L-5: `handoffs/s5-automator-to-critic.yaml:54-55` says "`story_step finish` checks that each [artifact] exists and is not empty";
    this draft did not locate that check in `story_step.py` or `handoff_check.py` (Grep `is_file()` / `.exists()` in `handoff_check.py`
    found only other sites) — the comment may be stale.

### For the owner
- None. F2 changes what the evidence folder holds (records of unverified answers) but no reader's meaning changes (I-1..I-4); if the
  Lead reads F2 (ii) as a change of meaning of "evidence", PROJECT.md acceptance p.6 (critic on plan) applies before the builder.

---

## Reading trail

Read (worktree p1b-n3 unless noted): `docs/tasks/specs/reports/20261114-p1b-n2f-report.md` (whole);
`scripts/runtime_probe.py` 1-110, 400-439, 1240-1699; `scripts/handoff_check.py` 139-179, 440-645, 1540-1850;
`scripts/null_outcomes.py` 1-340; `references/null-outcomes.json` 1-40 and Grep rows 155-197;
`scripts/coverage_contract.py` 715-849; `scripts/driver_dispatch.py` 1530-1579; `scripts/profile_contract.py` 700-929;
`scripts/run_suite.py` 570-629, 880-959, 2025-2074; `scripts/report_facts.py` 215-274; `scripts/driver_stage_build.py` 60-339;
`scripts/handoff.py` 535-560; `handoffs/s5-automator-to-critic.yaml` 40-79; `handoffs/s5-automator-to-runner.yaml` whole;
`references/slices/qa-automator/handoff-keys.md` whole; `references/artifact-writers.json` 1-30, 174-193;
`scripts/tests/scenario_walk.py` 834-933; `scripts/tests/fixtures/driver-exits/known_red.json` whole;
`design/architecture.md` 140-296; `C:\QAFactory\forge-repo\docs\SIBLING_MAP.md` 1-40, 120-179, 436-463, 557-616;
`C:\QAFactory\forge-repo\plans\builder-rules.md` 7/7a/7b.
Searched (Grep, content): `runtime[-_]provenance|no_runtime_record` (package, case-insensitive); `runtime-provenance` in `*.py`
(positive control: writer `runtime_probe.py:1331`); `not_applicable|No rung|...` in runtime_probe; `acceptable_provenance|...` in
scripts; `verifier gave no answer|not filled` in scripts; `not_established`; `"taken"|def stand_check`; `relaxed`;
`required_when|null_outcome` in handoffs; `provenance|runtime` in handoffs; `runtime_provenance` in eight readers;
`runtime-provenance|code_owned|...` in guards (empty; positive control `def deny` -> `stage_guard.py`); test-layers keep/quarantine
rows; `slow_tests.json` entries; `SLOW_TESTS\s*=` (empty; then `SLOW_TESTS` in `selftest.py` found the data file).
Main check (worktree wave13 = origin/main per the brief): Grep of the four sites in `handoff_check.py`, `runtime_probe.py`,
`null_outcomes.py` — same lines, same text.
Not run: any test or script (the designer runs nothing); the `--witness-for` outputs above are EXPECTED from the keep rows read in
`test-layers.json`, not printed.
Needed beyond the manifest: the files listed in this trail outside the brief's "given" (all read-only).
