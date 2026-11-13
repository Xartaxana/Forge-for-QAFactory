# t-521 — critic, code gate for the whole topic P1-a "writer -> reader round" (N0-N3)

Diff under review: `git -C .claude/worktrees/p1a-n3 diff 049ad7b~1 8580665 -- ai-packages/qa-factory` (HEAD 8580665).
Spec: `docs/tasks/specs/20261113-p1a-writer-reader-round-spec.md` (§3.4-3.7, §4, §4.1-4.3, §5 N0-N3, §6, §8-§10).
Critic: opus (claude-opus-5-5). The verdict is an input to acceptance; the decision belongs to Lead.

**Verdict: ACCEPT WITH FIXES. B1-B3 block the merge, and F1-F9 land in the same fix round. Q1-Q9 go to the queue.**

The machinery is sound. `known_red` is right on every edge of §3.6. The rounds call the real readers. An exception in a row
turns that row red. An empty registry turns red. The witness reproduces exactly. The problem is the ledger: about 60 of its
79 rows do not record a defect of main. They record a test world that is too poor, or a filler template that ignores what the
factory tells the role. 55 of those rows point at node ids that do not exist anywhere. If the layer merges like this, the
owner's piles get false product defects. Worse, 54 deriver fields are already red, so a regression in any of them would
stay invisible.

## Mechanical layer: control re-run and consistency
- Re-run: `python -B .../scripts/tests/test_field_producers.py` gave `=== test_field_producers: 906/906 ok ===`, `known red rows 79,
  rows walked 896`, `readers 20, pairs 62, languages 4`, `deriver round: forms 24, fields met 28`, `forms 24, variants 434, fields 937,
  unfillable 0, left_for_code 82`, and exit 0 in 15.08 s wall. This matches the N3 witness.
- The witness numbers are consistent:
  - Before the ledger: 985 = 906 + 79 new-red problem rows, and 159 fails = 79 rows + 79 problems + 1 summary.
  - Negative control: 907 = 906 + 1, and 3 fails = the row itself + `new red` + the summary.

## Findings

### BLOCKER
**B1. The ledger records rows that are not defects of main. Their nodes are placeholders and their raises are self-authorised (K2, K4).**
`form-rounds.json:50,71,73-126`. I sampled 10 of the 54 `derive:` rows, ran a probe on the round world, and traced the derivers
in `handoff_check.py`:

| row | verdict | why |
|---|---|---|
| s1-scout-to-tester:implementation.diff.files | world | `_diff_counts` needs a diff under `work/` (`:321-337`); `impl-diff.txt` is NotCovered, so the world has none |
| s2-tester-to-strategist:size.computed | world | `_size` reads `work/sizing.json` (`:458-460`), which code writes (sizing.py); not in the world |
| s3-strategist-to-designer:grounding.hunks | world | the grounding.yaml template exists (N2b), but `_round_world` (`test_field_producers.py:989`) does not write it, and there is no diff |
| s4-designer-to-case-critic:scope[0].case_version | world | `_case_version` reads `story-case-links.json` (ByCode, case_versions.py); absent |
| s4-designer-to-case-critic:scope[0].requirements | world/filler | the form row says `id: 'filled id'` (probe), not the world's `TC-001`; the deriver round's `FillContext` (`:1287`) carries no cases/minted |
| s5-automator-to-runner:inputs_read[0].version | filler | path `work/handoffs/<the gate A file>.yaml` stays unfilled; the test skips paths with `<` (`:1290`); `_version_of` returns None on `<` (`:482-486`) |
| s6-runner-to-analyst:run.totals | world | needs run-report.json (ByCode finalize_task) |
| s8-scribe-to-gate-b:delivery.ready | world | needs ledger.json (ByCode ledger.py) |
| s3-strategist-to-designer:scope[0].requirements | **real** | see P5: leaf `requirements` makes `_code_fills` true (`:2734`), but `_requirements_of` reads a CASE front matter (`:414-427`), and a plan row is no case |
| s8-bug-reporter-to-scribe:filed[0].requirements | **real** | same over-match: `filed` rows carry `cases` and have no `case`/`id`, so the deriver can never answer |

Result: about 7 in 10 are a poor world or the filler, and 3 in 10 are real. Two non-derive rows are filler artifacts too:
- `output: project:bugs/[base]`: the template (`form-fill-rules.json:316-328`) takes only the filing-header section. The bug
  writer is told all eight fields in its brief card (`references/ahead-cards.json:84`: "Frontmatter is checked: id, title,
  severity, status, area, found_by, created, violates"). This is a template defect, not a product defect, and node `P1A-1`
  is wrong.
- `obligation_refs <- manifest_from_tests@python`: the `test_file:<lang>` template (`form-fill-rules.json:205`) writes
  `qa(case=..., then=[1])` without `obligations=`. The automator is told to write it (`agents/qa-automator.md:69`
  "`obligation_refs`: `qa(obligations=)`"; `s5_precheck.py:3791`). The probe shows the marker carries no obligations, so
  `row_field_gaps` answers `missing`. This is the test world, not FV1-19.

`P1A-1` and `P1A-2` exist in no pile. I grepped `P1A-[12]` over `plans/` and `docs/tasks/specs/*.md`: 0 hits. The positive
control, `FV1-19`, was found in `batch-1-live-run-fvf.md:58`. The `raised_by` of these 58 rows is the builder's own
measurement, but §3.6 requires a critic verdict path or a word from Lead. This verdict does NOT name those raises.

What must land:
- (a) The deriver round fills each form with the world's context (cases, minted ids, dispatch ids).
- (b) The world holds the inputs the filler can already make (grounding.yaml) and the code-made inputs that are cheap to run.
  For each input that stays out, Lead decides the outcome and gives it a REAL node.
- (c) Fix both templates (bugs, test_file), and re-measure.
- (d) Every remaining row carries an existing node.

**B2. The filler leaves hints and context tokens embedded inside values, silently: neither filled nor `Unfillable` (E10, E12).**
I probed every form, base variant. 50 values still carry `<...>` outside `left_for_code`, for example:
- `inputs[0].path: 'work/handoffs/<dispatch>.yaml'` in 9 forms (`<dispatch>` is a context token in §3.2);
- `inputs_read[0].path: "work/handoffs/<the automator's file>.yaml"`;
- `'work/test-cases/<area>/<case>.md'`.

Some are literal command templates (`recorded_by: 'waiver.py --task <T> ...'`) and are legitimate as text. The path values are
not. The N1 summary says `unfillable 0`, which is false. The same gap produces at least 7 false `derive: ...inputs_read[N].version`
rows. Fix: substitute tokens inside a value; leave any other embedded hint as an `Unfillable` (or as a named literal-text rule).

**B3. The R7 carriers are not on the branch or on main (merge condition from spec §9 R7, AR-20 change check).** I grepped
`known_red` case-insensitively in `docs/SIBLING_MAP.md`, `design/architecture.md` and `docs/tasks/critic-diff-brief.md`, in the
worktree, the root checkout and `origin/main`: 0 hits. The positive control, `lint_ratchet` in the same files, gave 2 and 1. The
ledger is a new shrink-only ratchet, and axis 18, the AR-20 Carriers and question 9 must land with it. This is Lead's node
"P1 carriers"; it is merge-blocking, not a builder fix.

### FIX (same round)
- **F1 (K1, K8, Q12b).** The language rows run on the Python file:
  - `_marker_entry` hard-codes `tests/TC-001_test.py` (`test_field_producers.py:1105`).
  - `_f_row_fields` throws away the per-language fill (`:1124-1127`).
  - The template family `test_file:<lang>` has a Python body and a `_test.py` name for every language (`form-fill-rules.json:193-207`).

  Today `Unfillable` hides this. Once FV1-19 adds a marker form for csharp, the csharp row would judge the Python file and the
  ledger would go "stale" on the wrong data. The body and extension per language must become data rows, and the row must read
  the file it filled.
- **F2 (K2).** The `plan-row: s4.scope[].plan_row -> handoff_check._plan_row_of` row is attributed to the wrong node
  (`form-rounds.json:56`, FV1-14). `_plan_row_of` (`handoff_check.py:429-440`) reads the front-matter key `plan_row:`. The case
  contract's front matter (`artifact-contract.md:59-62`) does not list it; it gives the body line `Plan row: TS-n`. So the row
  stays red even on a TS-n case, and fixing FV1-14 will not turn it green. It needs its own finding and node (product defect P2).
- **F3 (K1, tuned to the reader).** The world of `output: manifest_row[base]` writes the case as the `cite_hint:body:Plan row:`
  variant, TS-1 (`test_field_producers.py:568`), so the manifest reader passes. A row named `[base]` is built on a non-base case.
  Either name the row after the variant, or use the base case and let the refusal show.
- **F4 (K3).** There is no pin on the number of `readers` rows or families; spec §6(c) asks for it. Only `walked > 0` exists
  (`:1265`). Deleting a green reader row, or a red row together with its ledger row, passes silently.
- **F5 (K7, duplication).**
  - `_in_project` (`:961-974`) and the inline environment swap in `refusals()` (`:569-579`) are the same code.
  - There are two language sets: `form_filler.test_file_languages()` (`form_filler.py:586-599`, reads `detectors.json` sections
    directly and adds the runner key `pytest`, 5 names) and `_languages()` (`test_field_producers.py:1201-1215`, through
    `languages_source`, 4). One reader is needed (axis 34).
- **F6 (K7, a name that lies).** The `tool_fields` rows name `handoff_check.check` as their reader, but they judge
  `bool(producer)` taken from `walk()` (`:1131-1132`, `:1192-1195`). `check` is never called. This re-judges
  `every_required_field_has_a_producer_or_a_declared_gap` (`:117`). Name the real judge, or drop the duplicate rows.
- **F7 (K8).** `covers` lacks `references/slices/qa-test-strategist/handoff-keys.md`, an identity carrier in
  `form-rounds.json:40-42`. After B1(c) it will also need `references/ahead-cards.json` and `agents/qa-automator.md`.
- **F8 (K5).** The N3 time line ("8.2 s, no measurable slowdown") compares whole-file runs. It is not a measurement of what N3
  adds. My run took 15.1 s; before the layer the file took 0.6 s (N1 report). That is about 14 s added against the 10 s budget
  in spec §2. Spec §2 asks for the number in a report line, and Lead decides.
- **F9 (K8, §4.2/§4.3 not delivered and not explained).**
  - The family "words whole -> brief_pack" with a ledger row for RC2-1 (Lead decision F7(a), spec §1.1 AR-24) is absent.
    I searched `RC2-1|question_answer|value whole` in the 3 new files: 0 hits. The positive control, `FV1-22`, was found.
  - The `report_facts` search for "unadapted readers" (§4.3) was not done. `report_facts.py:274,784` reads `ts` through
    `contract.parse_plan`.

  Do both, or have Lead queue them by name.

### QUEUE
- Q1 (K6). The "outputs no reader refuses" list (8 outputs) and the not-covered list (6 outputs) live only in stdout; open a
  finding for each.
  - Not covered: I spot-checked two reasons and both are true. `s5_plan` writes its skeleton without hints (N2c report :78).
    `artifact-contract.md:184` names `obligations.md` with no shape.
  - No reader refuses: I spot-checked two and both are true. A probe on `requirements-readiness.json` without `verdict` gets
    `collect_errors` == []. `grounding.yaml` without its `rows:` line gets [].
- Q2. `check` merges repeated ids with AND (`:59`), so a second case under an id already in the ledger is hidden. There are no
  duplicates today (`uniq -d` over the run output was empty). Refuse a repeated id instead.
- Q3. A known-red row whose failure changes (for example, to a crash) stays "known red"; the detail is not compared.
  Acceptable by design.
- Q4. `fill_form` (`:1287`) and `_round_world` sit outside the per-row try. A crash there is loud (the file dies), never silent.
  E14 is partial.
- Q5. `marker_form` re-reads `case-markers.json` instead of `manifest_from_tests.load_case_markers` (`:93-106`). That product
  reader hard-codes `pytest`, which is itself the FV1-19 class. A second reader, justified; note it with FV1-19.
- Q6. `_reference("artifact-writers.json")` (`form_filler.py:532-536`) uses `json.loads`, not `hooklib.load_ref_json` as spec
  §1.1 AR-13 says.
- Q7. Spec §6(b) says axis 27 (the `profile_id` variant) is covered. It is not implemented: `profile_id` is free text. I grepped
  `profile_id` in the rules and the test: 0 hits.
- Q8. The filler's own error-path batteries (N2c marker edges, `case[no issued id]` and the like) go beyond the spec table; see
  `docs/TESTING.md:55`. `known_red_ledger_cases` is legal by Lead's F11 (plan :241).
- Q9. The `sed -i` on `form-rounds.json` (hygiene point 4) is self-reported, and the content is equivalent. Calibration notes it.

## Answers per key
- **K1.**
  - Real joints:
    - `contract.case_plan_row` / `s5_precheck.case_plan_row`: the case comes from `fill_artifact`, and its base cites the
      minted P-1 per §3.5 (live evidence FV1-1).
    - `acceptance.stage_acceptance_errors`: the record is built by `fill_form(..., verdict="concerns")` and the real
      `stage_acceptance_from_form` (`:1085-1091`).
  - Composed by the test:
    - `validate_artifacts.check_plan_v0`, `plan_levels`, `_case_map`, `plan_by_ts`: `_plan_with` (`:1020-1029`) puts the S3
      form's P-1 into the plan's TS cell. That plan writer's own hint is `<TS-n>`, and its twin row is green. So these rows
      restate the identity defect; they are not independent defects.
    - `pattern_whole` regexes: P-1 is handed straight to a regex whose carrier hint is TS-n.
  - Tuned to the reader: F3. Templates that ignore what the factory tells the role: B1 (bugs, test_file).
- **K2.** See B1 and F2. Verdict on `manifest_from_tests@python`: a poor world/template, not FV1-19.
- **K3.** Both directions hold: new red, stale, unknown, a missing `raised_by` (`known_red.py:72-117`) and the empty
  registries (`:952-958`, `:1213`); a row exception is that row red (`:1256-1259`). Gaps: F4, Q2, Q4.
- **K4.** The `test_file:*:marker` rows and the obligation rows for 3 languages are real (FV1-19), but the same defect is
  counted twice. `project:bugs/[base]` is not real (B1). "A green file with N red rows in its ledger" is honest under
  AR-20/AR-28 only when every row is a defect with an existing node. Today it is not, and the placeholders are a defect (B1).
- **K5.** It stays one keep file, and every id names its case. Time: F8.
- **K6.** The reasons are true; carrying them as findings is Q1.
- **K7.** F5, F6, Q5, Q6.
- **K8.**
  - Axis 5 (stage twins): one table over every stage, pinned in both directions against stages.json (`:527-530`). Covered.
  - Axis 18 (ratchets): B3.
  - Axis 23 (the fields of a `tests[]` row): `REQUIRED_ROW_FIELDS` is read through `form_filler.row_fields`. Covered.
  - Axis 27 (the profile of a test row): Q7.
  - Axis 34 (one road): F1, F5.
  - §4.2: `check_plan` was replaced by `check_plan_v0`, and the report explains it. The python control row is red: B1.
    RC2-1 and report_facts are missing: F9.

## Standing questions
- **DUPLICATION AND CONSISTENCY:** F5, F6, Q5. Searched: `case-markers` over `scripts/*.py` (manifest_from_tests.py:85-106 is
  the reader); the `CLAUDE_PROJECT_DIR` swap inside the test; the language-set readers.
- **CODE QUALITY:**
  - `every_stage_output_fills_or_is_named`, about 420 lines (`:508-932`), and `every_reader_takes_what_its_writer_writes`
    (`:1218-1266`, nesting 4) are over the brief's cap. Queue a split; it does not block.
  - Names that lie: F6.
  - Dead input: `_f_case_levels` ignores `value` (`:1059-1060`).
- **ARCHITECTURE (q10):** AR-13 (Q6), AR-20 (B1, B3), AR-22 (deriver round, B1), AR-28 (B2: an unknown hint passes as filled).
- **JUDGMENT (q11):** none. Tests sit outside the census, and no role judgment moves into code.
- **ONE ROAD (q12):** F1. Searched: language names in the `+` lines of the diff. The only data row is `marker_key
  {"python":"pytest"}`; the hidden roads are the hard-coded `_test.py` path and the Python body.

## Real product defects the ledger proves (for the owner's piles)
- **P1 (FV1-1/FV1-14).** The plan-row id is P-n in the S3/S4 forms and `handoff-keys.md`, and TS-n in the plan md, the case
  body and the plan JSON. Rows: the two `case_plan_row` rows, `identity`, `agree`. The 10 rows of TS-only readers are
  consequences of this one split.
- **P2 (new).** `handoff_check._plan_row_of` reads the front-matter key `plan_row:`, which the case contract does not define
  (`artifact-contract.md:59-62`). One note: the live fixture `fixtures/case-id-form-13877/.../cv_*.md:14` shows that roles
  did write `plan_row: TS-6`. Where they were told to do that is unknown and is part of the finding.
- **P3 (FV1-22).** The S7 acceptance rows (2).
- **P4 (FV1-19).** No marker form for csharp/java/typescript.
- **P5 (new, candidate).** BY_LEAF over-match. The leaf `requirements` marks S3 `scope[].requirements`, S3
  `inputs_read[].requirements` and S8 `filed[].requirements` as code-filled (`handoff_check.py:2734`), but `_requirements_of`
  (`:414-427`) can only answer for a case row. These are role fields excused when blank and never filled by code, which spec
  §4.1 calls the forbidden direction.
- **P6 (candidate).** `validate_artifacts.collect_errors` accepts `requirements-readiness.json` without `verdict` (probe).

## Trail
Read:
- Spec: whole.
- N3 report: whole.
- `form-rounds.json`: whole.
- `known_red.py`: whole.
- `test_field_producers.py`: `:1-120`, `:508-637`, `:930-1402`.
- `form_filler.py`: `:528-977`.
- `form-fill-rules.json`: `:185-215`, `:316-335`.
- `handoff_check.py`: `:321-490` (derivers), `:399-440`, `:554-610`, `:926-940`, `:2725-2735`.
- `harness.py`: `:115-153`.
- `manifest_from_tests.py`: `:85-120`, `:740-760`.
- `references/case-markers.json`; `references/artifact-contract.md:50-72`, `:170-190`; `references/artifact-contract-run.md:136-150`;
  `references/ahead-cards.json:84`; `agents/qa-automator.md:69`.
- The `test-layers.json` diff.
- `critic-diff-brief.md:25-101`; `docs/TESTING.md:50-60`.

Probes (scratchpad):
- `probe1.py`: the round world, the python marker row → marker without `obligations`, gaps `obligation_refs missing`.
- `probe2.py`: the deriver round for 4 contracts → `filled id`/`filled case` rows; an unfilled path hint.
- `probe3.py`: broken variants of 2 outputs → `[]`.
- `probe4.py`/`probe5.py`: 50 embedded hints, `unfillable []`.

Searches with controls: `P1A-[12]` (0; control FV1-19 found); `known_red` in the R7 carriers (0; control lint_ratchet 2/1);
`^plan_row:` across the package (only the live fixture); `found_by` (ahead-cards only; control source_draft 3 files);
`RC2-1|...` (0; control FV1-22); `profile_id` (0).

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "B1 ledger: ~54 derive rows (sample 7/10 world or filler), project:bugs/[base] (template ignores ahead-cards.json:84) and obligation_refs@python (template omits obligations= per qa-automator.md:69) are not defects of main; placeholder nodes P1A-1/P1A-2 exist nowhere; 58 raised_by self-named (form-rounds.json:50,71,73-126)",
    "B2 filler leaves 50 embedded hints/context tokens in values neither filled nor Unfillable (E10/E12); the summary unfillable 0 is false; causes false derive inputs_read version rows",
    "B3 R7 carriers (SIBLING_MAP axis 18, AR-20 Carriers, critic brief q9) absent on the branch and on origin/main; Lead node P1 carriers must land with the merge"
  ],
  "fixes": [
    "F1 _marker_entry hard-codes tests/TC-001_test.py and discards the per-language fill (test_field_producers.py:1105,1124-1127); the test_file template body/extension is Python-only (form-fill-rules.json:193-207)",
    "F2 re-attribute the _plan_row_of row: it reads front-matter plan_row absent from artifact-contract.md:59-62; new finding, not FV1-14",
    "F3 manifest_row[base] world uses the cite_hint case (test_field_producers.py:568): rename or use the base case",
    "F4 pin the number of readers rows and families (spec 6(c)); only walked>0 today (:1265)",
    "F5 duplication: _in_project vs inline swap in refusals() (:961-974 vs :569-579); two language sets test_file_languages vs _languages",
    "F6 tool_fields rows name handoff_check.check but judge bool(producer) from walk() (:1131,:1192); re-judge of every_required_field...",
    "F7 covers misses references/slices/qa-test-strategist/handoff-keys.md (and ahead-cards.json, agents/qa-automator.md after B1)",
    "F8 report the in-process seconds N3 adds; measured whole file 15.1 s vs 0.6 s before the layer, over the 10 s budget: Lead decides",
    "F9 RC2-1 words-whole family (Lead F7(a)) and the report_facts unadapted-readers search (spec 4.3) absent: do or queue by name"
  ],
  "class_completeness": "Axis 5 covered (one table, pins both ways against stages.json); axis 18 blocked on R7 carriers (B3); axis 23 covered (REQUIRED_ROW_FIELDS read from window_record); axis 27 not implemented (profile_id free text, Q7); axis 34 hidden Python road in the language rows and two language sets (F1, F5). Spec 4.2: check_plan->check_plan_v0 explained; python control red is a template artifact (B1); RC2-1 family and report_facts search missing (F9).",
  "trail": {
    "read": [
      "docs/tasks/specs/20261113-p1a-writer-reader-round-spec.md",
      ".claude/worktrees/p1a-n3/docs/tasks/specs/reports/20261113-p1a-n3-report.md",
      "ai-packages/qa-factory/scripts/tests/fixtures/form-rounds.json",
      "ai-packages/qa-factory/scripts/tests/known_red.py",
      "ai-packages/qa-factory/scripts/tests/test_field_producers.py:1-120,508-637,930-1402",
      "ai-packages/qa-factory/scripts/tests/form_filler.py:528-977",
      "ai-packages/qa-factory/scripts/tests/fixtures/form-fill-rules.json:185-215,316-335",
      "ai-packages/qa-factory/scripts/handoff_check.py:321-490,399-440,554-610,926-940,2725-2735",
      "ai-packages/qa-factory/scripts/manifest_from_tests.py:85-120,740-760",
      "ai-packages/qa-factory/references/artifact-contract.md:50-72,170-190",
      "ai-packages/qa-factory/references/ahead-cards.json:84",
      "ai-packages/qa-factory/agents/qa-automator.md:69",
      "docs/tasks/critic-diff-brief.md:25-101",
      "docs/TESTING.md:50-60"
    ],
    "reruns": [
      {"command": "python -B .claude/worktrees/p1a-n3/ai-packages/qa-factory/scripts/tests/test_field_producers.py", "result": "=== test_field_producers: 906/906 ok ===; known red rows 79, rows walked 896; deriver round: forms 24, fields met 28; exit 0, 15.08 s"},
      {"command": "python -B scratchpad/probe1.py (round world, python marker row)", "result": "marker @pytest.mark.qa(case=TC-001, then=[1]) has no obligations; row_field_gaps -> obligation_refs missing"},
      {"command": "python -B scratchpad/probe5.py (embedded hints in filled forms)", "result": "embedded hints left silently: 50; unfillable []"}
    ]
  }
}
```
