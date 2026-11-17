# TBW siting card: the conductor's launch section tells every check of every launch (t-1096, node told-before-work/1/TBW1-11)

Status: DRAFT for Lead acceptance (designer). Closes N1 and N2 of verdict t-1091
(`docs/tasks/specs/reviews/t-1091-tbw-t9c-code.md`). Parent: finish spec `docs/tasks/specs/20261117-told-before-work-finish-spec.md`
(§1, §6 "common", card T9c, "Lead decisions on T9c at the build"); row drafts: `20261113-told-before-work-wave0-rows-part3.md` §1
(accepted t-489, F-P1/F-P2/F-P3 (a)). Code read in the T9c tree `W = C:/QAFactory/forge-repo/.claude/worktrees/agent-a8e7e4c769ef59136`
(HEAD with the F1-F5 fix round applied in the files read: `no_move.py` already has `DV.refusal("no_move:prose", "the question is
empty")`, `stage_joints.read_rows`, the F1/F2 row wordings). `PKG = ai-packages/qa-factory`. Function names are load-bearing,
line numbers are of W at read time and are re-located by the builder with Grep. Forks are in §9 and decided nowhere here; the
card is executable by the recommendations.

---

## §0 What the node delivers, in one paragraph

(N1) Fourteen command rows plus `planning_contract:plan.unmarked_revision` land in `references/stage-joints.json`, each with a
literal `DV.refusal("<id>", <same text>)` at its refusing site, so `told_ratchet.unsited` does not rise and `rows_for("conductor",
…, {"moves": open_ids})` lists each row in the launch section whenever its move is open. (N2) The section is rendered by ONE
function for all three driver conductor launches (`Driver._conductor_text` via `moves_section`, `Driver.no_move_legacy`, the S8
delivery in `driver_stage_s8s9`), each launch passing the answer tokens it is judged by, so a launch lists only the rows whose
`when` fits it; the class requirement keeps ONE wording (the row's) and `references/conductor.md:99` stops wording it a second
time; the S8 launch gets rows for the two things code reads of its answer (`action`, `mr`).

---

## §1 Architecture, owners, census (rule 10, AR-29, P27)

| AR | touched how | kept how | change check in the DoD |
|---|---|---|---|
| AR-10 a check's requirement reaches the role before the work | the three conductor launches list the rows of what will judge the answer and the commands of the open moves | one section renderer, rows selected by `when` against the launch's own answer tokens and open moves | `launch-section/*` table rows (B) per launch kind; `contract_slices.py --check` clean |
| AR-9 every refusal names what it expected and a door | 15 command/plan refusals get the row id on their Record (`expected`/`door` from the row) | text byte-identical (EC-1); the Record carries the rest | per-site table rows (A): text equals the OLD file's output AND the id the Record carries |
| AR-15 one survivor, wired everywhere | the section had one caller (`_conductor_text`); now `no_move.checks_section` is the one renderer and three launches call it | `moves_section` calls `checks_section`; no second heading, no second selection | critic: grep `WHAT_CODE_CHECKS` writers = 1 (`checks_section`) |
| AR-17 one seam to the conductor | the S8 delivery is the ONE named exception (`audit_factory.CONDUCTOR_SITES`, `Driver._ask_conductor` docstring); `no_move_legacy` is inside the seam | the S8 launch gets the section through the same helper, it does not become a second seam; `CONDUCTOR_SITES` unchanged | `audit_factory` A27 green in the canon (unchanged sites) |
| AR-13 a fact with a reader is read through it | rows read only by `stage_joints.read_rows` / `rows_for` / `told_line`; Records only by `DV.refusal` | no new reader of stage-joints.json | critic: no `json.load` of stage-joints in the diff |
| AR-1 closed variety is a data row | the new answer tokens (`conductor_options`, `delivery_answer`) | added to `when_kinds` (data); the conductor's selector tuple names them once in `stage_joints.py` beside `CAPABILITY_TOKENS` (its precedent) | `stage_joints.py --check` K3 green |
| AR-20 shrink-only ratchets | rows pin, `fixtures/driver-exits/gates.json` `unwalked` credit | every move named with old → new and reason; `told_ratchet.unsited` does NOT rise | ratchet lines in the report |
| AR-22 field read ↔ producer | new facts key `answer` | produced by the three launch callers, read by `_row_holds` | table rows per launch kind |
| AR-28 an unknown never becomes a pass | NOT KNOWN on an unreadable rows file | kept on all three launches (one renderer) | `UNREADABLE_ROWS` rows extended to the legacy and S8 callers |
| AR-29 code judges data | no check is added or moved | ids attach to existing refusals; the S8 rows tell two existing shape readings of code | "census: no new blocking unit" |

Checks added or altered, owner and census class (AR-29, P27):
- The 15 sited refusals (§3): no check added; each existing refusal gets an id. Owner: data (the call's or the plan's shape: options
  present, values in closed lists, files readable, a recorded pass present). Census class: unchanged per unit (the units are
  `controller.py::build_rework_request`, `::validate`, `::release_dispatch`, `::main`, `waiver.py::main`, `::record_refusals`,
  `::run_stage`, `source_exclusions.py::main`, `stage_done.py::parse_sets`, `planning_contract.py::gate_plan_errors`; their classes
  are read from `scripts/tests/fixtures/judgment-census.json` at the build and not changed).
- `no_move:class` site on the legacy road (`Driver.pass_to_person`): an existing check (`person_owned.question_rule`) gets the id it
  already has on the moves road. Owner: data (presence of a class id from a closed list and of a non-empty `checked`); judgment of
  whether the question really is the person's stays the conductor's, accepted by the person (P27). Census class unchanged.
- S8 rows `driver_stage_s8s9:delivery.action` / `.mr` (§4): tell two existing code readings of the answer: `action` in a closed list
  (else the person is asked), `mr` of the shape of a record (`driver_core.mr_record`; else the `mr` order is called off). Owner:
  data (shape). Census class: shape; whether `mr_record`'s unit has a census row is measured at the build (no new unit is added).

Commit lines: the form is `tools/architecture_gate.py` (not copied here). Prescribed content:
`architecture: AR-1, AR-9, AR-10, AR-13, AR-15, AR-17, AR-20, AR-22, AR-28, AR-29 -- conductor command rows sited at their refusals
and told through one launch section on all three conductor launches; texts unchanged` and
`judgment: none -- ids attach to existing refusals and rows tell existing code readings; no check is added or moved`.

FR walk (owed by each builder for its files): A (FR-1/FR-2 texts unchanged, expected/door on the Record; FR-59 unreadable row →
the factory-defect sentence of `refusal()`); B — n/a (the conductor prompt is not text a person reads; FR-6 untouched); C (FR-14
output shape additive; FR-38 the requirement before the work on all three launches); D (FR-16 literal ids; FR-17 one renderer
wired at every launch); E, F — not touched; G (FR-30 English ASCII, FR-32 a test row per site and per launch kind, FR-54 siblings).

---

## §2 Measured state (read, not run: a designer has no shell; every number marked "at build" is measured by the builder)

| fact | carrier read | value |
|---|---|---|
| told counters | `W/PKG/references/stage-joints.json` `told_ratchet` | hand_cards 12, legacy_legs 0, unsited 17 |
| conductor rows today | same file, `"check": "no_move` (4 hits) | `no_move:options`, `:prose`, `:class` (`when: ["conductor_answer"]`), `:args` (`when: ["move:rework_stage"]`) |
| rows of the 14 ids | Grep `"check": "(controller|waiver|source_exclusions|stage_done|planning_contract:plan)[^"]*"` | none of the 14; `planning_contract:plan` exists (:5811); the 6 `controller:*` rows are T9a's |
| S8 rows | Grep `"check": "(driver|delivery|s8)[^"]*"` → 0; positive control: the same tool on the same file with `"check": "no_move` found 4 | none |
| a sub-id of a sited id is sited | `stage_joints._is_sited` (C14) | `planning_contract:plan` is sited (`planning_contract.gate_plan_errors` writes it), so `planning_contract:plan.unmarked_revision` is counted sited with or without its own literal |
| `controller:rework` / `waiver:block` / `source_exclusions:revoke` / `stage_done:set` sited? | `refusal_registry.check_of` = `<file stem>:<A24 id>`; A24 ids are `CTRL-*`, `SD-*`, `CTRL-next-blocked` (waiver) | no: none of these families is an A24 id or a literal today, so each new row is unsited until its literal lands |
| `_row_holds` for the conductor | `stage_joints._row_holds` | only `move:<id>` tokens are evaluated; every other token (`conductor_answer`) holds; an unknown token holds ("toward more text") |
| K2 conductor leg | `stage_joints._page_leg` | a conductor row's `when` must hold `conductor_answer` or a `move:` token |
| `_raise_all` strips Records | `Controller._merged` does `message = str(message)` | a `Record` passed through `_raise_all` loses its `check` (text identical) — fork F-2 |
| CLI printers | `controller.py` `__main__` prints `json.dumps({"error": str(exc)})`; `waiver.main` uses `ap.error(...)`; `source_exclusions.main` prints to stderr; `stage_done` main catches and prints | no printer prints `spoken()`/`told_fields` for these families (K3 decision: no transport here) |
| dry ledger | `dry_exits._code_rows` + `scan_joints` | every `check` of stage-joints.json is a joint the driver "has": each new row needs a ledger row (t-1087 precedent: `gates.json`, `unwalked` + `raised_by`) |
| conductor prompt ratchet | Grep `conductor` (case-insensitive) in `W/PKG/references/role-load.json` → 0; positive control `qa-runner` → 2 | no conductor ratchet: nothing to raise; the size growth is reported (AR-12) |
| legacy launch | `Driver.no_move_legacy` | `_ask_conductor(str(state["text"]))`: no moves, no section; the answer's class is judged in `Driver.pass_to_person` by `PO.question_rule` (bare, prints + `file_defect`) |
| conductor.md:99 | `W/PKG/references/conductor.md:99` | "Without a `why_person` class or with an empty `checked`, it is refused once." |
| S8 launch | `driver_stage_s8s9` `run_claude("conductor", prompt, stage="S8", …, resume_key="S8:delivery")` | JSON-form line names `action` `continue|ask_person|stop` and `mr`; `action` outside it → `delivery_person("… an answer I do not recognise")`; `mr` → `mr_record(verdict.get("mr"))` (None when not a record shape) |
| prompt cut | `Driver.conductor` | the text passed in is printed as `refusal.strip()[:6000]` under `## The refusal` |

Measured premises owed AT BUILD (commands; the result goes into the report, verbatim tail):
1. `python -B W/PKG/scripts/stage_joints.py --check` before any edit → `rows 273 … unsited 17` (baseline).
2. After the A sites, before the rows: the same → `unsited 17` (sites alone change nothing).
3. After the rows (A merged): the same → `rows 290` (273 + 15 + 2 S8, or + 1 if F-4 (c)) and `unsited 17`.
4. `( cd W/PKG && python -B scripts/tests/dry_exits.py --check )` → `0 discrepancies` after the ledger rows; the NOTE lists the new `raised_by`.
5. Size: `rows_for("conductor", ["*"], {"moves": ids, "answer": tokens})` + `told_line` on the real file, for (i) no move open, (ii) `go_on_as_is`+`story_fact`+`person_does`+`stop_here` open (the commonest non-gate launch), (iii) rework open, (iv) legacy, (v) S8 → chars each (T9c measured 750 / 1133 for its rows).
6. `python -B W/PKG/scripts/selftest.py --limits --lang` before and after the conductor.md edit.

---

## §3 N1: the 15 rows, their sites, the sited form

Rule for every site (EC-1, EC-2 of the finish spec §6 "common", binding): the text is byte-identical; the id is written at the
caller that knows the requirement; a helper with more than one caller carries no id; a site whose id would depend on a runtime
value uses one literal per branch (a conditional expression as the check argument is a scanner walk error, `check_ids`).
Story-state refusals (StateConflict / FR-46, part3 "S-R*/S-L*/S-W*/S-X*") stay bare (F-P2 (a)).

| # | row id | `when` | refusing site(s) (file, function, current expression) | sited form |
|---|---|---|---|---|
| 1 | `controller:rework.call` | `move:rework_stage` | (a) `controller.main`: `root, problems = _cli_story_root(a)` then `Controller._raise_all(problems)` — `_cli_story_root` serves EVERY operation; (b) `controller.main`: `reason = person_words.read(a.reason, a.words_file, "--reason")` (raises `person_words.WordsRefused`, helper with many callers) | (a) in `main`, only when `a.operation == "rework"`: each `(ValueError, m)` of `problems` becomes `(ValueError, DV.refusal("controller:rework.call", m))`; the `StateConflict` "initialize task before work" stays bare (story-state S-R14); (b) `except person_words.WordsRefused as exc:` re-raise the SAME class with `DV.refusal("controller:rework.call", str(exc))` as its one argument |
| 2 | `controller:rework.args` | `move:rework_stage` | `Controller.build_rework_request`: every `problems.append((ValueError, <literal text>))` written in the function's own body (stage, purpose, blank reason, reopen-a-closed-story, cause, the three `--candidates` problems, cases S4+, outside scope, plan rows, no accepted dispatch (plan / window / live / none), S5 several windows) | each such append becomes `(ValueError, DV.refusal("controller:rework.args", <same text>))`; the two `StateConflict` hold problems stay bare (story-state); the problems from `_rework_kind`, `_rework_block_problems`, `_half_membership_problems` are NOT `.args` (rows 3 and "not drafted") |
| 3 | `controller:rework.runner_half` | `move:rework_stage` | `build_rework_request`: `problems.extend((ValueError, text) for text in kind_problems)` (`_rework_kind`, one caller) | `(ValueError, DV.refusal("controller:rework.runner_half", text))`; the `_rework_block_problems` / `_half_membership_problems` extends stay bare (`.runner_half.manual_block` is not drafted: E-T9c-2) |
| 4 | `controller:rework.cap` | `move:rework_stage` | `Controller.validate`, dispatch branch, the three `raise StateConflict(blocking[0] + …)` of the repair cap (mechanical non-author; mechanical cap; test_defect cap) | `raise StateConflict(DV.refusal("controller:rework.cap", blocking[0] + <same rest>))`; the site serves every dispatch road (a rework, `story_step finish --needs-author`): one requirement, one id (small choice S-3) |
| 5 | `controller:release.call` | `move:release_and_restart` | (a) `main` `_cli_story_root` problems when `a.operation == "release"`; (b) `main` `words = person_words.read(a.words, a.words_file, "--words")` (7 operations share it); (c) `Controller.release_dispatch`: the three `problems.append((ValueError, …))` (no `--dispatch` with not one open, blank words, `_unknown_dispatch`) | (a) as row 1 (a) with this id; (b) a `try` around the shared read whose `except` re-raises with this id ONLY when `a.operation == "release"` (literal in that branch), any other operation re-raises unchanged; (c) each text through `DV.refusal("controller:release.call", …)` — `_unknown_dispatch` is a helper of 5 callers: wrap its returned message at THIS caller: `cls, m = self._unknown_dispatch(...); problems.append((cls, DV.refusal("controller:release.call", m)))`; the `StateConflict` "holds nothing back" stays bare (S-L1) |
| 6 | `waiver:block.call` | `move:go_on_as_is` | `waiver.main`: `ap.error(str(exc))` after `person_words.read` (every form shares it); `ap.error("--task, --stage, --block and --decision or --words-file (the person's words) are all required")` | (i) words: `except person_words.WordsRefused as exc:` then, in the SAME order the forms are dispatched below (remark, revoke, stage/block, gate): `if ns.remark: ap.error(DV.refusal("waiver:remark.call", str(exc)))`; `if not ns.revoke and (ns.stage or ns.block): ap.error(DV.refusal("waiver:block.call", str(exc)))`; else `ap.error(str(exc))`; (ii) the "all required" line: `ap.error(DV.refusal("waiver:block.call", <same text>))` |
| 7 | `waiver:block.placeholder` | `move:go_on_as_is` | `waiver.record_refusals` (one caller, `run_stage`): `return [f'waiver: the block "{match}" still holds the placeholder …']` | `return [DV.refusal("waiver:block.placeholder", f'…same…')]` |
| 8 | `waiver:block.stand_gap_id` | `move:go_on_as_is` | `record_refusals`: `return [NO_GAP_ID]` | `return [DV.refusal("waiver:block.stand_gap_id", NO_GAP_ID)]` (`NO_GAP_ID` constant unchanged; `test_whole_identifier` compares with `==`: a Record equals its str) |
| 9 | `waiver:block.grant_pattern` | `move:go_on_as_is` | `record_refusals`: `return test_path_grants.pattern_errors(...)` (another module's helper) | `return [DV.refusal("waiver:block.grant_pattern", e) for e in test_path_grants.pattern_errors(...)]` |
| 10 | `waiver:block.standing` | `move:go_on_as_is` | `waiver.run_stage`: `print(unmatched_text(task, stage, match, standing), file=sys.stderr)` on `kind == "unmatched"` | `print(DV.refusal("waiver:block.standing", unmatched_text(...)), file=sys.stderr)`; the `BlockNamesError` print stays bare (data-state S-W3); "no pipeline.json" stays bare (S-W1) |
| 11 | `waiver:remark.call` | `move:go_on_as_is` | `waiver.main`: words (row 6 (i)); `ap.error("--remark needs --task, --stage and --text or --words-file (the person's words)")` | row 6 (i) branch; `ap.error(DV.refusal("waiver:remark.call", <same text>))` |
| 12 | `source_exclusions:revoke.call` | `move:revoke_exclusion` | `source_exclusions.main`: the "give exactly one of --load FILE, --show, --revoke …" print; the `_task_root` ValueError print; the "--revoke needs --words …" print | `print(DV.refusal("source_exclusions:revoke.call", <same text>), file=sys.stderr)` at each; new module import `import detector_verdict as DV` (the file has none today; module level, beside the other imports, so the scanner binds it); argparse/`hooklib.exact_options` refusals stay bare (S-P4: their text is argparse's) |
| 13 | `source_exclusions:revoke.target` | `move:revoke_exclusion` | `main`: `print(f"source_exclusions: no exclusion `{args.revoke}` in {args.task}; it has: " + …)` on `result["status"] == "unknown"` | `print(DV.refusal("source_exclusions:revoke.target", <same text>), file=sys.stderr)`; "no record, nothing to revoke" stays bare (S-X1) |
| 14 | `stage_done:set` | `move:story_fact` | `stage_done.parse_sets` (callers: `main`, its selftest): `raise ValueError(f"--set takes key=value, not `{item}`")`; `out[key.strip()] = coerce_value(key.strip(), raw)` (`coerce_value` has 4 callers: EC-2, no id inside it) | `raise ValueError(DV.refusal("stage_done:set", <same text>))`; `try: … coerce_value(...) except ValueError as exc: raise ValueError(DV.refusal("stage_done:set", str(exc))) from None`; `current_code_diff_refusal` stays bare (story-state, part3 O-1) |
| 15 | `planning_contract:plan.unmarked_revision` | fork F-3 (recommended `move:approve_gate`) | `planning_contract.gate_plan_errors`: `… + unmarked_revision_errors(rows, plan_contract_mode)` (one caller of `unmarked_revision_errors`) | `+ [refusal("planning_contract:plan.unmarked_revision", line) for line in unmarked_revision_errors(rows, plan_contract_mode)]` (the module already imports `refusal` from detector_verdict); the docstring sentence "stay bare … lands with node T9c" is rewritten to say they carry this id |

Row texts (every row: `roles: ["conductor"]`, `stages: ["*"]`, `door_needs: "none"`, producer entry told `{"page": true}`,
`demands: []`, `joint: null`, in the T9c row form):
- Rows 1, 3, 4, 5, 7-14: `requirement` and `door` VERBATIM from part3 §1 (accepted t-489), except the corrections below, each read
  against the body at this draft:
  - row 2 `controller:rework.args`: part3 predates FL4. Corrected sentence (drafted here, Lead accepts, EC-8): "`--stage` is one of
    S0-S9; `--purpose` is one of PURPOSES; the reason (the words) is not blank; `--cause` is one of REPAIR_CAUSES; from S4 on
    `--cases` names at least one case and every case is inside the approved scope; every `--rows` id is a row of the approved plan;
    `--candidates` names bug candidates the story lists, for the S7 author only and never with `--cases` or `--rows`; the role has an
    ACCEPTED dispatch on that stage (on S5: of the kind the purpose names, the plan for `s5_plan`, else a window); on S5 the cases of
    a code-typed reason lie in ONE window (a person's words over several windows are not refused)." Door: part3's.
  - row 1 `controller:rework.call`: drop "that holds the story journal" (that refusal is story-state and stays bare: a sentence never
    claims a refusal its id does not carry, EC-8 / t-703 B2 class).
  - row 14 `stage_done:set`: the O-1-corrected sentence lives in `docs/tasks/specs/20261114-told-before-work-t1r-cards-spec.md`
    (lines 101/342, NOT read whole in this pass); the Lead quotes it into the dispatch (fork F-1 names this).
- Row 15: Q3's proposed sentence (T9c report §7) verbatim, door "the conductor reruns the S3 step, never the role".
- Pending and NOT in this node (E-T9c-2): `waiver:carry.call`, `.old_key` (F-P1 (a) `moves` row `words_carry` not landed in
  `conductor-actions.json`), `controller:rework.runner_half.manual_block`, `controller:release.commit`, the 10 helper bodies of part3
  §1.1, `stand_health:probe` (no row by part3 §1.5).

---

## §4 N2: one renderer, three launches

1. `no_move.checks_section(open_ids, answer) -> str` (new, `no_move.py`): exactly the T9c block moved out of `moves_section` —
   `["", WHAT_CODE_CHECKS, ""]` then NOT KNOWN (unreadable, `SJ.read_rows()`), or `told_line` of `SJ.rows_for("conductor", ["*"],
   {"moves": list(open_ids), "answer": list(answer)}, data)`, or `NOTHING_CHECKED`. `moves_section` calls it with
   `answer=MOVES_ANSWER`; its output for the moves road is byte-identical to today for every launch whose open moves have no
   command row (EC-B1).
2. Answer tokens (data): `when_kinds` gains `conductor_options` and `delivery_answer`. Named tuples in `no_move.py`:
   `MOVES_ANSWER = ("conductor_answer", "conductor_options")` (moves road), `LEGACY_ANSWER = ("conductor_answer",)` (the S1 review),
   `DELIVERY_ANSWER = ("delivery_answer",)` (S8).
3. Rows: `no_move:options` and `no_move:prose` `when` → `["conductor_answer", "conductor_options"]` (ALL must hold: the legacy road
   does not validate options or prose, so they never hold there); `no_move:class` stays `["conductor_answer"]`; `no_move:args`
   unchanged.
4. `stage_joints._row_holds` (conductor branch): a token that is not `move:` and not a capability token holds iff it is in
   `facts["answer"]` when `facts` carries the key `answer` (a list); when the key is absent it holds (today's behaviour, every
   current caller). `stage_joints._page_leg`: the conductor's selector accepts any token of `CONDUCTOR_ANSWER_TOKENS =
   ("conductor_answer", "conductor_options", "delivery_answer")` or a `move:` token (the refusal sentence names the tuple).
5. `Driver.no_move_legacy`: the conductor text becomes `NM.checks_section([], NM.LEGACY_ANSWER).lstrip("\n") + "\n\n" + state text`
   (section FIRST, the same order as the moves road, so the 6000-char cut of `Driver.conductor` takes the state text's tail first).
   The `s1_review` exclusion from MOVES stays: no `## Moves open here`, no options validation; `NM.EXCLUDED_KINDS` and its comment
   are kept and the comment adds "the launch still lists what code checks (TBW1-11); it is excluded from moves only".
6. `Driver.pass_to_person`: `rule = PO.question_rule(...)` becomes `DV.refusal("no_move:class", rule)` when `rule` is non-empty
   (text identical in the print and the `file_defect` line; `[:160]`/`[:300]` slices apply to the str as before). Caller count of
   `pass_to_person` verified by Grep at the build (expected: `no_move_legacy` only; a second caller → EC-2 question).
7. `references/conductor.md:99`: the sentence "Without a `why_person` class or with an empty `checked`, it is refused once." is
   replaced by "What code checks of your answer is listed in each launch under `## What code will check in this launch`." (fork
   F-5 (a)); nothing else of the file changes.
8. S8 (`driver_stage_s8s9`, the delivery launch): the prompt list gains `NM.checks_section([], NM.DELIVERY_ANSWER)` as the item
   right BEFORE the "Answer with ONE JSON line last: …" item (the JSON-form line stays byte-identical and last of the list). Two
   rows (fork F-4 (a)):
   - `driver_stage_s8s9:delivery.action`, `when: ["delivery_answer"]`: "The answer's `action` is `continue`, `ask_person` or
     `stop`; any other action is read as no answer and the person is asked in words." Door: "answer with one of the three". Site:
     the unrecognised-action branch, `raise self.delivery_person(DV.refusal("driver_stage_s8s9:delivery.action", <same text>),
     why_person=…)` (`delivery_person(said: str)` — a Record is a str; text identical).
   - `driver_stage_s8s9:delivery.mr`, `when: ["delivery_answer"]`: "With `continue`, `mr` is the Draft MR's link, id or number
     when one was opened or already exists, empty when none; any other value is no record, and the `mr` order is then called off
     as delivered without an MR." Door: "give the MR's link or id, or leave it empty". Site (F-4 (a)): in the `continue` branch,
     when `verdict.get("mr")` is non-empty and `mr_record(...)` is None, one stdout line
     `print(DV.refusal("driver_stage_s8s9:delivery.mr", f"delivery: `mr` {value!r} is no record of a merge request; the mr order is called off"))`
     — the ONE behaviour addition of the node (a line in the run log; nothing else changes).

---

## §5 Edges (each with its invariant)

- E1 a `when` that cannot be evaluated at launch time (unknown token, facts without the key, a facts reader that raised): the row
  HOLDS. Invariant: a row is never omitted because a fact could not be read (`_row_holds` direction); over-telling is the safe side.
- E2 empty rows list for a readable file: `NOTHING_CHECKED`. Invariant: with N1 landed, a launch where a move is open whose command
  is checked lists that command's rows, so `NOTHING_CHECKED` is printed only when no row of the launch's answer tokens and open moves
  exists — never while a check of this launch is pending. A test row asserts: moves road with `rework_stage` open lists the 4
  `controller:rework.*` rows + `no_move:args`.
- E3 unreadable `stage-joints.json` (absent, OSError, not JSON, 0 bytes, not an object, schema mismatch, `joints` not a list): NOT
  KNOWN with the reader's reason on ALL three launches (one renderer). Invariant: an unknown is never `none` and never a decision;
  nothing reads the section.
- E4 a rework with no args yet: the `move:rework_stage` rows hold as soon as the move is open; nothing at launch reads `args`.
  Invariant: the section depends on open moves and answer tokens only, never on the answer it precedes.
- E5 TEMPORAL — sites before rows (stream A merged first): `refusal()` gives `expected` = "(the factory's requirement row <id> could
  not be read: no row for <id>; this is a factory defect)" on a Record no printer shows; `unsited` unchanged. Rows before sites: each
  row is unsited → `stage_joints --check` red ("a raise is named"). Invariant: `told_ratchet.unsited` never rises; hence the merge
  order A → B (§7) and B's witness runs on a tree with A merged.
- E6 TEMPORAL — the `answer` facts key: before, no caller passes it and every non-move token holds; after, the three launch callers
  pass it. Invariant: a caller that omits it gets today's behaviour (more rows), never fewer.
- E7 Records through `Controller._raise_all`: `_merged` turns each message into a plain `str`, so the id survives only if F-2 (a)
  lands. With F-2 (b), the id exists at the site (the ratchet counts it) but is gone at the raise — named in the report.
  Invariant either way: the raised text is byte-identical.
- E8 `_noted` (stage that is no stage) rebuilds the last message by f-string: that one problem loses its id (text identical). Named
  E6 (code); `_noted` is shared (16 callers) and not edited.
- E9 `ap.error` / `print` sites: the Record is printed as its text and dies there (no transport, K3 decision). Invariant: stderr bytes
  and exit codes unchanged.
- E10 POSITIONAL — `waiver.main` words refusal: the branch picking `waiver:remark.call` / `waiver:block.call` follows the order the
  forms are dispatched below it (remark, revoke, stage/block, gate). Invariant: a revoke or gate form never carries a block/remark
  id; a remark never carries the block id.
- E11 POSITIONAL — `controller.main`: the id mapping of `_cli_story_root` problems and of the shared words read happens only inside
  `a.operation == "rework"` / `"release"` branches. Invariant: no other operation's refusal carries a rework/release id.
- E12 the 6000-char cut (`Driver.conductor`, `refusal.strip()[:6000]`): the section rides inside that text. Invariant: the section is
  never cut. At build, measure (premise 5) lead + moves + section for the largest fixture launch; over 6000 → STOP and report (the
  cap is not changed by this node).
- E13 legacy road: `no_move:options` / `:prose` / `:args` and every command row never hold (moves `[]`, answer `LEGACY_ANSWER`).
  Invariant: the legacy launch claims only what `pass_to_person` checks.
- E14 S8: no `no_move:*` row holds (answer `DELIVERY_ANSWER`, moves `[]`). Invariant: the S8 launch claims only `action` and `mr`.
- E15 `pass_to_person` with an empty rule: no Record, path unchanged.
- E16 conductor.md edit vs `design/role-rules.json` mandatory rules: if `selftest.py --limits` names the removed sentence as a
  mandatory carrier line → STOP, fork F-5 (b) applies (the line is re-worded to quote the row's id), report verbatim.
- E17 tests that pin "unmarked stays bare" (`test_detector_verdict.py` ~:1845 docstring, ~:1982 `bare = PC.gate_plan_errors(...)`):
  their expectation flips to the new id; expected value from this card's row 15, never from the new code's output.
- E18 the rows `when` `move:<id>` must name a `moves[].id` of `conductor-actions.json` (K3, E-T9c-1): `rework_stage`,
  `release_and_restart`, `go_on_as_is`, `revoke_exclusion`, `story_fact`, `approve_gate` — all present (read in `no_move.MOVE_FACTS`).

Pinned texts that stay byte-identical: every refusal text of §3 (EC-1, expected from a byte copy of the OLD files); the stderr
lines of `waiver`, `source_exclusions`, `stage_done`; `controller.py`'s JSON `error` lines; the moves road prompt for launches whose
open moves have no command row; the `Driver.conductor` prompt frame; the S8 JSON-form line; every line of `conductor.md` but :99;
`NM.EXCLUDED_KINDS`; `audit_factory.CONDUCTOR_SITES`.

---

## §6 Effects on counters and ledgers (each named; numbers at build)

| counter | before | after | who moves it |
|---|---|---|---|
| `told_ratchet.unsited` | 17 | 17 (by measurement at build). The brief expected it to SHRINK: it does not — every new row lands with its literal; the 17 are rows of other families (the 6 `controller:*` of T9a among them). No raise. | nobody (F-1 (a): the integrator only if the measure moves) |
| stage-joints rows (K1 pin `test_stage_joints.py`) | 273 | 290 (+15 command/plan, +2 S8; +1 if F-4 (c)) | stream B, labelled "+N TBW1-11 conductor rows" |
| `rows-for/real` conductor expectation (`test_stage_joints.py`) | the four `no_move:*` ids | + the rows holding with `{"moves": [...], "answer": [...]}` of its fixture | stream B |
| `fixtures/driver-exits/gates.json` `unwalked` credit (`raised_by`) | 231 | 231 + 17 (one joint row + one `raised_by` line per new row, form of t-1087: reach `unwalked`, why "TBW1-11 conductor rows, <date>: reached by the conductor's launches, not judged by a row of their own"); group base unchanged | stream B |
| `role-load.json` | no conductor row | unchanged; the size growth (premise 5, chars per launch kind) is reported (AR-12), no ratchet exists to raise | — |
| `told-ratchet.json` (`rowless`, `untold`) | — | if `test_stage_joints` demands a change, named in the report; the file is the closing node's (non-goal) | closing |
| `judgment-census.json` | — | no edit expected ("census: no new blocking unit"); if `test_judgment_census` (canon) asks, named | — |

---

## §7 Streams, owns, witness

Split: two builders, parallel work, disjoint files; MERGE ORDER A → B (E5). Fork F-6.

### Stream A — the 15 sites (command and plan refusals)
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\controller.py (main, Controller.build_rework_request, Controller.validate repair-cap raises, Controller.release_dispatch; Controller._merged / Controller._raise_all only under F-2 (a))
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\waiver.py (main, record_refusals, run_stage)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\source_exclusions.py (main, the module import)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\stage_done.py (parse_sets)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\planning_contract.py (gate_plan_errors)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_detector_verdict.py (new function `tbw_siting_command_sites`; the rows that assert `unmarked_revision_errors` lines are bare)
C:\QAFactory\forge-repo\ai-packages\qa-factory\changelog.d\tbw-siting-a.md
non-goals: stage-joints.json; any refusal TEXT; `_noted`; `person_words.py`; `test_path_grants.py`; `coerce_value`; a transport
(spoken/told_fields printers); the story-state refusals; `.runner_half.manual_block`, `release.commit`, `waiver:carry.*`; census;
`told_ratchet`; slow or quarantined tests; CI.
items: one table row per site in `tbw_siting_command_sites` — (text, id) of the refusal: text = the OLD file's output (byte copy taken
before the edit), id = §3; a row per branch of row 6 (i) (remark / block / revoke / gate) and of row 5 (b) (release / another
operation); a row asserting `_raise_all` keeps the Record (F-2 (a)) or asserting the text only (F-2 (b)).
DoD: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for scripts/controller.py scripts/waiver.py scripts/source_exclusions.py scripts/stage_done.py scripts/planning_contract.py scripts/tests/test_detector_verdict.py`
— run every printed file not in `slow_tests.json` and not quarantined, each alone; slow ones listed "judged by the batch canon";
`python -B ai-packages/qa-factory/scripts/stage_joints.py --check` → clean, `unsited 17` (premise 2); `python -B
ai-packages/qa-factory/scripts/selftest.py --limits --lang`; `python -B tools/controller-blocks-gen.py` in its check form (flag read
from its `--help`; `design/controller-blocks.md` stays byte-identical or the regeneration is named); negative control: one wrapped
site turned bare on a byte copy → its table row FAILs; restore by `cp`, hashes equal.

### Stream B — the rows, one renderer, three launches
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\no_move.py (checks_section new, moves_section, MOVES_ANSWER / LEGACY_ANSWER / DELIVERY_ANSWER, the EXCLUDED_KINDS comment)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\stage_joints.py (_row_holds conductor branch, _page_leg, CONDUCTOR_ANSWER_TOKENS)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\driver_conductor.py (Driver.no_move_legacy, Driver.pass_to_person, Driver._conductor_text only if the facts key needs it, the detector_verdict import)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\driver_stage_s8s9.py (the delivery prompt list item, the unrecognised-action branch, the mr line of F-4 (a))
C:\QAFactory\forge-repo\ai-packages\qa-factory\references\conductor.md (line 99 only)
C:\QAFactory\forge-repo\ai-packages\qa-factory\references\stage-joints.json (the 15 + 2 new rows, `when` of no_move:options/:prose, `when_kinds`)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\driver-exits\gates.json (joint rows + raised_by of the new rows)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_controller_doors.py (new rows)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_stage_joints.py (K1 rows pin and `rows-for/real` conductor expectation only)
C:\QAFactory\forge-repo\ai-packages\qa-factory\changelog.d\tbw-siting-b.md
non-goals: `told_ratchet` (F-1 (a)); `told-ratchet.json`; `role-load.json`; `conductor-actions.json`; `audit_factory.CONDUCTOR_SITES`;
`NM.EXCLUDED_KINDS` membership; any refusal text; the moves section headings and order (E-T9c-5); slow tests; CI.
items (one parameterised table per behaviour in `test_controller_doors.py`): `LAUNCH_KINDS` — (launch, open moves, answer tokens) →
expected row ids, expected from §3/§4 (moves road no move / rework open / go_on_as_is+story_fact open / approve_gate open; legacy;
S8); `UNREADABLE_ROWS` gains the legacy and S8 callers; `ROW_HOLDS` — `_row_holds` with/without the `answer` key (E1, E6); one row
per launch prompt holding the section before the state text (legacy) / before the JSON line (S8); `pass_to_person` id row; S8
`action` and `mr` rows (text + id).
DoD: on a tree with stream A merged: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for scripts/no_move.py scripts/stage_joints.py scripts/driver_conductor.py scripts/driver_stage_s8s9.py references/conductor.md references/stage-joints.json scripts/tests/fixtures/driver-exits/gates.json scripts/tests/test_controller_doors.py scripts/tests/test_stage_joints.py`
— fast printed files each alone, slow ones "judged by the batch canon"; `python -B ai-packages/qa-factory/scripts/stage_joints.py
--check` → clean, `rows 290`, `unsited 17`; `( cd ai-packages/qa-factory && python -B scripts/tests/dry_exits.py --check )` → `0
discrepancies`; `python -B ai-packages/qa-factory/scripts/contract_slices.py --check`; `python -B
ai-packages/qa-factory/scripts/selftest.py --limits --lang`; premise 5 sizes in the report; negative control: `checks_section` call
removed from `no_move_legacy` on a byte copy → the legacy `LAUNCH_KINDS` row FAILs; restore by `cp`, hashes equal.

Common to both: "census: no new blocking unit"; the report holds the site table (function | fragment | id or E6 reason (class) |
test row | proof F/W/N), the FR walk, the ratchet lines of §6, the verbatim witness; siblings: axis 17 (Record shape), axis 34 (one
road: `refusal()` only; one renderer), axis 39 (when T10 opens it); analogs noticed are reported, not widened.

---

## §8 Readers of every touched file (rule 7)

Commands (Grep tool, count mode), pattern `controller\.py|waiver\.py|source_exclusions|stage_done\.py|planning_contract|no_move|driver_conductor|driver_stage_s8s9|stage-joints|conductor\.md|driver-exits|test_controller_doors`:
over `tools/` → 31 hits in 12 files; over `.githooks/` → 0; over `.claude/agents/` → 0; over `.claude/` whole → stopped at the
tool's time limit (the worktree copies), NOT established for `.claude/settings.json` and `.claude` hook files — owed before
dispatch: the same Grep over `.claude/settings.json` and `.claude/*.py` (no worktrees).

| touched file | reader | verdict |
|---|---|---|
| `controller.py` | `tools/controller-blocks-gen.py` (14 hits; generates `design/controller-blocks.md` from controller code) | unchanged code; its check run in stream A's DoD — if wrapping a raise text in `DV.refusal(...)` changes what it extracts, STOP and report (blocks must stay byte-identical, T9a precedent) |
| `controller.py` et al. | `tools/lint-baseline.json` (1), `tools/source-split-carriers.json` (2) | unchanged; a lint or size ratchet that moves is named in A's report |
| several names | `tools/test_forge_metrics.py` (5), `test_collect_intake.py`, `test_dispatch_gate.py`, `test_md_table.py`, `test_piles.py`, `test_quarantine.py`, `test_test_quarantine.py`, `test_test_split.py`, `test_controller_blocks_gen.py` | name mentions in tools' own tests; unchanged |
| `stage-joints.json` | `stage_joints.py`, `contract_slices.py`, `selftest.py` (via `load_rows`), `dry_exits.py` (`scan_joints`), `detector_verdict.refusal` (via `row_for`), N3a `told_before_work` (p1b-finish) | rows change in B; `dry_exits` ledger in B; N3a re-reads at its merge |
| `no_move.moves_section` | `driver_conductor._conductor_text`, `test_conductor_doors`, `test_no_move_seam_c26_g27_f2`, `test_story_run_exit_limit` (finish spec §11) | output unchanged except new command rows when their move is open (canon judges the slow ones) |
| `stage_joints._row_holds` / `_page_leg` | `rows_for` (pages of every role, `contract_slices.requirement_section`), the K2 walk | non-conductor branch unchanged; conductor branch changes only when `answer` is passed |
| `references/conductor.md` | `driver_conductor.Driver.conductor`, `driver_stage_s8s9` (system_file), `stage_joints.ROLE_FILES`, `selftest --limits` (role-rules) | line 99 changes in B (E16) |
| `fixtures/driver-exits/gates.json` | `dry_exits.py` | B |
| `test_detector_verdict.py` | the T-wave nodes' own functions (F-2 (b) precedent) | A adds one function, flips the bare rows (E17) |
| `test_controller_doors.py` | T9a (new rows only), T9c | B adds rows; merge keeps both sides' rows |

---

## §9 Forks (returned, not decided)

| # | fork | options | recommendation |
|---|---|---|---|
| F-1 | the row sentences | (a) part3 verbatim + the corrections of §3 (row 2 FL4 candidates, row 1 journal clause), `stage_done:set` quoted by the Lead from the T1r-cards spec O-1 fix; the Lead accepts them in the dispatch (EC-8) · (b) the builder drafts each from the body and returns them as questions (stalls the node) | **(a)** |
| F-2 | Records through `Controller._raise_all` (`_merged` stringifies) | (a) `_merged` keeps the message object when its count is 1, and `_raise_all` raises the one Record as the exception's argument; with several problems the exception gets `records` (the `ArgsRefused` EC-5 form); text byte-identical; `_raise_all` serves many controller paths — additive only · (b) leave it: the literal counts for the ratchet, the id is lost at the raise (E7) | **(a)**: a site the ratchet counts should carry its id to the exception; the change is additive and its text is pinned |
| F-3 | `when` of `planning_contract:plan.unmarked_revision` | (a) `move:approve_gate` — the move gate-inputs refuses while a row is unmarked (also listed at gate B: harmless noise) · (b) `conductor_answer` (every launch: ~300 chars on every call) · (c) no launch row: sited sub-row only. Also named: `gate_preflight.check_planning_contract` prints the door "repair the plan rows (a strategist rework) before the gate" while the line says "the conductor reruns the S3 step (never the role)" — two doors for one finding (P31); out of owns, reported for a pile finding | **(a)** |
| F-4 | the S8 delivery checks | (a) two rows; `action` sited at its existing branch, `mr` sited by one new run-log line when a given `mr` is no record (the node's one behaviour addition) · (b) `mr` row unsited (raise by 1: against the Lead decision "no raise") · (c) `action` row only; `mr` stays told by the JSON-form line alone (then the section does not list a check code makes) | **(a)** |
| F-5 | `conductor.md:99` | (a) replace by the pointer sentence of §4 item 7 · (b) keep a sentence that quotes the row id (`no_move:class`) if role-rules demand a line there · (c) delete with no pointer | **(a)**; (b) if E16 trips |
| F-6 | split | (a) two builders A/B, parallel work, merge A → B · (b) one builder (≈ 20 sites + N2: budget risk) | **(a)** |
| F-7 | answer tokens | (a) a facts key `answer` read by `_row_holds` for the conductor (§4) · (b) a per-launch explicit list of row ids passed by the caller (a second selection road beside `when`: P31 risk) · (c) give the legacy and S8 launches the full `conductor_answer` set (over-tells options/prose/args to launches that do not check them) | **(a)** |

## §10 Small choices closed by the designer

- S-1 Function name `checks_section`; tuple names `MOVES_ANSWER`, `LEGACY_ANSWER`, `DELIVERY_ANSWER`, `CONDUCTOR_ANSWER_TOKENS`.
- S-2 Token names `conductor_options`, `delivery_answer` (the existing kind is `conductor_answer`).
- S-3 `controller:rework.cap` keeps its drafted id at `Controller.validate` though the site serves every dispatch road: one
  requirement, one id (EC-2 forbids two requirements under one id, not one requirement met by two roads).
- S-4 S8 row family `driver_stage_s8s9:delivery.*` (the namespace is the producer stem, told-before-work §2.1).
- S-5 Ledger group for the new joints: `gates.json` (the t-1087 precedent for conductor rows).
- S-6 Test function in `test_detector_verdict.py` named `tbw_siting_command_sites` (F-2 (b) of the finish spec: one function per node).
- S-7 Changelog fragments `tbw-siting-a.md`, `tbw-siting-b.md` (one English ASCII bullet each).

## §11 Contradictions and analogs noticed (not widened)

- The brief says `told_ratchet.unsited` "shrinks": it does not (§6) — every new row is sited at landing.
- `gate_preflight.check_planning_contract` door vs the unmarked line's door (F-3).
- `waiver:carry.*` stay out until `conductor-actions.json` gains the `words_carry` move (F-P1 (a) accepted 13.11, not landed).
- `Controller._merged` stringifies every message: any future siting in controller.py through `_raise_all` meets E7 (F-2).
- The S8 JSON-form line words `action`/`mr`, and after this node the rows word them too: the T9c precedent (form line + section) is
  kept; if the Lead reads it as two wordings of one requirement, the form line can drop its value lists (pinned text change: not here).

## §12 Not established

- `stage_done:set` corrected sentence (T1r-cards spec :101/:342 not read whole).
- Readers in `.claude/settings.json` and `.claude` hook scripts (Grep stopped at the time limit over worktrees).
- `tools/controller-blocks-gen.py` CLI and whether it extracts raise texts (read by the builder).
- Every number marked "at build" (no shell in this role).
- `pass_to_person` caller count beyond the one read (`no_move_legacy`).
- Whether `test_judgment_census` / `told-ratchet.json` ask for a move after the rows land.

## §13 Reading trail

Read (W unless noted): verdict t-1091 whole; T9c report whole (incl. follow-up t-1087); finish spec :1-280, :390-708; part3 whole;
`no_move.py` :20-519; `stage_joints.py` :255-634, :700-869, :1050-1289; `detector_verdict.py` :95-244; `refusal_registry.py`
:1330-1369 and Grep of `check_of` / A24 entries; `planning_contract.py` :255-309 and Grep of `unmarked_revision_errors|gate_plan_errors(`;
`gate_preflight.py` :1895-1939; `controller.py` :3705-4044, :5640-5719, :6154-6235, :8223-8272, :9791-9838, :9990-10135;
`person_words.py` Grep (`WordsRefused`); `waiver.py` :1205-1364, :1887-1976; `source_exclusions.py` :614-691 and import Grep;
`stage_done.py` :212-221 and Grep; `driver_conductor.py` :170-359, :560-849; `driver_stage_s8s9.py` :405-484 and Grep;
`references/conductor.md` Grep `why_person`; `references/stage-joints.json` :8140-8302 and the family Greps; `dry_exits.py` :524-543,
:634-686; `fixtures/driver-exits/` Glob (8 files); `role-load.json` Grep (`conductor` -i → 0, control `qa-runner` → 2).
Greps with controls: `refusal\(\s*"(controller|waiver|…)` over W scripts (found no_move and planning_contract sites — control of the
same call); `detector_verdict` in 7 files; callers of `build_rework_request`, `release_dispatch`, `person_words.read`, `_cli_story_root`,
`record_refusals`, `coerce_value|parse_sets`, `_noted`, `_rework_kind`, `_half_membership_problems`; readers over `tools/`,
`.githooks/`, `.claude/agents/`.
Needed beyond the manifest: the code files above, part3, `dry_exits.py`, `refusal_registry.py`, `gate_preflight.py`, `role-load.json`.

## Lead decisions on the forks (17.11.2026)

- F-1 = (a); the `stage_done:set` sentence is quoted from the T1r-cards spec O-1 fix by the plan critic's check / the Lead at dispatch.
- F-2 = (a), F-3 = (a), F-4 = (a), F-5 = (a) ((b) if E16 trips), F-6 = (a) two builders A -> B, F-7 = (a).
- The two doors for one finding named under F-3 (`gate_preflight.check_planning_contract` vs the unmarked line) are NOT filed as a finding (the owner's word 17.11: fixed in the round): the plan critic says which door is true, and the card's stream gains that one-sentence fix.
- The brief's claim "`told_ratchet.unsited` shrinks" was the Lead's error; §6 stands (17 -> 17, no raise).
- Readers owed in §12: `grep -n -E "no_move|stage_joints|driver_conductor|driver_stage_s8s9|planning_contract|stage_done|waiver|source_exclusions" .claude/settings.json .claude/*.py` -> no hit (control: `grep -c "tools/" .claude/settings.json` -> 37).
