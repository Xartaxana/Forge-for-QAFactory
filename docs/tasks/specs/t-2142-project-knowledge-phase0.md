# t-2142 — project knowledge, phase 0: one fact end to end (product roles and accounts by role) + the answer registry schema — SPEC (designer draft, revision 3)

Designer (Opus), 10.11.2026. Revision 2 by the critic verdict t-2143 (`D:/ws2/wt-fbfix/docs/tasks/specs/reviews/20261110-t-2142-phase0-spec-critic.md`)
and the Lead's decisions on its blockers. Revision 3 by the critic re-review t-2159 (`D:/ws2/yml-text-factory/docs/tasks/specs/reviews/20261110-t-2142-phase0-spec-critic-r2.md`)
and the Lead's directions on its findings N1-N6. Forks are in §6, not closed. Draft for Lead acceptance.
Sources: `D:/ws2/wt-fbfix/plans/project-knowledge-plan.md` (§7 overrides §1-4; owner decisions В1-В8 final),
critic `D:/ws2/wt-fbfix/docs/tasks/specs/reviews/20261110-project-knowledge-plan-critic.md` (C1, C2, C8, C9, C10, C11, C13, C14, C15 bind).
All paths below are in the worktree `D:/ws2/wt-fbfix` (branch `experiment/thinking-roles`), measured at the HEAD the critic read (91641bb7b) or
re-read in this round. PKG = `D:/ws2/wt-fbfix/ai-packages/qa-factory`.
FR-59 is the rule this phase implements ("a policy kept in data: the project's registry, grown by the answers of the person and the roles"; critic C19).

## Lead acceptance (Fable, 10.11.2026)

Draft accepted as the phase-0 spec; critic on the spec is the next gate. **No builder starts until the parallel session finishes** (the
owner's word 10.11.2026, plan §8); before the first dispatch every F-n `path:line` is re-measured against the branch.
Spot-checked by the Lead: the recorded-writers window of `restore_config` (`config_contract.py:1962-1970`), §2, §3, §5, §6.

Forks of §6, decided by the Lead (technical; the owner may reverse any):
- FK-1 (a): the account value stays in config; the registry holds state and provenance.
- FK-2 (a): the roster lives in the registry; AR-3's text changes in this phase.
- FK-5: the gate A / S6 login merge waits for phase 3.1.
- FK-7 (a): a noticed role travels in the S3 handoff field; the strategist gets no new tool.
- FK-8 (a): the account fact is keyed `environments.credentials_by_role`.

Forks that change what a person is asked - DECIDED BY THE OWNER 10.11.2026 ("ок, по рекомендациям"):
- FK-3 (a): the default login is asked when a case declares it, the plan automates something, a manual case declares no account, or
  something cannot be read. Amended in revision 2 ONLY by the S7 addition (the Lead's decision): also when any executed case or the runner
  seeds data or creates a user with the default account, and whenever that cannot be established (§3 (7) items (e), (f)).
- FK-4: "this role is not tested on this stand" is a this-story-only answer until phase 2.
- FK-6 (a): a noticed role left unanswered is asked again in each later story whose plan names it.

Revision 2 accepted by the Lead (Fable, 10.11.2026); the critic's re-review of the fix is the next gate. Forks of revision 2, decided by the Lead:
- FK-9 (a): price lines live on the new cards; the class "stand-gap cards carry no price lines" goes to the pile as a finding (R-2 ii).
- FK-10 (a): the confirm card does not hold the gate - it follows the owner's В8 (silence keeps "not confirmed"); the owner may reverse.
- FK-11 (a): "not a role" rides the existing "decided once" road.
- FK-12 (a): no new closed answer words; the conductor reads the person's words.
- R-1: the raise `judgment-census.json` `ratchet.safety` 51 -> 52 for `project_knowledge._refuse_no_trace` is APPROVED (a refusal that keeps an
  experiment traceless, P8); no other raise is approved - a builder that meets one stops and returns.
- R-2: every remainder listed there becomes a finding file in the pile `project-knowledge` when it is opened. R-3 is gone (revision 3, N2).

Revision 3 accepted by the Lead (Fable, 10.11.2026) after the re-review t-2159 (accept-with-fixes, N1-N5): the five edits were checked by a
key-presence run over this file (a test named per finding; `_c4`, `gate_b_split` owned by PK0-9; a negative control key absent). No third
critic pass (one pass per topic plus one re-review, D-0038). SPEC STATUS: ready to be cut into pile nodes; before the first dispatch every
F-n `path:line` is re-measured (the parallel session changes the same files) and U-5 is settled by PK0-3's test.

## Revision 2 (by verdict t-2143)

| finding | what changed | where |
|---|---|---|
| S1 (blocker) | The role card and the confirm card leave the plain-finding road. Each is a ROW of `Rehearsal.stand_gaps` (the road case-precondition cards use), rendered whole by `gate_brief.stand_gap_card_lines` (no new renderer; `_gap_heading`, `_card`, `stand_gap_form_ids`, `stand_gap_card_lines` get a branch for the two new row scopes). One row per (stand, role), holding exactly that role's cases. The role card's finding is a lead of at most 200 characters with the fact and the question, and its door is `card_door(gap_id)` = block `stand gap: <gap id>`, keyed by the fact; `_exact_gap_view` already makes it exact, so an answer for one role never passes another. Gap id `RA-<stand>-<role>` by the new `role_gap_id` (a hash token when the name folds to nothing: non-ASCII roles are kept, not refused). U-1/U-2 replaced by measured facts F-32..F-36 | §0, §3 (2), §3 (6), PK0-4 |
| S2 (blocker) | A declared role whose roster state is `not_needed` gets NO account question. It rides the "decided once" road (`Rehearsal.covered_gaps`, B-414): one line in the packet names the role, the story and date of the answer and that its cases are reported as not run for that reason; the driver carries those cases as not run (the existing carry); `<id>: ask again` or the person's own words take it back. §2 states that a `not_needed` element with a config account stays out of the roster while its account `state()` is still `known` (config first). Until PK0-9 lands PK0-4 asks the role card for it (toward asking) | §2, §3 (2b), §4, PK0-9 (new) |
| S3 (blocker) | Census rows written per check UNIT by the test's own definition (u1 name family, u2 judge call, u3 refusal site; test_judgment_census.py:16-25, :58) with `roles`; only PK0-1 and PK0-4 add rows; queue `PK0-1 → PK0-4` on the fixture; every other shared file has a queue line (§5). Expected ratchet raises listed for approval: `safety` 51 -> 52, nothing else; any other raise = STOP | §1, §5 general, §6 R-1 |
| S4 (blocker) | The `asked` WRITER is cut: no `mark_asked`, no `Driver.gate`/`Driver.rehearse` change, no "you were asked earlier" line. `asked` stays in the schema as reserved for phase 2 with no producer; `state()` skips such a row | §2, §3, §4, §8, PK0-3 |
| S5 (blocker) | `product_roles` is an OPTIONAL section: declared only as a YAML comment block in the template (not a parsed key, so no field spec can owe it); absent and `[]` both mean "nothing noticed"; no `REQUIRED_LISTS` / `null_outcome` change. The strategist learns it from the S3 brief line (PK0-2) and its charter paragraph (PK0-2) | §3 (6), PK0-2, PK0-3 |
| S6 (blocker) | New node PK0-8: `guard_pre_tool.human_word_check` closes `project_knowledge.py account|role|revoke` to every role (`show` open), `HUMAN_WORD_MSG` gets its sentence, `STAND_RECORD_FILES` += `project-knowledge.json`; own tests; queue after TR3-5, TR3-14, TR3-16 on guard_pre_tool.py | §5 PK0-8 |
| S7 (blocker) | ONE rule `gate_preflight.default_login_needed`, used by gate A AND S6; S6's second rule removed. Added (e) an executed case declares `case_seeds`, (f) an executed manual-agent case declares a role whose account is not `known` on the chosen stand (the runner creates it as default, qa-runner.md:57; manual_capture.py:950, :961-963, :967-969); and unknown -> needed. Error direction: toward asking | §3 (7), PK0-5 |
| S8 | `check_role_accounts` is registered right BEFORE `check_actor_sign_in` (gate_preflight.py:5213) and leaves `self._role_carded` and `self._account_carded`; `_probe_actor` adds a note, not a card, for an account either set holds (the keys-not-set pair included); the role check reads `stand_gaps.declared_preconditions` (drops a case with parse errors, stand_gaps.py:178-180, the same rule as `_declared_cases` :4714-4724). `default` (probe + login keys + per-case) is a named remainder of F-13 | §3 (2), §6 remainders, PK0-4 |
| S9 | Twins (`account_role` -> None with >1 candidates) get their own card variant: the usable door is `myself` (the person removes the wrong entry by hand; the factory edits nothing) or `accept`; never "give the two names" (`record_stand_account` refuses twins, project_decisions.py:627-630) | §3 (2), PK0-4 |
| S10 | Moot: the "asked earlier" line is removed with S4 | §3 (2) |
| S11 | (a) the role card drops a case whose `accept as blocked` is already applied in this story (`stand_gaps.level_applied`, the one reader of applied records by case, :1082-1091); all dropped -> no card. (b) §4 row "no stand recorded" + the §7 sentence corrected (accounts are not learnable until phase 3.4). (c) PK0-5 makes S6 read a role's account on the CHOSEN stand (story_run.py:13641-13642 today searches all). (d) §3 (3): the registry `element` is `result["role"]`; `unchanged` prints `already recorded (PK-n)` | §3 (3), §4, §7, PK0-1, PK0-4, PK0-5 |
| S12 | Witnesses name only new narrow files and fast existing ones; every file of `scripts/slow_tests.json` (test_gate_preflight 29.4 s, test_judgment_census 28.1 s, test_brief_pack_roles 19.9 s, test_brief_pack 13.9 s, test_driver_layers 13.2 s, test_install_paths 10.5 s, test_handoff 35.5 s, test_person_words 24.1 s, test_stand_gap_carry 9.4 s, test_gate_brief_and_retro 33.2 s, test_story_run_*) is named "judged by CI" | §5 |
| S13 | Every option of every new card is followed by `the factory:` / `you:` / `the story:` lines (human-questions.md:38), quoted in §3; every case id is explained on first use by its title (`stand_gaps.what_the_test_does`) | §3 (2), §3 (6), PK0-4 |
| S14 | §4 row: on the conductor (skill) road no noticed rows are written, so no confirm card appears; В8 is then simply not asked in that story (no fact is made either) | §4 |
| S15 | §2: elements are compared by the comparator registered for the key (phase 0: `_role_form` for both keys) in one table `project_knowledge.KEYS`; phase 1's catalogue replaces the literal (§7) | §2, §7 |
| S16 | §3 (6) position: after story_run.py:16571 (the `apply_question_answers` return) and before `gate_entry_steps` (:16572); invariants (iii) and (iv) named | §3 (6), PK0-3 |
| S17 | F-31 rewritten: every file-level overlap with batch 3 (read now, batch-3-parallelnost.md:8, :22-39) | §0 F-31, §5 |

Also taken from the verdict's answers: an unparseable `at` loses (test); `record` and `revoke` load, decide, number and write all under the lock;
the collect-sets change is appending the path to the D3 `paths` list (collect-sets.json:51); `refusal_registry.py --sites` / `--check` in PK0-1's DoD;
a hand-renamed role or stand is a §4 row.

## Revision 3 (by re-review t-2159)

| finding | what changed | where |
|---|---|---|
| N1 (should-fix, near blocker) | `role_gap_id` builds the STAND token and the ROLE token separately. Role token = `_id_token(_role_form(role))` when that fold is lossless (`tok.replace("-", " ") == _role_form(role)`), otherwise `sha1(_role_form(role))[:8]` - so an empty fold (`аудитор`) and a lossy one (`admin-отдел`) both take the hash, whatever the stand's spelling. A lossless token maps back to exactly one role form, so the rule makes the id unique among the packet's roles by construction and stable across packets; a defensive check still widens the hash to 16 hex if two distinct forms of one packet ever give one token. The stand token follows the same lossless-or-hash rule. The finding `subject` is the same `<stand token>-<role token>` (no ordinal `-2`). Twins example ids corrected to `RA-dev-admin` (the form is lower-cased). Tests `test_two_non_ascii_roles_two_gap_ids`, `test_mixed_script_roles_two_gap_ids`, `test_lossless_role_keeps_readable_id` | §3 (2), §4, PK0-4 |
| N2 (blocker; closes S5, settles U-3) | `product_roles` becomes a REAL list section of the S3 template with one row whose three hints carry an OPTIONAL_WORDS word (`optional`), so the role writes it through its sanctioned road (`<dispatch>.values.yaml` / `handoff_check --fix --values`, `_apply_one` accepts a contract path). No change to handoff.py, handoff_check.py, `REQUIRED_LISTS` or `null_outcome` (every list but `scope` may be empty, handoff.py:455-458). Absent section, `[]` and placeholder-only rows all mean "nothing noticed"; `story_roles` skips placeholder rows (`handoff.is_placeholder`). Both worlds stated (a story in flight whose S3 form predates the section). U-3 replaced by the measured fact F-41; R-3 removed. PK0-3 owns the real section; its tests are the three the re-review asks plus the in-flight form; PK0-3 runs `role_load.py --all` before/after | §0 F-41, §3 (6), §4, PK0-1, PK0-3, §6 |
| N3 (should-fix) | Item (f) of `default_login_needed` does not count a role whose roster state is a live `not_needed` (its cases are carried as not run by (2b) and need no login). Every other unknown still counts (Lead direction): an unreadable registry, a revoked or superseded `not_needed`, a role carded at this gate. The re-review's two further exclusions (carded role, all cases dropped) are NOT taken - the Lead kept them on the asking side; listed in §6 R-2 (iii). Tests `test_not_needed_role_does_not_need_default_login`, `test_carded_role_still_needs_default_login`, `test_unreadable_registry_role_needs_default_login` | §3 (7), §4, PK0-5, §6 R-2 |
| N4 (blocker; closes S2) | PK0-9 owns `stand_gaps._c2`, `stand_gaps._c4` and `stand_gaps.gate_b_split` with the behaviour stated in §3 (2b): `_c2` treats `PK_BY` as `ENV_BY` (a commit or image change does not reopen; the stand's address and a withdrawal still do); `_c4` checks a `project_knowledge` property against `project_knowledge.load` (live, not revoked) and `state(product.roles||<element>)` still `not_needed`, else it reopens - the environment record is loaded only for environment-record properties; `gate_b_split` groups a not-a-role carry under its `RA-` gap id as covered at gate B. `carry_environment_properties` re-read (F-42): it does not filter by environment-record facts, so it stays out of the owns. The node's grep now pre-classifies every known hit outside the owned functions (gate_preflight.py:3444 `_environment_cover`, stand_gaps.py:1104 `record_lasting`), and only an UNLISTED hit stops. Tests `test_gate_b_does_not_reask_not_needed_cases`, `test_c4_revoked_pk_row_reopens`, `test_c4_role_no_longer_not_needed_reopens`, `test_c2_commit_change_keeps_pk_carry`, `test_c4_pk_only_carry_ignores_unreadable_environment_record` | §0 F-42, F-43, §3 (2b), §4, PK0-9 |
| N5 (should-fix; closes S11a) | The role card also drops a case whose own earlier stand-gap answer for that item is live: `stand_gaps.decisions(task_root)` holds `accept` for `precondition_gap_id(case, pc_id, shared_precondition_ids(task_root))`, or for the case carry key `<case>`. Existing readers only; a revoked record accepts nothing (contract.py:524-525). Tests `test_case_accepted_on_its_pc_card_is_dropped`, `test_case_carry_live_is_dropped`, `test_revoked_pc_accept_is_not_dropped` | §3 (2), §4, PK0-4 |
| N6 (note) | The `story_run.py` queue line names PK0-9's function list once: `Driver.revoke_environment_properties` only (N4 did not add `carry_environment_properties`, F-42); `take_stand_gap_answers` is touched by no phase-0 node; "function-disjoint, the later merges main" kept | §5 queue lines |
| other notes | S8 wording: the invariant reads "one PERSON_DECIDES card or one decided-once line" (applied). Q3 on R-1: PK0-1 registers any `refusal_registry` entry only on `_refuse_no_trace` or `record_problems`, never on `record`/`main` (applied). Q3 on PK0-8: "no new function in guard_pre_tool.py" stated literally (applied). S6 note (a global option before the subcommand, `project_knowledge.py --task T role`, slips the regex as it does its sibling at :1755): not a text fix - §6 R-2 (iv) | §3 (2), PK0-1, PK0-8, §6 R-2 |

Lead block: its line "R-3: stays a stop-and-return" refers to a request this revision removes by the Lead's N2 direction; the block itself is left
as written (non-goal of this round) - the Lead updates it at acceptance.

## Digest (what this phase proves)

The owner's sentence: a story arrives, the factory looks at the product's roles, sees e.g. four, and the plan takes them into account. Phase 0
proves the whole "ask at first need, remember, do not ask again" scheme on that ONE fact before any catalogue is filled:

1. the S3 strategist gets the roster (product roles + which have an account on the chosen stand) as brief lines and plans by role (its judgment);
2. a role the story's cases need with no account on the chosen stand -> ONE gate A card per (stand, role), holding only that role's cases;
3. the conductor records the answer with its scope (this story / this stand always / project always), the person's words, provenance, revocable;
4. the recorded fact survives `restore_config` at story end;
5. the next story on that stand does not ask and says so in one line; a role the person said is not a product role is not asked again either;
6. a role the strategist noticed in the ticket is recorded `noticed_unconfirmed` and confirmed by the person at gate A (В8);
7. the default login is asked only when the story needs it (gate A and S6, one rule), with the tie stated.

The registry is a new record of the `environment_record` family (C1), written by one function, read by one pure `state()` (C9, FR-45).
Phase 0 needs NO new deferral machinery: gate A is a stop the story makes anyway and comes after S3 and S4 (C8 stays with phase 2 / TR3-10).

---

## §0 Facts (measured; path:line in wt-fbfix)

**The record family the registry is built on (C1)**
- F-1 `environment_record.load_rows / write_rows / next_id / revoke_row`: PKG/scripts/environment_record.py:208-272. Absent file = `([], "")` (:216-218);
  unreadable / not an object / other `schema_version` / no list = `([], <why>)` (:221-231) and writers refuse to write over it (:261-263, :339-341).
  Header ERROR DIRECTION "toward asking (FR-59)" :16-17. `covering`: latest `at` wins, a tie the later row; revoked rows cover nothing (:300-315).
  `write_rows` is one `atomic_json` with NO lock (:235-243); `revoke_row` loads and writes with no lock (:261-271; critic Q1).
- F-2 The environment record lives at `qa-factory/records/environment-properties.json` (:33) and is `carried` (PKG/references/install-paths.json:55);
  `qa-factory/records` is tracked and carried across a reinstall (install-paths.json:14); collect-sets.json:51 is the D3 row whose `paths` list holds it.

**Accounts by role today: the carrier, the writer, every reader**
- F-3 Carrier: `config.json environments[<i>].credentials_by_role["<role>"] = "<USER_KEY> / <SECRET_KEY>"`, names only (PKG/references/environments.md:15).
- F-4 Writer: `project_decisions.record_stand_account` PKG/scripts/project_decisions.py:578-646 = `upsert` + `resolve` (:642-644) with a pointer
  by list INDEX `/environments/{index}/credentials_by_role/<role>` (:641). It returns the REAL key in `result["role"]` (:631-633) and `unchanged`
  with no DD id when the same note is there (:635-637); twins refuse "name one of them exactly, or remove the extra ones by hand" (:627-630).
  Stand pick `_stand_of` :531-550 refuses with no `environments[]` row, door "Record it first (/qa-factory:qa-onboarding, topic 2)" (:538-540) -
  contradicts the owner's word "stands are not asked at onboarding" (phase 3.4).
- F-5 Readers (all through `gate_preflight.account_role`, "the ONE reader of a role name", PKG/scripts/gate_preflight.py:828-835; exact key wins even
  beside a twin, else the only key of the same `_role_form`; twins -> None): `role_candidates` :808-825; `_role_form` :802-805; `account_keys` :747-767;
  gate `_stand_account` :4438-4490 (`default` before the stand :4453-4465; no stand -> `error` :4466-4470; twins -> `unmet` "name one of them exactly"
  :4476-4478; `met` only when both keys are SET :4482-4490); `manual_capture.resolve_actor` PKG/scripts/manual_capture.py:882-934; `auto_actor` :946+;
  `brief_pack._unpaired_actor_lines` PKG/scripts/brief_pack.py:2357-2381, `manual_stand_lines` :2460-2464, `s4_stand_lines` :2520-2522;
  `story_run.Driver.stand_login_problem` PKG/scripts/story_run.py:13584-13648 (the role's stand = the FIRST stand whose roles the value could mean,
  across all environments, :13641-13642); `Driver.walk_env_pair` :3706-3724; `config_contract.environments_account_errors`
  PKG/scripts/config_contract.py:203-234; `project_inventory.py:378`.
- F-6 A different key with a near name exists: `test_data.accounts_by_role` = how the project MAKES users (PKG/references/templates/config.json:67,
  read as such at manual_capture.py:731; not re-read this round). The plan's name `environments[].accounts_by_role` would collide with it.

**How a case declares the role it needs**
- F-7 The case's `preconditions:` line, item `kind: "account"` with `check: {"stand_account": "<credentials_by_role key>"}` (or `{"env": "<KEY>"}`);
  `PRECONDITION_CHECKS` gate_preflight.py:719 include `case_seeds` (the case creates it, never asked: :4557-4561). `default` is reserved
  (`config_contract.reserved_role` :196-200). `manual_evidence._actor_preconditions` copies the `account` items into `request.json actors`
  (PKG/scripts/manual_evidence.py:1087-1105), `request_actors` is the one reader (:1108-1127).
- F-8 The S4 designer and critic are TOLD the stand's roles (`s4_stand_lines`, brief_pack.py:2486-2523). The S3 strategist is told nothing about
  roles or the stand: `s3_strategist_lines` story_run.py:9699-9730; the S3 head in brief_pack.py:3431-3438.
- F-9 The S3 handoff (PKG/handoffs/s3-strategist-to-designer.yaml:51-119) has no field naming roles and no `null_outcome` block (critic's grep;
  re-read whole in revision 3: sections `scope` :51, `not_planned` :78, `grounding` :85, `blast_radius` :92, `manual_policy` :97, `budget` :104,
  `regression_recommendations` :112, `artifacts` :116, `claims` :121, `tried` :145, `tried_note` :150, `unresolved` :152, `blocked` :157).
- F-10 "A case with no account" means two things today: the walker treats an empty account key as a GUEST (story_run.py:3730-3737); S6
  `stand_login_problem` reads the DEFAULT account for any screen case not on a device stand (story_run.py:13600-13615).
- F-10b The default account is the creator and the seeder: qa-runner.md:57 ("no account on the stand: `http --as default` creating one");
  `auto_actor` "Seeding under the admin is `--as default`" (manual_capture.py:950) and its refusals name `--as default` "for a step the default
  account makes" (:961-963, :967-969). No case declares `default` for those steps.

**Where the account is asked today (twins)**
- F-11 Gate A `check_s5_credentials` asks the login keys of EVERY story (gate_preflight.py:3793-3860; env-file-absent card :3817-3822; login keys
  :3827, missing :3841, the card :3855-3857).
- F-12 Gate A `check_case_preconditions` (:4640-4694): `_sort_items` (:4670, def :4745-4769) -> `_card_items` (:4681, def :4800-4829: an open item
  WITH a valid `remedy` becomes a stand-gap ROW plus a one-line pointer finding with `card_door`) -> the rest -> `_case_question` (:4690, def
  :4867-4899, a per-CASE question); a met `stand_account` is `held` and voiced by `not_asked_line` (:916-931, :4691-4692).
  `_declared_cases` (:4696-4727) ADDS a FACTORY_FIXABLE finding for a case whose line has errors and leaves the case out.
  The row id of a carded item is `precondition_gap_id(case_id, item["id"], shared)` (:4813; def :1084-1089: `PC-1`, or `PC-1@TC-007` when the id is
  shared), with `shared = shared_precondition_ids(self.task_root)` (:4661).
- F-13 Gate A `check_actor_sign_in` (:1947-1972) -> `_probe_actor` adds ANOTHER card for the same missing account when `_stand_account` is `unmet`
  (:1985-1989). Gate A step order: `... r.check_case_environment_gaps, r.check_actor_sign_in, ..., r.check_s5_credentials, r.check_case_preconditions,
  ...` (gate_preflight.py:5211-5218).
- F-14 S6 `stand_login_gate` (story_run.py:13708+) asks only when a ready case has policy `ui`; a pass is the waiver block `STAND_LOGIN_BLOCK`.
- F-15 The gate A account card is answered in FREE words; the conductor runs `project_decisions.py stand-account ... --words-file`; "In an experiment
  (`pipeline.no_trace`) write no fact into the config" (PKG/skills/qa-story/phases/s4.md:177-190) - discipline only (F-22).

**The card road (S1; replaces U-1/U-2)**
- F-32 `Rehearsal.add` folds every whitespace run into one space (gate_preflight.py:1276); the packet's "After your approval" block shows a
  PERSON_DECIDES finding as one line cut at `BRIEF_CUT = 200` (:935, :5431) and prints `fix` only for `story_level` rows (:5432-5434). A multi-line
  card therefore never travels as a finding message.
- F-33 A finding with no door gets a `words` door = the longest `"`-free prefix of <= 60 characters of its message (gate_brief.py:427-477); such a
  block is blind to stand and role. `Rehearsal.door` / `card_door(gap_id)` (gate_preflight.py:1193-1201, :1230-1236) instead register the block
  `stand gap: <gap id>` with option `any`; `add` drops a finding only when its doors' blocks are passed (:1281-1287), and `_exact_gap_view`
  (:1238-1250) keeps a `stand gap:` override only when its gap id is EXACTLY one the finding's doors name.
- F-34 `subject=` makes the finding id `<check>-<token>` (`_id_token` :1131-1135: every run outside `[A-Za-z0-9_-]` folds to one `-`, edges stripped;
  `FINDING_ID_PATTERN` :1127); a subject with no ASCII letter or digit folds to `""` and falls back to an ordinal (not stable between rehearsals).
  A subject that keeps SOME ASCII folds to that part only: `_id_token("dev-аудитор")` = `dev`, `_id_token("dev-admin-отдел")` = `dev-admin`
  (re-review N1) - so a "token is empty" test never sees a mixed or a non-ASCII role on an ASCII stand. `_role_form` (:802-805) lower-cases and folds
  runs of spaces, `_` and `-` to one space, so a form holds no `-` or `_`.
- F-35 The card road: a row appended to `self.stand_gaps` (`_card_items` :4814-4823) is mapped by `stand_gaps._gate_a_gaps` (PKG/scripts/stand_gaps.py:216-259;
  pass-through keys `_PASS_THROUGH` :198-199; `the_test` from `what_the_test_does` :92-113, a case's title) and rendered whole by
  `gate_brief.stand_gap_card_lines` (PKG/scripts/gate_brief.py:1690-1742) -> `_card` (:1598-1642; first line `Stand gap: <heading>`, then `the test:`,
  `missing:`, `the fix:` from `stand_gaps.fix_line` :1108-1118), `_gap_heading` (:1484-1505; a `level` branch lists several cases),
  `stand_gap_form_ids` (:883-891, the id the person writes), `_answer_words` (:1645-1687; the closed words of `question-vocabulary.json`
  `stand_gap_words`: `change`/`myself`/`run`/`accept`/`accept always`, read by `read_stand_gap_answers` :900-992). A card's own `remedy.offers` narrows
  the words it takes (`offered_options` :1387-1394). `accept always` is offered only for a row with `property_key` (`lasting_offered` :894-897).
  The stand-gap words carry NO price lines today (question-vocabulary.json:22-41); the exploratory and attachment blocks do (:42-81), rendered
  with `_price_labels` (gate_brief.py:1082-1112).
- F-36 An `accept` on a gap feeds the cases of `stand_gaps.gap_cases(gap)` (its `cases` list, else its `case_id`; stand_gaps.py:406-413) into
  `stand_accept_cases` and the carry (story_run.py:18497-18503, :18577-18579; `write_carries` stand_gaps.py:1002+). The "decided once" road:
  `Rehearsal.covered_gaps` (gate_preflight.py:1164-1166) -> `stand_gaps.covered_a` (:277-281) -> `gate_brief._covered_block` (:1508-1525, `ER.says`
  :1521, the `ask again` line :1522-1524) and the driver's carry `carry_environment_properties` (story_run.py:18965-19009: `write_environment_overrides`
  stand_gaps.py:968-999 with `--by ENV_BY` :989 and `ER.says` :996-998, `covered_entries` :930-940, `write_carries` `ENV_BY` :1036-1037) and revoke
  `revoke_environment_properties` (story_run.py:19027-19062, runs `environment_record.py revoke` :19039). `ENV_BY = "environment-record"` (stand_gaps.py:547).
  `stand_gaps.level_applied(task_root, gap)` (:1082-1091) reads the story's applied `accept_as_blocked` records by case for ANY gap with `cases`.
  `stand_gaps.decisions(task_root)` (:389-391) = `contract.stand_gap_decisions` over `stage_overrides[]` (contract.py:514-535): keyed by gap id or case
  key, the latest live record wins, "a record the person revoked ... accepts nothing" (:524-525). A gate A per-case card answer is stored as
  `stand gap: PC-…` and its carry as `stand gap: <case>` (stand_gaps.py:394-403).

**The S3 handoff write road (N2; replaces U-3)**
- F-41 A role fills a form through `<dispatch>.values.yaml` or `handoff_check --fix --values`; a Write over an existing form is refused and points at the
  values file (guard_pre_tool.py:1052-1111; references/handoffs.md:16; critic r2). `handoff_check._apply_one` writes only a path of the contract's spec
  (`generic in spec or as_list`, handoff_check.py:2391-2408); a path the contract lacks is refused "`<path>` is not a field of `<contract>`" (:2413-2415).
  A contract path the FORM lacks (a form begun on an older package) returns "this form has no line for it and its check does not ask for it - not written"
  with no refusal (:2405-2407, M-7); a line the form holds and the contract no longer does is written as the form holds it (:2409-2412). The CHECK side
  skips a node outside the spec (critic r2: handoff_check.py:1649, :1742, :2609-2614; a case-insensitive search for a refusal of an unknown section over
  handoff*.py gave 0 hits with an 80-line positive control). A placeholder hint carrying an `OPTIONAL_WORDS` word (`optional`, `or omit`, ...,
  handoff.py:35-36) makes its field optional (`_spec_of_value` :434); a hint with `|` whose first part has no space is parsed as a choice (:439-441),
  so an optional hint avoids `|`. Every list except `REQUIRED_LISTS = ("scope",)` may be empty (:455-458). `handoff.is_placeholder(value)` (:662-664) is
  true for `<...>`, `<fill>` and `""`.

**The covered carry and its readers (N4)**
- F-42 `Driver.carry_environment_properties` (story_run.py:18965-19009, re-read in revision 3): takes the covered gaps of `shown_gaps[gate]` that carry
  a `property` DICT (:18979) - no other filter - and the reopened ones; calls `stand_gaps.write_environment_overrides` (:18988), `covered_entries` (:18992),
  `self.accepted_cases`, `_level_remedies` (level gaps only, :19020) and `stand_gaps.write_carries` (:19005). It reads no environment-record row, no `ENV_BY`
  and no `ER.*` itself: every record-specific step is inside the stand_gaps functions PK0-9 owns. It therefore does NOT join PK0-9's owns.
  `revoke_environment_properties` (:19027-19062) hard-codes `environment_record.py revoke` (:19039) and the printed words "taken back from the environment
  record" (:19054).
- F-43 Every reader of `ENV_BY` / `ER.says(` in PKG/scripts (grep, revision 3): stand_gaps.py:547 (the constant), :669 (`_c2`), :711 (`_c4`), :903 and
  :916 (`gate_b_split`), :937 (`covered_entries`), :989 and :998 (`write_environment_overrides`), :1036-1037 (`write_carries`), :1104 (`record_lasting`,
  `ER.says` of an `accept always` row - a role card has no `property_key`, so never reached); gate_brief.py:1521 (`_covered_block`); gate_preflight.py:3444
  (`_environment_cover`, `ER.says(held)` for a case row the environment record covers - a `not_needed` row is appended by `check_role_accounts` itself and
  never enters it). `waiver.py --by` takes any string (default `human`, waiver.py:1574). A grep of `get("by")` over scripts finds the stand-gap `by` read
  only in stand_gaps.py (:480, :669, :711, :903, :916, :1036); person_owned.py:171 counts `by == DRIVER_BY` for a metric (an `ENV_BY` entry is counted
  "interactive" today; a `PK_BY` entry is counted the same - unchanged).
- F-44 `_c2` (stand_gaps.py:637-675): for `by == ENV_BY` only the stand's address (`stand_definition_sha`) and a `withdrawn` row reopen (:669-670).
  `_c4` (:701-732): a carry with a `property` list or `by == ENV_BY` loads `environment_record` (:716-723: unreadable -> reopens), and every named id must
  be a live row covering the subject's CURRENT key (:726-731); no property with `by == ENV_BY` -> "names no record" (:714-715). `gate_b_split`
  (:890-927): `env_keys` = live S5 records with `by == ENV_BY` (:903); none, no project or no gaps -> nothing covered (:905-906); an unreadable record ->
  nothing covered (:908-910); a gap is covered only when its answer is `by == ENV_BY` with a property of subject scope `level` naming a live row under
  `RP-<contour>`, option `accept`, gate A, no `change`, not `ran_red` (:913-923).

**restore_config: what survives, and how a writer becomes "recorded" (C2)**
- F-16 `snapshot_config` keeps the bytes of `qa-factory/config.json` at a fresh story's start (config_contract.py:2018-2045). `restore_config`
  touches ONLY `qa-factory/config.json` (target :2303, write :2339; the only other write is its backup under state/config-reverts :2336-2337).
  Files under `qa-factory/records/` are never reverted.
- F-17 What is kept: pointers changed by a RECORDED writer in the story's window (`_kept_pointers` :2191-2208). Recorded writers = exactly three record
  forms with a `before` copy (`recorded_writes` :2116-2154); a project-decision receipt (`_decision_writes` :2160-2180) is one; `resolve` writes it
  before the config (project_decisions.py:465-478). `record_stand_account` already is one (via `resolve`); its `unchanged` path writes nothing to keep.
- F-18 The revert is skipped when another story is in flight or ran inside the window (config_contract.py:2240-2257, :2300-2302). Decision receipts
  are machine-local (install-paths.json:81).

**Deferred questions today (C8)**
- F-19 `deferrable` is True only when the question names cases (story_run.py:4692-4701); a deferred question is asked only at gate B entry
  (:4763-4797). The no-hold deferral is planned as E8.0 inside TR3-10 (`ожидает`). Phase 0 needs none of it.
- F-20 "Already answered" is per story, by body hash (`already_answered` story_run.py:4628-4639).

**no_trace and comparison runs (C14)**
- F-21 `Driver.no_trace` story_run.py:15487-15502; the one reader is `external_writes.closed_by_run` (PKG/scripts/external_writes.py:189-200).
- F-22 None of the record writers checks it (grep over no_move/external_writes/stand_gaps/environment_record/project_decisions/waiver hits only
  external_writes.py; positive control: the same grep's hit there).

**Stand selection and the gate entry**
- F-23 `environment_selection.select_environment` (PKG/scripts/environment_selection.py:2-22); `stand_gaps.stand_name(task_root)` (stand_gaps.py:148-159):
  the chosen name, else the only stand's name, else `pipeline.environment` or `"this stand"`. `Rehearsal._selected_environment` is the gate's pick.
- F-24 `Driver.gate_repair` (story_run.py:16518-16571+): the open-question return (:16534-16537, invariant iii), the old-kept-answer return
  (:16538-16548), the kept-answer branch (:16549-16564, invariant iv), `apply_question_answers` (:16566-16571), then `gate_entry_steps` (:16572).
- F-25 `brief_pack.last_accepted_form(task_root, stage, role)` (:3147-3155) is the one reader of "the last accepted handoff of a role at a stage".

**Locks, census, map, layers, guard**
- F-26 Lock precedents: `project_decisions.lock` (mkdir lock dir, 10 s, `TimeoutError`) project_decisions.py:193-204.
- F-27 Judgment census PKG/scripts/tests/fixtures/judgment-census.json:3-5: rows `{file, function, class, roles, owner}`; `ratchet` (:4):
  `word-list 0, meaning-proxy 8, meaning 24, safety 51, breach 1, blocks_overrides 8, blocking_per_role {... qa-test-strategist 162, conductor 467}`;
  the compare is dense and two-way (test_judgment_census.py:365-397). A UNIT is (u1) a name matching `UNIT_NAME_RE` (:58: `check_*`, `rule_*`,
  `judge*`, `judged_*`, `_?validate*`, `_?refuse*`, bare `check`/`run`, `*_check`, `*_errors`, `*_problems`), (u2) a judge call, (u3) a refusal site of
  `refusal_registry.sites()` (`deny`/`block`, `raise StateConflict|ValueError`) (:16-25). A unit BLOCKS when it holds a refusal site or sits in a
  `BLOCKING_ENTRY_FILES` file (:67-68: exit_gate, stage_guard, guard_pre_tool, inject_context, stage_done, validate_artifacts, s5_precheck,
  handoff_check, judge_form) or a `stages.json` detector (gate_preflight.py is none of these: stages.json names 11 `.py` hits, none of them it).
  Existing rows touched: `gate_preflight.check_case_preconditions` shape/data (:313), `check_actor_sign_in` safety/intent (:310), `check_s5_credentials`
  safety/intent (:323), `guard_pre_tool.human_word_check` safety/intent (:359), `stand_record_write_check` safety/intent (:370).
- F-28 SIBLING_MAP's last axis is 33 (D:/ws2/wt-fbfix/docs/SIBLING_MAP.md:569).
- F-29 `Driver` methods have rows in PKG/scripts/tests/fixtures/driver-layers.json, read by `test_driver_layers.py` (slow, CI).
- F-30 `question-prices.json` keys are driver questions only; gate A cards are not priced there.
- F-37 `guard_pre_tool.human_word_check` (PKG/scripts/guard_pre_tool.py:1727-1769) closes to every role the commands that record a person's word
  (e.g. `environment_record.py record|revoke` :1755, the regex form `<script>\.py["']?(?:\s*,\s*|\s+)["']?(?:...)(?![\w-])`); message `HUMAN_WORD_MSG`
  :1703-1724. `STAND_RECORD_FILES` (:2242) blocks role writes to the record files (`_stand_record_matcher` :2245-2274, `stand_record_write_check` :2277+).
  The conductor and the driver are not roles there (`from_role` :1766-1768).
- F-38 Slow registry PKG/scripts/slow_tests.json (measured 2026-11-10, slow over 10 s): see the S12 row above. Not listed (fast): test_environment_record.py,
  test_manual_actor.py, test_role_load.py, test_guard_command_text.py, test_stand_gaps.py, test_stand_gap_contract.py, test_stand_gap_remedy.py.
- F-39 role-load.json: `ratchet_tokens.qa-test-strategist` 16718, `process_ratchet_tokens.qa-test-strategist` 15287, `ratchet_slack_tokens` 1000
  (PKG/references/role-load.json:9-37). selftest `--limits`: agents/*.md <= 9000 bytes, references/*.md <= 12000 bytes (selftest.py:18-20).
- F-40 `handoff.REQUIRED_LISTS = ("scope",)` (PKG/scripts/handoff.py:458); `null_outcome_entries` drops any section outside it (:471-500); the
  'not filled' check owes template fields that carry no optional mark (`relaxed_sections` :535-544).

**Neighbours (S17; batch 3 read now, plans/piles/thinking-roles/batch-3-parallelnost.md:8, :22-39)**
- F-31 File-level overlaps with phase 0:
  - `scripts/brief_pack.py`: TR3-5 `в работе`, TR3-15 `ожидает` (critic: rounds landed, commits 6a3d7c787, 7ec970825, 5854cceb7) - batch order
    TR3-5 -> TR3-15 (:8). Phase 0: PK0-2 (`s3_roster_lines` + one call in the S3 head); function-disjoint by t-1937:261, :329 (critic Q8).
  - `scripts/story_run.py`: batch order TR3-2 (`в работе`) -> TR3-17 (`сдано`) -> TR3-6 -> TR3-18 -> TR3-9 -> TR3-10 (`ожидает`), TR3-13 (`сдано`) and
    TR3-5 (`в работе`) other functions (:8). Phase 0: PK0-3 `gate_repair`, PK0-5 `stand_login_problem`, PK0-9 `revoke_environment_properties` -
    no function overlap found (critic Q8); the S7 fact (seeding as default) is TR3-10's "accounts way" too: its designer is told.
  - `scripts/guard_pre_tool.py`: TR3-5, TR3-14, TR3-16 all `в работе`, "different functions" (:8). Phase 0: PK0-8 (`human_word_check`,
    `HUMAN_WORD_MSG`, `STAND_RECORD_FILES`).
  - `references/state-exits.md`: TR3-4 `сдано`, TR3-6 `ожидает`, TR3-16 `в работе`. Phase 0: PK0-1 (rows appended).
  - `scripts/handoff_check.py`: TR3-5. Phase 0 does not touch it (N2: the real template section needs no handoff_check change).
  - `scripts/manual_capture.py` (TR3-8 `принято`, TR3-10), `scripts/project_decisions.py` (TR3-10): phase 0 edits neither.
  - `scripts/gate_preflight.py`, `scripts/stand_gaps.py`, `scripts/gate_brief.py`, `agents/qa-test-strategist.md`, `handoffs/s3-strategist-to-designer.yaml`:
    no batch-3 node writes them (whole table read; the same table lists the files above, positive control).
  UNVERIFIED: in-work batches of OTHER piles were not read; the Lead re-measures before the first dispatch (Lead acceptance block).

UNVERIFIED (tried, not established):
- U-4 The measured role load of the strategist before PK0-2 (role_load.py not run in this round). PK0-2 and PK0-3 measure before and after.
- U-5 (revision 3) Whether `handoff_check._open_rows_for` opens a `product_roles` row on an S3 form begun BEFORE the section existed, or returns the
  M-7 "not written" line (handoff_check.py:2398-2407 read; `_open_rows_for` not read). Both outcomes are acceptable and neither refuses the values file;
  PK0-3's `test_in_flight_form_values_not_refused` pins which one happens and states it in the report.

---

## §1 AR-n touched, census classes, FR sections

**AR-n (design/architecture.md)**

| AR | How phase 0 keeps it | Change check written into the DoD |
|---|---|---|
| AR-3 | the roster is the first project fact stored OUTSIDE config.json (FK-2); AR-3's text changes in this phase | PK0-6 edits AR-3 + regenerates the index; no template key added |
| AR-7 / AR-29 | code carries roles and accounts, never decides which roles a story needs: the strategist does (S3), the case designer declares accounts (S4), the person confirms | census rows below; `test_judgment_census.py` judged by CI |
| AR-9 | every refusal of the registry writer and every card names what it expected and a door the receiver can use (twins: `myself`/`accept`, S9) | PK0-1 test per refusal; PK0-4 `test_twins_answer_door_is_usable` |
| AR-10 | `product_roles` and the roster reach the strategist BEFORE its work (brief line + charter + the template's optional section) | PK0-2 tests; PK0-3 `test_values_write_product_roles`; `role_load.py --all` before/after |
| AR-13 | one reader `project_knowledge.state()` for the registry; account VALUES read only through `account_role` / `account_keys`; applied accepts only through `level_applied`; earlier stand-gap answers only through `stand_gaps.decisions` | PK0-1: `state()` calls `GP.account_role`; PK0-4 reads `level_applied` and `decisions` |
| AR-14 | one writer of the registry (`project_knowledge.record`); config values keep their writer (`record_stand_account` -> `resolve`); roles cannot run the writers (PK0-8) | PK0-1 `test_account_cli_config_then_registry`; PK0-8 tests |
| AR-15 | the registry is the survivor of "a person's answer kept across stories"; the role card reuses the stand-gap card road; the not-a-role answer reuses the "decided once" road at gate A AND gate B (`gate_b_split`, N4); axis 34 in the same commit | PK0-6 axis 34 names every member (guard_pre_tool included); PK0-9 `test_gate_b_does_not_reask_not_needed_cases` |
| AR-16 | the new texts are stand-gap cards in the one card form; price lines per option | PK0-4 `test_texts_pass_human_text`, `test_every_option_has_three_price_lines` |
| AR-17 | free words go to the conductor (s4.md route); code reads only the closed word `accept` / `myself` / `ask again` | PK0-6 text; no phrase list |
| AR-18 | the role card's finding and door have the one output shape (`add` + `card_door`) | PK0-4 `test_finding_id_roundtrip` |
| AR-19 | twins changed together: role card <-> per-case card <-> `_probe_actor` card (PK0-4); gate A login keys <-> S6 default read through ONE function (PK0-5) | each node's report names its twins |
| AR-20 | expected raises listed in §6 R-1 before dispatch; a builder never raises one alone | node DoD "STOP on an unlisted raise" |
| AR-21 | the role's `product_roles` travels in its own handoff through the role's sanctioned values road (a real template section, N2) | PK0-3 `test_values_write_product_roles` |
| AR-22 | producer/reader pairs: strategist `product_roles` -> `story_roles` -> recorder and card; registry rows -> `state()` -> brief/gate; a `PK_BY` carry -> `_c2`/`_c4`/`gate_b_split` | PK0-3 grep of the field name with a positive control; PK0-9 tests per reader |
| AR-23 | empty outcomes declared: `product_roles` absent, `[]` or placeholder-only, empty roster, no stand | PK0-2/PK0-3 tests |
| AR-24 | words whole through `person_words`, printed door | PK0-1 CLI test |
| AR-25 | every state has a way out (`revoke`, a later row, `ask again`) and a `state-exits.md` row | PK0-1 owns the rows; PK0-9 `ask again` test |
| AR-28 | every unknown (unreadable registry, unreadable case, no stand, twins, unknown disposition) errs toward asking | tests named per edge in §5 |

**Judgment census rows (S3).** Rows are written for check UNITS only (F-27: u1/u2/u3). The table lists every unit phase 0 is expected to ADD, with the
node that owns its row; altered existing units keep their class and row. A builder whose code creates a unit not listed here (a name of the family, a
`raise ValueError`, a `deny`/`block`) adds its row in the same commit by the same rule AND reports it; a new unit that BLOCKS (a refusal site) would raise
`blocking_per_role` and is NOT pre-approved: STOP and return (§6 R-1).

| file | function | class | roles | owner | node | why it is not judgment |
|---|---|---|---|---|---|---|
| project_knowledge.py | `record_problems` (u1 `*_problems`: bad key, empty element/environment, empty words for a person, unsafe role characters, unreadable record) | shape | `["conductor"]` | data | PK0-1 | form and presence only; returns reasons, never raises |
| project_knowledge.py | `_refuse_no_trace` (u1 `_refuse*`: the story is `no_trace` by `external_writes.closed_by_run`) | safety | `["conductor"]` | intent | PK0-1 | protects the project from an experiment's trace (P8); returns a reason, never raises |
| gate_preflight.py | `check_role_accounts` (u1 `check_*`) | xref | `["conductor"]` | data | PK0-4 | joins case declarations, the registry's states, the applied accepts and the earlier stand-gap answers; never judges a name |

Not units (no row): `state`, `roster`, `record`, `revoke`, `story_roles`, `acting_line`, `notice_from_handoff`, `default_login_needed`, `role_gap_id`, `covered_says`,
CLI `main` (all named outside `UNIT_NAME_RE`, none holds a refusal site: refusals are returned, the CLI prints and exits with a code). The functions PK0-9 now
also alters - `stand_gaps._c2`, `_c4`, `gate_b_split` - are named outside `UNIT_NAME_RE` and return reasons/lists (no `deny`/`block`/raise): no row, no move.
Altered units, class kept: `check_case_preconditions` (shape/data), `check_actor_sign_in` (safety/intent; `_probe_actor` is its body, no row), `check_s5_credentials`
(safety/intent), `human_word_check` and `stand_record_write_check` (safety/intent).

**FR sections walked (design/factory-rules.md)**: A (FR-1, FR-2, FR-4, FR-57: refusals have doors; the twins card's door works; the card passes by the
person's word); B (FR-6, FR-7, FR-10: one card per fact, price lines, ids explained; a not-a-role answer is not asked again, at gate A or gate B); C (FR-11,
FR-12, FR-13, FR-15, FR-38, FR-49, FR-56: field and roster before work; the role's tool can write the field (FR-11, N2); no phrase list; closed words stay in
the data file); D (FR-58, FR-59: a recorded role is not a code oracle; unknown -> ask); E (FR-23: null outcome `[]`/absent); F (FR-55: "questions avoided by
memory" countable); G (FR-30, FR-32, FR-33 live proof §8, FR-45 the reader and the check write nothing, FR-47). Not touched: FR-46, money F-24/25.

---

## §2 The answer registry (the schema later phases reuse)

**File**: `qa-factory/records/project-knowledge.json`, `{"schema_version": 1, "facts": [ ...rows ]}`, class `carried` (committed, carried byte for
byte across a reinstall, like environment-properties.json). Read and written ONLY by `scripts/project_knowledge.py` through
`environment_record.load_rows / write_rows / next_id / revoke_row` (`list_key="facts"`, id prefix `PK-`).

**Keys (S15)**: one table in `project_knowledge.py`: `KEYS = {"product.roles": {"scope": "project", "compare": "role_form"},
"environments.credentials_by_role": {"scope": "stand", "compare": "role_form"}}`. A key outside `KEYS` is refused by `record_problems`. Elements are
compared by the comparator registered for the key (phase 0: `gate_preflight._role_form` for both); a later key with case-sensitive or punctuation-bearing
elements registers another comparator and needs no schema change. Phase 1's catalogue replaces this literal (§7; AR-1 debt stated there).

**Row fields**

| field | meaning | values |
|---|---|---|
| `id` | `PK-<n>` | `next_id(rows, "PK-")` |
| `key` | the fact's permanent name = its config path when it has one (C5) | a key of `KEYS` |
| `environment` | the stand NAME (never an index, C1); `""` for a project fact | exact string match with `environments[].name` |
| `element` | the list element the row is about; `""` for a one-value fact | phase 0: a role name; for accounts the REAL config key `record_stand_account` returned (S11 d) |
| `state` | see below | `known`, `not_needed`, `noticed_unconfirmed` (written); `asked` reserved |
| `scope` | where the answer holds | from `KEYS`; `story` answers are NOT written here (they stay waivers in `pipeline.json`) |
| `value` | a value the row itself carries, or null | `product.roles`: `{"sign_in": "account" \| "none"}`; accounts: null (FK-1) |
| `provenance` | who said it | `{"source": "person" \| "role" \| "legacy_config", "words", "story", "by": "conductor" \| "driver", "where"}` |
| `at` | ISO UTC time of the row | `environment_record.now_iso()` |
| `revoked_at`, `revoked_words` | the take-back (`revoke_row`) | the row stays |

**States**: `known` (value + provenance), `unknown` (no live row and no config evidence - never stored), `not_needed` (the person said so; phase 0 writes
it only for a `product.roles` element - `scope: project`; the per-stand form is FK-4), `noticed_unconfirmed` (a role noticed it; В8), `asked` (RESERVED for
phase 2: no phase-0 code writes it; `state()` and `roster()` SKIP a row with this state, so a hand-written one never suppresses a question), `unreachable`
(run-scoped per D-0043 / C10: NEVER stored here; phase 0 has no producer). A row whose `state` is outside the list is skipped.

**Identity and precedence**: the subject is `(key, environment, element)`, elements compared by the key's comparator. The subject's state is its latest
live row by `at` (tie: the later row), as `covering` does; a row whose `at` cannot be parsed is the OLDEST (it loses, never wins). Rows are append-only; a
changed answer is a new row; only `revoke` edits a row.

**Account state = config first.** For `environments.credentials_by_role`, `state()` returns `known` exactly when the config's stand of that NAME has
`GP.account_role(roles, element)` with `len(GP.account_keys(note)) == 2` - registry rows only add provenance. A `known` registry row whose config entry is
gone, malformed or twinned reads as `unknown` (the value carrier wins; toward asking); `state()` also returns `twins: [<keys>]` when `role_candidates` > 1 and
`malformed: True` when the entry exists with fewer than two keys. Config-held accounts with no registry row are `known`, `source: legacy_config`.

**Roster = registry rows of `product.roles` UNION legacy evidence.** Elements: live rows of key `product.roles` (`known`, `noticed_unconfirmed`) plus every
role key of `credentials_by_role` on any stand (`known`, `legacy_config`, `sign_in: account`), deduplicated by the comparator (a registry row wins over legacy
evidence). A `not_needed` element is OUT of the roster (listed under `removed`) EVEN WHEN a config account exists for it; that account's own `state()` stays
`known` (config first) - the two readings answer two questions (is it a product role / can the factory sign in as it), and §3 (2b) says which wins at the
gate (S2). `default`, `env:…`, `created:…` (`reserved_role`) are never roster elements.

**ERROR DIRECTION of `state()` (it becomes the input of a gate card - an advice-to-gate promotion)**: toward `unknown` / asking, never toward `known`.
Adversarial inputs that must stay on the asking side (each a test in PK0-1): the file unreadable; another `schema_version`; `facts` not a list; a row with an
empty `key` or `environment` for a stand fact; a revoked row; a row for `Dev` when the stand is `dev`; a `known` account row whose config note now names
one key; two config roles `Admin` / `admin` asked as `ADMIN` (twins -> `unknown` + `twins`); a `noticed_unconfirmed` element (never `known`); a `state`
outside the list; an `asked` row; an unparseable `at`. A `not_needed` row is the ONE input that suppresses an account question, and only through the
covered road that says so in the packet (§3 (2b)); the adversarial inputs for that direction: a revoked `not_needed` row (asks again), a `not_needed` row
for another element of the same comparator form only when it is EQUAL under the comparator, a `not_needed` row superseded by a later `known` row (asks).
`state()` never writes, never raises, and returns the load problem so the caller can say it (FR-41).

**Writer (AR-14)**: `project_knowledge.record(root, *, key, environment, element, state, scope, value, words, source, story, by, where="", task_root=None)`
-> `(row, problem, created)`. Under the lock `qa-factory/state/.project-knowledge.lock` (mkdir, 10 s, as `project_decisions.lock`) it LOADS, checks
(`record_problems`, `_refuse_no_trace(task_root)`), numbers (`next_id`) and writes - all four inside the lock, so two stories never lose a row. Refused,
nothing written, `problem` names why and the door: a key outside `KEYS`; `scope: stand` with an empty `environment`; empty words for `source: person`; an
element with `,` `|` `\` or a line break (the set `project_decisions._refuse_unsafe_role` refuses); an unreadable registry ("nothing was written over it");
a `no_trace` story: "an experiment leaves no trace: the answer stays in this story's words (waiver)". The same live state for the same subject again ->
the existing row, `created: False`. A busy lock -> `TimeoutError` -> CLI exit 2 "the record is busy; run the same command again". `revoke` takes the same
lock around `revoke_row`. "Recorded writer" (C2): `records/` is never reverted (F-16); the account VALUE goes into config only through
`record_stand_account` -> `resolve`, which leaves a decision receipt (F-17).

**Worked example (a project after two stories on `dev`)**

```json
{
  "schema_version": 1,
  "facts": [
    {"id": "PK-1", "key": "product.roles", "environment": "", "element": "guest", "state": "noticed_unconfirmed", "scope": "project",
     "value": {"sign_in": "none"}, "provenance": {"source": "role", "words": "", "story": "LOCAL-7", "by": "driver",
     "where": "R-2: 'a visitor who is not signed in sees the catalogue'"}, "at": "2026-11-12T09:10:00+00:00"},
    {"id": "PK-2", "key": "product.roles", "environment": "", "element": "auditor", "state": "known", "scope": "project",
     "value": {"sign_in": "account"}, "provenance": {"source": "person", "words": "yes, auditor is a read-only role; its account is QA_AUDITOR_EMAIL / QA_AUDITOR_PASSWORD",
     "story": "LOCAL-7", "by": "conductor", "where": ""}, "at": "2026-11-12T09:40:00+00:00"},
    {"id": "PK-3", "key": "environments.credentials_by_role", "environment": "dev", "element": "auditor", "state": "known", "scope": "stand",
     "value": null, "provenance": {"source": "person", "words": "yes, auditor is a read-only role; its account is QA_AUDITOR_EMAIL / QA_AUDITOR_PASSWORD",
     "story": "LOCAL-7", "by": "conductor", "where": ""}, "at": "2026-11-12T09:40:00+00:00"},
    {"id": "PK-4", "key": "product.roles", "environment": "", "element": "superuser", "state": "not_needed", "scope": "project",
     "value": null, "provenance": {"source": "person", "words": "superuser is not a role of the product, it is the stand's maintenance login",
     "story": "LOCAL-8", "by": "conductor", "where": ""}, "at": "2026-11-13T10:05:00+00:00"}
  ]
}
```

With `config.json environments[name=dev].credentials_by_role = {"admin": "QA_ADMIN_EMAIL / QA_ADMIN_PASSWORD", "auditor": "QA_AUDITOR_EMAIL / QA_AUDITOR_PASSWORD"}`
the roster for `dev` is: `admin` (known, legacy_config, account on dev), `auditor` (known, person LOCAL-7, account on dev), `guest` (noticed by a role in
LOCAL-7, not confirmed, no sign-in); removed: `superuser` (the person, LOCAL-8). A later case declaring `{"stand_account": "superuser"}` is not asked for an
account: it is carried as not run with that answer named (§3 (2b)).

**Migration - both worlds (temporal edge, rule 11 (i))**
- Before the file exists (every project today, and a new project): `load_rows` -> `([], "")`; `state()` reads config only; nothing is asked that is not
  asked today, nothing that is recorded is re-asked.
- The move that creates the file: the FIRST successful `record` - the driver's noticed-role recorder at gate A entry (PK0-3) or the conductor's
  `project_knowledge.py account|role` (PK0-1). No install, onboarding or migration step creates it; no existing file is rewritten.
- Existing `credentials_by_role`: stay, read as `legacy_config`. Existing DD rows from `stand-account`: untouched, not migrated. `environment-properties.json`
  and `stand-identity.json`: not read and not written by the registry module (the covered road of PK0-9 keeps reading the environment record for ITS rows).
- After the file exists: `state()` merges as above; an unreadable file -> config-only + the problem line in the brief and the gate note; writes refused.

---

## §3 Behaviour per step

### (1) The strategist gets the roster - `brief_pack.s3_roster_lines(task_root, cfg, env_name)` (new), S3 head
- Called in the S3 block of the head (brief_pack.py:3431-3438), after `walk_lines`, with `env_name = pipeline.environment`; the head is never shrunk.
  POSITION invariant: inside `if stage == "S3"` only - no other stage or role gets roster lines in phase 0 (FR-56; S4 keeps `s4_stand_lines`).
- Reads `project_knowledge.roster(root, cfg, stand)` (pure). Lines (at most 15 elements, then `+N more: qa-factory/records/project-knowledge.json`):
  ```
  Product roles (qa-factory/records/project-knowledge.json and the stand's accounts). Which roles this story's checks need is your judgment:
  - admin: an account on dev
  - auditor: an account on dev (the person, LOCAL-7)
  - guest: no sign-in; noticed in LOCAL-7, not confirmed by the person
  Removed by the person: superuser (LOCAL-8).
  Name every role this story's plan checks in the optional handoff section product_roles (role, sign_in, where in the requirements) - also one
  not listed here; leave it out or write [] when the checks need no particular role.
  ```
  Empty roster: `Product roles: none recorded yet (a project learns them story by story). Name every role this story's plan checks in the optional
  handoff section product_roles; leave it out or write [] when none.` No stand chosen: the roles without the account part and `Stand: not chosen yet -
  which roles have an account is not shown.` Registry unreadable: first line `Product roles: the record of earlier answers cannot be read (<why, 120
  chars>); listed from the stand's accounts only.`
- The charter of `qa-test-strategist` gets ONE craft paragraph (P27): roles are a coverage axis; an access rule is checked for each role it distinguishes,
  as parameters of one check where that is enough (P16); a role the requirements name that the roster lacks goes into the optional handoff section
  `product_roles` (role, sign_in, where), `[]` or no section when the checks need no particular role; a role is never invented from the code (P20).

### (2) A role the story needs with no account -> ONE card per (stand, role) - `gate_preflight.check_role_accounts` (new), on the card road
- Tie: a case of the story declares `{"stand_account": "R"}` (F-7). The strategist's `product_roles` is NOT a tie for asking. A role named only in
  `product_roles` asks nothing about accounts.
- Reading: `stand_gaps.declared_preconditions(self.task_root)` (pure; a case whose `parse_preconditions` returned errors is dropped, stand_gaps.py:178-180 -
  the same rule as `_declared_cases`; S8.3). Never `_declared_cases` (it adds findings). Stand: `self._selected_environment()`; none -> nothing here (the
  existing `_stand_account` "error" path says it, :4466-4470; S11 b). For each declared role R other than `default`, with C = the cases declaring R:
  `st = project_knowledge.state(root, "environments.credentials_by_role", stand_name, R, cfg=self.config)`.
  - roster state of R is `not_needed` -> branch (2b) (PK0-9; until PK0-9 lands: the role card below - toward asking).
  - `st` is `known` -> no role card. When `_stand_account(R, ctx)` is `unmet` (keys not set where the runner reads them) and the precondition step will
    run (`project_root` set and not `gate_rehearsal.skip_preconditions`) -> `self._account_carded[_role_form(R)] = "case"` (the per-case card asks for
    the keys - another fact).
  - otherwise (`unknown`, `twins`, `malformed`) -> drop from C every case already answered in this story (S11 a, N5), by EITHER existing reader:
    (i) `stand_gaps.level_applied(self.task_root, row)` lists it (an `accept as blocked` applied through the per-case QUESTION; `None` = unreadable ->
    drop nothing by this reader); (ii) `d = stand_gaps.decisions(self.task_root)` holds option `accept` for
    `precondition_gap_id(case, item["id"], shared_precondition_ids(self.task_root))` (the case's own per-case stand-gap CARD for this `stand_account`
    item, F-12, F-36) or for the case carry key `case` (`stand gap: <case>`). A revoked record accepts nothing (contract.py:524-525), so a taken-back
    answer drops nothing; an exception in either read -> drop nothing (toward asking). C empty -> no card; else ONE role card row, and
    `self._role_carded.add((stand_name, _role_form(R)))`, `self._account_carded[_role_form(R)] = "role"`.
    INVARIANT (N5): an answer the person already gave about a case's account in this story - in the question form or on its per-case card - is never
    asked again in the role card's form; and an answer that is not live (revoked, or another option than `accept`) never drops a case.
- The role card ROW (appended to `self.stand_gaps`; mapped by `stand_gaps._gate_a_gaps`, rendered by `gate_brief.stand_gap_card_lines`):
  `{"id": role_gap_id(stand, R), "scope": "role", "role": R, "stand": stand_name, "case": "", "cases": C, "kind": "account",
  "check": {"stand_account": R}, "fact": {"key": "environments.credentials_by_role", "environment": stand_name, "element": R},
  "remedy": {"kind": "credential", "where": <the runner's env file>, "where_words": "the project's env file", "change": "two variables for the role R",
  "offers": ["accept"] (twins: ["theirs", "accept"])}, "options": [<the per-option texts and price lines below>], "variant": "missing" | "twins" | "malformed",
  "in_roster": bool, "state": "unmet", "detail": ""}`. No `property_key`: `accept always` is never offered (the registry is the lasting record; FR-10).
- `role_gap_id(stand, role, packet_forms=())` (new, gate_preflight; N1). Two tokens, built separately:
  - role token: `form = _role_form(role)`; `tok = _id_token(form)`; when `tok == ""` OR `tok.replace("-", " ") != form` (the fold lost characters:
    `аудитор` -> `""`, `admin-отдел` -> form `admin отдел`, token `admin`), `tok = sha1(form.encode("utf-8")).hexdigest()[:8]`;
  - stand token: `stok = _id_token(stand)`; when `stok == ""` OR `stok != stand.strip()` (stand names are compared exactly, §2), `stok = sha1(stand.encode("utf-8")).hexdigest()[:8]`;
  - id: `f"RA-{stok}-{tok}"`.
  A lossless role token maps back to exactly one form (a form holds no `-`, F-34), so two distinct forms never share a lossless token, and a lossy form
  never takes a readable token another role could also take: the id is unique per (stand, role) among the packet's roles for ANY spelling, and it does
  not depend on which other roles the packet holds (stable between rehearsals). Defensive guard: `packet_forms` = the `_role_form`s of every role this
  rehearsal cards; if two distinct forms still give one `tok` (a sha1 prefix collision), both take `hexdigest()[:16]`. `PR-` ids (confirm card, stand
  `""`) use the same role token: `"PR-" + tok`.
  INVARIANT (N1): one `RA-…: <word>` answer, and one `stand gap: RA-…` override, can never pass two cards; the same role on the same stand gets the same id
  in every rehearsal.
- The role card's FINDING (S1): `self.add("role_accounts", PERSON_DECIDES, message, self.card_door(gap_id), gap=gap_id, subject=f"{stok}-{tok}",
  cases=C, fact={...})` - the subject is the gap id's own token pair (N1), so the finding id `role_accounts-<stok>-<tok>` is stable and never takes an
  ordinal; message (at most `BRIEF_CUT` = 200 characters after `GAP_SLOT` is replaced; stand and role each clipped to 40):
  `{GAP_SLOT} — a card at this gate: the stand "dev" has no account for the role "auditor", which 2 cases need; which account should the factory use?`
  (twins: `... the stand "dev" records two accounts the role "ADMIN" could mean; which one is it?`). The message carries NO case id, so no per-case
  block can match it; its door is the gap id (F-33), so `stand gap: RA-dev-auditor` never passes `RA-dev-admin`.
- Registration (S8.2): in `run` (gate_preflight.py:5211-5218) `r.check_role_accounts` goes right BEFORE `r.check_actor_sign_in`. POSITION invariant: the
  carded sets exist on `self` before `_probe_actor` and `check_case_preconditions` read them.
- `check_case_preconditions` (:4669-4690): after `_sort_items` and BEFORE `_card_items` (:4681), every open item whose check is `stand_account` with
  `(stand_name, _role_form(spec)) in self._role_carded` leaves `open_items`. `_probe_actor` (:1985-1989): an `unmet` actor whose `_role_form` is a key of
  `self._account_carded` gets `self.note(check, "the sign-in of <actor> waits for the card about its account")` instead of `add`. INVARIANT: every unmet
  non-default `stand_account` item and every `_probe_actor` unmet row reaches exactly ONE PERSON_DECIDES card (role card, per-case card or probe card) or
  one decided-once line (`_environment_cover`, (2b)) - never zero (AR-28), never two (FR-10). `default` stays outside the invariant (§6 remainder).
- How the card reads (the renderer's branch for `scope == "role"`; human-questions items 1-6; ids explained on first use by the title from
  `what_the_test_does`):
  ```
  Stand gap: RA-dev-auditor — the account of the role "auditor" on the stand "dev" (2 cases)
    the test: TC-3 (an auditor opens an order and sees no edit button) and TC-7 (an auditor exports the order list) sign in as "auditor"
    missing:  an account for the role "auditor" on "dev": the project records none, so the factory cannot sign in as it; the other cases of
              this story do not need it and are not held by it
    "auditor" is not among the product's roles yet; an account for it adds it.          (only when not in the roster)
    the answers:
    - the names of the two variables in the project's env file that hold its login and password (never the values), in your own words on a
      line of their own: kept for "dev" from now on, the next stories do not ask
      the factory: a record only, then the gate is rehearsed again; no agent works.
      you: this answer, and putting the login and password into the env file yourself if they are not there yet.
      the story: TC-3 and TC-7 are checked as "auditor"; delivery unchanged.
    - `RA-dev-auditor: accept` - only this story
      the factory: nothing runs for TC-3 and TC-7.
      you: this answer; the next story that needs "auditor" on "dev" asks again.
      the story: TC-3 and TC-7 are reported as not run on this stand; what they check stays unverified and is an open item of the report;
      delivery: not known.
    - "not a role of this product", in your own words on a line of their own
      the factory: a record for the whole project; no agent works.
      you: this answer; to undo it, say so in a later story.
      the story: TC-3 and TC-7 are reported as not run with your words as the reason, and later stories report the cases that need "auditor"
      the same way without asking; delivery: not known.
  ```
  Variant `malformed`: `missing:` reads `the project's settings hold an entry for "auditor" on "dev" that does not name two variables, so the factory cannot
  sign in as it` (the conductor records the names with `--replace`). Variant `twins` (S9) - two answers; the card id is `RA-dev-admin` (the role form is
  lower-cased by `_role_form`, N1), the role is still quoted as the case wrote it:
  ```
    missing:  the project's settings record two accounts the role "ADMIN" could mean on "dev" ("Admin", "admin"), so the factory cannot tell which
    the answers:
    - `RA-dev-admin: myself` - you remove the wrong one from the stand's entry in qa-factory/config.json by hand (the factory never edits it)
      the factory: the gate is rehearsed again after your change; no agent works.
      you: this answer, and that edit of your project's settings file.
      the story: TC-3 and TC-7 are checked as the account that stays; delivery unchanged.
    - `RA-dev-admin: accept` - only this story            (the same three lines as above)
  ```
  The packet's general answer block (`_answer_words`) keeps the form line and lists only the words the open cards offer (`accept`, `myself`).
- Price lines for these cards come from the row's `options` (fork FK-9 (a)); the stand-gap words of the data file are unchanged.
- The person's free words go to the conductor (s4.md route, PK0-6); code reads only `accept` / `myself` (the existing `read_stand_gap_answers`).

### (2b) A role the person said is not a product role -> no account question (S2) - `check_role_accounts` branch + the "decided once" road (PK0-9)
- When the roster state of a declared role R is `not_needed` (a live `product.roles` row), `check_role_accounts` raises NO card and NO finding for R; it
  appends a row to `self.covered_gaps` (the B-414 road, F-36): the role card row's fields plus `"property": {"record": "project_knowledge", "id": "PK-n",
  "words": <the row's words>, "at": <the row's at>, "story": <the row's story>, "subject": "product.roles||<element>", "gap": <the row's RA id>}`. The cases
  of C are then carried as not run by the driver's existing carry (`carry_environment_properties` -> `write_environment_overrides` + `write_carries`, F-36).
  `carry_environment_properties` itself needs no change (F-42: it takes any covered gap with a `property` dict and reads no record itself).
- The packet's "Decided once" block shows ONE line for it (`gate_brief._covered_block`, `stand_gaps.covered_says(row)`):
  `- RA-dev-superuser: "superuser" is not a role of this product (your answer in LOCAL-8 on 2026-11-13), so TC-9 (an operator purges the cache) is
  reported as not run - you wrote: "<words, 160 chars>"` and the block's existing line `To have one asked again, write `<name>: ask again``.
- Take-back: `<id>: ask again` -> `revoke_environment_properties` runs `project_knowledge.py revoke --id PK-n` for a `project_knowledge` row (the
  environment record for every other row; its printed line says "taken back from the record of earlier answers" for a PK row) and drops the cases as today;
  or the person's own words -> the conductor runs the same command. The next rehearsal then shows the role card.
- Every reader on the covered road that today assumes an environment-record row dispatches on `property.record` (PK0-9), each with the behaviour below
  (F-43, F-44). `PK_BY = "project-knowledge"`.
  - `covered_entries`: a PK gap's entry carries `by: PK_BY`, a line built by `covered_says`, and `property: [{"id", "record": "project_knowledge", "subject",
    "gap"}]`; an environment-record gap's entry is byte-for-byte as today.
  - `write_environment_overrides`: `--by PK_BY` and `covered_says` for a PK gap (the prefix guard :984 applies unchanged: an `RA-` id that is the start of
    another gap id gets no override as a whole, its cases still go through the carry).
  - `write_carries`: `from_record` = entries whose `by` is `ENV_BY` or `PK_BY`; `--by` is `PK_BY` when every entry of the case is PK, `ENV_BY` when every
    one is environment-record, none when they mix (the props of both still go into `property`, so `_c4` checks each by its record).
  - `revoke_environment_overrides`: matches by the typed property id as today (PK ids `PK-n` never equal an environment-record id).
  - `_c2` (C2): an answer `by` `PK_BY` is treated as `ENV_BY` - a changed commit or image does not reopen it (a not-a-role answer is not about the
    build); a changed stand address or a withdrawn confirmation still reopens it (as for `ENV_BY`, toward asking).
  - `_c4` (C4): the rule fires for a carry with a `property` list or `by` in (`ENV_BY`, `PK_BY`); no property -> "the answer names no record of it". For
    each property with `record == "project_knowledge"`: `project_knowledge.load(project)` problem -> "the record of earlier answers cannot be read"; the row
    of that id missing or revoked -> "it was taken back"; `project_knowledge.state(project, "product.roles", "", <element of subject>)["state"] !=
    "not_needed"` -> "the person's answer about the role has changed". Every other property is checked against the environment record exactly as today,
    and `environment_record` is loaded ONLY when such a property exists (a PK-only carry never reopens because the environment record is unreadable).
  - `gate_b_split`: `pk_keys` = live S5 records with `by == PK_BY`; the early return becomes "no `env_keys` AND no `pk_keys`, or no project, or no gaps";
    an unreadable environment record skips only the environment-record grouping, an unreadable registry skips only the PK grouping. A gate B gap whose
    answer is `by == PK_BY`, option `accept`, gate A, no `change` (so `_c2`/`_c4` passed), not `ran_red`, with a `project_knowledge` property whose `gap`
    is in `pk_keys` and whose row is live in `project_knowledge.load` is grouped under that `gap` id: covered entry `{"id": <RA id>, "gate": "B", "stage":
    GATE_STAGE["B"], "scope": "role", "case_id": "", "case": "", "cases": [...], "property": <the registry row + "record": "project_knowledge",
    "subject", "gap">}`, rendered by `_covered_block` through `covered_says`. Any other gap behaves exactly as today.
  - Pre-classified hits outside these functions (not on this road): gate_preflight.py:3444 (`_environment_cover`: covers a case row from the environment
    record; a `not_needed` row is appended by `check_role_accounts` and never passes through it); stand_gaps.py:1104 (`record_lasting`: `accept always`
    only, and a role row has no `property_key`); person_owned.py:171 (a metric counter of `DRIVER_BY`; a `PK_BY` entry is counted "interactive" as an
    `ENV_BY` one is today).
  INVARIANT: a project-knowledge row is never revoked or quoted through the environment record, and an environment-record row's road is byte-for-byte
  unchanged. ERROR DIRECTION of `_c4`/`gate_b_split` for a PK carry (an existing gate in a new role: it now decides NOT to re-ask a case at gate B): toward
  asking. Adversarial inputs that must stay on the asking side (each a test in PK0-9): a carry `by: project-knowledge` with no property; a property naming
  a revoked PK row; a property naming a PK row whose role is now `known` (a later row); a property whose `record` is `project_knowledge` but whose id is an
  environment-record id; an unreadable registry; a property whose `gap` is not among the live `PK_BY` keys; a gate B gap that ran red.

### (3) The answer recorded with scope - `project_knowledge.py` CLI (conductor) -> `record` / `record_stand_account`
- Keys given (stand, always): `project_knowledge.py account --task T --role "<role>" --user-key U --secret-key S --words-file F [--replace]`:
  (a) refuse under `no_trace`; (b) `result = project_decisions.record_stand_account(root, stand=<the story's chosen stand>, ...)` - the config value, its
  receipt, its DD row (unchanged writer); (c) `record(key="environments.credentials_by_role", environment=result["stand"], element=result["role"],
  state="known", source="person", by="conductor")` - `element` is the REAL key (S11 d); (d) when the role is not a `known` roster element,
  `record(key="product.roles", element=result["role"], state="known", value={"sign_in": "account"})`. ORDER invariant: config first, registry second.
  Printed: `auditor on dev: recorded (DD-12, PK-3)`; when `result["unchanged"]`: `auditor on dev: already recorded (PK-3)` (no DD id exists) - the
  registry row is still written if absent. No chosen stand -> refused "the story has no chosen stand; name it first" (the `_stand_of` invariant);
  no `environments[]` row at all -> `record_stand_account`'s own refusal is printed whole (phase 3.4 replaces its door; §4).
- "only this story": the person writes `RA-<..>: accept`; the driver records it on the existing stand-gap road (F-36); no registry row.
- "not a role of this product": `project_knowledge.py role --task T --role "<role>" --state not_needed --words-file F` -> a `product.roles` row
  `not_needed`; the conductor ALSO records `accept` for that card (`waiver.py --task T --stage S5 --block "stand gap: <gap id>" --words-file F`, the
  s4.md:189 form) so this story's cases are reported not run; later stories take road (2b).
- Revoke: `project_knowledge.py revoke --id PK-n --words-file F` (under the lock; door `project_knowledge.py show`). An account VALUE is changed with
  `--replace`; removing an account from config is outside phase 0 (hand edit; the registry row then reads `unknown`).
- `show [--json]` lists rows and the load problem (exit 1 when unreadable).

### (4) The fact survives the story's close
- The config pointer survives `restore_config` because `record_stand_account` leaves a decision receipt in the window (F-17); the registry survives
  because `records/` is never reverted (F-16). PK0-1's FIRST test: a fresh story T (`snapshot_config`), `project_knowledge.py account` during T,
  `restore_config(T)` -> the pointer is in `kept`, the registry row is there, and `state()` is `known` afterwards.

### (5) The next story does not ask, and says so
- `check_role_accounts` finds `known` -> no card. It adds ONE note per packet (D-0047 (2)) listing the declared roles whose account the person gave in
  an earlier story (`project_knowledge.acting_line(rows)`): `Acting on your earlier answers: the account of "auditor" on "dev" (given in LOCAL-7 on
  2026-11-12). To change it, say so.` Legacy accounts are not voiced (today's `held` line). A not-a-role answer is voiced by its own line (2b).

### (6) A role the strategist noticed -> `noticed_unconfirmed`, confirmed at gate A (В8)
- Producer: the OPTIONAL S3 handoff section `product_roles` (S5, N2), a REAL parsed list of `s3-strategist-to-designer.yaml`, placed after `unresolved:`
  and before `blocked:`, with its comment and ONE placeholder row whose three hints each carry the OPTIONAL_WORDS word `optional` (F-41) and no `|`:
  ```
  # Optional: every role this story's plan checks - also one the roster in your brief lacks - with where the requirements name it.
  # Leave the list out, empty or as this placeholder when the checks need no particular role. A role you name that the project does not
  # know yet is recorded as noticed, not confirmed; the person confirms it at gate A. Never a role taken from the code.
  product_roles:
    - role: <optional: the role's name as the requirements say it>
      sign_in: <optional: account or none>
      where: <optional: the requirement id and the words that name the role>
  ```
  The role writes it through its sanctioned road, e.g. `product_roles[0].role: auditor` in `<dispatch>.values.yaml` (`handoff_check._apply_one` accepts a
  contract path, F-41). No change to handoff.py, handoff_check.py, `REQUIRED_LISTS` or `null_outcome` (every list but `scope` may be empty; a field whose
  hint says `optional` is never owed by the 'not filled' check). The strategist learns it from the brief line and its charter paragraph (step 1).
- Both worlds (temporal edge): BEFORE the template change (and for a story in flight whose S3 form was begun on the older package) the form has no
  `product_roles` line: the check owes nothing (an optional field the form lacks); a values line for it is not a refusal - the role gets either the
  written row or the M-7 line "this form has no line for it and its check does not ask for it - not written" (F-41, U-5); `story_roles` returns `[]`;
  nothing is noticed, nothing is asked, no confirm card - exactly today's behaviour. AFTER (a form begun on the new package): `handoff_init` puts the
  placeholder row in the skeleton; left as it is, it reads as "nothing noticed"; filled, its rows are noticed. The move that creates the section in a
  form is `handoff_init` of a dispatch begun after PK0-3 merges.
- Reader: `project_knowledge.story_roles(task_root)` (PK0-1; pure) reads `brief_pack.last_accepted_form(task_root, "S3", "qa-test-strategist")` (F-25)
  through `handoff.parse` and returns `[{"role", "sign_in", "where"}]` and a reason. A row whose `role` is a placeholder or empty (`handoff.is_placeholder`)
  is SKIPPED; a `sign_in` that is a placeholder or not `account`/`none` reads as `account` (toward asking: a role with sign-in is the one that can raise an
  account card later, and `sign_in` only feeds the roster's display and the `guest` edge); a placeholder `where` reads as `""`. Absent form / unreadable /
  no section / `[]` / placeholder rows only -> `[]`. INVARIANT: a template placeholder never becomes a noticed role.
- Recorder: `project_knowledge.notice_from_handoff(root, task_root, story)` (PK0-3): for every element of `story_roles` whose comparator form is not a live
  roster element (and not `not_needed`) writes `record(key="product.roles", state="noticed_unconfirmed", source="role", by="driver", where=<where>,
  value={"sign_in": ...}, task_root=task_root)`. Idempotent. Never raises (one printed line on a failure; the gate is still shown).
- Called by the driver in `Driver.gate_repair("A")` AFTER story_run.py:16571 (the `apply_question_answers` return) and BEFORE `gate_entry_steps`
  (:16572) (S16). POSITION invariants: (iii) nothing is written under an open question about this gate (the return at :16534-16537 comes first); (iv)
  nothing is written after the person has spoken (the old-kept and kept-answer returns at :16538-16564 come first); the noticed rows exist before the
  rehearsal that builds the packet.
- The confirm card: `check_role_accounts` appends ONE row per noticed role that `story_roles` names (a noticed role this story does not name is not
  shown) to `self.stand_gaps`, `{"id": "PR-" + <the role token as role_gap_id makes it> , "scope": "product_role", "role": R, "case": "", "cases": [],
  "fact": {"key": "product.roles", "environment": "", "element": R}, "remedy": {"offers": []}, "options": [...]}` and NO finding (fork FK-10: the card
  does not hold the gate; "leave it" is silence). Rendered by the same renderer (branch `scope == "product_role"`: heading word `Product role to confirm:`,
  no `the fix:` line; excluded from the general answer block's open ids):
  ```
  Product role to confirm: PR-guest — "guest", a role the test strategist found in this story's requirements
    the test: the plan checks "guest" as a separate role (no sign-in), from R-2: "a visitor who is not signed in sees the catalogue"
    missing:  your word that "guest" is a role of the product; until then it stays marked as not confirmed
    the answers, in your own words on a line of their own, naming "guest":
    - yes, it is a role of the product
      the factory: a record for the whole project; no agent works.
      you: this answer.
      the story: unchanged; later stories show "guest" as a confirmed role; delivery unchanged.
    - no, it is not (say what it is instead, if it has another name)
      the factory: a record for the whole project; no agent works.
      you: this answer, and the other name if it has one.
      the story: this story's plan stays as it is; later stories do not show "guest" as a role; delivery unchanged.
    - leave it
      the factory: nothing runs.
      you: nothing more now; you are asked again in the next story whose plan names "guest".
      the story: unchanged; delivery unchanged.
  ```
  The conductor records `project_knowledge.py role --role R --state known|not_needed --words-file F`. Silence keeps `noticed_unconfirmed` (В8).

### (7) The default login is asked on need - `gate_preflight.default_login_needed(task_root, cfg)` (new, pure), ONE rule for gate A and S6 (S7)
- The stand's DEFAULT account is needed when ANY of (FK-3 (a) as amended):
  (a) a case declares `{"stand_account": "default"}`;
  (b) the plan (`work/test-plan.json`) has a row with disposition `automate` (the project's harness may sign in; nothing declares it);
  (c) a case of a `manual-agent` row declares NO account precondition (today's S6 reading of a screen case, F-10);
  (d) any case's preconditions, any case's plan row (the case's `plan_row` front matter -> the row's disposition) or the plan cannot be read, or a row's
      disposition is not one of the known words (AR-28);
  (e) an EXECUTED case (row disposition `automate` or `manual-agent`) declares a `case_seeds` precondition - seeding runs as default (F-10b);
  (f) an executed `manual-agent` case declares a role whose account is not `known` on the chosen stand
      (`project_knowledge.state(..., "environments.credentials_by_role", stand, role)`), or no stand is chosen - the runner creates it as default (F-10b).
      EXCEPT (N3) a role whose roster state is a LIVE `not_needed` (`project_knowledge.state(root, "product.roles", "", role)["state"] == "not_needed"`
      with no load problem): its cases are carried as not run by (2b), the runner never walks them, so they need no login and no creation. Every other
      unknown still counts (Lead direction): the registry unreadable (the `not_needed` cannot be established -> counts), a revoked or superseded
      `not_needed` (-> counts), a role carded at this gate (its card decides first, but until it is answered the default stays asked - toward asking).
  NOT needed only when every executed case that signs in declares a non-default role whose account is `known` on the chosen stand (or whose role is a live
  `not_needed`), none seeds, and the plan has no `automate` row - or no case is executed at all (only `manual-human` / `skip` / `unverifiable` rows).
  ERROR DIRECTION: toward "needed"; an exception inside -> True. Adversarial inputs for the N3 exception that must stay on the "needed" side: an unreadable
  registry; a revoked `not_needed` row; a `not_needed` row superseded by a later `known` row of `product.roles` while the account is not `known`; a role
  whose form only resembles a `not_needed` element (not equal under `_role_form`).
- Gate A: `check_s5_credentials` computes `missing` login keys (:3841) only when `default_login_needed` is True; else one INFO note `the stand's default
  account is not asked: no case of this story signs in with it, seeds data or creates an account (each names its own recorded account or none).` The
  env-file-absent card (:3817-3822) follows the same need when no integration and no case key is asked either.
- S6: `stand_login_problem(cases)` reads the default account (:13605-13615) only when today's block conditions hold (not `login_declared_none`, not all
  cases on a device stand) AND `default_login_needed(self.task_root, cfg)` is True; the per-block "every screen case declares a non-default account"
  rule of revision 1 is GONE (one rule, AR-19). POSITION invariant: after `login_declared_none` (:13600) and the device-stand clause, before
  `read_login(cfg, root)`. The per-case accounts below (:13616-13647) are still read.
- S6 reads a role's account on the CHOSEN stand (S11 c): the stand of :13641-13642 becomes the entry whose name is `stand_gaps.stand_name(self.task_root)`;
  no such entry -> `("missing_key", "<case>: the story has no chosen stand, so the account <id> (<role>) cannot be read on it\n\n" + STAND_LOGIN_KEYS)`.
  INVARIANT: an account answered for `dev` is never read on `stage`.
- The twin merge "a gate A login answer is the S6 answer" is FK-5: not in phase 0.

---

## §4 Edges (behaviour + the invariant each protects)

| edge | behaviour | invariant |
|---|---|---|
| empty roster (new project, no file) | S3 lines "none recorded yet"; a declared role with no account gets its card at gate A | an empty list is a declared outcome, never "the story needs no role" |
| no `environments[]` row (brand-new project; stands not asked at onboarding) | the roster still reaches S3 (roles without accounts) and the confirm card still runs; no role card (`_stand_account` "error" -> today's FACTORY_DEFECT sentence); `project_knowledge.py account` prints `record_stand_account`'s refusal whole. Accounts are NOT learnable until phase 3.4 (§7) | a stand fact never lands on a stand nobody recorded |
| guest (`sign_in: none`) | never needs an account; never asked for keys; not counted by `default_login_needed` | a role without sign-in is never a reason to ask for credentials |
| the story names a role absent from the roster (handoff) | `noticed_unconfirmed` row + confirm card at gate A | a role's inference never becomes a project fact without the person (В8, C13) |
| a case declares a role absent from roster AND stand | the role card with the "not among the product's roles yet" line; an account answer adds it `known` | one card per fact |
| a declared role the person said is `not_needed` | no account card; the "decided once" line names the answer; its cases carried as not run; `ask again` or words take it back (2b) | a person's project answer is not asked again (FR-7), and never silently applied (the line says it) |
| the same not-a-role cases at gate B (N4) | the carry is `by: project-knowledge` with the PK property; `_c2` ignores a commit/image change; `_c4` keeps it while the PK row is live and the role still `not_needed`; `gate_b_split` lists the cases covered under the `RA-` id; no card | a not-a-role answer is not reopened at gate B by facts it is not about, and is reopened the moment its row is taken back or changed |
| a not-a-role carry while the environment record is unreadable | `_c4` does not load the environment record for a PK-only carry; `gate_b_split` still groups the PK rows | one record's failure never reopens an answer that rests on the other |
| a case resting on BOTH an environment-record gap and a not-a-role gap | the carry has no `--by` (mixed), both props stored; `_c4` checks each by its record; `_c2` treats it as a person's word (a commit change reopens) | mixing never widens what keeps a case closed |
| `not_needed` element with a config account | out of the roster; the account's `state()` stays `known`; at the gate the `not_needed` answer wins (2b) | the person's latest word decides the role; config only decides whether the factory could sign in |
| a `not_needed` role and the default login (N3) | item (f) does not count it; every other item still applies | a case that will not run never asks for a login |
| a role carded at this gate and the default login (N3) | item (f) still counts it (not taken from the re-review; §6 R-2 iii) | an unknown stays on the asking side |
| twins `Admin`/`admin` asked as `ADMIN` | `state()` unknown + `twins`; the twins card (`myself` / `accept`), id `RA-dev-admin` | a doubt is never another account; the offered door works (FR-2) |
| malformed note (fewer than two keys) | role card variant `malformed`; the conductor records with `--replace` | an entry nobody can sign in with is not an account |
| keys recorded, not set in the env file | no role card; the per-case card asks; `_probe_actor` notes | one card per fact (S8.1) |
| a case with a partial parse | dropped by `declared_preconditions`; the existing FACTORY_FIXABLE finding; `default_login_needed` -> True | unknown is never "needs nothing" |
| a resumed story whose per-case account QUESTION was already answered `accept as blocked` | `level_applied` lists the case; the role card drops it; all dropped -> no card | an answered question is not asked again in a new form (S11 a) |
| a resumed story whose per-case account CARD was already answered `PC-…: accept` (N5) | `decisions` holds `accept` for the case's `precondition_gap_id` or its carry key; the role card drops it; all dropped -> no card | the same, for the card form of the earlier answer |
| that earlier card answer was revoked, or answered with another word | `decisions` gives no live `accept`; the case stays on the role card | an answer that is not live never drops a case |
| a second account of the same role (parallel walkers) | out of phase 0: TR3-10 | phase 0 never writes a second account of one role |
| stand not chosen | no role card, no stand-scoped write; S3 lines say so; S6 refuses to read a role's account | a stand fact never lands on a stand the person did not mean |
| several stands | rows keyed by NAME; brief, card and S6 speak only of the chosen stand | an answer for `dev` never covers `stage` (S11 c) |
| the person answers in free words | the conductor runs one of the commands; code reads only `accept` / `myself` / `ask again` | FR-12, AR-17 |
| `--replace`, or `Auditor` given while config holds `auditor` | `element = result["role"]` (the real key); `unchanged` prints `already recorded (PK-n)` | the registry names the key the readers read |
| answer revoked mid-story | the next read sees it; brief lines and a plan already made are not re-pointed; a shown packet is not changed | an assignment in flight is never re-pointed |
| registry unreadable / foreign `schema_version` | `state()` = config only + the problem line; writes refused; no `not_needed` cover (asks); item (f) counts every role | an unknown never suppresses a question (FR-59) |
| `no_trace` run | `record` refuses (code); the CLI prints "the answer stays in this story's words"; `notice_from_handoff` writes nothing | an experiment leaves no trace (P8, FR-53) |
| comparison arms (C14) | arms are `no_trace`, write nothing, read one snapshot; the "falling question count" proof is a non-`no_trace` run | arms are compared on one knowledge snapshot |
| config restored at story end | pointer kept by the decision receipt; registry not touched | a recorded answer outlives its story |
| parallel walkers reading while the driver writes | readers read without the lock (atomic replace); writers load-decide-number-write under the lock; walkers never write | no reader sees half a file; no write is lost |
| the gate A packet on the conductor (skill) road | `notice_from_handoff` is not called there: no noticed rows, no confirm card; the role card and (2b) still appear (they are rehearsal checks) | В8 is not asked in that story and no fact is made from the role's inference either (S14) |
| `product_roles` absent, `[]` or placeholder rows only (old or new S3 handoff) | nothing noticed, nothing refused; `story_roles` -> `[]` | backward compatibility; a placeholder is never a role |
| a story in flight whose S3 form predates the section (N2) | the check owes nothing; a values line for it is written or answered with the M-7 "not written" line, never refused (U-5); nothing noticed | an upgrade mid-story never blocks the strategist and never makes a fact |
| a filled row with a placeholder or unknown `sign_in` | read as `account`; `where` placeholder read as `""` | toward asking; a half-filled row still names its role |
| role name with `,` `|` `\` or a line break | `record_problems` refuses as the account road does | a row is never written that `resolve` would then fail on |
| a role written only in non-ASCII letters, on an ASCII stand (N1) | kept; gap id `RA-dev-<8 hex>` from the role form, stable between rehearsals | an answer meets the same card next time |
| two non-ASCII roles, or `admin-отдел` / `admin-склад`, on one stand (N1) | each lossy form takes its own hash token: two distinct `RA-` ids, two finding ids with no ordinal; an answer for one leaves the other's card | one answer never passes two cards |
| a stand name with non-ASCII or punctuation (N1) | the stand token is the sha1 prefix of the exact name | two stands never share a card id |
| an `RA-` id that is the start of another gap id (`RA-dev-admin`, `RA-dev-admin-x`) | `write_environment_overrides` writes no override for it as a whole (existing guard :984); its cases are still carried | a prefix is never read as another gap's answer |
| a role renamed in config by hand | the old registry `known` row reads `unknown` (config first); the new key is `legacy_config`; the roster shows both until the person removes one | nothing wrong is believed |
| a stand renamed or removed | rows keyed by the old name are orphaned (provenance lost); accounts read config first | nothing wrong is believed; nothing re-asked that config holds |
| a role a role-session tries to record | PK0-8 refuses `project_knowledge.py account|role|revoke` and writes to `project-knowledge.json` | a role never turns its inference into a project fact (В8, FK-7) |

---

## §5 Nodes (written for a weaker model; direction chosen; 8 builder nodes = revision 1's 6 + PK0-8, PK0-9)

General for every node: `given:` PKG/design/factory-rules.md whole, `D:/ws2/wt-fbfix/plans/builder-rules.md`, this spec. Witness = the narrow
files named below ONLY (builder-rules 7b): new test files of the node plus fast existing ones. EVERY file listed in `scripts/slow_tests.json` is judged
by CI on the batch branch and is never run locally; each node names the ones that judge its paths. Every package commit carries
`architecture: AR-n -- <how kept>` and `judgment:` lines. No node touches TR3-10's functions (`deferrable`, `defer_question`, `walk_before`).
Ratchets (AR-20): only the raises of §6 R-1 are approved; any other raise of `judgment-census.json` `ratchet`, `role-load.json`, `driver-layers.json`
or another shrink-only file = STOP and return. A refusal is RETURNED, never raised with `ValueError`/`StateConflict` in a new function (a raise there
makes a blocking unit, §1).

**Queue lines for shared files (D-0048 form: the later node merges main into its tree first, both sides' pins green, one critic after the merge):**
- `scripts/tests/fixtures/judgment-census.json`: `очередь: PK0-1 → PK0-4` (the only two that add rows; any node that finds it must add one queues after PK0-4).
- `scripts/gate_preflight.py`: `очередь: PK0-4 → PK0-9` (both edit `check_role_accounts`); PK0-5 owns other functions (`default_login_needed`,
  `check_s5_credentials`) - function-disjoint with PK0-4/PK0-9, the later merges.
- `scripts/stand_gaps.py`, `scripts/gate_brief.py`: `очередь: PK0-4 → PK0-9`. In stand_gaps.py PK0-4 owns `_gate_a_gaps` / `_PASS_THROUGH` and PK0-9 owns
  `PK_BY`, `covered_says`, `covered_entries`, `write_environment_overrides`, `write_carries`, `revoke_environment_overrides`, `_c2`, `_c4`, `gate_b_split`;
  no other phase-0 node and no batch-3 node writes `_c2`, `_c4` or `gate_b_split` (F-31: no batch-3 node writes stand_gaps.py).
- `scripts/story_run.py`: PK0-3 (`Driver.gate_repair`), PK0-5 (`Driver.stand_login_problem`), PK0-9 (`Driver.revoke_environment_properties` only;
  `carry_environment_properties` and `take_stand_gap_answers` are touched by no phase-0 node, F-42) - function-disjoint with each other and with the
  batch-3 order (F-31); each later one merges main first.
- `scripts/guard_pre_tool.py`: `очередь: TR3-5, TR3-14, TR3-16 → PK0-8` (function-disjoint; PK0-8 merges main after them).
- `scripts/brief_pack.py`: PK0-2 vs TR3-5 → TR3-15 - function-disjoint (F-31); PK0-2 merges main first.
- `references/state-exits.md`: PK0-1 vs TR3-4, TR3-6, TR3-16 - rows appended; PK0-1 merges main first.

### PK0-1 — the registry module `project_knowledge.py` (first; everything depends on it)
- **owns:** `D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\project_knowledge.py` (new), `D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_project_knowledge.py` (new),
  `D:/ws1/wt-fbfix\ai-packages\qa-factory\references\install-paths.json` (one `carried` row), `D:/ws1/wt-fbfix\ai-packages\qa-factory\references\collect-sets.json` (append the path to the D3 row's `paths` list, :51 - no new row),
  `D:/ws1/wt-fbfix\ai-packages\qa-factory\references\conductor-actions.json` (rows: account / role / revoke), `D:/ws1/wt-fbfix\ai-packages\qa-factory\references\state-exits.md` (a row per stored state),
  `D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\fixtures\judgment-census.json` (its two rows + `safety` 51 -> 52 only), `D:/ws1/wt-fbfix\ai-packages\qa-factory\changelog.d\t-2142-pk0-1.md`.
- **What:** `KEYS`; `load(root)`; `state(root, key, environment="", element="", cfg=None) -> {"state","row","source","problem","twins","malformed"}`;
  `roster(root, cfg, stand) -> {"elements": [...], "removed": [...], "problem"}`; `record(...)` with `record_problems` and `_refuse_no_trace` (census rows
  of §1); `revoke(root, pk_id, words)`; `story_roles(task_root)` (skips placeholder rows, §3 (6)); `acting_line(rows)`; CLI `show`, `account`, `role`,
  `revoke` - exactly as §2 and §3 (3), (6). Built on `environment_record.load_rows/write_rows/next_id/revoke_row` (no copy). `state()`, `roster()`,
  `story_roles()` write nothing. If `refusal_registry.py --sites` lists a site, any `refusal_registry.REGISTRY` entry this node adds is registered on
  `_refuse_no_trace` or `record_problems` (a `ref`), NEVER on `record` or `main` (an entry on a non-unit function creates a new unit, test_judgment_census.py:251-255).
- **Tests (one per item):** `test_fact_survives_restore_config` (first); `test_absent_file_reads_config_only`; `test_first_record_creates_file`;
  `test_unreadable_registry_refuses_write_and_reads_config`; `test_foreign_schema_version_is_unknown`; `test_revoked_row_covers_nothing`;
  `test_stand_name_exact`; `test_twin_roles_are_unknown_with_twins`; `test_malformed_note_is_unknown_with_flag`; `test_known_row_without_config_is_unknown`;
  `test_noticed_is_never_known`; `test_unknown_state_value_ignored`; `test_asked_row_is_skipped`; `test_unparseable_at_loses`; `test_latest_row_wins`;
  `test_same_state_again_not_created`; `test_no_trace_refused`; `test_lock_busy_refused`; `test_record_loads_inside_the_lock` (two records racing keep both
  rows); `test_revoke_holds_the_lock`; `test_account_cli_config_then_registry` (calls `record_stand_account`, never writes config itself);
  `test_account_cli_element_is_real_key` (`Auditor` given, `auditor` held); `test_account_cli_unchanged_prints_already_recorded`; `test_account_cli_no_stand_refused`;
  `test_account_cli_adds_roster_element`; `test_role_cli_not_needed_removes_from_roster`; `test_not_needed_with_config_account_out_of_roster_account_known`;
  `test_unsafe_role_name_refused`; `test_key_outside_keys_refused`; `test_words_whole_and_door`; `test_roster_legacy_accounts_dedup_by_form`;
  `test_reserved_roles_never_in_roster`; `test_story_roles_absent_empty_and_rows`; `test_story_roles_skips_placeholder_row` (the template's own placeholder
  row -> `[]`; a row with a filled `role` and placeholder `sign_in` -> `sign_in: account`).
- **non-goals:** any gate, brief, driver or guard change; `asked` writer; `unreachable` storage; per-stand `not_needed` (FK-4); migrating DD rows.
- **witness:** `python -m pytest ai-packages/qa-factory/scripts/tests/test_project_knowledge.py ai-packages/qa-factory/scripts/tests/test_environment_record.py -q`
  and `python -B ai-packages/qa-factory/scripts/selftest.py --limits --lang` and `python -B ai-packages/qa-factory/scripts/refusal_registry.py --sites`
  (attach; if it lists a site in project_knowledge.py, the node owns the registry entry and runs `--check`). Judged by CI: test_judgment_census.py,
  test_install_paths.py, test_person_words.py.
- **architecture:** AR-13, AR-14, AR-24, AR-25, AR-28, AR-29.

### PK0-2 — the roster in the S3 brief + the strategist's craft paragraph (after PK0-1; parallel with PK0-3, PK0-4, PK0-5)
- **owns:** `D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\brief_pack.py` (new `s3_roster_lines`; one call in the S3 head block :3431-3438),
  `D:/ws1/wt-fbfix\ai-packages\qa-factory\agents\qa-test-strategist.md` (one paragraph), `D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_brief_s3_roster.py` (new), `D:/ws1/wt-fbfix\ai-packages\qa-factory\changelog.d\t-2142-pk0-2.md`.
- **What:** §3 (1) - lines, caps, the removed line, the three empty/unknown forms, the "optional section" wording; never raises (an exception -> no lines).
- **Tests:** `test_roster_lines_s3_only`; `test_cap_15_then_more`; `test_empty_roster_line`; `test_no_stand_line`; `test_unreadable_registry_line`;
  `test_noticed_marked_not_confirmed`; `test_removed_line`; `test_provenance_shown`; `test_optional_section_named`; `test_exception_gives_no_lines`.
- **non-goals:** S4/S6 briefs; inject-map rows (phase 5); the handoff template (PK0-3).
- **witness:** `python -m pytest ai-packages/qa-factory/scripts/tests/test_brief_s3_roster.py ai-packages/qa-factory/scripts/tests/test_role_load.py -q`, `python -B ai-packages/qa-factory/scripts/selftest.py --limits --lang`,
  and `python -B ai-packages/qa-factory/scripts/role_load.py --all` before and after (attach both; no raise is approved for the strategist, §6 R-1).
  Judged by CI: test_brief_pack_roles.py, test_brief_pack.py.
- **architecture:** AR-10, AR-11, AR-29.

### PK0-3 — the optional `product_roles` section and the noticed recorder (after PK0-1; parallel with PK0-2, PK0-4, PK0-5)
- **owns:** `D:/ws1/wt-fbfix\ai-packages\qa-factory\handoffs\s3-strategist-to-designer.yaml` (a REAL list section `product_roles` after `unresolved:` and
  before `blocked:`: the comment lines and the one placeholder row of §3 (6), each hint carrying `optional` and no `|`; nothing else in the file),
  `D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\project_knowledge.py` (`notice_from_handoff` only - after PK0-1),
  `D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\story_run.py` (`Driver.gate_repair`: ONE call at the position of §3 (6), between :16571 and :16572),
  `D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_knowledge_notice.py` (new), `D:/ws1/wt-fbfix\ai-packages\qa-factory\changelog.d\t-2142-pk0-3.md`.
- **What:** §3 (6) producer section + recorder + the call. No `Driver.gate`, `Driver.rehearse` or `driver-layers.json` change (no new Driver name).
  No change to handoff.py or handoff_check.py: the section works through the existing optional-hint and empty-list rules (F-41).
- **Tests:** `test_notice_writes_noticed_for_new_role`; `test_notice_skips_known_by_form`; `test_notice_skips_not_needed`; `test_notice_idempotent`;
  `test_notice_absent_handoff_writes_nothing`; `test_notice_empty_list_writes_nothing`; `test_notice_placeholder_row_writes_nothing`;
  `test_notice_no_trace_writes_nothing`; `test_notice_never_raises`;
  `test_values_write_product_roles` (`handoff_check.apply_values` on a fresh S3 form begun from the new template with `product_roles[0].role: auditor`,
  `product_roles[0].sign_in: account`, `product_roles[0].where: R-2` -> written, no refusal; `story_roles` then returns the row);
  `test_old_and_new_forms_pass_the_check` (`handoff_check`'s pure check on (i) an S3 form WITHOUT the section and (ii) a new form whose `product_roles` holds
  only the placeholder row: neither gets a problem the same form gets without this change - compare the problem lists before/after the template edit);
  `test_placeholder_row_reads_empty` (`project_knowledge.story_roles` on the new form left as `handoff_init` made it -> `[]`);
  `test_in_flight_form_values_not_refused` (an S3 form begun on the OLD template, values `product_roles[0].role: auditor` -> no refusal; the test asserts
  and the report states which of the two outcomes of F-41 / U-5 happens - written, or the M-7 "not written" line);
  `test_gate_repair_calls_notice_after_kept_answer_branch` (a source-order test over `gate_repair`'s text: the call sits after the `apply_question_answers`
  return and before `gate_entry_steps`; fast, no driver loop). If the check DOES give a new problem for (i) or (ii), the node STOPS and returns with the
  problem text (the measured fact F-41 would be wrong) - it never edits handoff.py or handoff_check.py to make it pass.
- **non-goals:** `REQUIRED_LISTS`, `null_outcome`, handoff.py, handoff_check.py; any `asked` row; reading free words; S3 exit refusals on `product_roles` content (AR-29).
- **witness:** `python -m pytest ai-packages/qa-factory/scripts/tests/test_knowledge_notice.py ai-packages/qa-factory/scripts/tests/test_role_load.py -q`, and
  `python -B ai-packages/qa-factory/scripts/role_load.py --all` before and after the template edit (attach both; the template adds about 7 lines; no raise of
  `role-load.json` is approved, §6 R-1 - a raise = STOP). Judged by CI: test_handoff.py, test_driver_layers.py, test_story_run_gate_repair.py.
- **architecture:** AR-10, AR-21, AR-22, AR-23, AR-28, AR-29.

### PK0-4 — the role card, the twins card, the confirm card, the acting line on the card road (after PK0-1; parallel with PK0-2, PK0-3, PK0-5)
- **owns:** `D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\gate_preflight.py` (functions: `check_role_accounts` new, `role_gap_id` new; `Rehearsal.__init__` - the two sets
  `_role_carded`, `_account_carded`; `gap_name` - a branch returning the gap id for `scope` `role`/`product_role`; `check_case_preconditions` - take role-carded
  items out before `_card_items`; `_probe_actor` - a note for an account `_account_carded` holds; `run` - the step tuple, `r.check_role_accounts` right before
  `r.check_actor_sign_in`),
  `D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\stand_gaps.py` (`_gate_a_gaps`: a branch for `scope` `role`/`product_role` building `the_test` from each case's title and
  `missing` per §3 (2)/(6); `_PASS_THROUGH` += `role`, `fact`, `options`, `variant`, `in_roster`),
  `D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\gate_brief.py` (`_gap_heading`, `stand_gap_form_ids` (a `role`/`product_role` row is written by its gap id), `_card` (heading
  word for `product_role`; the `options` block with `_price_labels` lines instead of `the fix:` when a row carries `options`; the not-in-roster line),
  `stand_gap_card_lines` (a row whose `remedy.offers == []` is not an open id of the general answer block)),
  `D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\fixtures\judgment-census.json` (the `check_role_accounts` row; queue after PK0-1),
  `D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_gate_role_accounts.py` (new), `D:/ws1/wt-fbfix\ai-packages\qa-factory\changelog.d\t-2142-pk0-4.md`.
- **What:** §3 (2), (5), (6)-card. Texts verbatim from §3 (the builder may shorten only to pass `human_text.problems`). A `not_needed` role gets the
  role card here (toward asking) until PK0-9 replaces it. The drop of already-answered cases reads `stand_gaps.level_applied`, `stand_gaps.decisions`,
  `precondition_gap_id` and `shared_precondition_ids` - existing readers, no new one (N5). `role_gap_id` exactly as §3 (2) (N1).
- **Tests:** `test_one_card_per_stand_role_holding_only_its_cases`; `test_finding_lead_within_brief_cut_and_names_stand_role_question` (at `BRIEF_CUT`
  with 40-character stand and role; the question mark is inside the first 200 characters); `test_card_rendered_whole_in_packet` (`stand_gaps._gate_a_gaps`
  + `gate_brief.stand_gap_card_lines` on the rehearsal's rows: the heading, every answer and every price line are separate lines);
  `test_story_waiver_for_one_role_does_not_pass_another` (override `stand gap: RA-dev-auditor`; cards for `admin` and `auditor` holding the same cases;
  the admin card and finding stay); `test_accept_blocks_only_its_cases` (`read_stand_gap_answers` reads `RA-dev-auditor: accept`; `gap_cases` gives exactly C);
  `test_finding_id_roundtrip` (`role_accounts-dev-auditor` matches `FINDING_ID_RE`); `test_non_ascii_role_gap_id_stable`;
  `test_two_non_ascii_roles_two_gap_ids` (N1: roles `аудитор` and `менеджер` on the ASCII stand `dev`: two distinct `RA-dev-<8 hex>` ids, two distinct finding
  ids with no `-2`; override `stand gap: <id of аудитор>` leaves the `менеджер` card and finding in place; a second rehearsal gives the same two ids);
  `test_mixed_script_roles_two_gap_ids` (N1: `admin-отдел` and `admin-склад` on `dev` -> two distinct hash ids, neither `RA-dev-admin`);
  `test_lossless_role_keeps_readable_id` (N1: `auditor` -> `RA-dev-auditor`; `ADMIN` -> `RA-dev-admin`; `Default_User`-style separators -> `RA-dev-default-user`;
  a stand `dév` -> an 8-hex stand token); `test_known_role_no_card_acting_line`;
  `test_legacy_account_not_voiced`; `test_keys_not_set_stays_per_case_card_and_probe_notes`; `test_every_unmet_item_exactly_one_card` (3 cases x 2 roles,
  plus the keys-not-set case and a partial-parse case); `test_probe_actor_no_second_card`; `test_registered_before_actor_sign_in`; `test_no_stand_no_role_card`;
  `test_partial_parse_case_not_carded`; `test_case_already_accepted_is_dropped` (S11 a, the question form); `test_case_accepted_on_its_pc_card_is_dropped`
  (N5: `stage_overrides` holds a live `stand gap: PC-1` accept for TC-3's `stand_account` item - and, in a second fixture where `PC-1` is shared, `PC-1@TC-3` -
  the role card does not hold TC-3; with every case so answered, no card); `test_case_carry_live_is_dropped` (N5: a live `stand gap: TC-3` carry accept ->
  TC-3 dropped); `test_revoked_pc_accept_is_not_dropped` (N5: the same `PC-1` accept revoked, or answered `myself` -> TC-3 stays on the card);
  `test_all_cases_accepted_no_card`; `test_role_not_in_roster_line`;
  `test_twins_answer_door_is_usable` (offers `theirs` + `accept`; no names answer; the card id is `RA-dev-admin`); `test_malformed_variant`; `test_no_accept_always_offered`;
  `test_confirm_card_only_roles_this_story_names`; `test_confirm_card_holds_no_finding`; `test_confirm_card_not_in_answer_block`;
  `test_every_option_has_three_price_lines` (each new card: every option followed by lines starting with the three `_price_labels`);
  `test_case_ids_explained_by_title`; `test_unreadable_registry_note`; `test_texts_pass_human_text`; `test_check_writes_nothing` (FR-45: project and story
  trees byte-equal before/after the rehearsal).
- **non-goals:** login keys (PK0-5); the `not_needed` cover (PK0-9); recording anything; S6; `question-vocabulary.json` (FK-9 (b), FK-12 (b) not taken).
- **witness:** `python -m pytest ai-packages/qa-factory/scripts/tests/test_gate_role_accounts.py ai-packages/qa-factory/scripts/tests/test_stand_gaps.py ai-packages/qa-factory/scripts/tests/test_stand_gap_contract.py ai-packages/qa-factory/scripts/tests/test_stand_gap_remedy.py -q`
  and `python -B ai-packages/qa-factory/scripts/selftest.py --limits --lang`. Judged by CI: test_gate_preflight.py, test_judgment_census.py, test_stand_gap_carry.py,
  test_gate_brief_and_retro.py, test_gate_brief_attachments.py.
- **architecture:** AR-9, AR-10, AR-13, AR-15, AR-16, AR-18, AR-19, AR-28, AR-29.

### PK0-5 — the default login asked on need, one rule at gate A and S6 (after PK0-1; parallel with PK0-2, PK0-3, PK0-4)
- **owns:** `D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\gate_preflight.py` (functions: `default_login_needed` new; `check_s5_credentials`),
  `D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\story_run.py` (function `Driver.stand_login_problem` only),
  `D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_login_need.py` (new), `D:/ws1/wt-fbfix\ai-packages\qa-factory\changelog.d\t-2142-pk0-5.md`.
- **What:** §3 (7) (FK-3 (a) as amended; item (f) with the N3 exception for a live `not_needed` role only), the chosen-stand reader at S6 (S11 c); FK-5 not
  implemented. Tell TR3-10's designer the seeding fact (report line). Report line for the Lead: the N3 exception narrows the S7 amendment and changes no
  owner decision (FK-3 (a) "creates a user with the default account" still holds: a `not_needed` role's cases are not walked, so nothing is created).
- **Tests:** `test_default_declared_needs_login`; `test_automate_row_needs_login`; `test_manual_case_without_account_needs_login`; `test_seeded_case_needs_login`;
  `test_unprovisioned_role_needs_login`; `test_no_chosen_stand_needs_login`; `test_all_cases_named_known_roles_no_default_ask`; `test_only_manual_human_rows_no_ask`;
  `test_unreadable_plan_needs_login`; `test_unreadable_case_needs_login`; `test_unknown_disposition_needs_login`; `test_exception_means_needed`;
  `test_not_needed_role_does_not_need_default_login` (N3: the only executed `manual-agent` case declares `superuser`, a live `not_needed` row; no automate row,
  no seeding -> not needed); `test_carded_role_still_needs_default_login` (N3: a declared role with `unknown` account and no `not_needed` row -> needed);
  `test_unreadable_registry_role_needs_default_login` (N3: the registry unreadable -> needed); `test_revoked_not_needed_needs_default_login` (N3);
  `test_gate_a_note_when_not_asked`; `test_s6_uses_the_same_rule` (`Driver.stand_login_problem` on a fixture with a fake `manual_capture`: default read
  iff `default_login_needed`; fast, no driver loop); `test_s6_keeps_default_for_unreadable_request`; `test_role_accounts_still_read_in_s6`;
  `test_s6_reads_role_on_chosen_stand_only`; `test_s6_no_chosen_stand_refuses_role_read`.
- **non-goals:** merging the gate A login pass into S6 (FK-5); integration keys; `_probe_actor`; the `default` triple (§6 remainder); the re-review's
  carded-role and all-dropped exclusions of item (f) (§6 R-2 iii).
- **witness:** `python -m pytest ai-packages/qa-factory/scripts/tests/test_login_need.py ai-packages/qa-factory/scripts/tests/test_manual_actor.py -q`.
  Judged by CI: test_gate_preflight.py, test_story_run_s6.py.
- **architecture:** AR-19 (one rule for gate A and S6), AR-13 (one stand pick), AR-28, AR-29.

### PK0-8 — the guard closes the registry's write commands to roles (S6; after PK0-1; queued after TR3-5, TR3-14, TR3-16 on guard_pre_tool.py)
- **owns:** `D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\guard_pre_tool.py` (`human_word_check`: one alternative
  `re.search(r"project_knowledge\.py[\"']?(?:\s*,\s*|\s+)[\"']?(?:account|role|revoke)(?![\w-])", low)` in the same form as :1755; `HUMAN_WORD_MSG`: one sentence
  "`project_knowledge.py account`, `role` and `revoke` store what the person said about the product's roles and the stand's accounts, or take it back; a role
  running them would turn its own inference into a project fact (`show` is open to you)."; `STAND_RECORD_FILES` += `"project-knowledge.json"`; the
  `_stand_record_matcher` docstring names it), `D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_guard_project_knowledge.py` (new),
  `D:/ws1/wt-fbfix\ai-packages\qa-factory\changelog.d\t-2142-pk0-8.md`.
- **Tests:** `test_role_running_account_role_revoke_is_blocked` (each subcommand, space and argv-list spellings); `test_show_stays_open`; `test_conductor_not_blocked`
  (no `agent_type`); `test_another_script_with_role_word_not_blocked` (`role_load.py role`); `test_role_write_to_project_knowledge_json_blocked` (Write and a shell
  redirect); `test_message_names_show_as_open`.
- **non-goals:** any other guard function (TR3-5/14/16 own theirs); census rows (both functions exist; class unchanged); NO new function, helper or
  module-level callable in guard_pre_tool.py - literally (the file is on the blocking path: a new function named in the unit family would be a BLOCKING
  unit, critic r2 Q3); the global-option spelling (§6 R-2 iv).
- **witness:** `python -m pytest ai-packages/qa-factory/scripts/tests/test_guard_project_knowledge.py ai-packages/qa-factory/scripts/tests/test_guard_command_text.py -q`.
  Judged by CI: test_judgment_census.py, test_guard_dispatch_budget_and_logs.py.
- **architecture:** AR-14, AR-11 (FR-56, FR-39), AR-29.

### PK0-9 — "not a role of this product" is not asked again, at gate A and gate B (S2, N4; after PK0-4 - queue on gate_preflight.py, stand_gaps.py, gate_brief.py)
- **owns:** `D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\gate_preflight.py` (`check_role_accounts`: the `not_needed` branch -> a `covered_gaps` row, §3 (2b)),
  `D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\stand_gaps.py` (`PK_BY`; `covered_says` new; `covered_entries`, `write_environment_overrides`, `write_carries` (the `ENV_BY`
  lines :1036-1037), `revoke_environment_overrides` - each dispatches on `property.record`; `_c2` (:669: `PK_BY` as `ENV_BY`); `_c4` (:710-731: the
  `project_knowledge` property rule, the environment record loaded only for its own properties); `gate_b_split` (:903-923: `pk_keys`, the split early
  return, the PK grouping under the `RA-` id)),
  `D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\gate_brief.py` (`_covered_block`: `covered_says` instead of `ER.says`, at gate A and gate B),
  `D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\story_run.py` (`Driver.revoke_environment_properties`: `project_knowledge.py revoke` and its printed words for a `project_knowledge` row),
  `D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_not_needed_role.py` (new), `D:/ws1/wt-fbfix\ai-packages\qa-factory\changelog.d\t-2142-pk0-9.md`.
- **What:** §3 (2b), every bullet. `Driver.carry_environment_properties` is NOT owned and needs no change: it filters covered gaps only by `property`
  being a dict and reads no record itself (F-42). Before writing, grep `ENV_BY|ER\.says\(|environment_record\.py", "revoke` over PKG/scripts with a
  positive control (the known hit stand_gaps.py:989) and give every hit a verdict in the report. Known hits and their verdicts (F-43): inside the owned
  functions -> dispatched; gate_preflight.py:3444 (`_environment_cover`) -> not on this road; stand_gaps.py:1104 (`record_lasting`) -> not on this road;
  stand_gaps.py:547 -> the constant. Only a hit NOT in this list and outside the owned functions = STOP and return with the hit.
- **Tests:** `test_not_needed_role_is_not_asked_for_an_account_again` (a later story: no role card, no finding, one covered row); `test_covered_line_names_role_story_date`;
  `test_cases_carried_as_not_run` (`covered_entries` + `write_carries` on a fake `run`: the waiver lines carry `--by project-knowledge` and the cases);
  `test_ask_again_revokes_the_registry_row` (`revoke_environment_properties` with a fake `py`: `project_knowledge.py revoke --id PK-n`); `test_revoked_not_needed_asks_again`;
  `test_later_known_row_wins_over_not_needed`; `test_environment_record_rows_unchanged` (an environment-record covered gap: the same lines and commands as before,
  byte for byte, through `covered_entries`, `write_environment_overrides`, `write_carries`, `_c2`, `_c4` and `gate_b_split`); `test_unreadable_registry_no_cover`
  (toward asking);
  `test_gate_b_does_not_reask_not_needed_cases` (N4: the gate A carry written for TC-9 with `by: project-knowledge` and the PK property; at gate B
  `gate_b_split` lists TC-9 covered under `RA-dev-superuser`, `carried_change(task_root, "TC-9", answer)` is `""`, no card for TC-9);
  `test_c2_commit_change_keeps_pk_carry` (N4: a `stand-identity` row with a new `revision` after the answer -> `_c2` gives no reason for a `PK_BY` carry; a new
  `stand_definition_sha` still does); `test_c4_revoked_pk_row_reopens` (N4); `test_c4_role_no_longer_not_needed_reopens` (N4: a later `known` row of
  `product.roles` for the element); `test_c4_pk_only_carry_ignores_unreadable_environment_record` (N4: environment-properties.json unreadable, PK carry
  stays settled); `test_c4_pk_carry_without_property_reopens` (N4); `test_c4_unreadable_registry_reopens` (N4); `test_gate_b_split_mixed_carry_not_covered_by_pk`
  (a case whose carry has no `--by` because it mixes records -> not grouped as PK-covered; asked or shown by B-361's view as today).
- **non-goals:** per-stand `not_needed` (FK-4); any new closed word; the `environment_record` module; `Driver.carry_environment_properties`;
  `take_stand_gap_answers`.
- **witness:** `python -m pytest ai-packages/qa-factory/scripts/tests/test_not_needed_role.py ai-packages/qa-factory/scripts/tests/test_stand_gaps.py -q`.
  Judged by CI: test_stand_gap_carry.py, test_gate_preflight.py, test_story_run_stand*.py, test_gate_brief_and_retro.py.
- **architecture:** AR-15 (one "decided once" road, gate A and gate B), AR-22 (every reader of the new `by` value owned), AR-24, AR-25, AR-27, AR-28, AR-29.

### PK0-6 — texts, map, invariant (after PK0-1..PK0-5, PK0-8, PK0-9)
- **owns:** `D:/ws1/wt-fbfix\ai-packages\qa-factory\skills\qa-story\phases\s4.md` (:177-190: the role card's free answers -> `project_knowledge.py account|role` with `--task`;
  "not a role" also records `accept` for the card; the twins card is answered by `myself`/`accept`; the confirm card -> `role --state known|not_needed`; the
  no_trace line now says the command refuses), `D:/ws1/wt-fbfix\ai-packages\qa-factory\references\environments.md` (:15-16: accounts recorded through `project_knowledge.py account`),
  `D:/ws1/wt-fbfix\ai-packages\qa-factory\design\architecture.md` (AR-3 invariant: "a project's facts live in its config or in the answer registry `records/project-knowledge.json` ..."; carriers of AR-13/AR-14/AR-15 name the registry),
  `D:/ws1/wt-fbfix\docs\SIBLING_MAP.md` (axis 34 "a person's answer or a learned project fact kept across stories": survivor `project_knowledge.py`; members `environment_record`,
  `stand_identity`, `report_adapt` RA-n, `remembered_answers`, `asked_until_answered`, `waiver --carry-from`, `obligations.md`, confirmed default stand, `project_decisions` DD rows,
  `manual.accounts_way` (planned), `gap-classes.json` as the per-story twin; enforcement member `guard_pre_tool.human_word_check` / `STAND_RECORD_FILES`),
  `D:/ws1/wt-fbfix\docs\ARCHITECTURE_INDEX.md` (regenerated by `python tools/architecture_index.py`), `D:/ws1/wt-fbfix\ai-packages\qa-factory\changelog.d\t-2142-pk0-6.md`.
- **Tests / keys (doc witness, rule 11: keys quoted before the run, script attached, a negative control):** keys `project_knowledge.py account`,
  `project_knowledge.py role`, `records/project-knowledge.json`, `Axis 34`, `guard_pre_tool`.
- **witness:** `python tools/architecture_index.py --check`, `python -B ai-packages/qa-factory/scripts/selftest.py --limits --lang`, the key-presence script with its negative control.
- **architecture:** AR-3 (text change), AR-15, AR-17.

### PK0-7 — live proof (Lead / driver run, not a builder) - §8.

**Order and parallelism:** PK0-1 -> {PK0-2 ‖ PK0-3 ‖ PK0-4 ‖ PK0-5 ‖ PK0-8 (after TR3-5, TR3-14, TR3-16 merge)}; PK0-4 -> PK0-9; all -> PK0-6 -> PK0-7.
Writing slots after PK0-1: up to 5 at once (cap 6). Batch canon on CI (every slow file named above).
**Cut to stay small (and why):** no `asked` writer (phase 2); no generic `need()` seam (phase 2); no no-hold deferral (C8; TR3-10); no per-stand
`not_needed` carry (FK-4); no new closed answer words (FK-12); no stand selection change and no `_stand_of` door rewrite (phase 3.4); no onboarding
change (phase 4); no inject-map/`needed_by` (phase 5); no S9 fold (phase 6).

---

## §6 Forks for the Lead / owner

Decided (kept as recorded in the Lead acceptance block): FK-1 (a), FK-2 (a), FK-3 (a) amended by S7, FK-4 (defer), FK-5 (phase 3.1), FK-6 (a), FK-7 (a), FK-8 (a).

NEW in revision 2 (each node is executable on the recommendation until answered):
- **FK-9 Where the price lines of the new cards live (S13).** (a) per card: the row carries `options` (says + the three lines) and `_card` prints them
  with `_price_labels`; the data-file stand-gap words stay as they are; (b) add `factory`/`you`/`story` to every `stand_gap_words` row of
  question-vocabulary.json, so EVERY stand-gap card at both gates gains price lines (closes the shared road's debt, F-35, but changes every stand-gap
  packet and its tests, gate B included). **Recommend (a)** for phase 0, and queue (b) as a finding naming the class "stand-gap cards carry no price
  lines (human-questions item 6)". Builder: (a). This is a person-facing text: the owner may prefer (b).
- **FK-10 Does the confirm card hold the gate?** (a) no: it is a card with no finding; silence = "leave it" (В8: silence never makes a fact, and the card
  says it is asked again); (b) yes: a PERSON_DECIDES finding, so the gate waits for yes / no / leave. **Recommend (a)**: the card's own third answer is
  silence, and (b) would make the person write "leave it" to pass a gate. Builder: (a). A person's question is at stake: owner's to reverse.
- **FK-11 How "not a role" reaches later stories (S2's carry).** (a) the "decided once" road (`covered_gaps`, B-414) with a `record` dispatch on its
  readers (PK0-9); (b) a separate carry of its own in the driver (a new writer of the same overrides, a twin of the B-414 road). **Recommend (a)**
  (AR-15: one road for a person's lasting answer to a stand-gap card). Builder: (a).
- **FK-12 Closed words for the new answers.** (a) only `accept` / `myself` are closed (already in the data file); the account names, "not a role" and the
  confirm answers are the person's own words, read by the conductor; (b) new closed words in question-vocabulary.json (`not a role`, `yes`/`no`) read by
  code and recorded by the driver - a new reader and a driver writer of the registry. **Recommend (a)** (no new reader; AR-17). Builder: (a).

No new fork in revision 3: every N-finding was applied on the Lead's direction (N3 by the Lead's narrower scope).

Requests for the Lead (not forks):
- **R-1 Ratchet raises to approve before dispatch (AR-20):** `judgment-census.json` `ratchet.safety` 51 -> 52 (PK0-1, `project_knowledge._refuse_no_trace`).
  No other raise is expected: `blocking_per_role` unchanged (no new unit holds a refusal site and gate_preflight.py / project_knowledge.py / stand_gaps.py are
  not on the blocking path, F-27); `word-list`, `meaning-proxy`, `meaning`, `breach`, `blocks_overrides` unchanged; `role-load.json` `ratchet_tokens.qa-test-strategist`
  16718 and `process_ratchet_tokens.qa-test-strategist` 15287 unchanged (one craft paragraph, about 150 tokens, plus the template's optional section, about 7
  lines, against a 1000-token slack - the current measure is U-4, PK0-2 and PK0-3 measure); `driver-layers.json` unchanged (no new Driver name). Any other
  raise in a node = STOP and return.
- **R-2 Remainders queued (fix-the-class):** (i) F-13 for `default`: an unmet default account can still reach three cards (`_probe_actor`, the login keys of
  `check_s5_credentials`, a per-case `default` item) - outside the PK0-4 invariant; a finding file in the pile, one line here. (ii) FK-9 (b) if not taken.
  (iii) (revision 3, N3) the re-review's two further exclusions of item (f) - a role carded at this gate (none of its card's answers makes the runner create
  the account) and a role whose cases are all dropped by `level_applied` / `decisions` - are NOT taken by the Lead's direction ("keep the error direction
  toward asking for every other unknown"); the cost is the default login asked in a story whose only reason is an open role card; a finding file in the pile
  so the owner can weigh it. (iv) (revision 3, S6 note of the re-review) the guard regex of PK0-8, like its sibling at guard_pre_tool.py:1755
  (`environment_record.py record|revoke`), misses a global option written before the subcommand (`project_knowledge.py --task T role`); a shared class of the
  guard, fixed for both siblings at once (a subcommand-anywhere form plus a `--task T role` test), not a text fix of this spec - a finding file in the pile.

Conflicts found in the brief (not guessed): (i) the brief places `resolve_actor` in `project_decisions.py`; it is `manual_capture.py:882` (F-5). (ii) the
brief's S1 decision groups both cards "by (stand, role)": the confirm card's fact has no stand (`product.roles` is project-scoped), so it is grouped by role
with `environment ""` - the same key shape. (iii) the critic proposed `test_judgment_census.py` and `test_install_paths.py` as witnesses; both are in the slow
registry (28.1 s, 10.5 s), so S12 moves them to CI. (iv) (revision 3) the Lead's N1 wording "hash whenever the folded form is empty or not unique among this
packet's roles" and the re-review's "hash whenever the fold loses characters" are reconciled in §3 (2): the lossless-or-hash rule implies uniqueness among the
packet's roles without making an id depend on the other roles; the packet-level check remains as a defensive widening to 16 hex. (v) (revision 3) the Lead
block's line "R-3: stays a stop-and-return" refers to a request this revision removes by the Lead's N2 direction - left untouched (non-goal), for the Lead to update.

## Small choices I closed (no design weight; Lead may reverse)
File `qa-factory/records/project-knowledge.json`, list key `facts`, ids `PK-n`; lock dir `qa-factory/state/.project-knowledge.lock` (10 s); brief cap 15
elements; stand names compared exactly; roles by `_role_form`; config-first write order; card id prefixes `RA-` (role account) and `PR-` (product role),
a sha1 8-hex token for a role form or a stand name whose `_id_token` fold loses characters (N1; kept, not refused - P2), widened to 16 hex only on a collision
inside one packet; a role card's `the test:` names at most `LEVEL_CASES_NAMED` cases then "and N more"; the role/stand clip in the finding lead is 40
characters each; the S6 refusal for no chosen stand reuses `missing_key`; `PK_BY = "project-knowledge"`; the confirm-card recorder call sits in `gate_repair`,
not in a check (FR-45). Revision 3: `product_roles` sits after `unresolved:` and before `blocked:` in the template; its hints say `optional` and avoid `|`
(F-41: a `|` hint parses as a choice); a placeholder or unknown `sign_in` reads as `account`; `_c2` treats `PK_BY` exactly as `ENV_BY` (the stand's address
and a withdrawal still reopen - toward asking, one rule for both records); a mixed carry gets no `--by`; the PK property carries its `gap` id so gate B can
group it; the revoke line for a PK row reads "taken back from the record of earlier answers".

---

## §7 What phase 0 deliberately does not do, and the one sentence each later phase needs from it

| not done here | the sentence the later phase takes from phase 0 |
|---|---|
| catalogue of all keys (phase 1, C5/C6) | "a fact's key is its config path; a row of `records/project-knowledge.json` is `(key, environment NAME, element)` with `state`, `scope`, `provenance`, revocable; the `KEYS` literal (key -> scope, comparator) is replaced by the catalogue (AR-1 debt until then)" |
| the generic seam `need()`, no-hold deferral and the `asked` state (phase 2, C8/C9) | "the reader is the pure `project_knowledge.state()`; the writer is `record()` under the lock, refusing under `no_trace`; `asked` is reserved and has no writer yet" |
| stand selection, stand card, `_stand_of` door (phase 3, В7) | "every stand fact is keyed by the stand's name; an account value stays in config and is written only through `record_stand_account`; until phase 3.4 a project with no `environments[]` row learns roles but NOT accounts" |
| onboarding diet (phase 4, C4) | "a new project starts with an empty registry and learns roles at gate A of its first stories; accounts too once a stand is recorded (phase 3.4)" |
| `needed_by` -> inject-map, project-created kinds (phase 5, C20) | "the roster reaches the strategist as brief lines read from `roster()`" |
| `faq.md` retirement, S9 fold, metrics (phase 6) | "questions avoided by memory = the `Acting on your earlier answers` lines, the `not a role` lines of the decided-once block, plus registry rows by story" |
| moving environments to their own file (В1, node 3.6) | "nothing in phase 0 reads stands by index" |
| price lines on every stand-gap card (FK-9 (b)) | "the new cards carry their own; the shared words do not yet" |

## §8 Live proof (FR-33): two stories on the MyBooks stand

Setup (Lead, a fresh copy of the stand project, NOT `no_trace` - the proof is the memory): `dev` stand recorded with `admin` only in
`credentials_by_role`; the env file holds a second account under `QA_AUDITOR_EMAIL` / `QA_AUDITOR_PASSWORD`; no `records/project-knowledge.json`.
Story A: a ticket whose requirements say "an auditor sees orders read-only; a visitor not signed in sees the catalogue".
1. S3: the brief shows `Product roles: admin: an account on dev`; the handoff lists `auditor` and `guest` in `product_roles`. Witness: brief and handoff.
2. Gate A: the packet holds ONE stand-gap card `RA-dev-auditor` naming only the auditor cases with their titles and three priced answers, and the confirm
   cards for `auditor` and `guest`; no default login card if every executed case names a recorded account, seeds nothing and the plan automates nothing
   (FK-3 as amended). Witness: `work/gate-a-message.md`; `records/project-knowledge.json` has two `noticed_unconfirmed` rows and nothing else.
3. The person answers "the auditor account is QA_AUDITOR_EMAIL / QA_AUDITOR_PASSWORD; guest is a role; auditor is a role". The conductor runs
   `project_knowledge.py account` and `role`. Witness: the printed `auditor on dev: recorded (DD-n, PK-n)`; `show --json`.
4. The story ends (S9): the `restore_config` line says the pointer was kept "written by project decision". Witness: the report's revert line and
   `config.json` holding `auditor`.
Story B (same stand, a ticket touching auditor screens, and one case declaring a role `superuser`):
5. S3 brief lists `auditor: an account on dev (the person, <story A>)` and `guest: no sign-in`. Gate A: no auditor card; the note `Acting on your earlier
   answers: the account of "auditor" on "dev" (given in <A> on <date>)`; a `RA-dev-superuser` card. The person answers "superuser is not a role of this
   product"; the conductor runs `role --state not_needed` and records `accept` for the card. Witness: the packet, the brief, `show --json`.
6. Story C (or a re-run of B's gate on a fresh copy of the story): no superuser card; the "Decided once" line names the answer, the story and the date and
   its case is carried as not run; at gate B the case is shown covered, not asked. Then `RA-dev-superuser: ask again` -> the next rehearsal shows the card.
   Witness: the packet before and after, the gate B packet, `show --json`.
7. Revoke check: `project_knowledge.py revoke --id <guest row>` then the S3 brief of a later run shows `guest` gone. Witness: show + brief.
Pass = steps 2, 4, 5, 6 seen as described; any second auditor question in story B, or a superuser account question in step 6 (gate A or gate B), fails the proof.

---

## Trail

Revision 3 read (this round): the re-review r2 whole (217 lines); the revision-2 spec whole (915 lines); PKG/scripts/story_run.py 18965-19069
(`carry_environment_properties`, `_level_remedies`, `revoke_environment_properties`); PKG/scripts/stand_gaps.py 385-414 (`decisions`, `gap_cases`), 640-736
(`_c2` tail, `_c3`, `_c4`), 759-798 (`carried_change`, `gate_b_answers` head), 890-928 (`gate_b_split`), 929-1093 (`covered_entries` .. `level_applied`),
1093-1106 (`record_lasting`) (+ def grep); PKG/handoffs/s3-strategist-to-designer.yaml whole; PKG/scripts/handoff.py 28-41 (OPTIONAL_WORDS), 425-464
(`_spec_of_value`, `REQUIRED_LISTS`), def grep (`parse` :168, `is_placeholder` :662-664); PKG/scripts/handoff_check.py 2388-2416 (`_apply_one` tail);
PKG/scripts/gate_preflight.py 3425-3446 (`_environment_cover` tail), 4800-4830 (`_card_items`), grep `def precondition_gap_id|def _id_token|def _role_form`
(:1084-1089, :1131-1135, :802-805), grep `shared\s*=` (:4170, :4661, :5335); PKG/scripts/contract.py 514-535 (`stand_gap_decisions`); PKG/scripts/waiver.py
grep `"--by"` (:1574); PKG/scripts/person_owned.py 160-173. Searches: `ENV_BY|ER\.says\(` over PKG/scripts/*.py (19 hits; positive: stand_gaps.py:547, :989
present); `get\(["']by["']\)` over PKG/scripts/*.py (stand-gap `by` read only in stand_gaps.py; positive: stand_gaps.py:669, :711 present).
Not read this round: `handoff_check._open_rows_for` (U-5), the handoff_check check path end to end (taken from the re-review's read and 0-hit search with its
positive control, F-41), `gate_brief._covered_block` beyond F-36's lines, `project_knowledge` (does not exist yet).

Revision 2 read: the verdict whole (469 lines); the revision-1 spec whole (638 lines); PKG/scripts/gate_preflight.py 796-835, 1122-1137,
1150-1324, 1947-2006, 4438-4491, 4640-4936, 5207-5223 (+ def grep); PKG/scripts/stand_gaps.py 1-285, 930-1009, 1094-1153 (+ def index); PKG/scripts/gate_brief.py
883-997, 1387-1426, 1484-1745 (+ def index, price-line grep); PKG/scripts/contract.py 449-507 (grep); PKG/references/question-vocabulary.json 22-113 (grep);
PKG/scripts/story_run.py 13584-13653, 16518-16573, 18470-18579, 18973-19065 (grep -A) (+ def grep); PKG/scripts/planning_contract.py 2576-2606 (grep -A);
PKG/scripts/handoff.py 440-589; PKG/scripts/guard_pre_tool.py 1698-1772, 2239-2314 (grep); PKG/scripts/project_decisions.py 529-552, 578-647;
PKG/scripts/manual_capture.py 940-975; PKG/agents/qa-runner.md (grep `as default` :57); PKG/references/human-questions.md 15-74; PKG/scripts/slow_tests.json whole;
PKG/scripts/tests/fixtures/judgment-census.json 1-14 (+ grep of the touched rows); PKG/scripts/tests/test_judgment_census.py 1-48 (+ grep of defs/constants);
PKG/references/role-load.json 3-40; PKG/scripts/selftest.py (grep `--limits`); PKG/scripts/refusal_registry.py (grep argparse :940-942);
`D:/ws2/wt-fbfix/plans/piles/thinking-roles/batch-3-parallelnost.md` 1-20 and the node table :22-39.
Searches (negatives with a same-shape positive control): `gate_preflight` in references/stages.json -> no hit (control: `\.py` -> 11 hits in the same file);
`очередь` in batch-3 -> no hit (the order line is :8 "Порядок по общим файлам", read directly); tests files by Glob (slow registry cross-checked by reading it whole).
Not re-read in revision 2 (taken from revision 1 / the verdict's confirmations): config_contract.py ranges (F-16..F-18), environment_record.py (F-1), brief_pack.py
(F-8, F-25), manual_evidence.py (F-7), external_writes.py (F-21), environment_selection.py (F-23), templates/config.json:67 (F-6).
