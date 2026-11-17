# Builder report - t-1035, card S9 (a person's word on a `review` gap, FR-57)

Commit (code, tests, state-exits row): `b87cceee` on `worktree-agent-abb8f45302b3ae471`. Not pushed, not merged, no journal lines.

## Step 0 - the premise run (executed first)

The card's literal recipe could not be run on the bare `cart-1` copy. Three scratch-only setups were needed (none touches the repo):
the story folder must be named `CART-1` (`event_store` checks `task_id == root.name`), the project needs `qa-factory/config.json`
(taken from `state/config-at-start.json` of the fixture, `bytes_b64`), and the manifest's test files must exist under the project
(stubs `// stub` at the paths of `tests[].file`, otherwise `input_hash is missing` and no `review:` gap is reached).
Window `S5-qa-code-critic-2` has no `review.verdict` stored (the CLI rebuilds the window from the manifest), so the manifest's
`critic_verdict` of the first test (`@api @regression CART-1_TC_001 add unknown or sold-out book rejected`, was `unverified`) was deleted, as the card allows.
The word: stage S5, `match` = `review:<iid> — the manifest row carries no \`critic_verdict\`` (the real-data shape), decision `go on, they stay unverified`.

Command: `CLAUDE_PROJECT_DIR=<scratch>/proj python -B ai-packages/qa-factory/scripts/window_record.py --task CART-1 --dispatch S5-qa-code-critic-2 --out <scratch>/w.json`, filtered to `recorded, not read|^  - review:`. Verbatim:

```
note: recorded, not read by this window: go on, they stay unverified — the verdict of such an instance is `unverified` (a static review): the critic records it through `manifest_put.py`
  - review:@api @regression CART-1_TC_001 add unknown or sold-out book rejected — the manifest row carries no `critic_verdict`, and this instance's probe could not run here (a person's word or the factory names it); the verdict of such an instance is `unverified` (a static review): the critic records it through `manifest_put.py`
```

Expected line appeared (the gap line `review:<iid> — ...` and the `note: recorded, not read by this window` line naming the word). Premise true. (With a match that is NOT a whole-words part of the line - my first try dropped the backticks - the note is absent: `_unread_words` uses `split_overridden`'s whole-words rule. This is the observation that the card's "whole line" real data does print.)

## What was done (items of card S9)

1. `window_record.review_gap_words(window, task_root)`: new, never raises. Rule of section 2.2 item 2: live S5 records of `task_root/pipeline.json` via `contract.live_stage_overrides`; `match` must be a string; stripped; not `*`; no `waiver.PLACEHOLDER_RE`; instance named when `m == "review:"+iid` or `m.startswith("review:"+iid+" — ")` (space, U+2014, space), case-exact; one record names one instance (exact equality first, else the longest id: F9-3 (a)); latest record by file order wins; words whitespace-folded, `at` kept. Test: `s9_review_gap_words` (new, 60 rows) in `test_window_record.py`, registered in `pure_group`.
2. `word_let_go(lines, window, index, lets_go=None, review_words=None)`: third rule; lets go `review:<iid>` and `review:<iid> — ...` for each iid in `review_words`; `review_words=None` lets nothing go; runs when `index is None` (E9) and when the not_run/row_fields table read raises (that part now lets nothing, the review rule still works). Docstring names the three rules. Rows added to `fv1_30b_word_let_go_is_the_one_predicate` (6 rows incl. U1 at the predicate, index None, absent default, bad `review_words`).
3. `word_kept` passes `review_words=review_gap_words(window, task_root)`. Row in `fv1_30b_n6_the_three_judges_read_the_one_survivor` beside the old one: `word_kept(["review:A"], ...)` with a pipeline holding `review:A` -> `([], ["review:A"])`.
4. `verdict`: a `review` gap whose instance `review_gap_words` names joins `read`. Rows in `a_word_nothing_reads_is_printed_and_changes_nothing`: exact word and word with the ` — reason` tail: no unread note; `Review:test_a[x]` (case): still one unread note. `*` is already covered by the existing "every" rows (unchanged: 2 notes).
5. `GAP_ORIGIN["review"]` door: `REVIEW_GAP_RECORD = person_words.door('waiver.py --task <T> --stage S5 --block "review:<instance id>"')` (the same one-renderer form as `PROBE_GAP_RECORD`, so the words go by file), appended to the door; the two comments (`GAP_ORIGIN` review comment, `WORD_READ_KINDS` comment) rewritten. Row: `check_in` of `--block "review:` over `WR._explain("review:x", [])`.
6. `Controller._s5_gap_problems` (only that function): passes `review_words` to `word_let_go`; when `not problems`, one `_record_person_pass("S5", d.id, [...])` item per let-go `review:<iid>` line with the fields of the card (`error`, `decision`=words, `at`, `by`, `check: review`, `case: ""`, `tag`, `subjects`). Rows in `test_probe_gap_word.py::s9_a_review_word_at_the_controller`, every row with `p` carrying neither `unresolved` nor `reason`: (a) exact word -> accepted, ONE line (block `review:IID`, words whole, `word_at`, subjects); (b) `*` -> refused `unresolved window: review:IID`, no line; revoked word likewise; (c) U1 both directions plus a word for each (two lines, own words); (d) typed pair, no word -> accepted as today, no line; plus `passed_green` stays refused.
7. `design/state-exits.md`: one row (S5 review gap passed by the person's word) after the `contradicts_requirement` row.
8. Census row: VOID by Lead decision (N-1); `judgment-census.json` not touched.

Lead decisions applied: F9-3 (a); F9-1 stays reading (i) (delivery untouched, ledger/check_delivery/kinds not touched).

`controller-blocks.md`: not regenerated. A generator run to a scratch path (`python -B tools/controller-blocks-gen.py <scratch>/cb.md`) is byte-equal to the committed file (`diff` empty after CR strip), so no block text of `_s5_gap_problems` changed.

## Witness

DoD command (the walker prints what judges the owned paths; the slow files it names are NOT run locally - judged by the batch canon: test_window_record.py, test_probe_gap_word.py, test_controller_*, the scenario tests):

```
$ python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/window_record.py ai-packages/qa-factory/scripts/controller.py
scripts/window_record.py: scenario test_scenario_cart_1.py (story cart-1)
scripts/window_record.py: scenario test_scenario_dry_1.py (story dry-1)
scripts/window_record.py: scenario test_scenario_local_1_0108.py (story local-1-0108)
scripts/window_record.py: scenario test_scenario_local_1_arm_b.py (story local-1-arm-b)
scripts/window_record.py: keep test_blocked_by_env_window.py ... test_probe_gap_word.py ... test_state_exits.py ... test_window_record.py (layer gate_named, covers it)   [22 `keep` rows]
scripts/controller.py: scenario test_scenario_cart_1.py / test_scenario_dry_1.py / test_scenario_local_1_0108.py / test_scenario_local_1_arm_b.py
scripts/controller.py: keep ... (84 `keep` rows, ending test_words_doors.py)   [113 lines in all]
```

(the full 113-line listing was captured to a scratch file; every line is `scenario` or `keep`, no `FAIL`). The walker names no fast file to run: all named files are slow or scenarios -> "judged by the batch canon".

`python -B tools/architecture_index.py --check`: `architecture index: up to date (29 invariants, 2682 bytes)`, exit 0.

Pre-witness smoke (NOT the witness; run so the new rows are not shipped blind): the new/extended test functions called directly in one process (`fv1_30b_word_let_go_is_the_one_predicate`, `s9_review_gap_words`, `s9_a_review_word_at_the_controller` -> `=== smoke: 107/107 ok ===`; `a_word_nothing_reads_is_printed_and_changes_nothing`, `fv1_30b_n6_the_three_judges_read_the_one_survivor` -> `=== smoke2: 76/76 ok ===`). The whole files were not run.

Commit: pre-commit gates ran (`gates: ok (7 checks)`, `gates: ok (4 checks)`, factory rules index up to date).

## FR walk (A, B, D, E; C, F, G one line each)

- A FR-4: the informed pass is recorded (`_record_person_pass` per lifted review gap, only for an accepted completion). FR-57: the ban has a door now (`waiver.py --block "review:<instance id>"` in the gap's door text). FR-2: the door is one the orchestrator can use (it records the word; the critic returns the item). FR-1, FR-3, FR-5, FR-46, FR-48, FR-50: not applicable (no refusal text, no conductor call, no artifact requirement changed; the refusal `unresolved window: ...` is unchanged).
- B FR-7: the same boundary is not re-asked: a word naming the gap is read and not printed "recorded, not read". FR-8: the words travel whole (folded whitespace only; `word_at` points to the record). FR-6, FR-9, FR-10: the door text is for the orchestrator (not a person-facing question); no packet changed.
- D FR-59: unknown is never a pass (unreadable pipeline, `*`, revoked, other stage, placeholder, non-exact head -> nothing let go; rows E1-E6, E12, U1-U4). FR-16, FR-17, FR-18, FR-40, FR-58: FR-40 - the state has its way out (row in `state-exits.md`: a critic verdict later, or revoke); others not applicable.
- E FR-35: the critic's verdict is never rewritten; delivery still reads `review_gap`, `no`, owner `review` (reading (i)). FR-19..FR-23, FR-36, FR-37, FR-53: not applicable (no delivery text or path changed; FR-37: the door text names the real `waiver.py` command and block form `review:<instance id>` the code reads).
- C: FR-11/FR-14 - no field required from a role; the pass line fields are written by code. F: no measurement touched. G: FR-30 the diff is English (no Cyrillic); FR-29 no escape bytes (non-ASCII test ids are literal characters in the files - U+00DC, U+00EF, U+00FC, U+2713, U+2013 - not `\u` escapes; no Cyrillic, no control byte); FR-33: S9 stays "closed by code, not proven" until the `live-runs` row of the card is run.

Architecture: AR-13, AR-15, AR-24 (named in the commit) plus AR-25, AR-27, AR-28 as in the commit text.

## Deviations from the spec / divergences from reality

- Step 0 needed the three scratch setups above (the card says only "copy `cart-1`, add a record, run"). The premise holds.
- Item 5 door text is built with `person_words.door(...)` (adds the `--words-file <file>` form) rather than the raw string of the card; same road as `PROBE_GAP_RECORD`, the card's required substring `--block "review:` is present.
- `word_let_go`: besides the card's `index is None` case, an exception while reading the not_run/row_fields table also no longer hides the review rule (same invariant: a broken precheck does not hide a person's word; a broken word read lets nothing go).
- `review_gap_words` returns the folded words and `at`; the controller reads both from it (no second read of `pipeline.json`).
- `tests-over`: yes (stated in the commit): the card's U1-U4 and E1-E12 rows are table rows.

## Needed beyond the manifest

`ai-packages/qa-factory/scripts/hooklib.py` (the "refusing to create one" project-root rule), `ai-packages/qa-factory/scripts/event_store.py` (task id must equal the folder name), `ai-packages/qa-factory/scripts/person_words.py` (`door`), `ai-packages/qa-factory/scripts/contract.py` (`live_stage_overrides`, `manifest_test_links`), `ai-packages/qa-factory/scripts/waiver.py` (`PLACEHOLDER_RE`), `tools/architecture_gate.py` (judgment line forms), `ai-packages/qa-factory/scripts/tests/harness.py`, `test_probe_gap_word.py` helpers (`TW.a_story_at_s5`, `TB`), `ai-packages/qa-factory/scripts/tests/fixtures/stories/local-1-arm-b/pipeline.json:615-635` (real ids for the U1 real-data row).

## Analogs noticed, not fixed

- `window_record.py` `NO_DOOR` and the comment at GAP_ORIGIN `stale_run` say "no recorded word of a person is read for it": still true for every kind except `review`; no change needed, listed for the critic's class check.
- `acceptance.py:1157-1172` (the controller's bare `review:<iid>` lines) and `ledger.py` read the review state independently of the word; F9-1 follow-up (ii) will have to read `review_gap_words` (one reader, AR-13).
- `docs/OWNER_PRINCIPLES_INDEX.md` was regenerated by `tools/factory_rules_index.py` when pre-commit said the index was stale; it shows modified and unstaged in this worktree (not committed, as instructed). Whether `origin/main` carries the same stale index: not verified.
- A stray file `--help` was created at the worktree root by my own probe of `tools/controller-blocks-gen.py --help` (the generator treats its first argument as an output path, it has no `--help`); removed before the commit. A real usage hazard of that tool: `--help` writes a file.
- The card's section 2.4 readers grep (`window_record|controller\.py|state-exits|...` over `tools/`, `.githooks/`, `.claude/`) was not run by me beyond the walker output.

## Fix round (critic t-1040)

Commit `07d571d1` (this section in the follow-up commit). Finding -> change -> place (window_record.py = `ai-packages/qa-factory/scripts/window_record.py`):

- F1 -> new `_review_owner(text, ids)` (exact head first, else longest id + ` — `); `review_gap_words` and `word_let_go` both call it; `word_let_go` lets a review line go only when its owner among ALL non-empty window ids is in `review_words`. Rows added to `fv1_30b_word_let_go_is_the_one_predicate` (ids `A`, `A — x`, lines `review:A`, `review:A — x`, `review:A — x — e`, `review:A — e`; both directions + a word for an unheld id). window_record.py `_review_owner`, `word_let_go`; test_window_record.py after the U1 predicate row.
- F2 -> state-exits.md row exit cell: a later critic verdict removes the gap; the recorded pass stays in `passed-by-person.jsonl` and the report keeps printing it as a past pass.
- F3 -> `WORD_READ_KINDS` comment now says "and, through `word_let_go`, for the gaps it names".
- F4 -> the two new head tests are one `_review_owner`; the two older ones (problem line against head, P-i precedent) left as the verdict says.
- F5 -> `_index_let_go(window, index, lets_go) -> set` holds the old index body verbatim (set() on any exception); `word_let_go` is the union with the review rule. controller.py `_s5_gap_problems`: `iid` bound once (generator `for iid in [g.partition(":")[2]]`) - controller touched because F5 names it. Checked: all the old rows of `fv1_30b_word_let_go_is_the_one_predicate` (not_run, row_fields, raising index, non-object window) still PASS, see output.
- F6 -> the sentence above (line 68) now says literal characters.
- F7 -> no code change, pinned by two rows in `s9_review_gap_words`: `["A "]` + `review:A ` -> none (word stripped); `["A "]` + `review:A  — x` -> `["A "]`.

Scratch script `scratchpad/rows.py` calls the two row functions directly (source: imports `test_window_record`, runs `fv1_30b_word_let_go_is_the_one_predicate` and `s9_review_gap_words`, optionally with `t.WR` swapped for a given module). Output on the fixed tree: `ran, exceptions: 0`, 93 PASS lines, no FAIL (was 88).
Negative control, pre-fix module from `git show b87cceee:.../window_record.py`:
`FAIL S9 (F1, U4 at the predicate): the word for `A` lets go `review:A` and `review:A — e`, never the gap of `A — x` — expected (['review:A — x', 'review:A — x — e'], ['review:A', 'review:A — e']), got ([], ['review:A', 'review:A — x', 'review:A — x — e', 'review:A — e'])`
Other: `scenario_walk.py --witness-for .../window_record.py` printed its list (scenario tests, keep rows; test_window_record.py and test_probe_gap_word.py are slow: judged by the batch canon). `test_state_exits.py`: `=== test_state_exits: 142/142 ok ===`. `s9_a_review_word_at_the_controller` called directly: no FAIL.

Needed beyond the manifest: controller.py (F5 names it), test_state_exits.py (run, state-exits.md owner test). Not done: the line in spec §4 "follow-up node of (ii)" (the spec is not in owns) - Lead to add: "F9-1 follow-up: the recorded review pass stays under fact `other` after the gap is repaired; give the review word its own fact".
Analogs noticed, not fixed: the two older head tests at window_record.py (problem line vs head); `tools/controller-blocks-gen.py --help` writing a file (the verdict's carry-over).
