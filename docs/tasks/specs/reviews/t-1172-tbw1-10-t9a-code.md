# t-1172 — code critic, card T9a (TBW1-10): controller role-resumed units

Branch `worktree-agent-aec234043a06ad25c`, commits e28cc6f5 (builder t-1158) + acc41b8f (census, Lead, t-1163); diff
`origin/main...HEAD` 90+/22-, 4 files. Spec: `docs/tasks/specs/20261117-told-before-work-finish-spec.md` card T9a (:424-445),
row :47, ids :93, §1 census relabels :113-116; mech `20261113-told-before-work-mechanism-spec.md` :402 (T9a item (a)) and §5.3a (:514-523).

**Verdict: NEEDS WORK — 0 blocking findings, 5 fixes before merge** (the decision is the Lead's, rule 6).

Worst finding: the `_s3_completion_gate` relabel drops `conductor`, but 3 of the unit's 4 raise sites still go to the
conductor (measured with `match_known`). So "net zero" is not true: the honest move is qa-test-strategist 121 -> 122 with
conductor staying at 748, not 748 -> 747.

## Answers to the Lead's two questions

**(1) Census: the label, the named raise, and the judgment line.**
- The raise itself is allowed and named correctly. Mech :402 T9a item (a) says "relabel to the dispatch's roles with a
  `note`, `blocking_per_role` raises named". The census check run on the branch shows qa-test-strategist = 122 (dense,
  no C1-C6 problems).
- "Net zero" does not hold (F1). Road (b) brings back the strategist only for the `S3 structured test plan invalid:`
  site. The labelling-close raise (controller.py :7697-7699), `raise ValueError("structured test plan rows must be a
  list")` (:7706) and the grounding-only raise (:7729) carry no REPAIR_MARKER, no PERSON_MARKER and no KNOWN_REFUSALS
  row, so `route_known` sends them to the conductor. The spec says the same: in mech §5.3a, `s3_window1_close` and
  `s3_grounding` get a row "only if M7 finds a road", and the card's non-goal says ":7479/:7515 (M7 found no road:
  declared gap (4))". The unit therefore stands on both paths: `["qa-test-strategist", "conductor"]`. Taking conductor
  off lowers a shrink-only ceiling below the reach it really has. That is the unsafe direction: it leaves room for a
  later conductor unit to come in unseen.
- The `judgment: adds data check controller.py::_s3_completion_gate -- ...` line. The gate accepts four heads (none /
  adds data check / moves to role / moves to code), and a `blocking_per_role` raise takes only `adds` or `moves ... to
  code` (architecture_gate.py :41-56, :303-308). `moves to code` would be false. `adds data check` is true from the
  strategist's side: one blocking data-check unit is added to its reach. So the head is the only honest door the gate
  offers. The reason after the dashes is the inaccurate part (F4). "presence of the S3 artifacts" is wrong: the unit
  checks the plan contract (`planning_contract.validate_plan`), the grounding lines and the labelling close. "the unit
  moved between roles" becomes false once F1 is fixed.
- Proposal for the tier above, not a finding against this diff: the gate has no head for a pure reach relabel (for
  example `judgment: relabels <unit> reach -- <why>`). Every census relabel that raises a `blocking_per_role` ceiling
  will hit the same forced wording. The Lead decides whether to open a node (a mechanism change, `tier: opus`).

**(2) "The sixth id left unsited": the premise is wrong.** All six ids have a literal site in the diff:
`s3_plan` :7728, `s5_plan_accept` :6995, `s5_plan_gaps` :7001, `s5_plan_review` :7079/:7081/:7087,
`code_review_receipts` :6595, `s5_plan_gaps.rework_rows` :7037/:7042/:7058. I measured unsited on the branch with
`stage_joints._direction_a(rows, universe(), sited_ids(...))`: 11 rows, all `first_look:put.*`, none `controller:*`. So
17 -> 11 = -6 matches the card's counter "unsited -6". The builder's line "5 of 6 ids sited" contradicts its own
"17 -> 11" (N1). What was really left is the census row the card asked for `_code_review_refusal`. The builder's
reason holds: `_code_review_refusal` has no census unit. `UNIT_NAME_RE` (test_judgment_census.py:77) does not match the
`_refusal` suffix, and the function returns a list (the list transport never creates a unit). The census probe prints
`_code_review_refusal False`, and C1 would refuse a row that has no unit. But the reach did not reach the unit that does
carry it (F2).

## Findings

**F1 — fix before merge (census accuracy, AR-20/AR-29, axis 18).**
`judgment-census.json` row `_s3_completion_gate`, roles `["qa-test-strategist"]`.
- Evidence, measured: `driver_machine.match_known` returns `None` (conductor) for the labelling-close text, the
  grounding-only text (with its waiver door) and the rows-not-list text. It returns `('structured_artifact',
  'resume_structured')` only for `S3 structured test plan invalid:`.
- Fix:
  - roles `["qa-test-strategist", "conductor"]`, with the note rewritten;
  - ratchet `qa-test-strategist: 122`, `conductor: 748` (back to the old value);
  - the named raise becomes "qa-test-strategist 121 -> 122, conductor unchanged".
- The same reasoning applies to two non-blocking siblings in this diff, with no ratchet effect.
  - `_plan_rework_rows_problems` :7037: the `except SP.PlanUnreadable: return [..., str(exc)]` text has no marker, so
    `match_known` sends "work/s5-plan.json cannot be read ..." to the conductor (measured: `None`).
  - `_plan_review_problems` :7073: the same branch.
  - Both units should be `[<dispatch role>, "conductor"]`, or the report names why the conductor's reach is ignored.
- `_s5_plan_accept_problems` stays correct: both of its own sites end with `end` (REPAIR_MARKER).

**F2 — fix before merge (card T9a (a), census).**
The receipts refusal's census unit is `_code_review_problems` (census row :189, `["conductor"]`, xref, non-blocking).
Its only caller is `_code_review_refusal` (controller.py :6586, grep over `scripts/*.py`, tests excluded; positive
control: the same grep found the :7776 def and the brief_pack.py:788 prose). That caller returns problems only for
`role == "qa-code-critic"`, and its text carries REPAIR_MARKER. The card's "add it, named" is met by relabeling this
unit to `["qa-code-critic"]` with a `note`. It has no ratchet effect because the unit is non-blocking. The owns list
names functions, so the Lead widens it by one census row, or the report names why not.

**F3 — fix before merge (Q5 (f), `docs/TESTING.md` «Бюджет / Объём»).**
By `tools/test_volume.py`'s segment rule the diff adds +66 test lines (61 test_controller_doors + 5 fixture) against
+23 product lines (changelog.d excluded). Neither commit carries `tests-over:`, and the given material names no reason.
In my judgment a reason holds: one table row per unit as card (c) asks, five units, one shared world, two rows needing
stubs of `s5_plan`. It still has to be named: a report line plus `tests-over:` on the fix-round commit.

**F4 — fix before merge (commit text, Q11).**
acc41b8f's judgment reason mis-describes the unit (see question (1)). The fix-round commit carries an accurate line,
for example `judgment: adds data check controller.py::_s3_completion_gate -- an existing shape check of the S3 plan
contract, grounding and labelling close; its reach now names the strategist beside the conductor; no check added or
moved`. A history rewrite is not needed.

**F5 — fix before merge (Q4, the residual leaves only as a line with an executor).**
The dispatch's sibling decision "EC-8 rows left to T1r-cards-R" has no carrier yet. The T1r-cards-R inputs in the spec
(:676-695) hold no T9a line. These bare or over-told sites inside the owned functions must be written into T1r-cards-R's
input or «Остатки» as `<what> | узел: <id>`:
- `_plan_review_problems` :7073 (PlanUnreadable) and :7075 (the review cannot be read): bare, and the `s5_plan_review`
  sentence does not claim readability;
- the narrow-look refusal :7104-7108: bare, and no sentence covers it;
- `_plan_rework_rows_problems` :7037: sited with `rework_rows`, but `SP.reviews` also raises PlanUnreadable for a story
  state or `dispatches` that is not a mapping (s5_plan.py :282/:286), and the row's door "keep the rework to those
  rows" is no door for that refusal (FR-2 over-tell, EC-8 class).
- Not in this list: `_s3_completion_gate`'s labelling/grounding raises. They are the card's non-goal (M7 declared gap
  (4)), so they are n/a here.

**N1 — report claim corrected, no code change.** "5 of 6 ids sited" is false; it should read 6 of 6 (measured above). A
load-bearing claim of the report that the critic could not reproduce goes to the Lead (rule 12).

**Integrator note (not this node's owns).** `told_ratchet.unsited` is stored as 17 and measured at 11.
`test_stage_joints.py` pins the count exactly (EC-3), so the canon stays red until the wave integrator lowers it to 11
(AR-14, F-1).

## Standing questions (critic.md rule 22)
- **Q1 fit:** sites (b) are met for all 6 ids. The raised text is byte-identical: I read every wrapped hunk; only
  indentation and the `DV.refusal(` wrapper change, and string concatenation keeps its order. REPAIR_MARKER is kept.
  E-T9a-1 holds: Record is a `str` subclass (detector_verdict.py:95), and `match_known` still resumes `S3 structured ...
  invalid`. The sites are counted (-6). (a) has gaps: F1, F2. (c) has a row per unit. `controller-blocks.md` is
  unchanged (regenerated to scratch: identical).
- **Q2 builder decisions:** the reading "no census unit for `_code_review_refusal`" is right (verified); F2 is the
  missing next step.
- **Q3 seams:** `origin/main` has not touched controller.py, the census, stage-joints.json or test_controller_doors.py
  since the merge base 2b2d0f17 (diff --stat empty). T9c (TBW1-11) is in the base, so E-T9a-3 order holds.
- **Q4 class:** F1 siblings, F2, F5. Axis 18 (ratchet raise named row by row): qa-test-strategist 121 -> 122 (road-(b)
  relabel, mech :402 (a)); conductor 748 -> 747 is wrong per F1 and should stay 748. Axis 32: no class changed, no
  `blocks_override`, no scan constant edited.
- **Q5 tests:**
  - (a) killing power: yes. Each row asserts the id per problem and that `expected` rides on the Record; dropping the
    wrapper turns it red.
  - (b) expected values: the ids come from spec :93; the texts are the pre-diff literals, a byte-identity invariant.
  - (c) a row per unit is present. The `rework-rows` row reaches only the PlanUnreadable branch; the other two sites are
    covered by reading. Acceptable: one row per unit is what the card asks.
  - (e) no duplicate row.
  - (f) F3.
  - (g) no new file.
- **Q6 DUPLICATION AND CONSISTENCY:** no second implementation. All 37 `DV.refusal("controller:` sites go through the
  one constructor (grep: 11 distinct ids). No `refusal("controller:` outside controller.py (grep of `scripts/*.py`,
  tests excluded; positive control: the same pattern found the controller.py sites). Two identical `except
  SP.PlanUnreadable` branches are treated differently (:7037 sited, :7073 bare). That follows the two rows' sentences
  and is acceptable, but the over-tell goes into F5.
- **Q7 CODE QUALITY:** none found. The new test function is ~57 lines, nesting <= 3, and its stubs of `s5_plan` are
  restored in `finally`. The controller hunks are wrappers only. Severity: none.
- **Q8 hygiene:** the changelog fragment is English; no Cyrillic in the package hunks (read).
- **Q9 ratchets:** see Q4. `blocking_per_role` is the only key moved.
- **Q10 ARCHITECTURE:** AR-9, AR-10, AR-13 and AR-29 are named in e28cc6f5. AR-20 is named in acc41b8f, and its "net
  zero" is wrong per F1. AR-13 holds: ids are read only via `DV.refusal` -> `stage_joints.row_for`.
- **Q11 JUDGMENT:** no judgment is moved; the judgment wording is F4.
- **Q12 ONE ROAD:** none found. The diff has no language, runner or project branch (read all hunks); every site uses
  the one `DV.refusal` road.

## Trail
- Read: card T9a and its spec rows (:40-125, :415-445, :676-700); mech spec :402, :514-523, :760-775;
  critic.md :178-280; `git diff origin/main...HEAD` (whole); controller.py :5925-5996, :6575-6600, :6983-7125,
  :7683-7735; stage-joints.json :2780-2940; stage_joints.py :761-786, :1105-1170; test_judgment_census.py :77-87,
  :218-300, :498-512; driver_machine.py :44-66, :442-480; driver_dispatch.py :36-110; detector_verdict.py :95,
  :149-233; s5_plan.py PlanUnreadable raises; architecture_gate.py :34-62, :245-310; TESTING.md «Бюджет»;
  test_volume.py :1-30; SIBLING_MAP axes 18, 32; both commit messages.
- Re-runs:
  - `( cd <wt>/ai-packages/qa-factory && python -B scripts/tests/test_controller_doors.py )` gave `=== test_controller_doors: 83/83 ok ===`.
  - Census probe (scratchpad census.py, `T._real()` on the worktree package) gave
    `problems: {}`; totals `qa-test-strategist: 122 ... conductor: 747`; `_code_review_refusal False None`;
    `_s3_completion_gate True (True, ['u3'])`; `_s5_plan_accept_problems / _plan_rework_rows_problems /
    _plan_review_problems True (False, ['u1'])`.
  - Unsited probe (scratchpad unsited.py) gave `11` `['first_look:put.input', ... 'first_look:put.walk_open']`.
  - `controller-blocks-gen.py <scratch>/cb.md` + `diff -q` against design/controller-blocks.md gave `IDENTICAL`.
  - The `match_known` probe on 5 texts gave `None, None, None, ('structured_artifact','resume_structured'), None`.
  - `git diff --numstat` gave 1/0 changelog, 23/17 controller.py, 5/5 census, 61/0 test. `git log` grep `tests-over`
    gave none.
- Side effect, cleaned: `tools/controller-blocks-gen.py --help` (the card's instruction) treats `--help` as an output
  path and wrote a file `ai-packages/qa-factory/--help` into the worktree (gen :484-486). I removed it, and `git
  status --short` is back to 0 lines. The generator's argv handling is a tool defect outside this diff. Proposed node
  for the Lead: `--help` and unknown flags should refuse, not write. The same trap waits for any builder told to run
  `--help`.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "class_completeness": "Axis 18: qa-test-strategist 121->122 named (mech :402 (a)); conductor 748->747 wrong, stays 748 (F1). Axis 32: no class or scan-constant change. In-artifact sweep: _s3_completion_gate's labelling/ValueError/grounding raises reach the conductor (F1 label; siting is a card non-goal, M7 gap 4); _plan_rework_rows_problems and _plan_review_problems PlanUnreadable branches reach the conductor (F1 siblings); _code_review_problems carries the receipts reach (F2); bare/over-told sites of _plan_review_problems and rework_rows go to T1r-cards-R as written lines (F5).",
  "fixes": [
    "F1 judgment-census.json _s3_completion_gate roles [qa-test-strategist, conductor], ratchet conductor back to 748 (strategist 122 named); same reach for _plan_rework_rows_problems and _plan_review_problems (+conductor) or a named reason",
    "F2 judgment-census.json :189 _code_review_problems roles [qa-code-critic] with note (Lead widens owns by that row)",
    "F3 name the test-volume reason (+66 test vs +23 product): report line and tests-over: on the fix-round commit",
    "F4 fix-round commit carries an accurate judgment reason (plan contract, grounding, labelling close; reach adds the strategist beside the conductor)",
    "F5 write the T9a residual sites (controller.py :7073, :7075, :7104-7108, the :7037 state-not-mapping over-tell) into T1r-cards-R inputs or Ostatki with node id"
  ],
  "trail": {
    "read": [
      "docs/tasks/specs/20261117-told-before-work-finish-spec.md :40-125 :415-445 :676-700",
      "docs/tasks/specs/20261113-told-before-work-mechanism-spec.md :402 :514-523",
      "git diff origin/main...HEAD (worktree agent-aec234043a06ad25c)",
      "ai-packages/qa-factory/scripts/controller.py :5925-5996 :6575-6600 :6983-7125 :7683-7735",
      "ai-packages/qa-factory/references/stage-joints.json :2780-2940",
      "ai-packages/qa-factory/scripts/stage_joints.py :761-786 :1105-1170",
      "ai-packages/qa-factory/scripts/tests/test_judgment_census.py :77-87 :218-300 :498-512",
      "ai-packages/qa-factory/scripts/driver_machine.py :44-66 :442-480",
      "ai-packages/qa-factory/scripts/driver_dispatch.py :36-110",
      "ai-packages/qa-factory/scripts/detector_verdict.py :95 :149-233",
      "tools/architecture_gate.py :34-62 :245-310",
      "tools/test_volume.py :1-30",
      "docs/TESTING.md Budget section",
      "docs/SIBLING_MAP.md axes 18 and 32",
      ".claude/agents/critic.md :178-280"
    ],
    "reruns": [
      {"command": "python -B scripts/tests/test_controller_doors.py (worktree package cwd)", "result": "=== test_controller_doors: 83/83 ok ==="},
      {"command": "census probe: test_judgment_census._real() + units_of on worktree", "result": "problems {}; qa-test-strategist 122, conductor 747; _code_review_refusal no unit; _s3_completion_gate blocks u3; three S5 units non-blocking u1"},
      {"command": "unsited probe: stage_joints._direction_a(joints, universe(), sited_ids())", "result": "11 unsited, all first_look:put.*, no controller:*"},
      {"command": "controller-blocks-gen.py to scratch + diff -q design/controller-blocks.md", "result": "IDENTICAL"},
      {"command": "driver_machine.match_known on labelling / grounding / rows-not-list / plan-invalid / plan-unreadable texts", "result": "None, None, None, (structured_artifact, resume_structured), None"}
    ]
  }
}
```
