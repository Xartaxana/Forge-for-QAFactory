# FV3-31 build report (t-1320)

Round 3 (the last section) STOPPED with three questions; read it first. Round 1 below: branch `worktree-agent-ac123f6216163a6d8`, head `d89996aa67e0c6dfee2b9a6abecc7202b20e7e44` (pushed). Canon run (not waited): 44212972210. Dry run: 44212976230 = FAILURE (below). Note: `ci_read.py start` dispatches on `main` with the ref as an input, so the `pipelines` sha column shows main's 5bace71d, not my head. This report is written in the worktree (the shared path was refused); it is not in the commit.

## Items
- 0 DONE base: `role_load.py --role qa-code-critic --json` -> process_tokens 21782, total_bytes 94420; test_handoff_init green before edits.
- 1 DONE `references/stages.json`: `"reviewed_by": "qa-code-critic"` after `roles` of S5.
- 2 DONE `scripts/brief_pack.py`: `reviewed_author_of` (walk extracted from `advice_of`; `advice_of` calls it); `reviewed_dispatch(..., dispatch=None)` with the `reviewed_by` branch after the own-stage branch, before the consumer search, validity + one stderr line; `_id`/`_lines` pass `dispatch`; `build` passes `dict(dispatch or {}, id=dispatch_id)`. No `"S5"`/`"qa-code-critic"` literal in the branch code (docstring names them).
- 3 DONE `scripts/story_step.py`: `_author_argv(..., dispatch=None)`, `_handoff_form` passes the record with the id.
- 4 DONE both S5 critic forms: `inputs[0].path` and new first `inputs_read` row use the author token, row `version: <hash>`, comment says row 0 is the author's form. After the commit `<the automator's dispatch>` exists in no template (only in frozen story fixtures: filled forms).
- 5 DONE `scripts/handoff.py:406` comment.
- 6 DONE `contract_slices.py --write`: `handoff-keys.md` (+`handoff-keys-2.md`, see deviations); re-measured.
- 7 DONE `changelog.d/fv3-31-s5-critic-reviewed-row.md`.
- 8 DONE tests (below). 9 DONE commit with `architecture:` AR-22/13/15/1/28/20, `judgment: none`, `tests-over: none` (the dispatch asked for the trailer).

## A22 numbers
Base 21782 / 94420 B. After items 1-5 (before slice): 21806 / 94513. After slice regen: 21775 / 94389 (below = red too). Final 21782 / 94418 = base EXACTLY (N3).
Bytes trimmed: NONE. The regenerated slice shrank (two `inputs_read` rows with different version hints collapse, the path hint goes), so I ADDED 8 bytes of true meaning to the form comment: `(prefilled by code; keep it)` (both forms, same wording). role-load.json untouched.
Slice diff stat: `handoff-keys.md` 2+/2- (`inputs_read[].path` hint and the optional `version` line replaced by `inputs_read[].version (required) - hash`); `handoff-keys-2.md` 0+/1- (one `execution_request:profile_command` line; generator re-pagination, `handoff-keys.md` gains one line at its end).

## Witness (one round after all edits; code did not change after it)
```
== test_handoff_init
PASS FV3-31 S5 critic plan form + author
PASS FV3-31 S5 critic usual form, no author: the token stays
PASS FV3-31 S5 critic plan form, no author: the token stays
...
=== handoff_init purpose: 27/27 ok ===
== N1 (test_brief_pack.s5_reviewed_dispatch_rows)
PASS FV3-31 S5 prefill = brief (K1) / (KP) / (None)
=== N1: 13/13 ok ===
== N2 (test_field_producers, two functions)
PASS the deriver round walked forms
deriver round: forms 22, fields met 39
N2 returned
== N3 role_load --role qa-code-critic --json
  "total_bytes": 94418,
  "process_tokens": 21782,
== N4 advice_of probe (4 critics, synthetic state, plan + 2 windows), before vs after item 2(a): diff -> N4 IDENTICAL
(output: K1 work/advice-S5.json / K2 work/advice-S5-A2.json / ZZ work/advice-S5-A1b.json / K9 work/advice-S5.json)
```
Also (not asked): `test_brief_pack.role_brief_ratchet()` one function: `RATCHET ROLE_BRIEF_BYTES_MAX qa-code-critic 7177` vs 7189, green (E12 not triggered). The probe script lives in the session scratchpad (not committed).

## Tests
Added: `test_handoff_init.py::AUTHOR_ROWS/test_author_table` (4 rows, 24 lines); `test_brief_pack.py::s5_reviewed_dispatch_rows` (13 checks, registered in `main` after `role_brief_ratchet`, 49 lines). Test lines 73 vs code+product lines ~72 (numstat: brief_pack 48, story_step 6, handoff 1, stages 1, forms 8, slice 2, changelog 6).
Tests not written (over budget, trimmed): rows "the other window's critic", "S4 critic keeps the S4 author" (S7 analyst never written), "released automator skipped", "empty scope", "id not met in records". Code handles them; no row pins them.
Not run locally (canon judges): test_brief_pack.py whole, test_field_producers.py whole, test_contract_slices.py, test_handoff.py, test_story_run_s5*.py, test_judgment_census.py. Quarantine pin f18 (`test_handoff_init_author.py::test_s5_contracts_get_no_author_arg`) turns red by design (F4 a): not run, not edited. The three quarantine files untouched.

## DRY RUN 44212976230: FAILURE, a NEW red (reported, not fixed)
Compared with the latest finished dry-story on a main-based branch: 44209748794 (`worktree-agent-a8bcc2e22d235bf0a`, 0598c297, an ancestor of origin/main) = success, red set empty. Main has no finished dry-story of its own (44211245394 was in_progress). My red set is NOT a subset. Failed jobs: `dry-story / tables` (134495905113), `dry-story / parts (gates)` (134495905217). Verbatim:
```
tables: FAIL dry-1/exits:selftest/s8.delivery.no/go on ? start S8 not made and the main pass stopped at S5 with no known_red row
tables: FAIL dry-1/exits:selftest/known_red ? new red: s8.delivery.no/go on ? fix it, or add ... to .../fixtures/stories/dry-1/selftest/known_red.json known_red
tables: === scenario dry-1: 3/5 ok ===
gates: FAIL dry-1/exits:gates/gate_B/{rework,approve,retry,stop,free words,empty} ? start S8 not made and the main pass stopped at S5 with no known_red row
gates: FAIL dry-1/exits:gates/known_red ? new red: gate_B/{approve,empty,free words,retry,rework,stop} ? fix it, or add ... gates.json known_red
```
Cause NOT verified (estimate): the dry main pass stops at S5. E14 predicted the dry S5 critic now fills the token from the brief line; the filled S5 critic form (row 0 author, row 1 `<path exactly as the author listed it>` unfillable) is the first suspect. Not reproduced locally (dry worlds are canon-class). Canon run 44212972210 was still in_progress at hand-back.

## Deviations / needed from integration / analogs
- `references/slices/qa-code-critic/handoff-keys-2.md` is regenerated by item 6 but not in owns: committed with the slice (generator output). Lead: confirm.
- Slice content: the `inputs_read[].path` hint ("path exactly as the author listed it") no longer appears in the qa-code-critic slice; the template still holds it.
- Item 4 asked to trim comments; none needed (see A22 numbers).
- `reviewed_dispatch` prints the invalid-`reviewed_by` stderr line on every call at that stage (any role), as `acceptance_reads` does.
- Analogs: `s4-case-critic-to-designer.yaml` row 0 uses a prose version placeholder (not `<hash>`); `brief_pack.last_accepted_form` is another "last accepted dispatch of role at stage" walk (no part/scope), left alone.
- Needed beyond the manifest: `tools/architecture_gate.py` docstring, `acceptance.py::stage_author_dispatch/awaits_acceptance`, `controller.py::s5_part_of`, `dispatch_identity.py`, `probe_debt.bare_case_id`, `tools/ci_read.py`.
- No loops or processes left running.

## ROUND 2 (head a92dced66ccbc2f1c40e01e3ca5a939137a92252, origin/main merged first)
Cause (measured): row 0 `version: <hash>` makes `inputs_read[].version` REQUIRED for every row (a list's rows share the first row's field spec; `handoff.py` OPTIONAL_WORDS makes a hint optional only with words such as ", or "/"or omit"). The dry filler (`fill_form`) leaves row 1 as `path: filled path` with no file, so `handoff_check` refused the critic's form: local repro with `FF.fill_form('s5-critic-to-automator', ctx(author_dispatch=...))` + `handoff_check.py --file ... --no-judge` printed `inputs_read[0].version: not filled. hash` and `inputs_read[1].version: not filled. hash`; the refused critic form is the "conductor at S5" stop of the main pass (the CI log line is truncated by ci_read; the stop text itself is only an inference). No dry_* file needs a change.
Fix (both forms, E10): row 0 `version: <hash, or omit>` (optional as the single row was before; deriver unchanged); comment `(prefilled)` re-nets process_tokens to 21782 / 94419 B. After the fix the same repro prints no `inputs_read` problem. Slice `handoff-keys.md` regenerated (2 lines).
Witness: test_handoff_init 27/27 ok; N1 13/13 ok; role_load process_tokens 21782. Dry run 44214588432 = success (red set empty, subset of 44209748794's).

## ROUND 3 (t-1320 attempt 3, Opus; base head a92dced6): STOPPED on the role-load rule, three questions

Status per Lead decision: F1 PARTIAL (this file is committed; the round-1 sections above already carry N2, N4, the A22 base/after,
the trimmed-bytes account, the slice diff stat, the f18 quarantine-pin line and the not-run-locally lines). F2+F3 DONE as stated
(one helper), but see Q1/Q2. F4 DONE as stated, but see Q3. F5 DONE. Role-load net NOT DONE (Q1: STOP, as the dispatch orders).
Not done because of the stop: no code commit, no merge of origin/main (it moved to 1278f0dc), no push, no CI run started.
The code edits are LEFT UNCOMMITTED in the worktree (list below), so the next round resumes from them.

### What was done (uncommitted)
- `scripts/handoff.py`: new `field_nodes(doc)` = {generic path: the first node whose value is a WHOLE placeholder, else row 0};
  `spec_of` now reads it. `scripts/contract_slices.py::_keys_form` reads the same helper, so there is no second rule.
- `contract_slices.py --write` regenerated 7 slice files (4 of them are OUTSIDE owns, see Q1).
- `scripts/handoff_check.py::check` field loop: `blank = is_placeholder(value) or ("[" in path and only_template(value, <template
  leaf at the same path>))`. `leaves = handoff.template(contract).nodes` is read once before the loop. Deriver order unchanged.
- `tests/test_brief_pack.py::s5_reviewed_dispatch_rows`: +2 rows (F5). "S4 critic answer unchanged" -> ("S4","D1",True); "S7
  analyst answer unchanged" -> ("S6","R1",False). Both are called WITH the S5 critic record and the live `reviewed_by` row.
- `tests/test_handoff_init.py`: helper `_checked`. Per AUTHOR_ROWS row: "token row refused iff no author" (row 1 set to a real
  file, no version: no `inputs_read[1]` refusal). Plus an S4 row: "no author, a real row added: the token row is refused".
  Measured: S4 with its single token row was ALREADY refused before F4, as the empty `inputs_read` ("inputs_read: no rows").
  F4 adds the refusal only when the S4 critic adds a row and keeps the token, so the S4 row sets row 1.
- The refusal hint of a blank S5 case-row path is the case-row text again (probe, verbatim):
  `inputs_read[0].path: not filled. path exactly as the author listed it` (S5 critic, no author). S4 gives `inputs_read[0].path: not
  filled. work/handoffs/<the author's dispatch>.yaml` (single row, so the stated rule falls back to row 0).

### Witness (one round; then test_handoff_init.py alone re-run once, because its S4 row changed)
```
== DoD
PASS FV3-31 S5 critic usual form + author: token row refused iff no author
PASS FV3-31 S5 critic plan form + author
PASS FV3-31 S5 critic plan form + author: token row refused iff no author
PASS FV3-31 S5 critic usual form, no author: the token stays
PASS FV3-31 S5 critic usual form, no author: the token stays: token row refused iff no author
PASS FV3-31 S5 critic plan form, no author: the token stays
PASS FV3-31 S5 critic plan form, no author: the token stays: token row refused iff no author
FAIL FV3-31 S4 critic, no author: the token row is refused
PASS door: a plan form (purpose s5_plan, author) names --to then --purpose
...
=== handoff_init purpose: 31/32 ok ===
== N1
Traceback (most recent call last):
  File "<string>", line 1, in <module>
AttributeError: module 'test_brief_pack' has no attribute 'finish'
PASS FV3-31 S5 reviewed_dispatch: two windows: the critic's own automator, A3 created after it is not named
PASS FV3-31 S5 reviewed_dispatch: the plan critic: the plan automator only
PASS FV3-31 S5 reviewed_dispatch: a window critic with only a plan automator
PASS FV3-31 S5 reviewed_dispatch: no matching window
PASS FV3-31 S5 reviewed_dispatch: no record
PASS FV3-31 S5 reviewed_dispatch: no `reviewed_by`
PASS FV3-31 S5 reviewed_dispatch: `reviewed_by` not a string
PASS FV3-31 S4 critic answer unchanged
PASS FV3-31 S7 analyst answer unchanged
PASS FV3-31 S5 brief line names the critic's own automator path
PASS FV3-31 S5 no match: no line, not the none-yet line
PASS FV3-31 invalid `reviewed_by` prints a stderr line
PASS FV3-31 S5 prefill = brief (K1)
PASS FV3-31 S5 prefill = brief (KP)
PASS FV3-31 S5 prefill = brief (None)
== role_load
  "total_bytes": 94492,
  "process_tokens": 21800,
  "verdict": "within"
== slices
slices: 44 declared, all present and fresh; 20 key pages; 12 charters carry a generated digest line
== re-run after the S4 row fix (test_handoff_init.py only)
PASS FV3-31 S5 critic plan form, no author: the token stays: token row refused iff no author
PASS FV3-31 S4 critic, no author, a real row added: the token row is refused
PASS door: a plan form (purpose s5_plan, author) names --to then --purpose
PASS door: a plan review form (purpose s5_plan, critic) names --to then --purpose
PASS door: an ordinary S5 form prints no --purpose and no --to
PASS door: a two-contract stage form (S4 secondary) still prints --to alone

=== handoff_init purpose: 32/32 ok ===
```
The N1 traceback comes from my one-liner calling a `finish` that the module does not have (stderr is printed first). All 15 rows
ran and passed before it. `"verdict": "within"` is the threshold verdict, not the ratchet. The ratchet row is 21782 (`references/role-load.json`
`process_ratchet_tokens.qa-code-critic`), so 21800 is OVER by 18.

### Q1 (STOP): the one helper moves four roles over their process ratchet; three of them are outside owns
`role_load.py --all --json` after the helper + `--write`, against `process_ratchet_tokens` in `references/role-load.json`:
```
qa-code-critic          21800  row 21782  +18  slice gains `inputs_read[].path (required) - path exactly as the author listed it`
qa-requirements-tester  13557  row 13538  +19  slice gains `inputs_read[].path (required) - each source the scout marked `relevant``
qa-runner               17264  row 17247  +17  slice gains `inputs_read[].path (required) - the runtime_provenance record`
qa-failure-analyst      19625  row 19609  +16  slice gains `inputs_read[].path (required) - the runtime_provenance record`
```
Every other role equals its row. Cause: s2-tester-to-strategist, s6-runner-to-analyst and s7-analyst-to-automator also have a
non-placeholder row 0 in `inputs_read` (spec diff below). So the slice rule now lists their path field too: the same class as the
S5 restore. qa-code-critic alone can be netted inside owns: about 72 B of S5 critic form comments (lines 1-2 restate the
`to_role` comment on line 10). That is feasible but NOT done, because its size depends on Q2. The other three need the slices
`references/slices/{qa-requirements-tester/handoff-keys.md, qa-runner/handoff-keys.md, qa-runner/handoff-keys-2.md,
qa-failure-analyst/handoff-keys.md, qa-failure-analyst/handoff-keys-2.md}` plus comment trims in their own forms, all outside
owns. Question: widen owns to those slices and forms (net each one by form-comment trims), or take another road?

Spec diff of the helper (every contract, `handoff.spec_of`): required/optional is unchanged in every row; only hints change.
```
s2-tester-to-strategist inputs_read[].path    'work/impl-diff.txt' -> 'each source the scout marked `relevant`'
s5-automator-to-critic inputs[].path          'work/handoffs/<dispatch>.yaml' -> 'test files listed in artifacts.tests'      (contract-owned)
s5-automator-to-runner inputs[].path          'work/handoffs/<dispatch>.yaml' -> 'the runtime_provenance record named below' (contract-owned)
s5-critic-plan-to-automator inputs_read[].path  author-token literal -> 'path exactly as the author listed it'
s5-critic-to-automator inputs_read[].path       author-token literal -> 'path exactly as the author listed it'
s6-runner-to-analyst inputs_read[].path       'work/handoffs/<the automator's file>.yaml' -> 'the runtime_provenance record'
s7-analyst-to-automator inputs[].path         'work/handoffs/<dispatch>.yaml' -> 'the evidence paths named per repair'       (contract-owned)
s7-analyst-to-automator inputs_read[].path    author-token literal -> 'the runtime_provenance record'
s7-automator-to-analyst inputs[].path         'work/handoffs/<dispatch>.yaml' -> 'the changed test files named below'        (contract-owned)
```

### Q2: the stated F2/F3 rule and the stated expected result disagree on `inputs_read[].version`
The rule is "the first row whose value for that key is a WHOLE placeholder, falling back to row 0". Row 0's `version: <hash, or omit>`
IS a whole placeholder, so the rule keeps "hash, or omit" for every row. Measured: the S5 `version` spec did not change in the
diff above, and the slice still reads `inputs_read[].version (optional) - hash, or omit`. The expected result asks for the case-row
text. What I implemented: the rule as written (path restored, version not). Option B meets both expectations: a row-level pick,
where the first row whose EVERY leaf is a whole placeholder speaks for all its keys, and otherwise the per-key rule applies.
Cost: about +41 B / +10 tokens more in the qa-code-critic slice (estimate, not verified). Which one do you want?

### Q3: F4 as stated is contract-neutral and newly refuses 13 list fields in 10 contracts
Probe: `form_filler.fill_form` per contract (base variant), then `handoff_check.check(fix=False)`. A refusal counts as new when
the value is not `is_placeholder`. Run once with the author given and once without:
```
s4-designer-to-runner execution[0].evidence.where = work/evidence/<case>/
s5-automator-to-runner inputs_read[0].path = work/handoffs/<the gate A file>.yaml ; inputs_read[1].path = <cases_root>/<case>.md
s5-critic-(plan-)to-automator inputs_read[0].path = work/handoffs/<the author's dispatch>.yaml   (no author only: the target)
s5-critic-to-automator probes.records[0].record = work/probes/<instance>.json
s6-runner-to-analyst inputs_read[0].path = work/handoffs/<the automator's file>.yaml ; inputs_read[1].path = ...<the designer's manual file>.yaml
s7-analyst-to-automator / s7-analyst-to-scribe / s8-scribe-to-gate-b inputs_read[0].path = <the author's dispatch> token (no author only)
s7-analyst-to-scribe bug_drafts[0].path = work/bug-drafts/<file>.json
s7-automator-to-analyst inputs_read[0].path = work/handoffs/<the analyst's dispatch>.yaml
s8-bug-reporter-to-scribe inputs_read[0].path = work/handoffs/<the gate B decision file>.yaml
s8-scribe-to-gate-b questions[0].records_with = waiver.py --task <T> --stage <S> --block "<the exact block text code reads>"
s9-retro-to-project inputs_read[1].path = work/handoffs/<the gate B file>.yaml
```
All but one are values that the test filler marks unfillable. The dry stub raises on those, so dry worlds supply real values, and
by meaning these are correct refusals. The exception is `s8-scribe-to-gate-b questions[0].records_with`. Its
`tests/fixtures/form-fill-rules.json` `literal_text` row `command-template` declares it text that a role copies, the filler keeps
it verbatim, and F4 now refuses it. If a dry S8 scribe form keeps its `questions` row, the dry world newly stops at S8.
NOT measured: dry worlds are canon-class. Question: keep F4 contract-neutral (and accept or repair the S8 literal), or narrow it?
If narrowed, by which data rule (no contract list, AR-1)?

### Report lines
- Budget: this round adds 18 test lines against 24 code/product lines (handoff 12, handoff_check 4, contract_slices 1, slices 7).
  The branch is about 91 against 96.
- Tests not written: none of the dispatch's rows were dropped.
- Not run locally (canon judges): test_brief_pack.py whole, test_field_producers.py, test_contract_slices.py, test_handoff.py,
  test_story_run_s5*.py, test_judgment_census.py, test_role_load.py. The quarantine pin f18 is unchanged from round 1 (red by design).
- Uncommitted in the worktree: the 7 slice files, contract_slices.py, handoff.py, handoff_check.py, test_brief_pack.py,
  test_handoff_init.py. No loop or process left running.
- Deviation: I did not read `design/factory-rules.md` whole (dispatch cost discipline); I read FR-4, FR-57 and FR-59. The F4
  refusal is the existing `handoff_check:field.blank` refusal, whose door is that the role fills the field.
- The CHANGELOG fragment is not extended yet (scope still open). Proposed sentence: "`handoff_check` refuses a list row that
  still carries the contract's own token value (for example an unfilled author row) as not filled; a list whose rows differ
  takes its field hint from its placeholder row."
- Analogs (rule 5): S6/S7 now hint "the runtime_provenance record" for every blank `inputs_read[].path` row. That is the per-key
  rule's pick and still not the right text for their author rows. `filled_share` (handoff_check.py ~1590) still counts blanks by
  `is_placeholder` only.
- Needed beyond the manifest: handoff_check.py::check, acceptance.py::stage_author_dispatch/awaits_acceptance,
  tests/form_filler.py (_Survey, fill_form), tests/dry_stub.py::fill_handover, tests/fixtures/form-fill-rules.json, role-load.json.
