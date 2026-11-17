# t-942 — critic, topic "rules debt, phase 1" (S1a-S6, F19)

Spec / DoD: `docs/tasks/specs/20261117-rules-debt-fix-spec.md` §2, S1-S6, §4, §5. Brief: `docs/tasks/critic-diff-brief.md`.
Diffs: `git -C <worktree> diff origin/main...HEAD` for each of the six worktrees. The Lead's decisions I checked against
the journal: t-924 accepted "Lead forks F-L1..13 as recommended" (so moving G14 to "Real limits" is covered by F-L5 (a));
t-929 accepted "R5 stays until S1b (Lead decision b)".

## Verdict

**Topic: accept with fixes (fit_with_fixes). No finding blocks on meaning.** All the fixes are cheap text or commit-message
edits to do before `wave.py merge`.

| stream | verdict |
|---|---|
| S1a t-929 | accept with fixes: F1, F2, F3 (F4 optional) |
| S2 t-930 | accept with fixes: F5 (a `tests-over:` line) |
| S3 t-931 | accept with fixes: F6 (the `architecture:` line overclaims AR-1); W1 residue for S1b, see F7 |
| S4 t-932 | accept; class finding F8 is about other code (the F-O6 node) |
| S5 t-933 | accept with fixes: F9 (a `tests-over:` line), F10 (the guard is written twice) |
| S6 t-934 | accept with fixes: F5 (a `tests-over:` line); the class judgment is confirmed (key 2) |

## Findings

**F1 (S1a, fix before merge)** `design/factory-rules-debt.md:7` says "the two entries that are real limits stand under
'Real limits…'", but that section holds THREE rows (FR-41 R10, FR-13 G14, FR-59 G16; lines 146-158). Item 1 of the spec
requires every number in the header to be true. Fix: "the three entries".

**F2 (S1a, fix before merge; edge E5)** The narrowed X2 row (`:80`) dropped two statements of work that was already fixed:
"01.10: the unresolved-reason words live in ONE place (`contract.UNRESOLVED_REASONS`, t-227 …)" and "the tracker-prefix
list moved to data (`jira-fields.json` `not_tracker_prefixes`, t-267)". Edge E5 / line 7 says moved, never deleted. Fix: keep
both in the row's narrowed head, or add one "Fixed" bullet for them.

**F3 (S1a, fix before merge)** In the six FR-47 bullets moved to "Fixed" (`:152-157`), the text was stitched together without
a sentence break, e.g. "…`judgment-census.json` Cost it carried: …" and "…the census row is B4's Cost it carried: …". Fix: a
". " before "Cost it carried" in each of the six.

**F4 (S1a, optional now)** R5 (`:25`) still says "`story_run.delivery()` … has no state for 'nothing goes out'". The "Fixed"
FR-53 bullet in the same file now says the opposite, and origin/main has both null outcomes:
`driver_stage_s8s9.py:370-379` `nothing_outward` and `:315/:324` `declined_by_person`. Keeping the row is right, because
K0.15's positive control counts at least 2 `| … FR-23` lines (`test_null_outcomes.py:595-596`, which I read). But the
builder's option (b), which the Lead's note names, included a short in-row note: "closed in code (…); line kept until
S1b moves the K0.15 control". That note keeps the interim file from contradicting itself, and the line filter still matches.

**F5 (S2 and S6; rule 20)** Neither commit has a `tests-over:` line, although the hook warned. S2 adds 5 test lines and 0
product lines (`79e2b7d6`). S6 adds 2 lines, all in the fixture, which `tools/test_volume.py` counts as tests (`bef777a7`).
Both reasons hold: S2 fixes a defect that lives inside the test itself (FR-31), and S6 relabels one census fixture row with no
test logic. S6's report even writes the line, but not in the commit. Fix: add the line to each commit message before the merge.

**F6 (S3, fix before merge)** The commit line says "AR-1 -- the level words are a data row read from
contract.PLAN_LEVELS". `contract.PLAN_LEVELS` (`contract.py:2175`) is a tuple in code, not a data row, so that name is false.
What the diff really keeps is AR-13: one owner, and two copies removed. Fix: "AR-1 -- kept, not advanced: the set is still one
list in code (contract.PLAN_LEVELS); AR-13 -- …".

**F7 (S3 → S1b, a remark for the Lead)** The W1 row (FR-13) names `references/vocabularies.md:89` as the vocabulary's owner.
FR-13 reads "Closed variety lives in data files, never in code". After S3 the level set has one home, but that home is code,
and `contract.py:594` `TRACE_LEVELS` spells the same five words again (a spec non-goal). The row's own complaint ("a second
copy that disagrees") is closed. The letter of FR-13 is not. When S1b moves W1, it should narrow the row to "residue: the
Level vocabulary is a code tuple (`contract.PLAN_LEVELS`; `TRACE_LEVELS` :594 re-spells it)", not close it whole. The other
option is a written Lead decision that one code owner satisfies FR-13 for this set.

**F8 (S4, class completeness; about other code; not a fix for S4)** The S4 diff is right, and it matches the charter
(`agents/qa-bug-reporter.md:57`) and `brief_pack.py:298` byte for byte. The spec's sibling list for the "home of a bug file"
class (common-rules + 11 slices, the `bug_records.py:10` docstring, the dashboard) misses these:
- `scripts/judge_results.py:273-279,327` `_project_bugs_dir` reads ONLY `<project>/qa-factory/bugs` for the `--bugs`
  duplicate check. Since OH5-9 the reporter writes `<task root>/bugs/`, so this check never sees those bugs. That disproves
  the spec's §6 F-O6 premise "readers read both", and under option (a) the gap becomes permanent.
- `references/external-writes.md:44`: "a bug always gets `qa-factory/bugs/BUG-n.md`" (read by role slices through
  `common-rules.md`).
- `references/templates/test-report.md:35` and its copy `scripts/form_selftest.py:245`: "BUG-n — a bug file in
  `qa-factory/bugs/`".
Proposed: the node for F-O6 (a) owns these four sites as well as common-rules and its slices. Owner: the Lead opens the node
in an untaken batch. No SIBLING_MAP axis covers the bug-file homes. Axis 8 covers only the draft folder. The Lead may want a
new axis for "bug file homes: writer <-> readers".

**F9 (S5; rule 20)** Commit `60726fc0` adds 14 test lines and 8 product lines, with no `tests-over:` line. The handoff does not
mention this, and the Lead's list does not name it. A reason that holds is available: spec E1 asks for rows AT and BEYOND
400. Fix: the line in the commit message.

**F10 (S5, fix before merge; code quality, small)** The empty/absent case is guarded twice. `collect_failed_note` returns ""
on an empty error (`run_suite.py:1789-1790`), but its only caller is already guarded by
`if checked.get("collect_error"):` (`:1856`). So in production the helper's branch is dead, and two of the five new rows pin
that dead branch. Fix: keep ONE guard. Either the caller appends the helper's result only when it is non-empty (no `if` on
`collect_error`), or the helper drops its guard along with the empty/None rows. E2 behaviour (no note) stays the same either way.

## Keys

**1. Fit to the spec.**
- S1a does items 1-6. Rows moved: R8, R11, X5, X6, X8, X12-X15, X17, X18. Narrowed: X2, X3, X11. "Real limits": R10, G16, plus
  G14 (covered by F-L5). Fixed: the W2 number 221 (plus "353 today"), N1 55, the R3 wording, and FR-59 now says fourteen gates
  with the `environment_property_cover` row. G1-G13 now name their branches. P1 and X11 carry their nodes. No S2-S6 row moved
  (E6). The open count, 37 = 8+3+9+15+1+1, matches the tables after the edit.
  - Spot-checks against origin/main, all hold: R8 (`readiness.py:958-960`, `driver_s0.py:2367-2369`, `gate_brief.py:4968-4977`);
    R11 (`story_run.py:105`); X5 (`driver_stage_s8s9.py:342-379`); X6 (`factory-rules.md:498-503`); X8
    (`guard_pre_tool.py:1302-1312`); X3 (`driver_runner.py:845`, `:606-607`); X11 (`driver_dialog.py:61-70`); X2
    (`manifest_from_tests.py:347-352,1629`, `s5_precheck.py:1661`). For `cost_capture.py`, a case-insensitive grep for
    "testproject" found only the comment at :568. N1 (`audit_factory.py:1716` = 55); W2 (`controller-blocks.md:3` = 353,
    `:21` = 221); R6 (`len(null-outcomes.json pending)` = 52).
  - The 14 `debt` rows of the registry, with their branches (a script over `gate-registry.json`), equal the G1-G13 texts and
    the new row exactly.
- S2: the bound is the spec's, word for word; `queued_behind` and `took_over` are untouched. I read the sibling at :386: the
  holder is alive and never killed, and `[5,2]` is deterministic, so "not applicable" is right.
- S3 does items 1 and 2 exactly. E1: no import cycle, and `contract` reads no file at import (I read the top-level
  assignments). E2 and E4 hold.
- S4 changes one phrase and nothing else; E1 holds (`no_trace` lines are untouched).
- S5: the note is spec E1/E2 verbatim. The added helper is a new module function next to `verify_node_ids`. It adds to the
  function-disjoint seam with GW1-36 and reorders nothing.
- S6 does exactly row :1187 and the ratchet. I re-ran the census: `meaning-proxy=7; breach=0; census breaches: none`, and C3
  is dense, so this was the one `breach` row.

**2. Meaning.**
- S3: control run in the worktree. The old and new sets are equal (`ce equal True`, `pc equal True`). Membership is the same
  for the six words, for `manual-agent`/`manual-human` (refused), `E2E-UI` and `""`. The refusal text `sorted(LEVELS)` is
  unchanged. Side cost: 11 CLI scripts that never imported `contract` now do. Measured: profile_contract cold import with
  `-B` went from about 0.1 s to 0.40 s. Role sessions run with `PYTHONDONTWRITEBYTECODE=1` (`driver_core.py:531`). No hook
  imports profile_contract or candidate_evidence (I checked importtime for every script in `hooks.json`; positive control:
  `exit_gate` and `validate_artifacts` show `contract`). This is wall time only, not LLM spend; I record it, it is not a finding.
- S6: I read `check_behaviour_claims` (`validate_artifacts.py:690-718`) and `contract.claim_required_requirements`,
  `implementation_only`, `code_sourced_requirements`, `claim_row_errors`, `_claim_link_errors` and `before_now_errors` at
  origin/main.
  - Which R owes a claim is computed from typed markers the role chose: `source: derived`, an empty `ac_ref`, an `observable`
    prefix `diff:`/`current-code:`, a `derived_from` prefix `test:`, and matrix cells `silent`/`n/a:*`.
  - The row checks are presence, closed forms (`origin`, `differs`, `before_ref`, `absent`/`unknown`) and joins to
    requirements-readiness.json and the snapshot ids. No free wording is compared against a list.
  - Class `xref`, owner `data` is right under AR-29, and it matches the X7-5 precedent (`check_bug_form`). The census reads
    the class from the row (E1 does not fire). `judgment: none -- …` is the only form `architecture_gate.py` offers for a
    relabel (`:34-38`), and the reason it gives is true.
- S2: a lease that never waited (`waited_s` = 0) or waited a non-multiple of the poll fails the check. Past 1800 the lease
  raises `StandBusy` (red). The check no longer catches a slow takeover inside the limit (for example 1795), which is what the
  spec chose. The flake's cause is still only "suspect" in the row, so S1b moves R7 on the batch canon, not on this witness.
- S5: the note says "not verified" first and states no fact about the ids (FR-41/FR-59). The run decision and exit codes are
  unchanged.

**3. Package rules.**
- Each commit's `architecture:` and `judgment:` lines are present and in a form the gate accepts. Only F6 says something false.
- FR walks: I verified S3's negative "B no text changed" (same set, so the same refusal text), S4's "A, C, D, F not touched"
  and S5's "A untouched" (no exit or refusal changed).
- FR-30 / FR-29: added package lines have 0 Cyrillic and 0 control bytes in all six diffs (positive control: a planted "ж"
  counted 1). `git diff --check` is clean in all six.

**4. Class-wide completeness.**
- S3: a third copy? I grepped `"e2e-ui"` with single and double quotes, and the set shapes, over scripts and references.
  Positive control: the same call found `contract.py:594/2175`. No set copy is left except `TRACE_LEVELS` (F7). The level-keyed
  maps in `manual-policy-by-level.json` and `surfaces.json` are data.
- S4: F8.
- S5: the other notes of the class, `run_suite.py:1674,1743,1753,1847` and `node_ids.py:740,750`, already say "not
  verified". Nothing reads the prefix (grep over scripts, references and agents). So the six literal spellings of the prefix
  are only a duplication remark about other code, not a defect.
- S1a: axis 4 says "a gate's debt row and its backlog row move together" (B-278, `collected_ids`). That applies at S1b, when
  G4 moves.

**5. Tests, duplication, quality.**
- S2: the check is rewritten in place, it is the right layer, and it can still fail (key 2).
- S5: the rows can catch the wording at the helper. The call site is not driven by any non-quarantined test: the only check
  through the door is quarantined M-B1 (`test_run_suite_mine.py:1692`), and its needle "collect failed: banner" passes both
  before and after. That is a missing pin, so not a finding.
- S3, S4, S6: no new test, per the spec. S6's keep row is `register`.
- Duplication:
  - S3 removes two copies.
  - S4 adds one more literal spelling of the charter's path. The line "AR-13 -- read from the charter" is loose, but this is
    prompt text.
  - S5: F10.
  - I found nothing duplicated in S1a or S6. I grepped the other homes of each touched fact: `"e2e-ui"`, "qa-factory/bugs",
    "ids were not verified", "collect failed", and `check_behaviour_claims` in `told-ratchet.json` and `stage-joints.json`
    (both name only the function).
- No new function is over 60 lines or nested deeper than 3 levels.

**Ratchets (question 9).** `judgment-census.json` `ratchet`: `meaning-proxy` 8→7 and `breach` 1→0, both lowered. Nothing was
raised anywhere.

**One road (question 12).**
- S4 sits on the open two-roads fork F-O6, which waits on the owner and is named in the spec. F8 adds the reader that only
  takes one road.
- None found in S1a, S2, S3, S5 or S6. I grepped the diffs for language, runner or project names and new branches: none.
  S3's exclusion of manual levels is a condition of the task (a manual level has no test file), not a second road.

## Trail

Read:
- the spec (whole), the brief, and the six handoffs;
- all six diffs;
- the debt file after the edit (lines 1-175);
- `test_null_outcomes.py:585-600`, `test_stand_lease.py:21-40,280-394`, `test_node_ids.py` (grep), `run_suite.py` (grep and
  1784-1860);
- `candidate_evidence.py:1-48`, `profile_contract.py` (the uses of LEVELS);
- `contract.py` (top-level imports and assignments, 1289-1330, 1422-1545, 691-713);
- `validate_artifacts.py:690-718`, `test_judgment_census.py` (grep), `tools/architecture_gate.py` (the judgment forms),
  `tools/test_volume.py:1-60`, TESTING.md «Бюджет»;
- `judge_results.py:268-292`, `external-writes.md:40-48`, `qa-bug-reporter.md:55-58`, `brief_pack.py:296-300`;
- the origin/main carriers listed in key 1, `SIBLING_MAP.md` axis 4 and the axis 8 bug-drafts row, and journal lines
  2282-2319.

Re-runs:
- `( cd <S6 wt> && python -B ai-packages/qa-factory/scripts/tests/test_judgment_census.py )` printed
  `census: … meaning-proxy=7 … breach=0 …`, `census breaches: none`, `=== judgment_census: 25/25 ok ===`.
- The S3 set-equality control (output in key 2).
- Cyrillic, control-byte and whitespace scans of the six diffs: 0 in each.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "class_completeness": "S3: no set copy left besides contract.TRACE_LEVELS (spec non-goal; F7 asks S1b to narrow W1, not close it). S5: every other not-verified note of the class already says so. S4: the spec's sibling list for the bug-file home misses judge_results.py:273-279,327 (reads only the project home, so the dup check misses task-root bugs), external-writes.md:44, templates/test-report.md:35 and form_selftest.py:245. Proposed: the F-O6 node owns them; no SIBLING_MAP axis covers bug-file homes. S1a: axis 4 (debt row and backlog row move together) applies at S1b.",
  "trail": {
    "read": [
      "docs/tasks/specs/20261117-rules-debt-fix-spec.md",
      "docs/tasks/critic-diff-brief.md",
      "six worktree diffs origin/main...HEAD and handoffs t-929..t-934",
      "ai-packages/qa-factory/design/factory-rules-debt.md (worktree S1a)",
      "ai-packages/qa-factory/scripts/tests/test_null_outcomes.py:585-600",
      "ai-packages/qa-factory/scripts/tests/test_stand_lease.py:21-40,280-394",
      "ai-packages/qa-factory/scripts/run_suite.py:1784-1860",
      "ai-packages/qa-factory/scripts/candidate_evidence.py:1-48",
      "ai-packages/qa-factory/scripts/contract.py:691-713,1289-1330,1422-1545",
      "ai-packages/qa-factory/scripts/validate_artifacts.py:690-718",
      "ai-packages/qa-factory/scripts/judge_results.py:268-292",
      "ai-packages/qa-factory/references/external-writes.md:40-48",
      "tools/architecture_gate.py judgment forms",
      "tools/test_volume.py:1-60",
      "docs/TESTING.md Budget section",
      "docs/SIBLING_MAP.md axis 4, axis 8",
      "origin/main carriers: readiness.py, driver_s0.py, gate_brief.py, story_run.py, driver_stage_s8s9.py, guard_pre_tool.py, driver_runner.py, driver_dialog.py, manifest_from_tests.py, s5_precheck.py, audit_factory.py, controller-blocks.md, factory-rules.md, gate-registry.json, null-outcomes.json"
    ],
    "reruns": [
      {"command": "python -B ai-packages/qa-factory/scripts/tests/test_judgment_census.py (S6 worktree)", "result": "census breaches: none; meaning-proxy=7 breach=0; 25/25 ok"},
      {"command": "python -B -c set equality of candidate_evidence.EXECUTION_BOUNDARIES and profile_contract.LEVELS vs the old literals (S3 worktree)", "result": "ce equal True, pc equal True; manual-agent/manual-human/E2E-UI/empty refused by both"},
      {"command": "Cyrillic/control-byte scan and git diff --check over added package lines of the six diffs", "result": "0 / 0 / 0 in each; positive control counted 1"}
    ]
  },
  "fixes": [
    "S1a design/factory-rules-debt.md:7 - 'the two entries' -> 'the three entries' (R10, G14, G16)",
    "S1a design/factory-rules-debt.md:80 - restore the dropped closures (contract.UNRESOLVED_REASONS t-227; jira-fields not_tracker_prefixes t-267) in the row or as a Fixed bullet (E5)",
    "S1a design/factory-rules-debt.md:152-157 - sentence break before 'Cost it carried' in the six moved bullets",
    "S1a (optional) design/factory-rules-debt.md:25 - in-row note that R5 is closed in code and kept until S1b moves the K0.15 control",
    "S2 commit 79e2b7d6 and S6 commit bef777a7 - add the tests-over line with the reasons (FR-31 defect inside the test; census fixture relabel)",
    "S3 commit c687aee3 - architecture line: AR-1 is kept, not advanced (the set is still a code tuple); the change is AR-13",
    "S5 commit 60726fc0 - add a tests-over line (spec E1 rows AT/BEYOND 400)",
    "S5 run_suite.py:1789-1790 and :1856 - one guard for empty collect_error, not two; drop the rows that pin the dead branch if the helper's guard goes"
  ]
}
```
