# TBW siting card r2: the conductor's launches are told every check, in a block the refusal cut cannot reach (t-1108, node told-before-work/1/TBW1-11)

Status: DRAFT r2 for Lead acceptance (designer). Replaces `20261117-tbw-conductor-launches-siting-card.md` (r1, t-1096) WHOLE: a
builder executes from this file alone, plus the accepted row drafts it names one hop away (part3, `docs/tasks/specs/20261113-told-before-work-wave0-rows-part3.md` §1).
Applies verdict t-1102 (`docs/tasks/specs/reviews/t-1102-tbw-siting-plan.md`): B1, B2, B3, F1-F12, keys 2/4/7 and the standing
questions; the closing table (§13) maps each remark to where it is applied. Lead decisions of 17.11.2026 (r1 appendix and the t-1108
brief) are built in. Closes N1 and N2 of verdict t-1091.

Code read in the T9c tree `W = C:/QAFactory/forge-repo/.claude/worktrees/agent-a8e7e4c769ef59136` (read only; a fix round is still
landing in `no_move.py`, `stage_joints.py`, `stage-joints.json`, `test_controller_doors.py`: function names are load-bearing, line
numbers are not and are re-located by Grep). FV2-94's in-flight tree `F = C:/QAFactory/forge-repo/.claude/worktrees/agent-a7712a5a6d8bb4c87`
(read only, not merged). `PKG = ai-packages/qa-factory`. Every number marked "at build" is measured by the builder; this role has no shell.

---

## §0 What the node delivers

(N1) Fifteen command/plan rows land in `references/stage-joints.json`, each with a literal `DV.refusal("<id>", <same text>)` (or
`refusal(...)` where the file imports it so) at its refusing site; `told_ratchet.unsited` does not rise. The controller's block walk
(`tools/controller-blocks-gen.py` and the package detector `scripts/tests/test_controller_blocks.py`) reads a wrapped message as its
bare one, so `design/controller-blocks.md` stays byte-identical. The unmarked-revision line of `planning_contract` gets its TRUE door
(key 4). (N2) What code will check in a conductor launch is rendered by ONE function, `no_move.checks_section(open_ids, answer)`, and
travels as its OWN block of the conductor prompt, right before `## The refusal`, outside the 6000-character cut, outside the file scan,
the journal and `ConductorSpent` — on all three launches (moves road, legacy S1 review, S8 delivery). The S8 launch gets rows for the
two things code reads of its answer (`action`, `mr`).

## §0a Base, order and the two worlds (TEMPORAL; verdict F9, the FV2-94 collision)

Facts at draft time: T9c (`WHAT_CODE_CHECKS`, the section inside `moves_section`) is NOT on origin/main (t-1102 F9:
`git show origin/main:…/no_move.py | grep -c WHAT_CODE_CHECKS` → 0; the root checkout's `no_move.py` has no `WHAT_CODE_CHECKS`, control
`def moves_section` → 1). FV2-94 (`live-run-fvf/2/FV2-94`, t-1099, builder in F) is in flight: in F, `_conductor_text` builds a `head`
(lead + moves section + gate prices + the person's choice) BEFORE the state text and sets `self.conductor_head`; `Driver.conductor`
cuts `refusal.strip()` at `max(6000, len(keep))` when the text starts with that head, so the cut takes only the state text's tail.

| stream | may start | branches from | merges |
|---|---|---|---|
| A (sites, walk, key-4 door) | now | origin/main | before B |
| B (rows, renderer, three launches) | ONLY when T9c (with its fix round), FV2-94 and A are all on origin/main | origin/main after those three | last |
| T9a (TBW1-10, owns `controller.py`, `test_controller_doors.py`) | — | — | after this node; merges main into its tree (TEAMWORK §3); the B2 walk fix and F-2 serve its sites too |

PRECONDITION of stream B, checked by the Lead before dispatch (all three, verbatim output into the dispatch):
`git -C C:/QAFactory/forge-repo fetch` then
(1) `git -C C:/QAFactory/forge-repo show origin/main:ai-packages/qa-factory/scripts/no_move.py | grep -c WHAT_CODE_CHECKS` → ≥ 1 (T9c);
(2) `git -C C:/QAFactory/forge-repo log origin/main --oneline --grep FV2-94` → non-empty, and the batch-2 row FV2-94 is no longer `ожидает`;
(3) `git -C C:/QAFactory/forge-repo log origin/main --oneline --grep tbw-siting-a` (or A's merge commit) → non-empty.

- World 1 — FV2-94 merged (expected). B finds the head-keep of FV2-94 in `Driver.conductor` / `_conductor_text` (names as in F at
  read time: `conductor_head`, the `cap = max(6000, len(keep))` line; re-located by Grep `FV2-94`). B builds ON it and does not redo it:
  B never edits the cut expression or the head-keep logic; B's only edit inside `_conductor_text` is F-8 (a) (§4 item 7). Because B
  removes the checks section from `moves_section`, FV2-94's head shrinks by that section (nothing else changes for FV2-94). If the
  merged FV2-94 has another SHAPE (e.g. the cut applies only to the details), B keeps the INVARIANT of §4 item 3, not F's shape.
- World 2 — FV2-94 not merged: stream B does NOT start (precondition (2) fails; the Lead holds the dispatch). Nothing of this card
  re-creates FV2-94's work (the person's choice and prices before the details) — that stays FV2-94's.
- A needs neither T9c nor FV2-94 (its files are disjoint from both: §8).

---

## §1 Architecture, owners, census (rule 10, AR-29, P27)

| AR | touched how | kept how | change check in the DoD |
|---|---|---|---|
| AR-10 a check's requirement reaches the role before the work | the three conductor launches list the rows of what judges the answer and the commands of the open moves | one renderer; the block sits outside every cut, so no requirement is dropped for size | `LAUNCH_KINDS` rows per launch kind (B); the prompt row "told block before `## The refusal`" |
| AR-9 every refusal names what it expected and a door | 15 refusals get the row id on their Record; the unmarked-revision line's door was false (key 4) | texts byte-identical except ONE named tail (F1); the door now names the road that writes the mark | per-site rows (A): text = OLD output (card text for the one tail), id = §3 |
| AR-15 one survivor | the section had one placement (inside `moves_section`); now `checks_section` is the one renderer and one placement (the told block) serves three launches | `moves_section` no longer renders it; Grep `WHAT_CODE_CHECKS` writers = 1 (`checks_section`) | critic grep; a `LAUNCH_KINDS` row asserts `_conductor_text` output holds no `WHAT_CODE_CHECKS` (never twice) |
| AR-16 every text a person reads goes through one form | the legacy cap turns `ConductorSpent.refusal` into a Person text (B3) | the told block never enters `refusal`, so the Person text stays byte-identical | `LAUNCH_KINDS` row `legacy-cap` (pinned text, no `WHAT_CODE_CHECKS`) |
| AR-24 a person's words reach whatever acts on them, whole | FV2-94 keeps the person's choice and the prices out of the cut | the told block is outside `refusal`, so it never competes with the choice for the 6000 characters; F-8 (a) keeps the refused paragraph whole too | B's witness prints FV2-94's own rows unchanged; F-8 row |
| AR-17 one seam to the conductor | `_ask_conductor` stays THE caller of `self.conductor(`; S8 stays the one named exception | the told carrier is set inside `_ask_conductor` (F-9 (b)); `audit_factory.CONDUCTOR_SITES` unchanged | A27 green in the canon |
| AR-13 a fact with a reader is read through it | rows read only by `stage_joints.read_rows` / `rows_for` / `told_line`; Records only by `DV.refusal` | no new reader of `stage-joints.json` | critic: no `json.load` of stage-joints in the diff |
| AR-14 one artifact, one writer | the told carrier (F-9 (b): attribute `conductor_told`) | one writer (`_ask_conductor`), one reader (`conductor`, read-and-clear) | `driver-layers.json` row (B); critic grep `conductor_told =` writers = 1 (+ the clear) |
| AR-1 closed variety is a data row | answer tokens `conductor_options`, `delivery_answer` | in `when_kinds` (data); `CONDUCTOR_ANSWER_TOKENS` names them once in `stage_joints.py` beside `CAPABILITY_TOKENS` | `stage_joints.py --check` K3 green |
| AR-12 friction is measured | the told block grows each conductor prompt (est. up to ≈ 6100 chars on a gate-A launch with rework + go_on_as_is + approve_gate + story_fact, t-1102 B1) | no longer paid by losing the refusal (the cut never takes it); the chars per launch kind are measured and reported; no conductor ratchet exists (`role-load.json`: `conductor` -i → 0, control `qa-runner` → 2) | premise 5 in B's report |
| AR-20 shrink-only ratchets | rows pin, `gates.json` `unwalked` credit | each move named old → new with reason; `told_ratchet.unsited` does NOT rise | ratchet lines in the reports |
| AR-22 field read ↔ producer | facts key `answer`; the told carrier | produced by the three launch callers / `_ask_conductor`, read by `_row_holds` / `conductor` | table rows per launch kind |
| AR-28 an unknown never becomes a pass | NOT KNOWN on an unreadable rows file | kept on all three launches (one renderer) | `UNREADABLE_ROWS` per answer tuple |
| AR-29 code judges data | no check added or moved; `_row_holds` gains a selection by data tokens; the K2 leg accepts two more tokens | selection renders text, it blocks nothing | "census: no new blocking unit" |

Checks added or altered — owner and census class (AR-29, P27):
- The 15 sited refusals (§3): no check added; each existing refusal gets an id. Owner: data (the call's or the plan's shape). Census:
  measured by t-1102 key 2 — the units named exist with roles `["conductor"]`, `waiver.*` class `safety`, the rest `shape`;
  `planning_contract.py::gate_plan_errors` roles `["qa-test-strategist"]`; no unit for `Controller.build_rework_request`,
  `Driver.delivery`, `Driver.pass_to_person`, `driver_core.mr_record`. Unchanged; the new sites sit in non-transports. Final word:
  `test_judgment_census.py` (slow, canon).
- The key-4 tail (F1): a text change of an existing refusal; no check altered. Owner: data (presence of the revision mark).
- `no_move:class` on the legacy road (`Driver.pass_to_person`): an existing check (`PO.question_rule`) gets its id. Owner: data
  (a class id from a closed list, a non-empty `checked`); whether the question is really the person's stays the conductor's judgment,
  accepted by the person (P27). Census unchanged.
- S8 rows `driver_stage_s8s9:delivery.action` / `.mr`: tell two existing code readings (closed `action` list; `mr_record` shape).
  Owner: data. Census class shape; no new unit.
- `stage_joints._row_holds` answer selection and `_page_leg` token set: data (tokens of a closed list). Not blocking units; if
  `test_judgment_census` names them, the builder reports it.
- `tools/controller-blocks-gen.py` unwrap (B2): a forge tool outside the package; no census.

Commit lines (one commit per stream). Form: `tools/architecture_gate.py` — the only carrier of the grammar; not copied here.
Prescribed content:
- A: `architecture: AR-9, AR-13, AR-15, AR-20, AR-29 -- command refusals carry their row ids at the refusing site, texts unchanged
  but the one named unmarked-revision door; the controller walk reads a wrapped message as its bare one` and
  `judgment: none -- ids attach to existing refusals and the walk keeps every route; no check is added or moved`.
- B: `architecture: AR-1, AR-10, AR-12, AR-13, AR-14, AR-15, AR-16, AR-17, AR-20, AR-22, AR-24, AR-28, AR-29 -- one told block outside
  the refusal cut on all three conductor launches, selected by answer tokens; person texts unchanged` and
  `judgment: none -- the block tells existing code checks; no check is added or moved`.

FR walk (owed by each builder for its files):
- A — refusals: FR-1/FR-2 texts unchanged, expected/door on the Record; FR-2 the key-4 door now names a door the conductor can use
  (`rework_stage`); FR-59 unreadable row → the factory-defect sentence of `refusal()`.
- B — text a person reads: APPLICABLE (t-1102 B3 / key 2). The legacy cap Person text (`no_move_legacy`) is byte-identical (the told
  block is not in `refusal`); the S8 Person texts are byte-identical (the Record dies at `said.rstrip()`); the new S8 `mr` run-log line is
  plain words with no internal id in its text (FR-6); the key-4 line, if a gate packet shows it, is plain words (FR-6, A's walk).
  The conductor prompt itself is not a person's text.
- C — FR-14 output shapes additive (`exc.records` an attribute; the prompt gains one block); FR-38 the requirement before the work on
  all three launches. D — FR-16 literal ids; FR-17 one renderer wired at every launch. E, F — not touched. G — FR-30 English ASCII,
  FR-32 a table row per site and per launch kind, FR-54 siblings (§7 common).

---

## §2 Measured state (read; "at build" = the builder measures)

| fact | carrier | value |
|---|---|---|
| told counters | W `stage_joints.py --check` (t-1102 rerun) | rows 273, unsited 17 = 6 `controller:*` of T9a + 11 `first_look:put.*`; clean |
| dry ledger | W `dry_exits.py --check` (t-1102 rerun) | 0 discrepancies; `unwalked` raised 231 above base 39 |
| conductor rows today | W `stage-joints.json` | `no_move:options`, `:prose`, `:class` (`when: ["conductor_answer"]`), `:args` (`["move:rework_stage"]`); file order |
| `rows_for` order | W `stage_joints.rows_for` docstring | "File order" — expected row lists follow the insertion position fixed in §3 |
| `_row_holds` conductor branch | W `stage_joints._row_holds` | only `move:<id>` tokens are evaluated; any other token holds; facts None → all hold |
| K2 conductor leg | W `stage_joints._page_leg` | a conductor row's `when` must hold `conductor_answer` or a `move:` token |
| A24 ids in the five files | `refusal_registry.py` REGISTRY (t-1102 F4; read :1011) | `waiver:WV-placeholder-block` (function `record_refusals`, guarantor `PLACEHOLDER_RE`) is the SAME refusal as r1's row 7; families `waiver:CTRL-next-blocked`, `waiver:WV-*`, `stage_done:SD-*`, `controller:CTRL-*` exist; the other 14 ids map to none of them |
| sub-id sited | `stage_joints._is_sited` | `planning_contract:plan.unmarked_revision` counts sited via `planning_contract:plan` |
| `row_for` fallback | t-1102 F10 | `planning_contract:*` aggregator row exists; the other 14 families have no `<stem>:*` row |
| launches | t-1102 key 1 (Grep `run_claude\(\s*['"]conductor` -i, control `conductor\.md` system_file lines) | 2 `run_claude("conductor"` sites (`Driver.conductor`, `driver_stage_s8s9` delivery); `_ask_conductor` callers 3 (`_no_move` first ask, its refused re-ask, `no_move_legacy`); `pass_to_person` callers 1 (`no_move_legacy`, read W) |
| where `refusal` goes in `Driver.conductor` | W `Driver.conductor` | `ConductorSpent(count, refusal)`; `named_files(refusal, roots)` (fills the `CONDUCTOR_FILES` window); `## The refusal` + `refusal.strip()[:6000]`; `journal_conductor(refusal=refusal[:2000])` |
| legacy cap Person | W `Driver.no_move_legacy` | `Person("conductor", f"The conductor was called {spent.count} times at {self.boundary} and the block stands. Last refusal:\n\n{spent.refusal}\n\nWhat should happen? …")` |
| re-ask | W `Driver._no_move` | `self._ask_conductor(text + "\n\n## Your options were refused\n" + rule + "\n" + NM.rework_args_list(facts), state)` — appended AFTER the state text (F-8) |
| test fakes of `Driver.conductor` | Grep `def conductor\(|\.conductor = ` over W `scripts/tests` | ≈ 25 fakes in ≈ 12 files with the CLOSED signature `(text, *, words="", files=None, words_file=None)` (e.g. `test_story_run_refusals.py`, `test_story_run_gate_repair.py`, `test_person_owned_paths.py`, `no_move_seam_common.py`, `test_conductor_doors.py`); a new keyword argument raises TypeError in each (F-9) |
| Driver attribute registry | W `scripts/tests/fixtures/driver-layers.json` | instance attributes have rows (`conductor_calls`, `_in_no_move`); F adds `conductor_head` (`set_in_init: false`, FV2-94) — precedent for `conductor_told` |
| controller imports | W `controller.py` Grep `^import |^from ` and `\bDV\b` (0; control on `waiver.py` → 2) | no module-level `detector_verdict` import; local `refusal` NAMES exist (`raise StateConflict(refusal)` in `validate`), so a bare `refusal` import would be shadowed → use `import detector_verdict as DV` |
| `driver_conductor.py` imports | W | no `DV`, a parameter named `refusal` in `conductor` → `import detector_verdict as DV` |
| `driver_stage_s8s9.py` | W | `import delivery_verdict as DV` LOCAL in one method (`:194`); `except Refusal as refusal` in `stage_S8`/`stage_S9` methods (not in the delivery method) → `from detector_verdict import refusal` at module level (planning_contract precedent); no `no_move` import today |
| `_merged` / `_raise_all` | W `Controller._merged`, `_raise_all` | `_merged` does `message = str(message)` (the id is lost); one problem → `raise cls(message)`; several → `COMPOUND_HEAD` text |
| readers of a Record in `exc.args[0]` | t-1102 F3 (Grep `told_fields(`, `spoken(`, `.args[0]` over scripts) | `role_cli.run_guarded` only; none of controller/waiver/stage_done/source_exclusions is a `role_cli` command → F-2 (a) is additive |
| `mr_record` | `driver_core.py:415-426` (t-1102 F2) | returns `""` (not None) for no record |
| controller walk | `tools/controller-blocks-gen.py` (read :1-30, :305-510) | `sys.argv[1]` = OUTPUT path (`main`); head = FIRST string literal of the segment (`collect_rows.block`, `LIT`); route by `classify` / `BY_SEGMENT` (segment keys); 355 blocks, 0 unclassified (t-1102) |
| the package's twin walker | W `scripts/tests/test_controller_blocks.py` `blocks_in_source.Walk.block` (read whole) | the SAME head-literal reading; key `(function, class, head[:110])` compared with the rows of `design/controller-blocks.md` both ways → a wrapped site fails "every block has a row" unless this walker unwraps too (NOT in t-1102; found here) |
| key-4 writer | t-1102 F1 (`driver_dispatch.py:2800-2845`) | the revision mark is written only by `planning_contract.project_plan`, called only from `Driver.s3_project` at S3 strategist dispatch completion; no conductor command runs it; `gate_preflight.check_planning_contract` door "repair the plan rows (a strategist rework) before the gate" is the true road (read W `gate_preflight.py:1928`) |
| key-4 text readers | Grep `reruns the S3 step|never the role\)` over W `PKG` (hit = the carrier itself, the control) | only `planning_contract.py`; `test_story_run_s3_windows.py` reads the prefix `missing coverage_contract_revision` only (t-1102) |
| "unmarked stays bare" pins | `test_detector_verdict.py` (root checkout) :1845 docstring, :1981-1983 `bare = …` `(1, [""])` | flip in A (E17) |
| `NOTHING_CHECKED` text | W `no_move.py` | "- none: code checks nothing of this launch beyond your answer's form above"; tests compare with the constant (`test_controller_doors.py`), the literal is also in the historical mech spec |

Measured premises owed AT BUILD (command; verbatim tail into the report):
1. A, before any edit: `python -B <tree>/PKG/scripts/stage_joints.py --check` → baseline `rows R0 … unsited U0` (U0 = 17 expected).
2. A, after the sites: same → `rows R0`, `unsited U0` (sites alone change nothing).
3. B, before any edit (on its base): same → `rows R1`, `unsited U0`; after: `rows R1 + 17`, `unsited U0`.
4. B: `( cd <tree>/PKG && python -B scripts/tests/dry_exits.py --check )` → `0 discrepancies`; `unwalked` credit = its base + 17.
5. B, size per launch kind (chars of the told block, of `## The refusal` text, of the whole prompt): (i) moves road, no move open;
   (ii) `go_on_as_is`+`story_fact`+`person_does`+`stop_here`; (iii) rework open; (iv) gate A with `rework_stage`+`go_on_as_is`+
   `approve_gate`+`story_fact`; (v) legacy; (vi) S8. Reported (AR-12), no ratchet.
6. A and B: `python -B <tree>/PKG/scripts/selftest.py --limits --lang` before and after.
7. A: the walk, BEFORE the edit (positive control): `python -B <tree>/tools/controller-blocks-gen.py <scratchpad abs>/cb-before.md`,
   then a byte compare with `<tree>/PKG/design/controller-blocks.md` → equal.

---

## §3 N1: the 15 rows, their sites, the sited form (stream A sites; stream B rows)

Rule for every site (EC-1, EC-2 of the finish spec §6 "common"): the text is byte-identical — ONE named exception, the key-4 tail of
row 15 (F1; the owner's word 17.11.2026 "fixed in the round", Lead decision on r1). The id is written at the caller that knows the
requirement; a helper with more than one caller carries no id; one literal per branch (a conditional check argument is a scanner walk
error). Story-state refusals (StateConflict / FR-46) stay bare (F-P2 (a)) — ONE named exception, row 4 (below).

EC-2 and `build_rework_request` (t-1102 F7): rows 2, 3 and 5 (c) site inside `Controller.build_rework_request` (callers: `controller.main`
and `story_step.py` — the code-built rework) and `release_dispatch` (1 caller). `build_rework_request` is the rework COMMAND's own body,
not a helper: its requirement is the same on both roads (S-3 logic). On the `story_step` road the Record dies at the CLI/str; the id is
a ratchet literal there.

Walk-preserving form (B2, new here): a site that maps several problems never writes a NEW `(<RefusalClass>, …)` tuple literal or a new
`raise <RefusalClass>(` — it binds the class to a name: `[(cls, DV.refusal("<id>", m)) if cls is ValueError else (cls, m) for cls, m in problems]`.
Invariant: the walk's block count stays at its baseline (355 by t-1102; measured at build), so no new block row and no UNCLASSIFIED.

| # | row id | `when` | refusing site(s) | sited form |
|---|---|---|---|---|
| 1 | `controller:rework.call` | `move:rework_stage` | (a) `controller.main`: `root, problems = _cli_story_root(a)` then `Controller._raise_all(problems)` (serves every operation); (b) `main`: `reason = person_words.read(a.reason, a.words_file, "--reason")` (raises `person_words.WordsRefused`, shared helper) | (a) only when `a.operation == "rework"`: the walk-preserving comprehension above with this id; the `StateConflict` "initialize task before work" stays bare (S-R14); (b) `except person_words.WordsRefused as exc:` re-raise the SAME class with `DV.refusal("controller:rework.call", str(exc))` |
| 2 | `controller:rework.args` | `move:rework_stage` | `Controller.build_rework_request`: every `problems.append((ValueError, <literal text>))` in its own body (stage, purpose, blank reason, reopen-a-closed-story, cause, the three `--candidates` problems, cases S4+, outside scope, plan rows, no accepted dispatch (plan / window / live / none), S5 several windows) | `(ValueError, DV.refusal("controller:rework.args", <same text>))`; the two `StateConflict` holds stay bare; `_rework_kind` → row 3; `_rework_block_problems` / `_half_membership_problems` extends stay bare |
| 3 | `controller:rework.runner_half` | `move:rework_stage` | `build_rework_request`: `problems.extend((ValueError, text) for text in kind_problems)` | `(ValueError, DV.refusal("controller:rework.runner_half", text))` |
| 4 | `controller:rework.cap` | `move:rework_stage` | `Controller.validate`, dispatch branch: the three `raise StateConflict(blocking[0] + …)` of the repair cap | `raise StateConflict(DV.refusal("controller:rework.cap", blocking[0] + <same rest>))`. The named exception to "StateConflict stays bare" (t-1102 F6): the cap is a requirement the conductor can be told BEFORE the work, because the repair ledger is readable at launch; it is not a state the call cannot know. The id rides on every repair-loop dispatch, the driver-built rounds included (`story_step finish --needs-author`): one requirement, one id (S-3) |
| 5 | `controller:release.call` | `move:release_and_restart` | (a) `main` `_cli_story_root` problems when `a.operation == "release"`; (b) `main` `words = person_words.read(a.words, a.words_file, "--words")` (7 operations share it); (c) `Controller.release_dispatch`: the two literal appends (no `--dispatch` with not one open; blank words) and `problems.append(self._unknown_dispatch(identifier, dispatches))` | (a) as row 1 (a) with this id; (b) a `try` around the shared read; its `except` re-raises with this id ONLY when `a.operation == "release"` (literal in that branch), any other operation re-raises unchanged; (c) literal appends wrapped; `_unknown_dispatch` (5 callers) is wrapped at THIS caller: `cls, m = self._unknown_dispatch(identifier, dispatches); problems.append((cls, DV.refusal("controller:release.call", m)))`; the `StateConflict` "holds nothing back" stays bare (S-L1) |
| 6 | `waiver:block.call` | `move:go_on_as_is` | `waiver.main`: `ap.error(str(exc))` after `person_words.read`; `ap.error("--task, --stage, --block and --decision or --words-file (the person's words) are all required")` | (i) words: `except person_words.WordsRefused as exc:` then in the dispatch order of the forms (remark, revoke, stage/block, gate — confirmed t-1102 key 1): `if ns.remark: ap.error(DV.refusal("waiver:remark.call", str(exc)))`; `if not ns.revoke and (ns.stage or ns.block): ap.error(DV.refusal("waiver:block.call", str(exc)))`; else `ap.error(str(exc))`; (ii) `ap.error(DV.refusal("waiver:block.call", <same text>))` |
| 7 | `waiver:WV-placeholder-block` (t-1102 F4: the A24 id of this refusal; r1's `waiver:block.placeholder` would give one refusal two ids) | `move:go_on_as_is` | `waiver.record_refusals` (1 caller): `return [f'waiver: the block "{match}" still holds the placeholder …']` | `return [DV.refusal("waiver:WV-placeholder-block", f'…same…')]` |
| 8 | `waiver:block.stand_gap_id` | `move:go_on_as_is` | `record_refusals`: `return [NO_GAP_ID]` | `return [DV.refusal("waiver:block.stand_gap_id", NO_GAP_ID)]` |
| 9 | `waiver:block.grant_pattern` | `move:go_on_as_is` | `record_refusals`: `return test_path_grants.pattern_errors(...)` | `return [DV.refusal("waiver:block.grant_pattern", e) for e in test_path_grants.pattern_errors(...)]` |
| 10 | `waiver:block.standing` | `move:go_on_as_is` | `waiver.run_stage`: `print(unmatched_text(task, stage, match, standing), file=sys.stderr)` on `kind == "unmatched"` | `print(DV.refusal("waiver:block.standing", unmatched_text(...)), file=sys.stderr)`; `BlockNamesError` and "no pipeline.json" stay bare |
| 11 | `waiver:remark.call` | `move:go_on_as_is` | `waiver.main`: words (row 6 (i)); `ap.error("--remark needs --task, --stage and --text or --words-file (the person's words)")` | row 6 (i) branch; `ap.error(DV.refusal("waiver:remark.call", <same text>))` |
| 12 | `source_exclusions:revoke.call` | `move:revoke_exclusion` | `source_exclusions.main`: the "give exactly one of --load FILE, --show, --revoke …" print; the `_task_root` ValueError print; the "--revoke needs --words …" print | `print(DV.refusal("source_exclusions:revoke.call", <same text>), file=sys.stderr)`; module-level `import detector_verdict as DV` beside the other imports (the file has none); argparse / `hooklib.exact_options` refusals stay bare |
| 13 | `source_exclusions:revoke.target` | `move:revoke_exclusion` | `main`: the "no exclusion `{args.revoke}` in {args.task}; it has: …" print on `status == "unknown"` | `print(DV.refusal("source_exclusions:revoke.target", <same text>), file=sys.stderr)`; "no record, nothing to revoke" stays bare |
| 14 | `stage_done:set` | `move:story_fact` | `stage_done.parse_sets`: `raise ValueError(f"--set takes key=value, not `{item}`")`; `out[key.strip()] = coerce_value(key.strip(), raw)` (`coerce_value` 4 callers) | `raise ValueError(DV.refusal("stage_done:set", <same text>))`; `try: … coerce_value(...) except ValueError as exc: raise ValueError(DV.refusal("stage_done:set", str(exc))) from None`; `current_code_diff_refusal` stays bare |
| 15 | `planning_contract:plan.unmarked_revision` | `move:approve_gate` (F-3 (a)) | `planning_contract.gate_plan_errors`: `… + unmarked_revision_errors(rows, plan_contract_mode)` (1 caller) | `+ [refusal("planning_contract:plan.unmarked_revision", line) for line in unmarked_revision_errors(rows, plan_contract_mode)]`; the docstring sentence "stay bare … lands with node T9c (F-W4 (b))" says they carry this id; AND the key-4 tail (below) |

Key-4 fix (t-1102 F1; Lead decision: fixed in this node), file `scripts/planning_contract.py`, function `unmarked_revision_errors`:
the literal tail `"did not run for this plan: the conductor reruns the S3 step (never the role)"` becomes
`"did not run for this plan: a strategist rework of S3 writes it when that rework completes"`. Nothing else of the line changes.
It then names the same road as `gate_preflight.check_planning_contract`'s door; `gate_preflight.py` is untouched. The expected text of
its table row is THIS card's sentence, never the new code's output.

Module imports (stream A): `controller.py` gains module-level `import detector_verdict as DV` (local `refusal` names exist there: §2);
`source_exclusions.py` the same; `waiver.py`, `stage_done.py` already bind `DV`; `planning_contract.py` already imports `refusal`.

Row texts. Every row: `roles: ["conductor"]`, `stages: ["*"]`, `door_needs: "none"`, producer entry told `{"page": true}`, `demands: []`,
`joint: null`, the T9c row form. INSERTION POSITION (B): the 15 rows right after the `no_move:args` row, in this table's order, then the
two S8 rows (§4 item 8) — so `rows_for` (file order) gives the expected lists of §7 B.
- Rows 1, 3, 4, 5, 6, 8-13: `requirement` and `door` VERBATIM from part3 §1 (accepted t-489). Row 7: part3's `waiver:block.placeholder`
  sentence and door, verbatim, under the A24 key.
- Row 1: part3's sentence minus "that holds the story journal" (that refusal is story-state and stays bare: a sentence never claims a
  refusal its id does not carry, EC-8).
- Row 2 (`controller:rework.args`, part3 predates FL4; Lead accepted F-1 (a)): "`--stage` is one of S0-S9; `--purpose` is one of
  PURPOSES; the reason (the words) is not blank; `--cause` is one of REPAIR_CAUSES; from S4 on `--cases` names at least one case and every
  case is inside the approved scope; every `--rows` id is a row of the approved plan; `--candidates` names bug candidates the story lists,
  for the S7 author only and never with `--cases` or `--rows`; the role has an ACCEPTED dispatch on that stage (on S5: of the kind the
  purpose names, the plan for `s5_plan`, else a window); on S5 the cases of a code-typed reason lie in ONE window (a person's words over
  several windows are not refused)." Door: part3's.
- Row 14 (`stage_done:set`; the T1r-cards spec O-1 sentence, `20261114-told-before-work-t1r-cards-spec.md:342`, read, plus t-1102 F8
  read against `stage_done.SIDE_ATTRS` and the `sides_unknown` refusal; Lead accepts, EC-8): "`stage_done.py --set` takes `key=value`
  items and writes only the keys it lists: `implementation_source`, `size`, `environment_pending`, `no_trace`, `retro_mode`, `environment`,
  `parent_feature`, `sides.<name>.<attribute>` and `sides_unknown`; a closed key takes one of its listed words (true/false for the two
  flags, a reality word of `references/side-realities.json` for a side's `reality`, `retro_mode` only `full`), `parent_feature` is the
  parent's key alone, and a person's word does not widen the list; a side's attribute is one of `reality`, `deliverable` (true/false),
  `settles_by`, `reference`, `source`, `at`, and `sides_unknown` is cleared with `sides_unknown=` or written as `.at`/`.why`."
  Door: "give the value in the key's form, or have the script that owns the field write it".
- Row 15 (T9c report Q3 sentence, corrected by t-1102 F1): "A plan row the S3 projection did not stamp carries no
  `coverage_contract_revision`, and gate A's gate-inputs refuses the whole plan while any row is unmarked; code writes the mark when an
  S3 strategist dispatch completes (S3 closing or a rework of S3)." Door: "a strategist rework of S3 writes it when that rework completes".
- Not in this node (E-T9c-2): `waiver:carry.call`, `.old_key` (the `words_carry` move is not in `conductor-actions.json`),
  `controller:rework.runner_half.manual_block`, `controller:release.commit`, the 10 helper bodies of part3 §1.1, `stand_health:probe`.

### §3a F-2 (a) in `controller.py` (stream A; Lead F-2 = (a), with t-1102 F3)

- `Controller._merged`: counts and dedups by `str(message)` as today and appends the ORIGINAL object when its count is 1; a folded
  message (`"<message> (×K)"`) is a plain str and LOSES the id (E7; S-11 says why it is not re-wrapped).
- `Controller._raise_all`: one merged problem → `raise cls(message)` with the original object (a Record keeps `check`); several → the
  exception is built from the `COMPOUND_HEAD` text as today, then `exc.records = [m for _, m in merged if getattr(m, "check", "")]` is
  set as an ATTRIBUTE before `raise` — never a constructor keyword (`ValueError` / `StateConflict` take none: TypeError).
- Readers (t-1102 F3, trail there): the one reader of a Record in `exc.args[0]` is `role_cli.run_guarded`; none of these commands is a
  `role_cli` command; `hooklib.block` receives no controller exception. Additive on every road found. Texts byte-identical.

### §3b B2 — the controller walk reads a wrapped message as its bare one (stream A)

Both walkers change together, same commit (a producer and its reader, rule 10; F-10):
- `tools/controller-blocks-gen.py` `collect_rows.V.block` and `scripts/tests/test_controller_blocks.py` `blocks_in_source.Walk.block`:
  before taking the head literal and the segment, the MESSAGE node (the second element of a collected tuple; the first argument of a
  raised call) is UNWRAPPED when it is an `ast.Call` whose `func` is the Name `refusal` or the Attribute `DV.refusal` (value Name `DV`,
  attr `refusal`) with at least two positional arguments: the segment used for `head`, `seg` and every `BY_SEGMENT` key is the node's
  source with that call's source replaced by the source of its SECOND argument, unwrapped again if that is itself such a call. Whitespace
  is normalised after the replacement, exactly as today.
- ERROR DIRECTION (a reused reading in a detector role): the unwrap may err only toward NOT unwrapping. A call it does not recognise
  stays wrapped → its head becomes the id → the generator prints UNCLASSIFIED and writes nothing, and `test_controller_blocks` fails
  "not walked": loud, never a misroute and never a hidden block. Adversarial inputs that stay on the safe side (each a table row):
  `refusal("x")` (one argument: not unwrapped); `DV.refusal(check="…", problem="…")` (keywords: not unwrapped); `self.refusal(id, "x")`
  and `other.refusal(...)` (not `DV`: not unwrapped); `raise StateConflict(refusal)` (a Name, not a call: untouched, its `BY_SEGMENT` key
  `raise StateConflict(refusal)` keeps its route); a nested `DV.refusal(a, DV.refusal(b, "t"))` (unwrapped twice, head `t`);
  `DV.refusal(id, f"…{x}…")` and `DV.refusal(id, blocking[0] + "…")` (head and route as the bare form).
- Block count, heads, routes and `design/controller-blocks.md` stay byte-identical; `design/controller-blocks.md` is NOT owned —
  any byte of difference is a STOP (the unwrap is wrong), never a regeneration.

---

## §4 N2: one renderer, one placement, three launches (stream B)

1. `no_move.checks_section(open_ids, answer) -> str` (new): returns `WHAT_CODE_CHECKS + "\n\n"` followed by NOT KNOWN (unreadable,
   `SJ.read_rows()`, with the reader's reason), or the `told_line`s of `SJ.rows_for("conductor", ["*"], {"moves": list(open_ids),
   "answer": list(answer)}, data)`, or `NOTHING_CHECKED`. It is the T9c block moved out of `moves_section`.
   `moves_section` no longer renders it: the T9c lines (the late `import stage_joints`, `WHAT_CODE_CHECKS`, NOT KNOWN, `rows_for`) leave it,
   and its output returns to the two headings (`## Moves open here`, `## Answers this question already takes`). E-T9c-5 (the section after
   the two moves headings) is a pinned T9c position that CHANGES in this node to "its own block before `## The refusal`" (t-1102 B1 cost).
2. Answer tokens (data): `when_kinds` gains `conductor_options` and `delivery_answer`. Tuples in `no_move.py`:
   `MOVES_ANSWER = ("conductor_answer", "conductor_options")`, `LEGACY_ANSWER = ("conductor_answer",)`, `DELIVERY_ANSWER = ("delivery_answer",)`.
   Rows: `no_move:options` and `no_move:prose` `when` → `["conductor_answer", "conductor_options"]` (ALL must hold; the legacy road does
   not validate options or prose); `no_move:class` stays `["conductor_answer"]`; `no_move:args` unchanged.
3. THE TOLD BLOCK (B1 = (a), Lead 17.11.2026). `Driver.conductor` prints the told text as its own block between the frame lines
   ("Driver flags …") and `""`, `## The refusal`: list items `"", told.strip()` inserted there when `told.strip()` is non-empty; when it is
   empty nothing is inserted and the prompt is byte-identical to today. The told text is NOT part of `refusal`: never in the 6000 cut,
   never in `named_files(refusal, roots)`, never in `journal_conductor(refusal=…)`, never in `ConductorSpent.refusal`.
   POSITIONAL INVARIANT (the order of blocks in the moves-road and legacy prompts):
   frame lines → `## What code will check in this launch` (WHOLE, never cut) → `## The refusal`: [lead] → `## Moves open here` →
   [`## Answers this question already takes`] → [`## The options at this gate` (prices)] → [`## The person's choice`] →
   [`## Your options were refused` (re-ask, F-8 (a))] → the refusal details (state text) → `## \`story_step.py where\`` →
   [`## The person's words`] → [`## Files the refusal names`] → the JSON-form line LAST.
   What the cut may remove: ONLY the tail of the refusal details (the state text). What always arrives whole: the told block (by
   position: outside `refusal`), the person's choice paragraph and the option prices (FV2-94's head-keep), the refused paragraph (F-8 (a)).
   What must stay unreachable: a requirement of this launch omitted or cut for size; the told block in a person's text, the journal or
   the file window.
4. The carrier of the told text (fork F-9, recommended (b)): `Driver._ask_conductor(self, text, state, told="")` sets
   `self.conductor_told = told` immediately before its one `self.conductor(...)` call; `Driver.conductor` reads
   `told = str(getattr(self, "conductor_told", "") or "")` and sets `self.conductor_told = ""` as its FIRST statement (before the cap
   check). No signature of `Driver.conductor` changes, so every test fake keeps working. New row in
   `scripts/tests/fixtures/driver-layers.json` in the form of FV2-94's `conductor_head` row:
   `{"name": "conductor_told", "owner": "driver_conductor", "set_in_init": false, "note": "TBW1-11: the told block of the next conductor call; written only by `_ask_conductor`, read and cleared first in `conductor`"}`.
5. Callers: `_no_move` first ask and its refused re-ask pass `told=NM.checks_section(open_ids, NM.MOVES_ANSWER)` (the same text both
   times: the open moves do not change between them); `no_move_legacy` passes `told=NM.checks_section([], NM.LEGACY_ANSWER)` and keeps
   `str(state.get("text") or "")` as its refusal, byte-identical. The `s1_review` exclusion from MOVES stays; `NM.EXCLUDED_KINDS` and its
   comment stay, the comment adds "the launch still lists what code checks (TBW1-11); it is excluded from moves only".
6. Legacy cap (B3): `ConductorSpent.refusal` is the legacy state text, so the Person text "… Last refusal:\n\n{spent.refusal}\n\n…" is
   byte-identical to today; a `LAUNCH_KINDS` row `legacy-cap` pins it and asserts `WHAT_CODE_CHECKS` is absent (it FAILS when the
   section leaks).
7. F-8 (a), recommended (the re-ask's refused paragraph is today appended after the state text, so the cut removes it first — the class
   of FV2-94): `_conductor_text` gains a keyword `refused: str = ""`; when non-empty, `"\n\n## Your options were refused\n" + refused` is
   added to the HEAD after the prices/choice and before the state text, so FV2-94's head-keep counts it. The re-ask becomes
   `self._ask_conductor(self._conductor_text(state, facts, open_ids, site, chosen, refused=rule + "\n" + NM.rework_args_list(facts)), state, told=…)`.
   The paragraph's bytes are unchanged; only its position moves. Readers `test_no_move_seam_c26_g27_f2.py:115` and
   `test_person_owned_paths.py:140` test `"Your options were refused" in <refusal text>` — still true.
8. `Driver.pass_to_person`: `rule = PO.question_rule(...)` becomes `DV.refusal("no_move:class", rule)` when `rule` is non-empty; the
   print and `file_defect` use `rule[:160]` / `rule[:300]` as before (slices give plain str, text identical). The id is a ratchet literal
   with no reader on this road. `driver_conductor.py` gains module-level `import detector_verdict as DV`.
9. `references/conductor.md:99`: the sentence "Without a `why_person` class or with an empty `checked`, it is refused once." becomes
   "What code checks of your answer is listed in each launch under `## What code will check in this launch`." (F-5 (a)); the line's first
   sentence ("with nothing to ask, say `stop` …") and every other line stay.
10. S8 (`driver_stage_s8s9`, the delivery launch; its prompt has no cut): the prompt list gains two items right after
    `section.strip()`: `""` and `NM.checks_section([], NM.DELIVERY_ANSWER)`; the existing `""` and the JSON-form line follow unchanged, so
    one blank line precedes the JSON line and it stays the list's last item (t-1102 F12). Module-level `import no_move as NM` and
    `from detector_verdict import refusal` (never a second `DV`: `delivery_verdict` is bound as `DV` locally there). Two rows (F-4 (a)):
    - `driver_stage_s8s9:delivery.action`, `when: ["delivery_answer"]`: "The answer's `action` is `continue`, `ask_person` or `stop`; any
      other action is read as no answer and the person is asked in words." Door: "answer with one of the three". Site: the
      unrecognised-action branch, `raise self.delivery_person(refusal("driver_stage_s8s9:delivery.action", <the same text expression>), why_person=…)`.
      The Record dies at `said.rstrip()`: a ratchet literal only, no reader (F12); the person's text is byte-identical.
    - `driver_stage_s8s9:delivery.mr`, `when: ["delivery_answer"]`: "With `continue`, `mr` is the Draft MR's link, id or number when one
      was opened or already exists, and empty when none; any other value is read as no record, and the delivery is marked without an MR."
      Door: "give the MR's link or id, or leave it empty". Site (the node's one behaviour addition, F2): in the `continue` branch, after
      `mr = mr_record(verdict.get("mr"))`: `given = str(verdict.get("mr") or "").strip()`; when `given` and not `mr`:
      `print(refusal("driver_stage_s8s9:delivery.mr", f"delivery: `mr` {given!r} is no record of a merge request; the delivery is marked without an MR"))`.
      The text never claims an `mr` order exists (`settle_mr_from_mark` calls one off only when it exists).
11. `stage_joints._row_holds` (conductor branch): a token that is neither `move:` nor a capability token holds iff it is in
    `facts["answer"]` when `facts["answer"]` is a list or tuple; when the key is absent, or its value is not a list/tuple (a str would make
    `in` a substring test, F11), the token holds (today's behaviour). `stage_joints._page_leg`: the conductor's selector accepts any token
    of `CONDUCTOR_ANSWER_TOKENS = ("conductor_answer", "conductor_options", "delivery_answer")` or a `move:` token; its refusal sentence
    names the tuple.
12. `NOTHING_CHECKED` drops "above" (S-8): "- none: code checks nothing of this launch beyond your answer's form" — the form line is
    below the block on all three launches now.
13. `changelog.d/tbw-t9c.md` (T9c's fragment, on main after T9c): "now ends its moves with a section" becomes "now carries a section"
    (S-14), so the release notes do not state the old position; B's own fragment says where the block stands.

---

## §5 Edges (each with its invariant)

- E1 a `when` token that cannot be evaluated (unknown token, facts without `answer`, a non-list `answer`): the row HOLDS. Invariant: a
  row is never omitted because a fact could not be read; over-telling is the safe side (`_row_holds` direction).
- E2 a readable file with no row for the launch: `NOTHING_CHECKED`. Invariant: never printed while a row of this launch's tokens and open
  moves exists; with the real file it is unreachable on all three launches (`no_move:class` holds on moves and legacy, the S8 rows on S8).
- E3 unreadable `stage-joints.json` (absent, OSError, not JSON, 0 bytes, not an object, schema mismatch, `joints` not a list): NOT KNOWN
  with the reader's reason on all three launches. Invariant: an unknown is never `none`, never a decision; nothing reads the block.
- E4 a rework with no args yet: the `move:rework_stage` rows hold once the move is open. Invariant: the block depends on open moves and
  answer tokens only, never on the answer it precedes.
- E5 TEMPORAL — A merged, B not (t-1102 F10): `refusal("planning_contract:plan.unmarked_revision", …)` resolves to the `planning_contract:*`
  aggregator row (`expected` "" and its door); the other 14 ids get the unreadable sentence. No printer shows either; `rowless` does not
  move (t-1102 key 2). Rows before sites cannot happen (B starts after A). Invariant: `told_ratchet.unsited` never rises.
- E6 TEMPORAL — the `answer` key: before, no caller passes it and every non-move token holds; after, the three launches pass it.
  Invariant: a caller that omits it gets more rows, never fewer.
- E7 Records through `_raise_all` (F-2 (a)): one problem keeps its Record; several set `exc.records`; a folded `(×K)` message loses its
  id. Invariant: the raised text is byte-identical in every case.
- E8 `_noted` rebuilds the last message by f-string (16 callers, not edited): that problem loses its id; text identical.
- E9 `ap.error` / `print` sites: the Record prints as its text and dies there. Invariant: stderr bytes and exit codes unchanged.
- E10 POSITIONAL — `waiver.main` words refusal follows the dispatch order (remark, revoke, stage/block, gate). Invariant: a revoke or gate
  form never carries a block/remark id; a remark never carries the block id.
- E11 POSITIONAL — `controller.main`: the id mapping happens only inside `a.operation == "rework"` / `"release"`. Invariant: no other
  operation's refusal carries a rework/release id.
- E12 POSITIONAL — the block order of §4 item 3. Invariant: the cut removes only the state text's tail; the told block, the choice, the
  prices and the refused paragraph arrive whole. The told block itself has NO cap (a requirement is never dropped for size); its size is
  reported (premise 5). A told text over 6000 chars is legal and changes nothing of the cut.
- E13 legacy road: `no_move:options` / `:prose` / `:args` and every command row never hold. Invariant: the legacy launch claims only what
  `pass_to_person` checks.
- E14 S8: no `no_move:*` row holds. Invariant: the S8 launch claims only `action` and `mr`.
- E15 `pass_to_person` with an empty rule: no Record, path unchanged.
- E16 conductor.md edit vs `design/role-rules.json`: `role-rules.json` has no `why_person` hit (t-1102); if `selftest.py --limits` still
  names the removed sentence → STOP, F-5 (b) (re-word it to quote `no_move:class`), report verbatim.
- E17 tests pinning "unmarked stays bare" (`test_detector_verdict.py` docstring near the T7b function; `bare = PC.gate_plan_errors(...)`
  expecting `(1, [""])`): the expectation flips to `(1, ["planning_contract:plan.unmarked_revision"])` — from this card, not from output.
- E18 every `move:<id>` named is a `moves[].id` of `conductor-actions.json`: `rework_stage`, `release_and_restart`, `go_on_as_is`,
  `revoke_exclusion`, `story_fact`, `approve_gate`.
- E19 the walk unwrap (§3b): direction and adversarial inputs as stated there. Invariant: no block is hidden, merged or misrouted; an
  unrecognised wrapper is LOUD (UNCLASSIFIED / "not walked").
- E20 the walk-preserving mapping (§3): Invariant: no new `(<RefusalClass>, …)` tuple or `raise <RefusalClass>(` in `controller.py`;
  block count = baseline.
- E21 B3 legacy cap: Invariant: `spent.refusal` never holds the told block; the Person text is byte-identical (row `legacy-cap`).
- E22 F5 closed by B1 (a): `named_files` scans `refusal` only, so row paths (`references/block-names.json`,
  `references/conductor-actions.json`) never take the `CONDUCTOR_FILES` window ahead of the state text's files; the journal's
  `refusal[:2000]` stores the refusal, not the block. Invariant: the file window and the journal are as today.
- E23 the told carrier (F-9 (b)): set only by `_ask_conductor`, read-and-cleared first in `conductor`. Invariant: a block reaches only the
  call it was set for; a direct call of `Driver.conductor` (tests) gets no stale block; a fake `conductor` ignores it and still runs.
- E24 S8 `mr`: `None`, `""`, `"   "` → not given (no line); a given value with record shape → no line; `"N/A"`, `"none"`, `"not opened"` →
  one line. Invariant: the line is printed only for a GIVEN value code read as no record; no state, mark or order changes because of it.
- E25 F-8 (a): with FV2-94's head-keep, a head longer than 6000 widens the cap to the head (FV2-94's own rule); the state text may then be
  cut whole. Invariant: the refused paragraph is never cut while the state text survives.
- E26 the key-4 tail: Invariant: no other byte of the line changes; the prefix `missing coverage_contract_revision` (read by
  `test_story_run_s3_windows.py`) is untouched.

Pinned texts that stay byte-identical: every refusal text of §3 but the key-4 tail (EC-1, expected from a byte copy of the OLD files);
the stderr lines of `waiver`, `source_exclusions`, `stage_done`; `controller.py`'s JSON `error` lines; `design/controller-blocks.md`;
the moves-road `## The refusal` text apart from the section leaving it and F-8's move; the frame of `Driver.conductor` when no told text is
given; the S8 JSON-form line; the legacy cap Person text; every line of `conductor.md` but the one sentence; `NM.EXCLUDED_KINDS`;
`audit_factory.CONDUCTOR_SITES`.

---

## §6 Effects on counters and ledgers (numbers at build)

| counter | before | after | who |
|---|---|---|---|
| `told_ratchet.unsited` | U0 (17 in W) | U0 — no raise (every new row lands with its literal; the 17 are T9a's and `first_look:put.*`) | nobody |
| stage-joints rows (K1 pin, `test_stage_joints.py`) | R1 (B's base) | R1 + 17 (15 command/plan + 2 S8) | B, labelled "+17 TBW1-11 conductor rows" |
| `rows-for/real` conductor expectation (`test_stage_joints.py`) | the four `no_move:*` ids | + the rows holding for its fixture's `{"moves", "answer"}` | B |
| `gates.json` `unwalked` credit (`raised_by`) | base of B (231 in W) | + 17 (one joint row + one `raised_by` per new row, t-1087 form: reach `unwalked`, why "TBW1-11 conductor rows, <date>: reached by the conductor's launches, not judged by a row of their own") | B |
| `driver-layers.json` | — | + 1 attribute row `conductor_told` | B |
| controller walk | 355 blocks, 0 unclassified | unchanged; `design/controller-blocks.md` byte-identical | A |
| `role-load.json` | no conductor row | unchanged; sizes reported | — |
| `told-ratchet.json` (`rowless`, `untold`) | — | t-1102 key 2: `rowless` does not move between A and B; no told-ratchet baseline row for these units; a shrink caused by the A24-keyed row 7 is named in B's report | closing node edits the file |
| `judgment-census.json` | — | no edit expected; C1 is the canon's (`test_judgment_census.py`, slow) | — |

---

## §7 Streams, owns, witness (F-6 (a): two builders; order §0a)

### Stream A — the 15 sites, F-2, the walk, the key-4 door
given: this card; part3 §1 (row texts, for reference of the sited refusals); `design/factory-rules.md`; `plans/builder-rules.md`
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\controller.py (module import; main; Controller.build_rework_request; Controller.validate repair-cap raises; Controller.release_dispatch; Controller._merged; Controller._raise_all)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\waiver.py (main, record_refusals, run_stage)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\source_exclusions.py (main, the module import)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\stage_done.py (parse_sets)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\planning_contract.py (gate_plan_errors and its docstring; unmarked_revision_errors tail)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_detector_verdict.py (new function `tbw_siting_command_sites`; the rows asserting unmarked lines are bare)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_controller_blocks.py (blocks_in_source.Walk.block unwrap; one table of wrapped/bare pairs)
C:\QAFactory\forge-repo\tools\controller-blocks-gen.py (collect_rows.V.block unwrap)
C:\QAFactory\forge-repo\tools\test_controller_blocks_gen.py (one parameterised test of wrapped/bare pairs and the adversarial rows)
C:\QAFactory\forge-repo\ai-packages\qa-factory\changelog.d\tbw-siting-a.md
non-goals: stage-joints.json; any refusal TEXT but the key-4 tail; `gate_preflight.py`; `design/controller-blocks.md` (must stay
byte-identical); `_noted`; `person_words.py`; `test_path_grants.py`; `coerce_value`; a transport (spoken/told_fields printers); the
story-state refusals; `.runner_half.manual_block`, `release.commit`, `waiver:carry.*`; census; `told_ratchet`; slow or quarantined tests; CI.
items:
- `tbw_siting_command_sites` (one table): per site (text, id): text = the OLD file's output (byte copy taken before the edit), the key-4
  line's text = §3's sentence; id = §3; a row per branch of row 6 (i) (remark / block / revoke / gate) and of row 5 (b) (release / another
  operation); `_raise_all` rows: one problem keeps the Record (`check` equal to the id), several set `exc.records` with the ids and the text
  unchanged, a folded `(×K)` problem has the text and no id (E7).
- E17 flip.
- `test_controller_blocks.py`: a table of (bare source, wrapped source) pairs whose `blocks_in_source` Counters are equal, plus one
  adversarial row (`self.refusal(...)` stays wrapped → the Counters differ).
- `tools/test_controller_blocks_gen.py`: parameterised over the §3b inputs — wrapped vs bare give the same (head, route, seg); the
  not-unwrapped inputs keep the wrapped head (negative control).
DoD:
- `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for scripts/controller.py scripts/waiver.py scripts/source_exclusions.py scripts/stage_done.py scripts/planning_contract.py scripts/tests/test_detector_verdict.py scripts/tests/test_controller_blocks.py`
  — run every printed file not in `slow_tests.json` and not quarantined, each alone; slow ones listed "judged by the batch canon".
- `python -m pytest tools/test_controller_blocks_gen.py -q` (the outside-package path's own test).
- The walk: `python -B <tree>/tools/controller-blocks-gen.py <scratchpad abs>/cb-after.md` → exit 0, no `UNCLASSIFIED`, the block count
  of premise 7; then a byte compare with `<tree>/ai-packages/qa-factory/design/controller-blocks.md` → equal. NEVER `--help`, never a
  relative path, never a path inside the repo (argv[1] is an OUTPUT path; the stray `C:/QAFactory/forge-repo/--write` of 14.11 is that
  accident — not this stream's to remove).
- `python -B ai-packages/qa-factory/scripts/stage_joints.py --check` → clean, `unsited U0`, `rows R0` (premise 2).
- `python -B ai-packages/qa-factory/scripts/selftest.py --limits --lang`.
- Negative controls (byte copy, restore by `cp`, hashes equal in the report): one wrapped site turned bare on a copy → its
  `tbw_siting_command_sites` row FAILs; the unwrap removed from the generator copy → `cb-after.md` differs or UNCLASSIFIED appears.

### Stream B — the rows, the told block, three launches
given: this card; part3 §1 (row texts); the merged T9c and FV2-94 code on origin/main; `design/factory-rules.md`; `plans/builder-rules.md`
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\no_move.py (checks_section new; moves_section loses the section; MOVES_ANSWER / LEGACY_ANSWER / DELIVERY_ANSWER; NOTHING_CHECKED; the EXCLUDED_KINDS comment)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\stage_joints.py (_row_holds conductor branch, _page_leg, CONDUCTOR_ANSWER_TOKENS)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\driver_conductor.py (module import; Driver.conductor told block and carrier read; Driver._ask_conductor; Driver._no_move callers; Driver._conductor_text `refused` keyword only; Driver.no_move_legacy; Driver.pass_to_person)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\driver_stage_s8s9.py (module imports; the delivery prompt items; the unrecognised-action branch; the mr line)
C:\QAFactory\forge-repo\ai-packages\qa-factory\references\conductor.md (the one sentence of line 99)
C:\QAFactory\forge-repo\ai-packages\qa-factory\references\stage-joints.json (the 15 + 2 rows at the fixed position; `when` of no_move:options/:prose; `when_kinds`)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\driver-exits\gates.json (joint rows + raised_by of the 17 rows)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\driver-layers.json (the `conductor_told` row)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_controller_doors.py (T9c launch rows moved to checks_section / the prompt; new tables)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_stage_joints.py (K1 rows pin and `rows-for/real` conductor expectation only)
C:\QAFactory\forge-repo\ai-packages\qa-factory\changelog.d\tbw-t9c.md (the one wording of §4 item 13)
C:\QAFactory\forge-repo\ai-packages\qa-factory\changelog.d\tbw-siting-b.md
non-goals: FV2-94's cut and head-keep logic (built on, never edited); `told_ratchet`; `told-ratchet.json`; `role-load.json`;
`conductor-actions.json`; `audit_factory.CONDUCTOR_SITES`; `NM.EXCLUDED_KINDS` membership; any refusal text; the signature of
`Driver.conductor`; the test fakes of `Driver.conductor` (F-9 (b) leaves them working); slow tests; CI.
items (one parameterised table per behaviour, `test_controller_doors.py`; expected values from §3/§4, never from new output):
- `LAUNCH_KINDS` — (launch, open moves, answer tuple) → expected row ids in file order:
  moves/no-move-open `[]` → `no_move:options`, `:prose`, `:class`;
  moves/rework-open `["rework_stage", "person_does"]` → + `no_move:args`, `controller:rework.call`, `.args`, `.runner_half`, `.cap`;
  moves/go-on `["go_on_as_is", "story_fact", "person_does", "stop_here"]` → the three + `waiver:block.call`, `waiver:WV-placeholder-block`,
  `waiver:block.stand_gap_id`, `.grant_pattern`, `.standing`, `waiver:remark.call`, `stage_done:set`;
  moves/release `["release_and_restart"]` → the three + `controller:release.call`;
  moves/revoke `["revoke_exclusion"]` → the three + `source_exclusions:revoke.call`, `.target`;
  moves/gate `["approve_gate"]` → the three + `planning_contract:plan.unmarked_revision`;
  legacy `LEGACY_ANSWER` → `no_move:class`; S8 `DELIVERY_ANSWER` → `driver_stage_s8s9:delivery.action`, `.mr`.
- One-placement rows: `moves_section` output holds no `WHAT_CODE_CHECKS`; `_conductor_text` output holds none.
- Prompt rows (the real `Driver.conductor` bound to a driver with `run_claude` replaced by a recorder; precedent:
  `test_no_move_seam_n2b_n15.py` binds `story_run.Driver.conductor.__get__(driver)`): moves road and legacy — the told block stands after
  the frame and before `## The refusal`, whole, with a state text of 7000 chars (the cut takes only its tail); the JSON line last;
  `named_files` / journal see no row path (E22); S8 — the block after the delivery section, one blank line before the JSON line, the JSON
  line last.
- `legacy-cap` row (B3): the Person text equals the old text for a given state text and holds no `WHAT_CODE_CHECKS`.
- F-8 row: a re-ask with a 7000-char state text keeps `## Your options were refused` and its rule whole.
- `UNREADABLE_ROWS` × the three answer tuples through `checks_section`.
- `ROW_HOLDS` — `_row_holds` with the `answer` key absent, a list, a tuple, a str (`"conductor_options"` → holds, F11), None.
- `pass_to_person` id row; S8 `action` (text + id) and `mr` rows per E24's inputs (line printed or not, text).
DoD (on a tree where the §0a precondition holds):
- `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for scripts/no_move.py scripts/stage_joints.py scripts/driver_conductor.py scripts/driver_stage_s8s9.py references/conductor.md references/stage-joints.json scripts/tests/fixtures/driver-exits/gates.json scripts/tests/fixtures/driver-layers.json scripts/tests/test_controller_doors.py scripts/tests/test_stage_joints.py`
  — fast printed files each alone, slow ones "judged by the batch canon" (FV2-94's own prompt rows are among the printed files: they stay green).
- `python -B ai-packages/qa-factory/scripts/stage_joints.py --check` → clean, `rows R1 + 17`, `unsited U0`.
- `( cd ai-packages/qa-factory && python -B scripts/tests/dry_exits.py --check )` → `0 discrepancies` (in the builder's worktree subshell).
- `python -B ai-packages/qa-factory/scripts/contract_slices.py --check`; `python -B ai-packages/qa-factory/scripts/selftest.py --limits --lang`.
- Premise 5 sizes in the report.
- Negative controls (byte copy, restore by `cp`, hashes equal): the `told=` of `no_move_legacy` removed → the legacy prompt row FAILs;
  the told text concatenated into the legacy refusal → `legacy-cap` FAILs.

Common to both: "census: no new blocking unit"; the report holds the site table (function | fragment | id or E-reason | test row |
proof F/W/N), the FR walk (§1), the ratchet lines of §6, the verbatim witness. siblings: axis 17 (Record shape), axis 34 (one road:
`refusal()` only; one renderer, one placement), axis 39 (when T10 opens it); the walk twins (generator / package detector) change
together; analogs noticed are reported, not widened.

---

## §8 Readers of every touched file (rule 7)

Commands (Grep tool, count mode):
- over `tools/`, pattern `controller\.py|waiver\.py|source_exclusions|stage_done\.py|planning_contract|no_move|driver_conductor|driver_stage_s8s9|stage-joints|conductor\.md|driver-exits|test_controller_doors` → 31 hits in 12 files (re-run here, equal to r1);
- over `tools/`, pattern `controller-blocks-gen|test_controller_blocks|controller-blocks\.md|driver-layers` → 15 hits in 4 files
  (`controller-blocks-gen.py` 5, `test_controller_blocks_gen.py` 3, `test_quarantine.py` 2, `test_test_quarantine.py` 5);
- over `tools/`, pattern `stage_joints|test_stage_joints|test_detector_verdict|delivery_answer|conductor_options|checks_section|conductor_told` → 0 (control: the first pattern, same tool and mode, 31);
- over `.githooks/`, the broad pattern plus the new names → 0 (control `tools/` → 21 hits in 4 files);
- over `.claude/settings.json`, the same → 0 (control `tools/` → 37); `.claude/hooks/**` and `.claude/*.py` → no files (Glob; the
  Lead's grep in the r1 decisions agrees).

| touched file / name | reader | verdict |
|---|---|---|
| `controller.py` | `tools/controller-blocks-gen.py` (14 name hits), `scripts/tests/test_controller_blocks.py` (twin walker) | both change in A (§3b) |
| `controller.py` et al. | `tools/lint-baseline.json` (1), `tools/source-split-carriers.json` (2) | unchanged; a moved lint/size ratchet is named in A's report |
| `design/controller-blocks.md` | `test_controller_blocks.py`, `test_controller_doors.py`, `test_person_word_stages.py`, `test_repair_marker.py`, `test_state_exits.py` | file unchanged (byte-identical) |
| `tools/controller-blocks-gen.py` | `tools/test_controller_blocks_gen.py` | changes in A |
| `test_controller_blocks.py` | `tools/test_quarantine.py`, `tools/test_test_quarantine.py` (name mentions of quarantine registries) | unchanged |
| `driver-layers.json` | `tests/harness.py` (`DRIVER_MAP`), `tests/driver_golden.py`, `test_s6_reprove_manual.py`, `tools/test_quarantine.py` (`_purge_driver_layers`) | one row added in B; FV2-94 added `conductor_head` before it (merge keeps both) |
| several names | `tools/test_forge_metrics.py`, `test_collect_intake.py`, `test_dispatch_gate.py`, `test_md_table.py`, `test_piles.py`, `test_test_split.py` | name mentions; unchanged |
| `stage-joints.json` | `stage_joints.py`, `contract_slices.py`, `selftest.py` (`load_rows`), `dry_exits.py` (`scan_joints`), `detector_verdict.refusal` (`row_for`), N3a `told_before_work` | rows change in B; ledger in B; N3a re-reads at its merge |
| `no_move.moves_section` | `driver_conductor._conductor_text`, `test_conductor_doors`, `test_no_move_seam_c26_g27_f2`, `test_story_run_exit_limit`, `test_controller_doors` (T9c rows) | the section leaves it (back to the two headings); only `test_controller_doors` pins the section (Grep `WHAT_CODE_CHECKS|What code will check in this launch` over W PKG: no other test) — B moves those rows |
| `no_move.NOTHING_CHECKED` | `test_controller_doors.py` (by constant) | B |
| `Driver.conductor` / `_ask_conductor` | ≈ 25 test fakes with the closed signature (§2); `audit_factory` A27; `test_audit_rules.py` fixture text | no signature change (F-9 (b)); A27 unchanged |
| `Driver._conductor_text` | `test_controller_doors.launch_prompt` (positional call, 6 args) | a keyword with a default: unchanged |
| `Driver.no_move_legacy` / `pass_to_person` | `_no_move` (1 caller each) | B |
| `stage_joints._row_holds` / `_page_leg` | `rows_for` (pages, `contract_slices.requirement_section`), the K2 walk | non-conductor branch unchanged |
| `references/conductor.md` | `Driver.conductor`, `driver_stage_s8s9` (system_file), `stage_joints.ROLE_FILES`, `selftest --limits` | one sentence in B (E16) |
| `driver_stage_s8s9.py` delivery | `test_story_run_delivery*` (stdout redirected; printed by B's witness) | the prompt gains the block; one stdout line on E24 |
| `planning_contract.unmarked_revision_errors` text | `test_story_run_s3_windows.py` (prefix only), `test_detector_verdict.py` (E17) | tail in A |
| `test_detector_verdict.py` | the T-wave nodes' own functions | A adds one function, flips E17 |
| `test_controller_doors.py` | T9a (new rows), T9c | B; T9a merges after and keeps both sides' rows |
| `changelog.d/tbw-t9c.md` | the release aggregation | one wording in B |

---

## §9 Forks

Lead decisions of 17.11.2026 standing (none judged wrong by t-1102): F-1 = (a) with the F8 sentence (§3 row 14); F-2 = (a) with the F3
conditions (§3a); F-3 = (a) (`move:approve_gate`) with the F1 door; F-4 = (a) with the F2 fix (§4 item 10); F-5 = (a), (b) if E16 trips;
F-6 = (a) with the F9 order (§0a); F-7 = (a) with F11 (§4 item 11). B1 = (a). Key 4 built in (§3).

New forks (each executable by its recommendation):

| # | fork | options | recommendation |
|---|---|---|---|
| F-8 | the re-ask's `## Your options were refused` paragraph is appended after the state text, so the 6000 cut removes it first (the class of FV2-94, not covered by FV2-94's branch: F `_no_move` re-ask unchanged) | (a) stream B moves it into the kept head through a `refused` keyword of `_conductor_text` (§4 item 7) — bytes unchanged, position only · (b) leave it; offer a finding to `live-run-fvf` as FV2-94's sibling · (c) put it into the told block (breaks `test_no_move_seam_c26_g27_f2.py:115` and `test_person_owned_paths.py:140`, which read it from the refusal text: two more files in owns) | **(a)**: in B's own file and reach (designer rule 2), one line, no other file |
| F-9 | the carrier of the told text into `Driver.conductor` (t-1102 B1 (a) said "a keyword `told`") | (a) a keyword `told` on `conductor` and `_ask_conductor` — every closed-signature test fake (≈ 25 in ≈ 12 files of other piles) raises TypeError → all those files enter owns, overlapping other streams · (b) an attribute `conductor_told` set by `_ask_conductor` right before its one call and read-and-cleared first in `conductor` (FV2-94's `conductor_head` precedent; a `driver-layers.json` row) · (c) a keyword on `_ask_conductor` only and the block concatenated into the prompt by `_ask_conductor` (impossible: the prompt is built inside `conductor`) | **(b)**: no signature change, one writer one reader (AR-14), the precedent already in the same class; cost: an implicit channel, held by E23's row |
| F-10 | the two walkers of the controller (forge `tools/controller-blocks-gen.py`, package `scripts/tests/test_controller_blocks.py`) carry the same head-literal rule twice | (a) both get the same unwrap in A, same commit, mirrored table rows · (b) the generator imports the package test's walker (the package test returns Counter keys, not rows: a larger change, and a forge tool importing a package test) | **(a)**; the duplication is older than this node and the package cannot import `tools/` (it ships without it) |

## §10 Small choices closed by the designer

- S-1 Names `checks_section`, `MOVES_ANSWER`, `LEGACY_ANSWER`, `DELIVERY_ANSWER`, `CONDUCTOR_ANSWER_TOKENS`, `conductor_told`.
- S-2 Tokens `conductor_options`, `delivery_answer`.
- S-3 `controller:rework.cap` keeps one id at `Controller.validate` across every dispatch road (one requirement, one id).
- S-4 S8 family `driver_stage_s8s9:delivery.*` (producer stem).
- S-5 Ledger group `gates.json` for the new joints (t-1087 precedent).
- S-6 Test function `tbw_siting_command_sites` in `test_detector_verdict.py`.
- S-7 Changelog fragments `tbw-siting-a.md`, `tbw-siting-b.md`, one English ASCII bullet each.
- S-8 `NOTHING_CHECKED` drops "above" (false on all three launches once the block precedes the refusal); the historical mechanism spec
  line is not edited.
- S-9 S8: `""` before the block, so one blank line separates it from the delivery section.
- S-10 Import forms: `import detector_verdict as DV` in `controller.py`, `source_exclusions.py`, `driver_conductor.py` (a bare `refusal`
  would be shadowed by local names there); `from detector_verdict import refusal` in `driver_stage_s8s9.py` (`DV` is `delivery_verdict`
  locally; the new call sits in the delivery method, which binds no local `refusal`).
- S-11 A folded `(×K)` message is not re-wrapped: every carrying form (`DV.refusal(message.check, …)`, `with_check(…, message.check)`)
  puts a NON-literal check argument before the scanner (a walk error); named in E7 instead.
- S-12 Insertion position of the 17 rows: after `no_move:args`, §3 order, then S8 (deterministic expected lists).
- S-13 The walk-preserving comprehension (a class bound to a name) for the mapping sites.
- S-14 `changelog.d/tbw-t9c.md` re-worded by B rather than left stating the old position.
- S-15 The told text is not capped (a requirement is never dropped for size); measured instead.

## §11 Contradictions and analogs noticed (not widened)

- t-1102 did not name the package twin walker `test_controller_blocks.py`; without it A's B2 fix would leave that test red (§3b, F-10).
- t-1102 B1 (a) as written (a keyword) breaks ≈ 25 test fakes (F-9).
- The key-4 line keeps "code writes the mark when S3 closes" in its middle while the row says "when an S3 strategist dispatch completes":
  the critic's fix changes the tail only, as the Lead ordered; the middle clause is incomplete, not false for the commonest road.
  Reported, not changed.
- The S8 JSON-form line and the S8 rows word `action`/`mr` twice — accepted as the T9c precedent (t-1102 standing questions).
- `C:/QAFactory/forge-repo/--write` (untracked, 14.11) is the B2 accident's earlier instance; not in any owns here.
- `Controller._merged` stringifies: T9a's sites through `_raise_all` are served by F-2 (a).

## §12 Not established

- Every number marked "at build" (R0, R1, U0, block count, sizes).
- The merged shape of FV2-94 (in flight; read in F only). B keeps §4 item 3's invariant whatever the shape.
- Whether `refusal_registry.sites` binds `DV.refusal` in `controller.py` / `source_exclusions.py` after the new imports: measured by
  premise 3 (`unsited` would rise if not; then STOP and report).
- C1 of `test_judgment_census.py` (slow, the canon's).
- Replaced by facts (r1 §12 → established): `stage_done:set` sentence — T1r-cards spec :342 read, plus `stage_done.SIDE_ATTRS` (:89)
  and the `sides_unknown` refusal (:105) read; readers in `.claude` — `.claude/settings.json` 0 hits (control 37), no `.claude/hooks`
  or `.claude/*.py` files (Glob); `controller-blocks-gen.py` CLI and extraction — argv[1] output path, head = first literal (read
  `main`, `collect_rows`); `pass_to_person` callers = 1 (`no_move_legacy`, read W); `told-ratchet` / `rowless` — t-1102 key 2.

## §13 Closing table — remark → where applied

| remark (t-1102 / brief) | applied in |
|---|---|
| B1 the section inside the cut | §4 items 1, 3-5 (own block outside the cut, Lead B1 = (a)); §5 E12; positional invariant §4 item 3; F-9 for the carrier |
| B1 collision with FV2-94 | §0a (both worlds, precondition, not redone); §4 item 7; §5 E25 |
| B2 generator argv and head reading | §3b; §7 A owns (`tools/controller-blocks-gen.py`, `tools/test_controller_blocks_gen.py`, plus the twin `test_controller_blocks.py`), DoD (scratch path, byte compare, never `--help`); §5 E19-E20; F-10 |
| B3 legacy section leak to a person | §4 items 3, 6 (block not in `refusal`); `legacy-cap` row §7 B; §1 AR-16 and FR walk B; §5 E21 |
| F1 / key 4 two doors | §3 key-4 fix (`unmarked_revision_errors` tail), row 15 sentence and door; EC-1 named exception; §7 A owns; §5 E26 |
| F2 `mr_record` returns "" | §2; §4 item 10 (`given` non-blank and not `mr`; text without an order claim; `from detector_verdict import refusal`); §5 E24 |
| F3 F-2 conditions | §3a; §5 E7; S-11 |
| F4 row 7 duplicate id | §3 row 7 keyed `waiver:WV-placeholder-block`; §2 A24 row corrected |
| F5 named_files / journal | closed by B1 (a): §5 E22 |
| F6 row 4 vs story-state rule | §3 row 4 (reason and driver-built rounds) |
| F7 EC-2 wording | §3 paragraph "EC-2 and `build_rework_request`" |
| F8 row 14 sentence | §3 row 14 (full sentence) |
| F9 base and order | §0a |
| F10 E5 premise | §5 E5 |
| F11 non-list `answer` | §4 item 11; §5 E1; `ROW_HOLDS` row |
| F12 S8 position, S8 id, `NOTHING_CHECKED` | §4 item 10 (position, ratchet literal only); §4 item 12 / S-8 |
| key 2 AR-16, AR-12 not named | §1 rows AR-16, AR-12 (and AR-24, AR-14 added) |
| key 7 / brief: §12 facts | §12 "Replaced by facts" |
| standing question: `DV` alias collision | §4 item 10; S-10 |
| brief: F-1…F-7 stand unless judged wrong | §9 first paragraph (none judged wrong; conditions applied) |
| brief: Lead decisions B1, B2, B3, key 4 | §4, §3b/§7 A, §4 item 6, §3 key-4 fix |

## §14 Reading trail

Read: r1 card (whole, with the Lead decisions); verdict t-1102 (whole); finding `plans/piles/live-run-fvf/findings/20261117-p1b-conductor-refusal-cut-loses-the-persons-choice.md`;
batch-2 row FV2-94 (`plans/piles/live-run-fvf/batch-2-live-run-fvf.md:121`); journal Grep `FV2-94` (t-1099 delegated, worker
`agent:a7712a5a6d8bb4c87`); T1r-cards spec :340-343; T9c report :119-122 (in W).
W: `driver_conductor.py` :194-225, :260-349, :560-829 and import Grep; `no_move.py` :275-334 and Grep (`WHAT_CODE_CHECKS`,
`EXCLUDED_KINDS`); `stage_joints.py` :291-330, :535-569 and Grep (`_page_leg`, `CAPABILITY_TOKENS`); `detector_verdict.py` :95-184 and
def list; `controller.py` `_merged`/`_raise_all` (:6156-6189), `release_dispatch` (:8225-8272), `_unknown_dispatch` callers, import and
`DV` Greps; `planning_contract.py` :271-300; `gate_preflight.py` Grep; `driver_stage_s8s9.py` :400-504 and Greps (imports, `refusal`);
`stage_done.py` Grep (`SIDE_ATTRS`, `sides_unknown`); `refusal_registry.py` Grep (`WV-placeholder-block`); `conductor.md` :97-99;
`stage-joints.json` Grep (`when_kinds`, `conductor_answer`); `test_controller_doors.py` :225-334; `test_controller_blocks.py` whole;
`test-layers.json` rows of `test_controller_blocks.py`, `test_controller_doors.py`, `test_detector_verdict.py`; `driver-layers.json`
Greps; `driver_golden.py`, harness Grep (`driver-layers`); test-fake Grep (`def conductor\(|\.conductor = `); Greps
`Your options were refused`, `reruns the S3 step|never the role\)`, `answer's form above`, `WHAT_CODE_CHECKS|What code will check`.
F: `driver_conductor.py` :262-331, :640-709 and Grep (`conductor_head`, `spent.refusal`, `_ask_conductor`); `no_move.py` Grep; 
`driver-layers.json` Grep (`conductor_head`).
Root checkout: `test_detector_verdict.py` Grep `unmarked`; `no_move.py` Grep (`WHAT_CODE_CHECKS|conductor_head|def moves_section` → 1).
Forge: `tools/controller-blocks-gen.py` :1-30, :305-511; `tools/test_controller_blocks_gen.py` Grep (defs); reader Greps of §8.
Needed beyond the manifest: the W and F code above, the T1r-cards spec, the T9c report, `tools/controller-blocks-gen.py`,
`tools/test_controller_blocks_gen.py`, `driver-layers.json`, `test-layers.json`.

## §15 Lead decisions on the r2 forks (17.11.2026, Lead of the batch; by recommendation)

- F-8 = (a): stream B moves the re-ask paragraph into the kept head through the `refused` keyword of `_conductor_text`. If the FV2-94
  fix round (critic t-1111) already protects that paragraph when B starts, B finds it done and only pins it.
- F-9 = (b): the told text travels as the attribute `conductor_told`, set by `_ask_conductor` right before its one call and
  read-and-cleared by `Driver.conductor` (the FV2-94 precedent `conductor_head`); no test fake changes its signature.
- F-10 = (a): both controller walkers get the same unwrap in stream A, one commit, mirrored table rows.
- Closing table §13 checked against verdict t-1102 by the Lead: every remark has a place. No second plan-critic pass: the r2 changes
  apply the verdict and do not change the architecture of r1 (PROJECT.md, new idea, step 6).
- Stream A starts now from origin/main; stream B waits for the three preconditions of §0a.
