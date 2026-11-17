# t-1102: plan review of the TBW siting card (t-1096, TBW1-11 residuals N1/N2)

Card under review: `docs/tasks/specs/20261117-tbw-conductor-launches-siting-card.md`, including "Lead decisions on the forks".
I checked the facts against the T9c tree `W = .claude/worktrees/agent-a8e7e4c769ef59136` (HEAD `d440db2c`, with the F1-F5 fix round
uncommitted in 4 files). Paths below are relative to `W/ai-packages/qa-factory/` unless given in full.

## Verdict

**NEEDS WORK.** The direction is right: N1 sites go at the refusal and carry text byte for byte; N2 has one renderer for three
launches. Six of the seven fork decisions are right, and F-2 and F-4 are right with conditions. The card cannot go to builders
as written. Three findings block dispatch: B1, B2 and B3. Each is either a card edit or a fork the Lead decides now, and each
has a recommendation below. F1-F12 are card fixes for the same round. Accepting this verdict, and the B1 fork, is the Lead's
decision, not mine.

## Blocking findings

**B1. Feasibility of the moves-road section against the 6000-char cut (E12).** E12 says "over 6000 → STOP", and by estimate
that STOP will trip. The section rides inside the `refusal` argument of `Driver.conductor`, which is printed as
`refusal.strip()[:6000]`. On the moves road that text is lead + moves + section + state text. I measured the part3 row
cells (requirement + door, characters, from the accepted row text in `20261113-told-before-work-wave0-rows-part3.md`):
- the four `controller:rework.*` rows: 1936
- the six `waiver:*` rows of `go_on_as_is`: 2061
- `controller:release.call`: 458
- the two `source_exclusions` rows: 485

T9c measured 750 for the three `conductor_answer` rows and 1133 with `no_move:args`. Take a gate-A launch with `rework_stage` and
`go_on_as_is` open (both are legal before gate A, `conductor-actions.json` preconditions), plus `approve_gate` (row 15) and
`story_fact` (`stage_done:set`, ~600). The section alone is about 1133 + 1936 + 2061 + ~400 + ~600 ≈ 6100 characters before
the lead, the moves list and the state text. The cut keeps the HEAD, so the state text, which is the refusal itself, is cut
whole, and the section's own tail is cut too.

The legacy road has the same exposure, smaller. Section first means a long S1-review text loses up to len(section) of its
tail, which today it keeps.

This is a plan-level feasibility gap: the builder would STOP on the commonest gate launch. The Lead decides one of these before
dispatch:
- (a) **Recommended.** The section leaves the cut text. `Driver.conductor` gains a keyword `told: str = ""`, printed as its own
  block right before `## The refusal`. It is outside the 6000 cut, outside `named_files`, outside `journal_conductor(refusal=…)`
  and outside `ConductorSpent.refusal`.
  - `_conductor_text` / `moves_section` stop embedding the section.
  - `_no_move`, `no_move_legacy` and the refused re-ask (driver_conductor `:677`) pass `told=NM.checks_section(...)`.
  - S8 keeps its list item, because its prompt has no cut.
  - This also closes B3 and F5, and keeps one road for all three launches (P31).
  - Cost: E-T9c-5 (the section after the two moves headings) becomes "its own block before `## The refusal`". That is a pinned
    position of T9c and changes in this node. `test_no_move_seam_c26*` headings keep their order. The T9c rows of
    `test_controller_doors` that read the section from `moves_section` move to `checks_section` / the prompt.
  - Owns: stream B, driver_conductor.py and no_move.py (already owned).
- (b) Keep the section in the text and shorten it: each command row's `told_line` gives the id and the door only, not the
  sentence. This loses AR-10 content.
- (c) Raise the cap. That is a non-goal of the card, and the cost lands on every conductor call.

**B2. `tools/controller-blocks-gen.py`: the stream-A DoD step writes a file, and wrapping changes the generated design doc.**
- The tool has no flags. `sys.argv[1]` is an OUTPUT PATH (`controller-blocks-gen.py:454-456`). The card's "flag read from its
  `--help`" wrote a 75 KB file named `--help` into the session root when I ran it. I removed my own artifact (`rm`, confirmed
  absent). The repo root already holds an untracked `--write` from 14.11, which is the same accident.
- The tool reads a block's `head` as the FIRST string literal of the segment (`LIT`, `collect_rows.block`). After
  `(ValueError, DV.refusal("controller:rework.args", "<text>"))`, the head is the check id. For COMMAND-table messages the
  route then changes. Probe over the W controller with the real `classify` / `BY_SEGMENT`:
  - `build_rework_request` lines ~3814, 3827, 3861, 3864, 3868 and 3875 go `command -> caller`.
  - Two wrapped sites probed for real (`--reason ...`, `(ValueError, text)`): heads became `controller:rework.args` /
    `controller:rework.runner_half`.
  - The total stays 355 and 0 are unclassified. `design/controller-blocks.md` is then not byte-identical and its routes are
    wrong, so the card's own STOP trips with certainty.

Fix:
- Stream A owns `C:\QAFactory\forge-repo\tools\controller-blocks-gen.py` (`collect_rows.block`). When the message argument of
  the tuple or raise is a `refusal(...)` / `DV.refusal(...)` call, the head and the route are read from that call's SECOND
  argument. A segment-keyed `BY_SEGMENT` match is tried on the segment with the wrapper removed.
- Stream A also owns `C:\QAFactory\forge-repo\tools\test_controller_blocks_gen.py`, with one row: a wrapped pair keeps the head
  and route of the bare pair, plus a negative control.
- DoD: `python -B tools/controller-blocks-gen.py <scratchpad>/controller-blocks.md` (exit 0, no `UNCLASSIFIED`), then a byte
  diff against `ai-packages/qa-factory/design/controller-blocks.md` must be empty, and `python -m pytest
  tools/test_controller_blocks_gen.py -q`. Never `--help`, never a relative path. §12 item 3 is then established.

**B3. Legacy launch: the section leaks into a PERSON's text.** `no_move_legacy` turns `ConductorSpent` into
`Person(... f"...Last refusal:\n\n{spent.refusal}\n\nWhat should happen? ...")` (driver_conductor `:817-822`). `spent.refusal`
is the `refusal` argument of `Driver.conductor` (`:271`). Under §4 item 5, that argument starts with
`## What code will check in this launch` and its rows. So at the cap, the person reads the conductor's told section. That
breaks FR-6 / AR-16, and §1's "B — n/a (the conductor prompt is not text a person reads)" is false on this road.

The moves road does not have this: its `ConductorSpent` goes to `fallback_person(state, …)`.

Fix: B1 (a) removes it. Otherwise §4 item 5 adds "the `ConductorSpent` text uses `str(state.get("text") or "")`, byte-identical
to today", and a pinned-text row in `LAUNCH_KINDS` for the legacy cap.

## Fixes to the card (same round)

- **F1 (Key 4: the two doors). TRUE door: a strategist rework of S3.**
  - What the code does: the revision mark is written only by `planning_contract.project_plan`, called only from
    `Driver.s3_project` (driver_dispatch `:2810-2837`). That runs at the completion of an S3 strategist dispatch:
    `s3_window_completion` (closing or labelling), `s3_rework_completion` (a rework of S3) and `s3_ticket_completion`.
  - So the line's door is false. No command in the conductor's set runs the projection without a role dispatch: no CLI calls
    `project_plan`, and the 13 conductor moves have no such run. gate_preflight's "(a strategist rework)" is the true road.
  - The road in the conductor's set is the move `rework_stage`: `controller.py --operation rework --stage S3 --role
    qa-test-strategist …`, legal before gate A is decided. Whether the conductor may run it on the factory's own finding
    (inline `--reason`, `--cause mechanical`) or needs the person's words (`"word": "person"`) is the move's existing
    precondition, unchanged here.
  - One-sentence fix, file `scripts/planning_contract.py` (stream A, `unmarked_revision_errors`): the tail `the conductor reruns
    the S3 step (never the role)` becomes `a strategist rework of S3 writes it when that rework completes`. It then names the
    same road as `gate_preflight.check_planning_contract`'s door, and gate_preflight.py is untouched.
  - Card consequences:
    - Row 15's door is that clause.
    - Its sentence's "code writes the mark when S3 closes" becomes "when an S3 strategist dispatch completes (S3 closing or a
      rework of S3)".
    - EC-1 and the batch's "no refusal text" line get ONE named exception: this tail, by the owner's word 17.11 cited in the
      Lead decisions. The expected text in `tbw_siting_command_sites` comes from the card, not from the new code.
    - Readers checked: `test_story_run_s3_windows.py:961/964` read the prefix `missing coverage_contract_revision` only
      (unchanged).
- **F2 (F-4 / S8, a fact error).** `driver_core.mr_record` returns `""` for no record, not `None` (`driver_core.py:415-426`). §2
  says "(None when not a record shape)", and §4 item 8 says "`mr_record(...)` is None". As written, the new line never prints.
  Fix:
  - The condition is `not mr` with the given value non-blank: `str(verdict.get("mr") or "").strip()` non-empty, so `"   "` is
    "not given".
  - The text must not claim an order exists: "`mr` {value!r} is no record of a merge request; the delivery is marked without
    an MR". `settle_mr_from_mark` calls an order off only when one exists.
  - Import: `driver_stage_s8s9.py` already binds `DV` locally to `delivery_verdict` (`:194`, `delivery_record`). Use
    `from detector_verdict import refusal` at module level (the `planning_contract` precedent), never a second `DV`.
  - Stream B owns that import line.
- **F3 (F-2 conditions).**
  - `_merged` counts and dedups by `str(message)` and appends the ORIGINAL object.
  - A folded `(×K)` message is a plain str and loses the id. Name it in E7, or carry it: `DV.with_check(Record(folded), check)`
    for a Record.
  - With several problems, `_raise_all` builds the exception, then sets `exc.records = [m for _, m in merged if
    getattr(m, "check", "")]` as an ATTRIBUTE before `raise`. Never a constructor keyword: `ValueError` / `StateConflict` take
    none, and a keyword would be a TypeError.
  - Readers: I grepped `told_fields(`, `spoken(` and `.args[0]` over the scripts, not the tests. The one reader of a Record in
    `exc.args[0]` is `role_cli.run_guarded` (`role_cli.py:214-219`). None of controller / waiver / stage_done /
    source_exclusions is a `role_cli` command (34 registry keys read), and `hooklib.block` receives no controller exception.
    So F-2 (a) is additive on every road found. State this in the card with the trail, so the builder does not re-derive it.
- **F4 (row 7, duplication).** The placeholder refusal already has an identity: A24 `waiver:WV-placeholder-block`
  (`refusal_registry.py:1011`, function `record_refusals`, guarantor `PLACEHOLDER_RE`). It is sited through `check_of` and has no
  row. A24 ids carry rows elsewhere (`guard_pre_tool:PT-*` and `exit_gate:EG-*`: 43 rows). Row 7 as drafted gives one refusal
  two ids. Fix: key row 7 `waiver:WV-placeholder-block`, and write the site literal with that id (sentence and door from part3,
  unchanged). §2 row "none of these families is an A24 id" is corrected: `waiver:CTRL-next-blocked`, `waiver:WV-*`,
  `stage_done:SD-*` and `controller:CTRL-*` exist. The other 14 ids map to none of them one to one (checked against the 19 A24
  entries of the five files).
- **F5 (positional edges the card leaves silent, legacy and moves).** Closed by B1 (a). Otherwise each needs a stated behaviour:
  - `named_files(refusal)` (driver_conductor `:108`, `PATH_RE`) scans the section first. Paths in row text resolve against the
    plugin root: `references/block-names.json` (row `waiver:block.standing`), and already today `references/conductor-actions.json`
    from the moves section. They then take the `CONDUCTOR_FILES = 3` window ahead of the files the state text names.
  - `journal_conductor(refusal=refusal[:2000])` stores the section, not the refusal.
- **F6 (row 4 vs the card's own rule).** §3 says StateConflict story-state refusals stay bare (F-P2 (a)). Row 4 sites three
  `raise StateConflict(blocking[0] + …)` (controller `:5670/:5685/:5704`, all present). Add the reason: the cap is told before
  work, because the ledger is readable at launch. Also state that the id rides on every repair-loop dispatch, including
  driver-built rounds (S-3).
- **F7 (EC-2 wording).** Rows 2, 3 and 5(c) site inside `build_rework_request` (callers: controller `main` `:10093` and
  `story_step.py:2338`) and `release_dispatch` (1 caller). EC-2 literally forbids an id inside a helper with more than one
  caller. Add one sentence: `build_rework_request` is the command's own body, not a helper, and its requirement is the same on
  both roads (S-3 logic). The story_step road is code-built, and its Record dies at the CLI/str. Without that sentence the
  card contradicts EC-2 as quoted.
- **F8 (row 14 sentence, F-1).** The T1r-cards spec O-1 sentence (`20261114-told-before-work-t1r-cards-spec.md:342`) is quoted
  below. Read against `stage_done.coerce_value`, it under-tells two refusals: the side attribute list (`SIDE_ATTRS`) and the
  `sides_unknown` forms. Proposed (the Lead accepts, EC-8): append "; a side's attribute is one of `reality`, `deliverable`
  (true/false), `settles_by`, `reference`, `source`, `at`, and `sides_unknown` is cleared with `sides_unknown=` or written as
  `.at`/`.why`." Base text:
  "`stage_done.py --set` takes `key=value` items and writes only the keys it lists: `implementation_source`, `size`,
  `environment_pending`, `no_trace`, `retro_mode`, `environment`, `parent_feature`, `sides.<name>.<attribute>` and `sides_unknown`;
  a closed key takes one of its listed words (true/false for the two flags, a reality word of `references/side-realities.json`
  for a side's `reality`, `retro_mode` only `full`), `parent_feature` is the parent's key alone, and a person's word does not
  widen the list." Door: "give the value in the key's form, or have the script that owns the field write it".
- **F9 (TEMPORAL base, §7).** T9c is NOT on origin/main: `git show origin/main:…/no_move.py | grep -c WHAT_CODE_CHECKS` gives 0.
  Its F1-F5 round is uncommitted in W.
  - Stream B needs T9c's `moves_section` block; stream A does not.
  - State it: T9c (with its fix round) merges first. B branches from origin/main after that, A may start now, and the merge
    order is T9c -> A -> B.
  - T9a (TBW1-10, "ожидает") also owns `scripts/controller.py` and `test_controller_doors.py`. State that T9a merges after this
    node and merges main into its tree (batch rule §3). F-2 (a) also serves T9a's sites.
- **F10 (E5 correction).** Between the A and B merges, `refusal("planning_contract:plan.unmarked_revision", …)` does not give the
  unreadable sentence. `row_for` falls back to the `planning_contract:*` aggregator row (stage-joints `:468`): `expected` "" and
  the aggregator's door. The other 14 families have no `<stem>:*` row, so they get the unreadable sentence, as the card says.
  Either way no printer shows it, and `rowless` does not move (below).
- **F11 (`_row_holds` edge, F-7).** An `answer` value that is present but not a list or tuple (a str would make `in` a substring
  test) is treated as absent: the row holds, toward more text. Say so, with a `ROW_HOLDS` row.
- **F12 (S8 and legacy position, text).**
  - S8: insert the section after `section.strip()` and BEFORE the existing `""` item, so one blank line still precedes the JSON
    line and the JSON line stays the list's last item.
  - S8 site: `delivery_person` does `said.rstrip()`, so the Record dies at once. State that the S8 `action` id is a ratchet
    literal only, with no reader.
  - `NOTHING_CHECKED` says "your answer's form above". On S8 and on the legacy road the form is below the section. It is
    unreachable with the real file on all three launches. State that, or drop "above" (a pinned text, E24).

## Keys

1. **Facts by trail.**
   - The 15 sites exist as quoted, judged by function:
     - `_cli_story_root` problems (`:9791-9838`) and the shared words reads (`main` `:10018`, `:10034`).
     - `build_rework_request` appends (the 17 `.args` texts, the `kind_problems` extend, and the two StateConflict holds kept
       bare).
     - The three cap raises in `validate`.
     - `release_dispatch` (3 appends plus `_unknown_dispatch`, and the StateConflict "holds nothing back").
     - waiver `main` (the words `ap.error`, with the remark/revoke/stage-block/gate order matching row 6 (i)), `record_refusals`
       (1 caller, `:1307`) and `run_stage`.
     - `stage_done.parse_sets` (callers: `main` `:1558` plus its selftest), and `unmarked_revision_errors` (1 caller, `:300`).
     - `source_exclusions` has no detector_verdict import, as the card says.
   - Byte identity: `Record` is a `str` subclass whose `str` is the problem (`detector_verdict.py:95-116`). `ap.error`, `print`,
     f-strings and `str(exc)` keep text, and F-2 keeps the raise text. Not byte-identical: B2 (the generated doc) and F1 (the one
     named text change).
   - Launches: Grep `run_claude\(\s*['"]conductor` (case-insensitive, scripts, no tests) gives 2 sites: driver_conductor `:336`
     (`Driver.conductor`) and driver_stage_s8s9 `:450`. `_ask_conductor(` has 3 callers: `_no_move` `:653`, re-ask `:677`,
     `no_move_legacy` `:816`. Positive control: the same Grep on `conductor\.md` finds both `system_file` lines. So the three
     launches are all of them. `pass_to_person` has 1 caller (`:824`).
   - Counters reproduced:
     - `stage_joints.py --check` gives `rows 273 … unsited 17`, clean.
     - The 17 unsited are the 6 `controller:*` of T9a and 11 `first_look:put.*`, so 17 -> 17 holds.
     - `dry_exits --check` gives 0 discrepancies, `unwalked` raised 231 above base 39, which matches §6.
     - `role-load.json`: `conductor` (-i) 0, control `qa-runner` 2.
2. **Architecture and principles.**
   - The AR-n named are the ones touched and they are kept, except:
     - AR-16 (B3) and FR-6 are touched on the legacy cap and are not named.
     - AR-12: B1 (size) is the real cost, and "reported" is not enough when the cut drops the refusal.
     - AR-15 holds only if B1 (a) gives one placement for three launches.
   - P1/P3 hold: the section tells and code decides nothing new. The `mr` line is a log of an existing reading.
   - FR-38 holds on all three launches once B1 is settled.
   - Census, measured: no unit for `Controller.build_rework_request`, `Driver.delivery`, `Driver.pass_to_person` or
     `driver_core.mr_record` in `judgment-census.json`. The units named in §1 exist with roles `["conductor"]`; `waiver.*` is
     class `safety`, the rest `shape`. `planning_contract.py::gate_plan_errors` has roles `["qa-test-strategist"]`. The new sites
     sit in non-transports (list, return, attribute call, stdout print) or in units that already have rows, so C1 is expected
     unchanged. That is a judgement, not a run: `test_judgment_census.py` is slow (96.9 s) and is the canon's.
   - `rowless` (dense 1): conductor-only units are not `reachable` (`test_stage_joints.py:680-682`), and the one strategist
     unit's id is covered by `planning_contract:*`. So it does not move between A and B. K4: none of these units has a
     told-ratchet baseline row.
3. **Forks.**
   - F-1 is right, with F8 added.
   - F-2 is right with the conditions in F3. It is additive: the args[0] and told_fields readers were grepped (F3).
   - F-3 is right with the door fix (F1). `move:approve_gate` is when the refusal can bite.
   - F-4 is right with a condition. F2's `None`-vs-`""` bug must be fixed, or the one behaviour addition is dead code. The
     line is additive stdout; `test_story_run_delivery_c` redirects stdout and is printed by B's witness.
   - F-5 is right. `role-rules.json` has no `why_person` hit, so E16 is unlikely to trip. Line 99 holds a second sentence ("with
     nothing to ask, say `stop`…") that stays.
   - F-6 is right with F9's base and order.
   - F-7 is right with F11.
4. **Two doors:** F1.
5. **Edges.** E1-E18 each have an invariant. Silent edges the card's own requirements create:
   - B3 and F5: positional, legacy text.
   - B1: E12 states a STOP but not the decision.
   - F9: temporal, base not on main.
   - F10: E5 premise wrong for row 15.
   - F11: a non-list `answer`.
   - F12: S8 position and `NOTHING_CHECKED`.
   - F2: `mr` blank.
   - E7: the folded `(×K)` case (F3).
6. **Streams.**
   - A and B are disjoint by files. Adding tools/controller-blocks-gen.py and its test to A keeps them disjoint.
   - Merge order T9c -> A -> B is sound (E5, F10).
   - Size: A is 15 sites plus F-2 plus the B2 tool fix plus one test function, within one builder. B is 17 rows, 17 ledger rows,
     3 launches and B1 (a), the heavier stream but within budget.
   - The tests are table rows that can fail, with negative controls named.
   - Witness: the `scenario_walk.py --witness-for` lists ran clean in form. A's list prints `test_detector_verdict.py`'s scenario
     layer, and B's prints `test_conductor_doors`, `test_stage_joints`, `test_contract_slices` and `test_scenario_dry_1`; the slow
     ones go to the canon.
   - A's DoD step for `controller-blocks-gen` must be replaced as in B2.
7. **§12.**
   - Established here: `stage_done:set` sentence (F8); readers in `.claude` (Lead's grep re-run: settings.json no hit, no
     `.claude/*.py`, control `tools/` 37); controller-blocks-gen CLI and extraction (B2); `pass_to_person` callers = 1;
     told-ratchet/rowless (Key 2).
   - Must be settled before dispatch: B1 (Lead fork) and B2 (owns plus DoD).
   - Left to the build or the canon: C1 of `test_judgment_census` (slow).

## Standing questions

- **DUPLICATION AND CONSISTENCY:** found:
  - F4: two ids for the placeholder refusal.
  - F1: two doors.
  - The S8 JSON-form line and the rows word `action`/`mr` twice; §11 names this and it is accepted as the T9c precedent.
  - Grepped: A24 REGISTRY entries of the five files, `"check": "<stem>:<UPPER>-` rows (43), and `WHAT_CODE_CHECKS` writers
    (1, `no_move.py:320`).
- **CODE QUALITY:** the `DV` alias collision in driver_stage_s8s9 (F2). Nothing else found in the planned code shape.
- **ONE ROAD (P31):** B1 (a) is the recommended single placement for three launches. The `s1_review` exclusion stays, with its
  carrier `no_move.py:37`. No new exclusion is added.
- **TESTS:** one table per behaviour, and expected values come from the card and the OLD files. B2 adds one row to
  `tools/test_controller_blocks_gen.py`. No `tests-over:` case is visible at plan stage; the builder names one if the volume
  rule trips.

## Notes

I broke my write scope once: the `--help` file created by running the tool (B2). It was removed the same turn and checked
absent.

## Trail

Read: the card (whole); verdict t-1091 (whole); finish spec `:230-262`, `:440-480`, `:690-720`; T9c report `:117-124`; part3 row
lines (Grep); T1r-cards spec `:101`, `:342`; batch-1-finish `:10-38`. In W:
- `stage_joints.py`: `_is_sited`, `_direction_a`, `_told_counters`, `_row_holds`, `_page_leg`, `check_ids`.
- `refusal_registry.py`: `:75-90`, `:990-1045`, and the REGISTRY entries of 5 files.
- `detector_verdict.py:95-250`; `controller.py` `:5630-5712`, `:6150-6240`, `:10000-10140`, the `build_rework_request` appends,
  `release_dispatch`, `_cli_story_root`; `role_cli.py:74-121`, `:205-228`; `hooklib.py:985-1000`.
- `driver_conductor.py` `:25-37`, `:85`, `:108-125`, `:194-225`, `:263-345`, `:565-600`, `:645-700`, `:805-835`;
  `driver_stage_s8s9.py:395-545`, `:303-330`; `driver_core.py:415-426`; `driver_dispatch.py:2800-2845`;
  `driver_stage_plan.py:520-556`.
- `planning_contract.py:18-20`, `:270-310`, `:3405-3440`, `:4480-4510`; `gate_preflight.check_planning_contract`; `waiver.main`
  (Grep); `stage_done.py:60-160`, `:205-225`.
- `conductor-actions.json` moves; `conductor.md:97-99`; `test_stage_joints.py:680-760`; `test_judgment_census.py:218-275`;
  `judgment-census.json` (rows of these units); `told-ratchet.json`; `slow_tests.json`.
- `tools/controller-blocks-gen.py:21-23`, `:380-470`; `tools/test_controller_blocks_gen.py:40-140`.

Commands (verbatim tails):
```
python -B W/PKG/scripts/stage_joints.py --check | tail -2
... told counters: hand_cards 12, legacy_legs 0, unsited 17
stage joints: clean
unsited keys: controller:s3_plan, controller:s5_plan_accept, controller:s5_plan_gaps, controller:s5_plan_review, controller:code_review_receipts, controller:s5_plan_gaps.rework_rows, first_look:put.* (11)
( cd W/PKG && python -B scripts/tests/dry_exits.py --check ) | tail -1
dry_exits --check: 0 discrepancies   (NOTE ratchet unwalked: raised 231 row(s) above the base 39)
python -B tools/controller-blocks-gen.py --help   (repo root; the tool writes argv[1])
355 blocks: caller 105, command 220, person 17, unpassable 13
written: --help        <- file removed: rm -- "C:/QAFactory/forge-repo/--help"; ls -> No such file
cbg_probe.py (scratchpad; W controller, two sites wrapped): orig 355 unknown 0 / wrapped 355 unknown 0; NEW heads 'controller:rework.args', 'controller:rework.runner_half'
cbg_probe3.py (classify with the id as head): build_rework_request 3814/3827/3861/3864/3868/3875 command -> caller
git show origin/main:ai-packages/qa-factory/scripts/no_move.py | grep -c WHAT_CODE_CHECKS
0
grep -n -E "no_move|...|controller-blocks" .claude/settings.json -> no hit; grep -c "tools/" .claude/settings.json -> 37
size estimate (part3 requirement+door chars): rework 1936, go_on_as_is 2061, release 458, revoke 485
```

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "B1 the conductor section rides inside Driver.conductor's refusal text cut at 6000 chars; estimated section on a gate-A launch with rework_stage+go_on_as_is+approve_gate+story_fact is about 6100 chars, so E12's STOP trips and the state text is cut whole; Lead fork before dispatch, recommended (a) a told keyword printed as its own block outside the cut, named_files, journal and ConductorSpent, used by all three launches",
    "B2 tools/controller-blocks-gen.py takes argv[1] as an output path (the DoD's --help writes a file named --help) and reads the first literal as head, so DV.refusal wrapping makes heads the check id and moves six build_rework_request routes command->caller; stream A must own the tool (read the refusal call's second argument) and its test, DoD = render to a scratch path and byte-diff the design doc",
    "B3 no_move_legacy turns ConductorSpent into a Person text with spent.refusal, which under section-first starts with the conductor's told section: person-facing text change (FR-6/AR-16), card says B n/a; closed by B1 (a) or by using state text in that branch"
  ],
  "class_completeness": "Launches: 2 run_claude conductor sites and 3 _ask_conductor callers, all covered. Siblings of the defect classes: the head-literal reading of controller-blocks-gen also meets T9a's controller sites (same fix serves both); the A24 duplicate id class checked over the 19 REGISTRY entries of the five files - one hit (WV-placeholder-block, row 7); the false-door class checked on the unmarked line vs gate_preflight (F1). Positional leaks of the section (named_files, journal, cut, ConductorSpent) are one class closed together by B1 (a). SIBLING_MAP axes named by the card (17, 34, 39) unchanged by these findings.",
  "fixes": [
    "F1 planning_contract.unmarked_revision_errors tail 'the conductor reruns the S3 step (never the role)' -> 'a strategist rework of S3 writes it when that rework completes' (the only writer project_plan runs at S3 strategist dispatch completion); row 15 door = that clause, sentence 'when an S3 strategist dispatch completes'; named EC-1 exception by the owner's word 17.11",
    "F2 mr_record returns empty string not None: condition 'given value non-blank and not mr'; line text without claiming an mr order exists; import 'from detector_verdict import refusal' in driver_stage_s8s9 (DV is already delivery_verdict there)",
    "F3 F-2: _merged counts by str, appends the original object; folded (xK) message named or re-wrapped; several problems -> exc.records set as an attribute before raise, never a constructor keyword; record the reader grep (role_cli.run_guarded only, not on these commands)",
    "F4 row 7 keyed waiver:WV-placeholder-block (existing A24 id of the same refusal), site literal with that id; correct the section-2 A24 claim",
    "F5 if B1 (a) is not taken: state behaviour for named_files reading row paths ahead of the state text and for journal_conductor refusal[:2000]",
    "F6 row 4 sites StateConflict raises against the card's own story-state-bare rule: add the reason and the driver-built-round note",
    "F7 EC-2 sentence: build_rework_request is the command body (callers controller main and story_step:2338), one requirement on both roads",
    "F8 stage_done:set sentence quoted from the T1r-cards spec line 342 plus the SIDE_ATTRS and sides_unknown forms (Lead accepts, EC-8)",
    "F9 T9c is not on origin/main: order T9c(+fix round) -> A -> B, B branches after T9c merges; T9a merges after this node on controller.py and test_controller_doors.py",
    "F10 E5: between A and B, row 15 resolves to the planning_contract:* aggregator row, not the unreadable sentence",
    "F11 a non-list answer facts value is treated as absent (row holds), with a ROW_HOLDS row",
    "F12 S8 section after section.strip() and before the blank item; S8 action Record dies at said.rstrip() (ratchet literal only); NOTHING_CHECKED 'above' is false on S8/legacy - state unreachable or drop the word"
  ],
  "trail": {
    "read": [
      "docs/tasks/specs/20261117-tbw-conductor-launches-siting-card.md",
      "docs/tasks/specs/reviews/t-1091-tbw-t9c-code.md",
      "docs/tasks/specs/20261117-told-before-work-finish-spec.md:230-262,440-480,690-720",
      "docs/tasks/specs/20261114-told-before-work-t1r-cards-spec.md:101,342",
      "plans/piles/told-before-work/batch-1-finish.md:10-38",
      "W/ai-packages/qa-factory/scripts/stage_joints.py",
      "W/ai-packages/qa-factory/scripts/refusal_registry.py:75-90,990-1045",
      "W/ai-packages/qa-factory/scripts/detector_verdict.py:95-250",
      "W/ai-packages/qa-factory/scripts/controller.py build_rework_request, validate cap, _merged, _raise_all, release_dispatch, _cli_story_root, main",
      "W/ai-packages/qa-factory/scripts/role_cli.py:74-121,205-228",
      "W/ai-packages/qa-factory/scripts/driver_conductor.py:25-345,565-700,805-835",
      "W/ai-packages/qa-factory/scripts/driver_stage_s8s9.py:303-545",
      "W/ai-packages/qa-factory/scripts/driver_core.py:415-426",
      "W/ai-packages/qa-factory/scripts/driver_dispatch.py:2800-2845",
      "W/ai-packages/qa-factory/scripts/planning_contract.py:18-20,270-310,3405-3440,4480-4510",
      "W/ai-packages/qa-factory/scripts/gate_preflight.py check_planning_contract",
      "W/ai-packages/qa-factory/scripts/stage_done.py:60-225",
      "W/ai-packages/qa-factory/references/conductor-actions.json",
      "W/ai-packages/qa-factory/scripts/tests/test_stage_joints.py:680-760",
      "W/ai-packages/qa-factory/scripts/tests/test_judgment_census.py:218-275",
      "tools/controller-blocks-gen.py",
      "tools/test_controller_blocks_gen.py:40-140"
    ],
    "reruns": [
      {"command": "python -B W/PKG/scripts/stage_joints.py --check", "result": "clean; rows 273; unsited 17 (6 controller:* of T9a + 11 first_look:put.*)"},
      {"command": "python -B scripts/tests/dry_exits.py --check (in W package)", "result": "0 discrepancies; unwalked raised 231 above base 39"},
      {"command": "python -B tools/controller-blocks-gen.py --help", "result": "355 blocks; 'written: --help' - wrote a file named --help, removed and checked absent"},
      {"command": "scratchpad cbg_probe.py / cbg_probe3.py on W controller", "result": "wrapped heads become the check id; six build_rework_request routes command -> caller"},
      {"command": "git show origin/main:.../no_move.py | grep -c WHAT_CODE_CHECKS", "result": "0 - T9c not on main"},
      {"command": "grep run_claude conductor (case-insensitive) over W scripts, control conductor.md", "result": "2 launch sites; _ask_conductor 3 callers; pass_to_person 1 caller"},
      {"command": "part3 row char sizes", "result": "rework 1936, go_on_as_is 2061, release 458, revoke 485"}
    ]
  }
}
```
