# Critic review: P1-b N0 (dry-story spike), rounds 1-3 as one diff

Diff: `git -C .claude/worktrees/p1b-n0 diff 62421cf..1c1d08c` (HEAD verified `1c1d08cd75f1`). Spec: P1-b N0 `:522-540`, F12 `:804`.
Round-3 amendment: section 5, items 1-9, E-R1..E-R11, forks taken by recommendation.

**Verdict: NEEDS WORK (fit_with_fixes). 0 blockers, 8 fixes. Three of them (F1, F2, F4) must land before N1/N2 build on this base.**

## Findings (numbered, with severity)

**F1. AR-28 residual in the numbers branch. Fix before any gate number is counted (N2), queue owner: the N2 node.**
- `gate_line` correctly prints `undecided` while S3 is not done (`dry_world.py:501-508`).
- But once S3 is done, the median and the worst row come from every row's seconds (`dry_world.py:572-573`, printed at `:594`), and that includes rows that never reached their named question:
  - `live_only: expected a halt question...` (`:423`);
  - `red: no answer...` (`:427`);
  - `after: snapshot ... not found`, which takes about 0 s (`:415`);
  - `no question` (`:421`).
- Failure scenario: S3 is done, and two rows stop early at about 1 s each. The median is then about 1 s and the verdict prints `continue`. That verdict rests on rows that measured nothing.
- The same happens on CI today: row `halt/words` (6.8 s) is a `live_only` row and still feeds the median 8.0.
- A second gap: snapshot reds (`:589-590`) set exit 1, but the gate line still prints a verdict.
- Fix: the numbers verdict needs S3 done AND every row `asked <kind> (as expected); answered` AND no red. Otherwise print `undecided -- row <id>: <outcome>`.

**F2. E-R3 holds for type rows only. Fix before N1 adds walk rows with `stub`.**
- Row `stub` overlays (`probe.json`, item 2) never pass `check_stub`. `run_row` sends `row.get("stub")` through `World.control` and `merge_stub` (`dry_world.py:417,216-219,132-137`) without checking it.
- `merge_stub` also replaces a declared judgment WHOLE, not field by field.
- Probe witness (scratchpad script, pure functions, no repo write):
```
merged: {'source_relevance': {'A-1': {'relevance': 'maybe'}}}
RAISED KeyError 'reason'
```
- So a row entry without `reason` crashes the stub at `dry_stub.py:154` (`decl["reason"]`). The driver then sees an unlabelled failed role call.
- A value `maybe` would reach `ticket_adapter` argv. That argv check refuses it, so this is not a pass, but it breaks the E-R3 invariant "never reaches the factory".
- Fix: run `check_stub` on each probe/walk row's `stub` when the rows are loaded (A1-E4 form, red before the world is built). Then `.get` in `judge_sources` stays only as a guard.

**F3. Spike runs look like a green canon. Fix before merge to main. The pin file is outside the owns, so the Lead routes it.**
- `run-name: canon ${{ inputs.ref }}` (`canon.yml:15`) also names spike runs.
- A spike run concludes `success`: `checks` and `full` are skipped, the spike passes, and `clock` passes.
- `ci_read.py pipelines` prints `display_title` (`tools/ci_read.py:171`). So run 43500065530 lists as `canon wip/p1b-n0` success, the same as a real BATCH CANON. A coordinator looking for "the green canon of the branch" can take it.
- Also, `clock` (`needs: [start, checks, full]`, `if: always()`) runs on spike runs and measures nothing meaningful.
- Fix: make the run-name conditional (for example `${{ inputs.spike && 'dry-spike' || 'canon' }} ${{ inputs.ref }}`), add `if: ${{ !inputs.spike }}` to `clock`, and update the pin at `tools/test_workflows.py:273`.

**F4. DUPLICATION inside the diff. Fix before N2 grows the stub.**
- `dry_stub.py` runs a package script three ways: `run_script` (`:117-121`) and two inline `subprocess.run` blocks (`:246-249`, `:269-273`).
- The repository already has `harness.run_script` (`harness.py:232-240`). It sets `PYTHONDONTWRITEBYTECODE` and `timeout=300`; none of the three copies has a timeout.
- The text form `<cmd> exit N: ' '.join(text.split())[:400]` is copied 5 times (`:151,:160,:171,:249,:273`).
- Fix: one runner over `harness.run_script` plus one `cut()` helper.

**F5. DUPLICATION with the repository: a clone pair. Queue as a node; the Lead opens it.**
- `TrackerServer` + `direct_api` (`dry_world.py:150-191`) is a clone of `FakeJira` (`test_story_run_s0.py:76-119`).
- The probe-receipt seeding in `build_world` (`dry_world.py:237-246`) is a clone of `rest_project` (`test_story_run_s0.py:127-142`). `PERSON_TOKEN_ENV` is duplicated as well.
- The survivor belongs in `story_run_common.py`, with the no-route status as a parameter (404 vs 500). It touches `test_story_run_s0.py`, outside N0's owns.
- N1/N2 do not add a third server, so this does not block them. N3t (the `local` tracker kind) must not add a third copy.
- Mechanical layer missing: the clone ratchet result (`forge-check` of the branch) is not attached and never ran, because the spike dispatch skips `checks`. Request: one `forge-check` run on `wip/p1b-n0` before the PR.

**F6. Small fix: provenance is not enforced.** Item 1's shape carries `from`, but `check_stub` (`dry_world.py:118-129`) does not require it. The probe shows a judgment with no `from` loads silently. Without `from`, the value is not "declared and sourced" (AR-29). Require a non-empty `from`.

**F7. Small, queue: names that mislead.**
- `NOTE: unused judgment <key> (the stub never judged...)` also fires when the key WAS used but `peek`/`assess` refused (`dry_world.py:526-529`), because only successes go into `judged`.
- The `spike[...]` line prints `S0..S3 11.8 s` when only S0..S1 ran (`:592`). That is the literal DoD form, and the gate line corrects it.
- Fix: a separate note for refused keys; print `S0..<reached>` on the spike line.

**F8. Accuracy of the round-3 report.**
- Q1 and Deviation 2 say the collection of TP1-15791 "brings in six more mentioned tickets". The CI witness says `1 mentioned source(s) await` (TP1-10937 only). The other five may arrive later, or be non-required. The Lead's Q1 decision should rest on the measured count.
- Stop 2 (`s1_gap`, `vcs_evidence ... cli_missing`) is labelled a person-side closed answer. Its cause is equally a world gap: the dry world serves no VCS route or CLI (A1-E8). The choice for N2 is between the world and a probe answer, not only a probe answer.

## Answers by question

**1. DoD of round 3.**
- Item 1 met: `dry-types.json` has `stub.source_relevance`. The value and reason were verified at `investigation-14857/.../source-inventory.json:432-433`.
- Item 2 met: `merge_stub`, `World.control` `:216-219`. Caveat: F2.
- Item 3 met: `judge_sources` `dry_stub.py:124-174`, wired at `:250-258`. Selftest checks the argv exactly.
- Item 4 met: `collect --relation referenced` only for keys the stub judged (`:161-171`), matching `s1.md:160-163`. `inspect` is not run.
- Item 5 met: `read_sources` → `SI.load_inventory` (`:81-87`).
- Item 6 met (see Q6).
- Item 7 met for S3-not-done (`:501-508`). The numbers branch is weak: F1.
- Item 8 met (`:511-523`, `:562-571`).
- Item 9 met (`probe.json` row 3).
- Edges:
  - E-R1 met (`:142-143`, selftest).
  - E-R2 met, with a naming caveat (F7).
  - E-R3 met for type rows, open for row overlays (F2).
  - E-R4 met: the `tried` set; selftest shows calls `peek, assess` only.
  - E-R5 met (`:148-152`).
  - E-R6 met (selftest row "a row without `stub`").
  - E-R7 met (CI gate line `undecided -- ... S1`).
  - E-R8 met.
  - E-R9 met: `Road.drive` `for..else` (`:488-489`). A stage with no label shows as `UNLABELLED RED`, never as a pass.
  - E-R10 met (selftest `x*400`; gate line cut at 160).
  - E-R11 met (no hand-written forms; J16 left `live_only`).
- DoD 6 met: the commit `9cf28f5` carries `architecture:` lines for AR-29, 28, 14, 13, 1, 23, and `judgment: none`.
- Control re-runs:
  - `dry_stub --selftest`: 57/57 ok.
  - `selftest.py --lang`: 2/2 ok.
  - `test_field_producers.py`: 921/921, known red 29, not in world 47.

**2. AR-28 / FR-41.**
- With S3 not done, no path prints `continue`. `gate_line` branches on `state.get("S3") == "done"`, and missing `pipeline.json` reads as absent, which gives `undecided`.
- A failed command is `live_only` with its text, never retried within a call. A repeat dispatch re-runs with the SAME declared value, never another value. The only other value comes from a declared row overlay.
- Residuals: F1 (the numbers branch counts failed rows) and F2 (an unvalidated overlay crashes the stub).

**3. JUDGMENT (P27 / AR-29 / AR-7).**
- No code in the diff decides relevance. `declared.get(key)` is a lookup. `awaiting()` reads the `relevance` and `status` fields. The order peek → assess → collect replays the `s1.md` procedure.
- `collect` after a declared `relevant` is a read through the one writer: it fetches pages and bytes and records mentions as `pending`. It decides nothing. The report's claim holds.
- Residual for N2: closed verdicts still default to "the vocabulary's first word". This is `form_filler.fill_form`, P1-a code (`form_filler.py:424-445`), not this diff. When S2 is reached, `ready` (readiness) and the critic `accept` become code-chosen judgments with no `from`. That is inconsistent with the round-3 standard. Proposal: N2 declares them in `stub.<role>.verdict` with provenance, the same grammar.
- `judgment: none` is truthful for this diff.

**4. AR-14 / AR-13.**
- The stub never writes `source-inventory.json`. Grep `write_text|write_bytes|open(` over both files: the only writes are the stub journal (`:209-211`), the handover form the role fills (`:243`), role outputs via `FF.write_outputs`, and selftest temp files. Positive control: the same grep finds `:243`.
- The inventory is read only via `load_inventory`. `FakeRole` writes JSON in selftest temp only.
- The world seeds `jira-direct-probe.json` (`dry_world.py:241`), whose product writer is `readiness.py`. This is test-world seeding, the same as `rest_project`, not a new class (F5).
- `_rewrite` relocates paths in a COPY and skips `events.jsonl`.

**5. AR-1 / P2.** Grep `codemie|14857|TP1-|15791|mr-4566` over both files (case-insensitive) hits only selftest lines (`dry_stub.py:358,370-375,387,471-472`). Positive control: `dry-types.json:1,3`. The road and the stub have no type branch.

**6. Register template.**
- The template matches the contract exactly:
  - `Branches: none -- <why>` matches `NONE_LINE_RE` (`branch_accounting.py:59`);
  - the header `| unit | home |` equals `OBLIGATION_COLUMNS` (`:58`);
  - `rest | unreconciled: <why>` is the remainder form (`_take_rest` `:688-700`), and the contract states the same at `artifact-contract-plan.md:19-23`.
- No `## Attachments` row was added (it was not asked for).
- Consumers of `form-fill-rules.json` / `form_filler`: only `dry_stub.py`, `form_filler.py` and `test_field_producers.py`. Positive control: `dry_stub.py` is found by the same grep. No other test world can change.
- Re-run: counts 29 / 47 unchanged.
- Note: `rest` produces a gate-A debt (`source_unreconciled`, `:2385`), but `Branches: none` produces none. The `<why>` says it is not a judgment, so it is honest text. N2 must still not count "S2 done" as proof that branch accounting works.

**7. Snapshot guard and the loop bound.**
- `tree_hash` covers sorted relative paths plus bytes. A change prints `red: snapshot changed by a row: <id>` and exits 1. The hash is reset after a red, so the next row is judged on its own.
- The 8-round loop in `judge_sources` breaks when nothing moved. When it runs out, whatever is left is named by `pending_judgments` (`:256-258`), never dropped.
- `Road` reaching 12 turns gives `undecided`. A driver timeout gives rc -9 with a line.
- Loud in every case, except F1 (red still prints a verdict).

**8. `canon.yml`.**
- The only trigger is `workflow_dispatch`, and the boolean `spike` defaults to false. `checks`/`full` carry `if: !inputs.spike`; the spike job carries `if: inputs.spike`.
- So the canon jobs and what they judge are unchanged. Re-run: `tools/test_workflows.py`, 26 passed.
- The labelling and clock issue is F3.

**9. DUPLICATION / CODE QUALITY.**
- Duplication: F4 (inside the diff) and F5 (with the repository).
- `dry_stub`/`dry_world` vs `form_filler`: no clone; the stub calls `fill_form`/`fill_artifact`. Against the scenario walk: no runner clone found. `drive()` streams with time stamps, which `run_driver` (`story_run_common.py:333`) cannot do, so it is a justified second runner.
- Size:
  - `spike()` `dry_world.py:536-597` is 62 lines (queue: split print/measure);
  - `selftest()` `dry_stub.py:319-522` is 204 lines, but it is a case table (queue: split into tables);
  - `fill_role` `:220-277` is 58 lines.
- No nesting deeper than 3 found.
- Is there a clone that must become one survivor before N1/N2? F4, yes, because N2 grows the stub. F5 can wait as a node.

**10. Class completeness and stops.**
- Axis 34 covered: one road, `ticket_adapter` commands, a data row keyed by ticket.
- Axis 17: the output lines keep one shape. `outcome`/`gate` lines are not package detectors, so `detector_verdict` form 1 does not apply.
- Axis 18: no ratchet or baseline in the diff (`test-layers.json`, `dup-baseline` not touched). The clone ratchet result is still missing (F5).
- Sibling of F2 in the same artifact: `closed_answers` row words are also unvalidated. They are free text by design, so this is not applicable.
- Stops:
  - Stop 1 is truthful against the CI lines.
  - Stop 2 is honestly marked "local probe, not a witness" (byte-copy restore with hash), but its cause label is incomplete (F8).
  - Stop 3 is truthful.

**11. For the Lead's gate decision (the decision stays with the Lead).**
- Nothing in the code is a reason not to build N1/N2 on this base, provided F1 (before any numbers verdict counts) and F2 and F4 (before N1/N2 add rows and stub steps) land first. Those three are small.
- What is not shown:
  - feasibility past S1: S2 and S3 are unreached, there are two known further stops (the declarations of the cascade, `s1_gap`), and J10, J11 and J16 are untried;
  - time on the full road: on the partial numbers, 2.5 x 11.8 + 120 x 8.0 = 989.5 s, about 16.5 min. That is over the spec's own 15-min estimate (`:536`), although it sits under both per-number "continue" thresholds (120 s, 20 s).
- The row median comes from rows that ended at S1 (F1), so it is a lower bound, not a measure.

## Trail

- Read:
  - the round-3 amendment, whole;
  - P1-b `:520-545`, `:800-810`, `:489`;
  - the round-3 report, whole, and round-1 report `:84-111`;
  - `dry_stub.py`, whole;
  - `dry_world.py`, whole;
  - the diff of `canon.yml`, `form-fill-rules.json`, `form_filler.py`, `test_field_producers.py`, `dry-types.json`, `probe.json`, `routes.json`, `story.json`;
  - `canon.yml` at HEAD;
  - `artifact-contract-plan.md:12-34`;
  - `branch_accounting.py:50-80,680-712,732-770`, plus greps;
  - `s1.md:144-165`;
  - `harness.py:232-240`;
  - `test_story_run_s0.py:76-142`;
  - `story_run_common.py:333-353`;
  - `form_filler.py:424-445` (grep);
  - the recorded `source-inventory.json:380-434`, plus grep;
  - `SIBLING_MAP.md` axes 17, 18, 34;
  - `critic-diff-brief.md`, whole;
  - `tools/critic_verdict.schema.json`.
- Provenance: the 9 tracker files are sha256-identical to committed `investigation-14857/TP1-14857/work/sources/...` files. A secrets skim of `mr-4566.diff` and the ticket found only test names.
- Re-runs (verbatim tails):
  - `dry_stub.py --selftest`: `=== dry_stub --selftest: 57/57 ok ===`
  - `selftest.py --lang`: `=== qa-factory selftest: 2/2 ok ===`
  - `test_field_producers.py`: `known red rows 29, not in world rows 47, rows walked 910` / `=== test_field_producers: 921/921 ok ===`
  - `pytest tools/test_workflows.py -q`: `26 passed in 0.67s`
  - the scratchpad probe (F2/F6) as quoted above.
- Not run: CI and the spike (the CI log lines are taken from the report); the big scenario files; the ratchets.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "class_completeness": "Axis 34 covered (stub reaches source_inventory only through ticket_adapter commands; judgment is a data row keyed by ticket key). Axis 17 n/a for package detectors, the outcome/gate lines keep one shape. Axis 18: no ratchet rows touched; clone-ratchet result not attached (forge-check never ran on the branch). Same-artifact sweep: E-R3 validation covers type rows but not row stub overlays (F2); closed_answers words are free text by design (n/a). Clone pair TrackerServer/FakeJira and build_world/rest_project queued as a Lead-opened node (F5).",
  "fixes": [
    "F1 dry_world.py:572-573,594 - numbers verdict only when S3 done AND every row reached its named question AND no snapshot red; else undecided naming the row (before any gate number is counted, N2)",
    "F2 dry_world.py:417,132-137 / dry_stub.py:154 - validate each probe/walk row stub with check_stub before the world is built; a row entry without reason crashes the stub with KeyError (before N1 adds rows)",
    "F3 canon.yml:15,82-84 - spike runs are titled canon <ref> and conclude success, indistinguishable in ci_read pipelines from a green canon; conditional run-name, clock skipped on spike, pin tools/test_workflows.py:273 updated (Lead routes, outside owns)",
    "F4 dry_stub.py:117-121,246-249,269-273 - three script runners and five copies of the exit-text cut; reuse harness.run_script (timeout, no-bytecode) and one cut helper (before N2)",
    "F5 dry_world.py:150-191,237-246 vs test_story_run_s0.py:76-142 - clone pair, one survivor in story_run_common.py as a Lead-opened node; attach a forge-check run of wip/p1b-n0 (clone ratchet) before the PR",
    "F6 dry_world.py:118-129 - require a non-empty from (provenance) in check_stub",
    "F7 dry_world.py:526-529,592 - unused-judgment NOTE also fires for refused keys; spike line says S0..S3 when only S0..S1 ran (queue)",
    "F8 round-3 report Q1/Deviation 2 - six more tickets is not what the CI witness shows (1 pending required, TP1-10937); stop 2 cause is also a dry-world VCS gap (A1-E8)"
  ],
  "trail": {
    "read": [
      "docs/tasks/specs/20261113-p1b-n0-round3-amendment-spec.md",
      "docs/tasks/specs/20261113-p1b-dry-story-spec.md:489,520-545,800-810",
      ".claude/worktrees/p1b-n0/docs/tasks/specs/reports/20261113-p1b-n0-round3-report.md",
      ".claude/worktrees/p1b-n0/docs/tasks/specs/reports/20261113-p1b-n0-report.md:84-111",
      "ai-packages/qa-factory/scripts/tests/dry_stub.py (whole, worktree)",
      "ai-packages/qa-factory/scripts/tests/dry_world.py (whole, worktree)",
      ".github/workflows/canon.yml (HEAD and diff)",
      "scripts/tests/fixtures/form-fill-rules.json, test_field_producers.py, form_filler.py, dry-types.json, probe.json, routes.json, story.json (diff)",
      "references/artifact-contract-plan.md:12-34",
      "scripts/branch_accounting.py:50-80,680-712,732-770",
      "skills/qa-story/phases/s1.md:144-165",
      "scripts/tests/harness.py:232-240",
      "scripts/tests/test_story_run_s0.py:76-142",
      "scripts/tests/story_run_common.py:333-353",
      "fixtures/investigation-14857/TP1-14857/work/source-inventory.json:380-434",
      "docs/SIBLING_MAP.md axes 17,18,34",
      "docs/tasks/critic-diff-brief.md",
      "tools/critic_verdict.schema.json"
    ],
    "reruns": [
      {"command": "(package dir) python -B scripts/tests/dry_stub.py --selftest", "result": "=== dry_stub --selftest: 57/57 ok ==="},
      {"command": "(package dir) python -B scripts/selftest.py --lang", "result": "=== qa-factory selftest: 2/2 ok ==="},
      {"command": "(package dir) python -B scripts/tests/test_field_producers.py", "result": "known red rows 29, not in world rows 47, rows walked 910; 921/921 ok"},
      {"command": "(worktree root) python -m pytest tools/test_workflows.py -q", "result": "26 passed in 0.67s"},
      {"command": "python -B -I scratchpad/probe_row_stub.py <tests dir>", "result": "merged A-1 = {relevance: maybe}; RAISED KeyError 'reason'; type row judgment with no from loads: no error"}
    ]
  }
}
```
