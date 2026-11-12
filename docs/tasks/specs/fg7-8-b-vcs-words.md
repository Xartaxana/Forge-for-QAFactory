# FG7-8 part B — the words of gate A's test-repository question get rows, an executor and a record (B-13)

Draft by the designer, task t-106, node `forge/7/FG7-8` item 4 (feature F19), 12.11.2026. Forks are returned (§5),
not decided. Part A of the same node (builder t-105) runs in parallel; §4.0 says what lands after what.

Owner's word folded in (12.11.2026, relayed by the Lead during this draft): **the factory MAY itself run `commit` and
`stash` in the person's test repository when the person answers with that word.** This spec therefore writes the
executor as code that runs the command on the person's word, records it, and refuses with a door when the command
fails. What stays open is the command's scope, its message, P8, the record and failure handling (§5).

### Lead acceptance of the draft (12.11.2026, t-106)

The draft is accepted as the plan that goes to the critic on the plan. Forks of §5, decided by the Lead on the
designer's recommendations ("by recommendation, until the owner's word" where marked):

- **F1 = (a)**, by recommendation, until the owner's word: exactly the set the person was shown, outside
  `qa-factory/`, one commit, a factory-written message naming the story, the repository's own identity, the person's
  hooks running. The `says` line names "product code included" when the tests live in the product's repository.
- **F2 = (a)**: follows P8 directly — a run that leaves no trace neither offers nor runs `commit` / `stash`.
- **F3 = (a)**: the waiver's decision text carries the facts and the undo; no new record file. Whether a stash is
  listed under "Left with you" in the report is asked of the owner; (b) opens as its own node if she says yes.
- **F4 = (a)**, **F5 = (a)**, **F6 = (a)** (B5 is filed as a finding into an untaken batch), **F7 = (a)**.

B0 (the measurement) runs now, beside the critic on the plan; its table becomes F0-23. B1 waits for part A on `main`.

---

## §0 Facts (read in the carrier today, file:line)

| # | Fact | Carrier |
|---|---|---|
| F0-1 | `Rehearsal.check_vcs` (`:1917-1953`) writes two `person_decides` findings with `subject="test-repo"` (id `vcs-test-repo`). The dirty branch's `fix` is the literal `"answer with your approval: commit, stash, or go on on this branch"` (`:1946`) plus `waiver_command(block)`. The clean branch's `fix` is the literal `"answer with your approval: this branch, or name another"` (`:1952`). | `scripts/gate_preflight.py` |
| F0-2 | The door block is `test repository state: <HEAD[:12]>` (`:1939`), so a word stays valid while S5 writes into the tree, and a moved HEAD asks again (GW1-43). No HEAD means no door. | `gate_preflight.py:1936-1939` |
| F0-3 | Dirty paths are `outside_factory_home(status --porcelain lines, _factory_home_in_repo(...))` (`:1934`). Paths are read with `porcelain_path` (`:237`). A rename line `old -> new` stays in when either side is outside the factory home (`:244-258`). The message names the first 5 paths and "and N more" (`:1944-1945`). | `gate_preflight.py` |
| F0-4 | `_git` is read-only, 10 s timeout, no prompts (`GIT_TERMINAL_PROMPT=0`, `GCM_INTERACTIVE=Never`). It returns None on a non-zero exit (`:210-220`). | `gate_preflight.py` |
| F0-5 | `door(block, stage, option, row)` appends `{block (cut at 60), stage, option}` to the finding's `waives` (`:1318-1326`). `waiver_command` shows the door in words, `write \`<id>: accept\` with your reason` (`:1338-1353`). `add` drops a finding that a recorded word passes, through `waiver.split_overridden(matched_text(message, doors))` (`:1394-1414`). | `gate_preflight.py` |
| F0-6 | `render` prints each finding as `  - [id] message` and then `      fix: <fix>` on ONE line (`:5811-5814`). `brief_lines` (the "After your approval" block) prints the message only, and the `fix` only for `story_level` rows (`:5980-5985`). | `gate_preflight.py` |
| F0-7 | `FINDING_DOOR_OPTIONS = ("product_gap",)` (`:776`). `finding_door_words()` reads `question-vocabulary.json` `finding_door_words` and drops a row whose option is not in the tuple or that has no word (`:779-793`). `finding_door_option(rest, rows)` reads the word alone, a synonym alone, or the word plus a separator plus a reason kept whole (`:796-809`). `finding_door_word_of()` (`:812-814`). Matching uses `_word_key`: lower case, quotes and backquotes out, spaces collapsed, a closing `.`/`!` dropped (`:709-714`). | `scripts/gate_brief.py` |
| F0-8 | `_open_item` takes the `accept`/`any` door of `waives` as the item's line door (`:465-480`). `_finding_forms` offers `<item id>: accept <your reason>` and `approve as is` (`:2854-2876`). `answer_forms` is the one list of answer forms, each with its `reader` (`:2894-2904`). | `gate_brief.py` |
| F0-9 | The vocabulary block `finding_door_words` has one row, `product_gap` / `product gap` (`:91-98`). Its note says a word of the block belongs to no other block of the file. `probe_answers.live: false` is the precedent "an offered word nobody executes would pass the card on a promise (FR-9)" (`:99-101`). `exploratory_question_words` rows carry the price lines `factory` / `you` / `story` (`:42-63`). No row for commit/stash/go on exists (whole file read). | `references/question-vocabulary.json` |
| F0-10 | `Driver.read_finding_doors` (`:3078-3185`). A line is read only if the id is a finding of this rehearsal, the packet shown carried `[id] message`, the stored `shown_doors` equal the current `waives`, there is no `?`, and the word is a stand-gap word, else a `finding_door_words` word (`:3140-3144`). The door must take that option (`:3163`). The person's last line per id decides it. Unread lines are named, never dropped. | `scripts/driver_machine.py` |
| F0-11 | `_stand_gap_lines` runs ONE fresh rehearsal at answer time and calls `read_finding_doors` against `qtext` / `shown_doors` (`:2769-2801`). `_record_door_lines` (`:2837-2877`) has a `product_gap` branch that calls `product_gaps.record` (`:2847-2863`, the precedent of "a door option has its own executor"). Every other option records `waiver.py --stage --block --decision <person_decision(word, line, replaced)>` (`:2864-2876`). A failed record joins `failed`, then `hold`, and reaches the conductor once (`:2613-2626`). | `driver_machine.py` |
| F0-12 | `_relay_note` gives the conductor the unread lines and, per finding door, `block`, `stage`, `word option` (`:2908-2969`). | `driver_machine.py:2937-2940` |
| F0-13 | `story_run.py` is a facade. `read_finding_doors` lives in `driver_machine` (`fixtures/driver-layers.json:867`). | scout t-104; `driver-layers.json` |
| F0-14 | The guard's rules for a factory commit and stash. Rule 5 `rule_pathspec` (`:2361`): no `-a`, paths named after `--`. Rule 7 `rule_stash` (`:2410`): a stash names its paths after `--` and never `qa-factory`, or excludes it. Rule 3 `rule_manifest` applies to a commit of test files (`:2870`). `check_command` applies them to the orchestrator's Bash commands (`:2845-2877`). It does not see a subprocess a script runs. | `scripts/stage_guard.py` |
| F0-15 | `external_writes.closed_by_run(task_root)` is the one reader of `pipeline.no_trace` (P8, FR-53) (`:189-202`). `conductor-actions.json` rows say "a story that leaves no trace refuses it" for registry writes (`:26-29`). | `scripts/external_writes.py`; `references/conductor-actions.json` |
| F0-16 | The skill road's twin of a door word with an executor is a conductor-actions row: `product_gaps.py record --task-root <r> --row ... --gate A --words-file <file>` (`:30`). | `conductor-actions.json` |
| F0-17 | `s4.md:159-163`: on the skill road the orchestrator records `<check id>: accept` and the reason from the same answer. `conductor.md:21`: a gate item answered by name (the dirty tree included) is recorded with `waiver.py ... --words-file`. | `skills/qa-story/phases/s4.md`; `references/conductor.md` |
| F0-18 | `halts.md:19` still offers "stash / commit / proceed with a warning / abort" for a dirty tree at S5. Two eval files expect the same four words and a "phases/s5.md step 1" that `s5.md` no longer has (grep `stash\|dirty` in `s5.md`: no hit; the same Grep found other `s5.md` lines): `skills/qa-story/evals/evals.json:53,64` and `evals/plugin-eval-benchmark.json:86-93`. | read |
| F0-19 | Test layers. Keep (canon): `test_gate_question_form.py` (`:1896`, AR-16 detector, holds the `answer_forms` / reader table at `:744-833`), `test_gate_vocabulary.py` (`:2005`, holds the stand-gap vocabulary adversarial battery `part_stand_gap_words`, `:250-331`), `test_words_doors.py` (`:6790`, sole AR-24 detector). Quarantine (never edited): `test_decision_classes.py` (`:7652`, holds today's `vcs-test-repo` table c7 at `:427-489`), `test_d1_product_gap.py` (`:7596`). | `scripts/tests/test-layers.json` |
| F0-20 | Judgment census: `gate_preflight.check_vcs` is class `safety`, owner `intent` (`:340`). The ceilings only go down: `word-list: 0`, `safety: 54` (`:4`). | `scripts/tests/fixtures/judgment-census.json` |
| F0-21 | SIBLING_MAP axis 5, row 139: "a word offered anywhere must be offered, read and executed everywhere or nowhere" (reporter card). Row 137: gate A/B stand-gap words. Axis 34 (`:580-590`): one road. No axis-5 row names the VCS words. | `docs/SIBLING_MAP.md` |
| F0-22 | No driver part executes a VCS word. The id `vcs-test-repo` appears only as the id convention (`gate_brief.py:493`) and in tests. | scout t-104; Grep `read_finding_doors\|finding_door` over the package (hits listed in the trail) |

---

## §1 Scope, invariants, AR-n

**Goal.** Each word that gate A's test-repository question offers is a data row with a named executor. The hint is
built from those rows. A word the person writes reaches its executor on both roads. The action is done and recorded,
or it fails with a door. A word with no row is never a pass: it goes to the conductor with the list of words.

**In scope:** the dirty-tree finding of `check_vcs` and its three words `commit`, `stash`, `go on`.
**Non-goals** (the Lead's): part A (answered questions in the register); how gate A detects the VCS state (the
detection code is moved into a helper without any change in behaviour, B1); new words beyond the three; the
clean-tree literal and `check_stand`'s literal (siblings of the same class, queued node B5, F6).

### Invariants (each named edge in §3/§4 protects one of these)

- **I-1 Nothing is promised that nothing executes.** A word the hint offers has a row, a reader and an executor on
  both roads, or it is not offered (FR-9, axis 5 row 139).
- **I-2 A repository write takes exactly what the person was shown.** A commit or stash takes exactly the change set
  the shown packet was built on (same HEAD, same set of dirty entries). It never takes the factory's own folder and
  never takes a path git cannot name exactly. Any difference means nothing runs.
- **I-3 A repository write is never inferred.** `commit` / `stash` run only from the closed word, read whole, with no
  `?`, on a door the shown packet carried. Free words, two words, a word in another language, or a word on a stale id
  go to the conductor, and no code-side phrase list reads them (FR-12).
- **I-4 A ban is never bypassed.** The executor's command passes the same guard rules a factory commit or stash
  passes on the orchestrator's road (rules 3, 5 and 7). The person's own git hooks run; there is no `--no-verify` and
  no `-c` override of the person's config (FR-57).
- **I-5 An answered boundary is not re-asked.** After `commit` (HEAD moves) or `stash` (the tree changes), the same
  question is not shown again with the same text (FR-7).
- **I-6 A failure is the factory's to report, not the person's to resend.** A failed command records no pass. It goes
  to the conductor once, with git's own text, and the person is not asked to send the answer again (FR-3, P22).
- **I-7 A run that leaves no trace writes nothing into the project's repository** (P8, FR-53, FR-36). This is the
  recommended reading of F2.

### Architecture invariants touched (AR-n) and the change check each demands (copied into the node DoDs)

| AR | How it is kept | Change check (in the DoD) |
|---|---|---|
| AR-1 | The three words are rows of `finding_door_words` with `executor` and `writes_repository`. Code reads the capability key, never the word. | Grep `scripts/` for `"commit"`, `"stash"`, `"go on"` as literals in the touched functions: no hit outside the data file and the tests. |
| AR-9 | Each executor failure names what it expected and a door the person or the conductor can use. | Every failure text in B2 carries a door sentence (B2 test row). |
| AR-13 | One reader of the rows (`gate_brief.finding_door_words`). One builder of the state block (`gate_preflight.vcs_state_block`). One reader of the change set (`gate_preflight.vcs_changes`), called by `check_vcs` and by the executor. | Grep for `test repository state:` and `status", "--porcelain` in `scripts/`: only in the helper. |
| AR-14 | The waiver is written by `waiver.py`'s writer, git history by git. The new module is the one factory writer of gate-A repository actions. It needs an `artifact-writers.json` row only if F3-b is taken. | `test_artifact_writers.py` in the witness. |
| AR-15 | The guard rules (`stage_guard.rule_pathspec`, `rule_stash`, `rule_manifest`) are the one survivor of "what a factory commit/stash may take". The executor asks them before it runs. | B2 test row: the built command text passes both rules. A command made to take `qa-factory/` is refused by the executor, with the guard's text. |
| AR-16 | The hint is built from rows with the price lines of `human-questions.md` rule 6 (F4). It passes `human_text.problems`. | `test_gate_question_form.py` rows. |
| AR-17 | An unread word or a failed action reaches the conductor through the existing relay (`take_stand_gap_answers` → `note`/`hold`). There is no new driver stop. | No new `Person` / `Stop` in the driver set. A27 baseline unchanged. |
| AR-19 | Twins: the driver road (`driver_machine`) and the skill road (`s4.md` + the conductor-actions row + `conductor.md:21`) call ONE executor (function / CLI). | Axis 5 row added (B4, the Lead); the twins are named in the commit. |
| AR-22 | New produced fields (`waives` options, `executor`, `writes_repository`, price lines) each name their reader (§3.1). | `test_field_producers.py` if it reads `question-vocabulary.json` (not verified, §6). |
| AR-24 | The person's line reaches the executor whole (`--words-file` on the CLI, `person_words.read`). The record quotes it. | `test_words_doors.py` row: the CLI takes `--words-file` and prints `door()`. |
| AR-25 | New recorded states: "changes committed on the person's word" and "changes stashed on the person's word". Each names its reversal (the person's `git reset --soft <before>` / `git stash pop`) in the record and in `state-exits.md`. | `test_state_exits.py` in the witness. |
| AR-28 | An unreadable vocabulary, HEAD or change set never becomes a pass. Nothing is executed or offered (§3.3). | Rows in B1/B2 tests for the missing, unreadable and empty cases. |
| AR-29 | No check judges a role's work. The checks added (§1.1) are data and safety checks. | `test_judgment_census.py` in the witness. Any raised ceiling is named row by row (AR-20). |

### §1.1 Every check this spec adds or alters: owner it serves and census class

| Check | Where | Owner | Census class |
|---|---|---|---|
| A vocabulary row is dropped unless its option is in `FINDING_DOOR_OPTIONS`, `executor` is one of the closed executors, and it has a word | `gate_brief.finding_door_words` | data (code) | shape |
| A repository-writing word is read only as the whole answer (F5) | `gate_brief.finding_door_option` | intent (the person's word, read exactly) | word-list over the CLOSED vocabulary (FR-13). Not a phrase list. See §6 on whether it counts as a census unit. |
| The hint omits repository-writing rows in a run that leaves no trace | `gate_preflight.check_vcs` (via the hint builder) | intent (the run's standing decision) | shape |
| The change set at execution equals the one the shown door carries (digest) | `repo_words.run` | data | xref |
| The built command passes the guard rules | `repo_words.run` → `stage_guard` | intent (the person's repository) | safety |
| The executor refuses in a no-trace run (F2-a) | `repo_words.run` → `external_writes.closed_by_run` | intent | safety |

The executor returns `(done, problem)` and never raises a refusal. This follows the `product_gaps.record` precedent,
so it adds no refusal site to the census. Whether `test_judgment_census.py` still enumerates `repo_words.run` as a
check unit is not verified (§6). If it does, the row is `safety` / `intent` and the raise of `safety` 54 → 55 is named
in the verdict (AR-20).

---

## §2 Behaviour in one paragraph

Gate A's rehearsal finds uncommitted changes in the test repository. The finding `vcs-test-repo` now carries one door
per word: `accept` (unchanged), `go on`, `commit`, `stash`. Its `fix` is built from the vocabulary rows: each word,
what it does, and its three price lines. In a run that leaves no trace, only `go on` and `accept` are offered.

The person writes `vcs-test-repo: commit` (or `stash`, or `go on`). On the driver road `read_finding_doors` reads it
through `finding_door_option`. `_record_door_lines` hands it to `repo_words.run`. The function re-reads the change
set, checks it against the shown door, asks the guard rules, runs git, and records the person's word as a waiver on
the HEAD as it now stands (so the next rehearsal passes the finding, I-5). The person's line is quoted whole together
with what was done.

On the skill road the orchestrator runs the same `repo_words.py` CLI (a conductor-actions row). A word with no row,
or a line that is not exactly the word, goes to the conductor with the word list.

---

## §3 Shared definitions

### §3.1 Data: three rows in `question-vocabulary.json` `finding_door_words.answers`

Shape (values are the recommended text; the builder may polish the wording, not the meaning):

```json
{"option": "vcs_commit", "word": "commit", "executor": "git_commit", "writes_repository": true,
 "says": "I commit the uncommitted changes listed above on this branch, with a message that names this story, before the tests are written",
 "factory": "a factory command runs; no agent works.",
 "you": "nothing more; the commit is yours to keep, amend or undo.",
 "story": "the tests are written on a clean tree; delivery unchanged.",
 "synonyms": ["commit them", "commit it"]},
{"option": "vcs_stash", "word": "stash", "executor": "git_stash",  "writes_repository": true,
 "says": "I put the uncommitted changes listed above aside in a git stash, named after this story, before the tests are written",
 "factory": "a factory command runs; no agent works.",
 "you": "work of yours outside the factory: taking the changes back from the stash when you want them.",
 "story": "the tests are written on a clean tree; delivery unchanged.",
 "synonyms": ["stash them", "stash it"]},
{"option": "vcs_go_on", "word": "go on", "executor": "record", "writes_repository": false,
 "says": "the tests are written into this branch beside your uncommitted changes; nothing of yours is moved",
 "factory": "a record only; no agent works.",
 "you": "nothing more.",
 "story": "your changes and the story's tests share one tree; delivery unchanged.",
 "synonyms": ["go on on this branch", "go on as is"]}
```

- The block's `note` gains one sentence about `executor` (closed: `record`, `git_commit`, `git_stash`, plus the
  existing `product_gap`, which keeps its own branch) and `writes_repository`.
- `product_gap` gets `"executor": "product_gap"`, so every row names its executor (I-1).
- Readers:
  - `finding_door_words` reads `option`, `word`, `synonyms`, `executor`, `writes_repository` and the price lines.
  - The hint builder (§3.2) reads `says` and the price lines.
  - `_record_door_lines` dispatches on `executor` (B2).
  - `_relay_note` reads the words (B2).
- `FINDING_DOOR_OPTIONS` becomes `("product_gap", "vcs_commit", "vcs_stash", "vcs_go_on")`.
- Closed executors in code: `FINDING_DOOR_EXECUTORS = ("product_gap", "record", "git_commit", "git_stash")`. A row
  whose executor is not in the tuple is dropped, so a damaged file reads as fewer words, never a wrong one (the
  `stand_gap_words` direction, F0-7).

### §3.2 The hint builder (one function, one form)

`gate_brief.finding_door_hint(finding_id: str, options: list[str]) -> str`
- Returns the words of the given options, read from `finding_door_words()`, in the file's order. Each word is on its
  own line as `` `<id>: <word>` - <says> ``, followed by its three price lines `the factory:` / `you:` / `the story:`
  (rule 6, F4-a).
- Returns `""` when no option has a row. The caller then keeps the plain-words door (`waiver_command`), which already
  covers an unreadable file (I-1: nothing is offered that cannot be read).
- It is called only by `check_vcs` today. It lives in `gate_brief.py`, beside the one reader of the rows.

### §3.3 The change set and the state block (one reader each)

`gate_preflight.vcs_state_block(head: str) -> str` returns `f"test repository state: {head[:12]}"`, or `""` when there
is no head. `check_vcs:1939` calls it, and so does the executor.

`gate_preflight.vcs_changes(project_root, config) -> dict | None`
- Reads, exactly as `check_vcs` reads today: `tests_root`, `branch`, `head`, `dirty` (the porcelain lines outside the
  factory home).
- Adds `top` (`rev-parse --show-toplevel`; porcelain paths are relative to it) and
  `digest = sha256("\n".join(sorted(dirty)))[:12]`.
- Returns `None` in every case where `check_vcs` returns today: no project root, `tests_root` not a directory, git not
  answering the branch.
- `check_vcs` is rewritten to call it. **Its findings stay byte-identical in `message`, `id` and the
  `accept` door** (the non-goal: detection unchanged). This is asserted by a test row that compares the old and new
  output on the same repository.

---

## §4 Nodes

### §4.0 Order and ownership against part A

- Part A (t-105) owns: `gate_preflight.check_open_questions`, `gate_brief.still_open`, one helper in
  `question_register.py`, `tests/test_gate_preflight_question_status.py` and one row of `test-layers.json`. **No node
  below owns any of these.**
- B1 shares the FILES `gate_preflight.py` (a hot file, PROJECT.md «Командная работа» item 3) and `gate_brief.py` with
  part A, with disjoint functions. **Order: `очередь: A → B`.** B1 branches from `main` after t-105 is accepted and
  merged. If B1 must start earlier, it merges `main` into its tree after A lands, resolves the conflict itself, and
  gets one critic after the merge.
- Wave 0: B0. Wave 1: B1. Wave 2: B2 (needs B1's helpers and rows) and B3 (texts; needs B2's CLI name and flags,
  fixed in this spec, so B3 may run beside B2). Then B4 (the Lead). B5 is queued.

### B0 — wave-0 measurement: git's behaviour on every porcelain class (deterministic run, no package write)

- **Question.** Does `git add -- <paths>` + `git commit -m <msg> -- <paths>`, and
  `git stash push --include-untracked -m <msg> -- <paths>`, take exactly the listed entries for each porcelain class?
  The classes: `??` untracked file, `??` untracked folder (shown as `dir/`), ` M`, `M `, `MM`, ` D`, `D `, `A `,
  `R  old -> new`, a path with a space (quoted by porcelain), and a submodule pointer. Run it with the git of the owner's
  machine, on a scratch repository in the scratchpad, with the factory folder `qa-factory/` dirty beside the listed
  paths.
- **Output** (into this spec's §0 as F0-23, one command and one table): per class, whether both commands succeed and
  whether `qa-factory/` stays untouched.
- **Both outcomes.**
  - All classes behave → B2 takes every class.
  - A class fails or takes something unlisted → B2's executor refuses that class before running git, with a door
    ("commit or stash it yourself, then answer `go on`"). The class is named in B2's edge table.
  - The quoted-path class is refused in either outcome unless B0 shows a lossless read (I-2).
- **owns:** nothing in the repository. The scratch repository lives in the scratchpad. The result goes in the report
  to the Lead, who writes F0-23.
- **DoD:** the table, the git version, and the verbatim command output.

### B1 — data, reader, hint, doors (wave 1)

owns:
- `C:\QAFactory\forge-repo\ai-packages\qa-factory\references\question-vocabulary.json` (block `finding_door_words` only)
- `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\gate_brief.py` (`FINDING_DOOR_OPTIONS`, new `FINDING_DOOR_EXECUTORS`, `finding_door_words`, `finding_door_option`, `finding_door_word_of`, new `finding_door_hint`)
- `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\gate_preflight.py` (`check_vcs`, new `vcs_state_block`, new `vcs_changes`, `render`; NOT `check_open_questions`)
- `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_gate_vocabulary.py` (one new part beside `part_stand_gap_words`)
- `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_gate_question_form.py` (rows in `test_answer_forms_are_one_list_and_each_has_its_reader` / `_edges`)

**Behaviour**
1. The rows of §3.1 are added, and `product_gap` gains `executor`. `finding_door_words` returns each row with
   `executor`, `writes_repository` (bool, default false) and the price lines (default `""`). It drops a row whose
   `executor` is outside `FINDING_DOOR_EXECUTORS`.
2. `finding_door_option`: for a row with `writes_repository: true`, only the word alone or a synonym alone is read.
   The word followed by anything else returns `("", "")` (F5-a). Rows without the flag keep today's rule (word plus a
   separator plus a reason).
3. `check_vcs` gets its state from `vcs_changes` and its block from `vcs_state_block`, with byte-identical `message`
   and `accept` door. On the dirty branch it registers, after the `accept` door:
   - `door(block, option="vcs_go_on")`;
   - unless `external_writes.closed_by_run(task_root)` is truthy, `door(f"test repository changes: {head[:12]} {digest}", option="vcs_commit")` and the same block with `option="vcs_stash"`.

   The `fix` is `finding_door_hint(DOOR_ID, offered_options)` followed by `waiver_command(block)`. When the hint is
   `""`, the `fix` falls back to today's text without the three literal words: "answer with your approval - ...".
   It never names a word that has no row (I-1). `DOOR_ID` is replaced by `add` as today. The clean branch is
   unchanged (B5).
4. `render` indents every line of a multi-line `fix` under `      fix: ` (continuation lines get 10 spaces). A one-line
   `fix` prints byte-identical to today.

**Edges** (each protects the invariant named)

| Edge | Behaviour | Invariant |
|---|---|---|
| Vocabulary file unreadable or block missing | No vcs rows. Only the `accept` door is registered. The `fix` is the plain-words fallback, with no word named. | I-1, AR-28 |
| A row with an unknown `executor` / no word / an option outside the tuple | Dropped. The other rows stand. | I-1 |
| No HEAD (`head == ""`) | No door of any kind, as today (F0-2). The finding stands with the fallback `fix` and no words. | I-2: a commit is never offered without a block that pins the state |
| A no-trace run (`closed_by_run` truthy) | Only `vcs_go_on` and `accept` doors. The hint names only `go on`. | I-7 (F2-a), FR-36 |
| `closed_by_run` raises | Treated as closed: no repository-writing doors. | I-7: the safe default never advertises a write |
| More than 5 dirty paths | The message is unchanged ("and N more"). The digest door pins the whole set, so a change in a path the message hides still unreads the line at answer time. | I-2 |
| The tree changes between the packet and the answer | The fresh rehearsal's commit/stash door block (digest) differs from `shown_doors`, so `read_finding_doors` returns unread "the door this id showed is not the one it has now". The line goes to the conductor (existing path, F0-10). | I-2, I-3 |

**Tests** (rows, no new file; adversarial battery for the person's input, each a row)
- `test_gate_vocabulary.py`, new part `part_finding_door_words` (modelled on `part_stand_gap_words`):
  - The four rows are read with their executors. ASCII only. No word or synonym is shared with any other block or
    with `gate-approval-words.json` (the disjointness check extended to this block).
  - Damaged rows are dropped. An unreadable file gives `[]`.
  - `finding_door_option` table:
    - Read as the word: `commit`, `COMMIT`, `` `commit` ``, `commit.`, `  commit  `, `stash them`, `go on`, `Go On!`,
      `go on, the branch is mine` (reason kept).
    - Not read: `commit or stash`, `commit please`, `stash, then go on`, `commits`, `go onward`, `коммит` (built from
      code points, FR-30), `""`, `"   "`, a 1001-character line starting with `commit`, `commit\u200b`.
- `test_gate_question_form.py`:
  - A rehearsal finding shaped like the dirty `vcs-test-repo` (doors `accept`, `vcs_go_on`, `vcs_commit`,
    `vcs_stash`) is shown and read. Each of `vcs-test-repo: commit|stash|go on` is read by `Driver.read_finding_doors`
    with the option of its row. `vcs-test-repo: maybe` is read by none.
  - The `fix` of the finding passes `human_text.problems` and carries the three price lines per offered word.
  - In a no-trace finding, `commit` is unread ("the door of this finding does not take that word").
  - `check_vcs` on a temp git repository: same `message` and `accept` door as before the change (byte comparison
    against a literal captured from today's code in the same test).

**DoD:** `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/references/question-vocabulary.json ai-packages/qa-factory/scripts/gate_brief.py ai-packages/qa-factory/scripts/gate_preflight.py`
Run what it prints. The two rows above are green and go red when the B1 change is reverted (the builder states it,
no mutation list). Grep `"commit"|"stash"|"go on"` in `gate_preflight.py`/`gate_brief.py` outside docstrings: no hit
(AR-1). Also `python -B ai-packages/qa-factory/scripts/selftest.py --lang`. Name the AR rows of §1 the node touched:
AR-1, 13, 16, 22, 28.

### B2 — the executor and the driver road (wave 2)

owns:
- `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\repo_words.py` (new module: `run`, `main`)
- `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\driver_machine.py` (`_record_door_lines`, `_relay_note`; `read_finding_doors` only if a change proves needed, named in the report)
- `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_words_doors.py` (one new row function)
- `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\driver-layers.json` (only if its census demands a row for a changed method; not verified)

**`repo_words.run(task_root, project_root, config, option, line, replaced, door_block, words_ref, by) -> (done: dict, problem: str)`**
1. `option` → the row (`finding_door_words`). The executor must be `git_commit` or `git_stash`, else problem
   "not a repository word".
2. Refuse when `external_writes.closed_by_run(task_root)` is truthy (F2-a). Problem: "this run leaves no trace, so
   nothing is committed or stashed in your repository; answer `go on`, or do it yourself and answer `go on`".
3. `state = gate_preflight.vcs_changes(project_root, config)`. `None` → problem "the test repository could not be read
   by git (<why>)". `state["dirty"] == []` → problem "nothing is uncommitted now; nothing was done".
   `f"test repository changes: {head[:12]} {digest}" != door_block` → problem "the repository changed since you were
   shown the list; nothing was done".
4. Paths: `porcelain_path` per line, split on ` -> ` for a rename. A path starting with `"` (quoted by git), or of a
   class B0 marked unsafe → problem naming the path, with the door "commit or stash it yourself, then answer
   `go on`".
5. Build the commands. The flag tokens and the `--` separator are fixed; only the path tokens and the message vary.
   - commit: `["git", "add", "--", *paths]` then `["git", "commit", "-m", MESSAGE, "--", *paths]`
   - stash: `["git", "stash", "push", "--include-untracked", "-m", MESSAGE, "--", *paths]`

   `MESSAGE` is per F1: recommended `f"{task}: changes that were uncommitted before the QA Factory tests, {word} on your word at gate A"`.
   Before running, `stage_guard.rule_pathspec(text)` and `rule_stash(text)` (and `rule_manifest` for a commit) are
   asked on the joined command text. Any refusal → problem = the guard's text, and git is not run (I-4).
6. Run with `cwd = state["top"]`. Environment as `_git` (no prompts). Timeout `REPO_WORD_TIMEOUT = 120` s (the
   person's hooks may run). No `--no-verify`, no `-c` override.
7. After the run, read `head_after` and `vcs_changes` again.
   - Success (exit 0 on every step) → record the waiver: `waiver.py --task <T> --stage S5 --block vcs_state_block(head_after) --words-file <words_ref> --by <by>`.
     The decision text is `person_decision(word, line, replaced)` + `"; done: <commit <sha12> of N path(s) | stash '<MESSAGE>' of N path(s)>; to undo: <git reset --soft <head_before12> | git stash pop>"` (F3-a).
   - Return `done = {"word", "head_before", "head_after", "paths": N, "undo"}`.
8. Failures (each with `problem` and no waiver):
   - git exit ≠ 0 → git's stderr, last 600 characters, plus "nothing is passed; the question stays open".
   - `git add` succeeded and `commit` failed → also run `git reset -q -- <paths>`, so the index is as before (the add is
     undone). If the reset fails, say so.
   - Timeout → re-read HEAD and the change set. The problem says "the command did not finish in 120 s; HEAD is now
     <x> (was <y>)", so the conductor reads the state. No retry.
   - The action succeeded but the waiver failed → problem "the commit/stash IS made (<facts>); only the record of
     your word failed: <text>". The conductor records it (conductor.md row, B3).
9. `main()`: the CLI `repo_words.py --task <T> --word commit|stash --words-file <file> [--by person|conductor|orchestrator]`.
   - It runs a fresh `gate_preflight` rehearsal of gate A and takes the `vcs-test-repo` finding's door for the word.
   - A missing door → exit 2 with a door ("the question no longer offers that word; show gate A again").
   - The person's line comes through `person_words.read`. It calls `run` and prints one line, or the problem and
     `person_words.door(...)` on exit 3.
   - The CLI's `--word` takes the vocabulary WORD (data), mapped to its option through `finding_door_words` (AR-1).

**Driver changes**
- `_record_door_lines`: before the generic waiver branch, a branch on the row's executor (looked up by
  `door["option"]` through `finding_door_words`). `git_commit`/`git_stash` → `repo_words.run(...)` with
  `door_block = door["block"]` and `words_ref = self.words_file(line, "repoword")`.
  - `problem` → `failed.append((entry["id"], line, problem))` (existing relay, I-6).
  - Done → `recorded.append`, and print `gate A: vcs-test-repo: <word> done on the person's word (<facts>)`.
  - `vcs_go_on` (executor `record`) takes the existing generic waiver branch unchanged. The block is the HEAD block.
    No reason is required (the reason rule is keyed on option `accept` only, F0-10).
- `_relay_note` `door_keys`: a door whose option has a row also lists its word (`` `word` `` from
  `finding_door_word_of()`). Then the conductor sees `word option vcs_commit (\`commit\`)` and the list of words a line
  may use (requirement 4 of the brief).
- No change to the read order of `read_finding_doors`. The new options are read by the existing
  `finding_door_option` fallback (`:3140-3144`), AFTER the stand-gap words, so no existing word changes meaning.

**Edges**

| Edge | Behaviour | Invariant |
|---|---|---|
| Empty answer / no `vcs-test-repo:` line | Nothing read. The finding stays open, and the gate's own reading applies (`approve` does not pass an open item; `approve as is` does, recorded with words, as today). | I-3 |
| Two lines `vcs-test-repo: commit` / `vcs-test-repo: stash` | The last wins (existing rule). The executor runs once for it, and `replaced` names the earlier line in the record. | I-3 (P13) |
| `vcs-test-repo: commit or stash` / `commit please` | Unread (B1 F5-a). Goes to the conductor with the word list. | I-3 |
| A word in another case | Read (`_word_key`). Another language → unread → conductor. | I-3, FR-12 |
| `?` anywhere | Unread (existing). | I-3 |
| Test repository absent / not a git repository | `check_vcs` writes no finding (as today), so no door and no line to read. At execution `vcs_changes` is None → problem. | AR-28 |
| Nothing to commit (tree cleaned between show and answer) | The digest differs → unread at read time. If it still reaches `run`, problem "nothing is uncommitted now". | I-2 |
| A dirty tree with `go on` | Waiver on the HEAD block. S5 writes into the tree. Later changes do not re-ask (F0-2). | I-5 |
| The repeated question after `commit` | The waiver is on `head_after`. The next rehearsal's clean-tree finding (`this branch, or name another`) carries the block of `head_after` and is dropped by `add`. The dirty finding does not exist. Asserted by a row. | I-5 |
| The repeated question after `stash` | HEAD is unchanged, the waiver is on HEAD, so the clean finding is dropped. | I-5 |
| Commit refused by the person's hook / no git identity / signing prompt | git exit ≠ 0 or timeout → failed, add undone, conductor. | I-4, I-6 |
| tests_root inside the product's repository | The change set is the whole repository outside `qa-factory/` (as the message already lists it), so product-code changes are committed or stashed too. The `says` of commit/stash says "the uncommitted changes listed above". F1 asks whether to say "product code included" explicitly. | I-2 |
| `approve` + `vcs-test-repo: commit` in one answer, commit fails | The failed line joins `hold` and the approval is held for the conductor (existing `gate_lines_over_approval`). | I-6 |
| A dry run (`self.dry`) | `take_stand_gap_answers` returns `{}` before reading (existing `:2515`). Nothing runs. | I-3 |

**Tests** (one row function in `test_words_doors.py`, built ONCE on a temp git repository plus a seeded task root;
each line a case):
- `commit`: HEAD moves, the listed paths are committed, `qa-factory/` stays dirty, the waiver is recorded on the new
  block with the line quoted and the undo named, and the next `check_vcs` gives no `vcs-test-repo`.
- `stash`: the tree is clean outside `qa-factory/`, `git stash list` has the message, the waiver is on HEAD, and no
  re-ask.
- `go on`: a waiver only, the tree untouched.
- A stale digest: nothing runs. A no-trace pipeline: refused with its door. A path git quotes: refused, naming it.
- A pre-commit hook that exits 1: failed, the index restored, no waiver.
- The built command texts pass `stage_guard.rule_pathspec` / `rule_stash`. A path list holding `qa-factory/x` is
  refused by the executor with the guard's text.
- The CLI takes `--words-file` and prints `door()` on refusal (the AR-24 row form).

**DoD:** `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/repo_words.py ai-packages/qa-factory/scripts/driver_machine.py`
Run what it prints, plus `test_judgment_census.py`, `test_artifact_writers.py`, `test_state_exits.py` if not
printed. A raised ceiling is named row by row. Report the FR pass (§7) and the AR rows touched: AR-9, 13, 14, 15, 17,
24, 25, 28, 29.

### B3 — the skill road and the conductor's texts (wave 2, beside B2)

owns:
- `C:\QAFactory\forge-repo\ai-packages\qa-factory\skills\qa-story\phases\s4.md` (the paragraph at `:159-163` only)
- `C:\QAFactory\forge-repo\ai-packages\qa-factory\references\conductor-actions.json` (one new row after the `product_gaps.py record` row)
- `C:\QAFactory\forge-repo\ai-packages\qa-factory\references\conductor.md` (the row at `:21`)
- `C:\QAFactory\forge-repo\ai-packages\qa-factory\references\halts.md` (the row at `:19`)
- `C:\QAFactory\forge-repo\ai-packages\qa-factory\design\state-exits.md` (two new rows)
- `C:\QAFactory\forge-repo\ai-packages\qa-factory\changelog.d\fg7-8-b-vcs-words.md` (new fragment)

**Behaviour**
- `s4.md`: one sentence. A finding's own words (the ones its `fix` lists, e.g. `commit`, `stash`, `go on` on the
  test-repository item) are carried out by the command of their conductor-actions row. A word the finding does not
  list, or any other wording, is read by you and mapped to one of those words or to nothing. Nothing is committed or
  stashed on a word you inferred.
- conductor-actions row:
  - says: "the person answers the test-repository item with `commit` or `stash` (or says so in other words that map
    to exactly one of them)".
  - run: `repo_words.py --task <T> --word <the word> --words-file <file>`, once. A refusal is told to the person in
    words, and nothing else runs. `go on` is the item's waiver: `waiver.py --task <T> --stage S5 --block "<the item's block>" --words-file <file>`.
- `conductor.md:21` names the row for commit/stash. `halts.md:19`: the dirty tree is a gate A item. Its words are the
  item's own (the vocabulary rows), and the four literal words are removed. If the row is dead, it points to gate A.
- `state-exits.md`: "changes committed on the person's word at gate A" → exit `git reset --soft <head_before>`, the
  person's (the record names it). "changes stashed on the person's word at gate A" → exit `git stash pop`, the
  person's.
- Changelog fragment: one paragraph.

**Edges:** a word the orchestrator maps from other words is run only when the mapping is to exactly one word (I-3).
Two possible words, or none → ask, never run.

**Tests:** none new (texts). The witness runs what `--witness-for` prints for these paths (e.g. `test_conductor_doors.py`
if it reads conductor-actions rows, `test_state_exits.py`, `test_words_doors.py` (a) scan: the new row uses
`--words-file`, no inline words).

**DoD:** `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/skills/qa-story/phases/s4.md ai-packages/qa-factory/references/conductor-actions.json ai-packages/qa-factory/references/conductor.md ai-packages/qa-factory/references/halts.md ai-packages/qa-factory/design/state-exits.md`
Plus `selftest.py --lang` and `role_load.py --all` before and after (AR-11 text added). Report AR-17, AR-19, AR-25.

### B4 — the Lead: the map row

owns: `C:\QAFactory\forge-repo\docs\SIBLING_MAP.md` (axis 5, one new row "Gate A test-repository words").
- Data: `finding_door_words`.
- Reader: `gate_brief.finding_door_words` / `finding_door_option`.
- Hint: `finding_door_hint`.
- Door: `check_vcs`.
- Driver: `_record_door_lines`.
- Executor: `repo_words.run`.
- Skill road: `s4.md` + conductor-actions row + `conductor.md:21`.
- Detector rows: the B1/B2 tests.

DoD: the row is present, and axis 34's symmetry is satisfied (one executor, two roads).

### B5 — queued residual (F6): the same class in the neighbouring literals

owns (when taken):
- `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\gate_preflight.py` (`check_vcs` clean branch, `check_stand`)
- `C:\QAFactory\forge-repo\ai-packages\qa-factory\references\question-vocabulary.json`
- `C:\QAFactory\forge-repo\ai-packages\qa-factory\skills\qa-story\evals\evals.json` (`:53`, `:64`)
- `C:\QAFactory\forge-repo\ai-packages\qa-factory\evals\plugin-eval-benchmark.json` (`:86-93`)

Behaviour:
- The clean-tree hint `this branch, or name another` (`:1952`). "name another" has no executor. A branch switch is a
  new executor and needs the owner's word, since it is a new word.
- `check_stand`'s `fix the stand first, or let the stage run and report what it could not execute` (`:1978-1979`).
- The two eval files that expect a removed S5 halt.

Test: rows in `test_gate_question_form.py`. The Lead files it as a finding into an untaken batch of the pile.

---

## §5 Forks (decisions belong to the Lead / the owner)

| id | Fork | Options and consequences (person / story) | Recommendation |
|---|---|---|---|
| F1 | Scope and message of `commit` / `stash` | **(a) Exactly the dirty set the person was shown** (outside `qa-factory/`, the whole repository incl. product code when tests live in the product repository), one commit with the message `"<task>: changes that were uncommitted before the QA Factory tests, committed on your word at gate A"`, under the repository's configured identity, the person's hooks running. Person: their work-in-progress lands as one commit with a factory-written message on their branch; undo named. Story: a clean tree. **(b) Only paths under `tests_root`**: product WIP stays dirty, so the tree is still dirty, and the finding re-asks (I-5 breaks). **(c) The person writes the message** (`commit: <message>`): needs the reason form for a repository word, against F5. | (a). In addition, the `says` names "product code included" when `tests_root` and the product share the repository (one data clause read by a flag `vcs_changes` already knows: `top` vs the project root). |
| F2 | P8: a run that leaves no trace | **(a) `commit`/`stash` are neither offered nor executed** (FR-36); `go on` only. Person: in a comparison run they commit or stash themselves. Story: unchanged. **(b) Allowed**: a local commit is not an outward write. But it is a trace in the project's history, against P8 "no trace in the project". | (a) |
| F3 | The record and its reader | **(a) The waiver's decision text carries the facts and the undo**. One writer (`waiver.py`), existing readers (`waiver --list` at later gates, the report's words section). No new artifact. **(b) A new `state/repo-words.jsonl` record** plus a reader in the report ("Left with you": "your changes are in the stash ..."). Costs an `artifact-writers.json` row, a `stages.json` output and a report reader. | (a). Upgrade to (b) only if the report must list a stash among "Left with you" (the owner's call: is popping the stash a check left with the person?). |
| F4 | The form of the hint (human-questions rule 6) | **(a) One line per word with its three price lines** in the finding's `fix`, rendered indented (`render` change). **(b) One line naming the words with `says` only**, the price lines omitted (today's debt kept), plus a `factory-rules-debt.md` row. | (a) |
| F5 | How a repository-writing word is read | **(a) The word or a synonym ALONE**. `commit please`, `commit or stash` → conductor. Person: a polite or explained answer costs one conductor turn. Story: never a wrong write. **(b) The word plus a reason**, like `product gap`. `commit or stash` would read as commit with reason "or stash". | (a). `go on` keeps the reason form. |
| F6 | The siblings of the same class (clean-tree "name another", `check_stand`'s literal, two stale eval files) | **(a) Queued node B5** with owns and a test (designer rule 6: a residual is a node). **(b) In this node**: needs a new executor (branch switch) and new words, against the Lead's non-goal. | (a) |
| F7 | `stash` and untracked files | **(a) `--include-untracked`, limited to the listed paths**: the tree becomes clean outside `qa-factory/`. **(b) Tracked changes only**: untracked files stay, so the tree is still dirty and the finding re-asks. | (a) |

### Small choices closed by the designer
- Module name `repo_words.py`: no `test_` prefix, so it is never taken for a test file.
- Option names `vcs_commit` / `vcs_stash` / `vcs_go_on`. Executor keys `record` / `git_commit` / `git_stash`.
- `accept` stays on the vcs door as the universal door (FR-4). `go on` uses the same executor (a waiver on the HEAD
  block) without the reason requirement.
- Digest: sha256 of the sorted kept porcelain lines, 12 hex. Block `test repository changes: <head12> <digest12>`
  (≤ 60 chars).
- Timeout 120 s. A failed `commit` after `add` is undone with `git reset -q -- <paths>`.
- The executor returns `(done, problem)`, never raises (`product_gaps.record` precedent).
- Synonyms kept minimal (two per word), disjoint from every other block.

---

## §6 Not verified

- The git behaviour per porcelain class on the owner's machine (B0 measures it before B2).
- Whether `test_judgment_census.py` enumerates a function that only returns problems (no `ValueError`) as a check unit,
  and so whether `repo_words.run` needs a census row. The same question for the F5 condition in
  `finding_door_option`, which is not in the census today (Grep of the census file: no `finding_door` hit).
- Whether `waiver.py` accepts `--words-file` together with a composed decision text that carries the facts, or whether
  the facts must go into the words file. The builder reads `waiver.py`'s CLI. This is a small technical choice; the
  person's line is quoted whole either way.
- `contract.person_decision` and `Driver.words_file` signatures: they were read only as call sites
  (`driver_machine.py:2819, 2851`).
- Whether `test_words_doors.py`'s harness (`temp_project`, `run_script`) supports a temp git repository without new
  helpers. If not, the B2 row goes to `test_gate_question_form.py`, which already builds a `Driver.__new__`.
- Whether `test_field_producers.py` / `test_conductor_doors.py` read `question-vocabulary.json` /
  `conductor-actions.json` rows. `--witness-for` will say.
- Whether `halts.md:19`'s S5 row is still reached on any road. No driver part has an S5 dirty check (Grep
  `dirty|uncommitted` -i over `driver_*.py`: only walk-claim hits, so the tool works). Not checked: the skill road's
  S5 entry beyond `s5.md:108-110` and `s5_precheck.py` (empty Grep, no positive control run).
- Whether a commit at gate A disturbs `test_repo_base` readers. The base is recorded at S0 with the dirty paths and
  their hashes. The committed paths keep their hashes, so they should read as base, but this was not run.

---

## §7 FR pass by sections (A-C, the ones this change touches)

- **A refusals and doors.**
  - FR-1 / FR-2: every executor problem says what is wrong, what it expected, and a door the person or the conductor
    can use (§4 B2 step 8).
  - FR-3: a failure is reported, not put back to the person.
  - FR-4: `go on` / `accept` pass by an informed word; nothing passes silently.
  - FR-46: a failure's class is the story's (git refused), or the call's (stale door).
  - FR-48: the conductor gets the failed line once.
  - FR-57: the guard rules are asked, the hooks run, no override.
  - FR-5 / FR-50: n/a. FR-59: an unreadable state never passes (§4 B1/B2 edges).
- **B text shown to a person.**
  - FR-6: the hint follows `human-questions.md` (rule 4 closed set, rule 6 prices, F4).
  - FR-7: no re-ask after commit/stash (I-5, a test row).
  - FR-8 / FR-9: the person's line reaches its executor and every offered word has one (I-1).
  - FR-10: the packet's `fix` and the How-to-answer block do not contradict each other (`accept` and the three words
    are all read).
- **C contracts between code and roles.**
  - FR-11: the conductor-actions row names a command that exists (B2 CLI).
  - FR-12: no phrase list. Only closed words are read; free words go to the conductor.
  - FR-13: words in data.
  - FR-14: the CLI output is one line or a problem plus a door.
  - FR-15: the orchestrator is given the command.
  - FR-38: the waiver block the next rehearsal checks is the one the executor records.
  - FR-39 / FR-56 / FR-49 / FR-42: the executor's returned states (done, each problem) each have a move (record /
    conductor).
- D-G: not touched beyond FR-30 (English, ASCII data) and FR-32 (tests rows).

---

## §8 Reading trail

- `plans/piles/forge/findings/20261111-ostatki-sliyaniya-eksperimenta-v-main.md:1-60` (FG7-8 item 4)
- `plans/piles/thinking-roles/findings/20261106-plecho-b-shvy-pervogo-prohoda.md:25-51` (TR2-9)
- `scripts/gate_preflight.py`: 205-258, 1318-1438, 1880-1990, 5787-5820, 5917-5991
- `scripts/gate_brief.py`: 420-569, 640-840, 2840-2930, 3022-3066
- `scripts/driver_machine.py`: 2490-2978, 3078-3227
- `scripts/driver_s0.py`: 2190-2299 (`s0.flags`: `commit` there is a code source, unrelated)
- `scripts/driver_core.py`: 653-665
- `scripts/external_writes.py`: 189-202
- `scripts/stage_guard.py`: 1037-1053, 2280-2430, 2830-2890
- `scripts/test_repo_base.py`: 1-80
- `scripts/driver_gates.py`: 95-134
- `references/question-vocabulary.json` (whole); `references/gate-approval-words.json` (whole);
  `references/question-prices.json`: 1-70; `references/conductor-actions.json`: 1-60; `references/halts.md` (whole);
  `references/human-questions.md`: 1-134
- `skills/qa-story/phases/s4.md`: 125-164; `skills/qa-story/phases/s5.md`: 95-129 (+ Grep)
- `design/architecture.md`: 134-283 (+ Grep of change checks)
- `docs/SIBLING_MAP.md`: 111-158, 248-287, 580-591; `docs/TESTING.md` (whole)
- `scripts/tests/test-layers.json`: 1-45, 1890-2020, 6790-6820 (+ Grep keep/quarantine positions)
- `scripts/tests/test_gate_question_form.py`: 730-840; `test_gate_vocabulary.py`: 250-340;
  `test_decision_classes.py`: 415-489; `test_words_doors.py`: 1-80 (+ Grep)
- `scripts/tests/scenario_walk.py`: 200-365 (+ Grep); `fixtures/judgment-census.json`: 1-30 (+ Grep)
- `evals/plugin-eval-benchmark.json`: 84-96; `CHANGELOG.md`: 826-835
- Greps (the Grep tool, case-insensitive where stated):
  - `check_vcs|commit, stash|go on` -i, scripts
  - `"go on"|"stash"|"commit"`, json/py
  - `stash` in *.md
  - `dirty|uncommitted|vcs-test-repo|test repository state` -i, md/json
  - `dirty|uncommitted` -i in `driver_*.py` (hits found: positive control)
  - `read_finding_doors|finding_door_option|finding_door_words|stand_gap_words\(`
  - `test-repo-base`; `def no_trace|...`
- Needed beyond the manifest: `stage_guard.py`, `external_writes.py`, `test_repo_base.py`, `conductor-actions.json`,
  `halts.md`, `judgment-census.json`, `scenario_walk.py`, the evals files.
