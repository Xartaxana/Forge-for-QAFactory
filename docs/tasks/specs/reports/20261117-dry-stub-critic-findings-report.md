# t-1088 / FV3-20 - the dry stub's code critic writes its findings file (report)

## 1. Product facts (item 1), file:line in the worktree

- Refusal site: `scripts/controller.py:7743-7750` (`_code_review_problems`): `said = "the qa-code-critic window is not receipted: "`; it reads the accepted dispatch's
  `evidence_refs[].path` and refuses unless some basename, lower-cased, contains `findings` ("no findings file in the accepted evidence (a name containing `findings`, e.g.
  `work/test-code/critic-findings-<your dispatch>.md`)"). Only asked when `work/automation-manifest.json` exists (`:7737`).
- Where the evidence comes from: `story_step.py:1551-1571` `_role_receipts` -> `findings_path.resolve(task_root, dispatch)` (`findings_path.py:60-72`): the file
  `work/test-code/critic-findings-<dispatch>.md` (`findings_path.per_dispatch`, `:31-34`) must EXIST on disk, else the old single file (one window only), else "" = no receipt.
  `brief_pack.OWN_FINDINGS` (`brief_pack.py:80`) is the same path in the brief. `handoff_check._findings_file` (`handoff_check.py:178-196`) derives `review.findings_file` of the form
  from the same resolver (`--fix`), so the file must exist before the stub's `--fix`.
- Content/shape: NO code reader parses the S5 findings file. Name = receipt (controller); `ledger.remarks_carrier` (`ledger.py:1487-1504`) only searches it for a case id as a whole word;
  `driver_stage_s5.s5_author_round` (`:443-457`) reads its first 1200 characters as the repair reason. The charter (`agents/qa-code-critic.md:73,80`) says "your findings file holds
  the roll-call and notes". No verdict word is read from it (`critic_rollcall` / `_declared_review_verdict` read the S4 case critic's file only).
  The stub's file therefore follows the charter: heading, `Verdict: approve`, a roll-call row per instance, notes - and names the instance and the case.
- Divergence from the spec text: none; the spec's "per-test rows, the verdict word" is a charter convention, not a code requirement (stated above).

## 2. What changed

- `scripts/tests/dry_stub.py`: `write_files(..., dispatch)` resolves `<dispatch>` in a `files` path or text (new `DISPATCH_WORD`; KitError naming the key when the call names no dispatch);
  new `check_findings_file` called in `fill_role` before `critic_branch` for a kit's `qa-code-critic@S5`: no file at `findings_path.per_dispatch(dispatch)` (product's own resolver) is a
  KitError naming `qa-code-critic@S5.files["work/test-code/critic-findings-<dispatch>.md"]` (rc 3, the journal row says failed, nothing probed). The file goes through the same
  `files` road as the probe-model file, before the probe and before the form's `--fix`.
- `fixtures/stories/dry-1/story.json`: the `qa-code-critic@S5.files` row `work/test-code/critic-findings-<dispatch>.md`, an approving review of TC-1 / `test_the_case` (data, no text in the stub).
- `fixtures/driver-exits/known_red.json`: row `main/S5` replaced by `main/S6` (below); pin stays 1.
- `changelog.d/dry-stub-critic-findings.md`.
- Selftest: 234 rows (new FV3-20 rows: `<dispatch>` resolved in path and text, two wrong-shape KitErrors, the missing-findings KitError (function and process, rc 3), the file passes the check, the receipt road names the story's file, the review names case/instance; the three existing critic-call rows now carry a findings row of their own in their control, because the call without one is the new KitError).

## 3. What the main pass did after the change

S0..S5 and gate_A PASS; stops at S6 (verbatim head of the stop note, `--part main` and the whole file):
`stopped at S6: the road met the conductor: a state the driver has no move for; its own words: ... exit gate for S6-qa-runner-1 (qa-runner, S6): 21 finding(s): - digest: your final message is not the handoff form. ... the digest names no artifact path ... TC-1 was in this dispatch's scope and has no line ... - handover form S6-qa-runner-1.yaml - scope: no rows ...`
(20 more `handover form S6-qa-runner-1.yaml - <field>: not filled`); `the driver's first refusal: resume S1-qa-scout-1: the person answered what the role stopped for`.
S5 stub journal row: `S5-qa-code-critic-1 ... wrote=6 live_only=0` (the findings file, probe model, probe record, manifest, window record, form).
Classification: stub gap (the filler/stub for S6 `qa-runner`): its stub row says live_only `form s6-runner-to-analyst: a hint inside a value that no context token names and no literal_text row of form-fill-rules.json covers: the filler writes no value it cannot fill (E10)` and `work/evidence/manual/<case>/tried.md: no contract heading`.
Node: kept FV3-20 with a `note` - no node for the S6 runner stub exists in `plans/piles/live-run-fvf/` by grep (grep of `FV3-` rows and `qa-runner`/`s6-runner` in the pile: none) -> **a new finding/node is owed** (Lead).
Group rows that waited on S5: still wait (snapshot S6..S9 not made): `gate_B/{approve,empty,free words,retry,rework,stop}: after:FV3-20: its start snapshot S8 was not made`. None ran red; no group ledger edited.

## 4. FR walk

G: FR-29 no heredoc/control byte (edits by tool); FR-30 English ASCII (changelog, code, story text); FR-31 no load-dependent test added; FR-32 root cause = stub wrote no findings file, test row + green selftest; FR-33 n/a (not a role fix); FR-34 n/a; FR-54 siblings by map: see section 7.
C: a story-kit key (`<dispatch>` in `files`) was added: FR-11 the file is produced by the same tool the role would use (a role's own file, `files`); FR-14 the shape is as the product reads it (item 1); FR-15 the path is given by the product's resolver, never searched; FR-38/FR-39 n/a (no check judging a role). FR-59: a missing row is a named KitError, never an empty file.
A/B/D/E/F: not changed (test stub only).

## 5. Changelog fragment

`changelog.d/dry-stub-critic-findings.md`: one English ASCII bullet (see file).

## 6. Witness (verbatim tails)

```
$ python -B ai-packages/qa-factory/scripts/tests/dry_stub.py --selftest
=== dry_stub --selftest: 234/234 ok ===
$ python -B .../dry_exits.py --selftest
dry_exits selftest: 201/201 cases
$ python -B .../dry_exits.py --check
dry_exits --check: 0 discrepancies
$ python -B .../scenario_walk.py --witness-for <the three tests owns paths>
scripts/tests/dry_stub.py: keep test_scenario_dry_1.py (layer scenario, covers it)
scripts/tests/fixtures/stories/dry-1/story.json: scenario test_scenario_dry_1.py (story dry-1)
scripts/tests/fixtures/driver-exits/known_red.json: keep test_scenario_dry_1.py (layer scenario, covers it)
   (only file printed: test_scenario_dry_1.py; changelog.d and the report are doc paths with no row)
$ ( cd .../ai-packages/qa-factory && python -B scripts/tests/test_scenario_dry_1.py )     [whole, once, after the ledger edit]
PASS dry-1/census ... PASS dry-1/main/S0..S5, gate_A
NOTE dry-1/main/after: after:FV3-20: no snapshot for S6, S7, S8, S9
NOTE dry-1/gate_B/approve|empty|free words|retry|rework|stop: after:FV3-20: its start snapshot S8 was not made
=== scenario dry-1: 10/10 ok ===      exit 0
$ ( cd .../ai-packages/qa-factory && python -B scripts/tests/test_field_producers.py )
PASS known_red: the red rows of the walk are exactly the ledger
=== test_field_producers: 885/885 ok ===
$ ( cd .../ai-packages/qa-factory && python -B scripts/selftest.py --limits --lang )
PASS limits: every mandatory role rule of design/role-rules.json holds in its carrier
=== qa-factory selftest: 4/4 ok ===
```
The first `--part main` run (before the ledger edit) printed `FAIL dry-1/main/known_red - stale: main/S5 is green` and `new red: main/S6`, 7/9: the expected state before relabelling.

Negative control (byte copy): `cp story.json -> scratchpad/story_fv320.orig`, sha256 `241d68d4e9e76ad1ad37b702de6dc54daf24ec1f5a05f49769eabd385c835953` both; key renamed (findings text no longer under the findings path) ->
```
FAIL FV3-20: the story's critic row writes the findings file of its dispatch at the product's path, and the product's receipt road (`story_step._role_receipts`) names it as evidence - expected (True, ['work/test-code/critic-findings-S5-qa-code-critic-1.md']) ...
FAIL FV3-20: the review is an approval that names the instance and the case ... expected (True, True, True, False), got (False, False, False, False)
=== dry_stub --selftest: 232/234 ok ===
```
restored by `cp`, sha256 after: `241d68d4...5953` (equal); selftest 234/234 again. The main-pass S5 refusal was not re-run for the control (6 minutes); the receipt-road row stands for it (`_role_receipts` returns [] -> `controller.py:7746` refuses).
Note: the first control run crashed with FileNotFoundError in my own row (traceback instead of FAIL); fixed (`own_text` read guarded) before the final control above.

## 7. Analogs / siblings (reported, not fixed)

- The S4 case critic's file (`work/test-cases/critic-findings.md`): same road (`files` row of `qa-case-critic@S4` in dry-1 story.json), already written and read by the product's roll-call reader (selftest N2d); checked, same form, nothing to do.
- Other stub roles that hand back a window with no receipted file: the S6 `qa-runner` (this report's new stop: no `scope`, no digest path, no `tried.md`), and the S7 `qa-failure-analyst`, S8 `qa-doc-scribe`, S9 `qa-retro-analyst` rows of dry-1 `story.json` (`walk` lists them; the story holds no `stub` row for them) - not measured, the pass never reaches them.
- `story.json` `files` row `work/probe-models/S5-qa-code-critic-1.json` still hard-codes the dispatch id; `<dispatch>` now works there too (not converted: out of scope).

## 8. Needed beyond the manifest

`scripts/findings_path.py`, `scripts/story_step.py`, `scripts/handoff_check.py`, `scripts/ledger.py`, `scripts/driver_stage_s5.py`, `agents/qa-code-critic.md`, `handoffs/s5-critic-to-automator.yaml`, `references/artifact-writers.json`, `plans/piles/live-run-fvf/batch-3-live-run-fvf.md`.

## 9. Questions

1. The new stop at S6 is a stub/filler gap with no node of its own in `live-run-fvf`: should the Lead open one (the `note` of the `main/S6` row says it is owed)? Row kept on FV3-20 per item 3(a).
