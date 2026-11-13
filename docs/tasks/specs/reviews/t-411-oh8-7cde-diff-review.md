# t-411 — critic diff gate, pair OH8-7c / OH8-7d / OH8-7e (judgment census rows)

Reviewer: critic (Opus). Read-only. The three commits were read with `git show <sha>:<path>` / `git diff` in
`C:\QAFactory\forge-repo\.claude\worktrees\oh8-7b` (the working tree was never read: the 7f builder writes there). The package at
3589f5b was byte-extracted to my scratchpad (`git archive 3589f5b ai-packages/qa-factory | tar -x`), and every function was read there.

## Verdict per node

| node | commit | verdict | why |
|---|---|---|---|
| OH8-7c | d622080 | **fit_with_fixes** | all 23 rows agree; F1: the commit rewrote 12 EXISTING rows byte-wise (DoD 6 says "only inserted rows") |
| OH8-7d | 429bc9e | **fit_with_fixes** | 37 of 38 rows agree; F2: `red_sandbox.py::_check_row_in_clone` is not `shape` (hash join at least; a symlink guard on a written folder under Lead rule 2) |
| OH8-7e | 3589f5b | **fit** | all 32 rows agree under the Lead's rules; the open points go to the Lead list (K8b), not to a builder |

Overall: **NEEDS WORK (fit_with_fixes)**: 2 required fixes, 0 blockers. Accepting is the Lead's call (rule 6). Both fixes are small enough for one fresh builder round.

## Findings

**F1 (7c, consistency / DoD 6 / AR-20 diff hygiene).** d622080 removes 13 fixture lines: 1 ratchet line and 12 existing
`probe_by_code.py` rows (`_first_check`, `_inverted`, `_longer_title`, `_profile_cwd`, `_repeat_check`, `_statement_span`, `body_span`,
`find_oracle`, `manifest_entry`, `parse_detector_node`, `plan_mutation`, `run_shape_checks`). It re-adds them with the space after the
comma deleted: `"function": "_first_check","class": "shape"`. The new row `_located` has the same defect. That makes 13 lines on
3589f5b (`grep -c '","class"'` = 13: fixture lines 675, 677, 679, 680, 690, 698, 702, 706, 711, 717, 719, 723, 726). JSON-equal, so the
builder's reconcile ("existing rows unchanged: True", which compares parsed rows) is right on meaning. But DoD 6 asks that "`git diff` of the
fixture shows only inserted rows and the ratchet lines", and that is false for 7c. The diff a ratchet reviewer reads is noisier than it
should be, and the file now has two spellings. Fix: restore `", "` on those 13 lines (no ratchet change).

**F2 (7d, row class).** `red_sandbox.py::_check_row_in_clone` was written `shape`. Its raises:
- `red_sandbox.py:469-470`: `cwd.is_symlink()`, so the install folder may not be a link.
- `:476-477`: `digest(path) != pin`, a hash equality. That is `xref` by spec 4.2 step 3 ("a hash equals").
- `:479-481`: `os.path.lexists(cwd / name)` for `must_not_preexist`, whose text says "a link to a shared tree is no fresh install".

The install writes into `cwd` (`_run_install`, `:508`). So 469 and 479 are symlink guards on a WRITTEN path, which is `safety` under Lead
rule 2, and it is the same guard as `import_test_receipt.py::_reject_destination_symlinks` (safety, same pair). `shape` is wrong either way.
The highest reading wins (CLASS_ORDER), which gives `safety`, owner `data`, raise `safety: 72 -> 73`. If the Lead restates rule 2
(K2 (2)), the minimum fix is `xref`, with no ratchet change.

**F3 (7d commit message, not fixable in the commit).** 429bc9e says "38 rows: 9 xref, 21 shape ... 8 safety". The fixture has **8 xref,
22 shape, 8 safety** (my count: the xref rows are `_entries_of_case`, `_observe_stand`, `_profile_for`, `begin`, `find_active_dispatch`,
`rehearsal_probe`, `run_suite::main`, `probe_runtime`). The AR-20 raise lines are right. Only the class tally is wrong. The Lead should
record the correct tally in the `accepted` event or the batch «Ход». Commits are not rewritten.

**F4 (class-wide, census completeness; for the Lead, before OH8-7h).** `refusal_registry.sites()` / `raise_family` do not see a raise
through a FACTORY FUNCTION that returns the family exception (`raise _held_by(...)`). The census's "still unseen" list (fixture `about`,
`BLIND_SPOT`, printed by the totals line) does not name this form. Measured on the 3589f5b copy (`probe_units.py`, trail):
`exploration.py::acquire` is **NOT SEEN**, while the same tool reports `exploration.py::release_lock` as a unit (positive control).
`acquire` is the O_EXCL lock guard (`exploration.py:328-341`), the twin of the `release_lock` safety row, and it has no row at all.

In the 13 files of this pair alone, 15 rowless functions refuse only that way. My AST scan (`factory_raises.py`) lists them:
- probe_by_code.py: `_call_replacement`, `_chain_replacement`, `_target_at_line`, `load_models`, `_judge_walk`, `_judged_record`,
  `_judge_input`, `_demand_critic_dispatch` (the last four are on the critic's judgment path: possibly owner `judgment`);
- execution_request.py: `sandbox_run_directory`;
- exploration.py: `table`, `limit`, `root`, `load`, `acquire`;
- manual_capture.py: `stand_probe`.

This is outside the §3.1 lists, so it is not a defect of these nodes. But OH8-7h is specified to end with "every widened raise site creates
units", and it would close the second road while this third road stays unseen and unnamed. The repo-wide count needs a scout: the
question is which `scripts/*.py` functions refuse only via `raise <module function>(...)`, with no row. The fix belongs in the one
scanner (axis 32: "no second AST walk"). Proposed node, owner the Lead.

## K1 — all 93 rows

Columns: row | written class / roles / owner | my reading | verdict, raise line(s), one clause. "read" = every raise site with 2-5 lines
of context read by me (`raises.py`). "whole" = the function read in full. No row was accepted on the builder's clause alone: all 93 were read
at raise-site level, and 22 in full (the safety rows and the rows answered by the Lead). The roles column of every row is judged in K3; it
is not repeated per row.

### OH8-7c — probe_by_code.py (23)

| row | written | reading | verdict |
|---|---|---|---|
| `_body_of` | shape/[conductor]/data | shape | agree — :5191, :5208 the body holding the check is not found (presence); read |
| `_check_record` | shape (E3) | shape, E3 | agree — :6011-6013 int type guard; callers :6511, :7878 pass a plan check's int line; read |
| `_dispatch_context` | xref | xref | agree — :4746, :4760 the dispatch named resolves among open dispatches; read |
| `_invert_edit` | xref | xref | agree — :5540-5541 the planned line/form equals the record's check; :5530 form; read |
| `_judge_cli` | shape/[qa-code-critic]/data | shape | agree — :7900, :7904 flags present; :7908 story root; role per `judge_record` precedent and agents/qa-code-critic.md:68; whole |
| `_located` | xref | xref | agree — :5142 the statement sha equals what `checks_of` listed; :5101 UTF-8, :5125 parse; read |
| `_model_edit` | xref | xref | agree — :5335-5338, :5362 the call/AST outside the value equals the original (structural equality, not meaning); :5296 form; read |
| `_model_region` | shape | shape | agree — :5277 re-raises `_region_of` with doors; read |
| `_plan_cli` | shape | shape | agree — :8232 story root, :8238 entry names a case (presence); read |
| `_probe` | shape | shape | agree — :4812 manifest entry names no case; read |
| `_probe_alternative` | xref | xref | agree — :5793 model's check key in the Then's keys; :5771 gap AND values; :5785 instance join; read |
| `_probe_plan` | xref | xref | agree — :7473 `product` entry does not hold; :7467 entries owed; read |
| `_region_of` | shape | shape | agree — :5222-5244 argument number/form of the call; read |
| `_require_cover` | xref | xref | agree — :4790 instance id among the case's instance aliases; read |
| `_row_selection` | xref | xref | agree — :7197 `--oracle` selects no check of the plan, :7185 line holds no check (selection joined to the test's checks); read |
| `_selected_keys` | xref | xref | agree — :7216, :7221 selection spans joined to plan keys; read |
| `_test_path` | shape | shape | agree — :4436 file present under the root; read |
| `begin_copy` | safety/data | safety | agree — :3819-3829 no mutation without a written and verified byte copy of the author's test; whole |
| `claim_key` | safety/data | safety | agree — :3756 a running probe holds the lock; :3778 an unsettled copy; whole |
| `main` | shape | shape | agree — :8341 story root resolves (presence of the folder); read |
| `parse_alternative_token` | shape | shape | agree — :4840 `<case>:ALT-<n>` form; read |
| `plan_model` | xref | xref | agree — :5460 entry's check is a key of the plan; :5453, :5463, :5466 form; read |
| `release_copy` | safety/data | safety | agree — :3865-3869 a copy is not released while its probe holds the lock; whole |


### OH8-7d (38)

| row | written | reading | verdict |
|---|---|---|---|
| environment_preparation.py::`_claim_locked` | safety/data | safety | agree — :285 environment not provably unowned; :306 O_EXCL claim conflict; :278 digest xref; read |
| ::`_facts` | shape | shape | agree — :46, :59 required facts present; read |
| ::`_observation` | shape | shape | agree — :67, :70 presence; read |
| ::`_runtime_identity` | shape | shape | agree — :76 source_revision present; read |
| ::`_verified_absence` | safety/data | safety | agree — :84-87 a `create` never lands on an existing runtime (environment-bound absence evidence); whole |
| ::`observe` | shape | shape | agree — :317 job file present (same as execution_request `recover`); read |
| ::`plan_environment` | shape | shape | agree — :122, :131 objects/ids present; read |
| ::`read` | shape | shape | agree — :216 corrupt JSON; read |
| ::`reconcile_environment` | safety/data | safety | agree — :506-507 no reconciliation while coordinator/child live; :503, :510 shape; read |
| ::`transition` | shape (E3) | shape, E3 | agree — :252-253; all 18 callers pass a literal or the two-literal choice at :488-489; read |
| execution_request.py::`_command_from_profile` | shape | shape | agree — :1828, :1839 command present/well formed; read |
| ::`_entries_of_case` | xref | xref | agree — :1193, :1208, :1223 the case's area joined to manifest rows; read |
| ::`_observe_precedent` | shape | shape | agree — :2826 the stand cannot be looked at; read |
| ::`_observe_stand` | xref | xref | agree — :2860 registered probe; :2876 `reference_target_problem` (data join, :2512-2534); read |
| ::`_place_rows` | shape | shape | agree — :2678-2679 file present; read |
| ::`_profile_for` | xref | xref | agree — :1720, :1730, :1774, :1799 profile resolves for the files; read |
| ::`begin` | xref | xref | agree — :418-419, :439-440 idempotency key vs request digest; :438 shape; no ownership guard (contrast `_claim_locked`); read |
| ::`build_mine_request` | safety/data | safety | agree — :3458 a red probe never runs in the author's tree; :3603 file must be in the clone; the rest shape/xref; read (690-line function, raise sites only) |
| ::`find_active_dispatch` | xref | xref | agree — :915, :927 dispatch resolves; read |
| ::`probe_record` | shape | shape | agree — :108 exit code, :112 JSON; read |
| ::`read` | shape | shape | agree — :405; read |
| ::`recover` | shape | shape | agree — :456 job present; read |
| ::`rehearsal_probe` | xref | xref | agree — :2466-2468 provenance accepted; read |
| ::`s6_close_from_state` | safety/data | safety (borderline) | agree — :979 a dispatch open on the story (a second writer on the author's test) wins over the state joins :987, :993, :1007, :1014 (xref); read |
| execution_scheduler.py::`_resources` | shape | shape | agree — :175, :181; read |
| ::`_with_native_workers` | shape | shape | agree — :224 conflicting flag in argv; read |
| ::`_workers` | shape | shape | agree — :204, :208; read |
| ::`prepare_schedule` | shape | shape | agree — :270, :276 uniqueness (shape per spec 1.2), :281, :285; read |
| managed_dependency.py::`install` | safety/intent | safety/intent | agree — :95-98 authorization receipt bound to the descriptor (a person's word); precedent `validate_descriptor`; whole |
| red_sandbox.py::`_check_row_in_clone` | shape | **safety** (min. xref) | **differ** — :469 and :479 symlink/link guards on the folder the install writes; :476 pin hash equality (F2); read |
| ::`_clone_guard` | safety/data | safety | agree — :453, :457, :461 marked clone disjoint from the author's tree, targets unmutated; whole |
| ::`_plan_row` | shape | shape (Lead question) | agree under existing practice — :391 kind, :394-397 no field beyond the kind (the command comes from data, never the request), :399-401 cwd relative with no `..`; under rule 2 (written folder) and the command-injection reading it is a safety candidate → K8b; read |
| ::`_run_install` | shape | shape | agree — :511, :513, :517 a run outcome (timeout/exit), not a guard; read |
| ::`install_budget_s` | shape | shape | agree — :372-373; read |
| ::`plan_setup` | shape | shape | agree — :423, :431, :436 form/duplicate/budget; read |
| run_suite.py::`main` | xref | xref | agree — :2836-2838 runtime probe vs request moved; read |
| ::`probe_runtime` | xref | xref | agree — :927-929 provenance accepted; read |
| ::`reparse_run_block` | safety/data | safety | agree — :749-751 immutable raw reporter bytes (sha); :817-818 exclusive write collision; :737 read containment is shape and loses to safety; read |

### OH8-7e (32)

| row | written | reading | verdict |
|---|---|---|---|
| exploration.py::`_clean_stories` | shape | shape | agree — :537-538 one word, one path component; the key is stored and queried, not written as a path in this file; read |
| ::`_config` | shape | shape | agree — :383, :385 config present/readable; read |
| ::`_hit_repos` | shape | shape (Lead question) | agree under the `hooklib.artifacts_dir` precedent (`is_one_component`, shape) — :727, :732, :735; under rule 2 it is a safety candidate: the repo name enters the role's written output path (:818, `writes` `work/feature-map.{repo}.yaml`) → K8b; read |
| ::`_need_session` | shape | shape | agree — :290-291; read |
| ::`brief` | xref | xref | agree — :810-811 repo among hit repos; :801-809 step/table; read |
| ::`frame` | xref | xref | agree — :556-560 presence/length of the phrase; :571-574 continuation scope set equality; no content read; read |
| ::`narrow` | shape | shape | agree — :672-678 presence of the person's words and flags; read |
| ::`place` | shape | shape | agree — :265, :271; read |
| ::`record_answer` | xref/data | xref (Lead question on safety/intent) | agree on not-word-list — :625-649 exact equality of `_normal_word` (casefold/whitespace/punctuation only, :611-612) with `OFFERED` tokens of `FRAME_OPTIONS`; free words go to the conductor (:659-661); :635, :638, :647 guard the person's recorded word against the conductor's token → K8b; whole |
| ::`release_lock` | safety/data | safety | agree — :363-367 only the holder session or a person's word releases; whole |
| ::`set_step` | xref | xref | agree — :706, :711, :714 status/step/frame-answer state joins; read |
| explore_step.py::`_session` | shape | shape | agree — :95 session identity present; read |
| import_test_receipt.py::`_copy_evidence` | safety/data | safety | agree — :163-170 symlinked destination dir, modified source, immutable collision; :183 change during copy; whole |
| ::`_reject_destination_symlinks` | safety/data | safety | agree — :194, :199 written destination escape/symlink; whole |
| ::`_safe_local` | shape | shape | agree — :150-158 containment of a READ source (`import_receipt` :284); whole |
| ::`_time` | shape | shape | agree — :81, :83 ISO-8601 with tz; whole |
| ::`_trusted_producer` | xref/data | xref | agree by the raising condition — :59-73 config readable, exactly one profile (:65), opt-in flag (:69), complete identity (:73); the trust comparison itself is `validate_receipt` :96 (existing row) → K2 (4); whole |
| ::`_write_exclusive` | safety/data | safety | agree — :141-144 an existing import file is never overwritten; whole |
| ::`import_receipt` | safety/data | safety | agree — :276-277 immutable receipt collision; :280, :302 xref; whole |
| manual_capture.py::`_read_pair` | shape | shape | agree — :653, :658, :662 file/keys present (requires secrets, guards none); read |
| ::`read_login` | shape | shape | agree — :687, :693, :703; read |
| manual_evidence.py::`_case_thens` | shape | shape | agree — :1117-1118 case file readable; read |
| ::`_request_tail` | xref | xref | agree — :1073-1078 one policy/condition across the selected obligations; read |
| ::`prepare_request` | xref | xref | agree — :986, :1001, :1011, :1018, :1023, :1030-1041 gate-A decision, pins, expectation gaps, obligation joins; read |
| s7_reorder.py::`_entry` | xref | xref | agree — :144-146 instance id resolves in the manifest; read |
| ::`_read_test` | shape | shape | agree — :168-173 READ containment plus UTF-8; whole |
| ::`_triage` | shape | shape | agree — :112-113; read |
| ::`find_row` | xref | xref | agree — :123, :127, :130, :133; read |
| ::`finish` | xref | xref | agree — :290-334 snapshot state, line-multiset diff (`variant_shape.py:114-146`, Counter/SequenceMatcher: form, not meaning) and run status/sha joins; read |
| ::`locate` | shape | shape | agree — :159-160 selector form; read |
| ::`main` | xref | xref | agree — :425-426 row carried by this script (state join); read |
| ::`repo_of` | shape | shape | agree — :88-89 project marker present; read |

Tally: 93 rows; 91 agree, 1 differs (F2), 1 is a Lead question whose current value stands (`_plan_row`). `_hit_repos` and
`record_answer` agree today and depend on the Lead restatements in K8b.

## K2 — the six Lead rules

1. **Copy/lock/claim guard = safety, owner data — holds.** Every row it names refuses a second writer or an overwrite at its raise line:
   claim_key :3756, begin_copy :3827, release_copy :3866, `_claim_locked` :285/:306, `_verified_absence` :86, `reconcile_environment` :507,
   `build_mine_request` :3458, `s6_close_from_state` :979, `reparse_run_block` :751/:818, `_clone_guard` :453-461, `release_lock` :366,
   `_copy_evidence` :170, `_write_exclusive` :144, `import_receipt` :277. Restatement proposed: "judged by the RAISING CONDITION, not by
   what the function protects". `execution_request.begin` (O_EXCL claim, but it refuses only on a digest mismatch, so it is xref) and
   `_check_record` (it protects the standing record, but by a type guard, so shape/E3) are classified correctly only under that reading.
   Rows moved: none.
2. **Containment/symlink: written = safety, read = shape — wrong as stated (its precedent list is wrong).** `red_sandbox.inside`, cited as
   a READ precedent, guards WRITES: `red_sandbox.py:615` (copy target), `:617`, and `:625` (`inside(destination, ...).write_text(...)`).
   `manual_evidence._copy_atomic` (existing, shape) is the line-for-line twin of `_copy_evidence` (new, safety): a symlinked parent, a hash,
   an exclusive temp, an immutable collision. `hooklib.artifacts_dir` and `artifact_packet.work_path` (existing, shape) guard written
   paths too. Rows it moves inside the diff: `red_sandbox._check_row_in_clone` → safety (F2); `_plan_row` and `_hit_repos` become
   safety candidates. Outside the diff, if the rule stands: `red_sandbox.inside`, `manual_evidence._copy_atomic`, `hooklib.artifacts_dir`,
   `artifact_packet.work_path` (and a scout pass over the other `is_relative_to` / `is_symlink` callers; the list is in the trail). The
   Lead picks ONE road (P31): keep rule 2 and open a node that raises the existing rows (named safety raise), or restate it ("a path
   guard is shape unless it refuses a write through a link/escape") and re-judge `_reject_destination_symlinks` / `_copy_evidence` by it.
3. **`record_answer` = xref, not word-list — holds.** The comparison is exact equality of `_normal_word` (casefold, whitespace,
   punctuation; `exploration.py:611-612`) with `OFFERED`, the tokens of the closed question the code itself rendered (`FRAME_OPTIONS`,
   :42-49, `closed_question` :516). P22 sanctions code reading closed answers, and free words go to the conductor (:659-661). FR-12 is
   not broken. The rule does not consider the census's own `safety` clause ("a guard on ... a person's words"): :635, :638 and :647-649
   refuse to let a conductor token or `--not-asked` override the person's recorded word. That is a Lead question (K8b), not a builder fix.
4. **`_trusted_producer` = xref, owner data — holds on the class, wrong on the reason.** Its raises are config presence (:59, :61), a
   one-profile join (:65), an opt-in flag (:69) and identity completeness (:73), which is xref. The reason given, "owner data, unlike
   install's intent", is the wrong axis: the owner never decides the class. Spec 4.2 step 3 lists "trust of a producer" as a safety example,
   and the actual trust COMPARISON is `validate_receipt` :96 (`producer.get(k) != trusted.get(k)`), an EXISTING row written `shape`. That
   existing row is the one to re-judge (xref at least, safety candidate). It is queued, because changing it is outside these nodes.
5. **Roles `[conductor]` by file precedent — the precedent is wrong; answered in K3.**
6. **`begin` xref; `frame`/`narrow` presence/length only — holds.** `begin` :418-440 is a digest join. `frame` :556-574 checks emptiness,
   length, path budget and continuation set equality. `narrow` :672-678 checks presence of words and flags. Neither reads content.

## K3 — roles of the CLIs a role runs

The census definition is "the roles on whose path it stands" (test docstring :6). `blocking_per_role` counts exactly that. The evidence of
who calls each command (package at 3589f5b):
- `probe_by_code.py`: qa-code-critic (agents/qa-code-critic.md:68, :70; skills/qa-story/phases/s5.md:122, :160, :200); conductor for
  `--s6-close` (s6.md:85). `--release-copy`: the author (s5.md:209). Existing precedent: `judge_record` = [qa-code-critic].
- `red_sandbox.py`: qa-code-critic `--probe` (qa-code-critic.md:68, s5.md:124, :211); qa-failure-analyst `--diagnostic`
  (references/role-commands.json `red_sandbox.py --diagnostic` roles [qa-failure-analyst]; qa-failure-analyst.md:73).
- `run_suite.py`: qa-runner (qa-runner.md:62), qa-automator `--mine` (qa-automator.md:68), qa-code-critic `--detail`
  (qa-code-critic.md:69), qa-failure-analyst `--request` (qa-failure-analyst.md:73).
- `execution_request.py` `--mine` path (`build_mine_request`, `_entries_of_case`, `_profile_for`, `_command_from_profile`, `_place_rows`,
  `_observe_stand`, `_observe_precedent`, `find_active_dispatch`): qa-automator through `run_suite --mine`, and qa-code-critic through
  the red probe.
- `manual_capture.py`: role-commands.json `manual_capture.py ui|http` [qa-runner, qa-failure-analyst], `app` [qa-runner].
- `manual_evidence.py prepare` (`prepare_request`, `_request_tail`, `_case_thens`): role-commands.json [qa-runner]. Existing precedent in
  the same file: `_result_errors` = [qa-runner].
- `import_test_receipt.py`: qa-automator (qa-automator.md:68; s5.md:143).
- `s7_reorder.py`: the conductor's phase card s7.md:149-166, so [conductor] is right. `exploration.py` and `explore_step.py`: conductor
  plus step tools (references/exploration.json); [conductor] can stand.

Answer: the file precedent `[conductor]` is wrong for role-run CLIs. It under-counts `blocking_per_role` for qa-code-critic,
qa-automator, qa-runner and qa-failure-analyst, which is the unsafe direction for a shrink-only ratchet. It is NOT a defect of these
three nodes. Spec 4.2 step 4 (iii) told the builders to follow same-file rows, and the existing rows of the same files carry the same
`[conductor]`: about 20 `manual_capture.py` rows, `red_sandbox.py`, `run_suite.py`, `manual_evidence.py` except `_result_errors`, and
the 23 `probe_by_code.py` rows of 7b. Re-rolling only the 93 new rows would split files into two conventions (P31). So it is a proposed
class node (owner the Lead): re-derive roles of whole role-run files from references/role-commands.json, `agents/*.md` and the phase cards,
old and new rows together, with named `blocking_per_role` raises. Spec 4.2 step 4 gains a step before (iii): "the role a command
is declared for (role-commands.json / the role's tools line)". Rows of this pair it would move: all 23 of 7c except `_judge_cli`
(→ qa-code-critic + conductor), the 8 `--mine`-path rows of execution_request, run_suite 3, red_sandbox 6, manual_capture 2,
manual_evidence 3, import_test_receipt 7.

## K4 — words or content of a role or a person (E9)

None found. Walked: every row whose raise touches a person's or a role's text or output:
- `record_answer`: exact closed-token equality (K2 (3)).
- `frame` / `narrow`: presence and length only.
- `release_lock`: whether a person's word is present.
- `prepare_request`: presence of gate-A answers, `expectation_gaps`.
- `_request_tail`: equality of policy values.
- `s7_reorder.finish`: a line-multiset diff of the role's edit plus a run status. `variant_shape.py:114-146` uses Counter and
  SequenceMatcher on lines, with no regex on meaning.
- `probe_by_code._model_edit`: AST/argument equality outside the value.
- `_probe_alternative` / `_probe_plan`: key joins.

None compares wording to a phrase list or judges quality by pattern.

## K5 — AR-20 and "no existing row changed"

Reconciliation, recomputed by my script `cmp.py` from the four fixture versions:

| node | new rows | removed / changed rows (parsed) | ratchet delta | rows naming it |
|---|---|---|---|---|
| 7c | 23 | 0 / 0 | conductor 514→536 (+22), qa-code-critic 134→135 (+1), safety 56→59 (+3) | 22 / 1 / 3 |
| 7d | 38 | 0 / 0 | conductor 536→574 (+38), safety 59→67 (+8) | 38 / 8 |
| 7e | 32 | 0 / 0 | conductor 574→606 (+32), safety 67→72 (+5) | 32 / 5 |

Every raise named in a commit message equals the rows naming it, and no other ratchet key moved. Removed lines in
`git diff e9a3822 3589f5b`: **36**.
- Fixture: 15 (13 in 7c, 1 in 7d, 1 in 7e). That is 3 ratchet lines plus the **12 byte-rewritten existing rows of 7c (F1)**.
- Test file: 21. 7c's 23 `probe_by_code.py::f` entries collapsed to one entry. The ceiling went 167→144→106→74. 7c also rewrote the
  `listed_*` table rows, the `C7_NEUTRAL` line and one assert line: that is the t-377 F1/F2 fix that 7c's message declares ("also: critic
  t-377 F1/F2").

So "only additions besides the ratchet lines" holds for 7d and 7e, and fails for 7c on bytes, not on meaning. F3: 7d's class tally is
wrong in the message.

## K6 — §3.1 lists vs rows

Script `k6.py` (spec §3.1 blocks vs the new rows per commit): 7c 23/23, 7d 38/38, 7e 32/32. No row exists for an unlisted function, and
every listed function has a row. The two E3 rows (`_check_record`, `transition`) carry the `E3:` note and the finding path. Their callers
were verified (K1). Beyond the lists: F4 (15 functions invisible to the scanner in these 13 files).

## K7 — class-wide

Pairs of the same guard shape classified differently:
- (a) `import_test_receipt._copy_evidence` (safety, new) vs `manual_evidence._copy_atomic` (shape, existing): the same code.
- (b) `import_test_receipt._reject_destination_symlinks` (safety, new) vs `red_sandbox.inside` (shape, existing; guards writes :615,
  :617, :625).
- (c) `red_sandbox._check_row_in_clone` (shape, new) vs (b) in the same pair: F2.
- (d) `is_one_component` guards: `exploration._hit_repos` / `_clean_stories` (shape, new) and `hooklib.artifacts_dir` (shape) vs
  `waiver.run_carry` (safety).
- (e) `exploration.release_lock` (safety) vs `exploration.acquire` (no row: scanner blind spot, F4).
- (f) `import_test_receipt._trusted_producer` (xref) vs `validate_receipt` :96 (shape, existing), where the trust comparison really lives.

Pairs checked and consistent:
- `_claim_locked` (safety) vs `execution_request.begin` (xref): justified, since only the first refuses on ownership.
- `environment_preparation.read` / `execution_request.read` (shape).
- `observe` / `recover` (shape).
- `probe_runtime` / `rehearsal_probe` (xref).

Builders' analogs (verified):
- `import_test_receipt.py::main` (:307-318) has no guard. An `ImportError` (the module's own `class ImportError(ValueError)`, :26)
  from `import_receipt` surfaces as a traceback with exit 1. The command is run by qa-automator, a ROLE (qa-automator.md:68). That
  breaks P3/FR-1 and the references/role-commands.json note ("a refusal is an instruction, never a traceback"). This is a finding for a
  queue, with a priority above the next one. Side note: the module class shadows the builtin `ImportError` (:26), which is
  queue-worthy code quality.
- `environment_preparation.py::main` (:555-600) runs `plan_environment`, `execute_environment`, `observe` and `reconcile_environment`
  outside any try, so PreparationError gives a traceback with exit 1. The caller is `story_run` code (:566-570), not a role. This is
  FR-46 (exit class), a queue item.
- 7d's "`_entries_of_case` strict on `--mine`, advisory via `fresh_evidence`" and 7e's "`_safe_local` advisory on the reader path" are
  real (one function, two roles). The census classifies the raising condition, so no row moves. A note for the Lead, no node.

## Standing questions (critic brief items 6, 7, 10, 11, 12)

- **DUPLICATION AND CONSISTENCY:** the diff adds no code. Consistency defect: F1 (13 lines with `","class"`). Class inconsistencies:
  K7 (a)-(f). Package-level duplication noticed (pre-existing, outside the diff): `import_test_receipt._copy_evidence` ≈
  `manual_evidence._copy_atomic`, a queue item. Grepped/compared: `is_one_component`, `is_symlink`, `is_relative_to` callers vs their
  census classes (`callers.py`).
- **CODE QUALITY:** none found in the diff (one tuple, one constant). Noticed outside: the shadowed builtin `ImportError` (import_test_receipt.py:26).
- **ARCHITECTURE (10):** AR-29, AR-20, AR-13, AR-22 and AR-28 are named in all three messages. AR-20 was reconciled by me (K5). AR-13:
  `refusal_registry.py` is not in the diff (`git diff --stat`: 2 files). F4 is an AR-28/AR-13 gap of the one scanner (not of this diff).
- **JUDGMENT (11):** no class lowered, no `blocks_override` added, no scan constant edited (MEANING_CEILING 24 unchanged; the diff
  touches only `SUBCLASS_PENDING_CEILING` and `SUBCLASS_UNIT_FILES`). `judgment: adds data check ...` is legitimate. No row reads meaning (K4).
- **ONE ROAD (12):** rule 2 as practised gives two roads for one guard shape: new written-path guards are safety, old ones are shape
  (K2 (2), K7 (a)(b)). The role precedent gives a second convention for roles (K3). Both leave this verdict as proposed nodes for the
  Lead (K8b), not as builder fixes.

## K8 — fix lists

### K8a — for a fresh builder (one round, same worktree tip after 7f lands, or its own branch; owns: the fixture only)

1. `scripts/tests/fixtures/judgment-census.json`: on the 13 `probe_by_code.py` lines carrying `","class"` (`_first_check`,
   `_inverted`, `_located`, `_longer_title`, `_profile_cwd`, `_repeat_check`, `_statement_span`, `body_span`, `find_oracle`,
   `manifest_entry`, `parse_detector_node`, `plan_mutation`, `run_shape_checks`), change `","class"` to `", "class"`. Why: F1. JSON
   unchanged, no ratchet change. Witness: `grep -c '","class"'` returns 0, and the census test is green.
2. `red_sandbox.py::_check_row_in_clone`: change `shape` to `safety` (roles [conductor], owner data, unchanged), and raise
   `ratchet.safety` 72 to 73. The commit message raise line: `safety: 72 -> 73 -- census re-judges red_sandbox.py::_check_row_in_clone
   (symlink/link guard on the install folder, t-411 F2)`. Why: F2. If the Lead's K8b restatement of rule 2 makes path guards shape, the
   fix is instead `shape` to `xref` with no ratchet change (pin hash join :476).

### K8b — for the Lead (decisions and nodes; none is a builder's to take)

1. Rule 2: pick one road. Either keep it and open a node raising the existing written-path guards (`red_sandbox.inside`,
   `manual_evidence._copy_atomic`, `hooklib.artifacts_dir`, `artifact_packet.work_path`, plus a scout over the other `is_symlink` /
   `is_relative_to` callers), or restate it and re-judge `_copy_evidence` / `_reject_destination_symlinks` / `_check_row_in_clone`.
   Correct the precedent list either way: `red_sandbox.inside` guards writes. Decide `red_sandbox._plan_row` (the command comes only
   from data, :394-397, plus the cwd form) and `exploration._hit_repos` (repo name in a written output path, :818) under the chosen road.
2. Rule 1: restate it as "by the raising condition (a refusal of a second writer / an overwrite)".
3. `exploration.record_answer`: decide the census safety clause (a guard on a person's words, :635/:638/:647). The proposal is
   safety/intent (precedents `person_words.door`, `waiver.*`). If xref stays, owner `intent` per precedent `exit_gate.judge_words`
   (xref/intent). One Lead line either way.
4. Rule 4: restate the reason (owner is not the class axis). Queue the re-judgment of the EXISTING row
   `import_test_receipt.validate_receipt` (the trust comparison :96, written shape).
5. Roles (K3): open a class node "roles of role-run CLIs from role-commands.json / agents/*.md / phase cards", covering old and new rows of
   probe_by_code, execution_request (--mine path), run_suite, red_sandbox, manual_capture, manual_evidence (prepare) and
   import_test_receipt, with named `blocking_per_role` raises. Amend spec 4.2 step 4 for nodes f..h, or let f..h keep the file
   precedent and fold their rows into the same node. The Lead decides which; the remaining nodes need the answer before dispatch.
6. F4: open a node BEFORE OH8-7h for the scanner blind spot "raise through a factory function" (`raise _held_by(...)`). Concretely: a
   scout counts the rowless functions repo-wide (15 in these 13 files alone, including `exploration.acquire` and four
   `probe_by_code._judge_*` / `_demand_critic_dispatch` on the critic's judgment path); refusal_registry learns the form, or the census
   `about`/`BLIND_SPOT` names it. OH8-7h's end-state text must not claim completeness without it.
7. F3: record 7d's true tally (8 xref, 22 shape, 8 safety) in the `accepted` event or the batch «Ход».
8. Queue items (findings files, D-0044): `import_test_receipt.py::main` traceback to a role (P3/FR-1; higher priority);
   `environment_preparation.py::main` traceback to story_run (FR-46); the shadowed builtin `ImportError` (import_test_receipt.py:26);
   the `_copy_evidence` / `_copy_atomic` duplication.

## Trail

Read:
- Spec `docs/tasks/specs/t-346-oh8-7b-chain-spec.md`: §1 (13-57), §2.2 (134-152), §3.1-3.3 (156-342), §4 (405-465), §6a-§10 (591-680).
- `docs/tasks/critic-diff-brief.md` items 6, 7, 9-12.
- `docs/SIBLING_MAP.md` axes 18, 32, 34 (headings; the axis-32 table).
- `tools/critic_verdict.schema.json`.
- The three commit messages (`git log -3 --format=%B 3589f5b`).
- `git diff e9a3822 3589f5b` (both files, whole).
- The fixture at e9a3822, d622080, 429bc9e and 3589f5b (`git show`, parsed).
- `test_judgment_census.py` :1-60, plus a grep of roles/C2/C3.
- All 93 functions at 3589f5b (raise sites with context; 22 in full, see K1).
- Context functions: `exploration.acquire`, `_normal_word`, `OFFERED` / `FRAME_OPTIONS`; `variant_shape.variant_shape`;
  `red_sandbox.inside` and its callers; `manual_evidence._safe_evidence_path` and `_copy_atomic`; `artifact_packet.work_path`;
  `execution_request.reference_target_problem`; `import_test_receipt.main`; `environment_preparation.main`; `transition` callers;
  `_check_record` callers.
- `references/role-commands.json` (commands and roles).
- `agents/qa-code-critic.md` :66-72, `qa-runner.md` :60-64, `qa-failure-analyst.md` :72-74, `qa-automator.md` :68.
- `skills/qa-story/phases/s5.md`, `s6.md`, `s7.md` (grep hits).
- `references/exploration.json` (around `explore_step`).

Scratchpad scripts (pure reads; all under
`C:\Users\i_mas\AppData\Local\Temp\claude\b3e3188b390a00d9\acb1ecf0-04a8-42f3-8bdd-f14a2dae87bf\scratchpad\`):
- `cmp.py` (per-commit new/removed/changed rows, ratchet deltas, roles/class counts).
- `k6.py` (§3.1 lists vs rows).
- `fn.py` / `raises.py` (function/raise extraction).
- `callers.py` (census classes of the callers of a guard).
- `probe_units.py` (units_of on the copy).
- `factory_raises.py` (rowless factory-function refusers).

Control re-run (allowed form, byte copy at 3589f5b outside the tree): `python -B <copy>/scripts/tests/test_judgment_census.py`
gave `=== judgment_census: 26/26 ok ===`. The totals line: `1067 units; shape=777 xref=186 ... safety=72; ... conductor=606 ...
qa-code-critic=135 ...; subclass_family=55 subclass_pending=74 (ceiling 74)`. This matches the Lead's `26 passed`, `pending total:
106 -> 74` and the reconcile numbers. `probe_units.py` gave `exploration.py::acquire NOT SEEN`, `exploration.py::release_lock unit`
(positive control) and `pending total 74`.

Needed beyond the manifest: `references/role-commands.json`, `agents/*.md`, `skills/qa-story/phases/s5-s7.md`, `variant_shape.py`,
`hooklib.py` (`is_one_component`), `artifact_packet.py`, `refusal_registry` (through the test), `docs/SIBLING_MAP.md`. All were reads.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "fixes": [
    "F1 (OH8-7c): restore the space in the 13 probe_by_code.py fixture lines spelled with a comma directly before the class key (12 existing rows rewritten byte-wise by d622080 plus the new _located row); JSON and ratchet unchanged",
    "F2 (OH8-7d): red_sandbox.py::_check_row_in_clone shape -> safety (symlink/link guards on the install folder :469, :479; pin hash :476), raise ratchet.safety 72 -> 73 named in the message; if the Lead restates rule 2, shape -> xref with no ratchet change"
  ],
  "class_completeness": "Rows: 93/93 match spec 3.1 (k6.py), ratchet raises equal rows per node (cmp.py), no existing row changed in meaning. Class gaps for the Lead, not for these nodes: (1) Lead rule 2 cites red_sandbox.inside as a read precedent but it guards writes; manual_evidence._copy_atomic (shape) twins import_test_receipt._copy_evidence (safety): one road to pick, then a raise node for existing rows or a restatement; (2) roles of role-run CLIs are under-counted by the [conductor] file precedent across old and new rows (role-commands.json, agents/*.md): class node; (3) scanner blind spot, a raise through a factory function (raise _held_by(...)), unnamed in the census about/BLIND_SPOT: exploration.acquire not seen (release_lock seen as control), 15 rowless refusers in these 13 files; node before OH8-7h, scout for the repo-wide count; (4) validate_receipt :96 (existing, shape) holds the producer-trust comparison; (5) queue: import_test_receipt main traceback to a role, environment_preparation main traceback, shadowed builtin ImportError, copy-helper duplication.",
  "trail": {
    "read": [
      "C:/QAFactory/forge-repo/docs/tasks/specs/t-346-oh8-7b-chain-spec.md (1, 2.2, 3.1-3.3, 4, 6a-10)",
      "C:/QAFactory/forge-repo/docs/tasks/critic-diff-brief.md (items 6, 7, 9-12)",
      "C:/QAFactory/forge-repo/docs/SIBLING_MAP.md (axes 18, 32, 34)",
      "C:/QAFactory/forge-repo/tools/critic_verdict.schema.json",
      "git -C worktrees/oh8-7b log -3 --format=%B 3589f5b; git diff e9a3822 3589f5b (fixture and test, whole)",
      "fixture judgment-census.json at e9a3822, d622080, 429bc9e, 3589f5b (parsed)",
      "scripts at 3589f5b: probe_by_code.py, execution_request.py, environment_preparation.py, execution_scheduler.py, managed_dependency.py, run_suite.py, red_sandbox.py, exploration.py, explore_step.py, manual_evidence.py, manual_capture.py, import_test_receipt.py, s7_reorder.py (all 93 functions at raise sites, 22 whole), variant_shape.py, artifact_packet.py, hooklib.py is_one_component",
      "references/role-commands.json; agents/qa-code-critic.md, qa-runner.md, qa-failure-analyst.md, qa-automator.md; skills/qa-story/phases/s5.md, s6.md, s7.md; references/exploration.json",
      "scripts/tests/test_judgment_census.py (docstring, roles, C2/C3)"
    ],
    "reruns": [
      {"command": "python -B <scratchpad>/pkg/ai-packages/qa-factory/scripts/tests/test_judgment_census.py (byte copy of 3589f5b via git archive)", "result": "26/26 ok; totals 1067 units, safety=72, conductor=606, qa-code-critic=135, subclass_pending=74 (ceiling 74)"},
      {"command": "python -I <scratchpad>/cmp.py (parsed fixtures per commit)", "result": "7c +23 rows, conductor +22, qa-code-critic +1, safety +3; 7d +38, conductor +38, safety +8 (8 xref, 22 shape); 7e +32, conductor +32, safety +5; 0 rows removed or changed"},
      {"command": "python -I <scratchpad>/k6.py (spec 3.1 lists vs new rows)", "result": "23/23, 38/38, 32/32; none unlisted, none missing"},
      {"command": "git diff e9a3822 3589f5b | grep -c removed-line pattern", "result": "36 removed lines: fixture 15 (3 ratchet + 12 byte-rewritten probe_by_code rows in 7c), test 21"},
      {"command": "python -B -I <scratchpad>/probe_units.py <copy> exploration.py::acquire exploration.py::release_lock", "result": "acquire NOT SEEN; release_lock unit (positive control); pending total 74"},
      {"command": "python -I <scratchpad>/factory_raises.py <copy> census-3589f5b.json <13 files>", "result": "15 rowless functions refusing only via raise of a factory-function call"}
    ]
  }
}
```
