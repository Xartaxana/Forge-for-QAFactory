# t-170 — critic on PLAN: t-167 OH3-9 (the factory settles its own files by class)

Reviewed: `docs/tasks/specs/t-167-oh3-9-factory-files-by-class.md` (forks closed by the Lead 12.11 at the designer's recommendations).
Spec/DoD under review: the spec itself plus the owner's word 22.10.2026 (finding `plans/piles/onboarding-forge/findings/20261022-onbording-sprashivaet-pro-sluzhebnye-fajly-fabriki.md` :5-6).
One pass (R13-g). This verdict is an input to acceptance; acceptance stays with the Lead.

## Verdict: fit_with_fixes. No blocker. 4 must, 8 minor

The design holds: one drift function, deletions only through `_retire`, home membership read from the table, and the outside-home C2 refusal kept as a control. F-1 A, F-4 A and F-5 A are resolved correctly. F-3 A is correct for machine-local factory data, but as written it also reaches one tracked, person-editable row (M1). The spec as written would turn about ten existing assertions red, and it does not decide how to fix them (M2). The closed forks are still conditionals in the body (M3), so a sonnet builder cannot run it without inventing pieces.

## Key 1 — facts by trail (spot-checks)

| claim | check | result |
|---|---|---|
| `benefit-inputs.json` has no writer (NEGATIVE) | `grep -rnil "inputs\.json"` and `grep -rni "benefit-inputs"` over the whole package (py/md/json; CHANGELOG excluded), plus `benefit.inputs\|benefit_inputs\|BENEFIT_` over scripts/ outside tests | holds: hits only in install-paths.json, metrics_projection.py (:509 named, :668 read), test_install_paths.py and test_metrics_contract.py. Positive control, same shape: `grep -rnil "reporter-rehearsals"` found the known writer/readers gate_preflight.py, onboarding_probe.py, report_adapt.py |
| row :112 is regenerated machine-local, reader gate_preflight.py | install-paths.json :112 read | holds |
| carried + machine_local is legal in state/ | install_paths.py :666-679 `_layout_errors` read | holds: only carried non-local in an untracked folder, and machine-local in a tracked one, are refused |
| `_changed_since_summary` has exactly 2 call sites (S-1) | grep over the package's *.py | holds: onboard_apply.py :1442 (apply) and :1882 (main); def :1275 |
| `scan_tree(..., retire_unbuilt=True)` called only by `plan` | grep `retire_unbuilt` in scripts/ outside tests | holds: onboard_apply.py :928 only |
| every §3.3 `rebuilt_by` script contains the row's key | `grep -ciF <key> <script>` for all 12 pairs (install_paths/install-manifest.json, host_probe, stand_lease/stand-, execution_scheduler ×2, exit_gate, native_context, stand_identity, bug_snapshot, project_decisions, story_budget/budget, readiness/jira-direct-probe.json) | all ≥1: the shipped table will validate |
| retire_modes / delete-mode rows | install-paths.json :1-35, :119-123 read | discarded→delete, regenerated_stale→delete; the discarded rows are jira-probe-* (machine_local), qa-factory/readiness.json (machine_local) and **strategy/product-passport.md (NOT machine_local, tracked, requires fold_receipt)**. The last one drives M1 |
| C2 tests to flip: :434-465, K-A5 :1318-1333; the :448 "names no script" row | test_install_retire.py read | holds |
| REGEN_UNBUILT :68-70 holds coverage-map.receipt.json | test_reinstall_equals_fresh.py read | holds |
| census rows install_paths `_shape_errors` (shape) / `validate_table` (xref) | judgment-census.json :420, :423 | holds; there is no row for `_changed_since_summary` today |
| p4 :31-33 refusal sentence; SKILL ## Digest :130-138 | Grep/read | holds |
| SIBLING_MAP :76 is the hook_written row | read | holds |

Not covered by the spec's trail and found here: the synthetic-table assertions in `test_install_paths.py::section_validate` :213-280 (M2).

## Key 2 — forks resolved correctly?

- **F-1 A: correct.** B reclasses about 17 rows, `discard_when` caches would then pile up forever, and that contradicts «не нужны — удаляются». C is a closed list in code (AR-1). The data check is presence plus existence plus containment; the honesty of `rebuilt_by` is judgment, assigned to a tier above. That assignment lacks a registered detector (M4).
- **F-2: closed as recommended.**
  - a (benefit-inputs → carried): correct. Nothing can rebuild it.
  - b (reporter-unread → carried): correct under the owner's word. Its absence costs a rehearsal run (report_adapt.py :218, read). It knowingly overrides B-416's class, and the test docstring at :759-761 must change with it (M3).
  - c (host-probe keep): correct.
  - d (keep): the designer asked the critic whether a story can be mid-run during a reinstall. **It can.** The only refusal is a LIVE writer (apply :1425-1427, `_live_after_waiting`), so a story paused between sessions is reinstalled under with no refusal. The costs of a reset, from the code I read:
    - `budget/<task>.json` is only the warn-once marker (story_budget.py :11-12). Resetting it repeats a warning; the ceiling still reads the price.
    - `.exit_gate_blocks.json` holds the fuse (exit_gate.py :1955-1966). Resetting it makes the gate re-run its checks and possibly block once more. That is stricter, not looser, but it costs one role turn of money.
    - Keeping both regenerated is acceptable, but the declared `rebuilt_by` meaning ("no money") is borderline for exit_gate. See m4.
  - e (coverage receipt → carried): correct. The install runs check_coverage without `--write`.
- **F-3 A: correct in principle, over-broad as written (M1).**
  - The owner's word is literal: «служебные файлы… не нужны — удаляются», and «фабрика не должна спрашивать».
  - FR-3: A reports, it does not ask. So does B. Both comply.
  - FR-40/AR-25: a deletion's way out is the removal record plus `tracking.git_rm`. It cannot be undone, which the class already accepts for listed delete-mode files.
  - The spec's own F-3 cost line bounds A to "the factory's own technical data, and machine-local state". The §4.2 action table keys only on `retire_mode == "delete"`. That also matches `qa-factory/strategy/product-passport.md`: discarded, delete, tracked, not machine-local, a markdown document a person or the fold step edits.
  - Failure scenario: the summary lists the passport (sha S). After the summary, the person or the role edits it (sha S'), and the fold receipt exists. Today C2 refuses ("make the summary again"). Under §4.2, `changed`+`delete` makes the sha "read NOW", and `_retire` deletes the file with the uncommitted edits. That breaks the spec's own E11 invariant ("a person's possible file is never removed unseen").
- **F-4 A: correct.** An undetermined file may be the person's; keeping it with a line asks nothing and loses nothing. A person-named `--also-retire qa-factory/x` given only at apply lands here too (kept, with a line). That is safe.
- **F-5 A: correct.** Code writes the sentence once, and the role relays it. B is the incident's road.

## Key 3 — AR / P / FR

- AR-14: kept. `_retire` stays the one unlink site and the one record writer; the effective list is an in-memory copy and the sealed proposal is untouched.
- AR-15: kept. One `summary_drift` serves both sites.
- AR-21: kept. Every `after_summary` row reaches the Digest bullet.
- AR-22: kept. Both new fields have producer and reader. The benefit-inputs gap has no named owner yet (m6).
- AR-25: kept (§4.3).
- AR-28: kept. A path that does not normalise refuses.
- **AR-29: `_basis_errors` is a data check** (presence of a field, file existence, key containment; census `xref`). It is not judgment. The truth of the claim behind `rebuilt_by` belongs to a tier above, and the gap is where that is enforced (M4). `summary_drift` is also data (prefix from the table, class from `classify`, bytes vs sha).
- AR-1 / axis 34 / P31 (ONE ROAD, brief item 12): home membership comes from `home_of(table)` and nothing else. There is no language, project or case branch. The hook_written and carried skips are data rows, so no second road appears.
- FR-6: the `line` texts must pass human-questions.md; the builder reads it, as the spec says.
- FR-14: `after_summary` "always present" is not met on one return path (m1).

## Key 4 — edges

- Both worlds are named: E6 (table before/after), E7 (older sealed listing), E8 (old manifest).
- Positional invariants §4.4 1-7: traced against apply :1399-1451 and main :1873-1886. The positions and the order are as stated.
- Error direction of `validate_table`: correct (refuse-only). It runs only in tests (every caller found by grep is under scripts/tests), so a false refusal costs a red CI and never a user's install. The spec could say so.
- Missing:
  - the `nothing_to_do` early return (m1);
  - an unreadable listed or new file (m5);
  - and the decision of WHERE `rebuilt_by` is resolved (M2 b).

## Key 5 — executable by a sonnet builder?

Not yet. This fails PROJECT.md team rule 11 on M2 and M3.

## Key 6 — overlap with OF1-2

§5.1 claims disjoint functions. That does not fully hold. OF1-2 item 4 (its finding :28-29, "a shape fix needs no new yes" across p3/p4) will very likely touch `apply`'s hash and approval refusals (:1428-1434), and OH3-9 owns `apply`. What actually protects the overlap is the batch dependency column (OF1-2 depends on OH3-9, batch :68) together with docs/tasks/onboarding-streams-2026-11-12.md :26 (OH3-9 → OF1-2). See m3.

## Findings

### M1 (must) — F-3 deletion is not bounded to machine-local rows
- Surface: the `summary_drift` action table, §4.2.
- Evidence: install-paths.json :123, the product-passport row (no `machine_local`, `retire_mode: delete`, tracked strategy/); the scenario is above.
- Fix: in §4.2, `action = delete` only when `classify(...)["machine_local"]` is true AND `retire_mode == "delete"`. A delete-mode row that is not machine-local and drifted gets `keep` with a line ("kept: changed after the summary; the next summary lists it"). Add one Table B row, `listed-tracked-discarded-changed` → kept, file byte for byte.
- Neighbouring classes walked on the same surface:
  - the `new` kind on the passport: kept by the same rule;
  - `qa-factory/readiness.json`: machine-local, guarded by OLD_READINESS branch :1350;
  - jira-probe-*: machine-local, deleted (intended);
  - regenerated_stale rows: all machine-local in state/ (read :87-119), deleted (intended).

### M2 (must) — the new rule turns existing `section_validate` assertions red, and the spec does not decide the fix
- Evidence: test_install_paths.py :213-280. The fixture `alpha = rule("qa-factory/state/alpha.json", "regenerated")` has no basis, and so do the regenerated rows at :218, :224, :228, :231, :233, :236, :268, :270, :272, :275. Under `regenerated_without_basis`, these assertions break:
  - :219 `(True, [])`;
  - :237 `sibling["ok"] True`;
  - :245 `(False, ["reader_contradicted"])` and :261 `["reader_contradicted"]` (exact code lists);
  - :253-254 `r["ok"]`, :258 `(True, [])`, :273 `ok True`;
  - :269 `["reader_key_absent"]`.
- §5.2 lists only REGENERATED_UNBUILT, Q7 and report_adaptations as flips.
- Fix, stated in the spec:
  - (a) Fixture rows that test other codes carry a basis that adds no code. Recommended: give `rule()`'s regenerated fixtures in section_validate `hook_written: True` (legal shape; there is no regenerate_step in these synthetic tables, so the step-output shape rule cannot fire). Alternative: `rebuilt_by: "reader.py"` where the key is present. Either way the exact code lists stay unchanged.
  - (b) `rebuilt_by` is resolved under `validate_table`'s `package_root` argument and read directly, the way `_reader_path` does for `reader` (install_paths.py ~:759-771). It is NOT looked up in `_corpus`, because `_corpus` excludes this module (G4 row :255: "a mention in … this module is not a reader"). A corpus-based join would refuse row :88 (`rebuilt_by: install_paths.py`), and synthetic packages would never see the plugin's scripts.

### M3 (must) — closed forks are still conditionals in the body
Examples: §5.2 "whatever F-2 reclasses", "flips only if F-2 b is taken"; the test_reinstall line "only if F-2 reclasses"; §5 eval "(… depend on F-3; with F-3 = B …)"; Table B rows prefixed "F-3 A:"; the §3.3 verdict cells "F-2 a/b/e". Fold them into one unconditional list:
- install-paths.json: rows :112, :113, :114 and :116 become carried machine-local and move into the carried block, each with a note. The other rows get `rebuilt_by` as in §3.3.
- test_install_paths.py:
  - REGENERATED_UNBUILT :460-467 loses reporter-rehearsals, benefit-inputs and coverage-map.receipt;
  - the Q7 check :559-562 loses reporter-rehearsals AND benefit-inputs (the spec names only the first). Both go to the carried machine-local check beside :563-565;
  - the :76-81 regenerated loop loses coverage-map.receipt;
  - section_report_adaptations :759-770 flips to carried, docstring included;
  - plus the M2 fixture edits.
- test_reinstall_equals_fresh.py :70: coverage-map.receipt moves to the kept side.
- Eval 16 text: the F-3 A wording only.
- Also fix the numbering: §5 appears twice, and §4.5 sits inside §5.

### M4 (must) — `rebuilt_by` honesty has no registered detector
- §1.2 and F-1's note rest the class rule on "judged by the critic". Rule 3 makes the critic mandatory only for diffs over ~100 lines or on schema/core, so a one-line table edit adding `rebuilt_by` can be accepted with "critic: skipped".
- The instance itself would pass the code check as `rebuilt_by: gate_preflight.py`, which contains the key. F-3 A now deletes such a misclassified file after the summary without any person seeing it. Before this node, the person at least saw it listed or was refused.
- Fix (four questions (c)): name the detector in the spec. Cheapest data option: a shape rule that a `rebuilt_by` row also carries a non-empty `note` stating why its absence costs no run, money or question. This is a presence check, so it stays AR-29-clean, and it leaves a reviewable claim. Then name where it is judged: a critic-diff-brief or calibration line, proposed to the Lead as a node, since it is outside this node's owns.
- Observation (duplication, item 6): in all 11 §3.3 rows `rebuilt_by` equals the existing `reader`. The field's value is the explicit claim, not new data, which is one more reason the claim needs a reviewable carrier.

### Minor
- m1: initialise `"after_summary": []` in the first `out` dict at apply :1410-1411, before the `nothing_to_do` return at :1416 and the `early` path. Otherwise FR-14's "always present" fails on those returns. Owned lines already include "`out` keys"; say WHERE.
- m2: owns ranges are too narrow.
  - The invariant sentence starts at onboard_apply.py line 9 ("Invariant, spec-wide: nothing is retired that is … not in the approved listing…"); widen 10-17 to 9-17.
  - `apply`'s docstring (:1400-1407) still says "a listed path's sha256 differs from the summary (C2)" refuses. Add it.
  - `_retire`'s docstring ("Retire what the sealed listing names") should mention the after-summary rows.
- m3: §5.1 should say the order rests on the dependency column (batch :68) and the streams file :26, and that `apply` is possibly shared with OF1-2 item 4. OF1-2 merges main and re-runs both pins (team rule 3). An `очередь:` line is a between-batch device; inside one batch it is redundant.
- m4: F-2 d stays regenerated. Write the residual cost into the two row notes: a paused story's warn marker and exit-gate fuse reset on reinstall; the cost is one repeated warning or one extra gate run.
- m5: name the edge of an unreadable listed or new file inside the home. `I.sha256_file` is called at the drift point; say "kept, a line", never a crash and never a delete. Today's behaviour is the same, but the new delete branch makes it load-bearing.
- m6: name who files the two analog findings: the AR-22 benefit-inputs producer gap, and the AR-28 silent skip when the coverage receipt is absent on a fresh project, which carried does not cure. Per team rule 2, the Lead files the findings/ file plus the batch row in one move. They are not left as "queued".
- m7: optional home-membership rows `qa-factory./x` and `qa-factory /x` (Windows strips trailing dots and spaces, so the folder IS the home). Today these are treated as outside, which errs toward refusing. Safe; one row would pin the direction.
- m8: §5.5 says "all 31 rows enumerated". The count is not load-bearing; drop it or count from the table.

## Standing questions (critic-diff-brief items 6, 7, 12)
- DUPLICATION AND CONSISTENCY: one finding. `rebuilt_by` repeats `reader` on all 11 rows (M4 note). Otherwise none found. I grepped `_changed_since_summary|summary_drift` (2 sites become 1 function) and `retire-record|RECORD_NAME` (one writer, onboard_apply :1388).
- CODE QUALITY (plan level): the M2 fixture fallout and the M3 conditionals. Otherwise the plan stays inside existing helpers (`classify`, `normalize_rel`, `home_of`, `_retire`).
- ONE ROAD (item 12 / P31): none found. Home from the table; no language, project or case exclusion; one drift function at both sites.

## Class completeness (rule 5, SIBLING_MAP)
- The instance class (an evidence file classed regenerated) was walked over all regenerated rows (§3.3): four reclassed, the rest given a basis.
- The drift class: SIBLING_MAP :76 twin named.
- The remaining sibling surface is the delete-mode rows outside state/ (M1).
- Not walked by the spec, stated as scope: other `onboard_apply` refusals whose door is a person's move (§9 last bullet). That is a scout question for the Lead if wanted, not a blocker here.

## Trail
Read:
- t-167 spec (whole);
- the finding (whole);
- install-paths.json :1-35 and :85-140;
- install_paths.py :89-119, :280-290, :440-530, :555-620, :660-682, plus the validate_table reader loop;
- onboard_apply.py :1-40, :1270-1300, :1330-1520, :1845-1913;
- test_install_paths.py :40-46, :75-85, :205-280, :455-470, :555-567, :755-790;
- test_install_retire.py :432-466, :1316-1334;
- test_reinstall_equals_fresh.py :64-72, :705-726;
- judgment-census.json :415-425 and :578-584;
- report_adapt.py :205-225;
- story_budget.py :1-30;
- exit_gate.py :380-395, :1950-1975;
- batch file :1-14, :28-32, :60-80;
- OF1-2 finding :20-40;
- onboarding-streams file :26 (grep);
- SIBLING_MAP :76;
- the critic verdict schema.

Greps: listed in Key 1. No reruns: this is a plan review, with no mechanical layer to re-run.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "class_completeness": "Regenerated rows walked whole in spec 3.3 (4 reclassed carried, rest given a basis, joins verified by grep for all 12 rebuilt_by pairs); drift twin SIBLING_MAP:76 named; open sibling: delete-mode rows outside state/ (product-passport.md, tracked, not machine-local) reached by F-3 A deletion - M1; analog findings AR-22 benefit-inputs and AR-28 coverage receipt need a named filer - m6.",
  "trail": {
    "read": [
      "docs/tasks/specs/t-167-oh3-9-factory-files-by-class.md",
      "plans/piles/onboarding-forge/findings/20261022-onbording-sprashivaet-pro-sluzhebnye-fajly-fabriki.md",
      "ai-packages/qa-factory/references/install-paths.json:1-35,85-140",
      "ai-packages/qa-factory/scripts/install_paths.py:89-119,280-290,440-530,555-620,660-682,697-770",
      "ai-packages/qa-factory/scripts/onboard_apply.py:1-40,1270-1300,1330-1520,1845-1913",
      "ai-packages/qa-factory/scripts/tests/test_install_paths.py:40-46,75-85,205-280,455-470,555-567,755-790",
      "ai-packages/qa-factory/scripts/tests/test_install_retire.py:432-466,1316-1334",
      "ai-packages/qa-factory/scripts/tests/test_reinstall_equals_fresh.py:64-72,705-726",
      "ai-packages/qa-factory/scripts/tests/fixtures/judgment-census.json:415-425,578-584",
      "ai-packages/qa-factory/scripts/report_adapt.py:205-225",
      "ai-packages/qa-factory/scripts/story_budget.py:1-30",
      "ai-packages/qa-factory/scripts/exit_gate.py:380-395,1950-1975",
      "plans/piles/onboarding-forge/batch-1-onboarding-roles-forge.md:1-14,28-32,60-80",
      "plans/piles/onboarding-forge/findings/20261112-da-cheloveka-nichego-ne-zapisalo-apply-otkazal-predlozheniyu.md:20-40",
      "docs/SIBLING_MAP.md:76",
      "tools/critic_verdict.schema.json"
    ],
    "reruns": [
      {"command": "grep -rnil 'inputs.json' and grep -rni 'benefit-inputs' over ai-packages/qa-factory (CHANGELOG excluded); positive control grep -rnil 'reporter-rehearsals'", "result": "benefit-inputs: only install-paths.json, metrics_projection.py, two tests - no writer; control found gate_preflight.py, onboarding_probe.py, report_adapt.py"},
      {"command": "grep -ciF <key> <rebuilt_by script> for 12 spec 3.3 pairs", "result": "all >= 1"},
      {"command": "grep -rn '_changed_since_summary|summary_drift' and 'retire_unbuilt' over package scripts", "result": "2 call sites (1442, 1882); retire_unbuilt=True only at onboard_apply.py:928"},
      {"command": "grep -n 'validate_table(' over scripts/tests", "result": "synthetic regenerated rows without a basis in test_install_paths.py section_validate 213-280 - M2"}
    ]
  },
  "fixes": [
    "M1: spec 4.2 - delete only when classify machine_local AND retire_mode delete; a non-machine-local delete-mode drift (product-passport.md) is kept with a line; add Table B row listed-tracked-discarded-changed",
    "M2: name the section_validate fixture fallout (test_install_paths.py 213-280) and decide the fixture basis (hook_written True recommended, code lists unchanged); resolve rebuilt_by under validate_table package_root by direct read like _reader_path, never via _corpus (which excludes install_paths.py, row 88)",
    "M3: fold closed forks F-2 a/b/e and F-3 A into unconditional text with the full flip list (Q7 also loses benefit-inputs; loop 76-81 loses coverage receipt; report_adaptations docstring; reinstall_equals_fresh 70; eval 16 text); fix duplicate section numbers",
    "M4: register the detector for rebuilt_by honesty (e.g. shape rule: a rebuilt_by row carries a non-empty note with its no-cost claim; propose a critic-brief or calibration line to the Lead as a node)",
    "m1-m8 as listed in the file (after_summary init before nothing_to_do return; owns ranges for docstrings; OF1-2 order rests on dependency column; F-2 d residual in notes; unreadable-file edge; named filer of analog findings; trailing-dot home rows; drop the 31-row count)"
  ]
}
```
