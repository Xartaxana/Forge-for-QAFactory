# PK2-21 - S6 after the gate A accept of the stand's default account (draft spec)

task: t-1593 | node: project-knowledge/2/PK2-21 | feature: F19 | designer draft, 20.11.2026 | status: DRAFT for Lead acceptance
source finding: `plans/piles/project-knowledge/findings/20261119-s6-sprashivaet-default-posle-prinyatiya-na-gate-a.md` (builder t-1581).
Depends on: PK2-6a (`worktree-agent-a4a22bcf665bc7cc1`, head 92a89f11, not merged) - the PRODUCER of the gate A accept record (fork F1).

Line numbers are reading aids measured by Read/Grep on 20.11 (main working tree; the PK2-6a branch read through its worktree
`.claude/worktrees/agent-a4a22bcf665bc7cc1`, whose ref `.git/refs/heads/worktree-agent-a4a22bcf665bc7cc1` = `92a89f1167d4...` - the
worktree's uncommitted state is an `estimate`: the Lead confirms with `git -C C:/QAFactory/forge-repo show 92a89f11:ai-packages/qa-factory/scripts/tests/test_gate_role_accounts.py`).

## 0. The two variants, and what the person sees

Today (measured): the gate A card `s5_environment-default-login` (PK2-6a, `gate_preflight.py::Rehearsal._default_account_check`, branch :4753)
says in its fix "or accept the gap and let the stage report those cases as not executed" plus the door `s5_environment-default-login: accept`;
the door's `waives` is `{"block": "the stand's default account", "stage": "S5", "option": "accept"}` (branch test :598). At S6
`driver_stage_s6.py::Driver.stand_login_gate` (:1168) asks `stand_login_problem(screens)` (:1014) and passes only
`waiver.split_overridden([STAND_LOGIN_BLOCK], pipeline, "S6")` (:1196) - stage S6 only (`contract.live_stage_overrides(pipeline, (stage,))`),
block `stand login missing`. So the S5 record of another block is never read: the person is asked the S6 sign-in question again.

**Variant (a) - recommended (fork F0).** The live gate A accept lifts S6's default-account part of the question.
- At S6: NO question about the default account. Each screen case that signs in with the default account is left, one printed line per case:
  `S6: TC-1: not checked by hand — not checked by an agent: the stand's default account is not set up for the factory; at gate A you accepted going on without it: "<the person's words>"`
- Screen cases whose request names another account (a role, an `env:` pair) go on: their own account is read as today; a role whose
  account is missing still gets today's question, naming only those cases. http-only cases: untouched.
- In the S8 report (`report_facts._refusal` reads `request.json` `refused.reason` / `refused.door`, :1149): the case is in the manual
  section as not checked, reason = the line above after the dash, door = today's door "put the stand's test account in the project's
  settings; the next run checks it by hand"; `refused.by = left_unchecked` (the delivery check makes no claim that the person checks it).
- The card's own promise ("let the stage report those cases as not executed") becomes true; no text of PK2-6a changes.

**Variant (b).** S6 asks again but names the earlier accept.
- At S6: today's `stand_login` question (`stand_login_question_text`, :1143) with one sentence added after "I cannot find that account: <reason>.":
  `At gate A you accepted going on without the stand's default account ("<the person's words>"); these screens cannot be opened without it, so I ask once more.`
  Options unchanged: `retry` / `by hand` / `go on` (FR-7: a question asked again changes its text).
- In the S8 report after `go on`: today's reason `not checked by an agent: the stand's sign-in account is not set up for the factory; the person said: "<S6 words>"`, `by: left_unchecked`; after `by hand`: `by: person_checks`.
- Cost: two answers for one decision (AR-13, AR-15 "decided once"); the gate A card's fix text becomes untrue and must change in
  `gate_preflight.py` (PK2-6a's file) - "the stage asks you again before it leaves them".

The rest of this card is written for (a). Delta for (b) is §9.

## 1. Invariants, owners, variety

AR-n touched (`ai-packages/qa-factory/design/architecture.md`), each with its change check for the DoD:
- AR-13 (one reader) - the person's word is read only through `waiver._override_hits` / `contract.live_stage_overrides`; the block text
  has ONE definition (`waiver.DEFAULT_ACCOUNT_BLOCK`, like `STAND_LOGIN_MISSING_BLOCK`, t-722 N5); the default-account material only through
  `manual_capture.read_login`. Change check: grep the package for the literal `the stand's default account` - one definition, the rest names.
- AR-15 (one survivor) - the "decided once" for the default account: one record (gate A's), read by gate A and S6. Change check: the report
  names every reader of `DEFAULT_ACCOUNT_BLOCK` before/after.
- AR-19 (stage twins) - the gate A card and the S6 sign-in question are twins (`default_login_needed` docstring, `gate_preflight.py` :726);
  this node changes the S6 side to read the gate side's answer. Twins not changed here: §8 F6 (named, with nodes).
- AR-28 (unknown never a pass) - a revoked, placeholder, empty, unreadable or absent record is no word: S6 asks as today. A settings
  file that cannot be loaded is not "the default account is missing" (fork F3). Test rows T2, T3, T9 pin it.
- AR-16 (one question form) - the new reason text passes `human_text.problems`; the question text is byte-unchanged (variant a).
- AR-14 (one writer) - the refusal record is written only by `Driver.refuse_case` (`driver_dialog.py` :227); no new artifact.
- AR-25 / FR-40 (a way out of every state) - `design/state-exits.md` row 72 gains the new way in (the gate A accept) and its way out
  (`waiver.py --revoke --stage S5 --block "the stand's default account"`, or the account in the settings).
- AR-29 - the check this spec alters is the S6 stand-login gate's lift (not a census unit: `stand_login_gate` / `stand_login_problem`
  do not match `UNIT_NAME_RE`, `tests/test_judgment_census.py` :77; the new names below are chosen outside it). Owner: **intent** (the
  person's recorded word lifts a credential question), census class: none (no unit). Commit line: the `judgment:` line in the form
  `tools/architecture_gate.py` checks (the only carrier of the grammar; not copied here) - `judgment: none -- <why: no census unit added
  or altered; the lift reads the person's recorded word (owner intent)>`, never bare.
- AR-17 - no new driver stop; the `stand_login` seam question is unchanged.

Variety walk (§ A):
- axis 7: held by key -- `environment.env_file(s)` / `user_key` / `secret_keys` read by `manual_capture.read_login`, plus the person's
  recorded word in `stage_overrides`; unknown value -> no word is read, the S6 question is asked as today.
- axes 1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13: n/a -- the change only lets S6 read an answer gate A already recorded; it reads no product,
  surface, runner, tracker, delivery, host, process, language, size or age value. (Axis 2 device stands: the default account is not read
  for a block all on a device stand, `_cases_all_on_driver` - unchanged, edge E13.)

One road (P31): every project and language reaches the same reader; no case is left out (http-only cases are no exception: they
never sign in, unchanged).

## 2. Behaviour (variant a)

Position in `Driver.stand_login_gate` (order is load-bearing):
1. `screens` as today; `if not screens: return` (unchanged; `test_manual_actor.py` :377 pins the order - quarantined, not run).
2. `kind, details = self.stand_login_problem(screens)`; `if not kind: return` - **the accept is read ONLY while the material is missing**
   (a stale accept never blocks a working account, E2).
3. The S6 own word (`split_overridden([STAND_LOGIN_BLOCK], ..., "S6")`) passes -> today's road, byte-identical (E7).
4. NEW, only when 3 found no pass: `words = waiver.default_account_word(self.pipeline())`. Empty -> today's question (step 5).
   Non-empty -> `left = self.default_login_gap(screens)`:
   - `left` = the screen cases that sign in with the default account WHEN its material cannot be read: a case whose prepared request names
     `stand_account` `default` (trimmed, as :1093), names no `stand_account`/`env` actor, or is absent/unreadable (the partition :1068-1082
     already uses); `[]` when the default material reads, when `login_declared_none`, when all cases are on a device stand, or when
     `load_config` raises (F3).
   - each case of `left` -> `refuse_case(plan, case, reason, door, "left_unchecked")` + the printed line (§0);
   - `rest = [c for c in screens if c not in left]`; `kind, details = self.stand_login_problem(rest, default_settled=True)` (the default
     reads of :1059 and :1079 are skipped; role/env reads as today); `not kind` -> `plan["blocks"] = manual_blocks(<ready minus left>, ...)`,
     return; else today's question for `rest` only (`person.login_cases = person.holds = rest`), with `left` already refused.
5. Today's question (unchanged text, unchanged Person fields).

POSITION invariant: a word about the default account is consulted only after (i) a problem stands and (ii) the person's own S6 word did
not pass it; so it can never lift a question whose cause is a role's account, a missing stand (`no_stand`) or a broken settings file,
and it never overrides the typed `by hand` record of the S6 word.

`waiver.default_account_word(pipeline) -> str` (new, pure, never raises): the `decision` of the first live record over
`DEFAULT_ACCOUNT_STAGES = ("S5", "S6")` whose `match`, folded (`_fold`), EQUALS `_fold(DEFAULT_ACCOUNT_BLOCK)` (fork F4: no `*`, no
partial name); built on `contract.live_stage_overrides` (revoked / empty decision dropped) and `PLACEHOLDER_RE`; "" otherwise, also for a
pipeline that is not a dict.

## 3. Edges (behaviour + invariant)

| # | edge | behaviour | invariant |
|---|---|---|---|
| E1 | gate A accept live, default keys still absent at S6 | no question; default-signing screen cases refused with the accept's words, `by: left_unchecked`; the rest go on | one decision, one record: the default account is not asked twice while the word stands (AR-13); a left case is never reported checked |
| E2 | accept live, keys present at S6 | `stand_login_problem` -> ""; return before the word is read; cases run | a stale accept never blocks a working account |
| E3 | no gate A accept (today) | today's question, byte-identical text and Person fields | absence of a word never removes a question (AR-28) |
| E4 | screen case signing in as `default` vs one naming a role vs an http-only case | only the first is left; the role case's account is read and asked about if missing (question names it only); http-only never asked, never left | an accept about the default account never passes a role's account or a case that needs no sign-in |
| E5 | accept revoked (`revoked_at`) before S6 | `live_stage_overrides` drops it -> today's question | a revoked word acts nowhere (FR-40) |
| E5b | accept revoked AFTER S6 left the cases | the refused records stay (written with the words of that moment); the next S6 entry dispatches nothing already refused; the revocation acts at the next read, as `recheck_stage_block` says for revocations | a refusal record is bound to the words it was made with |
| E6 | PK2-6a NOT merged (world before) | no producer writes the record; `default_account_word` reads "" -> today's behaviour exactly; a person's hand-recorded `--stage S6 --block "the stand's default account"` passes via the `block-names.json` row | the change adds no pass without a record |
| E6b | PK2-6a merged | gate A card's door writes the S5 record -> E1 | the card's promise "the stage reports those cases as not executed" holds |
| E7 | S6 own word `stand login missing` AND the gate A accept both live | step 3 wins: today's road with the S6 words and the typed `login_choice` | the `by hand` record stays bound to its own pass |
| E8 | `pipeline.json` unreadable / `stage_overrides` not a list / pipeline not a dict | no word -> today's question | unknown is no pass |
| E9 | record `match` holds a `<placeholder>`; `decision` empty or whitespace | no word | a placeholder or an empty word is no word |
| E10 | S5 record with `match` `*`, or a partial name (`account`, `default account`) | no word (F4) | a blanket or partial word at gate A never lifts an S6 credential question |
| E11 | `load_config` raises (settings file absent/broken) | `default_login_gap` -> []; today's question (`missing_file`) | a broken settings file is not "the default account is missing" (F3) |
| E12 | problem is a role's (`missing_key` for `admin`) or `no_stand`, default material reads | `left` = []; today's question | the accept lifts only the default account |
| E13 | all screen cases on a device stand (`_cases_all_on_driver`) | default not read (EP1-41f); `left` = []; role reads as today | unchanged device road |
| E14 | `default_login_needed` False, every request names a role | default never read; `left` = [] | no new read, no new question |
| E15 | `default_login_needed` True (automate rule) but every screen case names a role | `left` = []; re-check with `default_settled=True` -> "" -> cases go on with their role accounts | the default account needed only by S5 does not hold S6 role cases once accepted |
| E16 | every screen case left | `plan["blocks"]` = the non-screen ready cases (possibly none); the C4 rule closes the half code-only as today | an emptied block list is the existing close, not a new state |
| E17 | the person's words long / multi-line / with a BOM | squashed as today's `said` (`" ".join(...split())`, BOM removed); no cut (today's reason has none) | the report quotes the person's words whole |
| E18 | the record is at stage S6 (hand-recorded) rather than S5 | read (S5 first, then S6) | one word per decision, wherever it was recorded |

Reuse in a more consequential role: `_override_hits` / `live_stage_overrides` (S6 reads an S5 record to lift a credential question).
Error direction: toward "no word" (ask). Adversarial inputs that must stay on the asking side: `*` at S5, a partial name, a placeholder,
`revoked_at`, an empty decision, a non-dict pipeline, a non-list `stage_overrides`, a record of another stage (S4, S7).

## 4. Builder node PK2-21a (variant a)

given: this spec §0-§3, §5; the finding (path above); `scripts/driver_stage_s6.py::Driver.stand_login_gate`, `::Driver.stand_login_problem`, `::Driver.stand_login_question_text`; `scripts/waiver.py::split_overridden`, `::_override_hits`, `::stand_passing_override`, `::STAND_LOGIN_MISSING_BLOCK`, `::PLACEHOLDER_RE`, `::_fold`; `scripts/contract.py::live_stage_overrides`; `scripts/driver_dialog.py::refuse_case`; `scripts/gate_preflight.py::DEFAULT_ACCOUNT_BLOCK` and `::Rehearsal._default_account_check` (PK2-6a); `scripts/tests/test_login_need.py` (S6 section :211-309, `FakeCapture`, `driver_over`, `request`); `scripts/tests/test_refuse_case.py` :60-130 (a driver for `stand_login_gate`); `scripts/tests/test_gate_role_accounts.py::test_s6_still_asks_after_the_default_account_accept`
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\driver_stage_s6.py
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\waiver.py
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\gate_preflight.py
C:\QAFactory\forge-repo\ai-packages\qa-factory\references\block-names.json
C:\QAFactory\forge-repo\ai-packages\qa-factory\design\state-exits.md
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_login_need.py
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_gate_role_accounts.py
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\driver-layers.json
C:\QAFactory\forge-repo\ai-packages\qa-factory\CHANGELOG.md
non-goals: no change of `default_login_needed` (PK0-5); no change of the gate A card's text or road (PK2-6a); no change of the `stand_login` question text, its tokens or `_take_stand_login_answer`; `gate_preflight.py` gets only `DEFAULT_ACCOUNT_BLOCK` taken from `waiver` (one line); no `OWN_FORM_BLOCKS` member (`test_waiver_release.py::own_form_table` pins four); no edit of quarantined `test_manual_actor.py` or canon-only `test_story_run_s6_*.py`; the twins of §8 F6
handoff: the branch + report: the grep of the literal `the stand's default account` before/after (one definition), the witness tail, `tests not written:` lines, `red-before:` for T1 (`red-before: <cmd> -> <tail>` before the code)
edges: §3 E1-E18 of this spec, each with its invariant (inline there; rows T1-T10 pin E1-E5, E7, E10-E12, E15)
DoD: `python -m pytest ai-packages/qa-factory/scripts/tests/test_login_need.py ai-packages/qa-factory/scripts/tests/test_gate_role_accounts.py "ai-packages/qa-factory/scripts/tests/test_refuse_case.py::test_stand_login_gate_writes_the_same_bytes" -q` and `python -B ai-packages/qa-factory/scripts/tests/test_state_exits.py` (estimate: canonical form of that harness-style file; the Lead confirms) and the narrow layer check of the new Driver name (estimate: `test_driver_layers.py` is on the slow list, 32.4 - the Lead names its narrow call, e.g. its `real_maps()`)
siblings: `waiver.stand_passing_override` (the S5+S6 precedent of one word read at two stages; unchanged); `Driver.manual_gate_note` (`gate A recorded dry`, an S6 reader of a gate-A fact; unchanged); twins not changed here: §8 F6
designer: C:\QAFactory\forge-repo\docs\tasks\specs\20261120-pk2-21-s6-after-gate-a-card.md
test: ai-packages/qa-factory/scripts/tests/test_login_need.py::test_s6_after_the_gate_a_accept (new table, rows T1-T9 of §5, top-down; next to the file's S6 section) | expected from: §2-§3 of this spec; the gate A card's own fix text (PK2-6a branch `gate_preflight.py` :4782-4783)
test: ai-packages/qa-factory/scripts/tests/test_gate_role_accounts.py::test_s6_still_asks_after_the_default_account_accept flipped in place (row T10 of §5) | expected from: the finding's "Тест" line; §2 `default_account_word`

Work items:
1. `waiver.py`: `DEFAULT_ACCOUNT_BLOCK = "the stand's default account"` beside `STAND_LOGIN_MISSING_BLOCK` (not in `OWN_FORM_BLOCKS`);
   `DEFAULT_ACCOUNT_STAGES = ("S5", "S6")`; `default_account_word(pipeline) -> str` as §2 (docstring: error direction, the adversarial list).
2. `gate_preflight.py`: `DEFAULT_ACCOUNT_BLOCK` becomes the name taken from `waiver` (module-level import; `waiver` imports no
   `gate_preflight` at module level - measured, `waiver.py` :100-111; the builder confirms no cycle by importing both).
3. `driver_stage_s6.py`: `stand_login_problem(cases=None, *, default_settled=False)` - when True the two default reads (:1059, :1079)
   are skipped, everything else unchanged (existing callers pass nothing). New `Driver.default_login_gap(cases) -> list` (§2; reads the
   default material once through the same `read_login` mapping as `read_default`, factored, not copied). `stand_login_gate`: step 4 of §2;
   docstring states the POSITION invariant. Reason/door constants beside `STAND_LOGIN_REASONS`.
4. `references/block-names.json`: row `{"block": "the stand's default account", "reader": "waiver:default_account_word", "stages": ["S6"]}`
   (fork F5).
5. `driver-layers.json`: the row of `Driver.default_login_gap` (home `driver_stage_s6`, the row number of `stand_login_problem`).
6. `design/state-exits.md` row 72: the way in (gate A accept, S5 record) and the way out (revoke at S5, or the account in the settings).
7. `test_gate_role_accounts.py`: flip §5 T10. 8. `CHANGELOG.md`: one entry (English, no Cyrillic).

## 5. The test table (one parameterised test, strongest first)

Place: `scripts/tests/test_login_need.py` (scenario, "one rule for gate A and S6", not slow, not canon-only - measured: `slow_tests.json`
has no row for it, control `test_driver_layers.py` found; `test-layers.json` :2887). One world per row: `story(...)` + `request(...)`, a
`pipeline.json` with `stage_overrides`, `FakeCapture(refuse=...)` for the default (`actor=None`) and role reads; the driver of
`driver_over` given `state = {}`, `plan = {"blocks": [cases], "refused": []}`, `manual_policy` -> `"ui"` (an http case -> `"api"`),
`site_seam_person` stubbed to return a raisable recorder. Expected = (Person raised?, its `holds`, refused ids, `by`, reason contains).

| row | world | expected |
|---|---|---|
| T1 | S5 record `the stand's default account`, decision "go on without it"; default read refused; TC-1 request no actor, TC-2 unreadable request | no Person; TC-1, TC-2 refused, `by` `left_unchecked`, reason has "at gate A you accepted" and the words; blocks empty (E1) |
| T2 | T1 + `revoked_at` | Person; holds (TC-1, TC-2); nothing refused (E5) |
| T3 | no record | Person; question text == `stand_login_question_text(screens, kind)` of today (E3) |
| T4 | T1 record, default read lands | no Person, nothing refused, blocks unchanged (E2) |
| T5 | T1 + TC-3 with `stand_account: admin` whose read is refused | TC-1, TC-2 refused; Person holds (TC-3,) only (E4, E12) |
| T6 | T1 + S6 record `stand login missing`, `login_choice` by hand with the same words | today's road: reason "the person said", `by` `person_checks` (E7) |
| T7 | variants of the record: `*` at S5; `default account`; `<placeholder>`; empty decision; stage S4 | Person, nothing refused (E9, E10) |
| T8 | T1 world with every case `stand_account: admin` (read lands), automate row (default needed) | no Person, nothing refused (E15) |
| T9 | T1 world, `load_config` raises | Person (`missing_file`), nothing refused (E11) |
| T10 | (in `test_gate_role_accounts.py`, flipped) the S5 record of `GP.DEFAULT_ACCOUNT_BLOCK` | `waiver.default_account_word` returns its words; control: `split_overridden([STAND_LOGIN_MISSING_BLOCK], ..., "S6")` unchanged |

Also every reason/printed text of T1 passes `human_text.problems` (one assert inside T1, not a row). The builder writes rows top-down
until test lines reach code lines and reports the rest as `tests not written: <row> -- over budget`.

The flipped row (exact): file `ai-packages/qa-factory/scripts/tests/test_gate_role_accounts.py` on 92a89f11, function
`test_s6_still_asks_after_the_default_account_accept` (worktree :619-625), docstring "Known, PK2-21: S6 passes only
`STAND_LOGIN_MISSING_BLOCK`, so the accept of the gate-A card does not carry to it (control: its own word does)", assertion
`passed(GP.DEFAULT_ACCOUNT_BLOCK) == [] and passed(waiver.STAND_LOGIN_MISSING_BLOCK)`. It is a standalone test, NOT a row of the
`DEFAULT_ROWS` table (the brief's "table row" wording differs; the docstring names PK2-21, not "PK2-6-s6"). Flip: renamed
`test_s6_reads_the_default_account_accept`; asserts `waiver.default_account_word(pipe)` is the words for a record at S5 (the card's
`waives` stage) and "" with `revoked_at`; keeps the control line.

## 6. Readers of every touched file

No `tools/owns_readers.py` block was attached; the designer has no shell. The Lead runs (label `estimate` until attached):
`python -B tools/owns_readers.py --paths ai-packages/qa-factory/scripts/driver_stage_s6.py ai-packages/qa-factory/scripts/waiver.py ai-packages/qa-factory/scripts/gate_preflight.py ai-packages/qa-factory/references/block-names.json ai-packages/qa-factory/design/state-exits.md ai-packages/qa-factory/scripts/tests/fixtures/driver-layers.json --names stand_login_gate stand_login_problem default_login_gap default_account_word DEFAULT_ACCOUNT_BLOCK DEFAULT_ACCOUNT_STAGES --readers`
Hand reads (Grep tool, counts with controls):

| reader | reads | verdict |
|---|---|---|
| `driver_machine.py::_take_stand_login_answer` (:4033), `driver_dialog.py` :355 (`login_cases`), `driver_core.py` :261 (`holds`) | the Person `stand_login_gate` raises | unchanged: same Person; in T5 `holds`/`login_cases` = the rest only (the documented meaning: the cases that wait) |
| `test_login_need.py` S6 section (:254-309) | `stand_login_problem(cases)` | unchanged (new keyword defaults False); changes in this node (new table) |
| `test_refuse_case.py` :67-129 (stubs `stand_login_problem = lambda screens:`) | the S6-word road bytes | unchanged: the stub sees one arg because the new branch is after the S6-word pass (§2 POSITION); in the DoD |
| `test_silent_passes.py` :722, `test_walk_road.py` :434 | stub `stand_login_gate` whole | unchanged |
| `test_story_run_deferred.py` :66, `test_story_run_s6_t292.py`, `test_story_run_s6_c16b.py` | the question and the S6-word pass | unchanged (canon-only, not run locally; CI) |
| `test_story_step_manual_block.py` :671 K-T2 | `"manual_blocks(" in getsource(stand_login_gate)` | unchanged: the new branch also re-chunks through `manual_blocks` |
| `test_manual_actor.py` :375-377 | `if not screens:` before `stand_login_problem(screens)` in the source | order kept; quarantined, not run |
| `test_gate_registry.py` :47, :73, :844 | gate row `stand_login_gate` | unchanged (name kept) |
| `fixtures/driver-exits/s6-s9.json` :300-305 | `stand_login` raised at `driver_stage_s6:stand_login_gate` | unchanged (no new Person site) |
| `fixtures/driver-layers.json` :669, :672, :1083, :1169, :1211 | homes; `login_cases` writer; `login_choice` | changes in this node (row for `default_login_gap`) |
| `waiver.py` importers (the driver set, `story_step`, gate tools) | existing names | unchanged: names only added |
| `test_waiver_release.py::own_form_table` (:881-895) | `OWN_FORM_BLOCKS` has 4 str and their rows | unchanged: not a member |
| `waiver.load_block_names` / `block_name_row` / `record_class` (:603-650); `contract.py` (2), `check_delivery.py`, `driver_core.py`, `driver_runner.py`, `grounding_table.py` (1 each); tests `test_decision_classes.py` (5), `test_silent_passes.py` (2), `test_check_delivery.py`, `test_probe_not_proved.py` | `block-names.json` rows | changes in behaviour: recording `--stage S6 --block "the stand's default account"` is accepted as a name its reader acts on; no `class` field, so no class reader acts; the loader validates `waiver:default_account_word` |
| `tools/source_split.py` :2755-2822, `tools/source-split-carriers.json` :17 | `block-names.json` reader form on a split | unchanged (a module function, not a mixin method) |
| `test_state_exits.py` | `design/state-exits.md` doors exist | changes in this node (row 72); in the DoD |
| `gate_preflight.py` users of `DEFAULT_ACCOUNT_BLOCK` (branch :729, :4783; test :557, :598, :625) | the name | unchanged value; changes in this node (source of the name) |
| `report_facts.py::_refusal` (:1149), `check_delivery.py` :1027 | `request.json` `refused` | unchanged reader; new reason text in the same field |
| `.githooks/` | none: Grep `stand_login|block-names|split_overridden` = 0 (control `python` = 18) |
| `tools/` | `stand_login_*`, `STAND_LOGIN_MISSING_BLOCK` = 0; `block-names.json` = 5 (rows above); `driver_stage_s6` = 0 (control: same Grep finds `block-names.json`) |

## 7. Readers on the PK2-6a side

`test_gate_role_accounts.py::DEFAULT_ROWS` R6 ("accepted (E5)") and R11 use `override(task, GP.DEFAULT_ACCOUNT_BLOCK)` - value unchanged,
unchanged verdict.

## 8. Forks (for the Lead)

- **F0 - the variant.** (a) the gate A accept lifts S6's default-account part [recommended: one decision, one record (AR-13/AR-15); the
  card already promises "let the stage report those cases as not executed" - (b) makes that text untrue; the precedent
  `stand_passing_override` reads one word over S5 and S6]. (b) ask again naming the accept - a second answer for one decision, a text
  change in PK2-6a's card, and the `go on` answer re-records what was said at gate A.
- **F1 - build order (PK2-6a merged vs not).** (i) build PK2-21a on top of the PK2-6a branch after the owner's census word merges it
  [recommended: the flipped test and the record's producer exist only there; one merge]. (ii) build on main now: E6 holds (no producer,
  today's behaviour), the constant lives in `waiver.py` first and PK2-6a's line :729 conflicts at merge; the T10 flip waits as a one-line
  follow-up. Producer of the record: PK2-6a's card door (`waives`, stage S5) and the existing gate A word recorder - owned by PK2-6a.
- **F2 - which screen cases the accept leaves.** (a2) only those that sign in with the default account (request names `default`, no
  account, or is unreadable) [recommended: the card names only the cases signing in with the default account; role cases keep their own
  account; `estimate`: that a case naming a role does not also need the default session - the Lead checks with
  `Grep "def read_login|actor=None" ai-packages/qa-factory/scripts/manual_capture.py` and the capture's sign-in]. (a1) every screen case
  of the block, as the S6 own word does today - simpler, but leaves role cases whose accounts are present.
- **F3 - a settings file that cannot be loaded (`load_config` raises).** (a) not covered by the accept: asked as today [recommended:
  AR-28; the gate A card is about absent keys, a broken config is another fact]. (b) covered (kind `missing_file` is shared today).
- **F4 - which records count.** (a) exact block (folded), stages S5 then S6, no `*`, no partial name [recommended: `_override_hits`'s
  `names_whole` would let `account` or an S5 `*` lift an S6 credential question]. (b) reuse `_override_hits` as is (S5 `*` passes, as for
  the stand block today).
- **F5 - the `block-names.json` row.** (a) stages `["S6"]`, reader `waiver:default_account_word` [recommended: S6 hand-recording works;
  gate A's recording stays as PK2-6a built it]. (b) `["S5", "S6"]` - turns the S5 record into an own-form name at gate A, which changes
  the recording message there (`waiver.py` :1182-1185) - PK2-6a's reach. (c) no row - a hand-recorded S6 word would be held against a
  standing refusal that does not hold it.
- **F6 - twins: other places that may re-ask a gate A accept (AR-19), `estimate` each.** (i) a role card `RA-<stand>-<role>` accepted at
  gate A (PK0-4) - S6 `stand_login_problem`'s role loop and `driver_dispatch.py::walk_account` (:3690) read no stand-gap answer;
  measure: `Grep "stand_gap_decisions" ai-packages/qa-factory/scripts/driver_stage_s6.py ai-packages/qa-factory/scripts/driver_dispatch.py`.
  (ii) S5's automate run after the accept (the card's "S5 needs credentials"): no reader of `DEFAULT_ACCOUNT_BLOCK` outside
  `gate_preflight.py` on the branch (Grep over the worktree package: gate_preflight 3, test_gate_role_accounts 3). Recommendation: two
  nodes in this pile with owns and a test (PK2-21b role-card accept at S6; PK2-21c S5 automate after the default accept), each opened
  by the measurement above; not widened into PK2-21a (other stage, other reader).

## 9. Variant (b) delta (if F0 = b)

Owns: `driver_stage_s6.py`, `waiver.py` (the reader, item 1), `gate_preflight.py` (card fix text), `test_login_need.py`,
`test_gate_role_accounts.py`, `CHANGELOG.md`. `stand_login_question_text(cases, kind, accepted="")` adds the §0 sentence when `accepted`;
the gate passes `waiver.default_account_word(...)` only when the problem is the default account's. Rows: T3 becomes "text has the accept
sentence"; T1 becomes "Person raised, text names the words"; T5-T9 as §5. The question changes text -> `human_text.problems` and the
`question-prices.json` key `s6.stand_login` unchanged (same options).

## 10. Small choices closed by the designer

- The constant moves to `waiver.py` (the home of every factory block name, t-722 N5); `gate_preflight` takes the name.
- Not added to `OWN_FORM_BLOCKS` (the driver's own `--block` literals; pinned at four by `own_form_table`).
- Own `DEFAULT_ACCOUNT_STAGES` rather than reusing `STAND_STAGES` (same values, another fact).
- Door text reused verbatim from today's S6 pass; `by` is `left_unchecked` (an accept is not "by hand").
- New names avoid `UNIT_NAME_RE` (`default_account_word`, `default_login_gap`): no census row.
- The test table goes to `test_login_need.py` (the S6 half of the one rule already lives there), not a new file.

## 11. Contradictions and notes for the Lead

- The brief calls the flipped item a "table row ... (known, finding PK2-6-s6)"; on 92a89f11 it is the standalone function
  `test_s6_still_asks_after_the_default_account_accept` whose docstring says "Known, PK2-21" (§5).
- The brief's DoD asks for "the chosen variant": the choice is F0, returned; the card is drafted for the recommended (a), with (b)'s delta.
- `test_waiver_release.py::own_form_table` expects readers `story_run:Driver.*` while `block-names.json` holds `driver_stage_s6:DriverStageS6.*`
  (a normalisation may exist; not checked, not touched).

## 12. Reading trail

- Read: the finding (whole); PK2-6 spec (whole, incl. Lead decisions); `driver_stage_s6.py` :578-617, :960-1260; `waiver.py` :195-384,
  :389-433 (Grep); `contract.py::live_stage_overrides` :169-185; `driver_dialog.py::refuse_case` :227-237; `driver_dispatch.py` :3760-3802;
  `report_facts.py` :1140-1179; `architecture.md` :33-72, :196-255, :312-335; `references/block-names.json` :1-60; `state-exits.md` :72;
  `test_login_need.py` :205-314; `test_waiver_release.py` :405-434, :880-904; `test_story_step_manual_block.py` :660-676;
  `driver-exits/s6-s9.json` :290-314; `driver-layers.json` :1-12; `test_state_exits.py` :1-30; `test-layers.json` :10-34, :2089-2096,
  :2887-2896, :6886-6897; worktree `gate_preflight.py` :4700-4809, `test_gate_role_accounts.py` :440-630; `.git/worktrees/.../HEAD`,
  `.git/refs/heads/worktree-agent-a4a22bcf665bc7cc1` (= 92a89f11...).
- Greps: `STAND_LOGIN|stand_login_problem|split_overridden` in driver_stage_s6 (8 lines); `stand_login_gate|stand_login_problem` over
  scripts (73 in 20 files) and tests (listed §6); `STAND_LOGIN_MISSING_BLOCK|STAND_LOGIN_BLOCK` (18 in 8); `block-names\.json` (38 in 14);
  `default_login_needed\(` (4 in 3); story_step.py `login` -i = 0 (control `import` = 91: the skill road has no sign-in gate);
  worktree `block-names.json` "default account" = 0 (control "stand login missing" = 1); slow_tests.json: t292 75.8,
  test_driver_layers 32.4, test_login_need / test_gate_role_accounts / test_state_exits / test_refuse_case absent (same Grep found the two);
  `canon_only` = `test_story_run_*.py`, `test_controller_*.py`, `test_fixes_13797.py`, `test_story_step.py`; `UNIT_NAME_RE` :77.
- Size: `estimate` ~30 KB; the Lead measures with `python -B -c "import os,sys;print(os.path.getsize(sys.argv[1]))" docs/tasks/specs/20261120-pk2-21-s6-after-gate-a-card.md`.

## 10. Lead decisions (20.11.2026)

F0 (a): the gate A accept lifts the default-account part of S6. F1 (i): PK2-21a is built on top of PK2-6a after the owner's census word
merges it; until then the node waits. F2 (a2). F3 (a). F4 (a). F5 (a). F6: PK2-21b and PK2-21c are opened as rows when PK2-21a is dispatched,
each after its measurement in §8 F6.
