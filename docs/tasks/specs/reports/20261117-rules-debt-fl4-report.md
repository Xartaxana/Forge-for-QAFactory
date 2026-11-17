# Builder report - card FL4 (t-1050, F19): the S7 rework door for a case-less bug candidate (FR-22)

Branch: worktree-agent-ab0738c6a4bd8d773. Spec: docs/tasks/specs/20261117-rules-debt-phase2-s9-fl-cards-spec.md section 3b.

## Status

Card items 1-8 done and tested. ONE witness file is red and is returned as a question (not forced): `test_role_load.py` K10-b / K10-c, because the one line the
card adds to `agents/qa-failure-analyst.md` grows that role's process text over its shrink-only ratchet (details and question below).

## Step 0 (before any edit)

(a) lazy imports make no cycle:

    $ python -B -c "import sys; sys.path.insert(0, r'<wt>/ai-packages/qa-factory/scripts'); import controller, check_delivery, no_move; print('ok')"
    ok

(b) scratchpad copy of cart-1, `check_delivery._grounding_candidates(<copy>)`:

    ([{'ref': 'R-13', 'requirements': ['R-13'], 'subject': 'Cart page with an emptied quantity input or a failed cart/book fetch: expected behaviour is not stated (code sends NaN, no response.ok check) (MyBooks/src/components/pages/CartPage.tsx:65)', 'source': 'register'}], [])

R-13 present, unreadable == []: the test world holds (F15). Step 0 passed as the card describes.

## What was done (by card item)

1. `check_delivery.bug_candidates(artifacts) -> (candidates, unreadable)` and `candidate_refusal(refs, known, unreadable) -> str` (new, public, after `_grounding_candidates`; nothing else of the file touched).
2. `Controller.build_rework_request(..., candidates=None)` + `main` rework `--candidates` (comma split, same as `--cases`): rules of 3b.5 (S7 + S7 author via `acceptance.stage_def_of("S7")["roles"][0]`; with cases/rows refused; refs outside `bug_candidates` refused with Rule R text; `sent_back` lookup skipped; case refusal now `not wanted and not wanted_candidates`; `request["bug_candidates"]` = sorted distinct refs). All problems join `problems` and go out through `_raise_all`; no direct raise was added.
3. `BINDING_KEYS` gains `bug_candidates`.
4. `no_move`: `ARGS_KEYS` + `candidates`; `rework_args_list` prints `candidates (S7 only, instead of cases): ...`; `check_args` per 3b.5 (candidate branch after stage/role rules and before the "names no case" rule; `check_delivery` imported inside the branch only). `driver_conductor.no_move_facts`: one call of `CD.bug_candidates(self.task_root)` in its own try giving `candidates` and `candidates_unreadable` (both `None` on a raise).
5. `driver_machine.seam_rework_step` passes `candidates=`; `driver_dispatch.Driver.rework(candidates=())` adds `--candidates a,b` when non-empty.
6. Packet readers: `inject_context.PACKET_DISPATCH_KEYS`, `story_step._packet_lines` (line `Bug candidates of this dispatch: ...`), `story_step.IDENTITY_FIELDS`, `brief_pack` rework head (same line).
7. Text carriers: `conductor-actions.json` (row 8 "(`--candidates <its ref>` instead of `--cases`)", `rework_stage.run`, `args`, `precondition`), `controller-api.md` (one sentence), `qa-failure-analyst.md` (one line), `s7.md` (one sentence in "No repair").
8. Census: ONE reclassification, `no_move.py` / `check_args`: `shape -> xref` (+1 xref, -1 shape); NO row added (F17: `build_rework_request`, `bug_candidates`, `candidate_refusal`, `no_move_facts` are not census units; `build_rework_request` has no direct raise, so C1 does not name it). Ratchet: `xref`/`shape` have no ceiling.
9. Tests (existing files only, no new file): `test_check_delivery.py::fl4_candidate_rows`, `test_controller_rework_window_words.py::fl4_candidate_rework` (CLI rows (i), (vi); builder rows (ii)-(v), (vii); E3, E5-E7, E10, E11 battery; `check_args`, `rework_args_list`, `no_move_facts` rows; BINDING_KEYS + `_relaunch_packet`; `_packet_lines`), `test_exploratory_answers.py::fl4_seam_rows` (seam carries candidates; `Driver.rework` arguments `--candidates R-13,K-1`, no `--cases`; old record: none).
10. `design/controller-blocks.md` regenerated (the generator's check said 3 new blocks; see witness).
11. Changelog fragment `ai-packages/qa-factory/changelog.d/rules-debt-fl4-candidate-rework.md`.

## Witness

### DoD command

    $ python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/check_delivery.py
    (30 lines: scenario test_scenario_cart_1 / local_1_0108 ..., keep rows test_check_delivery.py, test_third_verdict.py, ... )

The walker was run for ALL owned code, reference, text and census paths in ONE call (492 lines, 163 distinct test files). Of those, the 72 files that
`slow_tests.json` measures at <= 10 s were run, 6 in parallel, each as `python -B ai-packages/qa-factory/scripts/tests/<file>` from the worktree root:

    72 files run; 70 rc=0 (each ends "=== <name>: N/N ok ===")
    FAIL test_controller_blocks.py 370/372  (cause: controller-blocks.md not regenerated; FIXED, see below)
    FAIL test_role_load.py 184/186          (cause: the analyst md grew; NOT fixed, QUESTION 1)

After regenerating `design/controller-blocks.md`:

    $ python -B ai-packages/qa-factory/scripts/tests/test_controller_blocks.py | tail -1
    === test_controller_blocks: 375/375 ok ===
    $ python -B ai-packages/qa-factory/scripts/tests/test_judgment_census.py | tail -1
    === judgment_census: 25/25 ok ===       (C1 and C3 hold after the one reclassification)

The 91 slow files of the walk (incl. `test_check_delivery.py`, `test_controller_rework_window_words.py`) are judged by the batch canon. The row FUNCTIONS added to
slow files were called directly from a scratch script (`scratchpad/call_rows.py`, which imports the test module and calls the one function):

    window  -> fl4_candidate_rework: "=== scratch-window: 42/42 ok ===" (all PASS; sample: "PASS FL4 (vii)/E7: the unreadable table is named and the ref is 'not known'",
               "PASS FL4 item 4: the conductor's text after the args prefix is the controller's text, one builder", "PASS FL4 item 3: a relaunch packet of that record carries it")
    delivery-> fl4_candidate_rows: "=== scratch-delivery: 7/7 ok ==="
    seam    -> fl4_seam_rows: "=== scratch-seam: 4/4 ok ===" (test_exploratory_answers.py is not slow and also passed whole in the 72)

(The window rows were re-run once more after the Cyrillic fix below: 42/42.)

### Other checks

    $ python -B tools/architecture_index.py --check
    architecture index: up to date (29 invariants, 2682 bytes)
    $ python -B tools/controller-blocks-gen.py ai-packages/qa-factory/design/controller-blocks.md
    355 blocks: caller 105, command 220, person 17, unpassable 13   (3 new `build_rework_request` ValueError rows, all `caller`)
    $ ( cd ai-packages/qa-factory && python -B scripts/selftest.py --lang )
    PASS lang: no Cyrillic anywhere in the package
    PASS lang: no control byte left by an eaten escape sequence (FR-29)
    === qa-factory selftest: 2/2 ok ===

DOC-DISPATCH key run (item 7; keys quoted verbatim from the card before the run; script `scratchpad/dockeys.py`, full source below):

    RUN: PASS
    NEGATIVE CONTROL (one key absent): reports failure -> ["MISSING 'KEY-THAT-IS-NOT-THERE' in references/controller-api.md"]

    PRESENT = [("references/conductor-actions.json", "--candidates <its ref>"), ("references/controller-api.md", "--candidates"),
               ("skills/qa-story/phases/s7.md", "--candidates"), ("agents/qa-failure-analyst.md", "code-reading")]
    ABSENT  = [("references/conductor-actions.json", "the rework names any case of the approved scope")]
    run(): for each PRESENT key, fail if not in the file; for each ABSENT key, fail if it is in the file; the control appends one never-present key.

`"candidates"` Grep over `no_move.py` after the edit: lines 191 (`ARGS_KEYS`), 220 (`rework_args_list`), 247-278 (`check_args`) only, as card 3b.4 expected.

## FR walk (package diff)

- A: FR-1/FR-2 - every new refusal says what is wrong, what was expected (the known refs, `--cases`/`--rows`) and a door; FR-46 - all are `ValueError` (the call's fault); FR-4 - nothing silent is let through (a ref is accepted only when the code read it); FR-3 - the unreadable-input text is the factory's own defect text, the person is not asked to fix the file (E13).
- B: text shown to a person - not changed (the person's words travel unchanged by `--words-file`; the new refusals are caller/conductor text).
- C: FR-11 - the analyst is told the field it must act on (packet, prompt, brief, charter line); FR-14 - the request shape grows one optional key, old shapes read as before; FR-38 - the requirement reaches the role in the brief and in `qa-failure-analyst.md`; FR-42 - the state "candidate, no case" now has a move; FR-39 - no guard change needed (the rework is `controller.py`'s own door); FR-49 - what the packet carries reaches brief and prompt.
- D: FR-59 / AR-28 - an unreadable input is "not known", never "is a candidate" nor "is not a candidate" (E7, rows (vii) and item 4); FR-16 - refs are checked against the reader at the moment they are stored.
- E: FR-22 - the road to a bug no longer borrows a case (`conductor-actions.json` F7 text removed); FR-37 - the command text in `conductor-actions.json` equals the command `controller.py` takes.
- F: FR-41 - an unknown candidate is never reported as absent (`candidate_refusal` says "not in this story" only when every input was read).
- G: FR-30 English only (selftest --lang green); FR-29 no escape bytes in code (the Cyrillic test ref is written `chr(0x431)`); FR-54 siblings by the map below.

## Architecture (AR-n)

AR-9 refusals name expected refs + door; AR-13 one reader (`bug_candidates`) and one refusal text (`candidate_refusal`); AR-19 stage twins `--rows/--cases/--candidates` change together, `ANSWER_REWORK_OWNERS` untouched; AR-20 the census class move is named (check_args shape -> xref, +1 xref -1 shape, no row added); AR-22 producer (`build_rework_request`, `Driver.rework`, `seam_rework_step`, `check_args`) and every reader (BINDING_KEYS, PACKET_DISPATCH_KEYS, `_packet_lines`, IDENTITY_FIELDS, brief head, `no_move_facts`) in ONE commit; AR-25 the state "candidate, no case" has a move; AR-28 unknown never becomes a pass or an absence.

Census statement: one reclassification, `no_move.py` `check_args` `shape -> xref`; no row added (F17).

## Deviations from the card / spec text (all small, for acceptance)

1. `check_args`: card item 4 / E11 asks "nesting (a list inside `candidates`) -> not lists of ids", but the shared `clean()` stringifies elements, so `[["R-13"]]` would have read as the string `"['R-13']"`. I added a stricter test for `candidates` only (a non-string element -> `None` -> the "not lists of ids" refusal); `cases` / `rows` keep `clean` byte for byte. The one message text changed accordingly: `"args" cases / rows / candidates are not lists of ids` (the old text for the cases/rows case contained "cases / rows are not lists of ids"; a Grep over the repo found no pin on it).
2. `rework_args_list`: when `candidates` is an empty list and nothing was unreadable, the line prints `none` (the spec gives no text for the empty list; `(not read)` would claim an unknown). Spec silent: flagged as an edge I filled.
3. `no_move_facts` row was placed in `test_controller_rework_window_words.py` ("in the same file" of item 4), with a `Driver` built by `object.__new__` and `check_delivery.bug_candidates` patched; the seam row went into `test_exploratory_answers.py`.
4. For a call with candidates and a non-S7 stage the controller prints the stage/role refusal AND the membership refusal (all problems are raised whole, K1 rule); not a problem, noted.
5. `Driver.rework` row: tested with the controller faked (records the arguments, then returns no id so `ReworkRefused` ends the call); the real-process path is covered by the CLI rows (i) and (vi).

## Commit state: STALE (attempt 1; the Lead committed it as 13c4a757; attempt 2 is below)

All files are STAGED on the worktree branch (`git add` of `ai-packages/qa-factory` and this report; commit message ready in the scratchpad, carrying the
`architecture:`, `judgment:` and `axes: not a mechanism (package change, card FL4)` lines and the attribution). `git commit` was refused by the pre-commit hook:

    factory rules index: up to date (59 rules)
    factory rules index is stale: run python tools/factory_rules_index.py and stage docs/OWNER_PRINCIPLES_INDEX.md

Positive check that it is not caused by this diff: `python -B tools/factory_rules_index.py --check --row P` prints the same "stale" line with rc=1, and this diff touches
neither `docs/OWNER_PRINCIPLES.md` nor its index. The fix (regenerate and stage `docs/OWNER_PRINCIPLES_INDEX.md`) is outside my owns, so I did not do it; it may also be a
line-ending artifact of this Windows worktree (git warned "LF will be replaced by CRLF"). Not verified which. Question 2 below.

## Questions (returned, not decided)

2. May I regenerate and stage `docs/OWNER_PRINCIPLES_INDEX.md` (outside the owns) into this commit, or does the Lead fix the stale index on main first? Until answered the commit is not made.

1. `test_role_load.py` K10-b/K10-c is red: `qa-failure-analyst carries 20,306 process tokens, over its shrink-only process ratchet 20,261` (+45 tokens, from the ONE line the card adds to `agents/qa-failure-analyst.md`, item 7). `references/role-load.json` is not in my owns, and a ratchet raise must be named in a verdict (AR-20). Options for the Lead: (a) raise `process_ratchet_tokens` for qa-failure-analyst to 20,306 in this commit (add `role-load.json` to owns and name the raise), (b) offset by trimming 45+ tokens of existing process text of that role, (c) place the line in a section marked `<!-- kind: craft -->` if the Lead judges it craft. I left the line in place and changed nothing else.

## Siblings / analogs noticed (not fixed)

- Axis 5: the S1-S3 `--rows` and S4+ `--cases` spellings are checked again in the two judges and in `answer_pairs_owed` (unchanged, as the card says); `rework_args_list` now lists three spellings, `controller-api.md:19` still shows only the `--cases` example line.
- `conductor-actions.json:71` run text and `s7.md:130/:140/:249/:258` mention `--cases` for the gate-B bug road, which has a real case (EXPLORATORY_REWORK) - unchanged on purpose (non-goal).
- `controller.py` `Controller.build_rework_request` is now ~190 lines; a clone/size ratchet may notice (no tool run here).
- The generator `tools/controller-blocks-gen.py` treats ANY first argument as an output path (`--check`, `--help` write files with those names); I ran it with `--check` and `--help` once each and deleted the two stray files (`./--check`, `./--help`); they were never staged. Class: a CLI with no flag parsing.

## Needed beyond the manifest

`ai-packages/qa-factory/scripts/slow_tests.json` (to split fast/slow files of the walk), `ai-packages/qa-factory/design/controller-blocks.md` and `tools/controller-blocks-gen.py` (regeneration, named in the card), `ai-packages/qa-factory/references/role-load.json` (read for the question), test helpers `harness.py`, `test_controller_state.py`, `controller_rework_common.py`, `test_story_step_manual_block.py`.

## Live proof owed (FR-33)

A `live-runs` row: "a person's gate B words 'this needs a bug report (K-n/R-n)' send the analyst to S7 with `--candidates`, a draft is written, gate B lists it, the reporter files it". Not run here.


## Fix round (attempt 2) - t-1050, after critic t-1059

Tree `.claude/worktrees/agent-ab0738c6a4bd8d773`, from head 13c4a757. One commit, not pushed. `docs/OWNER_PRINCIPLES_INDEX.md` left unstaged (generator drift).

### One line per finding

- B1: `references/controller-api.md` 12133 -> 11997 bytes (cap 12000, not raised). The `--rows` and `--candidates` sentences are one (`Instead of --cases: S1-S3 (no cases) --rows TS-3, plan rows (plan_rows); S7 --candidates K-n,R-n, bug candidates (bug_candidates)`); wording trimmed in the same paragraph only ("such a stage" -> "it", "Rework is X, which takes" -> "X takes", "it misses after a session change" -> "it misses across sessions", "instead of lowering it" -> "(not lowering it)"); no fact lost. Witness: `selftest.py --limits` green.
- F1: `scripts/driver_conductor.py` answer template (`"cases": [...] | "rows": [...] | "candidates": ["<ref>", ...]`) and `references/conductor.md:94` (`"cases"|"rows"|"candidates"`). conductor.md 11897 -> 11910 bytes, under its cap.
- F2: `references/conductor-actions.json` row 8 `run`: `[--rows <ids> | --cases <ids> | --candidates <refs>]`.
- F3: (a) `check_delivery.BUG_CANDIDATES_LINE` beside `bug_candidates` (refs placeholder, the K-n/R-n parenthetical, "for each, a bug draft in the code-reading form, or the reason in your digest why no bug is owed"); read by `story_step._packet_lines` and the `brief_pack` rework head (lazy `import check_delivery`; the brief adds its final "."); (b) the FL4 line removed from `agents/qa-failure-analyst.md`; (c) `role-load.json` `process_ratchet_tokens.qa-failure-analyst` 20306 -> 20261 (`test_role_load.py` 186/186 at 20261, E5 satisfied); (d) the `code-reading` key is asserted on the packet-line row (`FL4 item 7/F3`). E2: no check pins the removed charter line (grep of `Bug candidates of this` finds only check_delivery and the FL4 test; `test_charters_s5_s9.py` pins `evidence: "code-reading"` of line 81, which stays).
- F4: `check_delivery._grounding_candidates`: (a) `missing` counts as "no table" only when nothing exists at `C.artifact_write_path(artifacts, "grounding.yaml")`; a folder / OSError path -> `the grounding table` unreadable; (b) register text with no `## Register` table (`C.md_table` empty) -> `the requirements register` unreadable; (c) `C.candidate_marks()` empty -> `the candidate marks of the vocabulary` unreadable (returns before any ref is derived). The decision is made inside the reader, before `bug_candidates` or the judges compare any ref with the known list (the positional invariant); no file at all stays silent. Rows: `FL4 F4 E1`, `(a)`, `(b) + E6` (both names, stable order), `(b)`, `(c)`, `control` in `test_check_delivery.py::fl4_candidate_rows`.
- F5: rows in `fl4_candidate_rework` (controller file): `FL4 E4` + its control (S7 consumer-reject record, acceptor `qa-doc-scribe`, reject of dispatch dS7-fb with scope TC-1; the case call gets scope TC-1, the candidate call gets `[]`), `FL4 E12` (`rerun_after {'stages': ['S8'], 'reviews': [], 'decisions': []}`, `person_words True`, `scope []`; none without words), `FL4 adversarial` R-1 and K-1 (cart-1 current-code table) refused "not in this story", item 4 compares to `text_vii` itself, the weak E2 row replaced by `FL4 E2` (`story_step._check_packet` with a packet differing only in `bug_candidates` is refused naming the field; control: an identical packet shows no drift), item 6 compares the packet line with `BUG_CANDIDATES_LINE.format(...)`, E3 absence row kept (`FL4 item 6/E1/E3`).
- N1: the K-n/R-n parenthetical is typed once (the constant).
- N5: `story_step materialize` echo gains `; bug candidates R-13` beside `; plan rows ...`.

### Verbatim runs (from the tree; subshell form)

- `( cd <tree>/ai-packages/qa-factory && python -B scripts/selftest.py --limits --lang )` -> `PASS limits: SKILL.md / agents / references within size caps`, `PASS limits: every mandatory role rule of design/role-rules.json holds in its carrier`, `=== qa-factory selftest: 4/4 ok ===` (run after all package edits).
- `test_role_load.py` -> `=== role_load (the one measure of a role's start load): 186/186 ok ===`; `test_exploratory_answers.py` -> `=== test_exploratory_answers: 111/111 ok ===`; `test_judgment_census.py` -> `=== judgment_census: 25/25 ok ===`; `tools/architecture_index.py --check` -> `architecture index: up to date (29 invariants, 2682 bytes)`.
- `test_check_delivery.py` and `test_controller_rework_window_words.py` are in `scripts/slow_tests.json` (60.5 s / 82.5 s): ran only the FL4 row functions, as attempt 1 did: `fl4_candidate_rows` -> `=== fl4 check_delivery rows: 14/14 ok ===`; `fl4_candidate_rework` -> `=== fl4 controller rows: 50/50 ok ===`.
- `scenario_walk.py --witness-for <the owned code, reference and test paths>` named 55 non-slow files plus slow ones. Run, all green with the totals each prints: the 55 non-slow files, among them test_ahead_cards 253/253, test_case_key_identity_join 154/154, test_codex_tool_guidance 217/217, test_conductor_stop 48/48, test_delivery_ownership 310/310, test_dispatch_identity 114/114, test_driver_stop_record 255/255, test_exploratory_answers 111/111, test_first_look_briefs 261/261, test_flow_requests 93/93, test_human_questions 651/651, test_null_outcomes 327/327, test_role_load 186/186, test_scenario_walk 95/95, test_scenario_world 33/33, test_stage_cards 163/163, test_then_remainder 354/354, test_whole_list_sites 292/292; the pytest-style ones: test_brief_s3_roster 12 passed, test_login_need 33 passed, test_probe_marker_judgment 46 passed, test_probe_not_proved 47 passed, test_triage_identity OK, all exit 0. NOT run: the slow files it names (81 of them, among them test_check_delivery, test_controller_rework_window_words, test_brief_pack, test_scenario_cart_1, test_story_step_start, test_no_move_seam_*, test_conductor_doors): judged by the batch canon.
- Negative controls (byte copies in the scratchpad, restored; sha256 before = after):
  - (i) `and not wanted_candidates` removed from the `sent_back` condition: `FAIL FL4 E4: with --candidates the same record gives no scope: the consumer-reject lookup does not run - expected ([], ['R-13']), got (['TC-1'], ['R-13'])`, `=== control i: 49/50 ok ===`; controller.py sha256 `265f26b971850e52...` before and after.
  - (ii) the F4 (a) branch (`or C.artifact_write_path(...).exists()`) removed: `FAIL FL4 F4 (a): ... expected (['R-13'], ['the grounding table']), got (['R-13'], [])` and `FAIL FL4 F4 (b) + E6: ... got ([], ['the requirements register'])`, `=== control ii: 12/14 ok ===`; check_delivery.py sha256 `ad9a737023c008bb...` before and after.
- Same verdict at head 13c4a757 (archived copy) and now: `stage_joints.py --check` -> `stage joints: clean` (both; summary line identical: rows 267, gaps 4, joints held 4 of 267); `contract_slices.py --check` -> `slices: 44 declared, all present and fresh; 19 key pages; 12 charters carry a generated digest line` (both); `gate_registry.py --check` -> first line `A26 gate registry: no violations`, 18 lines (both); `tests/dry_exits.py --check` -> `dry_exits --check: 0 discrepancies` (both, 12 lines). `controller.py` is untouched, so `controller-blocks.md` is not regenerated.

### FR walk

- A (refusals): FR-1, FR-2 - the refusal for an unreadable input names it and the door (`record the input, then ask again`), never "not in this story" (F4 rows); FR-46 unchanged (`ValueError`, the call's fault); FR-57 n/a.
- B (text to a person): not touched; the refusals go to the conductor and the controller's caller, `BUG_CANDIDATES_LINE` to the analyst role; no person-facing text changed.
- C (contracts): FR-10 - one prompt shows one form of `args` (F1) and row 8's command text carries the flag its `says` names (F2, FR-37); FR-38 - the analyst's requirement reaches it on the packet line of the dispatch that needs it (F3); FR-14 - the request and packet shape is unchanged since attempt 1; FR-49 - the field travels whole as before.
- D (identity, evidence): FR-59 and FR-41 - an unreadable source (a path that is no file, a register with no table, an unreadable vocabulary) is named as unknown, never as absent; FR-58 n/a.
- E (delivery): FR-22 - the road to a bug for a case-less candidate is unchanged; FR-37 - the paths and flags named in text equal the code.
- F (measurement): FR-41 holds as in D; others n/a.
- G (code): FR-30 - package files English/ASCII (selftest `--lang` green); FR-32 - a row per finding, with two negative controls; FR-54 - siblings walked (below).

### Architecture statement

AR-10 (the requirement reaches the role before the work, on its packet line), AR-11 (the standing charter pays nothing: ratchet back at 20261), AR-13 (one reader and now one packet-line text, `BUG_CANDIDATES_LINE`), AR-19 (rows/cases/candidates alike at every carrier, below), AR-20 (the ratchet raise reverted, no cap raised), AR-22 (the args form carriers move with the producer), AR-28 (an unreadable source is never "not in this story"). Judgment: none - refs are compared with data; no role's judgment judged.

### Twins and siblings (E7, AR-19)

- Touched `candidates` sites against their `rows`/`cases` twins: the conductor answer template and conductor.md now list all three; row 8 `run` lists `--rows | --cases | --candidates`; `moves.rework_stage` run (line 71) lists `--cases | --rows | --candidates` - the same three flags in a different ORDER than row 8 (not changed: order only, both complete). The brief head and `_packet_lines` print the `Plan rows ...` and `Bug candidates ...` lines in the same place; the `materialize` echo prints `plan rows` then `bug candidates`.
- Asymmetry found, not fixed: the `Plan rows of this dispatch` line is still typed twice (story_step and brief_pack), the same duplication as N1, outside FL4.
- Wording nit noticed: the F4 (c) name `the candidate marks of the vocabulary` reads "factory: the candidate marks of the vocabulary exists and could not be read ..." in `grounding_records` (verb agreement of a shared template).
- N2, N3, N4 of the verdict: not touched (non-goals).

### `grounding_records` ("Left with you") in the F4 states (it reads the same reader; its code is unchanged)

Measured on a scratchpad copy of cart-1: (a) grounding.yaml a folder -> one `factory_record` ("factory: the grounding table exists and could not be read, so its bug candidates are not known to be covered") plus the `bug_candidate` line of R-13; before this round the table was silently absent here. (b) register heading misspelled -> one `factory_record` for the requirements register and no candidate lines; before: nothing.

### Commit

Message lines: the `architecture:` line as dispatched, `judgment: none -- refs are compared with data; no role's judgment judged`, `axes: not a mechanism (fix round of an accepted card)`, `tests-over: rows per finding of critic t-1059`. On a "factory rules index is stale" refusal: reported verbatim in the digest, left staged.
