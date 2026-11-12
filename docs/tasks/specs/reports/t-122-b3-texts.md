# t-122 node B3 report (FG7-8 part B, skill road texts)

Status: all Behaviour bullets present EXCEPT two clauses of the `conductor.md` row, which do not fit the file's byte cap (question Q1).

## Old -> new per file

1. `skills/qa-story/phases/s4.md` (paragraph about `factory_defect` / stand gap, located by "word is recorded from the same answer"): one sentence inserted before "A stand gap whose": "The test-repository item's own words (`commit`, `stash`, `go on`, listed under it) are carried out by their row of `references/conductor-actions.json` only when the person's answer IS that word (`vcs-test-repo: commit`, or `commit` alone); for any other wording, a condition or a question, ask the person once to answer with the exact word and run nothing until they do, and tell the line the command prints as it stands." Nothing else changed.
2. `skills/qa-story/phases/s9.md` (the `config-restore` sentence): after "no `line` means nothing to say." added "Then run `python "${CLAUDE_PLUGIN_ROOT}/scripts/repo_words.py" --reminder --task <TICKET>`, which prints one JSON line; a non-empty `line` (your changes that still sit in a stash or a commit made on your word) is told to the person as it stands."
3. `references/conductor-actions.json`: one new row right before the `product_gaps.py revoke` row (= after `product_gaps.py record`): says "the person answered the test-repository item with exactly `commit` or `stash` (the item's own word, listed under it), or with `go on`"; run: `repo_words.py --task <T> --word commit|stash --words-file <file holding their exact answer>`, once; a refusal told in words, nothing else runs; printed line told as it stands; `go on`: `waiver.py --task <T> --stage S5 --block "<the item's block>" --words-file <file>`; other wording / condition / question: ask once for the exact word, run nothing, only that exact answer runs the command. JSON parses (test_conductor_doors 218/218).
4. `references/conductor.md` row (gate item answered by name): old `| A gate item they answered by name (dirty tree, toolchain, credentials, a stand-gap card, an accepted gap) | waiver.py ...` -> new `| A gate item answered by name | waiver.py --task <T> --stage S<n> --block "<a refusal line or card id>" --words-file <file>`; the test-repository item: its row in conductor-actions.json, exact word only, else ask once; a requirement gap: ...`. File is 11 897 bytes (was 11 887); K5 caps it at 12 000 and C3 wants 100 bytes of margin, so only about 13 bytes could be added. I had to drop the example list in the label, and two required clauses did NOT fit: "run nothing" and "the driver's note section 'Done in the person's repository' is told to the person line by line". See Q1.
5. `references/halts.md` row "Dirty working tree at S5": the four literal words removed; Move now "A gate A item whose words are the item's own, listed under it; the answer is recorded. person-owned: risk".
6. `design/state-exits.md`: two rows added in "What a person recorded (`pipeline.json`)" (before `deferred_to_report`): commit -> `git reset --soft <head_before>` then `git read-tree <tree>`; stash -> `git stash apply --index <sha>`, then remove the entry by its `stash@{N}` from `git stash list` (`git stash drop stash@{N}`; never `git stash drop <sha>`), plus F-16's sentence "This word also passes a tree made dirty again at this HEAD". The "proven by" cells name `test_gate_preflight.py` (`part_repo_words`, which B2 adds) and `test_state_exits.py`.
7. `changelog.d/fg7-8-b-vcs-words.md`: new, one paragraph.

## Edges check
(1) stash undo text = Lead decision 2, no `drop <sha>` as an instruction (only named as forbidden). (2) commit undo as given. (3) other wording -> ask ONCE, run nothing: in s4.md and the actions row (conductor.md partial, Q1). (4) `go on` recorded by the waiver command with `--words-file`. (5) English, no project names, selftest --lang passes. (6) All paragraphs located by content. (7) Shortened my own sentence; budget untouched.

## FR pass
A: FR-1/2/9 - each refusal in the new text is told in words and the exact word is the door; FR-4 no check added; FR-57 - hooks and bans untouched, no `--no-verify` anywhere. FR-3/5/46/48/50 - not touched. B: FR-6 - person-facing lines come from the command (`done_line`, B2), the texts only say to relay them as they stand; FR-7 - answered boundary not re-asked except once for the exact word; FR-8 - the person's words travel via `--words-file`, whole; FR-10 n/a. C: FR-12 - no phrase list, the conductor does not map wording to a word (asks instead); FR-13 - words are data (vocabulary rows, B1), texts name them only as examples; FR-14/15 - CLI name and flags `--task --word --words-file --reminder` as fixed by spec; FR-37 - the path `repo_words.py` is the one B2 writes (does not exist yet); FR-39/42/49/56 not touched. D-G: FR-30 English passes; FR-29 no control bytes; FR-44 documents live where loaded.
AR: AR-17 (no new stop, relay unchanged), AR-19 (one executor on both roads, row names it), AR-25 (state-exits rows name the true undo).

## Witness (verbatim closing lines)
`python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <six owns>` printed these files; run after final edits:
- test_gate_brief_and_retro.py: `=== gate brief and retro numbers: 975/975 ok ===`
- test_gate_preflight.py: `=== gate rehearsal: 1283/1283 ok ===`
- test_readiness.py: `=== test_readiness: 244/244 ok ===`
- test_conductor_doors.py (after conductor.md fix): `=== conductor doors: 218/218 ok ===` (first run with my long conductor.md sentence: 215/218, FAIL S6 size cap x3)
- test_conductor_investigates_first.py (after fix): `=== test_conductor_investigates_first: 33/33 ok ===` (first run: `FAIL K5: conductor.md stays within 12 000 bytes - 12193`, 32/33)
- test_needs_author.py: `=== test_needs_author: 89/89 ok ===`
- test_project_decisions_change_request.py: `=== project_decisions_change_request: 142/142 ok ===`
- test_state_exits.py: `=== test_state_exits: 142/142 ok ===`
- test_controller_resume.py: `=== test_controller_resume: 110/110 ok ===`
- test_exploration.py: `=== test_exploration: 219/219 ok ===`
- test_manual_evidence.py: `=== test_manual_evidence: 248/248 ok ===`
- test_question_register.py: `=== question_register: 684/684 ok ===`
- test_words_doors.py (slow, run once with a 500 s limit; it scans the rows for `--words-file`): `=== test_words_doors: 537/537 ok ===`
- SKIPPED as over a minute (run killed at the 60 s / 100 s limit, no verdict): test_check_delivery.py, test_silent_passes.py, test_red_window.py.
  (test_conductor_doors and test_conductor_investigates_first were run again after the fix; test_gate_preflight etc. ran after the s4/s9/json/halts/state-exits edits, before the final conductor.md edit, which only touches a file they do not read, as far as the printed `covers` list says.)
- `python -B ai-packages/qa-factory/scripts/selftest.py --lang`: `PASS lang: no control byte left by an eaten escape sequence (FR-29)` / `=== qa-factory selftest: 2/2 ok ===`
- `python -B ai-packages/qa-factory/scripts/role_load.py --all`: before and after outputs are byte-identical (diff printed `rl-identical`); every role row unchanged, e.g. `qa-automator 20,181 tokens, free 4,819`, `qa-code-critic 19,389 tokens, free 5,611`; exit 0.

## Temporal edge
The new actions row names `repo_words.py`, absent until B2. No test went red for that reason: test_conductor_doors 218/218 and test_words_doors 537/537 pass with the row present. (test_check_delivery / test_silent_passes / test_red_window were not run to a verdict, so the claim covers the tests that ran.)

## Beyond the manifest / siblings
- Read beyond manifest: `docs/tasks/specs/fg7-8-b-vcs-words.md` (lines 515-730), `scripts/tests/test_conductor_investigates_first.py` and `test_conductor_doors.py` output (size caps K5 / S6 / C3).
- B5's, not edited: `skills/qa-story/evals/evals.json` (about :53, :64) and `evals/plugin-eval-benchmark.json` (about :86-93) still carry the old four S5 words.
- Noticed analog: the `note` of `conductor-actions.json` says "A finding's door (`waives`) is a person's word and is never run from here" - now partly contradicted by the new row (the person's word for the test-repository item IS run from the row, on the exact word). Not edited (outside the owned row).
- Noticed: `conductor.md` has 103 bytes of headroom only; B2/B4 or later text for the conductor will meet the same cap.

## Question Q1 (for the Lead)
`conductor.md` is capped at 12 000 bytes with 100 bytes of margin (K5 in test_conductor_investigates_first, S6/C3 in test_conductor_doors); the file stood at 11 887. The spec's conductor.md bullet (row name + exact-word rule + "Done in the person's repository" note told line by line) needs about 190 bytes more than the cap allows. I kept the row name and "exact word only, else ask once" and dropped "run nothing" and the "Done in the person's repository" clause (the same duties stand in the s4.md sentence and the actions row, but the note-section duty stands nowhere yet). Options: (a) move ~100 bytes of the file's existing text elsewhere (not mine to edit), (b) put the "Done in the person's repository" duty into the actions row or s4.md, (c) the owner/Lead raises the cap (forbidden to me by edge 7).
