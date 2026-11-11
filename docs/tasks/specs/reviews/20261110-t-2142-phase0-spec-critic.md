# Critic on plan: t-2142 project knowledge, phase 0 spec (one pass)

VERDICT: rework

The spec holds up overall: one registry, kept outside config, written by one writer, with the account value staying in config. FK-1, FK-2,
FK-5, FK-7 and FK-8 are sound on the facts, and the two load-bearing survival claims are true. Seven blocking findings stop it from being
executable as written. In three of them a weaker model would have to choose an approach: S1 (rendering and door), S4 (the asked-row
carrier), S5 (the null outcome). In two a node cannot pass its own witness or owns: S3 (census), S6 (guard). S2 is a behaviour hole: the
person's "not a role of this product" answer is asked again. S7 (the default login) is the most likely wrong outcome. The rework means
bounded edits to the spec text, listed per finding below. It reopens no plan decision В1-В8.

Reviewed: D:/ws2/wt-fbfix/docs/tasks/specs/t-2142-project-knowledge-phase0.md (read whole, 638 lines) at wt-fbfix HEAD 91641bb7b.
All `path:line` below are in D:/ws2/wt-fbfix. PKG = ai-packages/qa-factory.
Scope note: the dispatch's own DoD was used. The plan and the earlier critic report were taken as the spec states them: I did not
re-read them, because the questions are about the spec's fit to the code.

## Findings

### S1 — blocker — §3 (2), §3 (6) card, PK0-4 (U-1 resolved). The cards as written cannot reach the person as cards, and the role card's door matches across roles
Evidence:
- `Rehearsal.add` folds every whitespace run of a message into one space (PKG/scripts/gate_preflight.py:1276). The multi-line card of
  §3 (2) and the confirm card of §3 (6), with their bullet list of three answers, become one line.
- The packet's "After your approval" block shows each PERSON_DECIDES finding as `- [your call] <message>` cut at `BRIEF_CUT = 200`
  (gate_preflight.py:935, :5429-5431). The `fix` (the answers) is printed only for `story_level` rows (:5432-5434). The §3 (2) card is about
  640 characters. Its question ("Which account should the factory use...") starts after character 200, so the packet line cuts off before
  the question.
- `gate_brief._open_item` (PKG/scripts/gate_brief.py:462-477) gives a finding with no `waives` a `words` door: the longest prefix of
  ≤60 characters with no `"` (gate_brief.py:427-457). The spec's message puts the role in quotes after the case list:
  `The cases TC-3 and TC-7 check what the role "auditor"...`. The block is therefore `The cases TC-3 and TC-7 check what the role`.
  - The block is blind to stand and role: a recorded "only this story" for auditor also matches a role card for `admin` that holds the same
    cases (`Rehearsal.add` drops it, :1281-1285). That case reaches zero cards, which breaks the spec's own invariant.
  - The block changes whenever the case list changes, so an answered card comes back after a case is added.
- U-2 resolved: `add(..., subject=f"{stand}-{role}")` gives the id `role_accounts-dev-auditor` (`_id_token` :1131-1135; pattern :1127).
  A role written only in non-ASCII letters folds to `""` and falls back to an ordinal id, which is not stable between rehearsals.

Change to the spec (§3 (2), §3 (6), PK0-4):
- (a) The message is a lead of at most 200 characters that carries the fact and the question: `The stand "dev" has no account for the
  role "auditor", which TC-3 and TC-7 need: which account should the factory use?`. The three answers go into `fix`, and the full card is
  the "Rehearsal of gate A" text.
- (b) Call `self.door(f"role account {stand} {role}", option="any")` (or `waiver_command`) before `add`, so the door is a `line` door
  keyed by the subject, not by the message.
- (c) Pass `subject=f"{stand}-{role}"`, `cases=[...]` and `fact={...}`.
- (d) Replace U-1/U-2 in §0 with these facts.
- (e) `test_card_rendered_in_gate_a_message` asserts that the question sits within the first 200 characters.
- (f) Add `test_story_waiver_for_one_role_does_not_pass_another`.
- (g) Non-ASCII role: either refuse it at `record` and at the card with a door, or use a hash-based subject token. Choose one in the spec.

### S2 — blocker — §2 states × §3 (2). "Not a role of this product" (scope: project) is asked again in the next story
Evidence: the step (2) tie reads only `state(..., "environments.credentials_by_role", stand, role)` (§3 (2), spec lines 315-318). A
`product.roles` row with `not_needed` (written by §3 (3) "not a role of this product") is never consulted. The next story whose designer
declares `{"stand_account": "auditor"}` reads the account state as `unknown` and gets the same role card again. The card carries no
"you said..." line, because that line exists only for `asked` rows. This contradicts the digest ("remember, do not ask again") and FR-7.
The spec also does not say what the roster shows when a `not_needed` row and a config account for the same role exist together (§2 says
only "registry row wins").

Change: add a branch to §3 (2).
- A declared role whose roster state is `not_needed` gets no account card. It gets ONE card per role per packet: `You said in <story> on
  <date> that "auditor" is not a role of this product; TC-3 and TC-7 still need it.` Closed answers: `it is a role after all` (the
  conductor runs `role --state known`, then the account card follows) / `report them as not checked`.
- Add the test `test_not_needed_role_is_not_asked_for_an_account_again`.
- In §2, state that a `not_needed` element with a config account stays out of the roster, while its account `state()` is still `known`
  (config first).

### S3 — blocker — §1 census table, PK0-1..PK0-5 owns. The census fixture and its ratchets are owned by one node and needed by four
Evidence:
- `test_judgment_census.py` C1 requires a row for EVERY function of scripts/*.py (test_judgment_census.py:468). Rows carry `roles`
  (fixture judgment-census.json:6-12), which the spec's table omits.
- Every ceiling is dense and shrink-only:
  - the class counts (`safety: 51`);
  - `blocking_per_role` (`conductor: 467`, `qa-test-strategist: 162`, ...): judgment-census.json:4;
  - the compare, which fails both above AND below the ceiling (test_judgment_census.py:365-373).
- PK0-3 (`notice_from_handoff`, `mark_asked` and their helpers), PK0-4 (`check_role_accounts`) and PK0-5 (`default_login_needed`) all add
  units, but only PK0-1 owns judgment-census.json. PK0-4's witness runs test_judgment_census.py and fails C1.
- PK0-4 and PK0-5 run in parallel and would both have to edit the same fixture rows and the same ratchet object.
- The census classes whole functions. "If the census test counts [the no_trace branch] as a new safety unit" does not decide anything:
  a branch is not a unit.

Change:
- (a) Each node owns judgment-census.json for its OWN rows and its ratchet raise.
- (b) Write the rows with `roles` and class in the spec, per function, including helpers and `main`.
- (c) Name the expected raises in advance (AR-20): `safety` +1 if `record`'s no_trace refusal sits in its own function classed safety
  (recommended: `_closed_by_run(task_root)`, safety/intent); `blocking_per_role.conductor` +k, where k is the new blocking units counted by
  `refusal_registry.sites`.
- (d) Serialize the fixture edit: PK0-4 then PK0-5 (queue line `очередь: PK0-4 → PK0-5` for that one file), or have PK0-1 pre-write the
  rows of every phase-0 function name.

### S4 — blocker — PK0-3 `mark_asked`. The findings it needs are not kept anywhere, and the function that would keep them is not owned
Evidence: §5 PK0-3 reads "`state["last_rehearsal_..."]` findings the packet was built from" (spec line 480). That is a placeholder.
`Driver.rehearse` keeps only `last_rehearsal_doors` (finding id -> waives) and `last_rehearsal_gaps` (PKG/scripts/story_run.py:16027-16040).
A grep of `last_rehearsal_[a-z_]*` in story_run.py finds only those two. Nothing keeps a finding's `fact`, and PK0-3's owns are
`gate_repair` and `gate` only.

Change: add `Driver.rehearse` to PK0-3's owns: keep `state["last_rehearsal_facts"][gate] = [f["fact"] for f in findings if f.get("fact")]`
beside the doors. In `gate()`, bind `shown_facts` the same way `shown_gaps` is bound (:15987), and have `mark_asked` read `shown_facts`.
Name the key in the spec.

### S5 — blocker — PK0-3 handoff field. The null outcome "in the form `handoff.null_outcome_entries` reads" is not implementable
Evidence: `null_outcome_entries` drops every entry whose section is not in `REQUIRED_LISTS` (PKG/scripts/handoff.py:471-500), and
`REQUIRED_LISTS = ("scope",)` (handoff.py:458). Declaring `product_roles` there means:
- editing handoff.py (not owned by PK0-3);
- making the section REQUIRED, which contradicts the §4 edge "`product_roles` absent in an old S3 handoff -> nothing refused"
  (builder-rules 9) and makes every in-flight S3 refusable.

Change: drop the `null_outcome` block for `product_roles` in phase 0. Declare the empty outcome as a template comment plus the charter
paragraph: `[]` = "this story's checks need no particular role". Replace `test_handoff_template_declares_null_outcome` with
`test_template_has_product_roles_section_and_absent_is_legal`. If a form check is wanted later, it is a node that owns handoff.py and
states both worlds (rule 11 (i)).

### S6 — blocker (class completeness, AR-14/FR-56, В8) — no node closes the new recorder to roles
Evidence: the siblings exist and are explicit.
- `guard_pre_tool.human_word_check` closes to every role the commands that record a person's word: `environment_record.py
  record|revoke`, `stand_identity.py record|confirm|...`, `source_exclusions.py --load|--revoke` (PKG/scripts/guard_pre_tool.py:1739-1769,
  message :1703-1724).
- `STAND_RECORD_FILES` blocks role writes to `records/environment-properties.json` and its siblings (:2240-2242).
- The spec adds `project_knowledge.py account|role|revoke` and `records/project-knowledge.json` to neither. Under FK-7 (a), the strategist
  could still run `project_knowledge.py role --state known` and turn its own inference into a project fact, which is exactly what В8
  forbids. No node owns guard_pre_tool.py.

Change:
- Add to PK0-1 (or a new small node) owns `PKG/scripts/guard_pre_tool.py` (`human_word_check`: a regex
  `project_knowledge\.py[\"']?(?:\s*,\s*|\s+)[\"']?(?:account|role|revoke)(?![\w-])`; `HUMAN_WORD_MSG` sentence; `STAND_RECORD_FILES`
  += `project-knowledge.json`, plus its message) and the guard's test file.
- `show` stays open (FR-39).
- Hot-file note: guard_pre_tool.py is owned by TR3-14 and TR3-16 (both `в работе`, batch-3 rows). Function-disjoint by D-0048
  (`human_word_check` and `STAND_RECORD_FILES` vs `window_file_check`); the later node merges.

### S7 — blocker — §3 (7), FK-3 (a). `default_login_needed` says "no" for a story that needs the default login
Story shape: the manual-agent cases all declare `{"stand_account": "auditor"}`, and one of them needs data seeded first, or the stand has no
auditor account yet and the runner creates one. The default account is then needed, and §3 (7) returns False.
- The runner's charter says "no account on the stand: `http --as default` creating one" (PKG/agents/qa-runner.md:57).
- `auto_actor` says "Seeding under the admin is `--as default`" (PKG/scripts/manual_capture.py:950); its refusal tells the role to use
  "`--as default` for a step the default account makes" (:962, :969).
- No case declares `default` for those steps.
- Gate A would therefore skip the login keys, and S6 `stand_login_problem` would skip the default read. The walk then fails mid-story,
  instead of being asked at the gate (AR-28).
- A second gap in the same function: §3 (7) says it is "used by gate A and S6", but the S6 rule written there is a different one: per
  block, "every screen case declares a non-default account". That is two rules for one fact (AR-19).

Change, in §3 (7):
- Add (e): any case declares a `case_seeds` precondition, or any manual-agent case's account is not `known` on the chosen stand. In both
  cases the default account is needed, because creation and seeding run as default.
- S6 calls the same `default_login_needed(task_root, cfg)` and ANDs it with today's per-block rule; no second rule.
- Add the tests `test_seeded_case_needs_login` and `test_unprovisioned_role_needs_login`.
- Put the hole to the owner as part of FK-3: option (b) as written has the same hole.

### S8 — should-fix — §3 (2) invariant "exactly one card". It is false where the spec leaves today's code, and the registration position is unstated
Evidence:
1. Keys not set for a role the config records: `state()` is `known`, so there is no role card. The per-case card asks for the keys
   (:4486-4489 -> `open_items`), and `_probe_actor` adds a SECOND card for the same unmet account (:1985-1989). The spec's
   `_probe_actor` change applies only "when (stand, role) has a role card", so this pair stays at two (F-13 is not fixed in its class).
2. The gate A checks run in list order: `check_actor_sign_in`, then `check_s5_credentials`, then `check_case_preconditions`
   (gate_preflight.py:5213-5217). The spec puts `check_role_accounts` "wherever gate A checks are listed" with no position. If it runs after
   `check_actor_sign_in`, `_probe_actor` cannot know which subjects were carded. If `check_case_preconditions` must "take carded items out",
   the carded set has to be on `self` before it runs.
3. `_case_checks` lists the items that DID parse from a case whose line has errors (:3903-3907), while `_declared_cases` drops that case
   entirely (:4714-4724). The role check would card roles from a case that the spec says is "not carded" (§3 (2), "A case whose
   preconditions cannot be read -> nothing here").

Change:
- POSITION: `check_role_accounts` is registered BEFORE `check_actor_sign_in` and keeps `self._role_carded = {(stand, role_form)}`.
  INVARIANT: every unmet `stand_account` item and every `_probe_actor` unmet row reaches exactly one PERSON_DECIDES card. The keys-not-set
  pair (per-case + probe) is deduplicated too (the probe adds a note when the per-case card holds that account), or it is queued explicitly
  as a known remainder of F-13.
- The role check skips any case whose `parse_preconditions` returned errors (use `_declared_cases`' rule).
- Extend `test_every_unmet_item_exactly_one_card` to the keys-not-set case and to a case with a partial parse.

### S9 — should-fix — §3 (2) twins and the account door (FR-2)
Evidence: for twins `Admin`/`admin`, `state()` is `unknown` and the role card "asks which". Its first answer, "the names of the two
variables", runs `project_knowledge.py account`, and `record_stand_account` refuses twins: "remove the extra ones by hand"
(project_decisions.py:627-630). The offered door does not work for the receiver.

Change: give the twins card its own text: `name which of "Admin" / "admin" is the account; the other is removed by hand` (the conductor
edits nothing). Or keep twins on today's per-case path (`_stand_account` already says "name one of them exactly", :4476-4478) and have
`check_role_accounts` skip subjects where `role_candidates` > 1. State which. Add `test_twins_answer_door_is_usable`.

### S10 — should-fix — §3 (2) "asked earlier" line: unknown stated as fact (FR-41)
Evidence: an `asked` row is written whenever the card is SHOWN (PK0-3 `mark_asked`). The added line says "the answer then held for that
story only". When the story was abandoned, approved as is, or never answered, that sentence is false.

Change: `You were asked this in LOCAL-7 on 2026-11-12; no lasting answer was recorded then.`

### S11 — should-fix — §4 missing edges
- (a) A story resumed across the upgrade with per-case account cards ALREADY answered (`TC-3: accept as blocked` recorded). Those items now
  leave the per-case card for the role card, which the earlier waiver does not match. The person is asked again in a new form.
  Change: the role card drops a case already waived by its per-case block; a card whose cases are all waived is not raised. Add a test.
- (b) Brand-new project with no `environments[]` row (the owner's word: stands are not asked at onboarding). `_stand_account` returns
  `error` (gate_preflight.py:4466-4470), so the item lands in `broken` and becomes a FACTORY_DEFECT sentence. No role card appears, and
  the CLI's `record_stand_account` refuses with the onboarding door (project_decisions.py:538-540). The §7 sentence for phase 4 ("a new
  project ... learns roles and accounts at gate A of its first stories") is false until phase 3.4.
  Change: §4 row "no stand recorded": the roster still reaches S3 and the confirm card still runs. Accounts are not learnable until phase
  3.4, and the §7 sentence says so.
- (c) The S6 account reader picks "the first stand whose roles the value could mean" across ALL environments
  (story_run.py:13641-13642), not the chosen stand. The §4 row "an answer for `dev` never covers `stage`" is false at S6: a `stage`
  auditor account is used while the `dev` card was asked. Name it as a known divergence (AR-13 sibling), or have PK0-5 read the chosen
  stand there (it owns `stand_login_problem`).
- (d) `--replace`, or a role given as `Auditor` while config holds `auditor`. `record_stand_account` returns the REAL key in
  `result["role"]` (project_decisions.py:631-633). The registry row's `element` must be `result["role"]`, and when the result is `unchanged`
  there is no DD id to print (:635-637). Change §3 (3) (c): `element=result["role"]`; the printed form reads `auditor on dev: already
  recorded (PK-4)` when unchanged.

### S12 — should-fix — §5 witnesses name SLOW_TESTS files (PROJECT.md: a slow file is never run locally)
Evidence (PKG/scripts/slow_tests.json, measured 2026-11-10, threshold 10 s): test_gate_preflight.py 29.4 s (PK0-4, PK0-5);
test_brief_pack_roles.py 19.9 s (PK0-2); test_driver_layers.py 13.2 s (PK0-3); test_install_paths.py 10.5 s (PK0-1); test_handoff.py is
listed too (PK0-3).

Change: the node witnesses are the new test files plus test_environment_record.py, test_judgment_census.py and test_manual_actor.py
(not listed). The slow files go to the batch canon on CI, named as such.

### S13 — should-fix — §3 texts against human-questions.md
- Item 6 (PKG/references/human-questions.md:38): "Every option of the closed set is followed by three lines: `the factory:` ... `you:` ...
  `the story:` ...". The role card (three options), the confirm card (yes / no / leave it) and the not-needed card of S2 have none.
- Row ids: human-questions.md:51-53 forbids "a row id (`TS-14`, ... `TC-`) not explained where it first appears". The role card opens with
  `The cases TC-3 and TC-7` and gives no titles.
- Change: add per-option price lines and explain each case on first mention (title from the case file, as `named_ids` neighbours do).
  `test_texts_pass_human_text` alone does not catch item 6. Quote the three lines into the spec text.

### S14 — note — FK-6 (a) and the conductor road
The confirm card is produced only when `notice_from_handoff` ran at driver gate A entry. On the conductor (skill) road, no noticed rows are
written and no confirm card appears, so the В8 confirmation silently does not happen. Add a §4 row saying so, or call `notice_from_handoff`
from `check_role_accounts` when no row exists. A check writes nothing (FR-45), so prefer the §4 row.

### S15 — note — §2 element comparator for later phases
`_role_form` folds case, `_`, `-` and spaces (gate_preflight.py:802). That is right for roles and wrong for later list facts whose elements
are case-sensitive or punctuation-bearing (an env key name, a URL path, a regulator id like `PCI-DSS` vs `PCI DSS`). Change §2: "elements
are compared by the comparator registered for the key (phase 0: `_role_form` for both keys)". Then a later key needs no schema change.

### S16 — note — §3 (6) position wording
"AFTER the 'question already open' and the old-answer returns (:16534-16537)" cites only the open-question branch. The old-answer return
(:16538-16548), the kept-answer branch (:16549-16564) and `apply_question_answers` (:16566-16571) follow it.
Change: "after line 16571 (the `apply_question_answers` return) and before `gate_entry_steps` (:16572)". The invariant also names (iv):
nothing is written after the person has spoken.

### S17 — note — F-31 is stale and incomplete (most likely to rot)
- Batch 3, read now: TR3-5 `в работе` (owns `brief_pack.py`, `story_run.py`, `handoff_check.py`); TR3-14 `в работе` and TR3-16 `в работе`
  (`guard_pre_tool.py`; TR3-16 also `references/state-exits.md`); TR3-4 `сдано` and TR3-6 `ожидает` (both `references/state-exits.md`);
  TR3-15 shows `ожидает` but has landed rounds (commits 6a3d7c787, 7ec970825, 5854cceb7 touch brief_pack.py).
- F-31 names none of these.
- Change: F-31 lists every file-level overlap.
- See Q8 for the function level.

## Answers by question

### 1. Facts
| fact | result | evidence |
|---|---|---|
| F-1 load/write/next_id/revoke_row, absent = `([], "")`, refusal on unreadable | confirmed | environment_record.py:208-272. `revoke_row` loads and writes with no lock (:261-271), so `project_knowledge.revoke` must hold the PK lock around it: the spec says "every write takes the lock", which covers it if `revoke` counts as a write. State it. |
| F-2 records tracked/carried | confirmed | install-paths.json:14, :55; collect-sets.json:51 (D3 row) |
| F-5 `_stand_account` met only when keys set | confirmed | gate_preflight.py:4438-4490 |
| F-7 `default` reserved, before stand lookup | confirmed | gate_preflight.py:4453-4465 |
| F-10 S6 reads default for any non-device screen block | confirmed | story_run.py:13600-13615 |
| F-11 login keys asked every story | confirmed | gate_preflight.py:3827, :3841-3857 |
| F-12 per-case card path and positions | confirmed | gate_preflight.py:4670, :4681-4690, :4745-4769 |
| F-13 second card from `_probe_actor` | confirmed | gate_preflight.py:1985-1989; checks order :5213-5217 (see S8) |
| F-16 `restore_config` touches only config.json | confirmed | config_contract.py:2303 (target), :2339 (write); only other write is the backup under state/config-reverts :2336-2337. records/ is never touched. |
| F-17 receipt makes a recorded writer; `record_stand_account` leaves one | confirmed | config_contract.py:2160-2180; project_decisions.py:465-478 (receipt with `recorded_at`/`before` only when config exists, :447, :472), :641-644. Caveat: the `unchanged` path returns before `resolve` (:635-637), which is harmless for survival because there was no change to keep. |
| F-18 revert skipped with a sibling in flight | confirmed | config_contract.py:2240-2257, :2300-2302 |
| F-21 `closed_by_run` | confirmed | external_writes.py:189-200 |
| F-24 `gate` binds shown_gaps; gate_repair invariant iii | confirmed | story_run.py:15987; :16534-16537 |
| F-25 `last_accepted_form` | confirmed | brief_pack.py:3147-3155 |
| F-27 census ceilings | confirmed and incomplete | judgment-census.json:4 also carries `blocking_per_role`; dense two-way compare test_judgment_census.py:365-394 (S3) |
| F-31 neighbour status | stale/incomplete | S17 |
| S3 head block position (§3 (1)) | confirmed | brief_pack.py:3431-3438 |
| U-1 | resolved | S1: one line, 200-character cut, `fix` hidden, words door |
| U-2 | resolved | S1: `subject` gives `role_accounts-<stand>-<role>`, readable by FINDING_ID_PATTERN (:1127); non-ASCII role falls back to ordinal |

Does `records/` survive `restore_config`? Yes (F-16). Does `record_stand_account` leave what keeps the pointer? Yes: a complete DD
receipt with `before` and `recorded_at` inside the window. `_kept_pointers` keeps the leaf `/environments/<i>/credentials_by_role/<role>`
(config_contract.py:2191-2208). Residual risk, as a note: the pointer is by index, so a hand reorder of `environments[]` inside the window
would keep the wrong leaf. That is outside phase 0 (В1 node 3.6).

U-1: can a gate A finding with `fact` and `cases` be one card and be answered? `add(**extra)` carries any fields (`cases=` already used at
:4936, :1988), so the data travels. The card's TEXT does not survive as designed (S1). Once message ≤200 characters, answers in `fix`, and
an explicit `door`, the existing packet renders it as an open item with a `line` door. No gate_brief.py change and no unowned node needed.

### 2. Schema §2
- `not_needed` roster row plus a config account for the same role: incoherent behaviour (S2). The roster excludes the role while the
  account reads `known`. A later declared case is never stopped and never told; an undeclared need re-asks.
- `asked` after `known`: `mark_asked` skips `known` subjects. If config later loses the account, `state()` is `unknown` (config first) and
  a later `asked` row supersedes. Coherent.
- Role renamed in config by hand: the old registry `known` row reads `unknown` (config first) and the new key is `legacy_config`. The
  roster shows both names. Harmless, but name it in §4.
- Stand renamed or removed: rows keyed by name are orphaned. Account state is config first, so nothing wrong is believed, and provenance
  and "asked earlier" lines are lost. Acceptable; one §4 row needed.
- Error direction: every adversarial input listed resolves to `unknown`, because the config is the value carrier. Confirmed by reading
  `account_role`, which gives None on twins (gate_preflight.py:828-835), and `load_rows` (environment_record.py:221-231). One input is
  missing: a row whose `at` cannot be parsed. Under "latest by `at`" it must lose, never win; add the test.
- Later phases: lists that grow (regulators, capabilities, project-created kinds) fit `(key, environment, element)` with no change of key
  or file, PROVIDED the comparator is per key (S15) and `record`'s key allow-list is a data row, not a code literal (AR-1). Otherwise every
  phase edits code to admit a key. Change: the allowed keys of phase 0 live in a data row (for example a `project_knowledge` block in a
  references file), or the spec states that phase 1's catalogue replaces the literal. A two-dimensional element (an account per role per
  tenant) would need an element encoding; name it as a later decision, not a phase-0 defect.

### 3. Behaviour (1)-(7)
- (1) Right place, and the invariant (S3 only) is sufficient. Nothing over-asked.
- (2) Right function family, but the position and registration are unstated (S8), and the card and door are not renderable (S1). Twins:
  S9. Not-needed: S2. Breaking the "exactly one" invariant: the keys-not-set pair gives two cards (S8.1); a role card dropped by a
  cross-role waiver gives zero (S1); a partial-parse case is carded by one check and dropped by the other (S8.3).
- (3) The order invariant (config first) is sound. Element spelling and the unchanged print: S11 (d).
- (4) True (Q1).
- (5) Sound. The acting line is one per packet.
- (6) Position wording: S16. Carrier for `asked`: S4. Conductor road: S14.
- (7) The default login is needed where the function says no: S7. AR-28 holds once (e) is added.

### 4. Judgment (AR-29, P27)
- `product_roles` is produced by the role and only recorded as `noticed_unconfirmed` by code. Code never judges it (FK-7 (a) and the
  non-goal "no S3 exit refusal on content"): xref/data, acceptable.
- The tie (a case declaration holds a case): code joins declarations, xref.
- The confirm card shows names. The person decides, the conductor reads the words, and code reads none (AR-17): acceptable.
- `_role_form` normalisation is equality after folding, not meaning: xref.
- No check in the spec judges a role's judgment.
- Census class per new unit, as I would write it: `state` / `roster` / `record` / `revoke` / CLI `main` = shape (data);
  `_closed_by_run` = safety (intent); `notice_from_handoff` = xref (data); `mark_asked` = shape (data); `check_role_accounts` = xref
  (data); `default_login_needed` = xref (data); the altered `check_case_preconditions` / `_probe_actor` / `check_s5_credentials` /
  `stand_login_problem` keep their class.
- `roles` per row and the ratchet raises: S3.

### 5. Texts
See S13 (item 6; unexplained `TC-` ids), S10 (a false sentence) and S1 (the question beyond 200 characters). The brief lines of §3 (1) are
for a role, not a person; human-questions.md does not bind them, and the extra `human_text` test is harmless. The INFO note of §3 (7) and
the acting line comply.

### 6. Nodes
- PK0-1:
  - owns are missing `guard_pre_tool.py` (S6);
  - `state-exits.md` overlaps TR3-4, TR3-6 and TR3-16 at file level (rows appended, mergeable);
  - witness `test_install_paths.py` is slow (S12);
  - the `collect-sets.json` row: "the form environment-properties.json has" means appending the path to the D3 `paths` list
    (collect-sets.json:51), not a new row. Say so.
- PK0-2: executable. Owns `brief_pack.py` while TR3-5 (`в работе`) owns it (Q8). Witness slow (S12).
- PK0-3:
  - not executable: S4 (rehearse not owned, carrier unnamed) and S5 (null outcome);
  - census rows not owned (S3);
  - witness slow (S12).
- PK0-4:
  - not executable without an approach choice: S1 (render and door), S8 (registration position);
  - census not owned (S3);
  - witness slow (S12).
- PK0-5: S7 changes its rule. Census not owned (S3). It shares gate_preflight.py with PK0-4 (function-disjoint, fine) and shares the census
  fixture (not fine). Witness slow.
- PK0-6: doc witness form is correct (keys quoted, negative control). The AR-3 text edit and index regeneration are right.
- Order: PK0-1 first is right. PK0-4 and PK0-5 must serialize on the census fixture (S3). PK0-3 may run beside them.

### 7. Edges and forks
- Edges missing or wrong: S11 (a)-(d), S14, plus the unparseable `at` (Q2).
- Two stories writing the registry: the lock covers it, provided `record` loads INSIDE the lock (state it: load, decide, next_id and write
  all under the lock).
- Reinstall: correct (carried).
- `--replace`: S11 (d).
- FK-1 (a): sound. The readers in F-5 are untouched and revert-safe via the receipt.
- FK-2 (a): sound, with the S2 consequence to close.
- FK-5: sound. The ids are readable (U-2 resolved), but `stand_login_gate` reading a gate A waiver block is still not built, so phase 3.1
  stands.
- FK-7 (a): sound ONLY with S6 (otherwise the role can bypass it).
- FK-8 (a): sound. The collision with `test_data.accounts_by_role` is as stated (manual_capture.py:731 reads it per the spec; not re-read).
- FK-3:
  - (a) implementable, but has the S7 hole;
  - (b) implementable, with the same seeding hole plus a guest walk for old cases;
  - (c) implementable (S6 only).
- FK-4 "defer": implementable (nothing built).
- FK-6 (a): implementable (§3 (6) as written).
- FK-6 (b): needs a "shown once" marker per element. The `asked` row of key `product.roles` could carry it; not specified.

### 8. Collision
- `brief_pack.py`: PK0-2 adds `s3_roster_lines` and one call in the S3 head (:3431-3438). TR3-5 (`в работе`) edits brief_pack for
  per-dispatch critic findings and TR3-15 for notes. t-1937:261, :329 put those edits in other functions (findings and notes read-first
  lines), so they are function-disjoint as far as the t-1937 text says. Not verified against TR3-5's live branch.
- `story_run.py`: PK0-3 (`gate_repair`, `gate`, plus `rehearse` per S4) and PK0-5 (`stand_login_problem`) vs the batch-3 queue. TR3-5 owns
  `s5_author_round`, TR3-13 `exit_errors`, and TR3-6/9/18 the S5 scheduler functions (t-1937:363). No function-level overlap found. TR3-10
  (`ожидает`) owns `s6.accounts_way` sites; the t-1957 §3.6 walker reads `request_actors` and the guest reading of an empty key
  (story_run.py:3730-3737), while PK0-5 changes only `stand_login_problem`. Disjoint, but the S7 change (seeding as default) is the same fact
  as TR3-10's accounts way, so tell its designer.
- `guard_pre_tool.py` (S6): TR3-14 and TR3-16 are `в работе`. Disjoint functions; merge order per D-0048.
- `references/state-exits.md`: TR3-4, TR3-6, TR3-16 vs PK0-1. Append-only rows.
- `project_decisions.py` / `manual_capture.py`: TR3-10 owns both, and phase 0 edits neither. Disjoint.
- `handoff_check.py`: TR3-5 owns it, and phase 0 edits it only if S5 is not taken. Taking S5 keeps it untouched.

## NOT DONE / UNVERIFIED
- `refusal_registry.py --check`: whether `project_knowledge.py`'s refusals must get registry entries (A24 scans "the dispatch path"). Not
  run, because no code exists. The PK0-1 builder must run `refusal_registry.py --sites` after writing and own the registry if it lists them.
- TR3-5's live branch diff of brief_pack.py was not read (it lives in another worktree).
- The plan and the earlier critic report were not re-read (taken as the spec's §0 cites them).
- `test_data.accounts_by_role` at templates/config.json:67 was not re-read (FK-8 rests on the spec's F-6).

## Trail
Read:
- the spec, whole (1-638);
- PKG/scripts/config_contract.py 2116-2355;
- PKG/scripts/project_decisions.py 370-646;
- PKG/scripts/gate_preflight.py 1125-1316, 1947-2022, 3793-3908, 4438-4490, 4640-4936, 5366-5440;
- PKG/scripts/gate_brief.py 427-539 (plus the def index);
- PKG/scripts/story_run.py 13584-13648, 15959-15992, 16015-16041, 16518-16587;
- PKG/scripts/manual_capture.py 875-972;
- PKG/scripts/manual_evidence.py 1085-1127;
- PKG/scripts/environment_record.py 205-316;
- PKG/scripts/handoff.py 458-500;
- PKG/scripts/guard_pre_tool.py 1700-1769, 2225-2260;
- PKG/scripts/tests/test_judgment_census.py 340-399 (plus the test index);
- judgment-census.json head;
- PKG/references/human-questions.md 20-62;
- PKG/scripts/refusal_registry.py head;
- install-paths.json (grep records);
- collect-sets.json (grep);
- PKG/scripts/slow_tests.json;
- brief_pack.py 3147-3158, 3428-3440;
- external_writes.py 185-202;
- batch-3-parallelnost.md (node table: status and owns columns);
- t-1937 spec (grep brief_pack / state-exits).

Searches (Grep / grep):
- `last_rehearsal_[a-z_]*` in story_run.py: 2 keys (positive control: `last_rehearsal_doors` found at :15983 and :16028).
- `FINDING_ID_PATTERN`: gate_preflight.py:1127, story_run.py:19073.
- `as default` in manual_capture.py and agents: :950, :962, qa-runner.md:57.
- `REQUIRED_LISTS =`: handoff.py:458.
- `source_exclusions|environment_record` in guard_pre_tool.py: :1709-1755, :2231-2241.
- The gate A check list: gate_preflight.py:5213-5217.
- `null_outcome` in the s3 handoff yaml: no hit. The section list (`^[a-z_]*:$`) was the same-shape positive control and found 17 sections.

Reruns: none. A plan review has no witness to rerun. No test suite was run (non-goal).

```json
{
  "verdict": "blocker",
  "blockers": [
    "S1 gate A role/confirm cards: add() folds whitespace (gate_preflight.py:1276), packet cuts at 200 (:935, :5429-5431), fix hidden unless story_level; words door stops at the first quote and matches across roles (gate_brief.py:427-477)",
    "S2 a product.roles not_needed answer is never consulted by check_role_accounts: the same role card is asked again in the next story",
    "S3 judgment-census.json (C1 row per function, two-way dense ratchets incl. blocking_per_role) owned only by PK0-1 while PK0-3/4/5 add units; PK0-4/PK0-5 parallel on one fixture",
    "S4 mark_asked has no carrier: rehearse keeps only doors and gaps (story_run.py:16027-16040); Driver.rehearse not in PK0-3 owns",
    "S5 product_roles null outcome not implementable: null_outcome_entries reads only REQUIRED_LISTS = (scope,) (handoff.py:458, :471-500); making it required breaks in-flight stories",
    "S6 guard_pre_tool human_word_check and STAND_RECORD_FILES not extended: a role could run project_knowledge.py role --state known (breaks FK-7, AR-14)",
    "S7 default_login_needed says no while seeding/creating runs --as default (manual_capture.py:950, :962; qa-runner.md:57); S6 uses a second rule"
  ],
  "fixes": [
    "S1 message is a lead of at most 200 characters with the question; answers in fix; explicit door role account <stand> <role>; subject stand-role; tests for the 200-char cut and the cross-role waiver",
    "S2 add a not_needed branch card with the earlier answer and two closed answers; test",
    "S3 each node owns its census rows with roles; name the safety and blocking_per_role raises; serialize PK0-4 then PK0-5 on the fixture",
    "S4 PK0-3 owns Driver.rehearse: keep last_rehearsal_facts, bind shown_facts in gate(), mark_asked reads it",
    "S5 drop the null_outcome block; template comment plus charter line; test that the section exists and its absence is legal",
    "S6 own guard_pre_tool.py human_word_check regex for account|role|revoke and STAND_RECORD_FILES += project-knowledge.json; show stays open",
    "S7 add (e) case_seeds or a manual role not known means needed; S6 calls default_login_needed; tests",
    "S8 register check_role_accounts before check_actor_sign_in; dedupe the keys-not-set pair; skip partially parsed cases",
    "S9 twins card text with a usable door, or leave twins on the per-case path",
    "S10 asked-earlier line says no lasting answer was recorded",
    "S11 edges: resumed story with answered per-case cards; no environments row; S6 any-stand reader; element is result role; unchanged print",
    "S12 witnesses drop the slow files (gate_preflight, brief_pack_roles, driver_layers, install_paths, handoff) to the CI canon",
    "S13 add price lines per option (human-questions item 6) and explain case ids"
  ],
  "class_completeness": "Siblings by surface: guard closures for person-word recorders (S6, missing), the stand-account second-card pair (S8, half fixed), the S6 any-stand account reader (S11c, not named), the census fixture as a shared registration (S3). The SIBLING_MAP axis 34 member list in PK0-6 is consistent with the plan; guard_pre_tool should be named as an enforcement member.",
  "trail": {
    "read": [
      "wt-fbfix/docs/tasks/specs/t-2142-project-knowledge-phase0.md 1-638",
      "PKG/scripts/config_contract.py 2116-2355",
      "PKG/scripts/project_decisions.py 370-646",
      "PKG/scripts/gate_preflight.py 1125-1316 1947-2022 3793-3908 4438-4490 4640-4936 5366-5440",
      "PKG/scripts/gate_brief.py 427-539",
      "PKG/scripts/story_run.py 13584-13648 15959-15992 16015-16041 16518-16587",
      "PKG/scripts/manual_capture.py 875-972",
      "PKG/scripts/manual_evidence.py 1085-1127",
      "PKG/scripts/environment_record.py 205-316",
      "PKG/scripts/handoff.py 458-500",
      "PKG/scripts/guard_pre_tool.py 1700-1769 2225-2260",
      "PKG/scripts/tests/test_judgment_census.py 340-399",
      "PKG/references/human-questions.md 20-62",
      "PKG/scripts/slow_tests.json",
      "wt-fbfix/plans/piles/thinking-roles/batch-3-parallelnost.md node table"
    ],
    "reruns": []
  }
}
```
