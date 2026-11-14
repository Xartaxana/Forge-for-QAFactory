# Plan critic t-703 — T1r-cards addendum spec (`20261114-told-before-work-t1r-cards-spec.md`)

Reviewer: critic (Opus). Object: the PLAN (no code). Tree: `.claude/worktrees/tbw-t1r`. When the review started HEAD was `10f4478`
with T1r's work uncommitted. During the review it moved to **`705837d` "T1r WIP (t-693): rows landed, STOPPED on K8 / K10 red (page
growth); not accepted, not green"**. Every stage-joints / page / K8 / K10 fact below was read from that content (the uncommitted
diff that `705837d` then committed). `ahead-cards.json`, `role-rules.json`, `role-load.json`, `inject-map.json` and every script
body cited are the same at both commits (705837d's `--stat` names none of them except `stage_joints.py`).

## Verdict: UNFIT (schema: `blocker`). 4 blocking findings, 9 fixes the Lead can make in the text, 2 questions for the owner.

The cards are mapped faithfully (12 ids, 52 segments, verbatim texts, all checked). But four things stop the node as written:
(B1) T1r itself has stopped on K10/K8, and by F-4's own stop clause this node cannot go green. (B2) Appending card words "verbatim"
under M1 puts claims into rows that the target function does not check (AR-29), in 5 of the 12 segments I checked on the body.
(B3) Rule P (F-10) is not deterministic, and on the real tree it STOPs or makes duplicate-check rows for 11 of its 15 segments.
(B4) The gate cannot be passed: the node waits for T1r to merge, and T1r cannot merge green without this node's owns.

---

## Blocking findings

### B1. F-4 (Lead decision) and the measured T1r tree: the node is required to stop at C-9
- Spec line: §8 Lead decisions "F-4 (a) a NAMED raise per role (role, U, H) … a role that would CROSS the ceiling stops the node (no raise
  past the refusal)"; §2.1 C-9; §5 edge "A role whose page grows past K8 / K10".
- Carrier (control re-run, read-only): `python -B …/tbw-t1r/ai-packages/qa-factory/scripts/contract_slices.py --check` at 705837d
  prints K10 red for 6 roles: qa-requirements-tester U 47,004 > H 42,400; qa-test-strategist 60,744 > 42,400 (baseline 46,008);
  qa-automator **95,217** > 68,400; qa-code-critic 83,044 > 68,400; qa-runner 90,414 > 68,400; qa-failure-analyst 86,333 > 68,400.
  K8 is red for 4 pages (qa-runner page 53,086 chars, more than twice L = 26,000) and WARN for 5. The ceiling code is
  `native_context.py:174` `if len(context) > 100000: raise`.
- Why it blocks: H is *defined* as the room left under the 100,000 ceiling (parent §2.6b, `H = 100000 − 26000·P − 5400 − 200`).
  So "over H" and "would cross the ceiling" are the same condition, and every raise F-4 (a) allows is also a stop under F-4's own
  clause. The decision cannot be carried out as written. Read the narrowest way (no project file at all), qa-automator alone is
  95,217 + 5,400 packet + 200 = 100,817 > 100,000: it crosses the ceiling in every project, before this node adds anything.
  This node then adds the au-* segments and the four §4 rows to that same page. The growth is T1r's (`*` rows on every page,
  F-4's own premise), not the cards': the card text is already on every page under `### Not yet in rows` (anchor counts 1, see
  trail), so moving it into rows is close to size-neutral.
- Fix: this is not a text fix. The Lead decides F-4 again on the measured numbers, before any dispatch. One option is F-4 (b):
  narrow T1r's `*` rows behind capability tokens, a T1r fix round. The other is F-4 (c): the owner's word on Appendix A. The cards
  node's C-9 then reads: "K10 is green on entry (fixed in T1r / its fix round); this node's own growth per role is ≤ <named
  bytes>, else stop". → **Question for the owner Q1** (Appendix A: "Decision of the owner needed: yes").

### B2. M1 "append verbatim, over-telling accepted" moves into rows claims that the target check does not make (AR-29)
- Spec lines: §3.0 M1 ("Over-telling is accepted"); the place column "V by §5.2 sentence"; §1 AR-29 row ("rows say what code CHECKS").
- Why it matters more than on the card: `stage_joints.told_text` is "THE composer of what a row tells (the page, the conductor
  section and a refusal all call it)" (`stage_joints.py:571-574`). So an appended clause is printed as the requirement of that check,
  on the page and later in its refusal. "V by §5.2 sentence" checks the *T1r sentence*, not the *card words* added to it.
- Five instances, each on the function body at 705837d:
  1. **br-2 → `validate_artifacts:check_bug_form`**: "with `severity` DERIVED from it by the scale rather than assigned". The body's
     docstring says the opposite: "a severity that differs from it is NOT refused here (F-X7-8 (a))" (`validate_artifacts.py:457-460`).
     The function only checks `impact` in the scale (:480-482).
  2. **cd-3 → `check_case_form`**: "defect_class and basis are inherited from your plan row, never reassigned". The body
     (`:376-406`) checks only that the fields are present (`CASE_FORM_REQUIRED`), covers ⊆ register, and the basis grammar. No plan
     row is read and nothing is compared.
  3. **rt-5 → `check_understanding`**: "its five sections in order". The body (`:1939-1942`) checks that each section is present
     with `any(...startswith(section))`. It does not check order. Compare `check_report_sections` (:1240-1243), which does.
  4. **rt-1 → `check_register`**: "a register of AC alone while a parent feature exists must be `low`". That check is in
     `check_witness._register_checks` (`check_witness.py:55-56`), not in `check_register`. The spec's own "Grep `parent` in
     check_register; absent → STOP" will STOP on a clause whose owner is already known.
  5. **ds-4 → `check_report_left_with_you`**: "Left with you has one item per case in `ledger.json` `left_items`". The body
     (`:1277-1298`) checks only R-n, case id, `To check:` and `Needed:`/`How:` per item. `left_items` is read only by
     `report_facts.py`, `check_delivery.py`, `ledger.py`, `delivery_verdict.py` and others (grep: no hit in `validate_artifacts.py`;
     positive control: the same grep finds `left_items` in `report_facts.py`).
- Clean (no over-claim): sc-2 (F17 body), rt-2 (`grounding_errors`), ru-2 `check_run_report_head` (:1633-1643), ru-3
  `check_run_report_v0` (:2419-2430), ru-4 `check_result_rows` (:2433-2481), ds-3 `check_report_sections` (order checked),
  ds-6 (TEST_REPORT_MAX_BYTES at :1987), fa-1 FLAKY clauses (:2516-2529), au-4 (correctly K: `s5_precheck.py:22-25` "ADVICE …
  never a refusal").
- Fix (text, but every V-by-sentence segment needs a body pass, so I count it as blocking): (1) Rewrite M1: "a segment is appended
  only for the clauses the target function's BODY checks. A clause checked elsewhere goes to the row of the function that checks it
  (by body). A clause no code checks is K." (2) Narrow F-1 (a): over-telling means repeating, never a claim of a check that is not
  there. (3) Before dispatch, the designer (not the builder) splits br-2, cd-3, rt-5, rt-1 and ds-4 at clause level: br-2 "severity
  DERIVED" → K (charter); cd-3 → K; rt-5 "in order" → drop the two words or K; rt-1 parent clause → `check_witness` (through the
  aggregator `exit_gate:witness_errors`, see B3); ds-4 second sentence → the row of the report_facts / check_delivery check. The same
  pass covers every other "V by §5.2 sentence" segment (cd-2, ds-1, ds-2, ds-5, ru-5, ru-6, br-1, br-4, au-1..3, ts-*).
- Sibling outside this node (a NEEDS-WORK note to queue, not this node's): the §5.2 / T1r sentence of `check_case_form` already says
  "the case inherits `defect_class` and `basis` from its plan row" (parent spec line 419). That is the same over-claim, already in
  T1r's rows. Owner: T1r fix round or T7a-1.

### B3. Rule P (F-10) is not deterministic, and on the real tree it stops or makes duplicate-check rows for 11 of its 15 segments
- Spec lines: §3.0 P ("exactly ONE `def` … → `<stem>:<function>` … when it differs from the table, the function found wins"); F-10;
  C-5 ("other → named in the report or STOP").
- I ran rule P as written (AST, every def that contains the token, over the card's sources) at 705837d. Script:
  `…\scratchpad\rulep.py` (output in the trail):
  - **STOP (several defs)**: ts-3 `source_conflict` 3; au-4 `smell` 8; au-5 `covers` 17; ck-2 `cause` 41; ru-1 `witness` 5; ra-3
    `forecast` 3.
  - **Zero defs**: ra-1 `retro-numbers` 0. The table says "none → K", rule P says "zero → STOP": two rules give two answers.
  - **"Function wins" makes a second row for a check that already has one** (P31 / two roads): ts-1 → `planning_contract:validate_plan`
    while `planning_contract:plan` exists; ts-2 → `observation_contract:validate_observation_contract` while
    `coverage_contract:obligations.observation` exists; au-6 → `s5_precheck:check_case_is_oracle` while `s5_precheck:oracle` exists;
    ck-4 → `manifest_put:expectation_change_problems`, which is the automator's `manifest_put:expectation_changes` check, not
    `critic_approval`. The §5.4 family ids (`s5_precheck:<family>`, `planning_contract:plan`, `coverage_contract:…`) are not function
    names, so `<stem>:<function>` can never match them.
  - **No siting node**: sc-3 → `source_preflight:check_source_inventory` and rt-4 → `check_witness:_readiness_form` would be new
    unsited ids under C-5's "other". "named in the report or STOP" does not say who names the node or when that is enough. Note: no
    `check_witness:*` / `source_preflight:*` / `estimate_record:*` row exists. `exit_gate:witness_errors` (sentence-less aggregator,
    roles scout/requirements-tester/strategist/case-designer/runner/failure-analyst) is the existing carrier for check_witness checks,
    and the spec never names it.
  - Further ambiguity: "contains" (substring or token, e.g. `covers` matches `covers_…`); nested defs; "the card's sources" or the
    narrower list in the place column ("Grep `covers` in check_manifest").
- Why it blocks: a node that predictably stops on about 8 segments and makes 4 duplicate rows is not executable by a weaker model
  (PROJECT.md «Командная работа» п. 11). F-10's alternative is the right one here: a short designer pass that places each P segment
  on the body.
- Fix: replace rule P with a table filled in by the designer. Starting points from my run: sc-3 → a new row on
  `source_preflight:check_source_inventory` with a NAMED siting node; rt-4 / ru-1 / rt-1 parent clause → M2 on `exit_gate:witness_errors`
  (one sentence per role: X sub-ids `exit_gate:witness_errors.requirements-tester`, `.runner`), or a named `check_witness:<fn>` row
  with its siting node; ts-1 → M1 on `planning_contract:plan`; ts-2 → M1 on `coverage_contract:obligations.observation`; ts-3 →
  split (oracle_unknown/source_conflict → `planning_contract:contradictions`, the body of `contradiction_errors`; settled branch →
  `coverage_contract:obligations`); au-5 → M1 `s5_precheck:manifest`; au-6 → M1 `s5_precheck:oracle`; ck-2 → the designer reads
  `check_witness.check_code_review` (:280) first; ck-4 → `manifest_put:critic_approval` only for clauses `expectation_change_problems`
  / approval checks, the `test_defect` coupling → K unless a body checks it; ra-1 → K; ra-3 → `estimate_record:facts_problems` with
  a siting node. Rule: an existing family row always beats a new function id.

### B4. The gate cannot be passed: the node waits for T1r to merge, T1r cannot merge green without this node
- Spec lines: §2 "Gate: starts after T1r is merged into main"; Lead decision "the builder starts only after T1r (t-693) is accepted";
  §0.2 A7 ("contract_slices --check may be RED after T1r … this node is the one that turns them green").
- Carrier: 705837d's message says "STOPPED on K8 / K10 red (page growth); not accepted, not green". T1r's non-goals (dispatch §2)
  put `inject-map.json` and `role-load.json` (the only K8/K10 doors) on this node.
- So either T1r merges with `contract_slices --check` red on main (red main, PROJECT.md «Командная работа» п. 12), or it never
  merges and this node never starts. A7 already expects the first and the Gate forbids it.
- Fix: the Lead picks one road and writes it in both specs: (a) T1r's fix round takes the K8 split lines and the K10 move for its OWN
  growth (after B1's re-decision), then merges green, and this node keeps only its delta. Or (b) T1r and T1r-cards land as one
  merge wave, with this node branched from T1r's branch (`wip/tbw-t1r`), not main, and one critic after the merge (the D-0048 pattern).
  Recommend (a): it keeps each node's witness green on its own.

---

## Fixes the Lead can apply to the text (not blocking)

- **X1 (§0.2 A3, A4, A5).** Name what T1r's card does not guarantee and what the tree contradicts. A3: false at 705837d.
  `critic_rollcall:*` is sentence-less with a key-page path leg, so M2 is the road for cc-1; make it primary, not the fallback.
  A4: false at 705837d. T1r regenerated all 12 pages and index files (705837d `--stat`: 24 slice files), against its own non-goal
  "generated pages". A5: `gaps` is 4, not 3 (705837d message), and `unsited` is 150. A2 holds (`exit_gate:grounding`, `:case_identity`
  have no `requirement` and a path leg, anchor `## Outputs`). A1 mostly holds: every §3 target id I checked exists, except that sc-1's
  id is `validate_artifacts:check_phase_json.context-manifest.json` (the spec writes "check_phase_json row of context-manifest.json":
  write the exact id). A6: guaranteed by the merge `10f4478` on the T1r branch, not by T1r's card.
- **X2 (owns vs non-goals, F-7).** Five F19 files are QUARANTINED in `test-layers.json`: `test_ahead_cards_rules.py`,
  `test_case_id_form_texts.py`, `test_context_bundle.py`, `test_report_texts.py`, `test_brief_pack_roles.py`. The owns line (§2) and
  C-10 tell the builder to re-point them, while the non-goals and F-7 forbid editing quarantined files. `siblings:` also says "retire
  `CARD_MAX_BYTES` here" in the quarantined `test_report_titles`… (`test_report_texts.py`). Take them out of owns. State the edge:
  after `cards: {}` they go red in `quarantine-watch`, which brings a `TEST QUARANTINE ALERT` the Lead reports to the owner (CLAUDE.md
  rule 11). Name each one in the report. §11's "not established" item is now established.
- **X3 (C-6).** Three rules have more than one carrier (`case-id-in-briefs-form` 3, `designer-one-case-per-plan-row` 2,
  `merge-keep-only-for-p16-p19` 2; `role-rules.json`, `carriers` is a list). Write: "re-point only the carrier entry whose `file` is
  `references/ahead-cards.json`; the other carriers stay".
- **X4 (rule K / F-2).** "Grep 2-6 words … present → dropped" can drop a clause on a coincidental 2-word match. Use: "its
  distinctive fact (a file, command, field or number) stands in the charter". Name the section: "closing section" does not exist as
  such in the charters. Say whether the line goes under a `kind: craft` marker (it decides craft vs process for
  `process_ratchet_tokens`). Add the edge: an appended charter line must not create a second occurrence of a role-rules anchor in that
  charter (F7 counts once). ck-1 says "(… are on the card)": after the cards are retired, "the card" points at nothing. The designer
  rewords that one parenthesis or drops it. Measured: ck-1, ts-0 and ra-2 are absent from their charters (grep counts 0; positive
  control `add-finding` = 1 in qa-retro-analyst.md), so F-2 appends them to roles already over H (code-critic, strategist).
- **X5 (POSITIONAL, M1 vs door).** Some segments carry their own door words (au-2 "through manifest_put.py", ru-5 "return blocked with a
  reason instead", sc-5 commands). Appended to a row whose `door` differs, the line reads "<sentence + card door> Door: <row door>.":
  two doors on one line. State the invariant: the row keeps ONE door; door words in a segment are dropped when the row's door covers
  them, or they replace the door (named in the report).
- **X6 (K8, C-7).** qa-runner's page is 53,086 chars, so W = 20,800 needs at least `-2` and `-3`. Write: "repeat the split until no
  page reaches W; continuation pages are consecutive (`-2`, `-3`, …); each new line in the same commit".
- **X7 (M3 template).** `roles` is not a row key (`ROW_KEYS`/`OPTIONAL_ROW_KEYS`, `stage_joints.py:67-68`). A top-level `roles` is red
  "unknown key". The producer entry also needs `field` (≥ FIELD_MIN). Write the M3 row as JSON: `{"check", "stages", "requirement",
  "door", "when", "producers": [{"roles": [<role>], "field": "<what is produced>", "told": [{"page": true}], "demands": []}], "joint": null}`.
- **X8 (owns overlap, Q5).** `stage-joints.json` (rows and `told_ratchet.unsited`) is also written by T9c (stage_done:set,
  plan.unmarked_revision), by T4 / T5 / T7a-n (siting lowers `unsited`), and by T1r's fix round (B4). `test_ahead_cards.py` (brief
  block) is touched again by T3b. Add `очередь:` lines (T1r → T1r-cards → T3b; T1r-cards ↔ T9c / T4 / T5 on stage-joints.json), or a
  key-level split in the owns. No overlap with FV1-30b N4/N5: their owns are `s5_precheck.py (refusal_cause; report)`,
  `detector_verdict.py`, `story_step.py`, `window_record.py (_terminal_runs)` and their tests. This node owns none of those, and §4's
  `_sides_provisional` / `_sides_pending` are outside N4's functions.
- **X9 (budget, Q6).** "given" names `stage-joints.json` (210 KB, 7,929 lines) and `role-rules.json` (155 KB) whole, plus
  `stage_joints.py` 68 KB, `contract_slices.py` 61 KB, `role_load.py` 48 KB, `factory-rules.md` 40 KB, the parents and 10 test files.
  That is about 150K tokens before any work, past half of WARN 250K. Narrow it to line ranges (the §3 target rows by id; the 11
  role-rules rows by id). Split the node: **T1r-cards-a** = §3 rows + §4 rows + role-rules re-points + page regeneration + cards
  retired (stage_joints / role_rules / contract_slices green). **T1r-cards-b** = C-10 test re-points + `test_ahead_cards.py`
  page-presence rows + inverted brief rows. These are separable because the tests read pages through `handoff_keys_pages`. K8/K10 move
  to T1r's fix round per B4 (a).

## Questions for the owner

- **Q1 (from B1).** qa-automator's own plugin text is already over the Codex 100,000 limit after T1r's rows (95,217 + 5,400 packet),
  and five more roles are over their headroom. Options: (a) shrink T1r's rows on the pages (rows that every role gets go behind
  capability marks) before going further; (b) remove or raise the Codex limit for the run (Appendix A of the told-before-work spec);
  (c) accept the size, knowing a Codex run would refuse those roles. Recommendation: (a) now, (b) as a separate decision.
- **Q2 (from B2, optional).** The cards today already tell the bug reporter that "severity is DERIVED from impact", and the code
  explicitly does not enforce that (F-X7-8 (a)). Should the role be told it as a rule (charter, craft) or not at all? Recommendation:
  charter line "severity follows the impact scale as a suggestion", no row.

## Item-by-item answers to the dispatch

1. Facts. 12 card ids and texts match `ahead-cards.json` 1-95 verbatim (52 segments, segmentation sums to the whole text of each card).
   Twelve segments checked on the body: sc-2, rt-1, rt-2, rt-5, cd-3, ru-2, ru-3, ru-4, ds-3, ds-4, ds-6, br-2, fa-1 (FLAKY part),
   au-4. Five over-claims (B2). 11 role-rules re-points: ids and anchors match `role-rules.json`. Each anchor counts 1 on today's
   pages (card group). §3.13 holds if the card group is removed and nothing else on the page carries the anchor. §4: `sides.provisional`
   matches `s5_precheck.py:2085-2149` (kind/data list, settles_on side, home marker via `marked_line_hash`, dependents ⊆ then_bindings,
   marker → row). `sides.pending` matches :2152-2179. `profile.none` matches :1790-1797 (`MineRefusal`, onboarding gap).
   `fingerprint` matches `execution_request.py:3714-3724` / `execution_fingerprint.build`, but leaves out one accepted provenance (the
   comment at `build`: "a probe that compared nothing"; `acceptable_provenance` ACCEPTS). It under-claims, it does not lie: optional
   wording fix. `stage_done:set` matches `SETTABLE` 71-86 (T9c's anyway).
2. §0 assumptions: X1 (A3, A4, A5 not guaranteed and false at 705837d; A7 contradicts the Gate, B4).
3. Fork decisions: F-4 not executable (B1). F-10 wrong as written (B3). F-1 (a) needs the AR-29 scope (B2). F-2 grows
   `process_ratchet_tokens` by named rows (C-8 says so), OK with X4. F-5: on the Claude host no role is told less in the window:
   the card is already on every page (`### Not yet in rows`, anchor counts 1), and the page is injected whole. On the Codex host the
   problem is not "less" but "refused" (B1, T1r-caused). No role, stage or sentence lost beyond rt-0 ("Three artifacts, three checks.",
   framing). F-3, F-6, F-7 (with X2), F-8, F-9: no objection.
4. Edges silent: X2 (quarantined readers after `cards: {}`), X4 (charter anchor duplicate), X5 (POSITIONAL two doors), X6 (multi-page
   split), M3 `when: ["always"]` vs rule D shell (state: D replaces `always` with `shell`; `when_exclusive` does not pair them, so either
   is legal, but the spec should say which wins), TEMPORAL "story started before" is stated (OK), `cards: {}` / absent is stated (OK).
5. Executability: no (B3, X7, X9). DoD commands are narrow; `--witness-for` with package-relative paths works (control re-run below).
   `test_stage_joints.py` once is stated. Overlaps: X8.
6. Split: yes (X9).

## Standing questions

- DUPLICATION AND CONSISTENCY: found. Rule P "function wins" creates second rows for checks that already have a family row (B3, four
  ids). M1 + door creates two doors on one line (X5). Grepped: the §3 target ids and the P function ids in `stage-joints.json` at
  705837d.
- CODE QUALITY (plan form): M3 template uses a key the schema refuses (X7). Rule P and the place column disagree (au-5, ra-1).
  "closing section" is undefined (X4).
- ONE ACTION, ONE ROAD (P31, item 12): found. The two-id telling of one check (B3), and the M2-vs-fallback road for `critic_rollcall:*`
  (X1). The exclusion of 5 quarantined readers is a data fact (test-layers.json), not an unjustified exclusion: OK once stated (X2).

## Class completeness (SIBLING_MAP)

Class "a row sentence claims more than the check's body" (AR-29): walked inside the artifact over every M1 / M2 segment I could read
(12 checked, 5 hit). The remaining V-by-sentence segments go to the designer's body pass (B2 fix). The sibling outside the node (the
T1r / §5.2 sentence of `check_case_form`) is queued to the Lead (owner: T1r fix round or T7a-1). Axis 34 (one road): B3 / X5. Axis
"ratchet raise named" (AR-20): C-5 / C-8 name raises. OK except the C-5 STOP ambiguity (B3).

## Trail

Read: the spec under review whole (1-477); dispatch spec §2 (93-205), §5, §8 and the Lead decisions (296-331); mechanism spec
§2.6b (255-277) and Appendix A (686-702), the T7a §5.2 rows (418-459); FV1-30b N4/N5 cards spec owns (105-116, 229-240). At tbw-t1r
(705837d content): `references/ahead-cards.json` whole; `references/role-load.json` whole; `stage-joints.json` (shape; rows for every
§3 target, dumped); `design/role-rules.json` (the 11 rows); `scripts/stage_joints.py` 52-80, 540-1066; `scripts/contract_slices.py`
600-665; `scripts/validate_artifacts.py` 376-695, 1218-1326, 1633-1643, 1750-1754, 1933-2012, 2419-2530; `scripts/check_witness.py`
(def list, 55-56, 121-129); `scripts/s5_precheck.py` 15-40, 2080-2180; `scripts/execution_request.py` 1783-1800, 3705-3728;
`scripts/execution_fingerprint.py` 70-152; `scripts/profile_contract.py` 830-855; `scripts/stage_done.py` 68-100;
`scripts/native_context.py` grep (174); `scripts/manifest_put.py` grep; `scripts/tests/test_ahead_cards.py` 60-94;
`scripts/tests/test-layers.json` (sections of 15 files); `agents/qa-code-critic.md`, `qa-retro-analyst.md`, `qa-test-strategist.md` (greps).

Negative claims and their positive controls:
- "`left_items` is not read in validate_artifacts.py": `grep -n left_items validate_artifacts.py` empty. Control: the same `grep -l` over
  `scripts/*.py` lists `report_facts.py`.
- "no plan-row comparison in check_case_form": body read whole (:376-406), Read tool, not search.
- "no row `check_witness:*` / `source_preflight:*` / `estimate_record:*`": the row-dump script filtered those substrings. The same
  filter printed the `handoff_check:*` and `exit_gate:*` rows (positive).
- "K clauses absent from charters": `grep -c -i` = 0 for 'duplicate green', 'worded, not fixed', 'static review first', '1,911',
  'in fields, not in prose'. Control: `add-finding` = 1 in qa-retro-analyst.md.
- "card readers": `grep -rli "ahead-cards|ahead_card|hand_cards" tests/*.py` lists 13 files incl. test_ahead_cards.py (positive),
  matching F19 + the two owned tests.

Re-runs (all read-only, against the tbw-t1r tree):
- `python -B …/scripts/contract_slices.py --check`: K8 red ×4 (automator 41,365; code-critic 27,878; failure-analyst 38,751; runner
  53,086), K10 red ×6 (numbers in B1), WARN K8 ×5.
- `python -B …/scripts/tests/scenario_walk.py --witness-for references/ahead-cards.json design/role-rules.json references/role-load.json
  references/inject-map.json`: lists test_ahead_cards, test_env_evidence, test_field_producers, test_s7_rejudge, test_role_rules,
  test_audit_rules, test_first_look_wiring, test_role_load, test_brief_pack, test_charters_s5_s9, test_contract_slices,
  test_hooks_wiring.
- `python -B …\scratchpad\rulep.py <scripts>` (rule P simulation): output in B3.
- `git -C …/tbw-t1r log --oneline -1`: `10f4478` at start, `705837d` during the review.

The decision to accept the plan, to re-decide F-4, and to change the T1r gate belongs to the Lead (and Q1 to the owner). This verdict
is an input to that decision.

```json
{
  "verdict": "blocker",
  "blockers": [
    "B1 F-4 is not executable: H is the room under the Codex ceiling, so every K10 raise is also a ceiling crossing that F-4 says stops the node; at 705837d K10 is red for 6 roles and qa-automator U 95,217 + 5,400 packet is over 100,000 with no project file (contract_slices.py --check, native_context.py:174). The Lead decides F-4 again (b or c) before dispatch; Q1 to the owner",
    "B2 M1 verbatim append puts claims into rows that the target body does not check (AR-29; told_text feeds page and refusal, stage_joints.py:571-574): br-2 severity derived vs check_bug_form docstring NOT refused (validate_artifacts.py:457-460); cd-3 inheritance not compared (check_case_form 376-406); rt-5 order not checked (1939-1942); rt-1 parent clause is check_witness.py:55, not check_register; ds-4 left_items join not in check_report_left_with_you",
    "B3 Rule P (F-10) is not deterministic: on the real tree it STOPs on ts-3, au-4, au-5, ck-2, ru-1, ra-3; contradicts the table on ra-1 (zero hits: STOP vs K); and function-wins makes second rows for checks with family rows (ts-1 planning_contract:validate_plan vs :plan, ts-2, au-6, ck-4); sc-3 and rt-4 get no siting node (C-5 other). Replace with a designer-placed table; an existing family row always wins",
    "B4 The gate cannot be passed: the node starts after T1r merges, but T1r stopped red on K8/K10 (705837d) and its only doors (inject-map.json, role-load.json) are this node's owns. Pick T1r fix round takes its own K8/K10, or a joint merge wave from wip/tbw-t1r"
  ],
  "fixes": [
    "X1 rewrite 0.2: A3 false (critic_rollcall:* sentence-less, M2 primary), A4 false (T1r regenerated the 12 pages), A5 gaps 4 and unsited 150, sc-1 exact id validate_artifacts:check_phase_json.context-manifest.json",
    "X2 drop the 5 quarantined F19 files from owns and C-10, and the CARD_MAX_BYTES retire; state their quarantine-watch red and the owner alert",
    "X3 C-6 re-points only the carrier entry whose file is references/ahead-cards.json",
    "X4 rule K: match a distinctive fact, not 2-6 words; name the charter section and the craft or process marker; no second role-rules anchor in a charter; reword ck-1 parenthesis about the card",
    "X5 POSITIONAL: one door per row; door words inside a segment are dropped or replace the door, named in the report",
    "X6 K8: repeat the split until no page reaches W; consecutive -2, -3 pages",
    "X7 M3 template as JSON with roles and field inside the producer entry (top-level roles is an unknown key)",
    "X8 add queue lines for stage-joints.json against T9c, T4, T5, T7a and the T1r fix round, and for test_ahead_cards.py against T3b",
    "X9 narrow given to line ranges and split into T1r-cards-a (rows, re-points, pages, retire) and T1r-cards-b (test re-points)"
  ],
  "class_completeness": "Class row sentence claims more than the check body (AR-29): 12 segments checked on the body, 5 hit; the remaining V-by-sentence segments go to the designer body pass; the sibling outside the node, the T1r / 5.2 sentence of check_case_form claiming inheritance from the plan row, is queued to the Lead (T1r fix round or T7a-1). Axis 34 one road: rule P function-wins duplicates and the M1 two-door line found. AR-20 raises named except the C-5 STOP ambiguity.",
  "trail": {
    "read": [
      "docs/tasks/specs/20261114-told-before-work-t1r-cards-spec.md (whole)",
      "docs/tasks/specs/20261114-told-before-work-t1r-t2-dispatch-spec.md 93-205, 296-331",
      "docs/tasks/specs/20261113-told-before-work-mechanism-spec.md 255-277, 418-459, 686-702",
      "docs/tasks/specs/20261114-fv1-30b-n4-n5-cards-spec.md 105-116, 229-240",
      "tbw-t1r references/ahead-cards.json, references/role-load.json, references/stage-joints.json (target rows), design/role-rules.json (11 rows)",
      "tbw-t1r scripts/stage_joints.py 52-80, 540-1066; contract_slices.py 600-665",
      "tbw-t1r scripts/validate_artifacts.py 376-695, 1218-1326, 1633-1643, 1750-1754, 1933-2012, 2419-2530",
      "tbw-t1r scripts/check_witness.py defs and 55-56, 121-129; s5_precheck.py 15-40, 2080-2180",
      "tbw-t1r scripts/execution_request.py 1783-1800, 3705-3728; execution_fingerprint.py 70-152; profile_contract.py 830-855; stage_done.py 68-100; native_context.py 174",
      "tbw-t1r scripts/tests/test_ahead_cards.py 60-94; scripts/tests/test-layers.json sections",
      "tbw-t1r agents/qa-code-critic.md, qa-retro-analyst.md, qa-test-strategist.md (greps)"
    ],
    "reruns": [
      {"command": "python -B tbw-t1r/ai-packages/qa-factory/scripts/contract_slices.py --check", "result": "K8 red 4 pages (runner 53,086 chars), K10 red 6 roles (automator 95,217 > H 68,400; strategist 60,744 > 42,400 baseline 46,008), WARN K8 5"},
      {"command": "python -B tbw-t1r/ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for references/ahead-cards.json design/role-rules.json references/role-load.json references/inject-map.json", "result": "12 keep files listed (test_ahead_cards, test_role_rules, test_role_load, test_contract_slices, test_field_producers among them)"},
      {"command": "python -B scratchpad/rulep.py <tbw-t1r scripts> (rule P simulation)", "result": "1 def: sc-3, rt-4, ts-1, ts-2, cd-4, au-6, ck-4; several: ts-3 3, au-4 8, au-5 17, ck-2 41, ru-1 5, ra-3 3; zero: ra-1"},
      {"command": "git -C tbw-t1r log --oneline -1", "result": "10f4478 at start, 705837d T1r WIP STOPPED on K8/K10 during review"}
    ]
  }
}
```
