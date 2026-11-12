# t-168 — critic gate on builder diff t-159 (OH3-24, onboarding-forge)

Diff: `git -C C:\QAFactory\forge-repo\.claude\worktrees\oh3-24-docref diff 6915cc0 ed705d8` (commits a5e1200, 097485a, ed705d8; 5 files, +175/-20).
Spec held to: Lead decisions Q-a … Q-e and the test rule from the dispatch.

**Verdict: NEEDS WORK (fit_with_fixes). 2 must, 2 minor.** No reject: the ref normalisation itself is correct, and the fixes are small and local.

## Findings

### M1 (must): a live test goes red. `test_onboarding_notes.py` pins the old p4 text
- Carrier: `scripts/tests/test_onboarding_notes.py:837` expects the literal `` `project_decisions.py --root . add --field-ref /environment/integrations --essence ...` `` in `p4-generate.md`. ed705d8 changed that line to `doc:config.json#/environment/integrations`.
- Re-run (worktree): `python -B scripts/tests/test_onboarding_notes.py` gives `FAIL K-TEXT OH2-6 p4 integrations add has its essence (Q1): present in p4-generate.md`, then `=== onboarding notes: 327/328 ok ===`.
- The file is LIVE, not quarantined (I checked the `quarantine` key of test-layers.json). The batch canon on CI would fail.
- Why the witness missed it: `scenario_walk.py --witness-for skills/qa-onboarding/phases/p4-generate.md` names only test_brief_pack and test_sizing. The `covers` row of test_onboarding_notes.py does not list p4-generate.md, even though the test pins p4 text. That row, as printed by my re-run, is: `config_contract.py, onboarding_notes.py, README.md, agents/qa-test-strategist.md, evals/plugin-eval-benchmark.json, references/automation-candidacy.md, references/templates/factory-backlog.md, tests/harness.py`. So the builder ran the 7b scope as written. Even so, the diff breaks a live test, so the fix belongs to this round.
- Fix: update the K-TEXT row at :837 to the new ref. The new junction check in test_project_decisions_doc_ref_form.py already proves the command is accepted, so the old pin can simply track the text.
- Queue the class gap separately: a text pin whose `covers` row does not name the file it reads. That is SIBLING_MAP axis 7 (per-test identity and the scopes a test depends on). Proposed Остатки line for the Lead: `test_onboarding_notes.py covers row lacks skills/qa-onboarding/phases/p4-generate.md (the file its K-TEXT rows read) -> witness-for misses it | узел: <Lead opens>`.

### M2 (must): the new exit-2 contract says "nothing written", but `resolve` writes before two of its ValueErrors (FR-14, AR-18, FR-4)
- Q-b maps every ValueError of `resolve` to exit 2. The module docstring (lines 10-13) now files it under "2 refused, one stderr line, nothing written".
- In `resolve`, two ValueErrors are raised after `_atomic(receipt_path, …pending…)` and after `_atomic(config_path, …)`: `marker file is absent: …` and `exact marker not found in …`.
- Probe 1, pointer row (scratch project): `add --field-ref x`, then `resolve --id DD-1 --field-values '{"/x":5}' --marker-file qa-factory/nope.md` printed `project_decisions: resolve refused - marker file is absent: …` with `exit=2`. Afterwards config.json held `{"a": 1, "x": 5}` and the receipt `DD-1.json` said `"status": "pending"`.
- Probe 2, doc row, marker text absent from the named file: `exit=2` with a pending receipt.
- Failure scenario: a caller reads exit 2 as "refused, nothing changed, fix and retry". But config.json was already written. Worse, a later `recover`, or a retry with the same arguments, sees `recovering=True`. On that path the marker-not-found check is skipped, so the row closes with no marker removed. The "refusal" quietly turns into a closure.
- The mechanics predate this diff: before it, these two cases exited 1 with a traceback, which promised nothing. Q-b is what relabels them as clean refusals.
- Fix, either way:
  - (a) Preferred. Inside the lock, before the receipt write, check that every marker file exists and (when not recovering) that the token is in it. Then every ValueError of `resolve` really comes before any write, and the docstring is true.
  - (b) Keep these two raises outside the exit-2 mapping (a different exception type, exit 1) and say so in the docstring.
- Either way, add one CLI table row (marker file absent, pointer row) asserting that config.json is byte-equal and no receipt exists.

### m1 (minor, fix in this round): a third copy of the refusal wrapper (brief item 6)
- The new `_refusal_as_line` (project_decisions.py about 872-882) repeats, line for line, the try/except of `_record_stand_fact` (673-685) and the ValueError/TimeoutError arms of `_record_finding` (855-869): `print(f"project_decisions: {action} refused - {exc}")` then `SystemExit(2)`, and `_registry_busy_line` then `SystemExit(2)`.
- Fix: write `_record_stand_fact` as `return _refusal_as_line(action, lambda: …)`. `_record_finding` keeps only its `FindingRecordedEarlier` arm before delegating. If FindingRecordedEarlier is a ValueError subclass, the inner try must stay first.
- That leaves one wrapper for the one action, which is P31/AR-15 inside the very file Q-c made the unit.

### m2 (minor): normalisation does more than the changelog says
- `_doc_ref` now also drops empty segments: `doc:a//b` becomes `doc:a/b` and `doc:a/` becomes `doc:a`. Q-a and the changelog name only `./` and an empty `#`.
- This is harmless and in the safe direction (it only merges spellings of one path). Either add one table row each and a changelog clause, or keep only `.` segments. Not blocking.

## Verdict layer: the questions asked

**Normalisation semantics (refs that passed before and now refuse, and the reverse).** I traced `_doc_ref` and `_refs` old vs new and probed with the table.
- Newly refused: a path with `:` anywhere (`doc:https://x`, `doc:http:x`, `doc:a/b:c.md`; the old `_DRIVE` matched only one letter plus `:`), `doc:.` and `doc:./`. All of these follow Q-a.
- Newly accepted: none. Every input the old code refused still refuses (`..`, a leading `/` or `\`, a drive, empty, `#h` only).
- Stored rows: the only shipped producer of doc refs is `doc:strategy/test-strategy.md#risk-and-impact-scale` (p4:594, CHANGELOG:4920), and it is unchanged by the new normaliser. I grepped the package for `doc:[^ |`"'<)]+`, case-insensitive. No fixture or shipped text carries a `:`-path, a `./` or a trailing `#`.
- A hand-written legacy cell with `doc:https://…` would now refuse every later `add`. It names the row and the cell to correct (the existing k6b_5b door), which is the FR-1/FR-59 direction.
- Legacy `doc:./a.md` or `doc:a.md#` cells now normalise equal to `doc:a.md`. `stored()` therefore reuses them instead of creating a second row, which improves dedup.
- The quarantined table `test_project_decisions_doc_refs.py` still passes: 56/56 on re-run.

**Q-d (p4 integrations as a `doc:` ref).**
- No code reader lifts on a registry row pointing at `/environment/integrations`. I grepped scripts/*.py for `integrations`, case-insensitive: the hits are brief_pack and config_contract, which read config.json and not the registry. Positive control of the same shape: `/profiles` is found as a lift ref in `onboarding_first_reader.py` 119-126.
- So moving the record to a doc ref starves no reader. Resolving it writes nothing into config.json, because doc refs are excluded from `pointers`.
- The `/profiles` row stays a pointer, as Q-d says.

**Q-c (one predicate).**
- `_is_relative_path` is used by both `_doc_ref` and the `resolve` marker check. The old `_DRIVE` regex and the `is_absolute()/parts` test are gone.
- The marker check is now also stricter in a correct way on Windows: `Path("/x.md").is_absolute()` is False there, so `/x.md` and `C:x.md` used to pass.
- The other copies in other files are out of scope and queued, per the Lead.

**Q-e.** Changelog only. Correct.

**FR walk.**
- A: FR-1/FR-2 hold. The doc-ref refusal names the form, what is wrong and the way out, and the test asserts all three. FR-4 is broken by M2: exit 2 is reported for a partially applied write.
- B: no text shown to a person changed beyond the p4 role text. FR-6 does not apply.
- C: FR-11 holds. The p4 command is accepted by `add`, and the new test runs exactly that command taken from the text. FR-14: the exit-code contract is inaccurate for two cases (M2).
- D: FR-58 holds. The table's expectations follow Q-a, not the code's output.
- E: no change.
- F: no change.
- G: FR-30. The test file holds Cyrillic only as `\u` escapes, so the source is ASCII; selftest `--lang` is in the builder's 4/4. FR-32: the tests come with the fix. FR-54: see class completeness.

**AR.**
- AR-9 kept: each refusal names its form.
- AR-13 kept: `_refs` is still the one reader of a field ref.
- AR-18 is partly broken: the output shape is unified, but the exit-2 meaning lies for two cases (M2).
- AR-15 kept inside the file; a third wrapper copy remains (m1).
- AR-22: the producer (p4 text) and its reader (`_refs`) changed in one commit, ed705d8.
- The commits name AR-9/18/15/22/23. AR-13 is not named; it is untouched in meaning.

**JUDGMENT (q11).** None. Shape checks of a typed path only. `judgment: none` holds.

**ONE ROAD (q12).** None found. The add and resolve refusals now take the add-finding road, which removes a divergent road. Grepped: `except ValueError|SystemExit(2)` in project_decisions.py (the m1 copies are found that way). No language, project or case branch was added.

**DUPLICATION AND CONSISTENCY.** m1, the third refusal wrapper. The test table duplicates the quarantined `test_project_decisions_doc_refs.py` K6b-1 and K6b-5 cases. That is legitimate: the DoD forbids writing into quarantined files, and the new file is the surviving table.

**CODE QUALITY.**
- No new function is over 60 lines or over three nesting levels. `_doc_ref` is 14 lines; `_is_relative_path` is 3.
- The module docstring line for exit 1 omits stand-account; that predates the diff.
- The `_refusal_as_line` docstring is accurate.

**Tests (brief item 5).**
- One table file with a keep row (layer `table`; it holds).
- The CLI battery uses a subprocess per case in one world. That is the door for exit codes, so it is acceptable.
- The p4 regex is a producer/reader junction, not a bare pin.
- Missing: no row would catch M2.

**Ratchets (q9).** test-layers.json gains a keep row only, no ratchet raise. I found no change to the census or role-load.

## Class completeness (SIBLING_MAP)
- Axis 7 (per-test identity and scope): open, see M1. The class "a text pin whose covers row omits the file it reads" should be queued as a node.
- Axis 34 (one road): improved, with m1 remaining.
- Axis 21 (markdown cell readers): n/a. `_refs` splits a cell on `,` after the table reader, unchanged.
- Other axes: n/a, since the diff stays inside one script, its test and one phase text.
- The ~22 copies of the relative-path predicate in other files are queued by the Lead (Q-c), so they are not a finding.

## Trail
- Read: the full diff 6915cc0..ed705d8; project_decisions.py 237-290, 297-305, 360-370, 400-545, 670-690, 820-882, 940-960; onboarding_first_reader.py 105-135; test_project_decisions_doc_refs.py 1-80 and 140-210; test_onboarding_notes.py:837 (by grep); test-layers.json (keys, quarantine membership, the new keep row); docs/tasks/critic-diff-brief.md 25-95; SIBLING_MAP.md axis list; commit trailers (architecture/judgment/tier).
- Not read: the OH3-24 node row and its finding file. The dispatch's Q-a…Q-e were taken as the spec.
- Re-runs (worktree, ai-packages/qa-factory as subshell cwd):
  - `test_project_decisions_doc_ref_form.py`: 102/102 ok. This matches the attached witness.
  - `test_project_decisions_doc_refs.py` (quarantined; it judges the same function): 56/56 ok.
  - `test_onboarding_notes.py`: 327/328, one FAIL (M1).
  - `test_conductor_doors.py`: 218/218 ok.
  - `test_guard_write_owners.py`: 537/537 ok.
  - `test_silent_passes.py`: 326/326 ok.
  - `test_test_locations.py`: 456/456 ok.
  - `test_project_knowledge.py` and `test_gate_preflight.py` printed no summary inside my 120 s per-file timeout, so they are not judged here. Neither touches doc refs.
  - `scenario_walk.py --witness-for` on both owned paths, output as quoted under M1.
  - Probes 1 and 2 in the scratchpad, results quoted under M2.
- Witness consistency: the builder's list covers 6 of the 14 tests in the 7b scope. The rest (scenario cart_1, local_1_0108 and arm_b, story_run_refusals) are slow files left to CI by rule. The fast ones I re-ran above.
- The verdict is an input to acceptance. Accepting is the Lead's decision.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "M1: p4-generate.md:296 text change turns live test_onboarding_notes.py:837 K-TEXT red (327/328); batch canon would fail",
    "M2: resolve ValueErrors 'marker file is absent' / 'exact marker not found' are raised after the pending receipt and config.json writes, yet Q-b maps them to exit 2 'refused, nothing written' (probe: exit=2, config gained x:5, receipt pending; a later recover/retry closes the row)"
  ],
  "fixes": [
    "M1: update test_onboarding_notes.py:837 to the doc:config.json#/environment/integrations text",
    "M2: validate marker files exist and hold the token (unless recovering) before the receipt write in resolve, or keep those two raises out of exit 2 and say so in the docstring; add a CLI row asserting config bytes equal and no receipt on that refusal",
    "m1: express _record_stand_fact and the ValueError/TimeoutError arms of _record_finding through _refusal_as_line (one wrapper)",
    "m2: either pin and changelog the empty-segment collapse (doc:a//b, doc:a/) or drop only '.' segments"
  ],
  "class_completeness": "Axis 7 open: test_onboarding_notes.py covers row omits p4-generate.md which its K-TEXT rows read, so witness-for misses it - queue as a node; axis 34 improved, third wrapper copy remains (m1); relative-path predicate copies in other files queued by Lead (Q-c); other axes n/a",
  "trail": {
    "read": [
      "git diff 6915cc0 ed705d8 (worktree oh3-24-docref)",
      "ai-packages/qa-factory/scripts/project_decisions.py 237-290, 297-305, 360-370, 400-545, 670-690, 820-882, 940-960",
      "ai-packages/qa-factory/scripts/onboarding_first_reader.py 105-135",
      "ai-packages/qa-factory/scripts/tests/test_project_decisions_doc_refs.py 1-80, 140-210",
      "ai-packages/qa-factory/scripts/tests/test_onboarding_notes.py:837",
      "ai-packages/qa-factory/scripts/tests/test-layers.json (quarantine membership, new keep row)",
      "docs/tasks/critic-diff-brief.md 25-95",
      "docs/SIBLING_MAP.md axis list"
    ],
    "reruns": [
      {"command": "python -B scripts/tests/test_project_decisions_doc_ref_form.py", "result": "102/102 ok"},
      {"command": "python -B scripts/tests/test_project_decisions_doc_refs.py", "result": "56/56 ok"},
      {"command": "python -B scripts/tests/test_onboarding_notes.py", "result": "327/328, FAIL K-TEXT OH2-6 p4 integrations add has its essence (Q1)"},
      {"command": "python -B scripts/tests/test_conductor_doors.py / test_guard_write_owners.py / test_silent_passes.py / test_test_locations.py", "result": "218/218, 537/537, 326/326, 456/456 ok"},
      {"command": "scratch probe: add --field-ref x; resolve --field-values {\"/x\":5} --marker-file qa-factory/nope.md", "result": "exit=2 'resolve refused - marker file is absent'; config.json now holds x:5; DD-1.json status pending"}
    ]
  }
}
```
