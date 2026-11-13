# t-524 report: P1-a fix round after critic t-521

Worktree `C:\QAFactory\forge-repo\.claude\worktrees\p1a-fix`, branch wip/p1a-fix, commit b5c7765 (pushed; HEAD == origin/wip/p1a-fix).
Spec: `docs/tasks/specs/reviews/20261113-p1a-topic-code-critic.md`.

## One line per item

- B1(a) done: deriver round uses `dataclasses.replace(w.ctx, author_dispatch="S2-author-1", dispatch_id=dispatch)`; forms get cases, minted ids (`_issued` maps TC-1 -> the world's TC-001) and dispatch ids; rule `case-id-of-the-world`. Derive red rows 54 -> 44.
- B1(b) done: world also fills `work/grounding.yaml` and `work/context-manifest.json`, pins the case version (`CV.create_version` + `CV.pin`), runs `sizing.run`; all through product writers, none by hand. Inputs that stay out, with reasons, are the 47 `not_in_world` rows (diff under work/: story-kit input, no writer; pipeline.json; source-inventory; blast-radius/grounding tables need a diff; critic roll-call file: no filler row; probes/provenance/receipts/fingerprints; run-report; ledger/traceability).
- B1(c) done: bugs template has all 8 front-matter fields (+ impact, confirmation, red_test_none, source_draft, cases, requirements); test_file template carries `qa(case=, then=, obligations=["OB-1"])`. Re-measured (below).
- B1(d) done with a stopgap: no `P1A-` id left (`grep -c "P1A-"` = 0). Rows with an existing node carry it (FV1-1, FV1-14, FV1-19, FV1-22). Rows with NO node (P2 x3, P5 x3) carry FV1-14 plus a note "Lead opens one". `known_red.py` refuses `lead-queue` (NODE_RE), unchanged: see questions.
- B2 done: context tokens substituted inside values; other embedded `<...>` is Unfillable unless a `literal_text` row matches (`command-template`, `git-add-prose`). 8 new `unfillable ...` rows are the honest count.
- F1 done: body and file name per language are rows in `form-fill-rules.json` (`languages`, `like` one hop); `language_body` makes a language with no row Unfillable naming it; `_marker_entry(w, written)` reads the file the filler wrote.
- F2 done: `_plan_row_of` row re-attributed (P2, node FV1-14 + note).
- F3 done: manifest world writes the base case via `FF.fill_artifact("case", ctx)`; refusal shows.
- F4 done: `pins` {readers: 19, families: 3}, one count each, checked in the test.
- F5 done: language reader = `FF.test_file_languages` (registry-driven, `languages_source`); environment swap = `_in_project(world)` (N2c refusals now use it).
- F6 done: tool_fields reader rows, `_f_tool_fields` and its FEEDS entry removed.
- F7 done: `covers` of test_field_producers.py gained `references/slices/qa-test-strategist/handoff-keys.md`, `references/ahead-cards.json`, `agents/qa-automator.md`.
- F8 done (measured, nothing cut): see N3 seconds.
- F9 partly returned: (a) RC2-1 `brief_pack.question_answer_lines` exists as a reader but its world needs a question register row (`question_register.record`) and no filler row builds register questions: returned by name, no ledger row added. (b) report_facts search below.

## Ledger before / after

Before: 75 rows, all `P1A-n` ids, no real nodes.
After (known_red 30 + not_in_world 47 = 77 ids walked red; 880 rows walked):

| class | node | rows |
|---|---|---|
| real product defect | FV1-19 | 3 marker (csharp, java, typescript) + 3 obligation (csharp, java, typescript) |
| real product defect | FV1-1 | 2 `case_plan_row` + identity + python/pytest obligation (2) |
| real product defect | FV1-14 | 10 TS-only readers + check_plan_v0 + agree; `_plan_row_of` (P2); derive rows 2 plan_row (P2) + 3 requirements (P5) |
| real product defect | FV1-22 | 2 accept rows |
| world / filler | - (not_in_world) | 47: 2 pipeline, 3 diff, 1 inventory, 11 grounding/blast, 2 roll-call, 7 probes/provenance/receipt/fingerprint, 3 run-report, 3 ledger/traceability, 7 `inputs_read[].version`, 8 unfillable path hints |

Stale rows removed this round (went green): `implementation.source`, 2 size derive rows, 6 case_version/requirements derive rows, `project:bugs/[base]`.

Deviation from "rows stay in the ledger": world/filler rows live in a separate `not_in_world` section of `form-rounds.json`, because the ledger's contract is "defects of main with a node" (shrink-only, node required). The section is printed (`NOT IN WORLD ...`), a green row there is `stale` red, an unknown id is red, and an id in both sections is red. Row removed -> red (negative control below).

## Rows that still need a node from Lead

- P2 x3: `handoff_check._plan_row_of` row, derive `s4-designer-to-case-critic:scope[0].plan_row`, `s4-designer-to-runner:scope[0].plan_row` (the deriver reads front-matter `plan_row:` the case contract does not define; `artifact-contract.md:59-62`).
- P5 x3: derive `...:inputs_read[0].requirements` (s3), `scope[0].requirements` (s3), `filed[0].requirements` (s8) (leaf `requirements` marks code-filled, `_requirements_of` answers only a case row).
- New red rows from this round to confirm: 8 `unfillable ...` rows (filler gap: no context token names an earlier form's or a record's file name) sit in `not_in_world`; the `@python`/`@pytest` obligation rows sit in known_red under FV1-1 (obligation now cited by the marker, case cites minted P-1, `case_plan_row` reads TS-n only).

## N3 layer seconds (F8, in-process, one run)

```
   0.64s  every_required_field_has_a_producer_or_a_declared_gap
   0.00s  the_two_paths_this_walk_wired
   0.17s  the_sensitivity_gap_is_reported_not_hidden
   0.02s  known_red_ledger_cases
   1.18s  form_filler_hint_cases
   8.72s  every_form_fills_from_its_own_hints
   2.79s  every_stage_output_fills_or_is_named
   1.80s  every_reader_takes_what_its_writer_writes
   3.59s  every_derived_field_meets_its_deriver
   0.13s  one_fact_one_form_everywhere
   0.00s  readers_of_one_field_agree
   0.00s  red_rows_equal_the_known_red_ledger
  19.03s  total
```
Script: scratchpad `p_time.py` (not committed). Baseline whole file was 12.8 s here before this round (critic 15.1 s; 0.6 s before the layer); `every_form_fills_from_its_own_hints` dominates. Nothing cut.

## F9(b): report_facts "unadapted readers" search (spec 4.3)

Search `TS-` (case-insensitive) over `scripts/report_facts*.py` (one file); positive control same tool/shape on `validate_artifacts.py`: 17 hits. Result: one real hit, `report_facts.py:1690` (a comment: the plan row speaks as `TS-1`). No literal `TS-` pattern in code. Candidates by name, not built (reads through other modules, needs a feed I cannot judge without product code): `report_facts._manual` reads `meta.get("plan_row")` (lines 1179, 1214) and `_cases` line 817 compares `meta.get("plan_row")` to `p.get("ts")` from `C.parse_plan`. Whether `C.parse_plan` keeps TS-only is not verified.

## Witness (verbatim)

1) `python -B ...\scripts\tests\scenario_walk.py --witness-for <the six owns under ai-packages>` (run in a `( cd worktree && ... )` subshell):
```
scripts/tests/test_field_producers.py: keep test_null_outcomes.py (layer gate_named, covers it)
scripts/tests/form_filler.py: keep test_field_producers.py (layer data_join, covers it)
scripts/tests/known_red.py: keep test_field_producers.py (layer data_join, covers it)
scripts/tests/fixtures/form-rounds.json: keep test_field_producers.py (layer data_join, covers it)
scripts/tests/fixtures/form-fill-rules.json: keep test_field_producers.py (layer data_join, covers it)
scripts/tests/test-layers.json: keep test_selftest_shard.py (layer table, covers it)
scripts/tests/test-layers.json: keep test_selftest_slow_tests.py (layer table, covers it)
```
2) The tests it names, run with `python -B <abs path>` (tail):
```
## test_null_outcomes        === test_null_outcomes: 337/337 ok ===
## test_selftest_shard       === test_selftest_shard: 95/95 ok ===
## test_selftest_slow_tests  === test_selftest_slow_tests: 123/124 ok ===
## test_field_producers      known red rows 30, rows walked 880
                             === test_field_producers: 890/890 ok ===
```
The one failure of test_selftest_slow_tests, verbatim:
`FAIL test-layers.json on the REAL file: every keep row covers the helpers it imports and its owned fixture — ['test_app_card_stand_lessons.py: tests/test_app_card.py', 'test_place_of_draft_observation.py: tests/test_place_answers.py']`
These two rows are not touched by this diff; not verified on the base commit (estimate, not verified: it predates this round). Not mine to fix (owns exclude them); the fix is one `covers` entry each.

3) `grep -c "P1A-" form-rounds.json`: Grep tool count on the file: no matches (0). Control: same tool on the same file for `^(NOT IN WORLD|KNOWN RED|FAIL)` over the run output counted 77 lines, so the invocation form works.

4) Negative control (byte copy first, restore from it, hash compared). Hash before: `048068588523c5b88e125fc7344b9aecf8f873f337721e463fec4ca2e4b66d02`. Deleted the `known_red` row `agree: plan-row id`:
```
FAIL agree: plan-row id — 1 readers accept it (...) and 13 refuse it (...)
FAIL new red: agree: plan-row id — new red: agree: plan-row id — fix it, or add "agree: plan-row id": {"node": "<FV1-n or node id>", "raised_by": "..."} to scripts/tests/fixtures/form-rounds.json known_red
FAIL known_red: the red rows of the walk are exactly the ledger — 1 problems
=== test_field_producers: 888/891 ok ===
```
Restored from the copy; hash after: `048068588523c5b88e125fc7344b9aecf8f873f337721e463fec4ca2e4b66d02` (equal); the run above (890/890) is on the restored file.

## Commit gates

Commit b5c7765: pre-commit passed with WARNs only: "(d) tracked package file ... matches no feature" for form_filler.py, known_red.py, form-rounds.json, form-fill-rules.json (and 3 files not in this diff). Commit message carries `architecture: AR-22 ...; AR-20 ...`, `judgment: none -- ...`, `axes: not a mechanism (...)`.

FR walk (package diff is under tests/ only): A refusals - not changed; B - no human text changed; C - C12/C13: closed variety (languages, literal text) moved into data rows (`form-fill-rules.json`); G - FR-30 English only, Cyrillic grep over the six files = 0 (control on PROJECT.md: 364).

## Questions

1. `known_red.py` refuses `lead-queue` as a node (NODE_RE), unchanged per spec. 6 rows (P2 x3, P5 x3) use node FV1-14 + a note as a stopgap. Lead: open real nodes, or allow `lead-queue` in the ledger?
2. `not_in_world` is a new section (deviation from "rows stay in the ledger"); confirm the shape, or say where those 47 rows live.
3. F9(a) RC2-1: world needs a question register row; no filler row for register questions. Needs a filler row / product writer decision.

## Analogs noticed (not fixed)

- `validate_artifacts.check_plan` legacy sits next to `check_plan_v0`.
- `_f_case_levels` takes a `value` input it never uses.
- `every_stage_output_fills_or_is_named` is ~420 lines: split is queued, not done.
- P6: `requirements-readiness` is a verdict-less acceptance.
- `test_app_card_stand_lessons.py` and `test_place_of_draft_observation.py` rows of `test-layers.json` miss helper covers (the failing row above).
- Feature registry: 4 files of this diff match no feature (pre-commit WARN, door (d)).

## Needed beyond the manifest

`docs/tasks/specs/reviews/20261113-p1a-topic-code-critic.md` (in root checkout, not the worktree); `scripts/report_facts.py`, `scripts/validate_artifacts.py` (search); `scripts/known_red.py` NODE_RE.
