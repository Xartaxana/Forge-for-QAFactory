# t-121 B1: the words of gate A's test-repository question (data, reader, hint, forms, change set, shown-doors store)

Worktree `agent-a365d2def0628cb25`, nothing committed (dispatch: "commit nothing"). Changed: `references/question-vocabulary.json`,
`scripts/gate_brief.py`, `scripts/gate_preflight.py`, `scripts/external_writes.py`, `tests/test_gate_vocabulary.py`,
`tests/test_gate_question_form.py`. Deferred as ordered (t-119): `factory_origin`, the factory-writes record, the "only factory
entries" branch and info row, the factory clause in the message: `vcs_changes` returns `person` = every entry outside the factory home
and `factory` = `[]`.

## Behaviour items 1-8 of node B1

1. DONE. Vocabulary: rows `product_gap` (+ `executor`), `vcs_commit` / `vcs_stash` (`writes_repository: true`, executors `git_commit` /
   `git_stash`), `vcs_go_on` (`record`), `says` as the spec text, three price lines each. `gate_brief.FINDING_DOOR_OPTIONS`,
   `FINDING_DOOR_EXECUTORS`, `finding_door_words` (executor / writes_repository / price lines; a row with a bad option, executor or no
   word is dropped).
2. DONE. `finding_door_option`: a `writes_repository` row is read only as the word or a synonym alone, else `("", "")`.
3. DONE. `external_writes.closed_by_run(task_root, unreadable_closes=False)`; True returns "the run's record cannot be read, so nothing
   is written into your repository" for an unreadable or non-object pipeline; default byte-identical (its 6 other callers untouched).
4. DONE (minus `factory_origin`). `factory_home_place` -> `(rel, why)`, `_factory_home_in_repo` delegates, `_in_home` (rule extracted from
   `outside_factory_home`, same result), `vcs_state_block`, `vcs_changes`, `vcs_blockers`, `REPO_WORD_PATH_CAP = 20`.
5. DONE (minus the factory clause / info row). `check_vcs` on `vcs_changes` (one `-z -uall` read, no second status read). Doors in order
   accept (HEAD block, byte-equal to today), go on (HEAD block, `vcs_go_on`), commit / stash (block `test repository changes: <head12>
   <digest12>`), each writing word only with: `closed_by_run(..., unreadable_closes=True)` falsy, `len(person) <= 20`, no blocker for it.
   `fix` one line; `answers` per `finding_door_hint`; `Rehearsal.add(answers=)` replaces `DOOR_ID` in it.
6. DONE. `render`: multi-line `fix` / `answers` continue at 10 spaces, a one-line fix byte-identical. `brief_lines`: a row with `answers`
   prints them in full under it, never cut by `limit` (limit counts the other rows; "+N more" counts them too).
7. DONE. `gate_brief.render` cap grows by the answers lines of the rehearsal's rows.
8. DONE. `_finding_forms`: one `<item id>: <word>` form per word of `finding_door_words` that a line item's door carries (also `product
   gap`, F16 (a)); reader `Driver.read_finding_doors`. `keep_shown_doors` / `shown_doors_of` per §3.3; `main` (skill path) calls the
   writer after `keep_shown_attachments`, one stderr line on failure.

## Edges (non-deferred rows of the table + the Lead's corrections)

Vocabulary unreadable -> only accept, plain fix ("answer with your approval on this branch" + the accept door), no `answers`: tested.
No HEAD -> no door at all, no words (`_vcs_words` returns nothing; blockers also say "no commit yet"). No-trace and unreadable
pipeline -> accept + go on only, hint names go on, no list: tested. 20 -> all 20 listed + both words; 21 -> no path lines, the over-cap
sentence, accept + go on only: tested. Space / non-ASCII / folder paths come from `-z -uall` (measured forms, no quoted text). Nested
repository (`?? x/`), unmerged XY, operation in progress (existence of the path `rev-parse --git-path <name>` prints, incl. `REVERT_HEAD`),
` A`, home unknown, a person path under the home or with a guard separator: both words blocked. Detached HEAD: commit only blocked.
Staged X (anything but space or `?`), mode 160000, `.gitmodules`: stash only blocked. Rename entries read NEW then OLD. `rev-parse` judged
by exit code (`_git` / `_git_raw` return None on non-zero). Tested through `vcs_blockers` (table, 18 rows) and through `check_vcs` on temp
repositories (cap, no-trace, unreadable pipeline, clean tree).

## AR rows

AR-1 (words are data rows; one grep hit in the touched functions: the keys `"commit"` / `"stash"` of the dict `vcs_blockers` returns, the
shape the spec fixes - they are git verbs, no person's word is read by them), AR-9, AR-13 (one status read, one block builder, one
blocker list, one home reader), AR-16 (hint lines pass `human_text.problems(kind="report")`), AR-22 (`answers` producer `check_vcs`,
readers `render` / `brief_lines` / `gate_brief.render`; `shown_doors` writer / reader), AR-28 (unreadable vocabulary / pipeline / state
file offers or writes nothing). AR-14: the shown-doors writer is one function on both roads (B2 wires the driver).

## FR pass (sections A-C; D-G one line)

A. FR-1/2: the over-cap sentence says what is wrong and names the door (`<id>: go on`, or do it yourself); FR-4: accept and go on stay;
FR-57: no write is offered or taken here, blockers say what stands in the way; FR-59: unknown home / unreadable pipeline / no HEAD offers
no writing word. B. FR-6: `answers` carry the three price lines in the labels of `human_text.price_labels`, commands none; FR-10: forms,
answers and fix name the same words (all from the vocabulary rows). C. FR-11: every offered word has an executor named in data (B2 builds
`repo_words.py`; NOT yet offered-and-executable until B2 lands - B1 alone offers words nothing carries out, as the spec's wave order
intends); FR-12: no phrase list (closed rows, whole-text match); FR-13: words, executors, texts in data; FR-14: n/a. D-G: FR-30 (ASCII
data; Cyrillic / full-width test inputs built from code points), FR-32 (rows), FR-29 (no escapes).

## Tests (each red on revert of its item: yes, see probes)

`test_gate_vocabulary.py::part_finding_door_words` (rows, ASCII, disjointness incl. `gate-approval-words.json`, damaged rows, the
`finding_door_option` read / not-read table of the spec incl. NBSP, `go on, the branch is mine`, Cyrillic, homoglyph, full-width, empty,
`commit​`, 1001 chars). `test_gate_question_form.py`: `test_the_test_repository_question_offers_its_words_with_prices` (message and
accept door literal, door order, list + prices, `human_text`, driver reads each word, `maybe` / `commit please` / `commit` then `commit?`
unread, forms and their examples read), `..._offered_only_where_they_can_be_carried_out` (cap 20 / 21, no-trace, unreadable pipeline,
clean, no vocabulary, no repository), `..._blockers_name_...` (18-row table), `..._shown_doors_have_one_writer_and_one_reader`
(driver form, skill form, three guards, unreadable), `..._answers_are_printed_whole_on_both_roads` (`brief_lines` 7th of 7, render, cap).

Red probes (in memory, `scratchpad/redprobe.py`: a module rebuilt from its source with ONE mutation, nothing on disk touched; full
source is the file named): item 1 two mutations, item 2, item 3, item 4 two, item 5 two, item 6 two, item 7, item 8 two = 13 probes, all
red (FAIL lines or the test crashing on the missing behaviour):

```
[item1 executor/writes read from the row] FAILS=5 :: EXIT 1
[item1 damaged rows kept] FAILS=0 :: KeyError: 'executor'
[item2 writing word read out of a sentence] FAILS=4 :: EXIT 1
[item3 unreadable pipeline closes nothing] FAILS=2 :: EXIT 1
[item4 no blockers] FAILS=16 :: EXIT 1
[item4 untracked folders not listed file by file] FAILS=2 :: IndexError: list index out of range
[item5 cap raised] FAILS=6 :: EXIT 1
[item5 doors of the words not registered] FAILS=1 :: IndexError: list index out of range
[item6 brief_lines cuts the answers row by limit] FAILS=0 :: ValueError: '- [your call] the tree' is not in list
[item6 render drops the answers] FAILS=1 :: EXIT 1
[item7 cap not grown] FAILS=1 :: EXIT 1
[item8 forms of the item's words dropped] FAILS=4 :: EXIT 1
[item8 store keeps nothing] FAILS=2 :: EXIT 1
```

## Witness (verbatim closing lines; all run in this worktree)

`python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <the four owns>` printed 3 scenario files (all
SLOW_TESTS: skipped, CI judges: test_scenario_cart_1, test_scenario_local_1_0108, test_scenario_local_1_arm_b) and 40 keep files. Run:

```
test_gate_vocabulary:           === test_gate_vocabulary: 141/141 ok ===
test_gate_question_form:        === gate question form: 297/297 ok ===
test_gate_preflight (42 s):     === gate rehearsal: 1283/1283 ok ===
test_gate_brief_and_retro (48): === gate brief and retro numbers: 975/975 ok ===
test_words_doors (72 s):        === test_words_doors: 537/537 ok ===
test_environment_record         === test_environment_record: 120/120 ok ===
test_exploratory_answers        === test_exploratory_answers: 107/107 ok ===
test_gate_ordered_reporter      === test_gate_ordered_reporter: 89/89 ok ===
test_gate_role_accounts         44 passed in 1.47s
test_gate_shown                 === gate shown: 129/129 ok ===
test_handed_to_person           === test_handed_to_person: 58/58 ok ===
test_not_needed_role            22 passed in 2.41s
test_one_source_per_fact        === test_one_source_per_fact: 21/21 ok ===
test_oracle_provenance          === oracle provenance: 296/296 ok ===
test_question_register          === question_register: 684/684 ok ===
test_stand_gaps                 === stand gaps: 182/182 ok ===
test_whole_identifier           === whole identifier and the revoked word: 166/166 ok ===
test_detector_verdict           === test_detector_verdict: 195/195 ok ===
test_gate_preflight_question_status === gate A: question status from the register: 25/25 ok ===
test_login_need                 33 passed in 0.98s
test_reference_window           === test_reference_window: 85/85 ok ===
test_external_writes            === test_external_writes: 52/52 ok ===
test_publication_gates          exit 0 (prints no summary line)
gate_brief.py --selftest        GATE_BRIEF SELFTEST: no violations (pyramid, verdict, roll-call, decisions, cap)
gate_preflight.py --selftest    GATE_PREFLIGHT SELFTEST: no violations (classes, brief block, ownership wording)
test_judgment_census            === judgment_census: 22/22 ok ===
selftest.py --lang              === qa-factory selftest: 2/2 ok ===
```

Not run (SLOW_TESTS or not a keep file I could judge in time): the three scenario files above; the other SLOW-listed printed files
(test_blocked_by_env_window, test_branch_accounting, test_bug_records, test_controller_gate_decision, test_gate_registry,
test_manual_capture, test_node_ids, test_profile_reader, test_read_json, test_role_commands, test_runtime_paths,
test_s7_investigation_replay, test_story_run_s6, test_story_run_stand_identity, test_story_run_loop_b_*). One red found and fixed on the
way: `test_gate_preflight` (AST scan "every waiver_command lives inside an add() call") failed on the first shape of `check_vcs`; the
call now sits inside `add(...)` and the item's other doors are registered by an argument that evaluates after `fix` (`_vcs_doors`).

## Changed expectations (old -> new)

None in an existing assertion. Behavioural: the dirty-tree `fix` was "answer with your approval: commit, stash, or go on on this branch"
+ door; now "answer with one of the words listed under this item - <accept door>" (no HEAD or no vocabulary: "answer with your approval
on this branch" + door if any). `finding_door_words()` now returns 4 rows (was 1); the quarantined `test_d1_product_gap.py:216` asserts
`finding_door_word_of() == {"product_gap": "product gap"}` and is stale (never run, never edited).

## Questions for the Lead

1) `says` "product code included" (F1 / Q-1 until the owner's word): nothing in B1's spec says how `finding_door_hint` learns that the
tests live in the product's repository (no flag in its signature, no config key named). NOT built; needs the criterion (e.g. `tests_root`
resolving to the project root / a config key) and whether the clause is a vocabulary field or built text.

## Contract notes for B2 / the Lead (no design decision taken; choices a reader can see)

- `vcs_changes` result: `home` is the tuple `(rel, why)` as `factory_home_place` returns it; `entries` / `person` are dicts `{xy, path,
  orig}` (rename: `path` = NEW, `orig` = OLD); `ops` lists existing operation names; `modes` is filled only when 0 < len(person) <= 20
  (above the cap both words are blocked anyway); `digest` joins the sorted `"<xy>\0<path>\0<orig>"` with "\n". `task_root` is accepted and
  unused until the factory-origin node.
- `vcs_state_block(head, digest="")` builds BOTH blocks (HEAD block, or `test repository changes: <head12> <digest>` with a digest): one
  builder for B2's comparison (the spec names the function for the HEAD block only).
- `vcs_blockers` adds, beyond the spec text: "no commit yet" (both), a path that is not UTF-8 text (U+FFFD after the lossy decode; both),
  `index.lock` among the operation names (G2 lists it). Keys `commit` / `stash`; B2 maps a row's executor with `removeprefix("git_")`.
- `_git_raw` (new, unstripped) is the `-z` reader; `_git` strips and would eat the first status space.
- Skill-path `keep_shown_doors` stores `{id: waives}` only for findings that CARRY waives (spec); the driver's `last_rehearsal_doors`
  (`driver_gates.py:336`) stores every finding id with a (possibly empty) list - B2's `Driver.gate` rewrite should choose one shape; the
  CLI finds a door by option so either works. `read_finding_doors` compares `stored[id]` with the current `waives` and reads "no stored
  entry" as changed, which for a finding with NO waives differs between the two shapes.
- The skill-path write does not happen when there is no file and no doors (no `driver-state.json` is created for nothing).

## Analogs noticed (not touched)

- `gate_preflight.py` other `_git(..., "status", "--porcelain")` readers strip the first line's status (`porcelain_path` is the existing
  workaround): any further reader of the change set should use `vcs_changes`.
- `tests/test_gate_preflight.py` AST pin on `waiver_command` inside `add()` (B2's file) constrained the shape of `check_vcs`.

## Needed beyond the manifest

`scripts/driver_machine.py` (`read_finding_doors`), `scripts/driver_gates.py:295-350`, `scripts/human_text.py`, `references/human-text.json`,
`references/human-questions.md`, `references/gate-approval-words.json`, `scripts/critic_rollcall.py`, `scripts/slow_tests.json`,
`tests/test_gate_preflight.py:486-525, 4170-4200`.
