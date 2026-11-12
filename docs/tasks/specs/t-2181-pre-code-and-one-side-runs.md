# t-2181 — One architecture for runs without code, with one side, and "as before" (revision 3)

Status: revision 3 by the designer (fix round on the critic's verdict t-2186,
`docs/tasks/specs/reviews/20261110-t-2181-plan-critic.md`). One text: the owner's Revision 2 is merged into §1–§8 and no
longer stands as an overlay. New forks are in §6 (F-14..F-18) and are NOT decided; the spec is executable by their
recommendations. Package paths are relative to `ai-packages/qa-factory/` in the worktree `D:/ws1/wt-fbfix`
(branch fb-fix) unless absolute. Every `path:line` below was re-read on 10.11.2026 (reading trail at the end).

**Line numbers of `scripts/controller.py` move today.** A first read of the file (this session, 10.11.2026) found
`build_rework_request` at :3450 and `_next_action_for_state` at :8351, as the verdict cites; a second read an hour later
found them at :3477 and :8459 (another session is editing the file in the same worktree). This spec cites
`controller.py` by FUNCTION NAME first and gives the line of the second read; a builder locates by name.

## Decisions record (short; who decided what)

- The owner, 10.11.2026: "Write ONE architecture for a factory run without code, and for using mocks even when code
  exists but only for one side ... a coherent solution, not different implementations in different places. Make a plan
  for bringing it into the factory." And: "if development takes 3 days, one run is impossible".
- Kept owner decisions: (D1) no locator contract for developers; (D2) a pre-code story carries NO "requirement not met"
  bug — a line "awaiting code" instead; (D3) in "as before" mode gate A shows only differences and gaps; (D4) S-a, S-b,
  S-c are taken together.
- The owner, 10.11.2026 15:18, on the forks: F-1 — "This must be kept in the knowledge store, a neighbouring session
  designed it today": the standing facts about sides live in the project knowledge registry of spec t-2142
  (`D:/ws1/wt-fbfix\docs\tasks\specs\t-2142-project-knowledge-phase0.md`), not in new `config.json` keys.
  "The rest by the recommendations": F-7, F-10, F-11, F-12, F-13 decided by the owner as recommended.
- The Lead, 10.11.2026: F-2, F-3, F-4, F-5, F-6, F-8, F-9 taken as recommended (technical; the owner may reverse).
- The Lead, 10.11.2026, rulings on verdict t-2186: all B1–B7 and S1–S18 accepted; B3's position (after
  returned/stopped, before the `unlaunched` relaunch and the stage loop) with its positional invariant; B2 covers every
  proof route; B4 carrier = the projected awaiting record with a terminal `stopped` mark; K9 mismatches are fixed by
  what PC-1b adds inside `project_knowledge.py`, with lines to agree with the project-knowledge session; PC-1 split into
  PC-1a / PC-1b with a first slice that proves S-a before the registry chain lands.

## Verdict t-2186 → revision 3

| finding | where changed | what changed |
|---|---|---|
| B1 | §2.3 rule, §1.3 C9 + error directions, PC-5 | resolved `about` = `about` if non-empty, else the keys of `tests[].sides` UNION every side the proof stamp recorded non-real; lookup needs `real` in BOTH the test's declaration and the stamp, a missing key is not real; an empty resolved `about` can prove only when the stamp holds no non-real side. Test `test_sides_ledger.py::empty_sides_no_about_on_stand_substitute_is_on_substitute` |
| B2 | §2.3, §4, PC-5a, PC-5, fork F-14 | one rule for every proof route: the sides a proof met are stamped by code on its EXECUTION BLOCK (run block and manual block), carried by `finalize_task.reduce` onto the report row, read by one ledger branch; a walk carries the runner's `about`. Tests `test_proof_stamp.py::manual_block_is_stamped`, `test_sides_ledger.py::manual_agent_green_on_stand_substitute_is_on_substitute` |
| B3 | §2.4, §3.1 step 6, §5 E-A6, PC-6 | the hold branch of `_next_action_for_state` sits after returned/stopped and before `unlaunched` and the stage loop; positional invariant stated; rework of S6–S9 refused while held; stage_guard rule `rule_awaiting_code`. Tests `test_awaiting_state.py::never_started_s6_rework_is_not_relaunched_while_awaiting`, `::rework_s6_refused_while_awaiting`, `test_stage_guard.py::s6_role_refused_while_awaiting` |
| B4 | §2.4, §4, §5 E-W1, PC-6, PC-7, PC-5 | carrier `pipeline.awaiting.stopped {at, words}` (and the controller state it is projected from); every reader named with its "no further action" behaviour; way out: the person's rework of S0–S5 with words (`await_reopened`) or a relaunch with the code (`arrive`). Tests `test_awaiting_state.py::stop_waiting_is_terminal`, `::rework_with_words_reopens_stopped`, `test_check_delivery.py::stopped_story_reads_awaiting_implementation` |
| B5 | §2.4 row 3, §3.2 step 5, §5 E-V1, C6, PC-4, PC-5 | the bind round retracts (`retracted_unresolved`) every pending row whose instances all ran stamped real; C6 refuses a leftover; the false citation of `state-exits.md:75` corrected (the slice rule is `:81`). Tests `test_s5_precheck_sides.py::leftover_pending_row_after_real_runs_refused`, `test_sides_ledger.py::retracted_pending_row_the_run_decides` |
| B6 | §3.1 step 5, C14, PC-4 | `check_witness._all_pending` beside `_all_handed`: every test excused by `acceptance.pending_instances` needs no `run_witness` but needs the collect row. Tests `test_check_witness.py::all_pending_with_collect_accepted`, `::all_pending_without_collect_refused`, `::one_runnable_needs_run_witness` |
| B7 | §3.2, PC-6 | PC-6 owns `PURPOSES` (+`bind`, `reference_walk`) and `REPAIR_CAUSES` (+`source_arrived`, placed BEFORE `ticket_changed`), and names the reader each word selects; PC-6 precedes PC-7 and PC-9b, the senders |
| S1 | §2.1, PC-1b, "to agree" list | `record_problems` in PC-1b's function list: per-key value shape for the three side keys, words from `references/side-realities.json`; census class unchanged |
| S2 | §2.1, C2, PC-1b, "to agree" | an `exact` comparator registered in PC-1b; side names compared exactly everywhere |
| S3 | §2.1, PC-1b, "to agree" | a pure lister `project_knowledge.subjects(...)` applying the module's own precedence; `story_sides` never reimplements it |
| S4 | §2.1, §5 E-K1, PC-1b, "to agree" | side rows are written `state: known`; on a `no_trace` story the answer stays in `pipeline.sides` with a report line; PC-1b owns `guard_pre_tool.py` (`human_word_check`, `HUMAN_WORD_MSG`) and `test_guard_project_knowledge.py`; queue line |
| S5 | §3.1 step 1, §5 E-O2, fork F-17 | a new side name at launch is accepted and the `sides.deliverable` answer records it (writer 2); E-O2 refuses only a name that differs from a recorded one by case; `product` is implied when the story's sides (the registry's, the launch's and the person's answers merged) hold no real side of this team (PC2-7, t-043) |
| S6 | §1.1, §3.1 step 6, PC-1a (`parks_after_s5`) | one rule: exit (i) only for an `absent` deliverable side; a substituted side (deliverable or not) runs to the end with `on_substitute` and a "Left with you" item |
| S7 | §2.1 reader shape, §4 | `settles_by` in the `story_sides` return and in `pipeline.sides`; empty → "the real <side>" |
| S8 | §2.4, PC-6 | the doctor is `stage_guard.stories` (qa-doctor step 4); it and `archive_task.open_items` are owned by PC-6 with tests |
| S9 | §2.2, C3, C4, §5 E-P1/E-P2, PC-3, PC-4 | the home is found by its marker in `<file>`; `line` is a hint; `home_hash` is the hash of the marked line wherever it is |
| S10 | §1.3 C1/C6, PC-4 | family `sides` stays OUT of `PASSABLE`; only the C1 tag `sides-undeclared` and the C6 tag `provisional-open-on-real` join `WORD_PASSABLE_TAGS` |
| S11 | §3.2 position, §5 E-A2, PC-7 | the launch word is kept BEFORE the freshness look; the arrival is recorded after it; invariant extended. Test `test_story_run_arrival.py::branch_word_survives_changed_ticket_question` |
| S12 | §2.1, §2.3, §5 E-U1, PC-1b, PC-5a, PC-5 | an unreadable registry (or a malformed side row) at S0 records `pipeline.sides_unknown`; the stamp carries it; the ledger reads covered Thens `not_verified:sides_unknown` (kind `sides_unknown`, after_checks, owner factory) until a later read succeeds and the Thens are re-run |
| S13 | §2.1, §2.3, §5 E-T1, PC-2, PC-5a, PC-6, PC-8 | `pipeline.sides` and the proof stamp are written only on a story that has (or had) a non-real side, a reference or an unknown; the controller reads only `pipeline.sides` / its own awaiting state, never the registry; PC-8 attaches `role_load.py --all` before/after with the token delta; E-T1 states the charter cost |
| S14 | §1.3 C5, PC-4 | C5 is `acceptance.pending_instances`, a sibling of `blocked_instances`, read once by `s5_precheck`, `window_record` and `check_witness` |
| S15 | §3.1 exit (ii), PC-5 | `on_substitute` records go one per case with `tests`, `how`, `to_check` through the existing generic path; `build_left_items` keying untouched |
| S16 | §1–§8 whole | Revision 2 merged into the body; no body sentence keeps the old config-key carrier, the dropped interview topic, or the old migration test |
| S17 | §7 | PC-1 split into PC-1a (no registry) and PC-1b (after PK0-1, PK0-8); PC-7 → PC-5 dropped; first slice stated |
| S18 | §7 PC-10, fork F-15 | PC-10 adds the three side keys and `contract.story_sides` to axis 34 (landed by PK0-6); no new axis by recommendation |
| N1 | §7 queue lines | `design/state-exits.md: PC-3 → PC-6` |
| N2 | §7 queue lines | `judgment-census.json` and `brief_pack.py` cross-pile queue lines |
| N3 | PC-6, §8 | the new fast file is `test_awaiting_state.py` (no `test_controller_*` name; it calls the static branch and the projection, no controller loop) |
| N4 | §2.1 | one line: the reference stand's address follows `environments[]` wherever t-2142 node 3.6 moves it |
| N5 | §1.2 AR-3, PC-1b | PC-1b's `architecture:` line names the AR-3 text on main plus PK0-6 as pending |
| N6 | PC-4 | `check_sides` is called by the caller right after `check_manifest` returns (`s5_precheck.py:4045-4046`), not from inside it |

Verdict items not applied as written: B4's "retro allowed" on a stopped story — returned as fork F-18 (recommendation: no
retro; stage_guard rule 1 needs S8 done). S18's "a new axis only if the Lead wants one" — fork F-15. S5's choice — fork
F-17. B2's choice of carrier — fork F-14. No finding is left unaddressed.

---

## §1 Purpose, situations, and what the design touches

### 1.1 The three situations as one model

| situation | in the model | exit |
|---|---|---|
| S-a: the story's code does not exist yet | the side(s) the story changes are `absent`, and they are this story's deliverable | after S5: story state `awaiting_implementation`; relaunch with the change = arrival road |
| S-b: only one side exists (UI without backend, backend without UI; the standing UI-only team) | the missing side is `substituted` (a mock stands for it) or `absent`; `deliverable` says whose it is | an `absent` deliverable side → as S-a. A `substituted` side (deliverable or not) and an `absent` non-deliverable side → run to the end; Thens that cross a substitute read `on_substitute`, verdict `after_checks`, "Left with you" names the re-pass |
| S-c: "must work as before" on a new architecture | a side carries a `reference` (a stand where the old version runs); its reality is whatever it is (absent → also S-a, real → normal run) | the reference supplies user-level expected behaviour through a parity requirement; the reality of the side decides the exit exactly as above |

No situation has a private field, state or stop: S-a, S-b and S-c are combinations of two per-side attributes
(`reality`, `reference`) plus `deliverable`, read by one reader, producing one registry of assumptions (`provisional[]`),
one proof rule (a Then is proven only when every side it speaks about was real for the proof that covers it, whatever
route that proof took), one new story state with one entry condition (a deliverable side is `absent` after S5) and one
arrival road (a side became real). (K1)

### 1.2 Invariants touched (AR-n), how each is kept, the change check it demands (goes into the DoD of the nodes in §7)

| AR | how kept | change check written into the DoD |
|---|---|---|
| AR-1 closed variety is data | reality words (`real`/`absent`/`substituted`) live in `references/side-realities.json`, provisional kinds in `references/provisional-kinds.json`; no tuple of these words in code; the controller's new purpose and cause words join the existing closed literals `PURPOSES` / `REPAIR_CAUSES` (their existing home) | grep `scripts/` for the literal reality tuple with a positive control; `test_story_sides.py` reads the words only from the data file |
| AR-2 open variety is a role's | side NAMES are open (`ui`, `backend`, `mobile`, `payments-gw`…); code never lists them; which side a Then or a walk speaks about is the automator's / runner's judgment | no side name in code; a fixture with the side name `kiosk` passes every check |
| AR-3 project facts in config or the answer registry, default for every key | the standing side facts are rows of the t-2142 registry `records/project-knowledge.json` (keys `product.sides`, `environments.sides`, `environments.reference_for`); the default for every key is the reader's default (`{product: real, deliverable: true}`, no reference). PC-1a stores no project fact (story record only). Until PK0-6 lands the AR-3 text naming the registry, PC-1b's `architecture:` line names the AR-3 text on main plus "PK0-6 pending" (N5) | PC-1b: `test_story_sides.py` default with no registry; `test_project_knowledge.py` side rows |
| AR-6 an LLM agent is never a read route | the reference version is walked through the recorder (`walk_session.py`/`manual_capture.py`), which writes the evidence; snapshot items must cite captures | `reference_snapshot.py put` refuses an item with no capture and no old-test ref |
| AR-9 refusals name expectation and door | every new refusal (S5 `sides` family, the `_all_pending` witness rule, a test run on a reference env, rework of S6–S9 while held, the stage_guard hold rule, the registry value check, a launch name differing by case) names what it expected and a door | refusal registry + A24 rows in the same commit |
| AR-10 a check's requirement reaches the role first | the automator's brief carries the story's sides, the provisional kinds and the fields it must fill before S5 (`brief_pack.build`); the runner's S6 brief names the walk's `about` field when the story has a non-real side | `test_brief_pack.py`: the S5 brief names `tests[].sides`, `then_bindings[].about`, `provisional[]` only when the story has a non-real side |
| AR-11 only the tools needed | no tool added to the automator; the reference walk is done by the runner, which already holds the recorder commands (`references/role-commands.json:40-72`) | `role_load.py --all` before/after |
| AR-12 friction measured | phase-2 cost and the provisional share are measured (§8); PC-8 names the charter token delta | `code_friction` before/after for qa-automator, or "not measured" as an open item |
| AR-13 one reader per fact | `contract.story_sides()` the one reader of sides; `contract.parks_after_s5()` the one reader of "this story parks"; `contract.awaiting()` the one reader of the projected awaiting record (the controller reads its own state, as `closure_of` beside `story_closure`); `contract.manifest_provisional()` the one accessor of the registry of assumptions; `acceptance.pending_instances()` the one reader of the "cannot run" excuse; `project_knowledge.state()` / `subjects()` the only readers of the three registry keys | grep for `"sides"` / `"provisional"` / `"awaiting"` / `sides_met` reads outside the readers with a positive control; axis 34 membership (PC-10) |
| AR-14 one artifact, one writer | `provisional[]` only by the automator through `manifest_put.py --fragment`; `pipeline.sides` / `pipeline.sides_unknown` only through `stage_done.py --set` (driver, conductor, skill path); the registry rows only through `project_knowledge.record`; the proof stamp only by the block writers (`run_suite.build_run_block`, `manual_evidence.write_block`); the reference snapshot only by `reference_snapshot.py put` (runner) | `stages.json` output rows + writer rows in one commit |
| AR-16 one question form | the new questions (`not built yet`, `sides.deliverable`, `arrival.not_waiting`, `awaiting.stop`) are `question-prices.json` keys through `closed_question`, and pass `human_text.problems` | `test_human_reading.py` on the new texts |
| AR-17 one seam to the conductor | an arrival conflict code has no move for (an unreadable diff, a refused rework chain) goes to the conductor through the existing seam | no new conductor entry point |
| AR-19 stage twins change together | `s0.no_change` (`story_run.py:8299-8336`) and `s1.no_diff` (`story_run.py:2964-2976`) change in one commit; the S5 run excuse is read by `s5_precheck`, `window_record` and `check_witness` through ONE reader | axis 5 lookup named in the commit |
| AR-20 shrink-only ratchets | census counts may grow by the checks of 1.3; each raise named in the verdict | `test_judgment_census.py`; raised rows listed |
| AR-21 a stage's gathering travels whole | the reference snapshot is an S1 output carried into S2 (`stages.json` inputs); the provisional registry lives in the manifest every later stage reads; the proof stamp travels from the block to the report row | `index.yaml` handover rows |
| AR-22 every field has producer and reader | §4 table | `test_field_producers.py` |
| AR-23 every list declares its empty outcome | `provisional: []`, `pipeline.sides` absent = default, `about` absent = conservative, no stamp = no non-real side recorded, snapshot `items: []` + gap line | `references/null-outcomes.json` rows; `test_null_outcomes.py` |
| AR-25 every state has a way out | §2.4 table; `design/state-exits.md` rows | `test_state_exits.py` enumerates the new states |
| AR-26 requirements are the unit | the parity requirement is a register requirement (`parity: yes`, set by the tester); a snapshot item never becomes a requirement by itself | C7 refuses a `precedent reference:` Then whose case basis is not a parity requirement |
| AR-27 a finding reaches the report under its owner | `on_substitute` owner `environment`; `awaiting_implementation` owner `product`; `sides_unknown` owner `factory` | kinds file `owner` words tested |
| AR-28 an unknown never becomes a pass | `on_substitute` and `sides_unknown` are `after_checks`, never `passed`; an excused (pending) instance is never green; a missing `about` reads conservative; an awaiting or stopped story has no verdict and any reader that asks gets `no` | negative tests in `test_sides_ledger.py` |
| AR-29 code judges data | every new check is shape / xref / presence / safety (1.3); "which side a Then or a walk speaks about", "does this mock stand for that side", "are old locators portable", "which rows the diff affects" are role judgments accepted by a tier above | `judgment:` line per package commit; census rows |

FR touched: FR-4 (no silent pass: every excuse is declared; a person's word on the hold rule is journaled), FR-5 (S6
never requires code that cannot exist — the story parks instead), FR-7 (the awaiting packet is a report, not a
question; a relaunch without a flag re-prints and asks nothing), FR-8/FR-9 (`stop waiting` words reach their
executor; a source word survives a question asked in the same process), FR-12 (no phrase list: "as before" is read by
the tester and recorded as `parity: yes`), FR-13, FR-18 (a collect is not a run; a run on a substitute is not coverage
of the real side), FR-21 (a requirement the ARRIVED code lacks still blocks: a surviving `pending_implementation` row
whose instances did not run green on real sides keeps `no`), FR-23, FR-33 (live proofs §7), FR-34, FR-35 (new kinds
are separate words), FR-38, FR-40, FR-41, FR-49, FR-50/P5 + D-0043 (an unreachable reference is a gap line), FR-51/FR-55
(§8), FR-57, FR-58 (the reference is observed USER behaviour confirmed by the person, never old code), FR-59 (an
unreadable registry is `sides_unknown`, never `real`).

P touched: P2 (side names open), P4 (snapshot in YAML), P5/D-0043, P8 (a `no_trace` story writes no registry row), P13
(every new block passes on a person's word), P17, P19 rung 5, P20, P21 (third verdict for a substituted side), P22,
P24 style ("Left with you" re-pass items: one command, the stand requirement named), P26 (the reference walk and the
manual walk are an agent through the recorder; code stamps what the walk met), P27, P28 (unchanged).

### 1.3 Every check this spec adds or alters: owner served and census class (designer rule 1, AR-29)

| id | check | where | owner served | census class | blocks? |
|---|---|---|---|---|---|
| C1 | a test row of a story that has a non-real side carries `sides` (an explicit `{}` is legal; it is read conservatively, §2.3) | `s5_precheck` `check_sides`, family `sides` | data | shape | repair; passable by a person's word BY TAG `sides-undeclared` (`WORD_PASSABLE_TAGS`), never by family (S10) |
| C2 | every name in `tests[].sides` and `then_bindings[].about` is a side of the story by the reader, compared EXACTLY | `s5_precheck` `sides` | data | xref | repair |
| C3 | a `provisional[]` row: `kind` in the kinds file; `home.file` exists in the test repo AND holds the marker `qa-provisional: P-n` on some line; `settles_on` is a side of the story; every `dependents` entry is a `(case, then)` of `then_bindings` | `s5_precheck` `sides` | data | shape + xref | repair |
| C4 | every `qa-provisional: P-n` marker in the scope's test files has a row, and every open row's marker is present in its `home.file` (any line) | `s5_precheck` `sides` | data | xref | repair; after arrival a marker whose row's side is real is a finding ("forgotten substitute") |
| C5 | an instance is excused from `runs` / `run_witness` / probe ONLY when `acceptance.pending_instances` names it: a `pending_implementation` row names it in `instance_ids`, AND its `tests[].sides` names a side valued `absent`, AND the reader says that side is `absent` | `acceptance.pending_instances` (new sibling of `blocked_instances`), read by `s5_precheck` (beside `blocked`), `window_record` (probe owed), `check_witness._all_pending` | data | xref | the excuse is refused (the instance must run) |
| C6 | after an arrival: (a) no `open` provisional row whose `settles_on` side is now `real` (tag `provisional-open-on-real`, passable by the person's word `substitute kept: <side>`, which makes the row `kept_by_decision`); (b) a `settled_*` row cites a run block (`evidence.run` = its `block_id`) that exists, is a run (not a collect) and whose stamp says `settles_on` was `real`, and the hash relation matches the status; (c) no `pending_implementation` row with `instance_ids` whose instances ALL have a run block stamped `real` on every side the test names (B5; repair: `retracted_unresolved`) | `s5_precheck` `sides` | data | xref | repair; (a) passable by tag, (b) and (c) not |
| C7 | a Then oracle `precedent` with ref `reference:<item>`: the item exists in `work/reference-snapshot.yaml`, and the case basis names an R-n whose register row carries `parity: yes` | `contract.py` (the then-oracle precedent branch, ~:1646-1650) | data | xref | refusal at the existing place (S4 exit) |
| C8 | a run on the reference stand goes and is recorded as a sample; it never counts as the story's evidence (owner, 11.11.2026) | `run_suite.py` (`build_run_block`, `write_run_block`) / `stand_identity.reference_run_mark`; read by `report_facts` | data | safety | no refusal; the run block carries the `reference_run` mark (stand, side, not the story's code) and is written to `work/reference-runs`, outside the folder every evidence reader reads (reducer, ledger, proof stamp, delivery verdict), so no reader can count it; the report names it "a run on the reference stand - a sample, not the story's result"; an older block with no mark reads as the story's own stand; what is still refused is the data contradiction, a record naming one stand as both its own and the reference: refused naming the record, never the same stand (t-2513 F3); a red sample is not a story bug (t-2277 W1; was: refusal, t-2513 open point 2) |
| C9 | the ledger derives `not_verified:on_substitute` for a covered Then (automated) or a walked case (manual-agent) whose resolved `about` meets a side the proof's stamp or the test's declaration does not record `real`; `not_verified:sides_unknown` for a proof whose stamp carries `sides_unknown` | `ledger.plan_row_state` | data | xref (a state derivation, not a refusal) | no |
| C10 | `check_delivery` reads `contract.awaiting` first and returns kind `awaiting_implementation` while the story is awaiting or stopped | `check_delivery.assess` | data | presence | no (a verdict word) |
| C11 | a manual block's `about` names only sides of the story (exact) | `manual_evidence.validate` | data | xref | repair for the runner |
| C12 | a rework of S6–S9 is refused while the story is held for code (due, awaiting or stopped); a code-typed rework (`--reason`) on a stopped story is refused (the person's words reopen) | `controller.build_rework_request` | data | presence | refusal with doors: a relaunch with the code (`--mr/--branch/--commit` or `--side <s>=real`, which IS the person's word that the side is real), `stop waiting`, or a rework of S0–S5 with the person's words |
| C13 | no S6–S8 role is dispatched while the story is held for code | `stage_guard.rule_awaiting_code` (new), appended in `dispatch_errors` | data | safety | refusal passable by a person's word through `waiver.split_overridden` and journaled `gate_override` (as rules 1–3) |
| C14 | `run_witness` is not demanded only when every test of the manifest is excused by `acceptance.pending_instances` (manifest-only mode, §2.3) AND a `runs[]` row with `kind: collect` names each of them | `check_witness._all_pending` (new), in `RULES["automation-manifest.json"]` beside `_all_handed` | data | presence | refusal (run_witness demanded) otherwise |
| C15 | a side name given at launch that differs from a recorded side name of the project only by letter case is refused with the recorded name | PC-1b, `Driver.s0_write_sides` | data | xref | refusal with door ("use `<recorded>`, or the conductor records a new side") |
| C16 | a row of `product.sides`, `environments.sides`, `environments.reference_for` carries a `value` of the shape §2.1 names, words from `side-realities.json` | `project_knowledge.record_problems` (t-2142 unit, altered) | data | shape | refusal of the write |
| C17 | `stage_done.py --set sides.<n>.reality=` accepts only a word of `side-realities.json`; `deliverable` only true/false | `stage_done.py` | data | shape | refusal |

Role judgments this spec relies on (never judged by code; accepted by the tier named): which sides a Then speaks about
(`about`) — automator, accepted by the code critic; which sides a manual walk's case speaks about (`about` on the manual
block) — runner, accepted at S6 acceptance by the failure analyst (`references/stages.json:196`, `acceptance_by`);
whether a mock stands for a side and the test level matches its boundary (`references/coverage-design.md:79-85`) — code
critic; which diff changes affect which register rows and cases at arrival — requirements tester, accepted by the case
critic and, where meaning changed, by the person at gate A; whether a requirement is a parity requirement — tester,
accepted by the case critic, confirmed by the person at gate A; whether old locators are portable — the runner who
walked the reference, read by the automator as a hint only. Intent (the person): `deliverable` where no
`product.sides` row says it; the parity scope at gate A; `stop waiting`.

Error directions of reused functions in a more consequential role:

- `ledger.plan_row_state` (`scripts/ledger.py:348-420`) becomes the place that refuses "green" for a substituted proof,
  for EVERY proof route. Allowed error: `on_substitute` for a Then really proven (over-caution, costs a re-pass line).
  Forbidden error: `passed_green` for a Then or a walked case whose subject side was substituted or unknown.
  Adversarial inputs that must stay on the safe side (each a case in `test_sides_ledger.py`): a `then_bindings` row with
  no `about`; `about: []`; `tests[].sides: {}` with no `about` on a stand whose stamp says `backend: substituted` (B1);
  a `tests[]` row with no `sides` on a story that has a substituted side; `about` naming a side the story does not
  declare; a side that became `real` after the run (the stamp decides, not today's reader); two instances covering one
  Then, one stamped real and one substituted (the real green proves it — one test whose own sides were all real;
  never merging evidence of two tests, FR-18); a red on a substitute (stays `failed:*`); a manual-agent walk green on a
  stand stamped `backend: substituted` with no `about` (B2); a manual-agent walk with `about: [ui]`, `ui: real`
  (proven); a stamp carrying `sides_unknown`; a reparsed run block (its stamp is copied from the block it supersedes).
  Manual-human cases are already never green (`ledger.py:442-459`: handed reads `not_executed:handed_to_person`) and
  stay so.
- `run_suite.collect_files` (`scripts/run_suite.py:1542-1558`, "the ONE collect over files of S5") becomes a WITNESS for
  an instance that cannot run. Allowed error: "collect unavailable" for a runner whose collect form is unknown (the
  instance then has a static witness only, said so, and C14 demands `run_witness`). Forbidden error: a collect recorded
  in a way the ledger or `check_witness` reads as a run. Adversarial inputs: a partial collect
  (`node_ids.CollectError.partial`, recorded `kind: collect, partial: true`, never `run`); a runner with no collect row
  in `launch-causes.json`; an instance id that collects under another spelling.
- `manual_capture.environment_of` (`scripts/manual_capture.py:522-534`) becomes the gate that lets the reference be
  walked. Allowed error: refuse a reference host that is configured but unreadable. Forbidden: allow a host outside
  `environments[]`. Nothing in the host check changes.
- `project_knowledge.state` / `subjects` (t-2142 PK0-1, SPEC:388-410) become the input of a PROOF rule (through
  `contract.story_sides` and the stamp). Allowed error: `sides_unknown` for a registry that is fine but holds one
  malformed side row. Forbidden: `real` for a side whose latest live row says `substituted` or `absent`. Adversarial
  inputs (cases in `test_story_sides.py`, PC-1b): the file unreadable; a foreign `schema_version`; a malformed `value`
  or a word outside the data file on a side row (→ `sides_unknown`, never "no row"); a revoked `substituted` row (covers
  nothing: the side is real — the person took it back); a later `real` row superseding a `substituted` one (real); an
  unparseable `at` (loses); `Backend` vs `backend` (two subjects: exact comparator); stand `Dev` vs `dev` (stand names
  exact, t-2142 SPEC:374, :1066).

---

## §2 The model

### 2.1 Sides and their reality

A **side** is a part of the product a story's checks can meet (open variety, P2). For one run each side has:

| attribute | values | meaning |
|---|---|---|
| `reality` | `real` · `absent` · `substituted` (closed list, `references/side-realities.json`) | `real`: present on the run's stand; `absent`: not built (nothing answers); `substituted`: a mock or stub stands for it on this stand or in the test |
| `deliverable` | `true` · `false` | is this side part of what THIS story delivers |
| `settles_by` | words (may be empty) | who makes the side real when this story does not ("integration testing by the platform team"); empty → "the real <side>" |
| `reference` | a stand name or absent | where an older version of this side's behaviour can be walked |
| `source` | `default` · `registry` · `launch` · `person` · `arrival` | who set the current value (for the report and the doctor); `default` only in the reader's output, never written |

**Project (standing fact) — the t-2142 registry.** `qa-factory/records/project-knowledge.json`, rows `{id PK-n, key,
environment, element, state, scope, value, provenance, at, revoked_at, revoked_words}`; one writer
`project_knowledge.record(...)`; the subject of a row is `(key, environment NAME, element)`, the latest live row by
`at` wins, a changed answer is a new row, `revoke` retires one (t-2142 SPEC:359-390, :412-420). Three keys, each row's
`element` = the side NAME, every row written with `state: known` (S4a):

| key | scope | `environment` | `value` (words from `references/side-realities.json`) | meaning |
|---|---|---|---|---|
| `product.sides` | project | `""` | `{"deliverable": true \| false, "settles_by": "<words, may be empty>"}` | the project has this side; whether a story of this team delivers it, and who makes it real when it does not |
| `environments.sides` | stand | stand name | `{"reality": "real" \| "substituted" \| "absent"}` | how this stand holds the side |
| `environments.reference_for` | stand | stand name | `{"reference": true}` | this stand runs the OLD version of the side (S-c) |

- The reference stand's ADDRESS stays an ordinary `environments[]` row (t-2142 keeps stands in config in phase 0); only
  the fact "it is the old version of side X" is a registry row. When t-2142 node 3.6 moves `environments[]` to its own
  file, the reference row follows it (N4).
- **What PC-1b adds inside `project_knowledge.py`** (on top of the module PK0-1 lands; each a line to agree with the
  project-knowledge session, end of spec):
  1. the three rows in the `KEYS` literal (t-2142 SPEC:363-366), each with comparator `exact`;
  2. an `exact` comparator: a function `_exact_form(text) -> str` returning the element unchanged, registered in the
     key → comparator map beside `role_form` (t-2142: "a later key with case-sensitive or punctuation-bearing elements
     registers another comparator", SPEC:365). Side names are compared EXACTLY everywhere: registry elements,
     `pipeline.sides` keys, `tests[].sides`, `about`, C2 (S2);
  3. `record_problems` (SPEC:412-418) gains, for the three side keys only, the `value` shape of the table above with
     words read from `side-realities.json` (S1); `record_problems` is an existing census unit of class `shape` — class
     unchanged, no raise;
  4. a pure lister `subjects(root, key, environment=None) -> {"subjects": [(environment, element)], "problem": str}`:
     the subjects of `key` (all stands when `environment` is None) whose latest live row (the module's own precedence:
     revoked skipped, unknown `state` skipped, unparseable `at` loses) exists; never writes, never raises (S3);
  5. the CLI subcommand `side --name <side> [--stand <name>] (--reality real|substituted|absent | --deliverable
     yes|no [--settles-by-file F] | --reference) --words-file F` (conductor only), a `references/conductor-actions.json`
     row, and the guard: `guard_pre_tool.py` `human_word_check` gets `side` in the alternation PK0-8 writes, and
     `HUMAN_WORD_MSG` one clause; no new function in `guard_pre_tool.py` (PK0-8's non-goal holds) (S4c).
- **Writers** (the registry has ONE writer function; these are its callers): (1) the conductor, on the person's words,
  through the `side` subcommand; (2) the driver (`by: driver`, `source: person`), from the person's CLOSED answer to
  `sides.deliverable` — `another team's` records `product.sides` `deliverable: false`, `ours` records `true` — so the
  question is asked ONCE per project and side (D-0043); (3) onboarding writes nothing (t-2142 moves onboarding to its
  phase 4, SPEC:1084).
- **A `no_trace` story** (P8): `record` refuses (SPEC:417). The driver keeps the answer in `pipeline.sides`
  (`source: person`) and the report says one line "your answer about <side> was kept for this story only (an
  experiment leaves no trace)"; the next story asks again (S4b).
- **A side becomes real for good**: a new `environments.sides` row `reality: real` supersedes the old one; the story-level
  change of ONE story stays `pipeline.sides` with `source: arrival`. The registry has no validity period; nothing
  expires by itself.
- `records/environment-properties.json` (the person's `accept always` on a gap card, `references/environments.md:98-107`)
  stays what it is — the acceptance of a gap, not a declared reality; it is named as a sibling on axis 34 (PC-10).

**Story — `pipeline.json` `sides`**: `{<name>: {reality, deliverable, settles_by, reference?, source, at}}`. Written by
`stage_done.py --set sides.<name>.<attr>=<value>` ONLY when the story has a non-real side or a reference (S13): at S0
by `Driver.s0_write_sides` from (later wins) the reader's registry leg for the chosen stand, the launch flags
`--side <name>=<reality>` / `--reference <env>`, the person's answer to the no-change question (`not built yet` → the
changed side `absent`, `deliverable: true`); later only by the arrival road (`source: arrival`). Once written it stays
(a side that becomes real keeps its entry with `reality: real, source: arrival`). Absent (every story on disk today, and
every all-real story) → the reader derives.

**Story — `pipeline.json` `sides_unknown`**: `{at, why}`. Written by `Driver.s0_write_sides` (PC-1b) when the registry
leg cannot be read (the file unreadable, a foreign schema, a malformed side row for this project or stand); re-tried on
every relaunch at the arrival-step position (§3.2), and cleared (`stage_done.py --set sides_unknown=`) by the first
successful read, which then writes `pipeline.sides` if a side is non-real. Absent → the sides were read (or there was
nothing to read).

**One reader**: `contract.story_sides(pipeline, cfg, env_name=None) -> {name: {reality, deliverable, settles_by,
reference, source}}`. Order: `pipeline.sides` first (a readable record always wins), then (PC-1b) the registry through
`project_knowledge.subjects` + `state` (never the file directly; `product.sides` for project rows,
`environments.sides` for the chosen stand, `environments.reference_for` over ALL stands to find a side's reference),
then the default `{product: {reality: real, deliverable: true, settles_by: "", reference: None, source: default}}`.
`product` is implied when the story's sides (the registry's, the launch's and the person's answers merged) hold no real side of this team (PC2-7, t-043, the owner's word 12.11.2026); a project that recorded its real side (`ui: ours`) gets no `product`; a side known only from an `environments.sides` row has
`deliverable` unknown (the `sides.deliverable` question decides, F-12) and, until answered, `deliverable: true`. In
PC-1a the registry leg does not exist and the reader goes `pipeline.sides` → default. An unreadable `pipeline.json` →
the default plus a note on stderr (the story's other readers fail on it too). `contract.parks_after_s5(pipeline) -> bool`:
`pipeline.sides` holds a side with `reality: absent` and `deliverable: true` (S6: never for `substituted`).

INVARIANT the sides record protects: a side recorded as non-real is never read as real by a later stage unless the
arrival road recorded the change — an unrecorded "it's real now" never makes a substituted proof count; and an
unreadable record of the sides never reads as `real` (S12).

### 2.2 The provisional registry — `automation-manifest.json` `provisional[]`

Everything a test ASSUMES rather than observed. One writer: the automator through `manifest_put.py --fragment` (merge
by `id`; fields a fragment omits survive, as for `unresolved[]`).

| field | content |
|---|---|
| `id` | `P-<n>`, unique in the story |
| `kind` | a key of `references/provisional-kinds.json`: `placeholder_locator`, `assumed_contract`, `side_substitute`, `reference_value` (the list grows as data) |
| `what` | the assumption in the user's words |
| `assumed_from` | `requirement:R-n` · `sibling:<file>:<line>` · `framework:<section of strategy/framework-rules.md>` · `reference:<snapshot item>` · `spec:<R-n>` |
| `home` | `{file, line_hint}` — the single place the PROJECT keeps this locator / contract / mock by its framework rules (`strategy/framework-rules.md` "Layers and idioms", `skills/qa-onboarding/phases/p4-generate.md:494-500`), never a test body. The home is FOUND by the marker comment `qa-provisional: P-n` in `file` (the test language's comment syntax); `line_hint` is a hint only (S9) |
| `home_hash` | sha256 of the marked line (the line carrying `qa-provisional: P-n`, wherever it is in `file`) at write time; written by `manifest_put.py`, a role-sent value ignored |
| `dependents` | `[{case, then}]` |
| `settles_on` | the side whose becoming real settles it |
| `status` | `open` · `settled_matched` · `settled_edited` · `kept_by_decision` · `retracted` |
| `evidence` | on settle: `{run: <run block_id>, home_hash_after}`; on `kept_by_decision`: the reason — the side's `deliverable: false` (registry or `pipeline.sides`), or the person's word (`stage_overrides[]` block `substitute kept: <side>`) |

Empty outcome: `provisional: []` (declared, not absent) on a story with a non-real side; absent on a story with all sides
real (old stories unchanged; the precheck does not ask for it).

The automator's grounding rule (`agents/qa-automator.md:54`: "Ground before you write. Selectors and contracts come from
a live check or the manifest's grounded observables; neither: stop for that case.") gains a third legal route: **a
provisional row** — only when the side the selector or contract belongs to is not `real` in the story's sides. On a
real side the old rule stands unchanged. A silent guess stays forbidden: a placeholder without a row is caught by C4 or
by the critic.

INVARIANT: a provisional value is never an expected value. A placeholder is HOW to reach the product, never WHAT a Then
expects (P20; the expected value still comes from `then_oracles`).

### 2.3 Proof strength — one rule for every proof route

- `tests[].sides`: `{<side>: real|substituted|absent}` — how this test's boundary meets each side it touches (declared
  by the automator, judged by the code critic against `coverage-design.md:79-85`). A test that touches an `absent` side
  declares it `absent`; it cannot run: it is written, collected, and its instances are listed in an `unresolved[]`
  `pending_implementation` row (`instance_ids`) — the existing reason (`scripts/contract.py:80`) with its existing
  meaning "awaiting the implementation MR" (`check_traceability.py:59-60`). The excuse is read by ONE reader,
  `acceptance.pending_instances(manifest, items, scope, sides=None)` (C5): with `sides` (the reader's output) it checks
  all three conditions; with `sides=None` (manifest-only mode, used by `check_witness`, which has no story root) it
  checks the first two, and the third is checked by `s5_precheck` C5 at the same S5 exit.
- `then_bindings[].about`: `[<side>]` — which sides the Then speaks about (automator; the code critic judges).
- A manual block (`work/manual-blocks/`, written by `manual_evidence.write_block`) may carry `about: [<side>]` — which
  sides the walked case speaks about (runner; S6 acceptance judges; C11 checks the names).
- **The proof stamp** (F-14 recommendation): every execution block — a run block (`run_suite.build_run_block`,
  `scripts/run_suite.py:469`, reparse `reparse_run_block` :647 copies the stamp of the block it supersedes) and a manual
  block (`manual_evidence.write_block`, `scripts/manual_evidence.py:1275`) — carries `sides_met: {<side>: <reality>}`
  copied by CODE from `contract.story_sides` at the moment of the execution, plus `sides_unknown: "<why>"` when
  `pipeline.sides_unknown` is set. Written only when `pipeline.sides` exists, or the reader returns a non-real side, or
  `sides_unknown` is set (S13); otherwise the block is byte-identical to today's. `finalize_task.reduce`
  (`scripts/finalize_task.py:339`, which reduces both `work/run-blocks/` and `work/manual-blocks/`, :2-7) copies the
  block's stamp onto every `results[]` and `current_manual_checks[]` row it reduces from that block. The ledger reads the
  stamp on the report row; C6 reads it on the run block `evidence.run` names. One place, one reader branch.
- **Rule (automated)**: for a covered Then bound to a test T whose result row carries stamp M:
  resolved `about` = `about` when it is a non-empty list; else the keys of `T.sides` UNION every side M records with a
  reality other than `real`. The Then is PROVEN when T ran green and, for every side `s` of the resolved `about`,
  `T.sides.get(s) == "real"` AND `M.sides_met.get(s) == "real"` (a missing key is NOT real). By construction an empty
  resolved `about` occurs only when M records no non-real side, so an empty claim never proves on a substitute (B1). A
  Then not proven by this rule but covered by a green T reads `not_verified:on_substitute`. A Then about the UI's own
  behaviour on a mocked backend (`about: [ui]`, `T.sides: {ui: real, backend: substituted}`) is green for good.
- **Rule (manual-agent)**: for a walked case W with stamp M: resolved `about` = W's `about` when non-empty, else every
  side M records. Green W is PROVEN when every side of the resolved `about` is `real` in M; otherwise
  `not_verified:on_substitute` (B2).
- **Unknown**: a result row whose stamp carries `sides_unknown` reads `not_verified:sides_unknown` (S12).
- **Where the branch applies**: only to a result row that carries a stamp, or whose test declares a non-real value in
  `tests[].sides`; every other row is read exactly as today (E-T1). Position in `plan_row_state`: after every failure,
  flaky, partial, error, unknown-word, unconfirmed, skipped and manual word, before `passed_green`; `sides_unknown`
  before `on_substitute`. A red on a substitute stays `failed:*`.

### 2.4 States and exits (FR-40, AR-25; rows for `design/state-exits.md`)

| state | who sets it | way out | verdict kind |
|---|---|---|---|
| `pipeline.sides.<s>.reality = absent/substituted` | S0 (registry, launch, the person's answer) | the arrival road (`source: arrival`): a relaunch with a source flag or `--side <s>=real` | none by itself |
| `pipeline.sides_unknown` | S0 (PC-1b) on an unreadable registry | a later successful read on a relaunch clears it; the Thens proven under it are re-run (S6 rework) or passed by the person's word | `sides_unknown` (after_checks, owner factory) on the Thens proven under it |
| story held for code — `due` (S5 completed, `contract.parks_after_s5` true, no `await` yet) and `awaiting` (controller event `await`, controller state `awaiting {since, sides, packet, s5_dispatch}`, projected to `pipeline.awaiting`) | the controller | (1) arrival: relaunch with `--mr/--branch/--commit` or `--side <s>=real` → event `arrive` clears it; (2) the person's `stop waiting` (`controller.py --operation stop_waiting --words-file`) → `stopped`; (3) `rework` of S0–S5 (a ticket change, the person's words): the work runs and the next S5 acceptance re-evaluates (a new `await` replaces the record and its packet when the S5 dispatch differs). A rework of S6–S9 is REFUSED (C12). POSITIONAL INVARIANT (B3): while the story is held for code, no dispatch of S6–S9 is opened, prepared or relaunched; a rework into S6–S8 is refused with a door | `awaiting_implementation` (no, owner product, line "awaiting code") if anything asks; no gate B, no bug |
| `pipeline.awaiting.stopped {at, words}` (B4) | the controller, event `stop_waiting` | (1) the person's `rework` of S0–S5 with words (`--words-file`) → event `await_reopened {words}` removes `stopped` (the story is awaiting again, then the rework runs); (2) a relaunch with the code → `arrive` clears the whole record (the person starting the story with the code is their own act) | `awaiting_implementation` (no, owner product, line "stopped while awaiting code: <words>") |
| `unresolved[]` `pending_implementation` with `instance_ids` (written, collected, not run) | the automator | after arrival the bind round runs the instances; every row whose instances ALL ran green-or-red stamped real is RETRACTED by the automator (`--fragment {"retracted_unresolved": ["<case key>"]}`, the door of `design/state-exits.md:81`), so the runs decide; a slice row is NOT taken by a green `tests[]` entry (the mover-wins rule `:77` is for whole-case rows; `:81` keeps slice rows by design); C6(c) refuses a leftover (B5) | `pending_implementation` (no) only for a row still standing because its instances did not run on real sides — the arrived code does not implement it |
| `provisional[]` `open` | the automator | `settled_matched` / `settled_edited` (bind round, with evidence), `kept_by_decision`, `retracted` (fragment `retracted_provisional: [P-n]`) | none (its effect on proof goes through `tests[].sides`) |
| `provisional[]` `kept_by_decision` | the automator, citing `deliverable: false` or the person's word | the side becomes real later → back to `open` in the bind round; the person revokes the word (`waiver.py --revoke`) → `open` | none |
| ledger `not_verified:on_substitute` | `ledger.py` (derived) | a green run or walk stamped real on the sides (re-pass on the real side) → `passed_green` | `on_substitute` (after_checks, owner environment) |
| reference snapshot item | the runner (S1 reference window) | re-walk (`reference_snapshot.py put --replace`), or `rework S1` | none |

Readers of the held / stopped state and what each does (B4, S8):

| reader | awaiting / due | stopped |
|---|---|---|
| `controller._next_action_for_state` (reads its own state `s["awaiting"]` + `contract.parks_after_s5(pipeline)`) | `due` → `{action: await_implementation}`; `awaiting` → `{action: awaiting_implementation, since, sides, packet, held: [never-started S6–S9 dispatches]}` unless an S0–S5 stage or dispatch is open (then that work runs) | `{action: awaiting_stopped, at, words}` — terminal; nothing relaunched |
| `controller.build_rework_request` | S6–S9 refused (C12); S0–S5 allowed | S6–S9 refused; S0–S5 only with the person's words (`await_reopened`); `--reason` refused |
| driver `_act_await_implementation` / `_act_awaiting_stopped` | builds the packet and records `await` (due), or re-prints the packet (awaiting); exit 0 | prints "this story was stopped while it waited for code on <date>: "<words>"; nothing runs"; exit 0 |
| `stage_guard.rule_awaiting_code` (C13) | S6–S8 roles refused | same |
| `stage_guard.stories` (the doctor, qa-doctor step 4, `scripts/stage_guard.py:2832`) | `awaiting code since <date> (<sides>)` | `stopped waiting <date>` |
| `archive_task.open_items` (`scripts/archive_task.py:93`) | `awaiting code since <date>` replaces "never reached S9 — parked" | no open item (the person ended it) |
| `check_delivery.assess` (C10, PC-5) | one record `awaiting_implementation` | the same kind, line with the words |
| `factory_dashboard.py` (PC-5) | label "awaiting code" + age | label "stopped while awaiting code" |
| `hooklib.story_closure` | untouched (F-2): the story is `open` for closure; every reader above that must not act reads `contract.awaiting` / the controller state | same |

No unknown or substitute becomes a pass: `on_substitute`, `sides_unknown` and `awaiting_implementation` are never
`passed`; an excused instance is never `green`; a missing declaration reads conservative. (K6)

---

## §3 The run — one flow

Who acts: **code** (scripts, driver, controller), **role**, **conductor**, **person**. Stages named as today; no new
stage number.

### 3.1 Phase 1 (S0–S5), all three situations

1. **S0 (code).** `Driver.s0_write_sides` writes the sides record from the reader's registry leg (PC-1b) + the launch
   flags + answers, only when a side is non-real or has a reference (S13). A story with no change and no flag:
   - a LOCAL story → the existing `s0.no_change` question (`story_run.py:8299-8336`) gains the answer `not built yet`;
     a real ticket → the scout's halt question `s1.no_diff` (`story_run.py:2964-2976`) gains the same answer (twins,
     AR-19). The `ungrounded` answer loses the promise "each one carries a 'not met' bug at gate B" (no code makes that
     bug: the text lives at `story_run.py:2974`, `:8323-8324`, `skills/qa-story/phases/s1.md:356-357`; D2) and reads:
     "go on with the requirements only, on the code the stand runs now; a test that goes red is judged like any red".
     The new option (closed, `human-questions.md` form, rule 6 prices):
     > (c) `not built yet` — the code for this story is not written yet. The factory writes the tests now from the
     > requirements, using what the project already has (page objects, locators of similar pages); what cannot be known
     > yet gets a named placeholder. It stops after the tests are written and reviewed and tells you what is missing.
     > When the code exists, start the same story again with the merge request, branch or commit.
     > the factory: the stages up to the written tests run now; the rest runs when you start it again.
     > you: starting the story again when the code exists.
     > the story: nothing is checked against the product yet; delivery waits for the code.
   - A launch `--side <name>=<reality>` with a name the project has not recorded is ACCEPTED (F-17 (a)); a name that
     differs from a recorded side only by letter case is refused (C15, PC-1b). When an answer or a flag makes a side
     non-real, no `product.sides` row (or `pipeline.sides` entry) says its `deliverable`, and the story has a named side
     other than the implicit `product`, one closed question asks whose it is (`ours` / `another team's` / `stop`) —
     F-12. The answer is kept in `pipeline.sides` (`source: person`) by `Driver._keep_sides_answer`, and (PC-1b)
     recorded in the registry through writer 2; a single-side story (only `product`) is never asked (default `true`).
2. **S1 (role: scout).** Grounds as today. Its brief names the sides: for an `absent` side it grounds on requirements and
   on what exists (page objects, sibling pages, `existing_test_candidates`); for a side with a `reference` it also lists
   the reference's old autotests (when the reference repo is in `code_repos`) as scenario sources. **Reference window
   (S-c only, role: runner)** — F-4: after the scout, the driver opens one runner dispatch at S1 with purpose
   `reference_walk` (a `walk_session.py` walk on the reference stand); the runner writes `work/reference-snapshot.yaml`
   through `reference_snapshot.py put` (§4). Build identity is not asked for a reference stand. Reference unreachable
   (the env probe fails): one gap line "the old version at <env> could not be reached: <probe line>", `items: []`, no
   question (D-0043).
3. **S2 (role: requirements tester).** As today. In S-c the tester marks a parity requirement (`parity: yes` in the
   register row; FR-12) and writes the existing `## Behaviour claims` rows (`contract.py:961`: `before`, `before_ref`,
   `now`, `now_ref`, `differs`) with `before_ref: reference:<item>`. An `absent` side's `now` is `unknown` with
   `now_ref: absent`.
4. **S3/S4 (roles as today).** Cases carry Then oracles from requirements; a parity Then carries the existing word
   `precedent` with the new ref form `reference:<item>` (C7). **Gate A** (person): in S-c the packet shows only (a)
   claims where `differs` is yes or unknown, (b) parity requirements with no snapshot item (gaps), (c) snapshot items no
   case uses; the rest is one line "N behaviours of the old version are carried over as they are — listed in the
   attached document" (D3). Approving gate A confirms the parity scope (F-7). No other gate A change.
5. **S5 (roles: automator, code critic).** The brief carries sides and the provisional rule (AR-10). The automator
   writes every test whole by the scenario: known locators and page objects at once; a placeholder or an assumed
   contract gets a provisional row with a marker at its single home; a mock of a side gets a `side_substitute` row.
   Tests whose sides are all real or substituted RUN, are probed and reviewed as today (nothing that could run is
   excused). Tests that touch an absent side are written, collected (`run_suite.py --mine <ids> --collect-only` →
   `runs[]` row with `kind: collect`), statically reviewed by the critic, and listed in a `pending_implementation` row
   with their `instance_ids`. The S5 exit runs C1–C5; `check_witness acceptance` (`scripts/check_witness.py:217-223`)
   demands `run_witness` unless every test is handed (`_all_handed`, :87-107) or every test is pending with a collect
   row (`_all_pending`, C14, B6); a mixed manifest still needs `run_witness` for its runnable part.
6. **After S5 (code: controller).** `_next_action_for_state` reads `contract.parks_after_s5(pipeline)` and its own
   awaiting state (never the registry, S13):
   - **Exit (i)** — some side is `absent` and `deliverable` → action `await_implementation`. The driver (or the skill's
     phase step) builds the **interim packet** by code (`interim_packet.py`, F-6) into `interim-report.md` (a markdown
     document for the person): what is written (tests per case, in words), what ran and what each test DECLARED and
     what its run stamp recorded (ran on real sides / ran on a substitute / collected only — data, not a proof
     verdict), the open provisional rows in the user's words grouped by side, and the command to start again. The
     controller records `await`; the driver prints the packet and exits 0. No gate B, no verdict, no bug (D2).
   - **Exit (ii)** — no deliverable side is absent → S6 onward as usual. Substitutes (deliverable or not) and absent
     non-deliverable sides stay; the automator re-sends the provisional rows of non-real sides as `kept_by_decision`
     before S5 closes (C6(a) asks for it). The ledger reads `on_substitute` for crossing Thens and walks;
     `check_delivery` gives `after_checks`; the `on_substitute` records go one per case with `tests` (the tests to
     re-pass), `how` (the profile's one-test command) and `to_check` ("needs <settles_by or 'the real <side>'>") through
     the existing generic path of `check_delivery.build_left_items` (`:2042-2084`, one row per case; keying untouched,
     S15) — P19 rung 5, P24 style.

### 3.2 Arrival road (phase 2) — one road for "a side became real"

Trigger: a relaunch of an existing story (`pipeline.json` present) with `--mr/--branch/--commit` and/or
`--side <s>=real`. Two positions in `Driver.run` (`story_run.py:17428`; POSITIONAL edge, S11):

- **Keep the word** — the source flags and `--side`/`--reference` are kept in `launch` by `s0_keep_late_launch`
  (`story_run.py:8019-8035`, extended by PC-2), called for a resumed story right after `skip_sources_late` (:17447) and
  BEFORE the freshness branch (:17453-17464). The `sides_unknown` re-read (PC-1b) sits here too.
- **Record the arrival** — `arrival_step` runs AFTER the freshness branch and `accept_no_trace` (:17464-17468) and
  BEFORE the loop (:17470).
- INVARIANT of the positions: a changed ticket is asked first (one road for a changed ticket: the existing
  `ticket_changed` question and `ticket_rework_step`); no role is dispatched on the new code before the person's answer
  about a changed ticket is taken; a source word given on a relaunch survives a question asked in the same process (the
  answer run carries `--answer`, not `--branch`, and still arrives); the arrival is recorded before any rework opens,
  so a crash in between replays from the record.
- A stopped story relaunched with NO source flag: after the keep-the-word step, the driver prints the stopped line and
  exits 0 (no freshness look, no dispatch). With a source flag: the arrival road (`arrive` clears the record).

1. **Code**: `arrival_step` writes `implementation_source` and the sides change (`stage_done.py --set`, `source:
   arrival`), records the controller event `arrive {sides, source}`, which clears `awaiting` (and `stopped`).
2. **Role: scout** — `rework --stage S1 --cause source_arrived`: grounds on the diff only (the brief names the previous
   context manifest; `grounding_table.py` moves old records to `orphans` with `source_changed`, `:710-729`).
3. **Role: requirements tester** — `rework --stage S2 --cause source_arrived`: reconciles the diff with the register
   and the approved cases; per affected row writes `code_says` (`meets/contradicts/unknown`) and lists in its handoff
   `affected: [{case|row, why}]`. A diff that contradicts an approved case is classified by the tester (§5 E-A1).
4. **Code** opens rework only for the affected rows and cases through the existing doors (S3/S4 rework; `semantic_reopen`
   of gate A only when a case's MEANING changed); none affected → gate A stands.
5. **Role: automator** — `rework --stage S5 --purpose bind --cause source_arrived` (S5 `rework_mode: resume`,
   `references/stages.json:157`; `controller.s5_part_of` reads `bind` as a window, `controller.py:94-113`): settles each
   open provisional row whose side is now real (a live run; matched or edited, §5 E-P1), removes the substitutes of real
   sides (the row becomes `settled_edited`), runs the pending instances, RETRACTS every pending row whose instances all
   ran stamped real (B5), re-sends `tests[].sides`. Then the code critic, the probe (now owed for the formerly pending
   instances), C6.
6. S5 closes → the controller re-evaluates: another deliverable side still absent → awaiting again (§5 E-A3); else S6
   onward as usual.

The words: `source_arrived` is a DRIVER's cause like `ticket_changed` (spends none of the cap; `judge_code` /
`repair_route` read `REVIEWER_CAUSES` only, `controller.py:220-231`), placed before `ticket_changed`, which stays the last
word of `REPAIR_CAUSES` (`test_story_run_freshness.py` K26 pins it, `controller.py:226-229`). `bind` selects the bind
brief (`brief_pack.build`, PC-8: only the open provisional rows and the pending instances). `reference_walk` selects
the runner's reference-walk brief at S1 (PC-9b). The existing purpose `collect` (`controller.py:53-55`) is a dispatch
purpose and is not the `--collect-only` run flag of PC-4.

### 3.3 Reference road (S-c) — inside the same flow

An `environments.reference_for` registry row (PC-1b) or the launch flag `--reference <env>` (PC-2) names the reference;
the reader attaches `reference` to the side; the S1 reference window walks it; S2 marks parity; S4 Thens use `precedent
reference:`; gate A shows differences and gaps; the S5 automator reads each snapshot item's `locators_portable` as a
hint (`yes` → it may reuse the old locator, recorded as a `reference_value` provisional row while the new side is
absent; `no`/`unknown` → a new locator by the framework rules, or a placeholder). The new version's reality decides the
exit as in 3.1.

### 3.4 Questions to the person (all closed, `human-questions.md` form, prices per rule 6)

| key (`question-prices.json`) | when | answers |
|---|---|---|
| `s0.no_change` / `s1.no_diff` (changed) | no change given | existing + `not built yet` |
| `sides.deliverable` (new, F-12) | a non-real side whose `deliverable` no `product.sides` row and no `pipeline.sides` entry says, on a story with a named side other than `product` | `ours` / `another team's` / `stop` |
| `arrival.not_waiting` (new, F-9) | a source flag on a story that is not held for code and has all sides real | `re-ground` (the arrival road on this story) / `ignore` (the flag is dropped, the run goes on) / `stop` |
| `awaiting.stop` (new, F-10) | the person writes that a waiting story should end (the conductor offers it) | `stop waiting` / `keep waiting` |

---

## §4 Producers and readers (AR-22, AR-23)

| field / artifact | producer | readers | empty outcome |
|---|---|---|---|
| registry rows `product.sides`, `environments.sides`, `environments.reference_for` (PC-1b) | `project_knowledge.record` called by the conductor's `side` subcommand and by the driver's `_keep_sides_answer` (writer 2) | `contract.story_sides` only, through `project_knowledge.subjects` + `state` | no row → the reader's default (`{product: real, deliverable: true}`, no reference); a `no_trace` story writes none |
| `pipeline.sides` `{reality, deliverable, settles_by, reference?, source, at}` | `stage_done.py --set` from `Driver.s0_write_sides`, `Driver._keep_sides_answer`, `arrival_step`, the skill path — only on a story with a non-real side or a reference | `contract.story_sides` → `brief_pack.build`, `s5_precheck`, `acceptance.pending_instances`, `window_record`, the stamp writers, `interim_packet`, `gate_brief` (A, S-c), `stand_identity`/`runtime_probe` (skip the reference), `run_suite`/`execution_request` (C8), `factory_dashboard`, `stage_guard.stories`; `contract.parks_after_s5` → controller, `stage_guard.rule_awaiting_code`, `build_rework_request` | absent → derived (registry, then default) |
| `pipeline.sides_unknown {at, why}` (PC-1b) | `Driver.s0_write_sides` and the relaunch re-read, through `stage_done.py --set` | the stamp writers (copied as `sides_unknown`), `interim_packet`, `stage_guard.stories` | absent → the sides were read |
| driver state `launch.side`, `launch.reference` | `s0_note_launch`, `s0_keep_late_launch` | `Driver.s0_write_sides`, `arrival_step` | absent → no flag given |
| `tests[].sides` `{side: real\|substituted\|absent}` | automator (`manifest_from_tests.py` scaffolds `{}` only on a story with a non-real side) | `s5_precheck` C1/C2, `acceptance.pending_instances` (C5), `ledger.plan_row_state` C9, `interim_packet` | absent on an all-real story → never read; absent otherwise → conservative + C1 repair |
| `then_bindings[].about` | automator | `s5_precheck` C2, `ledger` C9, the code critic | absent/empty → resolved by §2.3 |
| manual block `about` | runner (in the walk record `manual_evidence.write_block` writes) | `manual_evidence.validate` C11, `finalize_task.reduce` (carried), `ledger` C9 | absent/empty → every side of the stamp |
| stamp `sides_met`, `sides_unknown` on run blocks and manual blocks | `run_suite.build_run_block` (+ `reparse_run_block` copies it), `manual_evidence.write_block` | `finalize_task.reduce` (carries it to `results[].sides_met` / `current_manual_checks[].sides_met`), `s5_precheck` C6(b)(c), `interim_packet` | absent → no non-real side was recorded at that execution; the ledger reads the row as today unless the test declares a non-real value |
| `results[].sides_met`, `current_manual_checks[].sides_met` (+ `sides_unknown`) | `finalize_task.reduce` (projection of the block stamp, not a second record) | `ledger.plan_row_state` C9 | absent → as above |
| `provisional[]` (`home: {file, line_hint}`, `evidence.run` = run block id) | automator via `manifest_put.py` (merge by id; `home_hash` by `manifest_put` from the marked line) | `contract.manifest_provisional` → `s5_precheck` C3/C4/C6, `interim_packet`, `brief_pack` (bind brief), `report_facts` (§8) | `[]` declared; absent on all-real stories |
| `runs[].kind = collect` (+ `partial: true`) | `run_suite.py --collect-only` | `check_witness._all_pending` (C14; never as a run witness), `acceptance.pending_instances` callers, `interim_packet`, `ledger` (never reads a collect as a result) | absent → `run` (today's rows) |
| controller state `awaiting {since, sides, packet, s5_dispatch, stopped?: {at, words}}` | `controller.projection` (`controller.py:1461`) of events `await`, `arrive`, `stop_waiting`, `await_reopened` | `_next_action_for_state`, `build_rework_request`, `_project_pipeline` | absent → not awaiting |
| `pipeline.awaiting` (same shape) | `Controller._project_pipeline` (`controller.py:4580`) | `contract.awaiting` → driver (`_act_await_implementation`, `_act_awaiting_stopped`, `arrival_step`, the stopped relaunch), `stage_guard.rule_awaiting_code`, `stage_guard.stories`, `archive_task.open_items`, `check_delivery` C10, `factory_dashboard` | absent → not awaiting |
| `pipeline.awaiting.packet` (the path of `interim-report.md`) | the `await` event (from the driver) | the driver's re-print on a relaunch (E-A4), `stage_guard.stories` | always set with `await` |
| `interim-report.md` | `interim_packet.py` (code) | the person | always written on entering awaiting; a story whose cases are all unresolved still gets it, with the list |
| `work/reference-snapshot.yaml` (`{reference_env, walked_at, items: [{id, area, user_path, observed, evidence: [capture paths], old_test: file:line?, locators_portable: yes/no/unknown}], gaps: [lines]}`) | runner via `reference_snapshot.py put` | S2 tester (claims), `contract` C7, `gate_brief` A (S-c section), the automator's S5 brief | `items: []` with a gap line; absent when no side has a reference |
| register column `parity` | requirements tester | `contract` C7, `gate_brief` A, the case critic | absent → `no` |
| ledger states `not_verified:on_substitute`, `not_verified:sides_unknown`; kinds `on_substitute`, `sides_unknown`, `awaiting_implementation` | `ledger.py`; `references/delivery-verdict-kinds.json` | `delivery_verdict.decide`, `check_delivery`, the report, `factory_dashboard.py` labels (`:979`) | n/a |
| `check_delivery` `on_substitute` records `{kind, case, tests, how, to_check}` | `check_delivery.assess` | `build_left_items` (generic path), the report, gate B block, dashboard | none when no Then reads `on_substitute` |
| controller events `await`, `arrive`, `stop_waiting`, `await_reopened` | `controller.py` operations (`APPLY_OPERATIONS`) | `projection`, `test_state_exits.py`, `test_awaiting_state.py` | n/a |

Files and functions that change, by name, are listed per node in §7.

---

## §5 Edges (each with its behaviour and the invariant it protects)

### Temporal
- **E-T1 old stories on disk / projects with no declaration / every all-real story.** No `pipeline.sides`, no registry
  rows → reader default `{product: real}`; `pipeline.sides` is not written, no block is stamped, no new manifest field
  is required (C1, C3 ask nothing), `next` reads only absent fields; ledger and verdict are byte-identical. The one cost
  every story pays: the larger qa-automator, qa-code-critic and qa-requirements-tester charters (PC-8 measures it with
  `role_load.py --all` before/after and names the token delta). Invariant: a story that never declared a non-real side
  behaves exactly as before, except for the charter text it loads.
- **E-T2 the sides record** is created at S0 of a new story, or by `arrival_step` / `stage_done --set` on an old one;
  before it exists the registry (PC-1b) and the default are read. Invariant: once written, the record wins over the
  registry (a registry change mid-story does not silently change a running story's proof rule; `stage_guard.stories`
  prints the record's `source`). A story with no record reads the registry live: a later registry row making a side
  non-real reaches it (toward caution); none can make a recorded non-real side real.
- **E-T3 `provisional[]`** is created by the automator's first fragment on a story with a non-real side; such stories
  cannot exist on disk before PC-2 lands, so there is no legacy form.
- **E-T4 awaiting** exists only after an S5 close on exit (i); every reader treats absence as "not awaiting".
- **E-T5 reference** is created by an `environments.reference_for` row (PC-1b) or `--reference`; a story launched
  before it has no reference; adding it mid-story changes that story only through `rework S1`.
- **E-T6 snapshot** is created by the S1 reference window; an S2 without it (old stories) never sees `reference:`.
- **E-T7 the registry before PK0-1 / PC-1b.** Before PC-1b lands (or before the registry file exists) the reader has
  no registry leg / finds no rows and returns `pipeline.sides` or the default: every story behaves as in PC-1a. The
  registry file is created by the first successful `record`.
- **E-T8 `substituted` between PC-2 and PC-5 on the branch** (F-16): PC-2 accepts `--side <s>=substituted`, but its
  proofs are kept apart only once PC-5a/PC-5 land. Behaviour by the recommendation: the batch is released only whole
  (no release from the branch between PC-2 and PC-5); projects receive releases only (PROJECT.md), and the S-b live
  proof waits for PC-5. Invariant: no released build counts a substituted proof as green.

### Empty outcomes
- **E-E1 no provisional rows** on a story with a non-real side: `provisional: []`; legal.
- **E-E2 all sides real**: nothing of this spec runs; no field required.
- **E-E3 reference declared but unreachable**: one gap line (the factory's own probe, D-0043), `items: []`; parity Thens
  fall back to the ordinary oracle rules (a requirement text if any; else `unknown` with ONE grouped question at gate A).
  Invariant: an unreachable reference never supplies an expected value and is never asked about as access.
- **E-E4 a story awaiting code that is never resumed**: it stays awaiting (no expiry, P5); `stage_guard.stories` and the
  dashboard list it with its age; the person ends it with `stop waiting` (F-10). Invariant: nothing closes a waiting
  story without the person, and nothing reports it as delivered.

### Held for code (B3, B4)
- **E-A6 rework after S5 while held.** `rework --stage S6|S7|S8|S9` on a story that is due, awaiting or stopped →
  refused (C12) with the doors (a relaunch with the code, `stop waiting`, or a rework of S0–S5 with words). A
  never-started S6–S9 dispatch left from before (e.g. prepared before a ticket change) is not relaunched: it is listed
  in the action's `held`. A rework of S0–S5 runs (a ticket change while waiting); the stage loop answers for the open
  stage S0–S5 and stops at S6 with `awaiting_implementation`. Invariant: no dispatch of S6–S9 is opened or relaunched
  for a story that is held for code; a rework into S6–S8 is refused with a door.
- **E-W1 stopped.** `stop_waiting` marks the record `stopped {at, words}` (it does not clear `awaiting`); every reader of
  §2.4's table does nothing further; a relaunch without a flag prints the stopped line. Way out: the person's rework of
  S0–S5 with words (`await_reopened`) or a relaunch with the code (`arrive`). Invariant: a stopped story is never
  prepared for S6, never closed for `story_closure`, never reported delivered, and never left without a door.
- **E-W2 `next` called without a pipeline** (tests only; production passes `_pipeline()` at `controller.py:1982`,
  `:4649`, `:8175`, `:8284`, `:9420` and `story_step.py:154`, pinned by `test_consumer_close_route.py:114`): `due` cannot
  be computed and reads false; the recorded `awaiting` in the controller's own state still holds. Invariant: the
  recorded hold never depends on the pipeline argument.

### Unknown and unreadable (S12, S4b)
- **E-U1 an unreadable registry at S0** (or a malformed side row of this project or stand): no park (nothing invents an
  absent side), `pipeline.sides_unknown` recorded, every block stamped `sides_unknown`, the ledger reads proofs under it
  `not_verified:sides_unknown` (after_checks, owner factory). A relaunch re-reads; success clears it; the proofs under
  it stay unknown until re-run. Invariant: an unknown never becomes `real` (FR-59).
- **E-K1 a `no_trace` story answers `sides.deliverable`**: the answer stays in `pipeline.sides` (`source: person`), a
  report line says it was not kept, the registry is not written. Invariant: an experiment leaves no trace (P8) and the
  answer still reaches the run (FR-8).

### Arrival conflicts
- **E-A1 the diff contradicts an approved case.** The tester classifies (role judgment): (a) an implementation detail →
  no case change, the automator settles the provisional row; (b) behaviour differs from the requirement → the case
  stays, the test goes red, S7 triage → `APP_BUG` (FR-34, P20); (c) the requirement is silent and the code chose → a
  question with before/now (P20) and `semantic_reopen` of gate A for that case only. Invariant: the diff never becomes
  the oracle; an approved case changes only through the person at gate A.
- **E-A2 the ticket text changed while waiting**: the launch word is kept first, then the freshness look runs (§3.2);
  `new text` → `ticket_rework_step` (S2, S3, gate A reopened); the next run (carrying `--answer`) records the arrival
  from the kept word and the arrival's S2 rework runs on the new text. Invariant: one road for a changed ticket; an
  arrival never bypasses it and is never lost to it.
- **E-A3 code arrives for one side only**: only that side becomes `real`; the bind round settles only its rows; the S5
  close re-evaluates: another deliverable side absent → awaiting again with a new packet; only substitutes or absent
  non-deliverable sides left → exit (ii). Invariant: a side still substituted keeps every crossing Then `on_substitute`.
- **E-A4 relaunch without any source flag on an awaiting story**: the freshness look runs; nothing changed → the driver
  re-prints the packet and exits 0; no dispatch. The ticket changed → E-A2; the S5 rework writes tests without code and
  the story parks again. Invariant: no role runs on a story whose missing side is still missing, except for a ticket
  change.
- **E-A5 relaunch with a source flag on a story that is NOT held**: (a) the story has a non-real side → the flag is an
  arrival for the changed side (same road); (b) all sides real → question `arrival.not_waiting` (F-9). Invariant: a new
  `--mr` on an existing story is never silently dropped (today it is: launch words are kept only inside `s0`,
  `story_run.py:8007-8035`, and `s0` is skipped when `pipeline.json` exists, `:17448`) and never silently re-grounds a
  finished story.

### Provisional settling evidence
- **E-P1 matched vs edited.** After arrival the automator runs the test. Matched: the hash of the marked line equals
  `home_hash` and the run reached past the locator → `settled_matched`, `evidence.run`. Edited: the marked line changed
  → `settled_edited`, `evidence.run` + `home_hash_after`. C6 checks only data: the cited run block exists, is a run (not
  a collect), its stamp says the side was `real`, and the hash relation matches the status. Whether the run "reached
  past the locator" is the critic's judgment. Invariant: a row is never settled without a run on the real side.
- **E-P2 the marked line moved** (an edit above it, the bind round): the home is found by its marker, so C4 still finds
  it and the hash compares the marked line, not `line_hint` (S9). A marker removed from `home.file` → C4 finding.
  Invariant: a moved line is never read as an edited or missing home.

### Substitutes at the end
- **E-S1 a mock left in place by decision vs forgotten.** Left: its side is not real at the S5 close (non-deliverable,
  or the person's word `substitute kept: <side>`) → `kept_by_decision`, crossing Thens `on_substitute`, a "Left with you"
  item. Forgotten: the side is `real` and the row is `open`, or a marker stays in code with no row or with a settled row
  → a C4/C6 finding. Invariant: a substitute of a real side never stands silently.
- **E-D1 a deliverable side that is `substituted`** (the team's own backend runs as a mock on this stand): exit (ii),
  `on_substitute`, a "Left with you" item (S6). Invariant: only an `absent` side parks a story; a substitute never parks
  and never proves.

### Red on the real side
- **E-R1 green on a substitute, red on the real side at re-pass.** Inside the factory (a later arrival, or a relaunch
  with `--side backend=real` on an exit (ii) story): a normal red → S7 triage (`APP_BUG`, `TEST_BUG` when the mock lied,
  `ENV_ISSUE`, … FR-34). Outside the factory: the item says "a red here is a bug of <side>; give it back to the factory
  with a rework, or file it" — no new road.

### S5 exit families (POSITIONAL)
- **E-X1** `probe`, `runs`, `run_witness` for a test that cannot run: excused only through `acceptance.pending_instances`
  (C5, C14). Invariant: nothing that could run is excused from running — an instance touching only real or substituted
  sides owes its run and probe exactly as today; the excuse is checked against the sides reader at the S5 exit, never
  the author's word alone; a collect is never a run witness. PC-4's builder first lists every reader of "this instance
  ran" (Q-a): grep `run_witness|independent_run|red_probe|_terminal_runs|probe` over `scripts/` with a positive control,
  each hit a verdict (reads the excuse / not on this road / a question to the Lead).
- **E-X2** `NO_INSTANCE_REASONS` (`controller.py:4397`) is NOT changed: pending cases have instances (the written
  tests). A pending case with NO written test stays a whole-case `pending_implementation` row with no `instance_ids`.

### Verdict
- **E-V1 awaiting vs the diff-story `pending_implementation`.** While held (awaiting or stopped), `check_delivery`
  returns ONE record of kind `awaiting_implementation` and reads no other record (no bug, no gate B). After arrival the
  bind round retracts every pending slice row whose instances ran on real sides (B5), so the runs decide; a row still
  standing (its instances did not run on real sides) or a grounding `_pending_implementation_records` entry
  (`check_delivery.py:2325-2347`) keeps verdict `no` — "the code we have does not implement this requirement".
  Invariant: the diff-story `pending_implementation` keeps `no`; a pre-code case never produces a "not met" bug (D2);
  a retracted row never hides a red (the run's red reads `failed:*`).

### Cost
- **E-C1 phase 2 re-reads**: the snapshot (kept), the diff, the register, the approved cases, the manifest with its
  provisional rows, the touched test files. It must NOT redo: S0 (snapshot kept; freshness look only), S2–S4 beyond the
  affected rows, gate A unless meaning changed, the S5 plan (kept unless cases changed — then the existing stale-plan
  exit, `design/state-exits.md:40`), unaffected tests (not rerun unless their code changed — `runs[].warranted`). The
  bind brief names only the open provisional rows and the pending instances.

### Other edges the requirements create
- **E-O1 a test with two Thens, one `about: [ui]`, one `about: [ui, backend]`, backend substituted**: the first Then is
  proven, the second `on_substitute`; the plan row reads the weaker of its Thens.
- **E-O2 a launch side name.** A name the project has not recorded is accepted (F-17 (a)) and, when non-real, gets the
  `sides.deliverable` question (F-12). A name equal to a recorded side under case-folding but not exactly (`UI` beside a
  recorded `ui`) is refused (C15) with the recorded name and the door. On a project with no recorded side the implicit
  side is `product`; `product` is implied when the story's sides (the registry's, the launch's and the person's answers merged) hold no real side of this team (PC2-7, t-043, the owner's word 12.11.2026); a project that recorded its real side (`ui: ours`) gets no `product`. Invariant: one side never lives
  under two spellings.
- **E-O3 a stand whose `environments.sides` row says a side is `substituted`**: every execution on that stand is stamped
  with that side `substituted` even if the test itself mocks nothing; the reader gives the story that side
  `substituted`; C1 asks each test of the story to declare its sides; and the ledger reads crossing Thens and walks
  `on_substitute` from the stamp whatever the test declared (B1, B2). Invariant: a stand-level mock counts like a
  test-level mock, for every proof route.
- **E-O4 the reference env selected as the run's stand (`--env <reference>`)**: refused at S0 (C8). Invariant: the
  reference is never the stand under test.

---

## §6 Forks

### Decided (record; see the decisions record at the top)

F-1 (where the standing side fact lives) — the owner: the t-2142 registry, not new config keys, not
`environment-properties.json`, not per-story only. F-2 (`pipeline.awaiting` projected record, story closure untouched)
— the Lead. F-3 (S-c as a side attribute `reference`, not an `implementation_source` value) — the Lead. F-4 (the runner
walks the reference at S1, purpose `reference_walk`) — the Lead. F-5 (generic `--side`/`--reference` + the `not built
yet` answer; `--ungrounded` unchanged) — the Lead. F-6 (the interim packet by code) — the Lead. F-7 (gate A approval
confirms the parity scope) — the owner. F-8 (`precedent` with ref `reference:<item>` + register `parity`; the `history:`
guard unchanged) — the Lead. F-9 (`arrival.not_waiting` closed question) — the Lead. F-10 (`stop waiting` door) — the
owner. F-11 (`after_checks` with re-pass items for a substituted side) — the owner. F-12 (the person decides
`deliverable` by one closed question on a multi-side story; single-side default true) — the owner. F-13 (S-c live proof
on MyBooks with an older tag as a second stand; the set-up is the owner's) — the owner.

### New in revision 3 (the spec is written by the recommendation)

Taken by the Lead as recommended, 10.11.2026 15:57 (technical; the owner was told and may reverse): F-14, F-15, F-17,
F-18. F-16 — decided by the owner, 10.11.2026 (translated: "whole"): (a), the batch is released whole, no release between
the first slice and PC-5.

| id | fork | options | cost / consequence | recommendation |
|---|---|---|---|---|
| F-14 (B2) | the one place the sides a proof met are recorded | (a) a stamp `sides_met` on every execution block (run blocks and manual blocks), carried by `finalize_task.reduce` onto report rows; (b) `runs[].sides` in the manifest for automated runs plus a field on `current_manual_checks[]` for walks; (c) one report-level stamp written by `finalize_task` | (b) two places and the ledger joining results to manifest runs; (c) unsafe: blocks reused after an arrival would be read as met real (the forbidden direction); (a) touches three writers (`build_run_block`, `write_block`, `reduce`) but one field, one branch | **(a)** |
| F-15 (S18) | a new SIBLING_MAP axis for the per-story readers (`story_sides`, `manifest_provisional`, `awaiting`) | (a) none: the registry keys and `story_sides` join axis 34; the per-story readers are named as AR-13 carriers in `design/architecture.md`; (b) a new axis "sides reader" | (b) one more axis to walk on every change | **(a)** |
| F-16 (temporal) | `substituted` accepted by PC-2 before PC-5 keeps its proofs apart | (a) release only the whole batch (no release between PC-2 and PC-5); (b) PC-2 refuses `substituted` with a door and PC-5 removes the refusal | (b) code in two nodes for a branch-internal window; (a) holds only if the first slice is not released alone | **(a)**; if the Lead wants the first slice released alone, (b) |
| F-17 (S5) | a side name at launch the project has not recorded | (a) accepted; the `sides.deliverable` answer records it through writer 2; E-O2 refuses only a case variant of a recorded name; (b) refused; writer 2 dropped; the conductor's `side` subcommand is the only road | (b) makes F-12's question unreachable from a flag (it would reverse the owner's F-12 in practice) | **(a)** |
| F-18 (B4) | a retro (S9) on a stopped story | (a) none: stopped means no further action; stage_guard rule 1 already needs S8 done; the spend stays in the journal and the dashboard; (b) retro allowed: rule 1 exempts S9 on a stopped story | (b) a change in the order rule for a rare state | **(a)** |

Closed by the designer (no design weight; listed so they can be reversed):
- names: `sides`, `sides_unknown`, `sides_met`, `provisional`, `P-n`, `about`, `awaiting`, `stopped`, `await_reopened`,
  `interim-report.md`, `reference-snapshot.yaml`, marker `qa-provisional: P-n`, kinds `on_substitute`, `sides_unknown`,
  `awaiting_implementation`, ledger states `not_verified:on_substitute` / `not_verified:sides_unknown`, the stage_guard
  function `rule_awaiting_code` (not `awaiting_state`, which `stage_guard.py:728` already uses for X7-6), the test file
  `test_awaiting_state.py`, the C1/C6 tags `sides-undeclared` / `provisional-open-on-real`, the comparator `exact`;
- the awaiting and stopped stops exit 0 (a report, not a question; exit 3 is for a person's decision, `story_run.py:39-44`);
- the collect witness reuses `run_suite.collect_files` behind a new `--collect-only` flag;
- `pending_implementation` is reused for written-but-unrunnable instances;
- the implicit default side is named `product`;
- a side known only from a stand row reads `deliverable: true` until the person answers;
- an execution records the sides it met (the stamp), so a later change of reality never rewrites what it proved.

---

## §7 Implementation plan (batch form)

Pile/batch name suggestion: `pre-code/1` (the Lead's choice). Node ids `PC-n`. Paths from `ai-packages/qa-factory/` in
`D:/ws1/wt-fbfix` (a dispatch carries them absolute on its `owns:` line, R11-f). Witness commands run from the
package root of the builder's worktree: `python -B scripts/tests/<file>.py` (`plans/builder-rules.md` 7b;
`story_run.py` nodes add 7c). Every node that writes the package walks the FR sections it touches and carries its
`architecture:` and `judgment:` lines. Every node leaves the factory working: until PC-2 lands nothing can make a side
non-real, so PC-1a/3/4/6 are inert on every story (E-T1); until PC-6 lands nothing parks a story. Slow files
(`test_story_run_*`, the CI-tier `SLOW_TESTS`) are named in the hand-over and proved by CI, never run by the builder.
Executor: each node «builder → critic»; PC-5, PC-5a and PC-6 critic mandatory (verdict / core).

External nodes (pile `project-knowledge`, batch 1, spec t-2142): **PK0-1** (the registry module), **PK0-6** (AR-3 text,
axis 34), **PK0-8** (guard closes the registry's write commands). They are referenced in `depends`, not owned here.

| node | what (direction chosen) | files and functions | tests (one per item) | witness | tier | depends | AR |
|---|---|---|---|---|---|---|---|
| PC-1a | Sides data, the one reader over the story record, the hold readers | `references/side-realities.json` (new: `realities: [real, absent, substituted]`, `default: {product: {reality: real, deliverable: true, settles_by: ""}}`); `scripts/contract.py` (new `story_sides` [pipeline leg + default only], `parks_after_s5`, `awaiting` — nothing else); `scripts/stage_done.py` (`--set sides.<n>.<attr>=` and `sides_unknown=` accepted, words checked against the data file, C17) | `test_story_sides.py` (new): default with no `pipeline.sides`; `pipeline.sides` read with `settles_by` (empty → ""); unknown reality refused by `stage_done`; side `kiosk` passes; `parks_after_s5` true for absent+deliverable, false for substituted deliverable (S6) and absent non-deliverable; `awaiting` absent → none, record → awaiting, `stopped` mark → stopped | `python -B scripts/tests/test_story_sides.py` | sonnet builder → opus critic | — | AR-1, AR-2, AR-13 |
| PC-1b | The registry leg: three keys, `exact`, value check, `subjects`, `side`, guard, unknown | `scripts/project_knowledge.py` (functions: the `KEYS` literal +3 rows, new `_exact_form` and its comparator registration, `record_problems` value shape for the three keys, new `subjects`, the `side` subcommand and its parser — nothing else); `references/conductor-actions.json` (row `side`); `scripts/guard_pre_tool.py` (`human_word_check`: `side` in the alternation; `HUMAN_WORD_MSG`: one clause; no new function); `scripts/contract.py` (`story_sides`: the registry leg through `subjects` + `state`); `scripts/story_run.py` (`Driver.s0_write_sides`: the registry read, C15, `sides_unknown`; `Driver._keep_sides_answer`: writer 2 through `project_knowledge.record`, the `no_trace` line; the relaunch re-read call inside `s0_write_sides` — both functions created by PC-2) | `test_project_knowledge.py` additions: `side` writes `state: known` rows for each key; `record` refuses `reality: mocked` and a `product.sides` value without `deliverable`; `UI` and `ui` are two subjects; `subjects` skips revoked, latest wins, unparseable `at` loses; a `no_trace` story is refused with the door. `test_guard_project_knowledge.py` additions: `side` blocked for a role (space and argv-list spellings); `show` open. `test_story_sides.py` additions: a stand row; a project row; pipeline wins over the registry; reference found on another stand's row; malformed side row → `sides_unknown`; unreadable registry → `sides_unknown`; `product` implied beside another team's real side / not implied beside this team's real side (PC2-7, t-043). `test_driver_layers.py` (7c): the second story of a project is not asked `sides.deliverable`; a `no_trace` story keeps the answer in `pipeline.sides` with the line; C15 refuses `UI` beside a recorded `ui` | `python -B scripts/tests/test_story_sides.py`; `python -B scripts/tests/test_project_knowledge.py`; `python -B scripts/tests/test_guard_project_knowledge.py`; `python -B scripts/tests/test_driver_layers.py` | sonnet builder → opus critic | PK0-1, PK0-8 (pile project-knowledge), PC-1a, PC-2 | AR-3 (text on main + "PK0-6 pending", N5), AR-13, AR-14, AR-28 |
| PC-2 | Launch and the no-change twins | `scripts/story_run.py` — functions `s0_note_launch`, `s0_keep_late_launch` (keep `side`, `reference` too), `launch_flags`, `s0_no_change_entry`, the `s1.no_diff` branch of the halt question builder (`:2959-2976`), the argparse block (`--side`, `--reference`), new `Driver.s0_write_sides` (writes `pipeline.sides` only for a non-real side or a reference, S13), new `Driver._keep_sides_answer` (the `sides.deliverable` answer into `pipeline.sides`, `source: person`); `references/question-prices.json` (`s0.no_change`, `s1.no_diff`: answer `not built yet`; new key `sides.deliverable`); `skills/qa-story/phases/s1.md:330-373` (option 3 text, new option); `agents/qa-scout.md` (reads sides in its brief; grounding of an absent side) | `test_no_mr_entry.py`: `not built yet` records `pipeline.sides.<changed>.reality=absent`, `deliverable: true`; the `ungrounded` text carries no "not met" bug; an all-real launch writes NO `pipeline.sides`; `--side backend=substituted` with an unrecorded name is accepted and asks `sides.deliverable` (F-17 (a)); a single-side story is not asked. `test_story_run_words.py`, `test_driver_layers.py` (7c) | `python -B scripts/tests/test_no_mr_entry.py`; `python -B scripts/tests/test_story_run_words.py`; `python -B scripts/tests/test_driver_layers.py` | sonnet builder → opus critic | PC-1a | AR-16, AR-19, AR-24 |
| PC-3 | The manifest fields | `references/provisional-kinds.json` (new); `references/artifact-contract-automation.md` (sections `tests[].sides` with `absent`, `then_bindings[].about`, `provisional[]` with `home: {file, line_hint}` and `evidence.run` = run block id, `runs[].kind`); `scripts/manifest_put.py` (merge `provisional` by `id`, `home_hash` from the marked line found by its marker, door `retracted_provisional`); `scripts/contract.py` (new `manifest_provisional` — nothing else); `scripts/manifest_from_tests.py` (scaffold `sides: {}` only on a story with a non-real side); `references/null-outcomes.json` rows; `design/state-exits.md` manifest rows | `test_provisional.py` (new): merge by id keeps omitted fields; `home_hash` is the hash of the marked line wherever it is (marker one line below `line_hint` → same hash); a role-sent hash ignored; the retract door. `test_manifest_put_merge.py` addition; `test_null_outcomes.py`; `test_state_exits.py` | `python -B scripts/tests/test_provisional.py`; `python -B scripts/tests/test_manifest_put_merge.py`; `python -B scripts/tests/test_null_outcomes.py`; `python -B scripts/tests/test_state_exits.py` | sonnet builder → opus critic | PC-1a | AR-14, AR-22, AR-23, AR-25 |
| PC-4 | S5 exit checks C1–C6, the one excuse reader, the collect witness, `_all_pending` | first the Q-a pre-list (E-X1) in the report; `scripts/acceptance.py` (new `pending_instances` — nothing else); `scripts/s5_precheck.py` (new family `sides`, NOT in `PASSABLE`; `WORD_PASSABLE_TAGS` += `sides-undeclared`, `provisional-open-on-real`; new `check_sides(manifest, sides, task_root, findings)` called by the caller right after `check_manifest` returns (`:4045-4046`, N6); `pending_instances` read once beside `blocked` (`:4057-4059`) and passed into `check_run_mapping` as a second excused set); `scripts/window_record.py` (probe owed except a `pending_instances` instance, read beside `blocked_instances` at `:1049-1053`); `scripts/run_suite.py` (the `--collect-only` flag in the argparse block and its branch: `collect_files`, a `runs[]` row `kind: collect`, `partial: true` on a partial collect); `scripts/check_witness.py` (new `_all_pending`; `RULES["automation-manifest.json"]` reads it beside `_all_handed`); refusal registry / A24 rows; census rows | `test_s5_precheck_sides.py` (new): C1–C6, one positive and one negative each; C5: an instance on real+substituted sides with no run is refused even with a pending row; a pending row on an instance whose sides are all real is refused; C4/E-P2: marker moved one line → no finding; S10: a `sides-undeclared` finding passes by word, a C3 finding does not; B5 `leftover_pending_row_after_real_runs_refused`. `test_check_witness.py` (new): `all_pending_with_collect_accepted`, `all_pending_without_collect_refused`, `one_runnable_needs_run_witness`, a collect is no run witness. `test_window_record.py`: probe not owed for a pending instance, owed for a substituted one. `test_run_suite_mine.py`: collect row; partial collect never a run. `test_judgment_census.py` | `python -B scripts/tests/test_s5_precheck_sides.py`; `python -B scripts/tests/test_check_witness.py`; `python -B scripts/tests/test_window_record.py`; `python -B scripts/tests/test_run_suite_mine.py`; `python -B scripts/tests/test_judgment_census.py` | sonnet builder → opus critic | PC-3 | AR-9, AR-10, AR-15, AR-20, AR-28, AR-29 |
| PC-5a | The proof stamp (B2, F-14) | `scripts/run_suite.py` (`build_run_block`: stamp `sides_met` / `sides_unknown` by the S13 condition; `reparse_run_block`: copy the stamp of the superseded block); `scripts/manual_evidence.py` (`write_block`: the same stamp and the runner's `about`; `validate`: C11); `scripts/finalize_task.py` (`reduce`: carry the block's stamp onto each `results[]` / `current_manual_checks[]` row); `references/artifact-contract-run.md` (the stamp fields, `about` on a manual row); `agents/qa-runner.md` (one line: name `about` on a walk when the story has a non-real side) | `test_proof_stamp.py` (new): a run block on a story with `pipeline.sides` is stamped; an all-real story with no `pipeline.sides` gets a byte-identical block; a reparse keeps the stamp; `manual_block_is_stamped` with `about`; C11 refuses an `about` naming a non-side; `reduce` carries the stamp to both row kinds; `sides_unknown` carried. `test_manual_evidence.py`, `test_manual_projection.py` additions | `python -B scripts/tests/test_proof_stamp.py`; `python -B scripts/tests/test_manual_evidence.py`; `python -B scripts/tests/test_manual_projection.py`; `python -B scripts/tests/test_run_suite_mine.py` | sonnet builder → opus critic (mandatory: proof records) | PC-4 (`run_suite.py`), PC-1a | AR-14, AR-21, AR-22, AR-28 |
| PC-5 | Ledger and verdict | `scripts/ledger.py` (`plan_row_state`: the §2.3 branch, `sides_unknown` then `on_substitute`, at the position §2.3 names; new private helpers `_resolved_about`, `_met_real`); `references/delivery-verdict-kinds.json` (kinds `on_substitute` after_checks/environment, `sides_unknown` after_checks/factory, `awaiting_implementation` no/product; the ledger-state rows; words lines "awaiting code", "stopped while awaiting code"); `scripts/check_delivery.py` (`assess`: `contract.awaiting` first → one record; `on_substitute` records one per case with `tests`, `how`, `to_check` — `build_left_items` untouched, S15); `scripts/factory_dashboard.py` (label rows near `:979`) | `test_sides_ledger.py` (new): every adversarial input of §1.3's first error-direction bullet, by name: `empty_sides_no_about_on_stand_substitute_is_on_substitute` (B1), `manual_agent_green_on_stand_substitute_is_on_substitute` and the `about: [ui]` proven case (B2), `retracted_pending_row_the_run_decides` (B5), `stamp_sides_unknown_is_not_verified` (S12), a red on a substitute stays `failed:*`, a real green beside a substituted green proves, an unstamped row on an all-real story reads as today. `test_third_verdict.py` (S-b `after_checks`, one item per case listing its tests). `test_report_facts.py` (diff-story `pending_implementation` still `no`). `test_check_delivery.py`: awaiting → one `awaiting_implementation` record; `stopped_story_reads_awaiting_implementation` | `python -B scripts/tests/test_sides_ledger.py`; `python -B scripts/tests/test_third_verdict.py`; `python -B scripts/tests/test_report_facts.py`; `python -B scripts/tests/test_check_delivery.py` | sonnet builder → opus critic (mandatory: verdict) | PC-5a, PC-3 | AR-26, AR-27, AR-28 |
| PC-6 | Controller and guard: held for code (B3, B4, B7, S8) | `scripts/controller.py` — `PURPOSES` (+`bind`, `reference_walk`), `REPAIR_CAUSES` (+`source_arrived` before `ticket_changed`), `APPLY_OPERATIONS` (+`await`, `arrive`, `stop_waiting`), `projection` (the four events → state `awaiting`), `Controller._project_pipeline` (`pipeline.awaiting`), `Controller._next_action_for_state` (the hold branch after the `stopped` block and before `if unlaunched:`, and the S6+ stop inside the stage loop, with the position comment of §2.4), `Controller.build_rework_request` (C12; `await_reopened` on a stopped story with words), the apply/validate branches of the new operations; `scripts/stage_guard.py` — new `rule_awaiting_code`, `dispatch_errors` (append it), `stories` (the awaiting/stopped tail); `scripts/archive_task.py` — `open_items`; `design/state-exits.md` story rows; `references/gate-registry.json` only if `test_gate_registry.py` demands it; `with_stop_after` untouched | `test_awaiting_state.py` (new, FAST: calls `Controller._next_action_for_state` statically and `projection` on synthetic events; no controller loop, N3): enters `await_implementation` only on an absent deliverable side after S5; a deliverable substituted side → `prepare_stage S6`; `arrive` clears; `stop_waiting_is_terminal`; `never_started_s6_rework_is_not_relaunched_while_awaiting` (listed in `held`); `rework_s6_refused_while_awaiting` (doors named); a rework of S2 with words while awaiting runs and the loop stops at S6 with `awaiting_implementation`; `rework_with_words_reopens_stopped`; `--reason` on stopped refused; replay gives the same state; `bind`, `reference_walk`, `source_arrived` accepted, `ticket_changed` still last, `s5_part_of` of a `bind` S5 record is `window`. `test_stage_guard.py`: `s6_role_refused_while_awaiting`; passes by a person's word and journals `gate_override`; `stories` prints `awaiting code since` / `stopped waiting`. `test_archive_task.py`: awaiting item; stopped → no parked item. `test_state_exits.py`; `test_gate_registry.py` | `python -B scripts/tests/test_awaiting_state.py`; `python -B scripts/tests/test_stage_guard.py`; `python -B scripts/tests/test_archive_task.py`; `python -B scripts/tests/test_state_exits.py`; `python -B scripts/tests/test_gate_registry.py` | sonnet builder → opus critic (mandatory: core) | PC-1a | AR-1, AR-9, AR-17, AR-25, AR-28 |
| PC-7 | Driver: park, stop, arrive | `scripts/story_run.py` — functions `run` (call `s0_keep_late_launch` for a resumed story after `skip_sources_late` and before the freshness branch; the stopped relaunch line; call `arrival_step` after `accept_no_trace` and before the loop; position comments of §3.2), new `arrival_step`, new `_act_await_implementation`, new `_act_awaiting_stopped`, `dispatch_action` (the new kinds), `until_reached` (await and stopped count as a stop); `scripts/interim_packet.py` (new: assembles `interim-report.md` from sides, manifest, provisional rows, runs and stamps — data only); `references/question-prices.json` (`arrival.not_waiting`, `awaiting.stop`); `skills/qa-story/phases/s5.md` (the skill-path step for `await_implementation`); `scripts/audit_factory.py` `CLI_SCRIPTS` (the new script) | `test_interim_packet.py` (new, fast); `test_story_run_arrival.py` (new; slow → CI only, named in the hand-over): `branch_word_survives_changed_ticket_question` (S11), no role dispatched before the ticket answer, E-A4 re-print with no dispatch, a stopped relaunch without a flag prints and exits 0, a relaunch with a flag on a stopped story arrives; `test_story_run_words.py`, `test_driver_layers.py`; `test_human_reading.py` (the two new questions) | `python -B scripts/tests/test_interim_packet.py`; `python -B scripts/tests/test_story_run_words.py`; `python -B scripts/tests/test_driver_layers.py`; `python -B scripts/tests/test_human_reading.py` | sonnet builder → opus critic | PC-2, PC-4, PC-6 | AR-16, AR-17, AR-21, AR-24 |
| PC-8 | Charters and briefs | `agents/qa-automator.md` (Techniques `:54` third route; sides/about declaration incl. `absent`; the marker at the project's home; bind-round rules incl. retracting pending rows); `agents/qa-code-critic.md` (judge `about`, `sides`, a mock for a side, level by boundary); `agents/qa-requirements-tester.md` (arrival reconciliation, `affected` — the `parity` text is PC-9a's); `scripts/brief_pack.py` (`build`: sides + provisional section at S5; the bind brief on purpose `bind` — only open rows and pending instances); `skills/qa-story/phases/s2.md`, `s5.md` (text only; PC-7 owns the `await_implementation` step in `s5.md`) | `test_brief_pack.py` (the S5 brief names the fields only when a side is non-real; the bind brief lists only open rows and pending instances); `role_load.py --all` before/after with the token delta per role in the report (S13) | `python -B scripts/tests/test_brief_pack.py` | sonnet builder → opus critic | PC-4; `s5.md` after PC-7 | AR-7, AR-10, AR-11, AR-12, AR-29 |
| PC-9a | Reference: contract and oracle | `references/artifact-contract-reference.md` (new: the snapshot shape); `scripts/reference_snapshot.py` (new: `put` validates that items cite a capture or an old test; `show`); `scripts/contract.py` (`PRECEDENT_REF_RE` second form and C7 inside the precedent branch, plus the register `parity` column reader — nothing else); `references/vocabularies.md:47` (precedent ref forms); `agents/qa-requirements-tester.md` (the `parity` column, one paragraph) | `test_reference_snapshot.py` (new); `test_oracle_provenance.py` (the `reference:` form accepted only with a parity requirement and an existing item; `base:` form unchanged) | `python -B scripts/tests/test_reference_snapshot.py`; `python -B scripts/tests/test_oracle_provenance.py` | sonnet builder → opus critic | PC-1a; `qa-requirements-tester.md` after PC-8 | AR-6, AR-21, AR-26 |
| PC-9b | Reference: the walk and the stand rules | `references/stages.json` (S1: runner, purpose `reference_walk`, optional); `scripts/story_run.py` — function `stage_simple` (S1 path: open the reference window when a side has a `reference`); `scripts/stand_identity.py` / `scripts/runtime_probe.py` (skip build identity for a reference stand, in the functions that select the stand for identity); `scripts/run_suite.py` + `scripts/execution_request.py` (C8 refusal at entry); `references/role-commands.json` (`reference_snapshot.py put` for qa-runner) | `test_stand_identity.py` (a reference stand is not asked); `test_run_suite_mine.py` + `test_execution_request.py` (C8); `test_story_run_s1`-class file (slow → CI) | `python -B scripts/tests/test_stand_identity.py`; `python -B scripts/tests/test_run_suite_mine.py`; `python -B scripts/tests/test_execution_request.py` | sonnet builder → opus critic | PC-7 (`story_run.py`), PC-5a (`run_suite.py`), PC-9a, PC-6 (the `reference_walk` word) | AR-4, AR-8, AR-11 |
| PC-9c | Reference: gate A shows differences and gaps | `scripts/gate_brief.py` (gate A section for a story with a reference: differing claims, parity gaps, unused items, the count line + the attached document) | `test_gate_brief_and_retro.py` addition: 20 snapshot items with 2 differences show 2 + the count; `test_human_reading.py` | `python -B scripts/tests/test_gate_brief_and_retro.py`; `python -B scripts/tests/test_human_reading.py` | sonnet builder → opus critic | PC-9a; `test_human_reading.py` after PC-7 | AR-16, AR-26 |
| PC-10 | Measurement, detector, map | `scripts/report_facts.py` (§8 counters); `design/architecture.md` (AR-28 and AR-25 detectors name `test_sides_ledger.py`, `test_awaiting_state.py`; AR-13 carriers name `story_sides`, `manifest_provisional`, `awaiting`, `pending_instances`); dev side: `docs/SIBLING_MAP.md` axis 34 members (the three side keys, `contract.story_sides`; `environment-properties.json` mock gap named as the sibling), `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md` check (§8) | `test_report_facts.py` addition; `python tools/architecture_index.py --check` (dev) | `python -B scripts/tests/test_report_facts.py` | sonnet builder → opus critic | PC-5, PC-7, PK0-6 (axis 34) | AR-12, AR-13, AR-20 |
| PC-L | Live proofs (rows below) | — | — | the run's journal and `interim-report.md` / `test-report.md` | Lead + stand | per row | FR-33 |

**First slice — S-a provable on the stand before the registry chain lands** (ordered; `∥` = parallel):

1. PC-1a
2. PC-2 ∥ PC-3 ∥ PC-6
3. PC-4
4. PC-7
5. PC-8
6. PC-L row S-a

S-a on MyBooks uses the single implicit side `product` (`not built yet` → `product: absent, deliverable: true`): no
registry, no stamp (before arrival nothing runs; after arrival every side is real and `pipeline.sides` exists, so blocks
are stamped all-real and the ledger proves as usual), no `on_substitute`. Waiting for later: PC-5a, PC-5 (S-b
proofs), PC-1b (S-b standing facts, the S-c `reference_for` row), PC-9a–c (S-c), PC-10. PC-9a may run alongside the
first slice (it touches no first-slice file except `contract.py`, function-disjoint).

**Parallel sets (disjoint owns):** after PC-1a — {PC-2, PC-3, PC-6, PC-9a}: `contract.py` is written by PC-3
(`manifest_provisional`) and PC-9a (`PRECEDENT_REF_RE`, the precedent branch, the `parity` reader) with disjoint
function lists (D-0048); PC-6 only reads `contract`. After PC-3 — {PC-4}. After PC-4 — {PC-5a, PC-7 (also needs PC-2,
PC-6), PC-8 (its `s5.md` part after PC-7)}. After PC-5a — {PC-5}. PC-1b whenever PK0-1, PK0-8 and PC-2 are on main
(function-disjoint with PC-7 and PC-9b in `story_run.py`). PC-9b after PC-7, PC-5a, PC-9a. PC-9c after PC-9a (its
`test_human_reading.py` part after PC-7). PC-10 last.

**Queue lines** (D-0048 form: the later node merges main into its tree first, both sides' pins green, one critic after
the merge):
- `scripts/story_run.py`: `очередь: pre-code/1 PC-2 → PC-7 → PC-9b`; PC-1b owns only `Driver.s0_write_sides` and
  `Driver._keep_sides_answer` (created by PC-2, touched by no other PC node) — function-disjoint with PC-7/PC-9b, merges
  main first.
- `scripts/run_suite.py`: `очередь: PC-4 → PC-5a → PC-9b`.
- `scripts/contract.py`: PC-1a → {PC-3, PC-9a} (function-disjoint) ; PC-1b after PC-1a (same function `story_sides`,
  sequential by `depends`).
- `references/question-prices.json`: `очередь: PC-2 → PC-7`.
- `skills/qa-story/phases/s5.md`: `очередь: PC-7 → PC-8`.
- `agents/qa-requirements-tester.md`: `очередь: PC-8 → PC-9a`.
- `scripts/tests/test_human_reading.py` additions: `очередь: PC-2 → PC-7 → PC-9c`.
- `design/state-exits.md`: `очередь: PC-3 → PC-6` (rows appended; the later merges main first) (N1).
- `scripts/tests/fixtures/judgment-census.json`: `очередь: project-knowledge/1 PK0-1 → PK0-4 → pre-code/1 PC-4 → PC-6 →
  PC-5a` (any other node that finds it must add rows queues after the last) (N2).
- `scripts/brief_pack.py`: `очередь: project-knowledge/1 PK0-2, thinking-roles TR3-5 → TR3-15 → pre-code/1 PC-8`
  (function-disjoint; PC-8 merges main first) (N2).
- `scripts/guard_pre_tool.py`: `очередь: TR3-5, TR3-14, TR3-16 → PK0-8 → pre-code/1 PC-1b` (S4c).
- `scripts/project_knowledge.py`, `references/conductor-actions.json`: `очередь: project-knowledge/1 (every PK0 node
  that writes them) → pre-code/1 PC-1b` — `project_knowledge.py` has one writer at a time.

Hot-file function lists are disjoint: `controller.py` — PC-6 only; `story_run.py` — PC-2 {`s0_note_launch`,
`s0_keep_late_launch`, `launch_flags`, `s0_no_change_entry`, the `s1.no_diff` branch, argparse, `s0_write_sides`,
`_keep_sides_answer`}, PC-7 {`run`, `arrival_step`, `_act_await_implementation`, `_act_awaiting_stopped`,
`dispatch_action`, `until_reached`}, PC-9b {`stage_simple`}, PC-1b {`s0_write_sides`, `_keep_sides_answer`, after PC-2};
`stage_guard.py` — PC-6 only; `run_suite.py` — PC-4 {the `--collect-only` flag and branch}, PC-5a {`build_run_block`,
`reparse_run_block`}, PC-9b {the C8 entry check}.

Live proofs (FR-33), table «Живые доказательства»:

| what | stand / project | provable after | status |
|---|---|---|---|
| S-a: a LOCAL story for a feature MyBooks does not have; the run parks in awaiting, `interim-report.md` names the placeholders; the feature is implemented on a branch; relaunch `--branch` → bind round, pending rows retracted, at least one row `settled_matched`, a delivery verdict | MyBooks stand (RUNBOOK §11) | the first slice (PC-1a, PC-2, PC-3, PC-6, PC-4, PC-7, PC-8) | owed |
| S-b: MyBooks UI with the API mocked; the standing fact recorded through the conductor's `side` subcommand (`--stand <dev> --reality substituted` for `backend`, `product.sides` backend `--deliverable no`) or the launch answer — not by editing `config.json`; a UI story runs to the end, `after_checks`, "Left with you" names the re-pass tests per case; a manual-agent walk of a backend Then reads `on_substitute`; a re-pass with `--side backend=real` turns them `passed_green` | MyBooks stand | PC-5a, PC-5, PC-1b | owed |
| S-c: an older MyBooks tag as a second stand recorded as `environments.reference_for` for `ui` (the `side` subcommand `--reference`); a story "the cart page as before"; gate A shows only differences and gaps; Thens with `precedent reference:` | MyBooks + a second deployment (F-13) | PC-9a, PC-9b, PC-9c, PC-1b | owed; stand set-up is the owner's |

---

## §8 Measurement and the failure detector

Measured per story (producer `report_facts`; FR-51, FR-55, AR-12):
- `provisional_settled_matched / provisional_total` — the share settled without touching the marked line;
- `test_body_edits_at_bind` — lines changed in the bind round outside the marked homes (goal: 0);
- `phase2_cost` — the sessions of dispatches with cause `source_arrived` or purpose `bind` (FR-24: the story's own
  journal), against the story's phase-1 cost and against the median of from-scratch runs of comparable stories (one
  metric per comparison, pt.6b);
- `green_after_bind_only` — tests whose first green is after arrival;
- `on_substitute_count` and `sides_unknown_count` at delivery.

Failure detector of the mechanism (rule 10 (c)):
- in the package: `test_sides_ledger.py` (no `on_substitute` or `sides_unknown` input reads `passed`, for tests and walks),
  `test_awaiting_state.py` (no held story reaches S6 or gate B; a stopped story is terminal), `test_state_exits.py`
  (every new state has a row) — registered as AR-28 / AR-25 detectors in `design/architecture.md` (PC-10);
- in the forge: a calibration check in `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md` (PC-10): over the window's live runs,
  stories with a non-real side whose report says `yes` (must be 0), and stories whose `pipeline.awaiting.since` is
  older than 14 days without `stopped` (listed, not a defect).
- What stops it being skipped (rule 10 (d)): the controller's hold branch in `_next_action_for_state` and the C12
  refusal (code on the path), `stage_guard.rule_awaiting_code` on every dispatch, the S5 precheck family `sides`,
  `check_witness._all_pending`, the ledger branch; the role-side judgments are held by the code critic, the S6
  acceptance and the driver's acceptance (critic question 11).

---

## To agree with the project-knowledge session (t-2142; not edited here)

- `KEYS` gains three rows: `product.sides` (scope project), `environments.sides` (scope stand),
  `environments.reference_for` (scope stand), each with comparator `exact`.
- A second comparator `exact` (function `_exact_form`, element unchanged) is registered beside `role_form`; side names
  are case- and punctuation-sensitive.
- `record_problems` gains a per-key `value` check for the three side keys (words from `references/side-realities.json`);
  its census class (`shape`) is unchanged.
- A pure lister `subjects(root, key, environment=None)` is added; it applies the module's own precedence (latest live
  row by `at`, revoked and unknown-state rows skipped, unparseable `at` loses), so `contract.story_sides` does not
  reimplement it.
- A CLI subcommand `side` and a `references/conductor-actions.json` row; `guard_pre_tool.py` `human_word_check` gets
  `side` in PK0-8's alternation and `HUMAN_WORD_MSG` one clause; `test_guard_project_knowledge.py` gets the `side`
  cases. Queue lines `guard_pre_tool.py: PK0-8 → PC-1b`, `project_knowledge.py: PK0-* → PC-1b`.
- Side rows are written only with `state: known`; a `no_trace` refusal of the driver's write is answered by keeping
  the answer in `pipeline.sides` (the registry stays unwritten).
- PC-10 adds the three side keys and `contract.story_sides` as members of axis 34, which PK0-6 lands; PC-10 depends on
  PK0-6.
- t-2142's queue line and PK0-1's owns name `references/state-exits.md` (SPEC:808, :813); the file in the package is
  `design/state-exits.md` (glob today) — for that session to check.
- When node 3.6 moves `environments[]` to its own file, the reference stand's address moves with it; the
  `environments.reference_for` row keys the stand by name and is unaffected.

---

## Reading trail

Re-read 10.11.2026 for revision 3 (this session; package at `D:/ws1/wt-fbfix\ai-packages\qa-factory\`):

- The critic's verdict `docs/tasks/specs/reviews/20261110-t-2181-plan-critic.md` (1-231, whole); this spec revision 2
  (1-699, whole); t-2142 SPEC `D:/ws1/wt-fbfix\docs\tasks\specs\t-2142-project-knowledge-phase0.md` :355-424
  (registry schema, KEYS + comparator :363-366, states :383-386, precedence :388-390, `state()` error direction
  :403-410, writer + `record_problems` + `no_trace` :412-420), :795-824 (queue lines, PK0-1 owns and "What"), :940-1006
  (PK0-8 guard owns :944-959; PK0-6 AR-3 text :998, axis 34 :999-1001), :1064-1066 (stand names exact, roles by
  `_role_form`), :1077-1087 (later phases; onboarding phase 4 :1084; node 3.6 :1087).
- `scripts/project_knowledge.py` does not exist today (Glob `scripts/project_knowledge.py` → none; the same Glob form
  `scripts/stage_guard.py` found the file).
- `scripts/controller.py` (second read; first read had the verdict's numbers): `PURPOSES` :53-55 (holds `collect`, no
  `bind`, no `reference_walk`); `S5_PLAN` / `s5_part_of` :74-113; `REVIEWER_CAUSES` / `REPAIR_CAUSES` :220-232 (K26 note
  :226-229; no `source_arrived`); `closure_view` :1292, `closure_of` :1327; `projection` :1461; `build_rework_request`
  :3477 (purpose check :3508, cause check :3520; first read :3450/:3481/:3493); `NO_INSTANCE_REASONS` :4397 (as cited by
  revision 2); `_pipeline` :4572, `_project_pipeline` :4580; `_next_action_for_state` :8459 (first read :8351;
  `returned` :8557, `stopped` :8571, `if unlaunched:` :8584 — first read :8476-8484, `closed or held` :8607, the stage
  loop :8639, gate A for i ≥ 5 inside it); its production callers :1982, :4649, :8175, :8284, :9420 and
  `scripts/story_step.py:154`; `ROUTED_OPERATIONS` / `APPLY_OPERATIONS` (first read :8550-8557); `stop_after`,
  `with_stop_after` (first read :8574-8600).
- `scripts/stage_guard.py:1-63` (rules 1–7; rule 3 :16-20; fail-open :51-54; `--stories` = qa-doctor step 4 :61);
  :728-737 (`awaiting_state`, X7-6 — name taken); :739-745 (`rule_order`); :768 (`rule_gate_a`); :788-827
  (`dispatch_errors`, waiver pass and `gate_override`); :853-870 (rule 3 helpers, `MANIFEST_STAGES` :870); :932-938
  (`rule_manifest`); :2832-2904 (`stories`, reads `story_closure` :2884).
- `scripts/hooklib.py:570-614` (`story_closure`; readers listed in its docstring :582; "a decline is an answer" :595-596).
- `scripts/archive_task.py:93-117` (`open_items`: "never reached S9 — parked" :116).
- `scripts/check_witness.py:85-107` (`_all_handed`), :217-223 (`RULES["automation-manifest.json"]`).
  `scripts/validate_artifacts.py:145-157` (`NEXT_STEPS`; :151 is a hint line, not a check — the verdict's Q-a citation
  of it as a requirement is a hint the code critic reads; PC-4's pre-list covers the real readers).
- `scripts/s5_precheck.py:74-98` (`PASSABLE` :81, `WORD_PASSABLE_TAGS` :94), :1883-1904 (`check_run_mapping`, the
  `blocked` excuse :1893-1897), :4030-4099 (`check_manifest` call :4045, the "right after the manifest invariants"
  comment :4046, `AC.blocked_instances` :4057-4059 — the verdict's :4084-4092 is the later loop, `check_run_mapping`
  call :4092).
- `scripts/acceptance.py:410-422` (`blocked_instances`), :744 (`red_by_requirement`), :1320-1332 (`awaits_acceptance`).
- `scripts/window_record.py:76` (imports `blocked_instances`), :449 (`_terminal_runs`), :1040-1057 (the excuse read).
- `scripts/ledger.py:300-523` (`plan_row_state` :348; `pending_implementation` for the whole case :400-401; manual
  handed :442-459; the word order :468-523).
- `scripts/contract.py:4253-4292` (`run_results`; manual checks merged :4285-4291), :4337 (`manual_human_evidence`);
  Grep `def (awaiting|story_sides|manifest_provisional)|\bawaiting\b` found only :1907 and :1950 (the positive control
  of the same search: no reader of these names exists yet).
- `references/artifact-contract-run.md:1-48` (run-report writer `qa-runner` from `run_suite` summaries plus its own
  manual-agent execution :16-17; `manual_checks` :24-25; results reduced by `finalize_task.py` :28-31).
- `references/artifact-contract-automation.md:80-124` (`runs[]` :86-91: every launch, appended by its maker).
- `scripts/finalize_task.py:1-70` (run blocks and manual blocks :2-7, `_blocks` :38-56), :339-378 (`reduce`).
- `scripts/run_suite.py:469` (`build_run_block`), :633 (`write_run_block`), :647 (`reparse_run_block`).
- `scripts/manual_evidence.py` function list (:509 `validate`, :1206 `unprepared_rows`, :1275 `write_block`, :1532
  `record_from_walk`).
- `design/state-exits.md:68-81` (mover-wins :77; slice rows kept by design + `retracted_unresolved` door :81 — the
  verdict cites :75-76, the file reads :77/:81 today).
- `scripts/check_delivery.py:2040-2084` (`build_left_items`, one row per case :2043).
- `scripts/story_run.py:7517-7546` (`ticket_freshness_entry`; closed story → no look :7536), :8003-8037
  (`s0_note_launch` :8007, `s0_keep_late_launch` :8019-8035), :17425-17489 (`run`: `skip_sources_late` :17447, S0 branch
  :17448, `ticket_changed` branch :17453-17457, freshness :17464, `accept_no_trace` :17468, loop :17470).
- `references/stages.json` (Grep: S5 :155 has no `acceptance_by`, `rework_mode: resume` :157; S6 `acceptance_by:
  qa-failure-analyst` :196).
- `references/delivery-verdict-kinds.json` (Grep of `owner` words: product / factory / environment / review).
- `scripts/guard_pre_tool.py:1703` (`HUMAN_WORD_MSG`), :1727 (`human_word_check`), :2242 (`STAND_RECORD_FILES`).
- Test files: Glob found `test_archive_task.py`, `test_oracle_provenance.py`, `test_story_run_freshness.py`,
  `test_stage_guard.py`, `test_check_delivery.py`, `test_manual_evidence.py`, `test_run_suite_mine.py`,
  `test_window_record.py`, `test_s5_precheck.py`; NOT found (created by their node): `test_awaiting_state.py`,
  `test_story_sides.py`, `test_sides_ledger.py`, `test_s5_precheck_sides.py`, `test_provisional.py`,
  `test_interim_packet.py`, `test_story_run_arrival.py`, `test_reference_snapshot.py`, `test_proof_stamp.py`,
  `test_check_witness.py` (each negative with a positive control of the same Glob form in the same call).
  Tests that import `finalize_task`: `test_manual_projection.py` among eight (Grep).
- `D:/ws1/wt-fbfix\plans\builder-rules.md:32-42` (SLOW_TESTS and the CI canon).

Carried from revision 2 (re-read 10.11.2026 by the first designer pass, not re-opened in this round):
`scripts/contract.py:66-90`, `:894`, `:954-961`, `:1625-1654`; `scripts/story_run.py:1-52`, `:2959-2976`,
`:3010-3018`, `:8299-8336`, `:9416-9455`, `:16751-16755`, `:16786-16820`; `scripts/check_delivery.py:2304-2347`;
`scripts/delivery_verdict.py:119`; `scripts/check_traceability.py:59-60`; `scripts/grounding_table.py:54, 710-729`;
`scripts/run_suite.py:1542-1558`; `scripts/manual_capture.py:494-534`; `scripts/validate_artifacts.py:1773-1780`;
`references/coverage-design.md:55-86`; `references/vocabularies.md:14-49`; `references/environments.md:90-107`;
`references/role-commands.json:38-72`; `references/human-questions.md:13-132`; `agents/qa-automator.md:1-84`;
`skills/qa-story/phases/s1.md:325-373`; `skills/qa-onboarding/phases/p4-generate.md:486-519`;
`design/state-exits.md:1-221`; `design/architecture.md:140-170`;
`D:/ws1/wt-fbfix\plans\BACKLOG.md:116`; `D:/ws1/wt-fbfix\plans\piles\stand-and-sources\batch-1-stand-identity.md`.

Drift and analogs noticed (reported, not acted on):
- `controller.py` is being edited in the worktree during the day (line numbers moved by +27 / +108 between two reads);
  every node cites it by function name.
- t-2142 names `references/state-exits.md`; the file is `design/state-exits.md` (in the "to agree" list).
- `controller.PURPOSES` already holds a `collect` dispatch purpose; the new `--collect-only` is a run_suite flag, not a
  purpose — kept apart in §3.2 to avoid a builder conflating them.
- `stage_guard.awaiting_state` (X7-6, "awaits the consumer's acceptance") is a different "awaiting"; the new guard
  function is named `rule_awaiting_code`, and `contract.awaiting` reads only the projected code-wait record.
- `validate_artifacts.NEXT_STEPS["automation-manifest.json"]` (:151) tells the next reader to require
  `independent_run` and `red_probe`; for an all-pending manifest that hint is misleading. Not changed here (a text
  hint; the code critic's charter, PC-8, says what an all-pending review checks); a candidate line for PC-8 if the Lead
  wants it.
