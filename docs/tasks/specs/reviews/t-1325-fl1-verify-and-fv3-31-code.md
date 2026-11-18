# t-1325 critic: FL1 fix verification (t-1315 A1-A5) and FV3-31 code gate (t-1320)

Heads: FL1 `origin/worktree-agent-ae73b12e984c78fa9` (code `ef725767`, report `0e323c28`); FV3-31 `origin/worktree-agent-ac123f6216163a6d8`
(`a92dced6`). origin/main `25ff21f5`. Read-only: the package of each head was extracted with `git archive` into the scratchpad. No worktree was made and nothing was edited.

## Verdicts (input to the Lead's acceptance; the decision is the Lead's)

- **(1) FL1 / RD1-19: NEEDS WORK.** A1, A3, A4 and A5 are CLOSED. A2 is CLOSED as stated. The A2 fix adds one new fix-before-merge finding (N1). No blocker.
- **(2) FV3-31: NEEDS WORK.** 1 blocker (no build report or witness), 3 fix-in-round, 2 notes. The code follows F1-F4. The reader and walk are correct.

---

## (1) FL1: per item

- **A1 CLOSED.** `references/artifact-contract-automation.md:19` again has `"evidence": "evidence/sanity.json",`. Both slices have it too (`slices/qa-automator/...:19` and `slices/qa-code-critic/...:19`, by grep).
  - My role_load re-run gives qa-automator tokens 25,697, process 24,107, verdict within. qa-code-critic gives 23,605 / 21,782, and qa-failure-analyst 21,659 / 19,609. These match the report, and `role-load.json` is untouched.
  - Three bytes were netted. Two of them dropped wording: " — never by hand" at :9 and ", by `manifest_put.py --fragment`" on the `introduced_helpers` line. The meaning still holds because :9 says "Written only through `manifest_put.py --fragment`". `role_rules --check` gives 0 findings, so no anchor was lost.
- **A2 CLOSED (as the critic asked).** `_stamp_rows` (manifest_put.py:1053) collects the old spelling of a renamed held row. `_retract_renamed` (:1069) adds it to `retracted_instances`. `_retract_instances` (:2330) drops the old row.
  - My probe ended with one row, `test_x[chromium-eu]`, verified.
  - The Lead-confirmed side effect also holds. The stored Then on `test_x[eu]` is retired, and `removed_then_lines` prints `TC-001 Then 1 on test_x[eu]`. `run` builds that receipt from the stamped fragment: the stamp is at :2883 and `taken_out` at :2957.
- **A3 CLOSED.** When the call raises, `_ask_collect` returns `(None, "<ExcType>: <message>")` (:990). `stamp_node_ids` reads the collect only when `checked is not None` (:1106). The `ANSWER_ROWS` E1 row is the killing row.
- **A4 CLOSED; both Lead-confirmed choices hold in the code.**
  - Same file: `_verified_mark` (:1027) takes `base = last` when the typed base has no `::` and the resolved last segment differs. So `test_plian` -> `test_plain`, with `asked` keeping `test_plian`.
  - The class step is not added (E5a): typed `test_y` against resolved `TestA::test_y` keeps `t_base`. I traced this by hand.
  - Another file: `node_ids.same_file` is false, so the row becomes `not_verified` with "the collect named ..., a test of another file" (:1048). `same_file` exists on main (node_ids.py:574). It tolerates either slash and a rootdir prefix.
- **A5 CLOSED.** `stamp_node_ids` is now 34 lines, and no helper is over 26 lines or 3 nesting levels. `import node_ids` sits once at module top (:127).
  - Disclosed and acceptable: E1's "an import of node_ids fails -> not_verified" no longer holds, because node_ids uses only the standard library and a broken node_ids now fails the import of manifest_put.

### (1) New finding introduced by the A2 fix

**N1 (fix-before-merge): a renamed re-send drops the stored row's fields that the fragment does not repeat (covers, case_version_links).** The A2 road removes the held row instead of renaming it. The merged row therefore holds only what the re-send carried.
- Probe (pure `stamp_node_ids` + `merge`, collect stubbed to `test_x[eu] -> test_x[chromium-eu]`). Stored row: `covers [TC-001]`, `case_version_links`, `not_verified`. The re-send is `{instance_id: test_x[eu], file, status: red}`:
  `rows: [('test_x[chromium-eu]', 'red', None, False, 'verified')]`. Covers and links are gone.
- Control: the same patch with no rename (collected as typed) gives `[('test_x[eu]', 'red', ['TC-001'], True, 'verified')]`, and the Then is kept.
- Even a full re-send that omits `case_version_links` loses it. Probe: `('test_x[chromium-eu]', 'green', ['TC-001'], False, ...)`.
- Failure scenario: the automator patches the status of a row stored before any collect existed, with `file` (eligible, FR-40). The case silently loses its proving row. No receipt line names the loss, unlike the Thens.
- The A2 test (`test_manifest_put_assertion_line.py:324`) asserts only the row count.
- Fix: in `_stamp_rows`, for a renamed `held` row, first fill the fragment row with the held row's fields it lacks (`setdefault`, except `instance_id`/`node_id_check`), then retract. Add one assert to the parametrised row: covers kept. Whether to rebind the stored Thens instead of retiring them stays the Lead's confirmed choice.

### (1) standing questions
- Q1: A1-A5 are met as asked. Q2: the builder's two A4 choices point the safe way (Lead-confirmed). Q3: additive.
- Q4 class: the same A3/A4 shapes in `manifest_from_tests.resolve_through_pytest` are named for RD1-35 (the node exists). Q12(d) residual F6 is carried from t-1315 (Lead).
- Q5: (a) the ANSWER_ROWS and A2 rows kill A2-A4. (c) N1 has no row. Budget is 224 test lines against 403 product lines.
- Q6: none found (the helpers reuse `node_ids.same_file`/`split_id`; grep `def same_file` gives 1, on main).
- Q7: the one-line nested conditional at :1027 is dense but correct (note).
- Q8: English.
- Q9: no ratchet row changed in attempt 4. The role loads are equal (above).
- Q10: AR-20 is named. VARIETY: unchanged from t-1315.
- Q11: none.
- Q12: one road (`node_ids`).
- Canon 44215465984: `checks / forge-check` failure. The lint ratchet found 1 new finding, `driver_stage_s6.py:1563 'dispatch_identity' imported but unused`, in a file FL1 does not touch. It is the same line on origin/main, so it is main's red. package-full was still in_progress when read.

---

## (2) FV3-31: findings

**F1 (blocker, rule 7 witness): there is no build report.** `docs/tasks/specs/reports/20261118-fv3-31-build-report.md`, the card's `handoff:`, is absent on the branch. `git log --all -- <path>` is empty. The only report is the earlier question report `20261118-fv3-31-report.md`.
- Missing: the `test_handoff_init.py` witness, N2, N4, the base/after A22 numbers, "the bytes trimmed and why" (item 4), the slice diff stat, the F4 quarantine-pin line (f18 flips red by design), and the `not run locally` lines.
- I re-ran two of them: N1 (all 13 rows PASS) and N3 (`process_tokens` 21782). I traced N4 instead of running it (below). The rest has no carrier.

**F2 (fix-in-round): E11 is met in number but not the way item 4 says.** The bytes were netted by role-facing slice text the role loses, not by trimming form comments.
- Both forms grew by +114 B, and no comment was trimmed: round 2 only shortened its own added "(prefilled by code; keep it)". The net came from the slice: `handoff-keys.md` +282, `handoff-keys-2.md` -397. That is net -1 B and gives 21782.
- What the slice lost: `- inputs_read[].path (required) - path exactly as the author listed it` is gone. `inputs_read[].version` now reads "hash, or omit", which is the author row's hint and wrong for case rows (main: "pinned case version, content hash, or the file's sha256").
- Cause: `contract_slices.py:559` lists a field only when its FIRST row's value is a whole placeholder. Row 0's `work/handoffs/<the author's dispatch>.yaml` is not.
- The S4 twin slice has the same omission (single row, so no hint conflict). Compared with A1 it is milder, because the form copy itself still shows `path:` rows. But it is the same class: a key code checks, lost from "What code will check of you" to fit a ratchet, and not disclosed.

**F3 (fix-in-round): the refusal hint of every row now comes from the author row.** `handoff.spec_of` keys `inputs_read[].*` on row 0.
- Probe: `s5-critic-to-automator inputs_read[].path required | hint: work/handoffs/<the author's dispatch>.yaml`; `inputs_read[].version optional | hint: hash, or omit`. On main the hints were "path exactly as the author listed it" and the case-version text.
- A blank `inputs_read[1].path` is therefore refused with "not filled. work/handoffs/<the author's dispatch>.yaml" (handoff_check.py:1735/1769). That points the critic at the wrong value.
- Required/optional status itself is unchanged: path is required before and after, and version is optional before and after. So **no row loses a required field**, which answers the dispatch.
- Fix options for F2+F3, the Lead's call: per-row hints for a list whose rows differ (handoff.py is in owns), or an explicit, named change to the slice rule. The Lead decides scope.

**F4 (fix-in-round or a node, the Lead's call): with round 2, an unfilled author row passes.** The dispatch asked where the version check sits now.
- The deriver still fills row 0's version whenever the path is a real file, because deriving runs before the optional test (handoff_check.py:1745-1755 vs :1769). That part is where the card wants it.
- In the unknown-author worlds (E1, E3, E4, E7) the token stays. `handoff.is_placeholder("work/handoffs/<the author's dispatch>.yaml")` is `False` (probe), so the path counts as filled. `_version_of` returns None for a path with `<`, and the field is optional, so there is no refusal.
- The form then stands with a proof-of-reading row that names no file (AR-21, FR-59). The comment still says "Row 0 is the author's form (prefilled)". No S5 gate reads the row (E13).
- In round 1 the required `<hash>` refused exactly this row. Round 2 removed the only refusal along with the dry-world red.
- The S4 twin has the same gap (pre-existing), so this is a class of the token road. `handoff.only_template(value, template)` already treats "a token equal to the template's leaf" as untouched, but the field loop calls `is_placeholder` without a template.
- Proposed: the field loop reads blank as `only_template(value, template leaf)`, for S4 and S5 alike. handoff_check.py is outside owns, so this needs a node with an owner or wider owns (Lead).

**F5 (fix-in-round, Q5(c)): the card's test row 2 named "S4 critic and S7 analyst answers unchanged", and it is absent from `s5_reviewed_dispatch_rows`.** That row is the §2.1 position invariant. Its other carriers are the quarantined `test_handoff_init_author.py`/`test_stage_done.py` (card §4), so no keep-layer row guards it. Add the two rows to the same table.

**Notes.** (n1) The E2 stderr line prints on every `reviewed_dispatch` call for every S5 role, including the automator. It is harmless. (n2) `<the automator's dispatch>` is left only in prose (`skills/qa-story/phases/s5.md:313`, `tests/story_step_common.py:197`) and fixtures. E10 holds: grep over handoffs/ gives 0 templates, and the control `the author.s dispatch` hits 3 forms.

### (2) Edges, narrow calls, Lead decisions
- E1 holds (row "no `reviewed_by`"). E2 holds (brief_pack.py:3741-3744 covers every invalid kind; the row tests the non-string one). E3 holds by trace (`{}` -> no key -> today's search).
- E4 holds ("no record"; an unmet id gives `met` False). E5 and E6 hold (rows: A3 created after the critic, plan vs window). E7 holds (no line).
- E8 holds in the filled world (`test_author_table`, not run by me); the unknown world is F4. E9 holds by the deriver, except F4.
- E10 holds. E11 holds in number, with F2. E12 has no line (F1). E13 holds (wording unchanged). E14: dry run 44214588432 has 5 jobs, all success (my ci_read).
- N1 was re-run by me: 13 PASS. N2 has no witness (F1). N3 = 21782 (my run). N4 has no witness, but by trace `advice_of` is byte-identical: the old `s5_part_of(other) != "plan"` equals the new `== "window"`, because `controller.s5_part_of` returns only "plan"/"window" (controller.py:142-155). The walk, the stop at its own id and the input are the same, and `met` is ignored (brief_pack.py:3653).
- F1=(a): the token is in both forms and `handoff_init.py` is untouched. F2=(a): `reviewed_author_of` (:3620), bound to the controller record in both callers (`build`: the `dispatches[dispatch_id]` record + id; `_handoff_form`: `_dispatch_record` + id). F3=(a): unchanged. F4=(a): the report line is missing (F1).
- Q4: the token-road class is F4 (S4 twin). Q6: one walker (AR-13). Q7: none. Q9: no ratchet raised (`ROLE_BRIEF_BYTES_MAX` and role-load.json untouched).
- Q10: AR-1 holds (no "S5"/role literal in the new branch, apart from the card-prescribed `s5_part_of`). VARIETY: none. Q11: none. Q12: one road (token).

## Trail
- Read: the t-1315 review (whole); the FV3-31 card (whole); the FL1 report; both diffs. FL1 manifest_put.py :225-240, :885-916, :967-1110, :1165-1230, :1871-1900, :1968-2000, :2137-2150, :2318-2345, :2525-2580; node_ids.py :551-593.
- FV3-31 brief_pack.py :3620-3780 diff; story_step.py :318-370, :3133-3141; handoff.py :30-40, :403-430, :435-470, :660-680, :716-718; handoff_check.py :496-502, :1715-1790; contract_slices.py :548-566; handoff_init.py :115-150; controller.py :142-156; the S4 form and slice.
- Probes: `probe_a2.py`/`probe_a2b.py` (N1 rows quoted above); `probe_spec.py` (F3/F4 output quoted).
- Reruns (FL1 tree): role_load ×3 roles (numbers above); `role-rules: 457 rows, 546 carriers checked, 0 finding(s)`; `slices: 44 declared, all present and fresh`.
- Reruns (FV3 tree): role_load qa-code-critic `process_tokens 21782 within`; contract_slices fresh; N1 13 PASS.
- CI: `ci_read.py jobs 44215465984` (forge-check failure; log tail quoted above); `jobs 44214588432` (5 success).

```json
{
  "verdict": "blocker",
  "blockers": [
    "FV3-31 F1: no build report on the branch (docs/tasks/specs/reports/20261118-fv3-31-build-report.md absent, git log --all empty): no test_handoff_init witness, no N2/N4, no A22 before/after, no trimmed-bytes account, no F4 quarantine-pin line"
  ],
  "fixes": [
    "FL1 N1 manifest_put.py:1053/_retract_renamed :1069 - a renamed re-send of a held not_verified row drops covers/case_version_links the fragment does not repeat (probe: covers None after a status patch, kept without rename); carry the held row's missing fields before retracting, add a covers-kept assert",
    "FV3-31 F2 slices/qa-code-critic/handoff-keys.md - A22 netted by the slice losing inputs_read[].path (required) and the case-row version hint (contract_slices.py:559 first-row placeholder rule), not by form comment trims as item 4 requires",
    "FV3-31 F3 handoff.spec_of first-row rule - inputs_read[].path refusal hint is now the author row literal, version hint 'hash, or omit' for case rows",
    "FV3-31 F4 handoff_check.py:1735 - an unfilled author token row (is_placeholder False) with optional version passes; round 2 removed the only refusal; S4 twin shares it; proposed: blank = only_template(value, template leaf); outside owns, Lead opens node or widens owns",
    "FV3-31 F5 test_brief_pack.py::s5_reviewed_dispatch_rows - card row 'S4 critic and S7 analyst answers unchanged' missing"
  ],
  "class_completeness": "FL1: A3/A4 shapes in manifest_from_tests.resolve_through_pytest are RD1-35's (exists); F6 universality residual carried from t-1315 (Lead). FV3-31: the unfilled-token pass (F4) and the first-row hint rule (F2/F3) are token-road classes shared with the S4 twin form; a node with an owner is proposed for the Lead to open.",
  "trail": {
    "read": [
      "docs/tasks/specs/reviews/t-1315-fl1-and-pc4-19-b-code.md",
      "docs/tasks/specs/20261118-fv3-31-s5-critic-inputs-read-card.md",
      "docs/tasks/specs/reports/20261117-rd1-19-fl1-report.md",
      "ai-packages/qa-factory/scripts/manifest_put.py",
      "ai-packages/qa-factory/scripts/node_ids.py",
      "ai-packages/qa-factory/references/artifact-contract-automation.md",
      "ai-packages/qa-factory/scripts/tests/test_manifest_put_assertion_line.py",
      "ai-packages/qa-factory/scripts/brief_pack.py",
      "ai-packages/qa-factory/scripts/story_step.py",
      "ai-packages/qa-factory/scripts/handoff.py",
      "ai-packages/qa-factory/scripts/handoff_check.py",
      "ai-packages/qa-factory/scripts/contract_slices.py",
      "ai-packages/qa-factory/scripts/handoff_init.py",
      "ai-packages/qa-factory/scripts/controller.py",
      "ai-packages/qa-factory/handoffs/s5-critic-to-automator.yaml",
      "ai-packages/qa-factory/handoffs/s5-critic-plan-to-automator.yaml",
      "ai-packages/qa-factory/handoffs/s4-case-critic-to-designer.yaml",
      "ai-packages/qa-factory/scripts/tests/test_brief_pack.py",
      "ai-packages/qa-factory/scripts/tests/test_handoff_init.py"
    ],
    "reruns": [
      {"command": "role_load.py --role qa-automator/qa-code-critic/qa-failure-analyst --json (FL1 tree)", "result": "25697/24107, 23605/21782, 21659/19609, all within"},
      {"command": "role_rules.py --check (FL1 tree)", "result": "role-rules: 457 rows, 546 carriers checked, 0 finding(s)"},
      {"command": "contract_slices.py --check (FL1 and FV3 trees)", "result": "slices: 44 declared, all present and fresh"},
      {"command": "probe stamp_node_ids + merge, rename with partial re-send (FL1)", "result": "one row test_x[chromium-eu], covers None, links lost; control without rename keeps covers and Then"},
      {"command": "role_load.py --role qa-code-critic --json (FV3 tree)", "result": "process_tokens 21782, verdict within"},
      {"command": "N1 test_brief_pack.s5_reviewed_dispatch_rows (FV3 tree)", "result": "13 PASS"},
      {"command": "probe handoff.spec inputs_read hints + is_placeholder on token row (FV3 tree)", "result": "path hint = author row literal; version 'hash, or omit' optional; token row is placeholder: False"},
      {"command": "ci_read.py jobs 44215465984 / 44214588432", "result": "FL1 canon forge-check failure (driver_stage_s6.py:1563 lint, main's line); FV3 dry run 5 jobs success"}
    ]
  }
}
```
