# P1-b N4:gates report (t-1037, builder)

Worktree branch `worktree-agent-a4aebd95c3ca7d59c`. Files: `fixtures/stories/dry-1/exits/gates.json` (46 rows), `fixtures/stories/dry-1/seeds/gates.json` (`recipes: {}`), `fixtures/driver-exits/gates.json` (census), this report. `known_red/gates.json` is NOT created (see "needs a label"). Node comes back RED: 6 rows of `gate_A` need a label from the Lead.

## Table: row id -> start -> reach -> outcome (group run 1 of the final file, 676 s)
| row id | start | reach | outcome |
|---|---|---|---|
| gate_A/rework, approve, retry, stop, free words, empty | S4 | story | FAIL x6 (K15 key not observed; C2 offered set read from the wrong key) - needs a label |
| gate_A/words:questions-deferred (FV1-8 state) | S4 | live_only | NOTE live_only (measured, below) |
| gate_B/rework, approve, retry, stop, free words, empty | S8 | story | NOTE `after:FV3-5: its start snapshot S8 was not made` x6 |
| route:marked_repair, form_vocabulary, handover_form, missing_output, handoff_form /code move | S0 | live_only | NOTE live_only (measured, probe) x5 |
| route:active_dispatch, already_done, committed_event, dead_dispatch, gate_stage, known_false, not_in_build, stale_revision, unmatched /code move | S0 | live_only | NOTE live_only ("estimate, not verified") x9 |
| route:marked_person/free words | S0 | live_only | NOTE live_only ("estimate, not verified") |
| joint:exit_gate:{scoped,detector_errors,witness_errors,digest,required_outputs,text_end_after_handback}/{repair,no repair,word} | S0 | live_only | NOTE live_only x18 (digest: measured; the other five: "estimate, not verified") |

Census `driver-exits/gates.json`: 15 routes + 6 joints moved `unwalked` -> `live_only` with a why; ratchet `unwalked` base 21 -> 0 (the 84 L1c joints stay `unwalked`, F-P15 (b)); `live_only` base stays 0 and 55 `raised_by` entries name every live_only row (21 census + 33 walk + 1 FV1-8 row), same double-count form as N4:s0 (F-P8 (a)).

## Rows that run but are red: need a label (the Lead places it; nothing labelled by me)
All six are one reason, a WALKER defect, class proposal `stub gap` (walker/test layer, not product): `gate_A/rework`, `gate_A/approve`, `gate_A/retry`, `gate_A/stop`, `gate_A/free words`, `gate_A/empty` -> proposed finding "the walker cannot judge a gate key: the LAST record of dry-priced.jsonl at the gate_A ask is s1.review's (measured via the K15 text; whether any gate_A record exists at all was not read; the spy wraps `no_move.priced_options` only), so K15 reads that key (s1.review) and C2 takes its answers (agree, flip) as the offered set of the gate". Evidence (verbatim, probe 1 and final run): `FAIL ... gate_A/approve - C2: the token 'approve' was not offered at 'gate_A' (offered ['agree', 'flip']); K15: key not observed: expected gate_A, observed s1.review`. Same for the other five. Side effect: `gate_A/retry` and `rework` also print C3 red (the answer is not taken as the wrong key's token) - consequence of the same cause, not measured apart.

### FV1-7 and FV1-8 labels: NOT written (deviation from DoD item 3, with the evidence)
- FV1-7 (I-gate, C6): row `gate_A/approve` lists C6 and C6 did NOT fail (the failure text names only C2 and K15): the dry world's gate A is `gate_ready` true at S4 (the main pass also prints PASS gate_A, N2g report). The product red FV1-7 describes does not reproduce today; the row is red only for the walker reason above. A label FV1-7 would hide the walker defect under a product id (card edge 2, AR-28) and the next run would find it green (stale label).
- FV1-8 (`questions` x `go on`, then `gate_A` x `approve`): the state needs an open question the person left "until the report". Measured: Grep `question_register|QR\.` over `dry_*.py` -> 0 hits; positive control, same tool and filter, `def fill_role` -> 1 hit (dry_stub.py); no op of the closed seed list writes the register. The row `gate_A/words:questions-deferred` is `live_only` with that reason; a ledger row for it would be `unknown row` red (`known_red.reconcile`), so it carries no label.
- Consequence: `pins.known_red` file not created (0 rows). Question 1 below.

## live_only rows, reasons
- Measured (probe 2, rows run from snapshot S0, token `agree` at s1_review, stub control on qa-requirements-tester): `route:marked_repair`, `form_vocabulary`, `handover_form`, `missing_output` (control: `verdict: bogus`), `route:handoff_form` and `joint:exit_gate:digest` (control: `result_text: "I did the work."`). Output verbatim:
```
FAIL dry-1/exits:gates/route:marked_repair/code move - route: route not observed: 'marked_repair' was not matched by the driver during the row (state/dry-routes.jsonl)
FAIL .../route:form_vocabulary/code move - route not observed ...   FAIL .../route:handover_form/code move - route not observed ...
FAIL .../route:missing_output/code move - route not observed ...    FAIL .../route:handoff_form/code move - route not observed ...
FAIL dry-1/exits:gates/joint:exit_gate:digest/no repair - joint: joint not observed: no refusal line of the driver names 'exit_gate:digest'
=== scenario dry-1: 1/13 ok ===  rc=1 s=163.7
```
  C2 and C3 of the S0 ask passed on all six rows. Reason: the walker's post-answer turn is one driver boundary (`--max-boundaries 1`) and ends before the S2 role runs, so a role-handoff refusal is never read; and a joint id is not in the only text it reads (`resume <dispatch>: <class words>` from `resume_reason`, `driver_dispatch.py:155-174`).
- "estimate, not verified" (reasoned from code, not run): the other 9 routes of the table, `marked_person`, and the five other exit_gate joints (same road as digest, not tried each).
- `gate_A/words:questions-deferred`: measured by Grep as above.

## Rows that will print `after:` (edge 1, TEMPORAL)
`gate_B/rework, approve, retry, stop, free words, empty` (start S8): print `after:FV3-5` by the label `main/S5`; they run by themselves once the main pass passes S5 (checks C2, C3, C6 / `empty`). No static `after:` rows.

## Verbatim: `dry_exits.py --check` (tail)
```
NUMBER ratchet (rows now / base): live_only 86/0, after 0/0, unwalked 264/37, hook_layer 77/77; raised_by 313
NOTE ratchet live_only: raised 86 row(s) above the base 0, named in raised_by: [...86 entries...]
NOTE ratchet unwalked: raised 227 row(s) above the base 37, named in raised_by: [...]
dry_exits --check: 0 discrepancies
```
(`live_only 86` = the repo-wide sum: s0 16 + s1-s4 15 + gates 55; `unwalked 264/37`: 84 of this group are L1c joints.) Strict walker load of my rows (no world): `strict load ok: 46 rows; universe.errors: []`, `unwalked: 84 (census unwalked 84: ...; variants without a row 0)`.

## Verbatim: group run (`test_scenario_dry_1.py --part exits:gates`, 676 s: SLOWER than a couple of minutes, the prefix alone is 408 s; the coordinator's door judges it)
```
NOTE dry-1/exits:gates/prefix: reached S4 in 408.1 s; snapshots S0, S1, S2, S3, S4, gate-A; stopped: the road met the conductor: ... conductor at S5 ...
FAIL dry-1/exits:gates/gate_A/{rework,approve,retry,stop,free words,empty}  (texts above)
NOTE dry-1/exits:gates/gate_B/{rework,approve,retry,stop,free words,empty}: after:FV3-5: its start snapshot S8 was not made
FAIL dry-1/exits:gates/known_red - new red: gate_A/{approve,empty,free words,retry,rework,stop}
PASS dry-1/exits:gates/outcomes
NOTE dry-1/exits:gates/unwalked: 84 (census unwalked 84: joint:execution_request:active_dispatch, ...)
=== scenario dry-1: 1/13 ok ===  rc=1 s=675.6
```
(The 34 live_only NOTE lines and the scoreboard NOTEs are left out here; every row had exactly one outcome: `outcomes` PASS.)

## Unwalked remainder by origin
N1 epoch: 0 (21 -> 0). L1c: 84 joints stay `unwalked`, each with its `raised_by` entry (F-P15 (b)): execution_request 14, exit_gate 3 (EG-digest-form, EG-text-end, adviser), guard_pre_tool 24, handoff_check 19, host_adapter 8, role_cli 4, run_suite 3, stage_guard 8, validate_artifacts 1.

## Walker defects noticed, not fixed (non-goal: `dry_world.py`, `dry_exits.py`, `dry_stub.py`, `dry_driver.py`)
1. Gate keys unobservable: `dry-priced.jsonl` has no `gate_A` record; K15 and the C2 fallback read the last priced key. Fix site: `dry_driver.py` price spy (cover the gate path, `driver_gates`) or `dry_exits._judge_always` / `_check_c2` for gate asks.
2. Joint observation: `judge_row` needs the joint id in the driver's first `resume ...` line; `resume_reason` prints class words only, so no exit_gate joint can pass; the check ids live on `Record.check` and are not printed.
3. Post-answer window: one boundary, loop ends on the first turn with no new ask; a refusal of a LATER role (S2 onward) is not reachable from S0 and a mid-stage refusal cannot be a `drive_until` target (a seed that meets the conductor is "not reached"), so refusal-driven routes/joints have no road.
4. Prefix of an `exits:` part runs on past the stop stage (this run: "stopped: the road met the conductor ... S5"), 408 s; harmless, noted.

## FR walk
A-F: test-layer data only, no package behavior or text a person reads changed (FR-13: variety stays in data rows; FR-59: unknown stays red/NOTE, never a pass). G: FR-30: files hold ASCII only (generated); no control byte. AR-28: no red row hidden under a borrowed label; AR-20: every live_only raise has one `raised_by` entry, `unwalked` base lowered 21 -> 0.

## Questions
1) FV1-7/FV1-8 labels: write nothing (my choice, evidence above), or do you want `gate_A/approve` labelled FV1-7 anyway? The honest label for the six red rows is a walker finding (K15 on gate keys); give me the id, or dispatch the walker fix first (then the rows are likely green except possibly C3 of retry/rework).
2) Joint rows are 3 live_only rows each (F-W3 / `group_unwalked` demand all three once a row exists), 18 rows + 6 census rows = 24 raises for 6 joints: intended, or census-only live_only like N4:s1-s4?
3) `gate_B` key rows written (6, `after:FV3-5`); `gate_A`/`gate_B` are price keys (not census entries, edge 4): keep them in this node or leave to N4c (F-P9)?

## Siblings noticed
Axis 5: `route:handoff_form` and `joint:exit_gate:digest` both sit on the final-message digest check (one state, two subjects); `exit_gate:digest` and `exit_gate:EG-digest-form` (L1c) likewise. Axes 34/38: same walker limits will hit s5 and s6-s9 rows (joints, key rows of gates inside those groups).

## Needed beyond the manifest
`dry_exits.py` (`judge_row`, `group_unwalked`, loaders), `dry_world.py` (`run_exit_row`, `run_seed`, `walk_exits`), `dry_stub.py` (control grammar), `dry_driver.py`, `driver_dispatch.py` (KNOWN_REFUSALS, `resume_reason`), `driver_machine.py` (`match_known`), `exit_gate.py` (`all_errors`), `detector_verdict.py` (`with_check`), `known_red.py` (`reconcile`), `test_scenario_dry_1.py`, `references/stages.json`.

## Walker fix (t-1044, builder)

Item 2 DONE, item 1 NOT DONE (returned as a question; no spy written, nothing wrapped).

### Item 2 (joints, census-only like N4:s1-s4)
Removed the 18 `joint:exit_gate:*` rows from `fixtures/stories/dry-1/exits/gates.json` (46 -> 28 rows) and the 18 `walk/joint:exit_gate:*` entries from `ratchet.raised_by` of `fixtures/driver-exits/gates.json` (139 -> 121). The six `joints/exit_gate:*` census entries keep `reach: live_only` with their why and keep their one `raised_by` entry each. No F-W3 / `group_unwalked` refusal arose.
Witness (`( cd .../ai-packages/qa-factory && python -B scripts/tests/dry_exits.py --check )`, tail):
```
NUMBER ratchet (rows now / base): live_only 68/0, after 0/0, unwalked 264/37, hook_layer 77/77; raised_by 295
NOTE ratchet live_only: raised 68 row(s) above the base 0, named in raised_by: [...68 entries, 6 `joints/exit_gate:*` census, no `walk/joint:*`...]
dry_exits --check: 0 discrepancies
```

### Item 1: why nothing was wrapped (read, not run)
There is no function that resolves the offered answers of a gate ASK; the ask itself carries none:
- `driver_gates.py:288-322` `gate()` ends in `raise Person(f"gate_{gate}", head + body, ...)`: a plain Person (no `offered`, no `options`). `gate_text` (`driver_gates.py:106`) has no price/NM call (Grep `NM\.|priced|gate_option` over driver_gates.py: 0 hits; positive control, same filter: `def gate_text` found).
- `driver_dialog.py:321` writes `offered` into `asked` only `if person.offered`, so the gate ask records no offered set.
- The gate rows (`rework/approve/retry/stop`) are priced only by the SEAM fallback, after an answer the driver could not read: `driver_conductor.py:491-492` `fallback_person` -> `gate_fallback_question` (`:504`) -> `NM.priced_options("gate_A"|"gate_B", ...)` at `driver_conductor.py:523` (and `gate_prices` -> `priced_section("gate_A")` -> `driver_runner.py:1285`, the conductor prompt). Both already pass through `no_move.priced_options`, i.e. through the EXISTING spy of `dry_driver.py:73` (`NM` is the module, looked up at call time). A second spy on `gate_option_rows` / `gate_fallback_question` would record the same moment.
- Consequence: a `gate_A` record exists in `dry-priced.jsonl` only AFTER the first answer is not read, and `dry_world.py:1243-1244` reads `priced[-1]` at the ask, before the answer. The K15/C2 reds are therefore not a lost record: at the ask nothing is priced, and for a row whose token is a seam token (`approve`, `retry`, `stop`, `rework`) the offered set exists only in the seam question that comes after the first (unread) answer. (Whether the tokens of these rows are taken at the plain gate ask by `take_answer` was not run.) The fix is not a spy in `dry_driver.py`; it is a design decision in the judge (what offered set a plain gate ask is judged against: the `question-prices.json` `gate_A` rows, or the record of the seam question that follows) -- "do not invent a second road in the judge" applies, so I stopped.
- No file edited for item 1. Spy unit table: it exists, `dry_stub.py:1377-1389` (passing_spy / sink_path cases); no row added (no spy added).

### Rows still red
Unchanged from the first part of this report: `gate_A/{rework, approve, retry, stop, free words, empty}` FAIL on K15 / C2 (`FAIL ... gate_A/approve - C2: the token 'approve' was not offered at 'gate_A' (offered ['agree', 'flip']); K15: key not observed: expected gate_A, observed s1.review`). Not re-run this round: item 1 did not change the walker (the 11-minute part run was not started; negative control line is the one quoted above).

### Diff
`git -C <tree> diff --stat 6ca7829b..HEAD`: only the two fixture files and this report (see the commit); no production file.

### FR walk
A-F: test-layer data only, no package behavior or text a person reads changed. G: FR-30 ASCII only, no control byte; FR-13 variety stays in data rows; FR-59 an unknown stays red, never a pass. AR-20: every live_only raise keeps exactly one `raised_by` entry.

### Analogs noticed (not fixed)
- `gate_B` rows (6) and the key rows of gates inside groups s5, s6-s9 will meet the same plain-gate-ask situation (no price record at the ask).
- Every census-only joint exit_gate row of other groups follows the same one-form rule; none touched.

### Question (for the Lead)
1) At a plain `gate_A`/`gate_B` ask the driver offers no answers and writes no price record; the options (`rework, approve, retry, stop`) appear only in the seam question after an unread answer (`driver_conductor.py:523`). Which is the intended judgment: (a) judge the six rows against the `gate_A` data rows of `question-prices.json` plus the driver's acceptance of the token (a judge change in `dry_exits.py` / `dry_world.py`: K15 key from the gate kind, C2 offered from the data rows), or (b) drive the ask to the seam question first (a `dry_world.py` row-runner change, non-goal now), or (c) keep the six rows `live_only`/walker finding? Recommendation: (a).
