Critic code review: P1-v N0 check id producer (t-494)

The handoff gate refused the write to C:\QAFactory\forge-repo\docs\tasks\specs\reviews\20261113-p1v-n0-code-critic.md: the original dispatch has no handoff line inside reviews/, and your correction does not count for the gate. So the full verdict is below.

# t-494 critic gate: P1-v N0 (W0), commit 079dc63 on top of 5c16666

**Verdict: ACCEPT WITH FIXES.** No blocking findings. There are two fixes for this round: F1 is the census decision you already took, and F2 is new. There are also two minor fixes and three queue items. This verdict is input to acceptance; the decision is yours.

## Fix in this round

**F1. Census rows for `detector_verdict.py:116` `check_id` and `:132` `with_check`. Your decision is sound, with one condition.**
- Why they are units: they match `UNIT_NAME_RE` (`test_judgment_census.py:69`, the `^check_` and `_check$` patterns).
- The row values are right:
  - Class `shape`, owner `data`. Neither function judges meaning: one reads a field, the other copies a record. This pair is also what 828 of the 1142 census rows use, including the sibling `detector_verdict.py::_refused_of`.
  - Roles `["conductor"]`. The ids travel only on the driver's path; they never block a role and are never shown to one.
- Condition: the census ratchet also holds `blocking_per_role` (conductor 680). If the test computes `blocks` true for either row, that number rises, which is a second raise you did not name.
  - The fix round's witness must show `test_judgment_census.py` green and say whether `blocking_per_role` moved.
  - If it moved, a rename is the better fix (these functions are not checks, e.g. `origin_of` / `stamped`). If it did not, the rows are fine as a named AR-20 raise.

**F2. `driver_dispatch.py:836` reads the `checks:` line on every non-zero exit of `story_step finish`, but only exit 3 writes it.** The only writer is `story_step.py:2054`, reached only through `return 3, _gate_refusal(...)` at `story_step.py:2115`.
- Noise: every exit-2 refusal prints the note "story_step printed no `checks:` line". That includes `_gate_unreadable`, controller refusals and S9 `stage_done refused`. None of these is a gate refusal, so the note misleads.
- Wrong direction: a non-3 output can carry a line that starts with `checks: ` and holds a valid JSON list. It could come from text story_step quotes, or from stderr. That line is removed from the text the conductor reads, and its ids are adopted.
  - This is the error the spec forbids ("NEVER toward naming a check that did not produce the finding", §2 W0).
  - It also breaks §7.13's rule that the text stays byte-identical.
  - I could not establish a live non-3 path that puts such a line at a line start. The surface is outside input, so I am naming the risk, not a proven instance.
- Smallest fix:
  - Call `take_checks_line` only when `code == 3`. For other codes pass `checks=None`, which gives `("unknown",)` and no note.
  - Nothing downstream changes: `RESUMABLE_HEADS` holds only `(exit 3)`.
  - Add one variant row: an exit-2 output containing a `checks: ["x:y"]` line keeps its text whole and reads `unknown`.

## Minor

**M1. The "normalise an id set" step is written three times, in three shapes.**
- `driver_core.py:140/143` builds a tuple and falls back to `("unknown",)`.
- `driver_dispatch.py:3635` (`exit_limit`) builds a list and falls back to `["unknown"]`.
- `driver_runner.py:818` (`run_claude`) does the same as `exit_limit`.
- `tuple(sorted(Refusal.id_counts(errors)))` is also repeated in `handoff_ladder` at `:544`, `:555` and `:585`.
- Fix: one helper next to `id_counts` that all of them use (AR-15).

**M2. `Refusal.checks_n: dict = {}` is a mutable class default** (`driver_core.py:119`). It is only ever reassigned today, so it is not a live bug; `None` plus `or {}` removes the trap.

Also noted, harmless: `own(run_advisers(...))` at `exit_gate.py:1891` and `:1901` is dead code, because `run_advisers` always returns `[]` (`:713`); the spec asked for it.

## Queue candidates (do not widen the node)

- **Q1.** The `gate_unreadable` refusal in `Driver.exit_errors` (`driver_dispatch.py:317-320`) passes `findings=[str(r)...]`. The records' ids are lost and the refusal reads `unknown`. It is not a resume road (`known=False`). The builder listed it too.
- **Q2.** The hook path `exit_gate.main` (`:2057`) adds `text_end_after_handback` records (`:1058`) with no check, outside `all_errors`.
- **Q3.** Controller structured refusals (R-8) read `unknown`; the spec already names this as fork F18.

## Answers by key

**C1, fit to the spec: holds.** I grepped `Record(` in `exit_gate.py`; the hits are 78, 152, 442, 465, 474, 476, 594, 1058 and 1217.
- 78, 465, 474 and 476 carry a check.
- 152 and 594 are summaries, which `judge_words` drops (`:1840`, `:1899`).
- 442 and 1217 are advice, which never blocks.
- 1058 is hook-only (Q2).
- The gate's own producers are covered by `own()` at `:1878-1891`; `form_report` at `:346` and `:355` sets checks.
- `blocking` keeps the same objects through `judge_words` (`:1844`, `:1857`) and `_through_summaries` (`:1776`).
- Positive control: the same grep finds `:78`.

**C2, the carrier survives: holds; the one loss is Q1, which is not a resume road.**
- R-1 and R-2 count from the records at `:550` and `:581`, before they are turned into strings.
- R-5(i): `Refusal(findings=errors)` at `:597` reads the ids before the string conversion at `driver_core.py:160`.
- R-5(ii) uses the `checks:` line; R-7 uses `rec["checks"]`, which survives the JSON round trip.
- `strip`, `+`, `one_line` and `join` all return a plain `str`, but no road reads ids after them.

**C3(2), absent vs zero: holds.**
- `id_counts` never writes 0, and the docstring at `driver_runner.py:803-807` says a missing entry means the count is unknown.
- No key at all means the call was not a refusal resume (R-3, R-9).
- The G1 counting rule (§7.12) reads `checks` only.
- One note for N4: R-7 gives `checks_n {}` on a record written after N0, but `{"unknown": N}` on an older record.

**C3(3), the extras: needed, not scope creep.** The spec's `run_claude` bullet asks for `checks_n`. `id_counts` is the single counter, `CHECKS_LINE_PREFIX` is one spelling shared by writer and reader, and `take_checks_line` keeps `finish` readable.

**C3(4), R-8 `checks=`: right.** The spec's R-8 row and DoD (f) require it; the function list in owns was too narrow.

**C3(5), adversarial lines.**
- On exit 3 it holds. The machine line is last by construction, so the last line wins and an earlier `checks:` line stays in the text.
- These inputs all give `unknown`, a note and the line removed: an empty list, an empty value, a nested object, a number, broken JSON, U+FFFD.
- Non-ASCII ids survive through the JSON escapes.
- A huge value is bounded by the blocking set.
- Non-3 exits: defect F2.

**C4, edges: holds.**
- None or empty gives `("unknown",)`.
- A mixed list is counted per id.
- TEMPORAL, old data read by new code: an old record has no `checks`, so `rec.get` returns None and the refusal reads `unknown` (`:3662`).
- TEMPORAL, new data read by old readers: the new keys are additive. I found no exact-dict comparison of `parse` output outside `detector_verdict.py`.
- A verdict without `labels` is padded with `None`, so its findings read `unlabelled` (`:461`).

**C5, architecture: holds.**
- AR-13: only `check_id` reads `.check`, plus the copy guard inside `with_check`.
- AR-18: there is one record shape.
- AR-22, readers of the new fields:
  - `labels`: `detector_records`.
  - `tag`: `_finding_tag_of`.
  - `rec["checks"]`: `exit_round`.
  - The `checks:` line: `take_checks_line`.
  - The row's `checks`/`checks_n`: no reader yet; awaited by N4 (`run_counters`, G1), as §7.11 declares.
- AR-29 / question 11: no unit judges meaning.
- FR-14 holds. FR-43 and FR-49 are unaffected.

**C6, duplication, quality and tests.**
- Duplication and quality: M1 and M2.
- `test_driver_stop_record.py` is not a new file: git shows it as modified. It has a `test-layers.json` row (`:1409`, layer `detector`, named in SIBLING_MAP:455) and is named in owns.
- The crash in `test_story_step_finish.py:496` is pre-existing. The test regex-searches `story_run.py` for `WINDOW_REASON_LIMIT`, which has 0 hits there on 5c16666; the constant lives in `driver_dispatch.py:920` and `story_step.py:1622`. The diff touches neither `story_run.py` nor the test.

**C7, class completeness:** Q1 to Q3. The SIBLING_MAP axis-17 line is already queued to you by the builder.

**One action, one road (P31): none found.** Every producer reaches the same `check_id`; R-8 reads `unknown` by the named fork.

## Trail

**Read:**
- The spec: §2 W0, §7 and §8 N0.
- The builder's report.
- The full diff of the 7 package files.
- `exit_gate.py` 96-160, 560-713 and 1780-1908.
- At 079dc63: `driver_dispatch.py` 150-190, 285-600 and 790-860; `driver_core.py` 95-175; `driver_runner.py` 812-940; `story_step.py` 1960-2120.
- `test_story_step_finish.py` 485-500, `test-layers.json` around 1409, and the census JSON (ratchet, classes).

**Greps, each with a positive control:**
- `Record(` and `findings=`.
- The `run_claude` fakes: 11 test fakes plus the replay fakes, all taking `**kw`. This confirms the builder's "read, not run" claim.
- Readers of `check`, `tag` and `checks`.
- `WINDOW_REASON_LIMIT` on 5c16666.

**Rerun:** `python -B scripts/tests/test_detector_verdict.py` printed `=== test_detector_verdict: 209/209 ok ===`, the same line as the builder's witness. I ran no slow files.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "fixes": [
    "F1: add census rows for detector_verdict.py::check_id and ::with_check (class shape, owner data, roles [conductor]) as a named AR-20 raise; the witness shows test_judgment_census.py green and states whether blocking_per_role moved; if it moved, rename instead",
    "F2: driver_dispatch.py:836 call take_checks_line only when code == 3 (the one writer's exit code); other codes pass checks=None and print no note; add a variant row: exit-2 output with a checks line keeps its text whole and reads unknown",
    "M1 (minor): one helper for normalising an id set (sorted unique, unknown when empty) used by Refusal, exit_limit, run_claude, handoff_ladder",
    "M2 (minor): Refusal.checks_n class default not a shared mutable dict"
  ],
  "class_completeness": "All exit_gate.all_errors producers and form_report carry a check; summaries and advice never block. Queue candidates outside the node: Driver.exit_errors gate_unreadable Refusal stringifies records (driver_dispatch.py:317-320); exit_gate.main hook path text_end_after_handback records (exit_gate.py:2057); controller structured refusals (R-8, fork F18). SIBLING_MAP axis-17 line queued to the Lead by the builder.",
  "trail": {
    "read": [
      "docs/tasks/specs/20261113-p1v-run-scoreboard-spec.md (2 W0, 7, 8 N0)",
      ".claude/worktrees/p1v-n0/docs/tasks/specs/reports/20261113-p1v-n0-report.md",
      "git diff 5c16666 079dc63 (detector_verdict, exit_gate, story_step, driver_core, driver_dispatch, driver_machine, driver_runner)",
      "exit_gate.py 96-160, 560-713, 1780-1908",
      "driver_dispatch.py 150-190, 285-600, 790-860 at 079dc63",
      "driver_core.py 95-175 at 079dc63",
      "driver_runner.py 812-940 at 079dc63",
      "story_step.py 1960-2120 at 079dc63",
      "tests/test_story_step_finish.py 485-500",
      "tests/test-layers.json around 1409",
      "tests/fixtures/judgment-census.json ratchet and classes"
    ],
    "reruns": [
      {
        "command": "python -B scripts/tests/test_detector_verdict.py (worktree package root)",
        "result": "=== test_detector_verdict: 209/209 ok ==="
      }
    ]
  }
}
```
