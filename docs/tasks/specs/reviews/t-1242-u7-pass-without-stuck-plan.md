# t-1242 - plan critic on spec U7 "pass without getting stuck" (t-1240)

Plan under review: `docs/tasks/specs/20261117-u7-pass-without-stuck-spec.md` with the Lead acceptance header. DoD: the brief
(`20261117-u7-pass-without-stuck-brief.md`): "Охват", "Решено", "Край от владельца", "Что должна содержать спека" 1-8.

**Verdict: NEEDS WORK.** 6 findings block dispatch of the streams they name (B1-B6), 8 are fix-before-dispatch (M1-M8).
The direction is right: role first through the one seam, defaults said out loud, unknown never a pass. The streams are not yet
executable as written. Accepting the plan, and any change to the forks, is the Lead's decision (rule 6).

## Findings

**B1 - r4 premise does not reproduce; stream 4 cannot implement the path the code already shows (K3, K4, Q13c).**
`driver_stage_s7.py::failures_to_triage` 13-20: `not_executed` is accepted only when `s7_pretriage.s6_closed_by_code` holds,
i.e. when S6 closed on a code-only receipt. Otherwise it raises `Refusal("S7 entry: ... nothing to triage yet; the S6 halt that
produced it stands")`. A `reporter: none` run is a real S6 run (no code-only receipt), and `run_suite.py:366` records it
`not_executed`. So S7 refuses. The Lead's D-4 spot-check ("reads `not_executed` as intended") covers only the code-only close.
The measurement will land on outcome (b). F-4(b) needs files no stream owns: the S6 runner road / manual-evidence recording,
`driver_stage_s6.py` (owned by stream 6) and maybe `run_suite.py`. As it stands r4 is a block (class B), not a silent default.
Fix: re-class r4, write F-4(b) as its own node with owns, edges and a test, and drop the measurement or keep it only as a
witness.

**B2 - r11 starves S5's required output and its readers (AR-22, AR-25; K2).** `references/stages.json` S5 `required_outputs`
= `work/automation-manifest.json`. S6 `inputs` list the same file (stages.json:228). `s6.nothing` cites it as evidence
(`driver_stage_s6.py:511`). About 70 production modules read it (Grep `automation-manifest\.json` in `scripts/*.py`). The
spec leaves the absent-manifest world as "builder reads stage_done and returns a question". That is a fork handed to a weaker
model, and S6/S7/S8 are never walked. Fix: choose now. Either S5's code close writes the empty manifest through its one writer
(`manifest_put.py`, AR-14), or every reader's behaviour on a missing manifest is stated. Name the carrier of the class:
frozen `plans/BACKLOG.md` B-006 ("ручной маршрут S4→S6": S5 closes normally, S7 `not_executed` with nothing to triage, gate A
does not ask about the toolchain at zero automate rows, required outputs checked per role). D-2 reads NE25 as "design says S5
closes". NE25's "as it did before the plan existed" points at that same refused road, so B-006 is the real carrier. Its other
items are r11's siblings: the owner's goal is "all stages", and L4 proves S5 only. Also name SIBLING_MAP axis 5 row "Code-only
stage closes" (C3-2, accepted 5378bbef, which kept `code_only` S5 refused) and the existing pin
`test_controller_state.py:1145` (refusal text "allowed only for S0, S6, S7 or S8").

**B3 - Seam-first sites name conductor moves that do not exist (r8, r9; K6, P11/AR-12, PROJECT p.11).** The conductor acts
only through `references/conductor-actions.json`: `moves` = rework_stage, approve_gate, resume_with_words,
release_and_restart, go_on_as_is, story_fact, stand_prepare, revoke_exclusion, person_does, stop_here, plus the `actions`
rows. There is no "locate the tool on the machine" (r8) and no "a tests_root discovery saw elsewhere" (r9). Usable rows exist:
`install_dependencies` (r8), `readiness.py --write --probe-vcs` (r9 vcs), `stand_prepare` (r10, authorized by the `Stand
remedy:` line). Fix: per site, list the existing rows the conductor may use. Any new row goes into a stream's owns with its
table entry, or the item is cut. Bound the cost: no paid call when `NM.open_moves` leaves nothing for the state, e.g. a missing
`ticket_adapter` (credentials are the person's remainder). The §1.1 AR-12 check "web project byte-identical" is false for
r8/r9/r10, which fire on web projects too. Restate it (Q13b).

**B4 - Prescribed test homes are quarantined (K7, Q5g).** `scripts/tests/test-layers.json` `quarantine` holds
`test_surfaces.py` (stream 1, all r2/a2D1 rows, including flips of the existing rows 269 and 275-310) and
`test_story_run_gate_repair.py` (r12, 364.8 s). By the spec's own rule the builder stops on the first edit, so streams 1 and
5a are not dispatchable. The designer did not read the ledger (§12). Fix: put the rows in keep files (for example
`test_readiness.py`, detector layer, for the r2 data seam), or give a `quarantine-edit:` reason that holds.

**B5 - Same fact, two roads at gate A (r8 class completeness, P31, K5).** `gate_preflight.py:2966-2977`:
`check_s5_toolchain`'s `not_started` branch raises the same `executor_question` card, and the code says why: "Two differently
worded questions about one missing binary is two stops". `run_suite.py::refuse_missing_executor` (1556-1578) is the third
member. Stream 5a owns "check_s5_executor and helpers only". If r8 becomes seam-first, the other two stay person-first. Fix:
all three in stream 5a on one road. Q-2 is answered: yes, U7.

**B6 - The F-2(a) state has no exit unless the spec gives it one (AR-25).** A GATE_REPAIRS row works on `factory_fixable`
findings, and `stage_done.py:482-484` refuses S4 over any remaining `factory_fixable`. If the conductor's turn does not settle
a missing launcher, the finding must turn back into the PERSON_DECIDES card. If it stays fixable, S4 is held. Fix: state the
transition and its row. Model it on the existing `s5_reporter` row (`driver_gates.py:30-33`: one conductor turn, then the
card). The spec does not cite it (Q6).

**M1 - The seam entry is under-named (r9, r10; Q6).** The one entry is `Driver.no_move(state)` with `site_fallback`. Copy
`driver_machine.py:2153-2155` but with the conductor called. `_no_move` (`driver_conductor.py:646`) skips the conductor when
`call` is False, and `EXCLUDED_KINDS` go to legacy. A builder copying that template ships no conductor turn. §1.1 names
`Conductor.conductor`, which only `_ask_conductor` may call (axis 5, I-one). Precedent at S0: `self.unread("ticket_auth", ...)`
(`driver_s0.py:434`). Name the r9 test file (`test_no_move_seam_sites.py` holds `s0.ticket_auth` rows), not "the S0 test the
witness prints".

**M2 - §1.2 owner column contradicts the census (Q11).** `judgment-census.json` rows 415 (`check_s5_executor`) and 1118
(`stand_check`) say `owner: data`. In the census, `owner: judgment` goes with `meaning`/`meaning-proxy`, the counted
judgment-in-code classes. There are 0 rows with (judgment, shape). Routing a state to the conductor keeps owner `data`; the
judgment is the conductor's, outside the unit. Fix: set `data` for s0_rest, check_s5_executor and stand_check. Say that
declared_surfaces, _row_of_nobody, _check_plain_environment, s0_rest, stage_S5 and _no_entry have no census row and that
none is added.

**M3 - Owns overlap / gap.** The r2 data seam row goes into `test_readiness.py`, which stream 3 owns and stream 1 does not.
OF5-5's owns cell (D-5) must be corrected before stream 6 starts.

**M4 - E-7 has no owner stream.** The role behaviour ("brings up the second instance ... records `tried.md`") needs runner /
environment-preparation text, and no stream owns it. Yet L2 claims E-7. Say whether the current text already does it (cite
it), or open a node.

**M5 - F-3 rests on an unmeasured premise (Q13c, PROJECT package p.6a).** If the manual lane refuses a case with no capture
surface, the agent's attempt after `_row_of_nobody` converts has no way out (AR-25). Measure it before dispatching stream 1
item 4. Also say that this reverses EP1-41f N-17 and cite P19 step 3 (agent by hand before person) as the basis.

**M6 - r3 announced sentence may lie (FR-10/FR-37).** "the stand is asked about before tests run" holds only if
`env_probe.py` exits non-zero for a URL-less row (`driver_s0.py:2424-2427` sets pending False on exit 0, and then
`stand_check` returns at once at 167-168). Verify, or drop the clause. Name the existing pins
`test_readiness.py:873-874, 917`.

**M7 - r1 witness keys K3, K4 are already present** (`p1-discovery.md:43`, `p2-interview.md:226`). They cannot fail before
the edit. Replace them with keys new to the edit.

**M8 - Axis 38 and the ratchets are not named (Q9).** New seam sites (r9, r10), the `s5.nothing` close and the gate-row
change touch `scripts/tests/fixtures/driver-exits/<group>.json` (axis 38, same commit), A27 `NO_MOVE_BASELINE` (should
shrink: name it) and `driver-layers.json` (s0_rest, stage_S5, stand_check rows). Put them in the DoD of streams 3, 5a, 5b
and 6.

## Plan-gate questions (K1)

- Q13(a) EDGES: NOT MET. B2 (absent manifest), B6 (fixable exit) and M6 are silent; r2/r3/r9/r10 edges are stated.
- Q13(b) MEANING: NOT MET. "role" = the agent tries first, the person gets the remainder: consistent. "web byte-identical"
  contradicts r8/r9/r10 (B3). Undeclared vs `{}`: consistent.
- Q13(c) PREMISES: NOT MET. D-2 confirmed (`controller.py:6087-6088`). D-4 does not reproduce as stated (B1). F-3 premise
  unmeasured (M5).
- Q13(d) READERS: the block was missing, so I ran it (trail). Lines to answer before dispatch: `config-keys.json` names
  declared_surfaces, _check_plain_environment and check_s5_executor (pins on a value?); `gate-registry.json` and
  `block-names.json` name stand_check; `driver-layers.json` (M8); `judgment-census.json` (M2); `null-outcomes.json`
  (stage_S5); `test_silent_passes.py` (s0_rest, stand_check); quarantined readers (B4). Miss 6: the tool's base was
  b4eb74df; HEAD = origin/main = f7ab564a now, and the files read have no diff.
- Q13(e) FORKS: see K4.
- Q4 CLASS: NOT MET. B2 (B-006 siblings), B5, K5 below.
- Q6 DUPLICATION: NOT MET (M1, B6 templates not reused). "none found" for a second reader of surfaces.json (one reader,
  confirmed).
- Q12 ONE ROAD: NOT MET. (b) `gate_preflight.collect_base` reads `PYTEST_TOKENS`. Non-pytest runners get no toolchain
  rehearsal, have no data row, and are absent from the t-2046 census (grep `PYTEST_TOKENS|check_s5_toolchain|collect_base`
  -i: 0 hits; control `pytest` -i: 19 hits). In U7: say it (class A). The one-road fix (`launch_check.runner_row` is already
  data) needs a node with an owner (U8), opened by the Lead.
- VARIETY: on an all-manual project the target still stops (B2, B-006). On a `reporter: none` project S7 refuses (B1).

## K2 - per site

r1 OK. r2 OK (one note: F-1(a) changes the legacy-shape promise at `readiness.py:1314-1315`; say it). r3 OK apart from M6.
r4 STILL BLOCKS (B1). r5 the person tail stays until RD1-24 (named node, owner's word: acceptable residual). r8 a door past
the role stays on the two sibling roads (B5), and the exit is undefined (B6). r9 a seam turn with no moves (B3). r10 OK
(`stand_prepare` exists). r11 S5 passes, S6+ unwalked (B2). r12 OK. a2D1/s6.unknownword: the way out depends on M5.

## K4 - forks

F-1, F-3, F-6, F-7, F-8, F-9, F-10: the direction is right (F-3 subject to M5). F-2(a) is right, given B5/B6. F-4(b) is
right, and it is the main path, not a contingency (B1). F-5: stream 6 (r10) can go on F-5(a), which is the status quo and the
safe direction. The E-7 part (M4) and any onboarding question that records the authorization (stream 2, p2) wait for the
owner's answer.

## K5 - analogs

Q-4 (`check_s5_toolchain` silent return for non-pytest): U7 by the brief's own exception ("a set whose unknown value gives a
silent default"). In the same function: `tests_root` not a dir returns silently (2938), and the collect timeout goes
straight to PERSON_DECIDES (2978-2984). In the neighbouring `check_s5_dependencies`: "An environment the check cannot read
says nothing here". Q-2: B5. Map: axis 5 (code-only closes, the stage before a gate, one question for every stop), axis 18,
axis 34 and axis 38 walked. B-006 is the class carrier for r11.

## K6 - streams

The owns are disjoint except M3. Not executable for a weaker model as written: B1, B2, B3, B4, M1. The order with RD1-24,
OF5-5, PC4-2 and PC4-4 is right as written. OH3-35 and FV3-21 are correctly named as predecessors.

## K7 - tests

Layers are named and stated as rows, with no new files. B4 and M7. r12, a pin with no code change, is legitimate under
class C. Live rows L1-L6 cover the classes, but L4 must extend to S6-S8 of the all-manual story (B2) and L6 must follow
F-4(b).

## K8 - principles

P2 is kept: no platform word, and E-7 avoids "two emulators". P13 kept ("go on" stays). FR-1/2/57: the r11 reworded refusal
carries a door. P11/AR-12: B3. P27/AR-29: M2. P31: B5 and Q12. FR-4: the readiness and surfaces notes inform, they do not
pass.

## Trail

Read: the spec (whole), the brief (whole); `surfaces.py` 15-149; `readiness.py` 855-894, 1295-1323;
`test_readiness.py` 840-924; `gate_preflight.py` 440-472, 760-786, 2876-2984; `driver_s0.py` 725-744, 2300-2340,
2380-2427; `driver_conductor.py` 476-515 (+ grep `call`, `no_move`); `driver_runner.py` 1300-1315;
`driver_machine.py` 2140-2159; `driver_stage_s5.py` 185-244; `driver_stage_s6.py` 490-519; `driver_stage_s7.py` 5-29;
`controller.py` 4215-4276 (+ grep 6080-6096); `stage_done.py` 474-489; `driver_gates.py` 20-49, 500-529;
`planning_contract.py` 2268-2352; `manual_capture.py` 424-473; `run_suite.py` 1545-1584; `probe_by_code.py` 1450-1469;
`driver_stage_build.py` 139-206; `references/stages.json` 179-236; `null-outcomes.json` 25-31; `conductor-actions.json`
60-194; SIBLING_MAP axes 5, 34-38; `plans/BACKLOG.md:79`; `plans/piles/conductor/batch-3-vhodyashchie.md:3,26`;
`docs/OWNER_PRINCIPLES.md` P19.
Commands: `owns_readers.py --paths <13 touched> --names <10>` -> "readers: 724 outside owns ... base origin/main b4eb74df";
the test-layers lookup -> `test_surfaces.py quarantine`, `test_story_run_gate_repair.py quarantine` (364.8 s),
`test_mobile_road.py quarantine`, the others keep; the census lookup -> rows 415/1118 `owner: data`, 0 (judgment, shape);
the conductor-actions key dump (moves listed in B3); `git log -1 HEAD/origin/main` -> f7ab564a both, and the diff of the
read files is empty.

```json
{
  "verdict": "blocker",
  "blockers": [
    "B1 r4: S7 refuses not_executed after a real S6 run (driver_stage_s7.py:13-20); D-4 premise does not reproduce; F-4(b) is the main path and no stream owns its files",
    "B2 r11: S5 code close leaves work/automation-manifest.json (S5 required output, S6 input) absent with readers unwalked; B-006 manual-route siblings S6-S8 not walked",
    "B3 r8/r9: seam-first names conductor moves absent from conductor-actions.json; cost unbounded; AR-12 web byte-identical claim false",
    "B4 test homes quarantined: test_surfaces.py (stream 1) and test_story_run_gate_repair.py (r12)",
    "B5 same missing-launcher fact keeps two person-first roads: gate_preflight.py:2966-2977 and run_suite.refuse_missing_executor",
    "B6 F-2(a): a factory_fixable finding left after the conductor turn holds S4 (stage_done.py:482-484); no transition back to the card stated"
  ],
  "fixes": [
    "M1 name Driver.no_move with site_fallback and conductor called (not call False, not EXCLUDED_KINDS); name the r9 test file test_no_move_seam_sites.py",
    "M2 census owner data for s0_rest, check_s5_executor, stand_check; say which units have no census row",
    "M3 test_readiness.py row of r2 in stream 1 vs stream 3 owns; correct OF5-5 owns cell before stream 6",
    "M4 E-7 role text has no owner stream",
    "M5 measure F-3 premise (manual lane accepts a case with no capture surface) before stream 1 item 4; cite P19 step 3 and the EP1-41f reversal",
    "M6 r3 sentence 'asked before tests run' verified against env_probe exit for URL-less rows; name pins test_readiness.py:873-874,917",
    "M7 replace r1 witness keys K3 and K4 that already exist in p1/p2",
    "M8 name axis 38 driver-exits census, A27 NO_MOVE_BASELINE and driver-layers rows in streams 3, 5a, 5b, 6"
  ],
  "class_completeness": "Not complete. r8 siblings gate_preflight check_s5_toolchain not_started branch and run_suite refuse_missing_executor; r11 class carrier B-006 (S6-S8 manual route); Q-4 belongs to U7 with same-function siblings (tests_root silent return 2938, collect timeout card 2978) and check_s5_dependencies silent unknown; PYTEST_TOKENS one-road exclusion is absent from the t-2046 census and needs a node with an owner (U8). Map axes walked: 5, 18, 34, 38.",
  "trail": {
    "read": [
      "docs/tasks/specs/20261117-u7-pass-without-stuck-spec.md",
      "docs/tasks/specs/20261117-u7-pass-without-stuck-brief.md",
      "ai-packages/qa-factory/scripts/surfaces.py",
      "ai-packages/qa-factory/scripts/readiness.py",
      "ai-packages/qa-factory/scripts/tests/test_readiness.py",
      "ai-packages/qa-factory/scripts/gate_preflight.py",
      "ai-packages/qa-factory/scripts/driver_s0.py",
      "ai-packages/qa-factory/scripts/driver_conductor.py",
      "ai-packages/qa-factory/scripts/driver_machine.py",
      "ai-packages/qa-factory/scripts/driver_stage_s5.py",
      "ai-packages/qa-factory/scripts/driver_stage_s6.py",
      "ai-packages/qa-factory/scripts/driver_stage_s7.py",
      "ai-packages/qa-factory/scripts/controller.py",
      "ai-packages/qa-factory/scripts/stage_done.py",
      "ai-packages/qa-factory/scripts/driver_gates.py",
      "ai-packages/qa-factory/scripts/planning_contract.py",
      "ai-packages/qa-factory/scripts/run_suite.py",
      "ai-packages/qa-factory/scripts/probe_by_code.py",
      "ai-packages/qa-factory/scripts/driver_stage_build.py",
      "ai-packages/qa-factory/references/stages.json",
      "ai-packages/qa-factory/references/conductor-actions.json",
      "ai-packages/qa-factory/references/null-outcomes.json",
      "ai-packages/qa-factory/scripts/tests/test-layers.json",
      "ai-packages/qa-factory/scripts/tests/fixtures/judgment-census.json",
      "docs/SIBLING_MAP.md",
      "plans/BACKLOG.md",
      "plans/piles/conductor/batch-3-vhodyashchie.md"
    ],
    "reruns": [
      {"command": "python -B tools/owns_readers.py --repo C:/QAFactory/forge-repo --paths <13 touched files> --names <10 names>", "result": "readers: 724 outside owns, 53 lines below -- base origin/main b4eb74df"},
      {"command": "python -B -c <test-layers.json lookup of named test files>", "result": "test_surfaces.py quarantine; test_story_run_gate_repair.py quarantine; test_mobile_road.py quarantine; others keep"},
      {"command": "python -B -c <judgment-census owner/class counter>", "result": "check_s5_executor and stand_check rows owner data class shape; zero rows with owner judgment and class shape"},
      {"command": "Grep PYTEST_TOKENS|check_s5_toolchain|collect_base -i in t-2046 census; control pytest -i", "result": "0 hits; control 19 hits"}
    ]
  }
}
```
