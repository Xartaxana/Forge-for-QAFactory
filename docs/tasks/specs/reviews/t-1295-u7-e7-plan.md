# t-1295 - plan critic of U7 / E7 (another instance, asked once when needed), node universality/1/U1-11

Spec: `docs/tasks/specs/20261118-u7-e7-another-instance-spec.md`. Base: the dispatch started at origin/main 766fad1a; during
the review main moved to e2ddb6d7 (1b `e0503f09` and its fix `d4969e11` "t-1292 F1" merged: `manual_evidence.py` +31,
`test_manual_evidence.py` +33, `architecture.md` axis-2 cell in place). Code below was read on the working tree = origin/main
e2ddb6d7 (status clean for `ai-packages/qa-factory/scripts/`).

**Verdict: NEEDS WORK = accept with amendments.** N1-N5 block dispatch until they are in the spec header; N6-N11 are
fix-before-dispatch; Q1-Q3 are forks for the Lead. JSON `blocker` per critic rule 23 (findings block the dispatch, failure_class: spec).
The decision to accept stays with the Lead (rule 6).

## Keys

**P1 - FINDING (blocks; §0 F-N1, §2, §3 E7-3 non-goals).** Exits of a need record on a prepared case, as the person sees them:
- no stand / no-trace story: asked, answer held for the story (`extra_instance_held`) - told. OK.
- `stop`: held question, rerun asks with "You answered `stop` earlier" - told. OK.
- `by hand` / known "no": the analyst still judges it (`s7_pretriage._why_not`: an unprepared row is never code-triaged; `contract.triage_targets`
  counts `unprepared` as a target) - no quiet disappearance at S7. But at delivery `check_delivery.unprepared_records` (check_delivery.py:1914-1918)
  says "the factory could not prepare this check ..." for EVERY unprepared walk - false for a case the factory prepared. **N3.**
- known "yes" + rework refused, re-walked and still owed, a need newer than the yes: one printed line, then the same false delivery text;
  the person who said yes is never told the factory did not start it. **N3.**
- registry unreadable: asks (toward asking). OK.
- A runner using `--needs` to hide a hard case: with a standing "no", a prepared-case `inconclusive` becomes an unprepared walk; with
  7c (`current_unprepared`, r4 §5) that is `after_checks` and the coverage gap is excused, instead of today's `no`. The analyst still
  triages it, so it is not silent, but the delivery verdict is softened on the runner's word. **Q1.**
- The case's reason has no carrier on a walked case. **N4** (see P5).
- E5.8 restated (F-N1 a) leaves the validator honouring a need record with no request check at all. **N6.**

**P2 - FINDING (blocks; §2 position, INV ii).** Read `driver_stage_s7.py::stage_S7` 51-149. INV i holds: `s7_closed_by_scribe` (61),
`consumer_settled` (64) and the entry Refusal of `failures_to_triage` (22) all come before the proposed spot. INV iv: `seam_rework_step`
runs earlier in each loop turn (driver_machine.py:608, 650), so a pending `seam_rework` never reaches stage_S7; the check in the step
is harmless. INV ii fails in one class: a need record written by a runner round started INSIDE an open S7 after the triage
(`s7_rejudge_round` -> `rework("S6","qa-runner")`; a person-chosen rework through `seam_rework_step`; the comment at 67-70 says a
person-word rework of an earlier stage does not stale an open S7). Then `analyst_done` stays True; an unwalked need record has no
`attempt_id` and per `contract.triage_failures` "a failure with no attempt answers any row's attempt", so an old triage row naming the
case binds it, `s7_fresh` is True, and the run goes to `s7_repairs` -> `s7_close` without the question. The freshness re-triage path
and an S6 consumer reject (superseded analyst -> `analyst_done` False) are covered. No S6 close site settles a need: `manual_close`
runs `finalize_task` (driver_stage_s6.py:1079), which keeps the record as an unprepared row. **N2.**

**P3 - FINDING (blocks; §2 step 4).** `Driver.rework` (driver_dispatch.py:2849-2901) allows the call: `question_answer` is in
`REPAIR_CAUSES` (controller.py:280) and the controller does not restrict causes by stage. But "the shape of `s7_rejudge_round`" does
not carry over. `s7_rejudge_round` runs from `s7_repairs`, after `consumer_settled(..., ran=True)` closed S6, so S6 is `completed` and
`set_stage` is monotonic (its docstring). The trigger runs BEFORE the analyst. At that point S6 normally AWAITS its consumer
(`stages.json` S6 `acceptance_by: qa-failure-analyst`; `awaiting` non-empty), and `controller.next` returns S7 only while
`awaits_acceptance("S6")` holds (controller.py:9364-9368). A rework with `complete=False` leaves a newer accepted runner dispatch
with no awaits word, so `next` = `prepare_stage S6`, and `stage_S6` re-plans the manual half instead of coming back to S7. There
are three more gaps. "manual lines" is not a defined thing: the non-walking extra in `run_manual_block` (driver_stage_s6.py:1954-1964)
carries the `finalize_task.py` line, and without it `run-report.json` (which `unprepared_rows` and the triage read) stays stale. On
the walk road a rework dispatch has no `state/walks/<id>.json`, so `run_role` opens no walk session (driver_dispatch.py:700-706). The
counter `extra_instance_rewalk[case]` is per case, not "per case per answer". Loops: rework refused, the need written again and the
counter all end in triage, so there is no automatic loop. With a per-case key, a revoke followed by a new yes never re-walks. **N1, N7.**

**P4 - FINDING (blocks; §3 TEMPORAL).** The intermediate states:
- E7-1 alone: a CLI verb and a conductor row, no reader. Coherent. `needed_by` names functions that are not there yet; nothing checks
  them (the grep of `needed_by` over scripts found only test_config_migration.py:400-407, which checks the list type).
- E7-1 + E7-3: no page names `--needs`, so no records are written. Coherent, EXCEPT for the told-before-work ratchet.
  `tests/fixtures/told-ratchet.json` pins `manual_evidence.py::write_unprepared` at `bare: 4` (line 347; read by test_stage_joints.py
  K4/K6, slow). E7-3's new `ValueError` for a need outside the set is a fifth bare site in a role-reachable unit. The runner is told
  about it only by E7-2, which merges later, so main is red between the merges and E7-3 does not own the ratchet. **N5.**
- 1b: merged during this review (e2ddb6d7). Its F1 makes a `hands: none` case `unprepared` (prepare_request -> `Refused(walkable=True)`).
  E7-3's "marker kept, need added" meets it correctly. The header's "after 1b merges" should now name t-1294 if that round is still open. **N11.**
- 7c: both nodes edit `manual_evidence.py`, in different functions (textual merge only). The meaning changes: a need record walked=True
  passes 7c's `current_unprepared` and becomes `unprepared_walk`/`after_checks`; before 7c it keeps `chain_broken` (the r4 §5 item 6
  docstring), i.e. `no`. The spec states neither world, and neither node owns the delivery words for a need record. **N3, Q1.**

**P5 - FINDING (fix before dispatch; §3 edges).** Missing edges:
- (a) The lead's size: "several cases -> ONE question listing them all", each with quoted runner words, and no cap.
- (b) The runner words go into a person-facing lead with no secret masking. The walk-supply line masks with `MC.secret_pattern_hit`
  (driver_stage_s6.py:1944-1950).
- (c) **The reason carrier (blocks, N4).** `write_unprepared` refuses `--not-walked` when the recorder holds steps ("leave --not-walked
  out"), and the spec's `record_from_walk` drops `limitation` when the case was walked. A prepared case is usually walked, so on both roads
  "what you would start and why" (E7-2 page) has no field, and the lead has nothing to quote.
- (d) Outside-input battery, AT and BEYOND each limit: a huge words file, non-UTF-8 or BOM, `--stand ""`, a stand with spaces or
  non-ASCII, `--allowed YES`; a verdict `needs` that is null, a list or a number; `needs` on an item whose request is factory-unprepared.
- (e) Moments equal -> owed or not.
- (f) `walk_rule_errors` (manual_evidence.py) still asks `_result_errors` of a prepared case. Say that a `needs` verdict is checked
  against `write_unprepared`'s rules while the session lives (the one-function rule of t-2016 F2).
**N4, N8.**

**P6 - FINDING (fix before dispatch; §3 DoD/tests).** Checked against `slow_tests.json` `files` (dict of 152) and the test-layers
`canon_only` globs: slow = test_brief_pack, test_no_move_seam_sites, test_config_migration, test_conductor_doors, test_check_delivery;
no file matches `canon_only`. Not slow, kept: test_project_knowledge, test_role_rules, test_role_load, test_manual_evidence,
test_walk_record, test_state_exits. All three DoD lines pass `_dod_run_check` (tools/dispatch_manifest.py:990-1037). A `file.py::name`
token does not end in `.py` and is not counted; no `--witness-for`.
- The "narrow call (import, call)" is not an exact command (CLAUDE.md rule 11: the exact verification run).
- §3's "test_state_exits.py ... does not [fit the cap]" miscounts. E7-3 names 2 whole files, the cap is 3 (`MAX_DOD_TEST_FILES`), and
  E7-1 also edits state-exits.md.
- Rows: strongest first, behaviours, plausible within the volume budget. Missing: a seam row for the awaiting world (N1), one for the
  in-S7 rework need (N2), and the walked-reason row (N4). **N9.**

**P7 - FINDING (blocks via N3/N5).** The given readers block, line by line, is in Q13(d) below. Readers whose behaviour changes and
that no node owns:
- `check_delivery.unprepared_records`: false words (N3).
- `told-ratchet.json` (N5).
- `judgment-census.json` rows `write_unprepared` (xref, line 697), `_validate_unprepared`, `verdict_problems`: canon judged; the spec's
  "builder stops with a question" is acceptable.
- `ledger.unprepared_walks` gains `need`/`ended_at` keys. No schema names it (Grep `unprepared_walks` over non-.py files: CHANGELOG
  only). The readers compare cases or single fields (test_ledger.py:1429-1442, test_manual_projection.py:166, test_unprepared_outcome.py:181-199).
- test_manual_evidence.py:1177 compares whole rows, but only for records without a need: unchanged.
- `test_walk_account.py:180-183` pins `walk_supply < at < open_work` only. A branch after `open_work` keeps it.
- test-layers `named_by` `architecture.md:256` / `state-exits.md:69`: the axis 7 row is line 53 (edited in place). "The run's own
  records" (104) and "What the driver keeps" (185) are below 69, so appends keep both pins.

**P8 - FINDING (fork Q2; §6).** The §6 reason is only half true. The field merged without the trigger can be written only by a runner
told about `--needs`, and E7-2 (the page) merges last by the spec's own order. So the invariant is held by order, not by node size.
A split keeps it: E7-3a = record field on both roads + validator + walk_session (+ its tests, the state-exits record row); E7-3b = the
trigger, the question, the registrations. Order: E7-1 -> 3a -> 3b -> E7-2. The cost is a window in which F-N1 (a) lifts E5.8 with no
question, for a runner that improvises the flag. **Q2.**

**P9 - FINDING (fix before dispatch; §2 the question).** The lead names the stand and the cases, says the answer is kept, and names
`ask again`, which conductor-actions row 30 already maps to revoke. It has no platform word. Gaps:
- The doors' `says` texts are not written. `by hand` as a standing "no" must be said in the option itself.
- The printed lines are not written: rework refused, unparseable moment, held answer.
- For walked cases the lead has no runner words (N4). **N10.**

## Amendments (paste into the spec header)

- **N1 (§2 step 4; blocks).** Name the world: when `awaiting` (S6 awaits its consumer), the re-walk passes
  `complete=self.consumer_awaits("S6", True)`; when S6 is completed, `complete=False`. INVARIANT: after the re-walk returns,
  `controller.next` is S7 and no S6 manual block is re-planned. The extra lines are named: the two non-walking lines of
  `run_manual_block` (incl. "then `finalize_task.py <task root>`") plus the authorization line. The walk road: either `walk_before`
  for the block before the rework, or an explicit fork. Add a seam row for the awaiting world.
- **N2 (§2 position; blocks).** The step runs on EVERY S7 entry, right before `if not analyst_done:` (after the freshness block).
  INVARIANT: no S7 close (`s7.no_failures`, `s7.pretriaged`, `s7_close`), no pre-triage row and no analyst dispatch over a need with
  no answer; with a known answer it is a no-op. Add a seam row: need written by an S6 rework inside open S7 -> question.
- **N3 (§3 E7-3 owns or 7c; blocks).** `check_delivery.unprepared_records` gets a branch for a row with `need`: "the factory prepared
  this check, but it needs another instance of the stand or device, which the factory did not start: <reason>" (no "could not prepare").
  Both worlds (before and after 7c) are stated. Owner: Q3.
- **N4 (§3 E7-3 Work 1, §2 lead, E7-2 page; blocks).** A carrier for "what you would start and why": CLI `--need-why "<words>"`,
  required with `--needs`, non-blank, cut at `NOT_WALKED_MAX` with "…", stored as `unprepared.need_why` whether walked or not. On the
  walk road the verdict's `limitation` goes there. `unprepared_rows` carries it and the lead quotes it. E7-2's page names the flag.
- **N5 (§3 TEMPORAL; blocks).** `tests/fixtures/told-ratchet.json` joins E7-3 owns, with each raise named (unit, old -> new, reason).
  Alternatively, the need check lives only in argparse `choices` plus the verdict problem, and no new bare site is added. Say which,
  and that main is green on test_stage_joints K4/K6 between E7-3 and E7-2.
- **N6 (§3 E7-3 Work 2).** `_validate_unprepared` honours a need record without a marker only when `request.json` exists, is not
  `refused`, and `obligation_ids` equal the request's. Otherwise "unprepared marker without an unprepared request". Today the
  obligation check runs only `if request:` (coverage_contract.py:764).
- **N7 (§2 step 4).** Key `extra_instance_rewalk["<case>|<PK id or held at>"]` (one re-walk per case per answer); equal moments ->
  not owed.
- **N8 (§3 E7-1, E7-3 edges).** The lead's cap, e.g. the first 10 cases and then "and K more", or name the human_text limit.
  Runner words in the lead are masked through `MC.secret_pattern_hit` and cut. Battery rows AT and BEYOND each limit, per P5 (d).
  `needs` checked against `write_unprepared`'s rules while the walk session lives.
- **N9 (§3 DoD).** Narrow calls as exact commands, e.g. `python -B -c "import sys; sys.path.insert(0, r'C:/.../scripts/tests'); import
  test_no_move_seam_sites as t; t.e7_extra_instance_trigger()"`. `test_state_exits.py` is run whole in E7-1 and E7-3 (E7-3: 3 files =
  the cap).
- **N10 (§2 the question).** Write the doors' `says`. `start it`: "the factory may start another instance of the stand or device on
  `<stand>` whenever a case needs one, now and in later stories; the cases above are walked again now". `by hand`: "the factory never
  starts one on `<stand>`; these cases and later ones like them are left for you to check and the report lists them; say `ask again`
  to change it". Also write the three printed lines.
- **N11 (header).** "after 1b merges" -> 1b and t-1292 F1 merged at e2ddb6d7; name t-1294 if it is still open. §5 line numbers in
  `manual_evidence.py` moved by about +27. Re-run `owns_readers.py` on the new base.

## Questions (forks for the Lead)

- **Q1** The delivery verdict of a need record once 7c is in: (a) `after_checks` for every need record, with the N3 text; (b) 7c's
  `current_unprepared` excludes need records under a "yes" (the runner failed, or the re-walk was refused), which stay `no`.
- **Q2** E7-3: (a) one node, as drafted; (b) split 3a/3b as in P8, with `--needs` kept out of the help text until 3b.
- **Q3** The owner of N3: (a) E7-3 (adds `check_delivery.py`; `test_check_delivery.py` is slow -> a narrow call); (b) 7c (it already
  owns that file); (c) a node after both.

## Plan-gate questions (rule 24)

- Q13(a) EDGES: findings P5, N1 (temporal awaiting), N5. Q13(b) MEANING: "unprepared walk" means "factory could not prepare" at delivery
  but now also "prepared, needs an instance" - the contradiction is N3. Q13(c) PREMISES: the premise re-run is "the shape of
  `s7_rejudge_round`" (it does not hold in the awaiting world, N1). "`test_state_exits` does not fit the DoD cap" does not reproduce (P6).
  The `write_unprepared` refusal on a prepared case reproduces (manual_evidence.py write_unprepared).
- Q13(d) READERS (block t-1291, base 766fad1a):
  - slow test lines (test_audit_rules, test_brief_pack, test_conductor_doors, test_infra_failure_texts, test_no_move_seam_n2b_n15,
    test_person_words, test_s7_investigation_replay, test_story_run_* x9, test_story_sides): judged by the batch canon.
  - take_answer names in test_driver_stop_record, test_first_look_code_look, test_first_look_step, test_human_questions,
    test_walk_account, test_walk_supply, tools/test_dispatch_gate, tools/test_dispatch_manifest, tools/test_piles: unchanged (a new
    `elif` branch after `open_work`, the signature is the same).
  - test_manual_evidence: owned by E7-3.
  - test_validator_class (verdict_problems): unchanged for verdicts with no `needs`.
  - test_walk_lanes (record_from_walk): unchanged signature.
  - test_walk_record: owned.
  - artifact-writers.json (record_from_walk): unchanged, write_unprepared is already its callee.
  - null-outcomes.json (stage_S7): not checked: the E7-3 builder confirms.
  - driver-layers.json: owned.
  - judgment-census.json: canon judges; the builder stops with a question.
  - told-ratchet.json: N5.
  - The 23 "more" lines: interface kept, except `check_delivery` behind `unprepared_rows` (N3).
  - miss 3: `NO_MOVE_BASELINE_MAX` has no literal pin (test_audit_rules.py:1024, 1075 compute it from the sum).
  - miss 6: base 766fad1a is origin/main: NO (now e2ddb6d7; the delta touches E7-3's `manual_evidence.py` and `test_manual_evidence.py`,
    and E7-1's `architecture.md`).
  - misses 1, 2, 4, 5: not run by me (the Lead's block names them; no `--witness-for` run).
- Q13(e) FORKS: F-N1 (a) is consistent with the owner's word only with N3 + N6. F-N2 (a) is consistent ("ask once"). F-N3 (a) is
  consistent with P31 provided N1's walk-road re-walk is stated.
- Q4 CLASS: siblings of the defect class "unprepared = factory could not prepare" are the readers that word or decide on `unprepared`:
  `check_delivery.unprepared_records` (N3), `coverage_contract` gap text `not checked by hand: unprepared - <reason>`
  (coverage_contract.py:705; reads NEED_REASON, acceptable), `s7_pretriage._why_not` (fine). Named with files; no others found beyond
  the digest's q4f list.
- Q6 DUPLICATION: the stand of a story has two readers: `stand_gaps.stand_name` (trigger, CLI `_story_stand`) and
  `brief_pack._stand_pick` (E7-2 line, the lessons line). They agree on a named stand and on a single row, and both read "none" when
  nothing is chosen. A disagreement errs toward asking. Not a blocker; name it in E7-2's siblings. The re-walk "manual lines" must
  reuse `run_manual_block`'s lines, not a copy (N1).
- Q12 ONE ROAD: the walk road gets `needs` (F-N3 a), but the re-walk on the walk road has no session (N1). Until N1 says so, walk-road
  projects get the question and then a re-walk that cannot walk. Fix it in this round (N1). No language or project branch otherwise
  (none found: the spec text was read for platform or language words).
- VARIETY: an unknown stand, registry or answer -> asks once at S7; no silent default, no block. The `awaiting` world (every story with a
  runner) is broken by step 4 as drafted (N1): the stage would re-plan S6. Blocks until N1.

## Spot-checks (claims with carriers)

- "No reader checks `needed_by` names exist": Grep `needed_by` over `scripts/` -> env_probe/gate_preflight/readiness (a different
  `needed_by`), test_config_migration.py:400,407 (positive control: the pattern finds the known test).
- `test_state_exits.py` is not slow: the slow-list check found `test_brief_pack.py` with the same call (positive control).
- No schema for `unprepared_walks`: Grep over non-.py files of the package -> CHANGELOG.md:69 only (the control is the same Grep with
  `*.py` -> ledger.py:1668, check_delivery.py:1909).

## Trail

- Read: the spec (whole); digest t-1273 (whole); readers t-1291 (whole); r4 §5-§6 (351-434).
- Read on the tree at e2ddb6d7: driver_stage_s7.py 1-170, 340-520, 990-1089; driver_dispatch.py 619-718, 2849-2901;
  driver_stage_s6.py 163-183, 433-496, 1895-1969; driver_machine.py 3375-3474 + Grep; controller.py 255-294, 9340-9380 + Grep;
  acceptance.py 1433-1528; stages.json 205-254; manual_evidence.py 1236-1275, 1495-1634 + `git show` d4969e11; coverage_contract.py
  650-790; contract.py 4595-4724; s7_pretriage.py 140-189; check_delivery.py 1898-1922; walk_session.py 632-801, 1680-1722;
  stand_gaps.py 148-159; project_knowledge.py 459-473, 1034-1098; brief_pack.py 2734-2746; question-prices.json (via python);
  conductor-actions.json 29-31; state-exits.md headings and lines 69, 167; architecture.md 53, 256; test-layers.json keep, quarantine
  and canon_only; slow_tests.json; tools/dispatch_manifest.py 177, 985-1037; told-ratchet.json 1-20, 347-350;
  test_stage_joints.py Grep; test_walk_account.py Grep; audit_factory.py Grep; docs/TESTING.md 205-249.
- Commands:
  - `git -C ... rev-parse HEAD origin/main` -> 766fad1a (start), then e2ddb6d7 x2.
  - `git -C ... log --oneline 766fad1a..e2ddb6d7` -> 5 commits (1b, t-1292 F1, journal).
  - `python -B tools/architecture_index.py --check` -> "architecture index: up to date (29 invariants, 2682 bytes)", exit=0.

```json
{
  "verdict": "blocker",
  "failure_class": "spec",
  "blockers": [
    "N1 (spec section 2 step 4): the S7->S6 re-walk with complete=False in the awaiting world (S6 acceptance_by the analyst) leaves controller.next at prepare_stage S6 (controller.py:9364-9368); manual lines undefined (no finalize line); walk road has no session for a rework dispatch (driver_dispatch.py:700-706)",
    "N2 (section 2 position): a need record written by an S6 rework inside an open S7 after triage is bound by an old triage row (no attempt) -> s7_fresh True -> s7_close without the question; run the step on every S7 entry before if not analyst_done",
    "N3 (section 3 E7-3 or 7c): check_delivery.unprepared_records says the factory could not prepare this check for a need record on a prepared case (check_delivery.py:1914-1918); no node owns the words",
    "N4 (section 3 E7-3 Work 1, section 2 lead): no carrier for what the runner would start and why on a walked case: write_unprepared refuses --not-walked when walked, record_from_walk drops limitation",
    "N5 (section 3 TEMPORAL): told-ratchet.json write_unprepared bare 4 (test_stage_joints K4); E7-3 adds a bare refusal told only by E7-2 merged later; ratchet not owned"
  ],
  "fixes": [
    "N1 complete=consumer_awaits(S6, True) when awaiting; reuse run_manual_block lines incl. finalize_task; walk road stated; seam row for the awaiting world",
    "N2 trigger before if not analyst_done with the stated close invariant; seam row",
    "N3 need branch in unprepared_records words, both worlds of 7c, owner per Q3",
    "N4 --need-why field stored as unprepared.need_why on both roads, quoted by the lead",
    "N5 told-ratchet.json in E7-3 owns with the raise named, or no new bare site",
    "N6 validator honours a markerless need record only on a prepared, non-refused request with equal obligation ids",
    "N7 rewalk key per case per answer; equal moments not owed",
    "N8 lead cap, secret masking, adversarial battery AT and BEYOND each limit",
    "N9 exact narrow-call commands; test_state_exits.py whole in E7-1 and E7-3 DoD",
    "N10 door says texts and printed lines written out",
    "N11 order line updated for 1b merged at e2ddb6d7 and t-1294; rerun owns_readers on the new base"
  ],
  "class_completeness": "Class: readers that read unprepared as factory could not prepare. check_delivery.unprepared_records is wrong for need records (N3); coverage_contract gap text carries the reason and is acceptable; s7_pretriage._why_not is correct. The class of S7 entries that skip the trigger: the in-S7 S6 rework is open (N2); the scribe, consumer and entry-refusal exits are covered. Walk road re-walk is a sibling of N1.",
  "trail": {
    "read": [
      "docs/tasks/specs/20261118-u7-e7-another-instance-spec.md",
      "docs/tasks/specs/reports/t-1273-e7-trigger-site-digest.md",
      "docs/tasks/specs/reports/t-1291-e7-owns-readers.txt",
      "docs/tasks/specs/20261117-u7-pass-without-stuck-spec-r4-7b-7c-e7.md:351-434",
      "ai-packages/qa-factory/scripts/driver_stage_s7.py:1-170,340-520,990-1089",
      "ai-packages/qa-factory/scripts/driver_dispatch.py:619-718,2849-2901",
      "ai-packages/qa-factory/scripts/driver_stage_s6.py:163-183,433-496,1895-1969",
      "ai-packages/qa-factory/scripts/driver_machine.py:3375-3474",
      "ai-packages/qa-factory/scripts/controller.py:255-294,9340-9380",
      "ai-packages/qa-factory/scripts/acceptance.py:1433-1528",
      "ai-packages/qa-factory/references/stages.json:205-254",
      "ai-packages/qa-factory/scripts/manual_evidence.py:1236-1275,1495-1634",
      "ai-packages/qa-factory/scripts/coverage_contract.py:650-790",
      "ai-packages/qa-factory/scripts/contract.py:4595-4724",
      "ai-packages/qa-factory/scripts/s7_pretriage.py:140-189",
      "ai-packages/qa-factory/scripts/check_delivery.py:1898-1922",
      "ai-packages/qa-factory/scripts/walk_session.py:632-801,1680-1722",
      "ai-packages/qa-factory/scripts/stand_gaps.py:148-159",
      "ai-packages/qa-factory/scripts/project_knowledge.py:459-473,1034-1098",
      "ai-packages/qa-factory/scripts/tests/fixtures/told-ratchet.json:1-20,347-350",
      "tools/dispatch_manifest.py:177,985-1037",
      "docs/TESTING.md:205-249"
    ],
    "reruns": [
      {"command": "git -C C:/QAFactory/forge-repo rev-parse HEAD origin/main", "result": "766fad1a at start; e2ddb6d7 later (1b and t-1292 F1 merged during review)"},
      {"command": "python -B C:/QAFactory/forge-repo/tools/architecture_index.py --check", "result": "architecture index: up to date (29 invariants, 2682 bytes); exit=0"},
      {"command": "python slow_tests.json / test-layers canon_only membership of the named test files", "result": "slow: test_brief_pack, test_no_move_seam_sites, test_config_migration, test_conductor_doors, test_check_delivery; canon_only: none; all keep"}
    ]
  }
}
```
