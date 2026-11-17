# T9c report: the conductor's launch rows (t-1079, node told-before-work/1/TBW1-11)

Branch `worktree-agent-a8e7e4c769ef59136`, ONE commit on top of origin/main e6961849 (sha: in the final message; a report cannot hold its own sha), not pushed.

## 0. Result in one paragraph

Done: item 0 measured, item 1 (the section), item 2 (texts byte-identical, ids at sites), item 3 (prompt row), 4 conductor rows
(`no_move:options`, `:prose`, `:class`, `:args`), F-4 (a) applied, census notes, pins +4, changelog. NOT done, by a ratchet rule and not by
choice: every drafted COMMAND row (controller / waiver / source_exclusions / stage_done) stays out, because none of them has a literal
site in a file I own, so each would raise `told_ratchet.unsited` (17 now; measured, see 5). Questions Q1-Q4 below. `dry_exits.py --check`
is RED on 4 lines in a file outside owns (Q2): the DoD (`stage_joints.py --check`) is green.

## 1. Item 0 (measured, F-4 (a))

One conductor row added to a COPY of `references/stage-joints.json` (copy at the scratchpad, `--data <copy>`):

```
python -B scripts/stage_joints.py --check --data <copy>
stage joints: ... rows 270 ... unsited 18
REJECT - 2 finding(s):
- stage-joints: no_move:options producer[0]: role `conductor` has no agents/conductor.md
- stage-joints: told_ratchet.unsited is 17 but 18 rows have no site in code (...): a raise is named in the verdict (AR-20); write the site or remove the row
```

Red as the card predicted, so F-4 (a): `stage_joints.ROLE_FILES = {"conductor": "references/conductor.md"}` (one named data constant) and
`_producer_leg` accepts a role when `agents/<role>.md` exists OR its `ROLE_FILES` file exists; the refusal sentence is unchanged. Nothing
else of `stage_joints.py` touched. The same run measured the second finding (an unsited row raises the ceiling): see 5.

## 2. Site table (function | fragment | id or E6 reason (class) | test row | proof)

| function | fragment | id / reason | test row | proof |
|---|---|---|---|---|
| `validate_options` | options not a list / fewer than two | `no_move:options` | refusal-text/options-one | F: old text captured from a byte copy |
| `validate_options` | one option not the `rework` option | `no_move:options` | (same id, same wrapper) | N |
| `validate_options` | no token / two tokens equal | `no_move:options` | refusal-text/options-dup | N |
| `validate_options` | site door not read / a move's own word | `no_move:options` | (same wrapper) | N |
| `validate_options` | move not open | `no_move:options` | refusal-text/options-closed | N |
| `validate_options` | move never an option / token not the move's own | `no_move:options` | (same wrapper) | N |
| `validate_options` | lacks says / factory / person / story | `no_move:options` | (same wrapper) | N |
| `prose_refusal` | the question names a token that is not an option | `no_move:prose` (one caller: `validate_options`) | refusal-text/prose | F; the negative control hits this site |
| `validate_options` | `check_args` result | `no_move:args`, written HERE (EC-2: `check_args` has 3 callers) | refusal-text/args | F |
| `validate_options` | `question_rule` result | `no_move:class` | refusal-text/class | F |
| `validate_options` | args and class together | `no_move:args` + `no_move:class`, `ClassRefused.records` holds one Record each (EC-5), text one line as before | refusal-text/args-and-class | F |
| `check_args` | every return | NO literal id (EC-2, multi-caller: `driver_machine.py:2753`, `:3629`, and `validate_options`) | - | E6 (code), by rule |
| `validate_options` | the action is not `ask_person`/`stop` | bare: row `no_move:options` states what an `ask_person`/`stop` answer carries, not that other actions are refused | refusal-text not asserted | E6 (code) |
| `prose_refusal` | the question is empty | bare: row `no_move:prose` says nothing of an empty question | refusal-text/empty-question (text + empty id) | E6 (code) |
| `moves_section` | the new section | render, no check | launch-section/*, launch-prompt | N |

EC-1 proof (old text from a byte copy BEFORE the edit): `no_move_OLD.py` is a byte copy (sha256 20b6b3d2...) taken before any edit; one
battery of 17 verdicts (every refusal branch) run against OLD and NEW: text equal in all 17 (`compare.py`: SAME x17); the NEW run adds
only the id on the Record. The expected strings in `test_controller_doors.py` are the OLD file's output.

`ArgsRefused.__init__(rule, records=())` gained one attribute (`records`, `[]` by default): every caller keeps working; `str(exc)` and
`exc.rule` are as before.

## 3. Rows

Added to `references/stage-joints.json` (end of `joints`), text verbatim from mech §5.5, `roles: ["conductor"]`, `stages: ["*"]`,
`door_needs: "none"`, told `{"page": true}` (the conductor's K2 leg is the `when` token):

| row | when |
|---|---|
| `no_move:options` | `conductor_answer` |
| `no_move:prose` | `conductor_answer` |
| `no_move:class` | `conductor_answer` |
| `no_move:args` | `move:rework_stage` |

Left OUT (E-T9c-2 and the ratchet), counted:
- drafted in part3 and wave0 item 11, NOT landed because each would be an unsited row (no literal site in a file I own; unsited would
  go 17 -> 17+N, a raise): `controller:rework.call`, `.args`, `.runner_half`, `.cap` (4); `controller:release.call` (1);
  `waiver:block.call`, `.placeholder`, `.stand_gap_id`, `.grant_pattern`, `.standing` (5); `waiver:remark.call` (1); `source_exclusions:revoke.call`,
  `.target` (2); `stage_done:set` (1; its corrected O-1 sentence lives in the T1r-cards spec, not in my given) = 14.
- `waiver:carry.call`, `.old_key` (2): drafted with `when: move:words_carry` PENDING F-P1 (a), which needs a `moves` row in
  `conductor-actions.json` (non-goal); K3 would refuse the token today.
- NOT drafted (E-T9c-2, body not read in any draft): `controller:rework.runner_half.manual_block`, `controller:release.commit`, and the
  10 helper bodies of part3 §1.1 (2 named rows + 1 group = 12 undrafted items); `stand_health:probe` = no row by part3 §1.5.
- `planning_contract:plan.unmarked_revision`: E-T9c-3, see Q3.
- Command-row summary: 14 drafted-not-landed + 2 pending F-P1 + 12 undrafted + 1 unmarked_revision question.

Unsited before -> after: 17 -> 17 (the four new rows are sited by the literals above; `stage_joints.py --check` prints `unsited 17`).
Rows 269 -> 273.

## 4. Pins moved (each labelled "+N T9c conductor rows")

`test_stage_joints.py`: K1 rows `269 -> 273` ("+4 T9c conductor rows"); `rows-for/real` expected conductor rows `[] -> the four ids`
("+4 T9c conductor rows"). The walk-size pins (exit 8 / detector 5 / window 28) did not move; `UNSITED_CAP` 17 and `told-ratchet.json`
did not move: the test demanded no lowering (rowless, untold and unit counts unchanged: conductor units are not counted there).
Census (`judgment-census.json`): a `note` on `no_move.py::check_args`, `::validate_options`, `::site_check`; their roles were already
`["conductor"]` (T7f/FL4 on main); classes untouched (FL4's `check_args` `xref` kept); no `blocking_per_role` change. "census: no new
blocking unit": `prose_refusal` got a site and `test_judgment_census` is green with no census row for it.

## 5. Why the command rows are out: the measurement

`stage_joints.py --check --data <copy with one conductor row>` printed `told_ratchet.unsited is 17 but 18 rows have no site in code`
(the first run, section 1). The 14 drafted command rows name `controller.py`, `waiver.py`, `source_exclusions.py`, `stage_done.py`,
none of which is in `owns`. A literal `refusal("<id>", ...)` there is another node's edit; a raise of `unsited` is forbidden for me.

## 6. FR walk (touched sections)

A (refusals): FR-1/FR-2 texts byte-identical, the id rides the Record; FR-59: no row unreadable path added, an unreadable row gives the
existing factory-defect sentence through `refusal()`. B: not touched (the conductor prompt is not text a person reads; FR-6 untouched).
C: FR-14 the section is additive after the moves; FR-38 the conductor is told the requirement before the work in the prompt. D: FR-16
literal ids at the sites; FR-17 one seam (`moves_section`). E, F: not touched. G: FR-30 English ASCII (changelog fragment, `--lang` green),
FR-32 each site has a row that fails on the bare form (negative control), FR-54 siblings below.
AR touched: AR-15, AR-17 (one seam, the launch prompt), AR-10, AR-13 (`told_line` / `rows_for` are the only readers), AR-29 (no check
added or moved).

## 7. Questions to the Lead

- Q1 (command rows). Landing the 14 drafted command rows needs, per row, either a literal `refusal()` site in `controller.py`,
  `waiver.py`, `source_exclusions.py`, `stage_done.py` (a siting node), or a raise of `told_ratchet.unsited` by 14 (forbidden for me).
  Which? Until then the section lists only the four `no_move:` rows, so a rework launch is told `no_move:args` and no command row.
- Q2 (a file outside owns). `( cd PKG && python -B scripts/tests/dry_exits.py --check )` is RED, 4 lines, verbatim:
  `FAIL joint no_move:args: the driver has it and no row names it; add a row to fixtures/driver-exits/<group>.json with reach seed or live_only (or unwalked, counted in that group's ratchet) and a why_unreached`
  (the same for `no_move:class`, `no_move:options`, `no_move:prose`) -> `dry_exits --check: 4 discrepancies`. The `<group>` is not named by
  the tool. Precedent: `fixtures/driver-exits/gates.json` holds ledger lines `unwalked | joints/<id> | L1c census catch-up, 2026-11-17`
  (a raise of that group's `unwalked` ratchet) for sited rows. Four rows with `reach: live_only` and a `why_unreached` would raise nothing.
  Which group and which form? I did not edit it.
- Q3 (E-T9c-3, `planning_contract:plan.unmarked_revision`). Read `planning_contract.unmarked_revision_errors` (`planning_contract.py:274-284`).
  Proposed sentence, NOT landed: "A plan row the S3 projection did not stamp carries no `coverage_contract_revision`, and gate A's
  gate-inputs refuses the whole plan while any row is unmarked; code writes the mark when S3 closes." Door: "the conductor reruns the S3
  step, never the role." Open: its `when` (no `conductor_answer` or move token names it; `always` is not a conductor token), and its site
  (the lines are bare by design, `planning_contract.py:292`): the row would be unsited (a raise) until a literal lands.
- Q4 (rows that over-claim, EC-8). `no_move:args` as drafted (mech §5.5) says "cases ... or plan rows (never both) ... (at least one from
  S4)"; since FL4 `check_args` also accepts `candidates` at S7 INSTEAD of cases (`no_move.py` `if candidates:` branch; `rework_args_list`
  prints that line above). Landed VERBATIM as drafted, not edited; the Lead may want the sentence to name candidates.
- Q5 (edge not named by the spec, unreadable rows file). `moves_section` prints `- none: code checks nothing ...` when `rows_for` returns
  `[]`, which it also does for an UNREADABLE rows file (FR-41/FR-59: an unknown shown as a fact). The page's precedent is a line
  `NOT KNOWN: the rows of what code checks could not be read (<why>).` I left the spec's behaviour and did not invent this.

## 8. Analogs noticed (not widened)

- `driver_conductor.py:203` calls `PO.question_rule` itself for the same requirement as `no_move:class` and prints its own text: another site
  of the same requirement, bare.
- `driver_machine.py:2753`, `:3629` call `check_args` (the same requirement as `no_move:args`), bare, outside owns.
- `none` line wording: the card says `- none`, mech §2.9 gives the longer sentence; I used the mech sentence (`NOTHING_CHECKED`).
- `prose_refusal` empty-question and the action rule are bare (section 2).

## 9. Witness (verbatim tails; each judge once after all edits; the slow ones ran in one batch after the last code edit)

`stage_joints.py --check`:
```
stage joints: walked exit 8, detector 5, window 28 | rows 273, gaps 4 (producer 2, told 1, demands 1), joints held 4 of 273 | role leg not walked (code-to-code rows): 27 | stages with no detector: S0, S1, S6, S7, S9 | told counters: hand_cards 12, legacy_legs 0, unsited 17
stage joints: clean
exit 0
```
`test_controller_doors.py`: `=== test_controller_doors: 53/53 ok ===` (the new rows are the `launch-section/*`, `launch-prompt/*` and `refusal-text/*` lines)
Other printed non-slow files run alone: `test_scenario_walk: 95/95 ok`, `test_scenario_world: 33/33 ok`, `test_exploration: 219/219 ok`,
`test_retro_numbers: 316/316 ok`. Printed but in `slow_tests.json` (the four scenario stories, `test_detector_verdict`, `test_contract_slices`,
`test_story_run_*`, `test_controller_rework_*`, `test_person_owned_paths`, `test_selftest_slow_tests`): judged by the batch canon.
Slow judges of this change, run once each (exit 0, 0 FAIL lines):
```
=== test_stage_joints: 340/340 ok ===        (first run: 338/340, the two pins above; red before the pin edit, green after)
=== conductor doors: 224/224 ok ===
=== judgment_census: 25/25 ok ===
=== no_move seam_c26_g27_f2: 87/87 ok ===
=== no_move seam_k4s: 73/73 ok ===
=== no_move seam_n1_n9: 119/119 ok ===
=== no_move seam_n2b_n15: 188/188 ok ===
=== no_move seam_sites: 506/506 ok ===
```
`contract_slices.py --check`: `slices: 44 declared, all present and fresh; 19 key pages; 12 charters carry a generated digest line` (exit 0).
`selftest.py --limits --lang`: `PASS limits: every mandatory role rule of design/role-rules.json holds in its carrier` / `=== qa-factory selftest: 4/4 ok ===`.
`dry_exits.py --check`: RED, Q2 (4 lines, verbatim in Q2).

Negative control (DoD 4), `no_move.py` byte copy `no_move_NEW.py`, the `no_move:prose` site turned bare:
```
sha256 before  74aa99def434450e934896a3d5930e7416f24496db69eb58adf58a479fa847ce
stage_joints --check -> unsited 18 / REJECT - 1 finding(s): told_ratchet.unsited is 17 but 18 rows have no site in code (...)
test_controller_doors -> FAIL refusal-text/prose: the text, the id the Record carries - expected ('the question names `go on`, which is not one of its options', 'no_move:prose'), got ('the question names `go on`, which is not one of its options', '')   [52/53 ok]
restore by cp from the copy
sha256 after   74aa99def434450e934896a3d5930e7416f24496db69eb58adf58a479fa847ce   (equal)
```
Item 3 note: the prompt row calls `story_run.Driver._conductor_text` (the one caller of `moves_section`) with a stub `self`; the full
`no_move` flow through a seeded driver was run once by hand (a stub conductor received the prompt: moves, then the section with the three
`conductor_answer` rows, then the state text) and the canon's K12 `PromptRig` prompts pass through the same function (conductor_doors green).

## 10. Needed beyond the manifest

`scripts/planning_contract.py` (Q3), `scripts/driver_machine.py` and `scripts/driver_conductor.py` (callers), `scripts/story_run_common.py`
and `scripts/tests/test_conductor_doors.py` (a prompt rig), `scripts/slow_tests.json`, `scripts/tests/dry_exits.py` and
`fixtures/driver-exits/` (Q2), `scripts/contract_slices.py` (`requirement_section`), `scripts/refusal_registry.py` via the walk. The finish spec
sections for the T1r-cards `stage_done:set` sentence were not in the given.

## Follow-up t-1087

Three Lead answers made (Q2, Q4, Q5); Q1 and Q3 untouched (a siting node).

1. Q2: `fixtures/driver-exits/gates.json` gained the four joints `no_move:args|class|options|prose` (joints table, reach `unwalked`, why `T9c conductor rows, 2026-11-17: reached by the gate rows' conductor calls, not yet judged by a row of their own`) and four `raised_by` lines `unwalked | joints/<id> | <same reason>`. NAMED MOVE: the group's `unwalked` credit (raised_by entries) +4 (227 -> 231; rows 287 -> 291). The group's `ratchet.unwalked` base number stays 21: raising it made `--check` red ("stale raise credit: 231 entries, 227 rows above base"), because base + named credits must equal the rows; the base is the floor, the raise is the entries. No other pin named; no file outside owns touched.
2. Q4: the `no_move:args` sentence now reads: "...name a stage that can be sent back, a role that did accepted work there, a cause from the list, and the work to redo as one kind only: cases inside the approved scope (at least one from S4), plan row ids (S1-S3), or bug candidates the story lists (S7 only, instead of cases)." Derived from `check_args` branches (candidates: S7 only, never with cases/rows, from `facts["candidates"]`; cases and rows never together; rows are not judged by `check_args`). No pin of the text existed in `test_stage_joints.py`; `test_controller_doors.py` got table `ARGS_KINDS` (7 rows, expectation from the branches) and a sentence row.
3. Q5: `no_move.moves_section` now calls `stage_joints.load_rows()` itself (the public reader that already returns the reason, so no change outside `no_move.py`), treats a `joints` that is not a list as unreadable, prints `NOT KNOWN: the rows of what code checks could not be read (<why>).` and keeps `NOTHING_CHECKED` for a readable file with no rows. Precedent wording and form: `contract_slices.requirement_section` (`scripts/contract_slices.py:729`). Table `UNREADABLE_ROWS` (6 rows: absent, 0 bytes, not JSON, not object, joints-not-list, readable-no-rows) in `test_controller_doors.py`.

Analog noticed: `stage_joints.rows_for` still returns `[]` for both unreadable and empty (documented); other callers of it that print "none" would have the same fault (not searched).

Witness (verbatim tails):
```
dry_exits --check: 0 discrepancies
NUMBER ratchet (rows now / base): live_only 31/0, after 0/0, unwalked 291/60, hook_layer 77/77; raised_by 262
dry_exits selftest: 160/160 cases
stage joints: clean   (rows 273, told counters: hand_cards 12, legacy_legs 0, unsited 17)
=== test_controller_doors: 67/67 ok ===
=== test_stage_joints: 340/340 ok ===
=== judgment_census: 25/25 ok ===
=== conductor doors: 224/224 ok ===
=== no_move seam_c26_g27_f2: 87/87 ok ===
=== no_move seam_k4s: 73/73 ok ===
=== no_move seam_n1_n9: 119/119 ok ===
=== no_move seam_n2b_n15: 188/188 ok ===
=== no_move seam_sites: 506/506 ok ===
PASS limits: every mandatory role rule of design/role-rules.json holds in its carrier
=== qa-factory selftest: 4/4 ok ===
```
Negative control (byte copy of `no_move.py`, the NOT KNOWN branch turned off):
```
sha256 before  9a7981c586274d8c05663ad44c2a6af29d2131bd6cd413e3af43397cf4abf10b
FAIL launch-unknown/absent|empty-file|not-json|not-object|joints-not-list: NOT KNOWN with the reader's reason, never `none` -- - none: code checks nothing ...
=== test_controller_doors: 62/67 ok ===
restore by cp from the copy
sha256 after   9a7981c586274d8c05663ad44c2a6af29d2131bd6cd413e3af43397cf4abf10b   (equal)
```
Needed beyond the manifest: `scripts/stage_joints.py` (`load_rows`, `rows_for`), `scripts/contract_slices.py`, `scripts/null_outcomes.py`, `scripts/tests/dry_exits.py` (read only).
